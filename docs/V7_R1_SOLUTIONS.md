# V7-R1 — SOLUSI AGAR >3 (IDELNYA 7) KELAS DYSFUNGSI LOLOS GATE ML

Task: `t_d2cab982` [R&D] · Board: capstone-v7-solve · Tanggal: 2026-10-11 (WIB)
Status: DIAGNOSIS per kelas gagal + ≥2 solusi per kelas, semua dengan rumus/metode, data needed (dengan path), dan peluang vs beban. **Gate G1/G2 pra-reg V6 TIDAK digeser** (§8).

> **Riset pendahuluan: `literature-review`** — pencarian multi-query via `web_search` (6 query utama + 2 tambahan, 2026-10-11): survival/PdM, weak supervision, stuck-pipe early warning, tool wear monitoring, hydraulic/pump anomaly, rare-event learning, change-point/onset labeling; sintesis dikelompokkan per kelas gagal.
> **Riset pendahuluan: `paper-lookup`** — 8 DOI kandidat diverifikasi langsung lewat `api.crossref.org/works/{DOI}` (semua OK, judul cocok) + 4 query Crossref bibliograf; 12 sitasi lama dipakai ulang dari V6-R1 run-3 yang sudah 17/17 lolos Crossref.
> **Riset pendahuluan: `hypothesis-generation`** — tiap kegagalan diperlakukan sebagai hipotesis multi-kausal (label salah / unit salah / data kurang / sinyal memang tidak ada); tiap solusi punya tes pembeda yang disebut.
> **Riset pendahuluan: `scientific-critical-thinking`** — klaim "F-1 C/F-11 punya kanal dysfungsi" (hipotesis terbuka D0 §2.4) DIUJI dan DITEPIS dengan scan header 3.906 file; temuan baru (peta kanal seluruh wellbore) dilaporkan apa adanya, termasuk yang merugikan solusi yang diusulkan.
> **Riset pendahuluan: `grounded-citations`** — ledger `scratch/v7_r1_ledger.json` (22 entri); setiap solusi ilmiah bernomor `[n]` yang terkontrol ledger, bukan diketik dari ingatan.

---

## 0. RINGKASAN EKSEKUTIF

**Temuan sentral (bukti scan baru, §1):** hipotesis V6 bahwa "F-1 C + F-11 (54,6% file log) akan menambah label dysfungsi" **SALAH** — kedua wellbore terbesar itu **nol kanal `SHKRSK_RT`/`STUCK_RT`/`VIBLAT_RT`/`CRPM_RT`** (scan 3.906 file). TAPI scan seluruh 23 direktori wellbore menemukan **4 wellbore yang belum diparse dan KAYA kanal dysfungsi**: **F-10** (`SHKRSK_RT` 188 file, `CRPM_RT` 186, `STKSLP` 125, `VIBLAT_RT` 66, `STUCK_RT` 18), **F-4** (`SHKRSK_RT` 135, `STICK_RT` 135, `CRPM_RT` 135, `VIBLAT_RT` 86), **F-12** (`SHKRSK_RT` 91, `CRPM_RT` 90, `STICK_RT` 52, `STUCK_RT` 6), **F-15**StatoilHydro (`SHKRSK_RT` 77, `STICK_RT` 76, `VIBLAT_RT` 76, `CRPM_RT` 76). Ini, bukan F-1 C/F-11, adalah tambahan positif nyata untuk `shk`, `ssi`, `vib`, `stuck`.

**Diagnosis ringkas per kelas gagal (mechanik, angka di §2–§5):**

| Kelas | Akar kegagalan mekanis (1 kalimat) | Kelas solusi utama |
|---|---|---|
| `stuck` | Label = STATUS instrumen membentuk blok panjang (F-9_A prev 66,9%) → persistence (0,787) mengalahkan RF (0,651); hanya 2 sumur eligible → mayoritas 1/2 | onset-vs-status + sumur baru (F-10/F-12) |
| `shk` | BUKAN fitur buruk (G2 6/7 lolos) — jumlah POSITIF terlalu kecil (30–45 jendela di fold kecil) → lift tidak mayoritas | unit window + parse F-10/F-4/F-12/F-15 |
| `hyd` | Label = ambang residual SPPA≈status proses yang sangat persisten; kanal lain tidak membawa sinyal lintas-channe → lift ~1 di 7 fold | onset reframing + label alternatif (pit/flow-mismatch) |
| `tool_wear` | n=4 alat; label = identitas run (R01 vs R02) tercampur urutan percobaan; prev ~0.5 membatasi lift maksimum = 2,0 | label progresi/awal-keausan + fitur VMD |

**Jalur realistis ke ≥5 kelas LULUS** (diurut peluang vs beban, detail §7): `vib` + `ssi` (sudah) + **`stuck`-onset** + **`shk` (unit/sumur baru)** + **`bit_wear`-onset** (upgrade dari bersyarat) = **5**. Upside: `hyd` (onset + label baru) dan `tool_wear` (progresi) → potensi 7.

---

## 1. BUKTI BARU: PETA KANAL DYSFUNGSI SELURUH WELLBORE (scan mandiri, 2026-10-11)

Skrip: `~/.hermes/cache/scratch/v7_r1_f1c_f11_scan.py`, `v7_r1_f1c_f11_mnemonics.py`, `v7_r1_allwb_scan.py`; hasil mentah: `scratch/v7_r1_f1c_f11_channels.json`, `v7_r1_f1c_f11_mnemonics.json`, `v7_r1_allwb_channels.json` (di repo Capstone). Metode: baca header (`<mnemonic>`) 300–400 KB pertama setiap file log XML — `logCurveInfo` selalu di depan `<logData>` pada dataset ini (verifikasi pada sampel). **Batas metode (jujur):** jika sebuah file hanya berisi potongan data tanpa deklarasi kurva, kanalnya tidak terhitung — angka = jumlah file yang MENDAFTARKAN mnemonic, bukan jumlah baris data.

