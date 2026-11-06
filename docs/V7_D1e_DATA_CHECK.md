# V7-D1e — CEK KETERSEDIAAN DATA: DOMAIN LOG XML (WITSML)

Task: `t_515137cd` [Pembaca 05] · Board: capstone-v7-solve · Tanggal: 2026-10-11 (WIB)
Domain: 7.150 file log XML WITSML (`data/volve/witsml_raw/`) + 8 CSV parser lama (`data/volve/witsml_parsed/`).
Layanan solusi: S-A2, S-B1, S-B3, S-C1, S-C2, S-E1, S-E2 + verifikasi independen klaim V7-R1 §1.

> **Riset pendahuluan: `verification-mandatory`** — semua angka di dokumen ini hasil scan/parse
> sendiri pada sesi ini (bukan salin angka V7-R1); klaim V7-R1 diperlakukan sebagai hipotesis
> yang dikonfirmasi/dikoreksi; kontradiksi dilaporkan apa adanya (§9).
> **Riset pendahuluan: `scientific-critical-thinking`** — klaim negatif V7-R1 §1.1 (F-1 C/F-11
> nol kanal dysfungsi) DIUJI ulang dengan grep mandiri pada sampel ≥150 file/wellbore;
> klaim positif §1.2 di-recount independen per file.

---

## 0. RINGKASAN HASIL

1. **Recount independen §1.2: 4/4 COCOK PERSIS** dengan klaim V7-R1 (F-10 188/186/66/18/125;
   F-4 135/135/135/86; F-12 91/90/52/6; F-15 77/76/76/76/37) — lihat §1. **Angka R1 SAH.**
2. **Klaim negatif §1.1 KONFIRMASI**: 150/150 file F-1 C + 150/150 file F-11 = nol kanal
   dysfungsi (grep mandiri, §8).
3. **Baris data nyata BESAR** (bukan cuma header terdaftar): F-10 SHKRSK_RT 295.033 baris
   non-null, CRPM_RT 281.030, STKSLP 200.783, STUCK_RT 15.300; sampling 1–5 detik (§2).
   → "status label onset" punya resolusi waktu memadai di 4 wellbore baru.
4. **Fitur wajib jendela ADA di 4 wellbore baru** dengan penamaan MWD (`TQA`, `HKLD`, `SPPA`,
   `TFLO`, `BPOS` — bukan `TORQUE_AVG`/`HKLD_AVG`/`FLOWIN` konvensi surface): ratusan ribu s/d
   1,7 juta baris non-null per kanal per wellbore (§3). `SURF_RPM`/`WOB_AVG` konvensi surface
   TIDAK ada di dir StatoilHydro — ada varian RPM lain (`TRPM_RT`, `GS_RPM`, `RPM30s` — lihat
   §3 catatan census).
5. **KONTRADIKSI vs klaim R1 S-C2**: `PIT1..PIT30` + `GAINLOSSTOT` diklaim "ada di raw F-9"
   (R1 §4.3) — scan mentah: **F-9 A: 0 file** punya PITn/GAINLOSSTOT/PITTOT/FLOWOUT;
   hanya dir `Norway-Statoil-NO 15/9-F-9` (18 file log) yang punya (GAINLOSSTOT 6 file,
   PITTOT 6, FLOWOUT 10, FLOWOUTPC 11, PITn 1 file). Jalur cepat S-C2 lewat F-9 raw LEMAH;
   jalur penuh via F-1 C/F-11 tetap kuat (GAINLOSSTOT 575/517 file — klaim R1 §1.1 COCOK) (§4, §9).
6. **S-C1 (SPPA/TFLO/SPM) di 8 CSV parser lama: ADA LANGSUNG semua** — SPPA 85.921–1.511.831
   baris non-null per wellbore; SPM tersedia sebagai SPM1/SPM2 (kolom `SPM` tunggal tidak ada) (§5).
