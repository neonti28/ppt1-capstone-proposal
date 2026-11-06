# V10-A1: AUDIT PROPOSAL, ANGKA VS SUMBER, PENUTUPAN KELUHAN (a)-(f), REGISTRY, KEJUJURAN PENYAJIAN

Task: `t_8434e4f3` [Auditor] · Board: `capstone-v10-proposal` · Tanggal: 2026-10-15 (WIB)
Sumbu audit: `docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md` (hasil perakitan `t_0720bde5`) + `.ipynb` (221 cell),
seluruh `docs/V10_*.md`, sumber primer (`docs/V9_EVAL_*`, `docs/V9_E_*`, JSON `scratch/v9_*`, kode `code/`, file data di `data/`).
Metode: eksekusi modul REGISTRY, hitung ulang file data (wc -l, modul csv), baca JSON primer, dan bandingkan baris per baris.

> Riset pendahuluan: `verification-mandatory` (setiap klaim dicek dengan tool sebelum ditulis) ·
> `sequentialthinking` (4 pikiran, sequ-mcp: hipotesis → bukti → rencana patch → putusan) ·
> `statistical-analysis` (satuan angka diperiksa per kampanye V6/V8/V9, bukan dirata-ratakan).

---

## 0. RINGKAS AUDIT (satu paragraf)

Seluruh **28 angka kunci** yang ditelusuri **cocok dengan sumber primer**; modul REGISTRY **dijalankan** dan
membuktikan **7 engine · 11 klaim · 27 head** beserta rekap tier 12/13/2 dan lapisan 5/11/9/2 persis seperti
tabel Bab 1 proposal. Keluhan operator **(a) sampai (f) semuanya TERTUTUP** dengan seksi yang dapat ditunjuk.
Pemeriksaan kejujuran lolos: **0 "lulus bersyarat"**, **0 isi post-mortem** (satu kemunculan kata dalam kalimat
negasi), **0 vonis biner pada tingkat alat**, **0 em-dash** di `.md` maupun `.ipynb`. Audit menemukan **3 temuan
penyajian** (dua di antaranya inkonsistensi internal, satu angka basi yang diwarisi dari dokumen era V3/V6);
ketiganya **sudah dipatch** langsung ke proposal, `.ipynb`, dan dua dokumen sumber bab. Tidak ada angka hasil
evaluasi yang diubah; semua patch bersifat klarifikasi/penyelarasan penyajian.

---

## 1. METODE DAN BUKTI EKSEKUSI

| Langkah | Alat | Bukti keluaran |
|---|---|---|
| Jalankan REGISTRY | `importlib` atas `code/v9_i1_pipeline.py` (skrip `v10_a1_registry_check.py`) | 7 engine, 27 head (4+4+4+6+4+2+3), tier 12/13/2, layer 5/11/9/2, `AUTO_CRITICAL_SLOTS = 0` |
| Hitung ulang data primer | `wc -l` + modul `csv` (lebih akurat daripada pemecah koma naive) | USROP 198.928 brs/18 kol; time.csv F-9A 419.747 brs/239 kol; 10 CSV WITSML 9.935.698 brs |
| Hitung ulang dataset latih | `gzip` + hitung baris `scratch/v9_d1/datasets/*.csv.gz` | 292.954 baris (6 file, cocok §3.7 proposal) |
| Hitung fold | daftar `folds` pada JSON `lowo_*.json` dan `v9_e_ml/*_RESULTS.json` | 37 fold D1 (4+9+9+2+9+4); 26 fold ML (vib 4 + ssi 9 + shk 9 + stuck_k2 4) |
| Cocokkan angka kampanye | `grep` terarah ke `V9_EVAL_A/B/C`, `V9_E_STAT`, `V8_M1`, `V8_E_*` | lihat tabel §2 |

---

## 2. TELUSURI ANGKA KUNCI (28 angka, semuanya ditelusuri ke sumber primer)

