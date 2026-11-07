import json
d=json.load(open("scratch/v9_i1/v9_i1_RESULTS.json"))
print("META:", json.dumps(d["meta"], indent=1)[:900])
print("SEGMEN:", json.dumps(d["segmen_info"], indent=1)[:1200])
e=d["engines"][0]
print("ENGINE0 keys:", list(e.keys()))
print(json.dumps(e, indent=1)[:1800])
for e in d["engines"]:
    print("---", e.get("engine"), e.get("klaim"), "heads:", list(e.get("heads",{}).keys()) if isinstance(e.get("heads"),dict) else type(e.get("heads")))
