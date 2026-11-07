# 00 INVENTARIS V3-V6: vonis era kelayakan data menjadi calon fitur

Kartu: `t_69e694aa` (ARKOLOG V3-V6) · Board: `fitur-v9-swarm` · Tanggal: 2026-10-31 (WIB)
Workspace: `/mnt/d/Capstone 1(v2)`
Sifat dokumen: INVENTARIS. Dokumen ini tidak menjatuhkan vonis baru, tidak menjalankan model, dan
tidak mengubah angka sumber. Tugasnya satu: membaca vonis V3 sampai V6, lalu mengubah keputusan
yang mati menjadi calon fitur yang bisa dibangun.

Cara membaca: setiap angka diikuti rujukan berkas dan nomor baris dalam tanda kurung. Kode
singkat berkas ada di bagian 1. Keluaran perintah yang saya jalankan sendiri untuk memeriksa
angka ditempel apa adanya di bagian 14.

---

## 0. Kerangka wajib (dipakai apa adanya, tidak diubah)

1. Alarm otomatis BUKAN tujuan. ML dipakai sebagai sistem pendukung keputusan dengan skor
   keyakinan, bukan pemutus. Konsekuensi: setiap fitur di bawah menampilkan angka keyakinan dan
   batas pemakaiannya pada layar yang sama.
2. Setiap angka wajib punya sumber berkas dan baris, atau baris ledger
   `docs/RND_PROVENANCE_LEDGER.md`. Catatan penting: ledger itu tidak memuat baris untuk dokumen
   V3 sampai V6 (hasil `grep` di bagian 14.I kosong), sehingga seluruh rujukan di dokumen ini
   memakai berkas dan nomor baris dokumen sumber, bukan baris ledger.
3. Tidak ada klaim "berjalan" tanpa bukti. Angka yang saya hitung ulang ditempel keluarannya di
   bagian 14.
4. Kekurangan data dikemas menjadi fitur berguna (pola Dynamic Island), bukan keluhan. Contoh
   penerapan: sumur yang belum punya kanal label tidak disembunyikan, tetapi tampil sebagai kartu
   kesiapan dengan daftar berkas yang sudah ada dan yang masih perlu diunduh.
5. Setiap fitur punya lima field wajib: pengguna, momen pakai, masukan, keluaran, status bukti.
6. Tidak ada kalimat penutup yang menutup jalan. Bila sesuatu belum tersedia, yang ditulis adalah
   syarat yang dibutuhkan (bagian 12).
7. Keluaran hanya markdown di `planning/`. Tidak ada berkas .py, .html, .json, atau .csv sebagai
   deliverable kartu ini. Skrip verifikasi sementara ditulis di luar `planning/` dan hanya dipakai
   untuk menghasilkan keluaran di bagian 14.
8. Tidak memakai tanda pisah panjang. Rentang angka ditulis dengan tanda hubung biasa.

---

## 1. Berkas yang dibuka dan ukuran byte

Ukuran dan jumlah baris diambil dari `wc -c -l` pada 2026-10-31 (keluaran penuh di bagian 14.A).

| Kode | Berkas | Byte | Baris |
|---|---|---:|---:|
| [V3A] | `docs/V3_DATA_ACQUISITION_INVENTORY.md` | 17.514 | 205 |
| [V3T] | `docs/V3_TS_FEATURES.md` | 8.429 | 132 |
| [V3W] | `docs/V3_WITSML_PARSE_REPORT.md` | 3.346 | 55 |
| [V4] | `docs/V4_MAINTENANCE_ML_OPTIONS.md` | 14.334 | 168 |
| [PM6] | `docs/V6_PM_VERDICT.md` | 26.032 | 338 |
| [D0] | `docs/V6_D0_READERS_SYNTHESIS.md` | 19.871 | 203 |
| [A1] | `docs/V6_A1_DATA_AUDIT.md` | 28.138 | 302 |
| [E1] | `docs/V6_E1_PREREG.md` | 12.738 | 189 |
| [RD0] | `docs/RND_D0_DATA_FEASIBILITY.md` | 28.196 | 401 |
| | **Total 9 berkas** | **158.598** | **1.993** |

Sembilan berkas dibuka penuh, bukan sebagian. Di luar sembilan itu, lima artefak data ikut dibuka
untuk memeriksa angka: `data/predictive/features_timeseries.npz` (458.129 B),
`features_timeseries_meta.json`, `features_timeseries_events.csv` (662 baris),
`data/volve/witsml_parsed/*.csv` (10 berkas), `data/USROP_labeled.csv`, dan
`data/witsml/Norway-NA-15_47_9-F-9 A time.csv` (427.910.797 B).

---

## 2. Vonis sembilan dokumen dalam satu kalimat

### 2.1 [V3A] Inventaris akuisisi data

**Vonis.** Akuisisi berhasil sebagian lalu blokirnya pecah: 88 berkas sekitar 103 MB dari mirror
publik (28 berkas SPWLA, 4 berkas Kaggle, 56 XML WITSML) ditambah unduhan penuh lewat Databricks
workspace kedua sebanyak 17.368 berkas dan 3,32 GB dengan audit hilang=0 dan ukuran_salah=0
([V3A] baris 11, 37, 182-184).

**Angka kunci.** 10 dari 10 wellbore target tercakup log petrofisik (baris 17); katalog target
berisi 175 bhaRun, 16 mudLog, 253 LAS, 468 DLIS (baris 78); WITSML Realtime 11.894 berkas 2,91 GB
untuk 27 wellbore, Well_technical_data 5.474 berkas 0,41 GB, zip Realtime 2,88 GB berisi 20.086
entri (baris 185).

**Yang mati.** DLIS dan LIS belum diparse saat dokumen ditulis karena `dlisio` belum ada (baris
197). Blokir ini kemudian ditutup [D0]: 20 dari 20 DLIS plus 1 LIS terbaca, 309.644 baris
([D0] baris 50). Sisa yang masih terbuka: klaim byte-identik dengan berkas Equinor di Databricks
belum diuji (baris 163), Zenodo/figshare/OSF belum dicek (baris 165).

### 2.2 [V3T] Fitur time-series pra-event

**Vonis.** Terbangun dan terverifikasi: 661 event dikali 480 fitur, anti-leakage 4.274.005 baris
dipindai dengan 0 pelanggaran, verifier jalur kode berbeda 8 dari 8 PASS ([V3T] baris 4-5,
100-104).

**Angka kunci.** Aritmetika coverage 884 label dikurangi 213 tanpa CSV dikurangi 10 out-of-range
sama dengan 661 event (baris 39-44); 16 kanal kanonik, 14 kanal tersedia di 7 dari 7 fold
sedangkan RPM 6 dari 7 dan MDOA 5 dari 7 (baris 65-68); median gap antar sampel 4,9 detik dengan
median baris 379, 1.515, dan 4.549 untuk jendela 30 menit, 2 jam, dan 6 jam (baris 89).

**Yang mati.** 213 label F-15 B/C/D tanpa fitur karena folder WITSML-nya tidak diparse (baris
39-41, 129); 10 event di luar rentang data (baris 42-43); 185 event punya jendela kosong di ketiga
panjang jendela, dengan 191 kosong pada jendela 2 jam (baris 108); fraksi NaN fitur sensor 0,368
pada jendela 2 jam (baris 109).

### 2.3 [V3W] Laporan parse WITSML

