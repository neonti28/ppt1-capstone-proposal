# RND-E2: PROTOKOL PILOT TIGA KANDIDAT (NESTED LOWO, SEED TETAP, KRITERIA NAIK TIER)

Kartu: `t_79811fae` · Board: `rnd-algo-2026` · Tanggal: 2026-10-27 (WIB)
Workspace: `/mnt/d/Capstone 1(v2)` · Folder arsip `/mnt/d/Capstone 1` tidak disentuh
Dokumen hulu: `docs/RND_ALGO_RESEARCH_PLAN.md`, `docs/RND_E1_MATRIKS.md`, `docs/V9_EVAL_C_LAYERC.md`,
`docs/RND_R6_METRIK.md`, `docs/RND_E0_AUDIT_ENGINE.md`, `docs/RND_D0_DATA_FEASIBILITY.md`
Sumber angka: `scratch/rnd_e2/e2_final.json`, `e2_stats.json`, `e2_probe.json`, `e2_doi.json`
Turunan: `scratch/v9_e_stat/v9_e_stat_03_tool_wear_RESULTS.json`, `scratch/v9_d1/datasets/*.csv.gz`,
`scratch/v9_i1/v9_i1_RESULTS.json`

Riset pendahuluan: experimental-design, statistical-power, verification-mandatory, statistical-analysis.
Masing-masing dipakai begini. `experimental-design` menetapkan bahwa unit yang dirandomisasi dan
direplikasi adalah WELL (9) atau ALAT (4), bukan jendela menit, sehingga rancangan yang sah adalah
leave-one-well-out dengan kalibrasi di dalam fold, bukan pembagian acak baris. `statistical-power`
dipakai untuk menulis batas daya sebelum run: uji tanda pada 9 well baru signifikan bila 8 well
sepakat, pada 4 alat daya nol, dan MDE rasio laju FAR 1,40 berarti penurunan di bawah 29 persen
tidak dapat dibuktikan pada besaran data ini. `verification-mandatory` dipakai untuk menolak angka
yang tidak dapat ditunjuk asalnya (versi pustaka yang tidak terpasang, biaya latih LightGBM yang
belum pernah diukur) dan untuk memeriksa rujukan dua lapis (doi.org tanpa redirect, lalu Crossref).
`statistical-analysis` dipakai untuk mengunci uji sebelum data dilihat: Wilson untuk proporsi,
Garwood untuk laju, uji tanda untuk arah antar well, Holm dan Benjamini-Hochberg untuk keluarga uji,
serta pemisahan tegas antara konfirmatori dan eksploratori.

Riset pendahuluan: sequentialthinking, 7 pikiran (`mcp__sequentialthinking__sequentialthinking`,
thoughtNumber 1 sampai 7, thoughtHistoryLength 7). Ringkasnya: (1) unit independen dan konsekuensi
leave-one-well-out, (2) hipotesis dan falsifier tiap finalis, (3) anatomi gate C, A, B, (4) batas
daya yang harus masuk protokol sebelum jalan, (5) artefak wajib simpan skor per jendela, (6) keluarga
uji dan multiplisitas, (7) gerbang verifikasi dan koreksi pada skrip sendiri.

---

## 0. RINGKASAN KEPUTUSAN

Protokol ini dikunci SEBELUM pilot dijalankan. Sebelas keputusan yang mengikat:

| # | Keputusan | Alasan ringkas |
|---|---|---|
| E2-1 | Unit independen = well (9) untuk hyd dan shk, alat (4) untuk tool_wear | autokorelasi lag-1 di atas 0,97 membuat jendela di dalam satu well bukan replikat (R6 §2.1) |
| E2-2 | Split = LOWO satu well keluar, kalibrasi di dalam fold latih (nested) | kegagalan C paling umum adalah portabilitas ambang (vib FAR menyebar 119 kali), bukan kegagalan deteksi |
| E2-3 | Titik operasi dipatok di dalam fold latih saja, tidak pernah di fold uji | memilih ambang setelah melihat hasil tidak dapat dibedakan dari p-hacking (E1 §7 syarat 1) |
| E2-4 | Seed primer 42, ditambah 43, 44, 45, 46 untuk uji kestabilan | seed tunggal tidak mengukur kestabilan, dan R6 A4 mensyaratkannya |
| E2-5 | Skor per jendela per fold per model WAJIB disimpan | tanpa artefak ini DeLong dan McNemar tetap BELUM TERUKUR (R6 §2.9, A5) |
| E2-6 | FAR dihitung sebagai laju kalender dengan cakupan waktu teramati, bukan laju menit teramati saja | cakupan menit teramati hanya 1,46 sampai 71,7 persen (E0 K-4) |
| E2-7 | Fold di bawah 30 positif dilabeli UNDER-POWERED dan keluar dari inferensi | pada 30 positif setengah lebar Wilson di p=0,5 masih 0,1685 |
| E2-8 | tool_wear TIDAK memakai uji tanda | dengan 4 unit daya nol pada semua tingkat konkordansi (R6 §2.6) |
| E2-9 | Keluarga uji dideklarasikan sebelum run, koreksi Holm untuk keluarga utama | R6 §2.8 dan A6 |
| E2-10 | Runtime maksimum pilot 1.320 menit (110 fold-run x 12 menit) | anggaran diturunkan dari jumlah fold nyata, bukan taksiran |
| E2-11 | Tidak ada finalis yang boleh menaikkan tier hanya karena AUPRC | gate C, A, B harus terpenuhi bersamaan (plan §6) |

---

## 1. OBJEK PILOT DAN STATUS TIER SEKARANG

Tiga finalis diambil dari `docs/RND_E1_MATRIKS.md` §7. Angka tier di bawah adalah keadaan
REGISTRY saat protokol ditulis, bukan hasil pilot.

| Finalis | Algoritma | Mode / klaim | Fold | Tier sekarang | Gerbang yang gagal sekarang |
|---|---|---|---|---|---|
| F1 | Conformal kuantil (lintas well dan dalam well) | hyd K-i | 9 well | PERINGATAN-BERPENGAWAS | gate A: FAR 14,6 sampai 58,4 per 24 jam di 9 dari 9 well |
| F2 | Page-Hinkley dengan reset | tool_wear K-i | 4 alat x 2 run | PERINGATAN-BERPENGAWAS (bengkel) | gate B: presisi run 0,50, dan gate A pada satuan per menit (lihat §6.2) |
| F3 | Boosting terkalibrasi (LightGBM atau XGBoost) | shk | 9 well | PERINGATAN-BERPENGAWAS (rule) dan TREN (RF) | gate C: CI RF memuat prevalensi di 7 dari 9 fold |

Keadaan REGISTRY terukur saat ini: 7 mode, 27 head, dengan 12 head PERINGATAN-BERPENGAWAS,
13 head TREN, 2 head BELUM LAYAK PAKAI, dan **0 slot ALARM-OTOMATIS** (ledger E2-006).
Artinya pilot ini tidak boleh menghasilkan satu pun head bertier ALARM-OTOMATIS kecuali ketiga gate
terpenuhi pada angka yang dapat diaudit.

