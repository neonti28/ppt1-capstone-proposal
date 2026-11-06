# RND-E4: ENGINEER MENJAWAB TEMUAN R&D (PERBAIKAN DAN RUN ULANG)

Kartu: `t_61edf756` · Board: `rnd-algo-2026` · Tanggal: 2026-10-27 (WIB)
Workspace: `/mnt/d/Capstone 1(v2)` · Arsip `/mnt/d/Capstone 1` tidak disentuh
Dokumen yang dijawab: `docs/RND_R7_REVIEW.md` (359 baris) dan `docs/RND_E0_AUDIT_ENGINE.md` (522 baris)
Kebijakan penilaian: `docs/RND_EVALUATION_POLICY.md` (tiga lapisan A/B/C, tanpa vonis biner)

Riset pendahuluan: systematic-debugging, scikit-learn, statistical-analysis, verification-mandatory

- **systematic-debugging** dipakai untuk menolak menambal gejala: setiap temuan R7 diuji akar masalahnya
  lebih dulu lewat satu loop yang bisa gagal, yaitu jalankan ulang pilot penuh dan bandingkan seluruh angka
  ringkasan dengan run sebelumnya, baru kode diperbaiki setelah penyebabnya terbukti di tingkat fungsi.
- **scikit-learn** dipakai untuk mengendalikan kebocoran fitur dan pemisahan data: kolom `ts_bin` dilarang
  masuk matriks fitur, `Pipeline` dan `ColumnTransformer` dipakai agar praproses hanya di-fit pada data latih
  tiap fold, dan `random_state` dipatok supaya hasil reproducible.
- **statistical-analysis** dipakai untuk memilih satuan dan pembanding yang sah: FAR dilaporkan pada satuan
  baris, kejadian, dan kalender berdampingan, median dilaporkan bersama jumlah fold yang lulus, dan sel
  dengan nol alarm ditandai degenerat, bukan dihitung sebagai keberhasilan.
- **verification-mandatory** dipakai sebagai gerbang akhir: setiap baris ledger di-assert terhadap path JSON,
  DOI diuji dua lapis, dan klaim yang tidak dapat dibuka ditandai BELUM TERVERIFIKASI, bukan dilunakkan.

Riset pendahuluan: sequentialthinking, 6 pikiran (`mcp__sequentialthinking__sequentialthinking`,
thoughtNumber 1..6, thoughtHistoryLength 6). Ringkas: (1) memetakan empat temuan wajib dan tiga instruksi,
(2) memeriksa bahwa perbaikan benar-benar ada di kode, bukan hanya di narasi, (3) membuktikan reproduksibilitas
dengan run ulang penuh, (4) menetapkan satuan metrik tunggal untuk gate, (5) menemukan bahwa syarat yang
mengikat gate bukan mutu deteksi melainkan cakupan data, dan (6) memisahkan usulan tier dari klaim kemampuan.

---

## 0. CARA MEMBACA DOKUMEN INI

Kebijakan evaluasi melarang vonis biner, jadi dokumen ini tidak menutup temuan dengan kalimat "gate gagal".
Setiap temuan dijawab dengan salah satu dari dua bentuk yang dapat diaudit:

1. **Diperbaiki**, disertai bagian kode yang berubah dan angka sesudah perbaikan.
2. **Ditolak dengan bukti run**, disertai angka yang membantah temuan.

Angka sebelum dan sesudah selalu memakai jumlah sampel yang sama. Perbandingan lintas jumlah sampel
(9 fold lawan 18 fold-run) dinyatakan eksplisit supaya tidak menyesatkan.

Kelas sumber angka mengikuti `docs/RND_ALGO_RESEARCH_PLAN.md` §2: `STANDAR` > `JURNAL` > `RUN-KITA` >
`KONVENSI` > `BELUM-TERUKUR`. Seluruh angka di dokumen ini punya baris di
`docs/RND_PROVENANCE_LEDGER.md` Bagian E4 (`E4-001` sampai `E4-058`).

