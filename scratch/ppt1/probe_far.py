"""Bukti rinci: FAR per fold vib, tier 27 head, dan segmen tiap engine."""
import json
import os

BASE = "/mnt/d/Capstone 1(v2)"
vib = json.load(open(os.path.join(BASE, "scratch/v9_e_ml/v9_e_ML_vib_RESULTS.json")))
print("== vib keys:", list(vib.keys()))
for k, v in vib.items():
    if k in ("folds", "per_fold", "results", "by_fold", "eval"):
        print(k, "->", json.dumps(v, ensure_ascii=False)[:2500])

# cari semua angka FAR di struktur
def find(o, key_pat="far", path=""):
    hits = []
    if isinstance(o, dict):
        for k, v in o.items():
            hits += find(v, key_pat, path + "/" + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            hits += find(v, key_pat, path + f"[{i}]")
    else:
        if any(p in path.lower() for p in key_pat.split("|")):
            hits.append((path, o))
    return hits


print("\n== semua node path mengandung 'far' ==")
for p, v in find(vib, "far|tau|threshold")[:80]:
    print(p, "=", v)

i1 = json.load(open(os.path.join(BASE, "scratch/v9_i1/v9_i1_RESULTS.json")))
print("\n== engines (ringkas) ==")
for e in i1["engines"]:
    print(json.dumps(e, ensure_ascii=False)[:600])
    print("-" * 40)

print("\n== decision_layer ==")
print(json.dumps(i1["decision_layer"], ensure_ascii=False)[:3000])
