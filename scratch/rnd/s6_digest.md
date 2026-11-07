# DIGEST S6
Dibuat otomatis dari dokumen asli. Angka di bawah ini dikutip apa adanya dari berkas, bukan dari ingatan.

## S1 (docs/RND_S1_SEED_ROBUSTNESS.md)
Judul bagian: 1. Lingkup dan kebijakan pengikat / 2. Metode: harness bersama code/rnd_hybrid_harness.py / 3. Data dan pemeriksaan awal / 4. Reproduksi angka terbit R8 pada seed 42 / 5. Lintas seed H1 dan kontrol stokastik / 6. Nilai lapisan A/B/C pada H1 (berlaku untuk kelima seed karena hasilnya identik) / 7. Banding dengan konfigurasi engine pra-riset (V9) / 8. Batas pemakaian, yang belum terukur, dan penutup
| Detektor | seri_z, gerbang_rule, cusum_alarm, jendela_alarm, pilih_h, detektor_stat_rule | rule kanal kausal bin t-1, CUSUM dua sisi dengan reset, zona peringatan 10 menit, ambang h dari well kalibrasi |
| ML (S2/S3 dan kontrol S1) | fitur_dari, latih_lgb, threshold_conformal, skor_ml_fold | kolom bocor dibuang dengan assert, ambang conformal kuantil (1-alpha) skor negatif kalibrasi |
| F-10 | 7571 | 1394 | 11249 | 0,673 |
| F-12 | 7390 | 1426 | 86454 | 0,0855 |
| F-14 | 10401 | 865 | 317679 | 0,0327 |
| F-15A | 6156 | 698 | 32141 | 0,1915 |
| F-15_S | 8355 | 993 | 92488 | 0,0903 |
| F-5 | 6332 | 621 | 369549 | 0,0171 |
| F-7 | 2482 | 421 | 23011 | 0,1079 |
| F-9 | 1616 | 423 | 22858 | 0,0707 |
| F-9_A | 2206 | 331 | 7344 | 0,3004 |
| Metrik | Terbit R8 | Replikasi S1 | Selisih | Lulus |
| FP total | 935 | 935 | 0 | ya |
| TP total | 3804 | 3804 | 0 | ya |

## S2 (docs/RND_S2_HYBRID_VIB_SSI.md)
Judul bagian: 0. CARA MEMBACA DOKUMEN INI / 1. PERTANYAAN, KEBIJAKAN, DAN KEPUTUSAN DESAIN / 2. DATA DAN KELAYAKAN UJI / 3. BENTUK HYBRID YANG DIUJI / 4. LAPISAN A: APAKAH DETEKSI BEKERJA / 5. PERBANDINGAN HYBRID LAWAN SINGLE ENGINE TERBAIK / 6. LAPISAN C: KETEPATAN DAN KETAHANAN / 7. LAPISAN B: NILAI MAINTENANCE, BELUM TERUKUR / 8. KEPUTUSAN DAN BATAS PENGGUNAAN / 9. PROVENANCE DAN REPRODUKSI / 10. RINGKASAN LIMA BARIS / 11. YANG BELUM TERVERIFIKASI
| vib | 23.922 | 4 | 55 | 4 | 4 | 0 | 5.429 |
| ssi | 35.906 | 9 | 55 | 9 | 7 | 2 | 592 |
| F-14 | 1.989 | 1.124 | 3.018 | HKLD | 0,6757 | 30,0 | 0,8481 | 0,8274 | ya |
| F-15A | 6.482 | 1.543 | 32.141 | HKLD | 0,6419 | 30,0 | 0,5452 | 0,8078 | ya |
| F-15_S | 10.903 | 1.532 | 92.501 | HKLD | 0,6760 | 30,0 | 0,4806 | 0,7919 | ya |
| F-5 | 4.548 | 1.230 | 20.961 | depth | 0,6290 | 30,0 | 0,6073 | 0,8680 | ya |
| F-10 | 7.133 | 161 | 11.247 | TQA | 0,5319 | 30,0 | 0,0306 | 0,5387 | ya |
| F-12 | 4.293 | 83 | 85.643 | spm | 0,5778 | 15,0 | 0,0354 | 0,6498 | ya |
| F-14 | 5.455 | 75 | 275.834 | TFLO | 0,5818 | 30,0 | 0,0245 | 0,6663 | ya |
| F-15A | 6.020 | 31 | 32.133 | spm | 0,5647 | 15,0 | 0,0381 | 0,8722 | ya |
| F-15_S | 5.342 | 85 | 81.764 | TFLO | 0,5902 | 30,0 | 0,1848 | 0,8673 | ya |
| F-5 | 4.714 | 102 | 322.772 | spm | 0,5824 | 15,0 | 0,0893 | 0,6146 | ya |
| F-7 | 982 | 3 | 12.837 | spm | 0,5743 | 15,0 | 0,0340 | 0,9067 | tidak |
| F-9 | 1.126 | 12 | 2.287 | spm | 0,5716 | 15,0 | 0,0229 | 0,6896 | tidak |

