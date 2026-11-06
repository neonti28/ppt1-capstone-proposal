# V9-EVAL_A — PENILAIAN LAPISAN A UNTUK 7 ENGINE (kerangka operator A/B/C)

Status: HASIL EVALUASI (kemampuan + batas + kekuatan bukti per engine — BUKAN vonis LULUS/GAGAL).
Sumber angka: JSON primer eksekusi nyata di
`scratch/v9_eval_a/v9_eval_a_RESULTS.json` (turunan mekanis dari
`scratch/v9_e_ml/*.json`, `scratch/v9_e_stat/*.json`, `scratch/v9_e_rule/*.json`).
Dihitung oleh skrip `scratch/v9_eval_a/` (recompute 18/18 + cross-team 6/6, §4).

## Baris riset pendahuluan

- Riset pendahuluan: scientific-critical-thinking — bedakan data vs interpretasi; klaim "deteksi bekerja" wajib punya pembanding baseline yang SAH untuk tugas itu; hindari basahan/pemilihan ambang pasca-hasil (semua tau grid pra-reg dilaporkan).
- Riset pendahuluan: verification-mandatory — setiap angka dikomputasi ulang dari TP/FP/FN/n_neg mentah (18/18 recompute lolos), cross-check antar tim (6/6), dan "belum terukur" dipisahkan dari "gagal"; daftar yang belum dicek ada di §5.
- Riset pendahuluan: statistical-analysis — laporkan efek (AUPRC + CI95 + lift + plafon) bukan p-value semata; fold UNDERPOWERED (positif < 30) dilabeli dan tidak dihitung mayoritas; CI yang memuat prevalensi = sinyal tidak terbukti.
- Riset pendahuluan: what-if-oracle — diuji 4 cabang skenario penilaian (baseline universal vs per-tugas; persistence-horizon disalahtafsir; fold underpowered; "belum terukur" diperlakukan sbg gagal): hanya kerangka per-tugas + pemisahan hindsight/deployable yang menghasilkan peta jujur → dipilih (§0).
- Riset pendahuluan: consciousness-council — 5 arketipe (Empiricist/Pragmatist/Contrarian/Architect/Historian) mempertahankan 3 ketegangan: recall tinggi ↔ FAR meledak; persistence horizon kuat tapi hindsight; deteksi akurat tapi sirkular (rule hyd = pembentuk label).
- Riset pendahuluan: sequentialthinking — 5 pikiran (scope → validasi bukti → what-if/council → klasifikasi 11 klaim → gerbang verifikasi) sebelum dokumen ditulis.

---

## 0. METODE PENILAIAN LAPISAN A

Kerangka (operator, "Evaluasi User.txt" via PM1 §0): **Lapisan A = apakah deteksi bekerja**:
precision, recall, false alarm rate, waktu deteksi — dibanding **baseline relevan untuk tugas
itu**, pada **titik operasi praktis (grid ambang), bukan satu ambang**. Hasil disimpan sebagai
**kemampuan + batas penggunaan + kekuatan bukti**, bukan label gagal/buang.

Keputusan evaluasi (mengikat dokumen ini):

| # | Keputusan | Alasan |
|---|---|---|
| EA-1 | 7 engine dinilai pada **11 klaim**: vib(1), ssi(1), shk(1), stuck K-i+K-ii(2), hyd K-i+K-ii(2), bit_wear K-1+K-2(2), tool_wear K-i+K-ii(2) | PM1 §2: klaim terpisah punya tugas, label, dan baseline berbeda (D-A2) |
| EA-2 | Baseline per tugas: vib/ssi/shk/stuck_k1/hyd_ki = persistence + rule sistem-hari-ini + canary-kedalaman + prevalence-random; stuck_k2 = persistence-HORIZON (hindsight) DAN persistence-EVENT (deployable) dipisah + E1 rule + E2 stats + canary; hyd_kii = prevalence + rule z-pit + selalu-negatif; bit_wear = persistence + canary + prevalence; tool_wear = canary 3-RMS + identity-majority + rule 3-RMS (persistence N/A dinyatakan) | E_RULE mewajibkan pemisahan horizon/event; persistence = baseline terbaik terukur (D-A3) |
| EA-3 | FAR rig = **alarm palsu per 24 jam waktu operasi NEGATIF** (grid 60 dtk): `FAR = FP/(n_neg/60)*24`; tool_wear = **per MENIT** (domain bengkel 1 dtk, D-A7). Unit selalu dinyatakan | FAR tidak boleh dibaca tanpa skala (PM1 §4.6b) |
| EA-4 | Fold UNDERPOWERED (positif < 30) dilabeli, tidak dihitung mayoritas (S2) | mencegah rata-rata menipu |
| EA-5 | "A-bekerja" = ΔB > 0 pada ≥ 50% fold layak (PM1 §4.6, **bukan** lift ≥ 1,5) | gate lama diganti kerangka operator |
| EA-6 | Titik operasi praktis = (i) grid tau pra-reg {0,05;0,10;0,20;0,30;0,50} + q95-train, (ii) ambang tetap rule/persistence, (iii) FAR-terkalibrasi tool_wear; dilaporkan **semua** titik, tanpa memilih pasca-hasil | anti p-hacking |
| EA-7 | Angka berlabel **V8** = kutipan OBSERVED dari PM1 §2, dipakai hanya bila head tidak dijalankan ulang di V9 (hyd K-ii RF, bit_wear RF, tool_wear K-ii RF) dan ditandai sebagai referensi | jangan mencampur eksekusi dengan rujukan |
| EA-8 | Tidak ada vonis biner: tiap klaim ditutup "memenuhi lapisan A untuk X, belum untuk Y, belum terukur untuk Z" + bukti angka | aturan penilaian operator 1–6 |

