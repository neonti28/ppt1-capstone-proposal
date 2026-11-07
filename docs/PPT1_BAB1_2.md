# BAB I 1.2: IDENTIFIKASI MASALAH: FISHBONE 6M DAN 5W1H

**Proyek:** Perancangan Terpadu, deteksi dini kegagalan Bottom Hole Assembly berbasis pembelajaran mesin
**Mitra:** PT Halliburton Indonesia, divisi Sperry Drilling (jalur Magang/MBKM, pedoman butir 2.8c)
**Kartu kerja:** t_39eac1b2 · **Basis:** pedoman resmi halaman 33 sampai 36, butir BAB I 1.2
**Berkas bukti mesin:** `scratch/ppt1/fishbone.json` (27 sebab, 6 kategori, seluruhnya berjejak)

---

## 0. Riset pendahuluan yang dipakai

- **Riset pendahuluan: riset-dulu-baru-perbaiki**: urutan wajib masalah, riset, tulis opsi dan bukti, baru perbaiki; gate tidak boleh berubah setelah hasil terlihat.
- **Riset pendahuluan: scientific-critical-thinking**: pisahkan data dari interpretasi, korelasi dari kausalitas, dan nyatakan kekuatan klaim sebanding dengan kekuatan bukti; kegagalan satu hipotesis bukan bukti hipotesis lain benar.
- **Riset pendahuluan: hypothesis-generation**: objek harus tetap terpisah: observasi, hipotesis, mekanisme, prediksi, penjelasan rival; hipotesis adalah usulan yang harus ditantang, bukan temuan. Setiap hipotesis di dokumen ini diberi prediksi pembeda agar dapat difalsifikasi.

---

## 1. Batas masalah dan definisi status

Fishbone ini menjawab satu pertanyaan: **mengapa peringatan dini kegagalan BHA berbasis data operasi Sperry Drilling belum dapat dioperasikan sebagai alarm, padahal data historisnya tersedia.** Fishbone memetakan sebab. Penilaian risiko terkuantifikasi (FMEA dengan skala rujukan) berada pada kartu terpisah, sehingga skor S, O, dan D dari draft 13 Agustus 2026 tidak diulang di sini.

Setiap sebab diberi satu status, dengan arti yang dipakai konsisten di seluruh dokumen:

| Status | Arti | Konsekuensi pemakaian |
|---|---|---|
| **TERBUKTI** | Angka dihitung ulang pada sesi ini langsung dari berkas primer (CSV atau JSON hasil eksekusi) | Boleh dipakai sebagai landasan kalimat proposal |
| **TERBUKTI-DOKUMEN** | Angka tercatat pada dokumen audit tim dengan metode yang dinyatakan, namun tidak direplikasi pada sesi ini | Boleh dipakai, wajib menyebut sumber dan menyatakan belum direplikasi |
| **HIPOTESIS** | Mekanisme masuk akal dan konsisten dengan bukti lain, tetapi belum diukur | Dilarang ditulis sebagai temuan; wajib disertai uji pembeda |

Tautan sebab ke akibat juga diberi status terpisah. Sebuah besaran boleh TERBUKTI sementara **tautan kausalnya** masih HIPOTESIS. Pemisahan ini disengaja, karena korelasi bukan kausalitas.

---

## 2. Angka dasar yang menjadi landasan seluruh fishbone

Seluruh angka pada tabel ini dihitung ulang pada sesi ini dari berkas primer.

| Besaran | Nilai | Jejak yang dapat dijalankan ulang |
|---|---|---|
| Kejadian terkurasi | **884** baris | `data/volve/labels_curated_v2.csv`, jumlah baris data |
| Total durasi kejadian | **73.500 menit = 1.225 jam** | kolom `act_start` dan `act_end`, selisih per baris, dijumlahkan |
| Median durasi | **45 menit** | distribusi durasi 884 baris |
| Persentil 90 durasi | **180 menit** | idem |
| Durasi maksimum | **780 menit** | idem |
| Sumur tercakup | **10 wellbore** | kolom `wellbore` |
| Kejadian tanpa bukti kegagalan | **496 dari 884 = 56,1 persen** | kolom `category` nilai `routine_no_failure_evidence` |
| Kejadian relevan BHA | **50 dari 884 = 5,7 persen** | kolom `bha_relevant` nilai `yes` |
| Kejadian relevansi BHA belum pasti | **571 dari 884 = 64,6 persen** | kolom `bha_relevant` nilai `uncertain` |
| Detektor dan head | **7 mode, 27 head** (4+4+4+6+4+2+3) | `scratch/v9_i1/v9_i1_RESULTS.json` `engines[].heads` |
| Sebaran lapis keputusan | **L0 = 5, L1 = 11, L2 = 9, L3 = 2** | `decision_layer.ringkasan` |
| Sebaran tier | **13 TREN, 12 PERINGATAN-BERPENGAWAS, 2 BELUM LAYAK PAKAI** | `engines[].heads[].tier` |
| Slot alarm otomatis kritis | **0** | `auto_critical_alarm_slots` |
| Peringatan L1 yang harus dibaca manusia | **11** | `decision_layer.nperingatan_l1` |

