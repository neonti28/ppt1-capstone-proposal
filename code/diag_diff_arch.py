#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cari key top-level arsip T2-d yg beda isi dgn JSON T2-e (V1c)."""
import json

RES = "/mnt/d/Capstone 1/docs/V2_ML_BEAT_CANARY_TS.json"
ARCH = "/mnt/d/Capstone 1/docs/V2_ML_BEAT_CANARY_TS_T2D_ARSIP.json"
res = json.load(open(RES))
arch = json.load(open(ARCH))
print("keys arsip:", sorted(arch.keys()))
print("keys res  :", sorted(res.keys()))
for k, v in arch.items():
    if k in ("generated_at_utc", "task"):
        print(f"SKIP {k}")
        continue
    if k not in res:
        print(f"MISSING di res: {k}")
    elif res[k] != v:
        print(f"DIFF {k}: tipe res={type(res[k]).__name__} arsip={type(v).__name__}")
        if isinstance(v, dict) and isinstance(res[k], dict):
            sub = [kk for kk in set(v) | set(res[k])
                   if v.get(kk) != res[k].get(kk)]
            print("   sub-diff:", sub[:20])
            for kk in sub[:5]:
                print(f"     {kk}: res={json.dumps(res[k].get(kk))[:150]}")
                print(f"     {kk}: arsip={json.dumps(v.get(kk))[:150]}")
        else:
            print("   res:", json.dumps(res[k])[:200])
            print("   arsip:", json.dumps(v)[:200])
    else:
        print(f"OK {k}")
