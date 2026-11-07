#!/usr/bin/env python3
"""S5 probe penutup: rekap rerun S1, sisa anomali ledger, keberadaan skrip rujukan."""
import json
import os
import re

BASE = "/mnt/d/Capstone 1(v2)"

r = json.load(open(f"{BASE}/scratch/rnd/s5/s5_rerun.json", encoding="utf-8"))
print("== s5_rerun.json kunci:", list(r))
for k, v in r.items():
    if isinstance(v, dict):
        kecil = {kk: vv for kk, vv in list(v.items())[:8] if not isinstance(vv, (list, dict))}
        print(f" {k}: {json.dumps(kecil, ensure_ascii=False)[:300]}")
    elif isinstance(v, list):
        print(f" {k}[{len(v)}]: {json.dumps(v[:3], ensure_ascii=False)[:300]}")
    else:
        print(f" {k} = {str(v)[:160]}")

n = json.load(open(f"{BASE}/scratch/rnd/s5/s5_negative.json", encoding="utf-8"))
print("\n== s5_negative.json:", json.dumps({k: n[k] for k in list(n)[:6]}, ensure_ascii=False)[:400])

l = json.load(open(f"{BASE}/scratch/rnd/s5/s5_ledger.json", encoding="utf-8"))
d = l["per_kartu"]["S4"]
ids = [int(b["id"].split("-")[1]) for b in d["baris"]]
print("\n== S4 id gap:", [(a, b) for a, b in zip(ids, ids[1:]) if b != a + 1])
print("== S4 tanpa path/berkas:",
      [b["id"] for b in d["baris"] if b["hasil"] in ("TANPA_PATH", "TANPA_BERKAS")][:15])

for f in ("scratch/rnd/s4/p_remark_variants.py", "scratch/rnd/s4/p_rows.py",
          "scratch/rnd/s4/p_linecheck.py", "scratch/rnd/s4/s4i_token_scan.py"):
    print(f"{f}: {'ADA' if os.path.isfile(f'{BASE}/{f}') else 'TIDAK ADA'}")

h = open(f"{BASE}/code/rnd_hybrid_harness.py", encoding="utf-8").read()
m = re.search(r"H_GRID\s*=\s*([^\n]+)", h)
print("\nH_GRID:", m.group(1) if m else "tidak ditemukan")
for nm, pola in (("ALPHA_BUDGET", r"ALPHA_BUDGET\s*=\s*([^\n]+)"),
                 ("FAR_MAKS", r"FAR_MAKS\s*=\s*([^\n]+)"),
                 ("CAKUPAN_MIN", r"CAKUPAN_MIN\s*=\s*([^\n]+)")):
    mm = re.search(pola, h)
    print(f"{nm}:", mm.group(1) if mm else "tidak ditemukan")

# berkas 645763 byte: dibatasi pada empat direktori, walk penuh terlalu lambat
for sub in ("external/dbx_volume", "", "witsml_csv", "labels"):
    folder = os.path.join(BASE, "data/volve", sub) if sub else os.path.join(BASE, "data/volve")
    if not os.path.isdir(folder):
        continue
    for f in os.listdir(folder):
        p = os.path.join(folder, f)
        if os.path.isfile(p) and os.path.getsize(p) == 645763:
            print("645763 byte ->", p.replace(BASE + "/", ""))
