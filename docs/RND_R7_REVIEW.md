# RND-R7: REVIEW R&D ATAS HASIL ENGINEER DAN INSTRUKSI RISET LANJUTAN

Kartu: `t_f366fdcf` · Board: `rnd-algo-2026` · Tanggal: 2026-10-27 (WIB)
Objek review: `docs/RND_E3_HASIL.md` (pilot hyd K-i) dan `docs/RND_E0_AUDIT_ENGINE.md` (audit 7 mode)
Workspace: `/mnt/d/Capstone 1(v2)`. Folder arsip `/mnt/d/Capstone 1` tidak disentuh.
Dokumen hulu yang dibaca: `docs/RND_ALGO_RESEARCH_PLAN.md` (§2 aturan angka, §6 gate), `docs/V9_EVAL_C_LAYERC.md` (tabel tier §1 dan §2.5), `code/v9_i1_pipeline.py` (REGISTRY), `scratch/v9_i1/v9_i1_RESULTS.json`.

Riset pendahuluan: scientific-critical-thinking, statistical-analysis, verification-mandatory.

- **scientific-critical-thinking**: dipakai untuk menilai validitas desain sebelum menilai hasil, yaitu memisahkan pertanyaan "apakah model gagal" dari pertanyaan "apakah alat ukurnya sah", memeriksa bias pembanding dan kebocoran pada baseline, serta menuntut setiap klaim disertai falsifier yang bisa gagal.
- **statistical-analysis**: dipakai untuk memastikan besaran yang dibandingkan berada pada satuan yang sama (menit teramati versus kalender, baris alarm versus kejadian alarm), untuk menolak rata-rata tunggal yang mencampur rezim, dan untuk melaporkan recall bersama laju alarm pada titik operasi yang sama.
- **verification-mandatory**: dipakai sebagai gerbang akhir, yaitu eksekusi ulang perhitungan Engineer dari kode dan data mentah, pembacaan JSON mentah alih-alih menyalin tabel dokumen, verifikasi DOI dua lapis (registrasi dan metadata), dan daftar eksplisit hal yang tetap belum terukur.

Riset pendahuluan: sequentialthinking, 6 pikiran (`mcp__sequentialthinking__sequentialthinking`, `thoughtNumber` 1 sampai 6, `thoughtHistoryLength` 6). Ringkas: (1) menetapkan bahwa yang dinilai lebih dulu adalah kesahan pembanding, bukan kebaikan model, (2) menguji hipotesis bahwa proksi `rule_lag` di baris 203 memakai label yang menintip masa depan dan menetapkan falsifier berupa rekonstruksi rule t0-1 dari bins, (3) menghitung konsekuensi angka bila pembanding diganti, (4) merancang eksperimen pembeda dua titik operasi alpha untuk menguji klaim bahwa recall bisa dipertahankan pada anggaran alarm, (5) memisahkan tiga kelas penyebab dengan bukti masing-masing, (6) menetapkan rekomendasi yang boleh dan tidak boleh dipakai sebagai dasar keputusan.

---

## 1. VONIS

**Hasil pilot TIDAK MEMUASKAN, tetapi tidak hanya karena modelnya.** Dua hal yang harus dibaca bersamaan:

1. Tidak ada finalis yang memenuhi gate A. Angka Engineer sendiri menyatakan itu, dan review ini mereproduksinya persis pada seed 42 (`--` tabel 3.1).
2. Alat ukur yang dipakai untuk membandingkan juga tidak sah. Pembanding "hybrid proxy" di `code/rnd_e3_pilot.py:203` dibangun dari label baris sebelumnya, yang jendelanya meluas sampai sembilan menit ke masa depan dari titik keputusan. Ketika pembanding dibangun ulang memakai rule t0-1 yang benar-benar lampau, hasilnya mereproduksi angka terbit hampir persis, dan pembanding itu lulus gate A di **0 dari 9 fold**, bukan 4 dari 9.

Karena itu vonis R&D adalah: **jangan naikkan tier, jangan ulangi eksperimen yang sama, dan perbaiki alat ukur lebih dulu.** Menjalankan model lain di atas pembanding yang salah hanya akan menghasilkan angka yang tidak bisa dibandingkan dengan apa pun.

Tier tetap `PERINGATAN-BERPENGAWAS` untuk hyd K-i. Gate C tidak dinilai (gate A gagal lebih dulu, E2 §5.4), gate B tetap BELUM TERUKUR.

---

## 2. YANG DINILAI DAN CARA MENILAI

| Butir | Isi |
|---|---|
| Klaim yang diuji | hyd K-i (status), detektor rig, label proksi residu SPPA |
| Pembanding yang diminta kartu | baseline hyd K-i terbit: P 0,72 sampai 0,95; FP 2.091 turun ke 927; FAR 14,6 sampai 58,4; delay tidak lebih dari 3,5 menit |
| Metode | eksekusi ulang perhitungan Engineer (`scratch/rnd/r7/r7_measure.py`, `r7_measure2.py`), rekonstruksi baseline dari bins, dan dua titik operasi alpha sebagai eksperimen pembeda |
| Data | `scratch/v9_d1/datasets/hyd_ki.csv.gz` (52.509 baris, 9 well, 50 kolom), bins per well di `scratch/v9_d1/bins/` |
| Lingkungan | `/home/neonti/.venvs/rnd_e3/bin/python` (Python 3.11.15), pustaka sama dengan run E3 |

