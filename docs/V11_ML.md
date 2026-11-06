# V11-E_ML: UJI BAB MACHINE LEARNING KEDUA KANDIDAT (LABELING, KONTRAK, HASIL FOLD) VS PRIMER

Task: `t_29d17c33` [Algorithm Engineer ML] · Papan: `capstone-v11-vs` · 2026-10-15 (WIB)
Ruang kerja dokumen: `/mnt/d/Capstone 1(v2)` · Log verifikasi: `/mnt/d/Capstone 1(v2)/scratch/v11_e_ml/`
Anonimisasi: kartu ini menyebut **kandidat 1** dan **kandidat 2** saja. Kartu ini TIDAK menyimpulkan mana versi lebih awal atau lebih akurat secara usia; penilaian angka diserahkan apa adanya ke PM-FINAL.

| Label | Berkas (dicek ulang dari path ini) | Bab ML yang diuji |
|---|---|---|
| **kandidat 1** | `/mnt/d/Capstone 1(v2)/docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.v3_arsip.md` + pasangan `.v3_arsip.ipynb` | `## 8. Data` s/d sebelum `## 14. Arsitektur` (baris 121–221, 7.470 karakter) |
| **kandidat 2** | `/mnt/d/Capstone 1(v2)/docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md` + pasangan `.ipynb` | `## Bab 4: Labeling untuk Head ML, Fitur, dan Protokol LOWO` s/d sebelum `## Bab 5` (baris 1471–1920, 31.493 karakter) |

> **Riset pendahuluan: `scientific-critical-thinking`**: OBSERVED (angka eksekusi JSON, baris kode, isi CSV) dipisah dari DESAIN (kontrak harness) dan dari KLAIM DOKUMEN; setiap kontradiksi diuji dengan tes pembeda (dua parser berbeda, dua path file, hash256) sebelum diberi status; klaim yang tidak bisa direproduksi ditulis KOREKSI, bukan dilunakkan.
> **Riset pendahuluan: `verification-mandatory`**: bukti mentah per klaim (ledger §9), cross-check kedua sumber (JSON hasil + kode pembentuk + CSV primer), daftar "belum diverifikasi" eksplisit §10, dan angka utama dihitung ulang dari file (bukan disalin dari teks dokumen).
> **Riset pendahuluan: `statistical-analysis`**: AUPRC + CI95 moving-block bootstrap (blok 60 jendela, 1.000 resample, seed 42) per fold; lift terhadap plafon `1/prev`; fold uji <30 positif = UNDERPOWERED dan dikecualikan dari hitungan mayoritas; FAR pada skala asli (jendela 1 menit → per 24 jam); baseline relevan per tugas (persistence, canary-kedalaman, prevalence-random), bukan satu baseline universal.
> **Riset pendahuluan: `sequentialthinking`** (`sequ-mcp`, 5 pikiran, 5/5 sukses): orientasi primer → sintesis bukti + kontradiksi → audit 1:1 kandidat 2 + temuan kandidat 1 → keputusan skor → gerbang penyelesaian.

---

## 0. RINGKASAN

**Skor rubrik PM-0 (30 / 30 / 25 / 15 = 100), dihitung untuk bab ML masing-masing kandidat:**

| Kriteria rubrik | kandidat 1 | kandidat 2 |
|---|---|---|
| (1) Kedalaman teknis (30) | 13 | 28 |
| (2) Akurasi terhadap primer (30) | 19 | 26 |
| (3) Kepatuhan Evaluasi User.txt (25) | 23 | 22 |
| (4) Struktur & keterbacaan (15) | 9 | 14 |
| **Total (100)** | **64** | **90** |

Rincian alasan per kriteria ada di §8. Perbandingan total, penentuan pemenang, dan pembukaan keputusan akhir = kewenangan PM-FINAL (kartu ini hanya menyajikan skor per kriteria).

**Enam temuan kunci (semua terverifikasi eksekusi, rincian di §2–§6):**

1. **Seluruh angka tabel bab ML kandidat 2 = render JSON primer, 0 selisih.** Audit otomatis: 26 baris tabel per-fold, **286 sel angka**, 20 nilai ΔB prosa, 4 baris agregat, 17 klaim prosa kunci. Ketidakcocokan: **0** (`scratch/v11_e_ml/verify10_out.txt`).
2. **Bab ML kandidat 1 tidak memuat satu pun angka hasil fold.** Regex atas seluruh dokumen kandidat 1: 0 kemunculan `AUPRC<digit>`, 0 kemunculan `0,44`/`0.44`. Satu-satunya angka lipatan yang ditulis adalah "tujuh nilai lipatan" (§11.1), dan angka itu **bertentangan dengan primer** (lihat temuan 4).
3. **Satu klaim kandidat 2 tidak bisa direproduksi dari primer sekarang**: "kolom `ts_bin` dan `lab_ts` KOSONG untuk semua 118.567 baris (4/4 well; verifikasi baca gzip mentah)". Pembacaan ulang dengan dua parser berbeda pada dua path file: **0 baris kosong**. Ditambah hash256 dataset yang tercatat di JSON hasil (`a8307db3…`) **tidak cocok** dengan file yang ada di disk (`4dfb2221…`) untuk engine `stuck_k2` (tiga engine lain cocok), sehingga file yang benar-benar dipakai saat run sudah tidak tersedia untuk diperiksa. Status: **KOREKSI** (klaim historis tak dapat dicek ulang, bukan terbukti benar). Detail di §4.3.
4. **Tiga klaim kandidat 1 bertentangan/tidak terbukti terhadap primer**: (a) "dari tujuh sumur, enam untuk latih dan satu untuk uji" dan "LOWO memberi tujuh nilai lipatan"; (b) model "Histogram-based Gradient Boosting" (kode memakai `GradientBoostingClassifier`); (c) "Skor Brier & ECE" sebagai metrik (tidak dihitung harness, 0 field di JSON). Klaim determinisme "pelaksanaan ulang wajib identik" juga bertentangan dengan JSON (`rerun_identical=False`, selisih 2,22e-16). Detail ledger: `K1-1`…`K1-8`.
5. **Kepatuhan D-A5 dan temuan persistence-onset terverifikasi**: `argparse choices` menolak `hyd_ki`/`stuck_k1` (nol ML di hyd-K-i); persistence-onset AUPRC [0.8265, 0.9016] mengalahkan RF [0.0697, 0.4443] di **4/4 fold**, B1 persistence = 1.0 di keempat well. Kandidat 2 menuliskan keduanya; kandidat 1 tidak menyebut D-A5 tetapi tabel §15.1-nya konsisten (hyd = "Statistik (median/MAD) + persistence"). §5.
6. **md = ipynb lolos untuk bab ML di kedua kandidat** (kandidat 1: 0/70 baris §8–13 hilang; kandidat 2: 0/371 baris Bab 4 hilang). Satu artefak format ditemukan **di luar bab ini** (lihat §6.3). §6.

