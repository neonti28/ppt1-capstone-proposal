# V9-E_STAT — ENGINE STATISTIK: hyd-K-i · stuck-E2 · tool_wear-K-i · Fisher/Pearson (hyd K-ii baseline)

Task: `t_af8ea271` [Algorithm Engineer Statistik] · Board: capstone-v9-build · 2026-10-12 (WIB)
Status: SELESAI — 4 skrip berjalan pada data nyata, JSON primer tersimpan DULU di
`scratch/v9_e_stat/`, semua angka dokumen ini = kutipan dari JSON (S6).
Sumbu: `docs/V9_PM1_ARCHITECTURE.md` §2.4/§2.5/§2.7 + DoD §4.4 · `docs/V9_R1_JUSTIFICATION.md`
§3.4/§3.5/§3.7/§4.1/§4.5 · `docs/V9_D1_DATA_PIPELINE.md` (dataset + LOWO).
Kerangka penilaian: standar 3 lapisan A/B/C operator ("Evaluasi User.txt") — BUKAN gate lift 1,5.

> **Riset pendahuluan: `scientific-critical-thinking`** — tiap klaim dipisah OBSERVED
> (angka JSON eksekusi sesi ini) vs INTERPRETASI (makna persistence-onset, sirkularitas
> rule-|z| hyd) vs BELUM-TERUKUR (§8); tes pembeda dijalankan dan hasil NEGATIF dilaporkan
> apa adanya (spesifisitas change-point GAGAL; Fisher/Pearson 0 TP); hipotesis "label
> dataset bisa jadi duplikasi salah" diuji lewat recompute independen dari bins → 0 mismatch.
> **Riset pendahuluan: `verification-mandatory`** — label hyd dihitung ULANG dari sumber
> kedua (bins/) dan dibandingkan row-level (0/52.509 beda; y_prev 0/45.758 beda pada pasangan
> yang tersedia); run-count onset stuck21cocok persis dengan D1 (93/61/55/72); label hyd K-ii
> reproduksi persis V8 (124 episode = 39 kick/85 loss, prev_test 0,0037); determinisme diverifikasi
> dengan re-run penuh (4/4 JSON IDENTIK, hanya `elapsed_s` yang dibuang); daftar belum-diverifikasi §8.
> **Riset pendahuluan: `statistical-analysis`** — baseline RELEVAN per tugas (tidak ada baseline
> universal): persistence/prevalence/rule-|z| untuk hyd-K-i; persistence-onset/prevalence untuk
> stuck-E2; rule 3-RMS/identity-majority/persistence-N/A untuk tool_wear; prevalence/rule z-pit
> untuk hyd K-ii. Plafon lift 1/prev dilaporkan tiap fold; CI95 moving-block bootstrap (blok 60,
> 1.000, seed 42); <30 positif = UNDERPOWERED dilabeli; FAR per skala aslinya (jendela/24jam-neg,
> alarm/menit) — perbandingan lintas-kelas tanpa konversi dilarang.
> **Riset pendahuluan: `what-if-oracle`** — 5 cabang risiko eksekusi (Ω/α/Δ/Ψ/Φ) + tripwire §7.1.
> **Riset pendahuluan: `consciousness-council`** — 5 arketipe (Architect, Empiricist, Minimalist,
> Pragmatist, Contrarian) menekan keputusan interpretasi; titik ketegangan & sintesis §7.2.
> **Riset pendahuluan: `sequentialthinking`** (4 pikiran, 4/4 sukses, tool_call sequ-mcp):
> scope 4 workstream + ambang permutasi ganda → jalur data (bins/stuck_k2/F-9A) → hipotesis
> kompetitif & risiko validitas → rencana eksekusi 4 skrip + verifikasi determinisme.

---

## 0. RINGKASAN EKSEKUTIF

