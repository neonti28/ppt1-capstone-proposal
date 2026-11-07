import json

S = json.load(open("/mnt/d/Capstone 1(v2)/scratch/rnd/s3/s3c_ringkas.json"))
print("far_tak_terdefinisi:", json.dumps(S["far_tak_terdefinisi"], default=float))
print("meta:", json.dumps({k: S["meta"][k] for k in S["meta"] if k in
      ("CAKUPAN_MIN", "FAR_MAKS", "RECALL_MIN", "ALPHA_BUDGET", "H_GRID")}, default=float))
print("\nagregat keys:", list(S["agregat"]["H5_stat_dan_rule"].keys()))
print("\nfold-level (H5):")
for r in S["tabel"]:
    if r["model"] == "H5_stat_dan_rule":
        print(json.dumps(r, default=float))
print("\nfold-level (ml_fisik):")
for r in S["tabel"]:
    if r["model"] == "ml_fisik":
        print(json.dumps(r, default=float))
