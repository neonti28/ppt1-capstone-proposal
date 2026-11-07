# RND-R3: DEKOMPOSISI SINYAL DAN KERNEL (VMD/EMD/WAVELET + SVM/kNN-DTW/MATRIX PROFILE)

Status: hasil riset dan pengukuran, bukan vonis tier · Board: `rnd-algo-2026` · Kartu: `t_1fe4eed0` · 2026-10-27 (WIB)
Workspace: `/mnt/d/Capstone 1(v2)` (folder arsip `D:\Capstone 1` tidak disentuh)
Keluaran: dokumen ini + baris ledger `R3-01` sampai `R3-55` di `docs/RND_PROVENANCE_LEDGER.md`
Kelas bukti dipakai konsisten: OBSERVED (dibaca dari file hasil), DERIVED (turunan aritmetik dari angka terukur), HIPOTESIS (belum diuji, wajib punya falsifier), BELUM TERUKUR (tidak ada angka).

## 0. Riset pendahuluan

Baris wajib: **Riset pendahuluan: literature-review, paper-lookup, aeon, scikit-learn, scientific-critical-thinking, verification-mandatory.**

| Skill | Bagaimana dipakai di kartu ini |
|---|---|
| `literature-review` | Menyusun pencarian bertahap (VMD, EMD/EEMD, wavelet, SVM, DTW, matrix profile, hibrida VMD+SVM dan GWO/WOA) dan menyaring hasil ke rujukan yang bisa dibuka, bukan daftar judul yang tidak diperiksa. |
| `paper-lookup` | Menjalankan verifikasi DOI dua lapis lewat Crossref (metadata judul, tahun, penulis pertama) dan pendaftaran `doi.org` (status redirect), dengan perintah tersimpan di `verify_doi_r3.sh`, `verify_doi_r3b.sh`, `verify_doi_r3c.sh`. |
| `aeon` | Menjadi acuan pemilihan estimator deret waktu: `KNeighborsTimeSeriesClassifier` dengan jarak DTW, `STOMP` untuk matrix profile, `Normalizer` untuk z-normalisasi. |
| `scikit-learn` | Menjadi acuan aturan pipa: praproses wajib di dalam `Pipeline` agar tidak bocor antar fold, `StandardScaler` hanya untuk estimator berskala, dan pembanding linear lawan RBF. |
| `scientific-critical-thinking` | Memisahkan OBSERVED dari DERIVED, menolak menyimpulkan sebab dari korelasi, dan menandai keluaran yang rusak (mis. fraksi energi wavelet tidak ternormalisasi) sebagai alat ukur yang perlu diperbaiki, bukan sebagai temuan. |
| `verification-mandatory` | Mewajibkan setiap angka punya baris ledger, menolak angka tanpa sumber, dan menutup laporan dengan daftar yang belum terverifikasi. |

Baris wajib: **sequ-mcp dipakai 5 pikiran** (`mcp__sequentialthinking__sequentialthinking`, `thoughtNumber` 1 sampai 5, `thoughtHistoryLength` 5). Jumlah pikiran: **5**. Ringkas: (1) memisahkan "VMD tidak bisa dijalankan" dari "VMD tidak informatif" pada fs rendah, (2) menguji degenerasi pusat mode VMD dari angka `spacing_min_hz`, (3) memisahkan tiga kelompok biaya kernel (SVM murah, DTW mustahil, matrix profile layak), (4) memetakan tiga lapis overfitting hibrida, (5) menetapkan skor kesesuaian per mode dari ketersediaan kanal, sirkularitas label, dan keberadaan baseline lebih murah.

## 1. Syarat sinyal untuk dekomposisi (VMD, EMD/EEMD, wavelet)

### 1.1 Laju sampel dan Nyquist

Syarat minimal yang tidak bisa dilanggar: frekuensi Nyquist `fs/2` harus berada di atas pita yang ingin dibedah. Untuk diagnostik bantalan, pita yang relevan adalah frekuensi karakteristik cacat (BPFO/BPFI/BSF/FTF) beserta sideband porosnya, dan tutorial rujukan menempatkannya pada orde beberapa kali frekuensi poros (Randall & Antoni 2011, DOI `10.1016/j.ymssp.2010.07.017`, terverifikasi).

Angka terukur pada data D0 (OBSERVED, `scratch/rnd_d0` dan ulang di `m3_decomp.json`):

| Well | Kanal | Sampel | dt median (s) | Laju (Hz) | Nyquist (Hz) | Segmen | Segmen terpanjang (sampel) | Jendela 256/512/1024 |
|---|---|---|---|---|---|---|---|---|
| F-15_S | `VIBLAT_RT` | 141.114 | 3,000 | 0,3333 | 0,1667 | 4.126 | 5.457 | 475/214/91 |
| F-15_S | `CRPM_RT` | 137.170 | 3,000 | 0,3333 | 0,1667 | 4.139 | 5.413 | 464/208/87 |
| F-15_S | `SHKRSK_RT` | 152.923 | 3,000 | 0,3333 | 0,1667 | 5.177 | 5.458 | 511/232/97 |
| F-14 | `VIBLAT_RT` | 2.247 | 60,048 | 0,0167 | 0,0083 | 1.551 | **4** | **0/0/0** |
| F-14 | `SHKRSK_RT` | 21.643 | 47,952 | 0,0209 | 0,0104 | 5.409 | 1.644 | 31/6/2 |
| F-9_A | `SHKRSK_RT` | 45.927 | 3,000 | 0,3333 | 0,1667 | 67 | 3.828 | 149/66/26 |
| F-10 | `SHKRSK_RT` | 69.192 | 3,000 | 0,3333 | 0,1667 | 327 | 3.484 | 179/73/25 |

