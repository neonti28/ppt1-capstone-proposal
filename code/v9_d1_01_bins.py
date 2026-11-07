#!/usr/bin/env python3
"""V9-D1 01 — ekstraksi bin 60 detik dari 9 CSV WITSML terparse (resep V6 verbatim).

Reproduksi resep `v6_e1_10_bins.py` TANPA perubahan algoritma (kontrak D-A1 + kontrol
reproduksi V8/V6 untuk E_ML):
  - baca usecols terpilih, chunksize 250_000 (merge mean-of-means antar chunk = resep V6)
  - agregat surface HANYA baris pengeboran (RPM>0 & SWOB>0)
  - agregat kanal label SEMUA baris (max/count; CRPM n/min/max/mean)
  - kolom spm_mean huruf kecil = resep V6 (menyebabkan fitur SPM_* di jendela = NaN/frac=0;
    dipertahankan demi reproduksi numerik — terdokumentasi di dokumen D1)
Output: scratch/v9_d1/bins/<WELL>.csv.gz + v9_d1_01_summary.json (JSON primer + log).
Determinisme: operasi penuh deterministik; seed 42 ditekan di awal.
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

BASE = "/mnt/d/Capstone 1(v2)/data/volve/witsml_parsed"
OUTDIR = "/mnt/d/Capstone 1(v2)/scratch/v9_d1/bins"
FILES = ["F-5.csv", "F-7.csv", "F-9.csv", "F-9_A.csv", "F-10.csv", "F-12.csv",
         "F-14.csv", "F-15A.csv", "F-15_S.csv"]
SURF = ["TQA", "SPPA", "TFLO", "RPM", "SWOB", "HKLD", "ROP", "BPOS"]
SPM = ["SPM1", "SPM2", "SPM3"]
LBL_MAX = {"STUCK_RT": "stuck", "VIBLAT_RT": "vib", "SHKRSK_RT": "shk"}

os.makedirs(OUTDIR, exist_ok=True)
t_start = time.time()
log_lines = []


def log(msg):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line, flush=True)
    log_lines.append(line)


summary = {"seed": SEED, "recipe": "v6_e1_10_bins verbatim (chunksize=250000)",
           "wells": {}}

for fn in FILES:
    well = fn.replace(".csv", "")
    p = os.path.join(BASE, fn)
    hdr = pd.read_csv(p, nrows=0).columns.tolist()
    surf = [c for c in SURF if c in hdr]
    spm = [c for c in SPM if c in hdr]
    lab = [c for c in LBL_MAX if c in hdr]
    use = set(surf + spm + lab + ["CRPM_RT", "DMEA", "DBTM", "timestamp"])
    use = {c for c in use if c in hdr}
    parts = []
    for ch in pd.read_csv(p, usecols=sorted(use), chunksize=250_000, low_memory=False):
        ts = pd.to_datetime(ch.pop("timestamp"), format="ISO8601", utc=True, errors="coerce")
        ch = ch[ts.notna()]
        ts = ts[ts.notna()]
        binmin = (ts.astype("int64") // 10**9 // 60).astype("int64")
        num = ch.apply(pd.to_numeric, errors="coerce")
        drill = pd.Series(False, index=num.index)
        if "RPM" in num and "SWOB" in num:
            drill = (num["RPM"] > 0) & (num["SWOB"] > 0) & num["RPM"].notna() & num["SWOB"].notna()
        agg = {}
        d = num.loc[drill, surf] if surf else None
        if d is not None and len(d):
            g = d.groupby(binmin.loc[drill])
            for c in surf:
                agg[f"{c}_mean"] = g[c].mean()
                agg[f"{c}_std"] = g[c].std()
        grp = binmin
        cnt_all = grp.value_counts()
        cnt_drill = binmin.loc[drill].value_counts()
        if "DMEA" in num:
            dd = num.loc[drill, "DMEA"] if drill.any() else num["DMEA"]
            depth = dd.groupby(binmin.loc[drill] if drill.any() else binmin).mean()
        else:
            depth = None
        if "DBTM" in num:
            db = num.loc[drill, "DBTM"] if drill.any() else num["DBTM"]
            dbtm = db.groupby(binmin.loc[drill] if drill.any() else binmin).mean()
        else:
            dbtm = None
        labagg = {}
        for c, pref in LBL_MAX.items():
            if c in num:
                s = num[c]
                labagg[(pref + "_max", "")] = s.groupby(binmin).max()
                labagg[(pref + "_n", "")] = s.groupby(binmin).count()
        if "CRPM_RT" in num:
            s = num["CRPM_RT"]
            labagg[("crpm_mean", "")] = s.groupby(binmin).mean()
            labagg[("crpm_min", "")] = s.groupby(binmin).min()
            labagg[("crpm_max", "")] = s.groupby(binmin).max()
            labagg[("crpm_n", "")] = s.groupby(binmin).count()
        if spm:
            sp = num[spm].sum(axis=1, min_count=1)
            sp = sp[drill]
            labagg[("spm_mean", "")] = sp.groupby(binmin.loc[drill]).mean() if len(sp) else None
        frame = {}
        frame["rows"] = cnt_all
        frame["rows_drill"] = cnt_drill
        for name, v in agg.items():
            frame[name] = v
        if depth is not None:
            frame["depth_mean"] = depth
        if dbtm is not None:
            frame["dbtm_mean"] = dbtm
        for (name, _), v in labagg.items():
            if v is not None:
                frame[name] = v
        df = pd.DataFrame(frame)
        df.index.name = "ts_bin"
        parts.append(df.reset_index())
    if not parts:
        summary["wells"][well] = {"error": "no data"}
        log(f"== {well}: ERROR no data")
        continue
    bins = pd.concat(parts, ignore_index=True)
    numcols = [c for c in bins.columns if c != "ts_bin"]
    grouped = bins.groupby("ts_bin")
    out = pd.DataFrame({"rows": grouped["rows"].sum(), "rows_drill": grouped["rows_drill"].sum()})

    def _rule(col):
        if col.endswith("_max"):
            return "max"
        if col.endswith("_min"):
            return "min"
        if col.endswith("_n") or col in ("rows", "rows_drill"):
            return "sum"
        return "mean"

    for c in numcols:
        if c in ("rows", "rows_drill"):
            continue
        out[c] = getattr(grouped[c], _rule(c))()
    out = out.reset_index().sort_values("ts_bin")
    path = os.path.join(OUTDIR, f"{well}.csv.gz")
    out.to_csv(path, index=False, compression={"method": "gzip", "mtime": 0})
    w = {
        "n_bins": int(len(out)),
        "n_bins_drill": int((out["rows_drill"] > 0).sum()),
        "label_channels_present": sorted([k for k in LBL_MAX if f"{LBL_MAX[k]}_n" in out.columns]),
        "crpm_present": "crpm_n" in out.columns,
        "spm_present": "spm_mean" in out.columns,
        "depth_present": "depth_mean" in out.columns,
        "size_bytes": os.path.getsize(path),
    }
    for pref in LBL_MAX.values():
        col = f"{pref}_n"
        w[f"bins_with_{pref}_obs"] = int((out[col].fillna(0) > 0).sum()) if col in out.columns else None
    if "crpm_n" in out.columns:
        w["bins_with_crpm_obs"] = int((out["crpm_n"].fillna(0) > 0).sum())
    summary["wells"][well] = w
    log(f"== {well}: bins={w['n_bins']} drill={w['n_bins_drill']} "
        f"labels={w['label_channels_present']} crpm={w['crpm_present']}")

summary["elapsed_s"] = round(time.time() - t_start, 1)
json.dump(summary, open("/mnt/d/Capstone 1(v2)/scratch/v9_d1/v9_d1_01_summary.json", "w"), indent=1)
open("/mnt/d/Capstone 1(v2)/scratch/v9_d1/v9_d1_01_run_log.txt", "w").write("\n".join(log_lines) + "\n")
print("done", summary["elapsed_s"], "s")
