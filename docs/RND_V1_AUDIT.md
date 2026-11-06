# RND-V1: AUDIT PROVENANCE DAN RESOLUSI SITASI

Kartu: `t_3a2b1d40` · Board: `rnd-algo-2026` · Tanggal: 2026-10-27 (WIB)
Workspace: `/mnt/d/Capstone 1(v2)` · Keluaran: `docs/RND_V1_AUDIT.md`
Peran: auditor. Dokumen orang lain TIDAK diubah. Semua temuan ditulis di sini.

## 0. Riset pendahuluan

Riset pendahuluan: verification-mandatory, grounded-citations, dynamic-page-fetch, research-lookup.

- **verification-mandatory**: dipakai sebagai prosedur uji DOI dua lapis, yaitu lapis registrasi (`doi.org`, redirect dimatikan) dan lapis metadata (Crossref), dengan lapis akses penerbit dipisah supaya 403/202 tidak salah dibaca sebagai DOI palsu.
- **grounded-citations**: dipakai untuk memastikan setiap klaim dalam dokumen audit ini menempel pada sumber yang benar-benar diambil, bukan pada ingatan, sehingga tabel pelanggaran memuat path berkas atau status HTTP, bukan kalimat tanpa asal.
- **dynamic-page-fetch**: dipakai untuk membedakan halaman yang benar-benar terbuka dari halaman yang hanya mengembalikan cangkang JavaScript atau blokir bot, sehingga status 200/403/202 dicatat sebagai kondisi akses, bukan sebagai bukti isi terbaca.
- **research-lookup**: dipakai sebagai rujukan prosedur pemeriksaan metadata bibliografis (penulis pertama, tahun, judul, wadah terbit) supaya kecocokan identitas DOI diuji dengan field yang sama untuk semua rujukan.

Riset pendahuluan: sequentialthinking, 5 pikiran (`mcp__sequentialthinking__sequentialthinking`, thoughtNumber 1..5, thoughtHistoryLength 5). Jumlah pikiran: **5**.
Ringkas: (1) memisahkan tiga kategori pelanggaran, yaitu angka tanpa baris ledger, rujukan gagal dibuka, dan klaim komparatif tanpa pembanding; (2) menetapkan uji DOI dua lapis dan melarang pencampuran lapis akses penerbit; (3) menetapkan metode cakupan angka yang bisa diukur, yaitu normalisasi numerik dengan toleransi pembulatan, bukan pencocokan string; (4) menetapkan penanda angka karangan yang bisa diperiksa, yaitu angka bulat tanpa sumber, rujukan tanpa DOI, dan klaim menang tanpa baseline; (5) menetapkan bahwa normalisasi agresif berisiko menenggelamkan temuan nyata, sehingga daftar pendek hasil pemeriksaan manual wajib ikut dilaporkan.

## 1. Ruang lingkup dan metode

### 1.1 Yang diaudit

| # | Dokumen | Baris | DOI unik | URL unik |
|---|---|---|---|---|
| 1 | `docs/RND_D0_DATA_FEASIBILITY.md` | 402 | 8 | 8 |
| 2 | `docs/RND_E0_AUDIT_ENGINE.md` | 523 | 6 | 1 |
| 3 | `docs/RND_E1_MATRIKS.md` | 495 | 8 | 5 |
| 4 | `docs/RND_E2_PROTOKOL.md` | 567 | 17 | 4 |
| 5 | `docs/RND_P0_PARAMETER.md` | 213 | 1 | 0 |
| 6 | `docs/RND_R1_METAHEURISTIK.md` | 585 | 58 | 0 |
| 7 | `docs/RND_R2_STOKASTIK.md` | 408 | 29 | 0 |
| 8 | `docs/RND_R3_VMD_SVM.md` | 282 | 21 | 0 |
| 9 | `docs/RND_R4_BOOSTING.md` | 317 | 8 | 4 |
| 10 | `docs/RND_R5_DRIFT.md` | 352 | 11 | 2 |
| 11 | `docs/RND_R6_METRIK.md` | 296 | 10 | 0 |

