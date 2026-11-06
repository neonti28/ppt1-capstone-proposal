# V9-EVAL_C — PENILAIAN LAPISAN C UNTUK 7 ENGINE (kerangka operator A/B/C)

Status: HASIL EVALUASI (kemampuan + batas penggunaan + kekuatan bukti per engine —
**BUKAN vonis LULUS/GAGAL**).
Sumber angka: JSON primer `scratch/v9_eval_c/v9_eval_c_RESULTS.json`
(turunan mekanis dari `scratch/v9_e_ml/*.json`, `scratch/v9_e_stat/*.json`,
`scratch/v9_e_rule/*.json` — semua angka dihitung dari eksekusi nyata).
Dihitung oleh skrip `code/v9_eval_c_01_compute.py`; verifikasi independen
`code/v9_eval_c_02_verify.py`: **13/13 PASS** (§5).

## Baris riset pendahuluan

- Riset pendahuluan: scientific-critical-thinking — Layer C bukan "model bagus/tidak"
  melainkan "kepercayaan pemakaian":HIPOTESIS terpusat = engine layak dipakai bila
  perilakunya STABIL antar well/periode dan ketidakpastiannya TRANSPARAN; hipotesis
  alternatif (ambang global portable; persistence-horizon sbg bukti; "belum terukur" = gagal)
  diuji lalu ditolak/direserve berdasar angka, bukan dilindungi.
- Riset pendahuluan: verification-mandatory — SEMUA metrik C dikomputasi ulang dari JSON
  primer dengan skrip terpisah (13 check lolos, termasuk rekonsiliasi 3/7 layak + 2 UP
  = 5/9 EVAL_A untuk CI ssi, dan Wilson CI dihitung dari TP/FP mentah); selisih hash
  `_det_a` vs main E_STAT = **hanya `elapsed_s`** (dibuktikan lewat deep-diff struktural);
  daftar "belum terukur" terpisah dari "gagal" (§6).
- Riset pendahuluan: statistical-analysis — dispersi antar-fold dilaporkan sebagai
  min/median/maks + rasio maks/min (bukan satu titik); Wilson CI95 utk proporsi dari
  hitungan mentah (TP/FP/FN); fold UNDERPOWERED dilabeli dan tidak dihitung mayoritas;
  rasio dispersion dipakai sbg ukuran portabilitas, bukan p-value.
- Riset pendahuluan: what-if-oracle — 6 cabang diuji: Ω "kalibrasi ambang per-well
  prospektif memperbaiki portabilitas" (belum terukur → rekomendasi, bukan klaim),
  α "tier = rule/persistence sbg lapisan alarm-paruh + ML sbg ranking" (DIPILIH),
  Δ "RF shk sbg alarm otomatis" (CI memuat prev 7/9, B3 −212× → ditolak),
  Φ "persistence-HORIZON sbg dasar klaim" (hindsight → dibuang, dipakai sbg batas-atas),
  Ψ "tuntut CI sempit utk n fold kecil" (tidak realistis; dilaporkan lebar CI apa adanya),
  ∞ "engine tanpa TP/FP = gagal" (ditolak: bit_wear = belum terukur).
- Riset pendahuluan: consciousness-council — 5 arketipe mempertahankan ketegangan:
  (Empiricist) hyd K-i hybrid & tool_wear FAR-terkalibrasi = dua engine paling stabil
  lintas alat/periode (CI 0/9 memuat prev; FP-cut 9/9 konsisten; TLead 20–36 dtk di 4/4 alat);
  (Contrarian) ambang RF vib menyebar 119× antar well → portabilitas ambang global
  TERBANTAH; (Pragmatist) lapisan alarm harian harus rule/persistence (transparan,
  deterministik), ML untuk ranking/tren; (Architect) akar masalah C = prevalence beda
  40× antar well + kanal sensor absen (ssi nodata 62%) + anchor onset absorbed 4,6%;
  (Historian) pola V8 terulang (B3 RF shk negatif lagi) → ketidakstabilan RF shk kronis.
