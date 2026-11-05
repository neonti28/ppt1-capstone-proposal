# BAB III ANALISIS ALTERNATIF SOLUSI

## 3.1 Permasalahan & Alternatif Solusi

| Kendali dokumen | Keterangan |
|---|---|
| Dokumen | Proposal Proyek Perancangan Terpadu I, BAB III subbab 3.1 |
| Mitra | PT Halliburton Indonesia, divisi Sperry Drilling |
| Versi | 1.0, 25 Oktober 2026 |
| Status | Berjalan, subbab 3.2 sampai 3.4 belum disusun |
| Acuan format | Buku Pedoman PPT Tahap I, subbab 3.2 Format Proposal, halaman 33 sampai 36 |
| Acuan BoK | Buku Pedoman PPT Tahap I Tabel 2.1, empat belas IEBoK, selaras IISE ISEBoK 2021 |
| Identitas anggota | Diisi tim. Dokumen ini tidak mengarang nama maupun NIM. |

### 3.1.1 Dasar penyusunan dan aturan bukti

Riset pendahuluan: `grounded-citations` - setiap angka pada subbab ini melekat pada sumber yang sudah diekstrak, dan blok bukti memuat kunci jejak berupa berkas dan nomor baris, bukan ingatan.

Riset pendahuluan: `formal-project-documents` - register formal baku tanpa penanda status dalam tanda kurung, tanpa emoji, dan setiap konsep teknis dituliskan sebagai definisi, tujuan, alasan pemilihan, serta batasnya.

Riset pendahuluan: `sequentialthinking` (sequ-mcp, empat pikiran) - inventaris dua puluh dua sumber, uji tiga skema pembagian anggota, verifikasi status eksekusi per solusi, lalu penetapan pembagian berbasis lapisan intervensi (data dan label, formulasi model, sinyal fisik dan operasi).

Sembilan alternatif pada subbab ini disusun dari inventaris solusi yang sudah berkode di dalam proyek, yaitu tiga belas solusi S-A1 sampai S-D4 beserta empat solusi pendukung pada bagian kelas rapuh (S-E1, S-E2, S-F1, S-F2), tiga opsi peningkatan pada dokumen opsi ML, dan dua lever pasca-V9 (6a perbaikan label, 6b kalibrasi ambang per sumur). Seluruh dua puluh dua sumber dipetakan tepat satu kali ke sembilan alternatif, sehingga tidak ada alternatif yang menduplikasi mekanisme alternatif lain, dan tidak ada sumber yang hilang tanpa rumah.

Aturan bukti yang dipakai pada seluruh subbab:

1. Setiap angka menyebut berkas dan nomor baris, kunci JSON, atau skrip yang dapat dijalankan ulang.
2. Angka yang belum dihitung ditulis eksplisit sebagai asumsi atau perkiraan desain, dan tidak disamarkan sebagai hasil pengukuran.
3. Status pelaksanaan hanya memakai tiga nilai baku: Selesai, Berjalan, dan Rencana (belum terealisasi).

### 3.1.2 Permasalahan yang dirujuk

| Kode | Permasalahan | Uraian ringkas dan angka | Jejak |
|---|---|---|---|
| P1 | Label stuck berbentuk status, bukan peristiwa | Label STUCK_RT bertahan sebagai blok panjang sehingga jendela sebelumnya menjadi prediktor hampir sempurna. Prevalensi F-9_A 66,9%, persistence 0,787 mengalahkan Random Forest 0,651, dan lift F-9_A turun ke 0,97. | `docs/V7_R1_SOLUTIONS.md:66-70 (angka turunan docs/V6_E1_ML_DESIGN.md 4.4)` |
| P2 | Jumlah positif shk terlalu sedikit per fold | Gate G1 lolos 3 dari 7 fold sedangkan G2 lolos 6 dari 7, sehingga akarnya bukan mutu fitur melainkan jumlah informasi positif: F-9_A 30 positif dan F-9 45 positif, dibanding F-14 760 positif. | `docs/V7_R1_SOLUTIONS.md:97-99` |
| P3 | Label hyd adalah ambang residual dari proses yang persisten | Label diturunkan dari residual SPPA dengan ambang nilai mutlak z di atas 2 sehingga mewarisi persistensi proses. Persistence 0,42 sampai 0,63 mengalahkan Random Forest 0,11 sampai 0,61 pada 7 dari 7 fold, dan G1 hanya lolos 2 dari 7. | `docs/V7_R1_SOLUTIONS.md:127-131` |
| P4 | tool_wear terbatas 4 alat dengan label identitas run | Hanya 4 alat dan 2 run per alat (469 jendela), label berupa identitas run R01/R02 sehingga urutan percobaan ikut terkorelasi dengan label. Prevalensi sekitar 0,5 membatasi plafon lift pada 2,0; hasil nyata G1 0 dari 4 dengan lift 1,09 sampai 1,42. | `docs/V7_R1_SOLUTIONS.md:160-165` |
| P5 | bit_wear dikalahkan persistence pada seluruh fold | Gate G1 lolos 3 dari 4 dan G2 lolos 4 dari 4, tetapi persistence lebih tinggi daripada Random Forest pada 4 dari 4 fold karena label high-MSE membentuk blok lintas kedalaman. Aturan pra-registrasi menurunkan verdict menjadi layak bersyarat. | `docs/V7_R1_SOLUTIONS.md:203-205` |
| P6 | Sebagian fold ssi underpowered | ssi lolos G1 4 dari 5 dan G2 5 dari 5 dengan persistence 0 dari 5, tetapi F-7 hanya 3 positif dan F-9 hanya 12 positif sehingga selang kepercayaan melebar dan F-9_A gagal tipis pada lift 1,47. | `docs/V7_R1_SOLUTIONS.md:197-199` |
| P7 | Validitas label lintas sumur belum terbukti | Kontrol-positif stuck 0 dari 10, label hyd masih berupa proksi residual, dan campuran severitas berbeda antar sumur. Cacat ini mengancam seluruh lapisan onset sebelum model apa pun dipercaya. | `docs/V8_PM_VERDICT.md:202; docs/V4_MAINTENANCE_ML_OPTIONS.md:145-155` |
| P8 | Ambang global tidak portabel antar sumur | Pada titik operasi yang sama, false alarm rate vib menyebar 4,15 sampai 496,09 per 24 jam, yaitu rasio 119,6 kali antar sumur, sehingga satu ambang global tidak dapat dipakai. | `docs/V9_PM2_VERDICT.md:114` |
| P9 | Tidak ada label keausan fisik dari rig | Seluruh 77 berkas bhaRun tidak memuat dullingInfo, dullGrade, maupun bitName, sehingga label yang tersedia hanya batas waktu run, bukan tingkat keausan. Prediksi onset keausan bit (K-2) belum dijalankan sama sekali. | `docs/V4_MAINTENANCE_ML_OPTIONS.md:62; docs/V9_PM2_VERDICT.md:176` |

