"""Probe isi kolom array-of-dict ddr.parquet. READ-ONLY."""
import os, json
import numpy as np
import pandas as pd

ROOT = "/mnt/d/Capstone 1(v2)"
df = pd.read_parquet(os.path.join(ROOT, "data/volve/ddr.parquet"))

def as_list(obj):
    if obj is None:
        return []
    if isinstance(obj, np.ndarray):
        return list(obj)
    if isinstance(obj, (list, tuple)):
        return list(obj)
    if isinstance(obj, dict):
        return [obj]
    return []

for col in df.columns:
    v0 = df[col].iloc[0]
    print(f"COL {col}: type={type(v0).__name__}")

print()
for col in ["activity", "statusInfo", "fluid", "wellboreInfo", "lithShowInfo", "surveyStation", "porePressure"]:
    ks = set()
    tot = 0
    rows_nonempty = 0
    for v in df[col]:
        items = as_list(v)
        tot += len(items)
        if items:
            rows_nonempty += 1
        for it in items:
            if isinstance(it, dict):
                ks.update(it.keys())
    print(f"COL {col}: rows_nonempty={rows_nonempty} total_records={tot}")
    print("  keys:", sorted(ks))

print("\n=== contoh activity lengkap (3 record) ===")
shown = 0
for idx, v in df["activity"].items():
    items = as_list(v)
    if items:
        print("row", idx, "docName", df.at[idx, "docName"], "n_act", len(items))
        for a in items[:3]:
            print(json.dumps({k: str(x)[:200] for k, x in a.items()}, ensure_ascii=False, indent=2))
        shown += 1
    if shown >= 2:
        break

print("\n=== contoh statusInfo ===")
for idx, v in df["statusInfo"].items():
    items = as_list(v)
    if items:
        print("row", idx, "docName", df.at[idx, "docName"])
        print(json.dumps({k: str(x)[:150] for k, x in items[0].items()}, ensure_ascii=False, indent=2))
        break
