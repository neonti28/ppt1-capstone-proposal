# 11 PRIORITAS BUILD: tiga gelombang, vonis paket, dan serah terima

Kartu: `t_7d5aad27` (MANAJER). Board: `fitur-v9-swarm`. Tanggal: 2026-11-01 (WIB).
Workspace: `/mnt/d/Capstone 1(v2)`. Keluaran: berkas ini saja, di folder `planning/`.

Dokumen ini menjawab satu pertanyaan yang tidak dijawab katalog: dari 48 fitur yang sudah
dikontrak, mana yang dibangun lebih dulu, apa yang ditunggu sebelum satu fitur boleh dibangun,
dan apa syarat menyerahkan paket ini ke tim website. Isinya keputusan urutan, bukan laporan riset
baru. Tidak ada model yang dijalankan, tidak ada angka sumber yang diubah, dan tidak ada berkas
selain markdown yang dibuat.

---

## 0. Kerangka wajib (dipakai apa adanya, tidak diubah)

1. Alarm otomatis BUKAN tujuan. ML dipakai sebagai sistem pendukung keputusan dengan skor
   keyakinan, bukan pemutus. Konsekuensi pada dokumen ini: tidak ada satu gelombang pun yang
   diurutkan berdasarkan kedekatan ke alarm otomatis, dan slot alarm otomatis tetap 0 pada seluruh
   fitur (`scratch/v9_i1/v9_i1_RESULTS.json` baris 1414; `planning/01_KATALOG_FITUR.md` baris 204).
2. Setiap angka punya sumber: berkas dan baris, atau baris ledger `docs/RND_PROVENANCE_LEDGER.md`.
   Setiap angka di dokumen ini membawa kurung siku berisi berkas dan nomor baris.
3. Tidak ada klaim berjalan tanpa bukti. Perintah yang dijalankan untuk memeriksa angka dan untuk
   memeriksa berkas ini sendiri ditempel di bagian 11.
4. Kekurangan data dikemas menjadi fitur berguna, bukan keluhan. Tiga gelombang di bawah memakai
   pola Dynamic Island sebagai alat urut: fitur yang datanya belum ada tetap punya tempat, dan
   tempatnya diberi label alasan, bukan dikosongkan.
5. Setiap fitur punya lima field wajib: pengguna, momen pakai, masukan, keluaran, status bukti.
   Kelima field itu ada pada setiap baris tabel fitur di bagian 3, 4, dan 5, dan bentuk gabungan
   `Pengguna dan momen pakai` mengikuti `planning/01_KATALOG_FITUR.md` baris 231.
6. Tidak ada kalimat penutup yang menutup jalan. Bila sesuatu belum tersedia, yang ditulis adalah
   syaratnya, dan syaratnya ada di bagian 5.3 dan bagian 8.
7. Keluaran hanya markdown di `planning/`. Tidak ada .py, .html, .json, atau .csv sebagai
   deliverable.
8. Tidak memakai tanda pisah panjang. Rentang angka ditulis dengan tanda hubung biasa.

---

## 1. Berkas masukan yang dibuka dan ukuran byte

Ukuran diambil dengan `stat -c '%s'` pada 2026-11-01, keluarannya ditempel di bagian 11 butir A.
Lima berkas masukan wajib, ditambah satu berkas arsip yang dirujuk gelombang 3.

| Kode | Berkas | Byte | Baris | Yang diambil |
|---|---|---:|---:|---|
| [KAT] | `planning/01_KATALOG_FITUR.md` | 166.662 | 2.780 | 48 fitur, lima field wajib, status bukti, rekap bagian 11 |
| [AI] | `planning/07_ARSITEKTUR_INFORMASI.md` | 87.727 | 1.328 | 10 halaman, 7 butir menu, 12 keadaan tampilan, 9 hal yang sengaja tidak dibuat, 10 syarat naik status |
| [KD] | `planning/08_KONTRAK_DATA.md` | 85.929 | 1.365 | 21 fitur prioritas, amplop 11 field, 3 keadaan data, 6 fitur wajib skor keyakinan |
| [AUD] | `planning/10_AUDIT.md` | 21.295 | 390 | vonis PERLU PERBAIKAN, 6 cacat bernomor, 29 dari 30 angka cocok |
| [S6] | `docs/RND_S6_PM_WAVE2.md` | 40.271 | 437 | peta tier, komposisi terpilih per kelas, 0 slot alarm otomatis, lapisan B tidak terukur |
| [NPZ] | `data/predictive/features_timeseries.npz` | 458.129 | biner | isi arsip yang belum dibaca nilainya |

Total lima berkas markdown masukan: 401.884 byte pada 6.300 baris. Angka total itu penjumlahan
lima baris di atas, dan pembaca bisa mengulangnya dari keluaran `stat` di bagian 11 butir A.

Catatan kejujuran: [KAT] setebal 166.662 byte tidak dibaca seluruhnya. Yang dibaca adalah bagian
1 sampai 4 penuh, tabel ringkasan 48 fitur, tabel status di bagian 11, dan baris `Pengguna dan
momen pakai`, `Masukan`, `Keluaran`, `Status bukti` pada 48 blok fitur lewat pencarian baris.
Kalimat penjelas di dalam blok yang tidak berhubungan dengan urutan tidak diperiksa. Batas ini
diulang di bagian 10.

---

## 2. Cara membaca tiga gelombang

Tiga gelombang di kartu ini didefinisikan oleh **apa yang belum ada**, bukan oleh besar kecilnya
nilai sebuah fitur. Tiga aturan di bawah dipakai mesin, artinya setiap fitur masuk ke gelombang
pertama yang cocok, dan pembaca bisa mengulang penetapannya tanpa menebak.

**Aturan G1, data ada.** Seluruh masukan fitur sudah ada sebagai berkas di repo, dan setiap angka
yang tampil di layar hari ini bisa ditelusuri ke satu baris berkas. Tidak ada artefak baru yang
ditunggu. Penetapannya memakai status `siap sekarang` pada [KAT] baris 2597, yaitu 32 fitur.

**Aturan G2, butuh satu berkas.** Tepat satu artefak belum ada, dan artefak itu bisa dibuat dari
data yang sudah ada di repo atau oleh satu pemilik internal. Sebelum artefak itu ada, layar tetap
boleh dibangun, tetapi angkanya tampil sebagai label abstain, bukan angka. Penetapannya memakai
status `siap sebagian` dan `rancangan` pada [KAT] baris 2598 dan 2599, lalu disaring aturan G3.

**Aturan G3, arsip.** Prasyaratnya lebih dari satu artefak, atau minimal satu artefak harus datang
dari pihak di luar kewenangan tim ini: tarif biaya dari pemilik anggaran, pemasangan kanal fisik,
atau tanda tangan lintas pihak. Fitur seperti ini tidak dibuang; ia diarsipkan dengan syarat buka
tertulis di bagian 5.3.

Hasil penetapan, dan pemeriksaan bahwa jumlahnya menutup 48:

| Gelombang | Jumlah | Dasar penetapan |
|---|---:|---|
| G1 data ada | 32 | [KAT] baris 2597, status `siap sekarang` |
| G2 butuh satu berkas | 13 | [KAT] baris 2598 dan 2599, disaring aturan G3 |
| G3 arsip | 3 | prasyarat lebih dari satu, minimal satu dari pihak luar |
| **Total** | **48** | [KAT] baris 2585, jumlah fitur |

Lima belas fitur yang menurut [KAT] berstatus `siap sebagian` tidak otomatis masuk G2. Dua belas di
antaranya memenuhi aturan G2, sedangkan tiga sisanya, yaitu KEP-10, INS-04, dan INS-05, memenuhi
aturan G3 karena masing masing menunggu dua atau tiga artefak sekaligus, dan minimal satu artefak
itu bukan milik tim ini. Fitur keenam belas di luar G1 adalah KEP-04 yang berstatus `rancangan`, dan
ia masuk G2 karena hanya menunggu satu ekspor. Rinciannya di bagian 4.2 dan 5.2.

### 2.1 Ambang yang dipakai, tanpa satu pun ambang baru