### 3.1.3 Tabel rekap sembilan alternatif

| No | Anggota | Alternatif solusi | Kode sumber | BoK | Masalah yang dirujuk | Dieksekusi di kampanye | Status |
|---|---|---|---|---|---|---|---|
| A1 | Anggota 1 | Relabeling onset peristiwa: dari status menjadi kejadian | S-A1, S-C1, S-F1 | 14, 11, 5 | P1, P3, P5 | V9, sebagian (stuck K-ii dan hyd K-ii) | Berjalan |
| A2 | Anggota 1 | Perluasan wellbore berkanal disfungsi (F-10, F-4, F-12, F-15) | S-B1, S-A2, S-E1 | 11, 5, 14 | P2, P6 | V9, akuisisi data (baris hasil parse) | Berjalan |
| A3 | Anggota 1 | Penjaminan mutu label dan label probabilistik multi-sumber | 6a, S-A3 | 5, 11, 14 | P7 | belum ada | Rencana (belum terealisasi) |
| A4 | Anggota 2 | Unit analisis per-stand pengeboran | S-B2 | 7, 5, 11 | P2, P6 | belum ada | Rencana (belum terealisasi) |
| A5 | Anggota 2 | Prediksi severity ordinal dengan evaluasi stabilitas fold | S-B3, S-E2 | 5, 2, 11 | P6, P7 | belum ada | Rencana (belum terealisasi) |
| A6 | Anggota 2 | Formulasi survival dan sisa umur pakai (time-to-event) | S-C3, V4-Opsi3 | 5, 3, 2 | P9, P3 | belum ada | Rencana (belum terealisasi) |
| A7 | Anggota 3 | Penguatan kampanye keausan alat bengkel: progresi, dekomposisi mode, dan ranking | S-D1, S-D2, S-D4 | 12, 5, 14 | P4 | V9, domain bengkel (K-i) | Berjalan |
| A8 | Anggota 3 | Label fisika pengganti label proksi | S-C2, S-D3, S-F2 | 10, 5, 11 | P3, P5, P9 | belum ada | Rencana (belum terealisasi) |
| A9 | Anggota 3 | Lapisan keputusan operasional: kalibrasi ambang per sumur dan purwarupa peringatan dini | 6b, V4-Opsi1, V4-Opsi2 | 1, 6, 3 | P8, P1 | belum ada | Rencana (belum terealisasi) |

Tiga anggota membagi lapisan intervensi, bukan kelas disfungsi. Pembagian ini dipilih karena satu pekerjaan akuisisi data melayani beberapa kelas sekaligus, sehingga pembagian per kelas akan menduplikasi mekanisme yang sama pada dua alternatif berbeda.

- Anggota 1 mengerjakan lapisan data dan label (A1 sampai A3).
- Anggota 2 mengerjakan lapisan formulasi model dan evaluasi (A4 sampai A6).
- Anggota 3 mengerjakan lapisan sinyal fisik, keausan, dan operasi (A7 sampai A9).

### 3.1.4 Rincian setiap alternatif

#### 3.1.4.1 A1 Relabeling onset peristiwa: dari status menjadi kejadian (Anggota 1)

**Ringkasan.** Mengubah definisi target dari status yang bertahan menjadi titik masuk peristiwa, sehingga dominasi persistence hilang secara konstruksi.

**Deskripsi teknis.** Untuk setiap deret label instrumen (STUCK_RT, residual SPPA pada hyd, dan label high-MSE pada bit_wear), onset t_e didefinisikan sebagai titik naik status. Jendela positif adalah jendela fitur yang berakhir dalam horizon H sebelum t_e, sedangkan jendela di dalam blok setelah onset dibuang dari evaluasi dan tidak dinegatifkan. Horizon H ditetapkan 10 menit dengan uji sensitivitas pada 5 dan 30 menit. Gate G1 (lift minimal 1,5 pada mayoritas sumur layak) dan G2 (AUPRC minimal AUPRC canary kedalaman) tidak diubah, sehingga perubahan hanya berada pada definisi label.

**Permasalahan yang diselesaikan.** P1, P3, P5. Label STUCK_RT bertahan sebagai blok panjang sehingga jendela sebelumnya menjadi prediktor hampir sempurna. Prevalensi F-9_A 66,9%, persistence 0,787 mengalahkan Random Forest 0,651, dan lift F-9_A turun ke 0,97. Label diturunkan dari residual SPPA dengan ambang nilai mutlak z di atas 2 sehingga mewarisi persistensi proses. Persistence 0,42 sampai 0,63 mengalahkan Random Forest 0,11 sampai 0,61 pada 7 dari 7 fold, dan G1 hanya lolos 2 dari 7. Gate G1 lolos 3 dari 4 dan G2 lolos 4 dari 4, tetapi persistence lebih tinggi daripada Random Forest pada 4 dari 4 fold karena label high-MSE membentuk blok lintas kedalaman. Aturan pra-registrasi menurunkan verdict menjadi layak bersyarat.

**Keterkaitan BoK.** BoK 14 Systems Design & Engineering; BoK 11 Information Engineering; BoK 5 Quality & Reliability Engineering. BoK 14 karena alternatif ini menetapkan ulang fungsi sistem yang diprediksi (kejadian, bukan status); BoK 11 karena perubahan berada pada rantai data dan label; BoK 5 karena metrik yang dipakai adalah metrik keandalan dan deteksi kegagalan.

