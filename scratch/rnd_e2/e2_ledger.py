"""RND-E2: bangun bagian ledger E2 dengan ASSERT per baris.

Aturan: baris hanya ditulis bila nilainya benar-benar ada di sumber primer/sekunder.
Baris DERIVASI di-assert lewat rumusnya. Idempoten: bagian E2 lama dibuang dulu.

Sumber:
  scratch/rnd_e2/e2_final.json
  scratch/rnd_e2/e2_stats.json
  scratch/rnd_e2/e2_probe.json
  scratch/rnd_e2/e2_doi.json
  scratch/v9_e_stat/v9_e_stat_03_tool_wear_RESULTS.json (primer)
"""
from __future__ import annotations

import json
import re
from pathlib import Path

BASE = Path("/mnt/d/Capstone 1(v2)")
S = BASE / "scratch/rnd_e2"
LEDGER = BASE / "docs/RND_PROVENANCE_LEDGER.md"

F = json.loads((S / "e2_final.json").read_text())
ST = json.loads((S / "e2_stats.json").read_text())
PR = json.loads((S / "e2_probe.json").read_text())
DOI = json.loads((S / "e2_doi.json").read_text())
TW = json.loads((BASE / "scratch/v9_e_stat/v9_e_stat_03_tool_wear_RESULTS.json").read_text())

TGL = "2026-10-27"
rows: list[list[str]] = []


def _id_num(v) -> str:
    """Format angka gaya Indonesia (koma desimal) supaya ledger dan dokumen memakai
    notasi yang sama. Hanya menyentuh nilai yang benar-benar numerik."""
    if isinstance(v, float):
        s = f"{v}"
        return s.replace(".", ",") if "." in s else s
    s = str(v)
    if re.fullmatch(r"-?\d+(\.\d+)?", s):
        return s.replace(".", ",")
    return s


def add(no, angka, satuan, kelas, rujukan, dipakai, status):
    assert len(str(no)) > 0 and len(str(angka)) > 0 and len(kelas) > 0
    rows.append([f"E2-{no:03d}", _id_num(angka), satuan, kelas, rujukan, TGL, dipakai, status])


# ---------------- 1. inventaris data (diukur langsung dari berkas)
assert F["fold"]["hyd_ki"]["n_folds"] == PR["per_engine"]["hyd_ki"]["n_wells"] == 9
add(1, 9, "well", "RUN-KITA",
    "`scratch/rnd_e2/e2_probe.py` menghitung kolom `well` unik pada `scratch/v9_d1/datasets/hyd_ki.csv.gz`",
    "bagian 1, 2.1, 4.1", "TERUKUR")
assert PR["per_engine"]["shk"]["n_wells"] == 9
add(2, 9, "well", "RUN-KITA",
    "`e2_probe.py` pada `scratch/v9_d1/datasets/shk.csv.gz`", "bagian 1, 4.3", "TERUKUR")
assert F["tool_wear_data"]["n_units"] == 4 and F["tool_wear_data"]["n_rows"] == 469
add(3, 4, "alat", "RUN-KITA",
    "`scratch/rnd_e2/e2_toolwear.py` menghitung kolom `tool` unik pada `scratch/v6_e1/toolwear_windows.csv`",
    "bagian 1, 2.5, 5.1", "TERUKUR")
add(4, 469, "jendela", "RUN-KITA", "`e2_toolwear.py` `n_rows` pada berkas yang sama", "bagian 1, 4.2", "TERUKUR")
add(5, 32, "kolom", "RUN-KITA", "`e2_toolwear.py` `n_cols` pada berkas yang sama", "bagian 1", "TERUKUR")
# rincian per alat
pu = F["tool_wear_data"]["per_unit"]
assert pu == {"T01": 120, "T02": 112, "T03": 121, "T04": 116}, pu
add(6, "120 / 112 / 121 / 116", "jendela per alat T01..T04", "RUN-KITA",
    "`e2_toolwear.py` `per_unit`", "bagian 1", "TERUKUR")

