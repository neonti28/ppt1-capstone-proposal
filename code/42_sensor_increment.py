#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
code/42_sensor_increment.py — Kampanye T2b: uji nilai INKREMENTAL fitur sensor di atas baseline md
Kanban task: t_b925f329 [ML Engineer] — nested/paired, SATU kampanye, TANPA tuning.

PERTANYAAN (BUKAN "kalahkan 0.2465" — gate T2 ditutup, R8 berlaku):
  APAKAH fitur sensor MENAMBAH nilai di atas model hanya-md, pada fold LOWO yang sama?
Ini nested/paired comparison — pertanyaan BERBEDA dari T2, bukan retry.
Kedua arah hasil DITERIMA; TIDAK ada target absolut.

Protokol IDENTIK dengan kampanye 40 (code/40_beat_canary.py):
  LOWO 7 fold; uji = 1 sumur penuh; latih = 6 sumur lain; val = 15% ekor temporal latih;
  seed 42; StandardScaler logistik (fit di latih); threshold F1-maks dari skor val.
Bukti kemiripan dieksekusi skrip ini sendiri: tiap model md+sensor diuji fold-ke-fold
  terhadap padanannya di JSON kampanye 40 (A1/A3/A4) dan B1/D1 (crosscheck_campaign40).

Definisi fitur (diukur, bukan asumsi — lihat feature_definition.diagnosis di JSON):
  md  = kolom `md` (baseline posisi-kedalaman, sama dgn kampanye 40).
  sensor = 12 kolom `last_*` (X_row kampanye 40). Kolom `last_md` TERBUKTI identik
  persis dgn `md` (diecek skrip ini), sehingga sisi "md+sensor" = [md + 11 sensor]
  dan delta murni berasal dari 11 kolom sensor non-permukaan (wob, spp, torque, rop,
  rpm, flow, mud_density, diameter, hookload, tvd, gamma).

Pasangan model (kelas sama, hyperparameter sama, beda hanya fitur):
  log : log_md (replikasi persis B1)        vs log_md_sensor  (replikasi persis A4)
  rf  : rf_md  (MODEL BARU, RF_PARAMS 40)   vs rf_md_sensor   (replikasi persis A1)
  hgb : hgb_md (replikasi persis D1)        vs hgb_md_sensor  (replikasi persis A3)

Per pasangan per lengan (Δ=10 utama, Δ=30 sensitivitas):
  delta PR-AUC per fold + macro delta + sign test eksak dua sisi (fold delta==0 dikeluarkan).
Verdict dijalankan ATURAN, bukan target:
  mayoritas fold delta<=0 (per pasangan) -> (i) "sensor tidak menambah nilai di atas
  posisi-kedalaman pada dataset ini"; selain itu -> (ii) delta>0 terbatas, besaran +
  batas klaimnya, TETAP bukan "beat the canary".

Kalibrasi (menutup PM audit §9 poin 10 — kalibrasi belum pernah diukur):
  Brier score pooled + rata-fold, ECE 10 bin setara-jumlah, gap bin maks, reliability
  10 bin lengkap per model per lengan (di JSON).

Output: docs/V2_SENSOR_INCREMENT.json + docs/V2_SENSOR_INCREMENT.md + stdout (tee ke log).
Semua angka di .md ditulis skrip dari dict hasil — 0 angka ketik-manual.
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
REF40_JSON = BASE / "docs" / "V2_ML_BEAT_CANARY.json"
OUT_JSON = BASE / "docs" / "V2_SENSOR_INCREMENT.json"
OUT_MD = BASE / "docs" / "V2_SENSOR_INCREMENT.md"

# Referensi beku (dokumentasi T1, V2_ML_RESULTS §5/§8 + V2_ML_AUDIT CHECK 6) — konteks/repro, BUKAN target
CANARY_MACRO_REF = 0.2265            # B1 logistik hanya-MD macro-LOWO @ y_10 (frozen)
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

# Framing mengikat PM audit §3.3 — dipakai VERBATIM (sama persis dgn code/40)
FRAMING_33 = (
    '"Pipeline predictive maintenance (event nyata + jendela waktu/kedalaman sebelum event + '
    "model tervalidasi temporal dan leave-one-well-out) sudah terbangun dan bebas leakage. "
    "Keterampilan prediktifnya saat ini masih di bawah baseline posisi-kedalaman, sehingga klaim "
    "'prediksi dini berbasis sensor' belum boleh dinaikkan sebelum model mengalahkan baseline tersebut.\""
)

MODELS = ["log_md", "log_md_sensor", "rf_md", "rf_md_sensor", "hgb_md", "hgb_md_sensor"]
PAIRS = {"log": ("log_md", "log_md_sensor"),
         "rf": ("rf_md", "rf_md_sensor"),
         "hgb": ("hgb_md", "hgb_md_sensor")}
# Padanan di kampanye 40 (untuk bukti "identik kampanye 40"; rf_md memang model baru)
MAP40 = {"log_md": "B1_canary_md", "log_md_sensor": "A4_log_row",
         "rf_md_sensor": "A1_rf_row", "hgb_md": "D1_hgb_md_diag",
         "hgb_md_sensor": "A3_hgb_row"}


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


def brier(yt, st) -> float:
    return round(float(np.mean((np.asarray(st, float) - np.asarray(yt, float)) ** 2)), 4)