| # | Angka di proposal | Posisi proposal | Sumber primer | Hasil |
|---|---|---|---|---|
| 1 | 7 engine | Bab 1 §1.1 (baris 195) | eksekusi REGISTRY `v9_i1_pipeline.py` | **COCOK** (7 kunci: vib, ssi, shk, stuck, hyd, bit_wear, tool_wear) |
| 2 | 11 klaim (3×1 + 4×2) | Bab 1 §1.2 | REGISTRY `klaim_tugas` + penanda `klaim` per head | **COCOK** (3 engine satu klaim + 4 engine dua klaim) |
| 3 | 27 head (4+4+4+6+4+2+3) | Bab 1 §1.3 (baris 226) | eksekusi REGISTRY | **COCOK** |
| 4 | Rekap tier 12 / 13 / 2 | Bab 1 §1.3 | eksekusi REGISTRY | **COCOK** |
| 5 | Rekap lapisan L0 5 · L1 11 · L2 9 · L3 2 | Bab 1 §1.3 | eksekusi REGISTRY | **COCOK** |
| 6 | `AUTO_CRITICAL_SLOTS = 0` | Bab 1 §0 | eksekusi REGISTRY | **COCOK** |
| 7 | VIBLAT ambang 32,17405 ft/s² | Bab 1 §1.1, Bab 7 §0.1 | REGISTRY `klaim_tugas` vib | **COCOK** |
| 8 | stuck onset H = 10 menit | Bab 1 §1.1, Bab 7 | REGISTRY `klaim_tugas` stuck | **COCOK** |
| 9 | hyd K-i `\|z\| > 2` residu SPPA | Bab 1 §1.2 | REGISTRY `klaim_tugas` hyd | **COCOK** |
| 10 | USROP_labeled 198.928 baris / 18 kolom | Bab 3 §3.1, §3.2.2 | `wc -l` + header `data/USROP_labeled.csv` (198.929 baris − header) | **COCOK** |
| 11 | labels_curated_v2 884 kejadian; bha_relevant 571/263/50 | Bab 3 §3.2.3 | `data/volve/labels_curated_v2_log.json` (`input_rows` 884, `output_rows` 884, counts 571/263/50) | **COCOK** (file mentah 1.413 baris sudah direkonsiliasi eksplisit di bab) |
| 12 | time.csv F-9A 419.747 baris / 239 kolom | Bab 3 §3.2.10, §3.7 | `wc -l` (419.748 − header) + modul `csv` (239 kolom; pemecah koma naive keliru 247 karena ada koma di dalam kutip) | **COCOK** |
| 13 | 6 dataset latih 292.954 baris (23.922+35.906+56.495+5.555+52.509+118.567) | Bab 3 §3.7 | hitung ulang `scratch/v9_d1/datasets/*.csv.gz` | **COCOK persis per file** |
| 14 | 37 fold LOWO (4+9+9+2+9+4) | Bab 3 §3.7 | `scratch/v9_d1/lowo_*.json` (`folds` list per engine) | **COCOK** |
| 15 | n_features 55 (11 kanal × 5 stat), seed 42 | Bab 4 §2, §3 | `scratch/v9_e_ml/*_RESULTS.json` (`n_features` 55 di 4 JSON, `feature_cols` 55, `seed` 42) | **COCOK** |
| 16 | 26 fold kampanye ML | Bab 4 §4 | jumlah `folds`: vib 4 + ssi 9 + shk 9 + stuck_k2 4 | **COCOK** |
| 17 | tool_wear 469 jendela / 27 fitur | Bab 3 §3.1, Bab 2 §2 | `wc -l scratch/v6_e1/toolwear_windows.csv` (470 − header) | **COCOK** |
| 18 | TSPP 52.905 baris (4 CSV) | Bab 3 §3.1 | `cat` + `wc -l` 4 file `data/bo_tspp/TSPP{1..4}.csv` (52.909 − 4 header) | **COCOK** |
| 19 | XML: tubular 192, bhaRun 161, trajectory 63, wbGeometry 27, mudLog 8 | Bab 3 §3.1 | `find ... -name '*.xml' \| wc -l` atas `data/volve/witsml_raw/` | **COCOK semua** |
| 20 | tubular 1.392 komponen; trajectory 5.561 stasiun; mudLog 2.882 interval; DLIS 21 CSV/309.644 baris | Bab 3 §3.1 | `docs/V6_D1a_TUBULAR.md`, `V6_D1c_TRAJ_GEOM.md`, `V6_D1d_MUDLOG.md`, `V6_D1f_PETRO.md` | **COCOK** |
| 21 | WITSML 7.080.457 baris / 8 CSV parser V3; folder kini 10 CSV / 9.935.698 | Bab 3 §3.1, §3.2.1 (baris 926, 949) | `wc -l` per file; 8 CSV parser V3 = 7.080.457 **COCOK**; 10 CSV folder = 9.935.698; pipeline V9 = 9 CSV (`FILES` `code/v9_d1_01_bins.py`, daftar sumur `v9_d1_01_summary.json`) | **COCOK setelah patch (temuan T2)** |
| 22 | hyd K-i hybrid FAR 14,6–58,4; FP 2091→927 (−55,7%) 9/9 | Bab 2 §3.1, Bab 7 §1 | `docs/V9_EVAL_C_LAYERC.md` §2.5, C1 | **COCOK** |
| 23 | ssi hybrid FP 26→7 (−73,1%) | Bab 2, Bab 6 §1, Bab 7 §1 | `docs/V9_EVAL_C_LAYERC.md` baris 91/133 | **COCOK** (lihat catatan C-1 §7) |
| 24 | stuck E3 RF 0,326–0,331 < canary 0,410 | Bab 2 §3.2 | `docs/V9_PM1_ARCHITECTURE.md` baris 218 | **COCOK** |
| 25 | tool_wear K-i: cp 8/8, precision 0,50; FAR-terkalibrasi FP 1–3; TLead 20–36 dtk; artefak termal 0/8 | Bab 2 §2, Bab 5 §5.3, Bab 7 §1 | `docs/V9_E_STAT_ENGINE.md`, `V9_EVAL_C_LAYERC.md` §2.7 | **COCOK** |
| 26 | hyd K-ii q95 P=R=0 (0 TP, FP 177); sign-flip 78,7% (6.377/8.107); CI fisher memuat prev | Bab 5 §5.4, Bab 7 §1 | `docs/V9_EVAL_C_LAYERC.md` baris 96/186 | **COCOK** |
| 27 | canary 3-RMS AUPRC 0,516–0,612 (1,19×); vib AUPRC 0,441–0,912; stuck TLead persistence-EVENT 4,5–8,5 (med 7,0) | Bab 2 §2, Bab 7 §1 | `docs/V8_E_tool_wear_CAPABILITY.md`; `V9_EVAL_A_LAYERA.md` baris 54/74; `V9_EVAL_B_LAYERB.md` baris 101/190 | **COCOK** |
| 28 | Hitungan alat V8: 0 alarm · 3 peringatan · 2 bersyarat · 2 tren (0+3+2+2=7) | Bab 8 §7 (baris 3369) | `docs/V8_M1_CAPABILITY_MAP.md` §d (baris 167-174) | **COCOK** |

