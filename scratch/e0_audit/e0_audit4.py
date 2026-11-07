#!/usr/bin/env python3
"""E0 audit bagian 4: peluang kebetulan tool_wear, definisi segmen pipeline."""
import json

import numpy as np
import pandas as pd

BASE = "/mnt/d/Capstone 1(v2)"
OUTDIR = "/home/neonti/.hermes/kanban/boards/rnd-algo-2026/workspaces/t_57e7d52b"
res = {}
R = json.load(open(f"{BASE}/scratch/v9_i1/v9_i1_RESULTS.json"))
tw = [e for e in R["engines"] if e["engine"] == "tool_wear"][0]
H = {h["head"]: h for h in tw["heads"]}
cal = {t["alat"]: t for t in H["calib_5of27"]["per_alat"]}
op = {t["alat"]: t for t in H["op_far_calibrated"]["per_alat"]}
rows = []
for alat in sorted(cal):
    c, o = cal[alat], op.get(alat, {})
    n_eval, n_r02 = c["n_eval_R01"], c["n_R02"]
    fp_op, fp_eng = o.get("fp_R01"), c.get("fp_R01")
    r_op = fp_op / n_eval if (fp_op is not None and n_eval) else None
    r_eng = fp_eng / n_eval if (fp_eng is not None and n_eval) else None
    rows.append({
        "alat": alat, "n_kalibrasi": c["n_kalibrasi"], "n_eval_R01": n_eval,
        "n_R02": n_r02, "fp_engine_5of27": fp_eng, "fp_op_calibrated": fp_op,
        "laju_op_per_detik": None if r_op is None else round(r_op, 5),
        "harapan_alarm_kebetulan_R02": None if r_op is None else round(r_op * n_r02, 3),
        "P_min1_alarm_kebetulan": None if r_op is None else round(float(1 - np.exp(-r_op * n_r02)), 4),
        "det_op": o.get("det_R02"), "TLead_s_op": o.get("TLead_s"),
        "pct_R02_alarmed": o.get("pct_R02_alarmed"),
        "thr": o.get("thr_featcount"),
    })
res["tool_wear"] = rows
pvals = [r["P_min1_alarm_kebetulan"] for r in rows if r["P_min1_alarm_kebetulan"]]
res["P_4dari4_kebetulan"] = round(float(np.prod(pvals)), 4) if pvals else None
res["ringkas"] = {
    "n_alat": len(rows),
    "det_4dari4": sum(1 for r in rows if r["det_op"]),
    "target_fp_per_min": H["op_far_calibrated"].get("target_fp_per_min", 1.0),
    "metrik_segmen_op": H["op_far_calibrated"]["metrik_segmen"],
    "metrik_segmen_engine": H["calib_5of27"]["metrik_segmen"],
}
for r in rows:
    print(r)
print("P(4/4 kebetulan) =", res["P_4dari4_kebetulan"])
print("ringkas:", json.dumps(res["ringkas"], indent=1))
json.dump(res, open(f"{OUTDIR}/e0_audit_results4.json", "w"), indent=1, default=str)