Catatan tafsir yang mengikat: 884 kejadian **bukan** 884 kerusakan. Karena 56,1 persen basis tidak memuat bukti kegagalan, setiap kalimat dampak pada proposal wajib menyebut basis mana yang dipakai. Angka 1.225 jam adalah total waktu tercatat pada basis 884 kejadian, bukan waktu downtime murni.

![Gambar 3](assets/fig02_kategori_per_wellbore.png)

**Gambar 3.** Matriks kejadian per kategori per wellbore, sembilan kategori dikalikan sepuluh wellbore, total 884 kejadian. Skala warna memakai normalisasi pangkat 0,55 supaya sel kecil tetap terlihat, dan sel nol ditulis `0` dengan warna terang supaya tidak disamakan dengan data hilang. Dua baris teratas, yaitu `routine_no_failure_evidence` (496 kejadian) dan `surface_rig_equipment` (216 kejadian), mengisi 80,5 persen dari seluruh matriks. Konsentrasi kejadian per wellbore menyebar dari 2 (F-15 B) sampai 182 (F-14). Skrip sumber: `docs/assets/make_figures.py`, fungsi `fig02_kategori`.

---

## 3. Fishbone 6M

Diagram terdiri atas satu tulang punggung (efek) dan enam cabang, dengan 27 ranting. Identitas cabang dan ranting dipakai juga pada gambar G1 (lihat Bagian 6).

**Efek pada kepala ikan:** peringatan dini kegagalan BHA belum dapat dioperasikan sebagai alarm, karena ambang tidak portabel, label belum tervalidasi, dan kanal sensor tidak lengkap.

### 3.1 MAN (manusia): 4 ranting

| ID | Cabang | Ranting (sebab spesifik) | Status | Jejak |
|---|---|---|---|---|
| M1 | Validitas label buatan manusia | Kontrol-positif stick-slip tidak lulus: **0 dari 10** kontrol-positif stuck gagal, sehingga presisi dan recall kelas stuck dihitung dari basis label yang belum tervalidasi | TERBUKTI-DOKUMEN | `docs/V8_M1_CAPABILITY_MAP.md` baris 198 (kolom G7); `docs/V8_PM_VERDICT.md` baris 202; `docs/V4_MAINTENANCE_ML_OPTIONS.md` baris 149 |
| M2 | Validitas label buatan manusia | Relevansi BHA tidak diputuskan: **571 dari 884 (64,6 persen)** berstatus `uncertain`, hanya **50 (5,7 persen)** dinyatakan `yes` | TERBUKTI | `data/volve/labels_curated_v2.csv` kolom `bha_relevant`, 884 baris |
| M3 | Validitas label buatan manusia | Label hidraulik K-ii memakai **proksi** perubahan volume pit (ΔV_pit), bukan pengukuran hidraulika lubang bor, sehingga label berisiko sirkular terhadap fitur | TERBUKTI-DOKUMEN | `docs/V8_M1_CAPABILITY_MAP.md` baris 198 (hyd K-ii label proxy); `docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md` baris 300 |
| M4 | Rantai keputusan manusia | Seluruh keluaran berhenti di manusia: **0 slot alarm otomatis**, **11 peringatan L1** harus dibaca, beban waktu baca insinyur belum pernah diukur | TERBUKTI | `scratch/v9_i1/v9_i1_RESULTS.json` kunci `auto_critical_alarm_slots`, `human_review_required`, `decision_layer.nperingatan_l1` |

**Tautan ke G7.** G7 pada peta kapabilitas didefinisikan sebagai *validitas label lintas well*, dengan tiga komponen yang semuanya muncul di atas: kontrol-positif stuck 0/10, label hidraulik sebagai proksi, dan semantik `STUCK_RT` 0 sampai 3 yang belum ada. Karena itu cabang MAN adalah akar, bukan gejala.

### 3.2 METHOD (metode): 5 ranting

