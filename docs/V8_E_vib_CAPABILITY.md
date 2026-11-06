# V8-E_vib — PROFIL KEMAMPUAN kelas `vib` (LAPISAN A/B/C)

Task: `t_dbe58beb` [Evaluator] · Board: capstone-v8-capability · Tanggal: 2026-10-11 (WIB)
Status: bungkus ulang hasil V6/V7 ke kerangka 3-lapisan (V8-R1_ABC_SPEC) — TANPA run ulang.
Semua angka = kutipan dari dokumen primer; turunan aritmetika ditandai DERIVED; yang tidak
ada di dokumen ditulis **belum terukur** (bukan nol, bukan gagal).

> **Riset pendahuluan: `scientific-critical-thinking`** — setiap nilai dipisah OBSERVED
> (angka V6 §4.1 / V7) vs DERIVED (selisih dua kolom terukur) vs BELUM TERUKUR; klaim
> "LULUS kuat" V6 dipertahankan sebagai fakta gate lama, tetapi nilai maintenance (B) dan
> robustness lintas-regime (C2/C3) dinilai dari keberadaan BUKTInya, bukan dari reputasi gate.
> **Riset pendahuluan: `statistical-analysis`** — AUPRC+lift dipertahankan (kelas prev
> 0,14–0,57 tidak seimbang); CI95 moving-block bootstrap V6 dipakai apa adanya; spread
> AUPRC antar-fold dihitung sebagai C1; <30 positif/fold = UNDERPOWERED (tidak ada fold
> vib yang kena — semua fold punya 1.124–1.543 positif).
> **Riset pendahuluan: `verification-mandatory`** — seluruh tabel angka diverifikasi dengan
> read_file langsung atas `docs/V6_E1_ML_DESIGN.md` (§2, §4.1, §5) dan
> `docs/V7_R1_SOLUTIONS.md` §1.2 + `docs/V7_PM_VERDICT.md` §0; tidak ada angka dari
> ingatan; daftar "belum terukur" eksplisit di §8.
> **Riset pendahuluan: `sequentialthinking`** (5 pikiran, 5/5 sukses) — pemisahan
> OBSERVED/DERIVED/BELUM-TERUKUR per lapisan → ambang §4 V8-R1 → batas penggunaan wajar.

---

## 0. Konteks kerangka

Kerangka V8 (instruksi operator, spesifikasi: `docs/V8_R1_ABC_SPEC.md`) menilai engine
dengan NILAI kemampuan 3 lapisan, bukan LULUS/GAGAL. Gate biner V6 (G1 lift≥1,5 mayoritas
fold; G2 AUPRC RF ≥ canary-kedalaman mayoritas) TIDAK digeser — dipakai sebagai syarat
ambang-atas "TERBUKTI-KUAT" (klasifikasi alarm otomatis §4 V8-R1). Dokumen ini: profil
kemampuan kelas `vib` yang di V6 berstatus **LULUS (G1 4/4, G2 4/4)**.

## 1. Jenis tugas · engine · baseline relevan

| Aspek | Penetapan (ikut V8-R1 §2.1) |
|---|---|
| Jenis tugas | **Deteksi kondisi** — status keadaan GET/whirl lateral tinggi (`VIBLAT_RT ≥32,17405 ft/s²`, ambang absolut R1 §4.2). **BUKAN** prediksi kegagalan mendatang → ukuran T_lead (Tabel 1.2 V8-R1) tidak berlaku; B4 margin status-awal yang relevan. |
| Engine | **Hybrid**: (1) rule ambang absolut R1 §4.2 = layer dasar & sistem hari-ini; (2) persistence = pembanding status-quo; (3) Random Forest (V6 E1a) = penambah nilai untuk peringatan dini/lead-time; LogisticRegression sekunder (terukur, dicatat). |
| Baseline relevan | (a) **Rule ambang absolut** (baseline operasional rig; FP rule tidak dicetak di dokumen → belum terukur); (b) **persistence** AUPRC 0,517–0,796 (mengalahkan RF di 2/4 fold); (c) **canary-kedalaman** 0,277–0,612. |
| Sumber label | Kanal instrumen downhole `VIBLAT_RT` (WITSML Volve). Kanal duplikat `WHIRL_RT` DILARANG dipakai (D0 §2.5) — anti-sirkular terjaga. |