| # | Engine | Jenis tugas | Jenis engine | Split | Hasil kunci (OBSERVED) |
|---|---|---|---|---|---|
| 1 | hyd-K-i | deteksi kondisi (residu SPPA \|z\|>2) | statistical: label-forming median/MAD + **persistence** (RF DILARANG, D-A5) | LOWO 9 fold | Label tereproduksi **0/52.509 mismatch**; persistence AUPRC 0,425–0,843, lift 2,39–6,10 (9/9 >1), P 0,615–0,899, FAR 32–111 per 24jam-negatif |
| 2 | stuck-E2 | prediksi onset (H=10 mnt) | statistical: skor z(TQA)+z(HKLD)+ROP-drop, ambang q95-TRAIN | LOWO 4 fold | AUPRC 0,0073–0,324; lift 1,06–1,80 (4/4>1) tetapi **CI95 memuat prev 4/4** → sinyal TIDAK terbukti di atas prevalensi; onset-run cocok D1 (93/61/55/72) |
| 3 | tool_wear-K-i | deteksi perubahan-regime dalam-run (detik bengkel) | statistical: change-point SSE+permutation 500× + kalibrasi within-tool median/MAD | 8 run (4 alat × 2) | cp signifikan **8/8 di KEDUA ambang** termasuk alat baru → **spesifisitas GUGUR (precision 0,50)**; kalibrasi 5/27 deteksi R02 4/4 tapi FP alat baru 43–59/menit; titik operasi FAR-terkalibrasi: 4/4 deteksi, FP 1–3, TLead 20–36 dtk |
| 4 | Fisher/Pearson (baseline hyd K-ii) | prediksi kegagalan (kick/loss proxy) | statistical: korelasi Pearson + Fisher z-transform | temporal 70/30 (F-9A) | **Literal TIDAK DIJALANKAN**: FlowOut tidak ada di F-9A (bukti korelasi 4 kanal flow r=0,995–1,000 = semua aliran masuk); varian proxy dV_active/dt: AUPRC 0,022 (lift 5,95, CI memuat prev), 0 TP di ambang q95, B1 0/3 |

**Determinisme:** re-run penuh ke-4 skrip → 4/4 JSON IDENTIK (kecuali `elapsed_s`) —
`scratch/v9_e_stat/_det_a/` vs `_det_b/` + `determinism_check.py` = `ALL_DETERMINISTIC`.

---

## 1. IMPLEMENTASI (resep persis + penyimpangan tercatat)

### 1.1 Skrip

| Skrip | Engine | JSON primer |
|---|---|---|
| `code/v9_e_STAT_01_hyd_ki.py` | hyd-K-i | `scratch/v9_e_stat/v9_e_stat_01_hyd_ki_RESULTS.json` |
| `code/v9_e_STAT_02_stuck_e2.py` | stuck-E2 | `scratch/v9_e_stat/v9_e_stat_02_stuck_e2_RESULTS.json` |
| `code/v9_e_STAT_03_tool_wear.py` | tool_wear-K-i | `scratch/v9_e_stat/v9_e_stat_03_tool_wear_RESULTS.json` |
| `code/v9_e_STAT_04_fisher_pearson.py` | Fisher/Pearson baseline K-ii | `scratch/v9_e_stat/v9_e_stat_04_fisher_pearson_RESULTS.json` |

Run log bertimestamp per skrip: `scratch/v9_e_stat/v9_e_stat_0N_run_log.txt`. Seed 42 di semua
permutasi/bootstrap/konstanta. Semua fitur/label-kanal terlarang dipatuhi (assert anti-sirkular
di skrip 01; STUCK_RT hanya dipakai sbg mask in-block, bukan fitur skor E2).

### 1.2 Penyimpangan/perubahan metode — DICATAT, bukan disembunyikan (change-control)

| # | Temuan | Tindakan |
|---|---|---|
| CC-1 | Teks R1 §3.7 menulis `p = (1 + #{SSE_perm ≤ SSE_obs})/501` — **arah terbalik** (drop besar = signifikan → syaratnya `≥`); resep V8 `v8e_cp_validity.py` memakai `≥` | Eksekusi memakai `≥` (arah benar, reprodibel dgn V8); teks R1 dikoreksi via change-control ke PM/R1 |
| CC-2 | PM1 §2.7/R1 §3.7: "ambang p=0,002"; dgn 500 permutasi p minimum = 1/501 = 0,001996 — memakai ambang tunggal berarti memilih salah satu hasil | **DUA ambang dijalankan & dilaporkan**: p≤0,05 (resep V8) DAN p≤0,002 (literal spek). Hasil identik: 8/8 signifikan di keduanya → pilihan ambang TIDAK mempengaruhi kesimpulan (klaim keunggulan tidak bergantung ambang) |
| CC-3 | R1 §3.5.7 Fisher/Pearson literal butuh `FlowIn − FlowOut`; F-9A TIDAK punya kanal flow-out | Literal **TIDAK DIJALANKAN** (status: belum-terukur, penyebab terverifikasi probe: 4 kanal flow satu sama lain r=0,995–1,000 → semuanya aliran masuk). Varian terdokumentasi (imbalance = dV_active/dt) dijalankan & dilaporkan TERPISAH dengan anotasi sirkularitas |
| CC-4 | PM1 §2.5 menyebut "12 kolom pit"; F-9A punya **13** kolom `MudPit Volume Average` (V8 claim2 juga memakai 13) | Memakai 13 (resep V8); catatan off-by-one teks PM |
| CC-5 | persistence-onset literal (kolom `y_prev_stuck_onset`) memberi AUPRC 0,83–0,90 — ternyata **oracle**: y(t−1)=1 pada menit horizon ke-2..H karena label horizon diketahui retrospektif | DILAPORKAN DUA-FRAME: (i) literal (angka JSON), (ii) konstruksi V8 (alarm hanya di t_e → recall@H 0). Interpretasi §3.2: persistence-onset BUKAN detektor ter-deploy untuk lead-time |

