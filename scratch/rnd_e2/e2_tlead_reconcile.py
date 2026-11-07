"""RND-E2: rekonsiliasi angka TLead tool_wear antara JSON primer dan EVAL_C.

EVAL_C §2.7 menulis TLead 20-36 dtk (median 24,5; dispersi 1,8x).
JSON primer menyimpan t_lead_s per run dan TLead_to_end_R02_s.
Skrip ini menghitung ulang dari JSON dan melaporkan selisihnya apa adanya.
"""
from __future__ import annotations

import json
import statistics as st
from pathlib import Path

BASE = Path("/mnt/d/Capstone 1(v2)")
OUT = BASE / "scratch/rnd_e2"
d = json.loads((BASE / "scratch/v9_e_stat/v9_e_stat_03_tool_wear_RESULTS.json").read_text())
A = d["part_A_change_point"]
runs = A["runs"]

all_lead = {f"{r['tool']}/{r['run']}": r.get("t_lead_s") for r in runs}
r02_lead = {f"{r['tool']}/{r['run']}": r.get("t_lead_s") for r in runs if r["run"] == "R02"}
vals_all = [v for v in all_lead.values() if v is not None]
vals_r02 = [v for v in r02_lead.values() if v is not None]

out = {
    "t_lead_s_semua_run": all_lead,
    "t_lead_s_R02": r02_lead,
    "stat_semua_run": {"n": len(vals_all), "min": min(vals_all), "max": max(vals_all),
                       "median": st.median(vals_all),
                       "rasio_maks_min": round(max(vals_all) / min(vals_all), 4)},
    "stat_R02": {"n": len(vals_r02), "min": min(vals_r02), "max": max(vals_r02),
                 "median": st.median(vals_r02),
                 "rasio_maks_min": round(max(vals_r02) / min(vals_r02), 4)},
    "TLead_to_end_R02_s": A.get("TLead_to_end_R02_s"),
    "klaim_EVAL_C": "TLead 20-36 dtk (med 24,5; rasio 1,8x) — docs/V9_EVAL_C_LAYERC.md §2.7",
    "cross_family_spread_s": A.get("cross_family_spread_s"),
}
# median 20..36: apakah ada subset dengan median 24,5?
out["cek_median_24_5"] = {
    "median_semua": st.median(vals_all),
    "median_R02": st.median(vals_r02),
    "median_TLead_to_end": A["TLead_to_end_R02_s"]["median"],
    "cocok_24_5": any(abs(x - 24.5) < 1e-9 for x in
                      (st.median(vals_all), st.median(vals_r02),
                       A["TLead_to_end_R02_s"]["median"])),
}
(OUT / "e2_tlead_reconcile.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
print(json.dumps(out, indent=2, ensure_ascii=False))
