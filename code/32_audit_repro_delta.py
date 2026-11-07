#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
code/32_audit_repro_delta.py
AUDIT t_abc6eef6 [ML Auditor]
  CHECK 4b : REPRODUKSI independen angka laporan (split temporal, B1, B2 fuzzy, B2b,
             RF with_md / no_md) — angka laporan harus bisa dit ulang dengan seed sama
  CHECK 6  : FAKE-ML / sensitivitas Delta — apakah % positif melebar sehingga tugas jadi mudah?

Output stdout = bukti eksekusi auditor; ringkasan -> docs/V2_ML_AUDIT_PART2.json
"""
from __future__ import annotations
import json, sys, time
from pathlib import Path
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (average_precision_score, roc_auc_score, precision_score,
                             recall_score, f1_score, confusion_matrix)

BASE = Path(__file__).resolve().parents[1]
DS = BASE / "data" / "predictive" / "dataset_prediktif.csv"
USROP = BASE / "data" / "volve" / "usrop_timestamped.csv"
JSON_MET = BASE / "docs" / "V2_ML_METRICS.json"
STAT_PREFIX = ("mean_", "std_", "first_", "last_", "delta_")
RF_PARAMS = dict(n_estimators=300, class_weight="balanced", min_samples_leaf=2,
                 n_jobs=-1, random_state=42)
DELTAS = [5, 10, 15, 30]
T0 = time.time()

def hdr(t): print("\n" + "=" * 78 + f"\n{t}\n" + "=" * 78, flush=True)
def log(*a): print(*a, flush=True)

def tune_threshold(y, score):
    from sklearn.metrics import precision_recall_curve
    y = np.asarray(y).astype(int); score = np.asarray(score, float)
    if y.sum() == 0 or y.sum() == len(y):
        return float(np.quantile(score, 0.95))
    prec, rec, thr = precision_recall_curve(y, score)
    f1 = np.where((prec[:-1] + rec[:-1]) > 0,
                  2 * prec[:-1] * rec[:-1] / np.maximum(prec[:-1] + rec[:-1], 1e-12), 0.0)
    if f1.size == 0:
        return float(np.quantile(score, 0.95))
    best = np.max(f1)
    return float(thr[f1 >= best - 1e-12].max())

def met_at(y, score, thr):
    p = (score >= thr).astype(int)
    tn, fp, fn, tp = confusion_matrix(y, p, labels=[0, 1]).ravel()
    return dict(pr_auc=round(float(average_precision_score(y, score)), 4),
                roc=round(float(roc_auc_score(y, score)), 4),
                precision=round(float(precision_score(y, p, zero_division=0)), 4),
                recall=round(float(recall_score(y, p, zero_division=0)), 4),
                f1=round(float(f1_score(y, p, zero_division=0)), 4),
                tp=int(tp), fp=int(fp), fn=int(fn))

rep = json.loads(JSON_MET.read_text(encoding="utf-8"))["run"]

# --------------------------------------------------------------- muat + split
hdr("MUAT + SPLIT TEMPORAL (identik code/21)")
ds = pd.read_csv(DS, low_memory=False)
feats = [c for c in ds.columns if c.startswith(STAT_PREFIX)]
md_feats = [c for c in feats if c.endswith("_md")]
FEAT_NO_MD = [c for c in feats if c not in md_feats]
ds["ts"] = pd.to_datetime(ds["est_timestamp"], utc=True, errors="coerce")
ts_np = ds["ts"].dt.tz_convert("UTC").dt.tz_localize(None).to_numpy(dtype="datetime64[ns]")
order = np.argsort(ts_np, kind="stable")
n = len(ds); n_tr, n_va = int(0.70 * n), int(0.15 * n)
tr, va, te = order[:n_tr], order[n_tr:n_tr + n_va], order[n_tr + n_va:]
y10 = ds["y_10"].to_numpy(int)
X = {"with_md": ds[feats].to_numpy(float), "no_md": ds[FEAT_NO_MD].to_numpy(float)}
log(f"n={n} | train {len(tr)} val {len(va)} test {len(te)} | prev test {y10[te].mean():.4f}")

repro = {}

# --------------------------------------------------------------- B1
log("\n[REPRO B1] logistik hanya-MD")
sc = StandardScaler()
md_tr = sc.fit_transform(ds[["md"]].iloc[tr]); md_va = sc.transform(ds[["md"]].iloc[va])
md_te = sc.transform(ds[["md"]].iloc[te])
lr = LogisticRegression(max_iter=1000, class_weight="balanced")
lr.fit(md_tr, y10[tr])
thr = tune_threshold(y10[va], lr.predict_proba(md_va)[:, 1])
m = met_at(y10[te], lr.predict_proba(md_te)[:, 1], thr)
repro["B1_logistik_MD"] = m
log(f"  auditor: {m}")
log(f"  laporan : {rep['baselines_temporal']['B1_logistik_hanya_MD']}")

# --------------------------------------------------------------- B2 fuzzy
log("\n[REPRO B2] fuzzy legacy (threshold p75/p25/med dari TRAIN)")
us = pd.read_csv(USROP, usecols=["MSE", "D_exp", "ROC_coef"])
us["row_id"] = np.arange(len(us), dtype=np.int64)
ds2 = ds.merge(us, on="row_id", how="left", validate="1:1")
mse = ds2["MSE"].to_numpy(float); roc_ = ds2["ROC_coef"].to_numpy(float); dex = ds2["D_exp"].to_numpy(float)
mse_p75 = float(np.percentile(mse[tr][mse[tr] > 0], 75))
roc_p25 = float(np.percentile(roc_[tr][roc_[tr] > 0], 25))
dexp_med = float(np.median(dex[tr][dex[tr] > 0]))
mse_bad = np.clip((mse - mse_p75 * .5) / (mse_p75 * 1.5 - mse_p75 * .5 + 1e-9), 0, 1)
roc_bad = np.clip((roc_p25 * 1.5 - roc_) / (roc_p25 * 1.5 - roc_p25 * .1 + 1e-9), 0, 1)
d_bad = np.clip(np.abs(dex - dexp_med) / (dexp_med * 2 + 1e-9), 0, 1)
score_b2 = 100.0 * (0.5 * mse_bad + 0.35 * roc_bad + 0.15 * d_bad)  # = 100 - health
thr_b2 = tune_threshold(y10[va], score_b2[va])
m = met_at(y10[te], score_b2[te], thr_b2)
repro["B2_fuzzy"] = m
log(f"  auditor: {m}")
log(f"  laporan : pr_auc={rep['baselines_temporal']['B2_legacy_fuzzy']['pr_auc']} "
    f"P={rep['baselines_temporal']['B2_legacy_fuzzy']['precision']} "
    f"R={rep['baselines_temporal']['B2_legacy_fuzzy']['recall']}")

# --------------------------------------------------------------- B2b
log("\n[REPRO B2b] aturan torque>P95 (ambang kuantil train, pilihan di val)")
raw = {"torque": ds["last_torque"].to_numpy(float),
       "wob": ds["last_wob"].to_numpy(float), "rop": ds["last_rop"].to_numpy(float)}
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
    f1v = f1_score(y10[va], r[va].astype(int), zero_division=0)
    if f1v > best_f1:
        best_name, best_f1, best_rule = name, float(f1v), r
p_te = best_rule[te].astype(int)
tp = int(((p_te == 1) & (y10[te] == 1)).sum()); fp = int(((p_te == 1) & (y10[te] == 0)).sum())
fn = int(((p_te == 0) & (y10[te] == 1)).sum())
b2b = dict(rule=best_name, val_f1=round(best_f1, 4),
           precision=round(tp / max(tp + fp, 1), 4), recall=round(tp / max(tp + fn, 1), 4),
           f1=round(2 * tp / max(2 * tp + fp + fn, 1), 4))
repro["B2b_aturan"] = b2b
log(f"  auditor: {b2b}")
log(f"  laporan : {rep['baselines_temporal']['B2b_aturan_fisika']['best_rule']} "
    f"valF1={rep['baselines_temporal']['B2b_aturan_fisika']['val_f1']} "
    f"test={rep['baselines_temporal']['B2b_aturan_fisika']['test']}")

# --------------------------------------------------------------- RF
for variant in ("with_md", "no_md"):
    log(f"\n[REPRO B3] RF {variant} (n_estimators=300, seed 42)")
    rf = RandomForestClassifier(**RF_PARAMS)
    rf.fit(X[variant][tr], y10[tr])
    s_va = rf.predict_proba(X[variant][va])[:, 1]
    s_te = rf.predict_proba(X[variant][te])[:, 1]
    thr = tune_threshold(y10[va], s_va)
    m = met_at(y10[te], s_te, thr)
    repro[f"RF_{variant}"] = m
    ref = rep["rf_temporal"][f"B3_RF_{variant}"]
    log(f"  auditor: {m}")
    log(f"  laporan: pr_auc={ref['pr_auc']} roc={ref['roc_auc']} P={ref['precision']} "
        f"R={ref['recall']} F1={ref['f1']} thr={ref['threshold']:.6f}")
    log(f"  delta PR-AUC |auditor-laporan| = {abs(m['pr_auc'] - ref['pr_auc']):.4f}")
    # subset analisis: apakah skor bertahan pada md yang TIDAK pernah terlihat di train?
    mdv = ds["md"].to_numpy(float)
    wname = ds["well"].to_numpy()
    rng_md = {}
    for w in np.unique(wname[tr]):
        rng_md[w] = (float(mdv[tr][wname[tr] == w].min()), float(mdv[tr][wname[tr] == w].max()))
    md_te = mdv[te]; w_te = wname[te]
    sub3 = {"md di dalam rentang train (sumur sama)": np.zeros(len(te), bool),
            "md di LUAR rentang train (sumur sama)": np.zeros(len(te), bool),
            "sumur TIDAK ada di train": np.zeros(len(te), bool)}
    for i, (w, v) in enumerate(zip(w_te, md_te)):
        if w not in rng_md:
            sub3["sumur TIDAK ada di train"][i] = True
        elif rng_md[w][0] <= v <= rng_md[w][1]:
            sub3["md di dalam rentang train (sumur sama)"][i] = True
        else:
            sub3["md di LUAR rentang train (sumur sama)"][i] = True
    for tag, msk in sub3.items():
        if msk.sum() == 0 or y10[te][msk].sum() == 0:
            log(f"    subset {tag}: n={int(msk.sum())} (tanpa positif -> dilewati)")
            continue
        log(f"    subset {tag}: n={int(msk.sum())} prev={y10[te][msk].mean():.4f} "
            f"PR-AUC={average_precision_score(y10[te][msk], s_te[msk]):.4f} "
            f"ROC={roc_auc_score(y10[te][msk], s_te[msk]):.4f}")

# --------------------------------------------------------------- CHECK 6
hdr("CHECK 6 — FAKE-ML: sensitivitas Delta (definisi jendela vs kemudahan tugas)")
rows = []
for D in DELTAS:
    yD = ds[f"y_{D}"].to_numpy(int)
    # struktur positif: blok kontigu per wellbore
    dsx = ds[["wellbore", "md", "row_id"]].copy(); dsx["y"] = yD
    n_blocks, lens_rows, lens_m = 0, [], []
    for wbg, g in dsx.groupby("wellbore", sort=False):
        g = g.sort_values("md")
        arr = g["y"].to_numpy(int)
        if arr.sum() == 0:
            continue
        diff = np.diff(np.concatenate(([0], arr, [0])))
        starts = np.where(diff == 1)[0]; ends = np.where(diff == -1)[0]
        n_blocks += len(starts)
        for s, e in zip(starts, ends):
            lens_rows.append(e - s)
            sub = g.iloc[s:e]
            lens_m.append(float(sub["md"].max() - sub["md"].min()))
    prev_all = float(yD.mean())
    prev_test = float(yD[te].mean())
    # baseline "selalu positif" F1
    p_all = np.ones(len(te), dtype=int)
    f1_all = f1_score(yD[te], p_all, zero_division=0)
    rf_ref = rep["delta_sensitivity"][str(D)]
    rows.append(dict(D=D, prev_all=round(prev_all, 5), prev_test=round(prev_test, 5),
                     n_pos=int(yD.sum()), n_blocks=n_blocks,
                     block_rows_med=float(np.median(lens_rows)) if lens_rows else 0,
                     block_m_med=float(np.median(lens_m)) if lens_m else 0,
                     f1_always_pos=round(float(f1_all), 4),
                     rf_pr_auc=rf_ref["pr_auc"], rf_lift=round(rf_ref["pr_auc"] / rf_ref["prevalence_test"], 3),
                     rf_f1=rf_ref["f1"]))
log("\n  Delta | prev_all | prev_test | n_pos | blok positif | blok med (baris/m) | "
    "F1 selalu-positif | RF PR-AUC | lift RF/prev")
for r in rows:
    log(f"  {r['D']:4d}m | {r['prev_all']*100:6.2f}% | {r['prev_test']*100:6.2f}% | {r['n_pos']:6d} | "
        f"{r['n_blocks']:5d} | {r['block_rows_med']:6.0f} / {r['block_m_med']:5.1f} m | "
        f"{r['f1_always_pos']:.3f} | {r['rf_pr_auc']:.4f} | {r['rf_lift']:.2f}x")

# aturan-if posisi-kedalaman tiap Delta (dari TRAIN) -> test PR-AUC
def depth_rule_score(delta):
    d = ds["md"].to_numpy(float)
    wbn = ds["wellbore"].to_numpy()
    yD = ds[f"y_{delta}"].to_numpy(int)
    ivs = []
    for wbname in np.unique(wbn[tr]):
        pos_md = np.sort(yD[tr][(wbn[tr] == wbname) & (yD[tr] == 1)] * 0 +
                         ds["md"].to_numpy(float)[tr][(wbn[tr] == wbname) & (yD[tr] == 1)])
        if pos_md.size == 0:
            continue
        start, prev_ = pos_md[0], pos_md[0]
        for v in pos_md[1:]:
            if v - prev_ <= delta + 1e-9:
                prev_ = v
            else:
                ivs.append((wbname, start, prev_)); start = v; prev_ = v
        ivs.append((wbname, start, prev_))
    score = np.zeros(len(te), dtype=float)
    de = d[te]; we = wbn[te]
    for wbname, a, b in ivs:
        msk = we == wbname
        if not msk.any():
            continue
        x = de[msk]
        dist = np.where(x < a, a - x, np.where(x > b, x - b, 0.0))
        score[msk] = np.maximum(score[msk], np.clip(1.0 - dist / delta, 0, 1))
    return score

log("\n  aturan-if POSISI-KEDALAMAN (interval dari TRAIN) vs RF, di test temporal:")
depth_res = {}
for D in DELTAS:
    yD = ds[f"y_{D}"].to_numpy(int)
    s = depth_rule_score(D)
    p = float(average_precision_score(yD[te], s))
    depth_res[D] = p
    rf_pr = rep["delta_sensitivity"][str(D)]["pr_auc"]
    log(f"    Delta {D:2d}m: aturan-kedalaman PR-AUC={p:.4f} | RF={rf_pr:.4f} "
        f"| prev={yD[te].mean():.4f} | aturan/prev={p/yD[te].mean():.2f}x RF/prev="
        f"{rf_pr/rep['delta_sensitivity'][str(D)]['prevalence_test']:.2f}x")

# --------------------------------------------------------------- ringkasan
hdr("RINGKASAN 32_audit_repro_delta")
diffs = {}
for k, v in repro.items():
    if k.startswith("RF_"):
        ref = rep["rf_temporal"]["B3_" + k.replace("RF_", "RF_")]
        ref = rep["rf_temporal"]["B3_" + ("RF_" + k[3:]) if False else "B3_RF_" + k[3:]]
    diffs[k] = v
log(json.dumps(repro, indent=2))
comp = {
    "B1_pr_auc_aud": repro["B1_logistik_MD"]["pr_auc"],
    "B1_pr_auc_rep": rep["baselines_temporal"]["B1_logistik_hanya_MD"]["pr_auc"],
    "B2_pr_auc_aud": repro["B2_fuzzy"]["pr_auc"],
    "B2_pr_auc_rep": rep["baselines_temporal"]["B2_legacy_fuzzy"]["pr_auc"],
    "B2b_rule_aud": repro["B2b_aturan"]["rule"],
    "B2b_rule_rep": rep["baselines_temporal"]["B2b_aturan_fisika"]["best_rule"],
    "B2b_f1_aud": repro["B2b_aturan"]["f1"],
    "B2b_f1_rep": rep["baselines_temporal"]["B2b_aturan_fisika"]["test"]["f1"],
    "RF_with_pr_auc_aud": repro["RF_with_md"]["pr_auc"],
    "RF_with_pr_auc_rep": rep["rf_temporal"]["B3_RF_with_md"]["pr_auc"],
    "RF_no_pr_auc_aud": repro["RF_no_md"]["pr_auc"],
    "RF_no_pr_auc_rep": rep["rf_temporal"]["B3_RF_no_md"]["pr_auc"],
}
ok_repro = (abs(comp["B1_pr_auc_aud"] - comp["B1_pr_auc_rep"]) <= 1e-4
            and abs(comp["B2_pr_auc_aud"] - comp["B2_pr_auc_rep"]) <= 1e-4
            and abs(comp["RF_with_pr_auc_aud"] - comp["RF_with_pr_auc_rep"]) <= 1e-4
            and abs(comp["RF_no_pr_auc_aud"] - comp["RF_no_pr_auc_rep"]) <= 1e-4
            and comp["B2b_rule_aud"] == comp["B2b_rule_rep"])
log(f"reproduksi identik (toleransi 1e-4)? {ok_repro}")
log(json.dumps(comp, indent=2))
log(f"\nDelta sensitivity: {json.dumps(rows, indent=2)}")
log(f"depth-rule per Delta: {depth_res}")

out = dict(repro=repro, comparison=comp, repro_ok=bool(ok_repro),
           delta=rows, depth_rule_pr_auc={str(k): v for k, v in depth_res.items()},
           runtime_s=round(time.time() - T0, 1))
(BASE / "docs" / "V2_ML_AUDIT_PART2.json").write_text(json.dumps(out, indent=2, ensure_ascii=False),
                                                       encoding="utf-8")
log(f"-> docs/V2_ML_AUDIT_PART2.json (runtime {out['runtime_s']}s)")
sys.exit(0)