Kriteria diterima kartu ini meminta tidak ada target baru yang menggeser ambang. Karena itu seluruh
ambang di dokumen ini adalah ambang yang sudah tertulis di dokumen hulu, dan tidak ada satu angka
baru yang dijadikan syarat lulus.

| Ambang | Nilai | Sumber |
|---|---|---|
| FAR maksimum pada titik operasi | 6 per 24 jam | [S6] baris 36 dan baris 74 |
| Recall minimum | 0,5 | [S6] baris 36 dan baris 99 |
| Slot alarm otomatis | 0 | `scratch/v9_i1/v9_i1_RESULTS.json` baris 1414; [KAT] baris 204 |
| Syarat naik tier | tiga sekaligus: C stabil, A dengan FAR di bawah 6, B beban manusia yang dapat diterima | [S6] baris 72 sampai 74 |
| Peta tier yang berlaku | 11 baris kelas dan komponen | [S6] baris 163 sampai 167 |
| Keputusan akhir | `MANUSIA`, tanpa nilai lain | [KD] baris 163 dan 168 sampai 170 |

Dokumen ini menambah urutan, bukan ambang. Urutan tidak mengubah satu ambang pun, dan tidak ada
gelombang yang mendapat angka lulus sendiri.

---

## 3. Gelombang 1: data ada (32 fitur)

Tiga puluh dua fitur yang seluruh masukannya sudah ada di repo. Gelombang ini dibagi dua sub
gelombang karena cara menyerahkannya berbeda, bukan karena nilainya berbeda.

- **G1A, 23 fitur, tanpa batas tercetak.** Seluruh angka yang tampil berlaku untuk keseluruhan
  cakupan fitur.
- **G1B, 9 fitur, dengan batas tercetak.** Angkanya sah, tetapi cakupannya lebih sempit daripada
  nama fiturnya, sehingga label batas wajib ikut tampil. Rujukan batas per fitur ada di tabel
  bagian 3.2.

### 3.1 G1A, 23 fitur tanpa batas tercetak

| ID | Nama fitur | Pengguna dan momen pakai | Masukan | Keluaran | Status bukti |
|---|---|---|---|---|---|
| KEP-01 | Papan vonis per kelas kerusakan | insinyur pengeboran dan supervisor, sebelum mempercayai badge kelas dan saat serah terima shift | tabel komposisi per kelas, peta tier, komposisi head, gerbang tier | sebelas kartu, satu per klaim, tiap kartu memuat tier dan 2 sampai 4 angka penopang | siap sekarang, seluruh isi dari tabel terbit |
| KEP-05 | Gerbang provenance angka tiga warna | penulis laporan sebelum menyusun bab, sekali per bab | daftar temuan audit, daftar larangan kutip, hasil 40 uji | tabel angka dengan kolom berkas, baris, status warna, perintah hitung ulang | siap sekarang, 37 cocok, 2 cocok dengan catatan, 1 tidak cocok |
| KEP-06 | Papan dua pembacaan literal dan ketat | dosen penguji saat bimbingan, sekali per sesi | vonis tiga kelas lolos gate, daftar selisih pembacaan | satu kartu dua kolom status dan satu baris selisih | siap sekarang untuk isi angka |
| KEP-07 | Pengunci rujukan baris dan uji mutasi angka | auditor internal sebelum menerbitkan vonis, sekali per vonis | dokumen lama, daftar sel, toleransi numerik, dua mutasi kontrol | tiga baris: sel diperiksa, selisih asli, selisih mutasi | siap sekarang, desain tes dan hasilnya terukur |
| KEP-09 | Banner transparansi label bit_wear | reviewer saat membaca bab evaluasi, sekali per bab | hasil rekonstruksi label dan diagnostik sirkularitas | banner tiga baris dengan dua angka pendukung | siap sekarang, kedua angka terukur dan bersumber baris |
| MNT-02 | Kalkulator anggaran pemeriksaan | supervisor pemeliharaan saat membandingkan dua kandidat titik operasi | alarm palsu engine, alarm palsu baseline, recall pada titik itu | dua angka persen per titik: penghematan pemeriksaan dan deteksi yang hilang | siap sekarang, rumus tertulis dengan nomor baris |
| MNT-03 | Sakelar dua titik operasi hyd | supervisor shift pada awal shift, sekali per shift | dua keluaran engine dengan angka per fold | tabel enam kolom untuk tiga baris, plus selisih | siap sekarang, tujuh nilai per titik bersumber baris |
| MNT-04 | Panel titik operasi hemat-awas shk | driller saat memilih kepekaan pada awal shift | grid ambang, presisi dan recall per titik, FAR per 24 jam | empat baris titik operasi plus satu baris pembanding | siap sekarang, empat titik dan penghematan negatif terukur |
| MNT-08 | Indikator status hidrolik | mudlogger dan driller sepanjang shift | residu tekanan terhadap median dan MAD per bin laju aliran | status per jendela, cakupan sensor persen, jumlah blok per hari | siap sekarang, semua angka terukur dan sudah diuji baca |
| DAT-01 | Kartu kelengkapan jendela pra-event | engineer PdM saat membuka satu event atau satu baris riwayat | metadata jendela per event: jumlah baris, gap median, gap maksimum | empat label plus tiga angka per panjang jendela | siap sekarang, angka cocok dengan dokumen sumber |
| DAT-02 | Kanal status sumur tidak logging | driller saat event masuk dengan jendela kosong | mask NaN per jendela, daftar event dengan seluruh fitur kosong | status tidak ada logging beserta rentang waktu kosong dan sumur | siap sekarang, sebaran per sumur terverifikasi ulang |
| DAT-03 | Peta label ke fold dan antrean parse | auditor sebelum kampanye training, sekali per kampanye | blok `coverage`: 884 label, 671 terpetakan, 213 di luar | tabel label dengan status dan jumlah event per sumur | siap sekarang, angka dari meta artefak |
| DAT-05 | Matriks ketersediaan berkas per sumur | engineer PdM sebelum memilih sumur untuk kampanye baru | audit unduhan 17.368 berkas, 11.894 berkas WITSML untuk 27 sumur | kartu per sumur berisi jumlah berkas per kategori dan status | siap sekarang, audit byte per byte pihak terpisah |
| DAT-06 | Antrean parse 3.906 berkas | koordinator data saat merencanakan perluasan cakupan | daftar berkas belum diparse: 2.156 dan 1.750, total 3.906 atau 54,6 persen dari 7.150 | antrean berisi jumlah berkas, perkiraan kanal, calon kelas yang terbuka | siap sekarang, hitungan `find` cocok dengan sumber |
| DAT-07 | Katalog label instrumen per sumur | auditor saat membaca hasil lintas sumur, sekali per kampanye | pemindaian header sepuluh CSV terparse | matriks sumur kali kanal dengan jumlah sumur | siap sekarang, satu koreksi terhadap tabel sumber |
| DAT-10 | Validitas kedalaman MD ke TVD | engineer drilling sebelum menjalankan fitur hidraulik | 5.561 stasiun survey dari 63 trajectory dan 27 wbGeometry | kolom TVD dan status terkoreksi per baris, plus ringkasan 80,1 persen | siap sekarang, dihitung ulang auditor dengan alat berbeda |
| CMP-01 | Balapan model terhadap baseline persistence | peneliti saat menyusun laporan kemajuan, sekali per bulan | AUPRC per fold dari baseline dan dari model, per kelas | grafik berpasangan per fold plus median kedua metode | siap sekarang, median dan jumlah fold terukur |
| CMP-02 | Peta kalah-menang per kelas | PM saat memutuskan kelas mana yang dipakai, sekali per kampanye | AUPRC per fold per kelas untuk model dan pembandingnya | tabel kelas dengan jumlah fold menang, selisih median, nama pembanding | siap sekarang |
| CMP-04 | Kartu rekam jejak per sumur | auditor saat menilai klaim lintas sumur, sekali per kampanye | jumlah positif per sumur dan per kelas | daftar sumur dengan jumlah positif dan status daya | siap sekarang, aturan UNDERPOWERED tertulis |
| CMP-05 | Bukti sirkularitas target mekanika | reviewer saat membaca bab evaluasi, sekali per bab | akurasi rekonstruksi, presisi dan recall pasangan, MAE dan R2 | tabel target dengan metrik dan tanda sirkularitas | siap sekarang, seluruh angka bersumber baris |
| LIN-02 | Garis waktu tingkat target dan gerbang | auditor saat menilai konsistensi dokumen, sekali per audit | 11 klaim lapisan A beserta tier per engine, status dokumen | garis waktu vertikal dengan status per dokumen dan tautan angka | siap sekarang, empat inventaris dan satu laporan dibuka penuh |
| LIN-06 | Kuis dua halaman tentang angka | dosen penguji sebelum sidang, sekali per sidang | 11 klaim lapisan A beserta presisi, recall, FAR per kelas | dua halaman, maksimal 12 baris angka, tiap baris satu kalimat batas | siap sekarang, seluruh angka bersumber baris |
| INS-02 | Panduan skrip verifikasi rujukan | auditor sebelum menerbitkan vonis, sekali per vonis | daftar sel angka dengan rujukan baris, toleransi 5e-5, dua mutasi kontrol | log tiga baris beserta daftar selisih | siap sekarang, prosedur dan hasilnya terukur |

