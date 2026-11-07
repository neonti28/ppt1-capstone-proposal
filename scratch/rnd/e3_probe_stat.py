#!/usr/bin/env python3
import json
r = json.load(open("/mnt/d/Capstone 1(v2)/scratch/v9_e_stat/v9_e_stat_01_hyd_ki_RESULTS.json"))
print("summary:", json.dumps(r["summary"], indent=1)[:1500])
print("split:", json.dumps(r["split"])[:400])
f0 = r["folds"][0]
print("fold0 keys:", list(f0.keys()))
print(json.dumps(f0, indent=1)[:3000])
