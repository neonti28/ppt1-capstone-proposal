#!/usr/bin/env python3
"""S5 probe: peta kunci ringkas artefak S3 dan S4 (dipotong ketat)."""
import json

BASE = "/mnt/d/Capstone 1(v2)"


def peta(o, pref="", depth=0, maks=2, baris=None):
    if baris is None:
        baris = []
    if depth > maks:
        return baris
    if isinstance(o, dict):
        for k, v in list(o.items())[:18]:
            if isinstance(v, dict):
                baris.append(f"{pref}{k}/ ({len(v)})")
                peta(v, pref + "  ", depth + 1, maks, baris)
            elif isinstance(v, list):
                contoh = type(v[0]).__name__ if v else "-"
                baris.append(f"{pref}{k}[{len(v)}] {contoh}")
                if v and isinstance(v[0], dict):
                    baris.append(f"{pref}  kunci[0]: {list(v[0])[:12]}")
            else:
                baris.append(f"{pref}{k} = {str(v)[:60]}")
    return baris


for path in ("scratch/rnd/s3/s3a_feasibility.json",
             "scratch/rnd/s3/s3c_ringkas.json",
             "scratch/rnd/s4/inventory.json",
             "scratch/rnd/s4/crosscheck.json",
             "scratch/rnd/s4/token_scan.json",
             "scratch/rnd/s4/labels_duration.json"):
    o = json.load(open(f"{BASE}/{path}", encoding="utf-8"))
    print(f"\n##### {path}")
    for ln in peta(o)[:55]:
        print(" ", ln)

o = json.load(open(f"{BASE}/scratch/rnd/s3/s3b_hybrid.json", encoding="utf-8"))
print("\n##### s3b_hybrid.json kunci atas:", list(o))
for k, v in o.items():
    if isinstance(v, list) and v and isinstance(v[0], dict):
        print(f"  {k}[{len(v)}] kunci[0]: {list(v[0])}")
    elif isinstance(v, dict):
        print(f"  {k}/ {list(v)[:12]}")
