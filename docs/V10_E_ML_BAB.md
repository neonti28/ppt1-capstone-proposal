# V10-E_ML — BAB PROPOSAL: LABELING ML, FITUR 55, PROTOKOL LOWO & HASIL NYATA RF/GB/LR

Task: `t_2db22ea0` [Algorithm Engineer ML] · Papan: `capstone-v10-proposal` · 2026-10-14 (WIB)
Peran: **[Algorithm Engineer ML] V9-E_ML** (`t_902dd141`) — bab proposal dari sudut pandang peran sendiri.
Basis: draft konsultan `t_c653c6eb` (papan `capstone-v9-build`), **ditinjau ulang & dipoles** terhadap
JSON primer; dua angka draft diperbaiki (§0 catatan koreksi).
Sumbu angka: `docs/V9_E_ML_ENGINE.md` (dokumen hasil induk) + JSON primer eksekusi
`scratch/v9_e_ml/v9_e_ML_{vib,ssi,shk,stuck_k2}_RESULTS.json` +
`v9_e_ML_stuck_k2_persistence_onset.json` + kode `code/v9_e_ML_01_train.py` &
`code/v9_d1_0{2,3,4}_*.py` (pembentuk label) & `code/v9_d1_05_leak_lowo.py` (checker anti-bocor).

> **Prinsip dokumen:** SEMUA angka dikutip dari dokumen/JSON/kode milik peran ini — **tidak ada
> angka baru yang dikarang**. Dokumen ini adalah **solusi** untuk bab proposal (porsi **(e)-ML**),
> bukan riwayat kegagalan: yang ditulis = apa yang dijalankan, bagaimana mekanismenya, dan pada
> tingkat apa ia layak dipakai. Setiap angka dapat dilacak ke fold JSON (§8).

> **Riset pendahuluan: `scientific-critical-thinking`** — OBSERVED (angka eksekusi JSON) dipisah
> dari DESAIN (keputusan harness: hyperparam GB/LR, tau grid) dan DERIVED (rekonstruksi event
> stuck_k2); kontradiksi dataset stuck_k2 (§7) dilaporkan, bukan didiamkan; tes pembeda
> persistence-onset dijalankan apa adanya meski hasilnya merugikan ML (§6.4). Dua angka draft
> konsultan yang TIDAK lolos verifikasi JSON (jumlah fold; klaim FAR shk) **diperbaiki**, bukan
> diwariskan (§0 catatan koreksi).
> **Riset pendahuluan: `statistical-analysis`** — AUPRC + CI95 moving-block bootstrap (blok 60
> jendela, 1.000 resample, seed 42) per fold; lift dibaca terhadap plafon 1/prev yang dilaporkan
> per fold; fold <30 positif = UNDERPOWERED dilabeli, tidak dihitung mayoritas; FAR per skala
> aslinya (jendela 1 menit → per 24 jam) tanpa konversi diam-diam; baseline relevan per tugas
> (persistence/canary/prevalence-random), bukan satu baseline universal.
> **Riset pendahuluan: `verification-mandatory`** — setiap angka headline di dokumen ini dihitung
> ulang dari JSON mentah (bukan dari ingatan, bukan dari teks dokumen sumber); determinisme diuji
> re-run fold 0 (gerbang 1e-9 S4); anti-sirkularitas di-assert ulang di runtime (0 kanal label di
> fitur); reproduksi silang angka V8-E_vib (lift 1,61/2,36/3,50/1,63 cocok persis) = kontrol
> validitas pipeline; daftar "belum terukur" eksplisit §7.
> **Riset pendahuluan: `what-if-oracle`** — cabang risiko hasil: Ω (ML menang semua), α (ML menang
> vs canary tapi kalah persistence — KASUS NYATA kelas onset), Δ (FAR meledak di semua tau —
> terkonfirmasi), Φ (persistence memang sudah cukup — terdukung hyd-K-i V8 + stuck_k2 K-ii di
> sini); ketegangan direkonsiliasi sebagai KEMAMPUAN + BATAS, bukan label gagal (§6).
> **Riset pendahuluan: `consciousness-council`** — 5 arketipe menekan desain harness: Empiricist
> (tau grid = semua titik pra-reg dilaporkan, tanpa pemilihan pasca-hasil), Minimalist (1 harness,
> 3 model, 3 baseline, 4 engine), Contrarian (persistence-onset yang "menang telak" ditampilkan
> penuh §6.4), Architect (kepatuhan D-A5: nol ML di hyd-K-i), Pragmatist (prioritas engine sesuai
> fokus kartu).
> **Riset pendahuluan: `sequentialthinking`** (4 pikiran, 4/4 sukses, `sequ-mcp`) — verifikasi
> angka draft vs JSON → identifikasi 2 koreksi (fold 26; FAR shk) → identifikasi 2 kelas label
> yang hilang (turunan & kurasi) → rencana dokumen final.

---

## 0. RINGKASAN UNTUK DOSEN (satu paragraf)