### 1.1 F-1 C dan F-11 (hipotesis terbuka D0 §2.4 — DITEPIS)

- F-1 C: 2.156 file log; **0 file** berisi `SHKRSK_RT`, `STUCK_RT`, `VIBLAT_RT`, `CRPM_RT`, `STICK_RT`, `STKSLP`, `WHIRL_RT`, `BOUNCE_RT`, `SPPA`, `TFLO`, `TQA`, `SWOB`. Mnemonik yang ada = konvensi lama: `SURF_RPM` (621), `TORQUE_AVG/MAX/MIN` (599/529/528), `WOB_AVG` (599), `HKLD_AVG` (596), `ROP_AVG` (623), `FLOWIN` (990), `FLOWOUT` (688), `FLOWOUTPC` (949), `PUMP`/`STROKESUM` (952/801), `MSE`/`I_MSE` (513/511), **`LINEWEAR` (506)**, `GAINLOSSTOT` (575), `PITTOT` (565), `RIGHEAVE` (781), `BLOCKCOMP` (1.183), `MOTOR_RPM` (537), `BIT_RPM_*` (531).
- F-11: pola identik (1.750 file log; `FLOWIN` 737, `LINEWEAR` 455, `MSE` 466, `GAINLOSSTOT` 517; 0 kanal dysfungsi).
- **Konsekuensi:** parse F-1 C/F-11 **tidak** menambah positif `stuck`/`shk`/`vib`/`ssi`. Yang dibukanya: fitur surface kaya (termasuk `LINEWEAR` = keausan drilling line terukur, `GAINLOSSTOT`/`PITTOT` = indikator kick/lost circulation, `TOTGAS`) — bahan fitur & label ALTERNATIF, bukan ekspansi label lama.

### 1.2 WELLBORE BELUM DIPARSE YANG KAYA KANAL DYSFUNGSI (temuan terbesar)

| Direktori wellbore (witsml_raw) | File log | SHKRSK_RT | CRPM_RT | STICK_RT | VIBLAT_RT | STUCK_RT | STKSLP | Status parse |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Norway-StatoilHydro 15/9-F-10 | 271 | **188** | **186** | 0 | **66** | **18** | **125** | BELUM diparse |
| Norway-StatoilHydro 15/9-F-4 | 229 | **135** | **135** | **135** | **86** | 0 | 0 | BELUM diparse |
| Norway-Statoil 15/9-F-12 | 233 | **91** | **90** | **52** | 0 | **6** | 0 | BELUM diparse |
| Norway-StatoilHydro 15/9-F-15 | 92 | **77** | **76** | **76** | **76** | 0 | 37 | BELUM diparse |
| Norway-StatoilHydro 15/9-F-15B | 16 | 10 | 11 | 10 | 10 | 1 | 10 | BELUM diparse (kecil) |
| Norway-NA 15/9-F-9 A | 46 | 24 | 7 | 0 | 0 | 24 | 0 | sudah CSV (`data/witsml/Norway-NA-15_47_9-F-9 A time.csv`, 419.747 baris) |

(Catatan: F-14/F-5/F-7/F-9/F-15A/F-15S StatoilHydro juga tercatat punya kanal — sebagian sudah terpakai lewat CSV parser lama; `Norway-Statoil-NO 15/9-F-15` (1.100 file) hanya berisi `MSE`/`LINEWEAR` surface-konvensi-lama, TIDAK berikan label dysfungsi.)

**Implikasi langsung ke 4 kelas:**
- `shk`: +4 sumber positif (F-10/F-4/F-12/F-15) → fold besar baru, menyerang akar "prevalensi/positif terlalu sedikit".
- `ssi`: `CRPM_RT` (+`STKSLP`, `STICK_RT`) di 4 wellbore baru → fold UNDERPOWERED (F-7 3 pos, F-9 12 pos) bisa diganti fold berkekuatan penuh.
- `stuck`: `STUCK_RT` F-10 (18 file) + F-12 (6 file) → 2 sumur eligible tambahan (dari 2 menjadi 4).
- `vib`: `VIBLAT_RT` F-4/F-10/F-15 → memperkuat 4 fold yang sudah LULUS (anti-rapuh).

---

## 2. KELAS `stuck` — DIAGNOSIS + SOLUSI

### 2.1 Diagnosis mekanis (angka dari `docs/V6_E1_ML_DESIGN.md` §4.4)

Fakta: G1 1/2 fold, G2 1/2. F-14: AUPRC RF 0,421, lift 3,12 (canary 0,410 — nyaris seri). F-9_A: AUPRC 0,651, **lift 0,97**, canary 0,769 > RF, **persistence 0,787 > RF 0,651**. Prev F-9_A 66,9%.
Akar kegagalan (3 lapis, bukan satu):
1. **Label = STATUS, bukan peristiwa.** `STUCK_RT ≥1` bertahan puluhan/menit-jam membentuk blok (prev 66,9% di F-9_A) → "jendela sebelumnya positif" adalah prediktor yang hampir sempurna. Model apa pun yang memprediksi STATUS kalah telak dari persistence. Ini bukan kegagalan fitur — ini kegagalan FORMULASI TUGAS terhadap tuntutan dosen ("alat X mungkin akan SEGERA RUSAK" = peristiwa onset, bukan status).
2. **Jumlah fold = 2** (hanya F-14 & F-9_A eligible; F-9: 1.159 label valid tapi 0 jendela fitur pengeboran; 5 sumur lain tidak punya kanal). "Mayoritas" = keputusan 1 suara.
3. **Semantik `STUCK_RT` 0/1/2/3 tidak terdokumentasi** (pra-reg E1 §7.5) — label = flag instrumen, bukan kejadian stuck terverifikasi naratif.

### 2.2 SOLUSI S-A1 (ilmiah + cara kerja): label ONSET peristiwa, bukan status — REKOMENDASI #1

