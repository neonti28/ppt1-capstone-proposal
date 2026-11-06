# V7-M2 — SINTESIS 8 PEMBACA + RELASI ANTAR-FILE

Task: `t_aafc1ed2` [Master Data Reader] · Board: capstone-v7-solve · Tanggal: 2026-10-11 (WIB)
Sumber: docs/V7_D1a..h_DATA_CHECK.md (8 laporan bawahan) + docs/V7_R1_SOLUTIONS.md (solusi R&D).
Tujuan: (a) agregasi status data per solusi R&D; (b) RELASI ANTAR-FILE (join key + estimasi baris + solusi terbuka); (c) jalur olah data tidak-langsung; (d) 3 relasi paling bernilai.

> **Riset pendahuluan: `verification-mandatory`** — seluruh angka laporan bawahan dicek silang antar-bawahan sebelum dipakai; 4 klaim kunci diuji ULANG dengan skrip mandiri (§7): (1) rentang act_start labels_curated per wellbore vs rentang CSV parsed → 582/884 event berada di dalam jangkauan (bukan 884 penuh); (2) uidRef bhaRun→tubular = 154/161 match; (3) mudLog F-15 D md 1380,1–4.685,0 m vs USROP F-15 1.306,5–4.065,3 m → overlap besar; (4) SHK1_ARC F-15A = 7.998 non-null di 18.016 baris, kedalaman 1.350,9–2.569,6 m (konversi 0,1 in→m).
> **Riset pendahuluan: `scientific-critical-thinking`** — status dipisah OBSERVED (dihitung dari laporan/skrip) vs DERIVED (turunan logis) vs HIPOTESIS (identitas wellbore lintas-folder, mapping USROP). Kontradiksi antar-bawahan dilaporkan apa adanya di §6, tidak diluruskan agar cocok narasi. Klaim ketiadaan (blocked) hanya dinyatakan bila minimal satu laporan memberi bukti grep/parse mandiri.
> **Riset pendahuluan: `statistical-analysis`** — status per-solusi dinilai dari jumlah POSITIF nyata per fold (bukan total baris): syarat UNDERPOWERED V6 (<30 positif/fold) dipakai sebagai ambang; prev & plafon lift (1/prev) dihitung saat relevan (tool_wear prev ~0,5 → plafon lift 2,0; shk prev 0,02–1,59% di wellbore baru → jendela 60 s menentukan jumlah positif, dihitung saat eksekusi).
> **Riset pendahuluan: `sequentialthinking`** (3 pikiran, 3/3 sukses) — hipotesis akar kegagalan per kelas (stuck=status-persistence, shk=positif langka, hyd=label ambang persisten, tool_wear=identitas-run+konfounds) → tes pembeda per relasi kandidat (overlap baris nyata menguji kelayakan) → blocked-list dikunci sebelum rekomendasi.

---

## 0. RINGKASAN EKSEKUTIF

1. **Semua 8 laporan bawahan (D1a..D1h) teragregasi** di §1 — 16 solusi R&D dinilai statusnya dengan angka per-domain.
2. **Relasi antar-file utama (semua join key terverifikasi nyata, §2–§3):**
   - `labels_curated_v2` (884 event, rekonsiliasi 884-vs-1.412 SELESAI = 884 benar) + time-series WITSML/CSV → **582/884 event berada di dalam rentang CSV parsed** (bukti hitung ulang mandiri §7); buka S-A1/S-A3 untuk `stuck`.
   - Petro `SHK1_ARC` (7.998 non-null F-15A, terverifikasi) + WITSML `SHKRSK_RT` F-15A (hanya 12 baris) → label silang `shk` di fold UNDERPOWERED.
   - Petro flags litologi (`SAND_FLAG` 32.988 / `CARB_FLAG` 33.386) + `Well_picks` (409 pick/35 well) + USROP (198.928 baris) → fitur geologi eksplisit per MD → lawan temuan SHAP `bit_wear` yang "mengingat posisi kedalaman" → buka S-F1 dari LAYAK BERSYARAT ke LULUS.
   - `bhaRun.tubular` uidRef → `tubular` XML (154/161 match, verifikasi mandiri) + EDM `CD_BHA_COMP_BIT→CD_ASSEMBLY_COMP` (632/632) → rantai bit per interval.
   - F-1 C/F-11 `GAINLOSSTOT`(575/517)/`PITTOT`/`FLOWOUT`/`FLOWOUTPC` + mudLog litologi dTim 100% (wellbore sama persis) → label fisika kick/loss/washout S-C2 → buka `hyd` bila S-C1 onset gagal.
3. **Koreksi jujur terhadap klaim sebelumnya** (§6): (a) klaim R1 "labels_curated 1.412 event" SALAH (884 benar); (b) estimasi R1 S-B1 "100–200 positif shk/well" terlalu optimis — F-15 cuma 13 baris, F-4 cuma 50; fold shk kuat baru hanya F-10 (798) + F-12 (580); (c) "jalur cepat S-C2 butuh parse F-9 raw" TURUN BEBAN — semua kanal pit/flow sudah ada di time.csv F-9 A (345.442 non-null); (d) D1h §8.1 "94 event F-9 A bisa divalidasi ke time.csv" diperbaiki: time.csv F-9 A hanya menutup 2009-06-27..2009-07-16 → **hanya 12/94 event** yang berada di dalam rentang (82 di luar).
4. **Jalur realistis ke ≥5 kelas LULUS** (mengikuti peringkat R1 §7, dikoreksi dengan temuan bawahan): `vib` + `ssi` (sudah LULUS) + `stuck` via S-A1 onset (data onset 50–74 titik F-9_A + STUCK_RT F-10 15.300 baris) + `bit_wear` via S-F1 onset (1.489 transisi kandidat + fitur geologi relasi antar-file) + `shk` via parse F-10/F-12 (798+580 positif nyata). `hyd` & `tool_wear` = UPSIDE dengan tes pembeda (§4).

