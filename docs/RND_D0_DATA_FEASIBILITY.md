# RND-D0: KELAYAKAN DATA PER ALGORITMA (jawaban tim Data)

Status: hasil pengukuran data, bukan vonis algoritma · Board: `rnd-algo-2026` · Kartu: `t_34c20c78` · 2026-10-27
Workspace: `/mnt/d/Capstone 1(v2)` (folder arsip `D:\Capstone 1` tidak disentuh).
Keluaran: dokumen ini + baris ledger di `docs/RND_PROVENANCE_LEDGER.md`.

Riset pendahuluan: literature-review, scientific-critical-thinking, verification-mandatory, plus statistical-analysis (pemisahan OBSERVED / DERIVED / BELUM TERUKUR) dan sequentialthinking.

## 0. Metode, sumber, dan cara reproduksi

Riset pendahuluan: verification-mandatory. Setiap angka di bawah dibaca langsung dari file, bukan dari ingatan atau dari dokumen lama. Skrip pengukur disimpan di workspace kartu dan bisa dijalankan ulang:

| Skrip | Sumber yang dibaca | Keluaran |
|---|---|---|
| `meas1.py` | `scratch/v9_d1/datasets/*.csv.gz`, `scratch/v9_d1/bins/*.csv.gz` | `meas1_windows_bins.json` |
| `meas2.py` | `data/volve/witsml_parsed/<WELL>.csv` (kanal mentah) | `meas2_native_cadence.json` |
| `meas3.py` | `data/USROP_labeled.csv`, `scratch/v6_e1/toolwear_windows.csv` | `meas3_external.json` |
| `meas4.py` | `data/witsml_parsed/*.qc.json`, `data/witsml/Norway-NA-15_47_9-F-9 A time.csv` | `meas4_pit.json` |
| `meas5.py` | bins + dataset jendela (state diskret, transisi, baseline bersih) | `meas5_states_baseline.json` |

Perintah: `/home/neonti/.venv_audit/bin/python3 meas1.py` dan seterusnya (venv ini punya pandas dan numpy; `python3` default Hermes tidak).
Riset pendahuluan: sequentialthinking. Lima pikiran dipakai di kartu ini, yaitu (1) inventaris sumber yang bisa dibaca ulang, (2) uji pemisah kelayakan VMD/EMD lewat laju sampel nyata, (3) ketersediaan state diskret dan kejadian onset, (4) kanal tanpa label dan panjang baseline bersih, (5) verifikasi silang angka eksternal dan penandaan yang belum terukur. Jumlah pikiran: **5**.

## 1. Per engine: jendela, well, prevalensi, missing kanal kunci

Sumber: `scratch/v9_d1/datasets/*.csv.gz` (grid 1 menit, fitur jendela 10 menit, label jendela berikutnya). Missing kanal diukur pada dataset jendela (kolom `<KANAL>_mean`).

| Engine | Berkas | Jendela | Well | Positif | Prevalensi | Rentang (hari) |
|---|---|---|---|---|---|---|
| `vib` | `scratch/v9_d1/datasets/vib.csv.gz` | 23.922 | 4 | 5.429 | 22,7% | 3,8 |
| `ssi` | `scratch/v9_d1/datasets/ssi.csv.gz` | 35.906 | 9 | 607 | 1,7% | 12,4 |
| `shk` | `scratch/v9_d1/datasets/shk.csv.gz` | 56.495 | 9 | 2.005 | 3,5% | 12,4 |
| `stuck_k1` | `scratch/v9_d1/datasets/stuck_k1.csv.gz` | 5.555 | 2 | 2.007 | 36,1% | 7,1 |
| `stuck_k2` | `scratch/v9_d1/datasets/stuck_k2.csv.gz` | 118.567 | 4 | 1.975 | 1,7% | 10,2 |
| `hyd_ki` | `scratch/v9_d1/datasets/hyd_ki.csv.gz` | 52.509 | 9 | 7.172 | 13,7% | 12,4 |

Catatan waktu: kolom `ts_bin` pada dataset jendela adalah detik relatif dengan titik nol di luar epoch Unix, karena itu tanggal absolut tidak dicantumkan (konversi langsung menghasilkan artefak 1970). Contoh terverifikasi: WITSML F-14 dimulai 2007-11-04T13:00:13.968Z menurut kolom `timestamp` pada `data/volve/witsml_parsed/F-14.csv`. Panjang rentang per engine di atas dihitung dari selisih `ts_bin`.

Prevalensi per well (jumlah jendela, positif, prevalensi):