**Vonis.** Parse bersih: 20.086 berkas dari zip 2,88 GB dengan gagal=0, menghasilkan 8 CSV berisi
7.080.457 baris dengan `errors: []` di semua QC ([V3W] baris 4, 20, 26).

**Angka kunci.** 60 sampai 281 kanal per sumur, hanya 37 sampai 48 kanal yang fill rate-nya 50
persen atau lebih, sehingga ambang 50 persen dipakai sebagai aturan seleksi (baris 41). Semua
sumur berakhir pada 2015-09-22 sesuai batas dataset Volve (baris 28).

**Yang mati.** Pemetaan wellbore ke label salah untuk tiga sumur: F-15_S matched=0, F-15A
matched=357 padahal labelnya 32, F-9 matched=150 padahal labelnya 56 (baris 34-37). Validasi nilai
fisik (outlier dan satuan) belum dilakukan, duplikat timestamp belum dihitung, dan zona waktu
belum disilang dengan jam operasi CET (baris 45-48).

### 2.4 [V4] Opsi ML maintenance

**Vonis.** Tiga opsi disimpan dan belum dieksekusi, dengan angka audit yang sudah dikoreksi: union
seluruh sumur 275 kolom tetapi hanya 29 kolom tersedia di ketujuh sumur ([V4] baris 13, 17).

**Angka kunci.** 429.520 baris mentah lintas 7 berkas (baris 17); `MWD Shock Risk` hanya 26 baris
non-nol sehingga tidak layak (baris 25); `STUCK_RT` hanya ada di 2 sumur, F-9A 1.221 baris dengan
510 non-nol dan F-14 3.223 baris dengan 118 non-nol (baris 34-35); gabungan seluruh kolom getaran
memberi 6.927 baris dengan prevalensi 0,4 sampai 6,4 persen (baris 43); TSPP 4 berkas 52.905 baris
(baris 56).

**Yang mati.** Klaim bahwa getaran bisa diprediksi dari sensor permukaan belum terbukti: AUPRC
rata-rata 0,0333 terhadap prevalensi 0,0245 sama dengan lift 1,36, dan ROC-AUC di bawah 0,5 pada
tiga sumur (baris 68-80). Enam kolom getaran berasal dari enam alat berbeda yang aktif di kedalaman
berbeda, sehingga tidak boleh dihitung sebagai enam jenis kerusakan (baris 41-43). Label keausan
bit tidak ada karena `dullingInfo`, `dullGrade`, dan `bitName` kosong, sedangkan bhaRun hanya
memberi interval run (baris 62). Artefak autoencoder TSPP tidak boleh dikutip karena tidak
terdokumentasi dan tidak diskriminatif (baris 58).

### 2.5 [PM6] Vonis PM V6

**Vonis.** SAH pada pembacaan literal pra-registrasi: tiga kelas lolos gate G1 ditambah G2 dan
taksonomi tujuh kelas berpenduduk terverifikasi, dengan batasan mengikat bahwa pembacaan ketat
hanya menghasilkan dua kelas LULUS penuh ([PM6] baris 25-28, 130-141).

**Angka kunci.** Tujuh kelas dengan populasi terhitung: torsional 82.530, moderate stick-slip 320,
shock 180, whirl 714, stuck 394, hidraulik 58.317, ditambah lima kelas USROP (baris 164-167).
Uji beda jenis: phi antara vib dan ssi 0,0247, Jaccard 0,0174 pada 15.776 jendela co-valid (baris
170-171). Distribusi label USROP yang benar 134.013, 49.732, dan 15.183 dari n=198.928 (baris 91).

**Yang mati.** Tiga kelas dengan LULUS penuh (baru dua), empat kelas atau lebih lolos gate ML,
dan klaim "tiga detektor siap pakai" (baris 183-185). Enam kelompok angka dilarang dikutip sebelum
dipatch: 947/3.539/130 untuk EDM, 16.671 dan 152 untuk D1h, 49.629 sebagai bagian satu distribusi,
2.987 untuk azi, 60.504 baris per berkas, dan 14 kolom XAI (baris 188-190).

### 2.6 [D0] Sintesis delapan pembaca

**Vonis.** Delapan pembaca membuka berkas primer dan seluruh klaim jumlah berkas serta jumlah baris
cocok dengan hitung ulang aggregator, sedangkan klaim besarnya satu: EDM bukan basis data event
([D0] baris 17-31, 77-88).

**Angka kunci.** 192 tubular, 161 bhaRun, 63 trajectory, 27 wbGeometry, 8 mudLog, 7.150 log XML,
20 DLIS dan 2 LIS (baris 17-22); 1.392 komponen tubular (baris 45); 5.561 stasiun survey dengan
80,1 persen baris bisa dikoreksi MD ke TVD (baris 47); 2.882 interval litologi 100 persen terisi
(baris 48); F-1 C 2.156 ditambah F-11 1.750 sama dengan 3.906 berkas atau 54,6 persen belum
diparse (baris 49); 409 formation picks di 35 wellbore (baris 52).

**Yang mati.** EDM sebagai label kegagalan ditolak dengan bukti: lima kata kunci bernilai 0, dan
`stuck` maupun `kick` hanya atribut simulasi serta bit (baris 51, 77-88). WHIRL_RT identik dengan
BOUNCE_RT pada 1.790 dari 1.790 baris sehingga tidak boleh jadi dua kelas (baris 174). Rating
motor absen di 0 dari 192 berkas sehingga indeks torsi di lubang bawah tetap terblokir (baris 45,
172). Gas show mudLog hanya 17 dari 576 sehingga terlalu jarang untuk target (baris 48).

### 2.7 [A1] Audit data

**Vonis.** Delapan dari delapan pembaca benar-benar membuka berkas, 50 lebih klaim diverifikasi
ulang, dan audit menemukan lima angka tidak akurat, tiga angka tidak tereproduksi, serta satu
label sirkular penuh ([A1] baris 26-30).

**Angka kunci.** Uji sirkularitas memakai decision tree tanpa batas depth dengan split 75/25:
label litologi holdout 66,3 persen (non-sirkular), `STUCK_RT` time.csv holdout 92,1 persen
(non-sirkular), flag CARB_FLAG dan COAL_FLAG holdout 97,7 dan 99,9 persen (sirkular bersyarat),
label rule R1 dan USROP holdout 99,97 persen dengan R kuadrat rekonstruksi MSE 0,99987 (sirkular
penuh) (baris 198-204). `flowrateMx` ada di 9 berkas sedangkan rating motor 0 dari 192 (baris 58).

**Yang mati.** Melatih fitur USROP untuk memprediksi label rule USROP dinyatakan terlarang karena
model hanya akan mereproduksi rule (baris 206-208). Angka EDM 947/3.539/130 tidak tereproduksi
dengan enam metode berbeda, nilai terukur 945-968, 3.193-5.103, dan 41-370 bergantung metode
(baris 121, 256-259).

### 2.8 [E1] Pra-registrasi ML

**Vonis.** Gate, fitur, model, metrik, dan protokol dikunci sebelum hasil, dengan hash tercatat
sebelum training dan larangan menggeser gate ([E1] baris 3-7, 151-160).

