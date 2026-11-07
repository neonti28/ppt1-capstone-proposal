"""RND-E2: audit angka dokumen lawan ledger E2 (versi disaring).

Hanya token numerik di LUAR tabel rujukan dan di luar baris judul yang dinilai,
karena nomor volume/jurnal/DOI bukan angka hasil.
"""
from __future__ import annotations

import re
from pathlib import Path

BASE = Path("/mnt/d/Capstone 1(v2)")
doc = (BASE / "docs/RND_E2_PROTOKOL.md").read_text()
led = (BASE / "docs/RND_PROVENANCE_LEDGER.md").read_text()
e2 = "\n".join(l for l in led.splitlines() if l.startswith("| E2-"))

lines = doc.splitlines()
in_refs = False
body_lines = []
for ln in lines:
    if ln.startswith("## 11. RUJUKAN"):
        in_refs = True
    elif ln.startswith("## 12."):
        in_refs = False
    if in_refs or ln.startswith("#") or ln.startswith("Kartu:"):
        continue
    if "papers/v" in ln or "arxiv.org" in ln or "doi.org" in ln or "10." in ln:
        continue
    body_lines.append(ln)

pat = re.compile(r"\d[\d.]*(?:,\d+)?")
tokens = set()
for ln in body_lines:
    tokens.update(pat.findall(ln))

missing = sorted(t for t in tokens if t not in e2)
print(f"token di badan dokumen : {len(tokens)}")
print(f"tidak ada di ledger E2 : {len(missing)}")
for t in missing:
    ctx = next((l.strip()[:100] for l in body_lines if t in l), "")
    print(f"  {t:10s} | {ctx}")