| Engine | Well | Jendela | Positif | Prevalensi |
|---|---|---|---|---|
| `vib` | F-14 | 1.989 | 1.124 | 56,5% |
| `vib` | F-15A | 6.482 | 1.543 | 23,8% |
| `vib` | F-15_S | 10.903 | 1.532 | 14,1% |
| `vib` | F-5 | 4.548 | 1.230 | 27,0% |
| `ssi` | F-10 | 7.133 | 161 | 2,3% |
| `ssi` | F-12 | 4.293 | 83 | 1,9% |
| `ssi` | F-14 | 5.455 | 75 | 1,4% |
| `ssi` | F-15A | 6.020 | 31 | 0,5% |
| `ssi` | F-15_S | 5.342 | 85 | 1,6% |
| `ssi` | F-5 | 4.714 | 102 | 2,2% |
| `ssi` | F-7 | 982 | 3 | 0,3% |
| `ssi` | F-9 | 1.126 | 12 | 1,1% |
| `ssi` | F-9_A | 841 | 55 | 6,5% |
| `shk` | F-10 | 7.899 | 146 | 1,8% |
| `shk` | F-12 | 5.405 | 217 | 4,0% |
| `shk` | F-14 | 11.205 | 760 | 6,8% |
| `shk` | F-15A | 6.484 | 41 | 0,6% |
| `shk` | F-15_S | 11.394 | 259 | 2,3% |
| `shk` | F-5 | 7.140 | 240 | 3,4% |
| `shk` | F-7 | 2.761 | 267 | 9,7% |
| `shk` | F-9 | 1.851 | 45 | 2,4% |
| `shk` | F-9_A | 2.356 | 30 | 1,3% |
| `stuck_k1` | F-14 | 3.201 | 432 | 13,5% |
| `stuck_k1` | F-9_A | 2.354 | 1.575 | 66,9% |
| `stuck_k2` | F-10 | 4.216 | 772 | 18,3% |
| `stuck_k2` | F-14 | 95.925 | 389 | 0,4% |
| `stuck_k2` | F-9 | 16.184 | 311 | 1,9% |
| `stuck_k2` | F-9_A | 2.242 | 503 | 22,4% |
| `hyd_ki` | F-10 | 7.571 | 1.394 | 18,4% |
| `hyd_ki` | F-12 | 7.390 | 1.426 | 19,3% |
| `hyd_ki` | F-14 | 10.401 | 865 | 8,3% |
| `hyd_ki` | F-15A | 6.156 | 698 | 11,3% |
| `hyd_ki` | F-15_S | 8.355 | 993 | 11,9% |
| `hyd_ki` | F-5 | 6.332 | 621 | 9,8% |
| `hyd_ki` | F-7 | 2.482 | 421 | 17,0% |
| `hyd_ki` | F-9 | 1.616 | 423 | 26,2% |
| `hyd_ki` | F-9_A | 2.206 | 331 | 15,0% |

Missing kanal kunci pada dataset jendela (fraksi baris NaN dari kolom `<KANAL>_mean`):

| Engine | TQA | SPPA | TFLO | RPM | SWOB | HKLD | ROP | BPOS | SPM | depth | dbtm |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `vib` | 0,0% | 0,0% | 6,1% | 0,0% | 0,0% | 0,0% | 0,0% | 0,0% | 100,0% | 0,0% | 0,0% |
| `ssi` | 0,0% | 0,0% | 3,0% | 0,0% | 0,0% | 0,0% | 3,4% | 0,0% | 100,0% | 0,2% | 0,3% |
| `shk` | 0,0% | 0,0% | 2,8% | 0,0% | 0,0% | 0,0% | 2,6% | 0,0% | 100,0% | 0,0% | 0,0% |
| `stuck_k1` | 0,0% | 0,0% | 0,0% | 0,0% | 0,0% | 0,0% | 2,9% | 0,0% | 100,0% | 0,0% | 0,0% |
| `stuck_k2` | 0,5% | 0,5% | 0,5% | 3,1% | 0,1% | 0,2% | 1,0% | 0,1% | 0,3% | 0,0% | 0,1% |
| `hyd_ki` | 0,0% | tidak ada kolom | tidak ada kolom | 0,0% | 0,0% | 0,0% | 3,1% | 0,0% | tidak ada kolom | 0,2% | 0,2% |

Ketersediaan kanal label di bins 1 menit (bins yang benar-benar membawa sinyal). Empat kanal ini, yaitu VIBLAT, SHKRSK, STUCK, dan CRPM, tidak punya kolom `<KANAL>_mean` di dataset jendela, jadi missing-nya dilaporkan sebagai fraksi bin yang membawa sinyal, bukan sebagai NaN kolom fitur:

| Well | VIBLAT | SHKRSK | STUCK | CRPM |
|---|---|---|---|---|
| F-10 | 0,0% | 31,6% | 11,6% | 25,2% |
| F-12 | tidak ada kanal | 11,0% | tidak ada kanal | 13,1% |
| F-14 | 2,3% | 13,5% | 4,4% | 12,2% |
| F-15A | 27,3% | 28,6% | tidak ada kanal | 26,0% |
| F-15_S | 11,7% | 13,3% | tidak ada kanal | 11,5% |
| F-5 | 10,1% | 15,2% | tidak ada kanal | 11,6% |
| F-7 | tidak ada kanal | 8,9% | tidak ada kanal | 6,6% |
| F-9 | 4,7% | 13,9% | 4,2% | 9,7% |
| F-9_A | tidak ada kanal | 8,6% | 8,6% | 2,9% |

## 2. Sampling dan kontinuitas (penentu kelayakan VMD/EMD/wavelet)

Sumber: CSV WITSML terparse `data/volve/witsml_parsed/<WELL>.csv`, kanal mentah, bukan bins. Laju sampel dilaporkan sebagai median jarak antar sampel per kanal.

