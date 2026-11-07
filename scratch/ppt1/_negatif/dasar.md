# BAB III ANALISIS ALTERNATIF SOLUSI

## Subbab 3.4 Pemilihan Alternatif Solusi dengan MCDM

| Kendali dokumen | Keterangan |
|---|---|
| Dokumen | Proposal Proyek Perancangan Terpadu I, BAB III subbab 3.4 |
| Mitra | PT Halliburton Indonesia, divisi Sperry Drilling |
| Versi | 1.0, 25 Oktober 2026 |
| Status | Berjalan. Subbab 3.1, 3.2, dan 3.3 sudah selesai, subbab ini menutup BAB III. |
| Acuan format | Buku Pedoman PPT Tahap I subbab 3.2 Format Proposal, halaman 33 sampai 36 |
| Acuan rubrik | Rubrik Penilaian PPT oleh Dosen, halaman 38 dan berikutnya, butir 2.2, 3.2, dan 3.3 |
| Metode | TOPSIS dengan bobot Rank-Order Centroid, pembanding SAW |
| Hasil | A1 (Relabeling onset peristiwa: dari status menjadi kejadian) dengan koefisien kedekatan 0,8465 |
| Identitas anggota | Diisi tim. Dokumen ini tidak mengarang nama maupun NIM. |

### 3.4.1 Dasar perhitungan dan aturan bukti

Riset pendahuluan: `statistical-analysis` - disiplin uji sensitivitas dan larangan menyajikan angka tanpa ketidakpastian. Poin yang dipakai: analisis sensitivitas dipakai untuk menguji apakah kesimpulan bergantung pada asumsi bobot, dan seluruh hitungan disimpan pada skrip yang dapat dijalankan ulang. Dua butir panduan yang relevan adalah "A non-significant result is not evidence of no effect" dan "Make it reproducible"; keduanya diterapkan sebagai kewajiban sembilan skenario dan skrip reproduksi.

Riset pendahuluan: `grounded-citations` - setiap klaim dari sumber luar memakai penanda dan daftar sumber yang dihasilkan mesin, bukan diketik dari ingatan. Poin yang dipakai: DOI ketiga sumber metode diperiksa lewat pencarian web pada 25 Oktober 2026 sebelum ditulis, sedangkan rujukan internal tetap memakai bentuk berkas dan nomor baris.

Riset pendahuluan: `sequentialthinking` (sequ-mcp, enam pikiran) - menetapkan urutan kerja: verifikasi sumber sebelum memakai hasil lama, penolakan AHP karena tidak ada pakar, pemilihan TOPSIS dengan SAW sebagai pembanding, penanganan dua kolom tanpa variasi, penyelesaian pertentangan C8 terhadap subbab 3.3.6 butir 8, dan penetapan batas klaim sebelum menulis.

Aturan bukti yang dipakai pada subbab ini:

1. Setiap angka pada matriks keputusan menunjuk berkas dan nomor baris, kunci JSON, atau skrip yang dapat dijalankan ulang. Kolom jejak pada tabel 3.4.1 memuat rujukan itu.
2. Angka yang belum terukur ditulis sebagai asumsi dan diberi penanda yang sama pada tabel, bukan disamarkan sebagai hasil pengukuran.
3. Skala 1 sampai 5 tidak dipakai untuk kriteria yang sudah punya angka terukur, sesuai larangan pada subbab 3.3.5. Angka asli dipakai langsung, lalu dipetakan ke skala 0 sampai 100 memakai fungsi nilai yang ditulis terbuka pada subbab 3.4.3.
4. Dokumen tim tidak disebut dengan kata yang menyiratkan tuduhan. Perbedaan angka draft lama diperiksa dengan hitung ulang, dan hasilnya ditulis sebagai temuan yang dapat diperiksa sendiri.

### 3.4.2 Pemilihan metode MCDM

Tiga metode dipertimbangkan. Yang menentukan bukan popularitas, melainkan apakah masukannya tersedia tanpa mengarang angka.

| Metode | Kebutuhan masukan | Kesesuaian dengan bukti yang ada | Keputusan | Alasan |
|---|---|---|---|---|
| AHP | perbandingan berpasangan antar kriteria oleh pakar pada skala 1 sampai 9, ditambah uji rasio konsistensi | tidak tersedia. Belum ada wawancara mitra maupun penilaian pakar, sehingga matriks perbandingan hanya bisa diisi angka karangan | ditolak | Angka perbandingan tanpa pakar adalah angka tanpa jejak, dan rasio konsistensi tidak bermakna bila masukannya karangan. Menolak AHP di sini menjaga aturan bukti, bukan menilai AHP sebagai metode lemah. |
| TOPSIS | matriks keputusan kardinal, arah tiap kriteria, dan vektor bobot | tersedia. Empat kolom berisi angka terukur (C2, C4, C5, C7), dua kolom memakai rubrik berjangkar (C1 dan C3), dan dua kolom berstatus asumsi yang ditandai terbuka (C6 minggu kerja, C8 beban kognitif). Seluruh 72 sel terisi | dipakai sebagai metode utama | Menerima campuran kriteria benefit dan cost, menghasilkan jarak ke solusi ideal dan anti-ideal sehingga selisih antar alternatif terbaca sebagai angka, dan formulanya publik sehingga dapat direproduksi pihak lain. |
| SAW | matriks keputusan kardinal dan vektor bobot, keduanya sama dengan TOPSIS | tersedia, memakai masukan identik | dipakai sebagai pembanding bebas | Bila dua metode dengan cara mengukur jarak berbeda memberi juara sama, hasil tidak bergantung pada pilihan metode. SAW tidak dipakai sendirian karena penjumlahan berbobot dapat menutupi alternatif yang sangat lemah pada satu kriteria. |

TOPSIS dipakai sebagai metode utama dan SAW sebagai pembanding bebas. Keduanya memakai matriks keputusan yang sama, sehingga perbedaan hasil hanya berasal dari cara mengukur jarak. Hasilnya: juara kedua metode sama, yaitu A1, dengan Kendall tau 0,8889. Perbedaan hanya menyangkut posisi A9, yang naik dari peringkat sembilan ke peringkat tujuh pada SAW, dan itu tidak menyentuh keputusan.

AHP ditolak dengan alasan yang perlu dinyatakan tegas: AHP menuntut perbandingan berpasangan oleh pakar, dan pada proyek ini belum ada wawancara mitra. Mengisi matriks perbandingan tanpa pakar berarti menulis angka yang tidak punya jejak, sekaligus membuat rasio konsistensi tidak bermakna. Penolakan ini soal ketersediaan bukti, bukan penilaian bahwa AHP lemah. Bila wawancara tersedia pada tahap berikutnya, AHP dapat dijalankan dan dibandingkan dengan hasil subbab ini.

Sumber metode, dengan DOI yang sudah diperiksa:

| Sumber | Dipakai untuk | DOI | Cara verifikasi |
|---|---|---|---|
| Hwang, C. L., dan Yoon, K. (1981). Multiple Attribute Decision Making: Methods and Applications, A State-of-the-Art Survey. Springer-Verlag, New York. | rumus TOPSIS, yaitu normalisasi vektor, solusi ideal positif dan negatif, serta koefisien kedekatan | `10.1007/978-3-642-48318-9` | pencarian web 25 Oktober 2026 menemukan entri Springer tahun 1981 dengan DOI tersebut, dan artikel Wikipedia TOPSIS mengutip sumber yang sama |
| Barron, F. H., dan Barrett, B. E. (1996). Decision Quality Using Ranked Attribute Weights. Management Science, 42(11), 1515 sampai 1523. | penurunan bobot kardinal dari urutan prioritas kriteria memakai Rank-Order Centroid | `10.1287/mnsc.42.11.1515` | pencarian web 25 Oktober 2026 menemukan DOI tersebut pada INFORMS, dengan abstrak yang menyatakan ROC lebih akurat daripada formula berbasis urutan lain |
| Kunsch, P. L., dan Ishizaka, A. (2019). A note on using centroid weights in additive multi-criteria decision analysis. European Journal of Operational Research. | batas pemakaian ROC. Artikel ini menunjukkan keunggulan ROC bergantung pada cara elisitasi bobot, sehingga ROC pada kartu ini wajib disertai uji sensitivitas | `10.1016/j.ejor.2019.02.021` | pencarian web 25 Oktober 2026 menemukan DOI tersebut beserta ringkasan yang menyatakan peringkat kinerja metode bobot pengganti bergantung pada definisi simpleks bobot |

Satu batas pemakaian dinyatakan di depan. Kunsch dan Ishizaka menunjukkan bahwa keunggulan bobot Rank-Order Centroid bergantung pada cara bobot seharusnya diperoleh. Karena itu bobot ROC pada subbab ini bukan bobot final mitra, melainkan bobot terbaik yang dapat dipertanggungjawabkan dari bahan yang ada, dan wajib disertai uji sensitivitas pada 3.4.8.

### 3.4.3 Kriteria, arah, dan fungsi nilai

Delapan kriteria diambil tanpa perubahan definisi dari subbab 3.3.1. Yang ditambahkan di sini hanya fungsi nilai, yaitu aturan yang mengubah satuan mentah menjadi skala 0 sampai 100 supaya dapat dibandingkan dan diukur jaraknya.

