#!/usr/bin/env python3
"""V9-D1 02 — master jendela fitur rig (resep V6 verbatim + stempel anti-bocor).

Kontrak (D-A1 + S1 + S5):
- grid 60 detik (bin epoch-menit dari v9_d1_01)
- FITUR = bin [t0-10, t0)  (masa lalu; 11 kanal x mean/std/slope/last/frac = 55)
- LABEL = bin [t0, t0+10)  (status: vib VIBLAT>=32.17405, shk SHKRSK>=1,
  stuck STUCK>=1, ssi SSI(CRPM)>=1 dgn min 10 sampel)
- feat_valid >=5/10 bin drilling + >=60 baris drilling
- y_prev_* = label jendela sebelumnya (baseline persistence, S9)
TAMBAHAN D1 (kolom ekstra, tidak mengubah kolom V6):
- feat_ts_max  = menit terakhir yang BENAR-BENAR berkontribusi ke fitur (t0 - k_min)
                 (strict < t0; bila tak ada bin fitur = NaN)
- lab_ts       = menit mulai jendela label (= t0) untuk label status
- lab_kind     = 'status_window'
Output: scratch/v9_d1/windows/<WELL>.csv.gz + summary JSON + run log.
"""
import json
import os
import time
import random
import numpy as np
import pandas as pd

SEED = 42
np.random.seed(SEED)
random.seed(SEED)

BINS = "/mnt/d/Capstone 1(v2)/scratch/v9_d1/bins"
OUT = "/mnt/d/Capstone 1(v2)/scratch/v9_d1/windows"
W = 10
MIN_DRILL_BINS = 5
MIN_DRILL_ROWS = 60
SSI_MIN_SAMPLES = 10
VIB_THRESH = 32.17405

CHAN = ["TQA", "SPPA", "TFLO", "RPM", "SWOB", "HKLD", "ROP", "BPOS", "SPM",
        "depth", "dbtm"]
LABDEF = {"stuck": ("stuck_max", "stuck_n", 1.0),
          "vib": ("vib_max", "vib_n", VIB_THRESH),
          "shk": ("shk_max", "shk_n", 1.0)}

os.makedirs(OUT, exist_ok=True)
t_start = time.time()
log_lines = []


def log(msg):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line, flush=True)
    log_lines.append(line)


