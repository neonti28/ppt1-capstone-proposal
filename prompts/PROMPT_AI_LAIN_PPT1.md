# PROMPT UNTUK AI LAIN (salin seluruh blok di bawah, tempel ke AI pilihan Anda)

Anda penulis naskah proposal akademik Indonesia (formal, gaya tulisan tangan manusia, tanpa nada robot). Tugas: menulis ulang Bab I dan Bab II proposal Proyek Perancangan Terpadu (PPT I) tentang analisis akar penyebab kegagalan Bottom Hole Assembly (BHA) pada operasi pengeboran sumur, dan MENYERAHKAN bukti bahwa setiap bagian sudah diperiksa sebelum dinyatakan selesai.

## ATURAN KERAS (pelanggaran = ulang dari nol)
1. DILARANG membuat standar sendiri. Setiap alat analisis WAJIB mengikuti publikasi resminya dan menyebut rujukannya di teks saat alat itu dipakai pertama kali. Jika Anda tidak yakin isi suatu standar, cari dulu di internet, jangan mengarang.
2. DILARANG menaruh tanda strip "-", "TBD", "belum diukur", atau templat kosong di dalam gambar dan tabel. Kotak data hanya boleh memuat besaran yang benar-benar tersedia. Besaran yang tidak tercatat dinyatakan SEKALI dalam satu kalimat catatan di bawah gambar/tabel, bukan diulang per sel.
3. DILARANG mengarang angka. Semua angka harus terlacak ke tabel sumber dengan status bukti (terukur / tercatat / acuan kesepakatan klien / turunan / skenario simulasi). Setiap angka turunan harus menampilkan langkah hitungnya.
4. DILARANG menyebut nama perusahaan, operator, ladang, rig, atau kontrak mana pun. Semua aktor ditulis netral: "penyedia layanan", "klien", "kru rig", "bengkel".
5. DILARANG menulis kalimat pembelaan "ini X, bukan Y", kolom larangan per alat, instruksi untuk pembuat gambar, daftar periksa penulisan, atau kriteria internal. Naskah hanya berisi isi yang dibutuhkan pembaca penilai.
6. DILARANG mengutip dokumen kerja internal, catatan proses, atau panduan orkestrasi ke dalam naskah dan Daftar Pustaka.
7. Semua tabel diberi nomor pola bab.urut (Tabel 1.1, Tabel 2.1, dst.) dengan judul di atas tabel; semua gambar demikian (Gambar 1.1, Gambar 2.1, dst.). Dokumen dibuka DAFTAR ISI, DAFTAR TABEL, DAFTAR GAMBAR.
8. Daftar Pustaka gaya penulis-tahun lengkap dengan penerbit; setiap sumber yang tercantum HARUS disitasi di dalam teks di tempat ia dipakai.

## DATA YANG WAJIB DIPAKAI (jangan menambah angka lain)
- Dataset publik Equinor Volve: 884 kejadian terkurasi, 10 wellbore, total 1.225 jam; median 45 menit; p90 180 menit; kategori: bha_stuck_fishing 38, wellbore_fluid 25, failure_unlocated 28. Sisanya kategori lain.
- Kasus 1: NPT 5,00 jam (3,50 + 1,50) menurut laporan harian; pemulihan penuh 10 jam menurut skenario; keduanya tidak boleh dijumlahkan.
- Kasus 2: lost rig hours 0 karena operasi dilanjutkan sampai titik casing.
- Spread cost per hari: onshore 45.000 USD, jack-up 170.000 USD, deepwater 480.000 USD; per jam: 1.875, 7.083,33, 20.000 USD (tulis 7.083,33 dengan penanda pembulatan; 24 x 7.083,33 = 170.000).
- Biaya perbaikan dan tambahan: 25.000 USD (onshore), 75.000 USD (jack-up), 220.000 USD (deepwater). Kurs 1 USD = Rp16.000.
- Kerugian langsung: 34.375; 43.750; 245.000; 940.000 USD. Rasio antartipe: 5,6x dan 21,5x terhadap pemulihan penuh onshore.
- Skenario deepwater: siklus pemulihan 36 jam: Diagnosis 3, Penarikan 11, Pelepasan dan inspeksi 3, Perakitan pengganti 5, Uji fungsi 2, Turun kembali 9, Reaming dan pemulihan 3. Skenario jack-up 24 jam: 2, 7, 4, 2, 8, 1.
- Metode hitung kerugian: (1) lama hentian; (2) spread cost per jam = harian / 24; (3) kerugian operasional = jam x spread; (4) kerugian langsung = operasional + biaya perbaikan; faktor formasi 1,30 untuk formasi berat.
- Contoh: 5 jam x 1.875 = 9.375; + 25.000 = 34.375 USD; deepwater 36 jam x 1,30 = 46,8 jam ekuivalen; 936.000 + 220.000 = 1.156.000 USD (sekitar Rp18,5 miliar).
- Tarif acuan awal dari kesepakatan dengan klien: 41 USD/ft, operating charge 1.000 USD/jam, biaya tetap 21.500 USD.
- Tiga akar penyebab: A. akumulasi kerusakan komponen tidak dikelola sepanjang siklus hidup; B. kesiapan tool sebelum run tidak terjamin; C. keputusan operasi tanpa catatan kondisi komponen.

