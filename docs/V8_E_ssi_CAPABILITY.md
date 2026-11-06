# V8-E_ssi — PROFIL KEMAMPUAN 3 LAPISAN (A/B/C) KELAS `ssi`

Task: `t_b4b8f877` [Evaluator] · Board: capstone-v8-capability · Tanggal: 2026-10-11 (WIB)
Status: BUNGKUS ULANG hasil V6/V7 ke kerangka kemampuan 3-lapisan (V8-R1) —
TANPA run ulang ML. Semua angka dikutip dari dokumen primer (daftar sumber di §6);
angka yang tidak ada di dokumen ditulis **belum terukur** (bukan dikarangan).
Kerangka: `docs/V8_R1_ABC_SPEC.md` (§1 rumus, §2.2 spesifikasi ssi, §4 ambang).

> **Riset pendahuluan: `scientific-critical-thinking`** — status V6 "LULUS" dipisah
> menjadi OBSERVED (angka V6 §4.2) vs DERIVED (turunan logis: spread, kriteria CI)
> vs BELUM TERUKUR; klaim "CI95 bawah 2/5 fold" (V7) diuji ulang secara mandiri
> dari tabel V6 §4.2 dan terkonfirmasi dengan kriteria eksplisit (CI-bawah > prev).
> **Riset pendahuluan: `statistical-analysis`** — kelas sangat langka (prev 0,5–6,5%)
> → metrik primer tetap AUPRC + lift (bukan accuracy); CI95 moving-block bootstrap
> (60/20/10, 1.000, seed 42) dipertahankan; fold <30 positif = UNDERPOWERED
> (F-7, F-9) dilaporkan terpisah, tidak dihitung mayoritas.
> **Riset pendahuluan: `verification-mandatory`** — setiap angka wajib punya jejak
> baris sumber; grep mandiri di `V6_E1_ML_DESIGN.md` atas `precision|recall|FAR|T_lead`
> = **0 match** → metrik tersebut dinyatakan "belum terukur", bukan "gagal" dan bukan
> ditaksir.
> **Riset pendahuluan: `sequentialthinking`** (pikiran 1–5) — tarik angka → cek
> kontradiksi CI → susun lapisan A/B/C → tetapkan batas pemakaian → gerbang verifikasi.

---

## 0. IDENTITAS ENGINE

| Aspek | Nilai | Sumber |
|---|---|---|
| Kelas | `ssi` — stick-slip torsional | V6 §2 #4 |
| Label | `SSI(CRPM_RT) ≥ 1`, SSI = (max−min)/(2·mean), min 10 sampel (Liu 2025; R1 §2.1) | V6 §2 #4 |
| Jenis tugas | **Deteksi kondisi** (status keadaan stick-slip) — BUKAN prediksi kejadian mendatang/onset, BUKAN diagnosis akar-masalah | V8-R1 §2.0, §2.2 |
| Engine | **Hybrid**: rule definisi kanal SSI≥1 (layer dasar, sistem hari-ini) + ML (RF: `n_estimators=300, min_samples_leaf=5, class_weight=balanced_subsample, seed=42`) untuk lead-time/inidikasi dini | V6 §1; V8-R1 §2.2 |
| Baseline RELEVAN (per tugas, bukan universal) | (a) **persistence** — kalah 0/5 vs RF (angka per-fold TIDAK dicetak di V6 §4.2; hanya verdict 0/5); (b) **canary-kedalaman** — 0,0055–0,0676 (RF menang 5/5 = G2); (c) **rule ambang absolut SSI≥1** (baseline operasional rig) | V6 §4.2; V8-R1 §2.2 |
| Protokol validitas | LOWO (sumur uji tak terlihat), fitur lampau / label depan, kanal sumber-label (CRPM) dilarang jadi fitur, pra-reg E1a di-hash sebelum training | V6 §3 |

---

## 1. LAPISAN A — apakah deteksi bekerja

### 1.1 Angka terukur (OBSERVED — V6 §4.2, semua fold layak dinilai)

