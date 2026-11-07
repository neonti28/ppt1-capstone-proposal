import json, pathlib
B = pathlib.Path("/mnt/d/Capstone 1(v2)/scratch/rnd")
d = json.loads((B / "s2/s2_ringkas.json").read_text(encoding="utf-8"))
print("top:", list(d.keys()))
for k in ("vib", "ssi"):
    print("==", k, "keys:", list(d[k].keys()))
    if "agregat" in d[k]:
        print("  agregat:", json.dumps(d[k]["agregat"], ensure_ascii=False)[:1200])
    s = d[k].get("sensitivitas", {})
    print("  sensitivitas keys:", list(s.keys()))
    for kk, vv in s.items():
        print("   ", kk, json.dumps(vv, ensure_ascii=False)[:400])
