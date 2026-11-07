#!/usr/bin/env python3
"""RND-R4 tahap 1: LightGBM vs XGBoost vs CatBoost vs RF (RF = baseline kontrak V9).

Protokol:
  LOWO (leave-one-well-out) per engine, seed 42, tanpa grid search.
  Semua model memakai anggaran thread identik (4 thread) supaya biaya latih sebanding.
  Skor = predict_proba / pred_contrib probability, disimpan OOF untuk uji statistik tahap 3.

Keluaran: results_m1.json + oof_<engine>.npz
"""
from __future__ import annotations

import gzip
import json
import os
import time

import numpy as np
import pandas as pd

BASE = "/mnt/d/Capstone 1(v2)"
DS = f"{BASE}/scratch/v9_d1/datasets"
OUT = f"{BASE}/scratch/rnd_r4"
os.makedirs(OUT, exist_ok=True)

META_COLS = ("well", "ts_bin", "feat_ts_max", "lab_ts", "lab_kind")
LABEL_PREFIXES = ("y_", "valid_", "obs_", "anom_")
NTHREAD = 4
SEED = 42

# label kolom per engine (dari dataset v9_d1)
ENGINES = {
    "hyd_ki": {"ycol": "y_hyd", "prevcol": "y_prev_hyd"},
    "vib": {"ycol": "y_vib", "prevcol": "y_prev_vib"},
}


def load(name: str) -> pd.DataFrame:
    df = pd.read_csv(f"{DS}/{name}.csv.gz", compression="gzip")
    return df


def feature_cols(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns
            if c not in META_COLS and not c.startswith(LABEL_PREFIXES)]


def far24(fp: int, n_neg: int, win_s: int = 60) -> float | None:
    """Konvensi kampanye V8/V9: FP / (n_neg*win_s/3600) * 24."""
    h = n_neg * win_s / 3600.0
    return None if h == 0 else fp / h * 24.0


def thr_for_train_far(neg_scores: np.ndarray, target_far24: float) -> float:
    """Ambang dari skor negatif set LATIH agar FAR latih = target_far24 (per 24 jam)."""
    n_neg = len(neg_scores)
    if n_neg == 0:
        return 1.0
    # FP yang diizinkan pada set latih
    k = int(np.floor(target_far24 / 24.0 * (n_neg / 60.0)))
    k = max(k, 0)
    s = np.sort(neg_scores)[::-1]
    if k >= n_neg:
        return float(s.min())
    return float(s[k])  # skor negatif ke-(k+1) -> prediksi positif butuh skor > thr


def make_models():
    from sklearn.ensemble import RandomForestClassifier
    import lightgbm as lgb
    import xgboost as xgb
    from catboost import CatBoostClassifier

    m = {}
    m["rf"] = lambda: RandomForestClassifier(
        n_estimators=300, min_samples_leaf=5, class_weight="balanced_subsample",
        random_state=SEED, n_jobs=NTHREAD)
    m["lightgbm"] = lambda: lgb.LGBMClassifier(
        n_estimators=300, learning_rate=0.05, num_leaves=31, min_child_samples=20,
        random_state=SEED, n_jobs=NTHREAD, verbose=-1)
    m["xgboost"] = lambda: xgb.XGBClassifier(
        n_estimators=300, learning_rate=0.05, max_depth=6, tree_method="hist",
        random_state=SEED, n_jobs=NTHREAD, eval_metric="logloss")
    m["catboost"] = lambda: CatBoostClassifier(
        iterations=300, learning_rate=0.05, depth=6, random_seed=SEED,
        thread_count=NTHREAD, verbose=0, allow_writing_files=False)
    return m


