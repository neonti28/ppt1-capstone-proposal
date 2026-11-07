#!/usr/bin/env python3
import json
BASE = "/mnt/d/Capstone 1(v2)/scratch"
with open(f"{BASE}/v9_i1/v9_i1_RESULTS.json") as f:
    i1 = json.load(f)
print("keys:", list(i1.keys()))
heads = []
for eng in i1["engines"]:
    for h in eng["heads"]:
        heads.append((eng["engine"], h["head"], h.get("klaim"), h["tier"], h["layer"], h.get("human_review_required")))
print("n heads:", len(heads))
from collections import Counter
print("by layer:", Counter(h[4] for h in heads))
print("by tier:", Counter(h[3] for h in heads))
print()
for h in heads:
    print(f"  {h[0]:10s} {h[1]:28s} {str(h[2]):8s} {h[3]:24s} {h[4]}  hr={h[5]}")
# decision layer block
for k in i1:
    if k not in ("engines",):
        print("\n", k, "=", json.dumps(i1[k])[:600])