Data yang dipakai sudah diperiksa ulang langsung dari berkas, bukan dari ringkasan dokumen:

| Dataset | Baris | Well atau alat | Label yang dipakai | Positif minimum per fold | Positif maksimum per fold |
|---|---|---|---|---|---|
| `hyd_ki.csv.gz` | 52.509 | 9 well | `y_hyd` | 331 (F-9_A) | 1.426 (F-12) |
| `shk.csv.gz` | 56.495 | 9 well | `y_shk` | 30 (F-9_A) | 760 (F-14) |
| `toolwear_windows.csv` | 469 | 4 alat (T01 120, T02 112, T03 121, T04 116) | label regime di dalam run, bukan kolom `y_*` | tidak berlaku, lihat §3.5 | tidak berlaku |

Catatan penting mengenai berkas bengkel: `scratch/v6_e1/toolwear_windows.csv` punya 32 kolom dan
9 kolom berawalan `Y_` (`Y_mean`, `Y_rms`, dan seterusnya). Kolom itu adalah statistik sinyal sumbu Y,
BUKAN label. Deteksi otomatis "kolom label" pada skrip probe sempat salah menandainya sebagai label
karena awalan `Y_`; kesalahan itu ditemukan dan dicatat (ledger E2-013). Label tool_wear adalah
perubahan regime di dalam run seperti didefinisikan ulang di §3.5.

---

## 2. DESAIN SPLIT: LOWO DENGAN KALIBRASI DI DALAM FOLD

### 2.1 Mengapa unitnya well, bukan jendela

Jendela menit di dalam satu well berkorelasi tinggi. RND-R5 mengukur autokorelasi lag-1 di atas 0,97
pada deret yang sama, sehingga memperlakukan 7.571 jendela F-10 sebagai 7.571 sampel independen
adalah pseudoreplikasi. `experimental-design` menamai ini kesalahan struktural yang tidak dapat
diperbaiki pada tahap analisis: replikat harus berada pada tingkat tempat perlakuan diterapkan, yaitu
well. Konsekuensi angka: n = 9 untuk hyd dan shk, n = 4 untuk tool_wear. Semua uji inferensial yang
mengasumsikan independensi baris DILARANG dipakai untuk menyimpulkan portabilitas.

### 2.2 Anatomi satu fold

Setiap fold punya tiga lapis, dan hanya lapis terluar yang menghasilkan angka yang dilaporkan:

```
FOLD k (well uji = w_k)
├─ Lapis 0  TEST   : seluruh jendela well w_k. TIDAK PERNAH disentuh sampai titik operasi dipatok.
├─ Lapis 1  TRAIN  : 8 well sisanya. Model dilatih hanya di sini.
└─ Lapis 2  CALIB  : di dalam TRAIN, satu well dikeluarkan bergiliran (inner LOWO, 8 fold).
                     Titik operasi (alpha conformal, ambang Page-Hinkley, ambang boosting)
                     dipilih dari 8 fold dalam ini saja, dengan aturan yang ditulis di §5.
```

Urutan operasi yang mengikat, dieksekusi per fold:

1. Tetapkan well uji `w_k`, sisihkan seluruh barisnya.
2. Di dalam TRAIN, bangun 8 fold dalam (inner LOWO). Untuk tiap fold dalam: latih model, hitung skor
   pada well dalam yang dikeluarkan, catat TP, FP, FN, dan jam negatif.
3. Pilih titik operasi dari agregat 8 fold dalam dengan aturan yang dipatok per finalis (§5). Aturan
   pemilihan ditulis sebagai fungsi dari angka fold dalam, bukan dari angka fold uji.
4. Latih ulang model pada SELURUH TRAIN dengan titik operasi hasil langkah 3.
5. Baru buka TEST: hitung skor pada well uji, terapkan titik operasi, catat TP, FP, FN, jam negatif,
   cakupan waktu, dan seluruh metrik sekunder.
6. Simpan skor per jendela untuk fold uji, plus salinan titik operasi yang dipakai.

Langkah 3 yang membuat prosedur ini bersarang. Tanpa langkah 3, titik operasi akan dipilih dari angka
fold uji dan hasilnya bias optimistis (Varma & Simon 2006, DOI terverifikasi di §11).

### 2.3 Aturan anti-bocor yang berlaku untuk ketiga finalis

Daftar berikut berasal dari temuan audit E0 dan berlaku sebagai syarat mutlak, bukan saran. Kolom
yang masuk daftar terlarang dibuang dari matriks fitur sebelum fold pertama dibangun, dan skrip pilot
wajib meng-assert bahwa kolom itu tidak ada.

| Aturan | Isi | Asal |
|---|---|---|
| L1 | Kolom berawalan `y_`, `valid_`, `obs_`, `anom_` tidak boleh masuk fitur | `code/v9_i1_pipeline.py:64` (META_COLS/LABEL_PREFIXES) |
| L2 | Kolom masa depan (`feat_ts_max` lebih besar dari `ts_bin` pada baris yang sama) dibuang | E0 K-5 |
| L3 | `obs_hyd` dan `anom_hyd` dihitung di dalam jendela label, jadi DILARANG dipakai sebagai fitur | E0 K-5 (`code/v9_d1_03_rig_datasets.py:119-120`) |
| L4 | Standardisasi, imputasi, dan pemilihan fitur hanya di-fit pada TRAIN, tidak pada TEST | `experimental-design` bagian pseudoreplikasi dan kebocoran |
| L5 | Satu well tidak boleh muncul di TRAIN dan TEST pada fold yang sama | definisi LOWO |

### 2.4 Jumlah fold dan jalur fold dalam

| Finalis | Fold luar | Fold dalam per fold luar | Total latih model per seed |
|---|---|---|---|
| F1 hyd conformal | 9 | 8 | 9 x (8 + 1) = 81 |
| F2 tool_wear Page-Hinkley | 4 | 3 | 4 x (3 + 1) = 16 |
| F3 shk boosting | 9 | 8 | 9 x (8 + 1) = 81 |

Total 178 latih model per seed untuk tiga finalis. Dengan 5 seed (42 sampai 46) menjadi 890 latih
model, dan itu angka yang dipakai untuk menetapkan anggaran runtime di §4.3.

### 2.5 Satu pengecualian yang dinyatakan terbuka: tool_wear tidak punya 8 fold dalam

tool_wear hanya punya 4 alat. Pada F2, fold dalam berjumlah 3, dan uji inferensial lintas alat
mustahil (daya uji tanda nol pada n=4). Karena itu F2 hanya boleh menyimpulkan dua hal:
(1) perilaku PER ALAT, dilaporkan utuh tanpa dirata-rata, dan (2) klaim lintas alat hanya bila
keempat alat searah. Rata-rata empat alat TIDAK dipakai sebagai dasar naik tier (E2-8).

