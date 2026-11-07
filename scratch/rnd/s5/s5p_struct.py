#!/usr/bin/env python3
"""S5 probe struktur artefak S1."""
import json

BASE = "/mnt/d/Capstone 1(v2)"
d = json.load(open(f"{BASE}/scratch/rnd/s1/s1_hyd_seeds.json"))
print("top keys:", list(d.keys()))
print("status:", d["status"], "seed_list:", d["seed_list"])
ps = d["per_seed"]["42"]
print("per_seed keys:", list(ps.keys()))
print("ringkas keys:", list(ps["ringkas"].keys()))
print("ringkas 42:", json.dumps({k: v for k, v in ps["ringkas"].items() if not isinstance(v, list) and not isinstance(v, dict)}, indent=1))
f0 = ps["folds"][0]
print("fold keys:", list(f0.keys()))
print("fold f0:", json.dumps(f0, indent=1, default=str)[:2500])
print("lintas keys:", list(d["lintas_seed"].keys()))
print("sidik keys:", list(ps["sidik"].keys()))
print("n folds seed42:", len(ps["folds"]), "seed13:", len(d["per_seed"]["13"]["folds"]))
print("kontrol keys:", list((d.get("kontrol_stokastik") or {}).keys()))