Untuk pertanyaan proposal **(e) "labeling ML / rumus statistik / workflow hybrid"**, jawaban peran
Algorithm Engineer ML adalah: **empat head ML dilatih pada data lapangan Volve yang sama, dengan
kontrak yang sama, dan diuji dengan cara yang sama** — tidak ada perlakuan istimewa per kelas.
(1) **Labeling** tidak dikarang: tiap label berasal dari **kanal instrumen MWD** (`VIBLAT_RT`,
`SHKRSK_RT`, `STUCK_RT`), **turunan fisika** (`SSI(CRPM)`; untuk kelas lain: `high_MSE` Teale,
residu `SPPA` z), **kurasi kejadian** (onset stuck; serta 884 event DDR sebagai kontrol), atau
**identitas-run** (tool_wear); kanal pembentuk label **dilarang keras menjadi fitur** (asersi
anti-sirkularitas lolos di runtime, §1.2). (2) **Fitur = 55 = 11 kanal MWD × 5 statistik**
(mean/std/slope/last/frac) dihitung pada **jendela ketat-lalu `[t0−10, t0)`** — fitur selalu dari
masa lalu relatif label (anti-bocor). (3) **Protokol = LOWO (Leave-One-Well-Out), seed 42, imputer
median fold-safe, tanpa grid search**; ambang operasi (tau) **dipra-registrasi** dan **semua titik
dilaporkan**, bukan dipilih setelah melihat hasil. (4) **Hasil nyata** dari **26 fold**: RF vib
mereproduksi V8 **persis** (lift 1,61/2,36/3,50/1,63); RF ≥ canary di 4/4 (vib) dan 5/7–5/9
(ssi/shk); **temuan jujur** — persistence-onset mengalahkan RF 4/4 di kelas onset (AUPRC 0,83–0,90
vs 0,07–0,44) karena label horizon kontigu — ini **KEMAMPUAN baseline + BATAS formulasi label,
bukan kegagalan ML**. Tidak ada head yang memenuhi syarat alarm otomatis penuh; hasil disimpan
sebagai KEMAMPUAN + BATAS + KEKUATAN BUKTI per fold.

> **Catatan koreksi (verification-mandatory).** Dua angka pada draft konsultan (`t_c653c6eb`)
> **tidak lolos verifikasi JSON** dan sudah diperbaiki di dokumen ini:
> **(1) Jumlah fold = 26, bukan 28.** Empat head ML = vib 4 + ssi 9 + shk 9 + stuck_k2 4 = **26**
> (terverifikasi dari `scratch/v9_d1/lowo_*.json` dan array `folds` di tiap JSON). Angka "28" yang
> tertulis di draft (dan di `docs/V9_E_ML_ENGINE.md` §0/§9) adalah salah aritmetika — kemungkinan
> menghitung 5 dataset (termasuk `stuck_k1` 2 fold yang **bukan** head ML). Seluruh "28 fold"
> diganti "26 fold".
> **(2) Klaim FAR shk "di SEMUA fold dan SEMUA model × tau, FAR > 60/24jam" SALAH.** Dari JSON,
> **53 dari 135 titik shk punya FAR ≤ 60** (FAR minimum = 0,0). Yang benar dan tetap mendukung
> kesimpulan: FAR tinggi di **mayoritas** titik dan **tidak ada** titik yang memenuhi syarat L1
> penuh; **1 titik hemat-awas** ada (F-14 rf tau=0,3 FAR=0,69 R=0,0053) — persis yang juga
> dicatat dokumen induk di §6.3/§6.5. Angka "402 titik uji" dan "10 titik FAR≤6 & R>0" (§6.5)
> **terverifikasi cocok** dan dipertahankan.

---

## 1. (e.1) LABELING PER KELAS — EMPAT KELAS SUMBER LABEL

Tiap kelas memakai **satu jenis sumber label** (agar estimand tidak tercampur). Dua kolom terakhir
memisahkan **yang benar-benar dilatih di kartu ini** dari **skema label engine lain** (yang labelnya
ada, tetapi modelnya bukan milik kartu ML ini). Kode pembentuk: `code/v9_d1_02_rig_windows.py`
(label status vib/ssi/shk), `code/v9_d1_03_rig_datasets.py` (label turunan hyd), `code/v9_d1_04_stuck_k2.py`
(label onset kurasi), `data/USROP_labeled.csv` (label Teale, E1d).

| Kelas (head) | **Jenis sumber label** | Rumus / aturan label persis | Berkas pembentuk | **Dilatih di kartu ini?** |
|---|---|---|---|---|
| **vib** | **Instrumen** (kanal MWD) | `y = 1[ max_{k∈[0,10)} VIBLAT_RT(t0+k) ≥ 32,17405 ]` (ambang operasional rig) | `v9_d1_02` (`VIB_THRESH=32.17405`) | **YA** |
| **shk** | **Instrumen** (kanal MWD) | `y = 1[ max_{k∈[0,10)} SHKRSK_RT(t0+k) ≥ 1 ]` | `v9_d1_02` (`LABDEF shk`, thr 1,0) | **YA** |
| **ssi** | **Turunan fisika** (dari CRPM) | `SSI = (max − min)/(2·mean)` atas jendela CRPM ≥ **10 sampel** (`mean>0`); `y = 1[SSI ≥ 1]` | `v9_d1_02` (`SSI_MIN_SAMPLES=10`) | **YA** |
| **stuck K-ii** | **Kurasi kejadian** (onset) | onset = edge `0→1` pada `STUCK_RT` **ffill**; label positif = jendela **`[t_e−10, t_e)`** (H=10 mnt); baris dalam blok (`STUCK≥1`) **dibuang** | `v9_d1_04` (`H=10`) | **YA** |
| hyd K-i | **Turunan fisika** (residu) | z robust `median/MAD` `SPPA` per bin `qcut(TFLO,10)`; `y = 1[|z| > 2]` (agregasi jendela W=10, ≥50% menit anom) | `v9_d1_03` (`hyd_bin_labels`) | tidak — **RF dilarang** (D-A5) |
| bit_wear K-1 | **Turunan fisika** (Teale) | `high_MSE = Teale MSE > P75 = 256,600 psi` (kolom `label` tersimpan USROP) | `data/USROP_labeled.csv` (E1d) | tidak — dataset USROP **tak diproduksi D1** |
| tool_wear K-ii | **Identitas-run** | label = **identitas run** (4 alat × 2 run) — bukan turunan fitur | Mendeley `th4yv974r2` | tidak — domain bengkel (D-A7) |
| *(kontrol)* | **Kurasi kejadian DDR** | **884 event** `labels_curated_v2.csv` (yes 50 / uncertain 571 / no 263) | `data/volve/labels_curated_v2.csv` | tidak — dipakai sebagai **kontrol-positif** |