**Bukti kelayakan dari proyek.**

- Formulasi onset sudah dijalankan untuk stuck dan menghasilkan peringatan dengan arah benar pada beban rendah: Random Forest pada titik operasi 0,05 memberi B1 0,51 sampai 1,00 dengan TLead 10 sampai 11,5 menit, sedangkan baseline persistence-EVENT hanya memberi TLead median 7,0 menit dengan B1 0 sampai 11,5 persen. Jejak: `docs/V9_EVAL_B_LAYERB.md:101`.
- Untuk hyd, formulasi yang sama menghasilkan B1 nol dari tiga onset dengan TLead nol, jadi hasil negatifnya terukur dan dilaporkan apa adanya. Jejak: `docs/V9_EVAL_B_LAYERB.md:103`.
- Relabel tidak memerlukan parse baru karena deret sumber sudah berbentuk CSV. Jejak: `docs/V7_R1_SOLUTIONS.md:76, 136, 204 (data/volve/witsml_parsed/*.csv, data/USROP_labeled.csv)`.

**Status pelaksanaan.** Berjalan. Sudah dieksekusi untuk stuck (K-ii) dan hyd (K-ii) pada kampanye V9. Belum dieksekusi untuk bit_wear K-2 karena pra-registrasi kampanye tersebut belum terbit.

**Asal usul.** 13 solusi berkode (S-A1, S-C1) dan solusi pendukung V7 6 (S-F1). Kode sumber: S-A1, S-C1, S-F1.

#### 3.1.4.2 A2 Perluasan wellbore berkanal disfungsi (F-10, F-4, F-12, F-15) (Anggota 1)

**Ringkasan.** Menambah sumur dan fold dengan memparse wellbore yang terbukti memiliki kanal disfungsi, bukan menurunkan ambang label.

**Deskripsi teknis.** Empat wellbore yang belum diparse (F-10, F-4, F-12, F-15) diproses ke CSV dengan protokol identik kampanye sebelumnya: grid 60 detik, agregasi menit, syarat kelayakan jendela yang sama. Hasilnya digabungkan ke kampanye leave-one-well-out per kelas sehingga jumlah fold dan jumlah positif naik tanpa mengubah definisi label maupun gate. Peta kanal dipakai sebagai syarat masuk: hanya wellbore yang benar-benar mendaftarkan mnemonic disfungsi yang diambil.

**Permasalahan yang diselesaikan.** P2, P6. Gate G1 lolos 3 dari 7 fold sedangkan G2 lolos 6 dari 7, sehingga akarnya bukan mutu fitur melainkan jumlah informasi positif: F-9_A 30 positif dan F-9 45 positif, dibanding F-14 760 positif. ssi lolos G1 4 dari 5 dan G2 5 dari 5 dengan persistence 0 dari 5, tetapi F-7 hanya 3 positif dan F-9 hanya 12 positif sehingga selang kepercayaan melebar dan F-9_A gagal tipis pada lift 1,47.

**Keterkaitan BoK.** BoK 11 Information Engineering; BoK 5 Quality & Reliability Engineering; BoK 14 Systems Design & Engineering. BoK 11 karena pekerjaan inti adalah akuisisi dan pengelolaan data multi-sumur; BoK 5 karena tujuannya memulihkan kecukupan sampel untuk estimasi keandalan; BoK 14 karena data dari empat sumur harus diintegrasikan ke satu protokol evaluasi.

**Bukti kelayakan dari proyek.**

- Peta kanal menunjukkan sumber positif yang nyata: F-10 mendaftarkan SHKRSK_RT pada 188 berkas, CRPM_RT 186, STKSLP 125, VIBLAT_RT 66, dan STUCK_RT 18; F-4 135/135/135/86; F-12 91/90/52/6; F-15 77/76/76/76. Jejak: `docs/V7_R1_SOLUTIONS.md:43-48`.
- Akuisisi data sudah berjalan dan terukur: CRPM F-10 281.030 baris, F-4 42.010 baris, F-12 178.430 baris, F-15 57.846 baris, dengan re-run 11 fold belum dilakukan. Jejak: `docs/V9_PM1_ARCHITECTURE.md:186`.
- Akar masalah yang diserang terukur pada ssi: G1 4 dari 5, F-9_A lift 1,47 gagal tipis, dan dua fold underpowered (F-7 3 positif, F-9 12 positif). Jejak: `docs/V9_PM1_ARCHITECTURE.md:186`.

**Status pelaksanaan.** Berjalan. Akuisisi dan parsing selesai dengan angka baris terukur. Evaluasi ulang fold belum dijalankan, sehingga dampak terhadap gate belum dapat diklaim.

**Asal usul.** 13 solusi berkode (S-B1, S-A2) dan solusi pendukung V7 6.1 (S-E1). Kode sumber: S-B1, S-A2, S-E1.

#### 3.1.4.3 A3 Penjaminan mutu label dan label probabilistik multi-sumber (Anggota 1)

**Ringkasan.** Membereskan kebenaran label lebih dahulu, lalu menambah sumbu bukti melalui label model bila noise antar sumber masih besar.

**Deskripsi teknis.** Dua tahap berurutan. Tahap pertama adalah audit semantik label: mengunci satu varian onset stuck (strict atau forward-fill), memverifikasi arti skala 0/1/2/3 pada STUCK_RT dan SHKRSK_RT lintas sumur, merekonsiliasi prevalensi stuck 66,9 persen dengan 49,4 persen, menyinkronkan zona waktu kontrol-positif, dan mengganti label hyd proksi dengan kejadian nyata. Tahap kedua adalah label model generatif dengan labeling function independen (status instrumen, event kurasi, penanda fisika differential sticking, anomali overpull), dengan syarat kanal pembentuk label dilarang menjadi fitur. Urutan ini wajib karena kalibrasi ambang apa pun yang dilakukan sebelum label benar hanya menghasilkan presisi palsu.

**Permasalahan yang diselesaikan.** P7. Kontrol-positif stuck 0 dari 10, label hyd masih berupa proksi residual, dan campuran severitas berbeda antar sumur. Cacat ini mengancam seluruh lapisan onset sebelum model apa pun dipercaya.

