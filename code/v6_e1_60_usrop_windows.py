#!/usr/bin/env python3
"""V6-E1 60 — jendela USROP untuk kandidat kelas `bit_wear` (E1d).

Label = kolom `label` tersimpan (`high_MSE_bit_wear`, dari Teale MSE > P75; rumus sudah
diverifikasi ulang R1 run-3: selisih median 4,98e-05, korelasi log10 0,9999999999989).
Jendela: baris diurutkan depth per well; FITUR = 100 baris SEBELUM anchor,
LABEL = 100 baris SESUDAH anchor (horizon J meter/baris ke depan, non-sirkular).

Fitur (ANTI-SIRKULAR — kanal pembentuk MSE DIKECUALIKAN: WOB, TQ, RPM, ROP, Hookload,
MSE, D_exp, ROC_coef): SPP, Mud Flow In, Mud Density, Gamma, MD, TVD (6 kanal × 5 = 30).
Canary kedalaman: MD + TVD saja.
y = 1 bila ≥50% baris jendela label ber-label high_MSE_bit_wear.

Output: scratch/v6_e1/usrop_windows.csv + ch60_usrop_summary.json (HITUNGAN, bukan hasil model)
"""
import json
import numpy as np
import pandas as pd

SRC = "/mnt/d/Capstone 1/data/USROP_labeled.csv"
OUT = "/mnt/d/Capstone 1/scratch/v6_e1/usrop_windows.csv"
SUM = "/mnt/d/Capstone 1/scratch/v6_e1/ch60_usrop_summary.json"
W = 100
STRIDE = 50
MIN_FEAT_NONNULL = 60
CH = {"SPP": "Average Standpipe Pressure kPa",
      "FLOW": "Mud Flow In L/min",
      "MUD": "Mud Density In g/cm3",
      "GAM": "USROP Gamma gAPI",
      "MD": "Measured Depth m",
      "TVD": "Hole Depth (TVD) m"}
BANNED = ["Weight on Bit kkgf", "Average Surface Torque kN.m", "Rate of Penetration m/h",
          "Average Rotary Speed rpm", "Average Hookload kkgf", "MSE", "D_exp", "ROC_coef",
          "label", "well", "Unnamed: 0", "Diameter mm"]

df = pd.read_csv(SRC)
for b in BANNED:
    assert b not in CH.values(), b
df["y_bw"] = (df["label"] == "high_MSE_bit_wear").astype(np.int8)
stats = ["mean", "std", "slope", "last", "frac"]
rows = []
per_well = {}
for well, g in df.groupby("well"):
    g = g.sort_values("Measured Depth m").reset_index(drop=True)
    n = len(g)
    cols = {k: pd.to_numeric(g[v], errors="coerce").to_numpy() for k, v in CH.items()}
    y = g["y_bw"].to_numpy()
    nn = {k: np.isfinite(v) for k, v in cols.items()}
    cnt = 0
    for i in range(W, n - W + 1, STRIDE):
        sl = slice(i - W, i)          # fitur: masa lalu
        ll = slice(i, i + W)          # label: masa depan
        if nn["SPP"][sl].sum() < MIN_FEAT_NONNULL:
            continue
        fr = {}
        ok = True
        for k, v in cols.items():
            seg = v[sl]
            m = np.isfinite(seg)
            if m.sum() == 0:
                ok = False
                break
            x = seg[m]
            fr[f"{k}_mean"] = float(x.mean())
            fr[f"{k}_std"] = float(x.std()) if len(x) > 1 else 0.0
            if m.sum() >= 3 and x.std() > 0:
                fr[f"{k}_slope"] = float(np.polyfit(np.arange(len(seg))[m], x, 1)[0])
            else:
                fr[f"{k}_slope"] = 0.0
            fr[f"{k}_last"] = float(x[-1])
            fr[f"{k}_frac"] = float(m.mean())
        if not ok:
            continue
        frac_pos = float(y[ll].mean())
        fr["y_bitwear"] = int(frac_pos >= 0.5)
        fr["frac_pos_label_window"] = frac_pos
        fr["well"] = well
        fr["anchor_depth"] = float(g["Measured Depth m"].iloc[i])
        rows.append(fr)
        cnt += 1
    per_well[well] = {"rows": int(n), "windows": cnt}
    pos = sum(r["y_bitwear"] for r in rows if r["well"] == well)
    per_well[well]["positives"] = int(pos)
    per_well[well]["prev"] = round(pos / cnt, 4) if cnt else None
    print(f"== {well}: rows={n} windows={cnt} pos={pos} prev={per_well[well]['prev']}", flush=True)

d = pd.DataFrame(rows)
d.to_csv(OUT, index=False)
summary = {"per_well": per_well, "n_windows": int(len(d)),
           "n_features": int(len([c for c in d.columns if c not in
                                  ("y_bitwear", "frac_pos_label_window", "well", "anchor_depth")])),
           "banned_channels_excluded": BANNED}
json.dump(summary, open(SUM, "w"), indent=1)
print("total windows:", len(d), "features:", summary["n_features"],
      "positives:", int(d["y_bitwear"].sum()))
print("saved", OUT)
