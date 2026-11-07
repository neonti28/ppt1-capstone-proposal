"""Printer nilai metrik lapisan B dari inventory.json (untuk kutipan dokumen)."""
import json, os
ROOT = "/mnt/d/Capstone 1(v2)"
d = json.load(open(os.path.join(ROOT, "scratch/rnd/s4/inventory.json"), encoding="utf-8"))
for k, v in d["metrik_lapisan_b"].items():
    print("==", k)
    for kk, vv in v.items():
        print("   ", kk, "=", vv)