Batas yang harus dibaca lebih dulu:

1. Review ini **tidak** mengubah kode Engineer. Semua pengukuran dilakukan oleh skrip baru di `scratch/rnd/r7/`.
2. Rekonstruksi baseline memakai fungsi label yang sama (`qcut` TFLO 10 bin, median/MAD per bin, `|z| > 2`) dari `code/v9_d1_03_rig_datasets.py:55-75`, lalu mengambil nilai bin `ts-1` sebagai sinyal rule. Ini meniru mesin rule t0-1, bukan menjalankan `v9_e_RULE_01_status.py` apa adanya.
3. Delay deteksi pada definisi `detection_stats` (`code/rnd_e3_pilot.py:82-103`) dihitung per blok positif berurutan. Definisi yang dipakai kampanye V9 bisa berbeda, jadi perbedaan delay di §3.2 tidak otomatis berarti angka lama salah.

---

## 3. VERIFIKASI ULANG ANGKA ENGINEER

### 3.1 A1 direproduksi persis

Eksekusi ulang A1 seed 42 dengan fungsi dan hyperparameter yang sama sekali lagi (`r7_measure2.py`, label `asis_alpha_E2`) memberi angka yang identik dengan tabel 4.2 `RND_E3_HASIL.md`, sampai empat desimal, untuk sembilan fold. Contoh: F-10 FAR24 86,7217 (dokumen 86,72), F-15A 543,4958 (543,50), F-9 0,0000, F-9_A 29,1840 (29,18). Alpha terpilih juga sama, yaitu 0,10, 0,10, 0,10, 0,20, 0,05, 0,20, 0,05, 0,05, 0,10.

Verifikasi positif: **hasil Engineer dapat direproduksi**, jadi angka E3 bukan artefak satu proses. Yang dipermasalahkan review ini bukan aritmetika Engineer, melainkan pilihan pembanding dan satuan metriknya.

| Besaran seed 42 | E3 (dokumen) | Ukur ulang R7 | Status |
|---|---|---|---|
| Median FAR24 A1 | 86,72 (median 9 fold seed 42) | 86,722 | cocok |
| Rentang FAR24 A1 | 0,00 sampai 543,50 | 0,000 sampai 543,496 | cocok |
| Recall rentang A1 | 0,0010 sampai 0,5057 | 0,0010 sampai 0,5057 | cocok |
| Median FAR24 semua seed | 63,29 (45 fold-run) | tidak dihitung ulang | BELUM DIVERIFIKASI |
| Gate A A1 seed 42 | 2 dari 9 | 2 dari 9 | cocok |

Sumber: `scratch/rnd/r7/r7_measure2.json` kunci `a1.asis_alpha_E2`, dibandingkan dengan `scratch/rnd/e3/e3_a_conformal_results.json`.

### 3.2 Baseline: angka terbit dapat direproduksi, proksi Engineer tidak

Ini temuan inti review. `code/rnd_e3_pilot.py:203` menulis:

```
rule_lag = np.concatenate([[0], y[:-1]])
```

`y` adalah label `y_hyd`, yaitu ada-tidaknya anomali di jendela `[t, t+10)`. Jadi `y(t-1)` memakai data sampai `t+9`. Pada titik keputusan `t`, sinyal itu memuat sembilan menit masa depan. Ia bukan proksi rule, dan ia bukan prediktor kausal.

Sebagai pembanding, `y_prev_hyd` yang dipakai persistence berbeda dan sah: `code/v9_d1_03_rig_datasets.py:106` menulis `prev_h = LBh.reindex(pd.Index(ts - W))`, jadi `y_prev` adalah label jendela `[t-10, t)` yang seluruhnya lampau. Persistence karena itu tidak bocor, sedangkan `rule_lag` bocor.

Falsifier yang saya jalankan: bangun ulang baseline memakai rule t0-1 yang benar, yaitu `anom` pada bin `ts-1` dari `scratch/v9_d1/bins/<well>.csv.gz` (`r7_measure.py`). Bila hipotesis bocor benar, angka harus kembali ke terbit.

| Besaran | Terbit (E2, E_RULE) | Rekonstruksi jujur R7 | Proksi E3 | Putusan |
|---|---|---|---|---|
| FP rule | 2.091 | **2.105** | tidak dihitung | cocok, selisih 0,67 persen |
| FP hybrid | 927 | **927** | **195** | jujur cocok persis, proksi meleset 4,75 kali |
| FAR24 hybrid | 14,6 sampai 58,4 | **14,624 sampai 58,431** | 2,774 sampai 19,313 | jujur cocok persis |
| Presisi hybrid | 0,72 sampai 0,95 | **0,7236 sampai 0,9484** | 0,9423 sampai 0,9903 | jujur cocok persis |
| Recall hybrid | 0,52 sampai 0,87 | **0,5247 sampai 0,8702** | 0,5921 sampai 0,8752 | jujur cocok persis |
| Fold lulus gate A | tidak dilaporkan | **0 dari 9** | 4 dari 9 | proksi menciptakan 4 fold palsu |
| Delay median | tidak lebih dari 3,5 menit | 1,0 sampai 10,0 | tidak diukur | **tidak tereproduksi, definisi berbeda** |