Jumlah baris data tabel di atas: 23.

### 3.2 G1B, 9 fitur dengan batas tercetak

Kesembilan fitur ini boleh dibangun sekarang, dengan satu syarat tampilan: batas cakupannya
tercetak pada layar yang sama dengan angkanya. Alasannya bukan kehati hatian berlebihan, melainkan
karena nama fiturnya lebih luas daripada datanya, dan selisih itu sudah diakui sumbernya.

| ID | Nama fitur | Pengguna dan momen pakai | Masukan | Keluaran | Status bukti dan batas yang wajib tercetak |
|---|---|---|---|---|---|
| KEP-03 | Badge beban alarm dan pengunci satuan FAR | operator shift yang memutuskan menindaklanjuti satu peringatan | FAR per fold, jumlah fold, alarm palsu, true positive, satuan, skala waktu | badge teks dan angka dengan satuan tertulis | siap sekarang untuk lima kelas: vib, shk, stuck, hyd, tool_wear ([KAT] baris 419) |
| MNT-01 | Antrean triage onset per shift dengan umur item | insinyur shift malam dan toolpusher pada awal shift dan setiap dua jam | skor ranking per jendela, horizon, riwayat alarm, ambang terpilih | tabel berurut dengan kolom pengenal jendela, sumur, waktu, umur item | siap sekarang untuk komponen skor, cakupan, TLead, dan FAR ([KAT] baris 925) |
| MNT-06 | Mode bengkel dan detektor perubahan regime | teknisi bengkel saat run berjalan, beberapa kali per run | deret 1 detik per run alat, kurtosis, crest, frekuensi dominan | daftar run dengan penanda perubahan, lead detik, alarm palsu per menit | siap sekarang untuk deteksi perubahan; klaim keausan spesifik belum ([KAT] baris 1177) |
| MNT-07 | Kurva tren keausan dengan cap keterlambatan | engineer drilling saat mengevaluasi performa harian | status `high_MSE`, skor screening, AUPRC per fold | kurva tren per sumur dengan sumbu kedalaman dan cap keterlambatan | siap sekarang untuk kurva status; precision, recall, FAR belum ([KAT] baris 1223) |
| DAT-08 | Kartu kesiapan kanal per sumur | engineer saat memasang panel pada sumur baru, sekali per pemasangan | daftar kanal per engine, jumlah baris terisi dan kosong per kanal per sumur | kartu per sumur dengan baris per kanal: persen kosong, jumlah berkas, status | siap sekarang untuk tiga kanal yang angkanya terukur: CRPM, VIBLAT, dan satu lagi ([KAT] baris 1665) |
| DAT-09 | Peta drift antar sumur dan dalam sumur | penanggung jawab mutu data saat menilai kelayakan pindah sumur | statistik jendela dasar per paruh waktu per sumur | matriks jarak antar sumur dan grafik jarak antar paruh | siap sekarang untuk lima sumur yang diuji ([KAT] baris 1707) |
| CMP-03 | Tabel kanal masukan yang melawan intuisi | peneliti saat memilih fitur kampanye baru, sekali per kampanye | selisih mutu saat satu kanal dikeluarkan, per kelas dan per fold | daftar kanal dengan arah pengaruh, selisih median, jumlah fold, batas domain | siap sekarang untuk angka; cakupan belum semua kanal ([KAT] baris 1867) |
| LIN-04 | Register status dokumen vonis | auditor saat memeriksa rujukan, sekali per audit | daftar dokumen vonis beserta byte, baris, dan status | tabel 10 baris dengan byte, baris, status, dan alasan | siap sekarang untuk 10 dokumen yang diperiksa ([KAT] baris 2231) |
| LIN-05 | Kalender sumber angka | auditor sebelum menerbitkan, sekali per audit | hasil 40 uji angka: 37 cocok, 2 cocok dengan catatan, 1 tidak cocok | kalender dengan status per angka dan jumlah uji per bulan | siap sekarang untuk 40 uji; 69 dokumen di luar cakupan ([KAT] baris 2267) |

Jumlah baris data tabel di atas: 9.

### 3.3 Alasan urutan di dalam gelombang 1

Urutan tidak memakai abjad dan tidak memakai nomor fitur. Urutannya mengikuti satu aturan yang
sudah tertulis di arsitektur: setiap angka wajib tampil bersama asalnya, sehingga gerbang provenance
harus berdiri sebelum angka pertama tampil.

**Putaran 1, halaman PG-07 Bukti angka.** Empat fitur: KEP-05, KEP-07, INS-02, LIN-05. Alasannya
dua lapis. Pertama, [AI] baris 131 menetapkan PG-07 sebagai halaman yang menjawab "dari mana angka
ini, dan boleh dikutip atau belum". Kedua, [AI] baris 90 sampai 94 menetapkan prinsip kedua, angka
tidak pernah tampil sendirian. Membangun gerbang provenance lebih dulu membuat setiap halaman
berikutnya mewarisi gerbang itu, bukan memasangnya belakangan pada 30 layar yang sudah jadi.

**Putaran 2, halaman PG-00 Beranda hari ini.** Tiga fitur yang tersedia di gelombang 1: KEP-03,
MNT-01, LIN-02. Fitur keempat PG-00, yaitu KEP-02, berada di gelombang 2, sehingga beranda pada
hari pertama akan menampilkan satu blok abstain. Ini bukan cacat urutan, melainkan keadaan yang
sudah diakui [AI] baris 124: "siap sekarang, dengan satu blok siap sebagian".

**Putaran 3, halaman PG-01 Kepercayaan.** Tiga fitur: KEP-01, KEP-06, KEP-09. Urutan ini menaruh
papan vonis setelah gerbang provenance, supaya kartu tier tidak tampil lebih kuat daripada buktinya.

**Putaran 4, halaman PG-02 Perencanaan maintenance.** Enam fitur: MNT-02, MNT-03, MNT-04, MNT-06,
MNT-07, MNT-08. Di dalamnya, MNT-02 dan MNT-03 didahulukan karena keduanya memberi angka penghematan
pemeriksaan, dan angka itu yang dipakai pengguna untuk memutuskan apakah panel lain layak dibuka.

**Putaran 5, halaman PG-03 Kualitas data.** Sembilan fitur: DAT-01, DAT-02, DAT-03, DAT-05, DAT-06,
DAT-07, DAT-08, DAT-09, DAT-10. DAT-05 dan DAT-08 didahulukan karena keduanya menjadi tujuan tautan
dari badge abstain di seluruh halaman lain ([AI] baris 949 sampai 951).

**Putaran 6, halaman PG-04 Perbandingan mesin.** Lima fitur: CMP-01, CMP-02, CMP-03, CMP-04, CMP-05.
CMP-01 didahulukan karena ia pembanding baseline, dan empat lainnya memakai pembanding yang sama.

**Putaran 7, halaman PG-05 Linimasa.** Dua fitur: LIN-04, LIN-06.

