"""V9-E_ML 01 — harness training head ML (RF/GB/LR) + baseline relevan pada dataset D1.

Task: t_902dd141 [Algorithm Engineer ML] · Board: capstone-v9-build
Spesifikasi: docs/V9_PM1_ARCHITECTURE.md §2 (head ML per engine) + §3 (kontrak shared)
Rumus/baseline: docs/V9_R1_JUSTIFICATION.md §3-§4
Data: scratch/v9_d1/datasets/<engine>.csv.gz + lowo_<engine>.json (D1)

Kontrak (mengikat, TANPA grid search, seed 42):
- RF      : RandomForestClassifier(n_estimators=300 [stuck_k2 E3: 200],
            min_samples_leaf=5, class_weight="balanced_subsample", random_state=42)
- GB      : GradientBoostingClassifier(n_estimators=200, learning_rate=0.1,
            max_depth=3, random_state=42)  [DESAIN tetap — PM1 §1.2 ML heads RF/GBM/LR]
- LR      : SimpleImputer(median, fold-safe) -> StandardScaler -> LogisticRegression(
            max_iter=1000, class_weight="balanced", random_state=42)
- Imputer median fold-safe SEMUA model (fit hanya data latih).
- Baseline: persistence (y_prev; valid_prev==1 bila ada), canary-depth (RF kontrak,
            fitur depth_*/dbtm_* saja), prevalence-random (AUPRC = prev).
- Metrik per fold: AUPRC + CI95 moving-block bootstrap (blok 60 jendela, 1000
            resample, seed 42); lift = AUPRC/prev; plafon = 1/prev; P/R/FAR_24
            (FAR_24 = 1440*FP/n_neg, skala jendela 1 mnt -> per 24 jam operasi)
            pada tau pra-reg {0.05,0.10,0.20,0.30,0.50} (grid tau PM1 §2.6 shk,
            dipakai seragam — BUKAN grid search, semua titik dilaporkan).
- stuck_k2 (onset): + q95-train operating point (pra-reg PM1 §2.4 E3),
            B1 + TLead dari run positif berurutan (rekonstruksi DERIVED — kolom
            ts_bin/lab_ts dataset stuck_k2 kosong, lihat §limitations dokumen).
- Underpowered: test fold < 30 positif dilabeli, tidak dihitung mayoritas.
- Larangan dipatuhi: TIDAK ada RF/ML di hyd-K-i (D-A5) — skrip ini tidak
            menerima engine hyd_ki.

Pemakaian: python3 v9_e_ML_01_train.py --engine vib [--determinism-check]
Output: scratch/v9_e_ml/v9_e_ML_<engine>_RESULTS.json + run log bertimestamp.
"""
import argparse
import datetime
import hashlib
import json
import os
import platform
import time

import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, precision_score, recall_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

SEED = 42
BASE = "/mnt/d/Capstone 1(v2)"
DS_DIR = os.path.join(BASE, "scratch/v9_d1/datasets")
LOWO_DIR = os.path.join(BASE, "scratch/v9_d1")
OUT_DIR = os.path.join(BASE, "scratch/v9_e_ml")
os.makedirs(OUT_DIR, exist_ok=True)

TAUS = [0.05, 0.10, 0.20, 0.30, 0.50]
BOOT_BLOCK = 60       # jendela 60 mnt (grid 60 dtk) — moving-block bootstrap
BOOT_N = 1000
UNDERPOWERED_POS = 30

META = {"well", "ts_bin", "feat_ts_max", "lab_ts", "lab_kind"}
ENGINE_META = {  # kolom meta tambahan per engine yang bukan fitur
    "vib": {"y_vib", "y_prev_vib", "valid_prev_vib"},
    "ssi": {"y_ssi", "y_prev_ssi", "valid_prev_ssi"},
    "shk": {"y_shk", "y_prev_shk", "valid_prev_shk"},
    "stuck_k1": {"y_stuck", "y_prev_stuck", "valid_prev_stuck"},
    "hyd_ki": {"y_hyd", "y_prev_hyd", "valid_prev_hyd", "obs_hyd", "anom_hyd"},
    "stuck_k2": {"y_stuck_onset", "y_prev_stuck_onset"},
}
Y_COL = {"vib": "y_vib", "ssi": "y_ssi", "shk": "y_shk",
         "stuck_k1": "y_stuck", "hyd_ki": "y_hyd", "stuck_k2": "y_stuck_onset"}
PREV_COL = {"vib": "y_prev_vib", "ssi": "y_prev_ssi", "shk": "y_prev_shk",
            "stuck_k1": "y_prev_stuck", "hyd_ki": "y_prev_hyd",
            "stuck_k2": "y_prev_stuck_onset"}