## 1. TABEL AGRREGASI (solusi R&D | status data per bawahan | total baris | keyakinan)

Kolom pembaca: a=TUBULAR · b=BHARUN · c=TRAJ/WBGEOM · d=MUDLOG · e=LOG XML · f=PETRO · g=EDM · h=KAGGLE/CATALOG.
Status: LANGSUNG = siap pakai · DIOLAH = butuh proses (pemetaan/konversi/join/parse) · TIDAK = tidak ada.
Keyakinan: TINGGI = angka diverifikasi ≥2 jalur independen (recount bawahan + silang antar-bawahan atau verifikasi mandiri M2); SEDANG = satu jalur bukti kuat; RENDAH = ada syarat belum terverifikasi.

| # | Solusi | Kelas dituju | Status DATA (per pembaca) | Angka kunci (baris non-null) | Keyakinan |
|---|---|---|---|---|---|
| S-A1 | stuck onset relabel | `stuck` | **LANGSUNG** (h: time.csv F-9 A `STUCK_RT unitless`; e: 8 CSV parsed) | 45.715 non-null; onset 0→1 = **50** (biner ≥1 = 74); F-14 CSV 394 + F-9 381 baris ≥1 | TINGGI |
| S-A2 | parse F-10/F-12 (stuck) | `stuck` | **DIOLAH** (e: raw XML; b: anchor waktu F-12 start-only 10 run, F-10 = 0 run bhaRun) | F-10 `STUCK_RT` **15.300** baris (prev 44%, didominasi nilai 3); F-12 **3.463** (≥1 = 21) | TINGGI (data nyata); prev tinggi = risiko persisten → wajib bersama S-A1 |
| S-A3 | Snorkel weak supervision (LF1-4) | `stuck` (+ketukuan semua kelas) | **LANGSUNG sebagian + DIOLAH** (h: labels_curated **884 event** rekonsiliasi selesai; a: A_kontak collar Σ od·len 79/79; g: ΔP = PP PLAN/PROTOTYPE 5.080+33.996 dengan caveat kausalitas; e: HKLD/TQA 4 wellbore baru) | 884 event (bukan 1.412); 38 event `bha_stuck_fishing`; 582/884 event di dalam rentang CSV parsed (verifikasi M2 §7) | TINGGI (jumlah event); SEDANG (LF3 ΔP = estimasi pra-lubang, bukan pengukuran) |
| S-B1 | parse F-10/F-4/F-12/F-15 (shk) | `shk` | **DIOLAH** (e: recount 4/4 COCOK klaim R1; b: anchor F-4 start-only 4, F-15 lengkap 30 run C/D; a: F-10 0 tubular, F-12 4 + F-15 C/D 8 stab) | Positif `SHKRSK_RT≥1` **nyata**: F-10 798 (0,27%) · F-12 580 (1,59%) · F-4 50 · F-15 13 (0,02%) · F-15B 0. Total ~825 file log | TINGGI (recount); **koreksi**: hanya F-10+F-12 fold shk BERARTI |
| S-B2 | unit jendela → per-stand | `shk`/`ssi` | **DIOLAH** (e: `BPOS` 8/8 CSV; b: 108 interval bhaRun valid tapi **0 overlap** dgn 8 CSV; kandidat F-15 C/D 28 interval / 9.922,9 jam) | BPOS non-null 59.483–1.540.590 per CSV; gap >10 mnt 2–21/well = lompatan kampanye, bukan batas stand → batas stand = turunan BPOS+gap kecil | SEDANG (boundary = engineering judgment) |
| S-B3 | ordinal shock 0–3 | `shk` | **LANGSUNG** (e: distribusi nilai per wellbore) | F-10: 1→651/2→123/3→24; F-12: 196/226/158; skala 0–3 terkonfirmasi dari nilai, semantik tak terdokumentasi | TINGGI (data); semantik skala = RENDAH |
| S-C1 | hyd onset relabel | `hyd` | **LANGSUNG** (e: SPPA 85.921–1.511.831 + TFLO + SPM1/SPM2 per CSV; h: `Stand Pipe Pressure kPa` 345.442 di F-9 A) | 8/8 CSV punya SPPA+TFLO; label `|z|>2` residual dihitung ulang dari kolom yang ada | TINGGI (data); peluang lolos = SEDANG (sinyal precursor belum teruji) |
| S-C2 | label pit/flow-mismatch | `hyd` | **DIOLAH** — jalur cepat F-9 A: **LANGSUNG** di time.csv (h: 12 kolom pit 345.442, `Tank volume (active)` 345.442, `Flow Pumps` 345.442); jalur penuh F-1 C/F-11: **DIOLAH** (e: GAINLOSSTOT 575/517 file, PITTOT 565/506, FLOWOUTPC 949/731, PITn 59/51 file) | 345.442 baris label kandidat F-9 A; ratusan file F-1 C/F-11 (baris per file belum dihitung) | TINGGI (F-9 A LANGSUNG — koreksi beban R1); SEDANG (F-1 C/F-11 baris belum dihitung) |
| S-C3 | survival/hazard | `hyd` | **DIOLAH** (derivasi label S-C1/S-C2) | — (turunan) | SEDANG |
| S-D1 | tool_wear progresi-onset (change-point) | `tool_wear` | **LANGSUNG** (h: 8 xlsx) | 471.400 sampel, 0 NaN, 1000 Hz konstan; 8 run (4 alat × R01/R02), durasi 50–62 s | TINGGI (data); peluang = SEDANG (change-point validasi: `t_cp` di detik awal = artefak termal → gugur) |
| S-D2 | fitur VMD | `tool_wear` | **LANGSUNG** (h: 8 xlsx) | idem | TINGGI; TIDAK cukup sendiri (plafon lift 2,0) |
| S-D3 | label MSE/DS (Menand-Mills) | `bit_wear` (+`tool_wear` domain sumur) | **LANGSUNG** (h: USROP WOB/ROP/RPM/MSE 100% non-null) | 198.928 baris; inefisiensi parah 78.212 baris (dari V6 R1) | TINGGI |
| S-D4 | learning-to-rank | `tool_wear` | **LANGSUNG** (h: 8 xlsx) | idem | TINGGI (data); estimand baru → pra-reg ulang |
| S-E1 | parse 4 wellbore (CRPM/ssi) | `ssi` | **DIOLAH** (e: `CRPM_RT` 281.030/42.010/178.430/57.846 baris; f: `CRPM` petro 36.308 sbg cross-check) | 4 fold underpowered (F-7 3 pos, F-9 12 pos) bisa diganti fold kuat | TINGGI |
| S-E2 | pra-reg stabilitas fold | `ssi` | **LANGSUNG** (e: hitungan positif per wellbore) | Peta UNDERPOWERED: F-15A 12, F-9_A 40, F-5 82 (shk baris); F-7 tanpa VIBLAT | TINGGI |
| S-F1 | bit_wear onset relabel | `bit_wear` | **LANGSUNG** (h: USROP label; 1.489 transisi blok = kandidat onset) + **DIOLAH** (c: MD→TVD validator; f: konteks geologi flags/picks) | 198.928 baris; transisi 1.489 (sebagian = onset high_MSE, difilter per well saat eksekusi) | TINGGI |
| S-F2 | silang MSE/DS | `bit_wear` | **LANGSUNG** (h: idem S-D3) | 198.928 baris | TINGGI |

