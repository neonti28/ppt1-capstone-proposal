# V7-D1b — CEK KETERSEDIAAN DATA: DOMAIN bhaRun (BHARUN)

**Task:** `t_3e886804` [Pembaca 02] · Board: capstone-v7-solve · Tanggal: 2026-10-11 (WIB)
**Spesifikasi:** `docs/V7_M1_DELEGASI.md` §2.2 (dari Master V7-M1 `t_0d02b12f`)
**Domain:** 161 file `bhaRun/*.xml` WITSML 1.4.1.1 di `data/volve/witsml_raw/`

> **Riset pendahuluan: `verification-mandatory`** — (a) 1 file dibuka dengan `cat` dan isinya dicetak mentah sebelum parse (bukti §1); (b) SEMUA angka dihitung dua kali dengan jalur berbeda: parser Python `xml.etree` vs `rg` mentah — keduanya cocok 161/114/11/161 (§1, §2); (c) klaim ketiadaan (F-10) dibuktikan `rg` + daftar direktori, bukan asumsi; (d) angka D0 (`docs/V6_D1b_BHARUN.md`) dikutip lalu DIVERIFIKASI ULANG sendiri — seluruh metrik cocok (§6).
> **Riset pendahuluan: `scientific-critical-thinking`** — join "interval bhaRun ↔ 8 CSV parser lama" diuji dengan tes pembeda 2 hipotesis: (H1) join by nameWellbore+rentang waktu layak, (H2) sumber/folder beda sehingga rentang waktu tidak pernah bertemu. Hasil: H1 = 0 interval bertemu pada semua 8 CSV (nama persis), H2 terdukung bukti folder+rentang waktu (§4) — H1 TIDAK ditafsirkan sebagai "data rusak", melainkan sebagai "join kunci salah". Peringatan sirkularitas: klaim "data ada" di spesifikasi tidak dipakai sebagai bukti; semua dik hitung ulang.

---

## 1. BUKTI FILE DIBUKA (acceptance a)

Perintah: `cat "data/volve/witsml_raw/Norway-Statoil-NO 15_$47$_9-F-1 C/1/bhaRun/1.xml"` (1.060 byte).

```xml
<?xml version="1.0" encoding="UTF-8"?><bhaRuns xmlns="http://www.witsml.org/schemas/1series" version="1.4.1.1"><bhaRun uidWell="1bf1cc58-83af-4e13-9696-4fae2f9294ae" uidWellbore="c1a535e7-2f7e-4b2e-bcdc-8efd3df26de7" uid="23RGUI47"><nameWell>NO 15/9-F-1 C</nameWell><nameWellbore>NO 15/9-F-1 B</nameWellbore><name>15/9-F-1 B-22</name><tubular uidRef="23RGUI47">15/9-F-1 B_23RGUI47</tubular><dTimStart>2013-09-23T07:59:00.000Z</dTimStart><dTimStop>2013-09-23T09:10:00.000Z</dTimStop><numStringRun>22</numStringRun><commonData><sourceName>INTEQ</sourceName>...</commonData></bhaRun></bhaRuns>
```

Struktur: 1 record `bhaRun` per file. **Nama folder ≠ `nameWellbore`** (folder `…-F-1 C` berisi `nameWellbore=NO 15/9-F-1 B`) — jebakan D0 §2.5 terkonfirmasi di file pertama yang dibuka.

Parse 161 file: **161 record, 0 error XML**. Elemen yang ada (30 tag):
`nameWell, nameWellbore, name, tubular, dTimStart, dTimStop, numBitRun, numStringRun, dTimStartDrilling, dTimStopDrilling, mdHoleStart, mdHoleStop, eTimOpBit, wtMud, wtAboveJar, wtBelowJar, cTimCirc, objectiveBha, comments, drillingParams, commonData(sourceName, dTimCreation, dTimLastChange, itemState, priv_*),` + `cTimCirc`.

Hitungan non-null (dari 161 record; dikonfirmasi ulang dengan `rg`):

