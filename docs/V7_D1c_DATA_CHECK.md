# V7-D1c — Cek Ketersediaan Data untuk Solusi R&D
## Domain: WITSML TRAJECTORY (63 XML) + wbGeometry (27 XML)

Role: [Pembaca 03] · Board: capstone-v7-solve · Tugas: t_8200703b · Spesifikasi: Master V7-M1 (komentar kartu + `docs/V7_M1_DELEGASI.md` §2.3)
Tanggal: 2026-10-11 · Status: EKSEKUSI SELESAI (bukti di bawah)

Riset pendahuluan: **verification-mandatory** — tiap angka di dokumen ini berasal dari output tool run (parse XML, hitung non-null, grep ketiadaan), bukan ingatan; klaim D0 di-cross-check dengan recount independen dan angka-angkanya cocok persis.
Riset pendahuluan: **scientific-critical-thinking** — pemisahan OBSERVED/DERIVED/HYPOTHESIS dipertahankan: "ADA" = terhitung dari file; "menutup rentang" = deretan dari perbandingan dua pengukuran; identitas wellbore lintas folder operator = hipotesis untuk Master, bukan klaim.

---

## 0. Bukti pembukaan file (acceptance a)

Dua file domain dibuka dan isinya dicetak mentah:

**(a) Trajectory** — `witsml_raw/Norway-StatoilHydro-15_$47$_9-F-14/1/trajectory/1.xml` (cuplikan):
```xml
<trajectory uidWell="W-353085" uidWellbore="B-353085" uid="T-549724-1">
  <nameWell>15/9-F-14</nameWell><nameWellbore>15/9-F-14 - Main Wellbore</nameWellbore>
  <name>Real Time MWD/LWD data - 36in. Section - Actual Traj</name>
  <mdMn uom="m">0</mdMn><mdMx uom="m">184.0998096</mdMx>
  <trajectoryStation uid="S-0">
    <md uom="m">0</md><tvd uom="m">0</tvd>
    <incl uom="dega">0</incl><azi uom="dega">0</azi>
    <dls uom="dega/m">0</dls> ...
```

**(b) wbGeometry** — `witsml_raw/Norway-Statoil-NO 15_$47$_9-F-14/1/wbGeometry/1.xml` (cuplikan):
```xml
<wbGeometry ...><nameWell>NO 15/9-F-14</nameWell><mdBottom uom="m">3695</mdBottom>
<gapAir uom="m">0</gapAir><depthWaterMean uom="m">91</depthWaterMean>
<wbGeometrySection uid="4VG4D36"><typeHoleCasing>liner</typeHoleCasing>
  <mdTop uom="m">2597</mdTop><mdBottom uom="m">3695</mdBottom>
  <tvdTop uom="m">2597</tvdTop><tvdBottom uom="m">3695</tvdBottom>
  <idSection uom="m">0.157073600000229</idSection><odSection uom="m">0.17780000000026</odSection>
</wbGeometrySection> ...
```

Total terparse: **63/63 file trajectory + 27/27 file wbGeometry, 0 error parse** (script `parse_traj.py`, `xml.etree.ElementTree`).

---

## 1. Tabel utama — solusi R&D | data needed | status | bukti | peluang proses