## 2. Angka terukur (OBSERVED — kutipan V6_E1_ML_DESIGN.md §4.1; populasi §2)

| Sumur uji | n / pos / prev | AUPRC RF [CI95] | lift | canary-kedalaman | logreg | persistence | ΔB vs persistence (DERIVED) |
|---|---|---|---|---|---|---|---|
| F-14 | 1.989 / 1.124 / 0,565 | **0,912** [0,821; 0,961] | 1,61 | 0,612 | 0,875 | 0,796 | **+0,116** |
| F-15A | 6.482 / 1.543 / 0,238 | **0,562** [0,397; 0,683] | 2,36 | 0,458 | 0,647 | 0,547 | **+0,015** |
| F-15_S | 10.903 / 1.532 / 0,141 | **0,491** [0,338; 0,619] | 3,50 | 0,277 | 0,184 | 0,517 | **−0,026** |
| F-5 | 4.548 / 1.230 / 0,270 | **0,441** [0,341; 0,553] | 1,63 | 0,309 | 0,661 | 0,667 | **−0,226** |

Konteks tambahan (OBSERVED):
- Gate V6: **G1 4/4** (lift 1,61–3,50, semua ≥1,5) · **G2 4/4** (RF ≥ canary tiap fold) →
  label V6: **LULUS**. Persistence mengalahkan RF di **2/4 fold** (tidak mayoritas → tidak
  menurunkan verdict V6; dicatat sebagai batasan).
- SHAP (V6 §5, fold F-15_S, additivity 1,19e-08 ✓): 6 fitur teratas =
  TFLO_mean, TFLO_last, depth_mean, dbtm_last, dbtm_mean, HKLD_mean — model memakai
  sinyal aliran/beban, bukan hanya posisi kedalaman (konsisten G2 lolos 4/4).
- Wellbore baru siap memperkuat (OBSERVED, V7_R1 §1.2 + V7_PM §0, recount 3 pihak
  COCOK): `VIBLAT_RT` **F-4 86 file · F-10 66 file · F-15 76 file** — BELUM diparse;
  status parse ≠ angka hasil (belum ada metrik dari wellbore baru).
- F-9: 1.270 label vib teramati tapi 0 jendela fitur pengeboran (V6 §6.6) → 1 sumur
  hilang karena keadaan data. F-7 tanpa kolom VIBLAT (V7_M2 §1) → fold F-7 mustahil.

## 3. LAPISAN A — apakah deteksi bekerja?

| Ukuran | Nilai | Status bukti |
|---|---|---|
| AUPRC RF | 0,441–0,912 (4 fold layak) | OBSERVED |
| lift (vs prevalensi fold) | 1,61 / 2,36 / 3,50 / 1,63 — **4/4 > 1,5** | OBSERVED |
| ΔB vs persistence (metrik primer A kerangka baru) | +0,116 / +0,015 / −0,026 / −0,226 → **ΔB > 0 di 2/4 fold (= 50%)** | DERIVED |
| ΔB vs canary-kedalaman | RF ≥ canary di **4/4 fold** (margin +0,300 / +0,104 / +0,214 / +0,132) | DERIVED dari OBSERVED |
| Precision pada ambang operasi | **belum terukur** (V6 hanya mencetak AUPRC/lift; tidak ada ambang operasi RF yang dipra-registrasikan) | — |
| Recall | **belum terukur** | — |
| FAR_w / FAR_t | **belum terukur** (FP jendela & jam operasi negatif tidak dicetak) | — |
| Waktu deteksi / T_lead | tidak berlaku (tugas deteksi kondisi, bukan onset); B4 margin **belum terukur** | — |

