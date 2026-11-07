# RND-S2: HYBRID STATISTIK + RULE DAN ML + STATISTIK PADA KELAS vib DAN ssi

Kartu: `t_f52e1ecb` · Board: `rnd-algo-2026` · Tanggal: 2026-10-28 (WIB)
Workspace: `/mnt/d/Capstone 1(v2)` · Induk: S1 (`t_6890a1c7`)

Dokumen pendamping: `docs/RND_EVALUATION_POLICY.md` (kebijakan pengikat), `docs/RND_E1_MATRIKS.md`, `docs/RND_R8_EVALUASI_BERLAPIS.md`.

Artefak mentah: `scratch/rnd/s2/s2_records_vib.json`, `s2_records_ssi.json`, `s2_ringkas.json`, `s2_meta.json`. Generator dokumen: `scratch/rnd/s2/s2d_dokumen.py`. Generator ledger: `scratch/rnd/s2/s2c_ledger.py`. Pemeriksa: `scratch/rnd/s2/s2e_verify.py`.

Riset pendahuluan: scikit-learn (dipakai nyata untuk `average_precision_score` dan `roc_auc_score` per fold, supaya kemampuan pemeringkatan ML dinilai terpisah dari pilihan ambang, dan untuk menjaga pemisahan latih, kalibrasi, serta uji tanpa kebocoran).

Riset pendahuluan: statistical-power (dipakai untuk menghitung selang Wilson 95 persen pada recall sebagai fungsi jumlah positif, sehingga aturan positif kurang dari 30 berarti tidak dapat diuji berdiri di atas presisi estimasi dan bukan pilihan sewenang-wenang; juga dipakai untuk menolak post-hoc power, sehingga yang dilaporkan adalah kurva sensitivitas anggaran, bukan power dari hasil yang sudah terlihat).

Riset pendahuluan: verification-mandatory (setiap angka dibangkitkan lewat resolver jalur JSON yang menghentikan generator bila jalur tidak ada, dokumen dan ledger membaca modul sumber yang sama `s2_common.py`, ledger memakai 7 kolom, dan idempotensi diuji dengan sha256 dua kali jalan).

Riset pendahuluan: sequentialthinking, 6 pikiran (`mcp__sequentialthinking__sequentialthinking`, thoughtNumber 1 sampai 6, thoughtHistoryLength 6). Ringkas: (1) target dan syarat ukur per kelas, (2) risiko sirkularitas kanal crpm dan aturan memilih kanal gerbang hanya dari well latih, (3) komposisi hybrid dari primitif harness dan arti kalibrasi, (4) justifikasi ambang 30 positif lewat presisi estimasi, (5) satuan FAR dan risiko laporan menyesatkan, (6) rencana eksekusi dan syarat bukti.

---

## 0. CARA MEMBACA DOKUMEN INI

Tiga lapisan penilaian dipisah sesuai kebijakan evaluasi. Lapisan A menjawab apakah deteksi bekerja, lapisan B menjawab apakah deteksi memberi nilai maintenance, lapisan C menjawab apakah hasil cukup tepercaya. Dokumen ini mengukur A dan C. Lapisan B dinyatakan belum terukur dengan alasan yang ditulis di bagian 7, bukan dikosongkan tanpa keterangan.

Semua angka pada tabel berasal dari artefak JSON, dan setiap angka punya baris di `docs/RND_PROVENANCE_LEDGER.md` dengan awalan `S2-`.

## 1. PERTANYAAN, KEBIJAKAN, DAN KEPUTUSAN DESAIN

### 1.1 Pertanyaan

Untuk kelas kerusakan vib K-i dan ssi K-i, apakah dua bentuk hybrid berikut mengalahkan engine tunggal terbaik pada kelas yang sama:

1. Bentuk (a): statistik + rule, yaitu detektor perubahan CUSUM yang dipadukan dengan gerbang rule kanal.
2. Bentuk (b): ML + statistik dengan kalibrasi, yaitu skor LightGBM yang ambangnya dikalibrasi pada well kalibrasi, lalu digerbangi residu statistik.

### 1.2 Kebijakan pengikat

