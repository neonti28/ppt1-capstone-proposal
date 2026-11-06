# V6-D2 — Dataset Eksternal Open-Source Drilling Ber-Label Kegagalan

Status: **SELESAI (diverifikasi unduh)** — 10 Okt 2026
Card: t_5c834a19 (V6-D2, board capstone-v6-solve)
Target: ≥3 kriteria kerusakan/kerusakan-peralatan berbeda (stuck pipe, dysfunctions, bit wear, NPT, fishing, tool failure) dalam SATU dataset ATAU GABUNGAN beberapa dataset, semua di luar Volve yang sudah dipakai.

Riset pendahuluan: web-search-resilience — urutan pencarian dipakai sesuai skill (built-in `web_search` → registry API via `curl -4` → `ws`/`w9` tidak perlu dipanggil karena tier 1 selalu 200); semua panggilan eksternal wajib `curl -4` (akar penyebab HTTP 000 = jalur IPv6 WSL), retry 3×.
Riset pendahuluan: database-lookup — permintaan dibuat eksplisit per-sumber dengan endpoint, filter, dan pagination tercatat (Figshare POST `/v2/articles/search`, Zenodo `/api/records` + `resource_type.type=dataset`, Kaggle `/api/v1/datasets/list`, HF `/api/datasets?search=`, GitHub `search/repositories` + `git/trees/HEAD?recursive=1`, Mendeley `public-api/datasets/th4yv974r2`), hitungan hasil direkonsiliasi per query, tanpa klaim kelengkapan yang tidak diverifikasi.
Riset pendahuluan: grounded-citations — semua URL kandidat didaftarkan ke ledger saat retrieval, bukan saat menulis; blok `Sources` dirender mekanis dengan `sources.py render --cited-in` dan lolos `sources.py verify`.
Riset pendahuluan: drilling-datasets-oilfield — kandidat yang sudah pernah DITOLAK di skill ini tidak diusulkan ulang (Petrobras 3W = label produksi bukan kerusakan BHA; XJTU-SY/CWRU/Paderborn = uji bangku; Saadeldin 2023 data tidak publik), dan pola "unduh sampel dulu, README jangan dipercaya" diikuti untuk tiap kandidat.
> **Riset pendahuluan: `verification-mandatory` — patch koreksi A1 §8b (kolom XAI 15; handoff Mendeley per-file), diverifikasi cepat ulang sebelum ditulis.**

---

## 1. Tabel kandidat (wajib)