Sumber: `scratch/rnd/r7/r7_measure.json` kunci `baseline` dan `total_fp`, `r7_delay.json`.

Empat dari lima besaran terbit cocok persis, termasuk rentang FAR dan rentang presisi. Itu bukan kebetulan: konstruksi label dan bins yang dipakai memang sama. Kesimpulan yang bisa dipertanggungjawabkan: **angka terbit 2.091 dan 927 reproducible, dan yang tidak reproducible adalah proksi Engineer.**

### 3.3 A2: satu kejadian alarm dihitung sampai sepuluh baris

`code/rnd_e3_pilot.py:383-397` memetakan alarm per menit menjadi alarm per baris dengan `out[i] = int(al[lo:hi].max())` atas jendela `[lab_ts-10, lab_ts)`. Satu menit alarm karena itu menandai setiap baris yang jendelanya memuat menit itu, sehingga satu kejadian bisa muncul sebagai beberapa FP baris. Metrik baris lalu menghitung tiap baris sebagai satu FP.

Ukur ulang pada h=30 dengan reset (nilai yang dipilih di 9 dari 9 fold):

| Besaran | Satuan baris (E3) | Satuan kejadian (R7) | Rasio |
|---|---|---|---|
| Median FAR24 | 151,158 | 69,170 | 2,862 |
| Rentang FAR24 | 127,488 sampai 232,664 | 18,432 sampai 133,521 | 1,412 sampai 6,917 |
| Gate A lulus | 0 dari 9 | 0 dari 9 | tidak berubah |
| Menit alarm per well | tidak dilaporkan | 46 sampai 727 | informasi baru |

Sumber: `scratch/rnd/r7/r7_measure2.json` kunci `a2_kejadian`.

Status gate A tidak berubah karena 69,17 per 24 jam masih 11,5 kali anggaran. Tetapi besaran "21 sampai 38 kali anggaran" yang ditulis E3 §6.1 menjadi 3,1 sampai 22,3 kali pada satuan kejadian. Angka itu dipakai untuk menyimpulkan seberapa jauh A2 dari layak, jadi satuannya harus benar.

### 3.4 Fitur A1 memuat indeks waktu absolut

`code/rnd_e3_pilot.py:49-51` menyaring fitur hanya dengan membuang `LABEL_DERIVED` dan kolom non-numerik. Kolom `ts_bin` lolos, karena ia numerik dan tidak ada di daftar larangan. Hasil ukur: 41 fitur A1 dan **`ts_bin` termasuk di dalamnya** (`scratch/rnd/r7/r7_probe.json`, `ts_bin_in_feats: true`). Tanpa `ts_bin` fiturnya 40.

`ts_bin` adalah menit absolut sejak epoch kampanye. Nilainya berbeda jauh antar well (F-12 mulai 19.712.445, F-9_A mulai 20.776.616). Pada skema LOWO, model boleh memakai kolom itu untuk menghafal posisi waktu, dan posisi waktu berkorelasi dengan well. Ini bukan bukti kebocoran label, tetapi ia melanggar syarat bahwa fitur harus tersedia dan bermakna sama pada well baru.

---

## 4. PENILAIAN: MEMUASKAN ATAU TIDAK

### 4.1 Perbandingan pada satuan yang sama

| Kandidat | FAR24 median | Recall median | Presisi median | Fold lulus gate A (FAR tidak lebih dari 6) | Fold lulus gate A penuh (FAR dan recall tidak kurang dari 0,5) |
|---|---|---|---|---|---|
| Baseline persistence | 66,05 | 0,6791 | 0,7114 | 0 dari 9 | 0 dari 9 |
| Baseline hybrid, rekonstruksi jujur | 28,42 | 0,6519 | 0,8243 | 0 dari 9 | 0 dari 9 |
| Baseline hybrid, proksi E3 | 6,14 | 0,6648 | 0,9630 | 4 dari 9 | 0 dari 9 |
| A1 LightGBM + conformal, alpha aturan E2 | 86,72 | 0,0740 | 0,1084 | 2 dari 9 | 0 dari 9 |
| A1, alpha pada anggaran 1/240 | 2,72 | 0,0000 | tidak terdefinisi di 3 fold | 6 dari 9 | 0 dari 9 |
| A2 CUSUM, satuan kejadian | 69,17 | tidak dihitung pada satuan kejadian | tidak dihitung pada satuan kejadian | 0 dari 9 | 0 dari 9 |

Presisi dan recall A2 pada satuan baris adalah 0,4141 dan 0,4484. Keduanya tidak dipindahkan ke satuan kejadian di review ini, jadi sel itu ditulis apa adanya sebagai belum dihitung.

Sumber: `scratch/rnd/r7/r7_measure.json`, `r7_measure2.json`, `scratch/rnd/e3/e3_b_cusum_results.json`, dan `code/rnd_e3_pilot.py` untuk baseline persistence.

### 4.2 Putusan per kriteria kartu

