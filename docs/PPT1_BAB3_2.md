# BAB III ANALISIS ALTERNATIF SOLUSI

## Subbab 3.2 Analisis Alternatif Solusi dan Subbab 3.3 Kriteria dan Batasan

- Acuan BoK: Buku Pedoman PPT Tahap I Tabel 2.1, empat belas IEBoK, selaras IISE ISEBoK 2021

### 3.2.1 Dasar analisis dan aturan bukti

Pedoman menuntut tiga hal pada subbab 3.2, yaitu ruang brainstorming yang tidak menilai ide pada tahap awal, analisis sembilan alternatif dengan kedalaman minimal tiga BoK dari empat belas BoK, dan peta afinitas untuk mengelompokkan ide yang mirip ke kategori yang logis (Buku Pedoman PPT Tahap I subbab 3.2, halaman 35). Dokumen ini menjawab ketiganya dengan urutan: himpunan ide tetap sembilan alternatif dari subbab 3.1, pengelompokan dilakukan pada 3.2.2 sampai 3.2.6, dan pendalaman BoK dilakukan pada 3.2.7 sampai 3.2.9.

Aturan bukti yang dipakai:

1. Setiap angka menyebut berkas dan nomor baris, kunci JSON, atau skrip yang dapat dijalankan ulang.
2. Angka yang belum dihitung ditulis eksplisit sebagai asumsi atau perkiraan desain, dan tidak disamarkan sebagai hasil pengukuran.
3. Status pelaksanaan hanya memakai tiga nilai baku yang sama dengan subbab 3.1, yaitu Selesai, Berjalan, dan Rencana (belum terealisasi).
4. Dokumen tim tidak disebut dengan kata yang menyiratkan tuduhan. Yang dilakukan adalah menelusuri asal angka dan menguatkannya.

### 3.2.2 Metode peta afinitas

1. Himpunan yang dikelompokkan adalah sembilan alternatif yang sudah berkode pada subbab 3.1. Tidak ada alternatif baru yang ditambahkan pada langkah pengelompokan, sehingga peta tidak memunculkan ide hantu.
2. Sumbu pengelompokan ditetapkan sebelum hasil dilihat, yaitu objek yang diubah pada sistem kerja: definisi target, basis bukti, formulasi model, dan titik operasi keputusan. Sumbu ini dipilih karena sembilan alternatif pada 3.1 sudah dibedakan oleh mekanisme, bukan oleh kelas disfungsi.
3. Uji keterpisahan: satu alternatif hanya boleh masuk satu klaster, ditentukan oleh mekanisme utamanya. Alternatif yang menyentuh dua klaster dicatat sebagai kasus batas dan tetap ditempatkan pada mekanisme dominannya.
4. Penamaan klaster memakai kata kerja dan objek, bukan nama bidang, supaya nama langsung menyatakan apa yang diubah.
5. Sumbu keanggotaan (anggota 1, 2, dan 3) sengaja tidak dipakai sebagai sumbu pengelompokan. Alasan terukur: bila sumbunya keanggotaan, peta hanya menyalin pembagian pada subbab 3.1 dan tidak menghasilkan informasi baru. Hasil pengelompokan menunjukkan dua dari empat klaster melintasi batas anggota, sehingga kedua peta memang berbeda.

Hasil akhirnya empat klaster, dengan sebaran tiga, dua, dua, dan dua alternatif. Dua klaster melintasi batas anggota, yaitu K1 yang memuat alternatif milik anggota 1 dan anggota 3, serta K2 yang memuat alternatif milik anggota 1 dan anggota 2. Karena itu peta ini bukan salinan pembagian tugas pada subbab 3.1, melainkan pengelompokan berdasarkan mekanisme.

### 3.2.3 Peta afinitas empat klaster

| Klaster | Nama klaster | Prinsip pengelompokan | Anggota | Masalah | BoK | Status |
| --- | --- | --- | --- | --- | --- | --- |
| K1 | Definisi target dan mutu label | Ketiga alternatif mengubah apa yang dihitung sebagai kejadian positif, atau menguji kebenaran label yang sudah ada. Tidak ada yang mengubah model dan tidak ada yang menambah data baru. | A1, A3, A8 | P1, P3, P5, P7 | 14, 11, 5, 10 | A1 Berjalan, A3 Rencana, A8 Rencana |
| K2 | Basis bukti dan unit analisis | Kedua alternatif mengubah jumlah dan satuan bukti, yaitu berapa sumur yang masuk dan satu unit analisis sama dengan apa. Definisi label dan bentuk model tidak diubah. | A2, A4 | P2, P6 | 5, 7, 11, 14 | A2 Berjalan, A4 Rencana |
| K3 | Formulasi model dan evaluasi | Kedua alternatif mempertahankan himpunan data dan label, lalu mengubah bentuk hipotesis dan cara evaluasinya. Gate biner tetap dihitung pada ambang yang sama. | A5, A6 | P6, P7, P9, P3 | 2, 3, 5, 11 | A5 Rencana, A6 Rencana |
| K4 | Sinyal fisik dan titik operasi keputusan | Kedua alternatif bekerja pada sinyal dan pada titik tempat keluaran menyala, yaitu ambang, kalibrasi, purwarupa peringatan, dan urutan prioritas. Definisi label global tidak diubah. | A7, A9 | P8, P1, P4 | 1, 3, 5, 6, 12, 14 | A7 Berjalan, A9 Rencana |

Tabel di atas memuat seluruh sembilan alternatif tepat satu kali. Pemeriksaan otomatis pada menolak dokumen ini bila ada alternatif yang tidak masuk klaster atau masuk lebih dari satu klaster.

### 3.2.4 Rincian setiap klaster

#### 3.2.4.1 K1 Definisi target dan mutu label

**Prinsip pengelompokan.** Ketiga alternatif mengubah apa yang dihitung sebagai kejadian positif, atau menguji kebenaran label yang sudah ada. Tidak ada yang mengubah model dan tidak ada yang menambah data baru.

**Anggota dan mekanisme.**

- A1 Relabeling onset peristiwa: dari status menjadi kejadian. Memindahkan definisi target dari status yang bertahan menjadi titik masuk peristiwa, lalu membuang jendela di dalam blok setelah onset.
- A3 Penjaminan mutu label dan label probabilistik multi-sumber. Mengaudit semantik label lebih dahulu, mengunci satu varian onset, lalu menambah sumbu bukti melalui label multi-sumber bila noise antar sumber masih besar.
- A8 Label fisika pengganti label proksi. Mengganti sumber label dari ambang statistik menjadi mekanisme fisika, yaitu perubahan volume pit dan selisih laju alir untuk hidrolik, serta rasio energi spesifik untuk keausan bit.

**Yang menyatukan.** Ketiganya menyerang akar yang sama, yaitu label berbentuk blok status. Persistence menang atas model karena label bertahan panjang, bukan karena fitur lemah.

**Yang membedakan.** A1 mengubah bentuk target. A3 mengubah tingkat kepercayaan label. A8 mengubah asal label. Ketiganya dapat dijalankan bersama, tetapi masing-masing cukup untuk menguji hipotesis yang berbeda.

**Angka penentu.**

| Keterangan | Nilai |
| --- | --- |
| B1 dan TLead stuck K-ii setelah label onset | B1 0,51 sampai 1,00 dan TLead 10 sampai 11,5 menit pada titik operasi 0,05 |
| Hasil negatif label onset pada hyd | 0 dari 3 onset terdeteksi, TLead nol |
| Kontrol-positif label stuck | 0 dari 10 |
| Kanal sumber label fisika | GAINLOSSTOT 575 dan 517 berkas, PITTOT 565 dan 506, FLOWOUT 688, FLOWOUTPC 949 |
| Basis label kurasi | 884 kejadian, 50 relevan BHA, total durasi 73.500 menit atau 1.225 jam |

**Relasi dengan klaster lain.**

- Keluar ke K4 dengan jenis prasyarat. Kalibrasi ambang menyetel keluaran terhadap kebenaran lab
- Keluar ke K3 dengan jenis prasyarat. Skala severitas 0 sampai 3 dan label waktu han
- Masuk dari K2. Sumur baru memasok jumlah posi

**Risiko bila klaster dipilih sendirian.** Bila klaster ini dipilih sendirian, label menjadi benar tetapi tidak ada titik operasi yang dipakai, sehingga tidak ada keluaran yang bisa dipakai di rig. Perbaikan label tanpa kalibrasi hanya memperbaiki angka evaluasi.

**Status agregat.** A1 Berjalan, A3 Rencana, A8 Rencana.

#### 3.2.4.2 K2 Basis bukti dan unit analisis

**Prinsip pengelompokan.** Kedua alternatif mengubah jumlah dan satuan bukti, yaitu berapa sumur yang masuk dan satu unit analisis sama dengan apa. Definisi label dan bentuk model tidak diubah.

