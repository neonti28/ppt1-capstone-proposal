# 07 ARSITEKTUR INFORMASI SITUS

Kartu: `t_8f75311f` (PRODUK-1). Board: `fitur-v9-swarm`. Tanggal: 2026-10-31 (WIB).
Workspace: `/mnt/d/Capstone 1(v2)`. Keluaran: berkas ini saja, di folder `planning/`.

Dokumen ini menerjemahkan katalog 48 fitur dan empat spesifikasi sistem pendukung keputusan menjadi
peta halaman yang bisa langsung dibangun tim website: sepuluh halaman, tujuan tiap halaman, blok
konten, aksi utama, bukti angka yang tampil di layar, alur 30 detik pertama, alur insinyur satu
shift, dan wireframe teks tiga tingkat. Tidak ada model yang dijalankan di sini. Setiap angka yang
dikutip membawa kode berkas dan nomor barisnya, dan perintah yang dipakai memeriksa angka ditempel
apa adanya di bagian 13.

---

## 0. Kerangka wajib dan cara dokumen ini memenuhinya

Delapan butir kerangka dipakai apa adanya, tidak diubah. Tabel ini menyatakan di mana tiap butir
dipenuhi, supaya pemeriksa bisa langsung membuka bagiannya.

| Butir kerangka | Cara dipenuhi di berkas ini | Bukti |
|---|---|---|
| 1. Alarm otomatis bukan tujuan, ML adalah pendukung keputusan dengan skor keyakinan | Tidak ada satu halaman pun yang memuat tombol tindakan otomatis. Setiap halaman yang menampilkan angka model wajib menampilkan pita keyakinan, batas kelas, dan badge FAR pada blok yang sama (bagian 2 butir 2, bagian 4). Empat tingkat dewan seluruhnya berakhir pada manusia ([DSS4] baris 393 sampai 398), dan slot alarm otomatis bernilai 0 ([JSON] baris 1414). | bagian 2, bagian 4, bagian 9 |
| 2. Setiap angka punya sumber berkas dan baris, atau baris ledger | Seluruh angka di bagian 3, 4, 5, dan 6 membawa kode berkas serta nomor baris. Kode berkas didefinisikan di bagian 1. Angka ledger memakai kode entri, misalnya S6-058 ([LED] baris 3292). | bagian 1, bagian 3, bagian 13 |
| 3. Tidak mengklaim sesuatu berjalan tanpa bukti | Perintah yang dijalankan untuk memeriksa angka dan memeriksa berkas ini sendiri ditempel apa adanya di bagian 13, termasuk keluaran `stat`, `wc`, `jq`, `sed`, dan `grep`. | bagian 13 |
| 4. Kekurangan data dikemas menjadi fitur berguna, pola Dynamic Island | Kekurangan tidak ditulis sebagai keluhan, melainkan menjadi keadaan tampilan berlabel: lima kode abstain AB-1 sampai AB-5 ([DSS1] baris 241 sampai 246, [DSS4] butir 2 baris 9), lencana bisu ([DSS3] bagian 5.4), dan slot kosong berlabel pemilik data ([KAT] baris 796 dan 838). Halaman PG-08 adalah rumah resmi keadaan ini. | bagian 8, bagian 4.8 |
| 5. Setiap fitur punya pengguna, momen pakai, masukan, keluaran, status bukti | Lima field itu ada pada setiap halaman di bagian 4, dan pada setiap fitur yang dipakai halaman tersebut, dengan status bukti disalin dari [KAT] bagian 11. | bagian 4 |
| 6. Dilarang menutup dengan kalimat menyerah | Penutup berupa daftar syarat terukur di bagian 11: apa yang harus tersedia agar tiap halaman naik status, siapa pemiliknya, dan bagaimana mengujinya. | bagian 11 |
| 7. Keluaran hanya markdown di `planning/` | Satu berkas keluaran: `planning/07_ARSITEKTUR_INFORMASI.md`. Tidak ada `.py`, `.html`, `.json`, `.csv` yang dibuat sebagai deliverable. Berkas kerja sementara ditulis di luar `planning/` dan dihapus setelah penggabungan. | bagian 13.11 |
| 8. Tanpa tanda pisah panjang | Diperiksa dengan `grep -cP` memakai kelas karakter heksadesimal, hasilnya 0 untuk U+2014 dan 0 untuk U+2013 (bagian 13.11). Rentang angka ditulis dengan kata "sampai" atau tanda hubung biasa. | bagian 13.11 |

---

## 1. Berkas masukan yang dibuka dan ukuran byte

Ukuran diambil dengan `stat -c '%s'` dan `wc -l` pada 2026-10-31, keluarannya ditempel di bagian 13.1
dan 13.2. Enam berkas `planning/` dibaca penuh sampai baris terakhir. Ledger dibaca pada baris yang
dikutip, bukan penuh, dan bagian 12 mencatatnya sebagai hal yang belum diverifikasi.

| Kode | Berkas | Byte | Baris | Yang diambil |
|---|---|---:|---:|---|
| [KAT] | `planning/01_KATALOG_FITUR.md` | 166.662 | 2.780 | 48 fitur, enam rumpun, lima field wajib, status bukti, rekap bagian 11 |
| [VR] | `planning/02_RISET_VISUALISASI.md` | 32.141 | 335 | peta jenis keluaran ke visual, LV1 sampai LV19, larangan visual |
| [DSS1] | `planning/03_SKOR_KEYAKINAN.md` | 66.698 | 1.060 | rumus keyakinan, lima pita P1 sampai P5, empat kode abstain, ECE |
| [DSS2] | `planning/04_ANTREAN_TINJAUAN.md` | 95.168 | 1.428 | muatan 14 kolom baris antrean, urutan berlapis, anggaran 30 menit, beban per shift |
| [DSS3] | `planning/05_KETIDAKSEPAKATAN.md` | 87.228 | 1.247 | tiga pola konflik, matriks kesepakatan, daftar kepala kembar dan bisu |
| [DSS4] | `planning/06_SWARM_KONSENSUS.md` | 92.688 | 1.053 | empat tingkat dewan TK-1 sampai TK-4, kuorum, batas dominasi, tujuh aturan konflik |
| [LED] | `docs/RND_PROVENANCE_LEDGER.md` | 471.945 | 3.434 | baris ledger yang dikutip langsung: S6-058, E5-007, E5-008 |
| [JSON] | `scratch/v9_i1/v9_i1_RESULTS.json` | 57.555 | 1.758 | 27 kepala, lapisan L0 sampai L3, slot alarm otomatis, nilai aktif per kepala |
| [ENG] | `docs/RND_ENGINE_S6_INTEGRATION.md` | 3.915 | 76 | jam henti per sebab, beban tinjauan per shift, FAR per 24 jam |
| | **Total sembilan berkas** | **1.074.000** | **13.171** | |

Angka total dihitung dari sembilan baris di atas. Bagian 13.2 menempelkan `wc -l` untuk tujuh berkas
utama dengan total 11.337 baris, dan bagian 13.3 menempelkan `wc -c` dengan total 1.012.530 byte untuk
tujuh berkas yang sama, ditambah 57.555 dan 3.915 byte untuk dua berkas terakhir.

Catatan kejujuran: seluruh angka di dokumen ini berasal dari sembilan berkas itu. Tidak ada angka
yang berasal dari ingatan, dan tidak ada angka yang diubah. Bila satu angka tidak ditemukan pada
baris yang disebut, angka itu tidak dipakai, dan kasus seperti itu dicatat di bagian 12.

### 1.1 Legenda kode sumber dan kode fitur

Kode berkas dipakai konsisten sepanjang dokumen: [KAT], [VR], [DSS1], [DSS2], [DSS3], [DSS4], [LED],
[JSON], [ENG]. Kode fitur memakai awalan rumpun dari katalog:

| Awalan | Rumpun | Jumlah fitur | Halaman rumah |
|---|---|---:|---|
| KEP | kepercayaan | 10 | PG-01 |
| MNT | perencanaan maintenance | 9 | PG-02 |
| DAT | kualitas data | 10 | PG-03 |
| CMP | perbandingan mesin | 7 | PG-04 |
| LIN | linimasa dan jejak keputusan | 7 | PG-05 |
| INS | alat bantu insinyur | 5 | PG-06 |
| | **Total** | **48** | |

Jumlah 48 dan sebaran 10, 9, 10, 7, 7, 5 dibaca dari [KAT] baris 2585 sampai 2586, dan dihitung ulang
dengan `grep -c '^### '` yang keluarannya 48 di [KAT] baris 2683 sampai 2684.

---

## 2. Lima prinsip arsitektur

Kelima prinsip ini mengikat semua halaman. Setiap prinsip punya alasan yang bisa diperiksa, bukan
preferensi rasa.

**Prinsip 1: satu halaman menjawab satu pertanyaan.** Navigasi disusun dari pertanyaan pengguna, bukan
dari struktur berkas. Alasan: [VR] baris 10 mencatat bahwa pilihan visual ditentukan pertanyaan yang
ingin dijawab pembaca, dan prinsip yang sama berlaku untuk pilihan halaman. Konsekuensinya, halaman
rumpun dinamai dengan pertanyaannya, dan tidak ada halaman "semua angka".

**Prinsip 2: angka tidak pernah tampil sendirian.** Setiap angka model wajib tampil bersama pita
keyakinan, batas kelas, dan badge FAR pada blok yang sama. Alasan: satu angka keyakinan tanpa sebaran
dibaca sebagai kepastian, dan itu termasuk visual yang harus dihindari ([VR] baris 246); larangan
warna merah tanpa label manusia-peninjau juga sudah berlaku ([KAT] baris 203 sampai 207). Aturan
tampilan berjenjang untuk lima pita dan empat kode abstain ada di [DSS1] bagian 7.5.

**Prinsip 3: manusia selalu pemutus terakhir, dan tidak ada jalur yang melewatinya.** Tidak ada
halaman notifikasi otomatis, tidak ada tombol yang mengirim pesan sendiri, dan tidak ada tingkat yang
berakhir tanpa pembaca manusia. Alasan: `auto_critical_alarm_slots` bernilai 0 ([JSON] baris 1414),
asersi `AUTO_CRITICAL_SLOTS = 0` di [DSS4] baris 468, dan keempat tingkat dewan punya kolom pemutus
serta batas waktu ([DSS4] baris 461 sampai 466).

**Prinsip 4: kekurangan data adalah keadaan tampilan, bukan halaman galat.** Sistem ini punya lima
kode abstain, dua kepala lapis L3, dan empat kepala bisu. Semuanya tampil sebagai label bertekstur
dengan alasan tertulis, bukan sebagai angka nol dan bukan sebagai halaman kosong. Alasan: [DSS1]
baris 248 sampai 251 menetapkan pola garis miring dan teks alasan untuk abstain, dan [DSS3] bagian 5.4
menetapkan lencana bisu supaya kesepakatan semu tidak terbaca sebagai bukti.

**Prinsip 5: satu grafik satu satuan, panjang dan posisi untuk besaran.** Tidak ada dua sumbu Y, tidak
ada gauge, dan tidak ada donat untuk peluang. Alasan: dua sumbu Y membuat pembaca sulit menyimpulkan
dua deret sekaligus, dan gauge memakai sudut serta luas yang bukan kanal cepat untuk besaran
([VR] baris 244, 248, dan 265). Bila dua satuan harus tampil, bentuknya panel bersusun dengan sumbu x
sama atau keduanya diindeks ke nilai awal 100.

---

## 3. Peta halaman

Sepuluh halaman, satu halaman rumah untuk tiap rumpun, ditambah beranda, bukti angka, batas dan
syarat data, dan kamus. Setiap baris menyebut pertanyaan yang dijawab, fitur yang dipakai, pengguna
utama, dan status bukti terendah yang membatasi halaman itu.

| ID | Halaman | Pertanyaan yang dijawab | Fitur utama | Pengguna utama | Status bukti halaman |
|---|---|---|---|---|---|
| PG-00 | Beranda hari ini | Apa yang perlu saya lihat sekarang, dan seberapa kuat buktinya | KEP-03, KEP-02, MNT-01, LIN-02 | operator shift, supervisor, insinyur pengeboran | siap sekarang, dengan satu blok siap sebagian |
| PG-01 | Kepercayaan | Boleh saya percaya angka ini, dan sejauh mana | KEP-01 sampai KEP-10 | insinyur pengeboran, supervisor, dosen penguji, auditor | siap sekarang, dua fitur siap sebagian, satu rancangan |
| PG-02 | Perencanaan maintenance | Apa yang saya kerjakan shift ini, dan berapa menit tersedia | MNT-01 sampai MNT-09 | insinyur shift malam, toolpusher, supervisor pemeliharaan | siap sekarang, dua fitur siap sebagian |
| PG-03 | Kualitas data | Apakah data yang menopang angka ini ada dan layak dipakai | DAT-01 sampai DAT-10 | engineer PdM, koordinator data, auditor | siap sekarang, dua fitur siap sebagian |
| PG-04 | Perbandingan mesin | Mesin mana yang lebih baik, pada kelas apa, dan dengan harga apa | CMP-01 sampai CMP-07 | peneliti, dosen penguji, PM | siap sekarang, dua fitur siap sebagian |
| PG-05 | Linimasa keputusan | Apa yang diputuskan, kapan, oleh siapa, dan apa akibatnya | LIN-01 sampai LIN-07, SWARM-02, SWARM-05 | supervisor, auditor, dosen penguji | siap sebagian untuk log, siap sekarang untuk garis waktu |
| PG-06 | Alat bantu insinyur | Langkah apa yang harus dijalankan sebelum memindahkan ambang atau mengutip angka | INS-01 sampai INS-05 | engineer pemasangan, auditor internal, koordinator data | siap sebagian untuk empat fitur, siap sekarang untuk satu |
| PG-07 | Bukti angka | Dari mana angka ini, dan boleh dikutip atau belum | KEP-05, KEP-07, INS-02, LIN-05 | auditor, penulis laporan, PM | siap sekarang |
| PG-08 | Batas dan syarat data | Apa yang belum ada, siapa pemiliknya, dan apa syaratnya | KEP-09, KEP-10, DAT-05, DAT-08, INS-04, INS-05 | perencana maintenance, manajer, koordinator data | siap sebagian, dengan slot pemilik data |
| PG-09 | Kamus dan kuis angka | Istilah ini artinya apa, dan bagaimana angka ini diuji | LIN-06, KEP-06, SWARM-02 | dosen penguji, PM, staf baru | siap sekarang |