Tafsir yang bisa dipertahankan:

1. Laju sampel tertinggi yang tersedia adalah **0,3333 Hz**, sehingga Nyquist tertinggi **0,1667 Hz**. VMD, EMD, dan wavelet hanya bisa membedah pita di bawah 0,17 Hz. Pita itu berada jauh di bawah frekuensi karakteristik cacat bantalan pada putaran rig, jadi dekomposisi di sini tidak akan memisahkan komponen cacat, hanya memisahkan drift dan gerak lambat.
2. `VIBLAT_RT` F-14 bukan deret panjang yang jarang: kanal itu terpecah menjadi 1.551 segmen dengan segmen terpanjang **4 sampel** (0,0667 jam) karena pemutus gap 60 detik. Jendela 256 tidak ada sama sekali, jadi VMD pada kanal itu tidak punya masukan sah.
3. Jendela 1024 yang benar-benar utuh per kanal hanya berkisar 0 sampai 97 buah (OBSERVED). Jumlah itu cukup untuk demonstrasi, tidak cukup untuk melatih model per kanal dengan validasi antar-well.

### 1.2 Stasioneritas dan dominasi drift

Dekomposisi mengasumsikan sinyal bisa dipisah menjadi mode dengan pusat frekuensi yang bermakna. Kalau 95% daya berada di pita paling rendah, mode yang dihasilkan akan meniru drift, bukan getaran.

Angka pada F-15_S `VIBLAT_RT` (segmen terpanjang 5.457 sampel, OBSERVED `m3_decomp.json`):

- resolusi frekuensi FFT 6,108e-05 Hz, frekuensi dominan **0,005559 Hz**, `peak_share` **0,1246**;
- fraksi daya di bawah 0,05 Hz = **0,9586**.

Artinya 95,86% daya ada di bawah 0,05 Hz, sementara pita yang bisa dibedah sampai 0,1667 Hz. Sisa daya di atas 0,05 Hz sekitar 4,14% dan itulah satu-satunya bagian yang mungkin memuat informasi getaran.

Wavelet db4 level 5 memberi gambaran searah tetapi **keluarannya belum ternormalisasi**: `energy_frac` aproksimasi `a5` (0 sampai 0,0104 Hz) = 0,9528, sedangkan jumlah seluruh pita = 1,192 dan ada pita `d0` berlabel 0,1667 sampai 0,3333 Hz yang berada **di atas Nyquist**. Label pita dan normalisasi pada keluaran ini tidak konsisten, jadi angkanya dipakai hanya sebagai indikasi relatif (a5 jauh mendominasi d1 dan d0), bukan sebagai angka absolut. Perbaikan alat ukur dicatat sebagai temuan QA.

EMD pada segmen yang sama menghasilkan **5 IMF** dengan IMF1 di 0,0107 Hz dan `energy_frac` 0,6809; jumlah seluruh IMF = 2,45, jadi kolom yang sama juga tidak ternormalisasi. Jumlah IMF 5 pada sinyal yang didominasi drift adalah tanda mode-mixing: IMF memecah drift menjadi beberapa komponen, bukan memisahkan getaran.

### 1.3 Pemilihan K dan alpha pada VMD

Sapuan yang dijalankan: **alpha 500, 2000, 5000** dan **K 2 sampai 6**, pada 1.024 sampel F-15_S `VIBLAT_RT` (OBSERVED, 15 kombinasi per kanal). Hasil untuk kanal itu:

| alpha | K=2 resid | K=3 | K=4 | K=5 | K=6 |
|---|---|---|---|---|---|
| 500 | 0,0205 | 0,0140 | 0,0109 | 0,00676 | 0,00431 |
| 2000 | 0,0442 | 0,0266 | 0,0190 | 0,0161 | 0,0111 |
| 5000 | 0,1125 | 0,0590 | 0,0561 | 0,0520 | 0,0449 |

`resid_frac` turun monoton terhadap K dan naik terhadap alpha. Membaca `resid_frac` saja akan menuntun ke K=6, alpha=500 karena residu terkecil. Residu kecil bukan kriteria yang benar, karena residu akan selalu turun bila jumlah mode ditambah.

Bukti yang membatalkan pembacaan naif itu ada di kolom jarak antar pusat mode. `spacing_min_hz` pada kanal dan sapuan yang sama berkisar **1,27e-09 sampai 6,45e-06 Hz** terhadap lebar pita 0,1667 Hz. Dua pusat mode yang berjarak 1e-8 lebar pita berarti praktis bertumpuk di titik yang sama, sehingga mode yang "ditambahkan" bukan komponen baru.

