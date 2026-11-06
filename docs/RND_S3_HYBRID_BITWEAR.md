# RND-S3: HYBRID UNTUK BIT_WEAR DAN UJI KELAYAKAN DATA

Kartu: `t_9d50a5f0` · Board: `rnd-algo-2026` · Tanggal: 2026-10-28 (WIB)
Workspace: `/mnt/d/Capstone 1(v2)` (folder arsip `D:\Capstone 1` tidak disentuh)
Keluaran: dokumen ini, `scratch/rnd/s3/*.json`, dan blok S3 di `docs/RND_PROVENANCE_LEDGER.md`.

## 0. Riset pendahuluan

Riset pendahuluan: exploratory-data-analysis, scikit-learn, statistical-analysis, scientific-critical-thinking, verification-mandatory.

Cara tiap skill dipakai:

- `exploratory-data-analysis` dipakai untuk batas analisis yang jujur: laporan agregat, pemisahan ketersediaan kolom dari ada-tidaknya arti, penolakan menyimpulkan dari ketiadaan nilai yang tidak dicari, dan kewajiban melaporkan cakupan yang dipindai. Di kartu ini ia menentukan bahwa label, missing, dan satuan baris harus diukur dari berkas, bukan diwarisi.
- `scikit-learn` dipakai untuk komponen ML: pemisahan leave-one-well-out, pelatihan per fold, dan larangan menyentuh well uji saat memilih ambang. Ambang conformal diambil dari well kalibrasi, bukan dari well uji.
- `statistical-analysis` dipakai untuk memisahkan tiga kelas angka: nilai terukur langsung (hitungan baris, kolom, fold), nilai turunan (FAR dari menit kalender), dan nilai yang tidak punya penyebut (FAR pada well yang seluruh menitnya positif).
- `scientific-critical-thinking` dipakai untuk menolak klaim yang paling menggoda di kartu ini, yaitu skor tinggi sebagai bukti prediksi keausan, padahal labelnya adalah fungsi dari kolom yang sama.
- `verification-mandatory` dipakai sebagai gerbang tulis: setiap angka menunjuk sumbernya (baris ledger bila ada; cakupan terukur ada di catatan provenance), setiap ketidakmampuan diukur dibuktikan dengan pemindaian, dan percobaan yang gagal tetap dilaporkan dengan angkanya.

Riset pendahuluan: sequentialthinking, 5 pikiran (`mcp__sequentialthinking__sequentialthinking`, thoughtNumber 1..5, thoughtHistoryLength 5). Ringkas: (1) memisahkan ketersediaan record dari ketersediaan identitas bit, (2) menetapkan bahwa label yang deterministik tidak boleh diuji dengan fitur yang membentuknya, (3) satuan evaluasi harus menit kalender atau sampel kedalaman, bukan baris mentah, (4) memilih bentuk hybrid statistik dan rule serta ML dan statistik, (5) mengunci cara membuktikan ketiadaan data lapisan B. Jumlah pikiran: **5**.

### Catatan provenance (revisi 2026-10-29)

Cakupan ledger terukur pada dokumen ini: 74 dari 328 sel angka tabel (22.56 persen) punya padanan nilai pada blok `S3-` di `docs/RND_PROVENANCE_LEDGER.md`. Sel yang tidak punya padanan adalah agregat turunan antar fold atau antar berkas, dan tidak diklaim punya baris tersendiri.

Rujukan metode: konstanta metode di dokumen ini adalah konvensi internal repo dengan jejak berkas dan baris. Satu-satunya standar eksternal yang dipakai adalah ISO 2041:2018 §3.1.4 untuk nilai g, tercatat pada baris ledger L-01. Dokumen ini tidak mengklaim DOI luar, jadi butir audit DOI tidak berlaku di sini.

## 1. Cara reproduksi