| Well | Kanal | Sampel | Median dt (dtk) | Laju (Hz) | Gap > 60 dtk | Segmen kontinu terpanjang | Panjang segmen (jam) |
|---|---|---|---|---|---|---|---|
| F-10 | `SHKRSK_RT` | 69.192 | 3,000 | 0,3333 | 326 | 3.321 sampel | 2,77 |
| F-10 | `TQA` | 258.441 | 3,000 | 0,3333 | 21 | 55.723 sampel | 46,44 |
| F-10 | `CRPM_RT` | 64.295 | 3,000 | 0,3333 | 324 | 3.324 sampel | 2,77 |
| F-10 | `STUCK_RT` | 9.545 | 30,000 | 0,0333 | 91 | 402 sampel | 3,35 |
| F-12 | `CRPM_RT` | 169.185 | 3,024 | 0,3307 | 8.616 | 7.834 sampel | 6,58 |
| F-12 | `TQA` | 1.667.867 | 5,011 | 0,1996 | 76 | 97.707 sampel | 136,00 |
| F-12 | `SHKRSK_RT` | 25.970 | 59,961 | 0,0167 | 9.591 | 467 sampel | 7,78 |
| F-14 | `TQA` | 1.226.483 | 4,925 | 0,2030 | 40 | 163.117 sampel | 223,15 |
| F-14 | `SHKRSK_RT` | 21.643 | 47,952 | 0,0209 | 5.408 | 2.959 sampel | 39,41 |
| F-14 | `CRPM_RT` | 23.110 | 20,995 | 0,0476 | 4.784 | 2.212 sampel | 12,90 |
| F-14 | `STUCK_RT` | 5.147 | 50,976 | 0,0196 | 74 | 298 sampel | 4,22 |
| F-14 | `VIBLAT_RT` | 2.247 | 60,048 | 0,0167 | 1.550 | 332 sampel | 5,54 |
| F-15A | `VIBLAT_RT` | 50.794 | 3,975 | 0,2516 | 4.608 | 3.972 sampel | 4,39 |
| F-15A | `TQA` | 202.903 | 3,024 | 0,3307 | 169 | 19.446 sampel | 16,33 |
| F-15A | `CRPM_RT` | 50.413 | 3,975 | 0,2516 | 4.571 | 3.974 sampel | 4,39 |
| F-15A | `SHKRSK_RT` | 52.126 | 3,975 | 0,2516 | 5.168 | 3.974 sampel | 4,39 |
| F-15_S | `TQA` | 1.537.360 | 4,000 | 0,2500 | 24 | 160.156 sampel | 177,95 |
| F-15_S | `VIBLAT_RT` | 141.114 | 3,000 | 0,3333 | 4.125 | 4.138 sampel | 3,45 |
| F-15_S | `CRPM_RT` | 137.170 | 3,000 | 0,3333 | 4.138 | 4.138 sampel | 3,45 |
| F-15_S | `SHKRSK_RT` | 152.923 | 3,000 | 0,3333 | 5.176 | 4.139 sampel | 3,45 |
| F-5 | `TQA` | 865.089 | 4,061 | 0,2462 | 27 | 44.649 sampel | 50,37 |
| F-5 | `CRPM_RT` | 46.529 | 3,974 | 0,2516 | 760 | 6.789 sampel | 7,49 |
| F-5 | `SHKRSK_RT` | 53.738 | 3,974 | 0,2516 | 961 | 6.785 sampel | 7,49 |
| F-5 | `VIBLAT_RT` | 43.565 | 3,974 | 0,2516 | 728 | 6.789 sampel | 7,49 |
| F-7 | `HKLD` | 405.567 | 4,925 | 0,2030 | 13 | 110.735 sampel | 151,49 |
| F-7 | `SHKRSK_RT` | 3.659 | 48,038 | 0,0208 | 1.064 | 213 sampel | 2,84 |
| F-7 | `SPPA` | 405.563 | 4,925 | 0,2030 | 13 | 110.735 sampel | 151,49 |
| F-7 | `ROP` | 405.567 | 4,925 | 0,2030 | 13 | 110.735 sampel | 151,49 |
| F-7 | `TQA` | 405.488 | 4,925 | 0,2030 | 14 | 105.988 sampel | 145,00 |
| F-7 | `TFLO` | 405.567 | 4,925 | 0,2030 | 13 | 110.735 sampel | 151,49 |
| F-7 | `CRPM_RT` | 2.769 | 47,952 | 0,0209 | 873 | 144 sampel | 1,92 |
| F-9 | `TQA` | 320.609 | 4,925 | 0,2030 | 8 | 74.730 sampel | 102,23 |
| F-9 | `SHKRSK_RT` | 13.817 | 17,971 | 0,0556 | 60 | 1.929 sampel | 9,63 |
| F-9 | `CRPM_RT` | 9.875 | 17,971 | 0,0556 | 46 | 1.928 sampel | 9,62 |
| F-9 | `VIBLAT_RT` | 6.475 | 3,974 | 0,2516 | 10 | 1.931 sampel | 2,13 |
| F-9 | `STUCK_RT` | 5.728 | 3,974 | 0,2516 | 10 | 1.929 sampel | 2,13 |
| F-9_A | `SPPA` | 85.921 | 3,000 | 0,3333 | 7 | 17.692 sampel | 14,74 |
| F-9_A | `TFLO` | 83.557 | 3,000 | 0,3333 | 7 | 752 sampel | 0,63 |
| F-9_A | `HKLD` | 86.306 | 3,000 | 0,3333 | 6 | 17.692 sampel | 14,74 |
| F-9_A | `SHKRSK_RT` | 45.927 | 3,000 | 0,3333 | 66 | 3.828 sampel | 3,19 |
| F-9_A | `STUCK_RT` | 45.712 | 3,000 | 0,3333 | 65 | 3.827 sampel | 3,19 |
| F-9_A | `TQA` | 85.921 | 3,000 | 0,3333 | 7 | 17.692 sampel | 14,74 |
| F-9_A | `ROP` | 74.219 | 3,000 | 0,3333 | 6 | 12.508 sampel | 10,42 |
| F-9_A | `CRPM_RT` | 15.184 | 3,000 | 0,3333 | 35 | 2.340 sampel | 1,95 |