Tambahan yang memperkuat (DERIVED dari keluaran): `cf_max_hz` sama dengan `(K-1)·fs/(2K)` untuk K=2..5 pada ketiga nilai alpha, yaitu 0,0833; 0,1111; 0,125; 0,1333 Hz. Pusat mode berhenti tepat di grid inisialisasi seragam, artinya proses ADMM tidak menggeser pusat mode secara berarti. Pada kondisi ini **K tidak teridentifikasi dari data**, sehingga memilih K dengan menyapu nilai lalu mengambil residu terkecil adalah prosedur yang menghasilkan angka, bukan pengetahuan.

Kegagalan implementasi yang harus dicatat terpisah: dari **105 percobaan VMD** (7 kanal x 15 kombinasi), **75 gagal** dengan pesan `ValueError: zero-size array to reduction operation minimum which has no identity`. Kelima kanal yang gagal seluruhnya adalah semua `SHKRSK_RT` yang diuji ditambah `VIBLAT_RT` F-14. VMD hanya berhasil pada 2 dari 7 kanal, yaitu `VIBLAT_RT` dan `CRPM_RT` F-15_S. Penyebab teknis per kanal **belum didiagnosis**, jadi angka 75/105 dilaporkan sebagai batas implementasi alat ukur, bukan sebagai sifat algoritma.

Aturan pemilihan yang bisa dipakai kalau data nanti memenuhi syarat:

1. Tetapkan K dari pengetahuan fisika (jumlah komponen yang memang dicari: drift, putaran poros, orde harmonik), bukan dari residu terkecil.
2. Bekukan alpha pada satu nilai dari satu well latih, lalu uji nilai itu di well lain tanpa diubah.
3. Tolak konfigurasi yang `spacing_min_hz`-nya di bawah resolusi FFT, karena mode bertumpuk tidak bisa diinterpretasi.
4. Wajib ada pembanding: hasil dekomposisi harus mengalahkan statistik jendela polos (mean, std, RMS, kurtosis) pada metrik yang sama, kalau tidak dekomposisi hanya menambah biaya.

### 1.4 Risiko leakage kalau dekomposisi dilakukan pada seluruh deret

Ini risiko terbesar dan paling sering tidak dilaporkan di paper terapan. Kalau VMD/EMD/wavelet dijalankan pada deret penuh sebelum pembagian latih/uji, setiap jendela membawa informasi dari masa depan melalui dua jalur:

1. **Pusat mode global.** VMD mengoptimalkan pusat frekuensi memakai seluruh deret, sehingga mode di menit ke-100 sudah "tahu" spektrum menit ke-9.000.
2. **Normalisasi dan ambang.** Skala dan ambang yang dihitung dari deret penuh memindahkan distribusi uji ke dalam latih.

Aturan yang harus dipakai pada pipeline ini: dekomposisi **kausal per jendela**, yaitu untuk jendela yang berakhir di waktu `t`, dekomposisi hanya memakai sampel `<= t`; parameter K, alpha, dan jenis wavelet dibekukan dari data latih saja; dan hasil dekomposisi tidak boleh dipakai untuk menghitung statistik normalisasi lintas well. Tanpa tiga syarat itu, skor tinggi yang muncul adalah artefak, bukan kemampuan model.

Risiko kedua yang khas proyek ini: **sirkularitas label**. Label `vib` didefinisikan dari `VIBLAT_RT >= 32,17405 ft/s2` (REGISTRY `code/v9_i1_pipeline.py` baris 74 dan seterusnya). Kalau fitur yang masuk model adalah hasil dekomposisi kanal `VIBLAT_RT` yang sama, model mempelajari ulang definisi label, bukan gejala fisik. Ini sudah tercatat sebagai temuan audit implementasi di `docs/RND_E0_AUDIT_ENGINE.md` dan berlaku juga untuk semua usulan dekomposisi pada kanal label.

### 1.5 Syarat per metode, ringkas

| Metode | Syarat panjang | Syarat laju sampel | Syarat stasioneritas | Status pada data D0 |
|---|---|---|---|---|
| VMD | minimal beberapa ratus sampel per mode yang dicari; 1.024 cukup untuk demonstrasi | `fs/2` di atas pita yang dicari | lokal stasioner dalam jendela | GAGAL: Nyquist 0,1667 Hz, 75/105 percobaan gagal, mode bertumpuk |
| EMD/EEMD | puluhan sampai ratusan sampel; rentan endpoint effect pada segmen pendek | sama | tidak wajib stasioner, tetapi mode-mixing memburuk pada sinyal non-stasioner | GAGAL untuk tujuan diagnostik: 5 IMF didominasi drift, energi tidak ternormalisasi |
| Wavelet (db4, level 5) | minimal `2^level` sampel; level 5 butuh >= 32 sampel | `fs/2` menentukan pita tertinggi | tidak wajib | SEBAGIAN: bisa dijalankan, tetapi pita di atas 0,05 Hz hanya memuat 4,14% daya mentah (1 dikurangi 0,9586), dan label pita pada keluarannya belum konsisten |

## 2. Kernel: SVM, kNN-DTW, matrix profile

### 2.1 SVM

Kebutuhan normalisasi. Diukur pada dataset `vib` (23.922 jendela, 10 fitur, 5.429 positif, 4 well) dengan satu pembagian latih/uji temporal (OBSERVED `m3_decomp.json` bagian `C_biaya.svm`):

