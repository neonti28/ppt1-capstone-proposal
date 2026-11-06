# V7-D1h — CEK KETERSEDIAAN DATA (domain: KAGGLE + CATALOG)

Task: `t_4ec90702` [Pembaca 08] · Board: capstone-v7-solve · Tanggal: 2026-10-11 (WIB)
Spesifikasi: komentar kartu dari Master V7-M1 (`t_0d02b12f`, `docs/V7_M1_DELEGASI.md` §2.8).

> **Riset pendahuluan: `verification-mandatory`** — semua angka di bawah dihasilkan skrip yang dijalankan nyata (`~/.../scratch/v7_d1h/step*.py`, output mentah `step2b_stdout.txt`, `step3_stdout.txt`, `step4_toolwear.json`, `step5_out.json`); nol angka dari ingatan. Rekonsiliasi 884-vs-1.412 diselesaikan dengan menghitung record csv vs baris fisik (bukan dengan memilih salah satu klaim).
> **Riset pendahuluan: `scientific-critical-thinking`** — tiap butir dipisah: APA yang terbukti ada (data mentah) vs APA yang masih hipotesis (mis. "prev 66,9%"); kontradiksi angka dilaporkan apa adanya, tidak diluruskan agar cocok narasi.

---

## 0. RINGKASAN STATUS

| # | Solusi | Data needed | Status |
|---|---|---|---|
| 1 | S-A1 stuck onset | STUCK_RT + kanal dysfungsional di time.csv F-9 A | **ADA LANGSUNG** (45.715 baris non-null; 50 onset 0→1) |
| 2 | S-C2/S-C1 pit/flow/SPPA | PITTOT/GAINLOSSTOT/FLOWOUT/SPPA/TFLO/SPM di time.csv | **ADA SETELAH DIOLAH** (mnemonic mentah tidak ada; padanan deskriptif ada, 64.757–345.442 non-null) |
| 3 | S-A3 prasyarat | labels_curated_v2.csv 1.412 vs 884 event | **REKONSILIASI SELESAI: 884 event benar** (1.413 = baris fisik akibat field multiline) |
| 4 | S-D3/S-F1/S-F2 | USROP_labeled.csv WOB/ROP/RPM/MSE/label | **ADA LANGSUNG** (198.928 baris, semua kolom 100% non-null, 1.489 transisi label) |
| 5 | S-D1/D2/D4 | 8 xlsx toolwear | **ADA LANGSUNG** (8/8 file, 471.400 sampel, 0 NaN, sampling konstan) |
| 6 | Aux stratigrafi | well picks 409 + WBS* lithology | picks **ADA LANGSUNG** (409 baris/35 wellbore); WBS* di CSV **TIDAK ADA** efektif (2 baris non-null) |
| 7 | Zip kaggle F-9 A | duplikat identik? | **TERKONFIRMASI DUPLIKAT** (SHA-256 isi zip = file lokal, identik) |

---

## 1. S-A1 — `STUCK_RT` di time.csv F-9 A → ADA LANGSUNG

File: `data/witsml/Norway-NA-15_47_9-F-9 A time.csv` (427.910.797 bytes; **419.747 baris data**, 239 kolom; rentang `DateTime parsed` 2009-06-27 16:50:29 → 2009-07-16 16:11:33 UTC).

Catatan NAMING (penting untuk semua pembaca lain): kolom di CSV ini memakai nama deskriptif+satuan, BUKAN mnemonic mentah. Pencocokan persis `CRPM_RT`/`SHKRSK_RT`/`VIBLAT_RT`/`STICK_RT`/`STKSLP`/`PITTOT`/`SPPA`/`TFLO`/`SPM` = **0 temuan**; yang ada padanan fungsionalnya (tabel di §2).

