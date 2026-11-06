# RND-R5: DETEKSI PERUBAHAN (DRIFT) DAN ANOMALI TANPA LABEL

Kartu: `t_56d8d11d` · Board: `rnd-algo-2026` · Tanggal: 2026-10-27 (WIB)
Workspace: `/mnt/d/Capstone 1(v2)` · Arsip `/mnt/d/Capstone 1` tidak disentuh
Dokumen rujukan: `docs/RND_ALGO_RESEARCH_PLAN.md` §2 dan §6, `docs/RND_D0_DATA_FEASIBILITY.md`,
`docs/RND_P0_PARAMETER.md`, `docs/V9_EVAL_C_LAYERC.md` (tabel tier), `code/v9_i1_pipeline.py` (REGISTRY),
`scratch/v9_i1/v9_i1_RESULTS.json`
Skrip dan hasil mentah kartu ini: `scratch/rnd_r5/` (semua angka di bawah dapat dijalankan ulang)

Riset pendahuluan: literature-review, paper-lookup, aeon, scikit-learn, scientific-critical-thinking, verification-mandatory

Cara tiap skill dipakai:
- **literature-review** dipakai untuk menyusun pencarian bertahap (metode dulu, lalu aplikasi PdM pengeboran) dan untuk menolak rujukan yang tidak dapat dibuka, bukan mengumpulkan sitasi sebanyak mungkin.
- **paper-lookup** dipakai untuk resolusi DOI lapis kedua lewat Crossref (`api.crossref.org/works/<doi>`), karena halaman penerbit menolak host ini (HTTP 403), sehingga penulis, tahun, judul, jurnal, dan halaman tetap dapat diverifikasi dari rekaman resmi.
- **aeon** dipakai sebagai acuan taksonomi dan nama estimator untuk deteksi anomali dan segmentasi deret waktu (STOMP/matrix profile, ClaSP, detektor titik perubahan), sehingga metode yang diusulkan memakai nama yang sudah mapan, bukan istilah karangan.
- **scikit-learn** dipakai untuk memilih estimator tanpa label yang benar (novelty detection: `IsolationForest`, `LocalOutlierFactor(novelty=True)`, `OneClassSVM`), termasuk aturan bahwa penskalaan dan pelatihan hanya boleh pada baseline, bukan pada seluruh deret.
- **scientific-critical-thinking** dipakai untuk memisahkan klaim yang benar-benar diukur dari klaim yang hanya tampak masuk akal, khususnya menolak "recall tinggi" sebagai bukti deteksi ketika laju alarm dasar tidak dilaporkan.
- **verification-mandatory** dipakai untuk gerbang akhir: setiap angka punya berkas dan perintah, setiap DOI dicoba dibuka dan status HTTP dicatat, dan semua yang gagal diverifikasi ditulis sebagai BELUM TERVERIFIKASI.

Riset pendahuluan: sequentialthinking, 5 pikiran (`mcp__sequentialthinking__sequentialthinking`, thoughtNumber 1 s.d. 5, `thoughtHistoryLength` 5).
Ringkas: (1) kerangka kartu dan batas keras provenance, (2) koreksi satuan `ts_bin` yang membatalkan percobaan pertama dan pembongkaran recall palsu, (3) pemetaan dua rezim data (tool_wear skala detik di bengkel lawan rig skala menit antar well), (4) protokol evaluasi anomali tanpa label yang hanya mengklaim tiga hal terukur, (5) gerbang tulis: apa yang diklaim, apa yang ditandai belum terukur, dan status verifikasi DOI.

---

## 0. BATAS DAN DEFINISI

Kartu ini meminta dua hal yang sering dicampur, maka dipisah tegas:

| Istilah | Definisi operasional di dokumen ini |
|---|---|
| **Deteksi perubahan (change detection)** | Menguji apakah parameter distribusi bergeser pada satu deret, dengan asumsi ada periode acuan bersih. Keluaran: titik atau episode perubahan. Metode: CUSUM, Page-Hinkley, BOCPD, ADWIN, uji KS. |
| **Drift antar well** | Perbedaan distribusi antara dua sumber berbeda (well, alat, atau run), tanpa asumsi mana yang benar. Keluaran: ukuran jarak distribusi. Metode: uji KS dua sampel, jarak distribusi pada fitur. |
| **Anomali tanpa label** | Memberi skor kelainan pada satu observasi tanpa label positif, hanya dengan contoh "normal" (baseline). Keluaran: peringkat, bukan kelas. Metode: Isolation Forest, LOF, autoencoder, one-class SVM, matrix profile. |
| **Klaim palsu** | Pernyataan kinerja (recall, akurasi, "berhasil mendeteksi") yang tidak disertai laju alarm dasar, jumlah positif, atau mekanisme yang dapat diuji. |

Dua rezim data yang tidak boleh dicampur (mengikuti D-A7 di `docs/V9_EVAL_C_LAYERC.md`):

| Rezim | Sumber | Skala waktu | Konsekuensi metode |
|---|---|---|---|
| **Bengkel (tool_wear)** | Eksperimen 4 alat, 8 run, label regime dalam run | Detik (TLead terukur 20 s.d. 36 detik) | Detektor harus bekerja pada horizon detik dan dikalibrasi per alat |
| **Rig (vib, ssi, shk, stuck, hyd, bit_wear)** | Well Volve dan dataset USROP | Menit, laju sampel kanal maksimum 0,3333 Hz | Detektor bekerja pada jendela menit, kalibrasi per well, tidak boleh transfer ke bengkel atau sebaliknya |

Batas yang diakui sejak awal: tidak ada satu pun angka di dokumen ini yang berasal dari data rig berlabel sempurna. Label `y_hyd` adalah residu SPPA (proxy), dan itu dibawa apa adanya dari V9.

---

## 1. DETEKSI PERUBAHAN: PERBANDINGAN METODE