| Perlakuan | AUC F-14 | AUC F-15A | AUC F-15_S | AUC F-5 | Median AUC | Waktu fit total |
|---|---|---|---|---|---|---|
| Tanpa standardisasi | 0,8876 | 0,8041 | 0,6803 | 0,8448 | **0,8245** | 36,36 s |
| Dengan standardisasi | 0,7134 | 0,8051 | 0,6470 | 0,8610 | **0,7592** | 16,36 s |

Pembacaan yang benar: standardisasi menurunkan median AUC sebesar 0,0653 pada satu pembagian ini, dan menaikkan AUC di F-5. Selisih sebesar itu pada satu split **bukan bukti** bahwa standardisasi merugikan, karena tidak ada interval kepercayaan dan tidak ada pengulangan seed. Yang boleh disimpulkan hanya: pada data ini standardisasi tidak otomatis menaikkan kinerja, sehingga klaim "SVM wajib distandardisasi" harus diuji per kasus, bukan diasumsikan. Untuk protokol yang benar, standardisasi dimasukkan ke dalam `Pipeline` agar di-fit ulang per fold (aturan `scikit-learn`), bukan di-fit sekali pada seluruh data.

Biaya komputasi relatif murah: RBF pada 23.922 baris selesai 7,99 s, linear 0,05 s. Dibandingkan DTW pada bagian berikut, SVM pada fitur tabular bukan hambatan biaya.

Interpretabilitas. SVM RBF tidak memberi koefisien per fitur seperti regresi, sehingga untuk kebutuhan "kenapa alarm ini menyala" SVM lebih lemah daripada rule atau pohon. Pengganti yang tersedia tanpa biaya tambahan: importance dari model berbasis pohon yang sudah ada di jalur boosting, atau koefisien SVM linear yang bisa dibaca.

### 2.2 kNN-DTW

Biaya terukur (OBSERVED `m3_decomp.json` bagian `C_biaya.dtw`, satu pasangan jarak):

| Panjang seri | ms per pasangan | Estimasi 1-NN atas 23.922 jendela (jam) |
|---|---|---|
| 32 | 0,8431 | 134,01 |
| 64 | 2,7576 | 438,33 |
| 128 | 14,5964 | 2.320,17 |
| 256 | 49,2067 | 7.821,65 |
| 512 | 220,3579 | 35.027,00 |
| 1024 | 864,2339 | 137.374,35 |

Angka ini mematikan kNN-DTW sebagai komponen produksi pada ukuran jendela yang dipakai detektor. Bahkan pada panjang 32, satu kali klasifikasi seluruh dataset butuh 134 jam; pada 1024 dibutuhkan 137.374 jam. Batasan bukan pada akurasi (DTW memang kuat untuk bentuk), tetapi pada anggaran waktu.

Kalau DTW tetap ingin dipakai untuk validasi kecil, syaratnya: z-normalisasi per jendela (tanpa itu DTW membandingkan level, bukan bentuk), konstrain Sakoe-Chiba untuk memotong jalur (Sakoe & Chiba 1978, DOI `10.1109/TASSP.1978.1163055`), dan pengurangan jumlah prototipe (Xi et al. 2006, DOI `10.1145/1143844.1143974`, numerosity reduction). Ratanamahatana & Keogh 2004 (DOI `10.1137/1.9781611972740.2`) menunjukkan konstrain yang dipelajari bisa lebih akurat sekaligus lebih cepat, tetapi tetap tidak mengubah orde biaya.

Catatan audit rujukan: berkas verifikasi lama memakai DOI `10.1007/978-3-540-30075-5_46` berlabel "Ratanamahatana & Keogh 2004". Crossref untuk DOI itu mengembalikan makalah basis data (Bellatreche, 2004, "An a Priori Approach for Automatic Integration of Heterogeneous and Autonomous Databases"), jadi DOI tersebut **salah** dan tidak dipakai. DOI yang benar sudah diverifikasi pada tabel rujukan.

### 2.3 Matrix profile

Biaya terukur (OBSERVED `m3_decomp.json` bagian `C_biaya.matrix_profile`, `m=60`):

| Panjang seri | Jumlah query | Waktu satu query (s) | Nilai profil minimum |
|---|---|---|---|
| 3.000 | 2.941 | 0,00039 | 10,4107 |
| 6.000 | 5.941 | 0,00044 | 10,3981 |
| 12.000 | 11.941 | 0,00076 | 10,2860 |

Skalanya mendekati linear dan tiga orde lebih murah daripada DTW penuh. Matrix profile juga memberi keluaran yang bisa dibaca langsung: jarak ke tetangga terdekat per posisi, sehingga motif (pola berulang) dan discord (pola menyimpang) bisa ditunjuk dengan indeks, bukan dengan koefisien model. Untuk kebutuhan "tunjukkan kejadian yang mirip kejadian ini" di rig, ini bentuk interpretasi yang lebih berguna daripada SVM.

Acuan metode: Yeh et al. 2016 (DOI `10.1109/ICDM.2016.0179`) untuk STAMP dan penyatuan motif/discord. Implementasi tersedia di `aeon` (`STOMP`), sehingga tidak perlu menulis ulang.

### 2.4 Ringkas perbandingan kernel

