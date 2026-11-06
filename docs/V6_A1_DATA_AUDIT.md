# V6-A1 — AUDIT KLAIM TIM DATA (V6-D1a..h + V6-D0 + V6-D2): berdasar atau karangan?

Task: `t_9e5e4f81` [Auditor 1] · Board: capstone-v6-solve · Tanggal: 2026-10-10
Dokumen diaudit: `V6_D1a_TUBULAR.md`, `V6_D1b_BHARUN.md`, `V6_D1c_TRAJ_GEOM.md`, `V6_D1d_MUDLOG.md`,
`V6_D1e_LOG_XML.md`, `V6_D1f_PETRO.md`, `V6_D1g_EDM.md`, `V6_D1h_KAGGLE_CAT.md`,
`V6_D0_READERS_SYNTHESIS.md`, `V6_D2_EXTERNAL_DATASETS.md`.

> **Riset pendahuluan: `verification-mandatory` — setiap klaim dibuka ulang dari file primer dengan tool
> BERBEDA dari penulis (Python glob/os.walk, regex langsung, pandas, ripgrep, dlisio, unduhan urllib);
> angka yang tidak cocok ditelusuri beda-metode dulu sebelum dinyatakan salah; daftar "belum diverifikasi"
> wajib di akhir.**
> **Riset pendahuluan: `scientific-critical-thinking` — observasi/inferensi/hipotesis dipisah; tiap klaim
> kausal (mis. "EDM bukan event DB") diuji dengan tes pembeda (keyword-0 + konteks), bukan narasi.**
> **Riset pendahuluan: `statistical-analysis` — uji sirkularitas label memakai decision tree tanpa batas
> depth dengan train/holdout split (75/25, random_state=0): akurasi holdout <100% = label BUKAN fungsi
> deterministik fitur; rekonstruksi MSE diukur dengan R² holdout.**
> **Riset pendahuluan: `peer-review` — klaim dipetakan ke bukti per lokasi; hal yang tidak bisa diverifikasi
> ditandai "not verified" tanpa spekulasi; temuan disusun terpisah (benar / salah / belum teruji).**

---

## 0. VERDICT RINGKAS

| Pertanyaan audit | Jawaban |
|---|---|
| Apakah 8 pembaca BENAR-BENAR membuka file (bukan karangan, kasus V6_D1 lama)? | **YA — 8/8.** Semua dokumen punya artefak parse nyata di disk (CSV/JSON/script) DAN angka utamanya tereproduksi ulang dari file primer oleh auditor. Tidak ada satu pun dokumen yang klaim intinya gugur. |
| Berapa klaim diverifikasi ulang? | **50+ klaim**, 1 per pembaca jauh terlampaui (syarat minimum 8). |
| Ada klaim salah? | **YA — 5 angka tidak akurat** (2 off-by-one di D1h, 1 salah jumlah kolom di D2, 1 klaim uom azi tidak akurat di D1c, 1 penjelasan newline salah di D1h) + **3 angka tidak terepun­duksi** (keyword EDM stuck/kick/NPT) + 1 generalisasi handoff D2. Rincian §8b. |
| Label ada yang sirkular? | **YA — 1 SIRKULAR penuh** (label rule R1/USROP), **1 sirkular bersyarat** (flag DLIS COMPUTED_OUTPUT), 2 non-sirkular (litologi mudLog, STUCK_RT). §5. |
| Dataset eksternal bisa diunduh? | **YA — 4 unduhan independen sukses** (Haytham ×2, Mendeley T01+T02, XAI Kaggle) termasuk verifikasi sha256 yang diakui belum dicek D2. §6. |

---

## 1. METODE AUDIT (independen dari penulis)

| Aspek | Penulis (dugaan dari dokumen) | Auditor (dipakai di audit ini) |
|---|---|---|
| Hitung file | `find` / ElementTree parse | Python `glob`/`os.walk` (batch A), regex `<tag[ >]` mentah (batch C3) |
| Klaim ketiadaan | grep penulis | grep `LC_ALL=C` sendiri + metode alternatif (word-boundary, -o/-c/attr-token) untuk rekonsiliasi (batch B/B2/B3) |
| Baris CSV | `wc -l` / parser sendiri | `pandas.read_csv` + `csv.reader` + hitung newline byte (batch C/C2/C3) |
| Dataset eksternal | unduhan sesi D2 | unduhan ulang URLEN sendiri + sha256 (batch D/D2/D3/F) |
| Sirkularitas | (belum diuji) | `DecisionTreeClassifier` tanpa batas, split 75/25 seed=0 (batch E/E2) |
| Error F-7 LIS | kutipan error di dokumen | `dlisio.lis.load()` ulang di mesin auditor (batch E) |

Semua skrip audit ada di workspace task ini (`audit_batch_*.py|sh`, hasil di `batch_*_results.txt`).

