#!/usr/bin/env python3
"""Probe struktur artefak bengkel dan ringkasan s3a."""
import json

BASE = "/mnt/d/Capstone 1(v2)"

with open(f"{BASE}/scratch/v9_i1/v9_i1_RESULTS.json") as f:
    r = json.load(f)
print("top keys", list(r.keys())[:20])
if "tool_wear" in r:
    tw = r["tool_wear"]
    print("tool_wear keys", list(tw.keys()))
    for k, v in tw.items():
        if isinstance(v, dict):
            print(" ", k, "->", list(v.keys())[:8])
        elif isinstance(v, list):
            print(" ", k, "-> list", len(v), v[:1])
        else:
            print(" ", k, "=", v)

with open(f"{BASE}/scratch/rnd/s3/s3a_feasibility.json") as f:
    a = json.load(f)
print("\n--- grid kedalaman ---")
for g in a["grid_kedalaman"]:
    print(g)
print("\n--- label per well ---")
for g in a["label"]["per_well"]:
    print(g)
print("\n--- rekonstruksi per well ---")
for g in a["sirkularitas"]["per_well_ambang_sendiri"]:
    print(g)
