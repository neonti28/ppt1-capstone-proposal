# V6-D1g — EDM DATABASE (Volve F.edm.zip + Well_technical_data txt)

**Riset pendahuluan: `verification-mandatory` + `scientific-critical-thinking` — verifikasi ulang 2026-10-11 dengan 2 tool independen (grep & python): angka keyword 947/3539/130 tereproduksi PERSIS dengan metode "jumlah baris mengandung keyword, case-insensitive"; sifat klaim (false positive simulasi/ID acak/base64, bukan tag event) tetap benar (konteks ulang: `kick_pad_od`, base64, ID acak). Metode = kunci angka, lihat §0.**

Task kanban: `t_44b03f90` [Pembaca 07]
Tanggal eksekusi: 2026-10-10 (WIB)
Status file: **sudah dibuka & dipindai penuh (211 MB XML, semua angka di bawah = hasil tool nyata)**

---

## 0. VERDICT CEPAT (baca ini dulu)

**EDM di sini BUKAN database event drilling (bukan NPT/bit-run/failure log).**
Isinya adalah export **Landmark Compass/WellPlan/EDT (Engineering Data Tool)** — yaitu
*desain & perhitungan well engineering*: wellpath (plan + actual), casing/hole section,
BHA design, pore pressure & frac gradient profile, torque-drag/hydraulics cases,
leak-off test config, material/grade catalog, cementing design.

Bukti eksplisit (bukan asumsi):
- Keyword "NPT" 130 hit → **semua false positive** (ID acak `NPTc5`, base64). Tidak ada tag/tabel NPT.
- Keyword "stuck" 947 hit → semua atribut simulasi `stp_calc_stuck_point`, `stp_md_when_stuck`
  (parameter input "stuck pipe" di torque-drag case, bukan catatan kejadian nyata).
- Keyword "kick" 3539 hit → semua `kick_pad_length` / `kick_pad_od` (parameter Bit/Kick pad bit).
- "non-productive" 0, "bit run" 0, "lost circulation" 0, "well control" 0, "drilling report" 0.
- `failed` 416 hit → **0 hit yang bukan base64** (dicek: `grep -o -i '.\{40\}failed.\{40\}'` → kosong).

**Metode angka keyword (WAJIB disebut saat mengutip):** 947 / 3539 / 130 = **jumlah BARIS yang mengandung keyword, case-insensitive** (`grep -c -i` / python splitlines `.lower()`) — tereproduksi persis oleh 2 tool independen pada verifikasi ulang 2026-10-11. Angka BUKAN invariant, tergantung metode (verifikasi 2026-10-11): baris case-sensitif = 945 / 1699 / 41 (grep); occurrence case-insensitive = 968 / 5103 / 3331; word-boundary case-sensitif NPT = 0. Catatan: A1 §8b-5 menyebut 947/3539/130 "tidak tereproduksi" — dengan metode baris case-insensitive di atas angka asli tereproduksi persis; rentang A1 berasal dari pemilihan metode berbeda (bukan karangan penulis asli, bukan juga keliru total). Sifat klaim TETAP benar: semua hit = atribut simulasi/bit/ID acak/base64, bukan tag event (verifikasi konteks + token analysis A1 G4).

Jadi: label kegagalan/NPT **tidak** ada di file ini. Sumber label tetap DDR (PDF/XML/HTML)
dan NPD DISKOS. Yang EDM berikan adalah **fitur well engineering + wellpath definitif**.

---

## 1. README (dibaca penuh, dicetak)

File: `Well_technical_data/EDT_EDM_read_me.txt` — 272 byte, CRLF.

```
Statoil 2018-04-11
EDT_EDM

The data in the EDT_EDM folder structure is the EDT software export using the software from Landmark.

EDT_EDM
 CasingSeat
 CasingWear
 Compass
 EDM.XML
 Site
 Site_TemplateSlot
 StressCheck
 Wellcat
 WellPlan
 WellWellbore
```

Isi penting: export dibuat **2018-04-11**, memakai software **Landmark EDT**. Daftar folder di
readme = struktur folder yang memang ada di disk (dicek: semuanya ada; `Site`, `Site_TemplateSlot`,
`StressCheck`, `Wellcat` juga ada, tidak diminta task ini tapi ikut tercatat).

