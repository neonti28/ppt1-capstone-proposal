# RND-S5: audit gelombang 2 (rerun dua seed, artefak, ledger, DOI)

Kartu `t_b5b16adc`. Auditor independen, dan dokumen S1 sampai S4 tidak diubah oleh kartu ini. Cacat ditulis dengan bukti dan usulan perbaikan, bukan diperbaiki di sini.

Riset pendahuluan: scientific-critical-thinking, verification-mandatory, sequentialthinking.

Cara tiap skill dipakai:

- **scientific-critical-thinking** dipakai untuk memisahkan empat tingkat bukti pada setiap temuan: terukur langsung, konsekuensi logis, didukung tidak langsung, dan hipotesis. Cacat hanya dinaikkan menjadi cacat bila ada bukti terukur, misalnya hitungan sel yang tidak menemukan padanan di ledger. Skill ini juga dipakai untuk memisahkan kesalahan alat ukur dari kesalahan objek yang diukur, karena pada audit ini kesalahan pengurai milik auditor sendiri ditemukan empat kali dan diperbaiki sebelum angka dipakai.
- **verification-mandatory** dipakai sebagai aturan main: setiap klaim harus punya keluaran alat, setiap pengunci harus diuji bisa gagal, dan yang tidak dapat diukur ditulis sebagai belum terukur. Kontrol negatif pada bagian 2.4 adalah penerapan aturan ini, karena pengunci yang selalu lolos tidak membuktikan apa pun.
- **sequentialthinking** dipakai untuk merancang tes yang bisa gagal, menetapkan urutan pemeriksaan dari yang paling menentukan, dan memutuskan bahwa kesalahan alat ukur sendiri wajib dilaporkan. Jumlah pikiran yang dipakai: 4.

Kebijakan pengikat: `docs/RND_EVALUATION_POLICY.md`. Audit ini tidak mengubah gate, tidak menaikkan tier, dan tidak menyatakan kelayakan pakai.

---

## 1. Lingkup, bahan, dan definisi vonis

Empat dokumen diaudit dengan total 1015 baris dan 94644 byte. Artefak JSON yang diperiksa 21 berkas, 21 terbuka, dan 726 baris ledger dihitung per kartu.

| Kartu | Dokumen | Baris | Byte | Artefak JSON | Baris ledger |
|---|---|---|---|---|---|
| S1 | `docs/RND_S1_SEED_ROBUSTNESS.md` | 279 | 25445 | 4 | 84 |
| S2 | `docs/RND_S2_HYBRID_VIB_SSI.md` | 311 | 24464 | 6 | 455 |
| S3 | `docs/RND_S3_HYBRID_BITWEAR.md` | 218 | 21573 | 3 | 92 |
| S4 | `docs/RND_S4_LAYER_B_DATA.md` | 207 | 23162 | 8 | 95 |

Definisi tingkat cacat, ditetapkan sebelum hasil diperiksa:

- **kritis**: mengubah kesimpulan utama kartu, atau angka dokumen tidak dapat dibangkitkan ulang.
- **minor**: kesimpulan tidak berubah, tetapi provenance, keterlacakan, atau keterbacaan melemah dan harus diperbaiki.

---

## 2. Rerun dua seed dari S1 dengan harness

### 2.1 Bahan dan cap jari

Dataset dibaca ulang dan cap jarinya dihitung sendiri di luar runner S1: `hyd_ki.csv.gz`, sha256 16 karakter awal `4a701ed63291e455`, 52509 baris, 50 kolom, 9 well, 9 fold LOWO.

Tabel per well pada dokumen S1 bagian 3 diuji ulang dari CSV mentah: 9 well, dan 9 well memberi selisih nol pada keempat kolom.

### 2.2 Angka ringkas pada dua seed

Harness dijalankan segar untuk dua seed, keluaran ditulis ke `scratch/rnd/s5/`, bukan menimpa artefak S1.

| Metrik | Dokumen S1 | Rerun seed 42 | Rerun seed 13 | Selisih |
|---|---|---|---|---|
| FP total | 935 | 935 | 935 | 0 |
| TP total | 3804 | 3804 | 3804 | 0 |
| Presisi median | 0,7789 | 0,7789 | 0,7789 | 0 |
| Recall median | 0,5638 | 0,5638 | 0,5638 | 0 |
| FAR24 kalender median | 3,5302 | 3,5302 | 3,5302 | 0 |
| FAR24 baris median | 32,256 | 32,256 | 32,256 | 0 |
| Lead median | 11,5 | 11,5 | 11,5 | 0 |
| Diperingatkan | 219 | 219 | 219 | 0 |
| Fold FAR tidak lebih dari 6 | 7 | 7 | 7 | 0 |
| Fold gate A baru | 0 | 0 | 0 | 0 |
| Cakupan median | 0,0903 | 0,0903 | 0,0903 | 0 |

