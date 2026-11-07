"""RND-R8 -- agregasi hasil + verifikasi DOI dua lapis (registrasi + metadata)."""
import json, urllib.request, urllib.error, ssl
import numpy as np

BASE = "/mnt/d/Capstone 1(v2)"
OUT = f"{BASE}/scratch/rnd/r8"

agg = {"task": {}}
for task in ["hyd", "shk", "toolwear", "stuck"]:
    d = json.load(open(f"{OUT}/r8_{task}.json"))
    rows = d["rows"]
    per = {}
    for mdl in sorted({r["model"] for r in rows}):
        sub = [r for r in rows if r["model"] == mdl]
        if "far24_kalender" in sub[0]:
            per[mdl] = dict(
                n_fold=len(sub),
                per_fold={r["fold"]: dict(
                    precision=r["rows"]["precision"], recall=r["rows"]["recall"],
                    fp=r["rows"]["fp"], tp=r["rows"]["tp"], n_pos=r["rows"]["n_pos"],
                    far24=r["far24_kalender"], far24_kej=r["far24_kalender_kejadian"],
                    cakupan=r["cakupan"], prev=r["prev"],
                    lead=r["lead"], separuh=r["separuh"],
                    thr=r.get("thr_kalibrasi"), h=r.get("h_terpilih"),
                    auprc=r.get("auprc"), auc=r.get("auc"),
                ) for r in sub},
                fp_total=int(sum(r["rows"]["fp"] for r in sub)),
                tp_total=int(sum(r["rows"]["tp"] for r in sub)),
                menit_alarm_total=int(sum(r["rows"]["menit_alarm"] for r in sub)),
                fp_kejadian_total=int(sum(r["events"]["fp_kejadian"] for r in sub)),
                n_onset=int(sum(r["lead"]["n_onset"] for r in sub)),
                n_diperingatkan=int(sum(r["lead"]["n_diperingatkan"] for r in sub)),
                fold_far_le6=int(sum(1 for r in sub if r["far24_kalender"] <= 6.0)),
                fold_recall_gt0=int(sum(1 for r in sub if (r["rows"]["recall"] or 0) > 0)),
            )
        else:
            per[mdl] = dict(
                n_fold=len(sub),
                per_fold={r["fold"]: dict(bacc=r["bacc"], f1=r["f1"], precision=r["precision"],
                                          recall=r["recall"], tp=r["tp"], fp=r["fp"],
                                          fn=r["fn"], thr=r["thr"], C=r["C"], prev=r["prev"],
                                          delta_bacc=r["delta_bacc"]) for r in sub},
                tp_total=int(sum(r["tp"] for r in sub)),
                fp_total=int(sum(r["fp"] for r in sub)),
                fn_total=int(sum(r["fn"] for r in sub)),
            )
    agg["task"][task] = dict(elapsed_s=d["elapsed_s"], alpha_budget=d["alpha_budget"],
                             seed=d["seed"], model=per)

