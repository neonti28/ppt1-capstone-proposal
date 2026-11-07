import json
B = "/mnt/d/Capstone 1(v2)"
r8 = json.load(open(f"{B}/scratch/rnd/r8/r8_hyd.json"))
print("=== r8_hyd.json top keys ===", list(r8.keys()))
print("=== ringkas H1 (terbit) ===")
print(json.dumps(r8["ringkas"]["H1_stat_dan_rule"], indent=1))
print("=== REPRODUKSI per_fold (s1) ===")
d = json.load(open(f"{B}/scratch/rnd/s1/s1_hyd_seeds.json"))
for row in d["reproduksi"]["per_fold"]:
    print(json.dumps(row))
print("=== r8 sha256 file ===")
import hashlib
print(hashlib.sha256(open(f"{B}/scratch/rnd/r8/r8_hyd.json","rb").read()).hexdigest())
