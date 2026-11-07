# 09 NASKAH COPY, KEADAAN KOSONG, DAN AKSESIBILITAS

Kartu: `t_3219fb16` (PRODUK-3). Board: `fitur-v9-swarm`. Tanggal: 2026-11-01 (WIB).
Workspace: `/mnt/d/Capstone 1(v2)`. Keluaran: berkas ini saja, di folder `planning/`.

Dokumen ini menyerahkan naskah siap tulis untuk sepuluh halaman situs: judul layar, subjudul, tiga
paragraf badan, dan label aksi. Ditambah dua belas pesan keadaan kosong, enam pesan galat, aturan
aksesibilitas yang bisa diukur, dan daftar periksa yang bisa dijalankan pemeriksa lain tanpa membuka
sesi ini. Setiap angka yang muncul di naskah membawa pasangan berkas dan baris, dan setiap aturan
aksesibilitas membawa nomor kriteria WCAG 2.2 yang sudah dibuka pada sesi ini, bukan dari ingatan.

Satu keputusan nada mengikat seluruh naskah: situs ini tidak pernah mengeluh tentang data yang belum
ada. Kekurangan data tampil sebagai label berisi alasan, pemilik, dan satu langkah berikutnya. Pola itu
sudah ditetapkan sebagai pola Dynamic Island pada [AI] baris 599 sampai 600 dan pada [AI] baris 102
sampai 106.

---

## 0. Kerangka wajib dan cara dokumen ini memenuhinya

Delapan butir kerangka dipakai apa adanya, tidak diubah. Tabel ini menyatakan di mana tiap butir
dipenuhi, supaya pemeriksa bisa langsung membuka bagiannya.

| Butir kerangka | Cara dipenuhi di berkas ini | Bukti |
|---|---|---|
| 1. Alarm otomatis bukan tujuan, ML adalah pendukung keputusan dengan skor keyakinan | Tidak satu pun naskah halaman memuat kalimat yang menjanjikan pengiriman pesan otomatis. Kalimat penanda nol slot alarm otomatis dipakai sebagai teks tetap di kaki halaman, dan seluruh label aksi berakhir pada manusia. | bagian 2.2, bagian 3, [AI] baris 186 dan 780 sampai 786 |
| 2. Setiap angka punya sumber berkas dan baris, atau baris ledger | Setiap paragraf yang memuat angka menutup kalimatnya dengan kode berkas dan nomor baris. Kode berkas didefinisikan di bagian 1.1. | bagian 1, bagian 3, bagian 9 |
| 3. Tidak mengklaim sesuatu berjalan tanpa bukti | Perintah yang dijalankan untuk memeriksa berkas ini dan untuk membuka sumber standar ditempel apa adanya di bagian 9. | bagian 9 |
| 4. Kekurangan data dikemas menjadi fitur berguna, pola Dynamic Island | Dua belas pesan keadaan kosong di bagian 4 masing masing membawa pemilik, alasan, dan satu langkah berikutnya. Tidak ada satu pun yang berbunyi sebagai keluhan. | bagian 4 |
| 5. Setiap fitur punya pengguna, momen pakai, masukan, keluaran, status bukti | Tabel bagian 8 memuat kelima field untuk dua puluh tiga fitur yang membawa naskah dan label aksi di dokumen ini. Empat puluh delapan fitur katalog seluruhnya sudah memuat kelima field itu di blok fiturnya masing masing, dan jumlahnya diperiksa dengan `grep` di bagian 9.5. | bagian 8, bagian 9.5 |
| 6. Dilarang menutup dengan kalimat menyerah | Penutup berupa daftar syarat terukur di bagian 10 dan daftar periksa di bagian 7. Tidak ada satu kalimat pun yang menyatakan ketidakmampuan. | bagian 7, bagian 10 |
| 7. Keluaran hanya markdown di `planning/` | Satu berkas keluaran: `planning/09_NASKAH_AKSESIBILITAS.md`. Tidak ada `.py`, `.html`, `.json`, `.csv` yang dibuat sebagai deliverable. | bagian 9.7 |
| 8. Tanpa tanda pisah panjang | Diperiksa dengan `grep -cP` memakai kelas karakter heksadesimal. Rentang angka ditulis dengan kata "sampai" atau tanda hubung biasa. | bagian 9.7 |

---

## 1. Berkas masukan, ukuran byte, dan sumber standar

### 1.1 Berkas proyek yang dibuka

Ukuran diambil dengan `stat -c '%s'` dan `wc -l` pada 2026-11-01, keluarannya ditempel di bagian 9.1.
Berkas [AI] dibaca penuh sampai baris terakhir. Berkas [KAT] dibaca pada blok fitur dan bagian rekap.
Berkas [DSS2] dibaca pada bagian tiga keadaan antrean. Berkas [VR] dibaca penuh.

| Kode | Berkas | Byte | Baris | Yang diambil |
|---|---|---:|---:|---|
| [AI] | `planning/07_ARSITEKTUR_INFORMASI.md` | 87.727 | 1.328 | sepuluh halaman, label aksi, dua belas keadaan tampilan, aturan keterbacaan, syarat naik status |
| [KAT] | `planning/01_KATALOG_FITUR.md` | 166.662 | 2.780 | 48 fitur, lima field wajib per fitur, status bukti bagian 11 |
| [VR] | `planning/02_RISET_VISUALISASI.md` | 32.141 | 335 | sembilan visual terlarang, aturan satu satuan per grafik, sumber LV1 sampai LV16 |
| [DSS2] | `planning/04_ANTREAN_TINJAUAN.md` | 95.168 | 1.428 | tiga keadaan antrean, pemicu angka, ambang kanal absen 0,50 |
| | **Total empat berkas** | **381.698** | **5.871** | |

Angka total dihitung dari empat baris di atas, dan bagian 9.1 menempelkan `wc -c` yang menghasilkan
jumlah yang sama.

### 1.2 Sumber standar aksesibilitas yang dibuka pada sesi ini

Setiap angka aksesibilitas di bagian 6 dan 7 berasal dari kriteria WCAG 2.2 yang dibuka dan dibaca
pada sesi ini. Kalimat kriteria dikutip, bukan diringkas dari ingatan. Alamat lengkap ada di bagian 11.

| Kode | Kriteria | Angka yang diambil | Kalimat kriteria |
|---|---|---|---|
| [W143] | SC 1.4.3 Contrast (Minimum), level AA | 4,5:1 untuk teks; 3:1 untuk teks besar; nilai tidak dibulatkan, 4,499:1 tidak lulus | "has a contrast ratio of at least 4.5:1" dan "Large-scale text and images of large-scale text have a contrast ratio of at least 3:1" |
| [W143b] | SC 1.4.3, definisi teks besar | 18 pt, atau 14 pt tebal, setara 24 px dan 18,5 px | "18 point text or 14 point bold text is judged to be large enough to require a lower contrast ratio" dan "1pt = 1.333px" |
| [W1411] | SC 1.4.11 Non-text Contrast, level AA | 3:1 terhadap warna bersebelahan; 2,999:1 tidak lulus | "have a contrast ratio of at least 3:1 against adjacent color(s)" |
| [W258] | SC 2.5.8 Target Size (Minimum), level AA | 24 x 24 piksel CSS | "is at least 24 by 24 CSS pixels" |
| [W255] | SC 2.5.5 Target Size (Enhanced), level AAA | 44 x 44 piksel CSS | "is at least 44 by 44 CSS pixels" |
| [W1410] | SC 1.4.10 Reflow, level AA | 320 piksel CSS, setara 1.280 piksel pada perbesaran 400 persen | "320 CSS pixels is equivalent to a starting viewport width of 1280 CSS pixels wide at 400% zoom" |
| [W144] | SC 1.4.4 Resize Text, level AA | 200 persen | "text can be resized without assistive technology up to 200 percent without loss of content or functionality" |
| [W413] | SC 4.1.3 Status Messages, level AA | pesan status terbaca teknologi bantu tanpa menerima fokus | "can be programmatically determined through role or properties such that they can be presented to the user by assistive technologies without receiving focus" |
| [W247] | SC 2.4.7 Focus Visible, level AA | indikator fokus terlihat dan tidak dibatasi waktu | "the keyboard focus indicator is visible" dan "The focus indicator must not be time limited" |
| [W2411] | SC 2.4.11 Focus Not Obscured (Minimum), level AA | komponen berfokus tidak tertutup seluruhnya | "the component is not entirely hidden due to author-created content" |
| [W331] | SC 3.3.1 Error Identification, level A | galat disebut dalam teks, bukan hanya warna | "the item that is in error is identified and the error is described to the user in text" |
| [W111] | SC 1.1.1 Non-text Content, level A | setiap isi non teks punya alternatif teks | "All non-text content that is presented to the user has a text alternative that serves the equivalent purpose" |

---

## 2. Nada suara dan larangan gaya

### 2.1 Lima aturan nada

Nada yang dipakai adalah nada orang yang sudah memeriksa. Kalimatnya pendek, angkanya disebut, dan
batasnya ditulis. Tabel ini memasangkan aturan dengan contoh yang bisa ditiru tim website.

| Aturan | Contoh yang dipakai | Contoh yang dihindari |
|---|---|---|
| Sebut angka dan sumbernya dalam satu kalimat | "Keyakinan 61 persen, batas kelas 0,61, FAR 4,10 per 24 jam" | "Keyakinan cukup tinggi" |
| Sebut batas sebelum manfaat | "Pita P4 artinya bukti kuat, bukan artinya kerusakan pasti" | "Sistem mendeteksi kerusakan" |
| Nyatakan keadaan, bukan perasaan | "Jendela tenang, tidak ada baris berprioritas pada shift ini" | "Sayangnya tidak ada data" |
| Setiap keadaan kosong membawa satu langkah berikutnya | "Buka antrean pantau, 12 baris menunggu" | "Data kosong" |
| Sebut siapa pemutus | "Keputusan ada di supervisor, sistem menampilkan bahan" | "Sistem memutuskan" |

Alasan aturan pertama dan kedua sudah tertulis di hulu: satu angka keyakinan tanpa sebaran dibaca
sebagai kepastian ([VR] baris 246), dan angka keyakinan bukan peluang kerusakan ([AI] baris 683 sampai
684). Alasan aturan kelima adalah slot alarm otomatis bernilai 0 ([AI] baris 204) dan empat tingkat
dewan seluruhnya berakhir pada manusia ([AI] baris 96 sampai 100).

### 2.2 Istilah terlarang di layar

Tiga istilah dilarang tampil, dan penggantinya sudah ditetapkan ([AI] baris 662). Larangan ini berlaku
untuk seluruh naskah di bagian 3, 4, dan 5.

