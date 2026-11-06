# V3 — Laporan Parse WITSML Time-Based (T9)

Status: SELESAI (2026-10-05)
Sumber: `data/volve/witsml_raw/` (ekstrak 20.086 file dari zip 2,88 GB, gagal=0)
Output: `data/volve/witsml_parsed/*.csv` + `*_qc.json` + `_parse_summary.json` + `_verify.json` + `_coverage.json`

## 1. Ringkasan per wellbore (diverifikasi ulang scan kedua)

| Wellbore | Baris | Channel | Channel ≥50% fill | Rentang UTC | Label in-range |
|---|---:|---:|---:|---|---:|
| F-14 | 1,648,026 | 238 | 48 | 2007-11-04 → 2015-09-22 | 182 |
| F-15A | 778,162 | 281 | 42 | 2008-12-08 → 2015-09-22 | 253 |
| F-15_S | 1,883,062 | 244 | 37 | 2008-09-08 → 2015-09-22 | 0 |
| F-5 | 1,286,967 | 181 | 42 | 2007-11-15 → 2015-09-22 | 134 |
| F-7 | 547,500 | 118 | 47 | 2007-09-15 → 2015-09-22 | 58 |
| F-9 | 457,545 | 197 | 42 | 2007-11-26 → 2015-09-22 | 150 |
| F-9_A | 419,706 | 232 | 45 | 2009-06-27 → 2015-09-22 | 94 |
| VAR_F-5_alt | 59,489 | 60 | 44 | 2007-12-17 → 2015-09-22 | 130 |

**Total: 7,080,457 baris time-series, 8 CSV.**

## 2. Catatan kualitas (apa yang SUDAH dicek)

- Parser: WITSML 1.4 `log`/`chunk` XML → pandas; kolom waktu `timestamp` (ISO UTC, suffix `Z`).
- Log berbasis depth (`indexType=depth`, contoh "MWD ... MD Log") **dipisah/di-skip** dan dicatat di QC (`depth_logs_skipped`) — CSV final murni time-based.
- `errors: []` di semua QC = tidak ada chunk XML gagal parse.
- Fill-rate dihitung per kolom (lihat `fill_rate_ge_50pct` di `_verify.json`); threshold 50%.
- Rentang: semua sumur berakhir **2015-09-22** (batas akhir data Volve) — konsisten dokumentasi Equinor.

## 3. Coverage label (`_coverage.json`)

884 label di `labels_curated_v2.csv`; jumlah in-range per sumur = kolom terakhir tabel.

**Peringatan pemetaan (BELUM diperbaiki, jangan diabaikan):**
- `F-15_S` matched=0: nama wellbore `15/9-F-15S` tidak mengandung string label (`NO 15/9-F-15 D/C/A/B`) — perlu pemetaan eksplisit F-15S → label mana.
- `F-15A` matched=357 > label F-15 A (32): filter `contains("F-15")` mengambil lintas varian; **in_range 253 termasuk label sumur lain** — pemetaan wellbore wajib diperbaiki sebelum training.
- `F-9` matched=150 > 56: kasus sama ("F-9" menangkap "F-9 A"; rentang tumpang tindih).

## 4. Channel kandidat fitur (yang BENAR-BENAR ADA)

Dari sampel + QC: `SWOB`, `RPM`, `Bit_RPM`, `TQA` (torque), `HKLD`, `BPOS`, `ROP`, `SPPA` (standpipe pressure), `TFLO` (flow), `MWTI` (mud weight), `GASA`+`G_C1..G_IC5` (mud gas), `TV01..TV14` (pit volume), `DEPT`, `DVER`, `ECD_ARC_RT`, `SHKRSK_RT`/`SHKTOT_RT` (shock), `PASS_NAME`. Channel per sumur 60–281, yang fill ≥50% hanya 37–48 → **pakai threshold 50% saat seleksi fitur**.

## 5. Yang BELUM dicek (jujur)

- Tidak ada validasi nilai fisik (outlier/satuan) — hanya keberadaan + fill-rate.
- Duplikat timestamp belum dihitung per sumur.
- Pemetaan wellbore→label (butir 3) BELUM diperbaiki.
- Timezone sudah `Z` (UTC); belum disilang dengan jam operasi DDR lokal (CET).
- `VAR_F-5_alt` = varian kedua F-5 (folder `NA-NA-15_...`), sengaja TIDAK digabung; keputusan pemakaian di T2-d.

## 6. Rekomendasi ke T10

1. Pakai channel fill ≥50% saja (daftar di `_verify.json`).
2. Sebelum fitur: perbaiki pemetaan wellbore→label (butir 3) — block sementara F-15_S/F-15A/F-9.
3. Unit analisis = event label dengan window waktu **< `act_start`** (anti-leakage).