---

## 1. PRIMER DAN CARA VERIFIKASI

**Sumber primer (dibaca/dijalankan, bukan dikutip dari dokumen kandidat):**

| Sumber | Isi yang dipakai |
|---|---|
| `scratch/v9_e_ml/v9_e_ML_{vib,ssi,shk,stuck_k2}_RESULTS.json` | 26 fold: AUPRC/CI95/lift/plafon, ΔB, tau metrics, agregat, determinism, hyperparams, software |
| `scratch/v9_e_ml/v9_e_ML_stuck_k2_persistence_onset.json` | B1, TLead median, n_events/n_detected per well |
| `code/v9_e_ML_01_train.py` | kontrak RF/GB/LR, seed, taus, imputer fold-safe, CI95 bootstrap, `UNDERPOWERED_POS=30`, assert anti-sirkularitas (baris 192–193), `ALLOWED`/argparse (D-A5) |
| `code/v9_d1_02_rig_windows.py` | `W=10`, `MIN_DRILL_BINS=5`, `MIN_DRILL_ROWS=60`, `VIB_THRESH=32.17405`, `SSI_MIN_SAMPLES=10`, `STATS=[mean,std,slope,last,frac]`, stempel `feat_ts_max < lab_ts` |
| `code/v9_d1_03_rig_datasets.py` | `NQ=10`, `W=10`, `HYD_EXCLUDE=[SPPA,TFLO,SPM]`, qcut + median/MAD + `|z|>2`, agregasi `>=0.5` menit anom |
| `code/v9_d1_04_stuck_k2.py` | `H=10`, strict-past `[t0-10, t0)`, `REF_ONSETS` |
| `scratch/v9_d1/lowo_*.json` (6 file) | jumlah fold & well per engine |
| `scratch/v9_d1/v9_d1_04_qc.json` | onsets_ffill/strict/scorable + `v8_onsets_match` per well |
| `scratch/v9_d1/v9_d1_05_leak_lowo.json` | 6 entri dataset, hitungan pelanggaran anti-bocor, waktu pemeriksaan |
| `scratch/v9_d1/datasets/stuck_k2.csv.gz` | pembacaan ulang isi (csv module + pandas), hash256 |
| `data/USROP_labeled.csv`, `data/volve/labels_curated_v2.csv` | label Teale, 884 event kurasi |
| `docs/V9_E_ML_ENGINE.md`, `docs/V9_PM1_ARCHITECTURE.md`, `docs/V10_PM1_OUTLINE.md` | dokumen hasil induk, definisi D-A5, kosakata 7 engine / 11 klaim / 27 head |
| `/mnt/d/Capstone 1(v2)/Evaluasi User.txt` | instrumen penilaian (6 prinsip + lapisan A/B/C) |

**Cara verifikasi.** Sepuluh skrip Python dijalankan dengan `python3` dari ruang kerja kartu, log lengkap disalin ke `scratch/v11_e_ml/` (`verify_out.txt`, `verify2_out.txt`, `verify3_out.txt`, `verify5_out.txt`, `verify6_out.txt`, `verify7_out.txt`, `verify8_out.txt`, `verify9_out.txt`, `verify10_out.txt`, `ipynb_out.txt`). Total pemeriksaan terotomasi: **286 sel angka tabel + 20 nilai ΔB + 4 baris agregat + 17 klaim prosa kunci + 28 entri ledger klaim**. JSON primer (manifest hash + data fold terurai + ledger) tersimpan di `scratch/v11_e_ml/V11_ML_PRIMER.json` (50.275 byte).

**Catatan pembacaan primer.** Field `dataset_sha256` pada keempat JSON hasil cocok dengan isi file dataset saat ini untuk `vib`, `ssi`, `shk`, dan **tidak cocok** untuk `stuck_k2` (§4.3). Field `dataset` pada JSON menunjuk path `/mnt/d/Capstone 1/…`, sedangkan file di dua path (`/mnt/d/Capstone 1` dan `/mnt/d/Capstone 1(v2)`) berbeda hanya pada engine `stuck_k2` (hash tiga engine lain sama persis di dua path).

---

## 2. TUGAS 1: LABELING PER KELAS: BENAR & LENGKAP?

Primer labeling yang dicek: kode pembentuk label + CSV + `klaim_tugas` di JSON.

| Kelas | Primer (kode/CSV) | kandidat 1 | kandidat 2 (Bab 4 §1) |
|---|---|---|---|
| `vib` (instrumen) | `VIB_THRESH=32.17405` di `v9_d1_02:35`; JSON klaim "status VIBLAT>=32.17405" | Tidak dijelaskan per kelas; hanya "kanal pembentuk label dilarang jadi fitur" | **Instrumen**, rumus `1[max VIBLAT_RT >= 32,17405]`, berkas `v9_d1_02` → **benar** |
| `shk` (instrumen) | `LABDEF` thr 1.0 di `v9_d1_02:39-40` | idem | **Instrumen**, `1[max SHKRSK_RT >= 1]` → **benar** |
| `ssi` (turunan fisika) | `SSI_MIN_SAMPLES=10` + `(max-min)/(2*mean)`, `v9_d1_02:34,93` | idem | **Turunan fisika dari CRPM**, ≥10 sampel, `mean>0` → **benar** |
| `stuck K-ii` (kurasi onset) | `H=10` di `v9_d1_04:41`; onset edge `0→1` ffill; baris inblock dibuang | idem | **Kurasi kejadian**, jendela `[t_e-10, t_e)`, baris dalam blok dibuang → **benar** |
| `hyd K-i` (turunan residu) | `NQ=10`, `W=10`, z `(SPPA-median)/(1.4826*MAD)` per bin qcut TFLO, `\|z\|>2`, `>=0.5` menit anom, `v9_d1_03:63-70,101` | Tidak diuraikan; tabel §15.1 hanya "Statistik (median/MAD) + persistence" (konsisten) | Rumus identik + "SPPA/TFLO/SPM dibuang → 8 kanal" (`HYD_EXCLUDE`) → **benar** |
| `bit_wear K-1` (turunan Teale) | `USROP_labeled.csv`: 198.928 baris; label `high_MSE_bit_wear` = 49.732 baris = **100%** baris MSE > P75 = **256.600,424** (cross-tab eksak) | Disebut sebagai "keausan bit" tanpa rumus | `high_MSE = Teale MSE > P75 = 256,600 psi` → **benar** (satuan psi tak punya kolom unit di CSV: status DIDUKUNG utk satuan) |
| `tool_wear K-ii` (identitas-run) | Mendeley `th4yv974r2` (eksternal, di luar lingkup offline) | Disebut sebagai "keausan mata bor" tanpa rumus | **Identitas-run**, bukan turunan fitur, modul terpisah D-A7 → **tidak dapat diverifikasi offline** (sumber eksternal) |
| kontrol 884 event | `labels_curated_v2.csv`: 884 baris, `bha_relevant` = yes **50** / uncertain **571** / no **263** | Disebut "884 label peristiwa terkurasi" (benar) | **884 event (50/571/263)** sebagai kontrol-positif, bukan label latih → **benar persis** |
| anti-sirkularitas | assert `v9_e_ML_01_train.py:192-193` | Prinsip: "kanal pembentuk label dilarang menjadi fitur" (tanpa bukti kode) | Kutip assert + baris 192–193 + tabel kanal terlarang per kelas → **benar** |

