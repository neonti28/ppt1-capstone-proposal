import json
base = "/mnt/d/Capstone 1(v2)"
d = json.load(open(base + "/scratch/v9_i1/v9_i1_RESULTS.json", encoding="utf-8"))
for i, e in enumerate(d["engines"]):
    print("=== engine", i, type(e).__name__)
    if isinstance(e, dict):
        for k, v in e.items():
            if isinstance(v, list):
                print("  ", k, "list[%d]" % len(v))
                if v and isinstance(v[0], dict):
                    print("     item0 keys:", list(v[0].keys()))
            elif isinstance(v, dict):
                print("  ", k, "dict keys:", list(v.keys())[:12])
            else:
                print("  ", k, "=", str(v)[:120])
