# RND-ALGO — RENCANA RISET ALGORITMA UNTUK 7 mode

Status: rencana kerja (belum vonis) · Board: `rnd-algo-2026` · 2026-10-25
Pemilik arah: operator (Zey) · Pelaksana: R&D, Data, Engineer, PM

## 1. Tujuan

Menjawab satu pertanyaan: **algoritma apa yang layak dipakai untuk menaikkan tier 7 mode
(vib, ssi, shk, stuck, hyd, bit_wear, tool_wear) dari bukti ilmiah, bukan dari selera?**

Keluaran yang diminta:
1. Peta algoritma → detektor → klaim (K-i/K-ii) → potensi tier, dengan justifikasi literatur.
2. Jawaban kelayakan data per algoritma (punya datanya atau tidak).
3. Protokol uji yang bisa direproduksi + hasil pilot nyata pada minimal satu mode.
4. Ledger provenance: setiap angka punya asal (standar, jurnal, atau run kita).

## 2. Aturan angka (WAJIB, tanpa pengecualian)

Setiap angka yang muncul di dokumen RND wajib punya baris di
`docs/RND_PROVENANCE_LEDGER.md` dengan 7 kolom:

| # | Angka | Satuan | Kelas sumber | Rujukan persis | Tanggal akses | Dipakai di | Status |
|---|---|---|---|---|---|---|---|

Kelas sumber yang diizinkan, berurut kekuatan:
- `STANDAR` — ISO/API/IEC/SPE. Contoh: 32,17405 ft/s² = 1 g (9,80665 m/s² × 3,280839895).
- `JURNAL` — DOI/URL, harus bisa dibuka. Cantumkan tahun, nama penulis pertama, judul.
- `RUN-KITA` — hasil eksekusi sendiri. Cantumkan file hasil + timestamp + perintah.
- `KONVENSI` — kesepakatan internal (mis. FAR ≤ 6/24 jam dari V9). Sebutkan dokumen asalnya.
- `BELUM-TERUKUR` — dilarang diubah jadi angka tebakan.

Aturan tambahan:
- Angka tanpa salah satu kelas di atas = **dilarang masuk dokumen**. Tulis "BELUM TERUKUR".
- Setiap rekomendasi algoritma wajib menyebut baseline pembanding (rule, persistence, canary,
  atau RF) dan angka pembandingnya, bukan hanya "lebih baik".
- Klaim "algoritma X lebih baik" tanpa uji statistik (CI/bootstrap/DeLong) = hipotesis, bukan hasil.

## 3. Pembagian peran (sesuai mandat operator)

- **R&D** — riset literatur, usul algoritma, uji kesesuaian, tulis opsi + bukti.
- **Data** — jawab ketersediaan data (kanal, sampling, panjang run, jumlah event, missing,
  censoring). Jawaban Data dipakai R&D untuk meriset ulang, bukan untuk menutup riset.
- **Engineer** — protokol eksperimen, implementasi pilot, reproducibility, runtime.
- **PM** — vonis: layak/tidak, dampak tier, risiko, dan apa yang harus dihentikan.

## 4. Keluarga algoritma yang diperiksa (mandat operator + perluasan)

| Kelompok | Algoritma | Dugaan peran di kasus ini |
|---|---|---|
| Metaheuristik kontinu | GWO, WOA, PSO, SSA, HHO, EPO, SMA, BGWO, EO, HBO, Horse Herd, Slime Mould | tuning hyperparameter, feature selection, kalibrasi ambang per well |
| Metaheuristik hibrida | WOA+GWO, VMD+SVM, VMD+GWO-SVM | dekomposisi sinyal getaran + klasifikasi |
| Stokastik/diskret | Markov chain, HMM, Monte Carlo, MCMC, Bayesian network | transisi state, ketidakpastian onset, simulasi FAR |
| Survival | Cox, Random Survival Forest, DeepHit | lead-time dengan data tersensor |
| Boosting modern | LightGBM, XGBoost, CatBoost + isotonic/Platt + conformal | FAR terkendali, CI valid |
| Deteksi perubahan/drift | CUSUM, Page-Hinkley, BOCPD, ADWIN, KS | regime change tool_wear, drift antar well |
| Anomali tanpa label | Isolation Forest, LOF, autoencoder, one-class SVM, matrix profile | kelas tanpa label (hyd K-ii, bit_wear K-2) |