---

## 2. TABEL KLAIM — isi klaim · metode verifikasi · hasil · catatan

### D1a — TUBULAR (t_80ba3ae3)

| # | Isi klaim | Metode verifikasi auditor | Hasil | Catatan |
|---|---|---|---|---|
| A1 | 192 file tubular XML | `glob(*/*/tubular/*.xml)` | **192** | ✅ benar |
| A2 | 1392 `<tubularComponent>`, 192 `<tubular>` | regex mentah pada 192 file primer | **1392** dan **192** | ✅ benar (primer, bukan lewat CSV penulis) |
| A3 | CSV 1392 baris, 62 tipe, 1222 drill string, 870 wtPerLen, 1330 valid, 62 sentinel, 13 motor, 1 baris od=−999.25 | `pandas` atas `v6_d1a_tubular.csv` | 1392 / 62 / 1222 / 870 / 1330 / 62 / 13 / 1 | ✅ **8 angka EXACT** |
| A4 | Rating motor **0/192** (torqueMax/Pmax/revPerGallon/rpmMax/powerMax/torque) | grep `LC_ALL=C -l` sendiri ke 192 file | masing-masing **0 file**; `flowrateMx` = **9 file** | ✅ EXACT (klaim ketiadaan terbukti) |
| A5 | Ukuran artefak 349.851 B / 13.650 B | `stat` | 349851 / 13650 | ✅ EXACT |

### D1b — BHARUN (t_07d76f62)

| # | Isi klaim | Metode verifikasi | Hasil | Catatan |
|---|---|---|---|---|
| B1 | 161 file, `dullingInfo`/`dullGrade`/`bitName` = 0 | grep `-l` sendiri ke 161 file primer | 161 file; **0 / 0 / 0** | ✅ EXACT (klaim "label dull tidak ada" terkonfirmasi primer) |
| B2 | dTimStart 161, dTimStop 114, startDrilling 15, stopDrilling 10, window lengkap **9** | regex `<dTim*>` per file (auditor) | 161 / 114 / 15 / 10 / **9** | ✅ **5 angka EXACT** |
| B3 | **6** run durasi negatif (contoh F-15 C: stop 2013-11-07 < start 2013-11-08) | parse timestamp sendiri | **6**, contoh ekstem sama persis (1.xml 2013-11-08T23:15 → 2013-11-07T13:01) | ✅ EXACT |
| B4 | CSV 161 baris | pandas | 161 | ✅ |

### D1c — TRAJECTORY + WBGEOMETRY (t_315c30b1)

| # | Isi klaim | Metode verifikasi | Hasil | Catatan |
|---|---|---|---|---|
| C1 | 63 file trajectory + 27 wbGeometry | glob | 63 + 27 | ✅ |
| C2 | 5561 `<trajectoryStation>`, 109 `<wbGeometrySection>` | regex primer | **5561** / **109** | ✅ EXACT |
| C3 | "incl dan azi uom campuran: **2574 rad + 2987 dega** (dari 5561 station)" | grep `<incl uom=…>` + `<azi uom=…>` | incl: **2574 rad + 2987 dega EXACT**; azi: 2574 rad + **2920 dega** (total tag `<azi>` = 5494; 67 station tanpa tag azi) | ⚠️ **setengah salah**: angka 2574/2987 hanya cocok untuk `incl`; untuk `azi` tidak (lihat §8b-4) |
| C4 | `mdInclAzimType` absen; aziRef grid north 50 / true north 11 | grep sendiri (format elemen `<aziRef>…`) | **0** kemunculan; **50** grid north, **11** true north | ✅ EXACT |
| C5 | 8 CSV parser lama = 7.080.457 baris; 5.669.005 bisa dikoreksi TVD (80,1%) | `wc -l` 8 CSV primer: Σ=7.080.465 − 8 header = **7.080.457**; `v6_d1c_tvd_coverage.json` Σ correctable = **5.669.005** (80,1%) | ✅ **kedua angka EXACT** |

### D1d — MUDLOG (t_880f6e22)

| # | Isi klaim | Metode verifikasi | Hasil | Catatan |
|---|---|---|---|---|
| D1 | 8 file; ukuran 120/162/408/448 KB + 1.10/566/441/367 KB | `stat` 8 file primer | 120137 / 161876 / 407853 / 447689 / 1100238 / 565842 / 440715 / 367466 B | ✅ **8/8 ukuran cocok** |
| D2 | 2882 `geologyInterval` | regex primer | **2882** | ✅ EXACT dari file mentah |
| D3 | Distribusi kemunculan litologi: 1194/1156/780/227/216/20/15/5/4 | parse `<lithology>` sendiri | claystone 1194, sandstone 1156, limestone 780, marl 227, siltstone 216, dolomite 20, no sample 15, coal 5, tuff 4 | ✅ **9/9 EXACT** |
| D4 | Litologi primer per interval 957/884/678/178/151/17/10/5/2 (Σ=2882) | pandas atas CSV | 957/884/678/178/151/17/10/5/2 | ✅ **9/9 EXACT** |
| D5 | qualifier 1532 (53,2%), chromatograph 1316 (45,7%), mudGas 576 (20%), **gas show 17 dari 576** | hitung ulang `gasAv > 1.5×gasBackgnd` dari CSV | 1532 / 1316 / 576 / **17** | ✅ **4 angka EXACT** (termasuk ulang-rumus gas show) |
| D6 | "bukan label kegagalan; tidak ada kurva stuck/losses/kick" | grep struktur tag (auditor: tidak ada tag kegagalan di 8 file) | ✅ konsisten | Non-sirkular, lihat §5 |

