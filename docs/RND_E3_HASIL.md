# RND-E3: EKSEKUSI PILOT PADA mode hyd K-i (HASIL NYATA)

Kartu: `t_13309129` · Board: `rnd-algo-2026` · Tanggal: 2026-10-27 (WIB)
Detektor: `hyd` · Klaim: K-i · Workspace: `/mnt/d/Capstone 1(v2)`
Dokumen hulu: `docs/RND_E2_PROTOKOL.md` (protokol), `docs/RND_E1_MATRIKS.md` (kelayakan),
`docs/RND_ALGO_RESEARCH_PLAN.md` §2 (aturan angka) dan §6 (gate C/A/B).

Riset pendahuluan: scikit-learn, statsmodels, exploratory-data-analysis, statistical-analysis, verification-mandatory.

- **scikit-learn**: dipakai untuk memilih metrik dan prosedur evaluasi yang benar pada kelas tidak seimbang (`average_precision_score`, bukan akurasi), serta untuk aturan bahwa praproses dan pemilihan ambang harus berada di dalam fold latih supaya tidak bocor ke fold uji.
- **statsmodels**: dipakai untuk sisi inferensi, yaitu batas kepercayaan laju kejadian Poisson (Garwood/chi-square) dan alasan mengapa selang kepercayaan dilaporkan bersama titik estimasi, bukan sebagai pengganti.
- **exploratory-data-analysis**: dipakai untuk memeriksa struktur data sebelum memodelkan (jumlah baris, jumlah well, kolom turunan label, cakupan waktu teramati per well) dan untuk menjaga agar data mentah tidak diubah.
- **statistical-analysis**: dipakai untuk memisahkan analisis konfirmatori (kriteria E2 yang ditulis sebelum hasil dilihat) dari analisis eksploratif, dan untuk menolak melaporkan recall tanpa laju alarm.
- **verification-mandatory**: dipakai sebagai gerbang akhir, yaitu 113 assert independen terhadap berkas JSON, audit anti-bocor fitur, verifikasi DOI dua lapis, dan daftar eksplisit hal yang belum terukur.

Riset pendahuluan: sequentialthinking, 4 pikiran (`mcp__sequentialthinking__sequentialthinking`, thoughtNumber 1 sampai 4, `thoughtHistoryLength` 4). Ringkas: (1) menetapkan target penilaian gate A dan tiga hipotesis kegagalan, (2) menguji hipotesis bahwa baseline proxy tidak identik dengan baseline terbit, (3) mengenali pola CUSUM tanpa reset sebagai detektor yang menyala terus pada deret berautokorelasi tinggi, (4) menetapkan langkah verifikasi yang harus jalan sebelum menulis, termasuk menolak mengarang angka gate B.

---

## 1. Ringkasan hasil

Pilot berjalan dan menghasilkan angka nyata. **Tidak ada satu pun finalis yang memenuhi gate A.**
Bahkan baseline pun tidak dapat disertifikasi gate A pada 8 dari 9 fold, karena cakupan waktu
teramati di bawah 50 persen.

| Model | FAR per 24 jam (rentang 9 fold) | Recall | Fold lulus gate A | Status |
|---|---|---|---|---|
| Baseline persistence | 32,17 sampai 109,69 | 0,6052 sampai 0,8773 | 0 dari 9 | gagal |
| Baseline hybrid proxy (rule AND persistence) | 2,77 sampai 19,31 | 0,5921 sampai 0,8752 | 4 dari 9, tetapi hanya 1 fold yang dapat disertifikasi | gagal pada kriteria 7 dari 9 |
| A1 LightGBM + conformal | 0,00 sampai 543,50 | 0,0010 sampai 0,5057 | 2 dari 9 (seed 42), 3 dari 45 fold-run semua seed | gagal |
| A1b LightGBM + conformal + fitur lag label | 0,00 sampai 24,14 | 0,0000 sampai 0,3623 | 3 dari 9 | gagal, dan melanggar aturan anti-bocor |
| A2 CUSUM residu SPPA, dengan reset | 127,49 sampai 232,66 | 0,3871 sampai 0,8038 | 0 dari 9 | gagal |
| A2 CUSUM residu SPPA, tanpa reset | 1.330,94 sampai 1.440,00 | 0,8882 sampai 1,0000 | 0 dari 9 | gagal, alarm menyala hampir setiap menit |