| ID | Cabang | Ranting (sebab spesifik) | Status | Jejak |
|---|---|---|---|---|
| Me1 | Ambang tunggal lintas sumur | Satu nilai ambang (τ = 0,5) dipakai untuk semua sumur. Pada model dan ambang yang sama, laju alarm palsu bergerak dari **4,14897** per 24 jam di F-15_S sampai **496,09249** per 24 jam di F-14, yaitu rentang **119,57 kali** | TERBUKTI | `scratch/v9_e_ml/v9_e_ML_vib_RESULTS.json` → `folds[].models.rf.tau_metrics["0.5"].FAR_24jam` |
| Me2 | Ambang tunggal lintas sumur | Ambang yang sama juga meruntuhkan sensitivitas: recall pada τ = 0,5 adalah **0,1018** di F-15_S tetapi **0,8657** di F-14 | TERBUKTI | berkas JSON yang sama, kunci `...recall` |
| Me3 | Ketidakpastian statistik | Pada **5 dari 9** fold, selang kepercayaan 95 persen AUPRC menyentuh garis no-skill, sehingga keunggulan atas tebakan acak belum terpisah dari derau | TERBUKTI-DOKUMEN | `docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md` baris 562; contoh CI95 fold F-10 `[0,06008; 0,25484]` pada `scratch/v9_e_ml/v9_e_ML_ssi_RESULTS.json` |
| Me4 | Resolusi waktu pipeline | Pipeline memaksa grid 60 detik mode ALL-rows, sedangkan laju kanal permukaan diasumsikan sekitar 1 Hz. Bila laju nyata per sumur lebih rendah, satu bin dapat berisi kurang dari 10 sampel dan aturan SSI tidak dapat dievaluasi | HIPOTESIS | `docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md` baris 296 dan 1177; `SSI_MIN_SAMPLES = 10` baris 1567 |
| Me5 | Hirarki keluaran | 7 mode dan 27 head tersebar ke empat lapis dengan sebaran tier 13/12/2, tanpa aturan kenaikan tier yang dinyatakan sebagai ambang angka | TERBUKTI | `scratch/v9_i1/v9_i1_RESULTS.json` → `engines[].heads`, `decision_layer.ringkasan` |

**Catatan penting untuk Me1 dan Me2.** Kedua angka berasal dari satu kunci JSON yang sama, pada model dan ambang yang identik. Yang berubah hanya sumur uji. Inilah bukti langsung bahwa ambang global tidak portabel, dan sekaligus alasan mengapa target "satu ambang untuk semua sumur" harus digugurkan pada BAB III.

### 3.3 MACHINE (mesin dan perkakas): 4 ranting

| ID | Cabang | Ranting (sebab spesifik) | Status | Jejak |
|---|---|---|---|---|
| Ma1 | Arsitektur keluaran alat | Alat tidak memiliki slot alarm otomatis kritis sama sekali (**0**), dan **0 dari 7** detektor memenuhi syarat alarm. Ini keputusan desain yang dinyatakan, bukan cacat implementasi | TERBUKTI | `scratch/v9_i1/v9_i1_RESULTS.json` `auto_critical_alarm_slots`; `docs/V8_PM_VERDICT.md` baris 180 dan 41 |
| Ma2 | Cakupan parser | Parser CSV lama hanya menangani 8 kolom keluaran, sehingga **3906 dari 7150 berkas log (54,6 persen)** tidak pernah diparse: F-1 C sebanyak 2156 berkas dan F-11 sebanyak 1750 berkas. Kurva HKLD, TORQUE, MSE, MOTOR_RPM, dan FLOWIN-OUT juga tidak masuk | TERBUKTI-DOKUMEN | `docs/V6_D0_READERS_SYNTHESIS.md` baris 49 |
| Ma3 | Efek agregasi pipeline | Agregasi ALL-rows ke satu nilai per menit berpotensi meredam puncak getaran dan torsi berdurasi detik, sehingga label status menjadi lebih konservatif daripada kejadian fisiknya | HIPOTESIS | `docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md` baris 1179 |
| Ma4 | Cakupan pembuktian prototipe | Prototipe dijalankan pada satu segmen nyata (F-14), yang kebetulan satu-satunya wellbore hadir di keenam dataset rig. Perilaku alat sebagai sistem utuh pada sumur lain belum diuji | TERBUKTI | `scratch/v9_i1/v9_i1_RESULTS.json` `meta.segmen_rig` dan `segmen_info.*.n` |

### 3.4 MATERIAL (bahan dan data): 4 ranting

| ID | Cabang | Ranting (sebab spesifik) | Status | Jejak |
|---|---|---|---|---|
| Mt1 | Integritas kanal permukaan | `WHIRL_RT` dan `BOUNCE_RT` identik: **67 berkas pada 5 wellbore**, dan **1790 dari 1790** nilai identik di F-9 (F-5 368/368, F-15S 5/5, F-1 15/15). Keduanya tidak boleh menjadi dua fitur atau dua gejala | TERBUKTI-DOKUMEN | `docs/V6_A1_DATA_AUDIT.md` baris 100 dan 101; `docs/V6_D0_READERS_SYNTHESIS.md` baris 174 |
| Mt2 | Kelengkapan kanal MWD | Kanal CRPM bahan rumus SSI tidak lengkap: **22.385 dari 35.906 jendela (62,34 persen)** tanpa data pada agregat sembilan fold, dan dua sumur kanal mati (F-7 982/982, F-9 1126/1126) | TERBUKTI | `scratch/v9_eval_c/v9_eval_c_RESULTS.json` → `C_rule_status.ssi.sensor_nodata_rule`; `docs/V9_A1_AUDIT.md` baris 56 |
| Mt3 | Makna basis kejadian | Kejadian tercatat bukan sama dengan kegagalan: **496** tanpa bukti kegagalan, **47** bukti campuran, **28** kegagalan tanpa lokasi, dan hanya **50** kejadian menyangkut BHA (stuck atau fishing 38, peralatan downhole 12) | TERBUKTI | `data/volve/labels_curated_v2.csv` kolom `category`, 884 baris |
| Mt4 | Ketidakseimbangan kelas | Prevalensi positif sangat rendah dan tidak seragam: ssi F-15A **31 dari 6020 = 0,51 persen**, ssi F-7 **3 dari 982 = 0,31 persen**, ssi F-9_A **55 dari 841 = 6,54 persen** | TERBUKTI | `scratch/v9_eval_a/v9_eval_a_RESULTS.json` → `rule_status.classes.ssi.folds[].prev` |