## S3 (docs/RND_S3_HYBRID_BITWEAR.md)
Judul bagian: 0. Riset pendahuluan / 1. Cara reproduksi / 2. Kelayakan: hitungan yang menentukan boleh atau tidaknya uji hybrid / 3. Uji hybrid yang dijalankan / 4. Lapisan A: apakah deteksi bekerja / 5. Lapisan C: ketepatan dan ketahanan / 6. Lapisan B: belum terukur, dan buktinya / 7. Baseline regime bengkel dan perbandingan yang sah / 8. Vonis untuk kartu ini / 9. Ringkasan lima baris / 10. Yang belum terverifikasi
| `scratch/rnd/s3/s3a_feasibility.py` | `data/USROP_labeled.csv`, `data/volve/usrop_timestamped.csv` | `s3a_feasibility.json` |
| `scratch/rnd/s3/s3b_hybrid.py` | keduanya + `code/rnd_hybrid_harness.py` | `s3b_hybrid.json` |
| `scratch/rnd/s3/s3c_summary.py` | `s3a`, `s3b`, `scratch/v9_i1/v9_i1_RESULTS.json` | `s3c_ringkas.json` |
| `scratch/rnd/s3/s3d_dokumen.py` | `s3c_ringkas.json`, `s3b_hybrid.json` | dokumen ini + blok ledger S3 |
| `USROP_A 3 N-SH-F-15d.csv` | 53.041 | 7.622 | 5.278 | 40.141 | 14,37% |
| `USROP_A 4 N-SH_F-15Sd.csv` | 51.708 | 28.051 | 1.026 | 22.631 | 54,25% |
| `USROP_A 2 N-SH_F-14d.csv` | 47.645 | 4.918 | 8.053 | 34.674 | 10,32% |
| `USROP_A 5 N-SH-F-5d.csv` | 18.548 | 8.959 | 112 | 9.477 | 48,30% |
| `USROP_A 0 N-NA_F-9_Ad.csv` | 13.746 | 182 | 714 | 12.850 | 1,32% |
| `USROP_A 6 N-SH_F-9d.csv` | 7.851 | 0 | 0 | 7.851 | 0,00% |
| `USROP_A 1 N-S_F-7d.csv` | 6.389 | 0 | 0 | 6.389 | 0,00% |
| `USROP_A 0 N-NA_F-9_Ad.csv` | 13.746 | 0,042 | 0,003 | 35,010 | 714,966 |
| `USROP_A 1 N-S_F-7d.csv` | 6.389 | 0,051 | 0,003 | 7,041 | 332,305 |
| `USROP_A 2 N-SH_F-14d.csv` | 47.643 | 0,037 | 0,003 | 94,900 | 2.478,085 |