def run_engine(name: str, cfg: dict) -> dict:
    from sklearn.impute import SimpleImputer
    from sklearn.metrics import average_precision_score, roc_auc_score

    df = load(name)
    feats = feature_cols(df)
    ycol = cfg["ycol"]
    wells = sorted(df["well"].unique())
    models = make_models()
    folds = []

    oof = {k: np.zeros(len(df)) for k in models}
    y_all = df[ycol].to_numpy().astype(int)

    for tw in wells:
        tr_mask = (df["well"] != tw).to_numpy()
        te_idx = np.where((df["well"] == tw).to_numpy())[0]
        tr = df[tr_mask]
        te = df.iloc[te_idx]
        t0 = time.perf_counter()
        imp = SimpleImputer(strategy="median")
        Xtr = imp.fit_transform(tr[feats]).astype(np.float32)
        Xte = imp.transform(te[feats]).astype(np.float32)
        t_imp = time.perf_counter() - t0
        ytr = tr[ycol].to_numpy().astype(int)
        yte = te[ycol].to_numpy().astype(int)
        rec = {"test_well": tw, "n_train": int(len(tr)), "n_test": int(len(te)),
               "pos_train": int(ytr.sum()), "pos_test": int(yte.sum()),
               "t_impute_s": round(t_imp, 3), "models": {}}
        for mname, ctor in models.items():
            clf = ctor()
            t0 = time.perf_counter()
            clf.fit(Xtr, ytr)
            t_fit = time.perf_counter() - t0
            t0 = time.perf_counter()
            s = clf.predict_proba(Xte)[:, 1]
            t_pred = time.perf_counter() - t0
            oof[mname][te_idx] = s
            neg_tr = s_tr = None
            # skor latih untuk ambang portabel (predict pada set latih)
            s_tr = clf.predict_proba(Xtr)[:, 1]
            neg_tr = s_tr[ytr == 0]
            thr = thr_for_train_far(neg_tr, 6.0)
            pred6 = (s >= thr).astype(int)
            n_neg = int((yte == 0).sum())
            fp6 = int(((pred6 == 1) & (yte == 0)).sum())
            tp6 = int(((pred6 == 1) & (yte == 1)).sum())
            pred5 = (s >= 0.5).astype(int)
            fp5 = int(((pred5 == 1) & (yte == 0)).sum())
            tp5 = int(((pred5 == 1) & (yte == 1)).sum())
            rec["models"][mname] = {
                "t_fit_s": round(t_fit, 3),
                "t_pred_s": round(t_pred, 3),
                "auprc": round(float(average_precision_score(yte, s)), 4) if yte.sum() else None,
                "auc": round(float(roc_auc_score(yte, s)), 4) if 0 < yte.sum() < len(yte) else None,
                "thr_far6_train": round(thr, 6),
                "far24_test_at_thr_far6": None if far24(fp6, n_neg) is None else round(far24(fp6, n_neg), 3),
                "recall_at_thr_far6": None if (yte.sum() == 0) else round(tp6 / int(yte.sum()), 4),
                "far24_test_at_0p5": None if far24(fp5, n_neg) is None else round(far24(fp5, n_neg), 3),
                "recall_at_0p5": None if (yte.sum() == 0) else round(tp5 / int(yte.sum()), 4),
            }
        folds.append(rec)
        print(f"  [{name}] fold {tw}: " + " ".join(
            f"{m}={rec['models'][m]['auprc']}/{rec['models'][m]['t_fit_s']}s" for m in models), flush=True)

    np.savez_compressed(f"{OUT}/oof_{name}.npz",
                        y=y_all, wells=df["well"].to_numpy().astype(str),
                        ts=df["ts_bin"].to_numpy(), **oof)

    # rekap per model
    summ = {}
    for m in models:
        aps = [f["models"][m]["auprc"] for f in folds if f["models"][m]["auprc"] is not None]
        fits = [f["models"][m]["t_fit_s"] for f in folds]
        f6 = [f["models"][m]["far24_test_at_thr_far6"] for f in folds
              if f["models"][m]["far24_test_at_thr_far6"] is not None]
        r6 = [f["models"][m]["recall_at_thr_far6"] for f in folds
              if f["models"][m]["recall_at_thr_far6"] is not None]
        summ[m] = {
            "auprc_folds": aps,
            "auprc_median": round(float(np.median(aps)), 4) if aps else None,
            "auprc_mean": round(float(np.mean(aps)), 4) if aps else None,
            "auprc_min": round(float(np.min(aps)), 4) if aps else None,
            "auprc_max": round(float(np.max(aps)), 4) if aps else None,
            "fit_s_median": round(float(np.median(fits)), 3),
            "fit_s_total": round(float(np.sum(fits)), 2),
            "far24_at_thr_far6_median": round(float(np.median(f6)), 3) if f6 else None,
            "far24_at_thr_far6_max": round(float(np.max(f6)), 3) if f6 else None,
            "n_fold_far_le_6": int(sum(1 for v in f6 if v <= 6.0)),
            "n_fold_scored": len(f6),
            "recall_at_thr_far6_median": round(float(np.median(r6)), 4) if r6 else None,
        }
    return {"engine": name, "ycol": ycol, "n_rows": int(len(df)),
            "n_features": len(feats), "features": feats,
            "wells": wells, "n_wells": len(wells),
            "prevalence": round(float(y_all.mean()), 4),
            "nthread": NTHREAD, "seed": SEED,
            "folds": folds, "summary": summ}


def main():
    out = {"meta": {"generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "skript": "scratch/rnd_r4/m1_bench.py",
                    "perintah": "python m1_bench.py (venv .venv-r4)",
                    "nthread": NTHREAD, "seed": SEED},
           "engines": {}}
    for name, cfg in ENGINES.items():
        print(f"== {name} ==", flush=True)
        out["engines"][name] = run_engine(name, cfg)
        with open(f"{OUT}/results_m1.json", "w") as f:
            json.dump(out, f, indent=1)
    print("DONE ->", f"{OUT}/results_m1.json")


if __name__ == "__main__":
    main()