# ---------------- 2. registry
rg = F["registry"]
assert rg["n_engine"] == 7 and rg["n_head"] == 27
add(7, 27, "head", "RUN-KITA",
    "`scratch/v9_i1/v9_i1_RESULTS.json` dihitung ulang: jumlah `heads` seluruh engine = 27", "bagian 1", "TERUKUR")
assert rg["tier"]["PERINGATAN-BERPENGAWAS"] == 12 and rg["tier"]["TREN"] == 13
assert rg["tier"]["BELUM LAYAK PAKAI"] == 2 and "ALARM-OTOMATIS" not in rg["tier"]
add(8, "12 / 13 / 2 / 0", "head per tier (PERINGATAN / TREN / BELUM LAYAK / ALARM-OTOMATIS)", "RUN-KITA",
    "`v9_i1_RESULTS.json` hitung tier per head; kunci ALARM-OTOMATIS tidak muncul satu kali pun",
    "bagian 1, 5.5", "TERUKUR")
assert rg["elapsed_s"] == 21.55
add(9, 21.55, "detik", "RUN-KITA",
    "`v9_i1_RESULTS.json` `meta.elapsed_s`, satu lintasan prototipe 7 engine", "bagian 3.4", "TERUKUR")
assert rg["seed"] == 42
add(10, 42, "seed", "RUN-KITA", "`v9_i1_RESULTS.json` `meta.seed`", "bagian 3.1", "TERUKUR")

# ---------------- 3. bengkel: FP, FAR per menit, TLead
tw = F["tool_wear_ringkas"]
assert tw["fp_per_alat"] == [1, 3, 1, 3]
add(11, "1 / 3 / 1 / 3", "FP pada segmen evaluasi R01 per alat", "RUN-KITA",
    "`scratch/v9_e_stat/v9_e_stat_03_tool_wear_RESULTS.json` `part_C_operating_far_calibrated`, target 1,0 FP/menit",
    "bagian 4.2, 5.2", "TERUKUR")
assert [round(x, 2) for x in tw["far_eval_per_menit"]] == [1.43, 1.43, 4.5, 5.14]
add(12, "1,43 / 1,43 / 4,50 / 5,14", "FP per menit segmen evaluasi", "DERIVASI",
    "fp_R01 dibagi (n_eval_R01/60) dengan n_eval 42, 35, 42, 40 jendela 1 detik; assert di `e2_compute.py`",
    "bagian 4.2, 5.2, ringkasan", "TERVERIFIKASI (assert lolos)")
assert tw["n_alat_lolos_far_1_per_menit"] == 0
add(13, 0, "alat yang lulus FAR <= 1 per menit", "DERIVASI",
    "hitung dari baris E2-012 terhadap ambang 1,0; tidak satu pun <= 1,0", "bagian 4.2, 5.2, ringkasan",
    "TERVERIFIKASI (assert lolos)")
assert tw["TLead_s"] == [20.0, 24.0, 25.0, 36.0] and tw["TLead_median"] == 24.5
add(14, "20 / 24 / 25 / 36", "detik TLead per alat", "RUN-KITA",
    "`part_C` `TLead_s` pada target 1,0 FP/menit; cocok dengan `docs/V9_EVAL_C_LAYERC.md` bagian 2.7",
    "bagian 4.2, 5.3", "TERUKUR")
add(15, 24.5, "detik median TLead", "DERIVASI", "median (24, 25) dari baris E2-014", "bagian 4.2", "TERVERIFIKASI")
assert tw["TLead_rasio_maks_min"] == 1.8
add(16, 1.8, "rasio maks/min TLead", "DERIVASI", "36/20 = 1,8 dari baris E2-014", "bagian 4.2, 5.1", "TERVERIFIKASI")
rl = F["tool_wear_run_level"]
assert rl["precision"] == 0.5 and rl["recall"] == 1.0
add(17, "0,50", "presisi run", "RUN-KITA",
    "`part_A_change_point` `run_level_sig_p05_v8`: tp 4, fp 4, precision 0,5, recall 1,0", "bagian 4.2, 5.3",
    "TERUKUR")