## S4 (docs/RND_S4_LAYER_B_DATA.md)
Judul bagian: 1. CARA SAPUAN DILAKUKAN / 2. KANDIDAT YANG DITEMUKAN (path absolut, ukuran, jumlah record, kolom relevan) / 3. TIGA KELOMPOK / 4. METRIK LAPISAN B YANG BENAR-BENAR DAPAT DIHITUNG / 5. UJI SILANG DUA JALUR JAM HENTI / 6. YANG HARUS DIKUMPULKAN, DAN DARI SIAPA / 7. NILAI TIGA LAPISAN SETELAH KARTU INI / 8. RINGKASAN LIMA BARIS / 9. BELUM TERVERIFIKASI
| 1 | `/mnt/d/Capstone 1(v2)/data/volve/ddr.parquet` | 2.180.278 byte | 1.759 laporan, 17 kolom, 23.447 record `activity` (`S4-001`, `S4-003`, `S4-004`) | `activity.dTimStart`, `activity.dTimEnd`, `activity.proprietaryCode`, `activity.state`, `activity.stateDetailActivity`, `activity.comments` |
| 2 | `/mnt/d/Capstone 1(v2)/data/volve/labels_curated_v2.csv` | 519.171 byte | 884 record, 20 kolom (`S4-013`) | `act_start`, `act_end`, `category`, `state_detail`, `source_code`, `outcome`, `component` |
| 3 | `/mnt/d/Capstone 1(v2)/data/volve/external/dbx_volume/Well_technical_data/Daily Drilling Report - HTML Version/*.html` | 1.759 berkas, 30.971.159 byte | 325 berkas memuat tabel `equipmentfailureInfoTable`, 533 record (`S4-020`, `S4-021`) | Start time, Depth mMD, Depth mTVD, Sub Equip - Syst Class, Operation Downtime (min), Equipment Repaired, Remark |
| 4 | `/mnt/d/Capstone 1(v2)/data/volve/external/dbx_volume/Well_technical_data/Daily Drilling Report - XML Version/*.xml` | 1.759 berkas, 21.315.879 byte | 1.759 dokumen | struktur WITSML drillReport: `activity`, `statusInfo`, `fluid`, `lithShowInfo` (tanpa elemen biaya) |
| 5 | `/mnt/d/Capstone 1(v2)/data/volve/external/dbx_volume/Well_technical_data/Daily Drilling report - PDF Version/*.pdf` | 1.759 berkas, 56.814.977 byte | 1.759 dokumen | tidak dipindai teks pada kartu ini |
| 6 | `/mnt/d/Capstone 1(v2)/data/volve/external/volve_catalog_target_paths.csv` | 645.763 byte | 4.035 record data, 4.036 baris teks termasuk header (`S4-029`) | `category`, `well`, `ext`, `path` |
| 7 | `/mnt/d/Capstone 1(v2)/data/predictive/features_timeseries_events.csv` | 85.613 byte | 661 record, 17 kolom | `event_id`, `fold`, `wellbore`, `act_start`, jendela `w30m/w2h/w6h` |
| 8 | `/mnt/d/Capstone 1(v2)/data/USROP_health.csv` | 56.815.359 byte | 198.928 record, 20 kolom | `health_index`, `maintenance_recommendation` (turunan sendiri, `code/06_xgb_fuzzy.py:90`, bukan catatan maintenance nyata) |
| 9 | `/mnt/d/Capstone 1(v2)/data/volve/usrop_wellbores_events.csv` | 218.119 byte | 884 record, 8 kolom | `wellbore`, `ddr_date_start`, `act_start`, `act_end`, `code`, `state_detail`, `comments` |
| 10 | `/mnt/d/Capstone 1(v2)/data/volve/witsml_parsed/*.csv` | 10 berkas, 4.606.027.369 byte total | kanal realtime per sumur | tidak memuat kolom maintenance, biaya, atau inspeksi |
| Kode | Record | Jam | Median jam | p90 jam | Maks jam |
| interruption -- other | 1.202 | 2.680,917 | 1,0 | 5,5 | 24,0 |
| interruption -- waiting on weather | 445 | 1.925,5 | 2,5 | 10,9 | 24,0 |
| interruption -- repair | 806 | 1.215,0 | 1,0 | 3,5 | 12,5 |