Kanal yang tidak ada di well tertentu: F-12: VIBLAT_RT, STUCK_RT; F-15A: STUCK_RT; F-15_S: STUCK_RT; F-5: STUCK_RT; F-7: VIBLAT_RT, STUCK_RT; F-9_A: VIBLAT_RT

Tafsir yang bisa dibuktikan: laju sampel tertinggi yang terukur pada kanal label adalah 0,3333 Hz (VIBLAT_RT dan SHKRSK_RT di F-15_S, TQA di F-9_A dan F-10), sedangkan VIBLAT_RT di F-14 hanya 0,0167 Hz (satu sampel per 60 detik). Frekuensi Nyquist tertinggi yang tersedia karena itu 0,1667 Hz. VMD, EMD, dan wavelet hanya bisa membedah pita di bawah 0,17 Hz pada data ini.

Bins per well: jumlah menit, kerapatan baris mentah per menit, dan gap.

| Well | Bin 1 menit | Rentang (jam) | Baris mentah | Baris/menit (median) | Baris/menit (p95) | Gap > 1 mnt | Gap > 5 mnt |
|---|---|---|---|---|---|---|---|
| F-10 | 41.446 | 11,8 | 773.674 | 14 | 34 | 2 | 1 |
| F-12 | 180.958 | 1.209,1 | 2.081.567 | 11 | 26 | 16 | 7 |
| F-14 | 96.698 | 1.151,6 | 1.648.026 | 13 | 32 | 13 | 8 |
| F-15A | 44.347 | 991,6 | 778.162 | 14 | 34 | 7 | 3 |
| F-15_S | 101.630 | 1.028,1 | 1.883.062 | 13 | 42 | 14 | 6 |
| F-5 | 67.934 | 1.147,3 | 1.286.967 | 13 | 34 | 6 | 3 |
| F-7 | 34.533 | 1.171,7 | 547.500 | 13 | 31 | 7 | 5 |
| F-9 | 25.460 | 1.142,6 | 457.545 | 13 | 33 | 6 | 5 |
| F-9_A | 27.282 | 911,1 | 419.706 | 13 | 31 | 1 | 1 |

Catatan penting: bins sudah dipadatkan (menit kosong dibuang), karena itu setiap bin yang tersisa berisi data dan gap hanya terlihat sebagai lompatan waktu. Jumlah gap di tabel ini adalah jumlah lompatan, bukan jumlah menit hilang.

## 3. Data untuk Markov/HMM: state diskret dan transisi

State diskret yang tersedia tanpa dibuat-buat: `STUCK_RT` (bins `stuck_max`), `SHKRSK_RT` (bins `shk_max`), `VIBLAT_RT` dengan ambang 32,17405 ft/s2 (bins `vib_max`), dan `CRPM_RT` (ketersediaan, bukan state biner). Label regime untuk data rig TIDAK ADA. Label regime hanya ada di data bengkel (tool_wear), yaitu kolom `run` dan `y` pada 469 jendela.

| Well | State | Menit di state | Episode | Edge 0 ke 1 | Total perubahan state | Median episode (mnt) | Episode terpanjang (mnt) |
|---|---|---|---|---|---|---|---|
| F-10 | STUCK | 2.132 | 160 | 160 | 320 | 1,0 | 4,3 |
| F-10 | SHKRSK | 30 | 23 | 23 | 46 | 1,0 | 1,0 |
| F-10 | VIBLAT | 0 | 0 | 0 | 0 | NA | NA |
| F-12 | STUCK | tidak ada kanal | NA | NA | NA | NA | NA |
| F-12 | SHKRSK | 202 | 166 | 166 | 332 | 1,0 | 1,1 |
| F-12 | VIBLAT | tidak ada kanal | NA | NA | NA | NA | NA |
| F-14 | STUCK | 339 | 87 | 87 | 174 | 1,0 | 1,9 |
| F-14 | SHKRSK | 160 | 122 | 122 | 244 | 1,0 | 1,1 |
| F-14 | VIBLAT | 712 | 200 | 200 | 400 | 1,0 | 2,0 |
| F-15A | STUCK | tidak ada kanal | NA | NA | NA | NA | NA |
| F-15A | SHKRSK | 10 | 10 | 10 | 20 | 1,0 | 1,0 |
| F-15A | VIBLAT | 1.096 | 553 | 553 | 1.106 | 1,0 | 2,8 |
| F-15_S | STUCK | tidak ada kanal | NA | NA | NA | NA | NA |
| F-15_S | SHKRSK | 46 | 31 | 31 | 62 | 1,0 | 1,0 |
| F-15_S | VIBLAT | 1.083 | 297 | 297 | 594 | 1,0 | 1,9 |
| F-5 | STUCK | tidak ada kanal | NA | NA | NA | NA | NA |
| F-5 | SHKRSK | 40 | 37 | 37 | 74 | 1,0 | 1,0 |
| F-5 | VIBLAT | 1.009 | 152 | 152 | 304 | 1,0 | 6,5 |
| F-7 | STUCK | tidak ada kanal | NA | NA | NA | NA | NA |
| F-7 | SHKRSK | 174 | 80 | 80 | 160 | 1,0 | 1,1 |
| F-7 | VIBLAT | tidak ada kanal | NA | NA | NA | NA | NA |
| F-9 | STUCK | 135 | 61 | 61 | 122 | 1,0 | 1,4 |
| F-9 | SHKRSK | 16 | 10 | 10 | 20 | 1,0 | 1,1 |
| F-9 | VIBLAT | 989 | 36 | 36 | 72 | 1,1 | 7,6 |
| F-9_A | STUCK | 1.235 | 110 | 110 | 220 | 1,0 | 2,2 |
| F-9_A | SHKRSK | 6 | 4 | 4 | 8 | 1,0 | 1,0 |
| F-9_A | VIBLAT | tidak ada kanal | NA | NA | NA | NA | NA |

