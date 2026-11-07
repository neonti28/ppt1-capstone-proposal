#!/usr/bin/env python3
"""Cari blok baseline bengkel (tool_wear) di v9_i1_RESULTS.json."""
import json

BASE = "/mnt/d/Capstone 1(v2)"
with open(f"{BASE}/scratch/v9_i1/v9_i1_RESULTS.json") as f:
    r = json.load(f)

e = r["engines"]
print("engines type", type(e).__name__)
if isinstance(e, dict):
    for k, v in e.items():
        print("engine", k, "keys:", list(v.keys())[:15] if isinstance(v, dict) else type(v).__name__)
    if "tool_wear" in e:
        tw = e["tool_wear"]
        print("\n--- tool_wear ---")
        for k, v in tw.items():
            if isinstance(v, dict):
                print(" ", k, "->", list(v.keys())[:10])
            elif isinstance(v, list):
                print(" ", k, "-> list", len(v), v[:2])
            else:
                print(" ", k, "=", v)
elif isinstance(e, list):
    print("n", len(e))
    for it in e:
        print(" ", it.get("engine") or it.get("nama"), list(it.keys())[:12])
