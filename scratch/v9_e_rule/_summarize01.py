import json

r = json.load(open("/mnt/d/Capstone 1/scratch/v9_e_rule/v9_e_RULE_01_status_results.json"))
for cls, d in r["classes"].items():
    ident = d["identity_rule_window_vs_label"]
    print(f"== {cls}: identity={ident}")
    a = d["aggregate"]
    for k, v in a.items():
        print("   ", k, v)
    f0 = d["folds"][0]
    print("   fold0 keys:", list(f0.keys()))
    print("   rule fold0:", {k: f0["rule_display_t0minus1"].get(k) for k in
          ("tp", "fp", "precision", "recall", "far_24h", "auprc")})
    if "rule_E1_2of3" in f0:
        print("   E1 fold0:", f0["rule_E1_2of3"])
    if "hybrid_E1_and_persistence" in f0:
        print("   hybE1 fold0:", f0["hybrid_E1_and_persistence"])
    print("   persist fold0:", f0["persistence"])
