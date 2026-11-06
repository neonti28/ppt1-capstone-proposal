# V7-D1f — Cek ketersediaan data untuk solusi R&D (domain: PETROPHYSICS DLIS/LIS/LAS)

**Task kanban:** `t_3b4c9512` · **Tanggal:** 2026-10-11 · **Status:** selesai, semua angka berasal dari output tool pada sesi ini.
**Skrip bukti:** `d1f_step1_open.py` … `d1f_step10_join.py` (workspace task, dijalankan satu per satu, output dicetak).

**Riset pendahuluan: `verification-mandatory` — setiap klaim "ada/tidak ada" di dokumen ini punya angka dari tool output; klaim ketiadaan diuji di 4 lapis (kolom CSV, nama channel mentah DLIS, long-name mentah, kurva LAS), bukan dari asumsi.**
**Riset pendahuluan: `scientific-critical-thinking` — status dipisah OBSERVED vs DERIVED: "kurva tekanan tidak ada" = OBSERVED (bukti daftar channel), "pore pressure bisa diturunkan dari sonic" = hipotesis butuh kalibrasi, bukan data jadi.**
**Riset pendahuluan: `sequentialthinking` (3 pikiran) — gap verifikasi (F-14 LIS mentah tidak ter-scan, F-7 korup, encoding F-5 berbeda) dicatat eksplisit di §6, bukan disembunyikan.**

---

## 0. Bukti pembukaan file (acceptance a)

File pertama dibuka dan isinya dicetak (`d1f_step1_open.py`):

```
FILE: /mnt/d/Capstone 1/scratch/v6_d1f/csv/15_9-F-5__WLC_PETROPHYSICAL_COMPOSITE_1__lf0_frame0.csv
SIZE_BYTES: 9651589
NCOL: 49
COLUMNS: ['FRAMENO', 'DEPTH', 'A16H', 'A22H', 'A28H', 'A34H', 'A40H', 'ATMP', 'ATMP_MWD',
 'BPHI', 'CRPM', 'DRHB', 'DRHL', 'DRHO', 'DRHR', 'DRHU', 'DTCO', 'DTRP', 'DTTP', 'GR_ARC',
 'GRM1', 'GRMA', 'P16H', 'P16L', 'P22H', 'P22L', 'P28H', 'P28L', 'P34H', 'P34L', 'P40H',
 'P40L', 'PEB', 'PEF', 'PEL', 'PER', 'PEU', 'RHOB', 'ROBB', 'ROBL', 'ROBR', 'ROBU', 'ROP5',
 'ROP5_RM', 'TAB_ARC_RES', 'TNPH', 'UCAV', 'UCHO', 'UCVE']
row0: FRAMENO=1 DEPTH=74760 ... (semua kurva -999.25)
row4: GRM1=6.846776, sisanya -999.25
```

**Aturan null:** sentinel `-999.25` (dan nilai `<= -999`) dihitung NULL, bukan data. Tanpa aturan ini semua kolom terlihat "penuh".

**Inventaris diverifikasi ulang (bukan kutipan):** 21 CSV · **309.644 baris** (cocok klaim V6-D1f §0) · 188 kolom unik · jumlah kolom seluruh file = 573.
Jumlah channel per 20 file DLIS mentah (dlisio) = **504 → klaim "504 channel" V6-D1f TERKONFIRMASI** (504 = jumlah per-file, bukan nama unik; nama unik = 175 di DLIS mentah, 188 di CSV).

---

## 1. Tabel utama (acceptance b)