Kesimpulan satu baris: gate C dan gate B tidak dapat dinilai jujur karena gate A sudah gagal lebih dulu,
dan protokol E2 §5.4 menyatakan bahwa bila gate A gagal maka tier tetap `PERINGATAN-BERPENGAWAS`.

---

## 2. Apa yang dijalankan

| Butir | Nilai | Sumber |
|---|---|---|
| Skrip pilot | `code/rnd_e3_pilot.py` (23.941 B) | berkas di disk |
| Venv | `/home/neonti/.venvs/rnd_e3/bin/python`, Python 3.11.15 | `scratch/rnd/e3/e3_env.json` |
| Jumlah seed | 5, yaitu 42, 43, 44, 45, 46 | `e3_run_summary.json` `seeds` |
| Jumlah fold | 9 (LOWO satu well keluar) | `e3_run_summary.json` `n_folds` |
| Waktu jalan | 233,7 detik untuk 5 seed x 9 fold + baseline + CUSUM | `e3_run_summary.json` `elapsed_s` |
| Baris data | 52.509 | `e3_verify.json` `v6_total.n_baris` |
| Fitur A1 | 41 kolom numerik, tanpa kolom turunan label | `e3_verify.json` `v5_audit_fitur` |
| Fitur A1b | 43 kolom, termasuk 2 kolom turunan label | idem |

Catatan kejujuran soal perintah: `code/rnd_e3_pilot.py` dijalankan dua kali pada sesi yang sama,
yaitu satu kali dengan daftar seed tunggal (log `scratch/rnd/e3/run_seed42.log`, mulai 07:25:47) dan
satu kali dengan lima seed (log `scratch/rnd/e3/run_all.log`, mulai 07:27:33). Baris perintah lengkap
tidak tersimpan di log, jadi tidak diklaim di sini. Yang dapat dibuktikan adalah isi log dan berkas hasil.

Bukti reproduksibilitas silang yang nyata: dua proses terpisah menghasilkan angka baseline identik,
yaitu F-10 FP 138, F-12 FP 398, F-14 FP 323, F-15A FP 236, F-15_S FP 377 pada kedua log
(`run_seed42.log` baris 2 sampai 6 dan `run_all.log` baris 2 sampai 6).

---

## 3. Data, split, dan batas data

Split memakai `scratch/v9_d1/lowo_hyd_ki.json` dengan unit well. Anti-bocor mengikuti E2 §2.3 L3:
kolom `y_hyd`, `y_prev_hyd`, `valid_prev_hyd`, `obs_hyd`, `anom_hyd`, `lab_ts`, `lab_kind`,
`feat_ts_max` tidak dipakai sebagai fitur pada model A1.

Cakupan waktu teramati per fold adalah temuan pembatas yang paling penting:

| Fold | Jendela teramati | Menit kalender | Fraksi cakupan |
|---|---|---|---|
| F-10 | 7.571| 11.249| 0,6730 |
| F-15A | 6.156| 32.141| 0,1915 |
| F-9_A | 2.206| 7.344| 0,3004 |
| F-7 | 2.482| 23.011| 0,1079 |
| F-15_S | 8.355| 92.488| 0,0903 |
| F-12 | 7.390| 86.454| 0,0855 |
| F-9 | 1.616| 22.858| 0,0707 |
| F-14 | 10.401| 317.679| 0,0327 |
| F-5 | 6.332| 369.549| 0,0171 |