Jumlah baris data tabel di atas: 10.

Tiga aturan peta yang mengikat:

1. Tidak ada halaman ke-11. Setiap fitur baru wajib masuk ke salah satu dari sepuluh halaman ini,
   atau menggantikan satu halaman, bukan menambah menu. Alasan: menu dengan lebih dari tujuh butir
   memperlambat pemindaian, dan jumlah rumpun yang mengikat adalah enam.
2. Halaman rumpun memakai urutan yang sama dengan katalog, karena kode fitur dipakai lintas dokumen
   dan lintas kartu. Membalik urutan akan memutus rujukan yang sudah tertulis di [KAT], [DSS1],
   [DSS2], [DSS3], dan [DSS4].
3. Halaman PG-07, PG-08, dan PG-09 tidak berisi fitur baru. Ketiganya adalah halaman lintas rumpun
   yang menjawab pertanyaan yang muncul di semua rumpun: asal angka, syarat data, dan arti istilah.

### 3.1 Navigasi utama

Tujuh butir menu utama, urut sebagai berikut: Beranda, Kepercayaan, Perencanaan, Data, Mesin,
Linimasa, Bukti. Tiga halaman lain dicapai lewat kaki halaman dan lewat tautan di dalam blok: PG-06
Alat bantu ditautkan dari PG-01, PG-02, dan PG-07; PG-08 Batas data ditautkan dari setiap badge
abstain; PG-09 Kamus ditautkan dari setiap istilah bertanda.

Alasan urutan ini: pertanyaan pertama operator adalah "apa yang perlu dilihat" (Beranda), pertanyaan
kedua adalah "boleh dipercaya" (Kepercayaan), ketiga adalah "apa yang dikerjakan" (Perencanaan).
Data, Mesin, dan Linimasa adalah pertanyaan yang datang belakangan, biasanya saat angka dipertanyakan.
Bukti adalah pertanyaan terakhir, dan justru paling sering dibuka auditor serta dosen penguji.

---
## 4. Sepuluh halaman

Setiap halaman ditulis dengan pola yang sama: tujuan, pengguna dan momen pakai, blok konten, aksi
utama, bukti yang ditampilkan, keadaan khusus, dan salah tafsir yang harus dicegah. Pola ini mengikuti
lima field wajib kerangka butir 5, ditambah dua field yang dibutuhkan tim bangun.

### 4.1 PG-00 Beranda hari ini

**Tujuan.** Menjawab satu pertanyaan dalam satu layar: apa yang perlu dilihat sekarang, dan seberapa
kuat buktinya. Masalah yang diselesaikan: hari ini pembaca membuka dokumen dan melihat 11 klaim mesin
sebagai satu tumpukan angka, lalu menyimpulkan kemampuan yang lebih besar daripada buktinya
([KAT] baris 219 sampai 223).

**Pengguna dan momen pakai.** Operator monitoring setiap kali membuka halaman, puluhan kali per shift
([DSS1] baris 883 sampai 884). Supervisor saat serah terima, dua kali per shift. Insinyur pengeboran
saat memutuskan apakah satu klaim naik ke antrean kerja, beberapa kali per shift.

**Blok konten.**

| No | Blok | Isi | Sumber | Fitur |
|---|---|---|---|---|
| 1 | Banner tingkat dewan | Satu baris: tingkat TK, nama tingkat, dukungan berbobot S dalam persen, kuorum hadir, cakupan bobot, dan waktu hitung | [DSS4] baris 393 sampai 398, 419 sampai 422, 447 sampai 455 | SWARM-02, SWARM-03 |
| 2 | Tiga kartu fokus | Maksimal tiga kartu berisi klaim, jendela, lencana pita, satu batang 0 sampai 1 dengan garis batas kelas, jumlah kepala dinilai, badge FAR, lead, dan umur | [DSS2] baris 641 sampai 651 | KEP-02, MNT-01 |
| 3 | Ringkasan beban shift | Empat angka: perkiraan baris per shift, nilai tengah, persentil 95, dan sisa anggaran menit | [DSS2] baris 145 sampai 148, 481 sampai 496 | MNT-05, ANT-03 |
| 4 | Antrean ringkas | Lima baris teratas tabel antrean, dengan tautan ke halaman penuh dan penghitung baris tunda | [DSS2] baris 482 sampai 490 | MNT-01 |
| 5 | Penanda larangan otomatis | Satu label tetap: nol slot alarm otomatis, keputusan akhir manusia | [JSON] baris 1414, [DSS4] baris 468 | KEP-03 |
| 6 | Baris keadaan data | Jumlah klaim abstain hari ini beserta kode dan alasan terpendek | [DSS1] baris 241 sampai 246, [DSS2] baris 490 | KEP-02, DAT-08 |
| 7 | Kaki bukti | Tanggal potong data, versi katalog, dan tautan ke PG-07 | [KAT] baris 3 dan 251 | KEP-05 |

**Aksi utama.** "Buka antrean shift" menuju PG-02 dengan anggaran 30 menit dan urutan berlapis yang
sama. Aksi kedua, "Catat keputusan", membuka formulir satu baris yang menulis ke log keputusan
(LIN-01) dan menutup baris antrean sehingga umurnya berhenti bertambah ([KAT] baris 2085 sampai 2089).

**Bukti yang ditampilkan.**

| Angka | Nilai | Sumber |
|---|---|---|
| Tingkat dewan pada segmen terakhir | TK-2 PANTAU | [DSS4] baris 14 dan 393 sampai 396 |
| Dukungan berbobot setelah batas dominasi | 18,23 persen | [DSS4] baris 454 |
| Kuorum hadir | 6 dari 7 engine | [DSS4] baris 427 |
| Cakupan bobot | 1,00 | [DSS4] baris 427 |
| Beban tinjauan per shift | 40,15 baris, p50 39, p95 61 | [DSS2] baris 145 sampai 148 |
| Kapasitas anggaran 30 menit | 7 sampai 9 baris, 9 terlayani pada contoh | [DSS2] baris 491 sampai 505 |
| Slot alarm otomatis | 0 | [JSON] baris 1414 |
| Kepala per lapisan | 5 L0, 11 L1, 9 L2, 2 L3, total 27 | [JSON] `decision_layer.ringkasan`, dikutip [KAT] baris 264 |

**Keadaan khusus.** Bila tidak ada klaim pada pita P2 ke atas, banner menampilkan TK-1 TENANG dan
blok 2 diganti satu kalimat "jendela tenang, tidak ada baris antrean baru", sesuai syarat TK-1
([DSS4] baris 395). Bila beban melewati anggaran, angka tunda wajib tampil di blok 3, bukan di catatan
kaki, karena [DSS2] baris 502 sampai 505 menyebut jumlah tunda sebagai angka yang wajib dibaca
supervisor.

**Salah tafsir yang harus dicegah.** Pertama, membaca TK-2 sebagai "tidak ada masalah"; TK-2 berarti
bahan pantau, bukan antrean kerja ([DSS4] baris 396). Kedua, membaca 40,15 sebagai jumlah alarm bahaya;
angka itu mengukur beban tinjauan, bukan risiko ([DSS2] baris 502 sampai 505). Ketiga, membaca angka
keyakinan sebagai peluang kerusakan; labelnya "keyakinan bukti", dan 61 persen berarti `K_tampil` 0,61
([DSS1] baris 923 sampai 924).

### 4.2 PG-01 Kepercayaan

**Tujuan.** Menjawab pertanyaan "boleh saya percaya angka ini, dan sejauh mana" untuk setiap angka
model yang tampil di situs. Halaman ini adalah rumah rumpun kepercayaan, 10 fitur, dan rumah aturan
tampilan yang dipakai halaman lain.

**Pengguna dan momen pakai.** Insinyur pengeboran dan supervisor shift, dibuka sebelum mempercayai
badge kelas mana pun dan saat serah terima, dua kali per shift ([KAT] baris 231 sampai 233). Dosen
penguji sekali per sesi bimbingan ([KAT] baris 233). Auditor internal sekali per bulan ([DSS1] baris
896).

**Blok konten.**

| No | Blok | Isi | Sumber | Fitur |
|---|---|---|---|---|
| 1 | Baris ringkas papan vonis | Satu baris angka: 27 kepala, 5 L0, 11 L1, 9 L2, 2 L3, 0 slot alarm otomatis | [KAT] baris 258 sampai 264, [JSON] `decision_layer.ringkasan` | KEP-01 |
| 2 | Papan vonis | Sebelas kartu, satu per klaim, urutan tetap: nama kelas, tugas satu kalimat, lencana tier, dua sampai empat angka penopang, daftar syarat menggantung, tanggal potong | [KAT] baris 253 sampai 264 | KEP-01 |
| 3 | Kartu keyakinan | Tiga zona: judul (klaim, jendela, pita, persen), bukti (kepala dinilai, badge kalibrasi, badge FAR), alasan (batas kelas, tiga komponen, tanggal rujukan) | [DSS1] baris 869 sampai 951 | KEP-02, DSS-05 |
| 4 | Batang keyakinan | Batang mendatar 0 sampai 1 dengan garis batas kelas dan persen sebagai teks di ujung batang | [DSS1] baris 927 sampai 929 | KEP-02 |
| 5 | Badge beban alarm | Jumlah alarm per 24 jam kalender dengan satuan tertulis, dan label bila satuan berbeda | [KAT] baris 365 sampai 406 | KEP-03 |
| 6 | Panel ketidaksepakatan | Putusan tiap kepala pada jendela yang sama, dan daftar pasangan kembar | [KAT] baris 673 sampai 717, [DSS3] bagian 5.1 | KEP-08 |
| 7 | Kurva kalibrasi | Reliability diagram per engine dengan garis diagonal, jumlah bin, dan label "rancangan" selama ECE belum diukur | [KAT] baris 434 sampai 473, [VR] baris 163 sampai 167 | KEP-04 |
| 8 | Papan dua pembacaan | Satu klaim, dua pembacaan (literal dan ketat), selisihnya, dan sebab selisih | [KAT] baris 571 sampai 620 | KEP-06 |
| 9 | Gerbang provenance | Tiga warna label pada setiap angka: boleh dikutip, boleh dikutip dengan catatan metode, belum boleh dikutip | [KAT] baris 501 sampai 570 | KEP-05 |
| 10 | Banner bit_wear | Satu kalimat tetap bahwa label keausan bit adalah indeks mekanika, bukan observasi keausan | [KAT] baris 744 sampai 795 | KEP-09 |
| 11 | Slot nilai lapisan B | Lima slot kosong berlabel pemilik data untuk menerjemahkan jam henti ke nilai uang | [KAT] baris 796 sampai 838 | KEP-10 |

**Aksi utama.** "Buka alasan" pada satu kartu, yang membuka tiga komponen S_A, S_B, S_C beserta
rujukan barisnya. Tidak ada tombol tindakan pada pita P1 dan P2, dan itu keputusan tampilan, bukan
kekurangan: tombol tidak dirender pada dua pita itu ([DSS1] baris 899 sampai 900 dan 976).

**Bukti yang ditampilkan.**

| Angka | Nilai | Sumber |
|---|---|---|
| Batas lima pita | P1 0,00 sampai 0,19; P2 0,20 sampai 0,39; P3 0,40 sampai 0,59; P4 0,60 sampai 0,79; P5 0,80 sampai 1,00 | [DSS1] baris 219 sampai 225 |
| Batas atas bukti kelas hyd K-i | 0,6100, pita tertinggi P4 | [DSS4] baris 441 |
| Batas atas bukti kelas vib | 0,4950, pita tertinggi P3 | [DSS4] baris 437 |
| Batas atas bukti kelas bit_wear K-1 | 0,2525, pita tertinggi P2 | [DSS4] baris 442 |
| FAR komposisi hyd H1p | 4,0984 per 24 jam kalender | [LED] baris 3292, entri S6-058 |
| Lead median komposisi hyd H1p | 8,0 menit | [LED] baris 3432, entri E5-007 |
| Keyakinan tampil pada contoh segmen | 0,6100 hyd K-i (61 persen) | [DSS1] baris 400 sampai 414 |
| Kode abstain | AB-1 tanpa kepala berskor, AB-2 data sensor kurang, AB-3 skor jendela belum diekspor, AB-4 klaim lapis L3, AB-5 kepala bisu | [DSS1] baris 241 sampai 246, [DSS4] baris 9 |

**Keadaan khusus.** Empat kode abstain AB-1 sampai AB-4 tampil sebagai kartu redup berpola garis
miring, angka diganti tanda dan alasan, dan kartu tetap muncul di urutan dengan penanda "menunggu
data" ([DSS1] baris 248 sampai 251). Klaim lapis L3 hanya boleh menampilkan keadaan abstain, tanpa
pita ([DSS1] baris 260). Contoh nyata: `ssi.rule_display` dengan `n_nodata` 5.268 dari 5.455 jendela,
yaitu 0,9657, memicu AB-2 ([DSS1] baris 244).

**Salah tafsir yang harus dicegah.** Pertama, membaca tier sebagai mutu model; tier menilai kesiapan
pemakaian, dan engine dengan sinyal kuat bisa bertier rendah karena lapisan B belum terukur
([KAT] baris 275 sampai 281). Kedua, membaca 0 slot alarm sebagai kegagalan; itu keputusan desain
([KAT] baris 279 sampai 281). Ketiga, menjumlahkan tier antar kelas menjadi satu skor armada, yang
dilarang karena kelas tidak sebanding ([KAT] baris 278 sampai 279).

### 4.3 PG-02 Perencanaan maintenance

**Tujuan.** Menjawab "apa yang saya kerjakan shift ini, dan berapa menit tersedia". Halaman ini
mengubah skor menjadi daftar berurut dengan umur item, lalu memotongnya dengan anggaran waktu yang
tertulis, sehingga daftar tidak pernah menjadi tumpukan tanpa ujung ([KAT] baris 873 sampai 876,
[DSS2] bagian 5).