Pembanding: `docs/RND_PROVENANCE_LEDGER.md` (1.586 baris sebelum bagian V1 ditulis dan 1.620 sesudahnya, 1.395 baris ledger ber-ID, 1.185 nilai numerik unik setelah normalisasi). Aturan: `docs/RND_ALGO_RESEARCH_PLAN.md` §2. `RND_ALGO_RESEARCH_PLAN.md` sendiri tidak diaudit sebagai dokumen bukti karena isinya aturan, bukan klaim.

### 1.2 Alat ukur

Skrip di `/home/neonti/.hermes/cache/scratch/rnd_v1/`: `extract.py` (ekstraksi DOI dan URL), `verify.py` (uji HTTP dua lapis), `numcov.py` (cakupan angka), `classify.py` (pemisahan token struktural), `probe.py` (uji keberadaan angka di ledger), `claims.py` (pemindaian klaim komparatif), `doistat.py` (rekap per dokumen). Keluaran mentah: `v1_extract.json`, `v1_verify.json`, `v1_number_cov.json`, `claims.json`.

### 1.3 Batas metode yang harus dibaca sebelum angka di bawah dipakai

1. Cakupan angka diukur dengan mencocokkan **nilai numerik** token dokumen ke **semua** nilai yang muncul di ledger, tanpa memeriksa apakah baris ledger yang cocok itu memang milik dokumen tersebut. Artinya cakupan di §3 adalah **batas atas optimistis**, bukan bukti bahwa baris ledger yang tepat menaungi angka itu.
2. Token struktural (nomor halaman rujukan, nomor baris kode seperti `.py:578`, nomor bagian, tahun) tidak boleh dihitung sebagai klaim data. Pemisahan dilakukan otomatis lalu diperiksa manual; 58 dari 109 token yang tidak cocok masuk kelas struktural.
3. Teks penuh rujukan tidak dibaca. Verifikasi berhenti pada lapis registrasi dan lapis metadata, sesuai batas yang sama dengan yang dipakai dokumen RND sendiri.
4. Uji dua lapis **tidak bisa** mendeteksi DOI yang terdaftar tetapi menunjuk makalah lain. Kelas kesalahan itu diuji terpisah dengan membandingkan judul dan penulis pertama Crossref terhadap label di dokumen.

## 2. Hasil uji DOI dan URL

### 2.1 Rekap per dokumen (dua lapis)

| Dokumen | DOI unik | doi.org 3xx | Crossref 200 | Gagal |
|---|---|---|---|---|
| D0 | 8 | 8 | 8 | 0 |
| E0 | 6 | 5 | 5 | 1 |
| E1 | 8 | 8 | 8 | 0 |
| E2 | 17 | 16 | 16 | 1 |
| P0 | 1 | 1 | 1 | 0 |
| R1 | 58 | 58 | 58 | 0 |
| R2 | 29 | 29 | 29 | 0 |
| R3 | 21 | 21 | 21 | 0 |
| R4 | 8 | 8 | 8 | 0 |
| R5 | 11 | 11 | 11 | 0 |
| R6 | 10 | 9 | 9 | 1 |

Total: 143 DOI unik, 177 kemunculan lintas dokumen. 174 dari 177 kemunculan lolos dua lapis. Tiga kemunculan gagal dan itu berasal dari **dua** DOI, yaitu `10.1109/TII.2019.2950661` (E0) dan `10.2307/4615733` (E2 dan R6). Tidak ada satu pun DOI yang lolos registrasi tetapi gagal metadata.

### 2.2 Dua DOI yang gagal, dan statusnya di dokumen

| DOI | doi.org | Crossref | Dipakai di | Status di dokumen |
|---|---|---|---|---|
| `10.1109/TII.2019.2950661` | 404 | 404 | `RND_E0_AUDIT_ENGINE.md:415` | sudah ditolak eksplisit ("Crossref 404, tidak ada"), tidak dipakai |
| `10.2307/4615733` (Holm 1979) | 404 | 404 | `RND_E2_PROTOKOL.md:536`, `RND_R6_METRIK.md:261` dan `:293` | sudah ditandai BELUM TERVERIFIKASI, dan R6 menyatakan koreksi Holm tidak disandarkan pada rujukan itu |