`docs/RND_EVALUATION_POLICY.md` menetapkan bahwa gate bukan izin pakai, bahwa engine boleh berbeda antar kelas kerusakan, bahwa hybrid diizinkan, dan bahwa perbandingan selalu memakai baseline yang relevan untuk tugas itu. Karena itu baseline pada kartu ini adalah persistence `y_prev` yang memang disediakan pembentuk dataset sebagai baseline status, bukan baseline hyd.

### 1.3 Keputusan desain yang dikunci sebelum melihat hasil

1. Harness yang dipakai adalah `code/rnd_hybrid_harness.py` dari S1. Tidak ada harness kedua. Driver hanya merakit komposisi dari fungsi harness.
2. Kanal gerbang dan ambang rule dipilih hanya dari well latih setiap fold, memakai AUC nilai mutlak z terhadap label pada baris latih, lalu F1 baris latih pada grid ambang. Well uji tidak pernah dilihat saat memilih.
3. Kanal `crpm` dilarang menjadi gerbang karena `y_ssi` dibentuk dari kanal itu, sehingga gerbang crpm hanya akan merekonstruksi definisi label.
4. Fold dengan positif kurang dari 30 ditandai tidak dapat diuji dan tidak masuk agregat.
5. FAR dilaporkan pada dua satuan, kalender dan baris. Satuan kalender adalah satuan gate.
6. Ambang ML disiapkan dalam dua versi, conformal pada satuan baris dan anggaran pada satuan menit kalender, keduanya dari well kalibrasi.
7. Perbandingan hybrid lawan single engine memakai urutan yang ditetapkan di kode: jumlah fold yang lolos FAR dan recall lebih dulu, lalu recall median, lalu FAR median, lalu presisi median.

## 2. DATA DAN KELAYAKAN UJI

### 2.1 Jumlah yang tersedia per kelas

| Kelas | Baris | Well | Fitur | Fold LOWO | Fold dapat diuji | Fold gugur | Baris positif pada fold dapat diuji |
|---|---|---|---|---|---|---|---|
| vib | 23.922 | 4 | 55 | 4 | 4 | 0 | 5.429 |
| ssi | 35.906 | 9 | 55 | 9 | 7 | 2 | 592 |

Total fold lintas dua kelas adalah 13 fold, dan yang dapat diuji 11 fold. Well vib hanya 4, sehingga validasi lintas well untuk kelas ini lemah secara desain.

### 2.2 Rincian per fold

Kelas vib, kanal gerbang terpilih per fold dan kemampuan pemeringkatan ML pada well uji:

| Fold | Baris | Positif | Menit kalender | Kanal gerbang | AUC kanal | h CUSUM | AUPRC ML | AUC ML | Dapat diuji |
|---|---|---|---|---|---|---|---|---|---|
| F-14 | 1.989 | 1.124 | 3.018 | HKLD | 0,6757 | 30,0 | 0,8481 | 0,8274 | ya |
| F-15A | 6.482 | 1.543 | 32.141 | HKLD | 0,6419 | 30,0 | 0,5452 | 0,8078 | ya |
| F-15_S | 10.903 | 1.532 | 92.501 | HKLD | 0,6760 | 30,0 | 0,4806 | 0,7919 | ya |
| F-5 | 4.548 | 1.230 | 20.961 | depth | 0,6290 | 30,0 | 0,6073 | 0,8680 | ya |

Kelas ssi, kanal gerbang terpilih per fold dan kemampuan pemeringkatan ML pada well uji:

| Fold | Baris | Positif | Menit kalender | Kanal gerbang | AUC kanal | h CUSUM | AUPRC ML | AUC ML | Dapat diuji |
|---|---|---|---|---|---|---|---|---|---|
| F-10 | 7.133 | 161 | 11.247 | TQA | 0,5319 | 30,0 | 0,0306 | 0,5387 | ya |
| F-12 | 4.293 | 83 | 85.643 | spm | 0,5778 | 15,0 | 0,0354 | 0,6498 | ya |
| F-14 | 5.455 | 75 | 275.834 | TFLO | 0,5818 | 30,0 | 0,0245 | 0,6663 | ya |
| F-15A | 6.020 | 31 | 32.133 | spm | 0,5647 | 15,0 | 0,0381 | 0,8722 | ya |
| F-15_S | 5.342 | 85 | 81.764 | TFLO | 0,5902 | 30,0 | 0,1848 | 0,8673 | ya |
| F-5 | 4.714 | 102 | 322.772 | spm | 0,5824 | 15,0 | 0,0893 | 0,6146 | ya |
| F-7 | 982 | 3 | 12.837 | spm | 0,5743 | 15,0 | 0,0340 | 0,9067 | tidak |
| F-9 | 1.126 | 12 | 2.287 | spm | 0,5716 | 15,0 | 0,0229 | 0,6896 | tidak |
| F-9_A | 841 | 55 | 1.173 | TFLO | 0,5927 | 30,0 | 0,1215 | 0,6962 | ya |

Kanal gerbang yang terpilih berbeda antar fold, dan itu akibat aturan pemilihan dari well latih. Pada vib HKLD di 3 fold, depth di 1 fold. Pada ssi TFLO di 3 fold, TQA di 1 fold, spm di 5 fold.

### 2.3 Fold yang tidak dapat diuji

- Fold F-7 pada kelas ssi: 3 baris positif dari 982 baris. Alasan: positif 3 kurang dari 30.
- Fold F-9 pada kelas ssi: 12 baris positif dari 1.126 baris. Alasan: positif 12 kurang dari 30.

Ambang 30 positif tidak dipilih supaya hasil terlihat baik. Ambang itu diuji dengan lebar selang Wilson 95 persen pada recall, karena recall adalah rasio dengan penyebut jumlah positif sehingga presisinya ditentukan langsung oleh angka itu:

| Jumlah positif | Batas atas selang saat recall 0 | Batas bawah selang saat recall 1 | Lebar selang saat recall 1 |
|---|---|---|---|
| 3 | 0,5615 | 0,4385 | 0,5615 |
| 12 | 0,2425 | 0,7575 | 0,2425 |
| 30 | 0,1135 | 0,8865 | 0,1135 |
| 31 | 0,1103 | 0,8897 | 0,1103 |

Pada 3 positif, recall 1,0 masih kompatibel dengan nilai sebenarnya 0,4385, sehingga detektor sempurna dan detektor setengah benar tidak dapat dibedakan. Pada 30 positif lebar itu turun menjadi 0,1135. Itulah dasar angka 30.

### 2.4 Cacat data yang membatasi tafsir

Label `y_vib` dibentuk dari kanal `vib_max` dengan ambang satu g, yaitu 32,17405 ft/s2 menurut API RP 7G. Kanal `vib` tidak ada di antara 55 fitur dataset, sehingga tidak ada sirkularitas, tetapi juga tidak ada variabel pembangkit label yang bisa dipakai model. Label `y_ssi` dibentuk dari kanal `crpm` lewat SSI sama dengan (maksimum dikurangi minimum) dibagi dua kali rerata, dan kanal `crpm` juga tidak ada di 55 fitur, tetapi ada di bins. Karena itu gerbang rule untuk ssi sengaja tidak memakai crpm. Kedua hal ini menjelaskan mengapa tugas vib dan ssi bukan tugas menyalin definisi, melainkan tugas menyimpulkan kondisi dari kanal lain.

## 3. BENTUK HYBRID YANG DIUJI

| Nama model | Jenis | Komposisi |
|---|---|---|
| persistence | single | Persistence (y_prev, baseline per tugas dari data) |
| rule_kanal | single | Rule kanal (gerbang nilai mutlak z kanal) |
| stat_cusum | single | Statistik CUSUM pada z kanal |
| ML_conformal | single | ML LightGBM, ambang conformal |
| ML_kalender | single | ML LightGBM, ambang anggaran kalender |
| H1_stat_dan_rule | hybrid | H1 statistik DAN rule |
| H1b_stat_atau_rule | hybrid | H1b statistik ATAU rule |
| H2_ML_kalender_dan_stat | hybrid | H2 ML DAN statistik |
| H2b_ML_kalender_atau_stat | hybrid | H2b ML ATAU statistik |
| H3_ML_kalender_dan_rule | hybrid | H3 ML DAN rule |
| ML_conformal_seed13 | kontrol | ML conformal seed 13 (uji ketahanan) |

