import json
d=json.load(open("scratch/rnd/s1/s1_hluas.json"))
print("sifat:", d["sifat"])
print("n_fold:", d["n_fold"], "n_lolos_anggaran:", d["n_lolos_anggaran"])
print("grid_lama:", d["grid_lama"])
print("grid_luas:", d["grid_luas"])
print("ringkas:", json.dumps(d["ringkas"], indent=1)[:900])
print("banding:", json.dumps(d["banding"], indent=1)[:600])
