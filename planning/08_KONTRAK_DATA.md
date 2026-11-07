# 08 KONTRAK DATA PER FITUR

Dokumen ini menetapkan kontrak data untuk 21 fitur prioritas: nama field, tipe, satuan, sumber
nyata, dan perilaku saat data tidak tersedia. Kontrak ini dipakai tim website sebagai satu-satunya
rujukan bentuk muatan, sehingga dua orang yang membangun panel berbeda menghasilkan bentuk baris
yang sama.

Berkas masukan yang dibuka, ukuran byte, dan keluaran perintah pemeriksaan angka ada di bagian 1
dan bagian 10. Yang belum diverifikasi ada di bagian 9.

---

## 0. Kerangka wajib

Sembilan butir di bawah dipakai apa adanya dan tidak diubah. Butir 8 dan 9 adalah tambahan dokumen
ini untuk keperluan kontrak antarmuka.

1. Alarm otomatis BUKAN tujuan. ML dipakai sebagai sistem pendukung keputusan dengan skor keyakinan,
   bukan pemutus. Konsekuensi kontrak: tidak ada field `alarm_kritis`, tidak ada field
   `kirim_notifikasi`, dan setiap muatan wajib membawa `keputusan_akhir` bernilai `MANUSIA`.
2. Setiap angka yang ditulis punya sumber: berkas dan baris, atau baris ledger
   `docs/RND_PROVENANCE_LEDGER.md`. Konsekuensi kontrak: setiap field angka wajib punya pasangan
   field sumber, dan baris tanpa sumber ditolak oleh pemeriksa tampilan.
3. Dilarang mengklaim sesuatu berjalan tanpa bukti. Setiap perintah yang dijalankan untuk memeriksa
   angka ditempel keluarannya di bagian 10.
4. Kekurangan data dikemas menjadi fitur yang berguna (pola Dynamic Island), bukan ditulis sebagai
   keluhan. Konsekuensi kontrak: field yang tidak tersedia diisi `null` plus satu label teks, bukan
   angka nol dan bukan string kosong.
5. Setiap fitur wajib punya pengguna, momen pakai, masukan, keluaran, dan status bukti. Kelima butir
   itu ditulis di kepala setiap subbagian fitur.
6. Dilarang menutup laporan dengan tiga kata larangan itu. Bila sesuatu belum tersedia, ditulis
   syarat yang dibutuhkan.
7. Keluaran hanya markdown di folder `planning/`. Dokumen ini satu berkas markdown, tanpa berkas
   .py, .html, .json, atau .csv sebagai deliverable.
8. Semua nama field memakai huruf kecil dan garis bawah, tanpa spasi dan tanpa huruf besar.
9. Semua field waktu di dokumen ini adalah indeks menit internal, bukan tanggal kalender, kecuali
   field yang namanya berakhiran `_utc`. Alasannya di bagian 2 butir 6.

---

## 1. Berkas masukan yang dibuka dan ukuran byte

Ukuran diambil dengan `stat -c '%s'` dan `wc -l` pada 2026-10-31 pukul 18.2x WIB. Keluaran mentahnya
ada di bagian 10.1.

| Kode | Berkas | Byte | Baris | Cara dibuka |
|---|---|---:|---:|---|
| [K] | `planning/01_KATALOG_FITUR.md` | 166.662 | 2.780 | bagian 1 sampai 4 penuh, lalu kepala setiap fitur lewat pencarian baris `Masukan` dan `Keluaran` |
| [DSS1] | `planning/03_SKOR_KEYAKINAN.md` | 66.698 | 1.060 | baris 28 sampai 207 penuh, yaitu bagian 1 sampai 3.5 |
| [DSS2] | `planning/04_ANTREAN_TINJAUAN.md` | 95.168 | 1.428 | baris 150 sampai 269, yaitu bagian 3 dan 4 |
| [J] | `scratch/v9_i1/v9_i1_RESULTS.json` | 57.555 | 1.758 | dibaca lewat `jq` untuk setiap kunci yang dikutip, bukan berurutan dari baris 1 |
| [L] | `docs/RND_PROVENANCE_LEDGER.md` | 471.945 | 3.434 | hanya lewat pencarian baris `PM-078`, `L-21`, `L-22` |
| [V3T] | `docs/V3_TS_FEATURES.md` | 8.429 | 400 | baris 85 sampai 92 |
| [V3A] | `docs/V3_DATA_ACQUISITION_INVENTORY.md` | 17.514 | 626 | hanya lewat kutipan di [K] baris 1517 sampai 1520 |
| [V3W] | `docs/V3_WITSML_PARSE_REPORT.md` | 3.346 | 152 | baris 38 sampai 44 |
| [D0] | `docs/V6_D0_READERS_SYNTHESIS.md` | 19.871 | 700 | hanya lewat kutipan di [K] baris 1521 sampai 1524 |
| [A1] | `docs/V6_A1_DATA_AUDIT.md` | 28.138 | 1.000 | hanya lewat kutipan di [K] baris 517 sampai 520 dan 2548 sampai 2552 |
| [PM6] | `docs/V6_PM_VERDICT.md` | 26.032 | 900 | hanya lewat kutipan di [K] baris 517 sampai 520 |
| [PM7] | `docs/V7_PM_VERDICT.md` | 23.569 | 800 | hanya lewat kutipan di [K] baris 1885 sampai 1888 |
| [S6] | `docs/RND_S6_PM_WAVE2.md` | 40.271 | 1.400 | hanya lewat kutipan di [K] baris 235 sampai 238 dan 1006 sampai 1012 |
| [PM1] | `docs/V9_PM1_ARCHITECTURE.md` | 50.456 | 528 | hanya lewat kutipan di [K] baris 237 sampai 238, 1006 sampai 1012, 1633 sampai 1640 |
| [PM2] | `docs/V9_PM2_VERDICT.md` | 22.654 | 400 | hanya lewat kutipan di [K] baris 2083 sampai 2086 |
| [EVA] | `docs/V9_EVAL_A_LAYERA.md` | 32.713 | 315 | hanya lewat kutipan di [K] baris 381 sampai 386 dan 2161 sampai 2168 |
| [EVB] | `docs/V9_EVAL_B_LAYERB.md` | 30.472 | 300 | hanya lewat kutipan di [K] baris 954 sampai 960 |
| [EVC] | `docs/V9_EVAL_C_LAYERC.md` | 23.153 | 267 | hanya lewat kutipan di [K] baris 1633 sampai 1640 dan [DSS1] baris 116 sampai 126 |
| [Eb] | `docs/V8_E_bit_wear_CAPABILITY.md` | 16.116 | 200 | hanya lewat kutipan di [K] baris 1775 sampai 1778 |
| [ENG] | `docs/RND_ENGINE_S6_INTEGRATION.md` | 3.915 | 120 | hanya lewat kutipan di [K] baris 1110 sampai 1116 |
| [R2] | `docs/RND_R2_STOKASTIK.md` | 28.937 | 600 | hanya lewat kutipan di [K] baris 2161 sampai 2168 |
| [R3] | `docs/RND_R3_VMD_SVM.md` | 32.174 | 700 | hanya lewat kutipan di [K] baris 2464 sampai 2472 |
| [PMR] | `docs/RND_PM_VERDICT.md` | 34.575 | 700 | hanya lewat kutipan di [K] baris 2161 sampai 2168 |
| [VF] | `planning/00_VERIFIKASI_INVENTARIS.md` | 43.536 | 700 | hanya lewat kutipan di [K] baris 517 sampai 520 |
| [I4] | `planning/00_INVENTARIS_RND2_V11.md` | 35.536 | 412 | hanya lewat kutipan di [K] baris 2208 sampai 2216 |
| [NPZ] | `data/predictive/features_timeseries.npz` | 458.129 | bukan teks | daftar isi arsip dibaca dengan `python3 -m zipfile -l`, keluaran di bagian 10.3 |
| [META] | `data/predictive/features_timeseries_meta.json` | 37.307 | 1.100 | dibaca lewat `jq` pada kunci `coverage`, keluaran di bagian 10.4 |
| [DDR] | `data/volve/ddr.parquet` | 2.180.278 | biner | tidak dibaca; angka jam henti dikutip dari [J] `.nilai_maintenance` |

Catatan kejujuran tentang cakupan baca. Berkas [K] tidak dibaca seluruh 2.780 barisnya; yang dibaca
adalah bagian 1 sampai 4 penuh dan kepala 21 fitur terpilih lewat pencarian baris `Masukan` dan
`Keluaran`. Berkas bertanda "hanya lewat kutipan" tidak dibuka langsung oleh dokumen ini: angkanya
diwarisi dari [K] beserta rujukan baris yang tercetak di [K], dan status warisan itu ditulis ulang di
bagian 9.

---

## 2. Cara membaca kontrak ini

Enam butir kesepakatan, dipakai seragam di 21 fitur.

1. Kolom `Wajib` berisi tiga nilai. `wajib` berarti baris ditolak bila field kosong. `opsional`
   berarti field boleh `null` tanpa menurunkan keadaan data. `wajib bila ada` berarti field wajib
   muncul sebagai kunci, tetapi nilainya boleh `null` bila sumber tidak menyediakannya.
2. Tipe `enum` selalu disertai daftar nilai yang diizinkan di sel sumber pada baris yang sama.
   Penambahan nilai enum baru menaikkan versi kontrak di butir 5.
3. Tipe `null` bukan nilai sah untuk field `wajib`. Bila sumber tidak tersedia, field tetap ditulis
   dengan nilai `null` dan satu label teks pendamping pada array `label_kekurangan`, mengikuti pola
   Dynamic Island di [DSS1] baris 151 sampai 153.
4. Satuan ditulis dalam bentuk yang bisa dibaca manusia, dan untuk field rasio selalu ditulis
   `rasio 0..1`, bukan persen, supaya tidak ada pembulatan ganda di dua tempat.
5. Kontrak ini punya nomor versi `1.0.0` pada field `kontrak_versi`. Perubahan yang menaikkan versi
   minor: penambahan field opsional. Perubahan yang menaikkan versi mayor: penghapusan field,
   perubahan satuan, atau perubahan daftar enum.
6. Semua field waktu berbentuk indeks menit internal, bukan tanggal. Dasarnya keluaran `jq` di
   bagian 10.5: `.segmen_info.vib.catatan_waktu` menulis bahwa `ts_bin` adalah indeks menit internal
   dan asal kalender TIDAK diverifikasi. Field yang benar-benar berisi tanggal hanya yang namanya
   berakhiran `_utc`, dan hari ini tidak ada satu pun sumber di [J] yang menyediakannya.

---

## 3. Dua puluh satu fitur prioritas

Pemilihan memakai dua aturan yang bisa diperiksa. Aturan pertama: lima belas fitur teratas katalog
sudah ditulis dengan butir lengkap tanpa butir kosong ([K] baris 213 dan 214), jadi seluruh rumpun
kepercayaan dan lima fitur pertama rumpun perencanaan maintenance masuk. Aturan kedua: setiap rumpun
lain wajib terwakili minimal tiga fitur supaya kontrak muatan per rumpun bisa ditulis utuh, bukan
ditebak. Hasilnya 21 fitur dengan sebaran 4 di kepercayaan, 4 di perencanaan maintenance, 4 di
kualitas data, 3 di perbandingan mesin, 3 di linimasa, 3 di alat bantu insinyur.

| No | ID | Nama | Rumpun | Pengguna utama | Status bukti |
|---:|---|---|---|---|---|
| 1 | KEP-01 | Papan vonis per kelas kerusakan | kepercayaan | insinyur pengeboran, supervisor | siap sekarang |
| 2 | KEP-02 | Skor keyakinan 0 sampai 100 berlapis selang | kepercayaan | insinyur pemeliharaan | siap sebagian |
| 3 | KEP-03 | Badge beban alarm dan pengunci satuan FAR | kepercayaan | operator shift | siap sekarang |
| 4 | KEP-05 | Gerbang provenance angka tiga warna | kepercayaan | penulis laporan, PM | siap sekarang |
| 5 | MNT-01 | Antrean triage onset per shift dengan umur item | perencanaan maintenance | insinyur shift malam, toolpusher | siap sekarang |
| 6 | MNT-02 | Kalkulator anggaran pemeriksaan | perencanaan maintenance | supervisor pemeliharaan | siap sekarang |
| 7 | MNT-03 | Sakelar dua titik operasi hyd | perencanaan maintenance | supervisor shift | siap sekarang |
| 8 | MNT-05 | Penaksir beban tinjauan per shift | perencanaan maintenance | perencana tenaga kerja | siap sebagian |
| 9 | DAT-01 | Kartu kelengkapan jendela pra-event | kualitas data | engineer PdM, supervisor | siap sekarang |
| 10 | DAT-04 | Pemilih kanal berbasis fill rate dan QC fisik | kualitas data | engineer data | siap sebagian |
| 11 | DAT-05 | Matriks ketersediaan berkas per sumur | kualitas data | engineer PdM, peneliti | siap sekarang |
| 12 | DAT-08 | Kartu kesiapan kanal per sumur | kualitas data | engineer instrumentasi | siap sekarang |
| 13 | CMP-01 | Balapan model terhadap baseline persistence | perbandingan mesin | peneliti, dosen penguji | siap sekarang |
| 14 | CMP-02 | Peta kalah-menang per kelas | perbandingan mesin | PM, peneliti | siap sekarang |
| 15 | CMP-04 | Kartu rekam jejak per sumur | perbandingan mesin | auditor, supervisor | siap sekarang |
| 16 | LIN-01 | Log keputusan human-in-loop | linimasa dan jejak keputusan | supervisor, peneliti | siap sebagian |
| 17 | LIN-03 | Penanda selang wajib pada angka FAR dan recall | linimasa dan jejak keputusan | reviewer, operator | siap sebagian |
| 18 | LIN-04 | Register status dokumen vonis | linimasa dan jejak keputusan | auditor, penulis laporan | siap sekarang |
| 19 | INS-03 | Kartu kelayakan sinyal sebelum dekomposisi | alat bantu insinyur | peneliti sinyal | siap sebagian |
| 20 | INS-04 | Kartu kanal yang perlu dipasang | alat bantu insinyur | engineer instrumentasi | siap sebagian |
| 21 | INS-05 | Kartu permintaan data bertanda tangan | alat bantu insinyur | koordinator data, pembimbing | siap sebagian |