---

## 2. hyd-K-i — deteksi kondisi residu SPPA (9 fold LOWO)

**Jenis tugas:** deteksi kondisi (status `|z|>2` residu SPPA per bin qcut(TFLO,10)) — bukan onset,
TLead tidak berlaku (B4 margin status). **Engine:** persistence `ŷ(t)=y(t−W)`, W=10 menit
(kolom `y_prev_hyd`, subset `valid_prev_hyd`) — RF DILARANG (D-A5, ΔB− 7/7 V8).

### 2.1 Verifikasi independen label-forming statistic (verification-mandatory #2)

Recompute penuh dari `scratch/v9_d1/bins/*.csv.gz` dengan resep identik `v9_d1_03.hyd_bin_labels`
(qcut TFLO 10 bin → median/MAD SPPA per bin → z → anom per menit → agregasi jendela W=10,
MIN_OBS=5, ambang ≥50% menit anom):

| Cek | Hasil |
|---|---|
| `y_hyd` recompute vs dataset | **0 mismatch / 52.509 baris** (9/9 well persis 100%) |
| `y_prev_hyd` recompute vs dataset (pasangan ts−W yang ADA di dataset) | **0 mismatch / 45.758 pasangan** |

(Pasangan di luar dataset = jendela prev yang tidak terekspor; dihitung dari master windows V8/D1 —
di luar jangkauan recompute subset ini, dicatat jujur di JSON.)

### 2.2 Hasil per lipatan (eksekusi, bukan kutipan)

| Test well | n | pos | prev | AUPRC (CI95) | lift (plafon) | P | R | FAR/24jam-neg | delay med (mnt) |
|---|---|---|---|---|---|---|---|---|---|
| F-10 | 7.571 | 1.394 | 0,1841 | 0,843 [0,734; 0,915] | 4,58 (5,43) | 0,899 | 0,922 | 32,4 | 3,5 |
| F-12 | 7.390 | 1.426 | 0,1930 | 0,643 [0,543; 0,734] | 3,33 (5,18) | 0,742 | 0,820 | 98,0 | 0,0 |
| F-14 | 10.401 | 865 | 0,0832 | 0,444 [0,284; 0,580] | 5,34 (12,02) | 0,631 | 0,659 | 49,6 | 0,0 |
| F-15A | 6.156 | 698 | 0,1134 | 0,490 [0,269; 0,677] | 4,32 (8,82) | 0,668 | 0,679 | 62,3 | 0,0 |
| F-15_S | 8.355 | 993 | 0,1189 | 0,424 [0,279; 0,553] | 3,57 (8,41) | 0,615 | 0,617 | 74,9 | 3,0 |
| F-5 | 6.332 | 621 | 0,0981 | 0,599 [0,383; 0,757] | 6,10 (10,20) | 0,754 | 0,764 | 38,8 | 0,0 |
| F-7 | 2.482 | 421 | 0,1696 | 0,506 [0,321; 0,648] | 2,98 (5,89) | 0,648 | 0,705 | 110,7 | 2,0 |
| F-9 | 1.616 | 423 | 0,2618 | 0,625 [0,394; 0,799] | 2,39 (3,82) | 0,793 | 0,687 | 89,7 | 0,0 |
| F-9_A | 2.206 | 331 | 0,1500 | 0,541 [0,266; 0,715] | 3,61 (6,67) | 0,711 | 0,702 | 67,5 | 1,5 |

