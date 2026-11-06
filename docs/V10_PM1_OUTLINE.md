# V10-PM1 — KERANGKA PROPOSAL BARU: 7 ENGINE vs 11 KLAIM vs 27 HEAD + OUTLINE + DELEGASI

Task: `t_cf741053` [PM · System Architect · Tech Lead] · Board: `capstone-v10-proposal` · Tanggal: 2026-10-14 (WIB)
Peran: PM + System Architect — menetapkan kerangka proposal teknis V10 berdasar keluhan operator.
Status: **KERANGKA MENGIKAT** untuk 6 bab tim (D1 · R1 · E_ML · E_STAT · E_RULE · EVAL) dan perakitan akhir.
Proposal baru = dokumen V10 terpisah; V9_PM1 tetap arsitektur internal-engine dan tidak diedit.

KELUHAN OPERATOR (2026-10-14, VERBATIM INTI): proposal teknis "jelek, isinya dangkal".
Yang HILANG dan wajib ada: (a) daftar 7 hal yang dideteksi; (b) engine mana yang bekerja &
cara kerjanya; (c) alasan KENAPA tiap engine dipilih (bukti, bukan selera); (d) peran DATA;
(e) labeling ML / statistik / workflow hybrid; (f) penjelasan TEGAS angka 7 vs 11 (dan 27 head).

SUMBER ANGKA (semua dari dokumen/kode/JSON sumber — nol angka karangan):
`code/v9_i1_pipeline.py` (REGISTRY §1, baris 74–287 — **dibaca & DIJALANKAN**, bukan ditranskrip) ·
`docs/V9_PM1_ARCHITECTURE.md` (§2 spesifikasi 7 engine, §3 S1–S9) ·
`docs/V9_PM2_VERDICT.md` §e (tabel tier per klaim) ·
`docs/V8_M1_CAPABILITY_MAP.md` · `docs/V9_EVAL_A/B/C` (EA-1/EB-1/EC-1) · `docs/V9_I1_INTEGRATION.md` §2.

> **Riset pendahuluan: `scientific-critical-thinking`** — tiga angka 7/11/27 dipisah sebagai
> tiga UNIT berbeda (kelas kerusakan vs estimand/tugas vs varian metode terukur), bukan tiga
> label untuk hal yang sama; status "belum dijalankan/tidak tersedia" DIPERTAHANKAN sebagai
> klaim (kejujuran ≠ penghapusan); setiap bab diberi falsifier konsistensi ke REGISTRY kode.
> **Riset pendahuluan: `statistical-analysis`** — unit analisis ditetapkan = **klaim** (11), bukan
> engine (7) maupun head (27); baseline wajib relevan per tugas (deteksi-kondisi vs prediksi-onset
> punya baseline & label berbeda); FAR dibaca pada skala aslinya (rig = jendela/24 jam, bengkel =
> menit); fold UNDERPOWERED (<30 positif) dilabeli, tidak dihitung mayoritas; AUPRC/lift dilarang
> dirata-ratakan antar kelas (plafon lift beda per prevalensi).
> **Riset pendahuluan: `verification-mandatory`** — angka 7/11/27 diperoleh dengan **menjalankan
> modul** `v9_i1_pipeline.py` (IMPORT OK) lalu di-cross-check ke 3 dokumen evaluator (EA-1/EB-1/EC-1)
> dan tabel 11 baris PM2 §e; daftar "belum diverifikasi" ditulis eksplisit di §6.
> **Riset pendahuluan: `sequentialthinking`** (5 pikiran, 5/5 sukses, `sequ-mcp`): inventaris sumber
> & validasi angka → pemisahan tegas 7/11/27 → outline yang menutup (a)–(f) → delegasi per tim →
> gerbang acceptance + falsifier.

---

## 0. RINGKAS (PM1) — jawaban satu paragraf untuk keluhan (f)

