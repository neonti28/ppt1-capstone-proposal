import json, os

BASE = "/mnt/d/Capstone 1(v2)"
d = json.load(open(os.path.join(BASE, "scratch/v9_i1/v9_i1_RESULTS.json")))
for e in d["engines"]:
    print("=" * 72)
    print("ENGINE:", e["engine"], "|", e["jenis_tugas"])
    heads = e["heads"]
    if isinstance(heads, dict):
        heads = [dict(name=k, **v) for k, v in heads.items()]
    for h in heads:
        if not isinstance(h, dict):
            print("  HEAD(raw):", str(h)[:200])
            continue
        name = h.get("head") or h.get("nama") or h.get("name")
        print(f"  HEAD {name}: tier={h.get('tier')} layer={h.get('layer')}")
        for k, v in h.items():
            if k in ("head", "nama", "name"):
                continue
            if isinstance(v, (int, float, str)):
                print(f"     {k} = {str(v)[:160]}")
            elif isinstance(v, list):
                print(f"     {k} = list({len(v)}) {str(v)[:160]}")
            elif isinstance(v, dict):
                print(f"     {k} = dict({len(v)}) {list(v.keys())[:10]}")
