# BAB I PENDAHULUAN

## 1.1 Latar Belakang Sistem

| | |
|---|---|
| Kartu kanban | `t_6fff319f` (R&D, BAB I 1.1) |
| Tanggal | 25 Oktober 2026 (WIB) |
| Ruang kerja | `/mnt/d/Capstone 1(v2)` |
| Keluaran | `docs/PPT1_BAB1_1.md` (naskah) + `scratch/ppt1/bab1_1_angka.json` (bukti angka) + `scratch/ppt1/bab1_1_hitung.py` (skrip hitung ulang) |
| Mitra | PT Halliburton Indonesia, divisi Sperry Drilling (jalur Magang/MBKM, pedoman 2.8c) |
| Format acuan | Buku Pedoman PPT h.33-36, sub-bab 1.1: deskripsi objek kasus, stakeholder, rich picture, alur produksi, uraian singkat permasalahan; ditambah tuntutan SIMILAR tahap satu (trade-off minimal dua aspek) |
| Status angka dampak | TERUKUR untuk total durasi dan sebaran (kartu P0 `t_0eb03f13`, dihitung ulang di kartu ini). TEMPORER untuk pemetaan per mode FMEA karena kartu D1 `t_c0e851b8` berstatus **blocked** dan belum menghasilkan `docs/PPT1_BUKTI_DAMPAK.md` |

**Riset pendahuluan: `ppt-halliburton`** (beserta `references/ppt1-proposal-build.md` dan `references/pedoman-summary.md`) - format wajib 1.1 adalah lima elemen (objek, stakeholder, rich picture, alur produksi, uraian masalah) plus trade-off SIMILAR tahap satu; peta bahan menunjukkan angka dampak berasal dari `labels_curated_v2.csv`, bukan dari draft Agustus 2026.
**Riset pendahuluan: `verification-mandatory`** - setiap angka dipisah menjadi bukti mentah dan kesimpulan, angka tanpa jejak ditulis sebagai ASUMSI/TEMPORER, dan laporan ditutup dengan daftar yang belum diverifikasi (lihat 1.1.8).
**Riset pendahuluan: `sequentialthinking` (sequ-mcp, empat pikiran)** - urutan pikir: (1) susun struktur 1.1 dari tuntutan pedoman, (2) cek status kartu D1 sebelum memakai angka mode, (3) uji ulang angka durasi dengan instrumen parser yang berbeda, (4) rancang elemen rich picture agar kartu G1 dapat menggambar tanpa menebak.

### 1.1.1 Deskripsi Objek Studi dan Sistem yang Dikaji

Objek kajian proyek ini adalah **PT Halliburton Indonesia, divisi Sperry Drilling**, yaitu penyedia jasa pengeboran yang mengoperasikan instrumentasi lubang bawah (MWD, LWD, dan Rotary Steerable System) serta layanan pemantauan parameter pengeboran bagi operator minyak dan gas. Pengajuan objek melalui jalur Magang/MBKM mengikuti pedoman 2.8c, sehingga permasalahan yang diangkat harus berasal dari proses kerja nyata mitra dan dimiliki oleh seorang pemilik masalah di lapangan [S:draft Sperry `Proposal_PPT_I_SperryDrilling_ML_NPT.docx` l.28; Buku Pedoman PPT 2.8c].

Sistem yang dikaji bukan satu alat, melainkan **rantai keputusan pengeboran**: sensor lubang bawah mengirim data fisis ke permukaan, sistem permukaan menampilkan dan menyimpan data tersebut, driller dan drilling engineer membaca tampilan itu, lalu memutuskan apakah pengeboran dilanjutkan, parameter diubah, atau rangkaian ditarik. Mutu rantai ini ditentukan oleh dua hal yang saling bertukar: kelengkapan pengukuran (berapa kanal yang benar-benar terisi) dan kecepatan keputusan (berapa menit antara gejala terbaca dan tindakan diambil).

Basis data yang dipakai proyek berasal dari **lapangan Volve (Equinor, lisensi CC BY-NC-SA 4.0)** karena data operasi mitra tidak dapat dibuka [S:V3_DATA_ACQUISITION_INVENTORY.md baris lisensi]. Inventaris yang benar-benar ada di disk berisi **13 himpunan data** [H:inventaris.baris_tabel, rincian per himpunan di docs/V10_D1_BAB_DATA.md §3.1], dengan tulang punggung berupa **7.080.457 baris log pengeboran WITSML hasil parse** dari 8 berkas sumur [L:B12] dan matriks latih **292.954 baris** pada **6 dataset siap pakai** [L:B23]. Cakupan sumur adalah **10 wellbore** [L:D03] dengan rentang kejadian dari tahun 2007 sampai 2015 menurut kolom `event_date` [H:tahun.dari] [H:tahun.sampai].

Perlu dinyatakan sejak awal agar naskah tidak menyesatkan: data yang dipakai adalah **data lapangan nyata beresolusi grid 60 detik**, bukan telemetri real time 1 Hz milik Sperry seperti tertulis pada draft lama. Angka 1 Hz di draft berstatus ASUMSI dan bertabrakan dengan kontrak pipeline yang benar-benar dijalankan [L:A14]. Konsekuensinya, klaim kinerja di Bab I dan Bab II selalu dikaitkan ke resolusi 60 detik, dan klaim pemakaian langsung pada stream mitra dinyatakan sebagai rencana integrasi, bukan hasil.

Sistem yang diusulkan proyek berada di antara tahap pengukuran dan tahap keputusan, yaitu lapisan **decision support** yang mengubah data parameter pengeboran menjadi peringatan dini beserta alasannya. Lapisan ini dirancang sebagai **7 mode deteksi** [L:B01] yang direalisasikan dalam **27 varian metode (head)** [L:B03], dilatih pada matriks 55 fitur [L:B48] dan diuji dengan **37 lipatan leave-one-well-out** [L:B25] tanpa satu pun pelanggaran kebocoran fitur ke label [L:B26].

### 1.1.2 Stakeholder dan Kepentingannya