- **Rumus/metode:** dari deret `STUCK_RT` per sumur, definisikan onset `t_e` = titik naik `0→1` (edge deteksi). Jendela POSITIF = jendela fitur `[t0−10,t0)` yang `t0 ∈ [t_e−H, t_e]` (prediksi dalam horizon H menit SEBELUM onset); jendela di dalam blok setelah onset **dibuang dari evaluasi** (bukan dinegatifkan — menghindari anotasi semu). Persistence baseline pada label onset otomatis jauh lebih lemah (onset tidak persisten secara definisi). Horizon H = 10 menit (setara window V6) dengan sensitivitas H ∈ {5, 30}.
- **Preseden ilmiah:** pendekatan "early sign sebelum stuck" terbukti di Volve dengan data surface yang sama: Crossformer memberi peringatan 2,67–7,37 menit sebelum stuck[11]; autoencoder (latih hanya data normal) mencapai AUC 0,958 di Volve[12]. Jalur tanpa-label yang sama juga dibuktikan LSTM-AE[13] dan 3D CNN depth-domain pada data pengeboran nyata[14]. Framing "event-vs-state" untuk time-series imbang didukung tinjauan rare-event[7] dan pendekatan deteksi event via regresi[10].
- **DATA NEEDED:** `data/volve/witsml_parsed/F-14.csv` + `F-9_A.csv` (LANGSUNG, sudah ada) + hasil parse F-10/F-12 (lihat S-A2, perlu diolah).
- **Peluang vs beban:** peluang TINGGI (menghilangkan persistence dominance secara konstruksi; target = persis tuntutan dosen); beban RENDAH (relabel dari CSV yang sudah ada, nol parse baru). **Tes pembeda:** jika persistence pada label onset tetap ≥ RF di mayoritas fold, hipotesis "kegagalan = formulasi status" DITOLAK dan penyebabnya berpindah ke "sinyal fitur memang lemah untuk stuck-onset".

### 2.3 SOLUSI S-A2 (merekayasa data): parse 2 sumur eligible baru — F-10 & F-12

- **Metode:** parse WITSML F-10 (18 file `STUCK_RT`) & F-12 (6 file) ke CSV mengikuti parser V6 (grid 60 detik, agregat menit, syarat kelayakan jendela identik E1 §5), gabungkan ke kampanye LOWO stuck. Fold eligible naik 2 → 4; "mayoritas" kehilangan sifat 1-suara; prev F-10/F-12 kemungkinan jauh di bawah 66,9% (perlu dihitung, bukan diasumsikan).
- **DATA NEEDED:** `data/volve/witsml_raw/Norway-StatoilHydro-15_$47$_9-F-10/1/log/**` dan `Norway-Statoil-15_$47$_9-F-12/1/log/**` (ADA, perlu diolah jadi CSV; jumlah file kecil → beban parse ringan-menengah, jauh lebih kecil dari F-1 C).
- **Peluang vs beban:** peluang SEDANG-TINGGI (menambah fold; kalau prev rendah, lift langsung berpeluang >1,5 mengingat sinyal surface→stuck AUC 0,96–0,98 sudah terbukti di F-14); beban SEDANG.

### 2.4 SOLUSI S-A3 (cara kerja): weak supervision multi-sumber (label-model Snorkel)

- **Metode:** labeling functions (LF) independen: LF1 = `STUCK_RT≥1`; LF2 = event kurasi DDR (`data/volve/labels_curated_v2.csv`, 1.412 baris event — CATATAN: V6_R1 menyebut 884 event; selisih wajib direkonsiliasi sebelum dipakai); LF3 = fisika differential sticking `F = μ·A_contact·ΔP` (overbalance + HKLD/pressure proxy — dipakai sebagai penanda risiko, parameter kontak tidak tersedia sehingga LF3 hanya penanda relatif); LF4 = anomali overpull/torsi (deret HKLD/TQA melonjak saat operating-state sama). Label model generatif memperkirakan akurasi & korelasi antar-LF lalu menghasilkan label probabilistik — Ratner dkk.[5][6].
- **DATA NEEDED:** semua LANGSUNG/terparse (WITSML 7 sumur + labels_curated_v2.csv + USROP).
- **Peluang vs beban:** peluang SEDANG (menaikkan jumlah & kualitas positif, tahan terhadap noise satu sumber); beban SEDANG (implementasi label model, dijaga anti-sirkular: LF tidak boleh memakai kanal yang jadi fitur). Ini solusi KETUKUAN, bukan syarat lolos — dipasang setelah S-A1/S-A2.

---

## 3. KELAS `shk` — DIAGNOSIS + SOLUSI

### 3.1 Diagnosis mekanis

Fakta: G1 3/7 (lift per fold 1,35 / 1,24 / 1,26 / **3,36** / 0,94 / **9,79** / **2,31**), G2 **6/7 lolos**. Prev 0,6–2,4% di 4 fold; positif per fold: F-14 760, F-15_S 259, F-5 240, F-7 267, tapi F-15A 41, F-9 45, F-9_A 30.
Akar kegagalan:
1. **G2 lolos 6/7 = fitur BUKAN masalah utama**; yang gagal hanya G1 di fold-langka. Dengan 30–41 positif, AUPRC punya varians raksasa; satu fold dengan sedikit deteksi menjatuhkan "mayoritas". Ini masalah **jumlah informasi positif per fold**, kelas kegagalan "rare-event learning" yang terdokumentasi[7] (AUPRC sangat sensitif prevalensi kecil; ROC-AUC tinggi menyembunyikan deteksi lemah).
2. Bukan salah ambang: `SHKRSK_RT ≥1` ambang minimal sudah (0–3 skala); menurunkan ambang = menambah positif tapi juga menurunkan makna fisik — TIDAK disarankan (dan bisa dituduh menggeser definisi kelas).
3. F-1 C/F-11 TIDAK punya `SHKRSK_RT` (§1.1) — jalur ekspansi yang selama ini diaspirasikan tidak ada; tapi §1.2 menemukan 4 wellbore kaya `SHKRSK_RT`. Saini dkk. 2020 membuktikan ≥10 kelas dysfungsi bisa diklasifikasi dari sensor surface[16] — kelas shk bukan mustahil, hanya butuh sampel memadai.

