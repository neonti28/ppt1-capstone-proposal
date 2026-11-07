#!/usr/bin/env python3
"""S5 probe: baris ledger yang tidak cocok, dengan teks rujukan apa adanya."""
import json

BASE = "/mnt/d/Capstone 1(v2)"
d = json.load(open(f"{BASE}/scratch/rnd/s5/s5_ledger.json"))
for k in ("S1", "S3", "S4"):
    print(f"\n===== {k} =====")
    for b in d["per_kartu"][k]["baris"]:
        if b["hasil"] in ("COCOK",):
            continue
        print(f"{b['id']} | angka={b['angka']!r} | hasil={b['hasil']} | path={b['path']} | ruj={b['rujukan'][:150]}")
