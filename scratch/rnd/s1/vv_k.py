import json
d = json.load(open("scratch/rnd/s1/s1_hyd_seeds.json"))
print("=== KONTROL_STOKASTIK ===")
print(json.dumps(d["kontrol_stokastik"], indent=1))
print("\n=== DELTA FOLD vs SEED PERTAMA ===")
print(json.dumps(d["delta_fold_terhadap_seed_pertama"], indent=1)[:800])
print("\n=== LOG ===")
for l in d["log"]:
    print(" ", l)
