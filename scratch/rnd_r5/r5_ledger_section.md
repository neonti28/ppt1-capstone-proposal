
---

## Bagian R5: deteksi perubahan dan anomali tanpa label (kartu t_56d8d11d)

Tanggal akses seluruh baris: 2026-10-27 (WIB). Kelas sumber mengikuti plan §2 (`STANDAR` > `JURNAL` > `RUN-KITA` > `KONVENSI` > `BELUM-TERUKUR`). Baris RUN-KITA menyebut berkas dan perintah yang dapat dijalankan ulang; baris KONVENSI menyebut dokumen yang menetapkannya; skor 1 s.d. 5 dicatat sebagai KONVENSI karena itu penilaian rekayasa, bukan pengukuran.

| No | Angka | Satuan | Kelas sumber | Rujukan persis | Tanggal akses | Dipakai di | Status |
|---|---|---|---|---|---|---|---|
| R5-001 | 52.509 | baris | RUN-KITA | `scratch/rnd_r5/grid_structure.json` (`n_rows`), perintah `python3 scratch/rnd_r5/grid_check.py` | 2026-10-27 | RND_R5 §2 | TERUKUR |
| R5-002 | 9 | well | RUN-KITA | `scratch/rnd_r5/grid_structure.json` (`per_well` berisi 9 kunci), perintah `grid_check.py` | 2026-10-27 | RND_R5 §2.1 | TERUKUR |
| R5-003 | 50 | kolom | RUN-KITA | `scratch/rnd_r5/probe_env.py` mengeluarkan `NCOL 50` untuk `scratch/v9_d1/datasets/hyd_ki.csv.gz` | 2026-10-27 | RND_R5 §2 | TERUKUR |
| R5-004 | 1 | menit per selisih satu | RUN-KITA | `grid_structure.json` F-10 `delta_top5_seconds` = [1, 7483] dari 7.570 pasangan; bukti `ts_bin` = indeks menit, bukan detik | 2026-10-27 | RND_R5 §2.0 | TERUKUR |
| R5-005 | 11.248 | menit (187,5 jam) | RUN-KITA | `grid_structure.json` F-10 `ts_min` 20672177 dan `ts_max` 20683425, selisih 11.248 | 2026-10-27 | RND_R5 §2.0 | TERUKUR |
| R5-006 | 5 | dari 9 well | RUN-KITA | `scratch/rnd_r5/drift_measured_v2.json` (`summary.n_wells_dipakai`), perintah `python3 scratch/rnd_r5/measure_drift_v2.py` | 2026-10-27 | RND_R5 §2.1 | TERUKUR |
| R5-007 | 257 | menit baseline bersih | RUN-KITA | `drift_measured_v2.json` `per_well.F-10.baseline_minutes` | 2026-10-27 | RND_R5 §2.1, §2.2 | TERUKUR |
| R5-008 | 358 | menit baseline bersih | RUN-KITA | `drift_measured_v2.json` `per_well.F-14.baseline_minutes` | 2026-10-27 | RND_R5 §2.1, §2.2 | TERUKUR |
| R5-009 | 284 | menit baseline bersih | RUN-KITA | `drift_measured_v2.json` `per_well.F-15A.baseline_minutes` | 2026-10-27 | RND_R5 §2.1, §2.2 | TERUKUR |
| R5-010 | 297 | menit baseline bersih | RUN-KITA | `drift_measured_v2.json` `per_well.F-15_S.baseline_minutes` | 2026-10-27 | RND_R5 §2.1, §2.2 | TERUKUR |
| R5-011 | 361 | menit baseline bersih | RUN-KITA | `drift_measured_v2.json` `per_well.F-9_A.baseline_minutes` | 2026-10-27 | RND_R5 §2.1, §2.2 | TERUKUR |
| R5-012 | 297 | menit (median baseline) | RUN-KITA | `drift_measured_v2.json` `summary.baseline_minutes_median` | 2026-10-27 | RND_R5 §2.2 | TERUKUR |
| R5-013 | 16,81 | episode CUSUM per 24 jam | RUN-KITA | `drift_measured_v2.json` `per_well.F-10.cusum_far_24h` | 2026-10-27 | RND_R5 §2.2 | TERUKUR |
| R5-014 | 4,02 | episode CUSUM per 24 jam | RUN-KITA | `drift_measured_v2.json` `per_well.F-14.cusum_far_24h` | 2026-10-27 | RND_R5 §2.2 | TERUKUR |
| R5-015 | 10,14 | episode CUSUM per 24 jam | RUN-KITA | `drift_measured_v2.json` `per_well.F-15A.cusum_far_24h` | 2026-10-27 | RND_R5 §2.2 | TERUKUR |
| R5-016 | 9,70 | episode CUSUM per 24 jam | RUN-KITA | `drift_measured_v2.json` `per_well.F-15_S.cusum_far_24h` dan `summary.cusum_far24_median` | 2026-10-27 | RND_R5 §2.2 | TERUKUR |
| R5-017 | 7,98 | episode CUSUM per 24 jam | RUN-KITA | `drift_measured_v2.json` `per_well.F-9_A.cusum_far_24h` | 2026-10-27 | RND_R5 §2.2 | TERUKUR |
| R5-018 | 0,00 | episode PH per 24 jam | RUN-KITA | `drift_measured_v2.json` `per_well.F-10.ph_far_24h` | 2026-10-27 | RND_R5 §2.2 | TERUKUR |
| R5-019 | 8,04 | episode PH per 24 jam | RUN-KITA | `drift_measured_v2.json` `per_well.F-14.ph_far_24h` dan `summary.ph_far24_median` | 2026-10-27 | RND_R5 §2.2 | TERUKUR |
| R5-020 | 10,14 | episode PH per 24 jam | RUN-KITA | `drift_measured_v2.json` `per_well.F-15A.ph_far_24h` | 2026-10-27 | RND_R5 §2.2 | TERUKUR |
| R5-021 | 4,85 | episode PH per 24 jam | RUN-KITA | `drift_measured_v2.json` `per_well.F-15_S.ph_far_24h` | 2026-10-27 | RND_R5 §2.2 | TERUKUR |
| R5-022 | 11,97 | episode PH per 24 jam | RUN-KITA | `drift_measured_v2.json` `per_well.F-9_A.ph_far_24h` | 2026-10-27 | RND_R5 §2.2 | TERUKUR |
| R5-023 | 0,987 | autokorelasi lag-1 (median) | RUN-KITA | `drift_measured_v2.json` `summary.ac1_median`; rentang `ac1_min` 0,9765 dan `ac1_max` 0,9954 | 2026-10-27 | RND_R5 §2.2 | TERUKUR |
| R5-024 | 3 | dari 5 well | RUN-KITA | `drift_measured_v2.json` `summary.wells_half2_bersih_pada_h_kalibrasi` | 2026-10-27 | RND_R5 §2.2 | TERUKUR |
| R5-025 | 40 / 4 / 60 / 60 / 60 | ambang h CUSUM (sigma) | RUN-KITA | `drift_measured_v2.json` `per_well.*.half1_h_calibrated` untuk F-10, F-14, F-15A, F-15_S, F-9_A | 2026-10-27 | RND_R5 §2.2 | TERUKUR |
| R5-026 | 0,986 | statistik D KS (median) | RUN-KITA | `drift_measured_v2.json` `summary.ks_between_well_D_median`; min 0,723 dan maks 1,000 | 2026-10-27 | RND_R5 §2.3 | TERUKUR |
| R5-027 | 10 | dari 10 pasangan, p < 0,05 | RUN-KITA | `drift_measured_v2.json` `summary.ks_between_well_p_lt_0_05` = 10 dan `ks_between_well_pairs` = 10 | 2026-10-27 | RND_R5 §2.3 | TERUKUR |
| R5-028 | 0,211 | statistik D KS dalam well (median) | RUN-KITA | `drift_measured_v2.json` `summary.ks_within_well_D_median`; F-14 `D` 0,9777 | 2026-10-27 | RND_R5 §2.3 | TERUKUR |
| R5-029 | 4 | dari 5 well, p < 0,05 | RUN-KITA | `drift_measured_v2.json` `summary.ks_within_well_p_lt_0_05` | 2026-10-27 | RND_R5 §2.3 | TERUKUR |
| R5-030 | 0,7523 s.d. 1,0000 | recall horizon 10 menit (CUSUM, deret penuh) | RUN-KITA | `drift_measured_v2.json` `per_well.*.cusum_recall_h10_full_series` | 2026-10-27 | RND_R5 §2.4 | TERUKUR |
| R5-031 | 0,2387 s.d. 0,9069 | recall horizon 10 menit (PH, deret penuh) | RUN-KITA | `drift_measured_v2.json` `per_well.*.ph_recall_h10_full_series` | 2026-10-27 | RND_R5 §2.4 | TERUKUR |
| R5-032 | 52,293 s.d. 60,000 | menit alarm CUSUM per jam di luar baseline | RUN-KITA | `drift_measured_v2.json` `per_well.*.cusum_alarm_rate_outside_per_hour` | 2026-10-27 | RND_R5 §2.4 | TERUKUR |
| R5-033 | 4.281 | positif `y_hyd` pada 5 well | RUN-KITA | `drift_measured_v2.json` `summary.total_positives` | 2026-10-27 | RND_R5 §2.4 | TERUKUR |
| R5-034 | 0,5 sigma | parameter k CUSUM | KONVENSI | bentuk dari Page 1954 (DOI 10.1093/biomet/41.1-2.100); nilai 0,5 sigma dipilih tim, di `scratch/rnd_r5/measure_drift_v2.py` baris `K_SIGMA` | 2026-10-27 | RND_R5 §2, §2.2 | TERVERIFIKASI (bentuk) |
| R5-035 | 5 sigma | parameter h CUSUM | KONVENSI | dipilih tim, `measure_drift_v2.py` baris `H_SIGMA`; alasan memakai ambang konvensional adalah untuk menunjukkan bahwa nilai buku teks gagal pada data nyata | 2026-10-27 | RND_R5 §2, §2.2 | TERVERIFIKASI (konvensi) |
| R5-036 | 0,005 sigma dan 50 sigma | parameter delta dan lambda Page-Hinkley | KONVENSI | bentuk dari Hinkley 1971 (DOI 10.1093/biomet/58.3.509); nilai di `measure_drift_v2.py` baris `PH_DELTA` dan `PH_LAMBDA` | 2026-10-27 | RND_R5 §2, §2.2 | TERVERIFIKASI (bentuk) |
| R5-037 | 240 | menit (panjang minimum baseline bersih) | KONVENSI | `measure_drift_v2.py` baris `MIN_BASE`; dipilih agar setara 4 jam operasi dan tetap menyisakan 5 well | 2026-10-27 | RND_R5 §2.1 | TERVERIFIKASI (konvensi) |
| R5-038 | 30 | menit (jarak penggabungan episode alarm) | KONVENSI | `measure_drift_v2.py` baris `MERGE_GAP` | 2026-10-27 | RND_R5 §2.2 | TERVERIFIKASI (konvensi) |
| R5-039 | 10 | menit (horizon label onset) | KONVENSI | `measure_drift_v2.py` baris `HORIZON`; sama dengan horizon yang dipakai V9 (`scratch/v9_i1/v9_i1_RESULTS.json`) | 2026-10-27 | RND_R5 §2.4 | TERVERIFIKASI (konvensi) |
| R5-040 | 6 | episode alarm maksimum per 24 jam | KONVENSI | `docs/RND_ALGO_RESEARCH_PLAN.md` §6 gate A (FAR rig) | 2026-10-27 | RND_R5 §2.2, §2.5.1 | TERVERIFIKASI (konvensi) |
| R5-041 | 32 | fitur | RUN-KITA | `scratch/rnd_r5/anomaly_unsup.json` `meta.n_fitur`; 8 kanal x 4 statistik, daftar di `meta.fitur` | 2026-10-27 | RND_R5 §2.5 | TERUKUR |
| R5-042 | 2 | well dipakai pada uji anomali | RUN-KITA | `anomaly_unsup.json` `summary.n_well_dipakai` (F-10, F-15_S); perintah `scratch/rnd_r5/.venv/bin/python scratch/rnd_r5/anomaly_unsup.py` | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |
| R5-043 | 0,01 | contamination | KONVENSI | `anomaly_unsup.py` baris `CONTAM`; dipilih agar sesuai laju alarm 1% yang diminta | 2026-10-27 | RND_R5 §2.5.1 | TERVERIFIKASI (konvensi) |
| R5-044 | 1.500 | baris batas fit | KONVENSI | `anomaly_unsup.py` baris `FIT_CAP` | 2026-10-27 | RND_R5 §2.5.1 | TERVERIFIKASI (konvensi) |
| R5-045 | 0,0109 | laju alarm baseline Isolation Forest (median) | RUN-KITA | `anomaly_unsup.json` `summary.iforest.laju_alarm_baseline_median` | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |
| R5-046 | 11,21 dan 9,70 | FAR per 24 jam Isolation Forest (F-10, F-15_S) | RUN-KITA | `anomaly_unsup.json` `per_well.F-10.iforest.far_per_24h` dan `per_well.F-15_S.iforest.far_per_24h` | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |
| R5-047 | 0,6131 | recall horizon 10 menit Isolation Forest (median) | RUN-KITA | `anomaly_unsup.json` `summary.iforest.recall_h10_median`; per well 0,3793 dan 0,8470 | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |
| R5-048 | 0,2240 | presisi alarm-menit Isolation Forest (median) | RUN-KITA | `anomaly_unsup.json` `summary.iforest.presisi_menit_median` | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |
| R5-049 | 1.353 dan 6.096 | menit alarm total Isolation Forest | RUN-KITA | `anomaly_unsup.json` `per_well.F-10.iforest.alarm_menit_total` dan `per_well.F-15_S.iforest.alarm_menit_total` | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |
| R5-050 | 0,0089 | laju alarm baseline LOF (median) | RUN-KITA | `anomaly_unsup.json` `summary.lof.laju_alarm_baseline_median` | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |
| R5-051 | 0,9970 | recall horizon 10 menit LOF (median) | RUN-KITA | `anomaly_unsup.json` `summary.lof.recall_h10_median` | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |
| R5-052 | 5.920 dan 7.896 | menit alarm total LOF | RUN-KITA | `anomaly_unsup.json` `per_well.*.lof.alarm_menit_total` | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |
| R5-053 | 0,2032 | presisi alarm-menit LOF (median) | RUN-KITA | `anomaly_unsup.json` `summary.lof.presisi_menit_median` | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |
| R5-054 | 0,0665 | laju alarm baseline One-Class SVM (median) | RUN-KITA | `anomaly_unsup.json` `summary.ocsvm.laju_alarm_baseline_median`; rentang 0,0623 s.d. 0,0707 | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |
| R5-055 | 11,21 dan 14,55 | FAR per 24 jam One-Class SVM | RUN-KITA | `anomaly_unsup.json` `per_well.F-10.ocsvm.far_per_24h` dan `per_well.F-15_S.ocsvm.far_per_24h` | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |
| R5-056 | 0,0109 | laju alarm baseline autoencoder (median) | RUN-KITA | `anomaly_unsup.json` `summary.ae.laju_alarm_baseline_median` | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |
| R5-057 | 1,0000 | recall horizon 10 menit autoencoder (median) | RUN-KITA | `anomaly_unsup.json` `summary.ae.recall_h10_median` | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |
| R5-058 | 6.154 dan 8.006 | menit alarm total autoencoder | RUN-KITA | `anomaly_unsup.json` `per_well.*.ae.alarm_menit_total` | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |
| R5-059 | 0,2011 | presisi alarm-menit autoencoder (median) | RUN-KITA | `anomaly_unsup.json` `summary.ae.presisi_menit_median` | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |
| R5-060 | 0,5000 dan 1,0000 | laju alarm pada baseline well lain (median dan maksimum) | RUN-KITA | `anomaly_unsup.json` `summary.iforest.transfer_laju_alarm_median` 0,5 dan `summary.lof.transfer_laju_alarm_median` 1,0; OCSVM dan AE juga 1,0; `transfer_pasangan` = 2 | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |
| R5-061 | 2 dan 3 | titik diskord matrix profile | RUN-KITA | `anomaly_unsup.json` `per_well.F-10.matrix_profile.titik_diskord` = 2 dan `per_well.F-15_S.matrix_profile.titik_diskord` = 3; jendela 60 menit | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |
| R5-062 | 0 | well dipakai pada percobaan pertama | RUN-KITA | `scratch/rnd_r5/drift_far_measured.json` `summary.n_wells_dipakai` = 0; **artefak satuan** (langkah 60 pada indeks menit), tidak dipakai sebagai bukti | 2026-10-27 | RND_R5 §2.0 | TERUKUR (hasil dibatalkan) |
| R5-063 | 6 s.d. 28 | menit blok maksimum pada percobaan pertama | RUN-KITA | `drift_far_measured.json` `skipped.*.block_max_minutes`; artefak satuan yang sama, dicatat sebagai kesalahan yang sudah dikoreksi | 2026-10-27 | RND_R5 §2.0 | TERUKUR (artefak) |
| R5-064 | 1 s.d. 5 | skor kriteria data, biaya, interpretasi | KONVENSI | penilaian rekayasa tim R&D, kriteria dinyatakan di RND_R5 §1 dan §3.3; bukan hasil pengukuran | 2026-10-27 | RND_R5 §1, §3.3, §5 | TERVERIFIKASI (konvensi) |
| R5-065 | 0,3 / 0,3 / 0,4 | bobot skor gabungan (data / biaya / interpretasi) | KONVENSI | RND_R5 §5; bobot dinyatakan terbuka agar dapat dibantah | 2026-10-27 | RND_R5 §5 | TERVERIFIKASI (konvensi) |
| R5-066 | 124 | episode onset hyd K-ii (1 wellbore) | RUN-KITA | dikutip dari handoff kartu `t_34c20c78` (`onsets.hyd_K_ii`) dan `docs/RND_D0_DATA_FEASIBILITY.md`; tidak dihitung ulang di R5 | 2026-10-27 | RND_R5 §4.1 | TERUKUR (kutipan) |
| R5-067 | 78,7 | persen jendela sign-flip hyd K-ii | RUN-KITA | `docs/V9_EVAL_C_LAYERC.md` tabel §1 (6.377 dari 8.107 jendela); tidak dihitung ulang di R5 | 2026-10-27 | RND_R5 §4.1 | TERUKUR (kutipan) |
| R5-068 | 0,119 s.d. 0,984 | AUPRC persistence bit_wear K-1 | RUN-KITA | `docs/V9_EVAL_C_LAYERC.md` tabel §1; tidak dihitung ulang di R5 | 2026-10-27 | RND_R5 §4.2 | TERUKUR (kutipan) |
| R5-069 | 20 s.d. 36 | detik TLead tool_wear K-i | RUN-KITA | `docs/V9_EVAL_C_LAYERC.md` tabel §1 dan `docs/RND_P0_PARAMETER.md`; 4 alat | 2026-10-27 | RND_R5 §0, §1.1 | TERUKUR (kutipan) |
| R5-070 | 0,50 | presisi biner tool_wear K-i | RUN-KITA | `docs/V9_EVAL_C_LAYERC.md` tabel §1 (4 FP di alat baru) | 2026-10-27 | RND_R5 §1.1 | TERUKUR (kutipan) |
| R5-071 | 0,3333 | Hz laju sampel kanal maksimum | RUN-KITA | `docs/RND_D0_DATA_FEASIBILITY.md` tabel sampling; mengikat keputusan menolak metode yang butuh laju lebih tinggi | 2026-10-27 | RND_R5 §0 | TERUKUR (kutipan) |
| R5-072 | 119 | rasio sebar FAR ambang RF vib antar well | RUN-KITA | `docs/V9_EVAL_C_LAYERC.md` §1 (τ0,5 FAR 4,1 s.d. 496); alasan menolak ambang global | 2026-10-27 | RND_R5 §1.1 | TERUKUR (kutipan) |