Cakupan eksekusi V9: E_ML 28 fold (vib 4, ssi 9, shk 9, stuck_k2 4) + 3 model (RF/GB/LR);
E_STAT 4 engine (hyd_ki 9 fold, stuck_E2 4 fold, tool_wear 8 run, fisher/Pearson 1 split);
E_RULE 37 fold rig + 7 fold bit_wear + 4 fold tool_wear + 1 split hyd_kii.

---

## 1. TABEL RINGKAS — 7 ENGINE, 11 KLAIM (LAPISAN A)

Legenda: FAR dalam **per 24 jam operasi negatif** kecuali tool_wear (**per menit**).
"Titik praktis" = titik dengan FAR ≤ 6 + recall > 0 (gerbang LAYER-1 PM1 §1.3).
UP = fold underpowered dilabeli.

| Engine / klaim | Tugas | Metrik utama pada titik operasi praktis (P, R, FAR) | Waktu deteksi | Baseline relevan & ΔB (fold layak) | Kesimpulan kemampuan / batas |
|---|---|---|---|---|---|
| **vib** (K tunggal) | deteksi kondisi VIBLAT≥32,17405 | rule-sistem-hari-ini: P 0,87–0,95 · R 0,28–0,60 · FAR 10,0–49,9 · FP total 197; RF τ0,5: P 0,40–0,85 · R 0,10–0,87 · FAR 4,1–496,1; titik praktis RF **1/20** (F-15_S τ0,5: P 0,85 · R 0,10 · FAR 4,1) | TLead tidak berlaku (kelas status); delay konfirmasi persistence = 0–1 jendela (by construction); B4 = EVAL_B | RF vs canary **4/4**, vs prevalensi 4/4, vs rule 3/4, vs persistence **2/4 (50%)**; AUPRC 0,441–0,912, CI95 tak memuat prev **0/4** | **Memenuhi** utk deteksi kondisi + penambah ranking di atas canary/prevalensi/rule; **belum** utk alarm FAR≤6 lintas fold (1/4 fold; FAR≤1: 0/4). Rule presisi tinggi tapi FAR 10–50/24jam |
| **ssi** (K tunggal) | deteksi kondisi SSI≥1 | RF τ0,3: P 0,00–0,67 · R 0,00–0,13 · FAR 0,0–15,6; titik praktis RF **3/45** (R 0,012–0,161); rule-display FAR 0,0–7,3 (le6 **4/9**, le1 **3/9**) tetapi **R 0,00–0,03** (n_nodata 22.385/35.906 baris) | delay konfirmasi 0–1 jendela; B4 = EVAL_B | RF vs prevalensi **7/7**, vs rule **7/7**, vs persistence 6/7, vs canary 5/7 layak; AUPRC 0,015–0,459; **CI memuat prev 5/9**; UP: F-7 (3 pos), F-9 (12 pos) | **Memenuhi** utk ranking di atas baseline pada fold layak + deteksi hemat-awas (5 titik FAR≤6, R 0,01–0,16); **belum** utk deteksi andal per well (CI menyentuh no-skill di 5/9; rule praktis nyaris tanpa recall) |
| **shk** (K tunggal) | deteksi anomali SHKRSK≥1 | rule-display: P 0,00–0,94 · R 0,00–0,38 · FAR 0,7–6,6 → le6 **7/9 fold** (contoh F-7: P 0,94 · R 0,38 · FAR 4,0) · FP total 121; RF titik praktis **1/45** (F-14 τ0,3: P 0,44 · R 0,005 · FAR 0,69) | delay konfirmasi; alarm-awal & B3 = EVAL_B | RF vs prevalensi **9/9**, vs canary 5/9, vs persistence **4/9**, vs rule **4/9**; AUPRC 0,007–0,193; CI memuat prev 7/9 | **Memenuhi** utk lapisan dasar rule berbiaya-terkendali (7/9 fold FAR≤6 dgn recall>0) + RF sbg penambah ranking vs prevalensi; **belum** utk RF sbg alarm (recall 0,005 pada FAR≤1) dan **belum** A-bekerja vs persistence/rule (4/9 < 50%) |
| **stuck K-i** (status) | deteksi kondisi blok STUCK_RT | rule-display: P **0,92–0,97** · R 0,45–0,60 · FAR 8,3–61,0 (le6 **0/2**) · FP 49; persistence: P 0,68–0,81 · R 0,71–0,80 · FAR 75,4–537,9 · FP 436; E1 rule: R 0,01–0,03 (≈prevalence) · FAR 64,7–65,0 | delay konfirmasi 0–1 jendela | rule vs canary: AUPRC 0,489–0,847 vs 0,410–0,769; cakupan **hanya 2 fold** (F-14, F-9_A) | **Memenuhi** utk konfirmasi-status berpresisi tinggi (0,92–0,97) pada 2 fold yang diuji; **belum** utk FAR≤6 (0/2) → sesuai catatan turun-tier; cakupan 2 fold = kekuatan bukti terbatas |
| **stuck K-ii** (onset) | prediksi onset 0→1, H=10 mnt | RF τ0,5: **3/4 fold** FAR≤6 (P 0,05–1,00 · R 0,004–0,005); E2 q95: P 0,00–0,49 · R 0,00–0,151 · FAR 2,4–73,6 (le6 0/4 dgn R>0); E1: P 0,00–0,44 · R 0,00–0,054 · FAR 2,1–29,0 · FP alarm 422 | **B1 (RF τ0,5) 0,000–0,045** (3 fold FAR≤6: 0,027–0,045; F-9 = 0,000 dgn FAR 11,25 — dikoreksi PM2 sesuai JSON E_ML) · TLead 2–159 mnt; E2 TLead median 2,5–8 mnt, recall@H 0,000–0,181; persistence-EVENT B1 0,00–0,115, TLead 4,5–8,5 mnt; persistence-HORIZON B1 0,93–0,97, TLead 1–3 mnt, FAR 0,0 = **HINDSIGHT** | RF vs canary **4/4**, vs prevalensi 4/4, vs persistence-horizon **0/4**; E2 CI memuat prev **4/4** (lift 1,06–1,80) | **Memenuhi** utk ranking in-horizon di atas canary/prevalensi (triage risiko); **belum** utk peringatan dini pada FAR praktis (B1 hanya 2,7–4,5% di titik FAR≤6; recall onset E1/E2 ≤18%). Persistence-horizon = bukti kuat tapi HINDSIGHT, tidak dipakai sbg dasar klaim |
| **hyd K-i** (status) | deteksi kondisi \|z\|>2 residu SPPA | persistence: P **0,61–0,90** · R 0,62–0,92 · FAR 32,4–110,7 (le6 0/9); hybrid: P **0,72–0,95** · R 0,52–0,87 · FAR 14,6–58,4 (le6 0/9); FP total: rule 2091 → hybrid **927** (9/9 fold), persistence 1941 | **delay deteksi transisi median 0–3,5 mnt**; terdeteksi dlm H10: 31,6–65,4% | persistence ΔB vs prevalensi **9/9** (AUPRC 0,4245–0,8426, lift 2,39–6,10); hybrid vs persistence **8/9** (Δ −0,017…+0,092, mean 0,602 vs 0,555); rule \|z\| = **TAUTOLOGI** (pembentuk label, P=R=1 by construction, FAR definisional 325/24jam); RF dilarang (D-A5) | **Memenuhi** lapisan A utk deteksi kondisi (P/R ≥0,61, ΔB 9/9, delay ≤3,5 mnt) + hybrid = peningkatan presisi terukur; **belum** utk LAYER-1 (FAR 14,6–110,7 > 6 di 9/9 fold); rule bukan pembanding keunggulan (sirkular) |
| **hyd K-ii** (prediksi) | prediksi kick/loss proxy, H=10 mnt | fisher/Pearson varian (1 split temporal): **P 0,00 · R 0,00 · FP 177 · FAR 31,6** di q95; rule z-pit: FP eval 0 & **TLead=0 (10/10), B1=0%** by construction; selalu-negatif: R=0, FAR=0 by construction | TLead varian = nol (tidak ada TP); onset test **3 event** (underpowered utk B1) | AUPRC 0,022 CI [0,0025; 0,0684] **memuat prev 0,0037**; lift 5,95 (plafon 270); ΔB vs prevalensi +0,0183; **RF V8 (referensi)**: 0,2279 [0,009;0,629], lift 61,6, B1 66,7%, TLead 7 mnt, FAR 5,9 | **Belum memenuhi** lapisan A pada titik operasi (P=R=0, 0/3 onset terdeteksi, CI memuat prev); **memenuhi terbatas** sbg ranking di atas prevalensi dgn sinyal tidak terbukti. RF (angka V8) = kemampuan indikasi-dini dengan ketidakpastian sangat lebar, belum diulang di V9 |
| **bit_wear K-1** (status) | deteksi blok high_MSE (Teale) | **P/R/FAR TIDAK DIHITUNG** (field tidak ada di JSON E_RULE/E_STAT) → **belum terukur**, bukan gagal | Tidak ada (kelas status; delay konfirmasi by construction) | persistence AUPRC **0,119–0,984** (mean 0,670; 5/7 fold scorable), lift 1,81–10,67; ΔB persistence vs canary **5/5 scorable (4/4 fold layak)**: +0,101/+0,488/+0,410/+0,228/+0,179; canary mean 0,389; UP: F-9_Ad (3 pos), F-7d & F-9d (**0 pos → tak scorable**) | **Memenuhi** utk ranking status di atas canary & prevalensi pada fold scorable; **belum terukur** P/R/FAR (butuh run ulang dgn TP/FP); cakupan 5/7 fold |
| **bit_wear K-2** (onset) | prediksi onset blok high_MSE | — | — | — | **Belum terukur** (pra-reg K-2 belum terbit; E_RULE DoD-d "bila pra-reg terbit" tidak terpenuhi) — bukan gagal |
| **tool_wear K-i** (regime) | deteksi perubahan-regime dalam-run (bengkel) | change-point signifikan **8/8 run** (p≤0,05 dan p≤0,002) → precision run-level **0,50** (4 FP di R01 alat baru); kalibrasi 5/27: deteksi 4/4 tetapi **FAR 42,9–58,6/menit** (tidak layak); **FAR-terkalibrasi** (target 1,0 & 0,2/menit): **FP 1–3, deteksi 4/4, % jendela R02 alarm 3,3–6,9** | TLead ke akhir R02: median **35 dtk** (27–39); kalibrasi: median **59 dtk** (48–60); FAR-terkalibrasi: **20–36 dtk** | tes pembeda artefak termal **0/8** (sub-klaim bertahan); ranking AUPRC 0,5888 vs identity-majority 0,5117 (ΔB +0,077, lift 1,151 / plafon 1,954) | **Memenuhi** utk deteksi perubahan-regime pada FAR-terkalibrasi (deteksi 4/4, FP 1–3/menit, lead 20–36 dtk); **belum** utk klaim "deteksi keausan spesifik" (spesifisitas gagal: cp juga signifikan di alat baru, precision 0,50) |
| **tool_wear K-ii** (lintas-alat) | prediksi status keausan LOTO | Baseline V9: canary 3-RMS AUPRC 0,516–0,612; identity-majority = prevalensi 0,496–0,554 (plafon 2,0); persistence **N/A dinyatakan** (label konstan dalam run). **RF V9 belum dijalankan** (E_ML = 4 head) | TLead (angka V8): FAR-terkalibrasi ≤1/menit, TLead median 47,5 dtk (35–59), FP 1–3 | **RF V8 (referensi)**: AUPRC 0,5433–0,7684, lift 1,087–1,418, ΔB vs canary **4/4** (+0,027…+0,174), precision biner 0,50–0,56 | **Memenuhi** (basis V9 canary/identity + angka V8) utk ranking dgn margin kecil di atas canary; **belum** utk alarm (precision ≈ peluang); kekuatan bukti = referensi V8, re-run V9 belum ada |