Sumber: `scratch/rnd/e3/e3_cakupan.json`. Hanya 1 dari 9 fold (F-10) yang cakupannya mencapai 50 persen.
E2 §4.1 butir (d) menyatakan fold dengan cakupan di bawah 50 persen tidak dapat disertifikasi.
Konsekuensinya, klaim FAR pada 8 fold lain adalah deskriptif, bukan sertifikasi.

---

## 4. Hasil per model

### 4.1 Baseline dihitung ulang pada fold yang sama

Baseline dihitung dengan resep `v9_e_STAT_01`, yaitu `FAR_24 = FP / (n_neg/60) * 24`.
Aturan `t0-1` diproksikan dengan label satu menit sebelumnya di dalam well yang sama (`rule_lag`),
lalu digabung dengan persistence memakai operator AND.

| Well | Persistence FP | Persistence FAR24 | Persistence P | Persistence R | Hybrid proxy FP | Hybrid proxy FAR24 | Hybrid proxy P | Hybrid proxy R |
|---|---|---|---|---|---|---|---|---|
| F-10 | 138 | 32,17 | 0,8986 | 0,8773 | 12 | 2,80 | 0,9903 | 0,8752 |
| F-12 | 398 | 96,10 | 0,7417 | 0,8015 | 60 | 14,49 | 0,9486 | 0,7770 |
| F-14 | 323 | 48,78 | 0,6313 | 0,6393 | 20 | 3,02 | 0,9643 | 0,6243 |
| F-15A | 236 | 62,26 | 0,6676 | 0,6791 | 16 | 4,22 | 0,9667 | 0,6648 |
| F-15_S | 377 | 73,74 | 0,6145 | 0,6052 | 36 | 7,04 | 0,9423 | 0,5921 |
| F-5 | 152 | 38,33 | 0,7536 | 0,7488 | 11 | 2,77 | 0,9765 | 0,7359 |
| F-7 | 157 | 109,69 | 0,6480 | 0,6865 | 16 | 11,18 | 0,9465 | 0,6722 |
| F-9 | 74 | 89,32 | 0,7927 | 0,6690 | 16 | 19,31 | 0,9446 | 0,6454 |
| F-9_A | 86 | 66,05 | 0,7114 | 0,6405 | 8 | 6,14 | 0,9630 | 0,6284 |
| **Total FP** | **1.941** | | | | **195** | | | |

Sumber: `scratch/rnd/e3/e3_baseline_results.json`, diverifikasi ulang langsung dari dataset oleh
`code/rnd_e3_verify.py` pemeriksaan V6 (nilai FP per well cocok persis).

Dua koreksi yang wajib dinyatakan, bukan disembunyikan:

1. **Angka terbit berbeda dari angka hitung ulang.** E2 §4.1 mencatat baseline terbit sebagai
   FP total 2091 (rule) dan 927 (hybrid). Hitung ulang pada fold dan definisi di sini memberi
   1941 (persistence) dan 195 (hybrid proxy). Penyebabnya konkret: proxy `rule_lag` memakai label
   menit sebelumnya, bukan sinyal pra-label dari detektor rule asli, sehingga proxy lebih ketat
   daripada rule sebenarnya. Baseline terbit **tidak** dipakai sebagai pembanding utama di sini.
2. **FAR hybrid terbit 14,6 sampai 58,4 tidak dapat dibandingkan langsung** dengan FAR pada tabel
   ini karena definisi FAR E2 memakai jam negatif teramati, bukan jam kalender.

Gate A pada baseline: persistence lulus 0 dari 9 fold, hybrid proxy lulus 4 dari 9 fold
(F-10 FAR 2,80, F-14 FAR 3,02, F-15A FAR 4,22, F-5 FAR 2,77). Dari empat fold itu, hanya F-10
yang cakupannya di atas 50 persen, sehingga baseline pun hanya punya 1 fold yang dapat disertifikasi.

### 4.2 A1: LightGBM + conformal cross-conformal (CV+)