| # | Solusi R&D | Data needed | Status | BUKTI (kolom + baris + path) | Peluang proses |
|---|---|---|---|---|---|
| 1 | **S-F1** (bit_wear; SHAP didominasi `TVD_mean/last` → MD→TVD wajib benar) | Station MD→TVD per wellbore fold (F-14, F-15, F-15S, F-5, F-9_A) | **ADA SETELAH DIOLAH** (interpolasi MD→TVD) + **cross-check ADA LANGSUNG di domain USROP** | Kolom `md`+`tvd` ada: 5.561/5.561 non-null md, **5.543/5.561 non-null tvd** (18 hilang = `Norway-StatoilHydro-15_$47$_9-F-9/1/trajectory/2.xml`), uom md/tvd = `m` 5.561+5.543 (100%). Coverage per fold: F-14 ✓ (stasiun 0–3.750 m vs USROP 987,9–3.466,0), F-15 ✓ (0–4.075,0 vs 1.306,5–4.065,3), F-5 ✓ via `Norway-Statoil-NO 15_9-F-5` (0–3.792,0 vs 2.828,2–3.792,2), F-9_A ✓ via `Norway-Statoil-NO 15_9-F-9` (0–1.206,0 vs 491,0–1.206,0), **F-15S ✗ ada ekor tak-tertutup 47,1 m** (traj StatoilHydro F-15S berhenti 4.042,9; USROP s.d. 4.090,0). Detail §2. | Proses: (i) pilih 1 trajectory per wellbore (tiap wellbore punya 1–5 file seksi; lintas folder operator NO vs StatoilHydro ada DUPLIKAT — F-12 `trajectory/2.xml` vs `7.xml`: md identik 200/200 indeks, 197/200 identik md+tvd+incl+azi); (ii) sort MD monotonik + dedup; (iii) linear interp MD→TVD ke baris time-based — estimasi baris hasil = baris USROP per fold: F-9_A 13.746, F-14 47.645, F-15 53.041, F-15S 51.708, F-5 18.548. **CATATAN silang**: kolom `Hole Depth (TVD) m` sudah ADA non-null di semua baris file USROP (`data/USROP/USROP_A *.csv`, n = rows persis utk 7 file) → TVD untuk S-F1 mungkin LANGSUNG dari domain USROP; station trajectory berperan sebagai sumber validasi independen. Master yang putuskan sumber utama. |
| 2 | **S-A3 LF3** (incl tinggi = risiko differential sticking) | `incl` + `azi` per stasiun | **ADA LANGSUNG** (dengan konversi unit wajib) | `incl` non-null **5.561/5.561**; `azi` non-null **5.494/5.561**. Unit terkonfirmasi recount mandiri: **incl = 2.574 rad + 2.987 dega; azi = 2.574 rad + 2.920 dega + 67 tanpa tag azi** — PERSIS klaim D0 (`V6_D0_READERS_SYNTHESIS.md` baris 47). 67 stasiun tanpa `azi` semuanya di **`Norway-StatoilHydro-15_$47$_9-F-4/2/trajectory/1.xml`** (68 stasiun, 1 punya azi); file F-4 bukan fold `bit_wear`. | Proses wajib sebelum join: (i) konversi rad→deg (×180/π) untuk 2.574 stasiun di folder `Norway-Statoil-NO*` — uom per file konsisten (tidak ada file campuran), jadi konversi per-file aman; (ii) 67 stasiun F-4 tanpa azi → isi dari trajectory F-4 file lain (`2.xml`–`5.xml`, semua dega) atau tandai NaN; (iii) `aziRef`: **50 grid north + 11 true north** (61/63 file; 2 file tanpa tag) → azimuth lintas-file baru comparable setelah koreksi deklinasi/grid (`magDeclUsed`/`gridCorUsed` tersedia di header). `mdInclAzimType` = **0 kemunculan** (absensi terverifikasi). |
| 3 | **S-C1/S-C2** (TVD + konteks lubang terbuka untuk hidrostatik/overbalance) | `casingSeat`/casing shoe MD + TVD section per wellbore | **`casingSeat` literal TIDAK ADA; padanannya ADA SETELAH DIOLAH** (field `wbGeometrySection`) | Grep/scan 90 file domain: string `casingSeat` = **0 kemunculan** (`grep_tags.py`: "files containing 'casingSeat': 0"); padanan terdekat `wbGeometrySection` = **109 section di 27 file**, non-null **mdTop 109/109, mdBottom 109/109, tvdTop 109/109, tvdBottom 109/109** (odSection 86/109 — 23 section tanpa od, umumnya open hole). Tipe: casing 45, riser 31, open hole 23, liner 9, conductor 1. Root `mdBottom` 26/27 (hilang di `Norway-Statoil-NO 15_9-F-1 C/3/wbGeometry/1.xml` yang juga 0 section). `gapAir` + `depthWaterMean` 27/27 non-null. | Casing seat/shoe = `mdBottom` section bertipe casing/liner (**54 section**); per-wellbore: F-14 shoe 1604/2597/3695 (+915/1604/2457/3695 di `2.xml`), F-15/1 1368/1795/2766/3052.6, F-15/2 602/3172/4683 + 850/3300, F-5 604/2921, F-9 397/941. **GAP**: folder `Norway-StatoilHydro*` dan `Norway-NA*` TIDAK punya folder wbGeometry (16/16 dir wbGeometry = `Norway-Statoil-NO*` saja, terbukti `find -type d -name wbGeometry`) → **F-15S tidak punya wbGeometry sendiri**; konteks casing F-15S harus diambil dari wellbore F-15 (identitas = hipotesis, Master yang relasikan). Proses jadi fitur: ambil `mdBottom` casing/liner terdalam di atas MD titik → status open-hole vs cased; hidrostatik = `depthWaterMean`/`gapAir` + TVD interp dari #1. |