**Angka kunci.** 11 kanal permukaan dikali 5 statistik sama dengan 55 fitur (baris 110-113);
jumlah jendela per kelas: stuck 2.007 dari 5.555, vib 5.429 dari 23.922, shk 1.642 dari 43.191,
ssi 363 dari 24.480 (baris 75); gate per kelas lift minimal 1,5 pada mayoritas sumur layak dinilai
ditambah AUPRC RF minimal sama dengan canary kedalaman (baris 151-155); ambang layak dinilai 30
jendela positif per sumur uji (baris 149-150).

**Yang mati.** Kelas hidraulik dari residual SPP dibuang karena sirkular terhadap fitur (baris
103-105); STKSLP dibuang karena semantiknya tidak terdokumentasi dan 98,7 persen non-nol di F-15_S
(baris 100); severe stick-slip dengan SSI 3 atau lebih tidak dijadikan kelas karena populasinya
kecil (baris 102); sumur F-9 gugur untuk kelas stuck dan vib karena nol jendela fitur pengeboran
(baris 167-170); semantik kode `STUCK_RT` 0/1/2/3 tidak terdokumentasi sehingga kelas stuck adalah
flag instrumen, bukan kejadian fisik terverifikasi naratif (baris 173-175).

### 2.9 [RD0] Kelayakan data per algoritma

**Vonis.** Enam dataset engine terukur dengan 2 sampai 9 sumur dan prevalensi 1,67 sampai 36,13
persen, dan dekomposisi frekuensi ternyata tidak layak karena laju sampel tertinggi 0,3333 Hz
([RD0] baris 30-35, 159, 388).

**Angka kunci.** Nyquist tertinggi 0,1667 Hz sedangkan VIBLAT_RT di F-14 hanya 0,0167 Hz (baris
159, 364); state Markov tersedia untuk STUCK 4 sumur, SHKRSK 9 sumur, dan VIBLAT 6 sumur menurut
tabelnya sendiri (baris 183-211); baseline bersih gabungan 8.991 sampai 77.604 menit (baris 288-302);
USROP 198.928 baris dengan 49.732 high_MSE (baris 311-315); tool wear 469 jendela dengan 27 fitur
dan 4 alat (baris 336-341).

**Yang mati.** VMD, EMD, dan wavelet berkategori TIDAK ADA kelayakan datanya (baris 356-369, 389);
label regime untuk data rig tidak ada, label regime hanya ada di data bengkel (baris 179);
`GAINLOSSTOT` tidak ditemukan di 9 sumur terparse dan data pit hanya satu sumur (baris 349-352);
horizon survival yang tersedia hanya 10 menit (baris 228, 362).

---

## 3. Hitungan silang yang saya jalankan (temuan baru dari kartu ini)

Bagian ini bukan rangkuman. Ini hasil perhitungan ulang yang saya jalankan pada 2026-10-31 untuk
menguji angka antar dokumen. Keluaran mentah ada di bagian 14.

**3.1 Angka 7.080.457 tereproduksi persis, tetapi direktori sudah berisi 10 CSV, bukan 8.**
`wc -l` atas `data/volve/witsml_parsed/*.csv` memberi 9.935.708 baris untuk 10 berkas, jadi
9.935.698 baris data. Dikurangi F-10 sebanyak 773.674 dan F-12 sebanyak 2.081.567, sisanya
7.080.457, sama persis dengan klaim [V3W] baris 20. Artinya [V3W] dan [V3T] benar untuk era 8
berkas, dan dua sumur F-10 serta F-12 adalah tambahan era V9. Konsekuensi untuk fitur: peta
cakupan sumur harus menyebut versi parser, bukan hanya nama sumur.

**3.2 Jumlah baris di [E1] baris 59 selisih 59.500 dari hitungan saya.**
[E1] menulis 7 CSV berisi 6.961.468 baris. Penjumlahan `wc -l` tujuh CSV yang sama (F-14, F-15A,
F-15_S, F-5, F-7, F-9, F-9_A) memberi 7.020.968 baris data, selisih 59.500. Angka 59.500 hampir
sama dengan 59.489 baris `VAR_F-5_alt`, sehingga dugaan terkuat adalah salah kurung saat
penulisan, bukan data hilang. Status: belum dijelaskan oleh dokumen mana pun, dicatat sebagai
selisih terbuka, dan angkanya tidak dipakai di dokumen ini kecuali sebagai catatan.

**3.3 Matriks kanal label per sumur, hasil pemindaian header saya.**
Pemindaian `head -1` atas 10 CSV terparse memberi hasil ini (keluaran 14.D):

| Kanal label | Sumur yang punya | Jumlah |
|---|---|---:|
| `STUCK_RT` | F-10, F-14, F-9, F-9_A | 4 |
| `VIBLAT_RT` | F-10, F-14, F-15A, F-15_S, F-5, F-9 | 6 |
| `SHKRSK_RT` | F-10, F-12, F-14, F-15A, F-15_S, F-5, F-7, F-9, F-9_A | 9 |
| `CRPM_RT` | F-10, F-12, F-14, F-15A, F-15_S, F-5, F-7, F-9, F-9_A | 9 |

`VAR_F-5_alt` tidak punya satu pun dari empat kanal itu. Hasil ini cocok dengan [RD0] baris 183-211
untuk STUCK dan SHKRSK, tetapi berbeda satu sumur untuk VIBLAT: ringkasan [RD0] baris 211 dan 390
menyebut 7 sumur, sedangkan tabel [RD0] baris 98-104 dan pemindaian saya menunjukkan 6 sumur
(F-10, F-14, F-15A, F-15_S, F-5, F-9). Angka yang terverifikasi adalah 6.

**3.4 Matriks fitur yang sudah ada terverifikasi dari artefaknya.**
`features_timeseries.npz` berukuran 458.129 B, berisi X dengan bentuk 661 kali 480 dan 480 nama
fitur. Semua fitur berawalan jendela: 160 untuk `w30m`, 160 untuk `w2h`, 160 untuk `w6h`. Jumlah
event yang seluruh fiturnya NaN: 194 pada `w30m`, 191 pada `w2h`, 185 pada `w6h`, dan irisan
ketiganya tepat 185. Sebaran per sumur pada `w2h`: F-9_A 82 dari 94, F-14 46 dari 182, F-9 30 dari
56, F-7 20 dari 58, F-15_S 11 dari 105, F-5 2 dari 134, F-15A 0 dari 32. Semua ini sama dengan
[V3T] baris 108. Meta anti-leakage mencatat `rows_scanned` 4.274.005 dengan `violations` 0 dan
`pass` true, sama dengan [V3T] baris 100. Meta coverage mencatat 884 label, 671 terpetakan, 213
tanpa fold (F-15 D 122, F-15 C 89, F-15 B 2), 10 di luar rentang (F-15_S 7, F-5 2, F-7 1), dan
661 fitur terbangun.

**3.5 Dua klaim ketiadaan yang saya uji ulang dengan grep sendiri.**
`find` atas `witsml_raw` memberi 192 berkas tubular dan 161 berkas bhaRun, sama dengan [D0] baris
17-18. `grep -l` untuk `torqueMax|Pmax|revPerGallon|rpmMax` pada 192 berkas tubular memberi 0
berkas, dan `grep -l` untuk `dullingInfo|dullGrade|bitName` pada 161 berkas bhaRun juga memberi 0
berkas. Dua klaim mati terbesar di era ini (rating motor dan label keausan) berdiri di atas bukti
yang bisa diulang siapa pun, bukan ingatan.

