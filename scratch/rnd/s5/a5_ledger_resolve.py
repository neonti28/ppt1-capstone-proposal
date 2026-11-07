#!/usr/bin/env python3
"""Audit S5 - resolusi tiap baris ledger ke path JSON yang diklaimnya.

Untuk setiap baris ledger kartu S1..S4:
  - ambil kolom Angka dan kolom Rujukan persis
  - resolusi path JSON (nama berkas + jalur bertitik) terhadap artefak kartu
  - bandingkan nilai dengan toleransi sesuai jumlah desimal angka ledger
Klasifikasi: MATCH / MISMATCH / TIDAK_RESOLVE (formula atau path khusus).
"""
import json
import pathlib
import re
from collections import Counter

BASE = pathlib.Path("/mnt/d/Capstone 1(v2)")
LEDGER = BASE / "docs/RND_PROVENANCE_LEDGER.md"
CARD = {"S1": "s1", "S2": "s2", "S3": "s3", "S4": "s4"}


def muat_json(kartu):
    bundle = {}
    for p in (BASE / "scratch/rnd" / kartu).glob("*.json"):
        try:
            bundle[p.name] = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            bundle[p.name] = {"__error__": str(e)}
    for p in (BASE / "scratch/rnd" / kartu).glob("*.jsonl"):
        try:
            bundle[p.name] = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
        except Exception as e:
            bundle[p.name] = {"__error__": str(e)}
    return bundle


def baris_ledger(kartu):
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


def parse_angka(s):
    s = s.strip().replace("`", "")
    m = re.match(r"^-?\d{1,3}(?:\.\d{3})+(?:,\d+)?$|^-?\d+(?:[.,]\d+)?$", s)
    if not m:
        return None, 0
    if re.search(r"\.\d{3}(?:,|$)", s) and "," in s:
        v = float(s.replace(".", "").replace(",", "."))
        dec = len(s.split(",")[1])
    elif re.search(r"\.\d{3}$", s):
        v = float(s.replace(".", ""))
        dec = 0
    else:
        v = float(s.replace(",", "."))
        dec = len(s.split(",")[1]) if "," in s else (len(s.split(".")[1]) if "." in s else 0)
    return v, dec


def ambil_cabang(obj, sisa):
    cur = obj
    for bagian in sisa:
        if isinstance(cur, list):
            if not bagian.isdigit():
                return None, False
            i = int(bagian)
            if i >= len(cur):
                return None, False
            cur = cur[i]
        elif isinstance(cur, dict):
            if bagian in cur:
                cur = cur[bagian]
            else:
                return None, False
        else:
            return None, False
    return cur, True


def resolusi(bundle, rujukan):
    """Kembalikan (nilai, keterangan). nilai None berarti tidak dapat diresolusi."""
    teks = rujukan.replace("`", "")
    m = re.match(r"^(\S+?\.jsonl?|(?:inventory|token_scan|s\d\w*)[\w\.]*)", teks)
    fname = None
    for nama in bundle:
        if nama in teks:
            fname = nama
            break
    if fname is None:
        return None, "tanpa_nama_berkas"
    sisa = teks.split(fname, 1)[1]
    sisa = re.split(r"\s{2,}|\s=\s|\s\(|=|\[", sisa)[0]
    sisa = sisa.strip(" .,:;")
    if not sisa:
        return None, "tanpa_jalur"
    if re.search(r"[A-Za-z_]+\s+[A-Za-z]", sisa) or "/" in sisa:
        return None, "jalur_bebas_teks"
    jalur = [b for b in re.split(r"\.|\[|\]", sisa) if b not in ("", "$")]
    val, ok = ambil_cabang(bundle[fname], jalur)
    if not ok:
        return None, "jalur_tidak_ada"
    if isinstance(val, bool):
        return None, "boolean"
    if isinstance(val, (int, float)):
        return float(val), "ok"
    if isinstance(val, str):
        v, _ = parse_angka(val)
        if v is not None:
            return v, "ok_string"
        return None, "string_bukan_angka"
    return None, "bukan_skalar"


def main():
    hasil = {}
    for kartu, folder in CARD.items():
        bundle = muat_json(folder)
        rows = baris_ledger(kartu)
        kl = Counter()
        mismatch = []
        tak = []
        for sel in rows:
            kode, angka_s, satuan, kelas, rujukan, dipakai, status = sel
            v, dec = parse_angka(angka_s)
            if v is None:
                kl["angka_bukan_numerik"] += 1
                tak.append((kode, angka_s[:24], "angka bukan numerik"))
                continue
            got, ket = resolusi(bundle, rujukan)
            if got is None:
                kl[ket] += 1
                tak.append((kode, angka_s, ket))
                continue
            tol = 0.5 * 10 ** (-dec) + 1e-9
            if abs(got - v) <= tol:
                kl["MATCH"] += 1
            else:
                kl["MISMATCH"] += 1
                mismatch.append(dict(kode=kode, ledger=v, json=got, selisih=round(got - v, 8),
                                     rujukan=rujukan[:110]))
        hasil[kartu] = dict(n_baris=len(rows), klasifikasi=dict(kl), mismatch=mismatch,
                            tidak_resolve=tak[:60])
        print("=" * 74)
        print(kartu, "baris:", len(rows), "| kelas:", dict(kl))
        for m in mismatch[:10]:
            print("  MISMATCH", m)
        contoh = [t for t in tak if t[2] in ("jalur_tidak_ada", "string_bukan_angka")][:8]
        for t in contoh:
            print("  tak-resolve", t)

    (BASE / "scratch/rnd/s5/s5_ledger_resolve.json").write_text(
        json.dumps(hasil, indent=1, ensure_ascii=False), encoding="utf-8")
    print("\nWROTE scratch/rnd/s5/s5_ledger_resolve.json")


if __name__ == "__main__":
    main()