**Empat jenis sumber, satu alasan metodologis masing-masing:**

1. **Instrumen (vib, shk, stuck-K-i):** label dibaca langsung dari kanal MWD downhole — paling
   dekat dengan "kejadian nyata di lubang". Risikonya: label bisa drift antar-wellbore (getaran)
   atau severity-mix beda antar-well (shk) → dicatat sebagai batas semantik, bukan disembunyikan.
2. **Turunan fisika (ssi, hyd K-i, bit_wear K-1):** label **bukan** kanal mentah, melainkan
   **rumus** — `SSI=(max−min)/(2·mean)` atas CRPM (Liu 2025); z-residu SPPA (median/MAD per bin);
   `high_MSE` Teale (MSE > P75). Karena tiap label = **fungsi** dari kanal tertentu, kanal itu
   **dilarang jadi fitur** — kalau tidak, ML hanya "belajar rumus" (sirkular).
3. **Kurasi kejadian (stuck K-ii onset; 884 event DDR):** label onset **tidak** ada di kanal
   mentah sebagai "peristiwa" — ia **direkonstruksi** dari transisi `STUCK_RT 0→1` dengan resep
   V8-E_stuck (ffill dikunci pra-reg; strict = sensitivitas), dan **dikurasi** (baris dalam blok
   dibuang). Invarian validasi: jumlah onset ffill **cocok V8** di 3/3 well yang punya referensi
   (F-9_A 72, F-10 93, F-14 61; F-9 tanpa referensi V8 = 55, dicatat kekuatan bukti lebih rendah).
   Himpunan **884 event** `labels_curated_v2.csv` (kurasi laporan DDR) adalah ground-truth
   kejadian terpisah — dipakai sebagai **kontrol-positif** (uji label stuck 0/10 V8), bukan label
   latih kartu ini.
4. **Identitas-run (tool_wear):** label = identitas run bengkel (Mendeley `th4yv974r2`), **bukan
   turunan fitur** → anti-sirkular terpenuhi secara desain; **tidak dilatih** di kartu ini
   (modul terpisah, D-A7).

### 1.1 ANTI-SIRKULARITAS YANG DI-ASERSIKAN (bukan klaim, tapi assert runtime)

Di `code/v9_e_ML_01_train.py` baris 192–193, sebelum pelatihan dijalankan, ada **assert runtime**:

```python
assert not any(k in c for k in ("VIBLAT", "SHKRSK", "CRPM", "STUCK")
               for c in feats), "anti-sirkularitas: kanal label ada di fitur!"
```

Artinya: jika **satu saja** kolom fitur mengandung kanal pembentuk label
(`VIBLAT`/`SHKRSK`/`CRPM`/`STUCK`), pelatihan **berhenti**. Ini berjalan nyata setiap run — bukan
janji di dokumen. **Kanal fitur yang dipakai = `[TQA, SPPA, TFLO, RPM, SWOB, HKLD, ROP, BPOS, SPM,
depth, dbtm]`** (11 kanal surface/depth), **tanpa** kanal instrumen label.

Aturan anti-sirkularitas per kelas (tabel kanal terlarang):

| Kelas | Kanal pembentuk label | Dilarang jadi fitur |
|---|---|---|
| vib | `VIBLAT_RT` | VIBLAT (di-assert) |
| shk | `SHKRSK_RT` | SHKRSK (di-assert) |
| ssi | `CRPM_RT` | CRPM (di-assert) |
| stuck K-i/K-ii | `STUCK_RT` | STUCK (di-assert) |
| hyd K-i | `SPPA`, `TFLO`, `SPM` | SPPA/TFLO/SPM dibuang → **8 kanal** (D-A5) |
| bit_wear K-1 | WOB, TQ, RPM, ROP, Hookload, MSE, D_exp, ROC_coef | 8 kanal MSE dibuang (V6-E1d §4) |
| tool_wear K-ii | — (label = identitas run) | n/a (anti-sirkular by design) |

### 1.2 KENAPA "KETAT-LALU" (strict-past) — INTI KEJUJURAN METODE

Label setiap kelas dibentuk dari jendela **`[t0, t0+10)`** (positif = kanal terpicu **di dalam**
jendela). Maka:

- Fitur **harus** dibaca dari **`[t0−10, t0)`** (masa lalu ketat) supaya tidak membaca labelnya
  sendiri. Invariant anti-bocor S5 = `feat_ts_max < lab_ts`; checker independen
  (`v9_d1_05_leak_lowo.py`) melaporkan **0 pelanggaran** di 6/6 dataset.
- Untuk onset stuck, jendela fitur juga `[t0−10, t0)` **strict-past** (deviasi terdokumentasi dari
  rolling V8 t−9..t) — agar stempel anti-bocor berlaku untuk baris negatif (`lab_ts=t0`) **dan**
  positif (`lab_ts=t_e`).
- Konsekuensi jujur: **FAR pada semua tau ratusan/24jam** (§6.5) — justru karena fitur tidak
  "menyalin" label, ML jadi detektor yang bisa dikritik.

> **Ringkas:** strict-past = **aturan etika pengukuran**, bukan optimasi. Ia memastikan angka ML
> bukan artefak sirkularitas, sehingga perbandingan ML-vs-rule dan ML-vs-persistence berdiri di
> atas dasar yang bersih.

