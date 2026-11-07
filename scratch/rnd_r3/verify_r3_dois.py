"""Verifikasi DOI kandidat rujukan R3 lewat Crossref (judul + tahun + penulis pertama).

Output: out_doi_r3.json
"""
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

CAND = [
    # inti dekomposisi
    ("Dragomiretskiy2014_VMD", "10.1109/TSP.2013.2288675"),
    ("Huang1998_EMD", "10.1098/rspa.1998.0193"),
    ("Torrence1998_Wavelet", "10.1175/1520-0477(1998)079<0061:APGTWA>2.0.CO;2"),
    # kernel / kemiripan
    ("Cortes1995_SVM", "10.1007/BF00994018"),
    ("Rakthanmanon2012_DTW", "10.1145/2339530.2339576"),
    ("Yeh2016_MatrixProfileI", "10.1109/ICDM.2016.0179"),
    ("Yeh2016_MatrixProfileI_wrong_prior_attempt", "10.1109/ICDM.2016.0172"),
    # metaheuristik
    ("Mirjalili2014_GWO", "10.1016/j.advengsoft.2013.12.007"),
    ("Mirjalili2016_WOA", "10.1016/j.advengsoft.2016.01.008"),
    # bearing fault diagnosis + VMD
    ("RamaKrishna2018_VMD_SVM", "10.1088/1757-899X/310/1/012076"),
    ("LiLin2023_VMD_param_opt", "10.3390/electronics12061290"),
    ("Gai2020_HGWO_VMD", "10.1016/j.measurement.2020.107901"),
    ("Zhang2021_VMD_CGWO_SVR", "10.1016/j.knosys.2021.107297"),
    ("HeDeqiang2023_IGWO_AVMD", "10.1088/1361-6501/acd713"),
    # drilling vibration
    ("Reckmann2010_MWD_failure", "10.2118/127413-MS"),
    ("Mal2022_stuckpipe_ML", "10.2118/208778-MS"),
]

out = []
for tag, doi in CAND:
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
    rec = {"tag": tag, "doi": doi, "http": None, "year": None,
           "first_author": None, "title": None, "container": None}
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "rnd-r3-verify/1.0 (mailto:neonti@example.org)"})
        with urllib.request.urlopen(req, timeout=30) as r:
            j = json.load(r)["message"]
            rec["http"] = r.status
            rec["title"] = (j.get("title") or [""])[0]
            rec["container"] = (j.get("container-title") or [""])[0]
            for k in ("published-print", "published-online", "issued"):
                if j.get(k, {}).get("date-parts"):
                    rec["year"] = j[k]["date-parts"][0][0]
                    break
            au = j.get("author") or [{}]
            rec["first_author"] = " ".join(
                x for x in [au[0].get("family", ""), au[0].get("given", "")] if x)
    except Exception as e:
        rec["http"] = "ERR " + str(e)[:90]
    out.append(rec)
    print(f"{tag} | {rec['http']} | {rec['year']} | {rec['first_author']} | {(rec['title'] or '')[:88]}")
    time.sleep(0.4)

Path(__file__).parent.joinpath("out_doi_r3.json").write_text(
    json.dumps(out, indent=1, ensure_ascii=False))
