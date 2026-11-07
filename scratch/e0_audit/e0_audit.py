#!/usr/bin/env python3
"""E0 audit engine - pengukuran independen.

Tujuan: mengukur (1) kebocoran masa depan pada dataset yang benar-benar dipakai,
(2) dampak sirkularitas rule terhadap presisi, (3) determinisme rule + RF,
(4) penyebut FAR (cakupan waktu negatif), (5) rumus kuantil tool_wear.

Semua angka ditulis ke e0_audit_results.json. Tidak mengubah file apa pun di
workspace proyek (baca saja), kecuali folder kerja kartu ini.
"""
import hashlib
import importlib.util
import json
import os
import time
import traceback

import numpy as np
import pandas as pd

BASE = "/mnt/d/Capstone 1(v2)"
DS = f"{BASE}/scratch/v9_d1/datasets"
OUTDIR = "/home/neonti/.hermes/kanban/boards/rnd-algo-2026/workspaces/t_57e7d52b"
LOG = []


def log(m):
    line = f"[{time.strftime('%H:%M:%S')}] {m}"
    print(line, flush=True)
    LOG.append(line)


def load_rule_mod():
    spec = importlib.util.spec_from_file_location(
        "v9_e_rule01", f"{BASE}/code/v9_e_RULE_01_status.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def h(arr):
    return hashlib.sha256(np.ascontiguousarray(np.asarray(arr)).tobytes()).hexdigest()[:16]


def metrics(y, pred):
    y = np.asarray(y).astype(int)
    pred = np.asarray(pred).astype(int)
    tp = int(((pred == 1) & (y == 1)).sum())
    fp = int(((pred == 1) & (y == 0)).sum())
    fn = int(((pred == 0) & (y == 1)).sum())
    n_neg = int((y == 0).sum())
    p = tp / (tp + fp) if (tp + fp) else None
    r = tp / (tp + fn) if (tp + fn) else None
    return dict(n=int(len(y)), pos=int(y.sum()), neg=n_neg, tp=tp, fp=fp, fn=fn,
                P=None if p is None else round(p, 4),
                R=None if r is None else round(r, 4),
                far24=None if not n_neg else round(fp / (n_neg / 60.0) * 24.0, 3))


res = {}

# ---------------------------------------------------------------- 1. leakage
log("== 1. cek kebocoran masa depan pada dataset terpakai")
leak = {}
for eng in ["vib", "ssi", "shk", "stuck_k1", "hyd_ki", "stuck_k2"]:
    p = f"{DS}/{eng}.csv.gz"
    if not os.path.exists(p):
        leak[eng] = {"status": "file tidak ada"}
        continue
    cols = pd.read_csv(p, nrows=5).columns.tolist()
    df = pd.read_csv(p, usecols=[c for c in ("well", "ts_bin", "feat_ts_max", "lab_ts")
                                 if c in cols])
    ft = df["feat_ts_max"].to_numpy(dtype="float64")
    lt = df["lab_ts"].to_numpy(dtype="float64")
    tb = df["ts_bin"].to_numpy(dtype="float64")
    fin = np.isfinite(ft) & np.isfinite(lt)
    diff = ft[fin] - lt[fin]
    leak[eng] = {
        "n_rows": int(len(df)),
        "n_feat_ts_max_nan": int((~np.isfinite(ft)).sum()),
        "n_feat_ts_max_ge_lab_ts": int((diff >= 0).sum()),
        "max_feat_ts_max_minus_lab_ts": (None if diff.size == 0 else float(diff.max())),
        "min_feat_ts_max_minus_lab_ts": (None if diff.size == 0 else float(diff.min())),
        "n_feat_ts_max_ge_ts_bin": int((ft[fin] >= tb[fin]).sum()),
        "n_features": len([c for c in cols if c not in
                           ("well", "ts_bin", "feat_ts_max", "lab_ts", "lab_kind")
                           and not c.startswith(("y_", "valid_", "obs_", "anom_"))]),
        "label_channel_in_features": [c for c in cols
                                      if c.startswith(("vib_", "shk_", "stuck_", "crpm_"))
                                      or c.split("_")[0] in ("SPPA", "TFLO", "SPM")],
    }
    log(f"   {eng}: rows={leak[eng]['n_rows']} leak={leak[eng]['n_feat_ts_max_ge_lab_ts']} "
        f"labelch={leak[eng]['label_channel_in_features']}")
res["leakage"] = leak

# ------------------------------------------------- 2/3. rule, sirkularitas, FAR
log("== 2. rule: determinisme, sirkularitas, penyebut FAR")
r01 = load_rule_mod()
circ = {}
for cls in ["vib", "ssi", "shk", "stuck_k1", "hyd_ki"]:
    cfg = r01.CLS[cls]
    df = pd.read_csv(f"{DS}/{cls}.csv.gz")
    y = df[cfg["y"]].to_numpy().astype(int)
    yp = df[cfg["prev"]].to_numpy().astype(int)
    rp1, nd1 = r01.rule_display(cls, df)
    rp2, nd2 = r01.rule_display(cls, df)
    det = {"n": int(len(df)), "rule_hash_run1": h(rp1), "rule_hash_run2": h(rp2),
           "rule_bit_identik": h(rp1) == h(rp2),
           "nodata_hash_identik": h(nd1) == h(nd2)}
    m_all = metrics(y, rp1)
    m_on = metrics(y[yp == 1], rp1[yp == 1])       # sudah berlangsung
    m_new = metrics(y[yp == 0], rp1[yp == 0])      # onset baru (bukan sisa status)
    m_pers = metrics(y, yp)
    det["rule_all"] = m_all
    det["rule_subset_sudah_berlangsung"] = m_on
    det["rule_subset_onset_baru"] = m_new
    det["persistence_all"] = m_pers
    det["frac_pos_sudah_berlangsung"] = (round(float((yp[y == 1] == 1).mean()), 4)
                                         if y.sum() else None)
    det["frac_pos_onset_baru"] = (round(float((yp[y == 1] == 0).mean()), 4)
                                  if y.sum() else None)
    det["rule_pos_rate_pada_sudah_berlangsung"] = (
        round(float(rp1[yp == 1].mean()), 4) if (yp == 1).any() else None)
    det["rule_pos_rate_pada_onset_baru"] = (
        round(float(rp1[yp == 0].mean()), 4) if (yp == 0).any() else None)
    # penyebut FAR: cakupan waktu
    tb = df["ts_bin"].to_numpy(dtype="int64")
    cov = {}
    for w in np.unique(df["well"].to_numpy()):
        m = df["well"].to_numpy() == w
        span = int(tb[m].max() - tb[m].min() + 1)
        cov[str(w)] = {"n": int(m.sum()), "span_menit": span,
                       "cakupan": round(float(m.sum()) / span, 4)}
    det["cakupan_waktu_per_well"] = cov
    det["n_neg_dipakai_penyebut"] = int((y == 0).sum())
    det["jam_negatif_efektif"] = round(float((y == 0).sum()) / 60.0, 2)
    if cls == "stuck_k1":
        ep, end = r01.rule_e1(df)
        det["e1_all"] = metrics(y, ep)
        det["e1_subset_onset_baru"] = metrics(y[yp == 0], ep[yp == 0])
        det["e1_subset_sudah_berlangsung"] = metrics(y[yp == 1], ep[yp == 1])
    circ[cls] = det
    log(f"   {cls}: n={det['n']} ruleP={m_all['P']} ruleP_onset={m_new['P']} "
        f"ruleP_ongoing={m_on['P']} onset_frac={det['frac_pos_onset_baru']} "
        f"identik={det['rule_bit_identik']}")
res["rule"] = circ

# ---------------------------------- 2b. identitas rule-jendela-label (sirkular)
log("== 2b. identitas rule jendela-label vs label (sirkularitas konstruksi)")
ident = {}
for cls in ["vib", "ssi", "shk", "stuck_k1", "hyd_ki"]:
    df = pd.read_csv(f"{DS}/{cls}.csv.gz")
    try:
        ident[cls] = r01.rule_window_identity(cls, df)
    except Exception as e:
        ident[cls] = {"error": repr(e)}
    log(f"   {cls}: {ident[cls]}")
res["identity_rule_window_vs_label"] = ident

# ------------------------------------------------------ 4. determinisme RF
log("== 3. determinisme RF (dua fit, data sama)")
rfd = {}
try:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.impute import SimpleImputer
    dfv = pd.read_csv(f"{DS}/vib.csv.gz")
    feats = [c for c in dfv.columns
             if c not in r01.META and not c.startswith(("y_", "valid_", "obs_", "anom_"))]
    te_well = sorted(dfv["well"].unique())[0]
    tr = dfv[dfv["well"] != te_well]
    te = dfv[dfv["well"] == te_well].sort_values("ts_bin")
    imp = SimpleImputer(strategy="median")
    Xtr = imp.fit_transform(tr[feats])
    Xte = imp.transform(te[feats])
    ytr = tr["y_vib"].to_numpy().astype(int)
    sc = []
    for i in range(2):
        clf = RandomForestClassifier(n_estimators=300, min_samples_leaf=5,
                                     class_weight="balanced_subsample",
                                     random_state=42, n_jobs=-1)
        clf.fit(Xtr, ytr)
        sc.append(clf.predict_proba(Xte)[:, 1])
    same = bool(np.array_equal(sc[0], sc[1]))
    rfd = {"uji_well": str(te_well), "n_train": int(len(tr)), "n_test": int(len(te)),
           "n_fitur": len(feats), "skor_bit_identik": same,
           "hash1": h(sc[0]), "hash2": h(sc[1]),
           "max_abs_diff": float(np.abs(sc[0] - sc[1]).max()),
           "n_jobs": -1, "random_state": 42}
except Exception as e:
    rfd = {"error": repr(e), "trace": traceback.format_exc()[-800:]}
log(f"   RF: {rfd}")
res["determinisme_rf"] = rfd

# ------------------------------------------------------- 5. tool_wear satuan
log("== 4. tool_wear: satuan jendela, rumus kuantil, TLead")
tw = {}
try:
    t = pd.read_csv(f"{BASE}/scratch/v6_e1/toolwear_windows.csv")
    tw["n_baris"] = int(len(t))
    tw["per_alat_run"] = {f"{k[0]}_{k[1]}": int(v) for k, v in
                          t.groupby(["tool", "run"]).size().items()}
    tw["y_per_run"] = {f"{k[0]}_{k[1]}": float(v) for k, v in
                       t.groupby(["tool", "run"])["y"].mean().items()}
    diffs = []
    for (tool, run), g in t.groupby(["tool", "run"]):
        s = np.sort(g["start_sample"].to_numpy())
        if len(s) > 1:
            d = np.diff(s)
            diffs.append({"alat": tool, "run": run, "n": int(len(s)),
                          "langkah_min": int(d.min()), "langkah_max": int(d.max()),
                          "langkah_unik": [int(x) for x in np.unique(d)[:5]]})
    tw["langkah_start_sample"] = diffs
    # rumus kuantil di v9_i1_pipeline.py:631-632
    contoh = []
    for n_eval in (100, 469, 1000, 5000):
        q = 1.0 - 1.0 * (n_eval / 60.0) / max(n_eval, 1)
        contoh.append({"n_eval": n_eval, "q": round(q, 6)})
    tw["rumus_kuantil"] = contoh
    tw["catatan_kuantil"] = ("q = 1 - TARGET*(n/60)/n = 1 - 1/60 = 0,983333 "
                             "untuk setiap n; menyusut jadi konstanta")
except Exception as e:
    tw = {"error": repr(e)}
res["tool_wear"] = tw
log(f"   tool_wear: {tw.get('n_baris')} baris; langkah={tw.get('langkah_start_sample')}")

# ------------------------------------------------------------ 6. bit_wear
log("== 5. bit_wear: sirkularitas persistence")
bw = {}
try:
    u = pd.read_csv(f"{BASE}/data/USROP_labeled.csv")
    bw["n_baris"] = int(len(u))
    bw["kolom"] = u.columns.tolist()[:40]
    lab = u["label"] if "label" in u.columns else None
    if lab is not None:
        vc = lab.value_counts().to_dict()
        bw["komposisi_label"] = {str(k): int(v) for k, v in vc.items()}
        is_mse = (u["label"] == "high_MSE_bit_wear").to_numpy().astype(int)
        bw["n_pos"] = int(is_mse.sum())
        bw["prev"] = round(float(is_mse.mean()), 4)
        nxt = np.concatenate([is_mse[1:], [0]])   # y(t+1) vs y(t)
        bw["P_y(t+1)_given_y(t)"] = round(float(nxt[is_mse == 1].mean()), 4)
        bw["catatan"] = ("persistence di v9_i1_pipeline.py:580 = label digeser 1 baris; "
                         "presisi persistence karena itu = P(label tetap) bukan skill model")
except Exception as e:
    bw = {"error": repr(e)}
res["bit_wear"] = bw
log(f"   bit_wear: {bw.get('n_pos')} pos dari {bw.get('n_baris')}")

with open(f"{OUTDIR}/e0_audit_results.json", "w") as f:
    json.dump(res, f, indent=1, default=str)
open(f"{OUTDIR}/e0_audit_run_log.txt", "w").write("\n".join(LOG) + "\n")
log("SELESAI -> e0_audit_results.json")