| Kolom (nama asli di CSV) | Non-null | Keterangan |
|---|---:|---|
| `STUCK_RT unitless` | **45.715** | value counts: 0.0 = 23.123 · 1.0 = 3.171 · 2.0 = 363 · **3.0 = 19.058**; total `≥1` = 22.592 baris |
| `SHK3TM_RT min` | 45.914 | shock-related |
| `MWD Total Shocks unitless` | 46.900 | |
| `MWD Shock Risk unitless` | 45.930 | |
| `MWD Shock Peak m/s2` | 45.914 | |
| `PowerUP Shock Rate 1/s` | 45.914 | |
| `MWD Stick-Slip PKtoPK RPM rpm` | 15.023 | padanan ssi (bukan `CRPM_RT`) |
| `MWD Collar RPM rpm` | 15.185 | padanan collar RPM |
| `MWD Turbine RPM rpm` | 45.830 | |

**Transisi (kandidat onset S-A1):** `0→1` persis = **50** · `1→0` = 49 · biner `(≥1) 0→1` = **74**.
→ Proses jadi label onset: ambil titik `t_e` pada tiap transisi, jendela positif `[t0−10,t0)` dengan `t0 ∈ [t_e−H, t_e]`, blok `≥1` setelah onset dibuang (bukan dinegatifkan) — sesuai rumus S-A1 V7-R1 §2.2. Jumlah onset 50–74 per F-9_A.

**Temuan yang MENYULITKAN (dilaporkan apa adanya):**
1. Dominan nilai `3.0` (19.058 dari 22.592 baris `≥1`) — semantik 0/1/2/3 tetap tidak terdokumentasi (konsisten catatan pra-reg E1 §7.5). Onset 1→2→3 juga mungkin "onset" berlapis; keputusan ambang biner `≥1` vs `>2` = desain label, wajib pra-reg.
2. Prev `≥1` pada baris non-null = 22.592/45.715 = **49,4%** — ANGKA INI TIDAK COCOK dengan prev 66,9% F-9_A di V6_E1 §4.4 (kemungkinan beda basis: jendela grid V6 vs baris mentah; wajib direkonsiliasi pembaca ML sebelum dipakai, jangan asumsikan).
3. Kanal dysfungsi hanya terisi ~45–47 ribu dari 419.747 baris (11%) — jendela fitur hanya bisa dibentuk di rentang itu; jumlah onset efektif per jendela perlu dihitung saat eksekusi.

## 2. S-C2/S-C1 — kanal pit/flow/SPPA di time.csv → ADA SETELAH DIOLAH

Mnemonic mentah `PITTOT`, `GAINLOSSTOT`, `FLOWOUT`, `FLOWOUTPC`, `SPPA`, `TFLO`, `SPM` **TIDAK ADA** sebagai nama kolom (bukti: pencocokan persis atas header 239 kolom = 0; `PIT*_COLS: []`). Yang ADA (padanan fungsional):

| Kebutuhan label | Kolom padanan di time.csv | Non-null |
|---|---|---:|
| SPP (standpipe pressure) | `Stand Pipe Pressure kPa` | **345.442** |
| | `Average Standpipe Pressure kPa` / `SPP5s kPa` / `SPP-VPWD kPa` / `SPP-APWD kPa` | 85.929 (masing-masing) |
| Q_in | `Mud Flow In L/min` | 83.565 |
| Q_out proxy | `Flow Pumps L/min` | 345.442 |
| TFLO | `TFLO30s L/min` | 64.757 |
| SPM | `Total SPM 1/min` | 56.772 · `Pump 1..4 Stroke Rate 1/min` 86.314 (tiap kolom) |
| Pit volume | `MudPit Volume Average {1,2,4,5,6,7,8,9,10,12} m3` | **345.442 tiap kolom** (12 kolom pit; catatan: nomor 3 & 11 tidak ada di header) |
| | `MudPit Volume Average13/14 m3` | 305.233 / 305.239 |
| Pit gain | `Tank volume (active) m3` + `Tank volume change (active) m3` | 345.442 (keduanya) |
| | `Fill/gain volume obs. (cum) m3` | 284.843 |

