# V9-D1 — Pipeline Data, Fitur Jendela, Anti-Bocor untuk 7 Engine PdM

> Dokumen ini ditulis SEGERA dari hasil 5 skrip yang sudah berjalan (anti-crash protocol); bagian §8/§9 di-patch final 2026-10-12 setelah merge stuck_k2 selesai. Kerangka evaluasi: docs/V9_PM1_ARCHITECTURE.md (5 lapis, standar A/B/C). Peta data: docs/V6_D0_READERS_SYNTHESIS.md + V6_D1a..h.

## Riset pendahuluan: skill — poin

Riset pendahuluan: scientific-critical-thinking — memisahkan OBSERVED (angka artefak) / DERIVED (invariant anti-bocor) / HYPOTHESIS (kelayakan statistik) sebelum klaim; tiap engine dinilai di tingkat alat PdM, bukan LULUS/GAGAL.
Riset pendahuluan: verification-mandatory — semua angka di bawah baca langsung dari artefak JSON di `scratch/v9_d1/` (bukan ingatan); invariant `feat_ts_max < lab_ts` dihitung nyata, bukan diasumsikan.
Riset pendahuluan: statistical-analysis — prevalensi per well per kelas dilaporkan + flag `underpowered` (positif < threshold) supaya validasi LOWO tidak menuntut fold yang secara statistik tidak berdaya.

Catatan PM2 (V9-PM2, 2026-10-12): baris riset `what-if-oracle` / `consciousness-council` / `sequentialthinking` TIDAK dicatat pada dokumen ini (pelanggaran PM1 §4.0.5, tercatat di `V9_PM2_VERDICT.md` §a) — TIDAK ditambahkan retroaktif karena akan mengklaim kegiatan yang tidak terbukti; angka D1 (n_rows, invariant anti-bocor 0/118.567 stuck_k2, prev per well) tetap diverifikasi independen oleh auditor A1 §6.3.

## 0. Ringkasan eksekutif

Pipeline bins → jendela rig → fitur jendela ketat-lalu → matriks fitur per engine, anti-bocor terverifikasi (0 pelanggaran), siap-latih per engine + split Leave-One-Well-Out (LOWO) per sumur. Determinisme seed 42.

## 1. Pipeline (5 skrip, semua berjalan di disk nyata)

| Skrip | Fungsi | Artefak |
|---|---|---|
| `v9_d1_01_bins.py` | Baca WITSML parsed → grid bins 60 detik ALL-rows, 9 well | `scratch/v9_d1/v9_d1_01_summary.json` |
| `v9_d1_01b_crosscheck_v6.py` | Samakan bins V9 vs resep V6_E1_10 (identik) | `v9_d1_01_crosscheck_v6.json` (identical=true, 7 well) |
| `v9_d1_02_rig_windows.py` | Jendela rig per anchor + label status (vib/shk/stuck) + SSI dari CRPM | `v9_d1_02_summary.json` |
| `v9_d1_03_rig_datasets.py` | Matriks fitur per engine + hyd_ki (anti-sirkular) | `v9_d1_03_qc.json` |
| `v9_d1_04_stuck_k2.py` | Dataset onset stuck-pipe (H=10 menit), resep V8 E_stuck; read chunked 250rb (F-14 single-shot ENOMEM) | `datasets/stuck_k2.csv.gz` + `v9_d1_04_qc.json` |

Bins resep = verbatim V6_E1_10 (chunksize 250000), seed 42. Crosscheck V6: 7/7 well `ts_index_identical=true`, `col_diffs={}` (kolom hilang hanya turunan V6 `stkslp_*`).

## 2. Matriks fitur & jendela ketat-lalu (anti-bocor)

- Grid 60 detik (bin menit) ALL-rows.
- Fitur = statistik jendela KETAT-LALU `[t0-10, t0)` per kanal: `mean, std (ddof=1), slope OLS per menit, last, frac` — total 55 fitur (11 kanal × 5) / 40 fitur (hyd_ki, 8 kanal × 5).
- Stempel waktu kolom (setiap dataset):
  - `well` — identitas sumur (untuk LOWO)
  - `ts_bin` — menit anchor
  - `feat_ts_max` — menit data terakhir yang masuk jendela fitur
  - `lab_ts` — menit peristiwa / label
  - `lab_kind` — jenis baris (onset_event / onset_horizon_neg / status)

**Invariant anti-bocor:** `feat_ts_max < lab_ts` untuk semua baris → fitur selalu dari masa lalu relatif label. Imputasi/normalisasi dilakukan fold-safe (hanya dari data latih di tiap fold LOWO).

## 3. Skema label per engine + anti-sirkularitas

| Engine | Label | Sumber | Anti-sirkular (fitur dilarang) |
|---|---|---|---|
| vib | `VIBLAT_RT >= 32.17405` | kanal MWD instrumen | VIBLAT tidak di CHAN fitur |
| shk | `SHKRSK_RT >= 1` | kanal MWD instrumen | SHKRSK tidak di CHAN fitur |
| ssi | SSI = (max−min)/(2·mean) dari CRPM ≥ 1, ≥10 sampel | turunan fisika (CRPM) | CRPM tidak di CHAN fitur |
| stuck_k1 | `STUCK_RT >= 1` (status) | kanal MWD | STUCK tidak di CHAN fitur |
| stuck_k2 | onset edge 0→1 STUCK ffill, horizon H=10 menit | label kurasi V8 E_stuck | STUCK tidak di CHAN fitur |
| hyd_ki | hydraulic imbalance (turunan fisika) | 8 kanal (SPPA/TFLO/SPM Dibuang) | SPPA/TFLO/SPM dikecualikan dari fitur |
| tool_wear | modul terpisah (PM1 D-A7) — TIDAK punya dataset window di D1 | lihat V8_E_tool_wear / kartu engine terkait | — |