Algoritma di luar daftar ini boleh diusulkan R&D asal ada justifikasi literatur dan data.

## 5. DAG kartu (16 kartu, termasuk loop R&D ↔ Engineer)

```
P0 Protokol provenance ─┐
D0 Kelayakan data ──────┤
E0 Audit implementasi detektor (leakage, sirkularitas, konsistensi)
                        ├─> R1 Metaheuristik kontinu
                        ├─> R2 Stokastik + survival
                        ├─> R3 VMD/EMD + SVM/kernel
                        ├─> R4 Boosting + kalibrasi
                        ├─> R5 Drift + anomali tanpa label
                        └─> R6 Metrik & uji statistik
                                    │
                    E1 Matriks kelayakan (algo x detektor)
                                    │
                    E2 Protokol pilot (3 kandidat)
                                    │
                    E3 Eksekusi pilot (hyd K-i) ── hasil nyata
                                    │
                    R7 R&D menilai hasil engineer
                          │                     │
              (kalau tidak memuaskan)   (kalau implementasi salah)
                          └────> E4 Engineer memperbaiki + run ulang <─ E0
                                    │
                    V1 Audit provenance + sitasi
                                    │
                    PM Vonis + roadmap tier
```

Aturan loop: R&D tidak boleh menuduh implementasi salah tanpa menunjuk file dan baris.
Engineer tidak boleh menutup temuan tanpa memperbaiki kode atau membantah dengan hasil run.
Kalau R7 menyimpulkan algoritma yang salah, R&D wajib mengusulkan algoritma pengganti
dan eksperimen pembeda, bukan mengulang eksperimen yang sama.

## 6. Gate keputusan (tidak berubah dari V9)

Naik tier hanya boleh diusulkan bila tiga syarat terpenuhi bersamaan:
1. **C stabil**: hasil tidak hanyut antar well/alat (CI tidak memuat no-skill).
2. **A memadai**: FAR pada titik operasi ≤ 6 per 24 jam (rig) atau ≤ 1 alarm/menit (bengkel).
3. **B wajar**: beban pemeriksaan manusia dapat diterima (FP per shift, bukan per menit).

Tanpa ketiganya, algoritma baru tetap di TREN walau akurasinya terlihat tinggi.

## 7. Konkurensi dan biaya

- Board terpisah `rnd-algo-2026`, dispatch maksimal **2 worker** per pass (5 paralel pernah
  ditolak owner: "Kanban owner refused").
- Model kartu: `deepseek-flash` (provider `deepseek`). 9router hanya untuk websearch/webfetch.
- Runtime maksimum per kartu 30 menit; hasil wajib ditulis ke file, bukan hanya ke log.
- Kartu yang gagal 2x otomatis blocked, tidak diulang tanpa perubahan strategi.

## 8. Definisi selesai

Riset ini selesai kalau:
- 13 kartu tuntas atau dinyatakan blocked dengan alasan teknis yang jelas;
- setiap rekomendasi punya DOI/URL yang bisa dibuka + status data dari tim Data;
- ledger provenance terisi dan lolos audit V1 (tidak ada angka tanpa sumber);
- PM mengeluarkan vonis: algoritma mana yang masuk roadmap, mana yang ditolak, dan alasannya.

## 9. Yang TIDAK dilakukan di gelombang ini

- Tidak mengubah ambang detektor yang sudah ada tanpa bukti pilot.
- Tidak mengklaim transfer domain (bengkel → rig) yang belum diuji.
- Tidak memakai dataset baru tanpa izin/lisensi yang jelas.
- Tidak menyentuh folder arsip `D:\Capstone 1`.
