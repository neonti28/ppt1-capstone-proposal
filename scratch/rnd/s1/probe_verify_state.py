import json, os
B = "/mnt/d/Capstone 1(v2)"
p = f"{B}/scratch/rnd/s1/s1_hyd_seeds.json"
m = f"{B}/scratch/rnd/s1/s1_meta.json"
print("=== META ===")
print(open(m).read())
d = json.load(open(p))
print("=== TOP KEYS ===", list(d.keys()))
print("status:", d.get("status"), "seed_list:", d.get("seed_list"), "tanggal:", d.get("tanggal"))
print("=== REPRODUKSI ===")
r = d.get("reproduksi", {})
for k in ("terbit_r8", "aktual", "delta", "lulus", "semua_lulus"):
    print(k, "=", json.dumps(r.get(k)))
print("=== PER SEED RINGKAS ===")
for s in d.get("per_seed", {}):
    print(s, json.dumps(d["per_seed"][s]["ringkas"]))
print("=== LINTAS ===")
for k, v in d.get("lintas_seed", {}).items():
    print(k, {kk: vv for kk, vv in v.items() if kk != "per_seed"})
print("n_fold_berbeda_maks:", d.get("n_fold_berbeda_maks"))
print("=== KONTROL ===")
kk = d.get("kontrol_stokastik")
print("ada kontrol:", kk is not None)
if kk:
    print("sebaran:", json.dumps(kk.get("sebaran")))
    for s in kk["per_seed"]:
        print(" kontrol seed", s, json.dumps(kk["per_seed"][s]["ringkas"]))
print("=== LOG ===")
for line in d.get("log", []):
    print(line)
