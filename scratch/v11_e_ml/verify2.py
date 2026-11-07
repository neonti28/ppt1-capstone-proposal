#!/usr/bin/env python3
"""Cek 2: klaim LOWO (k1), sumber label, leak-checker, stuck_k1 2 fold, baris dataset."""
import json, glob, os, gzip, csv, io, collections

BASE = "/mnt/d/Capstone 1(v2)"
out = []

print("=== A. lowo_*.json: jumlah fold & well uji & jumlah well total ===")
for p in sorted(glob.glob(os.path.join(BASE, "scratch/v9_d1/lowo_*.json"))):
    j = json.load(open(p))
    folds = j["folds"]
    tw = [f["test_well"] for f in folds]
    trn = set()
    for f in folds:
        trn |= set(f["train_wells"])
    print(f"{os.path.basename(p)}: n_fold={len(folds)} test_wells={tw} "
          f"union_train_wells={sorted(trn)} keys={list(j.keys())}")

print("\n=== B. sumber label di kode (klaim kandidat 2 §1) ===")
needles = ["VIB_THRESH", "SSI_MIN_SAMPLES", "H = 10", "H=10", "32.17405", "LABDEF"]
for f in ["code/v9_d1_02_rig_windows.py", "code/v9_d1_03_rig_datasets.py",
          "code/v9_d1_04_stuck_k2.py", "code/v9_e_ML_01_train.py"]:
    p = os.path.join(BASE, f)
    if not os.path.exists(p):
        print(f"  MISSING {f}"); continue
    txt = open(p, encoding="utf-8", errors="replace").read().splitlines()
    for i, line in enumerate(txt, 1):
        if any(n in line for n in needles) and not line.strip().startswith("#"):
            print(f"  {f}:{i}: {line.strip()[:160]}")

print("\n=== C. labels_curated_v2.csv: 884 event (50/571/263) ===")
p = os.path.join(BASE, "data/volve/labels_curated_v2.csv")
if os.path.exists(p):
    with open(p, newline="", encoding="utf-8", errors="replace") as fh:
        r = csv.DictReader(fh)
        rows = list(r)
        print("  header:", r.fieldnames, "n_rows =", len(rows))
        for col in (r.fieldnames or []):
            vals = collections.Counter(x[col] for x in rows)
            if len(vals) <= 8:
                print(f"   {col}: {dict(vals)}")
else:
    print("  MISSING", p)

print("\n=== D. leak-checker output (klaim 0 pelanggaran 6/6 dataset) ===")
for p in sorted(glob.glob(os.path.join(BASE, "scratch/v9_d1/*leak*.json"))):
    j = json.load(open(p))
    print(" ", os.path.basename(p))
    print("  ", json.dumps(j, ensure_ascii=False)[:1200])

print("\n=== E. baris dataset stuck_k2 (klaim 118.567 baris) ===")
p = os.path.join(BASE, "scratch/v9_d1/datasets/stuck_k2.csv.gz")
if os.path.exists(p):
    n = 0
    with gzip.open(p, "rt", encoding="utf-8", errors="replace") as fh:
        header = fh.readline().rstrip("\n").split(",")
        cols = {c: i for i, c in enumerate(header)}
        for line in fh:
            n += 1
    print("  rows =", n, "n_cols =", len(header))
    print("  header:", header)
else:
    print("  MISSING", p)

print("\n=== F. onset counts per well (klaim k2: F-9_A 72, F-10 93, F-14 61, F-9 55) ===")
# dihitung dari kolom y_stuck_onset? tidak: onset = transisi STUCK 0->1 (ffill).
# pakai kolom label dataset: hitung run 0->1 dari y_stuck_onset adalah label horizon, bukan onset.
# sumber: dataset stuck_k2 label horizon; onset asli = jumlah label positif / 10 baris perkiraan.
# verifikasi alternatif: v9_d1_04_stuck_k2.py menyimpan ringkasan onset.
d4 = os.path.join(BASE, "code/v9_d1_04_stuck_k2.py")
if os.path.exists(d4):
    for i, line in enumerate(open(d4, encoding="utf-8", errors="replace").read().splitlines(), 1):
        if "onset" in line.lower() and any(ch.isdigit() for ch in line) and len(line) < 200:
            print(f"  v9_d1_04:{i}: {line.strip()}")
for p in sorted(glob.glob(os.path.join(BASE, "scratch/v9_d1/*stuck*.json"))) + \
         sorted(glob.glob(os.path.join(BASE, "scratch/v9_d1/*.json"))):
    pass
print("\n  file scratch/v9_d1:")
for p in sorted(glob.glob(os.path.join(BASE, "scratch/v9_d1/*.json"))):
    print("   ", os.path.basename(p))
