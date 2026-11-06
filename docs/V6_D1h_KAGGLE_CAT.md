# V6-D1h — Buka KAGGLE zips + time.csv/depth.csv + catalog + xlsx + well picks

**Riset pendahuluan: `verification-mandatory` — verifikasi ulang 2026-10-11 dengan tool berbeda (byte-count python + zipfile, bukan wc -l penulis): depth.csv = 16671 baris fisik berakhiran newline → 16670 baris data; `ROP data .csv` dari zip = 152 baris termasuk header → 151 baris data — dipakai untuk §2/§3/Kesimpulan.**

Task: t_13e3a454 (Pembaca 08). Semua angka di bawah dari eksekusi nyata (bukan tebakan).
Catatan path: spesifikasi task menyebut `data/witsml/Norway-NA-15_47_9-F-9 A/` dan `data/external/`,
kenyataannya CSV ada di `data/witsml/` (datar) dan external di `data/volve/external/`.

## 1. time.csv F-9 A (427 MB)

Path: `data/witsml/Norway-NA-15_47_9-F-9 A time.csv` (427.910.797 byte)
- Jumlah kolom: **239** (kolom terakhir: `DateTime parsed`, indeks 238)
- Jumlah baris: **419.748 baris total** (1 header + **419.747 baris data**)
- Wellbore: `15/9-F-9 A - Main Wellbore, 12.25 in Section - Time Log`
- Rentang waktu (dari baris pertama + 2 baris terakhir):
  - mulai: **2009-06-27T16:50:29Z**
  - akhir: **2015-09-22T12:21:35Z**
- Isi: full surface drilling time-log (WITSML) — ROP, hookload, SPP, pump strokes, pit volumes,
  gas chromatograph (C1–C5), MWD (GR, inclination, azimuth, toolface, shocks), ECD/ESD, WBS* lithology codes.
  Catatan: baris terakhir adalah record `GlcSettingsLog` (settings, bukan data drilling) — file ini
  pernah dipakai tim sebelumnya (mirror kaggle F9A).
- Kolom penting untuk capstone: `Rate of Penetration m/h`, `ROP30s m/h`, `1/2ft ROP m/h`,
  `Weight On Bit kkgf`, `Averaged RPM rpm`, `STUCK_RT unitless`, `MWD Total Shocks unitless`,
  `Bit Depth m`, `Total Vertical Depth m`.

## 2. depth.csv F-9 A

Path: `data/witsml/Norway-NA-15_47_9-F-9 A depth.csv` (5.596.360 byte; salinan identik juga di `data/volve/external/kaggle/`)
- Jumlah kolom: **115**
- Jumlah baris: **16.671 baris fisik = 1 header + 16.670 baris data** (python bytes: 16671 karakter `\n`, file BERAKHIR newline — koreksi A1 §8b-1: angka lama "16.671 baris data" dan penjelasan "baris terakhir tanpa newline" keduanya salah)
- Isi: MD log wellbore yang sama (12.25 in section) — Measured Depth 273,101 m → 1.205,999 m
- Kolom: MD, conf, rotary speed, STUCK_RT, WOB/hookload terkoreksi, MWD GR/inclination,
  ROP (2 varian), mud density out, gas butane, bit drilling run, dsb.

## 3. Kaggle zips (2 file)

Path: `data/volve/external/kaggle/`

| Zip | Isi |
|---|---|
| `kaggle_drilling_log_dataset_F15.zip` (6.084 byte) | 1 file: `ROP data .csv` (17.751 byte) |
| `kaggle_volve_witsml_F9A.zip` (40.413.012 byte) | 2 file: `... F-9 A depth.csv` (5.596.360) + `... F-9 A time.csv` (427.910.797) — **duplikat identik** dari `data/witsml/` (ukuran byte sama persis, sudah tereksstrak) |

### ROP data .csv (dari zip F15)
- Kolom: **8** — `Depth, WOB, SURF_RPM, ROP_AVG, PHIF, VSH, SW, KLOGH` (ada BOM di kolom Depth)
- Baris data: **151** (152 termasuk header — koreksi A1 §8b-2; kedalaman mulai 3305.0)
- Isi: data petrofisika per kedalaman — PHIF (porosity), VSH (shale volume), SW (water sat),
  KLOGH (log permeability) + ROP/WOB/RPM. Ini **bukan sekadar fitur** — PHIF/VSH/SW/KLOGH adalah
  properti formasi, kandidat kuat untuk label/ground truth formasi pada F-15.

## 4. volve_catalog_target_paths.csv

