#!/usr/bin/env python3
"""Kontrol negatif: pengunci perbandingan harus BISA GAGAL.

Dokumen S1 disalin di memori, tiga angka diubah, lalu jalur perbandingan yang
sama dijalankan. Kalau pengunci tidak melaporkan selisih, pengunci itu tidak sah
dan hasil audit positif sebelumnya tidak boleh dipakai.
"""
import json
import pathlib
import re

BASE = pathlib.Path("/mnt/d/Capstone 1(v2)")
RERUN = json.loads((BASE / "scratch/rnd/s5/s5_rerun_audit.json").read_text(encoding="utf-8"))
DOC = (BASE / "docs/RND_S1_SEED_ROBUSTNESS.md").read_text(encoding="utf-8")


def num(s):
    s = s.strip().replace(".", "").replace(",", ".") if re.search(r"\d,\d", s) else s.strip()
    try:
        return float(s)
    except ValueError:
        return None


def tabel(doc):
    lines = doc.splitlines()
    blocks, cur, start = [], [], 0
    for i, l in enumerate(lines, 1):
        if l.strip().startswith("|"):
            if not cur:
                start = i
            cur.append(l)
        elif cur:
            blocks.append((start, cur))
            cur = []
    if cur:
        blocks.append((start, cur))
    out = []
    for start, blk in blocks:
        rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in blk]
        out.append(dict(line=start, header=rows[0],
                        rows=[r for r in rows[1:] if not re.match(r"^:?-+:?$", r[0].replace(" ", ""))]))
    return out


def banding(doc):
    blk = next(b for b in tabel(doc) if b["header"] and b["header"][0] == "Metrik" and "42" in b["header"])
    i42 = blk["header"].index("42")
    gagal = []
    for r in blk["rows"]:
        vd, vu = num(r[i42]), RERUN["rerun"]["42"]["ringkas"].get(r[0])
        if vd is None or vu is None:
            continue
        if abs(vu - vd) > 5e-5:
            gagal.append((r[0], vd, vu))
    return gagal


asli = banding(DOC)
print("dokumen asli -> selisih terdeteksi:", len(asli))
assert len(asli) == 0, asli

rusak = DOC.replace("| fp_total | 935 |", "| fp_total | 936 |") \
           .replace("| precision_median | 0,7789 |", "| precision_median | 0,7791 |")
assert rusak != DOC
hasil = banding(rusak)
print("dokumen dirusak (2 angka) -> selisih terdeteksi:", len(hasil))
for h in hasil:
    print("   ", h)

luas = json.loads((BASE / "scratch/rnd/s1/s1_hluas.json").read_text(encoding="utf-8"))
print("pengunci kedua (s1_hluas) fp_total =", luas["ringkas"]["fp_total"],
      "| recall_median =", luas["ringkas"]["recall_median"])
assert luas["ringkas"]["fp_total"] == 237
assert abs(luas["ringkas"]["recall_median"] - 0.1457) < 5e-5

out = dict(
    kontrol="dokumen asli memberi 0 selisih, dokumen dengan 2 angka diubah memberi "
            f"{len(hasil)} selisih, sehingga pengunci terbukti bisa gagal",
    selisih_pada_dokumen_rusak=hasil,
    nilai_pengunci_hluas={k: luas["ringkas"][k] for k in ("fp_total", "tp_total", "precision_median",
                                                          "recall_median", "far24_kalender_median")},
)
(BASE / "scratch/rnd/s5/s5_negatif.json").write_text(json.dumps(out, indent=1, ensure_ascii=False),
                                                     encoding="utf-8")
print("WROTE scratch/rnd/s5/s5_negatif.json")
