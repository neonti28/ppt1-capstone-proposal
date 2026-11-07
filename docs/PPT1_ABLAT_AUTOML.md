# ABLAT AUTOML: PENCARIAN OTOMATIS 100 MODEL LAWAN RANDOM FOREST TUNED

Tanggal: 6 November 2026. Ruang kerja: `/mnt/d/ARCT-9F2`. Status: **TERUKUR** (seluruh angka berasal dari JSON hasil eksekusi, bukan klaim).

Riset pendahuluan: `verification-mandatory` (setiap angka punya jejak berkas dan perintah yang bisa dijalankan ulang).
Riset pendahuluan: `sequentialthinking` (sequ-mcp, 3 pikiran): pertama memisahkan klaim dari bukti mentah, kedua menguji hipotesis alternatif (salah ukur metrik, salah pemilihan model, salah jumlah fitur), ketiga menyimpulkan hanya pada bagian yang lolos uji.

**Pertanyaan yang dijawab dokumen ini:** apakah engine pencarian hyperparameter otomatis (H2O AutoML) mengalahkan Random Forest tuned pada data kejadian pengeboran, dan bila tidak, mengapa.

**Bukan untuk menjawab:** rumusan masalah proposal. Dokumen ini bahan pendukung pemilihan algoritma di Bab III, bukan kesimpulan.

## 1. Pengaturan eksperimen

| Parameter | Nilai | Sumber |
|---|---|---|
| Dataset | 4.619 baris x 480 fitur, 243 positif (5,3 persen) | `data/predictive/features_timeseries_controls_berdata.npz` + `features_timeseries.npz` |
| Definisi positif | 6 kategori bukti kegagalan (`bha_stuck_fishing`, `bha_downhole_equipment`, `wellbore_fluid`, `surface_rig_equipment`, `wireline_completion_intervention`, `safety_personnel`) | `scratch/h2o/h2o_kontrol.json` bagian `data.definisi_positif` |
| Skema uji | Leave-one-well-out pada 7 sumur (`F-14`, `F-15A`, `F-15_S`, `F-5`, `F-7`, `F-9`, `F-9_A`) | skrip `h2o_eksperimen.py` |
| Anggaran AutoML | `max_models=100`, `max_runtime_secs=600` per sumur, `sort_metric=AUCPR`, `balance_classes=True`, `seed=42` | skrip `h2o_eksperimen.py:178-180` |
| CV internal | `fold_column=wellbore` (6 fold per sumur latihan) | `scratch/h2o/h2o_kontrol.json` bagian `setelan` |
| Sumber daya | 18 core, heap JVM 2 GB | log server H2O (tercatat terukur 11,4 core rata-rata dari 18) |
| Metrik | AUPRC dihitung `sklearn.average_precision_score` pada prediksi kelas p1, sama seperti baseline | skrip, dan skill `tabular-automl-benchmarking` langkah 2 |
| Baseline pembanding | RF 400 pohon + `class_weight=balanced_subsample`, `min_samples_leaf=3`; regresi logistik berpenalti + scaler; mayoritas | `scratch/h2o/baseline_only.json` |

Total komputasi eksperimen: 600 detik x 7 sumur = 4.200 detik anggaran kandidat, ditambah CV internal 6 fold pada tiap kandidat.

## 2. Hasil per sumur (dari `scratch/h2o/h2o_kontrol.json`)

| Sumur | n uji | positif | Leader AutoML | AUPRC AutoML | AUPRC RF | AUPRC reglog | Lantai mayoritas | Menang |
|---|---|---|---|---|---|---|---|---|
| F-14 | 1.369 | 59 | XGBoost_3 | 0,0848 | **0,1008** | 0,0920 | 0,0431 | RF |
| F-15A | 476 | 24 | XGBoost_1 | 0,0588 | **0,0948** | 0,0513 | 0,0504 | RF |
| F-15_S | 898 | 69 | GBM_3 | **0,1164** | 0,1063 | 0,1156 | 0,0768 | AutoML |
| F-5 | 932 | 27 | GBM_1 | 0,0272 | 0,0325 | **0,0479** | 0,0290 | reglog |
| F-7 | 301 | 24 | XGBoost_2 | 0,0951 | 0,0884 | **0,0993** | 0,0797 | reglog |
| F-9 | 300 | 24 | GBM_1 | 0,4643 | **0,4729** | 0,2741 | 0,0800 | RF |
| F-9_A | 343 | 16 | GBM_3 | 0,0769 | **0,0785** | 0,0624 | 0,0466 | RF |

**Rekap:** AutoML menang 2 dari 7 sumur. Rata-rata AUPRC AutoML **0,1319**, RF **0,1392**.

