#!/usr/bin/env python3
"""Enumerate raw wellbore folders: time-log chunk counts, depth logs, plus label fold names."""
import os, csv, glob, collections, json

BASE = "/mnt/d/Capstone 1"
RAW = os.path.join(BASE, "data/volve/witsml_raw")

print("=== folder -> log chunk inventory ===")
rows = []
for name in sorted(os.listdir(RAW)):
    p = os.path.join(RAW, name)
    if not os.path.isdir(p):
        continue
    # find 1/log/**
    logs = glob.glob(os.path.join(p, "1", "log", "**", "*.xml"), recursive=True)
    traj = glob.glob(os.path.join(p, "1", "trajectory", "**", "*.xml"), recursive=True)
    tub = glob.glob(os.path.join(p, "1", "tubular", "**", "*.xml"), recursive=True)
    msg = glob.glob(os.path.join(p, "1", "message", "**", "*.xml"), recursive=True)
    # total size of log xml
    sz = sum(os.path.getsize(f) for f in logs)
    rows.append((name, len(logs), len(traj), len(tub), len(msg), sz))
    print(f"  {name!r}: log={len(logs)} traj={len(traj)} tubular={len(tub)} msg={len(msg)} log_MB={sz/1e6:.1f}")

print("\n=== indexType peek for F-15* folders ===")
import re
for name in sorted(os.listdir(RAW)):
    if "F-15" not in name:
        continue
    p = os.path.join(RAW, name)
    if not os.path.isdir(p):
        continue
    files = sorted(glob.glob(os.path.join(p, "1", "log", "**", "*.xml"), recursive=True))
    print(f"  {name!r}: {len(files)} log xml; first={os.path.relpath(files[0], p) if files else None}")
    # peek indexType of first file
    if files:
        txt = open(files[0], errors="replace").read(200000)
        m = re.findall(r'<indexType>(.*?)</indexType>', txt)
        m2 = re.findall(r'<mnemonic>(.*?)</mnemonic>', txt)[:6]
        m3 = re.findall(r'<nameWellbore>(.*?)</nameWellbore>', txt)
        print(f"     indexType={set(m)} wellbore={set(m3)} first_mnemonics={m2}")

print("\n=== labels_curated_v2.csv wellbore values ===")
lab = os.path.join(BASE, "data/volve/labels_curated_v2.csv")
if not os.path.exists(lab):
    # search
    hits = glob.glob(os.path.join(BASE, "**", "labels_curated_v2.csv"), recursive=True)
    print(" not at default; hits:", hits)
    lab = hits[0] if hits else None
if lab:
    print(" file:", lab)
    with open(lab, newline="", errors="replace") as fh:
        r = csv.DictReader(fh)
        print(" columns:", r.fieldnames)
        c = collections.Counter()
        c2 = collections.Counter()
        n = 0
        for row in r:
            n += 1
            c[row.get("wellbore", "")] += 1
            c2[row.get("fold", row.get("well_fold", ""))] += 1
        print(" n_rows:", n)
        print(" wellbore counts:")
        for k, v in sorted(c.items(), key=lambda x: -x[1]):
            print(f"    {k!r}: {v}")
        if any(c2):
            print(" fold counts:", dict(c2))
