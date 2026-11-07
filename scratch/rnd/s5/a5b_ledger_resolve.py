#!/usr/bin/env python3
"""Audit S5 - resolusi baris ledger ke artefak JSON (versi 2).

Perbaikan atas versi 1:
  - desimal titik dan koma sama-sama dicoba, karena ledger mencampur keduanya
  - path tanpa nama berkas dicari ke seluruh JSON kartu
  - sel multi-nilai (mis. "3577 record / 8343.253 jam") diuji per komponen
    terhadap daun numerik cabang yang dirujuk
  - rujukan filesystem (os.path.getsize) diuji langsung ke disk

Batasan yang harus disebut di laporan: untuk sel multi-nilai, yang dibuktikan
adalah KEBERADAAN nilai di cabang, bukan pemetaan posisional nilai ke kunci.
"""
import json
import os
import pathlib
import re
from collections import Counter

BASE = pathlib.Path("/mnt/d/Capstone 1(v2)")
LEDGER = BASE / "docs/RND_PROVENANCE_LEDGER.md"
CARD = {"S1": "s1", "S2": "s2", "S3": "s3", "S4": "s4"}
PATHTOK = re.compile(r"(?:[A-Za-z_][A-Za-z0-9_]*)(?:\.[A-Za-z0-9_\]\[]+)+")


def muat(kartu):
    b = {}
    for p in (BASE / "scratch/rnd" / kartu).glob("*.json*"):
        try:
            if p.suffix == ".jsonl":
                b[p.name] = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
            else:
                b[p.name] = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            b[p.name] = {"__error__": str(e)}
    return b


def baris(kartu):
    out, aktif = [], False
    for l in LEDGER.read_text(encoding="utf-8").splitlines():
        if l.startswith("## Bagian"):
            aktif = bool(re.search(r"Bagian %s\b" % kartu, l))
            continue
        if aktif and l.startswith("| %s-" % kartu):
            sel = [c.strip() for c in l.strip().strip("|").split("|")]
            if len(sel) == 7:
                out.append(sel)
    return out


def kandidat_angka(sel):
    """Semua token angka dalam sel, tiap token dengan dua tafsir (titik/koma)."""
    out = []
    for tok in re.findall(r"-?\d[\d.,]*", sel):
        tok = tok.rstrip(".,")
        if not tok:
            continue
        try:
            if "," in tok and "." in tok:
                v = float(tok.replace(".", "").replace(",", "."))
                out.append((v, len(tok.split(",")[1])))
            elif "," in tok:
                out.append((float(tok.replace(",", ".")), len(tok.split(",")[1])))
            elif "." in tok:
                out.append((float(tok), len(tok.split(".")[1])))   # titik desimal
                if re.match(r"^\d{1,3}(?:\.\d{3})+$", tok):         # titik ribuan
                    out.append((float(tok.replace(".", "")), 0))
            else:
                out.append((float(tok), 0))
        except ValueError:
            continue
    return out


def cabang(obj, jalur):
    cur = obj
    for b in jalur:
        if isinstance(cur, list):
            if not b.isdigit() or int(b) >= len(cur):
                return None, False
            cur = cur[int(b)]
        elif isinstance(cur, dict):
            if b not in cur:
                return None, False
            cur = cur[b]
        else:
            return None, False
    return cur, True


def daun(o, keluar, kedalaman=0):
    if kedalaman > 4:
        return
    if isinstance(o, bool):
        return
    if isinstance(o, (int, float)):
        keluar.append(float(o))
    elif isinstance(o, dict):
        for v in o.values():
            daun(v, keluar, kedalaman + 1)
    elif isinstance(o, list):
        for v in o[:4000]:
            daun(v, keluar, kedalaman + 1)


def cari_path(bundle, rujukan):
    """Kembalikan (nama_berkas, jalur, nilai_cabang) hasil pencarian terbaik."""
    toks = PATHTOK.findall(rujukan.replace("`", ""))
    # prioritas: berkas disebut eksplisit
    fname = next((n for n in bundle if n in rujukan), None)
    for tok in toks:
        jalur = tok.split(".")
        if jalur[0] in ("os", "pd", "data"):
            continue
        kandidat = [fname] if fname else list(bundle)
        for n in kandidat:
            val, ok = cabang(bundle[n], jalur)
            if ok and val is not None and not isinstance(val, str):
                return n, jalur, val
    return None, None, None


def cek_fs(rujukan):
    m = re.search(r"os\.path\.getsize\s+[`'\"]?([^\s`,;'\"]+)", rujukan)
    if not m:
        return None
    p = BASE / m.group(1)
    if p.exists() and p.is_file():
        return p.stat().st_size
    return None


def main():
    hasil = {}
    for kartu, folder in CARD.items():
        bundle = muat(folder)
        rows = baris(kartu)
        kl, mismatch, tak = Counter(), [], []
        for sel in rows:
            kode, angka_s, satuan, kelas, rujukan, dipakai, status = sel
            angka = kandidat_angka(angka_s)
            if not angka:
                kl["angka_bukan_numerik"] += 1
                tak.append((kode, angka_s[:30], "angka bukan numerik"))
                continue
            n, jalur, val = cari_path(bundle, rujukan)
            if val is None:
                fs = cek_fs(rujukan)
                if fs is not None:
                    v, dec = angka[0]
                    tol = 0.5 * 10 ** (-dec) + 1e-6
                    if abs(fs - v) <= tol:
                        kl["MATCH_fs"] += 1
                    else:
                        kl["MISMATCH_fs"] += 1
                        mismatch.append(dict(kode=kode, ledger=v, disk=fs, rujukan=rujukan[:100]))
                    continue
                kl["tidak_resolve"] += 1
                tak.append((kode, angka_s[:30], "path tidak ditemukan"))
                continue
            leaves = []
            daun(val, leaves)
            if isinstance(val, bool):
                leaves.append(1.0 if val else 0.0)
            elif isinstance(val, (int, float)):
                leaves.append(float(val))
            if isinstance(val, dict) and val and all(isinstance(x, bool) for x in val.values()):
                leaves.append(float(sum(1 for x in val.values() if x)))
            # cukup satu tafsir desimal yang cocok: sel dengan pola 1.234 memang ambigu
            cocok = 0
            for v, dec in angka:
                tol = 0.5 * 10 ** (-dec) + 1e-6
                if any(abs(x - v) <= tol for x in leaves):
                    cocok += 1
            if cocok:
                kl["MATCH" if cocok == len(angka) else "MATCH_sebagian"] += 1
                if any(re.match(r"^\d{1,3}(?:\.\d{3})+$", a) for a in re.findall(r"\d[\d.]*", angka_s)):
                    kl["ambigu_titik_ribuan"] += 1
            else:
                kl["MISMATCH"] += 1
                mismatch.append(dict(kode=kode, sel=angka_s[:40], berkas=n, jalur=".".join(jalur),
                                     cocok=f"0/{len(angka)}", daun=leaves[:8],
                                     rujukan=rujukan[:100]))
        hasil[kartu] = dict(n_baris=len(rows), kelas=dict(kl), mismatch=mismatch, tidak_resolve=tak)
        print("=" * 76)
        print(kartu, "baris", len(rows), "|", dict(kl))
        for m in mismatch[:12]:
            print("   MISMATCH", m)

    (BASE / "scratch/rnd/s5/s5_ledger_resolve2.json").write_text(
        json.dumps(hasil, indent=1, ensure_ascii=False), encoding="utf-8")
    print("\nWROTE scratch/rnd/s5/s5_ledger_resolve2.json")


if __name__ == "__main__":
    main()
