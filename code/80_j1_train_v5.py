"""V5 J1 — training kampanye klasifikasi kondisi kerusakan (data sintetik sim_v5).

Mengikuti dokumen pra-registrasi docs/V5_J1_PREREG.md (SHA-256 dikunci di kartu t_943af8af).
Gate TIDAK boleh berubah setelah hasil. Skrip ini tidak mengubah prereg apa pun.

Output:
  docs/V5_J1_RESULTS.json          — angka primer (memuat hash prereg)
  docs/V5_J1_run_predictions.csv   — prediksi run-level (tabel verifier)
  docs/V5_J1_fold_assignments.csv  — run_id -> fold
  docs/V5_J1_window_predictions.csv.gz — prediksi window-level (sekunder)
  docs/V5_J1_SHAP.png              — SHAP beeswarm deskriptif (fold-0)
"""
import hashlib
import json
import os
import sys
import time

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    classification_report,
    confusion_matrix,
    f1_score,
)
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

SEED = 42
N_SPLITS = 5
RF_PARAMS = dict(n_estimators=400, min_samples_leaf=2, random_state=SEED, n_jobs=-1)
RF_PERM_PARAMS = dict(n_estimators=100, min_samples_leaf=2, random_state=SEED, n_jobs=-1)
N_PERM = 100
N_BOOT = 1000
SHAP_N = 500
WINDOW_ROWS = 100
STRIDE = 50
MIN_DRILL_ROWS = 20
G1_THRESHOLD = 0.60
G2_MARGIN = 0.15

WS = "/mnt/d/Capstone 1"
SIM_DIR = os.path.join(WS, "data", "sim_v5")
PREREG = os.path.join(WS, "docs", "V5_J1_PREREG.md")
OUT_JSON = os.path.join(WS, "docs", "V5_J1_RESULTS.json")
OUT_RUNCSV = os.path.join(WS, "docs", "V5_J1_run_predictions.csv")
OUT_FOLDCSV = os.path.join(WS, "docs", "V5_J1_fold_assignments.csv")
OUT_WCSV = os.path.join(WS, "docs", "V5_J1_window_predictions.csv.gz")
OUT_SHAP = os.path.join(WS, "docs", "V5_J1_SHAP.png")

SENSORS = [
    "rop_m_per_hr",
    "wob_n",
    "hookload_n",
    "surface_rpm",
    "surface_torque_nm",
    "pump_spm",
    "flow_rate_m3_per_min",
    "spp_kpa",
    "difp_kpa",
    "block_position_m",
    "hole_depth_m",
    "bit_depth_m",
]
STATS = ["mean", "std", "min", "max", "slope"]
BANNED_TOKENS = [
    "n_rows", "n_windows", "duration", "wall_s", "end_md", "start_md",
    "timestamp", "seed", "run_id", "index", "ucs", "cutting_efficiency",
    "bha_resistance", "rpm_cmd", "spm_cmd",
]


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def slope_of(values):
    x = np.arange(values.shape[0], dtype=np.float64)
    x = x - x.mean()
    y = values - values.mean()
    denom = (x * x).sum()
    if denom == 0:
        return 0.0
    return float((x * y).sum() / denom)


def window_stats(block):
    """block: DataFrame (n_window_rows x SENSORS) -> dict fitur."""
    feats = {}
    for col in SENSORS:
        v = block[col].to_numpy(dtype=np.float64)
        feats[f"{col}__mean"] = float(v.mean())
        feats[f"{col}__std"] = float(v.std(ddof=0))
        feats[f"{col}__min"] = float(v.min())
        feats[f"{col}__max"] = float(v.max())
        feats[f"{col}__slope"] = slope_of(v)
    return feats