Skor 1 s.d. 5 pada tabel ini adalah **penilaian rekayasa** (kelas KONVENSI, bukan pengukuran), dengan kriteria yang dinyatakan lebih dulu supaya dapat dibantah:

- **Kebutuhan data**: 5 = cukup baseline pendek dan longgar; 1 = butuh deret panjang bersih dan prior yang tidak dimiliki.
- **Biaya**: 5 = hitung sekali lewat, O(n), tanpa pustaka berat; 1 = inferensi mahal per titik atau butuh penyetelan berat.
- **Interpretabilitas**: 5 = parameter dan ambang punya arti fisik yang bisa dijelaskan ke operator; 1 = kotak hitam.

| Metode | Kebutuhan data | Biaya | Interpretabilitas | Skor data | Skor biaya | Skor interpretasi | Peran usulan |
|---|---|---|---|---|---|---|---|
| **CUSUM** (Page 1954) | Baseline bersih untuk median dan sigma; sebaiknya ≥ 240 menit kontigu (konvensi kami) | O(n), satu lintasan, dua akumulator | Tinggi: `k` = kelipatan sigma, `h` = ambang akumulasi, dapat dibaca sebagai "berapa sigma kumulatif" | 4 | 5 | 5 | **Dipakai** untuk regime tool_wear per alat dan untuk pemantauan level kanal per well, setelah laju alarmnya diukur pada baseline nyata |
| **Page-Hinkley** (Hinkley 1971) | Sama seperti CUSUM | O(n) | Tinggi: `delta` = toleransi pergeseran, `lambda` = ambang | 4 | 5 | 5 | **Dipakai** sebagai pembanding CUSUM; lebih konservatif pada data berautokorelasi tinggi karena akumulator direset saat alarm |
| **BOCPD** (Adams dan MacKay 2007) | Prior run-length, model peluang per segmen, deret cukup panjang untuk posterior stabil | Mahal: pemangkasan run-length wajib, O(n·H) per titik | Sedang: posterior run-length bisa digambar, tetapi prior adalah asumsi yang tidak dapat diuji dari data kami | 2 | 2 | 3 | **Ditunda**. Tidak dijalankan pada gelombang ini. Prasyarat: baseline kontigu jauh lebih panjang dari 361 menit (maksimum terukur kami) |
| **ADWIN** (Bifet dan Gavaldà 2007) | Jendela adaptif, tanpa periode acuan eksplisit | O(n) amortized dengan pemangkasan bucket | Sedang: lebar jendela dapat dibaca sebagai "seberapa lama rezim ini bertahan" | 4 | 4 | 3 | **Diusulkan untuk tool_wear**, karena tidak menuntut baseline bersih panjang. **Belum dijalankan** (BELUM TERUKUR) |
| **Uji KS dua sampel** (Massey 1951) | Dua cuplikan; tidak butuh asumsi normalitas | O(n log n) | Tinggi: `D` = jarak maksimum CDF, mudah dijelaskan | 5 | 5 | 4 | **Dipakai** untuk drift antar well dan drift dalam well (paruh awal lawan paruh akhir). Bukan detektor waktu-nyata, tetapi alat kalibrasi ambang |

### 1.1 Pilihan untuk regime tool_wear (data 1 detik)

**Pilihan utama: CUSUM per alat dengan `h` dikalibrasi per alat, ditambah ADWIN sebagai pembanding.**
Alasan yang bisa diuji: label tool_wear sudah menunjukkan regime berubah di dalam run, TLead terukur 20 s.d. 36 detik, dan presisi biner 0,50 pada 4 alat baru. Pada kondisi itu, menuntut baseline panjang tidak realistis, sedangkan menuntut ambang global sudah terbukti gagal (ambang RF vib menyebar 119 kali antar well, lihat `docs/V9_EVAL_C_LAYERC.md` §1). Jadi kalibrasi harus per alat, dan detektor harus dapat menjelaskan "kapan" bukan hanya "apakah".

**Bukan BOCPD untuk tool_wear gelombang ini.** BOCPD menuntut prior run-length yang berarti; dengan run bengkel yang pendek, posterior akan didominasi prior, sehingga hasilnya mengukur prior kita, bukan data. Ini alasan menolak, bukan alasan malas.

### 1.2 Pilihan untuk drift antar well (rig)

**Pilihan utama: uji KS dua sampel sebagai alat keputusan, bukan CUSUM global.**
Alasannya terukur dan ada di §2.3: dari 10 pasangan well, 10 pasangan berbeda distribusi secara nyata dengan `D` median 0,986. Ketika dua well hampir tidak berbagi nilai sama sekali, satu ambang global tidak punya arti. Yang dibutuhkan bukan detektor yang lebih pintar, melainkan keputusan operasional: kalibrasi per well, dan uji KS sebagai gerbang sebelum memakai ambang pinjaman.

**CUSUM tetap dipakai di dalam well**, untuk memantau pergeseran level satu kanal pada satu well, dan **bukan** dipakai untuk membandingkan antar well.

---

## 2. HASIL UKUR PADA DATA NYATA (hyd K-i, 9 well)

Sumber: `scratch/v9_d1/datasets/hyd_ki.csv.gz` (52.509 baris, 9 well, 50 kolom).
Perintah: `python3 scratch/rnd_r5/measure_drift_v2.py` (3,3 detik pada host ini).
Hasil: `scratch/rnd_r5/drift_measured_v2.json` (`generated_at` 2026-10-27 03:56:09).
Kanal yang diuji: `TQA_mean`. Z = (x - median) / (1,4826 · MAD) dari baseline. CUSUM `k` = 0,5 sigma, `h` = 5 sigma. Page-Hinkley `delta` = 0,005 sigma, `lambda` = 50 sigma. Episode alarm digabung bila jaraknya ≤ 30 menit. Baseline bersih = blok kontigu dengan seluruh `y_hyd` = 0 dan panjang ≥ 240 menit.

### 2.0 Koreksi satuan yang membatalkan percobaan pertama

