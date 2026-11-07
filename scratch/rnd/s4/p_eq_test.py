"""Probe: uji baris eq dari s4b secara terpisah untuk menemukan sebab n=884."""
import os
import pandas as pd

ROOT = "/mnt/d/Capstone 1(v2)"
df = pd.read_csv(os.path.join(ROOT, "data/volve/labels_curated_v2.csv"), low_memory=False)
t0 = pd.to_datetime(df["act_start"], errors="coerce", format="ISO8601", utc=True)
t1 = pd.to_datetime(df["act_end"], errors="coerce", format="ISO8601", utc=True)
ok = t0.notna() & t1.notna()
dur_h = (t1 - t0).dt.total_seconds() / 3600.0
d = dur_h[ok & (dur_h >= 0)]

eq = df[ok & (dur_h >= 0) & (df["category"] == "equipment failure")].assign(_d=d)
print("type eq:", type(eq).__name__)
print("len eq:", len(eq))
print("shape eq:", getattr(eq, "shape", None))
print("kolom eq:", list(getattr(eq, "columns", []))[:8])
print("index eq head:", list(eq.index[:5]))
if hasattr(eq, "groupby"):
    g = eq.groupby("wellbore")
    print("n grup wellbore:", len(g))
    print("ngroups:", getattr(g, "ngroups", "n/a"))
    print("eq['wellbore'].isna().sum():", int(eq["wellbore"].isna().sum()) if "wellbore" in eq.columns else "no col")
