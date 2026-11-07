#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inspeksi run-1 baseline: runtime, generated_at, blok yang ada."""
import json

A = "/home/neonti/.hermes/cache/scratch/t2e_run1.json"
B = "/mnt/d/Capstone 1/docs/V2_ML_BEAT_CANARY_TS.json"
for tag, p in (("RUN1", A), ("RUN2", B)):
    a = json.load(open(p))
    p4 = a.get("p4_desain_baru", {})
    print(f"[{tag}] generated={a.get('generated_at_utc')} "
          f"runtime_p4={a.get('runtime_seconds_p4')}")
    print(f"[{tag}] p4 keys={list(p4.keys())}")
    print(f"[{tag}] pooled_scores_extra present={'pooled_scores_extra' in p4}")
    extra = p4.get("pooled_scores_extra")
    if isinstance(extra, dict):
        print(f"[{tag}] pooled_scores_extra keys={list(extra.keys())[:6]}")