**Jawaban tugas 1.**
- **kandidat 2: benar dan lengkap.** Empat kelas sumber label (instrumen / turunan fisika / kurasi kejadian / identitas-run) diuraikan dengan rumus, berkas pembentuk, dan kolom "Dilatih di kartu ini?"; seluruh angka rumus terverifikasi ke kode/CSV kecuali dataset Mendeley `th4yv974r2` (sumber eksternal, masuk daftar §10).
- **kandidat 1: benar tetapi tidak lengkap.** Bab ML-nya hanya menyebut tujuh kelas target dan prinsip anti-sirkularitas; tidak ada labeling per kelas, tidak ada rumus, tidak ada berkas pembentuk. Tidak ditemukan kesalahan label eksplisit di kandidat 1 karena memang tidak ada klaim label yang bisa diuji.

---

## 3. TUGAS 2: KONTRAK (55 FITUR, KETAT-LALU, LOWO, SEED, IMPUTER, TANPA GRID, TAU PRA-REG, UNDERPOWERED) SESUAI KODE?

| Butir kontrak | Primer (kode/JSON) | kandidat 1 | kandidat 2 | Status kandidat 2 |
|---|---|---|---|---|
| Fitur 55 = 11 kanal × 5 stat | `n_features=55` di 4 JSON; `feature_cols` 55 dan **identik** antar engine; `STATS=[mean,std,slope,last,frac]` | Ditulis "55 fitur dari 11 kanal MWD" + 5 statistik (mean, std, slope, last, fraksi) → **cocok** | Ditulis lengkap dengan detail `std(ddof=1)`, `slope OLS butuh cnt≥3 & den>1e-9`, `frac = non-null/10`, 11 kanal disebut satu per satu → **cocok** | TERBUKTI |
| Jendela ketat-lalu `[t0-10, t0)` | `v9_d1_02:6`, `v9_d1_03:6`, `v9_d1_04:14,72-73`; invariant `feat_ts_max < lab_ts` | Prinsip "fitur selalu berstempel waktu lebih awal daripada peristiwa" (benar, tanpa notasi jendela) | Ditulis eksplisit `[t0-10, t0)` + invariant S5 + selisih terhadap rolling V8 `t-9..t` → **cocok** | TERBUKTI |
| LOWO per fold | `lowo_*.json`: fold = vib 4, ssi 9, shk 9, stuck_k2 4, stuck_k1 2, hyd_ki 9; well = 9 / 4 / 2 | "dari tujuh sumur, enam latih satu uji" + "tujuh nilai lipatan" → **bertentangan** | "26 fold total: 4+9+9+4", fold per engine disebut wellnya satu per satu → **cocok** | TERBUKTI |
| seed 42 | `SEED=42` (`train.py:51`), `random_state=42` semua model, seed bootstrap per fold | "Benih acak tetap (42)" → cocok | "seed 42" di kontrak → cocok | TERBUKTI |
| Imputer fold-safe | `train.py:252-253` fit hanya `X_tr`; LR pipeline imputer fold-safe | "Imputasi median di-fit hanya di dalam fold latih" → **cocok** | "di-fit hanya dari data latih fold itu, tidak ada statistik data uji yang bocor" → **cocok** | TERBUKTI |
| Tanpa grid search | Tidak ada `GridSearchCV`/`RandomizedSearchCV`; hyperparams dikunci | "Pencarian hiperparameter berskala luas sengaja tidak dilakukan" → **cocok** (berbeda istilah) | "hyperparameter dikunci (DESAIN tetap), tidak ada pencarian" → **cocok** | TERBUKTI |
| Tau pra-reg | `TAUS=[0.05,0.10,0.20,0.30,0.50]` (`:58`), semua titik dilaporkan; onset + `q95` skor latih | Tidak disebut | Ditulis lengkap + alasan anti shopping-for-significance + `q95_train` pra-reg E3 → **cocok** | TERBUKTI |
| UNDERPOWERED < 30 | `UNDERPOWERED_POS=30` (`:61`), `underpowered = n_pos < 30`; fold UP = ssi F-7 (3 pos), F-9 (12 pos) | Tidak disebut (hanya "unit positif per lipatan kecil" sebagai alasan menolak deep learning) | "<30 positif dilabeli dan dikecualikan dari mayoritas; UP: F-7 (3), F-9 (12)" → **cocok** | TERBUKTI |
| Kontrak RF/GB/LR | RF 300 (`stuck_k2` 200) / `min_samples_leaf=5` / `balanced_subsample`; GB 200 / 0.1 / 3; LR median + scaler + `max_iter=1000` / `balanced` | Peran model saja (RF, regresi logistik, "Histogram-based GB"), **tanpa kontrak angka**; nama GB tidak cocok (K1-2) | Tabel §3 identik dengan `make_models()` dan JSON `hyperparams` (termasuk `n_jobs=-1` dan catatan 200 pohon untuk onset) → **cocok** | TERBUKTI |
| CI95 + FAR | moving-block bootstrap circular, blok 60, 1.000 resample, seed 42; `FAR_24 = 1440*FP/n_neg` | Tidak disebut | Ditulis lengkap + rumus FAR + definisi "60/20/10" S7 → **cocok** | TERBUKTI |