Alat PdM advisory yang kami bangun menjawab **7 pertanyaan perbaikan** di sekitar rig/bengkel
(**7 ENGINE** = 7 kelas kerusakan yang dideteksi). Karena sebagian pertanyaan punya dua sisi —
"apakah sedang terjadi sekarang?" dan "apakah akan terjadi beberapa menit lagi?" — jumlah
**klaim tugas** yang kami nilai = **11 KLAIM** (3 engine satu klaim + 4 engine dua klaim;
`3×1 + 4×2 = 11`). Karena tiap klaim kami jawab dengan beberapa **cara** (rule, persistence,
statistik z-score, random forest, hibrida) dan tiap cara diukur terpisah, jumlah **HEAD** (varian
metode per klaim) = **27 HEAD** (`4+4+4+6+4+2+3 = 27`). Setiap head membawa tier pemakaian sendiri
di REGISTRY kode; **tidak satu pun** berstatus alarm-otomatis (`AUTO_CRITICAL_SLOTS = 0`).
Bab 1 proposal memuat penjelasan tegas ini; PM1 menguncinya di sini supaya seluruh bab konsisten.

---

## 1. PENJELASAN TEGAS: 7 ENGINE vs 11 KLAIM vs 27 HEAD

Tiga angka itu tiga hal berbeda, berjenjang (**7 ⊂ 11 ⊂ 27**):

- **7 ENGINE = 7 kelas hal yang dideteksi** (unit fisis/operasional: "apa yang rusak?"; satu engine per kelas kegagalan).
- **11 KLAIM = 11 pertanyaan tugas terpisah yang dinilai** (unit estimand: deteksi-kondisi vs prediksi-onset adalah tugas beda dengan label & baseline beda — keputusan arsitektur D-A2). 3 engine (vib, ssi, shk) hanya punya satu pertanyaan (deteksi kondisi saat ini); 4 engine (stuck, hyd, bit_wear, tool_wear) punya dua pertanyaan — deteksi kondisi (K-i/K-1) DAN prediksi kejadian mendatang (K-ii/K-2): **3 × 1 + 4 × 2 = 11**.
- **27 HEAD = 27 varian metode yang benar-benar dievaluasi** (unit metode-terukur). Tiap klaim dijawab dengan beberapa cara (rule, persistence, statistik, RF, hibrida), dan tiap cara diukur sendiri dengan fold/kalibrasinya; satu cara = satu head dengan tier, lapisan, badge FAR, dan batas pemakaian di REGISTRY (`v9_i1_pipeline.py` baris 74–287). Sebaran per engine: `4+4+4+6+4+2+3 = 27`.

Konsekuensi penulisan (mengikat semua bab):
1. Pernyataan "**0 dari 7 engine layak alarm otomatis**" ditulis pada **level ENGINE** (tier adalah atribut head; tak ada engine yang seluruh head-nya berstatus alarm).
2. Setiap kali angka 7, 11, atau 27 muncul di sebuah bab, ia harus merujuk daftar eksak di §1.1–§1.3 ini.

### 1.1 Tujuh engine (kelas kerusakan) — NAMA EKSAK dari REGISTRY

| # | Engine (kunci REGISTRY) | Hal yang dideteksi (bahasa operasional) | Kanal/sensor kunci | Jml klaim |
|---|--------------------------|------------------------------------------|--------------------|-----------|
| 1 | `vib` | Kondisi getaran lateral berbahaya (whirl/GET tinggi) | `VIBLAT_RT` (MWD), ambang ≥ 32,17405 ft/s² | 1 |
| 2 | `ssi` | Stick-slip torsional (bit tersendat-sendat memutar) | `SSI(CRPM_RT)`, ambang ≥ 1 | 1 |
| 3 | `shk` | Bit bounce / shock risk (bit memantul memukul formasi) | `SHKRSK_RT`, ambang ≥ 1 | 1 |
| 4 | `stuck` | Stuck pipe (pipa terjepit) — K-i status blok; K-ii onset 0→1, H = 10 menit | `STUCK_RT`; TQA/HKLD/ROP-drop | 2 |
| 5 | `hyd` | Anomali hidrolik — K-i residu tekanan return vs laju aliran; K-ii proxy kick/loss | `SPPA` residu thd `TFLO` | 2 |
| 6 | `bit_wear` | Keausan/balling bit — K-1 blok high_MSE (Teale); K-2 onset | MSE Teale di `USROP` | 2 |
| 7 | `tool_wear` | Keausan mata bor di bengkel — K-i perubahan-regime dalam-run; K-ii ranking lintas-alat | getaran bengkel 1000 Hz, 27 fitur | 2 |

