#!/usr/bin/env python3
"""V6-E1d 61 — training + LOWO kelas `bit_wear` (USROP Volve).

Mengikuti pra-registrasi docs/V6_E1d_PREREG_BITWEAR.md
(SHA-256 986f45a1fbf866434e05b3aecfbc8c53fa1672e2caef98d7470a38ea8c03f1a6).
Gate: G1 lift>=1.5 di >=3/4 fold layak; G2 RF >= canary kedalaman (MD+TVD) di >=3/4 fold.
Kanal sirkular (WOB/TQ/RPM/ROP/Hookload/MSE/D_exp/ROC_coef) DILARANG di fitur (asersi).
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

CSV = "/mnt/d/Capstone 1/scratch/v6_e1/usrop_windows.csv"
OUT = "/mnt/d/Capstone 1/scratch/v6_e1/E1d_LOWO_RESULTS.json"
LOG = "/mnt/d/Capstone 1/scratch/v6_e1/E1d_LOWO_RUN_LOG.txt"
SEED, N_BOOT, BLOCK, MIN_POS, LIFT_GATE = 42, 1000, 20, 30, 1.5
STATS = ["mean", "std", "slope", "last", "frac"]
CH = ["SPP", "FLOW", "MUD", "GAM", "MD", "TVD"]
FEATS = [f"{c}_{s}" for c in CH for s in STATS]
DEPTH = [f"{c}_{s}" for c in ("MD", "TVD") for s in STATS]
BANNED_SUB = ("WOB", "TQ", "RPM", "ROP", "HKLD", "MSE", "D_exp", "ROC")
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
    df = pd.read_csv(CSV).sort_values(["well", "anchor_depth"]).reset_index(drop=True)
    assert all(c in df.columns for c in FEATS), [c for c in FEATS if c not in df.columns]
    for b in BANNED_SUB:
        assert not any(b in c for c in FEATS), b
    assert "label" not in FEATS and "well" not in FEATS
    log(f"features ({len(FEATS)}): {FEATS}")
    # persistence = label jendela sebelumnya dalam sumur yang sama (shift 1)
    df["y_prev"] = df.groupby("well")["y_bitwear"].shift(1)
    wells = sorted(df["well"].unique())
    folds = []
    for w_te in wells:
        tr = df[df["well"] != w_te]
        te = df[df["well"] == w_te].copy()
        y_tr = tr["y_bitwear"].to_numpy().astype(int)
        y_te = te["y_bitwear"].to_numpy().astype(int)
        prev = float(y_te.mean())
        f = {"well": w_te, "n_train": int(len(tr)), "n_test": int(len(te)),
             "n_pos": int(y_te.sum()), "prev": prev,
             "underpowered": int(y_te.sum()) < MIN_POS,
             "no_positives": int(y_te.sum()) == 0}
        if f["underpowered"]:
            log(f"  {w_te}: n_test={len(te)} pos={f['n_pos']} prev={prev:.4f} -> "
                f"{'TIDAK BERNILAI (0 positif)' if f['no_positives'] else 'UNDERPOWERED (<30 pos)'} "
                f"— tidak dihitung gate")
            folds.append(f)
            continue
        if len(np.unique(y_tr)) < 2:
            f["skipped"] = "train single class"
            folds.append(f)
            continue
        s = time.time()
        m = mk_rf().fit(tr[FEATS], y_tr); s_rf = m.predict_proba(te[FEATS])[:, 1]
        mc = mk_rf().fit(tr[DEPTH], y_tr); s_dep = mc.predict_proba(te[DEPTH])[:, 1]
        ml = mk_lr().fit(tr[FEATS], y_tr); s_lr = ml.predict_proba(te[FEATS])[:, 1]
        f["auprc_rf"] = float(average_precision_score(y_te, s_rf))
        f["auprc_logreg"] = float(average_precision_score(y_te, s_lr))
        f["auprc_depth"] = float(average_precision_score(y_te, s_dep))
        f["roc_rf"] = float(roc_auc_score(y_te, s_rf))
        f["lift_rf"] = f["auprc_rf"] / prev if prev else None
        f["lift_depth"] = f["auprc_depth"] / prev if prev else None
        f["ci95_rf"] = mblock_ci(y_te, s_rf)
        pv = te["y_prev"].notna().to_numpy()
        f["auprc_persistence"] = (float(average_precision_score(y_te[pv], te["y_prev"].to_numpy()[pv]))
                                  if pv.sum() and len(np.unique(y_te[pv])) > 1 else None)
        f["n_persistence"] = int(pv.sum())
        f["fit_time_s"] = round(time.time() - s, 1)
        log(f"  {w_te}: n_test={len(te)} pos={f['n_pos']} prev={prev:.4f} "
            f"AUPRC_rf={f['auprc_rf']:.4f} lift={f['lift_rf']:.3f} depth={f['auprc_depth']:.4f} "
            f"logreg={f['auprc_logreg']:.4f} persist={f['auprc_persistence']} "
            f"ci={f['ci95_rf']} ({f['fit_time_s']}s)")
        folds.append(f)
    ev = [f for f in folds if not f.get("underpowered") and not f.get("skipped")
          and f.get("lift_rf") is not None]
    n = len(ev)
    g1 = sum(1 for f in ev if f["lift_rf"] >= LIFT_GATE)
    g2 = sum(1 for f in ev if f["auprc_rf"] >= f["auprc_depth"])
    pd_f = [f for f in ev if f.get("auprc_persistence") is not None]
    pd_lose = sum(1 for f in pd_f if f["auprc_persistence"] > f["auprc_rf"])
    v = {"n_folds": len(folds), "n_evaluable": n, "g1_pass": g1, "g2_pass": g2,
         "G1": g1 >= 3, "G2": g2 >= 3, "persistence_folds": len(pd_f),
         "persistence_beats_rf": pd_lose}
    v["kelas"] = ("LULUS" if v["G1"] and v["G2"] else "GAGAL" if n else "TIDAK BISA DINILAI")
    if v["kelas"] == "LULUS" and pd_f and pd_lose > len(pd_f) / 2:
        v["kelas"] = "LAYAK BERSYARAT (persistence > model)"
    res = {"prereg_sha256": "986f45a1fbf866434e05b3aecfbc8c53fa1672e2caef98d7470a38ea8c03f1a6",
           "class": "bit_wear", "folds": folds, "verdict": v,
           "meta": {"n_boot": N_BOOT, "block": BLOCK, "seed": SEED, "features": FEATS,
                    "split": "Leave-One-Well-Out", "elapsed_s": round(time.time() - t0, 1)}}
    json.dump(res, open(OUT, "w"), indent=1)
    open(LOG, "w").write("\n".join(log_lines))
    log(f">> bit_wear: {v}")


if __name__ == "__main__":
    main()