Percobaan pertama kartu ini (`scratch/rnd_r5/measure_drift.py`, hasil `drift_far_measured.json`) menyimpulkan **0 dari 9 well punya baseline 600 menit**, karena blok kontigu terpanjangnya dilaporkan hanya 6 s.d. 28 menit. Itu **artefak satuan, bukan sifat data**. Bukti:

- `ts_bin` adalah **indeks menit** (epoch menit), bukan detik. Selisih antar baris berturut-turut bernilai 1 pada mayoritas mutlak pasangan (F-10: 7.483 dari 7.570 pasangan), dan rentang F-10 = 20.683.425 - 20.672.177 = 11.248 menit = 187,5 jam.
- Percobaan pertama memetakan grid dengan langkah 60 pada deret berindeks menit, sehingga setiap blok pecah menjadi satu titik.

Bukti mentah: `scratch/rnd_r5/grid_structure.json` (perintah `python3 scratch/rnd_r5/grid_check.py`). Semua angka pada §2 memakai satuan yang sudah dikoreksi; file `drift_far_measured.json` **tidak dipakai** sebagai sumber angka di dokumen ini.

### 2.1 Baseline yang tersedia (batas data, bukan batas metode)

| Well | Baris | Baseline bersih dipakai (menit) | Status |
|---|---|---|---|
| F-10 | 7.571 | 257 | dipakai |
| F-14 | 10.401 | 358 | dipakai |
| F-15A | 6.156 | 284 | dipakai |
| F-15_S | 8.355 | 297 | dipakai |
| F-9_A | 2.206 | 361 | dipakai |
| F-12 | 7.390 | tidak ada | blok kontigu terpanjang 504 menit, tetapi tidak ada 240 menit berturut-turut yang seluruh labelnya 0 |
| F-5 | 6.332 | tidak ada | blok kontigu terpanjang 418 menit, syarat label bersih tidak terpenuhi |
| F-7 | 2.482 | tidak ada | blok kontigu terpanjang 171 menit |
| F-9 | 1.616 | tidak ada | blok kontigu terpanjang 97 menit |

Catatan definisi: "blok kontigu" berarti baris yang `ts_bin`-nya berselisih tepat 1 menit tanpa celah. Pada well yang dipakai, nilai baseline adalah panjang blok bersih terpanjang. Pada well yang tidak dipakai, angka yang ditulis adalah blok terpanjang yang ditemukan sebelum syarat label diterapkan.

**5 dari 9 well** punya baseline bersih kontigu ≥ 240 menit, dengan rentang 257 s.d. 361 menit (median 297). Artinya: untuk detektor yang menuntut periode acuan "bersih", bahan acuan hanya tersedia untuk sebagian well, dan panjangnya di bawah 6,1 jam. Ini pembatas yang harus ditulis di setiap klaim kinerja detektor pada rig.

### 2.2 Laju alarm palsu pada baseline nyata

| Well | Baseline (menit) | CUSUM episode | CUSUM FAR / 24 jam | PH episode | PH FAR / 24 jam | ac1 | `h` hasil kalibrasi paruh awal | Episode paruh akhir pada `h` itu |
|---|---|---|---|---|---|---|---|---|
| F-10 | 257 | 3 | 16,81 | 0 | 0,00 | 0,9779 | 40 | 0 |
| F-14 | 358 | 1 | 4,02 | 2 | 8,04 | 0,9954 | 4 | 1 |
| F-15A | 284 | 2 | 10,14 | 2 | 10,14 | 0,9948 | 60 | 1 |
| F-15_S | 297 | 2 | 9,70 | 1 | 4,85 | 0,9765 | 60 | 0 |
| F-9_A | 361 | 2 | 7,98 | 3 | 11,97 | 0,9865 | 60 | 0 |
| **Median** | 297 | 2 | **9,70** | 2 | **8,04** | **0,987** | 60 | 3 dari 5 well bersih |

Bacaan yang sah:
1. Pada ambang konvensional (`k` = 0,5 sigma, `h` = 5 sigma), CUSUM menghasilkan **4,02 s.d. 16,81 episode per 24 jam** baseline, dan Page-Hinkley **0 s.d. 11,97**. Keduanya **melampaui gerbang FAR ≤ 6 per 24 jam** (plan §6) di mayoritas well. Jadi ambang konvensional tidak boleh dipakai apa adanya untuk alarm rig.
2. `ac1` = **0,9765 s.d. 0,9954**. Asumsi dasar ARL Gaussian (sampel bebas) **gugur**. Setiap angka ARL dari buku teks tidak berlaku di sini, dan itu alasan mengapa FAR diukur pada baseline nyata, bukan dihitung dari rumus.
3. Kalibrasi transfer hanya berhasil di **3 dari 5 well** (F-10, F-15_S, F-9_A bersih pada paruh kedua). Dua well gagal (F-14 dan F-15A masing-masing 1 episode), sehingga `h` yang dikalibrasi pada paruh awal tidak otomatis aman pada paruh berikutnya di well yang sama. Ini bukti langsung bahwa drift **di dalam well** ada, bukan hanya antar well.

### 2.3 Drift antar well dan dalam well (uji KS)

Uji KS dua sampel pada nilai `TQA_mean` baseline:

| Perbandingan | Hasil |
|---|---|
| Antar well (10 pasangan) | `D` median **0,986**, minimum 0,723, maksimum 1,000; **10 dari 10 pasangan** p < 0,05 |
| Dalam well, paruh awal lawan paruh akhir (5 well) | `D` median **0,211**; **4 dari 5 well** p < 0,05; terbesar F-14 `D` = 0,9777 |