---

## 1. RINGKASAN KEPUTUSAN

| Temuan | Tindakan | Status akhir |
|---|---|---|
| R7-1 pembanding memakai label baris sebelumnya yang menintip masa depan | Diperbaiki: baseline pindah ke `code/rnd_rule_baseline.py` yang hanya memakai anom bin (t-1) dari bins, ditambah assert FP | Tertutup, angka terbit reproducible |
| R7-2 `ts_bin` dipakai sebagai fitur | Diperbaiki: masuk `KOLOM_TERLARANG_FITUR`, ditambah `assert len(feats) == 40` | Tertutup |
| R7-3 satuan metrik A2 tidak sebanding | Diperbaiki: setiap detektor dilaporkan pada satuan baris dan kejadian berdampingan | Tertutup, dan cacat sejenis ditemukan lagi (§5.3) |
| R7-4 gate A tanpa syarat recall | Diperbaiki: `gate_A_lama_penuh` dan `gate_A_baru` memuat syarat recall | Tertutup, dengan bukti degenerat (§5) |
| R7-5 titik operasi dikunci syarat TP minimum | Diperbaiki: alpha diambil dari anggaran 1/240 tanpa syarat TP | Tertutup |
| R7-6 gate A memakai menit teramati | Diperbaiki: gate memakai FAR per 24 jam kalender ditambah syarat cakupan | Tertutup, dan mengubah diagnosis (§6) |
| R7 §9.3 audit label hyd belum dijalankan | Dijalankan pada ambang 2, 2,5, dan 3 (9 well) | Terukur, lihat §7 |

Tidak ada temuan yang ditutup tanpa perbaikan kode atau angka. Satu temuan tambahan ditemukan sendiri
saat verifikasi (§5.3) dan langsung diperbaiki.

---

## 2. DEFINISI YANG DIPAKAI (AGAR DAPAT DIAUDIT)

| Besaran | Definisi | Kelas sumber |
|---|---|---|
| FAR 24 jam baris | FP baris dibagi menit negatif teramati, dikali 24 jam | RUN-KITA |
| FAR 24 jam kejadian | FP kejadian dibagi menit negatif kalender, dikali 24 jam | RUN-KITA |
| FAR 24 jam kalender | FP baris dibagi menit negatif kalender, dikali 24 jam | RUN-KITA |
| Cakupan | baris teramati dibagi menit kalender pada satu well | RUN-KITA |
| Gate A lama | FAR 24 jam baris tidak lebih dari 6 | KONVENSI `V9_EVAL_C_LAYERC.md` EC-4 |
| Gate A lama penuh | FAR tidak lebih dari 6 dan recall tidak kurang dari 0,5 | KONVENSI `RND_R7_REVIEW.md` §6.4 |
| Gate A baru | FAR kalender tidak lebih dari 6 dan cakupan tidak kurang dari 0,50 dan recall tidak kurang dari 0,5 | KONVENSI `RND_E2_PROTOKOL.md` §4.1 (d) |
| Alpha anggaran | 1/240, setara FAR tidak lebih dari 6 per 24 jam | DERIVASI, `6/1440` |

Data: `scratch/v9_d1/` matriks 52.509 baris dan 50 kolom, 9 fold leave-one-well-out,
seed 42 dan 7. Waktu jalan pilot: 68,3 detik sampai 70,2 detik per run penuh.

---

## 3. BUKTI REPRODUKSI (SYARAT SEBELUM ANGKA APA PUN DIPERCAYA)

Pilot dijalankan dua kali penuh pada mesin yang sama: 10:55 dan 11:26, sebelum dan sesudah
perbaikan label satuan gate. Seluruh 76 angka ringkasan pada blok `ringkas` identik.

