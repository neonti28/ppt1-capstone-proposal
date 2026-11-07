import json
p = "/mnt/d/Capstone 1(v2)/scratch/rnd/s1/s1_hyd_seeds.json"
d = json.load(open(p))
print("STATUS:", d.get("status"))
print("SEEDS:", d.get("seed_list"))
print("MODEL:", d.get("model"))
print("n_fold_berbeda_maks:", d.get("n_fold_berbeda_maks"))
print()
print("=== REPRODUKSI ===")
r = d["reproduksi"]
print("semua_lulus:", r["semua_lulus"])
print("terbit:", r["terbit_r8"])
print("aktual:", r["aktual"])
print("delta:", r["delta"])
print("lulus:", r["lulus"])
print()
print("per_fold reproduksi:")
for f in r["per_fold"]:
    print(" ", f)
print()
print("=== LINTAS SEED ===")
for m, v in d["lintas_seed"].items():
    print(f"{m}: median={v['median']} min={v['min']} maks={v['maks']} rentang={v['rentang']}")
    print("   per_seed:", v["per_seed"])
print()
print("=== KONTROL ===")
k = d.get("kontrol_stokastik")
if k:
    print("model:", k["model"], "n_fitur:", k["n_fitur"])
    print("sebaran:", k["sebaran"])
    for s, v in k["per_seed"].items():
        rr = v["ringkas"]
        print(f"  seed {s}: FP {rr['fp_total']} presisi {rr['precision_median']} recall {rr['recall_median']}")
else:
    print("TIDAK ADA KONTROL")
print()
print("=== DELTA FOLD ===")
for s, v in d["delta_fold_terhadap_seed_pertama"].items():
    print(s, v)
