#!/usr/bin/env python3
"""Probe data vib dan ssi: kolom, label, jumlah positif, jumlah well, fold."""
import json

import pandas as pd

BASE = "/mnt/d/Capstone 1(v2)"
DSD = f"{BASE}/scratch/v9_d1/datasets"

out = {}
for name in ("vib", "ssi"):
    df = pd.read_csv(f"{DSD}/{name}.csv.gz")
    lab = [c for c in df.columns if c.startswith(("y_", "obs_", "anom_", "valid_prev_", "lab_"))]
    ycols = [c for c in lab if c.startswith("y_")]
    wells = df.groupby("well").size().to_dict()
    # rentang waktu per well
    rentang = {}
    for w, d in df.groupby("well"):
        ts = d["ts_bin"].to_numpy()
        rentang[w] = dict(n=int(len(ts)), menit_kalender=int(ts.max() - ts.min() + 1),
                          ts_min=int(ts.min()), ts_max=int(ts.max()))
    fold = json.load(open(f"{BASE}/scratch/v9_d1/lowo_{name}.json"))
    out[name] = dict(shape=list(df.shape), kolom=list(df.columns), label_cols=lab,
                     y_cols=ycols,
                     y_pos={c: int(df[c].sum()) for c in ycols if df[c].dtype != object},
                     y_prev={c: round(float(pd.to_numeric(df[c], errors="coerce").mean()), 6) for c in ycols},
                     per_well={c: df.groupby("well")[c].sum().astype(int).to_dict() for c in ycols},
                     wells=wells, rentang=rentang,
                     fold_keys=list(fold.keys()), n_fold=len(fold["folds"]),
                     folds=fold["folds"])
print(json.dumps(out, indent=1, default=str))
