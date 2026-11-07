#!/usr/bin/env python3
"""RND-E0 probe 01 — inventaris kolom dataset + uji kolom mana yang masuk fitur.

Tujuan: membuktikan kolom mana yang lolos `feature_cols()` di
code/v9_i1_pipeline.py:302-304 sehingga bisa dipakai RF.
Tidak mengubah data apa pun; hanya baca.
"""
from __future__ import annotations

import json
import os

import pandas as pd

BASE = "/mnt/d/Capstone 1(v2)"
DS = f"{BASE}/scratch/v9_d1/datasets"
OUT = f"{BASE}/scratch/rnd_e0"
META_COLS = ("well", "ts_bin", "feat_ts_max", "lab_ts", "lab_kind")
LABEL_PREFIXES = ("y_", "valid_", "obs_", "anom_")


def feature_cols(df):
    return [c for c in df.columns
            if c not in META_COLS and not c.startswith(LABEL_PREFIXES)]


res = {}
for key in ["vib", "ssi", "shk", "stuck_k1", "stuck_k2", "hyd_ki"]:
    p = f"{DS}/{key}.csv.gz"
    d = pd.read_csv(p, nrows=200)
    feats = feature_cols(d)
    leak_like = [c for c in feats if c.startswith(("ssi_val", "nobs_"))]
    res[key] = {
        "n_kolom": len(d.columns),
        "kolom": list(d.columns),
        "n_fitur_feature_cols": len(feats),
        "fitur": feats,
        "kolom_mencurigakan_lolos_filter": leak_like,
    }

os.makedirs(OUT, exist_ok=True)
json.dump(res, open(f"{OUT}/probe01_kolom.json", "w"), indent=1, ensure_ascii=False)
for k, v in res.items():
    print(f"== {k}: {v['n_kolom']} kolom | feature_cols()={v['n_fitur_feature_cols']}")
    print(f"   mencurigakan lolos filter: {v['kolom_mencurigakan_lolos_filter']}")
print("tulis:", f"{OUT}/probe01_kolom.json")