| Skrip | Yang dibaca | Keluaran |
|---|---|---|
| `scratch/rnd/s3/s3a_feasibility.py` | `data/USROP_labeled.csv`, `data/volve/usrop_timestamped.csv` | `s3a_feasibility.json` |
| `scratch/rnd/s3/s3b_hybrid.py` | keduanya + `code/rnd_hybrid_harness.py` | `s3b_hybrid.json` |
| `scratch/rnd/s3/s3c_summary.py` | `s3a`, `s3b`, `scratch/v9_i1/v9_i1_RESULTS.json` | `s3c_ringkas.json` |
| `scratch/rnd/s3/s3d_dokumen.py` | `s3c_ringkas.json`, `s3b_hybrid.json` | dokumen ini + blok ledger S3 |

Perintah: `/home/neonti/.venv_audit/bin/python3 scratch/rnd/s3/s3a_feasibility.py` lalu `s3b_hybrid.py`, `s3c_summary.py`, `s3d_dokumen.py`. Lingkungan itu berisi pandas 3.0.5, numpy 2.5.1, scipy 1.18.1, scikit-learn 1.9.1, dan lightgbm 4.7.0. Durasi run hybrid tercatat 13,6 detik.

## 2. Kelayakan: hitungan yang menentukan boleh atau tidaknya uji hybrid

### 2.1 Record, well, dan label

`data/USROP_labeled.csv` berisi **198.928 baris** dan **18 kolom**, dengan **7 well**. Label `high_MSE_bit_wear` berjumlah **49.732 baris** (prevalensi 25,00%).

| Well | Baris | high_MSE | low_ROP | normal | Prevalensi high_MSE |
|---|---|---|---|---|---|
| `USROP_A 3 N-SH-F-15d.csv` | 53.041 | 7.622 | 5.278 | 40.141 | 14,37% |
| `USROP_A 4 N-SH_F-15Sd.csv` | 51.708 | 28.051 | 1.026 | 22.631 | 54,25% |
| `USROP_A 2 N-SH_F-14d.csv` | 47.645 | 4.918 | 8.053 | 34.674 | 10,32% |
| `USROP_A 5 N-SH-F-5d.csv` | 18.548 | 8.959 | 112 | 9.477 | 48,30% |
| `USROP_A 0 N-NA_F-9_Ad.csv` | 13.746 | 182 | 714 | 12.850 | 1,32% |
| `USROP_A 6 N-SH_F-9d.csv` | 7.851 | 0 | 0 | 7.851 | 0,00% |
| `USROP_A 1 N-S_F-7d.csv` | 6.389 | 0 | 0 | 6.389 | 0,00% |

Dua well tidak punya satu baris pun berlabel positif: `USROP_A 1 N-S_F-7d.csv` dan `USROP_A 6 N-SH_F-9d.csv`. Akibatnya recall tidak terdefinisi di kedua well itu, dan keduanya hanya bisa menyumbang angka alarm palsu.

### 2.2 Identitas bit dan run: tidak ada

Pemindaian token pada 18 nama kolom mencari token identitas bit (`bitno`, `bit_no`, `bitrun`, `bit_run`, `bitid`, `bit_id`, `bit_number`, `serial`, `dull`, `iaddc`, `bha_no`) dan token run (`run`, `runno`, `run_no`, `trip`, `bha`, `assembly`).

- Kolom identitas bit: **tidak ada** (hasil `False`).
- Kolom run: **tidak ada** (hasil `False`).
- Satu-satunya kolom yang mengandung kata bit adalah `Weight on Bit kkgf`, yaitu berat pada bit, bukan nomor atau seri bit.
- `Diameter mm` hanya punya **3 nilai unik**, sehingga ia menandai seksi lubang, bukan pergantian bit.
- Kolom `Unnamed: 0` punya **145.887 duplikat**, jadi ia indeks gabungan antar berkas, bukan identitas alat.

Konsekuensi yang bisa dibuktikan: **jumlah bit = 0 yang dapat dihitung, jumlah run bit = 0 yang dapat dihitung**. Yang ada hanya 7 wellbore. Setiap uji yang menuntut satuan bit atau run (misalnya leave-one-bit-out, kurva keausan per bit, biaya per bit) tidak dapat dijalankan pada berkas ini, dan itu bukan soal jumlah baris.

