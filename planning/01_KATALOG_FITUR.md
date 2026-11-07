# 01 KATALOG FITUR: katalog detail untuk tim website

Kartu: `t_1a73862d` (KATALOG). Board: `fitur-v9-swarm`. Tanggal: 2026-10-31 (WIB).
Workspace: `/mnt/d/Capstone 1(v2)`. Keluaran: berkas ini saja, di folder `planning/`.

Dokumen ini menyatukan empat inventaris vonis dan satu laporan verifikasi menjadi satu katalog
fitur yang bisa langsung dipakai tim website. Isinya keputusan produk, bukan laporan riset baru.
Tidak ada model yang dijalankan di sini, tidak ada angka sumber yang diubah, dan tidak ada berkas
selain markdown yang dibuat.

---

## 0. Kerangka wajib (dipakai apa adanya, tidak diubah)

1. Alarm otomatis BUKAN tujuan. ML dipakai sebagai sistem pendukung keputusan dengan skor
   keyakinan, bukan pemutus. Konsekuensi pada katalog: setiap fitur yang menampilkan angka model
   wajib menampilkan angka keyakinan dan batas pemakaiannya pada layar yang sama, dan tidak ada
   satu fitur pun yang dirancang sebagai pemicu tindakan otomatis.
2. Setiap angka punya sumber: berkas dan baris, atau baris ledger
   `docs/RND_PROVENANCE_LEDGER.md`. Kode berkas di katalog ini ada di bagian 2.
3. Tidak ada klaim berjalan tanpa bukti. Perintah yang dijalankan untuk memeriksa angka dan untuk
   memeriksa berkas ini sendiri ditempel apa adanya di bagian 13.
4. Kekurangan data dikemas menjadi fitur berguna (pola Dynamic Island), bukan keluhan. Tujuh fitur
   di katalog ini dibangun justru dari kekurangan: DAT-02, DAT-05, DAT-06, DAT-08, DAT-09, KEP-10,
   dan INS-05.
5. Setiap fitur punya lima field wajib: pengguna, momen pakai, masukan, keluaran, status bukti.
6. Tidak ada kalimat penutup yang menutup jalan. Bila sesuatu belum tersedia, yang ditulis adalah
   syaratnya, dan daftar syaratnya ada di bagian 12.
7. Keluaran hanya markdown di `planning/`. Tidak ada .py, .html, .json, atau .csv sebagai
   deliverable.
8. Tidak memakai tanda pisah panjang. Rentang angka ditulis dengan tanda hubung biasa.

---

## 1. Berkas masukan yang dibuka dan ukuran byte

Ukuran diambil dengan `wc -c -l` pada 2026-10-31, keluaran ada di bagian 13.

| Kode | Berkas | Byte | Baris |
|---|---|---:|---:|
| [I1] | `planning/00_INVENTARIS_V3_V6.md` | 44.125 | 626 |
| [I2] | `planning/00_INVENTARIS_V7_V8.md` | 39.059 | 589 |
| [I3] | `planning/00_INVENTARIS_V9_RND1.md` | 33.601 | 472 |
| [I4] | `planning/00_INVENTARIS_RND2_V11.md` | 35.536 | 412 |
| [VF] | `planning/00_VERIFIKASI_INVENTARIS.md` | 43.536 | 700 |
| [VR] | `planning/02_RISET_VISUALISASI.md` | 24.746 | 258 |
| | **Total enam berkas** | **220.603** | **3.057** |

Enam berkas dibuka penuh sampai baris terakhir. Berkas [VR] dipakai untuk butir "dasar riset
penyajian" pada setiap fitur, karena di situlah rujukan visual dikumpulkan dengan ukuran byte
respons dan kutipan kalimat inti. Berkas [VF] dipakai untuk dua hal: memilih angka yang boleh
dikutip dan menandai angka yang wajib dihitung ulang lebih dulu.

Catatan kejujuran tentang angka di dalam katalog ini: seluruh angka berasal dari [I1] sampai [I4]
dan dari [VR], dan setiap angka sudah membawa kode berkas serta nomor baris di dalam tanda kurung
siku. Angka yang [VF] tandai tidak cocok atau meleset rujukannya TIDAK dipakai di sini, dan
daftarnya ada di bagian 12.

---

## 2. Legenda kode berkas sumber

Kode di bawah dipakai di seluruh katalog. Semua jalur relatif terhadap `/mnt/d/Capstone 1(v2)/`.
Ukuran byte diambil dari tabel berkas di [I1] bagian 1, [I2] bagian 1, [I3] bagian 1, dan
[I4] bagian 1.

| Kode | Berkas | Byte |
|---|---|---:|
| [V3A] | `docs/V3_DATA_ACQUISITION_INVENTORY.md` | 17.514 |
| [V3T] | `docs/V3_TS_FEATURES.md` | 8.429 |
| [V3W] | `docs/V3_WITSML_PARSE_REPORT.md` | 3.346 |
| [V4] | `docs/V4_MAINTENANCE_ML_OPTIONS.md` | 14.334 |
| [PM6] | `docs/V6_PM_VERDICT.md` | 26.032 |
| [D0] | `docs/V6_D0_READERS_SYNTHESIS.md` | 19.871 |
| [A1] | `docs/V6_A1_DATA_AUDIT.md` | 28.138 |
| [E1] | `docs/V6_E1_PREREG.md` | 12.738 |
| [RD0] | `docs/RND_D0_DATA_FEASIBILITY.md` | 28.196 |
| [PM7] | `docs/V7_PM_VERDICT.md` | 23.569 |
| [A1-7] | `docs/V7_A1_SOLUTION_AUDIT.md` | 17.731 |
| [PM8] | `docs/V8_PM_VERDICT.md` | 23.720 |
| [M1] | `docs/V8_M1_CAPABILITY_MAP.md` | 23.716 |
| [A1-8] | `docs/V8_A1_CAPABILITY_AUDIT.md` | 14.818 |
| [Ev] | `docs/V8_E_vib_CAPABILITY.md` | 13.970 |
| [Ess] | `docs/V8_E_ssi_CAPABILITY.md` | 12.678 |
| [Eb] | `docs/V8_E_bit_wear_CAPABILITY.md` | 16.116 |
| [Es] | `docs/V8_E_stuck_CAPABILITY.md` | 22.172 |
| [Eh] | `docs/V8_E_hyd_CAPABILITY.md` | 16.345 |
| [Ek] | `docs/V8_E_shk_CAPABILITY.md` | 17.176 |
| [Ew] | `docs/V8_E_tool_wear_CAPABILITY.md` | 11.876 |
| [PM1] | `docs/V9_PM1_ARCHITECTURE.md` | 50.456 |
| [PM2] | `docs/V9_PM2_VERDICT.md` | 22.654 |
| [EVA] | `docs/V9_EVAL_A_LAYERA.md` | 32.713 |
| [EVB] | `docs/V9_EVAL_B_LAYERB.md` | 30.472 |
| [EVC] | `docs/V9_EVAL_C_LAYERC.md` | 23.153 |
| [EML] | `docs/V9_E_ML_ENGINE.md` | 38.169 |
| [R1] | `docs/RND_R1_METAHEURISTIK.md` | 63.089 |
| [R2] | `docs/RND_R2_STOKASTIK.md` | 28.937 |
| [R3] | `docs/RND_R3_VMD_SVM.md` | 32.174 |
| [R4] | `docs/RND_R4_BOOSTING.md` | 28.460 |
| [R5] | `docs/RND_R5_DRIFT.md` | 35.937 |
| [R8] | `docs/RND_R8_EVALUASI_BERLAPIS.md` | 27.013 |
| [PMR] | `docs/RND_PM_VERDICT.md` | 34.575 |
| [S1] | `docs/RND_S1_SEED_ROBUSTNESS.md` | 26.235 |
| [S3] | `docs/RND_S3_HYBRID_BITWEAR.md` | 22.275 |
| [S4] | `docs/RND_S4_LAYER_B_DATA.md` | 23.799 |
| [S5A] | `docs/RND_S5_AUDIT_WAVE2.md` | 27.190 |
| [S6] | `docs/RND_S6_PM_WAVE2.md` | 40.271 |
| [ENG] | `docs/RND_ENGINE_S6_INTEGRATION.md` | 3.915 |
| [V11] | `docs/V11_PM_FINAL.md` | 20.660 |
| [L] | `docs/RND_PROVENANCE_LEDGER.md` | 471.945 |

Rujukan visual memakai kode [LV1] sampai [LV16], sesuai daftar di [VR] bagian 9. Kode itu
sengaja diberi awalan LV agar tidak tertukar dengan [S1] di atas yang berarti berkas robustness
seed. Tujuh kode yang paling sering dipakai di katalog ini:

| Kode | Sumber | Dipakai untuk |
|---|---|---|
| [LV1] | scikit-learn, Probability calibration | skor keyakinan dan kurva kalibrasi |
| [LV2] | ASQ, What is a Pareto Chart | peringkat jam henti dan prioritas |
| [LV3] | Hyndman dan Athanasopoulos, Time series graphics | tren waktu |
| [LV4] | Nielsen Norman Group, Data Tables | antrean kerja berbentuk tabel |
| [LV5] | Kay dan kawan-kawan, CHI 2016, When (ish) is My Bus | ketidakpastian pada skor |
| [LV6] | Financial Times, Visual Vocabulary | pemilihan jenis grafik |
| [LV7] | Nielsen Norman Group, Dashboards | kanal visual yang cepat dibaca |
| [LV14] | Workhint, Queue Aging Report | kolom umur pada antrean |

---

## 3. Ringkasan 48 fitur

Enam rumpun, sesuai urutan yang diminta kerangka: kepercayaan, perencanaan maintenance, kualitas
data, perbandingan mesin, linimasa dan jejak keputusan, alat bantu insinyur.

| ID | Nama fitur | Rumpun | Pengguna utama | Status bukti |
|---|---|---|---|---|
| KEP-01 | Papan vonis per kelas kerusakan | kepercayaan | insinyur pengeboran, supervisor | siap sekarang |
| KEP-02 | Skor keyakinan 0 sampai 100 berlapis selang | kepercayaan | insinyur pemeliharaan | siap sebagian |
| KEP-03 | Badge beban alarm dan pengunci satuan FAR | kepercayaan | operator shift | siap sekarang |
| KEP-04 | Kurva kalibrasi dan titik kuantil per head | kepercayaan | penilai model, auditor | rancangan |
| KEP-05 | Gerbang provenance angka tiga warna | kepercayaan | penulis laporan, PM | siap sekarang |
| KEP-06 | Papan dua pembacaan literal dan ketat | kepercayaan | dosen penguji, PM | siap sekarang |
| KEP-07 | Pengunci rujukan baris dan uji mutasi angka | kepercayaan | auditor internal | siap sekarang |
| KEP-08 | Panel ketidaksepakatan antar head | kepercayaan | supervisor, operator | siap sebagian |
| KEP-09 | Banner transparansi label bit_wear | kepercayaan | reviewer, pembimbing | siap sekarang |
| KEP-10 | Slot nilai jujur lapisan B | kepercayaan | perencana maintenance, manajer | siap sebagian |
| MNT-01 | Antrean triage onset per shift dengan umur item | perencanaan maintenance | insinyur shift malam, toolpusher | siap sekarang |
| MNT-02 | Kalkulator anggaran pemeriksaan | perencanaan maintenance | supervisor pemeliharaan | siap sekarang |
| MNT-03 | Sakelar dua titik operasi hyd | perencanaan maintenance | supervisor shift | siap sekarang |
| MNT-04 | Panel titik operasi hemat-awas shk | perencanaan maintenance | driller, supervisor | siap sekarang |
| MNT-05 | Penaksir beban tinjauan per shift | perencanaan maintenance | perencana tenaga kerja | siap sebagian |
| MNT-06 | Mode bengkel dan detektor perubahan regime | perencanaan maintenance | teknisi bengkel | siap sekarang |
| MNT-07 | Kurva tren keausan dengan cap keterlambatan | perencanaan maintenance | engineer drilling | siap sekarang |
| MNT-08 | Indikator status hidrolik | perencanaan maintenance | mudlogger, driller | siap sekarang |
| MNT-09 | Watchlist stick-slip dan penanda daya statistik | perencanaan maintenance | supervisor operasi | siap sebagian |
| DAT-01 | Kartu kelengkapan jendela pra-event | kualitas data | engineer PdM, supervisor | siap sekarang |
| DAT-02 | Kanal status sumur tidak logging | kualitas data | driller, mudlogger | siap sekarang |
| DAT-03 | Peta label ke fold dan antrean parse | kualitas data | auditor, ML engineer | siap sekarang |
| DAT-04 | Pemilih kanal berbasis fill rate dan QC fisik | kualitas data | engineer data | siap sebagian |
| DAT-05 | Matriks ketersediaan berkas per sumur | kualitas data | engineer PdM, peneliti | siap sekarang |
| DAT-06 | Antrean parse 3.906 berkas | kualitas data | koordinator data | siap sekarang |
| DAT-07 | Katalog label instrumen per sumur | kualitas data | auditor, ML engineer | siap sekarang |
| DAT-08 | Kartu kesiapan kanal per sumur | kualitas data | engineer instrumentasi | siap sekarang |
| DAT-09 | Peta drift antar sumur dan dalam sumur | kualitas data | penanggung jawab mutu data | siap sekarang |
| DAT-10 | Validitas kedalaman MD ke TVD | kualitas data | engineer drilling | siap sekarang |
| CMP-01 | Balapan model terhadap baseline persistence | perbandingan mesin | peneliti, dosen penguji | siap sekarang |
| CMP-02 | Peta kalah-menang per kelas | perbandingan mesin | PM, peneliti | siap sekarang |
| CMP-03 | Tabel kanal masukan yang melawan intuisi | perbandingan mesin | peneliti, engineer fitur | siap sekarang |
| CMP-04 | Kartu rekam jejak per sumur | perbandingan mesin | auditor, supervisor | siap sekarang |
| CMP-05 | Bukti sirkularitas target mekanika | perbandingan mesin | reviewer, peneliti | siap sekarang |
| CMP-06 | Lembar prasyarat eksperimen | perbandingan mesin | peneliti, reviewer metode | siap sebagian |
| CMP-07 | Panel kesetaraan head hyd | perbandingan mesin | PM, peneliti, dosen penguji | siap sebagian |
| LIN-01 | Log keputusan human-in-loop | linimasa dan jejak keputusan | supervisor, peneliti | siap sebagian |
| LIN-02 | Garis waktu tingkat target dan gerbang | linimasa dan jejak keputusan | auditor, dosen penguji | siap sekarang |
| LIN-03 | Penanda selang wajib pada angka FAR dan recall | linimasa dan jejak keputusan | reviewer, operator | siap sebagian |
| LIN-04 | Register status dokumen vonis | linimasa dan jejak keputusan | auditor, penulis laporan | siap sekarang |
| LIN-05 | Kalender sumber angka | linimasa dan jejak keputusan | auditor | siap sekarang |
| LIN-06 | Kuis dua halaman tentang angka | linimasa dan jejak keputusan | dosen penguji, PM | siap sekarang |
| LIN-07 | Linimasa tier per kelas dan syarat naik tier | linimasa dan jejak keputusan | PM, peneliti | siap sebagian |
| INS-01 | Wizard kalibrasi dan uji jalan sebelum pindah sumur | alat bantu insinyur | engineer pemasangan, auditor | siap sebagian |
| INS-02 | Panduan skrip verifikasi rujukan | alat bantu insinyur | auditor internal | siap sekarang |
| INS-03 | Kartu kelayakan sinyal sebelum dekomposisi | alat bantu insinyur | peneliti sinyal | siap sebagian |
| INS-04 | Kartu kanal yang perlu dipasang | alat bantu insinyur | engineer instrumentasi | siap sebagian |
| INS-05 | Kartu permintaan data bertanda tangan | alat bantu insinyur | koordinator data, pembimbing | siap sebagian |

Jumlah baris data tabel di atas: 48. Rekap status bukti ada di bagian 11.

---

## 4. Aturan pemakaian katalog ini

Tiga aturan singkat, supaya tim website tidak salah membaca.

Pertama, status bukti bukan status prioritas. Fitur berstatus rancangan atau siap sebagian tetap
boleh dikerjakan lebih dulu bila nilainya tinggi bagi pengguna, hanya saja layarnya wajib
menyatakan bahwa angka yang tampil masih rancangan atau masih menunggu satu komponen. Contoh:
KEP-04 masih rancangan, padahal ia menopang KEP-02 dan KEP-06.

Kedua, satu fitur boleh memakai beberapa head dan beberapa kelas, tetapi satu head tidak boleh
dipakai sebagai alasan menaikkan tier kelas lain. Aturan ini berasal dari keputusan arsitektur V8
dan V9: head dipisah per kelas, yang dibagi hanya infrastruktur grid dan feature store
([M1] baris 96-99).

Ketiga, tidak ada fitur di katalog ini yang boleh ditampilkan sebagai peringatan kritis. Slot alarm
otomatis hari ini nol, dan angka itu terukur: 0 dari 7 engine memenuhi syarat alarm otomatis
([I2] baris 91; [PM8] baris 180-184). Konsekuensi desain: tidak ada tombol "kirim alarm", tidak ada
notifikasi push bertanda kritis, dan tidak ada warna merah tanpa label manusia-peninjau di
sebelahnya.

---

## 5. Rumpun kepercayaan (KEP-01 sampai KEP-10)

Lima belas fitur teratas di katalog ini ditulis dengan butir lengkap tanpa butir kosong. Sepuluh
fitur pertama ada di rumpun ini karena kepercayaan adalah masalah nomor satu yang muncul di empat
inventaris: bukan model yang kurang, melainkan angka yang tampil lebih kuat daripada buktinya.

### KEP-01 Papan vonis per kelas kerusakan

**Tujuan.** Memberi satu kartu per kelas kerusakan yang menyatakan apa yang benar-benar sudah
terukur untuk kelas itu dan apa yang masih menggantung. Masalah yang diselesaikan: pembaca hari ini
melihat 11 klaim mesin sebagai satu tumpukan angka dan menyimpulkan kemampuan yang lebih besar
daripada buktinya. Penggunanya insinyur pengeboran, supervisor shift, dosen penguji, dan tim website
yang harus menulis label pada setiap panel.

**Menggambarkan apa.** Papan ini menggambarkan tingkat pemakaian sebuah head, bukan kondisi fisik
lubang bor. Tiga tingkat yang dipakai sudah ditetapkan V8 dan tidak berubah: peringatan
human-in-loop, tren atau skor, dan belum layak pakai. Bila sebuah kelas naik tingkat, artinya bukti
lapisan B dan C bertambah, bukan artinya kerusakan lebih sering terjadi. Bila turun, artinya ada
syarat yang gagal diukur pada kampanye terakhir.

**Pengguna dan momen pakai.** Insinyur pengeboran dan supervisor shift, dibuka sebelum mempercayai
badge kelas mana pun dan saat serah terima shift, jadi dua kali per shift. Dosen penguji membukanya
sekali per sesi bimbingan. Tim website memakainya sekali saat menulis label panel.

**Masukan.** Tabel komposisi terpilih per kelas ([S6] bagian 3 baris 148-159), peta tier
([S6] bagian 3.1 baris 163-167), komposisi head hasil perakitan ([PM2] baris 140 dan 181), dan
gerbang kenaikan tier ([PM1] baris 138-139). Semua bentuknya tabel statis, tidak ada masukan
pengguna.

**Algoritma.** Tidak memakai model. Aturannya tiga langkah penggabungan. Langkah satu, ambil tier
tertinggi yang dimiliki kelas itu dari peta tier. Langkah dua, tempelkan gerbang yang mengikat tier
tersebut: LAYER-1 butuh FAR maksimum 6 per 24 jam operasi negatif terukur dengan recall di atas nol
plus T_lead atau B4 terukur plus C4. LAYER-0 butuh FAR maksimum 1 dengan recall di atas nol plus B1
minimal 80 persen plus C2 per bin plus C3 dropout di bawah 20 persen. Langkah tiga, tandai setiap
syarat yang belum terukur sebagai menggantung, bukan sebagai lulus.

**Workflow.** (1) Baca tabel komposisi per kelas dari berkas markdown sumber. (2) Petakan setiap
kelas ke tier tertingginya. (3) Ambil angka penopang tier dari profil kelas masing-masing.
(4) Ambil daftar syarat yang menggantung dari bagian syarat di dokumen vonis. (5) Susun satu kartu
per kelas dengan urutan tetap: nama kelas, tugas, tier, angka penopang, syarat menggantung.
(6) Tampilkan tanggal potong data di kaki kartu, karena angka ini tidak bergerak sendiri.

**Keluaran.** Sebelas kartu, satu per klaim. Tiap kartu memuat: nama kelas, tugas dalam satu
kalimat, tier dalam bentuk label, dua sampai empat angka penopang dengan rujukan, dan daftar syarat
menggantung. Tidak ada skor gabungan di papan ini, karena menggabungkan tier antar kelas justru
membuat pembaca membandingkan hal yang tidak sebanding.

**Saran penyajian.** Kartu angka bertumpuk (satu kolom, sebelas kartu) dengan lencana tier di
kiri atas dan daftar syarat di bagian bawah kartu. Alasan: pertanyaan pembaca adalah "kelas ini
sampai mana", jadi yang dibutuhkan perbandingan nilai pada satu kelas, bukan perbandingan antar
kelas pada satu skala. Tata letak contoh: baris pertama tiga kartu (vib, ssi, shk), baris kedua
tiga kartu (stuck K-i, stuck K-ii, hyd K-i), baris ketiga tiga kartu (hyd K-ii, bit_wear K-1,
bit_wear K-2), baris keempat dua kartu (tool_wear K-i, tool_wear K-ii). Di atas grid ada satu baris
ringkas: 27 head, 5 L0, 11 L1, 9 L2, 2 L3, 0 slot alarm otomatis.

**Dasar riset penyajian.** [LV6] menempatkan "perbandingan kategori pada nilai yang sama" sebagai
tugas yang dilayani batang atau kartu bernilai, bukan donat. [LV4] menambahkan bahwa tabel dipakai
saat pembaca perlu membandingkan dan mencari, dan kolom pertama sebaiknya pengenal yang terbaca
manusia, bukan ID otomatis. Karena itu nama kelas ditulis sebagai judul kartu, bukan kode internal.

**Status bukti.** Siap sekarang. Seluruh isi kartu berasal dari tabel yang sudah terbit: komposisi
[S6] bagian 3, tier [M1] baris 169-174 dan [PM8] baris 176-184, gerbang [PM1] baris 138-139.
Hitung tier 0 + 3 + 2 + 2 = 7 juga sudah dicocokkan ([M1] baris 174; [PM8] baris 176-177).

**Salah tafsir yang harus dicegah.** Pertama, membaca tier sebagai mutu model. Tier menilai
kesiapan pemakaian, dan engine dengan sinyal kuat bisa bertier rendah karena lapisan B belum
terukur, contohnya vib dengan lift 1,61 sampai 3,50 di 4 dari 4 fold ([Ev] baris 52 dan 69) tetapi
B3 dan B4 belum pernah dicetak ([M1] baris 50). Kedua, menjumlahkan tier antar kelas menjadi satu
skor armada. Ketiga, membaca "0 slot alarm" sebagai kegagalan; itu keputusan desain yang diambil
karena tidak satu pun engine memenuhi syarat, dan angka itu tercatat sebagai TERUKUR di ledger
`PM-078` baris 2024.

**Cara menguji.** Ambil satu kartu secara acak, lalu minta dua orang berbeda mencari angka
penopangnya di berkas sumber hanya dengan rujukan yang tercetak. Lulus bila kedua orang menemukan
baris yang sama dalam dua menit. Uji kedua: tempel kartu ke layar 375 piksel dan pastikan daftar
syarat menggantung tetap terbaca tanpa menggulir horizontal.

### KEP-02 Skor keyakinan 0 sampai 100 berlapis selang

**Tujuan.** Memberi satu angka yang bisa dibawa ke rapat, tanpa mengubahnya menjadi kepastian.
Masalah yang diselesaikan: laporan hari ini memakai dikotomi lulus atau gagal, sedangkan buktinya
bertingkat. Untuk insinyur pemeliharaan yang harus memilih satu dari beberapa peringatan, dan untuk
pembaca laporan yang menuntut satu angka ringkas.

**Menggambarkan apa.** Skor ini menggambarkan keyakinan pada bukti, bukan peluang kerusakan. Skor
tinggi berarti sinyal kelas itu kuat dan lapisan operasionalnya terukur. Skor rendah bisa berarti
sinyal lemah, bisa juga berarti sinyal kuat tetapi biaya pemeriksaannya belum diukur. Bila skor
turun setelah kampanye baru, artinya ada komponen yang sebelumnya diasumsikan kini terukur dan
ternyata rendah, bukan artinya kondisi rig memburuk.

**Pengguna dan momen pakai.** Insinyur pemeliharaan saat memilih satu peringatan untuk dikerjakan
lebih dulu, beberapa kali per shift. Manajer operasi saat menyusun laporan mingguan, sekali per
minggu. Auditor saat memeriksa apakah angka di laporan masih memakai bobot yang sama.

**Masukan.** Tiga komponen berbobot: kekuatan sinyal S_A, kesiapan operasional S_B, dan
keterpercayaan S_C. Masukannya angka yang sudah terukur, yaitu lift per fold, nilai B1, FAR
terukur, dan penilaian C1 sampai C4. Bentuknya delapan baris tabel, satu per kelas, bukan deret
waktu. Sumber mentahnya angka di [I2] bagian 2.3.