---

## 2. (e.2) FITUR 55 (11 KANAL × 5 STAT) & PROTOKOL LOWO

### 2.1 Kontrak fitur (S1)

- **Grid 60 detik** (bin epoch-menit), ALL-rows.
- **Jendela ketat-lalu `[t0−10, t0)`** — 10 menit sebelum anchor.
- **11 kanal** MWD/surface: `TQA, SPPA, TFLO, RPM, SWOB, HKLD, ROP, BPOS, SPM, depth, dbtm`.
- **5 statistik per kanal** = **55 fitur**:
  `mean` · `std (ddof=1)` · `slope OLS per menit` (butuh `cnt≥3` & `den>1e-9`, selain itu NaN) ·
  `last` (nilai `t0−1`) · `frac` (hitung non-null / 10).
- **Eligibility:** `feat_valid = (drill_bins ≥ 5) & (drill_rows ≥ 60)`; tiap engine menambah
  `valid_<kelas>` (mis. SSI butuh ≥10 sampel CRPM). Baris tak layak tidak diekspor.

Ringkasnya, 55 = `11 kanal × 5 statistik`. Angka 55 ini **identik** di keempat head (JSON
`n_features: 55`, `feature_cols` panjang 55, keempat daftar **identik**) — **kontrol bahwa kontrak
fitur seragam** (§4).

### 2.2 Protokol LOWO (Leave-One-Well-Out)

- **Satu fold = satu sumur uji**; semua sumur lain = data latih. Fold dari
  `scratch/v9_d1/lowo_<engine>.json` (identik tim E_STAT/E_RULE/EVAL).
- **26 fold total:** vib 4 (F-14, F-15A, F-15_S, F-5) · ssi 9 (2 UNDERPOWERED) · shk 9 ·
  stuck_k2 4 (F-10, F-14, F-9, F-9_A). *(4+9+9+4 = 26.)*
- **Imputer median fold-safe:** `SimpleImputer(median)` di-fit **hanya** dari data latih fold itu,
  lalu ditransform ke data uji — tidak ada statistik dari data uji yang bocor ke pelatihan
  (berlaku untuk RF/GB/LR).
- **Tanpa grid search:** hyperparameter **dikunci** (DESAIN tetap), tidak ada pencarian. Ambang
  operasi tau **dipra-registrasi** = `{0,05; 0,10; 0,20; 0,30; 0,50}` (grid tau PM1 §2.6 shk,
  dipakai seragam semua engine) — **SEMUA titik dilaporkan**, tanpa pemilihan pasca-hasil
  (anti shopping-for-significance S3). Untuk onset: tambahan ambang `q95` skor **latih**
  (pra-reg PM1 §2.4 E3).
- **UNDERPOWERED:** fold uji **< 30 positif** dilabeli `underpowered=true` dan **dikecualikan
  dari hitungan mayoritas** (tidak dihapus — tetap dilaporkan). Yang berstatus UP: ssi F-7 (3 pos),
  ssi F-9 (12 pos).

### 2.3 Protokol evaluasi (S7/S9)

- **Metrik per fold:** AUPRC; **CI95 moving-block bootstrap** (circular, blok **60 jendela**,
  **1.000 resample**, seed **42**); `lift = AUPRC/prev`; `plafon_lift = 1/prev` dilaporkan;
  P/R/FAR pada tau grid; `FAR_24 = 1440·FP/n_neg` (skala jendela 1 menit → per 24 jam operasi).
- **Baseline per fold pada split IDENTIK (S9):** (1) **persistence** `ŷ(t)=y(t−1)` dari kolom
  `y_prev_*`; (2) **canary-kedalaman** = RF kontrak **hanya** fitur `depth_*`/`dbtm_*` (kontrol
  memorisasi posisi); (3) **prevalence-random** = AUPRC = prev. ΔB = AUPRC(model) − AUPRC(baseline)
  dihitung per fold.
- **Onset (stuck K-ii):** + B1 = % event dengan ≥1 alarm di horizon; TLead median (menit).
- **Determinisme (S4):** semua `random_state=42`; re-run fold 0 vib → `max_abs_diff = 2,22e-16`
  (di bawah gerbang 1e-9; bukan bit-exact karena akumulasi float `n_jobs=-1`, dicatat jujur).

---

## 3. (e.3) KONTRAK RF / GB / LR — APA ADANYA DARI SKRIP

Tiga model dilatih dengan **kontrak yang sama** tiap fold (kode: `code/v9_e_ML_01_train.py`
`make_models()`), seed 42, **tanpa tuning**:

| Model | Konfigurasi persis | Alasan dipilih (DESAIN tetap) |
|---|---|---|
| **RF** | `RandomForestClassifier(n_estimators=300 [stuck_k2: 200], min_samples_leaf=5, class_weight="balanced_subsample", random_state=42, n_jobs=-1)` | kontrak PM1 §2.1; E3 onset = 200 pohon (PM1 §2.4); tahan overfitting pada fitur noise |
| **GB** | `GradientBoostingClassifier(n_estimators=200, learning_rate=0.1, max_depth=3, random_state=42)` | PM1 §1.2 "ML heads RF/GBM/LR" — default sklearn dikunci, tanpa tuning |
| **LR** | `Pipeline(SimpleImputer(median, fold-safe) → StandardScaler(fold-safe) → LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42))` | pembanding linier seragam; imputer/scaler fold-safe |

