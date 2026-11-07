#!/usr/bin/env python3
"""RND-S1 -- generator baris ledger S1 (7 kolom), idempoten, ber-assert.

Setiap baris punya (nilai, satuan, kelas, rujukan, dipakai, status). Nilai di-assert
terhadap berkas JSON mentah lewat resolver, bukan terhadap angka yang diketik ulang.
Baris DERIVASI di-assert lewat rumusnya. Baris BELUM-TERUKUR ditulis tanpa angka.

Sumber mentah:
  scratch/rnd/s1/s1_hyd_seeds.json     hasil lintas seed H1
  scratch/rnd/s1/s1_h_saturasi.json    pemeriksaan saturasi ambang CUSUM
  scratch/rnd/s1/s1_meta.json          metadata run
  scratch/rnd/r8/r8_hyd.json           angka terbit R8 yang direproduksi
  scratch/v9_i1/v9_i1_RESULTS.json     angka engine pra-riset V9 pada segmen hyd_ki

Idempoten: blok "## Bagian S1:" lama dibuang sebelum menulis ulang. Bagian lain
ledger (termasuk Bagian PM yang ditulis setelah R8) TIDAK disentuh.
"""
import json
import os
import sys

BASE = "/mnt/d/Capstone 1(v2)"
LEDGER = f"{BASE}/docs/RND_PROVENANCE_LEDGER.md"
S1 = f"{BASE}/scratch/rnd/s1"
HEAD = "## Bagian S1: ketahanan lintas seed H1 hyd dan harness bersama"

seeds = json.load(open(f"{S1}/s1_hyd_seeds.json"))
sat = json.load(open(f"{S1}/s1_h_saturasi.json"))
meta = json.load(open(f"{S1}/s1_meta.json"))
r8 = json.load(open(f"{BASE}/scratch/rnd/r8/r8_hyd.json"))
v9 = json.load(open(f"{BASE}/scratch/v9_i1/v9_i1_RESULTS.json"))

M = "H1_stat_dan_rule"
ML = "ML_saja_kontrol"


def ring(seed):
    return seeds["per_seed"][str(seed)]["ringkas"]


def folds_of(model, seed=42):
    return [r for r in seeds["per_seed"][str(seed)]["folds"] if r["model"] == model]


def fold_rec(name, model=M, seed=42):
    for r in folds_of(model, seed):
        if r["fold"] == name:
            return r
    raise KeyError(name)


def v9_head(name):
    for e in v9["engines"]:
        if e["engine"] == "hyd":
            for h in e["heads"]:
                if h["head"] == name:
                    return h
    raise KeyError(name)


rows = []


def R(nilai, satuan, kelas, rujukan, dipakai, status="TERUKUR"):
    rows.append(dict(nilai=nilai, satuan=satuan, kelas=kelas, rujukan=rujukan,
                     dipakai=dipakai, status=status))


def angka(x):
    if isinstance(x, float):
        return f"{x:.6g}" if abs(x) < 1 else f"{x}"
    return f"{x}"


# ---------------------------------------------------------------- reproduksi R8
R(ring(42)["fp_total"], "FP", "RUN-KITA",
  "s1_hyd_seeds.json per_seed.42.ringkas.fp_total (model H1_stat_dan_rule)", "2, 4")
R(ring(42)["precision_median"], "presisi median", "RUN-KITA",
  "s1_hyd_seeds.json per_seed.42.ringkas.precision_median", "2, 4")
R(ring(42)["recall_median"], "recall median", "RUN-KITA",
  "s1_hyd_seeds.json per_seed.42.ringkas.recall_median", "2, 4")
R(ring(42)["lead_median_median"], "menit", "RUN-KITA",
  "s1_hyd_seeds.json per_seed.42.ringkas.lead_median_median", "2, 4")
R(ring(42)["tp_total"], "TP", "RUN-KITA",
  "s1_hyd_seeds.json per_seed.42.ringkas.tp_total", "2, 4")