**Pengguna dan momen pakai.** Insinyur shift malam dan toolpusher pada awal shift dan setiap dua jam,
lima kali per shift 12 jam ([KAT] baris 884 sampai 885). Supervisor pagi sekali untuk serah terima.
Perencana tenaga kerja sekali per minggu untuk penaksir beban ([KAT] baris 1099 sampai 1103).

**Blok konten.**

| No | Blok | Isi | Sumber | Fitur |
|---|---|---|---|---|
| 1 | Banner anggaran | Anggaran menit, jumlah terlayani, jumlah ditunda, total menit tunda | [DSS2] baris 481 sampai 496 | ANT-03 |
| 2 | Tabel antrean | Sembilan kolom tampil: nomor, klaim, jendela, kepala, keyakinan, pita, umur, menit, aksi. FAR, lead, dan interval adalah muatan baris yang tampil pada kartu detail saat satu baris dibuka | [DSS2] baris 601 sampai 603, 610 sampai 623, dan 648 sampai 651 | ANT-01 |
| 3 | Tiga kartu fokus | Maksimal tiga baris teratas, alasannya karena p95 hyd K-i hanya 10 baris | [DSS2] baris 641 sampai 651 | ANT-01 |
| 4 | Penanda umur | Empat pita umur per shift: 0 sampai 15, 16 sampai 60, 61 sampai 120, di atas 120 menit | [DSS2] baris 622 sampai 626 | ANT-04 |
| 5 | Urutan berlapis | Empat lapis urutan dan jatah minimum per klaim, supaya satu engine tidak mengisi seluruh anggaran | [DSS2] baris 189 sampai 240 | ANT-02 |
| 6 | Neraca penundaan | Jumlah baris tunda dan menit kekurangan, dihitung terhadap anggaran | [DSS2] baris 365 sampai 377 | ANT-03 |
| 7 | Beban per shift | Lambda per klaim, p50, p95, dan total setelah deduplikasi | [DSS2] baris 136 sampai 149 | MNT-05 |
| 8 | Kalkulator pemeriksaan | Berapa pemeriksaan manual yang dihemat satu titik operasi, dengan biaya waktu per pemeriksaan | [KAT] baris 939 sampai 992 | MNT-02 |
| 9 | Pareto jam henti | Batang terurut menurun ditambah garis persentase kumulatif, dari 39.397,986 jam tercatat | [ENG] baris 19 sampai 27, [VR] baris 193 sampai 210 | KEP-10 |
| 10 | Sakelar titik operasi | Dua atau empat titik operasi yang sudah dihitung konsekuensinya, bukan satu tombol global | [KAT] baris 993 sampai 1050 | MNT-03, MNT-04 |
| 11 | Tiga keadaan antrean | Keadaan kosong, panjang, dan keyakinan rendah, masing-masing dengan teks dan tata letaknya | [DSS2] baris 509 sampai 591 | ANT-05 |

**Aksi utama.** "Tutup baris" pada satu baris antrean. Aksi ini menulis satu baris log keputusan,
menghentikan pertambahan umur, dan mengubah angka pada banner ([DSS2] baris 1053 sampai 1118).
Aksi kedua, "Tunda", wajib menulis alasan dan menambah angka tunda pada neraca.

**Bukti yang ditampilkan.**

| Angka | Nilai | Sumber |
|---|---|---|
| Beban per shift setelah dedup | 40,15 baris, p50 39, p95 61 | [DSS2] baris 145 sampai 148 |
| Lambda vib | 16,647, p50 16, p95 24 | [DSS2] baris 138 |
| Lambda hyd rule_display | 18,523, p50 18, p95 26 | [DSS2] baris 142 |
| Lambda hyd hibrida | 5,537, p50 5, p95 10 | [DSS2] baris 141 |
| Lambda shk | 2,206, p50 2, p95 5 | [DSS2] baris 139 |
| Lambda stuck K-i | 2,774, p50 3, p95 6 | [DSS2] baris 140 |
| Kapasitas anggaran 30 menit | 7 sampai 9 baris | [DSS2] baris 502 sampai 505 |
| Konsekuensi pada shift p95 | sekitar 52 baris ditunda, kekurangan sekitar 208 menit | [DSS2] baris 504 sampai 505 |
| Tinjauan hyd hibrida per shift | 6, dihitung dari ceil(16,611 dibagi 3) | [LED] baris 3433, entri E5-008 |
| Total jam tercatat DDR | 39.397,986 jam dari 23.447 record | [ENG] baris 21 sampai 22 |
| Henti karena equipment failure | 2.739,667 jam | [ENG] baris 25 |

**Keadaan khusus.** Keadaan kosong menampilkan kalimat "tidak ada baris pada pita P2 ke atas" beserta
jumlah jendela tenang, bukan tabel kosong ([DSS2] baris 514 sampai 532). Keadaan panjang menampilkan
tabel dengan sepuluh baris pertama dan penghitung tunda, bukan menggulir tak berujung
([DSS2] baris 533 sampai 564). Keadaan keyakinan rendah meredupkan baris tanpa tombol tindakan
([DSS2] baris 565 sampai 591).

**Salah tafsir yang harus dicegah.** Pertama, menjumlahkan rule dan hibrida; setiap alarm hibrida juga
alarm rule, sehingga menjumlahkan keduanya menghitung jendela yang sama dua kali, dan beban vib yang
benar 17, bukan 34 ([DSS2] baris 107 sampai 113). Kedua, membaca panjang daftar sebagai tanda bahaya;
panjang daftar mengukur beban ([KAT] baris 905 sampai 907). Ketiga, memakai angka tool_wear sebagai
kalender; satuannya per menit, dan angka 1.006,08 hanya berlaku bila dibaca sebagai kalender
([DSS2] baris 115 sampai 122).

---
### 4.4 PG-03 Kualitas data

**Tujuan.** Menjawab "apakah data yang menopang angka ini ada dan layak dipakai", sebelum pembaca
mempercayai panel mana pun. Halaman ini adalah rumah rumpun kualitas data, 10 fitur, dan tujuh di
antaranya justru dibangun dari kekurangan data ([KAT] baris 23 sampai 25).

**Pengguna dan momen pakai.** Engineer PdM dan supervisor sebelum menilai satu event ([KAT] baris
1324 sampai 1328). Koordinator data sekali per kampanye saat merencanakan perluasan cakupan
([KAT] baris 1550). Auditor dan ML engineer saat memeriksa jejak label ([KAT] baris 1426 sampai 1430).

**Blok konten.**

| No | Blok | Isi | Sumber | Fitur |
|---|---|---|---|---|
| 1 | Kartu kesiapan kanal | Satu kartu per sumur yang menyatakan kanal mana siap, mana tipis, mana absen, sebelum panel dinyalakan | [KAT] baris 1620 sampai 1675 | DAT-08 |
| 2 | Matriks ketersediaan berkas | Matriks sumur lawan jenis berkas, dengan sel berisi jumlah dan status unduh | [KAT] baris 1507 sampai 1542 | DAT-05 |
| 3 | Antrean parse | Tiga angka pembuka: 3.906 berkas belum diparse, 54,63 persen dari 7.150, dan 213 label terbuka | [KAT] baris 1554 sampai 1565 | DAT-06 |
| 4 | Kartu kelengkapan jendela | Fraksi kanal hadir pada satu jendela pra-event, plus vonis layak atau tidak | [KAT] baris 1324 sampai 1385 | DAT-01 |
| 5 | Kanal status tidak logging | Daftar kanal yang absen karena sumur tidak logging, bukan karena sensor rusak | [KAT] baris 1386 sampai 1425 | DAT-02 |
| 6 | Peta label ke fold | Jejak setiap label: masuk fold mana, atau gugur dengan alasan | [KAT] baris 1426 sampai 1467 | DAT-03 |
| 7 | Pemilih kanal | Fill rate dan QC fisik per kanal, dengan vonis pakai, pakai dengan catatan, atau tolak | [KAT] baris 1468 sampai 1506 | DAT-04 |
| 8 | Katalog label instrumen | Matriks sumur lawan label, dengan jumlah event sebagai pengiring | [KAT] baris 1582 sampai 1619 | DAT-07 |
| 9 | Peta drift | Selisih sebaran kanal antar sumur dan di dalam satu sumur | [KAT] baris 1676 sampai 1714 | DAT-09 |
| 10 | Validitas kedalaman | Penanda apakah fitur berbasis tekanan memakai kedalaman vertikal yang benar | [KAT] baris 1715 sampai 1757 | DAT-10 |

**Aksi utama.** "Minta data" pada satu baris yang absen, yang membuka kartu permintaan data
bertanda tangan (INS-05) berisi kanal, sumur, alasan angka, dan pemilik. Aksi kedua, "Buka bukti
kanal", menuju PG-07 pada baris ledger yang menopang status kanal itu.

**Bukti yang ditampilkan.**

| Angka | Nilai | Sumber |
|---|---|---|
| Berkas belum diparse | 3.906 dari 7.150, yaitu 54,63 persen | [KAT] baris 1554 sampai 1556 dan 1565 |
| Sebaran berkas belum diparse | F-1 C 2.156 dan F-11 1.750 | [KAT] baris 1554 sampai 1556 |
| Label tanpa fold | 213 label, tersebar di tiga wellbore F-15 B, C, D | [KAT] baris 1557 sampai 1558 |
| Kanal absen pada ssi rule_display | 5.268 dari 5.455 jendela, yaitu 0,9657 | [DSS1] baris 244 |
| Ambang abstain data sensor | `n_nodata / n_windows` lebih dari 0,50 | [DSS1] baris 244 |
| Jumlah fitur rumpun kualitas data | 10 | [KAT] baris 2585 |
| Fitur rumpun ini berstatus siap sebagian | 2 dari 10, yaitu DAT-04 dan DAT-08 | [KAT] baris 2598 |

**Keadaan khusus.** Kanal yang absen tidak ditampilkan sebagai nilai nol, melainkan sebagai badge
"tidak logging" dengan sebabnya ([KAT] baris 1386 sampai 1390). Sumur yang belum punya kanal lengkap
tetap punya halaman, dengan kartu kesiapan yang menyebut kanal mana yang belum ada dan apa syaratnya
([KAT] baris 1620 sampai 1628).

**Salah tafsir yang harus dicegah.** Pertama, membaca kanal absen sebagai sensor rusak; DAT-02
memisahkan sumur yang tidak logging dari kanal yang gagal ([KAT] baris 1390 sampai 1396). Kedua,
membaca 213 label gugur sebagai data hilang permanen; sebagian hanya menunggu fold ([KAT] baris 1463
sampai 1465). Ketiga, memakai kanal setengah kosong sebagai bukti fisik; itu justru yang dicegah
DAT-04 ([KAT] baris 1472 sampai 1476).

### 4.5 PG-04 Perbandingan mesin

**Tujuan.** Menjawab "mesin mana yang lebih baik, pada kelas apa, dan dengan harga apa", termasuk
ketika jawabannya adalah "keduanya sama" atau "keduanya tidak sepakat". Halaman ini adalah rumah
rumpun perbandingan mesin, 7 fitur, dan rumah tiga pola konflik dari spesifikasi ketidaksepakatan.

**Pengguna dan momen pakai.** Peneliti dan dosen penguji saat memeriksa klaim keunggulan
([KAT] baris 1764 sampai 1768). PM saat memilih komposisi head untuk satu kelas ([KAT] baris 1982
sampai 1986). Supervisor saat dua panel memberi arah berbeda ([DSS3] baris 20 sampai 23).

**Blok konten.**

| No | Blok | Isi | Sumber | Fitur |
|---|---|---|---|---|
| 1 | Balapan model lawan persistence | Satu baris per fold, dua nilai, selisih, dan vonis menang atau kalah | [KAT] baris 1764 sampai 1801 | CMP-01 |
| 2 | Peta kalah-menang per kelas | Matriks kelas lawan pasangan model, dengan sel berisi vonis dan selang | [KAT] baris 1802 sampai 1837 | CMP-02 |
| 3 | Tabel kanal melawan intuisi | Kanal yang ternyata tidak membantu, dengan angka pendukungnya | [KAT] baris 1838 sampai 1874 | CMP-03 |
| 4 | Rekam jejak per sumur | Jumlah kejadian nyata per sumur, sebagai batas atas klaim | [KAT] baris 1875 sampai 1907 | CMP-04 |
| 5 | Bukti sirkularitas | Penanda bahwa target mekanika yang direkonstruksi tidak layak jadi bukti | [KAT] baris 1908 sampai 1945 | CMP-05 |
| 6 | Lembar prasyarat eksperimen | Daftar prasyarat sebelum satu kesimpulan diambil dari satu jalan | [KAT] baris 1946 sampai 1981 | CMP-06 |
| 7 | Panel kesetaraan head hyd | Tiga komposisi head hyd, bentuk pertukaran presisi dan recall, dan rekomendasi | [KAT] baris 1982 sampai 2040 | CMP-07 |
| 8 | Matriks kesepakatan komponen | Matriks head lawan head per mesin, angka di dalam sel, versi mentah dan ternormalisasi | [DSS3] bagian 6.1 sampai 6.7 | DSS3-01 |
| 9 | Lencana pola konflik | Empat lencana: kembar, cakupan sebagian, saling meniadakan, bisu, masing-masing dengan alasan wajib | [DSS3] bagian 5.1 sampai 5.4, 9.2 | DSS3-02 |
| 10 | Peta ketidaksepakatan tingkat klaim | Tujuh mesin, sebelas klaim, enam sisi bukti, dengan kolom yang paling sering tidak disepakati | [DSS3] bagian 7.2 dan 7.3 | DSS3-03 |

**Aksi utama.** "Buka jendela" pada satu sel matriks, yang menampilkan putusan tiap kepala pada
jendela yang sama beserta jumlah aktifnya. Aksi kedua, "Bandingkan komposisi", yang membuka panel
kesetaraan head hyd ([KAT] baris 1982 sampai 2040).

**Bukti yang ditampilkan.**