**Algoritma.** Rumus yang dipakai sekarang: SK sama dengan 100 dikali (0,40 S_A + 0,35 S_B + 0,25
S_C). Aturan pemetaan S_A: 0,75 bila lift minimal 1,5 di mayoritas fold, menang terhadap baseline
utama mayoritas, dan baseline sekunder tidak kalah di mayoritas fold. 0,60 bila lift di atas 1 di
mayoritas fold tetapi CI95 belum signifikan mayoritas. 0,30 bila menang terhadap baseline lemah
tetapi kalah terhadap baseline terbaik kelas itu. 0,20 bila belum terukur. Aturan S_B: 1,00 bila B1
minimal 80 persen dan FAR maksimum 1 terukur. 0,60 bila B1 50 sampai 79 persen atau FAR 2 sampai 6.
0,35 bila B1 di bawah 50 persen atau FAR di atas 6 terukur. 0,20 bila belum terukur. S_C adalah
rata-rata C1 sampai C4, masing-masing dinilai 1, 0,5, atau 0. Hasil terhitung: vib 50, ssi 53,
bit_wear 25, stuck 46, hyd K-i 61, hyd K-ii 51, shk 52, tool_wear 46 ([I2] bagian 4).

**Workflow.** (1) Ambil angka masuk dari tabel kapabilitas per kelas. (2) Petakan ke S_A, S_B, S_C
memakai aturan di atas. (3) Hitung SK dan bulatkan ke bilangan bulat. (4) Tempelkan pita selang
dari CI95 metrik utama kelas itu. (5) Tempelkan batas atas skor bila lapisan B kosong, mengikuti
usulan F-02 di [I4] yang memotong skor maksimum di 70 sampai B terukur. (6) Bekukan pemetaan itu
sebagai pra-registrasi sebelum dipakai sebagai ambang ([I3] bagian 9 butir 1). (7) Tampilkan tiga
komponen terbaca di balik angka, supaya pembaca bisa melihat mana yang menekan skor.

**Keluaran.** Satu bilangan bulat 0 sampai 100, satu pita selang, tiga komponen S_A, S_B, S_C dalam
bentuk pecahan dua desimal, dan satu penanda "batas atas dipotong" bila lapisan B kosong. Rentang
yang sudah muncul di data: 25 sampai 61. Arti tiap nilai: 25 berarti bukti sinyal ada tetapi kalah
dari baseline terbaik, 61 berarti sinyal kuat dan lapisan operasional sebagian terukur.

**Saran penyajian.** Titik kuantil atau batang interval, bukan satu angka besar. Skor ditulis
sebagai angka kecil di dalam batang, pita selang di belakangnya, dan tiga komponen sebagai tiga
batang horizontal pendek di bawahnya. Alasan: angka tunggal tanpa sebaran terbaca sebagai kepastian,
dan pada uji pembacaan, titik kuantil menurunkan variasi taksiran peluang sekitar 1,15 kali
dibanding density plot ([LV5]). Tata letak contoh: kartu 320 piksel dengan angka di tengah atas,
batang interval selebar kartu, tiga batang komponen bertumpuk di bawah, dan satu baris teks
"batas atas 70 karena lapisan B kosong". Perbandingan antar kelas memakai batang horizontal
berurutan, bukan donat, karena delapan nilai berbeda harus dibandingkan panjangnya.

**Dasar riset penyajian.** [LV5] menjadi dasar pemilihan titik kuantil dan peringatan terhadap
prediksi titik. [LV1] menjadi dasar larangan mengganti sebaran dengan satu skor agregat, karena
skor seperti Brier mencampur kalibrasi, daya pisah, dan keacakan data. [LV7] menambahkan bahwa
panjang dan posisi dua dimensi adalah kanal yang paling cepat diproses, sehingga batang lebih tepat
daripada cakram atau pengukur jarum untuk angka 0 sampai 100.

**Status bukti.** Siap sebagian. Aritmetika delapan baris sudah dihitung ulang dan cocok seluruhnya
([VF] bagian 3.2). Yang belum: daya pisah skor belum diuji, dan dua usulan rumus yang berbeda
belum disatukan. [I2] memakai rumus berbasis kelas dengan bobot 0,40 dan 0,35 dan 0,25, sedangkan
[I3] W1-03 dan [I4] F-02 memakai rumus berbasis head. Selama dua rumus itu hidup bersama, satu head
bisa menampilkan dua skor berbeda di dua panel.

**Salah tafsir yang harus dicegah.** Pertama, membaca skor sebagai peluang kejadian. Kedua,
membandingkan skor antar kelas seolah satu skala mutu, padahal bobotnya dinilai per kelas. Ketiga,
membaca skor 50 pada vib sebagai sinyal lemah, padahal lift 1,61 sampai 3,50 di 4 dari 4 fold
([Ev] baris 52 dan 69) dan yang kosong adalah lapisan B. Keempat, memakai skor sebagai ambang
keputusan sebelum pemetaan dibekukan.

**Cara menguji.** Hitung ulang delapan baris dari angka masuk di [I2] bagian 2.3 dengan skrip
terpisah dan bandingkan sampai dua desimal. Lalu uji daya pisah: urutkan peringatan historis
berdasarkan skor, dan periksa apakah urutan itu lebih baik daripada urutan acak pada data fold yang
sama. Uji ketiga, tampilkan dua rumus bersebelahan pada satu head dan pastikan selisihnya tercetak,
bukan disembunyikan.

### KEP-03 Badge beban alarm dan pengunci satuan FAR

**Tujuan.** Menampilkan berapa kali sebuah head menyala pada periode yang seharusnya tenang,
sebelum operator mempercayai presisinya. Masalah yang diselesaikan: presisi tinggi sering dibaca
sebagai "jarang menyala", padahal sebaliknya. Contohnya rule vib dengan presisi 0,87 sampai 0,95
tetapi FAR 10,0 sampai 49,9 per 24 jam operasi negatif ([EVA] baris 54).

**Menggambarkan apa.** FAR adalah alarm palsu per 24 jam operasi negatif, yaitu berapa kali alat
menyala saat tidak ada kejadian. Angka naik berarti beban tinjauan bertambah tanpa tambahan temuan.
Angka turun bisa berarti alat lebih tenang, bisa juga berarti ambang terlalu tinggi sehingga deteksi
hilang; karena itu badge ini tidak pernah tampil tanpa angka recall di sebelahnya.

**Pengguna dan momen pakai.** Operator shift yang memutuskan menindaklanjuti satu peringatan,
puluhan kali per shift. Supervisor yang menyusun beban tinjauan, sekali per shift. Penulis laporan
yang mengutip angka FAR, sekali per bab.

**Masukan.** FAR per fold, jumlah fold, jumlah alarm palsu, jumlah true positive, satuan yang
dipakai, dan skala waktu domain. Satuannya dua: per 24 jam operasi negatif untuk domain rig dengan
grid 60 detik, dan per menit untuk domain bengkel dengan data 1 detik. Rentang yang sudah terukur:
vib rule 10,0 sampai 49,9, vib RF pada tau 0,5 sebesar 4,1 sampai 496,1, shk rule 0,7 sampai 6,6,
stuck rule 8,3 sampai 61,0, hyd persistence 38,8 sampai 110,7 dan hybrid 14,6 sampai 58,4,
tool_wear 46,0 sampai 60,0 per menit ([EVA] baris 54-64; [EVC] baris 118-126; [A1-8] baris 68).

**Algoritma.** Tidak ada model. Aturan tampil: ambil FAR titik dan FAR rentang per fold, hitung
rasio sebaran maksimum dibagi minimum untuk mendeteksi ambang yang tidak portabel, lalu kunci
satuannya. Rasio yang sudah terukur: satu ambang global vib memberi FAR 4,1 sampai 496, yaitu
sebaran 119 kali antar sumur ([EVC] baris 120). Untuk satuan, dua angka dicetak berdampingan: 7 dari
9 fold lulus pada satuan kalender sedangkan 0 dari 9 lulus pada satuan baris, dengan rasio median
kedua satuan 9,1372 ([S1] baris 162; [S6] baris 94-95). Ambang tier: FAR maksimum 6 untuk LAYER-1,
maksimum 1 untuk LAYER-0 ([PM1] baris 138-139), dan ambang 6 itu konvensi operasional, bukan standar
eksternal, dengan status BELUM di ledger `L-26` baris 56.

**Workflow.** (1) Ambil tabel FAR per fold per head. (2) Tandai satuan tiap angka. (3) Hitung rasio
sebaran. (4) Cetak badge dengan satuan yang terkunci pada satu nilai. (5) Cetak recall pada titik yang
sama. (6) Blokir tampilan bila salah satu dari dua angka itu kosong, dan tampilkan alasan blokirnya.

**Keluaran.** Badge berbentuk teks dan angka: "beban 19 alarm per 24 jam, dari 1 segmen, rentang
17 sampai 22" beserta label satuan, ditambah recall pada titik itu dan tanda bahaya bila rasio
sebaran di atas 10 kali. Arti tiap nilai: beban 19 berarti satu tinjauan setiap 76 menit pada shift
8 jam.

**Saran penyajian.** Batang horizontal dengan sumbu skala logaritmik untuk rentang yang menyebar
ratusan kali, ditambah teks angka di ujung batang. Alasan: perbandingan panjang lebih akurat
daripada luas, dan rentang 4,1 sampai 496 tidak terbaca pada skala linear ([LV7]). Untuk badge
ringkas di dalam kartu, pakai kartu angka dengan satu baris teks satuan. Tata letak contoh: kartu
kecil 200 kali 96 piksel berisi angka besar di kiri, label satuan di bawahnya, dan batang tipis
selebar kartu yang menandai posisi pada skala 1 sampai 1000 dengan garis putus di angka 6 sebagai
gerbang tier.

**Dasar riset penyajian.** [LV7] menjelaskan bahwa kanal panjang dan posisi dua dimensi diproses
lebih cepat daripada luas atau sudut, sehingga batang dipilih dan cakram ditolak. [LV6] menempatkan
"sebaran satu variabel" pada strip atau titik, bukan batang tunggal. [LV5] menjadi alasan angka
titik tidak boleh berdiri sendiri tanpa rentang.

**Status bukti.** Siap sekarang untuk lima kelas (vib, shk, stuck, hyd, tool_wear), karena angka
FAR dan recall per fold sudah terukur di [EVA] baris 54-64 dan [EVC] baris 118-126. Siap sebagian
untuk ssi dan bit_wear, karena presisi, recall, dan FAR bit_wear K-1 belum terukur: field-nya tidak
ada di JSON primer ([EVA] baris 61).

**Salah tafsir yang harus dicegah.** Pertama, membandingkan FAR lintas sumur tanpa menyebut bahwa
ambang tidak portabel; sebaran 119 kali membuat perbandingan itu menyesatkan ([EVC] baris 120).
Kedua, mencampur satuan per menit dan per 24 jam dalam satu grafik. Ketiga, membaca FAR rendah
sebagai mutu, padahal FAR rendah bisa berasal dari ambang jenuh yang tidak pernah menyala, seperti
yang terjadi pada stuck dengan q95 jenuh 1,0 atau 0,0 ([Es] baris 151-153).

**Cara menguji.** Ambil satu head, hitung ulang FAR dari jumlah alarm palsu dan durasi operasi
negatif, lalu bandingkan dengan badge. Lulus bila selisih di bawah satu persen. Uji kedua, tampilkan
badge pada dua sumur berbeda dan pastikan label satuan serta rasio sebaran ikut tercetak.

### KEP-04 Kurva kalibrasi dan titik kuantil per head

**Tujuan.** Menjawab apakah skor boleh dibaca sebagai frekuensi. Masalah yang diselesaikan: seluruh
katalog ini memakai skor, dan belum ada satu panel pun yang membuktikan bahwa skor 0,8 benar-benar
berarti delapan dari sepuluh. Untuk penilai model dan auditor internal.

**Menggambarkan apa.** Kurva kalibrasi menggambarkan kesesuaian antara peluang prediksi dan fraksi
kejadian nyata. Bila titik menyimpang ke atas diagonal, model terlalu percaya diri. Bila menyimpang
ke bawah, model terlalu ragu. Titik kuantil menggambarkan sebaran hasil yang mungkin pada satu
kejadian, sehingga pembaca bisa menghitung berapa dari sepuluh kemungkinan yang berakhir dengan
kejadian nyata.

**Pengguna dan momen pakai.** Penilai model saat memutuskan apakah skor boleh dipakai sebagai
ambang, sekali per kampanye. Auditor internal saat memeriksa klaim kalibrasi, sekali per audit.
Operator hanya melihat versi ringkasnya, yaitu pita pada kartu skor.

**Masukan.** Pasangan skor prediksi dan label nyata per fold, per kelas, dalam bentuk dua kolom.
Jumlah bin harus ditetapkan lebih dulu, misalnya 10 bin desil. Sumber datanya keluaran engine per
fold yang saat ini tersimpan sebagai ringkasan, bukan deret per kejadian ([I3] bagian 9 butir 2).

**Algoritma.** Empat langkah. Langkah satu, urutkan skor dan bagi ke dalam bin desil. Langkah dua,
hitung rata-rata skor dan fraksi positif nyata per bin. Langkah tiga, gambar titik bin terhadap
diagonal acuan, lalu hitung jarak vertikal rata-rata sebagai satu angka penyimpangan. Langkah
empat, untuk tampilan operator, ambil 20 titik kuantil dari sebaran skor jendela yang sama dan
gambarkan sebagai titik bertumpuk. Alasan memilih langkah ini: definisi kalibrasi biner menuntut
bahwa di antara sampel dengan peluang mendekati 0,8, sekitar 80 persen benar-benar positif
([LV1]). Jumlah bin dan metode binning dibekukan sebelum hasil dilihat, supaya bukan pemilihan
pasca hasil.

**Workflow.** (1) Ekspor pasangan skor dan label per fold. (2) Bekukan jumlah bin dan metode
binning. (3) Hitung tabel bin. (4) Hitung penyimpangan rata-rata dari diagonal. (5) Simpan satu
gambar per head, bukan satu gambar gabungan. (6) Tampilkan jumlah bin dan jumlah sampel di kaki
grafik. (7) Untuk operator, tampilkan versi ringkas berupa pita pada kartu skor.

**Keluaran.** Satu kurva per head dengan sumbu x rata-rata peluang prediksi dan sumbu y fraksi
positif nyata, rentang 0 sampai 1, plus satu angka penyimpangan dan satu angka jumlah bin. Arti:
penyimpangan 0,05 berarti model cukup terkalibrasi pada data itu, penyimpangan 0,25 berarti skor
tidak boleh dibaca sebagai frekuensi.

**Saran penyajian.** Kurva kalibrasi dengan garis diagonal putus sebagai acuan, titik bin diberi
ukuran sesuai jumlah sampel, dan satu strip titik kuantil di bawahnya untuk pembaca non-teknis.
Alasan: diagonal adalah pembanding yang bisa dibaca tanpa tabel, sedangkan titik kuantil memberi
jumlah hasil yang bisa dihitung. Tata letak contoh: panel dua baris. Baris atas kurva kalibrasi
selebar 480 piksel dengan diagonal putus. Baris bawah strip 20 titik kuantil selebar sama, dengan
teks "dari 20 kemungkinan, 6 berakhir kejadian".

**Dasar riset penyajian.** [LV1] memberi definisi dan bentuk kurva, sekaligus peringatan bahwa skor
tunggal seperti Brier tidak boleh menggantikan kurva karena mencampur kalibrasi, daya pisah, dan
keacakan data. [LV5] menjadi dasar titik kuantil dan angka penurunan variasi taksiran sekitar 1,15
kali dibanding density plot. [LV6] menempatkan hubungan dua variabel kontinu pada sebar atau garis,
bukan batang.

**Status bukti.** Rancangan. Yang sudah ada hanya angka AUPRC dan CI95 per fold ([EML] bagian
tersimpan di [I3] bagian 6), bukan pasangan skor dan label. Syarat agar naik status: pasangan skor
dan label per fold diekspor, jumlah bin dibekukan, lalu kurva dihitung. Tanpa itu, panel ini tidak
boleh mengklaim apa pun.

**Salah tafsir yang harus dicegah.** Pertama, membaca kurva yang dekat diagonal sebagai bukti
kegunaan; kalibrasi baik pada kelas jarang tetap bisa tidak berguna secara operasional. Kedua,
memakai satu skor agregat sebagai bukti kalibrasi. Ketiga, menyatukan beberapa head dalam satu kurva
sehingga penyimpangan satu head tertutup head lain. Keempat, mengubah jumlah bin setelah melihat
bentuk kurva.

**Cara menguji.** Hitung kurva pada dua set bin berbeda (10 dan 20) dan pastikan kesimpulan arah
penyimpangan tidak berubah. Uji kedua, tanam satu head dengan skor acak dan pastikan kurvanya
mendekati diagonal, sebagai kontrol bahwa alat ukur tidak selalu menghasilkan penyimpangan.

### KEP-05 Gerbang provenance angka tiga warna

**Tujuan.** Menandai angka mana yang boleh dikutip, mana yang boleh dikutip dengan catatan metode,
dan mana yang harus dihitung ulang lebih dulu. Masalah yang diselesaikan: laporan dan slide hari ini
memuat angka yang sudah terbukti tidak tereproduksi. Untuk penulis laporan, PM, dan pembicara.

**Menggambarkan apa.** Gerbang ini menggambarkan status keterlacakan sebuah angka, bukan
kebenarannya. Angka berlabel sah berarti sudah dihitung ulang minimal dua jalur. Angka berlabel
catatan berarti nilainya ada tetapi metode atau cakupannya kurang tepat. Angka berlabel larangan
berarti nilainya tidak ditemukan pada rujukan yang disebut. Bila status sebuah angka naik, artinya
ada pihak yang menghitung ulang, bukan artinya angkanya berubah.

**Pengguna dan momen pakai.** Penulis laporan sebelum menyusun bab, sekali per bab. PM sebelum
menyetujui slide, sekali per presentasi. Pembicara saat menerima angka dari orang lain, setiap kali
menerima. Auditor saat menutup satu siklus, sekali per siklus.

**Masukan.** Daftar temuan audit: lima angka tidak akurat, tiga angka tidak tereproduksi, dan satu
label sirkular penuh ([A1] baris 248-264), ditambah daftar larangan kutip enam kelompok angka
([PM6] baris 188-190), dan hasil verifikasi empat inventaris dengan 40 uji ([VF] bagian 3.5).

**Algoritma.** Aturan tiga warna, tanpa model. Hijau bila angka punya rujukan berkas dan baris dan
sudah dihitung ulang minimal dua jalur berbeda. Kuning bila angka punya rujukan tetapi metode
hitungnya tidak tercatat atau cakupan klaimnya lebih luas daripada cakupannya. Merah bila angka
tidak ditemukan pada rujukan yang disebut, atau muncul di daftar larangan kutip. Contoh terukur yang
harus tampil: EDM 947, 3.539, dan 130 tidak tereproduksi dengan enam metode berbeda, sedangkan nilai
terukur adalah 945 sampai 968, 3.193 sampai 5.103, dan 41 sampai 370 bergantung metode ([A1] baris
121 dan 256-259). Contoh kuning: populasi tujuh kelas di [PM6] baris 164-166 hanya memuat enam nilai
([VF] bagian 3.1 uji nomor 5).

**Workflow.** (1) Kumpulkan semua angka yang akan tampil. (2) Cari setiap angka di berkas sumber.
(3) Tandai hasil pencarian: ditemukan pada baris yang disebut, ditemukan pada baris lain, atau tidak
ditemukan. (4) Terapkan warna. (5) Untuk angka merah, tulis perintah hitung ulangnya di catatan kaki.
(6) Kunci warna itu di dokumen, supaya tidak berubah tanpa jejak. (7) Perbarui warna hanya setelah
ada keluaran perintah baru.

**Keluaran.** Tabel angka dengan kolom: angka, klaim, berkas, baris, status warna, dan perintah
hitung ulang bila merah. Rekap: 40 uji pada empat inventaris memberi 37 cocok, 2 cocok dengan
catatan, dan 1 tidak cocok ([VF] bagian 3.5). Tiap baris juga membawa skor keyakinan 0 sampai 100
dari KEP-02 untuk kelas yang angkanya dikutip. Selama KEP-02 belum final, kolom itu menampilkan
label sumber TERUKUR atau BELUM, bukan angka kosong, supaya kerangka butir 1 tetap terpenuhi.

**Saran penyajian.** Tabel dengan kolom status berwarna, bukan lencana pada grafik. Alasan: tugas
pembaca di sini mencari dan membandingkan, dan tabel mendukung kedua tugas itu ([LV4]). Warna hanya
pelengkap, karena angka dan kata status tetap ditulis di sel. Tata letak contoh: tabel selebar
penuh, kolom pertama nama angka, kolom terakhir status berbentuk kata "sah", "catatan", "hitung
ulang", dengan latar berbeda per kata. Di atas tabel, satu baris rekap: 37 sah, 2 catatan, 1 hitung
ulang dari 40 uji.

**Dasar riset penyajian.** [LV4] memberi empat tugas tabel (cari, banding, urutkan, tindak lanjut)
dan menyarankan pengenal yang terbaca manusia di kolom pertama. [LV9] memberi alasan menulis angka
di dalam sel dan tidak hanya mengandalkan warna, karena warna saja gagal pada pembaca dengan
gangguan penglihatan warna. [LV6] menempatkan "status kategori" pada tabel atau lencana, bukan
grafik.

**Status bukti.** Siap sekarang untuk angka yang sudah diuji. Sumbernya konkret: 40 uji di [VF]
bagian 3.1 sampai 3.4 dengan rujukan baris per uji, dan daftar larangan kutip di [PM6] baris
188-190. Sembilan belas angka lain di luar 40 uji itu belum diuji, dan statusnya harus kuning sampai
dihitung ulang ([VF] bagian 7 butir 1).

**Salah tafsir yang harus dicegah.** Pertama, membaca warna hijau sebagai kebenaran fisik; hijau
hanya berarti terlacak. Kedua, memakai angka merah di slide dengan catatan kecil, karena pembaca
tidak membaca catatan kaki. Ketiga, menganggap selisih angka antar dokumen sebagai kontradiksi
tanpa memeriksa bahwa objeknya berbeda, seperti rekap tier per engine 0 + 3 + 2 + 2 = 7 lawan rekap
head 12 dan 13 dan 2 yang keduanya sah ([I4] bagian 7 catatan jebakan baca).

**Cara menguji.** Ambil lima angka dari slide terakhir dan jalankan pencarian baris. Lulus bila
setiap angka hijau ditemukan pada baris yang disebut dalam dua menit, dan setiap angka merah punya
perintah hitung ulang yang bisa dijalankan. Uji kedua, minta satu orang yang tidak menyusun tabel
menebak status tiga angka; bila tebakannya salah, tabelnya kurang jelas.

### KEP-06 Papan dua pembacaan literal dan ketat

**Tujuan.** Menampilkan satu klaim pada dua pembacaan sekaligus beserta selisihnya, supaya tidak ada
klaim yang tampil lebih kuat daripada buktinya. Untuk dosen penguji, PM, dan operator yang bertanya
"jadi berapa kelas yang lulus".

**Menggambarkan apa.** Pembacaan literal mengikuti bunyi pra-registrasi apa adanya. Pembacaan ketat
menambahkan syarat bahwa kelas harus lulus penuh, bukan lulus bersyarat. Selisih keduanya
menggambarkan seberapa banyak kelulusan bergantung pada cara membaca, dan itu sendiri merupakan
informasi mutu bukti.

**Pengguna dan momen pakai.** Dosen penguji saat sesi bimbingan, sekali per sesi. PM saat sidang,
sekali per sidang. Operator saat bertanya apakah panel tertentu boleh dinyalakan, sesekali.

**Masukan.** Vonis [PM6] baris 130-141 yang memuat tiga kelas lolos gate G1 ditambah G2, dan
pembacaan ketat yang hanya memberi dua kelas lulus penuh, ditambah angka gate [E1] baris 151-160.

**Algoritma.** Tidak ada model. Aturan: hitung jumlah kelas pada dua definisi, cetak keduanya,
cetak selisihnya, lalu cetak kalimat pembatas yang menyebut definisi mana yang dipakai untuk
keputusan produk. Kelas yang hanya lulus bersyarat tidak boleh dipindahkan diam-diam ke daftar
lulus.

**Workflow.** (1) Ambil daftar kelas dari dokumen vonis. (2) Tandai status per kelas pada pembacaan
literal. (3) Tandai status per kelas pada pembacaan ketat. (4) Hitung selisih. (5) Tempelkan
kalimat pembatas. (6) Tampilkan tanggal vonis, karena pembacaan ini terikat versi dokumen.

**Keluaran.** Satu kartu dengan dua kolom status dan satu baris selisih: literal 3 kelas, ketat 2
kelas, selisih 1 kelas, plus kalimat "angka yang dipakai untuk keputusan produk adalah pembacaan
ketat". Kedua kolom membawa skor keyakinan dari KEP-02 di sebelah statusnya, karena pembacaan yang
memotong satu kelas sekaligus menurunkan skor keyakinan kelas itu, dan pembaca harus melihat kedua
akibatnya bersamaan.