Ambang CUSUM `h` dipilih harness dari well kalibrasi pada anggaran FAR gate, dan grid harness berhenti di 30. Ambang ML conformal adalah kuantil 0,995833 dari skor negatif well kalibrasi, yaitu satu minus alpha 0,004167. Ambang ML kalender dihitung dari kuantil skor negatif well kalibrasi pada anggaran menit kalender, memakai primitif harness yang sama, dan kesetiaan komposisinya dibuktikan dengan assert bahwa ambang conformal hasil komposisi sama persis dengan ambang yang dikembalikan harness.

## 4. LAPISAN A: APAKAH DETEKSI BEKERJA

Kolom lolos menghitung fold yang memenuhi FAR tidak lebih dari 6,0 per 24 jam kalender dan recall tidak kurang dari 0,50 sekaligus. Itu definisi gate A pada harness.

### 4.1 Kelas vib

| Model | Fold | Recall median | Presisi median | FAR kalender median | FAR baris median | FP total | Cakupan median | Lolos |
|---|---|---|---|---|---|---|---|---|
| persistence | 4 | 0,7405 | 0,7288 | 22,0218 | 133,8624 | 1.456 | 0,2094 | 0/4 |
| rule_kanal | 4 | 0,2361 | 0,4856 | 37,3627 | 162,6561 | 2.293 | 0,2094 | 0/4 |
| stat_cusum | 4 | 0,2363 | 0,4499 | 29,5230 | 137,9930 | 1.903 | 0,2094 | 0/4 |
| ML_conformal | 4 | 0,0256 | 0,8724 | 0,4706 | 2,9156 | 25 | 0,2094 | 0/4 |
| ML_kalender | 4 | 0,0353 | 0,8427 | 0,8001 | 4,9565 | 65 | 0,2094 | 0/4 |
| H1_stat_dan_rule | 4 | 0,1426 | 0,5930 | 19,2783 | 73,7857 | 1.033 | 0,2094 | 0/4 |
| H1b_stat_atau_rule | 4 | 0,3298 | 0,4276 | 46,4076 | 226,8634 | 3.163 | 0,2094 | 0/4 |
| H2_ML_kalender_dan_stat | 4 | 0,0049 | 0,9500 | 0,0000 | 0,0000 | 3 | 0,2094 | 0/4 |
| H2b_ML_kalender_atau_stat | 4 | 0,2931 | 0,4624 | 30,2524 | 163,7964 | 1.965 | 0,2094 | 0/4 |
| H3_ML_kalender_dan_rule | 4 | 0,0010 | 0,6075 | 0,1177 | 0,7289 | 9 | 0,2094 | 0/4 |
| ML_conformal_seed13 | 4 | 0,0093 | 0,7965 | 0,7603 | 1,6647 | 50 | 0,2094 | 0/4 |

### 4.2 Kelas ssi

| Model | Fold | Recall median | Presisi median | FAR kalender median | FAR baris median | FP total | Cakupan median | Lolos |
|---|---|---|---|---|---|---|---|---|
| persistence | 7 | 0,0361 | 0,1111 | 0,3589 | 14,7078 | 255 | 0,0653 | 0/7 |
| rule_kanal | 7 | 0,0098 | 0,0197 | 1,9355 | 39,3349 | 1.985 | 0,0653 | 0/7 |
| stat_cusum | 7 | 0,0723 | 0,0166 | 2,2889 | 46,5178 | 3.895 | 0,0653 | 0/7 |
| ML_conformal | 7 | 0,0323 | 0,0449 | 1,3457 | 7,2132 | 402 | 0,0653 | 0/7 |
| ML_kalender | 7 | 0,0323 | 0,0435 | 2,5211 | 14,2513 | 579 | 0,0653 | 0/7 |
| H1_stat_dan_rule | 7 | 0,0000 | 0,0188 | 0,9762 | 19,8385 | 1.729 | 0,0653 | 0/7 |
| H1b_stat_atau_rule | 7 | 0,0994 | 0,0156 | 3,2482 | 66,0143 | 4.151 | 0,0653 | 0/7 |
| H2_ML_kalender_dan_stat | 7 | 0,0000 | 0,0000 | 0,0679 | 2,0654 | 76 | 0,0653 | 0/7 |
| H2b_ML_kalender_atau_stat | 7 | 0,0994 | 0,0384 | 8,9139 | 126,2138 | 4.398 | 0,0653 | 0/7 |
| H3_ML_kalender_dan_rule | 7 | 0,0000 | 0,1111 | 0,0418 | 1,2392 | 51 | 0,0653 | 0/7 |
| ML_conformal_seed13 | 7 | 0,0545 | 0,0682 | 0,3615 | 25,2905 | 768 | 0,0653 | 0/7 |