**Catatan untuk Mt1 dan Mt2.** Mt1 berasal dari audit tim atas 19 GB data primer, Mt2 dari berkas hasil evaluasi. Keduanya tidak saya ulang karena keduanya menuntut pemindaian data mentah berskala besar. Statusnya karena itu dinyatakan terbuka.

### 3.5 MEASUREMENT (pengukuran): 5 ranting

| ID | Cabang | Ranting (sebab spesifik) | Status | Jejak |
|---|---|---|---|---|
| Ms1 | Basis waktu | Waktu pada dataset turunan adalah **indeks menit internal** (`ts_bin`), dan asal kalender dinyatakan belum diverifikasi, sehingga join dengan tanggal kejadian pada CSV label rentan pergeseran | TERBUKTI | `scratch/v9_i1/v9_i1_RESULTS.json` → `segmen_info.vib.catatan_waktu`; rentang `segmen_info.ssi.ts_bin_min` 19947192 sampai 20223025 |
| Ms2 | Satuan metrik | Laju alarm palsu muncul dalam beberapa satuan pada berkas berbeda (`FAR_24jam`, `far_24h`, serta laju per jendela), sehingga perbandingan lintas detektor rawan salah baca bila satuan tidak diseragamkan | TERBUKTI | `scratch/v9_e_ml/v9_e_ML_vib_RESULTS.json` (`FAR_24jam`) dibanding `scratch/v9_e_rule/v9_e_RULE_01_status_results.json` (`far_24h`) |
| Ms3 | Skala penilaian risiko | Angka severity, occurrence, dan detection pada FMEA draft **ditulis langsung sebagai literal** pada skrip pembuat dokumen, bukan hasil penilaian dengan skala rujukan. Perkalian RPN konsisten, yang belum berdasar adalah nilai masukannya | TERBUKTI | `docs/PPT1_LEDGER_ANGKA.md` (grup A draft docx, temuan kunci FMEA); `scratch/ppt1/ledger.json` |
| Ms4 | Target kinerja | Target recall 0,70 sampai 0,80 dan target lead time 10 sampai 30 menit **belum dicapai** hasil terukur mana pun; lead time yang terukur hanya **4,5 sampai 8,5 menit** dan terbatas pada satu kelas | TERBUKTI-DOKUMEN | `docs/V8_PM_VERDICT.md` baris 186; `docs/PPT1_LEDGER_ANGKA.md` temuan kunci target KPI |
| Ms5 | Definisi label versus metrik | Label ssi didefinisikan sebagai deteksi **kondisi berlangsung** (SSI minimal 1), bukan onset, sehingga recall-nya tidak sebanding dengan head yang didefinisikan sebagai onset | TERBUKTI-DOKUMEN | `docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md` baris 3208 dan 1567 |

### 3.6 ENVIRONMENT (lingkungan dan sensor): 5 ranting

| ID | Cabang | Ranting (sebab spesifik) | Status | Jejak |
|---|---|---|---|---|
| En1 | Sensor peralatan downhole | **Rating motor tidak ada pada 0 dari 192 berkas** (torqueMax, Pmax, rpmMax, powerMax, revPerGallon, torque), sehingga batas operasi motor tidak dapat dipakai sebagai pembanding beban terukur | TERBUKTI-DOKUMEN | `docs/V6_A1_DATA_AUDIT.md` baris 58; `docs/V10_D1_BAB_DATA.md` baris 173; `docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md` baris 1031 |
| En2 | Sensor tekanan formasi | Tekanan pori EDM fase ACTUAL hanya **8 baris**, semuanya di datum air laut (tvd 298,56 ft); kurva tekanan formasi atau mud weight untuk indikator overbalance **tidak ada** setelah empat lapis pemeriksaan | TERBUKTI-DOKUMEN | `docs/V7_M2_SYNTHESIS.md` baris 58; `docs/V7_D1f_DATA_CHECK.md` baris 45 |
| En3 | Riwayat peralatan | Informasi penajaman bit (`dullingInfo`) **tidak ada pada 0 dari 161 berkas**, sehingga keausan bit hanya dapat didekati dari identitas run | TERBUKTI-DOKUMEN | `docs/V6_A1_DATA_AUDIT.md` baris 146 |
| En4 | Variasi kondisi antar sumur | Porsi waktu pengeboran berbeda tajam: F-14 **12.635 dari 96.698 bin (13,1 persen)**, F-12 **23.931 dari 180.958 bin (13,2 persen)**, F-10 **13.781 dari 41.446 bin (33,3 persen)** | TERBUKTI | `scratch/v9_d1/v9_d1_01_summary.json` → `wells.*.n_bins`, `wells.*.n_bins_drill` |
| En5 | Kualitas kanal getaran | Pada F-10 kanal `VIBLAT_RT` tercatat **hadir**, tetapi jumlah bin dengan observasi getaran adalah **0**. Kanal yang ada di skema tidak menjamin ada data | TERBUKTI | `scratch/v9_d1/v9_d1_01_summary.json` → `wells.F-10.bins_with_vib_obs`, `wells.F-10.label_channels_present` |