### D1e — LOG XML 7150 file (t_c74f2838)

| # | Isi klaim | Metode verifikasi | Hasil | Catatan |
|---|---|---|---|---|
| E1 | 7150 file log XML | `os.walk` sendiri | **7150** | ✅ |
| E2 | F-1 C 2156 + F-11 1750 = **3906 = 54,6%** belum diparse | hitung per direktori sendiri | 2156 / 1750 / 3906 / **54,6%** | ✅ EXACT |
| E3 | indexType 6075 date time / 1075 measured depth | dari artefak penulis `v6_d1e_scan_indexType.json` (isi 7150 entri, distribusi 6075/1075) | konsisten | ⚠️ sebagian: auditor tidak mengulang scan header 7150 file (lihat §8c-1) |
| E4 | parser lama = 8 CSV | `ls witsml_parsed/*.csv` | **8** (F-14, F-15A, F-15_S, F-5, F-7, F-9, F-9_A, VAR_F-5_alt) | ✅ |
| E5 | sample 24 file = 1022 kurva | pandas | 1022 | ✅ |
| E6 | WHIRL_RT di **67** file, 5 wellbore (23/19/16/5/4); BOUNCE_RT **70** file; keduanya **67** | **ripgrep `-l` sendiri** atas 19 GB primer | WHIRL **67 EXACT**; BOUNCE **70 EXACT**; both **67 EXACT**; F-9 23 / F-14 19 / F-5 16 / F-15S 5 / F-1 4 | ✅ **3/3 EXACT (primer, tool berbeda)** |
| E7 | WHIRL == BOUNCE identik 1790/1790 di F-9 `…/1/log/1/2/1/00005.xml` | parse `<data>` + `<mnemonicList>` sendiri pada file yang sama | 10000 baris, 1790 non-null bersama, **1790 identik / 0 beda** | ✅ EXACT |

### D1f — PETRO DLIS/LIS (t_f5506e30)

| # | Isi klaim | Metode verifikasi | Hasil | Catatan |
|---|---|---|---|---|
| F1 | 24 file log = 20 DLIS + 2 LIS + 2 LAS (koreksi "16 DLIS" di body task) | hitung ekstensi sendiri | **20 / 2 / 2** | ✅ EXACT — koreksi D1f benar |
| F2 | Magic DLIS `1V1.00RECORD08192PETROLOG`, LIS berheader `EDIT` | baca byte pertama sendiri | F-5 DLIS: `   1V1.00RECORD08192PETROLOG…`; F-7 LIS: `…45444954…` = "EDIT" | ✅ EXACT |
| F3 | 21 CSV = **309.644** baris | hitung baris semua 21 CSV sendiri | **309644** | ✅ EXACT |
| F4 | Per-file (F-14 LIS 18374×49, F-15D 33464, F-5 composite 23657, dst.) | baris per file (auditor) | semua 21 file cocok tabel §3 | ✅ **21/21 cocok** |
| F5 | F-7 LIS korup, error asli `head.prev(=457) != prev(prev(head)).next(=362)`, indexing berhenti di offset 461 | **jalankan ulang `dlisio.lis.load()` sendiri** | RuntimeError dengan pesan **karakter-identik** + "stopped at physical tell 461" | ✅ **direproduksi penuh** — blocker nyata, bukan karangan |
| F6 | 6 wellbore COMPUTED_OUTPUT + flag `CARB_FLAG`/`COAL_FLAG` | daftar CSV OUTPUT | **6** file OUTPUT; kolom CARB_FLAG/COAL_FLAG ada | ✅ |

### D1g — EDM (t_44b03f90)

