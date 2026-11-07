#!/usr/bin/env python3
"""Dump QC metadata per parsed well + extraction log status."""
import json, os, glob

BASE = "/mnt/d/Capstone 1"
OUT = os.path.join(BASE, "data/volve/witsml_parsed")

print("=== extraction log ===")
for cand in ["/home/neonti/.hermes/cache/scratch/witsml_extract.log",
             "/home/neonti/.hermes/cache/scratch/witsml_extract_stdout.log"]:
    if os.path.exists(cand):
        print(" --", cand)
        print(open(cand, errors="replace").read())

print("=== per-well qc.json ===")
rows = []
for f in sorted(glob.glob(os.path.join(OUT, "*.qc.json"))):
    d = json.load(open(f))
    rows.append((os.path.basename(f), d))
    print(f"\n## {os.path.basename(f)}")
    for k in sorted(d.keys()):
        v = d[k]
        if k in ("fill_rate", "channel_fill_rate", "columns", "fillrate"):
            if isinstance(v, dict):
                print(f"   {k}: <dict n={len(v)}>")
            else:
                print(f"   {k}: {str(v)[:120]}")
        else:
            print(f"   {k}: {str(v)[:300]}")
