import json, sys
p = "/mnt/d/Capstone 1(v2)/scratch/v9_i1/v9_i1_RESULTS.json"
d = json.load(open(p))
print("TOP KEYS:", list(d.keys())[:40])
meta = d.get("meta", {})
print("META:", json.dumps(meta, indent=1)[:800])
for k, v in d.items():
    if isinstance(v, dict):
        print("---", k, "dict keys:", list(v.keys())[:15])
    elif isinstance(v, list):
        print("---", k, "list len", len(v))
    else:
        print("---", k, type(v).__name__, str(v)[:100])