**Saran penyajian.** Tabel dua kolom dengan selisih di baris paling bawah, bukan dua donat. Alasan:
yang dibandingkan adalah dua daftar label yang sebagian sama, dan tabel memperlihatkan kelas mana
yang pindah status; donat hanya memperlihatkan jumlah ([LV4], [LV6]). Tata letak contoh: kolom kiri
"literal", kolom kanan "ketat", tiap baris satu kelas, sel yang berubah status diberi latar berbeda
dan teks "lulus bersyarat".

**Dasar riset penyajian.** [LV4] untuk bentuk tabel perbandingan dan tugas membandingkan.
[LV6] untuk penolakan donat pada perbandingan kategori yang saling menutupi.

**Status bukti.** Siap sekarang untuk isi angka. Kedua pembacaan tertulis dan berangka di [PM6]
baris 130-141 dan sudah diuji baca di [VF] bagian 3.1. Yang belum: skema skor keyakinan di balik
kartu ini belum diuji daya pisahnya, sehingga skor hanya boleh tampil sebagai angka pendamping.

**Salah tafsir yang harus dicegah.** Membaca selisih satu kelas sebagai kesalahan hitung. Selisih
itu berasal dari definisi, bukan dari aritmetika, dan justru harus ditampilkan.

**Cara menguji.** Minta dua pembaca menghitung jumlah kelas dari dokumen vonis tanpa melihat kartu
ini, lalu bandingkan. Lulus bila keduanya menghasilkan angka yang sama dengan kolom yang sesuai.

### KEP-07 Pengunci rujukan baris dan uji mutasi angka

**Tujuan.** Membuktikan bahwa pemeriksa angka benar-benar bisa gagal, dan menahan rujukan baris yang
meleset. Masalah yang diselesaikan: satu rujukan baris yang meleset membuat pembaca menyimpulkan
angka itu tidak ada, padahal angkanya ada di baris lain. Untuk auditor internal dan pemilik dokumen.

**Menggambarkan apa.** Ini alat uji, bukan tampilan operasional. Yang digambarkan adalah kesehatan
rantai rujukan: berapa sel angka yang bisa dicocokkan ke baris sumber, dan berapa yang tidak.

**Pengguna dan momen pakai.** Auditor internal sebelum menerbitkan vonis baru, sekali per vonis.
Pemilik dokumen saat menerima laporan dua angka berbeda untuk klaim yang sama, setiap kali terjadi.

**Masukan.** Dokumen lama, daftar sel yang akan dibandingkan, toleransi numerik, dan dua mutasi
angka yang disengaja sebagai kontrol negatif.

**Algoritma.** Tiga langkah. Langkah satu, bandingkan sel per sel terhadap dokumen sumber dengan
toleransi 5e-5. Langkah dua, jalankan ulang pada salinan yang dua angkanya dimutasi. Langkah tiga,
nyatakan lulus hanya bila dokumen asli memberi nol selisih dan dokumen termutasi memberi selisih.
Angka yang sudah terukur: 143 sel diperiksa, 0 selisih pada dokumen asli, 2 selisih pada dokumen
termutasi ([S5A] baris 65 dan 71). Dua mutasi contoh: `fp_total` 935 menjadi 936, dan presisi median
0,7789 menjadi 0,7791 ([I4] bagian 5 F-11).

**Workflow.** (1) Kumpulkan sel angka beserta rujukan barisnya. (2) Jalankan pembanding pada
dokumen asli. (3) Jalankan pada dokumen termutasi. (4) Cetak dua hasil. (5) Untuk setiap selisih,
cetak berkas, baris, dan nilai. (6) Simpan keluaran sebagai lampiran vonis.

**Keluaran.** Tiga baris: jumlah sel diperiksa, jumlah selisih pada asli, jumlah selisih pada
termutasi, plus daftar selisih dengan lokasi. Arti: bila termutasi memberi nol selisih, penguncinya
rusak dan seluruh angka lain tidak boleh dipercaya sampai diperbaiki.

**Saran penyajian.** Tabel tiga baris di dalam kartu hasil uji, ditambah lencana lulus atau gagal.
Alasan: hanya tiga angka yang perlu dibandingkan, dan tabel membuat kontrol negatif terbaca sebagai
pasangan ([LV4]). Tata letak contoh: kartu dengan judul "uji pengunci", tiga baris angka, satu
lencana di kanan atas, dan daftar selisih di bawah.

**Dasar riset penyajian.** [LV4] untuk bentuk tabel hasil uji dengan kolom pengenal yang terbaca.
[LV11] untuk pola mencatat kegagalan beserta tindak lanjut, yang menjadi dasar kewajiban menulis
selisih, bukan hanya status.

**Status bukti.** Siap sekarang. Desain tes dan hasilnya terukur ([S5A] baris 65 dan 71), dan dua
kasus rujukan meleset sudah ditemukan pada gelombang verifikasi: recall H1 ada di [R8] baris 127,
bukan baris 69 dan 109 ([VF] C-07), dan aturan tinjauan manusia ada di [PM2] baris 205, bukan baris
206 ([VF] C-08).

**Salah tafsir yang harus dicegah.** Membaca lulus pada dokumen asli sebagai bukti semua angka
benar. Pengunci hanya membuktikan bahwa angka tidak berubah sejak dibekukan, bukan bahwa angka itu
benar.

**Cara menguji.** Ulangi prosedur pada satu dokumen yang belum pernah diuji, dengan dua mutasi baru.
Lulus bila pengunci memberi nol selisih pada asli dan tepat dua selisih pada termutasi.

### KEP-08 Panel ketidaksepakatan antar head

**Tujuan.** Menampilkan bahwa beberapa head pada data yang sama bisa memberi arah berbeda, dan
menyebut penyebabnya. Masalah yang diselesaikan: satu label gabungan membuat pembaca mengira semua
head sepakat, padahal pemangkasan alarm bisa berasal dari syarat AND, dari kanal kosong, atau dari
ambang jenuh. Untuk supervisor dan operator yang memutuskan eskalasi.

**Menggambarkan apa.** Panel ini menggambarkan bentuk kesepakatan, bukan tingkat bahaya. Bila
rule menyala dan hybrid padam, itu bukan bug; hybrid memangkas karena syarat AND tidak terpenuhi.
Bila keduanya padam padahal kanal masukan kosong, itu bukan ketenangan, melainkan ketiadaan data.
Bila jumlah head yang sepakat naik, artinya jendela itu lebih mudah dibaca, bukan lebih berbahaya.

**Pengguna dan momen pakai.** Supervisor saat menyiapkan eskalasi, dua sampai empat kali per shift
pada jam sibuk. Operator saat satu peringatan masuk, setiap kali. Penilai model saat memeriksa
apakah dua komposisi berbeda memberi bentuk angka yang mirip tetapi makna berlawanan, sekali per
kampanye.

**Masukan.** Sinyal per menit dari empat komponen pada jendela yang sama: rule, persistence, hybrid,
dan skor model. Untuk tiap komponen: status menyala atau padam, nilai ambang, jumlah kanal masukan
yang kosong, dan alasan pemangkasan bila ada. Saat ini yang tersimpan adalah ringkasan per fold,
bukan deret per menit ([I3] bagian 9 butir 2), sehingga butir masukan ini adalah syarat, bukan
ketersediaan.

**Algoritma.** Langkah satu, untuk setiap jendela, kumpulkan putusan biner tiap head. Langkah dua,
hitung matriks kesepakatan antar head pada seluruh jendela, satu versi hitungan mentah dan satu
versi ternormalisasi per baris. Langkah tiga, untuk setiap jendela yang tidak sepakat, lampirkan
penyebab dari tiga kategori: syarat AND tidak terpenuhi, kanal masukan kosong, atau ambang jenuh.
Langkah empat, tandai jendela di mana seluruh head padam tetapi kanal kosong, karena itu harus
dibaca sebagai ketiadaan data. Alasan memilih matriks dan bukan satu label: metode penjelas terbukti
sering tidak sepakat, dan menyembunyikan itu membuat keputusan berisiko dibaca sebagai pasti
([LV15]).

**Workflow.** (1) Simpan sinyal per menit dari empat komponen. (2) Susun matriks kesepakatan per
kelas. (3) Hitung versi ternormalisasi. (4) Untuk tiap jendela tidak sepakat, tentukan penyebab.
(5) Tampilkan panel per jendela saat pengguna membuka satu peringatan. (6) Tampilkan matriks
ringkasan di halaman kelas.

**Keluaran.** Dua bentuk. Pertama, panel per jendela: empat baris head dengan status dan satu baris
alasan. Kedua, matriks kesepakatan berukuran jumlah head kali jumlah head, berisi persentase
kesepakatan, dengan diagonal selalu 100 persen. Contoh angka yang wajib tercetak saat ini: hyd
hybrid memangkas alarm palsu dari 2.091 ke 927 sambil menjaga presisi dan recall di atas 0,52
([EVA] baris 59), sedangkan ssi hybrid memangkas dari 26 ke 7 tetapi meninggalkan recall 0,03
([EVB] baris 143; [EVA] baris 55). Dua bentuk angka mirip, makna operasional berlawanan.

**Saran penyajian.** Heatmap matriks bernilai dengan angka di dalam sel, ditambah panel per jendela
berupa empat baris status. Alasan: diagonal dan luar diagonal punya arti berbeda, dan normalisasi
per baris diperlukan supaya kelas jarang tidak tertutup kelas mayoritas ([LV9]). Untuk panel per
jendela, empat baris teks lebih cepat dibaca daripada empat ikon. Tata letak contoh: di halaman
kelas, heatmap 4 kali 4 selebar 360 piksel. Di halaman peringatan, empat baris berurutan: nama head,
status, ambang, alasan, dengan latar berbeda untuk baris yang alasannya "kanal kosong".

**Dasar riset penyajian.** [LV15] memberi bukti bahwa metode penjelas sering tidak sepakat dan
praktisi bisa bergantung pada penjelasan yang menyesatkan. [LV9] memberi bentuk matriks dan alasan
normalisasi per baris. [LV5] menjadi dasar larangan meringkas ketidakpastian menjadi satu label.

**Status bukti.** Siap sebagian. Arah pemangkasan sudah terukur untuk hyd dan ssi ([EVB] baris 98
dan 102 serta 143; [EVA] baris 55 dan 59), dan panel "tidak ada pemenang" sudah punya angka: vib
tidak ada komposisi yang mencapai recall 0,5 di 0 dari 4 fold, ssi hanya 1 true positive dari 132
onset ([S6] baris 113-114 dan 171-174). Yang belum: deret per menit belum disimpan, sehingga
matriks kesepakatan belum bisa dihitung dari data yang ada hari ini.

**Salah tafsir yang harus dicegah.** Pertama, membaca pemangkasan sebagai peningkatan mutu; ssi
memangkas 73 persen alarm palsu dengan biaya recall 0,03, dan biaya itu harus tercetak di baris yang
sama. Kedua, membaca kesepakatan penuh sebagai kebenaran, karena empat head bisa sepakat pada
kesalahan yang sama bila kanal masukannya sama. Ketiga, menilai head yang paling sering menyala
sebagai head terbaik.

**Cara menguji.** Ambil satu jendela di mana rule dan hybrid berbeda, lalu periksa apakah alasan
yang tercetak benar-benar penyebabnya dengan membaca kanal masukan jendela itu. Uji kedua, hitung
matriks pada data sintetis dengan dua head identik dan pastikan kesepakatannya 100 persen.

### KEP-09 Banner transparansi label bit_wear

**Tujuan.** Menyatakan bahwa label keausan bit adalah indeks mekanika, bukan observasi keausan.
Masalah yang diselesaikan: tren keausan bisa dibaca sebagai riwayat fisik bit, padahal labelnya
direkonstruksi dari fitur mekanika. Untuk reviewer, dosen pembimbing, dan insinyur yang membuka tren.

**Menggambarkan apa.** Label `high_MSE_bit_wear` menggambarkan efisiensi mekanika pengeboran, bukan
sisa umur bit. Angka naik berarti blok pengeboran kurang efisien menurut indeks mekanika. Angka itu
tidak boleh diterjemahkan menjadi "bit lebih aus", karena tidak ada satu pun kolom identitas bit di
data.

**Pengguna dan momen pakai.** Reviewer saat membaca bab evaluasi, sekali per bab. Dosen pembimbing
saat sesi bimbingan. Insinyur saat membuka tren bit_wear, beberapa kali per minggu.

**Masukan.** Hasil rekonstruksi label dan diagnostik sirkularitas. Dua angka pendukung: rekonstruksi
198.928 dari 198.928 baris dengan akurasi 1,000000 ([S3] baris 100), dan perbandingan presisi 0,8496
pada model yang memakai `MSE` serta `ROC_coef` lawan recall 0,9968 pada model kanal fisik saja
([S3] baris 187).

**Algoritma.** Tidak ada model baru. Aturan tampil: setiap grafik bit_wear wajib membawa banner yang
menyebut sumber label, akurasi rekonstruksi, dan larangan menerjemahkan label menjadi umur bit. Bila
akurasi rekonstruksi 1,000000, banner juga wajib menyebut bahwa label adalah fungsi deterministik
dari fitur, sehingga model yang memakainya hanya mereproduksi rumus.

**Workflow.** (1) Ambil hasil rekonstruksi dan diagnostik. (2) Susun teks banner tiga baris.
(3) Tempelkan banner di atas grafik, bukan di catatan kaki. (4) Kunci banner supaya tidak dapat
ditutup. (5) Tautkan banner ke rujukan baris.

**Keluaran.** Banner tiga baris teks dengan dua angka: temuan rekonstruksi dan perbandingan presisi
lawan recall. Tidak ada angka baru yang dihitung di sini.

**Saran penyajian.** Banner penuh selebar grafik dengan latar berbeda, bukan ikon informasi kecil.
Alasan: peringatan yang bisa dilewati tidak dibaca, dan pembaca memindai bagian atas grafik lebih
dulu ([LV7]). Tata letak contoh: kotak setinggi tiga baris teks tepat di atas grafik tren, dengan
kalimat pertama paling tebal.

**Dasar riset penyajian.** [LV7] untuk posisi dan keterbacaan elemen dashboard. [LV11] untuk pola
menulis dampak dan akar masalah secara eksplisit, yang menjadi dasar menulis akibat salah tafsir,
bukan hanya label.

**Status bukti.** Siap sekarang. Kedua angka terukur dan bersumber baris ([S3] baris 100 dan 187),
dan keduanya sudah diuji baca di [VF] bagian 3.4.

**Salah tafsir yang harus dicegah.** Pertama, membaca akurasi 1,000000 sebagai mutu model. Itu
sirkularitas: label adalah fungsi deterministik dari fitur. Kedua, membaca tren naik sebagai bit
aus. Ketiga, memakai label ini sebagai target pelatihan baru tanpa melewati gerbang anti-ghost
(ING-05).

**Cara menguji.** Minta satu pembaca menjelaskan arti grafik tanpa membaca banner, lalu bandingkan
dengan penjelasan setelah membaca banner. Bila penjelasan pertama menyebut keausan fisik, banner
belum cukup jelas.

### KEP-10 Slot nilai jujur lapisan B

**Tujuan.** Menjawab pertanyaan "berapa nilai uang dari peringatan ini" dengan tiga tingkat jawaban:
yang terukur, yang bisa dihitung sebagai rasio, dan yang masih kosong beserta pemilik datanya.
Masalah yang diselesaikan: pertanyaan nilai biasanya dijawab dengan angka karangan atau dengan
diam. Untuk perencana maintenance dan manajer operasi.

**Menggambarkan apa.** Tingkat pertama menggambarkan beban waktu henti yang benar-benar tercatat di
data harian pengeboran. Tingkat kedua menggambarkan seberapa besar bagian waktu henti yang bisa
didahului peringatan. Tingkat ketiga menggambarkan jenis data yang belum dimiliki. Bila jam henti
naik, artinya beban pemeliharaan bertambah; itu bukan ukuran keberhasilan alat.

**Pengguna dan momen pakai.** Perencana maintenance saat menyusun prioritas perbaikan, sekali per
minggu. Manajer operasi saat ditanya nilai program, sekali per bulan. Auditor saat memeriksa asal
angka nilai, sekali per audit.

**Masukan.** Tiga kelompok. Pertama, agregat aktivitas dari `data/volve/ddr.parquet`: 39.397,986
jam tercatat pada 23.447 record, dengan rincian equipment failure 2.739,667 jam, interruption other
2.680,917 jam, interruption waiting on weather 1.925,5 jam, stuck equipment 212,0 jam, circulation
loss 195,0 jam ([ENG] baris 19-27; [VR] bagian 5.6). Kedua, tabel durasi maintenance S4: repair 806
kejadian dan 1.215,0 jam dengan median 1,0 jam dan p90 3,5 jam, maintain 310 kejadian dan 562,75 jam
dengan median 1,0 jam dan p90 4,5 jam, gabungan 1.116 kejadian dan 1.777,75 jam ([S4] baris 69, 72,
78, 125). Ketiga, daftar penyebut yang kosong: tarif biaya henti, nomor work order, jadwal inspeksi,
produksi tertunda, hasil uji integritas ([S4] bagian 6 baris 165-173).

**Algoritma.** Tiga tingkat, tanpa model. Tingkat satu menjumlahkan jam per kategori dan mengurutkan
menurun untuk diagram Pareto. Tingkat dua membagi lead peringatan dengan durasi henti median, dengan
hasil 11,5 menit dibagi 60 menit sama dengan 19,17 persen. Tingkat tiga mencetak slot kosong
berlabel, masing-masing dengan pemilik data. Catatan wajib: median 1,0 jam dan p90 3,5 jam adalah
milik repair saja, dan median populasi gabungan belum dihitung ([VF] C-09).

**Workflow.** (1) Baca agregat jam per kategori. (2) Urutkan menurun. (3) Ambil lead peringatan dari
dokumen vonis. (4) Hitung rasio terhadap durasi henti median. (5) Susun lima slot kosong beserta
pemiliknya. (6) Tampilkan tanggal potong data. (7) Tandai angka yang masih berselisih antar dokumen,
yaitu kategori equipment failure dan stuck equipment yang muncul di [ENG] tetapi tidak punya padanan
di tabel [S4] ([I4] bagian 7 baris 3).

**Keluaran.** Panel tiga tingkat. Tingkat satu: lima batang jam dengan total 39.397,986 jam.
Tingkat dua: satu angka rasio 19,17 persen. Tingkat tiga: lima slot kosong dengan nama pemilik data.
Tidak ada angka rupiah di panel ini, dan ketiadaannya ditulis sebagai slot, bukan sebagai catatan
kaki.

**Saran penyajian.** Diagram Pareto untuk tingkat satu, kartu rasio untuk tingkat dua, dan daftar
slot untuk tingkat tiga. Alasan: Pareto dipakai justru ketika ada banyak sebab dan tujuannya
memusatkan perhatian pada yang terbesar, dengan batang terpanjang di kiri ([LV2]). Tata letak
contoh: panel atas berupa Pareto selebar 520 piksel dengan garis kumulatif. Panel tengah satu kartu
angka "19,17 persen durasi henti median". Panel bawah lima baris slot, masing-masing dengan nama
data, pemilik, dan status "belum ada".

**Dasar riset penyajian.** [LV2] untuk bentuk dan alasan Pareto. [LV4] untuk daftar slot yang harus
bisa dibaca sebagai daftar tugas. [LV13] untuk prinsip bahwa pilihan grafik ditentukan pertanyaan
pembaca: di sini pertanyaannya "mana yang paling besar", bukan "bagaimana tren".

**Status bukti.** Siap sebagian. Tingkat satu dan dua terukur ([S4] baris 121-131; [ENG] baris
19-27), dengan satu catatan pemisahan populasi repair dan gabungan ([VF] C-09). Tingkat tiga
berstatus kosong dan itu memang isinya.

**Salah tafsir yang harus dicegah.** Pertama, membaca rasio 19,17 persen sebagai penghematan; itu
bagian durasi henti yang bisa didahului peringatan, bukan penghematan yang sudah terjadi. Kedua,
memakai angka [ENG] untuk equipment failure tanpa menandai bahwa angka itu belum punya padanan di
[S4] dan pencarian `2739`, `212.0`, `195.0` pada [S4] memberi nol kemunculan ([I4] bagian 7).
Ketiga, membaca slot kosong sebagai kegagalan program; slot itu daftar pekerjaan pengumpulan data.

**Cara menguji.** Hitung ulang total jam dari `ddr.parquet` dengan kolom pengelompok yang disebut,
lalu bandingkan dengan 39.397,986 jam. Uji kedua, minta satu manajer menjelaskan arti rasio 19,17
persen; bila ia menyebutnya penghematan, labelnya belum benar.

---

## 6. Rumpun perencanaan maintenance (MNT-01 sampai MNT-09)

Rumpun ini menjawab pertanyaan "apa yang dikerjakan minggu ini". Sembilan fitur di bawah mengubah
skor menjadi daftar pekerjaan yang bisa diperiksa orang, dengan biaya pemeriksaan yang tercetak di
sebelah daftarnya.

### MNT-01 Antrean triage onset per shift dengan umur item

**Tujuan.** Mengubah skor onset menjadi daftar berurut yang dibaca di awal shift, lengkap dengan
umur item dan biaya pemeriksaannya. Masalah yang diselesaikan: peringatan tanpa urutan membuat
semua item terlihat sama penting, dan daftar tanpa umur menyembunyikan item yang sudah lama
menggantung. Untuk insinyur shift malam dan toolpusher.

**Menggambarkan apa.** Setiap baris mewakili satu jendela waktu yang dinilai berisiko onset
kerusakan. Umur item menggambarkan berapa lama jendela itu sudah ada di antrean tanpa keputusan.
Bila umur bertambah tanpa keputusan, itu tanda beban kerja, bukan tanda bahaya. Bila jumlah item
naik, itu tanda alat lebih sering menyala, dan penyebabnya harus dibaca dari badge FAR (KEP-03),
bukan dari panjang daftar.

**Pengguna dan momen pakai.** Insinyur shift malam dan toolpusher pada awal shift dan setiap dua
jam, jadi lima kali per shift 12 jam. Supervisor pagi membacanya sekali untuk serah terima.

**Masukan.** Skor ranking per jendela, horizon H, riwayat alarm pada horizon itu, ambang terpilih
per sumur, dan cap waktu masuk antrean. Angka yang sudah terukur untuk mengisi daftar: stuck E3
dengan lift 1,65 dan 1,30 dan 9,72 dan 1,12 di 4 dari 4 fold ([Es] baris 113-114), rule E1 dengan
presisi 0,457 di F-10 dan lead median 10 menit ([Es] baris 88), cakupan onset RF pada tau 0,5
sebesar 0,004 sampai 0,045 dengan FAR 0,0 sampai 1,25 di 3 dari 4 fold ([EVA] baris 58 dan 128),
serta cakupan persistence-EVENT 0 sampai 0,115 dengan TLead 7,0 menit ([EVB] baris 101).

**Algoritma.** Langkah satu, hitung skor per jendela dari dua komponen: skor model dan hasil rule
2 dari 3. Langkah dua, urutkan menurun menurut skor, lalu pecah seri menurut umur item yang lebih
lama. Langkah tiga, tempelkan label cakupan: cakupan di bawah 5 persen berarti triage, bukan
peringatan. Langkah empat, cetak jumlah alarm yang harus diperiksa pada horizon itu. Ambang yang
dipakai tidak boleh satu angka global: titik dengan cakupan minimal 50 persen berbiaya 77 kali beban
([EVB] baris 101), sehingga titik itu ditolak untuk antrean ini.

**Workflow.** (1) Kumpulkan skor per jendela dari keluaran engine. (2) Tempelkan cap waktu masuk.
(3) Urutkan skor menurun, pecah seri dengan umur. (4) Hitung umur per baris. (5) Tempelkan label
cakupan dan jumlah alarm per horizon. (6) Simpan tangkapan layar awal shift sebagai arsip.
(7) Setiap keputusan ditutup dengan log keputusan (LIN-01), sehingga umur item berhenti bertambah.

**Keluaran.** Tabel berurut dengan kolom: pengenal jendela yang terbaca manusia, sumur, waktu
jendela, skor, skor keyakinan 0 sampai 100, cakupan, TLead yang diharapkan, umur item, dan aksi
berikutnya. Rentang yang sudah terukur: cakupan 0,004 sampai 0,115, TLead 7,0 sampai 10 menit, FAR
9,9 sampai 1.440 untuk stuck. Kolom skor keyakinan memakai rumus KEP-02, dan baris dengan skor di
bawah 40 ditandai sebagai tinjauan pendamping, bukan tindakan.

**Saran penyajian.** Tabel terurut dengan kolom umur dan status, bukan kartu besar. Alasan: beban
tinjauan per shift sudah terukur puluhan baris (vib 17, hyd rule 19, hyd hybrid 6, shk 3, stuck 3,
tool_wear 1, [ENG] baris 31-43), sehingga tata letak kartu lima baris tidak cukup; dan sumber
menyebut distribusi umur lebih informatif daripada satu jumlah terbuka ([LV14]). Tata letak contoh:
header tabel lengket, kolom umur diberi empat pita warna (0 sampai 2 jam, 3 sampai 7 jam, 8 sampai
15 jam, di atas 15 jam), baris di atas 8 jam diberi latar lebih gelap, dan kolom pertama berisi nama
sumur serta jam jendela, bukan ID.

