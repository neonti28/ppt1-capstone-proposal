#!/usr/bin/env python3
"""RND-E3 — verifikasi rujukan ilmiah dua lapis.

Lapis 1 (registrasi): HEAD ke https://doi.org/<doi> TANPA mengikuti redirect.
  301/302 = terdaftar ; 404 = tidak terdaftar.
Lapis 2 (metadata): GET https://api.crossref.org/works/<doi> ; 200 + judul/tahun
  cocok = identitas bibliografis terverifikasi.
Lapis 3 (akses penerbit): dicatat terpisah, 403/202 = blokir bot, BUKAN DOI palsu.

Keluaran: scratch/rnd/e3/e3_doi.json
"""
import json, ssl, urllib.request, urllib.error

OUT = "/mnt/d/Capstone 1(v2)/scratch/rnd/e3/e3_doi.json"
CTX = ssl.create_default_context()

REFS = [
    dict(key="angelopoulos2021", doi="10.48550/arXiv.2107.07511",
         penulis="Angelopoulos", tahun=2021,
         judul="A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification"),
    dict(key="vovk2005", doi="10.1007/b106715",
         penulis="Vovk", tahun=2005,
         judul="Algorithmic Learning in a Random World"),
    dict(key="lei2018", doi="10.1080/01621459.2017.1307116",
         penulis="Lei", tahun=2018,
         judul="Distribution-Free Predictive Inference for Regression"),
    dict(key="page1954", doi="10.1093/biomet/41.1-2.100",
         penulis="Page", tahun=1954,
         judul="Continuous Inspection Schemes"),
    dict(key="garwood1936", doi="10.1093/biomet/28.3-4.437",
         penulis="Garwood", tahun=1936,
         judul="Fiducial Limits for the Poisson Distribution"),
    dict(key="hawkins1998", doi="10.1007/978-1-4612-1686-5",
         penulis="Hawkins", tahun=1998,
         judul="Cumulative Sum Charts and Charting for Quality Improvement"),
    dict(key="siffer2017", doi="10.1145/3097983.3098144",
         penulis="Siffer", tahun=2017,
         judul="Anomaly Detection in Streams with Extreme Value Theory"),
]


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


NO_REDIR = urllib.request.build_opener(NoRedirect)


def lapis1(doi):
    req = urllib.request.Request(f"https://doi.org/{doi}", method="HEAD",
                                headers={"User-Agent": "rnd-e3-verify/1.0"})
    try:
        with NO_REDIR.open(req, timeout=25) as r:
            return r.status, r.headers.get("Location")
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Location") if e.headers else None
    except Exception as e:
        return None, f"ERR {type(e).__name__}: {e}"


def lapis2(doi):
    """Crossref untuk DOI penerbit, DataCite untuk DOI arXiv (10.48550)."""
    if doi.startswith("10.48550/"):
        api = f"https://api.datacite.org/dois/{doi}"
        try:
            req = urllib.request.Request(api, headers={"User-Agent": "rnd-e3-verify/1.0"})
            with urllib.request.urlopen(req, timeout=30, context=CTX) as r:
                a = json.loads(r.read().decode("utf-8"))["data"]["attributes"]
                return 200, dict(
                    judul=(a.get("titles") or [{}])[0].get("title"),
                    tahun=a.get("publicationYear"),
                    penulis_pertama=((a.get("creators") or [{}])[0].get("familyName")
                                     or (a.get("creators") or [{}])[0].get("name")),
                    kontainer=a.get("publisher"),
                    sumber="datacite",
                )
        except urllib.error.HTTPError as e:
            return e.code, None
        except Exception as e:
            return None, f"ERR {type(e).__name__}: {e}"
    req = urllib.request.Request(f"https://api.crossref.org/works/{doi}",
                                headers={"User-Agent": "rnd-e3-verify/1.0 (mailto:none@example.org)"})
    try:
        with urllib.request.urlopen(req, timeout=30, context=CTX) as r:
            d = json.loads(r.read().decode("utf-8"))["message"]
            return 200, dict(
                judul=d.get("title", [None])[0],
                tahun=(d.get("issued", {}).get("date-parts", [[None]])[0][0]),
                penulis_pertama=((d.get("author") or [{}])[0].get("family")),
                kontainer=(d.get("container-title") or [None])[0],
                sumber="crossref",
            )
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        return None, f"ERR {type(e).__name__}: {e}"


def lapis3(doi):
    req = urllib.request.Request(f"https://doi.org/{doi}",
                                headers={"User-Agent": "Mozilla/5.0 (rnd-e3)"})
    try:
        with urllib.request.urlopen(req, timeout=30, context=CTX) as r:
            return r.status, r.geturl()
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        return None, f"ERR {type(e).__name__}"


hasil = []
for ref in REFS:
    s1, loc = lapis1(ref["doi"])
    s2, meta = lapis2(ref["doi"])
    s3, url = lapis3(ref["doi"])
    terverifikasi = bool(s2 == 200 and isinstance(meta, dict))
    cocok = None
    if terverifikasi:
        cocok = (ref["penulis"].lower() in str(meta["penulis_pertama"]).lower()
                 and str(ref["tahun"]) == str(meta["tahun"]))
    hasil.append(dict(**ref, lapis1_registrasi=s1, location=loc,
                      lapis2_metadata=s2, metadata=meta, lapis3_akses=s3,
                      url_penerbit=url, metadata_terverifikasi=terverifikasi,
                      penulis_tahun_cocok=cocok))
    print(f"{ref['key']:16s} L1={s1} L2={s2} L3={s3} cocok={cocok}")

json.dump(dict(catatan="Lapis1=HEAD doi.org tanpa redirect; Lapis2=api.crossref.org; "
                       "Lapis3=akses penerbit (403/202 = blokir bot, bukan DOI palsu)",
               refs=hasil), open(OUT, "w"), indent=2, ensure_ascii=False)

n_ok = sum(1 for h in hasil if h["metadata_terverifikasi"])
print(f"\n{len(hasil)} rujukan, {n_ok} metadata terverifikasi")