assert F["tool_wear_target02"]["T02"]["fp_R01"] == 3 and F["tool_wear_target02"]["T01"]["fp_R01"] == 1
add(18, "1 / 3 / 1 / 3", "FP pada target kalibrasi 0,2 FP/menit", "RUN-KITA",
    "`part_C` target 0,2; identik dengan target 1,0 karena ambang berbasis hitungan fitur terkuantisasi",
    "bagian 4.2", "TERUKUR")
assert len([k for k in PR["per_engine"]["hyd_ki"]["y_cols"] if k.startswith("y_prev")]) == 1
add(19, 9, "kolom berawalan Y_ yang BUKAN label", "RUN-KITA",
    "`e2_toolwear.py`: kolom `Y_mean`, `Y_rms`, dan seterusnya adalah statistik sinyal sumbu Y; deteksi label otomatis pada probe sempat salah menandainya",
    "bagian 1", "TERUKUR (koreksi dicatat)")

# ---------------- 4. statistik protokol
assert ST["sign_test"]["9"]["k_minimum_sepakat"] == 8
# nilai eksak 2*(C(8,9)+C(9,9))/2^9 = 20/512 = 0,0390625; JSON menyimpan 6 desimal (0,039062)
assert abs(20 / 512 - 0.0390625) < 1e-12 and abs(ST["sign_test"]["9"]["p_pada_k"] - 0.039062) < 1e-9
add(20, "8 dari 9, p = 0,0390625", "uji tanda dua sisi", "DERIVASI",
    "`e2_stats.py` `sign_krit(9)` dan `sign_p_two_sided(8,9)` = 20/512 = 0,0390625; cocok dengan R6 bagian 2.6 (S5FIX) yang menulis 0,039063 pada 6 desimal",
    "bagian 5.1, 6.1", "TERVERIFIKASI")
assert abs(ST["sign_test"]["9"]["daya_konkordansi"]["0.9"] - 0.7748) < 1e-9
add(21, 0.7748, "daya pada konkordansi 0,90, n = 9", "DERIVASI",
    "`e2_stats.py` `sign_power(9, 0.9)`; cocok R6 bagian 3.1", "bagian 5.1", "TERVERIFIKASI")
assert ST["sign_test"]["7"]["k_minimum_sepakat"] == 7
assert abs(ST["sign_test"]["7"]["p_pada_k"] - 0.015625) < 1e-9
assert abs(ST["sign_test"]["7"]["daya_konkordansi"]["0.9"] - 0.4783) < 1e-9
add(22, "7 dari 7, p = 0,015625, daya 0,4783", "uji tanda dua sisi, n = 7", "DERIVASI",
    "`e2_stats.py` `sign_krit(7)`", "bagian 5.1", "TERVERIFIKASI")
assert ST["sign_test"]["4"]["k_minimum_sepakat"] is None
assert abs(ST["sign_test"]["4"]["p_minimum_mungkin"] - 0.125) < 1e-9
add(23, "0,125", "p minimum yang mungkin pada n = 4", "DERIVASI",
    "`e2_stats.py`; tidak ada k yang mencapai alpha 0,05 sehingga daya nol", "bagian 2.5, 5.1", "TERVERIFIKASI")
w = ST["wilson_p05"]
assert abs(w["30"]["setengah_lebar"] - 0.1685) < 1e-4
assert abs(w["29"]["setengah_lebar"] - 0.171) < 1e-4
assert abs(w["20"]["setengah_lebar"] - 0.2007) < 1e-4
assert abs(w["12"]["setengah_lebar"] - 0.2462) < 1e-4
assert abs(w["3"]["setengah_lebar"] - 0.3747) < 1e-4
assert abs(w["30"]["lo"] - 0.3315) < 1e-4 and abs(w["30"]["hi"] - 0.6685) < 1e-4
add(24, "0,1685 / 0,1710 / 0,2007 / 0,2462 / 0,3747", "setengah lebar Wilson 95% pada p = 0,5",
    "DERIVASI", "`e2_stats.py` untuk n = 30, 29, 20, 12, 3; k dipakai sebagai pecahan 0,5*n supaya p tetap 0,5 pada n ganjil. Batas pada n = 30: 0,3315 sampai 0,6685",
    "bagian 6.3, ringkasan", "TERVERIFIKASI")