| Angka | Nilai | Sumber |
|---|---|---|
| Head lapis L1 dan fungsi berbeda | 11 head, 7 fungsi, 4 pasangan identik | [DSS3] baris 25 sampai 26 |
| Putusan tiga head hyd | rule 975, persistence 876, hibrida 626 | [DSS3] baris 27 sampai 29 |
| Jendela yang hanya dimiliki satu head | 349 hanya rule, 250 hanya persistence | [DSS3] baris 29 |
| Kesepakatan status seluruh jendela | 92,47 sampai 99,43 persen | [DSS3] baris 30 sampai 31 |
| Kesepakatan pada kelas positif | 23,81 persen untuk shk, 0,00 persen Jaccard untuk ssi | [DSS3] baris 31 sampai 32 |
| Head yang tidak pernah menyala | ssi rule, ssi hibrida, ssi rf 0 dari 5.455; shk rf 0 dari 11.205 | [DSS3] baris 33 sampai 35 |
| Harga pemangkasan hid | alarm turun 35,79 persen, presisi naik 0,2017, recall turun 0,1052 | [DSS3] baris 36 sampai 37 |
| Harga pemangkasan tool_wear | alarm turun 93,11 persen, recall turun 0,6666 | [DSS3] baris 37 sampai 38 |

**Keadaan khusus.** Dua kepala identik tidak ditampilkan sebagai dua bukti; lencana kembar muncul
dengan alasan, dan bobotnya dideduplikasi sebelum dijumlahkan ([DSS4] baris 11 dan 338 sampai 355).
Kepala yang tidak pernah menyala ditampilkan sebagai bisu, bukan sebagai penolakan, dengan kode AB-5
([DSS4] baris 9 dan 356 sampai 366).

**Salah tafsir yang harus dicegah.** Pertama, membaca kesepakatan 92 sampai 99 persen sebagai bukti
kualitas; angka itu dihitung pada seluruh jendela, sementara pada kelas positif angkanya jatuh ke
23,81 persen ([DSS3] baris 30 sampai 32). Kedua, membaca kesepakatan 100 persen dengan kepala bisu
sebagai kesepakatan; itu dua pihak yang sama-sama diam ([DSS3] baris 33 sampai 35). Ketiga, membaca
pemangkasan sebagai perbaikan tanpa biaya; recall selalu turun, dan angkanya tertulis ([DSS3] baris 36
sampai 38).

### 4.6 PG-05 Linimasa keputusan

**Tujuan.** Menjawab "apa yang diputuskan, kapan, oleh siapa, dan apa akibatnya", sekaligus menjadi
rumah rumpun linimasa, 7 fitur. Halaman ini memisahkan tiga sumbu yang mudah tertukar: tier kepala,
pita klaim, dan tingkat dewan ([DSS4] baris 408 sampai 412).

**Pengguna dan momen pakai.** Supervisor setiap kali menutup peringatan, beberapa kali per shift
([KAT] baris 2080 sampai 2082). Auditor dan dosen penguji saat memeriksa urutan dokumen vonis
([KAT] baris 2114 sampai 2118). PM saat memeriksa posisi tier tiap kelas ([KAT] baris 2309 sampai 2313).

**Blok konten.**

| No | Blok | Isi | Sumber | Fitur |
|---|---|---|---|---|
| 1 | Tangga empat tingkat | Empat baris TK-1 sampai TK-4, syarat angka, pemutus, dan batas waktu | [DSS4] baris 393 sampai 398, 461 sampai 466 | SWARM-02 |
| 2 | Panel suara dewan | Suara tiap kepala per klaim: dukung, tolak, atau abstain dengan kode | [DSS4] bagian 8.1 | SWARM-01 |
| 3 | Meter kuorum | Kuorum hadir 4 dari 7 dan cakupan bobot minimum 0,50, dua angka terpisah | [DSS4] baris 419 sampai 422 | SWARM-03 |
| 4 | Buku konflik | Tujuh aturan konflik K-1 sampai K-7 dan lima pemicu turunnya manusia H-1 sampai H-5 | [DSS4] baris 482 sampai 502 | SWARM-05 |
| 5 | Log keputusan | Tabel waktu, kepala, label tindakan, dan alasan, dengan penghitung terbuka | [KAT] baris 2071 sampai 2110 | LIN-01 |
| 6 | Garis waktu gerbang | Urutan dokumen vonis, gerbang, dan perubahan target | [KAT] baris 2112 sampai 2146 | LIN-02 |
| 7 | Penanda selang | Setiap angka FAR dan recall wajib tampil bersama selangnya | [KAT] baris 2147 sampai 2196 | LIN-03 |
| 8 | Register status dokumen | Dokumen mana masih berlaku, mana sudah digantikan | [KAT] baris 2197 sampai 2240 | LIN-04 |
| 9 | Kalender sumber angka | Kapan setiap angka terakhir diuji, dan hasilnya | [KAT] baris 2241 sampai 2273 | LIN-05 |
| 10 | Linimasa tier kelas | Posisi tiap kelas pada tiga tingkat kesiapan dan syarat naik | [KAT] baris 2309 sampai 2352 | LIN-07 |

**Aksi utama.** "Catat keputusan" pada satu baris terbuka, yang menulis waktu, aktor, keputusan, dan
akibat ke log (LIN-01), lalu menutup baris tersebut ([KAT] baris 2085 sampai 2089). Aksi kedua,
"Buka aturan konflik", yang menampilkan aturan K-1 sampai K-7 beserta bukti yang memaksanya.

**Bukti yang ditampilkan.**

| Angka | Nilai | Sumber |
|---|---|---|
| Tingkat yang mungkin | TK-1 TENANG, TK-2 PANTAU, TK-3 TINJAU, TK-4 ESKALASI | [DSS4] baris 393 sampai 398 |
| Kuorum kehadiran | 4 dari 7 engine | [DSS4] baris 420 |
| Cakupan bobot minimum | 0,50 | [DSS4] baris 422 |
| Batas dominasi satu klaim | 35 persen bobot dewan | [DSS4] baris 447 |
| Pangsa hyd K-i sebelum dipotong | 36,07 persen dari 9,15 | [DSS4] baris 451 sampai 452 |
| Dukungan dewan pada segmen F-14 | 18,23 persen, tingkat TK-2 | [DSS4] baris 454 dan 14 |
| Batas waktu TK-3 | 1 shift, 8 jam | [DSS4] baris 465 |
| Batas waktu TK-4 | 1 jam | [DSS4] baris 466 |
| Aturan konflik bertabel | 7 baris, K-1 sampai K-7 | [DSS4] baris 482 sampai 491 |
| Pemicu turunnya manusia | 5 baris, H-1 sampai H-5 | [DSS4] baris 496 sampai 502 |
| Status log keputusan | siap sebagian, skema pencatatan belum ada | [KAT] baris 2104 |

**Keadaan khusus.** Selama log keputusan belum berisi, halaman menampilkan keadaan kosong dengan satu
kalimat yang membedakan "belum ada keputusan tercatat" dari "tidak ada peringatan", persis pembedaan
yang ditulis [KAT] baris 2076 sampai 2079. Bila konflik saling meniadakan muncul pada klaim penentu,
tingkat dibatasi TK-2 dan dua pembacaan ditampilkan berdampingan ([DSS4] baris 499).

**Salah tafsir yang harus dicegah.** Pertama, membaca tingkat dewan sebagai alarm; tidak ada tingkat
yang mengirim pesan sendiri ([DSS4] baris 474 sampai 476). Kedua, membaca label "abaikan" pada log
sebagai peringatan palsu; itu keputusan operator, bukan penilaian kebenaran model ([KAT] baris 2100
sampai 2102). Ketiga, mencampur tier kepala dengan tingkat dewan; keduanya sumbu berbeda dengan
pemutus berbeda ([DSS4] baris 408 sampai 412).

### 4.7 PG-06 Alat bantu insinyur

**Tujuan.** Menjawab "langkah apa yang harus dijalankan sebelum memindahkan ambang atau mengutip
angka". Halaman ini berisi prosedur, bukan panel angka, dan setiap prosedur punya keluaran yang bisa
diperiksa. Lima fitur, satu siap sekarang dan empat siap sebagian ([KAT] baris 2597 sampai 2599).

**Pengguna dan momen pakai.** Engineer pemasangan sebelum memindahkan ambang ke sumur baru
([KAT] baris 2358 sampai 2363). Auditor internal sekali per bulan saat menguji ulang satu keputusan
([KAT] baris 2420 sampai 2425). Peneliti sinyal sebelum menjalankan dekomposisi ([KAT] baris 2451
sampai 2456). Koordinator data saat menyusun permintaan data ([KAT] baris 2535 sampai 2540).

**Blok konten.**

| No | Blok | Isi | Sumber | Fitur |
|---|---|---|---|---|
| 1 | Wizard kalibrasi | Langkah berurutan sebelum pindah sumur: periksa drift, pilih titik operasi, uji jalan, catat hasil | [KAT] baris 2358 sampai 2419 | INS-01 |
| 2 | Panduan skrip verifikasi | Prosedur yang bisa dijalankan ulang untuk memeriksa satu angka, termasuk perintah dan keluarannya | [KAT] baris 2420 sampai 2450 | INS-02 |
| 3 | Kartu kelayakan sinyal | Vonis layak atau tidak sebelum VMD, EMD, atau wavelet dijalankan | [KAT] baris 2451 sampai 2495 | INS-03 |
| 4 | Kartu kanal yang perlu dipasang | Daftar permintaan pemasangan kanal, dengan alasan angka dan prioritas | [KAT] baris 2496 sampai 2534 | INS-04 |
| 5 | Kartu permintaan data bertanda tangan | Tiga ketiadaan terbukti diubah menjadi permintaan spesifik dengan pemilik dan tanda tangan | [KAT] baris 2535 sampai 2582 | INS-05 |
| 6 | Daftar periksa mutu angka | Enam pemeriksaan sebelum satu angka dikutip: sumber, baris, satuan, selang, tanggal, dan alat | [KAT] bagian 12, [KEP-07] | KEP-07 |

**Aksi utama.** "Jalankan pemeriksaan", yang menampilkan perintah verifikasi satu angka beserta
keluaran yang diharapkan. Aksi kedua, "Ajukan permintaan data", yang membuka kartu INS-05 dengan
kolom pemilik dan tanda tangan.

**Bukti yang ditampilkan.**

| Angka | Nilai | Sumber |
|---|---|---|
| Jumlah fitur rumpun alat bantu | 5 | [KAT] baris 2586 |
| Fitur siap sekarang di rumpun ini | 1, yaitu INS-02 | [KAT] baris 2597 |
| Fitur siap sebagian di rumpun ini | 4, yaitu INS-01, INS-03, INS-04, INS-05 | [KAT] baris 2598 |
| Ketiadaan yang menjadi isi kartu permintaan | 3 ketiadaan terbukti | [KAT] baris 2535 sampai 2540 |
| Uji yang wajib bisa gagal | uji mutasi angka pada pengunci rujukan | [KAT] baris 622 sampai 672 |

**Keadaan khusus.** Bila satu prosedur belum bisa dijalankan karena komponennya belum ada, halaman
menampilkan syarat yang dibutuhkan beserta pemiliknya, bukan tombol mati. Contoh: wizard kalibrasi
menampilkan langkah yang sudah bisa dijalankan dan langkah yang menunggu peta sumur.

**Salah tafsir yang harus dicegah.** Pertama, membaca prosedur sebagai izin memindahkan ambang; wizard
justru mencegah pemindahan tanpa uji ([KAT] baris 2360 sampai 2363). Kedua, membaca kartu permintaan
data sebagai keluhan; isinya spesifik, berangka, dan bertanda tangan ([KAT] baris 2535 sampai 2540).

---
### 4.8 PG-07 Bukti angka

**Tujuan.** Menjawab "dari mana angka ini, dan boleh dikutip atau belum". Halaman ini adalah satu
satunya tempat di situs yang menampilkan jalur angka dari berkas mentah sampai kalimat di layar, dan
halaman ini pula yang menahan angka yang belum boleh dikutip ([KAT] baris 501 sampai 570).

**Pengguna dan momen pakai.** Auditor internal sekali per bulan, dan setiap kali satu angka
dipertanyakan ([KAT] baris 2420 sampai 2425). Penulis laporan setiap kali mengutip angka ke dokumen
luar ([KAT] baris 506 sampai 511). PM saat memutuskan apakah satu angka masuk proposal.

**Blok konten.**

| No | Blok | Isi | Sumber | Fitur |
|---|---|---|---|---|
| 1 | Lencana provenance | Tiga warna label per angka: boleh dikutip, boleh dikutip dengan catatan metode, belum boleh dikutip | [KAT] baris 501 sampai 570 | KEP-05 |
| 2 | Tabel rujukan angka | Kolom: angka, nilai, satuan, berkas sumber, baris, status TERUKUR atau TURUNAN, tanggal uji | [LED] baris 3292, 3432, 3433; [KAT] baris 2241 sampai 2273 | LIN-05, KEP-07 |
| 3 | Pengunci rujukan | Pemeriksaan bahwa baris yang dirujuk benar benar berisi angka itu, bukan baris kosong | [KAT] baris 622 sampai 672 | KEP-07 |
| 4 | Uji mutasi | Uji yang sengaja merusak satu angka untuk membuktikan pemeriksa bisa gagal | [KAT] baris 622 sampai 672 | KEP-07 |
| 5 | Panduan skrip | Perintah yang bisa dijalankan ulang beserta keluaran yang diharapkan | [KAT] baris 2420 sampai 2450 | INS-02 |
| 6 | Papan satuan | Daftar satuan yang rawan tertukar: FAR per 24 jam kalender, FP per menit, tinjauan per shift | [DSS2] baris 115 sampai 122, [LED] baris 3292 dan 1155 | KEP-03 |
| 7 | Daftar dokumen belum dibuka | 119 dokumen di `docs/`, 69 di antaranya belum pernah dibuka, ditulis terbuka | [KAT] baris 2622 sampai 2625 | LIN-04 |
| 8 | Kaki berkas | Ukuran byte dan jumlah baris setiap berkas masukan dokumen ini | Bagian 1 berkas ini, [KAT] baris 39 sampai 47 | KEP-05 |

