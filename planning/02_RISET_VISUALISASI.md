# RISET VISUALISASI: PENYAJIAN TIAP JENIS KELUARAN

Kartu: `t_d597c132` (RISET-VIS). Disusun 2026-10-31. Lingkup: bukti terbuka tentang visual lazim untuk tiap jenis keluaran sistem pendukung keputusan, supaya saran penyajian tidak dikarang.

## 0. Ringkasan

Enam belas sumber dibuka dan dibaca. Pola yang berulang di seluruh sumber:

1. Angka tunggal tanpa sebaran/skala terbaca sebagai kepastian (LV5, LV1).
2. Yang menentukan pilihan visual adalah pertanyaan yang harus dijawab pembaca, bukan estetika (LV13, LV6).
3. Untuk pekerjaan berurutan, umur item lebih informatif daripada jumlah item (LV14).
4. Ketidaksepakatan antar model/metode adalah informasi, bukan gangguan yang harus diringkas jadi satu label (LV15).
5. Peringkat akurasi kanal visual: panjang dan posisi 2D mengalahkan luas/area (LV7).
6. Sumbu ganda dan sumbu terpotong adalah dua sumber salah baca yang paling sering dibahas sumber (LV8).

Setelah katalog fitur selesai, sepuluh jenis keluaran di bagian 3 dipetakan ke kode fitur katalog (KEP, MNT, DAT, CMP, LIN), dan kode sumber literatur diseragamkan menjadi LV1 sampai LV16 mengikuti katalog. Bukti pemeriksaan ada di bagian 1.4.

## 1. Bukti kerja riset

### 1.1 Masukan yang tersedia saat riset dijalankan

Perintah yang dijalankan dan keluarannya:

```
$ ls -la '/mnt/d/Capstone 1(v2)/planning/'
total 0
drwxrwxrwx 1 neonti neonti 4096 Oct 31 16:03 .
drwxrwxrwx 1 neonti neonti 4096 Oct 31 16:03 ..
```

Keluaran di atas menunjukkan folder `planning/` kosong, jadi `planning/01_KATALOG_FITUR.md` tidak ada pada saat riset ini berjalan. Konsekuensinya: daftar jenis keluaran diambil dari badan kartu ini, bukan dari katalog. Sepuluh jenis yang dipetakan: skor keyakinan, kalibrasi, antrean kerja, ketidaksepakatan model, konsensus, jam henti, tren waktu, sebaran, matriks konflik, linimasa keputusan.

Catatan waktu: pemeriksaan di atas terjadi pukul 16:03. Keadaan berubah setelah itu, karena katalog fitur selesai belakangan. Bagian 1.4 memuat pemeriksaan ulang, dan bagian 3 serta 4 sudah memakai nama dan kode fitur dari katalog.

### 1.2 Sumber yang dibuka, dengan ukuran byte nyata

Ukuran byte di bawah adalah byte respons yang benar-benar diterima (`curl -4 -sSL -o file -w '%{http_code}'`), bukan perkiraan. Kolom "karakter bersih" adalah panjang teks hasil ekstraksi yang dibaca.

| Kode | Judul | Penerbit | Byte | Karakter bersih | Status |
|---|---|---|---:|---:|---|
| LV1 | 1.16. Probability calibration | scikit-learn docs | 72.417 | 20.116 | terbuka |
| LV2 | What is a Pareto Chart? Analysis and Diagram | ASQ | 5.658 (403 ke curl) | 20.779 | terbuka via pembaca halaman, curl ditolak 403 |
| LV3 | 2 Time series graphics (Forecasting: Principles and Practice) | OTexts, Hyndman dan Athanasopoulos | 153.032 | 47.330 | terbuka |
| LV4 | Data Tables: Four Major User Tasks | Nielsen Norman Group | 125.715 | 17.057 | terbuka |
| LV5 | When (ish) is My Bus? User-centered Visualizations of Uncertainty | CHI 2016, Kay, Kola, Hullman, Munson | 1.842.246 (PDF) | 64.184 | terbuka |
| LV6 | Financial Times Visual Vocabulary (README) | Financial Times Visual Journalism | 22.912 | 22.702 | terbuka |
| LV7 | Dashboards: Making Charts and Graphs Easier to Understand | Nielsen Norman Group | 131.399 | 21.015 | terbuka |
| LV8 | Why not to use two axes, and what to use instead | Datawrapper | 727.998 | 18.714 | terbuka |
| LV9 | Evaluate the performance of a classifier with Confusion Matrix | scikit-learn docs | 108.371 | 7.560 | terbuka |
| LV10 | FAQ (Polis) | The Computational Democracy Project | 60.926 | 8.932 | terbuka |
| LV11 | Postmortem Culture: Learning from Failure | Google SRE Book | 55.113 | 18.710 | terbuka |
| LV12 | Visualizing distributions: Histograms and density plots | Claus Wilke, Fundamentals of Data Visualization | 51.754 | 16.905 | terbuka |
| LV13 | Choosing Chart Types: Consider Context | Nielsen Norman Group | 132.662 | 20.575 | terbuka |
| LV14 | Queue Aging Report for Operations Teams | Workhint | 152.266 | 10.146 | terbuka |
| LV15 | The Disagreement Problem in Explainable Machine Learning | TMLR, arXiv 2202.01602 | 359.099 | 102.718 | terbuka |
| LV16 | Postmortems at Loon: a guiding force for rapid development | Google Cloud Blog | 20.360 (teks tersimpan) | 20.320 | terbuka |