- **Baseline:** (a) prevalence-random (analitik): AUPRC = prev, lift by definition 1,0 →
  **ΔB persistence > 0 di 9/9 fold** (AUPRC − prev = 0,306–0,659; persis di JSON
  `dB_vs_prevalence_random`); (b) rule `|z|` manual = PEMBENTUK LABEL → **tautologi** (P=R=1,0
by construction; nilai B3-nya = hitung beban alarm: 32–111 alarm/24jam-negatif pada label itu
sendiri — bukan pembanding keunggulan). Tidak ada fold UNDERPOWERED (pos ≥ 331 semua).

**Kemampuan:** status anomali hidrolik persisten antar-menit → persistence menang semua fold
(dengan delay median 0–3,5 mnt). **Batas:** FAR 32–111/24jam skala jendela = beban blok,
bukan alarm (L2 tren/konfirmasi, sesuai gate §1.3: L1 butuh FAR≤6 terukur — BELUM).

---

## 3. stuck-E2 — skor z onset (4 fold LOWO)

**Jenis tugas:** prediksi kejadian mendatang (onset 0→1, H=10 mnt). **Engine:** `E2_stats`,
skor = z(TQA)+z(HKLD)+ROP-drop (resep literal `eval_stuck.rule_and_score` V8: med60 shift(1),
mad60×1,4826, mean10, rop_drop≥0 dilaporkan sebagai bagian skor), ambang = **q95 skor TRAIN**
(pooled train-wells, mask ops & ~in-block) — anti-peeking. Skor dihitung LABEL-BLIND dari
`bins/` (grid 60 dtk), join ke baris dataset via `feat_ts_max` (0 missing join di 4 fold).

### 3.1 Hasil per lipatan

| Test well | n | pos | prev | thr q95-train | AUPRC (CI95) | lift (plafon) | P@q95 | R@q95 | FAR/24jam-neg | onsets (run) | R@H | TLead med (mnt) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F-10 | 4.216 | 772 | 0,1831 | 2,4649 | 0,231 [0,167; 0,306] | 1,26 (5,46) | 0,313 | 0,104 | 73,6 | 93 | 0,161 | 7,0 |
| F-14 | 95.925 | 389 | 0,00406 | 2,8219 | 0,0073 [0,0036; 0,0149] | 1,80 (246,6) | 0,022 | 0,031 | 8,0 | 61 | 0,131 | 2,5 |
| F-9 | 16.184 | 311 | 0,0192 | 2,7621 | 0,0203 [0,0085; 0,0352] | 1,06 (52,0) | 0,000 | 0,000 | 2,4 | 55 | 0,000 | – |
| F-9_A | 2.242 | 503 | 0,2244 | 2,5144 | 0,324 [0,192; 0,496] | 1,45 (4,46) | 0,487 | 0,151 | 66,2 | 72 | 0,181 | 8,0 |

Onset-run hasil segmentasi positif = **93/61/55/72 = PERSIS invarian D1 (V8)** — crosscheck
konstruksi horizon terpenuhi 4/4. **CI95 AUPRC memuat prev di 4/4 fold** → lift >1 TIDAK
signifikan (konsisten V8: "CI memuat prev 5/5"). Fold UNDERPOWERED: 0 (pos ≥ 311 semua;
F-14 prev sangat rendah → plafon lift 246,6 wajib dibaca bersama lift titik 1,80).

### 3.2 Baseline (split yang sama)

- **Prevalence-random** (analitik): AUPRC = prev → semua lift engine >1 by raw point, tetapi
  signifikansi gugur oleh CI (§3.1).
- **E0 persistence LITERAL** (`y_prev_stuck_onset`): AUPRC 0,827–0,902, lift 3,96–208,
  R@H 0,78–0,94 — **namun ini ORACLE, bukan detektor ter-deploy** (CC-5): y(t−1) pada menit
  horizon ke-2..H hanya bisa diketahui setelah onset terjadi. Kegunaannya = batas atas
  autokorelasi label, bukan pesaing operasional.
- **E0 persistence konstruksi V8** (alarm hanya tepat di t_e): **recall@H = 0 by construction**
  (alarm jatuh di luar `[t_e−H, t_e)`) — angka V8 direproduksi sebagai definisi, tercatat di JSON.
- **Canary-kedalaman** = baseline S9 yang dihitung E_RULE/E_ML pada fold identik — BUKAN scope
  E_STAT (dicatat, bukan dihilangkan).

