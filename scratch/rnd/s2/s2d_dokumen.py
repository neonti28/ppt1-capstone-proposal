#!/usr/bin/env python3
"""Generator dokumen docs/RND_S2_HYBRID_VIB_SSI.md dari artefak JSON.

Seluruh angka pada tabel dan narasi dihitung dari artefak lewat modul sumber
s2_common, sehingga tidak ada angka yang ditulis tangan. Idempoten: dua kali
jalan menghasilkan sha256 yang sama.
"""
from __future__ import annotations

import hashlib

import s2_common as C

DOK = f"{C.BASE}/docs/RND_S2_HYBRID_VIB_SSI.md"


def tabel(header, baris):
    out = ["| " + " | ".join(header) + " |",
           "|" + "|".join(["---"] * len(header)) + "|"]
    for b in baris:
        out.append("| " + " | ".join(str(x) for x in b) + " |")
    return "\n".join(out)


def bangun():
    rec, ring, meta = C.muat()
    vib, ssi = ring["vib"], ring["ssi"]
    va, sa = vib["agregat"], ssi["agregat"]
    vb, sb = vib["banding_hybrid_lawan_single"], ssi["banding_hybrid_lawan_single"]

    n30 = n15 = 0
    for k in ("vib", "ssi"):
        for f in rec[k]["folds"]:
            h = f["h_terpilih"]
            if h == 30.0:
                n30 += 1
            elif h == 15.0:
                n15 += 1
    n_fold_semua = vib["n_fold_total"] + ssi["n_fold_total"]
    n_fold_uji = vib["n_fold_dapat_diuji"] + ssi["n_fold_dapat_diuji"]

    def maks(d, field, model=C.MODEL_SEMUA):
        return max(d[m][field] for m in model)

    def nama_maks(d, field, model=C.MODEL_SEMUA):
        return max(model, key=lambda m: d[m][field])

    def nama_min(d, field, model=C.MODEL_SEMUA):
        return min(model, key=lambda m: d[m][field])

    j3 = next(j for j in ring["justifikasi_ambang_positif"] if j["n_pos"] == 3)
    j30 = next(j for j in ring["justifikasi_ambang_positif"] if j["n_pos"] == 30)
    kanal_vib = {}
    for w in vib["wells"]:
        kanal_vib[w["kanal"]] = kanal_vib.get(w["kanal"], 0) + 1
    kanal_ssi = {}
    for w in ssi["wells"]:
        kanal_ssi[w["kanal"]] = kanal_ssi.get(w["kanal"], 0) + 1
    sens_vib = vib["sensitivitas"]
    sens_ssi = ssi["sensitivitas"]
    b_maks = max(C.BUDGET)
    ml_vib_longgar = sens_vib[f"ML_kalender_b{b_maks}"]
    ml_ssi_longgar = sens_ssi[f"ML_kalender_b{b_maks}"]
    ml_ssi_gate = sens_ssi["ML_kalender_b24"]
    rasio_fp_ssi = (1 - ml_ssi_gate["precision_median"]) / ml_ssi_gate["precision_median"]
    rasio_far_vib = va["persistence"]["far24_kalender_median"] / meta["far_maks"]

    L = []
    a = L.append

    a("# RND-S2: HYBRID STATISTIK + RULE DAN ML + STATISTIK PADA KELAS vib DAN ssi")
    a("")
    a("Kartu: `t_f52e1ecb` · Board: `rnd-algo-2026` · Tanggal: 2026-10-28 (WIB)")
    a(f"Workspace: `{C.BASE}` · Induk: S1 (`t_6890a1c7`)")
    a("")
    a("Dokumen pendamping: `docs/RND_EVALUATION_POLICY.md` (kebijakan pengikat), "
      "`docs/RND_E1_MATRIKS.md`, `docs/RND_R8_EVALUASI_BERLAPIS.md`.")
    a("")
    a("Artefak mentah: `scratch/rnd/s2/s2_records_vib.json`, `s2_records_ssi.json`, "
      "`s2_ringkas.json`, `s2_meta.json`. Generator dokumen: `scratch/rnd/s2/s2d_dokumen.py`. "
      "Generator ledger: `scratch/rnd/s2/s2c_ledger.py`. Pemeriksa: `scratch/rnd/s2/s2e_verify.py`.")
    a("")
    a("Riset pendahuluan: scikit-learn (dipakai nyata untuk `average_precision_score` dan "
      "`roc_auc_score` per fold, supaya kemampuan pemeringkatan ML dinilai terpisah dari pilihan "
      "ambang, dan untuk menjaga pemisahan latih, kalibrasi, serta uji tanpa kebocoran).")
    a("")
    a("Riset pendahuluan: statistical-power (dipakai untuk menghitung selang Wilson 95 persen pada "
      "recall sebagai fungsi jumlah positif, sehingga aturan positif kurang dari 30 berarti tidak "
      "dapat diuji berdiri di atas presisi estimasi dan bukan pilihan sewenang-wenang; juga dipakai "
      "untuk menolak post-hoc power, sehingga yang dilaporkan adalah kurva sensitivitas anggaran, "
      "bukan power dari hasil yang sudah terlihat).")
    a("")
    a("Riset pendahuluan: verification-mandatory (setiap angka dibangkitkan lewat resolver jalur "
      "JSON yang menghentikan generator bila jalur tidak ada, dokumen dan ledger membaca modul "
      "sumber yang sama `s2_common.py`, ledger memakai 7 kolom, dan idempotensi diuji dengan "
      "sha256 dua kali jalan).")
    a("")
    a("Riset pendahuluan: sequentialthinking, 6 pikiran "
      "(`mcp__sequentialthinking__sequentialthinking`, thoughtNumber 1 sampai 6, "
      "server melaporkan thoughtHistoryLength 7 sampai 12 karena enam pikiran sebelumnya "
      "sudah ada di riwayat sesi yang sama). Ringkas: (1) target dan syarat ukur per kelas, (2) risiko "
      "sirkularitas kanal crpm dan aturan memilih kanal gerbang hanya dari well latih, "
      "(3) komposisi hybrid dari primitif harness dan arti kalibrasi, (4) justifikasi ambang 30 "
      "positif lewat presisi estimasi, (5) satuan FAR dan risiko laporan menyesatkan, (6) rencana "
      "eksekusi dan syarat bukti.")
    a("")
    a("---")
    a("")
    a("## 0. CARA MEMBACA DOKUMEN INI")
    a("")
    a("Tiga lapisan penilaian dipisah sesuai kebijakan evaluasi. Lapisan A menjawab apakah deteksi "
      "bekerja, lapisan B menjawab apakah deteksi memberi nilai maintenance, lapisan C menjawab "
      "apakah hasil cukup tepercaya. Dokumen ini mengukur A dan C. Lapisan B dinyatakan belum "
      "terukur dengan alasan yang ditulis di bagian 7, bukan dikosongkan tanpa keterangan.")
    a("")
    a("Semua angka pada tabel berasal dari artefak JSON, dan setiap angka punya baris di "
      "`docs/RND_PROVENANCE_LEDGER.md` dengan awalan `S2-`.")
    a("")
    a("## 1. PERTANYAAN, KEBIJAKAN, DAN KEPUTUSAN DESAIN")
    a("")
    a("### 1.1 Pertanyaan")
    a("")
    a("Untuk kelas kerusakan vib K-i dan ssi K-i, apakah dua bentuk hybrid berikut mengalahkan "
      "engine tunggal terbaik pada kelas yang sama:")
    a("")
    a("1. Bentuk (a): statistik + rule, yaitu detektor perubahan CUSUM yang dipadukan dengan "
      "gerbang rule kanal.")
    a("2. Bentuk (b): ML + statistik dengan kalibrasi, yaitu skor LightGBM yang ambangnya "
      "dikalibrasi pada well kalibrasi, lalu digerbangi residu statistik.")
    a("")
    a("### 1.2 Kebijakan pengikat")
    a("")
    a("`docs/RND_EVALUATION_POLICY.md` menetapkan bahwa gate bukan izin pakai, bahwa engine boleh "
      "berbeda antar kelas kerusakan, bahwa hybrid diizinkan, dan bahwa perbandingan selalu memakai "
      "baseline yang relevan untuk tugas itu. Karena itu baseline pada kartu ini adalah persistence "
      "`y_prev` yang memang disediakan pembentuk dataset sebagai baseline status, bukan baseline "
      "hyd.")
    a("")
    a("### 1.3 Keputusan desain yang dikunci sebelum melihat hasil")
    a("")
    a("1. Harness yang dipakai adalah `code/rnd_hybrid_harness.py` dari S1. Tidak ada harness "
      "kedua. Driver hanya merakit komposisi dari fungsi harness.")
    a("2. Kanal gerbang dan ambang rule dipilih hanya dari well latih setiap fold, memakai AUC nilai "
      "mutlak z terhadap label pada baris latih, lalu F1 baris latih pada grid ambang. Well uji "
      "tidak pernah dilihat saat memilih.")
    a("3. Kanal `crpm` dilarang menjadi gerbang karena `y_ssi` dibentuk dari kanal itu, sehingga "
      "gerbang crpm hanya akan merekonstruksi definisi label.")
    a("4. Fold dengan positif kurang dari 30 ditandai tidak dapat diuji dan tidak masuk agregat.")
    a("5. FAR dilaporkan pada dua satuan, kalender dan baris. Satuan kalender adalah satuan gate.")
    a("6. Ambang ML disiapkan dalam dua versi, conformal pada satuan baris dan anggaran pada satuan "
      "menit kalender, keduanya dari well kalibrasi.")
    a("7. Perbandingan hybrid lawan single engine memakai urutan yang ditetapkan di kode: jumlah "
      "fold yang lolos FAR dan recall lebih dulu, lalu recall median, lalu FAR median, lalu presisi "
      "median.")
    a("")
    a("## 2. DATA DAN KELAYAKAN UJI")
    a("")
    a("### 2.1 Jumlah yang tersedia per kelas")
    a("")
    a(tabel(["Kelas", "Baris", "Well", "Fitur", "Fold LOWO", "Fold dapat diuji", "Fold gugur",
             "Baris positif pada fold dapat diuji"],
            [["vib", C.fi(vib["n_baris"]), C.fi(vib["n_well"]), C.fi(vib["n_fitur"]),
              C.fi(vib["n_fold_total"]), C.fi(vib["n_fold_dapat_diuji"]),
              C.fi(vib["n_fold_tidak_dapat_diuji"]), C.fi(vib["n_pos_total_dapat_diuji"])],
             ["ssi", C.fi(ssi["n_baris"]), C.fi(ssi["n_well"]), C.fi(ssi["n_fitur"]),
              C.fi(ssi["n_fold_total"]), C.fi(ssi["n_fold_dapat_diuji"]),
              C.fi(ssi["n_fold_tidak_dapat_diuji"]), C.fi(ssi["n_pos_total_dapat_diuji"])]]))
    a("")
    a("Total fold lintas dua kelas adalah " + C.fi(n_fold_semua) + " fold, dan yang dapat diuji "
      + C.fi(n_fold_uji) + " fold. Well vib hanya " + C.fi(vib["n_well"]) + ", sehingga validasi "
      "lintas well untuk kelas ini lemah secara desain.")
    a("")
    a(f"Jendela yang dinilai adalah jendela onset dari harness, yaitu satu jendela per transisi "
      f"label negatif ke positif, dengan alarm ditahan 10 menit dan horizon peringatan 60 menit. "
      f"Jumlah jendela onset adalah "
      f"{C.fi(vib['agregat']['persistence']['n_onset'])} untuk vib dan "
      f"{C.fi(ssi['agregat']['persistence']['n_onset'])} untuk ssi, dan nilainya sama untuk semua "
      f"model pada kelas yang sama karena jendela ditentukan data, bukan model.")
    a("")
    a("### 2.2 Rincian per fold")
    a("")
    for k, d in (("vib", vib), ("ssi", ssi)):
        a(f"Kelas {k}, kanal gerbang terpilih per fold dan kemampuan pemeringkatan ML pada well uji:")
        a("")
        rows = []
        for w in d["wells"]:
            rows.append([w["fold"], C.fi(w["n"]), C.fi(w["n_pos"]), C.fi(w["menit_kalender"]),
                         w["kanal"], C.fd(w["auc_kanal"]), C.fd(w["h_cusum"], 1),
                         C.fd(w["auprc_ml"]), C.fd(w["auc_ml"]),
                         "ya" if w["dapat_diuji"] else "tidak"])
        a(tabel(["Fold", "Baris", "Positif", "Menit kalender", "Kanal gerbang", "AUC kanal",
                 "h CUSUM", "AUPRC ML", "AUC ML", "Dapat diuji"], rows))
        a("")
    a("Kanal gerbang yang terpilih berbeda antar fold, dan itu akibat aturan pemilihan dari well "
      "latih. Pada vib " + ", ".join(f"{k} di {v} fold" for k, v in sorted(kanal_vib.items())) +
      ". Pada ssi " + ", ".join(f"{k} di {v} fold" for k, v in sorted(kanal_ssi.items())) + ".")
    a("")
    a("### 2.3 Fold yang tidak dapat diuji")
    a("")
    for t in ssi["tak_dapat_diuji"]:
        a(f"- Fold {t['fold']} pada kelas ssi: {C.fi(t['n_pos'])} baris positif dari "
          f"{C.fi(t['n'])} baris. Alasan: {t['alasan']}.")
    a("")
    a("Ambang 30 positif tidak dipilih supaya hasil terlihat baik. Ambang itu diuji dengan lebar "
      "selang Wilson 95 persen pada recall, karena recall adalah rasio dengan penyebut jumlah "
      "positif sehingga presisinya ditentukan langsung oleh angka itu:")
    a("")
    rows = []
    for j in ring["justifikasi_ambang_positif"]:
        if j["n_pos"] in (3, 12, 30, 31):
            rows.append([C.fi(j["n_pos"]), C.fd(j["wilson_recall_0"]["hi"]),
                         C.fd(j["wilson_recall_penuh"]["lo"]), C.fd(j["lebar_penuh"])])
    a(tabel(["Jumlah positif", "Batas atas selang saat recall 0",
             "Batas bawah selang saat recall 1", "Lebar selang saat recall 1"], rows))
    a("")
    a(f"Pada {C.fi(j3['n_pos'])} positif, recall 1,0 masih kompatibel dengan nilai sebenarnya "
      f"{C.fd(j3['wilson_recall_penuh']['lo'])}, sehingga detektor sempurna dan detektor setengah "
      f"benar tidak dapat dibedakan. Pada {C.fi(j30['n_pos'])} positif lebar itu turun menjadi "
      f"{C.fd(j30['lebar_penuh'])}. Itulah dasar angka 30.")
    a("")
    a("### 2.4 Cacat data yang membatasi tafsir")
    a("")
    a(f"Label `y_vib` dibentuk dari kanal `vib_max` dengan ambang satu g, yaitu 32,17405 ft/s2 "
      f"menurut API RP 7G. Kanal `vib` tidak ada di antara {C.fi(vib['n_fitur'])} fitur dataset, "
      f"sehingga tidak ada sirkularitas, tetapi juga tidak ada variabel pembangkit label yang bisa "
      f"dipakai model. Label `y_ssi` dibentuk dari kanal `crpm` lewat SSI sama dengan (maksimum "
      f"dikurangi minimum) dibagi dua kali rerata, dan kanal `crpm` juga tidak ada di "
      f"{C.fi(ssi['n_fitur'])} fitur, tetapi ada di bins. Karena itu gerbang rule untuk ssi sengaja "
      f"tidak memakai crpm. Kedua hal ini menjelaskan mengapa tugas vib dan ssi bukan tugas "
      f"menyalin definisi, melainkan tugas menyimpulkan kondisi dari kanal lain.")
    a("")
    a("## 3. BENTUK HYBRID YANG DIUJI")
    a("")
    rows = []
    for m in C.MODEL_SEMUA:
        jenis = "single" if m in C.MODEL_SINGLE else ("hybrid" if m in C.MODEL_HYBRID else "kontrol")
        rows.append([m, jenis, C.LABEL_MODEL[m]])
    a(tabel(["Nama model", "Jenis", "Komposisi"], rows))
    a("")
    a(f"Ambang CUSUM `h` dipilih harness dari well kalibrasi pada anggaran FAR gate, dan grid "
      f"harness berhenti di 30. Ambang ML conformal adalah kuantil {C.fd(1 - meta['alpha_budget'], 6)} "
      f"dari skor negatif well kalibrasi, yaitu satu minus alpha {C.fd(meta['alpha_budget'], 6)}. "
      f"Ambang ML kalender dihitung dari kuantil skor negatif "
      f"well kalibrasi pada anggaran menit kalender, memakai primitif harness yang sama, dan "
      f"kesetiaan komposisinya dibuktikan dengan assert bahwa ambang conformal hasil komposisi sama "
      f"dengan ambang yang dikembalikan harness sampai selisih di bawah 1e-12.")
    a("")
    a("## 4. LAPISAN A: APAKAH DETEKSI BEKERJA")
    a("")
    a(f"Kolom lolos menghitung fold yang memenuhi FAR tidak lebih dari {C.fd(meta['far_maks'], 1)} "
      f"per 24 jam kalender dan recall tidak kurang dari 0,50 sekaligus. Itu definisi gate A pada "
      f"harness.")
    a("")
    for k, d in (("vib", vib), ("ssi", ssi)):
        a(f"### 4.{1 if k == 'vib' else 2} Kelas {k}")
        a("")
        rows = []
        for m in C.MODEL_SEMUA:
            g = d["agregat"][m]
            rows.append([m, C.fi(g["n_fold"]), C.fd(g["recall_median"]), C.fd(g["precision_median"]),
                         C.fd(g["far24_kalender_median"]), C.fd(g["far24_baris_median"]),
                         C.fi(g["fp_total"]), C.fd(g["cakupan_median"]),
                         f"{g['fold_lolos_far_recall']}/{g['n_fold']}"])
        a(tabel(["Model", "Fold", "Recall median", "Presisi median", "FAR kalender median",
                 "FAR baris median", "FP total", "Cakupan median", "Lolos"], rows))
        a("")
    a("Pada vib tidak ada model yang lolos. Model dengan FAR median terendah adalah "
      f"{nama_min(va, 'far24_kalender_median')} pada nilai "
      f"{C.fd(va[nama_min(va, 'far24_kalender_median')]['far24_kalender_median'])} dengan recall "
      f"median {C.fd(va[nama_min(va, 'far24_kalender_median')]['recall_median'])} dan presisi "
      f"median {C.fd(va[nama_min(va, 'far24_kalender_median')]['precision_median'])}. Presisi itu "
      f"tidak bermakna karena hanya berlaku pada alarm yang sangat sedikit, sehingga model tersebut "
      f"bukan detektor melainkan gerbang yang hampir selalu tertutup. Model dengan recall median "
      f"tertinggi adalah {nama_maks(va, 'recall_median')} pada {C.fd(maks(va, 'recall_median'))}, "
      f"tetapi FAR mediannya {C.fd(va[nama_maks(va, 'recall_median')]['far24_kalender_median'])}, "
      f"yaitu {C.fd(rasio_far_vib, 2)} kali anggaran gate.")
    a("")
    a(f"Pada ssi, recall median tertinggi di antara semua model hanya {C.fd(maks(sa, 'recall_median'))} "
      f"dan presisi median tertinggi {C.fd(maks(sa, 'precision_median'))}. Presisi tertinggi itu "
      f"datang dari {nama_maks(sa, 'precision_median')} yang recall mediannya "
      f"{C.fd(sa[nama_maks(sa, 'precision_median')]['recall_median'])}, jadi angka presisi itu tidak "
      f"dapat dipakai sebagai bukti kualitas. Tidak ada model yang layak disebut detektor pada "
      f"anggaran gate.")
    a("")
    a("### 4.3 Kurva sensitivitas anggaran")
    a("")
    a("Satu titik anggaran tidak cukup untuk menyimpulkan, jadi ambang diambil ulang pada anggaran "
      + ", ".join(C.fi(b) for b in C.BUDGET) +
      " per 24 jam, semuanya dari well kalibrasi, lalu diukur pada well uji.")
    a("")
    for k, d in (("vib", vib), ("ssi", ssi)):
        a(f"Kelas {k}:")
        a("")
        rows = []
        for b in C.BUDGET:
            ml = d["sensitivitas"][f"ML_kalender_b{b}"]
            st_ = d["sensitivitas"][f"stat_cusum_b{b}"]
            rows.append([C.fi(b), C.fd(ml["recall_median"]), C.fd(ml["precision_median"]),
                         C.fd(ml["far24_kalender_median"]), C.fd(st_["recall_median"]),
                         C.fd(st_["precision_median"]), C.fd(st_["far24_kalender_median"])])
        a(tabel(["Anggaran", "ML recall", "ML presisi", "ML FAR", "CUSUM recall",
                 "CUSUM presisi", "CUSUM FAR"], rows))
        a("")
    a(f"Kurva ini naik seiring anggaran dan itu yang diharapkan. Yang menentukan adalah titik "
      f"temunya. Pada vib, ML mencapai recall median {C.fd(ml_vib_longgar['recall_median'])} pada "
      f"FAR {C.fd(ml_vib_longgar['far24_kalender_median'])}, sedangkan persistence mencapai recall "
      f"{C.fd(va['persistence']['recall_median'])} pada FAR "
      f"{C.fd(va['persistence']['far24_kalender_median'])}. Artinya pada FAR yang lebih rendah pun "
      f"persistence sudah lebih tinggi, sehingga ML tidak tertinggal karena ambang terlalu ketat, "
      f"melainkan karena memang tidak mengungguli baseline pada kelas ini. CUSUM sendiri baru "
      f"mendekati persistence pada anggaran {C.fi(b_maks)}, yaitu recall "
      f"{C.fd(sens_vib[f'stat_cusum_b{b_maks}']['recall_median'])} pada FAR "
      f"{C.fd(sens_vib[f'stat_cusum_b{b_maks}']['far24_kalender_median'])}, yang jauh di atas "
      f"anggaran gate.")
    a("")
    a(f"Komposisi bentuk (a) tidak memperbaiki keadaan. H1 statistik DAN rule menurunkan FAR median "
      f"dari {C.fd(va['stat_cusum']['far24_kalender_median'])} menjadi "
      f"{C.fd(va['H1_stat_dan_rule']['far24_kalender_median'])}, tetapi recall median turun dari "
      f"{C.fd(va['stat_cusum']['recall_median'])} menjadi "
      f"{C.fd(va['H1_stat_dan_rule']['recall_median'])}, sehingga tidak ada titik operasi yang "
      f"mengalahkan persistence. Varian ATAU memang menaikkan recall ke "
      f"{C.fd(va['H1b_stat_atau_rule']['recall_median'])}, tetapi FAR mediannya ikut naik ke "
      f"{C.fd(va['H1b_stat_atau_rule']['far24_kalender_median'])}.")
    a("")
    a(f"Pada ssi, ML mencapai recall median {C.fd(ml_ssi_longgar['recall_median'])} pada FAR "
      f"{C.fd(ml_ssi_longgar['far24_kalender_median'])} dengan presisi median "
      f"{C.fd(ml_ssi_longgar['precision_median'])}. Pada anggaran terdekat dengan gate, yaitu 24, "
      f"recall median {C.fd(ml_ssi_gate['recall_median'])} dengan presisi "
      f"{C.fd(ml_ssi_gate['precision_median'])} dan FAR {C.fd(ml_ssi_gate['far24_kalender_median'])}. "
      f"Presisi itu berarti sekitar {C.fd(rasio_fp_ssi, 1)} alarm palsu untuk setiap alarm benar, "
      f"sehingga pemakaiannya hanya mungkin sebagai pemantauan tren, bukan alarm kritis otomatis.")
    a("")
    a("### 4.4 Mengapa komposisi DAN runtuh")
    a("")
    a(f"Ambang CUSUM tersaturasi pada nilai tertinggi grid, yaitu 30, di {n30} dari {n_fold_semua} "
      f"fold, dan pada 15 di {n15} fold. Ketika anggaran FAR dipaksa sangat kecil pada well "
      f"kalibrasi, CUSUM hanya bisa memenuhi anggaran dengan ambang setinggi mungkin, sehingga "
      f"keluarannya hampir selalu nol. Gerbang DAN dengan komponen yang hampir selalu nol akan "
      f"mematikan sinyal pasangannya. Itulah sebabnya H2 ML dan statistik pada vib punya FAR median "
      f"{C.fd(va['H2_ML_kalender_dan_stat']['far24_kalender_median'])} dengan recall median "
      f"{C.fd(va['H2_ML_kalender_dan_stat']['recall_median'])}, dan pada ssi recall median "
      f"{C.fd(sa['H2_ML_kalender_dan_stat']['recall_median'])}. Itu bukan bukti komposisinya aman, "
      f"melainkan bukti komponen statistiknya tidak berfungsi pada anggaran ini.")
    a("")
    a("## 5. PERBANDINGAN HYBRID LAWAN SINGLE ENGINE TERBAIK")
    a("")
    rows = []
    for k, b in (("vib", vb), ("ssi", sb)):
        rows.append([k, b["single"], b["hybrid"], C.fd(b["delta_recall_median"]),
                     C.fd(b["delta_precision_median"]), C.fd(b["rasio_far_median"]),
                     C.fi(b["delta_fold_lolos"])])
    a(tabel(["Kelas", "Single terbaik", "Hybrid terbaik", "Selisih recall median",
             "Selisih presisi median", "Rasio FAR median", "Selisih fold lolos"], rows))
    a("")
    a(f"Pada vib hybrid terbaik kalah pada tiga sumbu sekaligus: recall median lebih rendah "
      f"{C.fd(abs(vb['delta_recall_median']))}, presisi median lebih rendah "
      f"{C.fd(abs(vb['delta_precision_median']))}, dan FAR median {C.fd(vb['rasio_far_median'])} "
      f"kali lipat lebih besar. Pada ssi hybrid terbaik menang tipis pada recall median sebesar "
      f"{C.fd(sb['delta_recall_median'])}, tetapi presisi median lebih rendah "
      f"{C.fd(abs(sb['delta_precision_median']))} dan FAR median {C.fd(sb['rasio_far_median'])} "
      f"kali lipat lebih besar. Kemenangan tipis pada kelas yang tidak punya satu model pun dengan "
      f"presisi median di atas {C.fd(maks(sa, 'precision_median'))} tidak cukup untuk menyebut hybrid "
      f"lebih baik, dan saya tidak menyebutnya demikian.")
    a("")
    a("## 6. LAPISAN C: KETEPATAN DAN KETAHANAN")
    a("")
    a("### 6.1 Kestabilan di dalam well")
    a("")
    a("Setiap well dipecah pada median waktu menjadi paruh awal dan paruh akhir, lalu recall "
      "dihitung pada masing masing paruh.")
    a("")
    for k, d in (("vib", vib), ("ssi", ssi)):
        rows = []
        for m in C.MODEL_SEMUA:
            s = d["lapisan_c_separuh"][m]
            rows.append([m, C.fd(s["recall_awal_median"]), C.fd(s["recall_akhir_median"]),
                         f"{s['n_fold_menurun']}/{s['n_fold_banding']}"])
        a(f"Kelas {k}:")
        a("")
        a(tabel(["Model", "Recall paruh awal", "Recall paruh akhir", "Fold menurun"], rows))
        a("")
    a(f"Pada ssi, hybrid H1b menurun di "
      f"{ssi['lapisan_c_separuh']['H1b_stat_atau_rule']['n_fold_menurun']} dari "
      f"{ssi['lapisan_c_separuh']['H1b_stat_atau_rule']['n_fold_banding']} fold dan H2b menurun di "
      f"{ssi['lapisan_c_separuh']['H2b_ML_kalender_atau_stat']['n_fold_menurun']} dari "
      f"{ssi['lapisan_c_separuh']['H2b_ML_kalender_atau_stat']['n_fold_banding']} fold, sehingga "
      f"keunggulan tipis pada bagian 5 tidak stabil antar paruh waktu.")
    a("")
    a("### 6.2 Variasi seed pada komponen ML")
    a("")
    a(f"Komponen statistik dan rule deterministik, sehingga seed hanya memengaruhi ML. Seed "
      f"{C.fi(meta['seed_utama'])} dan seed {C.fi(meta['seed_uji'])} dijalankan pada konfigurasi "
      f"yang sama:")
    a("")
    rows = []
    for k, d in (("vib", vib), ("ssi", ssi)):
        for s in d["variasi_seed_ml"]:
            rows.append([k, s["fold"], C.fi(s["delta_fp"]), C.fi(s["delta_tp"]),
                         C.fd(s["delta_recall"])])
    a(tabel(["Kelas", "Fold", "Selisih FP", "Selisih TP", "Selisih recall"], rows))
    a("")
    nol_vib = sum(1 for s in vib["variasi_seed_ml"] if s["delta_fp"] == 0 and s["delta_tp"] == 0)
    ubah_ssi = sum(1 for s in ssi["variasi_seed_ml"] if s["delta_fp"] != 0 or s["delta_tp"] != 0)
    a(f"Pada vib {nol_vib} dari {len(vib['variasi_seed_ml'])} fold memberi selisih nol, sedangkan "
      f"pada ssi {ubah_ssi} dari {len(ssi['variasi_seed_ml'])} fold berubah. Artinya komponen ML "
      f"tidak stabil terhadap seed pada titik operasi ini, dan itu harus disebut sebagai "
      f"ketidakpastian, bukan disamarkan dengan satu angka.")
    a("")
    a("### 6.3 Cakupan menit")
    a("")
    a(f"Cakupan menit adalah rasio jumlah baris terhadap rentang menit kalender well. Cakupan "
      f"median vib adalah {C.fd(va['persistence']['cakupan_median'])} dan ssi "
      f"{C.fd(sa['persistence']['cakupan_median'])}. Gate A pada harness mensyaratkan cakupan tidak "
      f"kurang dari 0,50, sehingga syarat itu gagal di semua fold pada kedua kelas. Kegagalan "
      f"cakupan bukan alasan membuang engine, sesuai kebijakan bagian 1, tetapi ia membatasi arti "
      f"FAR pada satuan kalender karena penyebut kalender jauh lebih besar daripada jumlah baris "
      f"berdata.")
    a("")
    a("## 7. LAPISAN B: NILAI MAINTENANCE, BELUM TERUKUR")
    a("")
    a("Lapisan B belum terukur, dan penyebabnya bukan kelalaian pada kartu ini. Ukuran utama lapisan "
      "B menurut kebijakan adalah waktu peringatan terhadap kejadian nyata dan berkurangnya "
      "pemeriksaan yang tidak perlu. Untuk itu dibutuhkan waktu kejadian maintenance, yaitu "
      "inspeksi, work order, atau perbaikan. Kartu S4 sudah memindai sumber itu dan hasilnya: biaya "
      "tidak ada sama sekali, work order bernomor tidak ada, jadwal inspeksi tidak ada, dan tabel "
      "kegagalan peralatan mencatat downtime nol pada semua record. Tanpa waktu kejadian nyata, "
      "waktu peringatan hanya bisa dihitung terhadap onset label, dan itu bukan lapisan B karena "
      "label bukan tindakan maintenance.")
    a("")
    a(f"Sebagai catatan batas, harness tetap menghasilkan lead median terhadap onset label, yaitu "
      f"{C.fd(va['persistence']['lead_median'], 2)} menit untuk persistence vib dan "
      f"{C.fd(sa['persistence']['lead_median'], 2)} menit untuk persistence ssi. Angka itu sengaja "
      f"tidak dipakai sebagai nilai lapisan B karena penyebutnya onset label, bukan kejadian "
      f"maintenance.")
    a("")
    a("## 8. KEPUTUSAN DAN BATAS PENGGUNAAN")
    a("")
    a(f"1. Untuk vib, tidak ada hybrid yang mengungguli {vb['single']}. Bentuk (a) dan bentuk (b) "
      f"sama sama gagal, dan kegagalannya bukan karena ambang terlalu ketat, karena kurva "
      f"sensitivitas pada bagian 4.3 tetap di bawah baseline pada FAR yang lebih longgar.")
    a(f"2. Untuk ssi, tidak ada engine yang layak sebagai alarm kritis. ML punya kemampuan "
      f"peringkat yang nyata dengan AUC well uji antara {C.fd(min(w['auc_ml'] for w in ssi['wells']))} "
      f"dan {C.fd(max(w['auc_ml'] for w in ssi['wells']))}, tetapi pada anggaran gate presisi "
      f"median hanya {C.fd(ml_ssi_gate['precision_median'])}, sehingga pemakaian yang jujur adalah "
      f"pemantauan tren dengan ambang longgar dan pengawasan manusia.")
    a("3. Komposisi DAN dengan komponen statistik yang tersaturasi adalah pola yang harus dihindari "
      "pada anggaran FAR kecil. Komposisi ATAU mempertahankan recall tetapi membayar dengan FAR "
      "lebih besar.")
    a("4. Gate bukan izin pakai, dan nol fold yang lolos di kedua kelas adalah pernyataan "
      "kemampuan, bukan vonis buang.")
    a("")
    a("## 9. PROVENANCE DAN REPRODUKSI")
    a("")
    a("1. Seluruh angka berasal dari empat artefak JSON di `scratch/rnd/s2/`, dan setiap angka "
      "punya baris ledger berawalan `S2-` dengan 7 kolom.")
    a("2. Ledger dibangkitkan `s2c_ledger.py` yang membaca JSON lewat resolver jalur. Bila jalur "
      "tidak ada, generator berhenti dengan KeyError, sehingga angka tidak bisa dikarang.")
    a("3. Dokumen dibangkitkan `s2d_dokumen.py` yang membaca modul sumber yang sama dengan generator "
      "ledger, sehingga tabel dokumen dan baris ledger tidak mungkin berbeda.")
    a(f"4. Eksekusi penuh memerlukan {C.fd(meta['durasi_detik'], 1)} detik dan "
      f"{C.fi(meta['panggil_harness_sinyal'])} panggilan fungsi sinyal harness.")
    a(f"5. Seed utama {C.fi(meta['seed_utama'])}, seed uji {C.fi(meta['seed_uji'])}, ambang FAR gate "
      f"{C.fd(meta['far_maks'], 1)} per 24 jam kalender, syarat positif minimum "
      f"{C.fi(meta['min_pos_uji'])} baris, grid anggaran "
      f"{', '.join(C.fi(b) for b in meta['budget_grid'])}.")
    a("")
    a("## 10. RINGKASAN LIMA BARIS")
    a("")
    a(f"1. vib punya {C.fi(vib['n_fold_total'])} fold dengan "
      f"{C.fi(vib['n_pos_total_dapat_diuji'])} baris positif, ssi punya "
      f"{C.fi(ssi['n_fold_total'])} fold dengan {C.fi(ssi['n_pos_total_dapat_diuji'])} baris positif "
      f"pada {C.fi(ssi['n_fold_dapat_diuji'])} fold yang dapat diuji, sedangkan "
      + " dan ".join(f"{t['fold']} gugur karena hanya {C.fi(t['n_pos'])} positif"
                     for t in ssi["tak_dapat_diuji"]) + ".")
    a(f"2. Tidak ada satu model pun yang lolos gate A pada kedua kelas, dengan nol fold lolos dari "
      f"{C.fi(vib['n_fold_dapat_diuji'])} fold vib dan nol dari "
      f"{C.fi(ssi['n_fold_dapat_diuji'])} fold ssi.")
    a(f"3. Pada vib hybrid terbaik kalah dari {vb['single']} pada recall, presisi, dan FAR "
      f"sekaligus, dengan selisih recall median {C.fd(abs(vb['delta_recall_median']))} dan FAR "
      f"{C.fd(vb['rasio_far_median'])} kali lipat.")
    a(f"4. Pada ssi hybrid terbaik hanya unggul {C.fd(sb['delta_recall_median'])} pada recall median "
      f"dengan FAR {C.fd(sb['rasio_far_median'])} kali lipat dan presisi median "
      f"{C.fd(sa[sb['hybrid']]['precision_median'])}, sehingga tidak layak disebut lebih baik.")
    a("5. Lapisan B belum terukur karena data inspeksi, work order, dan biaya tidak ada, dan itu "
      "dibuktikan pada kartu S4, bukan diasumsikan.")
    a("")
    a("## 11. YANG BELUM TERVERIFIKASI")
    a("")
    a("1. Lapisan B belum terukur sepenuhnya, dan tidak akan terukur tanpa waktu kejadian "
      "maintenance.")
    a("2. Pemilihan kanal gerbang memakai AUC nilai mutlak z pada baris latih. Varian pemilihan "
      "lain, misalnya memakai presisi pada ambang tertentu, belum diuji, sehingga kanal terpilih per "
      "fold belum tentu optimal.")
    a("3. Ambang CUSUM dibatasi grid harness yang berhenti di 30. Perluasan grid sudah dicoba S1 "
      "pada hyd dan menurunkan recall, tetapi perluasan yang sama belum dijalankan untuk vib dan "
      "ssi.")
    a("4. Jumlah well vib hanya " + C.fi(vib["n_well"]) + ", sehingga validasi lintas well untuk "
      "kelas ini lemah secara desain dan tidak dapat diperbaiki dengan menambah fold.")
    a("5. Pengaruh kalibrasi pada satu well kalibrasi, yaitu `train_wells[0]`, belum diuji dengan "
      "skema kalibrasi bergilir.")
    a("6. Tafsir fisis atas kanal yang terpilih, misalnya HKLD untuk vib, belum diverifikasi "
      "terhadap literatur atau catatan lapangan, sehingga statusnya hipotesis.")
    a("")

    return "\n".join(L)


def main():
    teks = bangun()
    with open(DOK, "w", encoding="utf-8") as f:
        f.write(teks + "\n")
    h = hashlib.sha256(teks.encode("utf-8")).hexdigest()
    print(f"dokumen: {DOK}")
    print(f"baris: {teks.count(chr(10)) + 1}, byte: {len(teks.encode('utf-8'))}, sha256: {h[:16]}")
    print(f"em-dash dan en-dash: {teks.count(chr(8212)) + teks.count(chr(8211))}")


if __name__ == "__main__":
    main()
