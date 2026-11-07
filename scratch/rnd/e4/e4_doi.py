"""RND-E4 — verifikasi DOI dua lapis (registrasi + metadata) untuk rujukan dokumen E4."""
import json, urllib.request, urllib.error

DOIS = [
    ("Kaufman", "2012", "Leakage in Data Mining: Formulation, Detection, and Avoidance",
     "10.1145/2382577.2382579"),
    ("Kapoor", "2023", "Leakage and the reproducibility crisis in machine-learning-based science",
     "10.1016/j.patter.2023.100804"),
    ("Saito", "2015", "The Precision-Recall Plot Is More Informative than the ROC Plot When "
     "Evaluating Binary Classifiers on Imbalanced Datasets", "10.1371/journal.pone.0118432"),
    ("Angelopoulos", "2021", "A Gentle Introduction to Conformal Prediction and "
     "Distribution-Free Uncertainty Quantification", "10.48550/arXiv.2107.07511"),
    ("Lei", "2018", "Distribution-Free Predictive Inference for Regression",
     "10.1080/01621459.2017.1307116"),
    ("Tatbul", "2018", "Precision and Recall for Time Series", "10.48550/arXiv.1803.03639"),
    ("Page", "1954", "Continuous Inspection Schemes", "10.1093/biomet/41.1-2.100"),
    ("Siffer", "2017", "Anomaly Detection in Streams with Extreme Value Theory",
     "10.1145/3097983.3098144"),
]


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


op = urllib.request.build_opener(NoRedirect)
out = []
for first, yr, title, doi in DOIS:
    rec = dict(penulis=first, tahun=yr, judul=title, doi=doi)
    try:
        r = op.open(urllib.request.Request("https://doi.org/" + doi, method="HEAD"), timeout=25)
        rec["lapis1"] = r.status
    except urllib.error.HTTPError as e:
        rec["lapis1"] = e.code
    except Exception as e:
        rec["lapis1"] = "ERR:" + type(e).__name__
    meta = None
    for base in ("https://api.crossref.org/works/", "https://api.datacite.org/dois/"):
        try:
            r = urllib.request.urlopen(base + doi, timeout=30)
            meta = json.loads(r.read().decode())
            rec["lapis2_sumber"] = "crossref" if "crossref" in base else "datacite"
            rec["lapis2"] = r.status
            break
        except urllib.error.HTTPError as e:
            rec["lapis2_" + ("crossref" if "crossref" in base else "datacite")] = e.code
        except Exception as e:
            rec["lapis2_err"] = type(e).__name__
    if meta:
        m = meta.get("message", meta.get("data", {}).get("attributes", {}))
        t = m.get("title")
        t = t[0] if isinstance(t, list) and t else (t if isinstance(t, str) else None)
        rec["judul_record"] = t
        issued = m.get("issued", {}).get("date-parts", m.get("publicationYear"))
        rec["tahun_record"] = issued[0][0] if isinstance(issued, list) and issued and issued[0] else issued
        au = m.get("author")
        rec["penulis_record"] = (au[0].get("family") if au and isinstance(au[0], dict) else None)
    out.append(rec)
    print(json.dumps(rec, ensure_ascii=False))

json.dump(out, open("/mnt/d/Capstone 1(v2)/scratch/rnd/e4/e4_doi.json", "w"), indent=2)
ok1 = sum(1 for r in out if r.get("lapis1") in (301, 302, 303, 307, 308))
ok2 = sum(1 for r in out if r.get("lapis2") == 200)
print("\nRESUME lapis1_terdaftar=%d/%d lapis2_metadata=%d/%d" % (ok1, len(out), ok2, len(out)))