### 2.3 Satuan baris: grid kedalaman, bukan waktu

| Well | Baris ber-MD | Median spasi (m) | Spasi min (m) | Spasi maks (m) | Rentang MD (m) |
|---|---|---|---|---|---|
| `USROP_A 0 N-NA_F-9_Ad.csv` | 13.746 | 0,042 | 0,003 | 35,010 | 714,966 |
| `USROP_A 1 N-S_F-7d.csv` | 6.389 | 0,051 | 0,003 | 7,041 | 332,305 |
| `USROP_A 2 N-SH_F-14d.csv` | 47.643 | 0,037 | 0,003 | 94,900 | 2.478,085 |
| `USROP_A 3 N-SH-F-15d.csv` | 53.039 | 0,027 | 0,003 | 166,497 | 2.758,821 |
| `USROP_A 4 N-SH_F-15Sd.csv` | 51.708 | 0,031 | 0,003 | 24,552 | 2.689,451 |
| `USROP_A 5 N-SH-F-5d.csv` | 18.548 | 0,031 | 0,003 | 39,076 | 963,961 |
| `USROP_A 6 N-SH_F-9d.csv` | 7.851 | 0,045 | 0,003 | 7,081 | 408,365 |

Spasi median berkisar 0,027 sampai 0,051 meter, dengan lompatan terbesar 166,497 meter. Kolom baris ber-MD adalah jumlah baris yang punya nilai kedalaman, sehingga pada dua well angkanya dua baris lebih kecil daripada jumlah baris di bagian 2.1 (F-14d 47.643 lawan 47.645 dan F-15d 53.039 lawan 53.041) karena baris tanpa kedalaman tidak dapat dipakai menghitung spasi. Angka ini dibaca dari berkas mentah. Temuan E0 S-6 menyebut grid 0,015 meter pada pipeline V9; keduanya sepakat pada hal yang penting untuk kartu ini, yaitu indeks baris adalah kedalaman, bukan waktu, sehingga FAR per 24 jam tidak sah dihitung dari jumlah baris.

### 2.4 Waktu kalender: ada, tetapi turunan interpolasi, dan cakupannya rendah

| Well | Baris | Terisi | Rentang (jam) | Menit berdata | Cakupan menit |
|---|---|---|---|---|---|
| `USROP_A 3 N-SH-F-15d.csv` | 53.041 | 53.041 | 688,248 | 18.411 | 0,4458 |
| `USROP_A 4 N-SH_F-15Sd.csv` | 51.708 | 51.707 | 1.538,487 | 21.360 | 0,2314 |
| `USROP_A 2 N-SH_F-14d.csv` | 47.645 | 47.645 | 4.534,969 | 18.047 | 0,0663 |
| `USROP_A 5 N-SH-F-5d.csv` | 18.548 | 18.548 | 297,469 | 6.479 | 0,3630 |
| `USROP_A 0 N-NA_F-9_Ad.csv` | 13.746 | 13.746 | 113,778 | 3.621 | 0,5303 |
| `USROP_A 6 N-SH_F-9d.csv` | 7.851 | 7.851 | 400,250 | 1.880 | 0,0783 |
| `USROP_A 1 N-S_F-7d.csv` | 6.389 | 6.389 | 305,482 | 2.464 | 0,1344 |

Status join: `interpolated` 198.927 baris, `out_of_range` 1 baris. Jadi waktu pada berkas ini adalah hasil interpolasi kedalaman ke waktu dari DDR, bukan waktu terukur per baris.

Cakupan menit adalah menit berdata dibagi rentang menit, dan nilainya hanya 0,0663 sampai 0,5303. Artinya rekaman ini hanya menempati sebagian rentang kalender well, karena pengeboran berhenti dan menyambung. Konsekuensi untuk FAR: penyebut yang dipakai adalah **jam operasi** (menit berdata dibagi 60), bukan rentang kalender, sehingga angka FAR tidak digelembungkan oleh jeda. Cakupan tetap dilaporkan karena ia dipakai sebagai syarat gate A.

