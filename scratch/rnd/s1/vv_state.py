import json
d = json.load(open("scratch/rnd/s1/s1_hyd_seeds.json"))
print("TYPE:", type(d).__name__)
if isinstance(d, dict):
    print("TOP KEYS:", list(d.keys()))
    for k in d:
        v = d[k]
        print(" ", k, type(v).__name__, len(v) if hasattr(v, "__len__") else v)
print("--- meta ---")
print(open("scratch/rnd/s1/s1_meta.json").read())
