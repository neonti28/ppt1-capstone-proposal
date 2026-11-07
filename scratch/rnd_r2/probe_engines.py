import json
p = "/mnt/d/Capstone 1(v2)/scratch/v9_i1/v9_i1_RESULTS.json"
d = json.load(open(p))
for e in d["engines"]:
    print("=" * 70)
    print("ENGINE:", e.get("engine"), "| keys:", list(e.keys()))
    for k, v in e.items():
        s = json.dumps(v, ensure_ascii=False)
        if len(s) > 700:
            s = s[:700] + " ...TRUNC"
        print(f"  {k}: {s}")
