# V10-R1 — BAB ALASAN PEMILIHAN ENGINE (KENAPA METODE INI DIPILIH, PER KELAS)

Task: `t_9cbb587e` [R&D] V10-R1 · Papan: `capstone-v10-proposal` · Tanggal: 2026-10-14 (WIB)
Peran: **PENERUS [R&D] V9-R1** (kartu induk `t_5c5c77e8`) — bab "Alasan Pemilihan Engine"
untuk proposal V10. Draf awal disusun konsultan V10 (`t_4c49de9c`, papan `capstone-v9-build`);
pada kartu ini draf **direview**: setiap angka dicocokkan ke dokumen/JSON sumber, kebahasaan
dipoles ke nada proposal, dan keluhan operator (a)–(f) dipastikan tertutup.
Sumbu: `docs/V9_PM1_ARCHITECTURE.md` (§2 spesifikasi 7 engine, §3 kontrak S1–S9) ·
`docs/V9_R1_JUSTIFICATION.md` (rumus + sitasi + baseline) · kampanye eksekusi V9
(`V9_E_ML_ENGINE.md`, `V9_E_STAT_ENGINE.md`, `V9_E_RULE_ENGINE.md`, `V9_EVAL_A/B/C`,
`V9_I1_INTEGRATION.md`) · profil kemampuan V8 (`V8_E_*_CAPABILITY.md`, `V8_M1_CAPABILITY_MAP.md`).
Kerangka penilaian: standar 3 lapisan A/B/C operator ("Evaluasi User.txt") — **bukan** gate
lift 1,5 tunggal.

> **Riset pendahuluan: `scientific-critical-thinking`** — tiap klaim alasan dipisah
> OBSERVED (angka eksekusi JSON/kampanye V9) vs DESAIN (keputusan arsitektur PM) vs
> BELUM-TERUKUR; hipotesis "metode dipakai di luar tugasnya" diuji balik per engine dan
> **0 kasus salah-framing** ditemukan; kesalahan kutipan rumus Teale di spesifikasi PM
> diangkat terbuka (§10-C1 R1), bukan disembunyikan.
> **Riset pendahuluan: `verification-mandatory`** — setiap alasan dipilih ditautkan ke
> dokumen/JSON primer yang benar-benar dibaca sesi ini; 27 sumber R1 telah diverifikasi
> (OpenAlex/Crossref/doi.org/liveness, 0 karangan); angka V9 dikutip dengan penyebut
> (fold/well) dan dinyatakan bila belum terukur.
> **Riset pendahuluan: `statistical-analysis`** — baseline dinilai **kesesuaian-tugas**-nya
> (deteksi status vs prediksi onset vs klasifikasi lintas-alat butuh baseline berbeda);
> tidak ada baseline universal; AUPRC/lift tidak dirata-ratakan antar kelas (plafon lift
> beda: ssi 15–196, bit_wear 1,84, tool_wear 2,0); FAR dilaporkan pada skala aslinya;
> fold <30 positif = UNDERPOWERED dilabeli, tidak dihitung mayoritas.
> **Riset pendahuluan: `what-if-oracle`** — 5 cabang risiko pemilihan metode (Ω/α/Δ/Ψ/Φ)
> + tripwire §7; kunci: cabang Δ ("pasang ML di semua kelas") ditolak berdasar angka
> D-A5 & FAR, bukan opini.
> **Riset pendahuluan: `consciousness-council`** — 5 arketipe menekan bab ini; ketegangan
> "ML harus dipakai di mana-mana" vs "rule/persistence sudah cukup" direkonsiliasi dengan
> prinsip operator: ML = satu komponen bila memberi nilai tambah.
> **Riset pendahuluan: `sequentialthinking`** (5 pikiran, tool_call sequ-mcp): inventaris
> alasan per engine → peta fisika-kegagalan↔sensor → uji keputusan metode vs bukti V9 →
> pemetaan sitasi per rumus → susun bab + acceptance.
> **Riset pendahuluan: `literature-review`** — sintesis dikelompokkan per engine (bukan
> ringkasan per-paper); 27 sumber dari ledger R1 dipakai ulang tanpa menambah klaim baru.
> **Riset pendahuluan: `hypothesis-generation`** — interpretasi "Fisher & Pearson literal"
> diperlakukan sebagai 3 hipotesis kompetitif (H1 Pearson-r+Fisher-z DIPILIH; H2 Fisher-exact
> ditolak; H3 Fisher-information ditolak) — lihat §3.5 & §4.5 R1.
> **Riset pendahuluan: `grounded-citations`** — setiap rumus ditautkan ke nomor ledger [1]–[27]
> yang sama dengan `docs/V9_R1_JUSTIFICATION.md` §11 (bukan diketik ulang dari ingatan).
> **Riset pendahuluan: agentmemory** — fakta tahan-lama: bab alasan = turunan langsung R1
> (§3.1–3.7) + kampanye V9; 0 angka baru.

---

## 0. RINGKASAN SATU PARAGRAF (untuk bab proposal)

