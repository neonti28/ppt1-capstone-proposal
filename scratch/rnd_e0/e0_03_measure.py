#!/usr/bin/env python3
"""RND-E0 probe 03 — ukur: (A) kebocoran waktu, (B) penyebut FAR & span, (C) sirkularitas
(identitas + matriks silang label), (D) determinisme, (E) bit_wear run-length.

Semua angka ditulis ke scratch/rnd_e0/e0_03_measure.json. Tidak mengubah data/kode kampanye.
"""
import json
import sys
import time

import numpy as np
import pandas as pd

BASE = "/mnt/d/Capstone 1(v2)"
sys.path.insert(0, f"{BASE}/code")
import v9_e_RULE_01_status as R          # noqa: E402
import v9_i1_pipeline as P              # noqa: E402

DS = f"{BASE}/scratch/v9_d1/datasets"
OUT = f"{BASE}/scratch/rnd_e0"
W = 10

DSET = {"vib": ("vib", "y_vib"), "ssi": ("ssi", "y_ssi"), "shk": ("shk", "y_shk"),
        "stuck_k1": ("stuck_k1", "y_stuck"), "stuck_k2": ("stuck_k2", "y_stuck_onset"),
        "hyd_ki": ("hyd_ki", "y_hyd")}

res = {"meta": {"t0": time.strftime("%Y-%m-%d %H:%M:%S"),
                "pandas": pd.__version__, "numpy": np.__version__}}

dfs = {}
for key in DSET:
    dfs[key] = pd.read_csv(f"{DS}/{key}.csv.gz")
    print(f"muat {key}: {dfs[key].shape}", flush=True)

# ---------------------------------------------------------------- A. kebocoran
leak = {}
for key, df in dfs.items():
    d = df.dropna(subset=["feat_ts_max"])
    lag = (df["ts_bin"] - df["feat_ts_max"]).dropna()
    leak[key] = {
        "n_rows": int(len(df)),
        "n_feat_ts_nan": int(df["feat_ts_max"].isna().sum()),
        "n_violasi_feat_ts_ge_t0": int((d["feat_ts_max"] >= d["ts_bin"]).sum()),
        "lag_min_minutes": float(lag.min()) if len(lag) else None,
        "lag_max_minutes": float(lag.max()) if len(lag) else None,
        "lag_median_minutes": float(lag.median()) if len(lag) else None,
        "lab_ts_equals_t0_all": bool((df["lab_ts"] == df["ts_bin"]).all()),
        "lab_kind_values": sorted(df["lab_kind"].dropna().unique().tolist()),
    }
    print(f"leak {key}: {leak[key]}", flush=True)
res["A_leak"] = leak

# verifikasi y_prev == y pada anchor t-10 (per well)
prevchk = {}
for key, (cls, ycol) in DSET.items():
    if key == "stuck_k2":
        continue
    df = dfs[key]
    bad = 0
    tot = 0
    for w, g in df.groupby("well"):
        s = g.set_index("ts_bin")[[ycol, f"y_prev_{cls.split('_')[0]}"]].sort_index()
        prev = s[f"y_prev_{cls.split('_')[0]}"]
        shifted = s[ycol].reindex(s.index + W)
        m = shifted.notna()
        bad += int((prev[m].astype(int) != shifted[m].astype(int)).sum())
        tot += int(m.sum())
    prevchk[key] = {"n_checked": tot, "n_mismatch": bad}
    print(f"y_prev {key}: {prevchk[key]}", flush=True)
res["A_y_prev_alignment"] = prevchk