Jumlah baris data tabel di atas: 21. Status bukti diwarisi dari [K] bagian 3 baris 136 sampai 183;
status itu status bukti, bukan status prioritas, mengikuti [K] baris 193 sampai 196.

---

## 4. Amplop bersama

Setiap muatan fitur dibungkus amplop yang sama. Amplop ini satu-satunya bagian yang wajib identik di
21 fitur; isi `payload` berbeda per fitur dan ditulis di bagian 5.

| Field | Tipe | Satuan | Sumber | Wajib |
|---|---|---|---|---|
| `kontrak_versi` | string semver | teks | dokumen ini bagian 2 butir 5 | wajib |
| `fitur_id` | enum 21 nilai | teks | [K] bagian 3 baris 136 sampai 183 | wajib |
| `rumpun` | enum `kepercayaan`, `perencanaan_maintenance`, `kualitas_data`, `perbandingan_mesin`, `linimasa`, `alat_bantu` | teks | [K] bagian 3 kolom rumpun | wajib |
| `keadaan_data` | enum `LENGKAP`, `SEBAGIAN`, `KOSONG` | teks | dokumen ini bagian 7 | wajib |
| `label_kekurangan` | array<string> | teks | [DSS1] baris 151 sampai 153 pola Dynamic Island | wajib bila keadaan bukan LENGKAP |
| `skor_keyakinan` | object `nilai`, `pita`, `batas_atas`, `komponen` | rasio 0..1 untuk `nilai` dan `batas_atas` | [DSS1] bagian 3.3 dan 3.4 baris 145 sampai 190 | wajib untuk 14 fitur, lihat bagian 8 |
| `sumber_data` | array<object> `berkas`, `baris`, `byte` | teks, bilangan bulat, byte | berkas yang dibuka pada bagian 1 | wajib |
| `waktu_indeks_menit` | integer atau null | indeks menit | [J] `.segmen_info.<engine>.ts_bin_min` sampai `ts_bin_max` | wajib bila ada |
| `segmen` | enum nama segmen, hari ini `F-14` | teks | [J] `.meta.segmen_rig` | wajib |
| `keputusan_akhir` | string tetap `MANUSIA` | teks | [J] `.keputusan_akhir` dan `.human_review_required` | wajib |
| `dibuat_pada_utc` | string ISO-8601 | detik UTC | jam sistem saat render, bukan dari [J] | wajib |

Tiga aturan amplop yang tidak boleh dilanggar:

Pertama, `keputusan_akhir` tidak boleh berisi nilai selain `MANUSIA`. Nilainya berasal langsung dari
[J] `.keputusan_akhir` yang berbunyi bahwa alat menyiapkan status, peringatan, tren, dan bahan
rencana inspeksi, dan dari `.human_review_required` bernilai `true` (keluaran di bagian 10.6).

Kedua, `sumber_data` wajib memuat minimal satu entri, dan entri itu memuat jalur berkas plus nomor
baris. Baris tanpa `sumber_data` ditolak, mengikuti [K] baris 275 sampai 281 yang menjadikan rujukan
baris sebagai syarat keterbacaan.

Ketiga, `label_kekurangan` tidak boleh berisi kalimat keluhan. Isinya hanya nama field yang kosong
plus sebabnya, dan sebabnya harus salah satu dari tiga nilai: `SUMBER_TIDAK_MENYEDIAKAN`,
`SUMBER_BELUM_DIUKUR`, atau `SUMBER_DI_LUAR_CAKUPAN`. Aturan ini menerjemahkan kerangka butir 4.
---

## 5. Kontrak per rumpun

Setiap fitur ditulis dengan lima butir kepala yang sama, lalu satu tabel field, lalu satu paragraf
perilaku saat data tidak tersedia. Urutan field di tabel adalah urutan tampil di layar, dari kiri ke
kanan.

### 5.1 Rumpun kepercayaan

#### 5.1.1 KEP-01 Papan vonis per kelas kerusakan

- Pengguna: insinyur pengeboran, supervisor shift, dosen penguji, tim website.
- Momen pakai: sebelum mempercayai badge kelas, saat serah terima shift (dua kali per shift) ([K] baris 231 sampai 233).
- Masukan: tabel komposisi per kelas ([S6] bagian 3 baris 148 sampai 159), peta tier ([S6] bagian 3.1 baris 163 sampai 167), komposisi head ([PM2] baris 140 dan 181), gerbang tier ([PM1] baris 138 sampai 139). Semua tabel statis, tanpa masukan pengguna ([K] baris 235 sampai 238).
- Keluaran: sebelas kartu, satu per klaim, tiap kartu memuat nama kelas, tugas satu kalimat, label tier, dua sampai empat angka penopang dengan rujukan, dan daftar syarat menggantung ([K] baris 253 sampai 256).
- Status bukti: siap sekarang, seluruh isi kartu berasal dari tabel yang sudah terbit ([K] baris 271 sampai 273).

| Field | Tipe | Satuan | Sumber | Wajib |
|---|---|---|---|---|
| `kelas` | enum 11 nilai: `vib`, `ssi`, `shk`, `stuck_k1`, `stuck_k2`, `hyd_ki`, `hyd_kii`, `bit_wear_k1`, `bit_wear_k2`, `tool_wear_ki`, `tool_wear_kii` | teks | [J] `.engines[].heads[].klaim` dan [DSS1] baris 129 sampai 139 yang memisahkan K-i dan K-ii | wajib |
| `tugas` | string satu kalimat, maksimum 120 karakter | teks | [J] `.profil_kapabilitas[].klaim_tugas` | wajib |
| `tier` | enum `PERINGATAN-BERPENGAWAS`, `TREN`, `BELUM LAYAK PAKAI` | teks | [J] `.engines[].heads[].tier`, keluaran `jq` di bagian 10.7 | wajib |
| `layer` | enum `L0`, `L1`, `L2`, `L3` | teks | [J] `.engines[].heads[].layer`, [DSS1] baris 119 sampai 122 | wajib |
| `angka_penopang` | array<object> `nama`, `nilai`, `satuan`, `sumber` | campuran, satuannya mengikuti `nama` | [S6] bagian 3 baris 148 sampai 159 dan [PM2] baris 140 | wajib, minimal 2 entri |
| `syarat_menggantung` | array<string> | teks | gerbang [PM1] baris 138 sampai 139, daftar syarat [K] baris 249 sampai 251 | wajib, boleh array kosong |
| `tanggal_potong_data` | string tanggal `YYYY-MM-DD` | teks | [J] `.meta.generated_at` tanggalnya saja | wajib |
| `slot_alarm_otomatis` | integer, hari ini `0` | jumlah slot | [J] `.decision_layer.auto_critical_alarm_slots`, ledger baris 2024 `PM-078` | wajib |

Perilaku saat data tidak tersedia. Tiga sebab yang mungkin. Bila `angka_penopang` kosong untuk satu
kelas, kartu tetap tampil dengan `keadaan_data` bernilai `KOSONG` dan teks `Angka penopang belum
terbit untuk kelas ini, tier ditampilkan tanpa angka`. Bila `tier` tidak ada, kartu tidak boleh
menampilkan label apa pun dan wajib menampilkan `Tier belum ditetapkan`. Bila `slot_alarm_otomatis`
tidak terbaca, field diisi `null` dan kartu menampilkan `Jumlah slot belum terbaca`, bukan angka
nol, karena nol adalah hasil ukur yang sah dan berbeda artinya.

#### 5.1.2 KEP-02 Skor keyakinan 0 sampai 100 berlapis selang

- Pengguna: insinyur pemeliharaan, manajer operasi, auditor.
- Momen pakai: memilih satu peringatan untuk dikerjakan lebih dulu (beberapa kali per shift), menyusun laporan mingguan, memeriksa apakah bobot masih sama ([K] baris 301 sampai 303).
- Masukan: tiga komponen berbobot S_A, S_B, S_C yang berasal dari lift per fold, nilai B1, FAR terukur, dan penilaian C1 sampai C4, delapan baris tabel satu per kelas ([K] baris 305 sampai 308, [I2] bagian 2.3).
- Keluaran: satu bilangan bulat 0 sampai 100, satu pita selang, tiga komponen pecahan dua desimal, satu penanda batas atas dipotong ([K] baris 327 sampai 330).
- Status bukti: siap sebagian, aritmetika delapan baris sudah dihitung ulang ([K] baris 347 sampai 351, [VF] bagian 3.2).

| Field | Tipe | Satuan | Sumber | Wajib |
|---|---|---|---|---|
| `kelas` | enum 8 nilai kelas, bukan 11 klaim | teks | [DSS1] baris 170 sampai 177 | wajib |
| `s_a` | float 0..1, satu desimal nilai pemetaan | rasio 0..1 | [I2] baris 161 sampai 168, aturan pemetaan [K] baris 311 sampai 314 | wajib |
| `s_b` | float 0..1 | rasio 0..1 | [I2] baris 161 sampai 168, aturan pemetaan [K] baris 314 sampai 316 | wajib |
| `s_c` | float 0..1, rata-rata C1 sampai C4 | rasio 0..1 | [I2] baris 161 sampai 168, [K] baris 316 dan 317 | wajib |
| `sk_mentah` | float 0..100, dua desimal | skor 0..100 | rumus `100 x (0,40 S_A + 0,35 S_B + 0,25 S_C)` di [DSS1] baris 158 | wajib |
| `sk_tampil` | integer 0..100 hasil pembulatan `sk_mentah` | skor 0..100 | [I2] baris 161 sampai 168, dicek ulang [DSS1] baris 179 sampai 181 | wajib |
| `selang` | object `bawah`, `atas` | rasio 0..1 | CI95 metrik utama kelas, [DSS1] baris 321 | wajib bila ada |
| `batas_atas` | float 0..1 | rasio 0..1 | potong 70 dari [I4] baris 233 dan [DSS1] baris 163 sampai 166 | wajib |
| `batas_dipotong` | boolean | benar atau salah | perbandingan `sk_tampil` dengan `batas_atas` kali 100 | wajib |
| `status_komponen` | enum `TERUKUR`, `BELUM` | teks | [K] baris 538 sampai 540 yang memakai label yang sama untuk kolom ini | wajib |
| `rumus_versi` | enum `kelas_0,40_0,35_0,25`, `head_W1-03`, `head_F-02` | teks | [DSS1] baris 348 sampai 351 yang mencatat dua rumus hidup bersama | wajib |

Perilaku saat data tidak tersedia. Bila S_B belum terukur, nilainya bukan nol, melainkan 0,20
menurut aturan pemetaan di [K] baris 316, dan kartu wajib mencetak `lapisan B belum terukur` plus
`batas atas 70`. Bila `selang` tidak ada, field tetap ada dengan nilai `null` dan kartu mencetak
`selang belum dihitung untuk kelas ini`, sedangkan angka titik tetap boleh tampil karena angka titik
adalah hasil hitung, bukan tebakan. Bila kedua rumus menghasilkan dua angka berbeda untuk satu head,
kartu wajib menampilkan keduanya bersebelahan beserta `rumus_versi`, mengikuti uji ketiga di [K]
baris 361 sampai 363.

#### 5.1.3 KEP-03 Badge beban alarm dan pengunci satuan FAR

- Pengguna: operator shift.
- Momen pakai: sebelum mempercayai presisi sebuah head, karena presisi tinggi sering dibaca sebagai jarang menyala ([K] baris 367 sampai 370).
- Masukan: FAR per fold, jumlah fold, jumlah alarm palsu, jumlah true positive, satuan yang dipakai, skala waktu domain ([K] baris 381 sampai 386).
- Keluaran: badge berbentuk teks dan angka dengan satuan tertulis ([K] baris 401 sampai 403).
- Status bukti: siap sekarang, angka terukur per head ada di [J] `.engines[].heads[].metrik_segmen`.

| Field | Tipe | Satuan | Sumber | Wajib |
|---|---|---|---|---|
| `head` | string | teks | [J] `.engines[].heads[].head` | wajib |
| `far_nilai` | float | alarm per 24 jam operasi negatif, atau alarm per menit untuk domain bengkel | [J] `.engines[].heads[].metrik_segmen.far_segmen`, contoh `vib.rule_display` 49,942 | wajib |
| `far_satuan` | enum `alarm_per_24jam_negatif`, `alarm_per_menit` | teks | [J] `.engines[].heads[].metrik_segmen.far_unit`, aturan satuan [DSS2] baris 176 sampai 178 | wajib |
| `skala_jendela_detik` | integer, hari ini `60` atau `1` | detik | [J] `.meta` dan [PM1] baris 132 keputusan D-A7 | wajib |
| `fp` | integer | jumlah alarm palsu | [J] `.engines[].heads[].metrik_segmen.fp` | wajib |
| `tp` | integer | jumlah true positive | [J] `.engines[].heads[].metrik_segmen.tp` | wajib |
| `presisi` | float 0..1 | rasio 0..1 | [J] `.engines[].heads[].metrik_segmen.precision` | wajib |
| `recall` | float 0..1 | rasio 0..1 | [J] `.engines[].heads[].metrik_segmen.recall` | wajib |
| `fold_lolos` | integer | jumlah fold | [K] baris 384 sampai 386, [EVA] baris 54 sampai 64 | wajib bila ada |
| `fold_total` | integer | jumlah fold | [K] baris 384 sampai 386 | wajib bila ada |
| `teks_badge` | string maksimum 120 karakter, wajib memuat satuan | teks | [J] `.engines[].heads[].badge_far` | wajib |

