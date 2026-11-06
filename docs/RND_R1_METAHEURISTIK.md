# RND-R1: METAHEURISTIK KONTINU (GWO, WOA, PSO, SSA, HHO, EPO, SMA, BGWO, EO, HBO, HORSE HERD, SLIME MOULD)

Kartu: `t_4ee3d4d1` · Board: `rnd-algo-2026` · Tanggal: 2026-10-27 (WIB)
Workspace: `/mnt/d/Capstone 1(v2)` · Folder arsip `/mnt/d/Capstone 1` tidak disentuh.
Dokumen pendamping: `docs/RND_PROVENANCE_LEDGER.md` (baris R1-001 sampai R1-062), `docs/RND_ALGO_RESEARCH_PLAN.md`, `docs/V9_EVAL_C_LAYERC.md`.

## Baris riset pendahuluan

Riset pendahuluan: literature-review, paper-lookup, exa-search, scientific-critical-thinking, verification-mandatory

- **literature-review**: dipakai untuk menetapkan protokol pencarian yang dapat direproduksi (kriteria inklusi/eksklusi, filter jenis publikasi, pencatatan string kueri dan tanggal akses) sebelum satu pun DOI dipilih, sehingga tabel bukti di dokumen ini bisa diulang pihak lain.
- **paper-lookup**: dipakai sebagai jalur registri resmi, yaitu Crossref untuk metadata (judul, tahun, jurnal, penulis pertama) dan `doi.org` untuk pembuktian bahwa identitas DOI benar-benar terdaftar dan mengarah ke penerbit; DOI tidak pernah diketik manual, selalu diambil dari respons API.
- **exa-search**: dipakai untuk pemeriksaan silang istilah pencarian pada mesin pencari semantik, khususnya ketika nama algoritma ambigu (SSA, SMA, HBO) sehingga kueri bibliografis Crossref saja bisa menyesatkan ke varian yang salah.
- **scientific-critical-thinking**: dipakai untuk menolak bukti yang tidak menjawab pertanyaan (contoh: paper yang memakai metaheuristik untuk melatih CNN mendalam tidak menjadi bukti bagi RF tabular 55 fitur), memisahkan korelasi dari kausalitas klaim "lebih baik", dan menilai risiko overfitting pada 9 fold.
- **verification-mandatory**: dipakai untuk menutup dokumen dengan pemeriksaan ulang (setiap DOI dikutip ada di `refs_registry.md` hasil harvest, tidak ada angka tanpa baris ledger, tidak ada em-dash, tidak ada karakter CJK) dan mendaftar eksplisit apa yang belum terverifikasi.

Riset pendahuluan: sequentialthinking, 5 pikiran (`mcp__sequentialthinking__sequentialthinking`, thoughtNumber 1 sampai 5, `thoughtHistoryLength` 5).
Ringkas: (1) disambiguasi tiga nama algoritma yang bercabang (SSA, SMA, HBO) sebelum penilaian; (2) standar bukti dua lapis (metadata Crossref + resolusi `doi.org`) dan pemisahan paper dasar dari paper bukti domain; (3) aritmetika kesesuaian kasus (55 fitur, 27 fitur getaran, 27 head, 9 well, kontrak tanpa grid search) dan konsekuensi anggaran evaluasi; (4) penyusunan rubrik skor 1 sampai 5 yang dapat diperiksa ulang; (5) gerbang verifikasi sebelum menulis, termasuk larangan mengarang angka biaya komputasi.

---

## 0. METODE, CAKUPAN, DAN BATAS BUKTI

### 0.1 Protokol pencarian

| Butir | Isi |
|---|---|
| Sumber | Crossref REST API (`api.crossref.org/works`), bidang bibliografis, bukan pencarian bebas |
| Filter | `type:journal-article` dan `from-pub-date:2019-01-01` |
| Kueri putaran 1 | 36 string unik, 2 sampai 3 string per algoritma (ranah: fault diagnosis, getaran, feature selection, hyperparameter, pengeboran, PdM) |
| Kueri putaran 2 | 12 pencarian paper dasar (judul asli) dan 25 string celah (EO fault diagnosis, Horse Herd domain, drilling, predictive maintenance) |
| Record ber-DOI putaran 1 | 323 |
| DOI unik diperiksa | 309 |
| DOI resolve `doi.org` | 309 dari 309 (HTTP 302 ke penerbit) |
| Kandidat lolos filter judul + domain | 185 |
| Kandidat celah putaran 2 | 80 |
| Rujukan akhir terverifikasi di `refs_registry.md` | 58 |
| Rujukan yang benar-benar dikutip di dokumen ini | 55 |
| Rujukan registry yang tidak dikutip di dokumen | 3 (`10.1007/s11761-023-00382-8`, `10.1038/s41598-024-53141-w`, `10.3390/fuels6020033`) |

Berkas bukti di workspace kartu: `lit_r1.json` (hasil putaran 1), `r1_selected.json` (185 kandidat terfilter), `r1_round2.json` (paper dasar + celah), `r1_round3.json` (HHO dan PSO), `refs_registry.md` (58 rujukan final dengan status `doi.org` dan jumlah sitasi). Skrip: `r1_harvest.py`, `r1_select.py`, `r1_round2.py`, `r1_round3.py`, `r1_registry.py`, `r1_stats.py`, `r1_diff_registry.py`.

**Koreksi angka, dicatat terbuka.** Versi dokumen sebelumnya menulis "54" pada baris rujukan akhir. Angka itu berasal dari keadaan registry sebelum `r1_registry.py` selesai menambahkan baris terakhir. Hitung ulang pada berkas final: 58 baris DOI, 55 di antaranya dikutip di dokumen ini, 3 tidak dikutip. Angka 54 tidak dipakai lagi di mana pun dalam dokumen ini.

### 0.2 Apa yang dibuktikan dan apa yang tidak

- Yang dibuktikan: DOI terdaftar, mengarah ke penerbit (HTTP 302), dan metadata (judul, tahun, jurnal, penulis pertama) cocok dengan catatan registri Crossref.
- Yang **tidak** dibuktikan: bahwa teks penuh bebas diakses. Beberapa penerbit berlangganan. Dokumen ini tidak mengklaim akses teks penuh, hanya klaim yang bisa ditopang judul, abstrak, dan metadata.
- Penulis pertama pada tabel diambil dari field `author[0].family` Crossref. Untuk paper yang penulisnya lebih dari satu, hanya penulis pertama disebut. Ini keterbatasan penyajian, bukan kekurangan verifikasi.
- Satu pengecualian jujur: Kennedy & Eberhart 1995 (DOI `10.1109/icnn.1995.488968`) tercatat di Crossref sebagai `proceedings-article` dengan field `issued` kosong, sehingga tahun 1995 diambil dari judul prosiding (`Proceedings of ICNN'95`), bukan dari field tanggal. DOI tetap resolve 302.

### 0.3 Disambiguasi nama: tiga keputusan yang mengubah hasil

Kartu menyebut 12 nama. Tiga di antaranya bercabang, dan pilihan varian mengubah seluruh bukti yang relevan. Keputusan diambil sebelum penilaian, bukan setelah melihat hasil.

| Nama di kartu | Kandidat varian | Keputusan | Alasan |
|---|---|---|---|
| SSA | Salp Swarm Algorithm (Mirjalili 2017) atau Sparrow Search Algorithm (Xue 2020) | **dibelah menjadi dua unit**: SSA-Salp dan SSA-Sparrow | mekanisme berbeda (rantai pemimpin-pengikut lawan producer-scrounger + deteksi bahaya), bukti domain juga berbeda; menggabung akan mencampur dua dasar yang tidak sebanding |
| SMA | Slime Mould Algorithm atau Spider Monkey Algorithm | **SMA = Slime Mould Algorithm** | di daftar kartu sudah ada butir "Slime Mould" terpisah; membaca SMA sebagai Spider Monkey akan membuat butir "Slime Mould" tidak punya pasangan |
| HBO | Heap-Based Optimizer atau Honey Badger Optimizer | **HBO = Heap-Based Optimizer** (nama harfiah), Honey Badger dilaporkan sebagai unit pembanding | Heap-Based adalah perluasan harfiah "HBO"; Honey Badger justru punya bukti fault diagnosis lebih banyak sehingga perlu terlihat terpisah, bukan tersembunyi |

**Temuan administratif yang wajib dinyatakan**: butir "SMA" dan butir "Slime Mould" pada kartu menunjuk algoritma yang sama (Slime Mould Algorithm, Li 2020, DOI `10.1016/j.future.2020.03.055`). Keduanya ditulis sebagai bagian terpisah agar kartu terpenuhi, tetapi **tidak dihitung sebagai dua bukti independen** dan pada tabel ringkas diberi tanda duplikat. Konsekuensinya 12 butir kartu menjadi 14 unit penilaian (SSA dibelah dua, Honey Badger ditambah sebagai pembanding, SMA dan Slime Mould tetap dua baris tetapi satu algoritma).

### 0.4 Verifikasi ulang seluruh DOI yang dikutip (pass 2)

Uji dilakukan dua lapis karena satu lapis saja menyesatkan. Lapis pertama memeriksa registrasi DOI di `doi.org` tanpa mengikuti redirect: status 302 berarti DOI terdaftar dan mengarah ke penerbit. Lapis kedua memeriksa metadata di Crossref: status 200 berarti judul, tahun, penulis pertama, dan nama jurnal dapat dibandingkan dengan yang dikutip dokumen ini.

