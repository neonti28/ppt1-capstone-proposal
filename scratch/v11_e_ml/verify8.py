#!/usr/bin/env python3
"""Cek 8: kata kunci rubrik pada kedua kandidat (ML chapter + whole doc) + Evaluasi User.txt."""
import os, re, glob

BASE = "/mnt/d/Capstone 1(v2)"
DOCS = os.path.join(BASE, "docs")

K1 = os.path.join(DOCS, "ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.v3_arsip.md")
K2 = os.path.join(DOCS, "ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md")

KEYS = ["Riset pendahuluan", "Brier", "ECE", "A/B/C", "Lapisan A", "deep learning",
        "Deep learning", "Logistic", "regresi logistik", "Regresi logistik",
        "Gradient", "7 vs 11 vs 27", "27 head", "11 klaim", "121 klaim", "UNDERPOWER",
        "underpowered", "persistence-onset", "D-A5", "q95", "bootstrap", "CI95",
        "Brier & ECE", "canary", "grid search", "pencarian hiperparameter"]


def slice_ml_k1(t):
    i = t.find("## 8. Data"); j = t.find("## 14. Arsitektur")
    return t[i:j]


def slice_ml_k2(t):
    i = t.find("## Bab 4: Labeling untuk Head ML"); j = t.find("## Bab 5: Metode Statistik")
    return t[i:j]


for tag, p, slicer in [("KANDIDAT_1", K1, slice_ml_k1), ("KANDIDAT_2", K2, slice_ml_k2)]:
    t = open(p, encoding="utf-8").read()
    ml = slicer(t)
    print(f"=== {tag} ===  full={len(t)} chars | bab-ML={len(ml)} chars")
    for k in KEYS:
        c_full = len(re.findall(re.escape(k), t))
        c_ml = len(re.findall(re.escape(k), ml))
        if c_full or c_ml:
            print(f"   {k!r}: di seluruh dokumen={c_full}, di bab ML={c_ml}")
    print()

print("=== jumlah baris & struktur bab ===")
for tag, p in [("KANDIDAT_1", K1), ("KANDIDAT_2", K2)]:
    lines = open(p, encoding="utf-8").read().splitlines()
    print(f"{tag}: total baris={len(lines)} | baris '### '={sum(1 for l in lines if l.startswith('### '))} "
          f"| baris '## '={sum(1 for l in lines if l.startswith('## ') and not l.startswith('### '))} "
          f"| tabel={sum(1 for l in lines if l.startswith('|'))}")

print("\n=== Evaluasi User.txt (instrumen rubrik) ===")
cands = []
for root in (BASE, os.path.expanduser("~/.hermes/kanban/boards/capstone-v11-vs")):
    for p in glob.glob(os.path.join(root, "**", "*valuasi*ser*"), recursive=True):
        cands.append(p)
print("kandidat berkas:", sorted(set(cands))[:10])
for p in sorted(set(cands))[:3]:
    if os.path.isfile(p):
        print(f"--- {p} ({os.path.getsize(p)} bytes)")
        print(open(p, encoding="utf-8", errors="replace").read()[:3000])
