#!/usr/bin/env python3
"""RND-E0 meas5 — titik operasi tool_wear: apakah FAR <=1 alarm/menit itu TERUKUR
atau hanya DEFINISI?

Replikasi identik resep code/v9_i1_pipeline.py:594-690 (CAL_FRAC 0.30, Z 3.0,
N_FEAT_ALARM 5), lalu tambah varian:
  A. kode apa adanya  : ambang = kuantil skor pada HIMPUNAN EVALUASI (ev1, R01
                        setelah kalibrasi) -> FP_R01 diukur pada data yang sama
                        yang dipakai memilih ambang (in-sample).
  B. ambang kausal    : ambang = kuantil skor pada SUBSET KALIBRASI (cal) saja,
                        lalu FP_R01 diukur di ev1 (out-of-sample).

Tulis: scratch/rnd_e0/meas5_toolwear.json
"""
from __future__ import annotations

import json
import math

import numpy as np
import pandas as pd

TW = "/mnt/d/Capstone 1(v2)/scratch/v6_e1/toolwear_windows.csv"
OUT = "/mnt/d/Capstone 1(v2)/scratch/rnd_e0/meas5_toolwear.json"
TARGET_FP_PER_MIN = 1.0
Z_THR = 3.0
N_FEAT = 5
CAL_FRAC = 0.30

tw = pd.read_csv(TW)
feats = [c for c in tw.columns
         if c.endswith(("_mean", "_std", "_rms", "_kurt", "_skew", "_p2p",
                        "_crest", "_zcr", "_fdom"))]
assert len(feats) == 27, len(feats)

rows = []
for tool, g in tw.groupby("tool"):
    r01 = g[g["run"] == "R01"].sort_values("start_sample")
    r02 = g[g["run"] == "R02"].sort_values("start_sample")
    ncal = max(5, int(math.ceil(CAL_FRAC * len(r01))))
    cal, ev1 = r01.iloc[:ncal], r01.iloc[ncal:]
    med = cal[feats].median()
    mad = (cal[feats] - med).abs().median() * 1.4826
    mad = mad.replace(0, np.nan)

    def sc(ev):
        Z = ((ev[feats] - med) / mad).abs()
        return (Z > Z_THR).sum(axis=1).to_numpy()

    s_cal, s1, s2 = sc(cal), sc(ev1), sc(r02)

    # --- rumus kode apa adanya ---
    q = 1.0 - TARGET_FP_PER_MIN * (len(ev1) / 60.0) / max(len(ev1), 1)
    q_clip = min(max(q, 0.5), 1.0)
    thr_insample = float(np.quantile(s1, q_clip))
    o1 = s1 >= thr_insample
    o2 = s2 >= thr_insample

    # --- varian kausal: ambang dari subset kalibrasi ---
    thr_causal = float(np.quantile(s_cal, q_clip))
    c1 = s1 >= thr_causal
    c2 = s2 >= thr_causal

    neg_min_ev1 = len(ev1)  # jendela 1 detik -> n jendela = n detik = n/60 menit
    rows.append({
        "alat": tool,
        "n_R01": int(len(r01)), "n_kalibrasi": int(ncal),
        "n_eval_R01": int(len(ev1)), "n_R02": int(len(r02)),
        "q_rumus": round(q, 6),
        "q_setelah_clip": round(q_clip, 6),
        "q_sama_untuk_semua_panjang": abs(q - (1.0 - 1.0 / 60.0)) < 1e-12,
        "A_ambang_insample": {
            "thr": thr_insample,
            "fp_R01": int(o1.sum()),
            "frac_R01_alarm": round(float(o1.mean()), 4) if len(o1) else None,
            "far_fp_per_menit_R01": round(int(o1.sum()) / (len(ev1) / 60.0), 3) if len(ev1) else None,
            "det_R02": bool(o2.any()),
            "frac_R02_alarm": round(float(o2.mean()), 4) if len(o2) else None,
        },
        "B_ambang_kausal": {
            "thr": thr_causal,
            "fp_R01": int(c1.sum()),
            "frac_R01_alarm": round(float(c1.mean()), 4) if len(c1) else None,
            "far_fp_per_menit_R01": round(int(c1.sum()) / (len(ev1) / 60.0), 3) if len(ev1) else None,
            "det_R02": bool(c2.any()),
            "frac_R02_alarm": round(float(c2.mean()), 4) if len(c2) else None,
        },
        "skor_unik_eval": sorted(set(int(v) for v in s1)),
    })

agg = {
    "n_alat": len(rows),
    "A_total_fp_R01": sum(r["A_ambang_insample"]["fp_R01"] for r in rows),
    "B_total_fp_R01": sum(r["B_ambang_kausal"]["fp_R01"] for r in rows),
    "n_eval_total": sum(r["n_eval_R01"] for r in rows),
    "A_det_alat": sum(1 for r in rows if r["A_ambang_insample"]["det_R02"]),
    "B_det_alat": sum(1 for r in rows if r["B_ambang_kausal"]["det_R02"]),
}
agg["A_far_per_menit_gabungan"] = round(agg["A_total_fp_R01"] / (agg["n_eval_total"] / 60.0), 3)
agg["B_far_per_menit_gabungan"] = round(agg["B_total_fp_R01"] / (agg["n_eval_total"] / 60.0), 3)

res = {"meta": {"sumber_data": TW, "n_jendela": len(tw), "n_fitur": len(feats),
                "target_fp_per_menit": TARGET_FP_PER_MIN},
       "per_alat": rows, "agregat": agg}
json.dump(res, open(OUT, "w"), indent=1, ensure_ascii=False)

print(f"jendela={len(tw)} alat={len(rows)} fitur={len(feats)}")
print(f"{'alat':<6}{'ncal':>5}{'nEv':>5}{'nR02':>5}{'q':>10}{'thrA':>7}{'fpA':>5}{'FAR_A':>8}{'thrB':>7}{'fpB':>5}{'FAR_B':>8}")
for r in rows:
    print(f"{r['alat']:<6}{r['n_kalibrasi']:>5}{r['n_eval_R01']:>5}{r['n_R02']:>5}"
          f"{r['q_setelah_clip']:>10.6f}{r['A_ambang_insample']['thr']:>7.0f}"
          f"{r['A_ambang_insample']['fp_R01']:>5}{r['A_ambang_insample']['far_fp_per_menit_R01']:>8.2f}"
          f"{r['B_ambang_kausal']['thr']:>7.0f}{r['B_ambang_kausal']['fp_R01']:>5}"
          f"{r['B_ambang_kausal']['far_fp_per_menit_R01']:>8.2f}")
print("AGREGAT A (insample):", json.dumps(agg, ensure_ascii=False))
print("tulis:", OUT)
