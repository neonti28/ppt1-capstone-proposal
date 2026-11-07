#!/usr/bin/env python3
"""Smoke test satu fold vib sebelum run penuh: seleksi kanal + satu ML + satu evaluasi."""
import sys
import time

import numpy as np

BASE = "/mnt/d/Capstone 1(v2)"
sys.path.insert(0, f"{BASE}/code")
sys.path.insert(0, f"{BASE}/scratch/rnd/s2")
import rnd_hybrid_harness as H
import s2a_run as S

t0 = time.time()
cache = S.CacheSinyal("vib")
df = H.muat_dataset(f"{BASE}/scratch/v9_d1/datasets/vib.csv.gz")
well_df = H.pecah_well(df)
folds = H.muat_fold(f"{BASE}/scratch/v9_d1/lowo_vib.json")
feats = H.fitur_dari(df)
print("n_fitur:", len(feats), "contoh:", feats[:5], flush=True)
f = folds[0]
sel = S.pilih_kanal_rule(well_df, f, "y_vib", cache)
print("seleksi:", sel, flush=True)

w = f["test_well"]
d = well_df[w]
y = d["y_vib"].to_numpy(int)
ts = d["ts_bin"].to_numpy(int)
cal0 = f["train_wells"][0]
sig = H.detektor_stat_rule(w, ts, cal0, well_df[cal0]["ts_bin"].to_numpy(int),
                           chan=sel["kanal"], alpha=H.ALPHA_BUDGET)
rule = cache.gerbang(w, ts, sel["kanal"], sel["thr"])
print("h:", sig["h"], "alarm stat:", int(sig["stat"].sum()), "alarm rule:", int(rule.sum()), flush=True)
rec = S.evaluasi("H1_stat_dan_rule", ((sig["stat"] == 1) & (rule == 1)).astype(int), y, ts)
print("rec H1:", {k: rec[k] for k in ("far24_kalender", "cakupan", "gate_A_baru", "lolos_far_recall")},
      rec["rows"], flush=True)

info = H.skor_ml_fold(well_df, f, "y_vib", feats, seed=42, alpha=H.ALPHA_BUDGET)
kk = S.latih_ulang_untuk_kalibrasi(well_df, f, "y_vib", feats, 42)
print("ambang harness:", info["ambang"], "ambang komposisi:", kk["ambang_conformal_komposisi"],
      "sama:", abs(info["ambang"] - kk["ambang_conformal_komposisi"]) < 1e-12, flush=True)
ak = S.ambang_kalender(kk["skor_cal"], kk["y_cal"], well_df[kk["cal_well"]]["ts_bin"].to_numpy(int))
print("ambang kalender:", ak, flush=True)
print("n_alarm conformal:", int((info["skor"] >= info["ambang"]).sum()),
      "n_alarm kalender:", int((info["skor"] >= ak["ambang"]).sum()), flush=True)
print("durasi:", round(time.time() - t0, 1), "s")
