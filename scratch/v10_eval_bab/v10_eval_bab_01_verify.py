#!/usr/bin/env python3
# V10 EVAL BAB — re-verify headline numbers from primary JSONs (read-only)
import json, os, glob

BASE = "/mnt/d/Capstone 1(v2)/scratch"

def load(p):
    with open(p) as f:
        return json.load(f)

def walk(o, path=""):
    """yield (path, value) for scalar leaves"""
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, f"{path}[{i}]")
    else:
        yield path, o

print("=== EVAL_C RESULTS meta/defs present ===")
ec = load(f"{BASE}/v9_eval_c/v9_eval_c_RESULTS.json")
print("top keys:", list(ec.keys()))

# vib FAR dispersion at tau 0.5
print("\n=== vib FAR tau0.5 (EVAL_C) ===")
for p, v in walk(ec):
    if "vib" in p and ("far" in p.lower()) and ("0.5" in p or "0_5" in p):
        print(p, "=", v)

# search FAR 496 / 4.1
print("\n=== grep 496 / 4.15 in EVAL_C ===")
for p, v in walk(ec):
    if isinstance(v, (int, float)) and (abs(v-496.092)<1 or abs(v-4.15)<0.2 or abs(v-4.155)<0.2):
        print(p, "=", v)

print("\n=== hyd_ki hybrid FP 2091->927 ===")
for p, v in walk(ec):
    if "hyd" in p.lower() and isinstance(v, (int,float)) and v in (2091, 927):
        print(p, "=", v)

print("\n=== shk rule FAR 0.67-6.6 / 7/9 ===")
for p, v in walk(ec):
    if "shk" in p.lower() and isinstance(v, (int,float)) and (abs(v-6.6)<0.1 or abs(v-0.67)<0.05):
        print(p, "=", v)

print("\n=== ssi hybrid FP 26->7 ===")
for p, v in walk(ec):
    if "ssi" in p.lower() and isinstance(v,(int,float)) and v in (26,7):
        print(p, "=", v)

print("\n=== anchor gap 13/281 ===")
for p, v in walk(ec):
    if "anchor" in p.lower() or "absorb" in p.lower():
        print(p, "=", v)
