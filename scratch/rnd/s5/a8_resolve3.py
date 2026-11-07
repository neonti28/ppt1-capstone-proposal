#!/usr/bin/env python3
"""Audit S5 - resolusi ledger v3 (path satu token), kelas sumber, dan tabel artefak."""
import json
import pathlib
import re
from collections import Counter

BASE = pathlib.Path("/mnt/d/Capstone 1(v2)")
LEDGER = BASE / "docs/RND_PROVENANCE_LEDGER.md"
CARD = {"S1": "s1", "S2": "s2", "S3": "s3", "S4": "s4"}
TOK = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z0-9_]+|\[\d+\])*")


def muat(kartu):
    b = {}
    for p in (BASE / "scratch/rnd" / kartu).glob("*.json*"):
        try:
            b[p.name] = ([json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
                         if p.suffix == ".jsonl" else json.loads(p.read_text(encoding="utf-8")))
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
    out = []
    for tok in re.findall(r"-?\d[\d.,]*", sel):
        tok = tok.rstrip(".,")
        if not tok:
            continue
        try:
            if "," in tok and "." in tok:
                out.append((float(tok.replace(".", "").replace(",", ".")), len(tok.split(",")[1])))
            elif "," in tok:
                out.append((float(tok.replace(",", ".")), len(tok.split(",")[1])))
            elif "." in tok:
                out.append((float(tok), len(tok.split(".")[1])))
                if re.match(r"^\d{1,3}(?:\.\d{3})+$", tok):
                    out.append((float(tok.replace(".", "")), 0))
            else:
                out.append((float(tok), 0))
        except ValueError:
            continue
    return out


def cabang(obj, jalur):
    cur = obj
    for b in jalur:
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\[(\d+)\]$", b)
        if m:
            kunci, idx = m.group(1), int(m.group(2))
            if not isinstance(cur, dict) or kunci not in cur:
                return None, False
            cur = cur[kunci]
            if not isinstance(cur, list) or idx >= len(cur):
                return None, False
            cur = cur[idx]
            continue
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
    if kedalaman > 4 or isinstance(o, bool):
        return
    if isinstance(o, (int, float)):
        keluar.append(float(o))
    elif isinstance(o, dict):
        for v in o.values():
            daun(v, keluar, kedalaman + 1)
    elif isinstance(o, list):
        for v in o[:4000]:
            daun(v, keluar, kedalaman + 1)


def cari(bundle, rujukan):
    fname = next((n for n in bundle if n in rujukan), None)
    for tok in TOK.findall(rujukan.replace("`", "")):
        if tok in ("os", "pd", "data") or tok.endswith(".json") or tok.endswith(".py"):
            continue
        jalur = re.findall(r"[A-Za-z_][A-Za-z0-9_]*(?:\[\d+\])?|\d+", tok)
        for n in ([fname] if fname else list(bundle)):
            val, ok = cabang(bundle[n], jalur)
            if ok and val is not None and not isinstance(val, str):
                return n, tok, val
    return None, None, None


def main():
    ring = {}
    for kartu, folder in CARD.items():
        bundle = muat(folder)
        rows = baris(kartu)
        kl, mismatch, tak = Counter(), [], []
        kelas = Counter()
        for sel in rows:
            kode, angka_s, satuan, kelas_src, rujukan, dipakai, status = sel
            kelas[kelas_src] += 1
            angka = kandidat_angka(angka_s)
            if not angka:
                kl["sel_bukan_angka"] += 1
                tak.append((kode, angka_s[:30]))
                continue
            if kelas_src.upper() == "DERIVASI":
                kl["derivasi_tidak_diuji_otomatis"] += 1
                continue
            n, tok, val = cari(bundle, rujukan)
            if val is None:
                kl["tidak_resolve"] += 1
                tak.append((kode, angka_s[:30]))
                continue
            leaves = []
            daun(val, leaves)
            if isinstance(val, bool):
                leaves.append(1.0 if val else 0.0)
            elif isinstance(val, (int, float)):
                leaves.append(float(val))
            cocok = sum(1 for v, dec in angka
                        if any(abs(x - v) <= 0.5 * 10 ** (-dec) + 1e-6 for x in leaves))
            if cocok:
                kl["MATCH" if cocok == len(angka) else "MATCH_sebagian"] += 1
            else:
                kl["MISMATCH"] += 1
                mismatch.append(dict(kode=kode, sel=angka_s[:40], berkas=n, jalur=tok,
                                     daun=leaves[:6], rujukan=rujukan[:90]))
        ring[kartu] = dict(n=len(rows), kelas_hasil=dict(kl), kelas_sumber=dict(kelas),
                           mismatch=mismatch, tidak_resolve=tak[:40])
        print("=" * 76)
        print(kartu, "n", len(rows), "| kelas:", dict(kl), "| sumber:", dict(kelas))
        for m in mismatch[:8]:
            print("   MISMATCH", m)

    # tabel artefak
    art = []
    for kartu, folder in CARD.items():
        for p in sorted((BASE / "scratch/rnd" / folder).glob("*.json*")):
            try:
                if p.suffix == ".jsonl":
                    d = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
                    n = len(d)
                    jenis = "JSONL"
                else:
                    d = json.loads(p.read_text(encoding="utf-8"))
                    n = len(d) if isinstance(d, (list, dict)) else 1
                    jenis = "list" if isinstance(d, list) else "dict"
                art.append(dict(kartu=kartu, berkas=p.name, bytes=p.stat().st_size, buka=True,
                                top=jenis, n_top=n))
            except Exception as e:
                art.append(dict(kartu=kartu, berkas=p.name, bytes=p.stat().st_size, buka=False,
                                error=f"{type(e).__name__}: {e}"))
    (BASE / "scratch/rnd/s5/s5_resolve3.json").write_text(
        json.dumps(dict(ledger=ring, artefak=art), indent=1, ensure_ascii=False), encoding="utf-8")
    print("\nartefak JSON:", len(art), "| gagal buka:", sum(1 for a in art if not a["buka"]))
    print("WROTE scratch/rnd/s5/s5_resolve3.json")


if __name__ == "__main__":
    main()
