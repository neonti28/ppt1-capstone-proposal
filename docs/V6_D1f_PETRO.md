# V6-D1f — Pembukaan & ekstraksi PETROPHYSICS DLIS/LIS (spwla_volve_logs)

**Task kanban:** `t_f5506e30` · **Tanggal:** 2026-10-10 · **Status:** 21 dari 24 file log berhasil diekstrak penuh ke CSV; **1 file (F-7 .LIS) gagal dibuka — blocker nyata, error asli dicatat §4.2.**

**Riset pendahuluan: `terminal` + dokumentasi resmi dlisio (readthedocs/README) — klaim apa pun di dokumen ini punya angka dari tool output, bukan perkiraan.**
**Riset pendahuluan (verifikasi ulang 2026-10-11): `verification-mandatory` — jumlah CSV ekstraksi diverifikasi ulang dengan glob (tool berbeda dari dlisio parser penulis): 21 file CSV, cocok dengan klaim §0.**

---

## 0. Ringkasan eksekutif

| Item | Angka nyata (terverifikasi dari tool) |
|---|---|
| Library `dlisio` | **ADA** — versi **1.0.4** (Python 3.14.7) — tidak perlu install |
| Library `lasio` | **ADA** — versi **0.32** |
| File di `spwla_volve_logs` (log saja) | **24 file = 20 `.DLIS` + 2 `.LIS` + 2 `.LAS`** (klawifikasi task "16 DLIS" salah — lihat §2) |
| DLIS berhasil dibuka | **20/20 file, 20 logical file, 504 channel, 291.270 baris** |
| LIS berhasil dibuka | **1/2** — F-14 LIS sukses (**18.374 baris × 49 channel**); **F-7 LIS gagal (korup, 0 channel)** |
| Total baris terekstrak | **309.644 baris** di **21 file CSV** (77 MB) di `/mnt/d/Capstone 1/scratch/v6_d1f/csv/` |
| Sumur tercakup petrophysics | **9 sumur: F-5, F-7 (kosong), F-9, F-9A, F-14, F-15, F-15A, F-15B, F-15C, F-15D** |
| Sumur BARU (petrophysics tanpa WITSML parsed) | **F-15, F-15B, F-15C, F-15D** (§7) |
| Kanal petrofisika kunci tersedia | RHOB, TNPH/NPHI, BPHI, PEF, DTCO/DT/DTSM, GR/GRAF, CALI, **SW, BVW, VSH** (COMPUTED_OUTPUT), resistivity array (A16H–A40H, P16L–P40L) (§5) |

---

## 1. Pemeriksaan library (tugas wajib no.1)

Output asli (`check_libs.py`):

```
dlisio: OK version=1.0.4  path=.../site-packages/dlisio/__init__.py
lasio:  OK version=0.32   path=.../site-packages/lasio/__init__.py
pandas: OK version=2.3.3
numpy:  OK version=2.5.3
python: 3.14.7
```

→ Tidak ada install; **dlisio ternyata membaca LIS79 juga** (modul `dlisio.lis`), bukan hanya DLIS — README dlisio: "reading well logs in Digital Log Interchange Standard (DLIS V1), also known as RP66 V1, **and Log Information Standard 79 (LIS79)**".

**Catatan API penting (bug versi):** `dlisio.lis.curves()` pada dlisio 1.0.4 + numpy 2.5 **crash** dengan `ValueError: cannot resize an array that may be referenced by another object` (pembaca Rust memanggil `ndarray.resize()` dengan `refcheck=True`). Workaround teruji: kembalikan subclass numpy yang override `resize(refcheck=False)` — lihat §4.1. `dlisio.dlis.load()` (file DLIS) tidak terdampak.

---

## 2. Inventaris file NYATA (buka dulu filenya)

`ls` + pembacaan magic bytes (64 byte pertama) — semua file DLIS punya signature teks `   1V1.00RECORD08192PETROLOG` (RECORD 8192 byte, ditulis perangkat PETROLOG), kedua file LIS punya header biner non-standar (`00...90...84` + teks `EDIT`).

