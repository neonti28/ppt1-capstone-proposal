import json
p='/mnt/d/Capstone 1(v2)/scratch/v9_i1/v9_i1_RESULTS.json'
d=json.load(open(p))
for i,e in enumerate(d['engines']):
    print(i, list(e.keys()))
    print("   nama:", e.get('nama') or e.get('engine') or e.get('name'))
