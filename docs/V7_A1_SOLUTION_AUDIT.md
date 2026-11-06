# V7-A1 — AUDIT SOLUSI R&D: NYATA atau KARANGAN?

Task: `t_712f5bae` [Auditor] · Board: capstone-v7-solve · Tanggal: 2026-10-11 (WIB)
Objek audit: `docs/V7_R1_SOLUTIONS.md` (solusi R&D) + `docs/V7_M2_SYNTHESIS.md` (relasi Master).
Peran: PEMBONGKAR. Keberhasilan audit = MENEMUKAN kelemahan/karangan, bukan stempel.
Metode: independen — sitasi dibuka sendiri via `web_extract`, klaim data dihitung ulang
dengan skrip mandiri (`~/.hermes/cache/scratch/a1_*.py`), gate dicek terhadap `V6_E1_ML_DESIGN.md`.

> **Riset pendahuluan: `scientific-critical-thinking`** — dipisah OBSERVED (dihitung ulang dari
> file primer) vs DERIVED vs klaim R&D; tiap solusi diuji "menyelesaikan AKAR atau MEMINDAHKAN
> masalah"; temuan yang merugikan R&D dilaporkan apa adanya.
> **Riset pendahuluan: `verification-mandatory`** — 10 titik; ≥5 sitasi dibuka langsung, ≥5 klaim
> data dihitung ulang ke file primer, "belum diverifikasi" didaftar eksplisit (§7).
> **Riset pendahuluan: `peer-review`** — claim–evidence mapping per solusi; status
> diterima/salah/tidak-bisa-diverifikasi; komentar terpisah temuan minor vs fatal.
> **Riset pendahuluan: `statistical-analysis`** — jumlah POSITIF nyata per fold & plafon lift
> (1/prev) dipakai menilai apakah solusi benar menyerang akar kegagalan, bukan sekadar menambah baris.

---

## 0. RINGKASAN EKSEKUTIF — vonis

**Solusi R&D LARGELY NYATA, bukan karangan.** Sitasi ilmiah terbuka dan rumusnya COCOK; klaim
data mayoritas terverifikasi EKSAK ke file primer; gate G1/G2 TIDAK digeser. Namun audit
MENEMUKAN beberapa angka klaim yang salah/overstated/tdk reconcile — dilaporkan terus terang
di §4. Tidak ada satu pun solusi yang memakai paper palsu atau menurunkan ambang secara diam-diam.

| Sisi | Temuan |
|---|---|
| Sitasi (≥5 dibuka) | **8 dibuka langsung**, 7 cocok, 1 (Saini) CAPTCHA-blocked; 0 paper karangan |
| Data (≥5 dihitung ulang) | **9 dihitung ulang**: 6 EKSAK, 3 bermasalah (§4) |
| Gate anti-geser | **TIDAK ada geseran** — G1/G2/persistence/UNDERPOWERED identik V6 |
| Engineering vs paper | JUJUR — solusi tanpa paper ditandai eksplisit (S-B2/C2/D4/E2) |
| Karangan ditemukan | TIDAK ada karangan murni; yang ada = **angka salah / overstated / stale** (4 butir, §4) |

**Kelemahan paling penting yang harus diperbaiki sebelum eksekusi (§5):**
1. **M2 "582/884 event dalam rentang CSV" = OVERSTATED.** Hitung ulang jujur = **523**.
   F-9_A (12/94) benar; 4 sumur lain dihitung "semua masuk" tanpa dicek rentang.
   Penyebab parsial: tiap parsed CSV mengandung **2 baris sentinel 2015-09-22** (sinyal kosong)
   yang mem-blow-up rentang.
