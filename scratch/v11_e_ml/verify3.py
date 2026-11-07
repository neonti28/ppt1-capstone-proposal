#!/usr/bin/env python3
"""Cek 4: defect stuck_k2, mekanisme persistence-onset, label hyd/bit, angka 28 fold, klaim V8."""
import json, gzip, glob, os, collections, math

BASE = "/mnt/d/Capstone 1(v2)"

print("=== A. stuck_k2: ts_bin/lab_ts kosong? feat_ts_max monotonic? y_prev NaN? ===")
p = os.path.join(BASE, "scratch/v9_d1/datasets/stuck_k2.csv.gz")
with gzip.open(p, "rt") as fh:
    h = fh.readline().rstrip("\n").split(",")
    ix = {c: i for i, c in enumerate(h)}
    n = 0
    empty = collections.Counter()
    per_well = collections.Counter()
    last_ts = {}
    mono_bad = collections.Counter()
    nan_prev = 0
    pos = 0
    pos_prev1 = 0
    pos_valid = 0
    for line in fh:
        c = line.rstrip("\n").split(",")
        n += 1
        w = c[ix["well"]]
        per_well[w] += 1
        if c[ix["ts_bin"]].strip() in ("", "nan", "NaN"):
            empty["ts_bin"] += 1
        if c[ix["lab_ts"]].strip() in ("", "nan", "NaN"):
            empty["lab_ts"] += 1
        ft = c[ix["feat_ts_max"]].strip()
        if ft and ft not in ("nan", "NaN"):
            v = float(ft)
            if w in last_ts and v < last_ts[w]:
                mono_bad[w] += 1
            last_ts[w] = v
        yp = c[ix["y_prev_stuck_onset"]].strip()
        if yp in ("", "nan", "NaN"):
            nan_prev += 1
        y = c[ix["y_stuck_onset"]].strip()
        if y not in ("", "nan", "NaN") and int(float(y)) == 1:
            pos += 1
            if yp not in ("", "nan", "NaN") and int(float(yp)) == 1:
                pos_prev1 += 1
print("rows =", n, "| per well =", dict(per_well))
print("ts_bin kosong =", dict(empty), "(dari ts_bin & lab_ts)")
print("lab_ts kosong =", {k: v for k, v in empty.items()})
print("feat_ts_max turun antar baris (per well) =", dict(mono_bad))
print("y_prev_stuck_onset NaN =", nan_prev)
print(f"baris positif = {pos}; di antaranya y_prev==1 = {pos_prev1} "
      f"({100*pos_prev1/max(1,pos):.1f}%)  [klaim k2: '±6/7 baris positif']")

print("\n=== B. klaim k2: '28 fold' ada di V9_E_ML_ENGINE.md (koreksi dokumentasi) ===")
eng_md = open(os.path.join(BASE, "docs/V9_E_ML_ENGINE.md"), encoding="utf-8").read().splitlines()
for i, l in enumerate(eng_md, 1):
    if "28 fold" in l or "28 FOLD" in l.upper() or "4 engine × LOWO = 28" in l:
        print(f"  V9_E_ML_ENGINE.md:{i}: {l.strip()[:180]}")

print("\n=== C. klaim hyd K-i label (k2 §1): z robust median/MAD SPPA per bin qcut(TFLO,10), |z|>2, W=10 ===")
p = os.path.join(BASE, "code/v9_d1_03_rig_datasets.py")
if os.path.exists(p):
    for i, l in enumerate(open(p, encoding="utf-8", errors="replace").read().splitlines(), 1):
        if any(k in l for k in ("qcut", "MAD", "mad", "|z|", "z_robust", "> 2", "TFLO", "n_bin", "SPPA")):
            if len(l) < 200:
                print(f"  v9_d1_03:{i}: {l.strip()}")

print("\n=== D. klaim k2: high_MSE Teale P75 = 256,600 psi (USROP_labeled) ===")
p = os.path.join(BASE, "data/USROP_labeled.csv")
if os.path.exists(p):
    import csv as _csv
    with open(p, newline="", encoding="utf-8", errors="replace") as fh:
        r = _csv.DictReader(fh)
        rows = list(r)
        print("  header:", r.fieldnames)
        print("  n_rows =", len(rows))
        for col in r.fieldnames or []:
            if "mse" in col.lower() or col.lower() == "label":
                vals = [x[col] for x in rows if x[col] not in ("", None)]
                print(f"  {col}: n={len(vals)} contoh={vals[:5]}")
else:
    print("  MISSING", p)

print("\n=== E. klaim V8 pembanding (k2 §6.2/6.3): RF>=canary 5/5 (vib? ssi?), persistence kalah 0/5, shk 6/9 ===")
hits = []
for p in sorted(glob.glob(os.path.join(BASE, "docs/V8_E_*.md"))):
    txt = open(p, encoding="utf-8", errors="replace").read().splitlines()
    for i, l in enumerate(txt, 1):
        if any(k in l for k in ("5/5", "6/9", "0/5")) and any(k in l.lower() for k in ("canary", "persistence", "ΔB", "deltab")):
            hits.append((os.path.basename(p), i, l.strip()[:170]))
for h in hits[:20]:
    print("  ", h)
print("  total temuan:", len(hits))

print("\n=== F. cross-check 'kemenangan fold' / majority rule k1: 'tujuh nilai lipatan' ===")
# jumlah fold & jumlah well per engine (primer)
for p in sorted(glob.glob(os.path.join(BASE, "scratch/v9_d1/lowo_*.json"))):
    j = json.load(open(p))
    print(f"  {os.path.basename(p)}: n_folds={j.get('n_folds')} wells_field={j.get('wells')} "
          f"n_rows={j.get('n_rows')}")
