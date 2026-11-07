#!/usr/bin/env python3
"""Klaim bernama: nilai dokumen dibandingkan dengan path JSON eksplisit.

Versi ini menggantikan a9_klaim.py yang gagal pada lima entri karena pengurai
teks klaim, bukan karena nilai sumber berbeda. Di sini nilai dokumen ditulis
sebagai teks apa adanya dan diurai terpisah dari nilai JSON.
"""
import json
import pathlib

B = pathlib.Path("/mnt/d/Capstone 1(v2)/scratch/rnd")
OUT = B / "s5/s5_klaim2.json"


def muat(kartu, berkas):
    return json.loads((B / kartu.lower() / berkas).read_text(encoding="utf-8"))


def idr(teks):
    t = teks.replace(" ", "").replace("\u00a0", "")
    if "," in t and "." in t:
        t = t.replace(".", "").replace(",", ".")
    else:
        t = t.replace(",", ".")
    return float(t)


def ambil(d, jalur):
    cur = d
    for k in jalur.split("|"):
        if isinstance(cur, list):
            cur = cur[int(k)]
        else:
            cur = cur[k]
    return cur


# (kartu, label, berkas, jalur, teks nilai pada dokumen, satuan)
K = [
 ("S1", "FP total seed 42", "s1_hyd_seeds.json", "per_seed|42|ringkas|fp_total", "935", "unit"),
 ("S1", "TP total seed 42", "s1_hyd_seeds.json", "per_seed|42|ringkas|tp_total", "3804", "unit"),
 ("S1", "presisi median seed 42", "s1_hyd_seeds.json", "per_seed|42|ringkas|precision_median", "0,7789", "rasio"),
 ("S1", "recall median seed 42", "s1_hyd_seeds.json", "per_seed|42|ringkas|recall_median", "0,5638", "rasio"),
 ("S1", "FAR24 kalender median", "s1_hyd_seeds.json", "per_seed|42|ringkas|far24_kalender_median", "3,5302", "alarm/24 jam"),
 ("S1", "lead median", "s1_hyd_seeds.json", "per_seed|42|ringkas|lead_median_median", "11,5", "menit"),
 ("S1", "onset", "s1_hyd_seeds.json", "per_seed|42|ringkas|n_onset", "390", "kejadian"),
 ("S1", "diperingatkan", "s1_hyd_seeds.json", "per_seed|42|ringkas|n_diperingatkan", "219", "kejadian"),
 ("S1", "fold FAR tidak lebih dari 6", "s1_hyd_seeds.json", "per_seed|42|ringkas|fold_far_le6", "7", "fold"),
 ("S1", "fold gate A baru", "s1_hyd_seeds.json", "per_seed|42|ringkas|fold_gate_A_baru", "0", "fold"),
 ("S1", "cakupan median", "s1_hyd_seeds.json", "per_seed|42|ringkas|cakupan_median", "0,0903", "rasio"),
 ("S1", "FP total dengan grid luas", "s1_hluas.json", "ringkas|fp_total", "237", "unit"),
 ("S1", "recall median dengan grid luas", "s1_hluas.json", "ringkas|recall_median", "0,1457", "rasio"),
 ("S1", "fold lolos anggaran dengan grid luas", "s1_hluas.json", "n_lolos_anggaran", "9", "fold"),
 ("S1", "fold dengan h tersaturasi", "s1_h_saturasi.json", "n_saturasi", "9", "fold"),
 ("S1", "batas atas grid h", "s1_h_saturasi.json", "h_grid_maks", "30", "satuan h"),
 ("S1", "h terkecil lolos di luar grid", "s1_h_saturasi.json", "h_terkecil_lolos_anggaran_di_luar_grid", "300", "satuan h"),
 ("S1", "rentang FP kontrol ML", "s1_hyd_seeds.json", "kontrol_stokastik|sebaran|fp_rentang", "345", "unit"),
 ("S1", "FP kontrol minimum", "s1_hyd_seeds.json", "kontrol_stokastik|sebaran|fp_min", "1076", "unit"),
 ("S1", "FP kontrol maksimum", "s1_hyd_seeds.json", "kontrol_stokastik|sebaran|fp_maks", "1421", "unit"),
 ("S2", "vib jumlah baris", "s2_ringkas.json", "vib|n_baris", "23922", "baris"),
 ("S2", "vib positif dapat diuji", "s2_ringkas.json", "vib|n_pos_total_dapat_diuji", "5429", "menit"),
 ("S2", "ssi jumlah baris", "s2_ringkas.json", "ssi|n_baris", "35906", "baris"),
 ("S2", "ssi positif dapat diuji", "s2_ringkas.json", "ssi|n_pos_total_dapat_diuji", "592", "menit"),
 ("S2", "ssi fold tidak dapat diuji", "s2_ringkas.json", "ssi|n_fold_tidak_dapat_diuji", "2", "fold"),
 ("S2", "persistence FAR24 kalender", "s2_ringkas.json", "vib|agregat|persistence|far24_kalender_median", "22,0218", "alarm/24 jam"),
 ("S2", "persistence recall median", "s2_ringkas.json", "vib|agregat|persistence|recall_median", "0,7405", "rasio"),
 ("S2", "persistence presisi median", "s2_ringkas.json", "vib|agregat|persistence|precision_median", "0,7288", "rasio"),
 ("S2", "ML vib b24 recall median", "s2_ringkas.json", "vib|sensitivitas|ML_kalender_b24|recall_median", "0,1041", "rasio"),
 ("S2", "ML vib b24 presisi median", "s2_ringkas.json", "vib|sensitivitas|ML_kalender_b24|precision_median", "0,7781", "rasio"),
 ("S2", "ML vib b24 FAR24 kalender", "s2_ringkas.json", "vib|sensitivitas|ML_kalender_b24|far24_kalender_median", "3,1225", "alarm/24 jam"),
 ("S2", "ML ssi b24 recall median", "s2_ringkas.json", "ssi|sensitivitas|ML_kalender_b24|recall_median", "0,2157", "rasio"),
 ("S2", "ML ssi b24 presisi median", "s2_ringkas.json", "ssi|sensitivitas|ML_kalender_b24|precision_median", "0,0762", "rasio"),
 ("S2", "ML ssi b24 FAR24 kalender", "s2_ringkas.json", "ssi|sensitivitas|ML_kalender_b24|far24_kalender_median", "6,0647", "alarm/24 jam"),
 ("S3", "USROP jumlah baris", "s3a_feasibility.json", "inventaris|baris", "198928", "baris"),
 ("S3", "label positif", "s3a_feasibility.json", "label|n_pos", "49732", "baris"),
 ("S3", "jumlah well", "s3a_feasibility.json", "label|n_well", "7", "well"),
 ("S3", "well tanpa positif", "s3a_feasibility.json", "label|n_well_tanpa_positif", "2", "well"),
 ("S3", "indeks duplikat", "s3a_feasibility.json", "identitas|indeks_duplikat", "145887", "baris"),
 ("S3", "ML fisik presisi median", "s3c_ringkas.json", "agregat|ml_fisik|precision_median", "0,6496", "rasio"),
 ("S3", "ML fisik recall median", "s3c_ringkas.json", "agregat|ml_fisik|recall_median", "0,9968", "rasio"),
 ("S3", "ML fisik FAR24 median", "s3c_ringkas.json", "agregat|ml_fisik|far24_median_valid", "110,432", "alarm/24 jam"),
 ("S4", "record activity DDR", "ddr_activity_stats.json", "activity|n_record", "23447", "record"),
 ("S4", "kode kerja unik", "ddr_activity_stats.json", "activity|n_kode_unik", "64", "kode"),
 ("S4", "laporan DDR", "ddr_activity_stats.json", "laporan|n_baris", "1759", "laporan"),
 ("S4", "record tabel downtime", "ddr_downtime_table.json", "record|n_record", "533", "record"),
 ("S4", "laporan yang memuat tabel", "ddr_downtime_table.json", "tabel|n_file_memuat_tabel", "325", "laporan"),
 ("S4", "record dengan downtime nol", "ddr_downtime_table.json", "record|n_downtime_nol", "533", "record"),
 ("S4", "kejadian pada label", "labels_duration.json", "n_baris", "884", "kejadian"),
 ("S4", "total jam label", "labels_duration.json", "durasi_jam|sum", "1225,0", "jam"),
 ("S4", "jumlah kolom labels", "labels_datum_placeholder", "sumber|kolom", "20", "kolom"),
]

