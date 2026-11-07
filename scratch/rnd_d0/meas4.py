"""RND-D0 measurement 4: pit volume dataset (F-9A time log) + GAINLOSSTOT search."""
import json, os, glob
import numpy as np
import pandas as pd

BASE = "/mnt/d/Capstone 1(v2)"
OUT = os.path.dirname(os.path.abspath(__file__))
res = {}

# ---- GAINLOSSTOT presence in any parsed WITSML qc channel list ----
hits = {}
for p in glob.glob(f"{BASE}/data/volve/witsml_parsed/*.qc.json"):
    qc = json.load(open(p))
    ch = qc.get("channels", [])
    h = [c for c in ch if any(k in c.upper() for k in ("GAINLOSSTOT", "PIT", "GAIN", "LOSS"))]
    hits[os.path.basename(p)] = {"n_channels": len(ch), "pit_like": h}
res["qc_pit_like"] = hits
for k, v in hits.items():
    if v["pit_like"]:
        print("[QC]", k, v["pit_like"])
print("[QC] wells scanned:", len(hits))

# ---- F-9A raw time log with MudPit columns (source of hyd K-ii pit) ----
F = "/home/neonti/.hermes/cache/scratch/f9a_time.csv"
if os.path.exists(F):
    cols = pd.read_csv(F, nrows=0).columns.tolist()
    pit_cols = [c for c in cols if "MudPit Volume Average" in c]
    res["f9a_time"] = {"file": F, "size_bytes": os.path.getsize(F), "n_cols": len(cols),
                       "n_pit_cols": len(pit_cols), "pit_cols": pit_cols}
    usec = ["Time s"] + pit_cols
    t_all = []
    for ch in pd.read_csv(F, usecols=usec, chunksize=200000):
        t = pd.to_datetime(ch["Time s"], utc=True, errors="coerce")
        t_all.append(t.dropna().to_numpy(dtype="datetime64[ns]").astype("int64"))
    tt = np.unique(np.concatenate(t_all)) / 1e9
    d = np.diff(tt)
    res["f9a_time"].update({
        "n_time_samples": int(len(tt)),
        "span_hours": float((tt[-1] - tt[0]) / 3600.0),
        "median_dt_s": float(np.median(d)),
        "gaps_gt_60s": int((d > 60).sum()),
        "max_gap_s": float(d.max()),
    })
    print("[PIT]", res["f9a_time"])
else:
    res["f9a_time"] = {"file": F, "exists": False}
    print("[PIT] NOT FOUND", F)

with open(f"{OUT}/meas4_pit.json", "w") as fh:
    json.dump(res, fh, indent=1, default=str)
print("WROTE", f"{OUT}/meas4_pit.json")