---

## 2. DETAIL PER ENGINE

### 2.1 `vib` — deteksi kondisi getaran lateral (4 fold LOWO, 0 UP)

| Metrik | Rule (sistem-hari-ini) | Persistence | Hybrid | RF (ML) | Canary | Prevalensi |
|---|---|---|---|---|---|---|
| AUPRC | 0,412–0,737 | 0,514–0,793 | 0,412–0,737 | **0,441–0,912** (CI [0,338;0,961]) | 0,277–0,612 | 0,141–0,565 |
| Lift (plafon) | 1,305–3,025 | 1,402–3,656 | 1,305–3,025 | 1,613–3,497 (plafon 1,77–7,12) | 1,084–1,971 | 1,0 (analitik) |
| P | 0,87–0,95 | 0,68–0,83 | 0,87–0,95 | τ0,05: 0,19–0,57 · τ0,3: 0,38–0,72 · τ0,5: 0,40–0,85 | — | — |
| R | 0,28–0,60 | 0,69–0,85 | 0,28–0,60 | τ0,05: 0,96–1,00 · τ0,3: 0,50–0,95 · τ0,5: 0,10–0,87 | — | — |
| FAR/24jam | 10,0–49,9 | 74,7–316,3 | 10,0–49,9 | τ0,05: 983–1440 · τ0,3: 189–699 · τ0,5: **4,1**–496 | — | — |
| FAR≤6 & R>0 | 0/4 | 0/4 | 0/4 | **1/20 titik** | — | — |