| Solusi R&D | Data needed | Status | Bukti (kolom + baris non-null + path) | Peluang proses |
|---|---|---|---|---|
| **S-B1 / S-E1** — kanal drilling petro jadi fitur/label lintas-sumur | `ROP5` | **ADA (sebagian wellbore)** | 3 file / **30.653** non-null: F-5 COMPOSITE 7.968 · F-9A COMPOSITE 5.188 · F-14 LIS COMPOSITE 17.497 (`…/scratch/v6_d1f/csv/`) | Kolom `ROP5` beda file → gabung asal depth diseragamkan (lihat §4) |
| S-B1/S-E1 | `ROP5_RM` (5-ft ROP smoothed; long-name mentah = `5ft ROP 6in`) | **ADA LANGSUNG** | 6 file / **66.837** non-null: F-5 15.697 · F-9 1.203 · F-15A 18.007 · F-15B 2.112 · F-15C 4.406 · F-15 25.412 | Kandidat fitur utama lintas-sumur (coverage terbaik) |
| S-B1/S-E1 | `CRPM` (long-name mentah = `Collar Rotational Speed`) | **ADA LANGSUNG** | 6 file / **36.308** non-null: F-5 5.664 · F-14 6.305 · F-15A 10.071 · F-15B 2.039 · F-15C 2.041 · F-15 10.188 | Cross-check terhadap `RPM` surface WITSML (6 wellbore sama ada `RPM`) |
| S-B1/S-E1 | `ROPAVG`, `WOBAVG` | **ADA LANGSUNG tapi hanya 1 wellbore** | masing-masing **33.055** non-null, hanya `15_9-F15D__WLC_PETROPHYSICAL_COMPOSITE_2__lf0_frame0.csv` (dari 33.464 baris) | Tidak bisa jadi fitur lintas-sumur; hanya cross-check F-15D |
| S-B1/S-E1 (tambahan, di luar spek) | `ROP` + `BS` (bit size) di LAS F-15D | **ADA LANGSUNG** | `15_9-F15D__WLC_PETRO_COMPUTED_INPUT_1.LAS`: `ROP` **44.678/45.391** non-null (unit m/hr), `BS` **45.391/45.391** (unit inches) | LAS F-15D **belum ikut 21 CSV** → kalau dipakai, ekstraksi tambahan dulu |
| **S-A3 LF3 / S-C2** — indikator tekanan formasi (overbalance) | kurva tekanan/mud weight/hydrostatic/pore pressure | **TIDAK ADA** | Lihat §3 — 4 lapis pemeriksaan, 0 hit. `RM` di LAS F-15D = **ohm.m (resistivity)**, bukan tekanan | Overbalance harus dari domain lain (EDM pore pressure / WITSML SPPA-PIT-FLOW); opsi turunan sonic = §3.3 |
| **S-F1** — formation tops = konteks depth blok high-MSE | `CARB_FLAG` | **ADA LANGSUNG** | 6 file COMPUTED_OUTPUT / **33.386** valid: F-5 3.574 · F-14 5.784 · F-15A 9.757 · F-15B 1.514 · F-15C 2.908 · F-15 9.849 (blok non-zero: 47/49/26/22/10/224) | Flag per-sampel depth → ubah jadi interval lalu join ke blok high-MSE pada MD (meter) |
| S-F1 | `COAL_FLAG` | **ADA tapi sangat jarang** | 6 file / **31.617** valid; non-zero hanya F-14 (27 baris, 3 blok), F-15C (8, 4 blok), F-15 (7, 2 blok); **F-5/F-15A/F-15B seluruhnya 0** | Jangan diandalkan sebagai label tunggal (varians mendekati nol di 3 wellbore) |
| S-F1 | `SAND_FLAG` | **ADA LANGSUNG** | 6 file / **32.988** valid; non-zero: F-14 4.244 · F-15A 3.183 · F-15 3.420 · F-15C 1.115 · F-15B 451 | Kandidat konteks litologi terkuat (varians paling sehat) |
| S-F1 | flags F-15D (`COAL_FLAG`, `SAND_FLAG`, `VCARB`) | **ADA SETELAH DIOLAH** (di LAS, bukan di CSV) | `15_9-F15D__WLC_PETRO_COMPUTED_OUTPUT_1.LAS`: `COAL_FLAG` **12.198/12.198**, `SAND_FLAG` **12.081**, `VCARB` **11.936** (v/v, bukan flag) | Perlu ekstraksi LAS → CSV dulu (lasio sudah teruji terpasang) |
| S-F1 | formation **tops** diskrit di dalam DLIS/LIS/LAS | **TIDAK ADA** | Tidak ada channel `*TOP*`/`*PICK*`/`*STRAT*` di 188 kolom CSV maupun 157 long-name mentah (daftar lengkap §3.2) | Sumber tops = `Well_picks_Volve_v1.dat` (§3.3) |

---

## 2. Jawaban per pertanyaan Master (§2.6)

### 2.1 Kanal drilling `ROP5` / `CRPM` / `ROPAVG` / `WOBAVG`

Status ringkas (semua dari `d1f_step3_counts.py`, null = `-999.25`):

