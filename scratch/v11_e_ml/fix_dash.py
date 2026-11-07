#!/usr/bin/env python3
"""Bersihkan em-dash dari dokumen V11_ML.md (aturan Zey) + perbaiki satu angka butir."""
p = "/mnt/d/Capstone 1(v2)/docs/V11_ML.md"
doc = open(p, encoding="utf-8").read()

REPL = [
    ("# V11-E_ML — UJI BAB", "# V11-E_ML: UJI BAB"),
    ("** — OBSERVED", "**: OBSERVED"),
    ("** — bukti mentah", "**: bukti mentah"),
    ("** — AUPRC + CI95", "**: AUPRC + CI95"),
    ("## 2. TUGAS 1 — LABELING", "## 2. TUGAS 1: LABELING"),
    ("## 3. TUGAS 2 — KONTRAK", "## 3. TUGAS 2: KONTRAK"),
    ("## 4. TUGAS 3 — ANGKA", "## 4. TUGAS 3: ANGKA"),
    ("## 5. TUGAS 4 — RF DILARANG", "## 5. TUGAS 4: RF DILARANG"),
    ("## 6. TUGAS 5 — KEPUTUSAN", "## 6. TUGAS 5: KEPUTUSAN"),
    ("## 7. TUGAS 6 — KELENGKAPAN", "## 7. TUGAS 6: KELENGKAPAN"),
    ("(ΔB negatif 7/7, replikasi eksak) — TIDAK digeneralisasi",
     "(ΔB negatif 7/7, replikasi eksak); larangan ini TIDAK digeneralisasi"),
    ("### kandidat 1 — `", "### kandidat 1: `"),
    ("### kandidat 2 — `", "### kandidat 2: `"),
    ("4 engine × 5 butir", "4 engine × 4 butir"),
]
for old, new in REPL:
    n = doc.count(old)
    if n == 0:
        print("PERINGATAN: pola tidak ditemukan:", old[:60])
    doc = doc.replace(old, new)

open(p, "w", encoding="utf-8").write(doc)
print("em-dash sisa:", doc.count("—"), "| en-dash (rentang, diperbolehkan):", doc.count("–"))
sisa = []
i = doc.find("—")
while i >= 0:
    sisa.append(doc[max(0, i - 60):i + 40].replace("\n", " "))
    i = doc.find("—", i + 1)
for s in sisa:
    print("  SISA:", s)