| Pemeriksaan | Run 1 | Run 2 | Putusan |
|---|---|---|---|
| `n_fitur` | 40 | 40 | sama |
| FP rule total 9 fold | 2.105 | 2.105 | sama |
| FP hybrid total 9 fold | 927 | 927 | sama |
| Selisih terhadap angka terbit (rule) | 0,67 persen | 0,67 persen | sama, di dalam toleransi 5 persen |
| Selisih terhadap angka terbit (hybrid) | 0,00 persen | 0,00 persen | sama, persis |
| Seluruh angka `ringkas` | - | - | identik (`SEMUA ANGKA RINGKASAN IDENTIK: True`) |
| Waktu jalan | 61,8 detik | 70,2 detik | beda waktu saja, bukan angka |

Perintah: `python3 code/rnd_e4_pilot.py --seeds 42,7`
Bukti: `scratch/rnd/e4/rerun_verify.log`, `scratch/rnd/e4/rerun_fix.log`,
`scratch/rnd/e4/cmp_determinism.py`.

Konsekuensi: R7-1 tertutup bukan dengan klaim, melainkan dengan kriteria selesai yang diminta review,
yaitu FP rule 2.091 lebih kurang 5 persen dan FP hybrid 927 lebih kurang 5 persen. Hasilnya 2.105 dan 927.

---

## 4. ANGKA SEBELUM DAN SESUDAH PERBAIKAN

### 4.1 Pembanding baseline

| Besaran | Sebelum (E3, proksi) | Sesudah (E4, jujur) | Angka terbit E3 | Kelas |
|---|---|---|---|---|
| FP rule 9 fold | tidak dilaporkan | 2.105 | 2.091 | RUN-KITA |
| FP hybrid 9 fold | 195 | 927 | 927 | RUN-KITA |
| FP persistence 9 fold | tidak dilaporkan | 1.941 | tidak ada | RUN-KITA |
| Selisih hybrid terhadap terbit | 78,7 persen lebih rendah | 0,00 persen | acuan | DERIVASI |

Proksi 195 terbukti tidak sah dan tidak dipakai lagi. Angka 927 justru persis sama dengan angka terbit,
sehingga kesimpulan R7 bahwa baseline terbit reproducible terkonfirmasi oleh run mandiri, bukan oleh kutipan.

### 4.2 Kandidat A1 dan baseline pada satuan yang sama

Median 9 fold untuk baseline, median 9 fold untuk A1 seed 42. Kolom gate memakai definisi §2.

| Kandidat | n | FAR baris | FAR kejadian | FAR kalender | Recall | Presisi | Gate lama | Gate lama penuh | Gate baru |
|---|---|---|---|---|---|---|---|---|---|
| Persistence | 9 | 66,048 | 7,0601 | 6,7404 | 0,6791 | 0,7114 | 0 dari 9 | 0 dari 9 | 0 dari 9 |
| Rule t0-1 | 9 | 70,220 | 27,3839 | 6,9320 | 0,7507 | 0,6835 | 0 dari 9 | 0 dari 9 | 0 dari 9 |
| Hybrid rule DAN persistence | 9 | 28,416 | 8,3208 | 4,0984 | 0,6519 | 0,8243 | 0 dari 9 | 0 dari 9 | 0 dari 9 |
| Hybrid proksi E3 (ditolak) | 9 | 6,144 | 0,7680 | 1,0161 | 0,6648 | 0,9630 | 4 dari 9 | 4 dari 9 | 1 dari 9 |
| A1 alpha aturan E2, seed 42 | 9 | 121,9111 | 29,2153 | 7,5565 | 0,1330 | 0,1120 | 0 dari 9 | 0 dari 9 | 0 dari 9 |
| A1 alpha anggaran 1/240, seed 42 | 9 | 0,0000 | 0,0000 | 0,0000 | 0,0000 | 0,4672 | 7 dari 9 | 0 dari 9 | 0 dari 9 |
| Hybrid ML DAN rule seed 42 | 9 | 0,0000 | 0,0000 | 0,0000 | 0,0000 | 0,9773 | 9 dari 9 | 0 dari 9 | 0 dari 9 |
| Hybrid ML ATAU rule seed 42 | 9 | 38,5067 | 9,0604 | 4,0984 | 0,6519 | 0,8158 | 0 dari 9 | 0 dari 9 | 0 dari 9 |

