import json
p='/mnt/d/Capstone 1(v2)/scratch/v9_i1/v9_i1_RESULTS.json'
d=json.load(open(p))
e=d['engines']
print(type(e), list(e.keys())[:20] if isinstance(e,dict) else len(e))
if isinstance(e,dict):
    for k,v in e.items():
        print(f"\n== engine {k}: {type(v).__name__} keys={list(v.keys())[:15] if isinstance(v,dict) else ''}")