- Riset pendahuluan: sequentialthinking — 4 pikiran: (1) scope + inventaris data,
  (2) desain metrik C1–C5 dari struktur JSON nyata, (3) sintesis council/what-if +
  keputusan tier pemakaian, (4) gerbang verifikasi sebelum dokumen ditulis.

---

## 0. METODE PENILAIAN LAPISAN C

Kerangka (operator, "Evaluasi User.txt" via PM1 §4.7): **Lapisan C = cukup tepercaya
untuk dipakai?** — ketahanan lintas periode/kondisi/peralatan, kualitas sensor,
perubahan operasi, ketidakpastian ditangani. Definisi metrik (pra-komputasi, EC-2):

| Metrik | Definisi operasional | Kelas |
|---|---|---|
| **C1 ketahanan** | dispersi metrik kunci antar fold LOWO (min/median/maks + rasio maks/min) + fraksi fold mengalahkan baseline relevan + fold terburuk | semua dgn fold |
| **C2 ketidakpastian** | CI95 AUPRC dari JSON: apakah memuat prevalensi (no-skill); utk E_RULE (tanpa CI tersimpan) → **Wilson CI95** dari TP/FP/FN mentah | semua |
| **C3 portabilitas ambang** | pada tau TETAP: sebar FAR/recall antar well + jumlah well dgn FAR≤6 & recall>0; konsistensi pemangkasan FP hybrid antar fold | ML + hybrid |
| **C4 kualitas sensor** | n_nodata, anchor onset hilang (ABSORBED), sign-flip jendela, kanal absen | per kelas |
| **C5 determinisme** | rerun identik (hash/semantik) — fondasi kepercayaan angka | semua tim |

Keputusan evaluasi (mengikuti dokumen ini):

| # | Keputusan | Alasan |
|---|---|---|
| EC-1 | 7 engine = **11 klaim** (mengikuti EA-1/EB-1) | klaim terpisah punya tugas, label, baseline berbeda |
| EC-2 | Baseline Layer C = **baseline relevan per tugas** (dispersi persistence/rule/canary pada fold yang sama) — bukan satu baseline universal | aturan operator: jangan tuntut standar identik |
| EC-3 | Fold UNDERPOWERED dilabeli; fraksi dihitung pada fold layak, angka all-fold juga dilaporkan bila berbeda | anti rata-rata menipu (SSA ssi 3/7 layak vs 5/9 all) |
| EC-4 | "Portabel" operasional = ambang tetap menghasilkan FAR≤6 dgn recall>0 di ≥50% fold layak; ini band PENILAIAN, bukan vonis | gerbang LAYER-1 PM1 §1.3 sbg acuan praktis |
| EC-5 | CI memuat prevalensi = **sinyal tidak terbukti** di fold itu (bukan kegagalan engine) | no-skill tak terbedakan |
| EC-6 | Tier pemakaian (TREN / PERINGATAN-BERPENGAWAS / ALARM-OTOMATIS) ditetapkan dari gabungan bukti A+B+C, mengutamakan keamanan: bukti C lemah → tier lebih rendah | alat PdM boleh berguna tanpa alarm otomatis (PM1 §4.7) |
| EC-7 | Angka **V8** = referensi terpisah (EA-7): RF hyd_K-ii, RF bit_wear, RF tool_wear_K-ii belum dijalankan di V9 | jangan campur eksekusi & rujukan |
| EC-8 | Tidak ada vonis biner; "belum terukur" ≠ "gagal"; korelasi ≠ kausalitas | aturan penilaian operator 1–6 |
| EC-9 | Tier = **KEPUTUSAN AKHIR EVAL_C** di tabel §1; justifikasi angka per klaim di §2 | output sesuai tugas |

Cakupan eksekusi: E_ML 28 fold (vib 4, ssi 9, shk 9, stuck_k2 4) × 3 model;
E_STAT 4 engine (hyd_ki 9 fold, stuck_E2 4 fold, tool_wear 8 run/4 alat, fisher 1 split);
E_RULE 37 fold rig + 7 fold bit_wear + 4 fold tool_wear + 1 split hyd_kii.