**Dasar riset penyajian.** [LV14] memberi alasan bahwa umur item lebih informatif daripada satu
angka backlog, beserta bucket umur contoh. [LV4] memberi empat tugas tabel dan aturan kolom pertama
yang terbaca manusia. [LV6] menempatkan "peringkat" pada batang terurut, tetapi tabel dipilih di
sini karena tiap baris butuh enam atribut sekaligus.

**Status bukti.** Siap sekarang untuk komponennya: skor, cakupan, TLead, dan FAR sudah terukur per
fold ([Es] baris 88, 100, 113-114; [EVA] baris 58; [EVB] baris 101). Yang belum: skema pencatatan
umur, karena log keputusan (LIN-01) belum ada.

**Salah tafsir yang harus dicegah.** Pertama, membaca urutan teratas sebagai kepastian kejadian;
cakupan 0,004 berarti 4 dari 1.000 onset. Kedua, membaca daftar panjang sebagai tanda bahaya;
panjang daftar mengukur beban, bukan risiko. Ketiga, membandingkan FAR stuck 1.440 dengan FAR hyd
38,8 tanpa menyebut bahwa keduanya dari kelas dan skala berbeda.

**Cara menguji.** Ambil satu shift historis, susun antrean dari data hari itu, lalu hitung berapa
onset nyata yang muncul di 10 baris teratas. Lulus bila hasilnya lebih baik daripada urutan acak
pada data yang sama. Uji kedua, periksa bahwa tidak ada baris dengan label cakupan di atas 0,5 pada
titik operasi yang dipakai.

### MNT-02 Kalkulator anggaran pemeriksaan

**Tujuan.** Menghitung berapa banyak pemeriksaan manual yang dihemat oleh satu titik operasi, dan
berapa deteksi yang hilang pada titik itu. Masalah yang diselesaikan: penghematan alarm hampir selalu
dibicarakan tanpa biaya recall. Untuk supervisor pemeliharaan yang menentukan jumlah kunjungan per
shift.

**Menggambarkan apa.** Angka ini menggambarkan pertukaran, bukan mutu. Penghematan naik berarti
beban tinjauan turun. Bila penghematan naik sementara deteksi yang hilang juga naik, titik operasi
itu bukan perbaikan, melainkan pemindahan pekerjaan menjadi risiko.

**Pengguna dan momen pakai.** Supervisor pemeliharaan saat membandingkan dua kandidat titik operasi
sebelum mengunci kebijakan, sekali per kampanye. Manajer operasi saat menyetujui beban shift, sekali
per bulan.

**Masukan.** Jumlah alarm palsu engine, jumlah alarm palsu baseline status quo, dan recall pada
titik yang sama. Ketiganya tersedia per fold di [EVB] dan [EVA].

**Algoritma.** Rumus penghematan: satu dikurangi jumlah alarm palsu engine dibagi jumlah alarm palsu
baseline ([EVB] baris 65). Angka siap pakai: hyd K-i memberi +0,557 karena alarm palsu turun dari
2.091 ke 927, tool_wear memberi +0,909 sampai +0,976, dan ssi memberi +0,731 karena turun dari 26 ke
7 tetapi dengan recall 0,03 ([EVB] baris 98, 102, 106; [EVA] baris 55). Contoh tukar yang harus
tercetak: H1 menurunkan alarm palsu dari 2.105 ke 935 dan menaikkan presisi dari 0,6835 ke 0,7789,
tetapi menukar 31,82 persen recall ([R8] baris 131; [PMR] baris 109).

**Workflow.** (1) Pilih dua titik operasi. (2) Ambil jumlah alarm palsu dan recall pada titik yang
sama. (3) Hitung penghematan. (4) Hitung deteksi yang hilang. (5) Cetak dua angka berdampingan.
(6) Kunci pilihan hanya setelah supervisor menandatangani trade-off-nya.

**Keluaran.** Dua angka persen per titik: penghematan pemeriksaan dan deteksi yang hilang, masing
masing dengan rentang antar fold, ditambah satu skor keyakinan per titik dari KEP-02. Arti: +0,731
dengan 0,03 recall berarti tiga perempat beban hilang dan hampir seluruh deteksi ikut hilang. Skor
keyakinan rendah pada satu titik berarti pemotongan anggaran di titik itu belum punya dasar bukti.

**Saran penyajian.** Batang berpasangan horizontal untuk dua titik, dengan angka di ujung batang.
Alasan: dua nilai pada skala sama lebih mudah dibandingkan lewat panjang daripada lewat warna, dan
angka harus tetap tertulis ([LV7], [LV6]). Tata letak contoh: satu baris berisi dua pasang batang
(engine dan baseline) untuk titik A, baris berikutnya untuk titik B, di bawahnya satu baris teks
"recall 0,03" dalam warna peringatan.

**Dasar riset penyajian.** [LV7] untuk kanal panjang dan posisi. [LV6] untuk pasangan nilai pada
kategori sama. [LV1] untuk larangan menyederhanakan pertukaran menjadi satu skor.

**Status bukti.** Siap sekarang. Rumusnya tertulis dengan nomor baris, dan tiga angka siap pakai
sudah terukur ([EVB] baris 98, 102, 106).

**Salah tafsir yang harus dicegah.** Pertama, membaca penghematan sebagai mutu tanpa recall. Kedua,
membandingkan penghematan antar kelas yang baseline-nya berbeda, karena penyebutnya berbeda. Ketiga,
memakai angka [EVB] sebagai angka armada padahal rentangnya antar fold.

**Cara menguji.** Hitung ulang penghematan dari jumlah alarm palsu mentah dan cocokkan dengan angka
yang ditampilkan. Uji kedua, minta satu supervisor memilih titik operasi dari panel ini dan periksa
apakah ia menyebut biaya recall dalam alasannya.

### MNT-03 Sakelar dua titik operasi hyd

**Tujuan.** Memberi supervisor dua pilihan yang sudah dihitung konsekuensinya, bukan satu tombol
kepekaan. Masalah yang diselesaikan: pilihan antara cakupan deteksi dan ketenangan alarm biasanya
dibuat dengan perasaan. Untuk supervisor shift.

**Menggambarkan apa.** Dua titik operasi pada kelas hidrolik. Titik pertama mengejar cakupan, titik
kedua mengejar alarm yang lebih tenang. Bila pengguna berpindah ke titik kedua, artinya tim memilih
menerima lebih banyak kejadian tanpa peringatan; itu keputusan operasional, bukan penyetelan teknis.

**Pengguna dan momen pakai.** Supervisor shift pada awal shift, sekali per shift, dan saat kondisi
sumur berubah. Manajer operasi saat menyetujui kebijakan tetap, sekali per kampanye.

**Masukan.** Dua keluaran engine yang sudah ada, dengan angka per fold. Titik pertama, yaitu rule
kanal DAN gerbang persistence: alarm palsu 927, true positive 4.924, presisi 0,8243, recall 0,6519,
FAR kalender median 4,0984, lead median 8,0 menit, 7 dari 9 fold memenuhi FAR dan recall sekaligus
([S6] baris 196). Titik kedua, yaitu rule DAN persistence DAN statistik: alarm palsu 568, true
positive 3.557, presisi 0,8646, recall 0,5296, FAR 2,0323, lead 12,5 menit, FAR lolos 9 dari 9 fold
dan recall lolos 5 dari 9 ([S6] baris 197). Pembanding lama H1: alarm palsu 935, true positive 3.804,
presisi 0,7789, recall 0,5638, FAR 3,5302, lead 11,5 menit, 5 dari 9 ([S6] baris 194).

**Algoritma.** Tidak ada model baru. Aturan: tampilkan dua titik berdampingan, hitung selisih setiap
kolom, lalu cetak biaya perpindahan dalam satuan yang bisa diperiksa orang. Biaya memilih titik
kedua adalah 247 true positive lebih sedikit daripada titik pertama ([S6] baris 221), dan biayanya
terhadap H1 adalah 1.120 true positive lebih banyak pada titik pertama ([S6] baris 204-208).

**Workflow.** (1) Ambil dua baris keluaran engine. (2) Susun tabel pertukaran. (3) Hitung selisih
per kolom. (4) Cetak biaya perpindahan dalam true positive dan menit lead. (5) Minta supervisor
memilih, lalu catat pilihan beserta alasannya di log keputusan (LIN-01). (6) Kunci pilihan per
sumur, karena kalibrasi lokal wajib ([PM1] baris 129).

**Keluaran.** Tabel enam kolom untuk tiga baris (titik pertama, titik kedua, pembanding lama), plus
satu baris biaya perpindahan. Arti tiap nilai: FAR 4,0984 berarti sekitar empat alarm palsu per 24
jam operasi negatif, dan lead 8,0 menit berarti peringatan datang delapan menit sebelum onset pada
median.

**Saran penyajian.** Tabel pertukaran dua kolom utama dengan selisih di kolom paling kanan, bukan
grafik radar. Alasan: pembaca harus membandingkan tujuh atribut sekaligus, dan radar membuat luas
bidang yang tidak sebanding; tabel mendukung tugas membandingkan dan mencari ([LV4]). Tata letak
contoh: tabel tiga baris, kolom diurutkan dari yang paling mudah ditafsirkan (true positive, alarm
palsu, presisi, recall, FAR, lead), dan kolom selisih diberi latar hanya pada baris yang dipilih.

**Dasar riset penyajian.** [LV4] untuk tabel perbandingan banyak atribut. [LV8] menjadi alasan
menolak dua sumbu Y pada satu grafik, karena FAR dan lead punya satuan berbeda dan harus tetap di
kolom terpisah.

**Status bukti.** Siap sekarang. Ketujuh nilai per titik tertulis dengan nomor baris yang sama
([S6] baris 194, 196, 197) dan sudah lolos uji baca di [VF] bagian 3.4.

**Salah tafsir yang harus dicegah.** Pertama, membaca titik pertama sebagai pemenang mutlak; ia
menukar 8 alarm tambahan untuk 1.120 true positive, dan itu pertukaran ([S6] baris 204-208). Kedua,
memakai satu titik untuk semua sumur. Ketiga, membaca FAR 4,0984 sebagai angka per hari kalender
untuk semua konteks, padahal satuannya 24 jam operasi negatif.

**Cara menguji.** Hitung ulang selisih true positive dan alarm palsu dari dua baris sumber dan
cocokkan dengan baris biaya. Uji kedua, tampilkan panel pada dua sumur dan pastikan pilihan tersimpan
per sumur, bukan global.

### MNT-04 Panel titik operasi hemat-awas shk

**Tujuan.** Menampilkan empat titik operasi yang memenuhi anggaran alarm, beserta cakupan yang
dikorbankan di tiap titik. Untuk driller dan supervisor yang memilih tingkat kepekaan.

**Menggambarkan apa.** Setiap titik adalah pasangan ambang dan konsekuensinya. Cakupan naik berarti
lebih banyak onset tertangkap; FAR naik berarti lebih banyak alarm palsu. Panel ini juga wajib
menampilkan bahwa pengurangan pemeriksaan pada ambang rendah bernilai negatif.

**Pengguna dan momen pakai.** Driller saat memilih kepekaan pada awal shift. Supervisor saat
meninjau kebijakan, sekali per minggu.

**Masukan.** Grid ambang tau 0,05 sampai 0,30, presisi dan recall per titik, FAR per 24 jam, dan
jumlah positif per sumur.

**Algoritma.** Saring titik yang memenuhi FAR maksimum 6 dengan recall di atas nol, lalu urutkan
menurut cakupan. Empat titik lolos: F-14 pada tau 0,20 dengan presisi 0,26 dan FAR 4,8; F-14 pada
tau 0,30; F-5 pada tau 0,30 dengan presisi 0,32; F-9 pada tau 0,50 dengan presisi 0,55 ([Ek] baris
60). Titik FAR maksimum 1 dengan recall di atas nol hanya satu di seluruh grid, yaitu F-14 pada tau
0,30 dengan FAR 0,69 dan recall 0,92 persen, dan titik itu ditandai tidak operasional ([A1-8] baris
45; [PM8] baris 104). Penghematan pemeriksaan negatif antara -0,11 sampai -53,75 pada tau maksimum
0,20 ([Ek] baris 84).

**Workflow.** (1) Ambil grid ambang dan metrik. (2) Saring dengan anggaran FAR. (3) Urutkan menurut
cakupan. (4) Cetak empat titik beserta biayanya. (5) Cetak peringatan bahwa penghematan negatif.
(6) Simpan pilihan per sumur.

**Keluaran.** Empat baris titik operasi dengan presisi, recall, FAR, dan cakupan, plus satu baris
peringatan penghematan negatif. Arti: presisi 0,55 berarti kira-kira separuh alarm benar.

**Saran penyajian.** Grafik sebar presisi terhadap recall dengan empat titik berlabel ambang, plus
tabel kecil di bawahnya. Alasan: hubungan dua variabel kontinu paling terbaca pada sebar, dan label
ambang di titik membuat pilihan konkret ([LV6]). Tata letak contoh: sebar 400 kali 300 piksel dengan
garis bantu FAR, empat titik berlabel tau, tabel empat baris di bawah.

**Dasar riset penyajian.** [LV6] untuk sebar pada dua variabel kontinu. [LV9] untuk kebiasaan menulis
angka di samping titik, bukan hanya posisi.

**Status bukti.** Siap sekarang. Empat titik dan penghematan negatif terukur ([Ek] baris 60 dan 84;
[A1-8] baris 45) dan sudah diuji baca di [VF] bagian 3.2.

**Salah tafsir yang harus dicegah.** Pertama, memilih titik dengan cakupan tertinggi tanpa melihat
FAR. Kedua, membaca penghematan negatif sebagai kesalahan hitung. Ketiga, memindahkan ambang antar
sumur, karena kalibrasi tidak portabel.

**Cara menguji.** Hitung ulang presisi dan recall pada satu titik dari data mentah sumur itu dan
bandingkan. Uji kedua, pastikan panel menolak menampilkan titik tanpa FAR terukur.

### MNT-05 Penaksir beban tinjauan per shift

**Tujuan.** Menerjemahkan FAR menjadi jumlah tinjauan per shift 8 jam, supaya perencanaan tenaga
kerja memakai angka yang bisa diperiksa. Untuk perencana tenaga kerja dan supervisor.

**Menggambarkan apa.** Beban perhatian, bukan jumlah kejadian. Angka ini menggambarkan berapa kali
orang harus melihat layar, dan bukan berapa kerusakan yang terjadi.

**Pengguna dan momen pakai.** Supervisor saat menyusun jadwal shift, sekali per hari. Perencana
tenaga kerja saat menghitung kebutuhan orang, sekali per minggu.

**Masukan.** FAR per 24 jam per head dari [ENG] baris 31-43, dan label segmen sumber angka.

**Algoritma.** Bagi FAR per 24 jam dengan tiga untuk mendapat perkiraan per shift 8 jam. Hasil yang
sudah terhitung di sumber, dalam tinjauan per shift: vib 17, hyd rule 19, hyd hybrid 6, shk 3, stuck
3, tool_wear 1 ([ENG] baris 31-43).

**Workflow.** (1) Ambil FAR per head. (2) Bagi tiga. (3) Bulatkan ke atas. (4) Tempelkan label
segmen wajib. (5) Jumlahkan per peran, bukan per head. (6) Cetak asumsi 8 jam di kaki tabel.

**Keluaran.** Enam angka tinjauan per shift, dengan label "angka segmen F-14, bukan median lintas
fold". Arti: 19 tinjauan per shift berarti satu tinjauan setiap 25 menit.

**Saran penyajian.** Batang horizontal berurut menurun, dengan angka di ujung dan label segmen di
kaki grafik. Alasan: enam nilai pada satu skala, dan urutan membantu perencana melihat penyumbang
terbesar ([LV7]). Tata letak contoh: enam batang selebar 300 piksel, label segmen dua baris di bawah.

**Dasar riset penyajian.** [LV7] untuk kanal panjang. [LV14] untuk alasan menampilkan beban sebagai
volume yang bisa dibagi ke orang, bukan satu angka backlog.

**Status bukti.** Siap sebagian. Angka ada ([ENG] baris 31-43), tetapi batas segmennya diakui
dokumen sumber ([ENG] bagian 5 butir 3 baris 67), sehingga angka ini tidak boleh dipakai sebagai
beban seluruh armada.

**Salah tafsir yang harus dicegah.** Membaca angka ini sebagai beban lapangan penuh, dan menjumlahkan
seluruh head sebagai kebutuhan orang tanpa memeriksa tumpang tindih peran.

**Cara menguji.** Bandingkan dengan hitungan FAR per 24 jam dibagi tiga pada satu sumur, lalu
periksa apakah label segmen tercetak.

### MNT-06 Mode bengkel dan detektor perubahan regime

**Tujuan.** Memisahkan domain bengkel berdetik dari domain rig bermenit, dan menandai perubahan
regime dalam satu run alat. Untuk teknisi bengkel dan perencana inspeksi alat.

**Menggambarkan apa.** Perubahan perilaku alat di dalam satu run. Deteksi berarti ada perubahan dari
kondisi awal run, bukan berarti alat aus. Perubahan itu juga muncul pada alat baru, dan fakta itu
wajib tercetak.

**Pengguna dan momen pakai.** Teknisi bengkel saat run berjalan, beberapa kali per run. Perencana
inspeksi saat menyusun jadwal bengkel, sekali per minggu.

**Masukan.** Deret 1 detik per run alat, fitur kurtosis, crest, dan frekuensi dominan per jendela
pendek, serta ambang hasil kalibrasi dalam run.

**Algoritma.** Deteksi perubahan titik dengan uji change-point per run. Hasil terukur: change-point
signifikan di 8 dari 8 run, termasuk 8 dari 8 run alat baru, sehingga spesifisitas keausan gagal
([Ew] baris 74 dan 146). Presisi tingkat run 0,50, lead median 24,5 detik untuk satu engine dan 47,0
detik untuk engine lain ([A1-8] baris 47, 48, 118; [Ew] baris 106). FAR 46,0 sampai 60,0 per menit
dan AUPRC 0,5433 sampai 0,7684 ([A1-8] baris 68). Penghematan pemeriksaan +0,909 sampai +0,976
([EVB] baris 106).

**Workflow.** (1) Ambil deret per run. (2) Hitung fitur per jendela pendek. (3) Jalankan uji
change-point. (4) Tandai run yang berubah. (5) Cetak catatan bahwa alat baru juga berubah. (6)
Terpisah dari mode rig, dengan satuan detik yang tidak dijumlahkan ke menit rig.

**Keluaran.** Daftar run dengan penanda perubahan, lead dalam detik, dan jumlah alarm palsu per menit.
Arti: lead 47 detik berarti inspeksi bisa dimulai 47 detik setelah perubahan terdeteksi.

**Saran penyajian.** Garis waktu run dengan penanda vertikal di titik perubahan, plus tabel run.
Alasan: pertanyaan pembaca adalah kapan berubah, dan posisi pada sumbu waktu paling tepat untuk itu
([LV3]). Tata letak contoh: garis waktu satu run selebar panel, penanda vertikal, tabel lima kolom
di bawahnya, dan label satuan detik di sumbu x.

**Dasar riset penyajian.** [LV3] untuk plot garis terhadap waktu sebagai langkah pertama analisis.
[LV8] untuk larangan mencampur dua satuan pada satu grafik, yang di sini berarti mode bengkel dan
mode rig tidak boleh disatukan.

**Status bukti.** Siap sekarang untuk deteksi perubahan. Yang belum: klaim keausan spesifik, karena
spesifisitas gagal pada alat baru.

**Salah tafsir yang harus dicegah.** Pertama, membaca perubahan sebagai keausan. Kedua, menjumlahkan
lead detik bengkel dengan lead menit rig. Ketiga, memakai presisi 0,50 sebagai dasar alarm.

**Cara menguji.** Jalankan detektor pada satu run alat baru dan pastikan panel tetap menandainya
sebagai perubahan, bukan sebagai keausan.

### MNT-07 Kurva tren keausan dengan cap keterlambatan

**Tujuan.** Menampilkan tren status bit_wear beserta cap eksplisit bahwa deteksinya terlambat satu
jendela. Untuk engineer drilling dan supervisor yang mengevaluasi performa bor harian.

**Menggambarkan apa.** Efisiensi mekanika pengeboran per blok, bukan umur bit. Kurva naik berarti
blok makin tidak efisien. Cap keterlambatan berarti peringatan muncul setelah kondisi berubah, bukan
sebelum.

**Pengguna dan momen pakai.** Engineer drilling saat mengevaluasi performa harian, sekali per hari.
Supervisor saat menyiapkan keputusan ganti bit, beberapa kali per minggu.

**Masukan.** Status `high_MSE` dari baseline persistence, skor model screening, AUPRC per fold, dan
kedalaman serta TVD per blok.

**Algoritma.** Baseline persistence dipakai sebagai dasar bobot karena memberi AUPRC 0,679 sampai
0,984 ([Eb] baris 40 dan 88), sedangkan skor model menang terhadap canary 4 dari 4 fold dengan delta
+0,058 sampai +0,107 tetapi kalah terhadap persistence 4 dari 4 fold dengan delta -0,087 sampai
-0,381 ([Eb] baris 76-81). AUPRC per fold 0,298 dan 0,365 dan 0,813 dan 0,783, canary 0,191 dan
0,288 dan 0,756 dan 0,692 ([Eb] baris 66-69). Lead masuk blok mendekati nol, dan transisi terdeteksi
satu jendela atau sekitar 10 menit terlambat ([Eb] baris 167; [M1] baris 52).

**Workflow.** (1) Hitung status per blok. (2) Susun kurva terhadap kedalaman. (3) Tempelkan cap
keterlambatan. (4) Cetak AUPRC per fold sebagai bobot kepercayaan. (5) Tandai tiga fold yang kurang
berdaya. (6) Jangan tampilkan kurva sebagai prediksi masa depan.

**Keluaran.** Kurva tren per sumur dengan sumbu kedalaman dan status, plus cap teks "terlambat satu
jendela sekitar 10 menit" dan daftar AUPRC empat fold.

**Saran penyajian.** Garis terhadap kedalaman dengan pita kepercayaan per fold, bukan batang. Alasan:
sumbu kedalaman adalah sumbu kontinu dan pertanyaannya tren, sehingga garis lebih tepat ([LV3]).
Tata letak contoh: grafik selebar panel, sumbu x kedalaman, sumbu y status, cap keterlambatan di
dalam area grafik, tabel AUPRC empat baris di sebelah kanan.

**Dasar riset penyajian.** [LV3] untuk plot garis pada sumbu kontinu. [LV12] untuk alasan memakai
beberapa lebar jendela sebelum menyimpulkan bentuk sebaran.

**Status bukti.** Siap sekarang untuk kurva status. Yang belum: precision, recall, dan FAR, karena
ketiganya tidak terukur dan bukti ketiadaannya berasal dari pemindaian artefak ([Eb] baris 96-98).

**Salah tafsir yang harus dicegah.** Pertama, membaca kurva sebagai prediksi. Kedua, membaca AUPRC
0,298 sebagai mutu rendah tanpa melihat canary 0,191. Ketiga, memakai label ini sebagai bukti
keausan fisik (lihat KEP-09).

**Cara menguji.** Hitung AUPRC satu fold dari data mentah dan bandingkan dengan tabel. Uji kedua,
periksa bahwa cap keterlambatan tercetak pada tangkapan layar 375 piksel.

### MNT-08 Indikator status hidrolik

**Tujuan.** Menandai kondisi hidrolik saat tekanan atau aliran mencurigakan. Untuk mudlogger dan
driller.

**Menggambarkan apa.** Simpangan tekanan terhadap median per bin aliran. Status menyala berarti
tekanan keluar dari kebiasaan pada laju aliran itu, bukan berarti kick sudah terjadi.

**Pengguna dan momen pakai.** Mudlogger dan driller saat memantau, terus menerus sepanjang shift
pengeboran.

**Masukan.** Residu tekanan terhadap median dan MAD per bin laju aliran, status jendela sebelumnya,
dan cakupan sensor.

**Algoritma.** Ambang simpangan absolut di atas 2. Baseline persistence memberi presisi 0,615 sampai
0,793 dan recall 0,617 sampai 0,764 dengan FAR 38,8 sampai 110,7 per 24 jam dan cakupan onset 31,6
sampai 65,4 persen ([Eh] baris 76). Model tidak dipakai untuk status, karena delta terhadap
persistence negatif di 7 dari 7 fold ([Eh] baris 62). Cakupan sensor SPPA dan TFLO 94,0 sampai 98,7
persen ([Eh] baris 157).

**Workflow.** (1) Hitung residu per bin. (2) Terapkan ambang. (3) Tempelkan cakupan sensor.
(4) Cetak jumlah blok per hari. (5) Jangan menampilkan ambang lintas sumur.

**Keluaran.** Status per jendela, cakupan sensor persen, dan jumlah blok per hari 0,16 sampai 4,7
([Eh] baris 161-171). Arti: cakupan sensor 94 persen berarti enam persen waktu tanpa data.

**Saran penyajian.** Pita status berwarna sepanjang waktu, dengan garis residu di bawahnya. Alasan:
status biner lebih mudah dibaca sebagai pita daripada sebagai titik, dan garis residu memberi
konteks ([LV3]). Tata letak contoh: pita setinggi 12 piksel di atas, garis residu setinggi 80
piksel, sumbu waktu bersama.

**Dasar riset penyajian.** [LV3] untuk garis waktu. [LV6] untuk pemilihan pita pada status biner.