CHAN fitur = `[TQA, SPPA, TFLO, RPM, SWOB, HKLD, ROP, BPOS, SPM, depth, dbtm]` — tidak mengandung VIBLAT/SHKRSK/STUCK/CRPM. hyd_ki memakai 8 kanal (tanpa SPPA/TFLO/SPM).

## 4. Matriks fitur per engine (dari `v9_d1_03_qc.json`)

| Engine | Rows | Features | Positives | Wells |
|---|---|---|---|---|
| vib | 23 922 | 55 | 5 429 | F-14, F-15A, F-15_S, F-5 |
| ssi | 35 906 | 55 | 607 | 9 well |
| shk | 56 495 | 55 | 2 005 | 9 well |
| stuck_k1 | 5 555 | 55 | 2 007 | F-14, F-9_A |
| hyd_ki | 52 509 | 40 | 7 172 | 9 well |
| stuck_k2 | 118 567 | 55 | 1 975 | F-9, F-9_A, F-10, F-14 |

Per-well `eligible`, `positives`, `prev` + flag `underpowered` ada di `v9_d1_03_qc.json` (mis. ssi F-7 underpowered, F-9 underpowered). `leak_violation_in_builder=0` di builder semua well.

## 5. Split Leave-One-Well-Out (LOWO)

Fungsi split menghasilkan fold `(train_wells, test_well)` — satu fold per sumur yang punya data engine itu. Contoh (vib, 4 well) → 4 fold. Fold JSON per engine disimpan di `scratch/v9_d1/lowo_<engine>.json`. Underpowered wells tetap dilaporkan agar validasi A/B/C tidak menuntut metrik stabil di fold tanpa daya statistik.

## 6. Determinisme

Seed 42 di semua skrip. Bins identik dengan resep V6 (crosscheck identical=true). Fitur & label reproducible dari bins + resep ketat.

## 7. Penerimaan (acceptance)

(a) Pipeline jalan + matriks fitur terbentuk — VERIFIED (5 dataset nyata di `datasets/`).
(b) Anti-bocor = 0 pelanggaran — dihitung dari kolom `feat_ts_max < lab_ts` (tabel di bawah; semua 0).
(c) Skema label 7 engine + anti-sirkularitas — tabel §3.
(d) Split LOWO siap — fungsi + fold JSON per engine.

## 8. Hasil verifikasi anti-bocor (feat_ts_max >= lab_ts harus 0)

Dihitung ulang dari file merged di `datasets/` oleh `v9_d1_05_leak_lowo.py` (bukan klaim builder):

| Dataset | Rows | Pelanggaran `feat_ts_max >= lab_ts` | Baris `feat_ts_max` NaN | LOWO folds |
|---|---|---|---|---|
| vib | 23 922 | **0** | 0 | 4 |
| ssi | 35 906 | **0** | 0 | 9 |
| shk | 56 495 | **0** | 0 | 9 |
| stuck_k1 | 5 555 | **0** | 0 | 2 |
| hyd_ki | 52 509 | **0** | 0 | 9 |
| stuck_k2 | 118 567 | **0** | 0 | 4 |

Total: 6/6 dataset, 0 pelanggaran. Fold JSON: `scratch/v9_d1/lowo_<engine>.json`.

## 9. stuck_k2 (onset prediction)

Merge final (4 well, `v9_d1_04_qc.json`): 118 567 baris, 55 fitur, 1 975 positif, seed 42, H=10 menit.

| Well | Eligible | Positif | Onsets ffill / strict | Scorable | Cocok invarian V8 |
|---|---|---|---|---|---|
| F-9 | 16 184 | 311 | 55 / 61 | 55 | (tanpa REF V8) |
| F-9_A | 2 242 | 503 | 72 / 72 | 72 | ✓ (72) |
| F-10 | 4 216 | 772 | 93 / 111 | 93 | ✓ (93) |
| F-14 | 95 925 | 389 | 61 / 81 | 61 | ✓ (61) |

Invarian V8 terpenuhi 3/3 well yang punya REF. F-9 tanpa REF V8 (55 onset tervalidasi internal: 0 onset terlewat karena alasan skorabilitas). Deviasi terdokumentasi: pembacaan CSV F-14 (813 MB) dilakukan chunked 250 rb baris karena read_csv single-shot gagal `OSError Errno 12` (ENOMEM di parser C) — angka akhir identik resep.

## 10. Limitasi & yang belum diverifikasi

- F-9 stuck_k2 tidak punya invarian eksternal V8 (onset 55 = hasil resep, bukan silang-verifikasi) — kekuatan bukti lebih rendah dari 3 well lain.
- Metrik deteksi (precision/recall/waktu deteksi) = domain kartu E_*/EVAL_*; di sini hanya kesiapan data + fitur + label + anti-bocor.
- Istilah operator "1mlnzs (opn/thk/chk/cls)" tidak terdefinisi di mana pun yang dapat diakses (pencarian penuh docs/ termasuk Evaluasi User.txt, 7 kanban.db, header WITSML 9 well, agentmemory = 0 rujukan) — menunggu kejelasan operator; tidak masuk artefak D1.