Seluruh sel tabel di atas memberi selisih nol. Dua seed memberi angka identik, dan itu sesuai klaim S1 bahwa H1 deterministik. Yang diuji di sini bukan kebenaran klaim tersebut, melainkan apakah angka dokumen dapat dibangkitkan ulang dari kode yang ada.

### 2.3 Perbandingan seluruh sel, bukan sebagian

Tiga tabel dokumen S1 diurai dan dibandingkan sel per sel dengan hasil rerun: tabel bagian 5.1 (26 sel), tabel per fold bagian 4 (27 sel), dan tabel lapisan A bagian 6.1 (90 sel). Total 143 sel dengan 0 sel gagal. Toleransi 5e-5 dipakai karena dokumen membulatkan empat desimal, sehingga batas wajar adalah setengah digit terakhir.

Pembanding kedua di luar dokumen adalah artefak S1 sendiri: 52 nilai ringkas pada dua seed dibandingkan dengan rerun, dan 0 berbeda.

### 2.4 Kontrol negatif: pengunci harus bisa gagal

Dokumen S1 disalin di memori, dua angka diubah, lalu jalur perbandingan yang sama dijalankan. Hasil: dokumen asli memberi nol selisih, dan dokumen yang diubah memberi 2 selisih. Dua mutasi yang dipakai: fp_total 935 menjadi 936, presisi median 0,7789 menjadi 0,7791. Mutasi kedua awalnya tidak tertangkap karena toleransi pertama terlalu longgar, yaitu 0,00051, dan setelah toleransi diperketat menjadi 5e-5 keduanya tertangkap. Tanpa langkah ini, hasil nol selisih pada bagian 2.3 tidak sah.

### 2.5 Aritmetika FAR dihitung ulang

Untuk setiap fold dan setiap seed, FAR kalender dihitung ulang dari fp dan menit negatif kalender tanpa memakai fungsi harness. 18 nilai diperiksa dan 0 menyimpang.

---

## 3. Artefak JSON dan klaim bernama

### 3.1 Artefak terbuka

| Kartu | Berkas | Byte | Buka |
|---|---|---|---|
| S1 | 4 | 319465 | ya |
| S2 | 6 | 600082 | ya |
| S3 | 3 | 115879 | ya |
| S4 | 8 | 310315 | ya |

Semua 21 berkas terbuka sebagai JSON atau JSONL. Catatan penting untuk S2: `s2_vib.json` dan `s2_ssi.json` tidak ada lagi di `scratch/rnd/s2/`, dan ketiadaannya disengaja karena berkas itu dibatalkan. Acuan S2 yang sah adalah `s2_records_vib.json`, `s2_records_ssi.json`, `s2_ringkas.json`, dan `s2_meta.json`.


Jumlah record diukur secara mekanis pada setiap berkas, bukan dikira: jumlah kunci top-level, koleksi terpanjang di dalam berkas, dan kunci hitung eksplisit bila berkas memuatnya. Nilai yang tidak dapat dihitung dari berkas tidak diklaim di tabel ini.

