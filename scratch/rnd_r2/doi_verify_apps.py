"""R2: verifikasi Crossref untuk DOI kandidat aplikasi (hasil OpenAlex)."""
import json
import time
import urllib.error
import urllib.parse
import urllib.request

UA = "rnd-r2-capstone/1.0 (mailto:zey.research@example.org)"
DOIS = [
    ("markov_chiachio2019", "10.1016/j.ress.2019.106621"),
    ("markov_budimir2025", "10.3390/jmse13040798"),
    ("semimarkov_cartella2015", "10.1155/2015/278120"),
    ("markov_camci2010", "10.1109/tase.2009.2038170"),
    ("hmm_ertunc2001", "10.1016/S0890-6955(00)00112-7"),
    ("hmm_yu2016", "10.1007/s00170-016-9711-0"),
    ("hmm_cholette2014", "10.1080/0740817X.2014.905734"),
    ("mc_depater2022", "10.1016/j.ress.2022.108341"),
    ("mc_annaz2026", "10.1016/j.nexres.2026.102266"),
    ("mcmc_pang2020", "10.1016/j.ress.2020.107341"),
    ("mcmc_benker2020", "10.1016/j.jmsy.2020.11.005"),
    ("bn_soltanali2021", "10.3390/en14227758"),
    ("bn_xia2024", "10.1109/TR.2024.3416064"),
    ("cox_chen2020", "10.1016/j.aei.2020.101054"),
    ("cox_malevich2019", "10.1007/978-3-030-25147-5_15"),
    ("rsf_asghar2024", "10.1186/s12911-024-02525-z"),
    ("rsf_zhou2016", "10.1186/s40064-016-3113-5"),
    ("deephit_ren2019", "10.1609/aaai.v33i01.33014798"),
]
OUT = "/mnt/d/Capstone 1(v2)/scratch/rnd_r2/doi_verified_apps.json"


def fetch(doi):
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi)}?mailto=zey.research@example.org"
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=35) as r:
                m = json.load(r)["message"]
                y = None
                for k in ("issued", "published", "published-print"):
                    p = (m.get(k) or {}).get("date-parts") or [[None]]
                    if p and p[0] and p[0][0]:
                        y = p[0][0]
                        break
                a = m.get("author") or []
                fam = (a[0].get("family") or a[0].get("name")) if a else "?"
                return {"status": "OK", "http": r.status, "doi": m.get("DOI"),
                        "title": (m.get("title") or ["?"])[0], "year": y, "first_author": fam,
                        "container": (m.get("container-title") or ["?"])[0] if m.get("container-title") else "?",
                        "type": m.get("type")}
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:
                time.sleep(8 * (attempt + 1))
                continue
            return {"status": "FAIL", "http": e.code, "doi": doi}
        except Exception as e:  # noqa: BLE001
            return {"status": "FAIL", "err": f"{type(e).__name__} {e}", "doi": doi}
    return {"status": "FAIL", "http": 429, "doi": doi}


res = []
for tag, doi in DOIS:
    r = fetch(doi)
    r["tag"] = tag
    res.append(r)
    print(f"{tag:26s} {doi:40s} -> {r['status']} {r.get('http','')} | {r.get('first_author','')} {r.get('year','')} | {str(r.get('title',''))[:75]} | {str(r.get('container',''))[:45]}")
    time.sleep(2.0)

json.dump(res, open(OUT, "w"), indent=1)
print("saved", OUT)
