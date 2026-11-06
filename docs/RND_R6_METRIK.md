# RND-R6: METRIK, UJI STATISTIK, DAN DESAIN EKSPERIMEN

Kartu: `t_5ffc95c0` · Board: `rnd-algo-2026` · Tanggal: 2026-10-27 (WIB)
Workspace: `/mnt/d/Capstone 1(v2)` · Arsip `/mnt/d/Capstone 1` tidak disentuh.
Keluaran angka: `rnd_r6_RESULTS.json` (skrip `rnd_r6_compute.py`) dan `rnd_r6_SUPPLEMENT.json` (skrip `rnd_r6_supplement.py`), keduanya di workspace kartu.
Rujukan silang: `docs/RND_ALGO_RESEARCH_PLAN.md` §2, `docs/RND_D0_DATA_FEASIBILITY.md`, `docs/RND_P0_PARAMETER.md`, `code/v9_i1_pipeline.py` (REGISTRY), `scratch/v9_i1/v9_i1_RESULTS.json`.

## 0. RISET PENDAHULUAN

Riset pendahuluan: statistical-analysis, statistical-power, statsmodels, literature-review, verification-mandatory.

- `statistical-analysis` dipakai untuk memilih uji yang sah per bentuk data (proporsi memakai Wilson, laju memakai Poisson eksak, dua proporsi independen memakai Fisher, unit independen memakai uji tanda, dan penolakan uji berpasangan bila hitungan berpasangan tidak tersedia), serta untuk memisahkan hasil konfirmatori dari eksploratori.
- `statistical-power` dipakai untuk menghitung daya dan efek minimum yang dapat dideteksi (MDE) pada dua sumbu: laju alarm (uji Poisson kondisional) dan delta AUPRC (simulasi blok per well), termasuk aturan bahwa MDE harus dibandingkan dengan efek terkecil yang menarik secara operasional, bukan dengan efek yang diharapkan.
- `statsmodels` dipakai langsung sebagai mesin hitung: `proportion_confint(method='wilson')`, `multipletests(method='holm'/'fdr_bh')`, dan SciPy `chi2` untuk selang eksak Garwood pada hitungan Poisson.
- `literature-review` dipakai untuk mengumpulkan dan memverifikasi rujukan wajib (DeLong, bootstrap, koreksi multiplisitas, AUPRC, daya, ukuran sampel) lewat Crossref dan `doi.org`, sehingga setiap DOI punya status HTTP yang dapat diaudit.
- `verification-mandatory` dipakai sebagai gerbang akhir: setiap angka di dokumen ini berasal dari JSON hasil skrip yang dapat dijalankan ulang, setiap DOI dicoba dibuka, dan satu bug logika yang ditemukan pada hitungan uji tanda dilaporkan sekaligus diperbaiki (bagian 2.6), bukan dibiarkan.

Riset pendahuluan: sequentialthinking, 5 pikiran saat penyusunan dokumen (`mcp__sequentialthinking__sequentialthinking`, thoughtNumber 1..5, thoughtHistoryLength 5) ditambah 4 pikiran pada run pelengkapan provenance (`thoughtNumber` 1..4, `thoughtHistoryLength` 4), sehingga total 9 pikiran pada dua run. Ringkas pikiran run dokumen: (1) artefak R6 sudah ada tetapi satu fungsi uji tanda cacat logika sehingga hasilnya tidak boleh dipakai apa adanya, (2) dua jalur kode memakai penyebut FAR yang berbeda dan selisihnya harus diukur, (3) unit independen yang sah adalah well (9), bukan jendela, sehingga daya uji tanda harus dihitung eksak, (4) rasio lebar CI 0,57 pada simulasi adalah artefak homogenitas well, bukan bukti konservatisme bootstrap jendela, (5) aturan berhenti harus berbasis batas resolusi, daya, dan kestabilan, bukan jam kerja. Ringkas pikiran run provenance: (1) satu baris ledger per klaim numerik koheren yang menunjuk JSON key persis, (2) dua angka dokumen tidak cocok dengan sumbernya sehingga dokumen wajib dipatch sebelum ledger ditulis, (3) status memakai taksonomi yang sama dengan bagian P0/D0/R1/R3/R5, (4) verifikasi baris harus bisa gagal lewat assert pada path JSON, dan ledger wajib memuat baris BELUM agar tidak memberi kesan cakupan penuh.

---

## 1. DEFINISI METRIK (RUMUS DAN SATUAN)

Notasi. Satu observasi adalah satu jendela waktu 1 menit (`ts_bin`, satuan menit). Untuk fold uji: `n_test` jendela, `n_pos` jendela berlabel positif, `n_neg = n_test - n_pos` jendela negatif. `jam_neg = n_neg / 60`.

### 1.1 FAR per 24 jam

```
FAR_24jam = 24 * FP / jam_neg = 1440 * FP / n_neg
```

Satuan: alarm palsu per 24 jam waktu operasi NEGATIF (bukan per 24 jam kalender, bukan per jendela). Penyebutnya adalah total jam jendela negatif, jadi FAR bersifat laju, bukan proporsi. Konsekuensi yang sering salah dibaca: FAR 6 tidak berarti 6 dari 1440 jendela, karena jendela negatif tidak tersebar merata sepanjang hari kalender.

