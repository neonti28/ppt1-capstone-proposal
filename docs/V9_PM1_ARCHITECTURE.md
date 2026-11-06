# V9-PM1 — ARSITEKTUR ALAT PdM ADVISORY: 7 ENGINE + SPESIFIKASI + DELEGASI TIM

Task: `t_cf4265ee` [PM · System Architect · Tech Lead] · Board: capstone-v9-build · Tanggal: 2026-10-12 (WIB)
Status: SPESIFIKASI MENGENKUT (kontrak kerja seluruh tim V9) — bukan hasil run; semua
angka = kutipan dokumen primer V8 (dibaca via `read_file` langsung di sesi ini).
Kerangka penilaian: `docs/V8_R1_ABC_SPEC.md` (A/B/C) sesuai instruksi operator
("Evaluasi User.txt") — BUKAN gate lift 1,5.
Sumber desain: `docs/V8_M1_CAPABILITY_MAP.md`, `docs/V8_R1_ABC_SPEC.md`,
`docs/V8_E_{vib,ssi,bit_wear,stuck,hyd,shk,tool_wear}_CAPABILITY.md`,
`docs/V6_D0_READERS_SYNTHESIS.md` + `V6_D1a..h`, `docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md` (v3).

> **Riset pendahuluan: `scientific-critical-thinking`** — dokumen ini memisahkan
> OBSERVED (angka kutipan 7 profil V8, dengan sumber per tabel) vs DESAIN (keputusan
> PM yang bisa diubah lewat change-control sebelum hasil) vs BELUM TERUKUR (daftar §7);
> kontradiksi antar-evaluator direkonsiliasi mengikuti V8_M1 §B.2, bukan dipilih yang
> nyaman; setiap keputusan punya falsifier (tes pembeda §5).
> **Riset pendahuluan: `statistical-analysis`** — baseline RELEVAN per tugas (bukan
> satu baseline universal); AUPRC/lift tidak dirata-ratakan antar kelas (plafon lift
> 1/prev per fold wajib dilaporkan: ssi 15–196, bit_wear 1,84–2,11, tool_wear 2,0);
> FAR dilaporkan per skala aslinya (jendela/24jam/blok/menit) — perbandingan
> lintas-kelas tanpa konversi-skala dilarang; CI95 moving-block bootstrap
> (60/20/10, 1.000 resample, seed 42) seragam; <30 positif/fold = UNDERPOWERED.
> **Riset pendahuluan: `verification-mandatory`** — setiap angka di dokumen ini punya
> jejak baris ke dokumen sumber (daftar §8); bagian tanpa sumber ditulis DESAIN;
> "belum terukur" ≠ 0 ≠ gagal; daftar belum-diverifikasi eksplisit di §7.
> **Riset pendahuluan: `what-if-oracle`** — arsitektur + rencana V9 distress-test 5
> cabang (Ω/α/Δ/Ψ/Φ) + tripwire eksplisit (§5), meng-extend cabang V8_M1 §c.
> **Riset pendahuluan: `consciousness-council`** — 5 arketipe (Architect, Empiricist,
> Minimalist, Pragmatist, Contrarian) menekan desain sebelum finalisasi; titik
> ketegangan & sintesis dicatat §5.2.
> **Riset pendahuluan: `sequentialthinking`** (5 pikiran, 5/5 sukses) — inventaris
> sumber+graph kartu → rancang 5 lapis arsitektur → spesifikasi 7 engine + cek
> konsistensi vs V8_R1 → delegasi+DoD+shared → checklist acceptance + risiko.

---

## 0. KONTEKS DAN APEA YANG BERUBAH

Kerangka evaluasi operator (dari "Evaluasi User.txt", dibawa oleh tiap kartu V9):

1. Keberhasilan = membangun ALAT PdM koheren & layak pakai; ML = satu komponen bila
   beri nilai tambah. Boleh rule-based, statistical, persistence, anomaly, supervised
   ML, atau HYBRID.
2. Setiap engine dinilai di 3 lapisan: **A** (apakah deteksi bekerja: precision,
   recall, FAR, waktu deteksi vs BASELINE RELEVAN tugas itu), **B** (apakah bernilai
   pemeliharaan: peringatan sebelum kondisi memburuk, waktu untuk bertindak —
   TLead vs kejadian nyata = kunci), **C** (cukup tepercaya: lintas periode/regime/
   peralatan, kualitas sensor, ketidakpastian transparan).
3. Hasil disimpan sebagai KEMAMPUAN + BATAS PENGGUNAAN + KEKUATAN BUKTI per engine —
   BUKAN label gagal/buang. "Layak tren tapi belum alarm otomatis" = keputusan wajar.
4. Gate V6 (G1 lift ≥1,5 mayoritas fold; G2 RF ≥ canary mayoritas) TIDAK digeser dan
   TIDAK dihapus — dipakai HANYA sebagai syarat ambang-atas kelas "alarm otomatis"
   (V8-R1 §4). Ini bukan gate kelolosan pemakaian.

Yang dibuat V9-PM1 (dokumen ini = SUMBU yang dirujuk SEMUA kartu):

- Arsitektur alat advisory penuh (§1): data → fitur → 7 engine → lapisan keputusan →
  antarmuka manusia.
- Spesifikasi tiap 7 engine (§2): jenis tugas, jenis engine, input, output, baseline
  relevan, rumus/metode persis, ukuran A/B/C, gate kenaikan tier.
- Komponen shared (§3): kontrak fitur, skema label, protokol pra-reg, determinisme,
  anti-bocor waktu.
- Delegasi + Definition of Done per tim (§4) — mengikat 10 kartu tim yang sudah ada di
  papan.
- Stress-test + tripwire (§5), batas jujur (§6), belum diverifikasi (§7).

## 1. ARSITEKTUR ALAT PdM ADVISORY

### 1.1 Diagram pipeline 5 lapis

```
┌──────────────────────────────────────────────────────────────────────────┐
│ LAYER-0 DATA (tikungan data — output: tabel terbersih + laporan kualitas) │
│  WITSML parsed CSV 9 wellbore · USROP 198.928 baris · F-9A time.csv       │
│  (419.747 baris) · external: trajectory (MD→TVD) · tubular · bhaRun ·     │
│  mudLog · DLIS COMPUTED_OUTPUT · EDM phase=ACTUAL · 409 formation picks   │
│  · tool_wear Mendeley (domain bengkel, modul terpisah)                   │
└──────────────┬───────────────────────────────────────────────────────────┘
               ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ LAYER-1 FITUR (Data Eng D1) — kontrak: grid 60 detik · jendela [t0−10,t0) │
│  statistik per kanal: mean/std/slope/last/frac · imputasi median fold-safe│
│  ANTI-BOCOR: stempel-waktu fitur < stempel-waktu label (pelanggaran = 0)  │
│  SKEMA LABEL per engine + daftar kanal sumber-label (DILARANG jadi fitur) │
│  Output per engine: X (matriks fitur), y (label), metadata, QC-report     │
└──────────────┬───────────────────────────────────────────────────────────┘
               ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ LAYER-2 ENGINE (7 kelas · 3 Algorithm Eng · onset-layer BERSAMA)          │
│  Status-confirmation module (BERSAMA, murah, nol training): persistence   │
│    + rule → vib · ssi · stuck-K-i · hyd-K-i · bit_wear-K-1               │
│  Onset-layer (grid+fitur+calibration harness BERSAMA, head TERPISAH/kelas)│
│    stuck-K-ii · hyd-K-ii · shk-sub-onset · bit_wear-K-2                  │
│  ML heads (bila ΔB>0 vs baseline relevan): RF/GBM/LR — vib · ssi · shk · │
│    stuck-E3 · hyd-K-ii · bit_wear · tool_wear-LOTO                       │
│  Stat heads: median/MAD hyd-K-i · change-point tool_wear-K-i · z stuck-E2│
│  Rule heads: VIBLAT≥32,17405 · SSI≥1 · stuck-E1 (2-dari-3) · 3-RMS canary│
└──────────────┬───────────────────────────────────────────────────────────┘
               ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ LAYER-3 LAPISAN KEPUTUSAN (tier pemakaian per engine — hasil A/B/C)       │
│  L0 · status otomatis (rule/persistence = sistem hari-ini, tanpa ML)      │
│  L1 · peringatan human-in-loop (butuh konfirmasi operator; badge FAR +    │
│       label keyakinan + beban-kerja terukur)                              │
│  L2 · tren/skor (dashboard, tanpa notifikasi)                             │
│  L3 · human decision (semua yang BELUM layak alarm)                       │
│  Alarm otomatis kritis tanpa manusia: 0 slot hari ini (0/7 engine)         │
└──────────────┬───────────────────────────────────────────────────────────┘
               ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ LAYER-4 ANTARMUKA MANUSIA (I1)                                           │
│  notifikasi + dasbor tren + label keyakinan + BADGE BEBAN-KERJA (FAR      │
│  terukur per fold) + batas pemakaian tertulis per engine + keterbatasan   │
│  satu-lapangan; keputusan operasional SELALU pada insinyur pengeboran     │
└──────────────────────────────────────────────────────────────────────────┘

Cross-cutting (berlaku di semua lapis): protokol pra-registrasi ber-hash ·
determinisme seed 42 · CI95 bootstrap seragam · LOWO/LOTO · kalibrasi ambang
SELALU lokal per wellbore · evaluasi A/B/C per engine · audit independen (A1).
```