**Aksi utama.** "Periksa rujukan", yang membuka baris ledger dan baris berkas sumber berdampingan.
Aksi kedua, "Salin rujukan", yang menyalin pasangan berkas dan baris, bukan hanya angkanya.

**Bukti yang ditampilkan.**

| Angka | Nilai | Sumber |
|---|---|---|
| Ukuran ledger | 471.945 byte, 3.434 baris | `stat` dan `wc` pada bagian 13.1 |
| Entri S6-058 | 4,0984, satuan alarm per 24 jam kalender, status TERUKUR | [LED] baris 3292 |
| Entri E5-007 | 8,0, satuan menit, status TERUKUR | [LED] baris 3432 |
| Entri E5-008 | 6, satuan tinjauan per shift, status TURUNAN, rumus ceil(16,611 dibagi 3) | [LED] baris 3433 |
| Jumlah dokumen di `docs/` | 119, dengan 69 belum dibuka | [KAT] baris 2622 sampai 2625 |
| Warna provenance | 3 tingkat | [KAT] baris 501 sampai 507 |

**Keadaan khusus.** Angka yang belum boleh dikutip tetap tampil di halaman asalnya, tetapi dengan
lencana kuning atau merah dan tanpa kemampuan menyalin rujukan. Ini penerapan langsung kerangka butir
4: angka yang belum terverifikasi diperlakukan sebagai keadaan tampilan, bukan disembunyikan.

**Salah tafsir yang harus dicegah.** Pertama, membaca status TURUNAN sebagai angka lemah; E5-008 justru
turunan aritmetika sederhana dari angka TERUKUR, dan rumusnya tertulis di baris yang sama
([LED] baris 3433). Kedua, membaca 69 dokumen belum dibuka sebagai 69 angka salah; itu daftar periksa,
bukan vonis ([KAT] baris 2622 sampai 2625). Ketiga, menyalin angka tanpa satuannya; 2,096 bisa berarti
2,096 per 24 jam atau 1.006,08 per shift, dan perbedaan satuan itu sudah tercatat ([DSS2] baris 115
sampai 122).

Catatan koreksi yang diterapkan di dokumen ini: [DSS2] baris 79 sampai 80 menulis bahwa lead 8,0 menit
tercatat di [LED] baris 3436. Pemeriksaan pada bagian 13.7 menunjukkan berkas ledger berakhir di baris
3.434, sehingga baris 3436 tidak ada, dan entri E5-007 berada di baris 3432. Dokumen ini memakai baris
3432, dan selisih itu dicatat di bagian 12.

### 4.9 PG-08 Batas dan syarat data

**Tujuan.** Menjawab "apa yang belum ada, siapa pemiliknya, dan apa syaratnya". Halaman ini adalah
rumah resmi pola Dynamic Island: setiap kekurangan data tampil sebagai kartu berlabel dengan pemilik
dan syarat, bukan sebagai kalimat penutup ([KAT] baris 23 sampai 28, 2618 sampai 2645).

**Pengguna dan momen pakai.** Perencana maintenance dan manajer saat memutuskan nilai uang dari satu
peringatan ([KAT] baris 796 sampai 800). Koordinator data saat menyusun permintaan ([KAT] baris 2535
sampai 2540). Pembimbing dan reviewer saat memeriksa batas klaim ([KAT] baris 144).

**Blok konten.**

| No | Blok | Isi | Sumber | Fitur |
|---|---|---|---|---|
| 1 | Peta kode abstain | Lima kode AB-1 sampai AB-5, syarat terpicu, tampilan, dan satu contoh nyata per kode | [DSS1] baris 241 sampai 246, [DSS4] baris 9 | KEP-02 |
| 2 | Peta lapis L3 | Dua kepala lapis L3, statusnya, dan alasan tidak dinilai | [JSON] `decision_layer.layers.L3`, [DSS1] baris 260 | KEP-01 |
| 3 | Slot nilai lapisan B | Lima slot kosong berlabel pemilik data untuk tarif biaya henti | [KAT] baris 828 sampai 838 | KEP-10 |
| 4 | Syarat per fitur | Sepuluh butir syarat dari katalog, termasuk cacat pemblokir C-01 sampai C-05 | [KAT] baris 2618 sampai 2645 | KEP-05 |
| 5 | Peta pemilik data | Siapa memiliki peta sumur, tarif biaya, identitas alat, kanal baru, dan deret per menit | [KAT] baris 2612 sampai 2614 | INS-04, INS-05 |
| 6 | Status per fitur | 32 siap sekarang, 15 siap sebagian, 1 rancangan, dengan kode fiturnya | [KAT] baris 2597 sampai 2599 | KEP-05 |
| 7 | Larangan tampilan | Sembilan visual yang harus dihindari, termasuk dua sumbu Y, gauge, dan skor tunggal sebagai bukti kalibrasi | [VR] baris 240 sampai 256 | KEP-04 |

**Aksi utama.** "Buka syarat", yang menampilkan syarat satu fitur beserta pemilik data dan uji yang
sudah ada. Aksi kedua, "Minta akses data", yang membuka kartu INS-05 dengan kolom tanda tangan.

**Bukti yang ditampilkan.**

| Angka | Nilai | Sumber |
|---|---|---|
| Kode abstain | 5, yaitu AB-1 sampai AB-5 | [DSS1] baris 241 sampai 246, [DSS4] baris 9 |
| Kepala lapis L3 | 2, yaitu hyd k2_tidak_tersedia dan bit_wear k2_onset_belum | [JSON] `decision_layer.layers.L3` |
| Slot nilai kosong lapisan B | 5 slot | [KAT] baris 834 |
| Fitur siap sekarang | 32 | [KAT] baris 2597 |
| Fitur siap sebagian | 15 | [KAT] baris 2598 |
| Fitur masih rancangan | 1, yaitu KEP-04 | [KAT] baris 2599 |
| Fitur yang dibangun dari kekurangan data | 7, yaitu DAT-02, DAT-05, DAT-06, DAT-08, DAT-09, KEP-10, INS-05 | [KAT] baris 23 sampai 25 |
| Visual yang harus dihindari | 9 baris | [VR] baris 240 sampai 254 |

**Keadaan khusus.** Halaman ini sengaja tidak punya keadaan kosong. Bila satu syarat sudah terpenuhi,
barisnya berubah menjadi "terpenuhi" dengan tanggal dan bukti, seperti yang sudah dicontohkan untuk
berkas katalog pada [VR] baris 273. Dengan begitu halaman ini tetap berguna pada hari pertama, bukan
hanya pada hari ketika semuanya sudah tersedia.

**Salah tafsir yang harus dicegah.** Pertama, membaca halaman ini sebagai daftar kekurangan; isinya
syarat, pemilik, dan uji, dan setiap baris punya satu langkah berikutnya. Kedua, membaca abstain
sebagai nilai nol; abstain adalah status yang menggantikan angka, dengan kode ([DSS1] baris 238 sampai
239). Ketiga, mengisi slot nilai dengan angka karangan; slot kosong lebih jujur daripada angka tanpa
pemilik.

### 4.10 PG-09 Kamus dan kuis angka

**Tujuan.** Menjawab "istilah ini artinya apa, dan bagaimana angka ini diuji", untuk pembaca baru,
dosen penguji, dan staf yang berganti shift. Halaman ini juga menjadi tempat kuis dua halaman yang
sudah diminta katalog ([KAT] baris 2274 sampai 2308).

**Pengguna dan momen pakai.** Dosen penguji sekali per sesi ([KAT] baris 2276 sampai 2278). Staf baru
pada hari pertama. PM saat menyiapkan jawaban atas pertanyaan angka.

**Blok konten.**

| No | Blok | Isi | Sumber | Fitur |
|---|---|---|---|---|
| 1 | Kamus lima belas istilah | Tier kepala, lapisan L0 sampai L3, pita P1 sampai P5, kode abstain AB, tingkat TK, keyakinan bukti, FAR, lead, umur item, cakupan, kuorum, batas dominasi, ECE, kembar, bisu | [DSS1] bagian 4, [DSS4] bagian 5, [DSS3] bagian 5 | LIN-06 |
| 2 | Peta tiga sumbu | Tabel yang memisahkan tier kepala, pita klaim, dan tingkat dewan beserta pemutusnya | [DSS4] baris 408 sampai 412 | SWARM-02 |
| 3 | Kuis dua halaman | Sepuluh pertanyaan angka dengan jawaban yang bisa diperiksa, dan batas tiap angka | [KAT] baris 2274 sampai 2308 | LIN-06 |
| 4 | Contoh baca angka | Satu angka yang sama dibaca benar dan dibaca salah, dengan sebab kesalahannya | [DSS1] baris 923 sampai 924, [KAT] baris 275 sampai 281 | KEP-06 |
| 5 | Daftar istilah terlarang | Tiga istilah yang tidak dipakai di layar beserta penggantinya: "alarm" untuk tingkat dewan, "peluang rusak" untuk keyakinan bukti, dan "prioritas" untuk pita P1 sampai P5 | [DSS4] baris 391 dan 474 sampai 476, [DSS1] baris 224 dan 923 sampai 924 | KEP-06 |

**Aksi utama.** "Mulai kuis", yang menampilkan sepuluh pertanyaan dan menilai jawaban terhadap angka
yang tercatat di [KAT] bagian 11 serta [DSS4] bagian 5.

**Bukti yang ditampilkan.**

| Angka | Nilai | Sumber |
|---|---|---|
| Jumlah istilah pada kamus | 15 | daftar blok 1, bersumber [DSS1], [DSS3], [DSS4] |
| Jumlah pertanyaan kuis | 10 | [KAT] baris 2274 sampai 2308 |
| Batas pita P4 | 0,60 sampai 0,79 | [DSS1] baris 224 |
| Ambang TK-3 | kuorum 4 dari 7, cakupan 0,50, dua klaim P3, S 0,40, beban 30 menit ke bawah | [DSS4] baris 397 |
| Jumlah tingkat dewan | 4 | [DSS4] baris 393 sampai 398 |
| Jumlah lapisan pemakaian | 4, yaitu L0 sampai L3 | [JSON] `decision_layer.ringkasan` |

**Keadaan khusus.** Kamus tidak bergantung pada data yang belum ada, sehingga halaman ini berstatus
siap sekarang. Bila satu istilah berubah, perubahan wajib lewat pengunci rujukan (KEP-07), dan baris
kamus yang menyebutnya ikut diperbarui ([KAT] baris 2644 sampai 2645).

**Salah tafsir yang harus dicegah.** Pertama, membaca "keyakinan 61 persen" sebagai peluang kerusakan;
itu keyakinan bukti, dan artinya `K_tampil` 0,61 ([DSS1] baris 923 sampai 924). Kedua, membaca "P4"
sebagai prioritas empat; P4 adalah pita keyakinan ([DSS1] baris 224). Ketiga, membaca "TK-4" sebagai
tingkat bahaya; TK-4 adalah tingkat urgensi manusia melihat, dengan keputusan tetap di manusia
([DSS4] baris 398).

---

## 5. Alur pengguna

Alur ditulis sebagai urutan tindakan yang bisa diuji, bukan sebagai narasi. Setiap langkah menyebut
halaman, angka yang dibaca, dan keputusan yang diambil.

### 5.1 Alur 30 detik pertama

Ukuran lulus: dalam 30 detik sejak halaman terbuka, pembaca sudah tahu tingkat dewan hari itu,
tiga klaim teratas, ukuran beban shift, dan satu tindakan berikutnya. Tidak ada modal, tidak ada
layar masuk di tengah, dan tingkat dewan wajib terlihat tanpa menggulir.

| Detik | Yang terlihat | Angka yang dibaca | Keputusan yang diambil |
|---|---|---|---|
| 0 sampai 3 | Banner tingkat dewan di paling atas, satu baris, teks besar | TK-2 PANTAU, dukungan 18,23 persen, kuorum 6 dari 7 | "Hari ini tidak ada eskalasi, ada bahan pantau" ([DSS4] baris 454) |
| 3 sampai 8 | Tiga kartu fokus, masing masing dengan lencana pita dan satu batang | hyd K-i 20 pada 61 persen, vib 429 pada 50 persen, shk 20 pada 52 persen | "Yang paling kuat hari ini hyd K-i, bukan vib" ([DSS2] baris 615 sampai 617) |
| 8 sampai 15 | Ringkasan beban shift: empat angka | 40,15 baris per shift, p50 39, p95 61, sisa anggaran 30 menit | "Beban hari ini di atas kapasitas 7 sampai 9 baris, jadi harus dipilih" ([DSS2] baris 145 sampai 148, 502) |
| 15 sampai 22 | Lima baris antrean teratas dengan kolom umur | Pita, umur, menit per baris, dan angka tunda | "Lima baris teratas umur nol menit, baris keenam stuck K-ii umur empat menit pada P2 di luar anggaran, dan satu baris abstain ssi 118 dengan alasan AB-2" ([DSS2] baris 615 sampai 624) |
| 22 sampai 30 | Satu kartu keyakinan terbuka, tiga zona | Batas kelas, tiga komponen S_A S_B S_C, badge FAR, lead | "Angka ini 61 persen karena batas kelasnya 61, bukan karena skornya mentah" ([DSS1] baris 400 sampai 414) |

Empat hal yang dilarang pada 30 detik pertama, karena masing masing menghapus satu detik yang
dibutuhkan: layar masuk yang menutup banner, modal pengumuman, animasi pembuka lebih dari 300
milidetik, dan tabel yang memaksa gulir horizontal untuk melihat pita keyakinan.

### 5.2 Alur insinyur satu shift

