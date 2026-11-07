#!/usr/bin/env python3
"""V6-E1c 51 — training + Leave-One-Tool-Out kelas `tool_wear` (eksternal Mendeley).

Mengikuti pra-registrasi docs/V6_E1c_PREREG_TOOLWEAR.md
(SHA-256 e2179bdeef64bcf01d71b50d8354008858c0fd9fea3b272af56a76c7dc86550b).
Gate: G1 lift>=1.5 di >=3/4 fold; G2 RF >= canary-amplitudo (X/Y/Z_rms) di >=3/4 fold.
"""
import json
import time
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import average_precision_score, roc_auc_score

CSV = "/mnt/d/Capstone 1/scratch/v6_e1/toolwear_windows.csv"
OUT = "/mnt/d/Capstone 1/scratch/v6_e1/E1c_LOWO_RESULTS.json"
LOG = "/mnt/d/Capstone 1/scratch/v6_e1/E1c_LOWO_RUN_LOG.txt"
SEED, N_BOOT, BLOCK, MIN_POS, LIFT_GATE = 42, 1000, 10, 30, 1.5
META = ["tool", "run", "file", "start_sample", "y"]
log_lines = []


def log(m):
    print(m, flush=True)
    log_lines.append(m)


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


def mblock_ci(y, s, n_boot=N_BOOT, block=BLOCK, seed=SEED):
    rng = np.random.default_rng(seed)
    n = len(y)
    if n < 2 * block or y.sum() in (0, n):
        return None
    nb = int(np.ceil(n / block))
    vals = []
    for _ in range(n_boot):
        st = rng.choice(np.arange(n), size=nb, replace=True)
        idx = ((st[:, None] + np.arange(block)[None, :]).ravel() % n)[:n]
        if y[idx].min() == y[idx].max():
            continue
        vals.append(average_precision_score(y[idx], s[idx]))
    return [float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))] if vals else None


def main():
    t0 = time.time()
    df = pd.read_csv(CSV)
    feats = [c for c in df.columns if c not in META]
    assert len(feats) == 27, feats
    for b in META:
        assert b not in feats
    log(f"features ({len(feats)}): {feats}")
    tools = sorted(df["tool"].unique())
    folds = []
    for w_te in tools:
        tr, te = df[df["tool"] != w_te], df[df["tool"] == w_te].copy()
        y_tr, y_te = tr["y"].to_numpy().astype(int), te["y"].to_numpy().astype(int)
        X_tr, X_te = tr[feats], te[feats]
        # urutkan dalam-file (start_sample) untuk bootstrap berblok
        o = np.lexsort((te["start_sample"].to_numpy(), te["file"].to_numpy()))
        y_te, X_te, te = y_te[o], X_te.iloc[o], te.iloc[o]
        prev = float(y_te.mean())
        f = {"tool": w_te, "n_train": int(len(tr)), "n_test": int(len(te)),
             "n_pos": int(y_te.sum()), "prev": prev,
             "underpowered": int(y_te.sum()) < MIN_POS}
        s = time.time()
        m = mk_rf().fit(X_tr, y_tr); s_rf = m.predict_proba(X_te)[:, 1]
        mc = mk_rf().fit(X_tr[["X_rms", "Y_rms", "Z_rms"]], y_tr)
        s_can = mc.predict_proba(X_te[["X_rms", "Y_rms", "Z_rms"]])[:, 1]
        ml = mk_lr().fit(X_tr, y_tr); s_lr = ml.predict_proba(X_te)[:, 1]
        f["auprc_rf"] = float(average_precision_score(y_te, s_rf))
        f["auprc_logreg"] = float(average_precision_score(y_te, s_lr))
        f["auprc_canary_rms"] = float(average_precision_score(y_te, s_can))
        f["roc_rf"] = float(roc_auc_score(y_te, s_rf))
        f["lift_rf"] = f["auprc_rf"] / prev if prev else None
        f["lift_canary"] = f["auprc_canary_rms"] / prev if prev else None
        f["ci95_rf"] = mblock_ci(y_te, s_rf)
        f["fit_time_s"] = round(time.time() - s, 1)
        log(f"  {w_te}: n_test={f['n_test']} pos={f['n_pos']} prev={prev:.3f} "
            f"AUPRC_rf={f['auprc_rf']:.4f} lift={f['lift_rf']:.3f} "
            f"canary_rms={f['auprc_canary_rms']:.4f} logreg={f['auprc_logreg']:.4f} "
            f"roc={f['roc_rf']:.3f} ci={f['ci95_rf']} ({f['fit_time_s']}s)")
        folds.append(f)
    ev = [f for f in folds if not f["underpowered"]]
    n = len(ev)
    g1 = sum(1 for f in ev if f["lift_rf"] >= LIFT_GATE)
    g2 = sum(1 for f in ev if f["auprc_rf"] >= f["auprc_canary_rms"])
    v = {"n_folds": len(folds), "n_evaluable": n, "g1_pass": g1, "g2_pass": g2,
         "G1": g1 >= 3, "G2": g2 >= 3, "persistence": "N/A (label konstan dalam file)"}
    v["kelas"] = ("LULUS" if v["G1"] and v["G2"] else "GAGAL" if n else "TIDAK BISA DINILAI")
    if v["kelas"] == "GAGAL" and v["G1"] and not v["G2"]:
        v["catatan"] = "G1 lolos tapi G2 gagal: sinyal hanya dari tingkat amplitudo"
    res = {"prereg_sha256": "e2179bdeef64bcf01d71b50d8354008858c0fd9fea3b272af56a76c7dc86550b",
           "class": "tool_wear", "source": "Mendeley th4yv974r2 (CC BY 4.0, SHA-256 verified 8/8)",
           "folds": folds, "verdict": v,
           "meta": {"n_boot": N_BOOT, "block": BLOCK, "seed": SEED,
                    "features": feats, "split": "Leave-One-Tool-Out",
                    "elapsed_s": round(time.time() - t0, 1)}}
    json.dump(res, open(OUT, "w"), indent=1)
    open(LOG, "w").write("\n".join(log_lines))
    log(f">> tool_wear: {v}")


if __name__ == "__main__":
    main()
