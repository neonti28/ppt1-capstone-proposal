#!/usr/bin/env python3
# t_de420dbc V10-EVAL Bab 7 — independent re-verify of headline numbers from primary JSONs.
import json
from collections import Counter

BASE = "/mnt/d/Capstone 1(v2)/scratch"

def load(p):
    with open(p) as f:
        return json.load(f)

def walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, f"{path}[{i}]")
    else:
        yield path, o

print("=== I1 registry ===")
i1 = load(f"{BASE}/v9_i1/v9_i1_RESULTS.json")
print("I1 top keys:", list(i1.keys()))
heads = []
for eng in i1["engines"]:
    for h in eng["heads"]:
        heads.append((eng["engine"], h["head"], h.get("klaim"), h["tier"], h["layer"],
                      h.get("human_review_required")))
print("n heads:", len(heads))
print("by layer:", dict(Counter(h[4] for h in heads)))
print("by tier:", dict(Counter(h[3] for h in heads)))
print("engines:", [e["engine"] for e in i1["engines"]])
for h in heads:
    print(f"  {h[0]:10s} {h[1]:28s} {str(h[2]):8s} {h[3]:24s} {h[4]} hr={h[5]}")
for k in i1:
    if k != "engines":
        print(k, "=", json.dumps(i1[k])[:500])

print("\n=== EVAL_C top keys ===")
ec = load(f"{BASE}/v9_eval_c/v9_eval_c_RESULTS.json")
print("top keys:", list(ec.keys()))

print("\n=== EVAL_C: any FAR 496 / 4.15 ===")
for p, v in walk(ec):
    if isinstance(v, (int, float)) and (abs(v - 496.092) < 1 or abs(v - 4.15) < 0.2):
        print(p, "=", v)

print("\n=== EVAL_C: hyd 2091 / 927 ===")
for p, v in walk(ec):
    if "hyd" in p.lower() and isinstance(v, (int, float)) and v in (2091, 927):
        print(p, "=", v)

print("\n=== EVAL_C: ssi 26 / 7 hybrid ===")
for p, v in walk(ec):
    if "ssi" in p.lower() and isinstance(v, (int, float)) and v in (26, 7):
        print(p, "=", v)

print("\n=== EVAL_C: shk FAR 0.67 / 6.6 ===")
for p, v in walk(ec):
    if "shk" in p.lower() and isinstance(v, (int, float)) and (abs(v - 6.6) < 0.1 or abs(v - 0.67) < 0.05):
        print(p, "=", v)

print("\n=== EVAL_C: anchor / absorb ===")
for p, v in walk(ec):
    if "anchor" in p.lower() or "absorb" in p.lower():
        print(p, "=", v)