| Butir | Hasil |
|---|---|
| DOI yang dikutip dokumen ini (pola backtick) | 55 |
| Lapis 1, resolve 302 di `doi.org` (redirect tidak diikuti) | 55 dari 55 |
| Lapis 2, metadata Crossref 200 | 55 dari 55 |
| DOI tidak resolve atau metadata tidak cocok | 0 |
| Halaman penerbit setelah redirect diikuti: 200 / 403 / 202 | 32 / 16 / 7 |

Status 403 dan 202 bukan bukti DOI palsu. Keduanya muncul setelah `doi.org` berhasil mengarahkan ke penerbit, lalu penerbit menolak permintaan otomatis: MDPI, Hindawi/Wiley, Taylor & Francis, dan IET memberi 403, sedangkan IEEE memberi 202 dengan halaman yang membutuhkan JavaScript. Konsekuensinya akses teks penuh tetap tidak terbukti untuk 23 dari 55 rujukan, dan dokumen ini tetap tidak mengklaim pembacaan teks penuh (lihat §0.2 dan §5 butir 3).

Pemeriksaan terpisah atas klaim jumlah pada §0.1: berkas `lit_r1.json` memuat 309 entri `doi_checks` dan seluruhnya bernilai `http: 302`. Angka "309 dari 309" pada §0.1 karena itu bukan warisan tanpa dasar.

Catatan Kennedy & Eberhart 1995 pada §0.2 diperiksa ulang dan tetap benar: record Crossref `10.1109/icnn.1995.488968` bertipe `proceedings-article` dengan `issued` berisi `[null]`, sedangkan tanggal 2002-11-19 hanya ada pada field `created`, yaitu tanggal deposit, bukan tanggal terbit.

Verifikasi pass 2 memakai 4 pikiran `mcp__sequentialthinking__sequentialthinking` tambahan, sehingga total untuk kartu ini 9 pikiran. Berkas bukti: `r1_verify_pass2.py`, `r1_verify_pass2.json`, `r1_publisher_status.py`, `r1_publisher_status.json`, `r1_check309.py` di workspace kartu `t_4ee3d4d1`.

---

## 1. KESESUAIAN DENGAN KASUS KITA

### 1.1 Apa yang sebenarnya akan dioptimasi

Tiga peran berbeda, dengan jenis ruang keputusan yang berbeda. Mencampurnya adalah kesalahan paling umum pada literatur "metaheuristik untuk PdM".

| Peran | Objek yang dioptimasi | Jenis ruang | Dimensi | Sumber angka dimensi |
|---|---|---|---|---|
| **T1 Tuning hyperparameter** | RF atau LightGBM: `max_depth`, `min_samples_leaf`, `max_features`, `n_estimators`, dan untuk LightGBM `num_leaves`, `learning_rate`, `min_child_samples` | kontinu dan/atau kategorikal kecil | **4 sampai 6** | hitungan parameter pada kontrak model `docs/V9_PM1_ARCHITECTURE.md` §5 baris RF 200 pohon, seed 42 (3 parameter eksplisit) ditambah 3 parameter LightGBM yang lazim; rentang 4 sampai 6 adalah **target desain**, bukan hasil ukur |
| **T2 Feature selection** | subset dari 55 fitur MWD (11 kanal x 5 statistik) | biner | **55** | `docs/V9_R1_JUSTIFICATION.md:169` dan `docs/V9_PM1_ARCHITECTURE.md:255` (11 kanal MWD x 5 statistik = 55 fitur) |
| **T2b Feature selection getaran** | subset dari 27 fitur getaran (9 statistik x 3 sumbu X/Y/Z) | biner | **27** | `docs/V9_PM1_ARCHITECTURE.md:276`; ditegaskan `code/v9_i1_pipeline.py:605` (`assert len(feats) == 27`) |
| **T3 Kalibrasi ambang per well** | satu ambang per engine per well (atau satu parameter bentuk ambang) | kontinu, 1 dimensi per well | **1 x jumlah well** = 9 untuk kelas 9 well, atau 4 untuk vib, 2 untuk stuck K-i | jumlah well per kelas: `docs/RND_D0_DATA_FEASIBILITY.md` §3; windows vib 23.922 di 4 well, hyd_ki 52.509 di 9 well, shk 56.495 di 9 well, ssi 35.906 di 9 well, stuck_k2 118.567 di 4 well, stuck_k1 5.555 di 2 well |

### 1.2 Fakta yang mengubah seluruh penilaian: baseline sekarang tidak dituning sama sekali

`docs/V9_PM1_ARCHITECTURE.md:356` menetapkan kontrak implementasi: "hyperparam kontrak (seed 42, tanpa grid search)". Artinya pembanding yang sah untuk metaheuristik bukan "model yang sudah dioptimasi", melainkan model dengan hyperparameter tetap.

Konsekuensi metodologis:

1. Ruang perbaikan yang tersedia untuk T1 nyata, karena belum ada pencarian sama sekali.
2. Tetapi klaim "metaheuristik mengalahkan baseline" menjadi terlalu mudah benar dan karena itu tidak informatif. Pembanding yang benar adalah **pencarian netral dengan anggaran sama** (random search atau Bayesian optimization dengan jumlah evaluasi identik). Tanpa pembanding itu, kenaikan metrik tidak bisa dipisahkan dari sekadar "ada pencarian".
3. Pernyataan ini **bukan klaim bahwa random search lebih baik**. Ini syarat kontrol, bukan hasil. Di repo ini belum ada satu pun run metaheuristik, sehingga tidak ada angka untuk diklaim.

### 1.3 Anggaran evaluasi, dan mengapa 9 well adalah batas keras

Satu evaluasi fitness untuk T1 dan T2 berarti satu protokol LOWO/LOTO penuh. Cakupan fold yang sudah ada: 28 fold E_ML (vib 4, ssi 9, shk 9, stuck_k2 4), 9 fold hyd_ki, 4 fold stuck_E2, 8 run tool_wear di 4 alat (`docs/V9_EVAL_C_LAYERC.md:76`).

Anggaran yang saya tetapkan untuk gelombang ini (**target desain, kelas KONVENSI, bukan hasil ukur**):

| Peran | Anggaran evaluasi fitness | Alasan |
|---|---|---|
| T1 tuning 4 sampai 6 dimensi | **maksimum 300** | 300 evaluasi x 9 fold = 2.700 fit model; di atas itu waktu dinding menjadi masalah dan tidak ada tambahan informasi karena ruang keputusan efektif kecil |
| T3 kalibrasi ambang 1 dimensi per well | **maksimum 100 per well** | ruang 1 dimensi; pencarian lebih dari 100 titik pada fungsi satu variabel adalah pemborosan, pencarian grid 100 titik sudah cukup dan lebih mudah diaudit |
| T2 feature selection 55 dimensi | **maksimum 1.000** | batas atas yang masih bisa dijalankan; ini juga batas di mana overfitting seleksi menjadi akut (lihat 1.4) |

Biaya waktu dinding per evaluasi **BELUM TERUKUR** di kartu ini. Saya tidak mengukur latensi fit RF atau LightGBM pada data nyata, jadi tidak ada angka detik yang boleh ditulis. Kolom biaya pada §2 karena itu dinyatakan dalam **jumlah evaluasi fitness per iterasi** (sifat struktural algoritma, bukan hasil ukur).

### 1.4 Risiko overfitting dengan 9 well: mengapa ini pembatas utama

Ini bagian paling penting dari seluruh dokumen, dan alasannya bukan teoretis.

1. **Jumlah unit independen adalah 9, bukan 55.000.** Baris data berjumlah puluhan ribu (hyd_ki 52.509, shk 56.495), tetapi unit yang boleh dianggap independen untuk generalisasi adalah well, karena baris dalam satu well berkorelasi kuat secara temporal. Memilih subset fitur atau ambang berdasarkan 9 well berarti mengambil keputusan statistik dari 9 titik.
2. **Noise antar well sudah terukur besar, bukan dugaan.** Pada `docs/V9_EVAL_C_LAYERC.md` §2.1, satu ambang tetap untuk vib menghasilkan FAR 4,1 sampai 496 antar well (**119 kali**). Pada §2.3, CI RF shk memuat prevalensi di **7 dari 9** fold. Pada §2.2, AUPRC RF ssi menyebar **30 kali** antar fold. Artinya variasi antar well lebih besar daripada efek yang ingin dideteksi oleh pencarian hyperparameter.
3. **Konsekuensi langsung**: optimizer yang mengevaluasi 1.000 kandidat pada 9 fold sedang mengevaluasi 1.000 konfigurasi terhadap 9 titik. Setiap kenaikan skor agregat bisa berasal dari penghafalan pola fold, bukan dari sinyal fisik. Seleksi pada 9 titik dengan 1.000 percobaan adalah multiple comparison masif tanpa koreksi.
4. **Bukti pendukung dari literatur PdM**: Hakami 2024 (`10.1038/s41598-024-59958-9`, Scientific Reports) secara eksplisit membahas kelangkaan data, ketidakseimbangan kelas, dan tantangan feature selection pada model PdM. Ini mendukung sikap konservatif, bukan menutup jalan. Sitasi ini dipakai sebagai peringatan metodologis, bukan sebagai bukti bahwa pendekatan tertentu berhasil.
5. **Mitigasi yang bisa diaudit** (harus menjadi syarat, bukan saran): (a) protokol bersarang, seleksi hyperparameter hanya di dalam fold latih, evaluasi di fold uji yang tidak pernah dilihat optimizer; (b) pembanding anggaran-sama (random search) wajib ada; (c) laporkan sebaran antar fold (min, median, maks), bukan rata-rata tunggal; (d) tolak kandidat yang menang hanya karena satu fold ekstrem, misalnya dengan memeriksa apakah median juga naik; (e) kunci protokol sebelum run (pra-registrasi), karena pencarian besar ditambah kebebasan memilih metrik agregat adalah mesin temuan palsu.