### 2.5 Label adalah fungsi deterministik dari dua kolom

Rekonstruksi label memakai aturan `MSE > P75` lalu `ROC_coef < P25` dengan persentil linear pada nilai positif memberi **198.928 baris cocok dari 198.928**, yaitu akurasi **1,000000** dan **0 baris tidak cocok**. Ambang globalnya `MSE` P75 = 256.600,4241 dan `ROC_coef` P25 = 0,000016038.

Bila ambang dihitung per well, akurasi hanya 0,679834 sampai 0,845146. Artinya label dibuat dengan ambang global, bukan per well, sehingga prevalensi per well melebar dari 1,32% sampai 54,25% dan dua well menjadi nol positif.

Ini fakta yang mengubah arti seluruh uji: label bukan hasil observasi keausan bit, melainkan indeks mekanika pengeboran. Setiap model yang memakai `MSE` atau `ROC_coef` sebagai fitur hanya merekonstruksi aturan, dan skor tinggi bukan temuan.

### 2.6 Cacat satuan yang ditemukan dan diperbaiki

Pada run pertama, indeks menit dihitung dengan `ts.astype("int64") / 1e9 / 60`. Pada pandas 3, kolom waktu bertipe `datetime64[us, UTC]`, sehingga `astype("int64")` memberi **mikrodetik**, bukan nanodetik. Akibatnya indeks menit terkompresi 1000 kali: well F-9_A yang rentangnya 113,78 jam hanya menghasilkan 8 nilai menit, dan FAR menjadi tidak sah.

Bukti pemisah, dari `scratch/rnd/s3/p9_satuan.py`: `astype("int64")` memberi 1246646927000000 sedangkan `total_seconds()` memberi 1246646927,0, dengan rasio tepat 1000000. Rentang per well menjadi 0,11 jam dengan cara lama lawan 113,78 jam dengan cara benar. Perbaikan: hitung menit lewat `(ts - epoch).dt.total_seconds() / 60`. Seluruh angka FAR di bagian 4 dan 5 berasal dari run setelah perbaikan ini.

## 3. Uji hybrid yang dijalankan

Harness dari S1 (`code/rnd_hybrid_harness.py`) dipakai langsung: `cusum_alarm`, `jendela_alarm`, `pilih_h`, `threshold_conformal`, `latih_lgb`, `rows_metrics`, `event_metrics`, `garwood_atas`, `lead_time`, `separuh`, `ringkas_records`, dan `tulis_json`. Yang ditambahkan hanya pembaca data USROP dan penghitung FAR menit kalender, karena harness S1 dibangun untuk grid menit.

| Butir | Setelan |
|---|---|
| Kanal gerbang rule | `Average Surface Torque kN.m` dengan ambang \|z\| > 2,0 pada sampel t-1 |
| Kanal statistik | `Average Standpipe Pressure kPa` |
| z | kausal: median dan MAD jendela 500 sampel lalu, digeser satu sampel |
| CUSUM | k = 0,5, grid h 0,5 sampai 30, dipilih pada well kalibrasi |
| Anggaran laju alarm | alpha = 6/1440 = 0,004167 per sampel |
| Penyebut FAR | jam operasi (menit berdata dibagi 60), bukan menit negatif dan bukan rentang kalender |
| Jendela alarm | 10 sampel |
| Fold | leave-one-well-out, 7 fold |
| Gate A | FAR <= 6,0 per 24 jam DAN cakupan menit >= 0,50 DAN recall >= 0,50 |
| Fitur ML | Weight on Bit kkgf, Average Standpipe Pressure kPa, Average Surface Torque kN.m, Rate of Penetration m/h, Average Rotary Speed rpm, Mud Flow In L/min, Average Hookload kkgf |
| Fitur terlarang | MSE, D_exp, ROC_coef (ketiganya membentuk label) |
| Seed | 42 |

