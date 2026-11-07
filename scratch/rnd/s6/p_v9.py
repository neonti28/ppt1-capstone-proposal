import json, os, sys

BASE = "/mnt/d/Capstone 1(v2)"
p = os.path.join(BASE, "scratch/v9_i1/v9_i1_RESULTS.json")
d = json.load(open(p))
print("TOP:", list(d.keys()))


def brief(o, name="root", depth=0, maxd=3):
    pad = "  " * depth
    if isinstance(o, dict):
        print(f"{pad}{name}: dict({len(o)}) keys={list(o.keys())[:14]}")
        if depth < maxd:
            for k, v in list(o.items())[:14]:
                brief(v, k, depth + 1, maxd)
    elif isinstance(o, list):
        print(f"{pad}{name}: list({len(o)}) first={type(o[0]).__name__ if o else None}")
        if o and depth < maxd:
            brief(o[0], name + "[0]", depth + 1, maxd)
    else:
        s = str(o)
        print(f"{pad}{name}: {type(o).__name__} {s[:120]}")


brief(d, maxd=2)
