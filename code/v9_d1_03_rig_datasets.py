#!/usr/bin/env python3
"""V9-D1 03 — ekspor dataset siap-latih per engine rig dari master windows.

Engine diekspor di skrip ini:
  vib, ssi, shk, stuck_k1 (status) + hyd_ki (label qcut SPPA/TFLO, resep V6-E1 31)
Semua memakai fitur jendela [t0-10, t0) dari v9_d1_02 (kolom V6-identik).
- vib/ssi/shk/stuck_k1 : 11 kanal x 5 stat = 55 fitur (kontrak V6/D-A1)
- hyd_ki               : 8 kanal x 5 = 40 fitur (SPPA/TFLO/SPM DIBUANG — anti-sirkular)
Kolom meta anti-bocor: well, ts_bin, feat_ts_max, lab_ts, lab_kind.
Eligibility: feat_valid & valid_<kelas> (baris tak layak TIDAK diekspor; jumlahnya
dilaporkan di QC). Output: scratch/v9_d1/datasets/<engine>.csv.gz + QC JSON + log.
"""
import json
import os
import time
import numpy as np
import pandas as pd

SEED = 42
np.random.seed(SEED)

BINS = "/mnt/d/Capstone 1(v2)/scratch/v9_d1/bins"
WIN = "/mnt/d/Capstone 1(v2)/scratch/v9_d1/windows"
OUT = "/mnt/d/Capstone 1(v2)/scratch/v9_d1/datasets"
os.makedirs(OUT, exist_ok=True)

W = 10
NQ = 10
MIN_OBS = 5
STATS = ["mean", "std", "slope", "last", "frac"]
CHAN = ["TQA", "SPPA", "TFLO", "RPM", "SWOB", "HKLD", "ROP", "BPOS", "SPM",
        "depth", "dbtm"]
FEAT55 = [f"{c}_{s}" for c in CHAN for s in STATS]
HYD_EXCLUDE = ["SPPA", "TFLO", "SPM"]
FEAT40 = [f for f in FEAT55 if f.rsplit("_", 1)[0] not in HYD_EXCLUDE]
META_W = ["ts_bin", "feat_ts_max", "lab_ts", "lab_kind"]   # kolom di master windows
META = ["well"] + META_W                                    # kolom di dataset ekspor
ENGINES = {  # engine -> (label col prefix, feature cols)
    "vib": ("vib", FEAT55),
    "ssi": ("ssi", FEAT55),
    "shk": ("shk", FEAT55),
    "stuck_k1": ("stuck", FEAT55),
}

t_start = time.time()
log_lines = []


def log(msg):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line, flush=True)
    log_lines.append(line)


def hyd_bin_labels(b):
    """Label anomali hidrolik per menit (resep V6-E1 31, per sumur)."""
    d = b.dropna(subset=["SPPA_mean", "TFLO_mean"]).copy()
    d = d[d["TFLO_mean"] > 0]
    anom = pd.Series(False, index=b.index)
    n_label_bins = 0
    if len(d) >= 50:
        try:
            d["qbin"] = pd.qcut(d["TFLO_mean"], NQ, labels=False, duplicates="drop")
        except ValueError:
            d["qbin"] = 0
        med = d.groupby("qbin")["SPPA_mean"].transform("median")
        mad = d.groupby("qbin")["SPPA_mean"].transform(
            lambda s: (s - s.median()).abs().median())
        z = (d["SPPA_mean"] - med) / (1.4826 * mad.replace(0, np.nan))
        anom.loc[d.index] = (z.abs() > 2).fillna(False)
        n_label_bins = len(d)
    B = pd.DataFrame({"ts_bin": b["ts_bin"],
                      "obs": b["SPPA_mean"].notna() & b["TFLO_mean"].notna(),
                      "anom": anom.values})
    return B, n_label_bins


qc = {"seed": SEED, "engines": {}}
acc = {e: [] for e in list(ENGINES) + ["hyd_ki"]}