Kesimpulan yang bisa dibuktikan: rantai Markov dan HMM bisa dibangun pada 4 well untuk STUCK (F-9, F-9_A, F-10, F-14), 9 well untuk SHKRSK, dan 7 well untuk VIBLAT. Well tanpa kanal STUCK (F-5, F-7, F-12, F-15A, F-15_S) tidak punya state itu sama sekali, jadi Markov lintas well untuk STUCK hanya mungkin pada 4 well tersebut.

## 4. Data untuk survival: kejadian onset, censoring, horizon

Kejadian onset yang terukur dari file hasil pipeline, bukan dari ingatan:

| Kelas | Well | Onset (ffill) | Onset (strict) | Onset skorable | Positif | Baris eligible | Sumber |
|---|---|---|---|---|---|---|---|
| stuck K-ii | F-9 | 55 | 61 | 55 | 311 | 16.184 | `scratch/v9_d1/v9_d1_04_qc.json` |
| stuck K-ii | F-9_A | 72 | 72 | 72 | 503 | 2.242 | `scratch/v9_d1/v9_d1_04_qc.json` |
| stuck K-ii | F-10 | 93 | 111 | 93 | 772 | 4.216 | `scratch/v9_d1/v9_d1_04_qc.json` |
| stuck K-ii | F-14 | 61 | 81 | 61 | 389 | 95.925 | `scratch/v9_d1/v9_d1_04_qc.json` |

| Kelas | Well | Episode | Positif (test) | Prevalensi test | Horizon | Sumber |
|---|---|---|---|---|---|---|
| hyd K-ii | F-9 A | 124 | 30 | 0,370% | 10 menit | `scratch/v9_e_rule/v9_e_RULE_04_hyd_k2_results.json` |

Censoring dan horizon: (a) horizon yang benar-benar tersedia di semua dataset rig adalah 10 menit ke depan, tidak ada dataset horizon jam atau hari; (b) well yang tidak menghasilkan onset sama sekali berlaku sebagai observasi tersensor, contohnya F-7 pada ssi hanya punya 1 segmen positif dan 185 menit baseline bersih, sedangkan F-9 A untuk hyd K-ii hanya 1 wellbore; (c) jumlah kejadian per kelas kecil di beberapa well (shk F-9_A 4 episode, shk F-9 10 episode), sehingga model survival dengan kovariat banyak akan kekurangan event.

## 5. Data untuk anomali tanpa label

Kanal yang bisa dipakai tanpa label (tersedia di bins, bukan turunan label): TQA, SPPA, TFLO, RPM, SWOB, HKLD, ROP, BPOS, SPM, depth, dbtm. Angka di bawah adalah fraksi bin 1 menit yang nilainya tidak NaN, jadi nilai rendah berarti menit tersebut bukan menit operasi (bukan berarti sensor rusak), dan nilai itu harus dibaca sebagai pangsa menit yang bisa dipakai model tanpa label:

| Well | TQA | SPPA | TFLO | RPM | SWOB | HKLD | ROP | BPOS | SPM | depth | dbtm |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-10 | 33,2% | 33,2% | 33,1% | 33,3% | 33,3% | 33,3% | 29,3% | 33,3% | NA | 33,3% | 33,3% |
| F-12 | 13,2% | 11,6% | 13,2% | 13,2% | 13,2% | 13,2% | 10,7% | 12,7% | NA | 49,3% | 49,3% |
| F-14 | 13,1% | 13,1% | 13,1% | 13,1% | 13,1% | 13,1% | 12,9% | 13,1% | NA | 44,6% | 44,6% |
| F-15A | 26,7% | 26,7% | 26,7% | 26,7% | 26,7% | 26,7% | 26,6% | 26,7% | NA | 26,7% | 26,7% |
| F-15_S | 13,3% | 13,3% | 10,4% | 13,3% | 13,3% | 13,3% | 13,2% | 13,3% | NA | 31,4% | 31,4% |
| F-5 | 15,0% | 15,1% | 15,1% | 15,1% | 15,1% | 15,1% | 15,1% | 15,1% | NA | 19,3% | 19,3% |
| F-7 | 10,6% | 10,6% | 10,6% | 10,6% | 10,6% | 10,6% | 10,6% | 10,6% | NA | 28,9% | 28,9% |
| F-9 | 8,6% | 8,6% | 8,6% | 8,6% | 8,6% | 8,6% | 8,6% | 8,6% | NA | 55,1% | 55,1% |
| F-9_A | 9,3% | 9,3% | 9,3% | 9,3% | 9,3% | 9,3% | 8,4% | 9,3% | NA | 9,3% | 9,3% |

