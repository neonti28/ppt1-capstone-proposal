#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
code/24_ml_diagnostics.py — Diagnostik hasil baseline prediktif (Capstone V2, task t_e7e9bd6d)

Tujuan: memastikan hasil LEMAH pada code/21_predictive_baseline.py itu NYATA (bukan bug),
dan mempersempit penyebabnya. Semua output = angka eksekusi.

D1  Memorization check : PR-AUC RF with_md di TRAIN (harus tinggi bila model bisa fit;
                         kalau train juga rendah -> masalah implementasi/label).
D2  Variant fitur baris-saja (last_* = 12 nilai sensor baris saat ini, TANPA agregasi window)
                         -> menguji hipotesis "agregasi 10 m memuluskan sinyal".
D3  Split per-well depth-blocked (70% latih / 10% val / 20% uji per well, urut md)
                         -> skenario operasi realistis: model di sumur yang SAMA, ramal masa depan.
D4  B1 logistik hanya-MD di LOWO -> apakah sinyal depth lintas-sumur (canary leakage).
D5  recall pada precision 0.15/0.20/0.30 untuk model utama (target lapangan realistis).

Output: docs/V2_ML_DIAGNOSTICS.json + stdout.
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
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (average_precision_score, roc_auc_score, precision_score,
                             recall_score, f1_score, confusion_matrix,
                             precision_recall_curve)

BASE = Path(__file__).resolve().parents[1]
DS_PATH = BASE / "data" / "predictive" / "dataset_prediktif.csv"
OUT_JSON = BASE / "docs" / "V2_ML_DIAGNOSTICS.json"
DELTA = 10
RF_PARAMS = dict(n_estimators=300, class_weight="balanced", min_samples_leaf=2,
                 n_jobs=-1, random_state=42)
RES: dict = {}


def log(m: str = "") -> None:
    print(m, flush=True)


def ap(y, s) -> float | None:
    if len(np.unique(y)) < 2:
        return None
    return round(float(average_precision_score(y, s)), 4)


def recall_at_prec(y, s, target: float) -> float:
    p, r, _ = precision_recall_curve(y, s)
    ok = p[:-1] >= target
    return round(float(r[:-1][ok].max()), 4) if ok.any() else 0.0


def prf(y, pred) -> dict:
    tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel()
    return {"precision": round(float(precision_score(y, pred, zero_division=0)), 4),
            "recall": round(float(recall_score(y, pred, zero_division=0)), 4),
            "f1": round(float(f1_score(y, pred, zero_division=0)), 4),
            "tp": int(tp), "fp": int(fp), "fn": int(fn), "tn": int(tn)}


def tune_thr(y, s) -> float:
    p, r, t = precision_recall_curve(y, s)
    f1 = np.where((p[:-1] + r[:-1]) > 0, 2 * p[:-1] * r[:-1] / np.maximum(p[:-1] + r[:-1], 1e-12), 0.0)
    if f1.size == 0:
        return float(np.quantile(s, 0.95))
    return float(t[f1 >= f1.max() - 1e-12].max())


