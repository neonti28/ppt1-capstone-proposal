# V6-D1e — Audit WITSML LOG XML Mentah (7150 file) vs Parser Lama

**Riset pendahuluan: `verification-mandatory` — verifikasi ulang 2026-10-11 dengan glob recursive: total file log XML = 7150, cocok dengan klaim PASS A §1.**

Tanggal: 2026-10-10
Task: t_c74f2838 (kanban capstone-v6-solve)
Metode: sampling header semua file (regex, tanpa parse penuh); sampling penuh 24 file lintas 6 wellbore; komparasi kurva mentah vs kolom CSV parser lama; verifikasi data WHIRL_RT vs BOUNCE_RT per `<data>` element.

## 0. Struktur direktori (ditemukan saat audit; penting untuk semua pass berikutnya)

Struktur yang benar BUKAN `<wb>/log/*/*.xml`, melainkan:

```
witsml_raw/<wellbore>/<ver>/log/<logSet>/<log>/<chunk?>/NNNNN.xml
```

Contoh: `Norway-StatoilHydro-15_$47$_9-F-14/1/log/2/2/1/00028.xml`

Format XML log: `<logCurveInfo>` per kurva (mnemonic/unit/deskripsi), lalu `<logData>` berisi `<mnemonicList>` + `<unitList>` + banyak elemen `<data>` (satu baris data per elemen, dipisah koma, tanpa newline).

## 1. Jumlah file per wellbore dan indexType (PASS A — SEMUA 7150 file, bukan sampling)

Total file log XML: **7150** (persis seperti angka klaim lama; terverifikasi).

Grand total per indexType: **date time = 6075 file (85.0%)**, **measured depth = 1075 file (15.0%)**.

Detail per wellbore direktori (23 direktori memiliki file log):

| File | Wellbore direktori | date time | measured depth |
|---:|---|---:|---:|
| 2156 | Norway-Statoil-NO 15/9-F-1 C | 1731 | 425 |
| 1750 | Norway-Statoil-NO 15/9-F-11 | 1341 | 409 |
| 1100 | Norway-Statoil-NO 15/9-F-15 | 972 | 128 |
| 271 | Norway-StatoilHydro 15/9-F-10 | 242 | 29 |
| 233 | Norway-Statoil 15/9-F-12 | 215 | 18 |
| 229 | Norway-StatoilHydro 15/9-F-4 | 223 | 6 |
| 203 | Norway-StatoilHydro 15/9-F-15S | 190 | 13 |
| 183 | Norway-StatoilHydro 15/9-F-14 | 171 | 12 |
| 153 | Norway-Statoil-NO 15/9-F-14 | 151 | 2 |
| 136 | Norway-StatoilHydro 15/9-F-5 | 132 | 4 |
| 127 | Norway-Statoil-NO 15/9-F-5 | 126 | 1 |
| 115 | Norway-StatoilHydro 15/9-F-15A | 109 | 6 |
| 110 | Norway-Statoil-NO 15/9-F-12 | 110 | 0 |
| 92 | Norway-StatoilHydro 15/9-F-15 | 80 | 12 |
| 60 | Norway-Statoil 15/9-F-7 | 57 | 3 |
| 57 | Norway-Statoil-NO 15/9-F-4 | 56 | 1 |
| 51 | Norway-StatoilHydro 15/9-F-9 | 49 | 2 |
| 46 | Norway-NA 15/9-F-9 A | 44 | 2 |
| 22 | Norway-Statoil-NO 15/9-F-7 | 22 | 0 |
| 18 | Norway-Statoil-NO 15/9-F-9 | 17 | 1 |
| 16 | Norway-StatoilHydro 15/9-F-15B | 15 | 1 |
| 14 | NA-NA 15/9-F-5 | 14 | 0 |
| 8 | Norway-NA 15/9-F-1 | 8 | 0 |

Data mentah tersimpan: `/mnt/d/Capstone 1/scratch/v6_d1e_scan_indexType.json` (7150 baris, per-file).

## 2. Sample lintas wellbore (PASS B — 24 file, 6 keluarga wellbore)

CSV: `/mnt/d/Capstone 1/scratch/v6_d1e_log_sample.csv` (1022 baris kurva, 24 file, kolom: family, wellbore_dir, file, log_name, indexType, curve_seq, mnemonic, unit, description).