def build(b):
    """Salinan logika v6_e1_20_windows.build + stempel leak (feat_ts_max)."""
    ts = b["ts_bin"].to_numpy()
    S = {c: pd.Series(b[c].to_numpy(dtype="float64"), index=ts)
         for c in b.columns if c != "ts_bin"}
    n = len(ts)

    def at(col, offsets, base):
        return [S[col].reindex(base + k).to_numpy(dtype="float64")
                if col in S else np.full(len(base), np.nan) for k in offsets]

    # PASS 1: label pada SEMUA anchor
    lab = {}
    for name, (mx, nn, thr) in LABDEF.items():
        if mx not in S:
            lab[f"valid_{name}"] = np.zeros(n, bool)
            lab[f"nobs_{name}"] = np.zeros(n)
            lab[f"y_{name}"] = np.zeros(n, np.int8)
            continue
        Mm = np.vstack(at(mx, range(0, W), ts))
        Nn = np.vstack(at(nn, range(0, W), ts)) if nn in S else np.zeros((W, n))
        Nn = np.nan_to_num(Nn, nan=0.0)
        valid = Nn > 0
        mxv = np.where(valid, np.nan_to_num(Mm, nan=-np.inf), -np.inf).max(axis=0)
        n_obs = np.where(valid, Nn, 0).sum(axis=0)
        lab[f"valid_{name}"] = (n_obs >= 1)
        lab[f"nobs_{name}"] = n_obs
        lab[f"y_{name}"] = ((n_obs >= 1) & (mxv >= thr)).astype(np.int8)
    if "crpm_n" in S:
        Cn = np.nan_to_num(np.vstack(at("crpm_n", range(0, W), ts)), nan=0.0)
        Cmean = np.vstack(at("crpm_mean", range(0, W), ts))
        Cmin = np.vstack(at("crpm_min", range(0, W), ts))
        Cmax = np.vstack(at("crpm_max", range(0, W), ts))
        n_tot = Cn.sum(axis=0)
        num = np.where(Cn > 0, np.nan_to_num(Cmean, nan=0.0) * Cn, 0.0).sum(axis=0)
        wmean = num / np.where(n_tot > 0, n_tot, np.nan)
        wmin = np.where(np.isnan(Cmin) | (Cn == 0), np.inf, Cmin).min(axis=0)
        wmax = np.where(np.isnan(Cmax) | (Cn == 0), -np.inf, Cmax).max(axis=0)
        ssi = (wmax - wmin) / (2.0 * wmean)
        ok = (n_tot >= SSI_MIN_SAMPLES) & (wmean > 0) & np.isfinite(ssi)
        lab["valid_ssi"] = ok
        lab["nobs_ssi"] = n_tot
        lab["y_ssi"] = (ok & (ssi >= 1.0)).astype(np.int8)
        lab["ssi_val"] = np.where(ok, ssi, np.nan)
    else:
        lab["valid_ssi"] = np.zeros(n, bool)
        lab["nobs_ssi"] = np.zeros(n)
        lab["y_ssi"] = np.zeros(n, np.int8)
        lab["ssi_val"] = np.full(n, np.nan)
    L = pd.DataFrame(lab, index=pd.Index(ts, name="ts_bin"))

    # PASS 2: kandidat anchor
    valid_cols = [c for c in L.columns if c.startswith("valid_")]
    cand = L[valid_cols].any(axis=1).to_numpy()
    Ac = ts[cand]

    acc = {c: {k: np.zeros(len(Ac)) for k in
               ("n", "nm", "nm2", "ns2", "cnt", "sm", "sx", "sx2", "sxm")}
        for c in CHAN}
    last_m = {c: np.full(len(Ac), np.nan) for c in CHAN}
    drill_bins = np.zeros(len(Ac))
    drill_rows = np.zeros(len(Ac))
    min_k_present = np.full(len(Ac), np.inf)  # TAMBAHAN D1: k terkecil dgn data fitur

    rdS = S["rows_drill"] if "rows_drill" in S else None
    for k in range(1, W + 1):
        keys = Ac - k
        x = -float(k)
        rd = rdS.reindex(keys).to_numpy(dtype="float64") if rdS is not None \
            else np.ones(len(Ac))
        rd = np.nan_to_num(rd, nan=0.0)
        drill_bins += (rd > 0).astype(np.float64)
        drill_rows += rd
        row_present = np.zeros(len(Ac), bool)
        for c in CHAN:
            cm, cs = c + "_mean", c + "_std"
            m = S[cm].reindex(keys).to_numpy(dtype="float64") if cm in S \
                else np.full(len(Ac), np.nan)
            pres = ~np.isnan(m) & (rd > 0)
            row_present |= pres
            s = S[cs].reindex(keys).to_numpy(dtype="float64") if cs in S \
                else np.full(len(Ac), np.nan)
            s = np.where(np.isnan(s), 0.0, s)
            a = acc[c]
            wgt = np.where(pres, rd, 0.0)
            mm = np.where(pres, m, 0.0)
            a["n"] += wgt
            a["nm"] += wgt * mm
            a["nm2"] += wgt * mm * mm
            a["ns2"] += wgt * s * s
            a["cnt"] += pres.astype(np.float64)
            a["sm"] += mm
            a["sx"] += np.where(pres, x, 0.0)
            a["sx2"] += np.where(pres, x * x, 0.0)
            a["sxm"] += np.where(pres, x * mm, 0.0)
            if k == 1:
                last_m[c] = np.where(pres, m, np.nan)
        min_k_present = np.where(row_present & (k < min_k_present), k, min_k_present)

    F = pd.DataFrame(index=pd.Index(Ac, name="ts_bin"))
    F["feat_drill_bins"] = drill_bins
    F["feat_drill_rows"] = drill_rows
    for c in CHAN:
        a = acc[c]
        wmean = np.where(a["n"] > 0, a["nm"] / np.where(a["n"] > 0, a["n"], 1), np.nan)
        var = (a["nm2"] + a["ns2"]) / np.where(a["n"] > 0, a["n"], 1) - wmean ** 2
        wstd = np.sqrt(np.clip(var, 0, None))
        den = a["cnt"] * a["sx2"] - a["sx"] ** 2
        slope = np.where((a["cnt"] >= 3) & (den > 1e-9),
                         (a["cnt"] * a["sxm"] - a["sx"] * a["sm"]) /
                         np.where(den > 1e-9, den, 1), np.nan)
        F[f"{c}_mean"] = wmean
        F[f"{c}_std"] = wstd
        F[f"{c}_slope"] = slope
        F[f"{c}_last"] = last_m[c]
        F[f"{c}_frac"] = a["cnt"] / W

    F["feat_valid"] = (drill_bins >= MIN_DRILL_BINS) & (drill_rows >= MIN_DRILL_ROWS)

    # TAMBAHAN D1 — stempel anti-bocor
    F["feat_ts_max"] = np.where(np.isfinite(min_k_present), Ac - min_k_present, np.nan)
    F["lab_ts"] = F.index.to_numpy(dtype=float)   # jendela label status mulai di t0
    F["lab_kind"] = "status_window"

    cols = [c for c in L.columns]
    Lc = L.reindex(Ac)
    for c in cols:
        F[c] = Lc[c].to_numpy()
    for name in list(LABDEF) + ["ssi"]:
        prev = L[f"y_{name}"].reindex(pd.Index(Ac - W)).to_numpy()
        pval = L[f"valid_{name}"].reindex(pd.Index(Ac - W)).to_numpy()
        F[f"y_prev_{name}"] = np.where(
            np.isnan(prev.astype(float)) if prev.dtype == float else False,
            0, prev).astype(np.float64)
        F[f"valid_prev_{name}"] = np.nan_to_num(pval.astype(np.float64), nan=0.0)
    return F