**Keterkaitan BoK.** BoK 5 Quality & Reliability Engineering; BoK 11 Information Engineering; BoK 14 Systems Design & Engineering. BoK 5 karena inti pekerjaan adalah analisis kegagalan dan mutu pengukuran; BoK 11 karena label adalah keluaran sistem informasi; BoK 14 karena keputusan label harus konsisten dengan tujuan sistem, bukan dengan satu sumur.

**Bukti kelayakan dari proyek.**

- Tiga cacat label sudah terukur: kontrol-positif stuck 0 dari 10, label hyd masih proksi residual, dan campuran severitas berbeda antar sumur. Jejak: `docs/V8_PM_VERDICT.md:202`.
- Basis label kurasi memuat 884 kejadian, 50 di antaranya relevan BHA, dengan total durasi 73.500 menit atau 1.225 jam, sehingga bahan rekonsiliasi tersedia dan dapat dihitung ulang. Jejak: `docs/PPT1_LEDGER_ANGKA.md:145, 193; skrip scratch/ppt1/verify_durations.py`.
- Urutan 6a sebelum 6b ditetapkan karena kalibrasi ambang menyetel kebenaran, sehingga label yang salah akan menghasilkan presisi palsu. Jejak: `docs/V4_MAINTENANCE_ML_OPTIONS.md:163-166`.

**Status pelaksanaan.** Rencana (belum terealisasi). Belum ada langkah audit label yang dieksekusi pada kampanye mana pun.

**Asal usul.** Lever V4 6a dan solusi berkode S-A3. Kode sumber: 6a, S-A3.

#### 3.1.4.4 A4 Unit analisis per-stand pengeboran (Anggota 2)

**Ringkasan.** Mengganti unit jendela 10 menit dengan unit operasional rig (stand) agar prevalensi naik dan varians antar fold turun.

**Deskripsi teknis.** Label per stand didefinisikan sebagai any(kanal minimal 1) selama stand berlangsung, dan fitur berupa statistik stand sebelumnya. Batas stand diturunkan dari BPOS atau celah waktu pada CSV yang sudah ada. Konsekuensi yang harus dinyatakan terbuka: horizon prediksi melebar dari 10 menit menjadi stand berikutnya, sehingga klaim yang boleh dibuat adalah peringatan risiko per stand, bukan peringatan 10 menit.

**Permasalahan yang diselesaikan.** P2, P6. Gate G1 lolos 3 dari 7 fold sedangkan G2 lolos 6 dari 7, sehingga akarnya bukan mutu fitur melainkan jumlah informasi positif: F-9_A 30 positif dan F-9 45 positif, dibanding F-14 760 positif. ssi lolos G1 4 dari 5 dan G2 5 dari 5 dengan persistence 0 dari 5, tetapi F-7 hanya 3 positif dan F-9 hanya 12 positif sehingga selang kepercayaan melebar dan F-9_A gagal tipis pada lift 1,47.

**Keterkaitan BoK.** BoK 7 Operations Engineering & Management; BoK 5 Quality & Reliability Engineering; BoK 11 Information Engineering. BoK 7 karena unit yang dipakai adalah unit operasi produksi pengeboran; BoK 5 karena tujuannya menstabilkan estimasi keandalan; BoK 11 karena agregasi dan penyimpanan fitur berubah.

**Bukti kelayakan dari proyek.**

- Rentang prevalensi 10 sampai 40 persen pada unit stand adalah perkiraan desain dan belum dihitung, sehingga berstatus asumsi. Jejak: `docs/V7_R1_SOLUTIONS.md:111 (ditandai sebagai angka yang dihitung saat eksekusi)`.
- Batas stand dapat diturunkan dari BPOS dan celah waktu pada data yang sudah tersedia, sehingga tidak memerlukan akuisisi baru. Jejak: `docs/V7_R1_SOLUTIONS.md:112`.
- Bila unit stand dipakai, false alarm rate wajib dihitung per stand disertai justifikasinya, karena gate saat ini dihitung per jendela waktu. Jejak: `docs/V9_PM1_ARCHITECTURE.md:470`.

**Status pelaksanaan.** Rencana (belum terealisasi). Belum dijalankan; belum ada artefak hasil untuk unit stand.

**Asal usul.** 13 solusi berkode. Kode sumber: S-B2.

#### 3.1.4.5 A5 Prediksi severity ordinal dengan evaluasi stabilitas fold (Anggota 2)

**Ringkasan.** Memakai seluruh informasi skala 0 sampai 3, lalu menurunkan keputusan biner pada ambang fisik yang sama sambil melaporkan stabilitas tiap fold secara eksplisit.

**Deskripsi teknis.** Model dilatih memprediksi skala (ordinal atau regresi) kemudian keputusan biner diturunkan pada ambang minimal 1, sehingga gate tetap dihitung pada AUPRC biner dan tidak bergeser. Lapisan kedua adalah evaluasi: stratified bootstrap per fold dan pelaporan jumlah positif per fold, agar selang kepercayaan yang lebar tidak menyembunyikan fold underpowered.

**Permasalahan yang diselesaikan.** P6, P7. ssi lolos G1 4 dari 5 dan G2 5 dari 5 dengan persistence 0 dari 5, tetapi F-7 hanya 3 positif dan F-9 hanya 12 positif sehingga selang kepercayaan melebar dan F-9_A gagal tipis pada lift 1,47. Kontrol-positif stuck 0 dari 10, label hyd masih berupa proksi residual, dan campuran severitas berbeda antar sumur. Cacat ini mengancam seluruh lapisan onset sebelum model apa pun dipercaya.

**Keterkaitan BoK.** BoK 5 Quality & Reliability Engineering; BoK 2 Operations Research & Analysis; BoK 11 Information Engineering. BoK 5 karena pengujian hipotesis dan regresi adalah alat utamanya; BoK 2 karena keputusan ambang adalah analisis keputusan; BoK 11 karena keluaran skor harus dikelola sebagai informasi operasional.

**Bukti kelayakan dari proyek.**