**Jawaban tugas 2.** Kandidat 2 memuat seluruh butir kontrak dan seluruhnya cocok dengan kode/JSON. Kandidat 1 memuat 5 dari 9 butir pada taraf prinsip (fitur 55, anti-bocor, LOWO, seed, imputer fold-safe, tanpa grid search) dengan satu klaim kontradiktif pada LOWO, dan tidak memuat kontrak hyperparameter, tau pra-reg, aturan UNDERPOWERED, maupun definisi CI95/FAR.

---

## 4. TUGAS 3: ANGKA HASIL PER FOLD DILACAK KE JSON

### 4.1 kandidat 2: audit 1:1 otomatis

| Yang dicocokkan | Jumlah | Selisih |
|---|---|---|
| Baris tabel per-fold (n, pos, prev, UP, RF, CI95 bawah/atas, GB, LR, persistence, canary, prev-random) | 26 baris / **286 sel angka** | **0** |
| Nilai ΔB prosa (vs persistence & vs canary, 4 engine) | **20 nilai** | **0** |
| Baris ringkasan agregat (rentang RF, spread, hitungan ΔB>0) | 4 engine × 4 butir | **0** |
| Klaim prosa kunci (26 fold, lift 1,61/2,36/3,50/1,63, rentang persistence-onset, 135 titik/53 FAR≤60, 10 dari 402 titik, determinisme 2,22e-16, UP F-7/F-9, assert baris 192–193, 884 (50/571/263), P75 256,600, onset 72/93/61/55, sklearn 1.9.1, koreksi 28→26, median run 10 menit, 6/7 baris positif) | 17 klaim hadir | 17 dari 17 diverifikasi; **16 benar, 1 gagal** (lihat §4.3) |

Contoh cocok persis (dari `verify10_out.txt`): baris agregat `vib` rentang `[0.4405, 0.9117]` dan JSON `[0.44052428575087504, 0.911676937088842]`; `stuck_k2` persist `[0/4]` dan JSON `0/4 fold layak`; lift RF per fold `[1.6133, 2.362, 3.4972, 1.6289]` dibulatkan kandidat 2 menjadi `1,61 / 2,36 / 3,50 / 1,63`.

**Angka mekanisme yang dicek ulang dan terbukti** (tidak hanya dikutip):
- median run label positif onset = **10,0 menit** (148 run; distribusi terbanyak 10 = 100 run) → cocok dengan klaim "kontigu (median run 10 menit)".
- dari 1.975 baris positif `stuck_k2`, **1.694 (85,8%)** punya `y_prev==1` → klaim "y(t-1)=1 pada ±6/7 baris positif" (85,7%) **terkonfirmasi** (klaim itu tidak membawa angka di dokumen, jadi saya hitung sendiri).
- klaim FAR: 135 titik shk → **53** titik FAR≤60, hanya **1** titik FAR≤6 & recall>0 (`F-14 / rf / 0.3 : FAR 0,69, R 0,0053`); seluruh engine → **402** titik, **10** titik memenuhi, detail identik dengan daftar di dokumen (vib 1, ssi 5, shk 1, stuck 3).

### 4.2 kandidat 1: tidak ada angka fold

Hasil regex seluruh dokumen kandidat 1: 0 kemunculan `AUPRC<digit>`, 0 kemunculan `0,44`/`0.44`, 0 tabel fold, 0 daftar traceability per angka (§19.3 hanya sitasi dokumen `[A-1]…[A-13]`). Satu-satunya klaim berangka terkait lipatan: **"LOWO memberi tujuh nilai lipatan"** dan **"dari tujuh sumur, enam untuk latih dan satu untuk uji"**.

Primer (`scratch/v9_d1/lowo_*.json`):

| file | n_fold | wells field |
|---|---|---|
| `lowo_hyd_ki.json` | 9 | 9 well (F-10, F-12, F-14, F-15A, F-15_S, F-5, F-7, F-9, F-9_A) |
| `lowo_shk.json` | 9 | 9 well |
| `lowo_ssi.json` | 9 | 9 well |
| `lowo_vib.json` | 4 | 4 well |
| `lowo_stuck_k2.json` | 4 | 4 well |
| `lowo_stuck_k1.json` | 2 | 2 well |

Tidak ada konfigurasi LOWO dengan **7** fold maupun **7** well, sehingga klaim kandidat 1 **KOREKSI** (ledger `K1-1`). Angka fold bab ML yang benar (26 = 4+9+9+4) hanya ditulis oleh kandidat 2, lengkap dengan koreksi terhadap angka 28 yang memang tercatat di `docs/V9_E_ML_ENGINE.md` baris 43 dan 468 (dicek langsung).

### 4.3 Kontradiksi yang wajib dilaporkan: kolom `ts_bin`/`lab_ts` dan hash dataset `stuck_k2`

**Klaim dokumen** (kandidat 2 Bab 4 §7, identik dengan `docs/V9_E_ML_ENGINE.md` §7): "Kolom `ts_bin` dan `lab_ts` pada `scratch/v9_d1/datasets/stuck_k2.csv.gz` KOSONG untuk semua 118.567 baris (4/4 well; verifikasi baca gzip mentah)".

**Empat pengamatan mentah (diurutkan, tanpa dipilih):**

1. Pembacaan dengan `csv.DictReader` atas `gzip.open(...)`: rows = 118.567; nilai contoh `ts_bin='20649209'`, `lab_ts='20649209.0'`; hitungan kosong/`nan` untuk `ts_bin` = **0**, untuk `lab_ts` = **0**.
2. Pembacaan ulang dengan `pandas.read_csv`: `ts_bin` dtype `int64` NaN **0**; `lab_ts` dtype `float64` NaN **0**; `feat_ts_max` NaN **0**; `lab_kind` terisi (`onset_horizon_neg` 116.592, `onset_event` 1.975).
3. File di dua path (`/mnt/d/Capstone 1(v2)/…` dan `/mnt/d/Capstone 1/…`) **identik** (sha256 prefix `acb9ebeaa64b147983ca5f5fe0f940b6`, mtime sama), jadi bukan kasus file lama vs file baru.
4. `dataset_sha256` yang tercatat di `v9_e_ML_stuck_k2_RESULTS.json` = `a8307db3c49ffa75187abea07fbbb73afbde8f23d94252a8a9a5a8577333271f`, sedangkan hash prefix file yang ada sekarang = `4dfb2221aa8e385753daf505e8e61c5b7c0625350e31f094858e36678b8af142` (**tidak cocok**). Untuk `vib`, `ssi`, `shk` hash JSON **cocok** file saat ini (metode identik dengan kode: `sha256(read(2**20))`).

