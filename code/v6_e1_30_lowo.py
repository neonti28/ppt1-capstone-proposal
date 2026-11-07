#!/usr/bin/env python3
"""V6-E1 30 — baseline RF/LogReg + LOWO antar sumur, AUPRC/lift per kelas per sumur.

Mengikuti pra-registrasi docs/V6_E1_PREREG.md (SHA-256 542772622d2d3539df35f484fa0a67869d485a3ff6944fab5fbd45252928e9fc).
Gate: G1 lift RF >= 1.5 di mayoritas sumur layak; G2 AUPRC RF >= canary depth di mayoritas
sumur layak. Sumur uji <30 positif = UNDERPOWERED (dilaporkan, tak dihitung mayoritas).
CI95 AUPRC RF: moving-block bootstrap (blok 60 jendela, 1000 resample, seed 42).
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

WIN = "/mnt/d/Capstone 1/scratch/v6_e1/windows"
OUT = "/mnt/d/Capstone 1/scratch/v6_e1/E1_LOWO_RESULTS.json"
LOG = "/mnt/d/Capstone 1/scratch/v6_e1/E1_LOWO_RUN_LOG.txt"
SEED = 42
N_BOOT = 1000
BLOCK = 60
MIN_POS_EVAL = 30
LIFT_GATE = 1.5

CHAN = ["TQA", "SPPA", "TFLO", "RPM", "SWOB", "HKLD", "ROP", "BPOS", "SPM", "depth", "dbtm"]
STATS = ["mean", "std", "slope", "last", "frac"]
FEATS = [f"{c}_{s}" for c in CHAN for s in STATS]
DEPTH_FEATS = [f"{c}_{s}" for c in ("depth", "dbtm") for s in STATS]
CLASSES = ["stuck", "vib", "shk", "ssi"]
LABEL_COLS = (["feat_drill_bins", "feat_drill_rows", "feat_valid"] +
              [c for c in []])

log_lines = []


def log(msg):
    print(msg, flush=True)
    log_lines.append(msg)


def moving_block_ci(y, score, n_boot=N_BOOT, block=BLOCK, seed=SEED):
    """CI95 AUPRC via circular moving-block bootstrap (blok = urutan jendela waktu)."""
    rng = np.random.default_rng(seed)
    n = len(y)
    if n < 2 * block or y.sum() == 0 or y.sum() == n:
        return None
    starts_pool = np.arange(n)
    vals = []
    nblocks = int(np.ceil(n / block))
    for _ in range(n_boot):
        starts = rng.choice(starts_pool, size=nblocks, replace=True)
        idx = (starts[:, None] + np.arange(block)[None, :]).ravel() % n
        idx = idx[:n]
        yb, sb = y[idx], score[idx]
        if yb.min() == yb.max():
            continue
        vals.append(average_precision_score(yb, sb))
    if not vals:
        return None
    return [float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))]


def rf():
    return Pipeline([
        ("imp", SimpleImputer(strategy="median")),
        ("clf", RandomForestClassifier(n_estimators=300, min_samples_leaf=5,
                                       class_weight="balanced_subsample",
                                       random_state=SEED, n_jobs=-1)),
    ])


def rf_depth():
    return Pipeline([
        ("imp", SimpleImputer(strategy="median")),
        ("clf", RandomForestClassifier(n_estimators=300, min_samples_leaf=5,
                                       class_weight="balanced_subsample",
                                       random_state=SEED, n_jobs=-1)),
    ])


def logreg():
    return Pipeline([
        ("imp", SimpleImputer(strategy="median")),
        ("sc", StandardScaler()),
        ("clf", LogisticRegression(class_weight="balanced", max_iter=1000,
                                   random_state=SEED)),
    ])


def main():
    t_start = time.time()
    # ---- muat semua jendela ----
    data = {}
    for f in sorted(os.listdir(WIN)):
        if not f.endswith(".csv.gz"):
            continue
        well = f.replace(".csv.gz", "")
        d = pd.read_csv(os.path.join(WIN, f))
        data[well] = d
    wells = list(data)
    log(f"wells: {wells}")

    # asersi anti-leak: tidak ada kolom label/eligibility di FEATS
    for bad in ("feat_drill_bins", "feat_drill_rows", "feat_valid", "ssi_val"):
        assert bad not in FEATS, bad
    for cl in CLASSES:
        for c in FEATS:
            assert not c.startswith("y_"), c
            assert not c.startswith("valid_"), c
            assert not c.startswith("nobs_"), c
            assert not c.startswith("obs_"), c
            assert not c.startswith("y_prev"), c
    log("assertions on feature list: PASS")

    results = {"prereg_sha256": "542772622d2d3539df35f484fa0a67869d485a3ff6944fab5fbd45252928e9fc",
               "classes": {}, "meta": {"n_boot": N_BOOT, "block": BLOCK,
                                        "min_pos_eval": MIN_POS_EVAL,
                                        "lift_gate": LIFT_GATE, "seed": SEED}}

    for cl in CLASSES:
        # periksa ketersediaan fitur per well
        avail = []
        for w in wells:
            d = data[w]
            need = FEATS + [f"valid_{cl}", f"y_{cl}", "feat_valid"]
            if not any(c in d.columns for c in FEATS):
                continue
            sub = d[(d["feat_valid"]) & (d[f"valid_{cl}"].astype(bool))]
            if len(sub) == 0:
                continue
            avail.append(w)
        folds = []
        log(f"\n=== kelas {cl}: sumur eligible = {avail}")
        for w_te in avail:
            # train = semua well selain w_te yang punya data kelas ini
            tr_parts = [data[w][lambda x: x["feat_valid"] & x[f"valid_{cl}"].astype(bool)]
                        for w in avail if w != w_te]
            tr = pd.concat(tr_parts, ignore_index=True) if tr_parts else None
            te = data[w_te][lambda x: x["feat_valid"] & x[f"valid_{cl}"].astype(bool)].copy()
            if tr is None or len(tr) == 0:
                log(f"  {w_te}: TIDAK ADA data latih -> skip fold")
                continue
            y_tr = tr[f"y_{cl}"].to_numpy().astype(int)
            y_te = te[f"y_{cl}"].to_numpy().astype(int)
            X_tr = tr[FEATS].apply(pd.to_numeric, errors="coerce")
            X_te = te[FEATS].apply(pd.to_numeric, errors="coerce")
            # urutkan waktu untuk bootstrap berblok
            order = np.argsort(te["ts_bin"].to_numpy())
            y_te = y_te[order]
            X_te = X_te.iloc[order]
            te = te.iloc[order]
            n_pos = int(y_te.sum())
            prev = float(y_te.mean())
            fold = {"well": w_te, "n_train": int(len(tr)), "n_test": int(len(y_te)),
                    "n_pos": n_pos, "prev": prev, "underpowered": n_pos < MIN_POS_EVAL}
            if len(np.unique(y_tr)) < 2:
                log(f"  {w_te}: data latih hanya 1 kelas -> skip fold")
                fold["skipped"] = "train single class"
                folds.append(fold)
                continue
            t0 = time.time()
            m = rf().fit(X_tr, y_tr)
            s_rf = m.predict_proba(X_te)[:, 1]
            md = rf_depth().fit(X_tr[DEPTH_FEATS], y_tr)
            s_dep = md.predict_proba(X_te[DEPTH_FEATS])[:, 1]
            ml = logreg().fit(X_tr, y_tr)
            s_lr = ml.predict_proba(X_te)[:, 1]
            fold["auprc_rf"] = float(average_precision_score(y_te, s_rf))
            fold["auprc_logreg"] = float(average_precision_score(y_te, s_lr))
            fold["auprc_depth"] = float(average_precision_score(y_te, s_dep))
            fold["roc_rf"] = float(roc_auc_score(y_te, s_rf)) if len(np.unique(y_te)) > 1 else None
            fold["lift_rf"] = fold["auprc_rf"] / prev if prev > 0 else None
            fold["lift_logreg"] = fold["auprc_logreg"] / prev if prev > 0 else None
            fold["lift_depth"] = fold["auprc_depth"] / prev if prev > 0 else None
            fold["ci95_rf"] = moving_block_ci(y_te, s_rf)
            # persistence: y_prev (skor biner) pada subset valid_prev
            if f"y_prev_{cl}" in te.columns and f"valid_prev_{cl}" in te.columns:
                pv = te[f"valid_prev_{cl}"].to_numpy() > 0
                if pv.sum() > 0 and len(np.unique(y_te[pv])) > 1:
                    fold["auprc_persistence"] = float(
                        average_precision_score(y_te[pv], te[f"y_prev_{cl}"].to_numpy()[pv]))
                    fold["n_persistence"] = int(pv.sum())
                else:
                    fold["auprc_persistence"] = None
                    fold["n_persistence"] = int(pv.sum())
            fold["fit_time_s"] = round(time.time() - t0, 1)
            log(f"  {w_te}: n_test={fold['n_test']} pos={n_pos} prev={prev:.4f} "
                f"AUPRC_rf={fold['auprc_rf']:.4f} lift={fold['lift_rf']} "
                f"depth={fold['auprc_depth']:.4f} logreg={fold['auprc_logreg']:.4f} "
                f"persist={fold.get('auprc_persistence')} "
                f"ci={fold['ci95_rf']} ({fold['fit_time_s']}s)")
            folds.append(fold)
        # gate
        evaluable = [f for f in folds if not f.get("skipped") and not f["underpowered"]
                     and f.get("lift_rf") is not None]
        n_eval = len(evaluable)
        g1 = sum(1 for f in evaluable if f["lift_rf"] >= LIFT_GATE)
        g2 = sum(1 for f in evaluable if f["auprc_rf"] >= f["auprc_depth"])
        verdict = {
            "n_folds": len(folds), "n_evaluable": n_eval,
            "g1_pass_folds": g1, "g2_pass_folds": g2,
            "G1": (g1 > n_eval / 2) if n_eval else None,
            "G2": (g2 > n_eval / 2) if n_eval else None,
        }
        verdict["kelas"] = ("LULUS" if (verdict["G1"] and verdict["G2"]) else
                            "GAGAL" if n_eval else "TIDAK BISA DINILAI")
        # persistence dominance check
        pd_folds = [f for f in evaluable if f.get("auprc_persistence") is not None]
        pd_lose = sum(1 for f in pd_folds if f["auprc_persistence"] > f["auprc_rf"])
        verdict["persistence_folds"] = len(pd_folds)
        verdict["persistence_beats_rf"] = pd_lose
        if verdict["kelas"] == "LULUS" and pd_folds and pd_lose > len(pd_folds) / 2:
            verdict["kelas"] = "LAYAK BERSYARAT (persistence > model)"
        results["classes"][cl] = {"folds": folds, "verdict": verdict}
        log(f"  >> {cl}: {verdict}")

    results["meta"]["elapsed_s"] = round(time.time() - t_start, 1)
    json.dump(results, open(OUT, "w"), indent=1)
    open(LOG, "w").write("\n".join(log_lines))
    # ringkas gate
    n_lulus = sum(1 for cl in CLASSES
                  if results["classes"].get(cl, {}).get("verdict", {}).get("kelas") == "LULUS")
    log(f"\nTOTAL kelas LULUS = {n_lulus} / {len(CLASSES)}")
    log(f"saved {OUT}")


if __name__ == "__main__":
    main()