| Kode | Kriteria | Arah | Satuan mentah | Fungsi nilai ke 0 sampai 100 | Status angka |
|---|---|---|---|---|---|
| C1 | Efektivitas deteksi pada gate yang sudah dikunci | benefit | lift dalam kali dan AUPRC | rubrik 4 tingkat: 100 gate lolos, 75 dieksekusi dan delta terukur positif, 40 dieksekusi tanpa delta positif, 20 belum dieksekusi | TERUKUR untuk alternatif yang sudah dieksekusi, RUBRIK untuk sisanya |
| C4 | Kepatuhan mode advisory tanpa alarm otomatis | benefit | jumlah slot alarm otomatis, target nol, dan jumlah head dengan review manusia | 100 bila slot alarm otomatis nol, 0 bila ada satu saja | TERUKUR |
| C2 | Kecukupan bukti per fold | benefit | jumlah fold teruji dan jumlah positif per fold | 100 x jumlah fold layak dibagi 18, dibatasi 100 | TERUKUR |
| C7 | Ketertelusuran dan reproduksibilitas angka | benefit | jumlah klaim tanpa jejak, target nol | 100 x jumlah klaim berjejak dibagi jumlah klaim | TERUKUR |
| C3 | Portabilitas antar sumur | benefit | rasio false alarm rate maksimum dibagi minimum per 24 jam | rubrik 3 tingkat: 100 kalibrasi per sumur sudah diuji pada dua sumur atau lebih, 60 menambah sumur uji atau memuat rancangan kalibrasi yang belum diuji, 30 tidak menyentuh portabilitas | TERUKUR untuk gejala, RUBRIK untuk tindakan alternatif |
| C6 | Waktu penyelesaian dalam satu semester | cost | minggu kerja | 100 x (9 dikurangi minggu kerja) dibagi 9, dibatasi 0 sampai 100 | ASUMSI untuk minggu kerja per alternatif, BAKU untuk tenggat |
| C5 | Kebutuhan akuisisi data baru | cost | jumlah wellbore atau berkas yang harus diproses | 100 dibagi (1 + jumlah wellbore tersisa) | TERUKUR |
| C8 | Beban kognitif keluaran | benefit | rubrik tiga tingkat | tingkat 3 menjadi 100, tingkat 2 menjadi 50, tingkat 1 menjadi 0 | ASUMSI |

Empat hal perlu dijelaskan tentang tabel di atas.

Pertama, kriteria terukur tidak diskalakan ulang menjadi 1 sampai 5. C2 memakai jumlah fold layak dibagi 18, yaitu jumlah fold terbesar yang dimiliki satu alternatif, sehingga 18 fold layak bernilai 100 dan 9 fold bernilai 50. C5 memakai bentuk 100 dibagi (1 ditambah jumlah wellbore tersisa), sehingga nol wellbore bernilai 100. C7 memakai persentase klaim yang berjejak, dan nilainya 100 untuk seluruh alternatif karena setiap butir bukti pada subbab 3.1 membawa rujukan.

Kedua, C1 dan C3 berbentuk rubrik berjangkar karena pertanyaannya bukan besaran, melainkan keadaan pelaksanaan. C1 memakai empat tingkat: 100 bila gate G1 dan G2 lolos, 75 bila mekanisme sudah dieksekusi dan delta terukur positif, 40 bila sudah dieksekusi tanpa delta positif, dan 20 bila belum dieksekusi. C3 memakai tiga tingkat: 100 bila kalibrasi per sumur sudah diuji pada dua sumur atau lebih, 60 bila menambah sumur uji atau memuat rancangan kalibrasi yang belum diuji, dan 30 bila tidak menyentuh portabilitas. Setiap tingkat menunjuk keadaan yang dapat diperiksa pada dokumen proyek, bukan kesan penilai.

Ketiga, C8 tetap berstatus asumsi dan ini dinyatakan terbuka. Subbab 3.3.6 butir 8 menyatakan antarmuka peringatan belum dirancang sehingga C8 belum dapat dinilai untuk alternatif mana pun (`docs/PPT1_BAB3_2.md:665`). Pada subbab ini C8 tetap diisi dengan tingkat yang dibaca dari niat desain: tingkat 3 untuk alternatif yang rancangan keluarannya berupa satu baris peringatan dengan waktu, keyakinan, dan tindakan, dan tingkat 2 untuk alternatif yang keluarannya masih berupa label, daftar kandidat, atau angka yang perlu ditafsirkan. Konsekuensinya, skenario P7 pada 3.4.8 menolkan bobot C8, sehingga dapat diperiksa apakah keputusan berubah bila kriteria yang belum divalidasi itu dibuang sama sekali.

Keempat, tidak ada angka rupiah pada subbab ini. Batasan B6 mengingatkan bahwa tarif rig per jam tidak tersedia pada seluruh 13 dataset (`docs/PPT1_BAB3_2.md:659`). Karena itu biaya diukur sebagai jumlah wellbore yang harus diproses dan jumlah minggu kerja, bukan rupiah. Dengan begitu tidak ada satu pun nilai pada matriks keputusan yang bersandar pada tarif yang tidak diketahui.

Tabel 3.4.1 Jejak setiap sel matriks keputusan