---

## 2. Isi ZIP (list, TANPA extract penuh)

`EDM.XML/Volve F.edm.zip` — 77.698.104 byte (77,7 MB)

```
entries: 1
by ext: {'.xml': 1}
compressed MB 77.7 / uncompressed MB 211.3
  77697976 -> 211263929  Volve F.edm.xml
```

ZIP cuma berisi **1 file**: `Volve F.edm.xml` (211,3 MB).

**Catatan penting:** file hasil extract-nya SUDAH ADA di disk, tidak perlu extract:
`EDM.XML/Volve F.edm.xml` = 211.263.929 byte, identik dengan ukuran uncompressed di zip.
Jadi "extract 1-2 file kecil" tidak diperlukan — langsung pakai XML yang sudah ada.

---

## 3. Struktur XML (identifikasi)

Kepala file:
```xml
<?xml version="1.0" standalone="no"?>
<?DataServices DB_Major_Version=14;...;DB_Version=EDM 5000.14.0 (14.00.00.000);expandPoint=CD_SITE;?>
<export>
<TOPLEVEL>
  <TU_TEMP_DERATION_SCHED .../>   ... ribuan elemen datar ...
```
Format: **satu file XML datar (flat), 142 tag unik, tanpa hierarki dalam** (semua elemen anak
langsung `<TOPLEVEL>`). Export EDM 5000.14.0, dibuat aplikasi Landmark COMPASS / WELLPLAN 5000.1
/ StressCheck 5000.1.

### Tag teratas (dihitung penuh dengan grep -o, 142 tag)

| hit | tag | arti |
|---|---|---|
| 65.675 | TU_LOAD_PROFILE | load case structural (torque-drag/casing) |
| 43.491 | TU_CASE_ASSEMBLY_PARAMETER | parameter per case assembly |
| 39.084 | CD_PORE_PRESSURE | profil tekanan pori (per stasiun kedalaman) |
| 37.257 | CD_FRAC_GRADIENT | profil frac gradient |
| 22.500 | CD_REAL_TIME_CONFIG | konfigurasi real-time (masing-masing case) |
| 18.154 | WP_TDA_DRAGCHART | hasil hitung torque-drag chart |
| 15.109 | CD_DEFINITIVE_SURVEY_STATION | **stasiun survei definitif (plan/actual)** |
| 10.650 | CD_ASSEMBLY_COMP | komponen BHA (drill pipe, MWD, bit, stabilizer, jar, motor) |
| 4.953 | CD_SURVEY_STATION | stasiun survei program |
| 3.902 | CD_ASSEMBLY | string/assembly (casing, drill string) |
| 2.741 | CD_HOLE_SECT | hole section / casing seat |
| 2.620 | CD_CASE | case analisis |
| 719 | CD_ATTACHMENT + 719 CD_ATTACHMENT_JOURNAL | lampiran biner StressCheck (.spc dll) |
| 632 | CD_BHA_COMP_BIT | record bit dalam BHA design |
| 442 | CD_NBK_LEAK_OFF_TEST | parameter LOT per case |
| 162 | execsql | perintah SQL rebuild (`delete from CD_FLUID where well_id=...`) — artefak export |

Contoh atribut nyata (dari parser, bukan tebakan):
- `CD_ASSEMBLY`: `assembly_name="9 5/8\""`, `string_type="Casing"`, `md_assembly_base=8678.1`,
  `create_app_id="COMPASS"`, `create_user_id="ksva(KSVA@STATOIL.NET)"`, `create_date={ts '2010-07-08 10:38:10'}`
- `CD_ASSEMBLY_COMP`: `catalog_key_desc="Drill Pipe, 5,500 in, 21,90 ppf, S-135, FH VAM EIS"`,
  `grade="S-135"`, `joints="264"`, `makeup_torque=56261`, `min_yield_stress=134999`,
  MWD: `catalog_key_desc="MWD Tool POWERPULSE, 6,75 in"`, bit: `comp_type_code="PDC"`, `tfa=0.00488`