**Kemampuan:** skor E2 memberi ranking di atas prevalensi di semua fold (poin), dengan TLead
median 2,5–8 mnt pada fold yang mendeteksi. **Batas:** signifikansi 0/4; FAR 2,4–74/24jam;
P di F-9 = 0 → **L3 triage (skor-ranking), L1/L0 BELUM** — konsisten gate V8 untuk kelas ini.

---

## 4. tool_wear-K-i — change-point + kalibrasi within-tool (8 run)

**Jenis tugas:** deteksi perubahan-regime dalam-run (bengkel, detik) — bukan prediksi horizon;
lead = DETIK bengkel (D-A7: tidak dijumlah dgn menit rig). **Data:** `toolwear_windows.csv`
(469 jendela 1 dtk, 27 fitur; 4 alat × 2 run; label = identitas run, desain dataset →
anti-sirkular terpenuhi).

### 4.1 Bagian A — change-point SSE + permutation 500× (seed 42)

- **Tes pembeda t_cp (artefak termal):** t_cp <5 dtk di **0/8 run** (frac_early = 0,0;
  R01 0,0 / R02 0,0) → "sub-klaim gugur karena artefak termal" **TIDAK terpenuhi** → lanjut dinilai.
- **Signifikansi DUA ambang (CC-2):** p≤0,05 → **8/8**; p≤0,002 → **8/8** (semua run p = 0,0020
  = 1/501, nol permutasi yang mengalahkan drop observasi).
- **Spesifisitas keausan = GUGUR (hasil NEGATIVE, dilaporkan apa adanya):** cp signifikan di
  **R01 (alat BARU) 4/4** → run-level precision = tp/(tp+fp) = 4/8 = **0,50**, recall 1,0,
  FAR cp = 0 TN. Identik dgn temuan V8 (precision 0,50) → **kemampuan = "detektor perubahan
  regime", klaim "onset progresi keausan" TERDUKUAT LEMAH**.
- TLead cp → akhir R02 (anchor alat tumpul): 34/36/39/27 dtk, median 35 dtk (min 27).
- Kesepakatan antar-family (kurt/crest/fdom/rms): selisih t_cp antar-family per run
  median **16,5 dtk**, rentang 8–40 dtk (JSON `cross_family_spread_s`); signifikansi
  per family (p≤0,05): kurt **7/8** (satu-satunya: T02-R02 kurt p=0,387, t_cp 39/62 dtk), crest 8/8,
  fdom 8/8, rms 8/8; pada p≤0,002: kurt 5/8, crest 5/8, fdom 6/8, rms 8/8 — cp gabungan
  12-dim tetap 8/8 di kedua ambang.
- n=8 run → **UNDERPOWERED (<30)**: metrik = proporsi, bukan klaim signifikansi populasi.

### 4.2 Bagian B — kalibrasi within-tool (median+MAD 30% awal R01, alarm ≥5/27 fitur |z|>3)

| Alat | FP R01 (alat baru) | FAR FP/menit | % jendela R01 alarm | Deteksi R02 | first alarm (dtk) | TLead→akhir R02 (dtk) | baseline rule 3-RMS (FP R01 / deteksi R02) | kurangi_ragu |
|---|---|---|---|---|---|---|---|---|
| T01 | 41/42 | 58,6 | 97,6% | ✓ | 0 | 60 | 41 / ✓ | 0,00 |
| T02 | 27/35 | 46,3 | 77,1% | ✓ | 14 | 48 | 33 / ✓ | 0,18 |
| T03 | 30/42 | 42,9 | 71,4% | ✓ | 0 | 60 | 40 / ✓ | 0,25 |
| T04 | 34/40 | 51,0 | 85,0% | ✓ | 0 | 58 | 36 / ✓ | 0,06 |

**Interpretasi jujur:** deteksi 4/4 (B1 100%) TAPI alarm nyala 71–98% di alat BARU →
"terdeteksi" TIDAK bermakna pada ambang 5/27; kurangi_ragu vs rule 3-RMS hanya 0,00–0,25
(reproduksi angka V8 0,00–0,25). FAR 43–59 alarm/menit >> tier §1.3.

### 4.3 Bagian C — titik operasi FAR-terkalibrasi (threshold = kuantile skor R01, dideklarasi)