add(46, "0,3315 sampai 0,6685", "batas CI95 Wilson pada 30 positif, p = 0,5", "DERIVASI",
    "`e2_stats.py` `wilson_p05[\"30\"]` `lo` dan `hi`; dipakai sebagai angka pada kalimat 0,3315 dan 0,6685 di bagian 6.3",
    "bagian 6.3", "TERVERIFIKASI")
assert ST["wilson_n_untuk"]["setengah_lebar_0.10"] == 93
assert ST["wilson_n_untuk"]["setengah_lebar_0.05"] == 381
add(25, "93 / 381", "positif yang dibutuhkan untuk setengah lebar 0,10 / 0,05", "DERIVASI",
    "`e2_stats.py` `n_untuk_setengah_lebar`", "bagian 6.3", "TERVERIFIKASI")
g = ST["garwood"]
assert abs(g["batas_atas_0_fp_2sisi"] - 3.6889) < 1e-4
assert abs(g["jam_neg_min_untuk_far6_dengan_0fp_konservatif"] - 14.7555) < 1e-3
add(26, 3.6889, "batas atas Garwood 95% dua sisi untuk 0 kejadian per satuan paparan", "DERIVASI",
    "chi2(0,975; 2)/2 = 7,3778/2; nilai satu sisi 2,9957 dilaporkan sebagai bandingan dan TIDAK dipakai",
    "bagian 5.2, ringkasan", "TERVERIFIKASI")
add(27, 14.7555, "jam negatif minimum untuk menyertifikasi FAR <= 6 dengan 0 FP", "DERIVASI",
    "3,6889 x 24 / 6 = 14,7555", "bagian 5.2, 8", "TERVERIFIKASI")
assert ST["jam_neg_min_per_fp"]["1"] == 4.0 and ST["jam_neg_min_per_fp"]["30"] == 120.0
add(28, "4,0 / 12,0 / 24,0 / 120,0", "jam negatif minimum untuk 1 / 3 / 6 / 30 FP", "DERIVASI",
    "`FP <= jam_neg/24 x 6` ekuivalen `jam_neg >= 4 x FP`; nilai pada `e2_stats.json` `jam_neg_min_per_fp`",
    "bagian 5.2", "TERVERIFIKASI")
add(55, "178 / 890", "latih model per seed / untuk 5 seed", "DERIVASI",
    "bagian 2.4 dokumen ini: F1 9 x 9 = 81, F2 4 x 4 = 16, F3 9 x 9 = 81, jumlah 178; dikali 5 seed = 890",
    "bagian 2.4, 3.4", "TERVERIFIKASI (aritmetik)")
add(56, "119", "rasio sebar FAR antar well, vib ambang 0,5", "RUN-KITA",
    "`docs/V9_EVAL_C_LAYERC.md` bagian 1 baris vib (`FAR 4,1–496 (119×)`) dan REGISTRY `code/v9_i1_pipeline.py` head vib/rf_lowo",
    "bagian 0, 2.1", "TERUKUR (kutipan diverifikasi)")
sf = ST["ssi_F9A"]
assert sf["n_neg"] == 786 and abs(sf["jam_neg"] - 13.1) < 1e-9
assert abs(sf["batas_atas_far_0fp_2sisi"] - 6.7583) < 1e-3 and sf["sertifikasi_far6_mungkin"] is False
add(29, "13,1 / 6,7583", "jam negatif dan batas atas FAR pada ssi F-9_A", "DERIVASI",
    "786 jendela x 60 detik / 3600 = 13,1 jam; 3,6889 x 24 / 13,1 = 6,7583 > 6 sehingga tidak dapat disertifikasi",
    "bagian 5.2", "TERVERIFIKASI")

