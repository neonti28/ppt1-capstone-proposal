import json
B = "/mnt/d/Capstone 1(v2)"
d = json.load(open(f"{B}/scratch/v9_i1/v9_i1_RESULTS.json"))
print("nama engine:", [e["engine"] for e in d["engines"]])
for e in d["engines"]:
    if "hyd" in e["engine"].lower():
        print(json.dumps(e, indent=1)[:3000])