**Inferensi (ditandai sebagai inferensi, bukan fakta):** file dataset yang dibaca saat run 10-12 10:03 tidak lagi berada di disk; file yang ada sekarang sudah berisi kolom waktu. Dengan kata lain klaim "kolom kosong" tidak dapat dibuktikan dan tidak dapat dibantah terhadap file semasa run, dan **terbantah terhadap file di path yang diklaim sekarang**. Pendukung tambahan: `v9_d1_05_leak_lowo.json` ber-`mtime` 10-12 **08:46**, lebih tua dari file dataset 10-12 **09:37**, sehingga angka "0 pelanggaran" berasal dari versi pemeriksaan yang lebih awal daripada file dataset yang ada sekarang.

**Akibat bagi skor.** Klaim ini dan hilirnya ("leak-check `stuck_k2` = vacuous") diberi status **KOREKSI** (tidak terbukti terhadap primer sekarang). Karena kandidat 2 **mengklaim verifikasi langsung** ("verifikasi baca gzip mentah") dan verifikasi ulang saya tidak menemukan kekosongan itu, klaim ini tidak dapat menerima poin ketelusuran. Seluruh klaim lain di bab ini lolos (§9). Kandidat 1 tidak memuat klaim ini.

---

## 5. TUGAS 4: RF DILARANG DI hyd K-i (D-A5) DAN PERSISTENCE-ONSET MENANG 4/4

**D-A5 (primer):** `docs/V9_PM1_ARCHITECTURE.md:130`: "Larangan RF spesifik kelas: hyd-K-i **DILANGGAN** (ΔB negatif 7/7, replikasi eksak); larangan ini TIDAK digeneralisasi ke kelas lain". Pada kode: `v9_e_ML_01_train.py:82-85` `ALLOWED = {vib, ssi, shk, stuck_k2}` dan `:179` `ap.add_argument("--engine", choices=list(ALLOWED))`, sehingga `hyd_ki` dan `stuck_k1` **tidak bisa dijalankan** (0 ML di hyd-K-i, stuck-K-i = persistence). Kepatuhan: **TERBUKTI**.

| Kandidat | Pernyataan | Status |
|---|---|---|
| kandidat 2 | §3 "kepatuhan larangan (D-A5): harness menolak engine di luar daftar (`argparse choices`)… hyd-K-i = nol ML" | **TERBUKTI** (cocok kode) |
| kandidat 1 | Tidak menyebut D-A5; tabel §15.1 baris hidraulik = "Statistik (median/MAD) + persistence" | **DIDUKUNG** (konsisten, tanpa rujukan larangan) |

**Persistence-onset menang 4/4 vs RF (primer JSON):**

| Well | persistence AUPRC | RF AUPRC | ΔB RF−persistence | persistence B1 | persistence TLead (mnt) | RF q95 B1 | RF q95 TLead | RF deteksi |
|---|---|---|---|---|---|---|---|---|
| F-10 | 0,9016 | 0,1997 | −0,7019 | 1,000 | 9,0 | 0,657 | 10,0 | 44/67 |
| F-14 | 0,8438 | 0,0704 | −0,7734 | 1,000 | 9,0 | 0,000 | n/a | 0/28 |
| F-9 | 0,8265 | 0,0697 | −0,7569 | 1,000 | 10,5 | 1,000 | 11,5 | 16/16 |
| F-9_A | 0,8890 | 0,4443 | −0,4446 | 1,000 | 9,0 | 1,000 | 10,0 | 37/37 |

`agregat.rf.deltaB_vs_persistence_pos` = `0/4 fold layak`; `persistence_onset.json` B1 = 1.0 di keempat well.

| Kandidat | Pernyataan | Status |
|---|---|---|
| kandidat 2 | "persistence-onset AUPRC 0,8265–0,9016 mengalahkan RF 0,0697–0,4443 di 4/4 fold; B1 persistence = 1,0 semua well; TLead median 9–10,5" + tabel B1/TLead per well + interpretasi "KEMAMPUAN baseline + BATAS formulasi label, bukan kegagalan ML" | **TERBUKTI** (semua angka cocok 1:1) |
| kandidat 1 | Tidak ada klaim onset; hanya "pada sebagian tugas persistence terbukti terbaik dan dicatat sebagai kemampuan" | **DIDUKUNG** (benar sebagai pernyataan umum, tanpa angka) |

---

## 6. TUGAS 5: KEPUTUSAN md = ipynb UNTUK BAB INI

| Kandidat | Baris bab ML di `.md` | Hilang di `.ipynb` | Sel `.ipynb` | Keputusan |
|---|---|---|---|---|
| kandidat 1 | 70 baris non-kosong (`## 8. Data` s/d `## 14. Arsitektur`) | **0 (0,0%)**; semua heading `#` di md ada di ipynb (43/43) | 37 sel (25 markdown + 12 code) | **KONSISTEN** |
| kandidat 2 | 371 baris non-kosong (Bab 4 penuh) | **0 (0,0%)**; heading md 208/208 hadir di ipynb | 221 sel (209 markdown + 12 code) | **KONSISTEN** |

Kedua `.ipynb` juga memuat blok kode di luar narasi yang ditandai sendiri sebagai "ARSIP VISUALISASI KAMPANYE LAMA (BUKAN BAGIAN NARASI PROPOSAL)", sehingga `.ipynb` = superset `.md` (syarat "memuat isi yang sama" terpenuhi; kelebihannya ditandai eksplisit di dalam file).