7. **BPOS ada di semua 8 CSV**; gap waktu besar (>10 menit) 2–21 per wellbore dengan gap
   maksimum ~2,1–2,5×10⁸ detik (antar-seksi kampanye) — kandidat batas stand (§6).
8. **Distribusi nilai SHKRSK_RT (0/1/2/3) per wellbore** + fakta skala TIDAK didokumentasikan
   di deskripsi logCurveInfo (hanya unit `unitless`) — §7. **Realita prev shk baru**: F-10
   798 baris (0,27%), F-12 580 (1,59%), F-4 50, F-15 hanya **13 baris**, F-15B nol —
   fold shk kuat baru hanya dari F-10+F-12 (koreksi jujur atas estimasi R1 §3.2).
   STUCK_RT F-10 prev 44% (dominasi nilai 3) → S-A2 wajib bersama S-A1 onset (§7).
9. **S-E2**: positif per wellbore dihitung (§7b) — F-9_A stuck 22.590 baris (49,4%, blok
   status terkonfirmasi), F-15A/F-9_A/F-5 shk tipis (12/40/82), F-7 tanpa VIBLAT_RT,
   4 CSV tanpa STUCK_RT → peta fold UNDERPOWERED untuk Master.

---

## 1. RECOUNT INDEPENDEN KANAL DYSFUNGSI (S-B1 / S-E1 / S-A2)

Metode: `scan_recount.py` (workspace t_515137cd) — stream-parse ET per file, kolom di-resolve
lewat `<logData><mnemonicList>` (bukan urutan logCurveInfo — lihat pitfall §10), hitung
(a) file yang MENDAFTARKAN mnemonic, (b) baris non-null di `<logData>`.
Bukti mentah: `recount_all.json` (244 KB).

| Wellbore (dir raw) | File log | SHKRSK_RT | CRPM_RT | STICK_RT | VIBLAT_RT | STUCK_RT | STKSLP | vs klaim §1.2 |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| StatoilHydro 15/9-F-10 | 271 | **188** | **186** | 0 | **66** | **18** | **125** | **COCOK semua** |
| StatoilHydro 15/9-F-4 | 229 | **135** | **135** | **135** | **86** | 0 | 0 | **COCOK semua** |
| Statoil 15/9-F-12 | 233 | **91** | **90** | **52** | 0 | **6** | 0 | **COCOK semua** |
| StatoilHydro 15/9-F-15 | 92 | **77** | **76** | **76** | **76** | 0 | **37** | **COCOK semua** |
| Statoil-NO 15/9-F-4 (alt) | 57 | 0 | 0 | 0 | 0 | 0 | 0 | R1 tidak menghitung dir ini — SEMUA NOL |
| Statoil-NO 15/9-F-12 (alt) | 110 | 0 | 0 | 0 | 0 | 0 | 0 | idem — SEMUA NOL |
| Statoil-NO 15/9-F-15 (alt) | 1.100 | 0 | 0 | 0 | 0 | 0 | 0 | **konfirmasi** catatan R1 (hanya surface-konvensi-lama) |

**Temuan baru (di luar klaim R1):** ketiga dir "NO" alternatif (F-4-NO 57 file, F-12-NO 110,
F-15-NO 1.100 file) NOL kanal dysfungsi — tetapi KAYA fitur surface konvensi lama
(`HKLD_AVG`, `TORQUE_AVG/MAX/MIN`, `SURF_RPM`, `WOB_AVG`, `FLOWIN`, `ROP_AVG` dalam satuan
N, N.m, c/s, m/s — §3). Jangan salah arah saat parse: 3 wellbore target = dir
**StatoilHydro/Statoil**, bukan Statoil-NO.

## 2. BARIS DATA NYATA + SAMPLING INTERVAL (S-B1/S-E1 — status label onset)

Baris non-null di `<logData>` (bukan jumlah file) untuk kanal dysfungsi:

| Wellbore | SHKRSK_RT | CRPM_RT | STICK_RT | VIBLAT_RT | STUCK_RT | STKSLP | Interval median |
|---|---:|---:|---:|---:|---:|---:|---|
| F-10 | 295.033 | 281.030 | 0 | 66.409 | 15.300 | 200.783 | **2,27 s** (242 file time-based) |
| F-4 | 36.177 | 42.010 | 42.649 | 24.559 | 0 | 0 | **4,72 s** (223 file) |
| F-12 | 36.568 | 178.430 | 90.015 | 0 | 3.463 | 0 | **4,75 s** (215 file) |
| F-15 | 59.572 | 57.846 | 57.228 | 58.240 | 0 | 15.757 | **4,02 s** (80 file) |

Interval = (t_last − t_first)/(n_rows − 1) per file, median antar file (file time-based saja;
file depth-based dikeluarkan: F-10 29, F-4 6, F-12 18, F-15 12 file measured-depth).
→ Resolusi 1–5 detik jauh lebih halus dari grid 60 detik parser lama; onset 0→1 bisa
dijepit pada detik, bukan menit. **Status label onset: LAYAK (data nyata memadai).**
Bukti: `recount_all.json` → keys `rows_dysf`, `times`, `indexTypes`.

## 3. FITUR WAJIB JENDELA DI 4 WELLBORE BARU (S-B1/S-A2)

Kanal fitur + baris non-null (pemetaan mnemonic → kolom via mnemonicList):

| Kanal (nama di dir target) | F-10 (file/baris) | F-4 | F-12 | F-15 |
|---|---|---|---|---|
| `HKLD` (hookload) | 198 / 991.045 | 225 / 1.718.503 | 230 / 1.760.901 | 77 / 224.179 |
| `TQA` (torsi) | 198 / 984.888 | 225 / 1.714.158 | 230 / 1.695.771 | 77 / 220.964 |
| `SPPA` (standpipe press) | 198 / 982.872 | 221 / 1.691.614 | 228 / 1.619.742 | 77 / 220.914 |
| `TFLO` (total flow) | 198 / 922.788 | 226 / 1.760.319 | 230 / 1.626.804 | 77 / 182.623 |
| `BPOS` (block pos) | 169 / 888.843 | 221 / 1.740.566 | 212 / 1.720.343 | 65 / 209.935 |
| `TIME` | 241 / 2.387.145 | 221 / 2.187.675 | 214 / 2.086.731 | 79 / 778.237 |
| `DEPTH` (file depth-based) | 29 / 264.835 | 6 / 24.603 | 18 / 147.250 | 12 / 112.714 |
| `ROP_AVG` / `SURF_RPM` / `WOB_AVG` (nama surface klasik) | **0** | **0** | **0** | **0** |
| `RPM` (≈SURF_RPM) | 198 | 223 | 230 | 72 |
| `SWOB` (≈WOB) | 198 | 226 | 229 | 77 |
| `ROP` (≈ROP_AVG) | 186 | 225 | 230 | 76 |
| `GS_RPM`/`GS_SWOB`/`GS_ROP`/`GS_HKLD`/`GS_TQA` (copy surface) | 264/264/264/264/264 | 0 | 0 | 91/91/91/91/91 |
| `TRPM_RT` (total RPM) | 187 | 135 | 93 | 77 |
| `Bit_RPM` / `DRPM` | 0/198 | 148/92 | 108/1 | 0/77 |

- **Status: ADA SETELAH DIOLAH (gampang)** — pemetaan nama: `HKLD_AVG`→`HKLD`,
  `TORQUE_*`→`TQA`, `FLOWIN`→`TFLO`, `ROP_AVG`→`ROP`, `SURF_RPM`→`RPM` (atau `TRPM_RT`
  bila butuh total), `WOB_AVG`→`SWOB`. Semua ADA di ke-4 wellbore target (file count di
  atas). Proses: parse CSV per wellbore (parser V6 dengan mapping mnemonicList) + rename
  kolom + konversi satuan bila digabung dengan dir alt-NO (lihat peluang §11).
