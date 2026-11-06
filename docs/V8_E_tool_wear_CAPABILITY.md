# V8-E `tool_wear` — KEMAMPUAN + BATAS PENGGUNAAN (kerangka 3 lapisan A/B/C)

Task: `t_edbe66a8` [Evaluator] · Board: capstone-v8-capability · Tanggal: 2026-10-11 (WIB)
Kerangka: `docs/V8_R1_ABC_SPEC.md` §1–§2.7 + §3.4 (mengganti gate biner V6/V7).
Semua angka di bawah dihasilkan EKSEKUSI NYATA pada data lokal (bukan angka karangan);
skrip: `v8e_a_loto.py`, `v8e_cp_validity.py`, `v8e_b_warning.py`, `v8e_c_robust.py`;
hasil mentah: `scratch/v8_e/V8_E_{A_loto,cp_validity,B_warning,C_robust}.json`.

> **Riset pendahuluan: `statistical-analysis`** — AUPRC+lift untuk prevalensi 0,5
> (plafon lift 1/prev = 2,0 wajib dilaporkan), CI95 moving-block bootstrap (blok 10,
> 1.000 resample, seed 42 — metode V6 dipertahankan), Wilcoxon signed-rank untuk
> perbandingan tren R02 vs R01 (n=4 pasang, dilaporkan apa adanya).
> **Riset pendahuluan: `scientific-critical-thinking`** — dua sub-klaim dinilai
> terpisah; tes pembeda t_cp (arteFak termal) dijalankan sebagai test of specificity,
> bukan hanya validity; confound R02 selalu sesudah R01 (urutan waktu identik dengan
> status keausan) diperlakukan sebagai batas kausal yang tak terpecahkan dengan data ini.
> **Riset pendahuluan: `verification-mandatory`** — angka LOTO baru divalidasi silang
> terhadap hasil pra-reg V6 (`E1c_LOWO_RESULTS.json`): AUPRC per fold identik 4 digit
> (0,5433/0,7684/0,7031/0,6497) → re-run terverifikasi; satu bug logika pada SSE
> change-point (cumsum tak dikurangi prefix → SSE salah, drop negatif) ditemukan via
> sanity check (SSE terbagi > total SSE = mustahil) lalu diperbaiki sebelum hasil cp sah.
> **Riset pendahuluan: `sequentialthinking`** (5 pikiran) — pemisahan desain engine
> per sub-klaim → anchor kejadian nyata → titik operasi FAR-terkalibrasi → C3.

---

## (a) Jenis tugas + engine (per sub-klaim)

Data: Mendeley `th4yv974r2` (CC BY 4.0) — 4 alat (T01–T04) × 2 run; deskripsi dataset:
Run 1 = alat BARU (diinspeksi di akhir Run 1); Run 2 = alat sama dilanjutkan sampai
TUMPUL di akhir Run 2. 469 jendela 1 dtk @1000 Hz, 27 fitur getaran (kurt/crest/fdom/
rms/skew/p2p/zcr/mean/std per sumbu X/Y/Z). Label = identitas run (desain dataset,
BUKAN turunan fitur → anti-sirkular terpenuhi).

| Sub-klaim | Jenis tugas | Jenis engine | Data |
|---|---|---|---|
| (i) pemantauan-alat-dikenal | Deteksi perubahan-regime dalam-run (klaim awal: progresi keausan; hasil §e) | (1) change-point statistics (SSE 1-split + permutation 500×); (2) baseline-calibration anomaly (median-MAD dari 30% awal R01 alat sendiri, alarm ≥5/27 fitur \|z\|>3) | 8 run, 469 jendela |
| (ii) generalisasi-lintas-alat | Prediksi status keausan pada alat tak terlihat (LOTO) | ML: RF (300 pohon, min_leaf 5, balanced_subsample) — ambang operasi = pooled inner-LOO F1 (tanpa peeking test) | 4 fold LOTO |