Bentuk hybrid yang diuji dua, yaitu statistik dan rule (H5) serta ML dan statistik (H6). Pembanding: rule tunggal, statistik tunggal, ML kanal fisik saja, batas atas sirkular (label itu sendiri), dan satu diagnostik ML yang sengaja memakai MSE dan ROC untuk mengukur sirkularitas.

## 4. Lapisan A: apakah deteksi bekerja

| Model | Fold | TP | FP | Presisi median | Recall median | FAR median per 24 jam | Fold FAR <= 6 | Fold gate A |
|---|---|---|---|---|---|---|---|---|
| Batas atas sirkular (label itu sendiri) | 7 | 49.732 | 0 | 1,0000 | 1,0000 | 0,000 | 7/7 | 1/7 |
| Rule kanal torsi saja | 7 | 6.012 | 16.687 | 0,1492 | 0,1134 | 241,948 | 0/7 | 0/7 |
| CUSUM residual SPP saja | 7 | 9.251 | 29.886 | 0,1142 | 0,1958 | 364,478 | 0/7 | 0/7 |
| H5: CUSUM DAN rule kanal | 7 | 2.165 | 5.266 | 0,1155 | 0,0377 | 65,617 | 0/7 | 0/7 |
| ML kanal fisik saja | 7 | 48.287 | 15.105 | 0,6496 | 0,9968 | 110,432 | 2/7 | 0/7 |
| H6: ML kanal fisik DAN CUSUM | 7 | 8.897 | 2.717 | 0,6132 | 0,1784 | 12,270 | 2/7 | 0/7 |
| ML dengan MSE dan ROC (diagnostik) | 7 | 49.732 | 13.928 | 0,8496 | 1,0000 | 45,641 | 2/7 | 0/7 |

Catatan penyebut: FAR dihitung sebagai menit alarm yang tidak memuat baris positif dibagi jam operasi. Ke-7 fold punya penyebut, sehingga tidak ada fold yang dihitung gagal karena penyebutnya kosong. Yang menggagalkan gate A adalah gabungan tiga syarat: cakupan menit hanya lolos di 1 dari 7 fold, dan pada ML kanal fisik dua fold yang FAR-nya nol justru dua well tanpa positif sehingga syarat recall tidak terdefinisi di sana. Tidak ada satu fold pun yang memenuhi ketiga syarat sekaligus kecuali batas atas sirkular.

Rincian per fold untuk hybrid dan pembanding utamanya:

| Fold | Model | Presisi | Recall | FAR/24 jam | Jam operasi | Menit negatif | Menit alarm negatif | Cakupan | Lead median (sampel) |
|---|---|---|---|---|---|---|---|---|---|
| `USROP_A 0 N-NA_F-9_Ad.csv` | rule_kanal | 0,0000 | 0,0000 | 245,369 | 60,35 | 3.468 | 617 | 0,5303 | 24,0 |
| `USROP_A 0 N-NA_F-9_Ad.csv` | H5_stat_dan_rule | 0,0000 | 0,0000 | 65,617 | 60,35 | 3.468 | 165 | 0,5303 | NA |
| `USROP_A 0 N-NA_F-9_Ad.csv` | ml_fisik | 0,1714 | 1,0000 | 325,700 | 60,35 | 3.468 | 819 | 0,5303 | 12,5 |
| `USROP_A 0 N-NA_F-9_Ad.csv` | H6_ml_dan_stat | 0,2369 | 0,4231 | 90,273 | 60,35 | 3.468 | 227 | 0,5303 | 12,5 |
| `USROP_A 1 N-S_F-7d.csv` | rule_kanal | 0,0000 | NA | 241,948 | 41,07 | 2.464 | 414 | 0,1344 | NA |
| `USROP_A 1 N-S_F-7d.csv` | H5_stat_dan_rule | 0,0000 | NA | 112,792 | 41,07 | 2.464 | 193 | 0,1344 | NA |
| `USROP_A 1 N-S_F-7d.csv` | ml_fisik | NA | NA | 0,000 | 41,07 | 2.464 | 0 | 0,1344 | NA |
| `USROP_A 1 N-S_F-7d.csv` | H6_ml_dan_stat | NA | NA | 0,000 | 41,07 | 2.464 | 0 | 0,1344 | NA |
| `USROP_A 2 N-SH_F-14d.csv` | rule_kanal | 0,1492 | 0,2141 | 250,227 | 300,78 | 16.186 | 3.136 | 0,0663 | 1,0 |
| `USROP_A 2 N-SH_F-14d.csv` | H5_stat_dan_rule | 0,1756 | 0,0716 | 72,052 | 300,78 | 16.186 | 903 | 0,0663 | 13,5 |
| `USROP_A 2 N-SH_F-14d.csv` | ml_fisik | 0,4063 | 1,0000 | 110,432 | 300,78 | 16.186 | 1.384 | 0,0663 | 1,0 |
| `USROP_A 2 N-SH_F-14d.csv` | H6_ml_dan_stat | 0,5130 | 0,2399 | 21,384 | 300,78 | 16.186 | 268 | 0,0663 | 3,0 |
| `USROP_A 3 N-SH-F-15d.csv` | rule_kanal | 0,1847 | 0,1134 | 171,367 | 306,85 | 15.787 | 2.191 | 0,4458 | 20,0 |
| `USROP_A 3 N-SH-F-15d.csv` | H5_stat_dan_rule | 0,1155 | 0,0180 | 59,521 | 306,85 | 15.787 | 761 | 0,4458 | 17,0 |
| `USROP_A 3 N-SH-F-15d.csv` | ml_fisik | 0,6496 | 0,9844 | 119,902 | 306,85 | 15.787 | 1.533 | 0,4458 | 1,0 |
| `USROP_A 3 N-SH-F-15d.csv` | H6_ml_dan_stat | 0,6132 | 0,1784 | 21,978 | 306,85 | 15.787 | 281 | 0,4458 | 14,0 |
| `USROP_A 4 N-SH_F-15Sd.csv` | rule_kanal | 0,5326 | 0,0827 | 74,292 | 356,00 | 11.676 | 1.102 | 0,2314 | 7,0 |
| `USROP_A 4 N-SH_F-15Sd.csv` | H5_stat_dan_rule | 0,5698 | 0,0377 | 26,090 | 356,00 | 11.676 | 387 | 0,2314 | 11,5 |
| `USROP_A 4 N-SH_F-15Sd.csv` | ml_fisik | 0,9324 | 0,9968 | 72,067 | 356,00 | 11.676 | 1.069 | 0,2314 | 1,0 |
| `USROP_A 4 N-SH_F-15Sd.csv` | H6_ml_dan_stat | 0,9340 | 0,1724 | 12,270 | 356,00 | 11.676 | 182 | 0,2314 | 11,0 |
| `USROP_A 5 N-SH-F-5d.csv` | rule_kanal | 0,6288 | 0,1981 | 108,017 | 107,98 | 2.702 | 486 | 0,3630 | 21,0 |
| `USROP_A 5 N-SH-F-5d.csv` | H5_stat_dan_rule | 0,6557 | 0,0691 | 16,447 | 107,98 | 2.702 | 74 | 0,3630 | 1,0 |
| `USROP_A 5 N-SH-F-5d.csv` | ml_fisik | 0,8888 | 0,8621 | 142,689 | 107,98 | 2.702 | 642 | 0,3630 | 1,0 |
| `USROP_A 5 N-SH-F-5d.csv` | H6_ml_dan_stat | 0,9064 | 0,1611 | 10,446 | 107,98 | 2.702 | 47 | 0,3630 | 1,0 |
| `USROP_A 6 N-SH_F-9d.csv` | rule_kanal | 0,0000 | NA | 292,596 | 31,33 | 1.880 | 382 | 0,0783 | NA |
| `USROP_A 6 N-SH_F-9d.csv` | H5_stat_dan_rule | 0,0000 | NA | 249,702 | 31,33 | 1.880 | 326 | 0,0783 | NA |
| `USROP_A 6 N-SH_F-9d.csv` | ml_fisik | NA | NA | 0,000 | 31,33 | 1.880 | 0 | 0,0783 | NA |
| `USROP_A 6 N-SH_F-9d.csv` | H6_ml_dan_stat | NA | NA | 0,000 | 31,33 | 1.880 | 0 | 0,0783 | NA |

