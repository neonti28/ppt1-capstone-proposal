# V3 — Data Acquisition Inventory (Volve: BHA runs, mudlog, well logs LAS/MWD)

Tanggal akuisisi: 2026-10-04. Lokasi tujuan: `/mnt/d/Capstone 1/data/volve/external/`
Lisensi sumber data: CC BY-NC-SA 4.0 (Equinor / Volve data sharing) kecuali disebut lain.
Semua klaim di bawah berasal dari output eksekusi pada sesi ini (status HTTP, ukuran byte, jumlah baris).

---

## 1. BERHASIL DIUNDUH

Total: **~103 MB, 88 file data + 1 file indeks (4.035 baris)**.
Semua file `GET` diverifikasi status 200 dan ukuran nonzero; struktur dicek dengan membuka file (bukan hanya `Content-Length`).

### 1.1 `spwla_volve_logs/` — 28 file, 58 MB (sumber: GitHub `andymcdgeo/spwla_volve`)

Log petrofisik Volve asli (mirror repo publik, file identik dengan paket Equinor: nama file sama persis dengan katalog resmi, lihat §3).
Cakupan wellbore target: **F-5, F-7, F-9, F-9 A, F-14, F-15, F-15 A, F-15 B, F-15 C, F-15 D** (10/10 wellbore target tercakup, format .DLIS/.LIS/.LAS + laporan PDF).

| File (prefix well) | Ukuran | Format/isi |
|---|---|---|
| `15_9-F-5__WLC_PETROPHYSICAL_COMPOSITE_1.DLIS` | 4.803.134 | DLIS wireline composite |
| `15_9-F-5__WLC_PETRO_COMPUTED_INPUT/OUTPUT_1.DLIS` | 1.120.684 / 1.120.800 | computed petrophysics |
| `15_9-F-5__PETROPHYSICAL_REPORT_1.PDF` | 189.018 | laporan |
| `15_9-F-7__WLC_PETROPHYSICAL_COMPOSITE_1.LIS` | 524.753 | LIS |
| `15_9-F-9__…COMPOSITE_1.DLIS` | 97.678 | DLIS |
| `15_9-F-9A__…COMPOSITE_1.DLIS` | 429.384 | DLIS |
| `15_9-F14__…COMPOSITE_1.LIS` + `COMPUTED_INPUT/OUTPUT.DLIS` | 3.677.190 / 1.285.000 / 908.852 | LIS+DLIS |
| `15_9-F15__…COMPOSITE_2.DLIS` + `COMPUTED_INPUT/OUTPUT.DLIS` | 6.487.888 / 1.903.424 / 455.460 | DLIS |
| `15_9-F15A/B/C__…` (9 file DLIS) | 3.506.640 … 71.594 | DLIS sidetrack A/B/C |
| `15_9-F15D__WLC_PETRO_COMPUTED_INPUT_1.LAS` | 15.255.718 | **LAS 2.0** — diverifikasi header: `STRT.M 145.9 / STOP.M 4684.9 / STEP.M 0.1` |
| `15_9-F15D__WLC_PETRO_COMPUTED_OUTPUT_1.LAS` | 1.759.612 | LAS 2.0 |
| `15_9-F15D__…COMPOSITE_2.DLIS` | 10.961.480 | DLIS |
| `VOLVE_INVENTORY.xlsx` | 94.165 | indeks per-well: sheet `INVENTORY` + 24 sheet well (semua well target ada: 15_9-F-5, F-7, F-9, F-9 A, F-14, F-15, F-15 A/B/C/D) |
| `Well_picks_Volve_v1.dat` | 74.548 | formation picks |
| `Readme.md` | 428 | sumber |

Semua file diunduh dari `raw.githubusercontent.com/andymcdgeo/spwla_volve/HEAD/…` — 22 file via URL biasa (200), 6 file (F-14, F-15) 404 di URL lalu berhasil via `GET git/blobs/<sha>` — total **28 OK, 0 gagal**.

