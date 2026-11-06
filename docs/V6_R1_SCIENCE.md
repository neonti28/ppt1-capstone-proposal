# V6-R1 — RISET ILMIAH PEMECAH BUNTU: label turunan, bukti sensor permukaan, taksonomi >3 dysfungsi

**Tanggal:** 10 Oktober 2026 · **Role:** [R&D] · **Task kanban:** `t_32e0ff8b` (board `capstone-v6-solve`)
**Status:** SELESAI + TERVERIFIKASI 3 RUN — 3 masalah diriset (masing-masing ≥3 paper dengan URL asli), ≥3 rumus benar-benar **diuji** pada data Volve nyata dengan angka populasi, satu bug data ditemukan & dilaporkan. **Run-3 (§10): 17/17 DOI lolos Crossref, 34 angka dihitung ulang dari data mentah, 2 cacat dokumen ketemu & diperbaiki (kuantil MSE/DS salah label, DOI sumber [7] salah), 0 angka verdict berubah.**

**Riset pendahuluan: `literature-review` — pencarian multi-sumber terdokumentasi (web_search, OpenAlex, Crossref, web_extract untuk teks penuh), tanggal akses 2026-10-10, query dicatat §1.3; sintesis dikelompokkan per masalah, bukan ringkasan per-paper.**
**Riset pendahuluan: `paper-lookup` — DOI diverifikasi lewat OpenAlex/Crossref sebelum dikutip; klaim "paper memakai data X" diambil dari teks penuh yang diekstrak, bukan dari judul; satu paper dinyatakan WITHDRAWN setelah PDF-nya gagal dimuat (lihat §2.1).**
**Riset pendahuluan: `scientific-critical-thinking` — setiap klaim dinilai apa yang benar-benar ditunjukkan datanya (termasuk klaim lemah AUC ~0,5 dan populasi nol), keterbatasan daftar eksplisit di §7, kekuatan bukti tidak dinaikkan melebihi datanya.**
**Riset pendahuluan: `hypothesis-generation` — tiga "solusi mati" diperlakukan sebagai hipotesis yang bisa ditolak: H1 (label bisa diturunkan dari data ada), H2 (sensor permukaan cukup), H3 (>3 kelas bisa dihitung) — tiap hipotesis punya tes pembeda dan angka hasil (§2–§4).**

---

## 0. RINGKASAN EKSEKUTIF

| Masalah | Verdict | Bukti kunci (angka nyata di data Volve) |
|---|---|---|
| **#1 Label tidak ada/tidak cukup** | **TERPECAH sebagian besar** | Rumus Teale MSE dihitung ulang di 198.928 baris USROP = kolom tersimpan (selisih median **0,005%**, korelasi log10 **0,9999999999989**); label rule lama tereproduksi **100%**. MSE/DS memberi 4 populasi kelas. Label turunan LAS (porositas/resistivitas/VSH/Sw) punya populasi 5–30% per kelas. |
| **#2 Sensor permukaan tidak cukup** | **TERPECAH untuk kelas stuck & stick-slip; TIDAK untuk kelas shock/axial** | 8 kanal surface (180 s mean+CV) → AUC 3-fold terhadap label downhole MWD: stuck **0,964/0,977**, status stick-slip **0,898/0,967**, p2p stick-slip **0,878/0,933**; shock risk hanya **0,797/0,821** (23 positif). |
| **#3 Taksonomi >3 dysfungsi** | **TERPECAH** | 7 kelas dihitung dengan populasi nyata di F-14 WITSML: 82.530 / 320 / 180 / 714 / 394 / 58.317 baris (+ kelas severe = 0, jujur). 5 kelas di USROP: 49.732 / 15.183 / 49.629. |

**Temuan sampingan wajib (bug):** kanal `WHIRL_RT` dan `BOUNCE_RT` pada WITSML F-14 adalah **duplikat** — di file mentah 19 file berisi keduanya, 18.147 baris bernilai **100% identik, 0 baris berbeda** (§5). Keduanya **tidak boleh dihitung sebagai 2 kelas independen**.

---

## 1. METODE, DATA, REPRODUKSI

### 1.1 Data Volve yang dipakai (semua nyata, lokal)

| Dataset | Path | Ukuran | Dipakai untuk |
|---|---|---|---|
| USROP 12 sensor (7 sumur) | `data/USROP_labeled.csv` | 198.928 baris × 17 kolom | Uji MSE, MSE/DS, taksonomi surface |
| USROP timestamped | `data/volve/usrop_timestamped.csv` | 198.928 baris, 2007-09-23 → 2009-07-07 | Uji kelangkaan label vs event kurasi |
| Event kurasi (DDR) | `data/volve/labels_curated_v2.csv` | 884 event (yes 50 / uncertain 571 / no 263) | Ground truth kelangkaan label |
| WITSML time-based F-14 (ter-parse) | `data/volve/witsml_parsed/F-14.csv` | 1.648.026 baris × 238 kanal | Uji sinyal surface vs MWD, taksonomi |
| WITSML mentah F-14 | `data/volve/witsml_raw/...F-14/1/log/2/*/*.xml` | 19 file berisi WHIRL/BOUNCE | Verifikasi bug duplikasi kanal |
| LAS petrofisika F-15 D | `data/volve/external/spwla_volve_logs/*.LAS` | 45.391 + 12.198 sampel kedalaman | Uji label turunan dari LAS |
| Paper lokal | `Reference/Tunkiel et al. 2021…pdf`, `Reference/MDPI 2025.pdf` | 12 & 16 halaman | Klaim paper dibaca dari teks asli |

Kanal kunci di F-14 (deskripsi dari `F-14.qc.json`): `STKSLP` *StickSlip status indicator*, `STICK_RT` *MWD Stick-Slip PKtoPK RPM*, `VIBLAT_RT` *MWD Vibration Lateral* (ft/s²), `SHKRSK_RT` *MWD Shock Risk* (0–3), `STUCK_RT` (0–3), plus surface `TQA` (kN·m), `RPM`, `SWOB`, `HKLD`, `SPPA`, `ROP`, `TFLO`, `BPOS`.

### 1.2 Protokol uji

- Setiap rumus dihitung **dari nol** pada data (bukan membaca kolom hasil), lalu dibandingkan/diuji terhadap kolom atau kanal referensi.
- Jendela waktu berbasis waktu (`rolling('180s', min_periods=20)`), bukan jumlah baris, karena jarak sampling F-14 tidak seragam (median Δt 3,97 s; maksimum gaps berbulan-bulan).
- Uji beda surface↔downhole: AUC Mann-Whitney (implementasi rank sendiri) untuk uji univariat; LogisticRegression + GradientBoosting dengan `StratifiedKFold(3, shuffle, seed=20261010)` untuk multivariat.
- Skrip: `v6_r1_tests.py`, `v6_r1_tests_v2.py`, `v6_r1_tests_v3.py`, `v6_r1_t7b.py`, `t8_las.py`, `t8b_las_out.py`, `whirl_scan.py` (semua di `~/.hermes/cache/scratch/`); hasil mentah: `v6_r1_test_results.json`, `…_v2.json`, `…_v3.json`, `v6_r1_t7b_cv.json`, `v6_r1_las_labels.json`, `v6_r1_las_output_labels.json`, `whirl_bounce_scan.json`.

### 1.3 Query pencarian (reproducible, akses 2026-10-10)

`web_search`: (a) "drilling dysfunction detection formulas mechanical specific energy stick-slip whirl bit bounce surface sensors paper"; (b) "physics-informed labeling weak supervision drilling failure labels derived from existing well data"; (c) "surface sensor measurements sufficient predict downhole drilling dysfunctions … paper"; (d) "classification of drilling dysfunction taxonomy … buckling differential sticking dataset machine learning multi-class"; (e) "stick slip index formula SSI = (rpmmax-rpmmin)/rpmavg grading"; (f) "Teale mechanical specific energy formula"; (g) "differential sticking force formula mud overbalance"; (h) "critical helical buckling load drillstring Paslay Bogy".
`OpenAlex` (9 judul, `search=`), `Crossref` (`query.bibliographic` — kena HTTP 429 di 8 query pertama, dicatat sebagai keterbatasan, diganti OpenAlex), `web_extract` teks penuh: PMC10110595, arXiv 2503.07440, thermalscience.rs TSCI2502521L, aade.org AADE-17-NTCE-033, hpinc.com extract, crewes.org CRR202310, scilit Saini 2020.