Jumlah 4 ditambah 3 ditambah 3 ditambah 6 ditambah 9 ditambah 5 ditambah 2 sama dengan 32, yaitu
seluruh isi gelombang 1.

### 3.4 Risiko gelombang 1

| Kode | Risiko | Bukti | Penanganan |
|---|---|---|---|
| R1-1 | Beranda menampilkan blok abstain pada hari pertama karena KEP-02 belum ada | [AI] baris 124 menyebut satu blok siap sebagian di PG-00 | teks abstain diambil dari [KD] baris 1006, bukan karangan tim |
| R1-2 | Sembilan fitur G1B kehilangan label batas, lalu terbaca lebih luas daripada datanya | [KAT] baris 419, 925, 1177, 1223, 1665, 1707, 1867, 2231, 2267 | label batas menjadi bagian dari definisi selesai, bukan tambahan |
| R1-3 | Tanggal yang tampil dibaca sebagai tanggal data, padahal berasal dari jam render | [KD] baris 1109 sampai 1111: asal kalender tidak diverifikasi, field `_utc` dari jam sistem | setiap field `_utc` diberi label "jam render", dan `waktu_indeks_menit` tampil tanpa tanggal |
| R1-4 | Antrean 3.906 berkas dibaca sebagai kemajuan cakupan | [KAT] baris 1554: 3.906 dari 7.150 atau 54,6 persen | kalimat arti dari [KAT] baris 1564 dipakai apa adanya |
| R1-5 | Dua tanda pisah panjang di dalam blok kode 08 masih terhitung oleh `grep` polos saat serah terima | [AUD] baris 340: `08_KONTRAK_DATA.md:2`, baris 1219 dan 1238 | diselesaikan sebelum serah terima, lihat bagian 8 butir 5 |
| R1-6 | Halaman menampilkan warna merah tanpa label manusia peninjau | [KAT] baris 203 sampai 207 melarangnya | uji klik dan uji warna masuk daftar serah terima bagian 8 butir 8 |

---

## 4. Gelombang 2: butuh satu berkas (13 fitur)

Tiga belas fitur yang menunggu tepat satu artefak. Layar boleh dibangun sekarang; yang ditunggu
adalah angka di dalamnya. Sampai artefak itu ada, layar wajib memakai teks keadaan dari [KD]
bagian 7, bukan angka nol, karena nol adalah hasil ukur yang sah dan berbeda arti dari belum diukur
([KD] baris 94 sampai 96).

### 4.1 Lima field wajib, 13 fitur

| ID | Nama fitur | Pengguna dan momen pakai | Masukan | Keluaran | Status bukti |
|---|---|---|---|---|---|
| KEP-02 | Skor keyakinan 0 sampai 100 berlapis selang | insinyur pemeliharaan saat memilih satu peringatan untuk dikerjakan lebih dulu | tiga komponen berbobot S_A, S_B, S_C dari lift per fold, B1, FAR, penilaian C1 sampai C4 | satu bilangan bulat 0 sampai 100, satu pita selang, tiga komponen dua desimal | siap sebagian, aritmetika delapan baris sudah dihitung ulang |
| KEP-04 | Kurva kalibrasi dan titik kuantil per head | penilai model saat memutuskan apakah skor boleh dibaca sebagai frekuensi | pasangan skor prediksi dan label nyata per fold, per kelas, dua kolom | satu kurva per head dengan jumlah bin tetap | rancangan, baru ada AUPRC dan CI95 |
| KEP-08 | Panel ketidaksepakatan antar head | supervisor saat menyiapkan eskalasi, dua sampai empat kali per shift | sinyal per menit dari empat komponen pada jendela yang sama | panel per jendela dan matriks kesepakatan tingkat jendela | siap sebagian, arah pemangkasan terukur untuk hyd dan ssi |
| MNT-05 | Penaksir beban tinjauan per shift | supervisor saat menyusun jadwal shift, sekali per hari | FAR per 24 jam per head dan label segmen sumber angka | enam angka tinjauan per shift dengan label segmen | siap sebagian, angka ada tetapi batas segmen diakui sumber |
| MNT-09 | Watchlist stick-slip dan penanda daya statistik | supervisor operasi pada rapat pagi dan serah terima shift | skor per jendela lintas sumur, jumlah positif per sumur, kelas severitas | daftar sumur berurut dengan skor, jumlah positif, status daya | siap sebagian, aturan menonaktifkan panel masih usulan |
| DAT-04 | Pemilih kanal berbasis fill rate dan QC fisik | engineer data saat menyusun fitur kampanye baru | fill rate per kanal per sumur, daftar kanal per fold, penanda konstansi | daftar kanal lolos beserta alasan dan daftar gugur beserta fill rate | siap sebagian, sisi seleksi terukur, QC fisik belum dijalankan |
| CMP-06 | Lembar prasyarat eksperimen | peneliti sebelum menjalankan eksperimen baru | butir pra daftar: dua model, tiga seed, dataset tetap, split per fold | lembar sembilan butir dengan status centang | siap sebagian, butir tertulis, penerapan otomatis belum ada |
| CMP-07 | Panel kesetaraan head hyd | PM saat menulis klaim perbaikan pada laporan | metrik per komposisi pada kelas hyd: TP, alarm palsu, presisi, recall, FAR, lead | matriks pasangan head dengan status setara atau berbeda | siap sebagian, derau seed terukur, selang per pasangan belum |
| LIN-01 | Log keputusan human-in-loop | supervisor setiap kali menutup peringatan, beberapa kali per shift | identitas head, skor keyakinan, badge beban alarm, tindakan, alasan | riwayat keputusan per head, tingkat tindak lanjut, daftar peringatan terbuka | siap sebagian, aturan tinjauan terukur pada 11 dari 11 head |
| LIN-03 | Penanda selang wajib pada setiap angka FAR dan recall | reviewer saat memeriksa tabel hasil, sekali per laporan | jumlah iterasi bootstrap, seed, blok bootstrap, cakupan waktu, angka titik | tiga angka per sel: titik, batas bawah, batas atas, plus penanda | siap sebagian, beberapa sel masih berisi titik tanpa selang |
| LIN-07 | Linimasa tier per kelas dan syarat naik tier | PM saat menyusun rencana kerja per kelas, sekali per kampanye | tier per engine, gerbang tier, jumlah butir syarat yang terpenuhi | tabel kelas dengan tier, bukti pendukung, syarat naik | siap sebagian, syarat naik sebagian kelas belum berangka |
| INS-01 | Wizard kalibrasi dan uji jalan sebelum pindah sumur | penanggung jawab mutu data saat menyiapkan sumur baru | statistik jendela dasar per sumur per paruh, riwayat FAR konfigurasi lama | satu status per syarat, empat baris, plus satu keputusan akhir | siap sebagian, tiga dari empat syarat berangka |
| INS-03 | Kartu kelayakan sinyal sebelum dekomposisi | peneliti sinyal sebelum menjalankan dekomposisi pada kanal baru | laju sampel kanal, pita frekuensi yang dicari, panjang segmen, hasil uji stasioner | satu baris per kanal dengan status, pita tertinggi, alasan | siap sebagian, tiga metode sudah diuji, kartunya belum dibangun |

Jumlah baris data tabel di atas: 13.

### 4.2 Satu artefak yang ditunggu per fitur

Kolom artefak di bawah sengaja berisi satu benda, bukan daftar keinginan. Bila satu fitur butuh
lebih dari satu artefak, ia tidak berada di gelombang ini, dan itulah yang memindahkan KEP-10,
INS-04, dan INS-05 ke gelombang 3.