Total: 16 sumber berbeda, semuanya bisa dibuka, URL lengkap di bagian 9.

Kode sumber di dokumen ini semula ditulis S1 sampai S16. Setelah katalog fitur terbit, kode itu diubah menjadi LV1 sampai LV16 karena katalog memakai awalan LV untuk rujukan visual dan memakai [S1] untuk berkas `docs/RND_S1_SEED_ROBUSTNESS.md` (katalog baris 112 sampai 114). Satu kode kini berarti satu sumber di seluruh rangkaian dokumen.

### 1.3 Sumber yang dicoba tetapi gagal dibuka (tidak dipakai sebagai bukti)

| URL | Keluaran nyata | Status |
|---|---|---|
| techrxiv.org/doi/pdf/10.36227/techrxiv.173386520.03447635/v2 | "Just a moment..." halaman verifikasi bot | tidak dipakai |
| docs.nrel.gov/docs/fy24osti/90550.pdf | "Blocked: URL targets a private or internal network address" | tidak dipakai |
| vis.stanford.edu/papers/ensemblematrix | "9router /web/fetch HTTP 422" | tidak dipakai |

Ketiganya disebut supaya jejak riset bisa diperiksa, dan tidak satu pun kalimatnya dipakai di dokumen ini.

### 1.4 Keadaan masukan setelah katalog tersedia (pemeriksaan ulang)

Katalog fitur selesai setelah riset ini berjalan. Berkasnya sekarang ada, sehingga penyelarasan bisa dikerjakan. Perintah yang dijalankan dan keluarannya:

```
$ stat -c '%n bytes=%s' planning/01_KATALOG_FITUR.md
planning/01_KATALOG_FITUR.md bytes=166662
$ wc -l planning/01_KATALOG_FITUR.md
2780 planning/01_KATALOG_FITUR.md
$ grep -c '^### ' planning/01_KATALOG_FITUR.md
48
$ grep -cE '^\*\*Saran penyajian' planning/01_KATALOG_FITUR.md
48
$ grep -c -i 'konsensus' planning/01_KATALOG_FITUR.md ; echo "rc=$?"
0
rc=1
$ grep -c -i 'konflik' planning/01_KATALOG_FITUR.md ; echo "rc=$?"
0
rc=1
$ grep -oE '\[LV[0-9]+\]' planning/01_KATALOG_FITUR.md | sort -u | tr '\n' ' '
[LV11] [LV12] [LV13] [LV14] [LV15] [LV16] [LV1] [LV2] [LV3] [LV4] [LV5] [LV6] [LV7] [LV8] [LV9]
```

Empat akibat yang dipakai dokumen ini:

1. Katalog memuat 48 fitur dan 48 butir "Saran penyajian", jadi setiap jenis keluaran di bagian 3 punya padanan kode fitur. Kolom kode fitur ditambahkan ke Tabel A dan Tabel B.
2. Katalog merujuk dokumen ini sebagai [VR] dan memakai kode [LV1] sampai [LV16] (katalog baris 112 sampai 114). Karena itu kode sumber literatur di dokumen ini diseragamkan menjadi LV1 sampai LV16, supaya satu kode berarti satu sumber.
3. Kata "konsensus" tidak muncul satu kali pun di katalog (0 baris, kode keluar 1), jadi jenis keluaran konsensus belum punya fitur. Bagian 3 menandainya terbuka, bukan mengarang kode.
4. Kata "konflik" juga tidak muncul (0 baris, kode keluar 1). Jenis keluaran matriks konflik dipetakan ke fitur bermatriks yang benar-benar ada, dan definisinya tetap ditandai sebagai asumsi di bagian 5.9.

## 2. Kepatuhan kerangka wajib

