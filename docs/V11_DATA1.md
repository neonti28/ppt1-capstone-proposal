# V11-D1: UJI KLAIM INVENTARIS DATA KEDUA KANDIDAT vs FILE PRIMER

Task: `t_89935b2f` [Data Engineer] · Board: `capstone-v11-vs` · Tanggal: 2026-10-15 (WIB)
Peran: menguji Bab data kedua kandidat: apakah inventaris dataset yang ditulis benar-benar
sesuai isi disk. Seluruh angka di bawah adalah hasil hitung ulang sendiri dari file primer
(wc, glob, modul csv Python, pembacaan zip, grep substring XML, awk per kolom), bukan kutipan
dari dokumen kandidat maupun dari PM0.

> Riset pendahuluan: `scientific-critical-thinking`: pemisahan data (angka primer) vs
> interpretasi (kelengkapan/akurasi); setiap klaim diberi status bukti (cocok/salah/
> tidak-terverifikasi) dan falsifier-nya dieksekusi, misalnya subset 8 file CSV diuji
> ekshaustif (pasangan dua file yang dikecualikan tidak ada yang berjumlah 1.461.526).
> Riset pendahuluan: `verification-mandatory`: hitung ulang dari sumber primer sebelum
> menilai kandidat; klaim "tidak dapat ditelusuri" hanya ditulis setelah pencarian sumber
> (grep seluruh docs/ + kedua workspace) dan pengujian subset dieksekusi; bagian "belum
> diverifikasi" ditulis eksplisit di §7.
> Riset pendahuluan: `statistical-analysis`: angka inventaris dinilai ketepatan nilainya
> (bukan format pemisah ribuan); pembulatan persentase fill-rate dinilai terhadap nilai
> hitung mentah (mis. 0,668% → klaim 0,67% dinilai cocok).
> Riset pendahuluan: `sequentialthinking` (sequ-mcp, 8 pikiran, 8/8 sukses): rencana
> hitung ulang netral (primer dulu, baru baca kandidat) → sintesis per kandidat →
> keputusan kelengkapan silang → rencana output.

---

## 0. PETA KANDIDAT (kode opaque; identitas versi dirahasiakan)

| Kode | File .md | File .ipynb (pasangan wajib) |
|---|---|---|
| Kandidat 1 | `/mnt/d/Capstone 1(v2)/docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.v3_arsip.md` | `/mnt/d/Capstone 1(v2)/docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.v3_arsip.ipynb` |
| Kandidat 2 | `/mnt/d/Capstone 1(v2)/docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md` | `/mnt/d/Capstone 1(v2)/docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.ipynb` |

Path diperlakukan sebagai kode kandidat, bukan penanda versi. Dokumen ini tidak menyimpulkan
mana versi baru/lama.

---

## 1. ANGKA PRIMER (hasil hitung ulang sendiri dari disk)

JSON primer lengkap: `scratch_d1_primary.json` (workspace task ini; berisi gabungan
`scratch_d1_recount*.json` + `scratch_d1_md_ipynb.json`).