Verifikasi rumus pada kode dan data:
- Jalur ML (`code/v9_e_ML_01_train.py:20` dan `:118`, `far24 = 1440.0 * fp / n_neg`) direproduksi ulang dari komponen mentah pada 26 fold: selisih absolut maksimum `5,684e-14` (`rnd_r6_RESULTS.json` S2b). Artinya rumus jalur ML konsisten sampai presisi mesin.
- Jalur hyd K-i (`code/v9_e_STAT_01_hyd_ki.py:70`, `far_24 = fp / jam_neg * 24`) memakai penyebut jam negatif teramati, bukan `n_neg/60`. Selisih absolut maksimum `1,9229` per 24 jam (fold F-12: tersimpan `98,0195`, hitung ulang dengan `n_neg/60` menghasilkan `96,0966`), dengan rentang selisih 0,0228 sampai 1,9229 pada 9 fold (S2). Contoh F-10: `far_per_neg_hour = 1,34919` menyiratkan penyebut `102,28` jam, sedangkan `n_neg/60 = 102,95` jam.
- Akibat yang harus dicatat: dua definisi penyebut hidup berdampingan dan berbeda sampai 2,0 persen relatif. Tidak satu pun fold hyd berada dekat ambang 6 (FAR tersimpan terendah 32,38), sehingga perbedaan ini tidak mengubah keputusan FAR <= 6, tetapi wajib disatukan sebelum angka FAR dipakai untuk perbandingan antar-engine pada ambang.

### 1.2 B1 (cakupan onset)

```
B1 = jumlah onset dengan >= 1 alarm pada [t_onset - H, t_onset] / jumlah onset
```

Satuan: proporsi (0 sampai 1), tanpa dimensi, dihitung pada horizon `H = 10 menit` (`scratch/v9_e_stat/v9_e_stat_02_stuck_e2_RESULTS.json`, field `task`). B1 bukan recall jendela: penyebutnya episode onset, bukan jendela positif. Pada data nyata: 281 onset di 4 well (F-10 93, F-14 61, F-9 55, F-9_A 72). B1 engine tergabung `0,1281` dengan Wilson 95 persen `[0,0940; 0,1723]`, B1 persistence tergabung `0,8719` dengan Wilson 95 persen `[0,8277; 0,9060]` (S12).

Resolusi B1 dibatasi jumlah onset: satu onset mengubah B1 sebesar `1/281 = 0,0036` (0,356 poin persen). Pada level per well resolusi jauh lebih kasar, misalnya F-9 dengan 55 onset: satu onset = 1,82 poin persen.

### 1.3 TLead (waktu ancang)

```
TLead_i = t_onset_i - t_alarm_terakhir_i        (menit, hanya untuk onset yang terdeteksi)
```

Satuan: menit. Dilaporkan sebagai median dan IQR per well, dengan dua syarat yang harus ditulis: (a) hanya dihitung pada onset dengan `B1 = 1`, sehingga TLead dan B1 tidak independen; (b) TLead tidak boleh dilaporkan bila jumlah onset terdeteksi kecil. Data nyata: F-10 median `7,0` menit IQR `[3,0; 10,0]` (15 onset terdeteksi), F-14 median `2,5` menit IQR `[1,75; 5,5]` (8 onset), F-9_A median `8,0` menit IQR `[2,0; 10,0]` (13 onset), F-9 tidak terdefinisi karena 0 onset terdeteksi (S10, S12).

Batas atas TLead adalah horizon H: TLead maksimum 10 menit karena definisi B1 memakai H = 10 menit. TLead 8 menit pada H = 10 menit hampir menyentuh langit-langit definisi, jadi angka itu tidak boleh ditafsirkan sebagai kemampuan prediksi 8 menit ke depan.

### 1.4 Presisi dan recall

```
Presisi = TP / (TP + FP)
Recall  = TP / (TP + FN) = TP / n_pos
```

Satuan: proporsi. Presisi memakai penyebut alarm (jendela yang menyala), recall memakai penyebut kejadian (jendela positif). Keduanya wajib dilaporkan bersama FAR, karena presisi tinggi dapat berasal dari prevalensi tinggi, bukan dari mutu deteksi. Contoh nyata pada hyd K-i persistence: F-10 presisi `0,8986` dengan prevalensi `0,18412`, sedangkan F-14 presisi `0,6313` dengan prevalensi `0,08317` (S3).

### 1.5 AUPRC

```
AUPRC = sum_k (TP_k / (TP_k + FP_k)) * delta(Recall_k)
```

Satuan: proporsi (0 sampai 1), dihitung sebagai average precision presisi-tertimbang-recall atas seluruh ambang, dengan prevalensi sebagai garis dasar acak (`baseline_prevalence_random` di JSON V9). Karena garis dasar AUPRC sama dengan prevalensi, AUPRC tidak dapat dibandingkan antar well tanpa menyebut prevalensi masing-masing.

### 1.6 Lift

```
lift = AUPRC / prevalensi          (tanpa dimensi, garis dasar acak = 1,0)
plafon = 1 / prevalensi            (lift maksimum yang mungkin)
```