| Kartu | Berkas | Tipe | Kunci top | Koleksi terpanjang | Kunci hitung eksplisit | Byte | sha256 |
|---|---|---|---|---|---|---|---|
| S1 | s1_h_saturasi.json | objek | 16 | h_grid = 15 | n_fold = 9 | 3606 | cd5258929f56 |
| S1 | s1_hluas.json | objek | 11 | grid_luas = 24 | n_fold = 9; ringkas.n_fold = 9; per_fold[].rows.n_pos = 1394 | 12141 | 275cc5084273 |
| S1 | s1_hyd_seeds.json | objek | 13 | per_seed.42.folds = 36 | reproduksi.ringkas_r8.n_fold = 9; reproduksi.ringkas_kini.n_fold = 9; per_seed.42.ringkas.n_fold = 9 | 302269 | ff82bf151abf |
| S1 | s1_meta.json | objek | 21 | dataset_shape = 2 | n_fold = 9 | 1449 | cad5be87f12b |
| S2 | p2_probe.json | objek | 2 | vib.kolom = 63 | vib.n_well = 4; ssi.n_well = 9 | 9388 | 1f03829dcd0c |
| S2 | p3_kanal.json | objek | 2 | vib.kolom_bins = 32 | - | 2994 | e8e7211d4e2d |
| S2 | s2_meta.json | objek | 13 | kanal = 11 | - | 529 | a876ec90d583 |
| S2 | s2_records_ssi.json | objek | 15 | fitur = 55 | n_baris = 35906; n_well = 9; n_fold = 9 | 343877 | d92af531fdf1 |
| S2 | s2_records_vib.json | objek | 15 | fitur = 55 | n_baris = 23922; n_well = 4; n_fold = 4 | 157781 | 1be569cf815f |
| S2 | s2_ringkas.json | objek | 3 | ssi.wells = 9 | vib.n_baris = 23922; vib.n_well = 4; vib.sensitivitas.H1_stat_dan_rule_b12.n_fold = 4 | 85513 | 1085a9dd6c24 |
| S3 | s3a_feasibility.json | objek | 7 | inventaris.nama_kolom = 18 | label.n_well = 7; label.n_pos = 49732 | 8072 | af906244ae46 |
| S3 | s3b_hybrid.json | objek | 7 | records = 49 | records[].n_pos = 182; records[].rows.n_pos = 182; records[].rows.n_neg = 13564 | 72822 | 8c6f829605c2 |
| S3 | s3c_ringkas.json | objek | 10 | tabel = 49 | kelayakan.n_well = 7; kelayakan.n_pos = 49732; tabel[].n_pos = 182 | 34985 | b43d6b7fd608 |
| S4 | crosscheck.json | objek | 4 | silang_per_wellbore = 26 | - | 7049 | 1d81851b7bbd |
| S4 | ddr_activity_stats.json | objek | 3 | laporan.wellbore_daftar = 26 | laporan.n_baris = 1759; activity.n_record = 23447 | 19860 | 58e7e897a836 |
| S4 | ddr_downtime_records.jsonl | JSONL | - | baris JSONL = 533 | - | 217645 | b1a99d8cb712 |
| S4 | ddr_downtime_table.json | objek | 9 | tabel.kolom = 7 | record.n_record = 533 | 6300 | 96b0e9f08784 |
| S4 | inventory.json | objek | 8 | uji_silang.per_wellbore = 26 | kelompok.tersedia_dan_layak[].n_baris = 1759; kelompok.ada_tetapi_tidak_memadai[].n_record = 533; kelompok.ada_tetapi_tidak_memadai[].n_laporan = 1212 | 15704 | 51aa0f1c097e |
| S4 | inventory_raw.json | objek | 7 | csv_di_data.berkas = 53 | katalog_volve.n_baris = 4035 | 24974 | 4bfb4ae03b98 |
| S4 | labels_duration.json | objek | 18 | sumber.kolom = 20 | n_baris = 884; tujuh_well_engine.n_kejadian = 671 | 15280 | 5555d516e1d6 |
| S4 | token_scan.json | objek | 4 | xml.contoh_berkas.kata_berakar_price = 2 | - | 3503 | 8ef09d9b0723 |

### 3.2 Klaim bernama: nilai dokumen dibandingkan dengan path JSON

Setiap baris di bawah mengambil satu nilai yang tertulis di dokumen, lalu mengambil nilai dari path JSON yang eksplisit. 51 klaim diuji, 51 lulus, 0 gagal. Nilai JSON ditulis apa adanya dengan titik desimal, sedangkan nilai dokumen ditulis dengan koma seperti pada dokumen asalnya, dan perbandingan dilakukan pada nilai numeriknya bukan pada teksnya.

