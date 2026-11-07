#!/usr/bin/env python3
"""Bongkar heads tool_wear (baseline bengkel) dan bit_wear (konteks V9)."""
import json

BASE = "/mnt/d/Capstone 1(v2)"
with open(f"{BASE}/scratch/v9_i1/v9_i1_RESULTS.json") as f:
    r = json.load(f)
by = {e["engine"]: e for e in r["engines"]}


def walk(obj, path="", depth=0):
    pad = "  " * depth
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, (dict, list)) and depth < 3:
                print(f"{pad}{k}: {type(v).__name__} n={len(v)}")
                walk(v, path + "/" + str(k), depth + 1)
            else:
                s = str(v)
                print(f"{pad}{k} = {s[:160]}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj[:4]):
            print(f"{pad}[{i}]")
            walk(v, path, depth + 1)
        if len(obj) > 4:
            print(f"{pad}... ({len(obj)} item)")


for name in ("tool_wear", "bit_wear"):
    print("=" * 30, name)
    walk(by[name])