---

## 3. PENUTUPAN KELUHAN OPERATOR (a)-(f)

| Keluhan | Status | Bukti seksi di proposal |
|---|---|---|
| (a) daftar 7 hal yang dideteksi | **TERTUTUP** | Bab 1 §1.1 (tabel 7 engine + kanal kunci) · Bab 7 §0.1 · Bab 8 §1 |
| (b) engine mana yang bekerja & cara kerjanya | **TERTUTUP** | Bab 7 §0.2 (lima keluarga metode) · Bab 7 §1 (tabel besar 11 klaim: metode, angka kunci, tier, batas) · Bab 7 §2 (arti tiap tier) · Bab 7 §3 (prototipe I1) · Bab 8 §2 |
| (c) alasan KENAPA tiap engine dipilih (bukti, bukan selera) | **TERTUTUP** | Bab 2 §2 (fisika kegagalan → sensor → metode per engine) · Bab 2 §3 (bukti empiris; metode yang ditolak berbukti, mis. RF dilarang di hyd K-i) · Bab 2 §4 (sitasi per rumus dari 27 sumber R1) · Bab 2 §6 (what-if-oracle) |
| (d) peran DATA | **TERTUTUP** | Bab 3 §3.1 (inventaris 13 dataset) · §3.2 (isi + peran + keterbatasan tiap dataset) · §3.3 (alur konversi) · §3.5 (kanal terlarang anti-sirkularitas) |
| (e) labeling ML / statistik / workflow hybrid | **TERTUTUP** | Bab 4 §1 (labeling per kelas, konstruksi onset, anti-sirkular) · Bab 4 §2-§3 (fitur 55 + LOWO + kontrak RF) · Bab 5 §5.1-§5.4 (rumus persis per head statistik + tes pembeda) · Bab 6 §1-§5 (rule, persistence, hibrida dua langkah, baseline fold identik) |
| (f) penjelasan TEGAS 7 vs 11 vs 27 | **TERTUTUP** | Bab 1 §0 (satu paragraf) · Bab 1 §1-§1.4 (7 ⊂ 11 ⊂ 27, daftar nama eksak, rekap tier) · ringkas ulang di Bab 4 §5, Bab 6 §6, Bab 7 §0.3, Bab 8 §6 |