VALID_COL = {"vib": "valid_prev_vib", "ssi": "valid_prev_ssi",
             "shk": "valid_prev_shk", "stuck_k1": "valid_prev_stuck",
             "hyd_ki": "valid_prev_hyd", "stuck_k2": None}

# engine yang boleh dilatih kartu ini (fokus kartu + D-A5 hyd dilarang, K-i stuck = persistence)
ALLOWED = {"vib": "deteksi kondisi (status VIBLAT>=32.17405)",
           "ssi": "deteksi kondisi (status SSI>=1)",
           "shk": "deteksi anomali berlangsung (status SHKRSK>=1)",
           "stuck_k2": "prediksi kejadian mendatang (onset STUCK 0->1, H=10 mnt)"}
RF_N_EST = {"stuck_k2": 200}   # E3 kontrak PM1 §2.4; lainnya 300 (§2.1)


def log(msg, log_path):
    line = f"[{datetime.datetime.now().isoformat(timespec='seconds')}] {msg}"
    print(line, flush=True)
    with open(log_path, "a") as f:
        f.write(line + "\n")


def ap_ci_block(y, score, rng, block=BOOT_BLOCK, n_boot=BOOT_N):
    """CI95 moving-block bootstrap (circular) untuk AUPRC. y/score urut waktu."""
    n = len(y)
    if n < 2 * block or y.sum() == 0 or y.sum() == n:
        return None
    n_blocks = int(np.ceil(n / block))
    aps = np.empty(n_boot)
    for b in range(n_boot):
        starts = rng.integers(0, n, size=n_blocks)
        idx = (starts[:, None] + np.arange(block)[None, :]).ravel() % n
        idx = idx[:n]
        aps[b] = average_precision_score(y[idx], score[idx])
    return [float(np.percentile(aps, 2.5)), float(np.percentile(aps, 97.5))]


def tau_metrics(y, pred):
    tp = int(((pred == 1) & (y == 1)).sum())
    fp = int(((pred == 1) & (y == 0)).sum())
    fn = int(((pred == 0) & (y == 1)).sum())
    n_neg = int((y == 0).sum())
    p = tp / (tp + fp) if (tp + fp) else None
    r = tp / (tp + fn) if (tp + fn) else None
    far24 = 1440.0 * fp / n_neg if n_neg else None
    return {"TP": tp, "FP": fp, "FN": fn, "n_neg": n_neg,
            "precision": p, "recall": r, "FAR_24jam": far24}


def onset_events(y):
    """Run positif berurutan = 1 kelompok event (rekonstruksi DERIVED)."""
    events, i, n = [], 0, len(y)
    while i < n:
        if y[i] == 1:
            j = i
            while j + 1 < n and y[j + 1] == 1:
                j += 1
            events.append((i, j))
            i = j + 1
        else:
            i += 1
    return events


def onset_metrics(y, score, feat_ts, tau):
    """B1 = % event (run positif) dgn >=1 alarm di horizon; TLead = menit."""
    events = onset_events(y)
    if not events:
        return {"n_events": 0}
    leads = []
    hit = 0
    for (i, j) in events:
        alarm_rows = np.where((np.arange(len(y)) >= i) & (np.arange(len(y)) <= j)
                              & (score >= tau))[0]
        if len(alarm_rows):
            hit += 1
            a = alarm_rows[0]
            # t_e ~ feat_ts_last + 2 ; t0_alarm = feat_ts_max+1 -> TLead = last-a+1
            leads.append(float(feat_ts[j] - feat_ts[a] + 1))
    leads = np.array(leads)
    return {"n_events": len(events), "B1_coverage": hit / len(events),
            "TLead_median_mnt": float(np.median(leads)) if len(leads) else None,
            "TLead_iqr_mnt": ([float(np.percentile(leads, 25)),
                               float(np.percentile(leads, 75))] if len(leads) else None),
            "n_detected": hit}