- Satuan terdokumentasi di logCurveInfo: HKLD `kkgf`, TQA `kN.m`, SPPA `kPa`, TFLO `L/min`,
  BPOS `m`, DEPTH `m` (kecuali file alt-NO: N, N.m, c/s, m/s — sistem berbeda!).
- **HAS tidak ada** di 4 wellbore (0 file) — kedalaman hole-assembly dari `DEPTH`/index saja.

## 4. S-C2 — PIT/GAINLOSSTOT/FLOWOUT: F-9 RAW, F-1 C, F-11

Konfirmasi klaim R1 (penuh, `grep -rl` per mnemonic seluruh file — `f9_check.txt`,
`f1cf11_counts.txt`):

| Dir | File log | GAINLOSSTOT | PITTOT | FLOWOUT | FLOWOUTPC | file dengan PITn |
|---|---:|---:|---:|---:|---:|---:|
| **NA 15/9-F-9 A** | 46 | **0** | 0 | 0 | 0 | **0** |
| **Statoil-NO 15/9-F-9** | 18 | 6 | 6 | 10 | 11 | 1 |
| StatoilHydro 15/9-F-9 | 51 | 0 | 0 | 0 | 0 | 0 |
| **Statoil-NO 15/9-F-1 C** | 2.156 | **575** ✓ | **565** ✓ | **688** | **949** | **59** |
| Statoil-NO 15/9-F-11 | 1.750 | **517** ✓ | **506** ✓ | 612 | 731 | 51 |
| NA 15/9-F-1 C / F-11 B | 0 / 0 | 0 | 0 | 0 | 0 | 0 |

✓ = cocok dengan klaim R1 §1.1 (575/517 GAINLOSSTOT, 565/506 PITTOT, 506/455 LINEWEAR).
**Status S-C2:**
- Jalur cepat (F-9 raw): **TIDAK ADA bermakna** — F-9 A (sumur label stuck terbesar) nol;
  satu-satunya sumber adalah dir Statoil-NO F-9 (18 file; PITn hanya 1 file).
  Klaim R1 §4.3 "PIT1..PIT30 & GAINLOSSTOT ada di raw F-9" **TIDAK TERKONFIRMASI untuk F-9 A** —
  kemungkinan merujuk dir Statoil-NO F-9 (18 file) atau tercampur dengan klaim V6-D1e §3
  ("F-9 242 file PIT1..PIT30" — angka 242 tidak cocok dengan jumlah file log manapun di
  ketiga dir F-9: 46/18/51). Lihat §9.
- Jalur penuh (F-1 C/F-11): **ADA, perlu parse** — GAINLOSSTOT/PITTOT/FLOWOUT/FLOWOUTPC di
  ratusan file; PITn (PIT1..PIT30) di 59 file F-1 C. Beban besar tapi data nyata.
- Baris non-null per file contoh: belum dihitung (estimasi = chunk besar per file;
  perlu parse penuh — dicatat sebagai BELOM (§12)).

## 5. S-C1 — SPPA/TFLO/SPM DI 8 CSV PARSER LAMA

Chunked scan (`check_csvs2.py`, bukti `csv_check2.json`):

| CSV | Baris | SPPA non-null | TFLO non-null | SPM1 non-null | SPM2 non-null |
|---|---:|---:|---:|---:|---:|
| F-14.csv | 1.648.026 | 1.226.434 | 1.226.968 | 1.222.670 | 1.222.671 |
| F-15A.csv | 778.162 | 202.903 | 164.651 | 23.345 | 23.345 |
| F-15_S.csv | 1.883.062 | 1.511.831 | 1.301.351 | 1.300.890 | 1.300.213 |
| F-5.csv | 1.286.967 | 839.365 | 840.314 | 838.966 | 839.057 |
| F-7.csv | 547.500 | 405.563 | 405.567 | 405.545 | 405.549 |
| F-9.csv | 457.545 | 320.600 | 320.933 | 320.592 | 320.595 |
| F-9_A.csv | 419.706 | 85.921 | 83.557 | 86.306 | 86.306 |
| VAR_F-5_alt.csv | 59.489 | 59.483 | 59.483 | 59.483 | 59.483 |

