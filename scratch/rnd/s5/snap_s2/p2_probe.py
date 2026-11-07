#!/usr/bin/env python3
"""Probe struktur dataset vib dan ssi: kolom, label, positif per well, fold, satuan ts.

Tidak menyimpulkan apa pun; hanya mengumpulkan fakta mentah untuk kartu S2.
"""
import json
import sys

import numpy as np
import pandas as pd

BASE = "/mnt/d/Capstone 1(v2)"
DSD = f"{BASE}/scratch/v9_d1/datasets"
LOWOD = f"{BASE}/scratch/v9_d1"
OUT = f"{BASE}/scratch/rnd/s2"

hasil = {}
for nama in ("vib", "ssi"):
    df = pd.read_csv(f"{DSD}/{nama}.csv.gz")
    lab = [c for c in df.columns if c.startswith(("y_", "obs_", "anom_", "valid_prev_", "lab_"))]
    ycols = [c for c in lab if c.startswith("y_")]
    meta = [c for c in ("well", "ts_bin", "feat_ts_max", "lab_ts", "lab_kind", "tool", "run",
                        "file", "start_sample") if c in df.columns]
    feat = [c for c in df.columns
            if c not in lab and c not in meta and pd.api.types.is_numeric_dtype(df[c])]
    per_well = {}
    for w, d in df.groupby("well"):
        ts = d["ts_bin"].to_numpy(dtype=np.int64)
        rec = {"n": int(len(d)), "ts_min": int(ts.min()), "ts_max": int(ts.max()),
               "menit_kalender": int(ts.max() - ts.min() + 1),
               "cakupan": round(len(d) / (ts.max() - ts.min() + 1), 4),
               "delta_ts_modus": int(pd.Series(np.diff(np.sort(ts))).mode().iloc[0]) if len(ts) > 1 else None}
        for c in ycols:
            rec[c] = int(pd.to_numeric(d[c], errors="coerce").fillna(0).sum())
        per_well[w] = rec
    fold = json.load(open(f"{LOWOD}/lowo_{nama}.json"))
    hasil[nama] = {
        "path": f"{DSD}/{nama}.csv.gz",
        "shape": list(df.shape),
        "kolom": list(df.columns),
        "label_cols": lab,
        "y_cols": ycols,
        "meta_cols": meta,
        "fitur_kandidat": feat,
        "n_fitur": len(feat),
        "dtype_ts_bin": str(df["ts_bin"].dtype),
        "wells": sorted(df["well"].unique().tolist()),
        "n_well": int(df["well"].nunique()),
        "per_well": per_well,
        "fold_n": len(fold["folds"]),
        "folds": fold["folds"],
    }
    print(f"{nama}: shape={df.shape} n_well={df['well'].nunique()} "
          f"y_cols={ycols} n_fitur={len(feat)} folds={len(fold['folds'])}", flush=True)
    for w, r in per_well.items():
        print("   ", w, {k: r[k] for k in r if k.startswith("y_") or k in ("n", "cakupan", "delta_ts_modus")},
              flush=True)

with open(f"{OUT}/p2_probe.json", "w") as f:
    json.dump(hasil, f, indent=1)
print("ditulis:", f"{OUT}/p2_probe.json")