**Anggota dan mekanisme.**

- A2 Perluasan wellbore berkanal disfungsi (F-10, F-4, F-12, F-15). Memparse empat wellbore yang terbukti memiliki kanal disfungsi, lalu menggabungkannya ke kampanye leave-one-well-out sehingga jumlah fold dan jumlah positif naik.
- A4 Unit analisis per-stand pengeboran. Mengganti unit jendela waktu dengan unit stand pengeboran, sehingga prevalensi naik tetapi horizon prediksi melebar menjadi stand berikutnya.

**Yang menyatukan.** Keduanya menyerang underpowering dengan mengubah himpunan atau agregasi sampel, bukan dengan mengubah model atau menurunkan ambang.

**Yang membedakan.** A2 menambah observasi independen berupa sumur baru. A4 mengubah resolusi dengan menggabungkan jendela menjadi stand. A2 menaikkan jumlah positif tanpa mengubah arti gate, sedangkan A4 menaikkan prevalensi sekaligus mengubah arti gate.

**Angka penentu.**

| Keterangan | Nilai |
| --- | --- |
| Kanal disfungsi pada empat wellbore yang belum diparse | F-10 SHKRSK_RT 188, CRPM_RT 186, STKSLP 125, VIBLAT_RT 66, STUCK_RT 18; F-4 135/135/135/86; F-12 91/90/52/6; F-15 77/76/76/76 |
| Baris CRPM hasil parse | 281.030 / 42.010 / 178.430 / 57.846 baris, re-run 11 fold belum dijalankan |
| Fold underpowered yang diserang | F-7 tiga positif, F-9 dua belas positif, F-9_A lift 1,47 gagal tipis |
| Prevalensi unit stand | 10 sampai 40 persen, berstatus perkiraan desain dan belum dihitung |
| Batas stand tanpa akuisisi baru | Dapat diturunkan dari BPOS dan celah waktu pada CSV yang sudah ada |

**Relasi dengan klaster lain.**

- Keluar ke K1 dengan jenis penyuplai bukti. Sumur baru memasok jumlah posi
- Keluar ke K3 dengan jenis penyuplai bukti. Jumlah positif per fold menentukan lebar selang kepercayaan, sehingga menent

**Risiko bila klaster dipilih sendirian.** A2 sudah menghasilkan baris data terukur tetapi dampaknya terhadap gate belum terukur karena re-run fold belum dijalankan. A4 berisiko mengubah arti gate secara diam-diam, karena horizon prediksi melebar dari sepuluh menit menjadi stand berikutnya.

**Status agregat.** A2 Berjalan, A4 Rencana.

#### 3.2.4.3 K3 Formulasi model dan evaluasi

**Prinsip pengelompokan.** Kedua alternatif mempertahankan himpunan data dan label, lalu mengubah bentuk hipotesis dan cara evaluasinya. Gate biner tetap dihitung pada ambang yang sama.

**Anggota dan mekanisme.**

- A5 Prediksi severity ordinal dengan evaluasi stabilitas fold. Melatih model pada skala severitas 0 sampai 3, menurunkan keputusan biner pada ambang minimal 1, lalu menambah evaluasi stabilitas fold berupa stratified bootstrap dan pelaporan jumlah positif.
- A6 Formulasi survival dan sisa umur pakai (time-to-event). Memodelkan waktu sampai peristiwa dengan hazard proporsional, sehingga keluaran berupa risiko per horizon dan sisa umur pakai.

**Yang menyatukan.** Keduanya tidak menyentuh data dan tidak menyentuh label. Yang berubah adalah bentuk keluaran dan cara menguji kestabilannya.

**Yang membedakan.** A5 menambah informasi dari label yang sudah ada, yaitu skala severitas, dan menambah rigor evaluasi. A6 mengubah target menjadi waktu, tetapi tidak menambah informasi baru.

**Angka penentu.**

| Keterangan | Nilai |
| --- | --- |
| Kinerja ssi dan dua fold underpowered | G1 4 dari 5, G2 5 dari 5, persistence 0 dari 5, F-7 tiga positif, F-9 dua belas positif |
| Posisi survival menurut penulis solusi | Mengubah formulasi tanpa menambah informasi, sehingga diposisikan sebagai opsi pembanding dan bukan solusi primer |
| Berkas bhaRun tanpa label keausan fisik | 77 berkas tanpa dullingInfo, dullGrade, maupun bitName |
| Klasifikasi severitas stick-slip sudah mapan | Sitasi Hegde 2019, doi 10.1016/j.petrol.2019.05.021 |
| Ambang underpowered | Fold dengan kurang dari 30 positif dilabeli UNDERPOWERED dan tidak dihitung sebagai mayoritas |

**Relasi dengan klaster lain.**

- Masuk dari K2. Jumlah positif per fold menentukan lebar selang kepercayaan, sehingga menent
- Masuk dari K1. Skala severitas 0 sampai 3 dan label waktu han

**Risiko bila klaster dipilih sendirian.** A6 berisiko menjadi pengulangan berbiaya, karena mengubah formulasi tanpa menambah informasi. A5 tidak menambah kelas, sehingga tidak dapat menggantikan A1 atau A2 sebagai perbaikan akar.

**Status agregat.** A5 Rencana, A6 Rencana.

#### 3.2.4.4 K4 Sinyal fisik dan titik operasi keputusan

**Prinsip pengelompokan.** Kedua alternatif bekerja pada sinyal dan pada titik tempat keluaran menyala, yaitu ambang, kalibrasi, purwarupa peringatan, dan urutan prioritas. Definisi label global tidak diubah.

**Anggota dan mekanisme.**

- A7 Penguatan kampanye keausan alat bengkel: progresi, dekomposisi mode, dan ranking. Mendeteksi titik perubahan pada sinyal keausan alat bengkel, menambah fitur dekomposisi mode, dan menyiapkan ranking antar status sebagai cadangan bila validasi titik ubah gagal.
- A9 Lapisan keputusan operasional: kalibrasi ambang per sumur dan purwarupa peringatan dini. Mengkalibrasi ambang per sumur, menjalankan purwarupa peringatan dini pada data berlabel, dan menyusun indeks kondisi untuk disfungsi yang labelnya belum tersedia.

**Yang menyatukan.** Keduanya menghasilkan keputusan pada tingkat sinyal, dan keduanya diukur dengan anggaran alarm, bukan dengan AUPRC saja.

**Yang membedakan.** Domain berbeda, yaitu bengkel alat pada A7 dan rig pada A9. Status eksekusi juga berbeda, karena A7 sudah memiliki kalibrasi alarm terukur sedangkan A9 belum.

**Angka penentu.**

| Keterangan | Nilai |
| --- | --- |
| Deteksi titik ubah alat bengkel | 4 dari 4 alat, TLead 20 sampai 36 detik atau 1,8 kali, presisi run 0,50 |
| False alarm terkalibrasi per alat | 1 sampai 3 per alat |
| Baseline ranking lintas alat | AUPRC 0,516 sampai 0,612 atau 1,19 kali, engine Random Forest belum dijalankan |
| Sebaran false alarm antar sumur pada ambang global | 4,15 sampai 496,09 per 24 jam, rasio 119,6 kali |
| Kanal permukaan frekuensi tinggi yang tersedia | TSPP 52.905 baris pada empat berkas |
| Kelayakan pemantauan menurut ambang operator | FAR maksimal 6 per 24 jam, setara satu pemeriksaan driller per empat jam |
| Keluaran screening shk saat ini | FAR 18 sampai 63 per 24 jam pada titik operasi 0,05 sampai 0,10, presisi 0,00 sampai 0,12 |

**Kasus batas.** A7 menyentuh dua klaster. Mekanisme label progresi di dalam A7 membentuk label dari titik ubah, sehingga ia juga menyentuh K1. Penempatan pada K4 memakai mekanisme dominan, yaitu titik operasi dan anggaran alarm, dan hubungan silang ini dinyatakan terbuka, bukan disembunyikan.

**Relasi dengan klaster lain.**

- Masuk dari K1. Kalibrasi ambang menyetel keluaran terhadap kebenaran lab

**Risiko bila klaster dipilih sendirian.** Bila dipilih sebelum label dibereskan, klaster ini menghasilkan alarm yang rapi secara statistik tetapi menunjuk peristiwa yang salah. Bukti pendukungnya sudah ada pada tingkat label, yaitu kontrol-positif 0 dari 10.

**Status agregat.** A7 Berjalan, A9 Rencana.

### 3.2.5 Silang klaster dengan masalah, BoK, dan lapisan intervensi

**Cakupan masalah.**