Pedoman mensyaratkan identifikasi stakeholder beserta kepentingannya, dan karakteristik masalah kompleks WP6 mensyaratkan adanya pihak dengan tuntutan yang berbeda. Tabel berikut memisahkan **kepentingan** (apa yang diinginkan pihak tersebut dari sistem) dari **risiko** (apa yang memburuk bila sistem salah bekerja), karena dua kolom itu yang menentukan arah desain di Bab III.

| No | Stakeholder | Peran dalam sistem | Kepentingan utama | Risiko bila sistem salah | Bukti keberadaan pihak |
|---|---|---|---|---|---|
| S1 | Driller / company man di rig | Pemakai keputusan akhir (problem owner) | Peringatan yang cukup awal dan cukup jelas untuk ditindaklanjuti sebelum kerusakan membesar | Kelelahan akibat alarm palsu; keputusan berubah karena saran yang salah | Draft Sperry menetapkan driller dan tim operasi Sperry sebagai problem owner [S:draft Sperry l.64]; pemilik masalah wajib ada pada Buku Pedoman PPT |
| S2 | Drilling engineer / supervisor Sperry Drilling | Penafsir data dan penyusun program pengeboran | Diagnosis yang dapat dijelaskan, bukan kotak hitam, agar dapat dipertanggungjawabkan ke operator | Kehilangan kepercayaan pada alat; rekomendasi tidak dipakai | Divisi mitra; draft Sperry l.31-32 (monitoring parameter pengeboran) |
| S3 | Manajemen Sperry Drilling (mitra MBKM) | Penyedia jasa, pemilik proses kerja | Efisiensi waktu rig dan reputasi layanan | Biaya layanan naik karena waktu non-produktif tidak terdeteksi | Mitra proyek (pedoman 2.8c) |
| S4 | Operator minyak dan gas (mis. Eni) | Pemilik sumur dan anggaran | Ketepatan waktu penyerahan sumur dan keamanan operasi | Pembengkakan biaya rig dan risiko integritas sumur | Rilis pers Halliburton 9 Juli 2026 tentang operasi closed-loop bersama Eni di Indonesia [L:A06] |
| S5 | Engineer MWD/LWD di lokasi | Penjaga mutu kanal pengukuran | Kanal yang rusak atau kosong dikenali sebagai keterbatasan alat, bukan disalahkan ke manusia | Kanal bermasalah tetap dipakai sebagai dasar peringatan | Kanal instrumen MWD menjadi sumber label (VIBLAT_RT, SHKRSK_RT, STUCK_RT, CRPM_RT) [S:docs/V10_D1_BAB_DATA.md §3.2.1] |
| S6 | Fungsi HSE / keselamatan | Penjaga batas keselamatan operasi | Tidak ada insiden sumur (kick, loss, pipa terjepit) yang terlambat ditangani | Peringatan yang terlalu lambat dianggap gagal sistem | Tujuh detektor mencakup hidraulik dan pipa terjepit [L:B01] [S:scratch/v9_i1/v9_i1_RESULTS.json engines]; kategori `safety_personnel` ada di label kejadian [L:B06] |
| S7 | Tim PPT I (tiga mahasiswa Teknik Industri UNS) | Perancang dan pelaksana kajian | Capaian pembelajaran, metode yang dapat dipertanggungjawabkan, data yang dapat diaudit | Naskah dinilai tidak berbasis bukti | Susunan tim dan pembagian peran pada 1.3 |
| S8 | Mentor dosen PPT | Penilai metodologi | Kesesuaian dengan pedoman, rubrik, dan model SIMILAR | Bab I dinilai lemah pada rubrik 1 (memetakan masalah kompleks, bobot 15 persen) | Buku Pedoman PPT h.38 sampai h.40 [S:Buku Pedoman PPT h.38-40] |
| S9 | Pemilik data (Equinor, lewat kanal Volve) | Penyedia data uji | Data dipakai sesuai lisensi dan tidak diklaim sebagai milik proyek | Pelanggaran lisensi CC BY-NC-SA 4.0 | `V3_DATA_ACQUISITION_INVENTORY.md` baris lisensi |

Dua ketegangan antarpihak yang akan muncul berulang di Bab III: (a) S1 dan S5 berlawanan soal ambang, karena S1 menuntut peringatan sesedikit mungkin sedangkan S5 menuntut kanal bermasalah tetap dilaporkan; (b) S2 dan S4 berlawanan soal bentuk keluaran, karena S2 menuntut penjelasan yang dapat diperiksa sedangkan S4 menuntut keputusan cepat. Keduanya menjadi bahan sub-bab trade-off 1.1.5.

### 1.1.3 Alur Operasi dan Alur Data

Alur operasi pengeboran terdiri atas delapan tahap. Kolom terakhir menunjukkan **di mana tahap itu meninggalkan jejak data yang benar-benar dipakai proyek**, sehingga alur ini bukan gambar konseptual tanpa kaitan ke berkas.

