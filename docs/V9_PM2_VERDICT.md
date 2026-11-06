# V9-PM2 — VONIS AKHIR: KEPATUHAN SELURUH PIPELINE PADA "Evaluasi User.txt"

Task: `t_07d88981` [PM · System Architect · Technical Lead] · Board: capstone-v9-build · 2026-10-12 (WIB)
Status: VONIS FINAL — **tanpa target baru yang digubah**; yang dinilai = kepatuhan kerangka A/B/C,
bukan pencapaian angka. Semua angka di dokumen ini = kutipan hasil recompute PM2 dari JSON primer
atau hasil re-run verifikasi (bukti di §2, §4).

> **Riset pendahuluan: `scientific-critical-thinking`** — klaim "seluruh pipeline memenuhi
> user.txt" diperlakukan sbg hipotesis yg diuji poin-per-poin (a–e) dgn bukti angka, bukan
> ringkasan naratif; OBSERVED (recompute PM2) dipisah dari DERIVED (sintesis tier) dan
> BELUM-TERUKUR (daftar §7); temuan audit A1 dikonfirmasi ulang, tidak ditelan mentah.
> **Riset pendahuluan: `verification-mandatory`** — 5 verifikasi terminal independen dari JSON
> primer (§2) + re-run `code/v9_i1_verify.py` (13/13 PASS, exit 0) + scan regex mandiri
> LULUS/GAGAL dan lift 1,5 (§3); koreksi penyajian DILAKUKAN langsung di dokumen tim
> (change-control PM, §2.3) — bukan sekadar dilaporkan; daftar belum-diverifikasi §7.
> **Riset pendahuluan: `statistical-analysis`** — perbandingan memakai ΔB pada fold yang sama
> (bukan AUPRC mentah antar-well dgn prevalensi beda 40×); FAR dibaca pada skala aslinya
> (jendela/24jam rig vs menit bengkel — dilarang diseragamkan); fold UNDERPOWERED (<30 positif)
> dilabeli dan tidak dihitung mayoritas; selisih pembulatan (119,6× vs "119×") dilaporkan apa
> adanya, bukan diganti.
> **Riset pendahuluan: `what-if-oracle`** — 5 cabang Ω/α/Δ/Ψ/Φ diuji untuk menekan keputusan
> vonis (§5): apakah temuan minor menurunkan vonis? Hanya cabang α yang terdukung bukti →
> koreksi langsung + LAYAK; cabang Δ/Ψ/Φ tidak terdukung data.
> **Riset pendahuluan: `consciousness-council`** — 5 arketipe (Empiricist, Contrarian,
> Pragmatist, Architect, Historian) menekan vonis (§5.2); ketegangan "cepat LAYAK" vs "jujur
> soal bukti" dipertahankan → diresolusi dgn koreksi faktual, bukan penurunan standar.
> **Riset pendahuluan: `sequentialthinking`** (5 pikiran, 5/5 sukses, tool_call sequ-mcp):
> rencana → sintesis bukti recompute → what-if vonis → council → gerbang akhir sebelum dokumen.

---

## 0. RINGKAS VONIS

**VONIS: LAYAK.**
Seluruh pipeline V9 **memenuhi kerangka evaluasi operator ("Evaluasi User.txt")** pada tingkat
alat PdM: 7 engine dinilai di 3 lapisan A/B/C (bukan gate biner), tiap engine punya baseline
relevan + kemampuan/batas/kekuatan bukti, jenis tugas dibedakan, dan nilai dinilai di tingkat
alat (tier pemakaian per head + lapisan keputusan), bukan dari jumlah model lolos gate.

Vonis ini **tanpa menggeser ambang apa pun** dan **tanpa target baru**: G1/G2 tetap hanya syarat
ambang-atas alarm-otomatis; 0 engine dinaikkan tier; "belum terukur" tetap terpisah dari "cukup".

Temuan yang harus (dan sudah) diselesaikan sebelum vonis dikeluarkan:

| # | Temuan | Asal | Status akhir |
|---|---|---|---|
| 1 | EVAL_A §1/§2.4 B1 stuck K-ii RF τ0,5 menulis "0,027–0,045" (fold F-9 = 0,000 dibuang) | A1 §7.1, dikonfirmasi recompute PM2 | **DIKOREKSI** di `V9_EVAL_A_LAYERA.md` (2 tempat) → "0,000–0,045 (3 fold FAR≤6: 0,027–0,045)" |
| 2 | E_RULE §2.5 "hibrida hyd mengalahkan persistence 9/9 fold (Δ +0,017…+0,391)" — recompute = **8/9** (Δ −0,0172…+0,0917) | EVAL_A §4; dikonfirmasi recompute PM2 | **DIKOREKSI** di `V9_E_RULE_ENGINE.md` (klaim FP-cut 9/9 tetap — terverifikasi) |
| 3 | EVAL_C ssi "hybrid FP-cut 73,1% konsisten 7/7" imprecise (memotong 6/7 layak; F-14 tie) | A1 §7.2; dikonfirmasi recompute PM2 | **DIKOREKSI** di `V9_EVAL_C_LAYERC.md` (2 tempat) + `V9_I1_INTEGRATION.md` (badge) |
| 4 | `V9_D1_DATA_PIPELINE.md` tanpa baris riset WIO/CC/SEQ | A1 §7.4 | **DICATAT** (pelanggaran prosedural rendah) + catatan jujur ditambahkan di D1; TIDAK direkayasa retroaktif |

Tidak ada temuan yang mengubah tier engine mana pun; tidak ada angka dasar yang berubah.

---

## a. KEPAATIHAN SKILL PER TIM

Kewajiban PM1 §4.0.5: baris `Riset pendahuluan: <skill> — <poin>` per dokumen; `sequentialthinking`
≥3 pikiran; agentmemory fakta tahan-lama; skill minimum SCT/VM/SA (+WIO/CC/SEQ utk PM).

| Tim / dokumen | Baris riset | Skill tercatat | sequ-mcp | agentmemory | Status |
|---|---|---|---|---|---|
| PM1 `V9_PM1_ARCHITECTURE` | ✓ | SCT, VM, SA, WIO, CC, SEQ | ✓ 5 pikiran | ✓ | PATUH |
| R&D `V9_R1_JUSTIFICATION` | ✓ | + literature-review, paper-lookup, grounded-citations, hypothesis-generation (10) | ✓ 5 pikiran | ✓ | PATUH |
| Data Eng `V9_D1_DATA_PIPELINE` | ✓ (3 baris) | SCT, VM, SA saja | **TIDAK ADA** | — | **PELANGGARAN** (WIO/CC/SEQ tidak dicatat) |
| Alg ML `V9_E_ML_ENGINE` | ✓ | SCT, SA, VM, WIO, CC, SEQ | ✓ 3 pikiran | ✓ (mem_mv4mbdf4) | PATUH |
| Alg Stat `V9_E_STAT_ENGINE` | ✓ | SCT, VM, SA, WIO, CC, SEQ | ✓ 4 pikiran | ✓ | PATUH |
| Alg Rule `V9_E_RULE_ENGINE` | ✓ (7 baris) | SCT, VM (klaim-batas), SA, WIO, CC, SEQ | ✓ 6 pikiran | ✓ (mem_mv4ofv21, mem_mv4ofvfr) | PATUH |
| Evaluator A `V9_EVAL_A_LAYERA` | ✓ | SCT, VM, SA, WIO, CC, SEQ | ✓ 5 pikiran | ✓ | PATUH |
| Evaluator B `V9_EVAL_B_LAYERB` | ✓ | SCT, VM, SA, WIO, CC, SEQ | ✓ 4 pikiran | ✓ | PATUH |
| Evaluator C `V9_EVAL_C_LAYERC` | ✓ | SCT, VM, SA, WIO, CC, SEQ | ✓ 4 pikiran | ✓ (mem_mv4sbvzc) | PATUH |
| Integration `V9_I1_INTEGRATION` | ✓ | SCT, VM, SA, WIO, CC, SEQ | ✓ 4 pikiran | ✓ (mem_mv4tkkju) | PATUH |
| Auditor `V9_A1_AUDIT` | ✓ | + peer-review (7) | ✓ 4 pikiran | ✓ (mem_mv4whjce) | PATUH |
| **PM2 (dokumen ini)** | ✓ | SCT, VM, SA, WIO, CC, SEQ | ✓ 5 pikiran | ✓ (§8) | PATUH |

