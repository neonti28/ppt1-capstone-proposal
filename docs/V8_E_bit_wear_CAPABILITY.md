# V8-E_bit_wear — PROFIL KEMAMPUAN 3 LAPISAN (A/B/C) KELAS `bit_wear`

Task: `t_0e9cfefb` [Evaluator] · Board: capstone-v8-capability · Tanggal: 2026-10-11 (WIB)
Status: BUNGKUS ULANG hasil V6 ke kerangka A/B/C (V8-R1) — TANPA run baru; setiap angka
ditandai OBSERVED (dari dokumen primer / artefak run) atau DERIVED (turunan aritmetika
dari angka OBSERVED), dan yang tidak ada ditulis "belum terukur".

> **Riset pendahuluan: `scientific-critical-thinking`** — klaim "engine layak X" dipisah
> OBSERVED vs DERIVED vs BELUM-TERUKUR; dua klaim tugas `bit_wear` (status vs onset)
> dinilai TERPISAH; persistence-dominance 4/4 dilaporkan sebagai KEMAMPUAN terukur
> (baseline punya nilai), bukan label gagal; tes pembeda onset-persistence dinyatakan
> sebagai pemecah hipotesis reframing.
> **Riset pendahuluan: `statistical-analysis`** — kelas prev 0,096–0,544 → AUPRC+lift
> dipertahankan; plafon lift 1/prev dilaporkan per fold (F-15S plafon 1,84 → ambang
> tetap 1,5 nyaris tak tercapai pada prev tinggi = konteks, bukan pelemahan ambang);
> CI95 moving-block bootstrap (E1d: n_boot 1000, block 20, seed 42) + fold <30 positif =
> UNDERPOWERED (3 fold dicatat, tidak dihitung mayoritas).
> **Riset pendahuluan: `verification-mandatory`** — angka ditarik dari dokumen primer
> (V6_E1 §4.3, V7_PM §3, V8-R1 §2.3) DAN dicocokkan ke artefak primer
> `scratch/v6_e1/E1d_LOWO_RESULTS.json` (koordinat persis per fold, termasuk field yang
> TIDAK ADA: grep artefak membuktikan precision/recall/FAR tidak pernah diukur →
> "belum terukur" berbasis bukti ketiadaan, bukan asumsi).
> **Riset pendahuluan: `sequentialthinking`** (5 pikiran, 5/5 sukses) — inventaris
> angka+gap → pemetaan tugas/baseline → turunan lapisan A → lapisan B/C+kekuatan bukti →
> batas penggunaan + cek pembanding (falsifier).

---

## 0. RINGKAS SINGKAT — APA YANG DINILAI

Kelas `bit_wear` memuat DUA klaim tugas yang dinilai terpisah (kerangka V8-R1 §2.3):

| Klaim | Jenis tugas | Engine | Status evaluasi |
|---|---|---|---|
| **K-1: status high_MSE** (yang benar-benar dijalankan V6, kampanye E1d) | Deteksi kondisi (status blok ineffisiensi Teale) | RF (supervised ML) · persistence (rule) · canary-kedalaman (rule) | **TERUKUR PENUH** (AUPRC/lift/CI/persistence, 4 fold LOWO) |
| **K-2: onset-of-high-MSE** (S-F1, relabel V7) | Prediksi kejadian mendatang (masuknya blok high_MSE) | RF onset (belum ada hasil) + persistence-onset (tes pembeda, belum dihitung) | **BELUM TERUKUR** — yang ada hanya: kandidat onset terverifikasi (481/329) + jalur termurah (nol parse) |

Kemampuan terukur hari ini (tanpa vonis biner):
1. RF mendeteksi status high_MSE LEBIH BAIK dari baseline "mengingat kedalaman" di **4/4 fold** (ΔB_vs_canary +0,058…+0,107) — fitur SPP/FLOW/MUD/GAM membawa sinyal di atas depth-only.
2. RF TIDAK menambah di atas rule persistence di **4/4 fold** (ΔB_vs_persistence −0,087…−0,381) — untuk tugas STATUS, rule sederhana "status jendela sebelumnya tetap" adalah engine terbaik terukur (AUPRC 0,679–0,984).
3. Nilai PdM sesungguhnya (peringatan dini masuk blok) ada di K-2 yang BELUM berangka; yang sudah ada = 481 kandidat onset (329 transisi dari blok normal) terverifikasi dua pihak (A1 skrip terbuka + PM reproduce).