**Catatan untuk En5.** Ini kasus paling tajam untuk kalimat "keterbatasan sensor", karena `crpm_present: true` dan `spm_present: true` juga berlaku untuk F-10, sementara kanal getarannya kosong. Bukti ketiadaan haruslah hitungan observasi, bukan keberadaan nama kanal.

---

## 4. Rekap status sebab

| Status | Jumlah | Proporsi |
|---|---|---|
| TERBUKTI | 15 | 55,6 persen |
| TERBUKTI-DOKUMEN | 10 | 37,0 persen |
| HIPOTESIS | 2 | 7,4 persen |
| **Total** | **27** | 100 persen |

Sebaran per kategori: Man 4, Method 5, Machine 4, Material 4, Measurement 5, Environment 5. Seluruh 27 sebab memiliki minimal satu rujukan berkas atau kunci JSON.

**Dua sebab berstatus HIPOTESIS** adalah Me4 (resolusi grid 60 detik melawan laju stream) dan Ma3 (puncak sinyal teredam agregasi). Keduanya sengaja dipertahankan karena menjelaskan pola nodata dan konservatisme label, tetapi keduanya dilarang ditulis sebagai temuan pada BAB IV.

Selain dua sebab di atas, terdapat **tautan kausal** yang masih HIPOTESIS meskipun besarannya TERBUKTI. Contoh: nilai FAR 119,57 kali adalah terukur, sedangkan pernyataan bahwa ambang global adalah **penyebab** utama ketidaklayakan alarm masih merupakan inferensi, karena portabilitas juga dipengaruhi prevalensi (Mt4) dan kelengkapan kanal (Mt2).

---

## 5. 5W1H

Tabel ini disusun agar setiap sel konsisten dengan angka pada Bagian 2 dan Bagian 3. Tidak ada angka baru yang diperkenalkan di sini.

| Unsur | Isi | Dasar dan status |
|---|---|---|
| **What** (apa masalahnya) | Belum tersedia peringatan dini kegagalan BHA yang layak dioperasikan sebagai alarm: **0 dari 7** detektor memenuhi syarat alarm, **0** slot alarm otomatis kritis, **2 dari 27** head berstatus BELUM LAYAK PAKAI, dan **5 dari 9** fold CI95 menyentuh no-skill | `v9_i1_RESULTS.json`, `V8_PM_VERDICT.md` baris 180, dokumen desain baris 562. TERBUKTI dan TERBUKTI-DOKUMEN |
| **Why** (mengapa penting) | Terdapat **884 kejadian** terkurasi dengan total **73.500 menit (1.225 jam)** waktu tercatat, median **45 menit**, p90 **180 menit**, maksimum **780 menit**. Namun **496 (56,1 persen)** di antaranya tidak memuat bukti kegagalan, sehingga nilai masalah harus dinyatakan atas basis yang jelas, bukan atas seluruh 1.225 jam | `labels_curated_v2.csv`. TERBUKTI |
| **Who** (siapa yang terlibat) | Pengguna hasil: insinyur pengeboran dan insinyur optimasi Sperry Drilling, karena keputusan akhir dinyatakan berada pada manusia (`human_review_required: true`). Penyedia data dan kurator label: pihak internal mitra. Pelaksana: mahasiswa. Pengarah akademik: dosen pembimbing. Tidak ada peran otomatis yang ditambahkan | `v9_i1_RESULTS.json`, `V8_PM_VERDICT.md` baris 41. TERBUKTI |
| **Where** (di mana) | Lingkungan data: **10 wellbore** lapangan Volve dengan penamaan NO 15/9-F-*. Segmen pembuktian prototipe: **F-14**, satu-satunya wellbore yang hadir di keenam dataset rig (vib 1989, ssi 5455, shk 11205, stuck_k1 3201, stuck_k2 95925, hyd_ki 10401 jendela). Cakupan fisik: kanal permukaan dan sebagian kanal MWD, tanpa tekanan formasi dan tanpa rating motor | `labels_curated_v2.csv`, `v9_i1_RESULTS.json`, `V6_A1_DATA_AUDIT.md` baris 58, `V7_D1f_DATA_CHECK.md` baris 45. TERBUKTI dan TERBUKTI-DOKUMEN |
| **When** (kapan) | Rentang data **2007 sampai 2015** (F-14 sendiri mencakup rentang panjang dengan hanya 13,1 persen bin pengeboran). Horizon peringatan yang dicita-citakan **10 sampai 30 menit** sebelum kejadian, sedangkan lead yang terukur baru **4,5 sampai 8,5 menit** dan belum pada semua kelas. Basis waktu internal masih berupa indeks menit tanpa verifikasi kalender | `V11_DATA1.md` baris 65 untuk rentang, `V8_PM_VERDICT.md` baris 186 untuk lead, `v9_i1_RESULTS.json` `catatan_waktu`. TERBUKTI dan TERBUKTI-DOKUMEN |
| **How** (bagaimana) | Alur: log sumur menjadi grid bin **60 detik** mode ALL-rows, menjadi **6 dataset latih 292.954 baris**, diuji dengan **37 fold** LOWO (4+9+9+2+9+4) tanpa pelanggaran anti-bocor, dinilai dengan FAR, recall, AUPRC, dan CI95, lalu disusun menjadi lapis keputusan **L0 sampai L3** dengan manusia di ujung rantai | `ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md` baris 1177 dan 1317, `V10_A1_AUDIT.md` baris 155, `v9_i1_RESULTS.json` `decision_layer`. TERBUKTI |