| # | File | Ukuran | Magic / identifikasi |
|---|---|---:|---|
| 1 | `15_9-F-5__WLC_PETROPHYSICAL_COMPOSITE_1.DLIS` | 4.803.134 | `1V1.00RECORD08192PETROLOG` → DLIS v1 |
| 2 | `15_9-F-5__WLC_PETRO_COMPUTED_INPUT_1.DLIS` | 1.120.684 | idem |
| 3 | `15_9-F-5__WLC_PETRO_COMPUTED_OUTPUT_1.DLIS` | 1.120.800 | idem |
| 4 | `15_9-F-7__WLC_PETROPHYSICAL_COMPOSITE_1.LIS` | 524.753 | biner → **LIS79, korup (§4.2)** |
| 5 | `15_9-F-9A__WLC_PETROPHYSICAL_COMPOSITE_1.DLIS` | 429.384 | DLIS v1 |
| 6 | `15_9-F-9__WLC_PETROPHYSICAL_COMPOSITE_1.DLIS` | 97.678 | DLIS v1 |
| 7 | `15_9-F14__WLC_PETROPHYSICAL_COMPOSITE_1.LIS` | 3.677.190 | biner → **LIS79, terbaca (§4.1)** |
| 8 | `15_9-F14__WLC_PETRO_COMPUTED_INPUT_1.DLIS` | 1.285.000 | DLIS v1 |
| 9 | `15_9-F14__WLC_PETRO_COMPUTED_OUTPUT_1.DLIS` | 908.852 | DLIS v1 |
| 10–12 | `15_9-F15A__…(COMPOSITE_2 / INPUT / OUTPUT)` | 3.506.640 / 1.697.846 / 451.090 | DLIS v1 |
| 13–15 | `15_9-F15B__…(COMPOSITE_1 / INPUT / OUTPUT)` | 1.243.316 / 113.806 / 71.594 | DLIS v1 |
| 16–18 | `15_9-F15C__…(COMPOSITE_1 / INPUT / OUTPUT)` | 1.109.726 / 254.308 / 135.754 | DLIS v1 |
| 19 | `15_9-F15D__WLC_PETROPHYSICAL_COMPOSITE_2.DLIS` | 10.961.480 | DLIS v1 |
| 20 | `15_9-F15D__WLC_PETRO_COMPUTED_INPUT_1.LAS` | 15.255.718 | `~Version Information.VERS` → **LAS 2.0 (sudah dipakai V6-R1)** |
| 21 | `15_9-F15D__WLC_PETRO_COMPUTED_OUTPUT_1.LAS` | 1.759.612 | LAS 2.0 (sudah dipakai V6-R1) |
| 22–24 | `15_9-F15__…(COMPOSITE_2 / INPUT / OUTPUT)` | 6.487.888 / 1.903.424 / 455.460 | DLIS v1 |

Non-log (tidak diekstrak): `15_9-F-5__PETROPHYSICAL_REPORT_1.PDF` (189 KB), `VOLVE_INVENTORY.xlsx`, `Well_picks_Volve_v1.dat`, `Readme.md`.

→ **Koreksi fakta:** yang tertulis "16 file DLIS" di body task adalah **20 file DLIS**; total 24 file log tetap benar (20 DLIS + 2 LIS + 2 LAS).

---

## 3. Hasil ekstraksi DLIS (20/20 sukses)

Semua DLIS: 1 logical file per file, 1 frame, index `DEPTH` (kecuali F-15B/F-15C pakai `DEPT`). **Satuan kedalaman mayoritas `0.1 in` (persepuluh inci) — bukan meter**; konversi ke meter = nilai × 0,00254. F-15D memakai satuan `mm` (÷ 1000). Sampling 60 (0.1 in) = 15,24 cm; F-15D 100 mm = 10 cm.