---

## 1. ENGINE + JENIS TUGAS + BASELINE RELEVAN (per V8-R1 §2.3)

| Engine | Jenis tugas yang dikerjakan | Baseline relevan (per tugas ini, bukan universal) | Peran |
|---|---|---|---|
| RF (30 fitur window: SPP/FLOW/MUD/GAM/MD/TVD × mean/std/slope/last/frac; kanal pembentuk MSE DILARANG — E1d anti-sirkular PASS) | K-1 deteksi kondisi (status) · K-2 prediksi onset (dirancang, belum dijalankan) | (a) persistence-status; (b) canary-kedalaman; (c) prevalence-random (lift=1) | engine ML utama |
| Persistence-status (label(t−1)) | K-1 deteksi kondisi — sekaligus BASELINE jujur dan terbukti engine terbaik utk status | — | rule sederhana, nol training |
| Canary-kedalaman (skor kedalaman murni) | baseline "mengingat posisi" utk K-1 | — | pembanding memorisasi depth |
| Persistence-onset (label onset(t−1)) | baseline K-2 — **tes pembeda**: bila persistence-onset ≥ RF mayoritas → hipotesis "kegagalan V6 = formulasi status" DITOLAK | — | belum dihitung |

Jenih tugas yang TIDAK dikerjakan kelas ini: deteksi anomali (bukan domain `bit_wear`)
dan diagnosis (tidak ada label diagnosis di Volve utk kelas ini — identitas bit serial/
dull/footage dari EDM = BLOCKED, M2 §1b).

---

## 2. LAPISAN A — APAKAH DETEKSI BEKERJA

### 2.1 K-1 (status high_MSE) — TERUKUR (angka OBSERVED, dicocokkan ke artefak E1d)

| Fold uji (LOWO) | n / pos / prev | AUPRC RF [CI95] | lift | plafon lift (1/prev) | canary-depth | persistence | ROC-AUC RF (sekunder) |
|---|---|---|---|---|---|---|---|
| F-14 | 949 / 91 / 0,0959 | **0,298** [0,148; 0,517] | 3,11 | 10,43 | 0,191 | 0,679 | 0,863 |
| F-15 | 1.057 / 155 / 0,1466 | **0,365** [0,171; 0,582] | 2,49 | 6,82 | 0,288 | 0,698 | 0,789 |
| F-15S | 1.031 / 561 / 0,5441 | **0,813** [0,679; 0,938] | 1,495 | 1,84 | 0,756 | 0,984 | 0,874 |
| F-5 | 367 / 174 / 0,4741 | **0,783** [0,489; 0,945] | 1,65 | 2,11 | 0,692 | 0,870 | 0,812 |

Fold UNDERPOWERED (dilaporkan, tidak dihitung mayoritas): F-9_A (3 positif), F-7 (0), F-9 (0)
→ cakupan penilaian = 4 dari 7 sumur.

Turunan delta (DERIVED, dihitung dari angka di atas):

| Fold | ΔB_vs_canary = RF − canary | ΔB_vs_persistence = RF − persistence |
|---|---|---|
| F-14 | **+0,107** | −0,381 |
| F-15 | **+0,076** | −0,333 |
| F-15S | **+0,058** | −0,170 |
| F-5 | **+0,092** | −0,087 |

Penilaian A (kerangka V8-R1 §1.2, baseline relevan per tugas):
- **vs canary-kedalaman: ΔB > 0 di 4/4 fold layak** → RF BEKERJA di atas baseline
  "mengingat posisi" — sinyal fitur non-kedalaman (SPP/FLOW/MUD/GAM) nyata.
- **vs persistence-status: ΔB < 0 di 4/4 fold** → untuk tugas deteksi-status, RF
  "tidak menambah di atas baseline" (kemampuan dicatat, bukan gagal); **persistence
  = engine deteksi-status dengan AUPRC tertinggi terukur (0,679–0,984)** — inilah
  dasar objektif reframing ke onset (alasan V6 menurunkan verdict ke "layak bersyarat"
  per aturan pra-reg E1a §6 — dikutip sebagai PROVENANSI, bukan vonis dokumen ini).