| Elemen | non-null | Keterangan |
|---|---|---|
| `dTimStart` | 161 (100%) | anchor waktu utama |
| `dTimStop` | 114 (70,8%) | 47 run tanpa tutup |
| `numStringRun` | 161 (100%) | 31 nilai berbeda (1–31) |
| `numBitRun` | **11 (6,8%)** | lihat §2 |
| `dTimStartDrilling` | 15 | |
| `dTimStopDrilling` | 10 | |
| **drilling window lengkap** (pasangan start+stop drilling) | **9** | klaim D0 "9 drilling window" KONFIRMASI |
| `mdHoleStart`/`mdHoleStop` | 19 / 19 (keduanya terisi pada 19 record yang sama) | jembatan waktu→kedalaman |
| `eTimOpBit`, `wtAboveJar`, `wtBelowJar` | 19 / 19 / 19 | |
| `comments` | 56 | teks bebas |
| `tubular` (uidRef) | 161 | join ke domain TUBULAR (D1a) |
| `objectiveBha`, `wtMud`, `cTimCirc` | 1 / 1 / 1 | hampir kosong |

Distribusi `nameWellbore` (14 wellbore, dihitung 2×: Python & `rg` identik):

```
26 NO 15/9-F-11 B   26 NO 15/9-F-1 C   17 NO 15/9-F-1 B   16 NO 15/9-F-15 D
14 NO 15/9-F-15 C   12 NO 15/9-F-11 T2  11 NO 15/9-F-5     11 NO 15/9-F-1
10 NO 15/9-F-12      7 NO 15/9-F-14      4 NO 15/9-F-4      3 NO 15/9-F-1 A
 2 NO 15/9-F-9 A     2 NO 15/9-F-11 A
```

`nameWell` (8 well): F-1 C 57, F-11 40, F-15 30, F-5 11, F-12 10, F-14 7, F-4 4, F-9 2.

Lokasi: **14 direktori bhaRun, SEMUA di folder `Norway-Statoil-NO …`** (F-1 C×4, F-11×3, F-12, F-14, F-15×2, F-4, F-5, F-9). Ada salinan identik (`md5` cocok) di `data/volve/external/dbx_volume/WITSML Realtime drilling data/` — 161 file lagi, BUKAN data baru.

---

## 2. TABEL UTAMA: solusi | data needed | status | bukti | peluang proses (acceptance b)

