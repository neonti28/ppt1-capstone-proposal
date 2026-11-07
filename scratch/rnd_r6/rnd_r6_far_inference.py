"""R6 pelengkap: inferensi FAR (Poisson eksak) dan galat keputusan di gerbang FAR<=6."""
import json
import math
from pathlib import Path

import numpy as np
from scipy import stats

BASE = Path("/mnt/d/Capstone 1(v2)")
SCR = BASE / "scratch"
OUT = SCR / "rnd_r6" / "rnd_r6_far_inference.json"

i1 = json.loads((SCR / "v9_i1" / "v9_i1_RESULTS.json").read_text(encoding="utf-8"))

GATE = 6.0  # konvensi gerbang A: FAR <= 6 per 24 jam operatif negatif
rows = []
for e in i1["engines"]:
    for h in e["heads"]:
        m = h.get("metrik_segmen")
        if not m:
            continue
        fp, neg = m.get("fp"), m.get("neg")
        if fp is None or not neg:
            continue
        unit = m.get("far_unit") or ""
        if "jendela 60" in unit:
            per_day = 1440.0
            satuan = "FP/24 jam-negatif"
        elif "jendela 1 dtk" in unit:
            per_day = 60.0
            satuan = "FP/menit-negatif"
        else:
            continue
        expose_day = neg / per_day              # hari-operasi-negatif
        lam_hat = fp / expose_day               # FAR titik
        # CI eksak Poisson untuk lambda_total, lalu diskalakan
        lo_cnt = 0.0 if fp == 0 else stats.chi2.ppf(0.025, 2 * fp) / 2
        hi_cnt = stats.chi2.ppf(0.975, 2 * (fp + 1)) / 2
        lo = lo_cnt / expose_day
        hi = hi_cnt / expose_day
        # uji satu sisi H0: FAR >= 6 (mau buktikan FAR < 6)
        lam0 = GATE * expose_day
        p_less = float(stats.poisson.cdf(fp, lam0))          # p utk H1: FAR < 6
        p_greater = float(1 - stats.poisson.cdf(fp - 1, lam0)) if fp > 0 else 1.0
        rows.append({
            "engine": e["engine"], "head": h["head"], "klaim": h.get("klaim"),
            "fp": fp, "neg": neg, "satuan": satuan,
            "expose_hari_negatif": expose_day,
            "far_titik": lam_hat,
            "far_ci95_lo": lo, "far_ci95_hi": hi,
            "lebar_ci_relatif": (hi - lo) / lam_hat if lam_hat else None,
            "p_FAR_di_bawah_6": p_less,
            "p_FAR_di_atas_6": p_greater,
            "terbukti_di_bawah_6": bool(hi < GATE),
            "terbukti_di_atas_6": bool(lo > GATE),
            "tidak_konklusif": bool(lo <= GATE <= hi),
        })

out = {"gerbang": GATE, "satuan_gerbang": "FP/24 jam-negatif (rig) atau FP/menit (bengkel)",
       "n_head": len(rows), "rows": rows,
       "rekap": {
           "terbukti_di_bawah_6": sum(1 for r in rows if r["terbukti_di_bawah_6"]),
           "terbukti_di_atas_6": sum(1 for r in rows if r["terbukti_di_atas_6"]),
           "tidak_konklusif": sum(1 for r in rows if r["tidak_konklusif"]),
       }}
OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")

print(f"{'engine':9s} {'head':30s} {'fp':>5s} {'FAR':>9s} {'CI lo':>9s} {'CI hi':>10s} "
      f"{'<6?':>4s} {'>6?':>4s} {'?':>3s}")
for r in rows:
    print(f"{r['engine']:9s} {str(r['head'])[:30]:30s} {r['fp']:5d} {r['far_titik']:9.3f} "
          f"{r['far_ci95_lo']:9.3f} {r['far_ci95_hi']:10.3f} "
          f"{'Y' if r['terbukti_di_bawah_6'] else '.':>4s} "
          f"{'Y' if r['terbukti_di_atas_6'] else '.':>4s} "
          f"{'Y' if r['tidak_konklusif'] else '.':>3s}")
print("\nrekap:", out["rekap"])
print("-> ", OUT)
