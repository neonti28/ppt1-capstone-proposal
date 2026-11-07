import os
import pandas as pd

BASE = "/mnt/d/Capstone 1(v2)"
p = os.path.join(BASE, "scratch/v9_d1/datasets/hyd_ki.csv.gz")
df = pd.read_csv(p)
print("shape", df.shape)
print("cols:", list(df.columns))
print()
for c in df.columns:
    if c.startswith("y_") or "prev" in c.lower():
        print(c, df[c].dtype, "nonnull", int(df[c].notna().sum()), "vals", df[c].dropna().unique()[:6])
print()
folds = pd.read_json(os.path.join(BASE, "scratch/v9_d1/lowo_hyd_ki.json"))
print("folds keys", list(folds.columns))
print(folds.head())