**Imputasi:** median fold-safe untuk **SEMUA** model (fit hanya data latih; PM1 S4). **CI95:**
moving-block bootstrap circular, blok 60 jendela, 1.000 resample, seed 42 (definisi "60/20/10" S7;
harmonisasi EVAL_A). **Software tercatat di JSON:** sklearn 1.9.1, numpy 2.5.3, pandas 2.3.3.

**Kepatuhan larangan (D-A5):** harness **menolak** engine di luar daftar (`argparse choices`) —
`hyd_ki` dan `stuck_k1` **tidak bisa** dijalankan skrip ini (hyd-K-i = nol ML, stuck-K-i =
persistence per spesifikasi). Ini bukan kelalaian, melainkan **paksaan kode**.

---

## 4. (e.4) HASIL NYATA PER ENGINE (KUTIPAN JSON — 26 FOLD)

Ringkasan agregat (dari JSON `agregat`; "layak" = fold non-UNDERPOWERED):

| Engine | Jenis tugas | Fold | RF AUPRC (rentang) | RF spread | RF ΔB>0 vs canary | RF ΔB>0 vs persistence | vonis kemampuan |
|---|---|---|---|---|---|---|---|
| **vib** | deteksi kondisi | 4 | 0,4405–0,9117 | 0,4712 | **4/4** | 2/4 | skor penambah layak (reproduksi V8 persis) |
| **ssi** | deteksi kondisi | 9 (2 UP) | 0,0151–0,4589 | 0,4438 | 5/7 | 6/7 | skor-ranking layak; keyakinan fold wajib tampil |
| **shk** | deteksi anomali | 9 | 0,0069–0,1929 | 0,1860 | 5/9 | 4/9 | layak L2/L1-terkalibrasi sesuai V8 |
| **stuck K-ii** | prediksi onset H=10 mnt | 4 | 0,0697–0,4443 | 0,3747 | **4/4** | **0/4** | ranking layak; persistence-onset menang telak (§6.4) |

### 4.1 vib (4 fold LOWO)

| Fold | Well | n | pos | prev | UP | RF AUPRC (CI95) | GB | LR | pers | canary | rand |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | F-14 | 1989 | 1124 | 0,5651 | . | 0,9117 [0,821;0,961] | 0,9164 | 0,8752 | 0,7959 | 0,6124 | 0,5651 |
| 1 | F-15A | 6482 | 1543 | 0,2380 | . | 0,5623 [0,397;0,683] | 0,4665 | 0,6472 | 0,5474 | 0,4578 | 0,2380 |
| 2 | F-15_S | 10903 | 1532 | 0,1405 | . | 0,4914 [0,338;0,619] | 0,2486 | 0,1839 | 0,5166 | 0,2770 | 0,1405 |
| 3 | F-5 | 4548 | 1230 | 0,2704 | . | 0,4405 [0,341;0,553] | 0,5193 | 0,6606 | 0,6675 | 0,3093 | 0,2704 |

**ΔB RF per fold** — vs persistence: +0,1192 / +0,0149 / −0,0181 / −0,2268; vs canary:
+0,2993 / +0,1044 / +0,2144 / +0,1313; vs prev-random: +0,3466 / +0,3242 / +0,3509 / +0,1701.

**Silang-kontrol reproduksi:** RF **lift per fold = 1,61 / 2,36 / 3,50 / 1,63** — **COCOK PERSIS**
dengan angka V8-E_vib (G1 4/4); RF ≥ canary **4/4** (G2). Ini kontrol validitas bahwa harness V9
memakai resep setara V8 (bukan pipeline berbeda).

### 4.2 ssi (9 fold LOWO; 2 UNDERPOWERED)

| Fold | Well | n | pos | prev | UP | RF AUPRC (CI95) | GB | LR | pers | canary | rand |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | F-10 | 7133 | 161 | 0,0226 | . | 0,0839 [0,036;0,194] | 0,0430 | 0,0826 | 0,2025 | 0,0302 | 0,0226 |
| 1 | F-12 | 4293 | 83 | 0,0193 | . | 0,0550 [0,014;0,165] | 0,0684 | 0,0810 | 0,0203 | 0,0709 | 0,0193 |
| 2 | F-14 | 5455 | 75 | 0,0137 | . | 0,0286 [0,009;0,075] | 0,0163 | 0,0171 | 0,0122 | 0,0305 | 0,0137 |
| 3 | F-15A | 6020 | 31 | 0,0051 | . | 0,0631 [0,007;0,200] | 0,0367 | 0,0160 | 0,0088 | 0,0139 | 0,0051 |
| 4 | F-15_S | 5342 | 85 | 0,0159 | . | 0,1361 [0,060;0,255] | 0,0552 | 0,0244 | 0,0170 | 0,0243 | 0,0159 |
| 5 | F-5 | 4714 | 102 | 0,0216 | . | 0,1073 [0,045;0,249] | 0,0675 | 0,0628 | 0,0354 | 0,0751 | 0,0216 |
| 6 | F-7 | 982 | 3 | 0,0031 | **Y** | 0,4589 [0,000;0,696] | 0,0069 | 0,0301 | 0,0000 | 0,0201 | 0,0031 |
| 7 | F-9 | 1126 | 12 | 0,0107 | **Y** | 0,0151 [0,000;0,116] | 0,0163 | 0,0451 | 0,0117 | 0,0097 | 0,0107 |
| 8 | F-9_A | 841 | 55 | 0,0654 | . | 0,1357 [0,065;0,281] | 0,1406 | 0,2082 | 0,0672 | 0,0860 | 0,0654 |

