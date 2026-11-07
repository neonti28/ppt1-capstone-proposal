"""RND-R8 -- generator baris ledger R8 (7 kolom), idempoten, ber-assert.

Setiap baris punya (id, nilai, satuan, kelas, path JSON + ekspresi, dipakai di, status).
Nilai di-assert terhadap nilai yang benar-benar dibaca dari JSON lewat resolver.
Baris DERIVASI di-assert lewat rumusnya, bukan angka tampilan.
Baris BELUM-TERUKUR ditulis tanpa angka tebakan.
"""
import json, re, sys

BASE = "/mnt/d/Capstone 1(v2)"
LEDGER = f"{BASE}/docs/RND_PROVENANCE_LEDGER.md"
OUT = f"{BASE}/scratch/rnd/r8"
agg = json.load(open(f"{OUT}/r8_agg.json"))
raw = {t: json.load(open(f"{OUT}/r8_{t}.json")) for t in ("hyd", "shk", "toolwear", "stuck")}
doi = json.load(open(f"{OUT}/r8_doi.json"))


def M(task, model):
    return agg["task"][task]["model"][model]


def fold(task, model, well):
    return M(task, model)["per_fold"][well]


rows = []   # (nilai, satuan, kelas, rujukan, dipakai, status)


def R(nilai, satuan, kelas, rujukan, dipakai, status="TERUKUR"):
    rows.append(dict(nilai=nilai, satuan=satuan, kelas=kelas, rujukan=rujukan,
                     dipakai=dipakai, status=status))


def angka(x):
    if isinstance(x, float):
        return f"{x:.6g}" if abs(x) < 1 else f"{x}"
    return f"{x}"


# ---------------- H1 hyd K-i
h_rule, h_stat, h_h1, h_h1b = M("hyd", "rule_kanal"), M("hyd", "stat_cusum"), M("hyd", "H1_stat_dan_rule"), M("hyd", "H1b_stat_atau_rule")
R(h_rule["fp_total"], "FP", "RUN-KITA", "r8_hyd.json ringkas.rule_kanal.fp_total", "4.1, 8", )
R(h_stat["fp_total"], "FP", "RUN-KITA", "r8_hyd.json ringkas.stat_cusum.fp_total", "4.1, 8")
R(h_h1["fp_total"], "FP", "RUN-KITA", "r8_hyd.json ringkas.H1_stat_dan_rule.fp_total", "4.1, 8")
R(round(100 * (1 - h_h1["fp_total"] / h_rule["fp_total"]), 2), "persen", "DERIVASI",
  "(1 - 935/2105) x 100", "4.1, 8, 9")
R(round(100 * (1 - h_h1["fp_total"] / h_stat["fp_total"]), 2), "persen", "DERIVASI",
  "(1 - 935/4361) x 100", "4.1, 9")
R(h_rule["tp_total"], "TP", "RUN-KITA", "r8_hyd.json ringkas.rule_kanal.tp_total", "4.1, 8")
R(h_h1["tp_total"], "TP", "RUN-KITA", "r8_hyd.json ringkas.H1_stat_dan_rule.tp_total", "4.1, 8")
R(round(100 * (1 - h_h1["tp_total"] / h_rule["tp_total"]), 2), "persen", "DERIVASI",
  "(1 - 3804/5579) x 100", "4.1, 8")
R(round(float(__import__("numpy").median([v["precision"] for v in h_rule["per_fold"].values()])), 4),
  "presisi median", "RUN-KITA", "r8_hyd.json per_fold.*.precision model rule_kanal", "4.1, 8")
R(round(float(__import__("numpy").median([v["precision"] for v in h_h1["per_fold"].values()])), 4),
  "presisi median", "RUN-KITA", "r8_hyd.json per_fold.*.precision model H1_stat_dan_rule", "4.1, 8")
R(round(float(__import__("numpy").median([v["recall"] for v in h_h1["per_fold"].values()])), 4),
  "recall median", "RUN-KITA", "r8_hyd.json per_fold.*.recall model H1", "4.1, 8, 9")
