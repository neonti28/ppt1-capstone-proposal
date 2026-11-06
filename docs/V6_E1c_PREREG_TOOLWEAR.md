# V6-E1c — Pra-Registrasi TAMBAHAN: kelas ke-6 `tool_wear` (dataset eksternal NYATA)

Dokumen ini DITULIS SEBELUM model apa pun untuk kelas `tool_wear` dijalankan. SHA-256 dicatat
di komentar kartu `t_5e052df1` sebelum skrip training kelas ini. Status: **kampanye sequential
ketiga**, diambil karena fallback yang diizinkan task ("jika 3 kelas tidak tercapai dari satu
sumber, gabung beberapa sumber — Volve + eksternal; catat label mana dari mana"). Hasil E1a,
E1b, E1c dilaporkan TERPISAH; kegagalan E1a/E1b tidak ditutupi oleh E1c.

Tanggal: 2026-10-10 (WIB), kartu `t_5e052df1`.

> **Riset pendahuluan: `experimental-design`** — unit = jendela 1 detik; klausa
> pseudoreplication: window dalam satu file berdekatan waktu → **split WAJIB kelompok per
> TOOL (Leave-One-Tool-Out, 4 fold)**, tidak boleh split acak per window (akan membocorkan
> identitas file). Proses tetap/berulang (satu konfigurasi 490 RPM, feed 0,285 mm/rev untuk
> semua file) → tidak ada fitur konfigurasi yang bisa dibocorkan.
> **Riset pendahuluan: `statistical-power`** — fold uji = 112–121 jendela (50–62 positif),
> semua ≥30 → semua fold layak dinilai; prevalensi ~50% sehingga gate lift 1,5 = AUPRC ≥0,75
> (sensitivitas dinyatakan begini, bukan observed power); n efektif untuk generalisasi =
> 4 alat (kecil → kesimpulan dibatasi pada generalisasi antar-alat dalam eksperimen ini).
> **Riset pendahuluan: `scikit-learn`** — estimator identik E1a (RF 300 pohon, min_leaf 5,
> balanced_subsample, seed 42; LogReg sekunder; imputer median + scaler HANYA di fold latih);
> tanpa tuning setelah hasil; asersi melarang `start_sample`, `file`, `run`, `tool` masuk fitur.
> **Riset pendahuluan: `statistical-analysis`** — metrik primer AUPRC + lift vs prevalensi
> (prev ≈ 0,5 per fold); CI95 = moving-block bootstrap (blok 10 jendela, 1.000 resample,
> seed 42) karena jendela dalam file bergantung waktu; gate konfirmatif di bawah.
> **Riset pendahuluan: `shap`** — deskriptif, tidak mengubah gate.

## 1. Hipotesis (H₁-E1c)

Pada Leave-One-Tool-Out (4 fold), RF dari 27 fitur akselerometer mencapai lift (AUPRC/prev)
≥ 1,5 pada ≥3 dari 4 fold, DAN AUPRC RF ≥ AUPRC canary-amplitudo (3 fitur RMS saja) pada
≥3 dari 4 fold.

## 2. Data & hitungan sampel (DIHITUNG sebelum pra-registrasi; `scratch/v6_e1/ch50_toolwear_summary.json`)

Sumber: Mendeley `th4yv974r2` (DOI 10.17632/th4yv974r2.1), **CC BY 4.0**, 8 file xlsx
diunduh dari API Mendeley dan **diverifikasi SHA-256 terhadap `content_details.sha256_hash`
API (8/8 cocok)** di `scratch/v6_e1/toolwear/`.

| Alat | jendela | R01 (baru) | R02 (tumpul) |
|---|---|---|---|
| T01 | 120 | 60 | 60 |
| T02 | 112 | 50 | 62 |
| T03 | 121 | 61 | 60 |
| T04 | 116 | 58 | 58 |
| **Total** | **469** | **229** | **240** |

## 3. Label (dikunci — sumber primer, bukan turunan fitur)

Kutipan deskripsi dataset Mendeley (API `description`, diunduh D2 → `mend_meta.json`):
*"The tool starts as a new tool at the beginning of run 1. The drilling process is stopped at
the end of run 1 and the tool is inspected visually for wear. Then the same tool is used to
continue the drilling process till it is completely blunt at the end of run 2."*
→ `y = 1` (R02, tumpul), `y = 0` (R01, baru). Label berasal dari **kondisi fisik terukur pada
eksperimen terkendali**, bukan fungsi dari data akselerometer (non-sirkular).

## 4. Fitur (dikunci — 27)

Per sumbu X/Y/Z (jendela 1000 sampel @1000 Hz): `mean, std, rms, kurtosis, skew, peak2peak,
crest, zcr` (24) + `fdom` frekuensi dominan per sumbu (3).
**LARANGAN (asersi di skrip):** `start_sample`, `file`, `run`, `tool`, nomor baris, atau
 statistik yang dihitung dari keseluruhan file (semua fitur wajib per-jendela saja).

## 5. Model, split, metrik, gate (semangat identik E1a)

- Model: RF (parameter E1a) primer; LogReg(+scaler) sekunder; Pipeline imputer median per fold.
- **Canary-B: RF dengan HANYA 3 fitur `X_rms, Y_rms, Z_rms`** (tingkat amplitudo saja —
  penanda keausan paling sederhana; padanan canary-kedalaman di E1a).
- **Split: Leave-One-Tool-Out (4 fold)** — fold uji = satu alat (kedua run-nya; kedua kelas
  ada di tiap fold uji). Tidak ada jendela alat uji di data latih.
- Metrik per fold: AUPRC, lift = AUPRC/prev, ROC-AUC, CI95 AUPRC (block bootstrap blok 10).
- Persistence TIDAK berlaku (label konstan dalam satu file → tidak ada pertanyaan "status
  sebelumnya" yang non-trivial); dinyatakan N/A, bukan dihilangkan diam-diam.
- **G1:** lift ≥1,5 di ≥3/4 fold. **G2:** AUPRC RF ≥ canary-B di ≥3/4 fold.
  LULUS jika keduanya; GAGAL jika salah satu; jika G1 lolos tapi G2 gagal → catat eksplisit
  "sinyal ada tapi hanya oleh tingkat amplitudo".

## 6. Kelemahan yang dinyatakan di muka

1. **Domain bengkel/mesin, bukan sumur minyak** — kelas ini memenuhi syarat "kerusakan
   nyata terukur" tetapi BUKAN dari domain Volve; dikombinasikan sesuai fallback task dan
   label asal dicatat (Volve vs eksternal).
2. **Label tercampur urutan percobaan**: R02 selalu dijalankan SETELAH R01 (perbedaan termal,
   kedalaman lubang, debu ikut berkembang bersama keausan) — tidak bisa dipisahkan dari
   desain data ini; dinyatakan sebagai batasan interpretasi.
3. **n alat = 4** → generalisasi terbatas pada populasi alat ini; jendela 469 berelasi waktu
   (n efektif jauh lebih kecil dari 469 untuk generalisasi lintas-alat).
4. Satu konfigurasi proses (490 RPM, feed 0,285 mm/rev) → tidak bisa menyimpulkan ke
   kondisi proses lain.
5. Dataset ini DIPAKAI SEBAGAI SUMBER LABEL TERPISAH — tidak digabungkan baris-per-baris
   dengan data Volve (domain berbeda); klaim "≥3 kriteria" dihitung per kelas + per sumber.