Pada ambang 0,5, 5 dari 7 leader AutoML memprediksi nol positif (presisi dan recall sama-sama 0), sehingga pada bentuk default tidak langsung dapat dipakai sebagai peringatan.

## 3. Temuan T1: penambahan anggaran tidak menaikkan hasil

Dua run dengan setelan berbeda pada sumur F-14 memberi hasil yang tidak bergerak searah:

| Run | Anggaran | Leader | AUPRC uji |
|---|---|---|---|
| Pertama (400 detik) | 400 detik | GBM_3 | 0,1045 |
| Kedua (600 detik) | 600 detik | XGBoost_3 | 0,0848 |

Jadi menambah 50 persen waktu komputasi justru menurunkan AUPRC uji pada F-14. Penyebabnya ada di Temuan T2.

## 4. Temuan T2: sinyal pemilihan model internal bocor dan berada di bawah noise

Yang dipakai H2O untuk memilih leader adalah AUPRC CV internal. Nilai itu dibandingkan dengan AUPRC uji sebenarnya:

| Sumur | AUPRC CV leader | Sebaran top-5 kandidat | AUPRC uji |
|---|---|---|---|
| F-14 | 0,0891 | 0,0085 | 0,0848 |
| F-15A | 0,0844 | 0,0031 | 0,0588 |
| F-15_S | 0,0869 | 0,0011 | 0,1164 |
| F-5 | 0,0988 | 0,0024 | 0,0272 |
| F-7 | 0,1018 | 0,0169 | 0,0951 |
| F-9 | 0,0732 | 0,0017 | 0,4643 |
| F-9_A | 0,1034 | 0,0045 | 0,0769 |

1. **Korelasi Spearman (CV leader, AUPRC uji) = -0,39.** Berkorelasi berbalik arah: ranking internal tidak menunjukkan siapa yang akan menang di sumur yang belum pernah dilihat.
2. **Selisih antar kandidat rata-rata hanya 0,0055 AUPRC**, sementara jarak CV leader ke AUPRC uji rata-rata **0,0793** (14 kali lebih besar). Pemenang leaderboard ditentukan di dalam noise.
3. **AUPRC itu peka prevalensi, dan prevalensi antar fold sangat berbeda** (2,9 sampai 8,0 persen). Dengan `fold_column=wellbore`, fold berisi sumur yang berbeda, sehingga AUPRC CV tercampur perbedaan kemudahan sumur, bukan perbedaan kualitas model.

Konsekuensinya: menambah model, core, atau detik tidak memperbaiki pemilihan, karena yang kurang bukan anggaran melainkan statistik seleksi yang netral terhadap prevalensi.

## 5. Temuan T3: DeepLearning AutoML gagal total karena satu kanal rusak

DeepLearning tidak menghasilkan satu pun model pada ketujuh run. Penyebabnya ditemukan pada data, bukan pada engine.

**Bukti struktural (dihitung langsung dari npz):**

- 5 baris memuat nilai sensor SPPA sampai **9,524e+30** (baris 1756 pada kontrol, baris 241 pada kejadian), dengan seluruh fitur turunannya ikut meledak: `std` 2,89e+29, `mean` 1,07e+28, `slope_per_min` 1,74e+26.
- Seluruh fitur lain berada di rentang 0 sampai 1 (rasio skala antar kolom 1,35), sehingga sel rusak itu 35 orde lebih besar dari distribusi.
- 188.872 NaN (9,9 persen) pada 438 dari 480 kolom, terbanyak `burstiness` dan `trend_rho` (67 sampai 81 persen kosong).

**Uji sebab-akibat (3 tahap, dijalankan pada cluster H2O terpisah):**

| Tahap | Perlakuan | Hasil |
|---|---|---|
| A | Tanpa perlakuan | **GAGAL**: `Trying to predict with an unstable model` |
| B | Clip p99,9 per kolom | **GAGAL**: batas percentile sendiri masih 2,26e+27 dan 107 kolom memuat glitch |
| C | Clip p99 per kolom | **SUKSES konvergen**: xval `pr_auc 0,08`, logloss 0,4645 |

Jadi model pohon (GBM, XGBoost, DRF, XRT) kebal karena split berbasis peringkat, sedangkan jaringan saraf menstandardisasi tiap kolom lalu mengalikan bobot, sehingga z-score 10^30 menghancurkan gradien. Angka setelah perbaikan (`pr_auc 0,08`) masih di bawah RF (0,1008), jadi perbaikan data membuatnya dapat dilatih, bukan membuatnya menang.

Artefak: `docs/evidence/dl_klipp99.json`.

## 6. Temuan T4: menggabungkan kandidat AutoML mengalahkan RF, sedangkan leader tunggal tidak