- ΔB (fold layak): RF vs canary **4/4**, vs prevalensi 4/4, vs rule **3/4**, vs persistence **2/4 (=50%, persis di ambang ≥50%)** → RF = A-bekerja; CI95 RF tidak memuat prevalensi di 4/4 fold.
- FP rule (untuk B3 EVAL_B): **197** (TP 2243, FN 3186, n_nodata 2999).
- **Kemampuan**: mendeteksi status VIBLAT dengan presisi 0,87–0,95 pada rule, dan RF menaikkan ranking di atas canary/prevalensi/rule di ≥75% fold.
- **Batas**: pada FAR ≤ 6/24jam hanya 1 dari 20 titik grid RF (dan 0/4 fold utk rule/persistence) → belum layak sbg alarm/gate L1; AUPRC spread 0,471 (C1 lebar, konsisten V8).
- **Belum terukur**: B4 margin status & B3 (EVAL_B); replikasi F-4/F-10/F-15 (VIBLAT belum diparse).

### 2.2 `ssi` — deteksi kondisi stick-slip (9 fold, UP: F-7 3 pos, F-9 12 pos)

| Metrik | Rule (definisi SSI) | Persistence | Hybrid | RF | Canary | Prevalensi |
|---|---|---|---|---|---|---|
| AUPRC | 0,003–0,068 | 0,003–0,188 | 0,003–0,065 | **0,015–0,459** (CI memuat prev **5/9**) | 0,010–0,086 | 0,003–0,065 |
| P / R | 0,00–0,50 / **0,00–0,03** | 0,00–0,43 / 0,00–0,40 | 0,00–0,67 / 0,00–0,01 | τ0,3: 0,00–0,67 / 0,00–0,13 | — | — |
| FAR/24jam | **0,0–7,3** (le6 4/9, le1 3/9) | 0,0–51,3 (le6 2/9) | 0,0–3,7 (le6 1/9) | τ0,3: 0,0–15,6; 5 titik le6 (R 0,012–0,161), 1 titik le1 | — | — |

- ΔB layak: RF vs prevalensi **7/7**, vs rule **7/7**, vs persistence 6/7, vs canary 5/7 → A-bekerja.
- Rule recall sangat rendah disertai **n_nodata 22.385 dari 35.906 baris** (CRPM absen di banyak jendela) → recall rendah = keterbatasan data, bukan murni kegagalan rule; FP rule total **26**.
- **Kemampuan**: RF = penambah ranking terukur di atas semua baseline pada fold layak; rule/persistence = detektor hemat-awas (FAR ≤ 7,3 dgn recall kecil).
- **Batas**: kualitas per-fold lemah (CI memuat prevalensi 5/9; AUPRC fold terendah ≈ prevalensi), recall praktis rule ≤0,03 → belum layak sbg detektor tunggal; 2 fold UP dilabeli, tidak dihitung mayoritas.

### 2.3 `shk` — deteksi anomali/dysfunction bit bounce (9 fold, 0 UP)

| Metrik | Rule | Persistence | Hybrid | RF | Canary | Prevalensi |
|---|---|---|---|---|---|---|
| AUPRC | 0,006–0,414 | 0,006–0,443 | 0,006–0,414 | 0,007–0,193 (CI memuat prev **7/9**) | 0,012–0,079 | 0,006–0,097 |
| P / R | 0,00–**0,94** / 0,00–0,38 | 0,00–0,70 / 0,00–0,58 | sama dgn rule | τ0,3: 0,00–0,44 / 0,00–0,49 | — | — |
| FAR/24jam | **0,7–6,6** → le6 **7/9 fold** | 3,2–54,0 (le6 1/9) | 0,7–6,6 (7/9) | 1 titik le6 (F-14 τ0,3: P 0,44 · R 0,005 · FAR 0,69), 1 titik le1 | — | — |

