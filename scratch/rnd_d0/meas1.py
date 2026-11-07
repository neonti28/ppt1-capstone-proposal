"""RND-D0 measurement 1: engine window datasets + per-well minute bins."""
import json, os, glob
import numpy as np
import pandas as pd

BASE = "/mnt/d/Capstone 1(v2)"
DS = f"{BASE}/scratch/v9_d1/datasets"
BINS = f"{BASE}/scratch/v9_d1/bins"
OUT = os.path.dirname(os.path.abspath(__file__))

ENGINES = ["vib", "ssi", "shk", "stuck_k1", "stuck_k2", "hyd_ki"]
LABEL_SUM = {"vib": "y_vib", "ssi": "y_ssi", "shk": "y_shk",
             "stuck_k1": "y_stuck", "stuck_k2": "y_stuck_onset", "hyd_ki": "y_hyd"}
CHAN_FEAT = ["TQA", "SPPA", "TFLO", "RPM", "SWOB", "HKLD", "ROP", "BPOS", "SPM", "depth", "dbtm"]
KEY_RAW = ["TQA", "SPPA", "TFLO", "RPM", "SWOB", "HKLD", "ROP", "BPOS", "SPM"]

res = {"engines": {}, "bins": {}}

# ---------------- 1. windows per engine ----------------
for e in ENGINES:
    p = f"{DS}/{e}.csv.gz"
    df = pd.read_csv(p, compression="gzip", low_memory=False)
    lab = LABEL_SUM[e]
    per_well = {}
    for w, g in df.groupby("well"):
        n = len(g)
        pos = int((g[lab] == 1).sum())
        per_well[w] = {"n_windows": int(n), "n_pos": pos,
                       "prevalence": (pos / n if n else None)}
    miss_mean = {c: float(df[f"{c}_mean"].isna().mean()) for c in CHAN_FEAT if f"{c}_mean" in df.columns}
    res["engines"][e] = {
        "file": f"scratch/v9_d1/datasets/{e}.csv.gz",
        "n_rows": int(len(df)), "n_cols": int(df.shape[1]),
        "n_wells": int(df["well"].nunique()),
        "wells": sorted(df["well"].unique().tolist()),
        "label_col": lab,
        "n_pos_total": int((df[lab] == 1).sum()),
        "prevalence_total": float((df[lab] == 1).mean()),
        "per_well": per_well,
        "missing_mean_feat": miss_mean,
        "ts_span": [str(pd.to_datetime(df["ts_bin"], unit="s").min()),
                    str(pd.to_datetime(df["ts_bin"], unit="s").max())],
    }
    print(f"[windows] {e}: rows={len(df)} wells={df['well'].nunique()} pos={int((df[lab]==1).sum())} prev={float((df[lab]==1).mean()):.4f}")

# ---------------- 2. bins per well ----------------
def longest_run(mask):
    best = cur = 0
    for v in mask:
        if v:
            cur += 1
            if cur > best:
                best = cur
        else:
            cur = 0
    return best

for p in sorted(glob.glob(f"{BINS}/*.csv.gz")):
    w = os.path.basename(p).replace(".csv.gz", "")
    b = pd.read_csv(p, compression="gzip")
    ts = b["ts_bin"].to_numpy()
    dt = np.diff(ts)
    gaps_gt60 = int((dt > 60).sum())
    gaps_gt300 = int((dt > 300).sum())
    rows = b["rows"].to_numpy()
    run_rows = longest_run(rows > 0)
    run_drill = longest_run(b["rows_drill"].to_numpy() > 0) if "rows_drill" in b.columns else None
    miss = {c: float(b[f"{c}_mean"].isna().mean()) for c in KEY_RAW if f"{c}_mean" in b.columns}
    # raw label channels coverage
    cov = {}
    for nm, cn in [("VIBLAT", "vib_n"), ("SHKRSK", "shk_n"), ("STUCK", "stuck_n"), ("CRPM", "crpm_n")]:
        if cn in b.columns:
            cov[nm] = {"bins_nonzero": int((b[cn] > 0).sum()), "bins_total": int(len(b)),
                       "frac_bins_with_signal": float((b[cn] > 0).mean())}
    res["bins"][w] = {
        "file": f"scratch/v9_d1/bins/{w}.csv.gz",
        "n_bins": int(len(b)),
        "ts_start": str(pd.to_datetime(ts.min(), unit="s")),
        "ts_end": str(pd.to_datetime(ts.max(), unit="s")),
        "span_hours": float((ts.max() - ts.min()) / 3600.0),
        "rows_total": int(rows.sum()),
        "rows_per_min_median": float(np.median(rows)),
        "rows_per_min_mean": float(rows.mean()),
        "rows_per_min_p95": float(np.percentile(rows, 95)),
        "gaps_gt_1min": gaps_gt60,
        "gaps_gt_5min": gaps_gt300,
        "longest_contiguous_bins": int(run_rows),
        "longest_drilling_bins": (int(run_drill) if run_drill is not None else None),
        "miss_minute_bins": miss,
        "label_cov": cov,
    }
    print(f"[bins] {w}: bins={len(b)} rows/min med={np.median(rows):.0f} gaps>1m={gaps_gt60} longest={run_rows}")

with open(f"{OUT}/meas1_windows_bins.json", "w") as fh:
    json.dump(res, fh, indent=1, default=str)
print("WROTE", f"{OUT}/meas1_windows_bins.json")
