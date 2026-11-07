#!/usr/bin/env python3
"""Orient: state of WITSML parse outputs + scripts + pending VAR_F-15A."""
import json, os, glob, sys

BASE = "/mnt/d/Capstone 1"
OUT = os.path.join(BASE, "data/volve/witsml_parsed")

print("=== CSV/QC present ===")
for f in sorted(os.listdir(OUT)):
    print(" ", f, os.path.getsize(os.path.join(OUT, f)))

sp = os.path.join(OUT, "_parse_summary.json")
if os.path.exists(sp):
    d = json.load(open(sp))
    print("=== _parse_summary.json ===")
    print(" type:", type(d).__name__)
    if isinstance(d, dict):
        for k, v in d.items():
            if isinstance(v, dict):
                print(f"  {k}: dict keys={list(v.keys())[:12]}")
            else:
                print(f"  {k}: {str(v)[:200]}")
    elif isinstance(d, list):
        print(" n entries:", len(d))
        for e in d[:15]:
            if isinstance(e, dict):
                print("  ", {k: e.get(k) for k in list(e.keys())[:10]})
            else:
                print("  ", str(e)[:200])

print("=== witsml_raw wellbore dirs ===")
raw = os.path.join(BASE, "data/volve/witsml_raw")
if os.path.isdir(raw):
    names = sorted(os.listdir(raw))
    print(" n:", len(names))
    for n in names:
        print("  ", n)
else:
    print(" MISSING", raw)

print("=== extraction log tail ===")
for cand in [os.path.join(BASE, "scratch/witsml_extract.log"),
             os.path.join(BASE, "data/volve/witsml_raw/../../scratch/witsml_extract.log")]:
    if os.path.exists(cand):
        lines = open(cand, errors="replace").read().splitlines()
        print(" file:", cand, "lines:", len(lines))
        for l in lines[-15:]:
            print("   ", l)
        break
else:
    print(" extract log not found at expected paths")

print("=== other scratch dirs ===")
for d in glob.glob(os.path.join(BASE, "*scratch*")) + glob.glob(os.path.join(BASE, ".*scratch*")):
    print("  ", d)