### 1b. Item yang TIDAK ADA (anti-klaim, bukti dari bawahan)

| Item | Bukti ketiadaan | Dampak |
|---|---|---|
| Rating motor (`torqueMax`/`Pmax`/`rpmMax`/`powerMax`/`revPerGallon`) | a: grep 0/192 file (mandiri) | Jalur I1/TOB dari rating motor = **TIDAK ADA di mana pun** |
| Kurva tekanan di domain petro | f: 4 lapis (188 kolom CSV + 175 channel DLIS + 157 long-name + 30 kurva LAS = 0 hit); `RM` LAS = ohm.m resistivity | Overbalance dari petro = turunan Eaton (DTCO+RHOB+GR), engineering judgment |
| Pore pressure EDM `phase=ACTUAL` | g: join leaf→group = **8 baris** semua di datum air laut (tvd 298,56 ft) | Overbalance EDM = PLAN/PROTOTYPE (fitur pra-lubang, bukan label pengukuran) |
| Event/NPT di EDM | g: grep mandiri non-productive 0, NPT 0, tag start/end_date 0; `stuck` 947 = `stp_calc_stuck_point` simulasi | Label kegagalan wajib dari labels_curated/DDR (h) |
| Serial/dull/footage bit di EDM | g: `serial` 0, `footage` 0, `dull` 21 hit = base64 noise | Identitas bit = jalur tubular nameTag (a: 26 serial unik) |
| `posAxialWellbore` | a: 0/1.392 komponen | Posisi stabilizer = turunan sequence+len (30 gap di 15 assembly) |
| Formation tops di mudLog & di dalam DLIS/LAS | d: grep `formation` 0/8 file; f: 0 channel `*TOP*`/`*PICK*` | Sumber tops = `Well_picks_Volve_v1.dat` (409 pick, h) |
| `casingSeat` literal | c: 0/90 file domain; padanan `wbGeometrySection` 109/109 non-null | Konteks casing = DIOLAH dari wbGeometry |
| Kolom `WBS*` litologi di time.csv F-9 A | h: non-null 2/419.747 | Jangan dipakai; pakai picks .dat |
| `VIBLAT_RT` di F-7 & F-15A (CSV parsed) | e: kolom absen | Vib fold F-7 mustahil dari CSV itu |

## 2. RELASI ANTAR-FILE (nilai utama M2)

Aturan join universal yang mempersatukan SEMUA relasi di bawah (terverifikasi di 8/8 laporan):
- **`nameWellbore` FIELD XML, bukan path folder** (folder `F-1 C` berisi wellbore F-1 A/B/C/F-1; folder `F-11` berisi 4 wellbore — d/a/b semuanya membuktikan).
- **Nama well ≠ nama folder ≠ nama kolom CSV** → mapping eksplisit wajib: `NO 15/9-F-14` (XML) ↔ `15/9-F-14 - Main Wellbore` (qc CSV) ↔ `N-SH_F-14d` (kolom `well` USROP).
- **Satuan**: WITSML/USROP = meter · EDM = FEET (×0,3048, rasio silang 3,27 terverifikasi) · petro 19 DLIS = `0.1 in` (×0,00254) · F-15D DLIS = `mm` (÷1000) — F-15D punya DUA unit dalam 1 wellbore (join tanpa konversi = salah 3 order magnitudo).
- **Parser pitfall** (e): mapping kolom WITSML = `<logData><mnemonicList>`, BUKAN urutan `logCurveInfo` (TIME dideklarasi ke-7 tapi kolom ke-1). `execute_code`/`-c` diblokir policy → semua run via file `.py` + terminal.

