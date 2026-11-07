# BAB III ANALISIS ALTERNATIF SOLUSI

## 3.1 Permasalahan & Alternatif Solusi

- Acuan format: Buku Pedoman PPT Tahap I, subbab 3.2 Format Proposal, halaman 33 sampai 36
- Acuan BoK: Buku Pedoman PPT Tahap I Tabel 2.1, empat belas IEBoK, selaras IISE ISEBoK 2021


### 3.1.1 Dasar penyusunan dan aturan bukti

Riset pendahuluan: `grounded-citations` - setiap angka pada subbab ini melekat pada sumber yang sudah diekstrak, dan blok bukti memuat kunci jejak berupa berkas dan nomor baris, bukan ingatan.

Riset pendahuluan: `formal-project-documents` - register formal baku tanpa penanda status dalam tanda kurung, tanpa emoji, dan setiap konsep teknis dituliskan sebagai definisi, tujuan, alasan pemilihan, serta batasnya.

Riset pendahuluan: `sequentialthinking` (sequ-mcp, empat pikiran) - inventaris dua puluh dua sumber, uji tiga skema pembagian anggota, verifikasi status eksekusi per solusi, lalu penetapan pembagian berbasis lapisan intervensi (data dan label, formulasi model, sinyal fisik dan operasi).

Sembilan alternatif pada subbab ini disusun dari inventaris solusi yang sudah berkode di dalam proyek, yaitu tiga belas solusi S-A1 sampai S-D4 beserta empat solusi pendukung pada bagian kelas rapuh (S-E1, S-E2, S-F1, S-F2), tiga opsi peningkatan pada dokumen opsi ML, dan dua lever pasca-V9 (6a perbaikan label, 6b kalibrasi ambang per sumur). Seluruh dua puluh dua sumber dipetakan tepat satu kali ke sembilan alternatif, sehingga tidak ada alternatif yang menduplikasi mekanisme alternatif lain, dan tidak ada sumber yang hilang tanpa rumah.

Angka pada seluruh subbab dihitung ulang dari data primer atau berkas hasil eksekusi; angka yang belum terukur disertai isi asumsinya, dasar, alasan dipilih, dan cara mengujinya, dan tidak disamarkan menjadi hasil pengukuran.


### 3.1.2 Kondisi pengikat dan celah teknis yang dirujuk

Tabel berikut memuat sembilan kode rujukan P1 sampai P9. Kode ini bukan rumusan masalah. Rumusan masalah hanya tiga, yaitu RM1, RM2, dan RM3 pada 1.1.6. Sebagian besar kode di bawah adalah keadaan yang mengikat ruang lingkup, misalnya jumlah alat, jumlah positif per fold, dan ketiadaan atribut pada berkas sumber, sehingga tidak dijawab sebagai temuan melainkan diakomodasi sebagai batasan. Sisanya adalah celah teknis yang menjadi prasyarat bagi RM1 atau RM2.