Pada vib tidak ada model yang lolos. Model dengan FAR median terendah adalah H2_ML_kalender_dan_stat pada nilai 0,0000 dengan recall median 0,0049 dan presisi median 0,9500. Presisi itu tidak bermakna karena hanya berlaku pada alarm yang sangat sedikit, sehingga model tersebut bukan detektor melainkan gerbang yang hampir selalu tertutup. Model dengan recall median tertinggi adalah persistence pada 0,7405, tetapi FAR mediannya 22,0218, yaitu 3,67 kali anggaran gate.

Pada ssi, recall median tertinggi di antara semua model hanya 0,0994 dan presisi median tertinggi 0,1111, sehingga tidak ada yang dapat disebut detektor pada anggaran gate.

### 4.3 Kurva sensitivitas anggaran

Satu titik anggaran tidak cukup untuk menyimpulkan, jadi ambang diambil ulang pada anggaran 12, 24, 48, 96, 192 per 24 jam, semuanya dari well kalibrasi, lalu diukur pada well uji.

Kelas vib:

| Anggaran | ML recall | ML presisi | ML FAR | CUSUM recall | CUSUM presisi | CUSUM FAR |
|---|---|---|---|---|---|---|
| 12 | 0,0525 | 0,8013 | 1,3648 | 0,2363 | 0,4499 | 29,5230 |
| 24 | 0,1041 | 0,7781 | 3,1225 | 0,2363 | 0,4499 | 29,5230 |
| 48 | 0,1838 | 0,7539 | 5,8714 | 0,3435 | 0,4560 | 40,0728 |
| 96 | 0,2805 | 0,6391 | 10,1961 | 0,4754 | 0,3980 | 68,7354 |
| 192 | 0,4876 | 0,5539 | 30,8036 | 0,6354 | 0,3613 | 107,4858 |

Kelas ssi:

| Anggaran | ML recall | ML presisi | ML FAR | CUSUM recall | CUSUM presisi | CUSUM FAR |
|---|---|---|---|---|---|---|
| 12 | 0,0909 | 0,0399 | 3,6494 | 0,0964 | 0,0166 | 3,9215 |
| 24 | 0,2157 | 0,0762 | 6,0647 | 0,0994 | 0,0199 | 8,8147 |
| 48 | 0,3922 | 0,0360 | 10,6661 | 0,1325 | 0,0300 | 8,8147 |
| 96 | 0,7765 | 0,0317 | 19,3754 | 0,1687 | 0,0202 | 8,8147 |
| 192 | 0,8434 | 0,0246 | 39,8085 | 0,1687 | 0,0207 | 10,1985 |

Kurva ini naik seiring anggaran dan itu yang diharapkan. Yang menentukan adalah titik temunya. Pada vib, ML mencapai recall median 0,4876 pada FAR 30,8036, sedangkan persistence mencapai recall 0,7405 pada FAR 22,0218. Artinya pada FAR yang lebih rendah pun persistence sudah lebih tinggi, sehingga ML tidak tertinggal karena ambang terlalu ketat, melainkan karena memang tidak mengungguli baseline pada kelas ini. CUSUM sendiri baru mendekati persistence pada anggaran 192, yaitu recall 0,6354 pada FAR 107,4858, yang jauh di atas anggaran gate.

Komposisi bentuk (a) tidak memperbaiki keadaan. H1 statistik DAN rule menurunkan FAR median dari 29,5230 menjadi 19,2783, tetapi recall median turun dari 0,2363 menjadi 0,1426, sehingga tidak ada titik operasi yang mengalahkan persistence. Varian ATAU memang menaikkan recall ke 0,3298, tetapi FAR mediannya ikut naik ke 46,4076.

