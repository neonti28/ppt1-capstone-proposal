import json
d = json.load(open('/mnt/d/Capstone 1(v2)/scratch/v9_i1/v9_i1_RESULTS.json'))
print("top keys:", list(d.keys()))
for k, v in d.items():
    if isinstance(v, dict):
        print(f"\n== {k} keys:", list(v.keys())[:25])