| Kanal | File (≥1 non-null) | Total non-null | Wellbore |
|---|---:|---:|---|
| `ROP5` | 3 | 30.653 | F-5, F-9A, F-14 |
| `ROP5_RM` | 6 | 66.837 | F-5, F-9, F-15A, F-15B, F-15C, F-15 |
| `CRPM` | 6 | 36.308 | F-5, F-14, F-15A, F-15B, F-15C, F-15 |
| `ROPAVG` | 1 | 33.055 | F-15D |
| `WOBAVG` | 1 | 33.055 | F-15D |

**Verdict: bisa jadi fitur lintas-sumur (S-B1/S-E1), bukan sekadar cross-check — TAPI dengan 3 syarat yang harus dikerjakan (status = ADA SETELAH DIOLAH):**

1. **Coverage tidak seragam & tidak bertumpuk penuh.** `ROP5` ≠ `ROP5_RM` (file yang berisi ROP5 justru tidak punya ROP5_RM, dan sebaliknya kecuali F-5). Satu kolom tidak mencakup semua sumur → gabungan = union beberapa kolom ROP.
2. **Kedalaman ≠ waktu.** Semua kanal ini depth-domain (`DEPTH`/`DEPT`), tanpa timestamp → untuk kampanye jendela 10 menit (grid waktu) butuh pemetaan waktu↔kedalaman lewat trajectory (domain pembaca lain).
3. **Panjang tercatat = interval logged saja.** Contoh: F-5 `ROP5` 7.968 / 23.657 baris = 33,7% — bukan seluruh sumur.

**Cross-check yang sudah terbukti ada:** WITSML parsed `F-14.csv` punya `ROP` 1.218.019 non-null dan `RPM` 1.331.827 non-null (`d1f_step10_join.py`) → petro `CRPM`/`ROP5` bisa divalidasi terhadap surface `ROP`/`RPM` pada wellbore yang sama (F-5, F-14, F-15A, F-15, F-9).

### 2.2 Kurva tekanan (RM, mud weight, hydrostatic, pore pressure) → **TIDAK ADA**

Bukti ketiadaan, 4 lapis (`d1f_step5_strict.py`, regex ketat: `press|pressure|pore|mud weight|hydrostatic|overbalance|ecd|bhp|frac grad|leak off|lot|minifrac|psi|mpa|kpa|bar|ppg`):

```
=== (1) STRICT PRESSURE-KEYWORD HITS ===
CSV columns (188): (NONE)
RAW DLIS channel names (175): (NONE)
RAW DLIS long names (157): (NONE)
```
+ lapis ke-4: kurva LAS F-15D (21 + 9 kurva) → `PRESSURE-HIT: (NONE)` (`d1f_step7_las_picks.py`).

**Daftar channel sebagai bukti** (188 kolom CSV, dicetak penuh oleh `d1f_step2_scan.py`):

```
A16H A22H A28H A34H A40H ABDC01M..ABDC16M ABDCQF01..04 APRA01M..APRA16M ARTM ATMP ATMP_MWD
AZRIT1T2 AZRTBM BDCFM BPHI BVW CALCM CALI CARB_FLAG COAL_FLAG CRPM DCAV DCHO DCVE DEPT DEPTH
DPEFM DRHB DRHFM DRHL DRHO DRHR DRHU DT DTCO DTRP DTRS DTS DTSM DTTP DTTS DW*_WAL/DW*_WALK2
FRAMENO GR GRA GRAF GRAFM GRCFM GRCS01M..08M GRM1 GRMA GR_ARC GR_ARC_FILT KLOGH MWD_GR_BHC
NBGRCFM NBGRCS01..16 NPCKLFM NPHI P16H P16L P22H P22L P28H P28L P34H P34L P40H P40L PEB PEF
PEL PER PEU PHID PHIF RACEHM RACELM RD RHGE RHOB ROBB ROBL ROBR ROBU ROP5 ROP5_RM ROPAVG
RPCEHM RPCELM RPTHM RS RT SAND_FLAG SHK1_ARC SIGE SW TABA TAB_ARC_ TAB_ARC_RES TCDM TNPH
UCAV UCHO UCVE VPVS VSH WCAR WCLA WOBAVG WPYR WQFM WSID
```

