import json

BASE = "/mnt/d/Capstone 1(v2)"
d = json.load(open(f"{BASE}/scratch/rnd/s1/s1_hyd_seeds.json"))
print("konstanta:", json.dumps(d["konstanta"], indent=1))
print("reproduksi:", json.dumps(d["reproduksi"], indent=1)[:1500])
print("log:", json.dumps(d["log"], indent=1)[:2500])