- **Plafon lift**: fold prev tinggi (F-15S prev 0,544 → plafon 1,84; F-5 plafon 2,11)
  secara matematis tidak bisa mencapai lift jauh di atas 1,5 — fold "gagal ambang"
  1,495 mencapai AUPRC 0,813 dengan CI terketat (lebar 0,26). Sesuai aturan penilaian
  (V8-R1: jangan tuntut lift seragam tanpa alasan operasional) ini dilaporkan sebagai
  KONTEKS prevalensi, bukan penurunan ambang.
- **Precision / recall / FAR_t / waktu deteksi: BELUM TERUKUR** — metrik primer kampanye
  E1d adalah AUPRC; grep artefak `E1d_LOWO_RESULTS.json` (bukti ketiadaan): field
  precision/recall/FAR tidak ada. FAR tidak bisa diputar dari dokumen yang ada.

### 2.2 K-2 (onset-of-high-MSE, S-F1) — BELUM TERUKUR

Yang sudah ada (semua OBSERVED):
- **481 kandidat onset nyata, 329 di antaranya transisi dari blok normal** — diverifikasi
  A1 (skrip terbuka `a1_usrop_trans.py`) dan direproduksi PM (V7_PM §3 butir 5).
  (Angka lama M2 "1.489 transisi" = hitungan pra-filter; angka final = 481/329.)
- Desain label: onset = transisi masuk blok high_MSE pada grid 60 detik; jendela DALAM
  blok Dibuang (bukan negatif); jendela positif [t0−H, t0), H = 10 menit + sensitivitas
  30 menit (V8-R1 §2.3, R1 §6.2 S-F1).
- Jalur eksekusi termurah: relabel langsung dari `USROP_labeled.csv` (nol parse baru).

Yang BELUM TERUKUR (kampanye onset belum dijalankan — V7 Fase 1): lift_onset, precision,
recall (cakupan B1), FAR_t, T_lead, dan **persistence-onset** (baseline tes pembeda).
G1 V6 3/4 pada STATUS = konteks kemampuan fitur (OBSERVED), bukan hasil onset —
dilarang dipakai sebagai pengganti hasil K-2 (estimand berbeda, V7_PM §6).

---

## 3. LAPISAN B — APAKAH DETEKSI MEMBERI NILAI MAINTENANCE

| Ukuran | K-1 (status, terukur) | K-2 (onset, desain) |
|---|---|---|
| B1 cakupan peringatan-dini | Tidak berlaku-ukur: detektor status hanya MENGONFIRMASI setelah blok dimulai | **BELUM TERUKUR** — didesain utk % onset dengan alarm dalam [t0−10 mnt, t0) |
| B2 waktu-untuk-bertindak | Lead time masuk blok ≈ 0 selayaknya (DERIVED dari definisi tugas status; tidak diukur V6) | **BELUM TERUKUR** — anchor kategorikal: onset high_MSE = tanda keausan/balling → waktu menyesuaikan parameter / keputusan bit change (bukan SLA; V8-R1 §6.6) |
| B3 pengurangan pemeriksaan tak perlu | **BELUM TERUKUR** (tidak ada hitungan FP; aturan pembanding bit_wear belum didefinisikan spt VIBLAT-rule) | belum terukur |
| B4 margin status-awal | **BELUM TERUKUR** | tidak berlaku (kelas onset) |

Nilai maintenance yang BISA diklaim hari ini (jujur, tanpa angka baru):
1. **K-1/persistence** memberi konfirmasi-status berbiaya nol (AUPRC 0,679–0,984;
   DERIVED: deteksi transisi terlambat 1 jendela ≈ 10 menit — persis ketiadaan lead-time
   yang membuatnya bukan alat peringatan-dini).
2. **K-2 dirancang** untuk memberi peringatan 10 menit (sensitivitas 30 menit) sebelum
   masuk blok ineffisiensi — nilai ini REALISTIS terukur setelah kampanye dijalankan;
   481 onset = 481 kesempatan deteksi yang sudah terverifikasi ada dalam data.
3. Anchor preseden ilmiah (peringatan 2,67–7,37 menit sebelum stuck, Volve surface data
   [R1-S1 §2.2]) milik kelas stuck — dipakai hanya sebagai eksistensi-bukti bahwa
   peringatan menit-level dari data surface mungkin, BUKAN angka janji `bit_wear`.

---

## 4. LAPISAN C — CUKUP TEPERCAYA UNTUK DIPAKAI

