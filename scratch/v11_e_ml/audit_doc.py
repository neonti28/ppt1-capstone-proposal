#!/usr/bin/env python3
"""Audit dokumen keluaran V11_ML.md: em-dash/en-dash, angka klaim, silang ke primer."""
import json, os, re

BASE = "/mnt/d/Capstone 1(v2)"
doc = open(os.path.join(BASE, "docs/V11_ML.md"), encoding="utf-8").read()

print("=== 1. karakter berisiko ===")
for name, ch in [("EM DASH —", "—"), ("EN DASH –", "–"), ("HYPHEN-MINUS-dash ganda", "--")]:
    n = doc.count(ch)
    print(f"  {name}: {n}")
    if n:
        for m in list(re.finditer(re.escape(ch), doc))[:8]:
            print("      ...", doc[max(0, m.start() - 60):m.start() + 40].replace("\n", " "))

print("\n=== 2. konsistensi internal skor ===")
print("  kandidat1: 13+19+23+9 =", 13 + 19 + 23 + 9, "| tertulis 64:", "64" in doc)
print("  kandidat2: 28+26+22+14 =", 28 + 26 + 22 + 14, "| tertulis 90:", "90" in doc)
print("  baris tabel skor ada:", doc.count("(1) Kedalaman teknis"))

print("\n=== 3. manifest JSON primer ===")
j = json.load(open(os.path.join(BASE, "scratch/v11_e_ml/V11_ML_PRIMER.json")))
man = j["meta"]["primer_manifest"]
print("  jumlah entri manifest:", len(man), "| hilang:",
      [m["path"] for m in man if m.get("missing")])
print("  ledger:", len(j["claim_ledger"]), "entri")
from collections import Counter
c = Counter(l["status"].split()[0] for l in j["claim_ledger"])
print("  rekap status:", dict(c))
print("  fold per engine:", {k: v["n_folds"] for k, v in j["primer_fold_data"].items()})

print("\n=== 4. klaim angka di dokumen vs primer (cek ulang independen) ===")
S = os.path.join(BASE, "scratch/v9_e_ml")
eng = {e: json.load(open(os.path.join(S, f"v9_e_ML_{e}_RESULTS.json")))
       for e in ["vib", "ssi", "shk", "stuck_k2"]}
sk = eng["stuck_k2"]
pers = [f["baselines"]["persistence"]["auprc"] for f in sk["folds"]]
rf = [f["models"]["rf"]["auprc"] for f in sk["folds"]]
print("  persistence stuck range:", round(min(pers), 4), round(max(pers), 4),
      "| tertulis [0.8265, 0.9016]:", round(min(pers), 4) == 0.8265 and round(max(pers), 4) == 0.9016)
print("  RF stuck range:", round(min(rf), 4), round(max(rf), 4),
      "| tertulis [0.0697, 0.4443]:", round(min(rf), 4) == 0.0697 and round(max(rf), 4) == 0.4443)
lifts = [round(f["models"]["rf"]["lift"], 4) for f in eng["vib"]["folds"]]
print("  vib lift:", lifts, "| tertulis 1,6133/2,3620/3,4972/1,6289:",
      lifts == [1.6133, 2.362, 3.4972, 1.6289])
print("  determinism:", eng["vib"]["determinism_check"])
print("  UP folds:", [(e, f["test_well"], f["pos_test"]) for e in eng for f in eng[e]["folds"]
                     if f["underpowered"]])

print("\n=== 5. klaim kualitatif dokumen vs hitungan ===")
print("  '25 berkas primer' =", len(man), "cocok:", len(man) == 25)
print("  '10 skrip verifier' =", len(j["meta"]["verifier_scripts"]),
      "cocok:", len(j["meta"]["verifier_scripts"]) == 10)
print("  '28 entri ledger' =", len(j["claim_ledger"]),
      "cocok:", len(j["claim_ledger"]) == 28)
tr = sum(1 for l in j["claim_ledger"] if l["status"].startswith("TERBUKTI"))
ko = sum(1 for l in j["claim_ledger"] if l["status"].startswith("KOREKSI"))
hi = sum(1 for l in j["claim_ledger"] if l["status"].startswith("HIPOTESIS"))
di = sum(1 for l in j["claim_ledger"] if l["status"].startswith("DIDUKUNG"))
print(f"  rekap dokumen '22 TERBUKTI / 1 DIDUKUNG / 1 HIPOTESIS / 4 KOREKSI' vs "
      f"hasil: TERBUKTI={tr} KOREKSI={ko} HIPOTESIS={hi} DIDUKUNG={di}")
print("  total entri = ", tr + ko + hi + di)

print("\n=== 6. jumlah baris dokumen & format ===")
lines = doc.split("\n")
print("  baris:", len(lines), "| karakter:", len(doc))
print("  baris Riset pendahuluan:", len(re.findall(r"Riset pendahuluan", doc)))
print("  judul H2:", [l for l in lines if l.startswith("## ")])
