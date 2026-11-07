"""R2: kandidat DOI via OpenAlex (pencarian) + cek registrasi via Crossref per DOI.

Satu skrip, dua jalur independen:
  1) OpenAlex  : cari kandidat paper (mendukung aplikasi PdM/pengeboran).
  2) Crossref  : /works/{doi} memastikan DOI terdaftar dan metadata cocok.
Output: scratch/rnd_r2/doi_verified.json
"""
import json
import time
import urllib.error
import urllib.parse
import urllib.request

UA = "rnd-r2-capstone/1.0 (mailto:zey.research@example.org)"
MAILTO = "zey.research@example.org"
OUT = "/mnt/d/Capstone 1(v2)/scratch/rnd_r2/doi_verified.json"


def get_json(url, timeout=35):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r), r.status


def openalex_search(q, per=4):
    url = "https://api.openalex.org/works?" + urllib.parse.urlencode(
        {"search": q, "per-page": per, "mailto": MAILTO, "select": "id,doi,title,publication_year,authorships,primary_location"}
    )
    d, _ = get_json(url)
    rows = []
    for w in d.get("results", []):
        auth = w.get("authorships") or []
        first = auth[0]["author"]["display_name"] if auth else "?"
        host = ((w.get("primary_location") or {}).get("source") or {}).get("display_name") or "?"
        rows.append({"doi": (w.get("doi") or "").replace("https://doi.org/", ""),
                     "title": w.get("title"), "year": w.get("publication_year"),
                     "first_author": first, "venue": host})
    return rows


QUERIES = {
    "markov_pdm": "Markov chain degradation state transition predictive maintenance",
    "markov_drill": "Markov chain drilling bit wear state transition",
    "hmm_wear": "hidden Markov model tool wear condition monitoring",
    "hmm_drill": "hidden Markov model drilling vibration state recognition",
    "mc_uncertainty": "Monte Carlo simulation uncertainty quantification alarm threshold",
    "mc_pdm": "Monte Carlo predictive maintenance false alarm probability",
    "mcmc_rul": "Bayesian MCMC remaining useful life estimation",
    "bayesnet_diag": "Bayesian network fault diagnosis drilling equipment",
    "cox_drill": "survival analysis drill bit life censored",
    "cox_pdm": "Cox proportional hazards equipment failure predictive maintenance",
    "rsf_pdm": "random survival forest prognostics censored failure",
    "deephit_phm": "DeepHit deep survival analysis machine prognostics",
}

search_out = {}
for tag, q in QUERIES.items():
    try:
        search_out[tag] = openalex_search(q)
        print(f"\n### {tag} :: {q}")
        for r in search_out[tag]:
            print(f"  - {r['doi']} | {r['first_author']} {r['year']} | {(r['title'] or '')[:100]} | {r['venue'][:50]}")
    except Exception as e:  # noqa: BLE001
        print(f"[FAIL openalex] {tag}: {type(e).__name__} {e}")
    time.sleep(0.4)

# --- Cek registrasi DOI kanonik via Crossref (serial, backoff) ---
CANON = [
    ("hmm_rabiner", "10.1109/5.18626"),
    ("cox_1972", "10.1111/j.2517-6161.1972.tb00899.x"),
    ("rsf_ishwaran", "10.1214/08-AOAS169"),
    ("deephit_lee", "10.1609/aaai.v32i1.11842"),
    ("deepsurv_katzman", "10.1186/s12874-018-0482-1"),
    ("mc_metropolis_ulam", "10.1080/01621459.1949.10483310"),
    ("mcmc_hastings", "10.1093/biomet/57.1.97"),
    ("mcmc_metropolis", "10.1063/1.1699114"),
    ("markov_norris", "10.1017/CBO9780511810633"),
    ("drill_vib_reckmann", "10.2118/127413-MS"),
    ("stick_slip_kyllingstad", "10.2118/16659-PA"),
    ("ssi_liu2025", "10.2298/TSCI2502521L"),
    ("teale_1965", "10.1016/0148-9062(65)90022-7"),
]


def crossref_doi(doi):
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi)}"
    for attempt in range(3):
        try:
            d, st = get_json(url + f"?mailto={MAILTO}")
            m = d["message"]
            y = None
            for k in ("issued", "published", "published-print"):
                p = (m.get(k) or {}).get("date-parts") or [[None]]
                if p and p[0] and p[0][0]:
                    y = p[0][0]
                    break
            a = m.get("author") or []
            fam = (a[0].get("family") or a[0].get("name")) if a else "?"
            return {"status": "OK", "http": st, "doi": m.get("DOI"),
                    "title": (m.get("title") or ["?"])[0], "year": y, "first_author": fam,
                    "container": (m.get("container-title") or ["?"])[0] if m.get("container-title") else "?",
                    "type": m.get("type")}
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:
                time.sleep(6 * (attempt + 1))
                continue
            return {"status": "FAIL", "http": e.code, "doi": doi}
        except Exception as e:  # noqa: BLE001
            return {"status": "FAIL", "err": f"{type(e).__name__} {e}", "doi": doi}
    return {"status": "FAIL", "http": 429, "doi": doi}


canon_out = []
for tag, doi in CANON:
    r = crossref_doi(doi)
    r["tag"] = tag
    canon_out.append(r)
    print(f"[CROSSREF] {tag:24s} {doi:42s} -> {r['status']} {r.get('http', '')} | {r.get('first_author', '')} {r.get('year', '')} | {str(r.get('title', ''))[:70]}")
    time.sleep(2.5)

json.dump({"search": search_out, "canon": canon_out}, open(OUT, "w"), indent=1)
print("\nSaved", OUT)