- Klasifikasi severitas stick-slip dengan pembelajaran mesin sudah mapan pada literatur sehingga jalur ordinal bukan klaim baru. Jejak: `docs/V7_R1_SOLUTIONS.md:197 (sitasi Hegde 2019, doi 10.1016/j.petrol.2019.05.021)`.
- ssi sudah lolos G1 4 dari 5 dengan dua fold underpowered (F-7 3 positif, F-9 12 positif), sehingga stabilitas fold adalah variabel yang wajib dilaporkan. Jejak: `docs/V9_PM1_ARCHITECTURE.md:186`.
- Penulis solusi sendiri menilai jalur stabilitas fold sebagai pengeras bukti, bukan penambah kelas, sehingga posisinya pelengkap A4 dan A2. Jejak: `docs/V7_R1_SOLUTIONS.md:199`.

**Status pelaksanaan.** Rencana (belum terealisasi). Belum dijalankan; tidak ada angka ordinal maupun bootstrap pada kampanye yang sudah ada.

**Asal usul.** 13 solusi berkode (S-B3) dan solusi pendukung V7 6.1 (S-E2). Kode sumber: S-B3, S-E2.

#### 3.1.4.6 A6 Formulasi survival dan sisa umur pakai (time-to-event) (Anggota 2)

**Ringkasan.** Memodelkan waktu sampai peristiwa, bukan status sesaat, sehingga keluaran berupa risiko per horizon dan sisa umur pakai peralatan.

**Deskripsi teknis.** Model hazard proporsional h(t|x) = h0(t) exp(beta transpose x) dipakai untuk waktu sampai peristiwa hidrolik dan untuk waktu sampai penarikan bit. Skor risiko per horizon H dievaluasi dengan gate biner yang sama, sehingga formulasi berubah tanpa mengubah gerbang. Label waktu sampai penarikan bit diturunkan dari interval dTimStart dan dTimStop pada berkas bhaRun.

**Permasalahan yang diselesaikan.** P9, P3. Seluruh 77 berkas bhaRun tidak memuat dullingInfo, dullGrade, maupun bitName, sehingga label yang tersedia hanya batas waktu run, bukan tingkat keausan. Prediksi onset keausan bit (K-2) belum dijalankan sama sekali. Label diturunkan dari residual SPPA dengan ambang nilai mutlak z di atas 2 sehingga mewarisi persistensi proses. Persistence 0,42 sampai 0,63 mengalahkan Random Forest 0,11 sampai 0,61 pada 7 dari 7 fold, dan G1 hanya lolos 2 dari 7.

**Keterkaitan BoK.** BoK 5 Quality & Reliability Engineering; BoK 3 Engineering Economic Analysis; BoK 2 Operations Research & Analysis. BoK 5 karena survival dan sisa umur pakai adalah inti rekayasa keandalan; BoK 3 karena keputusan penarikan bit adalah trade-off biaya; BoK 2 karena penaksiran hazard adalah model matematis untuk pengambilan keputusan.

**Bukti kelayakan dari proyek.**

- Label waktu sampai penarikan tersedia dari 77 berkas bhaRun, tetapi berkas itu tidak memuat dullingInfo, dullGrade, maupun bitName, sehingga label hanya berupa batas run dan bukan keausan fisik. Jejak: `docs/V4_MAINTENANCE_ML_OPTIONS.md:62`.
- Penulis solusi menilai survival sebagai opsi pembanding karena mengubah formulasi tanpa menambah informasi, sehingga posisinya bukan solusi primer. Jejak: `docs/V7_R1_SOLUTIONS.md:152`.
- Titik operasi hidrolik saat ini menghasilkan nol dari tiga onset terdeteksi, sehingga pembanding berformulasi waktu adalah langkah yang masuk akal dan bukan pengulangan. Jejak: `docs/V9_EVAL_B_LAYERB.md:103`.

**Status pelaksanaan.** Rencana (belum terealisasi). Belum dijalankan; belum ada model hazard pada kampanye mana pun.

**Asal usul.** Solusi berkode S-C3 dan opsi V4 nomor 3 (sisa umur pakai bit). Kode sumber: S-C3, V4-Opsi3.

#### 3.1.4.7 A7 Penguatan kampanye keausan alat bengkel: progresi, dekomposisi mode, dan ranking (Anggota 3)

**Ringkasan.** Tiga mekanisme pada dataset yang sama: label progresi dalam-run, fitur hasil dekomposisi, dan ranking antar status sebagai cadangan.

**Deskripsi teknis.** Bekerja pada 8 berkas akselerometer 1000 Hz (4 alat, 2 run, 469 jendela). Mekanisme pertama adalah label progresi: deret fitur keausan dihitung, titik ubah dideteksi per run, dan jendela sebelum titik ubah menjadi positif. Mekanisme kedua adalah fitur Variational Mode Decomposition berupa energi pita dan statistik per mode. Mekanisme ketiga adalah learning-to-rank pasangan dalam alat, dipakai hanya bila validasi titik ubah gagal karena artefak termal.

**Permasalahan yang diselesaikan.** P4. Hanya 4 alat dan 2 run per alat (469 jendela), label berupa identitas run R01/R02 sehingga urutan percobaan ikut terkorelasi dengan label. Prevalensi sekitar 0,5 membatasi plafon lift pada 2,0; hasil nyata G1 0 dari 4 dengan lift 1,09 sampai 1,42.

**Keterkaitan BoK.** BoK 12 Design & Manufacturing Engineering; BoK 5 Quality & Reliability Engineering; BoK 14 Systems Design & Engineering. BoK 12 karena objek yang dipantau adalah keausan pahat pada proses manufaktur; BoK 5 karena keluarannya metrik keandalan; BoK 14 karena tiga mekanisme harus diintegrasikan ke satu protokol evaluasi.

**Bukti kelayakan dari proyek.**

