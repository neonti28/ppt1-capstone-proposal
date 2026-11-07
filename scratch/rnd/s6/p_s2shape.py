import json

BASE = "/mnt/d/Capstone 1(v2)"
d = json.load(open(f"{BASE}/scratch/rnd/s2/s2_records_vib.json"))
f = d["folds"][0]
print("fold keys:", list(f.keys()))
for k, v in f.items():
    if isinstance(v, dict):
        print(f"  {k}: dict keys={list(v.keys())[:14]}")
        for k2, v2 in list(v.items())[:3]:
            print(f"     {k2}: {type(v2).__name__} {str(v2)[:200]}")
    elif isinstance(v, list):
        print(f"  {k}: list({len(v)}) {str(v)[:200]}")
    else:
        print(f"  {k}: {v}")