| Sumur | File | Baris | Channel | Kedalaman (satuan asli) | **Kedalaman (m)** |
|---|---|---:|---:|---|---|
| F-5 | PETROPHYSICAL_COMPOSITE_1 | 23.657 | 48 | 74.760 … 1.494.120 (0.1 in) | **189,9 … 3.795,1** |
| F-5 | PETRO_COMPUTED_INPUT_1 | 22.120 | 10 | 165.840 … 1.492.980 | **421,2 … 3.792,2** |
| F-5 | PETRO_COMPUTED_OUTPUT_1 | 22.120 | 10 | idem | 421,2 … 3.792,2 |
| F-9 | PETROPHYSICAL_COMPOSITE_1 | 1.204 | 17 | 354.240 … 426.420 | **899,8 … 1.083,1** |
| F-9A | PETROPHYSICAL_COMPOSITE_1 | 5.188 | 18 | 163.500 … 474.720 | **415,3 … 1.205,8** |
| F-14 | PETRO_COMPUTED_INPUT_1 | 23.474 | 11 | 67.920 … 1.476.300 | **172,5 … 3.749,8** |
| F-14 | PETRO_COMPUTED_OUTPUT_1 | 23.474 | 7 | idem | 172,5 … 3.749,8 |
| F-15 | PETROPHYSICAL_COMPOSITE_2 | 25.418 | 61 | 85.260 … 1.610.280 | **216,6 … 4.090,1** |
| F-15 | PETRO_COMPUTED_INPUT_1 | 26.838 | 15 | 0 … 1.610.220 | 0,0 … 4.090,0 |
| F-15 | PETRO_COMPUTED_OUTPUT_1 | 9.850 | 9 | 1.019.280 … 1.610.220 | 2.589,0 … 4.090,0 |
| F-15A | PETROPHYSICAL_COMPOSITE_2 | 18.016 | 46 | 531.480 … 1.612.380 | **1.350,0 … 4.095,4** |
| F-15A | PETRO_COMPUTED_INPUT_1 | 25.389 | 14 | 85.380 … 1.608.660 | 216,9 … 4.086,0 |
| F-15A | PETRO_COMPUTED_OUTPUT_1 | 9.757 | 9 | 1.027.020 … 1.612.380 | 2.608,6 … 4.095,4 |
| F-15B | PETROPHYSICAL_COMPOSITE_1 | 5.888 | 50 | 1.023.720 … 1.376.940 | **2.600,2 … 3.497,4** |
| F-15B | PETRO_COMPUTED_INPUT_1 | 2.236 | 10 | 1.238.940 … 1.373.040 | 3.146,9 … 3.487,5 |
| F-15B | PETRO_COMPUTED_OUTPUT_1 | 1.514 | 9 | 1.290.300 … 1.381.080 | 3.277,4 … 3.507,9 |
| F-15C | PETROPHYSICAL_COMPOSITE_1 | 4.409 | 60 | 1.007.880 … 1.272.360 | **2.560,0 … 3.231,8** |
| F-15C | PETRO_COMPUTED_INPUT_1 | 4.346 | 12 | 1.007.880 … 1.268.580 | 2.560,0 … 3.222,2 |
| F-15C | PETRO_COMPUTED_OUTPUT_1 | 2.908 | 9 | 1.098.000 … 1.272.420 | 2.788,9 … 3.231,9 |
| F-15D | PETROPHYSICAL_COMPOSITE_2 | 33.464 | 79 | 1.339.200 … 4.685.500 (**mm**) | **1.339,2 … 4.685,5** |
| **F-7** | **LIS — GAGAL** | **0** | **0** | — | — |
| F-14 | **LIS** (via workaround) | **18.374** | **49** | 1.000,05 … 3.800,09 (M) | **1.000,0 … 3.800,1** |