| Kriteria kartu | Target | Hasil ukur | Putusan |
|---|---|---|---|
| Presisi dibanding baseline | P 0,72 sampai 0,95 | A1 0,0500 sampai 0,2119 (kecuali F-9 yang 1,0000 dengan 0 FP); A2 satuan baris 0,3200 sampai 0,6786 | **lebih buruk dari baseline** |
| Pemangkasan FP | 2.091 turun ke 927 | A1 total FP 5.427 pada seed 42 (jumlah 9 fold), A2 satuan kejadian 1.919 | **tidak memangkas, menambah** |
| FAR | 14,6 sampai 58,4 (baseline) | A1 0,00 sampai 543,50; A2 18,43 sampai 133,52 | **lebih buruk dan jauh lebih tidak stabil** |
| Delay | tidak lebih dari 3,5 menit | A1 deteksi dalam 10 menit 0,0000 sampai 0,7576; A2 tidak dilaporkan | **tidak memenuhi, dan tidak sebanding** |

Catatan penting: target pada kolom kedua bukan target yang harus dikalahkan, melainkan angka baseline yang gagal gate A. Baseline terbit pun FAR 14,6 sampai 58,4, artinya **gate A belum pernah dicapai oleh apa pun pada definisi ini.** Karena itu pertanyaan "apakah pilot memuaskan" harus dijawab dua lapis: pilot gagal, dan gate-nya juga belum pernah bisa dicapai.

---

## 5. KLASIFIKASI PENYEBAB

### 5.1 (a) Algoritma tidak cocok: terbukti, dengan angka

Bukti 1, ambang conformal terikat aritmetika pada alpha. Ambang adalah kuantil `1-alpha` dari skor negatif, sehingga laju alarm pada menit negatif mendekati alpha dan `FAR24` mendekati `alpha x 1440`. Gate A `FAR <= 6` karena itu setara dengan `alpha <= 1/240 = 0,00416667`. Ini bukan taksiran, ini identitas konstruksi ambang.

Bukti 2, dua titik operasi diukur, dan tidak ada titik yang memenuhi dua syarat sekaligus.

| Titik operasi | Median FAR24 | Median recall | Fold recall nol | Fold lulus FAR | Fold lulus FAR dan recall tidak kurang dari 0,5 |
|---|---|---|---|---|---|
| alpha aturan E2 (terpilih 0,05 sampai 0,20) | 86,722 | 0,0740 | 0 | 2 dari 9 | 0 dari 9 |
| alpha = 1/240 = 0,004167 | 2,718 | 0,0000 | **6 dari 9** | 6 dari 9 | 0 dari 9 |

Sumber: `scratch/rnd/r7/r7_measure2.json` kunci `a1.asis_alpha_E2` dan `a1.asis_alpha_budget`.

Bukti 3, pemisahan skor tipis. AUPRC A1 seed 42 adalah 0,1180 sampai 0,5172 dengan median 0,1549, sedangkan prevalensi fold 0,0832 sampai 0,2618. Lift di atas prevalensi karena itu kecil, dan pada anggaran alarm 0,42 persen ekor atas skor hampir tidak memuat positif. Ini definisi "algoritma tidak cocok" untuk masalah ini: bukan soal hyperparameter, melainkan tidak ada ambang yang memisahkan.

### 5.2 (b) Implementasi salah: terbukti, dengan bagian kode

| Kode | Cacat | Bukti | Dampak ke angka |
|---|---|---|---|
| `code/rnd_e3_pilot.py:203` | `rule_lag` memakai label baris sebelumnya, jendelanya menintip 9 menit masa depan | FP hybrid 195 lawan 927 pada rekonstruksi jujur | FAR pembanding 2,77 sampai 19,31 menjadi 14,62 sampai 58,43; fold lulus gate A 4 menjadi 0 |
| `code/rnd_e3_pilot.py:49-51` | `ts_bin` masuk 41 fitur | `r7_probe.json` `ts_bin_in_feats: true` | tanpa `ts_bin` AUPRC median 0,1549 menjadi 0,1384, FAR median 86,72 menjadi 121,91 |
| `code/rnd_e3_pilot.py:383-397` | alarm jendela 10 menit dihitung per baris, satu kejadian menjadi beberapa FP | rasio median 2,862, rentang 1,412 sampai 6,917 | median FAR24 A2 151,16 menjadi 69,17 |
| `code/rnd_e3_pilot.py:294-295` | `gate_A_lulus` hanya memeriksa FAR dan syarat 4 kali FP, tidak memeriksa recall | fold F-15_S recall 0,0010 dan F-9 recall 0,0473 ditandai "ya" | 2 fold berlabel "ya" menjadi 0 fold pada kriteria E2 penuh |

### 5.3 (c) Data tidak mendukung: terbukti, dengan angka

| Bukti | Angka | Konsekuensi |
|---|---|---|
| Cakupan waktu teramati per fold | 0,0171 sampai 0,6730 | hanya F-10 yang boleh disertifikasi menurut E2 §4.1 butir (d) |
| Label hyd adalah proksi residu SPPA | `code/v9_d1_03_rig_datasets.py:55-75`, `|z| > 2` | model belajar meniru ambang statistik, bukan fisika hidraulik |
| Baseline terbit sendiri gagal gate A | FAR 14,624 sampai 58,431 di 9 dari 9 well | gate A belum pernah tercapai, sehingga target pilot bukan target yang terbukti mungkin |
| Penyebut FAR memakai menit teramati | E0 K-4 | FAR antar well tidak sebanding karena cakupan berbeda 39 kali |