Tidak ada `PRESS*`, `PORE*`, `MW*`, `HYD*`, `ECD`, `BHP`, `FG`, `LOT`. Yang mirip ternyata false positive saat dicek manual: `GRM1`/`GRMA` (gamma ray), `ATMP_MWD` (atmospheric), `ROP5_RM` (running mean ROP).

**Klarifikasi `RM`:** spek menyebut "RM" sebagai kandidat kurva tekanan. Fakta: `RM` **hanya** ada di `15_9-F15D__WLC_PETRO_COMPUTED_INPUT_1.LAS`, `unit=ohm.m` → famili **resistivity**, bukan tekanan (`d1f_step8_las_header.py`). Deskripsi LAS hanya `descr='v1'` sehingga apakah Rm = mud resistivity atau micro-resistivity **tidak bisa dipastikan dari header** → jangan dijual sebagai bahan overbalance tanpa konfirmasi.

**Blocker jujur:** `F-7 .LIS` korup (error asli: `file corrupt: head.prev (= 457) != prev(prev(head)).next (= 362)`) → 0 channel, ketiadaan tekanan di file ini **tidak bisa dibuktikan**. `F-14 .LIS` gagal di level header (`dlisio.lis.LogicalFile` tidak punya atribut `.channels`) → untuk F-14 LIS ketiadaan tekanan dibuktikan dari 49 kolom CSV hasil ekstraksi, bukan dari header sumber.

### 2.3 Formation tops/flags

| Flag | File | Baris valid | Non-zero | Blok non-zero | Catatan |
|---|---|---:|---:|---:|---|
| `CARB_FLAG` | F-5 COMPUTED_OUTPUT | 3.574 | 292 | 47 | **Nilai pecahan 0,014–1,0** (bukan 0/1) → encoding beda dari file lain |
| `CARB_FLAG` | F-14 COMPUTED_OUTPUT | 5.784 | 300 | 49 | 0/1 |
| `CARB_FLAG` | F-15A / F-15B / F-15C / F-15 COMPUTED_OUTPUT | 9.757 / 1.514 / 2.908 / 9.849 | 197 / 107 / 49 / 1.721 | 26 / 22 / 10 / 224 | 0/1 |
| `COAL_FLAG` | 6 file COMPUTED_OUTPUT | 31.617 total | F-14 27 · F-15C 8 · F-15 7 · **F-5/F-15A/F-15B 0** | 3 / 4 / 2 | Sangat jarang |
| `SAND_FLAG` | 6 file COMPUTED_OUTPUT | 32.988 total | F-14 4.244 · F-15A 3.183 · F-15 3.420 · F-15C 1.115 · F-15B 451 | 64 / 181 / 122 / 26 / 44 | Varians terbaik |
| `COAL_FLAG`/`SAND_FLAG`/`VCARB` | F-15D **LAS** OUTPUT | 12.198 / 12.081 / 11.936 | — | — | Belum ada di 21 CSV |

**Wellbore pemilik:** F-5, F-14, F-15A, F-15B, F-15C, F-15 (flag di CSV) + F-15D (flag di LAS) = **7 wellbore**.
**Tops diskrit di dalam DLIS/LIS/LAS: TIDAK ADA** (tidak ada channel `*TOP*`/`*PICK*`).

**Proses jadi label konteks kedalaman untuk S-F1:**
1. flag per-sampel → run-length encode jadi interval `[depth_awal, depth_akhir, tipe]` (estimasi hasil: ~33.386 baris valid → ±560 interval dari total 578 blok non-zero yang terhitung di 6 file, angka pasti dihitung saat eksekusi);
2. konversi `DEPTH`/`DEPT` ke meter (§4);
3. join many-to-one ke blok high-MSE (`USROP_labeled.csv`) pada MD meter → konteks "blok ini di dalam/seluar carbonate/sand/coal".

### 2.4 Unit trap — konfirmasi di sumber, bukan kutipan

Dibaca langsung dari channel index tiap file DLIS mentah (`d1f_step6_units.py`):

```
15_9-F-5__...COMPOSITE_1.DLIS      index=DEPTH UNITS='0.1 in'
15_9-F-5__...COMPUTED_INPUT_1.DLIS index=DEPTH UNITS='0.1 in' long='Measured Depth'
... (semua COMPUTED_* = '0.1 in')
15_9-F15B__...COMPOSITE_1.DLIS     index=DEPT  UNITS='0.1 in'
15_9-F15C__...COMPOSITE_1.DLIS     index=DEPT  UNITS='0.1 in'
15_9-F15D__...COMPOSITE_2.DLIS     index=DEPTH UNITS='mm'          <-- satu-satunya mm
```

