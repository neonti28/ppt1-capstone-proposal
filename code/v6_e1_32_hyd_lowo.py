#!/usr/bin/env python3
"""V6-E1b 32 — training + LOWO kelas `hyd` (anomali hidrolik, Volve).

Mengikuti pra-registrasi docs/V6_E1b_PREREG_HYD.md
(SHA-256 411366bec820d9978623a43418daaa0d123ecd397f398961f56ab19a2c912152).
Fitur = 8 channel mekanis; SPPA/TFLO/SPM DILARANG (asersi). Gate G1/G2 identik E1a.
"""
import json
import os
import time
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import average_precision_score, roc_auc_score

WIN = "/mnt/d/Capstone 1/scratch/v6_e1/windows_hyd"
OUT = "/mnt/d/Capstone 1/scratch/v6_e1/E1b_LOWO_RESULTS.json"
LOG = "/mnt/d/Capstone 1/scratch/v6_e1/E1b_LOWO_RUN_LOG.txt"
SEED = 42
N_BOOT = 1000
BLOCK = 60
MIN_POS_EVAL = 30
LIFT_GATE = 1.5

CHAN = ["TQA", "RPM", "SWOB", "HKLD", "ROP", "BPOS", "depth", "dbtm"]  # SPPA/TFLO/SPM excluded
STATS = ["mean", "std", "slope", "last", "frac"]
FEATS = [f"{c}_{s}" for c in CHAN for s in STATS]
DEPTH_FEATS = [f"{c}_{s}" for c in ("depth", "dbtm") for s in STATS]
CL = "hyd"
log_lines = []


def log(m):
    print(m, flush=True)
    log_lines.append(m)


def moving_block_ci(y, score, n_boot=N_BOOT, block=BLOCK, seed=SEED):
    rng = np.random.default_rng(seed)
    n = len(y)
    if n < 2 * block or y.sum() == 0 or y.sum() == n:
        return None
    nblocks = int(np.ceil(n / block))
    vals = []
    for _ in range(n_boot):
        starts = rng.choice(np.arange(n), size=nblocks, replace=True)
        idx = ((starts[:, None] + np.arange(block)[None, :]).ravel() % n)[:n]
        yb, sb = y[idx], score[idx]
        if yb.min() == yb.max():
            continue
        vals.append(average_precision_score(yb, sb))
    return [float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))] if vals else None


def mk_rf():
    return Pipeline([("imp", SimpleImputer(strategy="median")),
                     ("clf", RandomForestClassifier(n_estimators=300, min_samples_leaf=5,
                                                    class_weight="balanced_subsample",
                                                    random_state=SEED, n_jobs=-1))])


def mk_lr():
    return Pipeline([("imp", SimpleImputer(strategy="median")),
                     ("sc", StandardScaler()),
                     ("clf", LogisticRegression(class_weight="balanced", max_iter=1000,
                                                random_state=SEED))])


