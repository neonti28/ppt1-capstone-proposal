"""Probe: apakah mask kategori bekerja seperti dugaan (uji ekspresi s4b)."""
import os
import pandas as pd

ROOT = "/mnt/d/Capstone 1(v2)"
df = pd.read_csv(os.path.join(ROOT, "data/volve/labels_curated_v2.csv"), low_memory=False)
t0 = pd.to_datetime(df["act_start"], errors="coerce", format="ISO8601", utc=True)
t1 = pd.to_datetime(df["act_end"], errors="coerce", format="ISO8601", utc=True)
ok = t0.notna() & t1.notna()
dur_h = (t1 - t0).dt.total_seconds() / 3600.0

m1 = ok & (dur_h >= 0)
print("m1 True:", int(m1.sum()), "dtype:", m1.dtype)
m2 = (df["category"] == "equipment failure")
print("m2 True:", int(m2.sum()), "dtype:", m2.dtype)
m3 = m1 & m2
print("m3 True:", int(m3.sum()))
print("len(df[m3]) =", len(df[m3]))

m4 = m1 & (df["state_detail"] == "equipment failure")
print("m4 (state_detail) True:", int(m4.sum()))

# cek: apakah '&' dengan kolom string memicu broadcast aneh pada pandas 3.1
s = pd.Series(["a", "b", "a"], dtype="str")
print("tes banding:", (s == "a").tolist(), "&", (pd.Series([True, True, False]) & (s == "a")).tolist())