Alat PdM ini menangani **7 kelas kegagalan BHA**. Untuk **setiap kelas, metode dipilih dari
fisika kegagalan kelas itu**, bukan dari selera: sensor yang benar-benar membawa tanda
kerusakan dijadikan **label**, dan metode (rule / persistence / statistik / ML / hibrida)
dipilih menurut **bukti empiris** yang mengukur apakah ia menambah nilai di atas baseline
yang relevan untuk tugas itu. Hasil kampanye V9 tegas dan jujur: **ML menang di kelas dengan
sinyal fitur nyata (vib ΔB>0 vs canary 4/4; ssi RF≥canary 5/7; shk RF≥persistence B1 9/9)**,
sementara di kelas yang didominasi kontinuitas status, **persistence/rule justru menang
(hyd-K-i ΔB RF−persistence negatif 7/7; bit_wear persistence menang 4/4)** — dan di kelas
itu ML **dilarang** (D-A5). Tidak ada satu metode yang dipaksakan ke semua kelas, karena
**tidak ada baseline universal** (Evaluasi User.txt, prinsip 1–6).

---

## 1. PRINSIP PEMILIHAN (mengapa tidak ada "satu metode untuk semua")

Empat aturan mengikat yang memandu seluruh pemilihan (sumber: `Evaluasi User.txt` +
`V9_PM1_ARCHITECTURE.md` §1.2 + `V9_R1_JUSTIFICATION.md` §2 & §4.1):

1. **Bedakan jenis tugas lebih dulu, baru pilih metode.** Deteksi kondisi (status sekarang)
   ≠ deteksi anomali ≠ prediksi onset (kejadian mendatang) ≠ klasifikasi lintas-alat. Peta
   metode↔tugas R1 §2 menghasilkan **0 kasus salah-framing** (ML prediksi tidak dipakai
   untuk tugas deteksi kondisi; kelas status memakai margin B4, kelas onset memakai B1/TLead).
2. **Baseline per tugas, bukan baseline universal.** Persistence menjawab "apakah ML
   mengalahkan korelasi waktu?"; canary-kedalaman menjawab "apakah model cuma mengingat
   posisi?"; prevalence-random menjawab "apakah lift terbaca benar untuk kelas langka?";
   rule/display menjawab "apakah alat mengungguli sistem hari-ini?". Tiap baseline menutup
   ancaman validitas yang **berbeda**.
3. **ML hanya bila memberi nilai tambah terukur (ΔB>0).** Bila ML merugikan kelas itu, ML
   **dilarang** (contoh hyd-K-i). Ini keputusan empiris, bukan dogma anti-ML.
4. **Kejujuran label.** Kanal pembentuk label **dilarang** jadi fitur (anti-sirkular); kelas
   tanpa angka (bit_wear K-2) dilarang dipakai di tingkat apa pun sampai kampanye berangka.

Tabel ringkas "tugas → metode yang menang → bukti V9" (detail per engine §2–§3):

| Kelas | Jenis tugas | Metode terpilih | Bukti empiris V9 (kunci) |
|---|---|---|---|
| vib | deteksi kondisi | rule + persistence + **RF (penambah)** | RF ΔB vs canary 4/4; vs persistence 2/4 |
| ssi | deteksi kondisi | rule definisi + **RF** | RF≥canary 5/7; persistence kalah (0/5 V8) |
| bit_wear | K-1 status · K-2 onset | **persistence** (K-1) · RF-onset (K-2, belum jalan) | persistence menang 4/4 vs RF |
| stuck | K-i status · K-ii onset | persistence (K-i) · **4 engine setara** (K-ii) | persistence-horizon dominan (hindsight); E3 ranking |
| hyd | K-i status · K-ii prediksi | **persistence** (K-i, RF DILARANG) · RF+aliran (K-ii) | ΔB RF−pers negatif 7/7 (D-A5) |
| shk | deteksi anomali | rule (display) + **RF (onset)** | RF≥persistence B1 9/9; rule FAR≤6 7/9 |
| tool_wear | K-i regime · K-ii lintas-alat | **change-point** (K-i) · RF LOTO (K-ii) | cp 8/8; FAR-terkalibrasi deteksi 4/4 |

---

## 2. ALASAN PER ENGINE: FISIKA KEGAGALAN → SENSOR RELEVAN → METODE

Format tiap sub-bab: **(i)** fisika kegagalan kelas; **(ii)** mengapa sensor X relevan
(mengapa kanal itu pembawa tanda); **(iii)** mengapa metode Y (rule/persistence/statistik/ML/
hibrida) dipilih; **(iv)** bukti empiris V9; **(v)** batas.

### 2.1 `vib` — getaran lateral (whirl/GET tinggi)

- **Fisika kegagalan.** Getaran lateral (whirl) terjadi saat BHA berputar tak seimbang di
  lubang — energi mekanik muncul sebagai getaran samping pada rangkaian bor. Kerusakan yang
  mengancam: kelelahan BHA, lepasnya komponen, dan penurunan efisiensi pengeboran.
- **Mengapa sensor `VIBLAT_RT` relevan.** Kanal MWD `VIBLAT_RT` (ft/s²) adalah **instrumen
  downhole** yang langsung mengukur getaran lateral di dekat bit/BHA — jadi ia adalah sumber
  label paling dekat-fisika, bukan turunan. Ambang operasional rig `≥ 32,17405 ft/s²`
  adalah definisi yang sudah ada di lapangan (DESAIN PM, diturunkan dari populasi 714 baris
  F-14, `V6_R1` §4.2). Kanal duplikat `WHIRL_RT`/`BOUNCE_RT` **dilarang total** (identik
  row-level, bug data Volve `V6_R1` §4.3) → label diambil dari `VIBLAT_RT` saja.