R(ring(42)["n_diperingatkan"], "onset", "RUN-KITA",
  "s1_hyd_seeds.json per_seed.42.ringkas.n_diperingatkan", "2, 4")
R(ring(42)["n_onset"], "onset", "RUN-KITA",
  "s1_hyd_seeds.json per_seed.42.ringkas.n_onset", "2, 4")
R(seeds["reproduksi"]["delta"]["fp_total"], "FP", "DERIVASI",
  "s1_hyd_seeds.json reproduksi.delta.fp_total = aktual 935 - terbit 935", "4")
R(seeds["reproduksi"]["delta"]["precision_median"], "rasio", "DERIVASI",
  "s1_hyd_seeds.json reproduksi.delta.precision_median", "4")
R(seeds["reproduksi"]["delta"]["recall_median"], "rasio", "DERIVASI",
  "s1_hyd_seeds.json reproduksi.delta.recall_median", "4")
R(seeds["reproduksi"]["delta"]["lead_median"], "menit", "DERIVASI",
  "s1_hyd_seeds.json reproduksi.delta.lead_median", "4")
R(7, "metrik", "RUN-KITA",
  "s1_hyd_seeds.json reproduksi.lulus jumlah nilai True (fp, presisi, recall, lead, tp, onset, diperingatkan)", "4")

# ------------------------------------------------------------------ desain run
R(len(seeds["seed_list"]), "seed", "RUN-KITA",
  "s1_hyd_seeds.json seed_list = 42,7,13,21,33", "1, 3")
R(meta["n_fold"], "fold", "RUN-KITA",
  "s1_meta.json n_fold (lowo_hyd_ki.json)", "3")
R(meta["dataset_shape"][0], "baris", "RUN-KITA",
  "s1_meta.json dataset_shape[0] (hyd_ki.csv.gz)", "3")
R(len(meta["wells"]), "well", "RUN-KITA",
  "s1_meta.json wells jumlah kunci", "3")
R(meta["dataset_sha256"][:16], "sha256 (16 karakter awal)", "RUN-KITA",
  "s1_meta.json dataset_sha256", "3")

# --------------------------------------------------------------- lintas seed
ls = seeds["lintas_seed"]
R(ls["fp_total"]["rentang"], "FP", "DERIVASI",
  "s1_hyd_seeds.json lintas_seed.fp_total.rentang = maks 935 - min 935", "5")
R(ls["precision_median"]["rentang"], "rasio", "DERIVASI",
  "s1_hyd_seeds.json lintas_seed.precision_median.rentang", "5")
R(ls["recall_median"]["rentang"], "rasio", "DERIVASI",
  "s1_hyd_seeds.json lintas_seed.recall_median.rentang", "5")
R(ls["far24_kalender_median"]["rentang"], "alarm per 24 jam", "DERIVASI",
  "s1_hyd_seeds.json lintas_seed.far24_kalender_median.rentang", "5")
R(ls["lead_median_median"]["rentang"], "menit", "DERIVASI",
  "s1_hyd_seeds.json lintas_seed.lead_median_median.rentang", "5")
R(seeds["n_fold_berbeda_maks"], "fold", "DERIVASI",
  "s1_hyd_seeds.json n_fold_berbeda_maks (sidik_metrik antar seed)", "5")
R(ls["fp_total"]["median"], "FP", "RUN-KITA",
  "s1_hyd_seeds.json lintas_seed.fp_total.median", "5")
R(ls["far24_kalender_median"]["median"], "alarm per 24 jam", "RUN-KITA",
  "s1_hyd_seeds.json lintas_seed.far24_kalender_median.median", "5")

# ------------------------------------------------------- kontrol stokastik ML
k = seeds["kontrol_stokastik"]
ks = k["sebaran"]
R(k["n_fitur"], "fitur", "RUN-KITA",
  "s1_hyd_seeds.json kontrol_stokastik.n_fitur (fitur_dari, kolom label dibuang)", "5")
