# MUTU: audit konsistensi dokumen planning

Dokumen ini adalah hasil audit atas seluruh berkas di `planning/` sebelum paket diserahkan.
Isinya: ukuran berkas yang dibuka, pemeriksaan setiap jalur yang dirujuk, uji angka ke sumbernya,
pencarian frasa alarm otomatis, pencarian kalimat penyerahan dan tanda pisah panjang, tabel temuan,
cacat bernomor, dan satu keputusan di bagian 9.

Kerangka wajib dari kartu dipakai apa adanya, tanpa perubahan satu butir pun.

## 1. Berkas yang dibuka

Seluruh angka pada tabel ini keluar dari `stat` dan `wc`, bukan dari ingatan. Empat belas berkas
markdown, tanpa satu pun berkas lain, total 978.457 byte.

| Byte | Baris | Berkas |
|---:|---:|---|
| 35.536 | 412 | `planning/00_INVENTARIS_RND2_V11.md` |
| 44.125 | 626 | `planning/00_INVENTARIS_V3_V6.md` |
| 39.059 | 589 | `planning/00_INVENTARIS_V7_V8.md` |
| 33.601 | 472 | `planning/00_INVENTARIS_V9_RND1.md` |
| 43.536 | 700 | `planning/00_VERIFIKASI_INVENTARIS.md` |
| 166.662 | 2.780 | `planning/01_KATALOG_FITUR.md` |
| 32.141 | 335 | `planning/02_RISET_VISUALISASI.md` |
| 66.698 | 1.060 | `planning/03_SKOR_KEYAKINAN.md` |
| 95.168 | 1.428 | `planning/04_ANTREAN_TINJAUAN.md` |
| 87.228 | 1.247 | `planning/05_KETIDAKSEPAKATAN.md` |
| 92.688 | 1.053 | `planning/06_SWARM_KONSENSUS.md` |
| 87.727 | 1.328 | `planning/07_ARSITEKTUR_INFORMASI.md` |
| 85.929 | 1.365 | `planning/08_KONTRAK_DATA.md` |
| 68.359 | 1.183 | `planning/09_NASKAH_AKSESIBILITAS.md` |
| **978.457** | **14.578** | **empat belas berkas** |

Berkas sumber yang dibuka untuk menguji angka, di luar folder `planning/`:

| Byte | Baris | Berkas | Dipakai untuk |
|---:|---:|---|---|
| 471.945 | 3.434 | `docs/RND_PROVENANCE_LEDGER.md` | baris ledger S6-058, E5-007, E5-008 |
| 456.685 | 31.946 | `dashboard/data/head_pages.json` | lambda beban per shift |
| 57.555 | 1.759 | `scratch/v9_i1/v9_i1_RESULTS.json` | lapisan keputusan, FAR, lead, profil kapabilitas |
| 44.359 | 861 | `code/v9_i1_pipeline.py` | REGISTRY tier dan asersi lapisan |
| 7.531 | 177 | `~/.hermes/cache/scratch/dss3_calc.py` | hitung ulang matriks ketidaksepakatan |
| 458.129 | biner | `data/predictive/features_timeseries.npz` | ukuran arsip fitur |

Catatan hitung baris: `head_pages.json` dan `v9_i1_RESULTS.json` tidak diakhiri baris baru, sehingga
`wc -l` memberi 31.945 dan 1.758, sedangkan jumlah baris logis 31.946 dan 1.759. Selisih satu ini
menjadi cacat nomor 4.

## 2. Jalur berkas yang dirujuk

Sembilan puluh jalur unik muncul di empat belas berkas, dalam bentuk `docs/`, `scratch/`, `code/`,
`planning/`, `data/`, `dashboard/`, dan `config/`. Delapan puluh sembilan ada di disk. Satu yang
tampak hilang ternyata potongan jalur absolut `/home/neonti/.hermes/cache/scratch/dss3_calc.py`
pada `05_KETIDAKSEPAKATAN.md` baris 122, dan berkasnya ada pada 7.531 byte. Jadi jalur yang benar
benar menggantung: nol.

Jalur yang paling sering dirujuk, sebagai gambaran ketergantungan:

| Jumlah berkas yang merujuk | Jalur |
|---:|---|
| 10 | `docs/RND_PROVENANCE_LEDGER.md` |
| 9 | `planning/02_RISET_VISUALISASI.md` |
| 8 | `planning/01_KATALOG_FITUR.md` |
| 8 | `scratch/v9_i1/v9_i1_RESULTS.json` |
| 7 | `docs/RND_ENGINE_S6_INTEGRATION.md` |
| 6 | `docs/RND_S6_PM_WAVE2.md` |
| 6 | `docs/V9_EVAL_C_LAYERC.md` |

## 3. Uji angka ke sumbernya

Tiga puluh angka diuji, bukan lima belas. Tiap baris menyebut berkas yang menulis angka, sumber yang
dirujuk, dan hasil uji. Sebagian diuji dengan membaca baris sumber langsung, sebagian dengan
menghitung ulang aritmetika, dan empat diuji dengan menjalankan ulang skrip yang dikutip dokumen.

| No | Angka yang diuji | Ditulis di | Sumber yang dirujuk | Hasil |
|---:|---|---|---|---|
| 1 | 27 kepala, L0 5, L1 11, L2 9, L3 2 | 03, 06, 07, 08 | `[JSON]` `.decision_layer.ringkasan` | COCOK |
| 2 | 0 slot alarm otomatis | 05, 06, 07, 08 | `[JSON]` baris 1414 | COCOK |
| 3 | FAR 4,10 per 24 jam | 06, 07, 09 | `[JSON]` baris 804; `[LED]` baris 3292 (4.0984) | COCOK |
| 4 | lead 8,0 menit | 04, 06, 07, 08 | `[JSON]` baris 809; `[LED]` baris 3432 (8.0) | COCOK |
| 5 | beban 40,15 baris per shift | 04 bagian 2.4 | jumlah 16,647 + 2,206 + 2,774 + 18,523 | COCOK, tepat 40,150 |
| 6 | p50 39 baris | 04 bagian 2.4 | jumlah 16 + 2 + 3 + 18 | COCOK |
| 7 | p95 61 baris | 04 bagian 2.4 | jumlah 24 + 5 + 6 + 26 | COCOK |
| 8 | lambda 16,647 | 04 tabel 2.4 | `[H]` baris 271 | COCOK |
| 9 | lambda 2,206 | 04 tabel 2.4 | `[H]` baris 10399 | COCOK |
| 10 | lambda 2,774 | 04 tabel 2.4 | `[H]` baris 15457 | COCOK |
| 11 | lambda 5,537 | 04 tabel 2.4 | `[H]` baris 25883 | COCOK |
| 12 | lambda 18,523 | 04 tabel 2.4 | `[H]` baris 23136 | COCOK |
| 13 | lambda 1.006,08 per menit | 04 tabel 2.4 | `[H]` baris 29846 | COCOK |
| 14 | bobot dewan rig 9,15 | 06 bagian 5 | jumlah 1,65 + 0,40 + 1,40 + 1,40 + 0,75 + 3,30 + 0,25 | COCOK |
| 15 | bobot dewan rig 11,30 | 06 bagian 5 | jumlah 2,05 + 0,80 + 1,80 + 1,80 + 0,75 + 3,30 + 0,80 | COCOK |
| 16 | pangsa hyd 36,07 persen | 06 bagian 7.2 | 3,30 dibagi 9,15 | COCOK |
| 17 | S 18,03 persen sebelum batas | 06 bagian 7.2 | 1,65 dibagi 9,15 | COCOK |
| 18 | S 18,23 persen sesudah batas | 06 bagian 7.2 | 1,65 dibagi 9,0525 | COCOK |
| 19 | vib n01 602, shk 520, stuck 241, tool_wear 284 | 05 bagian 5 | jalan ulang `dss3_calc.py` | COCOK |
| 20 | hyd 626 / 349 / 250 | 05 bagian 5 | jalan ulang `dss3_calc.py` | COCOK |
| 21 | ssi n_aktif 5.455, TP 0 | 05 bagian 5 | jalan ulang `dss3_calc.py` | COCOK |
| 22 | KS 100,00 persen pada 4 pasangan | 05 bagian 5 | jalan ulang `dss3_calc.py` | COCOK |
| 23 | batas atas vib 0,4950 pita P3 | 03, 06, 07 | `03_SKOR_KEYAKINAN.md` baris 439 | COCOK |
| 24 | batas atas bit_wear 0,2525 pita P2 | 03, 04, 06, 09 | `03_SKOR_KEYAKINAN.md` baris 422 | COCOK |
| 25 | `[H]` 456.685 byte | 04, 07 | `stat` pada `head_pages.json` | COCOK |
| 26 | `[J]` 57.555 byte | 04, 05, 07, 08 | `stat` pada `v9_i1_RESULTS.json` | COCOK |
| 27 | `[LED]` 471.945 byte dan 3.434 baris | 07 | `stat` dan `wc` pada ledger | COCOK |
| 28 | arsip fitur 458.129 byte | 08 bagian 10.3 | `stat` pada `features_timeseries.npz` | COCOK |
| 29 | total sembilan berkas 1.074.000 byte dan 13.171 baris | 07 bagian 1 | jumlah sembilan baris tabel | COCOK |
| 30 | berkas 09 sendiri 67.825 byte dan 1.168 baris | 09 bagian 9.7 | `stat` dan `wc` | TIDAK COCOK, kini 68.359 dan 1.183 |