Bacaan lapisan A: H5 menurunkan alarm palsu terhadap komponennya tetapi juga memangkas deteksi, dengan presisi median 0,1155 dan recall median 0,0377. Tidak ada satu pun model yang memenuhi gate A di lebih dari satu fold, dan gate A hanya lolos pada batas atas sirkular, yaitu label itu sendiri. Di antara model yang tidak memakai fitur terlarang, presisi terbaik adalah ML kanal fisik dengan presisi median 0,6496 dan recall median 0,9968, tetapi FAR mediannya 110,432 per 24 jam, yaitu 18,41 kali anggaran 6,0.

## 5. Lapisan C: ketepatan dan ketahanan

1. Ambang CUSUM tersaturasi pada nilai grid terbesar h = 30,0 di **7 dari 7 fold**. Pada h itu laju alarm mentah masih 2,92% sampai 7,73% sampel, sementara anggarannya 0,42%. Artinya CUSUM residual SPP tidak dapat dikendalikan pada anggaran itu dengan grid yang ada, dan angka FAR statistik di bagian 4 harus dibaca sebagai akibat langsung dari saturasi ini.
2. Sebar presisi lintas well lebar: ML kanal fisik bergerak dari 0,1714 sampai 0,9324, dan rule kanal dari 0,0000 sampai 0,6288. Ambang yang dipinjam antar well tidak menjaga mutu.
3. Gate A tidak dapat dipenuhi pada satuan kalender bukan karena detektor saja, melainkan karena datanya: cakupan menit hanya 0,0663 sampai 0,5303, sedangkan syaratnya 0,50, sehingga hanya 1 dari 7 fold yang lolos syarat cakupan. Dua well tanpa positif menambahnya: recall tidak terdefinisi di sana.
4. Diagnostik sirkularitas: ML yang memakai `MSE` dan `ROC_coef` memberi recall median 1,0000 dan presisi median 0,8496. ML yang hanya memakai kanal fisik memberi recall median 0,9968. Selisihnya kecil, sehingga label praktis dapat direkonstruksi tanpa kedua kolom itu. Klaim prediksi keausan karena itu tidak sah dari angka ini.
5. Satuan kalender bergantung pada `est_timestamp` hasil interpolasi. Cacat satuan pada run pertama (bagian 2.6) menunjukkan bahwa satu baris kode yang salah satuan cukup untuk membuat seluruh angka FAR salah tanpa memunculkan error, jadi angka FAR di kartu ini hanya sah bersama skrip penghitungnya.

## 6. Lapisan B: belum terukur, dan buktinya

Pemindaian token biaya pada 18 kolom USROP (`cost`, `downtime`, `npt`, `price`, `usd`, `opex`, `rig_rate`, `standby`) memberi hasil **kosong**. Berkas ini tidak memuat biaya, jam henti, maupun harga per bit.

Artefak kartu S4 (`docs/RND_S4_LAYER_B_DATA.md`, `scratch/rnd/s4/inventory.json`) mendata jam henti dari DDR pada tingkat aktivitas, bukan pada tingkat bit, dan tidak ada kolom identitas bit di USROP untuk dijadikan kunci join. Karena itu nilai lapisan B untuk bit_wear **BELUM TERUKUR**, dan yang kurang bukan metode melainkan kunci: nomor bit, tanggal pasang dan lepas, biaya bit, serta jam henti yang diatribusikan ke bit.