| Tahap | Aktor utama | Keluaran tahap | Jejak data di proyek | Titik gangguan yang terukur |
|---|---|---|---|---|
| T1 Perencanaan sumur dan desain rangkaian bor | Drilling engineer | Program pengeboran, desain BHA | **161 berkas bhaRun** [L:B15], **192 assembly tubular berisi 1.392 komponen** [L:B14], **63 berkas trajectory berisi 5.561 stasiun** [L:B16], **27 berkas wbGeometry berisi 109 section** [L:B17] | Rating motor (batas torsi dan tekanan) tidak ada pada 192 dari 192 berkas, sehingga perhitungan beban puncak rangkaian tetap terblokir [S:docs/V10_D1_BAB_DATA.md §3.2.4] |
| T2 Rakit rangkaian dan masuk lubang (make-up dan RIH) | Rig crew, MWD engineer | Rangkaian siap, run dimulai | `dTimStart`/`dTimStop` per run; 154 dari 161 `uidRef` bhaRun bertaut ke tubular [L:B15] | Hanya 19 dari 161 run memuat batas kedalaman, sehingga penautan waktu ke kedalaman rapuh [S:docs/V10_D1_BAB_DATA.md §3.2.5] |
| T3 Pengeboran dengan parameter terkendali | Driller | Lubang bertambah, parameter terekam | Kanal inti `TQA`, `SPPA`, `TFLO`, `RPM`, `SWOB`, `HKLD`, `ROP`, `SPM`, `depth`, `dbtm` [S:docs/V10_D1_BAB_DATA.md §3.2.1] | Beban dan getaran berlebih tidak terlihat sebagai satu angka tunggal, melainkan pola beberapa kanal sekaligus |
| T4 Transmisi telemetri lubang bawah ke permukaan | Sistem MWD/LWD | Data lubang bawah di permukaan | Kanal instrumen `VIBLAT_RT`, `SHKRSK_RT`, `STUCK_RT`, `CRPM_RT` [S:docs/V10_D1_BAB_DATA.md §3.2.1] | Kanal instrumen jarang terisi: `SHKRSK_RT` di F-7 hanya 0,67 persen baris, `CRPM_RT` F-7 0,51 persen, `VIBLAT_RT` F-14 0,14 persen [S:docs/V10_D1_BAB_DATA.md §3.2.1] |
| T5 Perekaman dan penyeragaman grid data | Sistem permukaan dan historian | Data tersimpan dan seragam | Grid **60 detik** dengan mode seluruh baris; jendela fitur 10 menit hanya melihat ke masa lalu [S:docs/V10_D1_BAB_DATA.md §3.3.1-§3.3.2] | Fill-rate tidak seragam: 60 sampai 281 kanal per sumur, tetapi hanya **37 sampai 48 kanal terisi minimal 50 persen** [S:docs/V10_D1_BAB_DATA.md §3.2.1]; F-14 hanya 12.635 dari 96.698 bin menit berstatus mengebor (13,1 persen) [S:docs/V10_D1_BAB_DATA.md §3.2.1] |
| T6 Pemantauan dan interpretasi di permukaan | Driller, MWD engineer, drilling engineer | Penilaian kondisi lubang | Tampilan permukaan (LOGIX pada operasi mitra); di proyek digantikan dashboard advisory | Penilaian bergantung pada intuisi dan pengalaman, tanpa ambang adaptif per sumur; spread alarm palsu 119 kali antar sumur pada mode getaran [L:B33] |
| T7 Keputusan operasi | Driller bersama supervisor | Lanjut, ubah parameter, atau tarik rangkaian | Tidak terekam sebagai kolom keputusan; tercermin pada `state_detail`, `category`, dan `outcome` label kejadian | Keputusan yang tidak terdokumentasi menyulitkan penautan sebab dan akibat antara peringatan dan tindakan |
| T8 Pencatatan kejadian dan pelaporan harian | Rig supervisor, DDR | Laporan harian pengeboran | **884 kejadian terkurasi** [L:B05] dengan 9 kategori [L:B06] | Hanya **582 dari 884** kejadian yang rentang waktunya masuk ke rentang CSV terparse [S:docs/V10_D1_BAB_DATA.md §3.2.3]; 571 kejadian relevansi BHA-nya masih `uncertain` [L:B07] |

Pembacaan alur di atas menghasilkan satu kesimpulan yang menjadi dasar seluruh bab: **informasi disfungsi sudah tersedia di data, tetapi tidak pernah berubah menjadi keputusan lebih awal**. Nilai tambah bukan terletak pada penambahan sensor, melainkan pada penyisipan satu tahap penalaran antara T5 dan T6. Tahap itulah yang dibangun proyek, dan posisinya dalam rich picture ditandai sebagai simpul N7 pada 1.1.4.

![Gambar 1](assets/fig03_cakupan_wellbore.png)

**Gambar 1.** Cakupan data per wellbore: batang gelap (sumbu kiri) menunjukkan jumlah kanal WITSML tersedia dan batang merah (sumbu kanan) menunjukkan jumlah kejadian tercakup. Enam dari sepuluh wellbore memiliki berkas QC dengan jumlah kanal 118 sampai 281. Empat wellbore lain (F-15, F-15 B, F-15 C, F-15 D) tidak memiliki berkas QC terparse sehingga batangnya nol dan ditandai †. Jumlah kejadian per wellbore menyebar dari 2 (F-15 B) sampai 182 (F-14). Skrip sumber: `docs/assets/make_figures.py`, fungsi `fig03_cakupan`.

### 1.1.4 Rich Picture: Narasi dan Spesifikasi Elemen untuk Kartu G1

#### Narasi

Rich picture menggambarkan satu siklus pengeboran sebagai perpindahan data dari lubang bawah ke keputusan, lalu kembali menjadi tindakan di rig. Di sisi kiri gambar, rangkaian bor dan sensor lubang bawah menghasilkan besaran fisis: torsi, tekanan standpipe, laju alir, berat pada bit, putaran, dan getaran. Besaran itu naik ke permukaan sebagai telemetri, direkam oleh historian, diseragamkan ke grid 60 detik, lalu dipotong menjadi jendela 10 menit yang hanya melihat ke belakang [S:V10_D1 §3.3.1-§3.3.2]. Di tengah gambar, tujuh detektor menilai jendela tersebut dan mengeluarkan tiga tingkat keluaran: status kondisi, peringatan berpengawasan, dan tren [L:B04]. Di sisi kanan, driller dan drilling engineer menerima keluaran itu bersama penjelasan kanal mana yang menyimpang, lalu memutuskan melanjutkan, mengubah parameter, atau menarik rangkaian. Keputusan itu mengubah kondisi lubang, yang kembali terekam sebagai data, sehingga siklus tertutup.

Gangguan masuk ke gambar di lima tempat. Pertama, kanal instrumen yang jarang terisi membuat label sulit dibentuk, terlihat dari `CRPM_RT` yang kosong pada 62,34 persen baris dataset stick-slip [L:B34]. Kedua, kepadatan waktu tidak merata, karena F-14 hanya 13,1 persen bin menit berstatus mengebor [S:docs/V10_D1_BAB_DATA.md §3.2.1]. Ketiga, label kejadian bersifat ambigu, karena 56,1 persen dari 884 kejadian justru tidak memuat bukti kegagalan [H:persen.routine_no_failure_evidence] dan 64,6 persen relevansi BHA-nya uncertain [H:persen.bha_relevant_uncertain]. Keempat, ambang global tidak dapat dipakai karena alarm palsu menyebar 119 kali antar sumur [L:B33]. Kelima, keputusan manusia tidak terdokumentasi sebagai data, sehingga rantai sebab akibat antara peringatan dan tindakan harus disimpulkan dari label kejadian.

