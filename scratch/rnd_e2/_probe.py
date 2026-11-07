import json,sys
p="scratch/v9_i1/v9_i1_RESULTS.json"
d=json.load(open(p))
print("TOP", list(d.keys()))
for k,v in d.items():
    print(k, type(v).__name__, len(v) if hasattr(v,"__len__") else "")
