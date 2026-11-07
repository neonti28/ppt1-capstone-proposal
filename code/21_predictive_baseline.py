#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
code/21_predictive_baseline.py — Training + evaluasi model prediktif t+Delta (Capstone V2)

Task kanban : t_e7e9bd6d [ML Engineer] Dataset prediktif t+Delta + baseline RF & autoencoder
Input       : data/predictive/dataset_prediktif.csv  (dari code/20_predictive_dataset.py)
              data/volve/usrop_timestamped.csv (MSE/D_exp/ROC_coef HANYA untuk baseline B2)
              data/volve/labels_curated.csv (evaluasi level-event)
              data/bo_tspp/*.csv (validasi sekunder)

Model & baseline (mengikuti docs/V2_RND_METHODS.md §3.3-3.5):
  B0  selalu-normal                    (mematikan klaim accuracy)
  B1  regresi logistik hanya-MD        (canary leakage depth)
  B2  aturan legacy fuzzy 0,50/0,35/0,15 cutoff 40/70 (code/06_xgb_fuzzy.py) = current system
  B2b aturan-if fisika sederhana (ambang torque/WOB/ROP, grid di VALIDASI)
  B3  RandomForest class_weight=balanced (fitur window 12 sensor, TANPA MSE/ROC/D_exp/label)
  M1  autoencoder feed-forward normal-only + z-score + threshold divalidasi
      (deviasi terdokumentasi: LSTM MDPI tidak feasible -> MLPRegressor, lihat laporan)

Split: (1) TEMPORAL global 70/15/15 by est_timestamp (train lampau -> test masa depan)
       (2) LOWO antar 7 wellbore (threshold tiap fold dari ekor temporal well latih)
       (3) sensitivitas Delta {5,10,15,30} m -> kurva PR-AUC vs prevalensi
Bukan random split (anti-leakage Tunkiel).

Semua angka dicetak + disimpan ke docs/V2_ML_METRICS.json; PNG confusion matrix
& kurva PR-AUC vs Delta disimpan ke docs/.
"""

from __future__ import annotations

import json
import sys
import time
import traceback
from pathlib import Path

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (confusion_matrix, precision_score, recall_score,
                             f1_score, roc_auc_score, average_precision_score,
                             precision_recall_curve, accuracy_score)

BASE = Path(__file__).resolve().parents[1]
DS_PATH = BASE / "data" / "predictive" / "dataset_prediktif.csv"
USROP_PATH = BASE / "data" / "volve" / "usrop_timestamped.csv"
LABELS_PATH = BASE / "data" / "volve" / "labels_curated.csv"
TSPP_DIR = BASE / "data" / "bo_tspp"
OUT_JSON = BASE / "docs" / "V2_ML_METRICS.json"
PNG_CONFUSION = BASE / "docs" / "V2_CONFUSION_MATRICES.png"
PNG_PRDELTA = BASE / "docs" / "V2_PR_AUC_VS_DELTA.png"
PNG_TSPP = BASE / "docs" / "V2_TSPP_ANOMALY_SCORES.png"

DELTA_MAIN = 10
DELTAS = [5, 10, 15, 30]
STAT_PREFIX = ("mean_", "std_", "first_", "last_", "delta_")
FORBIDDEN = {"MSE", "D_exp", "ROC_coef", "label"}
RF_PARAMS = dict(n_estimators=300, class_weight="balanced", min_samples_leaf=2,
                 n_jobs=-1, random_state=42)
RESULTS: dict = {"run": {}}


def log(msg: str = "") -> None:
    print(msg, flush=True)


def save_json() -> None:
    OUT_JSON.write_text(json.dumps(RESULTS, indent=2, ensure_ascii=False, default=str))


def tune_threshold(y: np.ndarray, score: np.ndarray) -> float:
    """Threshold F1-maksimum di VALIDASI (bukan 0.5 default, bukan T=0.3 MDPI)."""
    y = np.asarray(y).astype(int)
    score = np.asarray(score, dtype=float)
    if y.sum() == 0 or y.sum() == len(y):
        return float(np.quantile(score, 0.95))
    prec, rec, thr = precision_recall_curve(y, score)
    f1 = np.where((prec[:-1] + rec[:-1]) > 0,
                  2 * prec[:-1] * rec[:-1] / np.maximum(prec[:-1] + rec[:-1], 1e-12), 0.0)
    if f1.size == 0:
        return float(np.quantile(score, 0.95))
    best = np.max(f1)
    cand = thr[f1 >= best - 1e-12]
    return float(cand.max())  # ambang tertinggi di antara yang F1-nya maks (paling konservatif)


def metrics_at(y: np.ndarray, score: np.ndarray, thr: float) -> dict:
    y = np.asarray(y).astype(int)
    score = np.asarray(score, dtype=float)
    pred = (score >= thr).astype(int)
    tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel()
    out = {
        "threshold": float(thr),
        "tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp),
        "n": int(len(y)), "n_pos": int(y.sum()),
        "precision": round(float(precision_score(y, pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y, pred, zero_division=0)), 4),
        "f1": round(float(f1_score(y, pred, zero_division=0)), 4),
        "accuracy": round(float(accuracy_score(y, pred)), 4),
        "prevalence": round(float(y.mean()), 4),
        "pr_auc": round(float(average_precision_score(y, score)), 4),
    }
    out["roc_auc"] = round(float(roc_auc_score(y, score)), 4) if 0 < y.sum() < len(y) else None
    # recall pada precision minimum (RND §3.5)
    p, r, t = precision_recall_curve(y, score)
    ok = p[:-1] >= 0.5
    out["recall_at_precision_0.5"] = round(float(r[:-1][ok].max()), 4) if ok.any() else 0.0
    return out


def lead_and_events(df: pd.DataFrame, ycol: str, pred: np.ndarray, tag: str) -> dict:
    """Lead time (meter) + evaluasi level-event untuk satu set evaluasi."""
    sub = df.copy()
    sub["pred"] = pred
    tp_rows = sub[(sub["pred"] == 1) & (sub[ycol] == 1)]
    res: dict = {"tag": tag}
    if len(tp_rows):
        res["lead_m_mean_tp_rows"] = round(float(tp_rows["lead_m"].mean()), 3)
        res["lead_m_median_tp_rows"] = round(float(tp_rows["lead_m"].median()), 3)
        res["n_tp_rows"] = int(len(tp_rows))
    else:
        res["lead_m_mean_tp_rows"] = None
        res["lead_m_median_tp_rows"] = None
        res["n_tp_rows"] = 0
    # level-event: cluster next_event_md dari baris positif
    pos = sub[sub[ycol] == 1]
    events = pos.groupby("next_event_md")
    n_ev = len(events)
    hit, leads = 0, []
    for emd, g in events:
        ga = g[g["pred"] == 1]
        if len(ga):
            hit += 1
            leads.append(float(emd - ga["md"].min()))
    res["n_event_clusters_test"] = int(n_ev)
    res["events_hit"] = int(hit)
    res["event_hit_rate"] = round(hit / n_ev, 4) if n_ev else None
    res["event_lead_m_mean"] = round(float(np.mean(leads)), 3) if leads else None
    res["event_lead_m_median"] = round(float(np.median(leads)), 3) if leads else None
    # false-alarm episode per 100 m bor
    fp_eps, span = 0, 0.0
    for _, g in sub.sort_values(["well", "md"]).groupby("well"):
        g = g.reset_index(drop=True)
        span += float(g["md"].max() - g["md"].min())
        arr = g["pred"].to_numpy()
        yv = g[ycol].to_numpy()
        i = 0
        while i < len(arr):
            if arr[i] == 1:
                j = i
                while j < len(arr) and arr[j] == 1:
                    j += 1
                if yv[i:j].sum() == 0:
                    fp_eps += 1
                i = j
            else:
                i += 1
    res["false_alarm_episodes"] = int(fp_eps)
    res["depth_span_m"] = round(span, 1)
    res["false_alarm_per_100m"] = round(100.0 * fp_eps / span, 3) if span > 0 else None
    return res


def fmt(m: dict) -> str:
    return (f"P={m['precision']:.3f} R={m['recall']:.3f} F1={m['f1']:.3f} "
            f"PR-AUC={m['pr_auc']:.3f} ROC-AUC={m['roc_auc']} "
            f"thr={m['threshold']:.4g} TP={m['tp']} FP={m['fp']} FN={m['fn']} TN={m['tn']} "
            f"prev={m['prevalence']:.4f} R@P>=.5={m['recall_at_precision_0.5']:.3f}")


# ================================================================= MAIN
def main() -> None:
    t_start = time.time()
    log("=" * 78)
    log("21_predictive_baseline.py — training + evaluasi prediktif t+Delta")
    log("=" * 78)

    # ---------- 0. muat data ----------
    ds = pd.read_csv(DS_PATH)
    log(f"[0] dataset_prediktif.csv: {len(ds)} baris x {ds.shape[1]} kolom")

    feats = [c for c in ds.columns if c.startswith(STAT_PREFIX)]
    md_feats = [c for c in feats if c.endswith("_md")]
    FEAT_WITH_MD = feats
    FEAT_NO_MD = [c for c in feats if c not in md_feats]
    bad = set(feats) & FORBIDDEN
    if bad:
        sys.exit(f"FATAL: fitur memuat kolom terlarang: {bad}")
    log(f"[0] fitur: with_md={len(FEAT_WITH_MD)}, no_md={len(FEAT_NO_MD)} "
        f"(buang {md_feats} untuk varian no-md); 0 kolom terlarang")

    us = pd.read_csv(USROP_PATH, usecols=["MSE", "D_exp", "ROC_coef"])
    us["row_id"] = np.arange(len(us), dtype=np.int64)
    ds = ds.merge(us[["row_id", "MSE", "D_exp", "ROC_coef"]], on="row_id", how="left", validate="1:1")
    if ds["MSE"].isna().any():
        sys.exit("FATAL: merge MSE/D_exp/ROC_coef gagal")
    ds["ts"] = pd.to_datetime(ds["est_timestamp"], utc=True, errors="coerce")
    if ds["ts"].isna().any():
        sys.exit("FATAL: est_timestamp gagal parse")

    ycol = f"y_{DELTA_MAIN}"
    X_all = {f"with_md": ds[FEAT_WITH_MD].to_numpy(dtype=float),
             f"no_md": ds[FEAT_NO_MD].to_numpy(dtype=float)}
    y_all = {f"y_{D}": ds[f"y_{D}"].to_numpy(dtype=int) for D in DELTAS}
    # timestamp netik (UTC naive) untuk argsort stabil
    ts_np = ds["ts"].dt.tz_convert("UTC").dt.tz_localize(None).to_numpy(dtype="datetime64[ns]")
    log(f"[0] class distribution: " + ", ".join(
        f"y_{D}={y_all[f'y_{D}'].sum()} ({y_all[f'y_{D}'].mean()*100:.2f}%)" for D in DELTAS))

    # ---------- 1. split temporal ----------
    order = np.argsort(ts_np, kind="stable")
    n = len(ds)
    n_tr, n_va = int(0.70 * n), int(0.15 * n)
    tr = order[:n_tr]
    va = order[n_tr:n_tr + n_va]
    te = order[n_tr + n_va:]
    log(f"\n[1] SPLIT TEMPORAL (bukan random): train {len(tr)} | val {len(va)} | test {len(te)}")
    comp = {}
    for nm, idx in [("train", tr), ("val", va), ("test", te)]:
        seg = ds.iloc[idx]
        comp[nm] = {
            "n": int(len(idx)),
            "ts_min": str(seg["ts"].min()), "ts_max": str(seg["ts"].max()),
            "y10_pos": int(seg[ycol].sum()),
            "y10_prev": round(float(seg[ycol].mean()), 4),
            "per_well": {k: int(v) for k, v in seg["well"].value_counts().items()},
        }
        log(f"    {nm:5s}: n={len(idx)} {seg['ts'].min()} -> {seg['ts'].max()} "
            f"pos y10={int(seg[ycol].sum())} ({seg[ycol].mean()*100:.2f}%) wells={seg['well'].nunique()}")
    RESULTS["run"]["split_temporal"] = comp
    RESULTS["run"]["features"] = {"with_md": len(FEAT_WITH_MD), "no_md": len(FEAT_NO_MD),
                                  "md_features_dropped_in_no_md": md_feats}
    save_json()

    test_df = ds.iloc[te].reset_index(drop=True)
    X = {k: v for k, v in X_all.items()}

    # ---------- 2. baselines ----------
    log("\n[2] BASELINE (evaluasi di test, split temporal, y_10)")
    res_b: dict = {}

    # B0 selalu normal
    y_te = y_all["y_10"][te]
    pred0 = np.zeros(len(te), dtype=int)
    tn, fp, fn, tp = 0, 0, int(y_te.sum()), 0
    res_b["B0_selalu_normal"] = {
        "accuracy": round(float((pred0 == y_te).mean()), 4),
        "pr_auc_reference_prevalence": round(float(y_te.mean()), 4),
        "note": f"predict-all-negative: accuracy={(pred0 == y_te).mean()*100:.2f}%, "
                f"PR-AUC acak = prevalensi {y_te.mean()*100:.2f}%",
    }
    log(f"    B0 selalu-normal : accuracy={res_b['B0_selalu_normal']['accuracy']:.4f} "
        f"(PR-AUC acak = {res_b['B0_selalu_normal']['pr_auc_reference_prevalence']:.4f})")

    # B1 logistic hanya-MD
    sc = StandardScaler()
    md_tr = sc.fit_transform(ds[["md"]].iloc[tr])
    md_va = sc.transform(ds[["md"]].iloc[va])
    md_te = sc.transform(ds[["md"]].iloc[te])
    lr = LogisticRegression(max_iter=1000, class_weight="balanced")
    lr.fit(md_tr, y_all["y_10"][tr])
    s_va = lr.predict_proba(md_va)[:, 1]
    s_te = lr.predict_proba(md_te)[:, 1]
    thr = tune_threshold(y_all["y_10"][va], s_va)
    res_b["B1_logistik_hanya_MD"] = metrics_at(y_te, s_te, thr)
    log(f"    B1 logistik MD    : {fmt(res_b['B1_logistik_hanya_MD'])}")

    # B2 legacy fuzzy (current system) — referensi dari TRAIN saja
    mse = ds["MSE"].to_numpy(float); roc = ds["ROC_coef"].to_numpy(float); dex = ds["D_exp"].to_numpy(float)
    mse_p75 = float(np.percentile(mse[tr][mse[tr] > 0], 75))
    roc_p25 = float(np.percentile(roc[tr][roc[tr] > 0], 25))
    dexp_med = float(np.median(dex[tr][dex[tr] > 0]))
    mse_bad = np.clip((mse - mse_p75 * 0.5) / (mse_p75 * 1.5 - mse_p75 * 0.5 + 1e-9), 0, 1)
    roc_bad = np.clip((roc_p25 * 1.5 - roc) / (roc_p25 * 1.5 - roc_p25 * 0.1 + 1e-9), 0, 1)
    d_bad = np.clip(np.abs(dex - dexp_med) / (dexp_med * 2 + 1e-9), 0, 1)
    health = 100 * (1 - (0.5 * mse_bad + 0.35 * roc_bad + 0.15 * d_bad))
    score_b2 = 100.0 - health  # makin tinggi = makin sakit
    thr_b2 = tune_threshold(y_all["y_10"][va], score_b2[va])
    res_b["B2_legacy_fuzzy"] = metrics_at(y_te, score_b2[te], thr_b2)
    res_b["B2_legacy_fuzzy"]["cutoff_40"] = metrics_at(y_te, score_b2[te], 60.0)   # health<40
    res_b["B2_legacy_fuzzy"]["cutoff_70"] = metrics_at(y_te, score_b2[te], 30.0)   # health<70
    res_b["B2_legacy_fuzzy"]["ref_stats_from_train"] = {"mse_p75": round(mse_p75, 3),
                                                        "roc_p25": float(f"{roc_p25:.6g}"),
                                                        "d_exp_med": round(dexp_med, 3)}
    log(f"    B2 fuzzy legacy    : {fmt(res_b['B2_legacy_fuzzy'])}")
    log(f"      -> cutoff health<40 : {fmt(res_b['B2_legacy_fuzzy']['cutoff_40'])}")
    log(f"      -> cutoff health<70 : {fmt(res_b['B2_legacy_fuzzy']['cutoff_70'])}")

    # B2b aturan-if fisika sederhana (ambang torque/WOB/ROP; ambang dari train, dipilih di val)
    raw = {"torque": ds["last_torque"].to_numpy(float),
           "wob": ds["last_wob"].to_numpy(float),
           "rop": ds["last_rop"].to_numpy(float)}
    q = {k: {p: float(np.quantile(v[tr], p)) for p in (0.02, 0.05, 0.90, 0.95, 0.98)}
         for k, v in raw.items()}
    rules = {
        "torque > P95": raw["torque"] > q["torque"][0.95],
        "torque > P98": raw["torque"] > q["torque"][0.98],
        "torque < P2": raw["torque"] < q["torque"][0.02],
        "wob > P95": raw["wob"] > q["wob"][0.95],
        "wob < P5": raw["wob"] < q["wob"][0.05],
        "rop < P5": raw["rop"] < q["rop"][0.05],
        "torque>P95 ATAU wob>P95": (raw["torque"] > q["torque"][0.95]) | (raw["wob"] > q["wob"][0.95]),
        "torque>P95 ATAU wob<P5": (raw["torque"] > q["torque"][0.95]) | (raw["wob"] < q["wob"][0.05]),
        "torque>P95 ATAU rop<P5": (raw["torque"] > q["torque"][0.95]) | (raw["rop"] < q["rop"][0.05]),
        "(torque>P95 ATAU wob<P5) ATAU rop<P5": ((raw["torque"] > q["torque"][0.95]) | (raw["wob"] < q["wob"][0.05])) | (raw["rop"] < q["rop"][0.05]),
    }
    best_name, best_f1, best_rule = None, -1.0, None
    for name, r in rules.items():
        f1v = f1_score(y_all["y_10"][va], r[va].astype(int), zero_division=0)
        if f1v > best_f1:
            best_name, best_f1, best_rule = name, float(f1v), r
    yv = y_all["y_10"][va]
    pv = best_rule[va].astype(int)
    tp = int(((pv == 1) & (yv == 1)).sum()); fp = int(((pv == 1) & (yv == 0)).sum())
    fn = int(((pv == 0) & (yv == 1)).sum())
    res_b["B2b_aturan_fisika"] = {
        "best_rule": best_name, "val_f1": round(best_f1, 4),
        "val_quantiles": {k: {str(p): round(v2, 4) for p, v2 in v.items()} for k, v in q.items()},
    }
    p_te = best_rule[te].astype(int)
    tp = int(((p_te == 1) & (y_te == 1)).sum()); fp = int(((p_te == 1) & (y_te == 0)).sum())
    fn = int(((p_te == 0) & (y_te == 1)).sum()); tn = int(((p_te == 0) & (y_te == 0)).sum())
    res_b["B2b_aturan_fisika"]["test"] = {
        "precision": round(tp / max(tp + fp, 1), 4), "recall": round(tp / max(tp + fn, 1), 4),
        "f1": round(2 * tp / max(2 * tp + fp + fn, 1), 4), "tp": tp, "fp": fp, "fn": fn, "tn": tn,
    }
    res_b["B2b_aturan_fisika"]["note"] = ("binary rule -> PR-AUC tidak dilaporkan sebagai skor kontinu; "
                                          "ambang dari kuantil train, pemilihan di val")
    log(f"    B2b aturan fisika  : rule='{best_name}' valF1={best_f1:.3f} -> "
        f"P={res_b['B2b_aturan_fisika']['test']['precision']:.3f} "
        f"R={res_b['B2b_aturan_fisika']['test']['recall']:.3f} "
        f"F1={res_b['B2b_aturan_fisika']['test']['f1']:.3f}")
    RESULTS["run"]["baselines_temporal"] = res_b
    save_json()

    # ---------- 3. B3 RF (with_md & no_md) ----------
    log("\n[3] B3 RANDOM FOREST (class_weight=balanced) — split temporal, y_10")
    res_rf: dict = {}
    preds_store = {}
    for variant in ("with_md", "no_md"):
        t0 = time.time()
        rf = RandomForestClassifier(**RF_PARAMS)
        rf.fit(X[variant][tr], y_all["y_10"][tr])
        s_va = rf.predict_proba(X[variant][va])[:, 1]
        s_te = rf.predict_proba(X[variant][te])[:, 1]
        thr = tune_threshold(y_all["y_10"][va], s_va)
        m = metrics_at(y_te, s_te, thr)
        m["fit_s"] = round(time.time() - t0, 1)
        m["lead_and_events"] = lead_and_events(test_df, ycol, (s_te >= thr).astype(int), f"RF_{variant}")
        res_rf[f"B3_RF_{variant}"] = m
        preds_store[variant] = (s_te, thr)
        imp = sorted(zip(FEAT_WITH_MD if variant == "with_md" else FEAT_NO_MD,
                         rf.feature_importances_), key=lambda z: -z[1])[:8]
        m["top_features"] = [[k, round(float(v), 4)] for k, v in imp]
        log(f"    RF {variant:8s}: {fmt(m)} fit={m['fit_s']}s")
        log(f"      lead: {m['lead_and_events']}")
        log(f"      top fitur: {[k for k, _ in imp]}")
    RESULTS["run"]["rf_temporal"] = res_rf
    save_json()

    # ---------- 4. M1 autoencoder ----------
    log("\n[4] M1 AUTOENCODER (feed-forward, normal-only, z-score) — split temporal, y_10")
    scaler = StandardScaler().fit(X["with_md"][tr][y_all["y_10"][tr] == 0])
    Xtr_n = scaler.transform(X["with_md"][tr][y_all["y_10"][tr] == 0])
    Xva = scaler.transform(X["with_md"][va])
    Xte = scaler.transform(X["with_md"][te])
    t0 = time.time()
    ae = MLPRegressor(hidden_layer_sizes=(32, 16, 32), activation="relu", solver="adam",
                      batch_size=256, max_iter=60, early_stopping=True,
                      validation_fraction=0.1, n_iter_no_change=5,
                      learning_rate_init=1e-3, random_state=42)
    ae.fit(Xtr_n, Xtr_n)
    err_va = np.mean((ae.predict(Xva) - Xva) ** 2, axis=1)
    err_te = np.mean((ae.predict(Xte) - Xte) ** 2, axis=1)
    thr_ae = tune_threshold(y_all["y_10"][va], err_va)
    thr_p99 = float(np.quantile(np.mean((ae.predict(Xtr_n) - Xtr_n) ** 2, axis=1), 0.99))
    m_ae = metrics_at(y_te, err_te, thr_ae)
    m_ae["fit_s"] = round(time.time() - t0, 1)
    m_ae["n_iter"] = int(ae.n_iter_)
    m_ae["n_train_normal"] = int(Xtr_n.shape[0])
    m_ae["lead_and_events"] = lead_and_events(test_df, ycol, (err_te >= thr_ae).astype(int), "AE_temporal")
    m_ae["threshold_p99_normal_train"] = metrics_at(y_te, err_te, thr_p99)
    RESULTS["run"]["ae_temporal"] = m_ae
    save_json()
    log(f"    AE feed-forward    : {fmt(m_ae)} fit={m_ae['fit_s']}s n_iter={m_ae['n_iter']} "
        f"train_normal={m_ae['n_train_normal']}")
    log(f"      thr alternatif p99-normal({thr_p99:.4g}): "
        f"P={m_ae['threshold_p99_normal_train']['precision']:.3f} "
        f"R={m_ae['threshold_p99_normal_train']['recall']:.3f} "
        f"F1={m_ae['threshold_p99_normal_train']['f1']:.3f}")
    log(f"      lead: {m_ae['lead_and_events']}")

    # ---------- 5. sensitivitas Delta ----------
    log("\n[5] SENSITIVITAS Delta (RF with_md, split temporal) — PR-AUC vs Delta")
    sens = {}
    for D in DELTAS:
        if D == DELTA_MAIN:
            sens[str(D)] = {"pr_auc": res_rf["B3_RF_with_md"]["pr_auc"],
                            "prevalence_test": res_rf["B3_RF_with_md"]["prevalence"],
                            "f1": res_rf["B3_RF_with_md"]["f1"],
                            "precision": res_rf["B3_RF_with_md"]["precision"],
                            "recall": res_rf["B3_RF_with_md"]["recall"],
                            "note": "reuse model Delta=10 utama"}
            continue
        yD = y_all[f"y_{D}"]
        rf = RandomForestClassifier(**RF_PARAMS)
        rf.fit(X["with_md"][tr], yD[tr])
        s_va = rf.predict_proba(X["with_md"][va])[:, 1]
        s_te = rf.predict_proba(X["with_md"][te])[:, 1]
        thr = tune_threshold(yD[va], s_va)
        m = metrics_at(yD[te], s_te, thr)
        sens[str(D)] = {"pr_auc": m["pr_auc"], "prevalence_test": m["prevalence"],
                        "f1": m["f1"], "precision": m["precision"], "recall": m["recall"]}
        log(f"    Delta {D:2d}m: prev={m['prevalence']:.4f} PR-AUC={m['pr_auc']:.4f} "
            f"F1={m['f1']:.3f} P={m['precision']:.3f} R={m['recall']:.3f}")
    RESULTS["run"]["delta_sensitivity"] = sens
    save_json()

    # ---------- 6. LOWO ----------
    log("\n[6] LOWO (Leave-One-Well-Out) — RF with_md, y_10, threshold dari val temporal well latih")
    wells = sorted(ds["well"].unique())
    lowo, pool = {}, {"y": [], "pred": [], "score": []}
    for w in wells:
        idx_all = np.arange(n)
        te_w = idx_all[ds["well"].to_numpy() == w]
        rest = idx_all[ds["well"].to_numpy() != w]
        rest_sorted = rest[np.argsort(ts_np[rest], kind="stable")]
        n_va_w = int(0.15 * len(rest_sorted))
        va_w = rest_sorted[-n_va_w:]
        tr_w = rest_sorted[:-n_va_w]
        rf = RandomForestClassifier(**RF_PARAMS)
        rf.fit(X["with_md"][tr_w], y_all["y_10"][tr_w])
        s_va = rf.predict_proba(X["with_md"][va_w])[:, 1]
        s_te = rf.predict_proba(X["with_md"][te_w])[:, 1]
        thr = tune_threshold(y_all["y_10"][va_w], s_va)
        yw = y_all["y_10"][te_w]
        m = metrics_at(yw, s_te, thr)
        m["test_well"] = w
        m["train_wells"] = int(ds.iloc[tr_w]["well"].nunique())
        lowo[w] = m
        pool["y"].append(yw); pool["pred"].append((s_te >= thr).astype(int)); pool["score"].append(s_te)
        log(f"    fold {w:28s}: n={m['n']} pos={m['n_pos']} prev={m['prevalence']:.4f} "
            f"P={m['precision']:.3f} R={m['recall']:.3f} F1={m['f1']:.3f} PR-AUC={m['pr_auc']:.3f}")
    y_p = np.concatenate(pool["y"]); pred_p = np.concatenate(pool["pred"]); score_p = np.concatenate(pool["score"])
    tn, fp, fn, tp = confusion_matrix(y_p, pred_p, labels=[0, 1]).ravel()
    pooled = {"n": int(len(y_p)), "n_pos": int(y_p.sum()),
              "precision": round(float(precision_score(y_p, pred_p, zero_division=0)), 4),
              "recall": round(float(recall_score(y_p, pred_p, zero_division=0)), 4),
              "f1": round(float(f1_score(y_p, pred_p, zero_division=0)), 4),
              "pr_auc": round(float(average_precision_score(y_p, score_p)), 4),
              "roc_auc": round(float(roc_auc_score(y_p, score_p)), 4),
              "prevalence": round(float(y_p.mean()), 4),
              "tp": int(tp), "fp": int(fp), "fn": int(fn), "tn": int(tn),
              "macro_pr_auc_folds": round(float(np.mean([lowo[w]["pr_auc"] for w in wells])), 4),
              "macro_f1_folds": round(float(np.mean([lowo[w]["f1"] for w in wells])), 4)}
    RESULTS["run"]["lowo"] = {"folds": lowo, "pooled": pooled}
    save_json()
    log(f"    LOWO POOLED        : P={pooled['precision']:.3f} R={pooled['recall']:.3f} "
        f"F1={pooled['f1']:.3f} PR-AUC={pooled['pr_auc']:.3f} (macro PR-AUC={pooled['macro_pr_auc_folds']:.3f})")

    # ---------- 7. PNG confusion ----------
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.6))
    panels = [
        (y_te, (preds_store["with_md"][0] >= preds_store["with_md"][1]).astype(int),
         f"RF with_md — temporal test (n={len(y_te)})"),
        (y_te, (err_te >= thr_ae).astype(int), f"AE feed-forward — temporal test (n={len(y_te)})"),
        (y_p, pred_p, f"RF LOWO pooled (n={len(y_p)})"),
    ]
    for ax, (yy, pp, ttl) in zip(axes, panels):
        cm = confusion_matrix(yy, pp, labels=[0, 1])
        im = ax.imshow(cm, cmap="Blues")
        for (i, j), v in np.ndenumerate(cm):
            ax.text(j, i, str(v), ha="center", va="center",
                    color="white" if v > cm.max() * 0.55 else "black", fontsize=11)
        ax.set_xticks([0, 1], ["negatif", "positif"])
        ax.set_yticks([0, 1], ["negatif", "positif"])
        ax.set_xlabel("prediksi"); ax.set_ylabel("aktual")
        ax.set_title(ttl, fontsize=9)
        fig.colorbar(im, ax=ax, fraction=0.046)
    fig.suptitle("Confusion matrix — prediksi event dalam t+10 m (test)", fontsize=11)
    fig.tight_layout()
    fig.savefig(PNG_CONFUSION, dpi=140)
    plt.close(fig)
    log(f"\n[7] PNG confusion -> {PNG_CONFUSION.name}")

    # PNG PR-AUC vs Delta
    xs = [int(k) for k in sens.keys()]
    xs.sort()
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(xs, [sens[str(d)]["pr_auc"] for d in xs], "o-", label="PR-AUC (RF with_md)")
    ax.plot(xs, [sens[str(d)]["prevalence_test"] for d in xs], "s--",
            label="baseline PR-AUC = prevalensi test")
    ax.set_xlabel("Delta (m)"); ax.set_ylabel("skor")
    ax.set_title("PR-AUC vs Delta — split temporal, RF with_md")
    ax.grid(alpha=0.3); ax.legend()
    fig.tight_layout(); fig.savefig(PNG_PRDELTA, dpi=140); plt.close(fig)
    log(f"    PNG PR-AUC vs Delta -> {PNG_PRDELTA.name}")

    # ---------- 8. validasi sekunder bo_tspp ----------
    log("\n[8] VALIDASI SEKUNDER data/bo_tspp/ (skor anomali AE-8sensor, tanpa label)")
    shared = {  # TSPP col -> USROP col
        "Average Hookload kkgf": "Average Hookload kkgf",
        "Hole depth (MD) m": "Measured Depth m",
        "Weight on Bit kkgf": "Weight on Bit kkgf",
        "Averaged WOB kkgf": "Weight on Bit kkgf",
        "Average Rotary Speed rpm": "Average Rotary Speed rpm",
        "RPM30s rpm": "Average Rotary Speed rpm",
        "Average Surface Torque kN.m": "Average Surface Torque kN.m",
        "Average Standpipe Pressure kPa": "Average Standpipe Pressure kPa",
        "Mud Flow In L/min": "Mud Flow In L/min",
        "Rate of Penetration m/h": "Rate of Penetration m/h",
        "Rate of Penetration  m/h": "Rate of Penetration m/h",
    }
    ucols = ["Average Hookload kkgf", "Measured Depth m", "Weight on Bit kkgf",
             "Average Rotary Speed rpm", "Average Surface Torque kN.m",
             "Average Standpipe Pressure kPa", "Mud Flow In L/min", "Rate of Penetration m/h"]
    us_raw = pd.read_csv(USROP_PATH, usecols=ucols)
    us_raw["row_id"] = np.arange(len(us_raw), dtype=np.int64)
    y_ds = ds[["row_id", ycol]]
    us_raw = us_raw.merge(y_ds, on="row_id", validate="1:1")
    normal_mask = (us_raw[ycol] == 0).to_numpy()
    Xn8 = us_raw.loc[normal_mask, ucols].to_numpy(float)
    n_tr8 = int(0.7 * len(Xn8))
    rng = np.random.default_rng(42)
    perm = rng.permutation(len(Xn8))
    fit8, hold8 = Xn8[perm[:n_tr8]], Xn8[perm[n_tr8:]]
    sc8 = StandardScaler().fit(fit8)
    ae8 = MLPRegressor(hidden_layer_sizes=(16, 8, 16), activation="relu", solver="adam",
                       batch_size=256, max_iter=50, early_stopping=True,
                       validation_fraction=0.1, n_iter_no_change=5, random_state=42)
    ae8.fit(sc8.transform(fit8), sc8.transform(fit8))
    err_hold = np.mean((ae8.predict(sc8.transform(hold8)) - sc8.transform(hold8)) ** 2, axis=1)
    thr8 = float(np.quantile(err_hold, 0.95))
    mu8, sd8 = fit8.mean(axis=0), fit8.std(axis=0) + 1e-9
    log(f"    AE8 latih: {len(fit8)} baris USROP normal, holdout {len(hold8)}, "
        f"threshold p95={thr8:.4g}")

    tspp_rows = []
    norm = lambda s: " ".join(str(s).lower().split())  # case-insensitive + multi-space
    shared_norm = {norm(k): v for k, v in shared.items()}
    med_full = np.nanmedian(fit8, axis=0)  # median USROP per kolom (koordinat ucols, len 8)
    for f in sorted(TSPP_DIR.glob("*.csv")):
        t = pd.read_csv(f)
        t.columns = [c.strip() for c in t.columns]
        colmap, missing = {}, []
        for c in t.columns:
            if norm(c) in shared_norm:
                colmap[c] = shared_norm[norm(c)]
        want = [c for c in t.columns if c in colmap]
        use_usrop = [colmap[c] for c in want]
        if len(want) < 6:
            missing.append(f"kolom cocok hanya {len(want)}")
        Xt = t[want].to_numpy(float)
        med = np.nanmedian(fit8[:, [ucols.index(u) for u in use_usrop]], axis=0)
        for j in range(Xt.shape[1]):
            bad = ~np.isfinite(Xt[:, j])
            Xt[bad, j] = med[j]
        # z-score terhadap statistis USROP (koordinat kolom USROP)
        z = np.zeros_like(Xt)
        for j, uc in enumerate(use_usrop):
            k = ucols.index(uc)
            z[:, j] = (Xt[:, j] - mu8[k]) / sd8[k]
        # AE butuh 8 kolom urut ucols -> isi kolom absen dgn median USROP (didokumentasikan)
        full = np.tile(med_full, (len(Xt), 1))
        for j, uc in enumerate(use_usrop):
            full[:, ucols.index(uc)] = Xt[:, j]
        err = np.mean((ae8.predict(sc8.transform(full)) - sc8.transform(full)) ** 2, axis=1)
        share_bad = float((err > thr8).mean())
        z3 = float((np.abs(z) > 3).any(axis=1).mean())
        ts = pd.to_datetime(t["date"], errors="coerce")
        tspp_rows.append({
            "file": f.name, "rows": int(len(t)), "matched_cols": len(want),
            "date_min": str(ts.min()), "date_max": str(ts.max()),
            "err_median": round(float(np.median(err)), 4),
            "err_p95": round(float(np.quantile(err, 0.95)), 4),
            "share_above_threshold": round(share_bad, 4),
            "share_rows_any_z_gt3": round(z3, 4),
            "note": missing,
        })
        log(f"    {f.name:16s}: rows={len(t):6d} cols={len(want)} err_med={np.median(err):.4g} "
            f"p95={np.quantile(err, 0.95):.4g} >thr={share_bad*100:.1f}% any|z|>3={z3*100:.1f}%")
    tspp_df = pd.DataFrame(tspp_rows)
    tspp_df.to_csv(BASE / "docs" / "V2_TSPP_AE_SCORES.csv", index=False)
    RESULTS["run"]["tspp_secondary"] = tspp_rows
    RESULTS["run"]["tspp_ae"] = {"train_rows": int(len(fit8)), "holdout": int(len(hold8)),
                                 "threshold_p95": thr8, "features": ucols}
    save_json()

    # PNG skor TSPP
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(tspp_df["file"], tspp_df["share_above_threshold"] * 100, color="steelblue")
    ax.axhline(5.0, ls="--", color="red", label="threshold p95 USROP (=5% by design holdout)")
    ax.set_ylabel("% baris di atas threshold anomali")
    ax.set_title("Skor anomali AE-USROP pada data Bo TSPP (tanpa label -> perilaku saja)")
    ax.legend(); plt.xticks(rotation=20, ha="right")
    fig.tight_layout(); fig.savefig(PNG_TSPP, dpi=140); plt.close(fig)
    log(f"    PNG TSPP -> {PNG_TSPP.name}")

    RESULTS["run"]["runtime_s_total"] = round(time.time() - t_start, 1)
    RESULTS["run"]["rf_params"] = RF_PARAMS
    RESULTS["run"]["ae_params"] = {"hidden": [32, 16, 32], "max_iter": 60, "normal_only": True,
                                   "zscore_on_train_normal": True}
    save_json()
    log(f"\nSELESAI total {RESULTS['run']['runtime_s_total']}s -> {OUT_JSON}")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        traceback.print_exc()
        sys.exit(1)