---

## 2. PENILAIAN PER ALGORITMA

Rubrik skor (ditetapkan sebelum melihat hasil, sama untuk semua algoritma). Skor 1 sampai 5.

| Kode | Kriteria | Cara memeriksa |
|---|---|---|
| K1 | Bukti domain terverifikasi 2019 atau lebih baru, minimum 2, DOI resolve | tabel rujukan di setiap bagian |
| K2 | Kecocokan jenis ruang keputusan dengan peran yang diusulkan | apakah butuh transfer function untuk ruang biner |
| K3 | Biaya evaluasi intrinsik per iterasi | populasi x iterasi |
| K4 | Risiko overfitting pada 9 fold (bobot ganda) | jumlah parameter bebas relatif 9 titik evaluasi |
| K5 | Kematangan implementasi dan risiko salah implementasi | kompleksitas fase algoritma |

Pembobotan: K1 dan K4 berbobot ganda karena keduanya yang menentukan lolos atau tidaknya gate keputusan plan §6. Algoritma tanpa bukti domain sama sekali tidak boleh melewati skor 2, walau secara matematis elegan.

### 2.1 GWO (Grey Wolf Optimizer)

**Mekanisme.** Meniru hierarki dan pola berburu serigala. Populasi dibagi menjadi empat peran (alpha, beta, delta, omega), dan perpindahan setiap individu dihitung sebagai rata-rata tertimbang posisi tiga pemimpin terbaik. Penekanan eksplorasi ke eksploitasi diatur oleh parameter `a` yang menurun linear dari 2 ke 0 sepanjang iterasi, sehingga di awal pencarian langkah besar dan di akhir langkah halus. Algoritma dasarnya (Mirjalili 2014, `10.1016/j.advengsoft.2013.12.007`) adalah salah satu metaheuristik paling banyak dikutip (19.176 sitasi pada catatan Crossref).

**Parameter utama.** Ukuran populasi, jumlah iterasi, `a` awal dan akhir (biasanya 2 ke 0), konstanta acak `r1` dan `r2`. Tidak ada parameter khas yang banyak; ini keunggulannya untuk pemakaian cepat.

**Biaya komputasi.** Satu evaluasi fitness per individu per iterasi. Dengan populasi 30 dan 100 iterasi, anggaran sekitar 3.000 evaluasi. Untuk T1 (4 sampai 6 dimensi) ini **melampaui** anggaran 300 yang ditetapkan di §1.3 sebanyak sepuluh kali, sehingga pemakaian naif tidak realistis dan populasi atau iterasi harus diperkecil drastis (misalnya 10 individu x 30 iterasi = 300).

**Kebutuhan evaluasi fitness.** Fungsi fitness harus mengembalikan satu skalar yang bisa dibandingkan antar kandidat. Untuk T1, skalar itu sebaiknya AUPRC rata-rata antar fold **dengan penalti dispersi**, karena rata-rata saja akan memilih konfigurasi yang sangat bagus di satu well dan buruk di well lain (pola yang sudah terukur pada vib).

**Bukti literatur domain.**

| Rujukan | Peran bukti |
|---|---|
| Lee 2022, "A Feature Selection Approach Hybrid Grey Wolf and Heap-Based Optimizer Applied in Bearing Fault Diagnosis", IEEE Access, `10.1109/access.2022.3177735` | GWO dipakai untuk memilih fitur pada diagnosis bantalan, yaitu peran T2 pada domain getaran |
| Xie 2022, "Locally generalized preserving projection and flexible grey wolf optimizer-based ELM for fault diagnosis of rolling bearing", Measurement, `10.1016/j.measurement.2022.111828` | GWO mengoptimasi parameter classifier pada diagnosis bantalan |
| Gu 2020, "Multi-objective Informative Frequency Band Selection Based on Negentropy-induced Grey Wolf Optimizer for Fault Diagnosis of Rolling Element Bearings", Sensors, `10.3390/s20071845` | GWO multiobjektif untuk pemilihan pita frekuensi, relevan dengan praproses getaran |
| Ramasamy Rajammal 2022, "Binary Grey Wolf Optimizer with Mutation and Adaptive K-nearest Neighbour for Feature Selection in Parkinson's Disease Diagnosis", Knowledge-Based Systems, `10.1016/j.knosys.2022.108701` | varian biner untuk seleksi fitur, relevan untuk T2 |

**Kesesuaian dengan kasus kita.** Cocok untuk T1 (tuning 4 sampai 6 dimensi) karena ruangnya kontinu dan dimensinya kecil, sehingga populasi kecil sudah memadai. Untuk T2 (55 dimensi biner) GWO harus diubah menjadi biner (lihat BGWO §2.10), dan itu menambah lapisan yang harus dijustifikasi terpisah. Untuk T3 (ambang per well, 1 dimensi) GWO berlebihan, karena satu variabel lebih baik ditangani grid atau pencarian kuadratik yang bisa diaudit manual.

**Skor: 4.** Alasan: bukti domain kuat dan berlapis (T2 getaran, T1 classifier, praproses getaran), mekanisme sederhana dengan parameter sedikit (K5 baik), ruang kontinu cocok untuk T1 (K2 baik). Dikurangi satu angka karena biaya evaluasi bawaan jauh di atas anggaran (K3 lemah) dan karena 9 fold tetap membuat T1 rawan (K4).

**Peran diusulkan: tuning hyperparameter (T1), prioritas pertama bersama PSO.**

### 2.2 WOA (Whale Optimization Algorithm)

**Mekanisme.** Meniru pola berburu paus bungkuk dengan dua manuver: serangan gelembung spiral (exploitation, posisi baru dihitung sepanjang spiral logaritmik terhadap solusi terbaik) dan pencarian acak dengan vektor referensi (exploration). Probabilitas `p` memilih antara spiral dan pengepungan, sedangkan parameter `a` menurun untuk menggeser fokus dari eksplorasi ke eksploitasi. Basis: Mirjalili dan Lewis 2016 (`10.1016/j.advengsoft.2016.01.008`, 14.089 sitasi Crossref).

**Parameter utama.** Ukuran populasi, jumlah iterasi, konstanta spiral `b` (biasanya 1), dan probabilitas `p`. Sama sederhananya dengan GWO.

**Biaya komputasi.** Satu evaluasi per individu per iterasi, identik strukturnya dengan GWO. Populasi 30 x 100 iterasi sekitar 3.000 evaluasi, sehingga masalah anggaran sama persis.

**Kebutuhan evaluasi fitness.** Sama seperti GWO: satu skalar per kandidat, dan sebaiknya skalar yang menghukum dispersi antar fold.

**Bukti literatur domain.** Empat rujukan 2022 sampai 2026, semuanya pada diagnosis bantalan, yaitu domain getaran yang dekat dengan engine vib:

| Rujukan | Peran bukti |
|---|---|
| wang 2024, "A rolling bearing fault diagnosis technique based on fined-grained multi-scale symbolic entropy and whale optimization algorithm-MSVM", Nonlinear Dynamics, `10.1007/s11071-023-09152-9` | WOA mengoptimasi SVM pada diagnosis bantalan |
| Huang 2022, "Bearing Fault Diagnosis Based on Stochastic Resonance and Improved Whale Optimization Algorithm", Electronics, `10.3390/electronics11142185` | WOA untuk pemilihan parameter praproses dan deteksi |
| Li 2025, "A rolling bearing fault diagnosis method based on extreme learning machine optimized by improved whale optimization algorithm", Facta Universitatis Series Mechanical Engineering, `10.22190/fume241130008l` | WOA sebagai pengoptimasi classifier |
| Liu 2026, "A Hybrid Denoising Model for Rolling Bearing Fault Diagnosis: Improved Edge Strategy Whale Optimization Algorithm", Symmetry, `10.3390/sym18010168` | WOA untuk pemilihan parameter denoising |

Catatan kritis: keempatnya memakai WOA untuk **mengoptimasi classifier atau parameter praproses sinyal getaran**, bukan untuk memilih subset fitur tabular dari 55 kolom. Transfernya ke kasus kita adalah transfer peran (optimizer sebagai pencari parameter kontinu), bukan transfer domain apa adanya.

**Kesesuaian dengan kasus kita.** Profilnya hampir identik dengan GWO. Untuk T1 layak. Untuk T3 berlebihan. Untuk T2 butuh versi biner yang tidak dibahas pada rujukan di atas.

**Skor: 4.** Alasan: bukti domain paling banyak di antara semua algoritma pada dokumen ini (empat rujukan 2024 sampai 2026 khusus bantalan), mekanisme sederhana. Sama seperti GWO dikurangi karena biaya evaluasi dan karena seluruh bukti berpusat pada sinyal getaran mentah, bukan fitur tabular multi-kanal MWD.

**Peran diusulkan: tuning hyperparameter (T1), kandidat kuat; untuk engine vib khususnya paling relevan.**

### 2.3 PSO (Particle Swarm Optimization)

**Mekanisme.** Setiap partikel membawa posisi dan kecepatan. Kecepatan diperbarui dengan menarik partikel ke arah posisi terbaik pribadinya dan posisi terbaik kawanan, dengan bobot inersia yang mengatur seberapa besar momentum lama dipertahankan. Basis: Kennedy dan Eberhart 1995 (`10.1109/icnn.1995.488968`, 42.382 sitasi Crossref, tercatat sebagai `proceedings-article` dengan field tanggal kosong).

**Parameter utama.** Ukuran populasi, bobot inersia `w`, koefisien kognitif `c1`, koefisien sosial `c2`, batas kecepatan. Ini **lebih banyak parameter daripada GWO dan WOA**, dan `w`, `c1`, `c2` sendiri sering perlu disetel, yang menimbulkan masalah meta: menyetel optimizer untuk menyetel model.