**TOTAL: 309.644 baris, 21 CSV.** Nilai kedalaman di atas konsisten dengan TD Volve yang dipublikasikan (mis. F-5 ≈ 3.795 m, F-15A ≈ 4.095 m) — konversi satuan divalidasi silang, bukan asumsi.

**Sentinel null DLIS = -999,25** dipakai konsisten; jumlah baris dengan nilai ≤ -999 per kanal tersimpan di JSON bukti (`v6_d1f_dlis_summary.json`, kunci `rows_with_null_lt_-999`).

### 3.1 Inventaris kanal petrofisika (valid/total baris, sentinel -999,25 dibuang)

| CSV | RHOB | TNPH/NPHI/BPHI | PEF | DTCO/DT | GR | CALI | **SW / BVW / VSH** | Resistivity |
|---|---|---|---|---|---|---|---|---|
| F-5 COMPOSITE | 5.664/23.657 | 5.640 | 5.664 | 5.565 | — | — | — | A40H 15.523, P40L 15.523 |
| F-5 INPUT | 6.317/22.120 | 6.317 | — | — | 22.120 | 3.503 | — | RT 22.120 |
| F-5 OUTPUT | — | — | — | — | — | — | **3.331 / 3.331 / 3.510** | — |
| F-9 COMPOSITE | — | — | — | — | — | — | — | A40H 1.168, P40L 1.168 |
| F-9A COMPOSITE | — | — | — | — | — | — | — | A40H 1.448, P40L 1.360 |
| F-14 LIS | 6.305/18.374 | 6.285 | 6.305 | DTCO 16.931, DTSM 5.504 | GRAF 7.821 | — | — | A40H 17.215 |
| F-14 INPUT | 6.305/23.474 | 6.286 | 6.305 | — | 23.408 | — | — | RT 17.710 |
| F-14 OUTPUT | — | — | — | — | — | — | **5.693 / 5.693 / 5.693** | — |
| F-15 COMPOSITE | 10.188/25.418 | 10.166 | 10.188 | 10.016 | — | — | — | A40H 7.557 |
| F-15 INPUT | 26.838/26.838 | 26.838 | 23.788 | — | 25.815 | 23.787 | — | RT 17.876 |
| F-15 OUTPUT | — | — | — | — | — | — | **9.764 / 9.764 / 9.849** | — |
| F-15A COMPOSITE | 10.071/18.016 | 10.045 | 10.071 | 9.366 | — | — | — | A40H 17.796 |
| F-15A INPUT | 9.906/25.389 | 9.880 | 9.906 | — | 25.353 | 9.905 | — | RT 17.905 |
| F-15A OUTPUT | — | — | — | — | — | — | **9.676 / 9.676 / 9.668** | — |
| F-15B COMPOSITE | 2.039/5.888 | 2.021 | 2.039 | 2.089 | — | — | — | (A/P-array tidak ada) |
| F-15B INPUT | 2.044/2.236 | 2.028 | — | 2.132 (DT) | 2.052 | 2.044 | — | RT 2.034 |
| F-15B OUTPUT | — | — | — | — | — | — | **1.356 / 1.356 / 1.356** | — |
| F-15C COMPOSITE | 2.041/4.409 | 2.020 | 2.041 | 2.370 | — | — | — | A40H 4.244 |
| F-15C INPUT | 2.041/4.346 | 2.021 | — | — | 4.283 | 2.040 | — | RT 4.265 |
| F-15C OUTPUT | — | — | — | — | — | — | **2.019 / 2.020 / 2.024** | — |
| F-15D COMPOSITE | *(tidak ada RHOB; lihat §3.3)* | | | | | | | |
| F-15 OUTPUT (LAS, sudah dipakai V6-R1) | — | — | — | — | — | — | SW/BVW/VSH | — |

Tambahan kanal turunan di semua COMPUTED_OUTPUT: **`CARB_FLAG`, `COAL_FLAG`** (flag litologi biner, contoh F-15: 9.849 dan 9.301 baris valid) — kandidat label litologi siap pakai.

