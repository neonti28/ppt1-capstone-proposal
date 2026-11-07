#!/usr/bin/env python3
"""J2 kampanye deteksi stuck (STUCK_RT) — eksekusi protokol V5_J2_PREREG.md.

Tugas A: kontemporer (bin 30s, positif bila kode dominan > 0).
Tugas B: dini (onset dalam 10 menit setelah jendela fitur).
E1: kronologis 70/30 per wellbore (tanpa shuffle).
E2: cross-well F-9_A -> F-14 / F-9 (kanal diseragamkan tanpa RPM).
GATE G1/G2/G3 dikunci di pra-registrasi; tidak boleh diubah di sini.
"""
import json
import numpy as np
import pandas as pd
from datetime import timedelta
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (average_precision_score, roc_auc_score,
                             precision_recall_fscore_support)

SEED = 20261010
RNG = np.random.default_rng(SEED)
DATA = "/mnt/d/Capstone 1/data/predictive/j2_stuck"
WELLS = ["F-9_A", "F-9", "F-14"]
CH9 = ["SPPA", "TQA", "TFLO", "HKLD", "SWOB", "RPM", "ROP", "BPOS"]  # DEPT dibuang: 0% di F-9/F-14 (fill check primer)
CH8 = [c for c in CH9 if c != "RPM"]  # common denominator lintas wellbore
BIN = "30s"
ROLL = 10        # 5 menit
HORIZON_MIN = 10


def load(well):
    df = pd.read_csv(f"{DATA}/{well}_window.csv",
                     dtype={"STUCK_RT": "float64"})
    df["ts"] = pd.to_datetime(df["timestamp"], format="ISO8601", utc=True)
    if "RPM" not in df.columns and "NRPM_RT" in df.columns:
        df = df.rename(columns={"NRPM_RT": "RPM"})
    for c in CH9:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
        else:
            df[c] = np.nan
    return df.sort_values("ts").reset_index(drop=True)


def make_bins(df, channels):
    """Resample 30s: median kanal; label = modus kode berlabel dalam bin."""
    df = df.set_index("ts")
    chan = df[channels].resample(BIN).median()
    # label dari baris berlabel saja
    lab = df["STUCK_RT"].dropna().resample(BIN).agg(
        lambda s: s.mode().iloc[0] if len(s.mode()) else np.nan)
    cnt = df["STUCK_RT"].dropna().resample(BIN).count()
    chan["code"] = lab
    chan["n_labeled"] = cnt
    chan = chan.reset_index()
    return chan


def add_features(bins, channels):
    """Fitur: rolling mean+std 10 bin TERAKHIR (termasuk bin kini; tanpa masa depan)."""
    out = bins.copy()
    for c in channels:
        out[f"{c}_m"] = bins[c].rolling(ROLL, min_periods=3).mean()
        out[f"{c}_s"] = bins[c].rolling(ROLL, min_periods=3).std()
    return out


def task_A(bins):
    b = bins.copy()
    b = b[b["n_labeled"] > 0]
    b["y"] = (b["code"] > 0).astype(int)
    return b.dropna(subset=["y"])


def task_B(bins):
    """Positif bila ada kode>0 dalam 10 menit SETELAH bin; buang bin saat/tepi event."""
    b = bins.copy()
    b = b[b["n_labeled"] > 0].reset_index(drop=True)
    active = (b["code"].fillna(0) > 0).values
    ts = b["ts"].values
    y = np.zeros(len(b), dtype=int)
    for i in range(len(b)):
        if active[i]:
            continue
        t0 = ts[i]
        t1 = t0 + np.timedelta64(HORIZON_MIN, "m")
        seg = (ts > t0) & (ts <= t1) & active
        y[i] = 1 if seg.any() else 0
    # exclude bin saat event (active) dan 10 menit setelah event terakhir
    excl = np.zeros(len(b), dtype=bool)
    last_active = -1
    for i in range(len(b)):
        if active[i]:
            last_active = i
        elif last_active >= 0 and (ts[i] - ts[last_active]) <= np.timedelta64(HORIZON_MIN, "m"):
            excl[i] = True
    b["y"] = y
    b["excl"] = excl
    return b[~b["excl"]].drop(columns=["excl"])