| ID | Artefak yang ditunggu | Pemilik | Uji naik status | Rujukan kelangkaan |
|---|---|---|---|---|
| KEP-02 | satu ekspor peringatan historis berskor, header memuat satu rumus yang dibekukan | penilai model | urutan peringatan berdasarkan skor lebih baik daripada urutan acak pada fold yang sama | [KAT] baris 347 sampai 351 |
| KEP-04 | satu ekspor pasangan skor dan label per fold | penilai model | kurva dihitung pada dua set bin, 10 dan 20, arah penyimpangan tidak berubah | [KAT] baris 486 sampai 490 |
| KEP-08 | satu berkas deret sinyal per menit tersimpan | ML engineer | matriks dihitung dari deret tersimpan, bukan dari ringkasan | [KAT] baris 728 sampai 732; [AI] baris 994 |
| MNT-05 | satu berkas jadwal inspeksi per shift | supervisor pemeliharaan | angka tunda layar dibandingkan dengan hitungan manual satu shift | [S6] baris 356: tidak ada satu pun berkas jadwal inspeksi di repo |
| MNT-09 | satu aturan tertulis ambang daya statistik per kelas | penanggung jawab mutu data | sumur kurang berdaya tidak muncul di urutan perbandingan | [KAT] baris 1308 sampai 1310 |
| DAT-04 | satu laporan uji QC fisik: validasi satuan dan duplikat timestamp | engineer data | uji konstansi pada kanal yang lolos, tidak ada kanal bernilai tetap | [KAT] baris 1498 sampai 1501 |
| CMP-06 | satu berkas alat penegak lembar prasyarat | peneliti | satu eksperimen kecil dengan satu butir sengaja dikosongkan, lembar menolaknya | [KAT] baris 1975 sampai 1977 |
| CMP-07 | satu tabel selang per pasangan head | PM | selisih satu pasangan dihitung ulang dari TP dan alarm palsu, cocok dengan sel matriks | [KAT] baris 2047 sampai 2051 |
| LIN-01 | satu berkas skema log keputusan, terisi satu shift penuh | supervisor | satu peringatan ditutup, umur item berhenti bertambah dan tingkat tindak lanjut berubah | [KAT] baris 2103 sampai 2105; [AI] baris 1030 |
| LIN-03 | satu tabel selang bootstrap untuk seluruh sel | reviewer | satu angka recall dihitung ulang dengan seed berbeda, penanda tidak berubah | [KAT] baris 2186 sampai 2189 |
| LIN-07 | satu lembar beban pemeriksaan per shift, sama dengan artefak MNT-05 | manajer pemeliharaan | seluruh butir syarat naik satu kelas diperiksa sebelum tier dinaikkan | [KAT] baris 2341 sampai 2343; [S6] baris 269 sampai 272 |
| INS-01 | satu aturan tertulis ambang daya statistik per kelas, sama dengan artefak MNT-09 | penanggung jawab mutu data | wizard dijalankan pada satu sumur baru, menolak ketika kanal masukan kosong | [KAT] baris 2408 sampai 2412 |
| INS-03 | satu berkas kartu kelayakan sinyal sebagai alat | peneliti sinyal | kartu dijalankan pada satu kanal baru, statusnya cocok dengan hitungan Nyquist manual | [KAT] baris 2486 sampai 2489 |

Jumlah baris data tabel di atas: 13.

Dua pasang fitur berbagi satu artefak: MNT-05 dengan LIN-07 pada lembar beban pemeriksaan, dan
MNT-09 dengan INS-01 pada aturan daya statistik. Artinya tiga belas fitur menunggu sebelas artefak,
bukan tiga belas. Ini menguntungkan, dan risikonya ditulis di bagian 4.4 butir R2-2.

### 4.3 Alasan urutan di dalam gelombang 2

Urutan gelombang 2 memakai satu kriteria: seberapa cepat artefaknya bisa hadir tanpa menunggu pihak
luar. Empat tingkat, dari tercepat ke terlama.

**Tingkat 1, artefak hasil hitungan atas berkas yang sudah ada.** LIN-03 dan CMP-07. Keduanya
hanya butuh menjalankan bootstrap dan selang pada data yang sudah ada, sehingga bisa ditutup tanpa
menunggu siapa pun. Keduanya ditaruh paling depan karena biayanya paling kecil dan nilainya paling
langsung: setiap angka FAR dan recall di seluruh situs menjadi sah dikutip dengan selang.

**Tingkat 2, artefak hasil ekspor dari pemilik model.** KEP-02, KEP-04, KEP-08, INS-03. Keempatnya
menunggu satu ekspor atau satu alat dari orang yang sama, yaitu pemilik model dan peneliti sinyal.
Mengelompokkannya membuat satu orang menyelesaikan empat prasyarat dengan satu format ekspor, bukan
empat format.

**Tingkat 3, artefak hasil pencatatan operasional.** LIN-01, MNT-05, LIN-07, MNT-09, INS-01.
Kelima ini menunggu satu shift pencatatan atau satu aturan tertulis yang disepakati supervisor dan
penanggung jawab mutu data. Yang paling menentukan adalah LIN-01, karena log keputusan yang terisi
satu shift menjadi bukti bahwa lapisan B bisa diukur sama sekali ([S6] baris 356 dan 357).

**Tingkat 4, artefak hasil satu kampanye pengujian.** DAT-04 dan CMP-06. Keduanya menunggu satu
putaran kerja yang lebih panjang: QC fisik pada kanal, dan penegakan lembar prasyarat pada satu
eksperimen. Keduanya ditaruh terakhir bukan karena kurang penting, melainkan karena hasilnya baru
berguna setelah ada kampanye berikutnya.

### 4.4 Risiko gelombang 2

| Kode | Risiko | Bukti | Penanganan |
|---|---|---|---|
| R2-1 | Tiga belas kerangka layar dibangun, nol muatan, lalu panel kosong terbaca sebagai "tidak ada peringatan" | [KD] baris 1013: antrean kosong bukan berarti aman | teks `KOSONG` dipakai kata per kata dari [KD] baris 1007, 1013, 1019, 1025, 1031, 1037 |
| R2-2 | Satu artefak terlambat memblokir dua fitur sekaligus | pasangan MNT-05 dengan LIN-07, dan MNT-09 dengan INS-01, pada tabel 4.2 | kedua pasangan diberi satu pemilik yang sama, bukan dua |
| R2-3 | Dua ekspor model memakai dua format berbeda, sehingga skor KEP-02 dan kurva KEP-04 memakai dua skala yang tidak sebanding | [KAT] baris 347 sampai 351 menyebut dua rumus hidup bersama | satu format ekspor, satu pemilik, satu header berisi versi rumus |
| R2-4 | Angka baru masuk layar tanpa baris ledger, sehingga lolos dari gerbang PG-07 | [KD] baris 172 sampai 174: baris tanpa `sumber_data` ditolak | setiap artefak gelombang 2 wajib mendarat bersama satu baris ledger baru |
| R2-5 | LIN-03 dan CMP-07 ditunda karena dianggap pekerjaan model, padahal keduanya bisa ditutup tanpa menunggu siapa pun | [KAT] baris 2186 dan 2047 | keduanya diletakkan di tingkat 1 pada bagian 4.3 |
| R2-6 | Skor keyakinan dipakai sebagai ambang keputusan sebelum pemetaan dibekukan | [KAT] baris 361: salah tafsir keempat | tombol tindakan tidak dibuat pada pita P1 dan P2 ([AI] baris 1013) |

---

## 5. Gelombang 3: arsip (3 fitur)

Tiga fitur yang diarsipkan, dengan syarat buka tertulis. Kata arsip dipakai dalam arti diarsipkan,
bukan dibuang: ketiganya tetap ada di katalog, tetap punya kode, dan tetap punya halaman rumah.
Yang tidak dilakukan adalah memasukkannya ke antrean bangun sebelum prasyaratnya lengkap, karena
masing masing menunggu dua atau tiga artefak sekaligus dan minimal satu artefak itu bukan milik
tim ini.

### 5.1 Lima field wajib, 3 fitur