| Kode | Kondisi pengikat atau celah teknis | Uraian ringkas dan angka | Jejak |
| --- | --- | --- | --- |
| P1 | Label stuck berbentuk status, bukan peristiwa | Label STUCK_RT bertahan sebagai blok panjang sehingga jendela sebelumnya menjadi prediktor hampir sempurna. Prevalensi F-9_A 66,9%, persistence 0,787 mengalahkan Random Forest 0,651, dan lift F-9_A turun ke 0,97. |  |
| P2 | Jumlah positif shk terlalu sedikit per fold | Gate G1 lolos 3 dari 7 fold sedangkan G2 lolos 6 dari 7, sehingga akarnya bukan mutu fitur melainkan jumlah informasi positif: F-9_A 30 positif dan F-9 45 positif, dibanding F-14 760 positif. |  |
| P3 | Label hyd adalah ambang residual dari proses yang persisten | Label diturunkan dari residual SPPA dengan ambang nilai mutlak z di atas 2 sehingga mewarisi persistensi proses. Persistence 0,42 sampai 0,63 mengalahkan Random Forest 0,11 sampai 0,61 pada 7 dari 7 fold, dan G1 hanya lolos 2 dari 7. |  |
| P4 | tool_wear terbatas 4 alat dengan label identitas run | Hanya 4 alat dan 2 run per alat (469 jendela), label berupa identitas run R01/R02 sehingga urutan percobaan ikut terkorelasi dengan label. Prevalensi sekitar 0,5 membatasi plafon lift pada 2,0; hasil nyata G1 0 dari 4 dengan lift 1,09 sampai 1,42. |  |
| P5 | bit_wear dikalahkan persistence pada seluruh fold | Gate G1 lolos 3 dari 4 dan G2 lolos 4 dari 4, tetapi persistence lebih tinggi daripada Random Forest pada 4 dari 4 fold karena label high-MSE membentuk blok lintas kedalaman. Aturan pra-registrasi menurunkan verdict menjadi layak bersyarat. |  |
| P6 | Sebagian fold ssi underpowered | ssi lolos G1 4 dari 5 dan G2 5 dari 5 dengan persistence 0 dari 5, tetapi F-7 hanya 3 positif dan F-9 hanya 12 positif sehingga selang kepercayaan melebar dan F-9_A gagal tipis pada lift 1,47. |  |
| P7 | Validitas label lintas sumur belum terbukti | Kontrol-positif stuck 0 dari 10, label hyd masih berupa proksi residual, dan campuran severitas berbeda antar sumur. Cacat ini mengancam seluruh lapisan onset sebelum model apa pun dipercaya. |  |
| P8 | Ambang global tidak portabel antar sumur | Pada titik operasi yang sama, false alarm rate vib menyebar 4,15 sampai 496,09 per 24 jam, yaitu rasio 119,6 kali antar sumur, sehingga satu ambang global tidak dapat dipakai. |  |
| P9 | Tidak ada label keausan fisik dari rig | Seluruh 77 berkas bhaRun tidak memuat dullingInfo, dullGrade, maupun bitName, sehingga label yang tersedia hanya batas waktu run, bukan tingkat keausan. Prediksi onset keausan bit (K-2) belum dijalankan sama sekali. |  |

Peta asal setiap kode, supaya tidak ada yang dibaca sebagai pertanyaan riset baru:

| Kode | Asal di Bab I | Peran |
| --- | --- | --- |
| P1 | RM1, mutu label | kondisi pengikat bentuk label |
| P2 | Kendala 1.4.4 butir 3 | jumlah positif per fold terbatas |
| P3 | RM1, mutu label | kondisi pengikat bentuk label |
| P4 | Kendala 1.4.4 butir 5 | cakupan domain bengkel |
| P5 | RM1 | celah teknis, baseline mengalahkan model |
| P6 | Kendala 1.4.4 butir 3 | jumlah sampel per fold terbatas |
| P7 | Kendala 1.4.4 butir 1 | validitas lintas sumur |
| P8 | RM2 | gejala yang harus dijawab pemilihan titik operasi |
| P9 | Kendala 1.4.4 butir 4 | atribut keausan tidak tersedia |

Konsekuensi pembacaan: P1 sampai P9 tidak menambah jumlah rumusan masalah. Yang bertambah hanya rincian mengapa ketiga pertanyaan riset itu sulit dijawab dengan data yang ada.

### 3.1.3 Tabel rekap sembilan alternatif

| No | Anggota | Alternatif solusi | BoK | Masalah yang dirujuk | Dieksekusi di kampanye |
|---|---|---|---|---|---|
| A1 | Anggota 1 | Relabeling onset peristiwa: dari status menjadi kejadian | 14, 11, 5 | P1, P3, P5 | V9, sebagian (stuck K-ii dan hyd K-ii) |
| A2 | Anggota 1 | Perluasan wellbore berkanal disfungsi (F-10, F-4, F-12, F-15) | 11, 5, 14 | P2, P6 | V9, akuisisi data (baris hasil parse) |
| A3 | Anggota 1 | Penjaminan mutu label dan label probabilistik multi-sumber | 5, 11, 14 | P7 | belum ada |
| A4 | Anggota 2 | Unit analisis per-stand pengeboran | 7, 5, 11 | P2, P6 | belum ada |
| A5 | Anggota 2 | Prediksi severity ordinal dengan evaluasi stabilitas fold | 5, 2, 11 | P6, P7 | belum ada |
| A6 | Anggota 2 | Formulasi survival dan sisa umur pakai (time-to-event) | 5, 3, 2 | P9, P3 | belum ada |
| A7 | Anggota 3 | Penguatan kampanye keausan alat bengkel: progresi, dekomposisi mode, dan ranking | 12, 5, 14 | P4 | V9, domain bengkel (K-i) |
| A8 | Anggota 3 | Label fisika pengganti label proksi | 10, 5, 11 | P3, P5, P9 | belum ada |
| A9 | Anggota 3 | Lapisan keputusan operasional: kalibrasi ambang per sumur dan purwarupa peringatan dini | 1, 6, 3 | P8, P1 | belum ada |

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