→ **Proses:** (a) S-C1 onset-hyd: hitung ulang `|z|>2` residual SPPA vs median/MAD per bin `qcut(TFLO,10)` dari `Stand Pipe Pressure kPa` + `TFLO30s L/min` — langsung dari CSV, nol parse XML. (b) S-C2 label pit/flow: `ΔV_pit` = diff temporal `Tank volume (active) m3` / tiap `MudPit Volume Average *` (z-score per well) untuk kick/loss; `Q_out−Q_in` = `Flow Pumps L/min − Mud Flow In L/min` untuk washout — estimasi 345.442 baris label sebelum intersect dengan rentang non-null tiap kanal. **Jalur cepat S-C2 di F-9 A TIDAK butuh parse F-9 raw** (klaim V7-R1 §4.3 bahwa jalur cepat butuh parse tambahan kecil bisa diturunkan beban-nya: semua kanal sumber label sudah ada di CSV time.csv F-9 A; parse raw hanya perlu kalau label mau dibuat di sumur lain).

## 3. S-A3 PRASYARAT — labels_curated_v2.csv → REKONSILIASI: 884 EVENT, klaim 1.412 SALAH

File: `data/volve/labels_curated_v2.csv` (519.171 bytes).

| Metode | Hasil |
|---|---|
| `wc -l` (baris fisik newline) | **1.413** (1.412 + header) — INI sumber klaim V7-R1 |
| Parser csv (`csv.reader`, menghormati quoting) | **885 record = header + 884 event** |
| `event_id` unik | 884/884 (tanpa duplikat) |
| Distribusi jumlah field | seragam 20 kolom di 885 record (tidak ada baris rusak) |
| Baris berisi newline di dalam quoted field | `evidence` 33 baris · `comments_full` 83 baris → 529 newline tambahan: 885 + 528 = 1.413 ✓ |

**Kesimpulan: V6_R1 (884 event) BENAR; klaim V7-R1 §2.4 "1.412 baris event" = artefak menghitung baris fisik file yang berisi quoted-newline.** Prasyarat S-A3 terpenuhi: rekonsiliasi selesai, silang-sumber pakai 884.

Kolom (20): `event_id, wellbore, event_date, act_start, act_end, ddr_date_start, md, md_valid, source_code, state_detail, category, bha_relevant, evidence, match_rules, comments_full, comments_trunc300, outcome, outcome_reason, component, component_reason`.
Distribusi wellbore: F-14 182 · F-5 136 · F-15 D 122 · F-15 112 · **F-9 A 94** · F-15 C 89 · F-7 59 · F-9 56 · F-15 A 32 · F-15 B 2.
Kategori: routine_no_failure_evidence 496 · surface_rig_equipment 216 · mixed_evidence 47 · **bha_stuck_fishing 38** · failure_unlocated 28 · wellbore_fluid 25 · wireline 21 · bha_downhole_equipment 12 · safety 1.
→ **Peluang relasi (untuk Master):** `act_start`/`act_end` (timestamp ISO) + `md` + `wellbore` = join key ganda ke time.csv F-9 A (`DateTime parsed` non-null 419.745) dan ke parsed CSV wellbore lain — LF2 Snorkel (S-A3) bisa langsung menyandingkan 94 event F-9 A dengan deret `STUCK_RT` tanpa parse ulang; 38 event `bha_stuck_fishing` = kandidat LF khusus stuck.

## 4. S-D3/S-F1/S-F2 — USROP_labeled.csv → ADA LANGSUNG

File: `data/USROP_labeled.csv` (51.055.017 bytes; **198.928 baris data**; 18 kolom; 7 well).