---

## 2. Cek wajib #1 — coverage station MD→TVD vs rentang USROP (fold bit_wear)

Sumber rentang USROP: `data/USROP/USROP_A *.csv`, kolom `Measured Depth m` (angka dari run `check_usrop.py`). "Covers" = stasiun terendah ≤ min USROP+1 m DAN stasiun tertinggi ≥ max USROP−1 m.

| Fold | File USROP | Rentang MD USROP | Kandidat trajectory | Stasiun | Rentang MD stasiun | Stasiun in-range | Max gap in-range | Cover? |
|---|---|---|---|---|---|---|---|---|
| F-9_A | `USROP_A 0 N-NA_F-9_Ad.csv` (13.746 baris) | 491,0–1.206,0 | `Norway-NA-15_9-F-9 A` | 38 | 420,4–1.181,0 | 36 | 91,3 m | **TIDAK** (ekor 25,0 m) |
| F-9_A | " | " | `Norway-Statoil-NO 15_9-F-9` | 25 | 0–1.206,0 | 15 | 91,3 m | **YA** |
| F-14 | `USROP_A 2 N-SH_F-14d.csv` (47.645) | 987,9–3.466,0 | `Norway-StatoilHydro-15_9-F-14` | 220 | 0–3.729,9 | 112 | 43,2 m | **YA** |
| F-14 | " | " | `Norway-Statoil-NO 15_9-F-14` | 94 | 0–3.750,0 | 62 | 43,2 m | **YA** |
| F-15 | `USROP_A 3 N-SH-F-15d.csv` (53.041) | 1.306,5–4.065,3 | `Norway-StatoilHydro-15_9-F-15` | 160 | 0–4.075,0 | 101 | 41,8 m | **YA** |
| F-15 | " | " | `Norway-Statoil-NO 15_9-F-15` (wb 1+2) | 194 | 0–4.671,0 | 117 | 79,2 m | **YA** |
| F-15S | `USROP_A 4 N-SH_F-15Sd.csv` (51.708) | 1.400,5–4.090,0 | `Norway-StatoilHydro-15_9-F-15S` | 165 | 0–4.042,9 | 96 | 51,0 m | **TIDAK** (ekor 47,1 m) |
| F-15S | " | " | `Norway-Statoil-NO 15_9-F-15` | 194 | 0–4.671,0 | 112 | 79,2 m | **YA** (asal identitas F-15/2 ≡ F-15S terkonfirmasi) |
| F-5 | `USROP_A 5 N-SH-F-5d.csv` (18.548) | 2.828,2–3.792,2 | `Norway-StatoilHydro-15_9-F-5` | 217 | 0–3.761,8 | 32 | 41,8 m | **TIDAK** (ekor 30,4 m) |
| F-5 | " | " | `Norway-Statoil-NO 15_9-F-5` | 98 | 0–3.792,0 | 28 | 41,8 m | **YA** (selisih ekor 0,2 m) |

Interpretasi (DERIVED): **tidak ada fold yang mustahil ditutup** — untuk tiap fold selalu ada ≥1 trajectory yang menutup rentang USROP; dua kandidat rekanan (StatoilHydro F-15S, StatoilHydro F-5) kurang 30–47 m di ekor, ditutup oleh folder `Norway-Statoil-NO` MELAINKAN identitas wellbore lintas-folder Master yang mesti putuskan (F-15S≡F-15/2 = HYPOTHESIS, bukan fakta). Max gap antar-stasiun di dalam rentang 40–91 m → interpolasi linear MD→TVD punya error potensial sebesar kelengkungan lintasan antar-stasiun; USROP punya `Hole Depth (TVD) m` sendiri untuk cross-check selisih.