# ------------------------------------------------- B/C. per kelas per well: FAR, presisi
def far_tables(key, cls, ycol):
    df = dfs[key]
    pred, nodata = R.rule_display(cls, df)
    rows = []
    for w, g in df.groupby("well"):
        m = (df["well"] == w).to_numpy()
        y = g[ycol].to_numpy().astype(int)
        p = pred[m].astype(int)
        tp = int(((p == 1) & (y == 1)).sum())
        fp = int(((p == 1) & (y == 0)).sum())
        fn = int(((p == 0) & (y == 1)).sum())
        n_neg = int((y == 0).sum())
        n_pos = int((y == 1).sum())
        ts = g["ts_bin"].to_numpy().astype("int64")
        span = int(ts.max() - ts.min() + 1)
        # label terkontrol waktu: label di t+120 (2 jam ke depan) pada anchor yang sama
        s = g.set_index("ts_bin")[ycol].sort_index()
        ysh = s.reindex(pd.Index(ts + 120)).to_numpy()
        ok = ~pd.isna(ysh)
        psh = p[ok]
        ysh = ysh[ok].astype(int)
        tp_s = int(((psh == 1) & (ysh == 1)).sum())
        fp_s = int(((psh == 1) & (ysh == 0)).sum())
        rows.append({
            "well": w, "n": int(len(g)), "n_pos": n_pos, "n_neg": n_neg,
            "span_menit": span, "coverage": round(len(g) / span, 4),
            "tp": tp, "fp": fp, "fn": fn,
            "precision": round(tp / (tp + fp), 4) if (tp + fp) else None,
            "recall": round(tp / (tp + fn), 4) if (tp + fn) else None,
            "prev_label": round(n_pos / len(g), 4),
            "prev_rule": round(float(p.mean()), 4),
            "far_report_24h": round(fp / (n_neg / 60) * 24, 3) if n_neg else None,
            "far_span_24h": round(fp / (span / 60) * 24, 3),
            "far_horizon_24h": round(fp / (n_neg * W / 60) * 24, 3) if n_neg else None,
            "ctrl_shift120_n": int(ok.sum()),
            "ctrl_shift120_precision": round(tp_s / (tp_s + fp_s), 4) if (tp_s + fp_s) else None,
            "ctrl_shift120_prev": round(float(ysh.mean()), 4) if len(ysh) else None,
        })
    return rows, int(nodata.sum())

farblk = {}
for key, (cls, ycol) in DSET.items():
    rows, n_nodata = far_tables(key, cls, ycol)
    farblk[key] = {"wells": rows, "n_nodata_total": n_nodata}
    for r in rows:
        print(f"FAR {key:9} {r['well']:8} n={r['n']:6} span={r['span_menit']:7} "
              f"cov={r['coverage']:.3f} P={r['precision']} R={r['recall']} "
              f"far={r['far_report_24h']} far_span={r['far_span_24h']} "
              f"far_hz={r['far_horizon_24h']} ctrlP={r['ctrl_shift120_precision']}",
              flush=True)
res["BC_per_class"] = farblk

# ringkas agregat: median FAR versi jendela vs span vs horizon
agg = {}
for key, blk in farblk.items():
    for k in ("far_report_24h", "far_span_24h", "far_horizon_24h"):
        v = [r[k] for r in blk["wells"] if r[k] is not None]
        agg.setdefault(key, {})[k] = {"min": round(min(v), 3) if v else None,
                                      "median": round(float(np.median(v)), 3) if v else None,
                                      "max": round(max(v), 3) if v else None}
    cov = [r["coverage"] for r in blk["wells"]]
    agg[key]["coverage"] = {"min": round(min(cov), 4), "median": round(float(np.median(cov)), 4),
                            "max": round(max(cov), 4)}
res["BC_aggregate"] = agg

# ---------------------------------------------------------- C. matriks silang rule vs label
cross = {}
classes = ["vib", "ssi", "shk", "stuck_k1"]
for key_lbl, cls_lbl in [(c, c) for c in classes]:
    df = dfs[key_lbl]
    ycol = DSET[key_lbl][1]
    y = df[ycol].to_numpy().astype(int)
    cross[key_lbl] = {}
    for cls_rule in classes:
        pr, _ = R.rule_display(cls_rule, df)
        tp = int(((pr == 1) & (y == 1)).sum())
        fp = int(((pr == 1) & (y == 0)).sum())
        cross[key_lbl][cls_rule] = {
            "precision": round(tp / (tp + fp), 4) if (tp + fp) else None,
            "n_alarm": int((pr == 1).sum()),
        }
    cross[key_lbl]["prev_label"] = round(float(y.mean()), 4)
    print(f"cross label {key_lbl}: {cross[key_lbl]}", flush=True)
res["C_cross_matrix"] = cross

# identitas rule-jendela-label, dihitung ulang (bukan dibaca dari JSON) utk 2 kelas
ident = {}
for cls in ("vib", "shk"):
    ident[cls] = R.rule_window_identity(cls, dfs[cls])
    print(f"identity {cls}: {ident[cls]}", flush=True)
res["C_identity"] = ident