| Kriteria | SVM (fitur tabular) | kNN-DTW | Matrix profile |
|---|---|---|---|
| Biaya pada 23.922 jendela | 0,05 s (linear) sampai 7,99 s (RBF) | 134 jam (n=32) sampai 137.374 jam (n=1024) | 0,00039 s per query (n=3.000) |
| Kebutuhan normalisasi | ya, di dalam `Pipeline`; efek pada data ini belum terbukti menaikkan AUC | wajib z-normalisasi per jendela | wajib z-normalisasi per subseri |
| Interpretabilitas | rendah untuk RBF, sedang untuk linear | tinggi (tetangga terdekat bisa ditunjuk) | tinggi (indeks motif dan discord) |
| Peran usulan | pembanding murah untuk ranking pada fitur jendela | hanya untuk validasi kecil, bukan produksi | pengganti DTW untuk pencarian motif dan discord |

## 3. Hibrida yang diminta operator

### 3.1 VMD + SVM

Arsitektur: sinyal kanal dipecah VMD menjadi K mode, tiap mode diringkas menjadi fitur (energi, kurtosis, pusat frekuensi), fitur digabung dengan fitur jendela yang sudah ada, lalu SVM dilatih pada gabungan itu.

Urutan yang benar: (1) potong jendela kausal, (2) jalankan VMD per jendela dengan K dan alpha yang dibekukan, (3) hitung fitur per mode, (4) latih SVM di dalam `Pipeline` dengan standardisasi di dalam fold, (5) uji pada well yang tidak dipakai melatih.

Titik overfitting: pemilihan K dan alpha. Kalau K dan alpha disapu pada data uji atau pada seluruh deret, hasilnya selalu terlihat bagus dan tidak bisa diulang. Pada data ini risikonya bukan teoretis: sapuan 15 kombinasi di atas menunjukkan residu bisa ditekan dari 0,0205 ke 0,0043 hanya dengan menambah mode, tanpa mode itu benar-benar terpisah.

Bukti bahwa hibrida ini bukan jalan pintas: skalanya sudah runtuh di langkah pertama, karena VMD hanya berhasil pada 2 dari 7 kanal yang diuji. Menambahkan SVM di belakangnya tidak memperbaiki masukan yang tidak ada.

### 3.2 VMD + GWO-SVM

Arsitektur: GWO menyetel hyperparameter SVM (C, gamma), sedangkan VMD memasok fitur. Dua sumbu optimasi ini harus dipisah tegas, karena kesalahan yang umum adalah membiarkan GWO juga menyetel K dan alpha VMD pada data uji.

Urutan optimasi yang bisa dipertanggungjawabkan:

1. Tetapkan K dan alpha VMD dari pengetahuan fisika, bekukan.
2. Bagi data secara temporal per well (latih di well A, uji di well B).
3. Jalankan GWO hanya di dalam data latih dengan validasi silang internal, objektif = AUPRC pada validasi dalam, bukan akurasi latih.
4. Bekukan hyperparameter terbaik, latih ulang pada seluruh latih, uji sekali di well uji.
5. Laporkan sebaran hasil antar well, bukan satu angka terbaik.

Titik overfitting ada tiga lapis dan harus disebut terpisah: (a) GWO mengoptimalkan skor validasi yang sama berulang kali, sehingga skor validasi menjadi bagian dari objektif (optimizer overfitting); (b) seleksi konfigurasi terbaik dari banyak percobaan tanpa koreksi multiplisitas; (c) VMD yang dijalankan pada deret penuh sebelum split, yang membocorkan masa depan. Rujukan yang relevan untuk pola VMD ditambah optimasi metaheuristik pada bantalan: Gai et al. 2020 (DOI `10.1016/j.measurement.2020.107901`, GWO memperbaiki VMD lalu klasifikasi) dan Li et al. 2023 (DOI `10.3390/electronics12061290`, optimasi parameter VMD plus SVM). Keduanya melaporkan akurasi tinggi pada dataset bantalan laboratorium, dan keduanya tidak menjawab pertanyaan yang berlaku di sini: apakah laju sampel 0,3333 Hz cukup.

### 3.3 WOA + GWO

Arsitektur: dua metaheuristik dijalankan berurutan atau berselang, misalnya WOA melakukan eksplorasi global lalu GWO memperhalus di sekitar kandidat terbaik, atau populasi digabung dengan pembagian peran. Varian yang terdokumentasi: Singh & Bansal 2018 (DOI `10.3390/mca23010014`, hibrida WOA dengan strategi mean GWO untuk optimasi global).

Catatan penting: WOA+GWO tidak menyentuh dekomposisi sama sekali. Hibrida ini hanya menyetel hyperparameter model. Karena itu kelayakannya bergantung sepenuhnya pada model dasarnya, dan pada kartu R1 (`docs/RND_R1_METAHEURISTIK.md`) sudah dicatat bahwa metaheuristik di kasus ini berperan sebagai penyetel, bukan sebagai penambah informasi. Menjalankan dua metaheuristik berturut-turut menambah jumlah evaluasi fungsi tanpa menambah informasi baru, sehingga risiko overfitting pada skor validasi naik sebanding jumlah evaluasi.