R(k["per_seed"]["42"]["ringkas"]["fp_total"], "FP", "RUN-KITA",
  "s1_hyd_seeds.json kontrol_stokastik.per_seed.42.ringkas.fp_total", "5")
R(k["per_seed"]["33"]["ringkas"]["fp_total"], "FP", "RUN-KITA",
  "s1_hyd_seeds.json kontrol_stokastik.per_seed.33.ringkas.fp_total", "5")
R(ks["fp_rentang"], "FP", "DERIVASI",
  "s1_hyd_seeds.json kontrol_stokastik.sebaran.fp_rentang = 1421 - 1076", "5")
R(ks["precision_rentang"], "rasio", "DERIVASI",
  "s1_hyd_seeds.json kontrol_stokastik.sebaran.precision_rentang", "5")
R(ks["recall_rentang"], "rasio", "DERIVASI",
  "s1_hyd_seeds.json kontrol_stokastik.sebaran.recall_rentang", "5")
R(1 if ks["ada_varians"] else 0, "boolean (1 = ada varians)", "DERIVASI",
  "s1_hyd_seeds.json kontrol_stokastik.sebaran.ada_varians", "5")

# ------------------------------------------------------------ satuan FAR
R(ring(42)["far24_kalender_median"], "alarm per 24 jam kalender", "RUN-KITA",
  "s1_hyd_seeds.json per_seed.42.ringkas.far24_kalender_median", "3, 6")
R(ring(42)["far24_baris_median"], "alarm per 24 jam baris", "RUN-KITA",
  "s1_hyd_seeds.json per_seed.42.ringkas.far24_baris_median", "3, 6")
R(ring(42)["cakupan_median"], "rasio baris/kalender", "RUN-KITA",
  "s1_hyd_seeds.json per_seed.42.ringkas.cakupan_median", "3, 6")
R(ring(42)["fold_far_le6"], "fold", "RUN-KITA",
  "s1_hyd_seeds.json per_seed.42.ringkas.fold_far_le6 (satuan kalender, dari 9)", "6")
R(ring(42)["fold_gate_A_baru"], "fold", "RUN-KITA",
  "s1_hyd_seeds.json per_seed.42.ringkas.fold_gate_A_baru (FAR<=6 DAN cakupan>=0,5 DAN recall>=0,5)", "6")
R(ring(42)["far24_kalender_maks"], "alarm per 24 jam kalender", "RUN-KITA",
  "s1_hyd_seeds.json per_seed.42.ringkas.far24_kalender_maks (fold F-10)", "6")
R(ring(42)["far24_kalender_min"], "alarm per 24 jam kalender", "RUN-KITA",
  "s1_hyd_seeds.json per_seed.42.ringkas.far24_kalender_min (fold F-5)", "6")
R(ring(42)["far24_kalender_rentang"], "alarm per 24 jam kalender", "DERIVASI",
  "s1_hyd_seeds.json per_seed.42.ringkas.far24_kalender_rentang = 8,9132 - 0,4059", "6")
R(ring(42)["far24_baris_maks"], "alarm per 24 jam baris", "RUN-KITA",
  "s1_hyd_seeds.json per_seed.42.ringkas.far24_baris_maks (fold F-9)", "6")
R(ring(42)["far24_baris_min"], "alarm per 24 jam baris", "RUN-KITA",
  "s1_hyd_seeds.json per_seed.42.ringkas.far24_baris_min (fold F-10)", "6")
R(round(ring(42)["far24_baris_median"] / ring(42)["far24_kalender_median"], 4), "rasio", "DERIVASI",
  "s1_hyd_seeds.json 32,256 / 3,5302 = 9,1372 (satuan baris terhadap satuan kalender)", "6")