### 1.2 `kaggle/` — 4 file, 44 MB (sumber: Kaggle API **tanpa kredensial**)

| File | Ukuran | Isi (diverifikasi dengan membuka) |
|---|---|---|
| `kaggle_volve_witsml_F9A.zip` | 40.413.012 | zip resmi dataset `imranulhaquenoor/volve-dataset-well-f-9-a` (parse WITSML → CSV) |
| `Norway-NA-15_47_9-F-9 A depth.csv` | 5.596.360 | **16.671 baris**; kolom: `Measured Depth m, TOFB s, AVG_CONF, MIN_CONF, Average Rotary Speed rpm, STUCK_RT, Corrected Surface Weight on Bit kkgf, Corrected Total Hookload kkgf, MWD Turbine RPM rpm, MWD Raw Gamma Ray 1/s, MWD Continuous Inclination dega, Pump 2 Stroke Rate 1/min, Rate of Penetration m/h, Bit Drill Time h, MWD Gravity Toolface dega, Mud Density Out g/cm3, MWD GR Bit Confidence Flag %, Pump Time h, Shock Rate, HKLO, DRET, Extrapolated Hole TVD m, MWD Gamma Ray (API BH corrected)…` + label bagian `15/9-F-9 A - Main Wellbore / 12.25 in Section - MD Log`. **Ini data MWD/LWD + drilling parameter depth-indexed untuk F-9 A.** |
| `kaggle_drilling_log_dataset_F15.zip` | 6.084 | zip dataset `ahmedelbashir99/drilling-log-dataset` (deskripsi: well 15/9-F-15) |
| `ROP data .csv` | 17.751 | 151 baris; kolom `Depth, WOB, SURF_RPM, ROP_AVG, PHIF, VSH, SW, KLOGH` (depth 3305–…) |

Catatan: di dalam zip F-9 A masih ada `Norway-NA-15_47_9-F-9 A time.csv` (ukuran asli 427.910.797 byte, terkompresi di dalam zip) — belum diekstrak; hanya `depth.csv` yang dikeluarkan untuk irit waktu. Ekstraksi bisa dilakukan kapan saja dari zip yang sudah ada.

Bukti endpoint tanpa login (semua `curl` dengan UA Mozilla + `--http1.1`):
```
GET /api/v1/datasets/list?search=volve                 -> 200 (51.381 B)
GET /api/v1/datasets/download/imranulhaquenoor/volve-dataset-well-f-9-a -> 200 (40.413.012 B)
GET /api/v1/datasets/download/ahmedelbashir99/drilling-log-dataset       -> 200 (6.084 B)
```
Pencarian Kaggle `volve / witsml / mudlog / volve F-14 / las well log volve / 15/9-F-15 / halliburton sperry` → hanya 2 dataset Volve berguna di atas; `mudlog` → `[]` (0 hasil).

### 1.3 `volve_witsml_f0nzie/` — 56 file, 152 KB (sumber: GitHub `f0nzie/volve-drilling`)

WITSML 1.4.1.1 **raw XML** untuk well target: **F-7 dan F-9 (wellbore `NO 15/9-F-9 A`)**.
Isi per well: `_wellInfo`, `_wellboreInfo`, `bhaRun`, `trajectory`, `tubular`, `wbGeometry`, `rig`, `MetaFileInfo/MetaDataFileInfo` (56 OK, 0 gagal).

Bukti isi (dibaca langsung):
```xml
<bhaRuns … version="1.4.1.1"><bhaRun uidWell="432612d4-…" uidWellbore="d1c7a0d7-…" uid="12VIRG33">
<nameWell>NO 15/9-F-9</nameWell><nameWellbore>NO 15/9-F-9 A</nameWellbore><name>15/9-F-9 A-2</name>
<tubular uidRef="12VIRG33">15/9-F-9 A_12VIRG33</tubular><dTimStart>2016-09-29T01:29:00Z</dTimStart>
<numStringRun>2</numStringRun><commonData><sourceName>Baker Hughes</sourceName>…</commonData></bhaRun></bhaRuns>
```
→ **BHA run configurations nyata (bukan simulasi)** untuk F-9 A: 2 file `bhaRun/1.xml`, `bhaRun/2.xml`.
F-7 tidak punya folder `bhaRun` di mirror ini (ada `trajectory`, `tubular`, `wbGeometry`).
Repositori juga memuat WITSML `bhaRun` untuk **15/9-F-4** (5 file) dan `log`/`message` telemetri ratusan MB — tidak diunduh (di luar cakupan 7 wellbore target; bisa diambil nanti).

