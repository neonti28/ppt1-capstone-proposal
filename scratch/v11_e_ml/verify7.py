#!/usr/bin/env python3
"""Cek 7: (1) pandas NaN ts_bin/lab_ts di file v2 + file workspace LAMA;
(2) v8_onsets_match per well; (3) MIN_DRILL_*; (4) nama engine kanonik 7/11/27."""
import os, gzip, csv, json, collections

BASE_V2 = "/mnt/d/Capstone 1(v2)"
BASE_OLD = "/mnt/d/Capstone 1"

print("=== 1a. file v2: cek kolom pakai pandas ===")
try:
    import pandas as pd
    for tag, p in [("v2", os.path.join(BASE_V2, "scratch/v9_d1/datasets/stuck_k2.csv.gz")),
                   ("OLD", os.path.join(BASE_OLD, "scratch/v9_d1/datasets/stuck_k2.csv.gz"))]:
        if not os.path.exists(p):
            print(f"  {tag}: TIDAK ADA -> {p}")
            continue
        df = pd.read_csv(p, usecols=lambda c: c in ("well", "ts_bin", "lab_ts", "lab_kind",
                                                    "feat_ts_max", "y_stuck_onset"))
        print(f"  {tag}: rows={len(df)} cols={list(df.columns)}")
        print(f"     dtypes={dict(df.dtypes.astype(str))}")
        print(f"     NaN: ts_bin={int(df['ts_bin'].isna().sum())} "
              f"lab_ts={int(df['lab_ts'].isna().sum())} "
              f"feat_ts_max={int(df['feat_ts_max'].isna().sum())}")
        print(f"     lab_kind top={df['lab_kind'].value_counts(dropna=False).head(5).to_dict()}")
        print(f"     ts_bin head={df['ts_bin'].head(3).tolist()} lab_ts head={df['lab_ts'].head(3).tolist()}")
except Exception as e:
    print("  pandas gagal:", type(e).__name__, e)

print("\n=== 1b. bandingkan hash kedua file (identik?) ===")
import hashlib
for tag, p in [("v2", os.path.join(BASE_V2, "scratch/v9_d1/datasets/stuck_k2.csv.gz")),
               ("OLD", os.path.join(BASE_OLD, "scratch/v9_d1/datasets/stuck_k2.csv.gz"))]:
    if os.path.exists(p):
        h = hashlib.sha256(open(p, "rb").read()).hexdigest()[:32]
        st = os.stat(p)
        import datetime
        print(f"  {tag}: sha256[:32]={h} size={st.st_size} "
              f"mtime={datetime.datetime.fromtimestamp(st.st_mtime)}")
    else:
        print(f"  {tag}: tidak ada")

print("\n=== 1c. dataset_sha256 di JSON hasil (primer) vs file ===")
# train.py: sha256 dari 2**20 byte pertama
for e in ["vib", "ssi", "shk", "stuck_k2"]:
    for tag, root in [("v2", BASE_V2), ("OLD", BASE_OLD)]:
        p = os.path.join(root, f"scratch/v9_d1/datasets/{e}.csv.gz")
        j = os.path.join(root, f"scratch/v9_e_ml/v9_e_ML_{e}_RESULTS.json")
        if os.path.exists(j):
            d = json.load(open(j))
            want = d.get("dataset_sha256")
            got = hashlib.sha256(open(p, "rb").read(2**20)).hexdigest() if os.path.exists(p) else None
            print(f"  {e} json_dataset_path={d.get('dataset')} | sha_json={want} | "
                  f"sha_file[{tag}]={got} | cocok={want == got}")

print("\n=== 2. v9_d1_04_qc.json: v8_onsets_match per well ===")
p = os.path.join(BASE_V2, "scratch/v9_d1/v9_d1_04_qc.json")
j = json.load(open(p))
for w, rec in j["wells"].items():
    print(f"  {w}: onsets_ffill={rec.get('onsets_ffill')} onsets_strict={rec.get('onsets_strict')} "
          f"onsets_scorable={rec.get('onsets_scorable')} v8_onsets_match={rec.get('v8_onsets_match')} "
          f"positives={rec.get('positives')}")
print("  reference_onsets_v8 =", j.get("reference_onsets_v8"))

print("\n=== 3. MIN_DRILL_BINS / MIN_DRILL_ROWS ===")
p = os.path.join(BASE_V2, "code/v9_d1_02_rig_windows.py")
for i, l in enumerate(open(p, encoding="utf-8", errors="replace").read().splitlines(), 1):
    if "MIN_DRILL" in l or "SSI_MIN" in l:
        print(f"  :{i}: {l.strip()}")

print("\n=== 4. nama kanonik 7 engine (outline PM1) ===")
for cand in ["docs/V10_PM1_OUTLINE.md", "docs/V9_PM1_ARCHITECTURE.md"]:
    p = os.path.join(BASE_V2, cand)
    if not os.path.exists(p):
        print("  MISSING", cand); continue
    lines = open(p, encoding="utf-8", errors="replace").read().splitlines()
    for i, l in enumerate(lines, 1):
        if ("7 engine" in l or "7 ENGINE" in l or "tujuh engine" in l.lower()) and i < 120:
            print(f"  {cand}:{i}: {l.strip()[:200]}")
    # tabel daftar engine
    for i, l in enumerate(lines, 1):
        if any(k in l for k in ("vib", "ssi", "shk", "hyd", "bit_wear", "tool_wear")) and \
           ("| " in l) and i < 200:
            print(f"  {cand}:{i}: {l.strip()[:200]}")