**Pelanggaran: 1 dari 12 dokumen (D1).** Tindakan: catatan jujur ditambahkan ke D1 (bukan baris
riset palsu); kewajiban baris riset WIO/CC/SEQ berlaku lagi untuk dokumen D1 berikutnya.
Dampak ke substansi = nol: seluruh angka D1 diverifikasi ulang independen oleh A1 §6.3
(0 pelanggaran anti-bocor di 6 dataset, termasuk stuck_k2 118.567 baris).

Sumber: pembacaan langsung 11/11 dokumen `docs/V9_*.md` + grep mandiri PM2 (136 baris riset).

## b. POTENSIAL HERMES (tool yang tersedia vs yang dipakai)

| Tool | Dipakai oleh | Catatan |
|---|---|---|
| `read_file` / `patch` / `write_file` | semua tim | wajib, dipenuhi |
| `terminal` / `execute_code` (eksekusi nyata) | semua tim + A1 + PM2 | 15+ skrip; JSON primer sebelum dokumen (S6) |
| `skill_view` (skill sci) | semua tim | 6 skill wajib terpakai (tabel §a) |
| sequ-mcp (`sequentialthinking`) | 11/12 dokumen | D1 = 1 pelanggaran |
| agentmemory (`memory_save`) | semua tim | id `mem_…` tercatat di handoff/§a |
| `session_search` | PM2 | riwayat kegagalan/keputusan kartu V9 dicek (§7) |
| `web_search` / `web_extract` | R1 | 27 sitasi diverifikasi 3 jalur (OpenAlex/Crossref/doi.org), 5 kandidat ditolak |
| kanban (komentar/handoff) | semua tim | temuan EVAL_A→E_RULE dikirim via kartu |

**Underuse (dilaporkan, bukan dijadikan target baru):**
1. `delegate_task` — tidak dipakai untuk paralelisasi di dalam satu kartu (paralelisme antar-kartu
   sudah lewat kanban) → dampak rendah.
2. `todo` tool — checklist eksekusi tidak dipakai; verifikasi dilakukan lewat tabel acceptance di
   dokumen masing-masing → dampak rendah.
3. Browser/vision — prototipe I1 diuji lewat log teks + JSON, tanpa tangkapan antarmuka → tidak
   diminta DoD; dicatat sbg peluang bila Tahap 2a membangun UI.
Tidak ada underuse yang memengaruhi validitas angka atau kepatuhan kerangka.

## c. KONSISTENSI ANGKA ANTAR LAPORAN

### c.1 Verifikasi independen PM2 (terminal → JSON primer; recompute sendiri, bukan kutipan)

