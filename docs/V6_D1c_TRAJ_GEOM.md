# V6-D1c — WITSML TRAJECTORY + WBGEOMETRY (Ekstraksi Lengkap)

**Riset pendahuluan: `verification-mandatory` — verifikasi ulang 2026-10-11 dengan grep (berbeda dari parser ElementTree penulis): `incl` = 2574 rad + 2987 dega; `azi` = 2574 rad + 2920 dega (total tag `<azi>` 5494; 67 stasiun tanpa tag azi) — dipakai untuk §2.**

Status: DONE
Tanggal: 2026-10-10
Sumber: `/mnt/d/Capstone 1/data/volve/witsml_raw/*/*/trajectory/*.xml` (63 file) + `*/*/wbGeometry/*.xml` (27 file)
Output CSV:
- `/mnt/d/Capstone 1/scratch/v6_d1c_trajectory.csv` (5561 baris survey station)
- `/mnt/d/Capstone 1/scratch/v6_d1c_wbgeom.csv` (109 baris wbGeometrySection)
- `/mnt/d/Capstone 1/scratch/v6_d1c_traj_summary.csv` (29 wellbore ringkas)
- `/mnt/d/Capstone 1/scratch/v6_d1c_tvd_coverage.json` (cakupan koreksi TVD time-based)

Parser: `/home/neonti/.hermes/kanban/boards/capstone-v6-solve/workspaces/t_315c30b1/parse_traj_geom.py` + `analyze_traj.py` + `tvd_coverage.py`
Parse errors: 0

## 1. Angka nyata (verified)

- 63 file trajectory -> **5561 survey station**, 0 error parse
- 27 file wbGeometry -> **109 wbGeometrySection**, 0 error parse
- **29 wellbore punya trajectory** (F-1, F-1 A, F-1 B, F-1 C, F-4, F-5, F-7, F-9, F-9 A, F-10, F-11, F-11 A, F-11 B, F-11 T2, F-12, F-14, F-15, F-15A/B/C/D/S) — catatan: WITSML punya 2 set nama wellbore per well (legacy "NO 15/9-X" dari folder Statoil + "15/9-X - Main Wellbore" dari folder StatoilHydro); keduanya dihitung terpisah di summary, isinya survey run berbeda.
- **16 wellbore punya wbGeometry**; tipe section: casing 45, open hole 23, riser 31, liner 9, conductor 1

## 2. Format data — PENTING (ditemukan saat baca raw)

- `incl` dan `azi` disimpan dengan uom campuran (dari 5561 station): **`incl` = 2574 uom="rad" + 2987 uom="dega"; `azi` = 2574 uom="rad" + 2920 uom="dega"** — jumlah tag `<azi>` hanya 5494, jadi **67 station tidak punya tag `azi`** (koreksi A1 §8b-4; klaim lama "2574 rad + 2987 dega" untuk incl DAN azi hanya benar untuk incl). Parser mengonversi per-elemen (rad->deg; dega diteruskan apa adanya). Verifikasi sampel: file StatoilHydro (F-1 dkk) memakai "dega", file Statoil (F-1 C dkk) memakai "rad" — konfirmasi kedua kasus plausible (0-180 deg / 0-pi rad).
- `md`, `tvd`, `dispNs`, `dispEw`, `vertSect` uom="m".
- `mdInclAzimType`: **ABSENT di semua 63 file** (tidak ditulis sama sekali). Acuan arah ada di `aziRef`: **grid north 50, true north 11** — dominan grid north, jadi azimuth perlu grid correction sebelum dipakai bareng north-referenced data lain. `stnGridCorUsed` di `corUsed` memberi nilai grid correction-nya.
- `typeTrajStation`: "tie in point", "gyro north seeking", "magnetic MWD", "magnetic multishot", dll.
- wbGeometrySection: `typeHoleCasing` ∈ {casing, liner, riser, open hole, conductor}; `odSection`/`idSection` uom = **meter** (mis. od 0.2445 m = 9-5/8 in).

