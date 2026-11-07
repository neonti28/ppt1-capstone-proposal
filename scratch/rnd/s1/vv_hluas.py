import json
d=json.load(open("scratch/rnd/s1/s1_hluas.json"))
print("KEYS:", list(d.keys()))
for k in list(d.keys())[:6]:
    v=d[k]; print(" ",k,type(v).__name__, len(v) if hasattr(v,"__len__") else v)
