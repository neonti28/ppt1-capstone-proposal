import json, sys
p = "/mnt/d/Capstone 1(v2)/scratch/v9_i1/v9_i1_RESULTS.json"
d = json.load(open(p))
print("TOP TYPE:", type(d).__name__)
if isinstance(d, dict):
    for k, v in d.items():
        t = type(v).__name__
        s = v if not isinstance(v, (dict, list)) else f"{t}({len(v)})"
        print(f"KEY {k!r}: {str(s)[:200]}")