Perilaku saat data tidak tersedia. `far_nilai` tanpa `far_satuan` tidak boleh dirender sama sekali,
karena satu angka yang sama bisa berarti 1 atau 1006 tinjauan ([DSS2] baris 177 dan 178). Bila
`fold_lolos` tidak ada, badge mencetak `jumlah fold lolos belum terhitung` dan tetap menampilkan
`fp` serta `tp`, karena keduanya hasil ukur langsung. Bila `presisi` ada tetapi `recall` tidak ada,
badge hanya mencetak presisi dan menambahkan label `recall belum tersedia`, bukan mencetak nol.

#### 5.1.4 KEP-05 Gerbang provenance angka tiga warna

- Pengguna: penulis laporan, PM.
- Momen pakai: saat memasukkan satu angka ke laporan atau ke slide, sebelum angka itu dikutip ([K] baris 503 sampai 505).
- Masukan: daftar temuan audit berisi lima angka tidak akurat, tiga angka tidak tereproduksi, satu label sirkular penuh ([A1] baris 248 sampai 264), daftar larangan kutip enam kelompok ([PM6] baris 188 sampai 190), hasil verifikasi 40 uji ([VF] bagian 3.5) ([K] baris 517 sampai 520).
- Keluaran: tabel angka dengan kolom angka, klaim, berkas, baris, status warna, dan perintah hitung ulang ([K] baris 536 sampai 540).
- Status bukti: siap sekarang, 40 uji pada empat inventaris memberi 37 cocok, 2 cocok dengan catatan, 1 tidak cocok ([VF] bagian 3.5).

| Field | Tipe | Satuan | Sumber | Wajib |
|---|---|---|---|---|
| `angka` | string, angka apa adanya termasuk desimal koma | teks | [K] baris 536 | wajib |
| `klaim` | enum 11 nilai kelas | teks | [K] bagian 3 baris 136 sampai 183 | wajib |
| `berkas` | string jalur relatif dari akar proyek | teks | [K] baris 536 dan tabel sumber bagian 2 katalog | wajib |
| `baris` | integer atau null | nomor baris | [K] baris 536 | wajib |
| `status_warna` | enum `HIJAU`, `KUNING`, `MERAH` | teks | aturan tiga warna [K] baris 521 sampai 526 | wajib |
| `perintah_hitung_ulang` | string perintah, boleh kosong untuk HIJAU | teks | [K] baris 536 | wajib untuk KUNING dan MERAH |
| `alasan_warna` | string satu kalimat | teks | [K] baris 521 sampai 526 | wajib |
| `skor_keyakinan_kelas` | integer 0..100 atau null | skor 0..100 | [K] baris 538 sampai 540 | wajib bila ada |
| `label_sumber` | enum `TERUKUR`, `BELUM` | teks | [K] baris 539 dan 540 | wajib |

Perilaku saat data tidak tersedia. Bila `baris` kosong, warna tertinggi yang boleh diberikan adalah
KUNING, mengikuti definisi HIJAU yang mensyaratkan rujukan berkas dan baris ([K] baris 521 sampai
526). Bila `skor_keyakinan_kelas` belum final, kolom itu menampilkan label `TERUKUR` atau `BELUM`,
bukan angka kosong ([K] baris 538 sampai 540). Bila angka tidak ditemukan di berkas yang disebut,
statusnya MERAH dan `perintah_hitung_ulang` wajib terisi perintah yang bisa dijalankan ulang.

### 5.2 Rumpun perencanaan maintenance

#### 5.2.1 MNT-01 Antrean triage onset per shift dengan umur item

- Pengguna: insinyur shift malam, toolpusher.
- Momen pakai: awal shift, saat menyusun urutan pemeriksaan dari peringatan yang masuk semalam ([K] baris 873 sampai 876).
- Masukan: skor ranking per jendela, horizon H, riwayat alarm pada horizon itu, ambang terpilih per sumur, cap waktu masuk antrean ([K] baris 887 sampai 893).
- Keluaran: tabel berurut dengan pengenal jendela, sumur, waktu jendela, skor, skor keyakinan, cakupan, TLead, umur item, aksi ([K] baris 906 sampai 910).
- Status bukti: siap sekarang untuk kolom skor dan cakupan, siap sebagian untuk kolom sumur karena peta jendela ke sumur belum ada ([DSS2] baris 179 sampai 181).

| Field | Tipe | Satuan | Sumber | Wajib |
|---|---|---|---|---|
| `id_baris` | string bentuk `klaim` lalu `jendela`, contoh `hyd K-i 20` | teks | [DSS2] baris 157 | wajib |
| `sumur` | string atau null | teks | [J] `.segmen_info` hanya memberi segmen per engine, bukan peta sumur per jendela ([DSS2] baris 179 sampai 181) | opsional |
| `waktu_indeks_menit` | integer 0 sampai 95.924 | indeks menit | [J] baris 618, [DSS2] baris 158 | wajib |
| `skor` | float 0..1 | rasio 0..1 | [K] baris 888 sampai 892 | wajib |
| `skor_keyakinan` | integer 0..100 | skor 0..100 | [DSS1] baris 170 sampai 177 | wajib |
| `cakupan` | float 0..1 | rasio 0..1 | [K] baris 907 sampai 909, rentang terukur 0,004 sampai 0,115 | wajib |
| `tlead_menit` | float atau null | menit | hanya hyd, [J] `.profil_kapabilitas[4].lapisan_B_nilai_maintenance.lead_menit` bernilai 8,0 (bagian 10.8) | wajib bila ada |
| `umur_menit` | integer | menit, batas bawah | [DSS2] baris 167 | wajib |
| `aksi` | enum `konfirmasi_lapangan`, `periksa_kanal`, `pantau`, `tutup` | teks | [DSS2] baris 170 | wajib |
| `segmen` | enum `F-14` | teks | [J] `.meta.segmen_rig` | wajib |

Perilaku saat data tidak tersedia. `sumur` diisi `null` dan baris tetap tampil dengan `segmen`
bernilai `F-14`, karena menulis nama sumur per baris hari ini akan menjadi tebakan ([DSS2] baris
179 sampai 181). `tlead_menit` diisi `null` dan baris mencetak `tidak tersedia`, bukan nol, karena
hanya satu head yang punya lead terukur ([DSS2] baris 182 sampai 185). Bila `skor_keyakinan` di
bawah 40, baris ditandai `tinjauan pendamping` dan `aksi` tidak boleh bernilai
`konfirmasi_lapangan` ([K] baris 908 sampai 910).

#### 5.2.2 MNT-02 Kalkulator anggaran pemeriksaan

- Pengguna: supervisor pemeliharaan.
- Momen pakai: saat memutuskan titik operasi mana yang dipakai pada shift berikutnya, satu kali per shift ([K] baris 941 sampai 944).
- Masukan: jumlah alarm palsu engine, jumlah alarm palsu baseline status quo, recall pada titik yang sama ([K] baris 954 sampai 960).
- Keluaran: dua angka persen per titik, penghematan pemeriksaan dan deteksi yang hilang, masing masing dengan rentang antar fold, ditambah skor keyakinan per titik ([K] baris 968 sampai 972).
- Status bukti: siap sekarang untuk aritmetika, siap sebagian untuk dasar pemilihan titik.

| Field | Tipe | Satuan | Sumber | Wajib |
|---|---|---|---|---|
| `titik_operasi` | enum `tau_0,5`, `tau_terpilih`, `pembanding_lama` | teks | [K] baris 956 sampai 960 | wajib |
| `fp_engine` | integer | jumlah alarm palsu | [K] baris 957, [EVB] baris 98 sampai 106 | wajib |
| `fp_baseline` | integer | jumlah alarm palsu | [K] baris 956, [EVB] baris 65 | wajib |
| `recall_titik` | float 0..1 | rasio 0..1 | [K] baris 958, [EVA] baris 55 | wajib |
| `penghematan_persen` | float 0..1 | rasio 0..1 dari rumus satu kurang `fp_engine` bagi `fp_baseline` | [EVB] baris 65 | wajib |
| `deteksi_hilang_persen` | float 0..1 | rasio 0..1 | turunan dari `recall_titik`, [K] baris 968 sampai 972 | wajib |
| `rentang_fold` | object `min`, `max` | rasio 0..1 | [K] baris 968 sampai 972 | wajib bila ada |
| `skor_keyakinan` | integer 0..100 | skor 0..100 | [DSS1] baris 170 sampai 177 | wajib |

Perilaku saat data tidak tersedia. Bila `fp_baseline` nol, `penghematan_persen` diisi `null` dan
kartu mencetak `pembagi nol, penghematan belum bisa dihitung`, karena pembagian dengan nol bukan
penghematan penuh. Bila `rentang_fold` kosong, kartu tetap menampilkan angka titik dengan label
`rentang antar fold belum terkumpul`. Bila `recall_titik` di bawah 0,10, kartu wajib menampilkan
kalimat tukar yang eksplisit, mengikuti contoh ssi dengan penghematan 0,731 tetapi recall 0,03
([K] baris 959 dan 960).

#### 5.2.3 MNT-03 Sakelar dua titik operasi hyd

- Pengguna: supervisor shift.
- Momen pakai: saat memilih komposisi pemicu untuk kelas hyd, sebelum shift dimulai ([K] baris 995 sampai 998).
- Masukan: dua keluaran engine yang sudah ada, dengan angka per fold ([K] baris 1006 sampai 1012).
- Keluaran: tabel enam kolom untuk tiga baris, titik pertama, titik kedua, pembanding lama, plus satu baris biaya perpindahan ([K] baris 1024 sampai 1028).
- Status bukti: siap sekarang, seluruh angka ada di [S6] baris 194, 196, dan 197.

| Field | Tipe | Satuan | Sumber | Wajib |
|---|---|---|---|---|
| `titik` | enum `titik_1`, `titik_2`, `pembanding_lama` | teks | [S6] baris 194, 196, 197 | wajib |
| `komposisi` | string, daftar pemicu yang aktif | teks | [K] baris 1007 sampai 1012 | wajib |
| `fp` | integer, 927 / 568 / 935 | jumlah alarm palsu | [S6] baris 196, 197, 194 | wajib |
| `tp` | integer, 4.924 / 3.557 / 3.804 | jumlah true positive | [S6] baris 196, 197, 194 | wajib |
| `presisi` | float 0..1, 0,8243 / 0,8646 / 0,7789 | rasio 0..1 | [S6] baris 196, 197, 194 | wajib |
| `recall` | float 0..1, 0,6519 / 0,5296 / 0,5638 | rasio 0..1 | [S6] baris 196, 197, 194 | wajib |
| `far_median` | float, 4,0984 / 2,0323 / 3,5302 | alarm per 24 jam operasi negatif | [S6] baris 196, 197, 194 | wajib |
| `lead_menit` | float, 8,0 / 12,5 / 11,5 | menit | [S6] baris 196, 197, 194, [J] `.profil_kapabilitas[4]` lead 8,0 untuk titik pertama | wajib |
| `fold_lolos_far` | integer | jumlah fold | [S6] baris 196 dan 197, 7 dari 9 dan 9 dari 9 | wajib |
| `fold_lolos_recall` | integer | jumlah fold | [S6] baris 196 dan 197, 7 dari 9 dan 5 dari 9 | wajib |
| `biaya_perpindahan` | string, dampak yang hilang saat pindah titik | teks | [K] baris 1024 dan 1025 | wajib |

Perilaku saat data tidak tersedia. Bila satu baris tidak punya `fold_lolos_recall`, sel itu diisi
`null` dan tabel mencetak `belum dihitung per fold`, sedangkan `far_median` dan `lead_menit` tetap
tampil. Bila `lead_menit` tidak ada pada satu titik, kolom itu mencetak `tidak tersedia` dan
`biaya_perpindahan` wajib menyebut bahwa pembandingan lead tidak lengkap. Nilai pecahan wajib
ditulis dengan koma desimal seperti di sumber, supaya pembaca bisa mencocokkan langsung dengan
baris [S6].

#### 5.2.4 MNT-05 Penaksir beban tinjauan per shift

- Pengguna: perencana tenaga kerja.
- Momen pakai: saat menyusun jadwal tinjauan per shift dan saat menambah satu head baru ([K] baris 1101 sampai 1104).
- Masukan: FAR per 24 jam per head dari [ENG] baris 31 sampai 43, dan label segmen sumber angka ([K] baris 1110 sampai 1113).
- Keluaran: enam angka tinjauan per shift dengan label `angka segmen F-14, bukan median lintas fold` ([K] baris 1119 sampai 1121).
- Status bukti: siap sebagian, angka per head ada, angka lintas fold belum ada.

| Field | Tipe | Satuan | Sumber | Wajib |
|---|---|---|---|---|
| `head` | string bentuk `engine.head` | teks | [J] `.nilai_maintenance.beban_tinjauan_L1[].head` | wajib |
| `far_per_24jam` | float | alarm per 24 jam operasi negatif | [J] `.nilai_maintenance.beban_tinjauan_L1[].far_per_24jam` | wajib |
| `tinjauan_per_shift_8jam` | integer | tinjauan per shift 8 jam | [J] `.nilai_maintenance.beban_tinjauan_L1[].tinjauan_per_shift_8jam`, [ENG] baris 31 sampai 43 | wajib |
| `metode_bagi` | integer tetap `3` | pembagi | [K] baris 1113 | wajib |
| `segmen` | enum `F-14` | teks | [J] `.meta.segmen_rig` | wajib |
| `label_skala` | string tetap `angka segmen F-14, bukan median lintas fold` | teks | [K] baris 1119 dan 1120 | wajib |
| `sumber_baris` | string nomor baris [ENG] | teks | [ENG] baris 31 sampai 43 | wajib |

Perilaku saat data tidak tersedia. Bila satu head bernilai nol, misalnya ssi dengan FAR 0,0
(keluaran bagian 10.9), baris itu tetap tampil dengan angka 0 dan label `nol tinjauan pada segmen
ini`, bukan dihilangkan, karena nol adalah hasil ukur. Bila sebuah head belum punya FAR terukur,
barisnya tampil dengan `tinjauan_per_shift_8jam` bernilai `null` dan label `FAR belum terukur`.
Bila label segmen hilang, seluruh tabel ditolak render, karena angka tanpa label segmen akan dibaca
sebagai median lintas sumur.
### 5.3 Rumpun kualitas data