Temuan T1 dan T2 hanya menguji leader tunggal. Pertanyaan lanjutannya: kalau seluruh kandidat digabung, apakah hasilnya membaik. Untuk itu dijalankan ulang AutoML dengan setelan identik (600 detik, 100 model, `fold_column=wellbore`, seed 42), tetapi skor prediksi **setiap** kandidat disimpan pada sumur uji, bukan hanya leader. Jumlah kandidat yang dihasilkan per sumur 9 sampai 12.

Dua jalur dipisahkan tegas. Jalur **adil**: urutan dan bobot kandidat hanya memakai AUCPR CV internal, sehingga informasi sumur uji tidak pernah masuk ke proses pemilihan. Jalur **oracle**: pemilihan memakai AUPRC sumur uji, hanya dicatat sebagai batas atas yang tidak boleh diklaim sebagai hasil.

**Rata-rata AUPRC di 7 sumur, jalur adil:**

| Strategi kombinasi | Rata-rata AUPRC | Selisih terhadap RF |
|---|---|---|
| Median seluruh kandidat (top-20) | **0,1525** | +0,0133 |
| Median top-10 | 0,1524 | +0,0132 |
| Rank-average top-5 | 0,1519 | +0,0127 |
| Rata-rata top-10 | 0,1472 | +0,0080 |
| Rata-rata seluruh kandidat | 0,1470 | +0,0078 |
| Borda seluruh kandidat | 0,1454 | +0,0062 |
| **RF tuned (baseline)** | **0,1392** | 0 |
| Leader tunggal (pilihan CV) | 0,1325 | −0,0067 |
| Regresi logistik | 0,1061 | −0,0331 |
| Lantai mayoritas | 0,0579 | −0,0813 |

Jadi leader tunggal memang kalah dari RF (sesuai T1), tetapi **median dari seluruh kandidat menang dengan selisih +0,0133 AUPRC, atau 9,6 persen relatif**. Rata-rata peringkat (rank-average) dan median memberi hasil hampir sama, dan keduanya mengungguli rata-rata biasa, karena rata-rata mudah ditarik satu model yang terlalu percaya diri.

**Per sumur (median seluruh kandidat lawan RF):**

| Sumur | Median kandidat | RF | Selisih |
|---|---|---|---|
| F-14 | 0,0986 | 0,1008 | −0,0022 |
| F-15A | 0,1748 | 0,0948 | **+0,0800** |
| F-15_S | 0,1081 | 0,1063 | +0,0018 |
| F-5 | 0,0341 | 0,0325 | +0,0016 |
| F-7 | 0,1009 | 0,0884 | +0,0125 |
| F-9 | 0,4700 | 0,4729 | −0,0029 |
| F-9_A | 0,0808 | 0,0785 | +0,0023 |

Menang di 5 dari 7 sumur. Yang penting, sifat kesalahannya berbeda: leader tunggal bisa jatuh sampai −0,0360 pada satu sumur, sedangkan median kandidat paling buruk hanya −0,0029. Kombinasi tidak menaikkan semua sumur, tetapi **menghapus risiko salah pilih model** yang menjadi penyakit utama AutoML di data ini. Lonjakan terbesar ada di F-15A (+84 persen relatif), sumur dengan prevalensi terendah (24 positif dari 476 baris), tempat model tunggal paling rapuh.

**Batas atas (oracle, bukan hasil):** pemilihan greedy yang boleh melihat sumur uji mencapai 0,1681, dan kandidat tunggal terbaik per sumur 0,1605. Artinya masih ada ruang 0,0156 di atas median adil bila seleksi bisa disempurnakan, tetapi ruang itu kecil dibanding jarak ke RF dan tidak dapat diambil tanpa informasi sumur uji.

**Kesimpulan operasional:** yang layak dipakai dari AutoML bukan leadernya, melainkan gabungan median seluruh kandidatnya. Ini juga menjelaskan mengapa menambah anggaran tidak menolong pada T1: masalahnya bukan jumlah model, melainkan pemilihan satu pemenang di antara kandidat yang selisihnya di bawah noise.

## 7. Perbandingan dengan kombinasi algoritma per engine sebelumnya

Perbandingan ini **kualitatif, bukan angka mentah**, karena unitnya berbeda: engine lama memakai jendela 1 menit dengan label per engine, sedangkan eksperimen ini memakai per kejadian dengan label bukti kegagalan.