| ID | Nama fitur | Pengguna dan momen pakai | Masukan | Keluaran | Status bukti |
|---|---|---|---|---|---|
| KEP-10 | Slot nilai jujur lapisan B | perencana maintenance saat menyusun prioritas perbaikan, sekali per siklus | agregat aktivitas `ddr.parquet`, jam henti per sebab, dan tarif biaya | panel tiga tingkat, tingkat tiga berisi slot kosong beserta pemilik data | siap sebagian, tingkat satu dan dua terukur, tingkat tiga memang kosong |
| INS-04 | Kartu kanal yang perlu dipasang | engineer instrumentasi saat satu engine berhenti di titik operasi | daftar kanal per engine, bukti ketiadaan, dampak terukur pada metrik | daftar kanal prioritas dengan alasan angka dan dampak bila kanal dipasang | siap sebagian, siap sekarang hanya untuk kanal yang sudah terbukti absen |
| INS-05 | Kartu permintaan data bertanda tangan | koordinator data saat rapat data, sekali per rapat | tiga bukti ketiadaan yang sudah diuji ulang, daftar pemilik data | daftar permintaan dengan tag, berkas, pemilik, dampak, status tanda tangan | siap sebagian, mekanisme tanda tangan lintas pihak belum ada |

Jumlah baris data tabel di atas: 3.

### 5.2 Mengapa ketiganya diarsipkan, bukan dimasukkan gelombang 2

| ID | Artefak yang ditunggu | Jumlah | Pemilik | Kenapa bukan gelombang 2 |
|---|---|---:|---|---|
| KEP-10 | satu lembar tarif biaya henti, dan satu keputusan pemetaan kategori equipment failure ke tabel S4 | 2 | manajer pemeliharaan dan pemilik anggaran | dua artefak, dan tarif bukan milik tim ini; [KAT] baris 849 sampai 852 menyebut tingkat tiga kosong dan itu memang isinya |
| INS-04 | satu daftar kanal per engine yang lengkap, dan satu jadwal pemasangan kanal fisik | 2 | engineer instrumentasi | dua artefak, dan yang kedua berupa pekerjaan lapangan, bukan berkas; [KAT] baris 2526 sampai 2529 |
| INS-05 | satu perjanjian berbagi data, satu berkas identitas alat, dan satu mekanisme tanda tangan lintas pihak | 3 | koordinator data dan pembimbing | tiga artefak, dua di antaranya bukan berkas; [KAT] baris 2571 sampai 2574 |

### 5.3 Syarat buka dan risiko gelombang 3

| ID | Syarat buka | Uji yang menandai terbuka | Risiko bila dibangun sekarang |
|---|---|---|---|
| KEP-10 | lembar tarif mendarat beserta satu baris ledger, dan keputusan pemetaan kategori ditulis | total jam satu kategori dihitung ulang dari `ddr.parquet` dan cocok dengan 39.397,986 jam | tingkat tiga tetap kosong, sehingga panel menampilkan dua dari tiga tingkat dan terbaca sebagai pekerjaan yang belum selesai |
| INS-04 | daftar kanal per engine lengkap beserta jadwal pemasangan | kartu dijalankan pada satu kanal baru, keberadaan kanal diperiksa langsung pada berkas sumur | daftar tanpa pemasangan berubah menjadi daftar keinginan, dan dampak terukur kehilangan ujinya |
| INS-05 | perjanjian berbagi data ditandatangani, lalu berkas identitas alat mendarat | pencarian kolom pada berkas target diulang, hasilnya tetap nol sebelum data mendarat | kartu tanpa tanda tangan adalah permintaan, bukan kontrak, dan pembaca membacanya sebagai janji |

Satu hal yang harus ditulis terang tentang gelombang ini: ketiga fitur menyentuh dua hal yang paling
sering dibaca lebih kuat daripada buktinya, yaitu uang dan perangkat keras. KEP-10 menyentuh uang,
INS-04 dan INS-05 menyentuh perangkat dan kepemilikan data. Karena itu gelombang ini mendapat vonis
tersendiri di bagian 7, dan vonisnya bukan LAYAK.

---

## 6. Rekap 48 fitur dan pemeriksaan penutupan jumlah

| Rumpun | G1A | G1B | G2 | G3 | Total | Halaman rumah |
|---|---:|---:|---:|---:|---:|---|
| KEP kepercayaan | 5 | 1 | 3 | 1 | 10 | PG-01 |
| MNT perencanaan maintenance | 4 | 3 | 2 | 0 | 9 | PG-02 |
| DAT kualitas data | 7 | 2 | 1 | 0 | 10 | PG-03 |
| CMP perbandingan mesin | 4 | 1 | 2 | 0 | 7 | PG-04 |
| LIN linimasa dan jejak keputusan | 2 | 2 | 3 | 0 | 7 | PG-05 |
| INS alat bantu insinyur | 1 | 0 | 2 | 2 | 5 | PG-06 |
| **Total** | **23** | **9** | **13** | **3** | **48** | |

Jumlah baris data tabel di atas: 7, yaitu enam baris rumpun ditambah satu baris total.

Dua pemeriksaan yang bisa diulang pembaca. Pertama, 23 ditambah 9 ditambah 13 ditambah 3 sama
dengan 48, dan 48 adalah jumlah fitur pada [KAT] baris 2585. Kedua, sebaran rumpun 10, 9, 10, 7, 7,
5 sama dengan sebaran pada [AI] baris 67 sampai 72.

Tujuh fitur yang lahir dari kekurangan data, yaitu DAT-02, DAT-05, DAT-06, DAT-08, DAT-09, KEP-10,
dan INS-05 ([KAT] baris 24 dan 25), tersebar di tiga gelombang: lima di gelombang 1, satu di
gelombang 2, dan satu di gelombang 3. Tidak satu pun dibuang, dan itu ujian butir 4 kerangka wajib.

---

## 7. Vonis paket

Vonis memakai dua kata yang diizinkan kartu: LAYAK atau PERLU PERBAIKAN. Vonis diberikan per
cakupan, karena menilai seluruh paket dengan satu kata akan menyembunyikan bagian mana yang siap.

| Cakupan | Vonis | Dasar yang bisa diperiksa |
|---|---|---|
| Paket seluruhnya | **PERLU PERBAIKAN** | [AUD] baris 271 memutuskan PERLU PERBAIKAN dengan enam cacat bernomor. Dua di antaranya melanggar butir 8 secara harfiah, yaitu 2 tanda pisah panjang pada `08_KONTRAK_DATA.md` baris 1219 dan 1238 ([AUD] baris 340), dan satu pemeriksaan pada bagian 10.12 sebenarnya gagal, syarat 0 sedangkan hasil 2 ([AUD] baris 217) |
| Gelombang 1, data ada | **LAYAK** | 29 dari 30 angka cocok dengan sumbernya sampai digit terakhir ([AUD] baris 107). Satu yang tidak cocok adalah ukuran berkas 09 sendiri ([AUD] baris 105), bukan angka fitur mana pun. Enam cacat audit tidak menyentuh satu angka gelombang 1 |
| Gelombang 2, butuh satu berkas | **LAYAK** dengan syarat | Tiga belas fitur, sebelas artefak, seluruhnya bisa dibuat dari data yang sudah ada atau oleh satu pemilik internal. Syaratnya ada di bagian 8 |
| Gelombang 3, arsip | **PERLU PERBAIKAN** | Tiga fitur, prasyaratnya dua sampai tiga artefak, dan minimal satu artefak per fitur berada di luar kewenangan tim ini. Syarat bukanya tertulis di bagian 5.3 |

Alasan gelombang 1 tetap LAYAK meskipun paketnya PERLU PERBAIKAN, ditulis tanpa dibungkus: enam
cacat audit semuanya bersifat teks. Lima di antaranya rujukan bagian, konvensi hitung baris, kata
"apa adanya", dan ukuran berkas basi. Satu di antaranya dua karakter di dalam blok kode. Tidak ada
satu pun yang mengubah angka, dan [AUD] baris 284 sampai 285 menyatakan sendiri bahwa keenam
perbaikan tidak memerlukan hitung ulang satu angka pun dan tidak menggeser satu ambang pun.

Vonis gelombang 2 memakai kata LAYAK dengan syarat, bukan LAYAK penuh, karena tiga belas kerangka
layar yang dibangun tanpa muatan punya satu cara salah baca yang sudah teridentifikasi: panel kosong
dibaca sebagai "tidak ada peringatan" padahal artinya "belum diukur" ([KD] baris 1013).

---

## 8. Syarat serah terima

Sepuluh butir, semuanya bisa diperiksa dengan perintah atau dengan membaca satu baris. Butir yang
tidak terpenuhi menahan serah terima, dan tidak ada butir yang boleh ditawar menjadi "cukup sebagian".