| Butir kerangka | Cara dipenuhi |
|---|---|
| 1. Alarm otomatis bukan tujuan | Seluruh rekomendasi berbentuk tampilan pendukung keputusan (skor, umur antrean, ketidaksepakatan), tanpa satu pun saran alarm otomatis. |
| 2. Setiap angka bersumber | Angka proyek memakai berkas dan baris (bagian 5.6, 5.3). Angka literatur memakai kode sumber LV1 sampai LV16, sama dengan kode yang dipakai katalog (katalog baris 112 sampai 114). |
| 3. Tidak mengklaim tanpa bukti | Keluaran perintah `ls` dan byte tiap sumber ditempel di bagian 1. |
| 4. Kekurangan data jadi fitur | Bagian 8 menuliskan syarat yang dibutuhkan, tanpa kalimat penutup yang menyerah. |
| 5. Pengguna, momen, masukan, keluaran, status bukti | Tabel B (bagian 4) memuat kelima kolom untuk tiap jenis keluaran, ditambah kolom kode fitur katalog. |
| 6. Tidak menutup dengan kata menyerah | Ditutup oleh enam rekomendasi (bagian 7) dan daftar syarat (bagian 8). |
| 7. Hanya .md di planning/ | Satu berkas keluaran: `planning/02_RISET_VISUALISASI.md`. Tidak ada .py, .html, .json, .csv yang dibuat sebagai deliverable. |
| 8. Tanpa tanda pisah panjang | Diverifikasi dengan `grep -c` di bagian 10. |

## 3. Peta jenis keluaran ke visual lazim (Tabel A)

| No | Jenis keluaran | Kode fitur katalog (baris, baris saran penyajian) | Visual lazim | Alasan | Sumber |
|---|---|---|---|---|---|
| 1 | Skor keyakinan | KEP-02 (288, 332), KEP-03 (365, 406) | Titik-titik kuantil (quantile dotplot) atau interval, bukan satu angka | Titik-titik kuantil menurunkan variasi taksiran peluang sekitar 1,15 kali dibanding density plot, dan pembaca bisa menghitung titik untuk mendapat peluang | LV5 |
| 2 | Kalibrasi | KEP-04 (434, 473), INS-01 (2358, 2400) | Kurva kalibrasi (reliability diagram) dengan garis diagonal acuan | Sumbu x rata-rata peluang prediksi per bin, sumbu y fraksi positif nyata, jadi penyimpangan dari diagonal terbaca langsung | LV1 |
| 3 | Antrean kerja | MNT-01 (871, 912), DAT-06 (1543, 1567, di sana jumlah antrean tampil sebagai batang berurut, bukan tabel) | Tabel terurut peringkat dengan kolom umur (aging) dan status SLA | Umur item lebih informatif daripada satu angka backlog, dan tabel mendukung tugas cari, banding, dan aksi | LV14, LV4 |
| 4 | Ketidaksepakatan model | KEP-08 (673, 717), CMP-07 (1982, 2037) | Panel per item yang menampilkan putusan tiap head, atau matriks kesepakatan | Metode penjelas terbukti sering tidak sepakat, dan menyembunyikan itu membuat keputusan berisiko dibaca sebagai pasti | LV15 |
| 5 | Konsensus | belum ada di katalog: kata konsensus 0 baris; bentuk terdekat KEP-08 (717) | Peta kelompok opini (sebaran titik) plus batang setuju/tidak setuju per pernyataan | Setelah kelompok opini muncul, yang dicari adalah pernyataan yang sama-sama diterima atau ditolak semua kelompok | LV10 |
| 6 | Jam henti | KEP-10 (796, 838) | Diagram Pareto: batang terurut menurun plus garis persentase kumulatif | Dipakai saat ada banyak sebab dan tujuannya memusatkan perhatian pada yang paling besar, batang terpanjang di kiri | LV2 |
| 7 | Tren waktu | MNT-07 (1186, 1215), MNT-06 (1139, 1168), MNT-08 (1233, 1259) | Plot garis terhadap sumbu waktu, boleh ditambah plot musiman dan ACF | Langkah pertama analisis data adalah memplot data, karena pola dan kejadian luar biasa terlihat di grafik | LV3 |
| 8 | Sebaran | CMP-01 (1764, 1787), MNT-04 (1051, 1081) | Histogram untuk satu variabel, density (KDE) untuk banyak distribusi sekaligus | Bentuk histogram sangat bergantung lebar bin, dan density lebih baik saat beberapa distribusi dibandingkan | LV12 |
| 9 | Matriks konflik | belum ada namanya di katalog: kata konflik 0 baris; bentuk matriksnya di DAT-05 (1507, 1530), DAT-07 (1582, 1606), CMP-07 (2037) | Heatmap matriks bernilai, dengan normalisasi per baris bila kelas tidak seimbang | Diagonal berarti benar, luar diagonal berarti salah label, dan normalisasi perlu supaya ketidakseimbangan kelas terbaca | LV9 |
| 10 | Linimasa keputusan | LIN-01 (2071, 2097), LIN-02 (2112, 2135), LIN-07 (2309, 2335) | Linimasa vertikal berurut waktu: waktu, aktor, keputusan, akibat | Postmortem standar memuat linimasa kejadian, dampak, akar masalah, dan tindak lanjut dalam satu urutan waktu | LV16, LV11 |

Jumlah baris Tabel A: 10.

## 4. Lima field wajib per jenis keluaran (Tabel B), ditambah kolom kode fitur katalog

