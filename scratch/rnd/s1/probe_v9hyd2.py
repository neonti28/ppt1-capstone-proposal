import json
p = "/mnt/d/Capstone 1(v2)/scratch/v9_i1/v9_i1_RESULTS.json"
d = json.load(open(p))
print("=== segmen_info hyd_ki ===")
print(json.dumps(d["segmen_info"]["hyd_ki"], indent=1, ensure_ascii=False))
print()
for e in d["engines"]:
    if "hyd" in str(e.get("engine", "")).lower():
        print("=== ENGINE hyd_ki ===")
        print(json.dumps(e, indent=1, ensure_ascii=False))
print()
print("=== decision_layer L0/L1 hyd ===")
dl = d["decision_layer"]
for lname, arr in dl.get("layers", {}).items():
    for it in arr:
        if "hyd" in str(it.get("engine", "")).lower():
            print(lname, json.dumps(it, indent=1, ensure_ascii=False))
print()
print("=== ringkasan ===")
print(json.dumps(dl.get("ringkasan"), indent=1, ensure_ascii=False)[:2000])
