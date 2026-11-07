#!/usr/bin/env python3
"""Harvest literatur metaheuristik via Crossref REST API (registri DOI resmi).
Output: scratch/rnd_r1/harvest_crossref.json  + ringkasan stdout.
Filter: judul harus memuat token algoritma DAN token domain.
"""
import json, time, urllib.parse, urllib.request, os, re

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "harvest_crossref.json")
UA = "RND-R1-research/1.0 (mailto:rnd@example.invalid)"

ALGOS = {
    "GWO": (["grey wolf optimizer", "grey wolf optimization"], "GWO"),
    "WOA": (["whale optimization algorithm", "whale optimization"], "WOA"),
    "PSO": (["particle swarm optimization", "particle swarm optimisation"], "PSO"),
    "SSA": (["sparrow search algorithm"], "SSA"),
    "HHO": (["harris hawks optimization", "harris hawks optimizer"], "HHO"),
    "EPO": (["emperor penguin optimizer", "emperor penguin optimization"], "EPO"),
    "SMA": (["slime mould algorithm", "slime mold algorithm"], "SMA"),
    "BGWO": (["binary grey wolf optimizer", "binary grey wolf optimization", "binary gray wolf"], "BGWO"),
    "EO": (["equilibrium optimizer", "equilibrium optimization algorithm"], "EO"),
    "HBO": (["honey badger optimization", "honey badger optimizer", "honey badger algorithm"], "HBO"),
    "HHO_HORSE": (["horse herd optimization", "horse herd optimization algorithm"], "HorseHerd"),
    "SLIME": (["slime mould algorithm", "slime mold optimization"], "Slime"),
}

DOMAINS = [
    "fault diagnosis",
    "bearing fault",
    "vibration signal",
    "drilling",
    "predictive maintenance",
    "remaining useful life",
    "rotating machinery",
]
DOMAIN_TOKENS = ["fault", "diagnos", "vibrat", "bearing", "drill", "maintenance",
                 "remaining useful life", "rul", "machinery", "gear", "tool wear", "condition monitor"]


def fetch(query, rows=25):
    url = ("https://api.crossref.org/works?" + urllib.parse.urlencode({
        "query.bibliographic": query,
        "filter": "from-pub-date:2019-01-01,type:journal-article",
        "rows": rows,
        "select": "DOI,title,author,issued,container-title,is-referenced-by-count,type",
    }))
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=45) as r:
        return json.loads(r.read().decode("utf-8", "replace"))["message"]["items"]


def year(it):
    for k in ("issued", "published"):
        v = it.get(k, {}).get("date-parts", [[None]])[0][0]
        if v:
            return int(v)
    return None


def main():
    out = {}
    stats = {"requests": 0, "errors": []}
    for key, (terms, label) in ALGOS.items():
        found = {}
        for t in terms:
            for dom in DOMAINS:
                q = f"{t} {dom}"
                try:
                    items = fetch(q)
                    stats["requests"] += 1
                except Exception as e:  # noqa: BLE001
                    stats["errors"].append(f"{q}: {e}")
                    time.sleep(1.0)
                    continue
                for it in items:
                    title = (it.get("title") or [""])[0]
                    tl = title.lower()
                    if t not in tl:
                        continue
                    if not any(dt in tl for dt in DOMAIN_TOKENS):
                        continue
                    y = year(it)
                    if not y or y < 2019:
                        continue
                    doi = it.get("DOI")
                    if not doi:
                        continue
                    if doi not in found or (it.get("is-referenced-by-count") or 0) > found[doi]["cited_by"]:
                        au = it.get("author") or []
                        first = ""
                        if au:
                            a = au[0]
                            first = " ".join(x for x in [a.get("family"), a.get("given")] if x)
                        found[doi] = {
                            "doi": doi,
                            "title": title,
                            "year": y,
                            "first_author": first,
                            "journal": (it.get("container-title") or [""])[0],
                            "cited_by": it.get("is-referenced-by-count") or 0,
                            "query": q,
                        }
                time.sleep(0.25)
        vals = sorted(found.values(), key=lambda r: -r["cited_by"])
        out[key] = {"label": label, "n": len(vals), "records": vals[:10]}
        print(f"{label:12s} n={len(vals):3d} top={[(v['year'], v['doi']) for v in vals[:4]]}")
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump({"generated": time.strftime("%Y-%m-%d %H:%M:%S"), "stats": stats, "algos": out}, f, indent=1, ensure_ascii=False)
    print("stats", stats["requests"], "reqs,", len(stats["errors"]), "errors ->", OUT)


if __name__ == "__main__":
    main()