Titik operasi: alpha terkecil yang masih memberi minimal 1 alarm benar di setiap 8 fold dalam.
Ambang = kuantil (1-alpha) skor negatif out-of-fold. Model uji dilatih pada 8 well dalam penuh.

| Well | alpha | FAR24 | Presisi | Recall | FP | TP | AUPRC | Deteksi dalam 10 menit | Gate A |
|---|---|---|---|---|---|---|---|---|---|
| F-10 | 0,10 | 86,72 | 0,2119 | 0,0717 | 372 | 100 | 0,1816 | 0,3478 | tidak |
| F-12 | 0,10 | 295,29 | 0,1034 | 0,0989 | 1223 | 141 | 0,1549 | 0,1087 | tidak |
| F-14 | 0,10 | 77,92 | 0,1103 | 0,0740 | 516 | 64 | 0,1180 | 0,1552 | tidak |
| F-15A | 0,20 | 543,50 | 0,1463 | 0,5057 | 2060 | 353 | 0,1367 | 0,7576 | tidak |
| F-15_S | 0,05 | 1,96 | 0,0909 | 0,0010 | 10 | 1 | 0,1243 | 0,0156 | ya, tetapi recall 0,0010 |
| F-5 | 0,20 | 213,57 | 0,1084 | 0,1659 | 847 | 103 | 0,1845 | 0,2500 | tidak |
| F-7 | 0,05 | 252,23 | 0,1020 | 0,0974 | 361 | 41 | 0,1309 | 0,2500 | tidak |
| F-9 | 0,05 | 0,00 | 1,0000 | 0,0473 | 0 | 20 | 0,5172 | 0,0000 | ya, tetapi recall 0,0473 |
| F-9_A | 0,10 | 29,18 | 0,0500 | 0,0060 | 38 | 2 | 0,1604 | 0,0833 | tidak |

Sumber: `scratch/rnd/e3/e3_a_conformal_results.json` seed 42. Gabungan semua seed:
median FAR 63,29 per 24 jam dan gate A lulus di 3 dari 45 fold-run.

Penilaian terhadap kriteria E2 §4.1:
(a) FAR tidak lebih dari 6 di minimal 7 dari 9 fold: **gagal**, tercapai 2 dari 9.
(b) recall tidak kurang dari 0,50 di fold yang memenuhi (a): **gagal**, kedua fold yang memenuhi (a)
memberi recall 0,0010 dan 0,0473.
Kriteria gagal eksplisit E2 §4.1 juga terpenuhi, yaitu jumlah fold yang memenuhi (a) kurang dari 5.
Maka A1 **dinyatakan gagal pada gate A**, bukan "belum optimal".

### 4.3 A2: CUSUM dua sisi pada residu SPPA terstandar

z dibangun per well dengan resep label: `qcut(TFLO, 10)` lalu median/MAD per bin, k = 0,5 sigma,
grid h 1,0 sampai 30,0. Alarm jendela = ada alarm CUSUM pada menit `[lab_ts - 10, lab_ts)`.

| Well | h terpilih | FAR24 (dengan reset) | Presisi | Recall | FP | TP | FAR24 (tanpa reset) |
|---|---|---|---|---|---|---|---|
| F-10 | 30,0 | 146,87 | 0,5676 | 0,5933 | 630 | 827 | 1.440,00 |
| F-12 | 30,0 | 188,57 | 0,4141 | 0,3871 | 781 | 552 | 1.439,28 |
| F-14 | 30,0 | 151,16 | 0,3200 | 0,5445 | 1.001 | 471 | 1.440,00 |
| F-15A | 30,0 | 143,79 | 0,3648 | 0,4484 | 545 | 313 | 1.440,00 |
| F-15_S | 30,0 | 133,01 | 0,4009 | 0,4582 | 680 | 455 | 1.403,23 |
| F-5 | 30,0 | 199,19 | 0,3780 | 0,7729 | 790 | 480 | 1.440,00 |
| F-7 | 30,0 | 232,66 | 0,4478 | 0,6413 | 333 | 270 | 1.440,00 |
| F-9 | 30,0 | 194,33 | 0,6786 | 0,8038 | 161 | 340 | 1.440,00 |
| F-9_A | 30,0 | 127,49 | 0,4679 | 0,4411 | 166 | 146 | 1.330,94 |