## SPESIFIKASI ALAT (ikuti persis)
- VSM: Rother & Shook, Learning to See, Lean Enterprise Institute (cetak versi 1.4, 2003). Unsur wajib: ikon pemasok berlabel, ikon pelanggan berlabel, kotak ketentuan aliran, kotak kendali produksi, kotak proses berurutan dengan kotak data (hanya besaran terukur: waktu siklus dan pelaksana), panah dorong bergaris antarproses, ikon pengiriman dengan frekuensi, aliran informasi garis tipis dengan frekuensi, penanda peluang perbaikan pada langkah terlama, tangga waktu (waktu proses di bawah garis, penantian di atas), dan baris jumlah: lead time, waktu proses, waktu nilai tambah, efisiensi. Segitiga persediaan hanya bila ada persediaan terekam. Nilai tambah didefinisikan dari sudut pelanggan (kemajuan sumur).
- MIFC: alur material dan alur informasi terpisah, dengan dokumen nyata (laporan harian, laporan interupsi layanan pada laporan akhir sumur, tally BHA, first alert, order perbaikan) dan temuan putusnya umpan balik.
- OPC: ASME Y15.3M-1979, simbol operasi/inspeksi/transportasi, langkah terlama ditunjuk eksplisit.
- FMECA: IEC 60812:2018; nilai O hanya dari cacah kejadian yang relevan BHA (kategori yang bukan kegagalan BHA dilarang dipakai sebagai frekuensi); sertakan peta pita O-S-D agar RPN dapat direproduksi.
- FTA: IEC 61025; gerbang dan kejadian dasar diberi kode; jumlah minimal cut set dihitung dan ditampilkan.
- Barrier analysis: IEC 62740:2015; status barrier (berdiri/lemah/hilang) dengan bukti per baris.
- Fishbone 6M: enam cabang, tiap ranting diberi kode Mn/Me/Ma/Mt/Ms/En dan SEMUA ranting dipetakan ke akar penyebab.
- 5W1H: enam baris What, Why, When, Where, Who, How (wajib ada "How" untuk mekanisme kegagalan; How much dipisah bila dipakai).

## PROSEDUR WAJIB SEBELUM MENYATAKAN SELESAI
1. Hitung ulang semua angka dengan skrip, tempel hasil hitungannya.
2. Ceklis simbol VSM satu per satu terhadap gambar.
3. Baca utuh naskah yang Anda tulis, baris demi baris, bukan pencarian kata.
4. Pastikan setiap rujukan silang menunjuk subbab/tabel yang benar-benar memuat isinya.
5. Pastikan penomoran tabel/gambar berurutan tanpa lompatan dan ketiganya ada di daftar.
6. Nyatakan di akhir: daftar pemeriksaan yang sudah Anda jalankan beserta hasilnya. Bila ada yang gagal, perbaiki dulu, jangan dilaporkan sebagai kekurangan.

## KELUARAN
Satu berkas Markdown lengkap Bab I-II + daftar isi/tabel/gambar + daftar pustaka; gambar sebagai skrip Python yang membaca SATU berkas data JSON (sumber tunggal) dan menghasilkan PNG; tambahkan pemeriksa tumpang-tindih teks pada skrip gambar.