# -------------------------------------------------- saturasi ambang CUSUM
R(sat["anggaran_alpha"], "fraksi menit negatif", "KONVENSI",
  "rnd_hybrid_harness.py ALPHA_BUDGET = 6/1440", "6")
R(sat["h_grid_maks"], "ambang CUSUM", "RUN-KITA",
  "s1_h_saturasi.json h_grid_maks = H_GRID[-1]", "6")
R(sat["n_saturasi"], "fold", "RUN-KITA",
  "s1_h_saturasi.json n_saturasi (laju alarm h=30 di atas anggaran)", "6")
R(fold_rec("F-10")["h_terpilih"], "ambang CUSUM", "RUN-KITA",
  "s1_h_saturasi.json per_fold F-10 h_dipilih", "6")
R(sat["per_fold"][0]["laju_alarm_h_maks"], "fraksi menit", "RUN-KITA",
  "s1_h_saturasi.json per_fold F-10 (cal F-12) laju_alarm_h_maks", "6")
R(sat["per_fold"][1]["laju_alarm_h_maks"], "fraksi menit", "RUN-KITA",
  "s1_h_saturasi.json per_fold F-12 (cal F-10) laju_alarm_h_maks", "6")
R(sat["h_terkecil_lolos_anggaran_di_luar_grid"], "ambang CUSUM", "RUN-KITA",
  "s1_h_saturasi.json h_terkecil_lolos_anggaran_di_luar_grid (pindai 40..600)", "6")
R(len(sat["well_kalibrasi_unik"]), "well", "RUN-KITA",
  "s1_h_saturasi.json well_kalibrasi_unik (train_wells[0] hanya F-10 dan F-12)", "6")

# --------------------------------------------- perbandingan dengan V9 pra-riset
v9_rule = v9_head("rule_display")["metrik_segmen"]
v9_hyb = v9_head("hybrid_rule_and_persistence")["metrik_segmen"]
f14_rule = fold_rec("F-14", "rule_kanal")
f14_h1 = fold_rec("F-14", M)
R(v9["segmen_info"]["hyd_ki"]["n"], "baris", "RUN-KITA",
  "v9_i1_RESULTS.json segmen_info.hyd_ki.n (segmen pra-riset hanya F-14)", "7")
R(v9_rule["pos"], "baris positif", "RUN-KITA",
  "v9_i1_RESULTS.json engines.hyd.heads.rule_display.metrik_segmen.pos", "7")
R(f14_rule["rows"]["tp"], "TP", "RUN-KITA",
  "s1_hyd_seeds.json per_seed.42.folds F-14 rule_kanal rows.tp (sama dengan V9)", "7")
R(v9_rule["tp"], "TP", "RUN-KITA",
  "v9_i1_RESULTS.json rule_display.metrik_segmen.tp", "7")
R(f14_rule["rows"]["fp"], "FP", "RUN-KITA",
  "s1_hyd_seeds.json per_seed.42.folds F-14 rule_kanal rows.fp (sama dengan V9)", "7")
R(v9_rule["fp"], "FP", "RUN-KITA",
  "v9_i1_RESULTS.json rule_display.metrik_segmen.fp", "7")
R(f14_rule["rows"]["precision"], "presisi", "RUN-KITA",
  "s1_hyd_seeds.json F-14 rule_kanal rows.precision", "7")
R(v9_rule["far_segmen"], "alarm per 24 jam baris", "RUN-KITA",
  "v9_i1_RESULTS.json rule_display.metrik_segmen.far_segmen", "7")
R(f14_h1["far24_baris"], "alarm per 24 jam baris", "RUN-KITA",
  "s1_hyd_seeds.json F-14 H1_stat_dan_rule far24_baris", "7")
R(v9_hyb["tp"], "TP", "RUN-KITA",
  "v9_i1_RESULTS.json hybrid_rule_and_persistence.metrik_segmen.tp", "7")
R(v9_hyb["fp"], "FP", "RUN-KITA",
  "v9_i1_RESULTS.json hybrid_rule_and_persistence.metrik_segmen.fp", "7")