| Istilah terlarang | Dipakai untuk apa | Pengganti di layar | Sumber |
|---|---|---|---|
| "alarm" untuk tingkat dewan | empat tingkat TK-1 sampai TK-4 | "tingkat pantauan", dengan nama tingkatnya | [AI] baris 662, [AI] baris 475 |
| "peluang rusak" untuk keyakinan bukti | angka 0 sampai 1 pada kartu keyakinan | "keyakinan bukti", dengan batas kelasnya | [AI] baris 662, [AI] baris 683 sampai 684 |
| "prioritas" untuk pita P1 sampai P5 | lima pita keyakinan | "pita P1" sampai "pita P5", dengan batasnya | [AI] baris 662, [AI] baris 254 |

Satu aturan tambahan: kata "aman" dilarang pada keadaan kosong, karena kanal absen menghasilkan nol
palsu. Penggantinya "tidak dinilai, kanal absen" bila rasio kanal absen di atas 0,50 ([DSS2] baris 528
sampai 531).

### 2.3 Larangan tanda pisah panjang

Tanda pisah panjang dan tanda pisah sedang tidak dipakai di seluruh berkas ini. Rentang angka ditulis
dengan kata "sampai", misalnya "0,00 sampai 0,19". Pemisah klausa memakai koma, titik dua, atau kata
sambung sesuai hubungannya. Pemeriksaan ada di bagian 9.7 dan hasilnya nol untuk kedua karakter.

### 2.4 Larangan kalimat penutup yang menyatakan ketidakmampuan

Tidak ada kalimat yang menyatakan ketidakmampuan menyelesaikan pekerjaan. Bila satu komponen belum
tersedia, yang ditulis adalah syaratnya, pemiliknya, dan uji yang menandai kenaikan status. Pola ini
sudah dipakai di [AI] bagian 11 baris 1023 sampai 1034, dan dokumen ini memakai pola yang sama di
bagian 10.

---

## 3. Naskah copy sepuluh halaman

Setiap halaman ditulis dengan pola yang sama: judul layar, subjudul, tiga paragraf badan, dan label
aksi. Judul layar dipakai untuk `<title>` dan `<h1>`, jadi keduanya berbunyi sama supaya tab peramban
dan judul halaman tidak pernah berbeda. Subjudul satu kalimat, dan wajib memuat pertanyaan yang
dijawab halaman itu, sesuai prinsip satu halaman satu pertanyaan ([AI] baris 85 sampai 88).

Nomor baris pada setiap butir menunjuk ke [AI] bagian 4, tempat tujuan, blok konten, dan aksi halaman
itu ditetapkan.

### 3.1 PG-00 Beranda hari ini

**Judul layar.** Beranda hari ini

**Subjudul.** Apa yang perlu saya lihat sekarang, dan seberapa kuat buktinya.

**Paragraf 1.** Halaman ini menjawab satu pertanyaan dalam satu layar. Baris paling atas menyebut
tingkat pantauan hari itu, dukungan berbobot dalam persen, jumlah dewan yang hadir, cakupan bobot, dan
waktu hitungnya. Pada segmen terakhir, tingkat yang tampil adalah TK-2 PANTAU dengan dukungan 18,23
persen, kuorum 6 dari 7, dan cakupan bobot 1,00 ([AI] baris 198 sampai 201).

**Paragraf 2.** Di bawah baris itu ada tiga kartu fokus, masing masing memuat klaim, jendela, lencana
pita, satu batang 0 sampai 1 dengan garis batas kelas, jumlah kepala yang dinilai, badge FAR, lead, dan
umur. Beban shift ditulis empat angka: 40,15 baris per shift, nilai tengah 39, p95 61, dan sisa anggaran
30 menit. Dengan kapasitas 7 sampai 9 baris pada anggaran itu, shift pada p95 menunda sekitar 52 baris
([AI] baris 202 sampai 205).

**Paragraf 3.** Halaman ini tidak pernah mengirim pesan sendiri, dan itu tertulis di kaki halaman:
nol slot alarm otomatis, keputusan akhir manusia ([AI] baris 204 dan 780 sampai 786). Bila tidak ada
klaim pada pita P2 ke atas, baris atas berubah menjadi TK-1 TENANG dan tiga kartu diganti satu kalimat
berisi jumlah jendela tenang. Angka keyakinan di halaman ini adalah keyakinan bukti, bukan peluang
kerusakan: 61 persen berarti `K_tampil` 0,61 ([AI] baris 216 sampai 217).

**Label aksi.**

| Label | Menuju | Kapan tampil |
|---|---|---|
| Buka antrean shift | PG-02, dengan anggaran 30 menit dan urutan berlapis yang sama | selalu |
| Catat keputusan | formulir satu baris yang menulis ke log keputusan | setelah satu baris dipilih |
| Buka bukti angka | PG-07 | selalu, di kaki halaman |

Sumber aksi: [AI] baris 190 sampai 192. Status halaman: siap sekarang, dengan satu blok siap sebagian
([AI] baris 124).

### 3.2 PG-01 Kepercayaan

**Judul layar.** Kepercayaan

**Subjudul.** Boleh saya percaya angka ini, dan sejauh mana.

**Paragraf 1.** Halaman ini rumah aturan kepercayaan untuk semua angka model di situs. Baris ringkasnya
menyebut 27 kepala, terbagi 5 lapis L0, 11 lapis L1, 9 lapis L2, dan 2 lapis L3, dengan nol slot alarm
otomatis ([AI] baris 234). Di bawahnya ada sebelas kartu papan vonis, satu per klaim, dengan urutan
tetap: nama kelas, tugas satu kalimat, lencana tier, dua sampai empat angka penopang, daftar syarat yang
menggantung, dan tanggal potong data ([AI] baris 235).

**Paragraf 2.** Setiap angka keyakinan tampil bersama pita dan batas kelasnya. Batas lima pita adalah
P1 0,00 sampai 0,19, P2 0,20 sampai 0,39, P3 0,40 sampai 0,59, P4 0,60 sampai 0,79, dan P5 0,80 sampai
1,00 ([AI] baris 254). Batas atas bukti berbeda per kelas, dan itu ditulis apa adanya: hyd K-i 0,6100
dengan pita tertinggi P4, vib 0,4950 dengan pita tertinggi P3, bit_wear K-1 0,2525 dengan pita
tertinggi P2 ([AI] baris 255 sampai 257).

**Paragraf 3.** Tombol tindakan tidak dirender pada pita P1 dan P2, dan itu keputusan tampilan, bukan
kekurangan ([AI] baris 246 sampai 248). Tier pada halaman ini menilai kesiapan pemakaian, bukan mutu
model, sehingga engine dengan sinyal kuat bisa bertier rendah karena lapisan B belum terukur
([AI] baris 269 sampai 271). Angka yang belum boleh dikutip tetap tampil, dengan lencana dan tanpa
tombol salin rujukan ([AI] baris 975).

**Label aksi.**

| Label | Menuju | Kapan tampil |
|---|---|---|
| Buka alasan | tiga komponen S_A, S_B, S_C beserta rujukan barisnya | pada kartu berpita P3 ke atas |
| Buka aturan konflik | buku konflik K-1 sampai K-7 | saat dua kepala berbeda putusan |
| Buka bukti angka | PG-07 pada baris ledger yang menopang angka itu | selalu |

Sumber aksi: [AI] baris 246 sampai 248. Status halaman: siap sekarang, dua fitur siap sebagian dan satu
rancangan ([AI] baris 125).

### 3.3 PG-02 Perencanaan maintenance

**Judul layar.** Perencanaan maintenance

**Subjudul.** Apa yang saya kerjakan shift ini, dan berapa menit tersedia.

**Paragraf 1.** Halaman ini mengubah skor menjadi daftar berurut dengan umur item, lalu memotongnya
dengan anggaran waktu yang tertulis, sehingga daftar tidak pernah menjadi tumpukan tanpa ujung
([AI] baris 277 sampai 280). Banner anggaran menyebut empat angka: anggaran menit, jumlah terlayani,
jumlah ditunda, dan total menit tunda ([AI] baris 290).

**Paragraf 2.** Tabel antrean menampilkan sembilan kolom: nomor, klaim, jendela, kepala, keyakinan,
pita, umur, menit, dan aksi. Kolom pertama adalah pengenal yang terbaca manusia, bukan kode internal
([AI] baris 291, [VR] baris 252). Empat pita umur dipakai per shift: 0 sampai 15, 16 sampai 60, 61
sampai 120, dan di atas 120 menit ([AI] baris 293).

**Paragraf 3.** Beban tinjauan per shift adalah 40,15 baris dengan nilai tengah 39 dan p95 61, dan angka
itu mengukur beban, bukan risiko ([AI] baris 310, [AI] baris 328 sampai 330). Empat lapis urutan dengan
jatah minimum per klaim mencegah satu engine mengisi seluruh anggaran. Bila anggaran habis, angka tunda
dan menit kekurangan wajib tampil di banner, bukan di catatan kaki ([AI] baris 971).

**Label aksi.**

| Label | Menuju | Kapan tampil |
|---|---|---|
| Tutup baris | menulis satu baris log keputusan dan menghentikan pertambahan umur | pada baris terpilih |
| Tunda | formulir alasan wajib, menambah angka tunda pada neraca | pada baris terpilih |
| Buka antrean penuh | tabel lengkap dengan penghitung tunda | saat baris tunda lebih dari nol |

Sumber aksi: [AI] baris 302 sampai 304. Status halaman: siap sekarang, dua fitur siap sebagian
([AI] baris 126).

### 3.4 PG-03 Kualitas data

**Judul layar.** Kualitas data

**Subjudul.** Apakah data yang menopang angka ini ada dan layak dipakai.

**Paragraf 1.** Halaman ini diperiksa sebelum pembaca mempercayai panel mana pun. Tujuh dari sepuluh
fiturnya justru dibangun dari kekurangan data, dan itu dinyatakan terbuka ([AI] baris 338 sampai 340).
Kartu kesiapan kanal menyebut kanal mana yang siap, mana yang tipis, dan mana yang absen, sebelum panel
dinyalakan ([AI] baris 350).

**Paragraf 2.** Antrean parse dibuka dengan tiga angka: 3.906 berkas belum diparse, yaitu 54,63 persen
dari 7.150 berkas, dan 213 label yang belum masuk fold mana pun ([AI] baris 369 sampai 371). Kanal yang
absen tidak ditampilkan sebagai nilai nol, melainkan sebagai lencana "tidak logging" beserta sebabnya
([AI] baris 377 sampai 379).