- Formulasi onset sudah dijalankan untuk stuck dan menghasilkan peringatan dengan arah benar pada beban rendah: Random Forest pada titik operasi 0,05 memberi B1 0,51 sampai 1,00 dengan TLead 10 sampai 11,5 menit, sedangkan baseline persistence-EVENT hanya memberi TLead median 7,0 menit dengan B1 0 sampai 11,5 persen. Jejak: .
- Untuk hyd, formulasi yang sama menghasilkan B1 nol dari tiga onset dengan TLead nol, jadi hasil negatifnya terukur dan dilaporkan apa adanya. Jejak: .
- Relabel tidak memerlukan parse baru karena deret sumber sudah berbentuk CSV. Jejak: .

**Keadaan pelaksanaan.** Berjalan. Sudah dieksekusi untuk stuck (K-ii) dan hyd (K-ii) pada kampanye V9. Belum dieksekusi untuk bit_wear K-2 karena pra-registrasi kampanye tersebut belum terbit.

#### 3.1.4.2 A2 Perluasan wellbore berkanal disfungsi (F-10, F-4, F-12, F-15) (Anggota 1)

**Ringkasan.** Menambah sumur dan fold dengan memparse wellbore yang terbukti memiliki kanal disfungsi, bukan menurunkan ambang label.

**Deskripsi teknis.** Empat wellbore yang belum diparse (F-10, F-4, F-12, F-15) diproses ke CSV dengan protokol identik kampanye sebelumnya: grid 60 detik, agregasi menit, syarat kelayakan jendela yang sama. Hasilnya digabungkan ke kampanye leave-one-well-out per kelas sehingga jumlah fold dan jumlah positif naik tanpa mengubah definisi label maupun gate. Peta kanal dipakai sebagai syarat masuk: hanya wellbore yang benar-benar mendaftarkan mnemonic disfungsi yang diambil.

**Permasalahan yang diselesaikan.** P2, P6. Gate G1 lolos 3 dari 7 fold sedangkan G2 lolos 6 dari 7, sehingga akarnya bukan mutu fitur melainkan jumlah informasi positif: F-9_A 30 positif dan F-9 45 positif, dibanding F-14 760 positif. ssi lolos G1 4 dari 5 dan G2 5 dari 5 dengan persistence 0 dari 5, tetapi F-7 hanya 3 positif dan F-9 hanya 12 positif sehingga selang kepercayaan melebar dan F-9_A gagal tipis pada lift 1,47.

**Keterkaitan BoK.** BoK 11 Information Engineering; BoK 5 Quality & Reliability Engineering; BoK 14 Systems Design & Engineering. BoK 11 karena pekerjaan inti adalah akuisisi dan pengelolaan data multi-sumur; BoK 5 karena tujuannya memulihkan kecukupan sampel untuk estimasi keandalan; BoK 14 karena data dari empat sumur harus diintegrasikan ke satu protokol evaluasi.

**Bukti kelayakan dari proyek.**

- Peta kanal menunjukkan sumber positif yang nyata: F-10 mendaftarkan SHKRSK_RT pada 188 berkas, CRPM_RT 186, STKSLP 125, VIBLAT_RT 66, dan STUCK_RT 18; F-4 135/135/135/86; F-12 91/90/52/6; F-15 77/76/76/76. Jejak: .
- Akuisisi data sudah berjalan dan terukur: CRPM F-10 281.030 baris, F-4 42.010 baris, F-12 178.430 baris, F-15 57.846 baris, dengan re-run 11 fold belum dilakukan. Jejak: .
- Akar masalah yang diserang terukur pada ssi: G1 4 dari 5, F-9_A lift 1,47 gagal tipis, dan dua fold underpowered (F-7 3 positif, F-9 12 positif). Jejak: .

**Keadaan pelaksanaan.** Berjalan. Akuisisi dan parsing selesai dengan angka baris terukur. Evaluasi ulang fold belum dijalankan, sehingga dampak terhadap gate belum dapat diklaim.

