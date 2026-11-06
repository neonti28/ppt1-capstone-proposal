# V6-E1 — Pra-Registrasi: Klasifikasi ≥3 Kriteria Kerusakan dari Data NYATA Volve

Dokumen ini DITULIS SEBELUM hasil model apa pun dihitung. SHA-256 file ini dicatat di
komentar kartu `t_5e052df1` sebelum skrip training dijalankan, dan diverifikasi ulang oleh
verifier terhadap hash yang terekam. Gate, fitur, model, metrik, dan protokol di bawah TIDAK
BOLEH berubah setelah hasil diketahui (protokol riset tim `PROTOCOL_RISET_TIM.md`).
Gagal = dicatat jujur, bukan digeser.

Tanggal penulisan: 2026-10-10 (WIB), kartu `t_5e052df1` (run 12).

> **Riset pendahuluan: `scikit-learn`** — seed=42 di semua estimator; imputer/scaler di-*fit*
> hanya pada fold latih (Pipeline per fold, tidak ada preprocessing global); RF dan
> LogisticRegression keduanya dideklarasikan di sini sebelum hasil; `class_weight="balanced"`
> dipilih karena kelas langka (prevalensi 0,5%–14%), tanpa resampling/SMOTE (resampling
> mengubah prevalensi dan membatalkan interpretasi AUPRC vs prevalensi).
> **Riset pendahuluan: `experimental-design`** — unit analisis = jendela 10 menit; sumur =
> kelompok (cluster). Window berturut-turut dalam satu sumur adalah pengukuran berulang pada
> unit yang sama → pembagian latih/uji WAJIB Leave-One-Well-Out (LOWO), tidak pernah split
> acak antar window, untuk mencegah pseudoreplication dan kebocoran antar-sumur. Semua fitur
> berasal dari jendela lampau, label dari jendela depan (tanpa tumpang tindih waktu).
> **Riset pendahuluan: `statistical-analysis`** — metrik primer AUPRC (kelas tidak seimbang);
> gate ditetapkan di sini sebelum hasil (confirmatory); eksplorasi lain dilabeli eksploratif;
> CI95 AUPRC memakai moving-block bootstrap (blok 60 jendela, 1.000 resample, seed 42) karena
> jendela dalam satu sumur bergantung waktu (autokorelasi) — bukan bootstrap i.i.d. yang
> akan melapiskan CI terlalu sempit.
> **Riset pendahuluan: `statistical-power`** — kesimpulan per-sumur hanya ditarik bila sumur
> uji punya ≥30 jendela positif (di bawah itu = UNDERPOWERED, dilaporkan terpisah, tidak
> dihitung dalam gate mayoritas). Sensitivitas dilaporkan lebar CI bootstrap AUPRC, bukan
> post-hoc/observed power (yang melingkar dan tidak informatif). Pemetaan: prevalensi 1% di
> 1.000 jendela uji → AUPRC canary ≈ 0,01; klaim "berhasil" menuntut lift ≥1,5 di atas
> angka itu, sehingga makin langka kelasnya, makin besar jumlah jendela yang dibutuhkan.
> **Riset pendahuluan: `shap`** — SHAP bersifat deskriptif perilaku model (bukan kausal),
> dihitung pada sampel jendela uji OOF dengan latar belakang dari fold latih, output yang
> dijelaskan = probabilitas kelas positif, additivity diperiksa; tidak dipakai untuk mengubah
> gate atau memilih model.

---

## 1. Pertanyaan dan hipotesis

**Pertanyaan:** apakah dari 11 kanal sensor PERMUKAAN (torsi, tekanan, flow, RPM, WOB,
hookload, ROP, block position, pompa, kedalaman) pada 10 menit lampau, model klasifikasi dapat
memprediksi terjadinya ≥3 kriteria kerusakan drilling yang BERBEDA secara fisik pada 10 menit
berikutnya, pada sumur yang TAK PERNAH dilihat saat training (LOWO), lebih baik daripada
prevalensi dan daripada canary kedalaman?

**H₁ (pra-registrasi, per kelas):** RF pada fitur jendela permukaan mencapai lift
(AUPRC ÷ prevalensi) ≥ 1,5 pada MAJORITAS sumur uji yang layak dinilai, DAN AUPRC RF ≥
AUPRC canary-kedalaman pada mayoritas sumur uji itu.