| Sumur uji | n / pos / prev | AUPRC RF [CI95] | lift | canary-kedalaman | ΔB canary (AUPRC_RF − canary) |
|---|---|---|---|---|---|
| F-14 | 5.455 / 75 / 0,0137 | 0,0358 [0,0096; 0,0797] | 2,61 | 0,0256 | +0,0102 |
| F-15A | 6.020 / 31 / 0,0051 | 0,0185 [0,0043; 0,0634] | 3,59 | 0,0055 | +0,0130 |
| F-15_S | 5.342 / 85 / 0,0159 | 0,1057 [0,0387; 0,2423] | 6,64 | 0,0221 | +0,0836 |
| F-5 | 4.714 / 102 / 0,0216 | 0,0810 [0,0305; 0,1874] | 3,74 | 0,0676 | +0,0134 |
| F-9_A | 841 / 55 / 0,0654 | 0,0961 [0,0297; 0,1901] | **1,47** ✗ (< 1,5) | 0,0593 | +0,0368 |

UNDERPOWERED (dilaporkan terpisah, tidak dihitung mayoritas): **F-7** (3 positif;
lift 134 — angka tak bermakna), **F-9** (12 positif) — V6 §4.2.

### 1.2 Nilai lapisan A (kerangka baru)

| Ukuran | Nilai | Status |
|---|---|---|
| AUPRC + lift | 0,0185–0,1057; lift 2,61–6,64 (5 fold layak); lift ≥1,5 di **4/5** (G1); RF ≥ canary di **5/5** (G2) | OBSERVED |
| ΔB vs persistence | RF **tidak dikalahkan** persistence di 5/5 fold (persistence menang 0/5) → ΔB ≥ 0 di 5/5. Catatan jujur: angka AUPRC persistence per-fold TIDAK dicetak di V6 §4.2 — hanya verdict 0/5 | OBSERVED (verdict) |
| ΔB vs canary-kedalaman | positif di 5/5 fold (tabel §1.1) | DERIVED dari angka V6 |
| Plafon lift | 1/prev = 15–196 per fold (prev 0,51–6,54% → 1/0,0654=15,3 … 1/0,0051=196) → lift 2,6–6,6 = fraksi kecil dari plafon; kelas langka memang lift-nya dibatasi prevalensi | DERIVED |
| Precision di ambang operasi | **belum terukur** — V6 hanya melaporkan metrik berbasis AUPRC; tidak ada ambang operasi yang dipilih/dilaporkan | belum terukur |
| Recall di ambang operasi | **belum terukur** | belum terukur |
| FAR_w / FAR_t | **belum terukur** | belum terukur |
| Waktu deteksi / lead-time | **belum terukur** (kelas ini berklaim deteksi status, bukan onset — lead-time akan relevan bila engine dipakai sebagai peringatan dini) | belum terukur |

**Nilai A (aturan V8-R1 §1.2):** A = "deteksi MENAMBAH di atas baseline relevan" —
`ΔB > 0` vs canary di 5/5 fold dan vs persistence di 5/5 fold (mayoritas syarat
terpenuhi). Kelemahan A yang jujur: kekuatan tambahan di 2 fold (F-14, F-15A) kecil
dalam satuan absolut AUPRC (prev juga sangat kecil di sana).

---

## 2. LAPISAN B — apakah deteksi memberi nilai maintenance

| Ukuran | Nilai | Status |
|---|---|---|
| B1 cakupan peringatan-dini | **belum terukur** — tidak ada klaim onset untuk `ssi`; bila nanti dipakai sbg peringatan dini, onset = transisi blok SSI berkelanjutan | belum terukur |
| B2 waktu-untuk-bertindak (T_lead) | **belum terukur**. Preseden ilmiah terdekat (bukan angka ssi): peringatan 2,67–7,37 menit sebelum stuck pada data Volve surface [R1-S1 §2.2] — relevan hanya jika klaim onset ssi dibuka | belum terukur (preseden = anchor, bukan hasil) |
| B3 pengurangan pemeriksaan tak perlu (vs rule SSI≥1) | **belum terukur** — FP engine vs FP rule absolut belum dihitung | belum terukur |
| B4 margin status-awal | **belum terukur** — median jendela antara alarm prediksi dan masuknya blok SSI berkelanjutan belum dihitung | belum terukur |

**Nilai B (jujur):** semua ukuran B **belum terukur** — ini konsekuensi langsung dari
jenis tugas engine saat ini (deteksi status, evaluasi V6 memakai AUPRC vs label status).
Yang bisa disimpulkan sekarang hanya arah: karena persistence LEMAH di kelas ini
(0/5), engine memberi informasi di atas "status tetap" → **potensi nilai maintenance
ADA dan terukur sebagian di lapisan A**, tetapi wujud operasionalnya (peringatan
berapa menit sebelum kondisi memburak, berapa banyak pemeriksaan yang dihemat)
**belum pernah diukur**. Jangan klaim "mengurangi N pemeriksaan" — angkanya belum ada.