# ---- turunan yang dipakai dokumen (dihitung di sini, bukan di kepala) ----
der = {}
h = agg["task"]["hyd"]["model"]
der["hyd"] = dict(
    fp_rule=h["rule_kanal"]["fp_total"], fp_stat=h["stat_cusum"]["fp_total"],
    fp_H1=h["H1_stat_dan_rule"]["fp_total"],
    potong_FP_pct=round(100 * (1 - h["H1_stat_dan_rule"]["fp_total"] / h["rule_kanal"]["fp_total"]), 2),
    potong_FP_vs_stat_pct=round(100 * (1 - h["H1_stat_dan_rule"]["fp_total"] / h["stat_cusum"]["fp_total"]), 2),
    tp_rule=h["rule_kanal"]["tp_total"], tp_H1=h["H1_stat_dan_rule"]["tp_total"],
    tp_stat=h["stat_cusum"]["tp_total"],
    ingat_rule=h["rule_kanal"]["n_diperingatkan"], ingat_H1=h["H1_stat_dan_rule"]["n_diperingatkan"],
    onset=h["H1_stat_dan_rule"]["n_onset"],
    far_rule=[min(v["far24"] for v in h["rule_kanal"]["per_fold"].values()),
              max(v["far24"] for v in h["rule_kanal"]["per_fold"].values())],
    far_H1=[min(v["far24"] for v in h["H1_stat_dan_rule"]["per_fold"].values()),
            max(v["far24"] for v in h["H1_stat_dan_rule"]["per_fold"].values())],
)
s = agg["task"]["shk"]["model"]
der["shk"] = dict(
    fp_ML=s["ML_saja"]["fp_total"], fp_H2=s["H2_ML_dan_stat"]["fp_total"],
    tp_ML=s["ML_saja"]["tp_total"], tp_H2=s["H2_ML_dan_stat"]["tp_total"],
    potong_FP_pct=round(100 * (1 - s["H2_ML_dan_stat"]["fp_total"] / s["ML_saja"]["fp_total"]), 2),
    drop_TP_pct=round(100 * (1 - s["H2_ML_dan_stat"]["tp_total"] / s["ML_saja"]["tp_total"]), 2),
    auprc=[v["auprc"] for v in s["ML_saja"]["per_fold"].values()],
    prev=[v["prev"] for v in s["ML_saja"]["per_fold"].values()],
)
t = agg["task"]["toolwear"]["model"]
der["toolwear"] = dict(
    bacc_default=[v["bacc"] for v in t["ML_default"]["per_fold"].values()],
    bacc_gwo_bacc=[v["bacc"] for v in t["H3b_GWO_objBacc"]["per_fold"].values()],
    bacc_gwo_f1=[v["bacc"] for v in t["H3a_GWO_objF1"]["per_fold"].values()],
    tp_default=t["ML_default"]["tp_total"], fp_default=t["ML_default"]["fp_total"],
    tp_gwo_bacc=t["H3b_GWO_objBacc"]["tp_total"], fp_gwo_bacc=t["H3b_GWO_objBacc"]["fp_total"],
    n_uji=t["ML_default"]["per_fold"].__len__(),
    n_window=int(sum(v["tp"] + v["fp"] + v["fn"] for v in t["ML_default"]["per_fold"].values()
                     if True)),
)
k = agg["task"]["stuck"]["model"]
der["stuck"] = dict(
    fp_ML=k["ML_saja"]["fp_total"], fp_H4=k["H4_tiga_komponen"]["fp_total"],
    tp_ML=k["ML_saja"]["tp_total"], tp_H4=k["H4_tiga_komponen"]["tp_total"],
    recall_max_semua=max(max((v["recall"] or 0) for v in m["per_fold"].values()) for m in k.values()),
    onset=k["H4_tiga_komponen"]["n_onset"],
    ingat_H4=k["H4_tiga_komponen"]["n_diperingatkan"],
)
agg["turunan"] = der
json.dump(agg, open(f"{OUT}/r8_agg.json", "w"), indent=1)
print(json.dumps(der, indent=1))

# ------------------------------ DOI dua lapis ------------------------------
REFS = [
    ("10.1093/biomet/41.1-2.100", "Page", 1954),
    ("10.1007/b106715", "Vovk", 2005),
    ("10.1109/ICDM.2008.17", "Liu", 2008),
    ("10.1016/j.advengsoft.2013.12.007", "Mirjalili", 2014),
    ("10.48550/arXiv.1803.03639", "Tatbul", 2018),
    ("10.1145/1541880.1541882", "Chandola", 2009),
]
ctx = ssl.create_default_context()


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **kw):
        return None


opener = urllib.request.build_opener(NoRedirect)


def lapis1(doi):
    url = f"https://doi.org/{doi}"
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "r8-check/1.0"})
    try:
        opener.open(req, timeout=25)
        return "200"
    except urllib.error.HTTPError as e:
        return str(e.code)
    except Exception as e:
        return f"ERR:{type(e).__name__}"


def lapis2(doi):
    for base in ("https://api.crossref.org/works/", "https://api.datacite.org/dois/"):
        try:
            r = urllib.request.urlopen(base + doi, timeout=30, context=ctx)
            j = json.loads(r.read().decode())
            if "message" in j and "title" in j["message"]:
                m = j["message"]
                return dict(status=200, sumber="crossref", judul=(m.get("title") or [""])[0],
                            tahun=(m.get("issued", {}).get("date-parts", [[None]])[0][0]),
                            penulis=(m.get("author") or [{}])[0].get("family"))
            if "data" in j:
                m = j["data"]["attributes"]
                return dict(status=200, sumber="datacite", judul=(m.get("titles") or [{}])[0].get("title"),
                            tahun=m.get("publicationYear"),
                            penulis=(m.get("creators") or [{}])[0].get("familyName"))
        except Exception as e:
            last = f"{type(e).__name__}"
    return dict(status="gagal", error=locals().get("last"))


doi_out = []
for doi, first, yr in REFS:
    r1 = lapis1(doi); r2 = lapis2(doi)
    rec = dict(doi=doi, penulis_pertama=first, tahun_klaim=yr, lapis1_registrasi=r1, lapis2=r2)
    doi_out.append(rec)
    print(doi, r1, r2)
json.dump(doi_out, open(f"{OUT}/r8_doi.json", "w"), indent=1)