- **Mengapa rule + persistence + RF (hibrida).** Tiga alasan berbeda untuk tiga lapisan:
  (a) **rule ambang-absolut** = "sistem hari-ini", tolok ukur apa yang sudah bisa dilakukan
  tanpa ML; (b) **persistence** `ŷ(t)=y(t−1)` = pembanding wajib korelasi temporal [13][14];
  (c) **RF** = penambah nilai peringatan, karena getaran lateral punya struktur lintas-kanal
  (aliran/beban/posisi) yang tak ditangkap ambang tunggal. Preseden klasifikasi dysfungsi
  dari data surface: Saini 2020 [23] (10 kelas dari sensor surface), Liu 2025 [24].
- **Bukti empiris V9.** RF AUPRC 0,4405–0,9117 (spread 0,4712, 4 fold LOWO); **ΔB>0 vs
  canary-kedalaman 4/4** (model tidak sekadar "mengingat posisi"); **vs persistence 2/4**
  (F-14 +0,119; F-15A +0,015; F-15_S −0,018; F-5 −0,227) — persistence menang di sumur
  ber-blok-panjang; rule-display P 0,87–0,95 stabil 1,1× antar-well; SHAP top = TFLO/HKLD/
  depth (bukan hanya kedalaman). Reproduksi silang: lift 1,61/2,36/3,50/1,63 **cocok persis**
  dengan V8-E_vib → kontrol validitas pipeline.
- **Batas.** Jangan klaim lead-time menit; FAR τ0,5 menyebar 119× antar-well → ambang global
  dilarang, wajib kalibrasi per-well (D-A4). Kecukupan surface untuk getaran aksial/lateral
  lemah (univariat AUC ≈0,54, `V6_R1` §3.3) → RF = "skor penambah", bukan detektor tunggal.

### 2.2 `ssi` — stick-slip torsional

- **Fisika kegagalan.** Stick-slip torsional terjadi saat bit "menempel" lalu terlepas
  berulang: RPM berayun keras (min→max) dalam waktu singkat. Ini merusak bit, BHA, dan
  sambungan (torsional fatigue).
- **Mengapa sensor `CRPM_RT` relevan.** Stick-slip adalah fenomena **rotasi**, maka kanal
  RPM collar (`CRPM_RT`) adalah besaran fisik yang persis mendefinisikannya. Label diambil
  dari **rumus baku**, bukan ambang tebakan: `SSI = (max − min)/(2·mean)` atas jendela CRPM
  ≥10 sampel, label 1 bila `SSI ≥ 1` — rumus + grading persis dari Liu et al. 2025
  *Thermal Science* [3]; klasifikasi severity SSI dengan ML sudah mapan (Hegde 2019 [4]).
- **Mengapa rule definisi + RF.** (a) **rule definisi SSI≥1** = detektor paling langsung
  (nol pelatihan, definisi kanal = sistem hari-ini); (b) **RF** = penambah nilai ranking
  karena SSI antar-menit tidak persisten (jarak antar-grid besar) → status-sebelumnya lemah,
  sehingga struktur lintas-kanal (TFLO/SPPA/BPOS) memberi informasi tambahan.
- **Bukti empiris V9.** RF AUPRC 0,0151–0,4589; **RF≥canary 5/7 fold layak**; **vs persistence
  6/7 fold layak**; V8 mencatat persistence kalah 0/5 vs RF. Bukaan baru: fold eksternal
  F-9_A (55 positif) RF 0,1357 vs prev 0,0654 = lift 2,07 → RF bekerja di fold eksternal.
  Hibrida `rule AND persistence` **memangkas FP 26→7 (−73,1% total)**; tak memburuk di 7/7 fold
  layak (memotong di 6/7; F-14 tie 0→0) tanpa menambah FN material.
- **Batas.** 5/9 fold CI95 menyentuh no-skill → label keyakinan wajib tampil; nodata CRPM
  62,3% (F-14 96,6%) = keterbatasan sensor terukur, bukan murni model. Rule tetap layer dasar.

### 2.3 `bit_wear` — keausan/balling (K-1 status · K-2 onset)

- **Fisika kegagalan.** Bit aus/balling menurunkan efisiensi pemotongan: untuk WOB/ROP yang
  sama dibutuhkan energi mekanik spesifik lebih besar. Inefisiensi MSE tinggi = tanda bit
  tidak lagi memotong efektif.
- **Mengapa sensor WOB/ROP/RPM/TORQ relevan.** Energi Mekanik Spesifik dihitung langsung dari
  4 sensor surface yang sudah ada — **tidak butuh sensor baru**:
  `MSE = WOB/A + (120·π·N·T)/(A·ROP)` (field units), Teale 1965 [1]; tipologi MSE vs MSE/DS
  (vibrasi vs keausan vs balling) dari Menand & Mills [2] via `DS = WOB/(R·DOC)`,
  `DOC = ROP/(60·RPM)`. Kolom MSE USROP sudah diverifikasi independen (recompute selisih
  median 0,005%, korelasi log10 0,9999999999989, `V6_R1` §2.2).
- **Mengapa persistence (K-1) — bukan RF.** Label `high_MSE` membentuk **blok kontigu pada
  sumbu kedalaman**; konsekuensinya `y(t−1)` sudah membawa hampir seluruh sinyal, sehingga
  rule sederhana "status jendela sebelumnya" adalah engine status terbaik **terukur**.
  ML **kalah**: RF tidak menambah di atas persistence di **4/4 fold** (ΔB −0,087…−0,381).
  Ini bukan kegagalan ML, melainkan sifat tugas status — karenanya fokus nilai dipindah ke
  K-2 onset (peringatan dini), yang dirancang RF-onset + tes pembeda persistence-onset.
