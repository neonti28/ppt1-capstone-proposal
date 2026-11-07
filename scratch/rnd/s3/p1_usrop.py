#!/usr/bin/env python3
"""Probe struktur USROP_labeled.csv (bit_wear K-1) tanpa asumsi."""
import pandas as pd

P = "/mnt/d/Capstone 1(v2)/data/USROP_labeled.csv"
d = pd.read_csv(P)
print("shape", d.shape)
print("cols", list(d.columns))
print("--- dtypes ---")
print(d.dtypes.to_string())
print("--- nunique ---")
print(d.nunique().to_string())
print("--- head 2 ---")
print(d.head(2).to_string())
print("--- label counts (kolom yang mengandung 'label') ---")
for c in d.columns:
    if "label" in c.lower() or c.lower().startswith("y"):
        print(c, d[c].value_counts(dropna=False).to_dict())
