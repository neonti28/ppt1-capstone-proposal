# V6-D1a — Buka & Ekstrak WITSML TUBULAR (192 XML)

**Riset pendahuluan: `verification-mandatory` — verifikasi ulang 2026-10-11 dengan tool berbeda (glob, bukan parser ElementTree penulis): jumlah file XML tubular = 192, cocok dengan klaim §1.**

**Status: DIBUKA & DIPARSE.** 192/192 file XML terbaca, 0 gagal parse, 1392 komponen diekstrak.

- Task: `t_80ba3ae3` — [Pembaca 01] V6-D1a
- Tanggal eksekusi: 2026-10-10
- Target: `/mnt/d/Capstone 1/data/volve/witsml_raw/<well>/<section>/tubular/*.xml`
- Parser: `ElementTree` (XML asli, bukan regex), namespace `http://www.witsml.org/schemas/1series`

## Deliverables

| File | Isi | Ukuran |
|---|---|---|
| `/mnt/d/Capstone 1/scratch/v6_d1a_tubular.csv` | 1392 baris, 1 komponen/baris | 349.851 bytes |
| `/mnt/d/Capstone 1/scratch/v6_d1a_tubular_summary.json` | ringkasan per wellbore + audit | 13.650 bytes |
| `/mnt/d/Capstone 1/docs/V6_D1a_TUBULAR.md` | dokumen ini | — |

Kolom CSV: `wellbore, well_folder, section, assembly_name, assembly_type, typeTubularComp, od_m, id_m, len_m, sequence, q_N_per_m, weight_kN, wtPerLen_rep_kg_m, weight_rep_kN, skip_drill_string, source_file, raw_od, raw_id, raw_len`

`raw_od/raw_id/raw_len` = nilai mentah dari XML (dipertahankan untuk audit), `od_m/id_m/len_m` = nilai bersih (sentinel dibuang ke `null`).

---

## 1. Angka nyata (wajib lapor)

| Metrik | Nilai |
|---|---|
| File XML ditemukan | **192** |
| File diparse sukses | **192 / 192** (0 gagal) |
| Record `<tubular>` (assembly) | **192** |
| Assembly yang punya komponen | **190** (2 file kosong, lihat §3) |
| `<tubularComponent>` = baris CSV | **1392** |
| Wellbore (`nameWellbore`) | **16** |
| Folder well × section | **16** (1:1 dengan wellbore) |
| `uom` pada `od/id/len` | **4176/4176 = `m`**, 0 MISSING, 0 unit lain |
| Baris dengan `od+id+len` valid | **1330** (62 baris kena sentinel, §7) |
| Baris dengan `wtPerLen` lapor | **870** |
| Baris drill string (`skip=False`) | **1222** |
| Baris casing/liner/tubing (`skip=True`) | **170** |

`typeTubularAssy` per **assembly (n=192)**: `drilling` **182**, `unknown` **7**, `clean out` **2**, `completion or testing` **1**. (Catatan: kunci JSON `typeTubularAssy_counts` dihitung **per komponen** — 1350 / 35 / 4 / 3 = 1392 — bukan per assembly; angka per assembly di atas dari `assy_counts.py`.)

---

## 2. Bukti file dibuka (RAW — 3 file dicetak utuh)

Raw output dicetak langsung ke terminal saat eksekusi. Ringkasannya:

**File 1** — `Norway-Statoil-NO 15_$47$_9-F-15/2/tubular/1.xml`
```
<tubulars ... version="1.4.1.1"><tubular uidWell="dd19bf7b-..." uidWellbore="e0cab46e-..." uid="19VFNI35">
<nameWell>NO 15/9-F-15</nameWell><nameWellbore>NO 15/9-F-15 D</nameWellbore>
<name>15/9-F-15 D_19VFNI35</name><typeTubularAssy>drilling</typeTubularAssy>
<tubularComponent uid="47VFNI35"><typeTubularComp>drill pipe</typeTubularComp><sequence>1</sequence>
<id uom="m">0.118618000000173</id><od uom="m">0.139700000142494</od><len uom="m">900</len>
<lenJointAv uom="m">40</lenJointAv><numJointStand>3</numJointStand><wtPerLen uom="kg/m">36.95</wtPerLen>
<tensYield uom="Pa">999739765</tensYield> ... <vendor>BHI</vendor> ...</tubularComponent>
<commonData><sourceName>Baker Hughes</sourceName><dTimCreation>2016-07-14T11:22:00.587Z</dTimCreation>
<itemState>actual</itemState> ...</commonData></tubular></tubulars>
```
→ 1 komponen: drill pipe od=0,1397 m / id=0,118618 m / len=900 m, `wtPerLen=36,95 kg/m`.

**File 2** — `Norway-Statoil-NO 15_$47$_9-F-11/1/tubular/1.xml`
```
<nameWellbore>NO 15/9-F-11 T2</nameWellbore><name>15/9-F-11 T2_14QKUJ48</name>
<typeTubularAssy>drilling</typeTubularAssy>
```
7 × `<tubularComponent>`, semuanya `typeTubularComp=casing`, `sequence` 1–7:
`od uom="m"` = 0.8255 / 0.56896 / 0.55118 / 0.489204 / 0.593852 / 0.55118 / 0.56388,
`id uom="m"` = 0.489204 (semua), `len uom="m"` = 2.431 / 9 / 9.68 / 9.6831 / 17.451 / 72.55 / 6.4896,
masing-masing punya `<bitRecord><diaBit uom="m">-999.25</diaBit></bitRecord>` (sentinel), `sourceName=INTEQ`.