#### 3.1.4.3 A3 Penjaminan mutu label dan label probabilistik multi-sumber (Anggota 1)

**Ringkasan.** Membereskan kebenaran label lebih dahulu, lalu menambah sumbu bukti melalui label model bila noise antar sumber masih besar.

**Deskripsi teknis.** Dua tahap berurutan. Tahap pertama adalah audit semantik label: mengunci satu varian onset stuck (strict atau forward-fill), memverifikasi arti skala 0/1/2/3 pada STUCK_RT dan SHKRSK_RT lintas sumur, merekonsiliasi prevalensi stuck 66,9 persen dengan 49,4 persen, menyinkronkan zona waktu kontrol-positif, dan mengganti label hyd proksi dengan kejadian nyata. Tahap kedua adalah label model generatif dengan labeling function independen (status instrumen, event kurasi, penanda fisika differential sticking, anomali overpull), dengan syarat kanal pembentuk label dilarang menjadi fitur. Urutan ini wajib karena kalibrasi ambang apa pun yang dilakukan sebelum label benar hanya menghasilkan presisi palsu.

**Permasalahan yang diselesaikan.** P7. Kontrol-positif stuck 0 dari 10, label hyd masih berupa proksi residual, dan campuran severitas berbeda antar sumur. Cacat ini mengancam seluruh lapisan onset sebelum model apa pun dipercaya.

**Keterkaitan BoK.** BoK 5 Quality & Reliability Engineering; BoK 11 Information Engineering; BoK 14 Systems Design & Engineering. BoK 5 karena inti pekerjaan adalah analisis kegagalan dan mutu pengukuran; BoK 11 karena label adalah keluaran sistem informasi; BoK 14 karena keputusan label harus konsisten dengan tujuan sistem, bukan dengan satu sumur.

**Bukti kelayakan dari proyek.**

- Tiga cacat label sudah terukur: kontrol-positif stuck 0 dari 10, label hyd masih proksi residual, dan campuran severitas berbeda antar sumur. Jejak: .
- Basis label kurasi memuat 884 kejadian, 50 di antaranya relevan BHA, dengan total durasi 73.500 menit atau 1.225 jam, sehingga bahan rekonsiliasi tersedia dan dapat dihitung ulang. Jejak: .
- Urutan 6a sebelum 6b ditetapkan karena kalibrasi ambang menyetel kebenaran, sehingga label yang salah akan menghasilkan presisi palsu. Jejak: .

**Keadaan pelaksanaan.** Rencana (belum terealisasi). Belum ada langkah audit label yang dieksekusi pada kampanye mana pun.

#### 3.1.4.4 A4 Unit analisis per-stand pengeboran (Anggota 2)

**Ringkasan.** Mengganti unit jendela 10 menit dengan unit operasional rig (stand) agar prevalensi naik dan varians antar fold turun.

**Deskripsi teknis.** Label per stand didefinisikan sebagai any(kanal minimal 1) selama stand berlangsung, dan fitur berupa statistik stand sebelumnya. Batas stand diturunkan dari BPOS atau celah waktu pada CSV yang sudah ada. Konsekuensi yang harus dinyatakan terbuka: horizon prediksi melebar dari 10 menit menjadi stand berikutnya, sehingga klaim yang boleh dibuat adalah peringatan risiko per stand, bukan peringatan 10 menit.

**Permasalahan yang diselesaikan.** P2, P6. Gate G1 lolos 3 dari 7 fold sedangkan G2 lolos 6 dari 7, sehingga akarnya bukan mutu fitur melainkan jumlah informasi positif: F-9_A 30 positif dan F-9 45 positif, dibanding F-14 760 positif. ssi lolos G1 4 dari 5 dan G2 5 dari 5 dengan persistence 0 dari 5, tetapi F-7 hanya 3 positif dan F-9 hanya 12 positif sehingga selang kepercayaan melebar dan F-9_A gagal tipis pada lift 1,47.

**Keterkaitan BoK.** BoK 7 Operations Engineering & Management; BoK 5 Quality & Reliability Engineering; BoK 11 Information Engineering. BoK 7 karena unit yang dipakai adalah unit operasi produksi pengeboran; BoK 5 karena tujuannya menstabilkan estimasi keandalan; BoK 11 karena agregasi dan penyimpanan fitur berubah.

