"""S4-F: gabung semua bukti menjadi inventory.json + metrik lapisan B terhitung.

Input (semua dari eksekusi nyata di scratch/rnd/s4/):
  ddr_activity_stats.json, labels_duration.json, inventory_raw.json,
  ddr_downtime_table.json, crosscheck.json
Keluaran: scratch/rnd/s4/inventory.json

Setiap angka penting di-assert terhadap sumbernya, supaya dokumen tidak bisa
menyimpang dari JSON mentah.
"""
import os, json

ROOT = "/mnt/d/Capstone 1(v2)"
S4 = os.path.join(ROOT, "scratch/rnd/s4")
OUT = os.path.join(S4, "inventory.json")

def load(name):
    with open(os.path.join(S4, name), encoding="utf-8") as f:
        return json.load(f)

ddr = load("ddr_activity_stats.json")
lab = load("labels_duration.json")
raw = load("inventory_raw.json")
dt = load("ddr_downtime_table.json")
cc = load("crosscheck.json")

# ---------- ASSERT angka kunci terhadap sumber ----------
a = ddr["activity"]
assert ddr["laporan"]["n_baris"] == 1759, ddr["laporan"]["n_baris"]
assert a["n_record"] == 23447, a["n_record"]
assert a["n_laporan_punya_activity"] == 1750, a["n_laporan_punya_activity"]
assert a["n_kode_unik"] == 64, a["n_kode_unik"]
assert abs(a["interruption"]["total_jam"] - 8343.253) < 1e-6, a["interruption"]["total_jam"]
assert a["interruption"]["total_record"] == 3577, a["interruption"]["total_record"]
assert abs(a["maintenance_terkait"]["total_jam"] - 1777.75) < 1e-6, a["maintenance_terkait"]["total_jam"]
assert a["maintenance_terkait"]["total_record"] == 1116, a["maintenance_terkait"]["total_record"]
assert a["state_fail_durasi"]["n"] == 480, a["state_fail_durasi"]["n"]
assert abs(a["state_fail_durasi"]["sum_jam"] - 1265.5) < 1e-6, a["state_fail_durasi"]["sum_jam"]
assert abs(a["total_jam_semua_activity"] - 39397.986) < 1e-6, a["total_jam_semua_activity"]

assert lab["n_baris"] == 884, lab["n_baris"]
assert lab["n_durasi_valid"] == 884, lab["n_durasi_valid"]
assert abs(lab["durasi_jam"]["sum"] - 1225.0) < 1e-6, lab["durasi_jam"]["sum"]
assert lab["durasi_jam"]["median"] == 0.75, lab["durasi_jam"]["median"]

assert raw["pindai_xml_ddr"]["n_file_dibaca"] == 1759, raw["pindai_xml_ddr"]["n_file_dibaca"]
assert raw["pindai_html_ddr"]["n_file_dibaca"] == 1759, raw["pindai_html_ddr"]["n_file_dibaca"]
# biaya: harus nol kemunculan di kedua format
assert "cost" not in raw["pindai_xml_ddr"]["kemunculan"], raw["pindai_xml_ddr"]["kemunculan"].get("cost")
assert "cost" not in raw["pindai_html_ddr"]["kemunculan"], raw["pindai_html_ddr"]["kemunculan"].get("cost")
assert "work order" not in raw["pindai_xml_ddr"]["kemunculan"]
assert "workorder" not in raw["pindai_xml_ddr"]["kemunculan"]

assert dt["tabel"]["n_file_memuat_tabel"] == 325, dt["tabel"]["n_file_memuat_tabel"]
assert dt["record"]["n_record"] == 533, dt["record"]["n_record"]
assert dt["record"]["n_downtime_nol"] == 533, dt["record"]["n_downtime_nol"]
assert dt["record"]["n_downtime_positif"] == 0, dt["record"]["n_downtime_positif"]

assert cc["silang_total"]["ddr_interruption_n"] == 3577, cc["silang_total"]
assert abs(cc["silang_total"]["labels_jam"] - 1225.0) < 1e-6, cc["silang_total"]
assert cc["pres_test_type"]["distribusi"]["formation integrity test"] == 1072, cc["pres_test_type"]["distribusi"]

# ---------- metrik lapisan B yang benar-benar dapat dihitung ----------
N_LAPORAN_HARIAN = ddr["laporan"]["n_baris"]
rep = a["durasi_per_kode"]["interruption -- repair"]
mnt = a["durasi_per_kode"]["interruption -- maintain"]

