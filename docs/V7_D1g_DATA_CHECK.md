# V7-D1g — Cek Ketersediaan Data untuk Solusi R&D (Domain: EDM)

Task: `t_f948943d` · Pembaca 07 · Master: V7-M1 (`t_0d02b12f`, spek di `docs/V7_M1_DELEGASI.md` §2.7)
Tanggal: 2026-10-11 · Status: SELESAI (4/4 spek dicek dengan bukti angka)

Sumber data (satu-satunya domain file yang dicek):
- `/mnt/d/Capstone 1/data/volve/external/dbx_volume/Well_technical_data/EDM.XML/Volve F.edm.xml` — 211.263.929 byte, 320.923 baris, flat XML `<export><TOPLEVEL>…`
- `/mnt/d/Capstone 1/data/volve/external/dbx_volume/Well_technical_data/EDT_EDM_read_me.txt` — 272 byte
- (zip asli: `Volve F.edm.zip` 77.698.104 byte — XML sudah terekstrak, dipakai yang XML)

Riset pendahuluan: verification-mandatory — klaim D0 "39.084 pore pressure / 37.257 frac" saya reproduksi sendiri dari tag census (persis 39.084 / 37.257), TAPI angka itu MENTAH tanpa filter; ketika filter `phase=ACTUAL` yang diminta M1 benar-benar diterapkan lewat join group, yang tersisa hanya **8 baris** — jadi angka D0 tidak boleh dipakai sebagai "data ACTUAL".
Riset pendahuluan: scientific-critical-thinking — klaim D0 "EDM BUKAN event DB" tidak saya ulangi, saya UJI ULANG dengan grep mandiri (5 keyword + pencarian tag rentang waktu + inspeksi konteks tiap hit); hasilnya **konfirmasi** dengan bukti sendiri, termasuk 3 false-positive yang harus dimentahkan (stuck/NPT/kick).

---

## 0. File dibuka + isi dicetak (acceptance a)

`EDT_EDM_read_me.txt` (cat, isi lengkap):

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

`Volve F.edm.xml` (head -c 3000, dipotong — 1 tag = 1 baris, atribut sebagai `name="value"`):

```
<?xml version="1.0" standalone="no"?>
<?DataServices DB_Major_Version=14;DB_Minor_Version=00;DB_Build_Version=000;DB_Version=EDM 5000.14.0 (14.00.00.000);expandPoint=CD_SITE;?>
<export>
<TOPLEVEL>
<TU_TEMP_DERATION_SCHED schedule_name="4145H MOD [SH-]" temp_deration_sched_id="SH494145HM      " />
<TU_TEMP_DERATION_POINT deration_temperature="212.0" correction_factor="0.959" temp_deration_sched_id="H9hEldg..." point_id="EVQmT" />
...
```

Tag census seluruh file (`grep -o '<[A-Za-z_…]' | sort | uniq -c`), 142 tag, yang relevan:

```
39084 <CD_PORE_PRESSURE        37257 <CD_FRAC_GRADIENT      15109 <CD_DEFINITIVE_SURVEY_STATION
 632 <CD_BHA_COMP_BIT          10650 <CD_ASSEMBLY_COMP       4953 <CD_SURVEY_STATION
 135 <CD_PORE_PRESSURE_GROUP    135 <CD_FRAC_GRADIENT_GROUP   194 <CD_SURVEY_HEADER
 110 <CD_DEFINITIVE_SURVEY_HEADER  3902 <CD_ASSEMBLY           54 <CD_WELLBORE   21 <CD_WELL
 159 <CD_FLUID                  719 <CD_ATTACHMENT_JOURNAL    162 <execsql
 (tidak ada tag yang namanya mengandung EVENT / NPT / INCIDENT)
```