Lift wajib dilaporkan bersama plafon, karena lift besar pada prevalensi sangat kecil dapat berarti model lemah. Kasus nyata yang membuktikan hal ini: ssi F-7 lift `150,205` dengan prevalensi `0,00305` dan plafon `327,3` (nilai JSON dari prevalensi tak dibulatkan `0,003055`; bila dihitung dari prevalensi bulat `0,00305`, hasilnya `1/0,00305 = 327,87` atau `327,9`), sedangkan ssi F-15A lift `12,252` dengan prevalensi `0,00515` dan plafon `194,2` (S14b). Tanpa plafon, F-7 tampak 4 kali lebih baik daripada kebanyakan engine, padahal AUPRC absolutnya `0,4589` pada prevalensi 0,3 persen dan hanya `3` jendela positif dari `982` jendela uji di fold itu (`scratch/v9_e_ml/v9_e_ML_ssi_RESULTS.json` folds[6] `pos_test` = 3, `n_neg` = 979, `prev_test` = 0,003055). Koreksi ini menggantikan angka 9 jendela positif yang tertulis pada draf pertama dokumen.

Ringkasan lift hyd K-i persistence (S14): F-5 lift `6,103` (plafon 10,196), F-14 `5,340` (12,024), F-10 `4,576` (5,431), F-15A `4,320` (8,820), F-9_A `3,609` (6,665), F-15_S `3,572` (8,414), F-12 `3,331` (5,182), F-7 `2,984` (5,895), F-9 `2,388` (3,820).

### 1.7 Tabel ringkas metrik

| Metrik | Rumus | Satuan | Penyebut | Batas tafsir |
|---|---|---|---|---|
| FAR_24jam | 24 x FP / jam_neg | alarm palsu per 24 jam operasi negatif | jam jendela negatif | laju, bukan proporsi; butuh jam negatif minimum agar dapat disertifikasi (bagian 3.4) |
| B1 | onset tercakup / total onset | proporsi | episode onset | bergantung horizon H = 10 menit |
| TLead | t_onset - t_alarm terakhir | menit | onset yang terdeteksi | maksimum H, hanya untuk yang terdeteksi |
| Presisi | TP / (TP + FP) | proporsi | jendela menyala | naik otomatis bila prevalensi naik |
| Recall | TP / n_pos | proporsi | jendela positif | tidak memuat informasi laju alarm |
| AUPRC | rata-rata presisi pada tiap kenaikan recall | proporsi | seluruh jendela | garis dasar = prevalensi |
| Lift | AUPRC / prevalensi | rasio | prevalensi | wajib dengan plafon 1/prevalensi |

---

## 2. UJI PEMBANDING DAN HASILNYA

### 2.1 Prinsip keluarga uji

Keluarga uji harus dideklarasikan sebelum hitung, beserta unit independennya. Untuk alat PdM ini unit independen adalah well (9), bukan jendela (puluhan ribu), karena jendela di dalam satu well berkorelasi tinggi. RND-R5 sudah mengukur autokorelasi lag-1 pada deret yang sama di atas 0,97 (`docs/RND_R5_DRIFT.md`), sehingga memperlakukan jendela sebagai sampel independen adalah pseudoreplikasi. Dua keluarga yang dipakai di sini:
- F1: 4 engine ML (vib, ssi, shk, stuck_k2) pada RF ambang 0,5, hipotesis nol presisi sama dengan prevalensi terkumpul, satu sisi.
- F2: 9 fold hyd K-i persistence, hipotesis nol presisi sama dengan prevalensi fold, satu sisi.

### 2.2 DeLong untuk AUROC, dan mengapa AUPRC tidak memakai DeLong

Uji DeLong membandingkan dua AUROC berkorelasi memakai komponen struktural (V01, V10) per observasi. Fungsi `delong_auc()` sudah ditulis dan diuji pada data sintetis: AUC `0,8186`, galat baku `0,0141`, CI95 `[0,7910; 0,8463]` (S9). Angka itu adalah uji kewajaran fungsi, bukan hasil engine, dan tidak boleh dikutip sebagai kinerja.

Status pada data nyata: TIDAK DIHITUNG. JSON V9 menyimpan metrik agregat (AUPRC, presisi, recall, FAR), bukan skor per jendela, sedangkan DeLong membutuhkan skor per observasi untuk tiap komponen. Karena itu DeLong untuk data ini BELUM TERUKUR, bukan "tidak berbeda". Tindakan yang harus diambil pada run berikutnya: simpan `skor` per jendela per fold per model.

Untuk AUPRC, DeLong tidak berlaku karena bentuk asimtotiknya berbeda; selang AUPRC dihitung dengan bootstrap (Boyd et al. 2013, DOI terverifikasi). Karena itu pasangan uji yang benar adalah: AUROC memakai DeLong, AUPRC memakai bootstrap berpasangan pada unit well.

### 2.3 Bootstrap berpasangan untuk delta metrik