Catatan kehati-hatian yang wajib dibaca bersama angka ini: p asimtotik mengasumsikan sampel bebas dan kontinu, sedangkan deret ini berautokorelasi (`ac1` ≈ 0,98). Karena itu **`D` dipakai sebagai ukuran jarak**, dan p hanya sebagai penunjuk arah. Klaim yang boleh dibuat: "distribusi `TQA_mean` berbeda tajam antar well". Klaim yang tidak boleh dibuat: "perbedaan ini signifikan secara statistik dengan p = 0,0000", karena p di sini tidak valid untuk deret berautokorelasi.

### 2.4 Perangkap yang tertangkap: recall tinggi karena detektor macet menyala

Ketika CUSUM dijalankan pada **seluruh deret** (parameter dari baseline, bukan hanya di dalam baseline), dengan 4.281 menit positif `y_hyd` pada lima well yang dipakai, hasilnya:

| Well | Recall horizon 10 menit (CUSUM) | Recall horizon 10 menit (PH) | Menit alarm di luar baseline | Menit di luar baseline | Laju alarm di luar baseline (per jam) |
|---|---|---|---|---|---|
| F-10 | 0,9986 | 0,0000 | 7.312 | 7.314 | 59,98 |
| F-14 | 0,9988 | 0,6231 | 10.042 | 10.043 | 59,99 |
| F-15A | 0,9857 | 0,9069 | 5.853 | 5.872 | 59,81 |
| F-15_S | 1,0000 | 0,5227 | 8.058 | 8.058 | 60,00 |
| F-9_A | 0,7523 | 0,2387 | 1.608 | 1.845 | 52,29 |

Recall CUSUM 0,75 s.d. 1,00 terlihat sangat baik. Angka itu **bukan bukti deteksi**. Buktinya ada di kolom berikutnya: CUSUM menyala pada **52,29 s.d. 60,00 menit alarm per jam** di luar baseline, artinya praktis **setiap menit menyala**. Detektor yang selalu menyala otomatis "menangkap" setiap onset. Ini contoh kanonik klaim palsu yang harus ditolak, dan alasan aturan di §3.2: recall tidak boleh dilaporkan tanpa laju alarm atau presisi.

Page-Hinkley, yang mereset akumulator saat alarm, tidak macet: recall 0,24 s.d. 0,91 dengan laju alarm yang jauh lebih terkendali. Untuk data berautokorelasi tinggi seperti ini, **PH lebih jujur daripada CUSUM tanpa mekanisme reset**.

### 2.5 Uji anomali tanpa label (realisasi)

Skrip: `scratch/rnd_r5/anomaly_unsup.py`, dijalankan dengan `scratch/rnd_r5/.venv/bin/python` (scikit-learn 1.9.1, numpy melalui wheel yang sama).
Protokol: 32 fitur (8 kanal × mean, std, slope, last), detektor dilatih **hanya** pada baseline bersih tiap well, `contamination` = 0,01, ukuran fit maksimum 1.500 baris. Label `y_hyd` **tidak** dipakai saat latih, hanya setelah skor keluar. Hasil lengkap ada di §2.5.1.

### 2.5.1 Hasil ukur anomali tanpa label

Berkas hasil: `scratch/rnd_r5/anomaly_unsup.json` (`generated_at` 2026-10-27 03:58:56, `EXIT=0` pada `scratch/rnd_r5/anomaly_run.log`). Pustaka: scikit-learn 1.9.1. Fitur: 32 kolom (8 kanal × mean, std, slope, last), `contamination` = 0,01, batas fit 1.500 baris baseline per well.

**Batas cakupan lebih dulu.** Syarat fitur lengkap (semua 32 kolom tidak kosong) memotong well yang dapat dipakai dari 5 (pada uji satu kanal §2.2) menjadi **2 well**, yaitu F-10 dan F-15_S. Well yang gugur: F-14, F-15A, F-9_A (blok bersihnya tidak lengkap pada 32 fitur), F-12, F-5, F-7, F-9 (tidak punya blok bersih ≥ 240 menit). Jadi setiap angka di bawah adalah **n = 2 well**, bukan 9. Ini keterbatasan bukti, bukan hasil yang boleh digeneralisasi.

| Detektor | Laju alarm pada baseline (median) | Episode alarm baseline | FAR / 24 jam (per well) | Recall horizon 10 menit (median) | Presisi alarm-menit (median) | Menit alarm total (F-10 / F-15_S) |
|---|---|---|---|---|---|---|
| Isolation Forest | 0,0109 | 2 | 11,21 / 9,70 | 0,6131 | 0,2240 | 1.353 / 6.096 |
| LOF | 0,0089 | 1 s.d. 2 | 5,60 / 9,70 | 0,9970 | 0,2032 | 5.920 / 7.896 |
| One-Class SVM | 0,0665 | 2 s.d. 3 | 11,21 / 14,55 | 1,0000 | 0,2007 | 6.167 / 8.024 |
| Autoencoder (MLP, error rekonstruksi) | 0,0109 | 1 s.d. 2 | 5,60 / 9,70 | 1,0000 | 0,2011 | 6.154 / 8.006 |
| Matrix profile (TQA, jendela 60 menit, pada baseline saja) | fraksi diskord 0,0101 / 0,0126 | 1 | tidak dihitung | tidak diukur | tidak diukur | 2 / 3 titik diskord |

Uji transfer lintas well (latih di well A, uji laju alarm pada baseline well B), hanya 2 pasangan karena hanya 2 well yang lolos:

| Detektor | Laju alarm pada well lain (median) | Maksimum |
|---|---|---|
| Isolation Forest | 0,5000 | 1,0000 |
| LOF | 1,0000 | 1,0000 |
| One-Class SVM | 1,0000 | 1,0000 |
| Autoencoder | 1,0000 | 1,0000 |

Bacaan yang sah, dan yang tidak:

1. **Kepatuhan contamination.** Isolation Forest dan autoencoder menghasilkan laju alarm 0,0109 pada baseline, dekat dengan 0,01 yang diminta. **One-Class SVM menghasilkan 0,0665**, yaitu 6,65 kali parameter yang diminta; `nu` adalah batas atas proporsi outlier, bukan kalibrasi, sehingga tidak boleh dipakai untuk menetapkan laju alarm.
2. **Recall tinggi yang menipu, lagi.** LOF dan autoencoder memberi recall 0,997 s.d. 1,000, tetapi menyalakan 5.920 dari 6.408 menit (F-10) dan 7.896 dari 8.300 menit (F-15_S). Presisi alarm-menit hanya 0,20, artinya sekitar 80% menit alarm tidak berada dalam 10 menit sebelum onset. Pola ini identik dengan kegagalan CUSUM di §2.4, dan menegaskan aturan §3.2.
3. **Isolation Forest satu-satunya yang tidak jenuh.** Recall 0,3793 (F-10) dan 0,8470 (F-15_S) dengan 1.353 menit alarm dari 6.408 (21%), presisi tertinggi 0,2240 s.d. 0,2461. Untuk peringkat triase, ini yang paling dapat dipertanggungjawabkan; untuk alarm, tetap tidak layak (FAR 9,70 s.d. 11,21 per 24 jam, di atas gerbang 6).
4. **Transfer lintas well gagal total.** Tiga dari empat detektor menandai **100% menit** pada baseline well lain. Ini konsisten dengan `D` KS antar well 0,986 di §2.3: model yang dilatih pada satu well menganggap well lain sebagai anomali seluruhnya. Kesimpulan operasional: **skor anomali wajib dikalibrasi per well, dan transfer tanpa kalibrasi dilarang**.
5. **Matrix profile pada baseline hanya mengukur dirinya sendiri.** Dengan `contamination` 1%, ia memilih 2 s.d. 3 diskord dari 257 s.d. 297 titik. Angka ini membuktikan implementasi berjalan, bukan membuktikan kegunaan deteksi, karena diskord dipilih menurut fraksi yang kita tetapkan.


---

## 3. ANOMALI TANPA LABEL: CARA MENGEVALUASI DAN CARA MENGHINDARI KLAIM PALSU

### 3.1 Mengapa evaluasi tanpa label berbeda

Pada klasifikasi, metrik dihitung terhadap label. Pada anomali tanpa label, tidak ada label, sehingga tiga hal yang biasa dipakai sebagai "bukti" menjadi tidak sah:

| Klaim yang sering muncul | Mengapa tidak sah di kasus ini |
|---|---|
| "Recall 0,9 pada data uji" | Recall hanya sah bila laju alarm dasar dilaporkan. Detektor yang menyala 100% waktu punya recall ~1,0 dan nol kegunaan (bukti §2.4). |
| "Model menemukan 120 anomali" | Jumlah anomali ditentukan oleh `contamination` yang kita pilih, bukan ditemukan model. Angka 120 hanya mengulang parameter. |
| "Anomali yang ditemukan sesuai dengan kejadian nyata" | Hanya sah bila kejadian nyata (onset) tidak dipakai untuk menyetel skor. Kalau dipakai, itu supervised dengan nama lain. |

### 3.2 Empat pilar evaluasi yang dapat diukur tanpa label

1. **Kepatuhan laju alarm pada baseline sendiri.** Set `contamination` = 0,01, lalu ukur laju alarm nyata pada baseline. Kalau hasilnya 0,01, model berperilaku seperti yang dijanjikan. Kalau hasilnya 0,10, model tidak layak dipakai untuk alarm.
2. **Stabilitas antar sumber (transfer).** Latih pada baseline well A, ukur laju alarm pada baseline well B. Rasio laju B terhadap A adalah ukuran portabilitas ambang. Pada `TQA_mean`, `D` KS antar well 0,986 sudah memberi peringatan bahwa rasio ini akan besar.
3. **Sensitivitas terhadap drift waktu.** Bagi baseline menjadi paruh awal dan paruh akhir, ukur laju alarm di keduanya. Kenaikan yang besar berarti model menghafal rezim awal.
4. **Presisi alarm-menit terhadap onset, sebagai diagnosis.** Ini **boleh** dilaporkan hanya bila (a) disebut sebagai diagnosis pasca-hoc, (b) label tidak dipakai untuk memilih ambang, dan (c) disertai laju alarm dasar.

### 3.3 Perbandingan metode anomali

Skor 1 s.d. 5 memakai kriteria yang sama dengan §1 (penilaian rekayasa, kelas KONVENSI).

| Metode | Kebutuhan data | Biaya | Interpretabilitas | Skor data | Skor biaya | Skor interpretasi | Peran usulan |
|---|---|---|---|---|---|---|---|
| **Isolation Forest** (Liu, Ting, Zhou 2008) | Fitur multivariat; baseline beberapa ratus baris cukup | Ringan, O(n log n) dengan 200 pohon | Rendah sampai sedang: skor = rata-rata kedalaman isolasi; tidak menjelaskan variabel penyebab | 5 | 4 | 2 | **Dipakai** sebagai skor peringkat triase pada kelas tanpa label (hyd K-ii, bit_wear K-2), bukan alarm |
| **LOF** (Breunig dkk. 2000) | Baseline cukup padat; `n_neighbors` menentukan skala lokal | Sedang: O(n²) naif, mahal di luar 10⁴ titik | Sedang: rasio kepadatan lokal dapat dijelaskan sebagai "seberapa asing dibanding tetangganya" | 3 | 3 | 3 | **Dipakai** sebagai pembanding; lemah pada data berautokorelasi dengan manifold sempit |
| **Autoencoder** (Sakurada dan Yairi 2014) | Baseline untuk rekonstruksi; arsitektur dan epoch harus diprareg | Berat: latih ulang per well | Rendah: galat rekonstruksi tidak menunjuk variabel penyebab kecuali dianalisis per fitur | 3 | 2 | 2 | **Dijalankan sebagai pembanding** (MLPRegressor, 16 unit tersembunyi). Tidak dijadikan dasar rekomendasi karena hasilnya jenuh menyala (`recall` 1,0 dengan 96% menit alarm) |
| **One-Class SVM** (Schölkopf dkk. 2001) | Baseline; `nu` dan `gamma` wajib diprareg | Sedang sampai berat pada n besar | Rendah: batas keputusan di ruang kernel | 3 | 2 | 2 | **Dijalankan sebagai pembanding**; hasil terukur jauh dari parameter (`nu` 0,01 menghasilkan laju alarm 0,0665), jadi tidak layak untuk menetapkan laju alarm |
| **Matrix profile** (Yeh dkk. 2016; Zhu dkk. 2016) | Satu kanal, jendela `m` yang punya arti fisik | O(n²) naif; STOMP mempercepat, tetap berat untuk deret panjang | Sedang: diskord dapat digambar dan ditunjuk langsung pada deret | 4 | 3 | 4 | **Diusulkan** untuk kanal tunggal yang sudah terpilih (mis. TQA atau SPPA), karena operator dapat melihat potongan waktu yang aneh |

