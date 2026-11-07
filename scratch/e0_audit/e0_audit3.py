#!/usr/bin/env python3
"""E0 audit bagian 3: angka JSON yang dilaporkan, unit FAR bit_wear, rujukan arsip v9."""
import json
import os
import re

import numpy as np
import pandas as pd

BASE = "/mnt/d/Capstone 1(v2)"
OUTDIR = "/home/neonti/.hermes/kanban/boards/rnd-algo-2026/workspaces/t_57e7d52b"
res = {}

# ---------------------------------------------------------- A. v9_i1 RESULTS
R = json.load(open(f"{BASE}/scratch/v9_i1/v9_i1_RESULTS.json"))
print("meta:", {k: R["meta"][k] for k in ("generated_at", "seed") if k in R["meta"]})
eng = {e["engine"]: e for e in R["engines"]}
summ = {}
for name, e in eng.items():
    hs = {}
    for h in e["heads"]:
        hs[h["head"]] = {"tier": h.get("tier"), "layer": h.get("layer"),
                         "metrik_segmen": h.get("metrik_segmen"),
                         "n_aktif": h.get("n_aktif"), "frac_aktif": h.get("frac_aktif")}
    summ[name] = hs
res["v9_i1_head_metrics"] = summ
for name in ("bit_wear", "vib", "hyd", "tool_wear"):
    print(f"-- {name}")
    for k, v in summ[name].items():
        print("   ", k, v["tier"], v["layer"], v["metrik_segmen"])
print("decision_layer:", R["decision_layer"]["ringkasan"],
      "nperingatan_l1=", R["decision_layer"]["nperingatan_l1"])

# per_alat tool_wear
tw = eng["tool_wear"]["heads"]
op = [h for h in tw if h["head"] == "op_far_calibrated"][0]
lam = []
for t in op.get("per_alat", []):
    fp, n_eval, n_r02 = t.get("fp_R01"), t.get("n_eval_R01"), t.get("n_R02")
    if None in (fp, n_eval, n_r02) or not n_eval:
        continue
    rate = fp / n_eval
    lam.append({"alat": t["alat"], "fp_R01": fp, "n_eval_R01": n_eval,
                "laju_alarm_per_detik": round(rate, 5), "n_R02": n_r02,
                "harapan_alarm_di_R02": round(rate * n_r02, 3),
                "P_minimal_1_alarm_kebetulan": round(float(1 - np.exp(-rate * n_r02)), 4),
                "det_benar": t.get("det_R02"), "TLead_s": t.get("TLead_s")})
res["tool_wear_kebetulan"] = lam
res["tool_wear_op_head"] = {k: op.get(k) for k in
                            ("metrik_segmen", "thr_featcount", "target_fp_per_min")}
print("-- tool_wear kebetulan")
for x in lam:
    print("   ", x)

# --------------------------------------------------- B. RULE JSON: tier delta
RU = json.load(open(f"{BASE}/scratch/v9_e_rule/v9_e_RULE_01_status_results.json"))
rule_sum = {}
for cls, blk in RU["classes"].items():
    folds = blk["folds"]
    def agg(key, field):
        v = [f[key].get(field) for f in folds if key in f and f[key].get(field) is not None]
        return None if not v else [round(float(x), 4) for x in v]
    rule_sum[cls] = {
        "identity": blk.get("identity_rule_window_vs_label"),
        "rule_P": agg("rule_display_t0minus1", "precision"),
        "rule_R": agg("rule_display_t0minus1", "recall"),
        "rule_FP": agg("rule_display_t0minus1", "fp"),
        "rule_FAR24": [None if x is None else round(x, 2) for x in
                       ([f["rule_display_t0minus1"].get("far_24h") for f in folds])],
        "hybrid_P": agg("hybrid_rule_and_persistence", "precision"),
        "hybrid_FP": agg("hybrid_rule_and_persistence", "fp"),
        "pers_P": agg("persistence", "precision"),
        "n_folds": len(folds),
        "wells": [f["test_well"] for f in folds],
    }
res["rule_json"] = rule_sum
for cls in ("vib", "ssi", "shk", "hyd_ki", "stuck_k1"):
    d = rule_sum[cls]
    print(f"-- {cls} P={d['rule_P']} hybP={d['hybrid_P']} FP={d['rule_FP']} "
          f"ident={None if not d['identity'] else d['identity'].get('identity')}")

# --------------------------------------------- C. bit_wear: unit & grouping
u = pd.read_csv(f"{BASE}/data/USROP_labeled.csv",
                usecols=["well", "Measured Depth m", "label"])
u = u.sort_values("Measured Depth m").reset_index(drop=True)
is_mse = (u["label"] == "high_MSE_bit_wear").to_numpy().astype(int)
pers = np.concatenate([[0], is_mse[:-1]])
bp = (is_mse[pers == 1]).mean() if (pers == 1).any() else None
res["bit_wear_pipeline"] = {
    "n_rows": int(len(u)), "n_pos": int(is_mse.sum()),
    "wells": {str(k): int(v) for k, v in u["well"].value_counts().items()},
    "P_pers_pipeline_style": None if bp is None else round(float(bp), 4),
    "n_boundary_rows": int(u["well"].nunique() - 1),
    "depth_min": float(u["Measured Depth m"].min()),
    "depth_max": float(u["Measured Depth m"].max()),
    "depth_step_median": float(np.median(np.diff(np.sort(u["Measured Depth m"].unique())))),
}
print("-- bit_wear:", json.dumps(res["bit_wear_pipeline"], indent=1))

# ---------------------------------------- D. rujukan folder arsip pada v9_*
hits = []
for fn in sorted(os.listdir(f"{BASE}/code")):
    if not fn.endswith(".py"):
        continue
    txt = open(f"{BASE}/code/{fn}", errors="ignore").read()
    for i, line in enumerate(txt.splitlines(), 1):
        if "/mnt/d/Capstone 1/" in line and "(v2)" not in line:
            hits.append(f"{fn}:{i}: {line.strip()}")
v9hits = [h for h in hits if h.startswith("v9_")]
res["arsip_refs"] = {"total_py": len(hits), "v9_py": len(v9hits),
                     "v9_contoh": v9hits[:20], "semua_contoh": hits[:10]}
print("-- rujukan arsip: total", len(hits), "di v9_*:", len(v9hits))
for h in v9hits[:10]:
    print("   ", h)

json.dump(res, open(f"{OUTDIR}/e0_audit_results3.json", "w"), indent=1, default=str)
print("SELESAI")