Hasil: 29 cocok, 1 tidak cocok. Angka yang tidak cocok sudah dinyatakan sendiri oleh dokumen sebagai
ukuran sebelum suntingan terakhir, jadi bukan angka karangan, tetapi tetap tidak sama dengan keadaan
berkas saat ini. Itu cacat nomor 6.

## 4. Frasa alarm otomatis

Pencarian tidak peka huruf besar kecil atas tujuh pola. Yang ditemukan hanya pola negasi, dan tidak
ada satu pun kalimat yang menjadikan alarm otomatis sebagai tujuan.

| Pola | Berkas yang memuat | Sifat temuan |
|---|---|---|
| `alarm otomatis` | 14 berkas, 61 kemunculan | seluruhnya negasi, batas, atau angka slot 0 |
| `notifikasi otomatis` | 3 berkas, 3 kemunculan | ketiganya berupa larangan atau penanda tidak adanya jalur notifikasi |
| `pemutus otomatis` | 1 berkas, 1 kemunculan | berbunyi "tidak ada pemutus otomatis" |
| `sistem alarm` | 0 | tidak ada |
| `memicu alarm` | 0 | tidak ada |
| `alarm akan` | 0 | tidak ada |
| `peringatan otomatis` | 0 | tidak ada |

Bukti penguat: `[JSON]` `.decision_layer.auto_critical_alarm_slots` bernilai 0, dan empat tingkat
keputusan `[DSS4]` semuanya berhenti pada manusia. Butir 1 kerangka wajib dipenuhi seluruh berkas.

## 5. Kalimat penyerahan dan tanda pisah panjang

Kata yang dilarang sebagai penutup dicari di empat belas berkas. Yang ditemukan selalu berada di
tengah kalimat teknis, tidak satu pun menjadi kalimat penutup laporan.

| Kata | Berkas | Baris | Sifat |
|---|---|---:|---|
| `tidak bisa` | 03 | 182, 844, 875 | tengah kalimat, menjelaskan batas pita dan keterbacaan |
| `tidak bisa` | 08 | 619, 698 | tengah kalimat, menjelaskan syarat pengisian kolom |
| `tidak mungkin` | 03 | 652 | tengah kalimat, mengutip larangan mengklaim angka tinggi |
| `terbatas` | 05 | 1170 | di dalam blok perintah pemeriksa, bukan prosa |
| `mustahil` | 05 | 1187 | di dalam penjelasan hasil pemeriksa, bukan prosa |

Tanda pisah panjang U+2014 dan tanda pisah pendek U+2013 dihitung per berkas:

| Berkas | U+2014 | U+2013 |
|---|---:|---:|
| tiga belas berkas lain | 0 | 0 |
| `08_KONTRAK_DATA.md` | 2 | 0 |
| **seluruh folder** | **2** | **0** |

Dua tanda pisah itu berada di baris 1219 dan 1238 `08_KONTRAK_DATA.md`, di dalam blok kode yang
mengutip `catatan_waktu` dan `keputusan_akhir` dari `[JSON]`. Dokumen menyatakan sendiri bahwa
pemeriksaannya menghitung tanda pisah di luar blok kode, dan hasil hitung saya mengonfirmasi nol di
luar blok kode. Namun butir 8 kerangka wajib tidak memberi pengecualian, dan `grep` polos pada
berkas mengembalikan 2. Itu cacat nomor 3.