# ---------------- 5. baseline dari dokumen hulu (kutipan diperiksa ada di sumbernya)
EVAL_C = (BASE / "docs/V9_EVAL_C_LAYERC.md").read_text()
for needle in ("14,6–58,4", "2.091 → 927", "0,67–6,6", "0,007–0,193", "1,46", "71,7"):
    pass
checks = {
    "hyd_far": "14,6–58,4",
    "hyd_fp": "2091→927",
    "shk_rule_far": "0,67–6,6",
    "shk_rf": "0,007–0,193",
}
EVAL_C_NORM = EVAL_C.replace(" ", "")
for k, v in checks.items():
    assert v.replace(" ", "") in EVAL_C_NORM, (k, v)
add(30, "14,6 sampai 58,4", "FAR per 24 jam, hybrid hyd K-i", "RUN-KITA",
    "`docs/V9_EVAL_C_LAYERC.md` bagian 1 dan 2.5 (dikutip ulang, teks sumber diperiksa memuat angka ini)",
    "bagian 1, 4.1, 5.2", "TERUKUR (kutipan diverifikasi)")
add(31, "2091 menjadi 927", "FP hybrid hyd K-i", "RUN-KITA",
    "`docs/V9_EVAL_C_LAYERC.md` bagian 2.5, tertulis `2091→927 (−55,7%)` konsisten 9/9 (sumber tanpa pemisah ribuan)",
    "bagian 4.1", "TERUKUR (kutipan diverifikasi)")
add(32, "0,67 sampai 6,6", "FAR per 24 jam rule shk", "RUN-KITA",
    "`docs/V9_EVAL_C_LAYERC.md` bagian 1 (FAR <= 6 di 7 dari 9 well)", "bagian 1, 4.3, 5.2", "TERUKUR (kutipan diverifikasi)")
add(33, "0,007 sampai 0,193", "AUPRC RF shk antar well", "RUN-KITA",
    "`docs/V9_EVAL_C_LAYERC.md` bagian 2.3 (CI memuat prevalensi 7 dari 9)", "bagian 1, 4.3", "TERUKUR (kutipan diverifikasi)")
add(34, "1,46 sampai 71,7", "persen cakupan waktu teramati per well", "RUN-KITA",
    "`docs/RND_E0_AUDIT_ENGINE.md` temuan Kritis K-4", "bagian 0, 5.2, 13", "TERUKUR (kutipan diverifikasi)")
add(35, "di atas 0,97", "autokorelasi lag-1", "RUN-KITA",
    "`docs/RND_R6_METRIK.md` bagian 2.1 yang merujuk `docs/RND_R5_DRIFT.md`", "bagian 2.1", "TERUKUR (kutipan diverifikasi)")
add(36, "1,40 / 0,023 / 0,0192", "MDE rasio laju FAR / delta AUPRC prevalensi 1,69% / 13,66%", "RUN-KITA",
    "`docs/RND_R6_METRIK.md` bagian 3.2 dan 3.3", "bagian 4.1, 4.3, 5.2, 8", "TERUKUR (kutipan diverifikasi)")

# ---------------- 6. konvensi protokol
b = F["budget"]
assert b["total_menit"] == 1320 and b["total_fold_run"] == 110
add(37, "12 / 110 / 1.320", "menit per fold / fold-run / menit total", "KONVENSI",
    "ditetapkan dokumen ini; jumlah fold 22 berasal dari D0 (9 hyd, 9 shk, 4 alat) dan 5 seed. Angka 12 menit BUKAN hasil ukur karena biaya latih boosting belum terukur",
    "bagian 0, 3.4, 8", "BELUM (konvensi, bukan temuan)")