Sumber: `scratch/rnd/e4/e4_beforeafter.json`, `scratch/rnd/e4/e4_summary.json`.

### 4.3 Dampak R7-2 pada A1

| Besaran | Dengan `ts_bin` (E3) | Tanpa `ts_bin` (E4, seed 42) | Arah |
|---|---|---|---|
| Jumlah fitur | 41 | 40 | sesuai tuntutan review |
| FAR 24 jam baris median | 86,7217 | 121,9111 | memburuk |
| Recall median | 0,0740 | 0,1330 | membaik pada definisi ini |
| Fold lulus gate A lama | 2 dari 9 | 0 dari 9 | memburuk |

Angka 121,9111 cocok sampai empat desimal dengan eksperimen P3 pada `RND_R7_REVIEW.md` §7, sehingga
perbaikan R7-2 terkonfirmasi oleh jalur pengukuran yang berbeda. Sesuai instruksi review, angka yang lebih
buruk ini diterima sebagai angka yang jujur dan tidak dipakai sebagai alasan mempertahankan `ts_bin`.

---

## 5. TEMUAN TAMBAHAN YANG DITEMUKAN SAAT VERIFIKASI

### 5.1 Label satuan gate bertentangan dengan perhitungannya (ditemukan dan diperbaiki)

`code/rnd_e4_pilot.py` versi sebelum perbaikan menulis `satuan_dipakai_gate = "kejadian (far24_kalender_kejadian)"`
padahal `gate_A_baru` dihitung dari `far24_kalender`, yaitu satuan baris. Ini keluarga cacat yang sama dengan
R7-3, hanya berpindah tempat: label menyebut satu satuan, angka memakai satuan lain.

Perbaikan: gate baris dipertahankan, gate kejadian ditambahkan sebagai `gate_A_baru_kejadian`, dan label
diubah menjadi "baris (far24_kalender); kejadian dilaporkan berdampingan". Setelah perbaikan, kedua satuan
dapat dibandingkan langsung pada tabel §6.

### 5.2 Kesalahan saya sendiri yang terbukti lewat kegagalan

Saya menaruh skrip bantu bernama `inspect.py` di dalam folder hasil. Nama itu menutupi modul standar
`inspect` sehingga `numpy` gagal diimpor (`AttributeError: module 'inspect' has no attribute 'cleandoc'`).
Skrip diganti nama menjadi `show_summary.py` dan run sesudahnya berhasil. Kesalahan ini dicatat karena
mengubah cara saya menjalankan skrip bantu, bukan karena mengubah angka.

### 5.3 Heuristik satuan yang ambigu (ditemukan dan diperbaiki)

Versi pertama skrip dekomposisi memilih satuan gate dengan mencari kata "kejadian" di dalam label.
Setelah label diperbaiki, label itu memuat kata "kejadian" pada frasa penjelas, sehingga heuristik
diam-diam berpindah satuan tanpa peringatan. Angka dekomposisi langsung berubah. Skrip ditulis ulang
agar menghitung kedua satuan secara eksplisit dengan nama kolom yang berbeda, tanpa menebak dari teks.
Angka yang dipakai di dokumen ini adalah hasil versi eksplisit.

---

## 6. APA YANG SEBENARNYA MENGIKAT GATE

Ini bagian yang mengubah diagnosis E3. E3 menyimpulkan model gagal. Setelah alat ukur diperbaiki,
kegagalan gate pada baseline terbit ternyata bukan pada mutu deteksi, melainkan pada cakupan data.

