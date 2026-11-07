#!/usr/bin/env python3
"""R5 — probe lingkungan + struktur kolom hyd_ki (stdlib saja)."""
import gzip
import csv
import sys

print("python", sys.version.split()[0])
for mod in ("numpy", "sklearn", "scipy", "pandas"):
    try:
        m = __import__(mod)
        print("OK", mod, getattr(m, "__version__", "?"))
    except Exception as exc:
        print("MISSING", mod, type(exc).__name__)

p = "/mnt/d/Capstone 1(v2)/scratch/v9_d1/datasets/hyd_ki.csv.gz"
with gzip.open(p, "rt", newline="", encoding="utf-8") as f:
    rd = csv.DictReader(f)
    cols = rd.fieldnames
    print("NCOL", len(cols))
    print("COLS", cols)
    r = next(rd)
    print("ROW0", {k: r[k] for k in cols[:18]})