---

## 4. 11 KLAIM DAN 27 HEAD VS REGISTRY KODE

Dieksekusi, bukan ditranskrip. Hasil modul `v9_i1_pipeline.py`:

- **7 engine**: `vib, ssi, shk, stuck, hyd, bit_wear, tool_wear`. Nama di tabel Bab 1 §1.1 **persis** kunci REGISTRY.
- **27 head**: seluruh 27 nama head di Bab 1 §1.3 **persis** kunci REGISTRY (`rule_display`, `persistence`,
  `hybrid_rule_and_persistence`, `rf_lowo`, `e1_2of3`, `persistence_event`, `k2_tidak_tersedia`,
  `k2_onset_belum`, `calib_5of27`, `op_far_calibrated`, `canary_3rms`), termasuk penempatan klaim per head.
- **Tier/lapisan per head**: 27 baris tabel §1.3 **semuanya cocok** dengan field `tier`/`layer` REGISTRY.
- **11 klaim**: 3 engine satu klaim (vib, ssi, shk) + 4 engine dua klaim (stuck, hyd, bit_wear, tool_wear) = 11.
  Status kejujuran klaim 7 (hyd K-ii TIDAK TERSEDIA) dan klaim 9 (bit_wear K-2 BELUM) dipertahankan di proposal,
  sesuai aturan "kejujuran ≠ penghapusan".
- **Tabel 11 klaim Bab 7 §1**: nama engine/klaim, metode, dan tier **konsisten** dengan REGISTRY; angka kunci
  per baris **cocok** dengan dokumen EVAL (bukti di tabel §2 butir 22-27).

---

## 5. CEK KEJUJURAN PENYAJIAN

| Pemeriksaan | Target | Hasil |
|---|---|---|
| 0 "lulus bersyarat" | `.md` + `.ipynb` | **0 / 0** (grep -ci) |
| 0 isi post-mortem | `.md` | **lolos**: 1 kemunculan kata "post-mortem" di baris 15, yaitu kalimat negasi ("proposal terbaca sebagai rencana solusi, bukan post-mortem"). Tidak ada riwayat kegagalan kampanye di badan proposal. |
| 0 vonis biner | `.md` | **lolos pada tingkat alat**: tidak ada klaim/engine yang divonis LULUS/GAGAL; seluruh penutupan memakai tier (ALARM-OTOMATIS / PERINGATAN-BERPENGAWAS / TREN / BELUM LAYAK PAKAI) + "memenuhi untuk X / belum untuk Y / belum terukur" (Bab 7 §1.1, Bab 8 §9). Sisa kata "gagal" semuanya berstatus bukti uji faktual berbasis angka (mis. "spesifisitas cp gagal (0,50)" Bab 2 §2, "G2 gagal" Bab 2 §3.2) atau negasi eksplisit ("bukan lulus/gagal"). |
| 0 em-dash | `.md` + `.ipynb` | **0 / 0** (grep -c). Dokumen bab V10 masih memuat 38-74 em-dash per file (artefak draft antara); deliverable sudah bersih. |