| Alternatif | Kriteria | Satuan mentah | Status | Dasar | Jejak |
|---|---|---|---|---|---|
| A1 | C1 | L75 | TERUKUR | Mekanisme sudah dieksekusi untuk stuck dan hyd. Stuck memberi B1 0,51 sampai 1,00 dengan TLead 10 sampai 11,5 menit. Hyd memberi B1 nol dari tiga onset, jadi hasil negatifnya terukur. | docs/V9_EVAL_B_LAYERB.md:101, 103 |
| A1 | C4 | 0 | TERUKUR | Keluaran berupa peringatan berpengawas manusia. Registry mencatat nol slot alarm otomatis. | scratch/v9_i1/v9_i1_RESULTS.json kunci auto_critical_alarm_slots |
| A1 | C2 | 13 | TERUKUR | Tiga kelas sasaran dengan fold layak terukur: stuck 2 fold, hyd 7 fold, bit_wear 4 fold. | docs/V7_R1_SOLUTIONS.md:69, 127, 203 |
| A1 | C7 | 3/3 | TERUKUR | Tiga dari tiga butir bukti pada 3.1.4.1 membawa jejak berkas dan baris. | scratch/ppt1/alternatif.json alternatif id A1 kunci bukti |
| A1 | C3 | L30 | RUBRIK | Relabel mengubah definisi target, bukan ambang. Kalibrasi per sumur tidak termasuk lingkup, sehingga gejala 119,6 kali tetap tidak tersentuh. | docs/V9_PM2_VERDICT.md:114 |
| A1 | C6 | 2 | ASUMSI | Beban dinilai rendah pada V7 bagian 7 karena relabel dan run ulang tanpa parse. Dua minggu adalah asumsi perkiraan desain. | docs/V7_R1_SOLUTIONS.md:215 |
| A1 | C5 | 0 | TERUKUR | Relabel tidak memerlukan parse baru karena deret sumber sudah berbentuk CSV. | docs/V7_R1_SOLUTIONS.md:76 |
| A1 | C8 | 3 | RUBRIK | Keluaran satu peringatan per onset dengan waktu, keyakinan, dan tindakan yang disarankan. Tingkat 3 pada rubrik 3.3. | scratch/ppt1/affinity.json kunci kriteria id C8 |
| A2 | C1 | L20 | TERUKUR | Parse empat wellbore selesai dan terukur, namun evaluasi ulang fold belum dijalankan sehingga dampak ke gate belum dapat diklaim. | docs/V9_PM1_ARCHITECTURE.md:186; docs/PPT1_BAB3_1.md:103 |
| A2 | C4 | 0 | TERUKUR | Tidak menambah slot alarm otomatis karena hanya menambah data, bukan keluaran baru. | scratch/v9_i1/v9_i1_RESULTS.json kunci auto_critical_alarm_slots |
| A2 | C2 | 18 | TERUKUR | Empat kelas sasaran dengan fold layak terukur: shk 7, ssi 5, vib 4, stuck 2. | docs/V7_R1_SOLUTIONS.md:97, 197, 55, 69 |
| A2 | C7 | 3/3 | TERUKUR | Tiga dari tiga butir bukti pada 3.1.4.2 membawa jejak berkas dan baris. | scratch/ppt1/alternatif.json alternatif id A2 kunci bukti |
| A2 | C3 | L60 | RUBRIK | Menambah empat sumur uji sehingga portabilitas diuji pada jumlah sumur lebih banyak, tanpa memuat kalibrasi ambang per sumur. | docs/V7_R1_SOLUTIONS.md:43-48 |
| A2 | C6 | 2 | ASUMSI | Sisa pekerjaan hanya evaluasi ulang fold karena parse selesai. Dua minggu adalah asumsi perkiraan desain. | docs/PPT1_BAB3_1.md:103 |
| A2 | C5 | 3 | TERUKUR | Jalur CRPM sudah diparse pada empat wellbore dengan baris terukur, namun jalur VIBLAT untuk F-4, F-10, dan F-15 masih berstatus belum diparse, sehingga tiga wellbore tersisa untuk kelas vib. | docs/V9_PM1_ARCHITECTURE.md:186, 169 |
| A2 | C8 | 2 | RUBRIK | Tidak menghasilkan bentuk keluaran sendiri. Beban kognitif mengikuti alternatif yang memakai datanya, sehingga dinilai netral pada tingkat 2. | scratch/ppt1/affinity.json kunci kriteria id C8 |
| A3 | C1 | L20 | TERUKUR | Belum dieksekusi. Cacat label yang diserang sudah terukur, yaitu kontrol-positif stuck nol dari sepuluh. | docs/V8_PM_VERDICT.md:202; docs/PPT1_BAB3_1.md:51 |
| A3 | C4 | 0 | TERUKUR | Bekerja pada mutu label, tidak menerbitkan alarm. | scratch/v9_i1/v9_i1_RESULTS.json kunci auto_critical_alarm_slots |
| A3 | C2 | 9 | TERUKUR | Dua kelas sasaran dengan fold layak terukur: stuck 2 fold dan hyd 7 fold. | docs/V7_R1_SOLUTIONS.md:69, 127 |
| A3 | C7 | 3/3 | TERUKUR | Tiga dari tiga butir bukti pada 3.1.4.3 membawa jejak berkas dan baris. | scratch/ppt1/alternatif.json alternatif id A3 kunci bukti |
| A3 | C3 | L30 | RUBRIK | Audit semantik label lintas sumur menyentuh konsistensi antar sumur, namun tidak menetapkan kalibrasi ambang per sumur. | docs/V9_PM2_VERDICT.md:114 |
| A3 | C6 | 4 | ASUMSI | Dua tahap berurutan, audit label lalu label probabilistik. Empat minggu adalah asumsi perkiraan desain. | docs/V7_R1_SOLUTIONS.md:89 |
| A3 | C5 | 0 | TERUKUR | Memakai label kurasi dan CSV yang sudah ada, tanpa parse baru. | docs/V7_R1_SOLUTIONS.md:88 |
| A3 | C8 | 2 | RUBRIK | Keluaran berupa label, bukan peringatan operator. Beban kognitif operator tidak berubah, sehingga dinilai netral pada tingkat 2. | scratch/ppt1/affinity.json kunci kriteria id C8 |
| A4 | C1 | L20 | TERUKUR | Belum dieksekusi. Akar yang diserang terukur, yaitu dua fold underpowered pada ssi dengan 3 dan 12 positif. | docs/V7_R1_SOLUTIONS.md:197; docs/PPT1_BAB3_1.md:52 |
| A4 | C4 | 0 | TERUKUR | Tidak menerbitkan alarm otomatis. | scratch/v9_i1/v9_i1_RESULTS.json kunci auto_critical_alarm_slots |
| A4 | C2 | 12 | TERUKUR | Dua kelas sasaran dengan fold layak terukur: shk 7 fold dan ssi 5 fold. | docs/V7_R1_SOLUTIONS.md:97, 197 |
| A4 | C7 | 3/3 | TERUKUR | Tiga dari tiga butir bukti pada 3.1.4.4 membawa jejak berkas dan baris. | scratch/ppt1/alternatif.json alternatif id A4 kunci bukti |
| A4 | C3 | L30 | RUBRIK | Perubahan unit analisis tidak menetapkan kalibrasi ambang per sumur. | docs/V9_PM2_VERDICT.md:114 |
| A4 | C6 | 3 | ASUMSI | Beban rendah sampai sedang pada V7 bagian 7. Tiga minggu adalah asumsi perkiraan desain. | docs/V7_R1_SOLUTIONS.md:222 |
| A4 | C5 | 0 | TERUKUR | Memakai CSV terparse dan batas stand yang diturunkan dari kolom yang sudah ada. | docs/V7_R1_SOLUTIONS.md:112 |
| A4 | C8 | 2 | RUBRIK | Unit stand memperlebar horizon prediksi menjadi stand berikutnya, sehingga keluaran menjadi daftar kandidat tanpa urutan. Tingkat 2 pada rubrik 3.3. | docs/V7_R1_SOLUTIONS.md:113 |
| A5 | C1 | L20 | TERUKUR | Belum dieksekusi. Akar yang diserang terukur, yaitu varians AUPRC pada fold dengan 30 sampai 41 positif. | docs/V7_R1_SOLUTIONS.md:99; docs/PPT1_BAB3_1.md:53 |
| A5 | C4 | 0 | TERUKUR | Tidak menerbitkan alarm otomatis. | scratch/v9_i1/v9_i1_RESULTS.json kunci auto_critical_alarm_slots |
| A5 | C2 | 9 | TERUKUR | Dua kelas sasaran dengan fold layak terukur: ssi 5 fold dan bit_wear 4 fold. | docs/V7_R1_SOLUTIONS.md:197, 203 |
| A5 | C7 | 3/3 | TERUKUR | Tiga dari tiga butir bukti pada 3.1.4.5 membawa jejak berkas dan baris. | scratch/ppt1/alternatif.json alternatif id A5 kunci bukti |
| A5 | C3 | L30 | RUBRIK | Formulasi ordinal tidak menetapkan kalibrasi ambang per sumur. | docs/V9_PM2_VERDICT.md:114 |
| A5 | C6 | 2 | ASUMSI | Beban rendah pada V7 bagian 7. Dua minggu adalah asumsi perkiraan desain. | docs/V7_R1_SOLUTIONS.md:222 |
| A5 | C5 | 0 | TERUKUR | Kanal sudah tersedia di CSV sehingga tidak ada parse baru. | docs/V7_R1_SOLUTIONS.md:118 |
| A5 | C8 | 2 | RUBRIK | Keluaran berupa tingkat severitas tanpa urutan prioritas tindakan. Tingkat 2 pada rubrik 3.3. | docs/V7_R1_SOLUTIONS.md:117 |
| A6 | C1 | L20 | TERUKUR | Belum dieksekusi. Hasil negatif pada hyd sudah terukur, yaitu B1 nol dari tiga onset, sehingga formulasi survival tidak punya sinyal pendukung pada kelas itu. | docs/V9_EVAL_B_LAYERB.md:103; docs/PPT1_BAB3_1.md:54 |
| A6 | C4 | 0 | TERUKUR | Skor risiko per horizon tetap advisory, tanpa alarm otomatis. | scratch/v9_i1/v9_i1_RESULTS.json kunci auto_critical_alarm_slots |
| A6 | C2 | 11 | TERUKUR | Dua kelas sasaran dengan fold layak terukur: hyd 7 fold dan bit_wear 4 fold. | docs/V7_R1_SOLUTIONS.md:127, 203 |
| A6 | C7 | 3/3 | TERUKUR | Tiga dari tiga butir bukti pada 3.1.4.6 membawa jejak berkas dan baris. | scratch/ppt1/alternatif.json alternatif id A6 kunci bukti |
| A6 | C3 | L30 | RUBRIK | Survival mengubah formulasi, bukan ambang, sehingga gejala 119,6 kali tidak tersentuh. | docs/V9_PM2_VERDICT.md:114 |
| A6 | C6 | 4 | ASUMSI | Beban sedang pada V7 bagian 7. Empat minggu adalah asumsi perkiraan desain. | docs/V7_R1_SOLUTIONS.md:222 |
| A6 | C5 | 0 | TERUKUR | Diturunkan dari label yang sudah ada, tanpa parse baru. | docs/V7_R1_SOLUTIONS.md:151 |
| A6 | C8 | 2 | RUBRIK | Keluaran berupa hazard atau sisa umur yang masih perlu ditafsirkan pengguna. Tingkat 2 pada rubrik 3.3. | docs/V7_R1_SOLUTIONS.md:150 |
| A7 | C1 | L75 | TERUKUR | Mekanisme progresi sudah dijalankan pada empat dari empat alat dengan TLead 20 sampai 36 detik dan false alarm terkalibrasi 1 sampai 3 per alat, sehingga delta terukur positif, namun gate G1 tetap nol dari empat dan presisi run hanya 0,50 sehingga makna delta terbatas. | docs/V9_EVAL_C_LAYERC.md:98; docs/V7_R1_SOLUTIONS.md:160 |
| A7 | C4 | 0 | TERUKUR | Keluaran berupa status dan tren alat, tanpa alarm otomatis. | scratch/v9_i1/v9_i1_RESULTS.json kunci auto_critical_alarm_slots |
| A7 | C2 | 4 | TERUKUR | Satu domain sasaran dengan empat fold alat terukur. | docs/V7_R1_SOLUTIONS.md:160 |
| A7 | C7 | 4/4 | TERUKUR | Empat dari empat butir bukti pada 3.1.4.7 membawa jejak berkas dan baris. | scratch/ppt1/alternatif.json alternatif id A7 kunci bukti |
| A7 | C3 | L30 | RUBRIK | Domain bengkel memakai empat alat dan bukan sumur, sehingga kalibrasi per sumur tidak berlaku dan tidak dirancang. | scratch/ppt1/affinity.json kunci batasan id B5 |
| A7 | C6 | 5 | ASUMSI | Pengembangan baru berskala sedang sampai besar karena dekomposisi mode dan ranking ditambahkan. Lima minggu adalah asumsi perkiraan desain. | docs/V7_R1_SOLUTIONS.md:219; scratch/ppt1/affinity.json kunci batasan id B3 |
| A7 | C5 | 0 | TERUKUR | Delapan berkas akselerometer sudah tersedia dan terverifikasi SHA-256, tanpa parse baru. | docs/V7_R1_SOLUTIONS.md:170 |
| A7 | C8 | 2 | RUBRIK | Keluaran berupa peringkat alat yang masih perlu dibaca sebagai daftar. Tingkat 2 pada rubrik 3.3. | docs/V7_R1_SOLUTIONS.md:185 |
| A8 | C1 | L20 | TERUKUR | Belum dieksekusi. Akar yang diserang terukur, yaitu label hyd masih proksi residual SPPA dan label keausan fisik tidak tersedia. | docs/V8_PM_VERDICT.md:202; docs/V4_MAINTENANCE_ML_OPTIONS.md:62 |
| A8 | C4 | 0 | TERUKUR | Label fisika dipakai sebagai label pelatihan, bukan alarm otomatis, sehingga batasan B2 tetap terpenuhi. | scratch/ppt1/affinity.json kunci batasan id B2 |
| A8 | C2 | 11 | TERUKUR | Dua kelas sasaran dengan fold layak terukur: hyd 7 fold dan bit_wear 4 fold. | docs/V7_R1_SOLUTIONS.md:127, 203 |
| A8 | C7 | 3/3 | TERUKUR | Tiga dari tiga butir bukti pada 3.1.4.8 membawa jejak berkas dan baris. | scratch/ppt1/alternatif.json alternatif id A8 kunci bukti |
| A8 | C3 | L60 | RUBRIK | Parse kanal pit dan flow pada F-9 serta F-1 C dan F-11 menambah sumur uji, tanpa rancangan kalibrasi ambang per sumur. | docs/V7_R1_SOLUTIONS.md:145 |
| A8 | C6 | 5 | ASUMSI | Beban rendah untuk label MSE dan DS ditambah beban sedang sampai besar untuk parse pit dan flow. Lima minggu adalah asumsi perkiraan desain. | docs/V7_R1_SOLUTIONS.md:146, 183 |
| A8 | C5 | 2 | TERUKUR | Dua sumur memerlukan parse tambahan, yaitu kanal pit mentah F-9 dan F-1 C atau F-11. | docs/V7_R1_SOLUTIONS.md:145 |
| A8 | C8 | 2 | RUBRIK | Mengubah sumber label tanpa mengubah bentuk keluaran, sehingga beban kognitif operator dinilai netral pada tingkat 2. | scratch/ppt1/affinity.json kunci kriteria id C8 |
| A9 | C1 | L20 | TERUKUR | Belum dieksekusi. Gejala yang diserang terukur, yaitu sebaran false alarm 4,15 sampai 496,09 per 24 jam. | docs/V9_PM2_VERDICT.md:114; docs/PPT1_BAB3_1.md:57 |
| A9 | C4 | 0 | TERUKUR | Purwarupa peringatan dini tetap advisory dengan review manusia, sesuai batasan B2. | scratch/v9_i1/v9_i1_RESULTS.json kunci auto_critical_alarm_slots |
| A9 | C2 | 6 | TERUKUR | Dua kelas sasaran dengan fold layak terukur: vib 4 fold dan stuck 2 fold. | docs/V7_R1_SOLUTIONS.md:55, 69 |
| A9 | C7 | 4/4 | TERUKUR | Empat dari empat butir bukti pada 3.1.4.9 membawa jejak berkas dan baris, termasuk kunci JSON registry. | scratch/ppt1/alternatif.json alternatif id A9 kunci bukti |
| A9 | C3 | L60 | RUBRIK | Memuat rancangan kalibrasi ambang per sumur sebagai inti pekerjaan, namun belum diuji pada dua sumur atau lebih. | docs/V9_PM2_VERDICT.md:114; docs/PPT1_BAB3_1.md:57 |
| A9 | C6 | 4 | ASUMSI | Kalibrasi ambang ditambah purwarupa peringatan. Empat minggu adalah asumsi perkiraan desain. | scratch/ppt1/affinity.json kunci batasan id B3 |
| A9 | C5 | 0 | TERUKUR | Memakai registry head dan CSV yang sudah ada, tanpa parse baru. | docs/V4_MAINTENANCE_ML_OPTIONS.md:58 |
| A9 | C8 | 3 | RUBRIK | Rancangan keluaran berupa satu baris peringatan dengan waktu, keyakinan, dan tindakan, serta frekuensi pemeriksaan satu kali per empat jam. Tingkat 3 pada rubrik 3.3. | docs/V8_R1_ABC_SPEC.md:240; docs/PPT1_BAB3_2.md:471 |

