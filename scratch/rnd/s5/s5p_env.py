#!/usr/bin/env python3
"""S5 probe: baca meta S1 untuk executable dan hash acuan, cek pustaka."""
import json
import os
import sys

BASE = "/mnt/d/Capstone 1(v2)"
m = json.load(open(f"{BASE}/scratch/rnd/s1/s1_meta.json"))
for k in ("executable", "python", "pandas", "numpy", "perintah", "elapsed_s",
          "dataset_sha256", "harness_sha256", "r8_sha256", "dataset", "fold_file"):
    print(f"{k}: {m.get(k)}")
print("current executable:", sys.executable)
print("current version:", sys.version.split()[0])
for mod in ("numpy", "pandas", "lightgbm", "sklearn"):
    try:
        __import__(mod)
        print(f"{mod}: OK")
    except Exception as e:
        print(f"{mod}: MISSING ({type(e).__name__}: {e})")
print("env VIRTUAL_ENV:", os.environ.get("VIRTUAL_ENV"))
print("cwd:", os.getcwd())