| Jenis keluaran | Kode fitur | Pengguna | Momen pakai | Masukan | Keluaran | Status bukti |
|---|---|---|---|---|---|---|
| Skor keyakinan | KEP-02, KEP-03 | Operator drilling, pengawas shift | Saat menimbang apakah perlu tindakan sebelum indikasi memburuk | Keluaran model per jendela waktu (skor, ambang, riwayat) | Sebaran skor plus peluang kejadian, bukan satu angka | Sumber primer (LV5). Katalog: KEP-02 siap sebagian, KEP-03 siap sekarang (katalog baris 137 dan 138) |
| Kalibrasi | KEP-04, INS-01 | Penilai model, auditor internal | Saat memutuskan apakah skor boleh dibaca sebagai frekuensi | Pasangan skor prediksi dan label nyata per fold | Kurva kalibrasi per engine plus jumlah bin | Sumber primer (LV1). Katalog: KEP-04 masih rancangan, INS-01 siap sebagian (katalog baris 139 dan 179) |
| Antrean kerja | MNT-01, DAT-06 | Engineer pemeliharaan, pengawas | Awal shift, saat membagi tinjauan | Daftar item tinjauan, stempel waktu, status | Tabel terurut umur dengan status | Sumber sekunder (LV14, LV4). Katalog: MNT-01 dan DAT-06 siap sekarang untuk komponennya; skema pencatatan umur belum ada (katalog baris 926) |
| Ketidaksepakatan model | KEP-08, CMP-07 | Penilai model, pengawas | Saat dua head memberi putusan berbeda pada kejadian sama | Putusan per head pada timestamp sama | Matriks atau panel kesepakatan per kejadian | Sumber primer (LV15). Katalog: KEP-08 dan CMP-07 siap sebagian; deret per menit belum tersimpan (katalog baris 693) |
| Konsensus | belum ada | Tim lintas disiplin | Saat menyimpulkan satu interpretasi bersama | Suara atau putusan tiap pihak per pernyataan | Peta kelompok plus batang dukungan | Sumber primer (LV10). Katalog tidak memuat fitur ini (0 baris), jadi status buktinya terbuka dan dicatat di bagian 8 |
| Jam henti | KEP-10 | Manajer pemeliharaan, perencana | Saat menyusun prioritas perbaikan | Jam aktivitas DDR per kategori | Pareto jam henti per kategori | Sumber primer (LV2) plus angka proyek terverifikasi. Katalog: KEP-10 siap sebagian (katalog baris 145) |
| Tren waktu | MNT-07, MNT-06, MNT-08 | Semua peran teknis | Saat memeriksa apakah kondisi membaik atau memburuk | Deret waktu per kanal dan per engine | Garis waktu dengan penanda kejadian | Sumber primer (LV3). Katalog: ketiganya siap sekarang (katalog baris 151 sampai 153) |
| Sebaran | CMP-01, MNT-04 | Penilai model, statistikawan | Saat memeriksa apakah satu rata-rata menyembunyikan dua populasi | Nilai metrik per fold atau per sumur | Histogram atau density, dengan catatan lebar bin | Sumber sekunder (LV12). Katalog: CMP-01 dan MNT-04 siap sekarang (katalog baris 149 dan 165) |
| Matriks konflik | belum ada namanya; bentuknya di DAT-05, DAT-07, CMP-07 | Penilai model, pengawas | Saat memeriksa pola salah putus antara dua sumber putusan | Dua set label pada unit yang sama | Heatmap bernilai plus versi ternormalisasi | Sumber primer (LV9). Katalog: ketiga fitur itu siap sekarang atau siap sebagian, tetapi istilahnya belum ada (katalog baris 159, 161, 171) |
| Linimasa keputusan | LIN-01, LIN-02, LIN-07 | Pengawas, auditor | Saat meninjau ulang satu shift atau satu kejadian | Catatan waktu, aktor, keputusan, akibat | Linimasa vertikal yang bisa disaring per shift | Sumber primer (LV16, LV11). Katalog: LIN-02 siap sekarang, LIN-01 dan LIN-07 siap sebagian (katalog baris 172 sampai 178) |

Jumlah baris Tabel B: 10.

## 5. Rincian per jenis keluaran

Setiap butir di bawah memakai kode fitur katalog yang sama dengan Tabel A, supaya satu jenis keluaran bisa dilacak ke satu fitur.

### 5.1 Skor keyakinan

Visual lazim: kumpulan titik kuantil untuk hasil yang mungkin, atau batang interval, disertai label peluang yang bisa dihitung pembaca.

Kalimat inti sumber: "most visualizations of predictions present the data as if it were true" dan "quantile dotplots reduce the variance of probabilistic estimates by ~1.15 times compared to density plots" (LV5, CHI 2016).

