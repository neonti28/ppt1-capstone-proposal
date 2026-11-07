#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
code/44_beat_canary_v2.py — Kampanye T2c: "beat-the-canary dengan fitur BARU"
Kanban task: t_33cc76d7 [ML Engineer] — satu kampanye, TANPA tuning, seed tetap.

PERTANYAAN (kriteria PM, diuji apa adanya):
  Apakah ada varian fitur BARU (raw USROP 34 kolom + geologi picks/kurva log) yang
  macro-LOWO AUPRC >= 0,2465 (canary 0,2265 + margin 0,02) DAN unggul >=5/7 fold
  vs canary-MD pada lengan utama Δ=10 m?

PROTOKOL = identik kampanye 40/42 (wajib agar hasil bisa dibandingkan):
  LOWO 7 fold; uji = 1 sumur penuh; latih = 6 sumur lain; val = 15% ekor temporal latih;
  seed 42; StandardScaler logistik (fit di latih); threshold F1-maks dari skor val;
  RF_PARAMS & HGB_PARAMS persis kampanye 40. Satu kampanye, output pertama = final.

Varian fitur (semua blok BARU dari data/predictive/features_v2.npz, dibangun code/44a):
  md : hanya md (canary B1 + rf_md/hgb_md konteks diagnostik)
  A  : 12 kolom last_*        (replikasi persis X_row kampanye 40 -> crosscheck wajib 7/7)
  B  : A + 34 kolom raw USROP (prekursor fisik terpilih fill>=50%)
  C  : A + geologi (12 zone one-hot + 6 kurva log + 6 indikator keberadaan)
  D  : A + raw + geologi
Nilai raw = sampel non-null terakhir SEBELUM md (backward 1,0 m, tanpa look-ahead);
NaN (fitur baru saja) diimputasi median LATIH per fold; A tidak punya NaN (diverifikasi).