Titik overfitting: skor validasi dipakai dua kali sebagai objektif (oleh WOA lalu oleh GWO), dan tidak ada pengujian terpisah yang tersisa untuk mengukur optimisme seleksi. Syarat minimum yang harus ditulis di protokol: simpan satu well sebagai uji akhir yang tidak pernah dilihat metaheuristik, dan laporkan selisih antara skor validasi dalam dan skor uji akhir. Kalau selisihnya besar, itu bukti optimisme seleksi, bukan bukti algoritma bagus.

## 4. Kecukupan data D0 untuk VMD/EMD (jawaban poin 4)

Kesimpulan: **tidak memenuhi syarat**, dan bukan karena panjang jendela, melainkan karena laju sampel dan sifat kanal.

| Syarat | Ambang yang dibutuhkan | Kondisi data D0 | Selisih |
|---|---|---|---|
| Laju sampel untuk pita bantalan | orde ratusan Hz sampai kHz, karena BPFO/BPFI berada pada orde beberapa kali putaran poros dan harmoniknya | 0,0167 sampai 0,3333 Hz | 3 sampai 5 orde kekurangan |
| Nyquist | di atas pita yang dicari | 0,0083 sampai 0,1667 Hz | di bawah 0,2 Hz |
| Segmen kontinu | minimal beberapa ribu sampel utuh per jendela | 4 sampai 5.458 sampel; `VIBLAT_RT` F-14 hanya 4 sampel | fragmen terburuk tidak bisa dipakai |
| Kanal kontinu (bukan terkuantisasi) | nilai hampir unik per sampel | `SHKRSK_RT` F-10: 69.192 baris, **4 nilai unik**, 99,81% nol; `VIBLAT_RT` F-15_S: 141.114 baris, **36 nilai unik**, satu nilai mendominasi 40,57% | kanal berperilaku sensor diskret atau tertahan, bukan gelombang kontinu |
| Panjang deret latih | ribuan jendela per kondisi | 23.922 jendela `vib`, tetapi hanya 4 well, dan jendela 1024 utuh hanya 0 sampai 97 per kanal | cukup untuk statistik jendela, tidak untuk dekomposisi per kanal |

Bukti kuantisasi itu penting karena mengubah diagnosis. Kanal `SHKRSK_RT` yang tampak seperti sinyal getaran ternyata membawa 4 nilai bulat (0, 1, 2, 3) dengan 99,81% nol, sehingga dekomposisi apa pun pada kanal itu hanya akan mengubah deret kejadian menjadi bentuk gelombang buatan. Angka 4 nilai unik dan 99,81% ini OBSERVED dari `m4_kanal_konstan.json` (F-10: 69.062 dari 69.192 baris bernilai nol).

Yang harus diakuisisi kalau dekomposisi getaran ingin benar-benar dipakai:

1. **Akuisisi high-frequency drilling dynamics**: accelerometer pada BHA dengan laju sampel minimal orde 1 kHz sampai 10 kHz, tersimpan sebagai deret waktu mentah per run, bukan agregat per menit. Tanpa ini, seluruh keluarga VMD/EMD/wavelet tetap tidak bisa dipakai untuk diagnostik bantalan.
2. **Kanal yang tidak terkuantisasi**: pastikan keluaran sensor disimpan pada resolusi penuh (float), dengan metadata skala (g atau ft/s2) dan titik pemasangan.
3. **Segmen kontinu minimal 60 detik tanpa gap pada laju 1 kHz**, yaitu 60.000 sampel utuh per jendela, dan pencatatan gap yang eksplisit.
4. **Minimal 3 well dengan kondisi berbeda** untuk uji transfer, karena semua metode dekomposisi rentan menyesuaikan diri pada satu well.
5. **Label kondisi bantalan yang independen dari kanal getaran** (mis. catatan inspeksi atau penggantian bit/bearing), supaya dekomposisi tidak sirkular terhadap label.

Sampai kelima hal itu ada, VMD/EMD/wavelet tetap dicatat sebagai **TIDAK LAYAK** pada data sekarang, dan itu kesimpulan berbasis pengukuran, bukan penolakan terhadap metode.

## 5. Skor kesesuaian per mode

Skor 0 sampai 5, dihitung dari empat komponen: ketersediaan kanal, kecukupan laju sampel, risiko sirkularitas label, dan keberadaan baseline lebih murah. Skor bukan penilaian kualitas algoritma, tetapi penilaian apakah algoritma itu bisa dipakai pada data ini sekarang.