**Bukti kelayakan dari proyek.**

- Rentang prevalensi unit stand 10 sampai 40 persen adalah **asumsi**. **Isi asumsinya:** proporsi unit stand yang menghasilkan kejadian di antara unit yang dikunci. **Dasar:** belum ada hitungan prevalensi untuk unit stand karena belum ada label stand pada data, sementara rancangan standar memerlukan ambang kalibrasi awal. **Alasan dipilih:** rentang dipakai untuk menguji kerentanan desain ambang sebelum biaya pengumpulan label stand dibelanjakan, bukan sebagai angka kinerja. **Cara mengujinya:** saat data stand tersedia, hitung proporsi unit stand dengan kejadian pada interval yang sama dan bandingkan dengan 10 sampai 40 persen.
- Batas stand dapat diturunkan dari BPOS dan celah waktu pada data yang sudah tersedia, sehingga tidak memerlukan akuisisi baru. Jejak: .
- Bila unit stand dipakai, false alarm rate wajib dihitung per stand disertai justifikasinya, karena gate saat ini dihitung per jendela waktu. Jejak: .

**Keadaan pelaksanaan.** Rencana (belum terealisasi). Belum dijalankan; belum ada artefak hasil untuk unit stand.

#### 3.1.4.5 A5 Prediksi severity ordinal dengan evaluasi stabilitas fold (Anggota 2)

**Ringkasan.** Memakai seluruh informasi skala 0 sampai 3, lalu menurunkan keputusan biner pada ambang fisik yang sama sambil melaporkan stabilitas tiap fold secara eksplisit.

**Deskripsi teknis.** Model dilatih memprediksi skala (ordinal atau regresi) kemudian keputusan biner diturunkan pada ambang minimal 1, sehingga gate tetap dihitung pada AUPRC biner dan tidak bergeser. Lapisan kedua adalah evaluasi: stratified bootstrap per fold dan pelaporan jumlah positif per fold, agar selang kepercayaan yang lebar tidak menyembunyikan fold underpowered.

**Permasalahan yang diselesaikan.** P6, P7. ssi lolos G1 4 dari 5 dan G2 5 dari 5 dengan persistence 0 dari 5, tetapi F-7 hanya 3 positif dan F-9 hanya 12 positif sehingga selang kepercayaan melebar dan F-9_A gagal tipis pada lift 1,47. Kontrol-positif stuck 0 dari 10, label hyd masih berupa proksi residual, dan campuran severitas berbeda antar sumur. Cacat ini mengancam seluruh lapisan onset sebelum model apa pun dipercaya.

**Keterkaitan BoK.** BoK 5 Quality & Reliability Engineering; BoK 2 Operations Research & Analysis; BoK 11 Information Engineering. BoK 5 karena pengujian hipotesis dan regresi adalah alat utamanya; BoK 2 karena keputusan ambang adalah analisis keputusan; BoK 11 karena keluaran skor harus dikelola sebagai informasi operasional.

**Bukti kelayakan dari proyek.**

- Klasifikasi severitas stick-slip dengan pembelajaran mesin sudah mapan pada literatur sehingga jalur ordinal bukan klaim baru. Jejak: .
- ssi sudah lolos G1 4 dari 5 dengan dua fold underpowered (F-7 3 positif, F-9 12 positif), sehingga stabilitas fold adalah variabel yang wajib dilaporkan. Jejak: .
- Penulis solusi sendiri menilai jalur stabilitas fold sebagai pengeras bukti, bukan penambah kelas, sehingga posisinya pelengkap A4 dan A2. Jejak: .

**Keadaan pelaksanaan.** Rencana (belum terealisasi). Belum dijalankan; tidak ada angka ordinal maupun bootstrap pada kampanye yang sudah ada.

#### 3.1.4.6 A6 Formulasi survival dan sisa umur pakai (time-to-event) (Anggota 2)

**Ringkasan.** Memodelkan waktu sampai peristiwa, bukan status sesaat, sehingga keluaran berupa risiko per horizon dan sisa umur pakai peralatan.