Catatan penolakan: **autoencoder dan one-class SVM tidak dijadikan dasar rekomendasi** pada kartu ini. Keduanya menambah parameter yang tidak dapat diuji dengan data kami (arsitektur, epoch, `nu`, `gamma`), sementara matrix profile dan Isolation Forest memberi peringkat dengan parameter yang lebih sedikit dan lebih mudah dipertanggungjawabkan.

### 3.4 Aturan anti-klaim-palsu (dipakai sebagai checklist gate)

1. Setiap laporan detektor wajib memuat: jumlah positif, laju alarm dasar pada baseline, dan panjang baseline dalam menit.
2. Recall tanpa laju alarm **dilarang** dicantumkan sendirian.
3. `contamination` adalah parameter masukan, bukan temuan. Jumlah alarm tidak boleh dilaporkan sebagai hasil penemuan.
4. Ambang yang disetel pada data uji harus disebut "disetel pada data uji", dan hasilnya menjadi hipotesis, bukan hasil.
5. Perbedaan antar well dilaporkan sebagai jarak distribusi (`D` KS), bukan sebagai p-value, karena asumsi independensi gugur.
6. Setiap klaim portabilitas wajib disertai uji transfer lintas sumber.
7. "Belum terukur" ditulis sebagai "belum terukur", bukan "gagal" dan bukan "berhasil".

---

## 4. KELAS YANG BELUM PUNYA LABEL ATAU BELUM LAYAK

### 4.1 hyd K-ii (FlowOut absen)

Kondisi terukur dari V9 dan D0:
- Tier saat ini **BELUM LAYAK PAKAI (eksplorasi)**. Bukti: 1 split temporal, CI fisher [0,0025; 0,0684] memuat prevalensi 0,0037, `q95` menghasilkan P = R = 0 dengan 177 FP, dan `sign-flip` 6.377 dari 8.107 jendela (78,7%).
- Kendala sensor: FlowOut tidak tersedia sebagai kanal. Ini penyebab terukur, bukan kegagalan metode.
- Onset hyd K-ii: 124 episode pada 1 wellbore (F-9 A), horizon 10 menit.

Konsekuensi metodologis: karena label onset hanya ada pada satu wellbore dan kanal fisik penentu (FlowOut) absen, **tidak ada dasar untuk melatih detektor supervised**. Yang jujur dilakukan:

| Langkah | Metode | Yang boleh diklaim |
|---|---|---|
| 1 | Uji KS antara jendela berlabel dan tanpa label pada kanal yang ada (SPPA, TQA, HKLD) | Jarak distribusi; bukan deteksi |
| 2 | Isolation Forest pada kanal yang ada, dilatih pada baseline F-9 A | Peringkat triase dengan laju alarm terukur; bukan alarm |
| 3 | Matrix profile pada kanal tunggal terpilih | Titik waktu yang paling tidak mirip dengan riwayatnya sendiri; dapat diperiksa manual |
| 4 | Bila FlowOut kelak tersedia | Baru boleh mengulang klaim deteksi |

Yang **dilarang** diklaim sekarang: "detektor menemukan 124 onset hyd K-ii". Ke-124 onset itu berasal dari label, bukan dari detektor.

### 4.2 bit_wear K-2 (belum jalan)

Kondisi terukur:
- bit_wear K-1 (status) berjalan: persistence AUPRC 0,119 s.d. 0,984 dengan `ΔB` terhadap canary 5 dari 5 well scorable, lift 1,81 s.d. 10,67, tetapi **CI, presisi, recall, dan FAR belum terukur** (kolom tidak ada di JSON V9).
- bit_wear K-2 (onset) **belum dijalankan**: praregistrasi belum terbit.
- Dataset berasal dari USROP, bukan rig Volve. Transfer lintas dataset belum diuji.

Konsekuensi: karena K-2 belum punya praregistrasi dan belum punya label onset, pekerjaan yang sah pada gelombang ini adalah **menyiapkan evaluasi tanpa label**, bukan mengklaim deteksi onset. Urutan yang diusulkan:

1. Tetapkan praregistrasi K-2 lebih dulu (horizon, definisi onset, baseline), mengikuti disiplin yang sama dengan K-i.
2. Jalankan CUSUM dan Page-Hinkley pada kanal torsi dan RPM dengan `h` dikalibrasi per well, lalu laporkan FAR pada baseline nyata dengan format §2.2.
3. Baru setelah FAR terukur, bandingkan dengan baseline rule dan persistence. Tanpa langkah 2, klaim "detektor onset bit_wear bekerja" tidak punya dasar.

Catatan penting: bit_wear K-1 sudah menunjukkan bahwa persistence adalah baseline yang sulit dikalahkan (5 dari 5 well). Setiap metode baru wajib mengalahkan persistence pada well yang sama, bukan pada rata-rata gabungan.

### 4.3 Tabel ringkas: kelas tanpa label dan peran metode

