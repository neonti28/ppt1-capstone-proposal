import json, os
base = "/mnt/d/Capstone 1(v2)/scratch/rnd/e4"
print("FILES")
for f in sorted(os.listdir(base)):
    p = os.path.join(base, f)
    print("  ", f, os.path.getsize(p))
print("=" * 70)
d = json.load(open(os.path.join(base, "e4_summary.json")))

def walk(o, p="", depth=0):
    if depth > 3:
        print(p, "<deep>")
        return
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, (dict, list)):
                walk(v, p + "/" + str(k), depth + 1)
            else:
                print(f"{p}/{k} = {v}")
    elif isinstance(o, list):
        for i, v in enumerate(o[:4]):
            if isinstance(v, (dict, list)):
                walk(v, p + f"[{i}]", depth + 1)
            else:
                print(f"{p}[{i}] = {v}")
        if len(o) > 4:
            print(f"{p} ... total {len(o)}")

walk(d)
