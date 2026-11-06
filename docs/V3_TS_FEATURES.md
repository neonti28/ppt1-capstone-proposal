# V3 — Fitur Time-Series WITSML (window pra-event, anti-leakage) — T10

Status: **SELESAI + TERVERIFIKASI** (2026-10-05)
Eksekusi: `code/60_ts_features.py` (83,8 s, satu kampanye, tanpa melihat test) — hasil: **661 event × 480 fitur**
Verifikasi independen: `code/61_verify_ts_features.py` → **8/8 PASS** (jalur kode berbeda)

Output:

| File | Isi |
|---|---|
| `data/predictive/features_timeseries.npz` | X (661×480), X_baseline (661×11), X_window_meta (661×12), event_id/fold/wellbore/act_start_utc/category/outcome, names |
| `data/predictive/features_timeseries_meta.json` | jendela, definisi fitur, resolusi channel per fold, fill-rate, coverage, **anti_leakage.violations=0** |
| `data/predictive/features_timeseries_events.csv` | audit per event: n_rows, gap_median/max, full_window per jendela |

---

## 1. Cakupan label → fitur (memperbaiki peringatan pemetaan T9 §3)

Pemetaan **eksplisit** label wellbore → fold CSV (dipakai ulang dari `code/51` FOLD2LABEL), dengan rantai bukti:

- nama file USROP mentah `Norway-<prefix>_<well> depth.csv` **== nama folder WITSML** (lihat `_parse_summary.json` kolom `folder`);
- `USROP_A N` → label wellbore: `V2_DATA_JOIN_REPORT` (join 99,998% utk A4; signature lubang/casing + TD utk A3/A4).

| Fold CSV (hasil T9) | Folder WITSML sumber | Label wellbore | Event |
|---|---|---|---:|
| F-14.csv | Norway-StatoilHydro-…-F-14 | NO 15/9-F-14 | 182 |
| F-5.csv | Norway-StatoilHydro-…-F-5 | NO 15/9-F-5 | 134 |
| F-15A.csv | **Norway-StatoilHydro-…-F-15** | NO 15/9-F-15 A | 32 |
| F-15_S.csv | Norway-StatoilHydro-…-F-15S | NO 15/9-F-15 | 105 |
| F-9_A.csv | Norway-NA-…-F-9 A | NO 15/9-F-9 A | 94 |
| F-9.csv | Norway-StatoilHydro-…-F-9 | NO 15/9-F-9 | 56 |
| F-7.csv | Norway-Statoil-…-F-7 | NO 15/9-F-7 | 58 |

> **Risiko yang diakui (bukan penemuan baru):** pemetaan F-15 dan F-15S memakai bukti struktural (signature lubang + program casing + TD), bukan nama — nama Norway berlawanan dengan label DDR. F-15S tidak terdaftar di NPD FactPages (T7). Sumber: `V2_DATA_JOIN_REPORT` §90–91, §237.

**Aritmetika coverage (diverifikasi otomatis):**

```
884 label
- 213 tanpa CSV WITSML  → F-15 D 122, F-15 C 89, F-15 B 2
    (folder WITSML F-15A / F-15B / NO-F-15 TIDAK diparse T9 — di luar cakupan T10)
-  10 out-of-range       → event 183–189 (F-15_S, Nov–Des 2007, sebelum data 2008-09-08),
                           event 540–541 (F-5, sebelum 2007-11-15), event 676 (F-7, sebelum 2007-09-15)
= 661 event dengan fitur time-series
```

`VAR_F-5_alt.csv` (varian folder kedua F-5) **sengaja tidak dipakai** — keputusan pemakaian varian dilepas ke T2-d (V3_WITSML_PARSE_REPORT §5).

## 2. Jendela pra-event (dokumentasi pilihan)

| Jendela | Panjang | Alasan |
|---|---|---|
| `w30m` | 30 menit | pendahulu segera — gejala operasional menit-jam sebelum kejadian |
| **`w2h` (primer)** | **2 jam** | **~1 stand/siklus koneksi: sinyal mekanis + hidrolik lengkap, sample size memadai** |
| `w6h` | 6 jam | konteks shift/operasi lebih luas (trend lambat, persiapan trip) |

Aturan potong: **window `[act_start − W, act_start)` ketat — semua sampel `timestamp < act_start`.**
Tiga jendela dihitung dalam SATU kampanye (desain fitur tidak melihat test set).

## 3. Channel (16 kanonik) dan resolusi kolom

Seleksi: channel fisik drilling yang **fill ≥50% di file** (`_verify.json`, threshold T9) — via kolom base **atau** varian `GS_` (F-15A & F-9_A hanya punya salinan ber-fill tinggi dengan prefix `GS_`):

```
Channel : DMEA DBTM DVER BPOS SWOB HKLD TQA RPM SPPA TFLO MWTI MDOA ROP GASA CHKP SPM1
7/7 fold: DMEA DBTM DVER BPOS SWOB HKLD TQA SPPA TFLO MWTI ROP GASA CHKP SPM1
6/7      : RPM (absen ≥50% di F-9)        5/7: MDOA (absen di F-15_S, F-9)
Variant  : F-15A & F-9_A = GS_ (semua channel); fold lain = base
```

- **Tidak eligible → semua statistik channel itu NaN utk fold itu** (tanpa interpolasi, dicatat di meta `channel_resolution_per_fold`).
- `ACTC` (rig mode, diskret) sengaja dikecualikan: mean tidak bermakna.
- Channel kandidat dari T9 §4 yang **tidak lolos ≥50%**: `DEPT` (0 fold — pakai `DMEA`), `ECD_ARC_RT`, `SHKRSK_RT`, `SHKTOT_RT` (0 fold), `Bit_RPM` (2 fold) → tidak dipakai.
- `PASS_NAME` kategorikal → tidak dipakai sebagai channel numerik.