---

## 1. TABEL RINGKAS — 7 ENGINE, 11 KLAIM (LAPISAN C + TIER PEMAKAIAN)

Legenda tier: **TREN** = pemantauan tren/ranking (tidak utk keputusan inspeksi otomatis);
**PERINGATAN-BERPENGAWAS** = peringatan bernilai tapi wajib konfirmasi manusia;
**ALARM-OTOMATIS** = boleh memicu tindakan tanpa konfirmasi (syarat: C stabil + A/B memadai).

| Engine / klaim | C1 ketahanan antar-well | C2 ketidakpastian | C3 portabilitas ambang | C4 sensor | **TIER** | Kesimpulan kemampuan / batas |
|---|---|---|---|---|---|---|
| **vib** (K tunggal) | RF AUPRC 0,441–0,912 (2,07×); ΔB RF vs canary **4/4**, vs persistence 2/4; rule P stabil 0,87–0,95 (1,1×) | CI RF memuat prev **0/4** (sinyal terbukti di semua fold) | **TIDAK PORTABEL**: τ0,5 FAR 4,1–496 (**119×**), well FAR≤6 1/4; rule FAR 10–50 (5×) | n_nodata rule 356/1.989 (F-14) | **TREN** (RF ranking) + **PERINGATAN-BERPENGAWAS** (rule) | **Memenuhi C utk ranking stabil di atas canary (4/4) & deteksi rule berpresisi (P 0,87–0,95 di 4 well)**; **belum** utk ambang global (FAR menyebar 119×) → ambang wajib kalibrasi per-well sebelum dipakai sbg alarm |
| **ssi** (K tunggal) | RF AUPRC 0,015–0,459 (**30×**); ΔB vs prevalensi 7/7, vs canary 5/7, vs persistence 6/7 | CI memuat prev **3/7 layak** (5/9 all) | τ0,3 FAR 0–15,6; well FAR≤6 2/7; hybrid **≤ rule di 7/7 fold layak** (memotong **6/7**; F-14 tie 0→0; total −73,1%) | **n_nodata 22.385/35.906 = 62,3%** (CRPM absen) | **TREN** (RF) + **PERINGATAN-BERPENGAWAS hemat** (hybrid: FP 26→7) | **Memenuhi C utk hybrid hemat-pemeriksaan (konsisten tak memburuk di 7/7 well; memotong di 6/7) & ranking di atas prevalensi**; **belum** utk detektor andal per well (30× spread; nodata 62% = keterbatasan sensor, bukan murni model); 2 fold UP dilabeli |
| **shk** (K tunggal) | RF AUPRC 0,007–0,193 (**28×**); ΔB vs prevalensi 9/9, vs persistence 4/9; **rule FAR 0,67–6,6 (9,9×) → lolos FAR≤6 di 7/9 fold** | CI RF memuat prev **7/9** (sinyal lokal-wellbore) | RF praktis memancar; rule: FAR≤6 di mayoritas well tanpa kalibrasi | n_nodata 6.831/56.495 = 12,1% | **PERINGATAN-BERPENGAWAS** (rule) + **TREN** (RF) | **Memenuhi C utk rule sbg lapisan dasar berbiaya-terkendali lintas 7 well** (satu-satunya kelas rig dgn mayoritas fold FAR≤6); **belum** utk RF (CI 7/9 memuat no-skill; B3 EVAL_B −212× = pola V8 berulang) |
| **stuck K-i** (status) | hanya **2 fold** (F-14, F-9_A): rule P 0,92–0,97 (1,05×), FAR 8,3–61 (7,3×) | Wilson CI presisi lebar (n kecil) | cakupan 2 well saja → portabilitas BELUM TERUKUR | anchor onset gap = kelas K-ii | **PERINGATAN-BERPENGAWAS** (cakupan terbatas) | **Memenuhi C untuk 2 well yang diuji (presisi konsisten 0,92–0,97)**; **belum terukur** utk well lain (cakupan 2 fold = kekuatan bukti terbatas); replikasi F-9/F-10/F-15 diperlukan |
| **stuck K-ii** (onset) | persistence-EVENT B1 0–0,115 · TLead 4,5–8,5 mnt (1,89×); E1 B1 0–0,066; RF τ0,5 B1 0–0,045 | E2 CI memuat prev **4/4** (tidak terbukti); RF 1/4 | E1 FAR 2,1–29,0 (**13,9×**); persistence-EVENT FAR 0–2,9 (3 fold ≤2,9) | **anchor absorbed 13/281 = 4,6%** onsets (absorber delta 2–7 mnt) | **TREN / triage risiko** | **Memenuhi C utk persistence-EVENT sbg peringatan-dini berbeban rendah dgn arah benar (TLead median 7,0 mnt ≈ anchor 2,67–7,37 mnt, konsisten 3 well)**; **belum** utk alarm (B1 hanya 0–11,5%); E2 tidak terbukti (CI 4/4); anchor gap 4,6% = ketidakpastian label yang harus dilaporkan |
| **hyd K-i** (status) | persistence AUPRC 0,425–0,843 (2×); hybrid P 0,72–0,95 di **9/9 well**; FP-cut **2091→927 (−55,7%) konsisten 9/9** | CI persistence memuat prev **0/9** (terbukti di semua fold) | hybrid FAR 14,6–58,4 (4×); delay deteksi median 0–3,5 mnt stabil | label = residu SPPA (**proxy**, anotasi wajib) | **PERINGATAN-BERPENGAWAS** (kandidat terkuat) | **Memenuhi C paling lengkap di antara kelas status**: deteksi stabil 9 well, CI tidak menyentuh no-skill, pemangkasan FP konsisten, delay ≤3,5 mnt; **belum** utk ALARM-OTOMATIS (FAR 14,6–58 > 6 di 9/9) — naik tier bila kalibrasi per-well terukur |
| **hyd K-ii** (prediksi) | 1 split temporal → dispersi antar-periode TIDAK TERUKUR | CI fisher [0,0025;0,0684] **memuat prev 0,0037** | q95: P=R=0 (0 TP, FP 177) | **sign-flip 6.377/8.107 = 78,7% jendela**; FlowOut absen | **BELUM LAYAK PAKAI** (eksplorasi) | **Belum memenuhi C**: bukti = 1 split, sinyal tidak terbukti (CI memuat no-skill), fisika korrelasi tidak stabil (78,7% jendela berbalik tanda); **kendala sensor (FlowOut absen) = penyebab terukur, bukan kegagalan metode**; RF V8 (B1 66,7%) tetap referensi, belum diulang |
| **bit_wear K-1** (status) | persistence AUPRC 0,119–0,984 (**8,3×**); ΔB vs canary **5/5 scorable**; lift 1,81–10,67 | CI: **belum terukur** (JSON tanpa CI; P/R/FAR juga tidak ada) | persistence = ambang tetap y(t−1) → portabilitas terbatas sifat metode | dataset **USROP ≠ rig Volve** (transfer lintas-dataset) | **TREN** | **Memenuhi C terbatas utk ranking di atas canary/prevalensi di 5 well scorable (5/5)**; **belum terukur** utk CI/P/R/FAR (field tidak ada); 2 fold 0 positif = tak scorable; **K-2 onset belum dijalankan** (pra-reg belum terbit) |
| **tool_wear K-i** (regime) | deteksi 4/4 alat; TLead 20–36 dtk (**1,8×**, paling ketat); cross-family spread 8–40 dtk | 8/8 run signifikan p≤0,002; **precision run 0,50** (4 FP di alat baru) | FAR-terkalibrasi FP 1–3/alat dgn threshold per-alat (kalibrasi dalam-run = sifat desain) | tes artefak termal **0/8** (transisi nyata) | **PERINGATAN-BERPENGAWAS** (bengkel) | **Memenuhi C utk deteksi perubahan-regime bengkel pada FAR-terkalibrasi: stabil 4 alat (TLead 1,8×, FP 1–3), bekal uji pembeda lolos**; **belum** utk klaim "deteksi keausan spesifik" (cp juga signifikan di alat baru → precision 0,50); **batas: domain bengkel, transfer ke rig TIDAK diklaim** (D-A7) |
| **tool_wear K-ii** (lintas-alat) | canary AUPRC 0,516–0,612 (**1,19×** — baseline stabil antar alat); identity = prev (plafon lift 2,0) | **belum terukur** utk RF (V9 tidak menjalankan; V8 = referensi) | LOTO 4 fold; persistence N/A dinyatakan | label konstan dalam run (by design) | **TREN** | **Memenuhi C utk baseline ranking lintas-4-alat yang stabil (1,19×)**; **belum terukur** utk engine RF di V9 (kekuatan bukti = referensi V8); precision biner V8 0,50–0,56 ≈ peluang → jangan sbg alarm |

