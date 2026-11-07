#!/usr/bin/env python3
"""V6-E1 10 — ekstraksi per-menit (bin 60 detik) dari 7 CSV WITSML terparse.

Output: scratch/v6_e1/bins/<WELL>.csv.gz — satu baris per menit data, memuat:
  - agregat sensor permukaan HANYA pada baris pengeboran (RPM>0 & SWOB>0)
  - agregat kanal label downhole (max/count untuk STUCK_RT, VIBLAT_RT, SHKRSK_RT, STKSLP;
    n/min/max/mean untuk CRPM_RT -> untuk SSI)
Kolom: ts_bin (epoch menit), rows, rows_drill, <ch>_mean/<ch>_std (drilling),
depth_mean, dbtm_mean, stuck_n, stuck_max, vib_n, vib_max, shk_n, shk_max,
crpm_n, crpm_min, crpm_max, crpm_mean, stkslp_n, stkslp_max.
"""
import json
import os
import numpy as np
import pandas as pd

BASE = "/mnt/d/Capstone 1/data/volve/witsml_parsed"
OUTDIR = "/mnt/d/Capstone 1/scratch/v6_e1/bins"
FILES = ["F-14.csv", "F-15A.csv", "F-15_S.csv", "F-5.csv", "F-7.csv", "F-9.csv", "F-9_A.csv"]
SURF = ["TQA", "SPPA", "TFLO", "RPM", "SWOB", "HKLD", "ROP", "BPOS"]
SPM = ["SPM1", "SPM2", "SPM3"]
LBL_MAX = {"STUCK_RT": "stuck", "VIBLAT_RT": "vib", "SHKRSK_RT": "shk", "STKSLP": "stkslp"}

os.makedirs(OUTDIR, exist_ok=True)
summary = {}

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
        # agregat surface: HANYA baris pengeboran
        d = num.loc[drill, surf] if surf else None
        if d is not None and len(d):
            g = d.groupby(binmin.loc[drill])
            for c in surf:
                agg[f"{c}_mean"] = g[c].mean()
                agg[f"{c}_std"] = g[c].std()
        # total per bin + drilling per bin
        grp = binmin
        cnt_all = grp.value_counts()
        cnt_drill = binmin.loc[drill].value_counts()
        # depth (drilling rows; fallback all rows)
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
        # label channels: max + count non-null (SEMUA baris, bukan hanya drilling)
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
        summary[well] = {"error": "no data"}
        continue
    bins = pd.concat(parts, ignore_index=True)
    # gabungkan baris bin yang sama (lintas chunk)
    numcols = [c for c in bins.columns if c != "ts_bin"]
    grouped = bins.groupby("ts_bin")
    out = pd.DataFrame({"rows": grouped["rows"].sum(), "rows_drill": grouped["rows_drill"].sum()})
    # Aturan gabung lintas chunk:
    #   *_max -> max, *_min -> min, *_n / rows* -> sum (exact),
    #   *_mean / *_std -> mean-of-means (aproksimasi; boundary chunk membelah <=1 menit per chunk,
    #   dicatat sebagai limitasi). max/min/count gabungan tetap eksak.
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
        aggname = _rule(c)
        out[c] = getattr(grouped[c], aggname)()
    out = out.reset_index().sort_values("ts_bin")
    path = os.path.join(OUTDIR, f"{well}.csv.gz")
    out.to_csv(path, index=False, compression="gzip")
    summary[well] = {"n_bins": int(len(out)),
                     "n_bins_drill": int((out["rows_drill"] > 0).sum()),
                     "n_bins_stuck": int((out.get("stuck_n", pd.Series(dtype=int)).fillna(0) > 0).sum()),
                     "n_bins_vib": int((out.get("vib_n", pd.Series(dtype=int)).fillna(0) > 0).sum()),
                     "n_bins_shk": int((out.get("shk_n", pd.Series(dtype=int)).fillna(0) > 0).sum()),
                     "n_bins_crpm": int((out.get("crpm_n", pd.Series(dtype=int)).fillna(0) > 0).sum()),
                     "size": os.path.getsize(path)}
    print(f"== {well}: bins={summary[well]['n_bins']} drill={summary[well]['n_bins_drill']} "
          f"stuck_obs={summary[well]['n_bins_stuck']} vib_obs={summary[well]['n_bins_vib']} "
          f"shk_obs={summary[well]['n_bins_shk']} crpm_obs={summary[well]['n_bins_crpm']}", flush=True)

json.dump(summary, open("/mnt/d/Capstone 1/scratch/v6_e1/ch10_bins_summary.json", "w"), indent=1)
print("done")