Alasan terapan: pada layar kecil dan waktu singkat, pembaca butuh jumlah hasil yang bisa dihitung, bukan kurva yang harus ditafsirkan. Untuk sistem ini, satu angka keyakinan per kejadian sebaiknya selalu ditemani sebaran skor pada jendela waktu yang sama.

### 5.2 Kalibrasi

Visual lazim: reliability diagram. Sumbu x rata-rata peluang prediksi per bin, sumbu y fraksi positif nyata, garis diagonal sebagai acuan sempurna.

Kalimat inti sumber: "a well calibrated (binary) classifier should classify the samples such that among the samples to which it gave a predict_proba value close to, say, 0.8, approximately 80% actually belong to the positive class" (LV1).

Peringatan penting dari sumber yang sama: Brier dan log loss mencampur kalibrasi, daya pisah, dan keacakan data, sehingga "a lower Brier loss does not necessarily mean a better calibrated model" (LV1). Artinya kurva kalibrasi tidak boleh diganti skor tunggal.

### 5.3 Antrean kerja

Visual lazim: tabel terurut dengan kolom peringkat, umur, status SLA, pemilik, dan aksi berikutnya. Bucket umur contoh dari sumber: 0 sampai 2 hari, 3 sampai 7 hari, 8 sampai 15 hari, lebih dari 30 hari (LV14).

Kalimat inti sumber: "age distribution matters more than a single open count" (LV14). Untuk sisi tabel: "The (default) first column should be a human-readable record identifier instead of a 'mystery meat' automatically generated ID" (LV4).

Angka proyek yang relevan (beban tinjauan per shift 8 jam): vib 17, hyd rule_display 19, hyd hybrid 6, shk 3, stuck 3, tool_wear 1. Sumber: `docs/RND_ENGINE_S6_INTEGRATION.md` baris 31 sampai 43. Angka ini adalah volume antrean, jadi visual antrean harus sanggup menampung puluhan baris per shift, bukan lima kartu.

### 5.4 Ketidaksepakatan model

Visual lazim: matriks kesepakatan antar head (baris dan kolom berisi head, sel berisi tingkat kesepakatan), atau panel per kejadian yang menampilkan putusan tiap head berdampingan. Warna hanya pelengkap, angka di sel tetap ditulis.

Kalimat inti sumber: "state-of-the-art explanation methods often disagree in terms of the explanations they output" dan "practitioners may be relying on misleading explanations when making consequential decisions" (LV15).

Alasan terapan: proyek ini sudah punya beberapa head setara per engine (hyd misalnya tiga head setara dengan satu head utama). Menampilkan ketidaksepakatan membuat pembaca tahu kapan keputusan berada di wilayah abu-abu, bukan disuguhi satu label seolah disepakati semua head.

### 5.5 Konsensus

Visual lazim: peta kelompok opini (sebaran titik dua dimensi) ditambah batang setuju, tidak setuju, dan abstain per pernyataan, dipisah per kelompok.

Kalimat inti sumber: "as the Algorithms find opinion groups and surface differences, one can then consider what they have in common, and which statements were supported or rejected commonly by all opinion groups" (LV10).

Alasan terapan: konsensus bukan rata-rata skor. Yang ditampilkan adalah pernyataan yang lolos di semua kelompok, sehingga satu angka agregat tidak cukup.

### 5.6 Jam henti

Visual lazim: diagram Pareto, batang kategori terurut dari terbesar ke terkecil, ditambah garis persentase kumulatif.

Kalimat inti sumber: dipakai "When there are many problems or causes and you want to focus on the most significant", dan batang "arranged with longest bars on the left and the shortest to the right" (LV2).

Angka proyek yang sudah ada, sumber `docs/RND_ENGINE_S6_INTEGRATION.md` baris 19 sampai 27, data dari `data/volve/ddr.parquet` kolom `activity`:

| Kategori | Jam |
|---|---:|
| Total jam tercatat | 39.397,986 |
| Henti karena equipment failure | 2.739,667 |
| Interruption other | 2.680,917 |
| Interruption waiting on weather | 1.925,5 |
| Henti karena stuck equipment | 212,0 |
| Henti karena circulation loss | 195,0 |

Dengan angka ini, Pareto langsung memberi urutan prioritas perbaikan tanpa perlu data baru. Jumlah record aktivitas: 23.447 (baris 21 berkas yang sama).

### 5.7 Tren waktu

Visual lazim: plot garis dengan sumbu waktu eksplisit, ditambah plot musiman, plot subseri, dan ACF bila pola berulang dicurigai.

Kalimat inti sumber: "The first thing to do in any data analysis task is to plot the data. Graphs enable many features of the data to be visualised, including patterns, unusual observations, changes over time, and relationships between variables" (LV3).

Alasan terapan: tren waktu adalah kanal untuk menjawab "membaik atau memburuk", jadi satu-satunya sumbu y harus satuan yang sama. Bila dua satuan harus tampil bersamaan, lihat larangan di bagian 6 butir 1.