Kesimpulan yang benar untuk dua DOI ini: **tidak ada rekomendasi yang perlu dicabut**, karena keduanya sudah ditandai gagal oleh dokumen sumber dan tidak dipakai sebagai dasar rekomendasi. Yang perlu dicabut adalah pemakaiannya sebagai sandaran, dan itu sudah tidak ada.

### 2.3 Lapis akses penerbit (dipisah, bukan kegagalan DOI)

17 URL diuji dengan GET. Hasil: 11 status 200, 3 status 403, 3 status 202.
- 403: `10.1093/biomet/41.1-2.100` (Page 1954), `10.1098/rspa.1998.0193`, `10.1111/j.2517-6161.1972.tb00899.x` (Cox 1972).
- 202: `10.1109/5.18626` (Rabiner 1989), `10.1109/ICDM.2008.17` (Liu 2008), `10.1109/TSP.2013.2288675` (Dragomiretskiy 2014).

Ketiga 403 dan ketiga 202 terjadi **setelah** `doi.org` mengarahkan ke penerbit, sehingga statusnya adalah blokir bot, bukan DOI tidak terdaftar. R5 sudah menulis batas ini (`RND_R5_DRIFT.md:310` dan `:346`).

### 2.4 Kelas kesalahan yang tidak tertangkap uji dua lapis

Uji dua lapis memberi 21 dari 21 lolos untuk R3, tetapi dua di antaranya menunjuk makalah lain. R3 sudah menemukan dan mencatat sendiri: `10.1007/978-3-540-30075-5_46` dilabeli Ratanamahatana dan Keogh, padahal Crossref memberi Bellatreche 2004, sedangkan `10.1098/rsta.2010.0331` dilabeli Randall dan Antoni, padahal Crossref memberi Ellis 2011 (`RND_R3_VMD_SVM.md:140`). E1 membuang `10.1214/18-AOS1801` karena menunjuk Chen 2020 tentang SGD (`RND_E1_MATRIKS.md:433`), dan R4 membuang dua DOI Zadrozny dan Elkan 2002 karena keduanya menunjuk makalah lain (`RND_R4_BOOSTING.md:280`).

Empat pembuangan rujukan itu mencakup lima DOI yang menunjuk makalah lain (dua di R3, satu di E1, dua di R4). Itu adalah bukti bahwa tim sudah melakukan pemeriksaan lapis ketiga (identitas bibliografis), dan itulah satu-satunya cara kelas kesalahan ini tertangkap.

## 3. Cakupan angka terhadap ledger

| Dokumen | Token angka data | Cocok | Tidak cocok | Cakupan mentah |
|---|---|---|---|---|
| D0 | 836 | 832 | 4 | 99,52% |
| E0 | 440 | 387 | 53 | 87,95% |
| E1 | 181 | 181 | 0 | 100,00% |
| E2 | 257 | 245 | 12 | 95,33% |
| P0 | 147 | 141 | 6 | 95,92% |
| R1 | 215 | 213 | 2 | 99,07% |
| R2 | 147 | 134 | 13 | 91,16% |
| R3 | 250 | 243 | 7 | 97,20% |
| R4 | 134 | 133 | 1 | 99,25% |
| R5 | 292 | 287 | 5 | 98,29% |
| R6 | 328 | 322 | 6 | 98,17% |
| **Total** | **3.227** | **3.118** | **109** | **96,62%** |

Dari 109 token yang tidak cocok: 58 adalah token struktural (nomor halaman rujukan, nomor baris kode, nomor standar seperti EEMUA 191), dan 51 adalah kandidat angka data. Setelah pemeriksaan manual, 51 kandidat itu menyusut menjadi **12 temuan nyata** yang tercatat di §4, sisanya adalah pengulangan token pada baris yang sama atau angka desain yang memang bukan hasil ukur.

## 4. Tabel pelanggaran

Kolom tindakan mengikuti tiga nilai: **perbaiki** (angka benar, provenance kurang), **cabut** (angka tidak dapat dipertanggungjawabkan), **lolos** (diperiksa, tidak ada masalah).