Sumber: `scratch/rnd/e3/e3_b_cusum_results.json`. Gate A lulus 0 dari 9 pada kedua varian.

Dua catatan metodologis:
1. h yang terpilih selalu batas atas grid (30,0 sigma), artinya kalibrasi di dalam fold tidak pernah
   menemukan ambang yang memenuhi FAR tidak lebih dari 6 sekaligus minimal 1 TP di tiap fold dalam.
   Ini bukan bug pemilihan, ini tanda bahwa kedua syarat itu tidak dapat dipenuhi bersamaan pada data ini.
2. Varian tanpa reset memberi recall 0,8882 sampai 1,0000 dengan FAR 1.330,94 sampai 1.440,00
   per 24 jam. Angka 1440 berarti satu alarm setiap menit. Recall tinggi itu tidak bermakna, dan
   pola ini sama dengan temuan R5 pada deret berautokorelasi tinggi.

Cacat desain yang wajib dinyatakan: z SPPA adalah statistik yang membentuk label
(`qcut(TFLO)`, median/MAD per bin). Karena itu A2 bersifat sirkular terhadap aturan pelabelan.
A2 bersaing dengan rule pada sumbu waktu, bukan menjadi pengganti independen. Hasil A2 tidak boleh
dipakai sebagai bukti bahwa CUSUM dapat mendeteksi hidraulik dari sinyal bebas label.

### 4.4 A1b: varian dengan fitur lag label (diagnostik, bukan hasil)

| Well | alpha | FAR24 | Presisi | Recall | AUPRC | Gate A |
|---|---|---|---|---|---|---|
| F-10 | 0,01 | 7,46 | 0,8725 | 0,1571 | 0,8438 | tidak |
| F-12 | 0,005 | 24,14 | 0,8020 | 0,2840 | 0,6902 | tidak |
| F-14 | 0,005 | 2,27 | 0,7414 | 0,0497 | 0,5538 | ya |
| F-15A | 0,01 | 20,05 | 0,6780 | 0,2292 | 0,6087 | tidak |
| F-15_S | 0,005 | 1,96 | 0,8305 | 0,0493 | 0,5101 | ya |
| F-5 | 0,01 | 6,81 | 0,8929 | 0,3623 | 0,7167 | tidak |
| F-7 | 0,001 | 6,99 | 0,4737 | 0,0214 | 0,4462 | tidak |
| F-9 | 0,005 | 6,04 | 0,9645 | 0,3215 | 0,7999 | tidak |
| F-9_A | 0,001 | 0,00 | tidak terdefinisi | 0,0000 | 0,6257 | ya |

Sumber: `scratch/rnd/e3/e3_a1b_lag_results.json`.

A1b memakai `y_prev_hyd` dan `valid_prev_hyd` sebagai fitur. Keduanya kolom turunan label, dan
E2 §2.3 L3 melarang pemakaian kolom turunan label sebagai fitur. Karena itu A1b **bukan** hasil
pilot yang sah, melainkan batas atas diagnostik: ia menunjukkan bahwa sebagian besar AUPRC dan
presisi tinggi berasal dari label menit sebelumnya, bukan dari fitur operasi. Gate A lulus 3 dari 9,
tetap di bawah 7 dari 9, dan tetap tidak dapat disertifikasi karena cakupan fold.

---

## 5. Status gate C, A, dan B