### 5.8 Sebaran

Visual lazim: histogram untuk satu variabel, density (KDE) saat beberapa distribusi dibandingkan, dan selalu mencoba beberapa lebar bin sebelum menyimpulkan bentuk.

Kalimat inti sumber: "if the bin width is too small, then the histogram becomes overly peaky and visually busy and the main trends in the data may be obscured. On the other hand, if the bin width is too large, then smaller features in the distribution of the data, such as the dip around age 10, may disappear" dan "To visualize several distributions at once, kernel density plots will generally work better than histograms" (LV12).

### 5.9 Matriks konflik

Visual lazim: heatmap matriks dengan angka di dalam sel, satu versi hitungan mentah dan satu versi ternormalisasi per baris.

Kalimat inti sumber: "The diagonal elements represent the number of points for which the predicted label is equal to the true label, while off-diagonal elements are those that are mislabeled by the classifier" dan normalisasi "can be interesting in case of class imbalance to have a more visual interpretation of which class is being misclassified" (LV9).

Definisi operasional yang dipakai dokumen ini, dinyatakan terbuka sebagai asumsi: matriks konflik berarti matriks antara dua sumber putusan pada unit waktu yang sama (misalnya putusan engine A versus engine B, atau putusan engine versus kejadian nyata). Istilah ini tidak ditemukan di dokumen proyek saat pencarian dilakukan, jadi definisinya perlu dikonfirmasi pemilik produk.

### 5.10 Linimasa keputusan

Visual lazim: linimasa vertikal berurut waktu dengan kolom waktu, aktor, keputusan, dan akibat. Setiap butir bisa ditautkan ke grafik metrik pada jam yang sama.

Kalimat inti sumber: "The postmortem usually includes a timeline of what happened, the solutions implemented, the incident's impact, the investigation into root causes" (LV16), dan postmortem didefinisikan sebagai "a written record of an incident, its impact, the actions taken to mitigate or resolve it, the root cause(s), and the follow-up actions" (LV11).

## 6. Visual yang harus dihindari

| Visual | Alasan | Sumber |
|---|---|---|
| Dua sumbu Y pada satu grafik | Skala kedua sumbu sewenang-wenang, dan sumber menyebut grafik dua sumbu "make it hard for most people to intuitively make right statements about two data series". Suntingan sumber 2026 menambahkan pengecualian: untuk audiens terlatih (misalnya jasa keuangan) dua sumbu bisa jadi pilihan terbaik, tetapi untuk audiens umum tetap disarankan alternatif | LV8 |
| Sumbu Y terpotong pada grafik batang | Panjang batang menyiratkan besaran dari nol, sehingga sumbu terpotong membesarkan perbedaan kecil. Sumber menyebut skala dua sumbu sewenang-wenang dan bisa dipakai menyesatkan, sehingga disiplin skala harus eksplisit | LV8 |
| Satu angka keyakinan tanpa sebaran atau interval | Prediksi titik dibaca sebagai kepastian, dan kasus bus dalam sumber adalah contoh kegagalan keputusan yang diakibatkannya | LV5 |
| Skor tunggal (misalnya Brier) sebagai bukti kalibrasi | Skor itu mencampur kalibrasi, daya pisah, dan keacakan data, sehingga skor rendah tidak otomatis berarti terkalibrasi baik | LV1 |
| Gauge, dial, atau cakram untuk peluang | Luas dan sudut bukan kanal yang diproses cepat; sumber menyarankan panjang dan posisi 2D untuk informasi kuantitatif | LV7 |
| Matriks konflik berisi hitungan mentah saja pada data tidak seimbang | Tanpa normalisasi per baris, kelas kecil terlihat benar padahal salah, karena sel besarnya didominasi kelas mayoritas | LV9 |
| Histogram dengan lebar bin bawaan tanpa uji lebar lain | Bentuk histogram bergantung lebar bin, fitur kecil bisa hilang atau data terlihat lebih ramai daripada kenyataannya | LV12 |
| Satu angka backlog untuk antrean kerja | Jumlah terbuka menyembunyikan bentuk pekerjaan; 400 item bisa sehat dan 80 item bisa bermasalah, tergantung umurnya | LV14 |
| Tabel tanpa pengenal baris yang terbaca manusia | Kolom pertama berisi ID otomatis menyulitkan pemindaian dan pencarian baris | LV4 |

Jumlah baris tabel larangan: 9.

Katalog menambahkan dua larangan bentuk yang tidak diambil dari sumber web mana pun, jadi dicatat terpisah dan bukan bagian tabel di atas: grafik radar untuk perbandingan kategori (katalog baris 1825 dan 2335) dan diagram alir untuk riwayat keputusan (katalog baris 2097). Keduanya berasal dari dokumen proyek, bukan dari sumber literatur, karena itu tidak dihitung dalam sembilan baris di atas.