Empat loop umpan balik digambar sebagai panah melingkar. Loop operasi menjelaskan mengapa masalah ini berulang: disfungsi terdeteksi setelah dampak terjadi, lalu tindakan perbaikan memakan waktu rig, dan hasilnya hanya tercatat sebagai kejadian baru tanpa mengubah cara pemantauan. Loop kalibrasi menjelaskan bahwa model harus disesuaikan per sumur karena karakter kanal berbeda. Loop pelabelan menjelaskan bahwa laporan harian menjadi sumber kebenaran acuan, sehingga mutu laporan menentukan mutu model. Loop keputusan menjelaskan bahwa keluaran model baru bernilai bila berakhir pada tindakan yang terverifikasi.

#### Daftar elemen: simpul (14 simpul, syarat minimal 10)

| ID | Nama elemen | Jenis | Isi yang harus tergambar | Bukti atau angka yang menempel |
|---|---|---|---|---|
| N1 | Formasi dan lubang bor | Lingkungan fisik | Potongan lubang, kedalaman, litologi sekitar | Litologi mudlog: 2.882 interval [L:B18], dengan claystone 957 dan sandstone 884 sebagai litologi terbanyak [S:V10_D1 §3.2.8] |
| N2 | Rangkaian bor dan sensor lubang bawah (MWD/LWD/RSS) | Peralatan | BHA, bit, sensor, arah aliran data ke atas | 161 run bhaRun dan 1.392 komponen tubular [L:B15] [L:B14] |
| N3 | Kanal telemetri lubang bawah | Aliran data | Empat kanal instrumen dan tanda kanal kosong | `VIBLAT_RT`, `SHKRSK_RT`, `STUCK_RT`, `CRPM_RT` [S:docs/V10_D1_BAB_DATA.md §3.2.1]; `CRPM` kosong 62,34 persen [L:B34] |
| N4 | Sensor dan kanal permukaan | Peralatan dan aliran data | Torsi, standpipe, laju alir, hookload, WOB, RPM, ROP | 11 kanal permukaan menjadi dasar 55 fitur [L:B48] |
| N5 | Historian dan penyimpanan data | Penyimpanan | Berkas WITSML terparse dan folder dataset | 10 CSV, 9.935.708 baris mentah [L:B13]; 13 himpunan data [H:inventaris.baris_tabel] |
| N6 | Penyeragaman grid dan jendela fitur | Proses | Dua kotak proses: grid 60 detik lalu jendela 10 menit | Konversi grid 60 detik dan jendela `[t0-10, t0)` [S:docs/V10_D1_BAB_DATA.md §3.3.1-§3.3.2] |
| N7 | Lapisan deteksi tujuh mode kegagalan (sisipan proyek) | Proses baru | Tujuh kotak kecil atau satu kotak berlabel 7 mode, dengan tiga tingkat keluaran | 7 mode [L:B01], 27 head [L:B03], 292.954 baris latih [L:B23] |
| N8 | Dashboard peringatan dan penjelasan | Antarmuka | Peringatan, tingkat keyakinan, kanal penyebab | Tier alat 0 alarm otomatis, 3 peringatan, 2 bersyarat, 2 tren [L:B04] |
| N9 | Driller di rig | Aktor manusia | Orang yang mengambil keputusan langsung | Pemilik masalah; ambang alarm belum layak otomatis [L:B42] |
| N10 | Drilling engineer dan supervisor | Aktor manusia | Pemeriksa penjelasan dan penyusun program | Kebutuhan explainability; ketegangan S2 melawan S4 di 1.1.2, lalu menjadi kriteria pemilihan di Bab III |
| N11 | Operator pemilik sumur | Aktor eksternal | Penerima laporan kinerja sumur | Rilis pers Eni dan Halliburton 9 Juli 2026 [L:A06] |
| N12 | Waktu rig dan waktu non-produktif | Dampak | Dua kolom waktu berdampingan: produktif dan terbuang | 884 kejadian, total 73.500 menit atau 1.225 jam [L:D01]; median 45 menit [L:D02] |
| N13 | Laporan harian pengeboran (DDR) | Sumber label | Tumpukan laporan yang menjadi asal label kejadian | 884 kejadian terkurasi [L:B05]; hanya 50 yang terverifikasi relevan BHA [L:B07] |
| N14 | Tim PPT I dan mentor | Aktor proyek | Kotak pemilik kajian di luar sistem operasi | Tim tiga mahasiswa dan mentor dosen (1.1.2 S7 dan S8) |

#### Daftar elemen: relasi (13 relasi berarah, syarat minimal 8)

| ID | Dari | Ke | Label panah | Jenis aliran |
|---|---|---|---|---|
| R1 | N1 | N2 | kondisi formasi menekan rangkaian | fisik |
| R2 | N2 | N3 | getaran, torsi, tekanan naik sebagai telemetri | data |
| R3 | N2 | N4 | parameter mekanis terukur di permukaan | data |
| R4 | N3 | N5 | kanal instrumen direkam | data |
| R5 | N4 | N5 | kanal permukaan direkam | data |
| R6 | N5 | N6 | penyeragaman grid 60 detik dan pemotongan jendela | proses [S:V10_D1 §3.3.1] |
| R7 | N6 | N7 | matriks 55 fitur masuk ke tujuh detektor | data [L:B48] |
| R8 | N7 | N8 | tiga tingkat keluaran beserta penjelasan | informasi |
| R9 | N8 | N9 | peringatan dan saran tindakan | keputusan |
| R10 | N9 | N2 | ubah parameter atau tarik rangkaian | tindakan |
| R11 | N9 | N12 | keputusan terlambat menambah waktu terbuang | dampak |
| R12 | N9 | N13 | tindakan dan hasilnya dicatat di laporan harian | dokumentasi |
| R13 | N13 | N5 | laporan menjadi label acuan bagi dataset | umpan balik data |

#### Loop umpan balik (4 loop)