**Paragraf 3.** Contoh nyata yang dipakai di halaman ini adalah `ssi.rule_display`, dengan kanal absen
5.268 dari 5.455 jendela, yaitu 0,9657, sehingga kode AB-2 terpicu karena ambangnya di atas 0,50
([AI] baris 372 sampai 373). Kanal yang setengah kosong tidak pernah dipakai sebagai bukti fisik, dan
itu justru yang dicegah pemilih kanal ([AI] baris 385 sampai 386).

**Label aksi.**

| Label | Menuju | Kapan tampil |
|---|---|---|
| Minta data | kartu permintaan data bertanda tangan berisi kanal, sumur, alasan angka, dan pemilik | pada baris yang absen |
| Buka bukti kanal | PG-07 pada baris ledger yang menopang status kanal | pada setiap kartu kesiapan kanal |
| Buka peta label | daftar label yang menunggu fold beserta alasannya | pada penghitung label |

Sumber aksi: [AI] baris 361 sampai 363. Status halaman: siap sekarang, dua fitur siap sebagian
([AI] baris 127).

### 3.5 PG-04 Perbandingan mesin

**Judul layar.** Perbandingan mesin

**Subjudul.** Mesin mana yang lebih baik, pada kelas apa, dan dengan harga apa.

**Paragraf 1.** Halaman ini menjawab pertanyaan keunggulan, termasuk ketika jawabannya adalah keduanya
sama atau keduanya tidak sepakat ([AI] baris 390 sampai 392). Balapan model melawan baseline persistence
ditampilkan satu baris per fold, dengan dua nilai, selisih, dan vonis ([AI] baris 402).

**Paragraf 2.** Matriks kesepakatan menunjukkan bahwa 11 kepala lapis L1 sebenarnya hanya 7 fungsi
berbeda, dengan 4 pasangan identik ([AI] baris 421). Putusan tiga kepala hyd juga ditulis: rule 975,
persistence 876, dan hibrida 626, dengan 349 jendela hanya dimiliki rule dan 250 hanya dimiliki
persistence ([AI] baris 422 sampai 423).

**Paragraf 3.** Kesepakatan status pada seluruh jendela berkisar 92,47 sampai 99,43 persen, tetapi pada
kelas positif angkanya jatuh ke 23,81 persen untuk shk dan 0,00 persen Jaccard untuk ssi
([AI] baris 424 sampai 425). Karena itu dua kepala identik tidak pernah ditampilkan sebagai dua bukti:
lencana kembar muncul dengan alasan, dan bobotnya dideduplikasi sebelum dijumlahkan ([AI] baris 430
sampai 431).

**Label aksi.**

| Label | Menuju | Kapan tampil |
|---|---|---|
| Buka jendela | putusan tiap kepala pada jendela yang sama beserta jumlah aktifnya | pada sel matriks |
| Bandingkan komposisi | panel kesetaraan head hyd dengan bentuk pertukaran presisi dan recall | pada kelas hyd |
| Buka bukti sirkularitas | penanda bahwa target mekanika tidak layak jadi bukti | pada kartu rekam jejak |

Sumber aksi: [AI] baris 413 sampai 415. Status halaman: siap sekarang, dua fitur siap sebagian
([AI] baris 128).

### 3.6 PG-05 Linimasa keputusan

**Judul layar.** Linimasa keputusan

**Subjudul.** Apa yang diputuskan, kapan, oleh siapa, dan apa akibatnya.

**Paragraf 1.** Halaman ini memisahkan tiga sumbu yang mudah tertukar: tier kepala, pita klaim, dan
tingkat dewan ([AI] baris 444 sampai 446). Tangga empat tingkat ditulis lengkap dengan syarat angka,
pemutus, dan batas waktunya. Kuorum kehadiran 4 dari 7 engine, cakupan bobot minimum 0,50, dan batas
dominasi satu klaim 35 persen bobot dewan ([AI] baris 475 sampai 478).

**Paragraf 2.** Buku konflik berisi tujuh aturan K-1 sampai K-7 dan lima pemicu turunnya manusia H-1
sampai H-5 ([AI] baris 483 sampai 484). Batas waktu tindak lanjut adalah 1 shift atau 8 jam pada TK-3,
dan 1 jam pada TK-4 ([AI] baris 481 sampai 482). Tidak ada tingkat yang mengirim pesan sendiri
([AI] baris 492).

**Paragraf 3.** Log keputusan adalah tabel waktu, aktor, keputusan, dan akibat, dengan penghitung
terbuka ([AI] baris 460). Selama log belum berisi, halaman menampilkan kalimat yang membedakan "belum
ada keputusan tercatat" dari "tidak ada peringatan", persis pembedaan yang ditetapkan di hulu
([AI] baris 487 sampai 489). Label "abaikan" pada log adalah keputusan operator, bukan penilaian
kebenaran model ([AI] baris 493 sampai 494).

**Label aksi.**

| Label | Menuju | Kapan tampil |
|---|---|---|
| Catat keputusan | menulis waktu, aktor, keputusan, dan akibat ke log, lalu menutup baris | pada baris terbuka |
| Buka aturan konflik | aturan K-1 sampai K-7 beserta bukti yang memaksanya | selalu |
| Buka pemicu manusia | lima pemicu H-1 sampai H-5 | saat konflik saling meniadakan |

Sumber aksi: [AI] baris 467 sampai 469. Status halaman: siap sebagian untuk log, siap sekarang untuk
garis waktu ([AI] baris 129).

### 3.7 PG-06 Alat bantu insinyur

**Judul layar.** Alat bantu insinyur

**Subjudul.** Langkah apa yang harus dijalankan sebelum memindahkan ambang atau mengutip angka.

**Paragraf 1.** Halaman ini berisi prosedur, bukan panel angka, dan setiap prosedur punya keluaran yang
bisa diperiksa. Lima fiturnya berstatus satu siap sekarang dan empat siap sebagian ([AI] baris 500
sampai 502). Wizard kalibrasi menuntun empat langkah sebelum pindah sumur: periksa drift, pilih titik
operasi, uji jalan, dan catat hasil ([AI] baris 513).

**Paragraf 2.** Panduan skrip verifikasi memuat perintah yang bisa dijalankan ulang beserta keluaran
yang diharapkan, sehingga satu angka bisa diuji orang lain tanpa membuka sesi penyusunnya
([AI] baris 514). Kartu kelayakan sinyal memberi vonis layak atau tidak sebelum dekomposisi dijalankan
([AI] baris 515).

**Paragraf 3.** Prosedur di halaman ini mencegah pemindahan ambang tanpa uji, bukan memberi izin
memindahkannya ([AI] baris 538 sampai 539). Bila satu langkah belum bisa dijalankan, halaman
menampilkan syarat yang dibutuhkan beserta pemiliknya, bukan tombol mati ([AI] baris 534 sampai 536).

**Label aksi.**

| Label | Menuju | Kapan tampil |
|---|---|---|
| Jalankan pemeriksaan | perintah verifikasi satu angka beserta keluaran yang diharapkan | pada panduan skrip |
| Ajukan permintaan data | kartu INS-05 dengan kolom pemilik dan tanda tangan | pada kartu kanal |
| Buka syarat langkah | syarat satu langkah beserta pemiliknya | pada langkah yang menunggu komponen |

Sumber aksi: [AI] baris 520 sampai 522. Status halaman: siap sebagian untuk empat fitur, siap sekarang
untuk satu ([AI] baris 130).

### 3.8 PG-07 Bukti angka

**Judul layar.** Bukti angka

**Subjudul.** Dari mana angka ini, dan boleh dikutip atau belum.

**Paragraf 1.** Halaman ini satu satunya tempat di situs yang menampilkan jalur angka dari berkas
mentah sampai kalimat di layar, dan halaman ini pula yang menahan angka yang belum boleh dikutip
([AI] baris 545 sampai 547). Lencana provenance punya tiga warna: boleh dikutip, boleh dikutip dengan
catatan metode, dan belum boleh dikutip ([AI] baris 557).

**Paragraf 2.** Tabel rujukan memuat tujuh kolom: angka, nilai, satuan, berkas sumber, baris, status
TERUKUR atau TURUNAN, dan tanggal uji ([AI] baris 558). Tiga entri ledger dipakai sebagai contoh nyata:
S6-058 bernilai 4,0984 alarm per 24 jam kalender pada baris 3292, E5-007 bernilai 8,0 menit pada baris
3432, dan E5-008 bernilai 6 tinjauan per shift pada baris 3433 ([AI] baris 574 sampai 576).

**Paragraf 3.** Pengunci rujukan memeriksa bahwa baris yang dirujuk benar benar berisi angka itu, dan
uji mutasi sengaja merusak satu angka untuk membuktikan pemeriksa bisa gagal ([AI] baris 559 sampai
560). Daftar dokumen yang belum dibuka ditulis terbuka: 119 dokumen di `docs/`, 69 di antaranya belum
pernah dibuka ([AI] baris 563, [AI] baris 577). Angka yang belum boleh dikutip tetap tampil di halaman
asalnya, dengan lencana dan tanpa kemampuan menyalin rujukan ([AI] baris 580 sampai 582).

**Label aksi.**

| Label | Menuju | Kapan tampil |
|---|---|---|
| Periksa rujukan | baris ledger dan baris berkas sumber berdampingan | pada setiap baris tabel |
| Salin rujukan | pasangan berkas dan baris, bukan hanya angkanya | pada angka berstatus boleh dikutip |
| Buka daftar dokumen | 119 dokumen dengan penanda sudah atau belum dibuka | selalu, di kaki tabel |

Sumber aksi: [AI] baris 566 sampai 567. Status halaman: siap sekarang ([AI] baris 131).

### 3.9 PG-08 Batas dan syarat data

**Judul layar.** Batas dan syarat data

**Subjudul.** Apa yang belum ada, siapa pemiliknya, dan apa syaratnya.

**Paragraf 1.** Halaman ini rumah resmi pola Dynamic Island: setiap kekurangan data tampil sebagai kartu
berlabel dengan pemilik dan syarat, bukan sebagai kalimat penutup ([AI] baris 598 sampai 600). Peta kode
abstain memuat lima kode AB-1 sampai AB-5, masing masing dengan syarat terpicu, tampilan, dan satu
contoh nyata ([AI] baris 610).

**Paragraf 2.** Peta lapis L3 menyebut dua kepala yang belum dinilai, yaitu hyd k2_tidak_tersedia dan
bit_wear k2_onset_belum ([AI] baris 611, [AI] baris 626). Slot nilai lapisan B berjumlah lima, semuanya
kosong dan berlabel pemilik data, untuk menerjemahkan jam henti ke nilai uang ([AI] baris 612, [AI]
baris 627).