## 3. Contoh 3 survey station (raw, F-14 `NO 15/9-F-14/1/trajectory/1.xml`)

```
Station 1: uid=6VFNI35_TIE_POINT  type=tie in point            md=0.0      tvd=0.0      incl=0.0deg   azi=0.0deg
Station 2: uid=93VG4D36           type=gyro north seeking      md=145.90   tvd=145.90   incl=0.0deg   azi=0.0deg    tool=gyroscopic north seeking
Station 3: uid=94VG4D36           type=gyro north seeking      md=155.09   tvd=155.09   incl=0.18deg  azi=5.42deg   tool=gyroscopic north seeking
```
Raw XML snippet station 3:
`<md uom="m">155.089996337891</md><tvd uom="m">155.089981220949</tvd><incl uom="rad">0.00314159277859448</incl><azi uom="rad">0.0945968467947622</azi>`

## 4. Deviasi well (selisih MD - TVD pada kedalaman maks)

Sesuai ekspektasi: well horizontal/deviated punya selisih besar. Lihat tabel penuh di `v6_d1c_traj_summary.csv`. Top deviasi:

| wellbore | n_station | md_max (m) | tvd_last (m) | MD-TVD (m) | max incl (deg) |
|---|---|---|---|---|---|
| 15/9-F-10 - Main Wellbore | 726 | 5300.1 | 2999.1 | **2301.0** | 88.1 |
| NO 15/9-F-11 B | 854 | 4770.0 | 3257.3 | **1512.7** | 90.0 |
| NO 15/9-F-15 D | 114 | 4671.0 | 3209.8 | **1461.2** | 82.0 |
| NO 15/9-F-11 T2 | 133 | 4547.6 | 3384.3 | **1163.3** | 82.1 |
| NO 15/9-F-1 C | 218 | 4094.0 | 3180.5 | **913.5** | 84.1 |
| 15/9-F-15S - Main Wellbore | 165 | 4042.9 | 3138.1 | **904.8** | 67.6 |
| 15/9-F-15 - Main Wellbore | 160 | 4075.0 | 3196.9 | **878.1** | 85.8 |
| NO 15/9-F-14 | 94 | 3750.0 | 3158.7 | **591.3** | 81.1 |
| 15/9-F-14 - Main Wellbore | 220 | 3729.9 | 3145.8 | **584.1** | 81.1 |
| 15/9-F-5 - Main Wellbore | 217 | 3761.8 | 3228.1 | **533.7** | 55.1 |
| 15/9-F-9 - Main Wellbore | 42 | 1048.9 | 1042.1 | 6.7 | 11.6 |
| NO 15/9-F-7 | 42 | 1083.0 | 1077.5 | 5.5 | 9.5 |

Catatan koreksi atas asumsi tugas: F-14 memang deviated berat (584-591 m selisih, max incl 81 deg) tapi **bukan horizontal** — profil build-and-hold. Kandidat horizontal sesungguhnya: **F-10 (2301 m selisih, 88 deg), F-11 B (90 deg), F-15 D (1461 m, 82 deg), F-1 C, F-11 T2**. F-7/F-9/F-1 vertikal dangkal (selisih <7 m).

TVD tersedia di **semua** station kecuali 18 station pada "15/9-F-9 - Main Wellbore" (24/42 station punya tvd).

## 5. Casing shoe (dari wbGeometry, contoh utama)

| wellbore | liner shoe (m) | casing shoe (m) | od |
|---|---|---|---|
| F-14 | 2597-3695 | 20-1604, 1604-2597 | 7in liner, 9-5/8in casing |
| F-11 B | 3094-4767 | 616-3094 | 7in liner, 9-5/8in casing |
| F-5 | - | 317-604, 604-2921 | 10-3/4in, 9-5/8in |
| F-12 | - | 146-1600, 900-3520, 1600-3520 | 10-3/4in, 9-5/8in |
| F-1 C | 2927-4087 | - | 7in liner |
| F-15 D | 850-3300, 3172-4683 | - | 9-5/8in + 7in liner |