| R# | Pasangan data (file BEDA) | JOIN KEY | Estimasi baris hasil join | Solusi R&D terbuka | Status relasi |
|---|---|---|---|---|---|
| R1 | `labels_curated_v2.csv` (884 event; wellbore + act_start/act_end + md) ↔ time.csv F-9 A + 7 CSV parsed + (nanti) parse F-10/F-12/F-4/F-15 | `wellbore` + irisan `[act_start, act_end]` ↔ timestamp; fallback `md` | **582 event masuk rentang CSV parsed** (verifikasi M2: F-14 182, F-5 136, F-9 56, F-7 59, F-15_S 105, F-15A 32, F-9_A **12**); 302 di luar (82 F-9_A + 7 F-15_S + 211 F-15 C/D → menanti parse wellbore baru) | **S-A1** (validasi onset STUCK_RT = kejadian nyata atau artefak instrumen), **S-A3** LF2 (38 event `bha_stuck_fishing` = LF khusus stuck), S-B1 (label onset shk dari kurasi) | **TERBUKA** — kunci ganda terverifikasi |
| R2 | Petro `SHK1_ARC` F-15A (7.998 non-null, terverifikasi M2; 1.350,9–2.569,6 m) ↔ WITSML `SHKRSK_RT` F-15A (12 baris saja) + fitur F-15A.csv (778.162 baris) | F-15A MD petro (konversi ×0,00254) → trajectory MD→TVD → grid waktu | ±7.998 titik silang label di fold shk UNDERPOWERED (positif WITSML cuma 12) | **S-B1/S-B3** `shk` — sumber label alternatif lintas-domain; cross-check fisika kanal drilling berbeda (LWD vs MWD) | **TERBUKA** (angka terverifikasi M2) |
| R3 | Petro flags `SAND_FLAG`/`CARB_FLAG` (6 file COMPUTED_OUTPUT, 32.988/33.386 valid) + `Well_picks_Volve_v1.dat` (409 pick/35 well) ↔ `USROP_labeled.csv` (198.928 baris, MD non-null 100%) | `wellbore` + MD (meter, setelah konversi 0.1 in→m); picks punya MD+TVD+TVDSS | 198.928 baris USROP ter-join litologi (picks menutup 35 well; flags menutup F-5/F-14/F-15A/B/C/F-15 = fold `bit_wear` + shk) | **S-F1** (fitur geologi eksplisit melawan SHAP "mengingat posisi kedalaman"), S-C1 (konteks formasi untuk hidrolik), S-A3 (aux label anti-konfond) | **TERBUKA** — overlap MD pasti (USROP F-15 1.306–4.065 m vs picks/flags lintas sumur) |
| R4 | `bhaRun` XML (161 run, dTimStart/Stop) ↔ `tubular` XML (192 assembly, 1.392 komponen) ↔ `USROP_labeled.csv` | `bhaRun.tubular` uidRef suffix → tubular `uid`; **154/161 match (verifikasi M2)**; wellbore name + interval | 154 run ber-BHA geometry; TAPI jembatan ke USROP praktis nol (USROP tanpa kolom waktu; `mdHoleStart/Stop` cuma 19/161, 3 span nol; wellbore USROP nyaris tanpa numBitRun) | **S-F1** pemotong bit-run (parsial: hanya F-15 D 1 interval), **S-A3** LF3 (A_kontak per assembly = Σ π·od·len, 15 assembly punya rantai len lengkap → 30 gap stab-to-stab) | **TERBUKA parsial** — anchor ke kampanye USROP rapuh; jalur depth-based wajib lewat `md_assembly_base` EDM atau trajectory |
| R5 | EDM `CD_BHA_COMP_BIT` (632) → `CD_ASSEMBLY_COMP` (join `assembly_comp_id`, **632/632 match**, g) → `CD_ASSEMBLY` (`md/tvd_assembly_base`, phase) ↔ tubular `nameTag` serial (26 unik, a) | `assembly_comp_id` + wellbore + kedalaman (EDM feet → m) | 632 baris identitas bit per depth-interval; serial lintas-domain hanya kandidat (EDM punya `catalog_key_desc` "PDC 6x14…" tapi tanpa serial) | **S-F1/S-D3** konteks bit (tipe/ukuran per interval kedalaman); rantai pemakaian (serial 5221270 muncul 80× = bit fisik dipakai berulang) | **TERBUKA** (join terverifikasi g) — tapi TIDAK menutup fold `bit_wear` USROP (wellbore EDM ≠ wellbore USROP kecuali F-5/F-14 parsial) |
| R6 | `bhaRun` F-15 C/D (29 interval valid, 9.922,9 jam) ↔ `F-15A.csv`/`F-15_S.csv` (778.162 / 1.883.062 baris) | level WELL (`NO 15/9-F-15` vs cabang C/D) + irisan waktu | 28 interval di dalam rentang CSV (kandidat) | **S-B2** (batas stand per wellbore nyata) | **KANDIDAT** — menunggu verifikasi apakah isi CSV = cabang C/D (bukan main) |
| R7 | MudLog F-15 D (301 interval, md 1.380,1–4.685,0 m, verifikasi M2; dTim 100%) ↔ USROP F-15 (53.041 baris, MD 1.306,5–4.065,3) + (setelah parse) StatoilHydro F-15 time-series | `nameWellbore` (NO 15/9-F-15 D ↔ kolom `well` `N-SH-F-15d` — MAPPING = hipotesis, wajib dikunci Master) + MD atau dTim | 301 interval × overlap MD 1.380–4.065 m → ±40 rb baris USROP ter-join litologi (claystone/sandstone/limestone 957/884/678) | S-F1 (geologi), S-C2 gas-rise (chromatograph 1.316 titik dual-key dTim+mdBottom) | **TERBUKA** dengan PRASYARAT mapping F-15↔F-15 D dikonfirmasi |
| R8 | MudLog litologi + chromatograph (8 wellbore F-1 A/B/C, F-1, F-11 A/B/T2, F-15 D) ↔ LOG XML F-1 C/F-11 (`GAINLOSSTOT` 575/517, `PITTOT`, `FLOWOUT(F)`, `PITn` 59/51 file) | `nameWellbore` identik persis (kedua domain memakai `NO 15/9-F-1*`/`F-11*`) + dTim (mudLog 100%, log time-based 1–5 s) | Ratusan file log × 2.882 interval litologi; baris log per file F-1 C/F-11 belum dihitung (BELOM) | **S-C2** (label kick/loss/washout fisika + konteks litologi: "losses di sandstone" = fisika kuat), S-C1 (konteks formasi) | **TERBUKA** — wellbore coverage IDENTIK antar kedua domain (hanya di F-1 C/F-11/F-15 D) |
| R9 | Trajectory MD→TVD (5.561 stasiun; `dTimStn` 5.415/5.561) + wbGeometry (109 section, casing shoe 54) ↔ SEMUA time-series depth-based (USROP, petro 309.644 baris, log depth-based 6–29 file/wellbore) | wellbore + MD (interp) ATAU `dTimStn` ↔ timestamp | 198.928 (USROP) + 309.644 (petro) + ratusan ribu baris depth-based log | S-F1 (SHAP depth → MD→TVD wajib benar; USROP sudah bawa TVD = validator), S-A3 LF3 (incl 5.561 non-null → risiko differential sticking), S-C1/S-C2 (hidrostatik: casing shoe + `depthWaterMean`/`gapAir` 27/27) | **TERBUKA** — semua fold punya ≥1 trajectory penutup (kecuali F-15S ekor 47,1 m, ditutup NO F-15 dgn asumsi identitas) |
| R10 | `time.csv` F-9 A (419.747 baris) ↔ `depth.csv` F-9 A (16.670 baris, punya `STUCK_RT` juga) | timestamp ↔ timestamp-depth grid | 16.670 titik depth saat onset | S-A1 (MD saat onset stuck → fitur kedalaman untuk label onset) | **TERBUKA** (d) |
| R11 | WITSML parsed (SHKRSK/CRPM/ROP/RPM) ↔ petro kanal sejenis (`CRPM` 36.308, `ROP5` 30.653, `ROP5_RM` 66.837, f) | wellbore + depth↔time via trajectory; cross-check per wellbore F-5/F-14/F-15A/F-15/F-9 | ±36 rb titik CRPM + 97 rb titik ROP lintas-domain | Cross-check kelayakan label (kanal berbeda → label berbeda = bahan S-A3 multi-LF); F-14 ROP petro 17.497 vs WITSML ROP 1.218.019 | **TERBUKA** (fitur, bukan label) |
| R12 | Dir alt-NO (F-4-NO/F-12-NO/F-15-NO: fitur surface konvensi lama, satuan SI) ↔ dir target StatoilHydro (MWD: kkgf/kN.m/L/min) | `nameWellbore` + konversi satuan (kkgf→N ×9,80665; kN.m→N.m ×1.000; L/min→m³/s) + irisan waktu (belum diukur) | Belum dihitung (rentang waktu alt-NO belum dicek) | Cadangan fitur/konvensi lama untuk 4 wellbore baru | **KANDIDAT RENDAH** — satuan beda sistem; overlap waktu BELUM diverifikasi |