**Paragraf 3.** Status per fitur ditulis terbuka: 32 siap sekarang, 15 siap sebagian, dan 1 masih
rancangan, yaitu KEP-04 ([AI] baris 628 sampai 630). Halaman ini tidak punya keadaan kosong, karena
setiap barisnya sudah berisi syarat, pemilik, dan uji. Bila satu syarat terpenuhi, barisnya berubah
menjadi "terpenuhi" dengan tanggal dan bukti, sehingga halaman tetap berguna pada hari pertama
([AI] baris 634 sampai 637).

**Label aksi.**

| Label | Menuju | Kapan tampil |
|---|---|---|
| Buka syarat | syarat satu fitur beserta pemilik data dan uji yang sudah ada | pada setiap baris tabel |
| Minta akses data | kartu INS-05 dengan kolom tanda tangan | pada slot yang pemiliknya sudah bernama |
| Buka peta pemilik | daftar pemilik peta sumur, tarif biaya, identitas alat, kanal baru, dan deret per menit | selalu |

Sumber aksi: [AI] baris 618 sampai 619. Status halaman: siap sebagian, dengan slot pemilik data
([AI] baris 132).

### 3.10 PG-09 Kamus dan kuis angka

**Judul layar.** Kamus dan kuis angka

**Subjudul.** Istilah ini artinya apa, dan bagaimana angka ini diuji.

**Paragraf 1.** Halaman ini untuk pembaca baru, dosen penguji, dan staf yang berganti shift. Kamusnya
memuat lima belas istilah, dikelompokkan per sumbu: tier kepala, lapisan L0 sampai L3, pita P1 sampai P5,
kode abstain AB, tingkat TK, keyakinan bukti, FAR, lead, umur item, cakupan, kuorum, batas dominasi,
ECE, kembar, dan bisu ([AI] baris 658, [AI] baris 671).

**Paragraf 2.** Peta tiga sumbu memisahkan tier kepala, pita klaim, dan tingkat dewan beserta
pemutusnya, karena ketiganya paling sering tertukar ([AI] baris 659). Kuisnya berisi sepuluh pertanyaan
angka dengan jawaban yang bisa diperiksa, dan setiap jawaban menunjuk batas angkanya ([AI] baris 660,
[AI] baris 672).

**Paragraf 3.** Halaman ini menutup tiga salah baca yang paling sering: "keyakinan 61 persen" dibaca
sebagai peluang kerusakan, "P4" dibaca sebagai prioritas empat, dan "TK-4" dibaca sebagai tingkat
bahaya ([AI] baris 682 sampai 686). Kamus tidak bergantung pada data yang belum ada, sehingga halaman
ini berstatus siap sekarang ([AI] baris 678 sampai 680).

**Label aksi.**

| Label | Menuju | Kapan tampil |
|---|---|---|
| Mulai kuis | sepuluh pertanyaan, dinilai terhadap angka tercatat | selalu |
| Buka istilah | baris kamus untuk satu istilah bertanda | pada setiap istilah bertanda |
| Buka peta tiga sumbu | tabel tier kepala, pita klaim, dan tingkat dewan | selalu |

Sumber aksi: [AI] baris 664 sampai 665. Status halaman: siap sekarang ([AI] baris 133).

### 3.11 Rekap naskah sepuluh halaman

| Halaman | Judul layar | Paragraf | Label aksi | Status bukti halaman |
|---|---|---:|---:|---|
| PG-00 | Beranda hari ini | 3 | 3 | siap sekarang, satu blok siap sebagian |
| PG-01 | Kepercayaan | 3 | 3 | siap sekarang, dua siap sebagian, satu rancangan |
| PG-02 | Perencanaan maintenance | 3 | 3 | siap sekarang, dua siap sebagian |
| PG-03 | Kualitas data | 3 | 3 | siap sekarang, dua siap sebagian |
| PG-04 | Perbandingan mesin | 3 | 3 | siap sekarang, dua siap sebagian |
| PG-05 | Linimasa keputusan | 3 | 3 | siap sebagian untuk log |
| PG-06 | Alat bantu insinyur | 3 | 3 | siap sebagian empat, siap sekarang satu |
| PG-07 | Bukti angka | 3 | 3 | siap sekarang |
| PG-08 | Batas dan syarat data | 3 | 3 | siap sebagian, dengan slot pemilik |
| PG-09 | Kamus dan kuis angka | 3 | 3 | siap sekarang |

Jumlah baris data tabel di atas: 10. Jumlah paragraf badan seluruhnya 30, dan jumlah label aksi
seluruhnya 30.

---

## 4. Dua belas pesan keadaan kosong

Setiap pesan memakai pola yang sama: pemicu berupa angka, judul pendek, badan yang menyebut alasan dan
pemilik, satu label aksi, dan pengaturan ARIA. Tidak satu pun memakai kata "aman" atau "kosong" sebagai
kalimat akhir, karena kosong bukan bukti sehat ([DSS2] baris 526 sampai 531).

### 4.1 EK-01 Jendela tenang

**Pemicu.** Tidak ada klaim pada pita P2 ke atas pada shift itu ([AI] baris 964).

**Judul.** Jendela tenang

**Badan.** Tidak ada baris berprioritas pada shift ini. Baris pantau pita P2 tetap tersedia beserta
penghitungnya, dan waktu pembaruan terakhir tertulis di blok yang sama, misalnya 14:33 pada segmen
terakhir ([AI] baris 793). Anggaran 30 menit tidak dialihkan otomatis ke baris pantau
([DSS2] baris 519 sampai 523).

**Aksi.** "Buka antrean pantau", menuju PG-02 dengan saringan pita P2.

**ARIA.** `role="status"` dengan `aria-live="polite"`, sehingga perubahan diumumkan tanpa memindahkan
fokus ([W413]).

**Sumber.** [DSS2] baris 514 sampai 532, [AI] baris 964.

### 4.2 EK-02 Tanpa kepala berskor

**Pemicu.** Bobot klaim bernilai 0 ([AI] baris 965).

**Judul.** Tidak dinilai, belum ada kepala berskor

**Badan.** Klaim ini belum punya kepala yang memberi skor pada jendela ini. Kode AB-1. Daftar kepala
yang menunggu ditampilkan di bawah kalimat ini, sehingga pembaca tahu apa yang ditunggu, bukan hanya
tahu bahwa angkanya tidak ada.

**Aksi.** "Buka daftar kepala menunggu", membuka panel kepala dengan status kosong per kepala.

**ARIA.** `role="note"` dengan `aria-describedby` menunjuk kode abstain AB-1.

**Sumber.** [AI] baris 965, [AI] baris 261.

### 4.3 EK-03 Data sensor kurang

**Pemicu.** Rasio `n_nodata / n_windows` lebih dari 0,50 ([AI] baris 966).

**Judul.** Tidak dinilai, kanal absen 96,6 persen

**Badan.** Dari 5.455 jendela, 5.268 jendela tidak punya data kanal, yaitu 0,9657. Kode AB-2. Angka
keyakinan diganti tanda, dan kanal yang absen ditampilkan per nama. Penyebabnya sumur tidak logging,
bukan sensor rusak ([DSS2] baris 528 sampai 531).

**Aksi.** "Buka kartu kesiapan kanal", menuju PG-03 pada sumur itu.

**ARIA.** `role="note"` dengan `aria-describedby` menunjuk kode AB-2 dan persen kanal absen.

**Sumber.** [AI] baris 966, [AI] baris 372, [DSS2] baris 528 sampai 531.

### 4.4 EK-04 Skor jendela belum diekspor

**Pemicu.** Hanya ringkasan min, median, dan maks yang tersedia ([AI] baris 967).

**Judul.** Pita ringkasan, skor jendela belum diekspor

**Badan.** Untuk jendela ini hanya tersedia ringkasan min, median, dan maks. Kode AB-3. Pita ringkasan
yang ada tetap ditampilkan, dan angka per jendela menunggu ekspor berikutnya.

**Aksi.** "Buka pita ringkasan", menampilkan tiga nilai ringkasan dengan satuan masing masing.

**ARIA.** `role="note"` dengan `aria-describedby` menunjuk kode AB-3.

**Sumber.** [AI] baris 967, [AI] baris 261.

### 4.5 EK-05 Klaim lapis L3

**Pemicu.** Klaim berada pada lapis pemakaian L3 ([AI] baris 968).

**Judul.** Belum layak pakai, klaim lapis L3

**Badan.** Klaim ini berada di lapis L3, sehingga tidak punya pita keyakinan. Kode AB-4. Dua kepala di
lapis ini adalah hyd k2_tidak_tersedia dan bit_wear k2_onset_belum, dan alasan masing masing ditulis di
kartu ([AI] baris 626).

**Aksi.** "Buka alasan lapis", menampilkan status dan alasan dari lapisan.

**ARIA.** `role="note"` dengan `aria-describedby` menunjuk kode AB-4.

**Sumber.** [AI] baris 968, [AI] baris 626.

### 4.6 EK-06 Kepala bisu

**Pemicu.** `n_aktif` bernilai 0 pada segmen ([AI] baris 969).

**Judul.** Kepala bisu pada jendela ini

**Badan.** Kepala ini tidak menyala satu kali pun pada jendela ini. Kode AB-5. Bisu bukan penolakan,
dan angka kesepakatan 100 persen dengan kepala bisu tidak boleh dibaca sebagai kesepakatan
([AI] baris 436 sampai 438).

**Aksi.** "Buka riwayat kepala", menampilkan jumlah aktif per jendela untuk kepala itu.

**ARIA.** `role="note"` dengan `aria-describedby` menunjuk kode AB-5.

**Sumber.** [AI] baris 969, [AI] baris 436 sampai 438.

### 4.7 EK-07 Keyakinan rendah

**Pemicu.** Pita P1 atau P2 ([AI] baris 970).

**Judul.** Pantau, keyakinan di pita P2

**Badan.** Batas atas bukti kelas ini 0,2525, sehingga pita tertingginya P2, seperti pada bit_wear K-1
([AI] baris 257). Angka ini bukan model yang salah menilai, melainkan kelas yang buktinya belum cukup
untuk menaikkan tindakan. Baris ini tidak masuk anggaran kerja dan tidak punya tombol tindakan
([AI] baris 325 sampai 326).

**Aksi.** "Buka batas atas", menampilkan batas kelas dan alasan pemotongannya.

**ARIA.** `role="note"` tanpa `aria-live`, karena keadaan ini tetap sepanjang shift dan tidak perlu
diumumkan berulang.