**Biaya komputasi.** Satu evaluasi per partikel per iterasi. Populasi 30 x 100 iterasi sekitar 3.000 evaluasi, sama seperti dua algoritma sebelumnya.

**Kebutuhan evaluasi fitness.** Satu skalar per posisi. Karena PSO paling sensitif terhadap skala antar dimensi, fungsi fitness untuk T1 sebaiknya dinormalisasi, dan parameter perlu diskalakan ke rentang seragam sebelum dipetakan ke nilai sebenarnya.

**Bukti literatur domain.**

| Rujukan | Peran bukti |
|---|---|
| Fan 2020, "A Bearing Fault Diagnosis Using a Support Vector Machine Optimised by the Self-Regulating Particle Swarm", Shock and Vibration, `10.1155/2020/9096852` | PSO mengoptimasi SVM pada diagnosis bantalan |
| Huang 2019, "A Morphological Filtering Method Based on Particle Swarm Optimization for Railway Vehicle Bearing Fault Diagnosis", Shock and Vibration, `10.1155/2019/2593973` | PSO untuk parameter praproses filter, relevan dengan rantai getaran |
| Sobhi 2021, "Prediction and analysis of penetration rate in drilling operation using deterministic and metaheuristic optimization methods", Journal of Petroleum Exploration and Production Technology, `10.1007/s13202-021-01394-w` | **rujukan pengeboran**: metode metaheuristik dipakai untuk memprediksi dan menganalisis laju penembusan |
| Ebrahimabadi 2024, "Prediction of rate of penetration (ROP) in petroleum drilling operations using optimization algorithms", Rudarsko-geolosko-naftni zbornik, `10.17794/rgn.2024.3.9` | **rujukan pengeboran**: algoritma optimasi untuk ROP |

Dua rujukan pengeboran di atas adalah satu-satunya bukti pengeboran yang berhasil dikumpulkan untuk seluruh dokumen ini, dan keduanya tidak spesifik PSO murni (Sobhi 2021 membandingkan beberapa metode metaheuristik). Ini harus dinyatakan apa adanya: **bukti pengeboran untuk metaheuristik kontinu bersifat tipis**, dan tidak ada satu pun rujukan yang mengoptimasi ambang alarm PdM pada data pengeboran.

**Kesesuaian dengan kasus kita.** Paling matang dari sisi implementasi (tersedia di banyak pustaka), sehingga risiko salah implementasi paling rendah. Cocok untuk T1. Kurang cocok untuk T3 karena 1 dimensi tidak butuh kawanan. `w`, `c1`, `c2` menambah tiga parameter bebas, dan pada 9 fold itu justru menambah risiko overfitting seleksi.

**Skor: 4.** Alasan: bukti domain getaran kuat ditambah dua rujukan pengeboran (satu-satunya di dokumen ini), kematangan implementasi tertinggi (K5), dan mekanisme mudah diaudit. Dikurangi karena parameter bebannya paling banyak di antara tiga algoritma teratas, yang memperburuk K4 pada 9 fold.

**Peran diusulkan: tuning hyperparameter (T1), dan sebagai pembanding implementasi termudah; untuk kalibrasi ambang per well hanya sebagai pemeriksaan silang, bukan metode utama.**

### 2.4 SSA-Salp (Salp Swarm Algorithm)

**Mekanisme.** Meniru rantai salp di laut. Individu pertama adalah pemimpin yang memandu ke arah makanan (solusi terbaik), sedangkan individu berikutnya mengikuti posisi individu di depannya, sehingga terbentuk rantai. Parameter `c1` menurun eksponensial dan mengatur seberapa jauh pemimpin bergerak. Basis: Mirjalili 2017 (`10.1016/j.advengsoft.2017.07.002`, 4.858 sitasi Crossref).

**Parameter utama.** Ukuran populasi, jumlah iterasi, dan parameter penurun `c1`. Sangat sedikit parameter.

**Biaya komputasi.** Satu evaluasi per individu per iterasi, sehingga populasi 30 x 100 iterasi sekitar 3.000 evaluasi. Sama dengan kelompok sebelumnya.

**Kebutuhan evaluasi fitness.** Satu skalar per kandidat; untuk versi biner (seleksi fitur) fitness harus menggabungkan akurasi dan penalti jumlah fitur terpilih, karena tanpa penalti jumlah fitur optimizer akan memilih semua fitur.

**Bukti literatur domain.**

| Rujukan | Peran bukti |
|---|---|
| Lee 2024, "Application of Salp Swarm Algorithm and Extended Repository Feature Selection Method in Bearing Fault Diagnosis", Mathematics, `10.3390/math12111718` | SSA dipakai untuk seleksi fitur pada diagnosis bantalan, yaitu T2 pada domain getaran |
| Neggaz 2020, "Boosting salp swarm algorithm by sine cosine algorithm and disrupt operator for feature selection", Expert Systems with Applications, `10.1016/j.eswa.2019.113103` | SSA untuk seleksi fitur (176 sitasi) |
| Zivkovic 2022, "Novel Improved Salp Swarm Algorithm: An Application for Feature Selection", Sensors, `10.3390/s22051711` | SSA untuk seleksi fitur (83 sitasi) |

**Kesesuaian dengan kasus kita.** Bukti domainnya ada, tetapi condong ke seleksi fitur, bukan ke tuning hyperparameter model tabular. Untuk T2 (55 dimensi biner) SSA butuh transfer function, dan tidak ada rujukan di atas yang menguji 55 dimensi pada fitur operasi pengeboran.

**Skor: 3.** Alasan: bukti domain cukup (satu rujukan getaran langsung ditambah dua rujukan seleksi fitur yang mapan), tetapi peran yang paling didukung literatur (seleksi fitur) adalah peran yang paling rawan overfitting pada 9 well (K4). Untuk T1 bukti domainnya tidak spesifik.

**Peran diusulkan: feature selection (T2) sebagai kandidat kedua, bukan prioritas; tidak untuk T1.**

### 2.5 SSA-Sparrow (Sparrow Search Algorithm)

**Mekanisme.** Meniru pembagian kerja burung pipit: sebagian individu berperan sebagai producer yang mencari makanan, sisanya sebagai scrounger yang mengikuti, ditambah mekanisme deteksi bahaya yang memindahkan individu secara acak ketika ambang peringatan terlampaui. Basis: Xue dan Shen 2020 (`10.1080/21642583.2019.1708830`, 3.816 sitasi Crossref).

**Parameter utama.** Ukuran populasi, jumlah iterasi, proporsi producer, proporsi individu yang mendeteksi bahaya, ambang keselamatan. Jumlah parameter sedang sampai banyak.

**Biaya komputasi.** Satu evaluasi per individu per iterasi; populasi 30 x 100 iterasi sekitar 3.000 evaluasi.

**Kebutuhan evaluasi fitness.** Satu skalar per posisi. Karena mekanismenya memindahkan individu secara acak saat "bahaya", fungsi fitness yang bising membuat perpindahan acak itu sulit dibedakan dari perbaikan nyata.

**Bukti literatur domain.**

| Rujukan | Peran bukti |
|---|---|
| Xing 2021, "Multi-component fault diagnosis of wheelset-bearing using shift-invariant impulsive dictionary matching pursuit and sparrow search algorithm", Measurement, `10.1016/j.measurement.2021.109375` | SSA-Sparrow pada diagnosis bantalan roda |
| Xu 2024, "Optimization of Deep Belief Network Based on Sparrow Search Algorithm for Rolling Bearing Fault Diagnosis", IEEE Access, `10.1109/access.2024.3354794` | SSA-Sparrow mengoptimasi Deep Belief Network |
| Ma 2023, "Deep Learning Network Based on Improved Sparrow Search Algorithm Optimization for Rolling Bearing Fault Diagnosis", Mathematics, `10.3390/math11224634` | SSA-Sparrow mengoptimasi jaringan mendalam |
| Wang 2024, "Adaptive Feature Extraction Using Sparrow Search Algorithm-Variational Mode Decomposition for Low-Speed Bearing Fault Diagnosis", Sensors, `10.3390/s24216801` | SSA-Sparrow untuk parameter dekomposisi VMD |

**Catatan kritis yang menentukan skor.** Hampir seluruh bukti SSA-Sparrow adalah **mengoptimasi jaringan mendalam atau parameter VMD**, bukan mengoptimasi hyperparameter RF atau LightGBM pada tabel fitur. Kasus kita tidak memakai jaringan mendalam, dan D0 sudah menyatakan VMD tidak layak karena laju sampel maksimum 0,3333 Hz (Nyquist 0,1667 Hz), sehingga rujukan VMD tidak bisa ditransfer. Bukti yang tersedia relevan pada tingkat "optimizer dipakai pada data getaran", tetapi tidak pada tingkat peran yang kita butuhkan.

**Skor: 3.** Alasan: bukti domain banyak dan berkualitas, tetapi perannya (jaringan mendalam dan VMD) tidak tersedia di kasus kita. Memberi skor lebih tinggi berarti meminjam bukti dari peran yang tidak kita pakai, dan itu tepat jenis kesalahan yang dicegah oleh scientific-critical-thinking.

**Peran diusulkan: tidak dipakai pada gelombang ini; dicatat sebagai kandidat bila kelak ada model sekuensial mendalam.**

### 2.6 HHO (Harris Hawks Optimization)