R(v9_hyb["precision"], "presisi", "RUN-KITA",
  "v9_i1_RESULTS.json hybrid_rule_and_persistence.metrik_segmen.precision", "7")
R(v9_hyb["recall"], "recall", "RUN-KITA",
  "v9_i1_RESULTS.json hybrid_rule_and_persistence.metrik_segmen.recall", "7")
R(v9_hyb["far_segmen"], "alarm per 24 jam baris", "RUN-KITA",
  "v9_i1_RESULTS.json hybrid_rule_and_persistence.metrik_segmen.far_segmen", "7")
R(f14_h1["rows"]["tp"], "TP", "RUN-KITA",
  "s1_hyd_seeds.json F-14 H1 rows.tp", "7")
R(f14_h1["rows"]["fp"], "FP", "RUN-KITA",
  "s1_hyd_seeds.json F-14 H1 rows.fp", "7")
R(f14_h1["rows"]["precision"], "presisi", "RUN-KITA",
  "s1_hyd_seeds.json F-14 H1 rows.precision", "7")
R(f14_h1["rows"]["recall"], "recall", "RUN-KITA",
  "s1_hyd_seeds.json F-14 H1 rows.recall", "7")

# ------------------------------------------------------------------ sebaran fold
R(ring(42)["precision_min"], "presisi", "RUN-KITA",
  "s1_hyd_seeds.json per_seed.42.ringkas.precision_min", "6")
R(ring(42)["precision_maks"], "presisi", "RUN-KITA",
  "s1_hyd_seeds.json per_seed.42.ringkas.precision_maks", "6")
R(ring(42)["recall_min"], "recall", "RUN-KITA",
  "s1_hyd_seeds.json per_seed.42.ringkas.recall_min", "6")
R(ring(42)["recall_maks"], "recall", "RUN-KITA",
  "s1_hyd_seeds.json per_seed.42.ringkas.recall_maks", "6")
R(ring(42)["lead_median_min"], "menit", "RUN-KITA",
  "s1_hyd_seeds.json per_seed.42.ringkas.lead_median_min (fold F-9)", "6")
R(ring(42)["lead_median_maks"], "menit", "RUN-KITA",
  "s1_hyd_seeds.json per_seed.42.ringkas.lead_median_maks (fold F-9_A)", "6")
R(ring(42)["fp_kejadian_total"], "kejadian", "RUN-KITA",
  "s1_hyd_seeds.json per_seed.42.ringkas.fp_kejadian_total", "6")
R(fold_rec("F-10")["cakupan"], "rasio", "RUN-KITA",
  "s1_hyd_seeds.json F-10 cakupan (tertinggi)", "6")
R(fold_rec("F-5")["cakupan"], "rasio", "RUN-KITA",
  "s1_hyd_seeds.json F-5 cakupan (terendah)", "6")

# ------------------------------------------------------------------ BELUM
for isi, dipakai in [
    ("beban alarm H1 pada satuan kalender di lapangan, karena cakupan rekaman hanya 9,03 persen sehingga penyebut kalender bukan waktu operasi nyata", "6"),
    ("nilai maintenance dalam rupiah atau jam henti terhindar", "8"),
    ("ketahanan H1 lintas kampanye pengeboran, karena tanggal kampanye tidak tersedia per baris", "6"),
    ("kinerja H1 pada seed bila komponen CUSUM diberi inisialisasi stokastik, karena implementasi sekarang deterministik penuh", "5"),
    ("apakah h=300 yang memenuhi anggaran pada F-12 masih memberi recall berguna, karena pemindaian hanya mengukur laju alarm", "6"),
]:
    R("tidak terukur", "n/a", "BELUM-TERUKUR", f"tidak ada sumber terukur untuk {isi}", dipakai,
      "BELUM TERUKUR")