**3.6 `time.csv` dan `USROP_labeled.csv`.**
`wc -l` `data/witsml/Norway-NA-15_47_9-F-9 A time.csv` memberi 419.748 baris, jadi 419.747 baris
data, sama dengan [D0] baris 52 dan [A1] baris 130. Jumlah kolom dari `awk -F,` memberi 247,
sedangkan [A1] memakai `csv.reader` dan mendapat 239; selisih 8 berasal dari koma di dalam tanda
kutip yang ikut terhitung oleh pemisahan naif. Angka otoritatif tetap 239. `USROP_labeled.csv`
berisi 198.929 baris, jadi 198.928 baris data, sama dengan [V4] baris 17 dan [RD0] baris 311.

---

## 4. Peta keputusan mati ke calon fitur

| # | Keputusan yang mati | Sumber vonis | Yang sebenarnya hilang | Fitur penampung |
|---|---|---|---|---|
| 1 | 213 label F-15 B/C/D tanpa fitur | [V3T] 39-41, 129 | Berkas WITSML tiga wellbore belum diparse | F-03, F-06 |
| 2 | 10 event di luar rentang data | [V3T] 42-43 | Tidak ada kanal waktu sebelum data mulai | F-03 |
| 3 | 185 event punya jendela kosong | [V3T] 108 | Sumur sedang tidak logging saat event | F-01, F-02 |
| 4 | Kanal DEPT, ECD, SHKRSK, SHKTOT nol fold | [V3T] 73 | Fill rate di bawah 50 persen per sumur | F-04 |
| 5 | Pemetaan wellbore ke label salah di 3 sumur | [V3W] 34-37 | Nama sumur tidak unik, bukti harus struktural | F-03 |
| 6 | Validasi fisik dan duplikat timestamp belum ada | [V3W] 45-46 | Belum ada lapisan QC kanal | F-04 |
| 7 | DLIS belum diparse | [V3A] 197 | `dlisio` belum tersedia saat itu | F-08 |
| 8 | Rating motor 0 dari 192 berkas | [D0] 45, 172; [A1] 58 | Tag rating tidak pernah direkam | F-20 |
| 9 | Label keausan bit 0 dari 161 berkas | [D0] 46; [A1] 65 | `dullingInfo` tidak ada di sumber | F-18, F-20 |
| 10 | `STUCK_RT` hanya di sebagian sumur | [V4] 34-35; [RD0] 211 | Kanal tidak direkam di sumur lain | F-07 |
| 11 | `MWD Shock Risk` 26 baris non-nol | [V4] 25 | Hampir selalu nol sehingga tidak layak | F-15 |
| 12 | Enam kolom getaran dari enam alat | [V4] 41-43 | Bukan enam jenis kerusakan | F-15 |
| 13 | Prediktabilitas getaran lift 1,36 | [V4] 68-80 | Sinyal permukaan belum terbukti | F-11, F-12, F-15 |
| 14 | Label rule USROP sirkular penuh | [A1] 201 | Label adalah fungsi fitur | F-09 |
| 15 | Flag DLIS sirkular bersyarat | [A1] 200 | Nyaris deterministik antar kanal petro | F-09 |
| 16 | `bit_wear` konfuk kedalaman | [PM6] 178-180 | Kedalaman saja lolos gate di 3 dari 4 fold | F-12 |
| 17 | Lima angka salah dan tiga tak tereproduksi | [A1] 248-264; [PM6] 188-190 | Tidak ada gerbang provenance | F-10 |
| 18 | EDM bukan basis data event | [D0] 77-88 | Kata kunci hanya atribut simulasi | F-17 |
| 19 | 3.906 berkas log belum diparse (54,6 persen) | [D0] 49; [PM6] 225 | Parser lama hanya 8 wellbore | F-06, F-07 |
| 20 | WHIRL_RT identik BOUNCE_RT | [A1] 100; [D0] 174 | Dua mnemonic, satu kanal | F-15 |
| 21 | VMD, EMD, wavelet tidak layak | [RD0] 159, 364 | Nyquist 0,1667 Hz | F-14 |
| 22 | Label regime rig tidak ada | [RD0] 179 | Hanya data bengkel punya label regime | F-14 |
| 23 | Horizon survival hanya 10 menit | [RD0] 228, 362 | Belum ada dataset horizon jam | F-19 |
| 24 | `GAINLOSSTOT` tidak ada, pit satu sumur | [RD0] 349-352 | Kanal loss tidak terekam di WITSML | F-20 |
| 25 | Semantik `STUCK_RT` 0/1/2/3 tidak terdokumentasi | [E1] 173-175 | Deskripsi kurva kosong | F-07, F-13 |

---

## 5. Kelompok A: kelengkapan data dan event

| Fitur dan tujuan | Pengguna | Momen pakai | Masukan | Keluaran | Status bukti |
|---|---|---|---|---|---|
| **F-01 Kartu kelengkapan jendela pra-event.** Tujuan: memberi tahu operator seberapa layak satu event dinilai sebelum skor model dipakai, supaya skor rendah tidak dibaca sebagai sinyal fisik | Engineer PdM, supervisor pengeboran | Saat membuka satu event atau satu baris riwayat | `n_rows`, `gap_median_s`, `gap_max_s`, `full_window` per jendela dari `X_window_meta` ([V3T] 89, 110) | Empat label kelengkapan: penuh, sebagian, kosong, terpotong, plus jumlah baris dan gap terbesar | Kuat. Median gap 4,9 detik dan median baris 379, 1.515, 4.549 terverifikasi dokumen; 185 event kosong di ketiga jendela terverifikasi ulang dari npz (14.E) |
| **F-02 Kanal status "sumur tidak logging".** Tujuan: menjadikan ketiadaan data sebagai informasi operasional, bukan NaN yang diimputasi diam-diam | Driller, mudlogger, engineer data | Saat event masuk dengan jendela kosong, dan saat menyiapkan shift | Mask NaN per jendela dari `X`, daftar event dengan seluruh fitur NaN ([V3T] 108, 130) | Status "tidak ada logging" beserta rentang waktu kosong dan sumur terkait, bukan angka model | Kuat. Irisan kosong ketiga jendela 185, sebaran per sumur 82/46/30/20/11/2/0 terverifikasi ulang (14.E) |
| **F-03 Peta label ke fold dan antrean parse.** Tujuan: setiap label punya jejak boleh atau tidaknya masuk evaluasi, sehingga 213 label yang gugur bisa ditindak, bukan dilupakan | Auditor internal, ML engineer | Sebelum kampanye training, dan saat menjawab pertanyaan dosen tentang cakupan | `coverage` dari `features_timeseries_meta.json`: 884 label, 671 terpetakan, 213 tanpa fold (122/89/2), 10 di luar rentang (7/2/1) ([V3T] 39-44) | Tabel label dengan status terpetakan, tanpa fold, atau di luar rentang, plus jumlah event per sumur | Kuat. Angka diambil langsung dari meta artefak dan cocok dengan [V3T] (14.E) |
| **F-04 Pemilih kanal berbasis fill rate dan QC fisik.** Tujuan: mencegah kanal yang 50 persen kosong atau konstan dipakai sebagai bukti fisik | Engineer data, ML engineer | Saat menyusun fitur kampanye baru | Fill rate per kanal per sumur dari `_verify.json` dan `channel_resolution_per_fold` ([V3W] 41; [V3T] 62-73) | Daftar kanal lolos, kanal gugur beserta alasannya, dan penanda konstansi seperti `trend_rho` NaN | Kuat untuk seleksi (37 sampai 48 kanal lolos dari 60 sampai 281). Sedang untuk QC fisik karena validasi satuan dan outlier belum pernah dijalankan ([V3W] 45) |