**Mekanisme.** Meniru tujuh strategi pengepungan kelinci oleh elang Harris, dipilih berdasarkan energi kelinci `E` yang menurun sepanjang iterasi. Fase mencakup pengepungan lunak, pengepungan keras, pengepungan lunak dengan penyusupan cepat, dan seterusnya, masing-masing dengan aturan perpindahan berbeda. Basis: Heidari 2019 (`10.1016/j.future.2019.02.028`, 6.235 sitasi Crossref).

**Parameter utama.** Ukuran populasi, jumlah iterasi, dan parameter energi awal `E0`. Meski parameter eksplisitnya sedikit, **struktur fase internalnya paling kompleks** di antara algoritma pada dokumen ini (tujuh cabang perilaku), sehingga risiko salah implementasi lebih tinggi.

**Biaya komputasi.** Satu evaluasi per individu per iterasi, populasi 30 x 100 iterasi sekitar 3.000 evaluasi.

**Kebutuhan evaluasi fitness.** Satu skalar per kandidat. Kompleksitas fase membuat lintasan pencarian sulit direproduksi bila implementasi berbeda, sehingga nomor versi implementasi wajib dicatat.

**Bukti literatur domain.**

| Rujukan | Peran bukti |
|---|---|
| Shao 2021, "Coordinated approach fusing time-shift multiscale dispersion entropy and vibrational Harris hawks optimization-based SVM for fault diagnosis of rolling bearing", Measurement, `10.1016/j.measurement.2020.108580` | HHO untuk mengoptimasi SVM pada diagnosis bantalan (133 sitasi) |
| Long 2022, "A velocity-guided Harris hawks optimizer for function optimization and fault diagnosis of wind turbine", Artificial Intelligence Review, `10.1007/s10462-022-10233-1` | HHO pada diagnosis turbin angin |
| Liang 2024, "An Antinoise Feature Extraction and Improved Harris Hawks Optimization for On-Load Tap Changer Mechanical Fault Diagnosis", IEEE Sensors Journal, `10.1109/jsen.2024.3350167` | HHO pada diagnosis mekanis |

**Kesesuaian dengan kasus kita.** Layak untuk T1 secara teknis, tetapi tidak menawarkan keunggulan yang bisa dibuktikan atas GWO atau WOA pada ruang 4 sampai 6 dimensi, sedangkan risiko implementasinya lebih tinggi. Pada anggaran evaluasi 300, keunggulan eksplorasi HHO tidak punya ruang untuk muncul.

**Skor: 3.** Alasan: bukti domain kuat (tiga rujukan diagnosis mesin), tetapi kompleksitas fase menaikkan risiko implementasi (K5) dan tidak ada alasan terukur untuk memilihnya di atas GWO atau WOA pada dimensi rendah (K2 netral). Pada 9 fold, tambahan kompleksitas tidak dibayar oleh tambahan informasi.

**Peran diusulkan: tuning hyperparameter (T1) sebagai kandidat ketiga; tidak dipakai bila GWO atau WOA sudah cukup.**

### 2.7 EPO (Emperor Penguin Optimizer)

**Mekanisme.** Meniru perilaku berkelompok penguin kaisar, khususnya pembentukan huddle untuk menjaga panas. Posisi individu diperbarui berdasarkan jarak ke posisi terbaik dan fungsi panas yang bergantung pada radius huddle. Basis: Dhiman dan Kumar 2018 (`10.1016/j.knosys.2018.06.001`, 674 sitasi Crossref).

**Parameter utama.** Ukuran populasi, jumlah iterasi, dan parameter yang mengatur radius huddle. Varian biner (BEPO) menambahkan fungsi transfer, yang menjadi titik lemah karena pemilihan fungsi transfer sangat memengaruhi hasil pada ruang biner.

**Biaya komputasi.** Satu evaluasi per individu per iterasi; populasi 30 x 100 iterasi sekitar 3.000 evaluasi.

**Kebutuhan evaluasi fitness.** Untuk EPO kontinu, satu skalar. Untuk BEPO (seleksi fitur), fitness harus menggabungkan kinerja dan penalti jumlah fitur; tanpa itu BEPO akan cenderung memilih banyak fitur.

**Bukti literatur domain.**

| Rujukan | Peran bukti |
|---|---|
| Lee 2024, "Application of symmetric uncertainty and emperor penguin-grey wolf optimisation for feature selection in motor fault classification", IET Electric Power Applications, `10.1049/elp2.12459` | EPO hibrida dengan GWO untuk seleksi fitur pada klasifikasi gangguan motor |
| Dhiman 2021, "BEPO: A novel binary emperor penguin optimizer for automatic feature selection", Knowledge-Based Systems, `10.1016/j.knosys.2020.106560` | varian biner EPO untuk seleksi fitur otomatis (210 sitasi) |
| Singh 2023, "Emperor penguin optimization algorithm and bacterial foraging optimization algorithm based novel feature selection approach for glaucoma classification", Soft Computing, `10.1007/s00500-023-08449-6` | EPO untuk seleksi fitur pada klasifikasi medis |

**Kesesuaian dengan kasus kita.** Seluruh bukti domainnya adalah **seleksi fitur**, bukan tuning hyperparameter. Jadi EPO hanya masuk akal untuk T2. Tetapi T2 adalah peran paling rawan pada 9 well, dan BGWO sudah menempati peran itu dengan bukti yang lebih langsung ke domain getaran.

**Skor: 3.** Alasan: bukti domain memadai tetapi seluruhnya pada peran T2, dan T2 adalah peran berisiko tertinggi (K4). Tidak ada bukti domain untuk T1.

**Peran diusulkan: feature selection (T2) sebagai alternatif ketiga, di bawah BGWO dan SSA-Salp. Tidak dipakai bila BGWO lolos uji.**

### 2.8 SMA (Slime Mould Algorithm)

**Mekanisme.** Meniru osilasi dan pembentukan jaringan hifa lendir jamur. Bobot individu diperbarui berdasarkan kualitas fitness relatif terhadap populasi, dengan aturan yang membuat individu berkualitas buruk bergerak lebih agresif. Basis: Li 2020 (`10.1016/j.future.2020.03.055`, 2.990 sitasi Crossref).

**Parameter utama.** Ukuran populasi, jumlah iterasi, dan parameter `z` yang mengatur skala langkah. Sedikit parameter.

**Biaya komputasi.** Satu evaluasi per individu per iterasi; populasi 30 x 100 iterasi sekitar 3.000 evaluasi.

**Kebutuhan evaluasi fitness.** Satu skalar; karena bobot bergantung pada peringkat fitness relatif, fungsi fitness yang bising membuat peringkat tidak stabil antar iterasi.

**Bukti literatur domain.**

| Rujukan | Peran bukti |
|---|---|
| Qiao 2025, "Optimizing LSSVM for Bearing Fault Diagnosis Using Adaptive t-Distribution Slime Mold Algorithm", Electronics, `10.3390/electronics14234568` | SMA mengoptimasi LSSVM pada diagnosis bantalan, peran T1 pada domain getaran |
| Fu 2025, "Multi-coupling fault detection and diagnosis of photovoltaic arrays with improved slime mould algorithm and PolyCatBoost", Process Safety and Environmental Protection, `10.1016/j.psep.2024.11.135` | SMA pada deteksi dan diagnosis gangguan |
| Hu 2022, "Dispersed foraging slime mould algorithm: Continuous and binary variants for global optimization and wrapper-based feature selection", Knowledge-Based Systems, `10.1016/j.knosys.2021.107761` | SMA versi kontinu dan biner untuk seleksi fitur wrapper (188 sitasi) |
| Ewees 2023, "Gradient-based optimizer improved by Slime Mould Algorithm for global optimization and feature selection for diverse computation problems", Expert Systems with Applications, `10.1016/j.eswa.2022.118872` | SMA untuk seleksi fitur |

**Kesesuaian dengan kasus kita.** Ini satu-satunya algoritma pada dokumen yang punya bukti domain untuk **kedua** peran yang relevan: T1 (Qiao 2025, mengoptimasi LSSVM pada getaran) dan T2 (Hu 2022, versi biner wrapper). Jadi secara profil bukti, SMA lebih seimbang daripada GWO atau BGWO.

**Skor: 4.** Alasan: bukti domain mencakup dua peran sekaligus (T1 dan T2) dengan rujukan 2019 sampai 2025, dan versi biner sudah tersedia di literatur sehingga tidak perlu diturunkan sendiri (K2 baik). Dikurangi karena SMA dan Slime Mould adalah algoritma yang sama sehingga tidak boleh dihitung dua kali sebagai bukti independen.

**Peran diusulkan: feature selection (T2) prioritas kedua setelah BGWO, dan tuning (T1) sebagai alternatif. Diperlakukan sebagai satu unit dengan Slime Mould §2.14.**

### 2.9 BGWO (Binary Grey Wolf Optimizer)

**Mekanisme.** Versi biner GWO yang dirancang khusus untuk seleksi fitur. Posisi setiap serigala menjadi vektor biner, dan perpindahan kontinu dari GWO dipetakan ke 0 atau 1 dengan fungsi transfer berbentuk S atau V. Basis: Emary 2016 (`10.1016/j.neucom.2015.06.083`, 1.316 sitasi Crossref).

**Parameter utama.** Ukuran populasi, jumlah iterasi, jenis dan parameter fungsi transfer. **Pemilihan fungsi transfer adalah keputusan desain besar** yang memengaruhi hasil, dan itu sendiri satu parameter bebas tambahan.

**Biaya komputasi.** Satu evaluasi per individu per iterasi. Untuk 55 dimensi, praktik lazim adalah populasi 20 sampai 30 dengan 100 iterasi, yaitu 2.000 sampai 3.000 evaluasi, jauh di atas anggaran 1.000 yang ditetapkan. Anggaran harus dipotong eksplisit (misalnya populasi 10 x 50 iterasi = 500).