**Sumber.** [AI] baris 970, [AI] baris 257, [AI] baris 325 sampai 326.

### 4.8 EK-08 Beban melebihi anggaran

**Pemicu.** Baris terlayani kurang dari baris masuk ([AI] baris 971).

**Judul.** 52 baris ditunda, kekurangan 208 menit

**Badan.** Anggaran 30 menit melayani 7 sampai 9 baris, sementara shift pada p95 membawa 61 baris.
Pita P4 dan P3 selalu dilayani lebih dulu. Angka tunda ini wajib dibaca supervisor, bukan catatan kaki
([DSS2] baris 502 sampai 507).

**Aksi.** "Buka daftar tunda", menampilkan baris tunda bernomor beserta menit kekurangannya.

**ARIA.** `role="status"` dengan `aria-live="polite"` dan `aria-atomic="true"`, karena dua angka di
dalamnya harus diumumkan sebagai satu kalimat.

**Sumber.** [AI] baris 971, [DSS2] baris 502 sampai 507.

### 4.9 EK-09 Log keputusan kosong

**Pemicu.** Belum ada keputusan tercatat ([AI] baris 974).

**Judul.** Belum ada keputusan tercatat

**Badan.** Kalimat ini berbeda arti dari "tidak ada peringatan". Log masih kosong karena pencatatan baru
dimulai, sementara peringatan yang tampil di halaman lain tetap berlaku. Skema pencatatan sedang
disiapkan, dan pemiliknya supervisor ([AI] baris 1030).

**Aksi.** "Catat keputusan pertama", membuka formulir satu baris yang menulis ke log.

**ARIA.** `role="status"` dengan `aria-live="polite"`.

**Sumber.** [AI] baris 974, [AI] baris 487 sampai 489.

### 4.10 EK-10 Angka belum boleh dikutip

**Pemicu.** Status provenance kuning atau merah ([AI] baris 975).

**Judul.** Boleh dibaca, belum boleh dikutip

**Badan.** Angka ini tampil dengan lencana dan tanpa tombol salin rujukan. Yang dibutuhkan sebelum
statusnya naik adalah penutupan lima cacat pemblokir C-01 sampai C-05, dan pemiliknya auditor internal
([AI] baris 1032).

**Aksi.** "Buka syarat pengutipan", menampilkan syarat yang tersisa beserta pemiliknya.

**ARIA.** `role="note"` dengan `aria-describedby` menunjuk nama status provenance.

**Sumber.** [AI] baris 975, [AI] baris 580 sampai 582, [AI] baris 1032.

### 4.11 EK-11 Slot nilai lapisan B kosong

**Pemicu.** Slot nilai belum diisi ([AI] baris 627).

**Judul.** Lima slot menunggu pemilik data

**Badan.** Kelima slot ini menerjemahkan jam henti ke nilai uang. Semuanya kosong dan berlabel pemilik,
dan slot kosong lebih jujur daripada angka tanpa pemilik ([AI] baris 641 sampai 643). Jam hentinya
sendiri sudah tersedia: 39.397,986 jam tercatat, dengan 2.739,667 jam pada equipment failure
([VR] baris 203 sampai 204).

**Aksi.** "Minta akses data", membuka kartu INS-05 dengan kolom tanda tangan.

**ARIA.** `role="group"` dengan `aria-labelledby` menunjuk judul slot, dan setiap slot memakai
`aria-describedby` menunjuk nama pemiliknya.

**Sumber.** [AI] baris 627, [AI] baris 641 sampai 643, [VR] baris 203 sampai 204.

### 4.12 EK-12 Kanal tidak logging

**Pemicu.** Kanal absen karena sumur tidak logging, bukan karena sensor gagal ([AI] baris 966).

**Judul.** Tidak logging pada sumur ini

**Badan.** Kanal ini tidak aktif karena sumur tidak menjalankan logging, sehingga tidak ada nilai yang
hilang. Sebabnya ditulis terpisah dari kanal yang gagal, dan permintaan pemasangan kanal bisa diajukan
dengan alasan angka dan prioritas ([AI] baris 382 sampai 384).

**Aksi.** "Buka kartu pemasangan kanal", menampilkan alasan angka dan prioritas pemasangan.

**ARIA.** `role="note"` dengan `aria-describedby` menunjuk sebab dan nama kanal.

**Sumber.** [AI] baris 966, [AI] baris 382 sampai 384, [AI] baris 516.

### 4.13 Rekap pesan keadaan kosong

| Kode | Keadaan | Kode abstain terkait | Label aksi | ARIA |
|---|---|---|---|---|
| EK-01 | Jendela tenang | tidak ada | Buka antrean pantau | status, polite |
| EK-02 | Tanpa kepala berskor | AB-1 | Buka daftar kepala menunggu | note |
| EK-03 | Data sensor kurang | AB-2 | Buka kartu kesiapan kanal | note |
| EK-04 | Skor jendela belum diekspor | AB-3 | Buka pita ringkasan | note |
| EK-05 | Klaim lapis L3 | AB-4 | Buka alasan lapis | note |
| EK-06 | Kepala bisu | AB-5 | Buka riwayat kepala | note |
| EK-07 | Keyakinan rendah | tidak ada | Buka batas atas | note |
| EK-08 | Beban melebihi anggaran | tidak ada | Buka daftar tunda | status, polite, atomic |
| EK-09 | Log keputusan kosong | tidak ada | Catat keputusan pertama | status, polite |
| EK-10 | Angka belum boleh dikutip | tidak ada | Buka syarat pengutipan | note |
| EK-11 | Slot nilai lapisan B kosong | tidak ada | Minta akses data | group |
| EK-12 | Kanal tidak logging | tidak ada | Buka kartu pemasangan kanal | note |

Jumlah baris data tabel di atas: 12. Dua belas pesan ini menutup kelima kode abstain AB-1 sampai AB-5
dan ketujuh keadaan tampilan lain yang ditetapkan [AI] bagian 8.

---

## 5. Enam pesan galat

Pesan galat memakai aturan yang sama dengan keadaan kosong, ditambah satu syarat: galat menyebut item
yang salah dalam teks, bukan hanya menandainya dengan warna ([W331]).

### 5.1 EG-01 Data halaman gagal dimuat

**Judul.** Data halaman belum termuat

**Badan.** Permintaan data tidak selesai pada percobaan pertama. Halaman menampilkan angka terakhir yang
tersimpan beserta waktunya, sehingga pembaca tetap punya angka yang jujur, bukan halaman kosong.

**Aksi.** "Coba muat ulang", ditambah tautan "Buka bukti angka" ke PG-07.

**ARIA.** `role="alert"` dengan `aria-live="assertive"`.

**Sumber aturan.** [W413], [W331], [AI] baris 102 sampai 106.

### 5.2 EG-02 Rujukan baris tidak cocok

**Judul.** Rujukan tidak cocok dengan isi baris

**Badan.** Pengunci rujukan membaca baris yang disebut, dan baris itu tidak berisi angka yang dimaksud.
Angka ditahan sampai rujukannya diperbaiki, dan pasangan berkas serta barisnya ditampilkan supaya bisa
diperiksa pembaca ([AI] baris 559 sampai 560).

**Aksi.** "Buka baris sumber", membuka baris berkas yang dirujuk.

**ARIA.** `role="alert"` dengan `aria-live="assertive"`.

**Sumber aturan.** [W331], [AI] baris 559 sampai 560.

### 5.3 EG-03 Keputusan gagal disimpan

**Judul.** Keputusan belum tersimpan

**Badan.** Baris yang ditutup belum masuk log keputusan. Umur baris tetap berjalan sampai penyimpanan
berhasil, sehingga tidak ada keputusan yang hilang tanpa jejak.

**Aksi.** "Simpan ulang", dan isian formulir tetap terisi.

**ARIA.** `role="alert"` dengan `aria-live="assertive"`, dan fokus tetap pada tombol simpan.

**Sumber aturan.** [W413], [AI] baris 460.

### 5.4 EG-04 Tanggal potong data melewati ambang

**Judul.** Tanggal potong data melewati ambang kesegaran

**Badan.** Angka pada halaman ini berasal dari potongan data yang lebih lama dari ambang kesegaran yang
ditetapkan pemilik produk. Ambang itu parameter desain, dan nilainya belum diukur pada operator. Angka
tetap ditampilkan dengan penanda tanggalnya, karena angka lama yang berlabel lebih berguna daripada
angka tanpa tanggal ([AI] baris 188).

**Aksi.** "Buka kalender sumber angka", menampilkan kapan setiap angka terakhir diuji.

**ARIA.** `role="status"` dengan `aria-live="polite"`.

**Sumber aturan.** [W413], [AI] baris 188, [AI] baris 464.

### 5.5 EG-05 Akses data ditolak

**Judul.** Data ini perlu izin tambahan

**Badan.** Akun ini belum punya izin untuk berkas yang diminta. Halaman menampilkan nama berkas, nama
pemilik data, dan jenis izin yang dibutuhkan, sehingga permintaan bisa diajukan langsung ke orang yang
tepat ([AI] baris 614).

**Aksi.** "Ajukan permintaan akses", membuka kartu INS-05 dengan kolom pemilik dan tanda tangan.

**ARIA.** `role="alert"` dengan `aria-live="assertive"`.

**Sumber aturan.** [W331], [AI] baris 614.

### 5.6 EG-06 Permintaan data belum lengkap

**Judul.** Dua kolom permintaan belum terisi

**Badan.** Permintaan data butuh pemilik dan tanda tangan sebelum bisa dikirim. Kedua kolom itu disebut
namanya, dan isian lain yang sudah benar tidak dihapus.

**Aksi.** "Lengkapi permintaan", memindahkan fokus ke kolom pertama yang kosong.

**ARIA.** `role="alert"`, `aria-live="assertive"`, dan setiap kolom memakai `aria-invalid="true"` dengan
`aria-describedby` menunjuk kalimat galatnya.

**Sumber aturan.** [W331], [W111], [AI] baris 517.

### 5.7 Rekap pesan galat

| Kode | Galat | Label aksi | ARIA | Sumber aturan |
|---|---|---|---|---|
| EG-01 | Data halaman gagal dimuat | Coba muat ulang | alert, assertive | [W413], [W331] |
| EG-02 | Rujukan baris tidak cocok | Buka baris sumber | alert, assertive | [W331] |
| EG-03 | Keputusan gagal disimpan | Simpan ulang | alert, assertive | [W413] |
| EG-04 | Tanggal potong data melewati ambang | Buka kalender sumber angka | status, polite | [W413] |
| EG-05 | Akses data ditolak | Ajukan permintaan akses | alert, assertive | [W331] |
| EG-06 | Permintaan data belum lengkap | Lengkapi permintaan | alert, assertive | [W331], [W111] |