| Kandidat | n | FAR tidak lebih dari 6 (baris) | FAR tidak lebih dari 6 (kejadian) | Recall tidak kurang dari 0,5 | Cakupan tidak kurang dari 0,50 | Tiga syarat (baris) | Tiga syarat (kejadian) | Fold tanpa alarm |
|---|---|---|---|---|---|---|---|---|
| Persistence | 9 | 4 | 9 | 9 | 1 | 0 | 1 | 0 |
| Rule t0-1 | 9 | 3 | 7 | 9 | 1 | 0 | 0 | 0 |
| Hybrid rule DAN persistence | 9 | 7 | 9 | 9 | 1 | 0 | 1 | 0 |
| Hybrid proksi E3 (ditolak) | 9 | 9 | 9 | 9 | 1 | 1 | 1 | 0 |
| Hybrid ML DAN rule | 18 | 18 | 18 | 0 | 2 | 0 | 0 | 13 |
| Hybrid ML ATAU rule | 18 | 14 | 18 | 18 | 2 | 0 | 2 | 0 |
| A1 alpha aturan E2 | 18 | 6 | 14 | 0 | 2 | 0 | 0 | 0 |
| A1 alpha anggaran 1/240 | 18 | 18 | 18 | 0 | 2 | 0 | 0 | 12 |

Sumber: `scratch/rnd/e4/e4_gate_decomp.json`.

Tiga pembacaan yang dapat dipertanggungjawabkan:

1. **Pada satuan kejadian, syarat FAR dan recall sudah terpenuhi baseline terbit.** Hybrid rule DAN
   persistence lulus FAR tidak lebih dari 6 pada 9 dari 9 fold dan recall tidak kurang dari 0,5 pada
   9 dari 9 fold. Yang gagal hanya cakupan, yaitu 1 dari 9 (hanya F-10 dengan cakupan 0,6730).
2. **Cakupan adalah syarat yang mengikat, bukan model.** Cakupan terendah 0,0171 (F-5) dan tertinggi
   0,6730 (F-10), rentang 39,36 kali. Delapan dari sembilan well tidak dapat disertifikasi gate A baru
   karena datanya tidak menutupi menit kalender, bukan karena detektornya salah.
3. **Sertifikasi palsu terbukti nyata.** Hybrid ML DAN rule lulus gate A lama pada 18 dari 18 fold-run
   dengan FAR 0,0000 dan presisi 0,9773 sampai 1,0000. Angka itu terlihat sempurna, padahal 13 dari 18
   fold-run tidak mengeluarkan satu alarm pun dan recall 0,0000. Inilah bukti langsung bahwa gate A tanpa
   syarat recall memberi sertifikat kepada detektor yang tidak mendeteksi. R7-4 terbukti, bukan sekadar
   disarankan.

---

## 7. AUDIT LABEL HYD (PERMINTAAN R7 §9.3, SEBELUMNYA BELUM DIJALANKAN)

R7 meminta audit label sebelum algoritma apa pun diuji lagi, karena label hyd adalah `|z| > 2` atas residu
SPPA per 10 bin TFLO. Resep diambil apa adanya dari `code/v9_d1_03_rig_datasets.py:55-75`. Skrip:
`scratch/rnd/e4/e4_audit_label.py`. Data 9 well, 87.412 menit teramati.

| Ambang z | Total menit positif | Laju positif | Onset | Retensi terhadap ambang 2 |
|---|---|---|---|---|
| lebih dari 2 | 14.783 | 0,169119 | 2.446 | 1,0000 |
| lebih dari 2,5 | 11.335 | 0,129673 | 2.158 | 0,7668 |
| lebih dari 3 | 8.130 | 0,093008 | 1.626 | 0,5500 |

Per well, ambang lebih dari 2 memberi laju positif antara 742 dari 3.620 menit (F-7) sampai 3.508 dari
20.572 menit (F-12). Rincian: `scratch/rnd/e4/e4_audit_label.json`.

Tiga konsekuensi yang mengubah cara membaca seluruh hasil sebelumnya:

1. **Label hyd bukan label kejadian langka.** Prevalensi 16,91 persen menit positif pada ambang 2, dan
   masih 9,30 persen pada ambang 3. Untuk pembanding, label kerusakan yang dipakai industri biasanya
   berada di bawah 1 persen. Karena itu AUPRC yang mendekati prevalensi bukan tanda model buruk, melainkan
   tanda labelnya memang lebar.
2. **Menaikkan ambang tidak menyelamatkan target, hanya mempersempitnya.** Retensi 0,7668 dan 0,5500
   berarti lebih dari separuh positif hilang pada ambang 3, sementara onsets turun dari 2.446 ke 1.626.
   Target menjadi lebih jarang tanpa bukti bahwa yang tersisa lebih dekat ke kegagalan fisik.
3. **Sirkularitas CUSUM terkonfirmasi secara mekanis.** z pembentuk label adalah z yang sama yang dipakai
   detektor A2. Karena itu A2 tidak boleh dipakai sebagai bukti kemampuan deteksi independen, dan baris
   itu sudah ditandai `SIRKULAR` di `e4_a2.json`.

---

## 8. USULAN TIER DAN STATUS GATE C, A, B

Tier tidak dinaikkan. Alasan utamanya bergeser dari "algoritma tidak cocok" menjadi "cakupan data dan
kesahan label", dan itu justru alasan yang lebih kuat untuk tidak menaikkan tier.

**Usulan: `hyd` K-i tetap `PERINGATAN-BERPENGANWAS`, dengan pemakaian yang dibatasi per well.**

| Lapisan | Pertanyaan | Bukti E4 | Status |
|---|---|---|---|
| C, tepercaya lintas kondisi | Apakah hasil bertahan pada kondisi berbeda | Cakupan 0,0171 sampai 0,6730 (39,36 kali); label proksi `|z|>2` dengan prevalensi 16,91 persen; tidak ada label fisik independen | **GAGAL**, dan ini yang mengikat |
| A, deteksi bekerja | Apakah deteksi menemukan kejadian dengan alarm yang dapat ditangani | Baseline terbit pada satuan kejadian: FAR tidak lebih dari 6 di 9 dari 9 fold, recall tidak kurang dari 0,5 di 9 dari 9 fold, presisi 0,8243; A1 conformal recall 0,0000 pada anggaran 1/240 | **SEBAGIAN**, terpenuhi pada baseline hybrid, tidak pada A1 |
| B, nilai maintenance | Apakah peringatan datang sebelum kondisi memburuk | Tidak ada data durasi inspeksi per alarm di repo | **BELUM TERUKUR** |

Konsekuensi pemakaian yang diusulkan, dengan dasar angka dan bukan preferensi:

1. **TREN** untuk 9 well. Sah karena lapisan A terpenuhi pada satuan kejadian dan presisi 0,8243.
2. **PERINGATAN-BERPENGANWAS** hanya untuk F-10, karena satu-satunya well dengan cakupan 0,6730.
   Untuk well lain, tier ini bersyarat sampai cakupan naik di atas 0,50.
3. **ALARM-OTOMATIS** tidak diusulkan untuk well mana pun. Lapisan C gagal dan lapisan B belum terukur,
   dan kebijakan `RND_EVALUATION_POLICY.md` §2 mengutamakan keamanan saat bukti C lemah.
4. **A1 LightGBM dengan conformal tidak diusulkan untuk pemakaian apa pun pada tahap ini.** Pada anggaran
   alarm 1/240 ia memberi FAR 0,0000 hanya karena recall 0,0000, dan 12 dari 18 fold-run tidak
   mengeluarkan alarm. Detektor yang tidak menyala tidak dapat dipakai sebagai peringatan.

Yang harus selesai sebelum tier dapat naik, berurut kepentingan:
cakupan data di atas 0,50 pada mayoritas well, label yang tidak lagi berupa residu SPPA, lalu pengukuran
lapisan B.

---

## 9. RUJUKAN DAN STATUS VERIFIKASI