5 raw dump header tersimpan di workspace task (`raw_dumps/`). Ringkasan sample:

| Family | File di-sample | Mnemonic unik | indexType terlihat |
|---|---:|---:|---|
| F-14 | 4 | 127 | measured depth + date time |
| F-5 | 4 | 183 | date time + measured depth |
| F-9 | 4 | 242 | date time |
| F-15 (termasuk F-15S) | 4 | 141 | measured depth + date time |
| F-1 C | 4 | 70 | date time + measured depth |
| F-11 | 4 | 106 | measured depth + date time |

Contoh raw (2 dari 5 dump):
- `Norway-Statoil-NO 15/9-F-14/1/log/1/1/1/00001.xml`, 15937 byte, indexType="measured depth", 46 kurva — berisi kurva MWD (INCL_CONT_RT, AZIM_CONT_RT, G_IC5, TDH, TVA, dst).
- `Norway-StatoilHydro-15/9-F-14/2/log/1/1/1/00001.xml`, 4671 byte, indexType="date time", 12 kurva.

## 3. Coverage parser lama: kurva TERLEWAT (PASS C)

CSV parser lama (`witsml_parsed/`) hanya punya 8 output: F-14, F-15A, F-15_S, F-5, F-7, F-9, F-9_A, VAR_F-5_alt.

Temuan coverage (dari 4 file sample per wellbore; angka adalah mnemonic unik yang ada di file mentah tapi TIDAK ada di kolom CSV parsed):

| Wellbore | Mnemonic unik di sample mentah | Tidak ada di CSV parsed | Catatan |
|---|---:|---:|---|
| F-14 | 127 | 59 | sebagian besar kurva chromatograph (CHR1*, *CIR) + RIGHEAVE + Depth/EditFlag |
| F-5 | 183 | 88 | HKLD_AVG/MAX/MIN, TORQUE_*, MOTOR_RPM, FLOWIN/OUT, MSE, PIT* |
| F-9 | 242 | 47 | PIT1..PIT30, PIT_PITTOT, CIRCVOL, DISPVOL, GAINLOSSTOT |
| F-15 | 141 | 65 | HKLD_*, TORQUE_*, FLOWIN/OUT, BIT_RPM_*, RIGHEAVE |
| F-1 C | 70 | 70 (**tidak ada CSV sama sekali**) | wellbore F-1 C tidak diparse sama sekali oleh parser lama |
| F-11 | 106 | 106 (**tidak ada CSV sama sekali**) | wellbore F-11 tidak diparse sama sekali oleh parser lama |

Temuan terbesar bukan duplikasi kurva individual, melainkan:

1. **Dua wellbore terbesar tidak diparse sama sekali.** F-1 C (2156 file) dan F-11 (1750 file) = **3906 file = 54,6% dari seluruh dataset log** tidak punya CSV output di `witsml_parsed/`. Bahkan `_coverage.json` dan `_verify.json` hanya memuat 8 wellbore; F-1 C dan F-11 tidak muncul di sana.
2. **Untuk wellbore yang diparse, sebagian besar kurva ada di CSV** (gap 47–88 mnemonic dari 127–242 sample). Gap terbesar di F-5 (88) dan F-15 (65): terutama seri HKLD_AVG/MAX/MIN, TORQUE_AVG/MAX/MIN, MOTOR_RPM, FLOWIN/FLOWOUT, FLOWOUTPC, MWIN/MWOUT, PIT*, MSE/DMSE/I_MSE, RIGHEAVE*, dan INDEX-helper (Depth, DEPTH, MDEPTH, EditFlag, RigActivityCode, TIME/Time).

Catatan: beberapa "missing" adalah non-kurva teknis (Depth/EditFlag/index helper), tapi HKLD_AVG/MAX/MIN, MOTOR_RPM, FLOWIN/FLOWOUT, TORQUE_AVG/MAX/MIN, MSE adalah kurva sains nyata yang terlewat.

Detail list per wellbore: `/home/neonti/.hermes/kanban/boards/capstone-v6-solve/workspaces/t_c74f2838/pass_c_missing.json`.

## 4. Bug WHIRL_RT == BOUNCE_RT: KONFIRMASI lintas well (PASS D + E)

