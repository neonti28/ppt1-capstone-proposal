#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cek apakah run-1 sudah memakai fix P7 (predict_n_jobs=1) dan penanda patch lain."""
import json

A = "/home/neonti/.hermes/cache/scratch/t2e_run1.json"
B = "/mnt/d/Capstone 1/docs/V2_ML_BEAT_CANARY_TS.json"


def find(obj, needle, path="$"):
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if needle in str(k):
                out.append(f"{path}.{k} = {json.dumps(v)[:200]}")
            out += find(v, needle, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj[:50]):
            out += find(v, needle, f"{path}[{i}]")
    return out


for tag, p in (("RUN1", A), ("RUN2", B)):
    j = json.load(open(p))
    print(f"[{tag}] predict_n_jobs hits:")
    for h in find(j, "predict_n_jobs")[:6]:
        print("   ", h)
    print(f"[{tag}] 'rfm.n_jobs' hits:")
    for h in find(j, "rfm.n_jobs")[:4]:
        print("   ", h)
    p4 = j.get("p4_desain_baru", {})
    print(f"[{tag}] design={json.dumps(p4.get('design'))[:300]}")
    print(f"[{tag}] sensitivity n_eval: {json.dumps(p4.get('sensitivity'))[:400]}")
    print()