### 3.4.4 Bobot kriteria

Bobot tidak ditetapkan sebagai angka bulat. Yang tersedia pada proyek ini adalah urutan prioritas, bukan rasio antar kriteria, sehingga urutan itu diturunkan menjadi bobot kardinal dengan Rank-Order Centroid. Aturan penyusunan urutan ditulis lebih dahulu, supaya urutan itu dapat dibantah.

| Kode | Aturan pengurutan | Kriteria | Dasar |
|---|---|---|---|
| R1 | kriteria yang menjadi definisi lulus gate | C1 | Gate G1 dan G2 adalah definisi operasional lulus pada docs/V7_R1_SOLUTIONS.md:97, 127, 197, 203, 160, sehingga kriteria yang mengukur gate mendahului semua kriteria lain. |
| R2 | batasan keras yang menggugurkan, dengan jumlah user story terbanyak | C4 | Batasan B2 pada scratch/ppt1/affinity.json menggugurkan alternatif yang mengklaim alarm otomatis, dan tiga user story bergantung pada C4 yaitu U2, U4, dan U6, terbanyak di antara delapan kriteria. |
| R3 | batasan keras yang menggugurkan, jumlah user story lebih sedikit | C2 | Batasan B4 menetapkan urutan kerja label lebih dahulu, dan dua user story bergantung pada C2 yaitu U1 dan U5. |
| R4 | batasan keras yang menuntut jejak, tanpa menggugurkan | C7 | Batasan B1 menuntut seluruh angka dapat diaudit, sifatnya administratif sehingga tidak menggugurkan alternatif, dan tiga user story bergantung pada C7 yaitu U4, U5, dan U6. |
| R5 | gejala terukur yang belum menjadi batasan | C3 | Sebaran false alarm rate 4,15 sampai 496,09 per 24 jam sudah terukur pada docs/V9_PM2_VERDICT.md:114, tetapi belum ada alternatif yang menguji kalibrasi per sumur, sehingga kriteria ini penting namun belum menggugurkan. |
| R6 | batasan jadwal dengan daya beda rendah | C6 | Tenggat sembilan minggu mengikat seluruh tim menurut Buku Pedoman PPT Tahap I Tabel 3.1 halaman 32, namun seluruh alternatif berada pada rentang dua sampai lima minggu sehingga daya bedanya kecil dan tidak ada user story yang bergantung padanya. |
| R7 | biaya data yang bersifat instrumental | C5 | Sebagian besar parse sudah selesai pada kampanye V9 menurut docs/V9_PM1_ARCHITECTURE.md:186, sehingga kebutuhan data baru hanya membedakan beberapa alternatif. |
| R8 | kriteria dengan bukti terlemah | C8 | Rubrik C8 disusun pada subbab 3.3 dan belum divalidasi mitra, bahkan docs/PPT1_BAB3_2.md:665 menyatakan antarmuka peringatan belum dirancang. Peringkat terakhir menandai kekuatan bukti, bukan ketidakpentingan. |

Aturan dibaca berurutan dari R1 sampai R8: kriteria yang memenuhi aturan lebih awal mendapat peringkat lebih tinggi. Di dalam kelompok batasan keras, dua hal menentukan urutan, yaitu sifat menggugurkan atau tidaknya pelanggaran lebih dahulu, lalu jumlah user story yang bergantung pada kriteria itu menurut `scratch/ppt1/affinity.json` kunci `matriks_us_kriteria`.

| Peringkat | Kriteria | Aturan | Bobot ROC | Alasan ringkas |
|---|---|---|---|---|
| 1 | C1 Efektivitas deteksi pada gate yang sudah dikunci | R1 | 0,3397 | Gate G1 dan G2 adalah definisi operasional lulus, sehingga kriteria ini mengukur apakah alternatif bekerja sama sekali. Rubrik 4.1 menuntut pemilihan memakai performance metrics yang ditetapkan lebih dahulu, dan U1 sebagai pemilik masalah utama bergantung pada C1. |
| 2 | C4 Kepatuhan mode advisory tanpa alarm otomatis | R2 | 0,2147 | Batasan B2 bersifat keras karena pelanggarannya membuat alat tidak boleh dipakai, bukan sekadar menurunkan skor. Tiga user story bergantung pada kriteria ini, yaitu U2, U4, dan U6, jumlah terbanyak di antara delapan kriteria. |
| 3 | C2 Kecukupan bukti per fold | R3 | 0,1522 | Batasan B4 menetapkan label dibereskan lebih dahulu, dan aturan kampanye menyatakan fold dengan kurang dari 30 positif berstatus underpowered sehingga tidak boleh dihitung sebagai mayoritas. Dua user story bergantung pada C2, yaitu U1 dan U5. |
| 4 | C7 Ketertelusuran dan reproduksibilitas angka | R4 | 0,1106 | Tiga user story bergantung pada C7, yaitu U4, U5, dan U6. Batasan B1 menuntut seluruh angka dapat diaudit pihak lain, dan rubrik 3.2 menuntut batasan standar yang dijelaskan dengan justifikasi kuat. |
| 5 | C3 Portabilitas antar sumur | R5 | 0,0793 | Sebaran false alarm rate terukur 4,15 sampai 496,09 per 24 jam pada titik operasi yang sama, yaitu rasio 119,6 kali, sehingga satu ambang global tidak portabel. Dua user story bergantung pada C3, yaitu U1 dan U2. |
| 6 | C6 Waktu penyelesaian dalam satu semester | R6 | 0,0543 | Batasan B3 bersifat keras karena jadwal Tabel 3.1 mengikat seluruh tim, namun kriteria ini berlaku hampir sama untuk semua alternatif sehingga daya bedanya rendah. Tidak ada user story yang bergantung padanya, sehingga peringkatnya tidak boleh lebih tinggi daripada kriteria yang punya pemangku kepentingan. |
| 7 | C5 Kebutuhan akuisisi data baru | R7 | 0,0335 | Biaya data bersifat instrumental karena hanya bermakna lewat kriteria lain. Satu user story bergantung padanya, yaitu U3, dan sebagian besar kebutuhan parse sudah dikerjakan pada kampanye V9 sehingga daya bedanya menyusut. |
| 8 | C8 Beban kognitif keluaran | R8 | 0,0156 | Hanya satu user story yang bergantung padanya, yaitu U2, dan rubriknya belum divalidasi mitra sehingga statusnya masih asumsi. Peringkat terakhir bukan berarti kriteria ini tidak penting, melainkan menandakan bukti pendukungnya paling lemah di antara delapan kriteria. |

Rumus yang dipakai: untuk n kriteria dan peringkat i, bobot sama dengan satu per n dikali jumlah satu per k untuk k dari i sampai n. Untuk delapan kriteria, peringkat satu menghasilkan 0,3397 dan peringkat delapan menghasilkan 0,0156. Pemeriksaan jumlah:

- Jumlah delapan bobot = 1,000000000000
- Bobot terbesar 0,3397 pada kriteria yang memenuhi R1, bobot terkecil 0,0156 pada kriteria yang memenuhi R8
- Rasio bobot terbesar terhadap terkecil = 21,74

Status bobot ini adalah ASUMSI, dengan dua alasan yang ditulis apa adanya: belum ada wawancara mitra yang menetapkan prioritas, dan ROC adalah pendekatan, bukan elisitasi langsung. Satu kelemahan perlu disebut di sini, bukan hanya di bagian hasil: karena C4 menempati peringkat dua, kriteria yang pada matriks ternyata tidak membedakan justru menerima bobot terbesar kedua. Hal itu tidak diubah tanpa pemberitahuan, sebab menurunkan peringkat C4 akan berarti mengubah penilaian tentang kekerasan batasan B2. Yang dilakukan adalah menguji akibatnya lewat skenario P6, yang menolkan bobot C4 dan C7. Karena status bobotnya asumsi, subbab ini tidak berhenti pada satu vektor bobot, melainkan menguji sembilan skenario, enam belas uji satu per satu, dan satu sapuan penuh pada kriteria terpenting. Yang menentukan adalah apakah juara berubah, bukan apakah angkanya bergeser.

### 3.4.5 Matriks keputusan

Matriks berukuran sembilan alternatif kali delapan kriteria, seluruhnya 72 sel terisi. Tabel 3.4.2 memuat satuan mentah supaya dapat dicocokkan dengan berkas sumber, sedangkan tabel 3.4.3 memuat nilai baku yang masuk hitungan.

Tabel 3.4.2 Matriks keputusan dalam satuan mentah

| Alternatif | C1 | C4 | C2 | C7 | C3 | C6 | C5 | C8 |
|---|---|---|---|---|---|---|---|---|
| A1 | L75 | 0 | 13 | 3/3 | L30 | 2 | 0 | 3 |
| A2 | L20 | 0 | 18 | 3/3 | L60 | 2 | 3 | 2 |
| A3 | L20 | 0 | 9 | 3/3 | L30 | 4 | 0 | 2 |
| A4 | L20 | 0 | 12 | 3/3 | L30 | 3 | 0 | 2 |
| A5 | L20 | 0 | 9 | 3/3 | L30 | 2 | 0 | 2 |
| A6 | L20 | 0 | 11 | 3/3 | L30 | 4 | 0 | 2 |
| A7 | L75 | 0 | 4 | 4/4 | L30 | 5 | 0 | 2 |
| A8 | L20 | 0 | 11 | 3/3 | L60 | 5 | 2 | 2 |
| A9 | L20 | 0 | 6 | 4/4 | L60 | 4 | 0 | 3 |