Baseline relevan per tugas (bukan universal): (i) aturan ambang amplitudo 3-RMS;
(ii) canary 3-RMS + identity-run majority (AUPRC = prev = 0,5); persistence **N/A**
(label konstan di dalam file run — tak ada yang bisa dipersist, dinyatakan bukan
dihilangkan).

---

## (b) LAPISAN A — apakah deteksi bekerja (eksekusi nyata)

### A(ii) LOTO lintas-alat — ambang operasi inner-LOO F1

| Fold | n_test (pos) | prev | AUPRC RF | lift (plafon) | canary 3-RMS | ΔB vs canary | precision | recall | FP | FAR (FP/menit negatif) | CI95 AUPRC |
|---|---|---|---|---|---|---|---|---|---|---|---|
| T01 | 120 (60) | 0,500 | 0,5433 | 1,087 (2,00) | 0,5164 | +0,0269 | 0,516 | 0,817 | 46 | 46,0 | [0,260; 0,809] |
| T02 | 112 (62) | 0,554 | 0,7684 | 1,388 (1,81) | 0,5947 | +0,1737 | 0,559 | 1,000 | 49 | 58,8 | [0,529; 0,929] |
| T03 | 121 (60) | 0,496 | 0,7031 | 1,418 (2,02) | 0,6024 | +0,1008 | 0,509 | 0,967 | 56 | 55,1 | [0,373; 0,924] |
| T04 | 116 (58) | 0,500 | 0,6497 | 1,299 (2,00) | 0,6124 | +0,0374 | 0,500 | 1,000 | 58 | 60,0 | [0,367; 0,882] |

Agregat: precision median **0,512** · recall median **0,983** · lift 1,09–1,42 ·
ΔB vs canary **positif 4/4** · ΔB vs identity-majority positif 4/4 · lift >1 di 4/4 ·
lift ≥1,5 (G1) **0/4** · spread AUPRC 0,225.

Interpretasi A(ii): ranking/skor keausan MENAMBAH di atas baseline relevan
(canary amplitudo dan majority) di 4/4 fold — sinyal lintas-alat nyata, kekuatan
sedang, terkunci plafon lift 2,0 (prev 0,5). Namun pada ambang keputusan biner
yang dipilih tanpa peeking (F1 inner-LOO), precision ≈ peluang (0,50–0,56) dan
FAR 46–60 FP/menit-negatif → keputusan biner pada titik ini TIDAK layak dipakai
sebagai alarm; nilai A ada di LAYER RANKING (AUPRC), bukan di ambang biner.

### A(i) within-tool — change-point (tes pembeda t_cp) + engine kalibrasi

| Ukuran | Hasil (8 run) |
|---|---|
| t_cp di detik awal (<5 dtk) | **0/8 run** (R01 0/4, R02 0/4) — tes pembeda "artefak termal" TIDAK terkonfirmasi |
| t_cp signifikan (perm p=0,002) | **8/8 run — termasuk SEMUA run alat BARU (R01)** |
| precision run-level (cp → progresi R02) | **0,50** (TP 4, FP 4) |
| recall run-level | **1,00** (FN 0) |
| FAR change-point di R01 (alat baru) | **1,05 cp/menit** |
| kesepakatan antar-family fitur (kurt/crest/fdom/rms) | spread t_cp median 16,5 dtk (rentang 8–40 dtk dari run 50–62 dtk) |

Kontrol tren (eksplorasi, Wilcoxon 4 pasang): median Spearman ρ vs waktu —
rms: R01 +0,929 vs R02 +0,895 (p=0,125); kurt: +0,725 vs +0,553 (p=0,625);
crest: +0,430 vs +0,458 (p=0,875); fdom: −0,467 vs −0,328 (p=0,125).
Drift menaik terjadi di alat BARU maupun alat aus — perbedaan R02−R01 tidak
signifikan pada 4 family (n=4, UNDERPOWERED, dilaporkan).

Interpretasi A(i): change-point MENDETEKSI perubahan-regime dalam-run (recall 1,0
terhadap anchor "alat tumpul di akhir R02"), tetapi TIDAK SPESIFIK ke keausan —
deteksi identik menyala pada run alat baru (precision 0,50; drift R01 setara R02).
Engine kalibrasi within-tool (median-MAD) memperkuat temuan ini: fraksi fitur
>3σ pada R01 (alat baru, 0,19–0,33) ≈ R02 (0,17–0,33) → non-stationarity dalam-run
bukanlah progresi keausan.