| # | Klaim yang diuji | Sumber primer | Hasil recompute PM2 |
|---|---|---|---|
| 1 | hyd K-i hybrid: FP 2.091→927; ΔB vs persistence berapa fold? | `scratch/v9_e_rule/v9_e_RULE_01_status_results.json` | **FP 2091→927 EXAK**; ΔB hybrid−persistence = **8/9 fold** (F-9 −0,0172; rentang −0,0172…+0,0917) → EVAL_A benar, E_RULE keliru → dikoreksi |
| 2 | ssi hybrid: "konsisten 7/7 fold"? | idem, kelas `ssi` | **< rule 6/9, = rule 3/9 (F-14, F-7, F-9), 0 lebih buruk**; fold layak 7 = 6 cut + F-14 tie; FP total 26→7 (**−73,1%** EXAK) → EVAL_C phrasing dikoreksi |
| 3 | stuck K-ii RF τ0,5 B1 per fold (kontradiksi EVAL_A vs EVAL_B) | `scratch/v9_e_ml/v9_e_ML_stuck_k2_RESULTS.json` | F-10 0,0448 · F-14 0,0357 · **F-9 0,0000** · F-9_A 0,0270 → rentang penuh **0,000–0,0448**; subset FAR≤6 = **0,0270–0,0448** → EVAL_B benar, EVAL_A tabel dikoreksi; narasi EVAL_A ("2,7–4,5% di titik FAR≤6") tetap benar |
| 4 | vib RF τ0,5 FAR menyebar "119×"? | `scratch/v9_e_ml/v9_e_ML_vib_RESULTS.json` | FAR 4,15–496,09 → rasio **119,6×** → "119×" EVAL_C dapat diterima (catatan A1 120× = beda pembulatan; kesimpulan "tidak portabel" tak berubah) |
| 5 | Arsitektur I1: tier tak dinaikkan, 0 alarm, human-in-loop | re-run `python3 code/v9_i1_verify.py` | **13/13 PASS, exit 0** (V2 27 head tanpa kenaikan tier; V3b slot alarm 0; V4b 11/11 L1 human review; V5 6/6 recompute; V9/V10 konsistensi kampanye) |

### c.2 Konsistensi silang yang sudah diverifikasi (A1 + PM2)