def reliability(yt, st, n_bins: int = 10):
    """Reliability ringkas: bin setara-jumlah pada skor pooled. Return (bins, ece, maxgap)."""
    idx = np.argsort(st, kind="stable")
    bins = []
    for b in np.array_split(idx, n_bins):
        if b.size == 0:
            continue
        mp = round(float(st[b].mean()), 4)
        fp = round(float(yt[b].mean()), 4)
        bins.append({"n": int(b.size), "mean_pred": mp, "frac_pos": fp})
    n = float(len(yt))
    ece = round(sum(x["n"] / n * abs(x["mean_pred"] - x["frac_pos"]) for x in bins), 4)
    maxgap = round(max(abs(x["mean_pred"] - x["frac_pos"]) for x in bins), 4)
    return bins, ece, maxgap


def sign_test(wins: int, ties: int, losses: int):
    """Sign test eksak dua sisi (fold delta==0 = tie, dikeluarkan dari n)."""
    n = wins + losses
    if n == 0:
        return None, 0
    k = min(wins, losses)
    p = 2.0 * sum(math.comb(n, i) for i in range(k + 1)) / (2 ** n)
    return round(min(1.0, p), 4), n


def run_arm(y, X_row, md1, wells, ts_np, label: str):
    """Satu lengan Δ: LOWO penuh untuk 6 model (3 pasangan paired). Return (folds, pooled)."""
    folds = {m: {} for m in MODELS}
    pool = {m: {"y": [], "score": [], "pred": []} for m in MODELS}

    for w in sorted(set(wells)):
        te = np.flatnonzero(wells == w)
        rest = np.flatnonzero(wells != w)
        rest = rest[np.argsort(ts_np[rest], kind="stable")]
        n_va = int(0.15 * len(rest))
        va, tr = rest[-n_va:], rest[:-n_va]
        yw = y[te]
        two = len(np.unique(yw)) > 1

        md_tr = md1[tr].reshape(-1, 1)
        md_va = md1[va].reshape(-1, 1)
        md_te = md1[te].reshape(-1, 1)

        # log_md — replikasi persis B1 kampanye 40
        sc = StandardScaler().fit(md_tr)
        lrm = LogisticRegression(max_iter=1000, class_weight="balanced")
        lrm.fit(sc.transform(md_tr), y[tr])
        s_va = lrm.predict_proba(sc.transform(md_va))[:, 1]
        s_te = lrm.predict_proba(sc.transform(md_te))[:, 1]
        thr_m = tune_thr(y[va], s_va)

        # log_md_sensor — replikasi persis A4 kampanye 40 (scaler di X_row, C=1.0)
        scr = StandardScaler().fit(X_row[tr])
        lrs = LogisticRegression(max_iter=1000, class_weight="balanced", C=1.0)
        lrs.fit(scr.transform(X_row[tr]), y[tr])
        s_va_s = lrs.predict_proba(scr.transform(X_row[va]))[:, 1]
        s_te_s = lrs.predict_proba(scr.transform(X_row[te]))[:, 1]
        thr_s = tune_thr(y[va], s_va_s)

        # rf_md — MODEL BARU (params persis kampanye 40, hanya md)
        rfm = RandomForestClassifier(**RF_PARAMS)
        rfm.fit(md_tr, y[tr])
        s_va_rm = rfm.predict_proba(md_va)[:, 1]
        s_te_rm = rfm.predict_proba(md_te)[:, 1]
        thr_rm = tune_thr(y[va], s_va_rm)

        # rf_md_sensor — replikasi persis A1 kampanye 40
        rfs = RandomForestClassifier(**RF_PARAMS)
        rfs.fit(X_row[tr], y[tr])
        s_va_rs = rfs.predict_proba(X_row[va])[:, 1]
        s_te_rs = rfs.predict_proba(X_row[te])[:, 1]
        thr_rs = tune_thr(y[va], s_va_rs)

        # hgb_md — replikasi persis D1 kampanye 40
        hgm = HistGradientBoostingClassifier(**HGB_PARAMS)
        hgm.fit(md_tr, y[tr])
        s_va_hm = hgm.predict_proba(md_va)[:, 1]
        s_te_hm = hgm.predict_proba(md_te)[:, 1]
        thr_hm = tune_thr(y[va], s_va_hm)

        # hgb_md_sensor — replikasi persis A3 kampanye 40
        hgs = HistGradientBoostingClassifier(**HGB_PARAMS)
        hgs.fit(X_row[tr], y[tr])
        s_va_hs = hgs.predict_proba(X_row[va])[:, 1]
        s_te_hs = hgs.predict_proba(X_row[te])[:, 1]
        thr_hs = tune_thr(y[va], s_va_hs)

        cand = {"log_md": (s_te, thr_m), "log_md_sensor": (s_te_s, thr_s),
                "rf_md": (s_te_rm, thr_rm), "rf_md_sensor": (s_te_rs, thr_rs),
                "hgb_md": (s_te_hm, thr_hm), "hgb_md_sensor": (s_te_hs, thr_hs)}
        row = {}
        for m, (s_te_m, thr) in cand.items():
            pred = (s_te_m >= thr).astype(int)
            if not two:
                folds[m][w] = {"n": int(len(te)), "note": "tanpa positif di test"}
                continue
            d = {"n": int(len(te)), "n_pos": int(yw.sum()),
                 "prev": round(float(yw.mean()), 4),
                 "pr_auc": ap(yw, s_te_m),
                 "roc_auc": round(float(roc_auc_score(yw, s_te_m)), 4),
                 "brier": brier(yw, s_te_m)}
            d.update(prf(yw, pred))
            d["thr"] = round(float(thr), 5)
            folds[m][w] = d
            pool[m]["y"].append(yw)
            pool[m]["score"].append(s_te_m)
            pool[m]["pred"].append(pred)
            row[m] = d["pr_auc"]
        log(f"  [{label}] {SHORT.get(w, w):10s} " +
            " ".join(f"{m}={row.get(m, 'NA')}" for m in MODELS))

    pooled = {}
    for m in MODELS:
        if not pool[m]["y"]:
            pooled[m] = {"note": "tanpa fold valid"}
            continue
        yP = np.concatenate(pool[m]["y"])
        sP = np.concatenate(pool[m]["score"])
        pP = np.concatenate(pool[m]["pred"])
        bins, ece, maxgap = reliability(yP, sP)
        d = {"n": int(len(yP)), "prev": round(float(yP.mean()), 4),
             "pr_auc": ap(yP, sP),
             "roc_auc": round(float(roc_auc_score(yP, sP)), 4),
             "brier": brier(yP, sP),
             "ece": ece, "reliability_max_gap": maxgap,
             "reliability_bins": bins}
        d.update(prf(yP, pP))
        d["macro_pr_auc"] = round(float(np.nanmean(
            [folds[m][w].get("pr_auc", np.nan) for w in folds[m]
             if folds[m][w].get("pr_auc") is not None])), 4)
        d["brier_fold_mean"] = round(float(np.mean(
            [folds[m][w]["brier"] for w in folds[m] if "brier" in folds[m][w]])), 4)
        d["lift"] = round(float(d["pr_auc"] / max(float(yP.mean()), 1e-9)), 3)
        pooled[m] = d
        log(f"  [{label}] POOLED {m:15s} PR-AUC={d['pr_auc']} macro={d['macro_pr_auc']} "
            f"Brier={d['brier']} ECE={d['ece']} F1={d['f1']}")
    return folds, pooled