| Target alarm/menit | FP R01 per alat | Deteksi R02 | first alarm (dtk) | TLead (dtk) | % R02 alarmed |
|---|---|---|---|---|---|
| ≤1,0 | 1 / 3 / 1 / 3 | **4/4** | 35 / 26 / 36 / 38 | 25 / 36 / 24 / 20 | 3,3–6,9% |
| ≤0,2 | 1 / 3 / 1 / 3 | **4/4** | 35 / 26 / 36 / 38 | 25 / 36 / 24 / 20 | 3,3–6,9% |

Titik operasi inilah yang LAYAK sebagai gating inspeksi (FP 1–3, TLead 20–36 dtk) — bukan
ambang 5/27 baku.

### 4.4 Bagian D — ranking AUPRC vs baseline relevan

AUPRC engine (skor = jumlah fitur |z|>3, label identitas run, 469 jendela) = **0,589**;
prev = 0,512; **lift 1,151; plafon 1/prev = 1,954**; ΔB vs identity-majority = +0,077.
**Persistence: N/A — DINYATAKAN** (label konstan dalam run; resep R1 §3.7 — bukan dihilangkan).
Canary 3-RMS AUPRC (0,516–0,612, V8) = pembanding K-ii LOTO → domain E_ML (S9).

**Kemampuan:** detektor perubahan-regime + gating inspeksi via FAR-terkalibrasi (4/4, FP 1–3).
**Batas:** spesifisitas cp gagal (0,50); kalibrasi baku 5/27 tidak spesifik; transfer ke rig
TIDAK diklaim (confound urutan-run); n=8 UNDERPOWERED.

---

## 5. Fisher/Pearson literal — baseline hyd K-ii (F-9A)

**Status literal (CC-3): BELUM DIJALANKAN — FlowOut tidak ada.** Bukti (probe sesi ini):
`Flow Pumps` 345.442 non-null, `Mud Flow In` 83.565, `TFLO30s` 64.757, `FLOW-TRPM` 34.115;
korelasi antar mereka **r = 0,995–1,000** (semua aliran MASUK); tidak ada kanal flow-out di
239 kolom F-9A. Klaim "tidak bisa dijalankan" = hasil tes diskriminatif, bukan asumsi.

**Varian terdokumentasi (dijalankan):** imbalance_proxy = dV_active/dt (`Tank volume (active)`
sentinel −10..250); `r_t = Pearson(dV_active/dt, ΔV_pit)` jendela 30 mnt; skor =
`|z'_t − med_base|/(1,4826·MAD_base)` dgn `z'=atanh(r)` (Fisher transform, R1 [15][16]),
baseline 60 mnt shift(1); alarm = skor ≥ q95-TRAIN.

**Label K-ii (resep LITERAL V8 claim2):** grid 1 mnt median, 13 kolom pit, sentinel [−5,150],
r10, z, |z|>2 sustain ≥5 mnt, sirkulasi ≥500 L/min SETIAP MENIT run, merge onset <30 mnt,
horizon [t_e−10, t_e), blok [t_e, t_e+30) dibuang. **Reproduksi persis V8: 124 episode
(39 kick / 85 loss), prev_test = 0,003701 = angka V8 0,0037** → kontrol validitas label OK.

| Metrik (test 30% akhir, n=8.107, pos=30) | Nilai |
|---|---|
| AUPRC (CI95) | 0,022 [0,0025; 0,0684] — **memuat prev 0,0037** |
| lift (plafon 270) | 5,95 (270,2) |
| P / R @q95 | **0,000 / 0,000** (TP=0, FP=177, FN=30) |
| FAR @q95 | 31,6 / 24jam-negatif |
| B1 / TLead | 0/3 onset uji (3 onset uji = UNDERPOWERED) |
| Baseline prevalence-random | AUPRC = 0,0037 (analitik) |
| Baseline rule z-pit | deteksi di menit t_e (DI LUAR horizon) → B1 = 0 by construction; TLead = 0 → hanya baseline "sistem hari-ini" B3 |

**Kemampuan varian:** ranking di atas prevalensi (poin) tapi TIDAK signifikan (CI memuat prev)
dan nol deteksi di ambang operasi. **Perbandingan diskriminatif (R1 §4.5):** AUPRC RF K-ii V8
= 0,2279 vs varian Fisher/Pearson = 0,022 (split/label sama) → **RF mempertahankan nilai-tambah**
atas baseline statistika literal terkuah (dengan caveat: varian ≠ literal penuh; literal butuh
data flow-out). **Batas:** 1 wellbore; label = PROXY; sirkularitas parsial varian (tank aktif
bisa diturunkan dari pit) → angka variant BUKAN klaim keunggulan metode.