| # | Nama | URL | Ukuran | Kolom (hasil pembukaan sampel) | Label | Lisensi | Status verifikasi | Potensi penuhi 3 kriteria |
|---|------|-----|--------|-------------------------------|-------|---------|-------------------|---------------------------|
| 1 | **Drilling tool wear dataset** (Mendeley) | https://data.mendeley.com/datasets/th4yv974r2 (DOI 10.17632/th4yv974r2.1) [1] | 8 file xlsx, **22.498.468 B total**; file contoh T01_R01 = 2.860.325 B | Terbuka: sheet 60.505×4 — `Sample No., X, Y, Z` (akselerometer, 1000 sampel/s), header blok: Drilling Speed 490 RPM, Feed 0.285 mm/rev, `Tool: 1 Run: 1` | **Kerusakan bertahap: 4 mata jalan baru→tumpul** — kondisi di-*implicit* lewat penamaan file `Txx_Rxx` (4 tool × 2 run), tidak ada kolom label eksplisit | **CC BY 4.0** (field `data_licence` API Mendeley) | **TERSURVEI**: `curl` file → `openpyxl` → 60.505 baris terbaca; daftar 8 file dari `public-api/.../files` 200 | **1 dari 3** — kriteria **tool/bit wear** (nyata, bukan sintetis). Domain pengeboran bengkel/mesin, bukan sumur minyak |
| 2 | **Explainable AI (XAI) Drilling Dataset** (Kaggle) | https://www.kaggle.com/datasets/raphaelwallsberger/xai-drilling-dataset [2] | CSV 1.107.906 B (**20.000 baris × 15 kolom**); zip unduhan 292.793 B | `ID, Cutting speed vc, Spindle speed n, Feed f, Feed rate vf, Power Pc, Cooling, Material, Drill Bit Type, Process Time, Main Failure, BEF, CCF, FWF, WDF` | **Multi-mode kegagalan**: `Main Failure` 0/1 = 18.999/1.001; flag satu-panas `BEF` 215, `CCF` 344, `FWF` 278, `WDF` 300 (4 jenis mode gagal) | **CC BY-NC-SA 4.0** (API Kaggle); mirror GitHub Alarconen memakai MIT — lisensi resminya milik Kaggle/paper | **TERSURVEI**: zip diunduh → dibuka → distribusi label dihitung dari CSV | **1 dari 3 (tapi 4 sub-jenis)** — kriteria **tool failure / mode kerusakan**; catatan: dataset **sintetis** (paper TransAI 2023, DOI 10.1109/TransAI60598.2023.00032) dan domain pengeboran mesin |
| 3 | **Drilling-Stuck-Pipe-Prediction** (GitHub, Gulf of Suez) | https://github.com/HaythamElmousalami/Drilling-Stuck-Pipe-Prediction [3] | `Stuck data Gitub.xlsx` 14.228 B; `Stuck data Multiclass.xlsx` 14.607 B | Sheet `Data augmanted 5` = **104×8** → **103 baris data**: `P1…P7, stuck case` | **Stuck pipe biner 77 normal / 26 stuck**; varian multiclass memberi derajat 0–1 (0.0–1.0, 10 tingkat) | **Tidak ada file LICENSE** (endpoint `/license` → 404) = secara hukum all-rights-reserved | **TERSURVEI**: kedua xlsx diunduh HTTP 200 → `openpyxl` → header + distribusi label dihitung | **1 dari 3** — kriteria **stuck pipe** dan satu-satunya kandidat ber-label **domain sumur minyak**. Kelemahan: n=103, sudah di-augment, tanpa lisensi |
| 4 | **Pillar Drill Hole Quality Dataset** (HuggingFace) | https://huggingface.co/datasets/nikhilr2907/Drilling-Dataset [4] | `metadata.csv` 8.511 B → **307 baris**; 1000 folder contoh (gambar+audio) | `metadata.csv`: `example_id, label, duration_s`; per contoh: `image.jpg`, `audio.wav`, `audio_label.npy` (per jendela 1 s), `image_label.npy` grid 16×16 | **normal 220 / abnormal 87** (klip), label per-jendela audio 0/1, label spasial 1/0/−1 | **Tidak ada lisensi di card HF** (`cardData` hanya `pretty_name`) | **TERSURVEI**: `metadata.csv` diunduh (200, 8.511 B) → baris pertama `example_0001,abnormal,14.100` terbaca | **1 dari 3** — kriteria **deteksi cacat/abnormalitas hasil pengeboran**; bengkel (aluminium), bukan sumur |
| 5 | **Synthetic Drilling Dataset** (HuggingFace) | https://huggingface.co/datasets/jonasmaltebecker/synthetic_drilling_dataset [5] | `download_size` 732.313 B, `dataset_size` 10.957.240 B; **39.133 baris** (train 27.393 / val 3.913 / test 7.827) | `torque_m_c` (sequence), `feed`, `cutting_speed`, `depth`, **`k_wear`**, `drill_no` | Target **`k_wear` = koefisien keausan** (kontinu, bukan kelas) — sampel baris pertama k_wear 1.049 / 1.229 / 1.104 | **Tidak ada lisensi** (`license: null` di API & card) | **TERSURVEI**: `datasets-server/first-rows` 200 → fitur + 3 baris data asli terbaca | **1 dari 3 (pelemah)** — kriteria **bit wear** hanya versi **sintetis** (model Kienzle), tanpa lisensi |
| 6 | Utah FORGE 16A(78)-32 Drilling Data (Kaggle) | https://www.kaggle.com/datasets/lordkun/utah-drilling-16a78-32-drilling-data [7] | zip 17.134.787 B → CSV 59.970.592 B, **503.905 baris × 14 kolom** | `Time, Weight on Bit, ROP Depth/Hour, Top Drive RPM, Top Drive Torque, Flow In, Pump Pressure, SPM Total, Pit Volume Active, Bit RPM, Depth Hole TVD, Differential Pressure, Downhole Torque, MUD TEMP` | **TIDAK ADA kolom label** | Apache 2.0 | **TERSURVEI**: zip diunduh → header + jumlah baris dihitung dari isi zip | **0 dari 3** — hanya sumber fitur (bisa jadi basis label fisika) [7] |
| 7 | promiseeee / Time-series-stuck-pipe-prediction (GitHub) | https://github.com/promiseeee/Time-series-stuck-pipe-prediction [6] | TSPP1.csv 2.722.605 B (21.121 baris), TSPP1-15s.csv 835.443 B (5.634 baris), TSPP2-4 1,0–1,5 MB | `date, Average Hookload, Hole depth (MD), Weight on Bit, Block Position, Average Rotary Speed, Average Surface Torque, Bit Depth (MD), Average Standpipe Pressure, Mud Flow In, Rate of Penetration` | **TIDAK ADA kolom label** di ketiga file yang dibuka — klaim "stuck pipe dataset" hanya di README | Tidak ada LICENSE | **TERSURVEI (negatif)**: `git/trees` → 3 file CSV diunduh → header dibaca, kolom label nihil | **0 dari 3** [6] — penting: repo ini **Volve-derived dan tak berlabel**, jangan dihitung pemenuh kriteria |
| 8 | Bit_wear / Bit_wear_data (Kaggle) | https://www.kaggle.com/datasets/atashnezhad/bit-wear [8] | xlsx 8.949 B = **10×5**; CSV 395 B = **9 baris** | `Fn (lbf), Fd (lbf), RPM, time intervals (sec), ROP (ft/hr)` | **TIDAK ADA label keausan** (hanya 9 baris data) | `Unknown` (API Kaggle) | **TERSURVEI (negatif)**: zip diunduh → xlsx & csv dibuka | **0 dari 3** [8] |
| 9 | drilling log dataset (Kaggle, Volve 15/9-F-15) | https://www.kaggle.com/datasets/ahmedelbashir99/drilling-log-dataset [9] | 6.084 B → CSV 17.751 B, **151 baris × 8 kolom** | `Depth, WOB, SURF_RPM, ROP_AVG, PHIF, VSH, SW, KLOGH` | **TIDAK ADA label** (Volve, sudah dalam lingkup internal) | `Unknown` | **TERSURVEI (negatif)** | **0 dari 3** [9] |
| 10 | MSEEL ROP_prediction well1/well2 (GitHub) | https://github.com/m-bizhani/ROP_prediction [10] | well1.csv 846.111 B = **7.999 baris × 21 kolom** | `Hole Depth, Rotary Torque, Rotary RPM, Standpipe Pressure, Weight on Bit, Hook Load, Differential Pressure, Inclination, Time Of Penetration, Total Mud Volume, Gamma at Bit, Bit Depth, Bit RPM, Line Wear, Block Height, Min/…, Rate Of Penetration` | **TIDAK ADA label kegagalan**; kolom `Line Wear` berupa nilai kontinu (keausan drilling line), bukan label kerusakan | Tidak ada LICENSE di repo | **TERSURVEI (negatif)**: CSV diunduh → header dibaca | **0 dari 3** (fitur + proxy `Line Wear` saja) [10] |
| 11 | Frontiers 2026 stuck-pipe (297 observasi, 13 variabel) | https://www.frontiersin.org/journals/built-environment/articles/10.3389/fbuil.2026.1913509/full [11] | 297 baris (dilaporkan paper) | P1… driling-related variables | Label biner pipe-sticking | — | **NEGATIF TERVERIFIKASI**: statement data availability dibaca langsung: *"not publicly available … available from the author upon reasonable request and with permission from Dolph and Dode Offshore Services India"* | **0** — tidak bisa diunduh [11] |