| Mode | Kanal yang relevan | Laju | Sirkularitas | Baseline lebih murah | Skor dekomposisi | Skor SVM | Skor matrix profile | Peran usulan |
|---|---|---|---|---|---|---|---|---|
| `vib` | `VIBLAT_RT` ada di 6 dari 9 well | 0,0167 sampai 0,3333 Hz | tinggi: label = `VIBLAT_RT >= 32,17405` | RF ranking (AUPRC 0,441 sampai 0,912) dan rule (P 0,87 sampai 0,95) | **0** | 2 | 2 | Dekomposisi ditolak. SVM hanya sebagai pembanding murah pada fitur jendela (median AUC 0,8245 satu split), bukan pengganti rule. Matrix profile untuk menunjuk episode mirip, bukan alarm. |
| `ssi` | `CRPM_RT` dan `SPPA` | 0,25 sampai 0,3333 Hz | sedang: label dari rasio RMS/peak, bukan bentuk gelombang | hybrid rule+persistence (FP turun 2.091 ke 927, 9/9 well) | **0** | 1 | 1 | Dekomposisi tidak relevan karena SSI sudah merupakan ringkasan jendela. Tidak ada usulan. |
| `shk` | `SHKRSK_RT` | 0,0167 sampai 0,3333 Hz | sedang: label = jumlah kejadian pada kanal yang sama | rule FAR 0,67 sampai 6,6 (lolos FAR <= 6 di 7 dari 9 fold) | **0** | 1 | 1 | Kanal membawa 4 nilai unik dengan 99,8% nol, jadi tidak ada gelombang untuk didekomposisi. Rule yang sudah ada tetap dasar. |
| `tool_wear` | 27 fitur tabular bengkel, 469 jendela, 4 alat | tidak berlaku (bukan deret waktu berkecepatan tinggi) | rendah: label dari run dan kondisi | canary AUPRC 0,516 sampai 0,612 | **0** | 3 | 0 | SVM pada 27 fitur adalah pembanding yang masuk akal dan murah untuk ranking lintas alat, dengan catatan label konstan dalam run. Dekomposisi tidak punya objek. |
| `stuck`, `hyd`, `bit_wear` | tidak termasuk lingkup kartu ini | tidak berlaku | tidak berlaku | sudah ada rule/persistence | 0 | 0 | 0 | Tidak diusulkan. |

Ringkas: **tidak ada detektor yang layak mendapat dekomposisi VMD/EMD/wavelet pada data sekarang**. Dari tiga kernel, yang punya tempat adalah SVM sebagai pembanding murah pada fitur yang sudah ada, dan matrix profile sebagai pengganti DTW untuk pencarian motif. kNN-DTW ditolak karena biaya.

## 6. Rujukan (semua sudah diperiksa; status akses dicatat terpisah)

Kolom "doi.org" adalah lapis registrasi (301/302 = terdaftar). Kolom "Crossref" adalah lapis metadata (200 dan `status: ok`). Penolakan penerbit (403/202) bukan kegagalan DOI dan tidak dicatat sebagai kegagalan verifikasi.

| # | Penulis pertama | Tahun | Judul | DOI | doi.org | Crossref |
|---|---|---|---|---|---|---|
| 1 | Dragomiretskiy, K. | 2014 | Variational Mode Decomposition | `10.1109/TSP.2013.2288675` | 302 | ok |
| 2 | Huang, N. E. | 1998 | The empirical mode decomposition and the Hilbert spectrum for nonlinear and non-stationary time series analysis | `10.1098/rspa.1998.0193` | 302 | ok |
| 3 | Daubechies, I. | 1988 | Orthonormal bases of compactly supported wavelets | `10.1002/cpa.3160410705` | 302 | ok |
| 4 | Wang, Y. | 2016 | Filter bank property of variational mode decomposition and its applications | `10.1016/j.sigpro.2015.09.041` | 302 | ok |
| 5 | Yan, R. | 2014 | Wavelets for fault diagnosis of rotary machines: A review with applications | `10.1016/j.sigpro.2013.04.015` | 302 | ok |
| 6 | Randall, R. B. | 2011 | Rolling element bearing diagnostics, a tutorial | `10.1016/j.ymssp.2010.07.017` | 302 | ok |
| 7 | Smith, W. A. | 2015 | Rolling element bearing diagnostics using the Case Western Reserve University data: A benchmark study | `10.1016/j.ymssp.2015.04.021` | 302 | ok |
| 8 | Li, L. | 2023 | Research on Rolling Bearing Fault Diagnosis Based on Variational Modal Decomposition Parameter Optimization and an Improved Support Vector Machine | `10.3390/electronics12061290` | 302 | ok |
| 9 | Gai, J. | 2020 | An integrated method based on hybrid grey wolf optimizer improved variational mode decomposition and deep neural network for fault diagnosis of rolling bearing | `10.1016/j.measurement.2020.107901` | 302 | ok |
| 10 | Li, H. | 2017 | Independence-oriented VMD to identify fault feature for wheel set bearing fault diagnosis of high speed locomotive | `10.1016/j.ymssp.2016.08.042` | 302 | ok |
| 11 | Cortes, C. | 1995 | Support-vector networks | `10.1007/BF00994018` | 302 | ok |
| 12 | Sakoe, H. | 1978 | Dynamic programming algorithm optimization for spoken word recognition | `10.1109/TASSP.1978.1163055` | 302 | ok |
| 13 | Ratanamahatana, C. A. | 2004 | Making Time-series Classification More Accurate Using Learned Constraints | `10.1137/1.9781611972740.2` | 302 | ok |
| 14 | Xi, X. | 2006 | Fast time series classification using numerosity reduction | `10.1145/1143844.1143974` | 302 | ok |
| 15 | Yeh, C.-C. M. | 2016 | Matrix Profile I: All Pairs Similarity Joins for Time Series | `10.1109/ICDM.2016.0179` | 302 | ok |
| 16 | Mirjalili, S. | 2014 | Grey Wolf Optimizer | `10.1016/j.advengsoft.2013.12.007` | 302 | ok |
| 17 | Mirjalili, S. | 2016 | The Whale Optimization Algorithm | `10.1016/j.advengsoft.2016.01.008` | 302 | ok |
| 18 | Singh, N. | 2018 | A New Hybrid Whale Optimizer Algorithm with Mean Strategy of Grey Wolf Optimizer for Global Optimization | `10.3390/mca23010014` | 302 | ok |
| 19 | Reckmann, H. | 2010 | MWD Failure Rates Due to Drilling Dynamics | `10.2118/127413-MS` | 302 | ok |