### 1.4 `volve_catalog_target_paths.csv` — 4.035 baris (metadata, bukan data)

Versi tersaring dari **katalog resmi-terbit-publik** `volve_catalog_v1.csv` (GitHub release `985185/volve-metadata-index` v1.0, 94.665.763 byte, HTTP 200).
Kolom: `category, well, ext, path`. Hitungan:
`bhaRun 175` (161 XML + 14 MetaDataFileInfo.txt), `mudLog 16` (8 XML + 8 txt), `las_target 253`, `dlis_target 468`, `other_target 3.123`.

Katalog asli membuktikan seluruh isi dataset Volve hanya diakses lewat jalur Databricks:
`dbfs:/Volumes/equinor_asa_volve_data_village/public/volve/…` (414.585 baris).

---

## 2. GAGAL / TERBLOKIR (dengan bukti HTTP)

### 2.1 ~~BLOKIR~~ → **TERPECAHKAN 2026-10-05** (lihat §6)

> **UPDATE 2026-10-05:** blokir ini sudah pecah lewat **Databricks workspace #2** (`dbc-58e19cf2-8e52`, PAT user, katalog `equinor_asa_volve_data_village`). Volume `public/volve` diunduh penuh: **17.368 file, 3,32 GB, audit byte-per-byte 0 hilang/0 ukuran salah** (termasuk 161 bhaRun, 8 mudLog, WITSML 27 wellbore, Well_technical_data 222 MB, zip Realtime 2,88 GB). Laporan §6 di bawah. Paragraf lama dipertahankan di bawah ini sebagai arsip alasan blokir lama.

#### (arsip alasan blokir lama — sudah tidak berlaku)

| Target | Status | Bukti |
|---|---|---|
| 161 file `bhaRun/*.xml` (F-1 C 61, F-11 43, F-12 11, F-14 8, F-15 32, F-4 5, F-5 12, F-9 3) | tidak bisa diunduh | hanya tersedia di `dbfs:/Volumes/equinor_asa_volve_data_village/public/volve/WITSML Realtime drilling data/<well>/1/bhaRun/*.xml`. Jumlah XML persis **161** = angka pada paper TADI (arXiv 2605.00060 §Appendix B) → cross-check terpenuhi |
| 8 file `mudLog/*.xml` (isi 2.882 interval mudlog) | tidak bisa diunduh | jalur sama; per wellbore: F-1 C = 4, F-11 = 3, **F-15 = 1**, F-9/F-5/F-14 = 0. (artinya: dari 7 wellbore target hanya F-15 yang punya mudlog WITSML di dataset resmi) |
| 253 file `.LAS` target well (LWD_EWL 43, PRESSURE 45, PRODUCTION LOGS 19, dsb.) | tidak bisa diunduh | `dbfs:/Volumes/…/Well_logs/…` |

Bukti akses resmi = akun:
- `https://www.equinor.com/energy/volve-data-sharing` → **HTTP 200 (325.396 B)**, tetapi satu-satunya link unduhan di halaman itu adalah halaman Marketplace Databricks (ditemukan di HTML: `https://marketplace.databricks.com/provider/006d1a44-e5d8-4d20-8bd7-e9a311106007/Equinor-ASA`).
- `https://marketplace.databricks.com/provider/…/Equinor-ASA` → **HTTP 200 (63.468 B)**, halaman berisi 9× "Login" / 4× "login"; user guide resmi (`/tmp/equinor_guide.pdf`, diunduh dari `equinoropendata.blob.core.windows.net/userguides/…`) langkah 3–4: *"if you are not already logged in, the system will prompt you to **Log in / Sign up** … you can sign-up using your university or company account"*.
- Kesimpulan: **butuh akun manusia — tidak dikerjakan lebih lanjut sesuai batasan.**