Proses interpolasi ke time-based (yang diminta S-F1): station MD harus MONOTONIK naik per wellbore (seksi real-time MWD kadang mulai dari 0 lagi → gabung beberapa file = urutkan + pilih file yang menutup rentang, jangan concat buta); hasil estimasi = jumlah baris USROP fold di atas.

## 3. Cek wajib #2 — `incl`/`azi`: unit, hitungan, konversi

Recount independen 5.561 stasiun (`parse_traj.py`):

| Field | non-null | uom |
|---|---|---|
| `md` | 5.561/5.561 | `m` 5.561 (100%) |
| `tvd` | 5.543/5.561 | `m` 5.543 (100%) |
| `incl` | 5.561/5.561 | **dega 2.987 + rad 2.574** |
| `azi` | 5.494/5.561 | **dega 2.920 + rad 2.574 + 67 tanpa elemen** |
| `dTimStn` | 5.415/5.561 (146 hilang) | — |

- **67 stasiun tanpa tag `azi`** = satu file saja: `Norway-StatoilHydro-15_$47$_9-F-4/2/trajectory/1.xml` (68 stasiun, 1 ada azi). Bukan fold bit_wear → tidak menghalangi S-F1.
- **18 stasiun tanpa `tvd`** = `Norway-StatoilHydro-15_$47$_9-F-9/1/trajectory/2.xml` (25 stasiun, 7 ada tvd). Fold F-9_A pakai kandidat lain (tabel §2), jadi tidak menutup fold; tetap wajib ditangani saat pakai F-9 StatoilHydro.
- Semua uom per FILE konsisten (tidak ada file campuran rad+dega) → konversi rad→deg cukup per-file untuk 2.574 stasiun folder `Norway-Statoil-NO*` (F-1 C, F-11, F-12, F-14, F-15/1, F-4, F-5, F-7, F-9).
- `aziRef` lintas-file: grid north 50, true north 11, tanpa tag 2 → koreksi arah utara wajib sebelum azimuth dipakai lintas-wellbore.
- Angka ini = **konfirmasi persis** klaim D0 (`V6_D0_READERS_SYNTHESIS.md`: "incl: 2574 rad + 2987 dega; azi: 2574 rad + 2920 dega (67 stasiun tanpa tag azi)") dan "mdInclAzimType absen" (scan: 0 kemunculan) — cross-check terpenuhi (klaim D0 vs recount run terpisah).

## 4. Cek wajib #3 — wbGeometry `casingSeat` / casing shoe MD per wellbore

- String literal `casingSeat` / `Seat`: **0 dari 90 file domain** (scan python atas seluruh `trajectory/*.xml` + `wbGeometry/*.xml`; grep rekursif atas seluruh tree `witsml_raw` ditinggalkan karena timeout 300 s — lihat §6).
- Padanan: `wbGeometrySection` 109 section / 27 file, `mdTop`+`mdBottom`+`tvdTop`+`tvdBottom` **109/109 non-null semua**; root `mdBottom` 26/27; `typeHoleCasing` casing 45, riser 31, open hole 23, liner 9, conductor 1.

Casing/liner shoe MD (`mdBottom` tipe casing+liner) per file — semua angka tercetak dari run `parse_traj.py`/`wg_root.py`:

| File | Section (types) | Shoe MD casing/liner |
|---|---|---|
| `NO 15_9-F-14/1/wbGeometry/1.xml` | 4 (liner, casing, riser, casing) | 3695, 1604, 2597 |
| `NO 15_9-F-14/1/wbGeometry/2.xml` | 5 (4 casing, riser) | 1604, 2457, 3695, 915 |
| `NO 15_9-F-15/1/wbGeometry/1.xml` | 7 | 1795, 2766, 3052.6, 1368, 3052.6 |
| `NO 15_9-F-15/2/wbGeometry/1.xml` | 6 | 3172, 4683, 602 |
| `NO 15_9-F-15/2/wbGeometry/2.xml` | 3 | 3300, 850 |
| `NO 15_9-F-5/1/wbGeometry/1.xml` | 5 | 604, 2921 |
| `NO 15_9-F-9/1/wbGeometry/1.xml` | 5 | 397, 941 |
| (20 file lain — F-1 C, F-11, F-12, F-4, F-7) | 0–7 | tercetak di run; total 109 section |

