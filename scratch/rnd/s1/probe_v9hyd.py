import json
p = "/mnt/d/Capstone 1(v2)/scratch/v9_i1/v9_i1_RESULTS.json"
d = json.load(open(p))
print("TOP:", list(d.keys()))
for k, v in d.items():
    if isinstance(v, dict):
        print(f"  {k}: dict keys={list(v.keys())[:12]}")
    elif isinstance(v, list):
        print(f"  {k}: list len={len(v)}")
    else:
        print(f"  {k}: {v!r}")
print()
# cari semua kunci yang mengandung hyd
def walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if "hyd" in str(k).lower():
                print("KEY HYD:", path + "/" + str(k), "->", type(v).__name__)
            walk(v, path + "/" + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o[:3]):
            walk(v, path + f"[{i}]")
walk(d)
print()
print("=== segmen_info hyd ===")
si = d.get("segmen_info", {})
if "hyd" in si:
    print(json.dumps(si["hyd"], indent=1))
print()
print("=== semua top-level sections yg punya hyd ===")
for k, v in d.items():
    s = json.dumps(v)[:200]
    if "hyd" in json.dumps(v).lower():
        print(f"--- {k} ---")
        print(s)