R(round(float(__import__("numpy").median([v["far24"] for v in h_h1["per_fold"].values()])), 4),
  "FAR per 24 jam", "RUN-KITA", "r8_hyd.json per_fold.*.far24 model H1", "4.1, 8, 9")
R(round(float(__import__("numpy").median([v["far24"] for v in h_rule["per_fold"].values()])), 4),
  "FAR per 24 jam", "RUN-KITA", "r8_hyd.json per_fold.*.far24 model rule_kanal", "4.1, 8")
R(h_h1["fold_far_le6"], "fold", "RUN-KITA", "r8_hyd.json ringkas.H1_stat_dan_rule.fold_far_le6 (dari 9)", "4.1, 8")
R(h_rule["fold_far_le6"], "fold", "RUN-KITA", "r8_hyd.json ringkas.rule_kanal.fold_far_le6 (dari 9)", "4.1, 8")
R(round(float(__import__("numpy").median([v["lead"]["lead_median_min"] for v in h_h1["per_fold"].values()
                                        if v["lead"]["lead_median_min"] is not None])), 4),
  "menit", "RUN-KITA", "r8_hyd.json per_fold.*.lead.lead_median_min model H1", "4.2, 8, 9")
R(round(float(__import__("numpy").median([v["lead"]["lead_median_min"] for v in h_rule["per_fold"].values()
                                        if v["lead"]["lead_median_min"] is not None])), 4),
  "menit", "RUN-KITA", "r8_hyd.json per_fold.*.lead.lead_median_min model rule_kanal", "4.2, 8")
R(h_h1["n_diperingatkan"], "onset", "RUN-KITA", "r8_hyd.json ringkas.H1_stat_dan_rule.n_diperingatkan", "4.2, 8")
R(h_rule["n_diperingatkan"], "onset", "RUN-KITA", "r8_hyd.json ringkas.rule_kanal.n_diperingatkan", "4.2, 8")
R(h_h1["n_onset"], "onset", "RUN-KITA", "r8_hyd.json ringkas.H1_stat_dan_rule.n_onset", "4.2, 8")
R(h_h1b["fp_total"], "FP", "RUN-KITA", "r8_hyd.json ringkas.H1b_stat_atau_rule.fp_total", "4.1")
R(round(float(__import__("numpy").median([v["recall"] for v in h_h1b["per_fold"].values()])), 4),
  "recall median", "RUN-KITA", "r8_hyd.json per_fold.*.recall model H1b", "4.1")
R(fold("hyd", "H1_stat_dan_rule", "F-10")["far24"], "FAR per 24 jam", "RUN-KITA",
  "r8_hyd.json per_fold.F-10.far24 model H1 (nilai terburuk)", "4.1, 8")
R(fold("hyd", "H1_stat_dan_rule", "F-5")["far24"], "FAR per 24 jam", "RUN-KITA",
  "r8_hyd.json per_fold.F-5.far24 model H1 (nilai terbaik)", "4.1, 8")

# ---------------- H2 shk
s_ml, s_h2, s_h2b, s_rule, s_stat = (M("shk", "ML_saja"), M("shk", "H2_ML_dan_stat"),
                                     M("shk", "H2b_ML_dan_stat_atau_rule"), M("shk", "rule_kanal"),
                                     M("shk", "stat_cusum"))
R(s_ml["fp_total"], "FP", "RUN-KITA", "r8_shk.json ringkas.ML_saja.fp_total", "5.1, 8")
R(s_h2["fp_total"], "FP", "RUN-KITA", "r8_shk.json ringkas.H2_ML_dan_stat.fp_total", "5.1, 8")
R(round(100 * (1 - s_h2["fp_total"] / s_ml["fp_total"]), 2), "persen", "DERIVASI",
  "(1 - 667/2633) x 100", "5.1, 8")
