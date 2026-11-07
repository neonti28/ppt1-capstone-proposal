"""RND-E4 — tulis bagian E4 di docs/RND_PROVENANCE_LEDGER.md, satu assert per baris.

Idempoten: blok "## Bagian E4" lama dibuang sebelum menulis ulang.
"""
import json, re

BASE = "/mnt/d/Capstone 1(v2)"
E4 = f"{BASE}/scratch/rnd/e4"
LEDGER = f"{BASE}/docs/RND_PROVENANCE_LEDGER.md"


def jload(p):
    with open(p) as f:
        return json.load(f)


cmp_ = jload(f"{E4}/e4_compare.json")
summ = jload(f"{E4}/e4_summary.json")
a2 = jload(f"{E4}/e4_a2.json")
a1 = jload(f"{E4}/e4_a1.json")

R = cmp_["ringkas"]
SEB = cmp_["sebelum"]
assert_info = cmp_["assert_r7_1"]

# ---------------- assert nilai yang akan ditulis ---------------------------
assert assert_info["fp_rule"] == 2105
assert assert_info["fp_hybrid"] == 927
assert round(assert_info["selisih_rule_pct"], 2) == 0.67
assert assert_info["selisih_hybrid_pct"] == 0.0
assert cmp_["assert_r7_2"]["n_fitur"] == 40 and cmp_["assert_r7_2"]["ts_bin_dipakai"] is False
assert SEB["n_fitur"] == 41 and SEB["ts_bin_dipakai"] is True
assert SEB["far24_baris_median"] == 86.7217, SEB["far24_baris_median"]
assert SEB["recall_median"] == 0.074
assert SEB["auprc_median"] == 0.1549
assert SEB["fold_gate_A_E3"] == 2
assert SEB["fp_baris_total"] == 5427
assert SEB["baseline_proxy_total_fp"]["hybrid_rule_lag1_and_persistence"] == 195
assert R["A1_alpha_E2_lama"]["far24_baris_median"] == 139.2916
assert R["A1_alpha_E2_lama"]["far24_kejadian_median"] == 22.8191
assert R["A1_alpha_E2_lama"]["recall_median"] == 0.0905
assert R["A1_alpha_E2_lama"]["G1_far_baris"] == 0
assert R["A1_alpha_E2_lama"]["n"] == 18
assert R["A1_alpha_anggaran"]["far24_baris_median"] == 0.0
assert R["A1_alpha_anggaran"]["recall_median"] == 0.0
assert R["A1_alpha_anggaran"]["fold_recall_nol"] == 13
assert R["A1_alpha_anggaran"]["G1_far_baris"] == 13
assert R["A1_alpha_anggaran"]["G2_far_kejadian_recall"] == 0
assert R["H_or_hybrid_ML"]["far24_kejadian_median"] == 8.8339
assert R["H_or_hybrid_ML"]["recall_median"] == 0.6519
assert R["H_or_hybrid_ML"]["precision_median"] == 0.8156
assert R["H_or_hybrid_ML"]["G2_far_kejadian_recall"] == 4
assert R["H_or_hybrid_ML"]["G4_tanpa_syarat_cakupan"] == 2
assert R["H_and_hybrid_ML"]["recall_median"] == 0.0
assert R["hybrid_rule_persistence"]["far24_kejadian_median"] == 8.3208
assert R["hybrid_rule_persistence"]["recall_median"] == 0.6519
assert R["hybrid_rule_persistence"]["G2_far_kejadian_recall"] == 2
assert R["persistence"]["far24_kejadian_median"] == 7.0601
assert R["persistence"]["G2_far_kejadian_recall"] == 3
assert R["A2_cusum_h30"]["far24_baris_median"] == 151.1577
assert R["A2_cusum_h30"]["far24_kejadian_median"] == 69.1703
assert R["hybrid_proxy_E3"]["far24_baris_median"] == 6.144
assert R["rule_t0m1"]["far24_kejadian_median"] == 27.3839
assert cmp_["n_fold_cakupan_lulus"] == 1
assert summ["elapsed_s"] == 61.8
assert summ["n_fitur"] == 40
assert len(a1["folds"]) == 18
assert len(a2["folds"]) == 9