Desain yang dipakai (S7, S15): 9 well, tiap well 800 jendela negatif, AP dihitung per well, delta = rata-rata AP engine A dikurangi rata-rata AP engine B, bootstrap 120 kali resampel blok per well (`n_boot` = 120 pada setiap baris hasil S7 dan S15), tolak H0 bila CI95 delta tidak memuat 0. Catatan: string `S7_mde_delta_auprc_simulasi.desain` menulis 150 kali, sedangkan jumlah yang benar-benar dipakai terekam sebagai `n_boot` = 120; yang dilaporkan adalah 120.

Hasil pada prevalensi 1,69 persen (setara ssi): delta median `0,0056` pada pemisahan 0,15 (daya 0,30), `0,0090` pada 0,25 (0,412), `0,0145` pada 0,35 (0,55), `0,0232` pada 0,50 (0,792), `0,0804` pada 1,0 (1,0), `0,1904` pada 1,5 (1,0).

Hasil pada prevalensi 13,66 persen (setara hyd K-i): delta median `0,0192` pada 0,15 (daya 0,838), `0,0346` pada 0,25 (1,0), `0,0525` pada 0,35 (1,0), `0,0829` pada 0,50 (1,0).

Peringatan yang wajib dibaca bersama S7b: lebar CI95 dengan bootstrap jendela `0,0453`, dengan bootstrap blok per well `0,0260`, rasio `0,57`. Rasio di bawah 1 ini TIDAK boleh ditafsirkan sebagai bukti bahwa bootstrap jendela lebih konservatif. Simulasi S7 memakai parameter well yang identik, sehingga tidak ada heterogenitas antar-well; pada data nyata AUPRC antar-well menyebar sampai sekitar 30 kali (`docs/V9_EVAL_C_LAYERC.md`, bagian C3 di REGISTRY: "AUPRC antar-well spread 30x"), dan heterogenitas itulah yang akan melebarkan CI blok. Angka 0,57 adalah artefak desain simulasi yang homogen, bukan properti data.

### 2.4 Wilson untuk proporsi

Wilson dipakai untuk presisi dan B1 karena proporsi dengan n kecil atau mendekati 1 (Wald tidak sah).

Presisi hyd K-i per fold: lebar CI95 antara `0,0321` (F-10, n = 1361) dan `0,1024` (F-9_A, n = 298). Semua selang presisi ada di dalam `[0,5836; 0,9135]` (S3). Konsekuensi praktis: dua well dengan presisi berbeda kurang dari sekitar 6 sampai 10 poin persen belum dapat dibedakan pada n alarm ratusan.

B1 tergabung: `0,1281` dengan Wilson `[0,0940; 0,1723]` pada 281 onset (S12). Lebar selang 7,8 poin persen berarti B1 engine pada data ini hanya dapat dibedakan dari B1 persistence (`0,8719`, `[0,8277; 0,9060]`) secara jelas, tetapi tidak dapat dipakai untuk memeringkat engine yang selisihnya di bawah sekitar 8 poin persen.

### 2.5 Fisher untuk dua proporsi independen

Contoh nyata: presisi hyd K-i persistence F-10 (TP 1223, FP 138) dibandingkan F-12 (TP 1143, FP 398). Tabel 2x2 memberi odds ratio `3,0859` dan p dua sisi di bawah `2,2e-308` (underflow float64; SciPy melaporkan `0,0`), artinya perbedaan presisi antar dua well itu nyata dan bukan variasi sampling (S13).

Batas yang harus ditulis: Fisher sah untuk dua kelompok independen. Untuk dua engine yang dinilai pada jendela yang SAMA, uji yang sah adalah McNemar pada tabel ketidaksesuaian berpasangan, dan hitungan berpasangan itu belum tersedia di JSON V9. Karena itu perbandingan engine pada jendela yang sama berstatus BELUM TERUKUR sampai skor per jendela disimpan.

### 2.6 Uji tanda pada unit well, dan satu bug yang ditemukan lalu diperbaiki

Uji tanda dua sisi eksak, alpha 0,05, unit well. Hasil setelah perbaikan (S5FIX):

| n well | k minimum sepakat | p pada k | p minimum mungkin | daya pada konkordansi 0,7 | 0,8 | 0,9 | 1,0 |
|---|---|---|---|---|---|---|---|
| 4 | tidak ada | tidak ada | 0,125 | 0,000 | 0,000 | 0,000 | 0,000 |
| 7 | 7 | 0,015625 | 0,015625 | 0,0824 | 0,2097 | 0,4783 | 1,000 |
| 9 | 8 | 0,039063 | 0,003906 | 0,1960 | 0,4362 | 0,7748 | 1,000 |

Bug yang ditemukan: versi pertama `sign_test_crit` mengiterasi `range(n+1, -1, -1)`, sehingga k = n+1 (dengan p = 0 karena jumlah ekor kosong) dikembalikan lebih dulu untuk setiap n. Akibatnya keluaran lama menyebut k minimum 5 untuk 4 well, 8 untuk 7 well, dan 10 untuk 9 well, dengan proporsi minimum di atas 1 dan daya 0 pada semua tingkat konkordansi. Keluaran itu tidak mungkin benar secara matematis (k tidak dapat melebihi n), sehingga dipakai sebagai penanda bug, bukan sebagai temuan. Perbaikan: iterasi naik dari k = 0 dan kembalikan k pertama dengan p dua sisi <= alpha. Angka pada tabel di atas adalah hasil setelah perbaikan dan dicatat di `rnd_r6_SUPPLEMENT.json` S5FIX.

