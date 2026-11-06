# V6-E1 — RANCANGAN + BASELINE ML ≥3 KRITERIA KERUSAKAN DARI DATA NYATA

Task: `t_5e052df1` [ML Eng] · Board: capstone-v6-solve · Tanggal: 2026-10-10 (WIB)
Status: 4 kampanye pra-registrasi dieksekusi penuh dengan angka LOWO nyata.

> **Riset pendahuluan: `scikit-learn`** — semua baseline memakai Pipeline RF
> (`n_estimators=300, min_samples_leaf=5, class_weight=balanced_subsample, seed=42`) +
> LogisticRegression sekunder; imputer median/scaler di-fit HANYA di dalam fold latih;
> tanpa resampling/SMOTE (resampling membatalkan interpretasi AUPRC vs prevalensi);
> tanpa tuning hyperparameter setelah hasil diketahui.
> **Riset pendahuluan: `experimental-design`** — unit = jendela; sumur/alat = cluster;
> seluruh evaluasi Leave-One-Well-Out / Leave-One-Tool-Out (tidak pernah split acak antar
> jendela → anti-pseudoreplication & anti-leak); fitur selalu dari jendela LAMPAU, label
> dari jendela DEPAN atau dari kanal sumber berbeda (non-sirkular); 4 pra-registrasi
> di-hash sebelum training masing-masing kampanye.
> **Riset pendahuluan: `statistical-analysis`** — metrik primer AUPRC + lift (AUPRC/prev)
> karena kelas tidak seimbang; CI95 = moving-block bootstrap (blok 60/20/10 jendela,
> 1.000 resample, seed 42) karena jendela bergantung waktu; baseline persistence &
> canary dilaporkan; kegagalan gate dilaporkan per kelas, tidak digabung.
> **Riset pendahuluan: `statistical-power`** — sumur uji dengan <30 jendela positif =
> UNDERPOWERED, dikecualikan dari gate mayoritas (F-7 ssi 3 pos, F-9 ssi 12 pos, F-9_A/F-7/F-9
> bit_wear); sensitivitas dilaporkan lebar CI bootstrap, bukan observed power.
> **Riset pendahuluan: `shap`** — TreeExplainer deskriptif pada fold uji terbesar per kelas,
> background 200 baris latih (seed 42), output P(positif), additivity diverifikasi;
> tidak mengubah gate.

---

## 1. Keputusan sumber data (berdasarkan bukti 8 pembaca + D2 + R1)

Dibaca dulu: `docs/V6_D0_READERS_SYNTHESIS.md` (peta lintas-sumber), 8 dokumen D1a–D1h,
`docs/V6_D2_EXTERNAL_DATASETS.md`, `docs/V6_R1_SCIENCE.md`, `docs/V4_MAINTENANCE_ML_OPTIONS.md`
+ V5_* (kegagalan lama tidak diulang).

Keputusan: **Volve gabungan (WITSML terparse 7 sumur + USROP 7 sumur) sebagai inti,
2 dataset eksternal NYATA dipakai sebagai kampanye terpisah** (bukan digabung baris-per-baris):

- **Label EDM DITOLKAN** (D0 §2.2: bukan database event — keyword non-productive 0 hit,
  stuck 947 = atribut simulasi torque-drag) → tidak dipakai sebagai label.
- **Label instrumen downhole** (D0 §3 rank 1–2) → kelas `stuck`, `vib`, `shk`, `ssi`.
- **Label USROP tersimpan** (`high_MSE_bit_wear`, rumus Teale terverifikasi R1 run-3) →
  kelas `bit_wear` (Volve, horizontalkedalaman).
- **Label turunan R1** (residual SPPA vs aliran, sudah diuji di F-14) → kelas `hyd`.
- **Eksternal**: Mendeley `th4yv974r2` tool wear (CC BY 4.0, SHA-256 API 8/8 cocok) →
  kelas `tool_wear`. Kaggle XAI DITOLKAN (sintetis, melanggar mandat "data nyata").

## 2. Tujuh kelas terdefinisi + jumlah sampel NYATA (sebelum training)