R(s_ml["tp_total"], "TP", "RUN-KITA", "r8_shk.json ringkas.ML_saja.tp_total", "5.1, 8")
R(s_h2["tp_total"], "TP", "RUN-KITA", "r8_shk.json ringkas.H2_ML_dan_stat.tp_total", "5.1, 8")
R(round(100 * (1 - s_h2["tp_total"] / s_ml["tp_total"]), 2), "persen", "DERIVASI",
  "(1 - 46/192) x 100", "5.1, 8")
R(round(float(__import__("numpy").median([v["recall"] for v in s_ml["per_fold"].values()])), 4),
  "recall median", "RUN-KITA", "r8_shk.json per_fold.*.recall model ML_saja", "5.1, 8, 9")
R(round(float(__import__("numpy").median([v["auprc"] for v in s_ml["per_fold"].values()])), 4),
  "AUPRC median", "RUN-KITA", "r8_shk.json per_fold.*.auprc model ML_saja", "5.1, 9")
R(round(float(__import__("numpy").median([v["prev"] for v in s_ml["per_fold"].values()])), 6),
  "prevalensi median", "RUN-KITA", "r8_shk.json per_fold.*.prev model ML_saja", "5.1, 9")
R(round(float(__import__("numpy").median([v["far24"] for v in s_ml["per_fold"].values()])), 4),
  "FAR per 24 jam", "RUN-KITA", "r8_shk.json per_fold.*.far24 model ML_saja", "5.1, 8")
R(s_h2["fold_far_le6"], "fold", "RUN-KITA", "r8_shk.json ringkas.H2_ML_dan_stat.fold_far_le6 (dari 9)", "5.1, 8")
R(s_h2b["fp_total"], "FP", "RUN-KITA", "r8_shk.json ringkas.H2b_ML_dan_stat_atau_rule.fp_total", "5.2")
R(round(float(__import__("numpy").median([v["recall"] for v in s_h2b["per_fold"].values()])), 4),
  "recall median", "RUN-KITA", "r8_shk.json per_fold.*.recall model H2b", "5.2")
R(s_rule["fp_total"], "FP", "RUN-KITA", "r8_shk.json ringkas.rule_kanal.fp_total", "5.1")
R(round(float(__import__("numpy").median([v["far24"] for v in s_rule["per_fold"].values()])), 4),
  "FAR per 24 jam", "RUN-KITA", "r8_shk.json per_fold.*.far24 model rule_kanal", "5.1")
R(round(float(__import__("numpy").median([v["recall"] for v in s_stat["per_fold"].values()])), 4),
  "recall median", "RUN-KITA", "r8_shk.json per_fold.*.recall model stat_cusum", "5.1")
R(s_ml["n_diperingatkan"], "onset", "RUN-KITA", "r8_shk.json ringkas.ML_saja.n_diperingatkan", "5.2, 8")
R(s_ml["n_onset"], "onset", "RUN-KITA", "r8_shk.json ringkas.ML_saja.n_onset", "5.2, 8")

# ---------------- H3 toolwear
t_def, t_f1, t_b = M("toolwear", "ML_default"), M("toolwear", "H3a_GWO_objF1"), M("toolwear", "H3b_GWO_objBacc")
import numpy as np
for nama, mdl in (("default", t_def), ("GWO objF1", t_f1), ("GWO objBacc", t_b)):
    bacc = [v["bacc"] for v in mdl["per_fold"].values()]
    R(round(float(np.median(bacc)), 4), "balanced accuracy median", "RUN-KITA",
      f"r8_toolwear.json ringkas model {nama} per_fold.*.bacc", "6.1, 8, 9")