Diperiksa 2026-10-27 oleh `scratch/rnd/e4/e4_doi.py`. Lapis 1: HEAD ke `https://doi.org/<doi>` tanpa
mengikuti redirect. Lapis 2: metadata `api.crossref.org` atau `api.datacite.org`. Hasil: 8 dari 8 terdaftar
(HTTP 302) dan 8 dari 8 metadata terjawab (HTTP 200).

| Penulis pertama | Tahun | Judul | DOI | Lapis 1 | Lapis 2 | Status |
|---|---|---|---|---|---|---|
| Kaufman | 2012 | Leakage in Data Mining: Formulation, Detection, and Avoidance | 10.1145/2382577.2382579 | 302 | 200 Crossref, penulis dan tahun cocok | TERVERIFIKASI |
| Kapoor | 2023 | Leakage and the reproducibility crisis in machine-learning-based science | 10.1016/j.patter.2023.100804 | 302 | 200 Crossref, judul dan tahun cocok | TERVERIFIKASI |
| Saito | 2015 | The Precision-Recall Plot Is More Informative than the ROC Plot When Evaluating Binary Classifiers on Imbalanced Datasets | 10.1371/journal.pone.0118432 | 302 | 200 Crossref, judul dan tahun cocok | TERVERIFIKASI |
| Angelopoulos | 2021 | A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification | 10.48550/arXiv.2107.07511 | 302 | 200 DataCite, tahun cocok, judul kosong di record | TERVERIFIKASI, judul dari `arxiv.org/abs/2107.07511` |
| Lei | 2018 | Distribution-Free Predictive Inference for Regression | 10.1080/01621459.2017.1307116 | 302 | 200 Crossref, penulis dan tahun cocok | TERVERIFIKASI |
| Tatbul | 2018 | Precision and Recall for Time Series | 10.48550/arXiv.1803.03639 | 302 | 200 DataCite, tahun cocok, judul kosong di record | TERVERIFIKASI, judul dari `arxiv.org/abs/1803.03639` |
| Page | 1954 | Continuous Inspection Schemes | 10.1093/biomet/41.1-2.100 | 302 | 200 Crossref, penulis dan tahun cocok | TERVERIFIKASI |
| Siffer | 2017 | Anomaly Detection in Streams with Extreme Value Theory | 10.1145/3097983.3098144 | 302 | 200 Crossref, judul dan tahun cocok | TERVERIFIKASI |

Dua judul yang kosong di record register dibuka langsung di halaman arXiv pada 2026-10-27 dan judulnya
cocok dengan yang dikutip. Rujukan `Kaufman (2012)` dan `Kapoor (2023)` dipakai sebagai dasar mengapa
`ts_bin` harus dibuang, bukan sebagai dasar ambang operasional. Ambang FAR 6 per 24 jam tetap KONVENSI
internal, bukan hasil standar, dan itu dicatat di ledger.

---

## 10. CARA REPRODUKSI

```
cd "/mnt/d/Capstone 1(v2)"
PY=/home/neonti/.venvs/rnd_e3/bin/python

$PY code/rnd_e4_pilot.py --seeds 42,7          # pilot penuh, ~70 detik
$PY scratch/rnd/e4/e4_gate_decomp.py           # dekomposisi gate dua satuan
$PY scratch/rnd/e4/e4_beforeafter.py           # tabel sebelum dan sesudah
$PY scratch/rnd/e4/e4_audit_label.py           # audit label z 2 / 2,5 / 3
$PY scratch/rnd/e4/cmp_determinism.py          # bukti reproduksibilitas
$PY scratch/rnd/e4/e4_doi.py                   # verifikasi DOI dua lapis
$PY scratch/rnd/e4/e4_ledger2.py               # tulis ledger E4 dengan assert
```

Semua skrip hanya membaca `scratch/v9_d1/`, `code/`, dan `docs/`, serta hanya menulis ke
`scratch/rnd/e4/` dan Bagian E4 pada `docs/RND_PROVENANCE_LEDGER.md`. Folder `/mnt/d/Capstone 1` tidak dibuka.