**Deskripsi teknis.** Model hazard proporsional h(t|x) = h0(t) exp(beta transpose x) dipakai untuk waktu sampai peristiwa hidrolik dan untuk waktu sampai penarikan bit. Skor risiko per horizon H dievaluasi dengan gate biner yang sama, sehingga formulasi berubah tanpa mengubah gerbang. Label waktu sampai penarikan bit diturunkan dari interval dTimStart dan dTimStop pada berkas bhaRun.

**Permasalahan yang diselesaikan.** P9, P3. Seluruh 77 berkas bhaRun tidak memuat dullingInfo, dullGrade, maupun bitName, sehingga label yang tersedia hanya batas waktu run, bukan tingkat keausan. Prediksi onset keausan bit (K-2) belum dijalankan sama sekali. Label diturunkan dari residual SPPA dengan ambang nilai mutlak z di atas 2 sehingga mewarisi persistensi proses. Persistence 0,42 sampai 0,63 mengalahkan Random Forest 0,11 sampai 0,61 pada 7 dari 7 fold, dan G1 hanya lolos 2 dari 7.

**Keterkaitan BoK.** BoK 5 Quality & Reliability Engineering; BoK 3 Engineering Economic Analysis; BoK 2 Operations Research & Analysis. BoK 5 karena survival dan sisa umur pakai adalah inti rekayasa keandalan; BoK 3 karena keputusan penarikan bit adalah trade-off biaya; BoK 2 karena penaksiran hazard adalah model matematis untuk pengambilan keputusan.

**Bukti kelayakan dari proyek.**

- Label waktu sampai penarikan tersedia dari 77 berkas bhaRun, tetapi berkas itu tidak memuat dullingInfo, dullGrade, maupun bitName, sehingga label hanya berupa batas run dan bukan keausan fisik. Jejak: .
- Penulis solusi menilai survival sebagai opsi pembanding karena mengubah formulasi tanpa menambah informasi, sehingga posisinya bukan solusi primer. Jejak: .
- Titik operasi hidrolik saat ini menghasilkan nol dari tiga onset terdeteksi, sehingga pembanding berformulasi waktu adalah langkah yang masuk akal dan bukan pengulangan. Jejak: .

**Keadaan pelaksanaan.** Rencana (belum terealisasi). Belum dijalankan; belum ada model hazard pada kampanye mana pun.

#### 3.1.4.7 A7 Penguatan kampanye keausan alat bengkel: progresi, dekomposisi mode, dan ranking (Anggota 3)

**Ringkasan.** Tiga mekanisme pada dataset yang sama: label progresi dalam-run, fitur hasil dekomposisi, dan ranking antar status sebagai cadangan.

**Deskripsi teknis.** Bekerja pada 8 berkas akselerometer 1000 Hz (4 alat, 2 run, 469 jendela). Mekanisme pertama adalah label progresi: deret fitur keausan dihitung, titik ubah dideteksi per run, dan jendela sebelum titik ubah menjadi positif. Mekanisme kedua adalah fitur Variational Mode Decomposition berupa energi pita dan statistik per mode. Mekanisme ketiga adalah learning-to-rank pasangan dalam alat, dipakai hanya bila validasi titik ubah gagal karena artefak termal.

**Permasalahan yang diselesaikan.** P4. Hanya 4 alat dan 2 run per alat (469 jendela), label berupa identitas run R01/R02 sehingga urutan percobaan ikut terkorelasi dengan label. Prevalensi sekitar 0,5 membatasi plafon lift pada 2,0; hasil nyata G1 0 dari 4 dengan lift 1,09 sampai 1,42.

**Keterkaitan BoK.** BoK 12 Design & Manufacturing Engineering; BoK 5 Quality & Reliability Engineering; BoK 14 Systems Design & Engineering. BoK 12 karena objek yang dipantau adalah keausan pahat pada proses manufaktur; BoK 5 karena keluarannya metrik keandalan; BoK 14 karena tiga mekanisme harus diintegrasikan ke satu protokol evaluasi.

**Bukti kelayakan dari proyek.**

- Deteksi perubahan regime sudah dijalankan pada 4 dari 4 alat dengan TLead 20 sampai 36 detik (1,8 kali) dan false alarm terkalibrasi 1 sampai 3 per alat, tetapi presisi run hanya 0,50 karena titik ubah juga signifikan pada alat baru. Jejak: .
- Uji artefak termal gagal membuktikan confound pada 0 dari 8 run, sehingga kritik urutan run tidak terbukti pada data ini. Jejak: .
- Baseline ranking lintas alat stabil pada 1,19 kali (AUPRC 0,516 sampai 0,612) sedangkan model Random Forest belum dijalankan di V9, sehingga mekanisme ranking masih terbuka. Jejak: .
- Fitur dekomposisi mode baru dinyatakan sebagai pengangkat AUPRC pada rancangan, tanpa artefak eksekusi, sehingga statusnya masih rencana. Jejak: .

