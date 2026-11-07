import json

D = "/mnt/d/Capstone 1(v2)/scratch/rnd/s3"
h = json.load(open(f"{D}/s3b_hybrid.json"))
print("top keys:", list(h.keys()))
for k in h:
    v = h[k]
    print(k, type(v).__name__, len(v) if hasattr(v, "__len__") else "")
r = h.get("records")
if isinstance(r, list) and r:
    print("\nrecord[0]:", json.dumps(r[0], indent=1, default=float)[:1200])
elif isinstance(r, dict):
    k0 = list(r)[0]
    print("\nrecords key", k0, json.dumps(r[k0], indent=1, default=float)[:1200])
