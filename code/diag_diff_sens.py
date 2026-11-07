#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Diff blok sensitivity run-1 (pra-fix flag S2) vs run-5 (final)."""
import json

A = json.load(open("/home/neonti/.hermes/cache/scratch/t2e_run1.json"))
B = json.load(open("/mnt/d/Capstone 1/docs/V2_ML_BEAT_CANARY_TS.json"))
a = A["p4_desain_baru"]["sensitivity"]
b = B["p4_desain_baru"]["sensitivity"]


def walk(x, y, path=""):
    out = []
    if isinstance(x, dict) and isinstance(y, dict):
        for k in sorted(set(x) | set(y), key=str):
            if k not in x:
                out.append(f"ONLY-B {path}/{k}")
            elif k not in y:
                out.append(f"ONLY-A {path}/{k}")
            else:
                out += walk(x[k], y[k], f"{path}/{k}")
    elif isinstance(x, list) and isinstance(y, list):
        if len(x) != len(y):
            out.append(f"LEN {path}")
        else:
            for i, (p, q) in enumerate(zip(x, y)):
                out += walk(p, q, f"{path}[{i}]")
    elif x != y:
        out.append(f"DIFF {path}: A={json.dumps(x)[:90]} B={json.dumps(y)[:90]}")
    return out


d = walk(a, b)
print(f"{len(d)} perbedaan blok sensitivity run1 vs run5:")
for x in d[:40]:
    print(" ", x)
