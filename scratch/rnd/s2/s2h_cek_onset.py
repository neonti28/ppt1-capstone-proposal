import json

r = json.load(open("/mnt/d/Capstone 1(v2)/scratch/rnd/s2/s2_ringkas.json"))
for k in ("vib", "ssi"):
    v = {m: g["n_onset"] for m, g in r[k]["agregat"].items()}
    print(k, "n_onset unik:", sorted(set(v.values())), "model:", len(v))
    print("   n_diperingatkan:", {m: g["n_diperingatkan"] for m, g in r[k]["agregat"].items()})