Implikasi yang harus dibawa ke desain: dengan 4 well, uji tanda tidak akan pernah signifikan pada alpha 0,05, sehingga setiap klaim antar-well yang hanya tersedia di 4 well harus ditulis sebagai deskriptif. Dengan 7 well, hanya konkordansi sempurna yang signifikan.

### 2.7 Poisson eksak untuk laju FAR

Wilson tidak sah untuk laju (FAR), karena penyebutnya jam paparan, bukan jumlah percobaan. Yang dipakai adalah selang eksak Garwood: `lo = chi2.ppf(alpha/2, 2k)/2`, `hi = chi2.ppf(1-alpha/2, 2(k+1))/2`, lalu dikali `24/jam_neg`.

Hasil pada 9 fold hyd K-i (S4): FAR titik `32,38` dengan CI95 `[27,03; 38,01]` (F-10) sampai FAR `110,71` dengan CI95 `[93,21; 128,26]` (F-7). Rasio batas atas terhadap batas bawah antara `1,22` dan `1,60`. Artinya pada paparan 20 sampai 160 jam negatif, FAR hanya dapat ditentukan dalam rentang sekitar 1,2 sampai 1,6 kali nilainya. Klaim "FAR turun 30 persen" pada selang selebar ini tidak dapat dibuktikan dengan data sebesar ini.

### 2.8 Koreksi multiplisitas: Holm dan Benjamini-Hochberg

Kedua koreksi dijalankan dengan `statsmodels.stats.multitest.multipletests`.

Keluarga F1 (4 uji, RF ambang 0,5): 3 signifikan mentah, 3 signifikan Holm, 3 signifikan BH. Rinciannya: `vib` p mentah `0,0` (tetap 0), `shk` p `3,263e-09` menjadi Holm `9,789e-09` dan BH `6,526e-09`, `stuck_k2` p `0,009521` menjadi Holm `0,019042` dan BH `0,012695`, sedangkan `ssi` p `1,0` tetap tidak signifikan (TP 0 dari 4 alarm).

Keluarga F2 (9 uji): 9 signifikan mentah, 9 signifikan Holm, 9 signifikan BH (S8).

Pelajaran metodologis yang penting dari F1: pada `stuck_k2`, presisi terkumpul `0,0457` dengan prevalensi `0,01666`, jadi presisi sekitar 2,7 kali garis dasar. Itu signifikan tetapi kecil, dan setelah Holm masih lolos. Ini contoh bahwa signifikansi statistik tidak sama dengan kelayakan operasional.

### 2.9 Tabel keputusan uji

| Pertanyaan | Data yang ada | Uji yang sah | Status pada data ini |
|---|---|---|---|
| Dua AUROC berkorelasi | skor per jendela | DeLong | BELUM TERUKUR (skor tidak disimpan) |
| Delta AUPRC antar engine | AP per well | bootstrap blok per well | TERUKUR (simulasi; data nyata butuh skor) |
| Presisi satu engine | TP, FP | Wilson | TERUKUR |
| Presisi dua engine, jendela sama | TP, FP, FN per jendela | McNemar | BELUM TERUKUR (hitungan berpasangan tidak ada) |
| Presisi dua well/engine berbeda | TP, FP dua kelompok | Fisher eksak | TERUKUR |
| Laju FAR | FP, jam negatif | Poisson eksak Garwood | TERUKUR |
| Arah perbaikan antar well | tanda delta per well | uji tanda eksak | TERUKUR (n = 4, 7, 9) |
| Banyak uji dalam satu keluarga | kumpulan p | Holm, BH | TERUKUR |

---

## 3. KEKUATAN UJI DAN EFEK MINIMUM YANG DAPAT DIDETEKSI

### 3.1 Batas daya uji tanda (sudah dihitung di 2.6)

Dengan 9 well, minimal 8 well harus sepakat agar signifikan, dan daya baru mencapai 0,775 bila probabilitas konkordansi sebenarnya 0,90. Dengan 7 well, hanya 7 dari 7 yang signifikan, daya 0,478 pada konkordansi 0,90. Dengan 4 well, daya 0 di semua tingkat konkordansi. Maka efek minimum yang dapat dideteksi pada unit well adalah "perbaikan yang terjadi di hampir semua well", bukan "perbaikan rata-rata".

### 3.2 MDE untuk selisih laju FAR

Uji Poisson kondisional eksak, alpha 0,05, daya 80 persen, grid rasio laju 1,10 sampai 4,00 langkah 0,10 (31 titik, `rnd_r6_compute.py:197`: `[1.0 + 0.1*i for i in range(1, 31)]`). Catatan `S6_mde_selisih_laju_far.catatan` di JSON menulis "grid RR 1,05..3,00"; catatan itu keliru dan sudah dikoreksi terhadap kode, sedangkan hasil MDE tidak terpengaruh karena titik 1,40 berada di dalam kedua rentang. Dengan laju dasar 157 FP per periode negatif panjang (median 9 fold hyd K-i), MDE adalah rasio laju `1,40` (S6). Artinya penurunan FAR kurang dari 29 persen tidak dapat dibuktikan pada besaran data ini.

