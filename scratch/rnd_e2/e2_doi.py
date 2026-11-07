"""RND-E2: verifikasi rujukan dua lapis.

Lapis 1 registrasi: HEAD/GET https://doi.org/<doi> TANPA mengikuti redirect.
  301/302 = terdaftar; 404 = tidak terdaftar.
Lapis 2 metadata: GET https://api.crossref.org/works/<doi> -> judul/tahun/penulis pertama.
Lapis 3 akses penerbit TIDAK dipakai sebagai bukti (403/202 = blokir bot).

URL non-DOI diperiksa dengan GET langsung dan judul halaman dicocokkan.

Output: scratch/rnd_e2/e2_doi.json
"""
from __future__ import annotations

import json
import ssl
import urllib.error
import urllib.request
from pathlib import Path

OUT = Path("/mnt/d/Capstone 1(v2)/scratch/rnd_e2")
OUT.mkdir(parents=True, exist_ok=True)

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
UA = {"User-Agent": "Mozilla/5.0 (compatible; RND-E2 protocol reference check)"}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


OPENER_NOREDIR = urllib.request.build_opener(NoRedirect)


def status_noredir(url: str, timeout: int = 25) -> tuple[int | None, str]:
    req = urllib.request.Request(url, headers=UA, method="GET")
    try:
        with OPENER_NOREDIR.open(req, timeout=timeout) as r:
            return r.status, r.headers.get("Location", "") or ""
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Location", "") or ""
    except Exception as e:  # noqa: BLE001
        return None, f"{type(e).__name__}: {e}"


def get_json(url: str, timeout: int = 30):
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
            return r.status, json.loads(r.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:  # noqa: BLE001
        return None, f"{type(e).__name__}: {e}"


def get_text(url: str, timeout: int = 30):
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
            return r.status, r.read(200000).decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:  # noqa: BLE001
        return None, f"{type(e).__name__}: {e}"


DOIS = [
    # protokol nested CV / CV untuk data terstruktur
    ("Varma & Simon 2006", "Bias in error estimation when using cross-validation for model selection", "10.1186/1471-2105-7-91"),
    ("Roberts et al. 2017", "Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure", "10.1111/ecog.02881"),
    ("Bergmeir & Benitez 2012", "On the use of cross-validation for time series predictor evaluation", "10.1016/j.ins.2011.12.028"),
    ("Cerqueira et al. 2020", "Evaluating time series forecasting models: an empirical study on performance estimation methods", "10.1007/s10994-020-05910-7"),
    ("Varoquaux 2018", "Cross-validation failure: small sample sizes lead to large error bars", "10.1016/j.neuroimage.2017.06.061"),
    # conformal
    ("Vovk et al. 2005", "Algorithmic Learning in a Random World", "10.1007/b106715"),
    ("Lei et al. 2018", "Distribution-Free Predictive Inference for Regression", "10.1080/01621459.2017.1307116"),
    ("Barber et al. 2023", "Conformal prediction beyond exchangeability", "10.1214/23-AOS2276"),
    # perubahan level
    ("Page 1954", "Continuous Inspection Schemes", "10.1093/biomet/41.1-2.100"),
    # statistik
    ("DeLong et al. 1988", "Comparing the Areas under Two or More Correlated ROC Curves", "10.2307/2531595"),
    ("Efron 1979", "Bootstrap Methods: Another Look at the Jackknife", "10.1214/aos/1176344552"),
    ("Benjamini & Hochberg 1995", "Controlling the False Discovery Rate", "10.1111/j.2517-6161.1995.tb02031.x"),
    ("Wilson 1927", "Probable Inference, the Law of Succession, and Statistical Inference", "10.1080/01621459.1927.10502953"),
    ("Boyd et al. 2013", "Area under the Precision-Recall Curve: Point Estimates and Confidence Intervals", "10.1007/978-3-642-40994-3_29"),
    ("Saito & Rehmsmeier 2015", "The Precision-Recall Plot Is More Informative than the ROC Plot", "10.1371/journal.pone.0118432"),
    ("Lakens 2022", "Sample Size Justification", "10.1525/collabra.33267"),
    ("Holm 1979", "A Simple Sequentially Rejective Multiple Test Procedure", "10.2307/4615733"),
]

URLS = [
    ("Cawley & Talbot 2010", "On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation",
     "https://www.jmlr.org/papers/v11/cawley10a.html"),
    ("Pineau et al. 2021", "Improving Reproducibility in Machine Learning Research",
     "https://www.jmlr.org/papers/v22/20-303.html"),
    ("Angelopoulos & Bates 2021", "A Gentle Introduction to Conformal Prediction",
     "https://arxiv.org/abs/2107.07511"),
    ("Romano et al. 2019", "Conformalized Quantile Regression",
     "https://arxiv.org/abs/1905.03222"),
]

res = {"doi": {}, "url": {}}

for label, title_expect, doi in DOIS:
    reg_status, loc = status_noredir(f"https://doi.org/{doi}")
    cr_status, cr = get_json(f"https://api.crossref.org/works/{doi}")
    meta = None
    if isinstance(cr, dict) and cr.get("message"):
        m = cr["message"]
        auth = m.get("author") or []
        meta = {
            "title": (m.get("title") or [""])[0][:160],
            "first_author": (auth[0].get("family", "") if auth else ""),
            "year": (m.get("issued", {}).get("date-parts", [[None]])[0][0]),
            "container": (m.get("container-title") or [""])[0][:80],
        }
    res["doi"][doi] = {
        "label": label,
        "expected_title": title_expect,
        "registrasi_status": reg_status,
        "registrasi_location": loc[:120],
        "crossref_status": cr_status,
        "crossref_meta": meta,
    }
    print(f"{doi:42s} reg={reg_status} crossref={cr_status} "
          f"auth={meta['first_author'] if meta else '?'} "
          f"year={meta['year'] if meta else '?'} | {label}")

for label, title_expect, url in URLS:
    st, body = get_text(url)
    title_ok = None
    if isinstance(body, str) and body:
        low = body.lower()
        key = title_expect.split(":")[0].lower()[:40]
        title_ok = any(w in low for w in key.split()[:4])
    res["url"][url] = {"label": label, "expected_title": title_expect,
                       "status": st, "judul_cocok": title_ok,
                       "bytes": len(body) if isinstance(body, str) else 0}
    print(f"{st}  {url}  cocok={title_ok}  {label}")

(OUT / "e2_doi.json").write_text(json.dumps(res, indent=2, ensure_ascii=False))
print("\ntertulis:", OUT / "e2_doi.json")