| No | Dokumen dan baris | Angka | Masalah | Tindakan |
|---|---|---|---|---|
| V1-01 | `RND_E0_AUDIT_ENGINE.md:303-307` | 92.501; 3.018; 322.772; 1.173; 369.665; 11.668; 7.354; 5.289; 369.549; 11.249 | penyebut menit per well dan rentang kalender tidak punya baris ledger; E0-014 dan E0-015 hanya memuat rasio cakupan dan menit negatif | perbaiki: tambah baris ledger E0 untuk `cakupan_waktu_per_well` |
| V1-02 | `RND_E0_AUDIT_ENGINE.md:303-307` | 308,2; 588,3; 908,2; 59,1; 755,6 | jam negatif diturunkan dari menit negatif, tetapi angkanya tidak muncul di ledger mana pun (diuji dengan `probe.py`: 0 baris) | perbaiki: tambah baris DERIVASI dengan rumus menit/60 |
| V1-03 | `RND_E0_AUDIT_ENGINE.md:111-112,221` | 1.056; 436; 267 | FP persistence shk, stuck K-i, dan ssi tidak dinaungi baris ledger: 1.056 dan 436 tidak muncul sebagai nilai mana pun, sedangkan 267 hanya muncul sebagai baris D0-683 (positif shk F-7), bukan sebagai FP persistence ssi. E0-013 hanya memuat FP vib 1.456 dan hyd 1.941 | perbaiki: lengkapi E0-013 atau tambah baris baru |
| V1-04 | `RND_E0_AUDIT_ENGINE.md:126` | 268 onset | jumlah onset stuck_k2 tidak ada di ledger (uji `probe.py`: hanya cocok dengan ID baris D0-268, bukan nilai) | perbaiki: tambah baris RUN-KITA ke `e0_audit_results2.json` |
| V1-05 | `RND_R3_VMD_SVM.md:148-150` | 2.941; 5.941; 11.941; 3.000; 6.000; 12.000 | jumlah query matrix profile dan panjang seri tidak ada di ledger; R3-xx hanya mencatat biaya per query | perbaiki: tambah baris dari `m4_matrix_profile.json` |
| V1-06 | `RND_R3_VMD_SVM.md:45,209` | 97 | batas atas jendela 1024 utuh per kanal tidak ada di ledger | perbaiki: tambah baris RUN-KITA |
| V1-07 | `RND_R5_DRIFT.md:104-107` | 504; 418; 171; 97 | panjang blok kontigu terpanjang per well tidak ada di ledger | perbaiki: tambah baris dari `drift_far_measured.json` |
| V1-08 | `RND_R5_DRIFT.md:88` | 600 menit | ambang baseline 600 menit adalah konvensi, tetapi tidak ada baris KONVENSI untuk angka ini | perbaiki: tandai KONVENSI dan sebut dokumen penetapnya, atau ubah menjadi BELUM TERUKUR |
| V1-09 | `RND_R1_METAHEURISTIK.md:127` | 55.000 | angka bulat retoris ("9, bukan 55.000") tanpa sumber; jumlah baris sebenarnya 52.509 dan 56.495 yang justru sudah ber-ledger | cabut: ganti dengan dua angka ber-ledger atau hapus klausa itu |
| V1-10 | `RND_R1_METAHEURISTIK.md:117` | 2.700 | turunan 300 x 9 ditulis tanpa baris ledger meski rumusnya terlihat | perbaiki: tambah satu baris DERIVASI |
| V1-11 | `RND_R2_STOKASTIK.md:290` | 212 | angka pembanding "B3 EVAL_B -212x" tidak punya baris ledger dan tidak menyebut path sumber | perbaiki: tambah rujukan `V9_EVAL_B` barisnya, atau tandai BELUM TERVERIFIKASI |
| V1-12 | `RND_P0_PARAMETER.md:160` | 386,089 in/s² | nilai kutipan ISO 2041 turunan inci tidak punya baris ledger; L-01 hanya menaungi 32,17405 ft/s² | perbaiki: tambah baris turunan atau hapus angka inci |
| V1-13 | `RND_P0_PARAMETER.md:165` | 0,67449 lawan 0,6745 | dua jumlah digit berbeda untuk konstanta yang sama di dalam satu dokumen | perbaiki: seragamkan penulisan |
| V1-14 | `RND_E0_AUDIT_ENGINE.md:415`, `RND_E2_PROTOKOL.md:536`, `RND_R6_METRIK.md:261,293` | DOI 404 | dua DOI gagal dibuka, tetapi sudah ditandai gagal dan tidak dipakai sebagai dasar rekomendasi | lolos |