LAS (lasio header): `F15D COMPUTED_INPUT`: STRT=145.9 STEP=0.1 **M**; `F15D COMPUTED_OUTPUT`: STRT=3465.0 STEP=0.1 **M**.
F-14 LIS CSV: `DEPT` 1000.0488 … 3800.0938, median step **0.1524** → konsisten dengan meter (60 × 0,00254 m); **label unit tidak terbaca dari header LIS** (lihat §6).

**Kolom yang WAJIB dikonversi sebelum join:**

| Kelompok | File | Kolom | Konversi |
|---|---|---|---|
| Mayoritas (19 dari 21 CSV) | semua DLIS kecuali F-15D | `DEPTH` / `DEPT` | × 0,00254 → meter |
| F-15D DLIS (1 CSV) | `15_9-F15D__...COMPOSITE_2` | `DEPTH` (satuan mm, step 100) | ÷ 1000 → meter |
| F-14 LIS (1 CSV) | `15_9-F14__...lislf0_dfsr0` | `DEPT` (step 0,1524) | sudah meter (asumsi, label belum dibaca) |
| F-15D LAS (2 file, di luar CSV) | `F15D COMPUTED_INPUT/OUTPUT` | `DEPTH` | sudah meter |

**Perangkap tajam:** F-15D punya **dua unit dalam satu wellbore** — `COMPOSITE_2.DLIS` memakai mm (1.339.200–4.685.500) sedangkan `COMPUTED_INPUT/OUTPUT.LAS` memakai meter (145,9–4.684,9). Join tanpa konversi = salah 3 order of magnitude.
**Anomali kecil:** `15_9-F15__WLC_PETRO_COMPUTED_INPUT_1` punya `DEPTH` min = **0** (perlu dicek apakah baris sampah sebelum dipakai).

---

## 3. Catatan tambahan di luar spek (untuk Master)

### 3.1 Peluang relasi antar-file (wajib dilaporkan, §3 tugas)

1. **Petro (depth, meter) ↔ WITSML parsed (time) — join key rapuh.** `F-14.csv` WITSML: `DEPT` non-null hanya **11.011 dari 1.648.026 baris (0,67%)**, `SRVDEPTH` 75, `TVDE` 321.803. Rentang `DEPT` 138,0–2.988,1 m vs petro F-14 setelah konversi 172,5–3.749,8 m → rentang masuk akal, tapi kepadatan depth WITSML sangat rendah → **join depth↔time wajib lewat trajectory, bukan merge langsung**.
2. **Cross-check kolom sejenis di 2 domain:** petro `CRPM` vs WITSML `RPM`; petro `ROP5`/`ROP5_RM` vs WITSML `ROP`; petro `SHK1_ARC` (7.998 non-null, hanya F-15A) vs WITSML `SHKRSK_RT` (F-14 21.643 non-null) → kandidat label silang kelas `shk` di wellbore yang WITSML-nya tipis.
3. **`Well_picks_Volve_v1.dat` (ada di folder domain ini, 74.548 byte):** 35 blok well · **409 baris pick** terhitung manual (scan baris), kolom: `Well NO | formation name | Obs# | Qlf | MD | TVD | TVDSS | TWT | Dip | Azi | Easting | Northing | Intrp` → **tops stratigrafi + MD/TVD meter** = bahan S-F1 paling langsung. Join key = `Well NO` + `MD`. **Overlap: file ini juga masuk spek Pembaca 08 (§2.8 no.6) → Master perlu menetapkan pemilik agar tidak dobel hitung.**
4. **`BS` (bit size) di LAS F-15D** = identitas bit depth-indexed (45.391 baris) → relevan untuk S-F1/S-D3; petro tidak punya `bit serial/dull`.

### 3.2 Kepatuhan angka klaim V6-D1f

