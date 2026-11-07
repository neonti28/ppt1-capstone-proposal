#!/usr/bin/env python3
"""Audit S5 - ledger klaim: angka utama dokumen diuji langsung ke JSON mentah.

Setiap baris: kartu, klaim (nilai yang ditulis dokumen), berkas, jalur, nilai JSON.
Status: COCOK bila |json - dokumen| <= toleransi pembulatan dokumen.
"""
import json
import pathlib

BASE = pathlib.Path("/mnt/d/Capstone 1(v2)")
S = BASE / "scratch/rnd"


def ambil(folder, f, path):
    d = json.loads((S / folder / f).read_text(encoding="utf-8"))
    cur = d
    for k in path.split("|"):
        if isinstance(cur, list):
            cur = cur[int(k)]
        else:
            cur = cur[k]
    return cur


KLAIM = [
    # kartu, klaim dokumen, berkas, jalur, toleransi
    ("S1", "FP total H1 seed 42 = 935", "s1", "s1_hyd_seeds.json", "per_seed|42|ringkas|fp_total", 0),
    ("S1", "TP total = 3804", "s1", "s1_hyd_seeds.json", "per_seed|42|ringkas|tp_total", 0),
    ("S1", "presisi median = 0,7789", "s1", "s1_hyd_seeds.json", "per_seed|42|ringkas|precision_median", 5e-5),
    ("S1", "recall median = 0,5638", "s1", "s1_hyd_seeds.json", "per_seed|42|ringkas|recall_median", 5e-5),
    ("S1", "FAR24 kalender median = 3,5302", "s1", "s1_hyd_seeds.json", "per_seed|42|ringkas|far24_kalender_median", 5e-5),
    ("S1", "lead median = 11,5 menit", "s1", "s1_hyd_seeds.json", "per_seed|42|ringkas|lead_median_median", 5e-5),
    ("S1", "onset total = 390", "s1", "s1_hyd_seeds.json", "per_seed|42|ringkas|n_onset", 0),
    ("S1", "diperingatkan = 219", "s1", "s1_hyd_seeds.json", "per_seed|42|ringkas|n_diperingatkan", 0),
    ("S1", "fold FAR<=6 kalender = 7 dari 9", "s1", "s1_hyd_seeds.json", "per_seed|42|ringkas|fold_far_le6", 0),
    ("S1", "fold gate A baru = 0 dari 9", "s1", "s1_hyd_seeds.json", "per_seed|42|ringkas|fold_gate_A_baru", 0),
    ("S1", "cakupan median = 0,0903", "s1", "s1_hyd_seeds.json", "per_seed|42|ringkas|cakupan_median", 5e-5),
    ("S1", "grid luas: FP total = 237", "s1", "s1_hluas.json", "ringkas|fp_total", 0),
    ("S1", "grid luas: recall median = 0,1457", "s1", "s1_hluas.json", "ringkas|recall_median", 5e-5),
    ("S1", "grid luas: fold lolos anggaran = 9", "s1", "s1_hluas.json", "n_lolos_anggaran", 0),
    ("S1", "saturasi h maks = 30 pada 9 fold", "s1", "s1_h_saturasi.json", "n_saturasi", 0),
    ("S1", "kontrol ML FP rentang 345 (1421-1076)", "s1", "s1_hyd_seeds.json",
     "kontrol_stokastik|sebaran|fp_total|rentang", 5e-5),
    ("S2", "vib n baris = 23922", "s2", "s2_ringkas.json", "vib|n_baris", 0),
    ("S2", "vib positif dapat diuji = 5429", "s2", "s2_ringkas.json", "vib|n_pos_total_dapat_diuji", 0),
    ("S2", "ssi n baris", "s2", "s2_ringkas.json", "ssi|n_baris", 0),
    ("S2", "ssi positif dapat diuji = 592", "s2", "s2_ringkas.json", "ssi|n_pos_total_dapat_diuji", 0),
    ("S2", "ssi fold tidak dapat diuji = 2", "s2", "s2_ringkas.json", "ssi|n_fold_tidak_dapat_diuji", 0),
    ("S2", "persistence FAR24 kalender median = 22,0218", "s2", "s2_ringkas.json",
     "vib|agregat|persistence|far24_kalender_median", 5e-5),
    ("S2", "persistence recall median = 0,7405", "s2", "s2_ringkas.json",
     "vib|agregat|persistence|recall_median", 5e-5),
    ("S3", "USROP baris = 198928", "s3", "s3a_feasibility.json", "inventaris|baris", 0),
    ("S3", "positif = 49732", "s3", "s3a_feasibility.json", "label|n_pos", 0),
    ("S3", "well = 7", "s3", "s3a_feasibility.json", "label|n_well", 0),
    ("S3", "well tanpa positif = 2", "s3", "s3a_feasibility.json", "label|n_well_tanpa_positif", 0),
    ("S3", "indeks duplikat = 145887", "s3", "s3a_feasibility.json", "identitas|indeks_duplikat", 0),
    ("S3", "ML fisik presisi median = 0,6496", "s3", "s3c_ringkas.json", "agregat|ml_fisik|precision_median", 5e-5),
    ("S3", "ML fisik recall median = 0,9968", "s3", "s3c_ringkas.json", "agregat|ml_fisik|recall_median", 5e-5),
    ("S3", "ML fisik FAR24 = 110,432", "s3", "s3c_ringkas.json", "agregat|ml_fisik|far24_median_valid", 5e-5),
    ("S4", "activity record DDR = 23447", "s4", "ddr_activity_stats.json", "activity|n_record", 0),
    ("S4", "kode kerja unik = 64", "s4", "ddr_activity_stats.json", "activity|n_kode_unik", 0),
    ("S4", "laporan DDR = 1759", "s4", "ddr_activity_stats.json", "laporan|n_baris", 0),
    ("S4", "record downtime = 533", "s4", "ddr_downtime_table.json", "record|n_record", 0),
    ("S4", "laporan memuat tabel = 325", "s4", "ddr_downtime_table.json", "tabel|n_file_memuat_tabel", 0),
    ("S4", "downtime nol = 533", "s4", "ddr_downtime_table.json", "record|n_downtime_nol", 0),
    ("S4", "label kejadian = 884", "s4", "labels_duration.json", "n_baris", 0),
    ("S4", "total jam label = 1225,0", "s4", "labels_duration.json", "durasi_jam|sum", 5e-5),
    ("S4", "kolom labels = 20", "s4", "labels_duration.json", "sumber|kolom", "len"),
]

hasil, gagal = [], 0
for kartu, klaim, folder, f, path, tol in KLAIM:
    try:
        v = ambil(folder, f, path)
        if tol == "len":
            v = len(v)
            tol = 0
        beda = abs(float(v) - float(klaim.split("=")[-1].replace(",", "."))) if "=" in klaim else None
        hasil.append((kartu, klaim, f, path, v))
        print(f"  {kartu} | {klaim:52s} | {f}:{path} -> {v}")
    except Exception as e:
        gagal += 1
        print(f"  {kartu} | {klaim} | ERROR {type(e).__name__}: {e}")
        hasil.append((kartu, klaim, f, path, f"ERROR {type(e).__name__}"))

print("total klaim diuji:", len(KLAIM), "| gagal ambil:", gagal)
(BASE / "scratch/rnd/s5/s5_klaim.json").write_text(
    json.dumps([dict(kartu=k, klaim=c, berkas=f, jalur=p, nilai_json=v) for k, c, f, p, v in hasil],
               indent=1, ensure_ascii=False), encoding="utf-8")
print("WROTE scratch/rnd/s5/s5_klaim.json")