- Contoh titik rule layak: F-7 P 0,935 · R 0,378 · FAR 4,04; F-12 P 0,579 · R 0,051 · FAR 2,22; F-15_S P 0,405 · R 0,058 · FAR 2,85. FP rule total **121**.
- ΔB layak: RF vs prevalensi **9/9**, vs canary 5/9, vs persistence **4/9 (44%)**, vs rule **4/9 (44%)** → A-bekerja HANYA vs prevalensi/canary.
- **Kemampuan**: rule = lapisan dasar berbiaya-terkendali (7/9 fold lolos gerbang FAR≤6 dgn recall>0 — satu-satunya kelas rig dgn mayoritas fold di bawah 6/24jam); RF menaikkan ranking vs prevalensi.
- **Batas**: RF praktis memancar (recall 0,005 pada FAR≤1); CI memuat prevalensi di 7/9; angka V8 melaporkan fold eksternal F-10/F-12 lift 0,96/1,06 (sinyal lokal-wellbore) → C1/C2 jadi risiko, B3 negatif terukur di EVAL_B.

### 2.4 `stuck` — K-i status (2 fold) + K-ii onset (4 fold), 0 UP

**K-i (status, E_RULE):**

| Metrik | Rule display | Persistence | Hybrid | E1 rule (2-dari-3) | Canary |
|---|---|---|---|---|---|
| AUPRC | 0,489–0,847 | 0,520–0,783 | 0,489–0,847 | 0,134–0,666 | 0,410–0,769 |
| P / R | **0,92–0,97** / 0,45–0,60 | 0,68–0,81 / 0,71–0,80 | = rule | 0,05–0,55 / 0,01–0,03 | — |
| FAR/24jam | 8,3–61,0 (le6 0/2) | 75,4–537,9 (0/2) | = rule | 64,7–65,0 | — |
| FP total | **49** | 436 | 49 | 160 (hybrid-E1 41) | — |

**K-ii (onset, H=10 mnt):**

| Engine | AUPRC | P (titik operasi) | R / recall@H | FAR/24jam | B1 | TLead median |
|---|---|---|---|---|---|---|
| RF (τ0,5 titik praktis) | 0,070–0,444 (CI [0,028;0,565]) | 0,05–1,00 | R 0,004–0,005 | **0,0–1,25** (3/4 fold) | **0,000–0,045** (F-9 0,000; 0,027–0,045 pada 3 fold FAR≤6 — koreksi PM2) | 2–159 mnt |
| RF (τ0,05) | (sama) | 0,01–0,33 | R 0,36–1,00 | 266,8–812,3 | 0,507–1,000 | 10–11,5 mnt |
| E2 statistik (q95-train) | 0,007–0,324 (CI memuat prev **4/4**) | 0,00–0,487 | recall@H 0,000–0,181 | 2,4–73,6 | — | 2,5–8 mnt |
| E1 rule | 0,193–0,193* (lift 1,00–1,06) | 0,00–0,435 | R 0,00–0,054 | 2,1–29,0 (le6 1/4) | 0,00–0,066 | 1–5 mnt |
| Persistence-EVENT (deployable) | 0,113 (mean) | 0,50–0,75 | R 0,000–0,019 | 0,0–2,9 (le6 3/4) | 0,000–0,115 | 4,5–8,5 mnt |
| Persistence-HORIZON (hindsight) | **0,827–0,902** | 1,00 | R 0,82–0,88 | **0,0** | **0,930–0,967** | 1–3 mnt |

\* E1 per-fold AUPRC 0,134–0,666 di K-i; pada onset aggregate mean 0,113.

- Persistence-HORIZON (juga terekam di `v9_e_ML_stuck_k2_persistence_onset.json`: B1 1,00 di 4 sumur, TLead 9–10,5 mnt) = **hindsight**: label horizon `[t_e−10, t_e)` kontigu sehingga y(t−1) "tahu" isi horizon. Persistence-EVENT (deployable) B1 hanya 0–11,5%.
- ΔB layak: RF vs canary **4/4**, vs prevalensi 4/4, vs persistence-horizon **0/4**.
- **Kemampuan**: ranking in-horizon RF > canary/prevalensi di semua fold; ada 3 titik operasi FAR≤6 dengan lead 2–159 mnt (B1 kecil); persistence-event & E1 punya FAR rendah tapi recall onset ~0–6,6%.
- **Batas**: peringatan dini pada FAR praktis = **B1 2,7–4,5%** (jauh di bawah syarat alarm B1≥80%, D-A6); E2 tidak terbukti (CI memuat prev 4/4); LR menunjukkan B1 0,92–1,00 justru dengan FAR 329–1080 → ilustrasi pertukaran recall↔FAR, bukan keunggulan.
- **Belum terukur**: H sensitivitas 5/30 mnt; fold F-12 (STUCK_RT hanya depth-log).

### 2.5 `hyd` — K-i status (9 fold) + K-ii prediksi (1 split temporal)

**K-i:**

| Metrik | Persistence (engine) | Rule \|z\| (pembentuk label) | Hybrid | Canary | RF |
|---|---|---|---|---|---|
| AUPRC | 0,4245–0,8426 (mean 0,5555) | 0,462–0,835 (mean 0,575) | **0,436–0,849 (mean 0,6024)** | 0,081–0,512 | **DILARANG (D-A5)** |
| CI95 | lo min 0,2662 · hi max 0,9146 | — | — | — | — |
| P / R | 0,615–0,899 / 0,617–0,922 | 0,62–0,89 / 0,66–0,93 | **0,72–0,95 / 0,52–0,87** | — | — |
| FAR/24jam | 32,4–110,7 | 38,7–132,1 | **14,6–58,4** | — | — |
| FP total | 1941 | **2091** | **927** | — | — |
| Delay deteksi | median **0–3,5 mnt**; terdeteksi ≤H10: 31,6–65,4% | by construction (jendela label) | — | — | — |