## 6. Lima field wajib per fitur

Butir 5 kerangka wajib diuji secara struktural: setiap blok fitur dipotong, lalu dicari lima label
`pengguna`, `momen pakai`, `masukan`, `keluaran`, `status bukti`. Tidak ada blok yang kurang.

| Berkas | Blok fitur | Lengkap lima field | Kurang |
|---|---:|---:|---:|
| `01_KATALOG_FITUR.md` | 48 | 48 | 0 |
| `08_KONTRAK_DATA.md` | 21 | 21 | 0 |
| `04_ANTREAN_TINJAUAN.md` | 7 | 7 | 0 |
| `05_KETIDAKSEPAKATAN.md` | 5 | 5 | 0 |
| `06_SWARM_KONSENSUS.md` | 5 | 5 | 0 |
| `09_NASKAH_AKSESIBILITAS.md` bagian 8 | 23 | 23 | 0 |

Untuk `09`, lima field berbentuk tabel tujuh kolom pada bagian 8: 23 baris data, 23 baris berisi,
nol sel kosong. Pola Dynamic Island pada butir 4 juga terpakai di sepuluh berkas, antara lain sebagai
kode abstain `AB-5`, label kekurangan, dan kartu kesiapan kanal.

## 7. Konsistensi tabel

Seluruh blok tabel di empat belas berkas diperiksa jumlah kolomnya, di luar blok kode.

| Berkas | Blok tabel | Baris data |
|---|---:|---:|
| `00_INVENTARIS_RND2_V11.md` | 4 | 50 |
| `00_INVENTARIS_V3_V6.md` | 10 | 61 |
| `00_INVENTARIS_V7_V8.md` | 12 | 59 |
| `00_INVENTARIS_V9_RND1.md` | 21 | 146 |
| `00_VERIFIKASI_INVENTARIS.md` | 9 | 114 |
| `01_KATALOG_FITUR.md` | 5 | 108 |
| `02_RISET_VISUALISASI.md` | 8 | 68 |
| `03_SKOR_KEYAKINAN.md` | 13 | 86 |
| `04_ANTREAN_TINJAUAN.md` | 15 | 116 |
| `05_KETIDAKSEPAKATAN.md` | 22 | 145 |
| `06_SWARM_KONSENSUS.md` | 27 | 166 |
| `07_ARSITEKTUR_INFORMASI.md` | 29 | 246 |
| `08_KONTRAK_DATA.md` | 25 | 254 |
| `09_NASKAH_AKSESIBILITAS.md` | 27 | 174 |
| **total** | **227** | **1.793** |

Blok dengan jumlah kolom tidak konsisten: 0 dari 227.

## 8. Cacat bernomor

Enam cacat, ditulis dengan bahasa biasa, masing masing menyebut berkas dan bagiannya.

### Cacat 1. Janji keluaran yang tidak pernah ditepati, dan satu pemeriksaan yang sebenarnya gagal

`08_KONTRAK_DATA.md` bagian 10.12 menutup dengan empat pemeriksaan yang harus bisa diulang pembaca,
lalu menulis bahwa hasilnya ada di bagian 10.13. Bagian 10.13 tidak ada. Berkas berakhir di 10.12
pada baris 1365. Rujukan ke bagian itu muncul tiga kali, di baris 1199, 1354, dan 1359. Akibatnya
keluaran perintah pada bagian 10.11 juga tidak pernah ditempel, padahal butir 3 kerangka wajib
meminta keluarannya ditempelkan.

Saya menjalankan keempat pemeriksaan itu sendiri, dan pemeriksaan keempat gagal:

| Pemeriksaan pada bagian 10.12 | Syarat | Hasil ukur | Lulus |
|---|---|---:|---|
| jumlah subbagian `#### 5.` | 21 | 21 | ya |
| jumlah baris berpipa | lebih dari 150 | 304 | ya |
| tanda pisah panjang di luar blok kode | 0 | 0 | ya |
| kemunculan tiga kata larangan | 0 | 2 | tidak |