### 1.2 Keputusan arsitektur PM (mengikat; diubah hanya lewat change-control §6.5)

| # | Keputusan | Dasar bukti |
|---|---|---|
| D-A1 | Grid 60 detik + jendela fitur 10 menit = tulang punggung semua kelas rig (tool_wear bengkel: jendela 1 detik, domain terpisah) | Kontrak V6 yang dipakai SEMUA evaluator V8 (reproduksi 7/7 <1e-9 shk; 9 fold nyata) |
| D-A2 | Onset-layer BERSAMA (grid + feature store + calibration harness), TAPI head prediktor TERPISAH per kelas | V8_M1 §B.3: label beda fisika (STUCK_RT vs ΔV_pit vs SHKRSK vs blok high_MSE) & tindakan beda → satu model gabungan = mencampur estimand |
| D-A3 | Status-confirmation module seragam (persistence + rule) = SATU modul murah untuk vib/ssi/stuck-K-i/hyd-K-i/bit_wear-K-1 | Persistence = engine status terbaik terukur di 4 kelas (hyd ΔB− 7/7; bit_wear 4/4; vib 2/4; shk 4/9) — V8_M1 §B.1 |
| D-A4 | Kalibrasi ambang SELALU lokal per wellbore; kalibrasi lintas-well DILARANG dipakai otomatis | shk: ambang budget-FAR latih → 0 alarm di semua fold uji; stuck: q95 jenuh 1,0/0,0; hyd: FAR test meledak 26–300× |
| D-A5 | Larangan RF spesifik kelas: hyd-K-i DILANGGAN (ΔB negatif 7/7, replikasi eksak) — TIDAK digeneralisasi ke kelas lain | V8_M1 §B.2 C1; vib-RF menang 4/4 vs canary, ssi-RF 5/5 vs canary |
| D-A6 | Tier pemakaian = L0/L1/L2/L3 mengikuti V8_M1 §c + ambang V8-R1 §4; 0 alarm otomatis hari ini | Syarat alarm (FAR≤1/24jam dgn recall>0 + B1≥80% + C2/C3) belum tercapai engine mana pun |
| D-A7 | tool_wear = modul terpisah (domain bengkel, lead detik) — lead-time-nya TIDAK dijumlahkan dengan lead-time rig (menit) | V8_M1 §B.2 C5; 4 alat, run 50–62 dtk, transfer ke drilling TIDAK diklaim |

### 1.3 Gate kenaikan tier per engine (dari V8-R1 §4 + M1 §c — TIDAK DIGESER)

| Kenaikan | Syarat (semua wajib terukur) |
|---|---|
| Masuk LAYER-1 (peringatan human-in-loop) | FAR≤6/24jam-negatif (atau setara skala) TERUKUR dgn recall>0 + TLead/B4 terukur + C4; kalibrasi lokal per well + anotasi regime |
| Masuk LAYER-0-alarm (otomatis) | FAR≤1/24jam-negatif dgn recall>0 + B1≥80% (kelas onset) + G1/G2 mayoritas fold layak + C2 per-bin (drop <20% relatif) + C3 dropout <20% + validasi kejadian nyata |
| Turun tier | Bukan GAGAL — bila FAR terukur >6/24jam (contoh: stuck) → engine turun ke triage/tren dengan anotasi; kemampuan tetap tercatat |

---

## 2. SPESIFIKASI TIAP 7 ENGINE (mengikat; dirujuk E_ML/E_STAT/E_RULE + EVAL A/B/C)

Format per engine: jenis tugas · jenis engine · input · label+anti-sirkular · output ·
baseline relevan · rumus/metode persis · ukuran A/B/C + gate tier · batas pemakaian.
Angka = kutipan V8 (OBSERVED); keputusan PM = DESAIN.

### 2.1 `vib` — deteksi kondisi getaran lateral (whirl/GET tinggi)

| Aspek | Spesifikasi |
|---|---|
| Jenis tugas | **Deteksi kondisi** (status `VIBLAT_RT ≥32,17405 ft/s²`) — BUKAN prediksi onset; TLead tidak berlaku, B4 margin status-awal yang relevan (V8-R1 §2.1) |
| Jenis engine | **Hybrid**: (1) rule ambang-absolut (layer dasar = sistem hari-ini); (2) persistence (konfirmasi-status); (3) RF (penambah nilai peringatan-dini) |
| Input data | Kanal MWD/surface: TFLO, HKLD, SWOB, RPM, ROP, BPOS, depth/dbtm + turunan (V8-E_vib: SHAP top = TFLO_mean/last, depth, dbtm_last/mean, HKLD_mean) |
| Label / anti-sirkular | `VIBLAT_RT` (kanal sumber-label); **`WHIRL_RT` DILARANG** (identik row-level dgn BOUNCE_RT, D0 §2.5); `VIBLAT_RT` dilarang jadi fitur |
| Output | (a) status biner + skor persistence; (b) skor RF [0..1] + status prediksi; tier badge per L1.2 |
| Baseline relevan | (a) rule ambang absolut (FP rule belum terukur → diukur D1/E_RULE); (b) persistence AUPRC 0,517–0,796 (menang 2/4 vs RF); (c) canary-kedalaman 0,277–0,612 |

Rumus/metode persis:
- Rule: `status(t) = 1[VIBLAT_RT(t) ≥ 32,17405]` (ambang absolut R1 §4.2 — definisi operasional rig).
- Persistence: `ŷ(t) = y(t−1)` (1 jendela = 60 dtk sebelumnya).
- RF: `RandomForestClassifier(n_estimators=300, min_samples_leaf=5, class_weight="balanced_subsample", random_state=42)`; fitur = statistik jendela (mean/std/slope/last/frac) 10 menit; imputer median di-fit hanya di fold latih.
- Canary-kedalaman: RF identik HANYA dgn fitur depth/dbtm (pembanding memorisasi posisi).

Ukuran A/B/C + gate (angka V8-E_vib, OBSERVED): AUPRC 0,441–0,912; lift 1,61/2,36/3,50/1,63 (**G1 4/4**); RF≥canary **4/4** (G2); ΔB vs persistence +0,116/+0,015/−0,026/−0,226 (2/4); CI95 semua fold; C1 spread 0,471 (lebar); C2 parsial (canary); C3 nol-bukti; B3/B4/FAR **belum terukur**.
Gate: L2 tren = LAYAK hari ini; L1 peringatan = LAYAK BERSYARAT setelah (i) FAR_t diukur, (ii) B4 diukur; L0-alarm = belum (menunggu B & FAR, bukan A).
Batas: jangan klaim lead-time berapa menit; jangan dipakai untuk prediksi kegagalan mendatang; replikasi F-4/F-10/F-15 (VIBLAT 86/66/76 file, BELUM diparse) = jalur penguatan C1.

### 2.2 `ssi` — deteksi kondisi stick-slip torsional