| Gate | Syarat (plan §6, E2 §5) | Hasil ukur | Status |
|---|---|---|---|
| C, kestabilan | CI tidak memuat no-skill, arah delta bertahan antar well dan antar seed | CI95 AUPRC blok bootstrap hanya dihitung pada seed 42; dispersi FAR antar seed besar (median 63,29, maksimum 543,50) | **tidak dinilai**, karena gate A gagal lebih dulu |
| A, laju alarm | FAR kalender tidak lebih dari 6 per 24 jam | A1 2 dari 9 fold; A2 0 dari 9; baseline hybrid proxy 4 dari 9 | **gagal** untuk semua finalis |
| B, beban manusia | FP per shift dapat diterima | tidak ada data durasi inspeksi per alarm di repo | **BELUM TERUKUR** |

Tambahan yang wajib dibaca bersama tabel di atas: sertifikasi gate A butuh cakupan waktu teramati
minimal 50 persen di fold yang diklaim (E2 §4.1 butir d). Hanya F-10 yang memenuhi syarat itu.
Maka klaim "FAR tidak lebih dari 6 di N fold" untuk N lebih dari 1 **tidak dapat disertifikasi**,
termasuk untuk baseline.

---

## 6. Mengapa gate A gagal: mekanisme, bukan kesan

### 6.1 Anggaran alarm yang tersedia

Gate A menetapkan FAR tidak lebih dari 6 per 24 jam. Dalam satuan menit, itu berarti
6/1440 = 1/240 = 0,00416667. Artinya hanya **0,4167 persen menit negatif** yang boleh menyala.
Setiap ambang pada kuantil alpha otomatis menyala pada sekitar alpha dari menit negatif.

| Model | Fraksi menit negatif menyala | Rasio terhadap anggaran 1/240 |
|---|---|---|
| A1 seed 42 | 0,000000 sampai 0,377428 | 0,0 sampai 90,6 kali |
| A1b (diagnostik) | 0,000000 sampai 0,016767 | 0,0 sampai 4,0 kali |
| A2 dengan reset | 0,088533 sampai 0,161572 | 21,2 sampai 38,8 kali |
| A2 tanpa reset | 0,924267 sampai 1,000000 | 221,8 sampai 240,0 kali |
| Baseline persistence | 0,022341 sampai 0,076177 | 5,4 sampai 18,3 kali |
| Baseline hybrid proxy | 0,001926 sampai 0,013412 | 0,5 sampai 3,2 kali |

Sumber: `scratch/rnd/e3/e3_budget.json`, dihitung dengan `code/rnd_e3_budget.py`.

### 6.2 Sebab yang dapat ditunjuk untuk A1

Alpha yang terpilih adalah 0,05 sampai 0,20, sedangkan anggaran gate A setara alpha 0,00416667.
Artinya titik operasi yang dipilih berada 12 sampai 48 kali di atas anggaran alarm.
Mengapa alpha tidak turun lebih kecil? Karena aturan E2 §4.1 mensyaratkan minimal 1 alarm benar
di **setiap** 8 fold dalam. Pada data ini, alpha di bawah 0,05 membuat setidaknya satu fold dalam
tidak memberi satu pun true positive, sehingga aturan itu menolak alpha yang lebih konservatif.

Kesimpulan mekanis: **aturan titik operasi E2 dan ambang gate A saling bertentangan pada data ini.**
Overlap skor antara menit positif dan menit negatif terlalu besar. Model yang cukup sensitif untuk
menangkap onset juga menyala pada 6 sampai 38 persen menit negatif. Ini bukan masalah kalibrasi
kecil, selisihnya dua orde besaran.

---

## 7. Verifikasi yang dijalankan

`code/rnd_e3_verify.py` menjalankan 113 pemeriksaan dengan assert terhadap berkas JSON:
V1 kesamaan FAR hasil hitung ulang (deviasi maksimum 0,0), V2 total FP baseline, V3 jumlah fold
lulus gate A per model dan per seed, V4 rentang metrik, V5 audit anti-bocor fitur, V6 hitung ulang
baseline langsung dari dataset, V7 syarat 4 kali FP.

