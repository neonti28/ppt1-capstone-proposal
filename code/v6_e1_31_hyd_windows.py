#!/usr/bin/env python3
"""V6-E1 31 — jendela label HYDRAULIC (kandidat kelas ke-5, V6-E1b).

Label = rumus R1 §4.2 #7 yang SUDAH diuji di data F-14 (verifikasi run-3):
  per sumur: qcut(TFLO_mean, 10) → median & MAD SPPA_mean per bin aliran,
  z = (SPPA − median)/(1.4826·MAD), anomali bin bila |z| > 2.
Jendela label [t0, t0+10): y_hyd = 1 bila ≥50% bin teramati anomali (n_obs ≥ 5).
Eligibility: feat_valid (dari v6_e1_20) DAN n_obs ≥ 5.

Fitur untuk kelas ini: 8 channel (TQA, RPM, SWOB, HKLD, ROP, BPOS, depth, dbtm)
— SPPA, TFLO, SPM DIKECUALIKAN (label memakai SPPA+TFLO; SPM � ≈ aliran → sirkular).

Output: scratch/v6_e1/windows_hyd/<WELL>.csv.gz + summary JSON (HITUNGAN, bukan hasil model)
"""
import json
import os
import numpy as np
import pandas as pd

BINS = "/mnt/d/Capstone 1/scratch/v6_e1/bins"
WIN = "/mnt/d/Capstone 1/scratch/v6_e1/windows"
OUT = "/mnt/d/Capstone 1/scratch/v6_e1/windows_hyd"
W = 10
NQ = 10
MIN_OBS = 5
MIN_DRILL_BINS = 5
MIN_DRILL_ROWS = 60

os.makedirs(OUT, exist_ok=True)
summary = {}

for fn in sorted(os.listdir(BINS)):
    if not fn.endswith(".csv.gz"):
        continue
    well = fn.replace(".csv.gz", "")
    b = pd.read_csv(os.path.join(BINS, fn)).sort_values("ts_bin").reset_index(drop=True)
    f = pd.read_csv(os.path.join(WIN, f"{well}.csv.gz")).sort_values("ts_bin").reset_index(drop=True)
    # --- label bin: anomali hidrolik per R1 ---
    d = b.dropna(subset=["SPPA_mean", "TFLO_mean"]).copy()
    d = d[d["TFLO_mean"] > 0]
    anom = pd.Series(False, index=b.index)
    n_bins_lab = 0
    if len(d) >= 50:
        try:
            d["qbin"] = pd.qcut(d["TFLO_mean"], NQ, labels=False, duplicates="drop")
        except ValueError:
            d["qbin"] = 0
        med = d.groupby("qbin")["SPPA_mean"].transform("median")
        mad = d.groupby("qbin")["SPPA_mean"].transform(lambda s: (s - s.median()).abs().median())
        z = (d["SPPA_mean"] - med) / (1.4826 * mad.replace(0, np.nan))
        flag = (z.abs() > 2).fillna(False)
        anom.loc[d.index] = flag
        n_bins_lab = int(d["tflo_mean" if "tflo_mean" in d else "TFLO_mean"].notna().sum()) if False else len(d)
    B = pd.DataFrame({"ts_bin": b["ts_bin"], "obs": b["SPPA_mean"].notna() & b["TFLO_mean"].notna(),
                      "anom": anom.values})
    Bs = B.set_index("ts_bin")
    # agregat jendela label [t0, t0+10)
    ts = f["ts_bin"].to_numpy()
    n_obs = np.zeros(len(ts)); n_anom = np.zeros(len(ts))
    for k in range(0, W):
        sub = Bs.reindex(ts + k)
        o = sub["obs"].fillna(False).to_numpy() & sub["anom"].notna().to_numpy()
        a = np.nan_to_num(sub["anom"].to_numpy(dtype=float), nan=0.0)
        n_obs += o.astype(float)
        n_anom += (o & (a > 0)).astype(float)
    valid = n_obs >= MIN_OBS
    y = (valid & (n_anom / np.maximum(n_obs, 1) >= 0.5)).astype(np.int8)
    # persistence: label jendela sebelumnya
    LB = pd.DataFrame({"y": y, "valid": valid}, index=pd.Index(ts))
    prev = LB.reindex(pd.Index(ts - W))
    f["obs_hyd"] = n_obs
    f["anom_hyd"] = n_anom
    f["valid_hyd"] = valid
    f["y_hyd"] = y
    f["y_prev_hyd"] = np.nan_to_num(prev["y"].to_numpy(dtype=float), nan=0.0)
    f["valid_prev_hyd"] = np.nan_to_num(prev["valid"].to_numpy(dtype=float), nan=0.0)
    elig = f["feat_valid"] & f["valid_hyd"]
    path = os.path.join(OUT, f"{well}.csv.gz")
    f.to_csv(path, index=False, compression="gzip")
    summary[well] = {"bins_with_hyd_label": n_bins_lab, "windows": int(len(f)),
                     "eligible": int(elig.sum()), "positives": int(f.loc[elig, "y_hyd"].sum()),
                     "prev": float(f.loc[elig, "y_hyd"].mean()) if elig.sum() else None}
    print(f"== {well}: bin label={n_bins_lab} windows={len(f)} eligible={summary[well]['eligible']} "
          f"pos={summary[well]['positives']} prev={summary[well]['prev']}", flush=True)

json.dump(summary, open("/mnt/d/Capstone 1/scratch/v6_e1/ch31_hyd_summary.json", "w"), indent=1)
print("done")