Keterangan satuan: C1 dan C3 memakai kode tingkat rubrik, yaitu L100, L75, L60, L40, L30, dan L20. C2 memakai jumlah fold layak, C4 jumlah slot alarm otomatis, C5 jumlah wellbore atau berkas yang harus diproses, C6 jumlah minggu kerja, C7 jumlah klaim berjejak dibagi jumlah klaim, dan C8 tingkat rubrik beban kognitif.

Tabel 3.4.3 Matriks nilai baku 0 sampai 100

| Alternatif | C1 | C4 | C2 | C7 | C3 | C6 | C5 | C8 |
|---|---|---|---|---|---|---|---|---|
| A1 | 75,00 | 100,00 | 72,22 | 100,00 | 30,00 | 77,78 | 100,00 | 100,00 |
| A2 | 20,00 | 100,00 | 100,00 | 100,00 | 60,00 | 77,78 | 25,00 | 50,00 |
| A3 | 20,00 | 100,00 | 50,00 | 100,00 | 30,00 | 55,56 | 100,00 | 50,00 |
| A4 | 20,00 | 100,00 | 66,67 | 100,00 | 30,00 | 66,67 | 100,00 | 50,00 |
| A5 | 20,00 | 100,00 | 50,00 | 100,00 | 30,00 | 77,78 | 100,00 | 50,00 |
| A6 | 20,00 | 100,00 | 61,11 | 100,00 | 30,00 | 55,56 | 100,00 | 50,00 |
| A7 | 75,00 | 100,00 | 22,22 | 100,00 | 30,00 | 44,44 | 100,00 | 50,00 |
| A8 | 20,00 | 100,00 | 61,11 | 100,00 | 60,00 | 44,44 | 33,33 | 50,00 |
| A9 | 20,00 | 100,00 | 33,33 | 100,00 | 60,00 | 55,56 | 100,00 | 100,00 |

Daya beda kolom diperiksa sebelum bobot dipakai. Kolom tanpa variasi: C4, C7. Keduanya bernilai sama untuk sembilan alternatif, yaitu nol slot alarm otomatis untuk C4 dan 100 untuk C7, sehingga tidak mungkin mengubah urutan. Massa bobot yang benar-benar membedakan hanya 0,6747, sedangkan 0,3253 berada pada dua kolom yang tidak membedakan. Ini bukan cacat hitungan, melainkan fakta tentang alternatifnya: pada tahap ini tidak ada alternatif yang mengusulkan alarm otomatis, dan semua alternatif membawa jejak bukti. Konsekuensinya diuji lewat skenario P6 yang menolkan bobot kedua kolom tersebut.

### 3.4.6 Perhitungan TOPSIS

Lima langkah, seluruhnya dijalankan oleh `scratch/ppt1/build_mcdm.py`.

1. Normalisasi vektor per kolom: setiap nilai dibagi akar jumlah kuadrat kolomnya.
2. Pembobotan: nilai ternormalisasi dikali bobot kriteria.
3. Solusi ideal positif dan negatif: nilai terbesar dan terkecil per kolom pada matriks berbobot.
4. Jarak Euclidean setiap alternatif ke kedua solusi ideal, yaitu D plus dan D minus.
5. Koefisien kedekatan C sama dengan D minus dibagi (D plus ditambah D minus). Nilai satu berarti paling dekat ke ideal.

| Kriteria | Pembagi normalisasi | Ideal positif | Ideal negatif | Bobot |
|---|---|---|---|---|
| C1 | 118,5327 | 0,2150 | 0,0573 | 0,3397 |
| C4 | 300,0000 | 0,0716 | 0,0716 | 0,2147 |
| C2 | 183,6697 | 0,0829 | 0,0184 | 0,1522 |
| C7 | 300,0000 | 0,0369 | 0,0369 | 0,1106 |
| C3 | 127,2792 | 0,0374 | 0,0187 | 0,0793 |
| C6 | 189,2154 | 0,0223 | 0,0128 | 0,0543 |
| C5 | 267,8360 | 0,0125 | 0,0031 | 0,0335 |
| C8 | 193,6492 | 0,0081 | 0,0040 | 0,0156 |

Tabel 3.4.4 Hasil TOPSIS

| Peringkat | Alternatif | Nama | D plus | D minus | Koefisien kedekatan C |
|---|---|---|---|---|---|
| 1 | A1 | Relabeling onset peristiwa: dari status menjadi kejadian | 0,0297 | 0,1636 | 0,8465 |
| 2 | A7 | Penguatan kampanye keausan alat bengkel | 0,0679 | 0,1579 | 0,6993 |
| 3 | A2 | Perluasan wellbore berkanal disfungsi F-10, F-4, F-12, F-15 | 0,1580 | 0,0678 | 0,3003 |
| 4 | A4 | Unit analisis per-stand pengeboran | 0,1612 | 0,0385 | 0,1930 |
| 5 | A8 | Label fisika pengganti label proksi | 0,1615 | 0,0373 | 0,1876 |
| 6 | A6 | Formulasi survival dan sisa umur pakai | 0,1622 | 0,0337 | 0,1721 |
| 7 | A5 | Prediksi severity ordinal dengan evaluasi stabilitas fold | 0,1641 | 0,0266 | 0,1396 |
| 8 | A3 | Penjaminan mutu label dan label probabilistik multi-sumber | 0,1642 | 0,0251 | 0,1324 |
| 9 | A9 | Lapisan keputusan operasional: kalibrasi ambang per sumur dan purwarupa peringatan dini | 0,1672 | 0,0234 | 0,1229 |

Selisih koefisien antara peringkat satu dan dua adalah 0,1473, sedangkan antara peringkat dua dan tiga adalah 0,3989. Lompatan terbesar karena itu berada di antara peringkat dua dan tiga, bukan di puncak. Artinya dua alternatif teratas membentuk kelompok tersendiri, dan jaraknya ke kelompok berikutnya jauh lebih lebar daripada jarak antar keduanya. Alasannya terbaca pada tabel kontribusi berikut, yang memecah koefisien menjadi sumbangan tiap kriteria.

Tabel 3.4.5 Kontribusi tiap kriteria pada tiga besar (nilai V sama dengan bobot kali nilai ternormalisasi)

| Kriteria | Bobot | A1 | A7 | A2 | Selisih A1 dikurangi A7 |
|---|---|---|---|---|---|
| C1 | 0,3397 | 0,21496 | 0,21496 | 0,05732 | +0,00000 |
| C4 | 0,2147 | 0,07158 | 0,07158 | 0,07158 | +0,00000 |
| C2 | 0,1522 | 0,05986 | 0,01842 | 0,08288 | +0,04144 |
| C7 | 0,1106 | 0,03685 | 0,03685 | 0,03685 | +0,00000 |
| C3 | 0,0793 | 0,01869 | 0,01869 | 0,03739 | +0,00000 |
| C6 | 0,0543 | 0,02233 | 0,01276 | 0,02233 | +0,00957 |
| C5 | 0,0335 | 0,01250 | 0,01250 | 0,00313 | +0,00000 |
| C8 | 0,0156 | 0,00807 | 0,00403 | 0,00403 | +0,00403 |

Kontribusi yang menentukan kemenangan A1 adalah C2 sebesar +0,04144, C6 sebesar +0,00957, C8 sebesar +0,00403, sedangkan pada kriteria lain selisihnya nol sehingga A7 tidak unggul pada satu kriteria pun. Dengan kata lain, kemenangan itu berasal dari selisih pada kriteria yang berbobot besar, bukan dari keunggulan menyeluruh.

Perlu dicatat bahwa A1 dan A7 sama-sama bernilai 75 pada C1, karena keduanya sudah dieksekusi dan memberi delta terukur positif, yaitu stuck dengan B1 0,51 sampai 1,00 pada `docs/V9_EVAL_B_LAYERB.md:101` dan alat bengkel dengan lead time 20 sampai 36 detik pada `docs/V9_EVAL_C_LAYERC.md:98`. Yang memisahkan keduanya adalah kriteria lain, terutama jumlah fold layak, beban kognitif, dan waktu kerja. Penilaian C1 untuk A1 juga tidak seragam antar kelas: pada kelas hyd hasilnya negatif, yaitu nol dari tiga onset menurut `docs/V9_EVAL_B_LAYERB.md:103`, dan itu dicatat terbuka, bukan dirata-ratakan menjadi kemenangan.

### 3.4.7 Pembanding SAW

SAW memakai normalisasi vektor dan bobot yang sama, lalu menjumlahkan hasil kali bobot dengan nilai ternormalisasi. Karena tidak memakai titik ideal, hasilnya dapat berbeda bila ada alternatif yang menonjol pada satu kriteria tetapi lemah pada kriteria lain.

| Peringkat | Alternatif | Skor SAW | Peringkat TOPSIS |
|---|---|---|---|
| 1 | A1 | 0,4448 | 1 |
| 2 | A7 | 0,3898 | 2 |
| 3 | A2 | 0,3155 | 3 |
| 4 | A4 | 0,2754 | 4 |
| 5 | A8 | 0,2748 | 5 |
| 6 | A6 | 0,2676 | 6 |
| 7 | A9 | 0,2673 | 9 |
| 8 | A5 | 0,2648 | 7 |
| 9 | A3 | 0,2584 | 8 |

Kendall tau antara peringkat TOPSIS dan SAW adalah 0,8889. Dengan sembilan alternatif, jumlah pasangan adalah 36, sehingga nilai itu berarti 34 pasangan sepakat dan 2 pasangan berbeda. Pasangan yang berbeda adalah A3 terhadap A9, A5 terhadap A9. Keduanya melibatkan posisi peringkat tujuh sampai sembilan, jauh di bawah dua besar. Juara kedua metode sama, yaitu A1, sehingga keputusan tidak bergantung pada pilihan metode.

### 3.4.8 Uji sensitivitas

Uji dilakukan pada tiga tingkat. Pertama, sembilan skenario vektor bobot yang mewakili pembacaan berbeda atas prioritas. Kedua, enam belas uji satu per satu, yaitu setiap bobot dikali 1,5 lalu 0,5 dan dinormalkan ulang. Ketiga, satu sapuan penuh bobot C1 dari nol sampai 0,90 untuk mencari titik balik juara.