Putusan tiga kelas: **(a) dan (c) adalah penyebab utama, (b) adalah penyebab tambahan yang membuat pembanding tidak sah dan sebagian angka terlalu optimistis atau terlalu pesimistis.** Tidak ada satu kelas yang bisa dipakai sendirian untuk menutup kasus.

---

## 6. ENGINEER TERBUKTI SALAH

Tiga butir di bawah adalah kesalahan yang bisa ditunjuk bagian kodenya dan dampaknya sudah diukur. Dua butir pertama wajib diperbaiki sebelum run berikutnya, karena tanpa perbaikan itu angka apa pun tidak bisa dibandingkan.

### 6.1 R7-1: pembanding memakai label yang menintip masa depan (Kritis)

- Bagian kode: `code/rnd_e3_pilot.py:202-204`.
- Bukti: rekonstruksi rule t0-1 dari bins memberi FP rule 2.105 (terbit 2.091) dan FP hybrid 927 (terbit 927), sedangkan proksi memberi 195. Rentang FAR dan presisi hasil rekonstruksi sama persis dengan angka terbit.
- Dampak: FP pembanding 195 menjadi 927 (4,75 kali), FAR 2,77 sampai 19,31 menjadi 14,62 sampai 58,43, fold lulus gate A 4 menjadi 0, dan kesimpulan dokumen bahwa "baseline pun gagal" berubah menjadi "baseline terbit tidak pernah lulus gate A sama sekali".
- Perbaikan yang diminta: buang `rule_lag`. Hitung sinyal pra-label per menit dari `scratch/v9_d1/bins/<well>.csv.gz` dengan resep `hyd_bin_labels` yang sama, lalu ambil `anom` pada `ts-1`. Simpan fungsi itu sebagai satu fungsi bernama di `code/` supaya E0 dan E4 memakai definisi yang sama. Tambahkan assert: total FP hybrid pada 9 fold harus 927 lebih kurang 5 persen, kalau tidak, gagal.
- Catatan keadilan: kesalahan ini membuat pembanding **lebih kuat** dari kenyataan, sehingga ia memperkeras kegagalan model, bukan meringankannya. Tetap harus diperbaiki karena angka 195 dan 4 fold tidak boleh dipakai lagi.

### 6.2 R7-2: `ts_bin` dipakai sebagai fitur (Kritis untuk kesahan, bukan untuk performa)

- Bagian kode: `code/rnd_e3_pilot.py:49-51`.
- Bukti: `scratch/rnd/r7/r7_probe.json` menunjukkan `ts_bin` ada di antara 41 fitur.
- Dampak: AUPRC F-9 turun dari 0,5172 menjadi 0,3680 ketika `ts_bin` dibuang, AUPRC median 0,1549 menjadi 0,1384, dan fold lulus gate A 2 menjadi 0. Arahnya jelas: sebagian performa berasal dari indeks waktu, bukan dari kanal operasi.
- Perbaikan yang diminta: tambahkan `ts_bin` ke daftar kolom terlarang sebagai fitur. Jangan memakai hasil "tanpa `ts_bin` lebih buruk" sebagai alasan mempertahankannya, karena angka yang lebih buruk itu adalah angka yang jujur.

### 6.3 R7-3: satuan metrik A2 tidak sebanding dengan A1 dan baseline (Sedang)

- Bagian kode: `code/rnd_e3_pilot.py:383-397` dan `:436`.
- Bukti: rasio FAR baris terhadap FAR kejadian 1,412 sampai 6,917 dengan median 2,862.
- Dampak: A2 dilaporkan 21 sampai 38 kali anggaran, sedangkan pada satuan kejadian 3,1 sampai 22,3 kali. Perbandingan A1 (per baris, satu alarm satu FP) dengan A2 (per baris, satu alarm menjadi beberapa FP) tidak setara.
- Perbaikan yang diminta: untuk detektor berjendela, laporkan dua besaran berdampingan, yaitu FP kejadian dan FP baris, dan sebutkan mana yang dipakai untuk gate.

### 6.4 Yang TIDAK terbukti salah

- Aritmetika A1. Reproduksi identik empat desimal di sembilan fold.
- Label `y_prev_hyd` dan persistence. Sudah diperiksa: `y_prev` adalah label jendela `[t-10, t)`, seluruhnya lampau, jadi persistence tidak bocor.
- Klaim bahwa A2 sirkular. Dokumen sudah menyatakannya sendiri di §4.3, dan review ini menguatkannya, bukan menemukan hal baru.

---

## 7. EKSPERIMEN PEMBEDA YANG SUDAH DIJALANKAN

Empat eksperimen, semuanya memakai data dan fungsi yang sama dengan E3, sehingga hasilnya sebanding.

| # | Pertanyaan | Perlakuan | Hasil | Tafsir |
|---|---|---|---|---|
| P1 | Apakah pembanding E3 sah | ganti proksi dengan rule t0-1 dari bins | FP 2.105 dan 927, FAR 14,62 sampai 58,43 | proksi tidak sah, baseline terbit reproducible |
| P2 | Apakah recall bisa dipertahankan pada anggaran alarm | alpha 1/240 | FAR median 2,72, recall median 0,0000, 6 fold recall nol | tidak bisa, dua syarat E2 saling meniadakan |
| P3 | Apakah `ts_bin` menyumbang kinerja | buang `ts_bin` | AUPRC median 0,1549 menjadi 0,1384 | ya, dan itu alasan untuk membuangnya |
| P4 | Seberapa besar A2 dilebihkan | hitung pada satuan kejadian | median 151,16 menjadi 69,17 | dilebihkan 2,86 kali, gate A tetap gagal |