**Keadaan pelaksanaan.** Berjalan. Mekanisme progresi dan kalibrasi ambang selesai pada domain bengkel. Dekomposisi mode dan ranking belum dieksekusi.

#### 3.1.4.8 A8 Label fisika pengganti label proksi (Anggota 3)

**Ringkasan.** Mengganti label berbasis ambang dengan label berbasis mekanisme: well-control untuk hidrolik dan kombinasi energi spesifik untuk keausan bit.

**Deskripsi teknis.** Untuk hidrolik, dua label turunan fisik dipakai sebagai onset: perubahan volume pit (PITTOT dan GAINLOSSTOT) sebagai penanda kick atau loss, serta selisih laju masuk dan keluar (FLOWOUT dikurangi FLOWIN) sebagai penanda washout, masing-masing dengan ambang z-score median dan MAD per sumur. Untuk keausan bit, status high-MSE hanya dihitung sebagai keausan bila disertai penurunan rasio MSE terhadap energi spesifik, mengikuti aturan Menand dan Mills. Kanal pembentuk label dilarang menjadi fitur.

**Permasalahan yang diselesaikan.** P3, P5, P9. Label diturunkan dari residual SPPA dengan ambang nilai mutlak z di atas 2 sehingga mewarisi persistensi proses. Persistence 0,42 sampai 0,63 mengalahkan Random Forest 0,11 sampai 0,61 pada 7 dari 7 fold, dan G1 hanya lolos 2 dari 7. Gate G1 lolos 3 dari 4 dan G2 lolos 4 dari 4, tetapi persistence lebih tinggi daripada Random Forest pada 4 dari 4 fold karena label high-MSE membentuk blok lintas kedalaman. Aturan pra-registrasi menurunkan verdict menjadi layak bersyarat. Seluruh 77 berkas bhaRun tidak memuat dullingInfo, dullGrade, maupun bitName, sehingga label yang tersedia hanya batas waktu run, bukan tingkat keausan. Prediksi onset keausan bit (K-2) belum dijalankan sama sekali.

**Keterkaitan BoK.** BoK 10 Safety; BoK 5 Quality & Reliability Engineering; BoK 11 Information Engineering. BoK 10 karena kick dan lost circulation adalah bahaya well-control; BoK 5 karena label baru harus diverifikasi terhadap keandalan alat; BoK 11 karena penurunan label adalah pekerjaan rekayasa informasi.

**Bukti kelayakan dari proyek.**

- Kanal sumber label tersedia dan terhitung: GAINLOSSTOT pada 575 berkas di F-1 C dan 517 di F-11, PITTOT 565 dan 506, FLOWOUT 688, FLOWOUTPC 949. Jejak: .
- Bahan label silang tersedia langsung: USROP_labeled.csv memuat 198.928 baris dengan kolom WOB, ROP, RPM, dan MSE. Jejak: .
- Aturan MSE dan MSE/DS sudah diverifikasi rumusnya pada dokumen sumber, sehingga label silang bukan gagasan tanpa dasar. Jejak: .

**Keadaan pelaksanaan.** Rencana (belum terealisasi). Belum ada label pit atau flow yang diparse menjadi deret label; kanal mentahnya sudah teridentifikasi di F-9, F-1 C, dan F-11.

#### 3.1.4.9 A9 Lapisan keputusan operasional: kalibrasi ambang per sumur dan purwarupa peringatan dini (Anggota 3)

**Ringkasan.** Menyentuh titik operasi alat, bukan model: ambang per sumur, purwarupa kampanye pada data berlabel, dan indeks kondisi untuk disfungsi yang labelnya belum tersedia.

