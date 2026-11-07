"""Verifikasi: apakah h=30 dipilih karena memenuhi anggaran, atau karena saturasi grid."""
import json
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, "/mnt/d/Capstone 1(v2)/code")
import rnd_hybrid_harness as H

DS = f"{H.DSD}/hyd_ki.csv.gz"
LOWO = f"{H.LOWOD}/lowo_hyd_ki.json"

df = H.muat_dataset(DS)
folds = H.muat_fold(LOWO)
well_df = H.pecah_well(df)

print("budget alpha =", H.ALPHA_BUDGET, " grid maks =", H.H_GRID[-1])
print()
print(f"{'fold':8} {'cal_well':10} {'n_cal':>6} {'laju_h30':>10} {'lolos_budget':>12} {'h_dipilih':>9}")
sat = 0
for f in folds:
    w = f["test_well"]
    cal = f["train_wells"][0]
    dc = well_df[cal]
    ts_c = dc["ts_bin"].to_numpy(int)
    zc, _ = H.seri_z(cal, ts_c)
    laju30 = float(H.cusum_alarm(zc, H.H_GRID[-1]).mean())
    lolos = laju30 <= H.ALPHA_BUDGET
    if not lolos:
        sat += 1
    print(f"{w:8} {cal:10} {len(zc):6d} {laju30:10.6f} {str(lolos):>12} {H.pilih_h(zc):>9}")
print()
print(f"fold dengan h saturasi di batas grid: {sat} dari {len(folds)}")

# Apakah ada h di atas 30 yang bisa memenuhi anggaran?
print()
print("Uji h di luar grid (40..400) pada well kalibrasi pertama:")
cal0 = folds[0]["train_wells"][0]
zc0, _ = H.seri_z(cal0, well_df[cal0]["ts_bin"].to_numpy(int))
for h in (30, 40, 60, 80, 100, 150, 200, 300, 400):
    print(f"  h={h:4d} laju={float(H.cusum_alarm(zc0, h).mean()):.6f} lolos={float(H.cusum_alarm(zc0, h).mean()) <= H.ALPHA_BUDGET}")

# R8 sumber angka
print()
r8 = json.load(open("/mnt/d/Capstone 1(v2)/scratch/rnd/r8/r8_hyd.json"))
print("R8 ringkas H1:", json.dumps(r8["ringkas"]["H1_stat_dan_rule"], indent=1))
print()
d = json.load(open("/mnt/d/Capstone 1(v2)/scratch/rnd/s1/s1_hyd_seeds.json"))
print("reproduksi.ringkas_r8 == R8 ringkas?",
      d["reproduksi"]["ringkas_r8"] == r8["ringkas"]["H1_stat_dan_rule"])
print("reproduksi.ringkas_kini:", json.dumps(d["reproduksi"]["ringkas_kini"], indent=1)[:600])