def analyze_delta(folds) -> dict:
    """Delta PR-AUC per fold + macro + sign test per pasangan. Aturan verdict TANPA target absolut."""
    out = {}
    for pair, (mo, ms) in PAIRS.items():
        per = {}
        deltas = []
        for w in sorted(folds[mo]):
            a = folds[mo][w].get("pr_auc")
            b = folds[ms][w].get("pr_auc")
            if a is None or b is None:
                per[w] = {"md_only": a, "md_sensor": b, "delta": None,
                          "note": "fold tanpa pr_auc (kelas tunggal di test)"}
                continue
            d = round(b - a, 4)
            per[w] = {"md_only": a, "md_sensor": b, "delta": d}
            deltas.append(d)
        n = len(deltas)
        wins = sum(1 for d in deltas if d > 0)
        ties = sum(1 for d in deltas if d == 0)
        losses = n - wins - ties
        p, n_sign = sign_test(wins, ties, losses)
        n_le0 = losses + ties
        majority = (n_le0 > n / 2) if n else None
        out[pair] = {
            "per_fold": per,
            "n_valid": n,
            "wins_delta_gt_0": wins,
            "ties_delta_eq_0": ties,
            "losses_delta_lt_0": losses,
            "n_delta_le_0": n_le0,
            "macro_md_only": round(float(np.mean([v["md_only"] for v in per.values()
                                                  if v["delta"] is not None])), 4) if n else None,
            "macro_md_sensor": round(float(np.mean([v["md_sensor"] for v in per.values()
                                                    if v["delta"] is not None])), 4) if n else None,
            "macro_delta": round(float(np.mean(deltas)), 4) if n else None,
            "mean_delta": round(float(np.mean(deltas)), 4) if n else None,
            "median_delta": round(float(np.median(deltas)), 4) if n else None,
            "min_delta": round(float(np.min(deltas)), 4) if n else None,
            "max_delta": round(float(np.max(deltas)), 4) if n else None,
            "sign_p_two_sided": p,
            "sign_n": n_sign,
            "majority_delta_le_0": majority,
            "verdict_pair": ("i_sensor_tidak_menambah_nilai" if majority
                             else "ii_delta_positif_terbatas") if majority is not None else "tidak_valid",
        }
    return out


def overall_verdict(delta: dict) -> tuple:
    per = {pair: delta[pair]["verdict_pair"] for pair in PAIRS}
    if all(v == "i_sensor_tidak_menambah_nilai" for v in per.values()):
        return "i_sensor_tidak_menambah_nilai_di_mayoritas_fold_semua_pasangan"
    return "ii_delta_positif_terbatas_di_sebagian_pasangan"


