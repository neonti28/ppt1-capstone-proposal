#!/usr/bin/env python3
"""Verifikasi independen S3: parser csv (bukan pandas) dan cek dokumen/ledger."""
import csv
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict

BASE = "/mnt/d/Capstone 1(v2)"
CSVP = f"{BASE}/data/USROP_labeled.csv"
DOC = f"{BASE}/docs/RND_S3_HYBRID_BITWEAR.md"
LEDGER = f"{BASE}/docs/RND_PROVENANCE_LEDGER.md"
GEN = f"{BASE}/scratch/rnd/s3/s3d_dokumen.py"
PY = "/home/neonti/.venv_audit/bin/python3"

with open(f"{BASE}/scratch/rnd/s3/s3c_ringkas.json") as f:
    S = json.load(f)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]


print("=== 1. hitung ulang dengan modul csv ===")
n = 0
cnt = Counter()
per_well = defaultdict(lambda: [0, 0])
mse_vals, roc_vals = [], []
rows = []
with open(CSVP, newline="", encoding="utf-8") as f:
    rd = csv.DictReader(f)
    for r in rd:
        n += 1
        lab = r["label"]
        cnt[lab] += 1
        w = r["well"]
        per_well[w][0] += 1
        if lab == "high_MSE_bit_wear":
            per_well[w][1] += 1
        try:
            m = float(r["MSE"])
            c = float(r["ROC_coef"])
        except (TypeError, ValueError):
            continue
        if m > 0:
            mse_vals.append(m)
        if c > 0:
            roc_vals.append(c)
        rows.append((m, c, lab))

print("baris", n, "== 198928 ?", n == 198928)
print("label", dict(cnt))
print("high_MSE", cnt["high_MSE_bit_wear"], "== 49732 ?", cnt["high_MSE_bit_wear"] == 49732)
print("well", len(per_well), "== 7 ?", len(per_well) == 7)
tanpa = sorted(w for w, (a, b) in per_well.items() if b == 0)
print("well tanpa positif", tanpa, "== 2 ?", len(tanpa) == 2)


def pctl(v, q):
    a = sorted(v)
    pos = (len(a) - 1) * q / 100.0
    lo, hi = int(pos // 1), int(-(-pos // 1))
    if lo == hi:
        return a[lo]
    return a[lo] + (a[hi] - a[lo]) * (pos - lo)


m75 = pctl(mse_vals, 75)
r25 = pctl(roc_vals, 25)
mism = 0
for m, c, lab in rows:
    rk = "high_MSE_bit_wear" if m > m75 else ("low_ROP_efficiency" if c < r25 else "normal")
    mism += rk != lab
print("mse_p75", round(m75, 6), "json", S["kelayakan"]["sirkularitas"]["mse_p75_positif"])
print("roc_p25", round(r25, 9), "json", S["kelayakan"]["sirkularitas"]["roc_p25_positif"])
print("mismatch", mism, "== 0 ?", mism == 0)

print("\n=== 2. dokumen ===")
doc = open(DOC).read()
print("baris", len(doc.splitlines()))
print("em-dash", doc.count("\u2014"), "en-dash", doc.count("\u2013"))
print("ada 'Riset pendahuluan'", doc.count("Riset pendahuluan:"))
print("sebut jumlah pikiran", "Jumlah pikiran: **5**" in doc)
print("ada ringkasan lima baris", "Ringkasan lima baris" in doc)
print("ada belum terverifikasi", "Yang belum terverifikasi" in doc)
print("sebut lapisan A/B/C", all(x in doc for x in ("Lapisan A", "Lapisan B", "Lapisan C")))

print("\n=== 2b. aritmetika FAR dan kecocokan menit berdata ===")
import pandas as pd
import numpy as np

h = json.load(open(f"{BASE}/scratch/rnd/s3/s3b_hybrid.json"))
bad = []
for r in h["records"]:
    f = r["far"]
    hit = f["menit_alarm_neg"] / (f["menit_berdata"] / 60.0 / 24.0) if f["menit_berdata"] else None
    if hit is None or abs(hit - f["far24_kalender"]) > 1e-3:
        bad.append((r["fold"], r["model"], hit, f["far24_kalender"]))
    if f["menit_berdata"] > f["rentang_menit"]:
        bad.append((r["fold"], r["model"], "berdata > rentang", f["menit_berdata"], f["rentang_menit"]))
print("record diperiksa", len(h["records"]), "| menyimpang", len(bad), bad[:3])

t = pd.read_csv(f"{BASE}/data/volve/usrop_timestamped.csv")
ts = pd.to_datetime(t["est_timestamp"], errors="coerce", utc=True)
t["menit"] = (ts - pd.Timestamp("1970-01-01", tz="UTC")).dt.total_seconds() / 60.0
uniq = t.dropna(subset=["menit"]).groupby("well")["menit"].apply(lambda s: np.floor(s).nunique())
cocok = 0
for r in h["records"]:
    if r["model"] != "H5_stat_dan_rule":
        continue
    w = r["fold"]
    if int(uniq.get(w, -1)) == r["far"]["menit_berdata"]:
        cocok += 1
    else:
        print("  beda menit", w, uniq.get(w), r["far"]["menit_berdata"])
print("fold dengan menit berdata cocok hitungan ulang", cocok, "dari 7")

print("\n=== 3. ledger ===")
led = open(LEDGER).read()
print("blok Bagian S3", led.count("## Bagian S3:"))
s3 = re.findall(r"^\| S3-(\d{3}) \|", led, re.M)
print("baris S3", len(s3), "unik", len(set(s3)), "duplikat", len(s3) - len(set(s3)))
kolom = [l.count("|") for l in led.splitlines() if l.startswith("| S3-")]
print("jumlah kolom pipa unik", sorted(set(kolom)))

print("\n=== 4. idempoten (jalankan generator 2x) ===")
d0, l0 = sha(DOC), sha(LEDGER)
for i in range(2):
    r = subprocess.run([PY, GEN], capture_output=True, text=True)
    if r.returncode != 0:
        print("GAGAL run", i, r.stderr[-500:])
        sys.exit(1)
d1, l1 = sha(DOC), sha(LEDGER)
print("doc", d0, d1, "sama", d0 == d1)
print("ledger", l0, l1, "sama", l0 == l1)
led2 = open(LEDGER).read()
print("setelah 2x run, blok S3", led2.count("## Bagian S3:"), "baris S3", len(re.findall(r"^\| S3-\d{3} \|", led2, re.M)))