## S5 (docs/RND_S5_AUDIT_WAVE2.md)
Judul bagian: 1. Lingkup, bahan, dan definisi vonis / 2. Rerun dua seed dari S1 dengan harness / 3. Artefak JSON dan klaim bernama / 4. Baris ledger per kartu / 5. DOI dan rujukan luar / 6. Pemisahan lapisan A, B, C dan daftar belum terverifikasi / 7. Tabel cacat / 8. Yang belum terverifikasi pada audit ini / 9. Ringkasan lima baris
| S1 | `docs/RND_S1_SEED_ROBUSTNESS.md` | 279 | 25445 | 4 | 84 |
| S2 | `docs/RND_S2_HYBRID_VIB_SSI.md` | 311 | 24464 | 6 | 455 |
| S3 | `docs/RND_S3_HYBRID_BITWEAR.md` | 218 | 21573 | 3 | 92 |
| S4 | `docs/RND_S4_LAYER_B_DATA.md` | 207 | 23162 | 8 | 95 |
| Metrik | Dokumen S1 | Rerun seed 42 | Rerun seed 13 | Selisih |
| FP total | 935 | 935 | 935 | 0 |
| TP total | 3804 | 3804 | 3804 | 0 |
| Presisi median | 0,7789 | 0,7789 | 0,7789 | 0 |
| Recall median | 0,5638 | 0,5638 | 0,5638 | 0 |
| FAR24 kalender median | 3,5302 | 3,5302 | 3,5302 | 0 |
| FAR24 baris median | 32,256 | 32,256 | 32,256 | 0 |
| Lead median | 11,5 | 11,5 | 11,5 | 0 |
| Diperingatkan | 219 | 219 | 219 | 0 |
| Fold FAR tidak lebih dari 6 | 7 | 7 | 7 | 0 |

