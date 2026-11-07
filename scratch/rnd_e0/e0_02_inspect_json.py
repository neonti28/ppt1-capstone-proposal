#!/usr/bin/env python3
"""RND-E0 probe 02 — baca JSON primer kampanye (angka yang dilaporkan) tanpa mengubah apa pun."""
import json

BASE = "/mnt/d/Capstone 1(v2)"
R1 = json.load(open(f"{BASE}/scratch/v9_e_rule/v9_e_RULE_01_status_results.json"))
R2 = json.load(open(f"{BASE}/scratch/v9_e_rule/v9_e_RULE_02_stuck_onset_results.json"))
R3 = json.load(open(f"{BASE}/scratch/v9_e_rule/v9_e_RULE_03_bitwear_toolwear_results.json"))
S3 = json.load(open(f"{BASE}/scratch/v9_e_stat/v9_e_stat_03_tool_wear_RESULTS.json"))
P1 = json.load(open(f"{BASE}/scratch/v9_i1/v9_i1_RESULTS.json"))

print("== meta R1:", R1["meta"]["far_convention"])
print("\n== identitas rule-jendela-label (R1)")
for cls, blk in R1["classes"].items():
    print(f"  {cls:9} identity={blk['identity_rule_window_vs_label']}")

print("\n== R1 per kelas: total FP rule, fold, P rule")
for cls, blk in R1["classes"].items():
    fps = [f["rule_display_t0minus1"]["fp"] for f in blk["folds"]]
    ps = [f["rule_display_t0minus1"]["precision"] for f in blk["folds"]]
    ns = [f["n"] for f in blk["folds"]]
    prevs = [f["prev"] for f in blk["folds"]]
    print(f"  {cls:9} folds={len(fps)} FP_total={sum(fps)} sum_n={sum(ns)} "
          f"P={ps}")
    print(f"            nperfold={ns} prev={prevs}")
    far = [f["rule_display_t0minus1"]["far_24h"] for f in blk["folds"]]
    print(f"            FAR24 per fold={far}")

print("\n== S3 tool_wear part_B per_tool")
for t in S3["part_B_within_tool_calibration"]["per_tool"]:
    e = t["engine_5of27"]
    print(f"  {t['tool']} n_cal={t['n_cal']} n_eval_R01={t['n_eval_R01']} n_R02={t['n_R02']} "
          f"fp_R01={e['fp_R01']} pct={e['pct_R01_alarmed']} FAR/min={e['far_fp_per_min_R01']} "
          f"det={e['detected_R02']} TLead={e['TLead_to_end_R02_s']}")
print("  aggregate:", S3["part_B_within_tool_calibration"]["aggregate"])

print("\n== S3 part_C (target vs capaian)")
for r in S3["part_C_operating_far_calibrated"]:
    print(f"  target={r['target_fp_per_min']} {r['tool']} thr={r['thr_featcount']} "
          f"fp_R01={r['fp_R01']} det={r['det_R02']} TLead={r['TLead_s']} pct_R02={r['pct_R02_alarmed']}")

print("\n== S3 part_D:", S3["part_D_ranking_auprc"])

print("\n== R3 bitwear per fold")
for f in R3["bitwear_k1"]["folds"]:
    print(f"  {f['test_well']}: n={f['n']} pos={f['pos']} prev={f['prev']} "
          f"pers.auprc={f['persistence']['auprc']} n_pers={f['persistence']['n_persistence']} "
          f"canary={f['canary_depth']['auprc']}")
print("  agg:", R3["bitwear_k1"]["aggregate"])

print("\n== R3 toolwear folds")
for f in R3["toolwear_kii"]["folds"]:
    print(f"  {f['test_tool']}: n={f['n']} pos={f['pos']} prev={f['prev']} "
          f"canary3rms={f['canary_3rms']['auprc']} persDiag={f['persistence_diagnostic']['auprc']}")

print("\n== R2 stuck onset aggregate:", json.dumps(R2["aggregate"], default=str)[:800])
for f in R2["folds"]:
    print(f"  {f['test_well']}: n={f['n']} pos={f['pos']} onsets={f['n_onsets']} "
          f"E1.FP={f['rule_E1_2of3']['fp']} E1.P={f['rule_E1_2of3']['precision']} "
          f"pev.FP={f['persistence_event']['fp']} pev.TLead={f['persistence_event']['onset']['tlead_min']}")

print("\n== I1 segmen info:", json.dumps(P1["segmen_info"], indent=1)[:1200])
print("\n== I1 meta:", json.dumps(P1["meta"], indent=1))
for e in P1["engines"]:
    for h in e["heads"]:
        print(f"  {e['engine']:10} {h['head']:28} tier={h['tier']:24} n={h['n_windows']} "
              f"n_aktif={h.get('n_aktif')} metrik={json.dumps(h.get('metrik_segmen'))}")
print("\n== I1 decision ringkasan:", P1["decision_layer"]["ringkasan"],
      "L1:", P1["decision_layer"]["nperingatan_l1"])
