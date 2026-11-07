"""Independent spot-check: recompute angka yang dikutip di dokumen langsung dari
JSON SUMBER (bukan dari results EVAL_A) — jalur kedua (verification-mandatory #2)."""
import json, re, os

BASE = "/mnt/d/Capstone 1(v2)"
doc = open(os.path.join(BASE, "docs", "V9_EVAL_A_LAYERA.md")).read()
J = lambda p: json.load(open(p))
ml = {e: J(f"{BASE}/scratch/v9_e_ml/v9_e_ML_{e}_RESULTS.json") for e in ["vib", "ssi", "shk", "stuck_k2"]}
r1 = J(f"{BASE}/scratch/v9_e_rule/v9_e_RULE_01_status_results.json")
r2 = J(f"{BASE}/scratch/v9_e_rule/v9_e_RULE_02_stuck_onset_results.json")
s1 = J(f"{BASE}/scratch/v9_e_stat/v9_e_stat_01_hyd_ki_RESULTS.json")
s3 = J(f"{BASE}/scratch/v9_e_stat/v9_e_stat_03_tool_wear_RESULTS.json")

ok, fail = [], []
def chk(name, cond, detail=""):
    (ok if cond else fail).append((name, detail))

# 1. RF AUPRC ranges dikutip di dokumen
def range_of(eng, model="rf"):
    v = [f["models"][model]["auprc"] for f in ml[eng]["folds"]]
    return round(min(v), 3), round(max(v), 3)

chk("vib RF AUPRC 0,441-0,912", range_of("vib") == (0.441, 0.912), str(range_of("vib")))
chk("ssi RF AUPRC 0,015-0,459", range_of("ssi") == (0.015, 0.459), str(range_of("ssi")))
chk("shk RF AUPRC 0,007-0,193", range_of("shk") == (0.007, 0.193), str(range_of("shk")))
chk("stuck_k2 RF AUPRC 0,070-0,444", range_of("stuck_k2") == (0.070, 0.444), str(range_of("stuck_k2")))

# 2. FP rule totals
for cls, exp in [("vib", 197), ("ssi", 26), ("shk", 121), ("stuck_k1", 49), ("hyd_ki", 2091)]:
    fp = r1["classes"][cls]["aggregate"].get("rule_display_total_fp")
    chk(f"FP rule {cls} = {exp}", fp == exp, str(fp))
hyb_fp = sum(f["hybrid_rule_and_persistence"]["fp"] for f in r1["classes"]["hyd_ki"]["folds"])
chk("hyd_ki hybrid FP = 927", hyb_fp == 927, str(hyb_fp))
chk("stuck_k2 E1 FP alarm = 422",
    sum(f["rule_E1_2of3"]["onset"]["fp_alarm"] for f in r2["folds"]) == 422, "")

# 3. praktis counts (independen)
n6 = sum(1 for e in ml for f in ml[e]["folds"] for m in ["rf", "gb", "lr"]
         for t, tm in f["models"][m]["tau_metrics"].items()
         if t != "q95_train" and tm["FAR_24jam"] <= 6 and tm["recall"] > 0)
n1 = sum(1 for e in ml for f in ml[e]["folds"] for m in ["rf", "gb", "lr"]
         for t, tm in f["models"][m]["tau_metrics"].items()
         if t != "q95_train" and tm["FAR_24jam"] <= 1 and tm["recall"] > 0)
chk("total titik FAR<=6 & R>0 = 10", n6 == 10, str(n6))
chk("total titik FAR<=1 & R>0 = 4", n1 == 4, str(n1))
ngrid = sum(1 for e in ml for f in ml[e]["folds"] for m in ["rf", "gb", "lr"]
            for t in f["models"][m]["tau_metrics"] if t != "q95_train")
chk("total grid = 390", ngrid == 390, str(ngrid))

# 4. hybrid hyd_ki 8/9 (dokumen memakai 8/9)
w = sum(1 for f in r1["classes"]["hyd_ki"]["folds"]
        if f["hybrid_rule_and_persistence"]["auprc"] > f["persistence"]["auprc"])
chk("hybrid hyd_ki menang 8/9", w == 8, str(w))

# 5. shk rule 7/9 FAR<=6 & R>0
s = sum(1 for f in r1["classes"]["shk"]["folds"]
        if f["rule_display_t0minus1"]["far_24h"] <= 6 and f["rule_display_t0minus1"]["recall"] > 0)
chk("shk rule le6 = 7/9", s == 7, str(s))

# 6. hyd_ki persistence ranges
P = [f["engine_persistence"]["op"]["precision"] for f in s1["folds"]]
F = [f["engine_persistence"]["op"]["far_per_24h_neg"] for f in s1["folds"]]
chk("hyd_ki P 0,615-0,899", abs(min(P) - 0.6145) < 1e-3 and abs(max(P) - 0.8986) < 1e-3,
    f"{min(P):.3f}-{max(P):.3f}")
chk("hyd_ki FAR 32,4-110,7", abs(min(F) - 32.38) < 0.1 and abs(max(F) - 110.71) < 0.1,
    f"{min(F):.1f}-{max(F):.1f}")

# 7. tool_wear part C
pc = s3["part_C_operating_far_calibrated"]
chk("tool_wear part C FP 1-3", min(x["fp_R01"] for x in pc) == 1 and max(x["fp_R01"] for x in pc) == 3, "")
chk("tool_wear part C TLead 20-36 dtk", min(x["TLead_s"] for x in pc) == 20 and max(x["TLead_s"] for x in pc) == 36,
    f"{min(x['TLead_s'] for x in pc)}-{max(x['TLead_s'] for x in pc)}")
chk("tool_wear cp 8/8 p05 & p002",
    s3["part_A_change_point"]["run_level_sig_p05_v8"]["tp"] == 4 and
    s3["part_A_change_point"]["run_level_sig_p002_literal"]["tp"] == 4, "")

# 8. kutipan wajib ada di dokumen
for token in ["Riset pendahuluan: scientific-critical-thinking", "Riset pendahuluan: verification-mandatory",
              "Riset pendahuluan: statistical-analysis", "Riset pendahuluan: what-if-oracle",
              "Riset pendahuluan: consciousness-council", "Riset pendahuluan: sequentialthinking",
              "recompute 18/18", "cross-team 6/6", "memenuhi", "belum terukur",
              "BELUM DIVERIFIKASI", "per 24 jam", "per MENIT"]:
    chk(f"dokumen memuat '{token}'", token in doc, "")

# 9. tidak ada vonis biner terlarang (abaikan baris negasi eksplisit "BUKAN vonis ...")
body_wo_negation = re.sub(r"BUKAN vonis LULUS/GAGAL", "", doc)
bad = re.findall(r"\bLULUS\b|\bGAGAL\b(?! terukur)", body_wo_negation)
chk("tanpa vonis LULUS/GAGAL biner", len(bad) == 0, str(bad[:5]))

# 10. 7 engine & 11 klaim disebut
for e in ["vib", "ssi", "shk", "stuck", "hyd", "bit_wear", "tool_wear"]:
    chk(f"engine {e} dibahas", e in doc, "")

print(f"PASS {len(ok)} / FAIL {len(fail)} (total {len(ok)+len(fail)})")
for n, d in fail:
    print("  FAIL:", n, d)
for n, d in ok:
    print("  ok:", n, d if d else "")