| # | Isi klaim | Metode verifikasi | Hasil | Catatan |
|---|---|---|---|---|
| G1 | `Volve F.edm.xml` 211.263.929 B | `stat` | **211263929** | ✅ EXACT |
| G2 | Keyword **0 hit**: `non-productive`, `bit run`, `lost circulation`, `well control`, `drilling report` | grep `-o -i` sendiri | **0 / 0 / 0 / 0 / 0** | ✅ **5/5 EXACT** |
| G3 | `failed` = 416 hit, semua base64 (tes konteks 40-karakter kosong) | **metode identik penulis**: `grep -o -i '.{40}failed.{40}'` | 416 hit `-i`; konteks 40-char = **0** (konteks 10-char = 416) | ✅ **EXACT — klaim & metode tereproduksi** |
| G4 | `stuck` 947, `kick` 3539, `NPT` 130 | 6 metode alternatif (occurrence `-i`/cs, baris, word-boundary, token atribut) | stuck: 968/966 occurrence, 945 baris, token = 945 `stp_calc_stuck_point`+12 `stp_md_when_stuck`+9 `stp_mw_when_stuck`; kick: 5103/3198 occurrence, `kick_*` attr 3193; NPT: 3331/370, baris 41, word-boundary **0** | ⚠️ **angka persis 947/3539/130 tidak tereproduksi** (§8b-5). **Sifat klaim tetap benar**: semua temuan = atribut simulasi/bit/ID acak, word-boundary NPT = 0 (bukan tag/tabel NPT) |
| G5 | 8 tag kunci: CD_PORE_PRESSURE 39084, CD_FRAC_GRADIENT 37257, CD_DEFINITIVE_SURVEY_STATION 15109, CD_ASSEMBLY_COMP 10650, CD_HOLE_SECT 2741, CD_BHA_COMP_BIT 632, CD_NBK_LEAK_OFF_TEST 442, WP_TDA_DRAGCHART 18154 | grep `<tag ` sendiri | **39084 / 37257 / 15109 / 10650 / 2741 / 632 / 442 / 18154** | ✅ **8/8 EXACT** |
| G6 | README 272 byte | `stat` | **272** | ✅ EXACT |
| G7 | Folder kosong sengaja: CasingSeat/CasingWear/Compass/WellPlan (`left_intentionally_empty.txt` 0 byte) | `find` (audit batch A pada struktur) | konsisten dengan struktur dbx_volume | ✅ |

### D1h — KAGGLE + CATALOG (t_13e3a454)

| # | Isi klaim | Metode verifikasi | Hasil | Catatan |
|---|---|---|---|---|
| H1 | time.csv **419.747** baris data, **239** kolom | `wc -l` + `csv.reader` sendiri | 419748 fisik − 1 header = **419747**; **239** kolom | ✅ EXACT |
| H2 | depth.csv "16.672 total (1 header + **16.671** data; wc -l = 16671 karena baris terakhir tanpa newline)" | cek byte: newline = 16671, **file berakhir `\\n`** → 16671 baris fisik = 1 header + **16670 data**; `csv.reader` = 16670 | ❌ **SALAH** (§8b-1): data = 16670, bukan 16671; penjelasan "tanpa newline" juga salah | |
| H3 | ROP data .csv = **152** baris data | `zipfile` baca langsung dari zip primer | 152 baris TOTAL = 1 header + **151 data** | ❌ **SALAH off-by-one** (§8b-2); **D2 menulis 151 = benar** → inkonsistensi internal tim |
| H4 | catalog 4035 baris × 4 kolom | `csv.reader` | **4035 × 4** | ✅ EXACT |
| H5 | Well_picks: 557 baris, 35 well, **409 pick** | parse penuh `.dat` primer | 557 / 35 section / **409 pick** / 35 well ber-pick | ✅ **3 angka EXACT** |
| H6 | Zip kaggle F9A = duplikat identik (ukuran byte sama) | keberadaan kedua salinan + ukuran | konsisten (5.596.360 B depth di kedua lokasi) | ✅ |
| H7 | STUCK_RT + MWD shocks ada di time.csv | baca header primer | `STUCK_RT unitless` (kolom 109), `MWD Total Shocks` (23) ada | ✅ |

### V6-D0 — SINTESIS (t_dc129046)

| # | Isi klaim | Metode verifikasi | Hasil | Catatan |
|---|---|---|---|---|
| O1 | "Semua angka kunci 8 pembaca COCOK hitung ulang ulang" (192/161/63/27/8/7150; 20 DLIS+2 LIS; CSV 1392/161/5561/2882/1022; D1f 309644) | seluruhnya dihitung ulang independent di atas | **semua cocok** | ✅ klaim agregasi terverifikasi |
| O2 | "EDM bukan event/NPT DB (keyword 0; stuck 947 simulasi; kick 3539)" | batch B/B2/B3 | keyword-0 ✓; angka spesifik tidak tereproduksi (G4) | ⚠️ mengulang angka D1g yang tidak terepun­duksi |
| O3 | "USROP 49.732 / 15.183 / **49.629**" | cek `USROP_labeled.csv` + telusuri R1 | kolom `label` aktual = **134013 / 49732 / 15183**; angka **49629** = kelas "torsional anomaly" R1 §4.2 (rule CV torsi), BUKAN kolom `label` yang sama; recompute auditor: ddof=0 → **49614** (Δ15 = 0,03%), ddof=1 → 50031 | ⚠️ **menyesatkan bila dibaca sebagai 1 distribusi kolom** (§8b-6); angka sendiri traced, bukan karangan |
| O4 | "Tidak ada pembaca yang melapor 'belum dibuka' terhadap file yang ada di disk; 8/8 terbit dengan angka primer" | audit artefak §3 | **benar** | ✅ |
| O5 | Klaim "rating motor 0/192", "dullingInfo 0/161" | batch B | ✅ independent EXACT | ✅ |