---

## 3. REPRODUKSIBILITAS

### 3.1 Seed

| Peran | Nilai | Kegunaan |
|---|---|---|
| Primer | 42 | semua angka yang dilaporkan sebagai hasil pilot |
| Kestabilan | 43, 44, 45, 46 | uji apakah arah delta berubah bila seed berubah (R6 A4) |

Aturan: angka yang dilaporkan diambil dari seed 42. Kelima seed dipakai untuk menghitung dispersi
antar seed, dan dispersi itu dilaporkan sebagai metrik sekunder. Bila arah delta berubah tanda pada
seed lain, status klaim diturunkan menjadi tidak stabil, bukan dirata-ratakan.

### 3.2 Versi pustaka: belum terukur, dan protokol memblokir run tanpa tangkapan versi

Diperiksa pada host ini tanggal 2026-10-27: `numpy`, `pandas`, `scikit-learn`, `scipy`, `statsmodels`,
`lightgbm`, `xgboost`, `catboost`, dan `pyarrow` **TIDAK TERPASANG** pada interpreter yang dipakai
(`Python 3.14.9`, tanpa pip). Karena itu versi pustaka untuk pilot **BELUM TERUKUR**, dan tidak ada
angka versi yang boleh ditulis di dokumen ini.

Konsekuensi protokol: langkah pre-flight berikut bersifat memblokir.

1. Sebelum fold pertama, jalankan `python -m pip freeze > scratch/rnd_e2/pip_freeze.txt`.
2. Tulis hash berkas itu ke `scratch/rnd_e2/e2_env.json` bersama versi Python.
3. Bila berkas itu tidak ada atau kosong, pilot TIDAK BOLEH dijalankan, dan statusnya dilaporkan
   sebagai terblokir, bukan sebagai gagal.

Alasan aturan ini bukan formalitas: hasil E1 menyatakan biaya latih LightGBM, XGBoost, dan CatBoost
pada data kita BELUM TERUKUR, dan tanpa versi yang tercatat, selisih hasil antar run tidak dapat
diatribusikan ke metode atau ke pustaka.

### 3.3 Artefak wajib per fold

| Artefak | Bentuk | Alasan wajib |
|---|---|---|
| Skor per jendela | `parquet`, kolom: `well`, `ts_bin`, `y`, `skor`, `model`, `fold`, `seed` | DeLong dan McNemar BELUM TERUKUR karena artefak ini tidak ada (R6 §2.9) |
| Titik operasi | `json`: alpha, ambang, jam negatif fold dalam, tanggal | membuktikan titik operasi dipilih di dalam fold |
| Hitungan berpasangan | `csv`: TP/FP/FN per jendela untuk pasangan model | McNemar butuh tabel ketidaksesuaian berpasangan |
| Cakupan waktu | `json`: menit teramati, menit kalender, fraksi cakupan | E0 K-4 |
| Hash dataset | sha256 berkas masukan | membuktikan fold dijalankan pada data yang sama |

### 3.4 Runtime maksimum

Anggaran dihitung dari jumlah fold nyata, bukan taksiran rasa. Jangkar yang sudah terukur: satu
lintasan prototipe 7 mode pada seluruh data selesai dalam 21,55 detik (`scratch/v9_i1/v9_i1_RESULTS.json`
`meta.elapsed_s`), tetapi lintasan itu hanya memuat rule, persistence, dan RF, bukan latih boosting
dengan kalibrasi bersarang.

| Pos | Nilai | Dasar |
|---|---|---|
| Batas per fold luar (termasuk 8 fold dalam) | 12 menit | KONVENSI, lihat catatan di bawah |
| Jumlah fold luar | 22 (9 hyd, 9 shk, 4 tool_wear) | D0 |
| Jumlah seed | 5 | §3.1 |
| Jumlah fold-run | 110 | 22 x 5 |
| Runtime maksimum pilot | 1.320 menit (22 jam) | 110 x 12 |
| Batas satu proses | 1.740 detik per fold, lalu proses dihentikan dan fold ditandai TIMEOUT | di bawah batas terminal 1.770 detik |

Angka 12 menit per fold adalah KONVENSI yang ditetapkan dokumen ini, bukan hasil ukur. Dasar
pemilihannya: biaya latih boosting pada data kita BELUM TERUKUR (E1 §7.3 kriteria berhenti), jadi
batas ini berfungsi sebagai pengaman agar satu fold tidak menghabiskan seluruh anggaran. Bila pada
run pertama satu fold melewati 12 menit, hasilnya dilaporkan sebagai temuan biaya, dan jumlah fold
diturunkan dengan pernyataan eksplisit, bukan diam-diam.

---

## 4. TIGA FINALIS: HIPOTESIS, BASELINE, METRIK, KRITERIA SUKSES

Aturan umum yang berlaku untuk ketiganya:

- Baseline pembanding EMPAT jenis: rule (ambang kanal apa adanya), persistence (`y_prev`), hybrid
  (rule dan persistence digabung dengan aturan yang sudah ada di REGISTRY), dan RF (hanya pada hyd
  dan shk, karena tool_wear tidak punya RF di V9).
- Metrik utama ditetapkan satu per finalis. Metrik sekunder dilaporkan semua, termasuk yang jelek.
- Kriteria sukses ditulis sebagai angka dan bentuk evaluasi mesin, bukan kata sifat.
- Pembanding selalu pada fold yang SAMA. Membandingkan angka finalis di 9 well dengan angka
  persistence di 7 well adalah kesalahan yang tidak boleh terjadi.

### 4.1 F1: Conformal pada hyd K-i

**Hipotesis H1.** Titik operasi yang dipilih dengan conformal di dalam fold latih menghasilkan FAR
kalender tidak lebih dari 6 per 24 jam pada mayoritas fold uji, tanpa menghapus alarm pada fold itu.

**Yang ditolak bila H1 benar-benar salah.** Bila alpha yang menghasilkan FAR tidak lebih dari 6
ternyata menghasilkan nol alarm di fold uji, maka ambang tunggal tidak dapat melayani 9 well, dan
itu temuan, bukan kegagalan alat (kriteria berhenti E1 §7.1).