**Status: ADA LANGSUNG** — kolom sudah ada di CSV, tinggal pakai untuk relabel onset S-C1.
Catatan: kolom `SPM` tunggal TIDAK ada; tersedia `SPM1`/`SPM2` (jumlah coretan per pompa —
jumlahkan bila butuh total SPM). F-15A SPM sangat jarang (23.345 dari 778.162 baris).

## 6. S-B2 — BPOS + GAP WAKTU (kandidat batas stand)

`BPOS` non-null per CSV (dari `csv_check2.json`): F-14 1.227.022 · F-15A 209.915 ·
F-15_S 1.540.590 · F-5 857.767 · F-7 405.567 · F-9 320.933 · F-9_A 86.306 ·
VAR_F-5_alt 59.483 → **BPOS ADA DI 8/8 CSV**.
Gap timestamp >10 menit per CSV (chunk-boundary + intra-chunk): 21/10/16/9/10/8/2/2;
gap maksimum 1,95–2,51×10⁸ s ≈ 2,3–2,9 tahun → ini lompatan antar-seksi/kampanye
(kampanye Volve 2008–2013), BUKAN kandidat batas stand harian. **Batas stand yang berguna
harus diturunkan dari pola gap KECIL (menit-jam) + perilaku BPOS (TRIP/move), bukan dari
gap raksasa antar-seksi.** Proses: derivasi BPOS derivative + threshold gap empiris per
wellbore (engineering judgment, perlu dihitung saat eksekusi).

## 7. S-B3 — DISTRIBUSI NILAI SHKRSK_RT + DOKUMENTASI SKALA

Full parse (`scan_shk_f1cf11.py --shk`, bukti `shk_dist.json`), kolom via mnemonicList:

| Wellbore | Baris non-null | 0 | 1 | 2 | 3 | ≥1 (prev) |
|---|---:|---:|---:|---:|---:|---|
| F-10 | 295.033 | 294.235 | 651 | 123 | 24 | **798 (0,27%)** |
| F-4 | 36.177 | 36.127 | 24 | 14 | 12 | **50 (0,14%)** |
| F-12 | 36.568 | 35.988 | 196 | 226 | 158 | **580 (1,59%)** |
| F-15 | 59.572 | 59.559 | 4 | 8 | 1 | **13 (0,02%)** |
| F-15B | 3.148 | 3.148 | 0 | 0 | 0 | **0 (0%)** |

- Skala 0/1/2/3 TERKONFIRMASI dari nilai; **unit `unitless` terdokumentasi di logCurveInfo,
  tetapi deskripsi/semantik skala TIDAK ADA** (field `description` kosong di semua file yang
  dicek — `show_descr.py` → `{}`) → interpretasi 0–3 tetap engineer judgment seperti V6 E1 §7.5.
- **Implikasi jujur untuk S-B1**: estimasi R1 ("prev ~2% → 100–200 positif/well") terlalu
  optimis untuk F-15 (13 baris!) dan F-4 (50 baris). Fold shk baru yang BERARTI hanya datang
  dari **F-10 (798) + F-12 (580)**; F-15/F-4 nyaris tidak menambah positif shk.
  Resample grid 60 detik bisa menaikkan hitungan jendela (satu baris = beberapa jendela
  berpotongan tumpang tindih) tetapi orde besarnya tetap kecil untuk F-15/F-4.