**Nilai A (aturan V8-R1 §1.2: A-bekerja bila ΔB > 0 pada ≥50% fold layak):**
- **vs canary-kedalaman: A KUAT** (4/4, margin lebar) — model tidak sekadar "mengingat
  posisi"; konsisten SHAP dominasi TFLO/HKLD.
- **vs prevalence-random: A KUAT** (lift 4/4 ≥1,5 → memenuhi syarat ambang-atas G1).
- **vs persistence: A SEBAGIAN** (2/4 fold, persis di ambang 50%) — di F-14 & F-15A RF
  menambah; di F-15_S & F-5 status-sebelumnya sudah membawa hampir semua sinyal.
  Ini hasil A yang jujur, bukan kegagalan: persistence di kelas ini kuat karena label
  membentuk blok temporal panjang (batasan V6 §4.1).
- Ringkas A: **deteksi TERBUKTI bekerja di 4/4 fold terhadap 2 dari 3 baseline relevan;
  vs baseline terberat (persistence) menang telak di separuh fold.**

## 4. LAPISAN B — apakah deteksi memberi nilai maintenance?

| Ukuran | Nilai | Status bukti |
|---|---|---|
| B3 pengurangan pemeriksaan tak perlu (`1 − FP_engine/FP_rule`) | **belum terukur** (FP rule ambang absolut tidak dicetak di dokumen mana pun) | — |
| B4 margin status-awal (median jendela alarm→blok GET berkelanjutan) | **belum terukur** | — |
| Nilai kualitatif dari angka yang ada | Persistence 0,517–0,796 → status GET tinggi membentuk blok: **rule absolut + status-quo sudah memberi cakupan deteksi-status yang baik**; nilai tambah RF = **potensi peringatan-dini sebelum blok** (aspirasi desain, belum diukur sebagai T_lead/B4) | DERIVED + HIPOTESIS |
| Anchor preseden | 2,67–7,37 menit peringatan stuck [R1-S1 §2.2] = **anchor kelas stuck, TIDAK dipinjam ke vib** (V8-R1 §1.3: anchor per kelas) | — |

**Nilai B: BELUM TERUKUR secara kuantitatif — ini celah bukti terbesar kelas ini.**
Bukan B-negatif: tidak ada angka yang menunjukkan vib tidak memberi nilai maintenance;
yang ada adalah V6 tidak mencetak metrik B (V6 menilai lewat gate A-up, desain pra-reg
E1a memang hanya G1/G2). Konsekuensi operasional: klaim "vib memberi peringatan dini X
menit sebelum whirl" **belum boleh dijual** sampai B3/B4 diukur.

## 5. LAPISAN C — cukup tepercaya untuk dipakai?

| Ukuran | Nilai | Status bukti |
|---|---|---|
| C1 stabilitas temporal | spread AUPRC antar fold = 0,912 − 0,441 = **0,471 (LEBAR)**; spread lift = 3,50 − 1,61 = 1,89 (semua fold tetap >1,5). CI95: F-14 ketat [0,821;0,961]; F-15_S & F-5 lebar ([0,338;0,619], [0,341;0,553]) | DERIVED dari OBSERVED |
| C2 ketahanan lintas-regime | **parsial**: canary-kedalaman (kasus khusus C2 lama) RF menang 4/4 → tidak ada fold yang runtuh terhadap kedalaman. Uji bin regime RPM/WOB & ΔAUPRC per bin: **belum terukur** | OBSERVED parsial |
| C3 toleransi kualitas sensor (dropout kanal/noise) | **belum terukur** | — |
| C4 transparansi ketidakpastian | **TERPENUHI**: CI95 dicetak untuk SEMUA fold (moving-block bootstrap 60/20/10, 1.000 resample, seed 42); tidak ada fold UNDERPOWERED (pos 1.124–1.543 >> 30; prev 0,141–0,565) | OBSERVED |
| C-lintas-peralatan | 4 wellbore berbeda (F-14, F-15A, F-15_S, F-5) semuanya fold layak → ketahanan antar-wellbore Volve TERUKUR untuk 4 wellbore; F-4/F-10/F-15 = kesempatan replikasi, belum dieksekusi | OBSERVED |