**H₀:** salah satu syarat tidak terpenuhi → kelas itu dinyatakan LEMAH (jujur, dilaporkan
per kelas, tidak digabung jadi klaim tunggal).

---

## 2. Data (semua NYATA, hasil eksekusi sebelum pra-registrasi)

- Sumber: 7 CSV hasil parser WITSML Volve `data/volve/witsml_parsed/` (F-14, F-15A, F-15_S,
  F-5, F-7, F-9, F-9_A) — total 6.961.468 baris; agregat per-menit di
  `scratch/v6_e1/bins/*.csv.gz` (skrip `code/v6_e1_10_bins.py`); jendela di
  `scratch/v6_e1/windows/*.csv.gz` (skrip `code/v6_e1_20_windows.py`).
- **Jumlah sampel kelas NYATA per sumur (dihitung sebelum pra-registrasi, dari
  `scratch/v6_e1/ch20_windows_summary.json`)** — jendela eligible = label teramati DAN
  jendela fitur valid (≥5 dari 10 bin berisi baris pengeboran, ≥60 baris pengeboran):

| Sumur | stuck pos/n (prev) | vib pos/n (prev) | shk pos/n (prev) | ssi pos/n (prev) |
|---|---|---|---|---|
| F-14   | 432 / 3.201 (13,5%) | 1.124 / 1.989 (56,5%) | 760 / 11.205 (6,8%) | 75 / 5.455 (1,4%) |
| F-15A  | — (kanal tak ada) | 1.543 / 6.482 (23,8%) | 41 / 6.484 (0,6%) | 31 / 6.020 (0,5%) |
| F-15_S | — (kanal tak ada) | 1.532 / 10.903 (14,1%) | 259 / 11.394 (2,3%) | 85 / 5.342 (1,6%) |
| F-5    | — (kanal tak ada) | 1.230 / 4.548 (27,0%) | 240 / 7.140 (3,4%) | 102 / 4.714 (2,2%) |
| F-7    | — (kanal tak ada) | — (0 jendela; kanal tak teramati saat pengeboran) | 267 / 2.761 (9,7%) | 3 / 982 (0,3%) |
| F-9    | 0 eligible (1.159 label valid, 0 punya jendela fitur pengeboran — lihat §7) | 0 eligible (1.270 label valid, 0 jendela fitur pengeboran) | 45 / 1.851 (2,4%) | 12 / 1.126 (1,1%) |
| F-9_A  | 1.575 / 2.354 (66,9%) | — (kanal tak ada) | 30 / 2.356 (1,3%) | 55 / 841 (6,5%) |
| **Total** | **2.007 / 5.555** | **5.429 / 23.922** | **1.642 / 43.191** | **363 / 24.480** |

- Populasi baris mentah (kanal, sebelum agregat; dari `scratch/v6_e1/ch02_label_counts.json`):
  STUCK_RT nonzero: F-14 394 / F-9 381 / F-9_A 22.590; VIBLAT_RT nonzero: F-14 2.234 /
  F-15A 42.804 / F-15_S 136.666 / F-5 40.277 / F-9 5.853; SHKRSK_RT nonzero ≥1: 180/12/300/82/
  176/146/40 (urutan F-14, F-15A, F-15_S, F-5, F-7, F-9, F-9_A); CRPM_RT nonnull: 23.110 /
  50.413 / 137.170 / 46.529 / 2.769 / 9.875 / 15.184.

---

## 3. Kelas kerusakan (dikunci — 4 kelas fisik berbeda, bukan tingkatan satu jenis)

| ID | Kelas | Rumus/sumber label | Sumber sinyal | Aksi perbaikan berbeda? |
|---|---|---|---|---|
| `stuck` | Stuck pipe / differential sticking | `STUCK_RT ≥ 1` di jendela label (kanal instrumen) | downhole/riser flag | ya — free point, jaring, pull |
| `vib` | Whirl / getaran lateral BHA | `VIBLAT_RT ≥ 32,17405 ft/s²` (ambang absolut R1 §4.2 = P75 F-14; BUKAN P75 per-well yang memaksa prevalensi 25%) | MWD downhole | ya — ubah RPM/WOB, stabilisator |
| `shk` | Bit bounce / getaran aksial | `SHKRSK_RT ≥ 1` (MWD Shock Risk 0–3) | MWD downhole | ya — ubah RPM/WOB, bit |
| `ssi` | Stick-slip torsional | `SSI = (CRPM_max − CRPM_min)/(2·CRPM_mean) ≥ 1` pada jendela label, min 10 sampel CRPM (Liu 2025 *Thermal Science*; grading R1 §2.1 no.3) | MWD collar RPM downhole | ya — soft torque, RPM/DOE |