| Langkah | Halaman | Tindakan | Keluaran | Waktu |
|---:|---|---|---|---|
| 1 | PG-00 | Baca banner tingkat dan kuorum | Tingkat TK dan dukungan berbobot | 30 detik |
| 2 | PG-00 | Baca tiga kartu fokus | Tiga klaim teratas dengan pita | 1 menit |
| 3 | PG-02 | Buka antrean, periksa banner anggaran | Anggaran 30 menit, jumlah terlayani dan tertunda | 2 menit |
| 4 | PG-02 | Saring pita P4 dan P3, lalu baca kolom umur | Baris yang wajib dilihat lebih dulu | 3 menit |
| 5 | PG-01 | Buka kartu keyakinan satu baris | Pita, persen, batas kelas, tiga komponen, badge FAR, lead | 2 menit |
| 6 | PG-03 | Periksa kartu kesiapan kanal untuk klaim itu | Kanal siap, tipis, atau absen | 2 menit |
| 7 | PG-04 | Bila dua kepala berbeda, buka panel ketidaksepakatan | Dua putusan berdampingan dan selisihnya | 3 menit |
| 8 | PG-01 | Bila FAR di atas 6 per 24 jam, buka badge beban | Beban tinjauan, bukan risiko | 1 menit |
| 9 | PG-01 | Bila perlu, buka papan dua pembacaan | Selisih pembacaan literal dan ketat | 2 menit |
| 10 | PG-02 | Putuskan: kerjakan, tunda dengan alasan, atau tutup | Satu baris log keputusan, umur berhenti | 1 menit per baris |
| 11 | PG-05 | Serah terima: papan tiga kolom baru, sedang diperiksa, ditunda | Daftar yang belum selesai | 5 menit |
| 12 | PG-05 | Periksa tingkat tindak lanjut setelah shift | Rasio baris berlabel terhadap baris tampil | 2 menit |

Total waktu untuk lima baris teratas: sekitar 20 menit, di dalam anggaran 30 menit yang ditetapkan
[DSS2] bagian 5. Bila lima baris itu semuanya P4 dan P3, biaya per baris 4 sampai 6 menit sesuai
jadwal pada [DSS2] baris 483 sampai 491.

### 5.3 Alur auditor

1. Buka PG-07, pilih satu angka dari tabel rujukan, dan baca pasangan berkas serta barisnya.
2. Bandingkan dengan baris ledger: S6-058 pada [LED] baris 3292, E5-007 pada [LED] baris 3432,
   E5-008 pada [LED] baris 3433.
3. Jalankan panduan skrip pada PG-06 butir 2, lalu bandingkan keluaran dengan yang tertulis.
4. Buka uji mutasi pada PG-07 butir 4, dan pastikan pemeriksa memang bisa gagal.
5. Buka daftar dokumen belum dibuka pada PG-07 butir 7, dan catat angka yang belum boleh dikutip.
6. Buka PG-05 butir 8 untuk register status dokumen, lalu pastikan angka diambil dari dokumen yang
   masih berlaku.

### 5.4 Alur dosen penguji

1. Buka PG-09, mulai kuis sepuluh pertanyaan, dan catat jawaban yang salah.
2. Buka PG-05 butir 1 untuk tangga empat tingkat, dan periksa bahwa tidak ada tingkat yang otomatis.
3. Buka PG-01 butir 2 untuk papan vonis, dan periksa tier tiap kelas beserta syarat menggantungnya.
4. Buka PG-04 butir 8 untuk matriks kesepakatan, dan periksa bahwa 11 head L1 hanya 7 fungsi berbeda.
5. Buka PG-08 untuk daftar syarat, dan periksa bahwa setiap kekurangan punya pemilik.

### 5.5 Alur koordinator data

1. Buka PG-03 butir 3, baca 3.906 berkas belum diparse dan sebarannya F-1 C 2.156 serta F-11 1.750.
2. Buka PG-03 butir 6, pilih label yang menunggu fold, dan periksa alasannya.
3. Buka PG-06 butir 5, susun kartu permintaan data dengan pemilik dan tanda tangan.
4. Kembali ke PG-03 butir 1, dan pastikan kartu kesiapan kanal berubah setelah data masuk.

---
## 6. Wireframe teks bertingkat

Tiga tingkat: kerangka global, kerangka halaman, dan kerangka komponen. Semua gambar memakai karakter
ASCII, tanpa tanda pisah panjang, dan tanpa warna sebagai satu-satunya pembeda. Lebar acuan 1.280
piksel untuk desktop dan 375 piksel untuk ponsel; uji 375 piksel sudah menjadi syarat di [KAT] baris
285 sampai 286.

### 6.1 Tingkat 1: kerangka global

```
+------------------------------------------------------------------------------------------+
| SITUS KEPUTUSAN PEMELIHARAAN SUMUR        potong data 2026-10-29   [cari klaim]   [bantuan] |
+------------------------------------------------------------------------------------------+
| Beranda | Kepercayaan | Perencanaan | Data | Mesin | Linimasa | Bukti                       |
+------------------------------------------------------------------------------------------+
|                                                                                          |
|  (isi halaman, satu pertanyaan per halaman)                                              |
|                                                                                          |
+------------------------------------------------------------------------------------------+
| nol slot alarm otomatis | keputusan akhir manusia | angka wajib bersumber | kamus | batas  |
+------------------------------------------------------------------------------------------+
```

Aturan kerangka global: banner tingkat dewan hanya muncul di PG-00 dan PG-05, bukan di semua halaman,
supaya halaman rumpun tidak dibaca sebagai halaman status. Kaki halaman memuat dua penanda tetap:
nol slot alarm otomatis ([JSON] baris 1414) dan keputusan akhir manusia ([DSS4] baris 468).

### 6.2 Tingkat 2: kerangka sepuluh halaman

**PG-00 Beranda.**

```
+ banner: TK-2 PANTAU | S 18,23% | kuorum 6/7 | cakupan 1,00 | dihitung 2026-10-29 14:33 +
+ tiga kartu fokus: [hyd K-i 20 | P4 61%] [vib 429 | P3 50%] [shk 20 | P3 52%]            +
+ beban shift: 40,15 baris | p50 39 | p95 61 | anggaran 30 menit | terlayani 9 | tunda 0 +
+ antrean ringkas: lima baris, kolom umur dan menit, tautan "buka antrean"                 +
+ keadaan data: abstain hari ini 1 baris, kode AB-2, kanal absen 96,6 persen                +
```

**PG-01 Kepercayaan.**

```
+ baris ringkas: 27 kepala | 5 L0 | 11 L1 | 9 L2 | 2 L3 | 0 slot alarm otomatis             +
+ [papan vonis 11 kartu, 3 + 3 + 3 + 2]                                                    +
+ [kartu keyakinan]  [panel ketidaksepakatan]  [badge beban alarm]                          +
+ [kurva kalibrasi: rancangan]  [papan dua pembacaan]  [gerbang provenance]                 +
+ [banner bit_wear]  [slot nilai lapisan B: lima slot kosong berlabel pemilik]              +
```

**PG-02 Perencanaan.**

```
+ banner: anggaran 30 menit | terlayani 9 | ditunda 0 | total tunda 0 menit                  +
+ [tiga kartu fokus]                                                                        +
+ tabel antrean: klaim | jendela | kepala | keyakinan | pita | FAR | lead | umur | menit | aksi+
+ [neraca penundaan]  [beban per shift: lambda, p50, p95]                                    +
+ [Pareto jam henti: 39.397,986 jam tercatat, equipment failure 2.739,667 jam]               +
```

**PG-03 Kualitas data.**

```
+ [kartu kesiapan kanal per sumur]        [matriks ketersediaan berkas]                      +
+ antrean parse: 3.906 berkas | 54,63 persen dari 7.150 | 213 label tanpa fold                +
+ [kartu kelengkapan jendela]  [kanal tidak logging]  [peta label ke fold]                    +
+ [pemilih kanal]  [katalog label instrumen]  [peta drift]  [validitas kedalaman]             +
```

**PG-04 Perbandingan mesin.**

```
+ [balapan model lawan persistence per fold]     [peta kalah menang per kelas]               +
+ [tabel kanal melawan intuisi]  [rekam jejak per sumur]  [bukti sirkularitas]               +
+ [matriks kesepakatan komponen: 11 head L1, 7 fungsi, 4 pasangan kembar]                    +
+ [lencana pola konflik]  [peta ketidaksepakatan tingkat klaim]                              +
```

**PG-05 Linimasa keputusan.**

```
+ tangga: TK-1 TENANG | TK-2 PANTAU | TK-3 TINJAU | TK-4 ESKALASI | pemutus | batas waktu    +
+ [panel suara dewan]  [meter kuorum 4/7]  [meter cakupan 0,50]                              +
+ [buku konflik K-1 sampai K-7]  [pemicu H-1 sampai H-5]                                     +
+ [log keputusan: waktu | aktor | keputusan | akibat]  [garis waktu gerbang]                  +
+ [register status dokumen]  [kalender sumber angka]  [linimasa tier per kelas]               +
```

**PG-06 Alat bantu insinyur.**

```
+ [wizard kalibrasi: langkah 1..n, syarat tiap langkah]                                      +
+ [panduan skrip verifikasi: perintah dan keluaran yang diharapkan]                          +
+ [kartu kelayakan sinyal]  [kartu kanal yang perlu dipasang]  [kartu permintaan data]        +
```

**PG-07 Bukti angka.**

```
+ [lencana provenance tiga warna]                                                            +
+ tabel rujukan: angka | nilai | satuan | berkas | baris | TERUKUR atau TURUNAN | tanggal     +
+ [pengunci rujukan]  [uji mutasi]  [panduan skrip]                                          +
+ [papan satuan]  [daftar dokumen belum dibuka: 119 dokumen, 69 belum dibuka]                +
```

**PG-08 Batas dan syarat data.**

```
+ [peta kode abstain AB-1 sampai AB-5, masing masing dengan contoh nyata]                    +
+ [peta lapis L3: 2 kepala]  [slot nilai lapisan B: 5 slot kosong berlabel pemilik]          +
+ tabel syarat: fitur | status | syarat | pemilik data | uji yang sudah ada                   +
+ [larangan tampilan: 9 baris]                                                               +
```

**PG-09 Kamus dan kuis angka.**

```
+ [kamus 15 istilah, dikelompokkan per sumbu]                                                +
+ [peta tiga sumbu: tier kepala, pita klaim, tingkat dewan]                                  +
+ [kuis 10 pertanyaan]  [contoh baca angka benar dan salah]  [daftar istilah terlarang]      +
```

### 6.3 Tingkat 3: kerangka komponen

**Kartu keyakinan**, dipakai di PG-00, PG-01, dan PG-02. Tata letak mengikuti [DSS1] baris 934 sampai
950, dengan penambahan baris pita umur karena kartu ini juga dipakai di antrean.

```
+-------------------------------------------------------------------+
| hyd K-i  jendela 14:32:00-14:33:00           [ P4 Keyakinan kuat ]|
|                                                                   |
| [=================|----]  61%              batas kelas 0,61       |
| kepala dinilai 3 dari 3           badge FAR 4,10 per 24 jam       |
| S_A 0,75   S_B 0,35   S_C 0,75           lead 8,0 menit           |
| belum terkalibrasi (ECE belum diukur)           rujukan 2026-10   |
+-------------------------------------------------------------------+

+-------------------------------------------------------------------+
| hyd K-ii  jendela 14:32:00     [ menunggu data ]  AB-1            |
| tidak dinilai: belum ada kepala berskor, daftar kepala menunggu   |
+-------------------------------------------------------------------+
```

Angka pada contoh kartu di atas: `K_tampil` 0,6100 tampil sebagai 61 persen, batas kelas 0,61, kepala
dinilai 3 dari 3, S_A 0,75, S_B 0,35, dan S_C 0,75 disalin dari [DSS1] baris 937 sampai 949. Dua angka
terakhir sengaja tidak disalin dari contoh itu. [DSS1] baris 960 menyebut `lead_menit` 42,8 dari [J]
baris 884 dan `badge_far` 12,4 per 24 jam dari [J] baris 88, tetapi pemeriksaan pada JSON menunjukkan
baris 884 berisi `"precision": 0.9927` dan baris 88 berisi `"pos": 1124`, sedangkan pencarian `42.8` dan
`12.4` pada JSON tidak menemukan satu pun (keluaran di bagian 13.10). Angka yang benar untuk klaim
`hyd` K-i ada di [J] baris 804 (`FAR 4,10/24jam, lead 8,0 mnt`) dan baris 809 (`lead_menit: 8.0`),
serta di ledger [LED] baris 3292 (S6-058, 4,0984) dan baris 3432 (E5-007, 8,0 menit). Dokumen ini
memakai 4,10 dan 8,0, dan selisih hulu itu dicatat di bagian 12 butir 12.

**Baris antrean**, dipakai di PG-02. Sembilan kolom tampil, kolom pertama terbaca manusia, umur berpita
([DSS2] baris 610 sampai 626).

```
| No | Klaim         | Jendela | Kepala        | K   | Pita | Umur  | Menit | Aksi  |
|  1 | hyd K-i       |      20 | rule+pers+hib | 61% | P4   | 0 mnt |   6   | cek   |
|  2 | vib           |     429 | rule+pers+hib | 50% | P3   | 0 mnt |   4   | cek   |
|  3 | stuck K-ii    |  30.122 | pers_event    | 33% | P2   | 4 mnt |   2   | lihat |
```

**Panel suara dewan**, dipakai di PG-05. Setiap kepala bersuara satu kali, dengan kode abstain bila
tidak menyala ([DSS4] bagian 4.1 sampai 4.4).

```
+ klaim hyd K-i  siklus 2026-10-29 14:33 -------------------------------------------+
| rule_display                  dukung     bobot 1,50                                |
| hybrid_rule_and_persistence   dukung     bobot 1,50 (satu fungsi, dihitung sekali)  |
| persistence                   abstain    AB-5 kepala bisu pada jendela ini          |
| dewan rig: bobot 9,15 | kuorum 6 dari 7 | cakupan 1,00 | S 18,03 menjadi 18,23 persen|
+------------------------------------------------------------------------------------+
```

---

## 7. Aturan navigasi, penamaan, dan tautan

1. Tujuh butir menu utama, tidak lebih. Urutannya: Beranda, Kepercayaan, Perencanaan, Data, Mesin,
   Linimasa, Bukti. Alasan: enam rumpun ditambah beranda, dan halaman lintas rumpun dicapai lewat
   tautan di dalam blok serta kaki halaman.