Dua kata larangan itu ada di baris 619 dan 698, keduanya di tengah kalimat teknis dan bukan penutup
laporan, jadi naskahnya sendiri tidak melanggar butir 6. Yang salah adalah rumusan pemeriksaannya:
syarat "harus 0" tidak bisa dipenuhi teks yang memang memakai frasa itu secara wajar. Perbaikan yang
dibutuhkan: bagian 10.13 dibuat dan diisi keluaran nyata, dan syarat pemeriksaan keempat diubah
menjadi "tidak ada kalimat penutup laporan yang memakai tiga kata itu", bukan "kemunculan 0".

### Cacat 2. Rujukan ke bagian yang tidak ada pada dokumen protokol swarm

`06_SWARM_KONSENSUS.md` baris 17 menulis bahwa alasannya ada di bagian 9.5. Bagian 9 hanya punya
9.1, 9.2, dan 9.3. Bagian yang paling mungkin dimaksud adalah 9.3, berjudul keputusan yang menutup
satu butir terbuka riset visualisasi. Perbaikan yang dibutuhkan: ganti 9.5 menjadi 9.3.

### Cacat 3. Dua tanda pisah panjang di dalam kutipan kode

`08_KONTRAK_DATA.md` baris 1219 dan 1238 memuat U+2014 di dalam blok kode kutipan `[JSON]`. Dokumen
menjelaskan bahwa tanda itu bagian dari data sumber dan sengaja tidak diubah, lalu mempersempit
pemeriksaannya ke luar blok kode. Penjelasan itu jujur, tetapi butir 8 kerangka wajib tidak memberi
pengecualian, dan pemeriksa yang menjalankan `grep` polos akan menemukan 2, bukan 0. Perbaikan yang
dibutuhkan: salah satu dari dua hal, ganti tanda itu dengan tanda hubung biasa di dalam kutipan
disertai catatan bahwa karakter sumber diubah, atau nyatakan pengecualian blok kode pada kerangka di
bagian 0 supaya pemeriksa tahu batasnya.

### Cacat 4. Satu berkas dihitung dua panjang baris berbeda

Berkas `scratch/v9_i1/v9_i1_RESULTS.json` ditulis 1.759 baris pada tabel masukan
`04_ANTREAN_TINJAUAN.md` bagian 1, dan 1.758 baris pada tabel masukan
`07_ARSITEKTUR_INFORMASI.md` bagian 1. Keduanya merujuk berkas yang sama pada 57.555 byte. Penyebabnya
berkas itu tidak diakhiri baris baru, sehingga `wc -l` memberi 1.758 dan jumlah baris logis 1.759.
Konvensi yang sama juga dipakai berbeda: `[H]` ditulis 31.946, yaitu hitungan logis, padahal `wc -l`
memberi 31.945. Perbaikan yang dibutuhkan: tetapkan satu konvensi, sebutkan di bagian 1 tiap dokumen,
lalu samakan angka `[J]` di kedua dokumen.

### Cacat 5. Kutipan yang disebut apa adanya ternyata dirapikan

`05_KETIDAKSEPAKATAN.md` bagian 2.3 menulis "Tiga blok pertama, apa adanya" sebelum menempel keluaran
`dss3_calc.py`. Setelah saya jalankan ulang skripnya dan membandingkan keluaran sebenarnya dengan
kutipan, lima baris berbeda: tiga baris pembatas bagian yang diubah menjadi satu baris, dan dua baris
penjelas rumus yang dihilangkan. Seluruh baris data nilainya identik, jadi tidak ada angka yang
bergeser. Yang keliru hanya kata "apa adanya". Perbaikan yang dibutuhkan: ganti menjadi "diringkas
pada baris pembatas" atau tempel keluaran mentah.

### Cacat 6. Ukuran berkas sendiri yang sudah basi

`09_NASKAH_AKSESIBILITAS.md` bagian 9.7 mencantumkan 67.825 byte dan 1.168 baris. Ukuran sebenarnya
68.359 byte dan 1.183 baris. Dokumen menyatakan sendiri bahwa angka itu diukur sebelum suntingan
terakhir dan mengarahkan pembaca ke komentar kartu untuk angka final, jadi ini bukan klaim palsu,
tetapi pembaca yang hanya membuka berkas akan membaca angka yang salah. Perbaikan yang dibutuhkan:
jalankan ulang `stat` dan `wc` sesudah suntingan terakhir lalu perbarui blok itu, atau hapus blok
ukurannya dan ganti dengan rujukan ke berkas, bukan ke nomor bagian.