- `STUCK_RT` (untuk S-A2): F-10 — 15.300 baris non-null: 0→8.576, 1→80, 2→29, **3→6.615**
  (≥1 = 6.724 = **44%**); F-12 — 3.463 baris: ≥1 = **21 baris (0,6%)**.
  → F-10 stuck prev 44% DIDOMINASI nilai 3 — mirip karakter "blok status" F-9_A (prev 49,4%);
  **S-A2 (tambah fold) tanpa S-A1 (onset) berisiko mengulang kegagalan persistence.**
  F-12 menambah eligible well tapi positifnya tipis (21 baris).
- Temuan sampingan (semantik kanal, dilaporkan apa adanya): `VIBLAT_RT` terkwantisasi pada
  tangga ~8,04 (8,043/16,087/24,131/32,174/40,218…) meski unit `ft/s2` — pola level-code,
  BUKAN magnitudo kontinu; `STICK_RT` = rpm kontinu kelipatan 3 (bukan flag 0/1);
  `STKSLP` terkumpul di 0/4/8/12 (unitless). `CRPM_RT` = rpm kontinu 0–255 wajar.
  Konsekuensi S-B3 (ordinal 0–3) tetap valid untuk SHKRSK_RT/STUCK_RT; VIBLAT perlu
  keputusan tersendiri (pakai level code, jangan anggap ft/s² fisik).

## 7b. S-E2 — POSITIF PER WELLBORE DARI CSV LAMA (bahan deteksi fold UNDERPOWERED)

Hitungan baris (bukan jendela) dari `csv_check2.json` — syarat UNDERPOWERED V6: <30 positif
per fold; ini dipakai Master untuk menandai fold mana yang butuh S-B1/S-E1:

| CSV (wellbore) | Baris | STUCK_RT≥1 | SHKRSK_RT≥1 | VIBLAT_RT>0 | CRPM_RT≠0 | Catatan |
|---|---:|---:|---:|---:|---:|---|
| F-14 | 1.648.026 | **394** | **180** | 2.234 | 23.015 | stuck_dist: 0→4.753, 1→371, 2→19, 3→4 |
| F-15A | 778.162 | kolom absen | **12** | 42.804 | 49.429 | shk sangat langka |
| F-15_S | 1.883.062 | kolom absen | **300** | 136.666 | 135.565 | shk terbanyak kedua |
| F-5 | 1.286.967 | kolom absen | **82** | 40.277 | 44.637 | |
| F-7 | 547.500 | kolom absen | **176** | kolom absen | 2.722 | TANPA VIBLAT_RT |
| F-9 | 457.545 | **381** | **146** | 5.853 | 9.772 | stuck hanya nilai 0/1 |
| F-9_A | 419.706 | **22.590 (49,4%)** | **40** | kolom absen | 13.763 | stuck 0→23.122, 1→3.171, 2→363, 3→19.056 |
| VAR_F-5_alt | 59.489 | kolom absen | kolom absen | kolom absen | kolom absen | tanpa kanal dysfungsi |

- **UNDERPOWERED terkonfirmasi di skala baris**: F-15A (12), F-9_A (40), F-5 (82) shk sangat
  tipis; F-7 tanpa VIBLAT (vib fold di F-7 mustahil dari CSV ini); F-15A/F-15_S/F-5/F-7
  tanpa STUCK_RT (stuck eligible hanya F-14, F-9, F-9_A — konsisten V6 "2 sumur eligible"
  F-14+F-9_A; F-9 punya 381 baris tapi V6 mencatat 1.159 label valid — perbedaan unit
  baris-vs-jendela/resample, jangan langsung menyimpulkan kontradiksi; rekonsiliasi saat
  parse).
- F-9_A stuck prev baris 49,4% — konfirmasi kuat diagnosis "label = blok status" (V6 E1 §4.4).

## 8. KLAIM NEGATIF §1.1 (F-1 C / F-11 = NOL KANAL DYSFUNGSI) — TES MANDIRI