Berkas hasil: `e4_a1.json`, `e4_a2.json`, `e4_baseline.json`, `e4_hybrid.json`, `e4_summary.json`,
`e4_beforeafter.json`, `e4_gate_decomp.json`, `e4_audit_label.json`, `e4_doi.json`, `e4_compare.json`,
`run_all.log`, `rerun_verify.log`, `rerun_fix.log`, `audit_label.log`, `doi_verify.log`.

---

## 11. RINGKASAN 5 BARIS

1. Empat temuan R7 ditutup dengan perbaikan kode yang dapat dijalankan: baseline jujur dari bins menghasilkan
   FP rule 2.105 dan FP hybrid 927 (terbit 2.091 dan 927), `ts_bin` dibuang sehingga fitur menjadi 40, dan
   gate memuat syarat recall serta FAR kalender dengan cakupan.
2. Reproduksibilitas terbukti: dua run penuh menghasilkan seluruh 76 angka ringkasan identik, dan angka
   tanpa `ts_bin` (FAR baris 121,9111) cocok sampai empat desimal dengan eksperimen P3 review.
3. Temuan yang mengubah diagnosis: pada satuan kejadian, baseline hybrid lulus FAR tidak lebih dari 6 di
   9 dari 9 fold dan recall tidak kurang dari 0,5 di 9 dari 9 fold, sedangkan syarat cakupan hanya terpenuhi
   di 1 dari 9 well. Yang mengikat gate adalah cakupan data, bukan mutu deteksi.
4. Gate A tanpa syarat recall terbukti memberi sertifikasi palsu: hybrid ML DAN rule lulus 18 dari 18
   fold-run dengan nol alarm pada 13 fold-run dan recall 0,0000.
5. Tier tidak dinaikkan: usulan `hyd` K-i tetap `PERINGATAN-BERPENGANWAS` dengan TREN untuk 9 well dan
   peringatan bersyarat hanya untuk F-10, karena lapisan C gagal pada cakupan dan label proksi, dan
   lapisan B belum terukur.

---

## 12. DAFTAR YANG BELUM TERVERIFIKASI

1. Gate B beban manusia per alarm belum terukur. Tidak ada data durasi inspeksi per alarm di repo, sehingga
   klaim nilai maintenance tidak dapat dibuat.
2. Delay deteksi pada definisi R7 belum tereproduksi. Angka terbit 3,5 menit tidak muncul lagi; rekonstruksi
   jujur memberi 1,0 sampai 10,0 menit per well, dan penyebabnya kemungkinan perbedaan definisi antara
   `detection_stats` dan resep E_STAT. Angka 3,5 menit tidak dipakai di dokumen ini.
3. Median FAR A2 pada satuan kejadian tidak dihitung ulang di E4. Angka 151,16 menjadi 69,17 tetap milik
   `RND_R7_REVIEW.md` §5.2 dan tidak dipakai sebagai dasar rekomendasi di sini.
4. Pengaruh pembuangan `ts_bin` hanya diukur pada seed 42 dan 7, belum pada lima seed.
5. Usulan dua tahap (R7 §9.1) belum dijalankan. Penyempitan kandidat tanpa kehilangan onset masih hipotesis.
6. Kesetiaan label terhadap kegagalan hidraulik fisik belum terukur, karena tidak ada label insiden
   independen. Audit §7 hanya mengukur jumlah dan retensi positif, bukan kebenaran fisiknya.
7. Cakupan pada delapan well selain F-10 bergantung pada ketersediaan sensor, dan penyebab hilangnya menit
   teramati belum dianalisis per kanal. Angka cakupan benar sebagai pengukuran, sebabnya belum.
8. Gate C pada well selain F-10 belum dinilai ulang dengan data segar; statusnya diambil dari cakupan E4
   dan tidak diuji pada periode terpisah.