**6.3 Catatan lintas-bab (di luar cakupan bab ML, untuk tim bab terkait).** Satu sel markdown `.ipynb` kandidat 2 (sel #45) memuat teks literal berupa backslash + `n` di tengah baris (`…v8_e_shk_02b,` + `\n` + `bukan V9…`), padahal `.md` memakai line break sungguhan. Posisi teks itu berada di seksi `### 2. ALASAN PER ENGINE: FISIKA KEGAGALAN → SENSOR RELEVAN → METODE` (Bab 2), bukan Bab 4, sehingga tidak memengaruhi keputusan md=ipynb bab ML. Jumlah literal `\n` di `.md` kandidat 2 = 0.

---

## 7. TUGAS 6: KELENGKAPAN: APA YANG HILANG DI SATU KANDIDAT TETAPI ADA DI KANDIDAT LAIN

**7.1 Hilang di kandidat 1, ada di kandidat 2 (bab ML):**

| Isi | Bukti kehadiran di kandidat 2 | Bukti ketiadaan di kandidat 1 |
|---|---|---|
| Labeling per kelas dgn 4 kelas sumber label + rumus + berkas pembentuk + tabel kanal terlarang + kutipan assert | Bab 4 §1 (§1.1, §1.2) | 0 bagian labeling per kelas |
| Kontrak hyperparameter RF/GB/LR (angka persis) | Bab 4 §3 | hanya peran model, tanpa angka |
| Hasil 26 fold (AUPRC, CI95, lift, ΔB, P/R/FAR, B1/TLead) | Bab 4 §4.1–4.4 | **0 angka fold** |
| Tau pra-reg `{0,05;0,10;0,20;0,30;0,50}` + `q95_train` + alasan anti shopping-for-significance | Bab 4 §2.2–2.3 | 0 kemunculan |
| Aturan UNDERPOWERED <30 positif + daftar fold UP | Bab 4 §2.2 | 0 kemunculan (hanya alasan menolak deep learning) |
| CI95 moving-block bootstrap (blok 60, 1.000, seed 42) + rumus `FAR_24` | Bab 4 §2.3 | 0 kemunculan |
| Larangan D-A5 + paksaan kode + temuan persistence-onset 4/4 + mekanismenya | Bab 4 §3, §6.4 | tidak ada (hanya tabel §15.1 yang implisit) |
| Penjelasan kosakata 7 / 11 / 27 dari sudut ML | Bab 4 §5 (`7 vs 11 vs 27`, 1 kemunculan) | 0 kemunculan `7 vs 11 vs 27`, `11 klaim`, `27 head` (kerangkanya "7 mesin / 121 klaim") |
| Baris "Riset pendahuluan: `<skill>`" per output | Bab 4: 6 baris; dokumen: 51 baris, 34 baris berisi nama skill | dokumen kandidat 1: **0** baris nama skill; hanya kebijakan "Tiap keluaran kerja mencantumkan rujukan riset pendahuluan" (§19.2) |
| Daftar traceability per angka | Bab 4 §8 "SUMBER ANGKA" (per JSON + per kode) | §19.3 sitasi dokumen `[A-1]…[A-13]`, tanpa peta angka |
| Disclosures: koreksi angka draft, defect dataset D1, "belum terukur" | Bab 4 §0, §7 | tidak ada padanan di bab ML |

**Catatan soal LogReg / GB sebagai pembanding** (contoh yang disebut di brief): pembanding **ada di kedua kandidat**, tetapi kedudukannya berbeda. kandidat 1 memuat "Regresi logistik = baseline interpretable" dan "Histogram-based Gradient Boosting = model utama kedua" di tabel §9.2 (peran + alasan, tanpa kontrak, tanpa angka, dan nama GB tidak cocok dengan kode: `K1-2`). kandidat 2 memuat kontrak ketiga model (§3) plus angka GB dan LR per fold di setiap tabel (286 sel sudah termasuk kolom GB/LR). Jadi yang hilang di kandidat 1 bukan keberadaan pembanding, melainkan kontrak dan hasilnya.

**7.2 Hilang di kandidat 2, ada di kandidat 1 (bab ML):**

| Isi | Bukti kehadiran di kandidat 1 | Bukti ketiadaan di kandidat 2 |
|---|---|---|
| Justifikasi penolakan *deep learning* ujung-ke-ujung (unit positif per lipatan kecil → risiko peng-fittingan) | §9.2, 1 kemunculan | **0** kemunculan "deep learning" di seluruh dokumen kandidat 2 |
| Definisi penuh lapisan A, B, C (apa yang diukur tiap layer) | §11.2 (Lapisan A/B/C masing-masing 1 kemunculan di bab ML) | Bab 4 hanya 1 penyebutan `A/B/C`; definisi layer ada di Bab 7 (di luar bab ML) |
| Metrik **Brier & ECE** (kejujuran skor probabilistik) | §13 tabel metrik | 0 kemunculan di seluruh dokumen kandidat 2. *Catatan primer: metrik ini tidak dihitung harness (`K1-3`), jadi nilainya sebagai rencana, bukan hasil.* |
| Pemisahan peran pemeriksa (pemeriksa data / insinyur data / insinyur ML / auditor / penilai akhir) | §10, 2 kemunculan | 0 kemunculan di bab ML kandidat 2 |
| Keterbatasan validasi implisit di bab ML: satu lapangan, label sebagian proxy, pembagian temporal murni belum terpisah dari LOWO | §11.3 + §8.2 (`lintas lapangan` 1 kemunculan di bab ML) | Bab 4 §7 membahas "belum terukur" yang berbeda (C1–C4, B3, kontrol-positif); batas lintas-lapangan/temporal tidak diulang di Bab 4 |
| Tabel "keputusan vs alternatif ditolak" untuk pemilihan metode | §12 | Bab 4 §3 memberi alasan per model, tanpa tabel alternatif ditolak |

**7.3 Keseimbangan.** kandidat 1 lebih kaya pada kerangka penilaian dan batas metodologis; kandidat 2 lebih kaya pada bukti numerik, kontrak, dan ketelusuran. Keduanya memuat pembanding statistik (LR) dan boosting; tidak ada kandidat yang menghapus pembanding tersebut.

---

## 8. SKOR RUBRIK PM-0, ALASAN PER KRITERIA

### kandidat 1: `/mnt/d/Capstone 1(v2)/docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.v3_arsip.md` (bab `## 8` s/d `## 13`)

| Kriteria | Skor | Alasan perolehan | Alasan potongan |
|---|---|---|---|
| (1) Kedalaman teknis 30 | **13** | Kerangka metode jelas: peran tiap model + alasan (§9.2), penolakan deep learning (§9.2), pra-registrasi (§9.3), prapemrosesan fold-safe (§8.3), alasan pemilihan metode (§12), metrik (§13) | Tidak ada labeling per kelas, tidak ada kontrak hyperparameter, tidak ada workflow harness (imputasi/bootstrap/tau/UP), tidak ada bukti per klaim di bab ini (0 bukti angka) |
| (2) Akurasi terhadap primer 30 | **19** | 4 klaim kecil terbukti (`K1-5`…`K1-8`: 55 fitur/5 statistik, imputer fold-safe, USROP 198.928×12, 884 label) dan tidak ada angka fold yang salah karena memang tidak ada angka | Klaim `K1-1` (7 sumur / 7 lipatan) **KOREKSI**; `K1-2` (Histogram-based GB) **KOREKSI**; `K1-4` (re-run identik) **KOREKSI**; `K1-3` (Brier & ECE) **HIPOTESIS** tanpa primer hasil; ketelusuran angka fold utama = 0 |
| (3) Kepatuhan Evaluasi User.txt 25 | **23** | Lapisan A/B/C didefinisikan penuh (§11.2); jenis tugas dibedakan (§9.1); baseline relevan per tugas, bukan universal (§12); kemampuan + batas tanpa vonis biner (§11.2, §15.2); nilai di tingkat alat (Tingkat 1/2/3, §15.2); transparansi ketidakpastian (§15.3, R1–R7) | Kekuatan bukti tidak terikat pada bab/hasil ML (hanya pada klaim umum §15.3); "nilai keberhasilan pada tingkat alat" ada di §15, di luar bab ML |
| (4) Struktur & keterbacaan 15 | **9** | Outline 19 bab + daftar isi konsisten; bab ML runtut (Data → Metodologi → Validasi → Alasan → Metrik); md = ipynb rapi (0 baris hilang) | 0 penjelasan 7/11/27 (kerangka berbeda: 7 mesin / 121 klaim); 0 baris "Riset pendahuluan: `<skill>`"; tidak ada daftar traceability per angka |
| **Total** | **64** | | |

### kandidat 2: `/mnt/d/Capstone 1(v2)/docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md` (bab `## Bab 4`)

| Kriteria | Skor | Alasan perolehan | Alasan potongan |
|---|---|---|---|
| (1) Kedalaman teknis 30 | **28** | Labeling per kelas dgn rumus + berkas + assert runtime; kontrak RF/GB/LR apa adanya; detail fitur (5 statistik + eligibility); protokol LOWO per engine; metrik + CI95 + baseline + onset; temuan per engine; §7 batas/defect; §8 traceability | Klaim mekanisme "±6/7 baris positif" ditulis tanpa angka pendukung di dokumen (angka itu ada di data: 85,8%, tetapi tidak dipaparkan); ketegangan internal §1.2 ("0 pelanggaran 6/6" tanpa syarat) vs §7 (entri stuck_k2 vacuous) |
| (2) Akurasi terhadap primer 30 | **26** | 286 sel tabel + 20 ΔB + 4 baris agregat + 17 klaim prosa diverifikasi, **0 selisih**; labeling, kontrak, D-A5, persistence-onset, hitungan FAR, hitungan UP, onset per well, P75 USROP, 884 label semua terbukti | `K2-16` (kolom `ts_bin`/`lab_ts` kosong 118.567 baris) **KOREKSI**, gagal direproduksi dengan dua parser + dua path, dan hash dataset tercatat tidak cocok file sekarang; `K2-17` (klaim leak-check tanpa syarat) hanya **DIDUKUNG** dan pemeriksaannya lebih tua dari file dataset (tidak diungkap dokumen) |
| (3) Kepatuhan Evaluasi User.txt 25 | **22** | Jenis tugas dibedakan tegas (`status_detection` vs `onset_prediction`); baseline relevan per kelas (persistence/canary/prevalence-random + persistence-onset E0); tau seragam dengan semua titik dilaporkan (tanpa pilih hasil); kemampuan + batas + kekuatan bukti per fold; nilai di tingkat alat (L2 skor-ranking, tanpa kenaikan tier otomatis); vonis eksplisit "bukan lulus/gagal" | Lapisan A/B/C hanya 1 penyebutan di Bab 4, definisi layer diberikan di Bab 7 (di luar bab ini) |
| (4) Struktur & keterbacaan 15 | **14** | 8 sub-bab runtut (ringkas → labeling → fitur → kontrak → hasil → kosakata 7/11/27 → temuan → traceability); penjelasan 7/11/27 ada (§5); md = ipynb konsisten 0/371 baris; 6 baris "Riset pendahuluan" ber-skill | Kepadatan tinggi (tabel per-fold 12 kolom, §0 koreksi panjang); artefak literal `\n` di sel `.ipynb` luar bab ini (§6.3) menandai paket keseluruhan belum sempurna |
| **Total** | **90** | | |

Perbandingan total, mayoritas kriteria, dan kelayakan menang menurut definisi protokol = urusan PM-FINAL. Kartu ini tidak menyimpulkan pemenang dan tidak menyebut mana kandidat lebih awal.

---

## 9. LEDGER KLAIM (28 ENTRI)

Format status: `TERBUKTI` (langsung dari alat) · `DIDUKUNG` (indirek/konsisten) · `HIPOTESIS` (tak punya primer hasil) · `KOREKSI` (klaim gugur). Rekap: **22 TERBUKTI · 1 DIDUKUNG · 1 HIPOTESIS (bercampur di 4 entri) · 4 KOREKSI**.

| ID | Kandidat | Klaim (ringkas) | Status |
|---|---|---|---|
| K1-1 | 1 | "tujuh sumur, enam latih satu uji" + "tujuh nilai lipatan" (§11.1) | **KOREKSI** (primer: fold 4/9/9/2/4; well 9/4/2; tak pernah 7) |
| K1-2 | 1 | "Histogram-based Gradient Boosting" (§9.2) | **KOREKSI** (kode `GradientBoostingClassifier`) |
| K1-3 | 1 | "Skor Brier & ECE" sbg metrik (§13) | **HIPOTESIS** (0 field Brier/ECE di harness & 4 JSON) |
| K1-4 | 1 | "pelaksanaan ulang wajib identik" (§10) | **KOREKSI** (JSON `rerun_identical=False`, diff 2,22e-16) / DIDUKUNG sbg persyaratan desain |
| K1-5 | 1 | 55 fitur dari 11 kanal; mean/std/slope/last/fraksi (§8.2) | **TERBUKTI** |
| K1-6 | 1 | imputasi median hanya di fold latih (§8.3, §11.1) | **TERBUKTI** |
| K1-7 | 1 | USROP 198.928 baris × 12 sensor; 884 label (§8.1) | **TERBUKTI** |
| K1-8 | 1 | bab ML memuat 0 angka hasil fold | **TERBUKTI** (regex 0 kemunculan) |
| K2-1 | 2 | 26 fold (4+9+9+4); angka 28 di dokumen induk dikoreksi | **TERBUKTI** (jumlah folds JSON = 26; `V9_E_ML_ENGINE.md`:43 & 468 = "28 fold"; `lowo_stuck_k1` = 2) |
| K2-2 | 2 | seluruh tabel fold Bab 4 = render JSON | **TERBUKTI** (286 sel, 0 selisih; 20 ΔB, 0 salah) |
| K2-3 | 2 | lift RF vib 1,61/2,36/3,50/1,63 | **TERBUKTI** (JSON 1,6133/2,3620/3,4972/1,6289) |
| K2-4 | 2 | persistence-onset 4/4 menang; B1 1,0 semua well | **TERBUKTI** |
| K2-5 | 2 | D-A5 dipatuhi; `argparse choices` menolak `hyd_ki`/`stuck_k1` | **TERBUKTI** |
| K2-6 | 2 | label VIB 32,17405 / SHKRSK 1 / SSI 1 (min 10 sampel) / onset H=10 + inblock dibuang | **TERBUKTI** |
| K2-7 | 2 | onset ffill cocok V8: 72/93/61; F-9 = 55 tanpa referensi | **TERBUKTI** (`v8_onsets_match` True/True/True/None) |
| K2-8 | 2 | 884 event: yes 50 / uncertain 571 / no 263 | **TERBUKTI** |
| K2-9 | 2 | `high_MSE > P75 = 256,600 psi` | **TERBUKTI** (P75 = 256.600,424; cross-tab label eksak) / **DIDUKUNG** (satuan psi) |
| K2-10 | 2 | hyd: qcut(TFLO,10) + median/MAD + \|z\|>2 + W=10 + ≥50% + 8 kanal | **TERBUKTI** |
| K2-11 | 2 | kontrak penuh (55, ketat-lalu, LOWO, seed 42, imputer fold-safe, tanpa grid, tau pra-reg, UP<30) | **TERBUKTI** |
| K2-12 | 2 | shk: 135 titik, 53 FAR≤60, 1 titik FAR≤6 & R>0 | **TERBUKTI** |
| K2-13 | 2 | 10 dari 402 titik uji FAR≤6 & R>0 | **TERBUKTI** |
| K2-14 | 2 | determinisme 2,22e-16, bukan bit-exact | **TERBUKTI** |
| K2-15 | 2 | median run 10 menit; y(t−1)=1 pada ±6/7 baris positif | **TERBUKTI** (median 10,0; 1.694/1.975 = 85,8%) |
| K2-16 | 2 | `ts_bin`/`lab_ts` KOSONG 118.567 baris (4/4 well) + leak-check vacuous | **KOREKSI** (0 kosong dengan 2 parser di 2 path; hash dataset tercatat ≠ file sekarang) |
| K2-17 | 2 | "0 pelanggaran di 6/6 dataset" (§1.2) tanpa syarat | **DIDUKUNG** (6 entri memang 0) + ketegangan internal dgn §7; pemeriksaan lebih tua dari file dataset |
| K2-18 | 2 | bab ML md = ipynb | **TERBUKTI** (0/371 baris hilang) |
| K2-19 | 2 | assert anti-sirkularitas di baris 192–193 | **TERBUKTI** |
| K2-20 | 2 | software sklearn 1.9.1 / numpy 2.5.3 / pandas 2.3.3 | **TERBUKTI** |

---

## 10. BELUM DIVERIFIKASI (verification-mandatory #3)

1. **Dataset Mendeley `th4yv974r2`** (tool_wear): sumber eksternal, tidak ada di disk lokal; klaim "label = identitas run" kandidat 2 tidak bisa dicek offline.
2. **File dataset `stuck_k2` semasa run** (`a8307db3…`): sudah tidak ada di disk, sehingga kebenaran historis klaim "kolom kosong" tidak dapat dipastikan (hanya klaim terhadap file sekarang yang terbantah).
3. **Angka pembanding V8** yang dikutip kandidat 2 (RF≥canary 5/5 ssi, persistence kalah 0/5, shk V8 6/9, lift V8 vib): dicek ke dokumen `V8_E_ssi_CAPABILITY.md` (5/5, 0/5) dan `V8_E_shk_CAPABILITY.md` (6/9), **bukan** ke JSON hasil V8; kecocokan tingkat JSON V8 tidak diuji di kartu ini.
4. **Angka 409/35 wellbore, 8.474.172 baris CSV, 17.368 berkas Databricks**: di luar bab ML, tidak diuji di kartu ini.
5. **`FAR_24` per titik tau yang tidak dikutip di dokumen**: hanya 10 titik dengan FAR≤6 & R>0 yang dihitung ulang; sisa 392 titik tidak dibedah satu per satu (agregat sudah dicek lewat 135 titik shk + 402 titik total).
6. **Re-run harness training**: tidak dijalankan ulang (butuh dataset D1 + waktu komputasi); verifikasi memakai JSON hasil + kode + pembacaan dataset, bukan training baru.
7. **Ketidakcocokan path `dataset` pada JSON** (`/mnt/d/Capstone 1/…`): dicatat sebagai fakta; alasan perpindahan path tidak diuji.
8. **Sel `.ipynb` kandidat 1 yang berisi kode VIS arsip**: hanya dicek sebagai teks penanda "ARSIP", eksekusi kode notebook tidak dijalankan.

---

## 11. ARTEFAK

- **Dokumen hasil:** `docs/V11_ML.md` (ini).
- **JSON primer:** `scratch/v11_e_ml/V11_ML_PRIMER.json` (manifest 25 berkas primer + hash, data 26 fold terurai + agregat + ΔB, persistence-onset, ledger 28 klaim).
- **Log verifikasi (output mentah 10 skrip):** `scratch/v11_e_ml/verify_out.txt`, `verify2_out.txt`, `verify3_out.txt`, `verify5_out.txt`, `verify6_out.txt`, `verify7_out.txt`, `verify8_out.txt`, `verify9_out.txt`, `verify10_out.txt`, `ipynb_out.txt`.
- **Skrip verifier (bisa dijalankan ulang):** `scratch/v11_e_ml/verify_ml_claims.py`, `verify2.py`, `verify3.py`, `verify5.py`, `verify6.py`, `verify7.py`, `verify8.py`, `verify9.py`, `verify10.py`, `check_ipynb.py`.
- **Salinan di ruang kerja kartu:** `/home/neonti/.hermes/kanban/boards/capstone-v11-vs/workspaces/t_29d17c33/` (skrip + log + `scratch/` salinan JSON primer).

*Selesai V11-E_ML (`t_29d17c33`): bab ML kedua kandidat diuji terhadap primer (labeling, kontrak, hasil fold, D-A5, persistence-onset, md=ipynb, kelengkapan) dengan 28 entri ledger dan skor rubrik 30/30/25/15. Satu klaim utama kandidat 2 (kolom waktu `stuck_k2` kosong) dinyatakan KOREKSI karena gagal direproduksi; empat klaim kandidat 1 dinyatakan KOREKSI/HIPOTESIS.*