- **Bukti empiris V9.** persistence AUPRC **0,679–0,984** (4/4 fold menang vs RF); RF menang
  vs canary-kedalaman 4/4 (ΔB +0,058…+0,107) → fitur non-kedalaman tetap membawa sinyal, tapi
  bukan di atas persistence; reproduksi angka V6 identik digit. K-2: **nol angka** (kampanye
  pra-reg belum jalan) — 481/329 kandidat onset terverifikasi.
- **Batas.** Label = kuantil internal (P75) → K-1 terdeteksi ≠ bit rusak (hanya "zona
  inefisiensi MSE"); P/R/FAR K-1 **belum terukur**; dataset USROP ≠ rig Volve.

### 2.4 `stuck` — pipa terjepit (K-i status · K-ii onset)

- **Fisika kegagalan.** Pipa terjepit terjadi saat rangkaian bor tak bisa bergerak: torsi
  (TQA) naik, hookload (HKLD) berubah drastis, dan ROP jatuh — tanda mekanis yang khas.
- **Mengapa sensor TQA/HKLD/ROP relevan.** Ketiganya adalah besaran mekanis inti pipa
  terjepit; aturan **2-dari-3** (`z(TQA)>2`, `z(HKLD)>2`, ROP-drop ≥30%) menekan false-positive
  kanal tunggal. Skor-z memakai statistik robust median/MAD [7][8][9]. Preseden: deteksi dini
  stuck dari data surface Volve dengan Crossformer (peringatan **2,67–7,37 menit**) [19],
  autoencoder hanya-data-normal (AUC 0,958 di Volve) [20], LSTM-AE unsupervised [21].
- **Mengapa 4 engine setara-tugas (E0/E1/E2/E3) + persistence-onset sebagai tes pembeda.**
  K-ii = prediksi kejadian mendatang, maka wajar memakai skor-ranking + ambang pra-reg:
  **E0 persistence** (tes kejujuran), **E1 rule** (2-dari-3), **E2 statistik** (z+z+ROP-drop,
  q95-train), **E3 RF** (ranking). Persistence-onset dijadikan **tes pembeda**: bila ≥ RF
  mayoritas → hipotesis "kegagalan V9 = formulasi status" DITOLAK.
- **Bukti empiris V9 (temuan penting).** Persistence-**horizon** AUPRC 0,827–0,902 (B1 93–97%)
  **mendominasi** semua detektor — TAPI ini **HINDSIGHT** (label positif = run 10 menit kontigu,
  `y(t−1)=1` hampir selalu benar di dalam run) → dipakai sebagai **batas-atas teori**, bukan
  pembanding fair. Persistence-**event** (deployable) ≈ prevalence; E1 ≈ prevalence; E2 CI
  memuat prev **4/4** (tidak terbukti); E3 RF lift >1 4/4, signifikan 1/4. Kesimpulan jujur:
  yang didominasi adalah **struktur label**, bukan ketiadaan ML.
- **Batas.** FAR 9,9–1.440/24jam; B1 maks 31,8% (<80%); kontrol-positif kejadian nyata 0/10;
  semantik skala STUCK_RT 0/1/2/3 beda antar-well (F-10 didominasi "3", F-14 "1") = risiko
  pra-reg Fase 0. Hanya 2 fold K-i terukur.

### 2.5 `hyd` — anomali hidrolik (K-i status · K-ii prediksi)

- **Fisika kegagalan.** Anomali hidrolik = ketidakseimbangan tekanan aliran lumpur terhadap
  laju alir yang diharapkan (mis. gain/loss). Ini prekursor kick/loss (masalah well-control).
- **Mengapa sensor `SPPA` (residu thd `TFLO`) relevan.** Tekanan pompa (SPPA) bergantung pada
  laju alir (TFLO); anomali = **residu** SPPA terhadap median-nya pada bin TFLO yang sama.
  Label = `z = 0,6745·(SPPA − median_bin)/MAD_bin` atas `qcut(TFLO, 10)`, status `|z|>2`
  [7][8][9]. Untuk K-ii (kick/loss proxy), label dibangun dari **perubahan volume pit**
  `ΔV_pit` — praktik mapan deteksi influx (IDAPS/SPE [17]; kick early detection [18]).
- **Mengapa persistence di K-i dan RF DILARANG (D-A5).** Ini keputusan **empiris paling
  tegas** di portofolio: label K-i = z dari kanal yang sama → status membentuk blok persisten,
  sehingga `ŷ(t)=y(t−1)` adalah engine terbaik. RF **tidak menambah** — **ΔB RF−persistence
  negatif di 7/7 fold** (−0,010…−0,400), CI non-tumpang 6/7 → RF **DILARANG** di kelas ini
  (D-A5). Untuk K-ii, RF dipakai **bersama fitur aliran (mass-balance)** karena sinyal
  kick/loss memang lintas-kanal.
- **Bukti empiris V9.** K-i persistence P 0,615–0,793, delay median 0–3,5 mnt, FAR_t
  32–111/24jam (beban blok, bukan alarm); **hibrida rule AND persistence memangkas FP
  2091→927 (−55,7%) konsisten 9/9 well** — hibrida non-degenerasi paling kuat di portofolio;
  CI persistence memuat prev **0/9** (satu-satunya kelas rig bersih). K-ii: RF+flow AUPRC
  0,228 vs konservatif 0,030 (fitur aliran = syarat sinyal).
- **Batas.** K-i label = PROXY (residu SPPA); FAR 14,6–58,4 >6 di 9/9 → belum alarm; K-ii
  literal Fisher/Pearson **tidak bisa dijalankan** — `FlowOut` tidak ada di F-9A (bukti:
  4 kanal flow saling berkorelasi r=0,995–1,000 = semuanya aliran masuk); varian proxy 0 TP
  @q95, sign-flip 78,7% jendela; 1 wellbore.

### 2.6 `shk` — bit bounce / shock risk

- **Fisika kegagalan.** Bit bounce (aksial) = bit memantul naik-turun saat mengebor, memberi
  beban kejut pada bit dan BHA — sumber kerusakan aksial dan kelelahan.
- **Mengapa sensor `SHKRSK_RT` relevan.** Kanal MWD `SHKRSK_RT` (skala risiko 0–3) adalah
  display shock-risk downhole yang langsung menandai kejutan; label `≥1`. Karena surface
  **tidak cukup** untuk shock (AUC surface 0,80–0,82, `V6_R1` §3.3 — dikonfirmasi peringatan
  Yi 2021/Hess 2023), kelas ini memang terikat ketersediaan kanal MWD.
- **Mengapa RF + persistence (hibrida).** Untuk **status**, RF dipakai bersama persistence;
  tetapi nilai tambah ML yang **terukur** ada di **sub-tugas onset**: RF≥persistence untuk
  B1 di **9/9 fold** (TLead median 5,0 mnt) → ML menambah nilai peringatan dini di atas
  "status kemarin", meski AUPRC statusnya sering kalah dari persistence (blok panjang).
- **Bukti empiris V9.** RF AUPRC 0,0069–0,1929; ΔB vs canary 5/9; rule-display FAR 0,67–6,6
  → **satu-satunya kelas rig dengan mayoritas fold lolos FAR≤6 (7/9 well)** tanpa kalibrasi;
  FAR≤1 dengan recall>0 = **0/9** (tidak ada di kurva); B3 negatif (engine menambah beban cek
  di tau rendah); fold eksternal F-10/F-12 lift ≈1 → sinyal lokal-wellbore.
- **Batas.** Kalibrasi lintas-well dilarang (D-A4); severity-mix beda antar-well (F-12 66%
  ≥2 vs F-14 40%); non-null SHKRSK_RT hanya 0,7–8% baris.

### 2.7 `tool_wear` — keausan mata bor (bengkel: K-i regime · K-ii lintas-alat)

- **Fisika kegagalan.** Mata bor aus berubah perilaku getarannya (spektrum, kurtosis, RMS)
  seiring waktu pemakaian. Domain = **bengkel**, skala detik, bukan rig.
- **Mengapa sensor getaran 1000 Hz relevan.** Data bengkel Mendeley `th4yv974r2` (4 alat ×
  2 run, 469 jendela 1 dtk @1000 Hz, 27 fitur getaran: kurt/crest/fdom/rms/skew/p2p/zcr/
  mean/std per sumbu X/Y/Z). Label = **identitas run** (desain dataset, bukan turunan fitur →
  anti-sirkular terpenuhi).
- **Mengapa change-point (K-i) dan RF LOTO (K-ii).** K-i = deteksi **perubahan-regime**
  dalam-run (bukan klasifikasi/prediksi) → statistik change-point: `SSE(τ) = Σ_{t≤τ}(x_t−μ₁)²
  + Σ_{t>τ}(x_t−μ₂)²`, `τ*=argmin_τ SSE(τ)`, signifikansi **permutation test 500×**
  [10][11][12]. K-ii = generalisasi antar-alat (LOTO) → RF klasifikasi + split Leave-One-Tool-Out.
- **Bukti empiris V9.** K-i: tes pembeda artefak termal lolos (t_cp <5 dtk di **0/8** run),
  tetapi **spesifisitas keausan GAGAL** — cp signifikan **8/8 run termasuk 8/8 alat BARU**
  (precision run 0,50) → klaim "onset progresi keausan" terdukung lemah; titik operasi
  FAR-terkalibrasi (≤1 alarm/menit) justru **deteksi 4/4 alat, FP 1–3, TLead 20–36 dtk**
  → layak sebagai **gating inspeksi**, bukan alarm. K-ii: RF AUPRC 0,5433–0,7684, ΔB vs canary
  4/4; canary 3-RMS 0,516–0,612 (reproduksi V8). Persistence **N/A dinyatakan** (label konstan
  dalam run — bukan dihilangkan).
- **Batas.** Precision run 0,50 (bukan "keausan spesifik"); transfer ke rig **TIDAK diklaim**
  (confound urutan-run R02 selalu setelah R01; D-A7: lead detik bengkel ≠ menit rig).

---

## 3. MENGAPA RULE / PERSISTENCE / STATISTIK / ML / HIBRIDA — BUKTI EMPIRIS V9

### 3.1 Peta keputusan metode ↔ bukti (per engine)

| Kelas | Rule | Persistence | Statistik | ML (RF) | Hibrida | Bukti penentu |
|---|---|---|---|---|---|---|
| vib | ✅ dasar (P 0,87–0,95) | ✅ pembanding | — | ✅ **penambah** | ✅ rule+persistence | ΔB vs canary 4/4; vs persistence 2/4 |
| ssi | ✅ definisi SSI≥1 | ✅ (lemah, kalah 0/5 V8) | — | ✅ **penambah** | ✅ (FP −73,1%) | RF≥canary 5/7; hybrid ≤ rule 7/7 |
| bit_wear K-1 | — (label=Teale) | ✅ **engine utama** | — | ❌ (kalah 4/4) | degradasi ke persistence | persistence AUPRC 0,679–0,984 |
| stuck K-i | ✅ display | ✅ | — | ❌ | ✅ | rule P 0,92–0,97 (2 well) |
| stuck K-ii | ✅ E1 | ✅ E0 (tes pembeda) | ✅ E2 | ✅ E3 ranking | — | E3 lift 4/4; persistence-horizon=hindsight |
| hyd K-i | ✅ \|z\| manual | ✅ **engine terbaik** | ✅ (label z) | ❌ **DILARANG (D-A5)** | ✅ (FP −55,7%) | ΔB RF−pers 7/7 negatif |
| hyd K-ii | ✅ z-pit (TLead=0) | — | ✅ Fisher/Pearson | ✅ RF+aliran | ✅ | AUPRC 0,228 (vs konservatif 0,030) |
| shk | ✅ display | ✅ | — | ✅ **onset** | ✅ | RF≥persistence B1 9/9 |
| tool_wear K-i | ✅ 3-RMS | N/A (dinyatakan) | ✅ **change-point** | — | ✅ FAR-terkalibrasi | cp 8/8; precision 0,50 |
| tool_wear K-ii | — | N/A | — | ✅ **LOTO RF** | ✅ | ΔB vs canary 4/4 |

### 3.2 Tiga temuan empiris yang **menentukan** pemilihan metode

1. **Persistence menang di kelas status yang ber-blok-panjang → ML dilarang di sana.**
   Bukti: hyd-K-i ΔB RF−persistence **negatif 7/7** (D-A5); bit_wear persistence menang
   **4/4**. Konsekuensi: RF **dilarang** di hyd-K-i; bit_wear K-1 memakai persistence sebagai
   engine utama. (Mekanisme: label membentuk blok temporal → `y(t−1)` membawa hampir semua
   sinyal.)
2. **ML menang di kelas dengan sinyal fitur lintas-kanal → RF dipakai.**
   Bukti: vib ΔB vs canary **4/4**; ssi RF≥canary **5/7**; shk RF≥persistence B1 **9/9**;
   tool_wear ΔB vs canary **4/4**. Konsekuensi: RF jadi lapisan ranking/peringatan di atas
   rule/persistence — **bukan pengganti**.
3. **Canary-kedalaman wajib ada.** Tanpa kontrol "RF hanya fitur depth/dbtm", model bisa
   tampak hebat karena cuma "mengingat posisi". Bukti nyata: bit_wear SHAP K-1 didominasi
   MD/TVD; stuck E3 RF 0,326–0,331 < canary 0,410 → **G2 gagal**, mengungkap deteksi terbantu
   posisi, bukan proses stuck. Karena itu setiap kampanye ML memasang canary-kedalaman.

### 3.3 Mengapa persistence-horizon ≠ pembanding fair (kejujuran pengukuran)

Pada kelas onset (stuck K-ii), label positif = **run horizon kontigu** (median 10 menit),
sehingga `y(t−1)=1` hampir selalu benar di dalam run → persistence-horizon "mendeteksi"
dengan B1 93–97% tanpa memprediksi apa pun (**hindsight**). Ini dilaporkan sebagai
**batas-atas teori**, bukan prestasi, dan **tidak** dijadikan standar "mengalahkan" yang fair
bagi detektor deployable (pembanding fair = persistence-event & E1, keduanya ≈ prevalence).

---

## 4. SITASI PER RUMUS (dari kumpulan 27 sumber R1, 0 karangan)

| Rumus / metode | Ditulis persis | Sumber (ledger R1) |
|---|---|---|
| MSE Teale | `MSE = WOB/A + (120·π·N·T)/(A·ROP)` (field) · SI `WOB/A + 2π·N_rps·T/(A·ROP)` | **[1]** Teale 1965 |
| MSE/DS, DOC | `DS = WOB/(R·DOC)`, `DOC = ROP/(60·RPM)`; aturan MSE & MSE/DS naik/turun | **[2]** Menand & Mills 2017 |
| SSI stick-slip | `SSI = (max−min)/(2·mean)` jendela CRPM ≥10; grading `<1 / 1–3 / ≥3` | **[3]** Liu et al. 2025 *Thermal Science* |
| Klasifikasi severity SSI via ML | label SSI dari data surface | **[4]** Hegde et al. 2019 |
| Random Forest | bagging + subsampling fitur, ensemble pohon terdekorrelasi | **[5]** Breiman 2001 |
| Justifikasi pilih RF | RF termasuk klasifikator terkuat benchmark dunia-nyata | **[6]** Fernández-Delgado et al. 2014 (JMLR) |
| MAD (median absolute deviation) | definisi MAD | **[7]** NIST/SEMATECH |
| Faktor skala 0,6745 | MAD/0,6745 ≈ σ untuk normal | **[8]** NIST/SEMATECH |
| Median/MAD detektor anomali robust | tahan-outlier | **[9]** Rousseeuw & Hubert 2017 |
| Change-point (survei offline) | SSE/least-squares segmentation family | **[10]** Truong et al. 2020 |
| Optimalitas changepoint (PELT) | konteks pencarian pecahan tunggal + uji valid | **[11]** Killick et al. 2012 |
| Permutation test (bebas distribusi) | `p = (1+#{SSE_perm ≤ SSE_obs})/(1+500)` | **[12]** Good 2000 |
| Persistence naive | `ŷ(t)=y(t−1)` baseline standar deret waktu | **[13]** Hyndman & Athanasopoulos (FPP3) |
| Naive sulit dikalahkan | kompetisi M4 | **[14]** Makridakis et al. 2020 |
| Distribusi korelasi sampel | dasar transformasi r | **[15]** Fisher 1915 |
| Probable error + inferensi r | `z' = atanh(r)`, `SE(z') = 1/√(n−3)` | **[16]** Fisher 1921 (*Metron*) |
| Deteksi influx via volume pit (IDAPS) | kick detection saat pompa berhenti | **[17]** IDAPS 2016 (SPE) |
| Peringatan dini kick (mud-logging) | sinyal dini kick | **[18]** kick early detection 2015 |
| Anchor peringatan stuck (B2) | 2,67–7,37 menit (Crossformer, Volve) | **[19]** Cao et al. 2025 (arXiv) |
| Label tanpa anotasi (AE normal) | AUC 0,958 di Volve | **[20]** Al-Mamoori et al. 2025 |
| LSTM-AE unsupervised | label onset tanpa anotasi manual | **[21]** Mopuri et al. 2022 |
| Kecukupan sensor surface | surface → getaran downhole (R>0,9) | **[22]** Saadeldin et al. 2023 |
| Taksonomi dysfungsi dari surface | physics-based workflow, 10 kelas | **[23]** Saini et al. 2020 |
| Dysfungsi dari surface + forensik bit | alternatif sensor downhole | **[24]** Liu et al. 2025 (SPE J) |
| UCS dari porositas (Horsrud) | `UCS = 2,922·φ^(−0,96)` MPa | **[25]** Horsrud 2001 |
| UCS (Chang) | `UCS = 143,8·e^(−6,95φ)` MPa | **[26]** Chang et al. 2006 |
| Dataset referensi ROP | benchmark pengeboran | **[27]** Tunkiel et al. 2021 |

> **Catatan change-control (§10-C1 R1):** teks rumus Teale di `V9_PM1_ARCHITECTURE.md` §2.3
> baris 201 (`MSE = (WOB/Am) + (480·N·π)/TOR`) **salah dimensi** — rumus benar = bentuk Teale
> di atas; label USROP tidak berubah karena kolom tersimpan terverifikasi Teale. Ini temuan
> nyata, bukan dokumen bebas cacat.

---

## 5. MENJAWAB KELUHAN OPERATOR (khusus poin (c), tautan ke a/b/d/e/f)

- **(c) "kenapa tiap engine dipilih"** → dijawab penuh: §2 (fisika→sensor→metode per engine) +
  §3 (bukti empiris) + §4 (sitasi per rumus). Tiap keputusan metode punya alasan berbukti,
  **0 "karena bagus"**.
- **(a) "7 hal yang dideteksi"** → §2 tiap sub-bab "Fisika kegagalan" + tabel §1 (kolom "Jenis
  tugas"); 7 kelas = vib, ssi, bit_wear, stuck, hyd, shk, tool_wear.
- **(b) "engine mana yang bekerja & bagaimana"** → §2 (i)–(iii) + tabel §3.1 (metode terpilih
  per kelas); detail angka per fold = kampanye V9.
- **(d) "peran data"** → §2 (ii) tiap engine ("mengapa sensor X relevan") + §4 (label turunan
  dari data yang sudah ada).
- **(e) "labeling / statistik / hybrid"** → §3.1 (peta metode) + §3.3 (labeling onset jujur) +
  hibrida `rule AND persistence` (FP −73,1% ssi; −55,7% hyd).
- **(f) "7 vs 11 vs 27"** → 7 = kelas masalah; 11 = klaim/sub-tugas (7 + 4 kelas ber-sub-klaim:
  bit_wear K-1/K-2, stuck K-i/K-ii, hyd K-i/K-ii, tool_wear K-i/K-ii); 27 = head pada registry
  prototipe `v9_i1_pipeline.py` (rule/persistence/hybrid/RF per kelas). Lihat
  `docs/V10_M1_PETA_V8.md` §6 untuk penjelasan tegas angka ini.

---

## 6. WHAT-IF-ORACLE (risiko pemilihan metode — 5 cabang)

| Cabang | Bobot | Skenario | Konsekuensi | Robust action |
|---|---|---|---|---|
| Ω Best | 15% | ML menang semua kelas | — (tidak terjadi) | prinsip tetap: pilih per tugas |
| α Likely | 45% | ML menang di kelas sinyal-nyata, persistence menang di kelas status | **terjadi** (bukti V9) | peta metode §3.1 dipakai apa adanya |
| Δ Worst | 20% | "Pasang ML di semua kelas" dipaksakan | RF hyd-K-i merugikan (ΔB −7/7) | larangan D-A5 (assert di harness) |
| Ψ Wildcard | 10% | Ambang global diklaim portabel | vib FAR menyebar 119× antar-well | kalibrasi per-well (D-A4); badge FAR tampil |
| Φ Contrarian | 10% | Ternyata rule/persistence sudah cukup | alat tetap koheren (L0+L2+L1-terbatas) | 0 alarm otomatis; ML = lapisan ranking |

**Tripwire:** (i) muncul kanal sensor baru (VIBLAT F-4/F-10/F-15, GAINLOSSTOT) → hitung ulang
baseline pada fold baru; (ii) ada tuntutan gate seragam → audit A1; (iii) pra-reg K-2 bit_wear
terbit → jalankan persistence-onset K-2.

---

## 7. BATAS JUJUR / BELUM TERUKUR

1. Angka kampanye V9 (ΔB, lift, FAR, AUPRC) = kutipan JSON/dokumen primer yang dibaca sesi
   ini; **tidak** dihitung ulang di sini (kualitas mengikuti audit A1/PM2 V9).
2. Verifikasi sitasi R1 = metadata (judul/tahun/DOI/URL hidup) — bukan pembacaan teks penuh
   semua paper (kecuali ekstrak Menand + teks Liu *Thermal Science*).
3. "Belum terukur" dipisah tegas dari "gagal": bit_wear K-2, RF tool_wear K-ii versi V9,
   RF hyd K-ii versi V9, P/R/FAR bit_wear K-1, portabilitas stuck K-i (>2 well).
4. Definisi "Fisher & Pearson literal" = interpretasi R1 (H1) — terbuka change-control bila
   PM bermaksud lain.
5. Semua hasil satu lapangan (Volve) + satu dataset bengkel (Mendeley) — generalisasi lintas
   lapangan TIDAK diklaim.
6. **Audit review V10-R1 (sesi ini):** angka draft dicocokkan satu-per-satu ke dokumen/JSON
   sumber dan **semuanya cocok persis** (contoh terverifikasi: vib ΔB pers +0,119/+0,015/−0,018/
   −0,227 = `V9_E_ML` baris 384–385; hyd ΔB −0,010…−0,400 7/7 & FP 2091→927 = `V9_PM1`/`A1`#6;
   tool_wear cp 8/8, precision 0,50, deteksi 4/4, TLead 20–36 dtk = `V9_E_STAT` baris 41;
   stuck canary 0,326–0,331 < 0,410 = `V9_PM1` baris 218). Satu imprecision dikoreksi: klaim
   ssi hibrida "konsisten 7/7" → "tak memburuk 7/7 (memotong 6/7)" sesuai `V9_PM2_VERDICT` §2.
   Angka **tidak** dihitung ulang dari JSON mentah (kualitas mengikuti audit A1/PM2 V9); yang
   dijalankan ulang hanya modul REGISTRY `v9_i1_pipeline.py` (7 engine, 27 head terkonfirmasi).

---

## 8. PENERIMAAN (self-check)

| # | Syarat | Bukti |
|---|---|---|
| a | Tiap keputusan metode punya alasan bukti + sitasi | §2 (per engine) + §3 (bukti V9) + §4 (sitasi per rumus) |
| b | 0 "karena bagus" | setiap pemilihan ditautkan ke angka (ΔB/FAR/AUPRC) atau fisika + sumber |
| c | Konsisten dgn `V9_R1_JUSTIFICATION.md` | rumus + baseline + larangan D-A5 + canary identik dengan R1 §2/§3/§4.1 |
| d | Fisika→sensor per engine | §2 (i)–(ii) 7 kelas lengkap |
| e | Bukti empiris V9 per kasus | §3.2 (3 temuan penentu) + tabel §3.1 |
| f | Baris "Riset pendahuluan" | header (10 skill) |
| g | sequ-mcp ≥3 pikiran | 5 pikiran (tool_call sequ-mcp) |
| h | agentmemory | fakta tahan-lama dicatat |
| i | Angka konsisten dgn sumber (review V10-R1) | tiap angka ditelusuri ke dokumen/JSON primer (V9_E_ML/E_STAT/E_RULE, V9_EVAL_A/B/C, V8_E_*, V9_PM1/PM2); registry `v9_i1_pipeline.py` **dijalankan** (7 engine, 27 head = 4+4+4+6+4+2+3); 1 imprecision ssi (klaim "konsisten 7/7" → "tak memburuk 7/7, memotong 6/7") dikoreksi ke bentuk `V9_PM2_VERDICT.md` §2 |

## Sumber (dibaca langsung sesi ini)

`docs/V9_PM1_ARCHITECTURE.md` (§2 spesifikasi 7 engine, §3 S1–S9) · `docs/V9_R1_JUSTIFICATION.md`
(§3.1–3.7 rumus+baseline, §4.1 tabel baseline, §11 27 sitasi) · `docs/V9_E_ML_ENGINE.md` ·
`docs/V9_E_STAT_ENGINE.md` · `docs/V9_E_RULE_ENGINE.md` · `docs/V9_EVAL_A_LAYERA.md`,
`docs/V9_EVAL_B_LAYERB.md`, `docs/V9_EVAL_C_LAYERC.md` · `docs/V9_I1_INTEGRATION.md`
(§2 registry 27 head) · `docs/V9_PM2_VERDICT.md` (§e tabel tier) · `docs/V9_D1_DATA_PIPELINE.md`
(§3 skema label) · `docs/V8_E_{vib,ssi,bit_wear,stuck,hyd,shk,tool_wear}_CAPABILITY.md` ·
`docs/V8_M1_CAPABILITY_MAP.md` · `docs/V6_R1_SCIENCE.md` (§2–§4 rumus teruji) ·
`code/v9_i1_pipeline.py` (REGISTRY 27 head) · `Evaluasi User.txt`.

*Selesai V10-R1 (`t_9cbb587e`). Dokumen ini = bab "Alasan Pemilihan Engine" pada proposal V10
yang dirakit `V10-ASM` (`t_0720bde5`); draf awal dari konsultan V10 (`t_4c49de9c`) direview:
angka dicocokkan ke dokumen/JSON sumber, satu imprecision ssi dikoreksi, keluhan (a)–(f) ditutup.*