| # | Kelas (kerusakan fisik) | Sumber label | Jumlah sampel nyata (jendela eligible / positif) | Sumbang untuk |
|---|---|---|---|---|
| 1 | `stuck` — stuck pipe / contact string-borehole | kanal instrumen `STUCK_RT ≥1` (WITSML) | F-14 **3.201/432**; F-9_A **2.354/1.575** (F-9: 1.159 label valid tapi 0 jendela fitur pengeboran) | Volve |
| 2 | `vib` — whirl / getaran lateral BHA | `VIBLAT_RT ≥32,17405 ft/s²` (ambang absolut R1 §4.2) | F-14 **1.989/1.124**; F-15A **6.482/1.543**; F-15_S **10.903/1.532**; F-5 **4.548/1.230** | Volve |
| 3 | `shk` — bit bounce / getaran aksial | `SHKRSK_RT ≥1` (MWD Shock Risk) | 7 sumur: F-14 **11.205/760**; F-15A **6.484/41**; F-15_S **11.394/259**; F-5 **7.140/240**; F-7 **2.761/267**; F-9 **1.851/45**; F-9_A **2.356/30** | Volve |
| 4 | `ssi` — stick-slip torsional | `SSI(CRPM_RT)≥1`, SSI=(max−min)/(2·mean), min 10 sampel (Liu 2025; R1 §2.1) | F-14 **5.455/75**; F-15A **6.020/31**; F-15_S **5.342/85**; F-5 **4.714/102**; F-7 **982/3**; F-9 **1.126/12**; F-9_A **841/55** | Volve |
| 5 | `hyd` — anomali hidrolik/pompa | rumus R1 §4.2 #7 (qcut TFLO 10 → median/MAD SPPA → \|z\|>2), jendela ≥50% bin anomali | 7 sumur: **37.548 jendela / 4.352 positif** (per sumur 1.616–10.401, prev 8,3–26,2%) | Volve |
| 6 | `bit_wear` — keausan bit/inefisiensi (proxy Teale MSE) | kolom `label=high_MSE_bit_wear` di `USROP_labeled.csv` (rumus terverifikasi R1 run-3) | 7 sumur **3.953/984**; 4 layak dinilai (F-14 949/91, F-15 1.057/155, F-15S 1.031/561, F-5 367/174) | Volve |
| 7 | `tool_wear` — keausan mata bor (terukur) | label primer eksperimen Mendeley: R01=baru, R02=tumpul (kutipan deskripsi dataset) | **469 jendela / 240 pos**; 4 alat × 2 run; SHA-256 file 8/8 cocok API | **eksternal** |

Kelas yang TIDAK dipakai (dinyatakan, bukan disembunyikan): `WHIRL_RT`/`BOUNCE_RT`
(duplikat baris-ke-baris, D0 §2.5), kode `STKSLP` pabrikan (semantik tak terdokumentasi,
nonzero 98,7% di F-15_S), EDM event (bukan event DB), severe SSI≥3 (populasi ~0 di F-14),
hidraulik-vs-fitur SPPA/TFLO kanan → kelas `hyd` dijalankan dengan SPPA/TFLO/SPM
DIKECUALIKAN dari fitur (anti-sirkular).

## 3. Pra-registrasi (ditulis & di-hash SEBELUM training — bukti di komentar kartu)

| Kampanye | Dokumen | SHA-256 | Isi kunci |
|---|---|---|---|
| E1a | `docs/V6_E1_PREREG.md` | `542772622d2d3539df35f484fa0a67869d485a3ff6944fab5fbd45252928e9fc` | 4 kelas; LOWO; gate G1 lift≥1,5 mayoritas + G2 RF≥canary-kedalaman; <30 pos = UNDERPOWERED |
| E1b | `docs/V6_E1b_PREREG_HYD.md` | `411366bec820d9978623a43418daaa0d123ecd397f398961f56ab19a2c912152` | kelas `hyd`; fitur 8 channel tanpa SPPA/TFLO/SPM; gate identik |
| E1c | `docs/V6_E1c_PREREG_TOOLWEAR.md` | `e2179bdeef64bcf01d71b50d8354008858c0fd9fea3b272af56a76c7dc86550b` | kelas `tool_wear`; Leave-One-Tool-Out 4 fold; canary = 3 RMS |
| E1d | `docs/V6_E1d_PREREG_BITWEAR.md` | `986f45a1fbf866434e05b3aecfbc8c53fa1672e2caef98d7470a38ea8c03f1a6` | kelas `bit_wear`; kanal pembentuk MSE dilarang dari fitur; 4 fold layak dinilai; **upaya terakhir** |