| Kartu | Klaim | Rujukan JSON | Nilai JSON | Nilai dokumen | Hasil |
|---|---|---|---|---|---|
| S1 | FP total seed 42 | `s1_hyd_seeds.json` `per_seed.42.ringkas.fp_total` | 935 | 935 | cocok |
| S1 | TP total seed 42 | `s1_hyd_seeds.json` `per_seed.42.ringkas.tp_total` | 3804 | 3804 | cocok |
| S1 | presisi median seed 42 | `s1_hyd_seeds.json` `per_seed.42.ringkas.precision_median` | 0.7789 | 0,7789 | cocok |
| S1 | recall median seed 42 | `s1_hyd_seeds.json` `per_seed.42.ringkas.recall_median` | 0.5638 | 0,5638 | cocok |
| S1 | FAR24 kalender median | `s1_hyd_seeds.json` `per_seed.42.ringkas.far24_kalender_median` | 3.5302 | 3,5302 | cocok |
| S1 | lead median | `s1_hyd_seeds.json` `per_seed.42.ringkas.lead_median_median` | 11.5 | 11,5 | cocok |
| S1 | onset | `s1_hyd_seeds.json` `per_seed.42.ringkas.n_onset` | 390 | 390 | cocok |
| S1 | diperingatkan | `s1_hyd_seeds.json` `per_seed.42.ringkas.n_diperingatkan` | 219 | 219 | cocok |
| S1 | fold FAR tidak lebih dari 6 | `s1_hyd_seeds.json` `per_seed.42.ringkas.fold_far_le6` | 7 | 7 | cocok |
| S1 | fold gate A baru | `s1_hyd_seeds.json` `per_seed.42.ringkas.fold_gate_A_baru` | 0 | 0 | cocok |
| S1 | cakupan median | `s1_hyd_seeds.json` `per_seed.42.ringkas.cakupan_median` | 0.0903 | 0,0903 | cocok |
| S1 | FP total dengan grid luas | `s1_hluas.json` `ringkas.fp_total` | 237 | 237 | cocok |
| S1 | recall median dengan grid luas | `s1_hluas.json` `ringkas.recall_median` | 0.1457 | 0,1457 | cocok |
| S1 | fold lolos anggaran dengan grid luas | `s1_hluas.json` `n_lolos_anggaran` | 9 | 9 | cocok |
| S1 | fold dengan h tersaturasi | `s1_h_saturasi.json` `n_saturasi` | 9 | 9 | cocok |
| S1 | batas atas grid h | `s1_h_saturasi.json` `h_grid_maks` | 30.0 | 30 | cocok |
| S1 | h terkecil lolos di luar grid | `s1_h_saturasi.json` `h_terkecil_lolos_anggaran_di_luar_grid` | 300.0 | 300 | cocok |
| S1 | rentang FP kontrol ML | `s1_hyd_seeds.json` `kontrol_stokastik.sebaran.fp_rentang` | 345 | 345 | cocok |
| S1 | FP kontrol minimum | `s1_hyd_seeds.json` `kontrol_stokastik.sebaran.fp_min` | 1076 | 1076 | cocok |
| S1 | FP kontrol maksimum | `s1_hyd_seeds.json` `kontrol_stokastik.sebaran.fp_maks` | 1421 | 1421 | cocok |
| S2 | vib jumlah baris | `s2_ringkas.json` `vib.n_baris` | 23922 | 23922 | cocok |
| S2 | vib positif dapat diuji | `s2_ringkas.json` `vib.n_pos_total_dapat_diuji` | 5429 | 5429 | cocok |
| S2 | ssi jumlah baris | `s2_ringkas.json` `ssi.n_baris` | 35906 | 35906 | cocok |
| S2 | ssi positif dapat diuji | `s2_ringkas.json` `ssi.n_pos_total_dapat_diuji` | 592 | 592 | cocok |
| S2 | ssi fold tidak dapat diuji | `s2_ringkas.json` `ssi.n_fold_tidak_dapat_diuji` | 2 | 2 | cocok |
| S2 | persistence FAR24 kalender | `s2_ringkas.json` `vib.agregat.persistence.far24_kalender_median` | 22.0218 | 22,0218 | cocok |
| S2 | persistence recall median | `s2_ringkas.json` `vib.agregat.persistence.recall_median` | 0.740465 | 0,7405 | cocok |
| S2 | persistence presisi median | `s2_ringkas.json` `vib.agregat.persistence.precision_median` | 0.728803 | 0,7288 | cocok |
| S2 | ML vib b24 recall median | `s2_ringkas.json` `vib.sensitivitas.ML_kalender_b24.recall_median` | 0.104132 | 0,1041 | cocok |
| S2 | ML vib b24 presisi median | `s2_ringkas.json` `vib.sensitivitas.ML_kalender_b24.precision_median` | 0.778128 | 0,7781 | cocok |
| S2 | ML vib b24 FAR24 kalender | `s2_ringkas.json` `vib.sensitivitas.ML_kalender_b24.far24_kalender_median` | 3.12255 | 3,1225 | cocok |
| S2 | ML ssi b24 recall median | `s2_ringkas.json` `ssi.sensitivitas.ML_kalender_b24.recall_median` | 0.215686 | 0,2157 | cocok |
| S2 | ML ssi b24 presisi median | `s2_ringkas.json` `ssi.sensitivitas.ML_kalender_b24.precision_median` | 0.07619 | 0,0762 | cocok |
| S2 | ML ssi b24 FAR24 kalender | `s2_ringkas.json` `ssi.sensitivitas.ML_kalender_b24.far24_kalender_median` | 6.0647 | 6,0647 | cocok |
| S3 | USROP jumlah baris | `s3a_feasibility.json` `inventaris.baris` | 198928 | 198928 | cocok |
| S3 | label positif | `s3a_feasibility.json` `label.n_pos` | 49732 | 49732 | cocok |
| S3 | jumlah well | `s3a_feasibility.json` `label.n_well` | 7 | 7 | cocok |
| S3 | well tanpa positif | `s3a_feasibility.json` `label.n_well_tanpa_positif` | 2 | 2 | cocok |
| S3 | indeks duplikat | `s3a_feasibility.json` `identitas.indeks_duplikat` | 145887 | 145887 | cocok |
| S3 | ML fisik presisi median | `s3c_ringkas.json` `agregat.ml_fisik.precision_median` | 0.6496 | 0,6496 | cocok |
| S3 | ML fisik recall median | `s3c_ringkas.json` `agregat.ml_fisik.recall_median` | 0.9968 | 0,9968 | cocok |
| S3 | ML fisik FAR24 median | `s3c_ringkas.json` `agregat.ml_fisik.far24_median_valid` | 110.432 | 110,432 | cocok |
| S4 | record activity DDR | `ddr_activity_stats.json` `activity.n_record` | 23447 | 23447 | cocok |
| S4 | kode kerja unik | `ddr_activity_stats.json` `activity.n_kode_unik` | 64 | 64 | cocok |
| S4 | laporan DDR | `ddr_activity_stats.json` `laporan.n_baris` | 1759 | 1759 | cocok |
| S4 | record tabel downtime | `ddr_downtime_table.json` `record.n_record` | 533 | 533 | cocok |
| S4 | laporan yang memuat tabel | `ddr_downtime_table.json` `tabel.n_file_memuat_tabel` | 325 | 325 | cocok |
| S4 | record dengan downtime nol | `ddr_downtime_table.json` `record.n_downtime_nol` | 533 | 533 | cocok |
| S4 | kejadian pada label | `labels_duration.json` `n_baris` | 884 | 884 | cocok |
| S4 | total jam label | `labels_duration.json` `durasi_jam.sum` | 1225.0 | 1225,0 | cocok |
| S4 | jumlah kolom labels | `labels_duration.json` `sumber.kolom` | 20 | 20 | cocok |