| # | Angka primer | Nilai hasil hitung | Metode eksekusi |
|---|---|---|---|
| P1 | WITSML parsed, 10 CSV di folder | 9.935.698 baris data (9.935.708 baris fisik termasuk 10 header) | `wc -l data/volve/witsml_parsed/*.csv` |
| P2 | WITSML 8 CSV parser V3 | 7.080.457 (9.935.698 − F-10 773.674 − F-12 2.081.567; juga cocok dengan `V3_WITSML_PARSE_REPORT.md` baris 20: "Total: 7,080,457 baris time-series, 8 CSV") | selisih dua file + cross-check dokumen sumber |
| P3 | `USROP_labeled.csv` | 198.928 baris data, 18 kolom; 12 kolom pengukuran (kolom 2–13: MD, WOB, SPP, torsi, ROP, RPM, flow, densitas lumpur, diameter, hookload, TVD, gamma) | `wc -l` + hitung kolom header |
| P4 | `labels_curated_v2.csv` | 884 baris data (modul csv; `wc -l` = 1.413 karena kolom kutipan multiline), 20 kolom; `bha_relevant` yes 50 / no 263 / uncertain 571; kategori 496/216/47/38/28/25/21/12/1 | modul csv Python (DictReader) |
| P5 | WITSML tubular | 192 XML = 192 objek `<tubular>`; 1.392 komponen (tag `tubularComponent` muncul 2.784 kali = 2×1.392 buka+tutup; CSV parse `v6_d1a_tubular.csv` = 1.392 baris data) | find + grep substring |
| P6 | WITSML bhaRun | 161 XML | find path `*/bhaRun/*` |
| P7 | WITSML trajectory | 63 XML; 5.561 stasiun (tag `<trajectoryStation`) | find + grep substring |
| P8 | WITSML wbGeometry | 27 XML; 109 section (tag `<wbGeometrySection` beraatribut) | find + grep substring |
| P9 | WITSML mudLog | 8 XML; 2.882 `geologyInterval`; `chromatograph` 1.316; `mudGas` 576 | find + grep substring per file |
| P10 | Total XML di `witsml_raw` | 18.814 XML + 1.272 file meta (`MetaFileInfo.txt`/`MetaDataFileInfo.txt`) = 20.086 file total ekstrak zip | find `-name *.xml` dan `! -name *.xml` |
| P11 | XML log | 7.150 (find path `*/log/*.xml`) | find |
| P12 | DLIS/LIS terparse | 21 CSV = 309.644 baris data (309.665 `wc -l` − 21 header) di `/mnt/d/Capstone 1/scratch/v6_d1f/csv/` (workspace lama; folder ini tidak ada di V2); raw: 20 `.DLIS` + 2 `.LIS` + 2 `.LAS` = 24 file; F-7 `.LIS` korup gagal parse (V6_D1f §4.2) | `wc -l` 21 CSV + find raw |
| P13 | F-9A time.csv | 419.747 baris data / 239 kolom, ada di isi zip kaggle DAN terekstrak di `data/witsml/Norway-NA-15_47_9-F-9 A time.csv`; kolom ber-prefix `MudPit Volume Average`: 13 (pola berspasi menangkap 11; #3 dan #13 ditulis tanpa spasi); `depth.csv` saudara = 16.670 baris / 115 kolom | modul csv + zipfile; regex `Average\s*\d+` |
| P14 | tool_wear bengkel | 469 jendela (470 baris fisik − 1 header); `toolwear_windows.csv` = 32 kolom = 27 fitur (9 statistik × sumbu X/Y/Z) + 5 kolom meta/label (tool, run, file, start_sample, y) | `wc -l` + baca header |
| P15 | TSPP | TSPP1 21.120 + TSPP2 8.499 + TSPP3 12.533 + TSPP4 10.753 = 52.905 baris data (4 file utama; varian TSPP1-long 59.163 dan TSPP1-15s 5.633 tidak dihitung sebagai data baru) | `wc -l` per file |
| P16 | Formation picks | `Well_picks_Volve_v1.dat`: 557 baris fisik → 409 baris data; 35 blok wellbore (parser blok `Well …`) | parser Python (blok + baris data) |
| P17 | Dataset latih V9 | 6 CSV.gz: vib 23.922 + ssi 35.906 + shk 56.495 + stuck_k1 5.555 + hyd_ki 52.509 + stuck_k2 118.567 = 292.954 baris | hitung baris gzip per file |
| P18 | Fold LOWO | 9+9+9+2+4+4 = 37 fold (`lowo_*.json`) | baca JSON |
| P19 | Anti-bocor | `v9_d1_05_leak_lowo.json`: 0 pelanggaran `feat_ts_max ≥ lab_ts`, 0 baris NaN di 6/6 dataset; wells/folds per dataset 4/9/9/2/9/4 | baca JSON |
| P20 | Fill-rate kanal label | F-7 `SHKRSK_RT` 3.659/547.500 = 0,668%; F-7 `CRPM_RT` 2.769 = 0,506%; F-14 `CRPM_RT` 23.110/1.648.026 = 1,402%; F-14 `VIBLAT_RT` 2.247 = 0,136% | awk per kolom pada CSV |
| P21 | Bin F-14 | `v9_d1_01_summary.json`: n_bins 96.698, n_bins_drill 12.635 (13,1%) | baca JSON |
| P22 | Volume Databricks | `dbx_volume` = 17.368 file | find `-type f` |
| P23 | DDR | `ddr.parquet` = 1.759 baris, 17 kolom | pyarrow.parquet |
| P24 | Katalog Volve | `data/volve/external/volve_catalog_target_paths.csv` = 4.035 baris data (4.036 fisik − 1) | hitung baris |
| P25 | EDM | angka per tabel (39.084 pore pressure / 37.257 frac / 15.109 survey / 10.650 assembly / 632 bit) tercatat di `docs/V6_D1g_EDM.md` baris 102–113; tidak dihitung ulang per-tag oleh penguji ini (status DIDUKUNG) | baca dokumen primer |
| P26 | Kontrol positif stuck | `docs/V9_R1_JUSTIFICATION.md` baris 145: "kontrol-positif 0/10" | grep |
| P27 | Audit klaim kemampuan | `docs/V8_A1_CAPABILITY_AUDIT.md` baris 110: 114/121 klaim numerik terverifikasi persis, 6 selisih penyajian, nihil fabrikasi | grep |
| P28 | Unduhan eksternal + sha256 | `docs/V6_A1_DATA_AUDIT.md` baris 30: "4 unduhan independen sukses (Haytham ×2, Mendeley T01+T02, XAI Kaggle) termasuk verifikasi sha256" | grep |

---

## 2. TABEL VERIFIKASI KANDIDAT 1

File diuji: `...v3_arsip.md` (352 baris; inventaris di §8.1, konversi di §8.2–8.3, sumber di §19.3).

| Klaim kandidat 1 | Hasil verifikasi (primer) | Status |
|---|---|---|
| "8 CSV WITSML berbasis waktu (8.474.172 baris)" (§8.1 baris 127) | Disk (dan workspace lama, identik): 10 CSV total 9.935.698 baris; tidak ada subset 8 file mana pun yang berjumlah 8.474.172 (pasangan yang dikecualikan harus berjumlah 1.461.526; seluruh 45 pasangan diuji, nihil). Sumber primer yang dikutip kandidat 1 sendiri, `docs/V3_WITSML_PARSE_REPORT.md` baris 20, menyebut "7,080,457 baris time-series, 8 CSV". Angka 8.474.172 hanya ditemukan di dokumen proposal kandidat 1 itu sendiri dan salinan lamanya, tanpa primer mana pun | SALAH |
| "USROP 198.928 baris × 12 sensor" | 198.928 baris ✓; 18 kolom total, 12 di antaranya kolom pengukuran (kolom 2–13) sehingga "× 12 sensor" sebagai ringkasan wajar | COCOK |
| "884 label peristiwa terkurasi dari laporan DDR" | `labels_curated_v2.csv` = 884 baris data (modul csv) ✓; log kurasi juga 884 | COCOK |
| "Volume terbuka Databricks: 17.368 berkas" | `dbx_volume` = 17.368 file ✓ | COCOK |
| "20.086 XML WITSML mentah" | 20.086 = total file ekstrak zip; yang ber-XML 18.814, sisanya 1.272 file meta `.txt`. Sumber primer (V3_DATA_ACQUISITION_INVENTORY baris 185) sendiri membedakan "20.086 entri; 18.814 XML time-series" | LABEL TIDAK TEPAT |
| "7.150 log XML" | find `*/log/*.xml` = 7.150 ✓ (cocok eksak) | COCOK |
| "192 tubular; 161 bhaRun; 63 trajectory; 8 mudLog" | 192 ✓, 161 ✓, 63 ✓, 8 ✓ | COCOK |
| "basis data EDM" | Ada: `data/volve/external/dbx_volume/Well_technical_data/EDM.XML/Volve F.edm.xml` (+ zip + readme) | COCOK |
| "4 dataset eksternal terverifikasi dengan checksum cocok (termasuk percobaan keausan alat)" | Tertelusur ke `V6_A1_DATA_AUDIT.md` baris 30: 4 unduhan independen dengan verifikasi sha256 (Haytham ×2, Mendeley T01+T02, XAI Kaggle); Mendeley = percobaan keausan alat ✓. Catatan: angka 4 = jumlah unduhan ulang, bukan jumlah sumber dataset | COCOK (dengan catatan makna) |
| "1.759 laporan DDR" (lini masa §18) | `ddr.parquet` = 1.759 baris ✓ | COCOK |
| "55 fitur dari 11 kanal MWD" (§8.2) | Kontrak 55 = 11 kanal × 5 statistik benar (kode v9_d1_03); namun 11 kanal inti (TQA, SPPA, TFLO, RPM, SWOB, HKLD, ROP, BPOS, SPM, depth, dbtm) mayoritas kanal permukaan/depth, bukan semuanya MWD | COCOK (istilah longgar) |
| "kanal pembentuk label dilarang menjadi fitur (anti-sirkularitas)" + "pemeriksaan kebocoran waktu" (§8.2–8.3) | Konsisten dengan kode `v9_d1_02/03` dan `v9_d1_05_leak_lowo.json` (0 pelanggaran 6/6) | COCOK (konsep) |
| Tier kemampuan "3 Tingkat 2, 2 bersyarat, 2 Tingkat 1, 0 Tingkat 3" | Cocok dengan rekap V8 (0 alarm + 3 peringatan + 2 bersyarat + 2 tren = 7) | COCOK |
| "121 klaim numerik, 0 fabrikasi, enam selisih penyajian" | `V8_A1_CAPABILITY_AUDIT.md`: 114/121 persis, 6 selisih penyajian, nihil fabrikasi | COCOK |
| R3 "kontrol positif stuck 0/10" | `V9_R1_JUSTIFICATION.md` baris 145 ✓ | COCOK |
| R5 "data petrofisik (DLIS/LAS) belum sepenuhnya diekstraksi" | Konsisten: 20/20 DLIS terparse tetapi 1 dari 2 LIS (F-7) korup, dan belum dipakai sebagai fitur | COCOK (jujur) |
| LOWO "dari tujuh sumur, enam latih satu uji … tujuh nilai lipatan" (§11.1) | Skema aktual pipeline V9: 6 dataset dengan 2–9 sumur per dataset, total 37 fold (bukan satu skema 7 fold). Pernyataan kandidat 1 adalah uraian desain generik yang tidak cocok dengan bentuk pipeline yang ada di disk | TIDAK COCOK (sebagai uraian pipeline aktual) |
| Bab data menyebut: DLIS 21/309.644, F-9A 419.747, toolwear 469, TSPP 52.905, picks 409, 292.954 baris latih, 37 fold, 1.392 komponen, 2.882 interval | Tidak disebut sama sekali di kandidat 1 (dicek dengan grep atas 25 angka kunci; semua nol kemunculan di .md maupun sel markdown .ipynb) | TIDAK DISEBUT (bukan kesalahan angka) |

---

## 3. TABEL VERIFIKASI KANDIDAT 2

File diuji: `...ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md` (3.557 baris; Bab 3 = inventaris, §3.1–3.10).

| Klaim kandidat 2 | Hasil verifikasi (primer) | Status |
|---|---|---|
| "10 CSV di folder, 9.935.698 baris; 8 CSV parser V3: 7.080.457; F-10 + F-12: 2.855.241" | `wc -l` 10 CSV = 9.935.698 ✓; 7.080.457 ✓ (P2); 773.674 + 2.081.567 = 2.855.241 ✓; daftar 8 file per nama (F-14, F-15_S, F-5, F-15A, F-7, F-9, F-9_A, VAR_F-5_alt) cocok dengan angka per file di disk ✓; "pipeline V9 memakai 9 CSV" cocok dengan daftar `FILES` `code/v9_d1_01_bins.py` ✓ | COCOK |
| "USROP_labeled 198.928 baris, 18 kolom"; koreksi §3.7 "18 kolom, bukan 115; 115 = kolom depth.csv F-9A (16.670 baris)" | 198.928/18 ✓; depth.csv F-9A = 16.670 baris/115 kolom ✓ eksak; distribusi label 134.013/49.732/15.183 ✓ eksak | COCOK |
| "884 kejadian; 20 kolom; kategori 496/216/47/38/28/25/21/12/1; bha yes 50/no 263/uncertain 571; 1.413 baris fisik sudah direkonsiliasi" | Semua dihitung ulang dengan modul csv: 884 ✓, 20 kolom ✓, seluruh distribusi ✓ eksak, `wc -l` 1.413 fisik ✓ | COCOK |
| "tubular 192 XML, 1.392 komponen; 2 assembly kosong" | 192 ✓; 1.392 komponen ✓ (2.784 substring tag = 2×1.392; CSV parse 1.392 baris); 192−190 = 2 assembly kosong sesuai V6_D1a | COCOK |
| "bhaRun 161 XML, 14 wellbore" | 161 ✓ (jumlah wellbore per-blok tidak dihitung ulang; DIDUKUNG V6_D1b) | COCOK (jumlah file) |
| "trajectory 63 XML, 5.561 stasiun" | 63 ✓; 5.561 `<trajectoryStation` ✓ eksak | COCOK |
| "wbGeometry 27 XML, 109 section" | 27 ✓; 109 `<wbGeometrySection` ✓ eksak | COCOK |
| "mudLog 8 XML, 2.882 interval; chromatograph 1.316/2.882; mudGas 576/2.882" | 8 ✓; 2.882 `geologyInterval` ✓ eksak; 1.316 ✓ eksak; 576 ✓ eksak | COCOK |
| "DLIS/LIS 21 CSV, 309.644 baris (20 DLIS + 1 LIS); F-7 LIS korup" | 21 CSV = 309.644 baris data ✓ eksak (309.665 − 21); raw 20 `.DLIS` + 2 `.LIS`; kegagalan F-7 sesuai V6_D1f §4.2 ✓ | COCOK |
| "F-9A time.csv 419.747 baris, 239 kolom; 13 kolom pit (koreksi §3.7: #3/#13 tanpa spasi; #11 tidak ada)"; "depth.csv 115 kolom, 16.670 baris" | 419.747/239 ✓ eksak (baik di zip maupun file terekstrak `data/witsml/`); 13 kolom pit dengan pola `Average\s*\d+` ✓ eksak; #3 dan #13 memang tanpa spasi, #11 memang tidak ada di header ✓; depth.csv ✓ eksak | COCOK |
| "tool_wear 469 jendela, 27 fitur; distribusi T01 120 (60/60), T02 112 (62/50), T03 121 (60/61), T04 116 (58/58)" | 469 baris data ✓; 27 fitur ✓ (32 kolom = 27 fitur + 5 meta); distribusi per alat tidak dihitung ulang (DIDUKUNG `v6_e1` summary) | COCOK |
| "katalog 4.035 baris"; sumber ditulis `data/volve_catalog_target_paths.csv` | 4.035 baris data ✓; tetapi path sebenarnya `data/volve/external/volve_catalog_target_paths.csv` (ada satu tingkat `external/`) | COCOK (angka); PATH KURANG TEPAT |
| "TSPP 4 CSV utama 52.905 baris (21.120+8.499+12.533+10.753); varian bukan data baru; tanpa kolom label" | Semua ✓ eksak (P15); header 11 kolom tanpa label ✓ | COCOK |
| "Well_picks 409 formation pick di 35 wellbore" | 409 baris data ✓, 35 blok wellbore ✓ eksak | COCOK |
| EDM "39.084 pore pressure, 37.257 frac gradient, 15.109 survey, 10.650 assembly, 632 bit" | Angka persis tercatat di `V6_D1g_EDM.md` baris 102–113 (primer dokumen); tidak dihitung ulang per-tag dari XML EDM oleh penguji ini | TIDAK TERVERIFIKASI (DIDUKUNG dokumen primer) |
| "6 dataset 292.954 baris; 37 fold LOWO (4+9+9+2+9+4); tabel per dataset 23.922/35.906/56.495/5.555/52.509/118.567" | Semua dihitung ulang dari `datasets/*.csv.gz` ✓ eksak; `lowo_*.json` 9+9+9+2+4+4 = 37 ✓ | COCOK |
| "anti-bocor feat_ts_max < lab_ts: 0 pelanggaran di 6/6; baris NaN 0" | `v9_d1_05_leak_lowo.json` ✓ eksak (P19), termasuk wells/folds per dataset sesuai tabel | COCOK |
| "F-14: 96.698 bin menit, 12.635 drilling (13,1%)" | `v9_d1_01_summary.json` ✓ eksak (12.635/96.698 = 13,07%) | COCOK |
| "SHKRSK_RT F-7 0,67%; CRPM_RT F-7 0,51%; F-14 CRPM_RT 1,40%; VIBLAT_RT F-14 0,14%" | Dihitung ulang dengan awk dari CSV: 0,668% / 0,506% / 1,402% / 0,136% ✓ | COCOK |
| Alur konversi: bin 60 detik (ALL-rows, seed 42); fitur `[t0−10, t0)`; label `[t0, t0+10)`; 11 kanal × mean/std/slope/last/frac = 55 fitur; hyd K-i 8 kanal = 40 fitur (SPPA/TFLO/SPM dibuang); stempel well/ts_bin/feat_ts_max/lab_ts/lab_kind | Diverifikasi langsung terhadap kode: `v9_d1_01_bins.py` (bin 60 detik, FILES 9 CSV), `v9_d1_02_rig_windows.py` baris 6–14, 31, 174–175, 202 (jendela, statistik, stempel, cek leak), `v9_d1_03_rig_datasets.py` baris 7–9, 33–36 (FEAT55/FEAT40) | COCOK (1:1 dengan kode) |
| "582 dari 884 kejadian masuk rentang CSV terparse" | Tidak dihitung ulang (butuh join tanggal kejadian vs rentang 9 CSV); sumber internal kandidat tidak menunjuk file primer tunggal | TIDAK TERVERIFIKASI |
| "uidRef bhaRun→tubular cocok 154/161" | Tidak dieksekusi ulang; tercatat di `V7_A1_SOLUTION_AUDIT.md` (DIDUKUNG) | TIDAK TERVERIFIKASI (DIDUKUNG) |
| "32.988 valid" flag DLIS COMPUTED_OUTPUT | Tidak dihitung ulang; tercatat di `V6_D1f_PETRO.md` (DIDUKUNG) | TIDAK TERVERIFIKASI (DIDUKUNG) |
| "SHA-256 8/8 cocok dengan API" (Mendeley) | Tidak dihitung ulang; tercatat di `V6_D2_EXTERNAL_DATASETS.md` (DIDUKUNG) | TIDAK TERVERIFIKASI (DIDUKUNG) |
| "hasil parse 20.086 XML dari zip Realtime" (baris sumber tabel §3.1 #1) | Jumlah XML di zip/ekstrak = 18.814; 20.086 = seluruh entri ekstrak (termasuk 1.272 file meta). Frasa "20.086 XML" longgar, meski angka 20.086 sendiri benar sebagai total entri | LABEL TIDAK TEPAT (satu frasa) |

---

## 4. KELENGKAPAN SILANG (dataset yang disebut salah satu tapi bukan yang lain)

| Dataset / angka primer | Kandidat 1 | Kandidat 2 |
|---|---|---|
| WITSML parsed (jumlah file + baris) | disebut (angka baris salah: 8.474.172) | disebut (9.935.698 + 7.080.457 + rincian per file) |
| USROP | disebut (198.928 × 12 sensor) | disebut (198.928 × 18 kolom + distribusi label) |
| labels_curated 884 | disebut | disebut (+ distribusi kategori/bha) |
| tubular | disebut jumlah file (192) | disebut file + komponen (192/1.392) |
| bhaRun | disebut (161) | disebut (161 + detail field) |
| trajectory | disebut (63) | disebut (63/5.561 stasiun) |
| wbGeometry | TIDAK disebut | disebut (27/109) |
| mudLog | disebut jumlah file (8) | disebut (8/2.882 interval + gas) |
| DLIS/LIS 21 CSV / 309.644 | TIDAK disebut (justru menulis "belum sepenuhnya diekstraksi") | disebut (21/309.644 + keterbatasan) |
| F-9A time.csv 419.747/239 + 13 pit | TIDAK disebut | disebut |
| tool_wear 469 jendela/27 fitur | TIDAK disebut (hanya "percobaan keausan alat" sebagai salah satu dataset eksternal) | disebut |
| TSPP 52.905 | TIDAK disebut | disebut |
| Formation picks 409/35 | TIDAK disebut | disebut |
| Katalog 4.035 | TIDAK disebut | disebut |
| EDM | disebut ("basis database EDM") | disebut (+angka per tabel, DIDUKUNG) |
| 17.368 berkas dbx | disebut ✓ | TIDAK disebut sebagai angka |
| 7.150 log XML | disebut ✓ | TIDAK disebut |
| 20.086 entri ekstrak | disebut (label "XML" longgar) | disebut (label "XML" longgar, satu frasa) |
| 292.954 baris latih + 37 fold | TIDAK disebut | disebut (tabel per dataset) |

Kesimpulan kelengkapan (fakta, bukan vonis skor): kandidat 2 menyebut 15 entri inventaris
dengan angka per entri; kandidat 1 menyebut 10 entri dengan cakupan lebih sempit. Kandidat 1
tidak melakukan kesalahan angka pada entri yang ia sebut kecuali satu angka besar
(8.474.172) dan satu label longgar (20.086 XML); kandidat 2 tanpa kesalahan angka pada entri
yang diuji, dengan satu cacat path (katalog tanpa `/external/`) dan satu frasa longgar
(20.086 XML).

---

## 5. ALUR KONVERSI vs KODE (tugas 4)

| Butir kontrak | Kandidat 1 | Kandidat 2 | Kode primer |
|---|---|---|---|
| Bin 60 detik | tidak disebut (hanya "jendela waktu") | disebut eksak (ALL-rows, seed 42) | `v9_d1_01_bins.py` baris 2: "ekstraksi bin 60 detik dari 9 CSV" |
| Fitur `[t0−10, t0)` | tidak disebut eksak; hanya "statistik jendela waktu … (fitur selalu berstempel waktu lebih awal)" | disebut eksak | `v9_d1_02_rig_windows.py` baris 6 |
| Label `[t0, t0+10)` | tidak disebut | disebut eksak | `v9_d1_02_rig_windows.py` baris 7 |
| 55 fitur (11 kanal × 5 statistik) | disebut ("55 fitur dari 11 kanal") | disebut eksak + hyd 40 fitur | `v9_d1_03_rig_datasets.py` baris 7–8, 33–36 |
| 292.954 baris, 37 fold | tidak disebut | disebut eksak | recount gzip + `lowo_*.json` |
| Anti-bocor `feat_ts_max < lab_ts` | konsep ("pemeriksaan kebocoran waktu") | invariant eksak + tabel 0 pelanggaran | `v9_d1_02` baris 202; `v9_d1_05_leak_lowo.json` |

---

## 6. KONSISTENSI .md vs .ipYNB (per pasangan kandidat)

Metode: sel markdown `.ipynb` diekstrak (JSON modul Python), disambung, lalu dibandingkan
dengan `.md` pasangannya: (a) kehadiran 25 angka kunci per kandidat, (b) garis substansial
`.md` (>25 karakter) yang harus muncul verbatim di sel markdown `.ipynb`, (c) jumlah heading.

| Uji | Kandidat 1 | Kandidat 2 |
|---|---|---|
| Sel markdown / sel code di `.ipynb` | 25 / 12 | 209 / 12 |
| 25 angka kunci: kehadiran sama di md dan ipynb | 25/25 identik | 25/25 identik |
| Garis substansial `.md` yang hilang di `.ipynb` | 0 dari 191 | 0 dari 2.544 |
| Heading `.md` yang hilang di `.ipynb` | 0 dari 43 | 0 dari 208 |

Kesimpulan mekanis: bab data pada kedua kandidat hadir utuh di kedua format; tidak ada
selisih substantif yang terbukti (angka kemunculan identik per nomor kunci).

---

## 7. BELUM DIVERIFIKASI (eksplisit, sesuai aturan bukti)

1. Distribusi per alat tool_wear (T01 120 / T02 112 / T03 121 / T04 116): tidak dihitung
   ulang dari `toolwear_windows.csv` per kandidat; status DIDUKUNG dari summary `v6_e1`.
2. "582 dari 884 kejadian masuk rentang CSV" (kandidat 2): tidak dihitung ulang.
3. uidRef bhaRun→tubular 154/161 (kandidat 2): tidak dieksekusi ulang; DIDUKUNG V7_A1.
4. 32.988 flag DLIS COMPUTED_OUTPUT (kandidat 2): tidak dihitung ulang; DIDUKUNG V6_D1f.
5. SHA-256 8/8 Mendeley (kandidat 2): tidak dihitung ulang; DIDUKUNG V6_D2.
6. EDM per-tag (39.084/37.257/15.109/10.650/632): tidak dihitung ulang dari XML EDM;
   DIDUKUNG V6_D1g.
7. Jumlah wellbore bhaRun "14 wellbore" (kandidat 2): tidak dihitung ulang.
8. Litologi pertama per interval mudLog (claystone 957, dst.): tidak dihitung ulang.

---

## 8. CATATAN METODE DAN KOREKSI DIRI PENGUJI

1. Hitung baris `labels_curated_v2.csv` dengan `wc -l` menghasilkan 1.413 (kolom kutipan
   multiline); dengan modul csv menghasilkan 884. Alat ukur pertama keliru, kebetulan
   sama dengan angka "1.413 baris fisik" yang dikutip kandidat 2 (yang memang menyebut
   angka fisik sebagai bahan rekonsiliasi, bukan jumlah kejadian).
2. Menghitung picks dengan heuristik spasi_awal menghasilkan 463 baris/2 wellbore (salah);
   parser blok `Well …` menghasilkan 409/35 sesuai primer. Hasil alat rusak tidak dipakai.
3. Tag XML `trajStation` dan `wbGeometrySection` dugaan awal salah (0 temuan); tag asli
   `trajectoryStation` dan `wbGeometrySection` beraatribut memberi 5.561 dan 109.
4. Angka 8.474.172 diuji dengan enumerasi seluruh subset 8-dari-10 file (pasangan
   pengecualian), bukan sekadar dibandingkan dengan satu tebakan; nihil cocok, dan sumber
   primer kandidat 1 sendiri menyebut 7.080.457.

---

*Selesai V11-D1 (`t_89935b2f`). Ringkas: kandidat 2 lolos seluruh uji inventaris yang
dieksekusi (semua angka utama terverifikasi eksak dari disk; dua cacat minor: path katalog
tanpa `/external/`, frasa "20.086 XML" longgar); kandidat 1 memiliki satu kesalahan angka
inventaris besar yang tidak dapat ditelusuri ke primer mana pun (8.474.172 baris, bertentangan
dengan sumbernya sendiri yang menyebut 7.080.457), satu label longgar (20.086 XML), cakupan
inventaris lebih sempit, dan satu uraian LOWO (7 fold) yang tidak cocok dengan bentuk pipeline
di disk (37 fold, 2–9 sumur per dataset). md=ipynb konsisten pada kedua kandidat.*
