import json, glob, os
B = "/mnt/d/Capstone 1(v2)"
p = f"{B}/scratch/v9_i1/v9_i1_RESULTS.json"
print("ada file:", os.path.exists(p), os.path.getsize(p) if os.path.exists(p) else 0)
d = json.load(open(p))
print("top keys:", list(d.keys()))


def walk(o, pref="", depth=0):
    if depth > 2:
        return
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, (dict, list)):
                n = len(v)
                print(f"{pref}{k}: {type(v).__name__}[{n}]")
                walk(v, pref + "  ", depth + 1)
            else:
                print(f"{pref}{k}: {v!r}")


walk(d)
print()
print("=== DOC V9 list ===")
for f in sorted(glob.glob(f"{B}/docs/V9_*")):
    print(os.path.basename(f), os.path.getsize(f))