Tiga entri pertama pada versi pertama pemeriksa ini salah karena path diambil dari handoff S2 yang sudah dibatalkan, bukan dari `s2_ringkas.json`. Kesalahannya adalah kesalahan auditor, dan yang benar adalah path `ssi.sensitivitas.ML_kalender_b24` untuk nilai 0,0762 dan 0,2157, serta `vib.sensitivitas.ML_kalender_b24` untuk 0,1041, 0,7781, dan 3,1225. Ini contoh mengapa angka handoff tidak boleh dipakai sebagai sumber.

### 3.3 Uji klaim setiap angka punya baris ledger

Klaim yang diuji: S1 menulis setiap angka punya baris S1-nnn, S2 dan S3 menulis hal yang sama untuk kartunya. Metode: setiap sel angka pada tabel dokumen diambil, lalu dicari padanannya pada blok ledger kartu itu, dengan dua tafsir untuk token bertitik dan toleransi pembulatan. Batas metode: yang diuji adalah keberadaan nilai pada blok, bukan pemetaan sel ke baris tertentu, dan penerimaan dua tafsir membuat angka ini batas atas.

| Kartu | Sel angka tabel | Punya padanan | Fraksi | Contoh tanpa padanan |
|---|---|---|---|---|
| S1 | 508 | 344 | 0,6772 | 7571, 1394, 11249, 7390, 1426 |
| S2 | 430 | 430 | 1 | tidak ada |
| S3 | 339 | 139 | 0,41 | 53.041, 7.622, 5.278, 40.141, 51.708 |
| S4 | 95 | 95 | 1 | tidak ada |

S2 memberi fraksi 1 dan S4 memberi 1, sehingga klaim kedua kartu itu terpenuhi. S1 memberi 0,6772 dan S3 memberi 0,41, sehingga klaim kedua dokumen itu tidak terpenuhi pada tabel per fold dan tabel kelayakan. Ini cacat D2 dan D3.

---

## 4. Baris ledger per kartu

| Kartu | Baris | Cocok | Tidak cocok | Tidak dapat diresolusi | Derivasi | Sel bukan angka |
|---|---|---|---|---|---|---|
| S1 | 84 | 38 | 4 | 20 | 17 | 5 |
| S2 | 455 | 427 | 0 | 5 | 23 | 0 |
| S3 | 92 | 73 | 2 | 12 | 1 | 4 |
| S4 | 95 | 54 | 0 | 32 | 4 | 5 |

Tidak ada kartu dengan nol baris, jadi tidak ada kartu yang gagal provenance pada butir hitung baris. Seluruh baris tepat tujuh kolom dan tidak ada kode ganda.