- ΔB persistence vs prevalensi **9/9** (+0,306…+0,658); hybrid vs persistence **8/9** (F-9 −0,0172; mean +0,0469); hybrid memangkas FP vs rule **9/9** (mis. F-14 368→110) dan vs persistence 9/9.
- Rule \|z\| **TAUTOLOGI** (≡ definisi label; P=R=1,0 by construction; FAR definisional 325/24jam) → hanya dipakai sbg **ukuran beban alarm sistem hari-ini**, bukan pembanding keunggulan.
- **Kemampuan**: P/R ≥ 0,61 di 9/9 fold, ΔB 9/9, delay konfirmasi ≤3,5 mnt, hybrid menurunkan alarm palsu 56% (2091→927) tanpa kehilangan rank-quality (mean AUPRC naik 0,555→0,602).
- **Batas**: FAR 14,6–110,7/24jam di **9/9 fold** → belum memenuhi gerbang LAYER-1 (FAR≤6); jangan dipakai sbg alarm otomatis; label = residu (proxy), anotasi tetap wajib.

**K-ii:**

| Engine | AUPRC (CI95) | P / R @q95 | FAR/24jam | B1 / TLead | Status bukti |
|---|---|---|---|---|---|
| Fisher/Pearson **varian proxy** (dV_active/dt) | 0,022 [0,0025; 0,0684] — **memuat prev 0,0037** | **0,00 / 0,00** (FP 177) | 31,6 | 0/3 onset (underpowered) | sinyal tidak terbukti |
| Rule z-pit (sistem hari-ini) | 0,0056 (emp; prev 0,0037) | — | FP eval 0 (by construction) | **TLead=0 (10/10), B1=0%** | deteksi saat-kejadian, bukan prediksi |
| Selalu-negatif | 0,0037 | — | 0,0 | 0 | plafon bawah |
| **RF (angka V8, referensi)** | 0,2279 [0,009; 0,629] | P? (V8) | 5,9 | **B1 66,7% (2/3), TLead 7 mnt** | 1 wellbore, 3 onset (underpowered) |
| Fisher/Pearson **literal** (FlowIn−FlowOut) | **TIDAK BISA** — FlowOut absen (bukti: 4 kolom flow r=0,995–1,000) | — | — | — | kendala data, bukan kegagalan metode |

- **Kemampuan**: varian ranking di atas prevalensi (lift 5,95) pada 1 split; rule z-pit = baseline "sistem hari-ini" dgn beban inspeksi 1.348 menit-episode.
- **Batas**: pada titik operasi q95 → **P=R=0** (0 TP); 3 onset uji = underpowered utk klaim peringatan-dini; literal tidak bisa dijalankan (FlowOut absen); RF V8 belum diulang di V9 → kekuatan bukti = referensi.
- **Belum terukur**: jalur penuh F-1C/F-11 (GAINLOSSTOT 575/517 file belum diparse) → peluang penguatan.

### 2.6 `bit_wear` — K-1 status (7 fold) + K-2 onset (belum)

| Fold (USROP) | UP | prev | Persistence AUPRC (lift) | Canary AUPRC | ΔB(pers−canary) |
|---|---|---|---|---|---|
| F-9_Ad | **ya** (3 pos) | 0,0111 | 0,1185 (10,67) | 0,0177 | +0,1008 |
| F-7d | **ya** (0 pos) | 0,0000 | n/a (tak scorable) | n/a | — |
| F-14d | tidak | 0,0959 | 0,6792 (7,08) | 0,1913 | +0,4879 |
| F-15d | tidak | 0,1466 | 0,6979 (4,75) | 0,2880 | +0,4099 |
| F-15Sd | tidak | 0,5441 | 0,9837 (1,81) | 0,7555 | +0,2282 |
| F-5d | tidak | 0,4741 | 0,8703 (1,84) | 0,6915 | +0,1788 |
| F-9d | **ya** (0 pos) | 0,0000 | n/a | n/a | — |

- Mean AUPRC: persistence **0,670** vs canary **0,389**; persistence vs canary **5/5 fold scorable** (4/4 fold layak) → A-bekerja.
- **P/R/FAR tidak tersedia** di JSON (E_RULE/E_STAT tidak menghitung TP/FP utk kelas ini; PM1 §2.3 juga mencatat field tidak ada) → **Lapisan A P/R/FAR = BELUM TERUKUR** (bukan gagal). Untuk mengukur: run ulang persistence/rule dgn TP/FP/FN pada fold identik.
- **K-2 onset**: **belum terukur** — pra-reg belum terbit (E_RULE DoD-d). K-2 dilarang dipakai di tingkat apa pun sampai kampanye berangka (PM1 §2.3).

### 2.7 `tool_wear` — K-i regime (8 run) + K-ii lintas-alat (4 LOTO fold)

**K-i (change-point + kalibrasi):**