---

## 3. LAPISAN C — cukup tepercaya untuk dipakai

| Ukuran | Nilai | Status |
|---|---|---|
| C1 stabilitas temporal | spread AUPRC antar fold layak = 0,1057 − 0,0185 = **0,0872** (rentang relatif lebar: fold terbaik 5,7× fold terlemah). CI95 lebar di 2 fold rapuh (F-14 [0,0096; 0,0797], F-15A [0,0043; 0,0634]). **CI-bawah di atas prevalensi (no-skill) hanya 2/5 fold** (F-15_S 0,0387 > 0,0159; F-5 0,0305 > 0,0216) → 3/5 fold: rentang kepercayaan menyentuh/lampaui no-skill = ketidakpastian transparan tapi nyata (klaim V7 "CI95 bawah 2/5 fold" terkonfirmasi dengan kriteria ini) | OBSERVED + DERIVED |
| C2 ketahanan lintas-regime | kasus khusus lama = canary-kedalaman: RF ≥ canary di **5/5 fold** (G2) → tidak ada fold di mana model kalah terhadap "diagnosis kedalaman". Bin regime eksplisit (kuartil kedalaman + RPM/WOB) **belum terukur** | OBSERVED (canary) / belum terukur (bin eksplisit) |
| C3 toleransi kualitas sensor | **belum terukur** — dropout kanal fitur teratas (SHAP ssi: TFLO_mean/last, SPPA_mean, BPOS_last/mean/std — fold F-15A, additivity 3,43e-09 lolos) belum diuji | belum terukur |
| C4 transparansi ketidakpastian | **TERPENUHI** — CI95 dilaporkan di SEMUA fold layak; fold UNDERPOWERED (F-7, F-9) diberi label dan dikecualikan dari mayoritas; log run tersimpan (`scratch/v6_e1/E1*_RUN_LOG.txt`) | OBSERVED |
| C-ketersediaan data lintas-peralatan (S-E1) | wellbore baru CRPM_RT **DIOLAH**: F-10 281.030 / F-4 42.010 / F-12 178.430 / F-15 57.846 baris (+CRPM petro 36.308 sbg cross-check) — fold underpowered (F-7 3 pos, F-9 12 pos) BISA diganti fold kuat. Re-run 11 fold **belum dijalankan** (S-E1 status DIOLAH, bukan hasil kampanye) | OBSERVED (data) / belum terukur (hasil re-run) |

**Nilai C:** kepercayaan = SEDANG. C4 terpenuhi penuh (ketidakpastian transparan);
C2 lolos pada kasus khusus canary; tetapi C1 menunjukkan 2 fold rapuh + hanya 2/5
fold dengan CI-bawah di atas no-skill, dan C3 belum diuji. Kerapuhan ini SEBABNYA
TERDIAGNOSIS: jumlah positif kecil (31–102 per fold; F-7/F-9 3–12) — akar yang sama
dengan `shk` (V7 §6.1), dan solusinya SUDAH ADA di pipeline (S-E1, wellbore baru).

---

## 4. BATAS PENGGUNAAN (eksplisit — bukan vonis biner)

| Mode pemakaian | Status | Dasar angka |
|---|---|---|
| **Pemantauan tren / indikasi** (tampilan drift stick-slip, bahan diskusi harian) | **LAYAK** | A: ΔB > 0 di 5/5 fold vs persistence & canary; C4 terpenuhi |
| **Peringatan dengan human-in-loop** (notifikasi "kemungkinan stick-slip — cek parameter") | **LAYAK BERSYARAT** — syaratnya: FAR diukur dulu (belum terukur) dan disetujui batas kerja-kerjaanya; 3/5 fold CI-bawah menyentuh no-skill = peringatan wajib bawa label keyakinan, bukan angka tunggal | A + C1; FAR belum terukur |
| **Alarm otomatis kritis** (memicu tindakan otomatis tanpa konfirmasi manusia) | **BELUM LAYAK** — BUKAN gagal: syarat ambang-atas (V8-R1 §4) G1 4/5 + G2 5/5 sudah terpenuhi (= label "TERBUKTI prediksi kuat" tercapai), tetapi syarat B (B4/FAR ≤ 1 per 24 jam-negatif) dan C3 BELUM DIUKUR, plus kerapuhan C1 (2 fold rapuh). Keputusan wajar = naik kelas setelah: (i) ukur P/R/FAR pada ambang operasi pra-reg, (ii) re-run S-E1 (11 fold) membuktikan stabilitas, (iii) uji dropout sensor C3 | §4 V8-R1: ambang alarm butuh A+B+C lengkap |
| Dipakai SEBAGAI SATU-SATUNYA detektor stick-slip | TIDAK — engine hybrid: layer dasar tetap rule SSI(CRPM)≥1 (baseline operasional); ML = penambah nilai di atas rule, bukan pengganti | V8-R1 §2.0 |
| Klaim prediksi kegagalan mendatang (onset/lead-time) | TIDAK boleh diklaim dari hasil saat ini — belum ada kampanye onset `ssi`; angka lead-time tidak ada | §2 B |