summary = {}
for fn in sorted(os.listdir(BINS)):
    if not fn.endswith(".csv.gz"):
        continue
    well = fn.replace(".csv.gz", "")
    b = pd.read_csv(os.path.join(BINS, fn))
    b = b.sort_values("ts_bin").reset_index(drop=True)
    F = build(b)
    path = os.path.join(OUT, f"{well}.csv.gz")
    F.to_csv(path, index=True, compression={"method": "gzip", "mtime": 0})
    leak_bad = int((F["feat_ts_max"] >= F["lab_ts"]).sum())
    summary[well] = {
        "n_bins": int(len(b)),
        "n_candidates": int(len(F)),
        "feat_valid": int(F["feat_valid"].sum()),
        "leak_violation_in_builder": leak_bad,
        "per_class": {},
    }
    for name in list(LABDEF) + ["ssi"]:
        v = F[f"valid_{name}"].astype(bool) & F["feat_valid"]
        summary[well]["per_class"][name] = {
            "eligible": int(v.sum()),
            "positives": int(F.loc[v, f"y_{name}"].sum()),
            "prev": float(F.loc[v, f"y_{name}"].mean()) if v.sum() else None,
        }
    log(f"== {well}: bins={len(b)} cand={len(F)} feat_valid={summary[well]['feat_valid']} "
        f"leak_in_builder={leak_bad}")
    for name, d in summary[well]["per_class"].items():
        log(f"     {name}: eligible={d['eligible']} pos={d['positives']} prev={d['prev']}")

json.dump(summary, open("/mnt/d/Capstone 1(v2)/scratch/v9_d1/v9_d1_02_summary.json", "w"), indent=1)
open("/mnt/d/Capstone 1(v2)/scratch/v9_d1/v9_d1_02_run_log.txt", "w").write("\n".join(log_lines) + "\n")
print("done", round(time.time() - t_start, 1), "s")
