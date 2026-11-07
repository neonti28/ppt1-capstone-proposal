#!/usr/bin/env python3
"""Probe bins: kolom SPPA/TFLO + struktur hid per well (untuk finalis CUSUM)."""
import pandas as pd, json

BASE = "/mnt/d/Capstone 1(v2)"
p = f"{BASE}/scratch/v9_d1/bins/F-10.csv.gz"
b = pd.read_csv(p)
print("bins cols:", list(b.columns))
print("shape", b.shape)
print(b[["ts_bin"]].describe() if "ts_bin" in b else "no ts_bin")
for c in ("SPPA_mean", "TFLO_mean"):
    if c in b.columns:
        print(c, "nan", int(b[c].isna().sum()), "min", float(b[c].min()), "max", float(b[c].max()))

# cek lowo file struktur
lowo = json.load(open(f"{BASE}/scratch/v9_d1/lowo_hyd_ki.json"))
print("lowo type:", type(lowo).__name__)
s = json.dumps(lowo)[:600]
print("lowo head:", s)

# cek hasil stat 01 yang ada (baseline per fold)
r = json.load(open(f"{BASE}/scratch/v9_e_stat/v9_e_stat_01_hyd_ki_RESULTS.json"))
print("stat01 keys:", list(r.keys())[:25])