Hasil: 113 pemeriksaan, **0 gagal** (`scratch/rnd/e3/e3_verify.json` kunci `ringkasan`).
Pada percobaan pertama, pemeriksaan V5a gagal karena kesalahan penulisan di skrip verifikasi saya
(yang diperiksa A1b, label yang ditulis A1). Bug itu diperbaiki, skrip dijalankan ulang, dan
hasil yang dilaporkan di sini adalah hasil setelah perbaikan.

Verifikasi DOI memakai tiga lapis sesuai `verification-mandatory`: lapis registrasi
HEAD ke doi.org tanpa redirect, lapis metadata ke Crossref atau DataCite, lapis akses penerbit.

---

## 8. Rujukan ilmiah dan status verifikasinya

Sumber: `scratch/rnd/e3/e3_doi.json`, dihasilkan `code/rnd_e3_doi.py` pada 2026-10-27.

| Penulis pertama | Tahun | Judul | DOI | Lapis 1 | Lapis 2 | Lapis 3 | Status |
|---|---|---|---|---|---|---|---|
| Angelopoulos | 2021 | A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification | 10.48550/arXiv.2107.07511 | 302 | 200 (DataCite) | 200 | TERVERIFIKASI |
| Vovk | 2005 | Algorithmic Learning in a Random World | 10.1007/b106715 | 302 | 200 (judul dan tahun cocok, nama penulis kosong di record) | 200 | judul dan tahun TERVERIFIKASI, nama penulis BELUM TERVERIFIKASI dari register |
| Lei | 2018 | Distribution-Free Predictive Inference for Regression | 10.1080/01621459.2017.1307116 | 302 | 200 | 403 | TERVERIFIKASI |
| Page | 1954 | Continuous Inspection Schemes | 10.1093/biomet/41.1-2.100 | 302 | 200 | 403 | TERVERIFIKASI |
| Garwood | 1936 | Fiducial Limits for the Poisson Distribution | 10.1093/biomet/28.3-4.437 | 302 | 200 | 403 | TERVERIFIKASI |
| Hawkins | 1998 | Cumulative Sum Charts and Charting for Quality Improvement | 10.1007/978-1-4612-1686-5 | 302 | 200 | 200 | TERVERIFIKASI |
| Siffer | 2017 | Anomaly Detection in Streams with Extreme Value Theory | 10.1145/3097983.3098144 | 302 | 200 | 403 | TERVERIFIKASI |

Lapis 3 dengan kode 403 adalah blokir bot penerbit (Taylor & Francis, Oxford Academic, ACM),
bukan bukti DOI palsu. Nol dari tujuh DOI gagal di lapis registrasi.
Rujukan LightGBM (Ke et al., 2017, prosiding NeurIPS, tanpa DOI) tidak dipakai sebagai dasar
rekomendasi apa pun di dokumen ini, jadi tidak dimasukkan ke tabel.

---

## 9. Yang belum terukur dan batas tafsir

1. **Gate B (beban manusia) BELUM TERUKUR.** Tidak ada data durasi inspeksi per alarm di repo.
   Jam orang per shift tidak dapat dihitung dari berkas yang ada.
2. **Sertifikasi FAR hanya mungkin di 1 fold (F-10).** Delapan fold lain cakupannya 1,71 sampai
   30,04 persen. Angka FAR di sana deskriptif.
3. **CI95 AUPRC hanya dihitung untuk seed 42.** Dispersi antar seed dilaporkan sebagai rentang
   FAR, bukan sebagai selang kepercayaan.
4. **Uji tanda gate C belum dijalankan** karena gate A gagal lebih dulu. Menjalankan uji tanda
   pada model yang sudah gagal gate A hanya akan menghasilkan angka tanpa keputusan tier.
5. **A2 sirkular terhadap label.** Statistik z adalah pembentuk label. Hasil A2 tidak membuktikan
   kemampuan deteksi independen.