Kasus batas yang harus ditulis: pada shk F-10 ambang 0,5 laju dasar 0 FP, sehingga MDE tidak terdefinisi (`null`). Bila laju dasar nol, tidak ada rasio yang dapat diuji; yang berlaku adalah batas atas eksak (bagian 3.4).

### 3.3 MDE untuk delta AUPRC

Simulasi blok per well, 9 well, 800 jendela negatif per well, 80 ulangan, bootstrap 120 (S15), ditambah grid kasar 120 ulangan (S7).

| Prevalensi | Delta AUPRC (median) | Daya | Tafsir |
|---|---|---|---|
| 1,69 persen | 0,0145 | 0,550 | belum memadai |
| 1,69 persen | 0,0232 | 0,792 | mendekati MDE 80 persen |
| 1,69 persen | 0,0804 | 1,000 | jauh di atas MDE |
| 13,66 persen | 0,0192 | 0,838 | sudah di atas MDE 80 persen |
| 13,66 persen | 0,0346 | 1,000 | jauh di atas MDE |

Kesimpulan terukur: pada prevalensi sekecil ssi (1,69 persen) dengan 9 well, efek minimum yang dapat dideteksi pada daya 80 persen adalah delta AUPRC sekitar `0,023`. Pada prevalensi hyd K-i (13,66 persen), MDE 80 persen paling besar `0,0192` (daya 0,838 sudah tercapai pada delta itu) dan daya penuh tercapai pada `0,0346`. Perbaikan AUPRC di bawah 0,02 pada prevalensi kecil harus dilaporkan sebagai "tidak dapat dideteksi pada desain ini", bukan sebagai "tidak ada perbaikan".

### 3.4 Batas resolusi instrumen (bukan daya statistik, tetapi batas yang lebih keras)

Dua batas ini tidak bergantung pada uji apa pun, sehingga harus diperiksa lebih dulu.

B1: 281 onset total, sehingga satu onset mengubah B1 sebesar 1/281 = `0,0036` (0,356 poin persen). Per well lebih kasar, misalnya F-9 (55 onset): 1,82 poin persen per onset.

FAR: aturan `FAR <= 6` ekivalen dengan `FP <= (jam_neg/24) x 6`, sehingga `jam_neg >= 4 x FP` jam. Tabel eksak (S16 dan S11): 1 FP butuh 4,0 jam negatif; 2 FP butuh 8,0 jam; 3 FP butuh 12,0 jam; 6 FP butuh 24,0 jam; 12 FP butuh 48,0 jam; 30 FP butuh 120,0 jam. Untuk sertifikasi dengan 0 FP, batas atas eksak Garwood adalah `3,6889/jam_neg` per jam, sehingga `FAR_24jam` batas atas `<= 6` menuntut `jam_neg >= 14,756` jam.

Penerapan pada data nyata: ssi F-9_A memiliki `n_neg = 786` jendela, yaitu 13,1 jam negatif. Dengan 0 FP sekali pun, batas atas 95 persen FAR adalah `3,6889 x 24 / 13,1 = 6,76` per 24 jam, masih di atas 6. Maka klaim "FAR <= 6" untuk fold itu TIDAK DAPAT DISERTIFIKASI pada data yang ada, terlepas dari hasil ujinya.

---

## 4. ATURAN BERHENTI EKSPERIMEN

Aturan berikut harus dievaluasi berurutan. Berhenti karena salah satu aturan berarti berhenti karena bukti; berhenti karena waktu habis bukan berhenti karena bukti dan wajib ditulis berbeda.

**A1. Berhenti bila klaim tidak dapat disertifikasi oleh resolusi instrumen.** Sebelum menjalankan uji, periksa `jam_neg >= 4 x FP` untuk klaim FAR, dan `jam_neg >= 14,756` jam untuk klaim FAR <= 6 dengan 0 FP. Bila gagal, hasilnya ditulis "tidak dapat disertifikasi", dan eksperimen pada klaim itu dihentikan. Contoh yang sudah terjadi: ssi F-9_A (13,1 jam negatif).

**A2. Berhenti bila unit independen terlalu sedikit untuk uji yang direncanakan.** Bila n well = 4 dan uji yang direncanakan adalah uji tanda atau Wilcoxon, daya = 0 tanpa melihat data. Hentikan uji inferensial, turunkan klaim menjadi deskriptif, dan jangan menambah fold semu dari well yang sama.

**A3. Berhenti bila MDE lebih besar daripada efek terkecil yang menarik.** Bandingkan MDE (bagian 3.2 dan 3.3) dengan efek minimum yang mengubah keputusan operasional. Bila MDE > efek itu, eksperimen dihentikan dan ditulis "desain tidak mampu menjawab", bukan "tidak ada efek". Angka acuan pada data ini: MDE rasio laju FAR `1,40`; MDE delta AUPRC `0,023` pada prevalensi 1,69 persen dan paling besar `0,0192` pada prevalensi 13,66 persen.