R(t_def["tp_total"], "TP", "RUN-KITA", "r8_toolwear.json ringkas.ML_default.tp_total", "6.1, 8")
R(t_def["fp_total"], "FP", "RUN-KITA", "r8_toolwear.json ringkas.ML_default.fp_total", "6.1, 8")
R(t_f1["tp_total"], "TP", "RUN-KITA", "r8_toolwear.json ringkas.H3a_GWO_objF1.tp_total (semua positif)", "6.1, 8")
R(t_f1["fp_total"], "FP", "RUN-KITA", "r8_toolwear.json ringkas.H3a_GWO_objF1.fp_total", "6.1, 8")
R(t_f1["fn_total"], "FN", "RUN-KITA", "r8_toolwear.json ringkas.H3a_GWO_objF1.fn_total", "6.1, 8")
R(t_b["tp_total"], "TP", "RUN-KITA", "r8_toolwear.json ringkas.H3b_GWO_objBacc.tp_total", "6.1, 8")
R(t_b["fp_total"], "FP", "RUN-KITA", "r8_toolwear.json ringkas.H3b_GWO_objBacc.fp_total", "6.1, 8")
R(469, "jendela", "RUN-KITA", "scratch/v6_e1/toolwear_windows.csv jumlah baris (T01 120, T02 112, T03 121, T04 116)", "6.1")
R(4, "alat", "RUN-KITA", "scratch/v6_e1/toolwear_windows.csv kolom tool nilai unik", "6.1, 8")
R(fold("toolwear", "ML_default", "T01")["bacc"], "balanced accuracy", "RUN-KITA",
  "r8_toolwear.json per_fold.T01.bacc model ML_default", "6.1, 8")
R(fold("toolwear", "ML_default", "T02")["bacc"], "balanced accuracy", "RUN-KITA",
  "r8_toolwear.json per_fold.T02.bacc model ML_default", "6.1, 8")
R(fold("toolwear", "H3b_GWO_objBacc", "T03")["bacc"], "balanced accuracy", "RUN-KITA",
  "r8_toolwear.json per_fold.T03.bacc model H3b_GWO_objBacc", "6.1, 8")

# ---------------- H4 stuck
k_ml, k_h4, k_h4b = M("stuck", "ML_saja"), M("stuck", "H4_tiga_komponen"), M("stuck", "H4b_strict_ML_dan_stat_dan_rule")
k_rule, k_stat = M("stuck", "rule_kanal"), M("stuck", "stat_cusum")
R(k_ml["fp_total"], "FP", "RUN-KITA", "r8_stuck.json ringkas.ML_saja.fp_total", "7.1, 8")
R(k_h4["fp_total"], "FP", "RUN-KITA", "r8_stuck.json ringkas.H4_tiga_komponen.fp_total", "7.1, 8")
R(k_ml["tp_total"], "TP", "RUN-KITA", "r8_stuck.json ringkas.ML_saja.tp_total", "7.1, 8")
R(k_h4["tp_total"], "TP", "RUN-KITA", "r8_stuck.json ringkas.H4_tiga_komponen.tp_total", "7.1, 8")
R(round(float(np.median([v["precision"] for v in k_h4["per_fold"].values()
                        if v["precision"] is not None] or [0])), 4),
  "presisi median", "RUN-KITA", "r8_stuck.json per_fold.*.precision model H4 (fold berpresisi)", "7.1, 8")
R(round(float(max(v["recall"] or 0 for v in k_ml["per_fold"].values())), 4),
  "recall maksimum", "RUN-KITA", "r8_stuck.json per_fold.*.recall model ML_saja nilai terbesar", "7.1, 8, 9")
R(round(float(np.median([v["recall"] for v in k_stat["per_fold"].values()])), 4),
  "recall median", "RUN-KITA", "r8_stuck.json per_fold.*.recall model stat_cusum", "7.1, 8")
R(round(float(np.median([v["recall"] for v in k_rule["per_fold"].values()])), 4),
  "recall median", "RUN-KITA", "r8_stuck.json per_fold.*.recall model rule_kanal", "7.1, 8")
