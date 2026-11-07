"""Probe struktur ddr.parquet (Daily Drilling Report, Volve). READ-ONLY."""
import os, json
import pandas as pd

ROOT = "/mnt/d/Capstone 1(v2)"
P = os.path.join(ROOT, "data/volve/ddr.parquet")
print("FILE", P, "bytes", os.path.getsize(P))
df = pd.read_parquet(P)
print("SHAPE", df.shape)
print("COLS", list(df.columns))
print("--- dtypes ---")
print(df.dtypes.to_string())
print("--- non-null counts ---")
print(df.notna().sum().to_string())
print("--- head 2 (kolom teks dipotong 200 char) ---")
for i in range(min(2, len(df))):
    r = df.iloc[i]
    print("ROW", i)
    for c in df.columns:
        v = r[c]
        s = str(v)
        if len(s) > 200:
            s = s[:200] + "..."
        print("   ", c, "=", s)