| Kelas | Status label | Metode yang masuk akal | Metode yang ditolak untuk sekarang | Alasan |
|---|---|---|---|---|
| hyd K-ii | Onset ada di 1 wellbore, kanal penentu absen | KS (diagnosis), Isolation Forest (triase), matrix profile (pemeriksaan manual) | BOCPD, autoencoder | Tidak ada prior maupun panjang deret bersih yang cukup; parameter tidak dapat diuji |
| bit_wear K-2 | Belum ada (praregistrasi belum terbit) | CUSUM dan PH terkalibrasi per well, lalu KS antar well | Semua metode supervised | Tidak ada label untuk melatih maupun mengevaluasi |
| tool_wear K-ii | Label konstan dalam run (by design) | CUSUM/PH per alat, ADWIN | Klasifikasi lintas alat | Label konstan membuat klasifikasi mustahil secara konstruksi |

---

## 5. SKOR GABUNGAN DAN PERAN USULAN

Tabel ini merangkum §1 dan §3 dengan bobot yang dinyatakan terbuka. Bobot: kebutuhan data 0,3; biaya 0,3; interpretabilitas 0,4. Skor akhir = jumlah (bobot × skor). Skor ini penilaian rekayasa (KONVENSI), bukan hasil pengukuran, dan boleh dibantah dengan argumen.

| Metode | Data | Biaya | Interpretasi | Skor berbobot | Peran usulan | Status pada kartu ini |
|---|---|---|---|---|---|---|
| Uji KS dua sampel | 5 | 5 | 4 | **4,6** | Gerbang drift antar well, alat kalibrasi | **Dijalankan** (10 pasangan, 5 uji dalam well) |
| CUSUM | 4 | 5 | 5 | **4,7** | Detektor perubahan level per well/per alat, wajib dengan mekanisme reset | **Dijalankan** (5 well), termasuk bukti kegagalan latch |
| Page-Hinkley | 4 | 5 | 5 | **4,7** | Pembanding CUSUM, lebih jujur pada data berautokorelasi | **Dijalankan** (5 well) |
| ADWIN | 4 | 4 | 3 | **3,6** | Detektor adaptif untuk tool_wear (tanpa baseline panjang) | **Belum dijalankan** |
| BOCPD | 2 | 2 | 3 | **2,3** | Ditunda sampai baseline kontigu > 361 menit tersedia | **Belum dijalankan** |
| Matrix profile | 4 | 3 | 4 | **3,7** | Pemeriksaan manual kanal tunggal, penunjuk potongan waktu | **Dijalankan pada baseline** |
| Isolation Forest | 5 | 4 | 2 | **3,5** | Triase peringkat untuk kelas tanpa label | **Dijalankan** (2 well), satu-satunya yang tidak jenuh |
| LOF | 3 | 3 | 3 | **3,0** | Pembanding lokal | **Dijalankan** (2 well), jenuh menyala |
| One-Class SVM | 3 | 2 | 2 | **2,3** | Pembanding; bukan dasar rekomendasi | **Dijalankan** (2 well), laju alarm 6,65 kali parameter |
| Autoencoder | 3 | 2 | 2 | **2,3** | Pembanding; bukan dasar rekomendasi | **Dijalankan** (2 well), jenuh menyala |

Urutan prioritas yang diusulkan untuk gelombang berikutnya: (1) CUSUM dan PH dengan reset dan kalibrasi per well/per alat, (2) uji KS sebagai gerbang sebelum memakai ambang pinjaman, (3) ADWIN untuk tool_wear, (4) Isolation Forest hanya untuk triase, (5) BOCPD ditunda.

---

## 6. RUJUKAN

Semua DOI di bawah diperiksa pada 2026-10-27 (WIB) dengan dua langkah: resolusi `https://doi.org/<doi>` (status HTTP dicatat) dan metadata `https://api.crossref.org/works/<doi>`. Berkas hasil: `scratch/rnd_r5/doi_check.txt`, perintah `bash scratch/rnd_r5/dois.sh`.

Status "TERVERIFIKASI" di sini berarti: **rekaman Crossref cocok pada penulis pertama, tahun, judul, wadah terbit, dan halaman**. Dari 11 rujukan, 7 mengembalikan 403 (bot wall: Page, Hinkley, LOF, Schölkopf, Bifet, Sakurada, Massey), 3 mengembalikan 202 (iForest, Matrix Profile I, Matrix Profile II), dan 1 terbuka (arXiv 0710.3742, HTTP 200). Artinya isi penuh 10 dari 11 rujukan tidak dibuka dari host ini; itu dicatat sebagai keterbatasan akses, bukan sebagai DOI palsu.