### V6-D2 — DATASET EKSTERNAL (t_5c834a19)

| # | Isi klaim | Metode verifikasi | Hasil | Catatan |
|---|---|---|---|---|
| X1 | #3 Haytham: xlsx 14.228 + 14.607 B; sheet 104×8 → **103 baris**; biner **77/26**; multiclass 10 tingkat; tanpa LICENSE | **unduh sendiri** dari raw.githubusercontent (master) + openpyxl | 14228 / 14607 B; 104×8; **103** baris; **0=77, 1=26**; label 0.0–0.9 + 1.0; daftar isi repo tanpa LICENSE | ✅ **SEMUA EXACT** |
| X2 | #1 Mendeley: 8 file; T01_R01 sheet **60.505×4**; header `Sample No., X, Y, Z`; 490 RPM; Feed 0.285; Tool 1 Run 1; CC BY 4.0 | **unduh sendiri** T01+T02 via API; cek sha256 | 8 file ✓; T01 = **60505×4 EXACT**; header/kondisi EXACT; **sha256 T01 & T02 MATCH** (menutup celah "(a) sha256 belum dicek" di §5 dokumen D2) | ✅ |
| X3 | Handoff D2: "60.504 baris/file" | cek T02 | T02 = **50005** baris | ❌ **generalisasi salah** — baris beda per file (§8b-7); dokumen D2 sendiri hanya klaim T01 (benar) |
| X4 | #2 XAI Kaggle: zip 292.793 B; CSV 1.107.906 B; **20.000 × 14 kolom**; Main Failure 18999/1001; BEF 215 / CCF 344 / FWF 278 / WDF 300 | **unduh sendiri** (API Kaggle tanpa auth) + pandas | zip **292793 EXACT**; CSV **1107906 EXACT**; **20000** baris ✓; **18999/1001 EXACT**; **215/344/278/300 EXACT**; kolom aktual **15** (ID + 14) | ⚠️ hanya jumlah kolom salah (§8b-3); sisanya EXACT |
| X5 | #11 Frontiers 2026: data **tidak publik** ("not publicly available … permission from Dolph and Dode Offshore"), 297 obs/13 var | `web_extract` halaman paper | kutipan **verbatim cocok**; 297 samples/13 features ✓ | ✅ klaim negatif benar |
| X6 | Repo `promiseeee` = Volve-derived **tanpa** kolom label | tidak diunduh ulang; dicek D2 sebagai hasil negatif | — | (c) belum diuji ulang auditor — lihat §8c-4 |

---

## 3. UJI "DIBUKA BENERAN" — bukti raw output per dokumen (prosedur 2)

| Dokumen | Artefak parse di disk (dicek auditor) | Kutipan raw di dokumen | Verdict |
|---|---|---|---|
| D1a | `scratch/v6_d1a_tubular.csv` (349.851 B) + `_summary.json` (13.650 B); **13 script** di workspace t_80ba3ae3 (daftar persis §10 dokumen) | APPENDIX 3 file XML utuh + kutipan 3 assembly | **KUAT** |
| D1b | `scratch/v6_d1b_bharun.csv` (35.881 B); 2 script | kutipan struktur XML + 2 contoh file | **KUAT** |
| D1c | 4 artefak (`trajectory/wbgeom/traj_summary.csv`, `tvd_coverage.json`); 5 script | kutipan 3 station + snippet XML mentah | **KUAT** |
| D1d | `scratch/v6_d1d_mudlog.csv` (1.034.069 B); 2 script | diagram struktur tag + tabel 8 file (ukuran terverifikasi §2 D1d-1) | **CUKUP** — tanpa kutipan XML verbatim, tapi ukuraan+regex primer auditor cocok |
| D1e | `v6_d1e_log_sample.csv` + `v6_d1e_scan_indexType.json` (1,4 MB); 12 script; **5 raw_dumps**; `pass_c_missing.json`, `pass_e_whirl_data.json` | 2 deskripsi raw dump | **KUAT** |
| D1f | **21 CSV (77 MB)** + **5 JSON bukti** di `scratch/v6_d1f/`; 20+ script | traceback/error asli (direproduksi auditor) | **KUAT** |
| D1g | 4 script (persis §8); README 272 B terverifikasi; XML 211 MB terbuka grep | kepala XML + README + daftar atribut | **KUAT** |
| D1h | tanpa CSV turunan (probe saja: 4 script), **tapi** file primer (time/depth/catalog/picks) langsung dibuka ulang oleh auditor dan semua angka diuji | angka byte/kolom presisi | **CUKUP** — klaim terverifikasi langsung ke primer |
| D2 | `cache/scratch/v6d2/` berisi unduhan nyata (xlsx, csv, ~15 JSON API) + workspace `raw/`, `samples/`, 8 script | tabel per kandidat dengan ukuran byte | **KUAT** — ditambah unduhan ulang auditor |