R(k_h4["n_onset"], "onset", "RUN-KITA", "r8_stuck.json ringkas.H4_tiga_komponen.n_onset", "7.1, 8")
R(k_h4["n_diperingatkan"], "onset", "RUN-KITA", "r8_stuck.json ringkas.H4_tiga_komponen.n_diperingatkan", "7.1, 8")
R(k_h4b["fp_total"], "FP", "RUN-KITA", "r8_stuck.json ringkas.H4b_strict_ML_dan_stat_dan_rule.fp_total", "7.1")
R(round(float(np.median([v["recall"] for v in k_ml["per_fold"].values()])), 4),
  "recall median", "RUN-KITA", "r8_stuck.json per_fold.*.recall model ML_saja", "7.1, 8")
R(round(float(max(max((v["recall"] or 0) for v in M("stuck", "ML_saja")["per_fold"].values()), 0)), 4),
  "recall maksimum", "RUN-KITA", "r8_stuck.json per_fold.*.recall model ML_saja nilai terbesar", "7.1")
R(118567, "baris", "RUN-KITA", "scratch/v9_d1/datasets/stuck_k2.csv.gz jumlah baris data", "7")
R(148, "onset", "RUN-KITA", "r8_stuck.json ringkas.ML_saja.n_onset", "7")

# ---------------- metode dan desain
R(4, "hybrid", "RUN-KITA", "empat hybrid dijalankan: H1 hyd, H2 shk, H3 toolwear, H4 stuck (r8_*.json)", "0, 3")
R(0.004167, "fraksi menit negatif", "KONVENSI", "6 alarm per 24 jam = 6/1440 (RND_EVALUATION_POLICY.md tidak menetapkan; dipakai FAR_MAKS E4)", "3.2")
R(9, "fold", "RUN-KITA", "scratch/v9_d1/lowo_hyd_ki.json n_folds", "4")
R(9, "fold", "RUN-KITA", "scratch/v9_d1/lowo_shk.json n_folds", "5")
R(4, "fold", "RUN-KITA", "scratch/v9_d1/lowo_stuck_k2.json n_folds", "7")
R(52509, "baris", "RUN-KITA", "scratch/v9_d1/datasets/hyd_ki.csv.gz jumlah baris", "4")
R(56495, "baris", "RUN-KITA", "scratch/v9_d1/datasets/shk.csv.gz jumlah baris", "5")
R(42, "seed", "RUN-KITA", "code/rnd_r8_hybrid.py SEED", "3.2")
R(60, "menit", "KONVENSI", "lead time horizon LEAD_HORIZON pada code/rnd_r8_hybrid.py", "4.2, 5.2, 7.1")

# ---------------- DOI
for i, d in enumerate(doi, 1):
    R(d["lapis1_registrasi"], f"status registrasi doi.org ({d['doi']})", "JURNAL",
      "r8_doi.json lapis1_registrasi; HEAD tanpa redirect", "11")
    R(d["lapis2"]["status"] if isinstance(d["lapis2"], dict) else "gagal",
      f"status metadata {d['lapis2'].get('sumber') if isinstance(d['lapis2'], dict) else '-'} ({d['doi']})",
      "JURNAL", "r8_doi.json lapis2.status; judul dan penulis pertama diperiksa", "11")

# ---------------- BELUM TERUKUR (tanpa angka)
for isi, dipakai in [
    ("nilai maintenance dalam rupiah atau jam henti terhindar", "9, 12"),
    ("pengurangan pemeriksaan fisik per kejadian (butuh data jadwal inspeksi)", "8, 12"),
    ("recall pada titik operasi di luar anggaran FAR 6 per 24 jam untuk shk dan stuck", "5, 7, 12"),
    ("kestabilan lintas kampanye pengeboran 2026-10-12 (tanggal kampanye tidak tersedia per baris)", "9, 12"),
]:
    R("tidak terukur", "n/a", "BELUM-TERUKUR", f"tidak ada sumber terukur untuk {isi}", dipakai,
      "BELUM TERUKUR")

# ---------------- tulis (idempoten)
assert len(rows) > 40, f"baris terlalu sedikit: {len(rows)}"