## 4. Statistik per channel per jendela (10 fitur — tanpa interpolasi)

| Statistik | Definisi |
|---|---|
| `mean` / `std` / `min` / `max` | basis atas sampel valid (std ddof=1) |
| `slope_per_min` | slope OLS nilai ~ waktu (per menit) |
| `trend_rho` | Spearman ρ nilai vs waktu (−1..1); **NaN bila nilai konstan** (mis. DMEA diam, SWOB=0 — terverifikasi: 356/470 event dgn data DMEA benar-benar konstan di jendela) |
| `delta_mean` | rata-rata selisih bertanda antar sampel valid berurutan |
| `delta_absmean` | rata-rata \|selisih\| antar sampel valid berurutan |
| `burstiness` | `std(diff)/std(level)` — variasi cepat relatif variasi total |
| `missing_rate` | fraksi baris jendela ber-`NaN` (NaN bila n_rows=0) |

- **Minimal 5 sampel valid** utk statistik selain `missing_rate` (selain itu NaN).
- **Gap antar-sampel DICATAT, tidak diinterpolasi**: `n_rows`, `gap_median_s`, `gap_max_s`, `full_window` per jendela (`X_window_meta`). Median gap di jendela ≈ **4,9 detik** (median n_rows: 379 / 1.515 / 4.549 utk 30m/2h/6h).

## 5. Baseline kontrol "sensor vs posisi" (11 fitur, jendela 2h)

- **Kedalaman saja (7):** `md_mean, md_std, md_min, md_max, md_slope_per_min, md_last, md_delta` — statistik DMEA (hole depth MD), identik dgn jalur channel, tanpa sensor mekanis/hidrolik.
- **Waktu (4):** `time_hour_sin/cos, time_dow_sin/cos` — hour-of-day + day-of-week (UTC) dari `act_start` = **konteks waktu yang diketahui saat scoring** (jendela berakhir tepat di saat prediksi), bukan informasi pasca-event. Disimpan terpisah (`X_baseline`) agar T2-d dapat membuangnya pada tes murni posisi.

## 6. Anti-leakage — VERIFIKASI (bukan klaim)

| Cek | Hasil |
|---|---|
| Pemanggilan utama: semua sampel `ts < act_start` (slice searchsorted `[t-W, t)`) | **4.274.005 baris dipindai → pelanggaran = 0** (meta: `anti_leakage.violations=0`, `pass=true`) |
| Verifier independen `code/61` (mask pandas, jalur kode berbeda, 12 event acak × 3 jendela) | **87.477 baris → 0 pelanggaran** |
| Regr-eval ulang mean/std/n_rows vs npz (96 cek) | **cocok semua** |
| Nama fitur bebas `act_end`/`outcome`/`label` | **0 match** |
| Coverage aritmetik 884−213−10=661 | **cocok** |

## 7. Kualitas data (jujur)

- **Window tanpa baris WITSML sama sekali** (well tidak logging saat event): 194 (30m) / **191 (2h)** / 185 (6h) dari 661; **185 event kosong di ketiga jendela**. Per fold (2h): F-9_A 82/94, F-14 46/182, F-9 30/56, F-7 20/58, F-15_S 11/105, F-5 2/134, F-15A 0/32. Event tsb. tetap ada baris (fitur NaN) agar coverage auditable — bukan dibuang diam-diam.
- **NaN fraksi fitur sensor**: 0,382 (30m) / 0,368 (2h) / 0,351 (6h) — didominasi window kosong (~29%) + channel tak eligible (MDOA/RPM) + channel konstan (`trend_rho`).
- **Window terpotong** (`full_window=0`): 1 event (w6h) — window mulai sebelum awal data fold.
- Timezone: `act_start` offset label (+01/+02) dikonversi ke UTC; belum disilang jam operasi lokal CET (catatan T9 §5) — konsisten dgn timestamp CSV (`Z`).

## 8. Cara muat (untuk T2-d)

```python
import numpy as np
z = np.load("data/predictive/features_timeseries.npz", allow_pickle=True)
X, names = z["X"], list(z["feature_names"])        # 480 = 3 jendela × 16 channel × 10 stat
# nama fitur: "<w>__<channel>__<stat>", w in {w30m, w2h, w6h}
XB, bnames = z["X_baseline"], list(z["baseline_names"])   # 11 baseline
XM, mnames = z["X_window_meta"], list(z["window_meta_names"])
meta = json.load(open("data/predictive/features_timeseries_meta.json"))  # definisi + fill-rate
```

`outcome`/`category` ikut tersimpan utk labeling T2-d; **fitur tidak pernah membacanya**.

## 9. Batasan & langkah berikut (T2-d)

1. 213 label F-15 B/C/D tanpa fitur time-series (folder WITSML-nya tidak diparse T9) — jika dibutuhkan, perlu parse fold baru (kartu T9).
2. Window kosong (185 event) = sinyal "well tidak logging" — T2-d putuskan apakah jadi negatif/flag terpisah, jangan diimputasi diam-diam.
3. Varian `VAR_F-5_alt` belum dipakai (keputusan di T2-d).
4. Pemetaan F-15/F-15S masih "asumsi terkuat, belum tervalidasi independen" (V2_DATA_JOIN_REPORT §237) — sudah ada sebagai caveat.