#### 5.3.1 DAT-01 Kartu kelengkapan jendela pra-event

- Pengguna: engineer PdM, supervisor pengeboran.
- Momen pakai: saat membuka satu event atau satu baris riwayat, sebelum skor model dibaca ([K] baris 1326 sampai 1329).
- Masukan: metadata jendela per event berisi jumlah baris, gap median dalam detik, gap maksimum, dan penanda jendela penuh, semuanya di `X_window_meta` pada [NPZ] berukuran 458.129 byte ([K] baris 1338 sampai 1341, [V3T] baris 89).
- Keluaran: empat label kelengkapan penuh, sebagian, kosong, terpotong, plus jumlah baris dan gap terbesar ([K] baris 1358 sampai 1362).
- Status bukti: siap sekarang, median gap 4,9 detik dan median baris 379, 1.515, 4.549 terverifikasi dokumen ([V3T] baris 89).

| Field | Tipe | Satuan | Sumber | Wajib |
|---|---|---|---|---|
| `event_id` | string | teks | [NPZ] larik `event_id.npy` 5.416 byte, daftar isi di bagian 10.3 | wajib |
| `n_rows` | integer | jumlah baris | [NPZ] `X_window_meta` kolom `n_rows`, [V3T] baris 89 | wajib |
| `gap_median_s` | float | detik | [NPZ] `X_window_meta` kolom `gap_median_s`, [V3T] baris 89 | wajib |
| `gap_max_s` | float | detik | [NPZ] `X_window_meta` kolom `gap_max_s`, [V3T] baris 89 | wajib |
| `full_window` | boolean | benar atau salah | [NPZ] `X_window_meta` kolom `full_window`, [V3T] baris 89 | wajib |
| `label_kelengkapan` | enum `penuh`, `sebagian`, `kosong`, `terpotong` | teks | [K] baris 1358 | wajib |
| `fraksi_nan_sensor` | float 0..1 | rasio 0..1 | [V3T] baris 109 lewat [K] baris 1345, nilai acuan 0,368 pada jendela 2 jam | wajib bila ada |
| `panjang_jendela_menit` | enum `30`, `120`, `360` | menit | [V3T] baris 89 lewat [K] baris 1343 dan 1344 | wajib |
| `skor_keyakinan` | integer 0..100 | skor 0..100 | [K] baris 1359 dan 1360 | wajib |

Perilaku saat data tidak tersedia. Bila ketiga kolom gap kosong tetapi `n_rows` ada, label yang sah
adalah `terpotong` dan kartu mencetak `gap tidak tercatat`. Bila seluruh baris `X_window_meta` untuk
satu event tidak ada, kartu tampil dengan `keadaan_data` `KOSONG` dan teks `Metadata jendela tidak
ada untuk event ini, skor tidak ditampilkan`. Jumlah event yang seluruh fiturnya kosong sudah
terukur: 194 pada jendela 30 menit, 191 pada 2 jam, dan 185 pada 6 jam ([K] baris 1344 dan 1345),
sehingga keadaan kosong ini keadaan nyata yang harus punya tampilan, bukan keadaan teoretis.

#### 5.3.2 DAT-04 Pemilih kanal berbasis fill rate dan QC fisik

- Pengguna: engineer data.
- Momen pakai: saat memilih daftar kanal untuk satu fold atau satu sumur baru ([K] baris 1470 sampai 1473).
- Masukan: fill rate per kanal per sumur, daftar kanal per fold, penanda konstansi ([K] baris 1478 sampai 1480).
- Keluaran: daftar kanal lolos beserta alasan, dan daftar gugur beserta fill rate ([K] baris 1488 sampai 1490).
- Status bukti: siap sebagian, ambang 50 persen sudah terukur dasarnya, validasi satuan belum.

| Field | Tipe | Satuan | Sumber | Wajib |
|---|---|---|---|---|
| `kanal` | string, nama kanal WITSML | teks | [V3T] baris 65 sampai 68, [K] baris 1482 dan 1483 | wajib |
| `sumur` | string | teks | [V3W] baris 41, rentang 60 sampai 281 kanal per sumur | wajib |
| `fill_rate` | float 0..1 | rasio 0..1 | [V3W] baris 41, [K] baris 1479 | wajib |
| `ambang_fill` | float tetap `0,50` | rasio 0..1 | [V3W] baris 41, alasan di [K] baris 1482 | wajib |
| `trend_rho` | float atau null | koefisien korelasi | [K] baris 1483, kanal dengan nilai NaN ditandai konstan | wajib bila ada |
| `kanal_konstan` | boolean | benar atau salah | [K] baris 1483 | wajib |
| `status` | enum `lolos`, `gugur` | teks | [K] baris 1488 | wajib |
| `alasan` | string satu kalimat | teks | [K] baris 1482 dan 1488 | wajib |
| `jumlah_fold_tersedia` | integer 0..7 | jumlah fold | [K] baris 1483 dan 1484 | wajib bila ada |

Perilaku saat data tidak tersedia. Bila `trend_rho` tidak ada, `kanal_konstan` diisi `null` dan
status tertinggi yang boleh diberikan adalah `lolos bersyarat`, bukan `lolos`, karena uji konstansi
belum dijalankan. Bila `fill_rate` kosong untuk satu kanal, kanal masuk daftar gugur dengan alasan
`fill rate belum dihitung` dan bukan dengan fill rate nol, sebab nol berarti kanal terukur kosong.
Angka pendukung yang wajib tampil di kaki daftar: 15 kanal kanonik dipakai, 14 tersedia di 7 dari 7
fold, RPM 6 dari 7, MDOA 5 dari 7 ([K] baris 1483 dan 1484).

#### 5.3.3 DAT-05 Matriks ketersediaan berkas per sumur

- Pengguna: engineer PdM, peneliti.
- Momen pakai: saat memutuskan sumur mana yang bisa dievaluasi dan sumur mana yang perlu unduh tambahan ([K] baris 1509 sampai 1512).
- Masukan: audit unduhan 17.368 berkas 3,32 GB dengan hilang nol, 11.894 berkas WITSML untuk 27 wellbore, 5.474 berkas teknis, 20.086 entri zip ([V3A] baris 182 sampai 185 lewat [K] baris 1517 sampai 1520).
- Keluaran: kartu per sumur berisi jumlah berkas per kategori dan status ([K] baris 1527 sampai 1530).
- Status bukti: siap sekarang untuk hitungan berkas, siap sebagian untuk pemetaan kanal label per sumur.

| Field | Tipe | Satuan | Sumber | Wajib |
|---|---|---|---|---|
| `sumur` | string, 27 wellbore | teks | [V3A] baris 182 sampai 185 | wajib |
| `kategori_berkas` | enum `witsml`, `teknis`, `zip`, `lain` | teks | [V3A] baris 182 sampai 185 | wajib |
| `jumlah_berkas` | integer | jumlah berkas | [V3A] baris 182 sampai 185, contoh F-1 C 2.156 dan F-11 1.750 ([D0] baris 49) | wajib |
| `punya_kanal_label` | boolean | benar atau salah | [D0] baris 17 sampai 22, [K] baris 1521 sampai 1524 | wajib |
| `status` | enum `siap`, `perlu_unduh` | teks | [K] baris 1527 sampai 1530 | wajib |
| `total_berkas_audit` | integer tetap `17.368` | jumlah berkas | [V3A] baris 182 | wajib |
| `total_byte_audit` | float `3,32` | gigabyte | [V3A] baris 182 | wajib |
| `hilang` | integer tetap `0` | jumlah berkas | [V3A] baris 182 | wajib |

Perilaku saat data tidak tersedia. Bila `punya_kanal_label` belum dipetakan untuk satu sumur, sel
itu diisi `null` dan statusnya `siap diparse`, bukan `siap`, karena siap diparse dan siap dievaluasi
dua keadaan berbeda ([K] baris 1527 sampai 1530). Bila `jumlah_berkas` nol, kartu tetap tampil dan
mencetak `tidak ada berkas pada audit`, karena nol di audit adalah hasil ukur dengan hilang nol
([V3A] baris 182). Matriks tidak boleh mewarnai sel kosong sebagai merah tanpa label, mengikuti
aturan [K] baris 206 sampai 208.

#### 5.3.4 DAT-08 Kartu kesiapan kanal per sumur

- Pengguna: engineer instrumentasi.
- Momen pakai: saat menyalakan panel peringatan pada satu sumur atau satu engine ([K] baris 1622 sampai 1625).
- Masukan: daftar kanal per engine, jumlah baris terisi dan kosong per kanal per sumur, jumlah berkas per kanal ([K] baris 1633 sampai 1637).
- Keluaran: kartu per sumur dengan baris per kanal berisi nama kanal, persen kosong, jumlah berkas, status, aksi ([K] baris 1650 sampai 1653).
- Status bukti: siap sekarang, angka kosong per kanal sudah terukur di [EVC] baris 121 dan 136.

| Field | Tipe | Satuan | Sumber | Wajib |
|---|---|---|---|---|
| `kanal` | string | teks | [EVC] baris 121 dan 136, [K] baris 1633 | wajib |
| `sumur` | string | teks | [EVC] baris 121, contoh F-14 | wajib |
| `baris_kosong` | integer | jumlah baris | [EVC] baris 121, contoh 356 dari 1.989 untuk VIBLAT | wajib |
| `baris_total` | integer | jumlah baris | [EVC] baris 121, contoh 1.989 | wajib |
| `persen_kosong` | float 0..1 | rasio 0..1 | hitungan dari dua field di atas, contoh 62,3 persen pada CRPM ([EVC] baris 136) | wajib |
| `jumlah_berkas` | integer | jumlah berkas | [K] baris 1650 | wajib |
| `status` | enum `siap`, `bersyarat`, `belum` | teks | ambang [K] baris 1640 sampai 1644 dan [PM1] baris 139 | wajib |
| `aksi` | string satu kalimat | teks | [K] baris 1650 sampai 1653 | wajib |
| `ambang_siap` | float tetap `0,20` | rasio 0..1 | [PM1] baris 139 lewat [K] baris 1642 dan 1643 | wajib |

Perilaku saat data tidak tersedia. Bila `baris_total` nol, `persen_kosong` diisi `null`, bukan
100 persen, dan statusnya `belum` dengan aksi `periksa berkas kanal`. Bila `jumlah_berkas` nol,
status langsung `belum` tanpa menghitung persen. Status `bersyarat` mewajibkan badge menyebut kanal
yang bolong ([K] baris 1650 sampai 1653). Ketersediaan kanal lintas sumur wajib dicetak apa adanya,
contoh VIBLAT tersedia di 6 dari 10 sumur, dengan koreksi dari angka 7 sumur pada ringkasan lama
([I1] baris 245 dan 250 lewat [K] baris 1636 dan 1637).

### 5.4 Rumpun perbandingan mesin

#### 5.4.1 CMP-01 Balapan model terhadap baseline persistence

- Pengguna: peneliti, dosen penguji.
- Momen pakai: saat memeriksa apakah model mengalahkan baseline pada satu kelas dan satu varian target ([K] baris 1766 sampai 1769).
- Masukan: AUPRC per fold dari baseline persistence dan dari model, per kelas dan per varian target ([K] baris 1775 sampai 1777).
- Keluaran: grafik berpasangan per fold dengan garis penghubung, plus median kedua metode ([K] baris 1784 sampai 1787).
- Status bukti: siap sekarang, angka AUPRC per fold ada di [Eb].

| Field | Tipe | Satuan | Sumber | Wajib |
|---|---|---|---|---|
| `kelas` | enum nama kelas | teks | [Eb] baris 88 lewat [K] baris 1778 | wajib |
| `varian_target` | string | teks | [K] baris 1775 | wajib |
| `fold` | integer atau string kode fold | teks | [Eb] baris 88 | wajib |
| `auprc_baseline` | float 0..1, rentang terukur 0,6376 sampai 0,9723 | rasio 0..1 | [Eb] baris 88 | wajib |
| `auprc_model` | float 0..1 | rasio 0..1 | [Eb] baris 88 | wajib |
| `selisih` | float, `auprc_model` kurang `auprc_baseline` | rasio 0..1 | turunan, arah kalah dicatat [Eb] baris 88 | wajib |
| `median_baseline` | float, 0,9038 | rasio 0..1 | [Eb] baris 88 | wajib |
| `median_model` | float, 0,8374 | rasio 0..1 | [Eb] baris 88 | wajib |
| `jumlah_fold_kalah` | integer, 100 dari 100 jawaban | jumlah fold | [Eb] baris 88 | wajib |
| `jumlah_fold` | integer | jumlah fold | [Eb] baris 88 | wajib |

Perilaku saat data tidak tersedia. Bila `auprc_model` kosong pada satu fold, pasangan itu tidak
digambar sebagai garis dan fold ditandai `fold tanpa hasil model`; nilai kosong tidak boleh diganti
median, karena median adalah ringkasan, bukan hasil fold. Bila `median_baseline` tidak ada tetapi
fold lengkap, median dihitung dari fold dan field sumbernya ditulis `dihitung dari fold`. Kartu
wajib mencetak jumlah fold yang dibandingkan di sebelah median, supaya pembaca tahu penyebutnya.

#### 5.4.2 CMP-02 Peta kalah-menang per kelas

- Pengguna: PM, peneliti.
- Momen pakai: saat menyusun ringkasan hasil per kelas, sekali per laporan ([K] baris 1804 sampai 1807).
- Masukan: AUPRC per fold per kelas untuk model dan pembandingnya ([K] baris 1812 sampai 1814).
- Keluaran: tabel kelas dengan jumlah fold menang, selisih median, dan nama pembanding ([K] baris 1821 sampai 1824).
- Status bukti: siap sekarang, angka menang per kelas ada di [E1] baris 119 lewat [K] baris 1815 dan 1816.