| ID | Nama loop | Jalur | Mengapa penting untuk gambar |
|---|---|---|---|
| L1 | Loop operasi reaktif | N9 lalu N12 lalu N13 lalu N5 lalu N7 | Menjelaskan akar masalah berulang: deteksi terjadi setelah dampak timbul, dan hasilnya hanya menjadi catatan kejadian baru |
| L2 | Loop kalibrasi per sumur | N7 lalu N8 lalu N10 lalu N7 | Menjelaskan mengapa ambang global dilarang: alarm palsu menyebar 119 kali antar sumur pada mode getaran [L:B33] |
| L3 | Loop mutu label | N13 lalu N5 lalu N6 lalu N7 | Menjelaskan mengapa mutu laporan harian menentukan mutu model, karena 56,1 persen kejadian tidak memuat bukti kegagalan [H:persen.routine_no_failure_evidence] |
| L4 | Loop keputusan dan verifikasi | N8 lalu N9 lalu N12 lalu N8 | Menutup siklus nilai: keluaran model baru bernilai bila berakhir pada tindakan yang hasilnya terukur |

#### Penanda gangguan (5 titik)

| ID | Titik gangguan | Letak di gambar | Angka pendukung |
|---|---|---|---|
| G1 | Kanal instrumen jarang terisi | Antara N2 dan N3, tanda putus | `CRPM_RT` kosong 62,34 persen baris [L:B34]; `SHKRSK_RT` F-7 0,67 persen terisi [S:docs/V10_D1_BAB_DATA.md §3.2.1] |
| G2 | Kepadatan waktu tidak merata | Di dalam N5 atau N6, tanda kepadatan berbeda per sumur | F-14 hanya 12.635 dari 96.698 bin menit berstatus mengebor (13,1 persen) [S:docs/V10_D1_BAB_DATA.md §3.2.1] |
| G3 | Label kejadian ambigu | Antara N13 dan N5, tanda tanya | 496 dari 884 kejadian tanpa bukti kegagalan (56,1 persen) [H:persen.routine_no_failure_evidence]; 571 uncertain [L:B07] |
| G4 | Ambang tidak portabel | Di dalam N7 atau N8, tanda larangan ambang global | Sebaran alarm palsu 119 kali antar sumur [L:B33] |
| G5 | Keputusan manusia tidak terekam | Antara N9 dan N13, kotak abu-abu | Tidak ada kolom keputusan pada 20 kolom label kejadian [H:labels.kolom] |

#### Ketentuan gambar untuk kartu G1

1. Tata letak: lubang bawah di kiri, permukaan dan historian di tengah, keputusan dan dampak di kanan, waktu sebagai sumbu mendatar dari kiri ke kanan.
2. N7 wajib dibedakan secara visual (warna berbeda) karena itu satu-satunya komponen yang ditambahkan proyek, sedangkan N1 sampai N6 dan N9 sampai N13 adalah sistem eksisting.
3. Setiap nomor simpul, relasi, loop, dan gangguan wajib ditulis di gambar dengan ID yang sama seperti tabel di atas, agar naskah dan gambar dapat dicocokkan satu per satu.
4. Angka yang dicetak di gambar dibatasi pada lima angka berikut agar tidak sesak: 884 kejadian [L:B05], 1.225 jam [L:D01], 7 mode [L:B01], 0 dari 7 alarm otomatis [L:B42], dan 62,34 persen kanal kosong [L:B34].
5. Legenda wajib memuat empat jenis garis: aliran data, aliran keputusan, aliran dampak, dan loop umpan balik.

### 1.1.5 Trade-off Variabel Sistem

Model SIMILAR tahap satu mensyaratkan perumusan trade-off minimal dua aspek. Trade-off di bawah disusun dari kategori 6M agar tidak menjadi retorika, dan setiap kutub ditempeli angka hasil pengukuran proyek, bukan perkiraan.

**T1 Man melawan Method: kewenangan manusia berbanding otomatisasi ambang.**
Kutub Man memberi driller hak memutuskan dengan dukungan peringatan, sedangkan kutub Method menyerahkan keputusan pada ambang otomatis. Data proyek menolak kutub Method untuk saat ini: **tidak ada satu pun dari 7 mode yang memenuhi syarat alarm otomatis** [L:B42], dan rekap alat menunjukkan 0 alarm, 3 peringatan berpengawasan, 2 bersyarat, serta 2 hanya untuk tren [L:B04]. Pada mode hidraulik yang paling kuat, alarm palsu masih 14,62 sampai 58,43 per 24 jam [L:B37], sedangkan sapuan ambang seluruh detektor hanya menemukan 10 dari 402 titik uji yang memenuhi syarat alarm dengan recall positif [L:B44]. Implikasi desain: keluaran 1.1 dan Bab III harus berupa **advisory dengan manusia di dalam loop**, dan klaim alarm otomatis ditulis sebagai sasaran yang belum tercapai, bukan sebagai kemampuan.

**T2 Machine melawan Measurement: resolusi instrumen berbanding kelengkapan pengukuran.**
Kutub Machine menuntut resolusi setinggi mungkin, sedangkan kutub Measurement dibatasi oleh kanal yang benar-benar terisi. Pipeline yang berjalan memakai grid 60 detik [S:docs/V10_D1_BAB_DATA.md §3.3.1], sementara draft lama menulis asumsi stream 1 Hz yang tidak pernah dibuktikan [L:A14]. Pada sisi kelengkapan, tiap sumur membawa 60 sampai 281 kanal tetapi hanya 37 sampai 48 kanal terisi minimal 50 persen [S:docs/V10_D1_BAB_DATA.md §3.2.1], dan kanal `CRPM_RT` yang menjadi dasar label stick-slip kosong pada 62,34 persen baris [L:B34]. Implikasi desain: menaikkan resolusi tanpa menutup kanal kosong hanya menambah baris kosong, sehingga prioritas Bab III adalah **pemilihan kanal dan kalibrasi per sumur**, bukan penambahan frekuensi.