Tabel 3.4.6 Sembilan skenario bobot

| Skenario | Nama | Jenis | C1 | C4 | C2 | C7 | C3 | C6 | C5 | C8 | Juara | Tiga besar | Tau terhadap P0 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P0 | Dasar, ROC atas peringkat | bobot | 0,340 | 0,215 | 0,152 | 0,111 | 0,079 | 0,054 | 0,033 | 0,016 | A1 | A1, A7, A2 | 1,0000 |
| P1 | Bobot sama | bobot | 0,125 | 0,125 | 0,125 | 0,125 | 0,125 | 0,125 | 0,125 | 0,125 | A1 | A1, A7, A2 | 0,5000 |
| P2 | Gate dominan | bobot | 0,550 | 0,146 | 0,104 | 0,075 | 0,054 | 0,037 | 0,023 | 0,011 | A1 | A1, A7, A2 | 1,0000 |
| P3 | Label dahulu | bobot | 0,184 | 0,117 | 0,350 | 0,250 | 0,043 | 0,029 | 0,018 | 0,008 | A1 | A1, A2, A4 | 0,7778 |
| P4 | Kelayakan dahulu | bobot | 0,149 | 0,094 | 0,067 | 0,048 | 0,035 | 0,300 | 0,300 | 0,007 | A1 | A1, A7, A5 | 0,3889 |
| P5 | Konvensi skor netral | skor | 0,340 | 0,215 | 0,152 | 0,111 | 0,079 | 0,054 | 0,033 | 0,016 | A1 | A1, A2, A4 | 0,6111 |
| P6 | Tanpa kriteria penyaring | bobot | 0,504 | 0,000 | 0,226 | 0,000 | 0,118 | 0,081 | 0,050 | 0,023 | A1 | A1, A7, A2 | 1,0000 |
| P7 | Beban kognitif dinolkan | bobot | 0,345 | 0,218 | 0,155 | 0,112 | 0,081 | 0,055 | 0,034 | 0,000 | A1 | A1, A7, A2 | 1,0000 |
| P8 | Portabilitas dominan | bobot | 0,258 | 0,163 | 0,116 | 0,084 | 0,300 | 0,041 | 0,025 | 0,012 | A1 | A1, A7, A2 | 0,7222 |

- P0 Dasar, ROC atas peringkat: Peringkat 1 sampai 8 diturunkan dari aturan R1 sampai R8 pada 3.4.4, lalu diubah menjadi bobot dengan Rank-Order Centroid.
- P1 Bobot sama: Delapan kriteria berbobot 0,125. Menguji apakah hasil bergantung pada penurunan ROC.
- P2 Gate dominan: C1 ditetapkan 0,55 dan sisanya dibagi proporsional dari bobot dasar. Menguji pembacaan paling ketat terhadap gate G1 dan G2.
- P3 Label dahulu: C2 ditetapkan 0,35 dan C7 0,25, sisanya proporsional. Menguji pembacaan V8_PM_VERDICT:202 yang menaruh mutu label sebagai prasyarat.
- P4 Kelayakan dahulu: C5 ditetapkan 0,30 dan C6 0,30, sisanya proporsional. Menguji pembacaan yang mengutamakan selesai dalam satu semester.
- P5 Konvensi skor netral: Bobot kembali ke ROC, tetapi alternatif yang belum dieksekusi diberi nilai C1 50 dan A7 60, sehingga penalti bukti dihapus.
- P6 Tanpa kriteria penyaring: C4 dan C7 diberi bobot nol karena kolomnya tidak membedakan, lalu enam kriteria yang tersisa dinormalkan ulang. Menguji apakah keputusan berubah bila kriteria penyaring dipakai sebagai saringan lulus atau gagal, bukan sebagai bobot.
- P7 Beban kognitif dinolkan: C8 diberi bobot nol. Alasannya terbuka: subbab 3.3.6 butir 8 menyatakan antarmuka peringatan belum dirancang, sehingga C8 pada kartu ini berstatus niat desain, bukan hasil uji. Skenario ini membuktikan keputusan tidak bergantung pada kriteria yang belum divalidasi.
- P8 Portabilitas dominan: C3 ditetapkan 0,30 dan sisanya dibagi proporsional. Menguji pembacaan yang menempatkan ketidakportabelan ambang, yaitu sebaran 4,15 sampai 496,09 per 24 jam, sebagai masalah utama sebagaimana dinyatakan pada V9_PM2_VERDICT.md:114.

Hasil sembilan skenario: juara yang muncul hanya A1, dan 9 dari 9 skenario memilih A1.

Tabel 3.4.7 Enam belas uji satu per satu

| Kriteria | Arah | Bobot baru | Juara | Juara berubah |
|---|---|---|---|---|
| C1 | naik 50 persen | 0,4356 | A1 | tidak |
| C1 | turun 50 persen | 0,2046 | A1 | tidak |
| C4 | naik 50 persen | 0,2909 | A1 | tidak |
| C4 | turun 50 persen | 0,1203 | A1 | tidak |
| C2 | naik 50 persen | 0,2122 | A1 | tidak |
| C2 | turun 50 persen | 0,0824 | A1 | tidak |
| C7 | naik 50 persen | 0,1572 | A1 | tidak |
| C7 | turun 50 persen | 0,0585 | A1 | tidak |
| C3 | naik 50 persen | 0,1144 | A1 | tidak |
| C3 | turun 50 persen | 0,0413 | A1 | tidak |
| C6 | naik 50 persen | 0,0793 | A1 | tidak |
| C6 | turun 50 persen | 0,0279 | A1 | tidak |
| C5 | naik 50 persen | 0,0494 | A1 | tidak |
| C5 | turun 50 persen | 0,0170 | A1 | tidak |
| C8 | naik 50 persen | 0,0233 | A1 | tidak |
| C8 | turun 50 persen | 0,0079 | A1 | tidak |

Dari 16 uji satu per satu, tidak satu pun mengubah juara, dengan hitungan 0 dari 16. Artinya juara tidak bergantung pada satu bobot saja, termasuk pada kriteria yang bobotnya paling besar.

Tabel 3.4.8 Sapuan bobot C1

| Juara | Bobot C1 dari | Bobot C1 sampai |
|---|---|---|
| A2 | 0,0000 | 0,1000 |
| A1 | 0,1050 | 0,9000 |

Titik balik juara berada pada bobot C1 = 0,1050. Di bawah nilai itu A2 menang, di atasnya A1 menang. Bobot C1 pada skenario dasar adalah 0,3397, dan skenario bobot sama memberi C1 = 0,1250. Keduanya berada di atas titik balik, sehingga hasil tidak bergantung pada penurunan ROC yang memberi C1 bobot besar.

Tabel 3.4.9 Stabilitas peringkat pada seluruh uji

| Alternatif | Menjadi juara | Masuk tiga besar | Peringkat terburuk | Jumlah kasus |
|---|---|---|---|---|
| A1 | 25 | 25 | 1 | 25 |
| A2 | 0 | 24 | 8 | 25 |
| A3 | 0 | 0 | 9 | 25 |
| A4 | 0 | 2 | 6 | 25 |
| A5 | 0 | 1 | 8 | 25 |
| A6 | 0 | 0 | 7 | 25 |
| A7 | 0 | 23 | 9 | 25 |
| A8 | 0 | 0 | 9 | 25 |
| A9 | 0 | 0 | 9 | 25 |

Jumlah kasus adalah 25, yaitu 9 skenario ditambah 16 uji satu per satu. A1 menjadi juara pada seluruh 25 kasus dan tidak pernah turun dari peringkat satu. Posisi tiga besar dihuni A1, A2, A4, A5, A7, dengan A7 masuk 23 kali dan A2 masuk 24 kali dari 25 kasus. Selain itu hanya A4 yang menyentuh tiga besar sebanyak 2 kali dan A5 sebanyak 1 kali, dan itu terjadi ketika bobot kriteria yang menjadi kekuatannya dinaikkan, bukan ketika bobot diturunkan.

### 3.4.9 Perbandingan dengan draft lama

Draft 13 Agustus 2026 memilih A1 ML Classifier dipadukan A3 SHAP dashboard, memakai enam kriteria berskala 1 sampai 5 tanpa rubrik dan bobot 0,25, 0,20, 0,15, 0,10, 0,15, 0,15 (`scratch/ppt1/docx_draft_text.txt:228-279`). Dua pemeriksaan dilakukan: menghitung ulang jumlah berbobot setiap baris, dan menjalankan TOPSIS sejati pada matriks draft itu sendiri.

Tabel 3.4.10 Hitung ulang jumlah berbobot draft lama

| Alternatif draft | Skor K1 sampai K6 | Total tertulis | Total hitung ulang | Selisih | Dapat direproduksi |
|---|---|---|---|---|---|
| A1 ML Classifier | 5, 5, 4, 3, 4, 4 | 4,35 | 4,35 | 0,00 | ya |
| A2 IsoForest | 4, 3, 3, 4, 3, 3 | 3,40 | 3,35 | -0,05 | tidak |
| A3 SHAP Dash | 3, 2, 5, 4, 5, 3 | 3,55 | 3,50 | -0,05 | tidak |
| A4 Rule-based | 3, 2, 2, 5, 5, 2 | 2,95 | 3,00 | 0,05 | tidak |
| A6 LOGIX Intg | 2, 1, 3, 2, 5, 2 | 2,45 | 2,40 | -0,05 | tidak |

Dari lima baris, 1 dapat direproduksi dan 4 tidak. Selisihnya 0,05 pada empat baris. Temuan ini bukan tuduhan, melainkan akibat langsung dari skala 1 sampai 5 tanpa rubrik: karena tidak ada aturan resmi yang menghubungkan angka 5 pada K1 dengan keadaan tertentu, selisih sekecil itu tidak dapat diketahui pembaca. Pada subbab ini hal yang sama dicegah dengan fungsi nilai yang ditulis terbuka pada 3.4.3 dan pemeriksa otomatis.

Peta kriteria draft ke kriteria subbab 3.3:

| Kriteria draft | Kriteria subbab 3.3 | Status | Catatan |
|---|---|---|---|
| K1 Recall (bobot 0,25) | C1 | terpetakan | Keduanya mengukur efektivitas deteksi. Bedanya, K1 memakai skor 1 sampai 5 tanpa rubrik, sedangkan C1 memakai lift dan AUPRC terukur yang sudah ada pada docs/V7_R1_SOLUTIONS.md:97, 127, 197, 203, 160. |
| K2 Lead time (bobot 0,20) | tidak punya kriteria sendiri | terpetakan sebagian | Angka lead time memang terukur, yaitu 10 sampai 11,5 menit pada stuck dan 20 sampai 36 detik pada alat bengkel, tetapi hanya untuk dua kelas. Karena tidak tersedia untuk tujuh kelas lain, lead time tidak dapat dipakai sebagai kriteria pemilihan lintas alternatif. |
| K3 Explainability (bobot 0,15) | C8 | terpetakan sebagian | C8 mengukur beban kognitif keluaran, bukan kualitas penjelasan model. Keduanya bersinggungan pada keterbacaan hasil, dan keduanya berstatus asumsi karena belum divalidasi mitra. |
| K4 Biaya implementasi (bobot 0,10) | C5 dan C6 | terpetakan | Biaya dipecah menjadi kebutuhan data dan waktu kerja. Rupiah tidak dipakai pada kedua sisi karena tarif rig tidak tersedia pada seluruh 13 dataset, sesuai docs/PPT1_BAB3_2.md:659. |
| K5 Kemudahan integrasi (bobot 0,15) | tidak terpetakan | tidak dapat dipertahankan | Tidak ada berkas proyek yang mengukur biaya integrasi ke sistem mitra, dan telemetri mitra tidak dipakai menurut batasan B1. Skor integrasi pada draft karena itu tidak punya jejak. |
| K6 ROI (bobot 0,15) | tidak terpetakan | tidak dapat dipertahankan | Tarif rig per jam tidak ada pada seluruh dataset, sehingga ROI dalam rupiah tidak dapat dihitung. Menuliskan angka ROI berarti menulis asumsi sebagai hasil ukur. |

Dua dari enam kriteria draft, yaitu K5 kemudahan integrasi dan K6 ROI, tidak dapat dipertahankan karena tidak ada berkas proyek yang mengukurnya. Karena itu perbandingan angka mentah antara TOPSIS subbab ini dan skor draft tidak bermakna. Yang dibandingkan adalah keputusan dan alasannya.

Tabel 3.4.11 TOPSIS sejati pada matriks draft lama

| Peringkat | Alternatif draft | D plus | D minus | C |
|---|---|---|---|---|
| 1 | A1 ML Classifier | 0,0340 | 0,1666 | 0,8306 |
| 2 | A2 IsoForest | 0,0879 | 0,0957 | 0,5213 |
| 3 | A3 SHAP Dash | 0,1141 | 0,0845 | 0,4255 |
| 4 | A4 Rule-based | 0,1330 | 0,0641 | 0,3251 |
| 5 | A6 LOGIX Intg | 0,1693 | 0,0355 | 0,1731 |

Tiga kesimpulan perbandingan, ditulis apa adanya.

Pertama, label juara sama tetapi isinya berbeda, dan ini harus dinyatakan terbuka. Draft memilih A1 yang berarti pengklasifikasi pembelajaran mesin. Pada subbab 3.1, A1 berarti relabeling onset peristiwa, yaitu memindahkan definisi target dari status ke titik masuk peristiwa, dan justru mekanisme itulah yang membuat pengklasifikasi dapat bekerja. Jadi kesamaan huruf A1 bukan kesamaan objek pemilihan. Yang benar-benar sejalan adalah arah: pembelajaran terbimbing di atas label onset dengan keluaran berpengawas manusia.

Kedua, draft menyebut metodenya TOPSIS (`scratch/ppt1/docx_draft_text.txt:229`), tetapi angka yang ditulis pada tabel draft adalah jumlah berbobot, yaitu skor dikali bobot lalu dijumlahkan. Hitungan itu adalah SAW, bukan TOPSIS. Ketika TOPSIS sejati dijalankan pada matriks yang sama, urutannya berubah: A3 SHAP Dash dan A2 IsoForest bertukar posisi. Juara tidak berubah, tetapi peringkat kedua dan ketiga pada draft bergantung pada metode yang dipakai, dan hal itu tidak terlihat karena draft tidak menulis langkah perhitungannya. Pada subbab ini kedua metode dihitung dan dibandingkan secara terbuka pada 3.4.6 dan 3.4.7.

Ketiga, draft tidak memisahkan alternatif yang sudah dieksekusi dari yang belum. Akibatnya alternatif yang belum dijalankan dapat memperoleh skor 5 pada K1 karena tampak menjanjikan. Pada subbab ini pemisahan itu dilakukan lewat rubrik C1, dan skenario P5 menguji apa yang terjadi bila penalti bukti dihapus: juara tetap A1. Artinya kemenangan A1 bukan akibat pembatasan metode, melainkan bertahan bahkan ketika alternatif yang belum dieksekusi diberi nilai lebih murah hati.

### 3.4.10 Keputusan dan tindak lanjut

Alternatif terpilih: A1 (Relabeling onset peristiwa: dari status menjadi kejadian), dengan koefisien kedekatan 0,8465 pada skenario dasar, menjadi juara pada 25 dari 25 kasus uji, dan tidak pernah turun dari peringkat satu.

| Peringkat | Alternatif | Peran yang diusulkan | Dasar |
|---|---|---|---|
| 1 | A1 Relabeling onset peristiwa: dari status menjadi kejadian | sumbu utama rancangan solusi | Mekanismenya sudah dieksekusi, memberi delta terukur positif pada kelas stuck, dan tidak menuntut parse baru sehingga C5 bernilai 100. |
| 2 | A7 Penguatan kampanye keausan alat bengkel | jalur kedua pada domain berbeda, dijalankan bila jadwal memungkinkan | Bukti terkuat pada domain bengkel dengan lead time 20 sampai 36 detik, tetapi domainnya berbeda dari rig sehingga tidak boleh menjadi klaim utama. |
| 3 | A2 Perluasan wellbore berkanal disfungsi F-10, F-4, F-12, F-15 | pendukung akuisisi bukti, dijalankan bersamaan dengan sumbu utama | Menambah wellbore dan fold layak paling banyak, sehingga memperkuat alternatif lain tanpa menjadi bentuk keluaran tersendiri. |
| 4 | A4 Unit analisis per-stand pengeboran | tidak dipilih sebagai sumbu PPT I | Nilai C1 masih 20 karena belum dieksekusi, dan C2 hanya 12 fold, sehingga kalah dari A2 yang menyentuh empat kelas; unit stand tetap menarik karena tidak menuntut data baru. |
| 5 | A8 Label fisika pengganti label proksi | tidak dipilih sebagai sumbu PPT I | Nilai C1 masih 20 karena belum dieksekusi, dan C5 bernilai 33,33 karena dua sumur masih perlu parse kanal pit dan flow. |
| 6 | A6 Formulasi survival dan sisa umur pakai | tidak dipilih sebagai sumbu PPT I | Nilai C1 masih 20 karena belum dieksekusi, dan hasil negatif hyd yaitu nol dari tiga onset membuat formulasi survival belum punya sinyal pendukung pada kelas itu. |
| 7 | A5 Prediksi severity ordinal dengan evaluasi stabilitas fold | tidak dipilih sebagai sumbu PPT I | Nilai C1 masih 20 karena belum dieksekusi, dan dua kelas sasarannya hanya memberi 9 fold layak sehingga C2 bernilai 50. |
| 8 | A3 Penjaminan mutu label dan label probabilistik multi-sumber | tidak dipilih sebagai sumbu PPT I | Nilai C1 masih 20 dan C2 hanya 9 fold, sehingga kalah sebagai alternatif tunggal, walaupun pekerjaannya tetap dituntut oleh batasan B4 sebagai prasyarat. |
| 9 | A9 Lapisan keputusan operasional: kalibrasi ambang per sumur dan purwarupa peringatan dini | tidak dipilih sebagai sumbu PPT I | Nilai C1 masih 20 dan C3 baru tingkat 60 karena rancangan kalibrasi belum diuji, walaupun A9 satu-satunya yang menyentuh langsung gejala 119,6 kali. |

Satu hal perlu dinyatakan supaya tabel di atas tidak dibaca keliru: A3 berada di peringkat delapan, tetapi batasan B4 menuntut audit mutu label dikerjakan lebih dahulu sebelum kalibrasi dan pelatihan. Karena itu peringkat delapan bukan izin melewati A3. Yang dikatakan MCDM adalah bahwa A3 tidak cukup kuat sebagai sumbu utama bila dibandingkan sebagai alternatif tunggal, bukan bahwa pekerjaannya boleh dilewati.

Satu catatan metodologis perlu disampaikan karena berkaitan dengan batas MCDM itu sendiri: matriks pada subbab ini memeringkat alternatif secara terpisah, sehingga kombinasi antaralternatif tidak dihitung. Kenyataan bahwa A1 dan A2 dapat dijalankan bersamaan, seperti terlihat pada klaster dan relasi prasyarat subbab 3.2, tidak diwakili oleh satu sel pun pada matriks. Karena itu keputusan di atas dibaca sebagai urutan prioritas, bukan sebagai larangan menjalankan alternatif lain secara paralel.

### 3.4.11 Hasil negatif dan batas yang harus dinyatakan