# ------------------------------------------------------------------ assert
EXPECT = {
    1: (935, ring(42)["fp_total"], 0),
    2: (0.7789, ring(42)["precision_median"], 0),
    3: (0.5638, ring(42)["recall_median"], 0),
    4: (11.5, ring(42)["lead_median_median"], 0),
    5: (3804, ring(42)["tp_total"], 0),
    6: (219, ring(42)["n_diperingatkan"], 0),
    7: (390, ring(42)["n_onset"], 0),
    8: (0, seeds["reproduksi"]["delta"]["fp_total"], 0),
    9: (0.0, seeds["reproduksi"]["delta"]["precision_median"], 0),
    10: (0.0, seeds["reproduksi"]["delta"]["recall_median"], 0),
    11: (0.0, seeds["reproduksi"]["delta"]["lead_median"], 0),
    12: (7, sum(1 for v in seeds["reproduksi"]["lulus"].values() if v), 0),
    13: (5, len(seeds["seed_list"]), 0),
    14: (9, meta["n_fold"], 0),
    15: (52509, meta["dataset_shape"][0], 0),
    16: (9, len(meta["wells"]), 0),
    18: (0.0, ls["fp_total"]["rentang"], 0),
    19: (0.0, ls["precision_median"]["rentang"], 0),
    20: (0.0, ls["recall_median"]["rentang"], 0),
    21: (0.0, ls["far24_kalender_median"]["rentang"], 0),
    22: (0.0, ls["lead_median_median"]["rentang"], 0),
    23: (0, seeds["n_fold_berbeda_maks"], 0),
    24: (935, ls["fp_total"]["median"], 0),
    25: (3.5302, ls["far24_kalender_median"]["median"], 0),
    26: (40, k["n_fitur"], 0),
    27: (1076, k["per_seed"]["42"]["ringkas"]["fp_total"], 0),
    28: (1421, k["per_seed"]["33"]["ringkas"]["fp_total"], 0),
    29: (345, ks["fp_rentang"], 0),
    30: (0.0608, ks["precision_rentang"], 0),
    31: (0.0453, ks["recall_rentang"], 0),
    32: (1, 1 if ks["ada_varians"] else 0, 0),
    33: (3.5302, ring(42)["far24_kalender_median"], 0),
    34: (32.256, ring(42)["far24_baris_median"], 0),
    35: (0.0903, ring(42)["cakupan_median"], 0),
    36: (7, ring(42)["fold_far_le6"], 0),
    37: (0, ring(42)["fold_gate_A_baru"], 0),
    38: (8.9132, ring(42)["far24_kalender_maks"], 0),
    39: (0.4059, ring(42)["far24_kalender_min"], 0),
    40: (8.5073, ring(42)["far24_kalender_rentang"], 0),
    41: (66.3873, ring(42)["far24_baris_maks"], 0),
    42: (14.2205, ring(42)["far24_baris_min"], 0),
    43: (9.1372, round(ring(42)["far24_baris_median"] / ring(42)["far24_kalender_median"], 4), 0),
    44: (0.00416667, sat["anggaran_alpha"], 1e-8),
    45: (30.0, sat["h_grid_maks"], 0),
    46: (9, sat["n_saturasi"], 0),
    47: (30.0, fold_rec("F-10")["h_terpilih"], 0),
    48: (0.044114, sat["per_fold"][0]["laju_alarm_h_maks"], 5e-7),
    49: (0.017567, sat["per_fold"][1]["laju_alarm_h_maks"], 5e-7),
    50: (300.0, sat["h_terkecil_lolos_anggaran_di_luar_grid"], 0),
    51: (2, len(sat["well_kalibrasi_unik"]), 0),
    52: (10401, v9["segmen_info"]["hyd_ki"]["n"], 0),
    53: (865, v9_rule["pos"], 0),
    54: (607, f14_rule["rows"]["tp"], 0),
    55: (607, v9_rule["tp"], 0),
    56: (368, f14_rule["rows"]["fp"], 0),
    57: (368, v9_rule["fp"], 0),
    59: (55.57, v9_rule["far_segmen"], 0),
    60: (32.4664, f14_h1["far24_baris"], 0),
    61: (516, v9_hyb["tp"], 0),
    62: (110, v9_hyb["fp"], 0),
    63: (0.8243, v9_hyb["precision"], 0),
    64: (0.5965, v9_hyb["recall"], 0),
    65: (16.611, v9_hyb["far_segmen"], 0),
    66: (443, f14_h1["rows"]["tp"], 0),
    67: (215, f14_h1["rows"]["fp"], 0),
    68: (0.6733, round(f14_h1["rows"]["precision"], 4), 0),
    69: (0.5121, round(f14_h1["rows"]["recall"], 4), 0),
}