for fn in sorted(os.listdir(WIN)):
    if not fn.endswith(".csv.gz"):
        continue
    well = fn.replace(".csv.gz", "")
    f = pd.read_csv(os.path.join(WIN, fn)).sort_values("ts_bin").reset_index(drop=True)
    b = pd.read_csv(os.path.join(BINS, f"{well}.csv.gz"))

    # ---- hyd_ki label (V6-31) ----
    B, n_lab_bins = hyd_bin_labels(b)
    Bs = B.set_index("ts_bin")
    ts = f["ts_bin"].to_numpy()
    n_obs = np.zeros(len(ts))
    n_anom = np.zeros(len(ts))
    for k in range(0, W):
        sub = Bs.reindex(ts + k)
        o = sub["obs"].fillna(False).to_numpy() & sub["anom"].notna().to_numpy()
        a = np.nan_to_num(sub["anom"].to_numpy(dtype=float), nan=0.0)
        n_obs += o.astype(float)
        n_anom += (o & (a > 0)).astype(float)
    valid_h = n_obs >= MIN_OBS
    y_h = (valid_h & (n_anom / np.maximum(n_obs, 1) >= 0.5)).astype(np.int8)
    LBh = pd.DataFrame({"y": y_h, "valid": valid_h}, index=pd.Index(ts))
    prev_h = LBh.reindex(pd.Index(ts - W))
    f["obs_hyd"] = n_obs
    f["anom_hyd"] = n_anom
    f["valid_hyd"] = valid_h
    f["y_hyd"] = y_h
    f["y_prev_hyd"] = np.nan_to_num(prev_h["y"].to_numpy(dtype=float), nan=0.0)
    f["valid_prev_hyd"] = np.nan_to_num(prev_h["valid"].to_numpy(dtype=float), nan=0.0)

    # ---- export tiap engine ----
    for engine, (cls, feats) in ENGINES.items():
        m = f["feat_valid"].astype(bool) & f[f"valid_{cls}"].astype(bool)
        cols = META_W + feats + [f"y_{cls}", f"y_prev_{cls}", f"valid_prev_{cls}"]
        sub = f.loc[m, cols].copy()
        sub.insert(0, "well", well)
        acc[engine].append(sub)
    m = f["feat_valid"].astype(bool) & f["valid_hyd"].astype(bool)
    cols = META_W + FEAT40 + ["y_hyd", "y_prev_hyd", "valid_prev_hyd",
                              "obs_hyd", "anom_hyd"]
    sub = f.loc[m, cols].copy()
    sub.insert(0, "well", well)
    acc["hyd_ki"].append(sub)

    qc.setdefault("per_well", {}).setdefault(well, {})["hyd_ki"] = {
        "label_bins": n_lab_bins,
        "eligible": int(m.sum()),
        "positives": int(f.loc[m, "y_hyd"].sum()),
    }
    log(f"== {well}: hyd_ki label_bins={n_lab_bins} eligible={int(m.sum())} "
        f"pos={int(f.loc[m, 'y_hyd'].sum())}")

for engine, parts in acc.items():
    if not parts:
        df = pd.DataFrame(columns=META)
    else:
        df = pd.concat(parts, ignore_index=True)
        df = df.sort_values(["well", "ts_bin"]).reset_index(drop=True)
    path = os.path.join(OUT, f"{engine}.csv.gz")
    df.to_csv(path, index=False, compression={"method": "gzip", "mtime": 0})
    ycol = [c for c in df.columns if c.startswith("y_") and not c.startswith("y_prev")
            and not c.startswith("valid")][0] if len(df) else None
    per_well = {}
    for w, g in df.groupby("well"):
        pos = int(g[ycol].sum()) if ycol else 0
        per_well[w] = {"n": int(len(g)), "pos": pos,
                       "prev": round(pos / len(g), 6) if len(g) else None,
                       "underpowered": pos < 30}
    qc["engines"][engine] = {
        "file": path,
        "n_rows": int(len(df)),
        "n_features": len([c for c in df.columns if c not in META and
                           not c.startswith("y_") and not c.startswith("valid_") and
                           not c.startswith("obs_") and not c.startswith("anom_")]),
        "positives": int(df[ycol].sum()) if ycol and len(df) else 0,
        "y_col": ycol,
        "per_well": per_well,
        "leak_stamp_cols": META,
    }
    log(f"-> {engine}: rows={len(df)} feats={qc['engines'][engine]['n_features']} "
        f"pos={qc['engines'][engine]['positives']} wells={list(per_well)}")

qc["elapsed_s"] = round(time.time() - t_start, 1)
json.dump(qc, open("/mnt/d/Capstone 1(v2)/scratch/v9_d1/v9_d1_03_qc.json", "w"), indent=1)
open("/mnt/d/Capstone 1(v2)/scratch/v9_d1/v9_d1_03_run_log.txt", "w").write(
    "\n".join(log_lines) + "\n")
print("done", qc["elapsed_s"], "s")
