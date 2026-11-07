#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cari blok JSON run-1 vs run-2 yang berbeda (di luar field volatil)."""
import json
import sys

VOL = {"generated_at_utc", "runtime_seconds"}
A = "/home/neonti/.hermes/cache/scratch/t2e_run1.json"
B = "/mnt/d/Capstone 1/docs/V2_ML_BEAT_CANARY_TS.json"


def strip(o):
    if isinstance(o, dict):
        return {k: strip(v) for k, v in o.items() if k not in VOL}
    if isinstance(o, list):
        return [strip(v) for v in o]
    return o


a = strip(json.load(open(A)))
b = strip(json.load(open(B)))
diffs = []


def walk(x, y, path=""):
    if type(x) is not type(y):
        diffs.append(f"TYPE {path}: {type(x).__name__} vs {type(y).__name__}")
        return
    if isinstance(x, dict):
        for k in sorted(set(x) | set(y), key=str):
            if k not in x:
                diffs.append(f"ONLY-B {path}/{k}")
            elif k not in y:
                diffs.append(f"ONLY-A {path}/{k}")
            else:
                walk(x[k], y[k], f"{path}/{k}")
    elif isinstance(x, list):
        if len(x) != len(y):
            diffs.append(f"LEN {path}: {len(x)} vs {len(y)}")
            return
        for i, (p, q) in enumerate(zip(x, y)):
            walk(p, q, f"{path}[{i}]")
    elif x != y:
        diffs.append(f"DIFF {path}: A={repr(x)[:160]} B={repr(y)[:160]}")


walk(a, b)
print(f"{len(diffs)} perbedaan (di luar {sorted(VOL)}):")
for d in diffs[:60]:
    print(" ", d)
sys.exit(1 if diffs else 0)
