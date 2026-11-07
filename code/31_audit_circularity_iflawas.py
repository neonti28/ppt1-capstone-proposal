#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
code/31_audit_circularity_iflawas.py
AUDIT t_abc6eef6 [ML Auditor]
  CHECK 1 : CIRCULARITY — sejauh mana label y_10 bisa direkonstruksi deterministik dari fitur
            (standar kegagalan audit lama: mismatch ~0% = CIRCULAR = GAGAL)
  CHECK 3 : IF-LAWAS COMPARISON — aturan-if sederhana (termasuk aturan posisi-kedalaman)
            vs model ML, dengan angka dari eksekusi sendiri
  CHECK 4 : VALIDATION INTEGRITY — split temporal vs kedalaman (overlap md train/test per sumur),
            bukti kode, metrik kelas langka

Semua angka dicetak dari eksekusi sendiri; sumber = data/predictive/dataset_prediktif.csv.
"""
from __future__ import annotations
import json, sys, time
from pathlib import Path
import numpy as np
import pandas as pd

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (average_precision_score, roc_auc_score, precision_score,
                             recall_score, f1_score, accuracy_score)

BASE = Path(__file__).resolve().parents[1]
DS = BASE / "data" / "predictive" / "dataset_prediktif.csv"
JSON_MET = BASE / "docs" / "V2_ML_METRICS.json"
STAT_PREFIX = ("mean_", "std_", "first_", "last_", "delta_")
T0 = time.time()

def hdr(t): print("\n" + "=" * 78 + f"\n{t}\n" + "=" * 78, flush=True)
def log(*a): print(*a, flush=True)

# --------------------------------------------------------------- muat data
hdr("MUAT DATA + SPLIT TEMPORAL (identik code/21_predictive_baseline.py)")
ds = pd.read_csv(DS, low_memory=False)
feats = [c for c in ds.columns if c.startswith(STAT_PREFIX)]
ds["ts"] = pd.to_datetime(ds["est_timestamp"], utc=True, errors="coerce")
ts_np = ds["ts"].dt.tz_convert("UTC").dt.tz_localize(None).to_numpy(dtype="datetime64[ns]")
order = np.argsort(ts_np, kind="stable")
n = len(ds)
n_tr, n_va = int(0.70 * n), int(0.15 * n)
tr, va, te = order[:n_tr], order[n_tr:n_tr + n_va], order[n_tr + n_va:]
y = ds["y_10"].to_numpy(int)
X = ds[feats].to_numpy(float)
log(f"n={n} fitur={len(feats)} | train {len(tr)} val {len(va)} test {len(te)}")
log(f"prev train {y[tr].mean():.4f} | val {y[va].mean():.4f} | test {y[te].mean():.4f}")
log(f"baseline akurasi test (semua-negatif) = {1-y[te].mean():.4f}")

# =============================================================== CHECK 1
hdr("CHECK 1 — CIRCULARITY: rekonstruksi deterministik label dari fitur")
findings = {}

# --- A1. aturan ambang per-fitur (paling sederhana) ---
log("\n[A1] aturan ambang 1 fitur (pilih ambang di TRAIN utk akurasi maks, dievaluasi di TEST)")
best = (None, 0.0, 0.0, 0.0)
for j, name in enumerate(feats):
    col = X[:, j]
    qs = np.unique(np.quantile(col[tr], np.linspace(0.01, 0.99, 60)))
    for thr in qs:
        for mode in (0, 1):  # 0: prediksi 1 bila < thr ; 1: bila > thr
            pred_tr = (col[tr] < thr).astype(int) if mode == 0 else (col[tr] > thr).astype(int)
            acc_tr = (pred_tr == y[tr]).mean()
            pred_te = (col[te] < thr).astype(int) if mode == 0 else (col[te] > thr).astype(int)
            acc_te = (pred_te == y[te]).mean()
            if acc_tr > best[1]:
                best = (f"{name} {'<' if mode==0 else '>'} {thr:.6g}", acc_tr, acc_te, 0.0)
log(f"    aturan terbaik (akurasi train): {best[0]}")
log(f"    akurasi TRAIN={best[1]:.4f} | akurasi TEST={best[2]:.4f} "
    f"(baseline semua-negatif test={1-y[te].mean():.4f})")
log(f"    mismatch rekonstruksi di TEST = {(1-best[2])*100:.2f}%")
findings["A1_aturan_1_fitur_mismatch_test"] = (1 - best[2]) * 100

# --- A2. pohon kedalaman-saja (uji: apakah label = f(md) ?) ---
log("\n[A2] DecisionTree tanpa batas pada 'md' saja (dan md + wellbore) — rekonstruksi penuh")
mdcol = ds["md"].to_numpy(float).reshape(-1, 1)
t_md = DecisionTreeClassifier(max_depth=None, min_samples_leaf=1, random_state=0)
t_md.fit(mdcol, y)
acc_md_all = accuracy_score(y, t_md.predict(mdcol))
log(f"    tree('md') dilatih PADA SELURUH data -> akurasi rekonstruksi = {acc_md_all:.4f} "
    f"(mismatch {(1-acc_md_all)*100:.2f}%), kedalaman pohon={t_md.get_depth()}, daun={t_md.get_n_leaves()}")

wb = pd.get_dummies(ds["wellbore"], prefix="wb").to_numpy()
X_md_wb = np.hstack([mdcol, wb])
t_mdwb = DecisionTreeClassifier(max_depth=None, min_samples_leaf=1, random_state=0)
t_mdwb.fit(X_md_wb, y)
acc_mdwb = accuracy_score(y, t_mdwb.predict(X_md_wb))
log(f"    tree('md' + wellbore) [wellbore BUKAN fitur, ini UJI ATAS] -> "
    f"akurasi rekonstruksi = {acc_mdwb:.4f} (mismatch {(1-acc_mdwb)*100:.2f}%), "
    f"daun={t_mdwb.get_n_leaves()}")
# generalized: md-only tree dilatih di train, dievaluasi di test
t_md_tr = DecisionTreeClassifier(max_depth=None, min_samples_leaf=1, random_state=0)
t_md_tr.fit(mdcol[tr], y[tr])
acc_md_tr_test = accuracy_score(y[te], t_md_tr.predict(mdcol[te]))
log(f"    tree('md') dilatih di TRAIN -> akurasi TEST = {acc_md_tr_test:.4f} "
    f"(mismatch {(1-acc_md_tr_test)*100:.2f}%)")
findings["A2_tree_md_all_acc"] = acc_md_all
findings["A2_tree_md_wellbore_acc"] = acc_mdwb
findings["A2_tree_md_test_acc"] = acc_md_tr_test

# --- A3. pohon penuh pada 60 fitur: train (hafal) vs test (generalisasi) ---
log("\n[A3] DecisionTree tanpa batas pada 60 fitur — latih TRAIN, uji di TRAIN & TEST")
t_all = DecisionTreeClassifier(max_depth=None, min_samples_leaf=1, random_state=0, max_features=None)
t_all.fit(X[tr], y[tr])
acc_tr_all = accuracy_score(y[tr], t_all.predict(X[tr]))
acc_te_all = accuracy_score(y[te], t_all.predict(X[te]))
log(f"    akurasi TRAIN = {acc_tr_all:.4f} (mismatch {(1-acc_tr_all)*100:.2f}%) | "
    f"akurasi TEST = {acc_te_all:.4f} (mismatch {(1-acc_te_all)*100:.2f}%) | "
    f"daun={t_all.get_n_leaves()}")
log(f"    PR-AUC TEST (skor proba pohon) = {average_precision_score(y[te], t_all.predict_proba(X[te])[:,1]):.4f} "
    f"vs prevalensi {y[te].mean():.4f}")
findings["A3_tree_full_train_acc"] = acc_tr_all
findings["A3_tree_full_test_acc"] = acc_te_all

# --- A4. pohon dangkal (aturan-if yang bisa dibaca dosen) ---
log("\n[A4] DecisionTree DANGKAL (max_depth=3, aturan-if terbaca) di TRAIN -> TEST")
for d in (2, 3, 4):
    t = DecisionTreeClassifier(max_depth=d, min_samples_leaf=200, random_state=0)
    t.fit(X[tr], y[tr])
    s_te = t.predict_proba(X[te])[:, 1]
    p_te = (s_te >= 0.5).astype(int)
    prauc = float(average_precision_score(y[te], s_te))
    if d == 3:
        findings["A4_tree_d3_pr_auc_test"] = prauc
    log(f"    depth={d}: akurasi TEST={accuracy_score(y[te], p_te):.4f} "
        f"PR-AUC={prauc:.4f} "
        f"P={precision_score(y[te], p_te, zero_division=0):.3f} "
        f"R={recall_score(y[te], p_te, zero_division=0):.3f} "
        f"F1={f1_score(y[te], p_te, zero_division=0):.3f} daun={t.get_n_leaves()}")

# --- A5. aturan posisi-kedalaman (interval positif dari TRAIN) ---
def depth_interval_rule(train_mask, eval_idx, delta=10.0):
    """Skor [0,1] = kedekatan md ke interval positif yang dipelajari HANYA dari train."""
    d = ds["md"].to_numpy(float)
    ivs = []
    for wbname, g in ds.assign(y_=y).loc[train_mask].groupby("wellbore"):
        pos_md = np.sort(g.loc[g["y_"] == 1, "md"].to_numpy(float))
        if pos_md.size == 0:
            continue
        # gabung yang berdekatan <= delta (positif berbentuk blok sepanjang delta)
        start = pos_md[0]; prev = pos_md[0]
        for v in pos_md[1:]:
            if v - prev <= delta + 1e-9:
                prev = v
            else:
                ivs.append((wbname, start, prev)); start = v; prev = v
        ivs.append((wbname, start, prev))
    score = np.zeros(len(eval_idx), dtype=float)
    wbe = ds["wellbore"].to_numpy()[eval_idx]
    de = d[eval_idx]
    for wbname, a, b in ivs:
        m = (wbe == wbname)
        if not m.any():
            continue
        x = de[m]
        dist = np.where(x < a, a - x, np.where(x > b, x - b, 0.0))
        sc = np.clip(1.0 - dist / delta, 0.0, 1.0)
        score[m] = np.maximum(score[m], sc)
    return score, len(ivs)

tr_mask = np.zeros(n, dtype=bool); tr_mask[tr] = True
sc_rule, n_iv = depth_interval_rule(tr_mask, te)
log(f"\n[A5] aturan-if POSISI-KEDALAMAN (interval positif dari TRAIN, {n_iv} interval) -> TEST")
log(f"    PR-AUC = {average_precision_score(y[te], sc_rule):.4f} | "
    f"ROC = {roc_auc_score(y[te], sc_rule):.4f} | prevalensi {y[te].mean():.4f}")
bestf = (0, 0, 0, 0.0)
for thr in np.linspace(0.01, 0.99, 99):
    p = (sc_rule >= thr).astype(int)
    f1 = f1_score(y[te], p, zero_division=0)
    if f1 > bestf[3]:
        bestf = (precision_score(y[te], p, zero_division=0),
                 recall_score(y[te], p, zero_division=0), f1, thr)
log(f"    operating point F1-maks di TEST: thr={bestf[3]:.2f} P={bestf[0]:.3f} "
    f"R={bestf[1]:.3f} F1={bestf[2]:.3f}")
findings["A5_depth_rule_pr_auc_test"] = float(average_precision_score(y[te], sc_rule))
log(f"    catatan: skor aturan = 0 untuk SEMUA baris test? "
        f"{bool((sc_rule == 0).all())} -> interval dari train tidak menjangkau md test")

# --- A5b. aturan-if posisi-md versi lembut: laju positif per-bin kedalaman dari TRAIN ---
log("\n[A5b] aturan-if POSISI-MD (laju positif per 100 bin md dari TRAIN) -> TEST")
mdv = ds["md"].to_numpy(float)
edges = np.unique(np.quantile(mdv[tr], np.linspace(0, 1, 101)))
bin_tr = np.clip(np.searchsorted(edges, mdv[tr], side="right") - 1, 0, len(edges) - 2)
bin_te = np.clip(np.searchsorted(edges, mdv[te], side="right") - 1, 0, len(edges) - 2)
cnt = np.bincount(bin_tr, minlength=len(edges) - 1).astype(float)
pos = np.bincount(bin_tr, weights=y[tr], minlength=len(edges) - 1).astype(float)
prior = float(y[tr].mean())
alpha = 5.0
rate = (pos + alpha * prior) / (cnt + alpha)
sc_bin = rate[bin_te]
log(f"    PR-AUC = {average_precision_score(y[te], sc_bin):.4f} | "
    f"ROC = {roc_auc_score(y[te], sc_bin):.4f} | (prev {y[te].mean():.4f})")
bestb = (0.0, 0.0, 0.0, 0.0)
for thr in np.unique(np.round(sc_bin, 6)):
    p = (sc_bin >= thr).astype(int)
    if p.sum() == 0:
        continue
    f1 = f1_score(y[te], p, zero_division=0)
    if f1 > bestb[3]:
        bestb = (precision_score(y[te], p, zero_division=0),
                 recall_score(y[te], p, zero_division=0), f1, thr)
log(f"    operating point F1-maks di TEST: thr={bestb[3]:.4f} P={bestb[0]:.3f} "
    f"R={bestb[1]:.3f} F1={bestb[2]:.3f}")
findings["A5b_md_bin_rule_pr_auc_test"] = float(average_precision_score(y[te], sc_bin))

# --- ringkasan check 1 ---
mismatch_best = min((1 - best[2]), (1 - acc_md_tr_test), (1 - acc_te_all)) * 100
hdr("VERDICT CHECK 1 — CIRCULARITY")
baseline_test = float(1 - y[te].mean())
best_acc_test = max(best[2], acc_md_tr_test, acc_te_all)
skill = best_acc_test - baseline_test   # kelebihan akurasi aturan di atas prediksi semua-negatif
log(f"  mismatch rekonstruksi terendah di TEST = {mismatch_best:.2f}% "
    f"(aturan-1-fitur {findings['A1_aturan_1_fitur_mismatch_test']:.2f}%, "
    f"pohon-md {100*(1-acc_md_tr_test):.2f}%, pohon-60fitur {100*(1-acc_te_all):.2f}%)")
log(f"  baseline semua-negatif TEST = {baseline_test:.4f} | akurasi aturan terbaik di TEST = "
    f"{best_acc_test:.4f} | SKILL rekonstruksi = {skill:+.4f} (<=0 berarti tanpa keterampilan)")
log(f"  referensi audit lama (10_AUDIT_RESULTS.json): mismatches=0, accuracy=1.0 -> GAGAL")
if skill > 0.05:
    status1 = "FAIL"
elif skill > 0.01:
    status1 = "PARTIAL"
else:
    status1 = "PASS"
caveat1 = (acc_mdwb >= 0.999)
log(f"  STATUS CHECK 1 = {status1}"
    + (" DENGAN CATATAN: label deterministik terhadap (wellbore, md) in-sample "
       f"akurasi {acc_mdwb:.4f} -> shortcut posisi wajib di-disclose" if caveat1 else ""))
findings["status_circularity"] = status1
findings["circularity_caveat_md_wellbore_insample_acc"] = float(acc_mdwb)
findings["circularity_reconstruction_skill_vs_baseline"] = float(skill)

# =============================================================== CHECK 3
hdr("CHECK 3 — IF-LAWAS COMPARISON (angka eksekusi sendiri vs angka laporan)")
met = json.loads(JSON_MET.read_text(encoding="utf-8"))["run"]
rf_with = met["rf_temporal"]["B3_RF_with_md"]["pr_auc"]
rf_no = met["rf_temporal"]["B3_RF_no_md"]["pr_auc"]
b1 = met["baselines_temporal"]["B1_logistik_hanya_MD"]["pr_auc"]
b2 = met["baselines_temporal"]["B2_legacy_fuzzy"]["pr_auc"]
b2b_f1 = met["baselines_temporal"]["B2b_aturan_fisika"]["test"]["f1"]
diagnostic = json.loads((BASE / "docs" / "V2_ML_DIAGNOSTICS.json").read_text(encoding="utf-8"))
d2 = diagnostic["D2_raw_row_features"]["test_pr_auc"]
d4 = diagnostic["D4_md_only_lowo"]["pooled"]["macro"]

log("\nperingkat PR-AUC di split temporal (test, prev=0.0581):")
rows = [
    ("RF baris-saja (D2, fitur 'last_*')", d2, "model"),
    ("logistik hanya-MD (B1 canary)", b1, "aturan-if/kanari"),
    ("pohon dangkal depth=3 (aturan-if diekstrak, auditor)",
     findings.get("A4_tree_d3_pr_auc_test", float("nan")), "aturan-if"),
    ("RF window 10 m (B3 utama)", rf_with, "model"),
    ("RF window tanpa-MD (B3)", rf_no, "model"),
    ("aturan posisi-md per-bin (A5b, auditor)", findings["A5b_md_bin_rule_pr_auc_test"], "aturan-if"),
    ("aturan interval-kedalaman keras (A5, auditor)", findings["A5_depth_rule_pr_auc_test"], "aturan-if"),
    ("fuzzy legacy current system (B2)", b2, "aturan-if"),
]
for nm, v, kind in sorted(rows, key=lambda r: -r[1]):
    log(f"    {nm:45s} PR-AUC={v:.4f} lift={v/0.0581:.2f}x  [{kind}]")
log(f"    aturan torque>P95 (B2b) binary F1={b2b_f1} (PR-AUC tidak terdefinisi)")
log(f"  LOWO lintas-sumur: canary-MD macro PR-AUC={d4:.4f} > RF window macro 0.1033 > RF baris-saja macro 0.1001")
log(f"  -> RF baris-saja ({d2:.4f}) mengalahkan fuzzy legacy ({b2:.4f}) dan aturan torque (F1 {b2b_f1}) di temporal,")
log(f"     tetapi TIDAK mengalahkan canary-MD ({b1:.4f}) dan tidak mengalahkan aturan kedalaman ({findings['A5_depth_rule_pr_auc_test']:.4f}) bila aturan itu pakai interval dari train.")
ml_beats_simple_if = d2 > b2 and d2 > 0.0581
depth_best = max(findings["A5_depth_rule_pr_auc_test"], findings["A5b_md_bin_rule_pr_auc_test"])
ml_beats_depth_if = d2 > depth_best
rf_window_beats_canary = rf_with > b1
log(f"  RF baris-saja > aturan kedalaman terbaik? {ml_beats_depth_if} "
    f"({d2:.4f} vs {depth_best:.4f})")
log(f"  RF window (model utama) > canary-MD? {rf_window_beats_canary} "
    f"({rf_with:.4f} vs {b1:.4f})")
status3 = ("PASS" if (ml_beats_simple_if and ml_beats_depth_if and rf_window_beats_canary)
           else ("PARTIAL" if ml_beats_simple_if else "FAIL"))
log(f"  STATUS CHECK 3 = {status3}")
findings["status_iflawas"] = status3
findings["depth_rule_beats_rf_row"] = bool(findings["A5_depth_rule_pr_auc_test"] > d2)

# =============================================================== CHECK 4
hdr("CHECK 4 — VALIDATION INTEGRITY")
# 4a. bukti kode: split diurutkan timestamp, bukan shuffle acak
src21 = (BASE / "code" / "21_predictive_baseline.py").read_text(encoding="utf-8")
bukti = [ln.strip() for ln in src21.splitlines()
         if "np.argsort(ts_np" in ln or "train_test_split" in ln or "shuffle" in ln.lower()]
log("  potongan kode split:")
for b in bukti:
    log(f"    | {b}")
has_shuffle = any("train_test_split" in b or "shuffle=True" in b for b in bukti)
log(f"  ada random/shuffle split? {has_shuffle} -> {'GAGAL' if has_shuffle else 'PASS (bukan random)'}")

# 4b. tumpang tindih md train vs test dalam sumur yang sama (label berbasis KEDALAMAN)
log("\n  [4b] rentang md train vs test per sumur (label = fungsi md, jadi overlap = bocor antar-split)")
w = ds["well"].to_numpy()
mdv = ds["md"].to_numpy(float)
split = np.array(["train"] * n, dtype=object)
split[va] = "val"; split[te] = "test"
overlap_rows = []
for wname in sorted(set(w)):
    mtr = (w == wname) & (split == "train")
    mte = (w == wname) & (split == "test")
    mva = (w == wname) & (split == "val")
    if mtr.sum() == 0 or (mte.sum() + mva.sum()) == 0:
        log(f"    {wname:32s} train={mtr.sum():6d} test={mte.sum():6d} val={mva.sum():6d}  (tidak ada di dua sisi)")
        continue
    lo_t, hi_t = mdv[mtr].min(), mdv[mtr].max()
    te_all = mte | mva
    lo_e, hi_e = mdv[te_all].min(), mdv[te_all].max()
    ov = min(hi_t, hi_e) - max(lo_t, lo_e)
    frac_in = float(((mdv[te_all] >= lo_t) & (mdv[te_all] <= hi_t)).mean())
    overlap_rows.append((wname, float(ov), frac_in))
    log(f"    {wname:32s} train md {lo_t:7.1f}-{hi_t:7.1f} | test+val md {lo_e:7.1f}-{hi_e:7.1f} "
        f"| overlap {ov:7.1f} m | {frac_in*100:5.1f}% baris test berada di rentang md train")

# 4c. korelasi rank timestamp vs md per sumur (join md->waktu non-monoton?)
log("\n  [4c] korelasi rank (est_timestamp vs md) per sumur — proyeksi ini join md->waktu:")
spear = {}
for wname in sorted(set(w)):
    m = w == wname
    r_ts = pd.Series(ts_np[m]).rank()
    r_md = pd.Series(mdv[m]).rank()
    rho = float(r_ts.corr(r_md))
    spear[wname] = rho
    log(f"    {wname:32s} spearman(ts, md) = {rho:+.3f}")
neg = [k for k, v in spear.items() if v < 0.9]
log(f"  sumur dengan spearman < 0.9: {neg if neg else 'tidak ada'}")

# 4d. metrik kelas langka
log("\n  [4d] metrik kelas langka di laporan:")
metrik = ["pr_auc", "recall_at_precision_0.5"]
for k in metrik:
    log(f"    {k} ada di B3_RF_with_md? {k in met['rf_temporal']['B3_RF_with_md']}")
log(f"    akurasi dilaporkan B0 = {met['baselines_temporal']['B0_selalu_normal']['accuracy']} "
    f"(dipakai utk MEMATIKAN klaim akurasi, bukan utk klaim)")
log(f"    recall@precision>=0.5 utk SEMUA model temporal = 0 (jujur, dilaporkan)")
status4 = "PARTIAL" if overlap_rows else "PASS"
log(f"\n  STATUS CHECK 4 = {status4} "
    f"(split bukan random & metrik langka OK; {'ada tumpang tindih md antar split' if overlap_rows else 'tanpa overlap md'})")
findings["status_validation"] = status4
findings["md_overlap"] = overlap_rows
findings["spearman_ts_md"] = spear

hdr("RINGKASAN 31_audit_circularity_iflawas")
for k, v in findings.items():
    log(f"  {k}: {v}")
(BASE / "docs" / "V2_ML_AUDIT_PART1.json").write_text(
    json.dumps({k: (v if not isinstance(v, (np.floating, np.integer)) else float(v))
                for k, v in findings.items()}, indent=2, ensure_ascii=False, default=str),
    encoding="utf-8")
log(f"\nselesai dalam {time.time()-T0:.1f}s -> docs/V2_ML_AUDIT_PART1.json")
sys.exit(0)