Scan global semua 7150 file header:
- File yang mengandung WHIRL_RT: **67**
- File yang mengandung BOUNCE_RT: **70**
- File yang mengandung keduanya dalam log yang sama: **67** (semua file WHIRL_RT selalu punya BOUNCE_RT)

5 wellbore terdampak (bukan hanya F-14):

| Jumlah file | Wellbore |
|---:|---|
| 23 | Norway-StatoilHydro 15/9-F-9 |
| 19 | Norway-StatoilHydro 15/9-F-14 |
| 16 | Norway-StatoilHydro 15/9-F-5 |
| 5 | Norway-StatoilHydro 15/9-F-15S |
| 4 | Norway-NA 15/9-F-1 |

Verifikasi pada level data (bukan cuma nama kurva): untuk 1 file terbesar per wellbore, kolom WHIRL_RT dan BOUNCE_RT dibandingkan per baris `<data>`:

| File | rows | non-null WHIRL | non-null BOUNCE | identik saat keduanya non-null |
|---|---:|---:|---:|---|
| F-9 `/1/log/1/2/1/00005.xml` | 10000 | 1790 | 1790 | **1790/1790** |
| F-14 `/1/log/2/2/1/00002.xml` | 10000 | 0 | 0 | 0/0 (kedua kolom kosong) |
| F-5 `/1/log/1/1/1/00016.xml` | 10000 | 368 | 368 | **368/368** |
| F-15S `/1/log/1/3/1/00003.xml` | 10000 | 5 | 5 | **5/5** |
| F-1 `/1/log/1/2/1/00004.xml` | 10000 | 15 | 15 | **15/15** |

Kesimpulan: **BUG TERKONFIRMASI dan bersifat lintas wellbore**, bukan spesifik F-14. Pada setiap baris tempat keduanya terisi, nilainya identik persis; jumlah baris non-null juga selalu sama. Dua kemungkinan mekanisme: (a) data mentah Volve memang menyalin sinyal yang sama ke dua mnemonic, atau (b) bug berada di sumber ekspor Volve, bukan di parser kita. Yang pasti dari sisi kita: **jangan memakai WHIRL_RT dan BOUNCE_RT sebagai dua fitur terpisah**; keduanya redundan.

Detail: `pass_e_whirl_data.json`.

## 5. Angka nyata (ringkas)

- Total file log XML: **7150** (23 direktori wellbore).
- indexType: **6075 date time (85.0%)**, **1075 measured depth (15.0%)**.
- Parser lama memproduksi **8 CSV**; **2 wellbore terbesar (F-1 C: 2156 file, F-11: 1750 file = 3906 file / 54.6%) tidak diparse sama sekali**.
- Sample 24 file lintas 6 wellbore: **1022 baris kurva** tercatat di `v6_d1e_log_sample.csv`.
- Gap kurva per wellbore yang diparse (sample 4 file/wellbore): F-14: 59, F-5: 88, F-9: 47, F-15: 65 mnemonic tak ada di CSV parsed.
- WHIRL_RT/BOUNCE_RT: **67 file, 5 wellbore, duplikasi identik terkonfirmasi di 4 wellbore dengan data non-null** (F-14 file yang dicek kebetulan kolomnya kosong semua).

## 6. Implikasi untuk V6

1. Parser coverage = 8 wellbore, bukan seluruh dataset. Kalau klaim lama menyebut "7150 file sudah diparse ke CSV", itu hanya benar untuk file mentah yang dibaca; output CSV tidak mencakup F-1 C dan F-11 (54.6% file). Ini gap coverage terbesar.
2. Untuk wellbore yang sudah diparse, sebagian besar kurva ada, tapi beberapa seri kurva sains berguna (HKLD_*/TORQUE_*/MOTOR_RPM/FLOWIN-OUT/MSE/PIT*) tidak masuk CSV.
3. WHIRL_RT vs BOUNCE_RT: redundan lintas wellbore — jangan dihitung dua fitur.

## File output

- `/mnt/d/Capstone 1/scratch/v6_d1e_log_sample.csv` (24 file sample, 1022 kurva)
- `/mnt/d/Capstone 1/scratch/v6_d1e_scan_indexType.json` (7150 file, indexType per file)
- `docs/V6_D1e_LOG_XML.md` (dokumen ini)
- Raw dump 5 file: workspace task `raw_dumps/`
- Pass artifacts: `pass_c_missing.json`, `pass_e_whirl_data.json` (workspace task)