### 3.2 Contoh 3 channel berisi per file (angka asli dari CSV)

| File | Kanal | Valid | min / median / max | 3 nilai pertama |
|---|---|---:|---|---|
| F-5 COMPOSITE | A16H (Ωm) | 15.523 (65,6%) | 0,1 / 1,117 / 200 | 0,5324 · 0,5410 · 0,5539 |
| F-5 INPUT | CALI (in) | 3.503 (15,8%) | 8,25 / 8,50 / 8,808 | 8,25 · 8,25 · 8,25 |
| F-5 OUTPUT | BVW | 3.331 (15,1%) | 0,001 / 0,0609 / 0,2045 | 0,0361 · 0,0300 · 0,0243 |
| F-9 COMPOSITE | A28H (Ωm) | 1.168 (97,0%) | 0,1 / 0,8159 / 500 | 0,1792 · 0,5505 · 0,2728 |
| F-9A COMPOSITE | A28H | 1.448 (27,9%) | 0,1 / 0,8864 / 30,3 | 0,1 · 0,1 · 0,1249 |
| **F-14 LIS** | A16H | 17.215 (93,7%) | 0,1 / 0,6326 / 5.000 | 0,1 · 0,1 · 0,1 |
| F-14 INPUT | DRHO (g/cm³) | 6.305 (26,9%) | −2,264 / 0,0283 / 0,4886 | −0,8831 · −1,0092 · −1,0406 |
| F-14 OUTPUT | BVW | 5.693 (24,3%) | 0,001 / 0,0374 / 1 | 0,0345 · 0,0349 · 0,0355 |
| F-15 COMPOSITE | A28H | 7.557 (29,7%) | 0,1 / 0,8468 / 14,63 | 0,3444 · 0,3408 · 0,3371 |
| F-15 INPUT | CALI | 23.787 (88,6%) | 8,307 / 8,88 / 9,958 | 8,88 · 8,88 · 8,88 |
| F-15 OUTPUT | BVW | 9.764 (99,1%) | 0,001 / 0,0732 / 1 | 0,1902 · 0,1955 · 0,1997 |
| F-15A COMPOSITE | A28H | 17.796 (98,8%) | 0,1 / 0,8658 / 200 | 0,3682 · 0,3684 · 0,3377 |
| F-15A INPUT | CALI | 9.905 (39,0%) | 8,25 / 8,485 / 9,786 | 8,25 · 8,25 · 8,25 |
| F-15A OUTPUT | BVW | 9.676 (99,2%) | 0,0014 / 0,0755 / 0,3145 | 0,1491 · 0,1518 · 0,1575 |
| F-15B COMPOSITE | CRPM (rpm) | 2.039 (34,6%) | 98,1 / 129,7 / 200,4 | 144,6 · 116,2 · 112,6 |
| F-15B INPUT | DT (µs/ft) | 2.132 (95,4%) | 53,12 / 73,3 / 104,9 | 56,97 · 56,75 · 57,35 |
| F-15B OUTPUT | BVW | 1.356 (89,6%) | 0,0018 / 0,0814 / 0,2612 | 0,0339 · 0,0345 · 0,0294 |
| F-15C COMPOSITE | A28H | 4.244 (96,3%) | 0,1 / 1,885 / 25,04 | 0,1969 · 0,1918 · 0,1772 |
| F-15C INPUT | CALI | 2.040 (46,9%) | 8,506 / 8,745 / 9,713 | 8,728 · 8,586 · 8,774 |
| F-15C OUTPUT | BVW | 2.020 (69,5%) | 0,001 / 0,06895 / 1 | 1,0 · 0,0097 · 1,0 |
| F-15D COMPOSITE | ABDC01M (array sonic, dB) | 13.552 (40,5%) | −4,539 / 2,341 / 4,831 | 2,585 · 2,544 · 2,576 |

### 3.3 F-15D COMPOSITE BUKAN suite porositas biasa

