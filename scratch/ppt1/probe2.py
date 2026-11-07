import json

base = "/mnt/d/Capstone 1(v2)"
d = json.load(open(base + "/scratch/v9_i1/v9_i1_RESULTS.json", encoding="utf-8"))

def walk(o, path="", depth=0):
    if depth > 3:
        return
    if isinstance(o, dict):
        for k, v in o.items():
            p = path + "/" + str(k)
            if isinstance(v, (dict, list)):
                print(p, type(v).__name__, len(v))
                walk(v, p, depth + 1)
            else:
                s = str(v)
                print(p, "=", s[:120])

walk(d)
