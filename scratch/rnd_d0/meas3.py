"""RND-D0 measurement 3: external datasets (USROP, tool wear, Volve pit/GAINLOSSTOT)."""
import json, os, glob
import numpy as np
import pandas as pd

BASE = "/mnt/d/Capstone 1(v2)"
OUT = os.path.dirname(os.path.abspath(__file__))
res = {}

# ---- USROP labeled ----
u = pd.read_csv(f"{BASE}/data/USROP_labeled.csv", low_memory=False)
res["usrop_labeled"] = {
    "file": "data/USROP_labeled.csv",
    "n_rows": int(len(u)),
    "n_cols": int(u.shape[1]),
    "columns": u.columns.tolist(),
    "n_wells": int(u["well"].nunique()),
    "label_value_counts": {str(k): int(v) for k, v in u["label"].value_counts().items()},
    "high_MSE_rows": int((u["label"] == "high_MSE_bit_wear").sum()),
    "high_MSE_frac": float((u["label"] == "high_MSE_bit_wear").mean()),
    "MSE_notnull": int(u["MSE"].notna().sum()) if "MSE" in u.columns else None,
    "per_well": {str(w): {"n": int(len(g)), "high_MSE": int((g["label"] == "high_MSE_bit_wear").sum())}
                 for w, g in u.groupby("well")},
}
print("[USROP]", res["usrop_labeled"]["n_rows"], "rows |", res["usrop_labeled"]["label_value_counts"])

# ---- tool wear windows ----
tw = pd.read_csv(f"{BASE}/scratch/v6_e1/toolwear_windows.csv")
feat = [c for c in tw.columns if c not in ("tool", "run", "file", "start_sample", "y")]
res["toolwear"] = {
    "file": "scratch/v6_e1/toolwear_windows.csv",
    "n_rows": int(len(tw)), "n_cols": int(tw.shape[1]),
    "n_features": len(feat),
    "feature_names": feat,
    "n_tools": int(tw["tool"].nunique()), "tools": sorted(tw["tool"].astype(str).unique().tolist()),
    "n_runs": int(tw["run"].nunique()) if "run" in tw.columns else None,
    "y_value_counts": {str(k): int(v) for k, v in tw["y"].value_counts().items()},
    "per_tool": {str(t): int(len(g)) for t, g in tw.groupby("tool")},
}
print("[TOOLWEAR]", res["toolwear"]["n_rows"], "rows |", res["toolwear"]["n_features"], "fitur |",
      res["toolwear"]["n_tools"], "alat |", res["toolwear"]["y_value_counts"])

# ---- Volve pit / GAINLOSSTOT ----
pit = {}
for p in sorted(glob.glob(f"{BASE}/data/volve/witsml_parsed/*.csv")):
    with open(p, "r", errors="replace") as fh:
        cols = fh.readline().strip().split(",")
    hits = [c for c in cols if any(k in c.upper() for k in ("PIT", "GAIN", "LOSS"))]
    pit[os.path.basename(p)] = hits
res["volve_pit_channels"] = pit
print("[VOLVE PIT/GAIN/LOSS]", {k: v for k, v in pit.items() if v})

# externally sourced pit/flow files
ext = {}
for p in glob.glob(f"{BASE}/data/volve/external/**/*", recursive=True):
    if os.path.isfile(p):
        ext[p.replace(BASE + "/", "")] = os.path.getsize(p)
res["volve_external_files"] = dict(sorted(ext.items(), key=lambda x: -x[1])[:40])
print("[VOLVE EXT FILES]", len(ext))

# DDR parquet columns (daily drilling report: pit gain/loss often recorded here)
try:
    ddr = pd.read_parquet(f"{BASE}/data/volve/ddr.parquet")
    pit_cols = [c for c in ddr.columns if any(k in str(c).upper() for k in ("PIT", "GAIN", "LOSS", "FLOW"))]
    res["ddr_parquet"] = {"file": "data/volve/ddr.parquet", "n_rows": int(len(ddr)),
                          "n_cols": int(ddr.shape[1]), "pit_like_cols": pit_cols,
                          "cols_sample": [str(c) for c in ddr.columns[:60]]}
    print("[DDR]", len(ddr), "rows; pit-like cols:", pit_cols)
except Exception as e:
    res["ddr_parquet"] = {"error": str(e)}
    print("[DDR] ERROR", e)

# Volve data village share inventory
try:
    vdv = []
    for p in glob.glob(f"{BASE}/Volve_Data_Village.share/**/*", recursive=True):
        if os.path.isfile(p):
            vdv.append((p.replace(BASE + "/", ""), os.path.getsize(p)))
    vdv.sort(key=lambda x: -x[1])
    res["volve_share_top"] = vdv[:40]
    res["volve_share_n_files"] = len(vdv)
    print("[VDV]", len(vdv), "files; top:", [v[0] for v in vdv[:8]])
except Exception as e:
    res["volve_share_error"] = str(e)

with open(f"{OUT}/meas3_external.json", "w") as fh:
    json.dump(res, fh, indent=1, default=str)
print("WROTE", f"{OUT}/meas3_external.json")