Panjang baseline bersih per well dan per engine (menit terpanjang tanpa label positif berurutan, dihitung pada grid 1 menit dengan pemutus gap):

| Engine | Well | Baris | Positif | Baseline bersih terpanjang (mnt) | Segmen positif |
|---|---|---|---|---|---|
| `vib` | F-14 | 1.989 | 1.124 | 372 | 34 |
| `vib` | F-15A | 6.482 | 1.543 | 886 | 71 |
| `vib` | F-15_S | 10.903 | 1.532 | 2.523 | 70 |
| `vib` | F-5 | 4.548 | 1.230 | 548 | 41 |
| `ssi` | F-10 | 7.133 | 161 | 1.549 | 28 |
| `ssi` | F-12 | 4.293 | 83 | 305 | 22 |
| `ssi` | F-14 | 5.455 | 75 | 1.359 | 13 |
| `ssi` | F-15A | 6.020 | 31 | 2.808 | 7 |
| `ssi` | F-15_S | 5.342 | 85 | 681 | 27 |
| `ssi` | F-5 | 4.714 | 102 | 676 | 19 |
| `ssi` | F-7 | 982 | 3 | 185 | 1 |
| `ssi` | F-9 | 1.126 | 12 | 354 | 3 |
| `ssi` | F-9_A | 841 | 55 | 168 | 12 |
| `shk` | F-10 | 7.899 | 146 | 1.718 | 15 |
| `shk` | F-12 | 5.405 | 217 | 696 | 20 |
| `shk` | F-14 | 11.205 | 760 | 1.376 | 62 |
| `shk` | F-15A | 6.484 | 41 | 1.800 | 6 |
| `shk` | F-15_S | 11.394 | 259 | 2.979 | 25 |
| `shk` | F-5 | 7.140 | 240 | 638 | 30 |
| `shk` | F-7 | 2.761 | 267 | 448 | 14 |
| `shk` | F-9 | 1.851 | 45 | 486 | 6 |
| `shk` | F-9_A | 2.356 | 30 | 1.375 | 3 |
| `stuck_k1` | F-14 | 3.201 | 432 | 573 | 20 |
| `stuck_k1` | F-9_A | 2.354 | 1.575 | 74 | 41 |
| `stuck_k2` | F-10 | 4.216 | 772 | 734 | 67 |
| `stuck_k2` | F-14 | 95.925 | 389 | 28.820 | 28 |
| `stuck_k2` | F-9 | 16.184 | 311 | 7.248 | 16 |
| `stuck_k2` | F-9_A | 2.242 | 503 | 300 | 37 |
| `hyd_ki` | F-10 | 7.571 | 1.394 | 1.329 | 23 |
| `hyd_ki` | F-12 | 7.390 | 1.426 | 393 | 92 |
| `hyd_ki` | F-14 | 10.401 | 865 | 1.063 | 58 |
| `hyd_ki` | F-15A | 6.156 | 698 | 1.902 | 33 |
| `hyd_ki` | F-15_S | 8.355 | 993 | 1.027 | 64 |
| `hyd_ki` | F-5 | 6.332 | 621 | 707 | 40 |
| `hyd_ki` | F-7 | 2.482 | 421 | 229 | 28 |
| `hyd_ki` | F-9 | 1.616 | 423 | 324 | 28 |
| `hyd_ki` | F-9_A | 2.206 | 331 | 816 | 24 |

Baseline bersih gabungan tiga state (menit tanpa STUCK, SHKRSK, dan VIBLAT sekaligus):

| Well | Baseline bersih terpanjang (mnt) | Fraksi menit bersih |
|---|---|---|
| F-10 | 9.730 | 94,8% |
| F-12 | 77.604 | 99,9% |
| F-14 | 27.062 | 98,8% |
| F-15A | 11.271 | 97,5% |
| F-15_S | 39.488 | 98,9% |
| F-5 | 27.679 | 98,5% |
| F-7 | 11.632 | 99,5% |
| F-9 | 8.991 | 96,1% |
| F-9_A | 12.014 | 95,5% |

Konsekuensi yang bisa dibuktikan: baseline bersih sangat tidak seimbang antar well (terpendek 8.991 menit di F-9, terpanjang 77.604 menit di F-12). Model anomali tanpa label harus dilatih dan dikalibrasi per well, bukan dengan satu ambang global.

## 6. Dataset eksternal

### 6.1 USROP (bit_wear K-1)

| Butir | Nilai |
|---|---|
| Berkas | `data/USROP_labeled.csv` |
| Baris | 198.928 |
| Kolom | 18 |
| Well | 7 |
| Label `normal` | 134.013 |
| Label `high_MSE_bit_wear` | 49.732 |
| Label `low_ROP_efficiency` | 15.183 |
| Prevalensi high_MSE | 25,0% |

| Well | Baris | high_MSE |
|---|---|---|
| USROP_A 0 N-NA_F-9_Ad.csv | 13.746 | 182 |
| USROP_A 1 N-S_F-7d.csv | 6.389 | 0 |
| USROP_A 2 N-SH_F-14d.csv | 47.645 | 4.918 |
| USROP_A 3 N-SH-F-15d.csv | 53.041 | 7.622 |
| USROP_A 4 N-SH_F-15Sd.csv | 51.708 | 28.051 |
| USROP_A 5 N-SH-F-5d.csv | 18.548 | 8.959 |
| USROP_A 6 N-SH_F-9d.csv | 7.851 | 0 |