**Nilai C: SEDANG — C4 kuat, C2 parsial-positif, C1 lebar (harus dianotasi), C3 nol-bukti.**
C4 lolos → engine tidak terblokir ke tingkat tren (aturan V8-R1 §1.4: satu kegagalan C4 =
tren maks; di sini C4 lolos).

## 6. BATAS PENGGUNAAN (eksplisit — bukan vonis biner)

| Tingkat | Status | Dasar |
|---|---|---|
| **Pemantauan tren / indikasi** | **LAYAK** | Syarat "LAYAK TREN" V8-R1 §4: (A) ΔB>0 di ≥50% fold — terpenuhi (2/4 vs persistence, 4/4 vs canary); (B) arah benar — B4/B3 belum terukur, tetapi deteksi-status oleh rule absolut + RF terbukti 4/4 fold vs prevalence & canary; (C) C4 wajib — terpenuhi; FAR ≤6/24 jam — belum diukur → batas pemakaian="anotasi beban kerja wajib" mengikuti §4. |
| **Peringatan (advisory, non-otomatis)** | **LAYAK BERSYARAT** — 2 syarat: (1) FAR_t diukur di kampanye penguatan; (2) B4 margin diukur. Syarat ambang-atas A sudah ada (G1 4/4 + G2 4/4 = label TERBUKTI-KUAT), yang belum ada = bukti B & FAR. |
| **Alarm kritis otomatis** | **BELUM — menunggu bukti B & C, bukan menunggu A.** Syarat §4 V8-R1: B1≥80% + T_lead ≥ anchor (kelas onset — untuk vib analognya B4 margin + FAR ≤1/24 jam-negatif) + C2 eksplisit per bin regime (ΔAUPRC drop <20%) + C3 dropout <20%. Keempatnya **belum terukur**. Ini keputusan tingkat keyakinan yang wajar, BUKAN kegagalan engine. |
| Jangan dipakai untuk | klaim prediksi kegagalan/keausan mendatang (tugasnya deteksi kondisi); klaim lead-time berapa menit (belum terukur); generalisasi ke wellbore non-Volve tanpa data baru. |

Catatan hybrid: rule ambang absolut (32,17405 ft/s²) + persistence adalah **engine itu
sendiri** dalam kerangka baru — "status-quo sudah bagus untuk konfirmasi status" adalah
kemampuan yang tercatat, dan RF diposisikan sebagai lapisan peringatan-dini di atasnya,
bukan pengganti.

## 7. KEKUATAN BUKTI (per lapisan)

| Lapisan | Kekuatan | Alasan |
|---|---|---|
| A | **KUAT** | Pra-registrasi E1a di-hash sebelum training; LOWO (anti-leak/pseudoreplication); fitur lampau/label depan; kanal sumber-label dilarang jadi fitur; 4/4 fold layak dinilai (bukan underpowered); metrik primer AUPRC+lift + CI95 bootstrap; log run tersimpan (`scratch/v6_e1/E1*_RUN_LOG.txt`). |
| B | **NOL-BUKTI (belum diukur)** | B3/B4/FAR tidak pernah dicetak; desain pra-reg E1a tidak memuat metrik B. Celah ini struktural (gate V6 = A-up saja), bukan kelemahan engine. |
| C | **SEDANG** | C4 penuh; C2 hanya parsial (canary); C1 lebar tapi transparan; C3 belum; replikasi wellbore baru (F-4/F-10/F-15) tersedia tapi belum dijalankan. |