### 2.2 BLOKIR — Azure blob Equinor: anonymous list ditolak

```
GET https://equinoropendata.blob.core.windows.net/?comp=list          -> 404 (223 B) <Error><Code>ResourceNotFound</Code>
GET https://equinoropendata.blob.core.windows.net/volve?comp=list     -> 404 (223 B) ResourceNotFound
GET https://equinoropendata.blob.core.windows.net/volve/Volve.zip     -> 404 (223 B)
```
Storage account hidup (balasan XML Azure asli + `RequestId`), tetapi container `volve` tidak ada / list anonymous dimatikan. Satu-satunya blob yang bisa diambil tanpa login dari domain itu adalah `userguides/Equinor%20open%20data%20-%20User%20Guide.pdf` (sudah ada di `/tmp/equinor_guide.pdf`).

### 2.3 BLOKIR — SoDIR FactPages: tidak ada endpoint log/BHA/mudlog

Ditelusuri: `js/Navigation.js?v=48` (200, 5.531 B), `js/Report.js?v=48` (200), halaman wellbore `6184` (F-15, redirect 302 → `https://factpages.sodir.no/en/wellbore/pageview/development/all/6184`, **200, 862.746 B**).

```
GET /api/Search?query=15/9-F-15                        -> 200 (JSON {label,url}, 549 B)
GET /api/wellbore/6184                                 -> 404 (1.245 B, IIS "404 - File or directory not found")
GET /api/Wellbore/pageview/development/all/6184        -> 404 (1.245 B)
GET /api/Report/wellbore/6184                          -> 404 (1.245 B)
GET /api/GetTabInfoPages?TabId=2&Culture=en            -> 200 (1.434 B, halaman intro tab)
GET /wellbore/Attributes                               -> 200 (285.717 B, tabel atribut umum)
GET https://factmaps.sodir.no/map/redirect/wlbDev.ashx?id=6184 -> 200 (5.007 B, peta)
```
Isi halaman pageview (diparse): hanya `<h1>15/9-F-15</h1>` + `<h2>General information</h2>` dan pohon navigasi daftar wellbore. **Tidak ada tabel log/drilling/BHA/mudlog, tidak ada endpoint `Get…` lain** di `Navigation.js`/`Report.js` selain `GetTabInfoPages`, `GetMapCalzoneJavascript`, `Nodes`, `Search`.
→ FactPages = metadata wellbore umum saja; bukan sumber LAS/BHA/mudlog.

### 2.4 BLOKIR — sumber lain yang dicek dan kosong

| Sumber | Hasil |
|---|---|
| Hugging Face API `GET /api/datasets?search=volve` | **200, tepat 3 dataset**, semuanya `bengsoon/*` (DDR, alpaca, alpaca_test) — sudah dimiliki |
| GitHub Code Search `GET /search/code?q=bhaRun+volve` | **401** `{"message":"Requires authentication"}` → pencarian isi-repo butuh token |
| GitHub repo search `volve las / volve witsml / bha runs volve` | 3 / 7 / **0** repositori; tidak ada mirror LAS untuk F-5/F-7/F-9/F-14/F-15 selain `andymcdgeo/spwla_volve` (F-15 D saja yang .LAS, sisanya .DLIS/.LIS) |
| Kaggle (tanpa kredensial) `mudlog`, `volve F-14`, `15/9-F-15`, `halliburton sperry` | 0 hasil relevan |
| Paper TADI (arXiv 2605.00060) full-text | sudah di `/tmp/tadi_full.html`, tidak ada link repo/dataset |