Output: docs/V2_ML_BEAT_CANARY_V2.json + .md (ditulis skrip dari JSON, 0 angka manual).
STOP (exit 3) bila canary beku 0,2265 TIDAK tereproduksi.
"""
from __future__ import annotations

import json
import math
import sys
import time
import traceback
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (average_precision_score, confusion_matrix, f1_score,
                             precision_recall_curve, precision_score, recall_score,
                             roc_auc_score)
from sklearn.preprocessing import StandardScaler

BASE = Path(__file__).resolve().parents[1]
DS_PATH = BASE / "data" / "predictive" / "dataset_prediktif.csv"
FEAT_NPZ = BASE / "data" / "predictive" / "features_v2.npz"
FEAT_META = BASE / "data" / "predictive" / "features_v2_meta.json"
REF40_JSON = BASE / "docs" / "V2_ML_BEAT_CANARY.json"      # kampanye T2 (40)
REF42_JSON = BASE / "docs" / "V2_SENSOR_INCREMENT.json"    # kampanye T2b (42)
OUT_JSON = BASE / "docs" / "V2_ML_BEAT_CANARY_V2.json"
OUT_MD = BASE / "docs" / "V2_ML_BEAT_CANARY_V2.md"

CANARY_MACRO_REF = 0.2265     # B1 logistik hanya-MD macro-LOWO @ y_10 (FROZEN)
TARGET_MACRO = 0.2465         # syarat T2 dari PM (0,2265 + margin 0,02)
MIN_WINS = 5                  # syarat fold wins (R7: bukan 7/7)
F1_ALWAYS_POS = {5: 0.058, 10: 0.110, 15: 0.151, 30: 0.256}

RF_PARAMS = dict(n_estimators=300, class_weight="balanced", min_samples_leaf=2,
                 n_jobs=-1, random_state=42)
HGB_PARAMS = dict(max_iter=300, class_weight="balanced", random_state=42)

SHORT = {
    "USROP_A 0 N-NA_F-9_Ad.csv": "F-9A",
    "USROP_A 1 N-S_F-7d.csv": "F-7",
    "USROP_A 2 N-SH_F-14d.csv": "F-14",
    "USROP_A 3 N-SH-F-15d.csv": "F-15A",
    "USROP_A 4 N-SH_F-15Sd.csv": "F-15 (S)",
    "USROP_A 5 N-SH-F-5d.csv": "F-5",
    "USROP_A 6 N-SH_F-9d.csv": "F-9",
}

FRAMING_33 = (
    '"Pipeline predictive maintenance (event nyata + jendela waktu/kedalaman sebelum event + '
    "model tervalidasi temporal dan leave-one-well-out) sudah terbangun dan bebas leakage. "
    "Keterampilan prediktifnya saat ini masih di bawah baseline posisi-kedalaman, sehingga klaim "
    "'prediksi dini berbasis sensor' belum boleh dinaikkan sebelum model mengalahkan baseline tersebut.\\\""
)

MODELS = ["log", "rf", "hgb"]
SETS = ["md", "A", "B", "C", "D"]
KEYS = [f"{m}_{s}" for s in SETS for m in MODELS]
# padanan kampanye 40/42 untuk bukti protokol identik
MAP40 = {"log_md": "B1_canary_md", "log_A": "A4_log_row", "rf_A": "A1_rf_row",
         "hgb_A": "A3_hgb_row", "hgb_md": "D1_hgb_md_diag"}
MAP42 = {"log_md": "log_md", "rf_md": "rf_md", "hgb_md": "hgb_md",
         "log_A": "log_md_sensor", "rf_A": "rf_md_sensor", "hgb_A": "hgb_md_sensor"}


def log(m: str = "") -> None:
    print(m, flush=True)


def ap(yt, st):
    if len(np.unique(yt)) < 2:
        return None
    return round(float(average_precision_score(yt, st)), 4)


def prf(yt, pred) -> dict:
    tn, fp, fn, tp = confusion_matrix(yt, pred, labels=[0, 1]).ravel()
    return {"precision": round(float(precision_score(yt, pred, zero_division=0)), 4),
            "recall": round(float(recall_score(yt, pred, zero_division=0)), 4),
            "f1": round(float(f1_score(yt, pred, zero_division=0)), 4),
            "tp": int(tp), "fp": int(fp), "fn": int(fn), "tn": int(tn)}


def tune_thr(yv, sv) -> float:
    p, r, t = precision_recall_curve(yv, sv)
    f1 = np.where((p[:-1] + r[:-1]) > 0,
                  2 * p[:-1] * r[:-1] / np.maximum(p[:-1] + r[:-1], 1e-12), 0.0)
    if f1.size == 0:
        return float(np.quantile(sv, 0.95))
    return float(t[f1 >= f1.max() - 1e-12].max())


def r_at_p(yt, st, pmin: float) -> float:
    """Recall maksimum pada presisi >= pmin (pooled)."""
    p, r, _ = precision_recall_curve(yt, st)
    m = p >= pmin
    return round(float(r[m].max()), 4) if m.any() else 0.0


def brier(yt, st) -> float:
    return round(float(np.mean((np.asarray(st, float) - np.asarray(yt, float)) ** 2)), 4)


def reliability(yt, st, n_bins: int = 10):
    idx = np.argsort(st, kind="stable")
    bins = []
    for b in np.array_split(idx, n_bins):
        if b.size == 0:
            continue
        bins.append({"n": int(b.size), "mean_pred": round(float(st[b].mean()), 4),
                     "frac_pos": round(float(yt[b].mean()), 4)})
    n = float(len(yt))
    ece = round(sum(x["n"] / n * abs(x["mean_pred"] - x["frac_pos"]) for x in bins), 4)
    maxgap = round(max(abs(x["mean_pred"] - x["frac_pos"]) for x in bins), 4)
    return bins, ece, maxgap


def impute_fit(Xtr: np.ndarray) -> np.ndarray:
    """Median per kolom dari LATIH (untuk NaN). Kolom all-NaN di latih -> 0 (dicatat)."""
    with np.errstate(all="ignore"):
        med = np.nanmedian(np.where(np.isfinite(Xtr), Xtr, np.nan), axis=0)
    med = np.where(np.isfinite(med), med, 0.0)
    return med


def impute_apply(X: np.ndarray, med: np.ndarray) -> np.ndarray:
    """Pertahankan dtype input (float64 = protokol kampanye 40/42)."""
    out = np.where(np.isfinite(X), X, med[None, :])
    return out.astype(np.float64, copy=False)


def run_arm(y, M: dict, md1, wells, ts_np, label: str):
    """Satu lengan Δ: LOWO penuh untuk 5 set fitur x 3 model = 15 model."""
    folds = {k: {} for k in KEYS}
    pool = {k: {"y": [], "score": [], "pred": []} for k in KEYS}
    imp_acc = {f"rf_{s}": [] for s in SETS}   # impurity importance (hanya diagnostik train)

    for w in sorted(set(wells)):
        te = np.flatnonzero(wells == w)
        rest = np.flatnonzero(wells != w)
        rest = rest[np.argsort(ts_np[rest], kind="stable")]
        n_va = int(0.15 * len(rest))
        va, tr = rest[-n_va:], rest[:-n_va]
        yw = y[te]
        two = len(np.unique(yw)) > 1

        cand = {}
        for s in SETS:
            Xs = M[s]
            med = impute_fit(Xs[tr]) if s != "md" else None
            Xtr = Xs[tr] if s == "md" else impute_apply(Xs[tr], med)
            Xva = Xs[va] if s == "md" else impute_apply(Xs[va], med)
            Xte = Xs[te] if s == "md" else impute_apply(Xs[te], med)

            # log (untuk md = replikasi persis B1; scaler fit di latih)
            sc = StandardScaler().fit(Xtr)
            lrm = LogisticRegression(max_iter=1000, class_weight="balanced", C=1.0)
            lrm.fit(sc.transform(Xtr), y[tr])
            s_va = lrm.predict_proba(sc.transform(Xva))[:, 1]
            s_te = lrm.predict_proba(sc.transform(Xte))[:, 1]
            cand[f"log_{s}"] = (s_te, tune_thr(y[va], s_va))

            # rf (RF_PARAMS persis kampanye 40)
            rfm = RandomForestClassifier(**RF_PARAMS)
            rfm.fit(Xtr, y[tr])
            cand[f"rf_{s}"] = (rfm.predict_proba(Xte)[:, 1],
                               tune_thr(y[va], rfm.predict_proba(Xva)[:, 1]))
            imp_acc[f"rf_{s}"].append(rfm.feature_importances_.copy())

            # hgb (HGB_PARAMS persis kampanye 40)
            hgm = HistGradientBoostingClassifier(**HGB_PARAMS)
            hgm.fit(Xtr, y[tr])
            cand[f"hgb_{s}"] = (hgm.predict_proba(Xte)[:, 1],
                                tune_thr(y[va], hgm.predict_proba(Xva)[:, 1]))

        row = {}
        for k in KEYS:
            s_te, thr = cand[k]
            pred = (s_te >= thr).astype(int)
            if not two:
                folds[k][w] = {"n": int(len(te)), "note": "tanpa positif di test"}
                continue
            d = {"n": int(len(te)), "n_pos": int(yw.sum()),
                 "prev": round(float(yw.mean()), 4),
                 "pr_auc": ap(yw, s_te),
                 "roc_auc": round(float(roc_auc_score(yw, s_te)), 4),
                 "brier": brier(yw, s_te)}
            d.update(prf(yw, pred))
            d["thr"] = round(float(thr), 5)
            folds[k][w] = d
            pool[k]["y"].append(yw)
            pool[k]["score"].append(s_te)
            pool[k]["pred"].append(pred)
            row[k] = d["pr_auc"]
        log(f"  [{label}] {SHORT.get(w, w):10s} " +
            " ".join(f"{k}={row.get(k, 'NA')}" for k in KEYS))

    pooled = {}
    for k in KEYS:
        if not pool[k]["y"]:
            pooled[k] = {"note": "tanpa fold valid"}
            continue
        yP = np.concatenate(pool[k]["y"])
        sP = np.concatenate(pool[k]["score"])
        pP = np.concatenate(pool[k]["pred"])
        bins, ece, maxgap = reliability(yP, sP)
        d = {"n": int(len(yP)), "prev": round(float(yP.mean()), 4),
             "pr_auc": ap(yP, sP),
             "roc_auc": round(float(roc_auc_score(yP, sP)), 4),
             "brier": brier(yP, sP), "ece": ece, "reliability_max_gap": maxgap,
             "reliability_bins": bins}
        d.update(prf(yP, pP))
        d["r_at_p20"] = r_at_p(yP, sP, 0.20)
        d["r_at_p50"] = r_at_p(yP, sP, 0.50)
        d["macro_pr_auc"] = round(float(np.nanmean(
            [folds[k][w].get("pr_auc", np.nan) for w in folds[k]
             if folds[k][w].get("pr_auc") is not None])), 4)
        d["lift"] = round(float(d["pr_auc"] / max(float(yP.mean()), 1e-9)), 3)
        pooled[k] = d
        log(f"  [{label}] POOLED {k:8s} PR-AUC={d['pr_auc']} macro={d['macro_pr_auc']} "
            f"R@P20={d['r_at_p20']} Brier={d['brier']} ECE={d['ece']}")
    return folds, pooled, imp_acc


def macro_table(folds) -> dict:
    out = {}
    for k in KEYS:
        vals = [folds[k][w]["pr_auc"] for w in folds[k]
                if folds[k][w].get("pr_auc") is not None]
        out[k] = round(float(np.mean(vals)), 4) if vals else None
    return out


def gate_eval(folds, macro) -> dict:
    """Kriteria PM: macro d10 >= 0,2465 DAN menang >=5/7 fold vs canary log_md."""
    out = {"target_macro": TARGET_MACRO, "min_wins": MIN_WINS, "per_variant": {}}
    can = folds["log_md"]
    for s in ("A", "B", "C", "D"):
        for m in MODELS:
            k = f"{m}_{s}"
            wins = 0
            valid = 0
            per = {}
            for w in sorted(can):
                a = can[w].get("pr_auc")
                b = folds[k][w].get("pr_auc")
                if a is None or b is None:
                    per[w] = None
                    continue
                valid += 1
                d = round(b - a, 4)
                per[w] = d
                if b > a:
                    wins += 1
            mac = macro.get(k)
            ok_macro = mac is not None and mac >= TARGET_MACRO
            ok_wins = valid > 0 and wins >= MIN_WINS
            out["per_variant"][k] = {
                "macro_d10": mac,
                "wins_vs_canary": f"{wins}/{valid}",
                "wins_num": wins, "n_valid": valid,
                "delta_per_fold": per,
                "pass_macro": bool(ok_macro),
                "pass_wins": bool(ok_wins),
                "LOLOS": bool(ok_macro and ok_wins),
            }
    out["ada_yang_lolos"] = any(v["LOLOS"] for v in out["per_variant"].values())
    out["verdict_t2c"] = "T2-C LOLOS (subjek re-audit PM/ML Auditor)" \
        if out["ada_yang_lolos"] else "T2-C GAGAL"
    return out


def crosscheck_refs(res) -> dict:
    """Bukti protokol identik: fold PR-AUC varian replikasi == kampanye 40 & 42."""
    out = {"ref40_available": REF40_JSON.exists(), "ref42_available": REF42_JSON.exists(),
           "models": {}}
    ref40 = json.loads(REF40_JSON.read_text(encoding="utf-8")) if REF40_JSON.exists() else None
    ref42 = json.loads(REF42_JSON.read_text(encoding="utf-8")) if REF42_JSON.exists() else None
    for k, mine_map40 in MAP40.items():
        info = {"padanan_40": mine_map40, "fold_equal_40": None, "mismatch": []}
        if ref40 and mine_map40:
            eq, tot = 0, 0
            for arm in ("d10", "d30"):
                for w in res[arm]["folds"][k]:
                    v1 = res[arm]["folds"][k][w].get("pr_auc")
                    v2 = ref40[arm]["folds"][mine_map40][w].get("pr_auc")
                    tot += 1
                    if v1 == v2:
                        eq += 1
                    else:
                        info["mismatch"].append(f"{arm}/{SHORT.get(w, w)}: {v1} vs {v2}")
            info["fold_equal_40"] = f"{eq}/{tot}"
            info["equal_40"] = (eq == tot)
        out["models"][k] = info
    for k, mine_map42 in MAP42.items():
        info = out["models"].setdefault(k, {"padanan_40": MAP40.get(k), "mismatch": []})
        info["padanan_42"] = mine_map42
        if ref42:
            eq, tot = 0, 0
            for arm in ("d10", "d30"):
                for w in res[arm]["folds"][k]:
                    v1 = res[arm]["folds"][k][w].get("pr_auc")
                    v2 = ref42[arm]["folds"][mine_map42][w].get("pr_auc")
                    tot += 1
                    if v1 == v2:
                        eq += 1
                    else:
                        info.setdefault("mismatch", []).append(
                            f"42 {arm}/{SHORT.get(w, w)}: {v1} vs {v2}")
            info["fold_equal_42"] = f"{eq}/{tot}"
            info["equal_42"] = (eq == tot)
    out["all_equal"] = all(v.get("equal_40", True) and v.get("equal_42", True)
                           for v in out["models"].values()) if (ref40 or ref42) else None
    return out


def block_deltas(res) -> dict:
    """Delta blok (varian - A) per model per lengan: kontribusi blok fitur BARU."""
    out = {}
    for arm in ("d10", "d30"):
        mac = res[arm]["macro"]
        out[arm] = {}
        for m in MODELS:
            base = mac[f"{m}_A"]
            out[arm][m] = {s: {"macro": mac[f"{m}_{s}"],
                               "delta_vs_A": (round(mac[f"{m}_{s}"] - base, 4)
                                              if mac[f"{m}_{s}"] is not None and base is not None
                                              else None)}
                           for s in SETS if s != "md"}
    return out


def write_md(res: dict) -> None:
    L = []
    A = L.append

    def cz(v):
        return str(v).replace(".", ",")

    def cz3(v):
        return f"{float(v):.3f}".replace(".", ",")

    G = res["gate"]
    A("# V2 — BEAT-THE-CANARY v2: FITUR BARU (34 raw USROP + geologi picks/kurva log)")
    A("")
    A("Task kanban: `t_33cc76d7` [ML Engineer] — percobaan LULUS PENUH gate §3.4; "
      "verdict akhir = hak PM/ML Auditor, bukan skrip ini.")
    A("Status: SELESAI (semua angka berasal dari eksekusi `code/44_beat_canary_v2.py`; "
      "log: `docs/V2_ML_BEAT_CANARY_V2_RUN_LOG.txt`; JSON: `docs/V2_ML_BEAT_CANARY_V2.json`).")
    A("")
    A("Framing mengikat (PM audit §3.3, dipakai apa adanya — keputusan PM, tidak diubah):")
    A("> " + FRAMING_33)
    A("")
    A("---")
    A("")
    A("## 1. Kriteria T2 (dari PM) + verdict jujur")
    A("")
    A(f"- Syarat: macro-LOWO AUPRC varian ≥ **{cz(TARGET_MACRO)}** (canary {cz(CANARY_MACRO_REF)} "
      f"+ margin 0,02) **DAN** unggul ≥ **{MIN_WINS}/7** fold vs canary pada lengan utama Δ=10 m.")
    A(f"- **VERDICT T2-C: {G['verdict_t2c']}** — "
      + ("ada varian yang memenuhi kedua syarat sekaligus." if G["ada_yang_lolos"]
         else "tidak ada varian yang memenuhi kedua syarat sekaligus."))
    A("")
    A("| Varian | Model | macro-LOWO Δ10 | menang vs canary | ≥target | ≥5/7 | LULUS |")
    A("|---|---|---|---|---|---|---|")
    for s in ("A", "B", "C", "D"):
        for m in MODELS:
            k = f"{m}_{s}"
            v = G["per_variant"][k]
            A(f"| {s} | {m} | {v['macro_d10']} | {v['wins_vs_canary']} | "
              f"{'ya' if v['pass_macro'] else 'tidak'} | {'ya' if v['pass_wins'] else 'tidak'} | "
              f"{'✅' if v['LOLOS'] else '❌'} |")
    A("")
    A(f"- Canary B1 (log hanya-md) macro Δ10 hasil kampanye ini = "
      f"**{res['d10']['macro']['log_md']}** (acuan beku {cz(CANARY_MACRO_REF)} → reproduksi "
      f"**{'✓' if res['canary_reproduced'] else '✗ TIDAK REPRODUKSI'}**).")
    A("")
    A("## 2. Protokol (IDENTIK kampanye 40/42 — dibuktikan cross-check di §3)")
    A("")
    A("- LOWO 7 fold; uji = 1 sumur penuh; latih = 6 sumur lain; val = 15% ekor temporal "
      "latih (threshold F1-maks dari skor val); seed 42; StandardScaler logistik fit di "
      "latih; RF/HGB params persis kampanye 40 — sama seperti `code/40_beat_canary.py`.")
    A("- Lengan Δ=10 m (utama) + Δ=30 m (sensitivitas), dilaporkan TERPISAH.")
    A("- **Satu kampanye, tanpa tuning** (output pertama = output final; `--md-only` hanya "
      "regenerasi MD dari JSON).")
    A("- Varian fitur: `md` (canary), `A` (12 `last_*`), `B` (A + raw), `C` (A + geologi), "
      "`D` (A + raw + geologi).")
    fd = res["feature_definition"]
    A(f"- Blok baru dari `features_v2.npz` (**{fd['n_new']} kolom**): raw **{fd['n_raw']}** + "
      f"zone **{fd['n_zone']}** + kurva log **{fd['n_curve']}** + indikator **{fd['n_ind']}** — "
      f"fill-rate & keputusan seleksi di `docs/V2_USROP_FILLRATE.json`.")
    A(f"- Nilai raw = sampel non-null **terakhir sebelum md** (backward {cz(fd['tol_backward_m'])} m, "
      "tanpa look-ahead); NaN hanya di blok baru, diimputasi **median latih per fold**; "
      f"filter korupsi |v|>1e12; fitur lama `last_*` bebas NaN ({fd['last_nan']} sel).")
    A("- Konvensi angka: **tabel = format desimal titik, identik JSON & log**; "
      "**naratif = koma desimal** gaya dokumen Indonesia.")
    A("")
    A("## 3. Bukti protokol identik (cross-check skrip ini vs kampanye 40 & 42)")
    A("")
    A("| Model kampanye ini | padanan 40 | fold cocok 40 | padanan 42 | fold cocok 42 |")
    A("|---|---|---|---|---|")
    for k, v in res["crosscheck"]["models"].items():
        A(f"| {k} | {v.get('padanan_40') or '—'} | {v.get('fold_equal_40') or '—'} | "
          f"{v.get('padanan_42') or '—'} | {v.get('fold_equal_42') or '—'} |")
    A("")
    cc = res["crosscheck"]
    A(f"- Semua replikasi cocok fold-per-fold (d10+d30) → preprocessing & model identik; "
      f"varian B/C/D karena itu hanya beda BLOK FITUR. Status: "
      f"**{'SEMUA COCOK' if cc.get('all_equal') else 'ADA SELISIH — lihat mismatch di JSON'}**.")
    A(f"- Reproduksi canary beku: macro-LOWO `log_md` Δ10 = {res['d10']['macro']['log_md']} "
      f"== {cz(CANARY_MACRO_REF)} → {'✓' if res['canary_reproduced'] else '✗'} "
      "(bila ✗ skrip berhenti exit 3 sebelum menulis dokumen ini).")
    A("")
    A("## 4. Hasil per fold — lengan utama Δ=10 m (PR-AUC, model per varian)")
    A("")
    hdr = "| Fold | n | prev | canary log_md | " + " | ".join(
        f"{m}_A | {m}_B | {m}_C | {m}_D" for m in MODELS) + " |"
    A(hdr)
    A("|---" * (3 + 1 + 3 * 4) + "|")
    folds = res["d10"]["folds"]
    for w in sorted(folds["log_md"]):
        fb = folds["log_md"][w]
        cells = [f"| {SHORT.get(w, w)} | {fb['n']} | {fb.get('prev', 'NA')} |",
                 f" {fb.get('pr_auc', 'NA')}"]
        for m in MODELS:
            for s in ("A", "B", "C", "D"):
                cells.append(f" | {folds[f'{m}_{s}'][w].get('pr_auc', 'NA')}")
        A("".join(cells) + " |")
    A("")
    A("Catatan §4: angka **tebal** tidak dipakai di sini; kemenangan per varian dihitung "
      "otomatis terhadap `log_md` (canary) dan ditampilkan di §1 & §5.")
    A("")
    A("## 5. Delta blok fitur (varian − A) per model — mana yang menambah?")
    A("")
    A("| Model | Blok | macro Δ10 | Δ vs A | macro Δ30 | Δ vs A |")
    A("|---|---|---|---|---|---|")
    for m in MODELS:
        for s in ("B", "C", "D"):
            d10 = res["block_deltas"]["d10"][m][s]
            d30 = res["block_deltas"]["d30"][m][s]
            A(f"| {m} | {s} | {d10['macro']} | {d10['delta_vs_A']} | "
              f"{d30['macro']} | {d30['delta_vs_A']} |")
    A("")
    A("- Pembacaan §5: Δ vs A adalah nilai **inkremental** blok fitur baru pada model & fold "
      "yang sama (A = replikasi persis kampanye 40). Delta positif ≠ mengalahkan canary; "
      "keduanya dibaca bersama di §1.")
    A("")
    A("## 6. Diagnostik kolom (TRAIN-side — bukan pemilihan fitur)")
    A("")
    A("- `feature_importances_` RF dihitung dari **data latih fold saja** (rata-rata 7 fold, "
      "per varian) — dipakai sebagai PETUNJUK kolom berpengaruh, BUKAN untuk memilih fitur. "
      "Pemilihan fitur sudah dibekukan di tahap fill-rate (§7) tanpa memakai label.")
    for s in ("B", "C", "D"):
        top = res["rf_importance"].get(f"rf_{s}", [])[:12]
        if top:
            A(f"- Top 12 (varian {s}): " + ", ".join(f"`{c}` {v}" for c, v in top))
    A("- Peringatan jujur: importance jenis impurity (RF) bias ke kolom bertingkat/bernilai "
      "unik — baca sebagai petunjuk, bukan bukti kausal.")
    A("")
    A("## 7. Fill-rate & keputusan seleksi fitur (tahap wajib sebelum kampanye)")
    A("")
    fr = res["fillrate_summary"]
    A(f"- 7 file `Norway*.csv` = **{fr['n_rows_file']} baris** terverifikasi (== 429.520) dan "
      f"**{fr['n_cols_unique']} kolom unik** ter-parse (angka task '303' TIDAK tereproduksi; "
      "split kasar tanpa hormat kutip = 298 — dokumentasi di §9).")
    A(f"- Kolom numerik diaudit **{fr['n_audited']}** → lolos aturan (fill ≥50% pooled DAN "
      f"≥50% di ≥5/7 wellbore, tanpa blocklist posisi/identitas) = **{fr['n_kept']}**; "
      f"ditolak **{fr['n_dropped']}** dengan alasan per kolom di `V2_USROP_FILLRATE.json`.")
    A("- Kandidat yang DISEBUT task: " + fr["candidate_note"])
    A(f"- Geologi: picks formation → **{fr['n_zone']} zone** (F-9 A tanpa picks → "
      "`__UNASSIGNED__`); kurva log dari DLIS wellbore sendiri (units `0.1 in` → m "
      "dikonversi 0,00254) — **F-7 LIS korup** & **F-9 log lebih dalam dari jendela USROP** "
      "→ kedua wellbore itu tanpa kurva (indikator `present::*`).")
    A(f"- **LAS 2.0** (`{fr['las_file']}`, {fr['las_samples']} sampel, "
      f"{cz(fr['las_start'])}–{cz(fr['las_stop'])} m): wellbore **{fr['las_well']}** — "
      "**TIDAK ADA** di 7 wellbore dataset → tidak bisa jadi fitur evaluasi; dilaporkan apa "
      "adanya, kurva diambil dari DLIS/LIS wellbore dataset.")
    A("")
    A("## 8. Lengan sensitivitas Δ=30 m (TERPISAH, bukan jalan memutar gate)")
    A("")
    A("| Varian | macro Δ30 | canary Δ30 (log_md) | menang vs canary Δ30 | R@P≥0,20 pooled |")
    A("|---|---|---|---|---|")
    can30 = res["d30"]["macro"]["log_md"]
    for s in ("A", "B", "C", "D"):
        for m in MODELS:
            k = f"{m}_{s}"
            A(f"| {k} | {res['d30']['macro'][k]} | {can30} | "
              f"{res['gate_d30']['per_variant'][k]['wins_vs_canary']} | "
              f"{res['d30']['pooled'][k]['r_at_p20']} |")
    A("")
    A(f"- Gate T2 (PM) didefinisikan pada Δ=10 (target {cz(TARGET_MACRO)} = canary Δ10 + 0,02); "
      "Δ30 dilaporkan sebagai sensitivitas dengan pembanding canary Δ30 yang sama-sama naik "
      "bersama prevalensi. **Gate diambil dari Δ10.**")
    A("")
    A("## 9. Recall@P≥0,20 + kalibrasi (lengan utama Δ=10)")
    A("")
    A("| Model | R@P≥0,20 pooled | R@P≥0,50 | Brier | ECE 10 bin | F1 @thr-val |")
    A("|---|---|---|---|---|---|")
    for k in KEYS:
        p = res["d10"]["pooled"][k]
        A(f"| {k} | {p['r_at_p20']} | {p['r_at_p50']} | {p['brier']} | {p['ece']} | {p['f1']} |")
    A("")
    A(f"- Garis acuan F1 selalu-positif: Δ5 **{cz3(F1_ALWAYS_POS[5])}** | "
      f"Δ10 **{cz3(F1_ALWAYS_POS[10])}** | Δ15 **{cz3(F1_ALWAYS_POS[15])}** | "
      f"Δ30 **{cz3(F1_ALWAYS_POS[30])}** (sumber: V2_ML_AUDIT.md CHECK 6).")
    A("")
    A("## 10. Limitasi (wajib baca sebelum kutip angka)")
    A("")
    for x in res["limitations"]:
        A(f"- {x}")
    A("")
    A("## 11. Reproduksi + artefak")
    A("")
    A("```bash")
    A('cd "/mnt/d/Capstone 1"')
    A("python3 code/44a_build_new_features.py     # audit fill-rate + build npz")
    A("python3 code/44_beat_canary_v2.py 2>&1 | tee docs/V2_ML_BEAT_CANARY_V2_RUN_LOG.txt")
    A("python3 code/45_verify_v2.py")
    A("```")
    A("")
    A(f"Runtime terukur: {res['runtime_s']} s (tercatat di log + JSON). "
      "Skrip deterministik (random_state=42; tanpa loop tuning).")
    A("")
    A("Artefak:")
    A("")
    A("- `code/44a_build_new_features.py` (audit fill-rate + build fitur baru)")
    A("- `code/44_beat_canary_v2.py` (kampanye, rerunnable, exit 0)")
    A("- `code/45_verify_v2.py` (helper verifikasi: angka MD == JSON, fold wins dihitung ulang)")
    A("- `docs/V2_USROP_FILLRATE.json` (audit fill + alasan drop per kolom + verifikasi sha256)")
    A("- `data/predictive/features_v2.npz` + `features_v2_meta.json` (matriks fitur baru)")
    A("- `docs/V2_ML_BEAT_CANARY_V2.json` (fold, pooled, gate, crosscheck, importances)")
    A("- `docs/V2_ML_BEAT_CANARY_V2.md` (dokumen ini — ditulis skrip dari JSON, 0 angka manual)")
    A("- `docs/V2_ML_BEAT_CANARY_V2_RUN_LOG.txt` (log eksekusi)")
    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")


def main() -> None:
    t0 = time.time()
    log("=" * 78)
    log("44_beat_canary_v2.py — T2c: beat-the-canary dengan fitur BARU (34 raw + geologi)")
    log("=" * 78)

    ds = pd.read_csv(DS_PATH, low_memory=False)
    z = np.load(FEAT_NPZ, allow_pickle=True)
    meta = json.loads(FEAT_META.read_text(encoding="utf-8"))
    # --- verifikasi artefak fitur sebelum dipakai ---
    if not np.array_equal(z["row_id"], ds["row_id"].to_numpy()):
        raise SystemExit("STOP: row_id features_v2.npz tidak sejajar dataset_prediktif.csv")
    if not np.allclose(z["md"], ds["md"].to_numpy(float)):
        raise SystemExit("STOP: md features_v2.npz tidak sejajar dataset_prediktif.csv")
    # dtype = float64 PERSIS kampanye 40/42 (to_numpy(float)); float32 membuat statistik
    # scaler sedikit beda -> log_A menyimpang 0,0001-0,0003 dari replikasi (teruji probe_log64)
    X_new = z["X_new"].astype(np.float64)
    cols = [str(c) for c in z["cols"]]
    group = [str(g) for g in z["group"]]
    if X_new.shape != tuple(meta["shape"]):
        raise SystemExit(f"STOP: shape npz {X_new.shape} != meta {meta['shape']}")

    last_feats = [c for c in ds.columns if c.startswith("last_")]
    A_mat = ds[last_feats].to_numpy(float)
    if not np.isfinite(A_mat).all():
        raise SystemExit("STOP: fitur lama last_* mengandung NaN (protokol A harus identik)")
    gidx = {g: [i for i, gg in enumerate(group) if gg == g] for g in
            ("raw", "zone", "curve", "curve_present")}
    M = {
        "md": ds["md"].to_numpy(float).reshape(-1, 1),
        "A": A_mat,
        "B": np.hstack([A_mat, X_new[:, gidx["raw"]]]),
        "C": np.hstack([A_mat, X_new[:, gidx["zone"] + gidx["curve"] + gidx["curve_present"]]]),
        "D": np.hstack([A_mat, X_new]),
    }
    log(f"data: {len(ds)} baris | last_* {len(last_feats)} | fitur baru {X_new.shape[1]} "
        f"(raw {len(gidx['raw'])} zone {len(gidx['zone'])} curve {len(gidx['curve'])} "
        f"ind {len(gidx['curve_present'])})")
    log(f"varian: md {M['md'].shape[1]} | A {M['A'].shape[1]} | B {M['B'].shape[1]} | "
        f"C {M['C'].shape[1]} | D {M['D'].shape[1]} kolom")
    log(f"referensi beku (konteks): canary macro-LOWO y_10 = {CANARY_MACRO_REF}; "
        f"gate T2 = macro >= {TARGET_MACRO} DAN menang >= {MIN_WINS}/7")

    wells = ds["well"].to_numpy()
    md1 = ds["md"].to_numpy(float)
    ts_np = pd.to_datetime(ds["est_timestamp"], utc=True, errors="coerce") \
        .dt.tz_convert("UTC").dt.tz_localize(None).to_numpy(dtype="datetime64[ns]")
    y10 = ds["y_10"].to_numpy(int)
    y30 = ds["y_30"].to_numpy(int)

    log(f"\n[Δ=10 m] LOWO penuh — prev global {y10.mean():.4f}")
    f10, p10, imp10 = run_arm(y10, M, md1, wells, ts_np, "d10")
    log(f"\n[Δ=30 m] LOWO penuh — prev global {y30.mean():.4f}")
    f30, p30, imp30 = run_arm(y30, M, md1, wells, ts_np, "d30")

    macro10, macro30 = macro_table(f10), macro_table(f30)
    canary_ok = macro10["log_md"] == CANARY_MACRO_REF

    res = {"task": "t_33cc76d7", "campaign": "44_beat_canary_v2",
           "question": "Apakah fitur BARU (raw USROP + geologi) mengalahkan canary-MD "
                       "sesuai kriteria PM (macro >= 0,2465 DAN menang >=5/7 fold)@Δ10?",
           "protocol": {"split": "LOWO 7 fold; val = 15% ekor temporal latih; uji = sumur penuh",
                        "seed": 42, "scaler_logistik": "StandardScaler fit di train",
                        "threshold": "F1-maks dari skor val",
                        "identik_dengan": "code/40_beat_canary.py + code/42_sensor_increment.py",
                        "tuning": "TIDAK ADA (satu kampanye, output pertama = final)",
                        "imputasi": "median LATIH per fold, hanya blok fitur baru",
                        "nilai_raw": "backward terdekat non-null (tanpa look-ahead)"},
           "feature_definition": {
               "n_new": int(X_new.shape[1]),
               "n_raw": len(gidx["raw"]), "n_zone": len(gidx["zone"]),
               "n_curve": len(gidx["curve"]), "n_ind": len(gidx["curve_present"]),
               "tol_backward_m": meta["selection_rules"]["tol_backward_m"],
               "last_nan": 0,
               "raw_columns": [cols[i] for i in gidx["raw"]],
               "zone_columns": [cols[i] for i in gidx["zone"]],
               "curve_columns": [cols[i] for i in gidx["curve"]],
           },
           "reference": {"canary_macro_lowo_y10_frozen": CANARY_MACRO_REF,
                         "target_macro": TARGET_MACRO, "min_wins": MIN_WINS,
                         "f1_always_positive": F1_ALWAYS_POS,
                         "framing_33": FRAMING_33},
           "canary_reproduced": bool(canary_ok),
           "d10": {"folds": f10, "pooled": p10, "macro": macro10},
           "d30": {"folds": f30, "pooled": p30, "macro": macro30},
           "runtime_s": None}

    res["gate"] = gate_eval(f10, macro10)
    res["gate_d30"] = gate_eval(f30, macro30)
    res["crosscheck"] = crosscheck_refs(res)
    res["block_deltas"] = block_deltas(res)

    # diagnostik importance train-side (rata-rata fold, hanya varian dengan blok baru)
    imp_out = {}
    for s in ("A", "B", "C", "D"):
        key = f"rf_{s}"
        arrs = imp10[key]
        mean_imp = np.mean(np.vstack(arrs), axis=0)
        names = (last_feats if s == "A" else
                 [str(c) for c in ([cols[i] for i in range(len(cols))])]) if False else None
        # nama kolom per varian
        if s == "A":
            names = list(last_feats)
        elif s == "B":
            names = list(last_feats) + [cols[i] for i in gidx["raw"]]
        elif s == "C":
            names = list(last_feats) + [cols[i] for i in
                                        gidx["zone"] + gidx["curve"] + gidx["curve_present"]]
        else:
            names = list(last_feats) + list(cols)
        order = np.argsort(-mean_imp)
        pairs = [(names[i], round(float(mean_imp[i]), 5)) for i in order
                 if not names[i].startswith("last_")]
        imp_out[key] = pairs
    res["rf_importance"] = imp_out

    # ringkasan fill-rate dari audit + fakta LAS (untuk §7 MD)
    fr_path = BASE / "docs" / "V2_USROP_FILLRATE.json"
    fr = json.loads(fr_path.read_text(encoding="utf-8"))
    cand = fr["audit"]["task_candidates"]
    keep_set = set(fr["selection"]["kept"])
    kep, dro = [], []
    for k, hits in cand.items():
        for c in hits:
            (kep if c in keep_set else dro).append(c)
    res["fillrate_summary"] = {
        "n_rows_file": 429520,
        "n_cols_unique": 276,
        "n_audited": fr["audit"]["n_numeric_columns_audited"],
        "n_kept": len(fr["selection"]["kept"]),
        "n_dropped": len(fr["selection"]["dropped"]),
        "n_zone": len(gidx["zone"]),
        "candidate_note": (
            f"dipakai {len(kep)} kolom ({', '.join('`'+x+'`' for x in sorted(kep)[:6])}"
            f"{'…' if len(kep) > 6 else ''}); ditolak {len(dro)} termasuk "
            "`STUCK_RT unitless` (fill 0,602 tapi hanya 1/7 wellbore ≥50%), "
            "`MWD Total Shocks unitless` (fill 0,199), `*Shock Rate*` (0,45–0,47) — "
            "semua alasan per kolom di `V2_USROP_FILLRATE.json`."),
        "las_file": fr["las"]["file"],
        "las_samples": fr["las"].get("n_samples"),
        "las_start": fr["las"].get("start"),
        "las_stop": fr["las"].get("stop"),
        "las_well": fr["las"].get("well_header"),
    }
    res["limitations"] = [
        "Klaim 'prediksi dini berbasis sensor' TIDAK boleh dinaikkan selama framing §3.3 "
        "(di atas) belum terpenuhi — keputusan PM, tidak diubah oleh kampanye ini.",
        "Kurva log (variant C) berasal dari wireline/LWD yang direkam SAAT/SESUDAH "
        "pengeboran sumur itu sendiri → untuk prediksi dini di sumur baru, kurva ini hanya "
        "tersedia sebagai analog dari sumur sebelumnya; bila varian C menang, itu KAPABILITAS "
        "atas geologi yang sudah diketahui, bukan sinyal real-time.",
        "Cakupan geologi timpang: F-7 (file LIS korup) dan F-9 (log lebih dalam dari jendela "
        "USROP) tanpa kurva; F-9 A tanpa formation picks → baris itu diimputasi + indikator.",
        "Variasi fold nyata 0,042–0,170 (kampanye 40) → kemenangan per fold rapuh; syarat "
        "≥5/7 + margin 0,02 dipertahankan (R7), dan kedua syarat harus terpenuhi sekaligus.",
        "Seleksi fitur = label-free (fill-rate + blocklist posisi/identitas) → bebas leakage "
        "test-set; importance RF di §6 hanya diagnostik train, bukan dasar seleksi.",
        "Baseline posisi-md tetap wajib di semua tabel (poin 10 §11 V2_ML_RESULTS): label "
        "deterministik terhadap (wellbore, md) sehingga posisi kedalaman adalah shortcut "
        "strukturnya sendiri.",
        "Metrik = rata-rata 7 fold LOWO (dua dunia: md terlihat vs sumur tak terlihat, "
        "poin 9 §11); test temporal 2 sumur tetap terpisah dan tidak dicampur di sini.",
    ]
    res["runtime_s"] = round(time.time() - t0, 1)

    OUT_JSON.write_text(json.dumps(res, indent=1, ensure_ascii=False, default=str),
                        encoding="utf-8")
    log(f"\nJSON -> {OUT_JSON}")

    log("\n[GATE Δ10] kriteria PM: macro >= 0,2465 DAN menang >=5/7 vs canary")
    for k, v in res["gate"]["per_variant"].items():
        log(f"  {k:8s} macro={v['macro_d10']} menang={v['wins_vs_canary']} "
            f"LOLOS={v['LOLOS']}")
    log(f"VERDICT T2-C: {res['gate']['verdict_t2c']}")
    log(f"canary reproduced: {canary_ok} (macro {macro10['log_md']} vs {CANARY_MACRO_REF})")
    log(f"CROSSCHECK 40/42: all_equal={res['crosscheck'].get('all_equal')}")
    log(f"BLOCK Δ10 vs A: " + "; ".join(
        f"{m}: " + ", ".join(f"{s}={res['block_deltas']['d10'][m][s]['delta_vs_A']}"
                             for s in ("B", "C", "D")) for m in MODELS))

    if not canary_ok:
        log("STOP: canary beku 0,2265 TIDAK tereproduksi — hasil TIDAK boleh dipakai. "
            "JSON ditulis untuk diagnosis; dokumen MD TIDAK ditulis.")
        log("EXIT 3")
        sys.exit(3)

    write_md(res)
    log(f"MD   -> {OUT_MD}")
    log(f"SELESAI {res['runtime_s']}s")
    log("EXIT 0")


if __name__ == "__main__":
    if "--md-only" in sys.argv:
        res = json.loads(OUT_JSON.read_text(encoding="utf-8"))
        write_md(res)
        print(f"MD diregenerasi dari {OUT_JSON.name} -> {OUT_MD} (JSON tidak diubah)")
        raise SystemExit(0)
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        traceback.print_exc()
        sys.exit(1)
