#!/usr/bin/env python3
"""V6-E1 01 — hitung populasi NYATA kanal label per sumur (chunked, hemat memori).

Output: scratch/v6_e1/ch02_label_counts.json
- per well: n_rows, n_drilling_rows (RPM>0 & SWOB>0), nonnull/nonzero per kanal label,
  value_counts untuk kanal diskrit, quantile untuk VIBLAT_RT.
"""
import json
import os
import numpy as np
import pandas as pd

BASE = "/mnt/d/Capstone 1/data/volve/witsml_parsed"
OUT = "/mnt/d/Capstone 1/scratch/v6_e1/ch02_label_counts.json"
FILES = ["F-14.csv", "F-15A.csv", "F-15_S.csv", "F-5.csv", "F-7.csv", "F-9.csv", "F-9_A.csv"]
DISCRETE = ["STUCK_RT", "STKSLP", "SHKRSK_RT", "STICK_RT", "WHIRL_RT", "BOUNCE_RT"]
CONTINUOUS = ["VIBLAT_RT", "CRPM_RT", "NRPM_RT", "BACC"]
CORE = ["RPM", "SWOB", "DMEA", "DEPT", "DBTM", "BONB", "ACTC", "TREV"]
SURF = ["TQA", "SPPA", "TFLO", "HKLD", "ROP", "BPOS", "SPM1", "SPM2", "SPM3"]

os.makedirs(os.path.dirname(OUT), exist_ok=True)
res = {}

for fn in FILES:
    p = os.path.join(BASE, fn)
    hdr = pd.read_csv(p, nrows=0).columns.tolist()
    want = [c for c in DISCRETE + CONTINUOUS + CORE + SURF if c in hdr]
    stats = {c: {"nonnull": 0, "nonzero": 0} for c in want}
    vcounts = {c: {} for c in DISCRETE if c in hdr}
    cont_vals = {c: [] for c in CONTINUOUS if c in hdr}
    n_rows = 0
    n_drill = 0
    tmin = tmax = None
    for ch in pd.read_csv(p, usecols=lambda c: c in set(want) | {"timestamp"},
                          chunksize=200_000, low_memory=False):
        n_rows += len(ch)
        ts = ch["timestamp"]
        t0, t1 = ts.iloc[0], ts.iloc[-1]
        tmin = t0 if tmin is None else min(tmin, t0)
        tmax = t1 if tmax is None else max(tmax, t1)
        rpm = pd.to_numeric(ch["RPM"], errors="coerce") if "RPM" in ch else None
        swob = pd.to_numeric(ch["SWOB"], errors="coerce") if "SWOB" in ch else None
        if rpm is not None and swob is not None:
            mask = (rpm > 0) & (swob > 0) & rpm.notna() & swob.notna()
            n_drill += int(mask.sum())
        for c in want:
            if c not in ch:
                continue
            s = pd.to_numeric(ch[c], errors="coerce")
            nn = int(s.notna().sum())
            nz = int((s.fillna(0) != 0).sum())
            stats[c]["nonnull"] += nn
            stats[c]["nonzero"] += nz
            if c in vcounts and nn:
                vc = s.dropna().astype(float).value_counts()
                for k, v in vc.items():
                    ks = str(k)
                    vcounts[c][ks] = vcounts[c].get(ks, 0) + int(v)
            if c in cont_vals and nn:
                # simpan quantile estimasi per chunk: ambil sampel maks 200k nilai
                vals = s.dropna().to_numpy()
                if len(vals) > 50_000:
                    vals = vals[:: len(vals) // 50_000 + 1]
                cont_vals[c].append(vals)
    entry = {"file": fn, "rows": n_rows, "drilling_rows": n_drill,
             "t_min": tmin, "t_max": tmax, "channels": stats,
             "value_counts": vcounts}
    for c, chunks in cont_vals.items():
        if chunks:
            allv = np.concatenate(chunks)
            entry.setdefault("quantiles", {})[c] = {
                "p50": float(np.percentile(allv, 50)),
                "p75": float(np.percentile(allv, 75)),
                "p90": float(np.percentile(allv, 90)),
                "p95": float(np.percentile(allv, 95)),
                "max": float(allv.max()),
                "n_sampled": int(allv.size),
            }
    res[fn] = entry
    print(f"== {fn} rows={n_rows} drill={n_drill} t=[{tmin} .. {tmax}]", flush=True)
    print("   nonzero:", {c: v["nonzero"] for c, v in stats.items() if c in DISCRETE + CONTINUOUS}, flush=True)
    for c in DISCRETE:
        if c in vcounts and vcounts[c]:
            print(f"   {c} value_counts:", dict(sorted(vcounts[c].items(), key=lambda kv: float(kv[0]))[:12]), flush=True)
    json.dump(res, open(OUT, "w"), indent=1)

print("saved", OUT)