| Ukuran | Nilai | Status |
|---|---|---|
| C1 stabilitas temporal | spread_AUPRC antar 4 fold layak = **0,515** (0,298–0,813) = LEBAR; lebar CI95 per fold 0,26–0,46 (n kecil) | Terukur — dianotasi: performa sangat tergantung sumur uji |
| C2 ketahanan lintas-regime (kedalaman/operasi) | RISIKO TERUKUR: SHAP K-1 didominasi 4 fitur teratas kedalaman (MD_last, MD_mean, TVD_mean, TVD_last — V6 §5) → model banyak "mengingat posisi"; canary-kuat (0,191–0,756) konsisten. ΔAUPRC per bin kedalaman/regime: **BELUM TERUKUR** | Terukur utk gejala; per-bin belum ada |
| C3 toleransi kualitas sensor (dropout/noise) | **BELUM TERUKUR** (uji dropout kanal SHAP-atas / noise σ/10 tidak dijalankan) | Belum |
| C4 transparansi ketidakpastian | **TERPENUHI** — CI95 dilaporkan semua 4 fold layak (meta artefak: n_boot 1000, block 20, seed 42); 3 fold UNDERPOWERED diberi label & dikecualikan mayoritas; LOWO (sumur tak terlihat = fold); anti-sirkular ditegakkan (kanal pembentuk MSE dilarang jadi fitur, asersi PASS) | Terukur |

Cakupan lintas-peralatan: 4/7 sumur layak dinilai (3 fold tanpa/cuma 3 positif) —
klaim ketahanan hanya berlaku pada 4 wellbore teruji (F-14, F-15, F-15S, F-5).

Mitigasi C2 yang disiapkan (data terverifikasi, performa BELUM ada):
- **R3 geologi-join** (M2 §2): `Well_picks` 409 pick / 35 well + flags `SAND_FLAG` 32.988 /
  `CARB_FLAG` 33.386 join ke USROP per MD → fitur geologi eksplisit melawan memorisasi
  kedalaman. Status: data dihitung dua pihak; join+uji performa = belum dijalankan.
- **S-F2 silang MSE/DS** (Menand & Mills: MSE↑ + MSE/DS↓ = keausan/balling): label lebih
  bersih dari blok MSE murni; USROP WOB/ROP/RPM/MSE 100% non-null. Status: rumus
  terverifikasi R1 run-3; kampanye belum dijalankan.

---

## 5. BATAS PENGGUNAAN (eksplisit, per engine/klaim)

| Engine / klaim | LAYAK untuk | BELUM layak untuk | Dasar |
|---|---|---|---|
| **RF K-1 (status)** | **Tren/pemantauan + screening** blok ineffisiensi pada 4 wellbore teruji (indikasi "sedang di zona high-MSE relatif", tampilan tren) | Alarm otomatis (A: kalah persistence 4/4; P/R/FAR belum terukur → syarat §4 FAR ≤1/24 jam tidak bisa ditunjukkan); peringatan dini (lead time ≈ 0 by construction) | §2.1 |
| **Persistence K-1 (status)** | **Konfirmasi-status + lapisan rule termurah** (AUPRC 0,679–0,984 terukur) | Peringatan dini masuk blok (transisi terdeteksi +1 jendela ≈ 10 menit TERLAMBAT — DERIVED); alarm onset | §2.1 |
| **Canary-kedalaman** | Baseline jujur "mengingat posisi" — tetap dipertahankan sebagai pembanding di setiap kampanye baru | Engine pemakaian mandiri (kalah RF 4/4) | §2.1 |
| **RF-onset K-2 (S-F1)** | **BELUM BOLEH DIPAKAI DI TINGKAT PUNCA** — bahkan tren menunggu kampanye dijalankan. Yang layak dipakai hari ini = kandidat onset 481/329 (inventaris peristiwa terverifikasi) + rencana pra-reg Fase 0 | Semua tingkat pemakaian engine sampai ada angka A/B/C | §2.2 |
| **Hybrid layak dipertimbangkan (usulan arsitektur)** | Rule persistence (status) sebagai layer dasar + RF-onset (jika kampanye K-2 terbukti) sebagai layer peringatan | — | §2–§4 |

Tidak ada klaim "alarm kritis otomatis" untuk kelas ini hari ini; syarat ambang-atas
(V8-R1 §4: G1 mayoritas + G2 + B1 ≥80% + T_lead ≥ anchor + FAR ≤1/24 jam) belum ada
yang bisa ditunjukkan untuk `bit_wear` — bukan penurunan ambang, melainkan pemenuhan
yang tertunda kampanye K-2.

---

## 6. KEKUATAN BUKTI