Ringkas satu kalimat: **`ssi` = engine dengan nilai tambah ML terukur di atas
status-quo (persistence 0/5, canary kalah 5/5) untuk PEMANTAUAN/PERINGATAN
ber-keyakinan-transparan; layak alarm otomatis baru setelah FAR + S-E1 + C3 terukur
— status hari ini "layak tren, belum alarm", bukan gagal dan bukan lulus penuh.**

---

## 5. KEKUATAN BUKTI per lapisan

| Elemen | Kekuatan | Alasan |
|---|---|---|
| Angka AUPRC/lift/canary (5 fold) | **TINGGI** | Eksekusi nyata LOWO, pra-reg di-hash sebelum training (E1a), anti-sirkular (CRPM dilarang dari fitur), CI95 bootstrap, log tersimpan |
| Verdict persistence 0/5 | **SEDANG-TINGGI** | Verdict dicatat V6, tetapi angka per-fold persistence TIDAK dicetak → tidak bisa dicek ulang per fold dari dokumen |
| G1 4/5, G2 5/5 | **TINGGI** | Turunan langsung dari tabel §1.1 |
| CI "2/5 fold di atas no-skill" | **TINGGI** | Direproduksi mandiri dari tabel V6 §4.2 (CI-bawah vs prev: hanya F-15_S & F-5 lolos) |
| Kelayakan alarm otomatis | **BELUM DINILAI** (bukan negatif) | FAR/P/R/B4/C3 belum diukur — ketidaktahuan terukur, bukan kegagalan |
| S-E1 (4 wellbore CRPM) | **TINGGI untuk keberadaan data; nol untuk hasil model** | Data DIOLAH (baris dihitung, cross-check petro); kampanye belum jalan |

---

## 6. Sumber angka (dokumen primer — semua OBSERVED kecuali ditandai)

- `docs/V6_E1_ML_DESIGN.md` §2 #4 (definisi kelas/label), §4.2 (tabel fold:
  n/pos/prev, AUPRC+CI95, lift, canary; verdict G1 4/5, G2 5/5, persistence 0/5;
  UNDERPOWERED F-7/F-9), §5 (SHAP F-15A: additivity 3,43e-09; TFLO/SPPA/BPOS),
  §1 (RF parameter).
- `docs/V7_PM_VERDICT.md` baris `ssi` (LULUS rapuh; S-E1 CRPM 281.030/42.010/
  178.430/57.846 baris; mekanisme label tidak berubah).
- `docs/V7_R1_SOLUTIONS.md` §6.1 (diagnosis kerapuhan: F-7 3 pos, F-9 12 pos,
  F-9_A lift 1,47 gagal tipis, CI95 lebar 2 fold; S-E1 parse F-10/F-4/F-12/F-15
  CRPM 186/135/90/76 file; S-E2 pra-reg stabilitas fold).
- `docs/V7_M2_SYNTHESIS.md` §1 tabel (S-E1 status DIOLAH, CRPM 281.030/42.010/
  178.430/57.846 baris + CRPM petro 36.308 cross-check).
- `docs/V8_R1_ABC_SPEC.md` §1 (rumus A/B/C), §2.0/§2.2 (jenis tugas + baseline
  relevan ssi), §4 (ambang layak-tren vs layak-alarm).

**Belum terukur (daftar eksplisit, tidak dikarangan):** precision, recall, FAR_w,
FAR_t, waktu deteksi/T_lead, B1, B2, B3, B4, C3 (dropout sensor), bin regime C2
eksplisit, hasil re-run S-E1 11 fold, angka AUPRC persistence per-fold.
