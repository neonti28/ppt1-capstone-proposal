#!/usr/bin/env python3
"""Audit S5 - (a) rujukan kode ledger di dokumen, (b) target DOI, (c) lapisan A/B/C.

(a) setiap kode Sx-nnn yang disebut dokumen harus punya baris ledger, dan setiap
    baris ledger sebaiknya disebut minimal satu kali di dokumen kartunya.
(b) dokumen dicari pola DOI dan URL/rujukan pustaka.
(c) pemisahan lapisan A, B, C dan kalimat "belum terukur" per lapisan.
"""
import json
import pathlib
import re
from collections import Counter

BASE = pathlib.Path("/mnt/d/Capstone 1(v2)")
LEDGER = BASE / "docs/RND_PROVENANCE_LEDGER.md"
DOC = {"S1": "docs/RND_S1_SEED_ROBUSTNESS.md", "S2": "docs/RND_S2_HYBRID_VIB_SSI.md",
       "S3": "docs/RND_S3_HYBRID_BITWEAR.md", "S4": "docs/RND_S4_LAYER_B_DATA.md"}


def ledger_kode(kartu):
    out, aktif = set(), False
    for l in LEDGER.read_text(encoding="utf-8").splitlines():
        if l.startswith("## Bagian"):
            aktif = bool(re.search(r"Bagian %s\b" % kartu, l))
            continue
        if aktif:
            m = re.match(r"^\|\s*(%s-\d+)\s*\|" % kartu, l)
            if m:
                out.add(m.group(1))
    return out


h = {}
for kartu, rel in DOC.items():
    doc = (BASE / rel).read_text(encoding="utf-8")
    lk = ledger_kode(kartu)
    cited = set(re.findall(r"%s-\d{3}" % kartu, doc))
    hilang = sorted(cited - lk)
    tak_dikutip = sorted(lk - cited)
    # DOI dan rujukan luar
    dois = sorted(set(re.findall(r"10\.\d{4,9}/[^\s\)\]\|,;`]+", doc)))
    urls = sorted(set(re.findall(r"https?://[^\s\)\]\|,;`]+", doc)))
    lit = [l.strip()[:120] for l in doc.splitlines()
           if re.search(r"\bet al\.|doi|arXiv|ISO \d|API RP|NORSOK", l, re.I)]
    # lapisan
    lap = {}
    for L in "ABC":
        pola = re.compile(r"[Ll]apisan %s" % L)
        ada = bool(pola.search(doc))
        belum = bool(re.search(r"[Ll]apisan %s[^.]{0,400}?BELUM|BELUM[^.]{0,200}?[Ll]apisan %s" % (L, L), doc, re.S))
        lap[L] = dict(ada_judul=ada, ada_pernyataan_belum=belum)
    h[kartu] = dict(
        n_kode_ledger=len(lk), n_kode_dikutip=len(cited),
        kode_hilang=hilang, n_tak_dikutip=len(tak_dikutip), tak_dikutip=tak_dikutip[:12],
        dois=dois, urls=urls, literatur=lit[:8], lapisan=lap,
        em_dash=doc.count("\u2014"),
    )
    print("=" * 74)
    print(kartu, rel)
    print(f"  kode ledger {len(lk)} | dikutip dokumen {len(cited)} | hilang {len(hilang)} | "
          f"tak dikutip {len(tak_dikutip)}")
    if hilang:
        print("   KODE HILANG:", hilang)
    if tak_dikutip:
        print("   kode tanpa kutipan:", tak_dikutip[:8])
    print("  DOI:", dois, "| URL:", urls)
    print("  pola literatur:", lit[:4])
    print("  lapisan:", lap, "| em-dash:", h[kartu]["em_dash"])

(BASE / "scratch/rnd/s5/s5_kode_doi_lapisan.json").write_text(
    json.dumps(h, indent=1, ensure_ascii=False), encoding="utf-8")
print("\nWROTE scratch/rnd/s5/s5_kode_doi_lapisan.json")