def main():
    t0 = time.time()
    # asersi anti-sirkular
    for banned in ("SPPA", "TFLO", "SPM"):
        for s in STATS:
            assert f"{banned}_{s}" not in FEATS, f"{banned}_{s}"
    for c in FEATS:
        assert not c.startswith(("y_", "valid", "nobs", "obs_"))
    log("assertions: SPPA/TFLO/SPM excluded, no label cols -> PASS")

    data = {}
    for f in sorted(os.listdir(WIN)):
        if f.endswith(".csv.gz"):
            d = pd.read_csv(os.path.join(WIN, f))
            data[f.replace(".csv.gz", "")] = d
    wells = list(data)
    log(f"wells: {wells}")

    folds = []
    for w_te in wells:
        parts = [data[w][lambda x: x["feat_valid"] & x[f"valid_{CL}"].astype(bool)]
                 for w in wells if w != w_te]
        tr = pd.concat(parts, ignore_index=True)
        te = data[w_te][lambda x: x["feat_valid"] & x[f"valid_{CL}"].astype(bool)].copy()
        y_tr = tr[CL].to_numpy().astype(int) if CL in tr else tr[f"y_{CL}"].to_numpy().astype(int)
        y_col = CL if CL in te else f"y_{CL}"
        y_te = te[y_col].to_numpy().astype(int)
        order = np.argsort(te["ts_bin"].to_numpy())
        y_te, te = y_te[order], te.iloc[order]
        X_tr = tr[FEATS].apply(pd.to_numeric, errors="coerce")
        X_te = te[FEATS].apply(pd.to_numeric, errors="coerce")
        prev = float(y_te.mean())
        fold = {"well": w_te, "n_train": int(len(tr)), "n_test": int(len(y_te)),
                "n_pos": int(y_te.sum()), "prev": prev,
                "underpowered": int(y_te.sum()) < MIN_POS_EVAL}
        s = time.time()
        m = mk_rf().fit(X_tr, y_tr)
        s_rf = m.predict_proba(X_te)[:, 1]
        md = mk_rf().fit(X_tr[DEPTH_FEATS], y_tr)
        s_dep = md.predict_proba(X_te[DEPTH_FEATS])[:, 1]
        ml = mk_lr().fit(X_tr, y_tr)
        s_lr = ml.predict_proba(X_te)[:, 1]
        fold["auprc_rf"] = float(average_precision_score(y_te, s_rf))
        fold["auprc_logreg"] = float(average_precision_score(y_te, s_lr))
        fold["auprc_depth"] = float(average_precision_score(y_te, s_dep))
        fold["roc_rf"] = float(roc_auc_score(y_te, s_rf))
        fold["lift_rf"] = fold["auprc_rf"] / prev if prev else None
        fold["lift_depth"] = fold["auprc_depth"] / prev if prev else None
        fold["ci95_rf"] = moving_block_ci(y_te, s_rf)
        if "y_prev_hyd" in te:
            pv = te["valid_prev_hyd"].to_numpy() > 0
            fold["auprc_persistence"] = (float(average_precision_score(y_te[pv], te["y_prev_hyd"].to_numpy()[pv]))
                                         if pv.sum() and len(np.unique(y_te[pv])) > 1 else None)
            fold["n_persistence"] = int(pv.sum())
        fold["fit_time_s"] = round(time.time() - s, 1)
        log(f"  {w_te}: n_test={fold['n_test']} pos={fold['n_pos']} prev={prev:.4f} "
            f"AUPRC_rf={fold['auprc_rf']:.4f} lift={fold['lift_rf']:.3f} depth={fold['auprc_depth']:.4f} "
            f"logreg={fold['auprc_logreg']:.4f} persist={fold['auprc_persistence']} "
            f"ci={fold['ci95_rf']} ({fold['fit_time_s']}s)")
        folds.append(fold)

    ev = [f for f in folds if not f["underpowered"] and f.get("lift_rf") is not None]
    n = len(ev)
    g1 = sum(1 for f in ev if f["lift_rf"] >= LIFT_GATE)
    g2 = sum(1 for f in ev if f["auprc_rf"] >= f["auprc_depth"])
    pd_f = [f for f in ev if f.get("auprc_persistence") is not None]
    pd_lose = sum(1 for f in pd_f if f["auprc_persistence"] > f["auprc_rf"])
    verdict = {"n_folds": len(folds), "n_evaluable": n, "g1_pass": g1, "g2_pass": g2,
               "G1": g1 > n / 2, "G2": g2 > n / 2,
               "persistence_folds": len(pd_f), "persistence_beats_rf": pd_lose}
    verdict["kelas"] = ("LULUS" if verdict["G1"] and verdict["G2"] else "GAGAL" if n else "TIDAK BISA DINILAI")
    if verdict["kelas"] == "LULUS" and pd_f and pd_lose > len(pd_f) / 2:
        verdict["kelas"] = "LAYAK BERSYARAT (persistence > model)"
    res = {"prereg_sha256": "411366bec820d9978623a43418daaa0d123ecd397f398961f56ab19a2c912152",
           "class": CL, "folds": folds, "verdict": verdict,
           "meta": {"n_boot": N_BOOT, "block": BLOCK, "seed": SEED,
                    "features": FEATS, "elapsed_s": round(time.time() - t0, 1)}}
    json.dump(res, open(OUT, "w"), indent=1)
    open(LOG, "w").write("\n".join(log_lines))
    log(f">> hyd: {verdict}")


if __name__ == "__main__":
    main()