- Deteksi perubahan regime sudah dijalankan pada 4 dari 4 alat dengan TLead 20 sampai 36 detik (1,8 kali) dan false alarm terkalibrasi 1 sampai 3 per alat, tetapi presisi run hanya 0,50 karena titik ubah juga signifikan pada alat baru. Jejak: `docs/V9_EVAL_C_LAYERC.md:98`.
- Uji artefak termal gagal membuktikan confound pada 0 dari 8 run, sehingga kritik urutan run tidak terbukti pada data ini. Jejak: `docs/V9_EVAL_C_LAYERC.md:98`.
- Baseline ranking lintas alat stabil pada 1,19 kali (AUPRC 0,516 sampai 0,612) sedangkan engine Random Forest belum dijalankan di V9, sehingga mekanisme ranking masih terbuka. Jejak: `docs/V9_EVAL_C_LAYERC.md:99`.
- Fitur dekomposisi mode baru dinyatakan sebagai pengangkat AUPRC pada rancangan, tanpa artefak eksekusi, sehingga statusnya masih rencana. Jejak: `docs/V9_PM1_ARCHITECTURE.md:276`.

**Status pelaksanaan.** Berjalan. Mekanisme progresi dan kalibrasi ambang selesai pada domain bengkel. Dekomposisi mode dan ranking belum dieksekusi.

**Asal usul.** 13 solusi berkode. Kode sumber: S-D1, S-D2, S-D4.

#### 3.1.4.8 A8 Label fisika pengganti label proksi (Anggota 3)

**Ringkasan.** Mengganti label berbasis ambang dengan label berbasis mekanisme: well-control untuk hidrolik dan kombinasi energi spesifik untuk keausan bit.

**Deskripsi teknis.** Untuk hidrolik, dua label turunan fisik dipakai sebagai onset: perubahan volume pit (PITTOT dan GAINLOSSTOT) sebagai penanda kick atau loss, serta selisih laju masuk dan keluar (FLOWOUT dikurangi FLOWIN) sebagai penanda washout, masing-masing dengan ambang z-score median dan MAD per sumur. Untuk keausan bit, status high-MSE hanya dihitung sebagai keausan bila disertai penurunan rasio MSE terhadap energi spesifik, mengikuti aturan Menand dan Mills. Kanal pembentuk label dilarang menjadi fitur.

**Permasalahan yang diselesaikan.** P3, P5, P9. Label diturunkan dari residual SPPA dengan ambang nilai mutlak z di atas 2 sehingga mewarisi persistensi proses. Persistence 0,42 sampai 0,63 mengalahkan Random Forest 0,11 sampai 0,61 pada 7 dari 7 fold, dan G1 hanya lolos 2 dari 7. Gate G1 lolos 3 dari 4 dan G2 lolos 4 dari 4, tetapi persistence lebih tinggi daripada Random Forest pada 4 dari 4 fold karena label high-MSE membentuk blok lintas kedalaman. Aturan pra-registrasi menurunkan verdict menjadi layak bersyarat. Seluruh 77 berkas bhaRun tidak memuat dullingInfo, dullGrade, maupun bitName, sehingga label yang tersedia hanya batas waktu run, bukan tingkat keausan. Prediksi onset keausan bit (K-2) belum dijalankan sama sekali.

**Keterkaitan BoK.** BoK 10 Safety; BoK 5 Quality & Reliability Engineering; BoK 11 Information Engineering. BoK 10 karena kick dan lost circulation adalah bahaya well-control; BoK 5 karena label baru harus diverifikasi terhadap keandalan alat; BoK 11 karena penurunan label adalah pekerjaan rekayasa informasi.

**Bukti kelayakan dari proyek.**

- Kanal sumber label tersedia dan terhitung: GAINLOSSTOT pada 575 berkas di F-1 C dan 517 di F-11, PITTOT 565 dan 506, FLOWOUT 688, FLOWOUTPC 949. Jejak: `docs/V7_R1_SOLUTIONS.md:37-38`.
- Bahan label silang tersedia langsung: USROP_labeled.csv memuat 198.928 baris dengan kolom WOB, ROP, RPM, dan MSE. Jejak: `docs/V7_R1_SOLUTIONS.md:182`.
- Aturan MSE dan MSE/DS sudah diverifikasi rumusnya pada dokumen sumber, sehingga label silang bukan gagasan tanpa dasar. Jejak: `docs/V7_R1_SOLUTIONS.md:181 (sitasi Menand dan Mills, AADE-17-NTCE-033)`.

**Status pelaksanaan.** Rencana (belum terealisasi). Belum ada label pit atau flow yang diparse menjadi deret label; kanal mentahnya sudah teridentifikasi di F-9, F-1 C, dan F-11.

**Asal usul.** Solusi berkode S-C2, S-D3, dan solusi pendukung V7 6.2 (S-F2). Kode sumber: S-C2, S-D3, S-F2.

#### 3.1.4.9 A9 Lapisan keputusan operasional: kalibrasi ambang per sumur dan purwarupa peringatan dini (Anggota 3)

**Ringkasan.** Menyentuh titik operasi alat, bukan model: ambang per sumur, purwarupa kampanye pada data berlabel, dan indeks kondisi untuk disfungsi yang labelnya belum tersedia.

**Deskripsi teknis.** Tiga komponen yang semuanya bersifat operasional. Pertama, kalibrasi ambang per sumur secara prospektif untuk hyd K-i, vib Random Forest, dan shk Random Forest, lalu pengukuran false alarm rate setelah kalibrasi dan pembandingan terhadap baseline persistence. Kedua, purwarupa kampanye stuck-pipe pada dataset TSPP yang sudah berlabel dengan kanal permukaan frekuensi tinggi sebagai uji kelayakan cepat sebelum kampanye lintas sumur. Ketiga, indeks kondisi drill-string berbasis autoencoder untuk disfungsi yang labelnya tidak tersedia langsung, dengan validasi berupa korelasi terhadap event bit run atau stuck, bukan klaim presisi tinggi. Ketiganya tidak menyentuh gate G1 dan G2 yang sudah dikunci.

**Permasalahan yang diselesaikan.** P8, P1. Pada titik operasi yang sama, false alarm rate vib menyebar 4,15 sampai 496,09 per 24 jam, yaitu rasio 119,6 kali antar sumur, sehingga satu ambang global tidak dapat dipakai. Label STUCK_RT bertahan sebagai blok panjang sehingga jendela sebelumnya menjadi prediktor hampir sempurna. Prevalensi F-9_A 66,9%, persistence 0,787 mengalahkan Random Forest 0,651, dan lift F-9_A turun ke 0,97.