### Rujukan R5 yang diverifikasi (JURNAL)

Perintah: `bash scratch/rnd_r5/dois.sh`; hasil: `scratch/rnd_r5/doi_check.txt`. Status "TERVERIFIKASI" berarti rekaman Crossref cocok pada penulis pertama, tahun, judul, wadah, dan halaman; halaman penerbit mengembalikan 403 (bot wall) atau 202 dari host ini, sehingga isi penuh tidak dibuka.

| No | Angka | Satuan | Kelas sumber | Rujukan persis | Tanggal akses | Dipakai di | Status |
|---|---|---|---|---|---|---|---|
| R5-073 | Page 1954 | rujukan | JURNAL | Page, E. S. (1954). Continuous inspection schemes. Biometrika 41(1-2), 100-115. DOI 10.1093/biomet/41.1-2.100 (Crossref OK; doi.org 403) | 2026-10-27 | RND_R5 §1, §6 | TERVERIFIKASI |
| R5-074 | Hinkley 1971 | rujukan | JURNAL | Hinkley, D. V. (1971). Inference about the change-point from cumulative sum tests. Biometrika 58(3), 509-523. DOI 10.1093/biomet/58.3.509 (Crossref OK; doi.org 403) | 2026-10-27 | RND_R5 §1, §6 | TERVERIFIKASI |
| R5-075 | Adams dan MacKay 2007 | rujukan | JURNAL | Adams, R. P., MacKay, D. J. C. (2007). Bayesian Online Changepoint Detection. arXiv:0710.3742 (arXiv API OK, HTTP 200) | 2026-10-27 | RND_R5 §1, §6 | TERVERIFIKASI |
| R5-076 | Bifet dan Gavaldà 2007 | rujukan | JURNAL | Bifet, A., Gavaldà, R. (2007). Learning from Time-Changing Data with Adaptive Windowing. Proc. SIAM Int. Conf. Data Mining, 443-448. DOI 10.1137/1.9781611972771.42 (Crossref OK; doi.org 403) | 2026-10-27 | RND_R5 §1, §6 | TERVERIFIKASI |
| R5-077 | Liu dkk. 2008 | rujukan | JURNAL | Liu, F. T., Ting, K. M., Zhou, Z.-H. (2008). Isolation Forest. ICDM 2008, 413-422. DOI 10.1109/ICDM.2008.17 (Crossref OK; doi.org 202) | 2026-10-27 | RND_R5 §3.3, §6 | TERVERIFIKASI |
| R5-078 | Breunig dkk. 2000 | rujukan | JURNAL | Breunig, M. M., Kriegel, H.-P., Ng, R. T., Sander, J. (2000). LOF: Identifying Density-Based Local Outliers. Proc. ACM SIGMOD, 93-104. DOI 10.1145/342009.335388 (Crossref OK; doi.org 403) | 2026-10-27 | RND_R5 §3.3, §6 | TERVERIFIKASI |
| R5-079 | Schölkopf dkk. 2001 | rujukan | JURNAL | Schölkopf, B., Platt, J. C., Shawe-Taylor, J., Smola, A. J., Williamson, R. C. (2001). Estimating the Support of a High-Dimensional Distribution. Neural Computation 13(7), 1443-1471. DOI 10.1162/089976601750264965 (Crossref OK; doi.org 403) | 2026-10-27 | RND_R5 §3.3, §6 | TERVERIFIKASI |
| R5-080 | Yeh dkk. 2016 | rujukan | JURNAL | Yeh, C.-C. M., Zhu, Y., Ulanova, L., dkk. (2016). Matrix Profile I: All Pairs Similarity Joins for Time Series. ICDM 2016, 1317-1322. DOI 10.1109/ICDM.2016.0179 (Crossref OK; doi.org 202) | 2026-10-27 | RND_R5 §3.3, §6 | TERVERIFIKASI |
| R5-081 | Zhu dkk. 2016 | rujukan | JURNAL | Zhu, Y., Yeh, C.-C. M., Zimmerman, Z., Kamgar, K., Keogh, E. (2016). Matrix Profile II. ICDM 2016, 739-748. DOI 10.1109/ICDM.2016.0085 (Crossref OK; doi.org 202) | 2026-10-27 | RND_R5 §3.3, §6 | TERVERIFIKASI |
| R5-082 | Sakurada dan Yairi 2014 | rujukan | JURNAL | Sakurada, M., Yairi, T. (2014). Anomaly Detection Using Autoencoders with Nonlinear Dimensionality Reduction. Proc. MLSDA 2014, 4-11. DOI 10.1145/2689746.2689747 (Crossref OK; doi.org 403) | 2026-10-27 | RND_R5 §3.3, §6 | TERVERIFIKASI |
| R5-083 | Massey 1951 | rujukan | JURNAL | Massey, F. J. (1951). The Kolmogorov-Smirnov Test for Goodness of Fit. JASA 46(253), 68-78. DOI 10.1080/01621459.1951.10500769 (Crossref OK; doi.org 403) | 2026-10-27 | RND_R5 §1, §6 | TERVERIFIKASI |
| R5-084 | 1 | DOI dibuang | BELUM-TERUKUR | 10.1214/09-AOAS282 terverifikasi sebagai makalah berbeda (Shirley dkk. 2010, HMM uji alkohol) dan dibuang; tidak dipakai di RND_R5 | 2026-10-27 | RND_R5 §6 | TERVERIFIKASI (penolakan) |