---

## 6. Kelompok B: cakupan sumur dan sumber

| Fitur dan tujuan | Pengguna | Momen pakai | Masukan | Keluaran | Status bukti |
|---|---|---|---|---|---|
| **F-05 Matriks ketersediaan berkas per sumur.** Tujuan: menampilkan apa yang sudah dimiliki dan apa yang masih perlu diunduh untuk setiap sumur, sehingga keputusan pindah sumur berbasis bukti | Engineer PdM, peneliti | Sebelum memilih sumur untuk kampanye baru | Audit unduhan 17.368 berkas 3,32 GB dengan hilang=0 ([V3A] 182-184); 11.894 berkas WITSML 27 wellbore, 5.474 berkas teknis, 20.086 entri zip ([V3A] 185); `VOLVE_INVENTORY.xlsx` sebagai peta log per sumur ([V3A] 151) | Kartu per sumur: jumlah berkas per kategori, kanal label yang ada, status siap atau perlu unduh | Kuat. Audit byte-per-byte pihak terpisah dan hitungan header saya atas 7.150 log XML, 192 tubular, 161 bhaRun (14.C, 14.F) |
| **F-06 Antrean parse 3.906 berkas.** Tujuan: mengubah gap 54,6 persen menjadi pekerjaan terurut dengan proyeksi dampak, bukan catatan kaki | Peneliti, koordinator data | Saat merencanakan perluasan cakupan sumur | Daftar berkas belum diparse: F-1 C 2.156 dan F-11 1.750 ([D0] 49; [PM6] 225) | Antrean berisi jumlah berkas, perkiraan kanal, dan calon kelas yang terbuka bila selesai | Kuat. Hitungan `find` saya memberi 2.156 dan 1.750, total 3.906 = 54,63 persen dari 7.150 (14.C) |
| **F-07 Katalog label instrumen per sumur.** Tujuan: menampilkan sumur mana punya label apa, sehingga klaim lintas sumur selalu disertai jumlah sumur yang benar | Auditor, ML engineer, dosen penguji | Saat membaca hasil LOWO, saat memilih sumur uji | Pemindaian header 10 CSV terparse ([V4] 34-35; [RD0] 183-211) | Matriks sumur kali kanal label dengan jumlah sumur: STUCK 4, VIBLAT 6, SHKRSK 9, CRPM 9 | Kuat. Hasil scan saya sama dengan tabel [RD0], dengan satu koreksi: VIBLAT 6 sumur, bukan 7 (14.D) |
| **F-08 Panel litologi dan stratigrafi.** Tujuan: menyediakan konteks geologi non-sirkular sebagai label bantu, supaya model tidak membaca formasi sebagai kerusakan | Geolog, engineer drilling | Saat menafsirkan satu episode, saat menyiapkan fitur konteks | 2.882 interval litologi 100 persen terisi ([D0] 48), 409 formation picks di 35 wellbore ([D0] 52), 309.644 baris petro dari 20 DLIS dan 1 LIS ([D0] 50) | Profil litologi per kedalaman beserta kode formasi, siap dipakai sebagai label bantu atau satu-hot | Kuat. Uji non-sirkular holdout 66,3 persen membuktikan litologi gagal direkonstruksi dari parameter drilling ([A1] 198) |

---

## 7. Kelompok C: kejujuran label dan angka

| Fitur dan tujuan | Pengguna | Momen pakai | Masukan | Keluaran | Status bukti |
|---|---|---|---|---|---|
| **F-09 Gerbang anti-ghost.** Tujuan: menolak kandidat label yang bisa direkonstruksi hampir sempurna dari fiturnya sendiri, supaya model tidak hanya mereproduksi rumus | ML engineer, auditor | Sebelum kampanye, sebagai syarat masuk daftar fitur | Uji decision tree tanpa batas depth dengan split 75/25 pada pasangan label dan fitur ([A1] 194-204) | Status lolos atau gugur beserta akurasi holdout: 66,3 persen litologi, 92,1 persen `STUCK_RT`, 97,7 dan 99,9 persen flag petro, 99,97 persen rule USROP | Kuat. Angka holdout dan R kuadrat 0,99987 terukur, dan larangan turunannya sudah tertulis di [A1] 206-208 |
| **F-10 Gerbang provenance angka.** Tujuan: menandai angka mana yang boleh dikutip dan mana yang harus dihitung ulang, sehingga tidak ada angka salah masuk slide | Penulis laporan, PM, pembicara | Sebelum menyusun slide atau bab, saat menerima angka dari dokumen lain | Daftar temuan audit: 5 angka salah, 3 tak tereproduksi, 1 generalisasi ([A1] 248-264); daftar larangan kutip ([PM6] 188-190) | Label tiga warna per angka: sah, sah dengan catatan metode, dilarang sampai dihitung ulang | Kuat. Contoh terukur: EDM 947/3.539/130 tidak tereproduksi, nilai terukur 945-968, 3.193-5.103, 41-370 ([A1] 256-259) |
| **F-11 Kartu dua pembacaan dengan skor keyakinan.** Tujuan: satu klaim ditampilkan pada dua pembacaan sekaligus (literal dan ketat) beserta selisihnya, supaya tidak ada klaim yang tampil lebih kuat dari buktinya | Dosen penguji, PM, operator | Saat sesi bimbingan dan saat sidang | Vonis [PM6] 130-141 ditambah angka gate [E1] 151-160 | Satu kartu: pembacaan literal 3 kelas, pembacaan ketat 2 kelas, selisih 1 kelas, plus kalimat pembatas wajib | Sedang. Kedua pembacaan tertulis dan berangka, tetapi skema skor keyakinan belum diuji daya pisahnya |

---

## 8. Kelompok D: pembanding dan kelayakan

| Fitur dan tujuan | Pengguna | Momen pakai | Masukan | Keluaran | Status bukti |
|---|---|---|---|---|---|
| **F-12 Panel pembanding berpasangan.** Tujuan: setiap skor model selalu tampil bersama baseline terkuatnya, supaya angka model tidak dibaca sebagai kemampuan tanpa pembanding | Auditor, ML engineer, dosen | Saat membaca hasil, saat memutuskan naik tingkat | Skor RF, persistence jendela sebelumnya, dan canary kedalaman pada fold yang sama ([E1] 138-144); temuan persistence menang 4 dari 4 fold pada bit_wear ([PM6] 178-180) | Tiga batang per fold: RF, persistence, canary kedalaman, plus status menang atau kalah | Kuat. Persistence mengalahkan RF 4 dari 4 fold dan kedalaman saja lolos gate 3 dari 4 fold, tercatat di vonis PM |
| **F-13 Badge kelayakan fold.** Tujuan: menandai fold yang jumlah positifnya kurang dari 30 sebagai UNDERPOWERED, supaya kesimpulan per sumur tidak ditarik dari sampel kecil | ML engineer, auditor | Saat evaluasi per kelas | Jumlah jendela positif per sumur ([E1] 66-75, 149-150) | Badge layak atau underpowered per sumur, plus jumlah positif dan lebar CI bootstrap | Sedang. Ambang 30 positif adalah konvensi pra-registrasi yang tertulis, efeknya ke CI belum diukur per fold |
| **F-14 Panel kesiapan algoritma per sumur.** Tujuan: menampilkan algoritma mana yang masuk akal untuk satu sumur berdasarkan laju sampel, ketersediaan state, dan horizon, supaya metode tidak dipilih dari selera | Peneliti, pembimbing | Saat memilih metode untuk kartu riset baru | Laju sampel dan Nyquist ([RD0] 159), ketersediaan state ([RD0] 183-211), horizon 10 menit ([RD0] 228) | Untuk setiap sumur: daftar metode siap, metode dengan syarat, dan metode di luar kelayakan data | Kuat. Nyquist 0,1667 Hz dan VIBLAT F-14 0,0167 Hz terukur; tabel state per sumur terverifikasi kecuali satu koreksi VIBLAT (14.D) |

