#!/usr/bin/env python3
"""Verifikasi DOI: metadata via Crossref /works/{doi} + status HTTP doi.org/{doi}.
Juga mencari DOI paper asal (original) tiap algoritma lewat Crossref search.
Memo: urllib hang di WSL ini, jadi semua jaringan lewat curl (subprocess).
"""
import json, subprocess, sys, os, re, time

HERE = os.path.dirname(os.path.abspath(__file__))
UA = "RND-R1-research/1.0 (mailto:rnd@example.invalid)"

CANDIDATES = {
    "GWO": ["10.1016/j.measurement.2020.107901", "10.3390/en12214170", "10.3390/s23146645"],
    "WOA": ["10.1016/j.aej.2021.03.034", "10.1016/j.egyr.2021.09.188", "10.1016/j.isatra.2024.02.014"],
    "PSO": ["10.1016/j.isatra.2019.01.012", "10.1109/access.2020.2968382", "10.1016/j.measurement.2024.114451"],
    "SSA": ["10.1109/access.2021.3075547", "10.1016/j.measurement.2021.110079", "10.1007/s12652-022-03703-5"],
    "HHO": ["10.1016/j.measurement.2020.108580", "10.3390/app10041403", "10.1007/s10462-022-10233-1"],
    "EPO": ["10.1016/j.eswa.2023.122940", "10.1049/elp2.12459", "10.1007/s11277-021-08765-w"],
    "SMA": ["10.1016/j.measurement.2021.109389", "10.1016/j.measurement.2025.117878", "10.1016/j.psep.2024.11.135"],
    "BGWO": ["10.1016/j.knosys.2022.108701", "10.1007/s11227-022-04931-4"],
    "EO": ["10.1155/2022/3792828", "10.1016/j.phycom.2024.102372", "10.3390/pr11061813"],
    "HBO": ["10.3390/machines10060469", "10.1016/j.ifacol.2022.05.040", "10.3390/en18040841"],
    "HORSE": ["10.1038/s41598-026-43015-8", "10.52783/jes.8089"],
}

ORIGINALS = [
    ("GWO", "Grey wolf optimizer", "Advances in Engineering Software"),
    ("WOA", "The whale optimization algorithm", "Advances in Engineering Software"),
    ("HHO", "Harris hawks optimization: Algorithm and applications", "Future Generation Computer Systems"),
    ("EPO", "Emperor penguin optimizer: a bio-inspired algorithm for engineering problems", "Knowledge-Based Systems"),
    ("SMA", "Slime mould algorithm: A new method for stochastic optimization", "Future Generation Computer Systems"),
    ("BGWO", "Binary grey wolf optimization approaches for feature selection", "Neurocomputing"),
    ("EO", "Equilibrium optimizer: A novel optimization algorithm", "Knowledge-Based Systems"),
    ("HBO", "Honey badger algorithm: new metaheuristic algorithm for solving optimization problems", "Mathematics and Computers in Simulation"),
    ("HORSE", "Horse herd optimization algorithm: A new metaheuristic algorithm for high-dimensional optimization problems", "Knowledge-Based Systems"),
    ("SSA", "Sparrow search algorithm", "Systems Science & Control Engineering"),
]


def curl_json(url):
    p = subprocess.run(["curl", "-s", "-m", "25", "-A", UA, url], capture_output=True, text=True)
    if p.returncode != 0 or not p.stdout.strip():
        return None
    try:
        return json.loads(p.stdout)
    except Exception:
        return None


def doi_status(doi):
    url = "https://doi.org/" + doi
    p = subprocess.run(["curl", "-s", "-o", "/dev/null", "-m", "25", "-L", "-A",
                        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
                        "-w", "%{http_code}", url], capture_output=True, text=True)
    return p.stdout.strip()


def meta(doi):
    m = curl_json("https://api.crossref.org/works/" + doi)
    if not m:
        return None
    it = m["message"]
    au = it.get("author") or []
    first = ""
    if au:
        a = au[0]
        first = ", ".join(x for x in [a.get("family"), a.get("given")] if x)
    y = (it.get("issued", {}).get("date-parts") or [[None]])[0][0]
    return {
        "doi": doi,
        "title": re.sub(r"\s+", " ", (it.get("title") or [""])[0]).strip(),
        "year": y,
        "first_author": first,
        "journal": re.sub(r"\s+", " ", (it.get("container-title") or [""])[0]).strip(),
        "type": it.get("type"),
        "cited_by": it.get("is-referenced-by-count"),
    }


out = {"candidates": {}, "originals": {}}
print("== A. KANDIDAT TERAPAN (Crossref metadata + status doi.org) ==")
for algo, dois in CANDIDATES.items():
    out["candidates"][algo] = []
    for d in dois:
        m = meta(d)
        st = doi_status(d)
        time.sleep(0.2)
        if not m:
            print(f"{algo:6s} {d:40s} METADATA-GAGAL http={st}")
            out["candidates"][algo].append({"doi": d, "http": st, "meta": None})
            continue
        print(f"{algo:6s} {str(m['year']):4s} http={st:3s} {m['first_author'][:28]:28s} {m['title'][:78]}")
        out["candidates"][algo].append({"doi": d, "http": st, "meta": m})

print("\n== B. PAPER ASAL ALGORITMA (Crossref search) ==")
for algo, title, journal in ORIGINALS:
    q = title.replace(" ", "+").replace(":", "")
    j = curl_json(f"https://api.crossref.org/works?query.bibliographic={q}&rows=3&select=DOI,title,author,issued,container-title,is-referenced-by-count")
    time.sleep(0.2)
    if not j:
        print(f"{algo:6s} SEARCH-GAGAL")
        continue
    items = j["message"]["items"]
    for it in items:
        t = (it.get("title") or [""])[0].lower()
        key = title.lower().split(":")[0][:35]
        if key not in t:
            continue
        d = it["DOI"]
        m = meta(d)
        st = doi_status(d)
        time.sleep(0.2)
        au = (it.get("author") or [{}])[0]
        print(f"{algo:6s} {str((it.get('issued',{}).get('date-parts') or [[None]])[0][0]):4s} http={st:3s} {d:34s} {(it.get('container-title') or [''])[0][:40]:40s} {(it.get('title') or [''])[0][:60]}")
        out["originals"][algo] = {"doi": d, "http": st, "meta": m}
        break

with open(os.path.join(HERE, "doi_verify.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1, ensure_ascii=False)
print("\nsaved doi_verify.json")