**T3 Method melawan Measurement: sensitivitas ambang berbanding beban alarm palsu.**
Menaikkan sensitivitas menaikkan recall tetapi juga menaikkan alarm palsu, dan keduanya terukur pada detektor yang sama. Pada mode getaran, presisi rule mencapai 0,868 sampai 0,952 [L:B32] tetapi recall hanya 0,276 sampai 0,595 dengan alarm palsu 9,99 sampai 49,94 per 24 jam [L:A17; MD baris 2972]. Pada mode stick-slip, recall rule bahkan 0,000 sampai 0,032 [L:A17; MD baris 2973]. Sebaliknya, detektor pipa terjepit memperoleh presisi 0,9238 sampai 0,9662 dan recall 0,449 sampai 0,599 tetapi alarm palsunya 8,32 sampai 61,0 dan cakupannya hanya 2 lipatan [L:B35] [H:kutipan_md.l2975_stuck_k1]. Implikasi desain: tidak ada satu titik operasi yang berlaku untuk semua detektor, sehingga Bab III wajib memilih titik operasi **per mode** dan menyertakan uji sensitivitas, bukan satu ambang global.

Ketiga trade-off di atas juga menegaskan batas yang jujur: target desain recall 0,70 sampai 0,80 dan lead time 10 sampai 30 menit masih berstatus **ASUMSI berupa target** [L:A17] [L:A08], karena hasil terukur baru mencapai lead 4,5 sampai 8,5 menit pada satu kelas [L:B36] dan nol alarm otomatis [L:B42].

### 1.1.6 Uraian Singkat Permasalahan

Permasalahan utama bukan kerusakan alat tunggal, melainkan **tidak adanya lapisan penalaran yang mengubah data pengeboran menjadi peringatan sebelum dampak terjadi**. Akibatnya, setiap disfungsi baru dikenali setelah ia menjadi waktu terbuang, dan pengetahuan tentangnya hanya tersimpan sebagai catatan kejadian, tidak sebagai aturan pemantauan.

Ukuran dampak yang dapat dipertanggungjawabkan disajikan pada tabel berikut. Semua baris berasal dari hitung ulang kartu ini atau dari ledger angka kartu P0, dan tidak ada baris yang berdiri sebagai perkiraan.

| Dimensi dampak | Angka | Cara membaca yang benar | Rujukan |
|---|---|---|---|
| Populasi kejadian operasi | 884 kejadian pada 10 wellbore | Ini populasi kejadian operasional, bukan 884 kerusakan | [L:B05] [L:D03] |
| Waktu terbuang tercatat | 73.500 menit atau 1.225 jam | Total durasi seluruh kejadian, dihitung dari selisih `act_start` dan `act_end` | [L:D01] |
| Sebaran durasi per kejadian | median 45 menit, p90 180 menit, maksimum 780 menit | Setengah kejadian berlangsung sampai 45 menit, dan sepuluh persen terpanjang bernilai 3 jam atau lebih | [L:D02] |
| Komposisi kategori terbesar | `routine_no_failure_evidence` 496 kejadian (56,1 persen) dan 601,1 jam | Kategori terbesar justru bukan kegagalan, sehingga tidak boleh dipakai sebagai bukti kerusakan | [L:B06] [H:durasi.jam_per_kategori.routine_no_failure_evidence] [H:persen.routine_no_failure_evidence] |
| Kategori kegagalan peralatan permukaan | `surface_rig_equipment` 216 kejadian dan 343,5 jam (28,0 persen jam) | Penyumbang jam terbesar di antara kategori yang memuat bukti kegagalan | [L:B06] [H:durasi.jam_per_kategori.surface_rig_equipment] [H:persen.jam_surface_rig] |
| Kategori kegagalan lubang bawah | `bha_stuck_fishing` 38 kejadian dan 47,3 jam, serta `bha_downhole_equipment` 12 kejadian dan 14,0 jam | Kedua kategori ini yang paling relevan bagi objek Sperry Drilling | [L:B06] [H:durasi.jam_per_kategori.bha_stuck_fishing] [H:durasi.jam_per_kategori.bha_downhole_equipment] |
| Relevansi BHA | 50 kejadian `yes` (5,7 persen), 263 `no`, 571 `uncertain` (64,6 persen) | Hanya sebagian kecil kejadian terbukti menyangkut rangkaian lubang bawah | [L:B07] [H:persen.bha_relevant_yes] [H:persen.bha_relevant_uncertain] |
| Konsentrasi sumur | F-14 menyumbang 182 kejadian (20,6 persen) | Beban kejadian tidak merata, sehingga validasi antar sumur wajib | [L:D03] [H:persen.wellbore_F14] |
| Mutu capaian deteksi saat ini | 0 dari 7 mode layak alarm otomatis | Kapasitas alat saat ini adalah peringatan berpengawasan, bukan alarm | [L:B42] [L:B04] |
| Lead time terukur | 4,5 sampai 8,5 menit dengan median 7,0 menit pada kelas pipa terjepit | Ini satu-satunya lead time bersatuan menit yang terukur di domain rig | [L:B36] |
| Sasaran yang belum tercapai | recall 0,70 sampai 0,80 dan lead 10 sampai 30 menit | Keduanya berstatus target desain, bukan hasil | [L:A17] [L:A08] |
| Rujukan pihak ketiga | efisiensi lebih dari 15 persen pada operasi closed-loop Eni | Milik vendor dan milik operasi pihak lain, tidak boleh menjadi janji luaran proyek | [L:A07] [L:A06] |

Dengan bahan tersebut, permasalahan dirumuskan dalam tiga pertanyaan yang menjadi batas kajian. Ketiganya diberi kode RM1, RM2, dan RM3 supaya dapat dirujuk ulang di Bab III dan Bab IV. Ketiga kode itu adalah pertanyaan riset. Hal-hal yang mengikat ruang lingkup jawaban, misalnya jumlah sumur, kualitas label, dan ketersediaan kanal, bukan pertanyaan riset dan diletakkan terpisah pada paragraf batasan di bawah serta pada subbab 1.4:

**RM1.** Bagaimana merancang lapisan peringatan dini yang memakai data pengeboran yang benar-benar tersedia pada grid 60 detik dan kanal yang terisi 37 sampai 48 per sumur, tanpa mengklaim resolusi yang tidak dimiliki [S:docs/V10_D1_BAB_DATA.md §3.2.1]?
**RM2.** Bagaimana memilih titik operasi per mode sehingga peringatan cukup awal untuk ditindaklanjuti, sedangkan beban alarm palsu tetap dapat diterima pengawas, mengingat sebaran alarm palsu mencapai 119 kali antar sumur [L:B33]?
**RM3.** Bagaimana menyajikan keluaran yang dapat dijelaskan kepada drilling engineer, sehingga rekomendasi dipakai dan bukan diabaikan, ketika kapasitas alat baru sampai pada peringatan berpengawasan pada 3 dari 7 mode [L:B04]?