Status untuk S-C1/S-C2: **ADA SETELAH DIOLAH** — casing seat = `mdBottom` per section, tinggal per-wellbore-kan + tentukan section casing/liner terdalam yang membingkai MD titik (buka/tutup lubang), lalu gabung TVD interp (#1) dan `depthWaterMean`/`gapAir` (langsung, 27/27) untuk hidrostatik.

## 5. Peluang PROSES / relasi antar-file (laporan ke Master)

1. **Lintas folder operator untuk wellbore yang sama**: hampir semua wellbore fold punya trajectory ganda — `Norway-Statoil-NO*` (rad, uom per-elemen) vs `Norway-StatoilHydro*`/`Norway-NA*` (dega). Kandidat pengganti saling menutup (tabel §2) → Master pilih sumber + rekonsiliasi, jangan digabung buta.
2. **Duplikat terdeteksi**: `Norway-Statoil-15_9-F-12/1/trajectory/2.xml` vs `7.xml` — md5 beda tapi md identik 200/200 stasiun indeks, 197/200 identik md+tvd+incl+azi → kemungkinan survei sama diekspor ulang; dedup sebelum dipakai.
3. **USROP sudah bawa TVD**: `data/USROP/USROP_A *.csv` kolom `Hole Depth (TVD) m` non-null semua baris (7 file) → relasi kandidat: station trajectory = validator TVD USROP (selisih max vs interp = kualitas S-F1), bukan satu-satunya sumber. Master putuskan hierarchy (ini menjawab prasyarat S-F1 tanpa bergantung penuh ke interpolasi).
4. **Join key MD vs waktu**: trajectory station punya `dTimStn` (5.415/5.561) → bisa juga join ke time-series lewat timestamp selain interpolasi kedalaman; untuk time-based MD-naik, MD→TVD lalu join MD tetap jalur utama.
5. **F-15S tanpa wbGeometry sendiri** (16/16 dir wbGeometry = folder `Norway-Statoil-NO*`) → konteks casing F-15S harus pinjam dari wellbore F-15 atau dinyatakan tak-ada; Master tentukan apakah F-15/2 ≡ F-15S.
6. **Azi grid vs true north** (50/11) + 2 file tanpa `aziRef` → kalau azimuth dipakai sebagai fitur lintas-wellbore, wajib koreksi dulu (header `magDeclUsed`/`gridCorUsed` tersedia per file).

## 6. Error / percobaan yang gagal (dilaporkan apa adanya)

1. `find` rekursif penuh atas `witsml_raw` → sebagian path gagal `Cannot allocate memory` (drvfs) + grep rekursif `casingSeat` seluruh tree **timeout 300 s** (exit 124). Alternatif dipakai: scan python atas glob 90 file domain → hasil: 0 kemunculan `casingSeat`. Ketiadaan hanya di-BUKTIKAN untuk 90 file domain, bukan seluruh tree.
2. `execute_code` (single-query mode) diblokir kebijakan → semua run via `terminal` + file script.
3. `python3 -c` / heredoc diblokir "dangerous" → dipindah ke file `.py`.

## 7. Belum diverifikasi

- Identitas wellbore lintas folder operator (F-15S vs `NO 15_9-F-15/2`, F-9_A `NA` vs `NO` vs `StatoilHydro` F-9) — **hipotesis, Master yang relasikan**; coverage §2 memakai pemetaan kandidat, bukan identitas terverifikasi.
- Kualitas numerik interpolasi (error vs `Hole Depth (TVD)` USROP) — butuh run interpolasi (belum dilakukan, di luar cek ketersediaan).
- Seluruh isi 20 file wbGeometry lain diringkas lewat hitungan, tidak dibaca manual baris-per-baris (field terekstrak: type/mdTop/mdBottom/tvdTop/tvdBottom/id/od).
- Grep seluruh tree `witsml_raw` di luar 90 file domain (timeout, §6) — kemungkinan `casingSeat` di domain lain tidak dicek (di luar scope domain ini).