**Kebutuhan evaluasi fitness.** Wajib multiobjektif atau bergabung dengan penalti: kinerja klasifikasi **dan** jumlah fitur terpilih, karena tanpa penalti BGWO akan memilih hampir semua 55 fitur dan tidak memberi manfaat operasional.

**Bukti literatur domain.**

| Rujukan | Peran bukti |
|---|---|
| Souaidia 2022, "Independent vector analysis based on binary grey wolf feature selection and extreme learning machine for bearing fault diagnosis", The Journal of Supercomputing, `10.1007/s11227-022-04931-4` | BGWO untuk seleksi fitur **pada diagnosis bantalan**, paling dekat dengan kebutuhan kita |
| Al-Tashi 2020, "Binary Multi-Objective Grey Wolf Optimizer for Feature Selection in Classification", IEEE Access, `10.1109/access.2020.3000040` | BGWO multiobjektif untuk seleksi fitur (136 sitasi) |
| Ramasamy Rajammal 2022, `10.1016/j.knosys.2022.108701` | BGWO dengan mutasi untuk seleksi fitur pada diagnosis penyakit |

**Kesesuaian dengan kasus kita.** Ini satu-satunya algoritma pada dokumen yang **dirancang sejak awal** untuk ruang biner dan punya bukti domain getaran (Souaidia 2022). Untuk T2 pada 55 fitur, ini kandidat paling tepat secara jenis ruang keputusan.

**Peringatan yang harus melekat.** Peran T2 adalah peran paling rawan overfitting pada 9 well: memilih subset dari 55 fitur berdasarkan 9 fold adalah 55 keputusan biner yang diuji pada 9 titik. Karena itu BGWO hanya boleh dipakai dengan protokol bersarang, dan hasilnya harus dibandingkan dengan (a) tanpa seleksi fitur sama sekali, dan (b) seleksi sederhana berbiaya rendah (misalnya importance dari RF atau korelasi). Tanpa dua pembanding itu, kenaikan metrik tidak bisa diatribusikan ke BGWO.

**Skor: 4.** Alasan: jenis ruang keputusan paling cocok (K2 terbaik di dokumen ini), bukti domain getaran langsung (K1 kuat), implementasi tersedia. Dikurangi karena biaya bawaan melebihi anggaran dan peran T2 sendiri berisiko tinggi (K4).

**Peran diusulkan: feature selection (T2), prioritas pertama, dengan syarat protokol bersarang dan dua pembanding.**

### 2.10 EO (Equilibrium Optimizer)

**Mekanisme.** Meniru model kesetimbangan massa pada volume kendali. Konsentrasi partikel diperbarui menuju keadaan kesetimbangan yang diperkirakan dari empat partikel terbaik plus satu rata-rata, dengan laju perpindahan yang menurun sepanjang iterasi. Basis: Faramarzi 2020 (`10.1016/j.knosys.2019.105190`, 2.249 sitasi Crossref).

**Parameter utama.** Ukuran populasi, jumlah iterasi, dan tiga koefisien `a1`, `a2`, `gp` yang mengatur laju perpindahan dan probabilitas pembangkitan. Jumlah parameter sedang.

**Biaya komputasi.** Satu evaluasi per individu per iterasi; populasi 30 x 100 iterasi sekitar 3.000 evaluasi.

**Kebutuhan evaluasi fitness.** Satu skalar per partikel; versi biner membutuhkan fungsi transfer seperti halnya BGWO.

**Bukti literatur domain.**

| Rujukan | Peran bukti |
|---|---|
| Gao 2020, "An Efficient Binary Equilibrium Optimizer Algorithm for Feature Selection", IEEE Access, `10.1109/access.2020.3013617` | EO biner untuk seleksi fitur (110 sitasi) |
| Ahmed 2021, "AIEOU: Automata-based improved equilibrium optimizer with U-shaped transfer function for feature selection", Knowledge-Based Systems, `10.1016/j.knosys.2021.107283` | EO untuk seleksi fitur |
| Too 2020, "General Learning Equilibrium Optimizer: A New Feature Selection Method for Biological Data Classification", Applied Artificial Intelligence, `10.1080/08839514.2020.1861407` | EO untuk seleksi fitur pada klasifikasi data biologis |

**Celah bukti yang harus dinyatakan.** Pencarian khusus putaran 2 untuk "equilibrium optimizer fault diagnosis" dan "equilibrium optimizer vibration fault detection" **tidak menghasilkan satu pun rujukan diagnosis gangguan atau getaran**. Hasil yang muncul adalah paper yang memakai kata "optimizer" dalam arti lain (misalnya "Adam optimizer" pada CNN). Jadi bukti domain untuk EO terbatas pada **seleksi fitur di domain medis dan biologis**, nol pada fault diagnosis, getaran, pengeboran, atau PdM.

**Kesesuaian dengan kasus kita.** Secara peran hanya bisa masuk T2, dan pada T2 ia kalah bukti dari BGWO (yang punya rujukan diagnosis bantalan langsung).

**Skor: 2.** Alasan: nol bukti domain fault diagnosis atau getaran atau pengeboran setelah pencarian khusus; bukti hanya seleksi fitur generik (K1 lemah). Tidak ada alasan memilihnya di atas BGWO untuk peran yang sama (K2 tidak unggul).

**Peran diusulkan: tidak dipakai pada gelombang ini.** Dicatat sebagai algoritma dengan bukti domain tidak memadai untuk kasus PdM pengeboran.

### 2.11 HBO (Heap-Based Optimizer)

**Mekanisme.** Meniru hierarki pangkat dalam organisasi korporat. Solusi disusun sebagai struktur heap dengan atasan dan bawahan, dan perpindahan individu mengikuti aturan mengikuti atasan ditambah pengaruh rekan sejawat. Basis: Askari 2020 (`10.1016/j.eswa.2020.113702`, 367 sitasi Crossref).

**Parameter utama.** Ukuran populasi, jumlah iterasi, dan parameter yang mengatur rasio pengaruh atasan terhadap rekan.

**Biaya komputasi.** Satu evaluasi per individu per iterasi; populasi 30 x 100 iterasi sekitar 3.000 evaluasi.

**Kebutuhan evaluasi fitness.** Satu skalar per individu; versi biner untuk seleksi fitur membutuhkan fungsi transfer.

**Bukti literatur domain.** Setelah filter judul dan domain, hanya **dua** rujukan bertahan:

| Rujukan | Peran bukti |
|---|---|
| Lee 2022, "A Feature Selection Approach Hybrid Grey Wolf and Heap-Based Optimizer Applied in Bearing Fault Diagnosis", IEEE Access, `10.1109/access.2022.3177735` | HBO dipakai **bersama GWO** pada diagnosis bantalan; bukan HBO murni |
| Ali 2022, "An Efficient Heap Based Optimizer Algorithm for Feature Selection", Mathematics, `10.3390/math10142396` | HBO untuk seleksi fitur, domain umum |

**Peringatan.** Ini tepat memenuhi syarat minimum dua rujukan, tetapi **satu-satunya rujukan diagnosisnya adalah hibrida dengan GWO**. Artinya bukti tersebut tidak dapat dipakai untuk memisahkan kontribusi HBO dari kontribusi GWO. Memakai rujukan itu sebagai bukti keunggulan HBO adalah kesalahan atribusi.

**Kesesuaian dengan kasus kita.** Perannya tumpang tindih sepenuhnya dengan GWO, sedangkan bukti mandirinya paling tipis di antara semua algoritma pada dokumen ini.

**Skor: 2.** Alasan: bukti diagnosis hanya tersedia dalam bentuk hibrida sehingga tidak bisa dipisahkan (K1 lemah secara atribusi), dan peran yang ditawarkan tidak berbeda dari GWO yang buktinya jauh lebih kuat (K2 tidak unggul).

**Peran diusulkan: tidak dipakai pada gelombang ini.**

### 2.12 Honey Badger Optimizer (unit pembanding, bukan singkatan HBO yang dipakai)

**Mekanisme.** Meniru dua perilaku mencari makan luak madu: menggali (mengikuti aroma kuat, eksploitasi) dan madu (mengikuti panduan burung pemandu, eksplorasi). Intensitas aroma menurun sepanjang iterasi.

**Parameter utama.** Ukuran populasi, jumlah iterasi, parameter penurunan intensitas, dan konstanta pengaturan eksplorasi.

**Biaya komputasi.** Satu evaluasi per individu per iterasi, sekitar 3.000 evaluasi pada populasi 30 x 100 iterasi.

**Kebutuhan evaluasi fitness.** Satu skalar per kandidat.

**Bukti literatur domain.** Justru lebih banyak daripada HBO Heap-Based:

| Rujukan | Peran bukti |
|---|---|
| Ma 2022, "Composite Fault Diagnosis of Rolling Bearing Based on Chaotic Honey Badger Algorithm Optimizing VMD and ELM", Machines, `10.3390/machines10060469` | luak madu mengoptimasi VMD dan ELM pada diagnosis bantalan |
| Ting 2025, "Improved Honey Badger Algorithm Based on Elite Tangent Search and Differential Mutation with Applications in Fault Diagnosis", Processes, `10.3390/pr13010256` | varian perbaikan untuk diagnosis gangguan |
| Chen 2022, "Sensor Fault Diagnosis of Aero Engine Control System Based on Honey Badger Optimizer", IFAC-PapersOnLine, `10.1016/j.ifacol.2022.05.040` | diagnosis sensor pada sistem kendali mesin pesawat |

**Kesesuaian dengan kasus kita.** Bukti domain cukup untuk T1. Tetapi kehadirannya di dokumen ini adalah konsekuensi disambiguasi nama, bukan permintaan kartu.