Penting — atribut `phase` TIDAK ada di tag daun; hanya di tag GROUP/header:
`phase="ACTUAL"` 306 kemunculan, `phase="PLAN"` 1.592, `phase="PROTOTYPE"` 4.024, dan hanya di 12 tag (`CD_PORE_PRESSURE_GROUP`, `CD_FRAC_GRADIENT_GROUP`, `CD_SURVEY_HEADER`, `CD_DEFINITIVE_SURVEY_HEADER`, `CD_ASSEMBLY`, `CD_CASE`, `CD_DATUM`, `CD_FLUID`, `CD_HOLE_SECT_GROUP`, `CD_SCENARIO`, `CD_TEMP_GRADIENT_GROUP`, `CD_WELLBORE_FORMATION`).
→ Konsekuensi: **filter `phase=ACTUAL` wajib lewat join `leaf.<x>_group_id → group.phase`**, bukan filter baris daun. Semua angka ACTUAL di bawah ini dihitung lewat join itu.

Unit kedalaman: **FEET** (tidak ada atribut `uom`/`unit` di seluruh file — grep `uom="` = 0, `unit="` = 0). Bukti silang: EDM F-5 `tvd` max = 10.624,6 vs WITSML `witsml_parsed/F-5.csv` kolom `TVDE` max = 3.246,54 m → rasio **3,27** (rasio ft/m = 3,28084, selisih 0,3% = beda datum RT/RKB). Rumus konversi: m = ft × 0,3048.

---

## 1. Tabel utama (acceptance b)