| Pasangan | Angka kunci | Status |
|---|---|---|
| E_RULE ↔ EVAL_A | FP rule 197/26/121/49/2091; FP hybrid hyd 927 | ✓ identik |
| EVAL_A ↔ EVAL_B | B3 dari FP mentah (8 titik: −6,391 · +0,731 · +0,678 · +0,557 · +0,163 · +0,974 · +0,909 · +0,976) | ✓ 8/8 (A1 #24, selisih <0,002) |
| E_STAT ↔ E_RULE | hyd persistence FP 1941; determinisme 4/4 JSON | ✓ |
| EVAL_C ↔ EVAL_A | CI ssi 3/7 layak vs 5/9 all-fold (denominator dinyatakan) | ✓ direkonsiliasi EC-3 |
| I1 ↔ E_RULE/E_STAT | replay F-14 == fold kampanye (10/10); tool_wear 4/4 alat | ✓ (re-run PM2: V9/V10 PASS) |
| E_ML ↔ V8 (baseline) | vib RF lift 1,61/2,36/3,50/1,63 reproduksi persis | ✓ |
| **Selisih ditemukan** | 3 temuan tabel §0 + catatan definisi "FAR≤1: 4 titik (EVAL_A) vs FAR≤6: 10 titik (E_ML)" = **beda definisi, bukan kontradiksi** (A1 #2) | ✓ sudah diselesaikan/dikoreksi |

Rekap: A1 menghitung ulang **27 kelompok klaim (26 terverifikasi)**; PM2 menghitung ulang
**5 kelompok secara independen — semuanya konsisten dgn A1**; 0 kontradiksi baru.

## d. VERIFIKASI KEPAatuHAN user.txt — POIN PER POIN

| Poin | Pertanyaan operator | Hasil | Bukti |
|---|---|---|---|
| **(a)** | Tiap engine dinilai A/B/C, bukan gate biner? | **TERPENUHI** | EVAL_A/EVAL_B/EVAL_C masing-masing menilai **11 klaim = 7 engine** (klaim ganda stuck/hyd/bit_wear/tool_wear dipisah). Scan mandiri PM2: 14 kemunculan uppercase `LULUS/GAGAL` = **semuanya negasi/sub-klaim** ("BUKAN vonis LULUS/GAGAL", "spesifisitas cp GAGAL", dst) — 0 vonis biner. Scan `lift 1,5`: semua penyebutan = penolakan eksplisit / syarat ambang-atas alarm beranotasi (PM1 §0.4, §1.3) — **0 gate lift 1,5 terselubung**. |
| **(b)** | Tiap engine punya baseline relevan (bukan satu baseline universal)? | **TERPENUHI** | R1 §4.1: baseline berbeda per tugas (persistence/canary-depth/prevalence-random/rule status-quo/anchor kelas/identity-majority/persistence-N/A dinyatakan); semua dihitung E_RULE pada fold identik (37 rig + 7 bit_wear + 4 tool_wear + 1 split); A1 §4.1 = 0 baseline universal dipaksakan; recompute PM2 #1/#2 memakai fold identik. |
| **(c)** | Tiap engine punya kemampuan + batas penggunaan + kekuatan bukti? | **TERPENUHI** | Setiap tabel engine di EVAL_A/B/C + 3 dokumen E_* memuat kolom kemampuan/batas/bukti; A1 §2 memeriksa setiap klaim "memenuhi/layak" → **0 klaim berlebihan material**; 5 entri "belum terukur" diberi alasan mekanis (field TP/FP tak ada, pra-reg belum terbit, RF V9 tak dijalankan, pembagi nol) — terpisah dari "gagal". |
| **(d)** | Jenis tugas dibedakan (deteksi anomali / deteksi kondisi / diagnosis / prediksi kejadian)? | **TERPENUHI** | R1 §2 peta 11 klaim ↔ tugas: **0 kasus salah-framing**; kelas status memakai B4 margin (bukan TLead/B1); kelas onset memakai B1/TLead vs anchor kelasnya sendiri; tool_wear bengkel (detik) tidak digabung lead rig (menit) — D-A7; persistence-HORIZON dilabeli HINDSIGHT dan tidak dipakai sbg bukti deployable. |
| **(e)** | Nilai di tingkat alat PdM menyeluruh, bukan jumlah model lolos gate? | **TERPENUHI** | EVAL_C menetapkan **tier pemakaian per engine** (TREN / PERINGATAN-BERPENGAWAS / BELUM LAYAK PAKAI; 0 ALARM-OTOMATIS); I1 merakitnya jadi alat: **5 head L0 + 11 L1 (human-in-loop) + 9 L2 + 2 L3, slot alarm otomatis = 0**, badge FAR + label keyakinan + batas tertulis per head; vonis PM2 = tingkat pemakaian alat (§e), bukan jumlah model lolos. |

**Bonus — 3(4) pertanyaan rumusan masalah proposal §3 (PM1 §4.11 DoD-b; proposal memuat 4
pertanyaan, PM1 menyebut 3 — dijawab semuanya):**
1. *Jenis kegagalan BHA mana yang terdeteksi & seberapa andal?* — 7 engine / 11 klaim: vib, ssi,
   shk, stuck K-i/K-ii, hyd K-i/K-ii, bit_wear K-1/K-2, tool_wear K-i/K-ii; lapisan A per klaim
   (EVAL_A §1): rule shk lolos FAR≤6 di 7/9 well, hyd hybrid P/R ≥0,61 di 9/9, stuck K-i P
   0,92–0,97 (2 well), bit_wear/hyd K-ii = belum terukur/belum layak pada titik operasi.
2. *Metode apa paling cocok per kegagalan?* — hybrid-per-tugas (R1 §2 + hasil): persistence =
   engine status terbaik terukur (hyd/bit_wear), rule = lapisan dasar berbiaya-terkendali
   (shk/vib/stuck), statistik = label & change-point (hyd K-i, tool_wear), ML = ranking/onset bila
   ΔB>0 (vib/ssi/shk/stuck K-ii), RF **dilarang** di hyd K-i (ΔB− 7/7) = metode dipilih per tugas.
3. *Seberapa tepercaya & pada tingkat apa (tren/peringatan/alarm)?* — tier EVAL_C per engine
   (§e di bawah): TREN 7 klaim, PERINGATAN-BERPENGAWAS 6 klaim, BELUM LAYAK 1 klaim,
   **alarm otomatis 0** — dengan syarat naik tier terukur (EVAL_C §4).
4. *Bagaimana memisahkan klaim berbukti dari klaim berlebihan?* — 3 lapis: pra-reg + JSON primer
   (S3/S6), recompute silang antar tim (EVAL_A 18/18 + 6/6), audit independen A1 (27 kelompok,
   retrain 24/24) + koreksi PM2 (§0) — klaim tanpa angka otomatis jatuh ke "belum terukur".

## e. VONIS + RINGKAS ALAT (tingkat pemakaian per engine — bukan vonis biner)

**VONIS: LAYAK** — alat PdM advisory koheren, jujur soal bukti, siap dipakai pada tingkat yang
terukur; 0 bagian diklaim melebihi buktinya.

Ringkasan alat (kutipan EVAL_C §1 + EVAL_A/B; tier TIDAK diubah PM2):

| # | Engine | Jenis tugas | Tier pemakaian (tingkat pakai) | Bukti inti | Batas pemakaian tertulis |
|---|---|---|---|---|---|
| 1 | **vib** | deteksi kondisi | **TREN** (RF ranking) + **PERINGATAN-BERPENGAWAS** (rule) | rule P 0,87–0,95 (4 well); RF ΔB vs canary 4/4; CI RF 0/4 memuat prev | jangan ambang global (FAR τ0,5 menyebar 119,6×); FAR rule 10–50/24jam; tanpa klaim lead-time |
| 2 | **ssi** | deteksi kondisi | **TREN** (RF) + **PERINGATAN hemat** (hybrid FP −73,1%) | RF > semua baseline di fold layak (7/7 vs prev); hybrid ≤ rule 7/7 | nodata CRPM 62,3% (F-14 96,6%); CI memuat prev 5/9; recall rule ≤0,03 |
| 3 | **shk** | deteksi anomali | **PERINGATAN-BERPENGAWAS** (rule) + **TREN** (RF) | rule FAR≤6 dgn recall>0 di **7/9 well** (satu-satunya kelas rig mayoritas) | RF: CI 7/9 memuat prev, B3 −212× → jangan sbg alarm; kalibrasi lintas-well dilarang |
| 4 | **stuck K-i** | deteksi kondisi | **PERINGATAN-BERPENGAWAS** (2 well) | rule P 0,92–0,97 konsisten | cakupan 2 fold saja; FAR 8–61 → belum ≤6 |
| 5 | **stuck K-ii** | prediksi onset | **TREN / triage** | RF ranking > canary 4/4; persistence-EVENT TLead 7,0 mnt ≈ anchor 2,67–7,37, FP 11 | B1 0–11,5% (jauh dari 80%); titik B1≥50% berbiaya 77×; semantik label = pra-reg Fase 0 |
| 6 | **hyd K-i** | deteksi kondisi | **PERINGATAN-BERPENGAWAS (kandidat terkuat)** | hybrid FP −55,7% (2091→927) 9/9 well, P/R ≥0,52, CI persistence 0/9 memuat prev, delay ≤3,5 mnt | FAR 14,6–58,4 >6 di 9/9 → belum L1 penuh/apalagi alarm; label = residu (proxy) |
| 7 | **hyd K-ii** | prediksi kegagalan | **BELUM LAYAK PAKAI (eksplorasi)** | V9: P=R=0 @q95, CI memuat prev, sign-flip 78,7% | kendala sensor terukur (FlowOut absen); RF V8 (B1 66,7%) = referensi belum diulang |
| 8 | **bit_wear K-1** | deteksi kondisi | **TREN** | persistence ΔB vs canary 5/5 scorable (AUPRC mean 0,670 vs 0,389) | P/R/FAR **belum terukur** (field tak ada); USROP ≠ Volve |
| 9 | **bit_wear K-2** | prediksi onset | **BELUM (belum dijalankan)** | nol angka — pra-reg belum terbit | dilarang dipakai di tingkat apa pun s/d kampanye berangka |
| 10 | **tool_wear K-i** | deteksi perubahan-regime | **PERINGATAN-BERPENGAWAS (bengkel)** | FAR-terkalibrasi: deteksi 4/4 alat, FP 1–3, lead 20–36 dtk, B3 +0,91…+0,98 | precision run 0,50 (spesifisitas keausan lemah); skala detik bengkel; transfer ke rig TIDAK diklaim |
| 11 | **tool_wear K-ii** | klasifikasi lintas-alat | **TREN** | baseline LOTO stabil (canary 1,19×); RF V8 ΔB 4/4 = referensi | RF V9 belum dijalankan; precision ≈ peluang → jangan alarm |

Komposisi alat hasil perakitan I1 (re-run verifikasi PM2): **L0 = 5 head · L1 = 11 head
(human_review_required) · L2 = 9 head · L3 = 2 head · slot ALARM OTOMATIS = 0 · keputusan
akhir = MANUSIA.**

**Langkah lanjut (syarat yang SUDAH terdaftar — bukan target baru):**
1. Kampanye penguatan: parse VIBLAT F-4/F-10/F-15 (buka FAR/B4 vib), S-E1 re-run 11 fold ssi,
   join trajectory F-12 (fold stuck tambahan), parse GAINLOSSTOT F-1C/F-11 (buka hyd K-ii),
   TP/FP bit_wear K-1 (run ulang dgn metrik), re-run RF hyd-K-ii & tool_wear K-ii versi V9.
2. Pra-reg Fase 0 (gerbang keras, sudah di PM1 §6.2): kunci satu varian onset stuck
   strict-vs-ffill, verifikasi semantik skala 0/1/2/3 STUCK_RT/SHKRSK_RT lintas-well, rekonsiliasi
   prev stuck 66,9% vs 49,4%, sinkronisasi zona-waktu kontrol-positif (tripwire §5.1).
3. Kalibrasi ambang per-well prospektif (D-A4) = syarat utama naik tier hyd K-i & vib/shk RF
   ke L1 penuh (EVAL_C §4) — diukur, bukan diasumsikan.
4. K-2 bit_wear hanya setelah kampanye pra-reg terbit; alarm otomatis (Tahap 3a proposal) hanya
   setelah FAR≤1/24jam + B1≥80% + C2/C3 terukur (PM1 §1.3 — ambang tidak digeser).
5. Prosedural: dokumen D1 berikutnya wajib mencantumkan baris riset WIO/CC/SEQ (pelanggaran §a).

## f. CEK ARSITEKTUR (prototipe I1: batas pemakaian + keputusan manusia)

| Syarat (PM1 §4.9) | Bukti | Status |
|---|---|---|
| Prototipe jalan pada data nyata | replay F-14 + USROP + 4 alat bengkel; JSON 45.879 byte; run 21,55 dtk | ✓ |
| Tier tidak dinaikkan I1 sendiri | cek V2 (re-run PM2): 27 head, 0 kenaikan tier | ✓ |
| 0 komponen menampilkan "alarm kritis" | V3a/V3b: 0 head ALARM-OTOMATIS, slot 0 (assert di kode) | ✓ |
| L1 hanya utk engine lolos syarat §1.3 | V4a: 0 pelanggaran aturan lapisan; engine TREN/BELUM tak pernah ke L1 | ✓ |
| Keputusan manusia dipertahankan | V4b: 11/11 L1 `human_review_required=true`; `keputusan_akhir=MANUSIA` | ✓ |
| Badge FAR + keyakinan + batas tampil | V1b: 0 head tanpa tier/layer/badge/keyakinan/batas | ✓ |
| Status non-aktif eksplisit (bukan 0 diam) | V6: hyd K-ii & bit_wear K-2 status kata, tanpa metrik palsu | ✓ |
| Konsistensi kampanye | V9 (tool_wear 4/4 alat) + V10 (F-14 == fold E_RULE 10/10) | ✓ |

Re-run penuh oleh PM2: `python3 code/v9_i1_verify.py` → **13/13 PASS, exit 0**.

## g. WHAT-IF-ORACLE + CONSCIOUSNESS-COUNCIL (dasar vonis)

### g.1 5 cabang
| Cabang | Bobot | Skenario | Hasil uji |
|---|---|---|---|
| Ω Best | 15% | temuan A1 tak berefek; semua angka eksak | Terjadi untuk 23/27 klaim — tapi 3 temuan nyata → tak cukup utk LAYAK bersih tanpa koreksi |
| **α Likely** | **55%** | 3 temuan = penyajian; koreksi langsung → LAYAK dgn catatan | **DIPILIH** — koreksi diterapkan (§0), tier tak berubah, vonis LAYAK |
| Δ Worst | 10% | kontradiksi lebih luas dari temuan A1 | **TIDAK terdukung** — recompute PM2 (5 klaim) + A1 (27 klaim) = 0 temuan baru |
| Ψ Wildcard | 10% | pelanggaran skill D1 = tanda kerja procedural rusak | **TIDAK terdukung** — angka D1 lolos verifikasi anti-bocor independen (A1 §6.3); user.txt tidak menuntut skill |
| Φ Contrarian | 10% | "0 alarm otomatis" = alat gagal | **DITOLAK** — user.txt eksplisit: "layak tren tapi belum alarm = keputusan wajar, bukan kegagalan"; alarm = Tahap 3a dgn syarat terukur |

Robust lintas cabang: koreksi penyajian + catatan pelanggaran + vonis berbasis bukti.
Tripwire: bila patch PM2 mengubah angka lain → recompute ulang (dilakukan: 6 patch, 0 angka dasar berubah).

### g.2 Council (5 arketipe)
- **Empiricist**: angka NYATA (recompute 26/27 A1 + 5/5 PM2) → tak ada dasar menurunkan tier.
- **Contrarian**: "LAYAK" berisiko vonis malas → diuji poin a–e dgn bukti tabel §d; kontra-argumen
  lemah karena tiap poin punya artefak + angka.
- **Pragmatist**: alat hari ini bernilai di L0+L2 tanpa menunggu kampanye; 3 patch kecil tak boleh
  menahan serah-terima.
- **Architect**: patch = change-control PM (PM1 §6.5) — menyesuaikan dokumen ke hasil recompute,
  BUKAN menggeser ambang; menambah baris riset D1 retroaktif = fabrication → ditolak.
- **Historian**: pola V8→V9 konsisten (persistence dominan kelas status, B3 shk negatif berulang) →
  tidak ada regresi metode diam-diam.

**Sintesis**: konvergensi 5/5 = **LAYAK + 3 koreksi penyajian + 1 pelanggaran skill tercatat**;
ketegangan yang dipertahankan (bukan dihapus): "belum terukur" ≠ "cukup", dan 0 alarm otomatis
tetap keputusan desain, bukan kegagalan.

## h. BELUM DIVERIFIKASI / DI LUAR RENTANG PM2 (verification-mandatory #3)

1. Bootstrap CI95 1.000× per fold tidak dihitung ulang PM2 (A1 juga tidak — mahal); keaslian skor
   dibuktikan lewat retrain identik (A1 §6.2, diff 0,00e+00).
2. B4 EVAL_B tidak dihitung ulang ulang penuh PM2 (A1 §8.2 merekomendasikan 1 kelas acak pada
   tahap berikutnya bila ingin bukti penuh).
3. Rantai WITSML→bins tidak diulang (data primer D1 dipakai sbg dasar; sha256 + crosscheck V6 =
   batas bukti saat ini).
4. Asal kalender `ts_bin` tetap tak diverifikasi (I1 & A1 sama) — tidak ada klaim tanggal di
   dokumen mana pun → tak ada pelanggaran.
5. 5 kelompok klaim yang direcompute PM2 dipilih purposif (4 temuan A1 + arsitektur I1) — bukan
   sampel acak dari 27; sisa klaim mengikuti recompute A1.

---
Skrip verifikasi PM2: `~/.hermes/cache/scratch/pm2_verify.py` (5 kelompok recompute dari JSON primer).
Koreksi yang diterapkan: `V9_EVAL_A_LAYERA.md` (2), `V9_E_RULE_ENGINE.md` (1),
`V9_EVAL_C_LAYERC.md` (2), `V9_I1_INTEGRATION.md` (1), `V9_D1_DATA_PIPELINE.md` (catatan pelanggaran).
Diakhiri: 2026-10-12 (WIB) — V9-PM2 (`t_07d88981`). **VONIS: LAYAK.**