**Rekap pemenuhan 3 kriteria (gabungan):**

| Kriteria | Pemenuh terverifikasi | Domain |
|---|---|---|
| (1) Stuck pipe | Kandidat **#3** (biner + multiclass, 103 baris) | Sumur minyak (Gulf of Suez) |
| (2) Bit / tool wear | Kandidat **#1** (nyata, 8 file) + #5 (sintetis) | Bengkel/mesin |
| (3) Tool failure multi-mode | Kandidat **#2** (4 mode: BEF/CCF/FWF/WDF) | Bengkel/mesin (sintetis) |
| (bonus) Cacat hasil pengeboran | Kandidat **#4** (normal/abnormal + grid spasial) | Bengkel |

→ **3 kriteria terpenuhi lewat gabungan #3 + #1 + #2** (masing-masing sudah dibuka isinya). **Belum ada** dataset eksternal publik yang terverifikasi untuk kriteria **drilling dysfunctions (stick-slip/bit-bounce) ber-label** maupun **NPT/fishing ber-label** pada domain sumur minyak — lihat §3.

---

## 2. Bukti pencarian (≥5 query berbeda, ≥3 sumber berbeda)

| # | Query / endpoint | Sumber | Hasil mentah (ringkas) |
|---|---|---|---|
| Q1 | `open source drilling dataset stuck pipe failure labels machine learning` | Tavily via 9router (built-in `web_search`) | 8 hasil; kandidat Frontiers 2026, promiseeee, paper Mopuri [11][6] |
| Q2 | `drilling dysfunctions dataset bit wear NPT labeled dataset download` | Tavily via 9router | 8 hasil; Mendeley `th4yv974r2`, SPE bit-failure images, MDPI Grad-CAM [1] |
| Q3 | `open dataset offshore drilling non-productive time NPT stuck pipe labeled csv download` | Tavily via 9router | 8 hasil; hanya rpubs/RSRT — tidak ada dataset NPT publik [15] |
| Q4 | `kaggle OR zenodo OR github drilling dysfunction stick slip bounce dataset download labels` | Tavily via 9router | 8 hasil; mayoritas glossary/paper, tanpa file data [12][15] |
| Q5 | `arxiv 2503.07440 stuck pipe drilling dataset github code available` | Tavily via 9router | promiseeee + arXiv; halaman arXiv tidak mencantumkan repo data [18][6] |
| Q6 | `POST https://api.figshare.com/v2/articles/search {"search_for":"drilling failure dataset"}` | Figshare API [14] | **19 hasil 200**; hanya `Drill image dataset for training I/II` (PLOS) |
| Q7 | `POST figshare search_for=stuck pipe / drilling dysfunction / drilling tool wear` | Figshare API [14] | 9 / 6 / 15 hasil — hanya *journal_contribution*, tanpa data CSV |
| Q8 | `GET https://zenodo.org/api/records?q=drilling failure dataset` | Zenodo API [13] | 15 dari 358.330 (relevansi rendah); tak ada file data kegagalan drilling |
| Q9 | `GET https://zenodo.org/api/records?q="stuck pipe"&resource_type.type=dataset` | Zenodo API [12] | **total 9** — semuanya PDF (proceeding), nol berkas data |
| Q10 | `GET https://zenodo.org/api/records?q="drilling dysfunction"` | Zenodo API [13] | **total 0** |
| Q11 | `GET https://www.kaggle.com/api/v1/datasets/list?search=drilling` | Kaggle API [15] | 20 hasil; XAI drilling, Utah FORGE, drilling log, dll. |
| Q12 | `search=bit wear` / `drilling dysfunction` / `predictive maintenance drilling` / `stuck pipe` / `NPT drilling` / `well kick influx` / `stick slip drilling` | Kaggle API [15] | 7 / **0** / 2 / **0** / **0** / **0** / **0** hasil |
| Q13 | `GET https://huggingface.co/api/datasets?search=drilling` | HuggingFace API [16] | 12 hasil; `stuck pipe`→0, `well control`→1 (tak relevan), `wear fault`→0 |
| Q14 | `GET https://api.github.com/search/repositories?q=drilling dataset` | GitHub API [17] | **306 hasil**; 6 repo di-*trees* menyeluruh (Hadi-mac, 931808712, markdlindsay, doon-hiro, m-bizhani, Alarconen) |
| Q15 | `GET https://api.github.com/search/repositories?q="stuck pipe" prediction dataset` | GitHub API [17] | **1 hasil** = promiseeee (sudah diperiksa, tak berlabel) [6] |
| Q16 | `GET https://archive.ics.uci.edu/api/datasets?search=drilling` | UCI ML Repo | **HTML shell, bukan JSON** (endpoint API tidak tersedia seperti itu) → tidak bisa dipakai sebagai bukti |
| Q17 | `POST data.mendeley.com/public-search` + `GET public-api/datasets?query=` | Mendeley Data | **404** `Cannot POST /public-search`, `Cannot GET /public-api/datasets` — sesuai catatan skill: pencarian Mendeley mati (perlu OAuth); *retrieval by DOI/ID tetap jalan* (Q18) |
| Q18 | `GET https://data.mendeley.com/public-api/datasets/th4yv974r2?version=1` + `/files?folder_id=root&version=1` | Mendeley Data [1] | **200** → metadata + 8 file dengan `download_url` (ini jalur verifikasi kandidat #1) |

Jumlah: **18 query/endpoint berbeda** di **7 sumber berbeda** (Tavily-9router, Figshare, Zenodo, Kaggle, HuggingFace, GitHub, Mendeley) + 2 sumber tambahan yang dicek dan negatif (UCI, arXiv) → syarat ≥5 query & ≥3 sumber terpenuhi jauh sebelum kesimpulan apa pun.

---

## 3. Hasil negatif yang diverifikasi (bukan "tidak ditemukan" tanpa bukti)

1. **Dataset NPT/fishing ber-label tidak ada yang publik.** [15][17] Query Q3 (web), Q12 (Kaggle `NPT drilling` = 0 hasil), Q12 (`well kick influx` = 0 hasil), Q8/Q9 (Zenodo) semuanya kembali tanpa file data. Kandidat terdekat — repo kick Aramco `Hadi-mac/Oil-Well-Drilling-influx-kick-prediction` — *trees* menyeluruh menunjukkan hanya `README.md`, 2 notebook, 2 docx: **tidak ada berkas data sama sekali** (data Aramco tertanam/proprietary).
2. **Drilling dysfunctions (stick-slip, bit-bounce) ber-label tidak ditemukan** [12][15][16] pada Zenodo (total 0 untuk `"drilling dysfunction"`), Kaggle (`stick slip drilling` = 0), HF (`search=drilling` 12 hasil, tak ada label fungsi), GitHub (Q14 — 6 repo diperiksa, tanpa label dysfunctions).
3. **Dataset stuck-pipe Frontiers 2026 (297 observasi) tidak publik** [11] — dibaca langsung dari statement paper: "not publicly available … upon reasonable request … Dolph and Dode Offshore Services India".
4. **Mendeley search API mati** [1] (404 pada `public-search` dan `public-api/datasets`) — tetap bisa *retrieval by ID*, itulah jalur yang dipakai untuk kandidat #1.
5. **UCI ML repo** tidak menjawab API `?search=` seperti JSON (mengembalikan shell HTML) → tidak dihitung sebagai sumber yang berhasil.
6. **Repo `promiseeee` yang selama ini dianggap "dataset stuck pipe" ternyata tidak berlabel** [6] — ketiga CSV dibuka, header hanya berisi 11 kolom sensor. Ini temuan yang mengoreksi asumsi sebelumnya (lihat §5).

---

## 4. Rekomendasi untuk V6 (lanjutan)

- **Pakai gabungan #3 (stuck pipe) [3] + #1 (tool wear) [1] + #2 (4 mode failure) [2]** untuk memenuhi syarat 3 kriteria; semuanya sudah terbukti bisa diunduh dan dibuka dari WSL.
- Untuk label **domain sumur minyak** yang lebih kuat dari n=103: tetap pakai rute Volve DDR (sudah terverifikasi di skill `drilling-datasets-oilfield`), karena pencarian eksternal Q1–Q18 tidak menemukan alternatif ber-label yang bisa diunduh.
- Kriteria **dysfunctions** dan **NPT/fishing** terbuka: tidak ada sumber publik terverifikasi → jika tetap dibutuhkan, opsi yang tersisa adalah label fisika (MSE / d-exponent / ROC_coef pada data tanpa label, sudah ada resepnya) atau penelusuran manual ke lampiran paper SPE/DUPTS.

---

## 5. Catatan verifikasi (jujur atas keterbatasan)

- Semua angka baris/kolom/distribusi di §1 berasal dari pembukaan berkas nyata di sesi ini (path kerja: `/home/neonti/.hermes/cache/scratch/v6d2/`), bukan dari README.
- **Belum dicek**: (a) integritas sha256 file Mendeley dibandingkan `content_details.sha256_hash` API (hanya ukuran + keberhasilan parsing yang dicek); (b) apakah label `stuck case` #3 berasal dari data nyata atau sudah di-augment (nama sheet `Data augmanted 5` menandakan augmentasi); (c) kolom `P1…P7` #3 tidak didefinisikan di README (perlu paper aslinya); (d) file `TSPP2/3/4` tidak dibuka satu per satu (TSPP1 dan TSPP1-15s dibuka); (e) UCI ML repo dan OSF tidak terjangkau lewat API (HTML shell / URL `[]` ditolak curl), jadi tidak dihitung sumber yang sukses.
- Dataset yang **sudah ditolak di skill** (3W, bearing test-rig, Saadeldin) tidak diusulkan ulang.

## Sources

[1] https://data.mendeley.com/datasets/th4yv974r2 — Mendeley Data: Drilling tool wear dataset (DOI 10.17632/th4yv974r2.1)
[2] https://www.kaggle.com/datasets/raphaelwallsberger/xai-drilling-dataset — Kaggle: Explainable AI (XAI) Drilling Dataset
[3] https://github.com/HaythamElmousalami/Drilling-Stuck-Pipe-Prediction — GitHub: Drilling-Stuck-Pipe-Prediction (Gulf of Suez stuck case xlsx)
[4] https://huggingface.co/datasets/nikhilr2907/Drilling-Dataset — HuggingFace: Pillar Drill Hole Quality Dataset
[5] https://huggingface.co/datasets/jonasmaltebecker/synthetic_drilling_dataset — HuggingFace: Synthetic Drilling Dataset (k_wear)
[6] https://github.com/promiseeee/Time-series-stuck-pipe-prediction — GitHub: Time-series-stuck-pipe-prediction (Volve TSPP)
[7] https://www.kaggle.com/datasets/lordkun/utah-drilling-16a78-32-drilling-data — Kaggle: Utah FORGE 16A(78)-32 Drilling Data
[8] https://www.kaggle.com/datasets/atashnezhad/bit-wear — Kaggle: Bit_wear (PDC)
[9] https://www.kaggle.com/datasets/ahmedelbashir99/drilling-log-dataset — Kaggle: drilling log dataset (Volve 15/9-F-15)
[10] https://github.com/m-bizhani/ROP_prediction — GitHub: MSEEL ROP_prediction well1/well2 CSV
[11] https://www.frontiersin.org/journals/built-environment/articles/10.3389/fbuil.2026.1913509/full — Frontiers 2026: stuck-pipe ML framework (297 obs, data NOT public)
[12] https://zenodo.org/api/records?q=%22stuck%20pipe%22&resource_type.type=dataset&size=15 — Zenodo API search: stuck pipe, type=dataset
[13] https://zenodo.org/api/records?q=drilling%20failure%20dataset&size=15 — Zenodo API search: drilling failure dataset
[14] https://api.figshare.com/v2/articles/search — Figshare API POST search (drilling failure / stuck pipe / drilling tool wear)
[15] https://www.kaggle.com/api/v1/datasets/list — Kaggle dataset list API (multiple queries)
[16] https://huggingface.co/api/datasets?search=drilling — HuggingFace datasets API search=drilling
[17] https://api.github.com/search/repositories?q=drilling+dataset — GitHub repository search API q=drilling dataset
[18] https://arxiv.org/abs/2503.07440 — arXiv 2503.07440: Early signs of stuck pipe detection based on Crossformer