| Field | Tipe | Satuan | Sumber | Wajib |
|---|---|---|---|---|
| `kelas` | enum nama kelas | teks | [E1] baris 119 lewat [K] baris 1815 | wajib |
| `pembanding` | string, nama pembanding per kelas | teks | [K] baris 1821 sampai 1824 | wajib |
| `fold_menang` | integer, contoh hyd 5, ssi 4, tool_wear 7, vib 4 | jumlah fold | [E1] baris 119 lewat [K] baris 1815 dan 1816 | wajib |
| `fold_total` | integer, contoh hyd 7, ssi 5 | jumlah fold | [E1] baris 119 lewat [K] baris 1815 | wajib |
| `median_auprc` | float 0..1, contoh hyd 0,6538 | rasio 0..1 | [E1] baris 119 lewat [K] baris 1815 | wajib |
| `selisih_median` | float | rasio 0..1 | [K] baris 1817 | wajib |
| `catatan_pembanding` | string, alasan pembanding tidak seragam | teks | [K] baris 1822 dan 1823 | wajib |

Perilaku saat data tidak tersedia. Karena pembanding tidak seragam antar kelas ([K] baris 1822 dan
1823), `pembanding` wajib terisi untuk setiap baris; baris tanpa nama pembanding ditolak render.
Bila `fold_total` kosong, `fold_menang` tidak boleh ditampilkan sendirian, karena 5 dari 7 dan 5 dari
5 dua arti berbeda. Bila satu kelas belum punya pembanding, baris tampil dengan teks `pembanding
belum ditetapkan` dan kolom menang diisi `null`.

#### 5.4.3 CMP-04 Kartu rekam jejak per sumur

- Pengguna: auditor, supervisor.
- Momen pakai: saat memeriksa apakah satu sumur cukup berdaya untuk dipakai menilai model ([K] baris 1877 sampai 1880).
- Masukan: jumlah positif per sumur dan per kelas ([K] baris 1885 sampai 1887).
- Keluaran: daftar sumur dengan jumlah positif dan status daya ([K] baris 1894 sampai 1896).
- Status bukti: siap sekarang untuk hitungan positif, siap sebagian untuk tautan ke peta daya penuh.

| Field | Tipe | Satuan | Sumber | Wajib |
|---|---|---|---|---|
| `sumur` | string | teks | [PM7] baris 141 lewat [K] baris 1891 | wajib |
| `kelas` | enum nama kelas | teks | [K] baris 1885 | wajib |
| `jumlah_positif` | integer, contoh shk F-10 798 dan F-12 580 | jumlah event | [PM7] baris 141 lewat [K] baris 1891 | wajib |
| `ambang_daya` | integer tetap `30` | jumlah event | [I1] baris 350 lewat [K] baris 1892 | wajib |
| `status_daya` | enum `berdaya`, `kurang_berdaya` | teks | aturan UNDERPOWERED [I1] baris 350 lewat [K] baris 1892 | wajib |
| `tautan_peta_daya` | string kode fitur `MNT-09` | teks | [K] baris 1893 | wajib |
| `catatan` | string | teks | [K] baris 1891 yang mencatat hanya dua sumur punya positif nyata untuk shk | wajib |

Perilaku saat data tidak tersedia. Bila `jumlah_positif` nol untuk satu sumur, statusnya
`kurang_berdaya` dan kartu mencetak `nol positif tercatat`, bukan menghapus sumur dari daftar, sebab
sumur tanpa positif tetap bagian dari rekam jejak. Bila satu kelas belum punya hitungan per sumur,
baris kelas itu tidak ditampilkan dan kartu mencetak `hitungan positif per sumur belum tersedia
untuk kelas ini`.

### 5.5 Rumpun linimasa dan jejak keputusan

#### 5.5.1 LIN-01 Log keputusan human-in-loop

- Pengguna: supervisor, peneliti.
- Momen pakai: setiap kali satu peringatan ditutup atau ditunda, dan saat meninjau riwayat keputusan ([K] baris 2073 sampai 2076).
- Masukan: identitas head, skor keyakinan, badge beban alarm, tindakan yang diambil, dan alasan singkat; aturan tinjauan manusia berlaku pada 11 dari 11 head L1 ([PM2] baris 205 lewat [K] baris 2083 sampai 2086).
- Keluaran: riwayat keputusan per head, tingkat tindak lanjut, dan daftar peringatan terbuka ([K] baris 2095 sampai 2098).
- Status bukti: siap sebagian, aturan wajibnya siap, penyimpanan label belum.

| Field | Tipe | Satuan | Sumber | Wajib |
|---|---|---|---|---|
| `peringatan_id` | string bentuk `engine.head.waktu` | teks | [J] `.decision_layer.layers.L1[]` (`engine`, `head`) dan `.engines[].heads[].contoh_idx_aktif` | wajib |
| `head` | string | teks | [J] `.decision_layer.layers.L1[].head`, 11 entri (bagian 10.6) | wajib |
| `skor_keyakinan` | integer 0..100 | skor 0..100 | [DSS1] baris 170 sampai 177 | wajib |
| `badge_far` | string dengan satuan | teks | [J] `.engines[].heads[].badge_far` | wajib |
| `tindakan` | enum `konfirmasi_lapangan`, `periksa_kanal`, `pantau`, `tutup` | teks | [DSS2] baris 170, [K] baris 2084 | wajib |
| `alasan` | string satu kalimat, wajib terisi | teks | [K] baris 2084, aturan [DSS2] baris 174 sampai 176 | wajib |
| `waktu_keputusan_utc` | string ISO-8601 | detik UTC | jam sistem saat keputusan disimpan, bukan dari [J] | wajib |
| `peninjau` | string identitas manusia | teks | [J] `.human_review_required` `true` (bagian 10.6) | wajib |
| `terbuka` | boolean | benar atau salah | [K] baris 2090 dan 2091, peringatan tanpa label dihitung terbuka | wajib |
| `tingkat_tindak_lanjut` | float 0..1 | rasio 0..1 | [K] baris 2092 dan 2093, jumlah berlabel dibagi jumlah tampil | wajib |

Perilaku saat data tidak tersedia. Peringatan tanpa label dihitung terbuka, bukan benar ([K] baris
2090 dan 2091). Bila `alasan` kosong, baris log ditolak simpan, karena satu label keputusan tanpa
alasan tidak bisa diaudit. Bila `peninjau` kosong, `tindakan` tidak boleh bernilai `tutup` dan
`terbuka` tetap `true`.

#### 5.5.2 LIN-03 Penanda selang wajib pada angka FAR dan recall

- Pengguna: reviewer, operator.
- Momen pakai: saat membaca satu angka FAR atau recall pada laporan atau panel ([K] baris 2149 sampai 2152).
- Masukan: jumlah iterasi bootstrap, seed, blok bootstrap, cakupan waktu, ditambah angka titik per fold; aturan Monte Carlo wajib dilaporkan ([PMR] baris 99 dan 149 lewat [K] baris 2161 sampai 2164).
- Keluaran: tiga angka per sel, titik, batas bawah, batas atas, plus penanda ([K] baris 2175 sampai 2177).
- Status bukti: siap sebagian, aturan dan contoh ada, hitungan selang untuk semua sel belum.

| Field | Tipe | Satuan | Sumber | Wajib |
|---|---|---|---|---|
| `angka_titik` | float | satuan angka induk, FAR per 24 jam atau rasio 0..1 | [K] baris 2161 | wajib |
| `batas_bawah` | float | satuan angka induk | [R2] baris 123 sampai 140 lewat [K] baris 2165 | wajib |
| `batas_atas` | float | satuan angka induk | [R2] baris 123 sampai 140 lewat [K] baris 2165 | wajib |
| `iterasi_bootstrap` | integer | jumlah iterasi | [R2] baris 123 sampai 140 | wajib |
| `seed` | integer | benih | [R2] baris 123 sampai 140 | wajib |
| `blok_bootstrap` | integer | jumlah sampel per blok | [R2] baris 123 sampai 140 | wajib |
| `cakupan_waktu` | string | teks rentang | [R2] baris 123 sampai 140 | wajib |
| `prevalensi` | float 0..1 | rasio 0..1 | [K] baris 2168 | wajib bila ada |
| `memuat_prevalensi` | boolean | benar atau salah | aturan tiga langkah [K] baris 2166 dan 2167 | wajib |
| `penanda` | enum `memuat_prevalensi`, `tidak_memuat_prevalensi` | teks | [K] baris 2175 sampai 2177 | wajib |

Perilaku saat data tidak tersedia. Bila selang belum dihitung, `batas_bawah` dan `batas_atas` diisi
`null` dan kartu mencetak `selang belum dihitung, angka titik belum boleh dipakai memutuskan`,
karena aturan Monte Carlo adalah kewajiban pelaporan ([PMR] baris 99 dan 149). Bila `prevalensi`
tidak ada, `memuat_prevalensi` diisi `null` dan penanda tidak boleh menulis salah satu dari dua
nilai enum. Contoh yang wajib tampil: AUPRC ssi 0,015 sampai 0,459 dengan selang yang memuat
prevalensi di 5 dari 9 fold ([EVA] baris 55 lewat [K] baris 2168).

#### 5.5.3 LIN-04 Register status dokumen vonis

- Pengguna: auditor, penulis laporan.
- Momen pakai: sebelum mengutip satu dokumen vonis, dan saat memeriksa apakah dokumen itu sudah digantikan ([K] baris 2199 sampai 2202).
- Masukan: daftar dokumen vonis beserta byte, baris, dan status; 10 dokumen diperiksa, 8 BERLAKU dan 2 DIGANTIKAN ([I4] bagian 1 baris 24 sampai 40 lewat [K] baris 2208 sampai 2216).
- Keluaran: tabel 10 baris dengan byte, baris, status, dan alasan ([K] baris 2221 sampai 2224).
- Status bukti: siap sekarang, seluruh dokumen sudah diperiksa.

| Field | Tipe | Satuan | Sumber | Wajib |
|---|---|---|---|---|
| `nama_dokumen` | string jalur relatif `docs/` | teks | [I4] bagian 1 baris 24 sampai 40 | wajib |
| `byte` | integer | byte | [I4] bagian 1 baris 24 sampai 40 | wajib |
| `baris` | integer | baris | [I4] bagian 1 baris 24 sampai 40 | wajib |
| `status` | enum `BERLAKU`, `DIGANTIKAN` | teks | [I4] bagian 1 baris 24 sampai 40 | wajib |
| `pengganti` | string atau null | teks | [I4] baris 24 sampai 40, contoh `RND_S5_DEFECT_STATUS.md` dan `V11_PM_FINAL.md` | wajib bila berstatus DIGANTIKAN |
| `alasan` | string satu kalimat | teks | aturan status [K] baris 2219 dan 2220 | wajib |
| `tanggal_periksa` | string tanggal | teks | [I4] bagian 1 baris 24 sampai 40 | wajib |
| `boleh_dikutip` | boolean | benar atau salah | akibat status per [K] baris 2219 dan 2220 | wajib |

Perilaku saat data tidak tersedia. Bila `pengganti` kosong padahal status `DIGANTIKAN`, baris itu
tidak boleh dirender sebagai DIGANTIKAN dan diisi `null` dengan label `dokumen pengganti belum
tercatat`. Bila satu dokumen baru muncul di `docs/` dan belum ada di register, barisnya ditambahkan
dengan status `BELUM DIPERIKSA` di luar dua nilai enum, dan penambahan itu menaikkan versi minor
kontrak sesuai bagian 2 butir 5.

### 5.6 Rumpun alat bantu insinyur

#### 5.6.1 INS-03 Kartu kelayakan sinyal sebelum dekomposisi

- Pengguna: peneliti sinyal.
- Momen pakai: sebelum menjalankan dekomposisi pada satu kanal pada satu sumur ([K] baris 2453 sampai 2456).
- Masukan: laju sampel kanal, pita frekuensi yang dicari, panjang segmen, hasil uji stasioneritas lokal ([K] baris 2464 sampai 2467).
- Keluaran: satu baris per kanal dengan status, pita tertinggi yang bisa dibaca, dan alasan ([K] baris 2477 sampai 2480).
- Status bukti: siap sebagian, syarat Nyquist siap, uji stasioneritas belum menyeluruh.

| Field | Tipe | Satuan | Sumber | Wajib |
|---|---|---|---|---|
| `kanal` | string | teks | [V3T] baris 159 dan 364 lewat [K] baris 2466 | wajib |
| `laju_sampel_hz` | float | hertz | [V3T] baris 159, contoh VIBLAT_RT F-14 hanya 0,0167 Hz | wajib |
| `nyquist_hz` | float | hertz | hitungan setengah laju sampel, batas atas terukur 0,1667 Hz ([V3T] baris 159) | wajib |
| `pita_dicari_hz` | float atau string rentang | hertz | [K] baris 2464 | wajib |
| `panjang_segmen_detik` | integer | detik | [K] baris 2464 | wajib |
| `uji_stasioner` | string hasil uji atau null | teks | [K] baris 2465 | wajib bila ada |
| `lulus` | boolean | benar atau salah | [K] baris 2468 dan 2469 | wajib |
| `alasan` | string satu kalimat | teks | [K] baris 2468 sampai 2472 | wajib |
| `pita_tertinggi_terbaca_hz` | float | hertz | [K] baris 2477 | wajib |

Perilaku saat data tidak tersedia. Bila `laju_sampel_hz` tidak ada, `nyquist_hz` diisi `null` dan
`lulus` diisi `null` dengan label `laju sampel belum tercatat`, sehingga kanal itu tidak bisa
dinyatakan lulus. Bila pita yang dicari di atas `nyquist_hz`, `lulus` bernilai salah dan alasan
wajib menyebut angka Nyquist, mengikuti contoh VMD yang gagal karena Nyquist 0,1667 Hz dengan 75
dari 105 percobaan gagal ([R3] baris 98 sampai 106 lewat [K] baris 2469). Bila `uji_stasioner`
kosong, status tertinggi adalah `lolos bersyarat`.