| Kolom yang diminta Master | Ada? | Non-null |
|---|---|---:|
| `Weight on Bit kkgf` (WOB) | ya | **198.928 (100%)** |
| `Rate of Penetration m/h` (ROP) | ya | 198.928 (100%) |
| `Average Rotary Speed rpm` (RPM) | ya | 198.928 (100%) |
| `MSE` | ya | 198.928 (100%) |
| `label` | ya | 198.928 (100%) |
| depth | ya (`Measured Depth m`) | 198.928 (100%) |
| time | **TIDAK ADA** — dataset depth-domain, hanya `Measured Depth m` (dan `Hole Depth (TVD) m`) | — |

Kolom lain yang TERSEDIA untuk turunan: `Diameter mm` (diameter bit, 100%), `Average Standpipe Pressure kPa`, `Average Surface Torque kN.m`, `Mud Flow In L/min`, `Mud Density In g/cm3`, `Average Hookload kkgf`, `USROP Gamma gAPI`, `D_exp`, `ROC_coef`.

Distribusi `label`: `normal` **134.013** (67,4%) · `high_MSE_bit_wear` **49.732** (25,0%) · `low_ROP_efficiency` **15.183** (7,6%).
Per well: F-15 d 53.041 · F-15 S 51.708 · F-14 47.645 · F-5 18.548 · F-9 A 13.746 · F-9 7.851 · F-7 6.389.
**Transisi blok `label` (kandidat onset S-F1): 1.489** di seluruh file (perubahan nilai label antar baris berurutan dalam well yang sama).

→ **Proses DS/DOC (S-D3/S-F2):** `DOC = ROP/(60·RPM)`, `DS = WOB/(R·DOC)` dengan `R = Diameter mm / 2000` (m) — semua input ada; WOB perlu konversi kkgf→kN (×9,80665), MSE sudah terhitung di kolom. Estimasi hasil: 198.928 baris (100%).
→ **Onset S-F1:** label onset = transisi blok menuju `high_MSE_bit_wear`; jumlah kandidat = bagian dari 1.489 transisi (perlu difilter per well & per tujuan kelas — dihitung saat eksekusi).
→ **Peluang relasi:** kolom `well` berformat nama file (`USROP_A 0 N-NA_F-9_Ad.csv`) — join ke wellbore Volve perlu mapping manual 7 nama; `Measured Depth m` bisa join ke well picks (§6) via wellbore+MD.

## 5. S-D1/D2/D4 — 8 xlsx toolwear → ADA LANGSUNG (semua syarat terpenuhi)

Lokasi: `scratch/v6_e1/toolwear/DrillingToolWearDataset_T0{1..4}_R0{1,2}.xlsx` — **8/8 file ADA** (2,36–3,07 MB tiap file).

Per file: 1 sheet (`Sheet1`); 4 baris meta + 1 baris header (`Sample No., X, Y, Z`); kolom = nomor sampel + 3 kanal akselerometer.

| File | Baris data | NaN (X/Y/Z) | Sample No. | Durasi @1000 Hz |
|---|---:|---:|---|---:|
| T01_R01 | 60.500 | **0** | 1..60.500 step 1 konstan | 60,5 s |
| T01_R02 | 60.400 | 0 | 1..60.400 step 1 | 60,4 s |
| T02_R01 | 50.000 | 0 | 1..50.000 step 1 | 50,0 s |
| T02_R02 | 62.000 | 0 | 1..62.000 step 1 | 62,0 s |
| T03_R01 | 61.500 | 0 | 1..61.500 step 1 | 61,5 s |
| T03_R02 | 60.000 | 0 | 1..60.000 step 1 | 60,0 s |
| T04_R01 | 58.500 | 0 | 1..58.500 step 1 | 58,5 s |
| T04_R02 | 58.500 | 0 | 1..58.500 step 1 | 58,5 s |