def crosscheck_40(res) -> dict:
    """Bukti empiris preprocessing identik: model md+sensor & replika md-only == kampanye 40."""
    out = {"ref_available": REF40_JSON.exists(), "models": {}, "all_equal": None,
           "rf_md": "MODEL BARU — tanpa padanan di kampanye 40 (memang tidak ada RF md-saja)"}
    if not out["ref_available"]:
        out["all_equal"] = None
        return out
    ref = json.loads(REF40_JSON.read_text(encoding="utf-8"))
    all_eq = True
    for mine, theirs in MAP40.items():
        info = {"padanan_40": theirs, "fold_equal": [], "pooled_equal": None,
                "macro_equal": None, "brier_dihitung_karena": "JSON kampanye 40 tidak menyimpan skor"}
        for arm in ("d10", "d30"):
            eq = 0
            tot = 0
            for w in res[arm]["folds"][mine]:
                v1 = res[arm]["folds"][mine][w].get("pr_auc")
                v2 = ref[arm]["folds"][theirs][w].get("pr_auc")
                tot += 1
                if v1 == v2:
                    eq += 1
                else:
                    info.setdefault("mismatch", []).append(f"{arm}/{SHORT.get(w, w)}: {v1} vs {v2}")
            info["fold_equal"].append(f"{arm} {eq}/{tot}")
            p1 = res[arm]["pooled"][mine]
            p2 = ref[arm]["pooled"][theirs]
            pe = p1["pr_auc"] == p2["pr_auc"]
            me = p1["macro_pr_auc"] == p2["macro_pr_auc"]
            info["pooled_equal"] = info["pooled_equal"] and pe if info["pooled_equal"] is not None else pe
            info["macro_equal"] = info["macro_equal"] and me if info["macro_equal"] is not None else me
            if not (pe and me):
                info.setdefault("mismatch", []).append(
                    f"{arm} pooled {p1['pr_auc']}/{p1['macro_pr_auc']} vs {p2['pr_auc']}/{p2['macro_pr_auc']}")
        ok = info.get("mismatch") is None and all(x.endswith("7/7") for x in info["fold_equal"])
        info["equal"] = ok
        all_eq = all_eq and ok
        out["models"][mine] = info
    out["all_equal"] = all_eq
    out["b1_frozen_macro_y10_0_2265"] = res["d10"]["pooled"]["log_md"]["macro_pr_auc"] == CANARY_MACRO_REF
    return out


def build_verdict(delta_by_arm) -> dict:
    v = {"rule": "per pasangan: mayoritas fold delta<=0 (delta<=0 count > n/2) -> (i); "
                 "selain itu -> (ii). Lengan utama d10 menentukan verdict keseluruhan; "
                 "d30 = sensitivitas. TANPA target absolut; kedua arah diterima.",
         "per_pair": {}}
    for arm, delta in delta_by_arm.items():
        v["per_pair"][arm] = {p: delta[p]["verdict_pair"] for p in PAIRS}
        v[f"overall_{arm}"] = overall_verdict(delta)
    return v


def stmt_i(delta_by_arm) -> str:
    d10 = delta_by_arm["d10"]
    bits = ", ".join(f"{p}: {d10[p]['n_delta_le_0']}/{d10[p]['n_valid']} fold delta<=0 "
                     f"(macro Δ={d10[p]['macro_delta']})" for p in PAIRS)
    return ("Kesimpulan (i): pada SEMUA 3 pasangan model, delta PR-AUC <= 0 di mayoritas "
            f"fold LOWO lengan utama Δ=10 m — {bits}. Kesimpulan: sensor TIDAK menambah "
            "nilai di atas posisi-kedalaman pada dataset ini. Klaim 'fitur sensor menambah "
            "nilai prediktif di atas baseline kedalaman' DITUTUP PERMANEN berdasarkan bukti "
            "ini (berlaku untuk dataset V2 ini, protokol LOWO ini, dan 3 kelas model yang "
            "diuji — BUKAN klaim universal lintas dataset).")


def stmt_ii(delta_by_arm) -> str:
    d10 = delta_by_arm["d10"]
    pos = [p for p in PAIRS if not d10[p]["majority_delta_le_0"]]
    bits = "; ".join(
        f"{p}: macro Δ={d10[p]['macro_delta']} (mean {d10[p]['mean_delta']}, "
        f"median {d10[p]['median_delta']}, rentang {d10[p]['min_delta']}..{d10[p]['max_delta']}), "
        f"menang {d10[p]['wins_delta_gt_0']}/{d10[p]['n_valid']}, "
        f"p uji-tanda {d10[p]['sign_p_two_sided']}" for p in pos)
    return ("Kesimpulan (ii): delta>0 TERBATAS pada pasangan " + ", ".join(pos) + " — " + bits +
            ". Batas klaim: ini delta INKREMENTAL pada fold yang sama, bukan klaim model "
            "mengalahkan baseline canary, dan TETAP bukan 'beat the canary' (gate T2 tetap "
            "tertutup — R8). Klaim 'prediksi dini berbasis sensor' TIDAK boleh dinaikkan "
            "(framing §3.3 di atas berlaku apa adanya).")