| Solusi R&D | Data needed dari domain bhaRun | Status | Bukti (kolom + angka + path) | Peluang proses |
|---|---|---|---|---|
| **S-B1 / S-A2** (fold wellbore baru F-10, F-4, F-12, F-15) | anchor waktu run untuk F-10 | **TIDAK ADA** | `rg "F-10" --glob "**/bhaRun/*.xml"` = **0 hit**; 14 direktori bhaRun (daftar §1) tidak ada `…-F-10`; `nameWell` distinct = 8 well, tanpa F-10 | F-10 hanya bisa di-anchor dari log XML-nya sendiri (domain Pembaca 05), bukan dari bhaRun |
| S-B1 / S-A2 | anchor waktu run untuk F-4 | **ADA SEBAGIAN (start-only)** | `nameWellbore=NO 15/9-F-4`: **4 run**, `dTimStart` 4/4 non-null, `dTimStop` **0/4**; start 2016-09-30T10:07Z … 2016-10-06T01:07Z; file `witsml_raw/Norway-Statoil-NO 15_$47$_9-F-4/1/bhaRun/*.xml` | 4 titik awal = 4 kandidat batas trip; tanpa stop, batas akhir run harus diturunkan dari gap waktu log (domain 05) |
| S-B1 / S-A2 | anchor waktu run untuk F-12 | **ADA SEBAGIAN (start-only)** | `NO 15/9-F-12`: **10 run**, start 10/10, stop **0/10**; start 2016-08-12T04:40Z … 2016-08-26T02:40Z; `…/Norway-Statoil-NO 15_$47$_9-F-12/1/bhaRun/` | sama dengan F-4: pakai start + gap-analisis |
| S-B1 / S-A2 | anchor waktu run untuk F-15 | **ADA LENGKAP (tapi wellbore sidetrack)** | `NO 15/9-F-15 C` 14 run + `NO 15/9-F-15 D` 16 run = **30 run**, start 30/30, stop 30/30 → **29 interval valid** (1 durasi negatif: F-15 C-15, stop 2013-11-07 < start 2013-11-08); span valid 2013-08-28 … 2014-11-11; `…/Norway-Statoil-NO 15_$47$_9-F-15/{1,2}/bhaRun/` | **Join hati-hati**: di bhaRun TIDAK ADA wellbore bernama polos `15/9-F-15` / `F-15S` / `F-15A` / `F-15B` — hanya C dan D. Fold baru harus didefinisikan per wellbore C/D, bukan "F-15" umum |
| S-B1 / S-A2 (konteks) | folder target parse vs folder bhaRun | **TIDAK COCOK PER FOLDER** | V7-R1 §3.2 menarget `Norway-StatoilHydro-…-F-10`, `…-F-4`, `Norway-Statoil-15_9-F-12`, `Norway-StatoilHydro-…-F-15`; keempatnya **`bhaRun_xml=0`** (dihitung `glob **/bhaRun/*.xml`: Hydro F-4=0, Statoil F-12=0, Hydro F-15=0, Hydro F-10=0). bhaRun hanya ada di `Norway-Statoil-NO …` | **Wajib join lewat field XML (`nameWellbore`+waktu), bukan folder** — konfirmasi langsung jebakan D0 §2.5 |
| **S-F1** (potong USROP per bit-run → label onset keausan) | `numBitRun` sebagai pemotong interval | **ADA TAPI TIDAK TERPAKAI untuk USROP** | `numBitRun` non-null **11/161 record** (`rg "<numBitRun>"` = 11 file; Python 11): integer valid **9** (`1`×4, `2`×2, `3`×2, `4`×1), non-integer **2** (`"3 RR 1"`, `"4RR1"` = re-entry); **durasi negatif di 11 record ini = 0** (semua 11 punya start+stop valid). Sebaran wellbore: F-1 C (4), F-1 (4), F-11 T2 (2), F-15 D (1). List 11 baris: `F-1 C/2/{13,14,16,24}.xml`, `F-1 C/4/{2,3,4,9}.xml`, `F-11/1/{1,4}.xml`, `F-15/2/5.xml` | **Proses agar jadi pemotong:** (1) parse string → regex `^(\d+)` + flag RR (jangan `int()` langsung); (2) USROP butuh DEPTH, bukan waktu → sambung lewat `mdHoleStart/Stop` yang ada di **9 dari 11** record numBitRun; (3) TAPI wellbore USROP (`data/USROP_labeled.csv`, kolom `well`): F-9 A, F-7, F-14, F-15, F-15S, F-5, F-9 — **hanya F-15 D (1 run) yang nyaris cocok, sisanya 0 record numBitRun** → lihat baris S-F1 kedua di bawah |
| **S-F1** (kelanjutan) | kecocokan anchor bhaRun ↔ `USROP_labeled.csv` | **TIDAK ADA (praktis)** | `USROP_labeled.csv` (198.928 baris; kolom: `Measured Depth m, WOB, SPP, torque, ROP, RPM, flow, mud density, diameter, hookload, TVD, gamma, well, label, MSE, D_exp, ROC_coef`) **TIDAK punya kolom waktu** → potong-by-`dTimStart/Stop` mustahil tanpa jembatan time↔depth. Jembatan `mdHoleStart/Stop` di wellbore USROP: **F-14 = 0 record, F-9 A = 0 record, F-5 = 3 record tapi `3792→3792` (span nol)**; F-7/F-15/F-15S/F-9 = 0 record bhaRun sama sekali | Satu-satunya jalur sisa: F-15 D (`numBitRun=1`, `md 1380→2618`, 1 interval valid) **jika** kolom `well` USROP `USROP_A 3 N-SH-F-15d.csv` = F-15 D (belum diverifikasi — domain Pembaca 08) |
| **S-B2** (unit jendela → per-stand: batas stand/trip) | `dTimStart/Stop` → interval | **ADA SETELAH DIOLAH** | 161 start / 114 stop → **114 pasangan, 108 valid (≥0), 6 durasi negatif** (detail §3); per wellbore valid: F-11 B 17, F-1 B 17, F-15 D 16, F-1 C 15, F-15 C 13, F-11 T2 12, F-1 10, F-11 A 2, F-14 2, F-5 3, F-1 A 1; **F-4, F-12, F-9 A = 0 interval valid** (stop kosong) | Proses: filter `stop≥start` (buang 6), lalu **klasifikasi batas**: selisih run berikutnya >N jam = trip/stand change; `dTimStartDrilling/StopDrilling` (9 pasangan lengkap) = jendela ON-BOTTOM yang lebih tajam dari dTimStart/Stop |
| **S-B2** (ujian join) | tumpang-tindih interval dgn **8 CSV parser lama** (join `nameWellbore` + rentang waktu) | **0 dari 8 CSV punya interval yang bertemu** | Detail §4: join nama persis → F-14 (2 interval valid) vs CSV `F-14.csv` [2007-11-04 … 2015-09-22] → **0 tumpang-tindih** (interval bhaRun F-14 = 2016-07/08); F-5 (3 interval) vs `F-5.csv`/**`VAR_F-5_alt.csv`** (maks 2015-09-22) → **0** (interval 2016-08/09); F-9 A (0 interval, 2 start 2016-09-29) vs `F-9_A.csv` → **0**; F-15A, F-15_S, F-7, F-9 → **0 run bhaRun bernama sama** | **Kesimpulan: anchor bhaRun TIDAK BISA dipakai langsung untuk memotong CSV parser lama.** Kandidat per-well (bukan per-wellbore): bhaRun `F-15 C/D` (29 interval valid) vs rentang `F-15A.csv`/`F-15_S.csv` → **28 interval, 9.922,9 jam** berada DI DALAM rentang CSV — tapi ini nama wellbore berbeda (sidetrack C/D vs Main/F-15S), status = **kandidat menunggu verifikasi Pembaca 05** apakah CSV memang berisi data C/D |
| **S-E2** (angka per fold — konteks) | jumlah run/wellbore untuk fold baru | ADA LANGSUNG | 14 wellbore, 161 run; 111 dari 161 run berada di wellbore yang **tidak punya CSV parser lama sama sekali** (F-1, F-1 A, F-1 B, F-1 C, F-11 A/B/T2, F-12, F-4 = 11+3+17+26+2+26+12+10+4 = 111) | wellbore kaya-run ini baru terpakai bila log-nya diparse (domain 05) |

---

## 3. `numBitRun` + durasi negatif (spesifikasi soal 2)

**11 record `numBitRun` (seluruh listing):**

| # | wellbore | run | numBitRun | dTimStart → dTimStop | file |
|---|---|---|---|---|---|
| 1 | F-1 C | 15/9-F-1 C - 1 | `1` | 2014-02-19 → 2014-02-27 | `…-F-1 C/2/bhaRun/16.xml` |
| 2 | F-1 C | - 2 | `2` | 2014-03-02 → 2014-03-05 | `…-F-1 C/2/bhaRun/24.xml` |
| 3 | F-1 C | - 3 | `3` | 2014-03-09 → 2014-03-11 | `…-F-1 C/2/bhaRun/13.xml` |
| 4 | F-1 C | - 3 RR 1 | **`3 RR 1`** | 2014-03-11 → 2014-03-15 | `…-F-1 C/2/bhaRun/14.xml` |
| 5 | F-1 | - 1 | `1` | 2013-07-21 → 2013-07-27 | `…-F-1 C/4/bhaRun/3.xml` |
| 6 | F-1 | - 2 | `2` | 2013-07-31 → 2013-08-01 | `…-F-1 C/4/bhaRun/2.xml` |
| 7 | F-1 | - 3 | `3` | 2013-07-31 → 2013-08-17 | `…-F-1 C/4/bhaRun/4.xml` |
| 8 | F-1 | - 1 | `1` | 2013-07-31 → 2013-07-31 | `…-F-1 C/4/bhaRun/9.xml` |
| 9 | F-11 T2 | - 4 | `4` | 2013-03-21 → 2013-03-25 | `…-F-11/1/bhaRun/1.xml` |
| 10 | F-11 T2 | - 4RR1 | **`4RR1`** | 2013-03-27 → 2013-05-07 | `…-F-11/1/bhaRun/4.xml` |
| 11 | F-15 D | - 1 | `1` | 2013-11-09 → 2013-11-17 | `…-F-15/2/bhaRun/5.xml` |

- Integer valid: **9** · non-integer: **2** (`"3 RR 1"`, `"4RR1"`)
- **Durasi negatif di record numBitRun: 0** (semua 11 punya `dTimStart`+`dTimStop` dan stop≥start)
- Durasi negatif TOTAL: **6 dari 114 pasangan** (bukan di record numBitRun):

| delta | wellbore | start → stop | file |
|---|---|---|---|
| −26.271 s | F-1 C | 2014-03-02T00:00Z → 2014-03-01T16:42Z | `…-F-1 C/2/bhaRun/20.xml` |
| −42.991 s | F-1 C | 2014-03-15T20:30Z → 2014-03-15T08:33Z | `…-F-1 C/2/bhaRun/4.xml` |
| −244.699 s | F-1 A | 2013-08-24T23:00Z → 2013-08-22T03:01Z | `…-F-1 C/3/bhaRun/2.xml` |
| −629 s | F-1 A | 2013-08-26T21:00Z → 2013-08-26T20:49Z | `…-F-1 C/3/bhaRun/3.xml` |
| −944 s | F-1 | 2014-01-21T08:31Z → 2014-01-21T08:15Z | `…-F-1 C/4/bhaRun/7.xml` |
| −123.188 s | F-15 C | 2013-11-08T23:15Z → 2013-11-07T13:01Z | `…-F-15/1/bhaRun/1.xml` |

**Proses agar jadi pemotong interval bit-run (S-F1):** (a) `numBitRun` parse sebagai STRING → regex `^(\d+)` untuk nomor + flag `RR` untuk re-entry (2/11 non-integer); (b) filter 6 durasi negatif (di luar record ini); (c) sambung ke depth lewat `mdHoleStart/Stop` (9 dari 11 record numBitRun punya md: F-1 C 4, F-1 3, F-11 T2 1, F-15 D 1) karena USROP depth-based; (d) **prasyarat yang gugur**: wellbore USROP hampir semuanya tidak punya record numBitRun → pemotong hanya berlaku parsial (lihat baris S-F1 di §2).

---

## 4. UJI JOIN ke 8 CSV parser lama (spesifikasi soal 3)

**8 CSV + sumber folder (dari `*.qc.json`, dibaca langsung):**

| CSV | `name_wellbore` (qc) | folder sumber | baris timestamp | rentang timestamp (scan penuh, semua baris) |
|---|---|---|---|---|
| F-14.csv | 15/9-F-14 - Main Wellbore | Norway-Statoil**Hydro**-…-F-14 | 1.648.026 | 2007-11-04 … 2015-09-22 |
| F-15A.csv | 15/9-F-15 - Main Wellbore | Norway-Statoil**Hydro**-…-F-15 | 778.162 | 2008-12-08 … 2015-09-22 |
| F-15_S.csv | 15/9-F-15S - Main Wellbore | Norway-Statoil**Hydro**-…-F-15S | 1.883.062 | 2008-09-08 … 2015-09-22 |
| F-5.csv | 15/9-F-5 - Main Wellbore | Norway-Statoil**Hydro**-…-F-5 | 1.286.967 | 2007-11-15 … 2015-09-22 |
| F-7.csv | 15/9-F-7 - Main Wellbore | Norway-Statoil-…-F-7 | 547.500 | 2007-09-15 … 2015-09-22 |
| F-9.csv | 15/9-F-9 - Main Wellbore | Norway-Statoil**Hydro**-…-F-9 | 457.545 | 2007-11-26 … 2015-09-22 |
| F-9_A.csv | 15/9-F-9 A - Main Wellbore | Norway-**NA**-…-F-9 A | 419.706 | 2009-06-27 … 2015-09-22 |
| VAR_F-5_alt.csv | 15/9-F-5 - Main Wellbore | **NA-NA**-…-F-5 | 59.489 | 2007-12-17 … 2015-09-22 |

**Hasil join (kunci = `nameWellbore` dinormalisasi + irisan rentang waktu):**

| CSV | run bhaRun bernama persis | interval valid bhaRun | **bertemu waktu** |
|---|---|---|---|
| F-14.csv | 7 | 2 (2016-07-30 … 2016-08-04) | **0** |
| F-5.csv | 11 | 3 (2016-08-29 … 2016-09-08) | **0** |
| VAR_F-5_alt.csv | 11 | 3 | **0** |
| F-9_A.csv | 2 | **0** (keduanya tanpa `dTimStop`; start 2016-09-29) | **0** |
| F-15A.csv | **0** (bhaRun hanya F-15 C/D) | kandidat well-level: 29 interval valid, **28 berada di dalam rentang CSV (9.922,9 jam)** | n/a (nama beda) |
| F-15_S.csv | **0** | kandidat well-level sama (F-15 C/D) → 28 | n/a (nama beda) |
| F-9.csv | **0** (bhaRun hanya F-9 A) | 0 | n/a |
| F-7.csv | **0** (F-7 tidak punya bhaRun sama sekali) | 0 | n/a |

**Akar penyebab (bukti, bukan dugaan):** semua 161 file bhaRun berada di folder `Norway-Statoil-NO …` dengan waktu **2012-06 … 2016-10**, sedangkan 8 CSV berasal dari folder `Norway-StatoilHydro/Statoil/NA/NA-NA …` dengan waktu **2007-09 … 2015-09-22**. Silang-periksa independen: 1 file log penuh folder `Norway-StatoilHydro-…-F-14` (`1/log/1/1/1/00001.xml`, grep seluruh file) berisi `2007-12-03 … 2015-06-10`, sedangkan 3 file sampel log folder `Norway-Statoil-NO …-F-14` berisi timestamp `2016-07-30 … 2016-08-13` — kedua pohon data memang menutup periode berbeda untuk nama well yang sama.

**Anomali kecil yang dilaporkan apa adanya:** timestamp MAKSIMUM identik `2015-09-22T12:21:35.938Z` di semua 8 CSV; baris terakhir `F-14.csv` ternyata baris KOSONG (hanya kolom timestamp, seluruh kolom lain kosong) → kemungkinan baris nyasar di akhir parse. Rentang "maks" di tabel = termasuk baris nyasar ini; data valid kemungkinan berakhir lebih awal. Tidak mengubah kesimpulan (interval bhaRun yang relevan tahun 2016 tetap di luar rentang).

---

## 5. Peluang PROSES / relasi antar-file (untuk Master, analisis relasi)

1. **Join lintas-folder WAJIB lewat field XML, bukan path** — terbukti: folder `…-F-1 C` ≠ `nameWellbore …-F-1 B`, dan bhaRun hanya ada di pohon `Norway-Statoil-NO` sedangkan CSV parser lama dari pohon `StatoilHydro/NA`. Kunci = `nameWellbore` + irisan waktu.
2. **2 kandidat join nyata ditemukan:** (a) bhaRun `F-15 C/D` ↔ `F-15A.csv`/`F-15_S.csv` di level WELL (28 interval, 9.922,9 jam dalam rentang) — perlu konfirmasi isi CSV; (b) `tubular` uidRef 161/161 → join ke 192 file `tubular/*.xml` (domain Pembaca 01) untuk identitas bit/BHA pada run yang sama.
3. **Jembatan waktu→kedalaman tipis:** `mdHoleStart/Stop` hanya 19/161 record, 3 di antaranya span nol (F-5 `3792→3792`). Untuk S-F1 (USROP depth-based) jembatan ini hampir tidak tersedia → kalau Master butuh pemotong depth per bit-run, itu harus datang dari sumber lain (EDM `CD_BHA_COMP_BIT` / tubular), bukan bhaRun.
4. **`drillingParams` = jendela on-bottom paling tajam:** 9 pasangan `dTimStartDrilling/StopDrilling` lengkap (F-1 C 4, F-1 2, F-11 T2 2, F-11 B 1) — kandidat batas stand yang lebih fisik daripada `dTimStart/Stop` (yang mencakup tripping). Plus 15−9 = 6 record start-drilling tanpa stop.
5. **`comments` 56/161** berisi teks bebas — belum diekstrak; bisa saja memuat catatan trip/washout (belum dicek isinya, domain bhaRun murni).
6. **Salinan ganda:** `external/dbx_volume/…` = 161 file identik (md5 cocok pada sampel) → jangan dihitung sebagai data baru.

---

## 6. Verifikasi silang vs angka D0 (`docs/V6_D1b_BHARUN.md`)

| Metrik | Klaim D0 | Hitung ulang sendiri | Status |
|---|---|---|---|
| file XML | 161 | 161 (`glob` + `rg`) | cocok |
| parse sukses | 161 (0 error) | 161 (0 error) | cocok |
| `dTimStart` | 161 | 161 | cocok |
| `dTimStop` | 114 | 114 | cocok |
| `numBitRun` | 11 (2 non-integer) | 11 (2 non-integer) | cocok |
| drilling window lengkap | 9 | 9 | cocok |
| durasi negatif | 6 | 6 | cocok |
| jumlah wellbore | 14 | 14 | cocok |
| distribusi per wellbore | F-1 C 26, F-11 B 26, F-15 D 16, F-1 B 17, F-15 C 14, F-11 T2 12, F-1 11, F-5 11, F-12 10, F-14 7, F-4 4, F-1 A 3, F-11 A 2, F-9 A 2 | identik | cocok |

**Tambahan yang TIDAK ada di D0** (temuan baru kartu ini): (a) 8 CSV parser lama = 0 tumpang-tindih dengan interval bhaRun pada join nama persis; (b) 141/161 run tidak punya CSV parser lama bernama sama; (c) `mdHoleStart/Stop` 19 record dengan 3 span nol; (d) baris nyasar timestamp-maks identik di semua 8 CSV.

---

## 7. BELUM DIVERIFIKASI (verification-mandatory #3)

1. **Apakah `F-15A.csv`/`F-15_S.csv` berisi data wellbore C/D** (kandidat join 28 interval) — butuh pembacaan isi CSV/lateral yang domain Pembaca 05. Di sini baru dibuktikan rentang waktu + nama folder.
2. **Kolom `well` di `USROP_labeled.csv`** (`USROP_A 3 N-SH-F-15d.csv`) = F-15 D atau F-15 Main — menentukan sisa-nyata jalur S-F1; domain Pembaca 08.
3. **Isi 56 kolom `comments`** — belum diekstrak (bisa berisi catatan trip).
4. **Apakah baris nyasar `2015-09-22T12:21:35.938Z` memang non-data** — diduga kuat (baris kosong), belum dicek di 7 CSV lain.
5. **Alasan dua pohon data (`StatoilHydro` vs `Statoil-NO`) menutup periode berbeda untuk nama well sama** — di luar lingkup domain bhaRun; dilaporkan sebagai fakta folder+waktu, bukan penjelasan sebab-akibat.
6. **Kelayakan statistik label** (apakah anchor ini bikin kelas lolos gate) = TIDAK dicek di sini — itu domain Master/V7-E, kartu ini hanya status ketersediaan data.

---

## 8. Ringkasan status (untuk Master)

- **S-B1/S-A2:** F-10 = TIDAK ADA (bukti grep) · F-4 = ADA START-ONLY (4) · F-12 = ADA START-ONLY (10) · F-15 = ADA LENGKAP (30 run, wellbore C/D). Folder bhaRun ≠ folder target parse → join via field.
- **S-F1:** `numBitRun` ADA (11; 9 integer, 2 non-integer, 0 negatif) tapi **hampir seluruhnya di wellbore yang bukan USROP**; USROP tanpa kolom waktu + `mdHole` bridge nyaris nol → **status praktis TIDAK ADA** untuk pemotong USROP, kecuali kemungkinan F-15 D (perlu konfirmasi Pembaca 08).
- **S-B2:** interval `dTimStart/Stop` ADA SETELAH DIOLAH (108 valid dari 114 pasangan) tetapi **0 interval bertemu dengan 8 CSV parser lama** pada join nama+waktu; kandidat per-well F-15 (28 interval) menunggu konfirmasi Pembaca 05. Jendela `dTimStart/StopDrilling` (9) = alternatif batas stand paling tajam.
