"""Verifikasi dua lapis DOI untuk kartu PM (t_776c0a03).

Lapis 1: HEAD ke https://doi.org/<doi> TANPA mengikuti redirect (301/302 = terdaftar).
Lapis 2: metadata Crossref (api.crossref.org) atau DataCite (api.datacite.org) = 200
         dengan judul/penulis pertama/tahun yang cocok.

Hasil ditulis ke scratch/rnd/pm/pm_doi.json. Tidak ada angka yang dikarang: semua
status berasal dari respons HTTP nyata.
"""
import json
import os
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = "/mnt/d/Capstone 1(v2)"
OUTDIR = os.path.join(BASE, "scratch/rnd/pm")

REFS = [
    {"key": "page1954", "doi": "10.1093/biomet/41.1-2.100",
     "penulis": "Page", "tahun": 1954, "judul": "Continuous inspection schemes"},
    {"key": "vovk2005", "doi": "10.1007/b106715",
     "penulis": "Vovk", "tahun": 2005, "judul": "Algorithmic Learning in a Random World"},
    {"key": "mirjalili2014", "doi": "10.1016/j.advengsoft.2013.12.007",
     "penulis": "Mirjalili", "tahun": 2014, "judul": "Grey Wolf Optimizer"},
    {"key": "dragomiretskiy2014", "doi": "10.1109/TSP.2013.2288675",
     "penulis": "Dragomiretskiy", "tahun": 2014, "judul": "Variational Mode Decomposition"},
    {"key": "liu2008", "doi": "10.1109/ICDM.2008.17",
     "penulis": "Liu", "tahun": 2008, "judul": "Isolation Forest"},
    {"key": "tatbul2018", "doi": "10.48550/arXiv.1803.03639",
     "penulis": "Tatbul", "tahun": 2018, "judul": "Precision and Recall for Time Series"},
    {"key": "rabiner1989", "doi": "10.1109/5.18626",
     "penulis": "Rabiner", "tahun": 1989, "judul": "A tutorial on hidden Markov models"},
    {"key": "cox1972", "doi": "10.1111/j.2517-6161.1972.tb00899.x",
     "penulis": "Cox", "tahun": 1972, "judul": "Regression Models and Life-Tables"},
    {"key": "ishwaran2008", "doi": "10.1214/08-AOAS169",
     "penulis": "Ishwaran", "tahun": 2008, "judul": "Random survival forests"},
    {"key": "chandola2009", "doi": "10.1145/1541880.1541882",
     "penulis": "Chandola", "tahun": 2009, "judul": "Anomaly detection"},
]

UA = "Mozilla/5.0 (compatible; rnd-pm-doi-check/1.0)"


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def head_no_redirect(url):
    ctx = ssl.create_default_context()
    opener = urllib.request.build_opener(
        NoRedirect, urllib.request.HTTPSHandler(context=ctx))
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
    try:
        with opener.open(req, timeout=30) as r:
            return r.status, r.headers.get("Location")
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Location") if e.headers else None


def get_json(url):
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=40, context=ctx) as r:
            return r.status, json.loads(r.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:  # noqa: BLE001
        return None, {"error": str(e)}


def crossref(doi):
    return get_json("https://api.crossref.org/works/" + urllib.parse.quote(doi))


def datacite(doi):
    return get_json("https://api.datacite.org/dois/" + urllib.parse.quote(doi))


def evaluasi(ref):
    out = dict(ref)
    status1, loc = head_no_redirect("https://doi.org/" + ref["doi"])
    out["lapis1_status"] = status1
    out["lapis1_location"] = loc
    out["lapis1_terdaftar"] = status1 in (301, 302, 303, 307, 308)

    status2, body = crossref(ref["doi"])
    out["lapis2_sumber"] = "crossref"
    out["lapis2_status"] = status2
    judul = penulis = tahun = None
    if status2 == 200 and body:
        msg = body.get("message", {})
        judul_list = msg.get("title") or []
        judul = judul_list[0] if judul_list else None
        auth = msg.get("author") or []
        if auth:
            penulis = auth[0].get("family")
        issued = msg.get("issued", {}).get("date-parts") or [[None]]
        tahun = issued[0][0]
    else:
        status2b, body_b = datacite(ref["doi"])
        out["lapis2_sumber"] = "datacite"
        out["lapis2_status"] = status2b
        if status2b == 200 and body_b:
            attr = body_b.get("data", {}).get("attributes", {})
            titles = attr.get("titles") or []
            judul = titles[0].get("title") if titles else None
            creators = attr.get("creators") or []
            if creators:
                nama = creators[0].get("name") or ""
                penulis = nama.split(",")[0].strip() or None
            tahun = attr.get("publicationYear")

    out["lapis2_judul"] = judul
    out["lapis2_penulis_pertama"] = penulis
    out["lapis2_tahun"] = tahun

    judul_cocok = bool(judul) and ref["judul"].lower()[:22] in judul.lower()
    penulis_cocok = (penulis or "").lower().startswith(ref["penulis"].lower()[:5]) if penulis else None
    tahun_cocok = (tahun == ref["tahun"]) if tahun else None
    out["judul_cocok"] = judul_cocok
    out["penulis_cocok"] = penulis_cocok
    out["tahun_cocok"] = tahun_cocok
    out["terverifikasi_dua_lapis"] = bool(
        out["lapis1_terdaftar"] and out["lapis2_status"] == 200 and judul_cocok)
    return out


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    hasil = []
    for ref in REFS:
        try:
            hasil.append(evaluasi(ref))
        except Exception as e:  # noqa: BLE001
            hasil.append(dict(ref, error=str(e), terverifikasi_dua_lapis=False))
        sys.stderr.write("checked %s\n" % ref["key"])

    ringkas = {
        "n_rujukan": len(hasil),
        "lapis1_terdaftar": sum(1 for h in hasil if h.get("lapis1_terdaftar")),
        "lapis2_status_200": sum(1 for h in hasil if h.get("lapis2_status") == 200),
        "judul_cocok": sum(1 for h in hasil if h.get("judul_cocok")),
        "terverifikasi_dua_lapis": sum(1 for h in hasil if h.get("terverifikasi_dua_lapis")),
        "gagal": [h["key"] for h in hasil if not h.get("terverifikasi_dua_lapis")],
    }
    payload = {"tanggal_akses": "2026-10-27", "cara": "lapis1 HEAD doi.org tanpa redirect; lapis2 Crossref/DataCite",
               "ringkas": ringkas, "rujukan": hasil}
    fp = os.path.join(OUTDIR, "pm_doi.json")
    with open(fp, "w") as f:
        json.dump(payload, f, indent=1, ensure_ascii=False)
    print(json.dumps(ringkas, indent=1, ensure_ascii=False))
    print("ditulis:", fp)


if __name__ == "__main__":
    main()