---

## 9. Kelompok E: fisika kanal dan validitas

| Fitur dan tujuan | Pengguna | Momen pakai | Masukan | Keluaran | Status bukti |
|---|---|---|---|---|---|
| **F-15 Indeks kondisi getaran enam alat.** Tujuan: menyatukan enam kolom getaran dari enam alat berbeda menjadi satu indeks kondisi per interval, bukan enam kelas palsu | Engineer PdM, driller | Saat memantau satu run, saat menyiapkan laporan kondisi BHA | Union kolom getaran 6.927 baris dengan prevalensi 0,4 sampai 6,4 persen ([V4] 43); peta alat aktif per kedalaman ([V4] 41); larangan WHIRL dan BOUNCE sebagai dua kanal ([A1] 100) | Satu garis indeks kondisi per kedalaman beserta alat mana yang aktif, dengan penanda tumpang tindih | Sedang. Union 6.927 baris dan 1.790 dari 1.790 identik terukur; daya prediksi permukaan masih lift 1,36 sehingga indeks ini deskriptif, bukan prediktif |
| **F-16 Validitas kedalaman MD ke TVD.** Tujuan: memastikan setiap fitur berbasis tekanan memakai kedalaman vertikal yang benar, karena kesalahan MD terhadap TVD mencapai 16 persen di F-14 dan 43 persen di F-10 | Engineer drilling, analis hidraulik | Sebelum menjalankan fitur hidraulik atau tekanan pori | 5.561 stasiun survey dari 63 trajectory ditambah 27 wbGeometry ([D0] 47); 5.669.005 dari 7.080.457 baris bisa dikoreksi ([A1] 78) | Kolom TVD per baris time-series beserta status terkoreksi atau tidak, dan ringkasan cakupan 80,1 persen | Kuat. Kedua angka, 7.080.457 dan 5.669.005, dihitung ulang auditor dengan tool berbeda ([A1] 78) |
| **F-17 Profil tekanan pori dan fraktur dari EDM.** Tujuan: memakai EDM pada perannya yang benar, yaitu fitur jendela operasi, bukan label kegagalan | Engineer well engineering, peneliti | Saat menyiapkan fitur konteks per kedalaman | 39.084 `CD_PORE_PRESSURE`, 37.257 `CD_FRAC_GRADIENT`, 15.109 stasiun survey definitif, 10.650 `CD_ASSEMBLY_COMP` ([A1] 122) | Kurva pore dan frac per kedalaman dengan filter `phase=ACTUAL`, dipakai sebagai jendela operasi | Sedang. Delapan hitungan tag cocok persis; pemakaian sebagai fitur belum pernah dijalankan di kampanye mana pun |

---

## 10. Kelompok F: umur peralatan dan horizon

| Fitur dan tujuan | Pengguna | Momen pakai | Masukan | Keluaran | Status bukti |
|---|---|---|---|---|---|
| **F-18 Time-to-pull dari interval bhaRun.** Tujuan: memberi perkiraan jarak ke pencabutan bit berbasis interval run nyata, bukan keausan fisik yang tidak pernah diukur | Engineer PdM, supervisor rig | Saat menyusun program run berikutnya | 161 bhaRun dengan 114 `dTimStop` dan 9 drilling window lengkap ([D0] 46); 15 `dTimStartDrilling` dan 10 `dTimStopDrilling` ([A1] 66); 1.392 komponen tubular ([D0] 45) | Distribusi durasi run per formasi dan per tipe string, dipakai sebagai pembanding program | Sedang. Sebaran interval terukur, tetapi populasi 9 drilling window terlalu kecil untuk model; 6 run durasi negatif wajib difilter ([D0] 176) |
| **F-19 Panel waktu sejak onset dan horizon.** Tujuan: menampilkan umur episode dan horizon yang benar-benar tersedia, supaya tidak ada klaim prediksi jam atau hari | Driller, supervisor, peneliti | Saat membaca status episode yang sedang berjalan | Jumlah onset per sumur 55 sampai 93 untuk stuck ([RD0] 219-222); horizon 10 menit ([RD0] 228); episode tertinggi shk F-9_A 4 dan F-9 10 ([RD0] 228) | Waktu berjalan sejak onset, jumlah episode, dan penanda bahwa horizon yang sah 10 menit | Sedang. Onset dan horizon terukur, tetapi model survival dengan banyak kovariat belum diuji daya pisahnya |
| **F-20 Kartu permintaan data bertanda tangan.** Tujuan: mengubah tiga ketiadaan yang terbukti (rating motor, label keausan, kanal loss) menjadi daftar permintaan data yang spesifik, bukan kalimat penutup | Koordinator data, pembimbing | Saat rapat data, saat mengajukan akses baru | 0 dari 192 berkas punya rating motor ([A1] 58); 0 dari 161 berkas punya `dullingInfo` ([A1] 65); `GAINLOSSTOT` tidak ada di 9 sumur ([RD0] 349) | Daftar tag yang diminta, berkas target, pihak pemilik data, dan dampak bila terpenuhi (indeks torsi lubang bawah, label keausan, deteksi loss) | Kuat. Ketiga klaim ketiadaan diuji ulang dengan grep sendiri pada 2026-10-31 (14.F) |

---

## 11. Sebaran status bukti

| Status bukti | Jumlah fitur | Fitur |
|---|---:|---|
| Kuat (angka terukur dan terverifikasi minimal dua jalur) | 14 | F-01, F-02, F-03, F-04, F-05, F-06, F-07, F-08, F-09, F-10, F-12, F-14, F-16, F-20 |
| Sedang (angka ada, efek ke keputusan belum diukur) | 6 | F-11, F-13, F-15, F-17, F-18, F-19 |

Dua catatan penilaian. F-04 berstatus kuat pada sisi seleksi kanal (37 sampai 48 kanal lolos dari
60 sampai 281), sedangkan sisi QC fisiknya belum dijalankan sehingga bagian itu ikut belum terukur.
F-15 berstatus sedang karena angkanya kuat sebagai deskripsi (6.927 baris union, 1.790 dari 1.790
identik) tetapi lemah sebagai prediksi (lift 1,36 pada uji [V4]).

Catatan pembacaan: tidak ada fitur di daftar ini yang bergantung pada lapisan B (kinerja operasional
FAR dan B1), karena V3 sampai V6 memang belum mengukur lapisan itu. Konsekuensi yang harus tampil
di layar: setiap fitur di atas adalah alat baca dan alat tanya, bukan pemicu tindakan otomatis.
Pola Dynamic Island dipakai pada F-02, F-05, F-06, F-13, F-14, dan F-20, yaitu enam tempat di mana
kekurangan data justru menjadi isi layar.