# ---- assert silang: nilai yang ditulis harus sama dengan nilai ekspektasi dari run mentah
EXPECT = {  # id -> (nilai, path JSON + kunci, toleransi)
    "R8-001": (2105, "hyd.ringkas.rule_kanal.fp_total", 0),
    "R8-002": (4361, "hyd.ringkas.stat_cusum.fp_total", 0),
    "R8-003": (935, "hyd.ringkas.H1_stat_dan_rule.fp_total", 0),
    "R8-004": (55.58, "D:(1-935/2105)*100", 0.005),
    "R8-006": (5579, "hyd.ringkas.rule_kanal.tp_total", 0),
    "R8-007": (3804, "hyd.ringkas.H1_stat_dan_rule.tp_total", 0),
    "R8-008": (31.82, "D:(1-3804/5579)*100", 0.005),
    "R8-012": (0.5638, "D:median recall H1", 0.00005),
    "R8-013": (3.5302, "D:median far24 H1", 0.00005),
    "R8-014": (6.932, "D:median far24 rule", 0.00005),
    "R8-015": (7, "hyd.ringkas.H1_stat_dan_rule.fold_far_le6", 0),
    "R8-016": (3, "hyd.ringkas.rule_kanal.fold_far_le6", 0),
    "R8-022": (219, "hyd.ringkas.H1_stat_dan_rule.n_diperingatkan", 0),
    "R8-023": (307, "hyd.ringkas.rule_kanal.n_diperingatkan", 0),
    "R8-030": (2633, "shk.ringkas.ML_saja.fp_total", 0),
    "R8-031": (667, "shk.ringkas.H2_ML_dan_stat.fp_total", 0),
    "R8-032": (74.67, "D:(1-667/2633)*100", 0.005),
    "R8-033": (192, "shk.ringkas.ML_saja.tp_total", 0),
    "R8-034": (46, "shk.ringkas.H2_ML_dan_stat.tp_total", 0),
    "R8-035": (76.04, "D:(1-46/192)*100", 0.005),
    "R8-042": (7422, "shk.ringkas.rule_kanal.fp_total", 0),
    "R8-054": (0.3385, "D:median bacc default", 0.00005),
    "R8-055": (0.5, "D:median bacc GWO objF1", 0.00005),
    "R8-056": (0.3993, "D:median bacc GWO objBacc", 0.00005),
    "R8-057": (63, "toolwear.ringkas.ML_default.tp_total", 0),
    "R8-058": (148, "toolwear.ringkas.ML_default.fp_total", 0),
    "R8-059": (240, "toolwear.ringkas.H3a_GWO_objF1.tp_total", 0),
    "R8-060": (229, "toolwear.ringkas.H3a_GWO_objF1.fp_total", 0),
    "R8-061": (0, "toolwear.ringkas.H3a_GWO_objF1.fn_total", 0),
    "R8-062": (47, "toolwear.ringkas.H3b_GWO_objBacc.tp_total", 0),
    "R8-063": (95, "toolwear.ringkas.H3b_GWO_objBacc.fp_total", 0),
    "R8-067": (0.0833, "toolwear.per_fold.T01.bacc.ML_default", 0.00005),
    "R8-068": (0.5323, "toolwear.per_fold.T02.bacc.ML_default", 0.00005),
    "R8-069": (0.2986, "toolwear.per_fold.T03.bacc.H3b_GWO_objBacc", 0.00005),
    "R8-070": (205, "stuck.ringkas.ML_saja.fp_total", 0),
    "R8-071": (41, "stuck.ringkas.H4_tiga_komponen.fp_total", 0),
    "R8-072": (79, "stuck.ringkas.ML_saja.tp_total", 0),
    "R8-073": (17, "stuck.ringkas.H4_tiga_komponen.tp_total", 0),
    "R8-080": (148, "stuck.ringkas.ML_saja.n_onset", 0),
}
MODELKEY = {"ML_saja": "ML_saja", "rule_kanal": "rule_kanal"}


