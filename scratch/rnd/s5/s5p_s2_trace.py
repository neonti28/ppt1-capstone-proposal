#!/usr/bin/env python3
"""S5 probe: apakah angka dokumen S2 masih tertelusur setelah artefak dipindah."""
import json
import os

BASE = "/mnt/d/Capstone 1(v2)"
S2 = f"{BASE}/scratch/rnd/s2"
print("--- isi s2 ---")
for f in sorted(os.listdir(S2)):
    p = f"{os.path.join(S2, f)}"
    print(f"{f:28s} {os.path.getsize(p):9d} mtime={os.path.getmtime(p):.0f}")
if os.path.isdir(f"{S2}/bak_gagal"):
    print("--- isi bak_gagal ---")
    for f in sorted(os.listdir(f"{S2}/bak_gagal")):
        p = f"{S2}/bak_gagal/{f}"
        print(f"{f:28s} {os.path.getsize(p):9d}")

doc = [0.4527, 0.6292, 0.6204, 456, 0.2713, 0.0037, 2.5, 0.0715, 0.0109, 210,
       0.0237, 0.1290, 220, 0.0440, 0.2542, 0.0159, 23922, 35906, 5429, 607]


def kump(o, out=None):
    if out is None:
        out = set()
    if isinstance(o, bool):
        return out
    if isinstance(o, (int, float)):
        out.add(float(o))
    elif isinstance(o, dict):
        for v in o.values():
            kump(v, out)
    elif isinstance(o, list):
        for v in o:
            kump(v, out)
    return out


def lapor(path, label):
    if not os.path.isfile(path):
        print(f"{label}: TIDAK ADA")
        return
    o = json.load(open(path, encoding="utf-8"))
    k = kump(o)
    ketemu = [d for d in doc if any(abs(d - v) <= max(1e-4, 0.5 * 10 ** -4) or
                                    (v and abs(abs(v) * 1000 - d) <= 0.01) for v in k)]
    print(f"{label}: dapat {len(ketemu)}/{len(doc)} angka dokumen; kunci={list(o)[:10] if isinstance(o, dict) else type(o).__name__}")
    for key in ("auprc_median", "prev_median", "rows", "wells", "n_pos"):
        if isinstance(o, dict) and key in o:
            print(f"   {key} = {o[key]}")
    if isinstance(o, dict) and "agg" in o:
        for m in ("ml", "hybrid", "stat"):
            if m in o["agg"]:
                a = o["agg"][m]
                print(f"   agg.{m}: precision.median={a.get('precision', {}).get('median')} "
                      f"recall.median={a.get('recall', {}).get('median')} "
                      f"fp.median={a.get('fp', {}).get('median')}")
    return o


for f, lab in ((f"{S2}/bak_gagal/s2_vib.json", "bak_gagal/s2_vib.json"),
               (f"{S2}/bak_gagal/s2_ssi.json", "bak_gagal/s2_ssi.json"),
               (f"{S2}/s2_records_vib.json", "s2_records_vib.json (run baru)")):
    lapor(f, lab)

m = f"{S2}/s2_meta.json"
if os.path.isfile(m):
    print("s2_meta.json:", json.load(open(m, encoding="utf-8")))