---

## 12. Syarat yang dibutuhkan (menggantikan kalimat penutup)

1. **Untuk F-03 dan F-06.** Parse F-1 C dan F-11 dengan parser WITSML yang sama seperti V3, lalu
   bandingkan daftar kanal hasilnya dengan kanal yang sudah ada. Syarat: skrip parse V3 dijalankan
   pada 3.906 berkas dan hasilnya dicatat dalam `_parse_summary.json` baru.
2. **Untuk F-04.** Jalankan validasi satuan dan deteksi duplikat timestamp per sumur. Syarat:
   tabel konversi satuan per format (trajectory campuran rad dan derajat, DLIS 0,1 inci, EDM ft)
   dipakai seragam seperti catatan [D0] baris 175.
3. **Untuk F-08.** Petakan 409 formation picks ke interval litologi mudLog dan ke baris time-series.
   Syarat: pemetaan lewat MD yang sudah dikoreksi TVD (F-16) dan field XML, bukan nama folder
   ([D0] baris 135).
4. **Untuk F-09.** Bekukan prosedur uji rekonstruksi sebagai pra-registrasi sebelum kandidat label
   baru diuji, supaya status gugur bersifat final setelah hasil diketahui.
5. **Untuk F-11.** Uji daya pisah skema skor keyakinan pada data yang sudah ada, lalu bekukan
   pemetaan komponennya. Syarat: hasil uji dicatat sebelum skor dipakai di layar mana pun.
6. **Untuk F-13.** Hitung ulang jumlah positif per fold dari dataset jendela V9 dan tandai fold
   yang di bawah 30. Syarat: dataset `scratch/v9_d1/datasets/*.csv.gz` dibaca ulang, bukan angka
   dari ingatan.
7. **Untuk F-15.** Ukur apakah indeks kondisi enam alat berkorelasi dengan peristiwa bit run atau
   stuck. Syarat: label peristiwa dari kanal instrumen dan interval bhaRun digabung lebih dulu.
8. **Untuk F-17.** Jalankan filter `phase=ACTUAL` dan hitung ulang jumlah stasiun per wellbore.
   Syarat: tag `CD_DEFINITIVE_SURVEY_STATION` disaring per well, bukan total global.
9. **Untuk F-18.** Rekonsiliasi 77 berkas bhaRun di disk dengan 161 berkas di inventaris akuisisi
   ([V4] 62 mencatat selisih ini). Syarat: kedua daftar dibandingkan per uid, bukan per jumlah.
10. **Untuk F-19.** Buat dataset horizon lebih panjang dari 10 menit. Syarat: agregat per menit
    dipertahankan tanpa pemadatan yang membuang menit kosong, karena pemadatan itulah yang
    menyembunyikan gap ([RD0] 175).
11. **Untuk F-20.** Ajukan permintaan rating motor dan tabel keausan bit ke pemilik data. Syarat:
    daftar tag yang diminta mengikuti temuan 0 dari 192 dan 0 dari 161, bukan daftar keinginan umum.

---

## 13. Yang belum diverifikasi

1. **Selisih 59.500 baris di [E1] baris 59.** Angka 6.961.468 tidak sama dengan hitungan saya
   7.020.968 untuk tujuh CSV yang sama. Dugaan salah kurung dengan `VAR_F-5_alt` belum dibuktikan,
   dan dokumen mana pun belum menjelaskan selisih ini.
2. **VIBLAT 6 atau 7 sumur.** Ringkasan [RD0] baris 211 dan 390 menyebut 7, sedangkan tabel [RD0]
   baris 98-104 dan pemindaian header saya menyebut 6. Angka 6 yang terverifikasi, tetapi alasan
   selisihnya belum diketahui.
3. **Kolom `time.csv`.** `awk -F,` memberi 247, `csv.reader` memberi 239. Saya tidak membuka
   berkas 428 MB itu dengan parser CSV penuh, sehingga angka 239 saya ambil dari [A1] baris 130.
4. **`labels_curated_v2.csv`.** `wc -l` memberi 1.413 baris, sedangkan meta coverage menyebut 884
   label. Saya tidak membuktikan hubungan keduanya (kemungkinan ada catatan multi-baris atau
   beberapa label per event), jadi angka 884 saya pakai dari meta, bukan dari hitungan baris.
5. **Baris ledger untuk V3 sampai V6.** `grep` atas `docs/RND_PROVENANCE_LEDGER.md` tidak menemukan
   baris yang menyebut dokumen-dokumen ini, sehingga tidak ada rujukan ledger yang bisa dipakai.
6. **Efek setiap fitur ke keputusan operator.** Belum ada satu pun fitur di dokumen ini yang diuji
   dengan pengguna nyata. Semua status bukti di atas menilai bukti angka, bukan bukti kegunaan.
7. **Angka V3 sampai V6 yang tidak saya hitung ulang.** Populasi kelas R1, tabel onset per sumur,
   dan sebaran litologi saya kutip dari dokumen beserta barisnya, tanpa pengukuran ulang. Yang saya
   ukur ulang hanya butir yang keluarannya ada di bagian 14.

---

## 14. Bukti perintah (keluaran apa adanya)

### 14.A Ukuran dan baris sembilan berkas masukan

```
   205  17514 docs/V3_DATA_ACQUISITION_INVENTORY.md
   132   8429 docs/V3_TS_FEATURES.md
    55   3346 docs/V3_WITSML_PARSE_REPORT.md
   168  14334 docs/V4_MAINTENANCE_ML_OPTIONS.md
   338  26032 docs/V6_PM_VERDICT.md
   203  19871 docs/V6_D0_READERS_SYNTHESIS.md
   302  28138 docs/V6_A1_DATA_AUDIT.md
   189  12738 docs/V6_E1_PREREG.md
   401  28196 docs/RND_D0_DATA_FEASIBILITY.md
  1993 158598 total
```

### 14.B Direktori CSV terparse dan jumlah kolom

```
F-10.csv cols=241 labelchans=4
F-12.csv cols=188 labelchans=2
F-14.csv cols=239 labelchans=4
F-15A.csv cols=282 labelchans=3
F-15_S.csv cols=245 labelchans=3
F-5.csv cols=182 labelchans=3
F-7.csv cols=119 labelchans=2
F-9.csv cols=198 labelchans=4
F-9_A.csv cols=233 labelchans=3
VAR_F-5_alt.csv cols=61 labelchans=0
```

### 14.C Baris CSV terparse dan hitungan aritmetika

```
    773675 data/volve/witsml_parsed/F-10.csv
   2081568 data/volve/witsml_parsed/F-12.csv
   1648027 data/volve/witsml_parsed/F-14.csv
    778163 data/volve/witsml_parsed/F-15A.csv
   1883063 data/volve/witsml_parsed/F-15_S.csv
   1286968 data/volve/witsml_parsed/F-5.csv
    547501 data/volve/witsml_parsed/F-7.csv
    457546 data/volve/witsml_parsed/F-9.csv
    419707 data/volve/witsml_parsed/F-9_A.csv
     59490 data/volve/witsml_parsed/VAR_F-5_alt.csv
   9935708 total
total_data_10csv=9935698
F10_data=773674 F12_data=2081567
9935698-773674-2081567=7080457
klaim_V3=7080457
7 sumur (tanpa VAR, tanpa F-10/F-12):
sum=7020968
klaim V6_E1 L59 = 6961468 | selisih dengan sum:
59500
8 CSV (tanpa F-10/F-12) = 7080457
klaim V3_WITSML L20 = 7080457
```