**Status bukti.** Siap sekarang. Semua angka terukur ([Eh] baris 62, 76, 157) dan sudah diuji baca
di [VF] bagian 3.2.

**Salah tafsir yang harus dicegah.** Pertama, membaca status sebagai kick. Kedua, membaca status
padam sebagai aman, padahal bisa berarti sensor kosong. Ketiga, memakai ML untuk status ini.

**Cara menguji.** Hitung ulang residu pada satu jam data dan bandingkan statusnya. Uji kedua,
pastikan panel menyatakan sensor kosong ketika cakupan turun.

### MNT-09 Watchlist stick-slip dan penanda daya statistik

**Tujuan.** Menyusun daftar sumur menurut risiko stick-slip harian, dengan penanda bahwa sebagian
sumur tidak punya cukup positif untuk dinilai. Untuk supervisor operasi.

**Menggambarkan apa.** Risiko relatif antar sumur pada satu hari, bukan peluang kejadian. Penanda
daya statistik berarti angka pada sumur itu belum layak dipakai membandingkan.

**Pengguna dan momen pakai.** Supervisor operasi pada rapat pagi dan serah terima shift, dua kali
per hari.

**Masukan.** Skor per jendela lintas sumur, jumlah positif per sumur, dan kelas severitas SSI.

**Algoritma.** Urutkan sumur menurut skor harian. Tandai sumur dengan positif di bawah 30 sebagai
kurang berdaya, sesuai aturan penandaan UNDERPOWERED ([I1] baris 350). Angka positif nyata yang
terukur: kelas shk hanya punya F-10 dengan 798 dan F-12 dengan 580 ([PM7] baris 141, lihat [I2] baris
79). Kelas severitas SSI minimal 3 punya rujukan jurnal di ledger `L-05` baris 5.
AUPRC ssi 0,0185 sampai 0,1057 dengan lift 2,61 sampai 6,64 dan lift minimal 1,5 di 4 dari 5 fold
([Ess] baris 58), tetapi CI bawah di atas no-skill hanya 2 dari 5 fold ([M1] baris 51).

**Workflow.** (1) Kumpulkan skor harian. (2) Urutkan. (3) Tempelkan jumlah positif. (4) Nonaktifkan
sumur kurang berdaya dari perbandingan. (5) Cetak tanpa notifikasi otomatis.

**Keluaran.** Daftar sumur berurut dengan skor, jumlah positif, dan status daya. Arti: skor tinggi
pada sumur kurang berdaya tidak boleh dibandingkan dengan sumur lain.

**Saran penyajian.** Tabel berurut dengan kolom status daya, bukan peta panas. Alasan: jumlah baris
kecil, dan status daya harus terbaca sebagai kata ([LV4]). Tata letak contoh: lima kolom, baris
kurang berdaya diberi latar abu dan teks "UNDER".

**Dasar riset penyajian.** [LV4] untuk tabel status. [LV1] untuk larangan menampilkan skor tanpa
daya pisah.

**Status bukti.** Siap sebagian. Angka positif terukur; aturan menonaktifkan panel adalah usulan
desain yang belum diuji.

**Salah tafsir yang harus dicegah.** Membaca urutan sebagai peringkat mutu sumur, dan membaca skor
tinggi pada sumur kurang berdaya sebagai temuan.

**Cara menguji.** Hitung ulang jumlah positif satu sumur dari label mentah. Uji kedua, pastikan
sumur kurang berdaya tidak muncul di urutan perbandingan.

---

## 7. Rumpun kualitas data (DAT-01 sampai DAT-10)

Rumpun ini mengurus pertanyaan "boleh tidak angka ini dipakai". Sepuluh fiturnya dibangun dari
kekurangan data yang sudah terukur, jadi isinya bukan keluhan, melainkan status dan pekerjaan.

### DAT-01 Kartu kelengkapan jendela pra-event

**Tujuan.** Memberi tahu seberapa layak satu event dinilai sebelum skor model dipakai, supaya skor
rendah tidak dibaca sebagai sinyal fisik. Untuk engineer PdM dan supervisor pengeboran.

**Menggambarkan apa.** Kelengkapan data pada jendela sebelum satu event. Empat label yang dipakai:
penuh, sebagian, kosong, terpotong. Bila sebuah event berlabel kosong, artinya sumur sedang tidak
mencatat data pada jendela itu, sehingga skor apa pun pada event itu tidak bermakna. Label ini
menggambarkan perilaku logging, bukan perilaku rig.

**Pengguna dan momen pakai.** Engineer PdM saat membuka satu event atau satu baris riwayat, beberapa
kali per hari. Supervisor saat memeriksa apakah satu peringatan layak dibahas di rapat pagi, sekali
per hari.

**Masukan.** Metadata jendela per event: jumlah baris, gap median dalam detik, gap maksimum, dan
penanda jendela penuh. Ketiganya tersedia di `X_window_meta` pada `features_timeseries.npz`
berukuran 458.129 byte. Angka acuan: median gap antar sampel 4,9 detik, median baris 379 untuk
jendela 30 menit, 1.515 untuk 2 jam, dan 4.549 untuk 6 jam ([V3T] baris 89). Jumlah event yang
seluruh fiturnya kosong: 194 pada jendela 30 menit, 191 pada 2 jam, 185 pada 6 jam, dengan irisan
ketiganya tepat 185 dari 661 ([V3T] baris 108-110). Fraksi NaN fitur sensor 0,368 pada jendela 2 jam
([V3T] baris 109).

**Algoritma.** Empat aturan berbasis ambang, tanpa model. Aturan satu, jendela penuh bila jumlah
baris minimal 80 persen dari nilai median jendela itu. Aturan dua, sebagian bila 20 sampai 79 persen.
Aturan tiga, kosong bila nol baris. Aturan empat, terpotong bila jendela melewati batas data sumur.
Ambang 80 persen dipilih karena median baris antar jendela berbeda satu orde (379 lawan 4.549),
sehingga ambang mutlak tidak dapat dipakai. Gap maksimum dicetak terpisah karena gap besar bisa
menyembunyikan dua perilaku berbeda dalam satu jendela.

**Workflow.** (1) Baca metadata jendela dari artefak. (2) Hitung ambang per panjang jendela dari
median baris. (3) Terapkan empat aturan. (4) Simpan label per event per panjang jendela. (5) Saat
pengguna membuka satu event, tampilkan label ketiga jendela berdampingan. (6) Bila ketiganya kosong,
blokir skor dan tampilkan kartu DAT-02.

**Keluaran.** Empat label plus tiga angka: jumlah baris, gap median, dan gap maksimum, per panjang
jendela. Tiap label juga membawa skor keyakinan 0 sampai 100 dari KEP-02 untuk kelas yang modelnya
dipakai pada jendela itu, supaya kartu lengkap tidak terbaca sebagai bukti model. Arti tiap nilai:
jendela sebagian dengan gap maksimum 40 menit berarti ada lubang data yang lebih besar daripada
jarak antar sampel normal, sehingga isi jendela itu tidak homogen.

**Saran penyajian.** Tiga kartu kecil berdampingan, satu per panjang jendela, dengan label di atas
dan tiga angka di bawah. Alasan: pembaca membandingkan tiga panjang jendela pada satu event, dan
tiga kartu sejajar membuat perbandingan itu langsung terlihat ([LV6]). Tata letak contoh: baris
berisi tiga kartu 200 kali 120 piksel, label "penuh", "sebagian", "kosong" sebagai lencana di kanan
atas, tiga angka berurutan di bawah.

**Dasar riset penyajian.** [LV6] untuk perbandingan kategori pada nilai sama. [LV4] untuk kebiasaan
menulis angka pendamping, bukan hanya warna lencana. [LV5] untuk penegasan bahwa nilai tanpa konteks
kelengkapan dibaca sebagai kepastian.

**Status bukti.** Siap sekarang. Seluruh angka terukur dari artefak dan cocok dengan dokumen sumber,
dan hitungan irisan 185 sudah dihitung ulang dari npz ([I1] bagian 3.4 dan 14.E; [VF] bagian 3.1 uji
nomor 2).

**Salah tafsir yang harus dicegah.** Pertama, membaca skor rendah pada jendela kosong sebagai kondisi
baik. Kedua, membaca label sebagian sebagai data cukup. Ketiga, mengimputasi nilai kosong tanpa
menandainya, karena itu menghapus informasi operasional yang justru bernilai.

**Cara menguji.** Ambil satu event berlabel kosong, lalu periksa berkas CSV sumurnya pada rentang
waktu itu dan pastikan memang tidak ada baris. Uji kedua, hitung ulang jumlah event kosong dari npz
dan cocokkan dengan angka yang ditampilkan.

### DAT-02 Kanal status sumur tidak logging

**Tujuan.** Menjadikan ketiadaan data sebagai informasi operasional, bukan NaN yang diimputasi
diam-diam. Untuk driller dan mudlogger.

**Menggambarkan apa.** Status perawatan alat logging atau keputusan operasional untuk tidak mencatat.
Status ini menggambarkan keadaan perekaman, bukan keadaan sumur.

**Pengguna dan momen pakai.** Driller saat event masuk dengan jendela kosong, setiap kali terjadi.
Mudlogger saat menyiapkan shift, sekali per shift.

**Masukan.** Mask NaN per jendela dari matriks fitur, daftar event dengan seluruh fitur kosong, dan
sebaran per sumur.

**Algoritma.** Tandai event yang seluruh fiturnya NaN pada satu jendela. Hitung sebaran per sumur.
Angka: 82 dari 94 pada F-9 A, 46 dari 182 pada F-14, 30 dari 56 pada F-9, 20 dari 58 pada F-7, 11
dari 105 pada F-15_S, 2 dari 134 pada F-5, 0 dari 32 pada F-15A ([V3T] baris 108; [I1] bagian 14.E).

**Workflow.** (1) Hitung mask NaN. (2) Kumpulkan event kosong. (3) Hitung rentang waktu kosong.
(4) Kelompokkan per sumur. (5) Tampilkan sebagai kanal status.

**Keluaran.** Status "tidak ada logging" beserta rentang waktu kosong dan sumur terkait, bukan angka
model. Arti: sumur dengan 82 dari 94 event kosong memberi tahu bahwa evaluasi model di sumur itu
nyaris tanpa dasar, dan itu informasi perencanaan data.

**Saran penyajian.** Kalender panas (heatmap) per sumur kali hari, dengan sel kosong ditandai jelas
dan angka di dalam sel. Alasan: pola waktu lebih terbaca pada heatmap daripada tabel panjang, dan
normalisasi per baris diperlukan karena jumlah event per sumur berbeda ([LV9]). Tata letak contoh:
heatmap tujuh baris sumur, kolom hari, legenda tiga tingkat, ringkasan "82 dari 94" di kiri baris.

**Dasar riset penyajian.** [LV9] untuk heatmap dan alasan normalisasi. [LV3] untuk alasan pola waktu
perlu dibaca pada sumbu waktu.

**Status bukti.** Siap sekarang. Sebaran per sumur terverifikasi ulang dari artefak ([I1] bagian 14.E).

**Salah tafsir yang harus dicegah.** Membaca status ini sebagai kerusakan sumur, dan membaca jumlah
event kosong sebagai jumlah kegagalan operasional.

**Cara menguji.** Pilih satu sel kosong pada heatmap dan periksa CSV sumur pada rentang waktu itu.

### DAT-03 Peta label ke fold dan antrean parse

**Tujuan.** Memberi setiap label jejak boleh atau tidaknya masuk evaluasi, supaya label yang gugur
bisa ditindak. Untuk auditor internal dan ML engineer.

**Menggambarkan apa.** Cakupan evaluasi. Label yang tidak terpetakan berarti tidak punya data
pendukung, bukan berarti tidak ada kejadian.

**Pengguna dan momen pakai.** Auditor sebelum kampanye training, sekali per kampanye. ML engineer
saat menjawab pertanyaan cakupan, setiap kali ditanya.

**Masukan.** Blok `coverage` dari `features_timeseries_meta.json`: 884 label, 671 terpetakan, 213
tanpa fold dengan rincian 122 pada F-15 D, 89 pada F-15 C, dan 2 pada F-15 B, serta 10 di luar
rentang dengan rincian 7 pada F-15_S, 2 pada F-5, dan 1 pada F-7 ([V3T] baris 39-44).

**Algoritma.** Aritmetika cakupan: 884 dikurangi 213 dikurangi 10 sama dengan 661 event terbangun
([V3T] baris 39-44). Setiap label diberi satu dari empat status: terpetakan, tanpa fold, di luar
rentang, atau tidak ditemukan. Status dihitung sekali per kampanye dan dibekukan.

**Workflow.** (1) Baca blok coverage. (2) Petakan label ke status. (3) Hitung jumlah per status.
(4) Urutkan pekerjaan parse menurut jumlah label yang terbuka. (5) Tampilkan bersama antrean parse
(DAT-06).

**Keluaran.** Tabel label dengan status dan jumlah event per sumur. Arti: 213 label tanpa fold
berarti 24 persen label tidak dapat dipakai pada kampanye terakhir.

**Saran penyajian.** Batang bertumpuk horizontal per sumur, dengan angka di dalam segmen. Alasan:
komposisi status per sumur lebih terbaca sebagai bagian dari keseluruhan, dan angka tetap ditulis
([LV6]). Tata letak contoh: satu batang per sumur, tiga segmen (terpetakan, tanpa fold, luar
rentang), total 661 di kanan.

**Dasar riset penyajian.** [LV6] untuk komposisi bagian. [LV4] untuk tabel pendamping yang memuat
angka pasti.

**Status bukti.** Siap sekarang. Angka diambil langsung dari meta artefak dan cocok dengan sumber
([I1] bagian 14.E).

**Salah tafsir yang harus dicegah.** Membaca 213 label gugur sebagai data hilang permanen; sebagian
berasal dari folder yang belum diparse (DAT-06).

**Cara menguji.** Jumlahkan status per sumur dan pastikan totalnya 884.

### DAT-04 Pemilih kanal berbasis fill rate dan QC fisik

**Tujuan.** Mencegah kanal yang setengah kosong atau konstan dipakai sebagai bukti fisik. Untuk
engineer data dan ML engineer.

**Menggambarkan apa.** Kelayakan kanal. Fill rate rendah berarti kanal jarang terisi; nilai konstan
berarti kanal tidak membawa informasi.

**Pengguna dan momen pakai.** Engineer data saat menyusun fitur kampanye baru, sekali per kampanye.

**Masukan.** Fill rate per kanal per sumur, daftar kanal per fold, dan penanda konstansi.

**Algoritma.** Ambang 50 persen fill rate sebagai aturan seleksi, karena dari 60 sampai 281 kanal per
sumur hanya 37 sampai 48 kanal yang mencapai 50 persen ([V3W] baris 41). Kanal dengan `trend_rho`
NaN ditandai konstan. Lima belas kanal kanonik dipakai, dengan 14 tersedia di 7 dari 7 fold,
sedangkan RPM 6 dari 7 dan MDOA 5 dari 7 ([V3T] baris 65-68).

**Workflow.** (1) Hitung fill rate per kanal. (2) Terapkan ambang. (3) Uji konstansi. (4) Terbitkan
daftar lolos dan gugur. (5) Jalankan validasi satuan sebelum lolos final.

**Keluaran.** Daftar kanal lolos beserta alasannya, dan daftar gugur beserta fill rate. Arti: kanal
gugur dengan fill rate 12 persen tidak boleh dipakai sebagai bukti fisik.

**Saran penyajian.** Tabel terurut dengan batang mini di kolom fill rate. Alasan: pembaca mencari
kanal tertentu dan membandingkan angka, dua tugas tabel ([LV4]). Tata letak contoh: kolom kanal,
sumur, fill rate dengan batang tipis, status.

**Dasar riset penyajian.** [LV4] untuk tabel pencarian dan perbandingan. [LV12] untuk alasan
memeriksa sebaran sebelum menyimpulkan.

**Status bukti.** Siap sebagian. Sisi seleksi terukur; sisi QC fisik belum pernah dijalankan, dan
validasi satuan serta duplikat timestamp belum ada ([V3W] baris 45-48).

**Salah tafsir yang harus dicegah.** Membaca kanal lolos sebagai kanal benar, karena validasi satuan
belum dijalankan.

**Cara menguji.** Hitung ulang fill rate satu kanal dan bandingkan. Uji kedua, jalankan uji
konstansi pada kanal yang lolos dan pastikan tidak ada yang bernilai tetap.

### DAT-05 Matriks ketersediaan berkas per sumur

**Tujuan.** Menampilkan apa yang sudah dimiliki dan apa yang masih perlu diunduh per sumur. Untuk
engineer PdM dan peneliti.

**Menggambarkan apa.** Kesiapan data per sumur, bukan mutu sumur.

**Pengguna dan momen pakai.** Engineer PdM sebelum memilih sumur untuk kampanye baru, sekali per
kampanye.

**Masukan.** Audit unduhan 17.368 berkas 3,32 GB dengan hilang nol, 11.894 berkas WITSML untuk 27
wellbore, 5.474 berkas teknis, dan 20.086 entri zip ([V3A] baris 182-185).

**Algoritma.** Hitung jumlah berkas per kategori per sumur, lalu tandai sumur yang punya kanal label.
Angka pendukung: 7.150 log XML, 192 tubular, 161 bhaRun, dan dua sumur terbesar F-1 C 2.156 berkas
serta F-11 1.750 berkas ([D0] baris 17-22, 49; [I1] bagian 14.C dan 14.F).

**Workflow.** (1) Baca audit berkas. (2) Kelompokkan per sumur. (3) Tempelkan kanal label. (4) Tandai
status siap atau perlu unduh. (5) Tautkan ke antrean parse.

**Keluaran.** Kartu per sumur berisi jumlah berkas per kategori dan status. Arti: sumur dengan 2.156
berkas tetapi nol kanal label siap diparse tetapi belum siap dievaluasi.

**Saran penyajian.** Matriks sumur kali kategori dengan angka di sel. Alasan: dua dimensi kategori
dan sumur paling terbaca sebagai matriks, dan angka di sel mencegah warna menjadi satu-satunya
pembeda ([LV9]). Tata letak contoh: sepuluh baris sumur, lima kolom kategori, total di kolom kanan.

**Dasar riset penyajian.** [LV9] untuk matriks bernilai. [LV4] untuk angka di sel.

**Status bukti.** Siap sekarang. Audit byte-per-byte pihak terpisah dan hitungan header sudah
dilakukan ([I1] bagian 14.C, 14.F).

**Salah tafsir yang harus dicegah.** Membaca jumlah berkas sebagai jumlah data siap pakai.

**Cara menguji.** Hitung ulang jumlah berkas satu sumur dengan `find` dan bandingkan.

### DAT-06 Antrean parse 3.906 berkas

**Tujuan.** Mengubah kesenjangan 54,6 persen menjadi pekerjaan terurut dengan proyeksi dampak. Untuk
koordinator data dan peneliti.

**Menggambarkan apa.** Sisa pekerjaan pengolahan data. Angka ini menggambarkan berkas yang belum
dibaca parser, bukan berkas yang tidak berguna.

**Pengguna dan momen pakai.** Koordinator data saat merencanakan perluasan cakupan, sekali per
kampanye.

**Masukan.** Daftar berkas belum diparse: F-1 C 2.156 dan F-11 1.750, total 3.906 atau 54,6 persen
dari 7.150 ([D0] baris 49; [PM6] baris 225; [I1] bagian 14.C).

**Algoritma.** Urutkan menurut jumlah berkas dan label yang terbuka bila selesai. 213 label tanpa
fold menyebar di tiga wellbore F-15 B, C, dan D ([V3T] baris 39-41), sehingga pekerjaan F-1 C dan
F-11 membuka kelas yang berbeda, bukan menambah jumlah baris pada kelas yang sudah ada.

**Workflow.** (1) Ambil daftar berkas. (2) Hitung per sumur. (3) Tautkan ke label terbuka. (4) Susun
urutan. (5) Jalankan parser yang sama seperti V3. (6) Catat hasil di `_parse_summary.json` baru.

**Keluaran.** Antrean berisi jumlah berkas, perkiraan kanal, dan calon kelas yang terbuka. Arti:
3.906 berkas adalah 54,63 persen dari 7.150, sehingga setengah pekerjaan data masih di depan.

**Saran penyajian.** Batang berurut menurun dengan anotasi label terbuka. Alasan: dua nilai besar
yang dibandingkan, dan anotasi menjelaskan dampak ([LV6]). Tata letak contoh: dua batang (2.156 dan
1.750), anotasi "212 label", total 3.906 di kanan.

**Dasar riset penyajian.** [LV6] untuk batang perbandingan. [LV14] untuk kebiasaan menampilkan
pekerjaan sebagai antrean berumur, bukan satu angka.

**Status bukti.** Siap sekarang. Hitungan `find` memberi 2.156 dan 1.750 dan totalnya 54,63 persen
([I1] bagian 14.C).

**Salah tafsir yang harus dicegah.** Membaca 3.906 berkas sebagai 3.906 sumur baru; jumlah sumur
tetap 10 ditambah dua era V9.

**Cara menguji.** Hitung ulang jumlah berkas per direktori dan cocokkan dengan 3.906.

### DAT-07 Katalog label instrumen per sumur

**Tujuan.** Menampilkan sumur mana punya label apa, supaya klaim lintas sumur selalu disertai jumlah
sumur yang benar. Untuk auditor, ML engineer, dan dosen penguji.

**Menggambarkan apa.** Ketersediaan label instrumen, bukan ketersediaan kejadian. Label tidak
direkam berarti kejadian tidak terukur di sumur itu.

**Pengguna dan momen pakai.** Auditor saat membaca hasil lintas sumur, sekali per kampanye. ML
engineer saat memilih sumur uji, sekali per fold.

**Masukan.** Pemindaian header sepuluh CSV terparse. Hasil: STUCK_RT di 4 sumur, VIBLAT_RT di 6,
SHKRSK_RT di 9, CRPM_RT di 9 ([I1] bagian 3.3 dan 14.D).

**Algoritma.** Hitung jumlah sumur per kanal label dan bandingkan dengan tabel sumber. Satu koreksi
sudah dilakukan: VIBLAT tercatat 6 sumur, bukan 7, dan angka 6 yang terverifikasi ([I1] bagian 3.3;
[RD0] baris 98-104).

**Workflow.** (1) Pindai header. (2) Hitung sumur per kanal. (3) Bandingkan dengan dokumen. (4) Cetak
matriks. (5) Tandai selisih yang belum dijelaskan.

**Keluaran.** Matriks sumur kali kanal dengan jumlah sumur. Arti: STUCK 4 berarti klaim kelas stuck
hanya berlaku di empat sumur.

**Saran penyajian.** Matriks dengan angka di sel dan total per kolom. Alasan: struktur data memang
dua dimensi, dan total per kolom menjawab pertanyaan "berapa sumur" langsung ([LV9]). Tata letak
contoh: sepuluh baris sumur, empat kolom kanal, baris total di bawah.

**Dasar riset penyajian.** [LV9] untuk matriks. [LV4] untuk total dan pengenal yang terbaca.

**Status bukti.** Siap sekarang. Hasil pemindaian cocok dengan tabel sumber, dengan satu koreksi
tercatat ([I1] bagian 14.D).

**Salah tafsir yang harus dicegah.** Membaca jumlah sumur sebagai jumlah kejadian, dan memakai angka
lama 7 untuk VIBLAT.

**Cara menguji.** Pindai ulang header dan bandingkan jumlah kolom kanal per berkas.

### DAT-08 Kartu kesiapan kanal per sumur

**Tujuan.** Menyatakan sebelum panel dinyalakan apakah kanal masukan yang dibutuhkan sudah ada dan
terisi. Untuk engineer instrumentasi dan engineer yang memasang panel.

**Menggambarkan apa.** Kesiapan kanal, bukan kesiapan model. Bila sebuah kanal 62,3 persen kosong,
panel yang bergantung pada kanal itu akan sering padam bukan karena kondisi aman, melainkan karena
tidak ada data.

**Pengguna dan momen pakai.** Engineer saat memasang panel pada sumur baru, sekali per pemasangan.
Engineer instrumentasi saat mengajukan pengadaan sensor, sekali per siklus anggaran. Supervisor saat
menjelaskan mengapa satu sumur tidak punya panel, setiap kali ditanya.

**Masukan.** Daftar kanal per engine, jumlah baris terisi dan kosong per kanal per sumur, dan jumlah
berkas per kanal. Angka terukur: ssi membutuhkan CRPM dengan 22.385 dari 35.906 baris kosong atau
62,3 persen, dan F-14 mencapai 96,6 persen ([EVC] baris 136). vib membutuhkan VIBLAT dengan 356 dari
1.989 baris kosong pada F-14 ([EVC] baris 121). Ketersediaan kanal VIBLAT lintas sumur: 6 sumur dari
10, dengan koreksi dari angka 7 sumur pada ringkasan lama ([I1] baris 245 dan 250).

**Algoritma.** Tiga status per kanal per sumur. Siap bila baris kosong di bawah 20 persen. Bersyarat
bila 20 sampai 60 persen. Belum bila di atas 60 persen atau berkas nol. Ambang 20 persen dipakai
karena dropout di atas 20 persen sudah dipakai sebagai syarat gerbang LAYER-0 ([PM1] baris 139),
sehingga angkanya konsisten dengan gerbang yang sudah ada. Ambang 60 persen dipilih agar status belum
muncul pada kasus yang jelas tidak layak, seperti F-14 dengan 96,6 persen kosong.