**Uji konsistensi 5W1H.** Tiga angka muncul di lebih dari satu sel dan harus sama: jumlah kejadian (884) pada Why dan basis Where, jumlah detektor (7) pada What dan Who, serta lead time (10 sampai 30 menit sebagai target, 4,5 sampai 8,5 menit sebagai hasil) pada When. Ketiganya konsisten dengan Bagian 2 dan Bagian 3.

---

## 6. Spesifikasi gambar G1

Gambar G1 adalah diagram tulang ikan dengan orientasi kiri ke kanan. Kepala di kanan memuat efek, tulang punggung horizontal, enam cabang berselang-seling atas dan bawah, dan 27 ranting. Daftar berikut adalah kontrak gambar, sehingga penggambar tidak perlu menafsirkan apa pun.

**Kepala (efek):** "Peringatan dini kegagalan BHA belum dapat dioperasikan sebagai alarm".

| Cabang | Posisi | Label cabang | Ranting (kode dan teks pendek) |
|---|---|---|---|
| B1 | atas 1 | **MAN** (4) | M1 kontrol-positif 0/10; M2 relevansi BHA 571/884 belum pasti; M3 label hidraulik proksi; M4 beban baca manusia 11 peringatan |
| B2 | bawah 1 | **METHOD** (5) | Me1 FAR 4,15 sampai 496,09 (119,57 kali); Me2 recall 0,10 sampai 0,87; Me3 CI95 5/9 menyentuh no-skill; Me4 grid 60 detik melawan 1 Hz; Me5 tier 13/12/2 tanpa ambang naik |
| B3 | atas 2 | **MACHINE** (4) | Ma1 slot alarm 0 dan 0/7 mode; Ma2 3906/7150 berkas tidak diparse; Ma3 puncak teredam agregasi; Ma4 satu segmen bukti F-14 |
| B4 | bawah 2 | **MATERIAL** (4) | Mt1 WHIRL sama dengan BOUNCE 1790/1790; Mt2 nodata CRPM 22.385/35.906; Mt3 496/884 tanpa bukti gagal; Mt4 prevalensi 0,31 sampai 6,54 persen |
| B5 | atas 3 | **MEASUREMENT** (5) | Ms1 basis waktu tanpa kalender; Ms2 satuan FAR tidak seragam; Ms3 S/O/D literal generator; Ms4 target belum tercapai; Ms5 kondisi disamakan dengan onset |
| B6 | bawah 3 | **ENVIRONMENT** (5) | En1 rating motor 0/192; En2 tekanan EDM 8 baris datum; En3 dullingInfo 0/161; En4 porsi drilling 13,1 persen; En5 VIBLAT F-10 nol observasi |

**Aturan gaya gambar G1.**
1. Ranting berstatus HIPOTESIS (Me4, Ma3) diberi garis putus-putus, bukan garis penuh.
2. Ranting berstatus TERBUKTI-DOKUMEN diberi penanda bintang kecil, dengan catatan kaki "belum direplikasi pada sesi ini".
3. Setiap ranting membawa kode (M1 sampai En5) yang identik dengan tabel Bagian 3, agar silang rujuk ke naskah tidak ambigu.
4. Dua angka wajib tercetak pada gambar karena merupakan bukti terkuat: **119,57 kali** pada Me1 dan **62,34 persen** pada Mt2.
5. Warna: cabang MAN dan MATERIAL satu keluarga warna karena keduanya menyumbang akar G7; cabang MACHINE dan MEASUREMENT keluarga kedua karena keduanya soal perkakas dan satuan.

**Kerangka Mermaid untuk G1** (dapat langsung dipakai sebagai titik awal di Mermaid Live, lalu diekspor ke draw.io bila diperlukan):