Sumber: `scratch/rnd/r7/r7_measure.json`, `scratch/rnd/r7/r7_measure2.json`, `scratch/rnd/r7/r7_delay.json`.
Waktu jalan: P1 dan P4 sekitar 10 detik, P2 dan P3 sekitar 150 detik untuk empat varian A1.

---

## 8. INSTRUKSI RISET LANJUTAN UNTUK ENGINEER (KARTU E4)

Berurut prioritas. Butir 1 sampai 3 wajib selesai sebelum run model apa pun dijalankan.

1. **Ganti pembanding (R7-1).** Pakai rule t0-1 dari bins. Kriteria selesai: FP rule 2.091 lebih kurang 5 persen dan FP hybrid 927 lebih kurang 5 persen pada 9 fold, dengan assert di skrip.
2. **Buang `ts_bin` dari fitur (R7-2).** Kriteria selesai: `assert "ts_bin" not in feats`, dan laporan menyebut 40 fitur.
3. **Satukan satuan metrik (R7-3).** Untuk setiap detektor, laporkan FP baris dan FP kejadian. Kriteria selesai: satu tabel dengan dua kolom satuan dan satu kolom "dipakai untuk gate".
4. **Perbaiki aturan titik operasi (R7-5).** Aturan "minimal 1 TP di setiap 8 fold dalam" secara struktural menolak alpha yang dibutuhkan gate A. Ganti menjadi: pilih alpha dari anggaran alarm (`alpha <= 1/240` untuk rig), lalu laporkan recall yang terjadi apa adanya, tanpa syarat TP minimum. Kriteria selesai: alpha terpilih selalu tidak lebih dari 1/240 dan dilaporkan bersama recall.
5. **Tulis ulang kriteria gate A agar bisa dinilai pada data ini.** Gate A sekarang memakai FAR per menit teramati (E0 K-4) sehingga well dengan cakupan 1,71 persen dinilai dengan besaran yang berbeda 39 kali dari well dengan cakupan 67,30 persen. Ubah menjadi FAR per 24 jam kalender ditambah syarat cakupan minimal 0,50, dan laporkan keduanya. Kriteria selesai: tabel gate A memuat kolom cakupan dan kolom FAR kalender.
6. **Jalankan A2 hanya sebagai pembanding sirkular.** Karena z SPPA membentuk label, A2 tidak boleh dipakai sebagai bukti kemampuan deteksi independen. Kalau tetap dijalankan, tulis satu baris di tabel hasil: "sirkular terhadap label, bukan bukti independen".
7. **Jangan jalankan A1b.** Varian itu melanggar E2 §2.3 L3. Kalau ingin mengukur batas atas, beri label "batas atas diagnostik" dan jangan masukkan ke hitungan fold lulus.

Yang **tidak** diminta: mengganti LightGBM dengan XGBoost atau CatBoost. Gejala yang diukur (AUPRC dekat prevalensi, recall nol pada anggaran alarm) adalah sifat pemisahan skor pada data ini, bukan sifat implementasi boosting tertentu. Mengganti merek boosting tanpa mengubah label, fitur, dan satuan metrik akan menghasilkan angka dengan bentuk yang sama.

---

## 9. ALGORITMA PENGGANTI YANG DIUSULKAN

Usulan di bawah ini dibedakan tegas antara yang **sudah terukur** dan yang **masih hipotesis**.

### 9.1 Usulan 1: dua tahap, kandidat dulu, klasifikasi kemudian (hipotesis, mekanisme jelas)

Mekanisme: tahap pertama mendeteksi perubahan pada residu SPPA/TFLO tanpa memakai label (CUSUM atau EVT streaming), tahap kedua mengklasifikasi hanya pada jendela kandidat. Alasan mekanis: anggaran alarm 1/240 habis karena model harus memeriksa 100 persen menit. Bila tahap pertama menyempitkan kandidat ke 1 persen menit, tahap kedua punya ruang 100 kali lebih besar untuk memisahkan kelas pada anggaran yang sama.

Dasar literatur: Page (1954) untuk CUSUM, Siffer (2017) untuk deteksi streaming berbasis nilai ekstrem, dan Tatbul (2018) untuk metrik presisi-recall berbasis rentang, yang memang dirancang agar satu kejadian tidak dihitung berkali-kali.

Yang belum terukur: berapa besar penyempitan kandidat yang bisa dicapai tanpa kehilangan onset. Ini harus diukur lebih dulu sebagai eksperimen kecil, bukan diasumsikan.

### 9.2 Usulan 2: conformal tetap dipakai, tetapi dengan titik operasi dari anggaran (mekanisme sudah terukur)

Yang sudah terukur: pada alpha 1/240, FAR median 2,72 dan gate A lulus 6 dari 9 (fitur as-is) atau 7 dari 9 (tanpa `ts_bin`). Yang gagal adalah recall, median 0,0000. Karena itu conformal bukan alat yang salah untuk mengendalikan laju alarm, ia hanya tidak bisa menciptakan pemisahan yang tidak ada. Kalau usulan 1 memberi skor yang lebih terpisah, conformal pada anggaran yang sama akan langsung bisa dipakai.