**ΔB RF per fold** — vs persistence: −0,1168 / +0,0382 / +0,0089 / +0,0562 / +0,1195 / +0,0736 /
+0,0000 / +0,0049 / +0,0892; vs canary: +0,0538 / −0,0159 / −0,0019 / +0,0492 / +0,1118 / +0,0322 /
+0,4388 / +0,0055 / +0,0496. Catatan: F-7 & F-9 UNDERPOWERED — AUPRC F-7 (0,4589) **tidak boleh
dibaca** sebagai bukti stabil; fold layak = 7. Persistence justru kuat di F-10 (0,2025) = KEMAMPUAN
baseline (stick-slip persisten antar-grid di sumur itu), bukan aib ML.

### 4.3 shk (9 fold LOWO)

| Fold | Well | n | pos | prev | UP | RF AUPRC (CI95) | GB | LR | pers | canary | rand |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | F-10 | 7899 | 146 | 0,0185 | . | 0,0201 [0,010;0,035] | 0,0219 | 0,0194 | 0,0236 | 0,0212 | 0,0185 |
| 1 | F-12 | 5405 | 217 | 0,0401 | . | 0,0456 [0,019;0,094] | 0,0324 | 0,0892 | 0,0492 | 0,0652 | 0,0401 |
| 2 | F-14 | 11205 | 760 | 0,0678 | . | 0,1036 [0,063;0,166] | 0,0892 | 0,0542 | 0,1673 | 0,0630 | 0,0678 |
| 3 | F-15A | 6484 | 41 | 0,0063 | . | 0,0069 [0,002;0,016] | 0,0093 | 0,0203 | 0,0063 | 0,0121 | 0,0063 |
| 4 | F-15_S | 11394 | 259 | 0,0227 | . | 0,0265 [0,016;0,040] | 0,0246 | 0,0148 | 0,0393 | 0,0251 | 0,0227 |
| 5 | F-5 | 7140 | 240 | 0,0336 | . | 0,0896 [0,047;0,185] | 0,0886 | 0,0997 | 0,0452 | 0,0487 | 0,0336 |
| 6 | F-7 | 2761 | 267 | 0,0967 | . | 0,1015 [0,045;0,183] | 0,1171 | 0,0906 | 0,4457 | 0,0789 | 0,0967 |
| 7 | F-9 | 1851 | 45 | 0,0243 | . | 0,1929 [0,032;0,466] | 0,1117 | 0,0865 | 0,0384 | 0,0611 | 0,0243 |
| 8 | F-9_A | 2356 | 30 | 0,0127 | . | 0,0209 [0,002;0,050] | 0,0206 | 0,0303 | 0,0144 | 0,0388 | 0,0127 |

**ΔB RF per fold** — vs persistence: −0,0034 / −0,0258 / −0,0842 / +0,0006 / −0,0125 / +0,0659 /
−0,3436 / +0,1591 / +0,0090; vs canary: −0,0011 / −0,0196 / +0,0406 / −0,0053 / +0,0014 / +0,0409 /
+0,0226 / +0,1318 / −0,0179. Catatan (terverifikasi JSON): FAR **tinggi di mayoritas titik** — dari
135 titik shk (9 fold × 3 model × 5 tau), **53 titik punya FAR ≤ 60/24jam** (minimum 0,0), dan
**hanya 1 titik** memenuhi FAR≤6 **dengan** recall>0 (F-14 rf tau=0,3 FAR=0,69 R=0,0053). Jadi
**tidak ada** titik yang memenuhi syarat L1 penuh di kerangka ini — konsisten dengan temuan V8
(kalibrasi lokal per well = prasyarat, D-A4). Klaim draft "FAR > 60 di SEMUA titik" **salah** dan
sudah diperbaiki (lihat §0).

### 4.4 stuck K-ii (4 fold LOWO; prediksi onset H=10 mnt)

| Fold | Well | n | pos | prev | UP | RF AUPRC (CI95) | GB | LR | pers | canary | rand |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | F-10 | 4216 | 772 | 0,1831 | . | 0,1997 [0,139;0,284] | 0,2020 | 0,2874 | **0,9016** | 0,1758 | 0,1831 |
| 1 | F-14 | 95925 | 389 | 0,0041 | . | 0,0704 [0,028;0,146] | 0,0192 | 0,0132 | **0,8438** | 0,0092 | 0,0041 |
| 2 | F-9 | 16184 | 311 | 0,0192 | . | 0,0697 [0,030;0,122] | 0,0554 | 0,0791 | **0,8265** | 0,0402 | 0,0192 |
| 3 | F-9_A | 2242 | 503 | 0,2244 | . | 0,4443 [0,334;0,565] | 0,2917 | 0,3128 | **0,8890** | 0,2569 | 0,2244 |

**ΔB RF per fold** — vs persistence: −0,7019 / −0,7734 / −0,7569 / −0,4446 (**0/4**); vs canary:
+0,0239 / +0,0612 / +0,0294 / +0,1874 (**4/4**). B1 + TLead RF (ambang `q95` latih) + baseline
persistence-onset:

| Well | RF B1 (q95) | RF TLead med (mnt) | RF deteksi | **persistence-onset B1** | **persistence-onset TLead** |
|---|---|---|---|---|---|
| F-10 | 0,657 | 10,0 | 44/67 | **1,000** | 9,0 |
| F-14 | 0,000 | — | 0/28 | **1,000** | 9,0 |
| F-9 | **1,000** | 11,5 | 16/16 | **1,000** | 10,5 |
| F-9_A | **1,000** | 10,0 | 37/37 | **1,000** | 9,0 |

Di mana RF tetap punya ruang: F-9 & F-9_A RF q95 mencapai B1 1,0 dengan **TLead median 10,0–11,5
mnt** — lebih panjang dari persistence (9,0–10,5), karena persistence-onset tidak bisa memberi
peringatan di **menit pertama** horizon.

---