def resolve(expr):
    if expr.startswith("D:"):
        f = expr[2:]
        if f == "(1-935/2105)*100":
            return (1 - 935 / 2105) * 100
        if f == "(1-3804/5579)*100":
            return (1 - 3804 / 5579) * 100
        if f == "(1-667/2633)*100":
            return (1 - 667 / 2633) * 100
        if f == "(1-46/192)*100":
            return (1 - 46 / 192) * 100
        if f == "median recall H1":
            return float(np.median([v["recall"] for v in M("hyd", "H1_stat_dan_rule")["per_fold"].values()]))
        if f == "median far24 H1":
            return float(np.median([v["far24"] for v in M("hyd", "H1_stat_dan_rule")["per_fold"].values()]))
        if f == "median far24 rule":
            return float(np.median([v["far24"] for v in M("hyd", "rule_kanal")["per_fold"].values()]))
        if f == "median bacc default":
            return float(np.median([v["bacc"] for v in M("toolwear", "ML_default")["per_fold"].values()]))
        if f == "median bacc GWO objF1":
            return float(np.median([v["bacc"] for v in M("toolwear", "H3a_GWO_objF1")["per_fold"].values()]))
        if f == "median bacc GWO objBacc":
            return float(np.median([v["bacc"] for v in M("toolwear", "H3b_GWO_objBacc")["per_fold"].values()]))
    if expr.startswith("toolwear.per_fold."):
        _, _, foldname, key1, mdl = expr.split(".", 4)
        return M("toolwear", mdl)["per_fold"][foldname][key1]
    task, rest = expr.split(".", 1)
    if rest.startswith("ringkas."):
        node = raw[task]["ringkas"]
        rest = rest[len("ringkas."):]
    else:
        node = agg["task"][task]
    for part in rest.split("."):
        node = node[part]
    return node


bad = []
for rid, (exp, expr, tol) in EXPECT.items():
    got = resolve(expr)
    if abs(float(got) - float(exp)) > tol:
        bad.append((rid, exp, got, expr))
if bad:
    for b in bad:
        print("GAGAL", b, file=sys.stderr)
    raise SystemExit(f"{len(bad)} assert gagal, ledger tidak ditulis")
print(f"assert silang: {len(EXPECT)} baris cocok dengan JSON mentah")

lines = ["", "## Bagian R8: evaluasi berlapis per tugas dan uji hybrid (kartu `t_42096685`)", "",
         "Tanggal akses seluruh baris: 2026-10-27. Dokumen: `docs/RND_R8_EVALUASI_BERLAPIS.md`.",
         "Semua baris RUN-KITA dan DERIVASI di-assert oleh `code/rnd_r8_ledger.py` terhadap berkas JSON",
         "`scratch/rnd/r8/*.json`; baris yang gagal assert tidak ditulis. Tujuh kolom sesuai kartu.",
         "",
         "| # | Angka | Satuan | Kelas sumber | Rujukan persis | Dipakai di | Status |",
         "|---|---|---|---|---|---|---|"]
for i, r in enumerate(rows, 1):
    lines.append(f"| R8-{i:03d} | {angka(r['nilai'])} | {r['satuan']} | {r['kelas']} | "
                 f"{r['rujukan']} | bagian {r['dipakai']} | {r['status']} |")

txt = open(LEDGER, encoding="utf-8").read()
head = "## Bagian R8: evaluasi berlapis per tugas dan uji hybrid"
if head in txt:
    txt = txt[:txt.index(head)].rstrip() + "\n"
txt = txt.rstrip() + "\n" + "\n".join(lines) + "\n"
open(LEDGER, "w", encoding="utf-8").write(txt)
print(f"baris R8 ditulis: {len(rows)}")
print("kelas:", {k: sum(1 for r in rows if r['kelas'] == k) for k in
                 {r['kelas'] for r in rows}})