**Temuan pusat Layer C**: TIDAK ada engine yang memenuhi syarat ALARM-OTOMATIS penuh
(C stabil + A FAR≤6 + B beban wajar bersamaan). Dua engine paling tepercaya —
**hyd K-i hybrid** (CI 0/9 memuat no-skill; FP-cut 9/9; delay ≤3,5 mnt) dan
**tool_wear K-i FAR-terkalibrasi** (deteksi 4/4 alat; TLead 1,8×; FP 1–3) — layak
PERINGATAN-BERPENGAWAS sekarang dan merupakan kandidat naik-tier bila ambang
dikalibrasi per-well/alat secara prospektif (EC-9). Kegagalan C paling umum =
**portabilitas ambang global** (vib 119×, shk CI 7/9), bukan kegagalan deteksi.

---

## 2. DETAIL PER ENGINE (angka JSON)

### 2.1 `vib` — TIER: TREN (RF) + PERINGATAN-BERPENGAWAS (rule)

| Sisi C | Angka (JSON) |
|---|---|
| C1 RF | AUPRC 0,441–0,912 (med 0,527, 2,07×); ΔB vs canary **4/4** (0,104–0,299), vs prevalensi 4/4, vs persistence **2/4** (−0,227…+0,119) |
| C1 rule | P 0,87–0,95 (1,1× — stabil); R 0,28–0,60 (2,2×); FAR 10,0–49,9 (5,0×); FP total 197 |
| C2 | CI95 RF memuat prevalensi **0/4** → sinyal ranking terbukti di semua fold; Wilson CI presisi rule per well = [0,82–0,99] kelas (n TP+FP ratusan) |
| C3 | τ0,05: FAR 983–1440 (0 well ≤6); τ0,3: 189–699 (0/4); **τ0,5: 4,1–496 = 119×** (1/4 well). Recall τ0,5 0,10–0,87 (8,5×) |
| C4 | n_nodata rule F-14 356/1.989; prevalensi antar well 0,14–0,57 (4×) = akar ketidakportabelan |