### 1.2 Sebelas klaim — daftar eksak (definisi per kode REGISTRY `klaim_tugas`)

| # | Klaim | Engine | Jenis tugas | Status |
|---|-------|--------|-------------|--------|
| 1 | `vib` K tunggal — deteksi kondisi getaran lateral (status `VIBLAT_RT ≥ 32,17405 ft/s²`) | vib | deteksi kondisi (bukan prediksi onset — TLead tidak berlaku) | aktif |
| 2 | `ssi` K tunggal — deteksi kondisi stick-slip torsional (`SSI(CRPM_RT) ≥ 1`) | ssi | deteksi kondisi | aktif |
| 3 | `shk` K tunggal — deteksi anomali/dysfunction bit bounce (`SHKRSK_RT ≥ 1`) | shk | deteksi anomali sedang berlangsung | aktif |
| 4 | `stuck` `K-i` — deteksi kondisi blok `STUCK_RT` | stuck | deteksi kondisi | aktif |
| 5 | `stuck` `K-ii` — prediksi onset 0→1 (H = 10 menit) | stuck | prediksi kejadian mendatang | aktif |
| 6 | `hyd` `K-i` — deteksi kondisi residu `SPPA` \|z\| > 2 | hyd | deteksi kondisi (label PROXY) | aktif |
| 7 | `hyd` `K-ii` — prediksi kick/loss proxy | hyd | prediksi kejadian mendatang | **TIDAK TERSEDIA** (data pit/GAINLOSSTOT belum diparse — ditulis eksplisit, bukan dihapus) |
| 8 | `bit_wear` `K-1` — deteksi status blok high_MSE (Teale) | bit_wear | deteksi kondisi | aktif |
| 9 | `bit_wear` `K-2` — prediksi onset keausan | bit_wear | prediksi onset | **BELUM** (pra-registrasi belum terbit; nol angka) |
| 10 | `tool_wear` `K-i` — deteksi perubahan-regime dalam-run (bengkel) | tool_wear | deteksi perubahan-regime | aktif |
| 11 | `tool_wear` `K-ii` — ranking keausan lintas-alat | tool_wear | ranking | aktif |

