import json
p = "/mnt/d/Capstone 1(v2)/scratch/v9_i1/v9_i1_RESULTS.json"
d = json.load(open(p))

print("=== META ===")
print(json.dumps(d["meta"], indent=1, ensure_ascii=False)[:2500])

print("\n=== SEGMEN INFO ===")
print(json.dumps(d["segmen_info"], indent=1, ensure_ascii=False)[:1500])

print("\n=== ENGINES (7) ===")
for e in d["engines"]:
    print("\n---")
    print(json.dumps(e, indent=1, ensure_ascii=False)[:3000])

print("\n=== DECISION LAYER ===")
print(json.dumps(d["decision_layer"], indent=1, ensure_ascii=False)[:2000])