Pada ssi, ML mencapai recall median 0,8434 pada FAR 39,8085 dengan presisi median 0,0246. Pada anggaran terdekat dengan gate, yaitu 24, recall median 0,2157 dengan presisi 0,0762 dan FAR 6,0647. Presisi itu berarti sekitar 12,1 alarm palsu untuk setiap alarm benar, sehingga pemakaiannya hanya mungkin sebagai pemantauan tren, bukan alarm kritis otomatis.

### 4.4 Mengapa komposisi DAN runtuh

Ambang CUSUM tersaturasi pada nilai tertinggi grid, yaitu 30, di 8 dari 13 fold, dan pada 15 di 5 fold. Ketika anggaran FAR dipaksa sangat kecil pada well kalibrasi, CUSUM hanya bisa memenuhi anggaran dengan ambang setinggi mungkin, sehingga keluarannya hampir selalu nol. Gerbang DAN dengan komponen yang hampir selalu nol akan mematikan sinyal pasangannya. Itulah sebabnya H2 ML dan statistik pada vib punya FAR median 0,0000 dengan recall median 0,0049, dan pada ssi recall median 0,0000. Itu bukan bukti komposisinya aman, melainkan bukti komponen statistiknya tidak berfungsi pada anggaran ini.

## 5. PERBANDINGAN HYBRID LAWAN SINGLE ENGINE TERBAIK

| Kelas | Single terbaik | Hybrid terbaik | Selisih recall median | Selisih presisi median | Rasio FAR median | Selisih fold lolos |
|---|---|---|---|---|---|---|
| vib | persistence | H1b_stat_atau_rule | -0,4107 | -0,3012 | 2,1073 | 0 |
| ssi | stat_cusum | H1b_stat_atau_rule | 0,0271 | -0,0010 | 1,4191 | 0 |

Pada vib hybrid terbaik kalah pada tiga sumbu sekaligus: recall median lebih rendah 0,4107, presisi median lebih rendah 0,3012, dan FAR median 2,1073 kali lipat lebih besar. Pada ssi hybrid terbaik menang tipis pada recall median sebesar 0,0271, tetapi presisi median lebih rendah 0,0010 dan FAR median 1,4191 kali lipat lebih besar. Kemenangan tipis pada kelas yang tidak punya satu model pun dengan presisi median di atas 0,1111 tidak cukup untuk menyebut hybrid lebih baik, dan saya tidak menyebutnya demikian.

## 6. LAPISAN C: KETEPATAN DAN KETAHANAN

### 6.1 Kestabilan di dalam well

Setiap well dipecah pada median waktu menjadi paruh awal dan paruh akhir, lalu recall dihitung pada masing masing paruh.

Kelas vib:

| Model | Recall paruh awal | Recall paruh akhir | Fold menurun |
|---|---|---|---|
| persistence | 0,4603 | 0,8002 | 1/4 |
| rule_kanal | 0,0939 | 0,2593 | 0/4 |
| stat_cusum | 0,0814 | 0,2593 | 1/4 |
| ML_conformal | 0,0000 | 0,0294 | 0/4 |
| ML_kalender | 0,0000 | 0,0405 | 0/4 |
| H1_stat_dan_rule | 0,0412 | 0,1607 | 1/4 |
| H1b_stat_atau_rule | 0,1333 | 0,3580 | 1/4 |
| H2_ML_kalender_dan_stat | 0,0000 | 0,0023 | 1/4 |
| H2b_ML_kalender_atau_stat | 0,0814 | 0,3361 | 1/4 |
| H3_ML_kalender_dan_rule | 0,0000 | 0,0011 | 1/4 |
| ML_conformal_seed13 | 0,0000 | 0,0121 | 0/4 |

Kelas ssi:

| Model | Recall paruh awal | Recall paruh akhir | Fold menurun |
|---|---|---|---|
| persistence | 0,0161 | 0,0333 | 3/7 |
| rule_kanal | 0,0000 | 0,0154 | 2/7 |
| stat_cusum | 0,1064 | 0,0200 | 3/7 |
| ML_conformal | 0,0476 | 0,0000 | 3/7 |
| ML_kalender | 0,0476 | 0,0200 | 3/7 |
| H1_stat_dan_rule | 0,0000 | 0,0000 | 2/7 |
| H1b_stat_atau_rule | 0,1064 | 0,0500 | 3/7 |
| H2_ML_kalender_dan_stat | 0,0000 | 0,0000 | 0/7 |
| H2b_ML_kalender_atau_stat | 0,1064 | 0,0500 | 4/7 |
| H3_ML_kalender_dan_rule | 0,0000 | 0,0000 | 1/7 |
| ML_conformal_seed13 | 0,1351 | 0,1600 | 2/7 |

Pada ssi, hybrid H1b menurun di 3 dari 7 fold dan H2b menurun di 4 dari 7 fold, sehingga keunggulan tipis pada bagian 5 tidak stabil antar paruh waktu.

### 6.2 Variasi seed pada komponen ML

Komponen statistik dan rule deterministik, sehingga seed hanya memengaruhi ML. Seed 42 dan seed 13 dijalankan pada konfigurasi yang sama:

| Kelas | Fold | Selisih FP | Selisih TP | Selisih recall |
|---|---|---|---|---|
| vib | F-14 | -3 | -68 | -0,0605 |
| vib | F-15A | 28 | 23 | 0,0149 |
| vib | F-15_S | 0 | 0 | 0,0000 |
| vib | F-5 | 0 | 0 | 0,0000 |
| ssi | F-10 | 0 | 0 | 0,0000 |
| ssi | F-12 | 168 | 10 | 0,1205 |
| ssi | F-14 | 35 | 4 | 0,0533 |
| ssi | F-15A | -30 | -1 | -0,0323 |
| ssi | F-15_S | 107 | -4 | -0,0471 |
| ssi | F-5 | 65 | 13 | 0,1275 |
| ssi | F-9_A | 21 | 2 | 0,0364 |

Pada vib 2 dari 4 fold memberi selisih nol, sedangkan pada ssi 6 dari 7 fold berubah. Artinya komponen ML tidak stabil terhadap seed pada titik operasi ini, dan itu harus disebut sebagai ketidakpastian, bukan disamarkan dengan satu angka.

### 6.3 Cakupan menit

Cakupan menit adalah rasio jumlah baris terhadap rentang menit kalender well. Cakupan median vib adalah 0,2094 dan ssi 0,0653. Gate A pada harness mensyaratkan cakupan tidak kurang dari 0,50, sehingga syarat itu gagal di semua fold pada kedua kelas. Kegagalan cakupan bukan alasan membuang engine, sesuai kebijakan bagian 1, tetapi ia membatasi arti FAR pada satuan kalender karena penyebut kalender jauh lebih besar daripada jumlah baris berdata.

## 7. LAPISAN B: NILAI MAINTENANCE, BELUM TERUKUR

Lapisan B belum terukur, dan penyebabnya bukan kelalaian pada kartu ini. Ukuran utama lapisan B menurut kebijakan adalah waktu peringatan terhadap kejadian nyata dan berkurangnya pemeriksaan yang tidak perlu. Untuk itu dibutuhkan waktu kejadian maintenance, yaitu inspeksi, work order, atau perbaikan. Kartu S4 sudah memindai sumber itu dan hasilnya: biaya tidak ada sama sekali, work order bernomor tidak ada, jadwal inspeksi tidak ada, dan tabel kegagalan peralatan mencatat downtime nol pada semua record. Tanpa waktu kejadian nyata, waktu peringatan hanya bisa dihitung terhadap onset label, dan itu bukan lapisan B karena label bukan tindakan maintenance.

Sebagai catatan batas, harness tetap menghasilkan lead median terhadap onset label, yaitu 1,00 menit untuk persistence vib dan 17,00 menit untuk persistence ssi. Angka itu sengaja tidak dipakai sebagai nilai lapisan B karena penyebutnya onset label, bukan kejadian maintenance.

## 8. KEPUTUSAN DAN BATAS PENGGUNAAN