Total **471.400 sampel**, 0 NaN di semua file/kanal. Meta tiap file: `Sampling Rate: 1000 samples/second` (dinyatakan di file), `Drilling Speed: 490 RPM`, `Feed: 0.285 mm/rev` (IDENTIK di 8/8 file → konfounds run-order TIDAK bisa dijelaskan oleh parameter pahat yang berbeda). Sampling terverifikasi konstan: `Sample No.` bertambah persis 1,0 tiap baris (dicek penuh, bukan asumsi dari metadata).
→ Syarat S-D1 (change-point per run pada deret fitur pendek), S-D2 (VMD per segmen), S-D4 (ranking pasangan dalam-alat) terpenuhi secara data. Catatan jujur: tidak ada kolom `time` eksplisit — waktu = `Sample No. / 1000` s (konstruksi deterministik, bukan pengukuran terpisah); durasi run 50–62 detik → change-point harus dalam skala detik.

## 6. Aux label — well picks: ADA LANGSUNG; WBS* lithology di CSV: TIDAK ADA (efektif)

File: `data/volve/external/spwla_volve_logs/Well_picks_Volve_v1.dat` (74.548 bytes).
Hasil scan: **35 wellbore**, **409 baris pick** (klaim "409" TERKONFIRMASI). Flag kualitas pada baris pick: `NL` 51 · `NR` 17 · `FP` 17 · `FO` 1 · `ER` 1 (sisa 323 tanpa flag). Format kolom: well name, formation/surface name, Obs#, Qlf, MD, TVD, TVDSS, TWT, Dip, Azi, Easting, Northing, Intrp.
→ **Join key:** `well name` (mis. `NO 15/9-F-14`) + `MD` (m). Label stratigrafi lintas 35 wellbore LAYAK dibentuk lewat join MD-window ke deret kedalaman mana pun (USROP `Measured Depth m` maupun parsed CSV Volve).

Yang TIDAK ADA: kolom `WBSLITHOLOGY1..5 unitless` memang ADA di time.csv F-9 A, tapi **non-null hanya 2 baris dari 419.747** (dan `Time Time` non-null juga cuma 2 — kolom WBS hampir pasti sisa join katalog yang gagal terisi). **Bukti ketiadaan fungsi:** label litologi dari kolom WBS* di CSV ini TIDAK BISA dipakai — gunakan well picks `.dat` sebagai sumber label stratigrafi, bukan kolom WBS*.

`VOLVE_INVENTORY.xlsx` (`data/volve/external/spwla_volve_logs/`, sheet: INVENTORY + 24 wellbore) = indeks file log per wellbore (nama file, tipe dataset, provider, interval). Contoh: sheet `15_9-F-9 A` 14 baris (ada DLIS/WLC 415,3–1205,8 m), `15_9-F-10` 42 baris, `15_9-F-4` 42, `15_9-F-12` 47, `15_9-F-15` 31. **Fungsi:** perencanaan parse (file mana berisi apa), BUKAN sumber fitur/label.
`volve_catalog_target_paths.csv` (`data/volve/external/`): 4.035 baris path dbfs per kategori file (segy/dlis/csv/dst) — pemetaan katalog, bukan data.

## 7. Zip kaggle → DUPLIKAT IDENTIK (bukan data baru)

| Zip | Isi | SHA-256 isi vs file lokal |
|---|---|---|
| `data/volve/external/kaggle/kaggle_volve_witsml_F9A.zip` (40,4 MB; sha256 zip `fbab41c1a914ee8e…`) | `Norway-NA-15_47_9-F-9 A time.csv` (427.910.797 B) + `… depth.csv` (5.596.360 B) | **IDENTIK** dengan `data/witsml/` kedua file (dicek SHA-256 penuh per entry vs file lokal — cocok 2/2) |
| `kaggle_drilling_log_dataset_F15.zip` (6,1 KB) | 1 file: `ROP data .csv` (17.751 B) | dataset ROP kecil F-15 — BUKAN duplikat time.csv; kandidat sumber fitur tambahan kecil (belum dibuka isinya di luar listing) |

→ **Konfirmasi untuk Master: zip F-9 A = duplikat byte-identik dari `data/witsml/`, JANGAN dihitung data baru / sumur tambahan.**

---

## 8. PELUANG PROSES / RELASI ANTAR-FILE (untuk analisis Master)