#### 5.6.2 INS-04 Kartu kanal yang perlu dipasang

- Pengguna: engineer instrumentasi.
- Momen pakai: saat merencanakan pemasangan sensor pada rig atau sumur berikutnya ([K] baris 2498 sampai 2501).
- Masukan: daftar kanal per engine, bukti ketiadaan, dan dampak terukur pada metrik ([K] baris 2507 sampai 2510).
- Keluaran: daftar kanal prioritas dengan alasan angka dan dampak terukur bila kanal dipasang ([K] baris 2518 sampai 2521).
- Status bukti: siap sebagian, bukti ketiadaan kuat untuk satu kanal, dampak metrik baru terukur sebagian.

| Field | Tipe | Satuan | Sumber | Wajib |
|---|---|---|---|---|
| `kanal` | string | teks | [EVA] baris 165 dan 169 lewat [K] baris 2510 sampai 2514 | wajib |
| `engine` | enum nama engine | teks | [K] baris 2507 | wajib |
| `bukti_ketiadaan` | string satu kalimat dengan angka | teks | [EVA] baris 165, contoh FlowOut absen pada hyd K-ii | wajib |
| `korelasi_pengganti` | object `min`, `max`, 0,995 sampai 1,000 | koefisien | [EVA] baris 165 | wajib bila ada |
| `dampak_metrik` | string, contoh P sama dengan R sama dengan nol pada q95 | teks | [EVA] baris 169 | wajib |
| `prioritas` | integer 1 sampai 5 | peringkat | [K] baris 2518 | wajib |
| `syarat_pasang` | string | teks | [K] baris 2519 sampai 2521 | wajib |

Perilaku saat data tidak tersedia. Bila `korelasi_pengganti` tidak ada, field diisi `null` dan
prioritas kanal itu tidak boleh lebih tinggi dari 3, karena tanpa korelasi pengganti dampak
penggantian kolom belum terbaca. Bila `dampak_metrik` kosong, kartu mencetak `dampak belum diukur
di titik operasi` dan kanal tetap masuk daftar dengan label tersebut.

#### 5.6.3 INS-05 Kartu permintaan data bertanda tangan

- Pengguna: koordinator data, pembimbing.
- Momen pakai: saat mengajukan permintaan data ke pemilik data, sekali per siklus ([K] baris 2537 sampai 2540).
- Masukan: tiga bukti ketiadaan yang sudah diuji ulang pada 2026-10-31, yaitu 0 dari 192 berkas punya rating motor ([A1] baris 58), 0 dari 161 berkas punya `dullingInfo` ([A1] baris 65), dan `GAINLOSSTOT` tidak ada di sembilan sumur ([RD0] baris 349) ([K] baris 2548 sampai 2552).
- Keluaran: daftar permintaan dengan tag, berkas, pemilik, dampak, dan status tanda tangan ([K] baris 2561 sampai 2564).
- Status bukti: siap sebagian, tiga bukti ketiadaan kuat, pemilik data belum ditetapkan.

| Field | Tipe | Satuan | Sumber | Wajib |
|---|---|---|---|---|
| `tag` | string, contoh `rating_motor`, `dullingInfo`, `GAINLOSSTOT` | teks | [A1] baris 58 dan 65, [RD0] baris 349 | wajib |
| `berkas_target` | string | teks | [K] baris 2555 dan 2556 | wajib |
| `pemilik_data` | string atau null | teks | [K] baris 2557, belum ditetapkan hari ini | opsional |
| `bukti_uji_ulang` | string dengan angka dan tanggal | teks | [A1] baris 58 dan 65, [RD0] baris 349 | wajib |
| `status_bukti` | enum `KUAT`, `DUGAAN` | teks | [K] baris 2556 dan 2557 | wajib |
| `dampak` | string, jumlah fitur yang terbuka | teks | [K] baris 2553 dan 2554 | wajib |
| `prioritas` | integer | peringkat | [K] baris 2554, urutan menurut jumlah fitur terbuka | wajib |
| `status_tanda_tangan` | enum `BELUM`, `DIMINTA`, `DITERIMA` | teks | [K] baris 2561 | wajib |
| `tanggal_uji_ulang` | string tanggal `2026-10-31` | teks | [K] baris 2548 | wajib |

Perilaku saat data tidak tersedia. Karena `pemilik_data` belum ditetapkan ([K] baris 2557), field
itu diisi `null` dan kartu mencetak `pemilik data belum ditetapkan`, sementara suratnya tetap boleh
disusun. Ketiadaan yang belum diuji ulang diberi `status_bukti` `DUGAAN` dan tidak boleh dipakai
sebagai dasar permintaan bertanda tangan. Bila `status_tanda_tangan` kosong, nilainya `BELUM`, bukan
`DIMINTA`, karena belum ada bukti permintaan terkirim.
---

## 6. Contoh muatan JSON per rumpun

Enam blok di bawah adalah contoh utuh satu muatan per rumpun. Angka di dalamnya diambil dari sumber
yang sama dengan tabel field di bagian 5, dan setiap angka yang tampil juga muncul di tabel field
beserta rujukannya. Blok ini contoh bentuk, bukan data produksi.

### 6.1 Rumpun kepercayaan, KEP-02 dan KEP-03 pada satu head

```json
{
  "kontrak_versi": "1.0.0",
  "fitur_id": "KEP-02",
  "rumpun": "kepercayaan",
  "keadaan_data": "SEBAGIAN",
  "label_kekurangan": [
    "selang: SUMBER_BELUM_DIUKUR",
    "s_b: SUMBER_BELUM_DIUKUR"
  ],
  "segmen": "F-14",
  "keputusan_akhir": "MANUSIA",
  "dibuat_pada_utc": "2026-10-31T11:30:00Z",
  "sumber_data": [
    { "berkas": "planning/00_INVENTARIS_V7_V8.md", "baris": 145, "byte": 39059 },
    { "berkas": "planning/03_SKOR_KEYAKINAN.md", "baris": 170, "byte": 66698 }
  ],
  "skor_keyakinan": {
    "nilai": 0.4950,
    "sk_tampil": 50,
    "pita": "P3",
    "batas_atas": 0.4950,
    "batas_dipotong": true,
    "komponen": { "s_a": 0.75, "s_b": 0.20, "s_c": 0.50 },
    "rumus_versi": "kelas_0,40_0,35_0,25",
    "selang": null,
    "status_komponen": "TERUKUR"
  },
  "payload": {
    "kelas": "vib",
    "sk_mentah": 49.50,
    "sk_tampil": 50,
    "label_batas": "batas atas 70 karena lapisan B belum terukur",
    "angka_penopang": [
      { "nama": "lift fold", "nilai": "1,61 sampai 3,50", "satuan": "kali", "sumber": "docs/V8_E_vib_CAPABILITY.md baris 52 dan 69" },
      { "nama": "presisi segmen", "nilai": 0.9444, "satuan": "rasio 0..1", "sumber": "scratch/v9_i1/v9_i1_RESULTS.json .engines[0].heads[0].metrik_segmen.precision" }
    ],
    "badge_far": {
      "head": "rule_display",
      "far_nilai": 49.942,
      "far_satuan": "alarm_per_24jam_negatif",
      "skala_jendela_detik": 60,
      "fp": 30,
      "tp": 510,
      "presisi": 0.9444,
      "recall": 0.4537,
      "n_windows": 1989,
      "n_aktif": 540,
      "frac_aktif": 0.2715,
      "n_nodata": 356,
      "teks_badge": "FAR 49,9/24 jam operasi negatif, jendela 60 detik, P 0,94, R 0,45"
    }
  }
}
```

### 6.2 Rumpun perencanaan maintenance, MNT-05 beban tinjauan per shift

```json
{
  "kontrak_versi": "1.0.0",
  "fitur_id": "MNT-05",
  "rumpun": "perencanaan_maintenance",
  "keadaan_data": "LENGKAP",
  "label_kekurangan": [],
  "segmen": "F-14",
  "keputusan_akhir": "MANUSIA",
  "dibuat_pada_utc": "2026-10-31T11:30:00Z",
  "sumber_data": [
    { "berkas": "scratch/v9_i1/v9_i1_RESULTS.json", "baris": 1687, "byte": 57555 },
    { "berkas": "docs/RND_ENGINE_S6_INTEGRATION.md", "baris": 31, "byte": 3915 }
  ],
  "skor_keyakinan": null,
  "payload": {
    "metode_bagi": 3,
    "label_skala": "angka segmen F-14, bukan median lintas fold",
    "baris": [
      { "head": "vib.rule_display", "far_per_24jam": 49.942, "tinjauan_per_shift_8jam": 17 },
      { "head": "hyd.rule_display", "far_per_24jam": 55.57, "tinjauan_per_shift_8jam": 19 },
      { "head": "hyd.hybrid_rule_and_persistence", "far_per_24jam": 16.611, "tinjauan_per_shift_8jam": 6 },
      { "head": "shk.rule_display", "far_per_24jam": 6.618, "tinjauan_per_shift_8jam": 3 },
      { "head": "stuck.rule_display", "far_per_24jam": 8.321, "tinjauan_per_shift_8jam": 3 },
      { "head": "tool_wear.op_far_calibrated", "far_per_24jam": 2.096, "tinjauan_per_shift_8jam": 1 },
      { "head": "ssi.rule_display", "far_per_24jam": 0.0, "tinjauan_per_shift_8jam": 0, "label": "nol tinjauan pada segmen ini" }
    ]
  }
}
```

### 6.3 Rumpun kualitas data, DAT-01 kelengkapan jendela

```json
{
  "kontrak_versi": "1.0.0",
  "fitur_id": "DAT-01",
  "rumpun": "kualitas_data",
  "keadaan_data": "SEBAGIAN",
  "label_kekurangan": [
    "gap_max_s: SUMBER_TIDAK_MENYEDIAKAN",
    "skor_keyakinan: SUMBER_BELUM_DIUKUR"
  ],
  "segmen": "F-14",
  "keputusan_akhir": "MANUSIA",
  "dibuat_pada_utc": "2026-10-31T11:30:00Z",
  "sumber_data": [
    { "berkas": "data/predictive/features_timeseries.npz", "baris": 0, "byte": 458129 },
    { "berkas": "docs/V3_TS_FEATURES.md", "baris": 89, "byte": 8429 }
  ],
  "skor_keyakinan": null,
  "waktu_indeks_menit": null,
  "payload": {
    "event_id": "contoh-event-2jam",
    "panjang_jendela_menit": 120,
    "n_rows": 1515,
    "gap_median_s": 4.9,
    "gap_max_s": null,
    "full_window": false,
    "label_kelengkapan": "sebagian",
    "fraksi_nan_sensor": 0.368,
    "teks_kartu": "Jendela 2 jam, 1.515 baris, gap median 4,9 detik, gap terbesar belum tercatat, fraksi NaN sensor 0,368"
  }
}
```

### 6.4 Rumpun perbandingan mesin, CMP-01 balapan terhadap baseline

```json
{
  "kontrak_versi": "1.0.0",
  "fitur_id": "CMP-01",
  "rumpun": "perbandingan_mesin",
  "keadaan_data": "SEBAGIAN",
  "label_kekurangan": [
    "fold: SUMBER_TIDAK_MENYEDIAKAN di dokumen ini, angka per fold ada di docs/V8_E_bit_wear_CAPABILITY.md baris 88",
    "auprc_model: SUMBER_DI_LUAR_CAKUPAN untuk baris ringkas"
  ],
  "segmen": "F-14",
  "keputusan_akhir": "MANUSIA",
  "dibuat_pada_utc": "2026-10-31T11:30:00Z",
  "sumber_data": [
    { "berkas": "docs/V8_E_bit_wear_CAPABILITY.md", "baris": 88, "byte": 16116 }
  ],
  "skor_keyakinan": null,
  "payload": {
    "kelas": "bit_wear",
    "varian_target": "target utama kelas",
    "median_baseline": 0.9038,
    "median_model": 0.8374,
    "auprc_baseline": { "min": 0.6376, "max": 0.9723 },
    "jumlah_fold_kalah": 100,
    "jumlah_fold": 100,
    "teks_kartu": "baseline persistence menang di 100 dari 100 jawaban, median 0,9038 berbanding 0,8374"
  }
}
```

### 6.5 Rumpun linimasa, LIN-03 dan LIN-04 pada satu angka dan satu dokumen

```json
{
  "kontrak_versi": "1.0.0",
  "fitur_id": "LIN-03",
  "rumpun": "linimasa",
  "keadaan_data": "SEBAGIAN",
  "label_kekurangan": [
    "iterasi_bootstrap: SUMBER_TIDAK_MENYEDIAKAN untuk baris ini",
    "seed: SUMBER_TIDAK_MENYEDIAKAN untuk baris ini"
  ],
  "segmen": "F-14",
  "keputusan_akhir": "MANUSIA",
  "dibuat_pada_utc": "2026-10-31T11:30:00Z",
  "sumber_data": [
    { "berkas": "docs/V9_EVAL_A_LAYERA.md", "baris": 55, "byte": 32713 },
    { "berkas": "planning/00_INVENTARIS_RND2_V11.md", "baris": 24, "byte": 35536 }
  ],
  "skor_keyakinan": null,
  "payload": {
    "angka": {
      "kelas": "ssi",
      "metrik": "AUPRC",
      "angka_titik": 0.015,
      "batas_bawah": 0.015,
      "batas_atas": 0.459,
      "prevalensi": null,
      "memuat_prevalensi": true,
      "fold_memuat": 5,
      "fold_total": 9,
      "penanda": "memuat_prevalensi",
      "iterasi_bootstrap": null,
      "seed": null
    },
    "dokumen": {
      "nama_dokumen": "docs/RND_S5_AUDIT_WAVE2.md",
      "byte": 27190,
      "status": "DIGANTIKAN",
      "pengganti": "docs/RND_S5_DEFECT_STATUS.md",
      "alasan": "fungsinya digantikan dokumen status cacat",
      "boleh_dikutip": false
    }
  }
}
```

