import re, pathlib, json

DOCS = {
 "S1": "docs/RND_S1_SEED_ROBUSTNESS.md",
 "S2": "docs/RND_S2_HYBRID_VIB_SSI.md",
 "S3": "docs/RND_S3_HYBRID_BITWEAR.md",
 "S4": "docs/RND_S4_LAYER_B_DATA.md",
}
out = {}
for k, rel in DOCS.items():
    p = pathlib.Path(rel)
    t = p.read_text(encoding="utf-8", errors="replace")
    lines = t.splitlines()
    record = {
        "path": rel,
        "bytes": p.stat().st_size,
        "lines": len(lines),
        "em_dash": t.count("\u2014"),
        "en_dash": t.count("\u2013"),
        "riset_pendahuluan": [l.strip() for l in lines if "Riset pendahuluan" in l],
        "sequ_count": len(re.findall(r"sequ", t, re.I)),
        "dois": sorted(set(re.findall(r"10\.\d{4,9}/[^\s\)\]\|,;]+", t))),
        "headings": [f"{i}:{l}" for i, l in enumerate(lines, 1) if l.startswith("#")],
        "lapisan": {kw: t.count(kw) for kw in ["Lapisan A","Lapisan B","Lapisan C","lapisan A","lapisan B","lapisan C"]},
        "belum_lines": [f"{i}:{l.strip()[:160]}" for i, l in enumerate(lines, 1) if re.search(r"belum (ter)?verifikasi|Belum (ter)?verifikasi", l)],
        "table_rows": sum(1 for l in lines if l.startswith("|")),
    }
    out[k] = record
    print("=" * 78)
    print(k, rel, "| bytes", record["bytes"], "| lines", record["lines"])
    print("em-dash:", record["em_dash"], "en-dash:", record["en_dash"], "| sequ:", record["sequ_count"], "| DOI:", len(record["dois"]))
    for l in record["riset_pendahuluan"]:
        print("  RISET:", l)
    for d in record["dois"]:
        print("  DOI:", d)
    print("  -- headings --")
    for h in record["headings"]:
        print("   ", h)
    print("  -- lapisan --", record["lapisan"])
    print("  -- belum --")
    for b in record["belum_lines"]:
        print("   ", b)
    print("  table rows:", record["table_rows"])

pathlib.Path("scratch/rnd/s5/a1_struktur.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
print("\nWROTE scratch/rnd/s5/a1_struktur.json")