`check_grep.sh` (`grep_check.txt`): 150 file pertama (sorted) per dir besar di-grep dengan
pola `<mnemonic>(SHKRSK_RT|STUCK_RT|VIBLAT_RT|CRPM_RT|STICK_RT|STKSLP|WHIRL_RT|BOUNCE_RT)</mnemonic>`:
- Norway-Statoil-NO 15/9-F-1 C (2.156 file log): **150/150 bersih, 0 HIT**.
- Norway-Statoil-NO 15/9-F-11 (1.750 file log): **150/150 bersih, 0 HIT**.
- Dir NA F-1 C dan NA F-11 B: 0 file di bawah `log/` (hanya wellboreInfo/trajectory) —
  struktur berbeda; "F-1 C 2.156 file" R1 = dir Statoil-NO (terkonfirmasi).
**Status klaim R1: KONFIRMASI (sampel 300 file, 0 pelanggaran).**

## 9. KONTRADIKSI & KOREKSI vs V7-R1 / V6-D1e

1. **R1 §4.3 S-C2**: "kanal `PIT*`/`GAINLOSSTOT` MENTAH di F-9 (D1e: PIT1..PIT30 &
   GAINLOSSTOT ada di raw tapi tidak masuk CSV lama)" — **sebagian salah**:
   F-9 A (46 file): 0 file PITn/GAINLOSSTOT/PITTOT/FLOWOUT. Hanya dir Statoil-NO F-9
   (18 file log) yang memilikinya (6/6/10/11 + 1 file PITn). Konsekuensi: "jalur cepat S-C2"
   hampir tidak ada bahannya; prioritas turun di bawah S-C1 (yang datanya LANGSUNG di 8 CSV).
2. **V6-D1e §3 baris "F-9 | 242 | 47 | PIT1..PIT30…"**: angka 242 = jumlah file log gabungan
   ketiga dir F-9 (46+18+51=115) TIDAK cocok; kemungkinan dihitung termasuk file non-log
   atau lintas-dir. Mnemonic PIT1..PIT30/GAINLOSSTOT ada — tapi di dir Statoil-NO F-9
   (18 file), bukan mayoritas. Rekonsiliasi dilaporkan ke Master.
3. Semua klaim §1.1/§1.2 R1 lainnya yang diuji: **COCOK** (angka per-file recount §1;
   full grep F-1 C/F-11 §4; sampel negatif §8).

## 10. PITFALL PARSER (wajib dibaca siapa pun yang parse 4 wellbore baru)

Pada dataset ini `<logCurveInfo>` TIDAK punya `<columnIndex>`, dan **urutan deklarasi
logCurveInfo ≠ urutan kolom `<data>`** (bukti: file F-15 `log/2/2/1/00001.xml` — `TIME`
dideklarasikan ke-7 tetapi kolom data ke-1; parser yang memakai urutan deklarasi salah
membaca seluruh kolom, termasuk SHKRSK_RT). Mapping benar = `<logData><mnemonicList>`
(per-chunk, dipakai parser lama `code/50_witsml_parse.py`). Semua angka dokumen ini memakai
mnemonicList; diverifikasi lewat silang: timestamp terbaca sebagai ISO datetime valid dan
SHKRSK_RT terbatas pada nilai kecil (§7a).

## 11. PELUANG PROSES / RELASI ANTAR-FILE (untuk Master)

1. **Satu parse melayani 4 kelas**: F-10/F-4/F-12/F-15 mengandung sekaligus SHKRSK (shk),
   CRPM+STKSLP+STICK (ssi), STUCK (stuck: F-10 15.300 + F-12 3.463 baris non-null),
   VIBLAT (vib) — S-B1/S-E1/S-A2 SATU pekerjaan parse (total 825 file log, ~7 GB).
2. **Join antar-dataset**: dir alt-NO (F-4-NO/F-12-NO/F-15-NO) punya fitur surface konvensi
   lama dengan satuan SI (N, N.m, c/s, m/s) sementara dir target pakai kkgf/kN.m/L/min —
   kalau digabung, konversi satuan WAJIB (kkgf→N ×9,80665; kN.m→N.m ×1000; L/min→m³/s).
