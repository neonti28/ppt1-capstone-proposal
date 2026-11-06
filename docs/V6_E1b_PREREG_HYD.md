# V6-E1b — Pra-Registrasi TAMBAHAN: kelas ke-5 `hyd` (anomali hidrolik, Volve-native)

Dokumen ini DITULIS SEBELUM model apa pun untuk kelas `hyd` dijalankan. SHA-256 dicatat di
komentar kartu `t_5e052df1` sebelum skrip training kelas ini. Status: **kampanye SEQUENTIAL
kedua** — keputusannya diinformasikan oleh hasil V6-E1a (§V6_E1_PREREG), tetapi hipotesis dan
gate ditetapkan di sini sebelum angka `hyd` diketahui. Hasil E1a dan E1b dilaporkan terpisah;
kegagalan E1a tidak boleh ditutupi oleh E1b.

Tanggal: 2026-10-10 (WIB), kartu `t_5e052df1`.

> **Riset pendahuluan: `experimental-design`** — kampanye sequential (group-sequential spirit):
> E1a selesai & gate-nya digunakan apa adanya (2 LULUS, 2 GAGAL); E1b adalah hipotesis BARU
> dengan desain yang dikunci sebelum data-label `hyd` dihitung menjadi hasil model. Unit =
> jendela, sumur = cluster, split LOWO identik dengan E1a (tak ada window sumur uji di latih).
> **Riset pendahuluan: `statistical-power`** — 7 sumur uji, prevalensi pilot 8,3%–26,2%,
> semua sumur punya ≥331 jendela positif (≥30 syarat evaluasi) → SEMUA fold layak dinilai;
> dengan n uji 1.616–10.401 dan prev ≥8%, sensitivitas cukup untuk membedakan lift 1,5
> (AUPRC ≥ 0,125 pada prev 8,3%) — dinyatakan sebagai sensitivitas, bukan observed power.
> **Riset pendahuluan: `scikit-learn`** — estimator, Pipeline, seed, dan class_weight IDENTIK
> dengan E1a (RF 300 pohon + LogReg; imputer median per fold; tanpa resampling); TIDAK ada
> tuning hyperparameter setelah melihat hasil.
> **Riset pendahuluan: `statistical-analysis`** — metrik primer AUPRC + lift vs prevalensi;
> CI95 moving-block bootstrap (blok 60, 1.000 resample, seed 42); gate konfirmatif di bawah.
> **Riset pendahuluan: `shap`** — deskriptif saja, tidak mengubah gate.

## 1. Hipotesis (H₁-E1b)

RF pada fitur mekanis 8 channel (TANPA SPPA/TFLO/SPM) mencapai lift ≥1,5 pada MAJORITAS
(>50%) dari 7 sumur uji, DAN AUPRC RF ≥ AUPRC canary-kedalaman pada mayoritas yang sama.

## 2. Data & hitungan sampel (DIHITUNG sebelum pra-registrasi; `scratch/v6_e1/ch31_hyd_summary.json`)

| Sumur | jendela eligible | positif | prevalensi |
|---|---|---|---|
| F-14  | 10.401 | 865 | 8,3% |
| F-15A | 6.156  | 698 | 11,3% |
| F-15_S| 8.355  | 993 | 11,9% |
| F-5   | 6.332  | 621 | 9,8% |
| F-7   | 2.482  | 421 | 17,0% |
| F-9   | 1.616  | 423 | 26,2% |
| F-9_A | 2.206  | 331 | 15,0% |
| **Total** | **37.548** | **4.352** | **11,6%** |

## 3. Label (dikunci)

Rumus persis V6-R1 §4.2 #7 yang sudah diverifikasi run-3 (`scratch/v6_r1_evidence/R1_run3_hydro_check.py`):
per sumur, atas bin 60 detik dengan `TFLO_mean` & `SPPA_mean` non-null: `qcut(TFLO,10)`,
`median` & `MAD` `SPPA` per bin aliran, `z = (SPPA − median)/(1.4826·MAD)`, anomali ⇔ `|z|>2`.
Jendela `hyd` = 1 bila **≥50% bin teramati** di `[t0, t0+10)` anomali, dengan **≥5 bin teramati**.
Sumber sinyal label: sensor tekanan/aliran (SPPA, TFLO) — TERPISAH dari fitur.

## 4. Fitur (dikunci — pengecualian anti-sirkular)

**8 channel × 5 statistik = 40 fitur**: `TQA, RPM, SWOB, HKLD, ROP, BPOS, depth, dbtm`.
**DIKECUALIKAN: `SPPA`, `TFLO`, `SPM`** — SPPA/TFLO dipakai label; SPM (stroke pompa) ≈
aliran → kalau masuk fitur, label jadi fungsi hampir deterministik dari fitur (sirkularitas
temporal). Asersi di skrip menolak ketiganya.

## 5. Model, split, metrik, gate (IDENTIK dengan E1a §6)

RF (300, min_leaf 5, balanced_subsample, seed 42) + LogReg sekunder; canary-B = RF
kedalaman saja; persistence = `y_prev_hyd`; split LOWO 7 fold; AUPRC/lift/ROC + CI block
bootstrap; sumur <30 positif = UNDERPOWERED (tidak ada di sini).
**G1:** lift RF ≥1,5 di >3,5 dari 7 fold (≥4 fold). **G2:** AUPRC RF ≥ canary-B di ≥4 fold.
LULUS/LEMAH/layak-bersyarat (persistence) sama seperti E1a.

## 6. Kelemahan yang dinyatakan di muka

1. Label residual SPPA-vs-aliran adalah **dysfunction proxy** (anomali tekanan pompa),
   bukan kegagalan pompa yang terverifikasi narasi.
2. Sinyal mungkin banyak berasal dari **kedalaman** (gaya gesek makin panjang) → G2 akan
   mengekspos hal ini; kalau RF ≈ canary-kedalaman, kelas dinyatakan LEMAH.
3. `TFLO`/`SPPA` dihitung atas agregat baris pengeboran per menit (bukan sampel mentah).
4. Kampanye ini sequential (keputusan setelah E1a) → status = konfirmatif kedua, bukan
   replikasi independen.