### 2b. Jebakan yang terbukti nyata (gagal join — jangan diulang)

| Percobaan | Hasil | Pelajaran |
|---|---|---|
| bhaRun (Norway-Statoil-NO, 2012–2016) ↔ 8 CSV parser lama (StatoilHydro/NA, 2007–2015) | **0/8 CSV** punya interval bertemu (bawahan 02, uji penuh) | Dua pohon data Volve menutup periode berbeda untuk nama well sama — join kunci nama+waktu = nol, bukan "data rusak" |
| DEPT WITSML ↔ depth petro (merge langsung) | F-14.csv `DEPT` non-null hanya **0,67%** (11.011/1.648.026) | Depth-time mapping WAJIB lewat trajectory/dTimStn |
| Kolom `WBS*` (litologi) di time.csv | 2/419.747 baris non-null | Sisa join katalog gagal — pakai picks .dat |
| `CasingSeat` EDM-tree literal | 0/90 file domain WITSML (padanan wbGeometrySection ada) | Cek nama field asli, bukan istilah domain |

## 3. JALUR OLAH — solusi yang datanya TIDAK ada langsung tapi BISA dari relasi

| Solusi | Data tidak-langsung | JALUR (langkah nyata) |
|---|---|---|
| **S-A1** onset stuck di F-10/F-12 | onset = turunan, bukan kolom | parse raw F-10/F-12 (D1e: mnemonicList mapping) → grid 60 s → deteksi tepi `STUCK_RT 0→1` pada resolusi 1–5 s (D1e) → jendela `[t0−H,t0)`, blok setelah onset DIBUANG → relabel onset → **gabung dengan onset F-9_A (50 titik) & F-14** → fold 4 |
| **S-A3 LF3** differential sticking `F = μ·A·ΔP` | ΔP & A tidak ada langsung | A_kontak = Σ π·od·len collar per assembly (D1a: 79 collar od/len non-null) + anchor interval via bhaRun→tubular uidRef (R4: 154/161) + ΔP = overbalance dari EDM PP PLAN/PROTOTYPE (g: 5.080+33.996 baris, ft→m) + `CD_FLUID` density 140 baris (filter `is_cement`) → `overbalance(ppg) = density_sg×8,345 − pore_pressure_emw` → μ = konstanta eksplisit bertanda asumsi. LF3 = penanda relatif, BUKAN label |
| **S-C1** hyd onset | label = turunan residu | 8 CSV sudah punya SPPA+TFLO+SPM1/2 (e: langsung) → `qcut(TFLO,10)` + median/MAD per bin → `|z|>2` → deteksi blok ≥k menit → onset → gate G1/G2 dihitung ulang identik |
| **S-C2** label pit/flow F-9 A | label = turunan diff | time.csv F-9 A sudah punya 12 kolom `MudPit Volume Average*` + `Tank volume (active)` + `Flow Pumps` + `Mud Flow In` (h: 345.442 non-null) → z-score per well → onset kick/loss; washout = `Flow Pumps − Mud Flow In` menyimpang + SPPA tren turun. **Nol parse XML** (koreksi beban R1) |
| **S-C2** jalur penuh F-1 C/F-11 | kanal hanya di raw | parse raw (GAINLOSSTOT 575/517, FLOWOUTPC 949/731, PITn 59/51 file) + litologi mudLog wellbore identik via dTim (R8) → label kick/loss dengan konteks litologi |
| **S-D1** tool_wear progresi | onset keausan = turunan | 8 xlsx → deret fitur pendek (kurtosis/crest/f_dom per segmen 1–2 s) → change-point per run → onset `t_cp` → label jendela sebelum `t_cp`; VALIDASI WAJIB: `t_cp` di detik awal = artefak termal → solusi gugur (tes pembeda R1 §5.2) |
| **S-D3/S-F2** label MSE/DS | DS/DOC = turunan | USROP: `DOC = ROP/(60·RPM)`, `DS = WOB/(R·DOC)`, `R = Diameter mm/2000` (m), WOB kkgf→kN ×9,80665 → aturan Menand-Mills `MSE↑ + MSE/DS↓ = bit wear/balling` → cross-label high_MSE |
| **S-F1** bit_wear onset + fitur geologi | onset = turunan transisi; geologi = join | USROP 1.489 transisi blok → filter transisi ke `high_MSE_bit_wear` per well → jendela sebelum transisi (H = 10 mnt ekuivalen 1 jendela, sensitivitas 30) + join picks/flags per MD (R3) sebagai fitur geologi → melawan SHAP `MD_last/mean` |
| **S-B2** batas stand | boundary = turunan | BPOS (8/8 CSV) + pola gap kecil (menit-jam; gap raksasa 10⁸ s = kampanye, D bukan batas stand) + kandidat bhaRun F-15 C/D (R6, menunggu verifikasi) |
| **S-E1** fold ssi kuat | wellbore baru = parse | satu parse F-10/F-4/F-12/F-15 (825 file, ~7 GB, chunk 250k baris anti-OOM) melayani shk+ssi+vib+stuck sekaligus (D1e §11.1) |