- `CD_HOLE_SECT`: `od_casing=30.0 / 20.0 / 13.375`, `catalog_key_desc="30 in, 309.7 ppf, X-52"`,
  `cof=0.25`, `md_shoe=482.6`
- `CD_SCENARIO`: `name="15/9-F-11 A NWest PIL DG3 rev0"`, `phase=PLAN/ACTUAL/PROTOTYPE`
- `CD_SITE`: `site_name="Volve F"`, `block_name="15/9"`, `geo_latitude=58.4416`, `geo_longitude=1.8875`
- `CD_PROJECT`: `project_name="SLEIPNER"`, `geo_zone_id="UTM-31N"`, `geo_datum_id="ED50"`
- `CD_NBK_LEAK_OFF_TEST`: `air_gap=180.118`, `sea_depth=298.556` (satuan feet/Statoil default)
- `execsql`: `delete from CD_FLUID where well_id='2DfUHhBj3x' and wellbore_id='3W9ZjV2yj0' and fluid_id='1WEoS'`

---

## 4. Cakupan well (dari XML, 21 well / 54 wellbore)

Project = SLEIPNER, site = Volve F, block 15/9 (Volve field). Semua subsea, water depth 298,556 ft.

Wells (21): 15/9-19, F-1, F-2, F-3, F-4, F-5, F-6, F-7, F-8, F-9, F-10, F-11, F-12, F-13,
F-14, F-15, + "Relief well location 1..5" (5 entri relief-well planning).

Wellbore contoh dengan `bh_md` terisi: F-1 C 13251,6 ft; F-15D 15190,6 ft; F-14 12123,0 ft;
F-5 12260,8 ft; F-12 11368,4 ft; F-4 11335,6 ft; F-1 11735,9 ft.
Rig name tercatat hanya di 15/9-19: **"Datum #2"**. sisanya `rig_name=None`.

### Sebaran phase (asumsi penting untuk pemakaian data)
```
CD_ASSEMBLY                     : None 2103 | PROTOTYPE 1582 | PLAN 207 | ACTUAL 10
CD_DEFINITIVE_SURVEY_HEADER     : PLAN 47 | PROTOTYPE 37 | ACTUAL 26
CD_SCENARIO                     : PROTOTYPE 45 | PLAN 39 | ACTUAL 26
```
Definitive survey header ACTUAL per well: 15/9-19 (5), F-15 (5), F-1 (4), F-11 (4),
F-9 (2), F-10, F-12, F-14, F-4, F-5, F-7 (masing-masing 1).
Artinya sebagian besar konten adalah **rencana/prototipe desain**, bukan data yang benar-benar
terjadi. Yang fase ACTUAL = wellpath definitif hasil survei (dipakai Compass "use_actual_data").

### CD_DEFINITIVE_SURVEY_STATION per wellbore (15.109 stasiun total)
Top: F-10 A (1715), F-13 (1473), F-2 (887), F-11 T2 (777), F-10 (678), F-11 B (639),
F-3 (517), F-8 (383), 19 SR (378), F-14 A (370), F-11 A (364), F-12 (330), 19 A (313),
19 BT2 (284), F-15D (268).

### CD_BHA_COMP_BIT (632 record bit di dalam desain BHA — BUKAN bit run log)
Per well: F-1 (229), F-11 (137), F-14 (67), F-10 (60), F-13 (53), F-12 (35), F-9 (18),
F-4 (10), F-5 (8), F-3 (6), F-6 (6), F-7 (2), F-15 (1).
Field terisi hanya sedikit: `bit_size` 4, `iadc_code` 3, `bit_class` 1, `bit_group` 1 —
mayoritas record bit hanya punya ID link (well/wellbore/assembly/assembly_comp). Lemah.

### CD_ATTACHMENT_JOURNAL (719 lampiran biner)
`mime_type="dws-app-data/stresscheck"`, `attachment_name="NoTemplate.spc"`, kompresi biner.
Isinya file proyek StressCheck/WPC — **bukan teks**, tidak dibuka (di luar scope, biner).

---

## 5. Folder Well_technical_data lain (task: catat mana yang kosong)