rasio_a2 = round(151.1577 / 69.1703, 3)
assert rasio_a2 == 2.185, rasio_a2
alpha_anggaran_frac = 1.0 / 240.0
assert round(alpha_anggaran_frac, 7) == 0.0041667

rows = [
    ("E4-001", "2105", "FP", "RUN-KITA",
     "`scratch/rnd/e4/e4_compare.json` `assert_r7_1.fp_rule`; skrip `code/rnd_e4_pilot.py`, "
     "dihitung `code/rnd_rule_baseline.py`", "bagian 3, 4.1", "TERUKUR"),
    ("E4-002", "927", "FP", "RUN-KITA",
     "`scratch/rnd/e4/e4_compare.json` `assert_r7_1.fp_hybrid`", "bagian 3, 4.1", "TERUKUR"),
    ("E4-003", "0,67", "persen", "DERIVASI",
     "(2105 − 2091) / 2091 × 100 = 0,6695; `assert_r7_1.selisih_rule_pct`", "bagian 3", "TERUKUR"),
    ("E4-004", "0,00", "persen", "DERIVASI",
     "(927 − 927) / 927 × 100; `assert_r7_1.selisih_hybrid_pct`", "bagian 3", "TERUKUR"),
    ("E4-005", "2091", "FP", "RUN-KITA",
     "`docs/V9_EVAL_C_LAYERC.md` baris 177 (angka kampanye V9, FP hybrid 2091 turun 927)",
     "bagian 3", "TERUKUR"),
    ("E4-006", "195", "FP", "RUN-KITA",
     "`scratch/rnd/e3/e3_baseline_results.json` "
     "`total_fp.hybrid_rule_lag1_and_persistence` (proksi E3, tidak sah)",
     "bagian 3, 5.1", "TERUKUR"),
    ("E4-007", "41", "fitur", "RUN-KITA",
     "`scratch/rnd/e4/e4_compare.json` `sebelum.n_fitur` (E3 memakai ts_bin)", "bagian 4.1", "TERUKUR"),
    ("E4-008", "40", "fitur", "RUN-KITA",
     "`scratch/rnd/e4/e4_a1.json` `n_fitur`; assert `ts_bin` tidak ada di `fitur`", "bagian 4.1", "TERUKUR"),
    ("E4-009", "86,7217", "FP per 24 jam", "RUN-KITA",
     "`scratch/rnd/e4/e4_compare.json` `sebelum.far24_baris_median` (median 9 fold seed 42, fitur 41)",
     "bagian 4.2", "TERUKUR"),
    ("E4-010", "0,0740", "rasio", "RUN-KITA",
     "`e4_compare.json` `sebelum.recall_median`", "bagian 4.2", "TERUKUR"),
    ("E4-011", "0,1549", "AUPRC", "RUN-KITA",
     "`e4_compare.json` `sebelum.auprc_median`", "bagian 4.2", "TERUKUR"),
    ("E4-012", "2", "fold dari 9", "RUN-KITA",
     "`e4_compare.json` `sebelum.fold_gate_A_E3` (definisi gate A lama, hanya FAR)",
     "bagian 4.2", "TERUKUR"),
    ("E4-013", "5427", "FP", "RUN-KITA",
     "`e4_compare.json` `sebelum.fp_baris_total` (jumlah 9 fold seed 42)", "bagian 4.2", "TERUKUR"),
    ("E4-014", "139,2916", "FP per 24 jam", "RUN-KITA",
     "`e4_compare.json` `ringkas.A1_alpha_E2_lama.far24_baris_median` (18 fold-run, seed 42 dan 7, "
     "fitur 40)", "bagian 4.3", "TERUKUR"),
    ("E4-015", "22,8191", "FP per 24 jam", "RUN-KITA",
     "`e4_compare.json` `ringkas.A1_alpha_E2_lama.far24_kejadian_median`", "bagian 4.3", "TERUKUR"),
    ("E4-016", "0,0905", "rasio", "RUN-KITA",
     "`e4_compare.json` `ringkas.A1_alpha_E2_lama.recall_median`", "bagian 4.3", "TERUKUR"),
    ("E4-017", "0", "fold dari 18", "RUN-KITA",
     "`e4_compare.json` `ringkas.A1_alpha_E2_lama.G1_far_baris`", "bagian 4.3", "TERUKUR"),
    ("E4-018", "0,000", "FP per 24 jam", "RUN-KITA",
     "`e4_compare.json` `ringkas.A1_alpha_anggaran.far24_baris_median`", "bagian 4.4", "TERUKUR"),
    ("E4-019", "0,0000", "rasio", "RUN-KITA",
     "`e4_compare.json` `ringkas.A1_alpha_anggaran.recall_median`", "bagian 4.4", "TERUKUR"),
    ("E4-020", "13", "fold dari 18", "RUN-KITA",
     "`e4_compare.json` `ringkas.A1_alpha_anggaran.fold_recall_nol`", "bagian 4.4", "TERUKUR"),
    ("E4-021", "13", "fold dari 18", "RUN-KITA",
     "`e4_compare.json` `ringkas.A1_alpha_anggaran.G1_far_baris` (lulus FAR saja, recall nol)",
     "bagian 4.4", "TERUKUR"),
    ("E4-022", "0", "fold dari 18", "RUN-KITA",
     "`e4_compare.json` `ringkas.A1_alpha_anggaran.G2_far_kejadian_recall`", "bagian 4.4", "TERUKUR"),
    ("E4-023", "8,8339", "FP per 24 jam", "RUN-KITA",
     "`e4_compare.json` `ringkas.H_or_hybrid_ML.far24_kejadian_median`", "bagian 5.2", "TERUKUR"),
    ("E4-024", "0,6519", "rasio", "RUN-KITA",
     "`e4_compare.json` `ringkas.H_or_hybrid_ML.recall_median`", "bagian 5.2", "TERUKUR"),
    ("E4-025", "0,8156", "rasio", "RUN-KITA",
     "`e4_compare.json` `ringkas.H_or_hybrid_ML.precision_median`", "bagian 5.2", "TERUKUR"),
    ("E4-026", "4", "fold dari 18", "RUN-KITA",
     "`e4_compare.json` `ringkas.H_or_hybrid_ML.G2_far_kejadian_recall`", "bagian 5.2", "TERUKUR"),
    ("E4-027", "2", "fold dari 18", "RUN-KITA",
     "`e4_compare.json` `ringkas.H_or_hybrid_ML.G4_tanpa_syarat_cakupan`", "bagian 5.2", "TERUKUR"),
    ("E4-028", "0,0000", "rasio", "RUN-KITA",
     "`e4_compare.json` `ringkas.H_and_hybrid_ML.recall_median` (gerbang AND mematikan alarm)",
     "bagian 5.2", "TERUKUR"),
    ("E4-029", "8,3208", "FP per 24 jam", "RUN-KITA",
     "`e4_compare.json` `ringkas.hybrid_rule_persistence.far24_kejadian_median`", "bagian 5.1", "TERUKUR"),
    ("E4-030", "2", "fold dari 9", "RUN-KITA",
     "`e4_compare.json` `ringkas.hybrid_rule_persistence.G2_far_kejadian_recall`", "bagian 5.1", "TERUKUR"),
    ("E4-031", "7,0601", "FP per 24 jam", "RUN-KITA",
     "`e4_compare.json` `ringkas.persistence.far24_kejadian_median`", "bagian 5.1", "TERUKUR"),
    ("E4-032", "3", "fold dari 9", "RUN-KITA",
     "`e4_compare.json` `ringkas.persistence.G2_far_kejadian_recall`", "bagian 5.1", "TERUKUR"),
    ("E4-033", "27,3839", "FP per 24 jam", "RUN-KITA",
     "`e4_compare.json` `ringkas.rule_t0m1.far24_kejadian_median`", "bagian 5.1", "TERUKUR"),
    ("E4-034", "151,1577", "FP per 24 jam", "RUN-KITA",
     "`e4_compare.json` `ringkas.A2_cusum_h30.far24_baris_median` (satuan baris)", "bagian 5.3", "TERUKUR"),
    ("E4-035", "69,1703", "FP per 24 jam", "RUN-KITA",
     "`e4_compare.json` `ringkas.A2_cusum_h30.far24_kejadian_median` (satuan kejadian)", "bagian 5.3", "TERUKUR"),
    ("E4-036", "2,185", "rasio", "DERIVASI",
     "151,1577 / 69,1703 = 2,1852; `ringkas.A2_cusum_h30`", "bagian 5.3", "TERUKUR"),
    ("E4-037", "1", "fold dari 9", "RUN-KITA",
     "`e4_compare.json` `n_fold_cakupan_lulus` (cakupan >= 0,50)", "bagian 6", "TERUKUR"),
    ("E4-038", "0,0041667", "fraksi menit negatif", "DERIVASI",
     "1/240 = 0,00416667; setara FAR <= 6 per 24 jam bila 1440 menit", "bagian 4.4", "TERUKUR"),
    ("E4-039", "61,8", "detik", "RUN-KITA",
     "`scratch/rnd/e4/e4_summary.json` `elapsed_s`, 2 seed x 9 fold", "bagian 7", "TERUKUR"),
    ("E4-040", "BELUM TERUKUR", "jam orang", "BELUM-TERUKUR",
     "tidak ada data durasi inspeksi per alarm di repo; gate B tidak dapat dihitung",
     "bagian 6, 8", "BELUM"),
    ("E4-041", "BELUM TERUKUR", "menit", "BELUM-TERUKUR",
     "delay deteksi H_or dan A1 pada satuan kejadian belum dirumuskan ulang; hanya delay satuan baris "
     "yang tersimpan di `e4_a1.json`", "bagian 8", "BELUM"),
]