Metode resolusi: nilai dan kolom rujukan persis setiap baris diambil, lalu path JSON pada rujukan itu dibuka dan nilainya dibandingkan. Bila satu sel memuat beberapa angka, setiap komponen diuji terhadap daun numerik cabang yang dirujuk. 6 baris dinyatakan tidak cocok oleh mesin. Setelah diperiksa tangan, keenam baris itu adalah sel hitungan atau julat, bukan nilai daun tunggal, sehingga resolver tidak dapat membandingkannya. Hitungan ulang mandiri memberi 6 baris cocok dari 6, jadi tidak ada angka salah pada kelompok itu. Bentuk selnya: panjang daftar 7, 5, 9, 2, dan 7, serta satu julat persen 1,32 sampai 54,25.

Cacat angka yang nyata ditemukan di luar kelompok itu. Baris S4-013 menulis 884 kolom, sedangkan kolom rujukan pada baris yang sama menyebut sumber.kolom berisi 20 kolom, sehingga baris itu membantah dirinya sendiri. Baris tersebut tidak masuk kelompok MISMATCH, karena resolver hanya menguji keberadaan nilai pada cabang dan tidak menguji pasangan nilai kedua di dalam satu sel. Ini contoh bahwa resolusi otomatis tidak cukup dan pemeriksaan tangan tetap perlu.

Versi pertama resolver juga menandai S2-448, S2-449, dan S3-085. Ketiganya derivasi sah dan dapat dihitung ulang: S2-448 nilai 12,1 = (1 - p) / p dengan p = 0,07619, yang memberi 12,13; S2-449 nilai 3,67 = 22,0218 dibagi 6, yang memberi 3,67; S3-085 nilai 18,41 = 110,432 dibagi 6. Penandaan itu kesalahan alat ukur, bukan kesalahan ledger.

Format angka ledger mencampur gaya: 61 sel memakai titik ribuan, sedangkan blok yang sama memakai koma desimal. Sebaran: S1 3, S2 42, S3 16, S4 0. Satu sel berisi 32.256 dapat berarti 32,256 atau 32256, dan keduanya benar terhadap JSON yang berbeda. Blok S5 pada ledger memakai titik desimal tanpa pemisah ribuan supaya cacat ini tidak berulang.

---

## 5. DOI dan rujukan luar

Butir DOI disiapkan dengan dua lapis seperti V1, yaitu lapis registrasi (HEAD ke doi.org tanpa mengikuti redirect) dan lapis metadata (api.crossref.org). Pada gelombang 2 tidak ada objek yang dapat diperiksa: 0 DOI dan 0 URL ditemukan. Karena tidak ada target, hasilnya ditulis tidak berlaku, bukan lulus. Nol pemeriksaan berhasil bukan bukti bahwa rujukan benar.

| Kartu | RUN-KITA | DERIVASI | KONVENSI | STANDAR | BELUM TERUKUR |
|---|---|---|---|---|---|
| S1 | 61 | 17 | 1 | 0 | 5 |
| S2 | 424 | 23 | 7 | 1 | 0 |
| S3 | 86 | 1 | 4 | 0 | 1 |
| S4 | 86 | 4 | 1 | 0 | 4 |

Satu-satunya rujukan luar adalah API RP 7G pada S2 untuk nilai 32,17405 ft/s2, dan rujukan itu tidak menyebut nomor bagian. Menurut aturan provenance, kelas STANDAR menuntut nomor standar dan bagian, sehingga baris ini lemah dan dicatat sebagai cacat D5.

---

## 6. Pemisahan lapisan A, B, C dan daftar belum terverifikasi

| Kartu | Lapisan A | Lapisan B | Lapisan C | Bagian belum terverifikasi | Butir |
|---|---|---|---|---|---|
| S1 | terukur penuh, bagian 6 untuk sembilan fold dan lima seed | terukur untuk lead dan beban alarm, belum untuk rupiah dan jam henti | terukur antar well, antar seed, antar titik operasi; lintas kampanye belum | `### 8.4 Daftar yang belum terverifikasi` | 8 |
| S2 | terukur, bagian 4 dengan kurva sensitivitas anggaran | belum terukur, bagian 7, sebabnya data maintenance tidak ada | terukur, bagian 6 kestabilan, variasi seed, cakupan | `## 11. YANG BELUM TERVERIFIKASI` | 6 |
| S3 | terukur, bagian 4 | belum terukur, bagian 6, sebabnya tidak ada kunci bit | terukur, bagian 5 | `## 10. Yang belum terverifikasi` | 6 |
| S4 | tidak diubah kartu ini, diambil dari R8 dan S1 | terukur sebagian, bagian 7, komponen jam henti terukur dan rupiah belum | tidak diubah kartu ini, satu kontribusi register kegagalan | `## 9. BELUM TERVERIFIKASI` | 7 |