79 kanal F-15D = **array sonic / dipole + GR & koreksi**, bukan RHOB/NPHI/SW: `ABDC01M–ABDC16M` + `ABDCQF01–04` (amplitudo array sonic), `APRA01M–APRA16M` (slowness array), `RACEH/RACEL/RPCEH/RPCELM` (resistivity deep/shallow), `GRAFM/GRCFM/NBGRCFM` (GR), `CALCM`, `DPEFM`, `DRHFM`, `TCDM`, `RPTHM`, **`ROPAVG`, `WOBAVG`**. Porositas/VSH/Sw F-15D memang ada di 2 file **LAS** (INPUT/OUTPUT) yang sudah dipakai V6-R1 — jadi F-15D lengkap, hanya sumbernya beda file.

---

## 4. Hasil ekstraksi LIS79 (1 sukses, 1 gagal)

### 4.1 F-14 — SUKSES via workaround numpy2 (18.374 × 49)

Urutan percobaan (semua nyata):
1. `dlisio.dlis.load(LIS)` → `RuntimeError: file corrupt: head.prev (= 362) != prev(prev(head)).next (= 288)` — memang salah API (ini file LIS, bukan DLIS).
2. `dlisio.lis.load()` default → `RuntimeError: file corrupt: head.prev (= 457) != …` (handler default menaikkan error).
3. `dlisio.lis.load(path, ErrorHandler(critical=custom))` → **F-14 terindeks bersih, 0 log error**; F-7: 1 log critical, indexing berhenti di offset 461.
4. `dlisio.lis.curves(lf, dfsr)` → `ValueError: cannot resize an array that may be referenced by another object` (bug dlisio 1.0.4 × numpy 2.5, terjadi setelah 4x resize: 3675→7350→14700→29400→18374).
5. **Workaround:** subclass `np.ndarray` dengan `resize(*a, **kw): kw['refcheck']=False` → **berhasil, shape (18374,) dengan 49 kanal**.

Kanal F-14 LIS (49): `DEPT, A16H, A22H, A28H, A34H, A40H, BPHI, CRPM, DRHB, DRHL, DRHO, DRHR, DRHU, DTCO, DTRP, DTTP, DTRS, DTSM, DTTS, GRAF, GRA, GRMA, P16H, P16L, P22H, P22L, P28H, P28L, P34H, P34L, P40H, P40L, PEB, PEF, PEL, PER, PEU, RHOB, ROBB, ROBL, ROBR, ROBU, ROP5, TABA, TNPH, UCAV, UCHO, UCVE, VPVS`.
Kedalaman 1.000,05 … 3.800,09 **meter** (satuan `M`), 93,7% kanal resistivity berisi, RHOB 6.305 sampel, DTCO 16.931, DTSM 5.504, GRAF 7.821.
File CSV: `/mnt/d/Capstone 1/scratch/v6_d1f/csv/15_9-F14__WLC_PETROPHYSICAL_COMPOSITE_1__lislf0_dfsr0.csv`.

> Catatan pemakaian: LIS F-14 **bertindih wellbore dengan DLIS F-14** (INPUT/OUTPUT), tapi LIS = *composite* (suite resistivity array + sonic + density + GR dalam satu logset), sedangkan DLIS F-14 hanya INPUT/OUTPUT (computed). Jadi LIS F-14 menambah **suite mentah** yang tidak ada di DLIS F-14.

### 4.2 F-7 — GAGAL (blocker nyata, dicatat apa adanya)

Pesan error ASLI (severity critical, dari `dlisio.lis.load`):

```
Problem:      file corrupt: head.prev (= 457) != prev(prev(head)).next (= 362). Assigning expected .next value to .prev
Where:        dlisio.lis.load: file /mnt/d/Capstone 1/data/volve/external/spwla_volve_logs/15_9-F-7__WLC_PETROPHYSICAL_COMPOSITE_1.LIS
Severity:     critical
Action taken: Indexing stopped at physical tell 461 (dec)
```