# ---------------------------------------------------------------- D. determinisme
det = {}
seg = dfs["vib"][dfs["vib"]["well"] == "F-14"].sort_values("ts_bin").reset_index(drop=True)
p1, n1 = R.rule_display("vib", seg)
p2, n2 = R.rule_display("vib", seg)
det["rule_twice_identical"] = bool(np.array_equal(p1, p2) and np.array_equal(n1, n2))
det["rule_n_alarm"] = int(p1.sum())

full = dfs["vib"].sort_values(["well", "ts_bin"]).reset_index(drop=True)
r1 = P.train_lowo(full, "y_vib", "F-14", n_estimators=300)
r2 = P.train_lowo(full, "y_vib", "F-14", n_estimators=300)
det["rf_twice_maxabsdiff"] = float(np.max(np.abs(r1["score"] - r2["score"])))
det["rf_twice_identical"] = bool(np.array_equal(r1["score"], r2["score"]))
det["rf_auprc_a"] = P.auprc(r1["y"], r1["score"])
det["rf_auprc_b"] = P.auprc(r2["y"], r2["score"])
det["rf_n_train"], det["rf_n_test"] = r1["n_train"], r1["n_test"]

blk1 = P.run_vib(seg, full, R, False)
blk2 = P.run_vib(seg, full, R, False)
det["run_vib_twice_identical"] = json.dumps(blk1, sort_keys=True, default=str) == \
    json.dumps(blk2, sort_keys=True, default=str)
# urutan well: apakah indeks baris mengubah hasil?
full_rev = full.iloc[::-1].reset_index(drop=True)
r3 = P.train_lowo(full_rev, "y_vib", "F-14", n_estimators=300)
det["rf_roworder_maxabsdiff"] = float(np.max(np.abs(r1["score"] - r3["score"])))
det["rf_roworder_identical"] = bool(np.array_equal(r1["score"], r3["score"]))
print(f"determinisme: {det}", flush=True)
res["D_determinism"] = det

# ---------------------------------------------------------------- E. bit_wear
usrop = pd.read_csv(f"{BASE}/data/USROP_labeled.csv", low_memory=False)
bw = {}
for w, g in usrop.groupby("well"):
    g = g.sort_values("Measured Depth m")
    y = (g["label"] == "high_MSE_bit_wear").to_numpy().astype(int)
    if len(y) == 0:
        continue
    runs = []
    cur = y[0]
    ln = 1
    for v in y[1:]:
        if v == cur:
            ln += 1
        else:
            runs.append((int(cur), ln))
            cur, ln = v, 1
    runs.append((int(cur), ln))
    pos_runs = [ln for c, ln in runs if c == 1]
    yp = np.concatenate([[0], y[:-1]])
    tp = int(((yp == 1) & (y == 1)).sum())
    fp = int(((yp == 1) & (y == 0)).sum())
    bw[w] = {
        "n": int(len(y)), "n_pos": int(y.sum()), "prev": round(float(y.mean()), 4),
        "n_runs_total": len(runs), "n_pos_runs": len(pos_runs),
        "mean_pos_run_len": round(float(np.mean(pos_runs)), 2) if pos_runs else None,
        "max_pos_run_len": int(max(pos_runs)) if pos_runs else None,
        "frac_pos_with_prev_pos": round(tp / y.sum(), 4) if y.sum() else None,
        "persistence_precision": round(tp / (tp + fp), 4) if (tp + fp) else None,
    }
    print(f"bitwear {w}: {bw[w]}", flush=True)
res["E_bitwear"] = bw

# varian pipeline (persis run_bit_wear: sort global by MD, shift global)
segm = usrop[usrop["well"].str.contains("_F-14", regex=False)].copy()
segm = segm.sort_values("Measured Depth m").reset_index(drop=True)
is_mse = (segm["label"] == "high_MSE_bit_wear").to_numpy().astype(int)
pers = np.concatenate([[0], is_mse[:-1]])
tp = int(((pers == 1) & (is_mse == 1)).sum())
fp = int(((pers == 1) & (is_mse == 0)).sum())
res["E_bitwear_pipeline_variant"] = {
    "n": int(len(is_mse)), "n_pos": int(is_mse.sum()),
    "precision": round(tp / (tp + fp), 4) if (tp + fp) else None,
    "recall": round(tp / is_mse.sum(), 4) if is_mse.sum() else None,
    "n_label_runs": None,
}

json.dump(res, open(f"{OUT}/e0_03_measure.json", "w"), indent=1, default=str)
print("-> e0_03_measure.json")