| Masalah | K1 | K2 | K3 | K4 | Jumlah klaster |
| --- | --- | --- | --- | --- | --- |
| P1 | ya | - | - | ya | 2 |
| P2 | - | ya | - | - | 1 |
| P3 | ya | - | ya | - | 2 |
| P4 | - | - | - | ya | 1 |
| P5 | ya | - | - | - | 1 |
| P6 | - | ya | ya | - | 2 |
| P7 | ya | - | ya | - | 2 |
| P8 | - | - | - | ya | 1 |
| P9 | - | - | ya | - | 1 |

Sembilan masalah P1 sampai P9 seluruhnya tercakup oleh empat klaster, yaitu 9 masalah. Tidak ada masalah pada subbab 3.1 yang kehilangan rumah, dan tidak ada klaster yang tidak menyentuh masalah.

**Cakupan BoK per klaster.**

| Klaster | BoK 1 | BoK 2 | BoK 3 | BoK 4 | BoK 5 | BoK 6 | BoK 7 | BoK 8 | BoK 9 | BoK 10 | BoK 11 | BoK 12 | BoK 13 | BoK 14 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| K1 | - | - | - | - | ya | - | - | - | - | ya | ya | - | - | ya |
| K2 | - | - | - | - | ya | - | ya | - | - | - | ya | - | - | ya |
| K3 | - | ya | ya | - | ya | - | - | - | - | - | ya | - | - | - |
| K4 | ya | - | ya | - | ya | ya | - | - | - | - | - | ya | - | ya |

Sepuluh dari empat belas BoK tersentuh, yaitu 10 BoK. Empat BoK yang belum tersentuh dibahas pada 3.2.9.

**Lapisan intervensi.** Lapisan memakai pembagian yang sama dengan subbab 3.1, supaya pembacaan tetap konsisten.

| Lapisan | Nama lapisan | Klaster | Anggota lapisan |
| --- | --- | --- | --- |
| L1 | Data dan label | K1, K2 | A1, A3, A8, A2, A4 |
| L2 | Formulasi model dan evaluasi | K2, K3 | A2, A4, A5, A6 |
| L3 | Sinyal fisik dan operasi | K4 | A7, A9 |

K1 seluruhnya berada pada lapisan data dan label. K3 seluruhnya berada pada lapisan formulasi model. K2 menyentuh dua lapisan, yaitu data dan formulasi, karena basis bukti memengaruhi himpunan sumur sekaligus agregasi fitur. K4 berada pada lapisan sinyal fisik dan operasi. Lapisan bukan sumbu pengelompokan, sehingga dua klaster boleh berada pada lapisan yang sama. Yang membedakan klaster adalah objek yang diubah, bukan lapisannya. Karena itu peta afinitas ini tidak dapat disamakan dengan pembagian anggota pada subbab 3.1.

### 3.2.6 Struktur klaster untuk diagram G1

Bagian ini adalah serahan untuk kartu diagram, supaya gambar tidak mengarang isi. Seluruh nilainya juga tersedia sebagai JSON pada dengan kunci `g1`.

Kanvas: A4 landscape, 11,69 kali 8,27 inci, 200 dpi.

**Node klaster.**

| Id | Label | Warna | Anggota | Teks ringkas | Posisi x | Posisi y |
| --- | --- | --- | --- | --- | --- | --- |
| K1 | Target dan mutu label | #2563eb | A1, A3, A8 | Mengubah apa yang dihitung sebagai kejadian atau menguji kebenaran label | 0.5 | 3.2 |
| K2 | Basis bukti dan unit analisis | #059669 | A2, A4 | Mengubah jumlah sumur dan satuan unit analisis | 6.3 | 3.2 |
| K3 | Formulasi model dan evaluasi | #7c3aed | A5, A6 | Mengubah bentuk hipotesis dan rigor evaluasi | 0.5 | 6.6 |
| K4 | Sinyal fisik dan titik operasi | #b45309 | A7, A9 | Mengubah ambang, kalibrasi, dan urutan prioritas | 6.3 | 6.6 |

**Node alternatif.**

| Id | Label pendek | Klaster | Status |
| --- | --- | --- | --- |
| A1 | Onset peristiwa | K1 | Berjalan |
| A3 | Audit mutu label | K1 | Rencana |
| A8 | Label fisika | K1 | Rencana |
| A2 | Perluasan sumur | K2 | Berjalan |
| A4 | Unit per stand | K2 | Rencana |
| A5 | Severity ordinal | K3 | Rencana |
| A6 | Survival dan RUL | K3 | Rencana |
| A7 | Keausan alat bengkel | K4 | Berjalan |
| A9 | Ambang per sumur | K4 | Rencana |

**Edge antar klaster.**

| Dari | Ke | Label | Gaya garis |
| --- | --- | --- | --- |
| K1 | K4 | prasyarat label sebelum kalibrasi | putus-putus |
| K2 | K1 | penyuplai positif | putus-putus |
| K2 | K3 | penyuplai positif per fold | putus-putus |
| K1 | K3 | semantik label sebelum skala | putus-putus |

**Legenda.**

- kotak berwarna: klaster, warna berbeda per klaster
- kotak kecil di dalam klaster: alternatif solusi beserta kode A1 sampai A9
- teks Berjalan: mekanisme inti sudah dieksekusi dan berangka pada kampanye V9
- teks Rencana: belum ada artefak eksekusi
- panah putus-putus: relasi prasyarat atau penyuplai bukti antar klaster

**Penanda kasus batas.** A7 menyentuh K1 lewat label progresi. Penanda ditulis sebagai catatan kecil pada kotak A7, bukan sebagai klaster kelima.

**Catatan desain.** Empat kolom klaster, sembilan kotak alternatif di dalam kolomnya, dan empat panah putus-putus untuk relasi. Status ditulis sebagai teks karena dokumen ini tidak memakai emoji. Warna klaster mengikuti palet yang sama dengan dokumen, yaitu biru, hijau, ungu, dan jingga.

### 3.2.7 Pendalaman BoK

Empat BoK didalami, bukan sepuluh. Alasannya: BoK 14 dan BoK 3 wajib muncul karena pedoman menetapkan rantai BoK dimulai dari BoK 14 dan berakhir pada BoK 3, sedangkan BoK 5 dan BoK 11 dipilih karena frekuensi pemakaiannya paling tinggi pada sembilan alternatif. Empat BoK yang didalami ini masing-masing membawa peran, keputusan, standar, angka, dan batas. BoK lain yang hanya muncul sekali dicatat pada 3.2.8 dan tidak dipaksakan menjadi pendalaman semu.

| BoK | Nama | Peran satu baris | Jumlah alternatif | Status pendalaman |
| --- | --- | --- | --- | --- |
| 14 | Systems Design & Engineering | Menetapkan batas sistem, fungsi yang diprediksi, dan arsitektur keputusan sebelum satu alternatif pun dipilih. | 4 | didalami |
| 11 | Information Engineering | Mengelola rantai data menjadi label menjadi fitur menjadi keluaran informasi, dan menetapkan bahwa akurasi sistem informasi diukur dari kebenaran label, bukan hanya dari metrik model. | 6 | didalami |
| 5 | Quality & Reliability Engineering | Menetapkan metrik, baseline pembanding, dan aturan pengujian yang dikunci sebelum eksekusi, lalu melaporkan hasil negatif tanpa menghapusnya. | 8 | didalami |
| 3 | Engineering Economic Analysis | Menerjemahkan keluaran teknis menjadi biaya dan manfaat, dan menetapkan bahwa ambang kelayakan alarm adalah keputusan ekonomi, bukan hanya keputusan statistik. | 2 | didalami |

#### 3.2.7.1 BoK 14 Systems Design & Engineering

**Peran konkret dalam solusi.** Menetapkan batas sistem, fungsi yang diprediksi, dan arsitektur keputusan sebelum satu alternatif pun dipilih. BoK ini yang memutuskan bahwa objek prediksi dipisah menjadi pertanyaan apakah sedang terjadi dan apakah akan terjadi, sehingga tujuh kelas kerusakan menjadi sebelas klaim, dan setiap klaim dijawab oleh beberapa varian sampai total dua puluh tujuh head.

**Keputusan yang diambil melalui BoK ini.**

- Batas sistem: data rig Volve dan data bengkel alat masuk ke dalam batas. Aktuasi, yaitu menutup blowout preventer atau mengubah beban bit secara otomatis, berada di luar batas, karena PPT I merancang sistem informasi keputusan dan bukan sistem kendali proses.
- Fungsi: tujuh detektor, sebelas klaim, dua puluh tujuh head, dengan hubungan 7 bagian dari 11 bagian dari 27, sehingga penjumlahan ketiganya dinyatakan salah kategori.
- Integrasi: dua puluh tujuh head dipetakan ke empat lapisan keputusan L0 lima, L1 sebelas, L2 sembilan, L3 dua, dengan penanda wajib review manusia pada tiga belas head.

