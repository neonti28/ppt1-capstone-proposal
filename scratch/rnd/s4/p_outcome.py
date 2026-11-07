"""Printer outcome/component dari labels_duration.json."""
import json, os
ROOT = "/mnt/d/Capstone 1(v2)"
d = json.load(open(os.path.join(ROOT, "scratch/rnd/s4/labels_duration.json"), encoding="utf-8"))
print("== per_outcome (semua)")
for k, v in d["per_outcome"].items():
    print(f"   {k} | n={v['n']} | jam={v['sum_jam']}")
print("== per_component (semua)")
for k, v in d["per_component"].items():
    print(f"   {k} | n={v['n']} | jam={v['sum_jam']}")
print("== per_category (semua)")
for k, v in d["per_category"].items():
    print(f"   {k} | n={v['n']} | jam={v['sum_jam']} | median={v['median_jam']}")