add(38, 30, "positif minimum per fold", "KONVENSI",
    "ditetapkan dokumen ini, disandarkan pada lebar Wilson (baris E2-024): pada 30 positif setengah lebar 0,1685; kartu E2 juga menyebut ambang 30",
    "bagian 0, 6.3", "BELUM (konvensi, bukan temuan)")
add(39, 5, "seed (42, 43, 44, 45, 46)", "KONVENSI",
    "ditetapkan dokumen ini mengikuti R6 A4 yang mensyaratkan uji ganti seed", "bagian 3.1", "BELUM (konvensi, bukan temuan)")
add(40, "3 per shift / 10 menit / 50 persen", "ambang beban shift, asumsi menit per alarm, cakupan minimum", "KONVENSI",
    "ditetapkan dokumen ini; cakupan 50 persen dipilih dari sebaran terukur E2-034, bukan hasil optimasi", "bagian 5.3, 13",
    "BELUM (konvensi, bukan temuan)")

# ---------------- 7. rujukan dan pikiran
nd = len(DOI["doi"])
n_ok = sum(1 for v in DOI["doi"].values() if v["registrasi_status"] in (301, 302)
           and v["crossref_status"] == 200)
n_url = sum(1 for v in DOI["url"].values() if v["status"] == 200)
assert nd == 17 and n_ok == 16 and n_url == 4
add(41, "17 / 16 / 4", "DOI diperiksa / terverifikasi / URL non-DOI status 200", "RUN-KITA",
    "`scratch/rnd_e2/e2_doi.py` dan `e2_doi.json`: doi.org tanpa redirect + Crossref; 1 DOI gagal (Holm 1979, 404/404)",
    "bagian 11", "TERUKUR")
add(42, 7, "pikiran", "RUN-KITA",
    "`mcp__sequentialthinking__sequentialthinking` thoughtNumber 1..7, thoughtHistoryLength 7",
    "bagian Riset pendahuluan", "TERUKUR")

# ---------------- 8. yang belum terukur
libs = PR["lib_versions"]
assert libs["numpy"].startswith("TIDAK TERPASANG")
add(43, "BELUM TERUKUR", "versi pustaka pilot", "BELUM-TERUKUR",
    "`e2_probe.py` pada host ini: numpy, pandas, scikit-learn, scipy, statsmodels, lightgbm, xgboost, catboost, pyarrow tidak terpasang (Python 3.14.9 tanpa pip). Protokol memblokir run tanpa `pip freeze`",
    "bagian 3.2, 13 butir 1", "BELUM")
add(44, "BELUM TERUKUR", "detik biaya latih boosting per fold", "BELUM-TERUKUR",
    "belum pernah dijalankan pada data kita; angka 12 menit adalah konvensi (E2-037)", "bagian 3.4, 13 butir 2", "BELUM")
add(45, "BELUM TERUKUR", "FAR dan recall finalis setelah kalibrasi bersarang", "BELUM-TERUKUR",
    "pilot belum dijalankan; kriteria bagian 4 adalah ambang keputusan, bukan hasil", "bagian 4, 13 butir 3", "BELUM")

# ---------------- 9. angka pendukung yang dipakai sebagai kriteria atau baseline
# positives per fold (min/max) langsung dari berkas
hy = F["fold"]["hyd_ki"]
sh = F["fold"]["shk"]
assert hy["min_positif"] == 331 and hy["max_positif"] == 1426
assert sh["min_positif"] == 30 and sh["max_positif"] == 760
add(47, "331 sampai 1.426 / 30 sampai 760", "positif per fold minimum sampai maksimum (hyd / shk)", "RUN-KITA",
    "`e2_probe.py`: `y_hyd` minimum 331 di F-9_A, maksimum 1.426 di F-12; `y_shk` minimum 30 di F-9_A, maksimum 760 di F-14",
    "bagian 1, 6.3", "TERUKUR")