| Pos | Isi |
|---|---|
| Baseline | rule t0-1 (FP total 2091 lintas fold), persistence (P 0,615 sampai 0,793; FAR 32,2 sampai 109,7), hybrid (FAR 14,6 sampai 58,4; FP 2.091 menjadi 927), RF DILARANG di kelas ini (D-A5, delta B negatif 7/7) |
| Metrik utama | FAR kalender per 24 jam pada titik operasi terkalibrasi, dihitung per fold |
| Metrik sekunder | recall, presisi, cakupan waktu teramati, jumlah alarm per shift, delay deteksi median (menit), B1 bila onset tersedia, dispersi antar fold dan antar seed |
| Kriteria sukses angka | (a) FAR kalender tidak lebih dari 6 per 24 jam di **minimal 7 dari 9 fold**; (b) recall tidak kurang dari 0,50 di tiap fold yang memenuhi (a); (c) CI95 FAR tidak memuat nilai di atas 6 di 7 dari 9 fold; (d) cakupan waktu teramati tidak kurang dari 50 persen per fold, bila kurang maka fold dilaporkan tidak dapat disertifikasi |
| Kriteria gagal angka | FAR tidak lebih dari 6 tercapai dengan recall 0 di lebih dari 1 fold, ATAU jumlah fold yang memenuhi (a) kurang dari 5 |
| Titik operasi dipatok dari | alpha conformal terkecil (paling konservatif) yang masih memberi minimal 1 alarm benar di 8 fold dalam |

### 4.2 F2: Page-Hinkley dengan reset pada tool_wear K-i

**Hipotesis H2.** Page-Hinkley dengan reset, dikalibrasi per alat di dalam run, menurunkan FP per
alat pada segmen evaluasi tanpa menurunkan TLead di bawah baseline 20 detik.

**Temuan yang sudah terukur dan mengubah kriteria.** Pada titik operasi terkalibrasi target 1 FP per
menit, FP per alat pada segmen evaluasi R01 adalah 1, 3, 1, 3 untuk T01 sampai T04. Dikonversi ke
laju memakai durasi segmen evaluasi masing-masing alat (42, 35, 42, 40 jendela 1 detik), laju
 menjadi 1,43, 1,43, 4,50, dan 5,14 FP per menit. Artinya **0 dari 4 alat** memenuhi konvensi gate A
bengkel (tidak lebih dari 1 alarm per menit) pada segmen evaluasi, walaupun target kalibrasinya
1 FP per menit. Menaikkan target menjadi 0,2 FP per menit TIDAK menurunkan FP sama sekali
(tetap 1, 3, 1, 3), karena ambang berbasis hitungan fitur terkuantisasi (ledger E2-008, E2-009).
Karena itu F2 tidak boleh dijanjikan sebagai perbaikan gate A tanpa mengubah mekanisme ambang.

| Pos | Isi |
|---|---|
| Baseline | rule 3-RMS dalam-run (FP R01: 41, 33, 40, 36 per alat), detektor 5/27 (deteksi 4/4 tetapi FAR 42,857 sampai 58,571 FP per menit, terlalu sensitif), titik operasi terkalibrasi (FP 1, 3, 1, 3; TLead 20, 24, 25, 36 detik) |
| Metrik utama | FP per menit pada segmen evaluasi R01, dilaporkan PER ALAT |
| Metrik sekunder | TLead ke akhir R02 (detik), cakupan alarm di R02 (persen jendela), presisi run, jumlah fitur yang melewati 3 sigma, dispersi lintas keluarga fitur |
| Kriteria sukses angka | (a) FP per menit tidak lebih dari 1,0 di **keempat alat**; (b) deteksi R02 tetap 4 dari 4; (c) TLead median tidak turun di bawah 20 detik dan TLead tiap alat tidak turun lebih dari 20 persen dari baseline alat itu; (d) presisi run tidak kurang dari 0,80 |
| Kriteria gagal angka | FP per menit tidak lebih dari 1,0 tercapai di kurang dari 3 alat, ATAU TLead median turun di bawah 20 detik |
| Titik operasi dipatok dari | ambang hitungan fitur per alat yang memberi FP per menit tidak lebih dari 1,0 pada 3 fold dalam (alat lain), lalu diterapkan apa adanya ke alat uji |

Batasan yang dinyatakan terbuka: F2 adalah domain bengkel. TLead dalam detik tidak boleh dijumlahkan
dengan lead rig dalam menit (D-A7), dan transfer ke rig tidak diklaim.

### 4.3 F3: Boosting terkalibrasi pada shk

**Hipotesis H2b.** Boosting terkalibrasi menaikkan daya pisah di atas RF pada mayoritas well, dan
kalibrasi menjaga FAR tidak melewati 6 di lebih banyak fold daripada rule.

**Yang ditolak bila H2b salah.** Bila AUPRC naik tetapi FAR melewati 6 di lebih banyak fold, boosting
dinyatakan gagal pada gate A walaupun menang di AUPRC (kriteria berhenti E1 §7.3). Bila biaya latih
melebihi anggaran sehingga hanya satu fold selesai, hasilnya bukan perbandingan, dan statusnya
kembali BELUM TERUKUR.

| Pos | Isi |
|---|---|
| Baseline | rule (FAR 0,67 sampai 6,6; tidak lebih dari 6 di 7 dari 9 well), persistence (menang atau seri dengan prevalensi di 7 dari 9), hybrid, RF (AUPRC 0,007 sampai 0,193; CI memuat prevalensi di 7 dari 9 fold) |
| Metrik utama | delta AUPRC berpasangan terhadap RF pada fold yang sama, dengan CI bootstrap blok per well |
| Metrik sekunder | FAR pada titik operasi terkalibrasi, recall, presisi, Brier score, kalibrasi (reliability slope), waktu latih (detik), jumlah pohon, dispersi antar seed |
| Kriteria sukses angka | (a) delta AUPRC positif di **minimal 8 dari 9 well** pada seed 42; (b) delta AUPRC minimal 0,023 pada fold berprevalensi rendah dan minimal 0,0192 pada fold berprevalensi tinggi (MDE terukur, R6 §3.3); (c) CI95 delta tidak memuat 0; (d) jumlah fold dengan FAR tidak lebih dari 6 TIDAK BERKURANG dari baseline rule (7 dari 9); (e) waktu latih per fold tidak lebih dari 12 menit |
| Kriteria gagal angka | delta AUPRC positif di kurang dari 7 well, ATAU jumlah fold FAR tidak lebih dari 6 turun di bawah 7, ATAU waktu latih satu fold melewati 12 menit sehingga fold lain tidak selesai |
| Titik operasi dipatok dari | ambang skor yang memberi FAR tidak lebih dari 6 pada agregat 8 fold dalam, dipilih sebelum fold uji dibuka |

---

## 5. KRITERIA NAIK TIER: APA YANG DIHITUNG UNTUK TIAP GATE

Gate mengikuti plan §6 dan tidak boleh diubah setelah hasil terlihat. Yang ditulis di sini adalah
DEFINISI HITUNG, supaya hasilnya dapat diperiksa ulang orang lain.

### 5.1 Gate C: kestabilan