def build_windows():
    classes = sorted(
        d for d in os.listdir(SIM_DIR) if os.path.isdir(os.path.join(SIM_DIR, d))
    )
    rows = []
    excluded = []
    t0 = time.time()
    for ci, cls in enumerate(classes):
        run_dirs = sorted(
            os.listdir(os.path.join(SIM_DIR, cls))
        )
        for k, run in enumerate(run_dirs):
            run_path = os.path.join(SIM_DIR, cls, run)
            tel = os.path.join(run_path, "surface_telemetry.csv")
            if not os.path.exists(tel):
                excluded.append({"run_id": run, "reason": "no_telemetry"})
                continue
            df = pd.read_csv(tel)
            drill = df[df["activity"] == "drilling"]
            n = len(drill)
            if n < MIN_DRILL_ROWS:
                excluded.append({"run_id": run, "reason": f"drill_rows_{n}_lt_{MIN_DRILL_ROWS}"})
                continue
            if n >= WINDOW_ROWS:
                starts = range(0, n - WINDOW_ROWS + 1, STRIDE)
                blocks = [drill.iloc[s : s + WINDOW_ROWS] for s in starts]
            else:
                blocks = [drill]
            for wi, block in enumerate(blocks):
                feats = window_stats(block)
                feats["run_id"] = run
                feats["window_idx"] = wi
                feats["y"] = ci
                rows.append(feats)
            if (k + 1) % 50 == 0:
                log(f"class {cls}: {k + 1}/{len(run_dirs)} runs, windows so far {len(rows)}")
        log(f"class {cls} done ({ci + 1}/{len(classes)}), windows total {len(rows)}")
    log(f"windows built in {time.time() - t0:.1f}s, excluded {len(excluded)} runs")
    return pd.DataFrame(rows), excluded, classes


def macro_ap(y_true, proba):
    return float(average_precision_score(y_true, proba, average="macro"))


def per_class_ap(y_true, proba, classes):
    out = {}
    for i, name in enumerate(classes):
        binary = (y_true == i).astype(int)
        out[name] = float(average_precision_score(binary, proba[:, i]))
    return out


def aggregate_run_level(df_win, proba, classes):
    """Rata-rata probabilitas window per run -> DataFrame run-level."""
    cols = {f"p_{name}": proba[:, i] for i, name in enumerate(classes)}
    cols["run_id"] = df_win["run_id"].to_numpy()
    cols["y"] = df_win["y"].to_numpy()
    tmp = pd.DataFrame(cols)
    agg = tmp.groupby("run_id", sort=True).mean(numeric_only=True)
    agg["y"] = agg["y"].round().astype(int)
    return agg.reset_index()


