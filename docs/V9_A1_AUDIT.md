# V9-A1 — AUDIT INDEPENDEN SELURUH PIPELINE V9
# (angka nyata atau karangan? klaim berlebihan? gate biner terselubung?)

Status: HASIL AUDIT — bukan vonis LULUS/GAGAL engine; temuan = kemampuan verifikasi + catatan perbaikan.

## Baris riset pendahuluan

- Riset pendahuluan: scientific-critical-thinking — hipotesis audit "angka karangan" diperlakukan sbg hipotesis yg harus dibantah/dibuktikan dgn bukti diskriminatif (retrain ulang + reimplementasi dari data mentah), bukan dgn membaca dokumen tim; OBSERVED/DERIVED/HYPOTHESIS dipisah di tiap baris tabel.
- Riset pendahuluan: verification-mandatory — SEMUA angka klaim di bawah dihitung ULANG oleh skrip auditor (a1_recompute1–12.py) langsung dari data primer (bins/*.csv.gz, windows→datasets/*.csv.gz, JSON hasil eksekusi); tanpa satu pun angka dikutip dari dokumen tanpa recompute.
- Riset pendahuluan: statistical-analysis — rentang/median dilaporkan dgn unit & denominator; fold UNDERPOWERED dilabeli; CI95-vs-prevalensi dicek per fold; FAR memakai konvensi kampanye FP/(n_neg/60)*24 dgn satuan dinyatakan.
- Riset pendahuluan: what-if-oracle — 5 cabang diuji: Ω "angka tim bisa direproduksi dgn resep persis" (uji: retrain tanpa imputer vs dgn imputer), α "ada gate lift 1,5 terselubung", Δ "ada klaim alarm-otomatis tanpa bukti FAR", Ψ "EVAL_A/B/C saling kontradiksi", Φ "leak QC bohong" — masing-masing diuji dgn tes diskriminatif (§1–§6).
- Riset pendahuluan: consciousness-council — 5 arketipe (Empiricist/Contrarian/Pragmatist/Architect/Historian) menekan audit: Contrarian menuntut auditor salah dulu sebelum menuduh tim (reimplementasi awal auditor SENDIRI keliru — dicatat §7.4, bukan dipakai utk menuduh).
- Riset pendahuluan: sequentialthinking — 4 pikiran (klasifikasi temuan → uji adil → kontrol kualitas verifikasi auditor → putusan) sebelum dokumen ditulis.
- Riset pendahuluan: peer-review — temuan dikelompokkan per tingkat keparahan dgn aksi perbaikan eksplisit (§7) agar bisa direview per butir.

## 0. METODE AUDIT (independen)

Kerangka penilaian = kerangka operator ("Evaluasi User.txt" via PM1 §0): 3 lapisan A/B/C, bukan gate lift 1,5.

Audit independen = auditor TIDAK memakai skrip tim. Sumber primer: `scratch/v9_d1/bins/*.csv.gz` (9 well), `scratch/v9_d1/datasets/*.csv.gz` (6 dataset), JSON hasil eksekusi (E_ML/E_RULE/E_STAT). Skrip auditor: `~/.hermes/cache/scratch/a1_recompute1–12.py` (+ log).

Tes yang dijalankan (7 prosedur tugas):
1. **ANGKA** — ≥12 klaim kunci dihitung ulang. Realisasi: **27 kelompok klaim** (§1).
2. **ANTI-KLAIM-BERLEBIHAN** — setiap "Memenuhi X" di 3 dokumen EVAL diminta bukti angka (§2).
3. **ANTI-GATE-BINER** — regex `LULUS|GAGAL` uppercase + scan pemakaian lift≥1,5 di semua docs & code (§3).
4. **BASELINE RELEVAN** — tiap engine dicek punya baseline per-tugas (§4.1).
5. **KONSISTENSI** — angka silang EVAL_A ↔ EVAL_B ↔ EVAL_C ↔ E_* ↔ I1 (§4.2).
6. **KEPATUHAN SKILL** — baris "Riset pendahuluan" per dokumen (§5).
7. **DETERMINISME & ANTI-BOCOR** — rerun E_STAT, retrain RF independen, invariant `feat_ts_max < lab_ts` dihitung ulang (§6).

## RINGKASAN EKSEKUTIF

| Butir | Hasil |
|---|---|
| Angka dihitung ulang | **27 kelompok klaim** (>12 diminta) |
| Match eksak / hampir-eksak | **23** — termasuk retrain RF independen 24/24 (4 fold × 5 tau + 4 AUPRC, diff 0,00e+00) |
| Kontradiksi antar-tim | **1** (EVAL_A B1 stuck_k2 RF τ0,5 — §7.1) |
| Klaim berlebihan/imprecise | **1** (EVAL_C ssi hybrid "konsisten 7/7" — §7.2) |
| Gate biner terselubung | **TIDAK ADA** (§3) |
| Klaim "layak alarm otomatis" tanpa bukti FAR | **TIDAK ADA** (§2) |
| Pelanggaran skill | **1** (D1 — §5) |
| Bukti determinisme | **TERBUKTI** (§6) |
| Anti-bocor | **0 pelanggaran** di 6 dataset (termasuk stuck_k2 yg log D1-nya MISSING — §6.3) |
| Angka karangan terdeteksi | **TIDAK ADA** |

## 1. TABEL RECOMPUTE — 27 KELOMPOK KLAIM KUNCI

Metode = auditor menghitung ulang dari data MENTAH (bins/datasets) atau retrain model sendiri; kolom "Hasil" = banding auditor vs klaim tim.

### 1A. Kelas rig — rule/persistence (reimplementasi independen dari bins + windows)

| # | Klaim (isi dokumen) | Metode verifikasi auditor | Hasil | Catatan |
|---|---|---|---|---|
| 1 | vib rule-display: P 0,87–0,95 · R 0,28–0,60 · FAR 10,0–49,9/24jam · FP 197 (E_RULE/EVAL_A §2.1) | Reimplementasi `vib_max ≥ 32,17405` pada menit t0−1 langsung dari `bins/*.csv.gz` (tanpa skrip tim) | **TERVERIFIKASI** — P 0,8676–0,9519 · R 0,2761–0,5951 · FAR 9,99–49,94 · FP 197 (persis) | n_nodata F-14 356/1.989 juga cocok |
| 2 | vib persistence: P 0,68–0,83 · R 0,69–0,85 · FAR 74,7–316,3 (EVAL_A §2.1) | Hitung `y_prev_vib` vs `y_vib` dari `datasets/vib.csv.gz` | **TERVERIFIKASI** — P 0,6832–0,8336 · R 0,6867–0,8470 · FAR 74,7–316,3 (persis; FP F-14 190, F-15A 497, F-15_S 486, F-5 283 → total 1.456 = klaim EVAL_B) | |
| 3 | ssi rule-display: FAR 0,0–7,3 (le6 4/9, le1 3/9), R 0,00–0,03, FP 26; nodata 22.385/35.906 = 62,3% | Reimplementasi SSI (crpm, `SSI_MIN_SAMPLES=10`) dari bins | **TERVERIFIKASI** — FAR 0,00–7,33 · le6 4/9 · le1 3/9 · R 0–0,0323 · FP 26 · nodata **22.385/35.906 = 62,3%** (persis) | n_nodata per well F-7 982/982 & F-9 1.126/1.126 = kelas mati sensor |
| 4 | shk rule-display: FAR 0,7–6,6 → le6 **7/9 fold**, FP 121, P 0,00–0,94 | Reimplementasi `shk_max ≥ 1.0` t0−1 dari bins | **TERVERIFIKASI** — FAR 0,67–6,62 · le6&R>0 **7/9** · FP 121 · P 0–0,9352 · R 0–0,3783 (persis) | fold lolos: F-10/12/15_S/5/7/9/9_A |
| 5 | stuck K-i rule: P 0,92–0,97 · R 0,45–0,60 · FAR 8,3–61,0 · FP 49 (2 fold) | Reimplementasi `stuck_max ≥ 1.0` t0−1 dari bins | **TERVERIFIKASI** — P 0,9238–0,9662 · R 0,4491–0,5994 · FAR 8,32–61,00 · FP 49 (persis) | |
| 6 | hyd K-i hybrid: FP **2.091 → 927 (−55,7%)**, P 0,72–0,95, FAR 14,6–58,4 (EVAL_A/C §2.5) | Reimplementasi label z-residu SPPA (qcut-10 median/MAD) + AND persistence dari bins | **TERVERIFIKASI** — rule FP **2.091**, hybrid FP **927**, cut **55,7%**, hybrid P 0,724–0,948 · R 0,525–0,870 · FAR 14,6–58,4 (persis, 9/9 fold hybrid<rule) | Ini klaim sentral "engine paling tepercaya" — LULUS recompute penuh |
| 7 | hyd K-i persistence: P 0,615–0,899 · FAR 32,4–110,7 · FP 1.941 (9 fold) | Hitung `y_prev_hyd` vs `y_hyd` dari windows + banding E_STAT | **TERVERIFIKASI** — P 0,6145–0,8986 · FAR 32,17–110,71 · FP 1.941; E_STAT (varian valid_prev) R 0,617–0,922 cocok kutipan EVAL_A | Dua varian persistence (all-row vs valid_prev) KONSISTEN dgn sumbernya masing-masing |

### 1B. ML (retrain independen — tes terberat)

| # | Klaim | Metode verifikasi auditor | Hasil | Catatan |
|---|---|---|---|---|
| 8 | vib RF: AUPRC 0,441–0,912; τ0,5 P 0,40–0,85 · R 0,10–0,87 · FAR **4,1–496,1** (E_ML/EVAL_A §2.1) | **Retrain RandomForest(n=300, leaf=5, balanced_subsample, seed=42) + SimpleImputer median fold-safe, SEMUA 4 fold, 5 tau** dari `datasets/vib.csv.gz` | **TERVERIFIKASI EKSAK** — AUPRC 4/4 selisih **0,00e+00**; TP/FP/FN **20/20 titik tau eksek**; rentang τ0,5 P 0,40–0,85 · R 0,10–0,87 · FAR 4,15–496,09 (persis) | sha256 prefix 1MB dataset juga cocok dgn JSON |
| 9 | vib RF "titik praktis 1/20 (F-15_S τ0,5: P 0,85 · R 0,10 · FAR 4,1)" | Hitung grid FAR≤6 & R>0 dari recompute #8 | **TERVERIFIKASI** — 1/20; titiknya F-15_S τ0,5 P 0,8525 R 0,1018 FAR 4,14 (persis) | |
| 10 | ssi RF: CI memuat prev **5/9**; AUPRC 0,015–0,459; titik praktis 3/45 | Rehitung CI95-vs-prevalensi per fold dari JSON E_ML + hitung grid | **TERVERIFIKASI** — 5/9 · 0,015–0,459 · 3/45 (F-10 τ0,3 R 0,012; F-12 τ0,3 R 0,048; F-15A τ0,2 R 0,161 — persis spt kutipan) | 2 fold UP (F-7 3 pos, F-9 12 pos) benar dilabeli |
| 11 | shk RF: CI memuat prev **7/9**; AUPRC 0,007–0,193; titik praktis 1/45 (F-14 τ0,3 P 0,44 R 0,005 FAR 0,69) | Rehitung dari JSON E_ML | **TERVERIFIKASI** — 7/9 · 0,007–0,193 · 1/45 dgn titik persis F-14 τ0,3 (P 0,4362 R 0,0053 FAR 0,69) | |
| 12 | vib RF CI memuat prev **0/4**; gb 0/4? — EVAL_C: "CI RF memuat prev 0/4" | Rehitung CI-vs-prev semua model/semua fold | **TERVERIFIKASI** — vib/rf 0/4; (gb 0/4, lr 1/4 — konsisten dgn EVAL_A yg mengutip rf) | |

### 1C. Onset & engine statistik (recompute dari JSON primer + perhitungan silang)

| # | Klaim | Metode verifikasi auditor | Hasil | Catatan |
|---|---|---|---|---|
| 13 | stuck K-ii persistence-EVENT: B1 0,000–0,115 · TLead 4,5–8,5 mnt (med fold 7,0) · FP 11 · FAR 0–2,9 (EVAL_B/C) | Rehitung agregat 4 fold dari JSON E_RULE_02 (b1, tlead_min.median, fp_alarm, far) | **TERVERIFIKASI** — B1 0,000–0,115 · TLead 4,5/8,5 (median fold-median **7,0**) · fp_alarm **11** · FAR 0–2,93 · le6 3/4 (persis) | TLead 7,0 ≈ anchor 2,67–7,37 = klaim "arah benar" berbukti |
| 14 | stuck K-ii persistence-HORIZON: P 1,00 · R 0,82–0,88 · FAR 0 · B1 0,930–0,967 = HINDSIGHT | Rehitung dari JSON E_RULE_02 | **TERVERIFIKASI** — P 1,000 · R 0,823–0,880 · FAR 0,00 · B1 0,930–0,967 (persis) | Label hindsight memang disebut eksplisit di semua dokumen — BUKAN dipakai sbg bukti deployable |
| 15 | stuck K-ii E1: B1 0–0,066 · FAR 2,1–29,0 · FP alarm 422 | Rehitung dari JSON E_RULE_02 | **TERVERIFIKASI** — B1 0–0,066 · FAR 2,09–28,98 · fp_alarm **422** (persis) | |
| 16 | stuck K-ii RF τ0,5: FAR≤6 d **3/4 fold** (P 0,05–1,00 · R 0,004–0,005) · B1 0,027–0,045 · TLead 2–159 | Rehitung dari JSON E_ML_stuck_k2 (tau_metrics + onset_by_tau) | **TERVERIFIKASI + 1 SELISIH** — FAR 0,00/0,60/1,25 (3/4 ≤6; F-9 11,25) · P 0,048–1,000 · R 0,0040–0,0052 · TLead 2–159; **tapi B1 fold F-9 = 0,000** → rentang benar **0,000–0,045**, bukan 0,027–0,045 (lihat §7.1) | EVAL_B menulis "0–0,045" = benar; EVAL_A menulis "0,027–0,045" |
| 17 | hyd K-ii fisher/Pearson: P=R=0 · FP 177 · FAR 31,6 · AUPRC 0,022 CI [0,0025; 0,0684] memuat prev 0,0037 · sign-flip 6.377/8.107 = 78,7% | Rehitung dari JSON E_STAT_04 | **TERVERIFIKASI** — tp=0 fn=30 fp=177 · P=R=0,0 · FAR_24h 31,56 · AUPRC 0,022 · CI memuat prev ✓ · sign_flip_windows **6.377** (6.377/8.107 = 78,7%) (persis) | klaim "belum layak + kendala sensor" berbukti lemah-nya sendiri |
| 18 | hyd K-ii rule z-pit: FP eval 0 & TLead=0 (10/10), B1 0% by construction | Baca JSON E_STAT_04 baseline_rule_zpit | **TERVERIFIKASI** — note "TLead=0 by construction: alarm DI t_e" ada; onsets_test 3 dgn detected_at_H 0 | EVAL_A/B menandai by-construction dgn jujur |
| 19 | tool_wear K-i: precision run 0,50 (4 FP di alat BARU R01) · cp signifikan 8/8 run | Rehitung dari runs[] JSON E_STAT_03 (sig_p05_v8 per run) | **TERVERIFIKASI** — R02 sig 4/4 (TP), R01 sig 4/4 (FP) → precision **0,50** (persis) | spesifisitas keausan gagal = diakui di semua dokumen |
| 20 | tool_wear FAR-terkalibrasi: FP 1–3/alat · deteksi 4/4 · TLead 20–36 dtk · %R02 alarm 3,3–6,9 (target 1,0 & 0,2/mnt) | Rehitung part_C dari JSON E_STAT_03 | **TERVERIFIKASI** — kedua target: FP 1–3 · det 4/4 · TLead 20–36 · pct 3,3–6,9 (persis) | part_B (5/27): FP 27–41/mnt 42,9–58,6 → dinilai TIDAK layak di dokumen — konsisten |
| 21 | tool_wear part D: AUPRC 0,5888 vs identity-majority 0,5117 (ΔB +0,077, lift 1,151); part A TLead med 35 dtk (27–39); artefak termal 0/8 | Rehitung dari JSON E_STAT_03 | **TERVERIFIKASI** — 0,5888 / 0,5117 / +0,0771 / lift 1,1507; TLead values [34,36,39,27] med 35 (27–39); n_early_5s **0/8** (persis) | |
| 22 | bit_wear K-1: persistence AUPRC 0,119–0,984 (lift 1,81–10,67) · ΔB vs canary **5/5 scorable** · 2 fold 0-positif = tak scorable · P/R/FAR "belum terukur" | Rehitung dari JSON E_RULE_03 (folds[]) | **TERVERIFIKASI** — persis: F-9_Ad 0,1185 (UP, 3 pos) · F-14d 0,6792 · F-15d 0,6979 · F-15Sd 0,9837 · F-5d 0,8703; ΔB +0,101/+0,488/+0,410/+0,228/+0,179 **5/5**; F-7d & F-9d prev=0 → persistence None (tak scorable); field TP/FP memang TIDAK ADA → "belum terukur" = status jujur, bukan penyembunyian | |
| 23 | tool_wear K-ii baseline: canary 3-RMS AUPRC 0,516–0,612 · identity = prev 0,496–0,554 (plafon 2,0) | Rehitung dari JSON E_RULE_03 toolwear_kii | **TERVERIFIKASI** — canary 0,5164–0,6119 · identity 0,496–0,554 (persis, 4 fold LOTO) | RF V9 memang TIDAK dijalankan — dinyatakan eksplisit (EA-7) |

### 1D. Lapisan B (B3), integrasi I1, & konsistensi silang

| # | Klaim | Metode verifikasi auditor | Hasil | Catatan |
|---|---|---|---|---|
| 24 | EVAL_B B3: vib persistence −6,39 · ssi hybrid +0,731 · shk RF τ0,5 +0,678 · hyd hybrid +0,557 · stuck hybrid-E1 +0,163 · stuck_k2 pers-EVENT +0,974 · tool_wear +0,909…+0,976 | Rehitung `1 − FP_engine/FP_baseline` dari FP mentah E_RULE/E_STAT (8 titik) | **TERVERIFIKASI 8/8** — −6,391 · +0,731 · +0,678 · +0,557 · +0,163 · +0,974 · +0,909 · +0,976 (semua selisih <0,002 dari kutipan) | FP dasar (197/26/121/2091/49/422/33-41) juga cocok dgn recompute §1A |
| 25 | EVAL_A recompute_checks "18/18" & cross_team "6/6" | Baca isi `v9_eval_a_RESULTS.json` — semua entri `ok:true`, abs_diff 0–1e-13; auditor menambah recompute independen di atas | **TERVERIFIKASI** — 18/18 ok, 6/6 ok; angka contoh (vib RF τ0,2 P 0,6891126494650723; hyd TP 1223/FP 138 silang STAT↔RULE) = angka yg sama dgn recompute auditor | klaim "recompute mandiri" EVAL_A = nyata, bukan stempel kosong |
| 26 | I1 segmen F-14 hyd: rule FP 368 → hybrid FP 110 (−70%), P 0,62→0,82, FAR 55,6→16,6; vib AUPRC segmen 0,9117 | Reimplementasi hyd rule+persistence pada segmen F-14 dari bins; AUPRC vib segmen = fold0 E_ML | **TERVERIFIKASI** — F-14: rule fp 368 P 0,623 FAR 55,6 · hybrid fp 110 P 0,824 FAR 16,6 (persis dgn I1); AUPRC 0,911677 = fold0 E_ML (segmen = fold, by design) | I1 replay F-14 konsisten dgn E_RULE fold0 — integrasi memakai engine asli |
| 27 | Determinisme: E_STAT rerun "identik kecuali elapsed_s"; E_ML "rerun_identical=False dgn diff 2,2e-16 = numerik identik"; ssi nodata 62,3% & F-14 CRPM 96,6% (I1) | Deep-diff struktural JSON `_det_a`/`_det_b` vs main (4 engine); retrain vib independen; recompute nodata | **TERVERIFIKASI** — `_det_a`: 1 selisih = hanya `elapsed_s` (4/4 engine); `_det_b`: **0 selisih**; retrain auditor AUPRC diff 0,00e+00 (numerik identik — konsisten dgn klaim); nodata F-14 ssi 5.268/5.455 = **96,6%** (persis dgn I1) | |

**Rekap §1: 27 kelompok klaim dihitung ulang; 26 terverifikasi (23 persis + 3 dengan selisih rounding <0,005); 1 menghasilkan temuan konsistensi (klaim #16 → §7.1).**

## 2. ANTI-KLAIM-BERLEBIHAN

Pemeriksaan: setiap bentuk "layak/ memenuhi X" di 3 dokumen EVAL + I1 ditanya bukti angkanya.

| Klaim "layak" | Bukti angka (dicek §1) | Verdict |
|---|---|---|
| hyd K-i hybrid "PERINGATAN-BERPENGAWAS, kandidat terkuat" | FAR 14,6–58,4 **>6 di 9/9 fold** dilaporkan berdampingan; tier DILARANG naik tanpa kalibrasi per-well (syarat naik tier dicantumkan dgn angka) | **TIDAK berlebihan** — batas ditulis sekuat klaimnya |
| tool_wear K-i "memenuhi gating inspeksi bengkel" | B3 +0,909…+0,976 dgn FP 1–3 (bukan klaim alarm rig); spesifisitas keausan 0,50 diakui; "transfer ke rig TIDAK diklaim" eksplisit | **TIDAK berlebihan** |
| vib/shk RF "memenuhi sbg penambah ranking" | ΔB vs canary 4/4 & vs prevalensi 9/9 (shk) — murni klaim ranking, BUKAN alarm; CI memuat prev 7/9 (shk) ikut dilaporkan | **TIDAK berlebihan** |
| stuck K-ii "memenuhi utk triage" | AUPRC 0,070–0,444 + B1 0–11,5% dilaporkan; "BELUM utk peringatan dini operasional" dgn alasan 77× beban | **TIDAK berlebihan** |
| "ALARM-OTOMATIS" | **0 head** diberi tier ini; I1 meng-assert `auto_critical_alarm_slots=0` + 11/11 L1 `human_review_required=true` | **TIDAK ADA** klaim alarm otomatis tanpa bukti FAR |

Tidak ditemukan satu pun "layak X" tanpa angka pendukung. Klaim tanpa angka justru dilabeli **"belum terukur"** (bit_wear P/R/FAR, tool_wear K-ii RF V9, B4 bit_wear) — kategori jujur, bukan selubung.

## 3. ANTI-GATE-BINER

| Cek | Metode | Hasil |
|---|---|---|
| Vonis `LULUS`/`GAGAL` uppercase di dokumen | Regex per baris di 10 dokumen V9 | **0 vonis biner.** Semua kemunculan dalam konteks negasi ("BUKAN vonis LULUS/GAGAL", "Bukan GAGAL — bila FAR terukur >6 → turun tier", "GAGAL diverifikasi → DITOLAK" utk kandidat metode R1, "spesifisitas change-point GAGAL" = sub-klaim, bukan vonis engine) |
| Gate lift ≥1,5 dipakai diam-diam sbg vonis | Scan `1.5|1,5`+lift di docs & `code/v9_*.py` | **TIDAK ADA.** 8 penyebutan semuanya eksplisit menolak ("BUKAN gate lift 1,5"). PM1 §0.4 mempertahankan G1/G2 V6 **hanya** sbg syarat ambang-atas kelas "alarm otomatis" dgn kalimat terbuka — bukan gate kelolosan pemakaian; tidak ada satu pun perhitungan/pemilihan angka memakai ambang itu |
| Tuntutan fold/lift seragam antar engine | Cek EA-5/EB-7/EC-2/EC-4 | Diganti dgn ΔB>0 pada ≥50% fold layak (A), band B1/B4 (B), portabilitas (C) — masing-masing dgn baseline per-tugas. Persistence-horizon (B1 0,93) dilabeli HINDSIGHT dan tidak dipakai sbg dasar klaim = contoh baik pemisahan tipe tugas |
| "belum terukur" ≠ "gagal" | Cek 5 entri "belum terukur" (bit_wear P/R/FAR & K-2, tool_wear K-ii RF V9, B4 bit_wear, B3 hyd_kii) | Semua dinyatakan dgn alasan mekanis (field tidak ada / pra-reg belum terbit / RF tidak dijalankan / pembagi nol) — bukan label gagal |

**Kesimpulan §3: tidak ada tim yang kembali ke gate biner; tidak ada gate lift 1,5 terselubung.**

## 4. BASELINE RELEVAN & KONSISTENSI

### 4.1 Baseline per tugas (bukan universal)

| Engine | Baseline dipakai | Cek auditor |
|---|---|---|
| vib/ssi/shk (status) | persistence (y_prev) + rule sistem-hari-ini + canary-kedalaman + prevalence-random | ke-4 ada di JSON E_ML & E_RULE; auditor hitung persistence & rule ulang → cocok (§1A) |
| stuck K-ii (onset) | persistence HORIZON (hindsight, dilabeli) + persistence EVENT (deployable) + E1 + E2 stats + canary | pemisahan hindsight/deployable ada & konsisten di EVAL_A §2.4 |
| hyd K-i | persistence + rule (TAUTOLOGI — dilabeli sbg pembentuk label, bukan pembanding) + canary; RF DILARANG (D-A5) | identitas tautologi diakui E_RULE (n_mismatch=0 pada window label) — circularity ditulis, tidak disembunyikan |
| hyd K-ii | prevalence + rule z-pit (by-construction) + selalu-negatif | FP eval 0 "by construction" dilaporkan dgn B3 "tidak terdefinisi" (EVAL_B) — benar menolak angka fiktif |
| bit_wear | persistence + canary + prevalence (persistence N/A di tool_wear dinyatakan) | ✓ |
| tool_wear | canary 3-RMS + identity-majority + rule 3-RMS; persistence **N/A dinyatakan** (label konstan dalam run) | penolakan persistence = keputusan metodologis ber-alasan, bukan penghapusan diam-diam |

Tidak ditemukan satu baseline universal dipaksakan ke semua engine.

### 4.2 Konsistensi silang

| pasangan | angka | status |
|---|---|---|
| E_RULE ↔ EVAL_A (rule FP 197/26/121/49/2091) | identik | ✓ |
| E_STAT ↔ E_RULE (hyd persistence TP 1223/FP 138 fold F-10; dua varian all-row vs valid_prev) | identik utk fold F-10; rentang R beda varian (0,605–0,877 all-row vs 0,617–0,922 valid_prev) — EVAL_A mengutip varian valid_prev dgn konsisten | ✓ (varian diberi label di JSON masing-masing) |
| EVAL_A ↔ EVAL_B (B3 dari FP E_RULE) | 8/8 titik cocok (§1D #24) | ✓ |
| EVAL_A ↔ EVAL_B (B1 stuck_k2 RF τ0,5) | EVAL_A "0,027–0,045" vs EVAL_B "0–0,045" vs JSON F-9=0,000 | **SELISIH → §7.1** |
| EVAL_C ↔ EVAL_A (CI ssi 3/7 layak vs 5/9 all) | direkonsiliasi eksplisit di EVAL_C EC-3 (2 UP) — dihitung ulang auditor: 5/9 ✓ | ✓ |
| EVAL_C ↔ E_ML (vib FAR τ0,5 4,1–496 = 119×) | recompute 4,14–496,09 → 496,09/4,14 = 120×... | **catatan**: 119× vs 120× (§7.3, selisih pembulatan minor) |
| I1 ↔ E_RULE/E_STAT (replay F-14, tool_wear 4/4 alat) | F-14 hyd rule/hybrid & tool_wear titik operasi identik (§1D #26) | ✓ |

## 5. KEPATUHAN SKILL

| Dokumen | Baris "Riset pendahuluan" | Skill tercatat | sequ-mcp | Catatan |
|---|---|---|---|---|
| V9_PM1_ARCHITECTURE | ✓ | SCT, VM, SA, WIO, CC, SEQ (5 pikiran) | ✓ (klaim) | |
| V9_R1_JUSTIFICATION | ✓ | + literature-review, paper-lookup (9) | ✓ (5 pikiran) | |
| V9_D1_DATA_PIPELINE | ✓ (3 baris) | SCT, VM, SA | **TIDAK ADA** | **PELANGGARAN** — PM1 §336 mewajibkan baris riset per dokumen; WIO/CC/SEQ tidak dicantumkan (lihat §7.4) |
| V9_E_ML_ENGINE | ✓ | SCT, SA, VM, WIO, CC, SEQ (3 pikiran) | ✓ | |
| V9_E_RULE_ENGINE | ✓ (7 baris) | termasuk verification-mandatory klaim-batas | ✓ (6 pikiran) | |
| V9_E_STAT_ENGINE | ✓ (6 baris) | SCT, VM, SA, WIO, CC, SEQ (4 pikiran) | ✓ | |
| V9_EVAL_A/B/C | ✓ (6 baris tiap dokumen) | lengkap + WIO/CC/SEQ dgn jumlah pikiran dicantumkan | ✓ (5/4/4 pikiran) | |
| V9_I1_INTEGRATION | ✓ (6 baris) | lengkap | ✓ (4 pikiran) | |

agentmemory: semua tim melaporkan penyimpanan fakta (mem_… id dicantumkan di handoff masing-masing) — diverifikasi keberadaan entri utk EVAL_C (mem_mv4sbvzc) & I1 (mem_mv4tkkju) via slot project_context.

**Pelanggaran skill: 1 (D1).** Dampak rendah: D1 = dokumen pipeline-data, angka D1 (n_rows, per-well prev, leak invariant) tetap diverifikasi ulang oleh auditor (§6.3) dan cocok.

## 6. DETERMINISME & ANTI-BOCOR

| Cek | Metode | Hasil |
|---|---|---|
| 6.1 Determinisme E_STAT | Deep-diff JSON rerun `_det_a` & `_det_b` vs main utk 4 engine | `_det_b` **identik 100%** (4/4); `_det_a` beda **hanya** `summary.elapsed_s` (4/4) — persis spt klaim EVAL_C |
| 6.2 Determinisme E_ML | **Retrain independen auditor**: RF seed 42, hyperparameter identik, imputer median fold-safe, semua 4 fold vib | AUPRC **4/4 diff 0,00e+00**; TP/FP/FN **20/20 titik tau eksek identik** — determinisme & keaslian angka TERBUKTI dgn resep persis. (Kontrol: tanpa imputer hasil MELESET — imputer material, bukan kosmetik; klaim E_ML "imputer median fold-safe SEMUA model" = benar dan bekerja) |
| 6.3 Anti-bocor `feat_ts_max < lab_ts` | Hitung ulang invariant langsung dari 6 file dataset (pandas) | **0 pelanggaran**: vib 0/23.922 · ssi 0/35.906 · shk 0/56.495 · stuck_k1 0/5.555 · hyd_ki 0/52.509 · **stuck_k2 0/118.567** |
| 6.4 Log leak D1 stuck_k2 "MISSING (merge berjalan)" | Cek ulang dataset akhir | Celah bukti pada waktu D1 ditulis, kini TERISI: recompute independen auditor 0 pelanggaran (6.3). Dataset stuck_k2 ada & valid |
| 6.5 Integritas data | sha256 prefix 1MB `vib.csv.gz` vs JSON E_ML | **COCOK** (f68727a5…) |
| 6.6 Anti-bocor canary/drift | canary-kedalaman (MD/TVD) dipakai sbg baseline bukan fitur terlarang; kanal high_MSE (label bit_wear) tdk masuk fitur ML (daftar 55 fitur = 11 kanal rig ×5 + depth/dbtm — auditor cek, tidak ada kanal label) | ✓ |

## 7. TEMUAN (dilaporkan terus terang)

### 7.1 [KONTRADIKSI ANTAR-TIM — rendah] EVAL_A B1 stuck_k2 RF τ0,5 menutupi fold terburuk
- **Fakta (OBSERVED)**: JSON E_ML_stuck_k2, fold F-9, RF onset_by_tau τ0,5: `B1_coverage = 0.0` (0/16 onset terdeteksi, TLead null). Fold lain: 0,0448 / 0,0357 / 0,0270.
- **Klaim**: EVAL_A §2.4 tabel "RF (τ0,5 titik praktis): B1 0,027–0,045" — memotong fold F-9 (0,000) tanpa anotasi. EVAL_B menulis "0–0,045" = benar.
- **Dampak**: rentang EVAL_A terlihat lebih sempit/lebih baik dari data; kesimpulan ("B1 hanya 2,7–4,5% di titik FAR≤6") tetap arah benar krn F-9 FAR 11,25 (di luar FAR≤6) — defensible, tapi rentang B1 sendiri tidak boleh membuang fold.
- **Aksi**: ubah EVAL_A §2.4 jadi "B1 0,000–0,045 (0,027–0,045 pada 3 fold FAR≤6)".

### 7.2 [KLAIM IMPRECISE — rendah] EVAL_C ssi "hybrid FP-cut 73,1% konsisten 7/7 fold"
- **Fakta (OBSERVED)**: recompute §1A: FP hybrid < rule di **6/7 fold layak**; F-14 = 0→0 (tie, rule sudah 0). Total 26→7 = 73,1% benar.
- **Klaim**: "konsisten 7/7" bisa dibaca "memotong di 7/7" (salah) atau "tidak memburuk di 7/7" (benar).
- **Aksi**: tulis "hybrid ≤ rule di 7/7 fold layak (memotong di 6/7; F-14 tie 0→0); total −73,1%".

### 7.3 [PEMBULATAN MINOR] EVAL_C "vib RF τ0,5 FAR 4,1–496 = 119×"
- **Fakta**: 496,09/4,14 = 119,8 → 120× bula dibulatkan utuh; 119× bila memakai nilai yg sudah dibulatkan 1 desimal (496,1/4,1=121). Selisih 1× tidak mengubah kesimpulan (119× vs 120× sama-sama "tidak portabel"). Tanpa aksi wajib; catat metode rasio bila ingin presisi.

### 7.4 [PELANGGARAN SKILL — rendah] V9_D1_DATA_PIPELINE.md tanpa baris WIO/CC/SEQ
- PM1 §336 mewajibkan baris "Riset pendahuluan: <skill>" di setiap dokumen output; D1 hanya mencantumkan 3 skill (SCT/VM/SA), tanpa sequentialthinking/what-if-oracle/consciousness-council.
- **Aksi**: tambahkan baris riset dgn jumlah pikiran aktual (atau ulangi rapat desain dgn sequ bila memang tidak dilakukan) sebelum D1 dipakai sbg dokumen rujukan proposal.

### 7.5 [CATATAN AUDITOR — bukan pelanggaran tim] kegagalan cocok awal saat audit
Reimplementasi hyd rule dgn binning manual (rank//10) memberi FP 3.380 (SALAH); memakai `pd.qcut(duplicates='drop')` persis resep tim → **2.091/927 EKSAK**. Retrain RF tanpa imputer meleset (AUPRC s/d 0,054); dgn imputer → **identik**. Ini membuktikan: (a) angka tim benar-benar berasal dari resep yg didokumentasikan, (b) resep cukup detail utk reproduksi pihak ketiga, (c) kegagalan pertama = kesalahan auditor, dicatatan ini supaya tidak diulang reviewer berikutnya.

## 8. BELUM DIVERIFIKASI / DI LUAR RENTANG AUDIT INI

1. **CI95 moving-block bootstrap E_ML** — auditor memverifikasi CI-vs-prevalensi dari JSON tersimpan, TIDAK menghitung ulang bootstrap 1.000× per fold (mahal); retrain membuktikan skor/split identik sehingga CI berasal dari skor yg sama.
2. **B4 (margin status-awal) EVAL_B** — perhitungan margin/coverage dari retrain gate-identitas tidak diulang penuh; auditor memverifikasi aritmetika B3 (8/8) + gate-identitas implisit via retrain vib (§6.2). Rekomendasi: evaluator berikutnya ulang B4 utk 1 kelas acak (mis. shk) bila ingin bukti penuh.
3. **AUPRC RF ssi/shk/stuck_k2** — retrain independen baru dilakukan utk vib (kelas dgn AUPRC tertinggi & klaim FAR 119×); ssi/shk/stuck_k2 diverifikasi konsistensi internal JSON + grid + CI, bukan retrain ulang. Ekstrapolasi determinisme dari vib didukung resep & seed identik.
4. **Asal kalender ts_bin** — I1 sendiri menyatakan "asal kalender TIDAK diverifikasi" (catatan waktu ts_bin = indeks menit internal); auditor mengonfirmasi tidak ada klaim tanggal di dokumen manapun → tidak ada pelanggaran, tapi verifikasi kalender tetap terbuka utk tahap berikutnya.
5. **Data primer di luar D1** (mis. file WITSML mentah) — audit memakai bins/datasets hasil pipeline D1 sbg data primer; rantai transformasi WITSML→bins tidak diulang (di luar skala audit ini). Invariant anti-bocor + sha256 + crosscheck V6 (dilaporkan D1) = batas bukti saat ini.

## 9. VERDICT AUDIT

| Pertanyaan audit | Jawaban |
|---|---|
| Angka nyata atau karangan? | **NYATA.** 27 kelompok klaim direcompute; retrain independen eksek 24/24; rerun deterministik; anti-bocor 0 pelanggaran. Tidak ada satu pun angka klaim yg gagal direproduksi. |
| Ada klaim berlebihan? | **TIDAK ADA klaim berlebihan material.** 2 temuan minor (§7.1 rentang B1, §7.2 frase 7/7) + 1 pembulatan (§7.3) — semuanya soal penyajian, bukan substansi penilaian. |
| Kembali ke gate biner? | **TIDAK.** 0 vonis LULUS/GAGAL; gate lift 1,5 hanya sbg syarat ambang-atas alarm-otomatis dgn anotasi; kerangka A/B/C dipakai konsisten dgn baseline per-tugas. |
| Kepatuhan skill | 9/10 dokumen patuh; D1 (§7.4) perlu dilengkapi. |
| Dasar utk menurunkan tier/engine? | **TIDAK ADA.** Temuan §7 bersifat koreksi penyajian; angka dasar & penilaian tier tetap berlaku. |

Audit ini menguatkan keputusan EVAL_C: tidak ada engine layak ALARM-OTOMATIS; hyd K-i hybrid & tool_wear K-i FAR-terkalibrasi tetap dua kandidat terkuat dgn bukti terkuat — persis seperti angka aslinya.

---
Skrip audit: `~/.hermes/cache/scratch/a1_recompute{1..12}.py` + log `a1_recompute{3,4,5,6,7,8,9}.log` (workspace sesi t_0b5671e0).