Klaim nomor 7 dan 9 TETAP dihitung sebagai bagian dari 11: kejujuran status ("belum / belum
tersedia") ≠ penghapusan. Ini aturan kejujuran yang mengikat seluruh proposal.

### 1.3 Dua puluh tujuh head — daftar eksak (nama head · klaim · tier · lapisan) dari REGISTRY

Tier/lapisan di bawah = kutipan REGISTRY (`v9_i1_pipeline.py`), diverifikasi dengan menjalankan modul.

| # | Engine | Head (nama kunci REGISTRY) | Klaim | Tier | Lapisan |
|---|--------|-----------------------------|-------|------|---------|
| 1 | vib | `rule_display` | kondisi | PERINGATAN-BERPENGAWAS | L1 |
| 2 | vib | `persistence` | kondisi | TREN | L0 |
| 3 | vib | `hybrid_rule_and_persistence` | kondisi | PERINGATAN-BERPENGAWAS | L1 |
| 4 | vib | `rf_lowo` | kondisi | TREN | L2 |
| 5 | ssi | `rule_display` | kondisi | PERINGATAN-BERPENGAWAS | L1 |
| 6 | ssi | `persistence` | kondisi | TREN | L0 |
| 7 | ssi | `hybrid_rule_and_persistence` | kondisi | PERINGATAN-BERPENGAWAS | L1 |
| 8 | ssi | `rf_lowo` | kondisi | TREN | L2 |
| 9 | shk | `rule_display` | anomali | PERINGATAN-BERPENGAWAS | L1 |
| 10 | shk | `persistence` | anomali | TREN | L0 |
| 11 | shk | `hybrid_rule_and_persistence` | anomali | PERINGATAN-BERPENGAWAS | L1 |
| 12 | shk | `rf_lowo` | anomali | TREN | L2 |
| 13 | stuck | `rule_display` | K-i | PERINGATAN-BERPENGAWAS | L1 |
| 14 | stuck | `persistence` | K-i | TREN | L0 |
| 15 | stuck | `hybrid_rule_and_persistence` | K-i | PERINGATAN-BERPENGAWAS | L1 |
| 16 | stuck | `e1_2of3` | K-ii | TREN | L2 |
| 17 | stuck | `persistence_event` | K-ii | TREN | L2 |
| 18 | stuck | `rf_lowo` | K-ii | TREN | L2 |
| 19 | hyd | `rule_display` | K-i | PERINGATAN-BERPENGAWAS | L1 |
| 20 | hyd | `persistence` | K-i | PERINGATAN-BERPENGAWAS | L0 |
| 21 | hyd | `hybrid_rule_and_persistence` | K-i | PERINGATAN-BERPENGAWAS | L1 |
| 22 | hyd | `k2_tidak_tersedia` | K-ii | BELUM LAYAK PAKAI | L3 |
| 23 | bit_wear | `persistence` | K-1 | TREN | L2 |
| 24 | bit_wear | `k2_onset_belum` | K-2 | BELUM LAYAK PAKAI | L3 |
| 25 | tool_wear | `calib_5of27` | K-i | TREN | L2 |
| 26 | tool_wear | `op_far_calibrated` | K-i | PERINGATAN-BERPENGAWAS | L1 |
| 27 | tool_wear | `canary_3rms` | K-ii | TREN | L2 |

Rekap tier (27 head): PERINGATAN-BERPENGAWAS **12** · TREN **13** · BELUM LAYAK PAKAI **2**.
Rekap lapisan (27 head): L0 **5** · L1 **11** · L2 **9** · L3 **2**. Slot ALARM-OTOMATIS = **0**.

### 1.4 Mengapa tiga angka, bukan satu (untuk dosen)

- Angka **7** menjawab "**apa yang dideteksi alat**" — peta kelas kegagalan BHA + bengkel.
- Angka **11** menjawab "**berapa pertanyaan yang benar-benar dinilai**" — karena tugas deteksi-kondisi dan prediksi-onset tidak boleh dicampur (label & baseline beda).
- Angka **27** menjawab "**berapa cara kami mengukur tiap pertanyaan**" — sehingga klaim "engine X bekerja" selalu dapat dilacak ke satu baris head dengan tier + badge FAR + batas pemakaian, bukan ke satu skor tunggal.

Menjumlahkan 7+11+27 (=45) adalah salah kategori: ketiganya **level berbeda dari objek yang sama**
(kelas → tugas → metode), bukan tiga populasi terpisah.

---

## 2. OUTLINE PROPOSAL BARU (seksi + isi + penutupan keluhan a–f)

Proposal V10 disusun sebagai dokumen tunggal 8 bab. Setiap bab menutup minimal satu butir
keluhan operator; matriks penutupan ada di §2.9.

### Bab 1 — Ruang lingkup & tiga angka: 7 engine / 11 klaim / 27 head  *(penulis: PM1 — dokumen ini)*
- §1.1 Peta 7 engine + hal yang dideteksi + kanal/sensor kunci.
- §1.2 Daftar 11 klaim (tugas, label, baseline per klaim).
- §1.3 Daftar 27 head (nama · klaim · tier · lapisan).
- §1.4 Mengapa 7 ≠ 11 ≠ 27; arti "0 alarm otomatis".
- **Menutup keluhan:** (a) daftar 7 hal yang dideteksi; (f) arti tegas 7/11/27.

### Bab 2 — Mengapa tiap engine dipilih (alasan berbasis bukti)  *(penulis: R&D — t_9cbb587e)*
- Per engine & per klaim: dasar ilmiah (rumus/paper) + dasar empiris (ΔB, lift, CI dari JSON kampanye).
- Justifikasi pemilihan metode: kenapa rule, kenapa persistence, kenapa statistik, kenapa RF, kenapa hibrida.
- Bukti yang MENOLAK sebuah metode (mis. RF dilarang di `hyd` K-i) ditulis sebagai keputusan berbukti, bukan selera.
- **Menutup keluhan:** (c) alasan KENAPA tiap engine dipilih (bukti, bukan selera).

### Bab 3 — Data: apa yang dipakai & perannya dalam identifikasi kerusakan  *(penulis: Data Eng — t_6209eacc)*
- Inventaris dataset: WITSML parsed (9 wellbore), USROP (198.928 baris), F-9A `time.csv` (419.747 baris), external (trajectory MD→TVD, tubular, bhaRun, mudLog, DLIS, EDM, 409 formation picks), tool_wear Mendeley.
- Isi tiap dataset (kanal, satuan, trap konversi) dan **peran masing-masing**: mana pembentuk label, mana fitur, mana join penguat C2.
- Tabel kanal terlarang jadi fitur (anti-sirkularitas, §2.8 V9_PM1) per kelas.
- Kontrak fitur: grid 60 dtk (rig) / 1 dtk (bengkel), jendela [t0−10, t0), statistik mean/std/slope/last/frac, anti-bocor waktu.
- **Menutup keluhan:** (d) peran DATA (data apa, isinya apa, masing-masing berperan apa).

### Bab 4 — Labeling untuk head ML  *(penulis: E_ML — t_2db22ea0)*
- Definisi label per kelas (vib `VIBLAT_RT`, ssi `SSI(CRPM_RT)`, shk `SHKRSK_RT`, stuck `STUCK_RT` onset 0→1 H=10, hyd K-ii z `ΔV_pit`, bit_wear blok high_MSE, tool_wear identitas run).
- Konstruksi label onset (transisi, jendela dalam blok dibuang, jendela positif [t_e−H, t_e)).
- Anti-sirkular: kanal pembentuk label DILARANG jadi fitur + asersi PASS.
- Skema LOWO/LOTO + kontrak model RF (n_estimators, seed 42, imputer fold-safe) + penanganan UNDERPOWERED.
- **Menutup keluhan:** (e) bagian ML — bagaimana LABELING-nya.

### Bab 5 — Metode statistik  *(penulis: E_STAT — t_656ee8de)*
- Rumus persis: median/MAD per bin `qcut(TFLO,10)` (hyd K-i), z-score TQA/HKLD/ROP-drop (stuck E2), change-point SSE 1-split + permutation 500× (tool_wear K-i), kalibrasi within-tool median+MAD 30% awal R01.
- Ambang dipilih di TRAIN (pra-reg), bukan dioptimasi pasca-hasil.
- Tes pembeda (t_cp validity) dan hasilnya apa adanya.
- **Menutup keluhan:** (e) bagian statistik — statistiknya gimana.

### Bab 6 — Rule, persistence & workflow hibrida  *(penulis: E_RULE — t_258c7550)*
- Rule dasar per kelas (VIBLAT≥32,17405 · SSI≥1 · stuck-E1 2-dari-3 · rule z-pit hyd · canary 3-RMS tool_wear).
- Persistence sebagai engine status (dan sebagai baseline tes pembeda).
- **Workflow hibrida**: bagaimana komponen rule + statistik + ML dirangkai (D-A3) dan **pengaruh antar-komponen** (mis. konfirmasi dua langkah rule→persistence; pemangkasan FP hybrid vs rule; di mana ML menambah/mengurangi beban cek).
- Perhitungan SEMUA baseline relevan pada fold identik (S9).
- **Menutup keluhan:** (e) bagian hybrid — workflow-nya & pengaruh antar-komponen.

### Bab 7 — Apa yang dideteksi tiap engine & seberapa bekerja (hasil A/B/C)  *(penulis: EVAL — t_de420dbc)*
- Satu blok per engine/klaim: apa yang dideteksi, metrik A (P/R/FAR/AUPRC/lift/CI vs baseline), B (TLead/B1–B4), C (C1–C4), dan **tier pemakaian** + batas.
- Tabel 11 klaim (setara PM2 §e) + tabel 27 head (tier/lapisan/badge FAR/batas).
- "Belum terukur" dipisah tegas dari "gagal".
- **Menutup keluhan:** (b) engine mana yang bekerja & bagaimana cara kerjanya; (a) diulang pada level hasil.

### Bab 8 — Sintesis alat, batas jujur & langkah lanjut  *(penulis: perakit — t_0720bde5; sumbu PM1)*
- Komposisi alat (L0/L1/L2/L3, 0 slot alarm), keputusan akhir pada manusia.
- Batas muktamad: satu lapangan (Volve), tool_wear domain bengkel ≠ rig, label hyd-K-ii = proxy, B3 tanpa data beban-kerja.
- Syarat kenaikan tier yang sudah terdaftar (kampanye penguatan) — bukan target baru.

### 2.9 Matriks penutupan keluhan → bab

| Keluhan operator | Bab penanggung jawab | Bukti isi |
|---|---|---|
| (a) daftar 7 hal yang dideteksi | Bab 1 (§1.1) + Bab 7 | tabel 7 engine + hasil per engine |
| (b) engine mana bekerja & caranya | Bab 7 + Bab 1 (§1.3) | hasil A/B/C + daftar 27 head |
| (c) alasan KENAPA dipilih (bukti) | Bab 2 | justifikasi ilmiah + empiris per klaim |
| (d) peran DATA | Bab 3 | inventaris dataset + isi + peran + kanal terlarang |
| (e) labeling ML / statistik / hybrid | Bab 4 (ML) · Bab 5 (statistik) · Bab 6 (hibrida) | definisi label · rumus · workflow hibrida |
| (f) arti tegas 7 / 11 / 27 | Bab 1 (§1.0–§1.4) | daftar nama eksak + rekap tier |

---

## 3. DELEGASI SEKSI → TIM (kartu sudah ada; kontrak = dokumen ini)

Setiap tim menerima: (i) daftar eksak §1 sebagai kosakata wajib; (ii) aturan lintas-bab §4; (iii) DoD bab masing-masing.

| Bab | Tim / Kartu | Input wajib | Definition of Done (bab) |
|-----|-------------|-------------|---------------------------|
| Bab 3 Data | Data Eng — `t_6209eacc` | V6_D0, V6_D1a..h, V3_WITSML, V9_D1, V4 | dataset+isi+peran+kanal terlarang lengkap; tiap angka punya jejak sumber |
| Bab 2 Alasan | R&D — `t_9cbb587e` | V9_R1_JUSTIFICATION (27 sitasi), V6_R1, V8_E_*_CAPABILITY | alasan per engine/klaim = bukti ilmiah + empiris; metode yang ditolak ditulis berbukti |
| Bab 4 Labeling ML | E_ML — `t_2db22ea0` | V9_E_ML_ENGINE, v9_e_ML_01_train.py, v9_e_ml JSON, V9_D1 §3 | definisi label per kelas + anti-sirkular + LOWO/LOTO + kontrak RF |
| Bab 5 Statistik | E_STAT — `t_656ee8de` | v9_e_STAT_01..03, V9_E_STAT_ENGINE, v9_e_stat JSON | rumus persis per head statistik + tes pembeda + hasil apa adanya |
| Bab 6 Rule/Hibrida | E_RULE — `t_258c7550` | v9_e_RULE_01..05, V9_E_RULE_ENGINE, v9_e_rule JSON | rule+persistence+workflow hibrida & pengaruh antar-komponen; baseline fold identik |
| Bab 7 Hasil/Tier | EVAL — `t_de420dbc` | V9_EVAL_A/B/C, V8_M1, V9_PM2 §e | hasil A/B/C per engine/klaim + tabel tier 11 klaim & 27 head; "belum terukur" ≠ gagal |
| Bab 1 & Bab 8 (sumbu + sintesis) | PM1 (dokumen ini) → perakit `t_0720bde5` | V10_PM1_OUTLINE + 6 bab tim | Bab 1 dari §1 dokumen ini; Bab 8 merangkai tanpa angka baru |

---

## 4. ATURAN LINTAS-BAB (mengikat semua tim)

1. **Kosakata angka mengikat**: setiap sebutan "7 engine", "11 klaim", "27 head" harus merujuk daftar eksak §1.1–§1.3; nama engine/head persis seperti kunci REGISTRY kode.
2. **Nol angka karangan**: semua angka = kutipan dokumen/JSON sumber; yang belum ada ditulis "belum terukur / belum tersedia / belum dijalankan" — bukan 0, bukan dihapus.
3. **Unit analisis = klaim (11)**: hasil dilaporkan per klaim; deteksi-kondisi dan prediksi-onset tidak digabung.
4. **Baseline relevan per tugas**; FAR pada skala aslinya; fold UNDERPOWERED dilabeli, tidak dihitung mayoritas.
5. **Baris wajib** `Riset pendahuluan: <skill> — <poin>` di setiap bab; `sequentialthinking` ≥3 pikiran; agentmemory untuk fakta tahan-lama.
6. **Proposal = solusi**: tulis apa yang alat deteksi, bagaimana, mengapa, dan pada tingkat apa layak dipakai — bukan riwayat kegagalan.

---

## 5. ACCEPTANCE + FALSIFIER (gerbang sebelum Bab 8 dirakit)

| # | Kriteria acceptance kartu | Uji | Status |
|---|---|---|---|
| AC-1 | Daftar 7/11/27 disebut NAMA-NAMENYA & konsisten dgn kode V9 | jalankan REGISTRY: 7 engine, 27 head (4+4+4+6+4+2+3), 11 klaim | **LULUS** (modul IMPORT OK; lihat §6) |
| AC-2 | Outline menutup keluhan (a)–(f) | matriks §2.9 | **LULUS** (tiap butir punya bab) |
| AC-3 | Delegasi seksi ke 6 tim (Data/R&D/ML/Stat/Rule/Eval) | tabel §3 vs children `t_cf741053` | **LULUS** (6 kartu terpasang) |

Falsifier kerangka (kerangka GUGUR bila salah satu terjadi):
- ada nama engine/head di dokumen yang tidak ada di REGISTRY kode; atau
- jumlah head ≠ 27 saat modul dieksekusi; atau
- ada bab yang mengarang angka di luar dokumen/JSON sumber.

---

## 6. BELUM DIVERIFIKASI / BELUM TERUKUR (verification-mandatory #3)

- Angka **7/11/27** = hasil MENJALANKAN `code/v9_i1_pipeline.py` (IMPORT OK) + cross-check ke EA-1/EB-1/EC-1 dan PM2 §e. Telah terverifikasi.
- Angka **tier/badge/FAR** di §1.3 = kutipan REGISTRY kode (dibaca langsung); TIDAK dihitung ulang dari JSON kampanye di sesi ini.
- Isi lengkap tiap dataset (§3 Bab 3) BELUM diperiksa ulang di sesi ini — menjadi kewajiban tim D1 pada babnya.
- Rincian metrik A/B/C per head BELUM direkapitulasi di sini — menjadi kewajiban tim EVAL (Bab 7).

## 7. SUMBER (dibaca/dijalankan di sesi ini)

`code/v9_i1_pipeline.py` (REGISTRY §1, baris 74–287; **dijalankan** — IMPORT OK, 7 engine/27 head) ·
`docs/V9_PM1_ARCHITECTURE.md` (§2, §3 S1–S9) · `docs/V9_PM2_VERDICT.md` §e (11 baris tier) ·
`docs/V8_M1_CAPABILITY_MAP.md` · `docs/V9_EVAL_A_LAYERA.md` (EA-1) · `docs/V9_EVAL_B_LAYERB.md` (EB-1) ·
`docs/V9_EVAL_C_LAYERC.md` (EC-1) · `docs/V9_I1_INTEGRATION.md` §2 (tabel 27 head).

## 8. BARIS RISET PENDAHULUAN (ringkas)

- Riset pendahuluan: `scientific-critical-thinking` — 7/11/27 dipisah sebagai tiga unit berbeda (kelas/estimand/metode); status "belum/tidak tersedia" dipertahankan sebagai klaim.
- Riset pendahuluan: `statistical-analysis` — unit analisis = klaim (11); baseline relevan per tugas; FAR skala asli; UNDERPOWERED dilabeli.
- Riset pendahuluan: `verification-mandatory` — angka diperoleh dengan menjalankan modul + cross-check 3 dokumen evaluator; daftar belum-diverifikasi §6.
- Riset pendahuluan: `sequentialthinking` — 5 pikiran, 5/5 sukses (inventaris → pemisahan angka → outline → delegasi → acceptance+falsifier).

*Selesai V10-PM1. Kontrak kerja untuk: t_6209eacc (D1), t_9cbb587e (R1), t_2db22ea0 (E_ML),
t_656ee8de (E_STAT), t_258c7550 (E_RULE), t_de420dbc (EVAL); perakitan Bab 8: t_0720bde5.*