---

## 6. TEMUAN DAN PERBAIKAN (semua patch sudah diterapkan)

| ID | Temuan | Bukti | Perbaikan |
|---|---|---|---|
| **T1** | Angka **"12 kolom pit"** basi di Bab 7 §0.1 (baris 2925) dan Bab 8 §5 (baris 3326), padahal Bab 3 §3.7 dan Bab 5 (CC-4) sudah memperbaikinya menjadi **13 kolom pit** (hitung ulang header time.csv F-9A: kolom pit bernomor 1-10, 12, 13, 14; #11 absen; #3/#13 tertulis tanpa spasi). | grep "12 kolom pit" sebelum patch: 4 lokasi (2 di antaranya diskusi koreksi, wajar dipertahankan) | Diubah ke 13 di proposal (2 lokasi) + dokumen sumber `V10_EVAL_BAB.md` baris 59 dan `V10_M1_PETA_V8.md` baris 173 agar tidak mengulang |
| **T2** | Inventaris WITSML Bab 3 menyebut **"8 CSV / 7.080.457 baris"** untuk `data/volve/witsml_parsed/`. Angka itu **benar untuk 8 CSV parser V3** (dibuktikan ulang dengan wc -l), namun folder kini berisi **10 CSV / 9.935.698 baris** (F-10 773.674 dan F-12 2.081.567 ditambahkan 2026-10-11, tanpa entri di `_parse_summary.json`), dan **pipeline V9 memakai 9 CSV** (`FILES` `v9_d1_01_bins.py`; daftar sumur `v9_d1_01_summary.json` memuat F-10 dan F-12). Bab 1 (baris 293) justru menyebut "9 wellbore", sehingga terjadi inkonsistensi internal. Klaim §3.7 "seluruh angka dihitung ulang dari disk" atas inventaris ini ternyata hanya mencakup 8 CSV. | wc -l 10 file; `v9_d1_01_bins.py` baris 27-28; `v9_d1_01_summary.json` `wells`; mtime F-10/F-12 = 2026-10-11 | §3.1 baris 926, heading §3.2.1 baris 949, paragraf Isi, diagram baris 1272, §3.7 baris 1401, dan traceability §3.9 baris 1431 ditulis ulang dengan tiga jenjang: folder 10 CSV/9.935.698; pipeline V9 9 CSV; parser V3 8 CSV/7.080.457 (angka lama dipertahankan, tidak ada angka yang dihapus) |
| **T3** | Bab 2 §3.1 bertajuk "BUKTI EMPIRIS V9" memakai rentang **AUPRC 0,679-0,984** untuk persistence bit_wear K-1. Rentang itu milik kampanye **V8** (`V8_E_bit_wear_CAPABILITY.md`); kampanye **V9** = **0,119-0,984** (mean 0,670; 5/7 fold scorable, `V9_EVAL_A_LAYERA.md` baris 61; konsisten pula dengan Bab 7 §1 baris bit_wear). | grep silang V8 vs EVAL_A vs JSON `v9_e_RULE_03` (nilai fold 0,1185 dan 0,0177 ada di JSON V9) | Sel Bab 2 §3.1 diubah menjadi "0,119-0,984 (V9, 5/7 fold scorable; angka V8: 0,679-0,984)" |

Sinkronisasi `.ipynb`: 10 replacement yang sama diterapkan ke 10 cell markdown; **221 cell tetap**, **12 code cell
byte-identical**, jumlah kemunculan frasa hasil patch di `.ipynb` identik dengan `.md`. Cadangan pre-audit ipynb
disimpan di `~/.hermes/cache/scratch/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.ipynb.pre_audit`.

---

## 7. CATATAN SISA (dilaporkan, tidak dipatch)

| ID | Catatan | Alasan tidak dipatch |
|---|---|---|
| C-1 | Denominasi "7/7" untuk pemangkasan FP ssi di beberapa tempat (REGISTRY, Bab 7) berdampingan dengan rumusan EVAL_C "memotong di 6/9 fold, tie 3/9, 0 lebih buruk (7/7 fold layak ≤ rule)". Angka −73,1% dan 26→7 konsisten; yang beda adalah pemilihan denominator fold-layak vs semua fold. | Ini bahasa sumber EVAL_C sendiri; mengubahnya berarti menulis ulang bukan sekadar menyajikan. Dilaporkan agar penyusun laporan memakai satu denominator. |
| C-2 | Tabel AC-1..AC-3 di Bab 1 §5 (baris 374-376) memakai kata **LULUS** untuk status acceptance kerangka PM1, bukan vonis alat. | Bukan vonis biner atas alat; dipertahankan sebagai catatan agar pembaca eksternal tidak salah baca. |
| C-3 | Kata "post-mortem" muncul 1 kali (baris 15) dalam kalimat negasi. | Memenuhi syarat "0 isi post-mortem"; menghapus kalimat justru menghilangkan penjelasan pemindahan riwayat ke CHANGELOG. |
| C-4 | Dokumen bab `V10_*.md` masih memuat 38-74 em-dash per file. | Deliverable (`.md` dan `.ipynb`) sudah 0 em-dash; bab adalah artefak antara yang sudah digantikan isinya oleh dokumen terakit. |

---

## 8. BATAS AUDIT

1. Audit memverifikasi **angka terhadap sumber**, bukan menghitung ulang seluruh kampanye evaluasi; nilai metrik
   diperiksa kesesuaiannya dengan JSON/dokumen EVAL primer, bukan direproduksi ulang dari data mentah.
2. Angka dataset yang bersifat "isi" (1.392 komponen tubular, 5.561 stasiun, 2.882 interval, 309.644 baris DLIS)
   ditelusuri ke dokumen verifikasi V6 (parser sudah dijalankan pihak bab data); yang dihitung ulang langsung dari
   disk adalah jumlah file XML, jumlah baris CSV utama, dan seluruh dataset latih V9.
3. Patch yang dilakukan bersifat penyajian (angka basi, anotasi kampanye, penyelarasan antar-bab); **tidak ada
   angka hasil evaluasi yang diubah**, dan seluruh angka lama tetap dapat ditelusuri di tempatnya.

---

## 9. SUMBER BUKTI (dibaca/dijalankan di sesi ini)

`code/v9_i1_pipeline.py` (dijalankan) · `code/v9_d1_01_bins.py` (daftar FILES) ·
`scratch/v9_d1/v9_d1_01_summary.json` (wells, 96.698/12.635) · `scratch/v9_d1/datasets/*.csv.gz` (292.954) ·
`scratch/v9_d1/lowo_*.json` (37 fold) · `scratch/v9_e_ml/*_RESULTS.json` (n_features 55, seed 42, 26 fold) ·
`scratch/v9_e_rule/v9_e_RULE_03_bitwear_toolwear_results.json` (auprc fold bit_wear) ·
`data/volve/labels_curated_v2_log.json` (884) · `data/volve/witsml_parsed/_parse_summary.json` (8 entri) ·
`wc -l` atas USROP_labeled.csv, time.csv F-9A, 10 CSV witsml_parsed, toolwear_windows.csv, TSPP1-4 ·
`docs/V9_EVAL_A_LAYERA.md`, `V9_EVAL_B_LAYERB.md`, `V9_EVAL_C_LAYERC.md`, `V9_E_STAT_ENGINE.md`,
`V9_PM1_ARCHITECTURE.md` baris 218, `V8_M1_CAPABILITY_MAP.md` §d, `V8_E_bit_wear_CAPABILITY.md`,
`V8_E_tool_wear_CAPABILITY.md`, `V3_WITSML_PARSE_REPORT.md`, `V6_D1a/D1c/D1d/D1f`, `V10_PM1_OUTLINE.md`.

*Selesai V10-A1. Proposal dinyatakan lolos audit dengan 3 temuan penyajian yang sudah dipatch (T1 pit 13 kolom,
T2 inventaris WITSML tiga jenjang, T3 anotasi kampanye bit_wear).*