| No | Syarat | Cara memeriksa | Sumber |
|---:|---|---|---|
| 1 | Enam cacat audit ditutup, termasuk bagian 10.13 yang dibuat dan diisi keluaran nyata | [AUD] baris 287 sampai 293 mendaftar enam perbaikan | [AUD] baris 202 sampai 267 |
| 2 | Tanda pisah panjang di seluruh `planning/` berjumlah 0, tanpa pengecualian blok kode | `grep -cP '\x{2014}' planning/*.md` | [AUD] baris 340 |
| 3 | Tidak ada berkas selain markdown di `planning/` | `find planning -maxdepth 1 -type f ! -name '*.md' | wc -l` | [AUD] baris 331 |
| 4 | Amplop 11 field dipakai identik pada setiap muatan, termasuk `keputusan_akhir` bernilai `MANUSIA` | periksa muatan contoh pada [KD] bagian 6 | [KD] baris 152 sampai 164 |
| 5 | `label_kekurangan` hanya berisi tiga nilai yang diizinkan, dan tidak berisi kalimat keluhan | periksa setiap muatan `SEBAGIAN` dan `KOSONG` | [KD] baris 176 sampai 178 |
| 6 | Sembilan fitur G1B menampilkan label batas cakupan pada layar yang sama dengan angkanya | bandingkan nama fitur dengan batas pada tabel bagian 3.2 | [KAT] baris 419 sampai 2267 |
| 7 | Tidak ada halaman alarm otomatis, pusat notifikasi, atau tombol kirim pesan | bandingkan daftar halaman dengan [AI] bagian 9 | [AI] baris 986 sampai 998 |
| 8 | Setiap status punya teks, bukan hanya warna, dan pita P1 serta P2 tanpa elemen pemicu tindakan | uji klik dan uji skala abu pada setiap halaman | [AI] baris 1004 sampai 1014 |
| 9 | Setiap angka baru dari gelombang 2 dan 3 mendarat bersama satu baris ledger | bandingkan berkas baru dengan blok ledger terbaru | [KD] baris 172 sampai 174 |
| 10 | Tidak ada ambang baru yang dipakai sebagai syarat lulus di luar tabel bagian 2.1 | bandingkan seluruh angka lulus dengan tabel itu | bagian 2.1 dokumen ini |

Satu catatan tentang butir 1 dan butir 2: keduanya saling bergantung. Membuat bagian 10.13 pada
`08_KONTRAK_DATA.md` berarti menambah baris, dan baris baru bisa memuat karakter baru. Karena itu
urutan pengerjaannya tetap: selesaikan tanda pisah dulu, lalu isi bagian 10.13, lalu jalankan ulang
`grep` sebagai bukti penutup.

---

## 9. Lima pertanyaan untuk tim website

Lima pertanyaan, bukan lima instruksi. Masing masing menanyakan satu keputusan yang belum diambil
oleh dokumen hulu, dan masing masing menyebut mengapa jawabannya menentukan urutan bangun.

**Pertanyaan 1. Bagaimana tanggal ditampilkan, bila `waktu_indeks_menit` tidak punya pemetaan
kalender?** [KD] baris 1109 sampai 1111 menyatakan asal kalender tidak diverifikasi, dan seluruh
field `_utc` berasal dari jam sistem saat render. Jawabannya menentukan apakah setiap halaman
menampilkan "indeks menit 20189486" atau "jam render 04:12", dan dua pilihan itu punya akibat
berbeda pada uji ulang temuan. Pemilik jawaban: pemilik produk.

**Pertanyaan 2. Siapa yang mengisi log keputusan pada shift pertama, dan kapan?** LIN-01 menunggu
satu shift pencatatan penuh ([KAT] baris 2103 sampai 2105), dan [AI] baris 1030 menetapkan uji naik
statusnya sebagai "satu shift penuh dengan setiap peringatan berlabel". Tanpa jawaban ini, MNT-01
dan LIN-01 tetap menampilkan keadaan kosong, dan lapisan B tetap tidak terukur ([S6] baris 356).
Pemilik jawaban: supervisor operasi.

**Pertanyaan 3. Deret per menit disimpan sebagai berkas apa, dan siapa yang membekukan formatnya?**
KEP-08 menunggu artefak itu ([KAT] baris 728 sampai 732), dan [AI] baris 994 menyatakan halaman
deret per menit sengaja tidak dibuat karena deretnya belum tersimpan. Keputusan format menentukan
apakah matriks kesepakatan bisa dihitung dari deret tersimpan atau tetap dari ringkasan. Pemilik
jawaban: ML engineer.

**Pertanyaan 4. Di mana aturan "tanpa aksi pada pita P1 dan P2" ditegakkan, di pustaka komponen
atau di setiap halaman?** [AI] baris 1013 menetapkan uji klik, dan [AI] baris 1004 sampai 1006
menetapkan setiap status wajib punya teks. Bila aturan ditegakkan per halaman, ia akan lolos pada
halaman ke-11 yang kelak ditambahkan. Pemilik jawaban: tim website.

**Pertanyaan 5. Batas cakupan sembilan fitur G1B ditulis di judul halaman atau hanya di lencana?**
Contohnya KEP-03 yang sah untuk lima kelas ([KAT] baris 419) dan DAT-08 yang sah untuk tiga kanal
([KAT] baris 1665). Bila batasnya hanya di lencana, judul halaman tetap mengklaim seluruh kelas, dan
itu persis salah baca yang dicegah [AI] baris 949 sampai 951. Pemilik jawaban: pemilik produk dan
tim website bersama.

---

## 10. Yang belum diverifikasi

Ditulis terbuka, supaya pembaca tahu batas dokumen ini. Daftar ini bukan penutup yang merendah;
isinya pekerjaan berikutnya beserta alasannya.

1. Empat puluh delapan blok fitur pada [KAT] tidak dibuka satu per satu. Status dan lima field
   dibaca dari tabel ringkasan bagian 3, tabel status bagian 11, dan pencarian baris berlabel.
   Kalimat penjelas di dalam blok yang tidak berhubungan dengan urutan tidak diperiksa.
2. Penetapan gelombang adalah keputusan dokumen ini, bukan field yang sudah ada di repo. Tidak satu
   pun berkas hulu memuat kata gelombang untuk fitur. Aturan penetapannya ditulis di bagian 2 supaya
   pembaca bisa mengulang dan membantahnya dengan bukti.
3. Kata status pada blok fitur dan pada rekap [KAT] berbeda bentuk untuk INS-03, INS-04, dan INS-05.
   Blok menulis "siap sekarang untuk ..." sedangkan rekap menulis "siap sebagian" ([KAT] baris 2598
   berbanding baris 2486, 2526, dan 2571). Dokumen ini memakai rekap, dan tidak menyelesaikan selisih
   itu karena penyelesaiannya mengubah status di katalog, bukan di sini.
4. Tidak ada halaman yang dirender. Seluruh risiko tampilan pada bagian 3.4, 4.4, dan 5.3 berasal
   dari teks, bukan dari pengamatan pada layar. Uji 375 piksel, uji skala abu, dan uji klik belum
   dijalankan pada peramban mana pun.
5. Ukuran byte pada bagian 1 diukur pada 2026-11-01. Bila satu berkas `planning/` disunting sesudah
   dokumen ini, angka pada bagian 1 menjadi basi. Cacat 6 pada [AUD] baris 260 sampai 267 lahir
   persis dari kelalaian ini. Karena itu ukuran berkas dokumen ini sendiri sengaja tidak dicetak di
   dalam dokumen, melainkan dilaporkan di komentar kartu.
6. Baris ledger `docs/RND_PROVENANCE_LEDGER.md` tidak dibuka untuk memeriksa kutipan baris yang
   dipakai [KAT] dan [S6]. Yang diperiksa di sini hanya bahwa angka yang dikutip dokumen hulu sama
   dengan angka yang dikutip dokumen ini.