| Yang dihitung | Rumus atau definisi | Ambang lulus |
|---|---|---|
| Dispersi antar fold | min, median, maks, dan rasio maks dibagi min untuk metrik utama | rasio dilaporkan apa adanya; lulus bila arah delta searah di minimal 7 dari 9 well (hyd, shk) atau 4 dari 4 alat (tool_wear) |
| Arah per fold | tanda delta finalis dikurangi baseline, per fold | uji tanda eksak dua sisi, alpha 0,05; pada 9 well butuh 8 sepakat (p = 0,0390625, daya 0,7748 pada konkordansi 0,90); pada 7 well butuh 7 dari 7 (p = 0,015625, daya 0,4783); pada 4 alat uji tanda DILARANG (daya 0) |
| Bebas no-skill | CI95 AUPRC per fold dibanding prevalensi fold itu | lulus bila CI tidak memuat prevalensi di minimal 7 dari 9 fold |
| Kestabilan seed | arah delta pada seed 42, 43, 44, 45, 46 | lulus bila tanda sama di kelima seed untuk minimal 7 dari 9 well |
| Kestabilan waktu | delta dihitung pada dua paruh waktu well (awal dan akhir) | dilaporkan; bila tanda berubah, klaim diturunkan menjadi tidak stabil |

### 5.2 Gate A: laju alarm

Dua satuan dipakai, dan tidak boleh dicampur:

| Lingkup | Definisi | Ambang | Cara hitung |
|---|---|---|---|
| Rig (hyd, shk) | FAR kalender per 24 jam | tidak lebih dari 6 | `FAR_24 = FP / jam_neg_teramati * 24`, dengan `jam_neg_teramati` = jumlah jendela negatif x 60 detik / 3600; cakupan = jam teramati dibagi jam kalender well itu, dilaporkan bersama |
| Bengkel (tool_wear) | alarm per menit | tidak lebih dari 1 | `FAR_menit = FP / (n_jendela_negatif / 60)`, jendela 1 detik |

Syarat sertifikasi yang harus diperiksa SEBELUM mengklaim gate A (resolusi instrumen, R6 §3.4):

| Syarat | Angka | Konsekuensi |
|---|---|---|
| `jam_neg` minimal 4 x FP | 1 FP butuh 4,0 jam; 3 FP butuh 12,0 jam; 6 FP butuh 24,0 jam; 30 FP butuh 120,0 jam | bila gagal, klaim FAR tidak dapat disertifikasi pada fold itu |
| Dengan 0 FP, batas atas Garwood 95 persen dua sisi | 3,6889 per satuan paparan; `jam_neg` minimal 14,7555 jam untuk FAR tidak lebih dari 6 | contoh terukur: ssi F-9_A hanya 13,1 jam negatif, batas atas 6,7583, jadi FAR tidak lebih dari 6 TIDAK DAPAT DISERTIFIKASI di sana, terlepas dari hasil ujinya |
| CI laju | Garwood eksak, bukan Wald dan bukan Wilson | dilaporkan bersama titik |
| MDE rasio laju | 1,40 | penurunan FAR kurang dari 29 persen tidak dapat dibuktikan pada besaran data ini |

Temuan gate A yang sudah terukur dan relevan untuk F2: pada satuan bengkel, laju segmen evaluasi
ialah 1,43, 1,43, 4,50, 5,14 per menit untuk T01 sampai T04, sehingga 0 dari 4 alat lulus. Ini bukan
kekeliruan dokumen hulu, karena `docs/V9_EVAL_C_LAYERC.md` §2.7 melaporkan FP 1 sampai 3 per alat
(tanpa satuan per menit) dan angka itu memang benar sebagai hitungan FP. Yang belum pernah dihitung
adalah konversinya ke laju per menit pada segmen evaluasi, dan konversi itu mengubah kesimpulan.

### 5.3 Gate B: beban manusia

| Yang dihitung | Definisi | Ambang lulus |
|---|---|---|
| Alarm per shift | jumlah alarm per 8 jam operasi pada titik operasi yang dipatok | dilaporkan; lulus bila tidak lebih dari 3 per shift (KONVENSI dokumen ini) |
| Presisi pada titik patok | TP dibagi TP ditambah FP, pada titik operasi yang dipatok SEBELUM run | tidak kurang dari 0,80 untuk F2, tidak kurang dari 0,50 untuk F1 dan F3 |
| Beban per inspeksi | menit pemeriksaan per alarm (asumsi 10 menit per alarm, KONVENSI) | dilaporkan sebagai jam orang per shift |
| Alarm tumpang tindih | jumlah alarm berurutan dalam 5 menit yang dihitung satu | dilaporkan; penyatuan alarm tidak boleh dipakai menurunkan FAR tanpa menyebut aturannya |

Presisi dilaporkan pada titik operasi yang dipatok, bukan pada titik operasi terbaik yang dicari
setelah hasil terlihat. Ini pembeda antara pengukuran dan pencarian.

### 5.4 Ringkasan: apa yang dihitung per finalis per gate

| | Gate C | Gate A | Gate B |
|---|---|---|---|
| F1 hyd | dispersi FAR dan recall antar 9 well, uji tanda (butuh 8 dari 9), CI AUPRC lawan prevalensi, kestabilan 5 seed | FAR kalender per 24 jam per fold, Garwood, cakupan waktu, syarat 4 x FP | presisi pada alpha terpatok, alarm per shift, jam orang |
| F2 tool_wear | PER ALAT, tanpa uji tanda, arah sama di 4 dari 4 alat, kestabilan 5 seed | FP per menit segmen evaluasi per alat, ambang tidak lebih dari 1,0, deteksi 4 dari 4, TLead | presisi run, sasaran 0,80, alarm per shift bengkel |
| F3 shk | delta AUPRC berpasangan lawan RF, uji tanda (butuh 8 dari 9), CI lawan prevalensi, kestabilan 5 seed | FAR kalender per 24 jam, jumlah fold lulus tidak boleh turun dari 7 dari 9, Garwood | presisi pada ambang terpatok, alarm per shift, waktu latih sebagai beban mesin |

### 5.5 Aturan naik tier

Naik tier ke ALARM-OTOMATIS hanya diusulkan bila ketiga gate lulus BERSAMAAN pada seed 42 dan arah
gate C bertahan pada kelima seed. Bila gate C lulus tetapi gate A gagal, tier tetap
PERINGATAN-BERPENGAWAS dan alasan penolakan ditulis dengan angka gate yang gagal. Bila gate A lulus
tetapi gate C gagal, tier justru turun ke TREN, karena alarm yang tidak stabil lebih berbahaya
daripada tidak ada alarm.

---

## 6. RENCANA ANALISIS

### 6.1 Uji yang dipakai, dan yang dilarang