| Bagian | Hasil (angka eksekusi) | Interpretasi lapisan A |
|---|---|---|
| A. Change-point SSE + permutasi 500× | signifikan **8/8 run** pada p≤0,05 DAN p≤0,002 (Fisher literal); TP 4, FP 4 → **precision run 0,50**; recall 1,00 | deteksi perubahan-regime bekerja, **spesifisitas keausan tidak ada** (alat baru R01 juga 4/4 signifikan) |
| A2. Tes pembeda artefak termal | t_cp <5 dtk pada **0/8 run** | sub-klaim "cp = artefak termal" gugur → cp = transisi nyata |
| A3. TLead ke akhir R02 (alat tumpul) | median **35 dtk** (27–39) | waktu deteksi bengkel (detik, D-A7) |
| B. Kalibrasi within-tool (≥5/27 fitur \|z\|>3) | deteksi R02 **4/4**, TLead median 59 dtk (48–60), tapi **FAR 42,9–58,6/menit** di R01; kurangi_ragu vs rule-3RMS 0,0–0,25 | **tidak layak sbg detektor harian** pada ambang mentah |
| C. FAR-terkalibrasi (target 1,0 & 0,2/menit) | deteksi **4/4**, **FP 1–3/alat**, TLead **20–36 dtk**, % jendela R02 alarm 3,3–6,9 | **titik operasi praktis yang layak** |
| D. Ranking (skor 5/27) | AUPRC 0,5888 vs identity-majority 0,5117 → ΔB +0,077; lift 1,151 (plafon 1,954) | margin kecil tapi di atas baseline |

**K-ii (LOTO lintas-alat):**

| Baseline/engine | AUPRC | Catatan |
|---|---|---|
| Canary 3-RMS (V9) | 0,516–0,612 | pembanding relevan |
| Identity-majority (V9) | = prev 0,496–0,554 (plafon 2,0) | plafon ketat: lift maks 2,0 |
| Persistence (V9) | **N/A — dinyatakan** | label konstan dalam run (PM1 §2.7) |
| RF kontrak (angka V8, referensi) | 0,5433–0,7684; ΔB vs canary **4/4** (+0,027…+0,174); precision biner 0,50–0,56; FAR-terkalibrasi ≤1/menit: deteksi 4/4, TLead med 47,5 dtk, FP 1–3 | **V9 tidak menjalankan ulang** (E_ML 4 head) |

- **Kemampuan**: K-i memenuhi lapisan A pada FAR-terkalibrasi (deteksi 4/4 alat, FP 1–3, lead 20–36 dtk); ranking K-i di atas identity-majority; K-ii baseline V9 menegaskan plafon lift 2,0 sehingga margin RF V8 (+0,027…+0,174) memang kecil tapi konsisten 4/4.
- **Batas**: precision run-level 0,50 → klaim "deteksi progresi keausan" terduku lemah; domain bengkel terpisah (transfer ke rig TIDAK diklaim, D-A7); run-level n=8 = underpowered.

---

## 3. FP RULE UNTUK EVAL_B (B3: pengurangan pemeriksaan)

Dihitung dari JSON E_RULE (fold identik dgn engine utama):

| Kelas | FP rule (t0−1, total fold) | FP persistence | FP hybrid | FP E1 / catatan |
|---|---|---|---|---|
| vib | **197** | 1456 | 197 | — |
| ssi | **26** | 267 | 7 | n_nodata rule 22.385/35.906 |
| shk | **121** | 1056 | 121 | n_nodata 6.831 |
| stuck_k1 | **49** | 436 | 49 | E1: FP 160 (hybrid-E1 41) |
| hyd_ki | **2091** (tautologi = beban alarm) | 1941 | **927** | rule \|z\| = pembentuk label |
| stuck_k2 (onset) | — | persistence-event **11**, persistence-horizon **0** (hindsight) | — | E1 alarm FP **422** |
| hyd_kii | rule z-pit **FP eval 0** (by construction; 1.348 menit-episode) | selalu-negatif FP 0 | — | TLead=0, B1=0% |
| tool_wear | part B **42,9–58,6 FP/menit** (kalibrasi mentah) | — | — | part C FAR-terkalibrasi FP **1–3** (target 1,0 & 0,2/menit) |
| bit_wear | **belum terukur** (P/R/FAR tidak dihitung) | — | — | — |

Angka ini = input langsung B3 `kurangi_ragu = 1 − FP_engine/FP_baseline_rule` di EVAL_B.
Aturan: jangan hitung B3 utk hyd_ki memakai rule tautologi sbg "keunggulan" — pakai sbg beban alarm.

---

## 4. VERIFIKASI (verification-mandatory)

**Recompute dari mentah (DoD e — ≥1 metrik per kelas): 18/18 lolos** (selisih 0, atau ≤1e-3
utk nilai tersimpan yg dibulatkan 3–4 desimal):

| Kelas | Sumber | Metrik | Rumus recompute |
|---|---|---|---|
| vib | E_ML RF τ0,2 fold F-14 | precision + FAR | TP/(TP+FP); FP/(n_neg/60)·24 |
| ssi | E_RULE persistence fold F-10 | precision + FAR | idem |
| shk | E_RULE rule-display fold F-10 | precision + FAR | idem |
| stuck_k1 | E_RULE rule-display fold F-14 | recall | TP/(TP+FN) |
| stuck_k2 | E_ML RF τ0,3 + E_STAT E2 | precision, FAR (2 file) | idem |
| hyd_ki | E_STAT persistence + E_RULE hybrid | precision, FAR (2 konvensi) | idem |
| hyd_kii | E_STAT fisher varian | FAR | FP/(n_neg/60)·24 |
| bit_wear | E_RULE persistence fold 0 | lift | AUPRC/prevalensi |
| tool_wear | E_STAT cp + part D | precision run, lift | TP/(TP+FP); AUPRC/prev |

**Cross-check antar tim: 6/6 lolos** (selisih 0 atau ≤5e-7):
vib persistence AUPRC (ML `0,79588` == RULE `0,79588` validprev) · hyd_ki TP/FP (STAT `1223/138` == RULE `1223/138`) ·
stuck_k2 persistence-horizon AUPRC (ML `0,90159` == RULE `0,90159`) · hyd_K-ii n_episodes (`124` == crosscheck V8 `124`) ·
prev_test (`0,003701` == `0,0037005`) · hyd_ki fold0 persistence FP (`138` == `138`).

**Selisih yang ditemukan (dilaporkan, bukan disembunyikan):**