def make_models(engine):
    rf = RandomForestClassifier(
        n_estimators=RF_N_EST.get(engine, 300),
        min_samples_leaf=5, class_weight="balanced_subsample", random_state=SEED,
        n_jobs=-1)
    gb = GradientBoostingClassifier(n_estimators=200, learning_rate=0.1,
                                    max_depth=3, random_state=SEED)
    lr = Pipeline([
        ("imp", SimpleImputer(strategy="median")),
        ("sc", StandardScaler()),
        ("clf", LogisticRegression(max_iter=1000, class_weight="balanced",
                                   random_state=SEED)),
    ])
    return {"rf": rf, "gb": gb, "lr": lr}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--engine", required=True, choices=list(ALLOWED))
    ap.add_argument("--determinism-check", action="store_true")
    args = ap.parse_args()
    engine = args.engine
    log_path = os.path.join(OUT_DIR, f"v9_e_ML_{engine}_RUN_LOG.txt")
    t_run = time.time()
    log(f"== START engine={engine} seed={SEED} sklearn={sklearn.__version__} "
        f"python={platform.python_version()}", log_path)

    ds_path = os.path.join(DS_DIR, f"{engine}.csv.gz")
    df = pd.read_csv(ds_path)
    ycol, pcol, vcol = Y_COL[engine], PREV_COL[engine], VALID_COL[engine]
    feats = [c for c in df.columns if c not in META | ENGINE_META[engine]]
    assert not any(k in c for k in ("VIBLAT", "SHKRSK", "CRPM", "STUCK")
                   for c in feats), "anti-sirkularitas: kanal label ada di fitur!"
    log(f"dataset rows={len(df)} feats={len(feats)} pos={int(df[ycol].sum())}", log_path)

    lowo = json.load(open(os.path.join(LOWO_DIR, f"lowo_{engine}.json")))
    is_onset = engine == "stuck_k2"
    rng_global = np.random.default_rng(SEED)

    result = {
        "engine": engine,
        "klaim_tugas": ALLOWED[engine],
        "jenis_task": "onset_prediction" if is_onset else "status_detection",
        "dataset": ds_path,
        "dataset_sha256": hashlib.sha256(open(ds_path, "rb").read(2**20)).hexdigest(),
        "n_features": len(feats),
        "feature_cols": feats,
        "seed": SEED,
        "hyperparams": {
            "rf": {"n_estimators": RF_N_EST.get(engine, 300), "min_samples_leaf": 5,
                   "class_weight": "balanced_subsample", "random_state": SEED},
            "gb": {"n_estimators": 200, "learning_rate": 0.1, "max_depth": 3,
                   "random_state": SEED},
            "lr": {"imputer": "median fold-safe", "scale": "StandardScaler fold-safe",
                   "max_iter": 1000, "class_weight": "balanced", "random_state": SEED},
        },
        "taus": TAUS,
        "ci95_method": f"moving-block bootstrap circular, block={BOOT_BLOCK}, "
                       f"n_boot={BOOT_N}, seed={SEED}",
        "software": {"sklearn": sklearn.__version__, "numpy": np.__version__,
                     "pandas": pd.__version__},
        "folds": [],
    }

    for fi, fold in enumerate(lowo["folds"]):
        tw = fold["test_well"]
        tr_wells = fold["train_wells"]
        tr = df[df.well.isin(tr_wells)]
        te = df[df.well == tw]
        y_tr = tr[ycol].to_numpy().astype(int)
        y_te = te[ycol].to_numpy().astype(int)
        X_tr, X_te = tr[feats], te[feats]
        prev = float(y_te.mean())
        n_pos = int(y_te.sum())
        rng = np.random.default_rng(SEED)  # per fold deterministik
        frec = {"fold": fi, "test_well": tw, "train_wells": tr_wells,
                "n_train": int(len(tr)), "n_test": int(len(te)),
                "pos_test": n_pos, "prev_test": prev,
                "underpowered": n_pos < UNDERPOWERED_POS,
                "models": {}, "baselines": {}, "delta_B": {}}
        log(f"-- fold {fi} test={tw} n_train={len(tr)} n_test={len(te)} "
            f"pos={n_pos} prev={prev:.4f}", log_path)

        scores = {}
        for name, model in make_models(engine).items():
            t0 = time.time()
            if name == "lr":
                model.fit(X_tr, y_tr)
                s_te = model.predict_proba(X_te)[:, 1]
                s_tr = model.predict_proba(X_tr)[:, 1]
            else:
                imp = SimpleImputer(strategy="median")
                X_tr_i, X_te_i = imp.fit_transform(X_tr), imp.transform(X_te)
                model.fit(X_tr_i, y_tr)
                s_te = model.predict_proba(X_te_i)[:, 1]
                s_tr = model.predict_proba(X_tr_i)[:, 1]
            scores[name] = s_te
            ap = float(average_precision_score(y_te, s_te))
            ci = ap_ci_block(y_te, s_te, rng)
            mrec = {"auprc": ap, "ci95": ci, "lift": ap / prev if prev else None,
                    "plafon_lift": 1.0 / prev if prev else None,
                    "n_train_scores": int(len(s_tr)), "fit_predict_s": round(time.time() - t0, 1),
                    "tau_metrics": {}}
            for tau in TAUS:
                mrec["tau_metrics"][str(tau)] = tau_metrics(y_te, (s_te >= tau).astype(int))
            if is_onset:
                thr95 = float(np.quantile(s_tr, 0.95))
                mrec["q95_train"] = thr95
                mrec["tau_metrics"]["q95_train"] = tau_metrics(
                    y_te, (s_te >= thr95).astype(int))
                feat_ts = te["feat_ts_max"].to_numpy()
                mrec["onset_by_tau"] = {str(tau): onset_metrics(y_te, s_te, feat_ts, tau)
                                        for tau in TAUS}
                mrec["onset_by_tau"]["q95_train"] = onset_metrics(y_te, s_te, feat_ts, thr95)
            frec["models"][name] = mrec
            log(f"   {name}: AUPRC={ap:.4f} CI95={ci} "
                f"({mrec['fit_predict_s']}s)", log_path)

        # ---- determinism check (fold 0 only, rf) ----
        if args.determinism_check and fi == 0:
            imp = SimpleImputer(strategy="median")
            X_tr_i, X_te_i = imp.fit_transform(X_tr), imp.transform(X_te)
            r2 = RandomForestClassifier(
                n_estimators=RF_N_EST.get(engine, 300), min_samples_leaf=5,
                class_weight="balanced_subsample", random_state=SEED, n_jobs=-1)
            r2.fit(X_tr_i, y_tr)
            s2 = r2.predict_proba(X_te_i)[:, 1]
            identical = bool(np.array_equal(scores["rf"], s2))
            result["determinism_check"] = {
                "fold": 0, "model": "rf", "rerun_identical": identical,
                "max_abs_diff": float(np.max(np.abs(scores["rf"] - s2)))}
            log(f"   determinism rf fold0 rerun identical={identical}", log_path)

        # ---- baselines ----
        b = {}
        b["prevalence_random"] = {"auprc": prev, "note": "AUPRC acak = prevalensi"}
        # persistence
        vmask = te[vcol].to_numpy().astype(bool) if vcol else np.ones(len(te), bool)
        s_prev = te[pcol].to_numpy().astype(float)
        ap_p = float(average_precision_score(y_te[vmask], s_prev[vmask]))
        b["persistence"] = {"auprc": ap_p, "n_eval": int(vmask.sum()),
                            "note": "y_prev (D1); valid_prev==1 bila ada"}
        # canary-depth (RF kontrak, fitur depth_*/dbtm_ saja)
        depth_cols = [c for c in feats if c.startswith(("depth_", "dbtm_"))]
        imp = SimpleImputer(strategy="median")
        Xd_tr = df[df.well.isin(tr_wells)][depth_cols]
        Xd_te = te[depth_cols]
        d_tr_i, d_te_i = imp.fit_transform(Xd_tr), imp.transform(Xd_te)
        can = RandomForestClassifier(n_estimators=RF_N_EST.get(engine, 300),
                                     min_samples_leaf=5,
                                     class_weight="balanced_subsample",
                                     random_state=SEED, n_jobs=-1)
        can.fit(d_tr_i, y_tr)
        s_can = can.predict_proba(d_te_i)[:, 1]
        ap_can = float(average_precision_score(y_te, s_can))
        b["canary_depth"] = {"auprc": ap_can,
                             "ci95": ap_ci_block(y_te, s_can, rng),
                             "n_depth_features": len(depth_cols)}
        frec["baselines"] = b

        # ---- delta B ----
        for name in scores:
            frec["delta_B"][f"{name}_vs_persistence"] = float(
                average_precision_score(y_te[vmask], scores[name][vmask]) - ap_p)
            frec["delta_B"][f"{name}_vs_canary_depth"] = float(
                average_precision_score(y_te, scores[name]) - ap_can)
            frec["delta_B"][f"{name}_vs_prevalence_random"] = float(
                frec["models"][name]["auprc"] - prev)
        result["folds"].append(frec)

    # agregat ringkas (fold layak saja utk mayoritas; underpowered tetap tercatat)
    for name in ("rf", "gb", "lr"):
        aps = [f["models"][name]["auprc"] for f in result["folds"]]
        dcan = [f["delta_B"][f"{name}_vs_canary_depth"] > 0 for f in result["folds"]
                if not f["underpowered"]]
        dpers = [f["delta_B"][f"{name}_vs_persistence"] > 0 for f in result["folds"]
                 if not f["underpowered"]]
        result.setdefault("agregat", {})[name] = {
            "auprc_min": min(aps), "auprc_max": max(aps),
            "spread_auprc": max(aps) - min(aps),
            "deltaB_vs_canary_pos": f"{sum(dcan)}/{len(dcan)} fold layak",
            "deltaB_vs_persistence_pos": f"{sum(dpers)}/{len(dpers)} fold layak",
        }

    out = os.path.join(OUT_DIR, f"v9_e_ML_{engine}_RESULTS.json")
    json.dump(result, open(out, "w"), indent=1, allow_nan=False)
    log(f"== DONE engine={engine} -> {out} elapsed={round(time.time()-t_run,1)}s",
        log_path)


if __name__ == "__main__":
    main()
