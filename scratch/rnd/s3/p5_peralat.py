#!/usr/bin/env python3
"""Struktur per_alat pada head op_far_calibrated."""
import json

BASE = "/mnt/d/Capstone 1(v2)"
with open(f"{BASE}/scratch/v9_i1/v9_i1_RESULTS.json") as f:
    v9 = json.load(f)
tw = {e["engine"]: e for e in v9["engines"]}["tool_wear"]
for head in tw["heads"]:
    print("HEAD", head.get("head"), "keys:", list(head.keys()))
    pa = head.get("per_alat")
    if isinstance(pa, list) and pa:
        print("  per_alat[0] keys:", list(pa[0].keys()))
        print("  per_alat[0]:", json.dumps(pa[0], default=str)[:400])
    print()