**Keterkaitan BoK.** BoK 1 Work Design & Measurement; BoK 6 Ergonomics & Human Factors; BoK 3 Engineering Economic Analysis. BoK 1 karena ambang dan prosedur alarm adalah bagian dari desain sistem kerja driller; BoK 6 karena beban kognitif dan tampilan alert adalah faktor manusia; BoK 3 karena keputusan biaya false alarm dan penghematan rig time adalah analisis ekonomi teknik, sekaligus menutup rantai BoK sesuai pedoman.

**Bukti kelayakan dari proyek.**

- Ambang global terbukti gagal: pada titik operasi 0,5 false alarm rate vib menyebar 4,15 sampai 496,09 per 24 jam atau rasio 119,6 kali antar sumur. Jejak: `docs/V9_PM2_VERDICT.md:114`.
- Dataset TSPP tersedia dengan 52.905 baris pada empat berkas dan 10 kanal permukaan, sehingga purwarupa dapat dijalankan tanpa akuisisi baru. Jejak: `docs/V10_D1_BAB_DATA.md:86, 296`.
- Artefak autoencoder lama tidak diskriminatif karena 75 sampai 99 persen baris berada di atas ambang, sehingga komponen indeks kondisi harus dikerjakan ulang dan tidak boleh mengutip artefak itu sebagai bukti. Jejak: `docs/V4_MAINTENANCE_ML_OPTIONS.md:58`.
- Alat saat ini berjalan dengan nol slot alarm otomatis dari 27 head, sehingga lapisan ini adalah syarat naik tier dan bukan tambahan opsional. Jejak: `scratch/v9_i1/v9_i1_RESULTS.json (kunci auto_critical_alarm_slots = 0; total head 4+4+4+6+4+2+3 = 27)`.

**Status pelaksanaan.** Rencana (belum terealisasi). Kalibrasi ambang per sumur untuk hyd, vib, dan shk belum dijalankan. Kalibrasi false alarm yang sudah ada hanya di dalam engine tool_wear pada domain bengkel.

**Asal usul.** Lever V4 6b dan opsi V4 nomor 1 dan 2. Kode sumber: 6b, V4-Opsi1, V4-Opsi2.

### 3.1.5 Peta sumber ke alternatif

| Sumber | Berkas asal | Alternatif |
|---|---|---|
| S-A1 | `docs/V7_R1_SOLUTIONS.md:72` | A1 |
| S-A2 | `docs/V7_R1_SOLUTIONS.md:79` | A2 |
| S-A3 | `docs/V7_R1_SOLUTIONS.md:85` | A3 |
| S-B1 | `docs/V7_R1_SOLUTIONS.md:103` | A2 |
| S-B2 | `docs/V7_R1_SOLUTIONS.md:109` | A4 |
| S-B3 | `docs/V7_R1_SOLUTIONS.md:115` | A5 |
| S-C1 | `docs/V7_R1_SOLUTIONS.md:133` | A1 |
| S-C2 | `docs/V7_R1_SOLUTIONS.md:139` | A8 |
| S-C3 | `docs/V7_R1_SOLUTIONS.md:148` | A6 |
| S-D1 | `docs/V7_R1_SOLUTIONS.md:167` | A7 |
| S-D2 | `docs/V7_R1_SOLUTIONS.md:173` | A7 |
| S-D3 | `docs/V7_R1_SOLUTIONS.md:179` | A8 |
| S-D4 | `docs/V7_R1_SOLUTIONS.md:185` | A7 |
| S-E1 | `docs/V7_R1_SOLUTIONS.md:198` | A2 |
| S-E2 | `docs/V7_R1_SOLUTIONS.md:199` | A5 |
| S-F1 | `docs/V7_R1_SOLUTIONS.md:204` | A1 |
| S-F2 | `docs/V7_R1_SOLUTIONS.md:205` | A8 |
| V4-Opsi1 | `docs/V4_MAINTENANCE_ML_OPTIONS.md:88` | A9 |
| V4-Opsi2 | `docs/V4_MAINTENANCE_ML_OPTIONS.md:96` | A9 |
| V4-Opsi3 | `docs/V4_MAINTENANCE_ML_OPTIONS.md:103` | A6 |
| 6a | `docs/V4_MAINTENANCE_ML_OPTIONS.md:145` | A3 |
| 6b | `docs/V4_MAINTENANCE_ML_OPTIONS.md:157` | A9 |

### 3.1.6 Rekapitulasi status pelaksanaan

| Status | Alternatif | Keterangan |
|---|---|---|
| Selesai | tidak ada | Tidak ada alternatif yang seluruh mekanismenya selesai. |
| Berjalan | A1, A2, A7 | Mekanisme inti sudah dieksekusi dan berangka; bagian lain belum. |
| Rencana (belum terealisasi) | A3, A4, A5, A6, A8, A9 | Belum ada artefak eksekusi. |

### 3.1.7 Keterkaitan dengan BoK dan kepatuhan pedoman

| Alternatif | BoK 1 | BoK 2 | BoK 3 | BoK 5 | BoK 6 | BoK 7 | BoK 10 | BoK 11 | BoK 12 | BoK 14 |
|---|---|---|---|---|---|---|---|---|---|---|
| A1 | - | - | - | ya | - | - | - | ya | - | ya |
| A2 | - | - | - | ya | - | - | - | ya | - | ya |
| A3 | - | - | - | ya | - | - | - | ya | - | ya |
| A4 | - | - | - | ya | - | ya | - | ya | - | - |
| A5 | - | ya | - | ya | - | - | - | ya | - | - |
| A6 | - | ya | ya | ya | - | - | - | - | - | - |
| A7 | - | - | - | ya | - | - | - | - | ya | ya |
| A8 | - | - | - | ya | - | - | ya | ya | - | - |
| A9 | ya | - | ya | - | ya | - | - | - | - | - |