6. **Baseline terbit (2091 dan 927) tidak direproduksi.** Proxy di sini menghasilkan 1941 dan 195.
   Selisih ini dicatat, bukan dijelaskan tuntas, karena mesin rule `t0-1` asli tidak dijalankan
   ulang pada fold ini. Delay terbit (tidak lebih dari 3,5 menit) juga **BELUM TERUKUR** di sini,
   karena `detection_stats` hanya dijalankan untuk alarm model, bukan untuk baseline.
7. **Waktu latih per fold tidak dicatat terpisah.** Yang tersedia hanya total 233,7 detik untuk
   seluruh lintasan.
8. **Tidak ada uji pada satuan bengkel**, karena hyd adalah detektor rig.

---

## 10. Konsekuensi untuk R7 dan E4

1. Kandidat conformal (A1) **tidak layak dinaikkan tier**. Kriteria gagal E2 §4.1 terpenuhi secara
   eksplisit: fold yang memenuhi FAR tidak lebih dari 6 hanya 2 dari 9, kurang dari 5.
2. CUSUM pada residu SPPA (A2) **tidak layak dilanjutkan pada bentuk sekarang** karena dua alasan
   sekaligus: laju alarm 21 sampai 240 kali anggaran, dan sirkularitas terhadap statistik label.
3. Bila R7 ingin mengubah arah, perubahan yang masuk akal secara mekanis adalah mengubah **sasaran
   titik operasi**, bukan mengganti model: menurunkan alpha ke sekitar 0,004 sampai 0,008 dan
   menerima recall rendah, lalu mengukur apakah frekuensi alarm per shift dapat diterima manusia.
   Ini perubahan protokol, sehingga wajib ditulis sebagai protokol baru sebelum dijalankan, bukan
   dipilih setelah melihat hasil.
4. Angka baseline yang dapat dipakai sebagai pembanding pada putaran berikutnya adalah angka hitung
   ulang di bagian 4.1, dengan catatan definisi proxy. Baseline terbit tidak dipakai tanpa
   rekonsiliasi.

---

## 11. Ringkasan 5 baris

1. Pilot jalan: 5 seed x 9 fold LOWO, 52.509 baris, 41 fitur bersih, 233,7 detik, dan verifikasi 113 assert lulus tanpa kegagalan.
2. Gate A gagal untuk semua finalis: A1 lulus 2 dari 9 fold (3 dari 45 fold-run), A2 lulus 0 dari 9, sedangkan syaratnya 7 dari 9.
3. Mekanisme kegagalan terukur: anggaran alarm gate A hanya 1/240 menit negatif, sedangkan alpha conformal terpilih 0,05 sampai 0,20, yaitu 12 sampai 48 kali anggaran.
4. Baseline hybrid proxy lulus gate A di 4 fold, tetapi hanya F-10 yang cakupannya di atas 50 persen, sehingga baseline pun hanya punya 1 fold yang dapat disertifikasi.
5. Tier tidak berubah: tetap `PERINGATAN-BERPENGAWAS`, karena gate A gagal sehingga gate C tidak dinilai dan gate B belum terukur.

## 12. Daftar yang belum terverifikasi

- Gate B: jam orang per shift (tidak ada data durasi inspeksi).
- Nama penulis pertama untuk DOI 10.1007/b106715: judul dan tahun cocok di Crossref, nama penulis kosong di record.
- CI95 AUPRC untuk seed 43 sampai 46: belum dihitung.
- Uji tanda gate C: belum dijalankan, sengaja ditunda karena gate A gagal.
- Rekonsiliasi baseline terbit 2091 dan 927 terhadap proxy 1941 dan 195: belum tuntas.
- Waktu latih per fold: hanya total yang tercatat.
- Kemampuan deteksi independen A2: tidak dapat dipisahkan dari sirkularitas label pada desain ini.
