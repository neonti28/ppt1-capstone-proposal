# BAB IV KESIMPULAN DAN SARAN

## 4.1 Kesimpulan

**Kesimpulan 1: masalah teridentifikasi.** Masalah utama pada layanan pengeboran yang
dikaji bukanlah ketiadaan data, melainkan tidak adanya satu titik keputusan yang
menggabungkan data kondisi dengan hasil kalkulasi risiko. Data dan hasil kalkulasi keduanya
sudah tersedia: telemetri 118 kanal per wellbore dan 27 head hasil evaluasi berlapis.
Yang belum ada adalah jembatan antara keduanya, sehingga 388 kejadian interupsi selama
1.212 jam window terkurasi masih ditangani reaktif, dengan median 45 menit dan p90 180 menit
per kejadian. Akar masalah ini diperinci pada fishbone 6M di 1.2 dan dibuktikan dengan
tiga alat analisis di Bab II: VSM menunjukkan lebih separuh waktu terkunci pada status
menunggu kejelasan, MIFC menunjukkan putusnya alur informasi, dan FTA menunjukkan cabang
yang paling menumpuk adalah cabang keputusan manusia, bukan ketiadaan alat ukur.

**Kesimpulan 2: peringkat risiko terbentuk.** FMECA menghasilkan empat mode ber-RPN
tinggi: kegagalan fluida sumur (490), stuck pipe (400), kegagalan BHA (378), dan kegagalan
mesin permukaan (320). Dua di antaranya justru sudah memiliki engine yang diuji, sehingga
celah yang perlu ditutup adalah keandalan deteksi dan penyajian keputusan, bukan penambahan
alat ukur semata.

**Kesimpulan 3: solusi terpilih.** Dari sembilan alternatif yang diusulkan tiga anggota,
solusi terpilih adalah **sistem pemantauan kondisi pengeboran berbasis dashboard dengan
7 engine dan 27 head, berstatus advisory dengan 0 slot alarm otomatis**, dipadukan dengan
tiga pendukung wajib: kendali mutu data WITSML, SOP eskalasi berjenjang, dan kalibrasi
ambang per sumur. Pemilihan dilakukan dengan TOPSIS atas enam kriteria dan diuji
sensitivitasnya pada sembilan skenario bobot. Tiga pendamping itu dipilih bukan sebagai
solusi pengganti, melainkan sebagai syarat agar solusi utama benar-benar dapat
dipertanggungjawabkan.

**Kesimpulan 4: batas yang diakui.** Sistem ini tidak menggantikan keputusan manusia.
Seluruh head berada di bawah tinjauan engineer, false alarm rate pada beberapa engine
masih menyebar hingga hampir 120 kali antar sumur, dan tidak ada klaim penghematan biaya
yang sudah terukur pada tahap ini.

## 4.2 Saran

**Saran 1: untuk kelanjutan proyek (PPT II).** Kalibrasi ambang per sumur pada tiga
engine terdepan (`stuck`, `hyd K-i`, `vib`) dengan target false alarm rate di bawah 6 per
24 jam pada mayoritas sumur, karena titik itu menjadi syarat agar sebuah head layak naik
dari peringatan berpengawas menjadi peringatan sungguhan.

**Saran 2: untuk penutupan celah deteksi.** Mengembangkan `hyd K-ii` untuk mode kegagalan
fluida sumur. Mode ini memperoleh RPN tertinggi justru karena deteksinya paling buruk,
sedangkan dampaknya menyentuh aspek keselamatan.

**Saran 3: untuk kerja sama data.** Membangun pemetaan antara jam berhenti dan work
order. Pada build sekarang jam berhenti tercatat (2.739,667 jam untuk kegagalan
peralatan) tetapi belum terikat pada satu peristiwa alarm, sehingga dampak finansial tidak
bisa dihitung sampai hubungan itu ada.

**Saran 4: untuk angka ekonomi.** Mengganti seluruh angka biaya asumsi dengan data
kontrak sebenarnya begitu ruang lingkupnya diizinkan, karena pada tahap ini seluruh
perhitungan kerugian berdiri di atas literatur publik, bukan pada nilai yang berlaku di
lapangan.

**Saran 5: untuk perbaikan metodologis.** Menguji stabilitas hasil antar sumur dengan
skema leave-one-well-out pada seluruh head yang kini baru diuji pada segmen tunggal.
Hasil AUPRC pada engine getaran sebesar 0,9117 wajib diuji ulang karena labelnya
diturunkan dari kanal yang sama, sehingga berisiko sirkular.

**Saran 6: untuk dokumen lanjutan.** Menyelesaikan prototipe antarmuka yang dapat
dibuka dan diuji bersama pemilik masalah, lalu melakukan validasi silang rancangan dengan
mereka sebelum tahap pemodelan sistem dimulai, sesuai kegiatan re-evaluate pada setiap
akhir tahap dalam model SIMILAR.