| Pertanyaan | Uji sah | Alasan |
|---|---|---|
| Dua model pada jendela yang sama (finalis lawan RF) | McNemar pada tabel ketidaksesuaian berpasangan, atau DeLong bila membandingkan AUROC | Fisher tidak sah untuk data berpasangan (R6 §2.5) |
| Delta AUPRC antar model | bootstrap blok per well, 120 resampel, CI95 | AUPRC tidak punya bentuk asimtotik DeLong (Boyd 2013) |
| Presisi satu fold | Wilson, dari TP dan FP mentah | Wald tidak sah pada n kecil atau p dekat 1 |
| Laju FAR | Garwood eksak | penyebutnya jam paparan, bukan jumlah percobaan |
| Perbedaan presisi dua well berbeda | Fisher eksak | dua kelompok independen |
| Arah perbaikan antar well | uji tanda eksak, alpha 0,05 | unit well, bukan jendela |
| Banyak uji dalam satu keluarga | Holm, lalu Benjamini-Hochberg sebagai pembanding | R6 §2.8 |
| Dilarang | uji yang mengasumsikan independensi jendela, chi-square pada tabel agregat tanpa unit well, perbandingan rata-rata fold tanpa bobot dan tanpa dispersi | pseudoreplikasi |

### 6.2 Keluarga uji dan multiplisitas, dideklarasikan sebelum run

| Keluarga | Isi | Jumlah uji | Koreksi |
|---|---|---|---|
| K1 | delta AUPRC finalis lawan RF pada F3, per well | 9 | Holm |
| K2 | gate C F1: tanda delta FAR hybrid lawan rule per well | 9 | Holm |
| K3 | gate C F3: tanda delta AUPRC lawan RF per well | 9 | Holm |
| K4 | gate A: FAR finalis lawan baseline pada titik patok, per finalis | 3 | Holm |
| K5 | uji tambahan apa pun setelah p mentah terlihat | tidak ditentukan | dilaporkan eksploratori, tidak dipakai untuk klaim konfirmatori |

Selang kepercayaan dilaporkan tanpa koreksi, karena koreksi multiplisitas mengatur keputusan
tolak atau tidak, bukan estimasi. Uji yang ditambahkan setelah hasil terlihat masuk K5.

### 6.3 Fold di bawah 30 positif

Aturan yang mengikat, berlaku per fold dan per finalis:

1. Fold dengan positif kurang dari 30 dilabeli **UNDER-POWERED**.
2. Fold itu tetap dilaporkan metriknya, tetapi tidak dihitung dalam penyebut inferensi dan tidak
   dipakai untuk uji tanda.
3. Dua denominator dilaporkan terpisah: semua fold, dan fold layak. Rasio keduanya ditulis, karena
   rata-rata all-fold bisa menipu (EVAL_C EC-3: ssi 3 dari 7 layak berbanding 5 dari 9 all).
4. Bila fold UNDER-POWERED lebih dari 30 persen dari total fold, klaim gate C diturunkan menjadi
   deskriptif.

Dasar angkanya, bukan selera: pada 30 positif dengan p = 0,5, setengah lebar Wilson 0,1685 dengan
batas 0,3315 sampai 0,6685, pada 29 positif 0,1710, pada 20 positif 0,2007, pada 12 positif 0,2462,
pada 3 positif 0,3747. Untuk setengah lebar 0,10 dibutuhkan 93 positif, dan untuk 0,05 dibutuhkan
381 positif. Dengan demikian fold di bawah 30 positif tidak dapat memisahkan B1 0,5 dari batas bawah
0,3315 atau batas atas 0,6685 pada tingkat yang berguna.

Sebaran nyata pada data kita: hyd K-i tidak punya fold di bawah 30 positif (minimum 331), shk tidak
punya fold di bawah 30 positif (minimum tepat 30 di F-9_A), sementara ssi punya 2 fold di bawah 30
(F-7 dengan 3 positif, F-9 dengan 12 positif). Dua finalis pilot karena itu tidak kehilangan fold
karena aturan ini, dan aturan tetap ditulis karena F3 memakai shk yang fold terkecilnya tepat di
batas.

### 6.4 Urutan analisis yang mengikat

1. Periksa resolusi instrumen lebih dulu (syarat 4 x FP dan 14,7555 jam). Fold yang gagal diberi
   status tidak dapat disertifikasi dan keluar dari klaim gate A.
2. Hitung metrik per fold, laporkan semua, termasuk yang jelek.
3. Labeli fold UNDER-POWERED.
4. Jalankan uji keluarga K1 sampai K4, terapkan Holm.
5. Bandingkan dengan baseline pada fold yang sama.
6. Baru susun klaim gate, dengan angka yang sudah dikoreksi.

---

## 7. FALSIFIKASI: APA YANG AKAN MEMBATALKAN KLAIM, DITULIS SEBELUM EKSPERIMEN

Bagian ini adalah bagian yang paling mengikat. Setiap klaim punya syarat batal yang dapat dievaluasi
mesin, dan syarat itu tidak boleh diubah setelah hasil terlihat.

| # | Klaim yang akan diuji | Falsifier yang sudah ditetapkan | Cara evaluasi |
|---|---|---|---|
| P1 | Kalibrasi dalam fold membuat FAR hyd terkendali | lebih dari 2 dari 9 fold tetap memiliki FAR kalender di atas 6, ATAU recall 0 di lebih dari 1 fold | hitung per fold, bandingkan dengan ambang |
| P2 | Kalibrasi dalam fold tidak menghapus alarm | ada fold dengan FAR di bawah 6 tetapi nol alarm benar | hitung TP per fold |
| P3 | Page-Hinkley dengan reset menurunkan FP bengkel | FP per menit di lebih dari 1 alat tidak turun dibanding baseline alat itu | bandingkan per alat, tanpa rata-rata |
| P4 | Page-Hinkley tidak mengorbankan lead | TLead median turun di bawah 20 detik | median TLead per alat |
| P5 | Boosting menaikkan daya pisah shk | delta AUPRC positif di kurang dari 7 dari 9 well | uji tanda, Holm |
| P6 | Boosting tidak merusak gate A | jumlah fold dengan FAR tidak lebih dari 6 turun dari 7 dari 9 | hitung per fold |
| P7 | Hasil tidak bergantung seed | tanda delta berubah pada salah satu dari seed 43 sampai 46 di lebih dari 2 well | jalankan 5 seed |
| P8 | Hasil tidak bergantung artefak | skor per jendela hilang atau tidak lengkap, sehingga McNemar tidak dapat dijalankan | periksa berkas artefak sebelum analisis |
| P9 | Baseline yang dipakai benar | baseline dihitung pada fold berbeda dari finalis | periksa kunci (well, fold) |
| P10 | Gate dihitung dengan satuan yang benar | FAR dilaporkan per menit untuk rig atau per 24 jam untuk bengkel | periksa satuan di keluaran skrip |

Klaim yang bertahan hanya bila TIDAK satu pun falsifier di atas terpenuhi. Falsifier yang tidak dapat
dievaluasi karena artefak hilang menghasilkan status BELUM TERUKUR, bukan lulus.

---

## 8. ATURAN BERHENTI

Mengikuti R6 §4 dan disesuaikan untuk pilot ini, dievaluasi berurutan:

| # | Aturan | Tindakan |
|---|---|---|
| B1 | Resolusi instrumen gagal (`jam_neg` kurang dari 4 x FP, atau kurang dari 14,7555 jam untuk klaim FAR tidak lebih dari 6 dengan 0 FP) | hentikan klaim FAR fold itu, tulis tidak dapat disertifikasi |
| B2 | Unit independen kurang dari 5 | hentikan uji inferensial, turunkan klaim menjadi deskriptif |
| B3 | MDE lebih besar dari efek terkecil yang menarik (FAR kurang dari 29 persen, delta AUPRC kurang dari 0,0192) | hentikan, tulis desain tidak mampu menjawab |
| B4 | Arah delta berbeda antar fold | eksperimen belum selesai, jangan dilaporkan sebagai hasil |
| B5 | Artefak wajib tidak ada (skor per jendela) | hentikan uji berpasangan, status BELUM TERUKUR |
| B6 | Keluarga uji berubah setelah hasil terlihat | uji baru dilaporkan eksploratori |
| B7 | Waktu habis, atau batas 1.320 menit tercapai | tulis dihentikan administratif, status klaim tetap BELUM TERUKUR |
| B8 | Versi pustaka tidak tercatat (`pip_freeze.txt` tidak ada) | run TIDAK BOLEH dimulai (memblokir, §3.2) |

Berhenti karena B1 sampai B6 adalah berhenti karena bukti. Berhenti karena B7 adalah berhenti
administratif, dan dua hal itu wajib ditulis berbeda.

---

## 9. YANG HARUS DISERAHKAN PELAKSANA PILOT

| # | Berkas | Isi minimum |
|---|---|---|
| 1 | `scratch/rnd_e2/pip_freeze.txt` | keluaran `pip freeze` sebelum run |
| 2 | `scratch/rnd_e2/e2_env.json` | versi Python, hash `pip_freeze.txt`, tanggal |
| 3 | `scratch/rnd_e2/skor_<finalis>_<fold>_<seed>.parquet` | skor per jendela |
| 4 | `scratch/rnd_e2/titik_operasi.json` | alpha atau ambang per fold, plus asal pemilihannya |
| 5 | `scratch/rnd_e2/hitungan_berpasangan.csv` | TP, FP, FN per jendela untuk pasangan model |
| 6 | `scratch/rnd_e2/cakupan.json` | menit teramati, menit kalender, fraksi cakupan per fold |
| 7 | `scratch/rnd_e2/HASIL_PILOT.md` | angka per fold, keputusan gate, falsifier yang diperiksa |

Tanpa berkas 1 dan 2, pilot tidak boleh dijalankan. Tanpa berkas 3 dan 5, klaim perbandingan antar
model tidak boleh dibuat, walau AUPRC terlihat lebih tinggi.

---

## 10. LEDGER PROVENANCE

Setiap angka di dokumen ini punya baris di `docs/RND_PROVENANCE_LEDGER.md` bagian
"Bagian E2: protokol pilot tiga kandidat", nomor `E2-001` sampai `E2-056`. Skrip pembangkit sekaligus
verifikator: `scratch/rnd_e2/e2_ledger.py`, yang meng-assert tiap nilai terhadap
`scratch/rnd_e2/e2_final.json`, `e2_stats.json`, `e2_probe.json`, atau JSON primer
`scratch/v9_e_stat/v9_e_stat_03_tool_wear_RESULTS.json`, lalu menolak menulis baris bila assert gagal.
Skrip itu idempoten: bagian lama dibuang sebelum ditulis ulang.

Kelas sumber yang dipakai: `RUN-KITA` untuk hasil eksekusi dan pengukuran berkas, `DERIVASI` untuk
angka yang lahir dari rumus, `KONVENSI` untuk ambang yang ditetapkan dokumen ini, `JURNAL` untuk
metode yang disandarkan pada rujukan terverifikasi, `BELUM-TERUKUR` untuk yang memang tidak dapat
diukur sekarang.

---

## 11. RUJUKAN

Status verifikasi: dua lapis. Lapis registrasi `https://doi.org/<doi>` TANPA mengikuti redirect
(301 atau 302 berarti terdaftar), lapis metadata `https://api.crossref.org/works/<doi>` (200 dengan
judul, penulis pertama, dan tahun yang cocok). Lapis akses penerbit tidak dipakai sebagai bukti.
Hasil mentah: `scratch/rnd_e2/e2_doi.json`, tanggal akses 2026-10-27.

| # | Penulis pertama, tahun | Judul | Wadah | DOI atau URL | Status |
|---|---|---|---|---|---|
| 1 | Varma, 2006 | Bias in error estimation when using cross-validation for model selection | BMC Bioinformatics 7:91 | 10.1186/1471-2105-7-91 | TERVERIFIKASI (302, Crossref 200, Varma 2006) |
| 2 | Roberts, 2017 | Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure | Ecography 40:913-929 | 10.1111/ecog.02881 | TERVERIFIKASI (302, 200, Roberts 2017) |
| 3 | Bergmeir, 2012 | On the use of cross-validation for time series predictor evaluation | Information Sciences 191:192-213 | 10.1016/j.ins.2011.12.028 | TERVERIFIKASI (302, 200, Bergmeir 2012) |
| 4 | Cerqueira, 2020 | Evaluating time series forecasting models: an empirical study on performance estimation methods | Machine Learning 109:1997-2037 | 10.1007/s10994-020-05910-7 | TERVERIFIKASI (302, 200, Cerqueira 2020) |
| 5 | Varoquaux, 2018 | Cross-validation failure: small sample sizes lead to large error bars | NeuroImage 180:68-77 | 10.1016/j.neuroimage.2017.06.061 | TERVERIFIKASI (302, 200, Varoquaux 2018) |
| 6 | Cawley, 2010 | On over-fitting in model selection and subsequent selection bias in performance evaluation | JMLR 11:2079-2107 | https://www.jmlr.org/papers/v11/cawley10a.html | TERVERIFIKASI (HTTP 200, judul cocok) |
| 7 | Vovk, 2005 | Algorithmic Learning in a Random World | Springer | 10.1007/b106715 | TERVERIFIKASI (302, 200, judul cocok; medan penulis kosong pada catatan Crossref karena buku) |
| 8 | Lei, 2018 | Distribution-Free Predictive Inference for Regression | JASA 113:1094-1111 | 10.1080/01621459.2017.1307116 | TERVERIFIKASI (302, 200, Lei 2018) |
| 9 | Barber, 2023 | Conformal prediction beyond exchangeability | Annals of Statistics 51:816-845 | 10.1214/23-AOS2276 | TERVERIFIKASI (302, 200, Barber 2023) |
| 10 | Page, 1954 | Continuous Inspection Schemes | Biometrika 41:100-115 | 10.1093/biomet/41.1-2.100 | TERVERIFIKASI (302, 200, PAGE 1954) |
| 11 | DeLong, 1988 | Comparing the areas under two or more correlated ROC curves | Biometrics 44:837-845 | 10.2307/2531595 | TERVERIFIKASI (302, 200) |
| 12 | Efron, 1979 | Bootstrap methods: another look at the jackknife | Annals of Statistics 7:1-26 | 10.1214/aos/1176344552 | TERVERIFIKASI (302, 200) |
| 13 | Benjamini, 1995 | Controlling the false discovery rate | JRSS-B 57:289-300 | 10.1111/j.2517-6161.1995.tb02031.x | TERVERIFIKASI (302, Crossref 200) |
| 14 | Wilson, 1927 | Probable inference, the law of succession, and statistical inference | JASA 22:209-212 | 10.1080/01621459.1927.10502953 | TERVERIFIKASI (302, 200) |
| 15 | Boyd, 2013 | Area under the precision-recall curve: point estimates and confidence intervals | LNCS 8190:451-466 | 10.1007/978-3-642-40994-3_29 | TERVERIFIKASI (302, 200) |
| 16 | Saito, 2015 | The precision-recall plot is more informative than the ROC plot | PLOS ONE 10:e0118432 | 10.1371/journal.pone.0118432 | TERVERIFIKASI (302, 200) |
| 17 | Lakens, 2022 | Sample Size Justification | Collabra: Psychology 8 | 10.1525/collabra.33267 | TERVERIFIKASI (302, Crossref 200) |
| 18 | Angelopoulos, 2021 | A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification | arXiv | https://arxiv.org/abs/2107.07511 | TERVERIFIKASI (HTTP 200, judul cocok) |
| 19 | Pineau, 2021 | Improving Reproducibility in Machine Learning Research | JMLR 22:1-20 | https://www.jmlr.org/papers/v22/20-303.html | TERVERIFIKASI (HTTP 200, judul cocok) |
| 20 | Holm, 1979 | A simple sequentially rejective multiple test procedure | Scandinavian Journal of Statistics 6:65-70 | 10.2307/4615733 | BELUM TERVERIFIKASI (doi.org 404, Crossref 404); TIDAK dipakai sebagai dasar rekomendasi |