**Jawaban prosedur 2: 8/8 dokumen pembaca punya bukti parse nyata; tidak ada dokumen yang hanya narasi.**

---

## 4. HITUNG ULANG ANGKA KUNCI (prosedur 6 — minimal 5)

Berikut ringkasannya (rincian di §2; ≥20 angka kunci dihitung ulang, alih-alih 5):

1. Jumlah file primer: 192 / 161 / 63 / 27 / 8 / **7150** (Python glob+walk) — cocok 6/6.
2. Baris CSV pembaca: 1392 / 161 / 5561 / 2882 / 1022 / **309644** (pandas) — cocok 6/6.
3. 8 CSV parser lama: Σ wc − 8 = **7.080.457** — cocok.
4. time.csv **419747×239**; depth.csv **16670** (bukan 16671); catalog **4035×4**; picks **409/35**.
5. Populasi kelas: litologi primer mudLog 9 kelas EXACT; gas show **17/576**; USROP label 134013/49732/15183; STUCK_RT time.csv 0/1/2/3 = 23123/3171/363/19058.
6. Tag EDM 8/8 EXACT; tag primer WITSML 1392/192/5561/109/2882 EXACT.

---

## 5. UJI SIRKULARITAS TIAP KANDIDAT LABEL (prosedur 3)

Metode: `DecisionTreeClassifier` tanpa batas depth → split 75/25 (seed 0) → **akurasi holdout**. Kalau label = fungsi deterministik fitur, rekonstruksi ≈ 100%. (Train-acc sengaja TIDAK dipakai sebagai kriteria: tree tak terbatas selalu hafal data latih.)

