#!/usr/bin/env python3
"""V6-E1 40 — SHAP (deskriptif) untuk RF tiap kelas, fold = kelompok (sumur/alat) terbesar.

Mengikuti prereg E1a §8.2: TreeExplainer via shap.Explainer, background 200 baris latih
(seed 42), 200 baris uji OOF (seed 42), output = prob kelas positif, cek additivity.
Kelas: stuck/vib/shk/ssi (E1a), hyd (E1b), tool_wear (E1c), bit_wear (E1d).
Output: scratch/v6_e1/E1_SHAP.json + E1_SHAP_<kelas>.png
"""
import json
import os
import numpy as np
import pandas as pd
import shap
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer

SEED = 42
SC = "/mnt/d/Capstone 1/scratch/v6_e1"
OUT = f"{SC}/E1_SHAP.json"
STATS = ["mean", "std", "slope", "last", "frac"]
ALL_CHAN = ["TQA", "SPPA", "TFLO", "RPM", "SWOB", "HKLD", "ROP", "BPOS", "SPM", "depth", "dbtm"]
MECH_CHAN = ["TQA", "RPM", "SWOB", "HKLD", "ROP", "BPOS", "depth", "dbtm"]
USROP_CHAN = ["SPP", "FLOW", "MUD", "GAM", "MD", "TVD"]
F_ALL = [f"{c}_{s}" for c in ALL_CHAN for s in STATS]
F_MECH = [f"{c}_{s}" for c in MECH_CHAN for s in STATS]
F_USROP = [f"{c}_{s}" for c in USROP_CHAN for s in STATS]
F_TOOL = None  # ditentukan dari CSV

JOBS = [
    # name, path (dir .csv.gz atau file csv), ycol, groupcol, validcol(None=semua baris), feats, filter_feat_valid
    ("stuck", f"{SC}/windows", None, "stuck", "well", "valid_stuck", F_ALL, True),
    ("vib", f"{SC}/windows", None, "vib", "well", "valid_vib", F_ALL, True),
    ("shk", f"{SC}/windows", None, "shk", "well", "valid_shk", F_ALL, True),
    ("ssi", f"{SC}/windows", None, "ssi", "well", "valid_ssi", F_ALL, True),
    ("hyd", f"{SC}/windows_hyd", None, "y_hyd", "well", "valid_hyd", F_MECH, True),
    ("tool_wear", f"{SC}/toolwear_windows.csv", "y", None, "tool", None, F_TOOL, False),
    ("bit_wear", f"{SC}/usrop_windows.csv", "y_bitwear", None, "well", None, F_USROP, False),
]


def load(path, ycol, validcol, filt):
    frames = []
    if os.path.isdir(path):
        for f in sorted(os.listdir(path)):
            if f.endswith(".csv.gz"):
                d = pd.read_csv(os.path.join(path, f))
                if "well" not in d.columns:
                    d["well"] = f.replace(".csv.gz", "")
                frames.append(d)
        df = pd.concat(frames, ignore_index=True)
    else:
        df = pd.read_csv(path)
    if ycol:
        y = ycol
    else:
        y = f"y_{validcol.replace('valid_', '')}"
    mask = pd.Series(True, index=df.index)
    if filt:
        mask &= df["feat_valid"].astype(bool)
    if validcol:
        mask &= df[validcol].astype(bool)
    return df[mask].copy(), y


res = {}
for name, path, ycol, yname, gcol, validcol, feats, filt in JOBS:
    df, y = load(path, ycol, validcol, filt)
    if y not in df.columns:
        y = f"y_{name}" if f"y_{name}" in df.columns else y
    if feats is None:
        feats = [c for c in df.columns if c not in (y, gcol, "file", "run", "start_sample",
                                                    "anchor_depth", "frac_pos_label_window",
                                                    "y_prev", "y_prev_hyd", "valid_prev_hyd",
                                                    "valid_prev_stuck", "valid_prev_vib",
                                                    "valid_prev_shk", "valid_prev_ssi",
                                                    "obs_hyd", "anom_hyd", "ssi_val",
                                                    "feat_valid", "feat_drill_bins",
                                                    "feat_drill_rows")]
        feats = [c for c in feats if df[c].dtype != object]
    groups = sorted(df[gcol].unique())
    sizes = {g: int((df[gcol] == g).sum()) for g in groups}
    g_te = max(sizes, key=sizes.get)
    tr, te = df[df[gcol] != g_te], df[df[gcol] == g_te]
    y_tr = tr[y].to_numpy().astype(int)
    y_te = te[y].to_numpy().astype(int)
    if len(np.unique(y_tr)) < 2 or len(np.unique(y_te)) < 2:
        res[name] = {"error": "single class in train/test", "group": g_te}
        print(name, "SKIP single class", g_te, flush=True)
        continue
    X_tr, X_te = tr[feats].apply(pd.to_numeric, errors="coerce"), te[feats].apply(pd.to_numeric, errors="coerce")
    imp = SimpleImputer(strategy="median", keep_empty_features=True).fit(X_tr)
    Xt = pd.DataFrame(imp.transform(X_tr), columns=feats)
    Xv = pd.DataFrame(imp.transform(X_te), columns=feats)
    clf = RandomForestClassifier(n_estimators=300, min_samples_leaf=5,
                                 class_weight="balanced_subsample", random_state=SEED,
                                 n_jobs=-1).fit(Xt, y_tr)
    rng = np.random.default_rng(SEED)
    bg = rng.choice(len(Xt), size=min(200, len(Xt)), replace=False)
    ix = rng.choice(len(Xv), size=min(200, len(Xv)), replace=False)
    explainer = shap.Explainer(clf, Xt.iloc[bg], algorithm="tree")
    exp = explainer(Xv.iloc[ix])
    pos = exp[..., 1] if exp.values.ndim == 3 else exp
    recon = np.asarray(pos.base_values) + pos.values.sum(axis=1)
    expected = clf.predict_proba(Xv.iloc[ix])[:, 1]
    err = float(np.max(np.abs(recon - expected)))
    mabs = np.abs(pos.values).mean(axis=0)
    order = np.argsort(-mabs)
    top = {feats[i]: float(mabs[i]) for i in order[:15]}
    res[name] = {"group_test": g_te, "n_train": len(Xt), "n_explained": len(ix),
                 "additivity_max_abs_err": err, "additivity_ok": bool(err < 1e-5),
                 "shap_version": shap.__version__, "output": "P(class=1)",
                 "background": f"{len(bg)} baris latih (seed {SEED})",
                 "top_features_mean_abs_shap": top,
                 "y_pos_explained": int(y_te[ix].sum())}
    print(name, "group=", g_te, "additivity_err=", round(err, 8),
          "top:", list(top)[:6], flush=True)
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        shap.plots.bar(pos.mean_abs(), max_display=15, show=False)
        plt.title(f"V6-E1 SHAP mean|value| — {name} (test {g_te})")
        plt.tight_layout()
        plt.savefig(f"{SC}/E1_SHAP_{name}.png", dpi=120)
        plt.close()
    except Exception as e:
        res[name]["plot_error"] = str(e)

json.dump(res, open(OUT, "w"), indent=1)
print("saved", OUT)