Keempat dokumen memisahkan tiga lapisan dan punya bagian daftar belum terverifikasi, dengan 27 butir seluruhnya. Yang belum terukur pada lapisan B konsisten dengan temuan S4: biaya, work order bernomor, jadwal inspeksi, dan produksi tertunda tidak ada di repo, sehingga nilai rupiah tidak dapat dihitung dari data yang ada.

Jumlah pikiran sequ-mcp yang dinyatakan tiap dokumen: S1 10, S2 6, S3 5, S4 4, seluruhnya 25. Semua di atas ambang tiga. Angka ini adalah laporan diri penulis kartu.

Keempat dokumen juga bersih dari em-dash: 0 kemunculan. Ini sesuai aturan nomor tujuh pada kartu.

---

## 7. Tabel cacat

Jumlah cacat 9, dengan 0 kritis dan sisanya minor. Tidak ada cacat kritis.

| Kode | Kartu | Cacat | Bukti | Tingkat | Yang harus diperbaiki |
|---|---|---|---|---|---|
| D1 | S4 | baris ledger S4-013 menulis 884 record / 884 kolom, sedangkan kolom rujukan pada baris yang sama menulis sumber.kolom berisi 20 kolom; dokumen S4 mengutip S4-013 untuk 20 kolom sehingga kutipan itu menunjuk baris yang membantah dirinya | RND_PROVENANCE_LEDGER.md baris 2182; RND_S4_LAYER_B_DATA.md baris 36; labels_duration.json sumber.kolom berisi daftar 20 nama | minor | ganti sel angka S4-013 menjadi 884 record / 20 kolom, dan tambahkan assert panjang daftar |
| D2 | S1 | dokumen menulis setiap angka punya baris S1-nnn, sedangkan hanya 344 dari 508 sel angka tabel (0,6772) menemukan padanan di blok ledger S1 | RND_S1_SEED_ROBUSTNESS.md baris 14; pencocokan setiap sel tabel ke angka pada blok S1 ledger; contoh tanpa padanan: 7571, 1394, 11249, 86454, 317679 | minor | samakan kalimat dengan cakupan, atau tambah baris untuk tabel per fold bagian 4 dan 6.1 |
| D3 | S3 | dokumen menulis setiap angka menunjuk baris ledger, sedangkan hanya 139 dari 339 sel angka tabel (0,41) menemukan padanan di blok ledger S3 | RND_S3_HYBRID_BITWEAR.md baris 17; contoh tanpa padanan: 53.041, 7.622, 5.278, 40.141 | minor | lengkapi baris untuk tabel kelayakan bagian 2, atau turunkan klaimnya |
| D4 | semua | 61 sel angka ledger memakai titik sebagai pemisah ribuan, sedangkan blok yang sama memakai koma desimal, sehingga satu sel berisi 32.256 dapat dibaca 32,256 atau 32256 | S1 3 baris, S2 42 baris, S3 16 baris berpola 1.234; contoh S1-034 (32.256) lawan S3-001 (198.928) | minor | tetapkan satu gaya pada seluruh ledger: titik desimal tanpa pemisah ribuan |
| D5 | S2 | nilai 32,17405 ft/s2 diberi kelas STANDAR dengan rujukan API RP 7G tanpa nomor bagian, sedangkan kelas STANDAR menuntut nomor standar dan bagian | RND_S2_HYBRID_VIB_SSI.md bagian 2 dan baris ledger S2 kelas STANDAR berjumlah 1 | minor | tambahkan bagian standar, atau turunkan kelas menjadi KONVENSI |
| D6 | semua | tidak ada DOI (0) dan tidak ada URL (0) di empat dokumen, sehingga butir audit DOI tidak punya target dan tidak dapat dinyatakan lulus | pencarian pola 10.xxxx dan https:// pada empat dokumen menghasilkan nol | minor | tambahkan rujukan ber-DOI untuk klaim metode, atau nyatakan klaim sebagai KONVENSI internal |
| D7 | S1 | dari 10 pikiran sequ-mcp yang diklaim, empat pikiran run awal tidak dapat dibuktikan dari artefak dan dokumen sendiri menyatakannya | RND_S1_SEED_ROBUSTNESS.md baris 12 | minor | simpan id sesi atau transkrip ringkas sequ pada artefak kartu |
| D8 | S1,S2,S3 | keterlacakan dokumen ke baris ledger lemah: kode S1-nnn yang dikutip 0, S2 0, S3 0, sedangkan S4 mengutip 42 | pencarian pola Sx-nnn pada tiap dokumen; kode hilang 0 pada semua kartu | minor | cantumkan kode baris pada tabel dokumen seperti S4 |
| D9 | S4 | 32 dari 95 baris ledger memakai rujukan prosa multi-nilai sehingga tidak dapat diresolusi mesin, dan pemetaan posisional nilai ke kunci tidak terbukti | hasil resolusi S4: 45 cocok penuh, 9 cocok sebagian, 32 tidak dapat diresolusi, 4 derivasi, 5 sel bukan angka | minor | satu nilai satu path pada kolom rujukan persis |