**A4. Berhenti bila hasil sudah stabil, dan lanjut bila belum.** Kriteria stabil: arah delta sama di semua fold, CI95 delta tidak memuat 0, dan hasil tidak berubah bila seed diganti (SEED = 42 pada semua skrip, jadi penggantian seed adalah uji yang masih harus dijalankan). Bila arah delta berbeda antar fold, eksperimen belum selesai.

**A5. Berhenti bila sisa ketidakpastian hanya dapat dikecilkan dengan data baru.** Contoh nyata: DeLong dan McNemar tidak dapat dijalankan karena skor per jendela dan hitungan berpasangan tidak disimpan. Pada kondisi itu, eksperimen berhenti dengan status BELUM TERUKUR dan tindakan yang diminta adalah menyimpan artefak tambahan pada run berikutnya, bukan mengulang uji yang sama.

**A6. Berhenti bila keluarga uji berubah setelah melihat hasil.** Setiap uji yang ditambahkan setelah p mentah terlihat wajib dilaporkan sebagai eksploratori dan tidak boleh dipakai untuk klaim konfirmatori. Aturan ini mencegah pencarian signifikansi lewat pergantian uji.

**A7. Yang dilarang sebagai alasan berhenti.** "Waktu habis", "sudah cukup lama", "sudah banyak yang dicoba", dan "kemungkinan tidak akan berubah" bukan alasan sah. Bila eksperimen dihentikan secara administratif, tulis "dihentikan administratif (belum ada bukti)", dan status klaim tetap BELUM TERUKUR.

**A8. Keluaran minimum saat berhenti.** Setiap penghentian wajib menghasilkan: (a) metrik yang sudah terukur beserta selang, (b) MDE pada desain yang dipakai, (c) daftar uji yang tidak dapat dijalankan beserta artefak yang hilang, (d) satu tindakan konkret untuk run berikutnya.

---

## 5. RUJUKAN

Status verifikasi: Crossref dan `doi.org` dicoba dibuka pada 2026-10-27 (WIB); hasil mentah di `doi_verify_r6.json`.

| # | Penulis pertama, tahun | Judul | Wadah | DOI | Status |
|---|---|---|---|---|---|
| 1 | DeLong, 1988 | Comparing the Areas under Two or More Correlated Receiver Operating Characteristic Curves: A Nonparametric Approach | Biometrics 44:837 | 10.2307/2531595 | TERVERIFIKASI (Crossref 200, doi.org 200) |
| 2 | Efron, 1979 | Bootstrap Methods: Another Look at the Jackknife | The Annals of Statistics 7:1-26 | 10.1214/aos/1176344552 | TERVERIFIKASI (200, 200) |
| 3 | Benjamini, 1995 | Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing | JRSS-B 57:289-300 | 10.1111/j.2517-6161.1995.tb02031.x | TERVERIFIKASI (Crossref 200; doi.org 403 karena pemblokiran bot, bukan DOI tidak ada) |
| 4 | Wilson, 1927 | Probable Inference, the Law of Succession, and Statistical Inference | JASA 22:209-212 | 10.1080/01621459.1927.10502953 | TERVERIFIKASI (Crossref 200; doi.org 403 karena pemblokiran bot) |
| 5 | Fisher, 1922 | On the Interpretation of chi-square from Contingency Tables, and the Calculation of P | JRSS 85:87 | 10.2307/2340521 | TERVERIFIKASI (200, 200) |
| 6 | Boyd, 2013 | Area under the Precision-Recall Curve: Point Estimates and Confidence Intervals | LNCS, hlm. 451-466 | 10.1007/978-3-642-40994-3_29 | TERVERIFIKASI (200, 200) |
| 7 | Saito, 2015 | The Precision-Recall Plot Is More Informative than the ROC Plot When Evaluating Binary Classifiers on Imbalanced Datasets | PLOS ONE 10:e0118432 | 10.1371/journal.pone.0118432 | TERVERIFIKASI (200, 200) |
| 8 | Lakens, 2022 | Sample Size Justification | Collabra: Psychology 8 | 10.1525/collabra.33267 | TERVERIFIKASI (Crossref 200; doi.org 403 karena pemblokiran bot) |
| 9 | Varoquaux, 2018 | Cross-validation failure: Small sample sizes lead to large error bars | NeuroImage 180:68-77 | 10.1016/j.neuroimage.2017.06.061 | TERVERIFIKASI (200, 200) |
| 10 | Holm, 1979 | A Simple Sequentially Rejective Multiple Test Procedure | Scandinavian Journal of Statistics 6:65-70 | 10.2307/4615733 | BELUM TERVERIFIKASI (Crossref 404, doi.org 404) |

Catatan pemakaian rujukan. Nomor 1 sampai 9 dipakai sebagai dasar metode. Nomor 10 TIDAK dipakai sebagai dasar rekomendasi karena DOI gagal dibuka; koreksi Holm pada dokumen ini dijalankan lewat implementasi `statsmodels` yang diuji langsung pada data (S8), bukan bersandar pada rujukan yang tidak dapat diverifikasi. Bila Holm tetap ingin dikutip formal, gunakan rujukan bibliografis jurnal di atas tanpa DOI, dengan penanda BELUM TERVERIFIKASI.

---

## 6. PROVENANCE DAN KOREKSI