**Strategi yang dipakai (≥4 berbeda, semuanya dieksekusi):** (1) katalog resmi + pencobaan jalur blob, (2) mirror GitHub (`spwla_volve`, `volve-drilling`, `volve-metadata-index`), (3) API Kaggle publik, (4) API SoDIR FactPages + JS endpoint mining, (5) API HuggingFace, (6) web search (`ws`/Tavily).

---

## 3. REKOMENDASI ML DARI FILE BARU

| File baru | Rekomendasi |
|---|---|
| `kaggle/Norway-NA-15_47_9-F-9 A depth.csv` (16.671 baris MWD+drilling) | **ROP prediction / drilling-parameter model untuk F-9 A** (fitur: WOB, Hookload, Turbine RPM, SPM, Mud Density Out; target `Rate of Penetration m/h`). Bisa juga deteksi stuck-pipe (`STUCK_RT` sudah ada sebagai label) dan kalibrasi GR MWD. Join ke `labels_curated_v2.csv` lewat MD + tanggal. |
| `kaggle/ROP data .csv` (F-15, 151 baris) | Sinyal **ROP + petrofisik sintetis (PHIF, VSH, SW, KLOGH)** untuk validasi silang F-15: bandingkan prediksi model pada USROP F-15. Sampel kecil → hanya untuk uji, bukan training utama. |
| `spwla_volve_logs/*.LAS` (F-15 D, 15,3 MB) | **Feature log kontinu** (interpretasi petrofisik computed input) → train log-embedding / proxy porosity-shale, atau ground truth untuk mengevaluasi prediksi dari USROP. |
| `spwla_volve_logs/*.DLIS/.LIS` (10 wellbore target) | Butuh parser (`dlisio` / `lasio` tidak membaca DLIS; pakai `dlisio`). Setelah parsing: **korelasi n-Gamma/RES/DT antar well** untuk transfer learning antar wellbore, dan penambahan fitur static per interval yang selama ini hanya dari USROP. |
| `spwla_volve_logs/VOLVE_INVENTORY.xlsx` | Peta ketersediaan log per well → **feature-availability matrix** untuk pemilihan well train/valid/test, dan bukti cakupan di laporan. |
| `volve_witsml_f0nzie/*bhaRun*` + `tubular` (F-9 A, F-7) | **BHA-as-feature**: join run BHA (numStringRun, sourceName, dTimStart) ke interval ROP → analisis ROP per konfigurasi BHA; kecil (2 run) jadi baseline sebelum data 161 run lengkap tersedia. |
| `volve_catalog_target_paths.csv` | **Sampling plan / gap analysis**: tunjukkan eksak 161 BHA, 8 mudLog, 253 LAS target yang belum ada → justifikasi permintaan akses Databricks + baseline kelengkapan data untuk laporan. |
| `Well_picks_Volve_v1.dat` | Formation tops untuk **stratifikasi interval** (train/test split per formasi, bukan per kedalaman acak). |

---

## 4. YANG BELUM DICEK / BELUM DILAKUKAN (jujur)

1. File `.DLIS/.LIS` belum diparse (belum ada `dlisio` di sesi ini) — header/format baru diverifikasi dengan membaca teks LAS F-15 D dan nama file; isi kurv DLIS belum dibuka.
2. `Norway-NA-15_47_9-F-9 A time.csv` (428 MB) masih terkompresi di zip, belum diekstrak.
3. WITSML `log`/`message` telemetri `f0nzie/volve-drilling` (ratusan MB, 3 well: F-4/F-7/F-9) tidak diunduh — hanya objek `bhaRun/trajectory/tubular/wbGeometry/rig`.
4. Tidak ada cross-check independen untuk klaim bahwa file `spwla_volve_logs` = byte-identik dengan file Equinor di Databricks (hanya nama path yang sama persis dengan katalog; isi asli tidak bisa dibuka tanpa akun).
5. `factmaps.sodir.no` hanya dicek status (200, 5.007 B), isinya peta — tidak ditelusuri lebih dalam kemungkinan ekspor survei/trajektori.
6. Tidak dicek: Zenodo/figshare/OSF (fokus ke GitHub/Kaggle/HF yang terbukti responsif); bisa jadi masih ada mirror di sana.