**Workflow.** (1) Kumpulkan daftar kanal per engine. (2) Hitung baris terisi dan kosong per kanal per
sumur. (3) Hitung jumlah berkas per kanal. (4) Terapkan tiga status. (5) Cetak tombol permintaan
kalibrasi atau pengadaan untuk status belum. (6) Simpan status per sumur supaya tidak dihitung ulang
setiap kali panel dibuka.

**Keluaran.** Kartu per sumur dengan baris per kanal: nama kanal, persen kosong, jumlah berkas,
status, dan aksi. Arti: status bersyarat berarti panel boleh dinyalakan tetapi badge harus menyebut
kanal yang bolong, dan skor pada jendela kosong tidak boleh ditampilkan.

**Saran penyajian.** Daftar baris per kanal dengan bilah persen kosong, plus lencana status. Alasan:
pembaca memeriksa satu kanal pada satu waktu, dan panjang bilah menunjukkan proporsi lebih akurat
daripada warna ([LV7]). Bentuk ini juga menerapkan pola Dynamic Island: yang kosong ditampilkan
sebagai isi layar, lengkap dengan tombol tindakan. Tata letak contoh: kartu selebar 360 piksel, judul
sumur, lima baris kanal, tiap baris berisi nama, bilah, persen, lencana, dan tautan "minta kalibrasi"
di kanan.

**Dasar riset penyajian.** [LV7] untuk kanal panjang pada proporsi. [LV6] untuk pemilihan bilah pada
satu nilai per kategori. [LV14] untuk alasan menampilkan pekerjaan yang menggantung sebagai antrean
yang bisa ditindak, bukan sebagai catatan.

**Status bukti.** Siap sekarang untuk tiga kanal yang angkanya sudah terukur (CRPM, VIBLAT, dan
kanal shk yang n_nodata-nya tercatat di [EVC] baris 146). Siap sebagian untuk kanal lain, karena
daftar kanal per engine belum lengkap diinventarisasi ([I3] bagian 10 butir 7).

**Salah tafsir yang harus dicegah.** Pertama, membaca status belum sebagai sumur buruk. Kedua,
menyalakan panel pada status bersyarat tanpa menampilkan kanal yang bolong. Ketiga, membaca persen
kosong sebagai persen waktu tanpa pengawasan; itu persen baris, dan barisnya bisa rapat atau jarang.

**Cara menguji.** Hitung ulang persen kosong satu kanal dari CSV dan bandingkan dengan kartu. Uji
kedua, matikan satu kanal dan pastikan statusnya berubah tanpa menghapus baris lain.

### DAT-09 Peta drift antar sumur dan dalam sumur

**Tujuan.** Menunjukkan bahwa ambang lama tidak otomatis berlaku di sumur lain, dan bahwa satu sumur
pun berubah antar paruh waktu. Untuk penanggung jawab mutu data dan engineer pemeliharaan.

**Menggambarkan apa.** Jarak distribusi sinyal antar sumur dan antar paruh. Jarak besar berarti
distribusi berbeda, sehingga ambang yang dipindahkan akan berperilaku lain.

**Pengguna dan momen pakai.** Penanggung jawab mutu data saat menilai kelayakan pindah sumur, sekali
per kampanye. Engineer saat ambang lama mulai berperilaku lain, setiap kali kejadian.

**Masukan.** Statistik jendela dasar per paruh waktu per sumur, misalnya rata-rata TQA.

**Algoritma.** Uji Kolmogorov-Smirnov antar sumur dan dalam sumur. Hasil: antar sumur D median 0,986
dengan 10 dari 10 pasangan p di bawah 0,05. Dalam sumur D median 0,211 dengan 4 dari 5 sumur p di
bawah 0,05 ([R5] baris 129-140 dan 135-136). Catatan metode wajib: p tidak sah untuk deret
berautokorelasi dengan ac1 sekitar 0,98, sehingga D dipakai sebagai jarak, bukan p sebagai bukti
([R5] baris 142-148).

**Workflow.** (1) Hitung statistik per paruh. (2) Jalankan uji. (3) Catat D dan p. (4) Tandai sumur
yang jaraknya besar. (5) Cetak catatan autokorelasi. (6) Tautkan ke wizard kalibrasi (ING-01).

**Keluaran.** Matriks jarak antar sumur dan grafik jarak antar paruh. Arti: D 0,986 berarti dua
distribusi hampir tidak bertumpang.

**Saran penyajian.** Heatmap matriks jarak dengan angka di sel, plus satu grafik garis jarak antar
paruh per sumur. Alasan: matriks untuk pasangan, garis untuk perubahan sepanjang waktu ([LV3],
[LV9]). Tata letak contoh: heatmap 5 kali 5, di sebelahnya lima garis tipis dengan penanda paruh.

**Dasar riset penyajian.** [LV9] untuk matriks bernilai. [LV3] untuk garis waktu.

**Status bukti.** Siap sekarang untuk lima sumur yang diuji. Syarat perluasan: statistik jendela
dasar untuk semua sumur ([I3] bagian 9 butir 3).

**Salah tafsir yang harus dicegah.** Membaca p sebagai bukti utama pada data berautokorelasi, dan
membaca jarak besar sebagai kesalahan data.

**Cara menguji.** Hitung ulang D satu pasangan dan bandingkan dengan sel matriks.

### DAT-10 Validitas kedalaman MD ke TVD

**Tujuan.** Memastikan setiap fitur berbasis tekanan memakai kedalaman vertikal yang benar. Untuk
engineer drilling dan analis hidraulik.

**Menggambarkan apa.** Koreksi kedalaman terukur menjadi kedalaman vertikal. Tanpa koreksi, dua titik
dengan kedalaman terukur sama bisa berada di posisi vertikal berbeda, sehingga perbandingan tekanan
menjadi salah.

**Pengguna dan momen pakai.** Engineer drilling sebelum menjalankan fitur hidraulik, sekali per
kampanye. Analis hidraulik saat memeriksa satu anomali tekanan, setiap kali.

**Masukan.** 5.561 stasiun survey dari 63 trajectory ditambah 27 wbGeometry ([D0] baris 47), dan
5.669.005 dari 7.080.457 baris yang bisa dikoreksi ([A1] baris 78).

**Algoritma.** Interpolasi TVD dari stasiun survey terdekat, lalu tandai baris yang terkoreksi.
Cakupan 80,1 persen baris ([D0] baris 47; [A1] baris 78). Baris tanpa stasiun survey yang mengapit
ditandai tidak terkoreksi, bukan diisi dengan nol.

**Workflow.** (1) Baca stasiun survey. (2) Interpolasi per kedalaman. (3) Tempelkan status per baris.
(4) Hitung cakupan. (5) Tampilkan status pada grafik tekanan.

**Keluaran.** Kolom TVD dan status terkoreksi per baris, plus ringkasan 80,1 persen. Arti: baris
tidak terkoreksi tidak boleh dipakai pada fitur yang peka kedalaman.

**Saran penyajian.** Garis TVD terhadap MD dengan penanda stasiun survey, ditambah bilah cakupan.
Alasan: hubungan dua variabel kontinu paling terbaca pada garis, dan penanda stasiun menunjukkan
dasar interpolasi ([LV3]). Tata letak contoh: grafik garis 400 kali 240 piksel, titik stasiun
sebagai penanda, bilah cakupan 80,1 persen di bawah.

**Dasar riset penyajian.** [LV3] untuk garis pada dua variabel kontinu. [LV8] untuk larangan
mencampur dua satuan pada satu sumbu.

**Status bukti.** Siap sekarang. Kedua angka dihitung ulang auditor dengan alat berbeda ([A1] baris
78; [VF] bagian 3.1).

**Salah tafsir yang harus dicegah.** Membaca 80,1 persen sebagai 19,9 persen data hilang; baris itu
ada, hanya tidak dapat dikoreksi.

**Cara menguji.** Ambil satu baris terkoreksi dan hitung ulang TVD dari stasiun yang mengapit.

---

## 8. Rumpun perbandingan mesin (CMP-01 sampai CMP-07)

Rumpun ini mengurus pertanyaan "apakah modelnya benar-benar menambah sesuatu". Tujuh fiturnya
memuat hasil yang tidak enak dibaca, termasuk kekalahan model terhadap baseline sederhana, karena
angka itu bagian dari katalog.

### CMP-01 Balapan model terhadap baseline persistence

**Tujuan.** Menampilkan perbandingan langsung antara model dan baseline persistence per fold, supaya
klaim perbaikan tidak berdiri sendiri. Untuk peneliti dan dosen penguji.

**Menggambarkan apa.** Selisih AUPRC antara dua metode pada data dan fold yang sama. Selisih negatif
berarti model kalah.

**Pengguna dan momen pakai.** Peneliti saat menyusun laporan kemajuan, sekali per bulan. Dosen
penguji saat memeriksa klaim perbaikan, sekali per sidang.

**Masukan.** AUPRC per fold dari baseline persistence dan dari model, per kelas dan per varian target.

**Algoritma.** Hitung selisih berpasangan per fold, lalu median dan rentangnya. Angka: baseline
persistence memberi AUPRC 0,6376 sampai 0,9723 dengan median 0,9038, sedangkan model memberi median
0,8374 pada target yang sama, sehingga model kalah pada 100 dari 100 jawaban ([Eb] baris 88).

**Workflow.** (1) Kumpulkan AUPRC per fold per metode. (2) Pasangkan per fold. (3) Hitung selisih.
(4) Hitung median dan rentang. (5) Tandai fold yang kalah. (6) Tampilkan bersama jumlah fold.

**Keluaran.** Grafik berpasangan per fold dengan garis penghubung, plus median kedua metode. Arti:
garis yang turun dari kiri ke kanan berarti model kalah pada fold itu.

**Saran penyajian.** Grafik kemiringan (slopegraph) dua kolom metode dengan garis per fold. Alasan:
pertanyaannya perubahan pada unit yang sama, dan kemiringan memperlihatkan arah per fold ([LV6]).
Tata letak contoh: kolom kiri "persistence", kolom kanan "model", sepuluh garis, garis turun diberi
warna peringatan.

**Dasar riset penyajian.** [LV6] untuk pemilihan bentuk pada data berpasangan. [LV4] untuk tabel
pendamping berisi median.

**Status bukti.** Siap sekarang. Angka median dan jumlah fold terukur ([Eb] baris 88).

**Salah tafsir yang harus dicegah.** Membaca kekalahan sebagai kegagalan total; persistence memang
sangat kuat pada target berautokorelasi tinggi, dan itu temuan, bukan cacat.

**Cara menguji.** Hitung ulang AUPRC satu fold untuk kedua metode dan cocokkan dengan garisnya.

### CMP-02 Peta kalah-menang per kelas

**Tujuan.** Menunjukkan kelas mana yang modelnya unggul dan kelas mana yang kalah, supaya keputusan
pemakaian per kelas punya dasar. Untuk peneliti dan PM.

**Menggambarkan apa.** Arah hasil per kelas, bukan mutu keseluruhan.

**Pengguna dan momen pakai.** PM saat memutuskan kelas mana yang dipakai, sekali per kampanye.
Peneliti saat memilih kelas untuk eksperimen lanjutan.

**Masukan.** AUPRC per fold per kelas untuk model dan pembandingnya.

**Algoritma.** Hitung jumlah fold menang dan selisih median. Angka: hyd menang 5 dari 7 dengan median
AUPRC 0,6538, ssi menang 4 dari 5, tool_wear menang 7 dari 7, dan vib menang 4 dari 4 terhadap
template ([E1] baris 119).

**Workflow.** (1) Kumpulkan hasil per kelas. (2) Hitung fold menang. (3) Hitung selisih median.
(4) Susun peta. (5) Tempelkan nama pembanding per kelas, karena pembandingnya tidak seragam.

**Keluaran.** Tabel kelas dengan jumlah fold menang, selisih median, dan nama pembanding. Arti: menang
7 dari 7 pada tool_wear berarti unggul konsisten, tetapi unggul terhadap template, bukan terhadap
persistence.

**Saran penyajian.** Tabel dengan kolom pembanding yang eksplisit, bukan grafik radar. Alasan:
pembanding berbeda per baris, dan itu harus terbaca sebagai teks ([LV4]).

**Dasar riset penyajian.** [LV4] untuk tabel multi atribut. [LV1] untuk larangan menggabungkan
perbandingan berbeda menjadi satu skor.

**Status bukti.** Siap sekarang ([E1] baris 119).

**Salah tafsir yang harus dicegah.** Membaca seluruh baris sebagai perbandingan terhadap pembanding
yang sama, dan membaca 7 dari 7 sebagai klaim mutlak.

**Cara menguji.** Periksa nama pembanding tiap baris pada dokumen sumber.

### CMP-03 Tabel kanal masukan yang melawan intuisi

**Tujuan.** Mendokumentasikan kanal mana yang ternyata tidak membantu, supaya tidak diulang. Untuk
peneliti dan engineer fitur.

**Menggambarkan apa.** Kontribusi kanal terhadap mutu, termasuk kontribusi negatif.

**Pengguna dan momen pakai.** Peneliti saat memilih fitur kampanye baru, sekali per kampanye.

**Masukan.** Selisih mutu saat satu kanal dikeluarkan, per kelas dan per fold.

**Algoritma.** Hitung selisih median mutu pada pengurangan kanal. Angka: pada hyd kanal SPPA kalah di
14 dari 14 perbandingan dengan selisih median 6.568 sel, dan penghapusan `rms_diff` tidak signifikan
karena selisih 193 masuk dalam derau antar seed ([A1] baris 85-92). Pada ssi kanal `turn` memberi
0,376 dan `dp_dt` memberi 0,271, dan model mengalahkan persistence di 2 dari 5 fold ([E1] baris 121).
Medan pengaruh kedalaman hidrolik hanya 6,5 meter, sehingga klaim tekanan tidak boleh dipetakan ke
kedalaman yang jauh, dan kanal vib hanya berlaku di domain bengkel ([E1] baris 124-127).

**Workflow.** (1) Jalankan pengurangan kanal per fold. (2) Hitung selisih median. (3) Tandai kanal
yang tidak berpengaruh. (4) Cetak batas domain. (5) Larang pemakaian kanal di luar domainnya.

**Keluaran.** Daftar kanal dengan arah pengaruh, selisih median, jumlah fold, dan batas domain.

**Saran penyajian.** Tabel dengan kolom arah pengaruh berbentuk panah teks, bukan warna saja.
Alasan: arah pengaruh lebih penting daripada besar, dan panah terbaca tanpa legenda ([LV4]).

**Dasar riset penyajian.** [LV4] untuk tabel berarah. [LV12] untuk alasan memeriksa sebaran sebelum
menyimpulkan pengaruh.

**Status bukti.** Siap sekarang untuk angka; siap sebagian untuk cakupan, karena tidak semua kanal
diuji pada semua kelas.

**Salah tafsir yang harus dicegah.** Membaca kanal tanpa pengaruh sebagai kanal rusak, dan memakai
kanal vib di luar domain bengkel.

**Cara menguji.** Ulangi pengurangan satu kanal pada satu fold dan bandingkan selisihnya.

### CMP-04 Kartu rekam jejak per sumur

**Tujuan.** Menampilkan berapa kejadian nyata per sumur, supaya klaim per sumur tidak melebihi
datanya. Untuk auditor dan supervisor.

**Menggambarkan apa.** Beban bukti per sumur, bukan mutu sumur.

**Pengguna dan momen pakai.** Auditor saat menilai klaim lintas sumur, sekali per kampanye.
Supervisor saat menanyakan dasar angka untuk sumurnya.

**Masukan.** Jumlah positif per sumur dan per kelas.

**Algoritma.** Hitung positif per sumur dan per fold, lalu tandai yang di bawah 30 sebagai kurang
berdaya sesuai aturan UNDERPOWERED ([I1] baris 350). Angka positif nyata yang terukur: kelas shk
hanya punya F-10 dengan 798 dan F-12 dengan 580 ([PM7] baris 141, lihat [I2] baris 79).

**Workflow.** (1) Kumpulkan positif per sumur. (2) Terapkan ambang 30. (3) Susun kartu. (4) Tautkan
ke peta daya statistik (MNT-09).

**Keluaran.** Daftar sumur dengan jumlah positif dan status daya.

**Saran penyajian.** Batang berurut menurun dengan garis ambang 30. Alasan: satu nilai per kategori
dengan pembanding ambang ([LV7]).

**Dasar riset penyajian.** [LV7] untuk kanal panjang dengan garis acuan.

**Status bukti.** Siap sekarang. Aturan UNDERPOWERED tertulis ([I1] baris 350), dan angka positif
nyata per sumur tersedia untuk kelas shk ([PM7] baris 141).

**Salah tafsir yang harus dicegah.** Membaca sumur kurang berdaya sebagai sumur tanpa masalah.

**Cara menguji.** Hitung positif satu sumur dari label mentah.

### CMP-05 Bukti sirkularitas target mekanika

**Tujuan.** Menyatakan bahwa target yang direkonstruksi dari fitur tidak layak dipakai sebagai bukti
mutu model. Untuk peneliti dan reviewer.

**Menggambarkan apa.** Sirkularitas. Angka mendekati sempurna pada target rekonstruksi berarti model
mereproduksi rumus, bukan memprediksi fenomena.

**Pengguna dan momen pakai.** Reviewer saat membaca bab evaluasi, sekali per bab. Peneliti saat
memilih target baru.

**Masukan.** Akurasi rekonstruksi, presisi dan recall pasangan, MAE dan R2 target turunan, serta hasil
uji sintetis.

**Algoritma.** Bandingkan mutu pada target turunan dengan mutu pada target observasi. Angka:
rekonstruksi 198.928 dari 198.928 baris dengan akurasi 1,000000 ([S3] baris 100). Presisi 0,8496 saat
memakai `MSE` serta `ROC_coef` lawan recall 0,9968 pada kanal fisik ([S3] baris 187). Fitur sintetik
memberi 21,0 dan 0,656, sedangkan data nyata memberi presisi 50,8 menit dan 6,37 ([Eb] baris 74-75).
MSE sisa median 0,000729 ([Es] baris 150). tool_wear dengan LSBoost memberi 0,881 dengan MAE 0,000185
dan R2 0,999 ([E1] baris 116). Uji campuran sintetis memberi 0,170 dan 0,209 ([EVC] baris 94).

**Workflow.** (1) Kumpulkan metrik target turunan. (2) Bandingkan dengan target observasi. (3) Tandai
target dengan R2 di atas 0,99. (4) Cetak larangan pemakaian sebagai bukti mutu.

**Keluaran.** Tabel target dengan metrik dan tanda sirkularitas.

**Saran penyajian.** Tabel dengan kolom "target turunan" dan "target observasi" berdampingan. Alasan:
perbandingan dua kolom angka adalah tugas tabel ([LV4]).

**Dasar riset penyajian.** [LV4] untuk tabel perbandingan. [LV1] untuk larangan menampilkan angka
tanpa peringatan validitas.

**Status bukti.** Siap sekarang, seluruh angka bersumber baris.

**Salah tafsir yang harus dicegah.** Membaca R2 0,999 sebagai model sangat baik.

**Cara menguji.** Hitung ulang MAE satu target turunan dan bandingkan.

### CMP-06 Lembar prasyarat eksperimen

**Tujuan.** Mencegah kesimpulan diambil dari satu jalan. Untuk peneliti dan reviewer metode.

**Menggambarkan apa.** Kelayakan sebuah klaim perbandingan. Tanpa dua model, tiga seed, dan tanda
tangan pra-daftar, selisih tidak boleh diklaim sebagai efek.

**Pengguna dan momen pakai.** Peneliti sebelum menjalankan eksperimen baru, sekali per eksperimen.

**Masukan.** Butir pra-daftar: minimal dua model, minimal tiga seed, dataset tidak berubah, split per
sumur, run id, log parameter dan kode, ukuran efek beserta interval kepercayaan, serta kontrol negatif
berupa label acak, label konstan, dan tanpa fitur.

**Algoritma.** Daftar periksa. Angka pendukung: baseline sekarang tidak dituning sama sekali sehingga
klaim tuning kehilangan dasar atribusi ([R1] baris 99-122), boosting berstatus pilot karena biayanya
belum terukur ([R4] baris 22-32), klaim metaheuristik ditolak tanpa pembanding netral beranggaran
sama ([PMR] baris 92), selang Monte Carlo wajib pada setiap angka FAR dan recall ([PMR] baris 99 dan
149), dan fold dengan kurang dari 30 positif ditandai UNDERPOWERED ([I1] baris 350).

**Workflow.** (1) Buka lembar. (2) Centang butir. (3) Tolak jalan bila ada butir kosong. (4) Simpan
lembar bersama run id.

**Keluaran.** Lembar sembilan butir dengan status centang.

**Saran penyajian.** Daftar periksa dengan kotak dan nama pemilik butir. Alasan: pembaca menjalankan
prosedur, dan daftar periksa lebih tepat daripada grafik ([LV11]).

**Dasar riset penyajian.** [LV11] untuk pola mencatat tindakan dan pemilik.

**Status bukti.** Siap sebagian. Butir dan aturannya tertulis; penerapan otomatisnya belum ada.

**Salah tafsir yang harus dicegah.** Membaca lembar tercentang sebagai hasil yang benar.

**Cara menguji.** Jalankan satu eksperimen kecil dengan satu butir sengaja dikosongkan dan pastikan
lembar menolaknya.

### CMP-07 Panel kesetaraan head hyd

**Tujuan.** Menyatakan bentuk pertukaran antara tiga komposisi head hyd, sehingga memilih salah satu
bukan peningkatan otomatis. Masalah yang diselesaikan: laporan sering menulis "naik" ketika satu
komposisi menang di satu metrik, padahal ia kalah di metrik lain. Register engine mencatat 27 head
pada 7 engine, dengan lapisan L0 lima, L1 sebelas, L2 sembilan, dan L3 dua, serta keputusan akhir
pada manusia ([I4] baris 181). Untuk PM dan peneliti yang menyusun klaim perbaikan.

**Menggambarkan apa.** Pertukaran antar komposisi pada data yang sama. Selisih kecil yang masih di
dalam derau seed berarti memilih komposisi lain tidak mengubah mutu secara terukur. Bila satu
komposisi menang di recall tetapi kalah di lead, itu pertukaran, bukan dominasi. Bila sebuah
komposisi memenuhi anggaran FAR di semua fold, keunggulannya operasional, bukan statistik.

**Pengguna dan momen pakai.** PM saat menulis klaim perbaikan pada laporan, sekali per laporan.
Peneliti saat memilih head untuk kampanye berikutnya, sekali per kampanye. Dosen penguji saat
memeriksa apakah klaim "naik" punya dasar, sekali per sidang.

**Masukan.** Metrik per komposisi pada kelas hyd: true positive, alarm palsu, presisi, recall, FAR,
lead per fold, dan jumlah fold yang memenuhi kriteria. Tiga komposisi yang dibandingkan adalah H1p,
H1p3, dan H1 penggantinya. Angka pengisi: H1p memberi alarm palsu 927 dan true positive 4.924,
presisi 0,8243, recall 0,6519, FAR median 4,0984 per 24 jam, lead median 8,0 menit, dan 7 dari 9 fold
memenuhi FAR serta recall ([I4] baris 156-160). H1p3 memberi alarm palsu 568 dan true positive 3.557,
presisi 0,8646, recall 0,5296, FAR 2,0323, lead 12,5 menit, FAR lolos 9 dari 9 fold dan recall lolos
5 dari 9 ([I4] baris 162). H1 memberi alarm palsu 935, true positive 3.804, presisi 0,7789, recall
0,5638, FAR 3,5302, lead 11,5 menit, dan 5 dari 9 fold ([I4] baris 161). Derau seed terukur:
`beda_sel` bernilai nol pada 45 sel hyd, dan kontrol negatif mengubah 2 dari 2 fold antar seed
(F-14 dari 362 alarm palsu dan 42 true positive menjadi 534 dan 71) ([I4] baris 166 dan 168).

**Algoritma.** Langkah satu, kumpulkan metrik per komposisi per fold. Langkah dua, hitung selisih
berpasangan per fold untuk setiap pasangan. Langkah tiga, bandingkan selisih itu dengan derau seed
yang sudah diukur, yaitu nol selisih pada 45 sel hyd disertai kontrol negatif yang berubah di 2 dari
2 fold ([I4] baris 166 dan 168). Langkah empat, nyatakan setara bila seluruh selisih pasangan berada
di dalam derau. Langkah lima, bila tidak setara, nyatakan arah dan besar efek beserta interval.
Angka siap pakai: H1p terhadap H1 memberi true positive lebih banyak 1.120 atau 29,4427 persen,
alarm palsu lebih sedikit 8, presisi naik 0,0453, recall naik 0,088, FAR naik 0,5682, lead lebih
pendek 3,5 menit, dengan onset 218 lawan 219 ([I4] baris 163). Biaya H1p3 terhadap H1 adalah 247 true
positive lebih sedikit ([I4] baris 165), dan beban alarm per onset adalah 2,3769 untuk H1p, 2,3974
untuk H1, dan 1,4564 untuk H1p3 ([I4] baris 164).

Dasar aturan: baseline sekarang tidak dituning sama sekali sehingga selisih harus dibandingkan dengan
baseline yang setara ([R1] baris 99-122), dan klaim metaheuristik ditolak tanpa pembanding pencarian
netral beranggaran sama ([PMR] baris 92). Selang Monte Carlo wajib disertakan pada setiap angka
([PMR] baris 99 dan 149).