| Klaim V6-D1f | Hasil verifikasi ulang | Status |
|---|---|---|
| 24 file log = 20 DLIS + 2 LIS + 2 LAS | `RAW_LOG_FILES=22` terhitung (20 `.DLIS` + 2 `.LIS`) + 2 `.LAS` terpisah = 24 | KONFIRMASI |
| 504 channel | jumlah channel 20 DLIS = **504** | KONFIRMASI |
| 309.644 baris | jumlah baris 21 CSV = **309.644** | KONFIRMASI |
| mayoritas `0.1 in`, F-15D `mm` | dibaca dari index unit tiap file DLIS (§4) | KONFIRMASI |
| F-7 LIS korup | error asli tercetak (§2.2) | KONFIRMASI |

---

## 4. Ringkasan status untuk Master

- **S-B1/S-E1 (kanal drilling petro):** ADA — 5 kanal (`ROP5`, `ROP5_RM`, `CRPM`, `ROPAVG`, `WOBAVG`) + `ROP`/`BS` di LAS; total 199.908 baris non-null gabungan; **status akhir = ADA SETELAH DIOLAH** (konversi depth, pemetaan waktu↔depth via trajectory, union kolom ROP karena coverage beda per wellbore).
- **S-A3 LF3 / S-C2 (overbalance):** **TIDAK ADA** kurva tekanan apa pun di domain petro (bukti 4 lapis). Satu-satunya jalan dari domain ini = **turunan** pore pressure dari `DTCO`/`DT` + `RHOB` + `GR` (metode Eaton) → status **ADA SETELAH DIOLAH, engineering judgment, butuh kalibrasi/overburden** — bukan data siap pakai, dan tidak boleh dihitung sebagai "indikator tekanan yang diukur".
- **S-F1 (konteks depth):** **ADA LANGSUNG** — `CARB_FLAG` 33.386 / `COAL_FLAG` 31.617 / `SAND_FLAG` 32.988 baris valid di 6 wellbore + 12.198/12.081 di F-15D LAS; tops diskrit tidak ada di dalam log → sumbernya `Well_picks_Volve_v1.dat` (409 pick, 35 well).

---

## 5. Riset pendahuluan (baris wajib)

- **Riset pendahuluan: `verification-mandatory` — klaim ketiadaan tekanan diuji di 4 lapis sumber berbeda (kolom CSV 188, nama channel mentah 175, long-name 157, kurva LAS 30) dan daftar channel dicetak utuh; klaim "504 channel" dan "309.644 baris" diverifikasi ulang independen = 504 dan 309.644.**
- **Riset pendahuluan: `scientific-critical-thinking` — dipisahkan OBSERVED (kurva tekanan tidak ada; flags ada dengan baris nyata) vs DERIVED/HIPOTESIS (pore pressure sonic-butuh-kalibrasi; F-14 LIS unit-meter baru konsisten, belum terbaca dari header).**
- **Riset pendahuluan: `sequentialthinking` — 3 pikiran memunculkan 3 gap yang dilaporkan terbuka: F-14 LIS tidak ter-scan di header mentah, F-7 LIS korup mustahil dicek, encoding `*_FLAG` F-5 berbeda (pecahan) dari file lain (0/1).**

---

## 6. BELUM DICEK (wajib, aturan 3)

1. **Label unit `DEPT` F-14 LIS dari header sumber** — `dlisio.lis.LogicalFile` tidak punya atribut `.channels` (error asli tercetak), workaround `dlisio.lis.curves()` diketahui crash di dlisio 1.0.4 (catatan V6-D1f §1) dan belum dicoba ulang di sesi ini. Kesimpulan "meter" = konsistensi numerik (step 0,1524), bukan pembacaan header.
2. **Identitas pasti kurva `RM`** di LAS F-15D (unit ohm.m, `descr='v1'`) — mud resistivity vs micro resistivity tidak bisa dibedakan dari header.
3. **Encoding `CARB_FLAG`/`SAND_FLAG` F-5** (nilai 0,014–1,0) — makna pasti belum diketahui; jangan diperlakukan 0/1 sebelum dicek.
4. **`F-7 .LIS`** — korup, 0 channel, ketiadaan tekanan di file ini tidak terbukti (dan tidak bisa dibuktikan dengan parser yang sama).
5. **`DEPTH` min = 0** pada `15_9-F15__WLC_PETRO_COMPUTED_INPUT_1` — belum ditelusuri apakah baris invalid.
6. **2 file LAS F-15D belum diekstrak ke CSV** (ekstraksi V6 hanya 21 CSV) → semua angka LAS di dokumen ini dibaca langsung dengan lasio, bukan dari CSV.