### 6.6 Rumpun alat bantu insinyur, INS-04 kanal yang perlu dipasang

```json
{
  "kontrak_versi": "1.0.0",
  "fitur_id": "INS-04",
  "rumpun": "alat_bantu",
  "keadaan_data": "LENGKAP",
  "label_kekurangan": [],
  "segmen": "F-14",
  "keputusan_akhir": "MANUSIA",
  "dibuat_pada_utc": "2026-10-31T11:30:00Z",
  "sumber_data": [
    { "berkas": "docs/V9_EVAL_A_LAYERA.md", "baris": 165, "byte": 32713 }
  ],
  "skor_keyakinan": null,
  "payload": {
    "kanal": "FlowOut",
    "engine": "hyd",
    "klaim": "hyd K-ii",
    "bukti_ketiadaan": "FlowOut absen pada data hyd K-ii",
    "korelasi_pengganti": { "min": 0.995, "max": 1.000, "jumlah_kolom": 4 },
    "dampak_metrik": "varian literal tidak dapat dihitung, P sama dengan R sama dengan nol pada q95",
    "prioritas": 1,
    "syarat_pasang": "sensor flow keluar terpasang dan tercatat pada berkas WITSML sumur terkait"
  }
}
```

---

## 7. Tiga keadaan data per rumpun

Tiga keadaan dipakai seragam: `LENGKAP`, `SEBAGIAN`, `KOSONG`. Teks di bawah adalah teks yang
benar-benar dirender, jadi boleh disalin apa adanya ke antarmuka. Aturan umum yang berlaku untuk
keenam rumpun: keadaan `SEBAGIAN` dan `KOSONG` wajib memuat minimal satu entri
`label_kekurangan`, dan keadaan `KOSONG` tidak boleh menyembunyikan panel, hanya mengganti isinya.

### 7.1 Kepercayaan

- `LENGKAP`: seluruh angka penopang, tier, layer, dan badge FAR terisi, `label_kekurangan` kosong. Teks: `Semua angka kelas ini terukur. Tier dan angka penopang berasal dari tabel terbit.`
- `SEBAGIAN`: satu komponen kosong, misalnya lapisan B belum terukur. Teks: `Sebagian angka terukur. Skor dibatasi 70 karena lapisan B belum terukur, dan baris yang kosong diberi label, bukan nol.`
- `KOSONG`: kelas belum punya angka penopang sama sekali. Teks: `Belum ada angka penopang untuk kelas ini. Yang ditampilkan hanya nama kelas dan tugasnya, tanpa tier dan tanpa skor.`

### 7.2 Perencanaan maintenance

- `LENGKAP`: seluruh baris punya FAR dan jumlah tinjauan, atau seluruh kolom antrean punya nilai. Teks: `Seluruh baris lengkap. Angka berlaku untuk segmen F-14 pada 24 jam operasi negatif.`
- `SEBAGIAN`: satu kolom kosong, misalnya lead hanya tersedia untuk hyd atau sumur belum terpetakan. Teks: `Sebagian kolom kosong. Kolom lead hanya terisi untuk hyd, kolom sumur belum terpetakan, dan kedua kolom itu ditandai tidak tersedia.`
- `KOSONG`: tidak satu pun baris punya FAR atau skor. Teks: `Tidak ada baris yang bisa diurutkan pada segmen ini. Antrean kosong bukan berarti aman, artinya belum ada peringatan yang terukur.`

### 7.3 Kualitas data

- `LENGKAP`: seluruh kanal punya fill rate dan status, atau seluruh kolom `X_window_meta` terbaca. Teks: `Seluruh kanal terukur. Status siap, bersyarat, dan belum dihitung dari persen kosong yang nyata.`
- `SEBAGIAN`: sebagian kanal tidak punya fill rate atau gap maksimum tidak tercatat. Teks: `Sebagian kanal belum terukur. Kanal tanpa fill rate masuk daftar gugur dengan alasan belum dihitung, dan kanal tanpa uji konstansi ditandai lolos bersyarat.`
- `KOSONG`: berkas kanal tidak ada atau metadata jendela tidak ada. Teks: `Berkas kanal tidak ada untuk sumur ini. Panel menampilkan daftar kanal yang dibutuhkan beserta nama berkas target, tanpa angka.`

### 7.4 Perbandingan mesin

- `LENGKAP`: seluruh fold punya AUPRC model dan baseline. Teks: `Seluruh fold terbanding. Jumlah fold yang dibandingkan tercetak di sebelah median.`
- `SEBAGIAN`: sebagian fold tanpa hasil model atau tanpa nama pembanding. Teks: `Sebagian fold tidak punya hasil model. Fold itu tidak digambar sebagai garis dan tidak diisi median.`
- `KOSONG`: kelas belum punya hasil sama sekali. Teks: `Kelas ini belum punya hasil per fold. Yang tampil hanya nama kelas dan baseline yang direncanakan, tanpa angka menang.`

### 7.5 Linimasa dan jejak keputusan

- `LENGKAP`: setiap peringatan punya label tindakan, peninjau, dan alasan. Teks: `Seluruh peringatan berlabel. Tingkat tindak lanjut dihitung dari peringatan berlabel dibagi peringatan yang tampil.`
- `SEBAGIAN`: sebagian peringatan belum berlabel atau selang belum dihitung. Teks: `Sebagian peringatan masih terbuka. Peringatan tanpa label dihitung terbuka, bukan benar, dan sel tanpa selang ditandai belum dihitung.`
- `KOSONG`: belum ada satu pun keputusan tercatat pada periode itu. Teks: `Belum ada keputusan tercatat pada periode ini. Tingkat tindak lanjut tidak ditampilkan karena penyebutnya nol.`

### 7.6 Alat bantu insinyur

- `LENGKAP`: laju sampel, Nyquist, pita dicari, dan uji stasioner semuanya ada. Teks: `Syarat sinyal lengkap. Pita tertinggi yang bisa dibaca dihitung dari laju sampel.`
- `SEBAGIAN`: laju sampel ada tetapi uji stasioner belum. Teks: `Laju sampel tercatat, uji stasioner belum dijalankan. Status tertinggi yang boleh diberikan adalah lolos bersyarat.`
- `KOSONG`: kanal belum punya laju sampel tercatat. Teks: `Laju sampel kanal ini belum tercatat. Kartu menampilkan nama kanal dan berkas target, tanpa status lulus.`

---

## 8. Aturan lintas fitur

### 8.1 Fitur yang wajib membawa skor keyakinan

Enam fitur wajib membawa objek `skor_keyakinan` karena keluarannya memuat satu angka keyakinan:
KEP-02, KEP-05, MNT-01, MNT-02, DAT-01, LIN-01. Lima belas fitur lain menulis
`"skor_keyakinan": null` dengan `label_kekurangan` berisi `SUMBER_DI_LUAR_CAKUPAN` untuk field itu.
Alasannya: memaksa skor pada fitur yang tidak menyajikannya akan mengarang angka baru.

### 8.2 Urutan validasi saat memuat muatan

Empat pemeriksaan berurutan, dan muatan ditolak pada pemeriksaan pertama yang gagal:

1. `kontrak_versi` cocok dengan versi yang dipakai antarmuka.
2. `fitur_id` termasuk 21 nilai di bagian 3.
3. `sumber_data` berisi minimal satu entri dengan `berkas` dan `baris`.
4. `label_kekurangan` terisi bila `keadaan_data` bukan `LENGKAP`, dan setiap entrinya memakai
   salah satu dari tiga sebab yang sah.

### 8.3 Larangan yang melekat pada semua muatan

Tiga larangan, semuanya turunan kerangka wajib butir 1 dan butir 4:

Pertama, tidak ada field `alarm`, `notifikasi`, atau `prioritas_kritis` di 21 fitur ini, karena slot
alarm otomatis hari ini nol dari tujuh engine ([J] `.decision_layer.auto_critical_alarm_slots`
bernilai 0, ledger baris 2024 `PM-078`).

Kedua, tidak ada angka nol yang dipakai sebagai pengganti data kosong. Nol hanya sah bila nol itu
hasil ukur, misalnya FAR ssi 0,0 pada segmen F-14 (keluaran bagian 10.9) atau `hilang` 0 pada audit
berkas.

Ketiga, tidak ada penggabungan angka antar engine di dalam satu muatan. Setiap baris membawa satu
`fitur_id` dan satu `klaim`, mengikuti larangan [DSS1] bagian 3.5 baris 191 sampai 210.

### 8.4 Rekap jumlah field per rumpun

| Rumpun | Fitur | Field kontrak (tidak termasuk amplop) | Field wajib | Field wajib bila ada |
|---|---:|---:|---:|---:|
| kepercayaan | 4 | 39 | 33 | 6 |
| perencanaan maintenance | 4 | 37 | 33 | 4 |
| kualitas data | 4 | 35 | 29 | 4 |
| perbandingan mesin | 3 | 24 | 22 | 2 |
| linimasa | 3 | 27 | 24 | 2 |
| alat bantu insinyur | 3 | 23 | 20 | 3 |
| **Total** | **21** | **185** | **161** | **21** |

Angka pada tabel di atas dihitung dari baris tabel di bagian 5, tidak termasuk tabel amplop di
bagian 4 yang berisi 11 field. Perintah penghitungnya ada di bagian 10.11.
---

## 9. Yang belum diverifikasi

Ditulis terbuka, sesuai kerangka butir 3 dan butir 6.

1. Berkas [K] setebal 166.662 byte dan 2.780 baris tidak dibaca seluruhnya. Yang dibaca adalah
   bagian 1 sampai 4 penuh dan kepala 21 fitur terpilih lewat pencarian baris `Masukan` dan
   `Keluaran`. Kalimat penjelas di dalam fitur yang tidak terpilih tidak diperiksa.
2. Sembilan berkas di bagian 1 bertanda "hanya lewat kutipan" tidak dibuka langsung. Angka dari
   berkas itu diwarisi dari [K] beserta rujukan baris yang tercetak di [K]. Konsekuensinya: bila
   rujukan baris di [K] keliru, dokumen ini mewarisi kekeliruan itu. Yang sudah diperiksa langsung
   oleh dokumen ini hanya [V3T] baris 85 sampai 92 dan [V3W] baris 38 sampai 44.
3. Angka `median gap 4,9 detik`, `median baris 379, 1.515, 4.549`, dan `fraksi NaN 0,368` dibaca
   dari [V3T] baris 89 dan 109. Isi larik `X_window_meta` belum dihitung ulang per sel, karena
   pustaka numpy tidak dipakai di sesi ini. Daftar isi arsip [NPZ] sudah diperiksa (bagian 10.3),
   tetapi nilai di dalam larik tidak.
4. Contoh muatan JSON di bagian 6 memakai angka yang benar, tetapi `event_id` pada contoh DAT-01
   bernilai `contoh-event-2jam`, bukan pengenal nyata. Pengenal nyata ada di larik `event_id.npy`
   dan belum dibaca.
5. `waktu_indeks_menit` belum bisa dipetakan ke tanggal kalender. [J]
   `.segmen_info.vib.catatan_waktu` menyatakan asal kalender TIDAK diverifikasi, sehingga semua
   field `_utc` di dokumen ini berasal dari jam sistem saat render, bukan dari data.
6. Jumlah field pada tabel 8.4 dihitung dari baris tabel dokumen ini, bukan dari kode program yang
   menghasilkan muatan. Bila kelak ada field baru, angka itu harus dihitung ulang.
7. Pemetaan 11 klaim ke 8 baris skor keyakinan memakai tabel [DSS1] baris 170 sampai 177. Dua baris
   yaitu `stuck K-ii` dan `tool_wear K-ii` masih memakai batas atas pinjaman dari baris kelasnya,
   dan keadaan itu dicatat di [DSS1] baris 186 sampai 189, bukan diselesaikan di sini.
8. Tidak ada satu pun model atau engine yang dijalankan ulang di sesi ini. Yang dijalankan hanya
   `stat`, `wc`, `sed`, `grep`, `jq`, dan `python3 -m zipfile -l`. Semua keluarannya ada di
   bagian 10.

---

## 10. Keluaran perintah yang dijalankan

Semua keluaran di bawah ditempel apa adanya. Keluaran yang panjang dipotong dan bagian yang dipotong
disebut eksplisit.

### 10.1 Ukuran dan jumlah baris berkas masukan

```
$ stat -c '%n %s bytes %y' planning/01_KATALOG_FITUR.md planning/03_SKOR_KEYAKINAN.md \
    planning/04_ANTREAN_TINJAUAN.md scratch/v9_i1/v9_i1_RESULTS.json
planning/01_KATALOG_FITUR.md 166662 bytes 2026-10-31 17:15:16.610541400 +0700
planning/03_SKOR_KEYAKINAN.md 66698 bytes 2026-10-31 17:42:18.207873600 +0700
planning/04_ANTREAN_TINJAUAN.md 95168 bytes 2026-10-31 18:19:09.425351900 +0700
scratch/v9_i1/v9_i1_RESULTS.json 57555 bytes 2026-10-29 11:21:21.855597100 +0700

$ wc -l planning/01_KATALOG_FITUR.md planning/03_SKOR_KEYAKINAN.md \
    planning/04_ANTREAN_TINJAUAN.md scratch/v9_i1/v9_i1_RESULTS.json
  2780 planning/01_KATALOG_FITUR.md
  1060 planning/03_SKOR_KEYAKINAN.md
  1428 planning/04_ANTREAN_TINJAUAN.md
  1758 scratch/v9_i1/v9_i1_RESULTS.json
  7026 total
```

### 10.2 Ukuran berkas pendukung

