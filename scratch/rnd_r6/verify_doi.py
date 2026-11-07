"""R6: verifikasi DOI via Crossref API + cek landing doi.org. Hasil -> doi_verify_r6.json."""
import json
import urllib.request
import urllib.error
from pathlib import Path

OUT = Path("/mnt/d/Capstone 1(v2)/scratch/rnd_r6/doi_verify_r6.json")
UA = {"User-Agent": "rnd-r6-verify/1.0 (mailto:research@example.org)"}

DOIS = [
    "10.2307/2531595",                    # DeLong 1988
    "10.1214/aos/1176344552",             # Efron 1979
    "10.1111/j.2517-6161.1995.tb02031.x",  # Benjamini-Hochberg 1995
    "10.1080/01621459.1927.10502953",     # Wilson 1927
    "10.1007/BF02295996",                 # McNemar 1947
    "10.1007/978-3-642-40994-3_29",       # Boyd/Eng/Page 2013 AUPRC CI
    "10.1371/journal.pone.0118432",       # Saito & Rehmsmeier 2015
    "10.1148/radiology.143.1.7063747",    # Hanley & McNeil 1982
    "10.1023/A:1024068626366",            # Nadeau & Bengio 2003
    "10.1162/089976698300017197",         # Dietterich 1998
    "10.1525/collabra.33267",             # Lakens 2022 sample size justification
    "10.2307/2340521",                    # Fisher 1922
]


def crossref(doi):
    url = f"https://api.crossref.org/works/{doi}"
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.loads(r.read().decode("utf-8"))
        m = d.get("message", {})
        authors = m.get("author") or []
        a0 = authors[0] if authors else {}
        return {
            "ok": True,
            "title": (m.get("title") or [""])[0],
            "author_first": f"{a0.get('family','?')}, {a0.get('given','?')}",
            "n_authors": len(authors),
            "container": (m.get("container-title") or [""])[0],
            "year": (m.get("issued", {}).get("date-parts") or [["?"]])[0][0],
            "volume": m.get("volume"),
            "issue": m.get("issue"),
            "page": m.get("page"),
            "crossref_doi": m.get("DOI"),
            "type": m.get("type"),
        }
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": f"{type(e).__name__}: {e}"}


def landing(doi):
    url = f"https://doi.org/{doi}"
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            return {"http": r.status, "final_url": r.geturl()}
    except urllib.error.HTTPError as e:
        return {"http": e.code, "final_url": e.geturl() if hasattr(e, "geturl") else None}
    except Exception as e:  # noqa: BLE001
        return {"http": None, "error": f"{type(e).__name__}: {e}"}


rows = []
for doi in DOIS:
    cr = crossref(doi)
    ld = landing(doi)
    row = {"doi": doi, "crossref": cr, "landing": ld}
    rows.append(row)
    tag = "OK " if cr.get("ok") else "GAGAL"
    print(f"{tag} {doi} http={ld.get('http')} | {cr.get('author_first','-')} | "
          f"{cr.get('year','-')} | {str(cr.get('title','-'))[:80]}")

OUT.write_text(json.dumps(rows, indent=1, ensure_ascii=False), encoding="utf-8")
print("\nn =", len(rows), "->", OUT)
print("crossref OK:", sum(1 for r in rows if r["crossref"].get("ok")), "/", len(rows))