| Kandidat label (penawar) | Fitur yang diuji | Hasil | Verdict |
|---|---|---|---|
| **Litologi mudLog** (D1d/D0 §2.4 "label litologi 100%") | rop/wob/tq/rpm/mudweight/ECD/dxc (n=1578) | train 98,3% · **holdout 66,3%** (+MD: 70,6%) | ✅ **NON-SIRKULAR** — litologi tak bisa direkonstruksi dari parameter drilling; klaim D0 §5.4 "non-sirkular" **terbukti empiris** |
| **STUCK_RT time.csv F-9 A** (D1h, ranking D0 #2) | ROP/WOB/RPM/torque/hookload/SPP (n=10998, 4 kelas, tanpa NaN) | train 100% (hafalan) · **holdout 92,1%** | ✅ **NON-SIRKULAR** — 92,1% < 100%; label instrumen bukan fungsi fitur. Ketinggian akurasi justru konsisten dengan premis proyek (AUC surface→stuck 0,96–0,98) |
| **Flag DLIS COMPUTED_OUTPUT** `CARB_FLAG`/`COAL_FLAG` (D1f) | kanal OUTPUT lain: PHIF/SAND_FLAG/SW/VSH/KLOGH/BVW | holdout **97,7% / 99,9%** | ⚠️ **SIRKULAR BERSYARAT** — nyaris deterministik antar kanal petro COMPUTED. Sirkular KALAU kanal petro dipakai sebagai fitur; aman KALAU fitur = parameter drilling/WITSML (kanal OUTPUT tidak memuat parameter drilling) |
| **Label rule R1 / USROP** (`high_MSE_bit_wear`, `low_ROP_efficiency`, torsional-CV) — "rumus R1" | kolom fitur USROP yang sama (n=198928) | holdout **99,97%**; rekonstruksi `MSE` dari fitur: **R² = 0,99987**; kelas torsional = rule(Torque) murni | ❌ **SIRKULAR by construction** — label = fungsi deterministik fitur (rumus Teale MSE & CV torsi dihitung dari kolom yang sama). Model yang dilatih fitur USROP → label rule R1 **hanya akan mereproduksi rule** |
| Label litologi DLIS `VSH`/`SW` (kontinu) | kanal OUTPUT lain | holdout 4,1% / 70,9% | ✅ nilai kontinu tidak bisa direkonstruksi tree → non-sirkular untuk regresi (tapi lihat catatan flag di atas) |
| **EDM / bhaRun** sebagai label | — | — | **N/A** — tidak ada label yang ditawarkan (D1g menolak eksplisit dengan bukti grep; D1b: numBitRun bukan target). Klaim "EDM = fitur, bukan label" justru menghindari sirkularitas |
| **409 formation picks** (D1h) | — (logis) | sumber berbeda (interpretasi well tie) vs fitur drilling | ✅ non-sirkular per sumber; **catatan desain**: top formasi ≈ fungsi kedalaman per well → hati-hati *depth-leak* kalau MD jadi fitur |

**Rekomendasi wajib untuk V6-E1:** larang melatih fitur USROP → label rule USROP/R1 (sirkular, holdout 99,97% =
bukti model belajar rule, bukan kegagalan). Prediksi yang sah = fitur sumur/wellbore LAIN (mis. time.csv F-9 A,
WITSML F-1 C/F-11) → label, atau kanal instrumen → label lintas sumber.

---

## 6. DATASET EKSTERNAL — unduhan mandiri (prosedur 5)

| Kandidat (D2) | Klaim | Unduhan auditor | Hasil |
|---|---|---|---|
| #3 Haytham stuck-pipe | 103 baris, 77/26, tanpa lisensi | 2 xlsx dari raw.githubusercontent (HTTP 200) | ✅ **cocok semua** |
| #1 Mendeley tool wear | 8 file, T01 60505×4 | T01 (2.860.325 B) + T02 (2.357.353 B) via public-api | ✅ cocok; **sha256 MATCH** |
| #2 XAI Kaggle | zip 292793, 20000×14, 18999/1001, 4 flag | zip via Kaggle API tanpa auth | ✅ cocok (kolom 15, bukan 14) |
| #11 Frontiers 2026 | data tidak publik | `web_extract` paper | ✅ kutipan verbatim cocok |

→ **3 kriteria terpenuhi lewat gabungan** (stuck pipe #3 + wear #1 + multi-mode failure #2) tetap berlaku;
semua pemenuh kini terverifikasi unduhan BERULANG oleh pihak kedua (auditor).

---

## 7. JEJAK SIZZLE (prosedur 4)

Pemindaian baris ber-kerja-verbal ("bisa dipakai/berguna/potensi/kandidat layak") **tanpa angka** di 10 dokumen:
**3 kandidat baris**, semuanya header tabel / lanjutan kalimat (`V6_D1g` baris 213, `V6_D1h` baris 57, `V6_D0` baris 39) —
bukan klaim. Klaim "bisa dipakai untuk X" yang lain semuanya membawa angka baris/kolom yang kemudian diverifikasi §2.
**Verdict: jejak sizzle minimal; tidak ditemukan klaim utilitas tanpa angka yang material.**

---

## 8. TEMUAN TERUS TERANG

### (a) TERVERIFIKASI BENAR (ringkas)
- **Seluruh kerangka inventaris 8 pembaca**: jumlah file, jumlah baris, jumlah kolom, populasi kelas, tag
  ketiadaan (rating motor, label dull), coverage gap 54,6%, TVD 80,1% — semua EXACT dengan tool berbeda.
- **"EDM bukan event/NPT DB"**: 5 keyword = 0 hit; `failed` 416 + tes konteks-40 identik; seluruh tag `stuck`/`kick`
  = atribut simulasi/bit; `NPT` word-boundary 0. **Verdict kualitatif terbukti dengan tes pembeda.**
- **Blocker F-7 LIS**: error direproduksi karakter-identik dengan dlisio 1.0.4 di mesin auditor.
- **WHIRL_RT == BOUNCE_RT**: WHIRL 67 file / BOUNCE 70 file / keduanya 67 (distribusi 23/19/16/5/4) +
  1790/1790 identik — primer, ripgrep auditor.
- **Semua artefak parse nyata** (21 CSV 77 MB, JSON bukti, raw dumps, script) — 8/8 dokumen lolos uji §3.
- **D2**: 4 unduhan independen cocok; klaim negatif Frontiers verbatim; sha256 Mendeley MATCH.

### (b) TERBUKTI SALAH / TIDAK AKURAT (wajib dikoreksi sebelum ke dosen)
1. **D1h depth.csv**: klaim "16.671 baris data, wc -l=16671 karena baris terakhir tanpa newline" → file
   **berakhir newline** dan berisi **16670 baris data**. Dua-duanya salah (angka + penjelasan).
2. **D1h ROP data**: klaim **152 baris data** → aktual **151** (152 = termasuk header). Dokumen **D2 sendiri
   menulis 151 = benar** → kontradiksi internal; D1h yang perlu dikoreksi.
3. **D2 XAI**: "20.000 baris × **14 kolom**" → kolom aktual **15** (daftar kolom di dokumen D2 pun berisi 15 item).
4. **D1c**: "incl **dan azi** uom campuran 2574 rad + 2987 dega" → EXACT hanya untuk `incl`; `azi` = 2574 + **2920**
   dega (67 station tidak punya tag `azi`). Klaim gabungan tidak akurat untuk azi.
5. **D1g angka keyword `stuck`=947, `kick`=3539, `NPT`=130**: **tidak terepun­duksi** dengan 6 metode berbeda
   (nilai terukur auditor: 945–968 / 3193–5103 / 41–370 tergantung metode). Sifat klaim (false positive,
   simulasi, bukan tag) terbukti benar — tapi **angka pastinya tidak bisa dipertanggungjawabkan apa adanya**;
   samakan metode atau ganti dengan angka terukur sebelum dikutip ke dosen.
6. **D0 §2.4** "USROP 49.732/15.183/49.629" menyesatkan bila dibaca sebagai satu distribusi: kolom `label`
   USROP_labeled.csv = **134013/49732/15183**; 49629 adalah kelas rule **terpisah** dari R1 (recompute auditor
   49614, Δ0,03% — angkanya sendiri bukan karangan).
7. **Handoff D2** "60.504 baris/file" → generalisasi salah (T01=60505, T02=50005); dokumen D2 sendiri benar.
8. Minor: **D1f** tertulis "Tanggal: 2026-10-05" — kartu dieksekusi 2026-10-10 (typo tanggal).

### (c) TIDAK BISA DIVERIFIKASI (jujur, tanpa spekulasi)
1. **D1e distribusi indexType 6075/1075 per file**: konsisten dengan artefak penulis, tapi auditor tidak
   mengulang scan header semua 7150 file (19 GB; scan independen diprioritaskan untuk WHIRL_RT yang hasilnya 67=EXACT).
2. **Statistik agregat turunan D1a** (median error formula −14,80%, per-tipe 9 baris, total 267.412,1 m) dan
   **tabel per-wellbore D1a/D1c** — tidak dihitung ulang per sel (sampel inti sudah EXACT; audit berhenti di
   minimum cukup).
3. **Per-kanal valid D1f** (mis. RHOB 5664/23657) — diverifikasi struktur & jumlah baris file, bukan tiap sel kanal.
4. **D2 kandidat #6–#10** (Utah FORGE, promiseeee, bit-wear Kaggle, MSEEL) — tidak diunduh ulang; minimal-1 syarat
   sudah dilewati 4 unduhan. Klaim negatif promiseeee (tanpa kolom label) diterima dari D2 tanpa uji ulang.
5. **Overlap depth mudLog vs USROP** — belum diverifikasi siapa pun (D1d sendiri menandai "belum diverifikasi");
   USROP_labeled.csv kini terkonfirmasi ada di `data/USROP/` → pekerjaan terbuka, bukan klaim.
6. **D1f F-14 LIS vs referensi SPWLA** — dokumen sendiri menyatakan belum divalidasi silang (keterbatasan jujur).

---

## 9. IMPLIKASI (untuk E1 & sebelum ke dosen)

1. **Jangan kutip ulang 3 angka keyword EDM (947/3539/130) dan 2 angka off-by-one D1h** sebelum dikoreksi —
   daftar §8b adalah koreksi wajib. Angka lain aman.
2. **Larangan sirkularitas untuk E1**: fitur USROP → label rule R1 = ghost-model (holdout 99,97% = reproduksi rule).
   Pakai lintas sumber (fitur sumur lain → label) atau kanal instrumen sebagai target.
3. **Flag DLIS COMPUTED_OUTPUT** hanya sebagai LABEL (atau fitur petro terpisah), jangan campur dalam fitur
   drilling saat memakainya sebagai target.
4. **Klaim inti "8 pembaca membuka file" terbukti** — tidak ada yang karangan; V6_D1 lama (fiktif) sudah tergantikan
   oleh 8 dokumen dengan artefak nyata.

---

## 10. LIMIT AUDIT
- Auditor memverifikasi sampel/bukti kuat, bukan setiap sel: daftar lengkap yang belum dicek ada di §8c.
- Uji sirkularitas memakai 1 model (decision tree) — bukti ketidak-rekonstruksian lemah hanya berlaku untuk
  fitur/horisont yang diuji; model lain bisa lebih kuat, tetapi tree tak terbatas adalah uji rekonstruksi yang wajar.
- Scan ripgrep WHIRL/BOUNCE dijalankan atas `witsml_raw` (19 GB); hasil WHIRL 67 file = EXACT, distribusi wellbore EXACT.
- Tidak ada file yang diubah/dihapus; semua audit read-only + unduhan ke workspace sendiri.

**Skrip & bukti mentah audit:** `audit_batch_a.py|b.sh|b2.sh|b3.sh|c.py|c2.sh|c3.py|d.py|d2.py|d3.py|e.py|e2.py|f.py`,
`batch_*_results.txt`, `whirl_files.txt`, `dl_verify/` — semua di workspace task `t_9e5e4f81`.