Rujukan yang dinyatakan **salah dan tidak dipakai**: `10.1007/978-3-540-30075-5_46` dilabeli "Ratanamahatana & Keogh 2004 (DTW constraints)" pada berkas verifikasi lama, padahal Crossref mengembalikan makalah basis data Bellatreche 2004. Rujukan `10.1098/rsta.2010.0331` dilabeli "Randall & Antoni 2011" pada berkas yang sama, padahal Crossref mengembalikan Ellis 2011 "Anthropogenic transformation of the terrestrial biosphere". Keduanya diganti nomor 6 dan 13 di tabel ini.

## 7. Ringkasan 5 baris

1. VMD, EMD, dan wavelet tidak layak pada data D0 karena laju sampel tertinggi 0,3333 Hz memberi Nyquist 0,1667 Hz, sementara pita diagnostik bantalan berada orde ratusan Hz ke atas; 95,86% daya VIBLAT F-15_S bahkan berada di bawah 0,05 Hz.
2. Pemilihan K pada VMD tidak bisa dipertanggungjawabkan dari data ini: sapuan alpha 500/2000/5000 dan K 2..6 menghasilkan jarak antar pusat mode 1,27e-09 sampai 6,45e-06 Hz, dan 75 dari 105 percobaan gagal dengan `zero-size array`.
3. SVM murah dan layak sebagai pembanding pada fitur tabular (7,99 s RBF, 0,05 s linear, median AUC 0,8245 pada satu split tanpa standardisasi), kNN-DTW ditolak karena biaya 134 sampai 137.374 jam per klasifikasi penuh, matrix profile layak sebagai pengganti DTW untuk motif.
4. Hibrida VMD+SVM, VMD+GWO-SVM, dan WOA+GWO semuanya bertumpu pada langkah pertama yang sudah runtuh, dan titik overfitting utamanya adalah penyapuan K/alpha serta optimasi berulang pada skor validasi yang sama.
5. Skor kesesuaian dekomposisi 0 untuk vib, ssi, shk, dan tool_wear; yang diusulkan hanya SVM sebagai pembanding murah (vib, tool_wear) dan matrix profile untuk pencarian motif, dengan syarat akuisisi data getaran ber-laju kHz lebih dulu.

## 8. Belum terverifikasi / batas

1. **Penyebab teknis 75 kegagalan VMD** (`zero-size array to reduction operation minimum`) belum didiagnosis per kanal. Angka 75/105 terukur, sebabnya belum.
2. **Skrip penghasil `m3_decomp.json` tidak ditemukan di workspace** dan tidak ada di `scratch/rnd_r3/`. Angka dari berkas itu dipakai karena keluarannya eksplisit (kunci, nilai, timestamp 2026-10-27T04:52:02), tetapi belum bisa dijalankan ulang baris per baris. Salinan bukti untuk audit disimpan di `scratch/rnd_r3/` (`m3_decomp.json`, `m4_kanal_konstan.json`, `m1_signal_inventory.json`, berkas `m2*.json`), dan skrip verifikasi DOI (`verify_doi_r3.sh`, `verify_doi_r3b.sh`, `verify_doi_r3c.sh` serta keluaran `doi_verify_r3.tsv`, `doi_verify_r3c.tsv`) disalin ke folder yang sama dan bisa dijalankan ulang.
3. **Efek standardisasi pada SVM** hanya satu pembagian tanpa pengulangan seed dan tanpa interval kepercayaan, jadi arah selisih 0,0653 belum bisa diklaim sebagai sifat umum.
4. **Normalisasi keluaran wavelet dan EMD** tidak konsisten (jumlah fraksi energi 1,192 dan 2,45; ada pita di atas Nyquist), sehingga angka energi pita hanya dipakai sebagai indikasi relatif.
5. **Ambang laju sampel untuk diagnostik bantalan** tidak dinyatakan sebagai angka pasti di dokumen ini, karena angka itu bergantung pada geometri bantalan, putaran, dan orde yang dicari. Yang dipakai hanya arah syarat (Nyquist di atas pita yang dicari) dan bukti bahwa 0,1667 Hz jauh di bawahnya.
6. **Kelas sumber untuk tabel jendela**: nilai `n_segmen`, `segmen_terpanjang_sampel`, dan jumlah jendela berasal dari satu skrip yang tidak tersedia, jadi statusnya TERUKUR-SATU-JALUR, bukan TERVERIFIKASI-DUA-JALUR. Nilai laju sampel dan jumlah sampel per kanal cocok dengan D0 (`docs/RND_D0_DATA_FEASIBILITY.md` §2) yang diukur skrip lain, sehingga dua jalur itu sepakat.
7. **Belum diuji**: apakah matrix profile pada kanal `VIBLAT_RT` benar-benar menemukan motif yang berguna. Biaya sudah terukur, manfaat belum.