def write_md(res: dict) -> None:
    L = []
    A = L.append
    V = res["verdict"]
    D = {arm: res[arm]["delta"] for arm in ("d10", "d30")}

    def cz(v):
        """Angka gaya Indonesia (koma desimal) untuk naratif.
        Tabel = format titik, identik JSON/log → reproduksi 1-ke-1."""
        return str(v).replace(".", ",")

    def cz3(v):
        """Garis acuan F1: SELALU 3 desimal gaya Indonesia (cz(0.110) -> '0,11' = salah)."""
        return f"{float(v):.3f}".replace(".", ",")

    A("# V2 — UJI NILAI INKREMENTAL SENSOR DI ATAS BASELINE MD (nested/paired, LOWO)")
    A("")
    A("Task kanban: `t_b925f329` [ML Engineer] — T2b, pengganti T2 yang DITUTUP sebagai "
      "TIDAK TERCAPAI (PM audit §9.3, keputusan D1–D3).")
    A("Status: SELESAI (semua angka berasal dari eksekusi `code/42_sensor_increment.py`; "
      "log: `docs/V2_SENSOR_INCREMENT_RUN_LOG.txt`; JSON: `docs/V2_SENSOR_INCREMENT.json`).")
    A("")
    A("Pertanyaan task ini (BUKAN \"kalahkan 0,2465\"): APAKAH fitur sensor MENAMBAH nilai "
      "di atas model hanya-md, pada fold yang sama? Ini nested/paired comparison — "
      "pertanyaan BERBEDA dari T2, bukan retry. Satu kampanye, tanpa tuning; kedua arah "
      "hasil diterima.")
    A("")
    A("Framing mengikat (PM audit §3.3, dipakai apa adanya — keputusan PM, tidak diubah):")
    A("> " + FRAMING_33)
    A("")
    A("---")
    A("")
    A("## 1. Protokol (IDENTIK dengan kampanye 40)")
    A("")
    A("- LOWO 7 fold; uji = 1 sumur penuh; latih = 6 sumur lain; val = 15% ekor temporal "
      "latih (threshold F1-maks dari skor val); seed 42; scaler logistik fit di latih — "
      "persis `code/40_beat_canary.py`.")
    A("- Lengan Δ=10 m (utama) + Δ=30 m (sensitivitas), persis kampanye 40.")
    fd = res["feature_definition"]
    nrows_id = f"{fd['n_rows_checked']:,}".replace(",", ".")
    ns = fd["n_sensor_kolom"]
    A(f"- Definisi fitur (diukur, bukan asumsi): `last_md` TERBUKTI identik persis dengan "
      f"`md` pada {nrows_id} baris (max|md-last_md| = {fd['max_abs_diff']}); karena itu "
      f"sisi **md+sensor** = {ns} kolom `last_*` kampanye 40 = [md + {ns - 1} sensor] "
      f"(wob, spp, torque, rop, rpm, flow, mud_density, diameter, hookload, tvd, gamma) — "
      f"delta murni berasal dari {ns - 1} kolom sensor, bukan dari duplikasi md.")
    A("- Pasangan (kelas model & hyperparameter sama, beda HANYA fitur): "
      "`log_md` vs `log_md_sensor`, `rf_md` vs `rf_md_sensor`, `hgb_md` vs `hgb_md_sensor`.")
    A("- replika = kode disalin dari kampanye 40 (B1→`log_md`, A4→`log_md_sensor`, "
      "A1→`rf_md_sensor`, D1→`hgb_md`, A3→`hgb_md_sensor`); `rf_md` MODEL BARU "
      "(RF_PARAMS kampanye 40, input md saja).")
    A("- Konvensi angka: **tabel = format desimal titik, identik dengan JSON & log** "
      "(reproduksi 1-ke-1); **naratif = koma desimal** gaya dokumen Indonesia.")
    A("")
    A("## 2. Bukti \"identik kampanye 40\" (cross-check dieksekusi skrip ini)")
    A("")
    A("| Model kampanye ini | Padanan kampanye 40 | Fold PR-AUC cocok | Pooled cocok | Macro cocok |")
    A("|---|---|---|---|---|")
    for m in MODELS:
        if m in res["crosscheck_campaign40"]["models"]:
            c = res["crosscheck_campaign40"]["models"][m]
            A(f"| {m} | {c['padanan_40']} | {', '.join(c['fold_equal'])} | "
              f"{'ya' if c['pooled_equal'] else 'TIDAK'} | {'ya' if c['macro_equal'] else 'TIDAK'} |")
        else:
            A(f"| {m} | — | — | — | — |")
    A("")
    cc = res["crosscheck_campaign40"]
    if cc.get("all_equal"):
        A(f"- Semua pasangan cocok 7/7 fold di kedua lengan → replay protokol kampanye 40 "
          f"terbukti identik. Rekonfirmasi canary beku: macro-LOWO `log_md` = "
          f"{res['d10']['pooled']['log_md']['macro_pr_auc']} "
          f"({'== ' + cz(CANARY_MACRO_REF) + ' ✓' if cc.get('b1_frozen_macro_y10_0_2265') else 'TIDAK == ' + cz(CANARY_MACRO_REF) + ' ✗'}).")
    else:
        A("- PERHATIAN: ada selisih replay vs kampanye 40 — lihat `crosscheck_campaign40."
          "models.*.mismatch` di JSON. Jangan tafsirkan delta sebelum selisih ini dijelaskan.")
    A(f"- Catatan: JSON kampanye 40 TIDAK menyimpan skor prediksi, sehingga Brier/kalibrasi "
      f"TIDAK bisa dihitung dari data lama — itulah mengapa kampanye ini re-run penuh "
      f"(6 model x 7 fold x 2 lengan) dalam SATU kampanye tanpa tuning.")
    A(f"- {cc['rf_md']}.")
    A("")
    A("## 3. Delta PR-AUC per fold — lengan utama Δ=10 m")
    A("")
    A("| Fold | n | prev | log md | log md+sensor | Δ | rf md | rf md+sensor | Δ | hgb md | hgb md+sensor | Δ |")
    A("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for w in sorted(res["d10"]["folds"]["log_md"]):
        fb = res["d10"]["folds"]["log_md"][w]
        cells = [f"| {SHORT.get(w, w)} | {fb['n']} | {fb.get('prev', 'NA')} |"]
        for pair in ("log", "rf", "hgb"):
            mo, ms = PAIRS[pair]
            a = res["d10"]["folds"][mo][w].get("pr_auc", "NA")
            b = res["d10"]["folds"][ms][w].get("pr_auc", "NA")
            d = res["d10"]["delta"][pair]["per_fold"][w]["delta"]
            cells.append(f" {a} | {b} | {d if d is not None else 'NA'} |")
        A("".join(cells))
    A("")
    A("## 4. Delta PR-AUC per fold — lengan sensitivitas Δ=30 m")
    A("")
    A("| Fold | n | prev | log md | log md+sensor | Δ | rf md | rf md+sensor | Δ | hgb md | hgb md+sensor | Δ |")
    A("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for w in sorted(res["d30"]["folds"]["log_md"]):
        fb = res["d30"]["folds"]["log_md"][w]
        cells = [f"| {SHORT.get(w, w)} | {fb['n']} | {fb.get('prev', 'NA')} |"]
        for pair in ("log", "rf", "hgb"):
            mo, ms = PAIRS[pair]
            a = res["d30"]["folds"][mo][w].get("pr_auc", "NA")
            b = res["d30"]["folds"][ms][w].get("pr_auc", "NA")
            d = res["d30"]["delta"][pair]["per_fold"][w]["delta"]
            cells.append(f" {a} | {b} | {d if d is not None else 'NA'} |")
        A("".join(cells))
    A("")
    A("## 5. Ringkasan delta + sign test (dua arah diterima; tanpa target absolut)")
    A("")
    A("| Pasangan | Lengan | macro md-only | macro md+sensor | macro Δ | fold Δ>0 | fold Δ≤0 | n | p uji-tanda (dua sisi) | mayoritas Δ≤0 | verdict pasangan |")
    A("|---|---|---|---|---|---|---|---|---|---|---|")
    for arm in ("d10", "d30"):
        for pair in ("log", "rf", "hgb"):
            d = D[arm][pair]
            A(f"| {pair} | {arm} | {d['macro_md_only']} | {d['macro_md_sensor']} | "
              f"{d['macro_delta']} | {d['wins_delta_gt_0']} | {d['n_delta_le_0']} | "
              f"{d['n_valid']} | {d['sign_p_two_sided']} | "
              f"{'ya' if d['majority_delta_le_0'] else 'tidak'} | {d['verdict_pair']} |")
    A("")
    A("Legenda §5: uji-tanda eksak dua sisi pada fold dengan delta≠0 (tie dikeluarkan, "
      "kolom n = wins+losses). Aturan verdict: mayoritas fold delta≤0 → (i); selain itu → (ii). "
      "Tidak ada target absolut yang ditetapkan.")
    A("")
    A("## 6. Verdict jujur (dihitung aturan dari angka §5, bukan harapan)")
    A("")
    A(f"- Per pasangan Δ10: " + "; ".join(f"{p} → **{V['per_pair']['d10'][p]}**" for p in PAIRS) + ".")
    A(f"- Per pasangan Δ30: " + "; ".join(f"{p} → **{V['per_pair']['d30'][p]}**" for p in PAIRS) + ".")
    A(f"- **Verdict keseluruhan (lengan utama Δ=10): `{V['overall_d10']}`**; "
      f"lengan sensitivitas Δ=30: `{V['overall_d30']}`.")
    A("")
    A("> " + (stmt_i(D) if V["overall_d10"].startswith("i_") else stmt_ii(D)))
    A("")
    if V["overall_d30"] != V["overall_d10"]:
        A(f"- Catatan jujur: lengan sensitivitas Δ=30 memberi verdict berbeda "
          f"(`{V['overall_d30']}`) — keduanya dilaporkan apa adanya; verdict keseluruhan "
          f"mengikuti lengan utama Δ=10.")
        A("")
    A("## 7. Kalibrasi (menutup PM audit §9 poin 10 — kalibrasi belum pernah diukur)")
    A("")
    A("| Model | Lengan | Brier pooled (makin kecil makin baik) | ECE 10 bin | gap bin maks | Brier rata-fold |")
    A("|---|---|---|---|---|---|")
    for arm in ("d10", "d30"):
        for m in MODELS:
            p = res[arm]["pooled"][m]
            A(f"| {m} | {arm} | {p['brier']} | {p['ece']} | {p['reliability_max_gap']} | "
              f"{p['brier_fold_mean']} |")
    A("")
    for arm in ("d10", "d30"):
        bits = []
        for pair, (mo, ms) in PAIRS.items():
            bm = res[arm]["pooled"][mo]["brier"]
            bs = res[arm]["pooled"][ms]["brier"]
            bits.append(f"{pair}: {bm} → {bs} ({'lebih baik' if bs < bm else ('lebih buruk' if bs > bm else 'sama')})")
        A(f"- Δ={arm[1:]} m, Brier md-only → md+sensor: " + "; ".join(bits) + ".")
    A("- Reliability 10 bin lengkap per model per lengan ada di JSON "
      "(`pooled.*.reliability_bins`: n, mean_pred, frac_pos per bin).")
    A("- Baca jujur: Brier/ECE adalah kualitas probabilitas terkalibrasi, BUKAN diskriminasi — "
      "nilai Brier ikut dipengaruhi prevalensi, jadi perbandingan Brier hanya berlaku antar model "
      "pada lengan (prevalensi) yang sama.")
    A("")
    A("## 8. Garis acuan F1 \"selalu positif\" (wajib — acceptance b)")
    A("")
    A(f"- Δ5 **{cz3(F1_ALWAYS_POS[5])}** | Δ10 **{cz3(F1_ALWAYS_POS[10])}** | "
      f"Δ15 **{cz3(F1_ALWAYS_POS[15])}** | Δ30 **{cz3(F1_ALWAYS_POS[30])}** "
      "(F1 = 2·prev/(1+prev); sumber: V2_ML_AUDIT.md CHECK 6, log V2_ML_AUDIT_LOG_32.txt).")
    A(f"- Pooled Δ=10 (prev {res['d10']['pooled']['log_md']['prev']}): F1 "
      + ", ".join(f"{m} {res['d10']['pooled'][m]['f1']}" for m in MODELS)
      + f" — semua dibandingkan garis Δ10 {cz3(F1_ALWAYS_POS[10])}.")
    A(f"- Pooled Δ=30 (prev {res['d30']['pooled']['log_md']['prev']}): F1 "
      + ", ".join(f"{m} {res['d30']['pooled'][m]['f1']}" for m in MODELS)
      + f" — semua dibandingkan garis Δ30 {cz3(F1_ALWAYS_POS[30])}.")
    A("")
    A("## 9. Batas klaim (acceptance c/d)")
    A("")
    A("- **Kampanye ini TIDAK membuktikan model mengalahkan canary** dan TIDAK membuka "
      "kembali gate T2 (R8: iterasi model/hyperparameter dengan setup sama = retry tanpa "
      "adaptasi — tetap ditolak). Tidak ada target absolut (0,2465 tidak dipakai di sini).")
    A("- Delta inkremental ≠ keunggulan absolut: pasangan md+sensor bisa unggul atas "
      "md-only-nya sendiri sementara macro absolutnya tetap di bawah baseline canary — "
      "kedua pernyataan bisa serius bersamaan dan keduanya dilaporkan di §5–§6.")
    A("- Klaim 'prediksi dini berbasis sensor' TIDAK boleh dinaikkan selama framing §3.3 "
      "di atas belum terpenuhi (keputusan PM, tidak diubah).")
    A("- Batas cakupan: 1 dataset (V2), protokol LOWO ini, 3 kelas model, 2 lengan Δ — "
      "kesimpulan (i) berlaku di dalam batas itu saja.")
    A("")
    A("## 10. Reproduksi + artefak")
    A("")
    A("```bash")
    A("cd \"/mnt/d/Capstone 1\"")
    A("python3 code/42_sensor_increment.py 2>&1 | tee docs/V2_SENSOR_INCREMENT_RUN_LOG.txt")
    A("python3 code/43_verify_sensor_increment.py")
    A("```")
    A("")
    A(f"Runtime terukur: {res['runtime_s']} s (tercatat di log + JSON). "
      "Skrip deterministik (random_state=42; tanpa loop tuning; keluaran pertama = keluaran final).")
    A("")
    A("Artefak:")
    A("")
    A("- `code/42_sensor_increment.py` (kampanye, rerunnable, exit 0)")
    A("- `code/43_verify_sensor_increment.py` (helper verifikasi: angka MD == JSON)")
    A("- `docs/V2_SENSOR_INCREMENT.json` (fold, pooled, delta, verdict, kalibrasi)")
    A("- `docs/V2_SENSOR_INCREMENT.md` (dokumen ini — ditulis skrip dari JSON, 0 angka manual)")
    A("- `docs/V2_SENSOR_INCREMENT_RUN_LOG.txt` (log eksekusi)")
    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")


def main() -> None:
    t0 = time.time()
    log("=" * 78)
    log("42_sensor_increment.py — T2b: nilai inkremental sensor di atas baseline md (nested/paired)")
    log("=" * 78)
    ds = pd.read_csv(DS_PATH, low_memory=False)
    raw_feats = [c for c in ds.columns if c.startswith("last_")]
    wells = ds["well"].to_numpy()
    md1 = ds["md"].to_numpy(float)
    X_row = ds[raw_feats].to_numpy(float)
    ds["ts"] = pd.to_datetime(ds["est_timestamp"], utc=True, errors="coerce")
    ts_np = ds["ts"].dt.tz_convert("UTC").dt.tz_localize(None).to_numpy(dtype="datetime64[ns]")

    # Diagnosis definisi fitur (diukur, bukan asumsi)
    maxdiff = float(np.max(np.abs(ds["md"].to_numpy(float) - ds["last_md"].to_numpy(float))))
    feat_def = {"md": "md", "sensor_cols": raw_feats, "n_rows_checked": int(len(ds)),
                "max_abs_diff": maxdiff, "last_md_identik_md": bool(maxdiff == 0.0),
                "n_sensor_kolom": len(raw_feats),
                "catatan": (f"last_md identik persis dgn md -> sisi md+sensor = [md + "
                            f"{len(raw_feats) - 1} sensor]; delta murni dari "
                            f"{len(raw_feats) - 1} kolom sensor") if maxdiff == 0.0 else
                           ("last_md != md — baca catatan ini sebelum tafsir delta; "
                            "sisi md+sensor memakai X_row persis kampanye 40")}
    log(f"data: {len(ds)} baris | fitur last_* ({len(raw_feats)}): {raw_feats}")
    log(f"diagnosis last_md vs md: max|diff|={maxdiff} -> identik={feat_def['last_md_identik_md']}")
    log(f"referensi beku (konteks, BUKAN target): canary macro-LOWO y_10 = {CANARY_MACRO_REF}")
    log("PERTANYAAN: apakah fitur sensor menambah nilai di atas hanya-md pada fold sama? "
        "(tanpa target absolut; kedua arah diterima)")

    y10 = ds["y_10"].to_numpy(int)
    y30 = ds["y_30"].to_numpy(int)
    log(f"\n[Δ=10 m] LOWO penuh (lengan utama) — prev global {y10.mean():.4f}")
    folds10, pooled10 = run_arm(y10, X_row, md1, wells, ts_np, "d10")
    log(f"\n[Δ=30 m] LOWO penuh (lengan sensitivitas) — prev global {y30.mean():.4f}")
    folds30, pooled30 = run_arm(y30, X_row, md1, wells, ts_np, "d30")

    delta10 = analyze_delta(folds10)
    delta30 = analyze_delta(folds30)

    res = {"task": "t_b925f329", "campaign": "42_sensor_increment",
           "question": "Apakah fitur sensor MENAMBAH nilai di atas model hanya-md pada fold LOWO sama? "
                       "(nested/paired; BUKAN beat-the-canary; tanpa target absolut)",
           "protocol": {"split": "LOWO 7 fold; val = 15% ekor temporal latih; uji = sumur penuh",
                        "seed": 42, "scaler_logistik": "StandardScaler fit di train",
                        "threshold": "F1-maks dari skor val (tune_thr, persis kampanye 40)",
                        "identik_dengan": "code/40_beat_canary.py",
                        "tuning": "TIDAK ADA (satu kampanye, output pertama = output final)"},
           "feature_definition": feat_def,
           "models": {m: d for m, d in [
               ("log_md", "logistik hanya-md (replikasi persis B1 kampanye 40)"),
               ("log_md_sensor", "logistik md+sensor (replikasi persis A4)"),
               ("rf_md", "RF hanya-md (MODEL BARU, RF_PARAMS kampanye 40)"),
               ("rf_md_sensor", "RF md+sensor (replikasi persis A1)"),
               ("hgb_md", "HGB hanya-md (replikasi persis D1)"),
               ("hgb_md_sensor", "HGB md+sensor (replikasi persis A3)")]},
           "pairs": {k: list(v) for k, v in PAIRS.items()},
           "reference": {"f1_always_positive": F1_ALWAYS_POS,
                         "canary_macro_lowo_y10_frozen": CANARY_MACRO_REF,
                         "framing_33": FRAMING_33,
                         "catatan": "referensi konteks/repro; BUKAN target kampanye ini"},
           "d10": {"folds": folds10, "pooled": pooled10, "delta": delta10},
           "d30": {"folds": folds30, "pooled": pooled30, "delta": delta30},
           "verdict": None,
           "runtime_s": round(time.time() - t0, 1)}

    res["crosscheck_campaign40"] = crosscheck_40(res)
    res["verdict"] = build_verdict({"d10": delta10, "d30": delta30})

    log("\n[DELTA @Δ10]")
    for pair in ("log", "rf", "hgb"):
        d = delta10[pair]
        log(f"  {pair:4s} macro Δ={d['macro_delta']} (md {d['macro_md_only']} -> "
            f"sensor {d['macro_md_sensor']}) | Δ>0 di {d['wins_delta_gt_0']}/{d['n_valid']} fold | "
            f"Δ<=0 di {d['n_delta_le_0']}/{d['n_valid']} | p={d['sign_p_two_sided']} | "
            f"{d['verdict_pair']}")
    log("[DELTA @Δ30]")
    for pair in ("log", "rf", "hgb"):
        d = delta30[pair]
        log(f"  {pair:4s} macro Δ={d['macro_delta']} | Δ>0 di {d['wins_delta_gt_0']}/{d['n_valid']} fold | "
            f"p={d['sign_p_two_sided']} | {d['verdict_pair']}")
    log(f"VERDICT d10: {res['verdict']['overall_d10']}")
    log(f"VERDICT d30: {res['verdict']['overall_d30']}")
    cc = res["crosscheck_campaign40"]
    log(f"CROSSCHECK kampanye 40: all_equal={cc['all_equal']} "
        f"(b1 frozen 0.2265: {cc.get('b1_frozen_macro_y10_0_2265')})")

    OUT_JSON.write_text(json.dumps(res, indent=2, ensure_ascii=False, default=str),
                        encoding="utf-8")
    log(f"\nJSON -> {OUT_JSON}")
    write_md(res)
    log(f"MD   -> {OUT_MD}")
    log(f"SELESAI {res['runtime_s']}s")
    log("EXIT 0")


if __name__ == "__main__":
    if "--md-only" in sys.argv:
        # Regenerasi MD dari JSON yang sudah ada (TANPA mengulang kampanye 341s).
        # Dipakai HANYA untuk perbaikan kosmetik format; angka tidak dihitung ulang.
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