```
mindmap
  root((Peringatan dini BHA belum layak alarm))
    MAN
      M1 kontrol-positif 0/10
      M2 relevansi BHA 571/884
      M3 label hidraulik proksi
      M4 beban baca manusia
    METHOD
      Me1 FAR 119,57 kali
      Me2 recall 0,10 s/d 0,87
      Me3 CI95 5/9 no-skill
      Me4 grid 60 dtk lawan 1 Hz
      Me5 tier tanpa ambang naik
    MACHINE
      Ma1 slot alarm 0
      Ma2 3906/7150 tak terparse
      Ma3 puncak teredam
      Ma4 satu segmen F-14
    MATERIAL
      Mt1 WHIRL sama BOUNCE
      Mt2 nodata CRPM 62,34 persen
      Mt3 496/884 tanpa bukti gagal
      Mt4 prevalensi 0,31 s/d 6,54 persen
    MEASUREMENT
      Ms1 waktu tanpa kalender
      Ms2 satuan FAR tak seragam
      Ms3 S/O/D literal
      Ms4 target belum tercapai
      Ms5 kondisi lawan onset
    ENVIRONMENT
      En1 rating motor 0/192
      En2 tekanan EDM 8 baris
      En3 dullingInfo 0/161
      En4 drilling 13,1 persen
      En5 VIBLAT F-10 nol
```

---

## 7. Hipotesis, penjelasan rival, dan uji pembeda

Bagian ini memenuhi syarat bahwa setiap HIPOTESIS wajib punya prediksi yang dapat membedakannya dari penjelasan rival. Tanpa ini, hipotesis hanya opini.

### 7.1 Me4: nodata disebabkan resolusi grid, bukan sensor rusak

- **Observasi:** nodata CRPM agregat 22.385 dari 35.906 jendela (62,34 persen), sementara pada F-14 kanal CRPM justru hadir pada 11.794 dari 12.635 bin pengeboran.
- **Hipotesis:** sebagian nodata timbul karena aturan minimal 10 sampel per bin tidak terpenuhi pada laju logging rendah, bukan karena kanal fisik mati.
- **Rival 1:** kanal memang mati pada sumur tertentu (didukung F-7 982/982 dan F-9 1126/1126).
- **Rival 2:** nodata berasal dari pemetaan nama mnemonic yang gagal, bukan dari ketiadaan nilai.
- **Prediksi pembeda:** bila hipotesis benar, nodata seharusnya menumpuk pada bin dengan jumlah sampel mentah rendah, dan **hilang** setelah grid dilonggarkan ke 2 atau 5 menit. Bila rival 1 benar, nodata tetap 100 persen meskipun grid dilonggarkan. Bila rival 2 benar, nodata berkorelasi dengan sumur, bukan dengan kelimpahan sampel.
- **Uji yang dapat dijalankan:** hitung histogram jumlah sampel mentah per bin untuk sembilan sumur, lalu ulangi perhitungan SSI dengan bin 2 menit dan bandingkan fraksi nodata. Kedua rival memberi tanda yang berlawanan, sehingga uji ini memisahkan keduanya.
- **Status:** HIPOTESIS, belum dijalankan.

### 7.2 Ma3: agregasi menit meredam puncak sinyal

- **Observasi:** label status dibangun dari satu nilai per menit, dengan puncak-puncak berdurasi detik tidak terwakili pada statistik bin.
- **Hipotesis:** sebagian negatif palsu berasal dari agregasi, bukan dari keterbatasan model.
- **Rival:** negatif palsu murni akibat ambang dan prevalensi, seperti ditunjukkan Me1, Me2, dan Mt4.
- **Prediksi pembeda:** bila hipotesis benar, mengganti statistik bin dari mode ALL-rows ke nilai maksimum akan menaikkan recall tanpa menaikkan FAR secara proporsional. Bila rival benar, recall dan FAR naik bersama pada rasio yang sama.
- **Uji yang dapat dijalankan:** bandingkan dua varian agregasi pada fold yang sama dengan ambang tetap, lalu bandingkan pasangan (recall, FAR).
- **Status:** HIPOTESIS, belum dijalankan.

### 7.3 Tautan kausal yang masih terbuka

Pernyataan "ambang global adalah penyebab utama alarm tidak layak" belum berstatus TERBUKTI walaupun angka 119,57 kali terukur. Alasannya, portabilitas juga dipengaruhi prevalensi per sumur (Mt4) dan kelengkapan kanal (Mt2). Uji pembeda yang disarankan: normalkan ambang per sumur berdasarkan kuantil prevalensi, lalu ukur apakah dispersi FAR menyempit. Bila menyempit tajam, ambang global terbukti sebagai penyebab dominan. Bila tidak, penyebab dominan ada pada data, bukan pada metode.

---

## 8. Catatan kejujuran angka

Dua hal ditemukan saat menyusun dokumen ini dan wajib dicatat agar tidak beredar sebagai angka tanpa jejak.

**Pertama, angka "nodata CRPM F-14 = 96,6 persen" tidak dapat direproduksi.** Angka itu tercatat di `docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md` baris 563 dan 3312. Namun dari `scratch/v9_d1/v9_d1_01_summary.json`, F-14 memiliki `bins_with_crpm_obs` sebesar 11.794 dari `n_bins` 96.698 (nodata 87,80 persen) dan dari `n_bins_drill` 12.635 (nodata 6,66 persen). Tidak ada penyebut yang menghasilkan 96,6 persen. Karena itu angka tersebut **tidak dipakai sebagai landasan** pada dokumen ini, dan digantikan oleh dua angka yang dapat dihitung ulang, yaitu 62,34 persen agregat dan 87,80 persen untuk F-14 atas seluruh grid bin.