1. **E_RULE §(klaim hybrid hyd_ki) tidak tereproduksi persis.** Dokumen V9_E_RULE_ENGINE.md
   baris 183: "mengalahkan persistence di 9/9 fold (Δ +0,017…+0,391)". Recompute dari JSON
   primer E_RULE sendiri: **8/9 fold** (F-9: −0,0172), rentang Δ **−0,017…+0,092**;
   mean (0,602 > 0,555) dan pemangkasan FP 9/9 (F-14 368→110) **tereproduksi**.
   Evaluasi ini memakai angka recompute (8/9); selisih dikirim ke kartu E_RULE.
2. **Hitungan FAR≤1 E_ML vs EVAL_A.** E_ML handoff: FAR≤1 + recall>0 = 2 titik; recompute
   EVAL_A = **4 titik** (daftar: ssi RF F-10 τ0,3 FAR 0,21; shk RF F-14 τ0,3 FAR 0,69;
   stuck_k2 RF F-14 τ0,5 FAR 0,60; stuck_k2 RF F-9_A τ0,5 FAR 0,00).
   Hitungan FAR≤6 E_ML **persis tereproduksi: 10 titik** (recall 0,004–0,16 ✓).
   Definisi E_ML utk FAR≤1 tidak dinyatakan → selisih definisi, bukan angka salah.
3. **RF hyd_kii / bit_wear / tool_wear_kii tidak dijalankan di V9** → angka V8 dipakai sbg
   referensi (EA-7), dinyatakan terpisah di tabel.

**Ketiadaan error ≠ logika benar**: selain recompute, keabsahan logika dibuktikan lewat
cross-tim (angka identik dari pipeline berbeda) dan tes pembeda (persistence-horizon vs
-event; t_cp artefak 0/8; rule tautologi terdeteksi dari identitas jendela label
`n_mismatch=0` di 5 kelas).

---

## 5. BELUM DIVERIFIKASI / BELUM TERUKUR (verification-mandatory #3)

- **Belum terukur (bukan gagal)**: P/R/FAR bit_wear K-1 & K-2; B3/B4 semua kelas (EVAL_B);
  C1–C4 (EVAL_C); RF hyd_K-ii, RF bit_wear, RF tool_wear_K-ii versi V9; fold F-12 stuck
  (STUCK_RT depth-log); sensitivitas H=5/30 mnt; ordinal shk (S-B3); replikasi VIBLAT
  F-4/F-10/F-15.
- **Belum dicek evaluator ini**: kalibrasi ambang per well secara prospektif (D-A4 diuji di
  EVAL_C/C3); koreksi multipelitas diagnostik (semua tau dilaporkan, tanpa klaim signifikansi
  tunggal); kestabilan CI95 utk metode E_RULE (JSON E_RULE tidak menyimpan CI → C4 diuji di EVAL_C).
- **Keterbatasan bukti**: cakupan fold kecil pada stuck_k1 (2), bit_wear scorable (5/7),
  hyd_kii (1 split, 3 onset), tool_wear (4 alat, 8 run); prevalensi sangat berbeda antar fold
  (vib 0,14–0,57; ssi 0,003–0,065) sehingga AUPRC antar-fold tidak sebanding langsung —
  selalu bandingkan ke baseline pada fold yang sama (itulah gunanya ΔB).

---

## 6. RINGKASAN KEPUTUSAN TINGKAT PEMAKAIAN (masukan EVAL_C; bukan vonis final)

| Engine | Lapisan A terpenuhi untuk | Lapisan A belum terpenuhi untuk | Alasan angka |
|---|---|---|---|
| vib | deteksi/ranking status; penambah nilai vs canary/rule | alarm FAR≤6 lintas fold | titik praktis 1/20; rule FAR 10–50 |
| ssi | ranking vs semua baseline (fold layak); deteksi hemat-awas | deteksi andal per well; rule sbg detektor tunggal | CI memuat prev 5/9; rule R ≤0,03 |
| shk | lapisan dasar rule (7/9 fold FAR≤6 + R>0); ranking vs prevalensi | RF sbg alarm; A-bekerja vs persistence/rule | RF le6 1/45; ΔB 4/9 |
| stuck K-i | konfirmasi-status presisi 0,92–0,97 (2 fold) | FAR≤6; cakupan luas | FAR 8–61 & 75–538 |
| stuck K-ii | ranking in-horizon vs canary/prevalensi; triage | peringatan dini pada FAR praktis; klaim E2 | B1 2,7–4,5% @FAR≤6; CI memuat prev 4/4 |
| hyd K-i | deteksi kondisi (P/R ≥0,61; ΔB 9/9; delay ≤3,5 mnt); hybrid hemat FP | LAYER-1 (FAR>6 di 9/9) | FAR 14,6–110,7 |
| hyd K-ii | ranking di atas prevalensi (signifikansi tidak terbukti) | deteksi/prediksi pada titik operasi | P=R=0 @q95; 3 onset |
| bit_wear K-1 | ranking status vs canary/prevalensi (5/5 scorable) | P/R/FAR (belum terukur); K-2 | field TP/FP tidak ada |
| tool_wear K-i | deteksi regime pada FAR-terkalibrasi (FP 1–3, lead 20–36 dtk) | klaim spesifisitas keausan; kalibrasi mentah | precision run 0,50; FAR mentah 43–59/menit |
| tool_wear K-ii | ranking margin kecil di atas canary (basis V9 + angka V8) | alarm (precision ≈ peluang); re-run V9 | plafon lift 2,0; RF V9 belum jalan |

Sumber: `scratch/v9_eval_a/v9_eval_a_RESULTS.json` (primer), `v9_eval_a_SUMMARY.txt` (log).
Dihitung: 2026-10-12, skrip EVAL_A (recompute 18/18, cross-team 6/6, sequ 5/5).