## 7. Baseline regime bengkel dan perbandingan yang sah

Baseline regime bengkel diambil dari artefak, yaitu `scratch/v9_i1/v9_i1_RESULTS.json` pada `engines[tool_wear].heads[op_far_calibrated]`: 469 jendela, 4 alat, FP R01 per alat 1, 3, 1, 3, TLead 25, 36, 24, 20 detik, presisi run 0,5672, recall run 0,7208.

Perbandingan yang sah: bengkel dan bit_wear sama-sama tidak punya label keausan yang independen, sehingga keduanya hanya bisa dibandingkan sebagai beban alarm per unit, bukan sebagai mutu prediksi. Perbandingan yang tidak sah: menyebut FAR bit_wear 6 per 24 jam setara dengan FP 1 sampai 3 per alat di bengkel, karena satuan, panjang rekaman, dan definisi kejadiannya berbeda.

## 8. Vonis untuk kartu ini

1. bit_wear K-1 **tidak layak** untuk uji hybrid yang mengklaim prediksi keausan, karena tidak ada identitas bit, tidak ada run, dan labelnya fungsi deterministik dua kolom.
2. bit_wear K-1 **layak** untuk uji yang lebih sempit, yaitu rekonstruksi indeks dan kendali laju alarm, dan uji itu sudah dijalankan di bagian 4 dan 5 dengan hasil: tidak ada model yang lolos gate A di lebih dari satu fold.
3. Uji yang bisa dijalankan setelah data itu ada: leave-one-bit-out dengan nomor bit, kurva keausan per bit terhadap meter tergali, kalibrasi ambang per bit, dan nilai lapisan B berupa biaya per meter per bit serta jam henti per trip.

## 9. Ringkasan lima baris

1. USROP punya 198.928 baris dan 7 well, tetapi **nol** kolom identitas bit dan **nol** kolom run, sehingga satuan bit dan run tidak dapat dibentuk.
2. Label `high_MSE_bit_wear` dapat direkonstruksi persis dari `MSE > P75` dan `ROC_coef < P25` dengan akurasi 1,000000 dan 0 baris selisih, jadi label itu indeks mekanika, bukan observasi keausan.
3. Hybrid H5 (CUSUM dan rule) memberi presisi median 0,1155 dengan recall median 0,0377 dan FAR median 65,617 per 24 jam, jadi gate A tidak terpenuhi.
4. Lapisan C lemah: ambang CUSUM tersaturasi di h = 30 pada 7 dari 7 fold, cakupan menit hanya 0,0663 sampai 0,5303 sehingga syarat cakupan 0,50 gagal di 6 dari 7 fold, dan dua well tanpa positif membuat recall tidak terdefinisi.
5. Lapisan B BELUM TERUKUR karena tidak ada kolom biaya atau jam henti di USROP dan tidak ada kunci bit untuk join ke data DDR; yang kurang adalah kunci, bukan metode.

## 10. Yang belum terverifikasi

- Apakah `MSE` dan `ROC_coef` di berkas ini dihitung dengan rumus Teale yang sama seperti kode pipeline, karena rumusnya tidak dihitung ulang di kartu ini.
- Apakah dua well tanpa positif benar-benar tidak mengalami kondisi high_MSE, atau hanya tidak terekam, karena tidak ada catatan operasi per well di berkas ini.
- Ketepatan `est_timestamp`: interpolasi linear kedalaman ke waktu tidak diuji terhadap waktu pengeboran nyata per baris, sehingga FAR kalender adalah perkiraan, bukan hasil ukur langsung.
- Apakah CUSUM akan dapat dikendalikan bila grid h diperluas di atas 30, karena perluasan grid belum dijalankan di kartu ini.
- Kestabilan lintas seed untuk komponen ML, karena kartu ini hanya memakai seed 42.
- Nilai lapisan B untuk bit_wear, karena datanya tidak ada di lingkungan ini.