## 5. (f) RINGKAS "7 vs 11 vs 27" DARI SUDUT ML

Angka mengikat mengikuti `docs/V10_PM1_OUTLINE.md` §1 (7 = engine/kelas, 11 = klaim/tugas,
27 = head/metode):

| Angka | Arti (kosakata PM1 §1) | Porsi peran ML ini |
|---|---|---|
| **7** | jumlah **engine** (kelas kerusakan) | head ML **dilatih untuk 4 kelas** (vib, ssi, shk, stuck K-ii); 3 kelas lain: hyd-K-i **DILARANG ML** (D-A5); stuck-K-i = persistence (bukan head ML); bit_wear K-2/tool_wear K-ii = dataset/pra-reg belum ada |
| **11** | jumlah **klaim** (sub-tugas dinilai A/B/C) | ML menyumbang di **4 klaim** (vib, ssi, shk, stuck-K-ii); baseline relevan disediakan per fold untuk semuanya |
| **27** | jumlah **head** pada registry prototipe I1 | head ML (RF/GB/LR per kelas) = bagian **L2 skor-ranking**; RF vib/ssi/shk/stuck = head `*_rf_lowo` (semua tier TREN/L2) |

Jadi: **7 = jumlah masalah**, **11 = jumlah klaim**, **27 = jumlah head yang dirakit**. Kontribusi ML
= **head skor-ranking L2** (bukan L0/L1) untuk kelas di mana ia lulus uji; di kelas onset ia adalah
pembanding yang **kalah** dari persistence (temuan jujur, §6.4).

---

## 6. TEMUAN UTAMA (KEMAMPUAN + BATAS — bukan lulus/gagal)

### 6.1 vib — ML menambah nilai vs canary 4/4; reproduksi V8 persis
RF ΔB>0 vs canary **4/4** (G2 terkonfirmasi); vs persistence **2/4** (F-14 +0,119; F-15A +0,015;
F-15_S −0,018; F-5 −0,227) — identik pola V8. GB/LR tidak konsisten menang (GB kalah persistence
3/4; LR menang 2/4 dengan AUPRC fold F-5 tertinggi 0,6606) → **RF tetap head utama**. Batas: FAR
pada semua tau ratusan/24jam → L2 tren layak; L1 menunggu FAR/B4 terukur.

### 6.2 ssi — RF ≥ canary 5/7 fold layak; RF ≥ persistence 6/7
Sejalan V8 (RF ≥ canary 5/5; persistence kalah 0/5). GB lebih lemah (menang canary 4/7); LR menang
5/7. Keyakinan: **5/9 fold CI95-nya menyentuh no-skill** (CI-bawah ≤ prev: F-12, F-14, F-7, F-9,
F-9_A) → layer keyakinan wajib (kekuatan bukti SEDANG). Bukaan baru vs V8: fold **F-9_A** (eksternal,
55 positif) RF 0,1357 vs prev 0,0654 = **lift 2,07** — RF bekerja di fold eksternal ini.

### 6.3 shk — reproduksi dekat V8; persistence dominan di F-7; FAR tetap tinggi
RF ≥ canary **5/9** (V8: 6/9 — selisih kecil, harness imputer fold-safe V9). Persistence sangat kuat
di F-7 (0,4457) — kelas shock di sumur itu persisten antar-grid. Titik dengan FAR≤6 **dan** recall>0
hanya **1 titik** (F-14 rf tau=0,3 FAR=0,69 R=0,0053) — recall <0,01 = praktis nol cakupan; klaim V8
(L0-alarm BELUM) terkonfirmasi ulang.

### 6.4 stuck K-ii — persistence-onset MENANG TELAK 4/4 (tes pembeda; temuan jujur)
Persistence-onset AUPRC **0,8265–0,9016** mengalahkan RF **0,0697–0,4443** di **4/4 fold**
(B1 persistence = 1,0 semua well; TLead median 9–10,5 mnt). **Mekanisme (DIAMATI dari data, bukan
asumsi):** label positif onset = horizon `[t_e−10, t_e)` yang **kontigu** (median run 10 menit) →
`y(t−1)=1` pada ±6/7 baris positif → persistence otomatis "deteksi in-horizon". Persistence **tidak
bisa** memberi peringatan di menit pertama horizon (TLead-nya maks run−1) dan tidak bisa memberi
peringatan **sebelum** horizon masuk — di situlah RF/LR tetap punya ruang (mis. F-9 RF q95 B1 1,0
dengan TLead median 11,5 mnt). Kekuatan bukti: SEDANG (1 kampanye, 4 well, label STUCK_RT masih
punya risiko semantik lintas-well, kontrol-positif 0/10 V8 belum diulang).
**Interpretasi:** pada formulasi horizon D1, persistence = engine konfirmasi-in-horizon yang sangat
kuat; ML bernilai hanya bila diukur pada kemampuan **pra-horizon/pre-event** (butuh dataset baru
dengan sampel pra-horizon) — ini **KEMAMPUAN baseline + BATAS formulasi label, BUKAN kegagalan ML**,
dan bukan alasan menurunkan gate.

### 6.5 FAR vs ambang alarm — titik hemat-awas ADA, tapi recall kecil
Pemindaian seluruh fold × model × tau (termasuk q95_train untuk stuck) menemukan titik dengan
FAR≤6/24jam **DAN** recall>0: **10 dari 402 titik uji (<1%)** — vib 1 (F-15_S rf tau=0,5 FAR=4,15
R=0,102) · ssi 5 (mis. F-15A rf tau=0,2 FAR=4,33 R=0,161) · shk 1 (F-14 rf tau=0,3 FAR=0,69
R=0,0053) · stuck 3 (F-10/F-14/F-9_A rf tau=0,5). Sebagian besar di tau tinggi (0,2–0,5) dengan
recall 0,004–0,16 = hampir semua positif terlewat → tidak layak alarm, tapi layak dicatat sebagai
opsi "hemat-awas" (L1-syarat-dasar terpenuhi, recall tipis). Syarat **L1 PENUH** (TLead/B4 terukur +
C4 + kalibrasi lokal per well + anotasi regime) **belum** terpenuhi engine mana pun → tidak ada
kenaikan tier otomatis dari kartu ini.

