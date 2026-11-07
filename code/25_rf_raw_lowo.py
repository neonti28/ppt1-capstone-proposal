#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
code/25_rf_raw_lowo.py — RF fitur baris-saja (last_*) di LOWO + banding canary MD (t_e7e9bd6d)

Pertanyaan: apakah RF dengan 12 nilai sensor baris saat ini (tanpa agregasi window 10 m,
varian terkuat di diagnostik D2 temporal: PR-AUC 0,194) mengalahkan canary "hanya-MD"
(D4: macro PR-AUC LOWO 0,2265) di Leave-One-Well-Out?

Output: docs/V2_ML_RAW_LOWO.json + stdout.
"""

from __future__ import annotations

import json
import sys
import time
import traceback
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (average_precision_score, roc_auc_score, precision_score,
                             recall_score, f1_score, confusion_matrix, precision_recall_curve)

BASE = Path(__file__).resolve().parents[1]
DS_PATH = BASE / "data" / "predictive" / "dataset_prediktif.csv"
OUT_JSON = BASE / "docs" / "V2_ML_RAW_LOWO.json"
RF_PARAMS = dict(n_estimators=300, class_weight="balanced", min_samples_leaf=2,
                 n_jobs=-1, random_state=42)


def tune_thr(y, s):
    p, r, t = precision_recall_curve(y, s)
    f1 = np.where((p[:-1] + r[:-1]) > 0, 2 * p[:-1] * r[:-1] / np.maximum(p[:-1] + r[:-1], 1e-12), 0.0)
    if f1.size == 0:
        return float(np.quantile(s, 0.95))
    return float(t[f1 >= f1.max() - 1e-12].max())


def main() -> None:
    t0 = time.time()
    print("=" * 78, flush=True)
    print("25_rf_raw_lowo.py — RF fitur baris-saja di LOWO", flush=True)
    print("=" * 78, flush=True)
    ds = pd.read_csv(DS_PATH, low_memory=False)
    raw_feats = [c for c in ds.columns if c.startswith("last_")]
    y = ds["y_10"].to_numpy(int)
    wells = ds["well"].to_numpy()
    ds["ts"] = pd.to_datetime(ds["est_timestamp"], utc=True, errors="coerce")
    ts_np = ds["ts"].dt.tz_convert("UTC").dt.tz_localize(None).to_numpy(dtype="datetime64[ns]")
    X = ds[raw_feats].to_numpy(float)
    print(f"fitur baris-saja ({len(raw_feats)}): {raw_feats}", flush=True)

    folds, pool = {}, {"y": [], "score": [], "pred": []}
    for w in sorted(set(wells)):
        te = np.flatnonzero(wells == w)
        rest = np.flatnonzero(wells != w)
        rest = rest[np.argsort(ts_np[rest], kind="stable")]
        n_va = int(0.15 * len(rest))
        va, tr = rest[-n_va:], rest[:-n_va]
        rf = RandomForestClassifier(**RF_PARAMS)
        rf.fit(X[tr], y[tr])
        s_va = rf.predict_proba(X[va])[:, 1]
        s_te = rf.predict_proba(X[te])[:, 1]
        thr = tune_thr(y[va], s_va)
        pred = (s_te >= thr).astype(int)
        yw = y[te]
        if len(np.unique(yw)) < 2:
            folds[w] = {"n": int(len(te)), "note": "tanpa positif di test"}
            print(f"    {w}: tanpa positif", flush=True)
            continue
        tn, fp, fn, tp = confusion_matrix(yw, pred, labels=[0, 1]).ravel()
        m = {"n": int(len(te)), "n_pos": int(yw.sum()),
             "prev": round(float(yw.mean()), 4),
             "pr_auc": round(float(average_precision_score(yw, s_te)), 4),
             "roc_auc": round(float(roc_auc_score(yw, s_te)), 4),
             "precision": round(float(precision_score(yw, pred, zero_division=0)), 4),
             "recall": round(float(recall_score(yw, pred, zero_division=0)), 4),
             "f1": round(float(f1_score(yw, pred, zero_division=0)), 4),
             "tp": int(tp), "fp": int(fp), "fn": int(fn), "tn": int(tn),
             "lift_pr_auc_over_prev": round(float(average_precision_score(yw, s_te)) / max(yw.mean(), 1e-9), 3)}
        folds[w] = m
        pool["y"].append(yw); pool["score"].append(s_te); pool["pred"].append(pred)
        print(f"    {w:30s} n={m['n']:6d} prev={m['prev']:.4f} PR-AUC={m['pr_auc']:.4f} "
              f"(lift {m['lift_pr_auc_over_prev']}) ROC={m['roc_auc']:.3f} "
              f"P={m['precision']:.3f} R={m['recall']:.3f} F1={m['f1']:.3f}", flush=True)

    yP = np.concatenate(pool["y"]); sP = np.concatenate(pool["score"]); pP = np.concatenate(pool["pred"])
    tn, fp, fn, tp = confusion_matrix(yP, pP, labels=[0, 1]).ravel()
    pooled = {"n": int(len(yP)), "prev": round(float(yP.mean()), 4),
              "pr_auc": round(float(average_precision_score(yP, sP)), 4),
              "roc_auc": round(float(roc_auc_score(yP, sP)), 4),
              "precision": round(float(precision_score(yP, pP, zero_division=0)), 4),
              "recall": round(float(recall_score(yP, pP, zero_division=0)), 4),
              "f1": round(float(f1_score(yP, pP, zero_division=0)), 4),
              "tp": int(tp), "fp": int(fp), "fn": int(fn), "tn": int(tn),
              "macro_pr_auc": round(float(np.nanmean([folds[w].get("pr_auc", np.nan)
                                                      for w in folds])), 4)}
    pooled["lift_pr_auc_over_prev"] = round(pooled["pr_auc"] / pooled["prev"], 3)
    print(f"    POOLED: prev={pooled['prev']} PR-AUC={pooled['pr_auc']} "
          f"(lift {pooled['lift_pr_auc_over_prev']}) macro={pooled['macro_pr_auc']} "
          f"P={pooled['precision']:.3f} R={pooled['recall']:.3f} F1={pooled['f1']:.3f}", flush=True)

    out = {"features": raw_feats, "rf_params": RF_PARAMS, "delta_m": 10,
           "folds": folds, "pooled": pooled,
           "reference_md_only_lowo_macro_pr_auc": 0.2265,
           "runtime_s": round(time.time() - t0, 1)}
    OUT_JSON.write_text(json.dumps(out, indent=2, ensure_ascii=False, default=str))
    print(f"SELESAI {out['runtime_s']}s -> {OUT_JSON}", flush=True)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        traceback.print_exc()
        sys.exit(1)