def main() -> None:
    t0 = time.time()
    log("=" * 78)
    log("24_ml_diagnostics.py — diagnostik baseline prediktif")
    log("=" * 78)
    ds = pd.read_csv(DS_PATH)
    feats = [c for c in ds.columns if c.startswith(("mean_", "std_", "first_", "last_", "delta_"))]
    raw_feats = [c for c in feats if c.startswith("last_")]
    y = ds[f"y_{DELTA}"].to_numpy(int)
    wells = ds["well"].to_numpy()
    md = ds["md"].to_numpy(float)
    ds["ts"] = pd.to_datetime(ds["est_timestamp"], utc=True, errors="coerce")
    ts_np = ds["ts"].dt.tz_convert("UTC").dt.tz_localize(None).to_numpy(dtype="datetime64[ns]")
    Xw = ds[feats].to_numpy(float)
    Xr = ds[raw_feats].to_numpy(float)
    log(f"data: {len(ds)} baris | fitur window={len(feats)} | fitur baris-saja={len(raw_feats)}")

    # ---------- D1 memorization (split temporal sama dengan 21) ----------
    n = len(ds)
    order = np.argsort(ts_np, kind="stable")
    n_tr, n_va = int(0.70 * n), int(0.15 * n)
    tr, va, te = order[:n_tr], order[n_tr:n_tr + n_va], order[n_tr + n_va:]
    rf = RandomForestClassifier(**RF_PARAMS)
    rf.fit(Xw[tr], y[tr])
    s_tr = rf.predict_proba(Xw[tr])[:, 1]
    s_va = rf.predict_proba(Xw[va])[:, 1]
    s_te = rf.predict_proba(Xw[te])[:, 1]
    d1 = {"train_pr_auc": ap(y[tr], s_tr), "val_pr_auc": ap(y[va], s_va),
          "test_pr_auc": ap(y[te], s_te), "test_prevalence": round(float(y[te].mean()), 4),
          "train_prevalence": round(float(y[tr].mean()), 4),
          "roc_auc_train": round(float(roc_auc_score(y[tr], s_tr)), 4)}
    log(f"\n[D1] memorization RF with_md: PR-AUC train={d1['train_pr_auc']} "
        f"(prev {d1['train_prevalence']}) | val={d1['val_pr_auc']} | test={d1['test_pr_auc']} "
        f"(prev {d1['test_prevalence']}) ROC-AUC train={d1['roc_auc_train']}")
    RES["D1_memorization"] = d1

    # ---------- D2 fitur baris-saja (last_*) ----------
    rf2 = RandomForestClassifier(**RF_PARAMS)
    rf2.fit(Xr[tr], y[tr])
    s2_va = rf2.predict_proba(Xr[va])[:, 1]
    s2_te = rf2.predict_proba(Xr[te])[:, 1]
    thr2 = tune_thr(y[va], s2_va)
    d2 = {"test_pr_auc": ap(y[te], s2_te), "test_roc_auc": round(float(roc_auc_score(y[te], s2_te)), 4),
          "val_pr_auc": ap(y[va], s2_va),
          "at_val_tuned_thr": prf(y[te], (s2_te >= thr2).astype(int)),
          "thr": round(float(thr2), 5),
          "recall_at_precision": {str(t): recall_at_prec(y[te], s2_te, t) for t in (0.15, 0.2, 0.3)},
          "top_features": [[k, round(float(v), 4)] for k, v in
                           sorted(zip(raw_feats, rf2.feature_importances_), key=lambda z: -z[1])[:8]]}
    log(f"\n[D2] fitur baris-saja (last_*, 12): PR-AUC test={d2['test_pr_auc']} "
        f"(prev {d2['test_prevalence'] if 'test_prevalence' in d2 else d1['test_prevalence']}) "
        f"P/R/F1={d2['at_val_tuned_thr']}")
    log(f"     top: {[k for k, _ in d2['top_features']]}")
    RES["D2_raw_row_features"] = d2

    # D2b recall@precision untuk model utama (RF window, run 21)
    d2b = {"rf_with_md": {str(t): recall_at_prec(y[te], s_te, t) for t in (0.15, 0.2, 0.3)},
           "rf_with_md_test_pr_auc": d1["test_pr_auc"]}
    log(f"\n[D2b] recall@precision (RF window, temporal test): {d2b['rf_with_md']}")
    RES["D2b_recall_at_precision"] = d2b

    # ---------- D3 per-well depth-blocked (70/10/20 urut md) ----------
    log("\n[D3] split per-well depth-blocked (train 70% | val 10% | test 20% terdalam)")
    d3, pool = {}, {"y": [], "score": [], "pred": []}
    for w in sorted(set(wells)):
        idx = np.flatnonzero(wells == w)
        idx = idx[np.argsort(md[idx], kind="stable")]
        a, b = int(0.7 * len(idx)), int(0.8 * len(idx))
        trw, vaw, tew = idx[:a], idx[a:b], idx[b:]
        if len(np.unique(y[tew])) < 2 or len(np.unique(y[trw])) < 2:
            d3[w] = {"skip": "kelas tunggal di train/test"}
            log(f"    {w}: SKIP (kelas tunggal)")
            continue
        m = RandomForestClassifier(**RF_PARAMS)
        m.fit(Xw[trw], y[trw])
        sv = m.predict_proba(Xw[vaw])[:, 1]
        st = m.predict_proba(Xw[tew])[:, 1]
        thr = tune_thr(y[vaw], sv)
        d3[w] = {"n_test": int(len(tew)), "prev_test": round(float(y[tew].mean()), 4),
                 "pr_auc": ap(y[tew], st), "roc_auc": round(float(roc_auc_score(y[tew], st)), 4),
                 "at_thr": prf(y[tew], (st >= thr).astype(int)),
                 "recall_at_precision": {str(t): recall_at_prec(y[tew], st, t) for t in (0.15, 0.2, 0.3)}}
        pool["y"].append(y[tew]); pool["score"].append(st)
        pool["pred"].append((st >= thr).astype(int))
        log(f"    {w:30s} n={len(tew):6d} prev={d3[w]['prev_test']:.4f} PR-AUC={d3[w]['pr_auc']} "
            f"P={d3[w]['at_thr']['precision']:.3f} R={d3[w]['at_thr']['recall']:.3f} "
            f"F1={d3[w]['at_thr']['f1']:.3f}")
    yP = np.concatenate(pool["y"]); sP = np.concatenate(pool["score"]); pP = np.concatenate(pool["pred"])
    pooled = {"n": int(len(yP)), "prev": round(float(yP.mean()), 4), "pr_auc": ap(yP, sP),
              "roc_auc": round(float(roc_auc_score(yP, sP)), 4),
              "at_thr": prf(yP, pP),
              "recall_at_precision": {str(t): recall_at_prec(yP, sP, t) for t in (0.15, 0.2, 0.3)},
              "macro_pr_auc": round(float(np.nanmean([d3[w].get("pr_auc") or np.nan
                                                      for w in d3 if "skip" not in d3[w]])), 4)}
    log(f"    POOLED: prev={pooled['prev']} PR-AUC={pooled['pr_auc']} ROC={pooled['roc_auc']} "
        f"F1={pooled['at_thr']['f1']} macroPR={pooled['macro_pr_auc']}")
    RES["D3_within_well_depth_blocked"] = {"per_well": d3, "pooled": pooled}

    # ---------- D4 B1 hanya-MD di LOWO ----------
    log("\n[D4] logistik hanya-MD (canary depth) di LOWO")
    d4, y4, s4 = {}, [], []
    for w in sorted(set(wells)):
        trm = wells != w
        tem = ~trm
        sc = StandardScaler().fit(md[trm].reshape(-1, 1))
        lr = LogisticRegression(max_iter=1000, class_weight="balanced")
        lr.fit(sc.transform(md[trm].reshape(-1, 1)), y[trm])
        st = lr.predict_proba(sc.transform(md[tem].reshape(-1, 1)))[:, 1]
        d4[w] = {"pr_auc": ap(y[tem], st), "prev": round(float(y[tem].mean()), 4)}
        y4.append(y[tem]); s4.append(st)
        log(f"    {w:30s} PR-AUC={d4[w]['pr_auc']} prev={d4[w]['prev']}")
    y4 = np.concatenate(y4); s4 = np.concatenate(s4)
    d4_pooled = {"pr_auc": ap(y4, s4), "prev": round(float(y4.mean()), 4),
                 "macro": round(float(np.nanmean([d4[w]["pr_auc"] for w in d4 if d4[w]["pr_auc"] is not None])), 4)}
    log(f"    POOLED: PR-AUC={d4_pooled['pr_auc']} prev={d4_pooled['prev']} macro={d4_pooled['macro']}")
    RES["D4_md_only_lowo"] = {"folds": d4, "pooled": d4_pooled}

    RES["runtime_s"] = round(time.time() - t0, 1)
    RES["rf_params"] = RF_PARAMS
    OUT_JSON.write_text(json.dumps(RES, indent=2, ensure_ascii=False, default=str))
    log(f"\nSELESAI {RES['runtime_s']}s -> {OUT_JSON}")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        traceback.print_exc()
        sys.exit(1)