Pemakaian rujukan. Nomor 1 sampai 6 mendasari desain bersarang dan pembatasan CV pada data
terstruktur. Nomor 7 sampai 9 mendasari conformal dan batasnya ketika pertukaran tidak berlaku
(well berbeda, bukan sampel acak). Nomor 10 mendasari Page-Hinkley. Nomor 11 sampai 17 mendasari
pilihan uji dan selang. Nomor 18 dan 19 dipakai sebagai penunjuk praktik, bukan dasar klaim.
Nomor 20 tidak dipakai: koreksi Holm dijalankan lewat implementasi `statsmodels` yang diuji langsung
pada data, bukan bersandar pada rujukan yang tidak dapat dibuka.

---

## 12. RINGKASAN 5 BARIS

1. Protokol mengunci unit independen sebagai well (9) dan alat (4), split leave-one-well-out dengan titik operasi dipilih hanya di 8 fold dalam, seed 42 ditambah 43 sampai 46, dan runtime maksimum 1.320 menit untuk 110 fold-run.
2. Tiga finalis dengan kriteria angka yang dapat dievaluasi mesin: hid conformal butuh FAR kalender tidak lebih dari 6 di minimal 7 dari 9 fold dengan recall minimal 0,50, tool_wear Page-Hinkley butuh FP tidak lebih dari 1 per menit di keempat alat dengan TLead median minimal 20 detik, dan shk boosting butuh delta AUPRC positif di minimal 8 dari 9 well tanpa menurunkan jumlah fold FAR tidak lebih dari 6.
3. Gate C dihitung dengan dispersi antar fold, uji tanda (8 dari 9 pada hyd dan shk, dan DILARANG pada 4 alat karena daya nol), CI lawan prevalensi, dan kestabilan 5 seed; gate A dihitung sebagai laju kalender dengan Garwood dan syarat resolusi 4 x FP serta 14,7555 jam untuk klaim FAR tidak lebih dari 6 dengan 0 FP; gate B dihitung sebagai alarm per shift dan presisi pada titik operasi yang dipatok sebelum run.
4. Temuan terukur yang mengubah kriteria: pada titik operasi terkalibrasi 1 FP per menit, laju segmen evaluasi tool_wear adalah 1,43, 1,43, 4,50, dan 5,14 per menit sehingga 0 dari 4 alat lulus gate A bengkel, dan mengetatkan target ke 0,2 FP per menit tidak menurunkan FP sama sekali karena ambang terkuantisasi.
5. Sepuluh falsifier ditulis sebelum eksperimen berjalan, fold di bawah 30 positif dikeluarkan dari inferensi (setengah lebar Wilson pada 30 positif masih 0,1685), dan run diblokir bila versi pustaka tidak tercatat, karena di host ini numpy sampai pyarrow tidak terpasang sehingga versi pilot masih BELUM TERUKUR.

## 13. DAFTAR YANG BELUM TERVERIFIKASI

1. Versi pustaka pilot (numpy, pandas, scikit-learn, scipy, statsmodels, LightGBM, XGBoost, CatBoost): BELUM TERUKUR, karena tidak satu pun terpasang pada interpreter host ini (Python 3.14.9 tanpa pip). Protokol memblokir run tanpa tangkapan `pip freeze`.
2. Biaya latih LightGBM, XGBoost, dan CatBoost pada data kita: BELUM TERUKUR, sehingga angka 12 menit per fold adalah KONVENSI, bukan hasil ukur.
3. FAR dan recall finalis setelah kalibrasi bersarang: BELUM TERUKUR, karena pilot belum dijalankan. Seluruh kriteria sukses di §4 adalah ambang keputusan, bukan hasil.
4. Kestabilan lintas seed 43 sampai 46: BELUM DIJALANKAN; semua hasil V9 memakai seed 42.
5. DeLong dan McNemar pada data nyata: BELUM TERUKUR karena skor per jendela belum pernah disimpan.
6. Transfer hasil bengkel ke rig: TIDAK DIKLAIM dan belum diuji.
7. Rujukan Holm 1979: BELUM TERVERIFIKASI (doi.org 404, Crossref 404), sehingga tidak dipakai sebagai dasar rekomendasi.
8. Label tool_wear sebagai perubahan regime: definisinya masih mengikuti deskripsi dataset dan kampanye V8/V9, dan belum ada anotasi independen. Pemetaan label ini belum diuji ulang pada run ini.
9. Ambang 3 alarm per shift dan asumsi 10 menit per pemeriksaan: KONVENSI dokumen ini, belum divalidasi dengan data beban kerja nyata.
10. Cakupan waktu minimum 50 persen sebagai syarat sertifikasi: KONVENSI, dipilih dari sebaran cakupan terukur 1,46 sampai 71,7 persen, bukan hasil optimasi.