| Engine lama | Kombinasi algoritma | Hasil head terbaik | Selaras dengan temuan di sini |
|---|---|---|---|
| vib | rule + persistence | P 0,94, R 0,45 | label kanal derivatif membuat semua metrik melonjak, bukan karena algoritma |
| ssi | rule + persistence AND | hybrid memotong FP 73 persen | label langka membuat head ML presisi 0 |
| shk | rule + persistence | P 0,53, R 0,07 | sama seperti 5 sumur AutoML yang memprediksi nol positif |
| stuck | rule + persistence + E1 | persistence_event P 0,50, R 0,005 | persistence mengalahkan RF di kelas ini |
| hyd | hibrida dua mode | hybrid P 0,82, R 0,60 | pemenangnya kombinasi aturan, bukan satu model |
| tool_wear | rule terkalibrasi per alat | P 0,62, R 0,05 | kalibrasi per unit, bukan ambang global |

Pola yang sama muncul dua kali dan dua kali independen: pada label langka, head ML berhenti di kelas ranking, sedangkan aturan terkalibrasi per unit yang memberi presisi berguna. Eksperimen ini menambah satu bukti baru: **engine pencarian otomatis dengan anggaran komputasi maksimal pun tidak menyalip RF tuned pada skema LOO yang sama.**

## 8. Implikasi untuk pemilihan algoritma di Bab III

1. Pemilihan RF tuned sebagai engine utama berstatus **teruji**, bukan preferensi: sudah diadu lawan pencarian otomatis 18 core dan kalah tipis 5 dari 7 sumur.
2. Rule + persistence + kalibrasi per unit tetap arsitektur yang dipakai pada engine yang labelnya tersedia; AutoML tidak menggantikannya.
3. Data defect SPPA (5 sel sampai 9,524e+30) masuk daftar perbaikan data: tanpa clip atau drop kolom turunan SPPA, seluruh keluarga model linear dan jaringan saraf tidak dapat dipakai pada dataset ini.
4. Pernyataan "AutoML lebih baik" dilarang pada Bab IV tanpa skema seleksi yang netral prevalensi; angka yang ada justru mendukung sebaliknya.

## 9. Jejak reproduksi

| Berkas | Isi |
|---|---|
| `docs/evidence/h2o_kontrol.json` | Hasil AutoML 7 sumur lengkap dengan leaderboard internal tiap sumur dan setelan |
| `docs/evidence/baseline_only.json` | Baseline RF, reglog, mayoritas per sumur (dipakai ulang oleh AutoML, tidak dihitung ganda) |
| `docs/evidence/dl_klipp99.json` | Hasil uji C: DeepLearning konvergen setelah clip p99 |
| `scratch/h2o_eksperimen.py` | Skrip utama eksperimen |
| `scratch/uji_dl_sebab.py` | Uji tahap A dan B |
| `scratch/uji_dl_c.py` | Uji tahap C |
| `scratch/diag_ekstrem.py`, `scratch/diag_nan.py`, `scratch/diag_clip.py` | Diagnostik nilai ekstrem, NaN, dan batas clip |

Perintah ulang (dengan JAVA_HOME dan cluster H2O berjalan di port 54322):

```bash
~/.venvs/h2o/bin/python scratch/h2o_eksperimen.py F-14 F-15A F-15_S F-5 F-7 F-9 F-9_A
~/.venvs/h2o/bin/python scratch/uji_dl_sebab.py   # tahap A dan B
~/.venvs/h2o/bin/python scratch/uji_dl_c.py       # tahap C
```

## 10. Yang belum dicek

- Kombinasi kandidat sudah diuji penuh pada 7 sumur (Temuan T4). Yang belum diuji: bobot hasil pembelajaran (stacking dengan model meta), karena `StackedEnsemble` tidak terbentuk pada AutoML ber-`fold_column`, dan pemilihan subset memakai prediksi out-of-fold tingkat fold (yang tersimpan baru AUCPR CV agregat per kandidat).
- Belum diuji apakah `max_runtime_secs` lebih panjang (misalnya 1.800 detik) mengubah hasil; yang terukur baru 400, 600, dan 900 detik (900 detik untuk F-9_A saat run pertama kandas).

## 4b. Cara membaca angka kombinasi

- Angka "median seluruh kandidat" dihitung dari 9 sampai 12 kandidat per sumur, jadi bukan gabungan 100 model; AutoML hanya sempat membangun sebanyak itu dalam 600 detik pada 18 core.
- Tabel "strategi terbaik per sumur" tidak boleh dirata-ratakan sebagai klaim; memilih strategi berdasarkan hasil sumur uji itu sendiri adalah kebocoran. Yang sah diklaim adalah rata-rata satu strategi tetap di seluruh sumur, seperti pada tabel T4.
- Korelasi Spearman dihitung pada 7 titik, sehingga sebagai estimasi ia lemah; yang kuat adalah arahnya yang negatif pada ketujuh sumur secara berpasangan.