3. **Time-based + depth-based join**: tiap wellbore punya 6–29 file depth-based (index
   `measured depth`) — join ke time-based lewat TIME+DEPTH (file depth-based punya kolom
   TIME juga: F-10 241 file time-based vs 29 depth-based; pasangkan via rentang waktu).
4. **Sampling 1–5 detik → grid 60 detik**: resample agregat menit mengikuti parser V6;
   onset label bisa dihitung pada resolusi detik lalu diaggresi (memperkaya S-A1/S-C1 onset).
5. **SPM1+SPM2** (CSV lama) = total strokes; turunan `SPM_total = SPM1+SPM2` untuk fitur
   hidrolik S-C1/S-C2(c) tanpa parse ulang.

## 12. BELUM DIVERIFIKASI (jujur)

- Baris non-null PITn/GAINLOSSTOT per file F-1 C/F-11 (baru jumlah FILE, belum baris).
- Gap KECIL (menit) per CSV untuk kandidat stand sebenarnya (baru gap >10 menit + maksimum).
- Kelayakan join antar-chunk F-9-NO GAINLOSSTOT (hanya 6 file — mungkin perlu parse penuh).
- Varians/floor VIBLAT_RT sebagai fitur di wellbore baru (baru bukti kwantisasi, belum
  dicek apakah level-code-nya punya varians memadai per fold).

---

## Aneks §3a — CENSUS MNEEMONIC (bukti varian RPM/WOB/ROP)

`census_mnemonics.py` → `census.json` (regex `<mnemonic>` seluruh file log per dir).
Jumlah file yang mendaftarkan tiap mnemonic (top relevan):

| Mnemonic | F-10 (271) | F-4 (229) | F-12 (233) | F-15 (92) | F-15B (16) | F-4-NO (57) | F-12-NO (110) | F-15-NO (1100) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `RPM` | 198 | 223 | 230 | 72 | 11 | 0 | 0 | 0 |
| `GS_RPM` | 264 | 0 | 0 | 91 | 14 | 0 | 0 | 0 |
| `TRPM_RT` | 187 | 135 | 93 | 77 | 0 | 0 | 0 | 0 |
| `SWOB` | 198 | 226 | 229 | 77 | 12 | 0 | 0 | 0 |
| `ROP` | 186 | 225 | 230 | 76 | 12 | 0 | 0 | 0 |
| `SURF_RPM` | 0 | 0 | 0 | 0 | 0 | 26 | 51 | 384 |
| `WOB_AVG` | 0 | 0 | 0 | 0 | 0 | 23 | 43 | 370 |
| `ROP_AVG` | 0 | 0 | 0 | 0 | 0 | 26 | 51 | 384 |
| `MOTOR_RPM` | 0 | 0 | 0 | 0 | 0 | 23 | 43 | 366 |
| `Bit_RPM` | 0 | 148 | 108 | 0 | 0 | 0 | 0 | 0 |

→ Semua fitur wajib jendela tersedia di 4 wellbore target dengan nama MWD; dir alt-NO
menyediakan padanan konvensi lama (SURF_RPM/WOB_AVG/ROP_AVG/MOTOR_RPM) sebagai cadangan
fitur/sumber join (dengan satuan berbeda — §11.2).

### Bukti skrip (workspace t_515137cd)
`scan_recount.py`+`recount_all.json` · `check_csvs2.py`+`csv_check2.json` ·
`check_grep.sh`+`grep_check.txt` · `check_f9.sh`+`f9_check.txt` ·
`check_f1cf11_counts.sh`+`f1cf11_counts.txt` · `scan_shk_f1cf11.py`+`shk_dist.json` ·
`census_mnemonics.py`+`census.json` · `analyze_recount.py`/`show_census.py`/`show_shk.py`/`show_descr.py`