**Skor: 3.** Alasan: bukti domain diagnosis memadai (tiga rujukan), tetapi perannya tidak berbeda dari GWO, WOA, dan HHO, dan tidak ada alasan terukur untuk memilihnya. Angka 3 diberikan karena bukti, bukan karena kebutuhan.

**Peran diusulkan: pembanding bila ada anggaran lebih; tidak dipakai pada gelombang ini.**

### 2.13 Horse Herd Optimization (HOA)

**Mekanisme.** Meniru perilaku kawanan kuda yang terbagi dalam kelompok sosial berdasarkan usia (foal, filly, colt, stallion), masing-masing dengan aturan perpindahan berbeda. Basis: MiarNaeimi 2021 (`10.1016/j.knosys.2020.106711`, 376 sitasi Crossref).

**Parameter utama.** Ukuran populasi, jumlah iterasi, dan pembagian proporsi kelompok usia.

**Biaya komputasi.** Satu evaluasi per individu per iterasi, sekitar 3.000 evaluasi pada populasi 30 x 100 iterasi.

**Kebutuhan evaluasi fitness.** Satu skalar; versi biner (BinHOA) membutuhkan fungsi transfer.

**Bukti literatur domain.** Hasil filter hanya **tiga** rujukan, dan tidak satu pun menyentuh fault diagnosis, getaran, pengeboran, atau PdM:

| Rujukan | Peran bukti |
|---|---|
| Preyanka Lakshme 2025, "Feature selection using binary horse herd optimization algorithm with lightGBA ensemble classification in microarray data", Knowledge-Based Systems, `10.1016/j.knosys.2025.113168` | HOA biner untuk seleksi fitur pada data mikroarray |
| Elmanakhly 2022, "BinHOA: Efficient Binary Horse Herd Optimization Method for Feature Selection: Analysis and Validations", IEEE Access, `10.1109/access.2022.3156593` | varian biner untuk seleksi fitur, domain umum |
| Zaimoğlu 2023, "A binary chaotic horse herd optimization algorithm for feature selection", Engineering Science and Technology, an International Journal, `10.1016/j.jestch.2023.101453` | varian biner chaos untuk seleksi fitur |

**Celah bukti.** Pencarian khusus putaran 2 ("horse herd optimization algorithm fault diagnosis", "horse herd optimization predictive maintenance") tidak menemukan rujukan diagnosis atau PdM. Bukti yang ada seluruhnya seleksi fitur pada data biologis atau domain umum.

**Kesesuaian dengan kasus kita.** Hanya bisa masuk T2, dan pada T2 buktinya kalah langsung dari BGWO yang punya rujukan diagnosis bantalan.

**Skor: 2.** Alasan: nol bukti domain fault diagnosis, getaran, pengeboran, atau PdM setelah pencarian khusus; bukti hanya seleksi fitur generik (K1 lemah). Peran yang sama sudah ditempati BGWO dengan bukti lebih kuat.

**Peran diusulkan: tidak dipakai pada gelombang ini.**

### 2.14 Slime Mould Algorithm (unit duplikat dari SMA)

**Mekanisme.** Sama dengan §2.8. Basis: Li 2020 (`10.1016/j.future.2020.03.055`).

**Bukti literatur domain.**

| Rujukan | Peran bukti |
|---|---|
| Hu 2022, "Dispersed foraging slime mould algorithm: Continuous and binary variants for global optimization and wrapper-based feature selection", Knowledge-Based Systems, `10.1016/j.knosys.2021.107761` | varian kontinu dan biner, seleksi fitur wrapper (188 sitasi) |
| Deng 2023, "A multi-strategy improved slime mould algorithm for global optimization and engineering design problems", Computer Methods in Applied Mechanics and Engineering, `10.1016/j.cma.2022.115764` | perbaikan multi-strategi (92 sitasi) |
| Qiao 2025, `10.3390/electronics14234568` | diagnosis bantalan melalui optimasi LSSVM |

**Pernyataan duplikasi.** Butir ini dan §2.8 menunjuk algoritma yang sama. Bukti di atas **tidak menambah** jumlah bukti independen untuk algoritma tersebut. Bila panitia menghitung "12 algoritma", jumlah algoritma berbeda yang benar-benar dinilai adalah **11** (karena SMA sama dengan Slime Mould), dan jumlah unit penilaian 14 karena SSA dibelah dan Honey Badger ditambah.

**Skor: 4** (skor algoritma, bukan skor tambahan). **Peran diusulkan: sama dengan §2.8, satu paket.**

---

## 3. TABEL RINGKAS

Legenda peran: T1 = tuning hyperparameter, T2 = feature selection, T3 = kalibrasi ambang per well, X = tidak dipakai.

| Algoritma | Rujukan terverifikasi (tahun) | Kebutuhan data untuk fitness | Risiko utama | Skor | Peran diusulkan |
|---|---|---|---|---|---|
| GWO | 2022 (Lee), 2022 (Xie), 2020 (Gu), 2022 (Ramasamy Rajammal) | 1 skalar per kandidat, idealnya AUPRC antar fold + penalti dispersi | biaya 3.000 evaluasi melampaui anggaran 300 (10x) | **4** | T1 |
| WOA | 2024 (wang), 2022 (Huang), 2025 (Li), 2026 (Liu) | idem GWO | seluruh bukti dari sinyal getaran mentah, bukan fitur MWD tabular | **4** | T1 (paling relevan untuk vib) |
| PSO | 2020 (Fan), 2019 (Huang), 2021 (Sobhi, pengeboran), 2024 (Ebrahimabadi, pengeboran) | skalar ternormalisasi, parameter diskalakan | tiga parameter bebas (`w`, `c1`, `c2`) memperburuk overfitting seleksi | **4** | T1 + pembanding implementasi |
| SSA-Salp | 2024 (Lee), 2020 (Neggaz), 2022 (Zivkovic) | skalar + penalti jumlah fitur | peran didukung literatur (T2) adalah peran paling rawan | **3** | T2 kandidat kedua |
| SSA-Sparrow | 2021 (Xing), 2024 (Xu), 2023 (Ma), 2024 (Wang) | skalar | bukti berpusat pada jaringan mendalam dan VMD, keduanya tidak dipakai di kasus kita | **3** | X |
| HHO | 2021 (Shao), 2022 (Long), 2024 (Liang) | skalar | tujuh fase internal, risiko salah implementasi tertinggi | **3** | T1 kandidat ketiga |
| EPO | 2024 (Lee), 2021 (Dhiman), 2023 (Singh) | skalar + penalti jumlah fitur | bukti hanya seleksi fitur; fungsi transfer menentukan hasil | **3** | T2 alternatif ketiga |
| SMA | 2025 (Qiao), 2025 (Fu), 2022 (Hu), 2023 (Ewees) | skalar + penalti jumlah fitur | duplikat dengan Slime Mould, tidak boleh dihitung dua kali | **4** | T2 prioritas kedua, T1 alternatif |
| BGWO | 2022 (Souaidia), 2020 (Al-Tashi), 2022 (Ramasamy Rajammal) | multiobjektif: kinerja + jumlah fitur | 55 keputusan biner diuji pada 9 titik; butuh protokol bersarang | **4** | **T2 prioritas pertama** |
| EO | 2020 (Gao), 2021 (Ahmed), 2020 (Too) | skalar + penalti jumlah fitur | **nol** bukti fault diagnosis/getaran/pengeboran setelah pencarian khusus | **2** | X |
| HBO (Heap-Based) | 2022 (Lee, hibrida GWO), 2022 (Ali) | skalar + penalti jumlah fitur | satu-satunya bukti diagnosis adalah hibrida, tidak bisa dipisahkan | **2** | X |
| Honey Badger (pembanding) | 2022 (Ma), 2025 (Ting), 2022 (Chen) | skalar | peran identik GWO/WOA/HHO tanpa keunggulan terukur | **3** | X (cadangan) |
| Horse Herd | 2025 (Preyanka), 2022 (Elmanakhly), 2023 (Zaimoğlu) | skalar + penalti jumlah fitur | **nol** bukti fault diagnosis/PdM setelah pencarian khusus | **2** | X |
| Slime Mould (duplikat SMA) | 2022 (Hu), 2023 (Deng), 2025 (Qiao) | idem SMA | sama dengan SMA; bukan bukti tambahan | **4** | sama dengan SMA |

Rekonsiliasi jumlah: kartu meminta 12 nama. Dokumen menilai **14 unit**: 12 nama ditambah SSA-Sparrow dan Honey Badger (pembanding) dikurangi nol, karena SMA dan Slime Mould tetap ditulis dua baris walau satu algoritma. **Jumlah algoritma berbeda yang benar-benar dinilai: 11.**

---

## 4. REKOMENDASI

### 4.1 Yang diusulkan untuk gelombang pilot

| Prioritas | Algoritma | Peran | Alasan yang bisa dipertahankan di depan PM |
|---|---|---|---|
| 1 | **BGWO** | T2 feature selection pada 55 fitur | satu-satunya algoritma yang dirancang untuk ruang biner dan punya bukti diagnosis bantalan langsung; dimensi 55 adalah masalah nyata karena kontrak sekarang memakai semua 55 fitur |
| 2 | **GWO** atau **WOA** | T1 tuning hyperparameter 4 sampai 6 dimensi | bukti domain terkuat, parameter paling sedikit, ruang kontinu cocok; WOA lebih relevan untuk engine vib |
| 3 | **SMA** | T2 alternatif dan T1 alternatif | satu-satunya yang punya bukti untuk dua peran sekaligus, sehingga bisa dipakai sebagai pemeriksaan silang hasil BGWO |