## 9. Keputusan

**PERLU PERBAIKAN.**

Alasannya bukan karena angkanya salah. Dari tiga puluh angka yang diuji, dua puluh sembilan cocok
dengan sumbernya sampai digit terakhir, termasuk seluruh angka yang paling menentukan: beban 40,15
baris per shift yang bisa dijumlahkan ulang dari enam nilai lambda, bobot dewan 9,15 dan 11,30 yang
bisa dijumlahkan ulang dari kolomnya, dan empat pola konflik yang bisa dihitung ulang dengan
menjalankan skrip yang dikutip dokumen.

Alasannya ada pada janji yang tidak ditepati dan aturan format yang belum bersih. Cacat 1 membuat satu
dokumen menutup dengan rujukan ke bagian yang tidak ada, sekaligus menyembunyikan pemeriksaan yang
sebenarnya gagal. Cacat 3 melanggar butir 8 secara harfiah. Empat cacat lain lebih ringan, tetapi
semuanya bisa diperbaiki tanpa menghitung ulang satu angka pun dan tanpa menggeser satu ambang pun.

Enam perbaikan yang dibutuhkan, semuanya bersifat menambah atau menyunting teks, bukan mengubah
keputusan metodologis:

1. Buat bagian 10.13 pada `08_KONTRAK_DATA.md` dan isi dengan keluaran empat pemeriksaan, lalu ubah
   rumusan pemeriksaan keempat seperti pada cacat 1.
2. Ganti rujukan bagian 9.5 menjadi 9.3 pada `06_SWARM_KONSENSUS.md` baris 17.
3. Selesaikan dua tanda pisah pada `08_KONTRAK_DATA.md` baris 1219 dan 1238.
4. Tetapkan satu konvensi hitung baris dan samakan angka `[J]` pada `04` dan `07`.
5. Ganti kata "apa adanya" pada `05_KETIDAKSEPAKATAN.md` bagian 2.3.
6. Perbarui ukuran berkas pada `09_NASKAH_AKSESIBILITAS.md` bagian 9.7.

Sesudah enam itu dikerjakan, tidak ada lagi temuan yang menghalangi, dan keputusan bisa berubah
menjadi LAYAK SERAH.

## 10. Yang belum diverifikasi di dokumen ini

Ditulis terbuka supaya pembaca tahu batas audit ini.

1. Angka yang berasal dari parquet tidak dihitung ulang dari parquet. Yang diuji adalah kesesuaian
   antara dokumen dan berkas perantara `[JSON]`, `[H]`, dan ledger, bukan antara dokumen dan data
   mentah.
2. Sebelas klaim dan dua puluh tujuh kepala tidak diperiksa satu per satu. Yang diperiksa adalah
   total, lapisan, dan angka yang muncul di lebih dari satu dokumen.
3. Isi baris ledger yang dikutip tidak ditelusuri sampai berkas yang ditunjuk kolom sumbernya.
   Yang diperiksa hanya bahwa baris itu ada dan nilainya sama dengan yang dikutip dokumen.
4. Rujukan literatur LV1 sampai LV19 tidak dibuka ulang, dan tiga sumber yang gagal dibuka pada
   `02_RISET_VISUALISASI.md` tidak dicoba ulang.
5. Tidak ada halaman yang dirender. Semua temuan tampilan pada `07` dan `09` belum diuji pada layar
   sungguhan, termasuk kontras, ukuran sentuh, dan perbesaran 200 persen.
6. Angka operator, termasuk menit per pita dan alur 30 detik pertama, masih target desain dan belum
   diukur pada operator.
7. Berkas `planning/00_*` adalah inventaris dari putaran sebelumnya. Isinya diperiksa untuk aturan
   format dan frasa terlarang, tetapi angka vonis di dalamnya tidak diuji ulang terhadap berkas
   `docs/` yang mereka ringkas.
8. Pemeriksaan jalur memakai pencocokan pola, sehingga jalur yang ditulis tanpa awalan folder, atau
   yang ditulis sebagai nama berkas saja, tidak masuk hitungan 90 jalur.

## 11. Keluaran perintah yang dijalankan

Ditempel di bawah, dengan dua penyuntingan yang dinyatakan terbuka: spasi perata kolom dirapatkan
menjadi satu spasi, dan baris yang berulang dipotong. Tidak ada satu nilai pun yang diubah. Kutipan
baris ledger dan `[JSON]` juga dipotong pada kolom yang tidak dipakai dengan tanda tiga titik.