Jumlah baris data tabel di atas: 6.

---

## 6. Aturan aksesibilitas

### 6.1 Kontras

| Elemen di situs | Minimum | Dasar | Sumber |
|---|---|---|---|
| Teks isi, teks tabel, teks lencana | 4,5:1 | SC 1.4.3 level AA | [W143] |
| Judul halaman 24 px ke atas, atau 18,5 px tebal | 3:1 | SC 1.4.3, definisi teks besar | [W143], [W143b] |
| Batas kartu, garis batang keyakinan, ikon status | 3:1 terhadap warna bersebelahan | SC 1.4.11 level AA | [W1411] |
| Cincin fokus | 3:1 terhadap latar bersebelahan | SC 1.4.11 dipakai bersama SC 2.4.7 | [W1411], [W247] |

Dua aturan pengukuran yang mengikat tim bangun. Pertama, nilai kontras tidak dibulatkan: 4,499:1 tidak
lulus ambang 4,5:1, dan 2,999:1 tidak lulus ambang 3:1 ([W143], [W1411]). Kedua, ukuran teks besar
dihitung dari px, bukan dari pt: 18 pt setara 24 px dan 14 pt setara 18,5 px ([W143b]).

Larangan yang sudah berlaku di proyek dan sejalan dengan aturan ini: warna tidak pernah menjadi satu
satunya pembeda status, dan warna merah tanpa label manusia-peninjau dilarang ([AI] baris 1004 sampai
1006, [DSS2] baris 585).

### 6.2 Ukuran sentuh

| Target | Minimum | Dasar | Sumber |
|---|---|---|---|
| Semua target yang bisa ditekan | 24 x 24 piksel CSS | SC 2.5.8 level AA | [W258] |
| Label aksi utama, tombol tutup baris, tombol catat keputusan | 44 x 44 piksel CSS | SC 2.5.5 level AAA, dipakai sebagai standar internal | [W255] |
| Target di dalam kalimat | dikecualikan dari ukuran, tetapi tetap wajib punya cincin fokus | SC 2.5.5 butir pengecualian | [W255] |

Alasan memakai 44 piksel untuk aksi utama: pengguna lapangan memakai sarung tangan, dan SC 2.5.5
menyebut tremor tangan serta ketidakmampuan motorik halus sebagai sasaran ([W255]). Ukuran 24 piksel
tetap dipakai sebagai lantai mutlak untuk target lain, dan ukuran itu diukur sebagai persegi 24 x 24
piksel yang seluruhnya berada di dalam target ([W258]).

### 6.3 ARIA dan peran

| Komponen | Peran | Label | Pengumuman | Sumber |
|---|---|---|---|---|
| Banner tingkat pantauan | `status` | `aria-labelledby` menunjuk nama tingkat | `aria-live="polite"`, `aria-atomic="true"` | [W413] |
| Kartu keyakinan | `group` | `aria-labelledby` menunjuk judul kartu | tidak ada | [W111] |
| Batang keyakinan | `img` | `aria-label` memuat persen, pita, dan batas kelas | tidak ada | [W111] |
| Tabel antrean | `table` | `caption` menyebut halaman dan tanggal potong | tidak ada | [W111] |
| Lencana abstain | `note` | `aria-describedby` menunjuk kode AB dan alasannya | tidak ada | [W413] |
| Pesan galat | `alert` | `aria-describedby` menunjuk item yang salah | `aria-live="assertive"` | [W413], [W331] |
| Menu navigasi utama | `nav` | `aria-label` bernilai "navigasi utama", `aria-current="page"` pada butir aktif | tidak ada | [W111] |
| Kolom formulir galat | `textbox` atau `combobox` | `aria-invalid="true"`, `aria-describedby` menunjuk kalimat galat | tidak ada | [W331] |

Aturan tambahan: pesan status diumumkan tanpa memindahkan fokus, dan itu memang syarat kriteria
([W413]). Fokus hanya dipindahkan pada dua keadaan, yaitu galat formulir EG-06 dan pembukaan kartu
keyakinan dari tabel.

### 6.4 Fokus

| Aturan | Ukuran atau perilaku | Dasar | Sumber |
|---|---|---|---|
| Cincin fokus selalu terlihat | ketebalan minimal 2 px sebagai standar internal proyek, kontras 3:1 | SC 2.4.7 untuk keberadaan indikator, SC 1.4.11 untuk kontras | [W247], [W1411] |
| Cincin fokus tidak dibatasi waktu | tetap terlihat selama elemen berfokus | SC 2.4.7 | [W247] |
| Fokus tidak tertutup kaki halaman tetap | minimal sebagian elemen berfokus tetap terlihat | SC 2.4.11 | [W2411] |
| Urutan fokus mengikuti urutan baca | banner, tiga kartu, antrean, aksi, kaki halaman | SC 2.4.7 dan urutan blok [AI] baris 180 sampai 188 | [W247] |
| Tautan lewati ke konten utama | elemen pertama pada urutan tab | SC 2.4.7 | [W247] |

Larangan: `outline: none` tanpa pengganti, dan cincin fokus yang hanya mengandalkan warna tanpa
ketebalan. Dua larangan ini dipakai karena fokus termasuk informasi non teks yang wajib 3:1
([W1411]).

### 6.5 Teks alternatif

| Isi non teks | Teks alternatif yang wajib | Sumber |
|---|---|---|
| Batang keyakinan pada kartu | "hyd K-i, keyakinan 61 persen, pita P4, batas kelas 0,61" | [W111], [AI] baris 889 sampai 891 |
| Kurva kalibrasi | "kurva kalibrasi hyd, jumlah bin tertulis di sumbu, status rancangan, garis diagonal acuan" | [W111], [AI] baris 240 |
| Diagram Pareto jam henti | "Pareto jam henti, terbesar equipment failure 2.739,667 jam dari 39.397,986 jam tercatat" | [W111], [VR] baris 203 sampai 204 |
| Lencana pita P1 sampai P5 | nama pita ditulis sebagai teks, bukan hanya warna | [W111], [AI] baris 1004 sampai 1006 |
| Pola garis miring untuk abstain | "tidak dinilai", beserta kode AB | [W111], [AI] baris 263 sampai 265 |
| Ikon status pada tabel | `aria-label` berisi nama status, misalnya "pantau" atau "tinjau" | [W111], [AI] baris 475 |
| Grafik tren | ringkasan satu kalimat berisi satuan, rentang waktu, dan arah perubahan | [W111], [VR] baris 212 sampai 218 |

Aturan tambahan: setiap angka pada teks alternatif memakai pembulatan yang sama dengan tampilan layar,
yaitu `round(100 x K_tampil)` untuk persen ([AI] baris 1011 sampai 1012).

### 6.6 Gerak, waktu, dan ukuran layar

| Aturan | Nilai | Dasar | Sumber |
|---|---|---|---|
| Animasi pembuka | maksimal 300 milidetik | keputusan desain proyek | [AI] baris 709 sampai 711 |
| Perbesaran teks | sampai 200 persen tanpa kehilangan isi | SC 1.4.4 level AA | [W144] |
| Lebar tanpa gulir dua dimensi | 320 piksel CSS | SC 1.4.10 level AA | [W1410] |
| Lebar uji internal | 375 piksel untuk ponsel, 1.280 piksel untuk desktop | syarat proyek | [AI] baris 764 sampai 766 |
| Perbesaran 400 persen | 1.280 piksel setara 320 piksel | SC 1.4.10 catatan 1 | [W1410] |

Tabel antrean mendapat pengecualian dua dimensi karena tabel termasuk isi yang butuh tata letak dua
dimensi ([W1410] catatan 2). Pengecualian itu tidak berlaku untuk sel di dalam tabel: setiap sel tetap
wajib memenuhi reflow ([W1410]).

---

## 7. Daftar periksa aksesibilitas yang bisa diuji

Setiap baris punya langkah, alat, dan syarat lulus. Pemeriksa lain bisa menjalankan seluruh daftar ini
tanpa membuka sesi penyusun dokumen. Alat yang disebut adalah alat yang lazim dipakai dan tidak
memerlukan lisensi berbayar.

| No | Uji | Alat | Langkah | Lulus bila |
|---:|---|---|---|---|
| 1 | Kontras teks isi | axe DevTools atau kalkulator kontras | jalankan pemindai pada sepuluh halaman, saring pelanggaran `color-contrast` | nol pelanggaran, dan setiap pasangan teks dengan latar minimal 4,5:1 |
| 2 | Kontras teks besar | kalkulator kontras | ukur setiap judul halaman dan subjudul | setiap pasangan minimal 3:1, tanpa pembulatan nilai |
| 3 | Kontras non teks | kalkulator kontras | ukur batas kartu, garis batang keyakinan, dan ikon status | setiap pasangan minimal 3:1 terhadap warna bersebelahan |
| 4 | Cincin fokus terlihat | peramban, tombol Tab | tekan Tab dari elemen pertama sampai elemen terakhir pada setiap halaman | setiap elemen berfokus menampilkan cincin minimal 2 px dengan kontras 3:1 |
| 5 | Fokus tidak tertutup | peramban, lebar 375 piksel | Tab sampai elemen terakhir sebelum kaki halaman | elemen berfokus tetap terlihat sebagian, tidak tertutup kaki halaman tetap |
| 6 | Ukuran target | DevTools, panel kotak elemen | ukur setiap tombol, tautan, dan ikon yang bisa ditekan | setiap target minimal 24 x 24 px, dan label aksi utama minimal 44 x 44 px |
| 7 | Reflow 320 piksel | peramban, lebar 320 piksel | buka sepuluh halaman, gulir vertikal saja | tidak ada gulir horizontal, kecuali tabel antrean yang dikecualikan |
| 8 | Perbesaran teks 200 persen | peramban, zoom 200 persen | buka sepuluh halaman | tidak ada teks terpotong dan tidak ada tombol hilang |
| 9 | Skala abu | peramban, filter grayscale | buka PG-01 dan PG-02 pada skala abu | pita P3 dan P4 tetap terbedakan karena pola atau teks, bukan hanya warna |
| 10 | Status bertekstur | pemeriksaan visual | periksa setiap lencana pita, umur, dan lencana konflik | setiap status punya teks, bukan hanya warna |
| 11 | Banner diumumkan tanpa fokus | pembaca layar, NVDA atau VoiceOver | muat PG-00 dan tunggu pembaruan | banner dibacakan tanpa fokus berpindah |
| 12 | Pesan galat diumumkan | pembaca layar | picu EG-02 dan EG-06 | pesan dibacakan, dan item yang salah disebut namanya |
| 13 | Tabel punya caption dan kepala kolom | axe DevTools | jalankan pemindai pada PG-02 dan PG-07 | nol pelanggaran `td-headers-attr` dan `table-fake-caption` |
| 14 | Batang keyakinan punya teks alternatif | pembaca layar | fokuskan setiap batang pada PG-00 dan PG-01 | setiap batang membacakan persen, pita, dan batas kelas |
| 15 | Urutan tab masuk akal | peramban, tombol Tab | Tab dari awal sampai akhir pada PG-00 | urutan mengikuti banner, kartu fokus, beban, antrean, lalu kaki halaman |
| 16 | Tautan lewati berfungsi | peramban, tombol Tab | tekan Tab satu kali pada setiap halaman, lalu Enter | fokus berpindah ke konten utama |
| 17 | Pita P1 dan P2 tanpa elemen aksi | peramban, uji klik | buka kartu pita P1 dan P2 pada PG-01 | tidak ada elemen yang bisa memicu tindakan |
| 18 | Urutan kartu sesuai aturan | pemeriksaan visual dan pembaca layar | buka PG-01 | kartu P4 di atas P2, dan semua kartu abstain di bawah kartu berpita |
| 19 | Kuis bisa dikerjakan tanpa tetikus | peramban, tombol Tab dan panah | kerjakan sepuluh pertanyaan pada PG-09 | seluruh pertanyaan bisa dijawab dan dinilai tanpa tetikus |
| 20 | Nada naskah bebas istilah terlarang | pencarian teks pada halaman | cari tiga istilah terlarang dari bagian 2.2 pada sepuluh halaman | nol temuan pada teks yang tampil |