Anti-sirkularitas di setiap kampanye: (a) label dari kanal/sumber yang BUKAN fitur;
(b) fitur selalu jendela lampau, label jendela depan (E1a/E1b/E1d) atau label fisik
terukur (E1c); (c) asersi di skrip menolak kolom label/eligibility/kanal terlarang masuk
daftar fitur (semua asersi PASS di log).

## 4. Hasil LOWO NYATA (semua angka dari eksekusi; log: `scratch/v6_e1/E1*_RUN_LOG.txt`)

### 4.1 `vib` — **LULUS** (G1 4/4, G2 4/4)

| Sumur uji | n / pos / prev | AUPRC RF [CI95] | lift | canary-kedalaman | logreg | persistence |
|---|---|---|---|---|---|---|
| F-14 | 1.989 / 1.124 / 0,565 | **0,912** [0,821; 0,961] | 1,61 | 0,612 | 0,875 | 0,796 |
| F-15A | 6.482 / 1.543 / 0,238 | **0,562** [0,397; 0,683] | 2,36 | 0,458 | 0,647 | 0,547 |
| F-15_S | 10.903 / 1.532 / 0,141 | **0,491** [0,338; 0,619] | 3,50 | 0,277 | 0,184 | 0,517 |
| F-5 | 4.548 / 1.230 / 0,270 | **0,441** [0,341; 0,553] | 1,63 | 0,309 | 0,661 | 0,667 |

Persistence mengalahkan RF di 2/4 fold (tidak mayoritas → tidak menurunkan verdict;
dicatat sebagai batasan: sebagian sinyal berasal dari label yang membentuk blok).

### 4.2 `ssi` — **LULUS** (G1 4/5 fold layak, G2 5/5; persistence 0/5 — model TIDAK dikalahkan persistence)

| Sumur uji | n / pos / prev | AUPRC RF [CI95] | lift | canary-kedalaman |
|---|---|---|---|---|
| F-14 | 5.455 / 75 / 0,0137 | **0,0358** [0,0096; 0,0797] | 2,61 | 0,0256 |
| F-15A | 6.020 / 31 / 0,0051 | **0,0185** [0,0043; 0,0634] | 3,59 | 0,0055 |
| F-15_S | 5.342 / 85 / 0,0159 | **0,1057** [0,0387; 0,2423] | 6,64 | 0,0221 |
| F-5 | 4.714 / 102 / 0,0216 | **0,0810** [0,0305; 0,1874] | 3,74 | 0,0676 |
| F-9_A | 841 / 55 / 0,0654 | **0,0961** [0,0297; 0,1901] | 1,47 ✗ | 0,0593 |

UNDERPOWERED (tidak dihitung): F-7 (3 positif, lift 134 — angka tak bermakna), F-9 (12 positif).

### 4.3 `bit_wear` (USROP) — **LAYAK BERSYARAT** (G1 3/4, G2 4/4; TAPI persistence > RF di 4/4 → diturunkan aturan pra-reg E1a §6)

| Sumur uji | n / pos / prev | AUPRC RF [CI95] | lift | canary-kedalaman | persistence |
|---|---|---|---|---|---|
| F-14 | 949 / 91 / 0,0959 | **0,298** [0,148; 0,517] | 3,11 | 0,191 | 0,679 |
| F-15 | 1.057 / 155 / 0,1466 | **0,365** [0,171; 0,582] | 2,49 | 0,288 | 0,698 |
| F-15S | 1.031 / 561 / 0,5441 | **0,813** [0,679; 0,938] | 1,495 ✗ | 0,756 | 0,984 |
| F-5 | 367 / 174 / 0,4741 | **0,783** [0,489; 0,945] | 1,65 | 0,692 | 0,870 |

Tidak dinilai: F-9_A (3 positif), F-7 (0), F-9 (0). Persistence (label jendela sebelumnya)
mengalahkan RF di SEMUA fold → model tidak menambah nilai di atas "status tetap";
kesimpulan jujur: **kelayakan kelas ini bersyarat pada kemampuan memprediksi PERUBAHAN,
bukan status** — jangan dijual sebagai detektor siap pakai.

### 4.4 Kelas yang GAGAL (angka lengkap, tidak digabung)