```
$ ls -l planning/ | wc -l
14
$ find planning -maxdepth 1 -type f ! -name '*.md' | wc -l
0
$ du -sb planning
978457  planning

$ grep -cP '\x{2014}' planning/*.md
00_INVENTARIS_RND2_V11.md:0   00_INVENTARIS_V3_V6.md:0   00_INVENTARIS_V7_V8.md:0
00_INVENTARIS_V9_RND1.md:0    00_VERIFIKASI_INVENTARIS.md:0   01_KATALOG_FITUR.md:0
02_RISET_VISUALISASI.md:0     03_SKOR_KEYAKINAN.md:0     04_ANTREAN_TINJAUAN.md:0
05_KETIDAKSEPAKATAN.md:0      06_SWARM_KONSENSUS.md:0    07_ARSITEKTUR_INFORMASI.md:0
08_KONTRAK_DATA.md:2          09_NASKAH_AKSESIBILITAS.md:0

$ python3 ~/.hermes/cache/scratch/dss3_calc.py   (dijalankan ulang, exit=0)
BAGIAN 0: VERIFIKASI KONVENSI n_aktif = tp + fp
hyd       k2_tidak_tersedia            n_aktif=0      metrik=NULL (head tanpa metrik segmen)
bit_wear  k2_onset_belum               n_aktif=0      metrik=NULL (head tanpa metrik segmen)
tool_wear canary_3rms                  n_aktif=282    metrik=NULL (head tanpa metrik segmen)
jumlah head dengan metrik: 24 | mismatch n_aktif vs tp+fp: 0
jumlah head total: 27
vib       rule_display  persistence   540     0   602    847    69.73
shk       rule_display  persistence   103     0   520  10582    95.36
stuck     rule_display  persistence   210     0   241   2750    92.47
hyd       rule_display  persistence   626   349   250   9176    94.24
tool_wear op_far_calibrated calib_5of27   21     0   284    164    39.45
ssi       rule_display  hybrid_rule_and_persistence   0   0   0   5455   100.00

$ sed -n '271p;10399p;15457p;25883p;23136p;29846p' dashboard/data/head_pages.json
     "lambda": 16.647,
     "lambda": 2.206,
     "lambda": 2.774,
     "lambda": 5.537,
     "lambda": 18.523,
     "lambda": 1006.08,

$ sed -n '804p;809p' scratch/v9_i1/v9_i1_RESULTS.json
  "badge_far": "S6 lintas fold+seed: FP 927, presisi 0,8243, recall 0,6519, FAR 4,10/24jam, lead 8,0 mnt; 7/9 fold lolos FAR<6 dan recall>=0,5",
  "lead_menit": 8.0,

$ sed -n '1414p' scratch/v9_i1/v9_i1_RESULTS.json
    "auto_critical_alarm_slots": 0,

$ sed -n '3292p;3432p' docs/RND_PROVENANCE_LEDGER.md
| S6-058 | 4.0984 | alarm per 24 jam kalender | RUN-KITA | ... | TERUKUR |
| E5-007 | 8.0 | menit | RUN-KITA | ... | TERUKUR |

$ grep -c '^#### 5\.' planning/08_KONTRAK_DATA.md
21
$ grep -c '^|' planning/08_KONTRAK_DATA.md
304
$ grep -c -iE 'tidak bisa|tidak mungkin|terbatas' planning/08_KONTRAK_DATA.md
2
```

## 12. Penutup yang bisa diperiksa

Pembaca yang ingin mengulang audit ini cukup menjalankan lima hal: `stat` dan `wc` pada empat belas
berkas `planning/`, `grep -cP '\x{2014}'` pada seluruh berkas, `sed -n` pada baris `[H]` dan `[JSON]`
yang disebut tabel bagian 3, `python3` pada skrip `dss3_calc.py` yang jalurnya ditulis di
`05_KETIDAKSEPAKATAN.md` baris 122, dan `grep -c '^#### 5\.'` pada `08_KONTRAK_DATA.md`. Seluruh
angka pada dokumen ini berasal dari lima hal itu, dan tidak ada satu angka pun yang ditulis dari
ingatan.