def feat_matrix(b, channels):
    cols = [f"{c}_m" for c in channels] + [f"{c}_s" for c in channels]
    return b[cols]


def drop_incomplete(b, channels):
    """Buang bin yang fiturnya tidak lengkap (gap waktu -> rolling NaN).
    Konsisten dengan pra-reg: 'bin tanpa fitur dibuang'."""
    cols = [f"{c}_m" for c in channels] + [f"{c}_s" for c in channels]
    return b.dropna(subset=cols).reset_index(drop=True)


def models():
    return {
        "logreg": Pipeline([("sc", StandardScaler()),
                            ("clf", LogisticRegression(max_iter=2000, C=1.0,
                                                       class_weight="balanced",
                                                       random_state=SEED))]),
        "rf": Pipeline([("clf", RandomForestClassifier(
            n_estimators=300, class_weight="balanced_subsample",
            min_samples_leaf=5, random_state=SEED, n_jobs=-1))]),
    }


def recall_at_fpr(y, p, fpr_max=0.05):
    order = np.argsort(-p)
    ys = y[order]
    n_pos = ys.sum()
    n_neg = len(ys) - n_pos
    if n_pos == 0 or n_neg == 0:
        return None
    tp = np.cumsum(ys)
    fp = np.cumsum(1 - ys)
    fpr = fp / n_neg
    ok = fpr <= fpr_max
    if not ok.any():
        return 0.0
    return float((tp[ok] / n_pos).max())


def block_bootstrap_ap(y, p, n_boot=1000, block=20, seed=SEED):
    rng = np.random.default_rng(seed)
    y = np.asarray(y); p = np.asarray(p)
    n = len(y)
    if n < block * 2:
        return None
    n_blocks = int(np.ceil(n / block))
    aps = []
    starts_pool = np.arange(n)
    for _ in range(n_boot):
        starts = rng.choice(starts_pool, size=n_blocks, replace=True)
        idx = np.concatenate([((s + np.arange(block)) % n) for s in starts])[:n]
        yy, pp = y[idx], p[idx]
        if yy.min() == yy.max():
            continue
        aps.append(average_precision_score(yy, pp))
    if not aps:
        return None
    return {"ap_mean": float(np.mean(aps)),
            "ci_lo": float(np.percentile(aps, 2.5)),
            "ci_hi": float(np.percentile(aps, 97.5)),
            "n_valid": len(aps)}


def eval_pair(y, p):
    out = {"pr_auc": float(average_precision_score(y, p)),
           "prevalence": float(np.mean(y)),
           "roc_auc": float(roc_auc_score(y, p)) if len(set(y)) > 1 else None,
           "recall_at_fpr5": recall_at_fpr(y, p),
           "n": int(len(y)), "n_pos": int(np.sum(y))}
    pred05 = (p >= 0.5).astype(int)
    pr, rc, f1, _ = precision_recall_fscore_support(
        y, pred05, average="binary", zero_division=0)
    out["at_0.5"] = {"precision": float(pr), "recall": float(rc), "f1": float(f1)}
    best_f1, best_t = -1, None
    for t in np.unique(p):
        pr, rc, f1, _ = precision_recall_fscore_support(
            y, (p >= t).astype(int), average="binary", zero_division=0)
        if f1 > best_f1:
            best_f1, best_t = f1, float(t)
    out["best_f1_exploratif"] = {"f1": float(best_f1), "threshold": best_t}
    out["bootstrap"] = block_bootstrap_ap(y, p)
    return out