metrics = {
    "B1_henti_perbaikan_per_kejadian": {
        "definisi": "durasi record activity DDR berkode 'interruption -- repair' (dTimEnd - dTimStart)",
        "n_kejadian": rep["n"], "total_jam": rep["sum_jam"],
        "median_jam": rep["median_jam"], "p90_jam": rep["p90_jam"], "max_jam": rep["max_jam"],
        "sumber": "scratch/rnd/s4/ddr_activity_stats.json -> activity.durasi_per_kode['interruption -- repair']",
    },
    "B2_henti_maintenance_per_kejadian": {
        "definisi": "durasi record activity DDR berkode 'interruption -- maintain'",
        "n_kejadian": mnt["n"], "total_jam": mnt["sum_jam"],
        "median_jam": mnt["median_jam"], "p90_jam": mnt["p90_jam"], "max_jam": mnt["max_jam"],
        "sumber": "scratch/rnd/s4/ddr_activity_stats.json -> activity.durasi_per_kode['interruption -- maintain']",
    },
    "B3_henti_maintenance_gabungan": {
        "definisi": "repair + maintain (dua kode kerja maintenance di taksonomi DDR)",
        "n_kejadian": a["maintenance_terkait"]["total_record"],
        "total_jam": a["maintenance_terkait"]["total_jam"],
        "per_laporan_harian": round(a["maintenance_terkait"]["total_record"] / N_LAPORAN_HARIAN, 4),
        "jam_per_laporan_harian": round(a["maintenance_terkait"]["total_jam"] / N_LAPORAN_HARIAN, 4),
        "sumber": "scratch/rnd/s4/ddr_activity_stats.json -> activity.maintenance_terkait",
    },
    "B4_henti_kegagalan_peralatan_berlabel": {
        "definisi": "durasi kejadian labels_curated_v2 dengan state_detail == 'equipment failure'",
        "n_kejadian": lab["equipment_failure_state_detail"]["n"],
        "total_jam": lab["equipment_failure_state_detail"]["sum_jam"],
        "median_jam": lab["equipment_failure_state_detail"]["median_jam"],
        "p90_jam": lab["equipment_failure_state_detail"]["p90_jam"],
        "sumber": "scratch/rnd/s4/labels_duration.json -> equipment_failure_state_detail",
    },
    "B5_rasio_kejadian_per_laporan_harian": {
        "definisi": "jumlah kejadian berlabel dibagi jumlah laporan harian DDR (1759)",
        "n_kejadian": lab["n_baris"], "n_laporan": N_LAPORAN_HARIAN,
        "rasio": round(lab["n_baris"] / N_LAPORAN_HARIAN, 4),
        "sumber": "labels_duration.json + ddr_activity_stats.json",
    },
    "B6_cakupan_jam_henti_berlabel": {
        "definisi": "jam kejadian berlabel dibagi jam interruption DDR (seberapa banyak henti yang sudah diberi label)",
        "jam_berlabel": lab["durasi_jam"]["sum"],
        "jam_interruption_ddr": a["interruption"]["total_jam"],
        "rasio": cc["silang_total"]["rasio_jam"],
        "sumber": "scratch/rnd/s4/crosscheck.json -> silang_total.rasio_jam",
    },
    "B7_peringatan_terhadap_durasi_henti": {
        "definisi": "lead median engine (dari R8/S1, menit) dibanding durasi henti repair median (jam)",
        "lead_menit_h1_hyd": 11.5,
        "lead_menit_rule_hyd": 6.0,
        "henti_repair_median_jam": rep["median_jam"],
        "henti_repair_p90_jam": rep["p90_jam"],
        "cakupan_lead_h1_persen_dari_median": round(100.0 * 11.5 / (rep["median_jam"] * 60.0), 2),
        "cakupan_lead_h1_persen_dari_p90": round(100.0 * 11.5 / (rep["p90_jam"] * 60.0), 2),
        "catatan": "lead 11,5 menit berasal dari docs/RND_R8_EVALUASI_BERLAPIS.md dan docs/RND_S1_SEED_ROBUSTNESS.md (RUN-KITA), bukan dihitung ulang di kartu ini",
        "sumber": "docs/RND_R8_EVALUASI_BERLAPIS.md (lead H1 11,5 menit; rule 6,0 menit) + ddr_activity_stats.json",
    },
    "B8_beban_alarm_per_kejadian": {
        "definisi": "FP total engine dibagi jumlah kejadian yang dijadikan target (rasio alarm palsu per kejadian)",
        "contoh_h1_hyd": {"fp": 935, "onset": 390, "fp_per_onset": round(935 / 390, 4)},
        "contoh_rule_hyd": {"fp": 2105, "onset": 390, "fp_per_onset": round(2105 / 390, 4)},
        "catatan": "angka FP/onset dari R8, dipakai apa adanya; rasio alarm per INSPEKSI tidak dapat dihitung karena jadwal inspeksi tidak ada",
        "sumber": "docs/RND_R8_EVALUASI_BERLAPIS.md",
    },
}

