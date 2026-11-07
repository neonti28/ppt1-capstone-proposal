#!/usr/bin/env python3
"""Cek 3: md = ipynb? (paket deliverable) + ekstrak bab ML dari ipynb utk perbandingan."""
import json, re, os, hashlib

DOCS = "/mnt/d/Capstone 1(v2)/docs"
PAIRS = [
    ("kandidat_1", "ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.v3_arsip.md",
     "ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.v3_arsip.ipynb"),
    ("kandidat_2", "ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md",
     "ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.ipynb"),
]


def norm(s):
    s = s.replace("\r\n", "\n")
    s = re.sub(r"[ \t]+", " ", s)
    return s.strip()


def md_to_lines(txt):
    return [l for l in txt.split("\n") if l.strip()]


for tag, mdf, ipf in PAIRS:
    mdp = os.path.join(DOCS, mdf)
    ipp = os.path.join(DOCS, ipf)
    md = open(mdp, encoding="utf-8").read()
    nb = json.load(open(ipp, encoding="utf-8"))
    cells = nb.get("cells", [])
    kinds = {}
    for c in cells:
        kinds[c["cell_type"]] = kinds.get(c["cell_type"], 0) + 1
    ip_text = "\n".join("".join(c.get("source", [])) for c in cells)
    md_lines = md_to_lines(md)
    ip_lines = md_to_lines(ip_text)
    md_set = {norm(l) for l in md_lines}
    ip_set = {norm(l) for l in ip_lines}
    # key lines = headings
    md_heads = [l for l in md_lines if l.strip().startswith("#")]
    ip_heads = [l for l in ip_lines if l.strip().startswith("#")]
    print(f"=== {tag} ===")
    print(f"  md: {len(md_lines)} baris non-kosong | ipynb: {len(cells)} sel {kinds}, "
          f"{len(ip_lines)} baris non-kosong")
    print(f"  md headings = {len(md_heads)} | ipynb headings = {len(ip_heads)}")
    only_md_h = [h for h in md_heads if norm(h) not in ip_set]
    only_ip_h = [h for h in ip_heads if norm(h) not in set(md_set)]
    print(f"  heading di md TIDAK ada di ipynb: {len(only_md_h)}")
    for h in only_md_h[:15]:
        print("     -", h[:130])
    print(f"  heading di ipynb TIDAK ada di md: {len(only_ip_h)}")
    for h in only_ip_h[:15]:
        print("     +", h[:130])
    # coverage: baris md yang hilang di ipynb
    miss = [l for l in md_lines if norm(l) not in ip_set]
    extra = [l for l in ip_lines if norm(l) not in md_set]
    print(f"  baris md hilang di ipynb: {len(miss)} ({100*len(miss)/max(1,len(md_lines)):.1f}%)")
    for l in miss[:12]:
        print("     -", l[:130])
    print(f"  baris ipynb di luar md: {len(extra)} ({100*len(extra)/max(1,len(ip_lines)):.1f}%)")
    for l in extra[:8]:
        print("     +", l[:130])
    # ML chapter presence
    pat = re.compile(r"labeling per kelas|LABELING PER KELAS|FITUR 55|fitur 55|Kontrak RF|KONTRAK RF|persistence-onset|LOWO", re.I)
    ml_md = sum(1 for l in md_lines if pat.search(l))
    ml_ip = sum(1 for l in ip_lines if pat.search(l))
    print(f"  baris kunci bab-ML: md={ml_md} ipynb={ml_ip}")
    print(f"  sha256 md={hashlib.sha256(md.encode()).hexdigest()[:16]} "
          f"ip_text_sha={hashlib.sha256(ip_text.encode()).hexdigest()[:16]}")
    print()