### 4.2 Syarat yang harus dipenuhi sebelum satu pun dijalankan

1. **Pembanding anggaran-sama.** Setiap run metaheuristik wajib disandingkan dengan random search pada jumlah evaluasi identik, dan dengan baseline tanpa tuning (kontrak seed 42), memakai fold yang sama. Tanpa ini, kenaikan metrik tidak bisa diatribusikan ke algoritma.
2. **Protokol bersarang.** Seleksi hyperparameter dan subset fitur hanya di dalam fold latih. Fold uji tidak boleh dilihat optimizer. Ini bukan saran, ini syarat agar angka bisa dipakai di gate plan §6.
3. **Fungsi fitness yang menghukum dispersi.** Rata-rata AUPRC antar fold saja akan memilih konfigurasi yang ekstrem di satu well. Minimalkan rata-rata dikurangi sebagian dispersi, atau gunakan median, atau laporkan keduanya dan tolak kandidat yang hanya menang di satu fold.
4. **Pra-registrasi.** Kunci protokol, metrik, dan aturan penolakan sebelum run. Pencarian besar ditambah kebebasan memilih metrik agregat adalah kombinatorik yang hampir pasti menghasilkan "temuan".
5. **Batas evaluasi dipatuhi.** Lihat §1.3. Populasi dan iterasi dipilih agar total evaluasi tidak melewati anggaran, bukan sebaliknya.

### 4.3 Yang TIDAK diusulkan, dan alasannya

| Algoritma | Alasan penolakan |
|---|---|
| EO, Horse Herd | nol bukti domain fault diagnosis, getaran, pengeboran, atau PdM setelah pencarian khusus putaran 2 |
| HBO (Heap-Based) | bukti diagnosis hanya tersedia dalam bentuk hibrida dengan GWO, sehingga tidak bisa dipisahkan; peran identik GWO |
| SSA-Sparrow | bukti berpusat pada jaringan mendalam dan VMD; VMD sudah dinyatakan tidak layak oleh D0 (laju sampel maksimum 0,3333 Hz) |
| Honey Badger | bukti ada, tetapi peran identik GWO/WOA tanpa keunggulan terukur; cadangan bila anggaran tersisa |
| HHO | risiko implementasi tertinggi (tujuh fase) tanpa keunggulan yang bisa dibuktikan pada 4 sampai 6 dimensi dan anggaran 300 evaluasi |
| EPO, SSA-Salp | hanya mendukung T2, dan T2 sudah ditempati BGWO dengan bukti lebih kuat |

### 4.4 Temuan yang lebih penting daripada peringkat algoritma

**Pembatas sebenarnya bukan pilihan optimizer, melainkan portabilitas ambang antar well.** Angkanya sudah ada: satu ambang tetap untuk vib menghasilkan FAR 4,1 sampai 496 antar well (119 kali), CI RF shk memuat prevalensi di 7 dari 9 fold, sedangkan hyd persistence tidak memuatnya di 0 dari 9 fold (`docs/V9_EVAL_C_LAYERC.md` §2). Artinya masalah utama adalah **ketidakstabilan antar unit**, dan itu masalah kalibrasi serta jumlah unit, bukan masalah pencarian hyperparameter.

Konsekuensi praktis: menaruh seluruh anggaran pada metaheuristik untuk tuning adalah salah alokasi. Perbaikan yang lebih mungkin berdampak adalah (a) kalibrasi ambang per well yang prospektif dan dapat diaudit, dan (b) penggantian model ke boosting yang lebih terkendali, yang sudah dibahas kartu R4. Metaheuristik di dokumen ini paling masuk akal dipakai untuk **T2 (mengurangi 55 fitur)** karena di sana ia menyelesaikan masalah nyata (dimensi tinggi pada 9 unit), bukan untuk T1 yang hanya menggeser hyperparameter pada ruang 4 sampai 6 dimensi dengan 9 titik evaluasi.

---

## 5. YANG BELUM TERVERIFIKASI DAN BELUM TERUKUR

Daftar ini bagian dari hasil, bukan lampiran. Semua butir di bawah **tidak dipakai** sebagai dasar rekomendasi di §4.

1. **Biaya waktu dinding per evaluasi fitness: BELUM TERUKUR.** Tidak ada pengukuran latensi fit RF atau LightGBM pada data nyata di kartu ini, sehingga tidak ada angka detik. Biaya dilaporkan hanya sebagai jumlah evaluasi fitness (sifat struktural algoritma).
2. **Tidak ada satu pun run metaheuristik di repo ini: BELUM ADA.** Karenanya tidak ada klaim kenaikan metrik dari algoritma mana pun pada dokumen ini. Semua skor adalah penilaian kelayakan berbasis bukti literatur dan struktur masalah, bukan hasil eksperimen.
3. **Teks penuh sebagian rujukan: TIDAK DIVERIFIKASI.** Yang diverifikasi hanya DOI resolve (HTTP 302) dan metadata Crossref. Klaim tentang isi metode di setiap paper bersandar pada judul, dan untuk beberapa pada pengetahuan umum tentang algoritma, bukan pada pembacaan teks penuh. Pengukuran pass 2 (§0.4) memberi angka: 23 dari 55 rujukan mengembalikan 403 atau 202 ketika halaman penerbit diminta secara otomatis, sehingga untuk rujukan itu abstrak pun tidak terbaca dari sumber. Bila sebuah paper ternyata memakai varian yang berbeda dari yang diasumsikan, penilaian peran untuk paper itu bisa berubah.
4. **Tahun terbit Kennedy & Eberhart 1995: dari judul prosiding, bukan field tanggal Crossref** (field `issued` kosong pada record `10.1109/icnn.1995.488968`).
5. **Jumlah fitur LightGBM: BELUM TERUKUR.** Rentang 4 sampai 6 dimensi untuk T1 adalah target desain yang saya tetapkan, bukan hasil inventaris kode. Yang terverifikasi dari kode hanya kontrak RF (`n_estimators=200`, seed 42) dan pernyataan "tanpa grid search" (`docs/V9_PM1_ARCHITECTURE.md:356`).
6. **Anggaran evaluasi 300 / 100 / 1.000: KONVENSI desain**, bukan hasil pengukuran kapasitas mesin. Bisa berubah setelah Engineer mengukur waktu dinding nyata.
7. **Kelayakan T2 pada 9 well: BELUM DIUJI.** Pernyataan bahwa feature selection berisiko tinggi adalah argumen struktural (55 keputusan biner diuji pada 9 titik), bukan hasil eksperimen di repo ini. Uji pembeda yang diperlukan: bandingkan subset hasil BGWO melawan tanpa seleksi dan melawan seleksi importance sederhana pada fold bersarang.
8. **Rujukan pengeboran untuk metaheuristik: TIPIS.** Hanya Sobhi 2021 dan Ebrahimabadi 2024, keduanya tentang prediksi laju penembusan, **bukan** tentang optimasi ambang alarm PdM pada data pengeboran. Tidak ada rujukan yang mengoptimasi ambang alarm PdM dengan metaheuristik pada data pengeboran yang berhasil ditemukan.
9. **Pemetaan Honey Badger dan SSA-Sparrow sebagai unit tambahan adalah keputusan dokumen ini**, bukan permintaan kartu. Bila panitia menghendaki 12 unit persis, kedua unit itu bisa dilebur tanpa mengubah rekomendasi.
10. **Verifikasi silang sitasi:** jumlah sitasi pada tabel berasal dari field `is-referenced-by-count` Crossref pada tanggal akses. Angka itu bergerak dan tidak dipakai sebagai kriteria skor.

---

## 6. RINGKASAN 5 BARIS

1. Dari 309 DOI yang diperiksa, 309 resolve dan 58 rujukan masuk registry dengan 55 di antaranya dikutip di sini untuk 11 algoritma berbeda (12 nama kartu, SMA sama dengan Slime Mould): bukti domain terkuat ada pada WOA, GWO, dan BGWO.
2. Rekomendasi utama bukan "algoritma terbaik", melainkan **BGWO untuk feature selection 55 fitur** dan **GWO atau WOA untuk tuning 4 sampai 6 dimensi**, keduanya wajib disandingkan dengan random search beranggaran sama.
3. EO dan Horse Herd ditolak karena nol bukti fault diagnosis/getaran/pengeboran setelah pencarian khusus; HBO ditolak karena satu-satunya bukti diagnosisnya adalah hibrida dengan GWO.
4. Pembatas sebenarnya bukan optimizer, tetapi portabilitas ambang antar well: FAR vib menyebar 119 kali dan CI RF shk memuat prevalensi di 7 dari 9 fold, sehingga anggaran lebih baik diarahkan ke kalibrasi ambang dan boosting daripada ke tuning.
5. Dengan hanya 9 well, setiap pencarian di atas 1.000 evaluasi adalah mesin penghafal noise; protokol bersarang, pembanding anggaran-sama, dan pra-registrasi adalah syarat, bukan saran.

## 7. DAFTAR BELUM TERVERIFIKASI (ringkas)

Biaya waktu dinding per evaluasi (belum terukur) · tidak ada run metaheuristik di repo (belum ada) · teks penuh 55 rujukan dikutip tidak dibaca, dan 23 di antaranya bahkan tidak bisa diminta otomatis (403/202) · tahun Kennedy 1995 dari judul prosiding · jumlah dimensi LightGBM (target desain) · anggaran 300/100/1.000 (konvensi desain) · kelayakan T2 pada 9 well (belum diuji, argumen struktural) · rujukan pengeboran hanya 2 dan bukan tentang ambang alarm PdM · jumlah sitasi bergerak.