---

## (c) LAPISAN B — nilai maintenance (anchor: alat TUMPUL di akhir Run 2)

| Engine / titik operasi | B1: terdeteksi sebelum akhir R02 | T_lead median (rentang) | FP di baseline R01 | Catatan |
|---|---|---|---|---|
| (i) kalibrasi within-tool, ambang dideklarasi ≥5/27 fitur \|z\|>3 | 4/4 (100%) | 59 dtk (48–60) | **43–59 alarm/menit** | "terdeteksi" TIDAK bermakna — alarm nyala terus di alat BARU juga; kurangi_ragu vs rule 3-RMS hanya 0,00–0,25 |
| (ii) LOTO RF, ambang F1 inner-LOO | 4/4 (100%) | 59,5 dtk (58–62) | 77–100% jendela R01 alarms | alarm jenuh → T_lead trivially besar |
| (ii) LOTO RF, **titik operasi FAR-terkalibrasi** (eksplorasi; ambang = kuantile skor R01 agar laju alarm baseline ≤1/menit — desain dideklarasi sebelum run) | **4/4 (100%)** | **47,5 dtk (35–59)** | 1–2 FP (target ≤1/menit) | alarm SPARSE di R02 (1,7–16,1% jendela); first alarm 3–25 dtk setelah R02 mulai |
| (i) kalibrasi within-tool, titik operasi FAR ≤1/menit | 4/4 (100%) | 30 dtk (20–36) | 1–3 FP | first alarm 26–38 dtk |

Nilai maintenance yang terukur: pada laju alarm yang wajar (≤1 alarm per menit
baseline — setara ambang "tren" §4 pada skala menit), KEDUA engine mendeteksi run
alat aus dengan peringatan median 30–47,5 dtk sebelum akhir run (≈35–60% durasi
run 50–62 dtk) dengan hanya 1–3 alarm palsu di baseline. Peringatan ini
BERKARAKTER INDIKASI/WAKTU-BERTINDAK di domain bengkel — bukan peringatan
kegagalan mendadak (durasi run 50–62 dtk = batas jujur domain; anchor B2
stand/POOH tidak berlaku di sini). Pada ambang F1-standar, B1=100% TIDAK boleh
dipakai sebagai bukti nilai (alarm menyala terus-menerus di alat baru).

---

## (d) LAPISAN C — cukup tepercaya untuk dipakai

| Ukuran | Hasil |
|---|---|
| C1 stabilitas antar-fold | spread AUPRC 0,225 (0,543–0,768); CI95 tiap fold LEBAR (mis. T01 [0,26; 0,81]) → ketidakpastian transparan; tidak ada fold UNDERPOWERED (n_pos 58–62 ≥30) |
| C2 ketahanan lintas-alat | lift >1 di 4/4 fold (rentang 1,09–1,42); TIDAK ada fold lift <1; tetapi lift ≥1,5 0/4 → stabilitas "menang tipis", bukan dominan |
| C3 toleransi kualitas sensor | dropout 1 kanal teratas (Z_kurt): penurunan relatif maks **18,3%** (T01 malah NAIK 9,3%) → <20% = robust; dropout 2 kanal (Z_kurt+X_fdom): maks **26,2%** (T04; T02 19,8%) → 1 fold melewati ambang 20% = marginal; noise σ/10: maks 14,9% → robust |
| C4 transparansi ketidakpastian | CI95 dilaporkan SEMUA fold; klaim (i) dilabeli UNDERPOWERED (8 run <30) |
| C-domain | transfer ke drilling **TIDAK diklaim**: 4 alat bengkel, run 50–62 dtk, dan confound tak terpecahkan — R02 selalu berurutan sesudah R01 sehingga keausan identik dengan urutan waktu (tak ada run acak/replik). Tidak ada dataset tool-wear drilling nyata tambahan (V7-D2). |