Pedoman menetapkan bahwa pelaksanaan proyek diawali BoK 14 Sistem Design dan Engineering, melibatkan minimal tiga IEBoK, lalu diakhiri BoK 3 Engineering Economic Analysis. Rancangan sembilan alternatif mengikuti pola tersebut: A1 memuat BoK 14 dan A9 memuat BoK 3, sedangkan setiap alternatif memuat tepat tiga BoK sehingga syarat minimal tiga BoK terpenuhi pada tingkat alternatif, bukan hanya pada tingkat proyek.

Sepuluh dari empat belas BoK tersentuh oleh rancangan ini. Empat BoK yang belum tersentuh adalah BoK 4 Facilities Engineering and Energy Management, BoK 8 Supply Chain Management, BoK 9 Engineering Management, dan BoK 13 Product Design and Development. Keempatnya dicatat terbuka agar subbab 3.2 dapat menilai apakah pengaitan tambahan diperlukan atau justru dipaksakan.

### 3.1.8 Hasil negatif dan batas yang harus dinyatakan

1. Formulasi onset untuk hyd sudah diuji dan gagal pada titik operasi saat ini: nol dari tiga onset terdeteksi dengan TLead nol (`docs/V9_EVAL_B_LAYERB.md:103`). Alternatif A1 karena itu tidak boleh diklaim berhasil untuk semua kelas.
2. Dua angka pada subbab ini berstatus asumsi atau perkiraan desain, yaitu rentang prevalensi unit stand 10 sampai 40 persen (`docs/V7_R1_SOLUTIONS.md:111`) dan hasil kalibrasi ambang per sumur yang belum diukur setelah kalibrasi. Satu angka lain berstatus turunan aritmetik, yaitu plafon lift 2,0 yang berasal dari satu dibagi prevalensi sekitar 0,5 (`docs/V7_R1_SOLUTIONS.md:164`). Tidak ada di antaranya yang merupakan hasil ukur.
3. Dampak perluasan wellbore pada gate belum dapat diklaim karena re-run fold belum dijalankan, meskipun baris data hasil parse sudah terukur (`docs/V9_PM1_ARCHITECTURE.md:186`).
4. Fitur dekomposisi mode pada A7 baru berupa rencana pada rancangan, tanpa artefak eksekusi (`docs/V9_PM1_ARCHITECTURE.md:276`).

### 3.1.9 Manifes jejak angka (internal, bukan untuk sirkulasi eksternal)

| Angka | Nilai | Berkas dan baris |
|---|---|---|
| Prevalensi stuck F-9_A | 66,9 persen | `docs/V7_R1_SOLUTIONS.md:66` |
| Persistence mengalahkan RF pada stuck | 0,787 berbanding 0,651 | `docs/V7_R1_SOLUTIONS.md:66` |
| Positif shk per fold | 760 / 259 / 240 / 267 / 41 / 45 / 30 | `docs/V7_R1_SOLUTIONS.md:97` |
| Gate shk | G1 3 dari 7, G2 6 dari 7 | `docs/V7_R1_SOLUTIONS.md:97` |
| Persistence hyd mengalahkan RF | 7 dari 7 fold | `docs/V7_R1_SOLUTIONS.md:127` |
| Gate hyd | G1 2 dari 7, G2 4 dari 7 | `docs/V7_R1_SOLUTIONS.md:127` |
| Gate tool_wear | G1 0 dari 4, G2 4 dari 4 | `docs/V7_R1_SOLUTIONS.md:160` |
| Gate bit_wear | G1 3 dari 4, G2 4 dari 4 | `docs/V7_R1_SOLUTIONS.md:203` |
| Gate ssi | G1 4 dari 5, G2 5 dari 5 | `docs/V7_R1_SOLUTIONS.md:197` |
| Kanal CRPM hasil parse | 281.030 / 42.010 / 178.430 / 57.846 baris | `docs/V9_PM1_ARCHITECTURE.md:186` |
| Syarat kanal per wellbore | 188 / 186 / 125 / 66 / 18 dan seterusnya | `docs/V7_R1_SOLUTIONS.md:43-48` |
| Stuck K-ii B1 dan TLead | B1 0,51 sampai 1,00; TLead 10 sampai 11,5 menit | `docs/V9_EVAL_B_LAYERB.md:101` |
| Persistence-EVENT stuck | TLead median 7,0 menit; B1 0 sampai 11,5 persen | `docs/V9_EVAL_B_LAYERB.md:101` |
| Hyd K-ii | 0 dari 3 onset; TLead nol | `docs/V9_EVAL_B_LAYERB.md:103` |
| tool_wear K-i | 4 dari 4 alat; TLead 20 sampai 36 detik; FP 1 sampai 3 | `docs/V9_EVAL_C_LAYERC.md:98` |
| tool_wear K-ii canary | AUPRC 0,516 sampai 0,612 (1,19 kali) | `docs/V9_EVAL_C_LAYERC.md:99` |
| Sebaran FAR vib | 4,15 sampai 496,09 per 24 jam, rasio 119,6 kali | `docs/V9_PM2_VERDICT.md:114` |
| Kontrol-positif stuck | 0 dari 10 | `docs/V8_PM_VERDICT.md:202` |
| Basis label kurasi | 884 kejadian, 50 relevan BHA, 1.225 jam | `docs/PPT1_LEDGER_ANGKA.md:145, 193` |
| Berkas bhaRun | 77 berkas, tanpa dullingInfo | `docs/V4_MAINTENANCE_ML_OPTIONS.md:62` |
| TSPP | 52.905 baris, 4 berkas, 10 kanal | `docs/V10_D1_BAB_DATA.md:86, 296` |
| Slot alarm otomatis | 0 dari 27 head | `scratch/v9_i1/v9_i1_RESULTS.json` |

Reproduksi: `python3 scratch/ppt1/build_alternatif.py` menulis ulang `scratch/ppt1/alternatif.json` dan dokumen ini, lalu menjalankan pemeriksaan acceptance.

---

Catatan penyusunan: subbab 3.2 Analisis Alternatif Solusi, 3.3 Kriteria dan Batasan, serta 3.4 Pemilihan Alternatif Solusi belum termasuk dalam dokumen ini.