Upaya pemulihan yang sudah dicoba (semua gagal → **0 DFSR, 0 channel**):
- `ErrorHandler(critical=LOG/SWALLOW)` → mengembalikan 1 logical file tanpa DFSR (metadata only).
- **Pemindaian offset geser bit:** memotong file pada offset 0…204.800 (step 128 byte) lalu load tiap potongan → **tidak satu pun offset menghasilkan DFSR** (1600-an load; daftar di `v6_d1f_lis_summary.json`, kunci `slice_scan`).
- Interpretasi: kerusakan rantai header di awal file (offset ~457) membuat seluruh byte sesudahnya tidak terindeks — sesuai dokumentasi dlisio: "because of how the internal structure of LIS files is defined, the bytes following the incorrect part become unreadable too".

**Konsekuensi:** F-7 tetap punya WITSML parsed (`data/volve/witsml_parsed/F-7.csv`, 190 MB) sehingga data drilling F-7 tidak hilang; yang hilang hanya petrophysics LIS F-7. Kalau petrophysics F-7 dibutuhkan, jalur pemulihan realistis = cari sumber ulang (mis. DLIS/SPWLA re-download) — bukan parser.

---

## 5. LAS (tugas wajib no.4) — tidak diulang

2 file LAS (`15_9-F15D__WLC_PETRO_COMPUTED_INPUT_1.LAS` 15,3 MB + `_OUTPUT_1.LAS` 1,76 MB) **sudah dibuka & dipakai V6-R1** untuk label turunan (§ Uji 5 `V6_R1_SCIENCE.md`: 45.391 + 12.198 sampel kedalaman; VSH>0,4 → 3.310 kelas; SAND_FLAG → 8.893). Magic bytes hari ini konsisten (`~Version Information.VERS`, LAS 2.0). **Tidak diekstrak ulang** — hanya dicatat bahwa LAS F-15 D sudah terpakai.

---

## 6. Overlap dengan WITSML parsed (tugas wajib no.3)

WITSML parsed yang ada (`ls /mnt/d/Capstone 1/data/volve/witsml_parsed/`): **F-14, F-15A, F-15_S, F-5, F-7, F-9, F-9_A, VAR_F-5_alt** (+ `_coverage.json`, `_parse_summary.json`).

| Sumur petro (DLIS/LIS) | Ada WITSML parsed? | Catatan |
|---|---|---|
| F-5 | ✅ `F-5.csv` (520 MB) | overlap penuh |
| F-7 | ✅ `F-7.csv` (190 MB) | petro LIS gagal dibuka (§4.2) → WITSML saja |
| F-9 | ✅ `F-9.csv` (201 MB) | overlap |
| F-9A | ✅ `F-9_A.csv` (240 MB) | overlap (beda penamaan: `F-9_A`) |
| F-14 | ✅ `F-14.csv` (813 MB) | overlap + LIS composite menambah suite mentah (§4.1) |
| F-15A | ✅ `F-15A.csv` (469 MB) | overlap |
| **F-15** | ❌ | **sumur baru untuk petrophysics** — 62.106 baris, 85 channel, 216,6–4.090,1 m |
| **F-15B** | ❌ | **sumur baru** — 9.638 baris, 69 channel, 2.600–3.508 m |
| **F-15C** | ❌ | **sumur baru** — 11.663 baris, 81 channel, 2.560–3.232 m |
| **F-15D** | ❌ (LAS-nya sudah dipakai V6-R1) | **33.464 baris, 79 channel array-sonic**, 1.339–4.686 m — tambahan di luar 2 file LAS |

→ **DLIS menambah 4 wellbore yang sebelumnya tidak punya petrophysics** (F-15, F-15B, F-15C, F-15D), dan F-15D DLIS menambah 79 kanal array-sonic di luar LAS yang sudah terpakai.

---