Batasan realistis yang mengikat jawaban tersebut ada empat. Pertama, batas teknik: data hanya 10 wellbore dengan rentang 2007 sampai 2015 dan tanpa rating motor pada 192 dari 192 berkas tubular [S:docs/V10_D1_BAB_DATA.md §3.2.4]. Kedua, batas kualitas data: 571 kejadian berstatus uncertain dan hanya 582 kejadian yang rentang waktunya bertaut ke CSV terparse [S:docs/V10_D1_BAB_DATA.md §3.2.3]. Ketiga, batas metode: seluruh evaluasi memakai leave-one-well-out dengan 37 lipatan [L:B25], sehingga klaim berlaku untuk sumur baru dalam lapangan yang sama, bukan untuk lapangan lain. Keempat, batas pemanfaatan: keluaran bersifat advisory karena syarat alarm otomatis belum terpenuhi pada detektor mana pun [L:B42].

### 1.1.7 Batas Kejujuran Data dan Status TEMPORER

Empat pernyataan berikut wajib menyertai Bab I agar pembaca tidak menarik kesimpulan berlebih dari angka dampak.

1. **884 kejadian tidak sama dengan 884 kerusakan.** Kategori terbesar, yaitu 496 kejadian atau 56,1 persen, tidak memuat bukti kegagalan [H:persen.routine_no_failure_evidence], dan hanya 50 kejadian atau 5,7 persen yang terverifikasi relevan BHA [H:persen.bha_relevant_yes]. Kalimat yang sah adalah "basis label memuat 884 kejadian operasi dengan total durasi 1.225 jam, 50 di antaranya terverifikasi relevan BHA" [L:D01] [L:B07].
2. **Data proyek adalah data lapangan pihak ketiga, bukan telemetri mitra.** Sumbernya Volve dengan lisensi CC BY-NC-SA 4.0 [S:V3_DATA_ACQUISITION_INVENTORY.md baris lisensi], sehingga klaim penerapan langsung pada stream Sperry dinyatakan sebagai rencana integrasi.
3. **Resolusi yang dipakai adalah 60 detik.** Asumsi 1 Hz pada draft lama tetap ditandai ASUMSI dan tidak boleh muncul kembali sebagai fakta [L:A14].
4. **Pemetaan dampak per mode FMEA berstatus TEMPORER.** Kartu D1 `t_c0e851b8` berstatus blocked dan belum menghasilkan keluaran yang dijanjikan (`docs/PPT1_BUKTI_DAMPAK.md`, `scratch/ppt1/dampak.json`, `code/ppt1_d1_hitung.py`). Karena itu 1.1 hanya memakai dampak **per kategori label** yang sudah terukur, dan tidak memuat occurrence per mode (getaran, stick-slip, telemetri) maupun kejadian per seribu jam operasi. Angka-angka itu akan dipasang oleh kartu D1 dan kartu B2.

Yang belum diverifikasi pada kartu ini dan perlu diperiksa kartu lanjutan: (a) isi 1.392 komponen tubular belum dihitung ulang, hanya jumlah berkasnya [L:B14]; (b) 239 kolom dan 13 kolom pit pada `time.csv` F-9A dilaporkan, belum direproduksi [L:B10] [L:B11]; (c) angka 10.650 `CD_ASSEMBLY_COMP` dan 632 `CD_BHA_COMP_BIT` pada EDM belum dihitung ulang [L:B22]; (d) angka lapisan B dan 402 titik uji masih dilaporkan, bukan dihitung ulang oleh kartu ini [L:B44].

Catatan alat ukur: `scratch/ppt1/verify_numbers.py` melaporkan 0 durasi valid dari 884 baris [L:B05] karena parser di skrip itu hanya menerima tiga format waktu tanpa offset, sedangkan `act_start` memakai offset seperti `+01:00`. Angka durasi karena itu dihitung ulang di kartu ini dengan parser berbeda (regex lalu konversi ke detik epoch) pada `scratch/ppt1/bab1_1_hitung.py`, dan hasilnya sepakat dengan `verify_durations.py`: 884 durasi valid [L:D04], total 73.500 menit [L:D01], median 45 menit, p90 180 menit dengan dua cara kuantil, serta maksimum 780 menit [L:D02]. Selisih nol antara dua instrumen inilah yang membuat angka 1.225 jam dipakai di naskah.

![Gambar 2](assets/fig01_durasi_kejadian.png)

**Gambar 2.** Sebaran durasi interupsi. Panel kiri: histogram 883 kejadian valid pada filter 0 sampai 720 menit dengan garis putus-putus median 45 menit dan garis putus-putus persentil 90 sebesar 180 menit. Panel kanan: fungsi distribusi kumulatif yang menunjukkan setengah kejadian selesai di bawah 45 menit. Filter ini menyisakan 72.720 menit atau 1.212 jam, sedangkan basis penuh 884 kejadian berjumlah 73.500 menit atau 1.225 jam. Satu baris durasi 780 menit berada di luar filter. Nilai persentil 90 sama pada dua cara kuantil (interpolasi dan nearest-rank). Skrip sumber: `docs/assets/make_figures.py`, fungsi `fig01_durasi`.

### 1.1.8 Jejak Angka dan Cara Verifikasi

Setiap angka pada 1.1 membawa salah satu dari tiga tanda. **L** berarti baris pada `docs/PPT1_LEDGER_ANGKA.md` milik kartu P0. **H** berarti kunci pada `scratch/ppt1/bab1_1_angka.json` yang dihasilkan kartu ini. **S** berarti fakta kualitatif atau provenance berkas tanpa klaim aritmetika baru.