**Standar dan metrik acuan.**

- Buku Pedoman PPT Tahap I subbab 2.5, solusi terintegrasi yang mempertimbangkan people, material, information, equipment, dan energy.
- Buku Pedoman PPT Tahap I Tabel 2.2 tahap Integrate, purwarupa untuk mengklarifikasi integrasi antar elemen.
- IABEE Criteria Guide, kewajiban memakai standar keteknikan dan multiple realistic constraints.

**Angka penentu.**

| Keterangan | Nilai |
| --- | --- |
| Tiga angka pengikat alat | 7 mode, 11 klaim, 27 head |
| Lapisan keputusan L0 sampai L3 | 5 / 11 / 9 / 2 sama dengan 27 |
| Head dengan review manusia wajib | 13 dari 27 |
| Head yang berstatus belum layak pakai | 2 dari 27 |
| Sumber terpetakan tepat satu kali | 22 sumber ke 9 alternatif, nol duplikat |

**Alternatif yang memakai BoK ini.** Seluruh alternatif A1 sampai A9 memakai BoK ini. Beban terberat ada pada A1 yang mendefinisikan ulang target, dan pada A2 serta A7 yang harus mengintegrasikan domain berbeda ke satu protokol evaluasi.

**Kegagalan yang terjadi bila BoK ini diabaikan.** Tanpa BoK 14, sembilan alternatif saling tumpang tindih karena tidak ada yang menetapkan batas. Contoh terukur: tanpa pemisahan deteksi status dan prediksi onset, hasil stuck K-ii dengan B1 0,51 sampai 1,00 akan dilaporkan sebagai kinerja deteksi status, padahal tugas, label, dan baseline kedua tugas itu berbeda.

**Batas pendalaman.** BoK 14 tidak menghasilkan angka kinerja. Verifikasinya berupa konsistensi, yaitu nol sumber terpakai ganda dan nol klaim di luar batas sistem, bukan berupa metrik.

#### 3.2.7.2 BoK 11 Information Engineering

**Peran konkret dalam solusi.** Mengelola rantai data menjadi label menjadi fitur menjadi keluaran informasi, dan menetapkan bahwa akurasi sistem informasi diukur dari kebenaran label, bukan hanya dari metrik model.

**Keputusan yang diambil melalui BoK ini.**

- Kelengkapan bukti: empat wellbore berkanal disfungsi diparse karena kanal sumbernya terdaftar, yaitu F-10, F-4, F-12, dan F-15.
- Volume yang dipakai: TSPP 52.905 baris pada empat berkas sebagai kanal permukaan frekuensi tinggi, dan CRPM hasil parse 281.030, 42.010, 178.430, serta 57.846 baris.
- Kebenaran label: kontrol-positif stuck 0 dari 10, sehingga akurasi keluaran belum sah meskipun AUPRC tinggi. Ini keputusan rekayasa informasi, bukan keputusan statistik.
- Kerahasiaan: seluruh angka berasal dari lapangan Volve yang terbuka dan empat set data eksternal, sehingga tidak ada telemetri mitra yang perlu disalin ke repositori.

**Standar dan metrik acuan.**

- ISO keamanan informasi, diterapkan sebagai kendali akses dan minimalisasi data, bukan sebagai sertifikasi.
- Prinsip minimalisasi data ala GDPR, diterapkan terbatas karena data sumur tidak memuat data pribadi. Klaim kepatuhan GDPR penuh tidak dibuat.
- Standar Web W3C, dicatat belum relevan karena antarmuka pengguna belum dibangun pada PPT I.
- System response time dan downtime, dicatat belum diukur sehingga tidak boleh diklaim.
- Accuracy, diterjemahkan sebagai kebenaran label dan kelengkapan kanal, bukan sebagai akurasi model.

**Angka penentu.**

| Keterangan | Nilai |
| --- | --- |
| Baris CRPM hasil parse empat wellbore | 281.030 / 42.010 / 178.430 / 57.846 baris |
| Volume TSPP | 52.905 baris pada empat berkas |
| Basis label kurasi | 884 kejadian, 50 relevan BHA, 73.500 menit atau 1.225 jam |
| Kontrol-positif label stuck | 0 dari 10 |
| Sumber data keseluruhan | Lapangan Volve terbuka dan empat set data eksternal terverifikasi |
| Batas muktamad cakupan data | Satu lapangan, domain bengkel berbeda dari rig, label hyd K-ii masih proksi |

**Alternatif yang memakai BoK ini.** A1, A2, A3, A4, A5, dan A8 memakai BoK ini. A2 adalah pekerjaan akuisisi dan pengelolaan data. A3 adalah audit kebenaran label. A8 adalah penurunan label dari kanal fisika. A1, A4, dan A5 memakainya karena setiap perubahan label atau agregasi mengubah keluaran informasi.

**Kegagalan yang terjadi bila BoK ini diabaikan.** Tanpa BoK 11, label diperlakukan sebagai kebenaran yang diberikan. Akibatnya urutan kerja 6a dan 6b terbalik, yaitu kalibrasi ambang dijalankan sebelum audit label, dan hasilnya presisi palsu.

**Batas pendalaman.** Empat wellbore sudah diparse tetapi belum dievaluasi ulang, sehingga dampaknya terhadap gate belum terukur. System response time dan downtime belum diukur sama sekali.

#### 3.2.7.3 BoK 5 Quality & Reliability Engineering

**Peran konkret dalam solusi.** Menetapkan metrik, baseline pembanding, dan aturan pengujian yang dikunci sebelum eksekusi, lalu melaporkan hasil negatif tanpa menghapusnya.

**Keputusan yang diambil melalui BoK ini.**

- Gate G1 dengan lift minimal 1,5 pada mayoritas sumur dan gate G2 dengan AUPRC minimal AUPRC canary dikunci. Alternatif hanya boleh mengubah label, data, formulasi, atau titik operasi, dan tidak boleh menggeser gate.
- Baseline wajib sesuai tugas: persistence untuk label temporal, prevalence-random untuk onset langka, dan canary untuk klaim yang berpotensi menghafal. Fold dengan kurang dari 30 positif dilabeli UNDERPOWERED dan tidak dihitung sebagai mayoritas.
- Metrik operasional memakai false alarm rate per 24 jam, dengan ambang kelayakan pemantauan 6 per 24 jam yang setara satu pemeriksaan driller per empat jam.

**Standar dan metrik acuan.**

- Standar kualitas ISO dan process capability, diterjemahkan sebagai kestabilan kinerja antar fold dan antar sumur.
- Defects probability, diterjemahkan sebagai prevalensi peristiwa dan plafon lift satu dibagi prevalensi.
- System reliability, diterjemahkan sebagai metrik deteksi kegagalan, yaitu B1, TLead, AUPRC, lift, dan false alarm rate.
- Failure analysis, diterjemahkan sebagai kontrol-positif dan pelaporan hasil negatif.

**Angka penentu.**

| Keterangan | Nilai |
| --- | --- |
| Gate shk | G1 3 dari 7, G2 6 dari 7 |
| Gate hyd | G1 2 dari 7, G2 4 dari 7, persistence menang pada 7 dari 7 fold |
| Gate tool_wear | G1 0 dari 4, G2 4 dari 4 |
| Gate ssi | G1 4 dari 5, G2 5 dari 5, F-7 tiga positif, F-9 dua belas positif |
| Gate bit_wear | G1 3 dari 4, G2 4 dari 4, persistence menang pada 4 dari 4 fold |
| Stuck K-ii pada titik operasi 0,05 | B1 0,51 sampai 1,00, TLead 10 sampai 11,5 menit |
| Hyd K-ii | 0 dari 3 onset, TLead nol |
| Tool_wear K-i | 4 dari 4 alat, TLead 20 sampai 36 detik, false positive 1 sampai 3 per alat |
| Sebaran false alarm antar sumur | 4,15 sampai 496,09 per 24 jam, rasio 119,6 kali |

**Alternatif yang memakai BoK ini.** Seluruh sembilan alternatif memakai BoK ini, karena gate dan baseline berlaku untuk semua. Beban terberat ada pada A5 yang menambah rigor evaluasi, dan pada A9 yang harus mengukur false alarm setelah kalibrasi.

**Kegagalan yang terjadi bila BoK ini diabaikan.** Tanpa BoK 5, alternatif dinilai dari satu fold yang bagus. Contoh terukur: bit_wear lolos G1 3 dari 4 dan G2 4 dari 4, tetapi persistence mengalahkan Random Forest pada 4 dari 4 fold, sehingga hanya aturan pra-registrasi yang menurunkan verdict menjadi layak bersyarat.

