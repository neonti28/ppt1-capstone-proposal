import json
d=json.load(open("scratch/v9_i1/v9_i1_RESULTS.json"))
for i,e in enumerate(d["engines"]):
    print(f"--- engine[{i}] keys={list(e.keys())}")
    for k,v in e.items():
        if k in ("nama","name","id","segmen","segment","hyd","dataset"): print("   ",k,"=",v)
    # cari blok hasil
    for key in e:
        v=e[key]
        if isinstance(v,dict) and any(("fp" in str(kk).lower() or "recall" in str(kk).lower()) for kk in v.keys()):
            print("   BLOK:",key, json.dumps(v)[:400])