2. Satu alamat satu keadaan. Setiap baris yang bisa dipilih punya alamat sendiri, misalnya
   `/kepercayaan?klaim=hyd-Ki&jendela=20`, supaya temuan bisa dikirim ulang ke orang lain dan dibuka
   pada keadaan yang sama. Ini syarat agar uji pada [KAT] baris 283 sampai 286 bisa diulang.
3. Pencarian memakai kode fitur dan kode klaim, bukan hanya teks bebas. Kode fitur 48 buah sudah
   stabil, dan kode klaim 11 buah sudah dipakai lintas dokumen ([DSS4] baris 8).
4. Remah roti tiga tingkat paling banyak: rumpun, halaman, komponen. Contoh: Kepercayaan, Kartu
   keyakinan, hyd K-i jendela 20.
5. Setiap istilah bertanda membuka PG-09 pada istilah itu, dan setiap badge abstain membuka PG-08
   pada kode itu. Dua tautan ini wajib ada di semua halaman, karena keduanya yang mencegah salah
   baca yang paling sering.
6. Tidak ada tautan yang membuka unduhan berkas mentah secara langsung. Berkas mentah dibuka lewat
   PG-07, supaya pembaca melihat satuan dan statusnya lebih dulu.

---

## 8. Keadaan tampilan lintas halaman

Kekurangan data dan konflik tidak punya halaman galat sendiri; keduanya menjadi keadaan yang punya
penampilan baku. Tabel ini yang dipakai semua halaman.

| Keadaan | Pemicu | Yang tampil | Sumber |
|---|---|---|---|
| Tenang | Tidak ada klaim pada pita P2 ke atas | Banner TK-1, tabel diganti kalimat jumlah jendela tenang, tanpa tombol tindakan | [DSS4] baris 395, [DSS2] baris 514 sampai 532 |
| Tanpa kepala berskor | Bobot klaim 0 | Kartu "tidak dinilai", kode AB-1, daftar kepala menunggu | [DSS1] baris 243 |
| Data sensor kurang | `n_nodata / n_windows` lebih dari 0,50 | Kode AB-2, persen kanal absen, tautan ke kartu kesiapan kanal | [DSS1] baris 244 |
| Skor jendela belum diekspor | Hanya ringkasan min, median, maks | Kode AB-3, pita ringkasan yang ada | [DSS1] baris 245 |
| Klaim lapis L3 | Tier BELUM LAYAK PAKAI | Kode AB-4, alasan dari lapisan, tanpa pita | [DSS1] baris 246 dan 260 |
| Kepala bisu | `n_aktif` 0 pada segmen | Kode AB-5, lencana bisu, bukan penolakan | [DSS4] baris 9 dan 356 sampai 366 |
| Keyakinan rendah | Pita P1 atau P2 | Kartu diredupkan, tanpa tombol tindakan, alasan batas atas dibuka | [DSS1] baris 907 sampai 909 |
| Beban melebihi anggaran | Baris terlayani kurang dari baris masuk | Angka tunda dan menit kekurangan pada banner, bukan catatan kaki | [DSS2] baris 502 sampai 505 |
| Konflik saling meniadakan | Dua kepala setara berbeda putusan | Dua pembacaan berdampingan, tingkat dibatasi TK-2 | [DSS4] baris 486 dan 499 |
| Dua angka FAR | Satu kepala membawa dua populasi angka | Dua angka berdampingan dengan label populasi, TK-4 tertahan | [DSS4] baris 490 sampai 492 |
| Log kosong | Belum ada keputusan tercatat | Kalimat pembeda "belum ada keputusan" dari "tidak ada peringatan" | [KAT] baris 2076 sampai 2079 |
| Angka belum boleh dikutip | Status provenance kuning atau merah | Angka tampil dengan lencana, tanpa tombol salin rujukan | [KAT] baris 501 sampai 570 |

Jumlah baris data tabel di atas: 12.

---

## 9. Yang sengaja tidak dibuat

Daftar ini sama pentingnya dengan daftar halaman, karena tiap butir menghapus satu cara salah baca
yang sudah teridentifikasi di dokumen hulu.

| Tidak dibuat | Alasan | Sumber |
|---|---|---|
| Halaman alarm otomatis atau pusat notifikasi | Slot alarm otomatis bernilai 0, dan tidak ada tingkat yang mengirim pesan sendiri | [JSON] baris 1414, [DSS4] baris 474 sampai 476 |
| Gauge, dial, atau donat untuk peluang | Sudut dan luas bukan kanal cepat untuk besaran, dan gauge termasuk visual yang harus dihindari | [VR] baris 248 |
| Satu angka besar sebagai pahlawan halaman | Angka tunggal tanpa sebaran dibaca sebagai kepastian | [VR] baris 246 |
| Dua sumbu Y pada satu grafik | Membuat pembaca sulit menyimpulkan dua deret sekaligus | [VR] baris 244 |
| Grafik radar untuk perbandingan kategori | Sudut tidak sebanding antar sumbu, dan bentuk ini sudah ditolak katalog | [KAT] baris 1825 dan 2335, [VR] baris 256 |
| Diagram alir untuk riwayat keputusan | Riwayat keputusan dibaca sebagai urutan waktu, bukan sebagai alur proses | [KAT] baris 2097, [VR] baris 256 |
| Halaman deret per menit | Deret sinyal per menit belum tersimpan, sehingga halaman akan menampilkan kekosongan tanpa alasan | [KAT] baris 2638 sampai 2639 |
| Papan kanban sebagai tampilan utama antrean | Papan kehilangan angka dan kehilangan urutan; papan hanya dipakai saat serah terima | [DSS2] baris 653 sampai 663 |
| Skor tunggal sebagai bukti kalibrasi | Skor seperti Brier mencampur kalibrasi, daya pisah, dan keacakan data | [VR] baris 247 |

Jumlah baris data tabel di atas: 9.

---

## 10. Keterbacaan dan pengujian tampilan

1. Setiap status wajib punya teks, bukan hanya warna. Syarat ini berasal dari larangan warna merah tanpa
   label manusia-peninjau ([KAT] baris 203 sampai 207), dan berlaku untuk pita, umur, serta lencana
   konflik.
2. Setiap halaman diuji pada skala abu. Bila pita P3 dan P4 sulit dibedakan tanpa warna, lencana
   diberi pola tekstur, seperti pola garis miring untuk abstain ([DSS1] baris 250 sampai 251).
3. Setiap halaman diuji pada lebar 375 piksel, dan daftar syarat menggantung pada kartu vonis wajib
   terbaca tanpa menggulir horizontal ([KAT] baris 285 sampai 286).
4. Angka pada kartu dan tabel wajib sama dengan pembulatan sumbernya. Contoh aturan: persen pada kartu
   sama dengan `round(100 x K_tampil)` ([DSS1] baris 975).
5. Uji klik: pada pita P1 dan P2 tidak ada elemen yang bisa memicu tindakan ([DSS1] baris 976).
6. Uji urutan: kartu P4 di atas P2, dan semua kartu abstain di bawah kartu berpita ([DSS1] baris 974).

---

## 11. Syarat agar tiap halaman naik status

Tidak ada halaman yang ditutup. Setiap baris menyebut apa yang dibutuhkan, siapa pemiliknya, dan uji
yang menandai kenaikan status.

| Halaman | Status hari ini | Yang dibutuhkan | Pemilik | Uji naik status |
|---|---|---|---|---|
| PG-00 | siap, dengan satu blok siap sebagian | skema pencatatan umur item, supaya angka tunda harian nyata bukan simulasi | pemilik produk | bandingkan angka tunda layar dengan hitungan manual satu shift |
| PG-01 | siap, dua fitur siap sebagian dan satu rancangan | ECE terukur per engine, supaya kurva kalibrasi berhenti berlabel rancangan | penilai model | satu diagram per engine dengan jumlah bin dan garis diagonal |
| PG-02 | siap | peta sumur per jendela, karena seluruh baris hari ini dari segmen F-14 | pemilik data | dua sumur tampil dengan baris berbeda |
| PG-03 | siap | daftar kanal masukan per engine yang lengkap | engineer instrumentasi | kartu kesiapan kanal penuh untuk seluruh klaim |
| PG-04 | siap | deret per menit, supaya matriks kesepakatan tingkat jendela bisa dihitung | ML engineer | matriks dihitung dari deret tersimpan, bukan dari ringkasan |
| PG-05 | siap sebagian | skema log keputusan dan pengisian awalnya | supervisor | satu shift penuh dengan setiap peringatan berlabel |
| PG-06 | siap sebagian | peta sumur dan prosedur uji jalan yang disepakati | engineer pemasangan | wizard dijalankan pada satu sumur baru |
| PG-07 | siap | penutupan lima cacat pemblokir C-01 sampai C-05 | auditor internal | 119 dokumen terbuka, atau daftar angka yang tidak boleh dikutip |
| PG-08 | siap sebagian | tarif biaya henti, identitas alat, dan kanal baru | manajer pemeliharaan | lima slot nilai terisi dengan sumber |
| PG-09 | siap | tidak ada, kamus tidak bergantung data baru | pemilik produk | kuis dijalankan dua orang, selisih jawaban nol |

Jumlah baris data tabel di atas: 10.

---

## 12. Yang belum diverifikasi di dokumen ini

Bagian ini bukan penutup yang merendah. Isinya daftar periksa untuk pekerjaan berikutnya, dan setiap
butir menyebut apa yang sudah diperiksa serta apa yang belum.

1. Ledger [LED] tidak dibaca penuh. Yang dibaca hanya baris yang dikutip: 3292, 3432, 3433, dan
   3428 sampai 3434 untuk memeriksa tetangga entri. Sisanya, lebih dari 3.400 baris, belum diperiksa.
2. Satu rujukan baris di [DSS2] tidak cocok. [DSS2] baris 79 sampai 80 menulis lead 8,0 menit di
   [LED] baris 3436, padahal berkas ledger berakhir di baris 3.434 sehingga baris 3436 tidak ada, dan
   entri E5-007 berada di baris 3432 (keluaran di
   bagian 13.7). Dokumen ini memakai baris 3432.
3. Satu selisih hitungan di [DSS4]: ringkasan butir 8 menyebut "sembilan aturan konflik", sedangkan
   tabel bagian 6.1 berisi tujuh baris K-1 sampai K-7 (dihitung dengan `grep -c '^| K-'` pada bagian
   13.5) dan metadata kartu induk menyebut tujuh. Dokumen ini memakai angka tujuh.
4. Angka status fitur 32, 15, dan 1 dikutip dari [KAT] bagian 11, bukan dihitung ulang dari setiap
   butir fitur. Yang dihitung ulang hanya jumlah fitur, yaitu 48, dan jumlah tabel katalog.
5. Angka beban 40,15 baris per shift berasal dari simulasi Poisson, bukan dari hitungan kejadian nyata
   ([DSS2] bagian 2.4). Dokumen ini menuliskannya sebagai perkiraan, bukan sebagai hasil ukur lapangan.
6. Angka kejadian tiap klaim, misalnya 975, 876, dan 626, dikutip dari [DSS3] baris 27 sampai 29 dan
   dicocokkan dengan [JSON] lewat `jq` pada bagian 13.4 untuk jumlah kepala dan lapisan, tetapi nilai
   per kepala tidak dihitung ulang satu per satu.
7. Tidak ada halaman yang dirender. Seluruh wireframe di bagian 6 adalah teks, dan uji 375 piksel serta
   uji skala abu belum dijalankan pada peramban.
8. Alur 30 detik dan estimasi waktu pada bagian 5 adalah target desain, bukan hasil pengukuran pada
   operator. Angka 30 detik, 20 menit, dan 2 menit belum diuji dengan pengguna nyata.
9. Status tiap halaman pada bagian 3 dan 11 adalah turunan dari status fitur di [KAT], bukan dari
   kesiapan bangun. Halaman bisa berstatus siap sekarang untuk datanya, tetapi belum dibangun.
10. Jumlah klaim 11 dan jumlah kepala 27 dikutip dari [DSS4] baris 8 dan diverifikasi sebagian dengan
    `jq` (27 kepala, lapisan 5, 11, 9, 2). Daftar sebelas klaim belum dihitung ulang satu per satu.
11. Rujukan literatur LV1 sampai LV19 tidak dibuka ulang di sesi ini. Yang dipakai adalah kalimat inti
    dan kode yang sudah tercatat di [VR] bagian 5 dan [DSS2] bagian 8.4.
12. Satu rujukan angka di [DSS1] tidak cocok. [DSS1] baris 960 menyebut `lead_menit` 42,8 dari [J]
    baris 884 dan `badge_far` 12,4 per 24 jam dari [J] baris 88. Pada JSON sekarang, baris 884 berisi
    `"precision": 0.9927` dan baris 88 berisi `"pos": 1124`, dan pencarian `42.8` serta `12.4` pada
    seluruh JSON menghasilkan 0 baris (keluaran di bagian 13.10). Angka yang terukur untuk `hyd` K-i
    ada di [J] baris 804 dan 809, yaitu FAR 4,10 per 24 jam dan `lead_menit` 8,0, dan itu yang dipakai
    dokumen ini. Angka 42,8 pada [DSS1] belum tertelusuri ke berkas mana pun.

---
## 13. Keluaran perintah yang dijalankan

Bagian ini menempelkan keluaran apa adanya pada 2026-10-31, sesuai kerangka butir 3. Tidak ada angka
di bagian ini yang berasal dari ingatan. Perintah dijalankan dari `/mnt/d/Capstone 1(v2)` kecuali
disebut lain.

### 13.1 Ukuran tujuh berkas masukan utama

```
$ stat -c '%s %n' planning/01_KATALOG_FITUR.md planning/02_RISET_VISUALISASI.md \
      planning/03_SKOR_KEYAKINAN.md planning/04_ANTREAN_TINJAUAN.md \
      planning/05_KETIDAKSEPAKATAN.md planning/06_SWARM_KONSENSUS.md \
      docs/RND_PROVENANCE_LEDGER.md
166662 planning/01_KATALOG_FITUR.md
32141 planning/02_RISET_VISUALISASI.md
66698 planning/03_SKOR_KEYAKINAN.md
95168 planning/04_ANTREAN_TINJAUAN.md
87228 planning/05_KETIDAKSEPAKATAN.md
92688 planning/06_SWARM_KONSENSUS.md
471945 docs/RND_PROVENANCE_LEDGER.md
```