**File 3** — `Norway-Statoil-NO 15_$47$_9-F-15/1/tubular/1.xml`
```
<nameWellbore>NO 15/9-F-15 C</nameWellbore><name>15/9-F-15 C_25RGUI47</name>
<tubularComponent uid="264RGUI47"><typeTubularComp>drill pipe</typeTubularComp><sequence>1</sequence>
<id uom="m">0.0702056</id><od uom="m">0.0889</od><len uom="m">477.5</len>
<lenJointAv uom="m">28.65</lenJointAv><numJointStand>3</numJointStand><wtPerLen uom="kg/m">20.89</wtPerLen>
<tensYield uom="Pa">999739765</tensYield><idFishneck uom="m">0.0508</idFishneck> ...
```
→ 1 komponen: drill pipe 3-1/2" od=0,0889 m, len=477,5 m, `wtPerLen=20,89 kg/m`.

Teks mentah ketiga file ada di APPENDIX (di ekstrak langsung dari disk).

---

## 3. Dua file KOSONG (temuan, bukan kegagalan parse)

192 file terbaca, tetapi **2 file berisi record `<tubular>` tanpa satu pun `<tubularComponent>`**:

| File | Ukuran | `nameWellbore` | `name` | n_comp |
|---|---|---|---|---|
| `Norway-Statoil-NO 15_$47$_9-F-1 C/2/tubular/23.xml` | 903 B | NO 15/9-F-1 C | (lihat file) | 0 |
| `Norway-Statoil-NO 15_$47$_9-F-11/2/tubular/14.xml` | 741 B | NO 15/9-F-11 B | `15/9-F-11 B_30QKUJ48` | 0 |

Raw isi `F-11/2/tubular/14.xml` (utuh):
```xml
<?xml version="1.0" encoding="UTF-8"?><tubulars xmlns="http://www.witsml.org/schemas/1series" ... version="1.4.1.1"><tubular uidWell="da2c7481-6737-4b5e-b430-32d50e69bd9a" uidWellbore="a69101ab-ffbf-49a9-96c9-2a73e250ee48" uid="30QKUJ48"><nameWell>NO 15/9-F-11</nameWell><nameWellbore>NO 15/9-F-11 B</nameWellbore><name>15/9-F-11 B_30QKUJ48</name><typeTubularAssy>drilling</typeTubularAssy><commonData><sourceName>INTEQ</sourceName><dTimCreation>2013-06-03T16:27:12.468Z</dTimCreation><dTimLastChange>2013-06-03T16:27:12.468Z</dTimLastChange><itemState>actual</itemState><priv_userOwner>sc-sync-BHI</priv_userOwner><priv_ipOwner>192.168.157.1</priv_ipOwner></commonData></tubular></tubulars>
```
→ Header assembly lengkap, komponennya memang tidak dikirim Statoil/INTEQ. Ini **sumber data**, bukan error parser. Karena itu: 192 file = 192 assembly, 190 assembly ber-komponen, 1392 komponen.

---

## 4. Komposisi `typeTubularComp` (1392 komponen, 62 tipe)

Yang relevan untuk BHA / drilling string:

| Tipe | Jumlah |
|---|---|
| drill pipe | 218 |
| logging while drilling tool | 169 |
| sub-crossover | 131 |
| heavy weight drill pipe | 126 |
| casing | 95 |
| drill collar | 79 |
| other | 78 |
| stabilizer string | 66 |
| sub-stop | 42 |
| jar | 34 |
| accelerator | 32 |
| sub-float | 26 |
| bit PDC fixed cutter | 24 |
| tubing | 18 |
| mill taper | 18 |
| rotary steering tool | 17 |
| casing shoe screw-in | 15 |
| spear / bit insert roller cone | 11 / 11 |
| hanger casing subsea / sub-orienting | 10 / 10 |
| magnet / casing cutter / stabilizer near bit | 9 / 9 / 9 |
| float shoe / unknown / sub-bumper | 8 / 8 / 8 |
| casing crossover / **motor steerable** / mule shoe / running tool / **motor** | 7 / **7** / 6 / 6 / **6** |
| hanger liner / landing float collar / sub-bit / mill casing cutting | 5 / 5 / 5 / 5 |
| liner / float collar / bit hole opener / bit mill tooth roller cone / drill collar short / die collar / bullnose | 4 masing-masing |
| packer / sub-jetting / drill pipe compressive / bull plug | 3 masing-masing |
| sisanya (1–2): bridge plug, hanger casing surface, washover pipe, MWD pulser, hanger tubing, surface pipe, dll. | — |

→ **13 komponen motor**: 6 × `motor` + 7 × `motor steerable`, di 13 file berbeda.

---

## 5. Ringkasan per wellbore

Rumus berat kering (diminta task):
`q = (π/4)(od² − id²) × 7850 × 9.80665` [N/m], total = Σ q·len / 1000 [kN].
Skip tipe mengandung `casing`/`liner`/`tubing`.

> **PENTING — cara baca kolom:** "drill_len_m" dan "drillW_formula" adalah **KUMULATIF lintas semua assembly/run** dalam wellbore itu (setiap file = satu run/assembly terpisah), **bukan satu string fisik**. Angka string fisik per run ada di kolom **"max asm"**.