1. **time.csv F-9 A ↔ labels_curated_v2.csv**: join `wellbore='NO 15/9-F-9 A'` + `act_start/act_end` ↔ `DateTime parsed` → 94 event kurasi bisa divalidasi terhadap 50 onset `STUCK_RT` (apakah onset punya bukti DDR?). Bahan LF2 Snorkel S-A3 + validasi semantik `STUCK_RT` (is stuck beneran atau false positive instrumen?).
2. **USROP_labeled ↔ well picks .dat**: join wellbore + `Measured Depth m` ↔ MD pick → fitur litologi/stratigrafi masuk kampanye `bit_wear` (mengurangi "mengingat posisi kedalaman" via fitur geologi eksplisit — melawan temuan SHAP F-15 yang didominasi `MD_last/mean`).
3. **S-C2 jalur cepat di F-9 A**: semua kanal sumber label (pit volume, tank active, flow) sudah di time.csv — parse raw F-9 (yang di V7-R1 jadi beban) bisa ditunda; beban solusi hyd turun satu tingkat.
4. **time.csv ↔ depth.csv F-9 A**: depth.csv (16.670 baris, 115 kolom) memuat `STUCK_RT` juga — dipakai untuk cek kedalaman saat onset (MD onset stuck), join by timestamp-depth grid.
5. **WBS\* ≠ sumber litologi** (§6) — siapa pun yang berencana pakai kolom WBS* dari CSV: batal, pakai picks `.dat`.

## 9. KOREKSI TERHADAP KLAIM SEBELUMNYA

| Klaim (sumber) | Status setelah dicek | Bukti |
|---|---|---|
| labels_curated_v2 = 1.412 event (V7-R1 §2.4, §9.2) | **SALAH** — artefak hitung baris fisik; parser csv = 884 event | step3b: physical_newlines 1.413 vs csv_records 885; 528 newline di quoted fields; event_id unik 884 |
| "884 event" (V6_R1) | **BENAR** | idem |
| prev F-9_A stuck = 66,9% (V6_E1 §4.4) | **TIDAK TERREPRODUKSI** dari baris mentah: 22.592/45.715 = 49,4% non-null (basis berbeda mungkin; jangan dipakai tanpa rekonsiliasi basis) | step2b value counts |
| "jalur cepat S-C2 butuh parse F-9 raw" (V7-R1 §4.3) | **DITURUNKAN**: kanal pit/flow sudah ada di time.csv F-9 A (345.442 non-null) | §2 tabel |
| picks "409" (D0/R1) | BENAR | step5: 409 baris, 35 wellbore |

## 10. BELUM DICEK (jujur)

- Isi `ROP data .csv` di kaggle F15 zip (baru listing entry, belum dibuka barisnya).
- Seluruh isi per-sheet `VOLVE_INVENTORY.xlsx` (baru header + jumlah baris tiap sheet).
- Transisi onset per well di USROP (baru total 1.489; per-well belum dipisah).
- Kelayakan jendela fitur F-9 A (apakah 45.715 baris non-null cukup membentuk N jendela ≥10 menit setelah intersect dengan kanal fitur) — perlu hitung saat eksekusi S-A1.
- CSV parsed 7 sumur Volve (`data/volve/witsml_parsed/`) — di luar domainku (Pembaca lain).

## Sumber bukti (skrip & output mentah)

`~/.hermes/cache/scratch/v7_d1h/`: `step1_header.py` (header 239 kolom), `step2b_stream.py` + `step2b_stdout.txt` (non-null/transisi time.csv), `step3_labels_usrop.py` + `step3_stdout.txt`, `step3b_reconcile.py` (rekonsiliasi 884/1.413), `step4_toolwear.py` + `step4_toolwear.json` (8 xlsx), `step5_picks_inv_zip.py` + `step5_out.json` (picks/inventory/checksum). Semua dijalankan nyata 2026-10-11; kelangsungan hidup: file mentah tersimpan di cache scratch.
