# BAB I 1.4: BATASAN PENELITIAN DAN KERAHASIAAN

Subbab ini dicantumkan eksplisit karena Buku Pedoman §2.5 menuntut perbedaan antara
proyek perancangan terpadu dan penelitian teoretis: proyek berjalan di tengah kendala
praktis, standar, dan aturan yang berlaku.

## 1.4.1 Sumber data

Seluruh data yang dianalisis dalam proposal ini berasal dari **dataset publik Equinor
Volve** yang diperoleh lewat kanal publik penyedia dan digunakan setelah mendapat
persetujuan dosen pengampu. Terdiri atas telemetri WITSML 10 wellbore dengan 118 kanal
pada satu wellbore contoh, 884 baris interupsi terkurasi, catatan aktivitas (DDR)
23.447 baris selama 39.398 jam, serta dokumen akhir sumur (EOWR) yang menjadi sumber
label kejadian. Seluruh angka dalam dokumen ini dapat direproduksi dari data tersebut.

Proposal ini **tidak memakai, tidak mengutip, dan tidak menyebut** data operasional milik
perusahaan mana pun. Data perusahaan tersebut bersifat rahasia dan hanya boleh diakses
untuk keperluan pembelajaran internal tim di luar dokumen akademik.

## 1.4.2 Identitas

Nama perusahaan, divisi, dan lokasi proyek disamarkan. Tim disebut sebagai anggota A, B,
dan C. Objek kajian dirujuk sebagai "perusahaan layanan pengeboran multinasional" tanpa
penyebutan nama, agar dokumen dapat diajukan tanpa melanggar perjanjian kerahasiaan.

## 1.4.3 Angka ekonomi

Tidak ada biaya, tarif, atau nilai penalti yang diambil dari data internal. Seluruh angka
ekonomi dalam dokumen ini berasal dari publikasi luar (studi biaya NPT, laporan tarif
pengeboran) dan **diberi label ASUMSI** beserta sumbernya di Lampiran D. Nilai sebenarnya
di lapangan bergantung pada perjanjian antara perusahaan dengan klien dan dapat berbeda
jauh dari rentang yang dipakai di sini.

## 1.4.4 Keterbatasan validitas

1. **Kalibrasi per sumur.** Ambang deteksi pada data ini memiliki false alarm rate yang
   menyebar 4,1 sampai 496 per 24 jam antar sumur. Angka yang sama pada sumur lain tidak
   dijamin, sehingga calibrasi per sumur menjadi prasyarat sebelum alat dipakai.
2. **Bukan bukti penurunan kerugian.** Proposal ini menawarkan rancangan, bukan klaim
   penghematan. Tidak ada pengurangan NPT yang terukur dalam kondisi nyata pada tahap ini.
3. **Kelas kegagalan tidak seimbang.** 496 dari 884 baris label adalah operasi wajar
   tanpa bukti kegagalan, dan hanya 50 kejadian yang berlabel relevan BHA. Model untuk
   kelas langka memiliki kekuatan statistik terbatas.
4. **Data telemetri yang tidak ada.** Kanal getaran yang tersedia berupa shock risk dan
   shock total dari MWD, bukan akselerasi tiga sumbu berfrekuensi tinggi. Klaim apa pun
   tentang vibrasi dibatasi pada kanal yang benar-benar ada.
5. **Domain berbeda untuk alat keausan.** Sebagian hasil keausan alat berasal dari data
   bengkel, sehingga waktu terdepannya dihitung dalam detik dan tidak boleh dijumlahkan
   dengan waktu terdepan pada domain rig.
6. **Cacat data pada kanal SPPA.** Tiga puluh sel pada kolom SPPA memuat nilai absolut
   di atas 10^20 dengan maksimum 9,524e+30 (25 sel pada berkas kontrol, 5 sel pada berkas
   kejadian), yang 35 orde di atas rentang fitur lain. Model berbasis pohon tidak terpengaruh,
   tetapi keluarga model linear dan jaringan saraf gagal dilatih sampai nilai itu
   dipotong. Klaim apapun tentang keluarga ini harus menyertakan syarat pemotongan.md` bagian 3.5.5.
7. **Pencarian otomatis belum menutup pemilihan algoritme.** Pada 7 sumur, satu model
   hasil pencarian otomatis kalah dari Random Forest antar hiperparameter, sedangkan
   gabungan median seluruh kandidatnya menang. Penggabungan berbobot hasil pembelajaran
   (stacking) belum diuji, sehingga urutan keunggulan antar strategi gabungan masih
   terbatas pada yang sudah diuji.5.7.

## 1.4.5 Ruang lingkup

Proposal ini berhenti pada tahap **State the Problem dan Investigate** sesuai pedoman.
Prototipe dashboard disebutkan sebagai bukti kelayakan solusi terpilih, bukan sebagai
klaim bahwa sistem sudah dipasang atau sudah dipakai di lapangan. Pengujian nyata di
lingkungan operasi menjadi ruang lingkup Proyek Perancangan Terpadu II.