## 7. Enam rekomendasi terkuat

1. Skor keyakinan ditampilkan sebagai sebaran hasil (titik kuantil atau batang interval) di dalam kartu KEP-02, bukan satu angka besar, karena titik tunggal terbaca sebagai kepastian dan varian titik kuantil terbukti lebih presisi (LV5).
2. Setiap engine yang memakai skor punya reliability diagram sendiri di KEP-04, lengkap dengan jumlah bin dan garis diagonal, karena hanya diagram itu yang menunjukkan apakah skor boleh dibaca sebagai frekuensi (LV1).
3. Antrean kerja disajikan sebagai tabel terurut umur di MNT-01 dengan status SLA dan aksi berikutnya, memakai beban tinjauan per shift yang sudah terhitung (vib 17, hyd 19, shk 3, stuck 3 di `docs/RND_ENGINE_S6_INTEGRATION.md` baris 31 sampai 43), bukan satu angka backlog (LV14, LV4).
4. Ketidaksepakatan antar head ditampilkan di KEP-08 sebagai matriks bernilai atau panel per kejadian, tidak diringkas menjadi satu label, karena ketidaksepakatan yang disembunyikan membuat keputusan berisiko dibaca sebagai kesepakatan (LV15, LV9).
5. Jam henti disajikan sebagai Pareto di KEP-10 memakai angka DDR yang sudah ada (39.397,986 jam tercatat, equipment failure 2.739,667 jam), sehingga prioritas perbaikan terbaca dari data yang sudah dimiliki tanpa pengumpulan baru (LV2, `docs/RND_ENGINE_S6_INTEGRATION.md` baris 21 sampai 27).
6. Satu grafik hanya memakai satu satuan. Bila dua satuan harus tampil, pakai panel bersusun (small multiples) dengan sumbu x sama, atau indekskan keduanya ke nilai awal 100, dan simpan dua sumbu Y hanya untuk audiens yang sudah terlatih membacanya (LV8).

Urutan penerapan mengikuti status katalog, bukan urutan di atas: MNT-01, MNT-07, MNT-08, KEP-03, DAT-06, CMP-01, dan MNT-04 berstatus siap sekarang; KEP-02, KEP-08, KEP-10, dan INS-01 siap sebagian; KEP-04 masih rancangan (katalog baris 137 sampai 179).

## 8. Syarat yang dibutuhkan (bukan penutup menyerah)

| Yang belum ada | Syarat agar bisa dikerjakan |
|---|---|
| Berkas `planning/01_KATALOG_FITUR.md` | Sudah terpenuhi: berkas ada, 166.662 byte, 2.780 baris, 48 fitur (bagian 1.4). Penyelarasan nama dan kode fitur sudah dikerjakan di bagian 3 dan 4. |
| Fitur untuk jenis keluaran konsensus | Satu keputusan pemilik produk: konsensus dihitung dari putusan head (maka KEP-08 cukup diperluas dengan batang dukungan) atau dari suara manusia (maka perlu kanal pengumpulan pendapat dan satu fitur baru di rumpun kepercayaan). Sebelum keputusan itu, jenis ini tetap dipetakan sebagai terbuka. |
| Definisi resmi istilah "matriks konflik" di proyek | Satu paragraf definisi dari pemilik produk: pasangan apa yang dibandingkan (engine lawan engine, atau engine lawan kejadian nyata) dan unit waktunya. Katalog sudah memuat tiga bentuk matriks yang bisa dipakai sebagai acuan: KEP-08 (kesepakatan antar head), DAT-05 (ketersediaan berkas), DAT-07 (label per sumur). |
| Log keputusan berstruktur untuk linimasa | Skema pencatatan disepakati lebih dulu, lalu kolom waktu, aktor, keputusan, dan akibat diisi. Katalog sudah menetapkan kolom waktunya di LIN-01 dengan status siap sebagian (katalog baris 2097). |
| Data biaya per kejadian | KEP-10 sudah menyediakan lima slot kosong berlabel pemilik data (katalog baris 838). Syaratnya: pemilik data mengisi tarif biaya henti, sehingga jam henti bisa diterjemahkan ke rupiah. Angka jamnya sudah tersedia. |
| Data suara pihak untuk konsensus | Diperlukan hanya bila keputusan konsensus memilih jalur suara manusia. Bila memilih jalur putusan head, data yang dibutuhkan sudah ada di keluaran engine. |

## 9. Rujukan lengkap