Keterbukaan: keempat label diambil dari kanal DOWNHOLE (bukan dari fitur permukaan) → label
bukan fungsi deterministik dari fitur. Tumpang tindih waktu nol: fitur = bin `[t0−10, t0)`,
label = bin `[t0, t0+10)` (agregat menit, grid 60 detik).

Kelas yang TIDAK dipakai (dideklarasikan di sini, bukan disembunyikan):
- `WHIRL_RT`/`BOUNCE_RT` — duplikat baris-ke-baris (D0 §2.5) → hanya `vib` dari `VIBLAT_RT`.
- `STKSLP` kode pabrikan — semantik tak terdokumentasi, dan 98,7% non-nol di F-15_S.
- EDM event/NPT — terbukti BUKAN database event (D0 §2.2).
- Severe stick-slip (SSI ≥ 3) — populasi sangat kecil; tidak dijadikan kelas terpisah.
- kelas ke-5 hidraulik dari residual SPP vs flow — TIDAK dipakai karena SPPA/TFLO adalah
  fitur (sirkularitas: label akan menjadi fungsi hampir deterministik dari fitur).

---

## 4. Fitur (dikunci)

11 kanal permukaan/depth: `TQA, SPPA, TFLO, RPM, SWOB, HKLD, ROP, BPOS, SPM (total stroke),
depth_mean (DMEA), dbtm_mean (DBTM)`. Per kanal 5 statistik atas 10 bin jendela lampau:
`mean` (terbobot baris pengeboran), `std` (terpool), `slope` (OLS terhadap offset menit),
`last`, `frac` (fraksi bin terisi) → **55 fitur**.

- Kolom `feat_drill_bins`, `feat_drill_rows` DILARANG masuk fitur (hanya syarat kelayakan;
  kalau masuk, model bisa belajar pola ketersediaan data, bukan fisika — shortcut).
- Kolom label, `y_prev_*`, `ssi_val` DILARANG masuk fitur (asersi di skrip).
- Missing value: imputasi median, di-fit HANYA pada fold latih (Pipeline).
- Kanal duplikat tidak dipakai (tidak ada WHIRL/BOUNCE di fitur).

## 5. Jendela & kelayakan (dikunci)

- Grid 60 detik. Anchor `t0` = awal jendela label. FITUR `[t0−10, t0)`; LABEL `[t0, t0+10)`.
- Jendela fitur valid: ≥5 dari 10 bin memiliki baris pengeboran (`RPM>0 & SWOB>0`) DAN
  ≥60 baris pengeboran terakumulasi.
- Kelayakan per kelas: jendela fitur valid DAN kanal label teramati di jendela label
  (`stuck`/`vib`/`shk`: ≥1 sampel non-null; `ssi`: ≥10 sampel CRPM dan mean > 0).
- Jendela dengan label TIDAK teramati TIDAK dihitung negatif (filter ≠ nol; kelas hanya
  dinilai di atas observasi nyata).

## 6. Model, evaluasi, gate (dikunci)

- **Model primer:** `RandomForestClassifier(n_estimators=300, min_samples_leaf=5,
  class_weight="balanced_subsample", random_state=42, n_jobs=-1)` dalam Pipeline bersama
  `SimpleImputer(median)`.
- **Model sekunder:** `LogisticRegression(class_weight="balanced", max_iter=1000)` dalam
  Pipeline `SimpleImputer(median) → StandardScaler → LogReg` (scaling hanya di fold latih).
- **Canary A:** prevalensi kelas (AUPRC canary = prevalensi; lift ≡ 1,0 per definisi).
- **Canary B (kedalaman):** RF dengan parameter sama, HANYA memakai fitur depth/dbtm
  (`*_mean/_std/_slope/_last/_frac` dari `depth`+`dbtm`, 10 fitur) — mendeteksi sinyal yang
  sebenarnya berasal dari formasi/ke kedalaman, bukan dari sensor proses.