def main():
    results = {"seed": SEED, "bin": BIN, "roll_bins": ROLL,
               "horizon_min": HORIZON_MIN, "wells": {},
               "deviasi_protokol": [
                   "Kanal DEPT dibuang dari set fitur SETELAH fill-check primer "
                   "menunjukkan 0% pada bin berlabel F-9 dan F-14 (DEPT hanya ada "
                   "di F-9_A); tanpa penghapusan ini E1 F-9/F-14 kosong total.",
                   "Koreksi bug pred_store Task B (tak tersimpan -> pooled Task B "
                   "identik Task A pada run pertama); run final memakai prefix E1B.",
                   "Fix NaN pada fitur rolling: bin dengan fitur tidak lengkap "
                   "dibuang (konsisten klausa pra-reg 'bin tanpa fitur dibuang').",
               ]}
    pred_store = {}

    # ---- build per well ----
    built = {}
    for w in WELLS:
        df = load(w)
        bins = make_bins(df, CH9)
        feat = add_features(bins, CH9)
        ta = task_A(feat).reset_index(drop=True)
        tb = task_B(feat).reset_index(drop=True)
        built[w] = {"bins": feat, "A": ta, "B": tb}
        results["wells"][w] = {
            "rows_window": int(len(df)),
            "bins_total": int(len(bins)),
            "bins_labeled": int(len(ta)),
            "A_prevalence": float(ta["y"].mean()),
            "B_prevalence": float(tb["y"].mean()),
        }

    # ---- E1 kronologis per well, Task A & B ----
    e1 = {}
    for task in ("A", "B"):
        e1[task] = {}
        for w in WELLS:
            b = drop_incomplete(built[w][task], CH9)
            split = int(len(b) * 0.7)
            tr, te = b.iloc[:split], b.iloc[split:]
            Xtr = feat_matrix(tr, CH9); Xte = feat_matrix(te, CH9)
            ytr = tr["y"].values; yte = te["y"].values
            entry = {"n_train": int(len(tr)), "n_test": int(len(te)),
                     "prev_train": float(ytr.mean()) if len(ytr) else None,
                     "prev_test": float(yte.mean()) if len(yte) else None}
            if len(ytr) == 0 or len(yte) == 0 or len(set(yte)) < 2:
                entry["note"] = "kosong/monokelas setelah dropna; model tidak dievaluasi"
                e1[task][w] = entry
                continue
            # majority baseline
            maj = np.full(len(yte), ytr.mean())
            entry["majority_pr_auc"] = float(average_precision_score(yte, maj)) if len(set(yte)) > 1 else None
            # persistence: label bin berlabel sebelumnya (Task A only meaningful; still compute)
            prev = tr["y"].values[-1]
            pers = []
            for _, row in te.iterrows():
                pers.append(prev)
                if not np.isnan(row["code"]):
                    prev = int(row["code"] > 0)
            entry["persistence_pr_auc"] = float(average_precision_score(yte, pers)) if len(set(yte)) > 1 else None
            for name, mdl in models().items():
                mdl.fit(Xtr, ytr)
                p = mdl.predict_proba(Xte)[:, 1]
                entry[name] = eval_pair(yte, p)
                if task == "A":
                    pred_store[f"E1_{w}_{name}"] = {"y": yte.tolist(), "p": p.tolist()}
                else:
                    pred_store[f"E1B_{w}_{name}"] = {"y": yte.tolist(), "p": p.tolist()}
            e1[task][w] = entry
        # pooled G1 pakai logreg (dari pred_store; prefix per tugas)
        pref = "E1" if task == "A" else "E1B"
        py, pp = [], []
        for w in WELLS:
            key = f"{pref}_{w}_logreg"
            if key not in pred_store:
                continue
            yw = np.array(pred_store[key]["y"])
            pw = np.array(pred_store[key]["p"])
            py.extend(yw.tolist()); pp.extend(pw.tolist())
        e1[task]["pooled_logreg"] = (eval_pair(np.array(py), np.array(pp))
                                     if len(set(py)) > 1 else
                                     {"note": "pooled kosong/monokelas"})
    results["E1"] = e1

    # ---- Task B tambahan khusus F-9_A (G3) sudah di E1["B"]["F-9_A"] ----

    # ---- E2 cross-well (kanal 8, tanpa RPM) ----
    e2 = {}
    tr_b = drop_incomplete(built["F-9_A"]["A"], CH8)
    for target in ("F-14", "F-9"):
        te_b = drop_incomplete(built[target]["A"], CH8)
        Xtr = feat_matrix(tr_b, CH8); Xte = feat_matrix(te_b, CH8)
        ytr = tr_b["y"].values; yte = te_b["y"].values
        entry = {"n_train": int(len(tr_b)), "n_test": int(len(te_b)),
                 "prev_train": float(ytr.mean()) if len(ytr) else None,
                 "prev_test": float(yte.mean()) if len(yte) else None}
        if len(ytr) == 0 or len(yte) == 0 or len(set(yte)) < 2:
            entry["note"] = "kosong/monokelas setelah dropna; model tidak dievaluasi"
            e2[target] = entry
            continue
        for name, mdl in models().items():
            mdl.fit(Xtr, ytr)
            p = mdl.predict_proba(Xte)[:, 1]
            entry[name] = eval_pair(yte, p)
            pred_store[f"E2_{target}_{name}"] = {"y": yte.tolist(), "p": p.tolist()}
        e2[target] = entry
    results["E2"] = e2

    # ---- GATE ----
    pooled = e1["A"].get("pooled_logreg", {})
    g1_ap = pooled.get("pr_auc"); g1_prev = pooled.get("prevalence")
    g1_boot = pooled.get("bootstrap")
    G1 = bool(g1_ap is not None and g1_prev is not None and g1_boot
              and g1_ap >= g1_prev + 0.15 and g1_boot["ci_lo"] > g1_prev)
    e2_entry = e2["F-14"].get("logreg", {})
    G2 = bool(e2_entry.get("pr_auc") is not None and e2_entry.get("prev_test") is not None
              and e2_entry["pr_auc"] >= e2_entry["prev_test"] + 0.10)
    b_f9a = e1["B"]["F-9_A"].get("logreg", {})
    G3 = bool(b_f9a.get("recall_at_fpr5") is not None and b_f9a["recall_at_fpr5"] >= 0.50)
    results["GATES"] = {
        "G1": {"pass": G1, "pooled_logreg_pr_auc": g1_ap,
               "pooled_prevalence": g1_prev, "bootstrap_ci": g1_boot,
               "criterion": "pr_auc >= prev+0.15 AND ci_lo > prev"},
        "G2": {"pass": G2, "f9a_to_f14_logreg_pr_auc": e2_entry.get("pr_auc"),
               "f14_prevalence": e2["F-14"].get("prev_test"),
               "criterion": "pr_auc >= prev+0.10"},
        "G3": {"pass": G3, "taskB_f9a_logreg_recall_at_fpr5": b_f9a.get("recall_at_fpr5"),
               "criterion": "recall@FPR<=5% >= 0.50"},
        "VERDICT": "LAYAK" if G1 else "TIDAK LAYAK",
    }

    # ---- determinism re-run check (logreg E1 F-9_A) ----
    b = drop_incomplete(built["F-9_A"]["A"], CH9)
    split = int(len(b) * 0.7)
    tr, te = b.iloc[:split], b.iloc[split:]
    mdl1 = models()["logreg"]
    mdl1.fit(feat_matrix(tr, CH9), tr["y"].values)
    p1 = mdl1.predict_proba(feat_matrix(te, CH9))[:, 1]
    mdl2 = models()["logreg"]
    mdl2.fit(feat_matrix(tr, CH9), tr["y"].values)
    p2 = mdl2.predict_proba(feat_matrix(te, CH9))[:, 1]
    results["determinism_check"] = {
        "identical_logreg_rerun": bool(np.array_equal(p1, p2))}

    # ---- simpan ----
    with open(f"{DATA}/j2_predictions.json", "w") as fh:
        json.dump(pred_store, fh)
    with open("/mnt/d/Capstone 1/docs/V5_J2_STUCK.json", "w") as fh:
        json.dump(results, fh, indent=1)
    print(json.dumps(results["GATES"], indent=1))
    print("wells:", json.dumps(results["wells"], indent=1))


if __name__ == "__main__":
    main()