Kesimpulan: ranking RF **tepercaya utk tren/penambah ranking** (CI 0/4 no-skill; ΔB canary 4/4);
rule **tepercaya sbg peringatan berpengawas** (presisi stabil 1,1× antar well).
**Belum** utk ambang alarm global: satu ambang τ menghasilkan FAR 119× antar well →
syarat C3 gagal. Rekomendasi: kalibrasi ambang per-well (D-A4) sebelum naik tier.

### 2.2 `ssi` — TIER: TREN (RF) + PERINGATAN-BERPENGAWAS hemat (hybrid)

| Sisi C | Angka |
|---|---|
| C1 RF | AUPRC 0,015–0,459 (**30,4×** — tertinggi di kelas rig); ΔB vs prevalensi **7/7**, vs canary 5/7 (−0,016…+0,112), vs persistence 6/7 |
| C1 hybrid | FP 26→7 (**−73,1%**) — **< rule di 6/9 fold, = rule 3/9 (tie), 0 lebih buruk** (7/7 fold layak ≤ rule); FAR hybrid 0–3,7 |
| C2 | CI RF memuat prev **3/7 layak** (F-12, F-14, F-9_A) + 2/2 UP = **5/9 all** (reconcile dgn EVAL_A ✓) |
| C3 | τ0,3: FAR 0–15,6, well FAR≤6 **2/7**; τ0,5: recall RF 0 di semua fold (model tidak menyala) |
| C4 | **n_nodata 22.385/35.906 = 62,3%** — recall rendah sebagian besar keterbatasan kanal CRPM, bukan murni model |