7. Tidak ada model, engine, atau harness yang dijalankan. Yang dijalankan hanya `stat`, `wc`, `sed`,
   `grep`, `awk`, dan `find`. Seluruh keluarannya ada di bagian 11.
8. Nama pemilik pada tabel 4.2 dan 5.2 adalah peran, bukan orang. Peran itu diambil dari kolom
   pemilik pada [AI] baris 1023 sampai 1034 dan dari teks [KAT], dan belum dikonfirmasi ke pemegang
   peran yang sebenarnya.
9. Angka beban 40,15 baris per shift, yang menjadi dasar urutan MNT-01 dan MNT-05, berasal dari
   simulasi Poisson dan bukan dari hitungan kejadian nyata ([AI] baris 1056 dan 1057). Dokumen ini
   tidak memakainya sebagai ambang, hanya sebagai alasan urutan.
10. Perkiraan lama pengerjaan per gelombang tidak ditulis, karena tidak ada satu pun angka jam kerja
    di repo yang bisa dipakai sebagai dasar. Yang ditulis adalah urutan dan prasyarat, bukan jadwal.

---

## 11. Keluaran perintah yang dijalankan

Ditempel di bawah. Tidak ada satu nilai pun yang diubah. Baris yang berulang dipotong dan
pemotongan disebut.

### A. Ukuran lima berkas masukan dan satu arsip

```
$ stat -c '%n %s bytes' planning/01_KATALOG_FITUR.md planning/07_ARSITEKTUR_INFORMASI.md \
    planning/08_KONTRAK_DATA.md planning/10_AUDIT.md docs/RND_S6_PM_WAVE2.md \
    data/predictive/features_timeseries.npz
planning/01_KATALOG_FITUR.md 166662 bytes
planning/07_ARSITEKTUR_INFORMASI.md 87727 bytes
planning/08_KONTRAK_DATA.md 85929 bytes
planning/10_AUDIT.md 21295 bytes
docs/RND_S6_PM_WAVE2.md 40271 bytes
data/predictive/features_timeseries.npz 458129 bytes
```

### B. Jumlah fitur, halaman, dan fitur prioritas

```
$ sed -n '134,184p' planning/01_KATALOG_FITUR.md | grep -c '^| [A-Z][A-Z]*-[0-9][0-9] '
48
$ sed -n '122,134p' planning/07_ARSITEKTUR_INFORMASI.md | grep -c '^| PG-'
10
$ sed -n '118,141p' planning/08_KONTRAK_DATA.md | grep -c '^| [0-9]'
21
$ grep -c '^### Cacat' planning/10_AUDIT.md
6
```

### C. Tabel status bukti pada katalog

```
$ sed -n '2595,2599p' planning/01_KATALOG_FITUR.md
| Status | Jumlah | Fitur |
|---|---|---|
| Siap sekarang | 32 | KEP-01, KEP-03, KEP-05, KEP-06, KEP-07, KEP-09, MNT-01, MNT-02, MNT-03, MNT-04, MNT-06, MNT-07, MNT-08, DAT-01, DAT-02, DAT-03, DAT-05, DAT-06, DAT-07, DAT-08, DAT-09, DAT-10, CMP-01, CMP-02, CMP-03, CMP-04, CMP-05, LIN-02, LIN-04, LIN-05, LIN-06, INS-02 |
| Siap sebagian | 15 | KEP-02, KEP-08, KEP-10, MNT-05, MNT-09, DAT-04, CMP-06, CMP-07, LIN-01, LIN-03, LIN-07, INS-01, INS-03, INS-04, INS-05 |
| Rancangan | 1 | KEP-04 |
```

### D. Slot alarm otomatis dan keputusan akhir pada berkas hasil

```
$ grep -n 'auto_critical_alarm_slots' scratch/v9_i1/v9_i1_RESULTS.json
1414:    "auto_critical_alarm_slots": 0,
$ grep -n 'keputusan_akhir' scratch/v9_i1/v9_i1_RESULTS.json | head -3
1415:    "keputusan_akhir": "MANUSIA (insinyur pengeboran), tidak ada output otomatis yang memicu tindakan tanpa konfirmasi"
1758:  "keputusan_akhir": "MANUSIA, alat ini menyiapkan status, peringatan, tren, dan bahan rencana inspeksi"
```

Catatan pemotongan: tanda pisah panjang pada dua baris di atas diganti koma saat ditempel, dan itu
dinyatakan di sini supaya pembaca yang menjalankan `grep` sendiri tidak mengira ada nilai yang
disembunyikan. Nilai teksnya tidak diubah selain karakter itu. Baris 1415 dan 1758 pada berkas asli
memuat U+2014, dan dua karakter itulah yang diganti.

### E. Aritmetika yang dipakai pada bagian 3 dan bagian 5

```
$ sed -n '1554,1555p' planning/01_KATALOG_FITUR.md
**Masukan.** Daftar berkas belum diparse: F-1 C 2.156 dan F-11 1.750, total 3.906 atau 54,6 persen
dari 7.150 ([D0] baris 49; [PM6] baris 225; [I1] bagian 14.C).
```

Pemeriksaan: 2.156 ditambah 1.750 sama dengan 3.906. 3.906 dibagi 7.150 sama dengan 0,54629, yaitu
54,6 persen. Kedua hasil itu sama dengan yang tertulis pada baris di atas.

### F. Pemeriksaan berkas ini sendiri

```
$ grep -cP '\x{2014}' planning/11_PRIORITAS_BUILD.md
0
$ grep -cP '\x{2013}' planning/11_PRIORITAS_BUILD.md
0
$ grep -c -iE 'tidak [b]isa|tidak [m]ungkin|terbata[s]' planning/11_PRIORITAS_BUILD.md
0
$ find planning -maxdepth 1 -type f ! -name '*.md' | wc -l
0
```

Pola pada baris ketiga ditulis dengan kelas karakter, bukan kata utuh, dengan satu alasan: pola yang
memuat kata utuh akan menghitung barisnya sendiri dan memberi hasil 1 pada berkas yang bersih.
Jebakan itu sudah tercatat sebagai cacat 1 pada [AUD] baris 217 sampai 223, dan di sini dicegah
dengan cara yang sama seperti [AUD] baris 221 sampai 223 menyarankan rumusan ulang syarat.

### G. Hitung baris tabel dokumen ini

```
$ grep -c '^|' planning/11_PRIORITAS_BUILD.md
151
$ grep -c '^Jumlah baris data tabel di atas:' planning/11_PRIORITAS_BUILD.md
6
```

Dua angka pada butir G diukur pada berkas yang sudah selesai, bukan pada draf. Urutannya penting:
berkas ditutup dulu, baru dihitung, lalu angka dimasukkan. Memasukkan angka lebih dulu berarti
mengulang cacat 6 audit, yaitu mencetak ukuran yang basi di dalam dokumen yang memuatnya. Ukuran
byte dan jumlah baris berkas ini sendiri sengaja tidak dicetak di sini dengan alasan yang sama, dan
dilaporkan di komentar kartu.

---

## 12. Penutup yang bisa diperiksa

Pembaca yang ingin mengulang dokumen ini cukup menjalankan enam hal: `stat` pada lima berkas masukan,
`grep -c` pada tabel ringkasan katalog, `sed -n '2595,2599p'` pada tabel status katalog, `grep -n`
pada `auto_critical_alarm_slots` dan `keputusan_akhir`, `sed -n '1554,1555p'` pada baris antrean
parse, dan `grep -cP` untuk tanda pisah pada berkas ini sendiri. Seluruh angka pada dokumen ini
berasal dari enam hal itu, dan tidak ada satu angka pun yang ditulis dari ingatan.

Tiga keputusan dokumen ini, diringkas dalam tiga baris. Gelombang 1 berisi 32 fitur dan vonisnya
LAYAK. Gelombang 2 berisi 13 fitur dan vonisnya LAYAK dengan syarat. Gelombang 3 berisi 3 fitur dan
vonisnya PERLU PERBAIKAN, dengan syarat buka yang sudah ditulis. Paket seluruhnya berstatus PERLU
PERBAIKAN sampai enam cacat audit ditutup, dan tidak satu pun dari enam itu mengubah angka atau
menggeser ambang.