## 8. BELUM TERUKUR (daftar eksplisit — jangan dianggap nol/gagal)

1. Precision, recall, ambang operasi RF → belum pernah dipra-registrasikan/dicetak.
2. FAR_w, FAR_t (FP per 1.000 jendela negatif / per jam operasi negatif).
3. B3 kurangi-ragu vs rule ambang absolut (butuh FP rule).
4. B4 margin status-awal (alarm→blok GET berkelanjutan).
5. C2 eksplisit per bin regime RPM/WOB + ΔAUPRC per bin kedalaman (canary = proxy parsial).
6. C3 dropout kanal SHAP teratas (TFLO) + noise σ/10.
7. Metrik apa pun dari wellbore baru F-4/F-10/F-15 (file VIBLAT terverifikasi ada, parse BELUM).

## 9. Ringkas 1-layar

`vib` = kelas dengan **bukti lapisan A terkuat di portofolio V6** (G1 4/4 + G2 4/4, satu-
satunya kelas yang lift & canary-nya menang di SEMUA fold) dan **bukti lapisan B paling
kosong** (tidak pernah diukur). Batas penggunaan wajar hari ini: **layak pemantauan tren
+ peringatan advisory dengan anotasi beban kerja; BELUM alarm otomatis kritis** — bukan
karena sinyalnya meragukan, melainkan karena FAR & margin peringatan belum pernah diukur.
Jalur naik tingkat: kampanye penguatan (parse F-4/F-10/F-15, pra-reg baru) yang MENCETAK
FAR_t + B4 + C2 per-regime. Persistence 2/4 menang = batasan nyata: di sumur dengan blok
label panjang, RF tidak menambah di atas status-quo — dekomposisi ini harus dipertahankan
di laporan mana pun, jangan dirata-rata.

## Sources (dokumen primer — semua angka di §2 terverifikasi via read_file langsung)

- `docs/V6_E1_ML_DESIGN.md` §2 (populasi sampel vib: F-14 1.989/1.124; F-15A 6.482/1.543;
  F-15_S 10.903/1.532; F-5 4.548/1.230), §4.1 (tabel AUPRC/CI95/lift/canary/logreg/persistence
  + verdict G1 4/4 G2 4/4 + persistence 2/4), §5 (SHAP vib fold F-15_S), §6 (kelemahan:
  persistence 2/4, F-9 0 jendela fitur).
- `docs/V7_R1_SOLUTIONS.md` §1.2 (tabel wellbore baru: VIBLAT_RT F-10 66 / F-4 86 /
  F-15 76 file, status BELUM diparse) + §0 (vib = memperkuat fold LULUS, anti-rapuh).
- `docs/V7_PM_VERDICT.md` §0 baris `vib` (recount 3 pihak: R1 scan → D1e COCOK PERSIS →
  A1 D6 EKSAK) + §5.2 (2 kalimat pembatas).
- `docs/V8_R1_ABC_SPEC.md` §1.1–1.4 (rumus A/B/C), §2.1 (spesifikasi vib), §4 (ambang
  tren vs alarm otomatis).
- `docs/V7_M2_SYNTHESIS.md` §1 (F-7 tanpa kolom VIBLAT → fold mustahil dari CSV itu).

## Belum diverifikasi (verification-mandatory #3)

- Eksistensi file run-log `scratch/v6_e1/E1*_RUN_LOG.txt` dikutip dari V6 §4/§7 (klaim
  dokumen V6); tidak dibuka ulang di sesi ini (angka V6 dipercaya sebagai dokumen primer
  yang sudah melalui audit V5_A1/V7).
- Jumlah baris VIBLAT_RT wellbore baru = jumlah FILE, bukan baris/jendela positif —
  prevalensi wellbore baru belum diketahui (belum diparse).