Kesimpulan: hybrid **memenuhi C utk pengurangan pemeriksaan** (konsisten 7 well);
RF **memenuhi C utk ranking** di atas prevalensi. **Belum** utk detektor andal per well
(spread 30×; 62% baris tanpa data sensor). Fold UP (F-7 3 pos, F-9 12 pos) dilabeli.

### 2.3 `shk` — TIER: PERINGATAN-BERPENGAWAS (rule) + TREN (RF)

| Sisi C | Angka |
|---|---|
| C1 rule | FAR 0,67–6,6 (9,9×) tapi **≤6 di 7/9 well** (satu-satunya kelas rig dgn mayoritas lolos); P 0,00–0,94; FP total 121; n_nodata 12,1% |
| C1 RF | AUPRC 0,007–0,193 (28,1×); ΔB vs prevalensi 9/9, vs persistence **4/9** |
| C2 | CI RF memuat prev **7/9** → RF tidak terbukti di 7 well; sinyal lokal-wellbore |
| C3 | RF τ0,3: FAR 0–96,5 (well ≤6: 1/9); rule tanpa kalibrasi pun lolos mayoritas |
| C5 | (konsisten V8: B3 RF −212× V9 vs −0,11…−53,75 V8 → ketidakstabilan kronis) |

Kesimpulan: **rule memenuhi C sbg peringatan berpengawas lintas 7 well** (FAR terkendali
 mayoritas well tanpa kalibrasi). **RF belum memenuhi C** (CI 7/9 no-skill; konsisten
 pola V8) → batas: jangan sbg alarm.

### 2.4 `stuck` — K-i TIER: PERINGATAN-BERPENGAWAS (terbatas 2 well); K-ii TIER: TREN/triage

**K-i**: 2 fold only. Rule P 0,92–0,97 (1,05× — sangat konsisten), FAR 8,3–61,0 (7,3×),
Wilson CI presisi per well [0,82;0,99] & [0,87;0,99] (n TP+FP 54–60). → **memenuhi C utk
2 well yang diuji**; portabilitas ke well lain **belum terukur** (cakupan 2/9 well).
**K-ii**:
- persistence-EVENT: B1 0–0,115 (med 0,051), **TLead med antar-fold 4,5–8,5 mnt (med 7,0; 1,89×)**, FAR 0–2,9, FP alarm total 11 → arah benar, beban wajar, konsisten 3–4 well.
- E1: B1 0–0,066, TLead 1–5, FAR 2,1–29,0 (**13,9×**), FP 422.
- E2 (STAT): CI memuat prev **4/4**, lift 1,06–1,80, FAR 2,4–73,6 (**31×**).
- persistence-HORIZON: B1 0,93–0,97, FAR 0 — **HINDSIGHT** (label kontigu), dipakai sbg batas-atas saja.
- C4: **anchor onset absorbed 13/281 = 4,6%** (per well: F-9 3/55, F-9_A 4/72, F-10 2/93, F-14 4/61; absorber delta 2–7 mnt) → ketidakpastian anchor yang dilaporkan, bukan disembunyikan.

Kesimpulan: **persistence-EVENT memenuhi C sbg peringatan-dini berbeban-wajar dgn
ketidakpastian transparan** (B1 kecil = batas kuantitatif, anchor gap 4,6%).
**Belum** utk alarm (syarat B1≥80% jauh tercapai hanya oleh hindsight).

### 2.5 `hyd` — K-i TIER: PERINGATAN-BERPENGAWAS (kandidat terkuat); K-ii TIER: belum layak pakai

