import json
base = "/mnt/d/Capstone 1(v2)/scratch/rnd/e4"
for f in ("e4_a1.json", "e4_baseline.json", "e4_hybrid.json", "e4_a2.json"):
    d = json.load(open(f"{base}/{f}"))
    print("==", f, "top keys:", list(d.keys())[:8])
    k0 = list(d.keys())[0]
    v = d[k0]
    if isinstance(v, list) and v:
        print("   list len", len(v), "item keys:", sorted(v[0].keys()))
    elif isinstance(v, dict):
        print("   dict keys:", sorted(v.keys())[:12])