## PM (docs/RND_PM_VERDICT.md)
Judul bagian: 0. CARA MEMBACA VONIS INI / 1. BUKTI YANG DIPAKAI DAN BUKTI YANG TIDAK DIPAKAI / 2. VONIS PER KELUARGA ALGORITMA / 3. VONIS PER KELAS DAN PER TUGAS (KOMPOSISI FINAL) / 4. YANG DIADOPSI: PERUBAHAN KONKRET PADA ENGINE DAN DAMPAK TIER / 5. YANG DIPILOT: ENGINE SASARAN, KLAIM, GATE, DAN RISIKO KEGAGALAN / 6. YANG DITOLAK DAN SYARAT MEMBUKANYA / 7. ROADMAP TIGA GELOMBANG / 8. YANG BELUM TERUKUR DAN TIDAK BOLEH DIKLAIM / 9. RUJUKAN DAN STATUS VERIFIKASI / 10. PROVENANCE / 11. RINGKASAN LIMA BARIS
| `scratch/rnd/r8/*.json` | empat uji hybrid dengan baseline per tugas, seed 42 | RUN-KITA, ter-assert (PM-001 sampai PM-056) |
| `scratch/rnd/e4/*.json` | baseline jujur dari bins, dekomposisi gate, jumlah fitur | RUN-KITA, ter-assert (PM-057 sampai PM-066) |
| `scratch/rnd/e3/*.json` | kegagalan pilot conformal dan cakupan waktu per well | RUN-KITA, ter-assert (PM-067 sampai PM-075) |
| `scratch/v9_i1/v9_i1_RESULTS.json` | tier per head, jumlah head, slot alarm otomatis | RUN-KITA dan KONVENSI (PM-076 sampai PM-078) |
| `docs/RND_R1`, `R2`, `R3`, `R4`, `R5`, `E0` | penilaian keluarga algoritma dan temuan audit | kutipan baris ledger lama (PM-099 sampai PM-110) |
| `scratch/rnd/pm/pm_doi.json` | status dua lapis untuk sepuluh rujukan yang dipakai | JURNAL, ter-assert (PM-079 sampai PM-098) |
| Metaheuristik kontinu untuk tuning hyperparameter (GWO, WOA, PSO, HHO, SSA, SMA) | **TOLAK** untuk peran tuning | Tidak ada satu pun run di repo yang menunjukkan kenaikan metrik dari tuning (R1 bagian 5.2). Uji metaheuristik yang benar-benar dijalankan, yaitu GWO membungkus ML pada tool_wear, tidak menambah nilai: objektif F1 menghasilkan balanced accuracy 0,5 dengan 240 TP dan 229 FP (PM-038, PM-040, PM-041), sedangkan objektif balanced accuracy memberi 0,3993 lawan 0,3385 pada default (PM-039, PM-037) dengan tanda yang berubah antar alat. Pembatas sebenarnya adalah portabilitas ambang, bukan hyperparameter (R1 bagian 4.4) | Setiap run wajib disandingkan random search pada jumlah evaluasi identik dan baseline tanpa tuning pada fold yang sama; tanpa itu kenaikan tidak bisa diatribusikan |
| BGWO untuk seleksi fitur (T2) | **PILOT** | Belum pernah dijalankan pada data kita, jadi statusnya belum terukur, bukan gagal (PM-117). Ruang masalahnya nyata: jalur ML resmi memakai 40 fitur setelah `ts_bin` dibuang (PM-061) | Anggaran evaluasi harus muat, protokol bersarang wajib, dan fitness harus menghukum dispersi antar well; risiko utama adalah overfit seleksi pada sembilan unit |
| Dekomposisi sinyal VMD, EMD, wavelet | **TOLAK permanen** | Laju sampel tertinggi 0,3333 Hz memberi Nyquist 0,1667 Hz (PM-103, PM-104), sedangkan pita diagnostik bantalan berada pada orde ratusan Hz. Percobaan yang sudah dijalankan: 105 percobaan VMD dengan 75 gagal (PM-105, PM-106) | Tidak ada anggaran yang bisa menutup selisih dua orde laju sampel. Syarat pembuka: kanal dengan laju minimal orde Hz, yang belum ada |
| Kernel SVM | **TOLAK** sebagai pengganti rule, dicatat sebagai pembanding murah | E1 menempatkannya di shortlist dengan skor 2,25 tetapi bukan finalis karena bukan pengganti rule. Tidak ada angka kita yang menunjukkan SVM mengalahkan rule pada FAR yang sama | Boleh dijalankan hanya sebagai pembanding pada anggaran sisa, tidak boleh menjadi dasar kenaikan tier |
| kNN-DTW | **TOLAK** | Biaya 134,01 sampai 137.374,35 jam untuk satu klasifikasi penuh (PM-107) | Biaya melampaui anggaran kartu dan anggaran operasional |
| Markov chain, HMM, Bayesian network, MCMC | **TOLAK** untuk gelombang ini | Prasyarat datanya tidak ada: label state fisik tidak tersedia, dan episode sangat pendek sehingga memori praktis nol (D0 bagian 7, R2 bagian 8). MCMC dan Bayesian network ditolak karena prior dan DAG belum ada, sehingga model akan menjelaskan prior kita, bukan data | Dapat dibuka kembali bila label state fisik tersedia dan uji orde Markov dijalankan |
| Monte Carlo | **ADOPSI** sebagai kewajiban pelaporan | R2 menilainya satu-satunya metode dari delapan yang menaikkan mutu keputusan tanpa asumsi baru, dengan peran pelaporan selang, bukan deteksi (skor 5) | Biaya komputasi kecil. Wajib dipakai untuk CI FAR dan recall pada laporan engine |
| Survival: Random Survival Forest, DeepHit | **TOLAK** | Event per well kecil dan horizon hanya sepuluh menit, sehingga model kovariat banyak rawan underpowered (D0 bagian 7, R2 bagian 8) | Tidak ada syarat pembuka dalam waktu dekat karena butuh event jauh lebih banyak |

