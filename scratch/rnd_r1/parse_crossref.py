#!/usr/bin/env python3
"""Parse hasil curl Crossref (lokal, tanpa jaringan). Filter judul: token algoritma + token domain."""
import json, os, glob, re

HERE = os.path.dirname(os.path.abspath(__file__))
ALGO_TOKENS = {
    "gwo": ["grey wolf", "gray wolf"],
    "woa": ["whale optimization"],
    "pso": ["particle swarm"],
    "ssa": ["sparrow search"],
    "hho": ["harris hawk"],
    "epo": ["emperor penguin"],
    "sma": ["slime mould", "slime mold"],
    "bgwo": ["binary grey wolf", "binary gray wolf", "binary gwo"],
    "eo": ["equilibrium optimizer", "equilibrium optimization"],
    "hbo": ["honey badger"],
    "horse": ["horse herd"],
    "slime": ["slime mould", "slime mold"],
}
DOM = ["fault", "diagnos", "vibrat", "bearing", "drill", "maintenance", "rul",
       "machinery", "gear", "wear", "condition monitor", "degradation", "anomal"]

rows = {}
for f in glob.glob(os.path.join(HERE, "raw", "*.json")):
    slug = os.path.basename(f).split("__")[0]
    try:
        with open(f, encoding="utf-8") as fh:
            items = json.load(fh)["message"]["items"]
    except Exception as e:  # noqa: BLE001
        print("SKIP", os.path.basename(f), e)
        continue
    for it in items:
        title = (it.get("title") or [""])[0]
        tl = title.lower()
        if not any(t in tl for t in ALGO_TOKENS[slug]):
            continue
        if not any(d in tl for d in DOM):
            continue
        y = (it.get("issued", {}).get("date-parts") or [[None]])[0][0]
        if not y or y < 2019:
            continue
        doi = it.get("DOI")
        if not doi:
            continue
        au = it.get("author") or []
        first = ""
        if au:
            a = au[0]
            first = ", ".join(x for x in [a.get("family"), a.get("given")] if x)
        rec = {
            "doi": doi, "title": re.sub(r"\s+", " ", title).strip(), "year": y,
            "first_author": first,
            "journal": re.sub(r"\s+", " ", (it.get("container-title") or [""])[0]).strip(),
            "cited_by": it.get("is-referenced-by-count") or 0,
            "src": os.path.basename(f),
        }
        k = doi.lower()
        if k not in rows or rec["cited_by"] > rows[k]["cited_by"]:
            rows[k] = rec

by = {a: [] for a in ALGO_TOKENS}
for r in rows.values():
    tl = r["title"].lower()
    for slug, toks in ALGO_TOKENS.items():
        if any(t in tl for t in toks):
            by[slug].append(r)

out = {}
for slug, rs in by.items():
    rs.sort(key=lambda r: (-r["cited_by"], r["year"]))
    out[slug] = rs
    print(f"\n=== {slug}  n={len(rs)}")
    for r in rs[:8]:
        print(f"  {r['year']} c{r['cited_by']:4d} {r['doi']:38s} {r['title'][:110]}")

with open(os.path.join(HERE, "parse_result.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=1, ensure_ascii=False)
print("\ntotal unique DOI:", len(rows))