**Batas pendalaman.** Gate dihitung per jendela waktu. Bila unit berubah menjadi stand pada A4, false alarm rate wajib dihitung ulang per stand dan diberikan justifikasinya, karena gate lama tidak dapat dibandingkan langsung.

#### 3.2.7.4 BoK 3 Engineering Economic Analysis

**Peran konkret dalam solusi.** Menerjemahkan keluaran teknis menjadi biaya dan manfaat, dan menetapkan bahwa ambang kelayakan alarm adalah keputusan ekonomi, bukan hanya keputusan statistik.

**Keputusan yang diambil melalui BoK ini.**

- Beban pemeriksaan dijadikan batas kelayakan: false alarm rate maksimal 6 per 24 jam dipakai sebagai ambang pemantauan karena setara satu pemeriksaan driller per empat jam.
- Basis kerugian memakai 884 kejadian dengan total durasi 73.500 menit atau 1.225 jam, dan 50 kejadian di antaranya terverifikasi relevan BHA. Kalimat yang benar adalah durasi kejadian operasi, bukan seluruhnya kehilangan akibat kegagalan.
- Keputusan penarikan bit pada A6 dinilai sebagai trade-off biaya, dengan label yang tersedia hanya batas run, karena 77 berkas bhaRun tidak memuat dullingInfo, dullGrade, maupun bitName.

**Standar dan metrik acuan.**

- Benefit Cost Ratio, dipakai sebagai kerangka membandingkan manfaat pengurangan kejadian dengan biaya implementasi.
- Payback Period, dipakai sebagai kerangka menilai jarak waktu sampai manfaat menutup biaya.
- Cost Efficiency pada BoK 7, dipakai sebagai kerangka membandingkan jumlah pemeriksaan per satuan waktu.

**Angka penentu.**

| Keterangan | Nilai |
| --- | --- |
| Basis durasi kejadian | 884 kejadian, 73.500 menit atau 1.225 jam |
| Peringatan kalimat yang benar | 884 kejadian operasi, 50 relevan BHA, bukan 884 kejadian kerusakan |
| Ambang kelayakan pemantauan | FAR maksimal 6 per 24 jam, setara satu pemeriksaan per empat jam |
| Berkas bhaRun tanpa label keausan | 77 berkas tanpa dullingInfo, dullGrade, dan bitName |
| Posisi survival menurut penulis solusi | Mengubah formulasi tanpa menambah informasi |

**Alternatif yang memakai BoK ini.** A6 memakai BoK ini secara langsung karena keputusan penarikan bit adalah keputusan biaya. A9 memakainya untuk menilai biaya false alarm dan penghematan rig time. A7 memakainya untuk memutuskan kapan penggantian alat bengkel layak.

**Kegagalan yang terjadi bila BoK ini diabaikan.** Tanpa BoK 3, alternatif dipilih karena paling canggih. Contoh terukur: A6 menambah formulasi tanpa menambah informasi, sehingga biaya naik tanpa manfaat yang dapat ditunjukkan.

**Batas pendalaman.** Tarif rig per jam tidak tersedia pada seluruh tiga belas dataset dan tidak ada pada dokumen keuangan mana pun di proyek ini. Karena itu nilai rupiah pada 3.4 adalah asumsi: isinya adalah tarif dan kalangan biaya; dasarnya adalah angka dari publikasi luas karena tidak ada dokumen keuangan proyek; alasannya dipakai adalah agar ranking biaya dapat dibandingkan dengan manfaat; ujinya adalah analisis sensitivitas pada 3.4 yang menggeser tarif dan memeriksa apakah urutan ranking berubah.

### 3.2.8 Cakupan BoK terhadap alternatif

| BoK | Nama | Jumlah alternatif | Alternatif |
| --- | --- | --- | --- |
| 1 | Work Design & Measurement | 1 | A9 |
| 2 | Operations Research & Analysis | 2 | A5, A6 |
| 3 | Engineering Economic Analysis | 2 | A6, A9 |
| 4 | Facilities Engineering & Energy Management | 0 | |
| 5 | Quality & Reliability Engineering | 8 | A1, A2, A3, A4, A5, A6, A7, A8 |
| 6 | Ergonomics & Human Factors | 1 | A9 |
| 7 | Operations Engineering & Management | 1 | A4 |
| 8 | Supply Chain Management | 0 | |
| 9 | Engineering Management | 0 | |
| 10 | Safety | 1 | A8 |
| 11 | Information Engineering | 6 | A1, A2, A3, A4, A5, A8 |
| 12 | Design & Manufacturing Engineering | 1 | A7 |
| 13 | Product Design & Development | 0 | |
| 14 | Systems Design & Engineering | 4 | A1, A2, A3, A7 |

Rubrik penilaian memuat frasa bahwa alternatif solusi minimal tiga per BoK yang berbeda. Bila frasa itu ditafsirkan sebagai tiga alternatif untuk setiap BoK yang disebut, maka BoK 1, BoK 6, BoK 7, BoK 10, dan BoK 12 belum memenuhi, karena masing-masing hanya dimuat oleh satu alternatif. Dua jalan keluar yang tersedia: pertama, mempersempit daftar BoK yang diklaim sehingga setiap BoK yang diklaim memuat minimal tiga alternatif; kedua, menambah mekanisme pada alternatif yang sudah ada, bukan menciptakan alternatif baru yang tidak berasal dari inventaris solusi subbab 3.1. Keputusan ini diserahkan kepada pembimbing, dan dicatat sebagai risiko penilaian pada 3.3.6.

### 3.2.9 BoK yang belum disentuh dan alasan tidak dipaksakan

| BoK | Nama | Alasan belum disentuh | Kandidat pengaitan | Rekomendasi |
| --- | --- | --- | --- | --- |
| 4 | Facilities Engineering & Energy Management | Menuntut data tata letak rig atau bengkel, aliran material di lantai kerja, dan konsumsi energi. Tiga hal itu tidak ada pada tiga belas dataset yang diinventaris, sehingga pengaitan akan berupa definisi tanpa peran. | Tata letak area bengkel alat pada A7, bila foto atau denah bengkel tersedia dari mitra. | Dibiarkan terbuka. Jangan dipaksakan sampai ada data denah yang dapat dijejak. |
| 8 | Supply Chain Management | Menuntut data persediaan bit dan alat, waktu pengadaan, dan hubungan pemasok. Tidak ada satu pun dari ketiganya di proyek ini. | Kebijakan penggantian bit pada A6, bila mitra memberi data persediaan dan waktu pengiriman. | Dibiarkan terbuka. Ini BoK yang paling lemah untuk dipaksakan karena nol data pendukung. |
| 9 | Engineering Management | Sebenarnya ada bahan nyata, yaitu jadwal satu semester pada Tabel 3.1, pembagian tiga anggota, dan gate pra-registrasi. Yang belum ada adalah artefak manajemen proyek formal seperti register risiko dan jadwal rinci berbasis tonggak. | Register risiko proyek dan jadwal tonggak sebagai artefak pendukung, bukan sebagai alternatif solusi baru. | Kandidat paling jujur bila mentor menuntut BoK tambahan. Tambahkan hanya bersama artefaknya, yaitu register risiko dan jadwal tonggak, supaya tidak menjadi dekorasi. |
| 13 | Product Design & Development | Relevan untuk desain antarmuka peringatan pada A9, tetapi antarmuka belum dirancang dan belum ada purwarupa tampilan. Tanpa itu, BoK ini hanya akan muncul sebagai definisi. | Purwarupa tampilan peringatan pada A9, bila ada waktu untuk membuat rangkar tampilan di PPT II. | Dibiarkan terbuka pada PPT I, dan dicatat sebagai kandidat kuat untuk PPT II. |

Empat BoK di atas dibiarkan terbuka dengan sadar. Memaksakan BoK tanpa data akan menghasilkan kalimat yang terdengar dalam tetapi tidak mengubah satu pun keputusan pada sembilan alternatif. Rubrik menilai kedalaman penggunaan standar BoK, bukan jumlah BoK yang disebut.

## 3.3 Kriteria dan Batasan Pemilihan Alternatif Solusi

Subbab ini menyiapkan bahan untuk subbab 3.4, dan sengaja tidak menetapkan bobot. Bobot adalah keputusan stakeholder dan dihitung pada subbab 3.4 beserta uji sensitivitasnya.

### 3.3.1 Kriteria pemilihan