| Kelas | G1 (lift≥1,5 mayoritas) | G2 (RF ≥ canary) | Angka kunci | Verdict |
|---|---|---|---|---|
| `stuck` | 1/2 fold | 1/2 | F-14 AUPRC 0,421 lift **3,12** (canary 0,410 — nyaris seri); F-9_A AUPRC 0,651 lift **0,97** (canary 0,769 > RF; persistence 0,787 > RF) | **GAGAL** |
| `shk` | 3/7 | 6/7 | lift per fold: 1,35 / 1,24 / 1,26 / **3,36** / 0,94 / **9,79** / **2,31** — tidak mayoritas; prevalensi sangat rendah (0,6–2,4%) di 4 fold | **GAGAL** |
| `hyd` | 2/7 | 4/7 | lift: 1,40 / 1,00 / 1,02 / 2,03 / 0,80 / 2,35 / 1,07; **persistence 0,42–0,63 jauh di atas RF 0,11–0,61 di 7/7 fold** | **GAGAL** |
| `tool_wear` | 0/4 (LOTO) | 4/4 | lift: **1,09 / 1,39 / 1,42 / 1,30** (AUPRC 0,54–0,77 vs prev ~0,5) — semua di bawah 1,5 | **GAGAL** |

### 4.5 Rekap gate (7 kelas, 4 kampanye)

| Verdict | Kelas | Jumlah |
|---|---|---|
| **LULUS** | `vib`, `ssi` | **2** |
| **LAYAK BERSYARAT** (G1+G2 lolos, persistence > model) | `bit_wear` | **1** |
| **GAGAL** | `stuck`, `shk`, `hyd`, `tool_wear` | 4 |

**Klaim terhadap syarat dosen ">3 jenis kriteria kerusakan":**
- Terpenuhi **BERSYARAT**: **3 kelas lolos G1+G2** (2 LULUS penuh + 1 layak bersyarat),
  didefinisikan dari **data nyata** dengan sumber label berbeda secara fisik (getaran lateral,
  getaran torsional, keausan/inefisiensi) dan populasi sampel nyata terhitung.
- TIDAK boleh diklaim sebagai "3 detektor siap pakai": `bit_wear` bergantung pada persistence,
  dan 4 kelas lainnya GAGAL dengan angka di §4.4. Jika dosen menuntut ≥3 kelas TANPA syarat,
  saat ini **belum terpenuhi** — angka-angkanya ada di §4.4 untuk ditunjukkan apa adanya.

## 5. SHAP (deskriptif — `scratch/v6_e1/E1_SHAP.json`, log `E1_SHAP_LOG.txt`)

Protokol: fold = kelompok terbesar, background 200 baris latih (seed 42), 121–200 baris uji
OOF, output P(positif), versi shap 0.52.0. Fitur peringkat atas (mean|SHAP|):

| Kelas (fold uji) | additivity max\|err\| | 6 fitur teratas |
|---|---|---|
| `stuck` (F-14) | 1,33e-03 ✗ | RPM_last, TQA_last, RPM_mean, TQA_mean, dbtm_last, HKLD_mean |
| `vib` (F-15_S) | 1,19e-08 ✓ | TFLO_mean, TFLO_last, depth_mean, dbtm_last, dbtm_mean, HKLD_mean |
| `shk` (F-15_S) | 3,62e-09 ✓ | TFLO_last, SPPA_mean, depth_mean, BPOS_mean, dbtm_mean, HKLD_mean |
| `ssi` (F-15A) | 3,43e-09 ✓ | TFLO_mean, TFLO_last, SPPA_mean, BPOS_last, BPOS_mean, BPOS_std |
| `hyd` (F-14) | 1,49e-08 ✓ | HKLD_mean, HKLD_last, dbtm_last, depth_last, dbtm_mean, depth_mean |
| `tool_wear` (T03) | 1,87e-04 ✗ | Z_kurt, X_fdom, X_kurt, X_crest, Z_fdom, X_std |
| `bit_wear` (F-15) | 1,45e-08 ✓ | **MD_last, MD_mean, TVD_mean, TVD_last**, FLOW_last, FLOW_mean |