cache, hasil = {}, []
for kartu, label, berkas, jalur, teks, satuan in K:
    if berkas == "labels_datum_placeholder":
        berkas = "labels_duration.json"
    kunci = (kartu, berkas)
    if kunci not in cache:
        cache[kunci] = muat(kartu, berkas)
    nilai = ambil(cache[kunci], jalur)
    if isinstance(nilai, list):
        nilai = len(nilai)   # sumber.kolom berisi daftar nama kolom, jadi panjangnya yang dipakai
    if isinstance(nilai, bool):
        nilai = float(nilai)
    d = idr(teks)
    desimal = 0
    if "," in teks:
        desimal = len(teks.split(",")[1])
    tol = 0.5 * 10 ** (-desimal) + 1e-9
    lulus = abs(float(nilai) - d) <= tol
    hasil.append(dict(kartu=kartu, label=label, berkas=berkas, jalur=jalur,
                      nilai_json=nilai, teks_dokumen=teks, satuan=satuan,
                      desimal=desimal, lulus=bool(lulus)))

gagal = [h for h in hasil if not h["lulus"]]
OUT.write_text(json.dumps(hasil, indent=1, ensure_ascii=False), encoding="utf-8")
print("klaim diuji:", len(hasil), "| lulus:", len(hasil) - len(gagal), "| gagal:", len(gagal))
for g in gagal:
    print("  GAGAL", g)