| Aspek | Spesifikasi |
|---|---|
| Jenis tugas | **Deteksi kondisi** (`SSI(CRPM_RT) ≥ 1`) — bukan onset, bukan diagnosis (V8-R1 §2.2) |
| Jenis engine | **Hybrid**: rule definisi kanal SSI (layer dasar) + RF (penambah nilai terukur — persistence kalah 0/5) |
| Input data | Kanal selain CRPM: TFLO, SPPA, BPOS, HKLD, SWOB, RPM?, ROP, depth/dbtm (V8-E_ssi: SHAP top = TFLO_mean/last, SPPA_mean, BPOS_last/mean/std) |
| Label / anti-sirkular | `SSI(CRPM_RT)` turunan kanal `CRPM_RT` — **`CRPM_RT` dilarang jadi fitur**; label = 1 bila SSI≥1 dengan minimal 10 sampel (Liu 2025; R1 §2.1) |
| Output | status biner + skor RF + label keyakinan (CI/ spread fold wajib tampil — 3/5 fold CI-bawah menyentuh no-skill) |
| Baseline relevan | (a) persistence (kalah 0/5 vs RF — angka per-fold tidak dicetak V6); (b) canary-kedalaman 0,0055–0,0676; (c) rule definisi SSI≥1 (sistem hari-ini) |

Rumus/metode persis:
- `SSI = (max − min) / (2 · mean)` atas jendela CRPM minimal 10 sampel; label `SSI ≥ 1`.
- RF parameter sama dgn vib (kontrak seragam V6); seed 42; imputer median fold-safe.

Ukuran A/B/C (OBSERVED): AUPRC 0,0185–0,1057; lift 2,61/3,59/6,64/3,74/1,47 (G1 4/5; F-9_A 1,47 ✗); RF≥canary **5/5** (G2); persistence 0/5; UNDERPOWERED F-7 (3 pos), F-9 (12 pos) dilaporkan terpisah; C1: hanya 2/5 fold CI-bawah > prev; B semua **belum terukur**; S-E1 (CRPM F-10 281.030 / F-4 42.010 / F-12 178.430 / F-15 57.846 baris) DIOLAH, re-run 11 fold BELUM.
Gate: L2 = LAYAK; L1 = LAYAK BERSYARAT setelah FAR diukur (wajib label keyakinan, bukan angka tunggal); L0-alarm = belum. Bukan satu-satunya detektor SSI (rule tetap dasar).

### 2.3 `bit_wear` — keausan/balling (DUA klaim, dinilai terpisah)

| Aspek | Spesifikasi |
|---|---|
| Jenis tugas | **K-1**: deteksi kondisi (status blok high_MSE Teale); **K-2**: prediksi onset (transisi masuk blok high_MSE, H=10 mnt, sensitivitas 30 mnt) — reframing V7 (V8-R1 §2.3) |
| Jenis engine | K-1: **persistence (engine status terbaik terukur)** + RF screening + canary; K-2: **RF-onset** (dirancang) + **persistence-onset** (tes pembeda wajib) |
| Input data | USROP/WITSML: SPP, FLOW, MUD, GAM, MD, TVD × (mean/std/slope/last/frac) = 30 fitur (E1d); kandidat penguat C2: geologi-join R3 (409 picks + SAND 32.988/CARB 33.386 flags per MD); S-F2 silang MSE/DS (Menand & Mills) |
| Label / anti-sirkular | K-1: blok `high_MSE` dari kolom label USROP (`high_MSE_bit_wear`); **kanal pembentuk MSE DILARANG jadi fitur** (E1d asersi anti-sirkular PASS); K-2: onset = transisi blok, jendela DALAM blok Dibuang (bukan negatif); kandidat 481/329 terverifikasi A1+PM |
| Output | K-1: status + skor (tren); K-2: skor risiko onset + TLead bila alarm; K-2 BELUM boleh dipakai di tingkat apa pun sebelum kampanye berangka |
| Baseline relevan | (a) persistence-status 0,679–0,984 (menang 4/4 vs RF — alasan reframing); (b) canary-kedalaman 0,191–0,756; (c) **persistence-onset** (tes pembeda K-2: bila ≥ RF mayoritas → hipotesis "kegagalan = formulasi status" DITOLAK); (d) prevalence-random (plafon lift 1/prev: F-15S 1,84; F-5 2,11) |

Rumus/metode persis:
- Teale MSE: `MSE = (WOB/Am) + (480 · N · π)/TOR` (Am = luas bit; N = rotary RPM; TOR = torsi) → label blok high_MSE = MSE di atas ambang blok yang sudah terpasang di `USROP_labeled.csv` (definisi label = artefak V2; jangan diubah tanpa pra-reg).
- Persistence-status: `ŷ(t) = y(t−1)`; persistence-onset: `ŷ_onset(t) = onset(t−1)`.
- RF K-1/K-2: kontrak RF seragam (§2.1), seed 42; onset: jendela positif `[t0−H, t0)`, H=10 (sensitivitas 30).

Ukuran A/B/C (OBSERVED, K-1): AUPRC 0,298–0,813; lift 3,11/2,49/1,495/1,65; ΔB vs canary **+0,107/+0,076/+0,058/+0,092 (4/4)**; ΔB vs persistence **−0,381/−0,333/−0,170/−0,087 (4/4 kalah)**; C1 spread 0,515 (lebar); C2 risiko "mengingat posisi" (SHAP didominasi MD/TVD); 3 fold UNDERPOWERED; P/R/FAR **belum terukur** (grep artefak E1d: field tidak ada). K-2: **nol angka** (kampanye belum jalan).
Gate: K-1 persistence = L2 konfirmasi-status LAYAK; K-1 RF = L2 screening; K-2 = BELUM (menunggu kampanye pra-reg); L0-alarm = belum untuk keduanya.


### 2.4 `stuck` — stuck pipe (DUA klaim; onset = fokus)