---

## 2. MASALAH #1 — LABEL TURUNAN DARI DATA YANG SUDAH ADA

### 2.1 Paper (5 sumber; DOI diverifikasi)

1. **Teale, R. (1965). "The concept of specific energy in rock drilling."** *Int. J. Rock Mech. Min. Sci.* DOI **[10.1016/0148-9062(65)90022-7](https://doi.org/10.1016/0148-9062(65)90022-7)** (diverifikasi Crossref 2026-10-10: Vol. 2, Issue 1, hlm. 57–73 — varian 90016-1 tercatat sebagai Vol. 2, Issue 2, hlm. 245, kemungkinan artikel terkait, jadi yang dipakai adalah 90022-7). Rumus: `MSE = WOB/A_B + 120π·RPM·TOB/(A_B·ROP)` (satuan field: psi, in², ft·lb, ft/hr) — versi SI setara `MSE = WOB/A + 2π·N_rps·T/(A·ROP)`. → **label ketidakefisienan murni dari 4 sensor surface yang sudah ada.**
2. **Menand, S. & Mills, K. (2017). "Use of MSE Calculation in Real-Time to Better Detect Vibrations and Bit Wear." AADE-17-NTCE-033.** Teks penuh: [aade.org/…/AADE-17-NTCE-033_-_Menand.pdf](https://www.aade.org/application/files/7815/7132/1752/AADE-17-NTCE-033_-_Menand.pdf). Rumus: `DS = WOB/(R·DOC)` (Eq. 5), `DOC = ROP/(60·RPM)`; aturan: **MSE/DS 1–1,5 = efisien; >5 = inefisiensi parah; MSE & MSE/DS naik bersama = vibrasi; MSE naik + MSE/DS turun = bit wear/balling.** Juga: TOB bisa diturunkan dari `TOB = T_surface − T_drillstring` (torque-drag) atau ΔP motor (Eq. 2–4).
3. **Cao, B., Song, Y., Yang, J., Li, L. (2025). "Early signs of stuck pipe detection based on Crossformer." arXiv:2503.07440.** [https://arxiv.org/abs/2503.07440](https://arxiv.org/abs/2503.07440). **Label dibuat tanpa data baru**: model dilatih hanya pada data normal, `Risk = Σ_d Norm(relative reconstruction error)` (Eq. 12), threshold dinamis `W_v = (1+MSE_τ)(μ + 2σ)` dengan 95% CI dari data normal (Eq. 14). Data = **Volve time-based, parameter surface yang sama dengan kita** (torsi, hookload, RPM, SPP, flow, WOB, ROP). Hasil: peringatan 2,67–7,37 menit sebelum stuck. Dataset TSPP-nya publik: [github.com/promiseeee/Time-series-stuck-pipe-prediction](https://github.com/promiseeee/Time-series-stuck-pipe-prediction).
4. **Al-Mamoori, H.N., Tian, J., Ma, H. (2025). "Stuck Pipe Detection … Using Deep Learning Autoencoder." *Applied Sciences* 15, 5042.** DOI **[10.3390/app15095042](https://doi.org/10.3390/app15095042)** (ada lokal: `Reference/MDPI 2025.pdf`, dibaca dari PDF). Autoencoder dilatih **hanya pada kondisi normal Volve**, reconstruction error = anomali: **akurasi 99,06%, AUC 0,958, precision 97,12%, recall 91,34%, F1 94,15%.**
5. **Mopuri, K.R., Bilen, H., Tsuchihashi, N. et al. (2021/2022). "Early sign detection for the stuck pipe scenarios using unsupervised deep learning." *J. Pet. Sci. Eng.* 208, 109489.** DOI **[10.1016/j.petrol.2021.109489](https://doi.org/10.1016/j.petrol.2021.109489)** (diverifikasi OpenAlex, dikutip oleh Cao 2025) — LSTM-AE tanpa label.
   - **Catatan kejujuran:** kandidat ke-6, *Hernandez-Matamoros et al. 2023, "Semi-Supervised Approach for Early Stuck Sign Detection"*, arXiv:2302.11135, ternyata **WITHDRAWN** (halaman abstract menyatakan *"This version has been withdrawn and is unavailable"*, PDF 404 saat diekstrak). **Tidak dipakai sebagai dasar.** Query yang dicoba tercatat §1.3.

### 2.2 Rumus yang DIUJI + hasil nyata

**Uji 1 — Teale MSE pada USROP (198.928 baris, 7 sumur).**
Hitung ulang dari nol: `A = π/4·(D/1000)²`, `WOB_N = kkgf·9,80665·1000`, `T_Nm = kN·m·1000`, `ROP_ms = m/h / 3600`.

| Metrik | Nilai |
|---|---|
| Baris valid | 198.928 / 198.928 |
| Selisih relatif median vs kolom `MSE` tersimpan | **4,98e-05 (0,005%)** — p95 4,98e-05 |
| Korelasi log10 (hitung ulang vs tersimpan) | **0,9999999999989** |
| Median MSE | 102.631 psi (hitung ulang 102.636 psi) |

→ Kolom MSE proyek **terverifikasi independen** sebagai Teale-1965 (bukan angka karangan).

**Uji 2 — label rule lama (MSE > P75; elif ROC_coef < P25) tereproduksi:**

| Kelas | Populasi | % |
|---|---|---|
| `high_MSE_bit_wear` | **49.732** | 25,00% |
| `low_ROP_efficiency` | **15.183** | 7,63% |
| `normal` | **134.013** | 67,37% |
| Kecocokan dengan kolom `label` tersimpan | **100,0%** | — |

(P75 MSE = 256.600 psi; P25 ROC_coef = 1,604e-05.)

**Uji 3 — MSE/DS (Menand & Mills 2017) di USROP, n = 198.602 valid:**

| Kelas (atas dasar paper) | Populasi | % |
|---|---|---|
| Efisien (1 ≤ MSE/DS ≤ 1,5) | **12.501** | 6,29% |
| Antara (1,5 < rasio ≤ 5) | **93.334** | 47,00% |
| **Inefisiensi parah / vibrasi (ratio > 5)** | **78.212** | 39,38% |
| Rasio < 1 | **14.555** | 7,33% |
| Kuantil rasio 5/25/50/75/95% | **0,824 / 2,318 / 3,990 / 6,438 / 15,557** (DOC benar: `DOC = ROP[m/h] ÷ (60·RPM)`, hasil independen run-3 §10 identik dengan `R1_t32e0ff8b_results_v3.json`) — peringatan: versi satuan-salah (`DOC` dihitung dari ROP m/s) masih tersimpan di `v6_r1_test_results_v2.json` blok `T5_MSE_DS` (median 0,0011, 99,99% <1) dan **tidak boleh dipakai**; **pemakaian praktis = relatif terhadap baseline per sumur, bukan ambang absolut 1–1,5 yang dirancang untuk Eagle Ford**) | |

> **Catatan batas (jujur):** ambang absolut 1–1,5 / >5 dari paper berlaku untuk TOB downhole & formasi Eagle Ford. Di USROP dengan DOC yang benar (satuan m/h): median rasio **3,99**, hanya **6,29%** masuk zona "efisien" 1–1,5 dan **39,38%** jatuh >5 — artinya mayoritas baris ditandai tidak efisien oleh ambang papuan, sehingga ambang dipakai **relatif per sumur (z-score/perzentil), bukan absolut**. Angka 99,99% <1 hanya muncul bila DOC dihitung keliru (m/s) dan dipakai hanya sebagai bukti sensitivitas satuan. **Rekomendasi: pakai rasio sebagai fitur ter-standardisasi per sumur (z-score/perzentil), jangan ambang absolut.**

**Uji 4 — kelangkaan label (mengukur masalahnya, bukan asumsi):**
Gabungan `usrop_timestamped` (198.927 baris ber-timestamp) dengan 884 event kurasi (`act_start`–`act_end`):

| Metrik | Nilai |
|---|---|
| Baris USROP di dalam jendela event apa pun | **8.533 (4,29%)** |
| Event `bha_relevant = yes` | **50** dari 884 (uncertain 571, no 263) |
| Per sumur (baris di event / total) | F-9Ad 312/13.746 · F-7d 366/6.389 · F-14d 1.816/47.645 · F-15d 1.136/53.041 · F-15Sd 3.670/51.707 · F-5d 867/18.548 · F-9d 366/7.851 |

→ **"Label tidak ada" itu terukur: 95,7% baris tidak punya label peristiwa; hanya 50 event BHA-positif.** Ini membenarkan pendekatan label turunan (physics/anomaly), bukan menunggu anotasi manual.

**Uji 5 — label turunan dari LAS F-15 D (`spwla_volve_logs`, dibaca manual dari LAS 2.0):**

| Rumus label | Sampel valid | Populasi kelas | % |
|---|---|---|---|
| Density porositas `φ = (2,65 − ρ_b)/1,65` > 0,25 | 13.592 | **3.729** | 27,44% |
| Resistivitas dalam `RT > 10 Ω·m` | 32.685 | **5.823** | 17,82% |
| `VSH > 0,4` (shale, OUTPUT LAS) | 12.081 | **3.310** | 27,40% |
| `SW < 0,5` (hidrokarbon) | 11.936 | **3.576** | 29,96% |
| `PHIF > 0,25` | 11.936 | **649** | 5,44% |
| `SAND_FLAG = 1` (flag turunan bawaan LAS) | 12.081 | **8.893** | 73,62% |
| Breakout `CALI − BS > 2 in` | 13.658 | **0** | 0,00% (median selisih hanya 0,047 in, p95 0,125 in → lubang praktis in-gauge) |

→ 6 dari 7 label LAS **punya populasi layak**; breakout gagal di sumur ini (negatif jujur, jangan diklaim berhasil).

### 2.3 Rekomendasi Masalah #1

1. **Jadikan MSE (Teale) + MSE/DS sebagai sumber label resmi** — sudah terverifikasi reproduksi 100%; tambah kelas ke-3/ke-4 dari rasio MSE/DS ter-standardisasi per sumur (z-score), bukan ambang absolut.
2. **Gunakan jalur anomaly-based (Cao 2025 / Al-Mamoori 2025 / Mopuri 2021)**: latih AE/forecast hanya pada data normal → reconstruction error + threshold `μ+2σ` = label "tanda dini" **tanpa anotasi manual**; preseden langsung di Volve dengan AUC 0,958.
3. **Label LAS/DLIS tersedia dan berpenduduk** (porositas, VSH, Sw, sand flag) untuk fitur geologi/label litologi — bukan untuk label kegagalan langsung.
4. Kelangkaan label (4,29% baris, 50 event BHA) **dilaporkan sebagai fakta terukur**, bukan sebagai alasan "tidak bisa" — karena dua jalur di atas tidak butuh label baru.

---

## 3. MASALAH #2 — APAKAH SENSOR PERMUKAAN CUKUP?

### 3.1 Paper (5 sumber; baca klaim persisnya)

1. **Saadeldin, R., Gamal, H., Elkatatny, S. (2023). "Detecting downhole vibrations through drilling horizontal sections: machine learning study." *Scientific Reports* 13, 6204.** DOI **[10.1038/s41598-023-33411-9](https://doi.org/10.1038/s41598-023-33411-9)** (teks penuh PMC10110595). **Klaim persis:** model RBF/SVM/ANFIS/FN dilatih **hanya dari data rig surface**, memprediksi **tiga tipe getaran downhole (aksial, torsional, lateral)**; hasil *"correlation coefficient higher than 0.9"* dan *"average absolute percentage error below 7.5%"*, divalidasi pada well tak terlihat. Horizon: selama pengeboran bagian horizontal, sampel 1 Hz. (Dikutip juga: Zha & Pham 2018 surface-only stick-slip 96–99%; Wiktorski 2019 SVM surface stick-slip R² 0,98 & lateral 0,93; Okoli 2019 intra-BHA 50–80%.)
2. **Saadeldin, R. et al. (2021). "Intelligent Model for Predicting Downhole Vibrations Using Surface Drilling Data During Horizontal Drilling." *J. Energy Resour. Technol.* 144, 083002.** DOI **[10.1115/1.4052794](https://doi.org/10.1115/1.4052794)** (diverifikasi OpenAlex).
3. **Liu, W. et al. (2025). "Machine Learning Model for Identifying Drilling Dysfunctions from Surface Data and Bit Failure Forensics." *SPE Journal*.** DOI **[10.2118/228303-pa](https://doi.org/10.2118/228303-pa)** — identifikasi dysfungsi **dari data surface + forensik bit**, sebagai alternatif *"downhole sensors"*.
4. **Lai, S.W. et al. (2015). "Surface Torque/Tension Measurements Used To Detect and Calculate Stick/Slip." *JPT*.** DOI **[10.2118/0915-0146-jpt](https://doi.org/10.2118/0915-0146-jpt)** — deteksi stick-slip murni dari torsi/tegangan surface (dikutip di PMC10110595 ref. 28).
5. **Bukti berlawanan (wajib dilaporkan):**
   - **Hess, S. et al. (2023), CREWES CRR202310** [PDF](https://www.crewes.org/Documents/ResearchReports/2023/CRR202310.pdf): *"system responses from downhole can be undetectable at the surface due to energy stop bands in the drilling assembly … or friction in deviated and deep wells (attenuation)."*
   - **Yi, M. et al. (2021), SPE-204063-MS** DOI **[10.2118/204063-ms](https://doi.org/10.2118/204063-ms)**: *"Detecting drilling dysfunctions from surface data is not always easy as downhole vibrations tend to get damped before they reach surface sensors."*
   - **SPE JPT (TWA)** [jpt.spe.org](https://jpt.spe.org/twa/drilling-and-logging-equipment-reliability-in-a-downhole-vibration-environment): *"Lateral vibrations do not propagate well through the drillstring and often cannot be detected by observing surface parameters."*

### 3.2 Uji di Volve F-14 (1.648.026 baris; jendela 180 s)

**Uji A — proxy surface UNIVARIAT vs kebenaran downhole MWD** (156.329 baris pengeboran, RPM>0 & SWOB>0):

| Pasangan (surface → label MWD) | n | n_pos | AUC | Spearman ρ | p |
|---|---|---|---|---|---|
| CV torsi surface → `STICK_RT` (p2p stick-slip ≥ P75) | 4.910 | 1.843 | **0,4598** | −0,114 | 1,5e-15 |
| SSI surface (RPM) → `STKSLP>0` | 2.989 | 1.673 | **0,4977** | +0,149 | 2,5e-16 |
| CV torsi → `VIBLAT_RT ≥ P75` (whirl/lateral) | 373 | 45 | **0,5351** | +0,143 | 0,0057 |
| CV torsi → `SHKRSK_RT ≥ 1` (shock/aksial) | 4.451 | 21 | **0,5641** | +0,015 | 0,31 (ns) |
| CV RPM → `SHKRSK_RT ≥ 1` | 4.484 | 27 | **0,5336** | +0,009 | 0,54 (ns) |
| CV torsi → `STUCK_RT ≥ 1` (indikator stuck) | 1.205 | 73 | **0,8313** | +0,274 | 3,0e-22 |

→ **Satu metrik surface tunggal TIDAK cukup** untuk getaran downhole (AUC ≈ 0,46–0,56 = kisaran tebakan), **tapi cukup untuk indikator stuck** (0,83).

**Uji B — 8 kanal surface + fitur 180 s (mean & CV dari TQA, RPM, SWOB, HKLD, SPPA, ROP, TFLO, BPOS), StratifiedKFold 3, seed 20261010:**

| Target downhole | n | n_pos | AUC LogReg (3 fold) | AUC GBM (3 fold) |
|---|---|---|---|---|
| `STUCK_RT ≥ 1` (stuck) | 1.205 | 72 (5,98%) | **0,9915 / 0,9442 / 0,9563 → 0,964** | **0,9948 / 0,9943 / 0,9404 → 0,977** |
| `STKSLP > 0` (status stick-slip MWD) | 1.350 | 728 (53,9%) | **0,8903 / 0,9062 / 0,8975 → 0,898** | **0,9626 / 0,9737 / 0,9650 → 0,967** |
| `STICK_RT ≥ P75` (p2p stick-slip) | 3.272 | 811 (24,8%) | **0,8709 / 0,8714 / 0,8908 → 0,878** | **0,9286 / 0,9243 / 0,9450 → 0,933** |
| `SHKRSK_RT ≥ 1` (shock risk) | 2.863 | 23 (0,80%) | 0,8601 / 0,6757 / 0,8543 → **0,797** | 0,9236 / 0,6970 / 0,8434 → **0,821** |

(Split temporal 70/30 juga dijalankan: STKSLP AUC 0,79 (LR) / 0,69 (GBM); STICK_RT 0,50 / 0,66 — lebih rendah karena distribusi positif menumpuk di fold uji; karenanya hasil utama memakai stratified 3-fold dan **dilaporkan keduanya**.)

### 3.3 Interpretasi kritis (scientific-critical-thinking)

- **Kuat:** klaim paper "surface cukup untuk stuck & stick-slip" **terkonfirmasi independen di Volve** (AUC 0,88–0,98), sejalan Saadeldin 2023 (R>0,9) dan Lai 2015.
- **Lemah/tidak dikonfirmasi:** untuk **shock/aksial (bit bounce)** surface hanya AUC 0,80–0,82 dengan 23 positif → **tidak boleh diklaim cukup**; ini konsisten dengan peringatan Yi 2021, Hess 2023, dan SPE JPT bahwa lateral/aksial teredam di permukaan.
- **Ancaman validitas:** target `STKSLP`/`STICK_RT` berasal dari MWD dengan non-null terbatas (8.357 / 23.209 baris) → n uji 1.350–3.272; jumlahnya cukup untuk AUC tapi **bukan untuk klaim generalisasi antar-sumur** (uji hanya F-14).
- **Data leakage dicegah:** fitur hanya 180 s lampau (rolling mean/CV), target pada baris yang sama; tidak ada kolom `label`/`MSE`/`D_exp`/`ROC_coef` yang masuk fitur.

### 3.4 Rekomendasi Masalah #2

1. **Klaim yang boleh dipakai di laporan:** *"Sensor permukaan (8 kanal, fitur 180 s) cukup untuk memprediksi stuck (AUC 0,96–0,98) dan stick-slip (0,88–0,97) di F-14 Volve."*
2. **Klaim yang TIDAK boleh dipakai:** "sensor permukaan mendeteksi semua dysfungsi" — shock/axial hanya 0,80–0,82, whirl/lateral univariat ~0,54.
3. Untuk kelas aksial/lateral: pakai kanal MWD yang memang ada (`SHKRSK_RT`, `VIBLAT_RT`) sebagai **label/sumber kelas**, bukan berharap surface membawanya.

---

## 4. MASALAH #3 — TAKSONOMI >3 JENIS DYSFUNSI/KERUSAKAN

### 4.1 Paper (5 sumber, minimal 5 dysfungsi + rumus identifikasinya)

1. **Saini, G. et al. (2020). "An Automated Physics-Based Workflow for Identification and Classification of Drilling Dysfunctions…"** DOI **[10.2118/200006-ms](https://doi.org/10.2118/200006-ms)** (abstrak penuh via [scilit](https://www.scilit.com/publications/fafef3ed2336f00e8cf472b755cca8b5)). **Kunci: "leveraging commonly available rig surface sensor data"; MSE + depth-of-cut dihitung, decision-tree physics-based, >100 sumur tidak konvensional, "10 different dysfunction categories were classified" — paling umum: whirl, stick-slip, bit balling.** → **bukti langsung bahwa >3 (bahkan 10) kelas bisa diturunkan dari sensor surface.**
2. **Menand & Mills 2017 (AADE-17-NTCE-033, §2.1 no.2)** — membedakan **3 penyebab** dari 2 indikator: MSE + MSE/DS (vibrasi vs bit wear vs bit balling), plus aturan 1–1,5 / >5.
3. **Liu, W. et al. (2025). "Intelligent Identification Method for Stick-Slip Vibration Based on Downhole Data." *Thermal Science* 29(2B), 1521–1526.** DOI **[10.2298/TSCI2502521L](https://doi.org/10.2298/TSCI2502521L)** (teks penuh PDF). **Rumus SSI: `SSI = (rpm_max − rpm_min)/(2·rpm_avg)`; grading: `SSI < 1` → torsional vibration; `1 < SSI < 3` → moderate stick-slip; `SSI ≥ 3` → severe stick-slip.**
4. **Hegde, C., Millwater, H., Gray, K. (2019). "Classification of drilling stick slip severity using machine learning." *J. Pet. Sci. Eng.* 179, 1023–1036.** DOI **[10.1016/j.petrol.2019.05.021](https://doi.org/10.1016/j.petrol.2019.05.021)** — SSI diklasifikasi low/high dengan ML (bukti SSI dipakai sebagai label lapangan).
5. **Liu, W. et al. (2025). SPE Journal, "…from Surface Data and Bit Failure Forensics."** DOI **[10.2118/228303-pa](https://doi.org/10.2118/228303-pa)** — klasifikasi dysfungsi dari surface + forensik bit.
   - Rumus pendukung (untuk lengkapnya 5+ dysfungsi, di luar Volve test): **differential sticking** `F = μ·A_contact·ΔP` ([drillingformulas.com](https://www.drillingformulas.com/differential-sticking-causes-stuck-pipe); ulasan ScienceDirect "Differential Sticking" — `F = μ·A·(p_m − p_f)`); **buckling helical kritis** (Paslay & Bogy 1964; ulasan AADE-19-NTCE-080 [PDF](https://www.aade.org/application/files/9715/7132/0378/AADE-19-NTCE-080_-_Menand.pdf)) — **tidak diuji** karena butuh parameter string/BHA yang tidak ada di USROP/WITSML (lihat §7).

### 4.2 Rumus yang DIUJI + populasi kelas nyata

**Dataset F-14 WITSML (jendela 180 s):**

| # | Kelas dysfungsi | Rumus + sumber | Ambang uji | Populasi | % terhadap basis |
|---|---|---|---|---|---|
| 1 | Torsional oscillation / stick-slip ringan | `TVI = std(TQA)/mean(TQA)` (torque variation index; Intellicess/SPE-212515-MS) | ≥ P75 (0,1224) | **82.530** | 25,0% dari 330.121 jendela |
| 2 | Moderate stick-slip | `SSI = (RPM_max−RPM_min)/(2·RPM_avg)` (Liu 2025 / Hegde 2019) | 1 ≤ SSI < 3 | **320** | 0,09% dari 344.396 jendela |
| 3 | Severe stick-slip | SSI ≥ 3 | ≥3 | **0** | 0,00% (jujur: tidak ada) |
| 4 | Bit bounce / aksial (proxy MWD) | `SHKRSK_RT ≥ 1` (MWD Shock Risk 0–3) | ≥1 | **180** | dari 21.643 non-null |
| 5 | Whirl / lateral (proxy MWD) | `VIBLAT_RT ≥ P75` (MWD Vibration Lateral, ft/s²) | ≥ 32,174 ft/s² | **714** | dari 2.247 non-null |
| 6 | Stuck / differential sticking (indikator) | `STUCK_RT ≥ 1` | ≥1 | **394** | dari 5.147 non-null |
| 7 | Hidraulik/pompa | residual `SPPA` vs bin `TFLO` (median+MAD, z-score) | \|z\| > 2 | **58.317** | 19,49% dari 299.228 |

> Metrik no.7 memakai `qcut(TFLO, 10)` (metode asli, diverifikasi ulang run-3: 58.317 persis); sensitif terhadap jumlah bin — dengan 20 bin hasilnya 47.359 (15,83%). Angka yang dipakai di dokumen = versi 10 bin; jangan bandingkan silang tanpa menyebut jumlah bin.

Basis: total 1.648.026 baris; baris pengeboran (RPM>0 & SWOB>0) **156.329**; baris dengan minimal satu metrik jendela **344.396**.

**Sebaran multi-kelas (5 kelas prosedural: torsi, stick-slip, shock, whirl, stuck):**

| Metrik | Nilai |
|---|---|
| Baris kena ≥1 kelas | **83.552** |
| Baris kena tepat 1 kelas | **82.966** |
| Baris kena ≥2 kelas | **586** |
| Pasangan ko-occurrence terbesar | torsi+stuck 197 · torsi+stick-slip 255 · torsi+whirl 98 · torsi+shock 36 · semua pasangan non-torsi = 0 |

**Dataset USROP (independen, 198.928 baris, 7 sumur):**

| # | Kelas | Rumus | Populasi |
|---|---|---|---|
| 1 | `high_MSE_bit_wear` | Teale MSE > P75 (256.600 psi) | **49.732** |
| 2 | `low_ROP_efficiency` | ROC_coef < P25 (1,604e-05) | **15.183** |
| 3 | Torsional anomaly | CV torsi berjalan (100 baris, min 60) ≥ P75 = 0,0701 | **49.629** |
| 4 (calon) | Hidraulik | residual SPP vs flow (z > 2) — sudah dipakai di rencana F2 | belum dihitung ulang di run ini (lihat §7) |

### 4.3 Temuan BUG (wajib, aturan #6)

`WHIRL_RT` dan `BOUNCE_RT` di `F-14.csv` tampak sebagai kolom terpisah tetapi **nilai duplikat**:

- Parsed CSV: **18.146 baris sama-sama non-null dan identik**; hanya 52 baris berbeda (selisih ±3 detik = offset timestamp antar file sumber).
- Verifikasi ke **file WITSML mentah** (19 file `1/log/2/*` yang memuat kedua mnemonic): total **18.147 baris berisi nilai → 100% identik, 0 baris berbeda**; 26 baris hanya `BOUNCE_RT`, 26 baris hanya `WHIRL_RT` (baris berselang-seling).
- Artinya: **duplikasi ada di data sumber Volve, bukan di parser kita**, tetapi konsekuensinya sama: kedua kanal **tidak bisa menjadi dua kelas independen**. Kelas whirl dipakai dari `VIBLAT_RT`, kelas aksial dari `SHKRSK_RT`.
- Bukti: `whirl_bounce_scan.json` (`{"files":19,"both":18147,"eq":18147,"diff":0}`).

### 4.4 Rekomendasi Masalah #3

1. **Taksonomi 6 kelas layak pakai** (semua dengan populasi > 0 dan rumus terpublikasi): torsional-oscillation, moderate-stick-slip, whirl/lateral, bit-bounce/shock, stuck/differential-sticking, hydraulic-anomaly (+ kelas ke-7 efficiency/MSE di USROP).
2. **Jangan pakai** `WHIRL_RT`/`BOUNCE_RT` sebagai kelas terpisah (bug §4.3), dan **jangan klaim** severe stick-slip ada di F-14 (populasi 0) — pakai agregat lintas sumur (F-5/F-15_S/F-15A juga punya `STKSLP`) bila kelas ini dibutuhkan.
3. Threshold bersifat **relatif (P75/z-score per sumur)** mengikuti praktik Saini 2020 (baseline MSE per formasi) dan rencana F1/F2 di `docs/11_PLAN_PERUBAHAN_LABELING.md`.

---

## 5. POSISI TERHADAP "PUTARAN SOLUSI → TIDAK BISA"

| Klaim lama | Status setelah V6-R1 | Angka |
|---|---|---|
| "Label tidak bisa diturunkan" | **DITEPIS** — 3 jalur teruji: physics (MSE/MSE/DS), anomaly (AE, preseden Volve AUC 0,958), LAS (6 label berpenduduk) | 49.732 / 78.212 / 3.729–8.893 baris |
| "Sensor permukaan tidak cukup" | **DITEPIS untuk stuck & stick-slip; DIPERTAHAN untuk shock/axial** | AUC 0,96–0,98 vs 0,80–0,82 |
| ">3 jenis kerusakan tidak bisa diturunkan" | **DITEPIS** — 6–7 kelas dengan populasi nyata di 2 dataset berbeda | 82.530 / 320 / 180 / 714 / 394 / 58.317 + 49.732 / 15.183 / 49.629 |
| "Tidak ada label peristiwa" | **DIUKUR, bukan diasumsikan** | 4,29% baris dalam jendela event; 50 event BHA-positif |

---

## 6. REKOMENDASI AKSIFIKASI (untuk kartu berikutnya)

1. **V6-D/E:** bangun label 6 kelas di F-14 + F-5 + F-15_S (kanal `STKSLP`, `STICK_RT`, `VIBLAT_RT`, `SHKRSK_RT`, `STUCK_RT` + dua proxy surface) — total kandidat >85 ribu baris di F-14 saja.
2. **V6-E:** model surface 8 kanal → stuck/stick-slip (bukti AUC sudah ada) dilatih **lintas sumur**, dengan split temporal + stratified; jangan sertakan klaim shock/axial tanpa downhole channel.
3. **Label DPR (dosen, ">3 jenis"):** ajukan 6 kelas di §4.2 dengan rumus + populasi per kelas sebagai lampiran — sudah memenuhi "minimal 3, berpotensi >3".
4. Perbaiki/standardisasi: rasio MSE/DS diperlakukan relatif per sumur; jangan ambang absolut 1–1,5.

---

## 7. DAFTAR HAL YANG BELUM DICEK / KETERBATASAN (wajib, aturan verifikasi)

1. **Uji lintas-sumur surface↔downhole (AUC) belum dijalankan** — semua uji AUC memakai **F-14 saja**. *Ditutup sebagian di §8.2* (populasi SSI multi-sumur untuk 5 wellbore lain), tetapi AUC lintas sumur tetap belum ada.
2. ~~Kelas `hydraulic anomaly` di USROP belum dihitung~~ → **ditutup di §8.3**: 28.046 baris (14,10%).
3. ~~Rumus differential sticking & buckling tidak diuji~~ → **buckling ditutup di §8.5** (terbukti non-diskriminatif, 79% baris); **differential sticking `F = μ·A·ΔP` tetap tidak diuji** (parameter kontak/permeabilitas tidak tersedia).
4. **Ambang absolut MSE/DS 1–1,5 / >5 hanya dipakai relatif** — median rasio dengan satuan DOC benar = **3,99** (bukan 0,0011; angka 0,0011 berasal dari bug satuan DOC m/s, sudah diperbaiki dan diverifikasi ulang di run-3 §10). Yang **masih belum diverifikasi silang**: TOB surface vs TOB downhole (`DTOR_RT` non-null hanya 2.351 baris dan median ≈ nol → patokannya sendiri rusak, lihat §9.3), sehingga klaim "MSE surface over-estimate" tetap berbasis analisis dimensi + rasio CCS/UCS (§9.2 I8–I9), bukan pembanding TOB langsung.
5. **Crossref kena HTTP 429** pada 8 dari 9 query verifikasi → sebagian DOI diverifikasi lewat **OpenAlex**; ini dicatat agar bisa diulang.
6. **Tidak ada pembacaan DLIS** (16 file `.DLIS` di `spwla_volve_logs`) — uji label LAS hanya 2 file `.LAS` (F-15 D).
7. **Klaim Saadeldin 2023 (R>0,9) tidak direplikasi persis** — replikasi kami memakai AUC/korelasi terhadap kanal MWD, bukan regresi R² pada 3 kanal getaran (kanal aksial/lateral terbatas non-null di F-14).
8. **arXiv 2302.11135 WITHDRAWN** — dinyatakan tidak dipakai; tidak dicari penggantinya di run ini (bisa jadi langkah lanjutan).
9. **`WHIRL_RT`/`BOUNCE_RT` duplikat diverifikasi pada 19 file F-14 saja**; belum dicek di sumur lain (F-5, F-15_S juga punya kedua kanal).

---

### Lampiran: path bukti mentah

**Durable (di repo proyek):** `/mnt/d/Capstone 1/scratch/v6_r1_evidence/` — 9 JSON hasil: `R1_t32e0ff8b_results_v2.json`, `R1_t32e0ff8b_results_v3.json`, `R1_t32e0ff8b_t7b_cv.json`, `v6_r1_test_results.json` (run awal), `v6_r1_las_labels.json`, `v6_r1_las_output_labels.json`, `whirl_bounce_scan.json`, `v6_r1_openalex.json`, `v6_r1_crossref.json` + 7 skrip (`v6_r1_tests*.py`, `v6_r1_t7b.py`, `t8_las.py`, `t8b_las_out.py`, `whirl_scan.py`).
**Catatan replikasi:** scratch bersama (`~/.hermes/cache/scratch/`) juga dipakai subagent lain — berkas `v6_r1_test_results_v2/v3.json` lama pernah tertimpa, karena itu run ulang memakai prefix `R1_t32e0ff8b_` dan seluruh angka di dokumen ini diverifikasi ulang terhadap JSON tersebut (51 cek otomatis, semua angka utama cocok).

---

## 8. VERIFIKASI INDEPENDEN + UJI TAMBAHAN (subagent paralel, run terpisah, prefix `R1_t32e0ff8b_`)

Seluruh bagian di atas ditulis oleh run pertama. Bagian ini = **run ulang independen** oleh subagent kedua dengan skrip terpisah (`v6_r1_tests*.py`, `v6_r1_t7b.py`, `v6_r1_tests6–9.py`) yang tujuannya mengulang angka kunci dan menutup 3 item "belum dicek" di §7. Hasil mentah: `R1_t32e0ff8b_results_v2.json`, `R1_t32e0ff8b_results_v3.json`, `R1_t32e0ff8b_t7b_cv.json`, `v6_r1_test_results_v6_multowell.json`, `…_v7.json`, `…_v8_buckling.json`, `…_v9_usrop_taxonomy.json` (semua di `scratch/v6_r1_evidence/`).

### 8.1 Angka kunci: konfirmasi silang (2 run, skrip berbeda → hasil identik)

| Angka | Run pertama (§2–§4) | Run independen | Status |
|---|---|---|---|
| Teale MSE selisih median vs kolom tersimpan | 4,98e-05 | **4,9753900170962275e-05** | identik |
| Populasi label 3 kelas USROP | 49.732 / 15.183 / 134.013 | **49.732 / 15.183 / 134.013**, kecocokan 100% | identik |
| F-14 taksonomi (torsi / moderate SS / shock / whirl / stuck / hydraulic) | 82.530 / 320 / 180 / 714 / 394 / 58.317 | **identik** (jendela 60 sampel vs 180 s — kedua metode memberi populasi yang sama besar) | identik |
| `WHIRL_RT` vs `BOUNCE_RT` di 19 file mentah | 18.147 baris, 100% sama | **identik** (scan ulang, hasil sama) | konfirmasi bug |

### 8.2 Penutup gap §7.1 — SSI multi-sumur (6 wellbore, 2 metrik)

Jendela 60 sampel (±4 menit), baris pengeboran RPM>0 & SWOB>0; kelas mengikuti grading Liu 2025 (§2.1 no.3).

| Sumur | Window SSI permukaan | Moderate 1–3 | Severe ≥3 | Window SSI RPM collar MWD | Moderate | Severe |
|---|---|---|---|---|---|---|
| F-14 | 156.290 | 602 | 6 | 22.976 | 1.005 | 38 |
| F-5 | 124.586 | 656 (0,53%) | **40** | 44.598 | 940 | **120** |
| F-9 | 26.521 | 161 (0,61%) | **17** | 9.733 | 113 | 0 |
| F-15_S | 239.282 | 778 (0,33%) | **23** | 135.526 | 464 | **67** |
| F-15A | 126.281 | 245 (0,19%) | **17** | 49.390 | 262 | **9** |
| F-7 | 43.908 | 832 (1,89%) | **24** | 2.683 | 156 | 0 |

(Jendela permukaan dihitung pada baris pengeboran; kolom MWD memakai `CRPM_RT` (RPM collar MWD, non-null terbatas). Angka per-sumur = `v6_r1_test_results_v6_multowell.json`; F-14 dari run `v6_r1_tests2.py`.)

→ **Koreksi terhadap §4.4:** kelas severe stick-slip (SSI≥3) **bukan nol secara umum** — nol hanya di F-14 permukaan. F-5 punya 40 window permukaan dan 120 window MWD; F-15_S 23 dan 67. **Populasi kelas ke-3/ke-4 (moderate & severe stick-slip) tersedia lintas sumur** — persis yang diminta untuk klaim ">3 jenis".

### 8.3 Penutup gap §7.2 — kelas keempat di USROP: anomali hidraulik (sudah dihitung)

Residual `SPPA` vs `Mud Flow In` (bin per well, median + MAD z-score) di 198.928 baris USROP:

- |z| > 2: **28.046 baris (14,10%)** · |z| > 3: **21.343 baris (10,73%)**

→ Taksonomi USROP final = **4 kelas berpenduduk**: `high_MSE_bit_wear` 49.732 · `low_ROP_efficiency` 15.183 · torsional-CV 49.629 · **hidraulik 28.046** (baris 4 tabel §4.2 kini terisi).

### 8.4 Uji tambahan 1 — threshold risiko Crossformer TANPA model terlatih (negatif, penting)

Prediktor persistence (x̂_{t+τ} = x_t, τ=30), W_v = μ+2σ dihitung dari 25% data awal sebagai "jendela normal", pada 4 dataset TSPP asli (paper yang sama):

| Dataset | W_v | % baris alarm | Alarm tahan-terakhir sebelum stuck | Alarm di 60 menit terakhir |
|---|---|---|---|---|
| TSPP2 (stuck 16:59) | 343,6 | 9,04% | 128 menit | **0** |
| TSPP3 (stuck 07:28) | 409,7 | 1,49% | 84,8 menit | **0** |
| TSPP1 (kontrol, tanpa stuck) | 140,9 | 0,69% | tetap menghasilkan "warning" 494 menit | 0 |
| TSPP4 (stuck mendadak) | 2333,0 | 2,38% | 82,6 menit | 0 |

→ **Rumus threshold-nya jalan, tetapi tanpa model foremulti-step terlatih ia TIDAK diskriminatif** (kontrol negatif juga "warning"). Ini menegaskan rekomendasi §2.3 no.2: AE/Crossformer **harus dilatih**, substitusi murah tidak cukup — dan sekaligus menjelaskan kenapa artefak AE lama (`V2_TSPP_AE_SCORES.csv`, 75–99% baris terdeteksi) tidak berguna.

### 8.5 Uji tambahan 2 — buckling helikal kritis (rumus Paslay & Bogy; diuji dengan asumsi eksplisit)

`F_cr = 2·√(E·I·q)`, asumsi DP 5" (OD 127 mm, ID 108,6 mm), E = 210 GPa, lumpur 1,30 g/cm³ → **F_cr = 3,37 kkgf** (stabil: 3,3–3,4 kkgf untuk lumpur 1,2–1,4).

- Di F-14: **123.216 / 156.329 baris pengeboran (78,8%)** punya SWOB ≥ F_cr; median SWOB 5,66, p95 12,61, maksimum 85,47 kkgf.

→ **Hasil jujur: dengan parameter string yang diasumsikan, kelas "buckling risk" menandai 79% baris → TIDAK layak sebagai kelas**. Ini memvalidasi keputusan §4.1 no.5 untuk tidak memakai rumus buckling di Volve: butuh data string/BHA riil (dia. drill pipe per run, ECD, sudut) — parameter itu memang tidak ada di USROP/WITSML.

### 8.6 Konsekuensi untuk kartu berikutnya

1. Taksonomi final yang diajukan ke DPR: **7 kelas** (tabel §4.2) + 4 kelas USROP (§8.3) + kelas severe-stick-slip lintas sumur (§8.2) = **8–9 kelas dengan populasi terhitung**.
2. Jalur anomaly (AE/Crossformer) tetap direkomendasikan, tetapi **wajib dengan model terlatih** (§8.4).
3. Buckling & differential-sticking `F=μ·A·ΔP` **tidak dipakai** sebagai kelas di Volve (parameter tidak tersedia; buckling sudah terbukti non-diskriminatif pada §8.5).

---

## 9. DATA TIDAK LANGSUNG — besaran yang tidak tertulis tapi bisa diturunkan (brief tambahan operator)

> Prinsip operator: *besaran bisa "ada" tanpa ada kolomnya* (arus listrik = tegangan ÷ hambatan). R&D wajib mengecek apakah hambatan engineer sebenarnya punya solusi lewat turunan. Bagian ini menguji 6 turunan di data Volve nyata. Hasil mentah: `v6_r1_indirect_i1_i5.json`, `v6_r1_indirect_i6_i8.json`, `v6_r1_indirect_i9_ucs.json`, `v6_r1_indirect_gt_audit.json` (semua di `scratch/v6_r1_evidence/`).

### 9.1 Peta besaran tidak langsung

| # | Besaran yang "tidak ada" | Diturunkan dari | Sumber rumus |
|---|---|---|---|
| I1 | TOB (torsi di bit) | SPP saat drilling − SPP off-bottom pada flow bin sama | Menand & Mills Eq.3–4 |
| I4/I6 | ECD | MW_in + ΔP_annular/(g·TVD) | rumus hidraulik standar |
| I5 | RPM downhole | RPM surface (proxy transfer rotasi) | — |
| I7 | Drag/overpull | HKLD ÷ berat terapung string | Johancsik et al. 1984 |
| I8 | CCS/kekuatan batuan (in-situ) | amplop minimum MSE per sumur (rolling P10) | Dupriest & Koederitz 2005; Pessier & Fear 1992 |
| I9 | UCS batuan | porositas dari RHOB (LAS) → korelasi empirik | Horsrud 2001 / Rzhevsky & Novick 1971 / Chang et al. 2006 |

### 9.2 Hasil uji (F-14 WITSML 1.648.026 baris + USROP 198.928 baris + LAS F-15 D 45.391 sampel)

**I1 — TOB dari ΔP standpipe: GAGAL divalidasi (negatif jujur).**
`dP = SPP(drilling) − SPP(off-bottom rotating, bin flow sama)`: 45.881 baris baseline off-bottom tersedia. Terhadap MWD downhole torque (`DTOR_RT`, n overlap 236): Spearman **ρ = 0,002 (p = 0,98)** — nol mutlak. Torsi surface (`TQA`) vs `DTOR_RT` juga nol (ρ = 0,017). Penyebab mekanis: (a) butuh kurva performa motor `TOB = (T_max/P_max)·ΔP` yang tidak ada di Volve; (b) torsi surface bukan TOB di well deviated (friction di string — persis peringatan Menand & Mills). → **TOB tidak bisa diturunkan dari data Volve tanpa spesifikasi motor/BHA.**

**I4/I6 — ECD: hitung jalan, validasi tidak bisa.**
`ECD = MW_in + dP_annular/(g·TVD)`: 312 baris drilling dengan baseline tersedia; ECD proxy median **1,393 g/cm³** vs MW median 1,36 (kenaikan 0,033 = wajar untuk annular loss). Namun overlap dengan kanal terkalibrasi `ECD_ARC_RT` = **0 baris** pada baris drilling (kanal hanya terisi saat off-bottom) → tidak bisa divalidasi silang di F-14. ECD layak sebagai fitur, bukan label tervalidasi.

**I5 — RPM surface → RPM downhole: BERHASIL (turunan paling kuat).**
n = 9.081 baris dengan `CRPM_RT` (MWD collar RPM) non-null. Spearman **ρ = 0,83 (p ≈ 0)**; rasio RPM_mwd/RPM_surface p5/p50/p95 = **0,266 / 0,981 / 1,029**; **71,5% baris dalam ±10% dari 1,0**. → Untuk 71% kasus RPM surface adalah pengganti RPM downhole yang valid; 29% sisanya (rasio jatuh ke 0,27) = periode mud-motor/sliding atau motor melemah → justru bisa jadi **indikator tidak langsung selip motor**.

**I7 — Drag/overpull dari HKLD: metode valid, parameter string meleset.**
`ratio = HKLD / ((1−ρ_m/7,85)·q·L)` pada 3.511 baris off-bottom lifting (BONB=0, HKLD>0, depth>500 m): ratio p5/p50/p95 = **0,90 / 1,81 / 1,86**; 94,7% baris > 1,1. Median 1,81 **terlalu tinggi untuk drag normal** → asumsi q (berat per panjang DP 5") dan panjang string meleset untuk string Volve riil (BHA berat + diameter DP berbeda). Butuh tabel BHA asli — `bhaRun` punya `numStringRun` tapi bukan berat/OD per segmen (sudah diverifikasi V4 §1.6).

**I8 — CCS dari amplop minimum MSE: BERHASIL sebagai baseline relatif.**
Amplop = rolling P10 `MSE_psi` per sumur (window 200 baris; Dupriest: MSE minimum ≈ CCS saat drilling efisien). Median amplop p5/p50/p95 = 3.703 / 80.794 / 439.622 psi. Rasio MSE/CCS_amplop: **94,4% baris ≤ 3** (zona efisien Dupriest) dan **2,14% (4.244 baris) > 6** → kelas inefisiensi/vibrasi/aus kecil tapi berpenduduk, **turunan dari data sendiri, bukan label eksternal**.

**I9 — UCS dari porositas LAS: BERHASIL, dan memvalidasi temuan Menand.**
φ dari RHOB (ρ_ma 2,65): p5/p50/p95 = 0,011/0,194/0,285 (13.592 sampel valid). Tiga korelasi empirik (lewat Chang et al. 2006 sebagai kompilasi):
- Horsrud 2001 (shale Tertiary North Sea, cocok geologi Volve): `UCS = 2,922·φ^(−0,96)` MPa → median **14,13 MPa (2.049 psi)**; 3.963 sampel ≥ 30 MPa (29,2%)
- Rzhevsky & Novick 1971: `UCS = 276·(1−3φ)²` MPa → median 48,4 MPa
- Chang 2006 eq.27: `UCS = 143,8·e^(−6,95φ)` MPa → median 37,4 MPa

**Silang-check penting:** CCS amplop I8 (median 80.794 psi) ÷ UCS Horsrud (2.049 psi) = **rasio 39,4×**. Ini **bukti kuantitatif** bahwa MSE dengan torsi permukaan over-estimate besar (persis klaim Menand & Mills §2.1 no.2). Jika TOB suatu saat berhasil diturunkan (I1), rasio ini akan mendekati 3–5×. → 39,4 menjadi **benchmark audit** untuk mengukur apakah turunan TOB sudah benar.

### 9.3 Audit kanal MWD sebagai patokan (wajib sebelum pakai "kebenaran downhole")

`DWOB_RT`: **33,2% nilai negatif** (p50 3,6 kkgf, min −32,2) → tidak layak jadi patokan WOB downhole. `DTOR_RT`: median −0,12 kN·m, rentang −28,8…24 → median praktis nol, isinya noise/salah kalibrasi. `CRPM_RT`: bersih (n 23.110, 0% negatif) → **hanya RPM downhole yang layak sebagai patokan** di F-14. Konsekuensi: verifikasi "surface vs downhole" untuk torsi memang **tidak bisa dilakukan** di F-14 karena patokannya sendiri rusak — bukan karena metode salah.

### 9.4 Rekomendasi (data tidak langsung)

1. **Pakai sekarang:** I5 (RPM surface sebagai proxy + deteksi selip motor dari deviasi rasio), I8 (baseline MSE/CCS amplop per sumur = fitur "efisiensi relatif"), I9 (UCS/φ dari LAS = fitur geologi per kedalaman).
2. **Satu permintaan data spesifik ke owner** yang membuka tiga turunan sekaligus: tabel BHA/string (berat & OD per segmen, motor rating Tmax/Pmax) → membuka I1 (TOB), I7 (drag terkalibrasi), dan mengubah rasio 39,4× menjadi audit TOB sungguhan. Ini permintaan data, bukan klaim "tidak bisa".
3. **Jangan dijadikan label tervalidasi:** ECD (I6) tanpa kanal terkalibrasi yang overlap.

---

## 10. VERIFIKASI RUN-3 (independen ketiga, 2026-10-10 — pihak ketiga yang tidak menulis §2–§9)

Skrip milik run ini (bukan skrip §8), baca CSV mentah langsung (tanpa pickle, tanpa membaca JSON hasil run sebelumnya): `check_urls.py`, `verify_dois.py`, `independent_recheck.py`, `independent_recheck2.py`, `hydro_check.py`, `tunkiel_doi.py` — disalin ke `scratch/v6_r1_evidence/R1_run3_*` bersama keluaran JSON/log-nya.

### 10.1 Sitasi: 17/17 DOI lolos Crossref, tidak ada yang karangan

Semua DOI di §2.1/§3.1/§4.1 + Daftar Sumber diverifikasi lewat `api.crossref.org/works/{DOI}` (judul + tahun cocok dengan klaim dokumen), termasuk yang saat cek liveness hanya mengembalikan 403 (bot-block penerbit, bukan DOI mati): Teale 1965, Al-Mamoori 2025 MDPI, Saadeldin 2023/2021, Saini 2020 SPE, Liu 2025 SPE-J, Hegde 2019, Mopuri 2022, Tunkiel 2021, Yi 2021, Lai 2015 JPT, Okoli 2019, Zha & Pham 2018, Tsuchihashi 2020, Alsaihati 2022, Ratner Snorkel 2019, Liu Thermal Science 2025 → **OK 17, FAIL 0**.

- **2 URL mati/betulan dicek:** halaman arXiv `2302.11135` (diklaim WITHDRAWN di §2.1) — halaman asli memuat teks *"withdrawn by Andres Hernandez-Matamoros"* dan PDF `/pdf/2302.11135v2` mengembalikan **404** → klaim penarikan **benar**. `aade.org/…AADE-17-NTCE-033…` gagal TLS di satu percobaan (transien; teks penuh paper dipakai lewat ekstrak `hpinc.com` yang tercatat §1.3) — dicatat, bukan dihapus.
- **1 pasangan DOI↔label salah ditemukan & diperbaiki:** Daftar Sumber [7] tertaut ke `10.1016/j.petrol.2020.108128` (judul Crossref: *"Training-while-drilling approach to inclination prediction…"* — paper Tunkiel lain). Paper ROP-benchmarking yang benar = **`10.1016/j.petrol.2020.108069`** (Tunkiel, Sui, Wiktorski 2021), sesuai PDF lokal. Sudah diganti.
- **Ledger `grounded-citations` dibangun ulang run-3** (`scratch/v6_r1_evidence/R1_run3_ledger.json`, 22 entri urut = nomor `[1]`–`[22]` blok Sumber). `sources.py verify` tetap keluar gagal hanya karena blok ini memakai judul `## DAFTAR SUMBER` (bukan format `Sources:` bawaan skrip) dan bukan karena id/url tidak cocok; validasi substantif dilakukan lewat liveness URL + Crossref di atas.

### 10.2 Angka: 34 klaim dihitung ulang dari data mentah

| Blok | Klaim di dokumen | Hasil run-3 | Status |
|---|---|---|---|
| USROP Teale MSE (baris valid, selisih median, korelasi, median, P75, P25) | 198.928 · 4,98e-05 · 0,9999999999989 · 102.631 · 256.600 · 1,604e-05 | identik | **6 PASS** |
| Populasi 3 kelas + kecocokan rule | 49.732 / 15.183 / 134.013 · 100% | identik | **4 PASS** |
| MSE/DS (DOC benar m/h) | n 198.602 · 12.501 / 93.334 / 78.212 / 14.555 | identik (kuantil 0,824/2,318/3,990/6,438/15,557 = `R1_…_results_v3.json`) | **5 PASS** |
| F-14 taksonomi (baris, baris pengeboran, TVI windows/p75/populasi, SSI windows/moderate/severe, SHKRSK, VIBLAT, STUCK, non-null ×3) | 1.648.026 · 156.329 · 330.121 · 0,1224 · 82.530 · 344.396 · 320 · 0 · 180 · 714 · 394 · 21.643 · 2.247 · 5.147 | identik | **14 PASS** |
| F-14 hidraulik `qcut=10` | 299.228 · 58.317 (19,49%) | identik | **3 PASS** |

**Satu-satunya selisih awal & penyebabnya:** recompute pertama run-3 memakai `qcut=20` → 47.359 (bukan 58.317). Dengan metode asli `qcut=10` hasilnya **58.317 persis** → selisih murni pilihan jumlah bin, sudah diberi catatan di §4.2.

### 10.3 Dua cacat dokumen yang ditemukan & sudah diperbaiki di run-3

1. **Baris kuantil §2.2 Uji 3 salah label** — tertulis "0,00023/0,00064/0,0011/0,0018/0,0043 = setelah koreksi satuan DOC", padahal angka itu versi **sebelum** koreksi (DOC dari ROP m/s, masing-masing 3600× terlalu kecil). Kuantil benar = **0,824 / 2,318 / 3,990 / 6,438 / 15,557** (median **3,99**). Populasi tabel (12.501/93.334/78.212/14.555) sudah benar — berasal dari skrip v3 yang bersih; yang salah hanya baris kuantil & implikasi §7.4 (median 0,0011). Keduanya sudah diganti.
2. **Sumber [7] DOI salah** → diperbaiki (lihat §10.1).

**Peringatan artefak:** `scratch/v6_r1_evidence/v6_r1_test_results_v2.json` blok `T5_MSE_DS` memuat versi satuan-salah (9 / 14 / 0 / 198.579; median 0,0011). **Yang benar = `R1_t32e0ff8b_results_v3.json` blok `T5_MSE_DS_FIXED`.** Skrip v2 (`v6_r1_tests_v2.py` baris 15) memakai `ROP_ms/(60·RPM)` untuk DOC — jangan dipakai ulang untuk MSE/DS.

### 10.4 Kesimpulan run-3

Ketiga verdict §0 **bertahan** setelah penghitungan ulang independen: label turunan terukur (MSE/MSE-DS/LAS), surface cukup untuk stuck & stick-slip (bukan untuk shock/axial), taksonomi ≥6 kelas berpenduduk. Perbaikan run-3 bersifat dokumentasi (label kuantil, 1 DOI, catatan sensitivitas bin) — **tidak ada angka verdict yang berubah**.



## DAFTAR SUMBER (ledger `grounded-citations`; semua DOI diverifikasi ulang via Crossref — run-3, §10.1)

[1] https://doi.org/10.1016/0148-9062(65)90022-7 — Teale 1965 - concept of specific energy in rock drilling
[2] https://www.hpinc.com/wp-content/uploads/2025/08/Use-of-Mechanical-Specific-Energy-Calculation-in-Real-Time-to-Better-Detect-Vibrations-and-Bit-Wear-While-Drilling-AADE-17-NTCE-033_Extract.pdf — Menand & Mills AADE-17-NTCE-033 - MSE vs DS to type dysfunction
[3] https://thermalscience.rs/pdfs/papers-2025/TSCI2502521L.pdf — Liu et al 2025 Thermal Science - SSI stick-slip grading formula
[4] https://doi.org/10.1016/j.petrol.2019.05.021 — Hegde et al 2019 - stick slip severity classification with ML
[5] https://arxiv.org/abs/2503.07440 — Cao et al 2025 - Crossformer early stuck signs on Volve TSPP
[6] https://doi.org/10.3390/app15095042 — Al-Mamoori et al 2025 MDPI - autoencoder stuck pipe on Volve
[7] https://doi.org/10.1016/j.petrol.2020.108069 — Tunkiel, Sui, Wiktorski 2021 - Reference dataset for rate of penetration benchmarking (DOI diverifikasi ulang run-3: entri lama `10.1016/j.petrol.2020.108128` ternyata paper Tunkiel lain, "Training-while-drilling approach to inclination prediction…", jadi diganti. PDF lokal `Reference/Tunkiel et al. 2021 - Reference dataset for rate of penetration benchmarking.pdf` = 108069.)
[8] https://doi.org/10.1038/s41598-023-33411-9 — Saadeldin et al 2023 Sci Rep - 3 vibration types from surface rig data
[9] https://doi.org/10.1115/1.4052794 — Saadeldin et al 2021 JERT - ANN predicts 3 vibration types from 6 surface params
[10] https://doi.org/10.2118/195334-MS — Okoli et al 2019 - downhole vibration estimated from surface only
[11] https://doi.org/10.1190/segam2018-2964198.1 — Zha & Pham 2018 - deep learning downhole vibration from surface data
[12] https://doi.org/10.2118/228303-PA — Liu et al 2025 SPE J - dysfunctions from surface data + bit forensics
[13] https://doi.org/10.2118/200006-MS — Saini et al 2020 - physics-based workflow, 10 dysfunction categories from surface sensors
[14] https://doi.org/10.2118/204063-MS — Yi et al 2021 - dysfunction classifiers, damping before surface
[15] https://doi.org/10.2118/204462-PA — Tsuchihashi et al 2021 - 3D CNN early stuck sign
[16] https://doi.org/10.1016/j.petrol.2021.109489 — Mopuri et al 2022 - unsupervised AE early stuck sign
[17] https://doi.org/10.2118/209575-PA — Alsaihati & Alotaibi 2022 - vibration severity surface+downhole
[18] https://arxiv.org/abs/2605.00060 — TADI 2026 - tool-augmented drilling intelligence
[19] https://doi.org/10.1007/s00778-019-00552-1 — Ratner et al - Snorkel weak supervision
[20] https://arxiv.org/abs/2302.11135 — Hernandez-Matamoros 2023 - WITHDRAWN semi-supervised stuck
[21] https://www.drillingformulas.com/differential-sticking-causes-stuck-pipe — Differential sticking force formula
[22] https://www.aade.org/application/files/9715/7132/0378/AADE-19-NTCE-080_-_Menand.pdf — Menand AADE-19-NTCE-080 - critical buckling load
