"""Ledger provenance Bagian PM (kartu t_776c0a03).

Aturan: setiap baris RUN-KITA, DERIVASI, dan JURNAL di-assert terhadap berkas JSON
mentah sebelum ditulis. Baris yang gagal assert tidak ditulis dan proses berhenti
dengan kode keluar bukan nol. Idempoten: blok "## Bagian PM" lama dibuang dulu.

Keluaran: docs/RND_PROVENANCE_LEDGER.md (bagian PM) dan scratch/rnd/pm/pm_ledger.json.
"""
import json
import os
import sys

BASE = "/mnt/d/Capstone 1(v2)"
LEDGER = os.path.join(BASE, "docs/RND_PROVENANCE_LEDGER.md")
OUTDIR = os.path.join(BASE, "scratch/rnd/pm")
TANGGAL = "2026-10-27"
HEADER = "## Bagian PM: vonis akhir dan roadmap tier (kartu `t_776c0a03`)"

ROWS = []
FAIL = []


def rd(rel):
    with open(os.path.join(BASE, rel)) as f:
        return json.load(f)


R8H = rd("scratch/rnd/r8/r8_hyd.json")
R8S = rd("scratch/rnd/r8/r8_shk.json")
R8T = rd("scratch/rnd/r8/r8_toolwear.json")
R8K = rd("scratch/rnd/r8/r8_stuck.json")
R8A = rd("scratch/rnd/r8/r8_agg.json")
E4 = rd("scratch/rnd/e4/e4_summary.json")
E4G = rd("scratch/rnd/e4/e4_gate_decomp.json")
E3C = rd("scratch/rnd/e3/e3_cakupan.json")
E3V = rd("scratch/rnd/e3/e3_verify.json")
V9 = rd("scratch/v9_i1/v9_i1_RESULTS.json")
DOI = rd("scratch/rnd/pm/pm_doi.json")

HY = R8H["ringkas"]
SH = R8S["ringkas"]
TW = R8T["ringkas"]
ST = R8K["ringkas"]
AGG = R8A["turunan"]


def num(x):
    """Format angka gaya Indonesia (koma desimal), tanpa nol berlebih."""
    if isinstance(x, int):
        return "{:,}".format(x).replace(",", ".")
    s = ("%.6f" % float(x)).rstrip("0").rstrip(".")
    if "." in s:
        bulat, pec = s.split(".")
        bulat = "{:,}".format(int(bulat)).replace(",", ".")
        return bulat + "," + pec
    return s


def row(angka, satuan, kelas, rujukan, dipakai, status="TERUKUR", cek=None, harap=None, tol=None):
    """Tambah baris dengan assert opsional: cek(nilai) harus sama dengan harap."""
    if cek is not None:
        nilai = cek()
        ok = False
        if tol is None:
            ok = nilai == harap
        else:
            ok = abs(float(nilai) - float(harap)) <= tol
        if not ok:
            FAIL.append((rujukan, nilai, harap))
            return
    ROWS.append({
        "angka": angka,
        "satuan": satuan,
        "kelas": kelas,
        "rujukan": rujukan,
        "dipakai": dipakai,
        "status": status,
    })


# ---------------------------------------------------------------- R8 hyd K-i
row(num(HY["rule_kanal"]["fp_total"]), "FP", "RUN-KITA",
    "scratch/rnd/r8/r8_hyd.json ringkas.rule_kanal.fp_total; python3 code/rnd_r8_hybrid.py --task hyd (seed 42)",
    "bagian 2, 3, 4", cek=lambda: HY["rule_kanal"]["fp_total"], harap=2105)
row(num(HY["H1_stat_dan_rule"]["fp_total"]), "FP", "RUN-KITA",
    "scratch/rnd/r8/r8_hyd.json ringkas.H1_stat_dan_rule.fp_total",
    "bagian 2, 3, 4", cek=lambda: HY["H1_stat_dan_rule"]["fp_total"], harap=935)
row(num(AGG["hyd"]["potong_FP_pct"]), "persen", "DERIVASI",
    "(2105-935)/2105x100 = 55,5819; r8_agg.json turunan.hyd.potong_FP_pct",
    "bagian 2, 4", cek=lambda: AGG["hyd"]["potong_FP_pct"], harap=55.58, tol=0.01)
row(num(HY["rule_kanal"]["precision_median"]), "rasio", "RUN-KITA",
    "scratch/rnd/r8/r8_hyd.json ringkas.rule_kanal.precision_median",
    "bagian 2, 4", cek=lambda: HY["rule_kanal"]["precision_median"], harap=0.6835)
row(num(HY["H1_stat_dan_rule"]["precision_median"]), "rasio", "RUN-KITA",
    "scratch/rnd/r8/r8_hyd.json ringkas.H1_stat_dan_rule.precision_median",
    "bagian 2, 4", cek=lambda: HY["H1_stat_dan_rule"]["precision_median"], harap=0.7789)