**Kedua, token `SSI_mwd` tidak ditemukan di repositori.** Pencarian ripgrep pada `docs/` versi v2 dan `docs/` arsip menghasilkan nol kecocokan. Frasa pada kartu kerja dipetakan ke kuantitas terukur yang setara, yaitu jumlah jendela SSI valid F-14 sebesar 5.455 dari 96.698 bin (5,64 persen) dengan 75 positif, ditambah nodata CRPM agregat 62,34 persen. Pemetaan ini dicatat, bukan disembunyikan, agar pembaca dapat menilai kesetaraannya sendiri.

Kedua catatan ini bukan penilaian atas dokumen tim. Keduanya adalah jejak penelusuran yang membuat naskah lebih kuat, karena setiap angka yang dipakai kini punya cara pembuktian ulang.

---

## 9. Daftar berkas rujukan

| Berkas | Dipakai untuk |
|---|---|
| `data/volve/labels_curated_v2.csv` | 884 kejadian, distribusi kategori, `bha_relevant`, durasi |
| `scratch/v9_i1/v9_i1_RESULTS.json` | 7 mode, 27 head, lapis L0 sampai L3, tier, slot alarm, metadata segmen |
| `scratch/v9_e_ml/v9_e_ML_vib_RESULTS.json` | FAR dan recall per fold pada τ = 0,5 |
| `scratch/v9_e_ml/v9_e_ML_ssi_RESULTS.json` | CI95 AUPRC contoh fold, prevalensi |
| `scratch/v9_eval_a/v9_eval_a_RESULTS.json` | n dan prevalensi per fold sembilan sumur |
| `scratch/v9_eval_c/v9_eval_c_RESULTS.json` | nodata sensor ssi dan shk, pemangkasan FP hybrid |
| `scratch/v9_e_rule/v9_e_RULE_01_status_results.json` | nama kunci `far_24h`, metrik rule per fold |
| `scratch/v9_d1/v9_d1_01_summary.json` | grid per sumur, bin drilling, observasi kanal |
| `docs/V8_M1_CAPABILITY_MAP.md` | definisi G7 dan komponennya |
| `docs/V8_PM_VERDICT.md` | 0/7 alarm, keputusan desain, lead time |
| `docs/V4_MAINTENANCE_ML_OPTIONS.md` | urutan perbaikan G7 lebih dulu |
| `docs/V6_A1_DATA_AUDIT.md` | WHIRL sama dengan BOUNCE, rating motor 0/192, dullingInfo 0/161 |
| `docs/V6_D0_READERS_SYNTHESIS.md` | 3906 dari 7150 berkas tidak terparse |
| `docs/V7_M2_SYNTHESIS.md` | tekanan EDM ACTUAL 8 baris |
| `docs/V7_D1f_DATA_CHECK.md` | kurva tekanan formasi tidak ada |
| `docs/V9_A1_AUDIT.md` | nodata per sumur, kanal mati F-7 dan F-9 |
| `docs/V10_D1_BAB_DATA.md` | rating motor 0/192, rincian data |
| `docs/V11_DATA1.md` | bin F-14, rekonsiliasi angka |
| `docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md` | grid 60 detik, definisi label, batas CI95, rating motor |
| `docs/PPT1_LEDGER_ANGKA.md` | status FMEA S/O/D, status target KPI |
| `scratch/ppt1/fishbone.json` | 27 sebab dalam bentuk mesin, seluruh jejak |

---

## 10. Pemenuhan kriteria penerimaan

| Kriteria | Target | Hasil | Bukti |
|---|---|---|---|
| Kategori 6M dengan sebab | 6 kategori, masing-masing minimal 3 | 6 kategori, sebaran 4/5/4/4/5/5 | Bagian 3, `fishbone.json` `kategori_6m` |
| Sebab berujuk berkas atau JSON | minimal 8 | 27 dari 27 (100 persen) | `fishbone.json`, larik sebab dengan kunci `evidence` |
| Hipotesis ditandai | ada penandaan eksplisit | 2 sebab HIPOTESIS, ditambah penandaan terpisah untuk tautan kausal | Bagian 1, 4, dan 7 |
| 5W1H konsisten dengan bukti | 6 unsur, tanpa angka baru | 6 unsur, seluruh angka merujuk Bagian 2 dan 3 | Bagian 5 |
| Daftar cabang dan ranting untuk G1 | dapat digambar tanpa tafsir | 6 cabang, 27 ranting berkode, plus kerangka Mermaid | Bagian 6 |
| Angka berjejak | tidak ada angka tanpa jejak | Seluruh angka pada tabel berasal dari CSV atau JSON, atau ditandai TERBUKTI-DOKUMEN | Bagian 2, 3, 8 |
