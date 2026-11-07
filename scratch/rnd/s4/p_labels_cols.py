"""Probe verifikasi: nilai unik kolom category/state_detail labels_curated_v2."""
import os
import pandas as pd

ROOT = "/mnt/d/Capstone 1(v2)"
SRC = os.path.join(ROOT, "data/volve/labels_curated_v2.csv")
df = pd.read_csv(SRC, low_memory=False)
print("SHAPE", df.shape)
print("KOLOM", list(df.columns))
for col in ["category", "state_detail"]:
    print("---", col, "---")
    print(df[col].value_counts(dropna=False).to_string())
print("n category == 'equipment failure':", int((df["category"] == "equipment failure").sum()))
print("dtype category:", df["category"].dtype)
print("dtype state_detail:", df["state_detail"].dtype)