| Angka | Konteks | Tanda | Status | Cara verifikasi ulang |
|---|---|---|---|---|
| 884 kejadian | Populasi label | [L:B05] | TERUKUR | `python3 scratch/ppt1/bab1_1_hitung.py` lalu lihat `labels.baris` |
| 9 kategori, 496/216/47/38/28/25/21/12/1 | Komposisi kejadian | [L:B06] | TERUKUR | idem, lihat `labels.kategori` |
| 50/263/571 relevansi BHA | Mutu label | [L:B07] | TERUKUR | idem, lihat `labels.bha_relevant` |
| 73.500 menit dan 1.225 jam | Total waktu terbuang | [L:D01] | TERUKUR | idem, lihat `durasi.total_menit`; bandingkan `scratch/ppt1/verify_durations.py` |
| Median 45, p90 180, maksimum 780 menit | Sebaran durasi | [L:D02] | TERUKUR | idem, lihat `durasi.median_menit`, `p90_menit_cara1`, `p90_menit_interpolasi`, `max_menit` |
| 10 wellbore dan F-14 sebanyak 182 | Sebaran sumur | [L:D03] | TERUKUR | idem, lihat `durasi.wellbore_n` dan `kejadian_per_wellbore` |
| 0 durasi gagal parse | Kualitas stempel waktu | [L:D04] | TERUKUR | idem, lihat `durasi.dibuang_timestamp_gagal` |
| 601,1 / 343,5 / 101,5 / 50,5 / 47,3 / 40,2 / 25,8 / 14,0 / 1,2 jam | Jam per kategori | [H:durasi.jam_per_kategori] | TERUKUR | idem, lihat `durasi.jam_per_kategori` |
| 56,1 persen, 5,7 persen, 64,6 persen, 20,6 persen, 28,0 persen | Persentase turunan | [H:persen] | TERUKUR | idem, lihat blok `persen` (pembilang dan penyebut tercetak di skrip) |
| 13 himpunan data | Inventaris | [H:inventaris.baris_tabel] | TERUKUR | idem, hitung baris tabel §3.1 `docs/V10_D1_BAB_DATA.md` |
| 7.080.457 baris dan 8 CSV | WITSML terparse | [L:B12] | TERUKUR | idem, lihat `witsml_parsed` |
| 9.935.708 baris dan 10 CSV | WITSML folder v2 | [L:B13] | TERUKUR | idem, lihat `witsml_parsed.baris_mentah_total` |
| 292.954 baris pada 6 dataset | Matriks latih | [L:B23] | TERUKUR | idem, lihat `dataset_latih` |
| 37 lipatan dan 0 pelanggaran | Validasi silang | [L:B25] [L:B26] | TERUKUR | idem, lihat `dataset_latih.fold_total` dan `pelanggaran_bocor_total` |
| 27 head dan 7 mode | Registry metode | [L:B03] [L:B01] | TERUKUR | idem, lihat `registry` |
| 55 fitur | Ruang fitur | [L:B48] | TERUKUR | `11 x 5` pada `scratch/ppt1/bab1_1_hitung.py`; rujukan `docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md` baris 1641 |
| 0 dari 7 alarm otomatis | Kapasitas alat | [L:B42] | TERUKUR | `python3 scratch/ppt1/verify_numbers.py` lalu lihat `registry.layer`; rujukan MD baris 3378 |
| Tier 0/3/2/2 | Rekap detektor | [L:B04] | TERUKUR | MD baris 3379-3381; aritmetika 0+3+2+2=7 |
| Recall 0,276 sampai 0,595 dan 0,000 sampai 0,032 | Sensitivitas rule | [L:A17] [H:kutipan_md.l2972_vib] [H:kutipan_md.l2973_ssi] | TERUKUR | kutipan verbatim MD pada JSON kartu ini |
| Alarm palsu 9,99 sampai 49,94 dan 14,62 sampai 58,43 serta 8,32 sampai 61,0 | Beban alarm | [L:B33] [L:B37] [L:B35] | TERUKUR | MD baris 2972, 2975, 2977; kunci `kutipan_md` pada JSON kartu ini |
| Sebaran alarm palsu 119 kali | Ketidakportabelan ambang | [L:B33] | TERUKUR | MD baris 2972 kolom angka kunci |
| Lead 4,5 sampai 8,5 menit | lead time terukur | [L:B36] [H:kutipan_md.l2976_stuck_k2] | TERUKUR | MD baris 2976 |
| 10 dari 402 titik uji | Sapuan ambang | [L:B44] | DILAPORKAN | Belum dihitung ulang; angka ini dipakai hanya sebagai pendukung, bukan dasar keputusan |
| Target recall 0,70 sampai 0,80 dan lead 10 sampai 30 menit | Sasaran desain | [L:A17] [L:A08] | ASUMSI | Ditulis sebagai target di kalimat yang sama |
| Asumsi 1 Hz | Laju stream draft lama | [L:A14] | ASUMSI | Dibantah pipeline 60 detik; `docs/V9_D1_DATA_PIPELINE.md` |
| Efisiensi lebih dari 15 persen | Klaim vendor | [L:A07] | TERUKUR (eksternal) | Rilis pers Halliburton 9 Juli 2026 [L:A06] |
| 62,34 persen kanal CRPM kosong | Keterbatasan sensor | [L:B34] | TERUKUR | MD baris 2973; 22.385/35.906 |
| 96.698 bin menit dan 12.635 bin mengebor | Kepadatan waktu F-14 | [S:V10_D1 §3.2.1] | Dilaporkan dokumen | `docs/V10_D1_BAB_DATA.md` §3.2.1, `v9_d1_01_summary.json` |
| 60 sampai 281 kanal dan 37 sampai 48 terisi | Kelengkapan kanal | [S:V10_D1 §3.2.1] | Dilaporkan dokumen | `docs/V10_D1_BAB_DATA.md` §3.2.1 |
| 582 dari 884 rentang waktu bertaut | Keterbatasan penautan | [S:V10_D1 §3.2.3] | Dilaporkan dokumen | `docs/V10_D1_BAB_DATA.md` §3.2.3 |

Perintah tunggal untuk mereproduksi seluruh angka bertanda L-D, H, dan S di atas pada sisi hitung:

```bash
cd "/mnt/d/Capstone 1(v2)"
python3 scratch/ppt1/bab1_1_hitung.py      # menghasilkan scratch/ppt1/bab1_1_angka.json
python3 scratch/ppt1/verify_durations.py   # pembanding independen untuk blok durasi
python3 scratch/ppt1/verify_numbers.py     # pembanding untuk dataset, fold, dan registry
```
