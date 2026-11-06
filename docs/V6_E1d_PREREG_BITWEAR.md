# V6-E1d — Pra-Registrasi TAMBAHAN: kelas `bit_wear` (USROP Volve, high-MSE)

Dokumen ini DITULIS SEBELUM model apa pun untuk kelas `bit_wear` (USROP) dijalankan.
SHA-256 dicatat di komentar kartu `t_5e052df1` sebelum training. **Kampanye sequential
keempat dan TERAKHIR** — setelah ini tidak ada upaya kelas baru (menutup peluang
"shopping for significance"); hasil semua kampanye dilaporkan terpisah.

Tanggal: 2026-10-10 (WIB), kartu `t_5e052df1`.

> **Riset pendahuluan: `experimental-design`** — unit = jendela 100 baris depth-ordered per
> sumur; sumur = cluster → split LOWO (7 fold; 4 layak dinilai). Fitur = 100 baris SEBELUM
> anchor, label = 100 baris SESUDAH (horizon ke depan; task mengizinkan "J menit/meter ke
> depan"). Kanal pembentuk label (WOB, TQ, RPM, ROP, Hookload, MSE, D_exp, ROC_coef)
> DIKECUALIKAN dari fitur — label bukan fungsi deterministik dari fitur yang tersisa.
> **Riset pendahuluan: `statistical-power`** — prevalensi per sumur 0%–54%; syarat evaluasi
> ≥30 jendela positif → F-7 (0), F-9 (0), F-9_A (3) UNDERPOWERED/tidak bernilai positif dan
> TIDAK dihitung dalam mayoritas; 4 fold layak dinilai (F-14 91, F-15 155, F-15S 561,
> F-5 174 positif). Gate mayoritas dihitung atas fold layak (≥3 dari 4).
> **Riset pendahuluan: `scikit-learn`** — estimator identik E1a (RF 300 pohon, min_leaf 5,
> balanced_subsample, seed 42; LogReg sekunder; Pipeline imputer median per fold); tanpa
> tuning setelah hasil; asersi melarang kolom terlarang masuk daftar fitur.
> **Riset pendahuluan: `statistical-analysis`** — AUPRC + lift vs prevalensi per fold;
> CI95 moving-block bootstrap (blok 20 jendela, 1.000 resample, seed 42); gate konfirmatif.
> **Riset pendahuluan: `shap`** — deskriptif, tidak mengubah gate.

## 1. Hipotesis (H₁-E1d)

Pada LOWO, RF dari 30 fitur (SPP, flow, mud density, gamma, MD, TVD — TANPA kanal MSE)
mencapai lift ≥1,5 pada ≥3 dari 4 fold layak dinilai, DAN AUPRC RF ≥ AUPRC canary-
kedalaman (MD+TVD saja) pada ≥3 dari 4 fold yang sama.

## 2. Data & hitungan sampel (DIHITUNG sebelum pra-registrasi; `scratch/v6_e1/ch60_usrop_summary.json`)

Sumber: `data/USROP_labeled.csv` (198.928 baris, 7 sumur Volve). Label `high_MSE_bit_wear`
= Teale MSE > P75 (256.600 psi) — rumus & angka sudah diverifikasi ulang oleh R1 run-3
(korelasi log10 0,9999999999989 terhadap kolom MSE tersimpan).

| Sumur | jendela | positif | prev | status evaluasi |
|---|---|---|---|---|
| F-9 A | 271 | 3 | 1,1% | UNDERPOWERED (<30 pos) |
| F-7   | 124 | 0 | 0% | tidak bernilai (tanpa positif) |
| F-14  | 949 | 91 | 9,6% | layak |
| F-15  | 1.057 | 155 | 14,7% | layak |
| F-15S | 1.031 | 561 | 54,4% | layak |
| F-5   | 367 | 174 | 47,4% | layak |
| F-9   | 154 | 0 | 0% | tidak bernilai (tanpa positif) |
| **Total** | **3.953** | **984** | **24,9%** | 4 fold layak dinilai |

## 3. Label (dikunci)

`y = 1` bila ≥50% baris dalam jendela LABEL (100 baris sesudah anchor) ber-label
`high_MSE_bit_wear` pada kolom `label` tersimpan. Semantik jujur: **proxy keausan bit /
inefisiensi pengeboran** (Teale MSE; Menand & Mills 2017 membedakan vibration vs wear vs
balling lewat MSE) — BUKAN penilaian visual keausan bit. Kecuali kanal pembentuknya (lihat §4).

## 4. Fitur (dikunci — 30; kanal sirkular DILARANG)

6 kanal × 5 statistik (`mean, std, slope, last, frac`): `Average Standpipe Pressure`,
`Mud Flow In`, `Mud Density`, `USROP Gamma`, `Measured Depth`, `Hole Depth (TVD)`.
**LARANGAN (asersi):** `Weight on Bit`, `Average Surface Torque`, `Rate of Penetration`,
`Average Rotary Speed`, `Average Hookload`, `MSE`, `D_exp`, `ROC_coef`, `label`, `well`.
(Catatan: Hookload ikut dilarang karena ≈ proxy WOB yang membentuk label.)

## 5. Model, split, metrik, gate (identik semangat E1a)

- RF primer (parameter E1a) + LogReg sekunder; imputer median per fold.
- Canary-B: RF **hanya** fitur `MD`+`TVD` (10 fitur) — guard terhadap konfuk formasi/kedalaman.
- Split LOWO per sumur; metrik AUPRC/lift/ROC per fold; CI block bootstrap blok 20.
- **G1:** lift RF ≥1,5 di ≥3 dari 4 fold layak. **G2:** AUPRC RF ≥ canary-B di ≥3 dari 4 fold.
  Persistence dilaporkan (label jendela sebelumnya) sebagai diagnostic; jika persistence >
  RF di mayoritas fold → verdict diturunkan menjadi layak-bersyarat (aturan E1a §6).

## 6. Kelemahan yang dinyatakan di muka

1. Label sangat bervariasi antar sumur (0%–54%) → batas keputusan global P75 sangat
   dipengaruhi formasi per sumur; G2 (canary kedalaman) dirancang untuk mengekspos ini.
2. 3 sumur tidak bisa dinilai (tanpa/kurang positif) → klaim hanya bertumpu 4 fold.
3. Baris USROP berurutan depth (bukan waktu) → horizon "ke depan" = lebih dalam, bukan
   lebih lambat; interpretasi = prediksi kondisi pada kedalaman berikutnya.
4. F-9_A/F-7/F-9 tanpa positif TIDAK dihitung sebagai fold lolos maupun gagal.