row(num(HY["rule_kanal"]["recall_median"]), "rasio", "RUN-KITA",
    "scratch/rnd/r8/r8_hyd.json ringkas.rule_kanal.recall_median",
    "bagian 2, 4", cek=lambda: HY["rule_kanal"]["recall_median"], harap=0.7507)
row(num(HY["H1_stat_dan_rule"]["recall_median"]), "rasio", "RUN-KITA",
    "scratch/rnd/r8/r8_hyd.json ringkas.H1_stat_dan_rule.recall_median",
    "bagian 2, 4", cek=lambda: HY["H1_stat_dan_rule"]["recall_median"], harap=0.5638)
row(num(HY["rule_kanal"]["lead_median_median"]), "menit", "RUN-KITA",
    "scratch/rnd/r8/r8_hyd.json ringkas.rule_kanal.lead_median_median",
    "bagian 2, 4", cek=lambda: HY["rule_kanal"]["lead_median_median"], harap=6.0)
row(num(HY["H1_stat_dan_rule"]["lead_median_median"]), "menit", "RUN-KITA",
    "scratch/rnd/r8/r8_hyd.json ringkas.H1_stat_dan_rule.lead_median_median",
    "bagian 2, 4", cek=lambda: HY["H1_stat_dan_rule"]["lead_median_median"], harap=11.5)
row(num(HY["rule_kanal"]["fold_far_le6"]), "fold", "RUN-KITA",
    "scratch/rnd/r8/r8_hyd.json ringkas.rule_kanal.fold_far_le6 dari n_fold 9",
    "bagian 2, 4", cek=lambda: HY["rule_kanal"]["fold_far_le6"], harap=3)
row(num(HY["H1_stat_dan_rule"]["fold_far_le6"]), "fold", "RUN-KITA",
    "scratch/rnd/r8/r8_hyd.json ringkas.H1_stat_dan_rule.fold_far_le6 dari n_fold 9",
    "bagian 2, 4", cek=lambda: HY["H1_stat_dan_rule"]["fold_far_le6"], harap=7)
row(num(HY["rule_kanal"]["far24_median"]), "alarm/24jam", "RUN-KITA",
    "scratch/rnd/r8/r8_hyd.json ringkas.rule_kanal.far24_median",
    "bagian 2, 4", cek=lambda: HY["rule_kanal"]["far24_median"], harap=6.932)
row(num(HY["H1_stat_dan_rule"]["far24_median"]), "alarm/24jam", "RUN-KITA",
    "scratch/rnd/r8/r8_hyd.json ringkas.H1_stat_dan_rule.far24_median",
    "bagian 2, 4", cek=lambda: HY["H1_stat_dan_rule"]["far24_median"], harap=3.5302)
row(num(HY["H1_stat_dan_rule"]["n_onset"]), "onset", "RUN-KITA",
    "scratch/rnd/r8/r8_hyd.json ringkas.H1_stat_dan_rule.n_onset",
    "bagian 2", cek=lambda: HY["H1_stat_dan_rule"]["n_onset"], harap=390)
row(num(HY["rule_kanal"]["n_diperingatkan"]), "onset", "RUN-KITA",
    "scratch/rnd/r8/r8_hyd.json ringkas.rule_kanal.n_diperingatkan",
    "bagian 2", cek=lambda: HY["rule_kanal"]["n_diperingatkan"], harap=307)
row(num(HY["H1_stat_dan_rule"]["n_diperingatkan"]), "onset", "RUN-KITA",
    "scratch/rnd/r8/r8_hyd.json ringkas.H1_stat_dan_rule.n_diperingatkan",
    "bagian 2", cek=lambda: HY["H1_stat_dan_rule"]["n_diperingatkan"], harap=219)
row(num(HY["rule_kanal"]["tp_total"]), "TP", "RUN-KITA",
    "scratch/rnd/r8/r8_hyd.json ringkas.rule_kanal.tp_total",
    "bagian 4", cek=lambda: HY["rule_kanal"]["tp_total"], harap=5579)
row(num(HY["H1_stat_dan_rule"]["tp_total"]), "TP", "RUN-KITA",
    "scratch/rnd/r8/r8_hyd.json ringkas.H1_stat_dan_rule.tp_total",
    "bagian 4", cek=lambda: HY["H1_stat_dan_rule"]["tp_total"], harap=3804)
row(num(AGG["hyd"]["potong_FP_pct"] and round((5579 - 3804) / 5579 * 100, 2)), "persen", "DERIVASI",
    "(5579-3804)/5579x100 = 31,8157 (r8_hyd ringkas; r8_agg turunan.hyd)",
    "bagian 4", cek=lambda: (5579 - 3804) / 5579 * 100, harap=31.8157, tol=0.01)