## R8 (docs/RND_R8_EVALUASI_BERLAPIS.md)
Judul bagian: 0. CARA MEMBACA DOKUMEN INI / 1. PETA KELAS KE TUGAS DAN BASELINE PER TUGAS / 2. RINGKASAN HASIL DALAM SATU TABEL / 3. METODE UJI YANG DIPAKAI / 4. H1, STATISTIK + RULE PADA hyd K-i / 5. H2, ML + STATISTIK PADA shk K-i / 6. H3, METAHEURISTIK + ML PADA tool_wear / 7. H4, TIGA KOMPONEN PADA stuck K-ii (ONSET) / 8. TABEL KEPUTUSAN / 9. KOMPOSISI ENGINE FINAL PER KELAS / 10. BATAS PENGGUNAAN DAN KEKUATAN BUKTI / 11. RUJUKAN
| H1 | statistik + rule (CUSUM memicu pemeriksaan rule kanal) | hyd K-i status | 52.509 baris, 9 well |
| H2 | ML + statistik (LightGBM dikalibrasi, gerbang residu CUSUM) | shk K-i status | 56.495 baris, 9 well |
| H3a/H3b | metaheuristik + ML (GWO memilih C dan ambang) | tool_wear K-i status | 469 jendela, 4 alat |
| H4 | tiga komponen (ML sebagai pemeringkat, rule dan statistik sebagai gerbang) | stuck K-ii onset | 118.567 baris, 4 well |
| hyd | K-i deteksi status (label qcut SPPA/TFLO) | rule kanal (anom bin t-1) dan CUSUM residu | keduanya kausal, hanya memakai bin masa lalu |
| shk | K-i deteksi status (SHKRSK pada jendela 10 menit) | rule kanal SPPA dan CUSUM residu | kelas positif langka, baseline harus bisa dibandingkan pada FAR yang sama |
| tool_wear | K-i klasifikasi status per jendela getaran | ML logistik ambang 0,5 | baseline yang dipakai engineer sebelum ada tuning |
| H1 | hyd K-i | rule: FP 2105, presisi 0,6835, FAR median 6,932, lead 6,0 menit | H1: FP 935, presisi 0,7789, FAR median 3,5302, lead 11,5 menit | alarm turun, presisi naik, peringatan lebih awal, recall turun |
| H2 | shk K-i | ML: FP 2633, TP 192, recall median 0,0829 | H2: FP 667, TP 46, recall median 0,0037 | alarm turun, tetapi deteksi hampir hilang |
| H3a | tool_wear K-i | ML default: balanced accuracy median 0,3385 | GWO objektif F1: 0,5 dengan semua jendela dinyatakan positif | tidak sah, objektif dimainkan |
| H3b | tool_wear K-i | ML default: balanced accuracy median 0,3385 | GWO objektif balanced accuracy: 0,3993 | naik di 2 alat, turun di 2 alat lain |
| H4 | stuck K-ii | ML: FP 205, TP 79, recall median 0,0322 | H4: FP 41, TP 17, presisi median 0,6404 | alarm turun, deteksi tetap tidak layak alarm |
| Model | FP (`R8-001`, `R8-002`, `R8-003`) | TP (`R8-006`, `R8-007`) | Presisi median | Recall median | FAR median per 24 jam | Fold FAR tidak lebih 6 |
| rule kanal | 2105 | 5579 | 0,6835 (`R8-009`) | 0,7507 | 6,932 (`R8-013`) | 3 dari 9 (`R8-015`) |

## POL (docs/RND_EVALUATION_POLICY.md)
Judul bagian: 1. Tidak ada gate biner / 2. Tiga lapisan penilaian, bukan satu ambang / 3. Engine tidak harus sama antar kerusakan / 4. Hybrid dan perpaduan tiga komponen diizinkan / 5. Baseline per tugas / 6. Empat kelas yang gagal tidak dibuang / 7. Keberhasilan dinilai di tingkat alat / 8. Konsekuensi untuk dokumen yang sudah ada