1. LV1. Probability calibration, scikit-learn. https://scikit-learn.org/stable/modules/calibration.html
2. LV2. What is a Pareto Chart? Analysis and Diagram, ASQ. https://asq.org/quality-resources/pareto
3. LV3. Time series graphics, Forecasting: Principles and Practice, Hyndman dan Athanasopoulos, OTexts. https://otexts.com/fpp3/graphics.html
4. LV4. Data Tables: Four Major User Tasks, Page Laubheimer, Nielsen Norman Group, 2022. https://www.nngroup.com/articles/data-tables
5. LV5. When (ish) is My Bus? User-centered Visualizations of Uncertainty in Everyday, Mobile Predictive Systems, Kay, Kola, Hullman, Munson, CHI 2016. https://www.mjskay.com/papers/chi_2016_uncertain_bus.pdf
6. LV6. Financial Times Visual Vocabulary, Financial Times Visual Journalism Team. https://raw.githubusercontent.com/Financial-Times/chart-doctor/main/visual-vocabulary/README.md
7. LV7. Dashboards: Making Charts and Graphs Easier to Understand, Page Laubheimer, Nielsen Norman Group, 2017. https://www.nngroup.com/articles/dashboards-preattentive
8. LV8. Why not to use two axes, and what to use instead, Lisa Charlotte Muth, Datawrapper, 2018, dengan suntingan Juli 2026. https://www.datawrapper.de/blog/dualaxis
9. LV9. Evaluate the performance of a classifier with Confusion Matrix, scikit-learn. https://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html
10. LV10. FAQ, Polis, The Computational Democracy Project. https://compdemocracy.org/faq
11. LV11. Postmortem Culture: Learning from Failure, Google SRE Book, 2017. https://sre.google/sre-book/postmortem-culture
12. LV12. Visualizing distributions: Histograms and density plots, Claus O. Wilke, Fundamentals of Data Visualization. https://clauswilke.com/dataviz/histograms-density-plots.html
13. LV13. Choosing Chart Types: Consider Context, Kate Moran, Nielsen Norman Group, 2022. https://www.nngroup.com/articles/choosing-chart-types
14. LV14. Queue Aging Report for Operations Teams, Mia Ali, Workhint. https://blog.workhint.com/blog/queue-aging-report-operations-teams
15. LV15. The Disagreement Problem in Explainable Machine Learning: A Practitioner's Perspective, TMLR, arXiv 2202.01602. https://arxiv.org/html/2202.01602v6
16. LV16. Postmortems at Loon: a guiding force for rapid development, Danielle van Dyke dan Giselle Font, Google Cloud Blog. https://cloud.google.com/blog/products/devops-sre/loon-sre-use-postmortems-to-launch-and-iterate

## 10. Verifikasi berkas ini

Perintah dijalankan dari `/mnt/d/Capstone 1(v2)`, sesudah seluruh penyuntingan selesai. Keluarannya ditempel apa adanya:

```
$ stat -c '%s' planning/02_RISET_VISUALISASI.md
32141
$ wc -l < planning/02_RISET_VISUALISASI.md
335
$ grep -c '^|' planning/02_RISET_VISUALISASI.md
84
$ grep -cP '\x{2014}' planning/02_RISET_VISUALISASI.md
0
$ grep -cP '\x{2013}' planning/02_RISET_VISUALISASI.md
0
$ grep -c -i -E 'tidak (bisa|mungkin)|terba(tas)' planning/02_RISET_VISUALISASI.md
0
$ grep -c '^### 5\.' planning/02_RISET_VISUALISASI.md
10
$ grep -oE 'https://[A-Za-z0-9./_?=-]+' planning/02_RISET_VISUALISASI.md | sort -u | wc -l
16
$ sed -n '/^| No | Jenis keluaran/,/^Jumlah baris Tabel A/p' planning/02_RISET_VISUALISASI.md | grep -c '^| [0-9]'
10
$ sed -n '/^| Jenis keluaran | Kode fitur/,/^Jumlah baris Tabel B/p' planning/02_RISET_VISUALISASI.md | grep -c '^| [A-Z]'
11
$ sed -n '/^## 6\. Visual yang harus dihindari/,/^Jumlah baris tabel larangan/p' planning/02_RISET_VISUALISASI.md | grep -c '^|'
11
```

Bacaan keluaran di atas:

1. Baris Tabel B keluar 11 karena baris pertama yang terhitung adalah baris kepala tabel, jadi data sebenarnya 10 baris, sesuai keterangan "Jumlah baris Tabel B: 10".
2. Baris tabel larangan keluar 11 karena hitungan itu memuat baris kepala dan baris pemisah, jadi data sebenarnya 9 baris, sesuai keterangan "Jumlah baris tabel larangan: 9".
3. Hitungan tanda pisah panjang dan pendek keduanya 0, dan tidak ada frasa penutup menyerah.
4. Enam belas URL unik muncul di berkas ini, sama dengan jumlah sumber di bagian 1.2 dan bagian 9.

Catatan kejujuran: angka byte di atas berubah setiap kali bagian ini disunting, karena bagian ini bagian dari berkas yang diukur. Angka final yang dilaporkan di komentar penutup kartu adalah hasil pengukuran terakhir setelah suntingan berhenti, dan selisih beberapa byte terhadap angka di blok ini berasal dari kalimat ini sendiri.