Catatan pembatas: 2 dari 7 well tidak punya satu baris pun berlabel `high_MSE_bit_wear` (USROP_A 1 N-S_F-7d.csv, USROP_A 6 N-SH_F-9d.csv). Validasi antar well untuk bit_wear K-1 karena itu hanya bisa memakai 5 well, dan satu kelas label `low_ROP_efficiency` (15.183 baris) belum pernah dipakai sebagai target di V9.

### 6.2 Mendeley tool wear (tool_wear)

| Butir | Nilai |
|---|---|
| Berkas | `scratch/v6_e1/toolwear_windows.csv` |
| Baris (jendela) | 469 |
| Fitur | 27 (mean, std, rms, kurt, skew, p2p, crest, zcr, fdom untuk sumbu X, Y, Z) |
| Alat | 4 (T01, T02, T03, T04) |
| Label y | 1: 240, 0: 229 |
| Jendela per alat | T01: 120, T02: 112, T03: 121, T04: 116 |
| Jumlah run kondisi | 2 |

Jumlah 469 jendela dan 27 fitur pada kartu ini TERBUKTI cocok dengan isi berkas. Pembatas penting: label `y` hanya dibedakan oleh 2 kondisi run dalam satu alat, sehingga identitas alat tidak bisa dipakai sebagai sumber variasi label. Uji lintas alat harus tetap memakai protokol leave-one-tool-out.

### 6.3 Volve pit dan GAINLOSSTOT

| Butir | Status | Bukti |
|---|---|---|
| Kanal `GAINLOSSTOT` | TIDAK ADA | Tidak muncul di daftar kanal 9 well terparse (`data/volve/witsml_parsed/*.qc.json`, 9 well diperiksa) |
| Kanal menyerupai pit/gain/loss | SEBAGIAN | F-15_S.qc.json: GAIN_CLNK |
| Data pit volume (13 kolom `MudPit Volume Average`) | ADA, satu well | `data/witsml/Norway-NA-15_47_9-F-9 A time.csv`, 419.748 baris termasuk header, 13 kolom pit |
| Sudah diparse jadi dataset siap pakai | BELUM | Label hyd K-ii pada run V9 memakai berkas cache `f9a_time.csv` yang sudah tidak ada di `~/.hermes/cache/scratch`; yang tersisa adalah CSV mentah F-9 A di atas |

## 7. Tabel akhir: algoritma, kebutuhan data, status

Status: ADA = data terukur cukup untuk dijalankan; SEBAGIAN = ada tetapi terbatas (well sedikit, kanal jarang, atau horizon pendek); TIDAK ADA = tidak ada data yang diperlukan.

| Algoritma | Kebutuhan data | Status | Catatan (angka pembatas) |
|---|---|---|---|
| Markov chain (state transisi) | state diskret biner per menit | ADA (SEBAGIAN untuk STUCK) | STUCK hanya 4 well (F-9, F-9_A, F-10, F-14); SHKRSK 9 well; VIBLAT 7 well; episode STUCK F-10 160, F-9_A 110, F-14 87, F-9 61 |
| HMM (state tersembunyi) | urutan state kategorik + observasi kontinu | ADA (SEBAGIAN) | butuh urutan panjang tanpa gap besar; gap > 60 dtk pada SHKRSK F-12 9.591, F-14 5.408, F-15_S 5.176 |
| Cox / survival regresi | waktu ke onset + censoring + kovariat | SEBAGIAN | event onset 55 sampai 93 per well untuk stuck; hyd K-ii 124 episode di 1 wellbore; horizon hanya 10 menit |
| Random Survival Forest / DeepHit | event lebih banyak + horizon berlapis | SEBAGIAN | well ber-event sedikit (shk F-9_A 4 episode, F-9 10 episode) sehingga model kovariat banyak rawan underpowered |
| VMD / EMD / wavelet | sinyal kontinu laju tinggi (minimal orde Hz) | TIDAK ADA | laju sampel tertinggi 0,3333 Hz, VIBLAT F-14 0,0167 Hz; Nyquist 0,1667 Hz |
| Metaheuristik kontinu (GWO, WOA, PSO, SSA, HHO, EPO, SMA, EO, HBO) | fungsi objektif + data latih/validasi | ADA | tidak butuh sinyal mentah; batas bukan data melainkan jumlah fold validasi (vib 4, stuck_k1 2) |
| Boosting + kalibrasi (LightGBM, XGBoost, CatBoost, isotonic, conformal) | fitur + label + fold antar well | ADA | jendela 23.922 sampai 118.567; well 2 sampai 9; prevalensi 1,67% sampai 36,13% |
| Drift / CUSUM / Page-Hinkley / BOCPD / ADWIN | deret waktu kontinu satu kanal | ADA | kanal TQA kontinu panjang (F-14 163.117 sampel berurutan, F-15_S 160.156) |
| Anomali tanpa label (Isolation Forest, LOF, autoencoder, one-class SVM) | kanal fisik tanpa label + baseline bersih | ADA (SEBAGIAN) | baseline bersih gabungan 8.991 sampai 77.604 menit; tetapi ssi F-9_A hanya 168 menit dan F-7 185 menit |
| Matrix profile | deret waktu kontinu dengan cadangan panjang | SEBAGIAN | butuh deret rapat; SHKRSK F-12 median dt 59,961 dtk dan 9.591 gap > 60 dtk |

## 8. Rujukan ilmiah (status verifikasi)