1. Bobot berstatus asumsi karena belum ada wawancara mitra. Yang dapat diklaim bukan bahwa bobot ini benar, melainkan bahwa keputusan tidak berubah pada sembilan skenario, enam belas uji satu per satu, dan satu sapuan penuh.
2. C8 belum tervalidasi, dan subbab 3.3.6 butir 8 menyatakan antarmuka peringatan belum dirancang. Tingkat C8 pada subbab ini adalah niat desain. Skenario P7 menolkan bobotnya dan juara tidak berubah, tetapi kriteria ini tetap tidak boleh dipakai sebagai bukti kualitas antarmuka.
3. Dua kolom tidak membedakan sama sekali, yaitu C4 dan C7, sehingga 0,3253 massa bobot tidak berperan dalam pengurutan. Keduanya tetap dipertahankan karena berfungsi sebagai saringan lulus atau gagal, dan skenario P6 membuktikan penolakan bobotnya tidak mengubah juara.
4. 7 dari 9 alternatif belum dieksekusi, sehingga nilai C1 mereka berasal dari rubrik tingkat 20, bukan dari hasil pengukuran. Bila salah satu alternatif itu dieksekusi dan gate-nya lolos, urutan dapat berubah. Ini pekerjaan terbuka yang dicatat, bukan risiko yang bisa diabaikan.
5. Jumlah minggu kerja pada C6 berstatus asumsi untuk setiap alternatif. Yang baku hanya tenggat sembilan minggu menurut Buku Pedoman PPT Tahap I Tabel 3.1 halaman 32.
6. Tidak ada angka rupiah pada perhitungan ini karena tarif rig tidak tersedia. Konsekuensinya keputusan tidak dapat dinyatakan sebagai penghematan biaya, dan klaim ROI tidak dibuat.
7. ROC adalah pendekatan bobot, bukan elisitasi. Menurut Kunsch dan Ishizaka, keunggulan ROC bergantung pada cara bobot seharusnya diperoleh, sehingga bila wawancara mitra menghasilkan rasio yang berbeda jauh, perhitungan wajib diulang dengan bobot hasil wawancara itu.
8. Portabilitas antar sumur belum terukur sesudah kalibrasi. Yang terukur baru sebaran sebelum kalibrasi, yaitu 4,15 sampai 496,09 per 24 jam (`docs/V9_PM2_VERDICT.md:114`), sehingga nilai C3 untuk A2, A8, dan A9 berstatus rubrik tingkat 60, bukan hasil uji.
9. A7 berada pada peringkat dua dengan koefisien 0,6993, tetapi berada pada domain bengkel, dengan presisi run 0,50 (`docs/V9_EVAL_C_LAYERC.md:98`) dan gate G1 nol dari empat alat (`docs/V7_R1_SOLUTIONS.md:160`). Peringkat dua itu tidak boleh dibaca sebagai kesiapan penerapan di rig.
10. Perbandingan dengan draft lama terbatas pada lima alternatif yang ada pada draft, dan dua kriteria draft tidak dapat dipetakan. Perbandingan angka mentah antara kedua dokumen tidak sah.

### 3.4.12 Manifes jejak angka (internal, bukan untuk sirkulasi eksternal)

| Angka | Nilai | Berkas, baris, atau kunci |
|---|---|---|
| Bobot ROC kriteria peringkat 1 | 0,3397 | dihitung `scratch/ppt1/build_mcdm.py` fungsi roc_weights |
| Bobot ROC kriteria peringkat 8 | 0,0156 | dihitung `scratch/ppt1/build_mcdm.py` fungsi roc_weights |
| Jumlah bobot | 1,000000000000 | `scratch/ppt1/mcdm.json` kunci bobot.jumlah |
| Koefisien kedekatan A1 | 0,8465 | `scratch/ppt1/mcdm.json` kunci topsis.sel.A1.C |
| Koefisien kedekatan A7 | 0,6993 | `scratch/ppt1/mcdm.json` kunci topsis.sel.A7.C |
| Jumlah skenario | 9 | `scratch/ppt1/mcdm.json` kunci sensitivitas.skenario |
| Jumlah uji satu per satu | 16 | `scratch/ppt1/mcdm.json` kunci sensitivitas.oat |
| Titik balik bobot C1 | 0,1050 | `scratch/ppt1/mcdm.json` kunci sensitivitas.titik_balik_C1 |
| Kendall tau TOPSIS dan SAW | 0,8889 | `scratch/ppt1/mcdm.json` kunci kendall_topsis_saw |
| Massa bobot efektif | 0,6747 | `scratch/ppt1/mcdm.json` kunci diskriminasi.massa_bobot_efektif |
| Baris draft lama yang tidak dapat direproduksi | 4 dari 5 | `scratch/ppt1/mcdm.json` kunci draft_lama.baris_tidak_reproduksi |
| Bobot draft lama | 0,25 / 0,20 / 0,15 / 0,10 / 0,15 / 0,15 | `scratch/ppt1/docx_draft_text.txt:232-237` |
| Pilihan draft lama | A1 ML Classifier dipadukan A3 SHAP | `scratch/ppt1/docx_draft_text.txt:279` |
| Slot alarm otomatis | 0 | `scratch/v9_i1/v9_i1_RESULTS.json` kunci auto_critical_alarm_slots |
| FAR vib antar sumur | 4,15 sampai 496,09 per 24 jam, rasio 119,6 kali | `docs/V9_PM2_VERDICT.md:114` |
| Stuck K-ii | B1 0,51 sampai 1,00, TLead 10 sampai 11,5 menit | `docs/V9_EVAL_B_LAYERB.md:101` |
| Hyd K-ii | 0 dari 3 onset | `docs/V9_EVAL_B_LAYERB.md:103` |
| Tool_wear K-i | TLead 20 sampai 36 detik, FP 1 sampai 3 per alat, presisi run 0,50 | `docs/V9_EVAL_C_LAYERC.md:98` |
| Gate shk, hyd, tool_wear, ssi, bit_wear, stuck | 3/7, 2/7, 0/4, 4/5, 3/4, 1/2 | `docs/V7_R1_SOLUTIONS.md:97, 127, 160, 197, 203, 66` |
| Jumlah bukti per alternatif | 3, 3, 3, 3, 3, 3, 4, 3, 4 | `scratch/ppt1/alternatif.json` kunci alternatif |
| Antarmuka peringatan belum dirancang | pernyataan 3.3.6 butir 8 | `docs/PPT1_BAB3_2.md:665` |
| Tarif rig tidak tersedia | pernyataan 3.3.6 butir 2 | `docs/PPT1_BAB3_2.md:659` |

### 3.4.13 Lampiran bukti kelas sasaran

Tabel berikut memuat angka yang menjadi jangkar rubrik C1 dan C3. Tujuannya supaya pembaca dapat memeriksa sendiri apakah tingkat 75 pada C1 memang layak, tanpa harus membuka dokumen V7 dan V9 satu per satu. 7 kelas sasaran tercatat, dan setiap baris menunjuk berkas dan nomor baris.

Tabel 3.4.12 Bukti terukur per kelas sasaran

| Kelas sasaran | Alternatif yang memakai | Lift terukur | Gate G1 dan G2 | Catatan | Jejak |
|---|---|---|---|---|---|
| stuck | A1, A2, A9 | 3,12 pada F-14 dan 0,97 pada F-9_A | G1 1 dari 2 fold, G2 1 dari 2 fold | Pada F-9_A persistence 0,787 mengalahkan Random Forest 0,651 dan canary 0,769 | docs/V7_R1_SOLUTIONS.md:66 |
| shk | A2, A4 | 1,35 / 1,24 / 1,26 / 3,36 / 0,94 / 9,79 / 2,31 | G1 3 dari 7 fold, G2 6 dari 7 fold | Tujuh fold dengan 30 sampai 760 positif per fold | docs/V7_R1_SOLUTIONS.md:97 |
| hyd | A1, A3, A6, A8 | 1,40 / 1,00 / 1,02 / 2,03 / 0,80 / 2,35 / 1,07 | G1 2 dari 7 fold, G2 4 dari 7 fold | Persistence 0,42 sampai 0,63 mengalahkan Random Forest 0,11 sampai 0,61 pada 7 dari 7 fold | docs/V7_R1_SOLUTIONS.md:127 |
| tool_wear | A7 | 1,09 / 1,39 / 1,42 / 1,30 | G1 0 dari 4 alat, G2 4 dari 4 alat | AUPRC 0,54 sampai 0,77 dengan prevalensi sekitar 0,5 sehingga plafon lift 2,0 | docs/V7_R1_SOLUTIONS.md:160 |
| ssi | A2, A4, A5 | 2,61 / 3,59 / 6,64 / 3,74 / 1,47 | G1 4 dari 5 fold, G2 5 dari 5 fold | Persistence kalah 0 dari 5 fold, dua fold underpowered dengan 3 dan 12 positif | docs/V9_PM1_ARCHITECTURE.md:186; docs/V7_R1_SOLUTIONS.md:197 |
| bit_wear | A1, A5, A6, A8 | 1,495 pada F-15S gagal tipis | G1 3 dari 4 fold, G2 4 dari 4 fold | Persistence lebih tinggi daripada Random Forest pada 4 dari 4 fold sehingga verdict turun menjadi layak bersyarat | docs/V7_R1_SOLUTIONS.md:203 |
| vib | A2, A9 | 1,61 / 2,36 / 3,50 / 1,63 | LULUS penuh pada baseline, direproduksi pada V9 | False alarm rate menyebar 4,15 sampai 496,09 per 24 jam, yaitu rasio 119,6 kali antar sumur | docs/V8_PM_VERDICT.md:155; docs/V6_PM_VERDICT.md:131; docs/V9_PM2_VERDICT.md:126, 114 |

Dua hal perlu dibaca dari tabel itu. Pertama, menurut `docs/V8_PM_VERDICT.md:155` yang mengutip `docs/V6_PM_VERDICT.md:131`, hanya dua kelas yang berstatus LULUS penuh pada baseline, yaitu vib dan ssi. Meski begitu, tingkat 100 pada C1 belum diberikan kepada alternatif mana pun, karena rubrik C1 menuntut gate lolos untuk mekanisme alternatif itu sendiri: A1 memberi delta terukur positif pada kelas stuck tetapi negatif pada kelas hyd, sedangkan A2 dan A9 yang menyentuh vib, serta A2, A4, dan A5 yang menyentuh ssi, belum menjalankan evaluasi ulang pada kelas-kelas itu. Kedua, jumlah fold berbeda jauh antar kelas, dari dua fold pada stuck sampai tujuh fold pada shk, sehingga C2 terikat pada kelas mana yang disentuh sebuah alternatif.

Reproduksi:

```bash
cd "/mnt/d/Capstone 1(v2)"
python3 scratch/ppt1/build_mcdm.py        # menulis scratch/ppt1/mcdm.json
python3 scratch/ppt1/build_doc_mcdm.py    # menulis dokumen ini dari mesin yang sama
python3 scratch/ppt1/check_mcdm.py        # memeriksa acceptance dan setiap jejak
```

Pemeriksa `check_mcdm.py` menolak dokumen bila ada angka yang berbeda dari JSON, bila rujukan berkas dan baris tidak ada atau di luar rentang, bila token penanda tidak ditemukan pada baris yang dikutip, bila jumlah skenario kurang dari delapan, dan bila terdapat em-dash atau en-dash. Pemeriksa itu sendiri diuji negatif memakai dokumen yang sengaja dirusak.