| Kode | Kriteria | Arah | Satuan | Dasar angka |
| --- | --- | --- | --- | --- |
| C1 | Efektivitas deteksi pada gate yang sudah dikunci | benefit | lift dalam kali dan AUPRC | terukur pada baseline, sebagian untuk alternatif |
| C2 | Kecukupan bukti per fold | benefit | jumlah fold teruji dan jumlah positif per fold | terukur dari hasil uji |
| C3 | Portabilitas antar sumur | benefit | rasio false alarm rate maksimum dibagi minimum per 24 jam | terukur sebelum kalibrasi, belum terukur sesudah kalibrasi |
| C4 | Kepatuhan mode advisory tanpa alarm otomatis | benefit | jumlah slot alarm otomatis, target nol, dan jumlah head dengan review manusia | terukur dari hasil uji |
| C5 | Kebutuhan akuisisi data baru | cost | jumlah wellbore atau berkas yang harus diproses | terukur pada kebutuhan data, jam kerja berstatus asumsi |
| C6 | Waktu penyelesaian dalam satu semester | cost | minggu kerja | tenggat 9 minggu baku dari pedoman; jam kerja per alternatif masih asumsi: isi = estimasi waktu kerja; dasar = belum ada pengukuran; alasan dipilih = untuk membandingkan beban waktu antaralternatif sebelum eksekusi; cara menguji = kalibrasi dengan pencatatan waktu saat eksekusi |
| C7 | Ketertelusuran dan reproduksibilitas angka | benefit | jumlah klaim tanpa jejak, target nol | terukur dari hasil uji |
| C8 | Beban kognitif keluaran | benefit | rubrik tiga tingkat | asumsi; isi: beban kognitif dinilai dengan rubrik tiga tingkat; dasar: antarmuka keluaran belum dirancang sehingga belum bisa diukur; alasan dipilih: memberi sinyal keluaran yang menuntut driller menafsir model; cara menguji: validasi rubrik bersama mitra saat purwarupa dan rekam berapa langkah keputusan |

Rincian cara ukur dan sumber setiap kriteria:

- **C1 Efektivitas deteksi pada gate yang sudah dikunci.** Cara ukur: Lift per fold dibanding baseline persistence, AUPRC dibanding canary. Gate G1 dan G2 tidak diubah. Sumber:.
- **C2 Kecukupan bukti per fold.** Cara ukur: Hitung positif per fold. Fold dengan kurang dari 30 positif dilabeli underpowered dan tidak dihitung sebagai mayoritas. Sumber:.
- **C3 Portabilitas antar sumur.** Cara ukur: Ukur false alarm rate per sumur pada titik operasi yang sama, sebelum dan sesudah kalibrasi per sumur. Sumber:.
- **C4 Kepatuhan mode advisory tanpa alarm otomatis.** Cara ukur: Hitung dari registry head. Slot alarm otomatis wajib nol, head wajib membawa penanda review manusia. Sumber:.
- **C5 Kebutuhan akuisisi data baru.** Cara ukur: Hitung dari peta kanal dan status parse. Alternatif yang memakai data yang sudah ada dinilai lebih murah. Sumber:.
- **C6 Waktu penyelesaian dalam satu semester.** Cara ukur: Petakan pekerjaan alternatif ke Tabel 3.1. Pekerjaan yang tidak dapat selesai sebelum presentasi akhir diberi penalti. Sumber: `Buku Pedoman PPT Tahap I Tabel 3.1, halaman 32`.
- **C7 Ketertelusuran dan reproduksibilitas angka.** Cara ukur: Jalankan pemeriksa jejak pada dokumen dan JSON. Setiap angka harus menunjuk berkas dan baris atau kunci JSON. Sumber:.
- **C8 Beban kognitif keluaran.** Cara ukur: Tingkat 3 bila keluaran satu baris peringatan dengan waktu, keyakinan, dan tindakan yang disarankan, serta frekuensi pemeriksaan satu kali per empat jam atau lebih jarang. Tingkat 2 bila keluaran berupa daftar kandidat tanpa urutan prioritas, atau frekuensi lebih dari 6 per 24 jam. Tingkat 1 bila keluaran berupa alarm biner tanpa konteks atau menuntut pengguna menafsirkan model. Sumber:.

Kriteria C8 adalah satu-satunya kriteria kualitatif, sehingga rubriknya ditulis terbuka pada tabel kriteria di atas dan diulang di sini: tingkat 3 bila keluaran satu baris peringatan dengan waktu, keyakinan, dan tindakan yang disarankan, serta frekuensi pemeriksaan satu kali per empat jam atau lebih jarang; tingkat 2 bila keluaran berupa daftar kandidat tanpa urutan prioritas, atau frekuensi lebih dari 6 per 24 jam; tingkat 1 bila keluaran berupa alarm biner tanpa konteks atau menuntut pengguna menafsirkan model. Rubrik ini berstatus asumsi sampai divalidasi mitra.

Tujuh dari delapan kriteria memiliki angka terukur atau baku, dan hanya C8 yang kualitatif. Ini disengaja, supaya subbab 3.4 tidak perlu memakai skala 1 sampai 5 untuk hal yang sudah dapat diukur, misalnya false alarm rate atau jumlah fold.

### 3.3.2 Batasan pemilihan

| Kode | Batasan | Kategori | Bukti | Konsekuensi desain |
| --- | --- | --- | --- | --- |
| B1 | Kerahasiaan data mitra | kerahasiaan dan legal | | Alternatif yang membutuhkan kanal milik mitra tidak dapat dieksekusi pada PPT I. Alternatif yang hanya memakai data terbuka dinilai lebih siap. |
| B2 | Mode advisory tanpa alarm otomatis | teknis | | Alternatif yang mengklaim alarm otomatis atau penghentian operasi otomatis gugur pada tahap seleksi. Keluaran wajib berupa konfirmasi status, peringatan berpengawas, atau tren. |
| B3 | Sumber daya dan waktu satu semester | waktu dan ekonomi | `Buku Pedoman PPT Tahap I Tabel 3.1, halaman 32; Buku Pedoman PPT Tahap I subbab 2.6 butir 1` | Alternatif yang menuntut pengembangan baru berskala besar, seperti pelatihan ulang dengan dekomposisi mode ditambah ranking, harus dipecah dan dijadwalkan. A2 sudah menyelesaikan bagian terberat, yaitu parse empat wellbore. |
| B4 | Mutu label belum terbukti | kualitas | | Urutan kerja wajib, yaitu audit label lebih dahulu, kalibrasi kemudian. Alternatif yang melanggar urutan ini dinilai tidak layak dipilih, sekuat apa pun hasil numeriknya. |
| B5 | Cakupan satu lapangan dan domain bengkel | proses | | Klaim generalisasi antar operator dilarang. Alternatif pada domain bengkel harus menyatakan batas domainnya secara terbuka. |
| B6 | Ketiadaan label keausan fisik dan tarif rig | data dan ekonomi | | Alternatif yang membutuhkan keausan fisik harus jujur memakai proksi berupa batas run. Analisis biaya pada subbab 3.4 wajib memakai asumsi tarif dengan uji sensitivitas. |

Rincian setiap batasan:

- **B1 Kerahasiaan data mitra (kategori kerahasiaan dan legal).** Seluruh angka pada proposal berasal dari lapangan Volve yang terbuka dan empat set data eksternal. Telemetri real-time milik mitra tidak dipakai sebagai sumber angka, sehingga tidak ada data mitra yang perlu disalin ke repositori maupun dilampirkan.
- **B2 Mode advisory tanpa alarm otomatis (kategori teknis).** Alat berjalan sebagai pemberi peringatan berpengawas manusia. Jumlah slot alarm otomatis kritis nol dari dua puluh tujuh head, dan dua head berstatus belum layak pakai sehingga dilarang dipakai di tingkat mana pun.
- **B3 Sumber daya dan waktu satu semester (kategori waktu dan ekonomi).** Tim tiga orang dengan satu semester. Pekerjaan harus selesai di dalam jadwal Tabel 3.1, dari perumusan masalah sampai presentasi akhir.
- **B4 Mutu label belum terbukti (kategori kualitas).** Kontrol-positif label stuck nol dari sepuluh, label hyd masih proksi residual, dan campuran severitas berbeda antar sumur. Kalibrasi ambang yang dijalankan sebelum label dibereskan menghasilkan presisi palsu.
- **B5 Cakupan satu lapangan dan domain bengkel (kategori proses).** Seluruh data berasal dari satu lapangan. Data keausan alat berasal dari domain bengkel dan bukan dari rig, sehingga tidak boleh diperlakukan sebagai bukti perilaku alat di rig.
- **B6 Ketiadaan label keausan fisik dan tarif rig (kategori data dan ekonomi).** Tujuh puluh tujuh berkas bhaRun tidak memuat dullingInfo, dullGrade, maupun bitName, sehingga label keausan fisik tidak tersedia. Tarif rig per jam juga tidak tersedia pada seluruh dataset.