HEAD = """## Bagian E4: perbaikan engineer dan run ulang pilot (kartu `t_61edf756`)

Tanggal: 2026-10-27. Dokumen: `docs/RND_E4_PERBAIKAN.md`. Semua baris di bawah di-assert oleh
`scratch/rnd/e4/e4_ledger.py` terhadap berkas JSON yang disebut (`scratch/rnd/e4/*.json`).
Baris BELUM-TERUKUR ditulis tanpa angka tebakan.

| # | Angka | Satuan | Kelas sumber | Rujukan persis | Dipakai di | Status |
|---|---|---|---|---|---|---|
"""

lines = [HEAD]
for no, angka, satuan, kelas, ruj, dipakai, status in rows:
    clean = [str(x).replace("|", "\\|") for x in (no, angka, satuan, kelas, ruj, "2026-10-27", dipakai, status)]
    lines.append("| " + " | ".join(clean) + " |\n")
block = "".join(lines)

txt = open(LEDGER).read()
# idempoten: buang blok E4 lama bila ada
txt = re.sub(r"\n## Bagian E4:.*?(?=\n## |\Z)", "\n", txt, flags=re.S).rstrip("\n") + "\n"
if not txt.endswith("\n"):
    txt += "\n"
txt += "\n" + block
open(LEDGER, "w").write(txt)
print(f"baris ditulis: {len(rows)} (E4-001..E4-{len(rows):03d})")
print("jumlah baris ledger:", len(open(LEDGER).read().splitlines()))