### 4.1 Klaim komparatif tanpa pembanding

Pemindaian frasa ("lebih baik", "unggul", "menang", "terbaik", "superior") menemukan 74 baris di 9 dokumen (D0 dan P0 tidak memuat frasa itu dalam konteks komparatif). Setelah pemeriksaan manual baris per baris, **tidak ada** klaim "algoritma X lebih baik" yang berdiri tanpa pembanding. Contoh yang benar dan bisa diperiksa:
- `RND_R4_BOOSTING.md:24` menulis eksplisit bahwa keluarga boosting "belum boleh diklaim lebih baik" dan menyebut satu-satunya angka terukur (RF AUPRC 0,9117).
- `RND_R3_VMD_SVM.md:85` menetapkan syarat bahwa dekomposisi harus mengalahkan statistik jendela polos pada metrik yang sama.
- `RND_R1_METAHEURISTIK.md:107` menyatakan bahwa random search bukan klaim lebih baik, melainkan syarat kontrol.

Satu catatan kecil: tabel ringkas `RND_R1_METAHEURISTIK.md:501-514` dan `RND_R5_DRIFT.md:57-61,220-224` menyebut penulis dan tahun tanpa DOI di baris itu. DOI-nya ada di subbagian dan di daftar rujukan dokumen yang sama, sehingga bukan rujukan tanpa DOI, tetapi pembaca tabel ringkas harus melacak dua tempat.

### 4.2 Angka bulat mencurigakan yang diperiksa dan dinyatakan wajar

| Angka | Lokasi | Alasan wajar |
|---|---|---|
| 300 evaluasi | `RND_R1_METAHEURISTIK.md:117` | konvensi anggaran desain, ditulis sebagai batas, bukan hasil ukur |
| 240 menit | `RND_R5_DRIFT.md:57` | konvensi baseline kontigu, sudah disebut sebagai konvensi kami |
| 6 per 24 jam | plan §6, dipakai di E2 dan R4 | KONVENSI V9, ada baris L-xx di ledger |
| 1 alarm per menit | plan §6 | KONVENSI bengkel, disebut sebagai gate |
| 0,95 atau 95% | banyak tempat sebagai level CI | parameter desain, bukan pengukuran |

## 5. Yang belum terverifikasi

1. **Teks penuh rujukan tidak dibaca.** 6 URL mengembalikan 403 atau 202, dan 11 dari 17 hanya terbuka pada lapis metadata. Klaim tentang isi metode tetap bersandar pada judul dan abstrak.
2. **Kelas DOI salah label tidak diuji menyeluruh.** Lima DOI ditemukan oleh dokumen sendiri menunjuk makalah lain (dua di R3, satu di E1, dua kandidat di R4), dan itu terjadi pada 4 rujukan. Sisa 138 DOI tidak dibandingkan judul Crossref terhadap label dokumen satu per satu pada audit ini, jadi statusnya "tidak diuji", bukan "bersih".
3. **Cakupan angka adalah batas atas.** Pencocokan berbasis nilai bisa lolos karena kebetulan sama dengan baris ledger dokumen lain. Pemeriksaan kelas sumber per baris tidak dilakukan menyeluruh.
4. **12 temuan §4 adalah hasil pemeriksaan manual atas 51 kandidat.** Kandidat yang saya nyatakan wajar bisa saja masih salah kelas sumber; yang saya ukur adalah keberadaan barisnya, bukan kesesuaian kelasnya.
5. **Nomor baris kode tidak diaudit ulang.** 58 token struktural jenis ini tidak diverifikasi terhadap isi berkas kode pada audit ini.
6. **Klaim kebutuhan bisnis tidak diuji.** Angka seperti "biaya pemeriksaan manusia" dan "beban per shift" tidak punya sumber di ledger dan tidak saya nyatakan salah karena memang belum diukur siapa pun.
7. **Dua DOI gagal** (`10.1109/TII.2019.2950661`, `10.2307/4615733`) tetap BELUM TERVERIFIKASI. Keduanya tidak boleh dipakai sebagai dasar rekomendasi.