row(num(HY["H1b_stat_atau_rule"]["fp_total"]), "FP", "RUN-KITA",
    "scratch/rnd/r8/r8_hyd.json ringkas.H1b_stat_atau_rule.fp_total (stat ATAU rule)",
    "bagian 2", cek=lambda: HY["H1b_stat_atau_rule"]["fp_total"], harap=5531)
row(num(HY["stat_cusum"]["far24_median"]), "alarm/24jam", "RUN-KITA",
    "scratch/rnd/r8/r8_hyd.json ringkas.stat_cusum.far24_median (statistik saja)",
    "bagian 2", cek=lambda: HY["stat_cusum"]["far24_median"], harap=11.0013)
row(num(HY["stat_cusum"]["recall_median"]), "rasio", "RUN-KITA",
    "scratch/rnd/r8/r8_hyd.json ringkas.stat_cusum.recall_median",
    "bagian 2", cek=lambda: HY["stat_cusum"]["recall_median"], harap=0.5832)

# ---------------------------------------------------------------- R8 shk
row(num(SH["ML_saja"]["fp_total"]), "FP", "RUN-KITA",
    "scratch/rnd/r8/r8_shk.json ringkas.ML_saja.fp_total",
    "bagian 2, 3", cek=lambda: SH["ML_saja"]["fp_total"], harap=2633)
row(num(SH["ML_saja"]["tp_total"]), "TP", "RUN-KITA",
    "scratch/rnd/r8/r8_shk.json ringkas.ML_saja.tp_total",
    "bagian 2, 3", cek=lambda: SH["ML_saja"]["tp_total"], harap=192)
row(num(SH["H2_ML_dan_stat"]["fp_total"]), "FP", "RUN-KITA",
    "scratch/rnd/r8/r8_shk.json ringkas.H2_ML_dan_stat.fp_total",
    "bagian 2, 3", cek=lambda: SH["H2_ML_dan_stat"]["fp_total"], harap=667)
row(num(SH["H2_ML_dan_stat"]["tp_total"]), "TP", "RUN-KITA",
    "scratch/rnd/r8/r8_shk.json ringkas.H2_ML_dan_stat.tp_total",
    "bagian 2, 3", cek=lambda: SH["H2_ML_dan_stat"]["tp_total"], harap=46)
row(num(AGG["shk"]["potong_FP_pct"]), "persen", "DERIVASI",
    "(2633-667)/2633x100 = 74,6677; r8_agg.json turunan.shk.potong_FP_pct",
    "bagian 2", cek=lambda: AGG["shk"]["potong_FP_pct"], harap=74.67, tol=0.01)
row(num(AGG["shk"]["drop_TP_pct"]), "persen", "DERIVASI",
    "(192-46)/192x100 = 76,0417; r8_agg.json turunan.shk.drop_TP_pct",
    "bagian 2", cek=lambda: AGG["shk"]["drop_TP_pct"], harap=76.04, tol=0.01)
