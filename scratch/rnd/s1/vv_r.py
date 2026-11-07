import json
d = json.load(open("scratch/rnd/s1/s1_hyd_seeds.json"))
print("STATUS:", d["status"], "| seed_list:", d["seed_list"], "| model:", d["model"])
print("KONSTANTA:", json.dumps(d["konstanta"], indent=1)[:1200])
print("\n=== REPRODUKSI ===")
print(json.dumps(d["reproduksi"], indent=1)[:2500])
print("\n=== LINTAS_SEED ===")
print(json.dumps(d["lintas_seed"], indent=1)[:3000])