Semua diperiksa dengan `find <dir> -type f`:

| Folder | Isi | Keterangan |
|---|---|---|
| CasingSeat | 1 file: `left_intentionally_empty.txt` (0 byte) | **KOSONG (sengaja)** |
| CasingWear | 1 file: `left_intentionally_empty.txt` (0 byte) | **KOSONG (sengaja)** |
| Compass | 1 file: `left_intentionally_empty.txt` (0 byte) | **KOSONG (sengaja)** |
| WellPlan | 1 file: `left_intentionally_empty.txt` (0 byte) | **KOSONG (sengaja)** |
| WellWellbore | **175 file** | berisi data asli, lihat bawah |

Folder lain yang ada tapi tidak diminta (tercatat apa adanya): `Daily Drilling Report - PDF/XML/HTML
Version`, `Site`, `Site_TemplateSlot`, `StressCheck`, `Wellcat`.

### WellWellbore (175 file)
```
by ext: .pdf 67, .txt 4, sisanya file tanpa ekstensi (tabel stasiun survei, teks)
phase di nama file: ACTUAL 21 + ACTUAL.pdf 21 | PLAN 38 + PLAN.pdf 23 + PLAN.txt 1 | PROTOTYPE 45
NPD survey txt: 3 file (15/9-19 A, 15/9-19 BT2, 15/9-19 SR)
```
Isi:
- `*_Standard_Survey_NPD.txt` (3 file, 34-45 KB) — header Equinor, unit Equinor default,
  `WELL NAME: 15/9-19`, `Survey Date: 13.10.2005`, `Extraction Date: 11.01.2024`,
  `Datum Name: Byford Dolphin RT(25.00m)`, Bottom Hole MD 4131,00 m / TVD 3318,72 m.
- File **tanpa ekstensi** bernama `..._ACTUAL` / `..._PLAN` / `..._PROTOTYPE` (mis.
  `Volve F_F-1_F-1_F-1_ACTUAL`, 13.5 KB) — teks, header Statoil default, lalu tabel:
  `SURVEY LIST` / `MD  Inc  Azim  TVD  X-Offset  Y-Offset  UTM E/W  UTM N/S  DLS` (deg/30m).
  Contoh F-1 ACTUAL: `Survey Date: 16.01.2014`, `Extraction Date: 26.03.2018`,
  `Bottom Hole MD: 3632.00 m`, `Bottom Hole TVD: 3330.40 m`, `Water Depth: 91.00 m`,
  `KB-MSL: 54.90 m`, `Vertical Section Direction: 302.24 deg`, plus **Survey Program** list
  yang menyebut tool per interval: `26" GYRO SCIENTIFIC MODULAR`, `17 1/2" AUTOTRAK G3`,
  `8 1/2" AUTOTRAK G3` (ini berguna: nama tool BHA per interval kedalaman).
- `Standard Survey Report_..._PLAN.pdf` / `_ACTUAL.pdf` (67 PDF) — versi cetak survei.
- `Well Summary F-1.pdf`, `Well Summary F-10.pdf` — ringkasan per well.
- Beberapa file malah berekstensi `.txt` tapi isinya survei plan (mis. `F10 Rev 51 280409_PLAN.txt`).

Catatan: file-file ini **isinya sama dengan CD_DEFINITIVE_SURVEY_HEADER/STATION di XML**
(Compass export) — jadi WellWellbore = terjemahan text/PDF dari data survei yang juga ada
di XML. Bukan sumber label baru.

---

## 6. Bisa jadi LABEL? — Penilaian jujur