Setiap angka di dokumen ini punya baris di `docs/RND_PROVENANCE_LEDGER.md` bagian "Bagian R6" (R6-01 sampai R6-134, 134 baris). Sumber primer: `rnd_r6_RESULTS.json`, `rnd_r6_SUPPLEMENT.json`, `doi_verify_r6.json`, ditambah kode dan data mentah yang dirujuk pada kolom rujukan tiap baris. Skrip pembangkit sekaligus verifikator: `verify_r6_ledger_rows.py` di workspace kartu, yang meng-assert tiap nilai terhadap path JSON (dan tiap baris DERIVASI lewat rumusnya) lalu menolak menulis baris bila assert gagal.

Koreksi yang dilakukan pada run provenance, semuanya perbaikan angka salah tulis, bukan temuan baru:

1. Bagian 1.6: "9 jendela positif" diganti `3` jendela positif dari `982` jendela uji. Bukti: `scratch/v9_e_ml/v9_e_ML_ssi_RESULTS.json` folds[6] `pos_test` = 3, `n_neg` = 979, `prev_test` = 0,003055.
2. Bagian 1.6: plafon ssi F-7 diganti `327,3` (nilai JSON dari prevalensi tak dibulatkan), dan `1/0,00305 = 327,87` dicatat sebagai nilai turunan dari prevalensi bulat.
3. Bagian 3.2: grid rasio laju diganti `1,10 sampai 4,00` langkah 0,10 sesuai `rnd_r6_compute.py:197`; catatan `S6` di JSON yang menulis 1,05 sampai 3,00 dinyatakan keliru.
4. Bagian 2.3: dicatat bahwa string `S7...desain` menulis 150 kali bootstrap, sedangkan `n_boot` yang benar-benar dipakai 120.

## 7. RINGKASAN 5 BARIS

1. Enam metrik didefinisikan ulang dengan rumus dan satuan, dan ditemukan dua definisi penyebut FAR yang hidup berdampingan (jalur ML memakai `n_neg`, jalur hyd memakai jam negatif teramati) dengan selisih sampai 1,9229 per 24 jam pada 9 fold.
2. Uji pembanding yang dapat dijalankan pada data yang ada: Wilson (lebar presisi 0,0321 sampai 0,1024), Poisson eksak Garwood (rasio CI 1,22 sampai 1,60), Fisher (OR 3,0859 antar well), uji tanda, serta Holm dan BH pada dua keluarga uji; DeLong dan McNemar BELUM TERUKUR karena skor per jendela dan hitungan berpasangan tidak disimpan.
3. Satu bug logika pada uji tanda ditemukan dan diperbaiki: keluaran lama memberi k minimum lebih besar daripada n dengan daya 0; setelah perbaikan, n = 9 membutuhkan 8 well sepakat (p = 0,039) dan n = 4 mustahil signifikan (p minimum 0,125).
4. Efek minimum yang dapat dideteksi: rasio laju FAR 1,40; delta AUPRC sekitar 0,023 pada prevalensi 1,69 persen dan paling besar 0,0192 pada prevalensi 13,66 persen; ditambah batas keras resolusi, yaitu 14,756 jam negatif untuk menyertifikasi FAR <= 6 dengan 0 FP dan 0,356 poin persen per onset untuk B1.
5. Aturan berhenti ditetapkan delapan butir berbasis bukti (resolusi instrumen, jumlah unit independen, MDE lawan efek yang diminati, kestabilan, batas data, disiplin keluarga uji), dan "waktu habis" dinyatakan bukan alasan sah untuk menghentikan eksperimen.

## 8. BELUM TERVERIFIKASI

1. DeLong pada data nyata: BELUM TERUKUR karena skor per jendela tidak disimpan di JSON V9 (fungsi hanya diuji pada data sintetis).
2. McNemar untuk dua engine pada jendela yang sama: BELUM TERUKUR karena hitungan ketidaksesuaian berpasangan tidak tersedia.
3. Uji kestabilan lintas seed (A4): BELUM DIJALANKAN; semua hasil memakai SEED = 42.
4. Seluruh hasil kekuatan uji (S6, S7, S15) berasal dari simulasi dengan asumsi well homogen (800 jendela negatif per well, parameter identik). Angka MDE nyata akan lebih lebar bila heterogenitas antar-well dimasukkan; besarnya belum diukur.
5. Rasio lebar CI 0,57 (S7b) hanya sah untuk simulasi homogen dan tidak dapat dipindahkan ke data nyata.
6. DOI Holm 1979 (10.2307/4615733) gagal dibuka (HTTP 404 pada Crossref dan doi.org), sehingga koreksi Holm tidak disandarkan pada rujukan itu.
7. Penyebab perbedaan penyebut FAR antara jalur hyd dan jalur ML belum ditelusuri sampai baris kode pembangkit `far_per_neg_hour`; yang terukur baru besar selisihnya (maksimum 1,9229 per 24 jam).
8. Validitas satuan jendela 1 menit pada jalur FAR diasumsikan dari `n_neg/60`; belum diuji ulang terhadap distribusi `ts_bin` pada run ini (RND-D0 sudah mengukur `ts_bin` sebagai indeks menit, tetapi pengujian ulang khusus jalur FAR belum dilakukan).