inv = {
    "kartu": "RND-S4",
    "tujuan": "pendataan lapisan B (inspeksi, work order, jam henti, biaya)",
    "dibuat_wib": "2026-10-28",
    "workspace": ROOT,
    "sumber_mentah": {
        "ddr_activity_stats.json": ddr["sumber"],
        "labels_duration.json": lab["sumber"],
        "inventory_raw.json": {"folder_well_technical_data": raw["folder_total"],
                               "ddr_dokumen_per_format": raw["ddr_dokumen_per_format"],
                               "katalog_volve_baris": raw["katalog_volve"]["n_baris"],
                               "csv_dipindai": raw["csv_di_data"]["n_file"]},
        "ddr_downtime_table.json": dt["sumber"],
        "crosscheck.json": {"silang_total": cc["silang_total"], "pres_test_type": cc["pres_test_type"]["distribusi"]},
    },
    "kelompok": {
        "tersedia_dan_layak": [
            {"id": "S4-C1", "nama": "Record activity DDR (durasi kerja dan henti)",
             "path": "data/volve/ddr.parquet",
             "bytes": ddr["sumber"]["bytes"], "n_baris": ddr["laporan"]["n_baris"],
             "n_record_anak": a["n_record"], "kolom_kunci": ["activity.dTimStart", "activity.dTimEnd", "activity.proprietaryCode", "activity.state", "activity.stateDetailActivity", "activity.comments"],
             "kolom_relevan": "durasi, kode kerja (interruption -- repair/maintain/fish/sidetrack), status ok/fail, komentar tindakan",
             "bukti": "23.447 record, 64 kode, 8.343,253 jam interruption, 1.777,75 jam repair+maintain"},
            {"id": "S4-C2", "nama": "Label kejadian terkurasi dengan waktu mulai dan selesai",
             "path": "data/volve/labels_curated_v2.csv",
             "bytes": lab["sumber"]["bytes"], "n_baris": lab["n_baris"],
             "kolom_kunci": ["act_start", "act_end", "category", "state_detail", "source_code", "outcome", "component"],
             "kolom_relevan": "durasi henti, kategori kegagalan, hasil tindakan (repaired/removed/installed/monitored)",
             "bukti": "884 kejadian, 100 persen durasi valid, total 1.225,0 jam, median 0,75 jam"},
            {"id": "S4-C3", "nama": "Taksonomi kode kerja DDR sebagai pengganti kode work order",
             "path": "data/volve/ddr.parquet (kolom activity.proprietaryCode)",
             "n_kode_unik": a["n_kode_unik"],
             "bukti": "10 kode interruption; repair 806 record/1.215,0 jam; maintain 310 record/562,75 jam; inspect 0 record"},
        ],
        "ada_tetapi_tidak_memadai": [
            {"id": "S4-P1", "nama": "Tabel equipment failure per laporan DDR (HTML)",
             "path": "data/volve/external/dbx_volume/Well_technical_data/Daily Drilling Report - HTML Version/*.html (table id equipmentfailureInfoTable)",
             "n_file_memuat": dt["tabel"]["n_file_memuat_tabel"], "n_file_total": dt["sumber"]["n_file_html"],
             "n_record": dt["record"]["n_record"],
             "kolom": dt["tabel"]["kolom"],
             "cacat_terukur": "kolom Operation Downtime (min) bernilai 0 pada 533 dari 533 record; Equipment Repaired bernilai '00:00' pada 533 dari 533 record; hanya 23 dari 533 remark memuat durasi dalam teks",
             "sisa_nilai": "41 kelas sistem peralatan, kedalaman, tanggal, dan remark tekstual tetap dapat dipakai sebagai register kegagalan independen"},
            {"id": "S4-P2", "nama": "Ringkasan 24 jam dan prakiraan 24 jam per laporan",
             "path": "data/volve/ddr.parquet (statusInfo.sum24Hr, statusInfo.forecast24Hr)",
             "cacat_terukur": "teks bebas, tidak terstruktur; tidak ada kuantifikasi jam henti atau biaya"},
            {"id": "S4-P3", "nama": "Uji integritas sumur sebagai catatan uji berjadwal",
             "path": "data/volve/ddr.parquet (statusInfo.presTestType)",
             "n_laporan": cc["pres_test_type"]["n_laporan_dengan_uji"],
             "distribusi": cc["pres_test_type"]["distribusi"],
             "cacat_terukur": "hanya jenis uji (FIT/LOT), tanpa tanggal uji terpisah, tanpa hasil lolos/gagal, dan bukan inspeksi peralatan"},
            {"id": "S4-P4", "nama": "Dokumen DDR versi PDF dan HTML",
             "path": "Daily Drilling Report - HTML Version (1759 file), PDF Version (1759 file), XML Version (1759 file)",
             "cacat_terukur": "isi sama dengan parquet untuk kolom terstruktur; PDF tidak dipindai teks pada kartu ini; tidak menambah kolom biaya"},
            {"id": "S4-P5", "nama": "Katalog target unduhan Volve",
             "path": "data/volve/external/volve_catalog_target_paths.csv",
             "n_baris": raw["katalog_volve"]["n_baris"],
             "kategori": raw["katalog_volve"]["kategori"],
             "cacat_terukur": "tidak memuat kategori laporan inspeksi, work order, atau biaya"},
        ],
        "tidak_ada": [
            {"id": "S4-N1", "nama": "Biaya (cost) per kejadian atau per hari",
             "bukti_ketiadaan": "token 'cost' 0 kemunculan pada 1759 XML DDR dan 0 kemunculan pada 1759 HTML DDR; tidak ada kolom biaya di 17 kolom parquet",
             "dibutuhkan": "nilai biaya per operasi atau per hari dari sistem akuntansi rig (daily cost report), atau tarif rig harian plus durasi henti"},
            {"id": "S4-N2", "nama": "Work order bernomor",
             "bukti_ketiadaan": "token 'work order' dan 'workorder' 0 kemunculan pada 1759 XML DDR",
             "dibutuhkan": "nomor WO, tanggal buka/tutup, vendor, komponen, jam kerja teknisi dari CMMS"},
            {"id": "S4-N3", "nama": "Jadwal inspeksi fisik dan jam orang inspeksi",
             "bukti_ketiadaan": "tidak ada kode activity 'inspect' (0 record dari 23.447); kata 'inspection' hanya muncul di teks bebas 154 kali pada 1759 laporan"},
            {"id": "S4-N4", "nama": "Produksi tertunda (barrel) dan nilai rupiah",
             "bukti_ketiadaan": "tidak ada berkas produksi di workspace (pencarian nama berkas production/onstream/barrel: 0 hasil)"},
            {"id": "S4-N5", "nama": "Durasi henti terstruktur per kegagalan peralatan",
             "bukti_ketiadaan": "kolom Operation Downtime (min) nol pada 533 dari 533 record tabel equipment failure"},
        ],
    },
    "metrik_lapisan_b": metrics,
    "uji_silang": {
        "per_wellbore": cc["silang_per_wellbore"],
        "total": cc["silang_total"],
        "catatan": "rasio jam berlabel terhadap jam interruption DDR 0,1468 secara total, tetapi 1,4033 pada F-9 karena sebagian label berasal dari kode non-interruption (drilling -- casing 135 kejadian, drilling -- trip 63, drilling -- drill 26)",
    },
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(inv, f, ensure_ascii=False, indent=1)
print("WROTE", OUT, os.path.getsize(OUT), "bytes")
print("kelompok: layak", len(inv["kelompok"]["tersedia_dan_layak"]),
      "| tidak memadai", len(inv["kelompok"]["ada_tetapi_tidak_memadai"]),
      "| tidak ada", len(inv["kelompok"]["tidak_ada"]))
print("metrik:", list(metrics.keys()))
print("B7:", metrics["B7_peringatan_terhadap_durasi_henti"])
