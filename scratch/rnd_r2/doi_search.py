"""R2: pemilihan + verifikasi DOI kandidat via Crossref API (query bibliografis).

Menjalankan pencarian Crossref untuk tiap metode, mencetak 3 kandidat teratas
(DOI, judul, tahun, wadah), lalu mencatat apakah DOI terdaftar.
Tidak mengarang DOI: DOI diambil dari respons Crossref.
"""
import json
import time
import urllib.parse
import urllib.request

UA = "rnd-r2-capstone/1.0 (mailto:research@example.org)"

QUERIES = {
    "markov": "Markov chain model equipment condition state transition maintenance",
    "markov_drill": "Markov chain drilling bit wear state transition",
    "hmm": "hidden Markov model tool wear condition monitoring",
    "hmm_drill": "hidden Markov model drilling vibration stick-slip state",
    "montecarlo": "Monte Carlo simulation uncertainty propagation threshold alarm",
    "montecarlo_pdm": "Monte Carlo predictive maintenance false alarm rate estimation",
    "mcmc": "Markov chain Monte Carlo Bayesian remaining useful life estimation",
    "bayesnet": "Bayesian network fault diagnosis rotating machinery",
    "cox": "Cox proportional hazards model drill bit life censored",
    "cox_pdm": "proportional hazards model equipment failure time censored maintenance",
    "rsf": "random survival forest remaining useful life censored",
    "deephit": "DeepHit deep learning survival analysis competing risks",
    "deephit_pdm": "deep learning survival time prediction machine prognostics censored",
    "rnn_surv": "recurrent neural network survival analysis predictive maintenance",
}


def crossref(q, rows=3):
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode(
        {"query.bibliographic": q, "rows": rows, "select": "DOI,title,author,issued,container-title,type"}
    )
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.load(r)["message"]["items"]


def first_author(it):
    a = it.get("author") or []
    if not a:
        return "?"
    return (a[0].get("family") or a[0].get("name") or "?")


def year(it):
    for k in ("issued", "published-print", "published-online"):
        v = it.get(k) or {}
        p = v.get("date-parts") or [[None]]
        if p and p[0] and p[0][0]:
            return p[0][0]
    return "?"


out = {}
for tag, q in QUERIES.items():
    try:
        items = crossref(q)
    except Exception as e:  # noqa: BLE001
        print(f"[FAIL] {tag}: {type(e).__name__} {e}")
        continue
    rows = []
    print(f"\n### {tag} :: {q}")
    for it in items:
        doi = it.get("DOI")
        title = (it.get("title") or ["?"])[0]
        cont = (it.get("container-title") or ["?"])[0] if it.get("container-title") else "?"
        rows.append({"doi": doi, "title": title, "year": year(it), "first": first_author(it),
                     "container": cont, "type": it.get("type")})
        print(f"  - {doi} | {first_author(it)} {year(it)} | {title[:110]} | {cont[:60]}")
    out[tag] = rows
    time.sleep(1.2)

with open("/mnt/d/Capstone 1(v2)/scratch/rnd_r2/doi_candidates.json", "w") as f:
    json.dump(out, f, indent=1)
print("\nSaved:", len(out), "queries")