### 3.2 SOLUSI S-B1 (merekayasa data): parse F-10, F-4, F-12, F-15 — REKOMENDASI #2

- **Metode:** parse 4 wellbore (file `SHKRSK_RT`: 188/135/91/77) ke CSV dengan protokol identik E1; masuk LOWO `shk`. Fold eligible naik 7 → ~11; fold besar baru menggeser G1 ke mayoritas secara jujur (angka baru = angka nyata, bukan simulasi). Estimasi kasar positif: bahkan bila prev hanya 2% per well, fold ~5–10 ribu jendela → ~100–200 positif/well (DIHITUNG saat eksekusi, bukan klaim).
- **DATA NEEDED:** `data/volve/witsml_raw/Norway-StatoilHydro-15_$47$_9-F-10/`, `…-F-4/`, `Norway-Statoil-15_$47$_9-F-12/`, `Norway-StatoilHydro-15_$47$_9-F-15/` (ADA semua, perlu diolah; total ~825 file log — beban parse menengah).
- **Peluang vs beban:** peluang TINGGI (menyerang akar penyebab persis: jumlah positif; G2 sudah lolos → sinyal ada); beban SEDANG (4 parse). **Tes pembeda:** kalau setelah parse G1 tetap <mayoritas, berarti lift memang tidak stabil lintas wellbore → jalur S-B2 (unit stand).

### 3.3 SOLUSI S-B2 (merekayasa data): ganti unit jendela 10-menit → PER-STAND

- **Metode:** agregasi label & fitur per stand pengeboran (per trip/stand, unit operasional rig): label stand = `any(SHKRSK_RT≥1)` selama stand; fitur = statistik stand sebelumnya. Prevalensi naik ke kisaran 10–40% (dihitung saat eksekusi) → canary naik TAPI varians AUPRC turun drastis dan fold kecil berhenti menjadi UNDERPOWERED; gate G1/G2 diterapkan identik pada unit baru. Ini eksplisit salah satu arah yang diminta operator ("ganti unit window→stand/interval").
- **DATA NEEDED:** `data/volve/witsml_parsed/*.csv` + boundary stand — bisa diturunkan dari `BPOS`/gaps waktu (perlu diolah, engineering judgment).
- **Peluang vs beban:** peluang SEDANG (varians turun; tapi fisika "stuck/shk akan segera terjadi" jadi kurang tajam di unit stand — horizon prediksi melebar); beban RENDAH-SEDANG. Konsekuensi jujur: unit stand = deteksi "stand berikutnya berisiko", bukan "10 menit lagi".

### 3.4 SOLUSI S-B3 (cara kerja): ordinal/regresi ke level shock (0–3), evaluasi AUPRC pada onset-klasifikasi hasil binarisasi fisik

- **Metode:** daripada hanya `≥1`, latih model memprediksi SKALA shock (0–3, `SHKRSK_RT` ordinal; loss ordinal/regresi), lalu turunkan keputusan biner pada ambang yang sama (`≥1`) dari skor terprediksi — sering menstabilkan fold langka karena seluruh informasi kanal dipakai[15] (Liu 2025 memakai data surface + forensik untuk klasifikasi dysfungsi). Gate tetap dihitung pada AUPRC biner hasil ambang `≥1` — tidak digeser.
- **DATA NEEDED:** LANGSUNG (kanal sudah di CSV 7 sumur; makin kuat bila digabung S-B1).
- **Peluang vs beban:** peluang SEDANG-RENDAH sebagai solusi tunggal (jumlah positif tidak bertambah); beban RENDAH. Posisi: pelengkap S-B1.

---

## 4. KELAS `hyd` — DIAGNOSIS + SOLUSI

### 4.1 Diagnosis mekanis