| Klaim | Kekuatan | Dasar |
|---|---|---|
| RF-beats-canary 4/4 (K-1) | **KUAT** | Pra-reg E1d di-hash sebelum training (SHA-256 986f45a1…); artefak primer JSON per fold; LOWO; CI95 bootstrap |
| Persistence-beats-RF 4/4 (K-1) | **KUAT** | Idem; persistence dihitung pada fold yang sama (n_persistence = n−1 per fold, lag-1) |
| Inventaris onset 481/329 (K-2) | **SEDANG-KUAT** | Dua pihak independen (skrip A1 terbuka + reproduce PM); hitungan pra-filter 1.489 (M2) sudah dikoreksi & direkonsiliasi (V7_PM §3.5) |
| Performa engine onset (K-2) | **BELUM ADA BUKTI** | Kampanye belum dijalankan — semua metrik = belum terukur |
| Mitigasi geologi-join (R3) menaikkan C2 | **KANDIDAT** | Ketersediaan data terverifikasi (409 picks, 33 rb flags); efek performa belum diuji |

Validitas data & temporal: label dari kanal berbeda dari fitur anti-sirkular (E1d);
fitur jendela lampau / label jendela depan; LOWO anti-pseudoreplication; agregat 1 menit
kehilangan variasi sub-menit (batas desain V6 §6.7 — berlaku juga untuk K-2).

---

## 7. DAFTAR "BELUM TERUKUR" + TES PEMBEDA

Belum terukur (dilarang diisi angka tanpa kampanye baru): precision K-1/K-2 · recall K-1/K-2 ·
FAR_t/FAR_w K-1/K-2 · T_lead K-2 · B1/B3/B4 · persistence-onset (baseline tes pembeda) ·
ΔAUPRC per bin kedalaman/regime (C2 per-bin) · dropout/noise (C3) · performa join geologi R3.

Tes pembeda yang mengikat evaluasi berikutnya:
1. **Persistence-onset ≥ RF mayoritas fold** → hipotesis "akar kegagalan V6 = formulasi
   status" DITOLAK; penyebab pindah ke "sinyal fitur lemah untuk onset" (V8-R1 §2.3).
2. **Fitur geologi R3 tidak menurunkan dominasi MD/TVD pada SHAP kampanye K-2** →
   risiko C2 "mengingat posisi" berdiri dikonfirmasi → pemakaian tetap di level tren.
3. **FAR_t K-2 ≤ 1 per 24 jam operasi negatif** → satu-satunya jalan klaim "layak alarm
   otomatis" (V8-R1 §4) — tanpa ini, semua hasil K-2 tetap di tingkat tren/peringatan.

---

## Sources (angka primer — tanpa karangan)

- `docs/V6_E1_ML_DESIGN.md` §4.3 (tabel LOWO bit_wear), §5 (SHAP MD/TVD), §6.1 (kelemahan
  jujur persistence 4/4), §2 (definisi 7 kelas), §3 (pra-reg).
- `scratch/v6_e1/E1d_LOWO_RESULTS.json` (artefak primer: koordinat persis per fold,
  verdict block, meta bootstrap 1000/20/42, daftar 30 fitur) + `E1d_LOWO_RUN_LOG.txt`.
- `docs/V6_E1d_PREREG_BITWEAR.md` (SHA-256 986f45a1fbf866434e05b3aecfbc8c53fa1672e2caef98d7470a38ea8c03f1a6).
- `docs/V7_PM_VERDICT.md` §3 butir 5 (onset 481/329 diverifikasi A1+PM; koreksi M2 1.489),
  §0 (jalur bit_wear = kandidat TINGGI), §7 Fase 1.
- `docs/V7_R1_SOLUTIONS.md` §6.2 (S-F1/S-F2), §5.3 (S-D3 MSE/DS Menand & Mills).
- `docs/V7_M2_SYNTHESIS.md` §2 relasi R3 (picks 409/35 well; SAND 32.988/CARB 33.386),
  §1 tabel S-F1 (198.928 baris USROP, transisi 1.489 pra-filter), §1b (identitas bit
  serial/dull/footage EDM = BLOCKED → tidak ada tugas diagnosis/identitas di kelas ini).
- `docs/V8_R1_ABC_SPEC.md` §1.2–1.4 (rumus A/B/C), §2.3 (spesifikasi `bit_wear`),
  §4 (ambang tren vs alarm otomatis).