| Kandidat label | Ada di EDM? | Bukti |
|---|---|---|
| NPT / non-productive time | **TIDAK** | 0 hit "non-productive", tag NPT tidak ada |
| Kegagalan alat / stuck pipe / lost circulation | **TIDAK** | "stuck"=hanya atribut simulasi torque-drag; "lost circulation" 0 hit |
| Bit run record (bit A masuk → bit B keluar, ROP per run) | **TIDAK** | CD_BHA_COMP_BIT = komponen desain BHA, bukan run log; field `iadc_code` cuma 3 terisi |
| Kick / well control event | **TIDAK** | "kick" = kick pad bit; "well control" 0 hit |
| Leak-off test hasil (pressure value) | **SEBAGIAN** | CD_NBK_LEAK_OFF_TEST 442 record tapi field cuma `air_gap` + `sea_depth` per case — tekanan LOT-nya sendiri tidak ada di tag ini |
| Wellpath definitif (MD/Inc/Azim/TVD/DLS) | **YA** | 15.109 CD_DEFINITIVE_SURVEY_STATION + 26 header ACTUAL + 21 file `*_ACTUAL` text |
| Pore pressure & frac gradient profile | **YA** | 39.084 CD_PORE_PRESSURE + 37.257 CD_FRAC_GRADIENT (per wellbore/scenario) |
| BHA design & material (drill pipe spec, MWD, bit type, casing spec) | **YA** | 3.902 CD_ASSEMBLY, 10.650 CD_ASSEMBLY_COMP, 2.741 CD_HOLE_SECT, 21 material + 21 grade |
| Torque-drag / hydraulics perhitungan | **YA** | 18.154 WP_TDA_DRAGCHART + 953 WP_HYD_PARAMS/WP_TDA_PARAMS dll (output simulasi, bukan pengukuran lapangan) |
| Difficulty metrics (DDI, max DLS, tortuosity) | **YA** | atribut CD_SURVEY_HEADER & CD_DEFINITIVE_SURVEY_HEADER: `directional_difficulty_index`, `maximum_dls_value`, `tortuosity`, `average_dogleg` — 194 + 110 record |

**Kesimpulan:** EDM bukan sumber label kegagalan. Nilainya = **fitur well engineering** yang
bisa digabung ke pipeline (wellpath definitif, pore/frac pressure profile, BHA & casing spec,
DDI/tortuosity). Kalau butuh label, tetap ke DDR (NPT table per hari) dan NPD DISKOS
(`nested_reoccurring_problems` / wellbore re-entry). Perhatikan juga: mayoritas konten phase
= PLAN/PROTOTYPE, jadi harus difilter `phase=ACTUAL` supaya bukan data rencana yang dipakai
sebagai fakta.

---

## 7. Angka kunci (ringkas)

- `EDT_EDM_read_me.txt`: 272 byte; isi = daftar 10 folder sub-struktur + kredit "EDT software
  export using the software from Landmark", tanggal 2018-04-11.
- `Volve F.edm.zip`: 77.698.104 byte, **1 entry**, `Volve F.edm.xml` 211.263.929 byte.
- XML: 142 tag unik, 1 project (SLEIPNER), 1 site (Volve F), **21 well, 54 wellbore**,
  110 scenario, 110 definitive survey header (47 PLAN / 37 PROTOTYPE / 26 ACTUAL),
  15.109 definitive survey station, 3.902 assembly, 10.650 assembly comp, 632 bit comp,
  2.741 hole section, 39.084 pore pressure point, 37.257 frac gradient point,
  18.154 drag chart, 442 leak-off test case, 159 fluid, 21 material, 21 grade, 719 attachment.
- Keyword label (metode: baris case-insensitive, lihat §0): NPT 130 (false positive), stuck 947 (simulasi), kick 3539 (bit pad),
  non-productive 0, bit run 0, lost circulation 0, well control 0, drilling report 0.
- Folder kosong sengaja (`left_intentionally_empty.txt` 0 byte): **CasingSeat, CasingWear,
  Compass, WellPlan**.
- WellWellbore: 175 file = 67 PDF + 4 txt + 104 file teks tanpa ekstensi; 3 file NPD survey txt;
  21 `*_ACTUAL` text (wellpath definitif per wellbore), 38 PLAN, 45 PROTOTYPE.

## 8. Script pendukung (reproducible)

Semua hitungan di atas dihasilkan script di workspace task:
`zipinfo.py` (list zip), `xmlscan.py` (parse 142 tag + sample atribut),
`wells.py` (21 well/54 wellbore), `phases.py` (phase + station + bit per well).
Jalankan: `python3 <script>.py` (XML 211 MB diparse penuh dengan ElementTree iterparse,
selesai ~4 detik).