## 4. SOLUSI YANG BENAR-BENAR BLOCKED (terus terang + apa yang kurang)

| Solusi/klaim | Status | Yang kurang |
|---|---|---|
| I1/TOB dari rating motor | **BLOCKED TOTAL** | `torqueMax`/`Pmax`/`rpmMax`/`powerMax`/`revPerGallon` = 0/192 file (a, grep mandiri); tidak ada di domain lain yang dicek. Kurang: datasheet motor pabrikan / rating dari DDR (tidak tersedia di Volve) |
| Overbalance sebagai LABEL kebocoran/tekanan dari pengukuran | **BLOCKED** | Petro = 0 kurva tekanan (4 lapis); EDM ACTUAL = 8 baris datum; kurva hanya PLAN/PROTOTYPE → sah sbg fitur pra-lubang, TIDAK sah sbg label (kausalitas: label ditentukan proses lain tidak bisa diprediksi) |
| Identitas bit (serial/dull/footage) dari EDM | **BLOCKED** | `serial` 0, `footage` 0, `dull` = base64 noise (g). Jalur alternatif parsial: tubular nameTag 26 serial (a) — tapi coverage fold `bit_wear` USROP hanya 1/4 (F-14 0 bit, F-5 0 bit, F-15S tidak ada wellbore-nya) |
| Label kegagalan dari EDM/mudLog | **BLOCKED** (bukti ganda) | EDM bukan event DB (g, grep mandiri); mudLog 0 hit stuck/losses/kick/NPT (d, grep ganda). Sumber = labels_curated (884) + kanal dysfungsi WITSML |
| Vib fold F-7 dari CSV parsed | **BLOCKED parsial** | `VIBLAT_RT` kolom absen di F-7.csv (e). Alternatif: parse raw F-7 StatoilHydro (belum dicek apakah kanalnya ada di raw) |
| F-10 + fitur BHA (stabilizer spacing, casing context) | **BLOCKED parsial** | F-10 = 0 file tubular + 0 wbGeometry (a, c) → fitur BHA tidak tersedia di fold shk terkuat; jangan dijanjikan |
| F-7 .LIS petro | **BLOCKED** (file korup: `head.prev 457 != 362`) | Ketidaktekanan kurva tekanan di F-7 LIS tidak bisa dibuktikan; tidak menghalangi klaim umum (sudah dibuktikan di 20 DLIS + 1 LAS + 1 CSV F-14) |