Enam batasan di atas menutup 6 kategori, yaitu data dan ekonomi, kerahasiaan dan legal, kualitas, proses, teknis, waktu dan ekonomi. Rubrik menuntut minimal tiga batasan, sehingga syarat itu terpenuhi.

### 3.3.3 User stories

Enam peran di bawah ini adalah peran operasi yang lazim pada pengeboran dan pada pengelolaan alat. Dua peran memiliki rujukan langsung di dokumen proyek, yaitu insinyur dan driller. Empat peran lain belum memiliki rujukan dokumen dan belum diverifikasi melalui wawancara mitra. Dasar pernyataan itu: pencarian kata wawancara dan interview pada seluruh berkas docs/ hanya menemukan dokumen ini sendiri, dan tidak ada berkas bernama wawancara atau interview di dalam docs/. Status verifikasi peran ditulis pada setiap cerita, dan verifikasi wawancara dicatat sebagai pekerjaan terbuka.

Format yang dipakai adalah kalimat peran, kebutuhan, dan manfaat, lalu dilengkapi kriteria penerimaan yang dapat diukur beserta jejaknya.

#### 3.3.3.1 U1 Insinyur pengeboran Sperry Drilling

**Cerita.** Sebagai insinyur pengeboran, saya ingin menerima peringatan onset beberapa menit sebelum kondisi memburuk beserta waktu peringatan dan tingkat keyakinannya, agar saya punya waktu memilih tindakan sebelum kejadian berubah menjadi waktu rig yang hilang.

**Mengapa peran ini pemilik masalah.** Ini pemilik masalah utama, karena seluruh keluaran alat berakhir pada keputusan insinyur dan bukan pada aktuasi otomatis.

**Status peran.** Rujukan dokumen ada, wawancara belum dilakukan. Dasar:, yaitu empat skenario penggunaan: konfirmasi status otomatis, peringatan berpengawas manusia yang ditindaklanjuti insinyur, dasbor tren, dan keputusan manusia.

**Alternatif yang melayani.** A1, A8, A9. Klaster: K1, K4. Kriteria utama: C1, C2, C3.

**Kriteria penerimaan.**

| Kriteria penerimaan | Ambang | Status |
| --- | --- | --- |
| Pada kelas stuck dengan horizon 10 menit dan titik operasi 0,05, peringatan memberi B1 minimal 0,50 dan TLead median minimal 5 menit. | B1 minimal 0,50 dan TLead median minimal 5 menit | lulus pada kelas stuck, terukur B1 0,51 sampai 1,00 dan TLead 10 sampai 11,5 menit |
| Setiap peringatan menampilkan tingkat keyakinan, tier, dan batas pemakaian head yang menghasilkannya. | 27 dari 27 head memiliki isi pada kunci batas_pemakaian, dan 13 head wajib review manusia | lulus |
| Untuk kelas hidrolik, sistem tidak menampilkan peringatan yang diklaim sebagai deteksi kick atau loss sampai label fisika tersedia. | nol klaim deteksi kick pada kelas hyd | terbuka, menunggu label fisika pada A8, terukur 0 dari 3 onset dengan TLead nol |

#### 3.3.3.2 U2 Driller di lantai rig

**Cerita.** Sebagai driller, saya ingin menerima daftar menit yang layak diperiksa beserta alasannya, bukan alarm yang memaksa saya berhenti, agar saya tidak kehilangan waktu pada alarm yang salah.

**Mengapa peran ini pemilik masalah.** Driller adalah penerima keluaran dengan beban kerja paling langsung, sehingga anggaran alarm harus diukur dari pemeriksaan yang ia harus lakukan.

**Status peran.** Rujukan dokumen ada, wawancara belum dilakukan. Dasar: tentang menandai menit yang layak driller cek, dan tentang satu pemeriksaan driller per empat jam.

**Alternatif yang melayani.** A9, A7. Klaster: K4. Kriteria utama: C3, C4, C8.

**Kriteria penerimaan.**

| Kriteria penerimaan | Ambang | Status |
| --- | --- | --- |
| False alarm rate pada titik operasi terpilih tidak lebih dari 6 per 24 jam untuk setiap sumur. | FAR maksimal 6 per 24 jam per sumur | belum lulus pada shk, karena terukur 18 sampai 63 per 24 jam pada titik operasi 0,05 sampai 0,10 |
| Tidak ada slot alarm otomatis kritis pada alat. | auto_critical_alarm_slots sama dengan 0 | lulus |
| Keluaran berupa satu baris peringatan dengan waktu, keyakinan, dan tindakan yang disarankan, sehingga tidak menuntut driller menafsirkan model. | rubrik beban kognitif tingkat 3 sesuai kriteria C8 | terbuka, karena antarmuka belum dirancang |

#### 3.3.3.3 U3 Toolhand penanggung jawab bengkel alat

**Cerita.** Sebagai toolhand, saya ingin tahu alat mana yang sedang menuju akhir umur dan seberapa cepat, agar penggantian dilakukan sebelum kerusakan memaksa berhenti.

**Mengapa peran ini pemilik masalah.** Satu-satunya domain pada proyek ini yang sudah memiliki ambang alarm terkalibrasi adalah domain bengkel, sehingga peran ini paling cepat menerima manfaat.

**Status peran.** Peran operasi, belum ada rujukan dokumen dan belum diverifikasi. Dasar: Kebutuhan diturunkan dari domain data bengkel, yaitu 4 alat dan 2 run dengan 469 jendela; nama peran belum ada di dokumen proyek.

**Alternatif yang melayani.** A7. Klaster: K4. Kriteria utama: C1, C5.

**Kriteria penerimaan.**

| Kriteria penerimaan | Ambang | Status |
| --- | --- | --- |
| Titik perubahan terdeteksi pada setiap alat yang diuji. | 4 dari 4 alat | lulus |
| Waktu ancang sebelum titik perubahan minimal 20 detik. | TLead 20 sampai 36 detik, yaitu 1,8 kali | lulus |
| Jumlah alarm palsu per alat tidak lebih dari 3 setelah kalibrasi, dan presisi per run dinyatakan terbuka. | false positive 1 sampai 3 per alat, presisi run 0,50 dilaporkan | lulus dengan catatan, karena presisi run 0,50 berarti separuh titik ubah terjadi pada alat baru |

#### 3.3.3.4 U4 Manajer operasi Sperry Drilling

**Cerita.** Sebagai manajer operasi, saya ingin setiap klaim alat membawa tingkat kesiapan dan batasnya, agar saya dapat memutuskan pemakaian tanpa menanggung klaim yang berlebih.

**Mengapa peran ini pemilik masalah.** Keputusan memakai alat di lapangan adalah keputusan manajerial, dan risiko klaim berlebih bersifat organisasi, bukan teknis.

**Status peran.** Peran operasi, belum ada rujukan dokumen dan belum diverifikasi. Dasar: Kebutuhan diturunkan dari struktur registry yang memberi tier dan batas pemakaian per head.

**Alternatif yang melayani.** A3, A5, A9. Klaster: K1, K3, K4. Kriteria utama: C4, C7.

**Kriteria penerimaan.**

| Kriteria penerimaan | Ambang | Status |
| --- | --- | --- |
| Setiap head membawa tier, batas pemakaian, dan lencana false alarm. | 27 dari 27 head terisi ketiga kunci tersebut | lulus |
| Head yang belum layak pakai tidak dipakai di tingkat mana pun. | 2 head berstatus belum layak pakai dinyatakan terbuka | lulus |
| Setiap angka pada laporan manajemen menunjuk berkas dan baris atau kunci JSON. | nol angka tanpa jejak pada pemeriksa | lulus pada dokumen ini, diperiksa skrip |

#### 3.3.3.5 U5 Insinyur data dan kinerja

**Cerita.** Sebagai insinyur data, saya ingin dapat menjalankan ulang pipeline dan evaluasi dari skrip yang tersimpan, agar angka pada proposal dapat diaudit oleh pihak lain.

**Mengapa peran ini pemilik masalah.** Tanpa reproduksibilitas, seluruh klaim hanya dapat dipercaya atas dasar kepercayaan, dan itu tidak cukup untuk mitra industri.

**Status peran.** Peran operasi, belum ada rujukan dokumen dan belum diverifikasi. Dasar: Kebutuhan diturunkan dari adanya pipeline registry dan berkas hasil.

**Alternatif yang melayani.** A2, A5. Klaster: K2, K3. Kriteria utama: C2, C7.

**Kriteria penerimaan.**

| Kriteria penerimaan | Ambang | Status |
| --- | --- | --- |
| Registry dapat dihitung ulang dari skrip yang tersimpan. | code/v9_i1_pipeline.py tersedia dan head terhitung 27 dari 7 mode | sebagian, karena skrip tersedia dan jumlah head terverifikasi dari JSON, tetapi eksekusi ulang belum dijalankan pada kartu ini |
| Setiap lapisan keputusan dapat ditelusuri ke head asalnya. | jumlah head pada empat lapisan sama dengan 27 | lulus |
| Perubahan definisi label tercatat sebagai versi, bukan sebagai penimpaan. | satu varian onset dikunci dan varian lain dicatat | terbuka, karena audit label belum dijalankan |