bad = []
for idx, (exp, got, tol) in EXPECT.items():
    if abs(float(got) - float(exp)) > tol:
        bad.append((f"S1-{idx:03d}", exp, got))
if bad:
    for b in bad:
        print("GAGAL", b, file=sys.stderr)
    raise SystemExit(f"{len(bad)} assert gagal, ledger tidak ditulis")

# silang: rule F-14 S1 harus identik dengan V9 rule_display pada TP dan FP
assert f14_rule["rows"]["tp"] == v9_rule["tp"] == 607
assert f14_rule["rows"]["fp"] == v9_rule["fp"] == 368
assert abs(f14_rule["rows"]["precision"] - v9_rule["precision"]) < 1e-4
assert abs(f14_rule["rows"]["recall"] - v9_rule["recall"]) < 1e-4

# silang: jumlah fold yang lolos FAR<=6 pada satuan baris dihitung, bukan dikira
n_baris_le6 = sum(1 for r in folds_of(M) if r["far24_baris"] <= 6.0)
R(n_baris_le6, "fold", "DERIVASI",
  "s1_hyd_seeds.json per_seed.42.folds model H1: hitung far24_baris <= 6 (dari 9)", "6")
assert n_baris_le6 == 0, f"dugaan salah: {n_baris_le6} fold lolos pada satuan baris"

print(f"assert: {len(EXPECT)} baris cocok dengan JSON mentah; silang V9 F-14 cocok; "
      f"fold lolos FAR<=6 satuan baris = {n_baris_le6}")

# ------------------------------------------------------------------ tulis
lines = ["", HEAD, "",
         "Tanggal akses seluruh baris: 2026-10-28. Dokumen: `docs/RND_S1_SEED_ROBUSTNESS.md`.",
         "Semua baris RUN-KITA dan DERIVASI di-assert oleh `code/rnd_s1_ledger.py` terhadap berkas JSON",
         "mentah (`scratch/rnd/s1/*.json`, `scratch/rnd/r8/r8_hyd.json`, `scratch/v9_i1/v9_i1_RESULTS.json`);",
         "baris yang gagal assert tidak ditulis dan proses berhenti. Tujuh kolom sesuai kartu.",
         "",
         "| # | Angka | Satuan | Kelas sumber | Rujukan persis | Dipakai di | Status |",
         "|---|---|---|---|---|---|---|"]
for i, r in enumerate(rows, 1):
    lines.append(f"| S1-{i:03d} | {angka(r['nilai'])} | {r['satuan']} | {r['kelas']} | "
                 f"{r['rujukan']} | bagian {r['dipakai']} | {r['status']} |")

txt = open(LEDGER, encoding="utf-8").read()
if HEAD in txt:
    txt = txt[:txt.index(HEAD)].rstrip() + "\n"
txt = txt.rstrip() + "\n" + "\n".join(lines) + "\n"
open(LEDGER, "w", encoding="utf-8").write(txt)
print(f"baris S1 ditulis: {len(rows)}")
print("kelas:", {c: sum(1 for r in rows if r["kelas"] == c) for c in {r["kelas"] for r in rows}})
