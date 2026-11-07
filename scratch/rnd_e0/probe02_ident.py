import json

P1 = "/mnt/d/Capstone 1(v2)/scratch/v9_e_rule/v9_e_RULE_01_status_results.json"
d = json.load(open(P1))
for cls, v in d["classes"].items():
    print("=" * 70)
    print(cls)
    print(" identity:", json.dumps(v["identity_rule_window_vs_label"], ensure_ascii=False))
    f = v["folds"]
    print(" n_folds:", len(f), "| fold keys:", list(f[0].keys()) if f else None)
    if f:
        print(" fold0:", json.dumps(f[0], ensure_ascii=False)[:900])
    print(" aggregate:", json.dumps(v["aggregate"], ensure_ascii=False)[:900])