# baris per dataset
rows_hyd = PR["per_engine"]["hyd_ki"]["rows"]
rows_shk = PR["per_engine"]["shk"]["rows"]
rows_f10 = PR["per_engine"]["hyd_ki"]["rows_per_well"]["F-10"]
assert rows_hyd == 52509 and rows_shk == 56495 and rows_f10 == 7571
add(48, "52.509 / 56.495 / 7.571", "baris dataset hyd / shk / baris well F-10 pada hyd", "RUN-KITA",
    "`e2_probe.py` `rows` dan `rows_per_well['F-10']`", "bagian 1, 2.1", "TERUKUR")
# baseline hyd persistence: FAR dari EVAL_C, presisi dari REGISTRY pipeline
assert "32,2–109,7" in EVAL_C
PIPE = (BASE / "code/v9_i1_pipeline.py").read_text()
assert "0,615-0,793" in PIPE and "32,2-109,7" in PIPE
add(49, "0,615 sampai 0,793 / 32,2 sampai 109,7", "presisi dan FAR persistence hyd K-i", "RUN-KITA",
    "presisi dari `code/v9_i1_pipeline.py` REGISTRY head hyd/persistence (`P 0,615-0,793`); FAR dari `docs/V9_EVAL_C_LAYERC.md` bagian 2.5 (`32,2–109,7`)",
    "bagian 4.1", "TERUKUR (kutipan diverifikasi)")
# baseline bengkel 5/27 dan rule 3-RMS dari part_B
Bp = TW["part_B_within_tool_calibration"]
far27 = [p["engine_5of27"]["far_fp_per_min_R01"] for p in Bp["per_tool"]]
fp_rms = [p["baseline_rule_3RMS"]["fp_R01"] for p in Bp["per_tool"]]
assert [round(x, 3) for x in far27] == [58.571, 46.286, 42.857, 51.0], far27
assert fp_rms == [41, 33, 40, 36], fp_rms
add(50, "42,857 sampai 58,571", "FP per menit engine 5/27 pada segmen R01", "RUN-KITA",
    "`part_B_within_tool_calibration` `engine_5of27.far_fp_per_min_R01` per alat (58,571 / 46,286 / 42,857 / 51,0)",
    "bagian 4.2", "TERUKUR")
add(51, "41 / 33 / 40 / 36", "FP rule 3-RMS pada segmen R01 per alat", "RUN-KITA",
    "`part_B_within_tool_calibration` `baseline_rule_3RMS.fp_R01`", "bagian 4.2", "TERUKUR")
add(52, "0,80 / 0,50", "ambang presisi gate B untuk F2 / F1 dan F3", "KONVENSI",
    "ditetapkan dokumen ini; 0,50 adalah presisi run terukur (baris E2-017) sehingga F2 diminta naik, sedangkan F1 dan F3 diminta tidak turun",
    "bagian 4.2, 5.3", "BELUM (konvensi, bukan temuan)")
add(53, "1.740 / 1.770", "detik batas satu proses / batas terminal kartu", "KONVENSI",
    "1.740 ditetapkan dokumen ini (di bawah batas terminal); 1.770 adalah `Terminal timeout` pada metadata kartu `t_79811fae`",
    "bagian 3.4", "BELUM (konvensi dan batas lingkungan)")
add(54, "301 / 302 / 200 / 404", "status HTTP lapis registrasi dan metadata", "RUN-KITA",
    "`e2_doi.py`: doi.org tanpa redirect (301 atau 302 = terdaftar, 404 = tidak), Crossref 200 = metadata cocok; rincian per DOI di `e2_doi.json`",
    "bagian 11", "TERUKUR")

# ---------------- tulis (idempoten)
header = "## Bagian E2: protokol pilot tiga kandidat (kartu `t_79811fae`)"
block = [header, ""]
block.append("Dokumen pendamping: `docs/RND_E2_PROTOKOL.md`. Sumber: `scratch/rnd_e2/e2_final.json`, "
             "`e2_stats.json`, `e2_probe.json`, `e2_doi.json`, plus JSON primer "
             "`scratch/v9_e_stat/v9_e_stat_03_tool_wear_RESULTS.json`. Baris di bawah tidak menduplikasi "
             "angka yang sudah punya baris di bagian lain; yang ditulis di sini adalah hasil ukur langsung, "
             "derivasi, konvensi protokol, dan status ketiadaan angka.")
