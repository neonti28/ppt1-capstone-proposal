import json, sys
p = sys.argv[1]
d = json.load(open(p))
print(p, "elapsed", d.get("elapsed_s"))
for k, v in d["ringkas"].items():
    print(k, json.dumps(v, ensure_ascii=False))