```
$ stat -c '%s %n' docs/V3_TS_FEATURES.md docs/V3_DATA_ACQUISITION_INVENTORY.md \
    docs/V3_WITSML_PARSE_REPORT.md docs/RND_S6_PM_WAVE2.md docs/V9_PM1_ARCHITECTURE.md \
    docs/V9_PM2_VERDICT.md docs/V9_EVAL_A_LAYERA.md docs/V9_EVAL_B_LAYERB.md \
    docs/V9_EVAL_C_LAYERC.md docs/RND_ENGINE_S6_INTEGRATION.md docs/V6_A1_DATA_AUDIT.md \
    docs/RND_D0_DATA_FEASIBILITY.md docs/RND_R2_STOKASTIK.md docs/RND_R3_VMD_SVM.md \
    docs/RND_PM_VERDICT.md docs/V8_E_bit_wear_CAPABILITY.md
8429 docs/V3_TS_FEATURES.md
17514 docs/V3_DATA_ACQUISITION_INVENTORY.md
3346 docs/V3_WITSML_PARSE_REPORT.md
40271 docs/RND_S6_PM_WAVE2.md
50456 docs/V9_PM1_ARCHITECTURE.md
22654 docs/V9_PM2_VERDICT.md
32713 docs/V9_EVAL_A_LAYERA.md
30472 docs/V9_EVAL_B_LAYERB.md
23153 docs/V9_EVAL_C_LAYERC.md
3915 docs/RND_ENGINE_S6_INTEGRATION.md
28138 docs/V6_A1_DATA_AUDIT.md
28196 docs/RND_D0_DATA_FEASIBILITY.md
28937 docs/RND_R2_STOKASTIK.md
32174 docs/RND_R3_VMD_SVM.md
34575 docs/RND_PM_VERDICT.md
16116 docs/V8_E_bit_wear_CAPABILITY.md
```

Catatan: ukuran `docs/RND_S6_PM_WAVE2.md` di sini 40.271 byte, sedangkan legenda [K] bagian 2 baris
107 menulis 40.271 juga untuk berkas itu, dan [K] menulis 471.945 byte untuk ledger. Kedua angka itu
cocok dengan `stat` di bagian 10.10 dan 10.2. Satu angka di [K] yang TIDAK cocok: [K] menulis [VR]
setara 24.746 byte pada baris 46, sedangkan `stat` hari ini memberi 32.141 byte untuk
`planning/02_RISET_VISUALISASI.md`, karena berkas itu diperbarui setelah katalog ditulis.

### 10.3 Daftar isi arsip features_timeseries.npz

```
$ python3 -m zipfile -l data/predictive/features_timeseries.npz
File Name                                             Modified             Size
X.npy                                          1980-01-01 00:00:00      1269248
feature_names.npy                              1980-01-01 00:00:00        10908
X_baseline.npy                                 1980-01-01 00:00:00        29212
baseline_names.npy                             1980-01-01 00:00:00          416
X_window_meta.npy                              1980-01-01 00:00:00        31856
window_meta_names.npy                          1980-01-01 00:00:00          491
event_id.npy                                   1980-01-01 00:00:00         5416
fold.npy                                       1980-01-01 00:00:00         1636
wellbore.npy                                   1980-01-01 00:00:00         1691
act_start_utc.npy                              1980-01-01 00:00:00        18786
category.npy                                   1980-01-01 00:00:00         1789
```

Keluaran di atas dipotong pada sebelas baris pertama dari seluruh isi arsip. Ukuran berkas npz itu
sendiri 458.129 byte menurut bagian 10.13.

### 10.4 Blok coverage pada metadata fitur

```
$ jq -c '.coverage' data/predictive/features_timeseries_meta.json
{"labels_total":884,"mapped_to_fold":671,"unmapped_excluded":{"NO 15/9-F-15 D":122,
"NO 15/9-F-15 C":89,"NO 15/9-F-15 B":2},"out_of_range_excluded":{"F-15_S":7,"F-5":2,"F-7":1},
"features_built":661,"zero_row_windows":570,"partial_windows":1}
```

Angka 122 ditambah 89 ditambah 2 sama dengan 213, sehingga 671 ditambah 213 sama dengan 884. Ini
aritmetika yang bisa diperiksa pembaca langsung dari keluaran di atas.

### 10.5 Struktur waktu pada segmen_info

```
$ jq -c '.segmen_info | to_entries[0]' scratch/v9_i1/v9_i1_RESULTS.json
{"key":"vib","value":{"n":1989,"ts_bin_min":20189486,"ts_bin_max":20192503,"rentang_menit":3018,
"catatan_waktu":"ts_bin = indeks menit internal D1 (grid 60 dtk, +1 per menit); asal kalender
TIDAK diverifikasi di sesi ini — jangan dibaca sebagai tanggal"}}
```

Perhatikan: keluaran asli memuat tanda pisah panjang di dalam teks `catatan_waktu`. Tanda itu bagian
dari data sumber, bukan tanda pisah yang ditulis dokumen ini, dan tidak diubah supaya kutipan tetap
setia. Pemeriksaan tanda pisah dokumen ini di bagian 10.12 menghitung tanda pisah di luar blok kode.

### 10.6 Lapisan keputusan dan status manusia

```
$ jq -c '.decision_layer.layers.L1[0], .decision_layer.ringkasan, .decision_layer.auto_critical_alarm_slots' \
    scratch/v9_i1/v9_i1_RESULTS.json
{"engine":"vib","head":"rule_display","klaim":null,"tier":"PERINGATAN-BERPENGAWAS",
"status":null,"n_aktif":540,"human_review_required":true}
{"L0":5,"L1":11,"L2":9,"L3":2}
0

$ jq -r '.human_review_required, .keputusan_akhir' scratch/v9_i1/v9_i1_RESULTS.json
true
MANUSIA — alat ini menyiapkan status, peringatan, tren, dan bahan rencana inspeksi
```

Jumlah L0 5, L1 11, L2 9, L3 2 bila dijumlahkan sama dengan 27, yaitu jumlah kepala seluruh engine
pada keluaran 10.7.

### 10.7 Tujuh engine dan jumlah kepala

```
$ jq -r '.engines[] | "\(.engine) | heads=\(.heads|length)"' scratch/v9_i1/v9_i1_RESULTS.json
vib | heads=4
ssi | heads=4
shk | heads=4
stuck | heads=6
hyd | heads=4
bit_wear | heads=2
tool_wear | heads=3
```

4 ditambah 4 ditambah 4 ditambah 6 ditambah 4 ditambah 2 ditambah 3 sama dengan 27.

### 10.8 Satu kepala lengkap, dipakai sebagai contoh bentuk field

```
$ jq -c '.engines[0].heads[0]' scratch/v9_i1/v9_i1_RESULTS.json
{"head":"rule_display","klaim":null,"tier":"PERINGATAN-BERPENGAWAS","layer":"L1",
"badge_far":"FAR 10,0-49,9/24jam di 4 well (E_RULE §2.1); P 0,87-0,95",
"keyakinan":"presisi rule stabil antar-well (1,1x); recall 0,28-0,60",
"batas_pemakaian":"jangan klaim lead-time menit; ambang wajib kalibrasi per-well (D-A4) sebelum dipakai sbg alarm",
"human_review_required":true,"n_windows":1989,"n_aktif":540,"frac_aktif":0.2715,
"contoh_idx_aktif":[429,444,472,478,489],
"metrik_segmen":{"n":1989,"pos":1124,"neg":865,"tp":510,"fp":30,"fn":614,
"precision":0.9444,"recall":0.4537,"far_segmen":49.942,"far_unit":"FP/24jam-negatif (jendela 60 dtk)"},
"n_nodata":356,"definisi":"aturan kanal pada menit t0-1 (strict-past)"}

$ jq -c '[.engines[] | .engine as $e | .heads[] | select(has("lead_menit") or has("head_utama")) |
    {engine:$e, head:.head, lead:.lead_menit, utama:.head_utama}]' scratch/v9_i1/v9_i1_RESULTS.json
[{"engine":"hyd","head":"hybrid_rule_and_persistence","lead":8.0,"utama":true}]
```

Keluaran kedua adalah dasar pernyataan bahwa hanya satu head yang punya `lead_menit` dan harga itu
8,0 menit.

### 10.9 Beban tinjauan per shift dan profil kapabilitas

```
$ jq -r '.nilai_maintenance.beban_tinjauan_L1[] | "\(.engine).\(.head) far=\(.far_per_24jam) shift=\(.tinjauan_per_shift_8jam)"' \
    scratch/v9_i1/v9_i1_RESULTS.json
vib.rule_display far=49.942 shift=17
vib.hybrid_rule_and_persistence far=49.942 shift=17
ssi.rule_display far=0.0 shift=0
ssi.hybrid_rule_and_persistence far=0.0 shift=0
shk.rule_display far=6.618 shift=3
shk.hybrid_rule_and_persistence far=6.618 shift=3
stuck.rule_display far=8.321 shift=3
stuck.hybrid_rule_and_persistence far=8.321 shift=3
hyd.rule_display far=55.57 shift=19
hyd.hybrid_rule_and_persistence far=16.611 shift=6
tool_wear.op_far_calibrated far=2.096 shift=1

$ jq -c '.profil_kapabilitas[] | {engine, status_B:.lapisan_B_nilai_maintenance.status,
    lead:.lapisan_B_nilai_maintenance.lead_menit, kekuatan:.kekuatan_bukti}' \
    scratch/v9_i1/v9_i1_RESULTS.json
{"engine":"vib","status_B":"BELUM TERUKUR","lead":{},"kekuatan":"SEDANG"}
{"engine":"ssi","status_B":"BELUM TERUKUR","lead":{},"kekuatan":"SEDANG"}
{"engine":"shk","status_B":"BELUM TERUKUR","lead":{},"kekuatan":"SEDANG"}
{"engine":"stuck","status_B":"BELUM TERUKUR","lead":{},"kekuatan":"SEDANG"}
{"engine":"hyd","status_B":"TERUKUR","lead":{"hybrid_rule_and_persistence":8.0},"kekuatan":"SEDANG"}
{"engine":"bit_wear","status_B":"BELUM TERUKUR","lead":{},"kekuatan":"LEMAH"}
{"engine":"tool_wear","status_B":"BELUM TERUKUR","lead":{},"kekuatan":"SEDANG"}
```

Enam head dari sebelas baris beban bernilai FAR sama dengan head pasangannya, karena `rule_display`
dan `hybrid_rule_and_persistence` memakai angka FAR yang sama pada kelas definisi-kanal. Ini bukan
salinan yang salah, melainkan sifat komposisi hibrida yang sudah dicatat di `badge_far` kepala
hibrida (bagian 10.8).

### 10.10 Nilai maintenance dan baris ledger

```
$ jq -c '.nilai_maintenance | {batas,sumber,total_jam_tercatat,n_record_aktivitas,
    jam_per_kode:(.jam_per_kode|type),jam_henti_per_sebab:(.jam_henti_per_sebab|type)}' \
    scratch/v9_i1/v9_i1_RESULTS.json
{"batas":"jam henti tidak dapat dipetakan ke satu alarm tertentu: tidak ada kunci bit atau work order
yang menghubungkan alarm ke record DDR","sumber":"/mnt/d/Capstone 1(v2)/data/volve/ddr.parquet",
"total_jam_tercatat":39397.986,"n_record_aktivitas":23447,"jam_per_kode":"object",
"jam_henti_per_sebab":"object"}

$ jq -c '.nilai_maintenance.jam_henti_per_sebab' scratch/v9_i1/v9_i1_RESULTS.json
{"success":4688.087,"equipment failure":2739.667,"operation failed":479.75,"stuck equipment":212.0,
"circulation loss":195.0,"mud loss":28.75}

$ grep -n 'PM-078' docs/RND_PROVENANCE_LEDGER.md
2024:| PM-078 | 0 | slot | KONVENSI | scratch/v9_i1/v9_i1_RESULTS.json auto_critical_alarm_slots;
docs/V9_EVAL_C_LAYERC.md tier | bagian 3, 4, 6 | TERUKUR |
3418:| S6-184 | lihat baris PM-078 | kutipan | KUTIPAN | kutipan: tier ALARM-OTOMATIS 0 slot |
bagian 3 dan 4 | TIDAK DIHITUNG ULANG |

$ grep -n 'L-21\b' docs/RND_PROVENANCE_LEDGER.md
51:| L-21 | >= 5 dari 27 fitur | hitungan fitur | KONVENSI | `code/v9_e_STAT_03_tool_wear.py:40`
(`N_FEAT_ALARM = 5`), `:206`; `code/v9_i1_pipeline.py:627`; jumlah 27 dipaksakan oleh asersi
`code/v9_i1_pipeline.py:605` dan `code/v9_e_RULE_03_bitwear_toolwear.py:145` | 2026-10-27 |
tool_wear `calib_5of27` | BELUM |
```

Keluaran `grep` di atas dipotong pada baris yang tercetak, sesuai keluaran alat. Nomor baris ledger
2024, 3418, dan 51 adalah nomor yang harus dikutip bila angka alarm nol dirujuk di dokumen lain.

### 10.11 Perintah penghitung baris tabel dokumen ini

```
$ awk '/^### 5\./ {if (f) print f" "n; f=$0; n=0}
       /^\| `/ {n++}
       END {if (f) print f" "n}' planning/08_KONTRAK_DATA.md
```

Keluaran perintah ini ditempel di bagian 10.13 setelah berkas selesai ditulis, karena perintah yang
sama dipakai untuk memeriksa angka pada tabel 8.4.

### 10.12 Penutup yang bisa diperiksa

Empat pemeriksaan yang bisa diulang pembaca pada berkas ini, dan hasilnya ada di bagian 10.13:

1. Jumlah subbagian fitur dengan pola `#### 5.` harus 21.
2. Jumlah baris berpipa harus lebih dari 150, karena 21 tabel field ditambah tabel amplop, tabel
   fitur, tabel rekap, dan tabel keadaan.
3. Jumlah tanda pisah panjang di luar blok kode harus 0.
4. Jumlah kemunculan tiga kata larangan kerangka butir 6 harus 0.
