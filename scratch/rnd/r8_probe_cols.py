import gzip, json, os
import pandas as pd

BASE = "/mnt/d/Capstone 1(v2)"
out = {}
for c in ["hyd_ki", "shk", "stuck_k1", "stuck_k2", "ssi", "vib"]:
    p = f"{BASE}/scratch/v9_d1/datasets/{c}.csv.gz"
    df = pd.read_csv(p, nrows=5)
    n = sum(1 for _ in gzip.open(p, "rt")) - 1
    out[c] = dict(rows=int(n), cols=len(df.columns), columns=list(df.columns))
    print(c, "rows", n, "cols", len(df.columns))
    print("   cols:", list(df.columns))

tw = f"{BASE}/scratch/v6_e1/toolwear_windows.csv"
if os.path.exists(tw):
    d = pd.read_csv(tw)
    out["toolwear_windows"] = dict(rows=len(d), cols=len(d.columns), columns=list(d.columns))
    print("toolwear_windows rows", len(d), "cols", list(d.columns))
    print(d.head(3).to_string())

json.dump(out, open(f"{BASE}/scratch/rnd/r8_probe_cols.json", "w"), indent=1)
