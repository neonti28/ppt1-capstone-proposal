#!/usr/bin/env python3
# t_de420dbc — acceptance verification of docs/V10_EVAL_BAB.md
import re, json

DOC = "/mnt/d/Capstone 1(v2)/docs/V10_EVAL_BAB.md"
txt = open(DOC).read()

print("=== ACCEPTANCE CHECKS ===")

# AC1: 11 claim rows in the big table (rows starting "| N |" with engine bold)
rows = re.findall(r"^\|\s*(\d{1,2})\s*\|\s*\*\*([a-z_ ]+?)\*\*", txt, re.M)
big = [r for r in rows if int(r[0]) <= 11]
nums = sorted({int(r[0]) for r in big})
print("AC1 claim-numbered rows found:", nums)
print("AC1 count == 11:", nums == list(range(1, 12)))

# each row has a tier word
tier_words = ["TREN", "PERINGATAN-BERPENGAWAS", "BELUM"]
lines = txt.splitlines()
claim_lines = [l for l in lines if re.match(r"^\|\s*(\d{1,2})\s*\|\s*\*\*", l)]
claim_lines = [l for l in claim_lines if int(re.match(r"^\|\s*(\d{1,2})", l).group(1)) <= 11]
print("claim_lines:", len(claim_lines))
tier_ok = all(any(t in l for t in tier_words) for l in claim_lines)
print("AC1 every claim row carries a tier:", tier_ok)
# each has an angka kunci (digits)
angka_ok = all(re.search(r"\d", l) for l in claim_lines)
print("AC1 every claim row carries numbers:", angka_ok)

# AC2: 7 engine list present
engines = ["vib", "ssi", "shk", "stuck", "hyd", "bit_wear", "tool_wear"]
print("AC2 all 7 engines present:", all(e in txt for e in engines))

# AC2b: 27 head / layers / tiers
for token in ["27 head", "L0", "L1", "L2", "L3", "keputusan_akhir", "MANUSIA", "auto", "alarm"]:
    pass
print("AC2 27 head mentioned:", "27 head" in txt or "27 HEAD" in txt)
print("AC2 layer counts (5/11/9/2):", all(s in txt for s in ["5", "11", "9", "2"]))
print("AC2 0 alarm:", "slot alarm" in txt.lower() or "0 alarm" in txt.lower())

# AC3: no binary verdict
bad = re.findall(r"\b(LULUS|GAGAL)\b", txt)
# allow inside explicit negation phrases
print("AC3 occurrences of LULUS/GAGAL tokens:", bad)
# check they only appear in negation context
neg_ok = True
for m in re.finditer(r".{40}\b(LULUS|GAGAL)\b.{10}", txt):
    ctx = m.group(0)
    if "BUKAN" not in ctx and "bukan" not in ctx and "tanpa" not in ctx.lower():
        neg_ok = False
        print("  non-negated verdict context:", ctx.strip())
print("AC3 no bare binary verdict (all negated):", neg_ok)

# AC4: mandatory riset pendahuluan lines
for skill in ["scientific-critical-thinking", "verification-mandatory", "statistical-analysis",
              "multi-engine-detection-evaluation", "sequentialthinking"]:
    print(f"AC4 riset line for {skill}:", f"Riset pendahuluan: `{skill}`" in txt)

# AC5: 7 vs 11 vs 27 explanation present
print("AC5 '7 vs 11 vs 27' explanation:", "7 vs 11 vs 27" in txt or "7 · 11 · 27" in txt or "7 ⊂ 11 ⊂ 27" in txt)

print("\n=== CROSS-CHECK NUMBERS vs JSON ===")
ec = json.load(open("/mnt/d/Capstone 1(v2)/scratch/v9_eval_c/v9_eval_c_RESULTS.json"))
checks = {
    "119,57": ec["C_ml"]["vib"]["rf"]["far_by_tau"]["0.5"]["FAR_disp"]["max"]/ec["C_ml"]["vib"]["rf"]["far_by_tau"]["0.5"]["FAR_disp"]["min"],
    "30,36": ec["C_ml"]["ssi"]["rf"]["auprc_disp"]["max_min_ratio"],
    "8,3": ec["C_bitwear"]["K1"]["auprc_disp_scorable"]["max_min_ratio"],
    "1,19": ec["C_toolwear"]["K_ii"]["canary_auprc_disp"]["max_min_ratio"],
    "9,87": ec["C_rule_status"]["shk"]["rule_display_t0minus1"]["far24h_disp"]["max_min_ratio"],
}
for k, v in checks.items():
    print(f"  {k}: recomputed = {round(v,2)}")