Dasar literatur: Angelopoulos (2021) dan Lei (2018) untuk jaminan cakupan tanpa asumsi distribusi.

### 9.3 Usulan 3: perbaiki label sebelum menambah model (wajib, bukan pilihan)

Label hyd adalah `|z| > 2` atas residu SPPA per 10 bin TFLO. Dua konsekuensi: model belajar meniru ambang statistik, dan A2 sirkular. Sebelum algoritma apa pun diuji lagi, R&D meminta audit label: berapa banyak positif yang bertahan bila ambang digeser ke `|z| > 2,5` atau `3`, dan apakah onset yang dipakai di `hyd` K-i masih muncul. Tanpa jawaban itu, peningkatan AUPRC tidak bisa dibedakan dari peningkatan kesetiaan meniru ambang.

Dasar literatur: Kaufman (2012) dan Kapoor (2023) untuk taksonomi kebocoran dan sirkularitas label.

### 9.4 Urutan kerja yang diusulkan

```
E4a  perbaiki 3 cacat alat ukur (R7-1, R7-2, R7-3)  -> tanpa model baru
E4b  audit label hyd (ambang 2 / 2,5 / 3)           -> menentukan apakah target bisa ada
E4c  ukur penyempitan kandidat tahap 1 (tanpa label)
E4d  baru jalankan model pada kandidat, alpha dari anggaran
```

E4a dan E4b tidak butuh model baru dan bisa selesai cepat. Menjalankan E4d lebih dulu berarti mengulang kesalahan yang sama dengan nama algoritma berbeda.

---

## 10. YANG TIDAK BOLEH DIPAKAI SEBAGAI DASAR KEPUTUSAN

1. Angka FP hybrid 195 dan "baseline lulus gate A di 4 fold". Keduanya berasal dari label yang menintip masa depan.
2. Klaim "baseline terbit tidak reproducible". Klaim itu salah, dan angka 927 serta rentang FAR 14,6 sampai 58,4 sudah direproduksi.
3. Angka FAR A2 pada satuan baris sebagai perbandingan langsung dengan A1.
4. Klaim bahwa A1 "hampir berhasil" karena lulus FAR di 2 fold. Pada kedua fold itu recall 0,0010 dan 0,0473.
5. Klaim bahwa CUSUM dapat mendeteksi hidraulik secara independen. z pembentuk label, jadi hasilnya sirkular.
6. Kenaikan tier dalam bentuk apa pun. Gate A gagal, gate C tidak dinilai, gate B belum terukur.

---

## 11. RUJUKAN DAN STATUS VERIFIKASI

Semua DOI diperiksa pada 2026-10-27 oleh `scratch/rnd/r7/r7_doi.py`: lapis 1 HEAD ke `https://doi.org/<doi>` tanpa mengikuti redirect, lapis 2 metadata `api.crossref.org` atau `api.datacite.org`. Hasil: 8 dari 8 terdaftar (HTTP 302), 8 dari 8 metadata terjawab (HTTP 200).

| Penulis pertama | Tahun | Judul | DOI | Lapis 1 | Lapis 2 | Status |
|---|---|---|---|---|---|---|
| Kaufman | 2012 | Leakage in Data Mining: Formulation, Detection, and Avoidance | 10.1145/2382577.2382579 | 302 | 200 Crossref, penulis dan tahun cocok | TERVERIFIKASI |
| Kapoor | 2023 | Leakage and the reproducibility crisis in machine-learning-based science | 10.1016/j.patter.2023.100804 | 302 | 200 Crossref, judul dan tahun cocok | TERVERIFIKASI |
| Saito | 2015 | The Precision-Recall Plot Is More Informative than the ROC Plot When Evaluating Binary Classifiers on Imbalanced Datasets | 10.1371/journal.pone.0118432 | 302 | 200 Crossref, judul dan tahun cocok | TERVERIFIKASI |
| Angelopoulos | 2021 | A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification | 10.48550/arXiv.2107.07511 | 302 | 200 DataCite (tahun cocok, judul kosong di record); judul dicek di `arxiv.org/abs/2107.07511` | TERVERIFIKASI (judul dari halaman arXiv) |
| Lei | 2018 | Distribution-Free Predictive Inference for Regression | 10.1080/01621459.2017.1307116 | 302 | 200 Crossref, penulis dan tahun cocok | TERVERIFIKASI |
| Tatbul | 2018 | Precision and Recall for Time Series | 10.48550/arXiv.1803.03639 | 302 | DataCite tidak menjawab dalam 20 detik; judul dicek di `arxiv.org/abs/1803.03639` | TERVERIFIKASI (registrasi dan halaman arXiv), metadata register BELUM TERVERIFIKASI |
| Page | 1954 | Continuous Inspection Schemes | 10.1093/biomet/41.1-2.100 | 302 | 200 Crossref, penulis dan tahun cocok | TERVERIFIKASI |
| Siffer | 2017 | Anomaly Detection in Streams with Extreme Value Theory | 10.1145/3097983.3098144 | 302 | 200 Crossref, judul dan tahun cocok | TERVERIFIKASI |