## 5. ~~REKOMENDASI AKSI MANUSIA (satu-satunya jalur sisa)~~ → SUDAH DIGANTIKAN §6 (akses via PAT workspace #2, tidak perlu aksi manusia lagi untuk Databricks)

1. **Databricks Marketplace** — akun universitas/perusahaan → listing Equinor ASA → "Get Instant Access" (butuh ±1 jam provisioning). Dari situ 161 bhaRun XML, 8 mudLog XML, dan 253 LAS target bisa diambil.
2. **Kaggle kredensial** (`~/.kaggle/kaggle.json`) — tidak wajib (API terbukti jalan tanpa login), tetapi dibutuhkan bila ingin dataset besar lain atau upload hasil.
3. Opsional: GitHub token untuk GitHub Code Search (mencari mirror tersembunyi dengan query `bhaRun`/`mudLog` per nama file).


---

## 6. UPDATE 2026-10-05 — DIBUKA via Databricks Workspace #2 (semua blokir §2.1 TERPECAHKAN)

Akses: `dbc-58e19cf2-8e52.cloud.databricks.com` + PAT milik user (workspace kedua; workspace pertama `dbc-4c03ecb3-eabb` ternyata kosong) + warehouse `/sql/1.0/warehouses/5339789b75cd7e4d`. Katalog `equinor_asa_volve_data_village`, volume `public/volve` + `public/volvezipfiles`.

### 6.1 Unduhan (terverifikasi audit independen)

- **17.368 file, 3,32 GB** → `data/volve/external/dbx_volume/`
- Metode: Files API (`/api/2.0/fs/files/<path>`) + Range-resume + 6 worker + sweeper auto-fix (loop sampai nol)
- Audit akhir (script terpisah dari downloader): `hilang=0, ukuran_salah=0` terhadap inventory 17.368 entri
- Isi utama: **WITSML Realtime drilling data** 11.894 file (2,91 GB) 27 wellbore (log/trajectory/tubular/rig/message/wbGeometry/bhaRun/mudLog) + **Well_technical_data** 5.474 file (0,41 GB, DDR/EDM/HTML/PDF) + zip `Volve - Real Time drilling data 13.05.2018.zip` 2,88 GB (20.086 entri; 18.814 XML time-series)
- File >900 MB (Well_logs 7,4 GB & Seismic TB-an) **sengaja tidak diunduh** — di luar scope budget 15 GB

### 6.2 Ekstrak + parse

- Ekstrak zip → `data/volve/witsml_raw/`: **20.086 file, gagal=0**
- Parse WITSML 1.4 (time-based only; depth-log dipisah & dicatat) → `data/volve/witsml_parsed/`:
  **8 CSV, 7.080.457 baris, 60–281 channel/sumur, 37–48 channel fill ≥50%, errors=0**
- Laporan: `docs/V3_WITSML_PARSE_REPORT.md`; JSON pendukung `_parse_summary/_verify/_coverage.json`

### 6.3 Dampak ke item §4 (yang sebelumnya "belum")

1. DLIS masih belum diparse (tetap) — butuh `dlisio`.
2. ~~time.csv 428 MB belum diekstrak~~ → sudah ada ekstrak setara via zip Realtime (WITSML per wellbore CSV).
3. ~~WITSML log telemetri tidak diunduh~~ → sudah (18.814 XML, 7 wellbore target + varian).
4. Klaim §2.1 (161 bhaRun = angka paper TADI) kini bisa diverifikasi langsung di disk.
5. Zenodo/figshare/OSF tetap belum dicek (tidak perlu lagi untuk jalur utama).

### 6.4 Dampak ke ML

- Fitur time-series (`docs/V3_TS_FEATURES.md`): 661 event × 480 fitur, anti-leakage 4.274.005 baris 0 pelanggaran → dipakai kampanye T2-d/T2-e (lihat `docs/V2_ML_BEAT_CANARY_TS.md` + `CHANGELOG.md` root).