Fakta: G1 2/7 (lift 1,40/1,00/1,02/2,03/0,80/2,35/1,07), G2 4/7; **persistence 0,42–0,63 >> RF 0,11–0,61 di 7/7 fold**. Label = `|z|>2` residual SPPA terhadap median/MAD per bin `qcut(TFLO,10)` (R1 §4.2 #7), prev 8,3–26,2%.
Akar kegagalan:
1. **Label adalah status ambang dari proses yang sangat persisten** (tekanan/pompa berubah lambat) → persistence menang telak; ini analog persis kasus `bit_wear`.
2. **Sinyal lintas-kanal lemah**: ketika SPPA/TFLO/SPM dikeluarkan dari fitur (anti-sirkular, E1b), kanal sisa (RPM/WOB/HKLD/ROP dll.) tampaknya tidak memprediksi anomali tekanan dengan lift >1,5 — konsisten dengan temuan V6-R1 §3.3: banyak dysfungsi downhole teredam dan tidak terbaca dari parameter lain[18][19]. Ini hipotesis yang DUKUNGANNYA ada tapi belum final: kemungkinan tersisa label onset memang lebih bisa diprediksi (kanal proses bergerak SEBELUM tekanan melonjak).
3. F-1 C/F-11 punya `GAINLOSSTOT` (575/517 file) dan `PITTOT` (565/506) — data untuk label ALTERNATIF fisik (kick/lost circulation/pump problem), bukan label residual SPPA (§1.1).

### 4.2 SOLUSI S-C1 (cara kerja + ilmiah): reframing ONSET — prediksi awal-masuk-anomali, bukan status anomali — REKOMENDASI #4

- **Rumus/metode:** label onset = jendela `[t0−H, t0)` di mana blok anomali (status `|z|>2` berkelanjutan ≥k menit) dimulai pada `t0`; jendela di dalam blok dibuang. Persistence pada label onset otomatis jatuh ke kisaran rendah (onset tidak berulang di jendela berikutnya); G1 dihitung ulang identik. Framing ini sejalan tinjauan rare-event[7] dan pendekatan deteksi-event[10]; preseden pemakaian prediksi SPP dari parameter operasional untuk mendeteksi anomali pompa/washout (bukan untuk mengganti label) = Husseiny dkk.[2] — paper itu memprediksi SPP dari RPM/flow/depth lalu memakai residunya untuk diagnosis; di kampanye kita, prediktor SPP (model terlatih di fold latih) boleh dipakai sebagai SISTEM PERINGATAN-DINI fitur, dengan label tetap kanal sumber berbeda (jaga anti-sirkular).
- **DATA NEEDED:** `data/volve/witsml_parsed/*.csv` (LANGSUNG; label bisa dihitung ulang dari kolom SPPA/TFLO yang sudah ada).
- **Peluang vs beban:** peluang SEDANG (menghapus dominasi persistence TAPI tidak menjamin lift — kalau memang tak ada sinyal precursor, G1 tetap gagal; ini risiko jujur); beban RENDAH (relabel + run ulang). **Tes pembeda krusial:** onset-`hyd` dengan fitur 8 kanal — kalau lift mayoritas → kelas LULUS; kalau tidak → "hyd tidak bisa diprediksi dari kanal lain" berstatus TERDUKUNG KUAT, dan jalurnya pindah ke S-C2 (label berbeda).

### 4.3 SOLUSI S-C2 (ilmiah + merekayasa data): ganti SUMBER LABEL ke fisika well-control — pit gain / flow mismatch

- **Rumus/metode:** dua label turunan fisik, keduanya onset-based:
  (a) **Kick/loss:** `ΔV_pit = PITTOT(t) − PITTOT(t−τ)` atau kumulatif `GAINLOSSTOT` — lonjakan/penurunan laju pit di luar baseline operasi = awal kejadian; ambang z-score per sumur (median+MAD), seperti metode residual R1 tapi pada KANAL SUMBER yang berbeda dari fitur.
  (b) **Washout/clog nozzle:** `Q_out − Q_in` (`FLOWOUT`−`FLOWIN`, kanal FLOWOUTPC = % return) menyimpang terus-menerus, disertai tren SPPA turun pada flow tetap — aturan klasik deteksi washout; prediksi SPP dari parameter operasional[2] menyediakan baseline model-nya.
  Fitur memakai kanal pengeboran yang BUKAN kanal sumber label (RPM/WOB/TQA/HKLD/ROP/dst) — anti-sirkular seperti E1b.
- **DATA NEEDED:** untuk jalur cepat: kanal `PIT*`/`GAINLOSSTOT`/`FLOWOUT*` MENTAH di F-9 (`data/volve/witsml_raw/…-F-9/…`, D1e: PIT1..PIT30 & GAINLOSSTOT ada di raw tapi tidak masuk CSV lama) — perlu parse tambahan kecil; jalur penuh: parse F-1 C/F-11 (`GAINLOSSTOT` 575/517 file, `PITTOT`, `FLOWOUT`/`FLOWOUTPC`) — BEBAN BESAR tapi membuka label di 2 wellbore terbesar + fitur kaya (§1.1). Semua path ADA di disk.
- **Peluang vs beban:** peluang SEDANG (label baru dengan fisika berbeda; prevalensi & persistensi tidak diketahui sebelum dihitung — jangan dijanjikan); beban SEDANG (parse F-9 raw) sampai BESAR (F-1 C/F-11). Diprioritaskan hanya setelah S-C1 diuji.

### 4.4 SOLUSI S-C3 (cara kerja): survival/hazard time-to-hydraulic-event

- **Metode:** model hazard proporsional/deep survival untuk waktu-sampai-peristiwa hidrolik (onset S-C1 atau label S-C2): `h(t|x) = h0(t)·exp(βᵀx)`; jendela uji diberi skor risiko per horizon → gate G1/G2 dihitung dari skor risiko horizon-H (klasifikasi biner "peristiwa dalam H") sehingga gate tidak berubah. Preseden tinjauan survival untuk predictive-maintenance[1][4].
- **DATA NEEDED:** LANGSUNG (derivasi dari label onset S-C1/S-C2).
- **Peluang vs beban:** peluang SEDANG-RENDAH untuk menaikkan lift (survival mengubah FORMULASI, bukan menambah informasi); beban SEDANG. Posisi: opsi pembanding, bukan primer.

---

## 5. KELAS `tool_wear` — DIAGNOSIS + SOLUSI

### 5.1 Diagnosis mekanis

Fakta: G1 0/4 (LOTO lift 1,09 / 1,39 / 1,42 / 1,30; AUPRC 0,54–0,77), G2 4/4. Hanya 4 alat (T01–T04), 2 run masing-masing (R01 baru / R02 tumpul), 469 jendela; SHAP fold T03 didominasi `Z_kurt`, `X_fdom`, `Z_kurt`… (fitur spektral — G2 lolos berarti sinyal keausan ADA).
Akar kegagalan:
1. **n cluster = 4** → LOTO hanya 4 fold; dengan 4 sampel cluster, "mayoritas" = 3/4 dan varians antar-alat besar; generalisasi antar-alat memang adalah pertanyaan tersulit di kondisi monitoring[8].
2. **Label = identitas run (R01 vs R02)** — tercampur urutan percobaan: R02 selalu sesudah R01 → perbedaan termal/dinamika spindle ikut terkorelasi dengan label (confound), melemahkan transfer ke alat baru.
3. **Prevalensi ~0,5 membatasi plafon lift = 1/prev = 2,0** — butuh AUPRC ≥0,75 untuk lolos G1; angka nyata 0,54–0,77 = di sekitar ambang, tidak heran 0/4 lolos[9] (AUPRC sangat bergantung pada prevalensi & jumlah positif).
4. TIDAK ADA dataset tool-wear drilling REAL tambahan yang bisa diunduh (D2 Q1–Q18 diverifikasi negatif: Mendeley `th4yv974r2` = 4 alat; XAI Kaggle & synthetic HF = SINTETIS, melanggar mandat "data nyata"; path bukti: `~/.hermes/cache/scratch/v6d2/`, `docs/V6_D2_EXTERNAL_DATASETS.md` §1/§3). **Jadi "tambah alat" bukan opsi yang tersedia dari data publik — solusi harus memperkaya informasi dari 4 alat yang ada.**

### 5.2 SOLUSI S-D1 (ilmiah + cara kerja): label PROGRESI KEAUSAN dalam-run (onset-of-accelerated-wear), bukan identitas run — REKOMENDASI #5

- **Rumus/metode:** (1) hitung deret fitur keausan per sampel/jendela pendek dari akselerometer mentah (kurtosis, crest, frekuensi dominan — sudah terbukti di SHAP E1c); (2) deteksi titik ubah (change-point) pada deret itu per run → onset keausan terakselerasi `t_cp`; (3) label = jendela SEBELUM `t_cp` dalam horizon H (prediksi "alat akan segera aus parah") — sejalan permintaan dosen ("SEGERA RUSAK") dan preseden RUL/degradation modeling[1][3] serta monitoring keausan dari sinyal tidak langsung[8]. Dengan banyak run (8 run) dan banyak titik ubah per run, jumlah cluster efektif naik dari 2 kelas×4 alat menjadi banyak ONSET per alat; LOTO tetap (uji = 1 alat tak terlihat).
- **DATA NEEDED:** 8 xlsx akselerometer 1000 Hz — `scratch/v6_e1/toolwear/DrillingToolWearDataset_T0{1..4}_R0{1,2}.xlsx` (ADA, terverifikasi SHA-256 vs API Mendeley di E1c; 8 file).
- **Peluang vs beban:** peluang SEDANG (mengalahkan dua cacat sekaligus: confound urutan-run dan plafon lift via label langka-baru yang lebih fisik); beban SEDANG (perlu validasi change-point: kalau `t_cp` selalu di detik awal = artifact termal, solusi gugur — tes pembeda eksplisit).

### 5.3 SOLUSI S-D2 (ilmiah): fitur keausan berbasis VMD + jaringan saraf — menaikkan AUPRC per fold

- **Rumus/metode:** dekomposisi Variational Mode Decomposition sinyal akselerometer → band energy & statistik per mode → klasik BP-NN/SVM; preseden: Wang dkk. 2024 (VMD + BP untuk prediksi keausan alat, Sensors)[3]; pemakaian audio/vibration domain features untuk keausan dengan akurasi >90%[8]. Formula ringkas: `x(t) → VMD → {u_k(t)} → f_k = [std(u_k), kurt(u_k), E_k/ΣE] → clf`.
- **DATA NEEDED:** LANGSUNG (8 xlsx).
- **Peluang vs beban:** peluang SEDANG (G2 sudah lolos → fitur lebih tajam menaikkan AUPRC; tapi plafon lift prev~0,5 tetap 2,0 → S-D2 saja TIDAK cukup, harus digabung S-D1 atau S-D4); beban RENDAH-SEDANG (pustaka VMD: `vmdpy`, CPU cukup).

### 5.4 SOLUSI S-D3 (ilmiah + cara kerja): label keausan turunan MSE/DS pada data Volve (kelas keausan domain sumur)

- **Rumus/metode:** aturan Menand & Mills[21]: `MSE naik + MSE/DS turun = bit wear/balling` (`DS = WOB/(R·DOC)`, `DOC = ROP/(60·RPM)`; rumus terverifikasi R1 run-3 §10.3); populasi sudah terhitung (USROP: inefisiensi parah 78.212 baris; rasio per-sumur z-score). Kelas `bit_wear` versi "keausan terkonfirmasi silang" memakai 2 indikator fisik berbeda → label lebih bersih dari blok MSE murni. (Terhubung ke §6: juga membantu `bit_wear`.)
- **DATA NEEDED:** `data/USROP_labeled.csv` (LANGSUNG, 198.928 baris; kolom WOB/ROP/RPM/MSE sudah ada).
- **Peluang vs beban:** peluang SEDANG sebagai PENGUAT label (mengurangi noise blok); beban RENDAH. Bukan solusi tunggal untuk LOTO `tool_wear` (domain berbeda: sumur vs bengkel) — dipakai untuk memperkaya kampanye `bit_wear`, bukan menggantikan S-D1.

### 5.5 SOLUSI S-D4 (cara kerja): learning-to-rank / few-shot pairwise antar status dalam alat

- **Metode:** ubah klasifikasi biner menjadi ranking pasangan dalam-alat ("jendela A lebih aus dari B" dari fitur vibrasi), generalisasi diuji LOTO; metrik ranking dikonversi ke gate biner pada ambang fisik (top-quantile wear = positif). Engineering judgment (belum ada paper drilling khusus; preseden umum ranking/few-shot di predictive maintenance[1]).
- **DATA NEEDED:** LANGSUNG (8 xlsx).
- **Peluang vs beban:** peluang RENDAH-SEDANG (elegan tapi mengubah estimand; gate biner tetap dipakai tapi ambang fisiknya adalah keputusan desain baru → wajib pra-registrasi baru); beban SEDANG. Posisi: cadangan bila S-D1 gagal di change-point validation.

---

## 6. KELAS RAPUH: `ssi` (LULUS tapi CI95 bawah 2/5 fold) & `bit_wear` (LAYAK BERSYARAT)

### 6.1 `ssi` — diagnosis + 2 solusi

Diagnosis: LULUS (G1 4/5, G2 5/5; persistence 0/5 — model TIDAK dikalahkan status-quo), TAPI: fold F-7 (3 positif) & F-9 (12 positif) UNDERPOWERED; F-9_A lift 1,47 (gagal tipis); CI95 lebar di 2 fold. Akar = jumlah positif & fold kecil, sama seperti `shk`. (Label SSI memakai grading Liu 2025[17]; klasifikasi severitas stick-slip dengan ML sudah mapan[22].)
- **S-E1 (data): parse F-10/F-4/F-12/F-15** (`CRPM_RT` 186/135/90/76 file; §1.2) → fold UNDERPOWERED tergantikan fold kuat; severe stick-slip lintas-sumur (R1 §8.2: F-5 40/120 window, F-15_S 23/67) ikut menguat. DATA: raw XML ADA, perlu diolah. Peluang TINGGI (hanya menambah sampel; mekanisme label tidak berubah); beban SEDANG (terbagi dengan S-B1 — satu parse melayani `shk`+`ssi`+`vib`+`stuck`).
- **S-E2 (cara kerja): deep-ensemble/CI lebih ketat bukan solusi — YANG BENAR: prereg-ulang dengan stabilitas fold** (stratified bootstrap per fold, laporkan jumlah positif) — engineering judgment; peluang RENDAH sebagai "penambah kelas" (ssi sudah LULUS); posisi: pengeras bukan kelas tambahan.

### 6.2 `bit_wear` — diagnosis + 2 solusi (target: naik dari BERSYARAT ke LULUS penuh)

Diagnosis: G1 3/4 (F-15S lift 1,495 gagal tipis), G2 4/4, TAPI persistence > RF di **4/4 fold** → aturan pra-reg E1a §6 menurunkan verdict. SHAP F-15 didominasi `MD_last/mean`, `TVD_mean/last` → model "mengingat posisi kedalaman"; label high-MSE membentuk blok lintas kedalaman.
- **S-F1 (cara kerja, REKOMENDASI #3): onset-of-high-MSE** — label = prediksi MASUKNYA blok high-MSE (rumus Teale[20], kolom `label` USROP terverifikasi R1 run-3), jendela dalam blok dibuang; persistence jatuh secara konstruksi; kanal pembentuk MSE tetap dilarang dari fitur (E1d). Horison = 1 jendela (10 menit) + sensitivitas 30 menit. DATA: `data/USROP_labeled.csv` LANGSUNG. Peluang TINGGI (mekaniknya identik dengan S-A1; G1 sudah 3/4 — sekadar menghapus hukuman persistence); beban RENDAH (relabel ulang, run kampanye baru ber-pra-reg). **Ini +1 kelas LULUS paling murah kedua setelah S-A1.**
- **S-F2 (ilmiah): label silang MSE/DS (Menand & Mills[21], S-D3)** — high-MSE hanya "keausan" bila disertai MSE/DS turun; memotong label blok yang sebenarnya vibrasi/balling. DATA: LANGSUNG (USROP). Peluang SEDANG; beban RENDAH. Digabung dengan S-F1.

---

## 7. PERINGKAT SOLUSI (peluang sukses vs beban kerja) + JALUR KE ≥5

Urutan eksekusi yang disarankan (semua memakai gate G1/G2 YANG SAMA):

| # | Solusi | Kelas dituju | Peluang | Beban | Alasan |
|---|---|---|---|---|---|
| 1 | S-A1 stuck onset | `stuck` LULUS | TINGGI | RENDAH (nol parse) | persistence dibunuh secara konstruksi; preseden Volve[11][12][13][14] |
| 2 | S-F1 (+S-F2) bit_wear onset (+MSE/DS) | `bit_wear` BERSYARAT→LULUS | TINGGI | RENDAH | G1 sudah 3/4; hanya hukuman persistence yang dilepas |
| 3 | S-B1 parse F-10/F-4/F-12/F-15 | `shk` LULUS (+`ssi`/`vib` keras, +`stuck` via S-A2) | TINGGI | SEDANG | menyerang akar "positif terlalu sedikit"; G2 sudah 6/7 |
| 4 | S-C1 hyd onset | `hyd` LULUS? | SEDANG | RENDAH | perlu tes pembeda; kalau gagal → sinyal lintas-kanal terbukti lemah |
| 5 | S-D1 tool_wear progresi-onset (+S-D2 VMD) | `tool_wear` LULUS? | SEDANG | SEDANG | mengalahkan confound run-order & plafon lift; change-point wajib divalidasi |
| 6 | S-A2 stuck F-10/F-12 | `stuck` ketahanan fold | SEDANG-TINGGI | SEDANG | bagian dari parse #3 |
| 7 | S-C2 hyd label pit/flow-mismatch | `hyd` cadangan | SEDANG | SEDANG-BESAR | fisika berbeda; tunda sampai S-C1 selesai |
| 8 | S-A3 Snorkel / S-C3 survival / S-D4 rank / S-B2 stand / S-B3 ordinal | ketukuan/masing-masing | rendah-sedang | bervariasi | pelengkap, bukan primer |

**Jalur ke target operator:**
- **5 kelas LULUS (target minimum):** `vib` + `ssi` + `stuck`(S-A1) + `bit_wear`(S-F1) + `shk`(S-B1) → eksekusi #1+#2+#3.
- **Upside 6–7:** `hyd` lolos kalau onset punya sinyal precursor (S-C1) atau label pit/flow punya lift (S-C2); `tool_wear` lolos kalau change-point valid (S-D1). Keduanya dikerjakan SETELAH jalur 5 aman.
- Semua solusi adalah perbaikan LABEL/DATA/REFORMULASI — **bukan penurunan ambang** (lihat §8).

---

## 8. PERNYATAAN GATE (wajib)

Gate pra-reg V6 tetap **G1: lift RF ≥1,5 pada mayoritas sumur uji layak dinilai; G2: AUPRC RF ≥ AUPRC canary-kedalaman pada mayoritas**; aturan persistence → "layak bersyarat" tetap berlaku; <30 positif = UNDERPOWERED; LOWO; fitur jendela lampau / label jendela depan; kanal pembentuk label dilarang jadi fitur. **Tidak ada solusi di dokumen ini yang mengubah ambang, metrik, canary, atau aturan mayoritas.** Yang berubah hanya: (a) definisi LABEL (status→onset/progresi/fisika-label), (b) UNIT (window→stand pada S-B2 sebagai opsi), (c) TAMBAHAN DATA (parse wellbore yang benar-benar punya kanal — diverifikasi §1), (d) reformulasi model (survival/ordinal/rank) yang skornya tetap dievaluasi dengan gate biner yang sama. Setiap perubahan label/unit = pra-registrasi BARU (di-hash sebelum training), konsisten `PROTOCOL_RISET_TIM.md`.

---

## 9. CATATAN VERIFIKASI & ANTI-KARANGAN

1. Semua angka kegagalan dikutip dari `docs/V6_E1_ML_DESIGN.md` §4.4 (hasil run nyata V6).
2. Semua klaim "data X ada" diberi path & dicek langsung: `labels_curated_v2.csv` (1.413 baris termasuk header — CATATAN selisih dengan angka 884 event V6_R1 wajib direkonsiliasi sebelum dipakai S-A3), 8 xlsx toolwear (ada), `USROP_labeled.csv` 198.929 baris termasuk header (ada), F-9 A time.csv 419.747 baris (ada), raw F-10/F-4/F-12/F-15/F-9/F-1 C/F-11 (ada semua, struktur folder diverifikasi).
3. Peta kanal §1 = scan mandiri 2026-10-11 (3 skrip, 3 JSON bukti); F-1 C/F-11 divalidasi DENGAN menemukan kanal surface konvensi-lama (FLOWIN 990 file dll.) sehingga hasil nol-kanal-dysfungsi bukan artefak pembacaan kosong.
4. 8 DOI baru diverifikasi Crossref di sesi ini (judul cocok); 12 sitasi dipakai ulang dari V6-R1 run-3 (sudah 17/17 Crossref). Tidak ada DOI yang ditulis tanpa verifikasi.
5. Solusi yang memakai penalaran engineering tanpa paper ditandai eksplisit ("engineering judgment"): S-B2, S-C2 (bagian aturan washout klasik), S-D4, S-E2.
6. Hal yang TIDAK bisa dijanjikan: keberhasilan `hyd`/`tool_wear` (sinyal bisa terbukti tidak ada — tes pembeda tiap solusi menyatakan apa yang membuktikan kegagalan).
7. Hasil `sources.py verify`: 22/22 id dikutip terdaftar di ledger, 0 id asing, 0 `[unverified]`. Verifier gagal HANYA pada satu baris [20] karena parser-nya memotong DOI yang berisi kurung `10.1016/0148-9062(65)90022-7` pada tanda `)` — URL di blok Sources dan di ledger identik (dicek manual, baris 267); DOI itu sendiri terverifikasi Crossref di sesi ini. Kegagalan ini murni artefak parser, bukan ketidakcocokan sumber.

## Sources

[1] https://doi.org/10.1016/j.cie.2023.109566 — Tasci 2023 RUL predictive maintenance survey
[2] https://doi.org/10.1186/s44147-026-00980-1 — Husseiny 2026 ML standpipe pressure prediction
[3] https://doi.org/10.3390/s24248107 — Wang 2024 tool wear VMD-BP
[4] https://doi.org/10.3390/s26061915 — Shadi 2026 survival models PdM RUL
[5] https://doi.org/10.1007/s00778-019-00552-1 — Ratner Snorkel weak supervision VLDB J
[6] https://doi.org/10.1609/aaai.v33i01.33014763 — Ratner 2019 multi-task weak supervision AAAI
[7] https://doi.org/10.1145/3699955 — ACM CSUR comprehensive survey rare event prediction
[8] https://doi.org/10.1016/j.jmapro.2019.10.020 — Tool wear monitoring audio signals ML
[9] https://doi.org/10.3390/forecast8030052 — Learning rare events deep learning extreme price prediction
[10] https://arxiv.org/abs/2311.15654 — Event detection in time series universal DL regression approach
[11] https://arxiv.org/abs/2503.07440 — Cao 2025 Crossformer early stuck pipe signs Volve
[12] https://doi.org/10.3390/app15095042 — Al-Mamoori 2025 autoencoder stuck pipe Volve
[13] https://doi.org/10.1016/j.petrol.2021.109489 — Mopuri 2022 unsupervised LSTM-AE stuck pipe early sign
[14] https://doi.org/10.2118/204462-PA — Tsuchihashi 2021 3D CNN early stuck pipe sign
[15] https://doi.org/10.2118/228303-PA — Liu 2025 SPE J dysfunctions surface data bit failure forensics
[16] https://doi.org/10.2118/200006-MS — Saini 2020 physics-based 10 dysfunction categories surface sensors
[17] https://doi.org/10.2298/TSCI2502521L — Liu 2025 Thermal Science SSI stick-slip grading
[18] https://doi.org/10.1038/s41598-023-33411-9 — Saadeldin 2023 3 vibration types from surface data
[19] https://doi.org/10.2118/204063-MS — Yi 2021 dysfunction classifiers surface damping
[20] https://doi.org/10.1016/0148-9062(65)90022-7 — Teale 1965 specific energy rock drilling
[21] https://www.hpinc.com/wp-content/uploads/2025/08/Use-of-Mechanical-Specific-Energy-Calculation-in-Real-Time-to-Better-Detect-Vibrations-and-Bit-Wear-While-Drilling-AADE-17-NTCE-033_Extract.pdf — Menand Mills 2017 MSE MSE/DS vibrations bit wear
[22] https://doi.org/10.1016/j.petrol.2019.05.021 — Hegde 2019 stick slip severity ML
