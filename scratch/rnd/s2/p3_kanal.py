#!/usr/bin/env python3
"""Probe kanal dan semantik label vib/ssi.

Pertanyaan yang dijawab:
1. Kolom kanal apa saja yang tersedia (bins dan dataset).
2. Apakah y_prev_<kelas> sama dengan y_<kelas> digeser satu baris per well
   (definisi persistence), atau definisi lain.
3. Kanal mana yang paling terkait label (AUC satu fitur) sebagai petunjuk
   kanal untuk gerbang rule. Ini hanya petunjuk, bukan model.
"""
import json

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

BASE = "/mnt/d/Capstone 1(v2)"
DSD = f"{BASE}/scratch/v9_d1/datasets"
BINSD = f"{BASE}/scratch/v9_d1/bins"
OUT = f"{BASE}/scratch/rnd/s2"

hasil = {}
for nama, kol in (("vib", "y_vib"), ("ssi", "y_ssi")):
    df = pd.read_csv(f"{DSD}/{nama}.csv.gz").sort_values(["well", "ts_bin"]).reset_index(drop=True)
    d0 = df[df["well"] == sorted(df["well"].unique())[0]]
    bins = pd.read_csv(f"{BINSD}/{d0['well'].iloc[0]}.csv.gz")
    # kanal di bins: pola <CHAN>_mean
    chans = sorted({c[:-5] for c in bins.columns if c.endswith("_mean")})
    # persistence: y_prev == y.shift(1) per well?
    prev_col = "y_prev_" + nama
    cek = {}
    if prev_col in df.columns:
        geser = df.groupby("well")[kol].shift(1)
        sama = (df[prev_col].fillna(-1) == geser.fillna(-1))
        cek = {"n": int(len(df)), "cocok": int(sama.sum()),
               "fraksi_cocok": round(float(sama.mean()), 6),
               "prev_sum": int(df[prev_col].fillna(0).sum()),
               "y_sum": int(df[kol].sum())}
    # AUC satu fitur untuk tiap kolom numerik non-label
    lab_like = [c for c in df.columns if c.startswith(("y_", "obs_", "anom_", "valid_prev_", "lab_"))]
    meta = ["well", "ts_bin", "feat_ts_max", "lab_ts", "lab_kind", "tool", "run", "file", "start_sample"]
    feats = [c for c in df.columns
             if c not in lab_like and c not in meta and pd.api.types.is_numeric_dtype(df[c])]
    y = df[kol].astype(int).to_numpy()
    auc = {}
    for c in feats:
        x = pd.to_numeric(df[c], errors="coerce").to_numpy(float)
        m = np.isfinite(x)
        if m.sum() < 100 or len(np.unique(y[m])) < 2:
            continue
        try:
            auc[c] = round(float(roc_auc_score(y[m], x[m])), 4)
        except Exception:
            pass
    top = sorted(auc.items(), key=lambda kv: -abs(kv[1] - 0.5))[:12]
    hasil[nama] = {"kanal_bins": chans, "kolom_bins": list(bins.columns)[:40],
                   "n_kolom_bins": len(bins.columns),
                   "persistence": cek,
                   "auc_top": [{"kolom": k, "auc": v} for k, v in top],
                   "n_fitur": len(feats)}
    print(f"== {nama}: kanal bins = {chans}", flush=True)
    print("   persistence:", cek, flush=True)
    print("   AUC top:", top, flush=True)

with open(f"{OUT}/p3_kanal.json", "w") as f:
    json.dump(hasil, f, indent=1)
print("ditulis:", f"{OUT}/p3_kanal.json")