def main():
    prereg_hash = sha256_file(PREREG)
    log(f"prereg sha256: {prereg_hash}")
    log("building windows ...")
    df, excluded, classes = build_windows()
    n_classes = len(classes)

    feature_cols = [f"{c}__{s}" for s in STATS for c in SENSORS]
    assert len(feature_cols) == 60, len(feature_cols)
    for fc in feature_cols:
        for tok in BANNED_TOKENS:
            assert tok not in fc, f"banned token {tok} in feature {fc}"
    log(f"features OK: {len(feature_cols)} (banned-token assertion passed)")

    DEPTH_IDX = [i for i, fc in enumerate(feature_cols)
                 if fc.startswith(("hole_depth_m__", "bit_depth_m__"))]
    assert len(DEPTH_IDX) == 10, DEPTH_IDX  # 5 statistik x 2 kolom kedalaman

    X = df[feature_cols].to_numpy(dtype=np.float64)
    y = df["y"].to_numpy(dtype=int)
    groups = df["run_id"].to_numpy()

    sgkf = StratifiedGroupKFold(n_splits=N_SPLITS, shuffle=True, random_state=SEED)
    oof_m1 = np.zeros((len(df), n_classes))
    oof_m2 = np.zeros((len(df), n_classes))
    oof_can = np.zeros((len(df), n_classes))
    fold_of_window = np.full(len(df), -1, dtype=int)
    g3_overlap = []

    t0 = time.time()
    for fold, (tr, te) in enumerate(sgkf.split(X, y, groups)):
        g_tr = set(groups[tr])
        g_te = set(groups[te])
        overlap = g_tr & g_te
        g3_overlap.append({"fold": fold, "n_train": len(g_tr), "n_test": len(g_te),
                           "overlap_runs": len(overlap)})
        assert not overlap, f"fold {fold}: run leakage {list(overlap)[:5]}"
        fold_of_window[te] = fold

        m1 = RandomForestClassifier(**RF_PARAMS)
        m1.fit(X[tr], y[tr])
        oof_m1[te] = m1.predict_proba(X[te])

        m2 = HistGradientBoostingClassifier(random_state=SEED)
        m2.fit(X[tr], y[tr])
        p2 = m2.predict_proba(X[te])
        assert np.array_equal(m2.classes_, np.arange(n_classes)), m2.classes_
        oof_m2[te] = p2

        can = Pipeline([
            ("scaler", StandardScaler()),
            ("lr", LogisticRegression(max_iter=2000, random_state=SEED)),
        ])
        can.fit(X[tr][:, DEPTH_IDX], y[tr])  # 10 fitur kedalaman (dipilih per-nama)
        oof_can[te] = can.predict_proba(X[te][:, DEPTH_IDX])

        log(f"fold {fold} done: train windows {len(tr)}, test windows {len(te)}")

    log(f"5-fold training done in {time.time() - t0:.1f}s")

    assert (fold_of_window >= 0).all(), "some windows never got a fold"
    df["fold"] = fold_of_window

    run_m1 = aggregate_run_level(df, oof_m1, classes)
    run_m2 = aggregate_run_level(df, oof_m2, classes)
    run_can = aggregate_run_level(df, oof_can, classes)

    y_run = run_m1["y"].to_numpy(dtype=int)
    p_m1 = run_m1[[f"p_{c}" for c in classes]].to_numpy()
    p_m2 = run_m2[[f"p_{c}" for c in classes]].to_numpy()
    p_can = run_can[[f"p_{c}" for c in classes]].to_numpy()

    ap_m1 = macro_ap(y_run, p_m1)
    ap_m2 = macro_ap(y_run, p_m2)
    ap_can = macro_ap(y_run, p_can)
    log(f"run-level macro-AUPRC: M1={ap_m1:.4f} M2={ap_m2:.4f} C={ap_can:.4f}")

    # ---- bootstrap CI95 (run-level, seed 42) ----
    rng = np.random.default_rng(SEED)
    boot_m1 = np.empty(N_BOOT)
    boot_gap = np.empty(N_BOOT)
    n_run = len(y_run)
    for b in range(N_BOOT):
        idx = rng.integers(0, n_run, n_run)
        boot_m1[b] = macro_ap(y_run[idx], p_m1[idx])
        boot_gap[b] = macro_ap(y_run[idx], p_m1[idx]) - macro_ap(y_run[idx], p_can[idx])
    ci_m1 = [float(np.percentile(boot_m1, 2.5)), float(np.percentile(boot_m1, 97.5))]
    ci_gap = [float(np.percentile(boot_gap, 2.5)), float(np.percentile(boot_gap, 97.5))]
    log(f"bootstrap CI95 M1 macro-AUPRC {ci_m1}, gap vs canary {ci_gap}")

    # ---- window-level (sekunder) ----
    win_m1_macro = macro_ap(y, oof_m1)
    win_can_macro = macro_ap(y, oof_can)

    # ---- argmax metrics ----
    pred_m1 = p_m1.argmax(axis=1)
    acc_m1 = float(accuracy_score(y_run, pred_m1))
    f1_m1 = float(f1_score(y_run, pred_m1, average="macro"))
    pred_can = p_can.argmax(axis=1)
    acc_can = float(accuracy_score(y_run, pred_can))
    f1_can = float(f1_score(y_run, pred_can, average="macro"))
    cm = confusion_matrix(y_run, pred_m1).tolist()
    rep = classification_report(y_run, pred_m1, target_names=classes, output_dict=True,
                                zero_division=0)

    # ---- permutasi label run (seed 42, fold sama, RF 100) ----
    log("permutation test mulai (100 x 5 fold RF100) ...")
    perm_rng = np.random.default_rng(SEED)
    run_ids_sorted = np.sort(df["run_id"].unique())
    win_run_idx = pd.Categorical(df["run_id"], categories=run_ids_sorted).codes
    assert win_run_idx.min() >= 0, "ada run_id di window yang tidak ada di run_ids_sorted"
    assert (np.asarray(y_run)).shape[0] == run_ids_sorted.shape[0], "y_run bukan per-run terurut"
    perm_null = np.empty(N_PERM)
    folds_list = list(sgkf.split(X, y, groups))
    for pi in range(N_PERM):
        perm_run_y = perm_rng.permutation(y_run)  #acak label di level RUN (bukan window)
        y_win_perm = perm_run_y[win_run_idx]     #propagasi ke window dalam run itu
        oof_perm = np.zeros((len(df), n_classes))
        for tr, te in folds_list:
            rf = RandomForestClassifier(**RF_PERM_PARAMS)
            rf.fit(X[tr], y_win_perm[tr])
            oof_perm[te] = rf.predict_proba(X[te])
        run_perm = aggregate_run_level(df, oof_perm, classes)
        y_perm_run = perm_run_y  #urutan run_m1 == urutan run_ids_sorted == urutan y_run
        p_perm = run_perm[[f"p_{c}" for c in classes]].to_numpy()
        perm_null[pi] = macro_ap(y_perm_run, p_perm)
        if (pi + 1) % 10 == 0:
            log(f"permutation {pi + 1}/{N_PERM}, null so far mean={np.nanmean(perm_null[:pi+1]):.4f}")
    p_value = float((1 + (perm_null >= ap_m1).sum()) / (1 + N_PERM))
    log(f"permutation p = {p_value:.4f}")

    # ---- SHAP deskriptif (fold 0, 500 window OOF acak, seed 42) ----
    shap_info = {"executed": False}
    try:
        import shap as shap_lib
        import matplotlib
        matplotlib.use("Agg")
        f0_test_idx = np.where(df["fold"].to_numpy() == 0)[0]
        rng2 = np.random.default_rng(SEED)
        pick = rng2.choice(f0_test_idx, size=min(SHAP_N, len(f0_test_idx)), replace=False)
        rf0 = RandomForestClassifier(**RF_PARAMS)
        rf0.fit(X[df["fold"].to_numpy() != 0], y[df["fold"].to_numpy() != 0])
        explainer = shap_lib.TreeExplainer(rf0)
        sv = explainer(X[pick])
        assert sv.values.ndim == 3, sv.values.shape  # multikelas: (n, fitur, kelas)
        base = np.asarray(sv.base_values)           # (n, kelas)
        recon = base + np.asarray(sv.values).sum(axis=1)  # (n, kelas)
        expected = rf0.predict_proba(X[pick])       # (n, kelas)
        add_err = float(np.max(np.abs(recon - expected)))
        # additivity per kelas (maks absolut)
        add_err_per_class = {
            classes[k]: float(np.max(np.abs(recon[:, k] - expected[:, k])))
            for k in range(n_classes)
        }
        # beeswarm deskriptif satu output (kelas 0 = normal_soft); deskriptif saja
        sv0 = sv[..., 0]
        shap_lib.summary_plot(sv0.values, features=X[pick],
                              feature_names=feature_cols, show=False, max_display=20)
        import matplotlib.pyplot as plt
        plt.tight_layout()
        plt.savefig(OUT_SHAP, dpi=120)
        plt.close()
        # mean |SHAP| dirata-ratakan lintas kelas (n, fitur, kelas) -> fitur
        mean_abs = np.abs(np.asarray(sv.values)).mean(axis=(0, 2))
        top = np.argsort(-mean_abs)[:20]
        shap_info = {
            "executed": True,
            "explainer": "TreeExplainer (tree_path_dependent, no background)",
            "n_windows": int(len(pick)),
            "fold": 0,
            "additivity_max_abs_err": add_err,
            "additivity_max_abs_err_per_class": add_err_per_class,
            "top20_mean_abs_shap": {feature_cols[i]: float(mean_abs[i]) for i in top},
            "plot": OUT_SHAP,
        }
        log(f"SHAP done, additivity max abs err {add_err:.2e}")
    except Exception as e:  # noqa: BLE001
        shap_info = {"executed": False, "error": repr(e)}
        log(f"SHAP FAILED (sekunder, tidak mengubah gate): {e!r}")

    # ---- gate ----
    g1 = ap_m1 >= G1_THRESHOLD
    g2 = ap_m1 >= ap_can + G2_MARGIN
    g3 = (
        all(f["overlap_runs"] == 0 for f in g3_overlap)
        and len(excluded) >= 0
    )
    verdict = "LOLOS" if (g1 and g2 and g3) else "GAGAL"

    run_df = pd.DataFrame({"run_id": run_m1["run_id"], "y_true": y_run})
    for i, c in enumerate(classes):
        run_df[f"p_m1_{c}"] = p_m1[:, i]
        run_df[f"p_m2_{c}"] = p_m2[:, i]
        run_df[f"p_can_{c}"] = p_can[:, i]
    run_df.to_csv(OUT_RUNCSV, index=False)
    df[["run_id", "window_idx", "fold", "y"]].to_csv(OUT_FOLDCSV, index=False)
    wdf = pd.DataFrame({"run_id": df["run_id"], "window_idx": df["window_idx"],
                        "fold": df["fold"], "y": df["y"]})
    for i, c in enumerate(classes):
        wdf[f"p_m1_{c}"] = oof_m1[:, i]
    wdf.to_csv(OUT_WCSV, index=False, compression="gzip")

    results = {
        "task_id": "t_943af8af",
        "campaign": "V5 J1 — klasifikasi kondisi kerusakan (data sintetik sim_v5)",
        "prereg_file": PREREG,
        "prereg_sha256": prereg_hash,
        "seed": SEED,
        "versions": {
            "python": sys.version.split()[0],
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "sklearn": __import__("sklearn").__version__,
        },
        "data": {
            "n_classes": n_classes,
            "classes": classes,
            "n_runs_total": int(df["run_id"].nunique() + len(excluded)),
            "n_runs_used": int(df["run_id"].nunique()),
            "n_windows": int(len(df)),
            "excluded_runs": excluded,
            "windows_per_run_min": int(df.groupby("run_id").size().min()),
            "windows_per_run_max": int(df.groupby("run_id").size().max()),
            "windows_per_run_median": float(df.groupby("run_id").size().median()),
        },
        "protocol": {
            "split": "StratifiedGroupKFold(5, shuffle=True, random_state=42), group=run_id",
            "metric_primary": "run-level macro-AUPRC (mean window proba per run)",
            "rf_params": RF_PARAMS,
            "rf_perm_params": RF_PERM_PARAMS,
        },
        "primary": {
            "m1_macro_auprc_run": ap_m1,
            "m1_ci95_bootstrap": ci_m1,
            "n_bootstrap": N_BOOT,
            "canary_macro_auprc_run": ap_can,
            "gap_m1_minus_canary": ap_m1 - ap_can,
            "gap_ci95_bootstrap": ci_gap,
        },
        "secondary": {
            "m2_hgb_macro_auprc_run": ap_m2,
            "m1_macro_auprc_window": win_m1_macro,
            "canary_macro_auprc_window": win_can_macro,
            "m1_accuracy_run": acc_m1,
            "m1_macro_f1_run": f1_m1,
            "canary_accuracy_run": acc_can,
            "canary_macro_f1_run": f1_can,
            "per_class_ap_run_m1": per_class_ap(y_run, p_m1, classes),
            "per_class_ap_run_canary": per_class_ap(y_run, p_can, classes),
            "confusion_matrix_m1": cm,
            "classification_report_m1": rep,
            "prevalence_per_class": {classes[i]: float((y_run == i).mean()) for i in range(n_classes)},
        },
        "permutation_test": {
            "n_perm": N_PERM,
            "statistic": "run-level macro-AUPRC M1 (RF100, fold sama)",
            "p_value": p_value,
            "null_mean": float(np.nanmean(perm_null)),
            "null_std": float(np.nanstd(perm_null)),
            "null_max": float(np.nanmax(perm_null)),
            "null_distribution_file": "docs/V5_J1_perm_null.npy",
        },
        "shap": shap_info,
        "gates": {
            "G1_m1_macro_auprc_ge_0.60": {"threshold": G1_THRESHOLD, "value": ap_m1,
                                          "pass": bool(g1)},
            "G2_m1_ge_canary_plus_0.15": {"margin": G2_MARGIN, "value": ap_m1 - ap_can,
                                          "pass": bool(g2)},
            "G3_integrity": {
                "fold_overlap": g3_overlap,
                "banned_features_present": False,
                "banned_assertion": "passed at runtime",
                "pass": bool(g3),
            },
        },
        "verdict": verdict,
        "artifacts": {
            "run_predictions": OUT_RUNCSV,
            "fold_assignments": OUT_FOLDCSV,
            "window_predictions": OUT_WCSV,
            "shap_plot": OUT_SHAP if shap_info.get("executed") else None,
        },
        "wall_s_total": round(time.time() - t0 + 0.0, 1),
    }
    np.save(os.path.join(WS, "docs", "V5_J1_perm_null.npy"), perm_null)
    with open(OUT_JSON, "w") as fh:
        json.dump(results, fh, indent=2)
    log(f"VERDICT: {verdict} (G1={g1}, G2={g2}, G3={g3})")
    log(f"results -> {OUT_JSON}")


if __name__ == "__main__":
    main()