Arti tidak adanya cacat kritis: pada dua seed yang diuji, angka utama S1 dapat dibangkitkan ulang persis, seluruh artefak terbuka, dan setiap kartu punya baris ledger. Cacat yang tersisa menyangkut kebenaran klaim tentang provenance sendiri, format angka, dan keterlacakan.

Satu hal yang harus dinyatakan tegas supaya tidak disalahpahami: tidak adanya cacat kritis bukan bukti bahwa angka S2, S3, dan S4 benar. Untuk ketiganya, kartu ini memeriksa keberadaan nilai pada artefak dan keterlacakan baris ledger, bukan menjalankan ulang modelnya. Hanya S1 yang dijalankan ulang penuh, dan hanya pada dua dari lima seed.

---

## 8. Yang belum terverifikasi pada audit ini

1. Rerun hanya dua seed dari lima seed S1, yaitu 42 dan 13. Seed 7, 21, dan 33 tidak dijalankan.
2. Rerun memakai harness yang sama dengan S1, sehingga yang terbukti adalah kesambungan dan reproduksibilitas, bukan kebenaran desain harness. Jalur independen yang dipakai terbatas pada cap jari dataset, tabel per well dari CSV mentah, dan aritmetika FAR.
3. S2, S3, dan S4 tidak dijalankan ulang. Model, kalibrasi, dan pemindaian DDR tidak direproduksi; yang diperiksa hanya artefak, ledger, dan angka yang dikutip.
4. Resolusi ledger memakai heuristik path. Untuk sel multi-nilai, pemetaan posisional nilai ke kunci tidak diuji, hanya keberadaan nilai di cabang.
5. Uji cakupan ledger memakai pencarian nilai pada blok, bukan pemetaan sel ke baris, dan menerima dua tafsir titik. Angka fraksi pada bagian 3.3 karena itu adalah batas atas.
6. Jumlah pikiran sequ pada empat dokumen adalah laporan diri penulis kartu dan tidak dapat diperiksa dari artefak. Untuk S1, empat pikiran run awal bahkan dinyatakan tidak terbukti oleh dokumen itu sendiri.
7. Pemeriksaan DOI berhenti pada kesimpulan tidak ada DOI. Tidak ada permintaan jaringan ke doi.org atau Crossref pada kartu ini karena tidak ada objek yang bisa diperiksa.
8. Mutu keputusan teknis tiap kartu, misalnya apakah pemilihan ambang wajar, tidak dinilai di sini. Kartu ini menilai bukti dan keterlacakan.

---

## 9. Ringkasan lima baris

1. Rerun seed 42 dan 13 memberi angka yang sama persis dengan dokumen S1 pada 143 sel yang diperiksa, dengan 0 selisih, dan pengunci sudah diuji bisa gagal lewat 2 mutasi yang tertangkap.
2. Seluruh 21 artefak terbuka, dan 51 klaim bernama path terbukti sama dengan JSON mentah.
3. Empat kartu punya ledger, total 726 baris tujuh kolom tanpa duplikat, sehingga tidak ada kartu yang gagal provenance pada butir hitung baris.
4. Audit menemukan 9 cacat, semuanya minor, termasuk satu baris ledger yang membantah dirinya sendiri (S4-013: 884 kolom lawan 20 kolom).
5. Tidak ada DOI untuk diperiksa, klaim setiap angka punya baris ledger hanya terpenuhi penuh pada S2, dan keterlacakan kode ledger masih lemah karena S1, S2, dan S3 tidak mengutip kode barisnya sendiri di badan dokumen.

---

Berkas bukti: `scratch/rnd/s5/s5_rerun_audit.json`, `s5_negatif.json`, `s5_resolve3.json`, `s5_klaim2.json`, `s5_coverage.json`, `s5_stats.json`, `s5_kode_doi_lapisan.json`. Kode: `scratch/rnd/s5/s5a_rerun_audit.py`, `s5b_negatif.py`, `s5c_klaim2.py`, `s5e_coverage.py`, `s5d_stats.py`, `a8_resolve3.py`, `a7_kode_doi.py`, `s5g_dokumen.py`.
