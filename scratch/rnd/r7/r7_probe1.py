import pandas as pd, numpy as np, json
df = pd.read_csv("scratch/v9_d1/datasets/hyd_ki.csv.gz")
LABEL_DERIVED = ("y_hyd","y_prev_hyd","valid_prev_hyd","obs_hyd","anom_hyd","lab_ts","lab_kind","feat_ts_max")
feats = [c for c in df.columns if c not in LABEL_DERIVED]
feats = [c for c in feats if pd.api.types.is_numeric_dtype(df[c])]
print("n_cols", len(df.columns), "n_feats", len(feats))
print("FEATS:", feats)
print("ts_bin_in_feats:", "ts_bin" in feats)
print("non_numeric_cols:", [c for c in df.columns if not pd.api.types.is_numeric_dtype(df[c])])
print("--- ts_bin per well ---")
print(df.groupby("well")["ts_bin"].agg(["min","max","count"]).to_string())
# apakah y_prev = label pada t-10 (jendela tidak tumpang tindih) ?
g = df.sort_values(["well","ts_bin"])
for w in [g["well"].unique()[0]]:
    d = g[g["well"]==w]
    y = d["y_hyd"].to_numpy(int); yp = d["y_prev_hyd"].to_numpy(int); ts = d["ts_bin"].to_numpy(int)
    idx = {t:i for i,t in enumerate(ts)}
    sama10 = sum(1 for i,t in enumerate(ts) if (t-10) in idx and y[idx[t-10]]==yp[i])
    sama1 = sum(1 for i,t in enumerate(ts) if (t-1) in idx and y[idx[t-1]]==yp[i])
    print(w, "cocok_yprev_vs_y(t-10):", sama10, " cocok_vs_y(t-1):", sama1, " n:", len(ts))
print("--- bins schema ---")
import glob
b = pd.read_csv(sorted(glob.glob("scratch/v9_d1/bins/*.csv.gz"))[0])
print(sorted(glob.glob("scratch/v9_d1/bins/*.csv.gz")))
print(b.columns.tolist())
print(b.head(3).to_string())

import json as _j
_j.dump({"n_cols": int(df.shape[1]), "n_feats": len(feats), "ts_bin_in_feats": bool("ts_bin" in feats), "n_feats_tanpa_ts_bin": len([c for c in feats if c != "ts_bin"]), "feats": feats}, open("scratch/rnd/r7/r7_probe.json", "w"), indent=2)
print("PROBE JSON WRITTEN")