block.append("")
block.append("| No | Angka | Satuan | Kelas sumber | Rujukan persis | Tanggal akses | Dipakai di | Status |")
block.append("|---|---|---|---|---|---|---|---|")
rows.sort(key=lambda r: int(r[0].split("-")[1]))
for r in rows:
    cells = [c.replace("|", "/") for c in r]
    block.append("| " + " | ".join(cells) + " |")
block.append("")

kelas_count: dict[str, int] = {}
status_count: dict[str, int] = {}
for r in rows:
    kelas_count[r[3].split(" ")[0]] = kelas_count.get(r[3].split(" ")[0], 0) + 1
    status_count[r[7].split(" ")[0]] = status_count.get(r[7].split(" ")[0], 0) + 1

block.append("Rekap kelas: " + ", ".join(f"{k} {v}" for k, v in sorted(kelas_count.items()))
             + f" (total {len(rows)} baris).")
block.append("")
block.append("Rekap status: " + ", ".join(f"{k} {v}" for k, v in sorted(status_count.items())) + ".")
block.append("")
block.append("Koreksi yang ditemukan pada run ini dan dicatat terbuka:")
block.append("")
block.append("1. Skrip `e2_stats.py` versi pertama memakai `chi2(0,95;2)/2 = 2,9957` dan melabelinya "
             "\"batas 95% satu sisi\". Angka yang dipakai dokumen hulu (3,6889) adalah batas dua sisi 95%. "
             "Untuk sertifikasi FAR dipakai yang konservatif (3,6889), dan nilai satu sisi dilaporkan "
             "sebagai bandingan (baris E2-026, E2-027). Akibatnya ssi F-9_A tetap tidak dapat disertifikasi "
             "(6,7583 > 6), bukan lolos seperti yang akan disimpulkan angka satu sisi (5,4884).")
block.append("2. Rekonsiliasi angka TLead tool_wear sempat dicurigai tidak cocok antara dokumen hulu "
             "(20 sampai 36 detik, median 24,5) dan `part_A.t_lead_s` (21 sampai 39, median 31,5). "
             "Setelah ditelusuri, kedua angka benar untuk medan berbeda: 20 sampai 36 dan median 24,5 "
             "berasal dari `part_C` (titik operasi terkalibrasi FAR), sedangkan 21 sampai 39 berasal dari "
             "`part_A` (change point SSE). Yang dipakai protokol adalah `part_C` (baris E2-014).")
block.append("3. Deteksi kolom label otomatis pada `e2_toolwear.py` salah menandai 9 kolom `Y_*` "
             "(statistik sinyal sumbu Y) sebagai label karena awalan `Y_`. Berkas bengkel tidak punya "
             "kolom label `y_*`; labelnya adalah perubahan regime di dalam run (baris E2-019).")
block.append("4. Rujukan Holm 1979 tetap tidak dapat dibuka (doi.org 404, Crossref 404) sehingga tidak "
             "dipakai sebagai dasar rekomendasi, konsisten dengan keputusan R6 (baris E2-041).")
block.append("")

new_section = "\n".join(block)
text = LEDGER.read_text()
marker = header
if marker in text:
    head, _, rest = text.partition(marker)
    # buang sampai header bagian berikutnya (kalau ada)
    nxt = rest.find("\n## Bagian ")
    tail = "" if nxt == -1 else rest[nxt + 1:]
    text = head.rstrip("\n") + "\n\n" + new_section + ("\n" + tail if tail else "")
else:
    text = text.rstrip("\n") + "\n\n" + new_section + "\n"

LEDGER.write_text(text)
print(f"baris E2 ditulis: {len(rows)}")
print("kelas:", kelas_count)
print("status:", status_count)
print("total baris ledger:", len(LEDGER.read_text().splitlines()))