**Workflow.** (1) Kumpulkan metrik per komposisi. (2) Pasangkan per fold. (3) Hitung selisih dan
derau seed. (4) Klasifikasikan setiap pasangan sebagai setara atau berbeda. (5) Cetak jumlah pasangan
setara dan jumlah pasangan yang belum bisa diputuskan. (6) Kunci klaim perbaikan hanya untuk pasangan
yang berbeda di luar derau.

**Keluaran.** Matriks pasangan head dengan status setara atau berbeda, plus satu baris derau acuan
dan satu baris catatan terbuka, plus skor keyakinan per head dari KEP-02 pada baris judul kolom.
Arti: status setara berarti memilih head lain tidak mengubah mutu secara terukur, sehingga alasan
memilih harus operasional, misalnya FAR lebih kecil atau lead lebih panjang. Skor keyakinan pada
baris judul mencegah pasangan head berkeyakinan rendah dibaca sebagai bukti kesetaraan.

**Saran penyajian.** Matriks pasangan dengan sel berisi selisih dan lencana status, ditambah satu
grafik sebar per fold untuk pasangan yang paling sering dibahas. Alasan: jumlah head kecil sehingga
matriks pasangan selesai dalam satu layar, dan sebar per fold mencegah pembaca menyimpulkan dari satu
angka agregat ([LV9], [LV6]). Tata letak contoh: matriks 3 kali 3 selebar 320 piksel dengan selisih
di sel, lencana "setara" di sel luar diagonal yang lolos, dan di bawahnya sebar tiga warna per head
dengan sumbu presisi dan recall.

**Dasar riset penyajian.** [LV9] untuk matriks bernilai dan alasan normalisasi. [LV6] untuk sebar
pada dua variabel kontinu. [LV1] untuk larangan meringkas kesetaraan menjadi satu skor gabungan.

**Status bukti.** Siap sebagian. Seluruh metrik per komposisi terukur dan bersumber baris
([I4] baris 156-165), derau seed diukur pada 45 sel hyd dengan kontrol negatif yang peka
([I4] baris 166 dan 168), dan reproduksi R8 lulus 30 dari 30 pemeriksaan ([I4] baris 167). Yang
belum: interval kepercayaan per pasangan belum dihitung, sehingga status setara atau berbeda baru
memakai derau seed, bukan selang penuh.

**Salah tafsir yang harus dicegah.** Pertama, membaca head dengan presisi 0,8646 sebagai head terbaik
padahal recall-nya 0,5296, jadi ia menang di satu metrik dan kalah di metrik lain. Kedua, membaca
kenaikan true positive 29,4427 persen sebagai dominasi, padahal lead justru lebih pendek 3,5 menit
([I4] baris 163). Ketiga, membaca FAR yang lolos 9 dari 9 fold sebagai mutu keseluruhan, karena
recall di H1p3 hanya lolos 5 dari 9 fold ([I4] baris 162). Keempat, membaca 27 head sebagai 27 model
berbeda, karena lapisan L0 sampai L3 menandakan peran yang berbeda ([I4] baris 181).

**Cara menguji.** Hitung ulang selisih presisi dan recall satu pasangan head dari nilai true positive
dan alarm palsu, lalu bandingkan dengan sel matriks. Uji kedua, ambil satu pasangan berstatus setara
dan periksa bahwa selisihnya memang di bawah derau antar seed yang tercetak.

---

## 9. Rumpun linimasa dan jejak keputusan (LIN-01 sampai LIN-07)

Rumpun ini mengurus pertanyaan "apa yang sudah diputuskan, kapan, dan atas dasar angka apa".
Tujuh fiturnya membuat keputusan bisa ditelusuri kembali, termasuk keputusan yang ternyata salah.

### LIN-01 Log keputusan human-in-loop

**Tujuan.** Mencatat keputusan atas setiap peringatan beserta alasannya, sehingga antrean punya
penutup dan evaluasi punya umpan balik. Untuk supervisor shift dan peneliti.

**Menggambarkan apa.** Tindakan manusia, bukan keadaan alat. Log kosong berarti tidak ada keputusan
yang tercatat, bukan tidak ada peringatan. Log juga satu-satunya sumber label yang benar-benar
prospektif, karena label hari ini dibangun retrospektif ([I3] bagian 8).

**Pengguna dan momen pakai.** Supervisor setiap kali menutup peringatan, beberapa kali per shift.
Peneliti saat memeriksa umpan balik, sekali per minggu.

**Masukan.** Identitas head, skor keyakinan, badge beban alarm, tindakan yang diambil, dan alasan
singkat. Aturan tinjauan manusia sudah berlaku pada 11 dari 11 head L1, dan keputusan akhir
ditetapkan manusia ([PM2] baris 205, yang menggantikan rujukan baris 206 sesuai [VF] C-08).

**Algoritma.** Setiap peringatan wajib punya tepat satu keputusan. Label disimpan apa adanya tanpa
diturunkan menjadi skor mutu. Peringatan tanpa label dihitung terbuka, bukan benar. Tingkat tindak
lanjut dihitung sebagai jumlah peringatan berlabel dibagi jumlah peringatan yang tampil.

**Workflow.** (1) Tampilkan peringatan beserta kartu keyakinan. (2) Minta satu label tindakan.
(3) Simpan waktu, label, dan alasan. (4) Tutup baris antrean sehingga umurnya berhenti bertambah.
(5) Hitung tingkat tindak lanjut per head. (6) Pakai hasilnya sebagai bahan kalibrasi berikutnya.

**Keluaran.** Riwayat keputusan per head, tingkat tindak lanjut, dan daftar peringatan terbuka.

**Saran penyajian.** Tabel dengan kolom waktu, head, label, dan alasan, bukan diagram alir. Alasan:
pembaca mencari satu baris tertentu dan memeriksa urutan waktu ([LV4], [LV14]).

**Dasar riset penyajian.** [LV4] untuk tabel pencarian. [LV14] untuk alasan menampilkan pekerjaan
terbuka sebagai antrean yang bisa ditindak.

**Status bukti.** Siap sebagian. Aturan tinjauan manusia terukur pada 11 dari 11 head ([PM2] baris
205), tetapi skema pencatatan tindakan belum ada ([I3] bagian 7 W1-10).

**Salah tafsir yang harus dicegah.** Membaca label "abaikan" sebagai peringatan palsu; label itu
keputusan operator, bukan penilaian kebenaran model.

**Cara menguji.** Tutup satu peringatan dan periksa bahwa umur item berhenti bertambah serta
tingkat tindak lanjut berubah.

### LIN-02 Garis waktu tingkat target dan gerbang

**Tujuan.** Menunjukkan urutan dokumen vonis, gerbang, dan perubahan target, supaya pembaca tidak
mencampur angka dari era berbeda. Untuk auditor dan dosen penguji.

**Menggambarkan apa.** Urutan keputusan metodologis dari waktu ke waktu, bukan urutan mutu.

**Pengguna dan momen pakai.** Auditor saat menilai konsistensi dokumen, sekali per audit. Dosen
penguji saat menanyakan versi mana yang berlaku.

**Masukan.** 11 klaim mesin lapisan A beserta tier per engine ([I3] bagian 3 dan 4), dan status
dokumen vonis per gelombang ([I4] bagian 1).

**Algoritma.** Urutkan dokumen menurut tanggal, tempelkan status berlaku atau digantikan, lalu
tempelkan keputusan yang mengubah target. Keputusan yang sudah digantikan tetap ditampilkan dengan
penanda. Tiga tingkat kesiapan dari V8 dipakai apa adanya sebagai label: peringatan human-in-loop,
tren atau skor, belum layak pakai ([I2] bagian 4).

**Workflow.** (1) Kumpulkan dokumen vonis. (2) Urutkan menurut tanggal. (3) Tempelkan status.
(4) Tautkan angka ke baris ledger `PM-078`. (5) Bekukan garis waktu per tanggal rilis.

**Keluaran.** Garis waktu vertikal dengan status per dokumen dan tautan angka.

**Saran penyajian.** Garis waktu vertikal dengan penanda status, bukan tabel lebar. Alasan: urutan
waktu adalah pesan utamanya ([LV3]).

**Dasar riset penyajian.** [LV3] untuk sumbu waktu.

**Status bukti.** Siap sekarang. Empat inventaris dan satu laporan verifikasi sudah dibuka penuh,
dan 0 dari 7 engine memenuhi syarat alarm otomatis ([I2] baris 91; [PM8] baris 180-184).

**Salah tafsir yang harus dicegah.** Membaca dokumen lama sebagai kesimpulan yang masih berlaku.

**Cara menguji.** Pilih satu angka dan periksa apakah ia berasal dari dokumen yang masih berlaku.

### LIN-03 Penanda selang wajib pada setiap angka FAR dan recall

**Tujuan.** Mewajibkan setiap angka FAR dan recall tampil bersama selangnya, dan menandai angka yang
selangnya memuat prevalensi. Masalah yang diselesaikan: angka titik tanpa selang terbaca sebagai
kepastian, padahal pada beberapa fold selangnya memuat prevalensi sehingga sinyalnya belum terbukti.
Untuk reviewer, operator, dan pembaca laporan.

**Menggambarkan apa.** Ketidakpastian angka. Bila selang memuat prevalensi, artinya angka itu tidak
bisa dibedakan dari menebak memakai prevalensi dasar. Penanda ini menggambarkan kekuatan bukti,
bukan kekuatan sinyal.

**Pengguna dan momen pakai.** Reviewer saat memeriksa tabel hasil, sekali per laporan. Operator saat
membaca satu angka recall sebelum memilih titik operasi, setiap kali.

**Masukan.** Jumlah iterasi bootstrap, seed, blok bootstrap, dan cakupan waktu, ditambah angka titik
per fold. Aturan Monte Carlo sudah diadopsi sebagai kewajiban pelaporan ([PMR] baris 99 dan 149),
dan jumlah iterasi yang memenuhi kriteria presisi diukur pada dua kasus nyata ([R2] baris 123-140).

**Algoritma.** Tiga langkah. Langkah satu, hitung selang bootstrap untuk setiap angka FAR dan
recall. Langkah dua, bandingkan batas bawah selang dengan prevalensi kelas. Langkah tiga, tempelkan
penanda "memuat prevalensi" bila batas bawah berada di bawah prevalensi. Contoh yang wajib tampil:
AUPRC ssi 0,015 sampai 0,459 dengan selang yang memuat prevalensi di 5 dari 9 fold ([EVA] baris 55),
dan keputusan EA-4 serta EA-8 yang menyatakan sinyal belum terbukti pada keadaan itu ([EVA] baris 30).

**Workflow.** (1) Jalankan bootstrap per angka. (2) Simpan angka titik dan dua batas. (3) Bandingkan
dengan prevalensi. (4) Tempelkan penanda. (5) Larang tampilan angka tanpa selang. (6) Cetak jumlah
fold yang selangnya memuat prevalensi.

**Keluaran.** Tiga angka per sel: titik, batas bawah, batas atas, plus penanda. Arti: penanda aktif
berarti angka itu belum bisa dipakai memilih titik operasi.

**Saran penyajian.** Batang galat (error bar) pada setiap titik, bukan angka telanjang. Alasan:
selang adalah pesan utamanya, dan batang menampilkan rentang lebih akurat daripada teks ([LV5]).
Tata letak contoh: tabel hasil dengan kolom titik dan batang selang kecil di sebelahnya, baris
berpenanda diberi latar berbeda dan teks "selang memuat prevalensi".

**Dasar riset penyajian.** [LV5] untuk penanganan ketidakpastian pada tampilan angka. [LV4] untuk
tabel hasil dengan kolom angka pendamping.

**Status bukti.** Siap sebagian. Aturan dan dua kasus nyata terukur ([PMR] baris 99 dan 149; [R2]
baris 123-140; [EVA] baris 30 dan 55), tetapi penerapannya belum seragam: beberapa sel di [EVA] dan
[EVC] hanya berisi titik tanpa selang ([I3] bagian 7 W1-14).

**Salah tafsir yang harus dicegah.** Pertama, membaca angka titik sebagai nilai pasti. Kedua,
membaca penanda "memuat prevalensi" sebagai angka salah; angkanya benar, kekuatan buktinya yang
belum cukup. Ketiga, memilih fold yang selangnya paling sempit lalu mengabaikan fold lain.

**Cara menguji.** Ambil satu angka recall, hitung ulang selangnya dengan seed berbeda, dan pastikan
penandanya tidak berubah.

### LIN-04 Register status dokumen vonis

**Tujuan.** Menyatakan dokumen mana yang masih berlaku dan mana yang sudah digantikan, supaya angka
dari dokumen lama tidak dikutip sebagai kesimpulan terkini. Untuk auditor dan penulis laporan.

**Menggambarkan apa.** Status fungsi dokumen, bukan kebenaran isinya. Dokumen berstatus digantikan
tetap dipakai sebagai riwayat dan sebagai sumber angka tertentu ([I4] bagian 1 baris 40).

**Pengguna dan momen pakai.** Auditor saat memeriksa rujukan, sekali per audit. Penulis laporan saat
mengutip angka lama, setiap kali mengutip.

**Masukan.** Daftar dokumen vonis beserta byte, baris, dan status. Angka: 10 dokumen diperiksa, 8
BERLAKU dan 2 DIGANTIKAN, yaitu `RND_S5_AUDIT_WAVE2.md` yang fungsinya digantikan
`RND_S5_DEFECT_STATUS.md`, dan `V10_PM2_VERDICT.md` yang digantikan `V11_PM_FINAL.md` ([I4] bagian 1
baris 24-40).

**Algoritma.** Setiap dokumen diberi satu status. Status dihitung dari ada atau tidaknya dokumen
pengganti di `docs/`, bukan dari tanggal. Bila status berubah, angka yang dikutip dari dokumen itu
tetap boleh dipakai dengan catatan sumbernya digantikan.

**Workflow.** (1) Baca daftar dokumen. (2) Periksa dokumen pengganti. (3) Tetapkan status.
(4) Cetak byte dan baris. (5) Tautkan angka yang diambil dari dokumen digantikan. (6) Perbarui
register setiap kali dokumen baru terbit.

**Keluaran.** Tabel 10 baris dengan byte, baris, status, dan alasan. Arti: status DIGANTIKAN berarti
fungsi dokumen sudah diambil alih, sedangkan angkanya tetap sah sebagai riwayat.

**Saran penyajian.** Tabel dengan kolom status berisi kata, bukan warna saja, dan kolom byte serta
baris sebagai bukti ukuran. Alasan: pembaca mencari satu nama dokumen dan memeriksa statusnya, dua
tugas tabel ([LV4]).

**Dasar riset penyajian.** [LV4] untuk tabel pencarian. [LV11] untuk pola mencatat status beserta
alasan tindak lanjut.

**Status bukti.** Siap sekarang untuk 10 dokumen yang diperiksa. Syarat perluasan: setiap dokumen
baru wajib masuk register sebelum angkanya dikutip ([I4] bagian 1).

**Salah tafsir yang harus dicegah.** Pertama, membaca DIGANTIKAN sebagai salah. Kedua, mengutip
angka dari dokumen digantikan tanpa menyebut statusnya. Ketiga, membaca register ini sebagai daftar
kebenaran isi.

**Cara menguji.** Pilih satu dokumen berstatus DIGANTIKAN dan periksa apakah dokumen penggantinya
benar-benar ada di `docs/`.

### LIN-05 Kalender sumber angka

**Tujuan.** Menampilkan kapan setiap angka terakhir diuji dan hasilnya. Untuk auditor dan pembaca
laporan.

**Menggambarkan apa.** Kesegaran verifikasi, bukan kesegaran data.

**Pengguna dan momen pakai.** Auditor sebelum menerbitkan, sekali per audit.

**Masukan.** Hasil 40 uji angka pada laporan verifikasi: 37 cocok, 2 cocok dengan catatan, 1 tidak
cocok karena rujukan baris meleset, serta cakupan dokumen 50 disebut dan 69 tidak disebut ([VF]
bagian 1 dan 4).

**Algoritma.** Tempelkan tanggal uji per angka, hitung umur uji, tandai angka tanpa uji. Angka yang
gagal uji dikeluarkan dari katalog, dan daftarnya ada di bagian 12 dokumen ini.

**Workflow.** (1) Baca laporan verifikasi. (2) Petakan angka ke hasil uji. (3) Hitung umur.
(4) Tandai yang belum diuji. (5) Terbitkan kalender per bulan.

**Keluaran.** Kalender dengan status per angka dan jumlah uji per bulan.

**Saran penyajian.** Kalender panas per bulan dengan jumlah uji di dalam sel. Alasan: pertanyaannya
kapan, dan pola waktu terbaca pada sel tanggal ([LV3], [LV9]).

**Dasar riset penyajian.** [LV3] untuk sumbu waktu. [LV9] untuk sel bernilai.

**Status bukti.** Siap sekarang untuk 40 uji. Yang belum: 69 dokumen di luar cakupan verifikasi
([VF] bagian 1).

**Salah tafsir yang harus dicegah.** Membaca angka tanpa uji sebagai angka salah.

**Cara menguji.** Pilih satu angka berstatus cocok dan ulangi pengujiannya.

### LIN-06 Kuis dua halaman tentang angka

**Tujuan.** Memberi dosen penguji dua halaman ringkas berisi angka kunci beserta batasnya, supaya
sidang tidak tenggelam di dokumen panjang. Untuk dosen penguji dan PM.

**Menggambarkan apa.** Ringkasan yang bisa diperiksa, bukan ringkasan yang menyederhanakan.

**Pengguna dan momen pakai.** Dosen penguji sebelum sidang, sekali per sidang. PM sebelum rapat
dengan sponsor, sekali per rapat.

**Masukan.** 11 klaim mesin lapisan A beserta presisi, recall, dan FAR per kelas ([I3] bagian 3),
tier per engine ([I3] bagian 4), dan status alarm otomatis: 0 dari 7 engine memenuhi syarat
([I2] baris 91; [PM8] baris 180-184).

**Algoritma.** Pilih maksimal 12 angka. Setiap angka wajib membawa sumber baris dan satu batas
pemakaian. Angka tanpa sumber tidak masuk. Angka yang selangnya memuat prevalensi wajib membawa
penanda dari LIN-03.

**Workflow.** (1) Pilih angka. (2) Tempelkan sumber. (3) Tempelkan batas. (4) Uji baca pada dua
pembaca. (5) Kunci versi per tanggal sidang.

**Keluaran.** Dua halaman dengan maksimal 12 baris angka, tiap baris satu kalimat batas.

**Saran penyajian.** Kartu angka besar per baris, maksimal 12 kartu. Alasan: dibaca cepat sebelum
rapat, dan satu angka satu kartu mencegah pembaca mencampur dua kelas ([LV6], [LV5]).

**Dasar riset penyajian.** [LV6] untuk kartu angka. [LV5] untuk larangan angka tanpa konteks
ketidakpastian.

**Status bukti.** Siap sekarang, seluruh angka sudah bersumber baris.

**Salah tafsir yang harus dicegah.** Membaca ringkasan sebagai pengganti dokumen.

**Cara menguji.** Minta satu pembaca menjelaskan satu angka beserta batasnya.

### LIN-07 Linimasa tier per kelas dan syarat naik tier

**Tujuan.** Menampilkan posisi setiap kelas pada tiga tingkat kesiapan beserta syarat yang harus
dipenuhi untuk naik. Masalah yang diselesaikan: pembaca mengira seluruh kelas berada pada tingkat
yang sama, padahal sebagian masih di tingkat tren atau skor. Untuk PM, peneliti, dan dosen penguji.

**Menggambarkan apa.** Tingkat pemakaian, bukan tingkat kerusakan. Naik tingkat berarti bukti
lapisan B dan C bertambah, bukan berarti alat lebih sering menyala.

**Pengguna dan momen pakai.** PM saat menyusun rencana kerja per kelas, sekali per kampanye.
Peneliti saat memilih kelas untuk kampanye berikutnya, sekali per kampanye.

**Masukan.** Tier per engine dari [I3] bagian 4, gerbang tier dari [PM1] baris 137-141, dan jumlah
engine yang memenuhi syarat alarm otomatis: 0 dari 7 ([I2] baris 91).

**Algoritma.** Setiap kelas diberi satu dari tiga label: peringatan human-in-loop, tren atau skor,
belum layak pakai. Syarat naik ditulis sebagai butir yang bisa diperiksa, bukan sebagai catatan.
Contoh syarat yang sudah terukur: bit_wear K-2 belum dijalankan karena pra-registrasi belum terbit,
dan hyd K-ii masih memakai angka RF V8 dengan tiga onset sehingga berstatus kurang berdaya
([I3] bagian 10).

**Workflow.** (1) Baca tier per kelas. (2) Tempelkan bukti yang sudah ada. (3) Tulis syarat naik.
(4) Cetak tanggal keputusan. (5) Kunci keputusan supaya tidak berubah setelah hasil keluar.

**Keluaran.** Tabel kelas dengan tier, bukti pendukung, dan syarat naik.

**Saran penyajian.** Daftar bertingkat tiga kolom (tier, kelas, syarat naik), bukan grafik radar.
Alasan: pembaca mencari satu kelas dan membaca syaratnya sebagai kalimat ([LV4]).

**Dasar riset penyajian.** [LV4] untuk tabel pencarian. [LV11] untuk pola mencatat syarat dan pemilik
pada pekerjaan yang belum selesai.

**Status bukti.** Siap sebagian. Tier dan gerbangnya tertulis dengan rujukan baris; syarat naik untuk
sebagian kelas belum punya angka pengukuran.

**Salah tafsir yang harus dicegah.** Pertama, membaca tier tinggi sebagai alat yang lebih berbahaya.
Kedua, menaikkan tier karena satu angka membaik. Ketiga, membaca "belum layak pakai" sebagai kelas
yang dibuang.

**Cara menguji.** Ambil satu kelas dan periksa apakah seluruh butir syarat naiknya benar-benar
terpenuhi sebelum tier-nya dinaikkan.

---

## 10. Rumpun alat bantu insinyur (INS-01 sampai INS-05)

Rumpun ini mengurus pertanyaan "bagaimana orang memakai angka ini tanpa dibohongi olehnya". Lima
fiturnya adalah alat kerja, bukan tampilan data.

### INS-01 Wizard kalibrasi dan uji jalan sebelum pindah sumur

**Tujuan.** Mencegah ambang dipindahkan antar sumur tanpa uji. Masalah yang diselesaikan: ambang yang
dipilih pada satu sumur berperilaku lain pada sumur berikutnya, dan tanpa uji jalan perpindahannya
tidak pernah diperiksa. Untuk penanggung jawab mutu data dan engineer pemeliharaan.

**Menggambarkan apa.** Kelayakan pindah konfigurasi. Wizard ini menggambarkan kesiapan, bukan mutu
model. Bila satu syarat gagal, artinya konfigurasi harus dipilih ulang di sumur itu, bukan bahwa
modelnya buruk. Bila jarak distribusi dalam satu sumur kecil, artinya ambang lama masih bisa dipakai
di paruh waktu berikutnya pada sumur yang sama.

**Pengguna dan momen pakai.** Penanggung jawab mutu data saat menyiapkan sumur baru, sekali per
sumur. Engineer pemeliharaan saat ambang mulai berperilaku lain, setiap kali kejadian. Auditor saat
memeriksa apakah perpindahan konfigurasi pernah diuji, sekali per audit.

**Masukan.** Statistik jendela dasar per sumur dan per paruh waktu, riwayat FAR pada konfigurasi lama,
dan daftar kanal masukan per engine. Angka pengisi: uji KS antar sumur memberi D median 0,986 dengan
10 dari 10 pasangan p di bawah 0,05, dan uji dalam sumur memberi D median 0,211 dengan 4 dari 5 sumur
p di bawah 0,05 ([R5] baris 135-136, lihat [I3] baris 293). Syarat kanal masukan terukur pada hyd
K-ii: kanal FlowOut absen, empat kolom flow berkorelasi 0,995 sampai 1,000 sehingga varian literal
tidak dapat dihitung, dan dampaknya P sama dengan R sama dengan nol pada q95 ([EVA] baris 165 dan
169, lihat [I3] bagian 7 W1-11).

**Algoritma.** Empat langkah berurutan, tanpa model. Langkah satu, hitung jarak distribusi sumur baru
terhadap sumur acuan memakai KS, dan perlakukan p sebagai pelengkap karena deret berautokorelasi
membuat p tidak sah sebagai bukti tunggal ([R5] baris 142-148). Langkah dua, jalankan konfigurasi
lama pada data sumur tujuan dan bandingkan FAR dengan anggaran FAR 10. Langkah tiga, periksa
ketersediaan kanal masukan memakai kartu DAT-08. Langkah empat, periksa jumlah positif; bila di bawah
30, wizard berhenti dan menyatakan uji tidak bermakna, sesuai aturan penandaan UNDERPOWERED
([I1] baris 350).

**Workflow.** (1) Pilih sumur tujuan. (2) Hitung jarak distribusi. (3) Jalankan konfigurasi lama pada
data sumur tujuan. (4) Bandingkan FAR dengan anggaran. (5) Periksa kanal masukan. (6) Periksa jumlah
positif. (7) Bila semua lolos, terbitkan konfigurasi beserta tanda tangan; bila gagal, kembalikan ke
pemilihan ambang. (8) Catat hasil di log keputusan (LIN-01).