## 5. REKOMENDASI — 3 RELASI PALING BERNILAI untuk kelas tambahan lolos gate

**Relasi #1: labels_curated_v2 ↔ time-series WITSML (R1) → kelas `stuck` LULUS (S-A1 + S-A3 LF2).**
Alasan: menyerang AKAR kegagalan `stuck` (label = status persisten → formulation failure, V6 E1 §4.4) bukan sekadar menambah baris; semua kanal langsung ada (onset F-9_A 50 titik, STUCK_RT F-14/F-9 CSV, F-10 15.300 + F-12 3.463 baris menanti parse); 582/884 event kurasi berada di dalam rentang CSV (terverifikasi M2) → LF2 Snorkel bisa langsung menyandingkan event DDR (termasuk 38 `bha_stuck_fishing`) dengan onset instrumen. Beban: relabel + Snorkel, NOL parse untuk fold eksisting. Gate tidak digeser — hanya definisi LABEL (status→onset) yang berubah (pra-reg baru wajib, R1 §8).

**Relasi #2: trajectory/wbGeometry + picks/flags geologi ↔ USROP (R3+R9) → kelas `bit_wear` naik BERSYARAT→LULUS (S-F1+S-F2).**
Alasan: G1 sudah 3/4 — satu-satunya hukuman = persistence (SHAP didominasi `MD_last/mean` = "mengingat posisi kedalaman"). Relasi ini memberi (a) onset-of-high-MSE dari 1.489 transisi (label lebih fisik), (b) fitur geologi EKSPLISIT (picks 409/35 well + SAND/CARB flags 33 rb baris) yang menggantikan memorisasi depth, (c) validator TVD independen (USROP sudah bawa TVD; trajectory = cross-check). Semua data LANGSUNG/interpolasi, nol parse baru. Ini relasi termurah kedua setelah #1 dan juga membuka S-C1 (konteks formasi).

**Relasi #3: LOG XML F-1 C/F-11 pit/flow (GAINLOSSTOT/PITTOT/FLOWOUT(F)/PITn) ↔ mudLog litologi + labels_curated (R8+R1) → kelas `hyd` (S-C2 pengganti).**
Alasan: S-C1 onset hyd punya risiko nyata "tidak ada sinyal precursor lintas-kanal" (V6 R1 §3.3); relasi ini menyiapkan pengganti dengan SUMBER LABEL berbeda (fisika well-control: pit gain/loss, flow mismatch, washout) di 2 wellbore TERBESAR yang kaya kanal ini (575/517 file GAINLOSSTOT + PITn 59/51 file) DENGAN konteks litologi (losses di sandstone vs seal di claystone = fisika kuat). Jalur cepat cadangan: S-C2 F-9 A dari time.csv (nol parse, 345.442 baris) sudah TERBUKA sekarang untuk tes cepat prevalensi. Beban: parse besar hanya jika S-C1 onset gagal — urutan benar: S-C1 dulu (murah), S-C2 sebagai cadangan berbasis relasi.

Catatan jujur: `hyd` dan `tool_wear` TIDAK bisa dijanjikan lolos — keduanya punya tes pembeda eksplisit (S-C1: lift mayoritas atau "sinyal lemah" terdukuat; S-D1: change-point valid atau gugur). Target minimum 5 kelas (vib+ssi+stuck+bit_wear+shk) TIDAK bergantung pada keduanya.

## 6. KONTRADIKSI & KOREKSI (dilaporkan apa adanya)