---

## 6. KERANGKA A/B/C — KEMAMPUAN + BATAS + KEKUATAN BUKTI (bukan lulus/gagal)

| Engine | Jenis tugas | Lapisan A (deteksi vs baseline relevan) | Lapisan B (nilai pemeliharaan) | Lapisan C (kepercayaan) | Bukti |
|---|---|---|---|---|---|
| hyd-K-i | deteksi kondisi | persistence ΔB>0 vs prevalence 9/9; rule-\|z\| = label (tautologi, bukan pembanding) | delay median 0–3,5 mnt; TIDAK ada peringatan-dini (tugas status) | 9 well; label tereproduksi 0 mismatch; FAR 32–111 >> 6 → max L2 | KUAT (reproduksi + LOWO penuh) |
| stuck-E2 | prediksi onset | lift >1 4/4 tapi CI memuat prev 4/4 → **tidak terbukti** vs prevalence | TLead 2,5–8 mnt pada fold terdeteksi; B1 0–18% << 80% | 4 well; onset-run cocok D1; FAR 2,4–74 | LEMAH (ranking sah, alarm tidak) |
| tool_wear-K-i | deteksi regime | cp 8/8 signifikan TAPI precision 0,50 (spesifisitas gagal); kalibrasi baku FP 43–59/menit | FAR-terkalibrasi: 4/4, TLead 20–36 dtk vs alat tumpul | n=8 UNDERPOWERED; confound urutan-run; label desain (bukan fitur) | SEDANG (operating point layak gating; klaim progresi lemah) |
| Fisher/Pearson (K-ii) | prediksi kegagalan | literal TIDAK DIJALANKAN (FlowOut absen); varian: 0 TP, CI memuat prev | B1 0/3 (onset uji UNDERPOWERED) | 1 well; label proxy; reproduksi label V8 persis | LEMAH (varian); literal = belum-terukur |

Tidak ada satupun engine yang diklaim layak alarm otomatis (L0-alarm 0/7 — gate §1.3 TIDAK
digesir; angka di sini = bahan evaluasi A/B/C untuk EVAL_A/PM, bukan label lolos).

---

## 7. KERANGKA TAMBAHAN

### 7.1 What-if-oracle (risiko eksekusi)

| Cabang | Bobot | Skenario | Kenyataan/robust action |
|---|---|---|---|
| Ω Best | 15% | Semua resep reproduksi V8 persis | **Terjadi**: label K-ii 124/39/85 + prev 0,0037 cocok; kurangi_ragu 0,00–0,25 cocok |
| α Likely | 45% | Ambang permutasi ganda mengubah kesimpulan | Ternyata 8/8 di kedua ambang → kesimpulan invariant (CC-2) |
| Δ Worst | 20% | Data flow-out tidak ada → literal buntu | **Terjadi** (CC-3): dites, diverifikasi, varian dijalankan + status belum-terukur dicatat |
| Ψ Wildcard | 10% | persistence-onset literal ternyata bukan detektor | **Terjadi** (CC-5): oracle terdeteksi, dilaporkan dua-frame |
| Φ Contrarian | 10% | Baseline "menang" dari RF (R1 §4.5 tes) | TIDAK terjadi: RF 0,228 >> varian 0,022 → nilai-tambah ML bertahan |
| Tripwire | – | Angka beda dari V8 → cek resep | Semua deviasi terjelaskan (split LOWO vs temporal; anchor `feat_ts_max`) |

### 7.2 Consciousness-council (sintesis)

- **Architect:** 4 skrip = 4 modul murni-statistik tanpa overlap dgn RF E_ML; JSON-per-engine
  siap digabung EVAL_A.
- **Empiricist:** satu-satunya klaim ber-temuan kuat = reproduksi (label 0 mismatch; K-ii
  identik V8; determinisme 4/4); dua klaim deteksi LEMAH dilaporkan apa adanya.
- **Minimalist:** tidak menambah engine baru di luar DoD; Fisher literal yang buntu TIDAK
  diganti dgn heuristik optimis — dicatat sebagai belum-terukur.
- **Pragmatist:** 2 hasil siap-pakai operasional = FAR-terkalibrasi tool_wear (gating inspeksi)
  dan persistence hyd-K-i (monitoring tren).