Catatan jujur: (a) additivity lolos 1e-5 pada 5/7 kelas; `stuck` (1,3e-03) dan `tool_wear`
(1,9e-04) TIDAK lolos ambang pra-reg — penyebab penuh tidak didiagnosis (kemungkinan
interaksi imputer fitur kosong + TreeExplainer pada fold kecil) → SHAP dua kelas itu
dipakai deskriptif dengan status "additivity gagal", bukan sebagai bukti kuantitatif;
(b) `bit_wear` didominasi fitur KEDALAMAN → konsisten dengan §4.3 (persistence & canary
kedalaman kuat): model banyak "mengingat posisi", bukan memodelkan fisika keausan;
(c) `tool_wear` didominasi kurtosis/frekuensi dominan (bukan hanya amplitudo) — konsisten
dengan G2 lolos tapi G1 gagal; (d) plot PNG tidak tersimpan: `shap.plots.bar` pada shap
0.52.0 tidak menerima `Explanation.mean_abs` (error terekam di JSON per kelas) — angka
mean|SHAP| di atas berasal dari `Explanation.values` yang sudah diverifikasi additivity-nya.

## 6. Kelemahan jujur (wajib, tidak digabung)

1. **`bit_wear` persistence > RF di 4/4 fold** → layak bersyarat; label high-MSE membentuk
   blok panjang lintas kedalaman, model tidak mengalahkan "status sebelumnya".
2. **`stuck` hanya 2 sumur eligible** dan F-9_A prev 66,9% (blok label panjang; V5-J2 sudah
   memperingatkan persistence) → GAGAL; semantik kode STUCK_RT 0/1/2/3 tidak terdokumentasi.
3. **`shk`/`ssi` sangat langka** di beberapa sumur (F-15A 0,5–0,6%); 2 fold ssi UNDERPOWERED.
4. **`hyd` label = proxy anomali tekanan**, persistence mengalahkan model 7/7 → gagal total.
5. **`tool_wear` domain bengkel** (bukan sumur minyak), n alat = 4, label tercampur urutan
   percobaan (R02 selalu sesudah R01: termal/kedalaman ikut berkembang).
6. **F-9 1.159 label stuck & 1.270 label vib teramati tapi 0 jendela fitur pengeboran**
   (median baris drilling = 0 di jendela fitur) → 2 kelas kehilangan 1-2 sumur karena
   keadaan data, bukan pilihan.
7. **Agregat 1 menit** kehilangan variasi sub-menit (desain sadar: 3,2 GB CSV).
8. **Kampanye E1b–E1d sequential** (keputusan setelah melihat hasil E1a) — setiap kampanye
   punya pra-registrasi sendiri, tetapi bukan replikasi independen; E1d dinyatakan upaya
   terakhir untuk mencegah shopping-for-significance.
9. F-1 C + F-11 (54,6% file log) belum diparse → belum masuk LOWO (peluang perluasan).
10. Semua fold memakai kanal duplikat WHIRL_RT/BOUNCE_RT DILARANG sebagai fitur/kelas
    terpisah (larangan D0 §2.5 ditegakkan: kelas `vib` hanya dari VIBLAT_RT).

## 7. Artefak & reproduksi

- Pra-registrasi: `docs/V6_E1_PREREG.md`, `V6_E1b_PREREG_HYD.md`, `V6_E1c_PREREG_TOOLWEAR.md`,
  `V6_E1d_PREREG_BITWEAR.md` (hash di komentar kartu, dihitung sebelum training masing-masing).
- Kode (semua bisa dijalankan ulang, urutan: 00→01→10→20→30; 31→32; 50→51; 60→61; 40):
  `code/v6_e1_00_channels.py`, `01_label_counts.py`, `10_bins.py`, `20_windows.py`,
  `30_lowo.py`, `31_hyd_windows.py`, `32_hyd_lowo.py`, `40_shap.py`, `50_toolwear.py`,
  `51_toolwear_lowo.py`, `60_usrop_windows.py`, `61_usrop_lowo.py`.
- Hasil mentah: `scratch/v6_e1/E1_LOWO_RESULTS.json` (+`E1b`,`E1c`,`E1d`) dan
  `*_RUN_LOG.txt`; hitungan sampel: `ch20_windows_summary.json`, `ch31_hyd_summary.json`,
  `ch50_toolwear_summary.json`, `ch60_usrop_summary.json`; data unduhan terverifikasi:
  `toolwear/` (8 xlsx, SHA-256 cocok API Mendeley).
- Data sumber: `data/volve/witsml_parsed/*.csv` (7 sumur, 6,96 juta baris),
  `data/USROP_labeled.csv` (198.928 baris).