| # | Klaim (sumber) | Status | Bukti |
|---|---|---|---|
| 1 | labels_curated_v2 = 1.412 event (R1 §2.4) | **SALAH** → 884 event benar | h: 1.413 baris fisik vs 885 record csv parser; 528 newline di quoted `evidence`/`comments_full`; event_id unik 884/884; M2 konfirmasi 884 record |
| 2 | Estimasi S-B1 "100–200 positif shk/well" (R1 §3.2) | **TERLALU OPTIMIS** | e: prev F-10 0,27% (798), F-12 1,59% (580), F-4 0,14% (50), F-15 0,02% (13 baris!), F-15B 0. Fold shk baru BERARTI = F-10 + F-12 saja |
| 3 | "Jalur cepat S-C2 butuh parse F-9 raw" (R1 §4.3) | **TURUN BEBAN** | h: semua kanal sumber label (12 kolom pit, tank active, flow) ADA di time.csv F-9 A, 345.442 non-null. F-9 A raw sendiri 0 file PITn/GAINLOSSTOT (e) |
| 4 | "94 event F-9 A bisa divalidasi ke time.csv" (D1h §8.1) | **DIPERBAIKI M2 → 12/94** | time.csv F-9 A hanya 2009-06-27..2009-07-16; hitungan M2: 12 dalam, 82 di luar (event F-9 A tersebar sampai 2015-02) |
| 5 | prev F-9_A stuck 66,9% (V6 E1 §4.4) vs 49,4% (h, baris mentah) | **BELUM DIREKONSILIASI** | basis berbeda (jendela grid V6 vs baris mentah); wajib direkonsiliasi pembaca ML sebelum dipakai — M2 TIDAK memilih salah satu |
| 6 | V6-D1e "F-9 242 file" PIT1..30 | **TIDAK COCOK** jumlah file mana pun (46/18/51) | e: kemungkinan lintas-dir; mnemonic PIT1..30 memang ada di dir Statoil-NO F-9 (1 file) |
| 7 | F-9_A prev shk 40 baris vs klaim V6 "12 positif jendela" | BUKAN kontradiksi | beda unit baris-vs-jendela (resample); rekonsiliasi saat eksekusi |

## 7. VERIFIKASI MANDIRI M2 (skrip di workspace `t_aafc1ed2`)

| Cek | Skrip | Hasil |
|---|---|---|
| uidRef `bhaRun.tubular` → `tubular` uid | `verify_joins.py` (V1) | 161 ref, **154 match**, 7 miss (uid tak ada di 192 assembly — dilaporkan apa adanya) |
| labels_curated per-wellbore + rentang act_start | `verify_joins.py` (V2) + `verify_joins2.py` | 884 event; **582 dalam** rentang CSV parsed; F-9_A 12/94 (koreksi D1h) |
| mudLog F-15 D header + 301 interval | `verify_joins2.py` (V3) | wellbore `NO 15/9-F-15 D`, md 1.380,1–4.685,0; overlap USROP F-15 1.306,5–4.065,3 → join layak |
| petro F-15A `SHK1_ARC` | `v4_shk1arc.py` | kolom ada, **7.998 non-null / 18.016 baris**, kedalaman 1.350,9–2.569,6 m (×0,00254) |
| sequ-mcp | tool_call langsung | **3/3 pikiran sukses** (thoughtHistoryLength 3) — wrapper bug yang melaporkan D1d/D1g tidak terulang sesi ini |

Cross-check silang antar-bawahan (tanpa run ulang): recount 4 wellbore baru D1e **COCOK PERSIS** klaim R1 §1.2 (F-10 188/186/66/18/125; F-4 135/135/135/86; F-12 91/90/52/6; F-15 77/76/76/76/37); litologi D1d 957/884/678 direproduksi D1d sendiri; picks 409 D1h = D1f; unit trap D1f dikonfirmasi dari header sumber.

## 8. BELUM DIVERIFIKASI (aturan 3 verification-mandatory)

1. Prev stuck F-9_A: 66,9% (jendela V6) vs 49,4% (baris mentah) — basis belum direkonsiliasi.
2. Isi CSV F-15A/F-15_S: apakah memuat sidetrack C/D (menentukan kandidat R6 bhaRun F-15 28 interval).
3. Mapping USROP `N-SH-F-15d` ↔ wellbore `NO 15/9-F-15 D` (R7) — hipotesis, Master yang kunci.
4. Rentang waktu dir alt-NO (F-4-NO/F-12-NO/F-15-NO) vs dir target — overlap belum diukur (R12).
5. Baris non-null PITn/GAINLOSSTOT per file F-1 C/F-11 (baru jumlah FILE 575/517; baris = BELOM).
6. Overlap per-interval chromatograph (1.316) vs mudGas (576) di mudLog — subset/disjoint belum dicek.
7. 7 miss uidRef bhaRun→tubular (bisa wellbore-mismatch atau assembly hilang) — belum ditelusuri.
8. Isi `ROP data .csv` (kaggle F-15 zip, 17.751 B) — baru listing.
9. Semantik `phase` EDM (ACTUAL/PLAN/PROTOTYPE) & skala 0/1/2/3 STUCK_RT/SHKRSK_RT — tidak terdokumentasi di file; tetap engineer judgment berjangka pra-reg.

## 9. PERNYATAAN GATE (dibawa ke eksekusi V7-E)

Gate pra-reg V6 TIDAK digeser di dokumen ini: G1 lift RF ≥1,5 mayoritas fold layak dinilai; G2 AUPRC RF ≥ canary-kedalaman mayoritas; <30 positif = UNDERPOWERED; LOWO; fitur lampau/label depan; kanal pembentuk label dilarang jadi fitur; persistence>RF = layak bersyarat. Yang disiapkan M2 hanyalah BAHAN: (a) definisi-label baru (onset/progresi/fisika-label) = pra-reg BARU per solusi; (b) data parse baru (F-10/F-12/F-4/F-15); (c) relasi antar-file untuk fitur/label tambahan. Setiap perubahan label/unit = pra-registrasi baru di-hash sebelum training, konsisten `PROTOCOL_RISET_TIM.md`.

---
**Reproduksi:** skrip di workspace task `t_aafc1ed2`: `verify_joins.py`, `verify_joins2.py`, `v4_shk1arc.py` (semua stdlib Python, dijalankan nyata 2026-10-11, output tercetak di sesi).