| wellbore (`nameWellbore`) | folder/sect | files | comps | drill_len_m (kumulatif) | drillW formula kN | n baris drill dgn wtPerLen | drillW dari wtPerLen kN* | max asm m | assembly terpanjang |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| NO 15/9-F-1 A | F-1 C/3 | 3 | 31 | 5.396,2 | 1.770,7 | 27 | 2.420,5 | 4.150,0 | 15/9-F-1 A_13RGUI47 |
| NO 15/9-F-1 B | F-1 C/1 | 17 | 113 | 27.218,6 | 8.922,5 | 70 | 10.792,5 | 4.322,0 | 15/9-F-1 B_14RGUI47 |
| NO 15/9-F-1 C | F-1 C/2 | 29 | 175 | 41.311,7 | 13.653,2 | 112 | 16.688,7 | 4.680,2 | 15/9-F-1 C_37RGUI47 |
| NO 15/9-F-1 | F-1 C/4 | 11 | 155 | 23.752,5 | 8.620,7 | 136 | 10.817,8 | 4.779,8 | 15/9-F-1_30RJGJ56 |
| NO 15/9-F-11 A | F-11/4 | 2 | 34 | 11.703,8 | 3.773,9 | 33 | 4.494,2 | **8.166,3** | 15/9-F-11 A_23QKUJ48 |
| NO 15/9-F-11 B | F-11/2 | 25 | 188 | 48.421,2 | 16.566,5 | 101 | 12.866,0 | 5.625,5 | 15/9-F-11 B_25QKUJ48 |
| NO 15/9-F-11 T2 | F-11/1 | 13 | 169 | 27.917,7 | 10.534,4 | 101 | 8.449,2 | 5.116,9 | 15/9-F-11 T2_19QKUJ48 |
| NO 15/9-F-11 | F-11/3 | 8 | 112 | 1.716,7 | 3.285,9 | 104 | 2.728,9 | 363,3 | 15/9-F-11_7QKUJ48 |
| NO 15/9-F-12 | F-12/1 | 9 | 50 | 6.190,0 | 2.250,7 | 11 | 2.474,6 | 1.002,7 | 15/9-F-12_18VG4D36 |
| NO 15/9-F-14 | F-14/1 | 6 | 13 | 5.750,8 | 1.746,9 | 3 | 1.193,9 | 1.240,0 | 15/9-F-14_2VG4D36 |
| NO 15/9-F-15 C | F-15/1 | 14 | 51 | 22.494,2 | 7.234,6 | 26 | 4.599,2 | 4.763,4 | 15/9-F-15 C_4RJGJ56 |
| NO 15/9-F-15 D | F-15/2 | 36 | 235 | 41.449,2 | 15.312,4 | 90 | 16.017,3 | 5.909,1 | 15/9-F-15 D_26RJGJ56 |
| NO 15/9-F-4 | F-4/1 | 3 | 4 | 762,0 | 220,6 | 0 | — | 562,0 | 15/9-F-4_16VIRG33 |
| NO 15/9-F-5 | F-5/1 | 9 | 42 | 1.580,3 | 712,8 | 4 | 310,1 | 604,6 | 15/9-F-5_21VG4D36 |
| NO 15/9-F-7 | F-7/1 | 5 | 18 | 861,3 | 312,1 | 1 | 14,4 | 368,8 | 15/9-F-7_43VFNI35 |
| NO 15/9-F-9 A | F-9/1 | 2 | 2 | 886,0 | 224,1 | 0 | — | 886,0 | 15/9-F-9 A_12VIRG33 |
| **TOTAL** | | **192** | **1392** | **267.412,1** | **95.141,9** | **819** | **93.867,2** | | |

\* kolom `wtPerLen` hanya menjumlahkan **819 dari 1222** baris drill string yang membawa `wtPerLen` di XML (870 dari 1392 bila semua tipe dihitung) — karena itu kolom ini **bukan total sebanding** dengan kolom formula (lihat §6).

**Total SEMUA komponen (tanpa skip):** 354.033,0 m · 158.343,9 kN (formula) · 111.434,7 kN (wtPerLen, 870 baris).

**Catatan folder ≠ wellbore** (validasi identitas target — jangan pakai nama folder sebagai wellbore):

| folder | `nameWellbore` di dalamnya |
|---|---|
| `Norway-Statoil-NO 15_$47$_9-F-1 C` | sect 1 → **F-1 B** (17 file), sect 2 → **F-1 C** (29), sect 3 → **F-1 A** (3), sect 4 → **F-1** (11) |
| `Norway-Statoil-NO 15_$47$_9-F-11` | sect 1 → **F-11 T2** (13), sect 2 → **F-11 B** (25), sect 3 → **F-11** (8), sect 4 → **F-11 A** (2) |
| `Norway-Statoil-NO 15_$47$_9-F-15` | sect 1 → **F-15 C** (14), sect 2 → **F-15 D** (36) |
| `Norway-Statoil-NO 15_$47$_9-F-9` | sect 1 → **F-9 A** (2) |

---

## 6. Validasi formula q terhadap `wtPerLen` yang dilaporkan file

870 komponen membawa `<wtPerLen uom="kg/m">` (nomor yang **dilaporkan vendor**, bukan hasil hitung). Dibandingkan dengan formula yang diminta task, pada **846 pasangan valid**:

| Metrik | Nilai |
|---|---|
| pasangan | 846 |
| median error bertanda | **−14,80 %** (formula kurang) |
| median \|error\| | 20,11 % |
| MAE | 35,26 % |
| dalam ±10 % | 289 / 846 (34,2 %) |
| dalam ±20 % | 420 / 846 (49,6 %) |

Per tipe (n ≥ 5), median error formula vs laporan:

| tipe | n | median % | rentang % |
|---|---:|---:|---|
| drill collar | 60 | **+0,13** | −51,9 … +12,3 |
| casing | 29 | −1,15 | −16,0 … +12,9 |
| stabilizer string | 45 | −9,32 | −63,3 … +336,5 |
| heavy weight drill pipe | 93 | −18,56 | −49,1 … +90,4 |
| drill pipe | 159 | −20,11 | −73,5 … +115,4 |
| logging while drilling tool | 149 | −30,38 | −69,9 … +35,6 |
| accelerator / jar | 32 / 32 | −33,5 / −33,3 | −95,4 … −2,0 |
| motor | 5 | −39,68 | −40,1 … −39,7 |
| rotary steering tool | 17 | −39,68 | −60,3 … +8,9 |

**Apples-to-apples (795 baris drill string yang punya KEDUA nilai):**

| | |
|---|---|
| formula q | **72.994,1 kN** |
| `wtPerLen` dilaporkan | **93.830,0 kN** |
| selisih | **−22,21 %** |

**Kesimpulan:** formula `(π/4)(od²−id²)·7850·9,80665` adalah **estimasi kasar** — akurat untuk drill collar & casing, tapi **underestimate ±15–22 % untuk drill string** (tidak memperhitungkan tool joint / upset / grade), dan **tidak valid untuk alat** yang bukan tabung baja (lihat §7). Kolom `wtPerLen_rep_kg_m` + `weight_rep_kN` sudah ditambahkan ke CSV supaya downstream bisa memakai angka laporan yang lebih baik, dengan coverage 870/1392 baris.

---

## 7. Temuan data quality

1. **Sentinel WITSML `-999.25`** (bukan nilai fisik — parser membuang ke `null`):
   - `id` = −999.25 pada **62 baris**, rinciannya terverifikasi: `bit PDC fixed cutter` 20, `bit insert roller cone` 11, `other` 6, `stabilizer near bit` 4, `bit mill tooth roller cone` 4, `logging while drilling tool` 2, `casing` 2, `mill taper` 2, `mill casing cutting` 2, + 9 tipe masing-masing 1 (sub-orienting, sub-stop, casing crossover, casing shoe screw-in, hanger casing subsea, motor steerable, mule shoe, drill collar short, landing float collar). 35 dari 62 adalah **bit** (bit memang tidak punya `id`).
   - `od` = −999.25 pada **1 baris** → motor steerable `15/9-F-11_5QKUJ48`
   - `len` = −999.25 pada **1 baris** → motor steerable `15/9-F-11_5QKUJ48` (**od=id=len=−999.25, geometri motor ini hilang total**)
   - Total **62 baris tidak punya bobot formula** (1392 − 1330 = 62 ✓)
   - `<diaBit>`: **913 dari 952** = `−999.25`, 39 berisi nilai nyata (0,1397 … 0,6604 m) — 39 ini cocok dengan jumlah `<typeBit>` = 39.