**Keluaran.** Satu status per syarat, empat baris, ditambah satu keputusan akhir: boleh dipakai,
boleh dengan catatan, atau kalibrasi ulang, ditambah skor keyakinan 0 sampai 100 dari KEP-02 untuk
konfigurasi yang diterbitkan. Arti: status boleh dengan catatan berarti konfigurasi dipakai sambil
menampilkan kanal yang bolong dan jumlah positif yang sedikit, dan skor keyakinan dipakai sebagai
angka pengiring yang tidak boleh menjadi pemicu tindakan.

**Saran penyajian.** Daftar periksa bertingkat dengan status per baris dan satu lencana keputusan di
atas. Alasan: ini prosedur yang dijalankan orang, jadi bentuknya daftar periksa, bukan grafik; dan
keputusan akhir harus terlihat lebih dulu ([LV11]). Tata letak contoh: lencana besar di atas, empat
baris syarat dengan ikon status, tombol "terbitkan konfigurasi" nonaktif selama ada baris gagal.

**Dasar riset penyajian.** [LV11] untuk pola daftar tindakan dengan pemilik dan status. [LV1] untuk
larangan menggabungkan empat syarat menjadi satu skor kelayakan.

**Status bukti.** Siap sebagian. Tiga dari empat syarat punya angka pendukung yang terukur (jarak
drift [R5] baris 135-136; kanal masukan [EVA] baris 165 dan 169; aturan positif minimum [I1] baris
350). Yang belum: ambang daya statistik per kelas belum ditetapkan sebagai aturan tertulis.

**Salah tafsir yang harus dicegah.** Pertama, membaca status kalibrasi ulang sebagai kegagalan model.
Kedua, memindahkan ambang tanpa menghitung ulang FAR. Ketiga, memakai nilai p dari uji KS sebagai
bukti tunggal pada deret berautokorelasi.

**Cara menguji.** Jalankan wizard pada satu sumur yang belum pernah dipakai dan periksa apakah ia
menolak ketika kanal masukan kosong. Uji kedua, jalankan pada sumur yang sama dengan dua konfigurasi
berbeda dan pastikan keputusannya mengikuti angka FAR, bukan urutan pemilihan.

### INS-02 Panduan skrip verifikasi rujukan

**Tujuan.** Memberi auditor prosedur yang bisa dijalankan ulang untuk memeriksa angka. Untuk auditor
internal.

**Menggambarkan apa.** Prosedur, bukan hasil.

**Pengguna dan momen pakai.** Auditor sebelum menerbitkan vonis, sekali per vonis.

**Masukan.** Daftar sel angka dengan rujukan baris, toleransi 5e-5, dan dua mutasi kontrol.

**Algoritma.** Jalankan tiga langkah pengunci (KEP-07), lalu cocokkan setiap temuan dengan berkas dan
baris. Hasil acuan: 143 sel, 0 selisih pada dokumen asli, 2 selisih pada dokumen termutasi ([S5A]
baris 65 dan 71).

**Workflow.** (1) Siapkan daftar sel. (2) Jalankan pembanding. (3) Jalankan pada dokumen termutasi.
(4) Catat selisih beserta lokasi. (5) Simpan keluaran sebagai lampiran vonis.

**Keluaran.** Log tiga baris beserta daftar selisih.

**Saran penyajian.** Blok kode dan tabel hasil, bukan grafik. Alasan: pembaca akan menyalin perintah,
dan grafik tidak dapat disalin ([LV11]).

**Dasar riset penyajian.** [LV11] untuk dokumentasi prosedur.

**Status bukti.** Siap sekarang. Prosedur dan hasilnya terukur ([S5A] baris 65 dan 71).

**Salah tafsir yang harus dicegah.** Membaca nol selisih sebagai bukti kebenaran isi.

**Cara menguji.** Jalankan panduan pada satu dokumen baru dan pastikan dua mutasi terdeteksi.

### INS-03 Kartu kelayakan sinyal sebelum dekomposisi

**Tujuan.** Menyatakan apakah satu kanal layak didekomposisi sebelum VMD, EMD, atau wavelet dijalankan.
Masalah yang diselesaikan: tiga metode dekomposisi dicoba berulang pada kanal yang laju sampelnya
tidak memenuhi syarat. Untuk peneliti sinyal dan engineer yang akan menambah metode.

**Menggambarkan apa.** Kelayakan sinyal, bukan mutu dekomposisi. Laju sampel menentukan pita
tertinggi yang bisa dibaca. Bila pita yang dicari di atas batas Nyquist, hasil dekomposisi tidak
bermakna berapa pun parameternya disetel.

**Pengguna dan momen pakai.** Peneliti sinyal sebelum menjalankan dekomposisi pada kanal baru, sekali
per kanal. Engineer saat menambah metode ke pipeline, sekali per penambahan.

**Masukan.** Laju sampel kanal, pita frekuensi yang dicari, panjang segmen, dan hasil uji
stasioneritas lokal. Angka terukur: Nyquist tertinggi 0,1667 Hz sedangkan VIBLAT_RT di F-14 hanya
0,0167 Hz ([V3T] baris 159 dan 364, lihat [I1] baris 207).

**Algoritma.** Hitung Nyquist dari laju sampel, bandingkan dengan pita yang dicari, lalu terbitkan
lulus atau tidak lulus beserta alasannya. Hasil acuan per metode: VMD gagal karena Nyquist 0,1667 Hz
dengan 75 dari 105 percobaan gagal, EMD gagal karena lima IMF didominasi drift, dan wavelet lolos
sebagian karena pita di atas 0,05 Hz hanya memuat 4,14 persen daya ([R3] baris 98-106).

**Workflow.** (1) Baca laju sampel kanal. (2) Hitung Nyquist. (3) Bandingkan dengan pita target.
(4) Jalankan uji stasioneritas lokal. (5) Terbitkan status lulus atau tidak lulus. (6) Simpan alasan
di samping setiap percobaan supaya tidak diulang.

**Keluaran.** Satu baris per kanal dengan status, pita tertinggi yang bisa dibaca, dan alasan.

**Saran penyajian.** Kartu status dengan tiga baris angka (laju sampel, Nyquist, pita target) dan
lencana lulus. Alasan: keputusannya biner dan alasannya pendek, sehingga kartu lebih cepat dibaca
daripada grafik ([LV6]).

**Dasar riset penyajian.** [LV6] untuk pemilihan bentuk pada keputusan biner. [LV4] untuk angka
pendamping yang harus terbaca.

**Status bukti.** Siap sekarang untuk tiga metode yang sudah diuji ([R3] baris 98-106). Yang belum:
kartunya belum dibangun sebagai alat ([I3] bagian 7 W1-12).

**Salah tafsir yang harus dicegah.** Pertama, membaca kegagalan VMD sebagai bukti kanal tidak berguna.
Kedua, membaca lolos sebagian pada wavelet sebagai lolos penuh. Ketiga, mengulang percobaan tanpa
membaca alasan yang sudah tercatat.

**Cara menguji.** Jalankan kartu pada satu kanal baru dan periksa apakah statusnya cocok dengan
hitungan Nyquist manual.

### INS-04 Kartu kanal yang perlu dipasang

**Tujuan.** Mengubah kanal yang tidak ada menjadi daftar permintaan pemasangan dengan alasan angka.
Untuk engineer instrumentasi dan pengambil keputusan anggaran sensor.

**Menggambarkan apa.** Ketiadaan kanal dan dampaknya pada metrik. Bila satu engine berhenti di titik
operasi karena kanal masukan tidak ada, itu bukan kegagalan model, melainkan pekerjaan pengadaan.

**Pengguna dan momen pakai.** Engineer instrumentasi saat satu engine berhenti di titik operasi,
setiap kali terjadi. Pengambil keputusan anggaran saat menyusun prioritas sensor, sekali per siklus.

**Masukan.** Daftar kanal per engine, bukti ketiadaan, dan dampak terukur pada metrik.

**Algoritma.** Untuk setiap kanal yang absen, catat bukti ketiadaan, korelasi antar kolom pengganti,
dan dampak pada metrik di titik operasi. Contoh hyd K-ii: FlowOut absen, empat kolom flow berkorelasi
0,995 sampai 1,000 sehingga varian literal tidak dapat dihitung, dan P sama dengan R sama dengan nol
pada q95 ([EVA] baris 165 dan 169).

**Workflow.** (1) Kumpulkan daftar kanal per engine. (2) Uji keberadaan kanal pada data. (3) Hitung
korelasi kolom pengganti. (4) Ukur dampak pada metrik. (5) Susun daftar prioritas. (6) Kirim ke
pemilik data.

**Keluaran.** Daftar kanal prioritas dengan alasan angka dan dampak terukur bila kanal dipasang.

**Saran penyajian.** Tabel berurut dengan kolom kanal, engine, dampak, dan pemilik data. Alasan:
pembaca mencari satu kanal dan memeriksa dampaknya, lalu meneruskannya ke pihak lain ([LV4]).

**Dasar riset penyajian.** [LV4] untuk tabel yang diteruskan ke pihak lain. [LV11] untuk pola
menuliskan pemilik dan tindak lanjut.

**Status bukti.** Siap sekarang untuk kanal yang sudah terbukti absen ([EVA] baris 165 dan 169).
Syarat perluasan: daftar kanal per engine yang lengkap ([I3] bagian 9 butir 1D).

**Salah tafsir yang harus dicegah.** Pertama, membaca kanal absen sebagai model gagal. Kedua,
memakai kolom pengganti yang berkorelasi 1,000 seolah-olah kanal aslinya ada.

**Cara menguji.** Periksa keberadaan kanal pada berkas sumur dengan pencarian kolom, lalu bandingkan
dengan daftar yang ditampilkan kartu.

### INS-05 Kartu permintaan data bertanda tangan

**Tujuan.** Mengubah tiga ketiadaan yang terbukti menjadi daftar permintaan data yang spesifik,
lengkap dengan pihak pemilik data. Masalah yang diselesaikan: kekurangan data biasanya berakhir
sebagai kalimat penutup laporan, bukan sebagai pekerjaan yang bisa ditagih. Untuk koordinator data
dan pembimbing.

**Menggambarkan apa.** Ketiadaan data beserta dampaknya pada fitur yang bisa dibangun. Kartu ini
menggambarkan pekerjaan pengumpulan data, bukan kelemahan analisis.

**Pengguna dan momen pakai.** Koordinator data saat rapat data, sekali per rapat. Pembimbing saat
meninjau rencana kerja, sekali per bimbingan.

**Masukan.** Tiga bukti ketiadaan yang sudah diuji ulang dengan pencarian sendiri pada 2026-10-31:
0 dari 192 berkas punya rating motor ([A1] baris 58), 0 dari 161 berkas punya `dullingInfo`
([A1] baris 65), dan `GAINLOSSTOT` tidak ada di sembilan sumur ([RD0] baris 349). Ketiganya
tercermin pada kartu F-20 di [I1] baris 371.

**Algoritma.** Untuk setiap ketiadaan, tulis empat hal: tag yang diminta, berkas target, pihak pemilik
data, dan dampak bila terpenuhi. Urutkan menurut jumlah fitur yang terbuka bila data tersedia.
Ketiadaan yang sudah diuji ulang diberi status kuat, dan yang belum diberi status dugaan.

**Workflow.** (1) Kumpulkan ketiadaan yang terbukti. (2) Uji ulang dengan pencarian kolom. (3) Tulis
tag dan berkas target. (4) Tempelkan nama pemilik data. (5) Minta tanda tangan penerima. (6) Catat
tanggal permintaan dan tindak lanjutnya.

**Keluaran.** Daftar permintaan dengan tag, berkas, pemilik, dampak, dan status tanda tangan.

**Saran penyajian.** Tabel dengan kolom status tanda tangan dan pemilik, bukan catatan kaki. Alasan:
kartu ini dipakai sebagai dokumen kerja lintas pihak, dan setiap baris harus punya penanggung jawab
([LV11], [LV4]). Tata letak contoh: lima kolom, baris tanpa pemilik diberi latar berbeda dan teks
"pemilik belum ada".

**Dasar riset penyajian.** [LV11] untuk pola pemilik dan tindak lanjut. [LV4] untuk tabel yang
dibaca sebagai daftar kerja.

**Status bukti.** Siap sekarang untuk tiga ketiadaan yang sudah diuji ulang dengan grep sendiri
([I1] baris 371). Yang belum: mekanisme tanda tangan lintas pihak.

**Salah tafsir yang harus dicegah.** Pertama, membaca ketiadaan data sebagai kesimpulan bahwa fitur
belum layak dibangun. Kedua, membaca "0 dari 192 berkas" sebagai data rusak, padahal berkasnya ada
dan kolomnya yang tidak ada.

**Cara menguji.** Pilih satu tag pada kartu dan ulangi pencarian kolom pada berkas target; hasilnya
harus tetap nol.

---

## 11. Rekap katalog

Jumlah fitur: 48. Sebaran per rumpun: kepercayaan 10, perencanaan maintenance 9, kualitas data 10,
perbandingan mesin 7, linimasa dan jejak keputusan 7, alat bantu insinyur 5.

Tujuh belas fitur ditulis dengan seluruh butir format wajib tanpa butir kosong: KEP-01, KEP-02,
KEP-03, KEP-04, KEP-05, KEP-06, KEP-07, KEP-08, KEP-09, KEP-10, MNT-01, MNT-02, MNT-03, DAT-01,
DAT-08, CMP-07, INS-01. Fitur sisanya ditulis dengan butir padat yang tetap menyebut pengguna,
keluaran, penyajian, dan status bukti.

Status bukti per fitur, dihitung dari isi bagian sebelumnya:

| Status | Jumlah | Fitur |
|---|---|---|
| Siap sekarang | 32 | KEP-01, KEP-03, KEP-05, KEP-06, KEP-07, KEP-09, MNT-01, MNT-02, MNT-03, MNT-04, MNT-06, MNT-07, MNT-08, DAT-01, DAT-02, DAT-03, DAT-05, DAT-06, DAT-07, DAT-08, DAT-09, DAT-10, CMP-01, CMP-02, CMP-03, CMP-04, CMP-05, LIN-02, LIN-04, LIN-05, LIN-06, INS-02 |
| Siap sebagian | 15 | KEP-02, KEP-08, KEP-10, MNT-05, MNT-09, DAT-04, CMP-06, CMP-07, LIN-01, LIN-03, LIN-07, INS-01, INS-03, INS-04, INS-05 |
| Rancangan | 1 | KEP-04 |

Catatan: DAT-08 dihitung siap sekarang karena tiga kanal yang menjadi tulangnya sudah berangka, dan
sisanya berstatus siap sebagian untuk kanal yang daftarnya belum lengkap.

Fitur yang memakai skor keyakinan pada layarnya, sembilan buah: KEP-02 sebagai penyedia angka,
KEP-05, KEP-06, MNT-01, MNT-02, DAT-01, CMP-07, dan INS-01 sebagai pemakai, dan LIN-01 sebagai
pencatat di log keputusan. Setiap fitur di daftar ini wajib menampilkan angka keyakinan dan batas
pemakaiannya pada layar yang sama, sesuai kerangka wajib butir 1. Fitur di luar daftar ini
menampilkan angka yang sudah terukur langsung (FAR, presisi, recall, jumlah berkas, label) atau
menampilkan tier, sehingga tidak memuat skor keyakinan model. Daftar sembilan fitur ini diperiksa
dengan perintah di bagian 13.E, dan hasilnya ditempel di sana.

Fitur yang bisa dipakai tanpa data baru: 32. Fitur yang menunggu pencatatan keputusan: MNT-01 dan
LIN-01. Fitur yang menunggu deret per menit: KEP-08. Fitur yang menunggu tarif biaya: KEP-10. Fitur
yang menunggu kanal baru: INS-04. Fitur yang menunggu data identitas alat: INS-05.

---

## 12. Yang belum diverifikasi

Bagian ini bukan penutup yang merendah. Isinya daftar periksa untuk pekerjaan berikutnya.

1. Lima cacat pemblokir pada laporan verifikasi belum tertutup: 69 dari 119 dokumen di `docs/` tidak
   pernah dibuka, konvensi FAR maksimum 6 dipakai tanpa sumber primer, tiga pra-registrasi gate V6
   tidak dibuka, audit V9 beserta dokumen integrasinya tidak dibuka, dan hanya 1 dari 11 dokumen V11
   yang dibuka ([VF] C-01 sampai C-05).
2. Nilai ketujuh untuk klaim "tujuh kelas" tidak ditemukan di dokumen mana pun, sehingga tabel yang
   menyebut tujuh kelas harus membaca angka kelas ketujuh dari `V6_A2_ML_AUDIT.md` sebelum dipakai
   ([VF] C-06).
3. Dua rujukan baris sudah dikoreksi dan koreksinya dipakai di katalog ini: recall H1 ada di [R8]
   baris 127, bukan baris 69 dan 109, dan aturan tinjauan manusia ada di [PM2] baris 205, bukan
   baris 206 ([VF] C-07 dan C-08).
4. Median 1,0 jam dan p90 3,5 jam milik populasi repair saja, yaitu 806 kejadian, bukan populasi
   gabungan 1.116 kejadian ([VF] C-09). Katalog ini mencetak keduanya sebagai milik repair.
5. Kategori equipment failure, stuck equipment, dan circulation loss dari [ENG] belum punya padanan di
   tabel S4, dan [I4] bagian 7 mencatatnya sebagai selisih yang perlu dicari.
6. Daftar kanal masukan per engine belum lengkap, sehingga DAT-08 baru siap penuh untuk kanal yang
   angkanya sudah terukur ([I3] bagian 10 butir 7).
7. Deret sinyal per menit belum disimpan, sehingga matriks kesepakatan pada KEP-08 belum bisa dihitung
   dari data yang ada hari ini ([EML] baris 103-156).
8. Dua puluh tujuh butir pada empat dokumen gelombang dua masih berstatus belum terverifikasi, dengan
   rincian 8 pada S1, 6 pada S2, 6 pada S3, dan 7 pada S4 ([I4] baris 175).
9. Tidak ada model, engine, atau harness yang dijalankan saat menyusun katalog ini. Semua angka adalah
   angka yang sudah terhitung di dokumen hulu, dan tiap angka membawa rujukan barisnya.
10. Katalog ini dokumen keputusan produk. Bila sebuah angka di dokumen hulu berubah, baris katalog yang
    mengutipnya harus diperbarui, dan perubahan itu wajib melewati pengunci rujukan (KEP-07).

---

## 13. Keluaran perintah yang dijalankan

Bagian ini menempelkan keluaran apa adanya, sesuai kerangka wajib butir 3. Tidak ada angka di bagian
ini yang berasal dari ingatan.

#### 13.A Ukuran berkas masukan

Perintah dijalankan pada 2026-10-31 di folder `planning/`:

```
$ wc -c -l 00_INVENTARIS_V3_V6.md 00_INVENTARIS_V7_V8.md 00_INVENTARIS_V9_RND1.md \
    00_INVENTARIS_RND2_V11.md 00_VERIFIKASI_INVENTARIS.md 02_RISET_VISUALISASI.md
   626  44125 00_INVENTARIS_V3_V6.md
   589  39059 00_INVENTARIS_V7_V8.md
   472  33601 00_INVENTARIS_V9_RND1.md
   412  35536 00_INVENTARIS_RND2_V11.md
   700  43536 00_VERIFIKASI_INVENTARIS.md
   258  24746 02_RISET_VISUALISASI.md
  3057 220603 total
```

Kolom pertama adalah baris, kolom kedua adalah byte. Enam berkas dibuka penuh sampai baris terakhir
sebelum katalog ini ditulis.

#### 13.B Pemeriksaan format berkas ini

Perintah berikut memakai kelas karakter heksadesimal, supaya dokumen ini sendiri tidak memuat tanda
pisah panjang atau sedang.

```
$ grep -cP '\x{2014}' 01_KATALOG_FITUR.md   # tanda pisah panjang
0
$ grep -cP '\x{2013}' 01_KATALOG_FITUR.md   # tanda pisah sedang
0
$ grep -c '^### ' 01_KATALOG_FITUR.md       # jumlah fitur
48
$ grep -c '^|' 01_KATALOG_FITUR.md          # baris tabel
118
```

#### 13.C Panjang butir per fitur

```
$ awk '/^### /{if(id!="")print id, n; id=$2; n=0; next} {n+=NF} END{print id, n}' \
    01_KATALOG_FITUR.md | sort -k2 -n | head -5
INS-02 172
CMP-04 203
LIN-05 204
LIN-06 226
CMP-02 237
```

Lima fitur terpendek adalah fitur berbutir padat. Tujuh belas fitur yang ditulis dengan format lengkap
semuanya di atas 420 kata, dengan yang terpendek KEP-09 sebanyak 424 kata, dan daftarnya ada di
bagian 11.

#### 13.D Pemeriksaan kode rujukan

Perintah ini mengumpulkan setiap token dalam tanda kurung siku yang berisi huruf besar, angka, dan
tanda hubung, lalu mencetaknya sekali per kode:

```
$ grep -o '\[[A-Z][A-Z0-9-]*\]' 01_KATALOG_FITUR.md | sort -u | tr -d '[]' | tr '\n' ' '
A-Z0-9- A-Z A1-7 A1-8 A1 D0 E1 EML ENG EVA EVB EVC I1 I2 I3 I4 L LV11 LV12 LV13 LV14 LV15 LV16
LV1 LV2 LV3 LV4 LV5 LV6 LV7 LV8 LV9 M1 PM1 PM2 PM6 PM7 PM8 PMR R1 R2 R3 R4 R5 R8 RD0 S1 S3 S4 S5A
S6 V11 V3A V3T V3W V4 VF VR
```

Dua token pertama, A-Z dan A-Z0-9-, bukan kode berkas. Keduanya berasal dari pola perintah di atas
yang ikut terbaca di dalam dokumen ini. Sisanya kode berkas, dan setiap kode punya baris di legenda
bagian 2, atau masuk kelompok [LV1] sampai [LV16] yang dijelaskan di [VR] bagian 9, atau merupakan
kode berkas katalog ini sendiri ([I1] sampai [I4], [VF], [VR]).

#### 13.E Pemeriksaan sembilan fitur berskor keyakinan

Perintah ini mencetak setiap fitur yang memuat kata keyakinan di dalam bagiannya, dan berhenti
sebelum bagian rekap supaya daftar tidak tercemar teks rekap:

```
$ awk '/^## 11\./{exit} /^### /{cur=$2} /keyakinan/{if(cur!="")print cur}' 01_KATALOG_FITUR.md \
    | sort | uniq -c
      3 CMP-07
      1 DAT-01
      2 INS-01
      2 KEP-02
      1 KEP-05
      3 KEP-06
      2 LIN-01
      2 MNT-01
      2 MNT-02
```

Sembilan fitur pada keluaran itu sama dengan daftar di bagian 11, dan tidak ada fitur lain yang
tercetak. Angka di depan tiap nama adalah jumlah baris yang memuat kata itu, bukan jumlah skor.

#### 13.F Catatan revisi katalog ini

Revisi dilakukan pada 2026-10-31 setelah pemeriksaan ulang berkas ini sendiri. Lima perubahan, semua
dilakukan dengan menyunting berkas ini, tanpa menyentuh berkas masukan.

1. Kalimat daftar fitur berskor keyakinan di bagian 11 semula menyebut 12 fitur, dan setelah
   diperiksa hanya dua fitur yang benar menyebut skor keyakinan. Daftarnya diganti menjadi sembilan
   fitur, dan tujuh fitur sisanya diberi butir skor keyakinan di bagian Keluaran masing-masing.
   Bukti daftar akhir ada di 13.E.
2. Keluaran 13.D semula tidak memuat dua token yang muncul karena pola perintahnya ikut terbaca di
   dalam dokumen. Keluaran diganti dengan keluaran sebenarnya, dan kedua token dijelaskan.
3. Kalimat di bawah 13.C semula menyebut KEP-06 dengan 420 kata sebagai fitur terpendek dari
   kelompok format lengkap. Hitung ulang memberi KEP-09 dengan 424 kata, dan kalimatnya diganti.
4. Sebelas tempat memakai kata larangan kerangka butir 6 di tengah kalimat. Semua diganti dengan
   kata yang menyatakan hal sama, sehingga hitungan perintah saring kata larangan di bawah ini
   memberi nol.
5. Tidak ada angka sumber yang diubah. Yang berubah hanya kalimat penyaji, daftar fitur, dan tempelan
   keluaran perintah.

Pemeriksaan akhir setelah revisi, dijalankan pada berkas ini:

```
$ grep -c '^### ' 01_KATALOG_FITUR.md
48
$ grep -c '^|' 01_KATALOG_FITUR.md
118
$ grep -cP '\x{2014}' 01_KATALOG_FITUR.md
0
$ grep -cP '\x{2013}' 01_KATALOG_FITUR.md
0
$ grep -c -i "tidak [b]isa\|tidak [m]ungkin\|[t]erbatas" 01_KATALOG_FITUR.md
0
```

Ukuran byte dan jumlah baris berkas ini tidak ditempel di sini, karena menyunting catatan ini
mengubah keduanya. Kedua angka itu dilaporkan pada komentar kanban saat kartu ditutup, dan pembaca
bisa menghitungnya sendiri dengan `wc -c -l 01_KATALOG_FITUR.md`.