Path: `data/volve/external/volve_catalog_target_paths.csv` (645.763 byte)
- Kolom: **4** — `category, well, ext, path`
- Baris data: **4.035**
- Distribusi category: `other_target` 3.123, `dlis_target` 468, `las_target` 253, `bhaRun` 175, `mudLog` 16
- Distribusi ekstensi (top): pdf 1.231, xml 797, html 628, **dlis 442**, asc 255, **las 253**, pds 174, segy 102
- Path bertipe `dbfs:/Volumes/equinor_asa_volve_data_village/public/volve/...` → ini path Databricks
  Unity Catalog (marketplace Volve Data Village), bukan path lokal. Berguna sebagai peta aset:
  253 LAS + 442 DLIS tersedia di katalog sumber jika perlu log asli.

## 5. VOLVE_INVENTORY.xlsx

Path: `data/volve/external/spwla_volve_logs/VOLVE_INVENTORY.xlsx`
- **25 sheet**: 1 sheet `INVENTORY` (29 baris x 27 kolom) + 24 sheet per wellbore:

| Sheet | Baris x Kolom | Sheet | Baris x Kolom |
|---|---|---|---|
| INVENTORY | 29 x 27 | 15_9-F-11 A | 27 x 10 |
| 15_9-F-1 | 42 x 10 | 15_9-F-11 B | 29 x 10 |
| 15_9-F-1 A | 32 x 10 | 15_9-F-12 | 48 x 10 |
| 15_9-F-1 B | 40 x 10 | 15_9-F-14 | 39 x 10 |
| 15_9-F-1 C | 42 x 13 | 15_9-F-15 | 32 x 10 |
| 15_9-F-4 | 43 x 61 | 15_9-F-15 A | 39 x 10 |
| 15_9-F-5 | 36 x 11 | 15_9-F-15 B | 22 x 10 |
| 15_9-F-7 | 17 x 10 | 15_9-F-15 C | 30 x 10 |
| 15_9-F-9 | 14 x 10 | 15_9-F-15 D | 23 x 10 |
| 15_9-F-9 A | 15 x 10 | 15_9-19 A | 111 x 24 |
| 15_9-F-10 | 43 x 11 | 15_9-19 B_BT2 | 47 x 25 |
| 15_9-F-11 | 14 x 10 | 15_9-19_S_SR | 63 x 24 |

- Isi: inventaris log SPWLA per wellbore (daftar file/mnemonic per sumur) — peta "log apa saja yang
  tersedia di sumur mana".

## 6. Well_picks_Volve_v1.dat (FORMATION TOPS)

Path: `data/volve/external/spwla_volve_logs/Well_picks_Volve_v1.dat`
- Total baris: **557**
- Jumlah well: **35 wellbore**
- Jumlah baris pick: **409 pick**
- Kolom per pick: `Well name | Surface name | Obs# | Qlf | MD | TVD | TVDSS | TWT | Dip | Azi | Easting | Northing | Intrp`
- Kode kualitas Qlf: `ER`=Eroded, `FP`=Faulted pick, `FO`=Faulted out, `NL`=Not logged, `NR`=Not reached
- Surface paling sering muncul: Seabed (32), Heather Fm. Top (32), Utsira Fm. Top (31),
  HORDALAND GP. Top (30), SHETLAND GP. Top (29), NORDLAND GP. Top (28), Hod Fm. Top (28),
  Draupne Fm. Top (28), Hugin Fm. VOLVE Top (28) + Base (28), Ty Fm. Top (27), Ekofisk Fm. Top (27),
  Sleipner Fm. Top (22), Smith Bank Fm. Top (13)
- **Nilai untuk capstone:** ini sumber label geologi (formation tops) lintas sumur — bisa jadi basis
  lithology/stratigrafi label atau validasi lithology code WBS* di time.csv.

## Kesimpulan aksi

1. time.csv (239 kolom, 419.747 baris, 2009-06-27 → 2015-09-22) dan depth.csv (115 kolom, 16.670 baris data)
   F-9 A terbuka penuh, siap dipakai untuk ekstraksi fitur drilling event/stuck-pipe.
2. Zip kaggle F9A = duplikat file yang sudah ada; tidak perlu ekstrak ulang.
3. `ROP data .csv` (151 baris data, F-15) membawa kolom petrofisika PHIF/VSH/SW/KLOGH — kandidat label.
4. Catalog 4.035 baris = peta aset sumber (253 LAS, 442 DLIS, jalur dbfs marketplace).
5. `Well_picks_Volve_v1.dat` = 409 formation picks di 35 wellbore → sumber label geologi lintas well.
6. `VOLVE_INVENTORY.xlsx` = inventaris log per wellbore (25 sheet).