Jumlah baris data tabel di atas: 20.

Tiga uji pada daftar ini berasal langsung dari syarat proyek, bukan dari WCAG: uji 9 skala abu, uji 17
klik pada pita rendah, dan uji 18 urutan kartu ([AI] baris 1007 sampai 1014). Sisanya berasal dari
kriteria WCAG 2.2 yang sudah dibuka di bagian 1.2.

---

## 8. Lima field wajib per fitur yang membawa naskah

Kerangka butir 5 meminta lima field untuk setiap fitur: pengguna, momen pakai, masukan, keluaran, dan
status bukti. Tabel ini memuat kelima field untuk dua puluh tiga fitur yang membawa label aksi atau
pesan keadaan kosong di dokumen ini. Fitur lain tetap memuat kelima field itu di blok fiturnya masing
masing pada [KAT], dan jumlahnya diperiksa dengan `grep` di bagian 9.5.

| Kode fitur | Pengguna | Momen pakai | Masukan | Keluaran | Status bukti | Halaman |
|---|---|---|---|---|---|---|
| KEP-01 | insinyur pengeboran, supervisor, dosen penguji | sebelum mempercayai badge kelas, dua kali per shift | tabel komposisi per kelas dan peta tier | sebelas kartu vonis dengan tier dan syarat menggantung | siap sekarang | PG-01 |
| KEP-02 | insinyur pengeboran, supervisor | saat menimbang tindakan | keluaran model per jendela: skor, ambang, riwayat | kartu keyakinan dengan pita, batang, dan batas kelas | siap sebagian | PG-00, PG-01, PG-02 |
| KEP-03 | operator, supervisor | saat membaca beban tinjauan | jumlah alarm per 24 jam dengan satuannya | badge beban dengan satuan tertulis | siap sekarang | PG-00, PG-01 |
| KEP-04 | penilai model, auditor internal | saat memutuskan skor boleh dibaca sebagai frekuensi | pasangan skor prediksi dan label nyata per fold | kurva kalibrasi per engine dengan jumlah bin | rancangan | PG-01 |
| KEP-05 | auditor, penulis laporan | setiap mengutip angka ke dokumen luar | status provenance tiap angka | lencana tiga warna dan gerbang pengutipan | siap sekarang | PG-01, PG-07, PG-08 |
| KEP-06 | dosen penguji, PM | saat dua pembacaan berbeda | satu klaim dengan dua pembacaan | papan dua pembacaan dan selisihnya | siap sekarang | PG-01, PG-09 |
| KEP-07 | auditor internal | sekali per bulan, dan saat satu angka dipertanyakan | pasangan berkas dan baris setiap angka | pengunci rujukan dan uji mutasi | siap sekarang | PG-06, PG-07 |
| KEP-08 | penilai model, supervisor | saat dua kepala berbeda putusan | putusan per kepala pada jendela sama | panel ketidaksepakatan dan daftar pasangan kembar | siap sebagian | PG-01 |
| KEP-09 | insinyur, peneliti | sebelum memakai label keausan bit | label keausan bit dan status mekanikanya | banner transparansi satu kalimat tetap | siap sekarang | PG-01, PG-08 |
| KEP-10 | manajer pemeliharaan, perencana | saat menyusun prioritas perbaikan | jam henti per kategori dan tarif biaya | Pareto jam henti dan lima slot nilai | siap sebagian | PG-02, PG-08 |
| MNT-01 | insinyur shift malam, toolpusher | awal shift dan setiap dua jam | daftar item tinjauan, stempel waktu, status | tabel antrean terurut umur dengan kolom aksi | siap sekarang | PG-00, PG-02 |
| MNT-02 | perencana tenaga kerja | sekali per minggu | jumlah pemeriksaan dan biaya waktu per pemeriksaan | kalkulator pemeriksaan yang dihemat | siap sekarang | PG-02 |
| MNT-05 | perencana tenaga kerja, supervisor | saat menaksir beban shift | lambda per klaim dan hasil simulasi | empat angka beban: lambda, p50, p95, anggaran | siap sebagian | PG-02 |
| DAT-01 | engineer PdM | sebelum menilai satu event | fraksi kanal hadir pada jendela pra-event | kartu kelengkapan dengan vonis layak | siap sekarang | PG-03 |
| DAT-02 | engineer PdM, koordinator data | saat satu kanal tidak menyala | daftar kanal dan status logging sumur | daftar kanal tidak logging beserta sebabnya | siap sekarang | PG-03 |
| DAT-05 | koordinator data | saat merencanakan perluasan cakupan | daftar berkas per sumur dan status unduh | matriks ketersediaan berkas per sumur | siap sekarang | PG-03, PG-08 |
| DAT-08 | engineer PdM, koordinator data | sebelum panel dinyalakan | kanal siap, tipis, dan absen per sumur | kartu kesiapan kanal per sumur | siap sekarang | PG-03, PG-08 |
| CMP-01 | peneliti, dosen penguji | saat memeriksa klaim keunggulan | nilai metrik per fold untuk model dan baseline | balapan model lawan persistence per fold | siap sekarang | PG-04 |
| CMP-07 | PM, peneliti | saat memilih komposisi head untuk satu kelas | tiga komposisi head hyd dan hasil tiap komposisi | panel kesetaraan dengan bentuk pertukaran presisi dan recall | siap sebagian | PG-04 |
| LIN-01 | supervisor | setiap kali menutup peringatan | waktu, aktor, keputusan, akibat | log keputusan dengan penghitung terbuka | siap sebagian | PG-05 |
| LIN-02 | auditor, dosen penguji | saat memeriksa urutan dokumen vonis | urutan dokumen vonis, gerbang, dan perubahan target | garis waktu gerbang | siap sekarang | PG-05 |
| INS-02 | auditor internal, penulis laporan | saat menguji ulang satu angka | satu angka beserta rujukannya | panduan skrip dengan perintah dan keluaran harapan | siap sekarang | PG-06, PG-07 |
| INS-05 | koordinator data | saat menyusun permintaan data | tiga ketiadaan terbukti dan nama pemilik | kartu permintaan bertanda tangan | siap sebagian | PG-03, PG-08 |

Jumlah baris data tabel di atas: 23.

Dua puluh tiga fitur di atas menutup seluruh label aksi di bagian 3 dan seluruh pesan keadaan kosong di
bagian 4. Status bukti disalin dari [KAT] bagian 11, yang mencatat 32 siap sekarang, 15 siap sebagian,
dan 1 rancangan ([AI] baris 628 sampai 630).

---

## 9. Keluaran perintah yang dijalankan

Bagian ini menempelkan keluaran apa adanya pada 2026-11-01, sesuai kerangka butir 3. Perintah
dijalankan dari `/mnt/d/Capstone 1(v2)`.

### 9.1 Ukuran berkas masukan

```
$ stat -c '%s %n' planning/07_ARSITEKTUR_INFORMASI.md planning/01_KATALOG_FITUR.md \
      planning/02_RISET_VISUALISASI.md planning/04_ANTREAN_TINJAUAN.md
87727 planning/07_ARSITEKTUR_INFORMASI.md
166662 planning/01_KATALOG_FITUR.md
32141 planning/02_RISET_VISUALISASI.md
95168 planning/04_ANTREAN_TINJAUAN.md
```

Jumlah keempat angka di atas 381.698 byte, cocok dengan tabel bagian 1.1.

### 9.2 Jumlah baris berkas masukan

```
$ wc -l planning/07_ARSITEKTUR_INFORMASI.md planning/01_KATALOG_FITUR.md \
       planning/02_RISET_VISUALISASI.md planning/04_ANTREAN_TINJAUAN.md
  1328 planning/07_ARSITEKTUR_INFORMASI.md
  2780 planning/01_KATALOG_FITUR.md
   335 planning/02_RISET_VISUALISASI.md
  1428 planning/04_ANTREAN_TINJAUAN.md
  5871 total
```

### 9.3 Sumber standar yang dibuka

Dua belas kriteria WCAG 2.2 dibuka dan dibaca pada sesi ini. Kalimat kriteria yang dikutip di bagian 1.2
diambil dari halaman `Understanding` masing masing kriteria, dan alamatnya ada di bagian 11.

### 9.4 Keadaan antrean pada berkas hulu

```
$ sed -n '514,515p' planning/04_ANTREAN_TINJAUAN.md
**Pemicu.** Tidak ada baris P3 atau P4 pada shift itu. Angka pendukungnya nyata dan hari ini benar
untuk satu klaim: ssi `rule_display` punya `n_aktif` 0 dari 5.455 jendela ([J] baris 232), FAR 0,0
$ sed -n '528,531p' planning/04_ANTREAN_TINJAUAN.md
tidak dinilai, kanal absen", bukan "aman". Ini pola
Dynamic Island: yang hilang menjadi label, bukan angka nol.
```