**K-i**:
| Sisi C | Angka |
|---|---|
| C1 hybrid | P 0,72–0,95 (1,31×) di **9/9 well**; R 0,52–0,87; FAR 14,6–58,4 (4,0×); FP 2091→927 (−55,7%) **konsisten 9/9** |
| C1 persistence | AUPRC 0,425–0,843 (1,98×); FAR 32,2–109,7 (3,42×) |
| C2 | CI95 persistence memuat prev **0/9** — satu-satunya kelas rig dgn no-skill tak terkandung di semua fold |
| C3/C4 | delay deteksi median 0–3,5 mnt; terdeteksi ≤H10 31,6–65,4%; label = residu SPPA (proxy — anotasi wajib) |

Kesimpulan: **memenuhi C paling lengkap** (9 well, CI bersih, FP-cut konsisten, delay kecil).
**Belum** ALARM-OTOMATIS: FAR >6 di 9/9 → peringatan berpengawas manusia.

**K-ii**: 1 split temporal; fisher varian AUPRC 0,022 CI [0,0025;0,0684] **memuat prev**;
q95 → TP 0, FP 177; **sign-flip 78,7% jendela** (6.377/8.107) → korelasi tidak stabil;
FlowOut absen (kendala sensor terukur). RF V8 (B1 66,7%, 3 onset) = referensi.
→ **belum memenuhi C** utk pemakaian; layak eksplorasi bila GAINLOSSTOT diparse.

### 2.6 `bit_wear` — TIER: TREN (K-1); K-2 belum dijalankan

5/7 fold scorable; persistence AUPRC 0,119–0,984 (**8,3×**); lift 1,81–10,67;
ΔB vs canary **5/5** (canary sendiri 42,7× — kedua metrik sama-sama menyebar);
2 fold 0 positif (tak scorable); 3 fold UP. **P/R/FAR/CI = belum terukur** (field tidak
ada di JSON, konsisten EVAL_A §2.6). Dataset USROP ≠ Volve → C lintas-dataset belum terukur.
Kesimpulan: **memenuhi C terbatas utk ranking di 5 well scorable**; tier TREN.

### 2.7 `tool_wear` — K-i TIER: PERINGATAN-BERPENGAWAS bengkel; K-ii TIER: TREN

**K-i**:
| Sisi C | Angka |
|---|---|
| C1 | deteksi R02 **4/4 alat**; TLead 20–36 dtk (med 24,5; **1,8×** — dispersi terkecil antar engine); FP 1–3/alat (3×) |
| C2 | cp signifikan **8/8 run** (p≤0,05 & p≤0,002); precision run 0,50 (4 FP alat baru) → ketidakpastian spesifisitas terukur |
| C5/C4 | tes artefak termal 0/8; cross-family spread 8–40 dtk (16,5 dtk med) |

Kesimpulan: **memenuhi C utk lingkup bengkel** (4 alat, stabil, uji pembeda lolos).
**Belum** utk "deteksi keausan spesifik" (precision 0,50) dan **TIDAK diklaim utk rig** (D-A7).

**K-ii**: LOTO 4 fold; canary 0,516–0,612 (**1,19×** — baseline lintas-alat stabil);
identity-majority = prev (plafon lift 2,0); persistence N/A dinyatakan (label konstan).
RF V9 belum dijalankan → **belum terukur** utk engine; angka V8 (ΔB 4/4, precision 0,50–0,56)
= referensi. Tier TREN.

---

## 3. SINTESIS: MENGAPA TIDAK ADA ALARM-OTOMATIS (what-if Δ & council)

Uji cabang Δ ("pasang RF shk/vib sbg alarm otomatis"): dari JSON — shk RF CI memuat
prevalensi 7/9 well + B3 EVAL_B −212×; vib RF τ0,5 FAR menyebar 119× → alarm otomatis
akan menambah 10–488× pemeriksaan di well buruk tanpa jaminan deteksi di well baik.
Ditolak berdasar angka. Cabang Ω ("kalibrasi per-well prospektif"): belum terukur di V9 —
dicatat sbg REKOMENDASI (D-A4 diuji prospektif, bukan klaim). persistence-HORIZON
(B1 0,93–0,97, FAR 0) = hindsight, dipakai sbg batas-atas teori, bukan dasar tier.

