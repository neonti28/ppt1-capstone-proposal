import json
B = "/mnt/d/Capstone 1(v2)"
d = json.load(open(f"{B}/scratch/v9_i1/v9_i1_RESULTS.json"))
for e in d["engines"]:
    print("=== ENGINE ===")
    print(json.dumps(e, indent=1)[:1800])