### 9.5 Lima field wajib pada katalog

```
$ for k in 'Pengguna dan momen pakai' 'Masukan' 'Keluaran' 'Status bukti' 'Cara menguji'; do \
    printf '%-28s %s\n' "$k" "$(grep -c "^\*\*$k\.\*\*" planning/01_KATALOG_FITUR.md)"; done
Pengguna dan momen pakai     48
Masukan                      48
Keluaran                     48
Status bukti                 48
Cara menguji                 48
```

Keluaran ini menopang klaim pada kerangka butir 5 dan pada bagian 8: keempat field wajib ada pada
keempat puluh delapan fitur, bukan hanya pada dua puluh tiga fitur yang ditabelkan di sini.

### 9.6 Label aksi pada berkas arsitektur

```
$ grep -c 'Aksi utama' planning/07_ARSITEKTUR_INFORMASI.md
10
$ grep -c 'Aksi kedua' planning/07_ARSITEKTUR_INFORMASI.md
8
```

Sepuluh butir "Aksi utama" berarti setiap halaman punya satu blok aksi, dan delapan butir "Aksi kedua"
berarti delapan halaman punya aksi tambahan. Dua halaman tanpa aksi kedua adalah PG-01 dan PG-09:
blok aksi PG-01 berakhir di baris 248 dan blok aksi PG-09 berakhir di baris 665 ([AI] baris 246 sampai
249 dan 664 sampai 665).

### 9.7 Pemeriksaan berkas ini sendiri

Diukur sebelum blok ini disunting, karena menempelkan keluaran mengubah ukuran berkas.

```
$ stat -c '%s byte' planning/09_NASKAH_AKSESIBILITAS.md
67825 byte
$ wc -l < planning/09_NASKAH_AKSESIBILITAS.md
1168
$ grep -c '^|' planning/09_NASKAH_AKSESIBILITAS.md
228
$ grep -cP '\x{2014}' planning/09_NASKAH_AKSESIBILITAS.md
0
$ grep -cP '\x{2013}' planning/09_NASKAH_AKSESIBILITAS.md
0
$ grep -c '^## ' planning/09_NASKAH_AKSESIBILITAS.md
14
$ ls planning/*.py planning/*.html planning/*.json planning/*.csv 2>/dev/null | wc -l
0
```

Empat belas bagian utama sesuai dengan daftar berikut: 0 kerangka wajib, 1 berkas masukan, 2 nada suara,
3 naskah sepuluh halaman, 4 pesan keadaan kosong, 5 pesan galat, 6 aturan aksesibilitas, 7 daftar
periksa, 8 lima field per fitur, 9 keluaran perintah, 10 syarat naik status, 11 rujukan standar,
12 yang belum diverifikasi, dan 13 penutup.

Tiga angka pertama pada blok ini berubah bila berkas ini disunting lagi. Angka final sesudah seluruh
suntingan berhenti dilaporkan di komentar penutup kartu, dan pembaca yang menemukan selisih memakai
keluaran `stat` dan `wc` pada pembacaan pembaca itu.

---

## 10. Syarat agar naskah ini naik status

Tidak ada bagian yang ditutup. Setiap baris menyebut apa yang dibutuhkan, siapa pemiliknya, dan uji
yang menandai kenaikan status. Pola ini sama dengan pola [AI] bagian 11.

| Bagian | Status hari ini | Yang dibutuhkan | Pemilik | Uji naik status |
|---|---|---|---|---|
| Naskah sepuluh halaman | tertulis, belum dirender | render pada peramban, lalu ukur panjang baris dan tinggi blok | tim website | setiap halaman muat tanpa gulir horizontal pada 375 piksel |
| Dua belas pesan keadaan kosong | tertulis dengan pemicu angka | sambungkan setiap pesan ke pemicu di kode, bukan ke keadaan tiruan | tim website | setiap pesan muncul dari data nyata, bukan dari tombol uji |
| Enam pesan galat | tertulis dengan label aksi | satu uji jalan yang sengaja memicu setiap galat | tim website | keenam galat terpicu dan terbaca pembaca layar |
| Aturan kontras | ambang tertulis | palet warna final dengan nilai kontras tercatat per pasangan | desainer | nol pelanggaran `color-contrast` pada axe |
| Ukuran sentuh | ambang tertulis | ukuran tombol final pada lembar gaya | desainer | setiap target terukur minimal 24 px, aksi utama 44 px |
| ARIA dan peran | peran tertulis per komponen | pemasangan atribut pada komponen | tim website | pemindai aksesibilitas nol pelanggaran tingkat kritis |
| Daftar periksa dua puluh butir | bisa dijalankan | satu putaran penuh pada sepuluh halaman | auditor internal | dua puluh butir lulus, dengan tangkapan layar per butir |
| Istilah terlarang | tiga istilah terkunci | pemeriksa teks otomatis pada pipeline | tim website | pemeriksa gagal bila satu istilah muncul |

Jumlah baris data tabel di atas: 8.

---

## 11. Rujukan standar

1. W143. Understanding SC 1.4.3 Contrast (Minimum), W3C. https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
2. W143b. Definisi teks besar dan konversi pt ke px, pada halaman yang sama dengan W143.
3. W1411. Understanding SC 1.4.11 Non-text Contrast, W3C. https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
4. W258. Understanding SC 2.5.8 Target Size (Minimum), W3C. https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
5. W255. Understanding SC 2.5.5 Target Size (Enhanced), W3C. https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html
6. W1410. Understanding SC 1.4.10 Reflow, W3C. https://www.w3.org/WAI/WCAG22/Understanding/reflow.html
7. W144. Understanding SC 1.4.4 Resize Text, W3C. https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html
8. W413. Understanding SC 4.1.3 Status Messages, W3C. https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html
9. W247. Understanding SC 2.4.7 Focus Visible, W3C. https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html
10. W2411. Understanding SC 2.4.11 Focus Not Obscured (Minimum), W3C. https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html
11. W331. Understanding SC 3.3.1 Error Identification, W3C. https://www.w3.org/WAI/WCAG22/Understanding/error-identification.html
12. W111. Understanding SC 1.1.1 Non-text Content, W3C. https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html

---

## 12. Yang belum diverifikasi di dokumen ini

Bagian ini daftar periksa untuk pekerjaan berikutnya. Setiap butir menyebut apa yang sudah diperiksa
dan apa yang belum.

1. Tidak ada halaman yang dirender. Seluruh naskah di bagian 3 adalah teks, dan uji 375 piksel, uji
   skala abu, serta uji perbesaran 200 persen belum dijalankan pada peramban.
2. Palet warna belum ada. Ambang kontras di bagian 6.1 sudah benar menurut kriteria, tetapi nilai
   kontras tiap pasangan warna baru bisa diukur setelah palet final ditetapkan.
3. Ukuran tombol belum ada. Ambang 24 dan 44 piksel di bagian 6.2 adalah syarat, bukan hasil ukur.
4. Atribut ARIA di bagian 6.3 adalah rencana pemasangan. Belum ada satu komponen pun yang memuat
   atribut itu, sehingga pembacaan pembaca layar belum diuji.
5. Dua belas pesan keadaan kosong di bagian 4 memakai pemicu angka yang sudah terukur, tetapi
   pemetaan pemicu ke kode belum ditulis. Daftar periksa bagian 7 belum punya butir khusus untuk pesan
   keadaan kosong, sehingga butir terdekat adalah uji 11 tentang pengumuman status, dan butir khusus
   untuk dua belas pesan itu perlu ditambahkan sebelum dijalankan.
6. Angka pada pesan EK-03, EK-08, dan EK-11 dikutip dari berkas hulu, tidak dihitung ulang dari parquet
   pada sesi ini.
7. Dua belas kriteria WCAG dibuka pada sesi ini, tetapi teknik pemenuhannya pada tingkat kode tidak
   dibuka, sehingga contoh atribut di bagian 6.3 adalah usulan, bukan kutipan teknik resmi.
8. Tiga uji pada daftar periksa bagian 7 berasal dari syarat proyek, bukan dari WCAG, dan ketiganya
   belum pernah dijalankan pada satu halaman pun.
9. Naskah bagian 3 belum diuji pada pembaca lapangan. Nada dan panjang kalimat adalah target desain,
   bukan hasil pengukuran pada operator.
10. Istilah terlarang di bagian 2.2 diperiksa pada naskah dokumen ini, bukan pada teks yang tampil di
    layar, karena layarnya belum dibangun.
11. Ketebalan cincin fokus 2 px pada bagian 6.4 adalah standar internal proyek. Kriteria WCAG yang
    dibuka pada sesi ini mengatur keberadaan indikator fokus dan kontrasnya, bukan ketebalannya.
12. Ambang kesegaran data pada pesan EG-04 adalah parameter desain yang nilainya ditetapkan pemilik
    produk. Angka harinya belum ditetapkan pada sesi ini, sehingga judul pesan itu menyebut ambang
    tanpa angka.
13. Jumlah bin pada kurva kalibrasi belum tertulis di berkas hulu yang dibuka. Teks alternatif di
    bagian 6.5 karena itu menyebut jumlah bin sebagai isi yang harus tertulis di sumbu, tanpa
    menyebut angkanya.

---

## 13. Penutup yang bisa diperiksa

Dokumen ini menyerahkan naskah sepuluh halaman dengan tiga puluh paragraf dan tiga puluh label aksi,
dua belas pesan keadaan kosong, enam pesan galat, aturan aksesibilitas pada enam bidang, daftar periksa
dua puluh butir, dan dua puluh tiga fitur dengan lima field wajib. Empat hal bisa diperiksa orang lain
tanpa membuka sesi ini:

1. Setiap angka pada bagian 3, 4, dan 5 punya pasangan berkas dan baris yang bisa dibuka dengan
   `sed -n '<baris>p' <berkas>`.
2. Setiap ambang aksesibilitas pada bagian 6 dan 7 punya nomor kriteria WCAG yang alamatnya ada di
   bagian 11.
3. Setiap pesan keadaan kosong punya pemicu angka, alasan, pemilik, satu label aksi, dan pengaturan
   ARIA, sehingga bisa diuji satu per satu.
4. Berkas ini lolos pemeriksaan format pada bagian 9.7: nol tanda pisah panjang, nol tanda pisah
   sedang, dan nol berkas non markdown di `planning/`.

Bila satu angka hulu berubah, naskah halaman yang mengutipnya wajib diperbarui lewat pengunci rujukan
KEP-07, dan perubahan itu tercatat di PG-05 sebagai satu baris log keputusan ([AI] baris 1327 sampai
1328).