| # | Solusi R&D | Data needed | Status | Bukti (kolom + baris + path) | Peluang proses |
|---|---|---|---|---|---|
| 1a | **S-A3 LF3 / S-C2** — fitur overbalance | Pore pressure per depth, `phase=ACTUAL` | **TIDAK ADA (untuk ACTUAL)** — 8 baris saja, semua titik datum seawater | Join `CD_PORE_PRESSURE.pore_pressure_group_id → CD_PORE_PRESSURE_GROUP.phase`: ACTUAL **8 baris** (dari 39.084 mentah), PLAN 5.080, PROTOTYPE 33.996. 25 group ACTUAL: 17 kosong, 8 group isi tepat 1 baris, semua `tvd="298.556430445"` (91 m, = seawater datum; `pore_pressure_emw="5.3639"`, `pore_pressure="133.38"`). 8 wellbore masing-masing 1 baris: F-1, F-5, F-9 A, F-12, F-14, F-15, F-15D, 15/9-F-11 B | — |
| 1b | **S-A3 LF3 / S-C2** — fitur overbalance (versi realistis) | Pore pressure + frac gradient (fase PLAN/PROTOTYPE) | **ADA SETELAH DIOLAH** | Kolom `tvd` (ft), `pore_pressure`, `pore_pressure_emw`, `is_permeable_zone`, `sequence_no`; `pore_pressure_emw` terisi **39.084/39.084**, `frac_gradient_emw` **37.257/37.257**. PLAN 5.080 + PROTOTYPE 33.996 baris PP; PLAN 4.851 + PROTOTYPE 32.398 FG. Proses: join group→phase, konversi ft→m, sort per `wellbore_id`+`tvd` | Per wellbore (PP, semua fase): F-10 A 8.874 · F-1 B 4.672 · F-1 C 4.570 · F-14 A 4.470 · F-13 3.920 · F-3 1.627 · F-5 1.019 · F-14 515 · sisanya ≤33. **F-8 = 0 baris** (tidak ada di daftar) |
| 2 | **S-F1 / S-D3** — identitas bit | `CD_BHA_COMP_BIT` selain `bit_size` | **TIDAK ADA (nyaris kosong)** — laporan apa adanya | 632 baris; pengisian field: `bit_size` **4/632**, `bit_size_pass_through` 4/632, `bit_size_pilot` 4/632, `iadc_code` **3/632** (semua value `2`), `bit_class` **1/632** (`NEW`), `bit_group` **1/632** (`PDC`); field lain hanya kunci join (`well_id`, `wellbore_id`, `assembly_id`, `assembly_comp_id` = 632/632). `serial` = **0 hit**, `footage`/`bit_run(s)` = **0 hit**, `dull` = 21 hit semuanya base64 noise (bukan IADC dull grade) | — |
| 2b | **S-F1 / S-D3** — identitas bit (jalur alternatif) | tipe/ukuran bit | **ADA SETELAH DIOLAH** | Join `CD_BHA_COMP_BIT.assembly_comp_id → CD_ASSEMBLY_COMP`: **632/632 match, semua `sect_type_code="BIT"`**. Row BIT di CD_ASSEMBLY_COMP = 638. Field terisi: `catalog_key_desc` 632/632 (contoh: `Tri-Cone Bit, 3x18, 0.746 in²`, `Polycrystalline Diamond Bit, 6x14, 1 x 15, 1.075 in²`), `comp_type_code` (PDC 545 / BIT 87), `od_body` 632 (ukuran, inci), `tfa` 621, `approximate_weight` 430, `percent_plugged` 35, `manufacturer` 15, `model` 10, `create_date` 92 | `CD_BHA_COMP_BIT → CD_ASSEMBLY_COMP → CD_ASSEMBLY` (`phase` + `md_assembly_base`/`tvd_assembly_base` + `create_date`) → **interval bit per kedalaman**. Kunci join `assembly_id`/`assembly_comp_id` sudah terbukti match penuh |
| 3 | **S-A3 LF2** — kurasi event (label kegagalan) | Tag event: waktu mulai–selesai, `phase=ACTUAL` | **TIDAK ADA** — konfirmasi D0 (uji ulang mandiri, lihat §4) | `non-productive`=0, `nonproductive`=0, `lost circulation`=0, `well control`=0, `incident`=0, `\bNPT\b`=0, `event`=1 (base64 blob), `start_date`/`end_date`/`begin_date`=0 tag | Event label harus datang dari domain lain: `data/volve/ddr.parquet` / `labels_curated_v2.csv` (domain Pembaca 08) |
| 4 | **S-B1/S-A2/S-E1** (rekonstruksi jalur MD→TVD) — wellpath ACTUAL F-2, F-3, F-6, F-8 | Survey baris per wellbore, `phase=ACTUAL` | **F-6: TIDAK ADA · F-2/F-3/F-8: ADA SETELAH DIOLAH (tapi fase PLAN/PROTOTYPE, bukan ACTUAL)** | Detail §5. F-6: 0 header + 0 station di kedua tabel survey. F-2: def 887 (PROTOTYPE 617/PLAN 270/**ACTUAL 0**) + survey 55 (PLAN). F-3: def 517 (PRO 247/PLAN 270/**ACTUAL 0**) + 34 (PLAN). F-8: def 383 (PLAN 131/PRO 252/**ACTUAL 0**) + 19 (PLAN) | Kolom `md`, `tvd`, `inclination`, `azimuth`, `dogleg_severity`, `offset_east/north` tersedia → geometri MD→TVD bisa diinterpolasi; TAPI label phase-nya bukan hasil survei aktual |

---

## 2. Cek 1 — Pore pressure & frac gradient (S-A3 LF3 / S-C2)

**2.1 Klaim D0 direproduksi (pre-filter):** `CD_PORE_PRESSURE` = **39.084**, `CD_FRAC_GRADIENT` = **37.257** — persis klaim D0. Tapi ini semua fase.

**2.2 Distribusi fase di tag GROUP** (n=135 masing-masing, dari `edm_check.py`):

```
PP_GROUP phase dist: Counter({'PROTOTYPE': 72, 'PLAN': 38, 'ACTUAL': 25})
FG_GROUP phase dist: Counter({'PROTOTYPE': 72, 'PLAN': 38, 'ACTUAL': 25})
```

**2.3 Hasil join leaf→group (angka yang diminta M1):**

```
PP rows by phase: {'PROTOTYPE': 33996, 'PLAN': 5080, 'ACTUAL': 8}
FG rows by phase: {'PROTOTYPE': 32398, 'PLAN': 4851, 'ACTUAL': 8}
ACTUAL PP groups=25 with>0 rows=8 empty=17   (rows per ACTUAL group: [1,1,1,1,1,1,1,1])
PP ACTUAL tvd range: min=298.6 max=298.6 n=8
```

**2.4 Isi 8 baris ACTUAL (grep asli, bukan ringkasan):**

```
<CD_PORE_PRESSURE wellbore_id="tRSGmE9FNr" ... pore_pressure_emw="5.3639479095271" pore_pressure="133.38092125931" sequence_no="100000" tvd="298.556430445" />
<CD_FRAC_GRADIENT wellbore_id="tRSGmE9FNr" ... frac_gradient_emw="9.0" frac_gradient_pressure="223.79566535344" sequence_no="100000" tvd="298.556430445" />
```

Semua 8 baris `tvd=298,556430445` ft = **91,0 m** — titik datum air laut (PP emw 5,36 = gradien air laut; 133,38 psi / (0,052 × 298,556) = 8,6 ppg konsisten hidrostatik air laut). Artinya: **EDM tidak punya profil tekanan pori "ACTUAL"**, hanya titik datum. Group ACTUAL berisi 1 baris = anchor, bukan kurva.

**2.5 Kolom & kedalaman:** kolom kedalaman = `tvd` (feet, lihat silang WITSML §0), kolom tekanan = `pore_pressure` (psi) + `pore_pressure_emw` (ppg) — keduanya terisi penuh (39.084/39.084 dan 37.257/37.257). `is_permeable_zone` = flag Y/N.

**2.6 Per wellbore (semua fase, `edm_check4.py`):**

```
F-10 A 8874 {PROTOTYPE 6779, PLAN 2095} | F-1 B 4672 | F-1 C 4570 | F-14 A 4470
F-13 3920 | 15/9-F-11 3792 | F-15D 2017 | 15/9-F-11 A 1896 | F-1 1648 | F-3 1627
F-5 1019 | F-14 515 | F-4 33 | F-9 15 | ... | F-2 1 (PLAN) | F-6 1 (PLAN)
(F-8 tidak muncul = 0 baris pore pressure)
```

**Kesimpulan:** status untuk overbalance = **ADA SETELAH DIOLAH**, dengan dua syarat yang harus dibawa ke Master: (i) sumbernya estimasi pra-lubang (PLAN/PROTOTYPE), bukan pengukuran — sah sebagai *fitur* pra-lubang, tidak sah sebagai *label* kebocoran/tekanan nyata (cek kausalitas: label yang ditentukan proses lain tidak bisa diprediksi); (ii) join + konversi ft→m wajib. Filtrasi `phase=ACTUAL` seperti diminta spek = mati total (8 baris datum).

---

## 3. Cek 2 — Bit record (S-F1 / S-D3)

M1 meminta: "kalau cuma `bit_size` 4 baris → laporkan apa adanya." **Tepat seperti itu:**

```
CD_BHA_COMP_BIT n=632 non-empty per field:
   well_id: 632/632   wellbore_id: 632/632   assembly_id: 632/632   assembly_comp_id: 632/632
   bit_size: 4/632    bit_size_pass_through: 4/632   bit_size_pilot: 4/632
   iadc_code: 3/632 (value: '2')   bit_class: 1/632 ('NEW')   bit_group: 1/632 ('PDC')
3 sample bit rows (kunci join saja):
  {"well_id":"2DfUHhBj3x","wellbore_id":"3W9ZjV2yj0","assembly_id":"0GmRW","assembly_comp_id":"cnpIr"}
```

Ketiadaan dibuktikan dengan grep asli terhadap seluruh 211 MB: `serial`=0, `footage`=0, `bit_run(s)`=0, `dull`=21 hit tapi semua di dalam blob base64 (contoh: `...cSHhaa5h0x8eGYm5J8bcFXPYL...` — huruf `DulL` kebetulan), **bukan** IADC dull grade.

**Jalur alternatif yang berfungsi (join teruji):** `CD_BHA_COMP_BIT → CD_ASSEMBLY_COMP` match **632/632, semuanya `sect_type_code="BIT"`**:

```
non-empty field counts on bit-linked comp rows (n=632):
   catalog_key_desc: 632   od_body: 632   comp_type_code: 632   tfa: 621
   approximate_weight: 430   percent_plugged: 35   manufacturer: 15   model: 10   create_date: 92
comp_type_code dist: {'PDC': 545, 'BIT': 87}
desc samples: ['Tri-Cone Bit, 3x18, 0.746 in&#xB2;', 'Polycrystalline Diamond Bit, 6x14, 1 x 15, 1.075 in&#xB2;', ...]
```

Status: **tipe & ukuran bit = ADA SETELAH DIOLAH (join 1 langkah, kunci terbukti 632/632)**; **serial / dull grade / footage-per-run = TIDAK ADA** (bukti grep di atas). `percent_plugged` (35 baris) adalah satu-satunya sinyal keausan, bukan dull grade IADC.

---

## 4. Cek 3 — Event/NPT (LF2 S-A3): UJI ULANG klaim D0

Saya tidak mengulang D0 — saya jalankan grep sendiri (`edm_check_out.txt`, output §mentah):

| keyword | hasil (grep asli) | makna sebenarnya (konteks dicetak) |
|---|---|---|
| `non-productive` | **0** | — |
| `nonproductive` | **0** | — |
| `lost circulation` / `well control` / `incident` | **0 / 0 / 0** | — |
| `\bNPT\b` (word boundary) | **0** | 130 baris mengandung `npt` case-insensitive = substring acak di ID: `bLnPT`, `NPTc5`, `KnPTJ` — bukan akronim |
| `stuck` (947 baris) | attribute | SEMUANYA `stp_calc_stuck_point="0"` di tag torque-drag/WP_TDA — parameter simulasi, bukan kejadian nyata |
| `kick` (3.539) | attribute | `kick_pad_length`/`kick_pad_od` (steering tool) + "kick-off int." (azimuth) — bukan well control kick |
| `trip_in`/`trip_out` (5.945/5.907) | attribute | `trip_in_meas_weight`/`trip_out_meas_weight` di `WP_TDA_ACTLOAD` (223), `WP_TDA_PARAMS` (953), `WP_TDA_DISCRETE_PARAMS` (17) — load case simulasi, bukan catatan trip |
| `spud` (6) / `event` (1) | noise | semua di dalam blob base64 `BINARY_DATA` |
| `start_date` / `end_date` / `begin_date` / `event_` | **0 tag** | tidak ada satu pun tag dengan rentang waktu |

Tag yang punya timestamp hanya `CD_ATTACHMENT_JOURNAL` (create/update file lampiran, 719), `CD_SURVEY_STATION.survey_date`, `CD_ASSEMBLY.create_date` — semuanya metadata perencanaan/manajemen file, bukan kejadian operasional (mulai–selesai).

**VERDICT: konfirmasi D0 "EDM bukan event DB" — dengan bukti grep milik sendiri.** Tidak ada tag event fase ACTUAL dengan waktu mulai–selesai. → S-A3 LF2 (label event/NPT) **TIDAK ADA di domain EDM**; sumber label kegagalan harus dari DDR/label curated (domain Pembaca 08).

---

## 5. Cek 4 — Wellpath ACTUAL F-2, F-3, F-6, F-8 (`edm_check3.py`)

```
target wellbores: {'h8MNxid5Ma': 'F-8', 'xzpZei21x9': 'F-3', '9mSdrT6MSY': 'F-2', 'us67jMDQQ4': 'F-6'}

F-2 (9mSdrT6MSY): def_stations=887 {'PROTOTYPE': 617, 'PLAN': 270, 'ACTUAL': 0} | survey_stations=55 {'PLAN': 55}
   def: md -180..12700  tvd -180..10762      surv: md 299..12700 tvd 299..10761
F-3 (xzpZei21x9): def_stations=517 {'PROTOTYPE': 247, 'PLAN': 270, 'ACTUAL': 0} | survey_stations=34 {'PLAN': 34}
   def: md -180..12979  tvd -180..10102
F-8 (h8MNxid5Ma): def_stations=383 {'PLAN': 131, 'PROTOTYPE': 252, 'ACTUAL': 0} | survey_stations=19 {'PLAN': 19}
   def: md 299..12584   tvd 299..10560
F-6 (us67jMDQQ4): def_stations=0 {} | survey_stations=0 {}
   def_hdr=[]   surv_hdr=[]        ← 0 header, 0 station di kedua tabel survey
```

Bukti ketiadaan F-6: wellbore `us67jMDQQ4` **ada** di `CD_WELLBORE` (dan `F-6` ada di `CD_WELL`), tapi tidak punya satu pun `CD_DEFINITIVE_SURVEY_HEADER`/`CD_SURVEY_HEADER` → tidak ada baris survey sama sekali.

Header F-2/F-3/F-8 (dicetak): semua `phase` ∈ {PLAN, PROTOTYPE}; nama survey berupa dokumen rencana (`F-2 rev#1 STGAL 141015`, `F8 Volve Sør Prod DRAFT NewRigCoords 220607`, `F-3 _IOR_SE_entry(Top Hugin) rev2`) — konsisten dengan rencana, bukan survei as-built. Sebagai pembanding, wellbore LAIN punya fase ACTUAL (F-10 479, 19 SR 378, 15/9-F-11 T2 650) — jadi ketiadaan ACTUAL di F-2/F-3/F-8 itu nyata, bukan artefak skema.

**Status:** F-6 = **TIDAK ADA**; F-2/F-3/F-8 = **ADA SETELAH DIOLAH** untuk geometri MD→TVD (kolom `md`,`tvd`,`inclination`,`azimuth`,`dogleg_severity`), **bukan** jalur aktual. ⚠ Semantik `phase="PROTOTYPE"` pada wellpath **tidak terdokumentasi di file export** (nama header cuma "Wellpath") — status maknanya **UNKNOWN**, jangan diasumsikan as-built tanpa dokumen EDM.

---

## 6. Peluang PROSES / relasi antar-file (item 3 — untuk Master)

1. **PP/FG ↔ survey (join depth):** `CD_PORE_PRESSURE.tvd` dan `CD_DEFINITIVE_SURVEY_STATION.tvd/md` sama-sama feet dan sama-sama punya `wellbore_id` → join `(wellbore_id, depth)` setelah konversi ft→m. Langkah: join group→phase, filter fase, konversi, sort, interpolasi EMW ke grid depth. Estimasi baris hasil: 5.080 (PLAN) + 33.996 (PROTOTYPE) baris PP + 4.851 + 32.398 FG.
2. **Rantai bit 3 file:** `CD_BHA_COMP_BIT` (632) → `CD_ASSEMBLY_COMP` (join `assembly_comp_id`, **632/632 match**) → `CD_ASSEMBLY` (`phase`, `md_assembly_base`, `tvd_assembly_base`, `create_date`; 1.799/3.902 baris CD_ASSEMBLY membawa atribut `phase`). Hasil: interval bit + tipe/ukuran per kedalaman. Kunci join sudah diverifikasi programatik.
3. **Mud weight untuk overbalance (S-A3 LF3):** `CD_FLUID` 159 baris, kolom `density` (sg) terisi 140, range 0,915–15,856 (max kemungkinan semen → wajib filter `is_cement`), fase PROTOTYPE 126 / tanpa fase 33. Ditambah atribut `mud_density=` (948 hit baris, ada di tag case WP_*) dan `mud_weight=` (65 hit). Rumus: `overbalance(ppg) = density_sg × 8,345 − pore_pressure_emw` pada depth yang sama.
4. **Relasi lintas domain:** karena event/NPT = 0 di EDM (§4), label LF2 **wajib** dari `data/volve/ddr.parquet` / `labels_curated_v2.csv` (1.412 vs 884 event — sudah didelegasikan ke Pembaca 08). EDM hanya bisa memberi konteks depth/fase untuk memperkaya record dari DDR (join kandidat: `wellbore_id`/nama well + timestamp `create_date` vs DDR date).
5. **Peringatan satuan:** EDM = feet, WITSML/`witsml_parsed/*.csv` = meter (`TVDE` 3.246,54 m vs EDM 10.624,6 ft untuk F-5). Semua join lintas file wajib konversi ×0,3048 — kalau tidak, error faktor 3,27.

---

## 7. Belum diverifikasi (aturan 3)

- **Semantik `phase`** (ACTUAL/PLAN/PROTOTYPE): makna resmi dari EDM 5000.14 tidak ada di file export; interpretasi "ACTUAL = as-built" adalah inferensi, bukan fakta terdokumentasi.
- **Unit feet** disimpulkan dari rasio silang WITSML (3,27 vs 3,2808) — di XML tidak ada atribut `uom` (grep = 0), jadi bukan konfirmasi eksplisit dari file.
- **Owner `mud_density=` (948 hit)** dipetakan per-baris via tag awal baris (`WP_CASE_CENTRALIZER_SCHD` 948) — belum diverifikasi per elemen apakah atributnya memang milik tag itu atau baris multi-tag.
- **`CD_FLUID` density max 15,856** belum dicek apakah baris semen (`is_cement=Y`).
- Tabel `execsql` (162 baris) dan `LINKTABLE` tidak diekstrak — di luar spek, tapi bisa berisi definisi relasi SQL.
- File "Well_technical_data txt" yang disebut body task **tidak ditemukan** di domain (hanya `EDT_EDM_read_me.txt`, sudah dicetak §0) — `find` di `Well_technical_data` hanya menemukan `.txt` "left_intentionally_empty" pada folder lain.
- **sequ MCP (SOUL: wajib) terblokir sesi ini:** tool `mcp__sequentialthinking__sequentialthinking` dipanggil 9×; hanya payload 4 karakter yang lolos, sisanya gagal di level pembungkus dengan `tool_call 'calls' is not valid JSON: Expecting ',' delimiter` pada posisi akhir string (payload JSON saya valid; kegagalan di serialization wrapper, bukan di argumen). 1 panggilan sukses tercatat (`thoughtHistoryLength: 1`), 8 gagal. Analisis berlapis tetap dijalankan manual per tahap OBSERVED→HYPOTHESIS→TEST→RESULT.

---

## 8. Artefak bukti (raw output)

Semua di workspace task `t_f948943d` (`/home/neonti/.hermes/kanban/boards/capstone-v7-solve/workspaces/t_f948943d/`):

- `edm_check.py` + `edm_check_out.txt` — tag census, join phase, bit join, survey per wellbore
- `edm_check2.py` + `edm_check2_out.txt` — field fill `CD_BHA_COMP_BIT`, nama group per fase, daftar well, F-6
- `edm_check3.py` + `edm_check3_out.txt` — detail survey F-2/F-3/F-6/F-8 + header
- `edm_check4.py` + `edm_check4_out.txt` — PP per wellbore, group ACTUAL kosong, `CD_FLUID`, tag `mud_density`
- `unit_xcheck.py` + `unit_xcheck_out.txt` — silang satuan EDM vs WITSML F-5

Acceptance: (a) ✅ 2 file dibuka + isi dicetak (§0); (b) ✅ 4 spek + 5 baris solusi R&D diberi status + bukti angka (§1); (c) ✅ 5 peluang proses/relasi antar-file dilaporkan (§6).
