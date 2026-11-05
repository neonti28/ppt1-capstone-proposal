# BAB I 1.3: PEMBAGIAN TANGGUNG JAWAB DAN TITIK KRITIS

Tim terdiri dari tiga anggota dengan penamaan disamarkan sesuai kesepakatan.
Pembagian dilakukan per-bab, bukan per-anggota, supaya setiap titik kritis punya
satu pemilik dan tidak ada pekerjaan yang jatuh di antara dua orang.

| Anggota | Tanggung jawab utama | Titik kritis | Bukti penyelesaian |
|---|---|---|---|
| A | Bab I 1.1 latar belakang sistem; Bab I 1.2 akar penyebab; skala Severity FMEA di 2.4 | Rumusan masalah dinilai jujur terhadap data; jika fishbone tidak menjawab data, seluruh bab III jadi menjawab masalah yang salah | Fishbone 6M dan 5W1H terbit di 1.2 dengan angka 388 dan 611 jam sebagai landasan |
| B | Bab II 2.1 VSM; 2.2 MIFC; 2.3 OPC; ledger angka dan provenance seluruh dokumen | Setiap angka di proposal harus punya baris sumber; angka tanpa jejak dilarang masuk naskah | `PPT1_LEDGER_ANGKA.md` (111 angka, 72 terukur) dan tabel sumber di tiap bab |
| C | Bab III 3.1 alternatif; 3.2 affinity dan BoK; 3.3 kriteria dan user stories; 3.4 MCDM | Pemenang MCDM harus menang pada bukan hanya satu set bobot; kalau menang hanya pada bobot tunggal, hasilnya lemah | Delapan belas uji bobot dan sapuan C1 di 3.4 |

**Kontribusi individual yang disyaratkan.** Pedoman §3.2 dan rubrik kriteria 3
mensyaratkan usulan per mahasiswa disertai laporan singkat BoK. Karena itu:

| Anggota | Tiga alternatif | BoK yang didalami |
|---|---|---|
| A | A1 dashboard pemantauan kondisi lubang bor; A2 SOP triage dan eskalasi alarm berjenjang; A3 pelatihan kru membaca tren | BoK 14, BoK 9, BoK 1 |
| B | B1 pipeline pencatatan WITSML dan kendali mutu data; B2 penambahan kanal sensor getaran; B3 perbaikan alur informasi rig-ke-kantor | BoK 11, BoK 12, BoK 9 |
| C | C1 model deteksi dini per mode kegagalan; C2 kontrak berbasis performa; C3 manajemen keandalan BHA berbasis risiko | BoK 5, BoK 3, BoK 2 |

Ringkasan masing-masing anggota beserta BoK dan standarnya ada di Lampiran B.

**Mengapa titik kritis di tiga tempat itu.**

1. *Rumusan masalah* (milik A): pedoman §2.3 mensyaratkan masalah yang jelas, nyata,
   dan disertai root cause analysis. Kalau rumusan meleset, semua analisis di belakangnya
   tetap terlihat rapi tetapi menjawab pertanyaan yang salah.
2. *Provenance angka* (milik B): 111 angka di inventaris awal, 30 di antaranya berstatus
   warisan draft tanpa jejak hitung. Tanpa pemilik tunggal, angka seperti itu lolos ke
   naskah dan menjadi temuan paling mudah saat sidang.
3. *Robustness pemilihan* (milik C): rubrik kriteria 4 menilai ketepatan tools keputusan.
   Pemenang yang hanya menang pada satu bobot tunggal adalah hasil rapuh, dan itu baru
   terlihat jika ada pemilik yang menguji sensitivitasnya.

**Titik kritis yang melewati batas anggota.** Dua hal tetap dijadikan tanggung jawab
bersama karena tidak bisa diselesaikan oleh satu orang: validasi oleh pemilik masalah
(keputusan C di luar kuasa tim) dan pengumpulan bukti presentasi (poster individu tetap
tanggung jawab masing-masing, dokumen presentasi kelompok adalah kerja bersama).