#### 3.3.3.6 U6 Pengawas well-control

**Cerita.** Sebagai pengawas well-control, saya ingin alat tidak pernah menyatakan kick atau kehilangan sirkulasi secara otomatis, agar tidak ada keputusan keselamatan yang bergantung pada label proksi.

**Mengapa peran ini pemilik masalah.** Kick dan lost circulation adalah bahaya well-control. Klaim deteksi otomatis pada label proksi akan menjadi tanggung jawab keselamatan yang tidak dapat dipertanggungjawabkan.

**Status peran.** Peran operasi, belum ada rujukan dokumen dan belum diverifikasi. Dasar: Kebutuhan diturunkan dari BoK 10 Safety dan dari status label hyd yang masih proksi.

**Alternatif yang melayani.** A8. Klaster: K1. Kriteria utama: C4, C7.

**Kriteria penerimaan.**

| Kriteria penerimaan | Ambang | Status |
| --- | --- | --- |
| Nol klaim deteksi kick atau loss secara otomatis pada seluruh keluaran alat. | auto_critical_alarm_slots sama dengan 0 dan nol head berlabel kick otomatis | lulus |
| Status label hidrolik dinyatakan sebagai proksi pada setiap dokumen yang memuatnya. | satu pernyataan proksi pada dokumen ini dan pada verdict | lulus |
| Label fisika, yaitu perubahan volume pit dan selisih laju alir, dicatat sebagai prasyarat sebelum klaim well-control apa pun dibuat. | kanal sumber label terdaftar dan terhitung | terbuka, karena label pit dan flow belum diparse menjadi deret label |

### 3.3.4 Silang user story, kriteria, dan alternatif

| User story | Peran | Kriteria | Alternatif | Jumlah kriteria terpenuhi |
| --- | --- | --- | --- | --- |
| U1 | Insinyur pengeboran Sperry Drilling | C1, C2, C3 | A1, A8, A9 | 2 dari 3 |
| U2 | Driller di lantai rig | C3, C4, C8 | A9, A7 | 1 dari 3 |
| U3 | Toolhand penanggung jawab bengkel alat | C1, C5 | A7 | 3 dari 3 |
| U4 | Manajer operasi Sperry Drilling | C4, C7 | A3, A5, A9 | 3 dari 3 |
| U5 | Insinyur data dan kinerja | C2, C7 | A2, A5 | 1 dari 3 |
| U6 | Pengawas well-control | C4, C7 | A8 | 2 dari 3 |

Kolom terakhir menghitung kriteria penerimaan yang berstatus lulus, bukan yang berstatus terbuka. Ini sengaja dibuat ketat, supaya kemajuan tidak dilaporkan dari kriteria yang belum diuji.

### 3.3.5 Serahan untuk subbab 3.4

Subbab 3.4 menerima bahan berikut, dan tidak perlu menghitung ulang dari awal:

1. Delapan kriteria dengan arah, satuan, cara ukur, dan sumber angka, pada 3.3.1.
2. Enam batasan dengan kategori dan konsekuensi desain, pada 3.3.2.
3. Enam user story dengan kriteria penerimaan terukur, pada 3.3.3.
4. Empat klaster beserta relasi prasyarat, pada 3.2.3 sampai 3.2.5, sebagai dasar membaca mengapa dua alternatif tidak boleh dibandingkan sendirian tanpa prasyaratnya.

Yang belum tersedia dan menjadi tugas subbab 3.4:

1. Bobot kriteria. Belum ada wawancara mitra, sehingga bobot wajib ditetapkan sebagai asumsi dengan minimal tiga skenario sensitivitas, bukan satu angka tunggal.
2. Skor kriteria kualitatif C8 untuk setiap alternatif. Rubriknya sudah tersedia di 3.3.1.
3. Perbandingan dengan pilihan draft lama, yang memilih pengklasifikasi pembelajaran mesin tanpa prosedur MCDM.

Larangan yang perlu dipegang subbab 3.4: jangan memakai skala 1 sampai 5 untuk kriteria yang sudah memiliki angka terukur, misalnya C1, C2, C3, C4, dan C5. Untuk kriteria itu, angka asli dipakai langsung setelah dinormalisasi.

### 3.3.6 Hasil negatif dan batas yang harus dinyatakan

1. Peran pemilik masalah belum diverifikasi melalui wawancara. Pencarian kata wawancara dan interview pada seluruh berkas tidak menemukan berkas lain selain dokumen ini, sehingga empat dari enam peran pada 3.3.3 berstatus peran operasi yang belum dikonfirmasi mitra.
2. Tarif rig per jam tidak tersedia, sehingga nilai rupiah apa pun pada subbab 3.4 berstatus asumsi.
3. Portabilitas antar sumur sesudah kalibrasi belum terukur. Yang terukur baru sebaran sebelum kalibrasi, yaitu 4,15 sampai 496,09 per 24 jam.
4. Prevalensi unit stand 10 sampai 40 persen pada A4 masih perkiraan desain.
5. Presisi titik ubah pada alat bengkel hanya 0,50, sehingga klaim keausan progresif belum sah untuk alat baru.
6. Rubrik yang menuntut tiga alternatif per BoK belum terpenuhi untuk BoK 1, 6, 7, 10, dan 12. Risiko penilaian ini dicatat pada 3.2.8, beserta dua jalan keluarnya.
7. System response time dan downtime belum diukur, sehingga standar BoK 11 yang berkaitan dengannya tidak dapat diklaim terpenuhi.
8. Antarmuka peringatan belum dirancang, sehingga kriteria C8 belum dapat dinilai untuk alternatif mana pun.

### 3.3.7 Manifes jejak angka (internal, bukan untuk sirkulasi eksternal)

| Angka | Nilai | Berkas dan baris |
| --- | --- | --- |
| FAR vib antar sumur | 4,15 sampai 496,09 per 24 jam, rasio 119,6 kali | |
| Kontrol-positif stuck | 0 dari 10 | |
| Stuck K-ii | B1 0,51 sampai 1,00, TLead 10 sampai 11,5 menit | |
| Hyd K-ii | 0 dari 3 onset, TLead nol | |
| Tool_wear K-i | 4 dari 4 alat, TLead 20 sampai 36 detik, FP 1 sampai 3, presisi run 0,50 | |
| Tool_wear K-ii canary | AUPRC 0,516 sampai 0,612 atau 1,19 kali | |
| Gate shk | G1 3 dari 7, G2 6 dari 7 | |
| Gate hyd | G1 2 dari 7, G2 4 dari 7 | |
| Gate tool_wear | G1 0 dari 4, G2 4 dari 4 | |
| Gate ssi | G1 4 dari 5, G2 5 dari 5, F-7 tiga positif, F-9 dua belas positif | |
| Gate bit_wear | G1 3 dari 4, G2 4 dari 4, persistence menang 4 dari 4 | |
| Kanal disfungsi empat wellbore | 188/186/66/18, 135/135/135/86, 91/90/52/6, 77/76/76/76 | |
| Kanal label fisika | GAINLOSSTOT 575 dan 517, PITTOT 565 dan 506, FLOWOUT 688, FLOWOUTPC 949 | |
| Baris CRPM hasil parse | 281.030 / 42.010 / 178.430 / 57.846 | |
| TSPP | 52.905 baris, empat berkas | |
| Basis label kurasi | 884 kejadian, 50 relevan BHA, 73.500 menit atau 1.225 jam | |
| Berkas bhaRun tanpa label keausan | 77 berkas | |
| Prevalensi unit stand | 10 sampai 40 persen, berstatus asumsi | |
| Ambang kelayakan pemantauan | FAR maksimal 6 per 24 jam | |
| Keluaran screening shk | FAR 18 sampai 63 per 24 jam, presisi 0,00 sampai 0,12 | |
| Tiga angka pengikat | 7 mode, 11 klaim, 27 head | |
| Lapisan keputusan | 5 / 11 / 9 / 2 sama dengan 27 | |
| Sumber data | Volve terbuka dan empat set data eksternal | |
| Batas muktamad cakupan | satu lapangan, bengkel berbeda dari rig, hyd proksi | |
| Slot alarm otomatis | 0 pada 27 head | |

Reproduksi: `python3 scratch/ppt1/build_bab3_2.py` menulis ulang tabel subbab ini dari berkas hasil eksekusi, sehingga angka pada tabel berasal dari berkas yang sama dan bukan diketik ulang dari tempat lain.