Koreksi yang tercatat terbuka: percobaan pertama memakai `10.48550/arXiv.1803.03635` untuk Tatbul (2018). Pemeriksaan judul di `arxiv.org/abs/1803.03635` menunjukkan DOI itu milik "The Lottery Ticket Hypothesis". DOI yang benar adalah `10.48550/arXiv.1803.03639`. Tanpa pemeriksaan judul, rujukan itu akan lolos sebagai "terdaftar" padahal menunjuk paper yang salah. DOI yang salah tidak dipakai di dokumen ini.

Catatan kejujuran: tidak satu pun rujukan di atas dipakai untuk mengklaim ambang operasional. Ambang FAR 6 per 24 jam dan 1 alarm per menit tetap KONVENSI internal yang tercatat di `RND_PROVENANCE_LEDGER.md`, bukan hasil standar.

---

## 12. CARA REPRODUKSI

```
cd "/mnt/d/Capstone 1(v2)"
PY=/home/neonti/.venvs/rnd_e3/bin/python
$PY scratch/rnd/r7/r7_probe1.py     # daftar fitur, cek ts_bin          ~15 detik
$PY scratch/rnd/r7/r7_measure.py    # baseline jujur + A2 baris/kejadian ~10 detik
$PY scratch/rnd/r7/r7_measure2.py   # A2 kejadian + 4 varian A1         ~150 detik
$PY scratch/rnd/r7/r7_delay.py      # delay baseline jujur              ~10 detik
$PY scratch/rnd/r7/r7_doi.py        # verifikasi DOI 2 lapis            ~26 detik
$PY scratch/rnd/r7/r7_ledger.py     # tulis baris ledger + assert
```

Semua skrip hanya membaca `scratch/v9_d1/` dan `code/`, dan hanya menulis ke `scratch/rnd/r7/` serta bagian R7 di `docs/RND_PROVENANCE_LEDGER.md`.

Berkas hasil: `r7_probe.json`, `r7_measure.json`, `r7_measure2.json`, `r7_measure2.log`, `r7_delay.json`, `r7_doi.json`. Bagian R7 di ledger berisi 44 baris (`R7-001` sampai `R7-044`) dengan 28 baris RUN-KITA, 11 baris DERIVASI, 1 baris KONVENSI, dan 4 baris BELUM-TERUKUR. Setiap baris RUN-KITA dan DERIVASI di-assert terhadap path JSON sebelum ditulis, sehingga menjalankan ulang `r7_ledger.py` tidak menggandakan baris dan tidak bisa menulis angka yang tidak cocok.

---

## 13. RINGKASAN 5 BARIS

1. Hasil pilot tidak memuaskan dan tidak dapat dinaikkan tier: gate A gagal untuk semua finalis, dan angka Engineer direproduksi persis pada seed 42 (FAR median 86,722, gate A 2 dari 9).
2. Pembanding yang dipakai pilot tidak sah: `code/rnd_e3_pilot.py:203` memakai label baris sebelumnya yang menintip 9 menit masa depan, sehingga FP hybrid 195 padahal rekonstruksi jujur dari bins memberi 927 dan FAR 14,624 sampai 58,431 yang persis sama dengan angka terbit.
3. Penyebab diklasifikasikan dan terukur: algoritma tidak cocok (pada alpha 1/240 recall median 0,0000 dengan 6 fold recall nol), implementasi salah (3 cacat dengan dampak angka), dan data tidak mendukung (cakupan 1,71 sampai 67,30 persen, label proksi, baseline terbit sendiri gagal gate A).
4. Eksperimen pembeda sudah dijalankan dan memberi arah: FAR bisa diturunkan ke median 2,72, tetapi hanya dengan recall nol, sehingga prioritas perbaikan bukan mengganti boosting melainkan memperbaiki alat ukur, membuang `ts_bin`, menyatukan satuan metrik, dan mengaudit label.
5. Tier tidak berubah, `PERINGATAN-BERPENGANWAS` untuk hyd K-i, dan kartu E4 diberi 3 perbaikan wajib lebih dulu sebelum run model apa pun.

## 14. DAFTAR YANG BELUM TERVERIFIKASI

1. Median FAR 63,29 pada 45 fold-run semua seed tidak dihitung ulang. Review ini memverifikasi seed 42 saja.
2. Delay baseline terbit tidak lebih dari 3,5 menit tidak tereproduksi. Rekonstruksi jujur memberi median 1,0 sampai 10,0 menit per well, dan penyebabnya kemungkinan perbedaan definisi antara `detection_stats` dan resep E_STAT. Angka delay terbit tetap BELUM TERUKUR pada definisi R7.
3. Dampak pembuangan `ts_bin` hanya diukur pada seed 42, bukan pada 5 seed.
4. Usulan dua tahap (§9.1) belum diukur sama sekali. Penyempitan kandidat tanpa kehilangan onset masih hipotesis.
5. Audit label hyd pada ambang 2,5 dan 3 belum dijalankan.
6. Metadata DataCite untuk `10.48550/arXiv.1803.03639` tidak menjawab dalam 20 detik, sehingga judul Tatbul (2018) diverifikasi dari halaman arXiv, bukan dari register.
7. Gate B tetap BELUM TERUKUR, karena tidak ada data durasi inspeksi per alarm di repo ini.