---

## 7. TEMUAN DATA & YANG BELUM TERUKUR (eksplisit, ≠ 0 ≠ gagal)

**Defect D1 stuck_k2 (dilaporkan, tidak didiamkan).** Kolom `ts_bin` dan `lab_ts` pada
`scratch/v9_d1/datasets/stuck_k2.csv.gz` **KOSONG** untuk semua 118.567 baris (4/4 well; verifikasi
baca gzip mentah). Konsekuensi: (a) leak-check `v9_d1_05_leak_lowo.json` entry stuck_k2
(`0 pelanggaran`) = **vacuous** (komparasi dengan NaN selalu False); (b) B1/TLead di §4.4
direkonstruksi sebagai **DERIVED** dari run positif berurutan (`feat_ts_max` monotonic per well 4/4
terverifikasi — urutan waktu dataset tetap sah; `y_prev_stuck_onset` terisi 0 NaN). Defect sudah
dilaporkan ke kartu D1 (`t_1ca71445`, komentar #3) dengan rekomendasi regenerate + checker NaN-count.
Konstruksi anti-bocor stuck_k2 tetap terverifikasi lewat **KODE builder** (jendela ketat-lalu
`[t0−10, t0)`), bukan lewat kolom.

**Belum terukur (eksplisit, ≠ 0 ≠ gagal):** hyd-K-i (sengaja TANPA ML, D-A5) · stuck K-i
(persistence per spesifikasi) · hyd-K-ii & bit_wear K-1/K-2 & tool_wear K-ii & shk sub-onset
(dataset belum diproduksi D1 / pra-reg belum terbit) · kontrol-positif stuck (`labels_curated_v2`,
884 event) belum diulang V9 (masih angka V8 0/10) · C1–C4 = domain EVAL_C · B3 = butuh FP rule dari
E_RULE.

---

## 8. SUMBER ANGKA (traceability)

- `docs/V9_E_ML_ENGINE.md` — dokumen hasil induk `t_902dd141` (dirender mekanis dari JSON oleh
  `code/v9_e_ML_03_build_doc.py`). *Catatan: klaim "28 fold" (§0/§9) dan "FAR shk > 60 di semua
  titik" (§2.3) pada dokumen ini salah dan tidak diwariskan; lihat §0 di atas.*
- `scratch/v9_e_ml/v9_e_ML_vib_RESULTS.json` — 4 fold vib (§4.1, §6.1, §6.5).
- `scratch/v9_e_ml/v9_e_ML_ssi_RESULTS.json` — 9 fold ssi (§4.2, §6.2).
- `scratch/v9_e_ml/v9_e_ML_shk_RESULTS.json` — 9 fold shk (§4.3, §6.3).
- `scratch/v9_e_ml/v9_e_ML_stuck_k2_RESULTS.json` — 4 fold onset (§4.4, §6.4, §6.5).
- `scratch/v9_e_ml/v9_e_ML_stuck_k2_persistence_onset.json` — baseline persistence-onset (§4.4).
- `scratch/v9_d1/lowo_<engine>.json` — definisi fold LOWO (jumlah 4/9/9/4 = 26).
- `code/v9_e_ML_01_train.py` (harness RF/GB/LR + CI95 + baseline + assert anti-sirkular) ·
  `code/v9_d1_02_rig_windows.py` (label status vib/ssi/shk) ·
  `code/v9_d1_03_rig_datasets.py` (ekspor 55 fitur + QC + label turunan hyd) ·
  `code/v9_d1_04_stuck_k2.py` (label onset kurasi H=10) · `code/v9_d1_05_leak_lowo.py` (checker
  anti-bocor) · `code/v9_e_ML_03_build_doc.py` (builder).
- Label turunan/kurasi lintas-engine: `data/USROP_labeled.csv` (Teale high_MSE, E1d) ·
  `data/volve/labels_curated_v2.csv` (884 event DDR) · Mendeley `th4yv974r2` (tool_wear).
- Sumbu: `docs/V9_PM1_ARCHITECTURE.md` (§2 spesifikasi head ML, S1/S2/S3/S4/S5/S7/S9) ·
  `docs/V9_R1_JUSTIFICATION.md` (§3 rumus SSI/RF, §4 baseline) ·
  `docs/V9_D1_DATA_PIPELINE.md` (§2 fitur, §3 skema label, anti-bocor, LOWO) ·
  `docs/V10_PM1_OUTLINE.md` (§1 kosakata 7/11/27, §3 Bab 4, §4 aturan lintas-bab).

*Selesai V10-E_ML (`t_2db22ea0`) — porsi (e)-ML bab proposal: labeling per kelas (instrumen /
turunan / kurasi / identitas-run) + fitur 55 + protokol LOWO + kontrak RF/GB/LR + hasil nyata
**26 fold**. Dua koreksi angka terhadap draft konsultan (`t_c653c6eb`): fold 28→26 dan klaim FAR
shk. Siap digabung ke bab proposal V10 bersama keluaran peran lain (PM1 Bab 1/8, R1 Bab 2, D1 Bab 3,
E_STAT Bab 5, E_RULE Bab 6, EVAL Bab 7).*