## 6. Rekomendasi tindakan (berbasis bukti, urut prioritas)

1. **Tambah baris ledger untuk 9 kelompok angka di V1-01 sampai V1-08, V1-10 sampai V1-13.** Semua angkanya berasal dari berkas JSON yang sudah ada, jadi pekerjaannya menambah provenance, bukan mengukur ulang. Tanpa ini, dokumen E0, R3, dan R5 tetap punya angka tanpa baris.
2. **Cabut klausa "bukan 55.000" di R1 §5 butir 1** dan ganti dengan dua angka yang sudah ber-ledger.
3. **Tandai seluruh angka kutipan standar sebagai turunan** (`386,089 in/s²` di P0) supaya tidak tampak seperti hasil ukur.
4. **Jangan mencabut rekomendasi apa pun karena DOI.** Dari 143 DOI unik, 141 lolos dua lapis, dan 2 yang gagal sudah ditandai serta tidak dipakai.
5. **Uji kelas salah label untuk sisa DOI** sebelum PM memvonis, karena uji dua lapis tidak menangkapnya dan empat kasus sudah terbukti ada di repo ini.

## 7. Ringkasan 5 baris

1. Dari 143 DOI unik di 11 dokumen RND, 141 lolos uji dua lapis dan 2 gagal, yaitu `10.1109/TII.2019.2950661` dan `10.2307/4615733`, keduanya sudah ditandai gagal di dokumen sumber dan tidak dipakai sebagai dasar rekomendasi.
2. Lapis akses penerbit memberi 11 status 200, 3 status 403, dan 3 status 202 dari 17 URL, dan semuanya diperlakukan sebagai blokir bot, bukan kegagalan DOI.
3. Cakupan angka terhadap ledger adalah 3.118 dari 3.227 token (96,62%), dengan E0 terendah (87,95%) karena tabel cakupan waktu memuat penyebut dan jam negatif yang belum ditulis ke ledger.
4. Dua belas temuan nyata tercatat di tabel pelanggaran: sepuluh perlu perbaikan provenance, satu perlu dicabut (angka retoris 55.000 di R1), dan satu lolos karena sudah ditangani dokumen sumber.
5. Tidak ada klaim "algoritma X lebih baik" yang berdiri tanpa pembanding setelah 74 baris klaim komparatif diperiksa satu per satu.

## 8. Provenance angka pada dokumen ini

Setiap angka di atas berasal dari eksekusi yang tercatat, dengan sumber sebagai berikut (baris ledger lengkap ada di `docs/RND_PROVENANCE_LEDGER.md` bagian V1, ID `V1-01` sampai `V1-24`):

| Kelompok angka | Sumber persis |
|---|---|
| 143 DOI unik, 177 kemunculan, 174 lolos | `scratch/rnd_v1/v1_extract.json`, `v1_verify.json`, `doistat.py` |
| 17 URL dengan 11/3/3 status | `scratch/rnd_v1/v1_verify.json` kunci `url` |
| 3.227 token, 3.118 cocok, 109 tidak cocok | `scratch/rnd_v1/v1_number_cov.json`, `numcov.py` |
| 58 struktural dan 51 kandidat | `scratch/rnd_v1/classify.py` |
| 1.586 baris ledger, 1.395 baris ber-ID, 1.185 nilai unik | `grep -c '^| [A-Z]'` pada ledger, `v1_number_cov.json` kunci `ledger_rows_est_values` |
| 74 baris klaim komparatif | `scratch/rnd_v1/claims.json` |
| 9,52% sisa tidak cocok di E0 dan rincian per dokumen | `v1_number_cov.json` kunci `docs` |