**Deskripsi teknis.** Tiga komponen yang semuanya bersifat operasional. Pertama, kalibrasi ambang per sumur secara prospektif untuk hyd K-i, vib Random Forest, dan shk Random Forest, lalu pengukuran false alarm rate setelah kalibrasi dan pembandingan terhadap baseline persistence. Kedua, purwarupa kampanye stuck-pipe pada dataset TSPP yang sudah berlabel dengan kanal permukaan frekuensi tinggi sebagai uji kelayakan cepat sebelum kampanye lintas sumur. Ketiga, indeks kondisi drill-string berbasis autoencoder untuk disfungsi yang labelnya tidak tersedia langsung, dengan validasi berupa korelasi terhadap event bit run atau stuck, bukan klaim presisi tinggi. Ketiganya tidak menyentuh gate G1 dan G2 yang sudah dikunci.

**Permasalahan yang diselesaikan.** P8, P1. Pada titik operasi yang sama, false alarm rate vib menyebar 4,15 sampai 496,09 per 24 jam, yaitu rasio 119,6 kali antar sumur, sehingga satu ambang global tidak dapat dipakai. Label STUCK_RT bertahan sebagai blok panjang sehingga jendela sebelumnya menjadi prediktor hampir sempurna. Prevalensi F-9_A 66,9%, persistence 0,787 mengalahkan Random Forest 0,651, dan lift F-9_A turun ke 0,97.

**Keterkaitan BoK.** BoK 1 Work Design & Measurement; BoK 6 Ergonomics & Human Factors; BoK 3 Engineering Economic Analysis. BoK 1 karena ambang dan prosedur alarm adalah bagian dari desain sistem kerja driller; BoK 6 karena beban kognitif dan tampilan alert adalah faktor manusia; BoK 3 karena keputusan biaya false alarm dan penghematan rig time adalah analisis ekonomi teknik, sekaligus menutup rantai BoK sesuai pedoman.

**Bukti kelayakan dari proyek.**

- Ambang global terbukti gagal: pada titik operasi 0,5 false alarm rate vib menyebar 4,15 sampai 496,09 per 24 jam atau rasio 119,6 kali antar sumur. Jejak: .
- Dataset TSPP tersedia dengan 52.905 baris pada empat berkas dan 10 kanal permukaan, sehingga purwarupa dapat dijalankan tanpa akuisisi baru. Jejak: .
- Artefak autoencoder lama tidak diskriminatif karena 75 sampai 99 persen baris berada di atas ambang, sehingga komponen indeks kondisi harus dikerjakan ulang dan tidak boleh mengutip artefak itu sebagai bukti. Jejak: .
- Alat saat ini berjalan dengan nol slot alarm otomatis dari 27 head, sehingga lapisan ini adalah syarat naik tier dan bukan tambahan opsional. Jejak: .

**Keadaan pelaksanaan.** Rencana (belum terealisasi). Kalibrasi ambang per sumur untuk hyd, vib, dan shk belum dijalankan. Kalibrasi false alarm yang sudah ada hanya di dalam mode tool_wear pada domain bengkel.

### 3.1.6 Rekapitulasi status pelaksanaan

| Alternatif | Keterangan |
|---|---|
| tidak ada | Tidak ada alternatif yang seluruh mekanismenya selesai. |
| A1, A2, A7 | Mekanisme inti sudah dieksekusi dan berangka; bagian lain belum. |
| A3, A4, A5, A6, A8, A9 | Belum ada artefak eksekusi. |

### 3.1.7 Keterkaitan dengan BoK dan kepatuhan pedoman

| Alternatif | BoK 1 | BoK 2 | BoK 3 | BoK 5 | BoK 6 | BoK 7 | BoK 10 | BoK 11 | BoK 12 | BoK 14 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
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

1. Formulasi onset untuk hyd sudah diuji dan gagal pada titik operasi saat ini: nol dari tiga onset terdeteksi dengan TLead nol (). Alternatif A1 karena itu tidak boleh diklaim berhasil untuk semua kelas.
2. Dua hal pada subbab ini masih asumsi: rentang prevalensi unit stand 10 sampai 40 persen (dijelaskan dengan isi, dasar, alasan, dan uji pada butir di atas) dan hasil kalibrasi ambang per sumur yang belum ada karena belum ada label stand.
3. Dampak perluasan wellbore pada gate belum dapat diklaim karena re-run fold belum dijalankan, meskipun baris data hasil parse sudah terukur ().
4. Fitur dekomposisi mode pada A7 baru berupa rencana pada rancangan, tanpa artefak eksekusi ().