## 4. REKOMENDASI NAIK TIER (bukan janji — syarat terukur)

| Engine | Syarat naik ke ALARM-OTOMATIS | Bukti saat ini |
|---|---|---|
| hyd K-i hybrid | ambang dikalibrasi per-well → FAR≤6 di ≥7/9 well dgn P/R ≥0,5 | FAR 14,6–58,4 (9/9 well) |
| tool_wear K-i | precision run ≥0,8 (spesifisitas keausan) | 0,50 (cp juga nyata di alat baru) |
| vib/shk RF | kalibrasi per-well + CI tidak memuat prev di ≥75% fold | vib 4/4 CI, tapi FAR 119×; shk 2/9 CI |

## 5. VERIFIKASI (verification-mandatory)

`code/v9_eval_c_02_verify.py`: **13/13 PASS** — recompute terpisah dari JSON mentah:
V1/V1b FAR dispersion vib τ0,5 (min & maks eksak) · V2 shk CIprev 7/9 ·
**V3 rekonsiliasi ssi: 3/7 layak + 2 UP = 5/9 == EVAL_A** · V4 Wilson CI shk F-10
([0,138;0,500] dari TP=6 FP=15) · V5 hyd_ki FP 2091→927 · V6 anchor gap 13/281 ·
V7 TLead tool_wear {20,24,25,36} · V8 sign-flip 0,7866 · V9 bitwear 5/5 ·
**V10 E_STAT determinisme: deep-diff 4/4 file = hanya `elapsed_s`** (selisih hash awal
`_det_a` = timestamp komputasi, BUKAN angka — dilaporkan apa adanya) · V11 E2 4/4 ·
V12 hyd_ki 0/9. C5 E_ML: `max_abs_diff 2,2e-16` (machine epsilon) = numerik identik.

**Selisih yang ditemukan & dilaporkan**: (1) hash `_det_a` ≠ main E_STAT → deep-diff
membuktikan satu-satunya selisih `elapsed_s` (bukan hasil); (2) CIprev ssi dilaporkan
EVAL_A sbg 5/9 (all-fold) sedangkan hitungan fold-layak = 3/7 — keduanya benar bila
denominator dinyatakan (V3); (3) `determinism_check` E_ML vib `rerun_identical=False`
dgn selisih 2,2e-16 → ditandai "numerik identik", bukan "identik bit".

## 6. BELUM DIVERIFIKASI / BELUM TERUKUR (verification-mandatory #3)

- **Belum terukur (bukan gagal)**: CI/P/R/FAR bit_wear K-1; K-2 onset; RF hyd_K-ii,
  RF bit_wear, RF tool_wear_K-ii versi V9; portabilitas ambang stuck_K-i (>2 well);
  ketahanan hyd_K-ii antar-periode (1 split); kalibrasi per-well prospektif (D-A4).
- **Belum dicek evaluator ini**: rerun ulang E_RULE (mengikuti laporan tim 4/4 +
  determinisme metode seed-42); energi/komputasi ulang dataset D1 (dataset sama dgn EVAL_B
  yg lolos gate identitas 22/22); robustness terhadap pilihan grid 1 menit (EB-2).
- **Keterbatasan bukti**: fold kecil (stuck_K-i 2, tool_wear 4 alat, hyd_K-ii 1 split);
  prevalensi antar well sangat berbeda (vib 0,14–0,57; ssi 0,003–0,065) sehingga
  dispersi AUPRC antar-fold sebagian mencerminkan perbedaan prevalensi — selalu bandingkan
  ke baseline fold yang sama (ΔB).

---

Sumber: `scratch/v9_eval_c/v9_eval_c_RESULTS.json` (primer), `v9_eval_c_VERIFY.txt` (13/13).
Dihitung: 2026-10-12, skrip EVAL_C (compute + verify, sequ 4 pikiran, council 5 arketipe).
