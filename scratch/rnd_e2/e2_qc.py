"""RND-E2: pemeriksaan mutu dokumen + keterkaitan angka ke ledger.

Cek: em-dash, en-dash, karakter CJK, jumlah bagian, tabel seimbang, dan
keberadaan angka kunci dokumen di ledger E2.
"""
from __future__ import annotations

import re
from pathlib import Path

BASE = Path("/mnt/d/Capstone 1(v2)")
DOC = BASE / "docs/RND_E2_PROTOKOL.md"
LED = BASE / "docs/RND_PROVENANCE_LEDGER.md"

text = DOC.read_text()
ledger = LED.read_text()
fail = []

em = text.count("\u2014")
en = text.count("\u2013")
cjk = len(re.findall(r"[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]", text))
sections = len(re.findall(r"^## ", text, re.M))
fences = text.count("```")

# tabel: setiap baris tabel harus punya jumlah pipa sama dengan header tabelnya
bad_rows = []
lines = text.splitlines()
i = 0
while i < len(lines):
    if lines[i].startswith("|") and i + 1 < len(lines) and set(lines[i + 1].replace("|", "").strip()) <= {"-", ":"}:
        n_pipe = lines[i].count("|")
        j = i + 2
        while j < len(lines) and lines[j].startswith("|"):
            if lines[j].count("|") != n_pipe:
                bad_rows.append((j + 1, n_pipe, lines[j].count("|"), lines[j][:60]))
            j += 1
        i = j
    else:
        i += 1

# angka kunci harus ada di ledger E2
key_numbers = [
    ("21,55", "E2-009"), ("0,1685", "E2-024"), ("14,7555", "E2-027"), ("3,6889", "E2-026"),
    ("0,7748", "E2-021"), ("1,43", "E2-012"), ("5,14", "E2-012"), ("24,5", "E2-015"),
    ("0,0390625", "E2-020"), ("1.320", "E2-037"), ("6,7583", "E2-029"), ("0,50", "E2-017"),
]
e2_rows = [l for l in ledger.splitlines() if l.startswith("| E2-")]
ledger_e2 = "\n".join(e2_rows)
missing = [(n, r) for n, r in key_numbers if n not in ledger_e2]

print(f"baris dokumen      : {len(lines)}")
print(f"ukuran dokumen     : {len(text.encode())} B")
print(f"jumlah bagian (##) : {sections}")
print(f"em-dash (U+2014)   : {em}")
print(f"en-dash (U+2013)   : {en}")
print(f"karakter CJK       : {cjk}")
print(f"blok kode (```)    : {fences} (harus genap)")
print(f"tabel baris rusak  : {len(bad_rows)}")
for b in bad_rows[:10]:
    print("   ", b)
print(f"baris ledger E2    : {len(e2_rows)}")
print(f"angka kunci hilang : {missing if missing else 'tidak ada'}")

if em or cjk or fences % 2 or bad_rows or missing:
    fail.append("ada temuan")
print("\nVERDICT:", "LULUS" if not fail else "PERIKSA")