- **Contrarian (tekanan inti):** "lift >1 di semua fold stuck-E2" terlihat bagus → DITOLAK
  sebagai klaim: CI memuat prev 4/4; dan persistence literal 0,83–0,90 = oracle, bukan prestasi.
- **Sintesis:** nilai E_STAT = baseline jujur + reproduksi; ketegangan "angka bagus vs bukti"
  diresolusi dengan melaporkan CI dan sifat oracle eksplisit.

---

## 8. BELUM DIVERIFIKASI / BELUM TERUKUR (verification-mandatory #3)

1. **Fisher/Pearson literal (FlowIn−FlowOut)**: butuh kanal flow-out — TIDAK ADA di F-9A
   (bukti korelasi §5). Status: belum-terukur; varian proxy ≠ literal.
2. Perbandingan langsung baseline K-ii vs **RF V8** memakai angka lintas-run (0,022 vs 0,2279);
   RF E_ML V9 belum dijalankan → perbandingan final menunggu kartu E_ML/EVAL_A.
3. CI95 = moving-block bootstrap (blok 60, 1.000) mengikuti konvensi V8 hyd; skrip stuck-E2/
   tool_wear memakai blok yang sama — blok 10 (V8 tool_wear C1) TIDAK dipakai ulang di sini.
4. `y_prev_hyd` 45.758/45.758 pasangan cocok; sisa pasangan di luar ekspor D1 tidak diverifikasi.
5. Merge-episode V8 = "drop onset <30 mnt" (bukan gabung span) — mengikuti kode V8 claim2;
   teks PM "merge" tidak merinci; bila PM maksud lain → change-control.
6. FAR hyd-K-i/E2 = FP/(jendela negatif/60) ×24, asumsi jam-operasi V8-R1 §6.4 — harmonisasi
   antar-kelas = tugas EVAL_A (S7).
7. tool_wear: rho-time per family dihitung tersimpan di JSON tapi uji Wilcoxon lintas-alat
   (V8 bagian 3) TIDAK diulang di run ini.

---

## 9. PENERIMAAN (acceptance)

| # | Syarat | Bukti |
|---|---|---|
| a | Engine jalan pada data nyata | 4/4 skrip sukses: hyd_ki 52.509 baris/9 fold; stuck_k2 118.567 baris/4 fold; toolwear 469 jendela/8 run; F-9A 419.745 baris/27.322 menit grid |
| b | Hasil per lipatan tercatat dari eksekusi | tabel §2.2, §3.1, §4, §5 — semua dari JSON di `scratch/v9_e_stat/` |
| c | Baseline relevan dibandingkan | prevalence-random (semua engine), rule-\|z\| hyd, persistence-onset literal + konstruksi V8 (stuck), rule 3-RMS + identity-majority + persistence-N/A (tool_wear), rule z-pit (K-ii) — pada split/fold yang sama |
| d | 0 angka karangan | semua angka terbaca dari JSON hasil run; determinisme 4/4 IDENTIK (re-run) |
| e | Baris "Riset pendahuluan" | header (6 skill) |
| f | sequ-mcp ≥3 pikiran | 4 pikiran, 4/4 sukses |

## 10. SUMBER

`docs/V9_PM1_ARCHITECTURE.md` §2.4/§2.5/§2.7/§4.4 · `docs/V9_R1_JUSTIFICATION.md` §3.4/§3.5/§3.7/§4.1/§4.5 ·
`docs/V9_D1_DATA_PIPELINE.md` §3–§9 + `scratch/v9_d1/` (datasets + lowo_*.json) ·
`docs/V8_E_hyd_CAPABILITY.md`, `docs/V8_E_stuck_CAPABILITY.md`, `docs/V8_E_tool_wear_CAPABILITY.md` ·
resep V8: `scratch/v8_e_hyd/claim1_eval.py`, `claim2_eval.py`, `scratch/v8_e/v8e_cp_validity.py`,
kanban `capstone-v8-capability/workspaces/t_edbe66a8/v8e_b_warning.py`, `v8e_c_robust.py`,
`workspaces/t_d7fa8c16/eval_stuck.py` · data: `scratch/v6_e1/toolwear_windows.csv`,
`data/witsml/Norway-NA-15_47_9-F-9 A time.csv` · JSON primer: `scratch/v9_e_stat/v9_e_stat_0*_RESULTS.json`.