## 6. Kaitan ke kebutuhan: koreksi TVD time-based

Time-based WITSML hasil parse sebelumnya (`witsml_parsed/*.csv`, 8 wellbore, total 7.080.457 baris) semuanya punya trajectory dengan TVD di range MD yang sama -> MD->TVD bisa dikoreksi dengan nearest-survey interpolation.

| file | wellbore | baris | dengan DBTM(MD) | bisa dikoreksi ke TVD | % benar |
|---|---|---|---|---|---|
| F-14.csv | 15/9-F-14 - Main Wellbore | 1.648.026 | 1.597.523 | 1.587.487 | 96,3% |
| F-15A.csv | 15/9-F-15 - Main Wellbore | 778.162 | 231.222 | 226.838 | 29,1% |
| F-15_S.csv | 15/9-F-15S - Main Wellbore | 1.883.062 | 1.690.737 | 1.662.147 | 88,3% |
| F-5.csv | 15/9-F-5 - Main Wellbore | 1.286.967 | 1.138.226 | 1.117.584 | 86,8% |
| F-7.csv | 15/9-F-7 - Main Wellbore | 547.500 | 547.291 | 524.805 | 95,9% |
| F-9.csv | 15/9-F-9 - Main Wellbore | 457.545 | 447.032 | 426.414 | 93,2% |
| F-9_A.csv | 15/9-F-9 A - Main Wellbore | 419.706 | 85.055 | 64.243 | 15,3% |
| VAR_F-5_alt.csv | 15/9-F-5 - Main Wellbore | 59.489 | 59.487 | 59.487 | 100,0% |
| **TOTAL** | | **7.080.457** | **5.796.573** | **5.669.005** | **80,1%** |

Kriteria "bisa dikoreksi": baris punya DBTM (MD, meter) yang berada di dalam [md_min, md_max] trajectory wellbore-nya dan trajectory punya TVD. Baris tanpa DBTM atau di luar range survey (mis. F-9_A hanya survey 420-1181 m sementara log mencakup kedalaman lain) tidak bisa dikoreksi nearest-survey tanpa extrapolasi.

## 7. Hasil scan koreksi TVD

Scan penuh (7 juta baris, DBTM per baris diverifikasi against range survey): `/mnt/d/Capstone 1/scratch/v6_d1c_tvd_coverage.json`. Total 5.669.005 baris (80,1% dari seluruh time-based) siap dikoreksi MD->TVD dengan asumsi nearest-survey / minimum-curvature interpolation.

## 8. Implikasi untuk model (ECD, buckling, pore pressure)

- ECD/pore pressure: hidrostatik = MW*g*TVD, bukan MD. Untuk F-14 (MD 3730, TVD 3146), pakai MD salah ~16%; untuk F-10 (MD 5300, TVD 2999) salah ~43%. Koreksi TVD wajib sebelum fitur pressure.
- Buckling: weight-on-bit / drag dihitung di MD, tapi gravitational load component butuh inkl/dogleg dari survey — survey lengkap tersedia (5561 stasiun, dls + rateBuild + rateTurn ada di XML).
- Asumsi nearest-survey aman: spacing survey rata-rata ~10-60 m; di zona build (incl berubah cepat) pakai minimum-curvature lebih baik — tersedia dari md/tvd/incl/azi per stasiun.

## 9. Metodologi verifikasi

- Cek jumlah file: `find` = 63 + 27 (persis seperti spek tugas).
- Raw print 3 file: F-14 trajectory (incl/azi = rad, terverifikasi dari uom), F-14 wbGeometry, plus grep mdInclAzimType.
- Parse: ElementTree namespace-agnostic, 0 error, row count = jumlah `<trajectoryStation>` di 63 file.