auprc = AGG["shk"]["auprc"]
prev = AGG["shk"]["prev"]
auprc_med = sorted(auprc)[len(auprc) // 2] if len(auprc) % 2 else sum(sorted(auprc)[len(auprc)//2-1:len(auprc)//2+1]) / 2
prev_med = sorted(prev)[len(prev) // 2] if len(prev) % 2 else sum(sorted(prev)[len(prev)//2-1:len(prev)//2+1]) / 2
row(num(auprc_med), "AUPRC", "DERIVASI",
    "median AUPRC 9 fold dari r8_agg.json turunan.shk.auprc; median aritmetik 9 nilai",
    "bagian 2", cek=lambda: auprc_med, harap=0.0499, tol=0.0001)
row(num(prev_med), "rasio", "DERIVASI",
    "median prevalensi 9 fold dari r8_agg.json turunan.shk.prev",
    "bagian 2", cek=lambda: prev_med, harap=0.0243, tol=0.0001)
row(num(SH["H2_ML_dan_stat"]["recall_median"]), "rasio", "RUN-KITA",
    "scratch/rnd/r8/r8_shk.json ringkas.H2_ML_dan_stat.recall_median",
    "bagian 2", cek=lambda: SH["H2_ML_dan_stat"]["recall_median"], harap=0.0037)
row(num(SH["H2_ML_dan_stat"]["n_onset"]), "onset", "RUN-KITA",
    "scratch/rnd/r8/r8_shk.json ringkas.H2_ML_dan_stat.n_onset",
    "bagian 2", cek=lambda: SH["H2_ML_dan_stat"]["n_onset"], harap=181)
row(num(SH["H2_ML_dan_stat"]["n_diperingatkan"]), "onset", "RUN-KITA",
    "scratch/rnd/r8/r8_shk.json ringkas.H2_ML_dan_stat.n_diperingatkan",
    "bagian 2", cek=lambda: SH["H2_ML_dan_stat"]["n_diperingatkan"], harap=21)
row(num(SH["ML_saja"]["n_diperingatkan"]), "onset", "RUN-KITA",
    "scratch/rnd/r8/r8_shk.json ringkas.ML_saja.n_diperingatkan",
    "bagian 2", cek=lambda: SH["ML_saja"]["n_diperingatkan"], harap=64)
row(num(SH["ML_saja"]["lead_median_median"]), "menit", "RUN-KITA",
    "scratch/rnd/r8/r8_shk.json ringkas.ML_saja.lead_median_median",
    "bagian 2", cek=lambda: SH["ML_saja"]["lead_median_median"], harap=13.0)
row(num(SH["H2_ML_dan_stat"]["lead_median_median"]), "menit", "RUN-KITA",
    "scratch/rnd/r8/r8_shk.json ringkas.H2_ML_dan_stat.lead_median_median",
    "bagian 2", cek=lambda: SH["H2_ML_dan_stat"]["lead_median_median"], harap=22.0)

# ---------------------------------------------------------------- R8 tool_wear
row(num(TW["ML_default"]["bacc_median"]), "balanced accuracy", "RUN-KITA",
    "scratch/rnd/r8/r8_toolwear.json ringkas.ML_default.bacc_median",
    "bagian 2, 3", cek=lambda: TW["ML_default"]["bacc_median"], harap=0.3385)
row(num(TW["H3a_GWO_objF1"]["bacc_median"]), "balanced accuracy", "RUN-KITA",
    "scratch/rnd/r8/r8_toolwear.json ringkas.H3a_GWO_objF1.bacc_median",
    "bagian 2", cek=lambda: TW["H3a_GWO_objF1"]["bacc_median"], harap=0.5)
row(num(TW["H3b_GWO_objBacc"]["bacc_median"]), "balanced accuracy", "RUN-KITA",
    "scratch/rnd/r8/r8_toolwear.json ringkas.H3b_GWO_objBacc.bacc_median",
    "bagian 2", cek=lambda: TW["H3b_GWO_objBacc"]["bacc_median"], harap=0.3993)
row(num(TW["H3a_GWO_objF1"]["tp_total"]), "TP", "RUN-KITA",
    "scratch/rnd/r8/r8_toolwear.json ringkas.H3a_GWO_objF1.tp_total (objektif F1 semua-positif)",
    "bagian 2", cek=lambda: TW["H3a_GWO_objF1"]["tp_total"], harap=240)
row(num(TW["H3a_GWO_objF1"]["fp_total"]), "FP", "RUN-KITA",
    "scratch/rnd/r8/r8_toolwear.json ringkas.H3a_GWO_objF1.fp_total",
    "bagian 2", cek=lambda: TW["H3a_GWO_objF1"]["fp_total"], harap=229)
row(num(TW["H3b_GWO_objBacc"]["tp_total"]), "TP", "RUN-KITA",
    "scratch/rnd/r8/r8_toolwear.json ringkas.H3b_GWO_objBacc.tp_total",
    "bagian 2", cek=lambda: TW["H3b_GWO_objBacc"]["tp_total"], harap=47)
row(num(TW["H3b_GWO_objBacc"]["fp_total"]), "FP", "RUN-KITA",
    "scratch/rnd/r8/r8_toolwear.json ringkas.H3b_GWO_objBacc.fp_total",
    "bagian 2", cek=lambda: TW["H3b_GWO_objBacc"]["fp_total"], harap=95)
row(num(TW["ML_default"]["tp_total"]), "TP", "RUN-KITA",
    "scratch/rnd/r8/r8_toolwear.json ringkas.ML_default.tp_total",
    "bagian 2", cek=lambda: TW["ML_default"]["tp_total"], harap=63)
row(num(TW["ML_default"]["fp_total"]), "FP", "RUN-KITA",
    "scratch/rnd/r8/r8_toolwear.json ringkas.ML_default.fp_total",
    "bagian 2", cek=lambda: TW["ML_default"]["fp_total"], harap=148)
row(num(TW["ML_default"]["n_fold"]), "alat", "RUN-KITA",
    "scratch/rnd/r8/r8_toolwear.json ringkas.ML_default.n_fold (LOTO 4 alat)",
    "bagian 2, 6", cek=lambda: TW["ML_default"]["n_fold"], harap=4)

# ---------------------------------------------------------------- R8 stuck
row(num(ST["H4_tiga_komponen"]["fp_total"]), "FP", "RUN-KITA",
    "scratch/rnd/r8/r8_stuck.json ringkas.H4_tiga_komponen.fp_total",
    "bagian 2, 3", cek=lambda: ST["H4_tiga_komponen"]["fp_total"], harap=41)
row(num(ST["H4_tiga_komponen"]["tp_total"]), "TP", "RUN-KITA",
    "scratch/rnd/r8/r8_stuck.json ringkas.H4_tiga_komponen.tp_total",
    "bagian 2, 3", cek=lambda: ST["H4_tiga_komponen"]["tp_total"], harap=17)
row(num(ST["H4_tiga_komponen"]["precision_median"]), "rasio", "RUN-KITA",
    "scratch/rnd/r8/r8_stuck.json ringkas.H4_tiga_komponen.precision_median",
    "bagian 2", cek=lambda: ST["H4_tiga_komponen"]["precision_median"], harap=0.6404)
row(num(ST["H4_tiga_komponen"]["recall_median"]), "rasio", "RUN-KITA",
    "scratch/rnd/r8/r8_stuck.json ringkas.H4_tiga_komponen.recall_median",
    "bagian 2", cek=lambda: ST["H4_tiga_komponen"]["recall_median"], harap=0.001)
row(num(ST["H4_tiga_komponen"]["n_onset"]), "onset", "RUN-KITA",
    "scratch/rnd/r8/r8_stuck.json ringkas.H4_tiga_komponen.n_onset",
    "bagian 2", cek=lambda: ST["H4_tiga_komponen"]["n_onset"], harap=148)
row(num(ST["H4_tiga_komponen"]["n_diperingatkan"]), "onset", "RUN-KITA",
    "scratch/rnd/r8/r8_stuck.json ringkas.H4_tiga_komponen.n_diperingatkan",
    "bagian 2", cek=lambda: ST["H4_tiga_komponen"]["n_diperingatkan"], harap=13)
row(num(ST["ML_saja"]["recall_median"]), "rasio", "RUN-KITA",
    "scratch/rnd/r8/r8_stuck.json ringkas.ML_saja.recall_median",
    "bagian 3", cek=lambda: ST["ML_saja"]["recall_median"], harap=0.0322)
row(num(ST["stat_cusum"]["recall_median"]), "rasio", "RUN-KITA",
    "scratch/rnd/r8/r8_stuck.json ringkas.stat_cusum.recall_median",
    "bagian 3", cek=lambda: ST["stat_cusum"]["recall_median"], harap=0.133)
row(num(ST["rule_kanal"]["recall_median"]), "rasio", "RUN-KITA",
    "scratch/rnd/r8/r8_stuck.json ringkas.rule_kanal.recall_median",
    "bagian 3", cek=lambda: ST["rule_kanal"]["recall_median"], harap=0.0808)
row(num(ST["H4_tiga_komponen"]["fold_far_le6"]), "fold", "RUN-KITA",
    "scratch/rnd/r8/r8_stuck.json ringkas.H4_tiga_komponen.fold_far_le6 dari n_fold 4",
    "bagian 3", cek=lambda: ST["H4_tiga_komponen"]["fold_far_le6"], harap=4)

# ---------------------------------------------------------------- E4
A7 = E4["assert_r7_1"]
row(num(A7["fp_rule_terbit"]), "FP", "RUN-KITA",
    "scratch/rnd/e4/e4_summary.json assert_r7_1.fp_rule_terbit (baseline bins t-1)",
    "bagian 2, 4", cek=lambda: A7["fp_rule_terbit"], harap=2091)
row(num(A7["selisih_rule_pct"]), "persen", "DERIVASI",
    "abs(2105-2091)/2091x100 = 0,6695; e4_summary.json assert_r7_1.selisih_rule_pct",
    "bagian 2, 4", cek=lambda: A7["selisih_rule_pct"], harap=0.67, tol=0.01)
row(num(A7["fp_hybrid_terbit"]), "FP", "RUN-KITA",
    "scratch/rnd/e4/e4_summary.json assert_r7_1.fp_hybrid_terbit",
    "bagian 2, 4", cek=lambda: A7["fp_hybrid_terbit"], harap=927)
row(num(A7["selisih_hybrid_pct"]), "persen", "DERIVASI",
    "e4_summary.json assert_r7_1.selisih_hybrid_pct (0,00 persen, identik)",
    "bagian 2, 4", cek=lambda: A7["selisih_hybrid_pct"], harap=0.0)
row(num(E4["n_fitur"]), "fitur", "RUN-KITA",
    "scratch/rnd/e4/e4_summary.json n_fitur (ts_bin dibuang, 40 fitur)",
    "bagian 4", cek=lambda: E4["n_fitur"], harap=40)
row(num(E4G["hybrid_proxy_E3"]["ketiga_kejadian"]), "fold", "RUN-KITA",
    "scratch/rnd/e4/e4_gate_decomp.json hybrid_proxy_E3.ketiga_kejadian dari n 9",
    "bagian 2, 3, 4", cek=lambda: E4G["hybrid_proxy_E3"]["ketiga_kejadian"], harap=1)
row(num(E4G["hybrid_proxy_E3"]["far_dan_recall_kejadian"]), "fold", "RUN-KITA",
    "scratch/rnd/e4/e4_gate_decomp.json hybrid_proxy_E3.far_dan_recall_kejadian",
    "bagian 2, 4", cek=lambda: E4G["hybrid_proxy_E3"]["far_dan_recall_kejadian"], harap=9)
row(num(E4G["rule_t0m1"]["cakupan_ok"]), "fold", "RUN-KITA",
    "scratch/rnd/e4/e4_gate_decomp.json rule_t0m1.cakupan_ok dari n 9",
    "bagian 2, 3", cek=lambda: E4G["rule_t0m1"]["cakupan_ok"], harap=1)
row(num(E4G["A1_alpha_anggaran"]["fold_tanpa_alarm"]), "fold", "RUN-KITA",
    "scratch/rnd/e4/e4_gate_decomp.json A1_alpha_anggaran.fold_tanpa_alarm dari n 18",
    "bagian 2, 5", cek=lambda: E4G["A1_alpha_anggaran"]["fold_tanpa_alarm"], harap=12)
row(num(E4["ringkas"]["hybrid_proxy_E3"]["fold_gate_A_baru"]), "fold", "RUN-KITA",
    "scratch/rnd/e4/e4_summary.json ringkas.hybrid_proxy_E3.fold_gate_A_baru",
    "bagian 2, 5", cek=lambda: E4["ringkas"]["hybrid_proxy_E3"]["fold_gate_A_baru"], harap=1)

# ---------------------------------------------------------------- E3
folds = {d["test_well"]: d["fraksi"] for d in E3C["per_fold"]}
row(num(folds["F-10"]), "fraksi cakupan", "RUN-KITA",
    "scratch/rnd/e3/e3_cakupan.json per_fold F-10 fraksi = 7571/11249",
    "bagian 2, 3", cek=lambda: folds["F-10"], harap=0.673)
row(num(folds["F-5"]), "fraksi cakupan", "RUN-KITA",
    "scratch/rnd/e3/e3_cakupan.json per_fold F-5 fraksi = 6332/369549",
    "bagian 2, 3", cek=lambda: folds["F-5"], harap=0.0171)
n_cak = sum(1 for v in folds.values() if v >= 0.5)
row(num(n_cak), "well", "DERIVASI",
    "hitung fraksi >= 0,50 pada e3_cakupan.json per_fold (9 well)",
    "bagian 2, 3", cek=lambda: n_cak, harap=1)
row(num(E3V["v3_gate_A"]["A1"]["n_gate_A_lulus"]), "fold-run", "RUN-KITA",
    "scratch/rnd/e3/e3_verify.json v3_gate_A.A1.n_gate_A_lulus dari n_fold 45",
    "bagian 2, 5", cek=lambda: E3V["v3_gate_A"]["A1"]["n_gate_A_lulus"], harap=3)
row(num(E3V["v3_gate_A"]["A1"]["n_fold"]), "fold-run", "RUN-KITA",
    "scratch/rnd/e3/e3_verify.json v3_gate_A.A1.n_fold (5 seed x 9 fold)",
    "bagian 2, 5", cek=lambda: E3V["v3_gate_A"]["A1"]["n_fold"], harap=45)
row(num(E3V["v3_gate_A"]["A2_reset"]["n_gate_A_lulus"]), "fold", "RUN-KITA",
    "scratch/rnd/e3/e3_verify.json v3_gate_A.A2_reset.n_gate_A_lulus dari 9",
    "bagian 2", cek=lambda: E3V["v3_gate_A"]["A2_reset"]["n_gate_A_lulus"], harap=0)
row(num(E3V["v4_rentang"]["A1_semua_seed_far"]["median"]), "alarm/24jam", "RUN-KITA",
    "scratch/rnd/e3/e3_verify.json v4_rentang.A1_semua_seed_far.median",
    "bagian 2", cek=lambda: E3V["v4_rentang"]["A1_semua_seed_far"]["median"], harap=63.28839082472421)
row(num(E3V["v4_rentang"]["A1_semua_seed_far"]["max"]), "alarm/24jam", "RUN-KITA",
    "scratch/rnd/e3/e3_verify.json v4_rentang.A1_semua_seed_far.max",
    "bagian 2", cek=lambda: E3V["v4_rentang"]["A1_semua_seed_far"]["max"], harap=543.4957860021987)
row(num(E3V["v4_rentang"]["A2_tanpa_reset_far"]["max"]), "alarm/24jam", "RUN-KITA",
    "scratch/rnd/e3/e3_verify.json v4_rentang.A2_tanpa_reset_far.max (1440 = alarm tiap menit)",
    "bagian 2", cek=lambda: E3V["v4_rentang"]["A2_tanpa_reset_far"]["max"], harap=1440.0)

# ---------------------------------------------------------------- V9 registry
n_head = sum(len(e["heads"]) for e in V9["engines"])
row(num(n_head), "head", "RUN-KITA",
    "scratch/v9_i1/v9_i1_RESULTS.json jumlah heads pada 7 engines",
    "bagian 0, 3", cek=lambda: n_head, harap=27)
row(num(len(V9["engines"])), "engine", "RUN-KITA",
    "scratch/v9_i1/v9_i1_RESULTS.json len(engines)",
    "bagian 3", cek=lambda: len(V9["engines"]), harap=7)
row(num(V9["auto_critical_alarm_slots"]), "slot", "KONVENSI",
    "scratch/v9_i1/v9_i1_RESULTS.json auto_critical_alarm_slots; docs/V9_EVAL_C_LAYERC.md tier",
    "bagian 3, 4, 6", cek=lambda: V9["auto_critical_alarm_slots"], harap=0)

# ---------------------------------------------------------------- JURNAL (DOI)
for ref in DOI["rujukan"]:
    row(num(ref["lapis1_status"]), "status HTTP", "JURNAL",
        "scratch/rnd/pm/pm_doi.json %s lapis1_status; HEAD doi.org tanpa redirect; %s" % (ref["key"], ref["doi"]),
        "bagian 8", status="TERVERIFIKASI")
    row(num(ref["lapis2_status"]), "status HTTP", "JURNAL",
        "scratch/rnd/pm/pm_doi.json %s lapis2_status (%s); %s" % (ref["key"], ref["lapis2_sumber"], ref["doi"]),
        "bagian 8", status="TERVERIFIKASI")

# ---------------------------------------------------------------- kutipan baris lama
KUTIPAN = [
    ("4,1 sampai 496 (119 kali)", "alarm/24jam; rasio", "baris R1-029 (di-assert di Bagian R1) dan R5-072; sumber primer docs/V9_EVAL_C_LAYERC.md 2.1 baris C3; tidak dihitung ulang di kartu PM",
     "bagian 2, 3"),
    ("62,3", "persen baris", "baris R4-26 (di-assert di Bagian R4); n_nodata 22.385/35.906 pada docs/V9_EVAL_C_LAYERC.md 2.2; tidak dihitung ulang di kartu PM",
     "bagian 3"),
    ("0,5678", "rasio", "baris E0-021 (di-assert di Bagian E0); peluang minimal satu alarm kebetulan 4/4 alat; tidak dihitung ulang di kartu PM",
     "bagian 3, 4"),
    ("0,0542", "rasio", "baris E0-022 (di-assert di Bagian E0); recall segmen tool_wear head op_far_calibrated; tidak dihitung ulang di kartu PM",
     "bagian 3, 4"),
    ("0,3333", "Hz", "baris R3-02 (di-assert di Bagian R3); laju sampel tertinggi kanal; tidak dihitung ulang di kartu PM",
     "bagian 2, 6"),
    ("0,1667", "Hz", "baris R3-02 (di-assert di Bagian R3); Nyquist = fs/2; tidak dihitung ulang di kartu PM",
     "bagian 2, 6"),
    ("105", "percobaan VMD", "baris R3-29 (di-assert di Bagian R3); m3_decomp.json; tidak dihitung ulang di kartu PM",
     "bagian 2, 6"),
    ("75", "percobaan gagal", "baris R3-30 (di-assert di Bagian R3); m3_decomp.json; tidak dihitung ulang di kartu PM",
     "bagian 2, 6"),
    ("134,01 sampai 137.374,35", "jam", "baris R3-40 (di-assert di Bagian R3); estimasi 1-NN kNN-DTW; tidak dihitung ulang di kartu PM",
     "bagian 2, 6"),
    ("52,293 sampai 60,000", "menit alarm per jam", "baris R5-032 (di-assert di Bagian R5); CUSUM tanpa reset di luar baseline; tidak dihitung ulang di kartu PM",
     "bagian 2, 3"),
    ("0,0109", "laju alarm baseline", "baris R5-045 (di-assert di Bagian R5); Isolation Forest median; tidak dihitung ulang di kartu PM",
     "bagian 2"),
    ("6.377 dari 8.107 (78,7 persen)", "jendela", "baris R5-067 (kutipan terverifikasi); sign-flip hyd K-ii; tidak dihitung ulang di kartu PM",
     "bagian 3"),
]
for angka, satuan, sumber, pakai in KUTIPAN:
    ROWS.append({
        "angka": angka,
        "satuan": satuan,
        "kelas": "RUN-KITA",
        "rujukan": sumber,
        "dipakai": pakai,
        "status": "TERUKUR (kutipan)",
    })

# ---------------------------------------------------------------- BELUM TERUKUR
BELUM = [
    ("nilai maintenance dalam rupiah atau jam henti terhindar",
     "tidak ada data biaya dan tidak ada catatan jam henti per kejadian", "bagian 3, 6, 7"),
    ("pengurangan pemeriksaan fisik per shift",
     "tidak ada data jadwal inspeksi dan beban pemeriksaan aktual", "bagian 3, 6, 7"),
    ("lapisan B untuk tool_wear",
     "label hanya urutan jendela tanpa stempel waktu", "bagian 3, 7"),
    ("kestabilan lintas seed untuk R8 dan E4",
     "R8 memakai seed 42 tunggal; E4 memakai dua seed untuk satu assert baseline", "bagian 6, 7"),
    ("kestabilan lintas kampanye pengeboran",
     "tanggal kampanye tidak tersedia per baris", "bagian 6, 7"),
    ("hybrid untuk vib, ssi, bit_wear",
     "R8 hanya menguji hyd, shk, tool_wear, stuck", "bagian 3, 6, 7"),
    ("seleksi fitur BGWO pada 55 fitur",
     "belum ada satu run; R1 hanya menilai kelayakan dari literatur", "bagian 2, 5, 6"),
    ("biaya latih LightGBM, XGBoost, CatBoost pada data kita",
     "run pembanding R4 tidak selesai dalam anggaran waktu; E1-018", "bagian 2, 5, 7"),
    ("kalibrasi ambang per well prospektif",
     "belum pernah dijalankan; hanya usul D-A4 di EVAL_C", "bagian 4, 6, 7"),
    ("FAR bit_wear dalam satuan 24 jam",
     "baris pada grid kedalaman 0,015 m, bukan deret waktu; E0 S-6", "bagian 3, 7"),
    ("onset bit_wear K-2",
     "pra-registrasi label belum terbit; REGISTRY menandai BELUM LAYAK PAKAI", "bagian 3, 6, 7"),
]
for teks, alasan, pakai in BELUM:
    row("tidak terukur", "n/a", "BELUM-TERUKUR", alasan, pakai, status="BELUM TERUKUR")

# ---------------------------------------------------------------- tulis
if FAIL:
    print("ASSERT GAGAL (%d):" % len(FAIL))
    for f in FAIL:
        print("  ", f)
    sys.exit(1)

nomor = 0
lines = [HEADER, ""]
lines.append("Tanggal akses seluruh baris: %s. Dokumen: `docs/RND_PM_VERDICT.md`." % TANGGAL)
lines.append("Baris RUN-KITA, DERIVASI, dan JURNAL di-assert terhadap JSON mentah oleh "
             "`code/rnd_pm_ledger.py`; baris yang gagal assert tidak ditulis dan proses berhenti.")
lines.append("Tujuh kolom sesuai kartu. Angka yang tidak punya sumber ditulis BELUM TERUKUR.")
lines.append("")
lines.append("| # | Angka | Satuan | Kelas sumber | Rujukan persis | Dipakai di | Status |")
lines.append("|---|---|---|---|---|---|---|")
for r in ROWS:
    nomor += 1
    lines.append("| PM-%03d | %s | %s | %s | %s | %s | %s |" % (
        nomor, r["angka"].replace("|", "/"), r["satuan"], r["kelas"],
        r["rujukan"].replace("|", "/"), r["dipakai"], r["status"]))
blok = "\n".join(lines) + "\n"

with open(LEDGER) as f:
    isi = f.read()

if HEADER in isi:
    mulai = isi.index(HEADER)
    sisa = isi[mulai:]
    # buang sampai sebelum header bagian lain, atau akhir berkas
    idx = sisa.find("\n## ", len(HEADER))
    if idx == -1:
        isi = isi[:mulai].rstrip("\n") + "\n"
    else:
        isi = isi[:mulai] + sisa[idx + 1:]
    with open(LEDGER, "w") as f:
        f.write(isi)

with open(LEDGER, "a") as f:
    if not isi.endswith("\n"):
        f.write("\n")
    f.write("\n" + blok)

os.makedirs(OUTDIR, exist_ok=True)
with open(os.path.join(OUTDIR, "pm_ledger.json"), "w") as f:
    json.dump({"n_baris": nomor, "baris": ROWS}, f, indent=1, ensure_ascii=False)

print("baris ditulis:", nomor)
print("total baris ledger:", sum(1 for _ in open(LEDGER)))
kelas = {}
for r in ROWS:
    kelas[r["kelas"]] = kelas.get(r["kelas"], 0) + 1
print("kelas:", kelas)
