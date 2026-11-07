import json, os, sys
import pandas as pd, numpy as np
BASE="/mnt/d/Capstone 1(v2)"
DS=f"{BASE}/scratch/v9_d1/datasets"
def labcols(df):
    return [c for c in df.columns if c.startswith(("y_","valid_","obs_","anom_"))]
for name in ["hyd_ki","shk","ssi","vib","stuck_k2"]:
    df=pd.read_csv(f"{DS}/{name}.csv.gz", low_memory=False)
    print("="*20, name, "cols_meta_ok", df.shape)
    lc=[c for c in df.columns if c.startswith("y_") and df[c].nunique(dropna=True)<=2]
    print(" y cols:", lc[:5])
    y = lc[0] if lc else None
    if y:
        g = df.groupby("well")[y].agg(["size","sum","mean"])
        print(g.to_string())
        print(" total pos:", int(df[y].sum()), "rows", len(df), "wells", df["well"].nunique())
        # positives per well <30
        print(" wells_pos<30:", [w for w in g.index if g.loc[w,"sum"]<30])
print("="*20,"toolwear")
p=f"{BASE}/scratch/v6_e1/toolwear_windows.csv"
if os.path.exists(p):
    t=pd.read_csv(p, low_memory=False)
    print(t.shape, [c for c in t.columns][:12])
    print(t.head(3).to_string()[:600])
else:
    print("MISSING", p)