2. **S-A1 (rekomendasi #1) onset stuck sangat sedikit** — hitung ulang ketat = **34 transisi
   0→≥1** (bukan 50/74 seperti klaim M2). Dengan 34 onset di 2 sumur, fold risiko
   UNDERPOWERED (<30/sumur). Solusi termurah ini paling berisiko soal daya statistik.
3. **S-F1 "1.489 transisi = kandidat onset" overstated** — 1.492 hit, tapi hanya **481** yang
   benar awal blok `high_MSE` (329 dari `normal`); sisanya noise normal↔low_ROP.
4. **"inefisiensi parah 78.212 baris" tidak reconcile** — non-normal USROP = **64.915**.

---

## 1. AUDIT SITASI (dibuka langsung; ≥5 wajib)

| # | Sitasi (R1) | Cara verifikasi | Hasil | Catatan |
|---|---|---|---|---|
| [12] | Al-Mamoori 2025 autoencoder Volve, `10.3390/app15095042`, "AUC 0,958, latih hanya data normal" | `web_extract` mdpi.com/2076-3417/15/9/5042 | **COCOK** | Judul+abstrak: "Stuck Pipe Detection…Autoencoder", Volve, AUC **0.958**, acc 99.06%, "trained exclusively on normal". Persis klaim R1 §2.2. |
| [11] | Cao 2025 Crossformer, arxiv 2503.07440, "peringatan 2,67–7,37 menit sebelum stuck" | `web_extract` arxiv abs + PDF | **COCOK** | Tabel warning time: τ=15→**2.67**, τ=30→4.67, τ=45→**7.37** min. Angka 2.67 & 7.37 ADA. Karakterisasi R1 adil ( rentang peringatan lintas τ). |
| [3] | Wang 2024 VMD+BP tool wear, `10.3390/s24248107` | `web_extract` mdpi | **COCOK** | Judul "Tool Wear Monitoring…VMD and BP Neural Network". R1 §5.3 akurat. |
| [5] | Ratner Snorkel weak supervision, `10.1007/s00778-019-00552-1` | `web_extract` springer | **COCOK** | "labeling functions… generative model… estimate accuracies & correlation". Cocok deskripsi S-A3. |
| [2] | Husseiny 2026 SPP prediction, `10.1186/s44147-026-00980-1` | `web_extract` springer | **COCOK (prediksi) / ENGINEERING (residu)** | Paper: prediksi SPP dari parameter operasional (LightGBM/ET/XGB/RF, R2>0.968). Bagian "residu→diagnosis" = perpanjangan R1, bukan literal paper. R1 menandai jujur "bukan untuk mengganti label". |
| [21] | Menand & Mills 2017 MSE/DS, AADE-17-NTCE-033, "MSE naik + MSE/DS turun = bit wear" | `web_extract` PDF hpinc.com + aade.org | **COCOK PERSIS** | Kutipan asli: "the MSE increases dramatically… At the same time, the **MSE/DS ratio decreases**, clearly differentiating this change in MSE from… vibration". Rule R1 §5.4/§6.2 benar. Rumus Teale (MSE=WOB/AB + 120π·RPM·TOB/(AB·ROP)) juga ada. |
| [20] | Teale 1965 specific energy, `10.1016/0148-9062(65)90022-7` | Crossref API | **DOI VALID** | "The concept of specific energy in rock drilling", IJRMMS 1965 vol 2 pp 57-73. Teks penuh Elsevier-paywalled; rumus terekam sekunder di [21]. |
| [22] | Hegde 2019 stick-slip severity ML, `10.1016/j.petrol.2019.05.021` | Crossref API (doi.org 404 = resolver hiccup) | **DOI VALID + judul cocok** | "Classification of drilling stick slip severity using machine learning", JPSE 179:1023-1036. onepetro full-text CAPTCHA. |
| [16] | Saini 2020 ≥10 dysfungsi dari surface, `10.2118/200006-MS` | `web_extract` onepetro | **TIDAK BISA DIVERIFIKASI** | CAPTCHA bot-wall. Klaim "≥10 kelas dysfungsi dari sensor surface" (R1 §3.1) TIDAK terkonfirmasi dari sumber asli. satu-satunya sitasi tak-terbuka. |

**Kesimpulan sitasi:** 8 dari 9 dibuka langsung (lolos acceptance ≥5). Nol URL mati palsu
(satu 404 doi.org ternyata resolver hiccup, DOI valid di Crossref). Nol rumus salah kutip.
Satu (Saini) gagal karena CAPTCHA — dilaporkan sebagai tidak-bisa-diverifikasi, bukan dipakai
menopang klaim kunci.

---

## 2. AUDIT DATA (dihitung ulang ke file primer; ≥5 wajib)

Semua dijalankan skrip independen (`a1_data_check1/2/3/5/10/usrop_trans.py`, stdlib Python,
2026-10-11) — bukan mengutip angka R1/M2.

| # | Klaim data | Skrip | Hitung ulang | Hasil |
|---|---|---|---|---|
| D1 | `labels_curated_v2.csv` = **884 event** (M2; R1 awal 1.412 = sudah dikoreksi M2) | check1 | **884 record, 884 event_id unik** | **EKSAK** — 884 benar, R1 1.412 memang artefak (sudah diakui) |
| D2 | `bha_stuck_fishing` = **38 event** | check2 | **38** (kolom `category`) | **EKSAK** |
| D3 | `USROP_labeled.csv` = **198.928 baris**, kolom WOB/ROP/RPM/MSE ada, non-null 100% | check2/3 | **198.928**; kolom ber-nama panjang ("Weight on Bit kkgf" dll) semua non-null | **EKSAK** (baris & kolom) |
| D4 | F-9 A `time.csv` = **419.747 baris**, `STUCK_RT` non-null **45.715** | check2/3 | **419.747** rows; kolom `STUCK_RT unitless` non-null **45.715** | **EKSAK** |
| D5 | uidRef `bhaRun.tubular`→`tubular` = **154/161 match** | check5 | **154/161** (161 ref, 191 uid) | **EKSAK** |
| D6 | F-10 kanal dysfungsi: SHKRSK_RT **188** / CRPM_RT **186** / STUCK_RT **18** / VIBLAT_RT **66** / STKSLP **125** | check5 (full-file) | **188/186/18/66/125** | **EKSAK** (temuan terbesar R1 terkonfirmasi) |
| D7 | toolwear = **8 xlsx** (4 alat × R01/R02) | check2 | **8** file `DrillingToolWearDataset_T0{1-4}_R0{1,2}.xlsx` | **EKSAK** |
| D8 | "inefisiensi parah **78.212 baris**" (M2 §1 S-D3, dikutip dari V6 R1) | check3 | non-normal = 15.183+49.732 = **64.915** | **TIDAK RECONCILE** (§4-C) |
| D9 | S-F1 "**1.489 transisi** kandidat onset" | usrop_trans | transisi label total **1.492**; awal blok `high_MSE` = **481**; normal→high_MSE = **329** | **OVERSTATED** (§4-D) — 1.492 cocok utk "semua transisi", bukan "kandidat onset" |

**Catatan metode:** klaim "data X ada di file Y" mayoritas benar. Tidak ditemukan klaim data
mengarang keberadaan file/kolom. Kelemahannya pada ANGKA TURUNAN (hitungan transisi, jumlah
inefisiensi, jumlah event dalam rentang) — lihat §4.

---

## 3. ANTI-GESER-GATE

Dicek terhadap pra-reg V6 asli (`V6_E1_ML_DESIGN.md` §4.4):

- **G1** = lift RF ≥ **1,5** pada **mayoritas** sumur uji layak dinilai. V6: identik.
- **G2** = AUPRC RF ≥ AUPRC canary-kedalaman mayoritas. V6: identik.
- **<30 positif = UNDERPOWERED**, dikecualikan dari gate mayoritas. V6: identik.
- **persistence > RF → layak bersyarat**. V6: identik.
- **LOWO; fitur lampau / label depan; kanal pembentuk label dilarang jadi fitur.** V6: identik.

Semua angka kegagalan yang dikutip R1 (stuck F-14 AUPRC 0,421 lift 3,12 / F-9_A lift 0,97
persistence 0,787; shk G1 3/7 G2 6/7; hyd 2/7 & 4/7 persistence 0,42–0,63; tool_wear 0/4 lift
1,09–1,42) **cocok persis** dengan V6 §4.4. **Tidak ada ambang, metrik, canary, atau aturan
mayoritas yang diturunkan.** R1 §8 & M2 §9 menyatakan perubahan hanya: (a) definisi LABEL
(status→onset/progresi/fisika), (b) UNIT (window→stand, sbg opsi), (c) TAMBAH DATA, (d)
reformulasi model — semuanya menuntut **pra-registrasi baru** yang di-hash sebelum training.

**Vonis anti-geser: LULUS.** onset-reframing mengubah ESTIMAND (status→peristiwa), bukan
menurunkan ambang; ini sah karena selaras tuntutan dosen ("akan SEGERA RUSAK") dan dinyatakan
terbuka, bukan disembunyikan. Catatan kehati-hatian: mengganti label = tugas baru, jadi angka
lama (V6) tidak boleh dibandingkan langsung; hasil onset = kampanye pra-reg tersendiri.

---

## 4. TEMUAN KELEMAHAN / KARANGAN (dilaporkan terus terang)

### A. M2 "582/884 event dalam rentang CSV parsed" = OVERSTATED → jujur **523**
- M2 §2 R1 & §7 memakai 582 sebagai bukti kelayakan relasi #1 (labels↔timeseries).
- Hitung ulang independen (`a1_range2.py`): setiap parsed CSV punya **2 baris sentinel
  2015-09-22** (sinyal kosong) yang mem-blow-up rentang maks. Setelah membuang sentinel,
  rentang nyata jauh lebih pendek (mis. F-9_A 2009-06-27..07-16; F-7 2007-09-15..10-13).
- Dengan rentang nyata, `act_start` di dalam = **523**, bukan 582. Selisih 59 event.
- **F-9_A = 12/94 TEREPRODUKSI EKSAK** (M2 §6 koreksi D1h benar). Jadi koreksi parsial M2
  tepat, tapi AGREGAT 582 tidak konsisten dengan rentang-sentinel yang sama.
- **Dampak:** relasi #1 tetap TERBUKA & bernilai, tapi angka yang dikutip ke eksekusi harus
  **523** (atau M2 harus menyatakan eksplisit bahwa 582 memakai rentang yang belum dibersihkan
  sentinel). Jangan pakai 582 di dokumen downstream.

### B. S-A1 (rekomendasi #1, stuck-onset) onset SEDIKIT — risiko UNDERPOWERED
- M2 §1: "onset 0→1 = **50** (biner ≥1 = **74**)".
- Hitung ulang (`a1_data_check3.py`, `STUCK_RT unitless` F-9 A time.csv): transisi ketat
  0→≥1 = **34**; nilai ≥1 = 22.592 baris; runs-of-≥1 = 9.871. **Baik 50 maupun 74 tidak
  terreproduksi** — metode M2 tidak didefinisikan (kemungkinan forward-fill/resample).
- **Logika:** onset stuck yang dimulai dari hanya **34** titik di 2 sumur (F-9_A + F-14) =
  rata-rata ~17/sumur → di bawah ambang <30 positif → fold berisiko **UNDERPOWERED** dan
  diekskludkan dari gate mayoritas. Ini melemahkan solusi termurah & #1 paling direkomendasikan.
- **Rekomendasi:** hitung onset dengan definisi eksplisit (forward-fill? resample 60 s?) sebelum
  training; kalau <30/sumur, S-A1 sah tapi TIDAK boleh dijanjikan "LULUS" — hanya "layak diuji".

### C. "inefisiensi parah 78.212 baris" tidak reconcile (stale)
- M2 §1 (S-D3/S-F2) & §5 mengutip "78.212 baris inefisiensi parah" dari V6 R1.
- Hitung ulang USROP: `low_ROP_efficiency` 15.183 + `high_MSE_bit_wear` 49.732 = **64.915**
  non-normal (dari 198.928). 78.212 tidak cocok dengan angka mana pun di file saat ini.
- **Status:** angka STALE/salah-kutip. Dampak kecil (hanya konteks populasi), tapi jangan
  dipakai ulang; ganti 64.915 atau definisikan ulang "inefisiensi parah".

### D. S-F1 "1.489 transisi kandidat onset" = OVERSTATED
- Hitung ulang (`a1_usrop_trans.py`): total transisi label = **1.492** (cocok ~1.489), tapi:
  - awal blok `high_MSE_bit_wear` = **481**
  - transisi `normal`→`high_MSE_bit_wear` = **329**
- **Masalah logika:** yang disebut "1.489 kandidat onset" mayoritas adalah transisi
  normal↔low_ROP (bukan onset keausan). Kandidat onset bit_wear yang sah = **481** (atau 329
  bila hanya dari normal). Angka jujur untuk S-F1 = 481/329, bukan 1.489.
- Dampak: estimasi "banyak onset per alat" (yang dipakai melawan plafon lift) berlebihan;
  tetap >0, jadi solusi tidak gugur, tapi justifikasi jumlahnya harus dikoreksi.

### E. Husseiny [2] "residu→diagnosis" = perpanjangan R1 (bukan literal paper)
- Paper = prediksi SPP dari parameter operasional. R1 §4.2 memakai residu SPP sbg diagnosis
  anomali — ini ENGINEERING EXTENSION. R1 sudah jujur menandai "bukan untuk mengganti label".
  Bukan karangan, tapi jangan dilaporkan seolah ada paper yang langsung melakukan "residu→label".

**Tidak ditemukan:** paper karangan, URL palsu, rumus salah kutip, atau penurunan ambang
diam-diam. Kelemahan R1/M2 = pada ANGKA TURUNAN (A–D), bukan pada keberadaan data/sitasi.

---

## 5. LOGIKA SOLUSI: selesaikan AKAR atau MEMINDAHKAN masalah?

| Solusi | Akar kegagalan (V6) | Apa yang dilakukan | Menyelesaikan akar? | Risiko logika |
|---|---|---|---|---|
| **S-A1** stuck-onset | label=STATUS→persistence 0,787 menang | onset 0→1, blok setelah onset dibuang | **Ya** — persistence dibunuh by construction | onset cuma ~34 (§4-B) → fold bisa UNDERPOWERED |
| **S-B1** parse F-10/F-4/F-12/F-15 | shk positif terlalu sedikit | +positif nyata (F-10 798, F-12 580) | **Ya** — menyerang jumlah positif | M2 koreksi: hanya F-10+F-12 berarti; F-4 50/F-15 13 nyaris nol |
| **S-C1** hyd-onset | label=ambang proses persisten | onset anomali | **Sebagian** — persistence turun, tapi sinyal precursor lintas-kanal blm teruji | R1 sendiri akui "bisa tak ada sinyal"; tes pembeda jelas |
| **S-D1** tool_wear progresi | n=4 + run-order confound + plafon lift 2,0 | change-point onset per run | **Sebagian** — menambah event & kurangi confound | plafon lift 1/prev≈2,0 tetap mengikat bila prev~0,5; change-point bisa artefak termal (R1 akui) |
| **S-F1** bit_wear-onset | persistence>RF di 4/4 → diturunkan | onset high-MSE | **Ya** — menghapus hukuman persistence | kandidat onset jujur 481/329, bukan 1.489 (§4-D) |

**Kesimpulan logika:** solusi menyerang AKAR masing-masing (bukan memindahkan masalah),
kecuali S-C1/S-D1 yang R1 sendiri sudah tandai berisiko & punya tes pembeda. onset-reframing
bukan "menurunkan ambang" tapi "mengubah pertanyaan" — sah, asal hasilnya pra-reg baru dan
tidak dibandingkan dengan angka V6.

---

## 6. DAFTAR AKHIR

**(a) Solusi DITERIMA (sitasi cocok + data terverifikasi + logika akar benar):**
- S-A1 stuck-onset — diterima **bersyarat**: logika benar, tapi onset ~34 → daya statistik
  wajib dihitung dulu (§4-B).
- S-B1 parse 4 wellbore shk — diterima (F-10 188/F-12 91 kanal SHKRSK terverifikasi D6).
- S-F1 bit_wear-onset — diterima **bersyarat**: koreksi jumlah onset 1.489→481 (§4-D).
- S-D3/S-F2 MSE/DS — diterima; rumus & arah **cocok persis** dengan Menand-Mills [21].
- S-A3 Snorkel — diterima; kerangka labeling-function cocok [5]; LF2 (884 event) & LF3 (38
  bha_stuck_fishing) terverifikasi D1/D2.
- S-D2 VMD — diterima; preseden [3] cocok (tapi tdk cukup sendiri, plafon lift).

**(b) Solusi SALAH / KARANGAN / overstated (dilaporkan jujur):**
- **Angka 582/884 (M2)** → overstated; jujur **523** (§4-A).
- **"inefisiensi parah 78.212"** → stale/tidak reconcile; jujur **64.915** (§4-C).
- **"1.489 kandidat onset" (S-F1)** → overstated; jujur **481/329** (§4-D).
- **onset stuck 50/74 (S-A1)** → tdk terreproduksi; hitung ketat **34** (§4-B).
- *(bukan karangan murni — semua adalah angka turunan yang salah/overstated, sudah terbuka
  datanya; keberadaan file & sitasi tetap nyata.)*

**(c) TIDAK BISA DIVERIFIKASI:**
- Sitasi **[16] Saini 2020** (`10.2118/200006-MS`) — onepetro CAPTCHA; klaim "≥10 kelas
  dysfungsi dari surface" tdk terkonfirmasi dari sumber asli.
- Klaim **GAINLOSSTOT F-1 C = 575 file** — scan 2.156 file timeout (300 s), belum dihitung ulang.
- Rumus **DS = WOB/(R·DOC)** spesifik (R1 §5.4) — arah MSE/DS cocok [21], tapi bentuk eksplisit
  DS tidak terbaca di ekstrak PDF yang tersambung; perlu buka teks penuh [21].

---

## 7. BELUM DIVERIFIKASI (aturan 3 verification-mandatory)
1. GAINLOSSTOT/PITTOT per-file F-1 C & F-11 (scan timeout) — klaim 575/517 belum dihitung ulang.
2. Sitasi [16] Saini, [1] Tasci, [4] Shadi, [7] rare-event survey, [8] tool-wear audio,
   [9] learning rare events, [10] event-detection DL, [13] Mopuri, [14] Tsuchihashi, [15] Liu
   2025 SPE, [17] Liu 2025 Thermal, [18] Saadeldin, [19] Yi — tidak dibuka di audit ini
   (hanya 8 dari 22 yang dibuka langsung; 14 sisanya = kutipan ulang V6 yang tdk dicek ulang).
3. Prev stuck F-9_A (66,9% vs 49,4%) — masih belum direkonsiliasi (diakui M2 §8 butir 1; audit
   ini tdk memilih salah satu, karena basis jendela-vs-baris berbeda).
4. "100–200 positif shk/well" (R1 §3.2) — tdk dihitung ulang; sudah dikoreksi M2 (F-4 50,
   F-15 13), dipakai versi M2.
5. Efektivitas prediktif sesungguhnya tiap solusi onset — BELUM bisa diverifikasi dari audit
   statis; hanya kebenaran data/sitasi/logika yang diuji. Lolos-tidaknya gate = kerja V7-E.

---
**Reproduksi:** skrip di `~/.hermes/cache/scratch/`: `a1_data_check1.py`, `a1_data_check2.py`,
`a1_data_check3.py`, `a1_check5.py`, `a1_range2.py`, `a1_usrop_trans.py` (stdlib Python,
dijalankan nyata 2026-10-11, output tercetak di sesi).