2. **2 file tanpa komponen** — §3.
3. **`bit hole opener` 4 komponen = 1.015,2 kN**, rata-rata **46,96 kN/m** (≈4,8 ton/m) — mustahil secara fisik. Tiga di antaranya `od=0,9144 m` (36") × `id=0,0635 m` × `len=6,7 m` → `q=50.309,87 N/m` = **50,31 kN/m (≈5,1 ton/m) per komponen**; formula memperlakukan silinder setebal itu sebagai baja utuh. Jangan pakai formula untuk bit/hole opener/motor/LWD.
   Rata-rata q per tipe (drill string): drill pipe 0,30 kN/m · HWDP 0,73 · drill collar 2,23 · LWD 2,24 · stabilizer 4,95 · motor steerable 5,96 · bit hole opener **46,96**.
4. **Aturan skip mengena 14 baris yang bukan string**: `casing cutter` (9 baris, 49,5 m) + `mill casing cutting` (5 baris, 47,1 m) ikut ter-skip karena substring `casing`. Dampak: **96,6 m = 0,036 %** dari 267.412,1 m — tidak material, tapi dicatat.
5. **`surface pipe`** 1 komponen (505,6 m) ikut terhitung sebagai drill string (tabel per tipe di JSON).

---

## 8. RATING MOTOR: **TIDAK ADA di 192 file**

Ini **temuan**, bukan kegagalan. Pencarian dilakukan di **semua tag dan semua teks** 192 file:

| Kata kunci | Jumlah file (dari 192) |
|---|---:|
| `torqueMax` | **0** |
| `Pmax` | **0** |
| `revPerGallon` | **0** |
| `rpmMax` | **0** |
| `powerMax` | **0** |
| `torque` | **0** |
| `flowrateMx` | 9 (19 elemen) — **semua di `/mwdTool/`** |
| `motor` | 13 — **semua sebagai `typeTubularComp` / `mwdComponent` / `description`** |

Inventarisasi **semua path elemen** yang mengandung `torque|pmax|pressure|max|rpm|power|revper|flowrate` di 192 file hanya menghasilkan dua:

```
19  /mwdTool/flowrateMn
19  /mwdTool/flowrateMx
```

Keduanya adalah **rentang operasi alat MWD** (mis. `0.00833 … 0.0883` m³/s dan `2100 … 5300` L/min), **bukan rating motor tekan**.

Kemunculan kata `motor` hanya di:
```
 6  /typeTubularComp = motor
 7  /typeTubularComp = motor steerable
 5  /customData/mwdComponent/fullName = Modular Motor
 7  /customData/mwdComponent/fullName = Motor - steerable
 1  /customData/mwdComponent/fullName = Motor
 1  /customData/mwdComponent/shortName = Motor
 7  /customData/mwdComponent/shortName = Steer motor
 3  /description = Modular Motor
```
→ semuanya **identifikasi komponen**, bukan rating.

### VERDIK: **rating motor tidak ada di 192 file.**

Yang **ADA** untuk motor hanyalah geometri BHA (13 komponen):

| wellbore | assembly | type | seq | od (m) | id (m) | len (m) |
|---|---|---|---:|---|---|---|
| NO 15/9-F-1 B | 15/9-F-1 B_14RGUI47 | motor | 4 | 0,25400 | 0,17220 | 9,22 |
| NO 15/9-F-1 C | 15/9-F-1 C_35RGUI47 | motor | 4 | 0,26035 | 0,17221 | 9,23 |
| NO 15/9-F-1 | 15/9-F-1_1RGUI47 | motor steerable | 2 | 0,32385 | 0,07620 | 9,97 |
| NO 15/9-F-11 T2 | 15/9-F-11 T2_9QKUJ48 | motor steerable | 2 | 0,32385 | 0,07938 | 10,80 |
| NO 15/9-F-11 T2 | 15/9-F-11 T2_10QKUJ48 | motor steerable | 2 | 0,32385 | 0,07938 | 10,81 |
| NO 15/9-F-11 T2 | 15/9-F-11 T2_11QKUJ48 | motor steerable | 2 | 0,32385 | 0,07938 | 10,81 |
| NO 15/9-F-11 B | 15/9-F-11 B_26QKUJ48 | motor | 4 | 0,24130 | 0,07620 | 9,21 |
| NO 15/9-F-11 B | 15/9-F-11 B_24QKUJ48 | motor | 4 | 0,24130 | 0,07620 | 9,17 |
| NO 15/9-F-11 | 15/9-F-11_8QKUJ48 | motor steerable | 2 | 0,32385 | 0,07938 | 10,45 |
| NO 15/9-F-11 | 15/9-F-11_6QKUJ48 | motor steerable | 2 | 0,32385 | 0,07938 | 10,45 |
| NO 15/9-F-11 | 15/9-F-11_5QKUJ48 | motor steerable | 2 | **−999,25** | **−999,25** | **−999,25** |
| NO 15/9-F-15 D | 15/9-F-15 D_26VFNI35 | motor | 5 | 0,18098 | 0,07620 | 8,23 |
| NO 15/9-F-15 D | 15/9-F-15 D_18RJGJ56 | motor | 4 | 0,25400 | 0,17220 | 9,29 |

**Implikasi untuk model:** torque/power/RPM motor **tidak bisa diambil dari WITSML tubular Volve**. Kalau model butuh rating motor, sumbernya harus lain (spesifikasi pabrikan, Daily Drilling Report, atau asumsi eksplisit yang ditandai sebagai asumsi).

---

## 9. Tiga contoh assembly BHA lengkap

Dipilih yang benar-benar ber-BHA (drill collar + stabilizer + motor/jar), diurutkan berdasar `sequence`.

### (a) `NO 15/9-F-1 C` :: `15/9-F-1 C_35RGUI47` — 19 komponen
file: `Norway-Statoil-NO 15_$47$_9-F-1 C/2/tubular/5.xml`, `typeTubularAssy=drilling`

| seq | type | od (m) | id (m) | len (m) |
|---:|---|---|---|---|
| 1 | bit PDC fixed cutter | 0,31115 | *−999,25* | 0,34 |
| 2 | rotary steering tool | 0,26035 | 0,06299 | 2,51 |
| 3 | logging while drilling tool | 0,24130 | 0,07303 | 2,15 |
| 4 | **motor** | 0,26035 | 0,17221 | 9,23 |
| 5 | stabilizer string | 0,24130 | 0,07938 | 3,71 |
| 6 | logging while drilling tool | 0,24448 | 0,07620 | 6,95 |
| 7 | MWD pulser | 0,24130 | 0,07620 | 3,68 |
| 8 | sub-stop | 0,24130 | 0,07620 | 1,09 |
| 9 | stabilizer string | 0,20320 | 0,07303 | 2,20 |
| 10 | sub-float | 0,21352 | 0,07303 | 0,80 |
| 11 | heavy weight drill pipe | 0,16828 | 0,07303 | 30,00 |
| 11 | drill collar | 0,20955 | 0,07303 | 18,79 |
| 12 | jar | 0,20320 | 0,07620 | 9,69 |
| 13 | drill collar | 0,20955 | 0,07303 | 8,68 |
| 13 | heavy weight drill pipe | 0,16828 | 0,07303 | 40,00 |
| 14 | sub-crossover | 0,20320 | 0,07620 | 0,79 |
| 15 | heavy weight drill pipe | 0,13970 | 0,07620 | 121,96 |
| 16 | drill pipe | 0,13970 | 0,12136 | 1.937,633 |
| 17 | drill pipe | 0,13970 | 0,11862 | 1.493,690 |

### (b) `NO 15/9-F-1` :: `15/9-F-1_1RGUI47` — 23 komponen
file: `Norway-Statoil-NO 15_$47$_9-F-1 C/4/tubular/5.xml`, `typeTubularAssy=drilling`

| seq | type | od (m) | id (m) | len (m) |
|---:|---|---|---|---|
| 1 | bit insert roller cone | 0,66040 | *−999,25* | 0,59 |
| 2 | **motor steerable** | 0,32385 | 0,07620 | 9,97 |
| 3 | stabilizer string | 0,24130 | 0,07620 | 2,75 |
| 4 | sub-stop | 0,24130 | 0,07938 | 0,68 |
| 5–7 | logging while drilling tool ×3 | 0,24130 (jg 0,24130) | 0,07620 / 0,07938 / 0,07620 | 6,97 / 1,79 / 3,60 |
| 8 | other | 0,24130 | 0,07620 | 5,75 |
| 9 | sub-stop | 0,24130 | 0,07620 | 0,74 |
| 10 | stabilizer string | 0,24130 | 0,07938 | 1,91 |
| 11 | sub-orienting | 0,24130 | 0,07620 | 1,36 |
| 12 | stabilizer string | 0,20955 | 0,06985 | 2,33 |
| 13 | sub-crossover | 0,24130 | 0,07620 | 0,70 |
| 13 | drill collar | 0,20955 | 0,07303 | 9,00 |
| 14 | stabilizer string | 0,20320 | 0,07144 | 2,33 |
| 15 | jar | 0,20320 | 0,07620 | 9,69 |
| 15 | drill collar | 0,20320 | 0,07620 | 18,00 |
| 16 | accelerator | 0,17780 | 0,17145 | 3,00 |
| 17 | drill collar | 0,20955 | 0,07303 | 18,00 |
| 17 | sub-crossover | 0,20320 | 0,07620 | 1,00 |
| 18 | heavy weight drill pipe | 0,13970 | 0,09843 | 157,78 |
| 18 | accelerator | 0,20320 | 0,07620 | 9,00 |
| 19 | drill pipe | 0,13970 | 0,12136 | 1.291,938 |

### (c) `NO 15/9-F-11 T2` :: `15/9-F-11 T2_9QKUJ48` — 21 komponen
file: `Norway-Statoil-NO 15_$47$_9-F-11/1/tubular/13.xml`, `typeTubularAssy=drilling`

| seq | type | od (m) | id (m) | len (m) |
|---:|---|---|---|---|
| 1 | bit insert roller cone | 0,66040 | *−999,25* | 0,56 |
| 2 | **motor steerable** | 0,32385 | 0,07938 | 10,80 |
| 3 | stabilizer string | 0,65405 | 0,07938 | 2,86 |
| 4 | sub-stop | 0,24130 | 0,07938 | 0,78 |
| 5 | logging while drilling tool | 0,24130 | 0,06033 | 7,01 |
| 6 | logging while drilling tool | 0,23813 | 0,07303 | 1,83 |
| 7 | logging while drilling tool | 0,24130 | 0,06033 | 3,57 |
| 8 | other | 0,24130 | 0,06033 | 5,73 |
| 9 | sub-stop | 0,24130 | 0,07938 | 0,71 |
| 10 | stabilizer string | 0,24130 | 0,07938 | 1,94 |
| 11 | sub-orienting | 0,24130 | 0,07303 | 1,37 |
| 12 | sub-crossover | 0,24130 | 0,07620 | 0,70 |
| 13 | drill collar | 0,20955 | 0,07303 | 8,55 |
| 14 | stabilizer string | 0,20320 | 0,07620 | 2,25 |
| 15 | drill collar | 0,20955 | 0,07303 | 44,86 |
| 16 | jar | 0,20320 | 0,07620 | 9,68 |
| 17 | drill collar | 0,20955 | 0,07303 | 17,74 |
| 18 | accelerator | 0,20320 | 0,07620 | 9,70 |
| 19 | sub-crossover | 0,20320 | 0,07620 | 1,03 |
| 20 | heavy weight drill pipe | 0,13970 | 0,09843 | 81,30 |
| 21 | drill pipe | 0,13970 | 0,12065 | 40,63 |

---

## 10. Reproduksi

Script ada di workspace task (`t_80ba3ae3`), urutan eksekusi:

```
python3 parse_tubular.py        # 192 file -> CSV + JSON (parse, q, bobot, cek rating motor)
python3 augment_tubular.py      # audit sentinel, max assembly per wellbore, final verdict motor
python3 analyze_tubular.py      # bukti path elemen 'motor'/flowrate, mapping folder->wellbore, 3 BHA
python3 validate_formula.py     # formula q vs wtPerLen laporan
python3 pair_compare.py         # apples-to-apples formula vs laporan (baris sama)
python3 headline.py             # angka headline + artefak aturan skip
python3 weight_breakdown.py     # kontribusi bobot per tipe
python3 check_gaps.py           # 2 file tanpa komponen
python3 verify_claims.py        # rincian sentinel per tipe + distribusi diaBit
python3 wpl_counts.py           # jumlah baris drill dgn wtPerLen per wellbore
python3 assy_counts.py          # typeTubularAssy per assembly (192)
python3 verify_examples.py      # cetak ulang 3 contoh assembly dari CSV
python3 append_raw.py           # lampirkan APPENDIX raw 3 file ke dokumen
```

Semua angka di dokumen ini berasal dari output nyata script di atas, bukan estimasi.

---

# APPENDIX — RAW isi 3 file (di-`cat` langsung dari disk)

## F-15/2/tubular/1.xml — File 1 - drill pipe 5-1/2 in, 1 komponen

path: `/mnt/d/Capstone 1/data/volve/witsml_raw/Norway-Statoil-NO 15_$47$_9-F-15/2/tubular/1.xml`  
ukuran: 1528 bytes

```
<?xml version="1.0" encoding="UTF-8"?><tubulars xmlns="http://www.witsml.org/schemas/1series" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.4.1.1"><tubular uidWell="dd19bf7b-02a7-4383-9038-ce201cee4d91" uidWellbore="e0cab46e-aa2a-4d69-b466-108dafd4ae62" uid="19VFNI35"><nameWell>NO 15/9-F-15</nameWell><nameWellbore>NO 15/9-F-15 D</nameWellbore><name>15/9-F-15 D_19VFNI35</name><typeTubularAssy>drilling</typeTubularAssy><tubularComponent uid="47VFNI35"><typeTubularComp>drill pipe</typeTubularComp><sequence>1</sequence><id uom="m">0.118618000000173</id><od uom="m">0.139700000142494</od><len uom="m">900</len><lenJointAv uom="m">40</lenJointAv><numJointStand>3</numJointStand><wtPerLen uom="kg/m">36.95</wtPerLen><tensYield uom="Pa">999739765</tensYield><idFishneck uom="m">0.101600000103632</idFishneck><odFishneck uom="m">0.184150000000269</odFishneck><configCon>unknown</configCon><vendor>BHI</vendor><customData><mwdComponent><shortName>DP</shortName><fullName>Drill pipe</fullName></mwdComponent></customData></tubularComponent><commonData><sourceName>Baker Hughes</sourceName><dTimCreation>2016-07-14T11:22:00.587Z</dTimCreation><dTimLastChange>2016-07-15T22:42:43.391Z</dTimLastChange><itemState>actual</itemState><priv_userLastChange>sc-sync-bhi</priv_userLastChange><priv_ipLastChange>143.97.229.4</priv_ipLastChange><priv_userOwner>statfeedstg</priv_userOwner><priv_ipOwner>10.166.14.6</priv_ipOwner><priv_dTimReceived>2016-07-15T22:40:12.312Z</priv_dTimReceived></commonData></tubular></tubulars>
```

## F-11/1/tubular/1.xml — File 2 - 7 casing components

path: `/mnt/d/Capstone 1/data/volve/witsml_raw/Norway-Statoil-NO 15_$47$_9-F-11/1/tubular/1.xml`  
ukuran: 4567 bytes

```
<?xml version="1.0" encoding="UTF-8"?><tubulars xmlns="http://www.witsml.org/schemas/1series" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.4.1.1"><tubular uidWell="da2c7481-6737-4b5e-b430-32d50e69bd9a" uidWellbore="31f506a6-0faf-4b83-be77-ff3864dd9eda" uid="14QKUJ48"><nameWell>NO 15/9-F-11</nameWell><nameWellbore>NO 15/9-F-11 T2</nameWellbore><name>15/9-F-11 T2_14QKUJ48</name><typeTubularAssy>drilling</typeTubularAssy><tubularComponent uid="220QKUJ48"><typeTubularComp>casing</typeTubularComp><sequence>2</sequence><id uom="m">0.489204000000714</id><od uom="m">0.568960000000831</od><len uom="m">9</len><lenJointAv uom="m">9</lenJointAv><numJointStand>1</numJointStand><tensYield uom="Pa">0</tensYield><configCon>unknown</configCon><vendor>BHI</vendor><bitRecord uid="30088"><diaBit uom="m">-999.25</diaBit></bitRecord><customData><mwdComponent><shortName>Csg</shortName><fullName>Csg</fullName></mwdComponent></customData></tubularComponent><tubularComponent uid="218QKUJ48"><typeTubularComp>casing</typeTubularComp><sequence>4</sequence><id uom="m">0.489204000000714</id><od uom="m">0.551180000000805</od><len uom="m">72.55</len><lenJointAv uom="m">72.55</lenJointAv><numJointStand>1</numJointStand><tensYield uom="Pa">0</tensYield><configCon>unknown</configCon><vendor>BHI</vendor><bitRecord uid="30087"><diaBit uom="m">-999.25</diaBit></bitRecord><customData><mwdComponent><shortName>Csg</shortName><fullName>Csg</fullName></mwdComponent></customData></tubularComponent><tubularComponent uid="215QKUJ48"><typeTubularComp>casing</typeTubularComp><sequence>7</sequence><id uom="m">0.489204000000714</id><od uom="m">0.563880000000823</od><len uom="m">6.4896</len><lenJointAv uom="m">6.4896</lenJointAv><numJointStand>1</numJointStand><tensYield uom="Pa">0</tensYield><configCon>unknown</configCon><vendor>BHI</vendor><bitRecord uid="24409"><diaBit uom="m">-999.25</diaBit></bitRecord><customData><mwdComponent><shortName>Csg</shortName><fullName>Csg</fullName></mwdComponent></customData></tubularComponent><tubularComponent uid="221QKUJ48"><typeTubularComp>casing</typeTubularComp><sequence>1</sequence><id uom="m">0.489204000000714</id><od uom="m">0.825500000001205</od><len uom="m">2.431</len><lenJointAv uom="m">2.431</lenJointAv><numJointStand>1</numJointStand><tensYield uom="Pa">0</tensYield><configCon>unknown</configCon><vendor>BHI</vendor><bitRecord uid="30089"><diaBit uom="m">-999.25</diaBit></bitRecord><customData><mwdComponent><shortName>Csg</shortName><fullName>Csg</fullName></mwdComponent></customData></tubularComponent><tubularComponent uid="219QKUJ48"><typeTubularComp>casing</typeTubularComp><sequence>3</sequence><id uom="m">0.489204000000714</id><od uom="m">0.551180000000805</od><len uom="m">9.68</len><lenJointAv uom="m">9.68</lenJointAv><numJointStand>1</numJointStand><tensYield uom="Pa">0</tensYield><configCon>unknown</configCon><vendor>BHI</vendor><bitRecord uid="30084"><diaBit uom="m">-999.25</diaBit></bitRecord><customData><mwdComponent><shortName>Csg</shortName><fullName>Csg</fullName></mwdComponent></customData></tubularComponent><tubularComponent uid="216QKUJ48"><typeTubularComp>casing</typeTubularComp><sequence>6</sequence><id uom="m">0.489204000000714</id><od uom="m">0.593852000000867</od><len uom="m">17.451</len><lenJointAv uom="m">17.451</lenJointAv><numJointStand>1</numJointStand><tensYield uom="Pa">0</tensYield><configCon>unknown</configCon><vendor>BHI</vendor><bitRecord uid="30085"><diaBit uom="m">-999.25</diaBit></bitRecord><customData><mwdComponent><shortName>Csg</shortName><fullName>Csg</fullName></mwdComponent></customData></tubularComponent><tubularComponent uid="217QKUJ48"><typeTubularComp>casing</typeTubularComp><sequence>5</sequence><id uom="m">0.489204000000714</id><od uom="m">0.551180000000805</od><len uom="m">9.6831</len><lenJointAv uom="m">9.6831</lenJointAv><numJointStand>1</numJointStand><tensYield uom="Pa">0</tensYield><configCon>unknown</configCon><vendor>BHI</vendor><bitRecord uid="30086"><diaBit uom="m">-999.25</diaBit></bitRecord><customData><mwdComponent><shortName>Csg</shortName><fullName>Csg</fullName></mwdComponent></customData></tubularComponent><commonData><sourceName>INTEQ</sourceName><dTimCreation>2013-04-05T17:34:54.101Z</dTimCreation><dTimLastChange>2013-05-07T11:38:56.505Z</dTimLastChange><itemState>actual</itemState><priv_userLastChange>sc-sync-BHI</priv_userLastChange><priv_ipLastChange>192.168.157.1</priv_ipLastChange><priv_userOwner>wlfeeddub</priv_userOwner><priv_ipOwner>147.108.61.93</priv_ipOwner></commonData></tubular></tubulars>
```

## F-15/1/tubular/1.xml — File 3 - drill pipe 3-1/2 in, 1 komponen

path: `/mnt/d/Capstone 1/data/volve/witsml_raw/Norway-Statoil-NO 15_$47$_9-F-15/1/tubular/1.xml`  
ukuran: 1559 bytes

```
<?xml version="1.0" encoding="UTF-8"?><tubulars xmlns="http://www.witsml.org/schemas/1series" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.4.1.1"><tubular uidWell="dd19bf7b-02a7-4383-9038-ce201cee4d91" uidWellbore="9ab4989d-11c6-4ac1-83c1-e74362292dd8" uid="25RGUI47"><nameWell>NO 15/9-F-15</nameWell><nameWellbore>NO 15/9-F-15 C</nameWellbore><name>15/9-F-15 C_25RGUI47</name><typeTubularAssy>drilling</typeTubularAssy><tubularComponent uid="264RGUI47"><typeTubularComp>drill pipe</typeTubularComp><sequence>1</sequence><id uom="m">0.0702056</id><od uom="m">0.0889</od><len uom="m">477.5</len><lenJointAv uom="m">28.65</lenJointAv><numJointStand>3</numJointStand><wtPerLen uom="kg/m">20.89</wtPerLen><tensYield uom="Pa">999739765</tensYield><idFishneck uom="m">0.0508</idFishneck><odFishneck uom="m">0.104775</odFishneck><configCon>unknown</configCon><vendor>BHI</vendor><bitRecord uid="39395"><diaBit uom="m">-999.25</diaBit></bitRecord><customData><mwdComponent><shortName>DP</shortName><fullName>Drill pipe</fullName></mwdComponent></customData></tubularComponent><commonData><sourceName>INTEQ</sourceName><dTimCreation>2013-10-18T13:45:17.819Z</dTimCreation><dTimLastChange>2013-11-06T16:45:40.730Z</dTimLastChange><itemState>actual</itemState><priv_userLastChange>sc-sync-BHI</priv_userLastChange><priv_ipLastChange>192.168.157.252</priv_ipLastChange><priv_userOwner>wlfeeddub</priv_userOwner><priv_ipOwner>212.33.154.196</priv_ipOwner><priv_dTimReceived>2013-11-06T16:45:40.730Z</priv_dTimReceived></commonData></tubular></tubulars>
```