1. Untuk vib, tidak ada hybrid yang mengungguli persistence. Bentuk (a) dan bentuk (b) sama sama gagal, dan kegagalannya bukan karena ambang terlalu ketat, karena kurva sensitivitas pada bagian 4.3 tetap di bawah baseline pada FAR yang lebih longgar.
2. Untuk ssi, tidak ada engine yang layak sebagai alarm kritis. ML punya kemampuan peringkat yang nyata dengan AUC well uji antara 0,5387 dan 0,9067, tetapi pada anggaran gate presisi median hanya 0,0762, sehingga pemakaian yang jujur adalah pemantauan tren dengan ambang longgar dan pengawasan manusia.
3. Komposisi DAN dengan komponen statistik yang tersaturasi adalah pola yang harus dihindari pada anggaran FAR kecil. Komposisi ATAU mempertahankan recall tetapi membayar dengan FAR lebih besar.
4. Gate bukan izin pakai, dan nol fold yang lolos di kedua kelas adalah pernyataan kemampuan, bukan vonis buang.

## 9. PROVENANCE DAN REPRODUKSI

1. Seluruh angka berasal dari empat artefak JSON di `scratch/rnd/s2/`, dan setiap angka punya baris ledger berawalan `S2-` dengan 7 kolom.
2. Ledger dibangkitkan `s2c_ledger.py` yang membaca JSON lewat resolver jalur. Bila jalur tidak ada, generator berhenti dengan KeyError, sehingga angka tidak bisa dikarang.
3. Dokumen dibangkitkan `s2d_dokumen.py` yang membaca modul sumber yang sama dengan generator ledger, sehingga tabel dokumen dan baris ledger tidak mungkin berbeda.
4. Eksekusi penuh memerlukan 152,2 detik dan 277 panggilan fungsi sinyal harness.
5. Seed utama 42, seed uji 13, ambang FAR gate 6,0 per 24 jam kalender, syarat positif minimum 30 baris, grid anggaran 12, 24, 48, 96, 192.

## 10. RINGKASAN LIMA BARIS

1. vib punya 4 fold dengan 5.429 baris positif, ssi punya 9 fold dengan 592 baris positif pada 7 fold yang dapat diuji, sedangkan F-7 gugur karena hanya 3 positif dan F-9 gugur karena hanya 12 positif.
2. Tidak ada satu model pun yang lolos gate A pada kedua kelas, dengan nol fold lolos dari 4 fold vib dan nol dari 7 fold ssi.
3. Pada vib hybrid terbaik kalah dari persistence pada recall, presisi, dan FAR sekaligus, dengan selisih recall median 0,4107 dan FAR 2,1073 kali lipat.
4. Pada ssi hybrid terbaik hanya unggul 0,0271 pada recall median dengan FAR 1,4191 kali lipat dan presisi median 0,0156, sehingga tidak layak disebut lebih baik.
5. Lapisan B belum terukur karena data inspeksi, work order, dan biaya tidak ada, dan itu dibuktikan pada kartu S4, bukan diasumsikan.

## 11. YANG BELUM TERVERIFIKASI

1. Lapisan B belum terukur sepenuhnya, dan tidak akan terukur tanpa waktu kejadian maintenance.
2. Pemilihan kanal gerbang memakai AUC nilai mutlak z pada baris latih. Varian pemilihan lain, misalnya memakai presisi pada ambang tertentu, belum diuji, sehingga kanal terpilih per fold belum tentu optimal.
3. Ambang CUSUM dibatasi grid harness yang berhenti di 30. Perluasan grid sudah dicoba S1 pada hyd dan menurunkan recall, tetapi perluasan yang sama belum dijalankan untuk vib dan ssi.
4. Jumlah well vib hanya 4, sehingga validasi lintas well untuk kelas ini lemah secara desain dan tidak dapat diperbaiki dengan menambah fold.
5. Pengaruh kalibrasi pada satu well kalibrasi, yaitu `train_wells[0]`, belum diuji dengan skema kalibrasi bergilir.
6. Tafsir fisis atas kanal yang terpilih, misalnya HKLD untuk vib, belum diverifikasi terhadap literatur atau catatan lapangan, sehingga statusnya hipotesis.