---

## (e) KESIMPULAN — kemampuan, batas pemakaian, kekuatan bukti

### Sub-klaim (ii) generalisasi-lintas-alat (RF LOTO, ML)
- **LAYAK untuk:** (1) *scoring/ranking* status keausan lintas alat di domain
  bengkel — AUPRC 0,54–0,77 mengalahkan canary amplitudo 4/4 dan majority 4/4;
  (2) *indikasi/pemantauan tren* dengan titik operasi FAR-terkalibrasi ≤1
  alarm/menit baseline (deteksi 4/4, T_lead median 47,5 dtk sebelum kondisi
  tumpul tercapai).
- **BELUM untuk:** alarm kritis otomatis — G1 (lift ≥1,5) 0/4, precision biner
  ≈0,50–0,56 pada ambang tanpa-peeking, CI95 lebar, plafon lift 2,0 (prev 0,5).
- **Kekuatan bukti:** SEDANG — 4 fold LOTO SEMUA menang di atas baseline relevan
  (bukan kebetulan 1 fold), re-run identik 4 digit dengan pra-reg V6 (E1c), tapi
  hanya 4 alat, 1 dataset, prev 0,5, dan confound urutan-run melekat.

### Sub-klaim (i) pemantauan-alat-dikenal (change-point + kalibrasi within-tool)
- **LAYAK untuk:** detektor *perubahan-regime dalam-run* (statistik change-point:
  recall 1,0 terhadap anchor akhir-run-tumpul, FAR 1,05 cp/menit) — berguna untuk
  gating kapan inspeksi layak dilakukan pada alat yang sedang dipantau.
- **BELUM untuk:** klaim *"onset progresi keausan"* — spesifisitas gagal pada tes
  kontrol: cp signifikan juga di 8/8 run alat BARU (precision run 0,50) dan drift
  fitur R01 setara R02 (Wilcoxon p 0,125–0,875). Tes pembeda pra-reg "artefak
  termal di detik awal" memang TIDAK terkonfirmasi (0/8), tetapi kegagalan
  spesifisitas ini lebih mendasar: yang terdeteksi adalah drift umum dalam-run,
  bukan keausan.
- **Kekuatan bukti:** untuk kemampuan "deteksi perubahan-regime": SEDANG-RENDAH
  (8 run, underpowered, tapi 8/8 konsisten); untuk klaim keausan: TERDUKUAT LEMAH
  (bukti kontrol R01 menentang spesifisitas).

### Ringkasan batas pemakaian (bukan vonis biner)
1. Dipakai sebagai **skor/indikasi tren keausan** (ranking + timing pada skala
   menit-run bengkel): LAYAK, bukti terukur di §b–§c.
2. Dipakai sebagai **alarm kritis otomatis**: BELUM — FAR biner pada ambang
   standar 46–60/menit; G1 0/4; butuh dataset lebih besar + prev rendah nyata.
3. **Ditransfer ke drilling (Volve/USROP)**: TIDAK DIKLAIM — domain, skala, dan
   confound berbeda; butuh data tool-wear drilling nyata (belum tersedia).
4. **Waktu peringatan** yang diklaim = detik (30–47,5 dtk pada run ~60 dtk) —
   setara anchor RUL/degradation bengkel, BUKAN SLA operasional rig.

### Belum terukur (jujur)
- Precision/recall onset keausan intra-run terhadap kejadian nyata: **belum
  terukur** — dataset tidak punya label onset intra-run (label hanya per-run);
  anchor pengganti = akhir R02 (dipakai di §c) dan kontrol R01.
- B2 (waktu-untuk-bertindak vs stand/POOH): **tidak berlaku** — durasi run 50–62 dtk.
- Generalisasi ke rig/sensor drilling: **belum terukur** — tidak ada data.

---
*Semua angka berasal dari eksekusi skrip pada data lokal; angka V6 yang dikutip
sebagai pembanding (E1c) berasal dari `scratch/v6_e1/E1c_LOWO_RESULTS.json`.*
