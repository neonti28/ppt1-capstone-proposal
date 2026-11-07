import json
base = "/mnt/d/Capstone 1(v2)/scratch/rnd/e4"
b = json.load(open(f"{base}/e4_baseline.json"))
print("total_fp:", json.dumps(b["total_fp"])[:300])
print("assert_r7_1:", b["assert_r7_1"])
f0 = b["folds"][0]
print("fold0 keys:", sorted(f0.keys()))
print("fold0:", json.dumps(f0, indent=1)[:700])
s = json.load(open(f"{base}/e4_summary.json"))
print("\nsummary assert:", s["assert_r7_1"])
print("elapsed:", s["elapsed_s"])
au = json.load(open(f"{base}/e4_audit_label.json"))
print("\naudit agregat:", json.dumps(au["agregat"], indent=1))
g = json.load(open(f"{base}/e4_gate_decomp.json"))
print("\ndecomp hybrid:", g["hybrid_rule_persistence"])
print("decomp H_and:", g["H_and_hybrid_ML"])
ba = json.load(open(f"{base}/e4_beforeafter.json"))
print("\nbeforeafter keys:", list(ba.keys()))