### 14.D Kanal label per sumur (header scan)

```
F-10: SHKRSK_RT|CRPM_RT|VIBLAT_RT|STUCK_RT|
F-12: CRPM_RT|SHKRSK_RT|
F-14: SHKRSK_RT|STUCK_RT|CRPM_RT|VIBLAT_RT|
F-15A: VIBLAT_RT|CRPM_RT|SHKRSK_RT|
F-15_S: VIBLAT_RT|CRPM_RT|SHKRSK_RT|
F-5: CRPM_RT|SHKRSK_RT|VIBLAT_RT|
F-7: SHKRSK_RT|CRPM_RT|
F-9: SHKRSK_RT|CRPM_RT|VIBLAT_RT|STUCK_RT|
F-9_A: SHKRSK_RT|STUCK_RT|CRPM_RT|
VAR_F-5_alt: NONE
```

### 14.E Artefak fitur time-series

```
npz_exists True 458129
keys ['X', 'X_baseline', 'X_window_meta', 'act_start_utc', 'baseline_names', 'category',
'channels', 'event_id', 'feature_names', 'fold', 'outcome', 'primary_window', 'wellbore',
'window_meta_names', 'windows']
X_shape (661, 480) n_features 480
w2h_features 160
events_w2h_all_nan 191 of 661
nan_frac_w2h 0.368
w30m__ features 160 all_nan_events 194
w6h__ features 160 all_nan_events 185
anti_leakage {'rule': 'semua sampel fitur: timestamp < act_start', 'rows_scanned': 4274005,
'violations': 0, 'required': 0, 'pass': True}
empty_all_three 185
per_well_w2h_empty {'NO 15/9-F-14': 46, 'NO 15/9-F-15': 11, 'NO 15/9-F-15 A': 0,
'NO 15/9-F-5': 2, 'NO 15/9-F-7': 20, 'NO 15/9-F-9': 30, 'NO 15/9-F-9 A': 82}
wellbore_counts {'NO 15/9-F-14': 182, 'NO 15/9-F-15': 105, 'NO 15/9-F-15 A': 32,
'NO 15/9-F-5': 134, 'NO 15/9-F-7': 58, 'NO 15/9-F-9': 56, 'NO 15/9-F-9 A': 94}
coverage {"labels_total": 884, "mapped_to_fold": 671, "unmapped_excluded":
{"NO 15/9-F-15 D": 122, "NO 15/9-F-15 C": 89, "NO 15/9-F-15 B": 2},
"out_of_range_excluded": {"F-15_S": 7, "F-5": 2, "F-7": 1},
"features_built": 661, "zero_row_windows": 570, "partial_windows": 1}
662 /mnt/d/Capstone 1(v2)/data/predictive/features_timeseries_events.csv
```

### 14.F Klaim ketiadaan yang diuji ulang

```
=== tubular xml ===
192
rating hits (torqueMax|Pmax|revPerGallon|rpmMax):
0
=== bhaRun xml ===
161
dull hits (dullingInfo|dullGrade|bitName):
0
=== log xml total / per well top ===
7150
   2156 Norway-Statoil-NO 15_$47$_9-F-1 C
   1750 Norway-Statoil-NO 15_$47$_9-F-11
   1100 Norway-Statoil-NO 15_$47$_9-F-15
    271 Norway-StatoilHydro-15_$47$_9-F-10
    233 Norway-Statoil-15_$47$_9-F-12
```

### 14.G `time.csv` dan `USROP_labeled.csv`

```
-rwxrwxrwx 1 neonti neonti 427910797 Oct  4 14:04 data/witsml/Norway-NA-15_47_9-F-9 A time.csv
cols=247
419748 data/witsml/Norway-NA-15_47_9-F-9 A time.csv
198929 data/USROP_labeled.csv
```

### 14.H Direktori `planning/` saat kartu ini jalan

```
-rwxrwxrwx 1 neonti neonti 38846 Oct 31 16:15 00_INVENTARIS_V7_V8.md
-rwxrwxrwx 1 neonti neonti 24746 Oct 31 16:13 02_RISET_VISUALISASI.md
```

Dua berkas itu keluaran kartu lain di board yang sama. Kartu ini menulis
`00_INVENTARIS_V3_V6.md` dan tidak menyentuh keduanya.

### 14.I Pemeriksaan ledger dan label

```
=== I. LEDGER CUPLIKAN ===
(grep untuk RND-D0, V3_TS_FEATURES, V6_A1, V6_PM_VERDICT: tidak ada keluaran)
=== PROVENANCE LEDGER ===
-rwxrwxrwx 1 neonti neonti 471945 Oct 29 11:24 docs/RND_PROVENANCE_LEDGER.md
=== LABELS ROWS ===
1413 data/volve/labels_curated_v2.csv
```

---

## 15. Daftar sumber

1. `docs/V3_DATA_ACQUISITION_INVENTORY.md` (17.514 B, 205 baris). Dipakai: baris 11, 17, 37, 43-46,
   78, 147-154, 163, 165, 182-185, 197.
2. `docs/V3_TS_FEATURES.md` (8.429 B, 132 baris). Dipakai: baris 4-5, 39-44, 54, 62-73, 82, 89,
   100-104, 108-110, 129-132.
3. `docs/V3_WITSML_PARSE_REPORT.md` (3.346 B, 55 baris). Dipakai: baris 4, 20, 26-28, 34-37, 41,
   45-48.
4. `docs/V4_MAINTENANCE_ML_OPTIONS.md` (14.334 B, 168 baris). Dipakai: baris 7, 13, 17, 25, 34-35,
   41-43, 56, 58, 62, 68-80, 84, 88-108, 112-120, 127-129, 143-167.
5. `docs/V6_PM_VERDICT.md` (26.032 B, 338 baris). Dipakai: baris 25-28, 89-100, 130-141, 164-171,
   178-190, 225.
6. `docs/V6_D0_READERS_SYNTHESIS.md` (19.871 B, 203 baris). Dipakai: baris 17-31, 45-52, 60-73,
   77-88, 92-103, 135, 147-159, 166-181.
7. `docs/V6_A1_DATA_AUDIT.md` (28.138 B, 302 baris). Dipakai: baris 26-30, 58, 65-66, 76, 78, 100,
   130-136, 194-208, 248-264.
8. `docs/V6_E1_PREREG.md` (12.738 B, 189 baris). Dipakai: baris 3-7, 41-52, 58-75, 100-105,
   110-113, 138-160, 164-179.
9. `docs/RND_D0_DATA_FEASIBILITY.md` (28.196 B, 401 baris). Dipakai: baris 30-35, 98-104, 159,
   175, 179, 183-228, 288-302, 311-341, 349-352, 356-369, 388-392.
10. Artefak yang dibuka langsung: `data/predictive/features_timeseries.npz`,
    `features_timeseries_meta.json`, `features_timeseries_events.csv`,
    `data/volve/witsml_parsed/*.csv`, `data/volve/witsml_raw/**`,
    `data/USROP_labeled.csv`, `data/witsml/Norway-NA-15_47_9-F-9 A time.csv`,
    `data/volve/labels_curated_v2.csv`.