Dua berkas tambahan yang dibuka untuk verifikasi angka:

```
$ stat -c '%s %n' scratch/v9_i1/v9_i1_RESULTS.json docs/RND_ENGINE_S6_INTEGRATION.md
57555 scratch/v9_i1/v9_i1_RESULTS.json
3915 docs/RND_ENGINE_S6_INTEGRATION.md
```

### 13.2 Jumlah baris

```
$ wc -l planning/01_KATALOG_FITUR.md planning/02_RISET_VISUALISASI.md \
      planning/03_SKOR_KEYAKINAN.md planning/04_ANTREAN_TINJAUAN.md \
      planning/05_KETIDAKSEPAKATAN.md planning/06_SWARM_KONSENSUS.md \
      docs/RND_PROVENANCE_LEDGER.md
   2780 planning/01_KATALOG_FITUR.md
    335 planning/02_RISET_VISUALISASI.md
   1060 planning/03_SKOR_KEYAKINAN.md
   1428 planning/04_ANTREAN_TINJAUAN.md
   1247 planning/05_KETIDAKSEPAKATAN.md
   1053 planning/06_SWARM_KONSENSUS.md
   3434 docs/RND_PROVENANCE_LEDGER.md
  11337 total
$ wc -l scratch/v9_i1/v9_i1_RESULTS.json docs/RND_ENGINE_S6_INTEGRATION.md
 1758 scratch/v9_i1/v9_i1_RESULTS.json
   76 docs/RND_ENGINE_S6_INTEGRATION.md
 1834 total
```

### 13.3 Total byte sembilan berkas

```
$ wc -c planning/01_KATALOG_FITUR.md planning/02_RISET_VISUALISASI.md \
      planning/03_SKOR_KEYAKINAN.md planning/04_ANTREAN_TINJAUAN.md \
      planning/05_KETIDAKSEPAKATAN.md planning/06_SWARM_KONSENSUS.md \
      docs/RND_PROVENANCE_LEDGER.md scratch/v9_i1/v9_i1_RESULTS.json \
      docs/RND_ENGINE_S6_INTEGRATION.md
 166662 planning/01_KATALOG_FITUR.md
  32141 planning/02_RISET_VISUALISASI.md
  66698 planning/03_SKOR_KEYAKINAN.md
  95168 planning/04_ANTREAN_TINJAUAN.md
  87228 planning/05_KETIDAKSEPAKATAN.md
  92688 planning/06_SWARM_KONSENSUS.md
 471945 docs/RND_PROVENANCE_LEDGER.md
  57555 scratch/v9_i1/v9_i1_RESULTS.json
   3915 docs/RND_ENGINE_S6_INTEGRATION.md
1074000 total
```

Total 1.074.000 byte dan 11.337 ditambah 1.834 sama dengan 13.171 baris, cocok dengan tabel bagian 1.

### 13.4 Struktur JSON: kepala, lapisan, dan slot alarm

```
$ jq -r '.decision_layer.ringkasan' scratch/v9_i1/v9_i1_RESULTS.json
{
  "L0": 5,
  "L1": 11,
  "L2": 9,
  "L3": 2
}
$ jq -r '"nperingatan_l1=\(.decision_layer.nperingatan_l1) auto_slots=\(.decision_layer.auto_critical_alarm_slots)"' \
     scratch/v9_i1/v9_i1_RESULTS.json
nperingatan_l1=11 auto_slots=0
$ jq -r '[.engines[].heads[]] | "heads=\(length)"' scratch/v9_i1/v9_i1_RESULTS.json
heads=27
$ jq -r '[.engines[].heads[].tier] | group_by(.) | map("\(.[0]) \(length)") | .[]' \
     scratch/v9_i1/v9_i1_RESULTS.json
BELUM LAYAK PAKAI 2
PERINGATAN-BERPENGAWAS 12
TREN 13
$ jq -r '.decision_layer.layers.L3[] | "\(.engine) \(.head) \(.klaim) \(.tier) \(.status)"' \
     scratch/v9_i1/v9_i1_RESULTS.json
hyd k2_tidak_tersedia K-ii BELUM LAYAK PAKAI BELUM TERSEDIA DI PROTOTIPE
bit_wear k2_onset_belum K-2 BELUM LAYAK PAKAI BELUM DIJALANKAN
```

Keluaran ini yang menopang lima angka pada bagian 4: 27 kepala, 5 L0, 11 L1, 9 L2, 2 L3, dan
`auto_critical_alarm_slots` 0. Sebaran tier 2, 12, 13 juga dari keluaran ini, dan jumlahnya konsisten
dengan lapisan: 11 kepala L1 ditambah satu kepala L0 bertier peringatan menghasilkan 12.

### 13.5 Hitungan tabel katalog dan tabel aturan konflik

```
$ grep -c '^### ' planning/01_KATALOG_FITUR.md
48
$ grep -c '^|' planning/01_KATALOG_FITUR.md
118
$ sed -n '482,492p' planning/06_SWARM_KONSENSUS.md | grep -c '^| K-'
7
```

Baris pertama menopang klaim 48 fitur. Baris ketiga menopang klaim tujuh aturan konflik dan sekaligus
menunjukkan selisih dengan ringkasan [DSS4] butir 8 yang menyebut sembilan, seperti dicatat di
bagian 12 butir 3.

### 13.6 Baris ledger yang dikutip

```
$ sed -n '3292p' docs/RND_PROVENANCE_LEDGER.md
| S6-058 | 4.0984 | alarm per 24 jam kalender | RUN-KITA | s6_verifikasi.json ringkas.hyd.H1p_rule_dan_persist.far24_kalender_median | bagian 3 | TERUKUR |
$ sed -n '3432p;3433p' docs/RND_PROVENANCE_LEDGER.md
| E5-007 | 8.0 | menit | RUN-KITA | scratch/v9_i1/v9_i1_RESULTS.json:engines[hyd].heads[hybrid].lead_menit | 2026-10-29 | RND_ENGINE_S6_INTEGRATION.md bagian 1 | TERUKUR |
| E5-008 | 6 | tinjauan/shift | TURUNAN | ceil(16,611 / 3) dari nilai_maintenance.beban_tinjauan_L1 | 2026-10-29 | RND_ENGINE_S6_INTEGRATION.md bagian 2 | TERUKUR |
```

### 13.7 Pemeriksaan rujukan baris 3436

Ini pemeriksaan yang menemukan selisih pada [DSS2] baris 79 sampai 80.

```
$ wc -l < docs/RND_PROVENANCE_LEDGER.md
3434
$ awk 'END{print NR": "substr($0,1,60)}' docs/RND_PROVENANCE_LEDGER.md
3434: | E5-009 | 11 | head | RUN-KITA | scratch/v9_i1/v9_i1_RESULT
$ awk 'NR>=3430 && NR<=3436 {printf "%d|%s\n", NR, substr($0,1,110)}' docs/RND_PROVENANCE_LEDGER.md
3430| | E5-005 | 2739.667 | jam | RUN-KITA | scratch/v9_i1/v9_i1_RESULTS.json:nilai_maintenance.jam_henti_per_sebab.
3431| | E5-006 | 212.0 | jam | RUN-KITA | scratch/v9_i1/v9_i1_RESULTS.json:nilai_maintenance.jam_henti_per_sebab.stu
3432| | E5-007 | 8.0 | menit | RUN-KITA | scratch/v9_i1/v9_i1_RESULTS.json:engines[hyd].heads[hybrid].lead_menit | 2
3433| | E5-008 | 6 | tinjauan/shift | TURUNAN | ceil(16,611 / 3) dari nilai_maintenance.beban_tinjauan_L1 | 2026-10-
3434| | E5-009 | 11 | head | RUN-KITA | scratch/v9_i1/v9_i1_RESULTS.json:decision_layer.nperingatan_l1 | 2026-10-29
```

Keluaran menunjukkan berkas ledger berakhir pada baris 3434, sehingga baris 3436 yang disebut [DSS2]
tidak ada. Entri E5-007 berada di baris 3432, dan dokumen ini memakai baris itu.

### 13.8 Pemeriksaan berkas ini sendiri

Diukur sebelum bagian 13 ditambahkan, karena menempelkan keluaran mengubah ukuran berkas.

```
$ stat -c '%s byte' planning/07_ARSITEKTUR_INFORMASI.md
75363 byte
$ wc -l < planning/07_ARSITEKTUR_INFORMASI.md
1060
$ grep -cP '\x{2014}' planning/07_ARSITEKTUR_INFORMASI.md
0
$ grep -cP '\x{2013}' planning/07_ARSITEKTUR_INFORMASI.md
0
$ grep -c -i 'tidak[ ]bisa' planning/07_ARSITEKTUR_INFORMASI.md
0
$ grep -c -i 'tidak[ ]mungkin' planning/07_ARSITEKTUR_INFORMASI.md
0
$ grep -c -i 'terbat[a]s' planning/07_ARSITEKTUR_INFORMASI.md
0
$ grep -c '^|' planning/07_ARSITEKTUR_INFORMASI.md
326
$ grep -c '^## ' planning/07_ARSITEKTUR_INFORMASI.md
13
$ ls *.py *.html *.json *.csv 2>/dev/null | wc -l
0
```

Angka 13 bagian utama sesuai dengan daftar berikut: 0 kerangka wajib, 1 berkas masukan, 2 prinsip,
3 peta halaman, 4 sepuluh halaman, 5 alur, 6 wireframe, 7 navigasi, 8 keadaan tampilan, 9 yang tidak
dibuat, 10 keterbacaan, 11 syarat, 12 yang belum diverifikasi, dan 13 keluaran perintah.

Sesudah bagian 13 ditambahkan, hitungan `grep` pada berkas ini berubah karena keluaran perintah yang
ditempel ikut terhitung. Ukuran akhir berkas, jumlah tabel, dan jumlah baris data tabel dicatat pada
komentar kartu saat penyerahan, bukan di sini, supaya tidak ada angka yang diklaim tanpa pengukuran.

### 13.9 Yang tidak dijalankan

Tidak ada model, engine, pipeline, atau peramban yang dijalankan saat menyusun dokumen ini. Tidak ada
halaman yang dirender. Seluruh angka adalah angka yang sudah terhitung di dokumen hulu, dan setiap
angka membawa rujukan barisnya. Wireframe pada bagian 6 adalah teks, bukan tangkapan layar.

### 13.10 Pemeriksaan angka kartu keyakinan pada JSON

Pemeriksaan ini yang menemukan selisih rujukan pada [DSS1] baris 960.

```
$ grep -c '42\.8\|12\.4' scratch/v9_i1/v9_i1_RESULTS.json
0
$ sed -n '88p;884p' scratch/v9_i1/v9_i1_RESULTS.json
            "pos": 1124,
            "precision": 0.9927,
$ sed -n '804p' scratch/v9_i1/v9_i1_RESULTS.json | cut -c1-118
          "badge_far": "S6 lintas fold+seed (docs/RND_S6_PM_WAVE2.md §4.1): FP 927, presisi 0,8243, recall 0,6519, FA
$ sed -n '809p' scratch/v9_i1/v9_i1_RESULTS.json
          "lead_menit": 8.0,
```

Baris 804 dipotong pada 118 karakter supaya muat di layar. Bagian yang terpotong memuat `FAR
4,10/24jam` dan `lead 8,0 mnt`, dan bunyi penuhnya terbaca dengan `sed -n '804p'` tanpa `cut`. Hasil
pencarian 0 menunjukkan angka 42,8 dan 12,4 tidak ada di JSON, sehingga rujukan [DSS1] baris 960 tidak
menunjuk angka itu. Dokumen ini memakai 4,10 dan 8,0 dari baris 804 dan 809.

### 13.11 Pemeriksaan berkas ini sesudah perbaikan

```
$ stat -c '%s byte' planning/07_ARSITEKTUR_INFORMASI.md
87727 byte
$ wc -l < planning/07_ARSITEKTUR_INFORMASI.md
1328
$ grep -c '^|' planning/07_ARSITEKTUR_INFORMASI.md
329
$ grep -cP '\x{2014}' planning/07_ARSITEKTUR_INFORMASI.md
0
$ grep -cP '\x{2013}' planning/07_ARSITEKTUR_INFORMASI.md
0
$ grep -c -i 'tidak[ ]bisa\|tidak[ ]mungkin\|terbat[a]s' planning/07_ARSITEKTUR_INFORMASI.md
0
$ ls planning/*.py planning/*.html planning/*.json planning/*.csv 2>/dev/null | wc -l
0
```

Angka pada blok ini diukur tepat sebelum blok ini ditulis, dan tiga angka pertama adalah satu satunya
angka di dokumen ini yang berubah bila berkas ini disunting lagi. Bila pembaca menemukan selisih,
yang berlaku adalah keluaran `stat` dan `wc` pada pembacaan pembaca itu.

---

## 14. Penutup yang bisa diperiksa

Dokumen ini menyerahkan sepuluh halaman, tujuh butir menu utama, lima prinsip arsitektur, dua belas
keadaan tampilan, sembilan bentuk yang sengaja tidak dibuat, dua belas butir yang belum diverifikasi,
dan keluaran perintah apa adanya. Tiga hal bisa diperiksa orang lain tanpa membuka sesi ini:

1. Setiap angka pada bagian 4 dan 5 punya pasangan berkas dan baris, atau kode entri ledger, yang
   bisa dibuka dengan `sed -n '<baris>p' <berkas>`.
2. Setiap klaim status fitur bisa dicocokkan dengan [KAT] bagian 11, dan setiap klaim tingkat dewan
   bisa dicocokkan dengan [DSS4] bagian 5.
3. Berkas ini lolos pemeriksaan format pada bagian 13.8: nol tanda pisah panjang, nol tanda pisah
   sedang, nol frasa terlarang, dan nol berkas non-markdown di `planning/`.

Bila satu angka hulu berubah, halaman yang mengutipnya wajib diperbarui lewat pengunci rujukan
(KEP-07), dan perubahan itu tercatat di PG-05 sebagai satu baris log keputusan.