| # | Rujukan | DOI / URL | Status |
|---|---|---|---|
| 1 | Page, E. S. (1954). Continuous inspection schemes. *Biometrika* 41(1-2), 100-115. | 10.1093/biomet/41.1-2.100 | TERVERIFIKASI (Crossref), halaman penerbit 403 |
| 2 | Hinkley, D. V. (1971). Inference about the change-point from cumulative sum tests. *Biometrika* 58(3), 509-523. | 10.1093/biomet/58.3.509 | TERVERIFIKASI (Crossref), halaman penerbit 403 |
| 3 | Adams, R. P., dan MacKay, D. J. C. (2007). Bayesian Online Changepoint Detection. arXiv:0710.3742. | https://arxiv.org/abs/0710.3742 | TERVERIFIKASI (arXiv API: judul dan penulis cocok), HTTP 200 |
| 4 | Bifet, A., dan Gavaldà, R. (2007). Learning from Time-Changing Data with Adaptive Windowing. *Proc. SIAM Int. Conf. Data Mining*, 443-448. | 10.1137/1.9781611972771.42 | TERVERIFIKASI (Crossref), halaman penerbit 403 |
| 5 | Liu, F. T., Ting, K. M., dan Zhou, Z.-H. (2008). Isolation Forest. *ICDM 2008*, 413-422. | 10.1109/ICDM.2008.17 | TERVERIFIKASI (Crossref), halaman penerbit 202 |
| 6 | Breunig, M. M., Kriegel, H.-P., Ng, R. T., dan Sander, J. (2000). LOF: Identifying Density-Based Local Outliers. *Proc. ACM SIGMOD*, 93-104. | 10.1145/342009.335388 | TERVERIFIKASI (Crossref), halaman penerbit 403 |
| 7 | Schölkopf, B., Platt, J. C., Shawe-Taylor, J., Smola, A. J., dan Williamson, R. C. (2001). Estimating the Support of a High-Dimensional Distribution. *Neural Computation* 13(7), 1443-1471. | 10.1162/089976601750264965 | TERVERIFIKASI (Crossref), halaman penerbit 403 |
| 8 | Yeh, C.-C. M., Zhu, Y., Ulanova, L., Begum, N., Ding, Y., Dau, H. A., dkk. (2016). Matrix Profile I: All Pairs Similarity Joins for Time Series. *ICDM 2016*, 1317-1322. | 10.1109/ICDM.2016.0179 | TERVERIFIKASI (Crossref), halaman penerbit 202 |
| 9 | Zhu, Y., Yeh, C.-C. M., Zimmerman, Z., Kamgar, K., dan Keogh, E. (2016). Matrix Profile II: Exploiting a Novel Algorithm and GPUs to Break the One Hundred Million Barrier. *ICDM 2016*, 739-748. | 10.1109/ICDM.2016.0085 | TERVERIFIKASI (Crossref), halaman penerbit 202 |
| 10 | Sakurada, M., dan Yairi, T. (2014). Anomaly Detection Using Autoencoders with Nonlinear Dimensionality Reduction. *Proc. MLSDA 2014*, 4-11. | 10.1145/2689746.2689747 | TERVERIFIKASI (Crossref), halaman penerbit 403 |
| 11 | Massey, F. J. (1951). The Kolmogorov-Smirnov Test for Goodness of Fit. *JASA* 46(253), 68-78. | 10.1080/01621459.1951.10500769 | TERVERIFIKASI (Crossref), halaman penerbit 403 |

Rujukan yang **tidak** dipakai sebagai dasar rekomendasi: tidak ada di daftar ini yang berstatus BELUM TERVERIFIKASI. Satu DOI uji, 10.1214/09-AOAS282, terbaca sebagai makalah berbeda (Shirley dkk. 2010, HMM untuk uji alkohol) dan **dibuang** karena bukan rujukan yang dimaksud; itu dicatat agar tidak muncul kembali.

---

## 7. RINGKASAN DAN YANG BELUM TERVERIFIKASI

### 7.1 Ringkasan (5 baris)

1. Untuk regime tool_wear (data detik), pilihan yang diusulkan adalah CUSUM dan Page-Hinkley dengan `h` dikalibrasi per alat, ditambah ADWIN sebagai pembanding; BOCPD ditunda karena prior run-length tidak dapat dipertanggungjawabkan pada run bengkel yang pendek.
2. Untuk drift antar well, uji KS adalah alat yang tepat dan sudah terbukti perlu: 10 dari 10 pasangan well berbeda distribusi dengan `D` median 0,986, sehingga ambang global tidak sah.
3. Pada baseline bersih nyata (5 well, 257 s.d. 361 menit), ambang konvensional CUSUM `k` = 0,5 sigma, `h` = 5 sigma menghasilkan 4,02 s.d. 16,81 episode per 24 jam dan melampaui gerbang FAR ≤ 6; `ac1` 0,9765 s.d. 0,9954 membatalkan asumsi iid yang mendasari ARL buku teks.
4. Perangkap klaim palsu tertangkap langsung: CUSUM pada deret penuh memberi recall 0,75 s.d. 1,00 sambil menyala 52,29 s.d. 60,00 menit per jam, jadi recall tinggi tanpa laju alarm adalah artefak detektor macet, bukan kinerja.
5. Untuk hyd K-ii (FlowOut absen) dan bit_wear K-2 (praregistrasi belum terbit), satu-satunya keluaran yang jujur adalah peringkat triase plus uji stabilitas lintas sumber, bukan alarm dan bukan F1.

### 7.2 Yang BELUM TERVERIFIKASI atau BELUM TERUKUR

- **BOCPD tidak dijalankan** pada data mana pun. Skornya adalah penilaian rekayasa, bukan hasil.
- **ADWIN tidak dijalankan** pada data mana pun.
- **Uji anomali hanya pada 2 well** (F-10, F-15_S) karena syarat fitur lengkap 32 kolom memotong 3 well lain; angkanya tidak boleh digeneralisasi ke 9 well.
- **Matrix profile hanya dijalankan pada baseline** (257 s.d. 297 titik, jendela 60 menit), belum pada deret penuh, sehingga belum ada angka deteksi untuk metode ini.
- **Isi penuh 10 dari 11 rujukan tidak dibuka** (7 mengembalikan HTTP 403, 3 mengembalikan HTTP 202; hanya arXiv 0710.3742 yang terbuka). Verifikasi terbatas pada metadata Crossref sesuai `scratch/rnd_r5/doi_check.txt`.
- **Nilai p KS tidak sah untuk deret berautokorelasi**; `D` yang dipakai, p hanya penunjuk arah.
- **Recall dan presisi hyd K-ii serta bit_wear K-2 tidak diukur**, karena label yang sah tidak ada (K-2) atau hanya 1 wellbore dengan kanal penentu absen (K-ii).
- **Transfer domain bengkel ke rig tidak diuji dan tidak diklaim** (D-A7).
- **FAR hanya diukur pada satu kanal** (`TQA_mean`). Kanal lain (SPPA, HKLD, SWP) belum diukur; angka FAR di dokumen ini tidak boleh digeneralisasi ke kanal lain.
- **Baseline hanya 257 s.d. 361 menit per well**, sehingga kalibrasi `h` tidak diuji untuk horizon harian.