| Aspek | Spesifikasi |
|---|---|
| Jenis tugas | **K-i**: deteksi anomali/kondisi (blok `STUCK_RT` persisten); **K-ii**: prediksi kejadian mendatang (onset 0→1, H=10 mnt) (V8-R1 §2.4, §3.1) |
| Jenis engine | K-ii 4 engine setara-tugas: **E0 persistence** (tes pembeda) · **E1 rule** (2-dari-3) · **E2 statistical** (z-score) · **E3 RF**; K-i: persistence (angka V6 dipertahankan) |
| Input data | TQA, HKLD, ROP, + 10 kanal rolling window (E3: 55 fitur); label kurasi `labels_curated_v2.csv` (884 event; `bha_stuck_fishing` 38) untuk kontrol-positif |
| Label / anti-sirkular | `STUCK_RT` (primer: ffill, dikunci pra-reg; strict = sensitivitas); **`STUCK_RT` dilarang jadi fitur**; prasyarat pra-reg Fase 0: verifikasi semantik skala 0/1/2/3 lintas wellbore (F-10 didominasi "3", F-14 "1") + rekonsiliasi prev 66,9% vs 49,4% (M2 §8#1) |
| Output | K-ii: skor-ranking risiko onset (triage) + alarm bila lolos gate; K-i: konfirmasi status |
| Baseline relevan | (a) **persistence-onset** (0% recall 3/3 fold — terkonfirmasi lemah per konstruksi); (b) prevalence-random; (c) canary-kedalaman (E3 0,326–0,331 < canary 0,410 → G2 gagal); (d) anchor preseden 2,67–7,37 mnt [R1-S1 §2.2] (untuk B2); K-i: persistence 0,787 (F-9_A) + canary 0,410/0,769 |

Rumus/metode persis:
- E1_rule: `alarm = 1[ (z(TQA)>2) + (z(HKLD)>2) + (ROP-drop ≥30%) ≥ 2 ]`, z vs median+MAD 60 menit.
- E2_stats: skor = `z(TQA) + z(HKLD) + z(ROP-drop)`, ambang q95 di TRAIN (pra-reg).
- E3_RF: `RandomForestClassifier(n_estimators=200, …, random_state=42)`; ambang operasi dipilih di train (q95), BUKAN dioptimasi pasca-hasil.
- Onset: transisi `STUCK_RT 0→1` pada grid 60 dtk; jendela DALAM blok DibuANG; jendela positif `[t_e−H, t_e)`; H=10 (sensitivitas 5/30 belum dijalankan).

Ukuran A/B/C (OBSERVED, run V8-E_stuck): E3 lift 1,65/1,30/9,72/1,12 (4/4>1; signifikan CI hanya 1/4); E2 lift 0,80–1,24 (CI memuat prev 5/5); E1 P 0,457 hanya F-10; B1 maks **31,8%** (<50% bar tren, <80% alarm); TLead 1,5–10 mnt; FAR 9,9–1.440/24jam (semua >6); kontrol-positif **0/10** (F-14); fold F-12 belum terukur (STUCK_RT hanya depth-log, butuh join trajectory).
Gate: L3 triage/inspeksi-manual terbantu (sumur mirip F-10) LAYAK dgn anotasi beban-kerja; L2 ranking riset LAYAK; **L1/L0 = BELUM** (FAR & B1 di atas ambang; C-semantik = risiko utama).

### 2.5 `hyd` — anomali hidrolik (DUA klaim TERPISAH)

| Aspek | Spesifikasi |
|---|---|
| Jenis tugas | **K-i**: deteksi kondisi (status `|z|>2` residu SPPA); **K-ii**: prediksi kegagalan independen (kick/loss proxy, H=10 mnt) (V8-R1 §2.5, §3.2) |
| Jenis engine | K-i: statistical pembentuk-label (median/MAD per bin) + **persistence = ENGINE TERBAIK terukur** (RF DILARANG: ΔB negatif 7/7, D-A5); K-ii: **hybrid RF + fitur aliran (mass-balance)**; rule z-pit = baseline "sistem hari-ini" |
| Input data | K-i: 40 fitur mekanis (TQA/RPM/SWOB/HKLD/ROP/BPOS/depth/dbtm ×5); K-ii: Gas%+ECD+choke+HKLD+RPM+WOB+ROP+BPOS+shocks+depth + varian +Flow Pumps+Mud Flow In; data F-9A time.csv (12 kolom pit, 345.442 non-null, NOL parse sebelumnya); jalur penuh F-1C/F-11 (GAINLOSSTOT 575/517 file) BELUM diparse |
| Label / anti-sirkular | K-i: residu `SPPA − median/MAD per bin qcut(TFLO,10)`; **SPPA/TFLO/SPM DILARANG jadi fitur** (asersi lolos V8); K-ii: z-score `ΔV_pit` per well (median+MAD), sustain ≥5 mnt, syarat sirkulasi ≥500 L/min → 124 episode (39 gain/85 loss); **kolom pit DILARANG jadi fitur**; label = PROXY (annotasi wajib) |
| Output | K-i: status + skor persistence (tren/konfirmasi); K-ii: skor onset + indikasi dini bertingkat-menit + label UNDERPOWERED tampil |
| Baseline relevan | K-i: **persistence** (0,615–0,793; mengalahkan RF 7/7, CI non-tumpang 6/7); canary/aturan-\|z\| manual (B3); K-ii: prevalence-random (prev_test 0,0037; plafon lift 268); rule z-pit (TLead=0 by construction); Fisher & Pearson literal (R1) |

Rumus/metode persis:
- K-i label: bin = `qcut(TFLO, 10)`; `z = 0,6745 · (SPPA − median_bin) / MAD_bin`; status = `|z| > 2`.
- K-i engine: `ŷ(t) = y(t−1)` (persistence; nol-look-ahead, delay 0–3 mnt).
- K-ii label: `ΔV_pit(t) = Σ perubahan volume pit (12 kolom)`; `z = 0,6745·(r10(ΔV_pit) − median_well)/MAD_well`; episode `|z|>2` sustain ≥5 mnt, merge <30 mnt.
- K-ii engine: RF kontrak seragam; varian konservatif vs +flow-in (fitur aliran = syarat sinyal: AUPRC 0,030 vs 0,228).

Ukuran A/B/C (OBSERVED, V8-E_hyd): K-i ΔB RF−persistence **negatif 7/7** (−0,010…−0,400); persistence P 0,615–0,793, R 0,617–0,764, FAR_t 38,8–110,7/24jam (skala jendela) = beban blok 0,16–4,7/hari; konfirmasi kejadian nyata pos_frac 0,884 (7,4× base; n=1 episode); peringatan-dini kejadian nyata **0/1**; coverage sensor 94–98,7%. K-ii: AUPRC_test 0,2279 [0,009;0,629], lift titik 61,6 (konsisten 3 varian label, rentang 8–151); B1 66,7% (2/3) tier alarm +flow; TLead median 7 mnt; onset test 3 = UNDERPOWERED; FAR 5,9/24jam (tier alarm); 1 wellbore.
Gate: K-i = L2 tren status + konfirmasi-kondisi (bukti KUAT) LAYAK; **jangan pakai RF di kelas ini**; K-ii = L2 indikasi dini dgn anotasi ketidakpastian (SEDANG-LEMAH); L0-alarm keduanya = BELUM.


### 2.6 `shk` — deteksi anomali/dysfunction bit bounce (shock risk)

| Aspek | Spesifikasi |
|---|---|
| Jenis tugas | **Deteksi anomali/dysfunction sedang berlangsung** (`SHKRSK_RT ≥1`; ordinal 0–3 = opsi S-B3, belum dievaluasi) + sub-tugas onset blok berkelanjutan H=10 mnt (V8-R1 §2.6, §3.3) |
| Jenis engine | **ML (RF, 55 fitur 11 kanal MWD)** + persistence; reproduksi V6 7/7 <1e-9 = kontrol validitas pipeline |
| Input data | 11 kanal MWD × (mean/std/slope/last/frac) per jendela 10 mnt; fold 9 (7 ORIG + eksternal F-10 146 pos / F-12 217 pos) |
| Label / anti-sirkular | `SHKRSK_RT ≥1` (binarisasi ≥1 dipakai; ordinal = opsi terpisah); **`SHKRSK_RT` dilarang jadi fitur**; semantik severity-mix antar-well wajib diverifikasi (F-12 66% non-null ≥2 vs F-14 40%) |
| Output | skor RF + alarm pada tau operasi lokal; **badge FAR + beban-kerja WAJIB tampil** (B3 negatif terukur di tau ≤0,20); kalibrasi lokal per well |
| Baseline relevan | (a) canary-kedalaman (RF depth-only; V6 G2 lolos 6/7); (b) persistence (`y_prev_shk`); (c) prevalence-random (prev 0,6–9,7%; plafon lift besar); (d) display MWD status-quo (baseline B3) |

Rumus/metode persis:
- RF kontrak seragam (§2.1; n_estimators=300, seed 42); grid tau pra-reg {0,05; 0,10; 0,20; 0,30; 0,50}.
- Alarm = transisi negatif→positif prediksi; FP_alarm = alarm tanpa y=1 dalam `[t, t+H)`; `FAR = FP / jam_operasi_negatif` (per 24 jam).
- B3: `kurangi_ragu = 1 − FP_engine / FP_display_status_quo`.
- Opsi S-B3 ordinal: latih regresi/ordinal, keputusan biner TURUN ke ambang ≥1 yang SAMA (gate tidak digeser); FAR dihitung pada keputusan biner hasil.

Ukuran A/B/C (OBSERVED, V8-E_shk 9 fold): lift 0,94–9,79 (spread 8,85); RF>canary 6/9; **fold eksternal F-10/F-12 lift 0,96/1,06 = sinyal lokal-wellbore**; FAR≤6/24jam dgn recall>0 = **4 titik** (P 0,18–0,55); FAR≤1 dgn recall>0 = **0 dari 9 fold**; B1 @tau0,05 0–0,348, TLead median 2–9 mnt (median global 5,0); **RF≥persistence B1 di 9/9** (nilai tambah ML terukur utk onset); B3 NEGATIF (−0,11…−53,75); C2 drop AUPRC 49–93% pada kuartil depth/RPM/SWOB (7/9 fold); C3 6–8/9 robust; ambang budget-FAR lintas-well = 0 alarm semua fold.
Gate: L2 screening berbiaya-cek-tinggi (tau 0,05–0,10) + L1 peringatan situasional well terkalibrasi + 4 titik hemat-awas LAYAK; **L0-alarm BELUM** (tidak ada di kurva); kalibrasi lintas-wellbore DILARANG (D-A4).

### 2.7 `tool_wear` — keausan mata bor (modul bengkel, 2 sub-klaim)

| Aspek | Spesifikasi |
|---|---|
| Jenis tugas | **K-i**: deteksi perubahan-regime dalam-run (within-tool); **K-ii**: prediksi status keausan lintas-alat (LOTO) (V8-R1 §2.7, §3.4) |
| Jenis engine | K-i: **change-point statistics** + baseline-calibration anomaly; K-ii: **RF LOTO** (ambang inner-LOO F1, tanpa peeking test) |
| Input data | Mendeley `th4yv974r2`: 4 alat × 2 run, 469 jendela 1 dtk @1000 Hz; 27 fitur getaran (kurt/crest/fdom/rms/skew/p2p/zcr/mean/std per sumbu X/Y/Z); VMD features (S-D2) = pengangkat AUPRC |
| Label / anti-sirkular | Label = identitas run (desain dataset, BUKAN turunan fitur → anti-sirkular terpenuhi); K-i anchor = akhir R02 (alat tumpul) + kontrol R01 (alat baru) |
| Output | K-i: skor/flag perubahan-regime (gating kapan inspeksi layak); K-ii: skor ranking keausan lintas-alat; lead = DETIK bengkel (bukan menit rig) |
| Baseline relevan | (i) rule 3-RMS amplitudo + t_cp validity test; (ii) canary 3-RMS (AUPRC 0,516–0,612) + identity-run majority (prev 0,5, plafon lift 2,0); persistence **N/A** (label konstan dalam run — dinyatakan, bukan dihilangkan) |

Rumus/metode persis:
- K-i change-point: SSE 1-split per fitur per segmen 1–2 dtk + permutation test 500× (p=0,002); **tes pembeda t_cp**: bila t_cp ∈ detik awal (<5 dtk) di >50% run → artefak termal → sub-klaim GUGUR (hasil: 0/8 — tapi spesifisitas gagal: cp signifikan 8/8 termasuk alat baru, precision run 0,50).
- Kalibrasi within-tool: median+MAD dari 30% awal R01; alarm ≥5/27 fitur `|z|>3`.
- K-ii RF: kontrak seragam (§2.1); ambang operasi = pooled inner-LOO F1; varian FAR-terkalibrasi (kuantile skor R01 agar laju alarm baseline ≤1/menit) = titik operasi LAYAK.

Ukuran A/B/C (OBSERVED, V8-E_tool_wear): K-ii AUPRC 0,5433–0,7684; lift 1,087–1,418 (G1 0/4; plafon 2,0); ΔB vs canary **4/4 positif** (+0,027…+0,174); precision biner 0,50–0,56 ≈ peluang; FAR-terkalibrasi ≤1/menit: deteksi 4/4, TLead median 47,5 dtk (35–59), FP 1–3; K-i: t_cp signifikan 8/8 run termasuk 8/8 alat baru → spesifisitas keausan GAGAL (precision 0,50); artefak termal 0/8; C3 dropout 1 kanal maks 18,3% (robust), 2 kanal 26,2% (marginal); C-domain: transfer ke drilling TIDAK diklaim (confound urutan-run R02>R01).
Gate: K-ii = L2 skor/ranking + indikasi FAR-terkalibrasi LAYAK (bukti SEDANG); K-i = L2 detektor perubahan-regime (gating inspeksi) — klaim "onset progresi keausan" TERDUKUAT LEMAH; L0-alarm = BELUM; transfer ke rig = TIDAK DIKLAIM tanpa data baru.

### 2.8 Tabel induk anti-sirkularitas (mengikat D1 + semua Algorithm Eng)

| Kelas | Kanal pembentuk label (DILARANG jadi fitur) | Sumber label |
|---|---|---|
| vib | `VIBLAT_RT`; `WHIRL_RT`/`BOUNCE_RT` (duplikat identik) | kanal instrumen MWD |
| ssi | `CRPM_RT` | turunan rumus SSI |
| bit_wear | kanal pembentuk MSE (WOB/ROP/RPM/TORQ — konsisten E1d); kolom `label` USROP | blok high_MSE (Teale) |
| stuck | `STUCK_RT` | kanal instrumen + kurasi DDR (kontrol) |
| hyd K-i | `SPPA`, `TFLO`, `SPM` | residu z-score SPPA |
| hyd K-ii | 12 kolom pit + `GAINLOSSTOT` | z ΔV_pit (proxy) |
| shk | `SHKRSK_RT` | kanal instrumen MWD |
| tool_wear | (label = identitas run — tidak ada kanal sumber) | desain dataset Mendeley |

Aturan turunan: kanal apapun yang MEMBENTUK label (langsung atau lewat rumus) = DILARANG
masuk fitur kelas itu; asersi anti-sirkular dijalankan di pipeline D1 dan WAJIB PASS
(0 pelanggaran) sebelum training dimulai.

---

## 3. KOMPONEN SHARED (kontrak mengikat SEMUA tim)

| # | Komponen | Spesifikasi | Pemilik |
|---|---|---|---|
| S1 | Kontrak fitur | Grid 60 dtk (rig) / 1 dtk (bengkel); jendela [t0−10, t0); statistik mean/std/slope/last/frac per kanal; unit dikonversi per sumber (trap: DLIS 0.1 in ×0.00254, F-15D mm, trajectory rad/dega, EDM ft); join wajib pakai field XML (folder ≠ nameWellbore) | D1 |
| S2 | Skema label per engine | Tabel §2.8 + definisi onset dikunci pra-reg Fase 0 (stuck: strict vs ffill — PILIH SATU); <30 positif/fold = UNDERPOWERED (dilaporkan, tidak dihitung mayoritas) | D1 + PM (pra-reg) |
| S3 | Protokol pra-registrasi | Desain + ambang + identitas pembanding di-hash (SHA-256) SEBELUM training tiap kampanye; ambang TIDAK boleh diubah setelah hasil diketahui (anti shopping-for-significance); perubahan metode = change-control dengan alasan tertulis | PM + tim pelaksana |
| S4 | Determinisme | `random_state=42` SEMUA model; imputer/normalisasi fold-safe (fit hanya di data latih); re-run wajib identik (gerbang eksak tol 1e-9 pada artefak tertentu) | semua tim |
| S5 | Anti-bocor waktu | Stempel-waktu setiap baris fitur < stempel-waktu label-nya; checker independen menghitung pelanggaran (target 0); jendela DALAM blok onset Dibuang (bukan negatif) | D1 (checker) + EVAL_A (verifikasi) |
| S6 | Format hasil | JSON primer per fold di scratch DULU (`*_RESULTS.json` + run log bertimestamp), baru dokumen markdown; setiap angka di dokumen = kutipan dari JSON | semua tim |
| S7 | Metrik + CI | AUPRC + lift (plafon 1/prev dilaporkan); P/R/FAR pada ambang operasi pra-reg; `FAR = FP/jam_neg` per SKALA ASLINYA (jendela/24jam, blok/hari, menit) — konversi-skala wajib dianotasi; CI95 moving-block bootstrap (blok 60/20/10, 1.000, seed 42) | Evaluator A |
| S8 | Output per engine (JSON) | `engine, kelas, klaim_tugas, fold, n/pos/prev, AUPRC+CI95, lift+plafon, P, R, FAR_t/FAR_w, TLead/B1–B4 (onset/status), ΔB vs tiap baseline, C1–C4, status: OBSERVED/DERIVED/BELUM-TERUKUR, batas_pemakaian` | Algorithm Eng |
| S9 | Baseline relevan | Dihitung E_RULE per tugas pada fold yang sama (persistence, canary-depth, prevalence-random, rule ambang); angka baseline = syarat masuk evaluator | E_RULE |


---

## 4. DELEGASI TIM + DEFINITION OF DONE (DoD)

### 4.0 Prinsip delegasi (mengikat semua tim)

1. Graph kartu di papan = urutan kerja nyata: D1+R1 → E_ML/E_STAT/E_RULE → EVAL_A →
   EVAL_B → EVAL_C → I1 → A1 → PM2. Worker TIDAK boleh melompati dependensi.
2. Setiap tim menerima: (i) spesifikasi engine §2 sebagai kontrak; (ii) komponen
   shared §3; (iii) DoD di bawah. Perubahan spesifikasi = change-control ke PM
   (alasan tertulis), BUKAN perubahan sepihak.
3. Semua output = KEMAMPUAN + BATAS PENGGUNAAN + KEKUATAN BUKTI — bukan lulus/gagal.
4. Semua angka dari EKSEKUSI pada data nyata; 0 angka karangan (S6).
5. Baris `Riset pendahuluan: <skill> — <poin>` wajib di setiap dokumen output;
   `sequentialthinking` ≥3 pikiran wajib; agentmemory untuk fakta tahan-lama.

### 4.1 Data Engineer — V9-D1 (`t_1ca71445`)

- Input: data primer Volve (WITSML parsed + raw untuk wellbore baru) + eksternal + USROP + F-9A time.csv + Mendeley tool_wear.
- Tugas: pipeline baca → bersih (konversi satuan S1) → grid → jendela → fitur → matriks per engine + QC-report; skema label §2.8 + anti-sirkular asersi; dataset siap-latih per engine + split LOWO per wellbore; checker anti-bocor (S5).
- DoD: (a) pipeline jalan end-to-end, matriks fitur terbentuk untuk ketujuh kelas + tool_wear; (b) pelanggaran anti-bocor = 0 (dicetak); (c) asersi anti-sirkular PASS per kelas (tabel §2.8); (d) split LOWO siap + determinisme terverifikasi (hash matriks identik 2 run); (e) JSON primer + run log sebelum dokumen; (f) "belum terukur/tidak ada" ditulis eksplisit (bukan nol diam).
- Larangan: membuat keputusan model; memilih ambang; mengubah definisi label tanpa pra-reg.

### 4.2 R&D — V9-R1 (`t_5c5c77e8`)

- Input: spesifikasi §2 (7 engine).
- Tugas: justifikasi ilmiah per engine (paper/rumus + DOI/URL asli via web_search/web_extract): Teale MSE, SSI, median/MAD, change-point, persistence-as-baseline, RF utk deteksi kondisi, z-score pit, Fisher/Pearson literal; tentukan baseline relevan + alasannya per tugas; nyatakan sumber label + risiko sirkularitas per engine; verifikasi metode dipakai SESUAI tugasnya (larangan: ML prediksi untuk tugas deteksi kondisi = salah framing).
- DoD: (a) 7 engine terjustifikasi dgn sitasi asli (0 sitasi karangan — cek via web_extract); (b) rumus persis tertulis per metode; (c) baseline relevan + alasan per tugas; (d) usulan perubahan metode (bila ada) via change-control dengan alasan; (e) daftar risiko label per engine.
- Larangan: mengganti spesifikasi PM sepihak; menuntut metrik seragam antar tugas.

### 4.3 Algorithm Engineer ML — V9-E_ML (`t_902dd141`)

- Input: §2 (head ML per engine) + V9_R1_JUSTIFICATION + fitur D1.
- Tugas: implementasikan + latih head ML: vib-RF, ssi-RF, stuck-E3-RF (200 pohon), shk-RF (55 fitur), hyd-K-ii-RF (+varian flow-in), bit_wear K-1-RF + K-2-onset-RF (bila pra-reg K-2 terbit), tool_wear-K-ii-LOTO-RF; hyperparam kontrak (seed 42, tanpa grid search); jalankan pada LOWO/LOTO data nyata; JSON per fold (S6, S8).
- DoD: (a) semua head jalan pada data nyata + determinisme terverifikasi; (b) hasil per fold dari eksekusi (bukan kutipan); (c) 0 angka karangan; (d) larangan D-A5 dipatuhi (TIDAK ada RF hyd-K-i); (e) dokumen per engine: jenis tugas + jenis engine + baseline yang dipakai + hasil per fold + "belum terukur" eksplisit.
- Larangan: mengubah metode tanpa catatan change-control; melatih pada fold yang berisi data uji (leak); memilih ambang pasca-hasil.

### 4.4 Algorithm Engineer Statistik — V9-E_STAT (`t_af8ea271`)

- Input: §2 (head statistik) + V9_R1 + fitur D1.
- Tugas: implementasikan + jalankan: hyd-K-i median/MAD pembentuk-label + persistence engine; tool_wear-K-i change-point SSE+permutation 500× + kalibrasi within-tool (median+MAD 30% awal R01, alarm ≥5/27 fitur |z|>3); stuck-E2 z-score (q95-train); skor-z turunan fisika yang disetujui R1 (Fisher/Pearson literal bila lolos justifikasi).
- DoD: (a) semua engine jalan pada data nyata; (b) hasil per fold/run dari eksekusi (JSON + log); (c) tes pembeda dijalankan + hasil dilaporkan apa adanya (t_cp validity; persistence-onset); (d) determinisme seed 42; (e) kemampuan+batas ditulis (termasuk hasil NEGATIF terukur = temuan, bukan kegagalan).
- Larangan: mengganti persistence dengan ML di hyd-K-i (D-A5); menyembunyikan hasil tes pembeda yang gugur.


### 4.5 Algorithm Engineer Rule/Persistence/Hybrid — V9-E_RULE (`t_c8bebfb6`)

- Input: §2 (head rule/persistence) + V9_R1 + fitur D1.
- Tugas: (i) persistence semua kelas (status + onset sebagai baseline tes pembeda); (ii) rule: VIBLAT≥32,17405 · SSI≥1 · stuck-E1 (2-dari-3 z TQA/HKLD + ROP-drop≥30%, z vs median+MAD 60 mnt) · rule z-pit hyd (baseline sistem hari-ini) · canary 3-RMS tool_wear; (iii) **menghitung SEMUA baseline relevan (S9)** pada fold yang sama dengan engine utama — persistence, canary-kedalaman, prevalence-random; (iv) perakitan mesin hibrida (rule dasar + statistik + ML sesuai D-A3).
- DoD: (a) semua baseline terhitung per fold per kelas + JSON (syarat masuk evaluator); (b) rule dijalankan pada data nyata (angka FP rule tercetak — membuka B3 vib/ssi yang belum terukur); (c) hibrida dirakit sesuai spesifikasi (bukan model gabungan baru); (d) persistence-onset tes pembeda dijalankan untuk stuck + bit_wear K-2 (bila pra-reg terbit); (e) kemampuan "persistence = engine terbaik" dicatat sebagai KEMAMPUAN (bukan basahan).
- Larangan: menghitung baseline setelah melihat hasil engine lain (harus fold identik, deterministik); mengganti baseline relevan sepihak.

### 4.6 Evaluator Lapisan A — V9-EVAL_A (`t_8a7a33d4`)

- Input: JSON hasil SEMUA engine (S8) + baseline E_RULE (S9).
- Tugas: nilai LAPISAN A per engine per kelas: P, R, FAR_w/FAR_t pada ambang operasi pra-reg, AUPRC+CI95+lift+plafon, TLead/B1 (onset) / B4 (status), ΔB vs SETIAP baseline relevan; hitung pula FP rule (untuk B3 lanjutan EVAL_B); klasifikasi: "A-bekerja" bila ΔB>0 di ≥50% fold layak (bukan ≥1,5).
- DoD: (a) tabel A lengkap 7 engine + klaim terpisah (stuck/hyd/bit_wear/tool_wear) dari angka JSON, bukan karangan; (b) FAR per skala aslinya + anotasi unit; (c) fold UNDERPOWERED dilabeli, tidak dihitung mayoritas; (d) "belum terukur" ≠ "gagal" dipisahkan; (e) recompute sampel ≥1 metrik per kelas dari JSON primer (verifikasi silang).
- Larangan: menilai B/C (tugas EVAL_B/C); menerapkan satu ambang universal; membandingkan FAR lintas-kelas tanpa konversi-skala.

### 4.7 Evaluator Lapisan B — V9-EVAL_B (`t_019ce414`)

- Input: hasil EVAL_A + JSON engine.
- Tugas: nilai LAPISAN B per engine: B1 cakupan peringatan-dini (% onset dalam [t_e−H, t_e)), B2 TLead median/IQR vs anchor kelas (stuck 2,67–7,37 mnt; tool_wear anchor RUL bengkel; kelas status: B4 margin), B3 pengurangan pemeriksaan `1 − FP_engine/FP_baseline_rule` (memakai FP rule dari EVAL_A/E_RULE; baseline = aturan operasional hari ini); validasi terhadap kejadian kurasi (kontrol-positif) bila tersedia.
- DoD: (a) B1/B2/B3/B4 per engine dengan angka dari JSON (bukan taksiran); (b) anchor dipakai per KELAS (dilarang meminjam anchor antar kelas); (c) kasus "arah benar tapi kuantitas kurang" ditulis terpisah dari "tidak terukur"; (d) korelasi ≠ kausalitas ditegaskan (mis. pos_frac 0,88 n=1 episode).
- Larangan: menuntut B1≥80% dari kelas status; menghitung ulang metrik A.

### 4.8 Evaluator Lapisan C — V9-EVAL_C (`t_e43490bf`)

- Input: hasil EVAL_A + EVAL_B + JSON engine + artefak D1.
- Tugas: nilai LAPISAN C per engine: C1 stabilitas temporal (spread AUPRC antar fold + CI95), C2 ketahanan lintas-regime (ΔAUPRC per bin kuartil kedalaman/RPM/SWOB), C3 toleransi kualitas sensor (dropout kanal SHAP-atas 1 & 2 + noise σ/10), C4 transparansi ketidakpastian (CI95 semua fold + label UNDERPOWERED); C-semantik (skala ordinal lintas-well, label proxy, domain bengkel).
- DoD: (a) C1–C4 per engine + klaim; (b) satu kegagalan C4 = engine maks LAYAK TREN (aturan V8-R1 §1.4 ditegakkan); (c) C2/C3 yang BELUM diuji ditulis "belum terukur" (bukan lolos); (d) rekomendasi tier (L0/L1/L2/L3) per engine dengan syarat kenaikan yang tersisa (§1.3).
- Larangan: menaikkan tier tanpa syarat §1.3 terpenuhi; menjatuhkan engine ke "gagal/buang".

### 4.9 Integration Engineer — V9-I1 (`t_34e9b879`)

- Input: rekomendasi tier EVAL_A/B/C + dataset D1 + semua JSON engine.
- Tugas: rakit prototipe alat advisory ( Tahap 1a proposal §17): satu antarmuka yang menampilkan Layer-0 status otomatis, Layer-1 peringatan human-in-loop (shk well terkalibrasi, stuck E1-triage sumur mirip F-10, hyd K-ii anotasi UNDERPOWERED), Layer-2 tren/skor, Layer-3 daftar keputusan manusia; badge FAR + label keyakinan + batas pemakaian per engine; **TANPA alarm otomatis kritis** (0 slot); kalibrasi ambang lokal per well (D-A4); uji integrasi: replay satu wellbore end-to-end.
- DoD: (a) prototipe jalan pada data nyata (replay F-9_A atau F-10); (b) SEMUA tier menampilkan badge FAR + keyakinan + batas tertulis; (c) tidak ada komponen yang menampilkan output sebagai "alarm kritis"; (d) peringatan L1 hanya untuk engine yang lolos syarat §1.3; (e) keterbatasan satu-lapangan tampil di UI.
- Larangan: menaikkan tier engine sendiri; menyembunyikan beban-kerja (FAR) dari tampilan.

### 4.10 Auditor — V9-A1 (`t_0b5671e0`)

- Input: SEMUA dokumen + JSON + skrip V9.
- Tugas: verifikasi independen: (i) angka nyata atau karangan? (recompute ≥1 metrik per kelas dari JSON primer; cek run log bertimestamp); (ii) klaim berlebihan? (setiap "LAYAK X" dicek syarat §1.3 + bukti di dokumen; klaim tanpa jejak = temuan); (iii) kembali ke gate biner? (cek tidak ada tim yang diam-diam menerapkan LULUS/GAGAL seragam atau menuntut lift 1,5 sama rata); (iv) anti-bocor & anti-sirkular: baca ulang laporan D1 + sampling baris fitur; (v) pra-reg: hash kampanye cocok dengan yang dijalankan.
- DoD: (a) tabel klaim: dikutip vs terverifikasi vs terbantah (angka + lokasi); (b) daftar pelanggaran kerangka A/B/C (bila ada) dengan bukti; (c) 0 fabrikasi dikonfirmasi ATAU daftar fabrikasi dengan bukti baris; (d) rekomendasi perbaikan spesifik per tim; (e) audit tidak mengubah hasil tim (read-only + temuan).
- Larangan: "memaafkan" klaim tanpa bukti; memperbaiki data sendiri.

### 4.11 PM2 — V9-PM2 (`t_07d88981`)

- Input: dokumen semua tim + audit A1.
- Tugas: vonis akhir apakah SELURUH pipeline memenuhi evaluasi operator ("Evaluasi User.txt") pada TINGKAT ALAT PdM: (i) koherensi 7 engine + lapisan keputusan; (ii) nilai alat menyeluruh (bukan jumlah model lolos gate); (iii) kejujuran batas; (iv) rekomendasi Tahap 2a (ukur FAR/B4 kampanye penguatan). TIDAK ada target biner lulus/tidak — vonis = tingkat pemakaian alat + sisa syarat.
- DoD: (a) vonis per lapisan A/B/C alat + per engine diringkas dari dokumen tim (bukan angka baru); (b) 3 pertanyaan §3 rumusan masalah proposal dijawab; (c) daftar syarat kenaikan tier tersisa per engine; (d) baris "Riset pendahuluan" + agentmemory fakta tahan-lama.


---

## 5. STRESS-TEST ARSITEKTUR + DELEGASI

### 5.1 What-if-oracle (5 cabang; meng-extend V8_M1 §c)

| Cabang | Bobot | Skenario | Konsekuensi bagi V9 |
|---|---|---|---|
| Ω Best | 15% | Kampanye penguatan jalan penuh (parse VIBLAT F-4/F-10/F-15; S-E1 re-run 11 fold; K-2 bit_wear; GAINLOSSTOT F-1C/F-11; join trajectory F-12) → FAR+B4 tercetak | vib & ssi naik penuh ke L1; stuck/hyd punya fold tambahan; tetap 0 alarm hingga B1≥80% + FAR≤1 terbukti |
| α Likely | 45% (prioritas 61,8% perhatian) | Alat live sebagai L0+L2+L1-terbatas (shk well terkalibrasi, stuck E1-triage, hyd K-ii anotasi) | Nilai PdM = konfirmasi status + triage + indikasi menit; I1 prototipe = bentuk akhir |
| Δ Worst | 20% | FAR/B tak pernah terukur utk vib/ssi/bit_wear (parse tertunda) | Alat tetap koheren di L0+L2 (+L1 shk/stuck/hyd) — batas jujur, BUKAN kegagalan |
| Ψ Wildcard | 10% | Semantik label salah lintas-well (STUCK_RT 0–3, shk severity-mix, hyd proxy) | Onset layer salah sasaran; TRIPWIRE sudah ada: kontrol-positif stuck 0/10 → prasyarat pra-reg Fase 0 jadi gerbang keras |
| Φ Contrarian | 10% | Ternyata persistence/rule SUDAH cukup utk nilai PdM kelas status (terdukung hyd/bit_wear) | ML hanya dipertahankan shk/stuck/hyd-onset + ssi; arsitektur & tim TIDAK berubah (E_ML tugasnya berkurang, bukan batal) |

**Robust actions** (baik di semua cabang): D1 pipeline + anti-bocor + skema label;
persistence/rule module; pra-reg discipline; badge FAR di UI.
**Tripwire (sinyal → perbarui cabang):** FAR≤1 terukur per kelas · K-2 bit_wear
dijalankan · kontrol-positif stuck disinkronkan (zona waktu) · S-E1 re-run ssi ·
parse VIBLAT F-4/F-10/F-15 · GAINLOSSTOT F-1C/F-11 · join trajectory F-12 (stuck).

### 5.2 Consciousness-council (5 arketipe; ketegangan yang dipertahankan, bukan dihapus)

- **The Architect**: onset-layer bersama + head terpisah = struktur yang benar; status-module
  seragam menghemat 5× replikasi. Risiko: over-engineering — I1 cukup prototipe replay
  satu wellbore, jangan platform produksi.
- **The Empiricist**: satu-satunya keputusan yang boleh = yang punya angka. Persistence
  sudah terbukti di 4 kelas; jangan jual ML yang ΔB-nya belum terukur (vib B, ssi FAR).
- **The Minimalist**: 7 engine TIDAK boleh jadi 7 codebase — persistence+rule module
  tunggal (D-A3), RF kontrak seragam tunggal, canary harness tunggal. Yang berbeda
  hanya head + label + baseline.
- **The Pragmatist**: prioritas 61,8% pada cabang α: bangun yang TERBUKTI dulu (L0+L2+L1
  tiga engine), kampanye penguatan = penambahan, bukan prasyarat.
- **The Contrarian**: "0 alarm otomatis" bisa jadi kegagalan persepsi — kontra-argumen:
  ini memang desain advisory (proposal §17: alarm = Tahap 3a setelah label kuat);
  yang berbahaya justru alarm dini tanpa FAR terukur (bukti shk B3 negatif: engine
  MENAMBAH beban cek). Ketegangan ini TIDAK diselesaikan dengan menurunkan ambang.

**Sintesis**: konvergensi 4+ arketipe = modularitas + prioritas bukti + prototipe kecil.
Ketegangan inti = "cepat terlihat berguna" vs "jujur soal bukti" → diresolusi dengan
tier L0/L2 yang langsung bernilai tanpa menunggu kampanye, tanpa mengklaim hal yang
belum terukur.

---

## 6. BATAS JUJUR + CHANGE-CONTROL

1. **Dokumen ini SPESIFIKASI, bukan hasil run.** Semua angka = kutipan V8 (dokumen
   primer yang sudah melalui audit V8_A1); kampanye V9 menghasilkan angka BARU yang
   bisa berbeda — hasil baru MENANG atas kutipan lama (dengan catatan di JSON).
2. **Prasyarat pra-reg Fase 0** (blocker diakui, bukan disembunyikan): definisi onset
   stuck strict-vs-ffill dikunci SATU varian; semantik skala 0/1/2/3 STUCK_RT/
   SHKRSK_RT lintas-well diverifikasi; rekonsiliasi prev stuck 66,9% vs 49,4%.
3. **FAR per 24 jam** mengasumsikan skala operasi Volve (jam operasi = jendela
   eligible); bila unit stand dipakai (S-B2), FAR dihitung per stand + justifikasi
   pra-reg (V8-R1 §6.4).
4. **Gate V6 tidak digeser** (G1/G2 = syarat ambang-atas alarm); kerangka A/B/C
   MENAMBAH ukuran (ΔB, FAR_t, TLead, B1–B4, C1–C4) — tidak ada ambang V6 yang
   dilunakkan, tidak ada gate biner baru yang dibuat untuk "kelolosan".
5. **Change-control**: perubahan spesifikasi §2–§3 setelah kartu tim berjalan =
   hanya via komentar di kartu + persetujuan PM (task ini) SEBELUM eksekusi terkait;
   perubahan SETELAH hasil diketahui = dilarang (anti shopping-for-significance).
6. **Keterbatasan muktamad**: satu lapangan (Volve); tool_wear domain bengkel ≠ rig;
   label hyd-K-ii = proxy; B3 butuh data beban-kerja operasional yang TIDAK ADA di
   Volve (b3 = "belum terukur" untuk kelas tanpa baseline aturan).

## 7. BELUM DIVERIFIKASI / BELUM TERUKUR (verification-mandatory #3)

- Angka V6/V8 yang dikutip di sini = kutipan dokumen primer (dibaca via read_file
  sesi ini); TIDAK dihitung ulang di sesi PM1 — kualitasnya bergantung pada dokumen
  sumber yang sudah melalui audit A1 V8.
- File run-log V6 (`scratch/v6_e1/E1*_RUN_LOG.txt`) tidak dibuka ulang di sesi ini.
- Prevalensi wellbore baru (VIBLAT F-4/F-10/F-15; CRPM hasil S-E1; GAINLOSSTOT) =
  jumlah FILE/baris terverifikasi, bukan jumlah jendela positif (belum diparse).
- Eksistensi data Mendeley tool_wear diverifikasi lewat hasil run V8-E (artefak JSON
  ada); file mentah tidak dibuka ulang di sesi PM1.
- Definisi "jam operasi negatif" per kelas mengikuti konvensi evaluator V8 masing-
  masing; harmonisasi antar-kelas = tugas EVAL_A (S7).

## 8. SUMBER (semua dibaca via read_file di sesi ini)

`docs/V8_M1_CAPABILITY_MAP.md` (peta 7 engine, §B.2 kontradiksi, §c arsitektur awal) ·
`docs/V8_R1_ABC_SPEC.md` (§1 rumus A/B/C, §2.1–2.7 spesifikasi kelas, §3 uji balik,
§4 ambang, §6 batasan) ·
`docs/V8_E_vib_CAPABILITY.md` · `V8_E_ssi_CAPABILITY.md` · `V8_E_bit_wear_CAPABILITY.md` ·
`V8_E_stuck_CAPABILITY.md` · `V8_E_hyd_CAPABILITY.md` · `V8_E_shk_CAPABILITY.md` ·
`V8_E_tool_wear_CAPABILITY.md` (angka terukur per engine) ·
`docs/V6_D0_READERS_SYNTHESIS.md` + `V6_D1a..h` (peta data, trap satuan, WHIRL==BOUNCE) ·
`docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md` v3 (proposal, Tahap 1a–4a) ·
`docs/PROTOCOL_RISET_TIM.md` (pra-reg tim) · papan `capstone-v9-build`
(12 kartu, graph diverifikasi via sqlite langsung di sesi ini).

## 9. BARIS RISET PENDAHULUAN (ringkas)

- Riset pendahuluan: `scientific-critical-thinking` — OBSERVED/DESAIN/BELUM-TERUKUR
  dipisah per bagian; kontradiksi antar-evaluator direkonsiliasi (mengikuti M1 §B.2);
  falsifier per keputusan (§5 tripwire, tes pembeda §2).
- Riset pendahuluan: `statistical-analysis` — baseline relevan per tugas; plafon lift
  1/prev dilaporkan; FAR per skala aslinya; CI95 bootstrap seragam; UNDERPOWERED <30.
- Riset pendahuluan: `verification-mandatory` — angka berjejak sumber (§8); "belum
  terukur" ≠ 0 ≠ gagal; daftar belum-diverifikasi §7; graph kartu diverifikasi langsung
  dari SQLite (bukan asumsi).
- Riset pendahuluan: `what-if-oracle` — 5 cabang Ω/α/Δ/Ψ/Φ + robust actions + tripwire
  (§5.1), prioritas 61,8% cabang α.
- Riset pendahuluan: `consciousness-council` — 5 arketipe; ketegangan inti
  dipertahankan eksplisit (§5.2).
- Riset pendahuluan: `sequentialthinking` — 5 pikiran, 5/5 sukses (tool_call
  sequ-mcp): inventaris → arsitektur → 7 engine → delegasi+DoD → acceptance+risiko.

*Selesai V9-PM1. Kontrak kerja untuk: t_1ca71445 (D1), t_5c5c77e8 (R1),
t_902dd141 (E_ML), t_af8ea271 (E_STAT), t_c8bebfb6 (E_RULE), t_8a7a33d4 (EVAL_A),
t_019ce414 (EVAL_B), t_e43490bf (EVAL_C), t_34e9b879 (I1), t_0b5671e0 (A1),
t_07d88981 (PM2).*