| Penulis pertama | Tahun | Judul | DOI/URL | Status verifikasi |
|---|---|---|---|---|
| Dragomiretskiy, K. | 2014 | Variational Mode Decomposition, IEEE Trans. Signal Process. 62(3):531-544 | https://doi.org/10.1109/TSP.2013.2288675 | TERVERIFIKASI (halaman doi.org terbuka, judul cocok) |
| Huang, N. E. | 1998 | The empirical mode decomposition and the Hilbert spectrum for nonlinear and non-stationary time series analysis, Proc. R. Soc. A 454(1971):903-995 | https://doi.org/10.1098/rspa.1998.0193 | TERVERIFIKASI lewat Crossref API (judul, volume, halaman cocok); halaman penerbit menolak bot |
| Rabiner, L. R. | 1989 | A tutorial on hidden Markov models and selected applications in speech recognition, Proc. IEEE 77(2):257-286 | https://doi.org/10.1109/5.18626 | TERVERIFIKASI (halaman doi.org terbuka, judul cocok, Crossref cocok) |
| Cox, D. R. | 1972 | Regression Models and Life-Tables, J. R. Stat. Soc. B 34(2):187-202 | https://doi.org/10.1111/j.2517-6161.1972.tb00899.x | TERVERIFIKASI lewat Crossref API (abstrak censored failure times cocok); halaman penerbit menolak bot |
| Ishwaran, H. | 2008 | Random survival forests, Ann. Appl. Stat. 2(3):841-860 | https://doi.org/10.1214/08-AOAS169 | TERVERIFIKASI (halaman doi.org terbuka, judul cocok, Crossref cocok) |
| Liu, F. T. | 2008 | Isolation Forest, Proc. IEEE ICDM, 413-422 | https://doi.org/10.1109/ICDM.2008.17 | TERVERIFIKASI (halaman doi.org terbuka, judul cocok, Crossref cocok) |
| Page, E. S. | 1954 | Continuous Inspection Schemes, Biometrika 41(1-2):100-115 | https://doi.org/10.1093/biomet/41.1-2.100 | TERVERIFIKASI lewat Semantic Scholar API (judul dan tahun cocok); halaman penerbit menolak bot |
| Mirjalili, S. | 2014 | Grey Wolf Optimizer, Advances in Engineering Software 69:46-61 | https://doi.org/10.1016/j.advengsoft.2013.12.007 | TERVERIFIKASI lewat Semantic Scholar API (judul, tahun, jurnal cocok); resolve doi.org gagal di alat ini |

Rujukan di atas dipakai hanya untuk menyatakan bahwa algoritma yang diminta memang punya dasar ilmiah. Tidak ada rekomendasi di dokumen ini yang bersandar pada rujukan berstatus BELUM TERVERIFIKASI, karena tidak ada rujukan yang dipakai dalam keadaan itu.

## 9. Ringkasan 5 baris

1. Data jendela 1 menit terbukti ada untuk 6 dataset engine dengan 2 sampai 9 well dan prevalensi 1,67% sampai 36,13%; dataset dengan cakupan well paling lemah adalah stuck_k1 (2 well, 5.555 jendela) dan vib (4 well, 23.922 jendela).
2. VMD, EMD, dan wavelet TIDAK LAYAK pada data rig ini karena laju sampel tertinggi 0,3333 Hz (Nyquist 0,1667 Hz) dan VIBLAT_RT di F-14 hanya 0,0167 Hz; dekomposisi frekuensi pada pita itu tidak mewakili getaran lateral maupun stick-slip.
3. Markov dan HMM layak secara data tetapi terkunci pada state yang tersedia: STUCK 4 well, SHKRSK 9 well, VIBLAT 7 well, dan label regime hanya ada di data bengkel (469 jendela, 4 alat).
4. Survival hanya punya horizon 10 menit dengan event 55 sampai 93 per well untuk stuck dan 124 episode hyd K-ii di satu wellbore; model survival multi-kovariat akan rawan underpowered, bukan mustahil.
5. Dataset eksternal siap pakai: USROP 198.928 baris dengan 49.732 baris high_MSE, tool wear 469 jendela dan 27 fitur; sedangkan GAINLOSSTOT TIDAK ADA dan data pit hanya tersedia untuk satu well (F-9 A, 13 kolom, 419.748 baris) dan belum siap pakai.

## 10. Yang belum terverifikasi

- Kelayakan statistik metaheuristik, boosting, dan survival TIDAK diukur di kartu ini, karena butuh run pilot, bukan pengukuran data.
- Horizon survival lebih panjang dari 10 menit belum pernah dibuat, jadi ketersediaannya BELUM TERUKUR.
- `GAINLOSSTOT` tidak ditemukan sebagai nama kanal di 9 well terparse; kemungkinan ada di sumber luar WITSML (laporan harian), dan itu BELUM TERUKUR karena `data/volve/ddr.parquet` gagal dibaca di lingkungan ini (pyarrow tidak terpasang).
- Label hyd K-ii berasal dari berkas cache `f9a_time.csv` yang sudah tidak ada; reproduksi penuh butuh langkah parse ulang dari `data/witsml/Norway-NA-15_47_9-F-9 A time.csv`, dan langkah itu belum dijalankan di kartu ini.
- Kanal VIBLAT_RT tidak ada di F-7, F-9_A, dan F-12; kanal STUCK_RT tidak ada di F-5, F-7, F-12, F-15A, dan F-15_S. Apakah kanal tersebut benar-benar tidak direkam atau hanya tidak terparse BELUM TERUKUR.