## 7. Temuan sampingan yang relevan untuk capstone

1. **Kanal drilling ada di dalam log petrofisika**: `ROP5` (F-14 LIS), `ROP5_RM` (F-9), `CRPM` (F-15B composite, 2.039 sampel), `ROPAVG` + `WOBAVG` + `TCDM` + `RPTHM` (F-15D, 33k baris) — potensi fitur drilling-by-depth lintas sumur yang selama ini hanya dicari di WITSML/USROP.
2. **Label litologi siap pakai**: `SW`, `BVW`, `VSH`, `CARB_FLAG`, `COAL_FLAG` di semua COMPUTED_OUTPUT (6 wellbore, populasi 1.356–9.764 sampel per well) — memperkaya 4 label LAS V6-R1.
3. **Trap satuan**: mayoritas index DLIS dalam `0.1 in` (bukan m). Join ke WITSML (meter) **wajib** konversi `×0,00254`; F-15D `mm` (÷1000); F-14 LIS `M`. Tanpa konversi, join akan salah ~394×.
4. Coverage kanal berbeda jauh antar wellbore (mis. F-9 composite hanya 17 kanal tanpa density/porosity; F-15C 60 kanal) — jangan asumsikan suite lengkap di semua sumur.

---

## 8. Blocker & keterbatasan (jujur)

| # | Item | Status | Bukti |
|---|---|---|---|
| 1 | F-7 `.LIS` | **GAGAL — 0 channel** | error asli §4.2; 1.600+ offset slice tanpa DFSR |
| 2 | dlisio.lis.curves × numpy 2.5 | **Bug upstream**, diakali subclass resize | traceback §4.1; workaround di `extract_lis_v2.py` |
| 3 | F-15D composite | Bukan suite porositas (array sonic) | daftar 79 kanal §3.3 |
| 4 | Sanity data pasca-workaround | Baris akhir (18.374) = offset resize terakhir dari pembaca; nilai sebagian besar kanal awal = -999,25 (zona air). **Belum ada validasi silang terhadap referensi SPWLA** — kalau angka LIS F-14 dikutip di laporan, validasi dulu. | `v6_d1f_lis_summary.json` |

---

## 9. Bukti & artefak

- **CSV (21 file, 77 MB):** `/mnt/d/Capstone 1/scratch/v6_d1f/csv/`
- **JSON bukti:** `v6_d1f_dlis_summary.json` (per file: channel+units, frame, rows, null-sentinel per kanal), `v6_d1f_lis_summary.json` (log dlisio, reader dipakai, slice scan F-7), `v6_d1f_channel_samples.json` (3 kanal contoh tiap CSV), `v6_d1f_petro_inventory.json`, `v6_d1f_per_file_table.json` — semua di `/mnt/d/Capstone 1/scratch/v6_d1f/`
- **Skrip (dapat direproduksi):** `extract_dlis.py`, `extract_lis_v2.py` (memuat workaround numpy2), `samples.py`, `final_table.py`, `aggregate.py`, `check_libs.py`, `magic.py`, `probe.py` — sama di `/mnt/d/Capstone 1/scratch/v6_d1f/`
- **Referensi format:** README & docs dlisio 1.0.4 (github.com/equinor/dlisio; dlisio.readthedocs.io) — dlisio membaca DLIS V1 (RP66v1) dan LIS79; bagian "Incorrectly written files" menjelaskan escape hatch `error_handler`.

**Kesimpulan tugas:** semua file DLIS dan 1 dari 2 LIS kini terbuka dan terekstrak (309.644 baris total), petrophysics kunci (RHOB/TNPH/PEF/DTCO/SW/BVW/VSH/flag litologi) terkonfirmasi ada di 6 wellbore + 4 wellbore baru ditambahkan; 1 file (F-7 LIS) tetap tertutup karena korup di sumber — dibuktikan dengan pesan error asli dan pemulihan offset yang gagal, bukan klaim tanpa tes.