- **Baseline persistence:** skor = label jendela sebelumnya (`y_prev_<kelas>`), dihitung hanya
  pada jendela yang punya `valid_prev` — mengikuti pelajaran V5-J2 (persistence bisa
  mengalahkan model pada label berblok panjang). Kehadiran persistence wajib dilaporkan.
- **Split:** LOWO per kelas. Fold = satu sumur uji. Tidak ada window dari sumur uji di
  data latih. Tidak ada shuffle lintas sumur.
- **Metrik per fold:** AUPRC (primer), prevalensi, lift = AUPRC/prevalensi, ROC-AUC
  (sekunder), CI95 AUPRC (moving-block bootstrap, blok 60 jendela, 1.000 resample, seed 42).
- **Layak dinilai (per sumur uji):** ≥30 jendela positif di sumur uji. Di bawah itu →
  UNDERPOWERED, dilaporkan terpisah, tidak dihitung dalam penentuan mayoritas.
- **GATE per kelas:**
  - **G1:** lift RF ≥ 1,5 pada MAJORITAS sumur uji yang layak dinilai.
  - **G2:** AUPRC RF ≥ AUPRC canary-B (kedalaman) pada mayoritas sumur uji yang layak dinilai.
  - Kedua gate lolos → kelas LULUS; salah satu gagal → kelas LEMAH (disebut per kelas,
    per sumur, dengan angkanya).
- **Gate gabungan tugas:** ≥3 kelas LULUS → klaim "≥3 kriteria kerusakan" terpenuhi dengan
  bukti angka. Jika <3 → klaim TIDAK terpenuhi, disampaikan apa adanya.
- **Catatan wajib:** jika persistence mengalahkan RF di mayoritas sumur suatu kelas, kelas itu
  tetap LULUS/LEMAH menurut G1/G2 tetapi verdict akhir DITURUNKAN menjadi "layak bersyarat"
  (mengikuti temuan audit V5-J2), dan ini disebut eksplisit.

## 7. Kelemahan yang SUDAH diketahui saat pra-registrasi (jujur di muka)

1. **`stuck` hanya punya 2 sumur eligible** (F-14, F-9_A) → LOWO hanya 2 fold, klaim
   lintas-sumur lemah secara struktural; F-9_A sendiri 66,9% positif (blok label panjang,
   V5-J2 sudah memperingatkan persistence).
2. **F-9: 1.159 jendela label `stuck` dan 1.270 label `vib` teramati tetapi 0 punya jendela
   fitur pengeboran** (median baris pengeboran di jendela fitur = 0) → sumur ini gugur dari
   dua kelas itu karena di jendela itu memang tidak sedang pengeboran (RPM/SWOB nol). Ini
   keadaan data, bukan pilihan; dilaporkan, tidak disetel ulang.
3. **`ssi` sangat langka** di F-15A (0,5%), F-7 (0,3%) → fold itu kemungkinan UNDERPOWERED.
4. **`shk` langka** di F-15A (0,6%) dan F-9_A (1,3%) → sama.
5. **Semantik `STUCK_RT` kode 0/1/2/3 tidak terdokumentasi** (V5-J2: deskripsi kurva kosong,
   konfirmasi naratif DDR = 0) → kelas `stuck` = flag instrumen, BUKAN kejadian stuck-pipe
   fisik yang terverifikasi naratif.
6. **Agregat menit kehilangan variasi sub-menit** (desain sadar: hemat memori 3,2 GB CSV;
   konsekuensi: statistik window = statistik agregat, bukan sampel mentah).
7. **CDM/gap:** F-1 C + F-11 (54,6% file log) belum diparse (D1e) → tidak masuk LOWO;
   menjadi peluang perluasan, bukan bagian klaim.

## 8. Protokol eksekusi

1. Skrip: `code/v6_e1_30_lowo.py` (training + evaluasi) → JSON hasil
   `scratch/v6_e1/E1_LOWO_RESULTS.json` + log run.
2. SHAP: `code/v6_e1_40_shap.py` — TreeExplainer, sampel 200 jendela uji per kelas
   (seed 42), latar 200 baris latih, cek additivity `|base+Σ−pred| < 1e−5`.
3. Semua angka hasil ditulis apa adanya; kegagalan gate dilaporkan per kelas.
4. Dokumen final: `docs/V6_E1_ML_DESIGN.md` memuat pra-registrasi ini + hasil run nyata +
   kelemahan jujur.
