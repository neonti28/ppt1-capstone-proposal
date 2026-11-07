#!/usr/bin/env python3
"""
RND-R3 / M2: verifikasi DOI.
Dua jalur: (a) Crossref API untuk metadata, (b) resolve https://doi.org/<doi> untuk
memastikan DOI benar-benar bisa dibuka.
Juga menjalankan pencarian bibliografis Crossref untuk menemukan DOI topik
(bearing fault + VMD + SVM, drilling vibration) lalu melaporkan kandidat teratas.
Output: m2_doi_verified.json
"""
import json, os, ssl, sys, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "m2_doi_verified.json")
UA = "rnd-r3-provenance/1.0 (mailto:agent@example.invalid)"
CTX = ssl.create_default_context()

KNOWN = [
    ("Dragomiretskiy & Zosso 2014 VMD", "10.1109/TSP.2013.2288675"),
    ("Huang et al. 1998 EMD", "10.1098/rspa.1998.0193"),
    ("Daubechies 1988 orthonormal bases wavelets", "10.1002/cpa.3160410705"),
    ("Cortes & Vapnik 1995 support-vector networks", "10.1007/BF00994018"),
    ("Ratanamahatana & Keogh 2004 DTW constraints", "10.1007/978-3-540-30075-5_46"),
    ("Yeh et al. 2016 matrix profile I (STAMP)", "10.1109/ICDM.2016.0179"),
    ("Mirjalili et al. 2014 GWO", "10.1016/j.advengsoft.2013.12.007"),
    ("Mirjalili & Lewis 2016 WOA", "10.1016/j.advengsoft.2016.01.008"),
    ("Reckmann et al. 2010 drilling vibration", "10.2118/127413-MS"),
    ("Kyllingstad & Halsey 1988 stick-slip", "10.2118/16659-PA"),
    ("Randall & Antoni 2011 bearing diagnostics tutorial", "10.1098/rsta.2010.0331"),
]

QUERIES = [
    ("bearing VMD SVM", "variational mode decomposition rolling bearing fault diagnosis support vector machine"),
    ("bearing VMD GWO SVM", "grey wolf optimizer variational mode decomposition bearing fault support vector machine"),
    ("drilling vibration decomposition", "drilling vibration signal decomposition empirical mode decomposition drillstring"),
    ("whale optimization SVM bearing", "whale optimization algorithm support vector machine bearing fault diagnosis"),
    ("matrix profile discord", "matrix profile time series discord motif discovery"),
]


def get(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
        return r.status, r.read()


def crossref_doi(doi):
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="")
    try:
        st, body = get(url)
        m = json.loads(body)["message"]
        auth = m.get("author") or []
        first = None
        if auth:
            a = auth[0]
            first = " ".join(x for x in [a.get("family"), a.get("given")] if x) or a.get("name")
        year = None
        for k in ("published-print", "published-online", "issued", "created"):
            if m.get(k, {}).get("date-parts"):
                year = m[k]["date-parts"][0][0]
                break
        return {"crossref_http": st, "title": (m.get("title") or [""])[0],
                "first_author": first, "year": year,
                "container": (m.get("container-title") or [""])[0],
                "volume": m.get("volume"), "page": m.get("page"),
                "type": m.get("type"), "status": "CROSSREF_OK"}
    except Exception as e:
        return {"status": "CROSSREF_FAIL", "error": f"{type(e).__name__}: {e}"}


def resolve_doi(doi):
    url = "https://doi.org/" + urllib.parse.quote(doi, safe="/:()")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30, context=CTX) as r:
            return {"resolve_http": r.status, "final_url": r.geturl()}
    except urllib.error.HTTPError as e:
        return {"resolve_http": e.code, "final_url": getattr(e, "url", None),
                "note": "HTTPError (penerbit menolak bot)" if e.code in (403, 404) else "HTTPError"}
    except Exception as e:
        return {"resolve_http": None, "error": f"{type(e).__name__}: {e}"}


def search(q, rows=4):
    url = ("https://api.crossref.org/works?rows=%d&select=DOI,title,author,issued,container-title"
           "&query.bibliographic=%s" % (rows, urllib.parse.quote(q)))
    try:
        st, body = get(url)
        items = json.loads(body)["message"]["items"]
        out = []
        for m in items:
            auth = m.get("author") or []
            first = None
            if auth:
                a = auth[0]
                first = " ".join(x for x in [a.get("family"), a.get("given")] if x) or a.get("name")
            year = None
            if m.get("issued", {}).get("date-parts"):
                year = m["issued"]["date-parts"][0][0]
            out.append({"doi": m.get("DOI"), "title": (m.get("title") or [""])[0],
                        "first_author": first, "year": year,
                        "container": (m.get("container-title") or [""])[0]})
        return out
    except Exception as e:
        return [{"error": f"{type(e).__name__}: {e}"}]


def main():
    res = {"generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
           "note": "Crossref = metadata; resolve = apakah doi.org bisa dibuka",
           "known": [], "search": []}
    for label, doi in KNOWN:
        rec = {"label": label, "doi": doi}
        rec.update(crossref_doi(doi))
        time.sleep(0.3)
        rec.update(resolve_doi(doi))
        time.sleep(0.3)
        res["known"].append(rec)
        with open(OUT, "w") as f:
            json.dump(res, f, indent=2)
        print(f'{doi:42s} {rec.get("status","?"):13s} resolve={rec.get("resolve_http")} '
              f'{(rec.get("title") or "")[:60]}', flush=True)
    for tag, q in QUERIES:
        hits = search(q)
        res["search"].append({"tag": tag, "query": q, "hits": hits})
        with open(OUT, "w") as f:
            json.dump(res, f, indent=2)
        print("\n[search]", tag)
        for h in hits:
            print("   ", h.get("doi"), "|", h.get("year"), "|", (h.get("title") or "")[:80])
    print("\nWROTE", OUT)


if __name__ == "__main__":
    main()
