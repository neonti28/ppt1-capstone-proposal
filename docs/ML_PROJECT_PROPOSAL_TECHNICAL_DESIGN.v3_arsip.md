# DOKUMEN PROPOSAL PROYEK DAN DESAIN TEKNIS

## Sistem Pendukung Keputusan Pemeliharaan Berbasis Prediksi Kegagalan Bottom Hole Assembly pada Operasi Pengeboran Minyak dan Gas

### KONTROL DOKUMEN

| Item | Nilai |
|---|---|
| Versi | 3.0 — restrukturisasi solusi advisory (12 Oktober 2026) |
| Status | Proposal dan desain teknis — tahap prototipe |
| Lingkup | Alat pemeliharaan berbasis prediksi (advisory / berpengawas manusia) |
| Sumber data | Lapangan Volve (Equinor, terbuka) + 4 dataset eksternal terverifikasi |
| Riwayat pengembangan | Dirujuk ke `CHANGELOG.md` dan Lampiran A (arsip bukti) |
| Catatan versi | Versi ini hanya memuat solusi aktual. Seluruh riwayat kegagalan kampanye lama dipindah ke `CHANGELOG.md` agar proposal terbaca sebagai rencana solusi, bukan post-mortem. |

### DAFTAR ISI

1. Ringkasan Eksekutif
2. Latar Belakang
3. Rumusan Masalah
4. Tujuan Proyek
5. Usulan Solusi
6. Alur Kerja Sistem
7. Skenario Penggunaan
8. Data
9. Metodologi (multi-metode + penilaian berlapis A/B/C)
10. Pendekatan Teknis
11. Strategi Validasi
12. Alasan Pemilihan Metode
13. Metrik Evaluasi
14. Arsitektur
15. Peta Kemampuan dan Status Terkini
16. Risiko dan Keterbatasan
17. Rencana Penerapan
18. Lini Masa
19. Kriteria Keberhasilan

---

# BAGIAN A: TINGKAT BISNIS DAN EKSEKUTIF

## 1. Ringkasan Eksekutif

Proyek ini membangun **alat pemeliharaan berbasis prediksi** untuk mendeteksi kerusakan dan disfungsi *Bottom Hole Assembly* (BHA) selama operasi pengeboran. Alat ini dirancang sebagai **kelas advisori / berpengawas manusia**: ia memberi peringatan dini, skor kondisi, dan dasbor tren kepada insinyur pengeboran, sementara keputusan operasional tetap pada manusia.

Daripada memaksakan satu model pembelajaran mesin untuk semua jenis kegagalan, alat ini menyusun **tujuh mesin deteksi yang berbeda tugas**, masing-masing memakai metode yang paling cocok untuk tugasnya: deteksi berbasis aturan, deteksi statistik, *persistence*, pembelajaran mesin terawasi, dan mesin hibrida. Setiap mesin dinilai pada tiga lapisan (A: apakah deteksi bekerja; B: apakah bernilai pemeliharaan; C: apakah cukup tepercaya untuk dipakai), lalu dipasang pada tingkat pemakaian yang sesuai dengan kekuatan buktinya.

**Status kemampuan ketujuh mesin (per 12 Oktober 2026):**

| Tingkat pemakaian | Jumlah mesin | Keterangan |
|---|---|---|
| Alarm otomatis kritis | **0** | Belum ada mesin yang memenuhi syarat alarm palsu rendah terukur; tidak diklaim |
| Peringatan berpengawas manusia (terbukti) | **3** | memberi peringatan beberapa menit sebelum kejadian pada sumur terkalibrasi |
| Peringatan berpengawas manusia (bersyarat) | **2** | menunggu pengukuran alarm palsu lanjutan |
| Pemantauan tren / skor | **2** | konfirmasi status dan indeks keausan |
| **Punya peran dalam alat** | **7 dari 7** | tidak ada mesin dibuang; tiap mesin punya batas pemakaian tertulis |

Riwayat pengembangan, termasuk seluruh kampanye evaluasi beserta hasil yang tidak memenuhi ambang, tercatat transparan pada `CHANGELOG.md` dan arsip Lampiran A. Angka penutup kampanye lama dipertahankan apa adanya dan tidak dicabut.

## 2. Latar Belakang

Kegagalan BHA — mencakup *stick-slip*, *whirl*, *bit bounce*, *differential sticking*, dan keausan komponen — menyebabkan non-productive time (NPT) yang mahal, kerusakan peralatan, dan risiko keselamatan. Deteksi dini memungkinkan penyesuaian parameter pengeboran atau penarikan string sebelum kerusakan berlanjut.

Data pengeboran modern (WITSML) mencakup sensor permukaan (torsi, RPM, WOB, hookload, tekanan standpipe, aliran lumpur) dan sensor *Measurement-While-Drilling* (MWD) di bawah permukaan. Meskipun demikian, sebagian besar sinyal disfungsi bersifat lokal di bawah permukaan dan teredam sebelum mencapai permukaan, sehingga deteksi dari sensor permukaan saja memiliki batas yang harus dinyatakan terbuka.

## 3. Rumusan Masalah

1. Jenis kegagalan BHA mana yang dapat dideteksi dari data pengeboran yang tersedia, dan dengan tingkat keandalan apa?
2. Metode apa (aturan, statistik, persistence, atau pembelajaran mesin) yang paling cocok untuk tiap jenis kegagalan, mengingat tiap kegagalan mengerjakan tugas yang berbeda?
3. Seberapa tepercaya hasil deteksi untuk dipakai dalam keputusan pemeliharaan, dan pada tingkat apa (tren, peringatan berpengawas manusia, atau alarm otomatis)?
4. Bagaimana memisahkan klaim yang didukung bukti dari klaim yang berlebihan, agar alat dapat dipakai tanpa menyesatkan pengguna?

## 4. Tujuan Proyek

1. Membangun alat pemeliharaan berbasis prediksi yang mendeteksi minimal tiga jenis kerusakan/disfungsi BHA dari data nyata.
2. Menetapkan tingkat pemakaian yang jujur untuk tiap mesin deteksi (tren, peringatan berpengawas manusia, atau alarm otomatis) berdasarkan lapisan bukti A/B/C.
3. Menyatakan batas pemakaian dan ketidakpastian setiap mesin secara terbuka.
4. Menyusun prototipe advisori yang siap diuji pada sumur terkalibrasi tanpa koneksi langsung ke sistem rig.

## 5. Usulan Solusi

Solusi berupa **susunan banyak mesin deteksi yang berbeda tugas**, dipilih per jenis kegagalan:

| Jenis mesin | Peran | Contoh penerapan |
|---|---|---|
| Deteksi berbasis aturan | Kondisi abnormal sederhana dan konsisten | tekanan tidak normal, ambang torsi |
| Deteksi statistik (median/MAD, change-point, skor-z) | Deteksi perubahan pola operasi | indikasi dini hidraulik, perubahan regime keausan |
| Persistence (status-quo) | Konfirmasi status + pembanding jujur | keadaan berlanjut dari kondisi sebelumnya |
| Pembelajaran mesin terawasi | Peringatan dini dengan lead-time | getaran lateral, stick-slip |
| Mesin hibrida (aturan + statistik + ML) | Arsitektur per mesin | gabungan lapisan dasar + prediksi |

Karena tiap kelas kegagalan mengerjakan tugas berbeda (deteksi anomali, deteksi kondisi, diagnosis, atau prediksi kejadian mendatang), tidak semua mesin memerlukan ambang yang identik. Sebuah aturan sederhana yang mendeteksi tekanan abnormal secara konsisten dapat sangat berguna tanpa mengalahkan model ML pada ambang *lift* 1,5; demikian pula metode statistik dapat membantu pemeriksaan peralatan meskipun belum mampu memprediksi tanggal kejadian. Keputusan akhir pemeliharaan tetap pada manusia.

## 6. Alur Kerja Sistem

```
Data pengeboran (WITSML + MWD)
        ↓
Prapemrosesan (pembersihan, imputasi, jendela waktu)
        ↓
Tujuh mesin deteksi (aturan / statistik / persistence / ML / hibrida)
        ↓
Penilaian berlapis A / B / C per mesin
        ↓
Lapisan keputusan: konfirmasi status · peringatan berpengawas manusia · dasbor tren
        ↓
Keputusan insinyur pengeboran (manusia)
```

## 7. Skenario Penggunaan dan Perjalanan Pengguna

1. **Konfirmasi status otomatis.** Sistem menampilkan status kondisi terkini (normal, disfungsi terdeteksi) berdasarkan aturan dan persistence, tanpa perlu pelatihan.
2. **Peringatan berpengawas manusia.** Saat mesin peringatan mendeteksi pola yang mendahului kondisi memburuk, sistem menampilkan peringatan beserta waktu peringatan dan tingkat keyakinan; insinyur menindaklanjuti.
3. **Dasbor tren.** Skor kondisi dan indeks keausan ditampilkan sebagai tren sepanjang sumur untuk pemantauan, bukan sebagai keputusan otomatis.
4. **Keputusan manusia.** Seluruh keputusan pengeboran/pemeliharaan tetap pada insinyur; alat tidak menjadi satu-satunya dasar penghentian operasi.

---

# BAGIAN B: TINGKAT SOLUSI DAN TEKNIS

## 8. Data

### 8.1 Sumber dan Karakteristik Data

| Sumber | Isi | Peran |
|---|---|---|
| Lapangan Volve (Equinor, terbuka) | 8 CSV WITSML berbasis waktu (8.474.172 baris), USROP 198.928 baris × 12 sensor, 884 label peristiwa terkurasi dari laporan DDR | Data utama pelatihan dan evaluasi |
| Volume terbuka Databricks | 17.368 berkas; 20.086 XML WITSML mentah; 7.150 log XML; 192 tubular; 161 bhaRun; 63 trajectory; 8 mudLog; basis data EDM | Sumber label turunan dan penguatan well |
| Dataset eksternal terverifikasi | 4 dataset terunduh ulang dengan checksum cocok (termasuk percobaan keausan alat) | Data keausan alat dan validasi silang |

Seluruh volume telah dibuka dan dipetakan oleh delapan tim pembaca; peta komplit ada pada Lampiran A [A-16].

### 8.2 Variabel Target, Fitur, dan Pembagian Data

- **Tujuh kelas target** (dysfungsi/kerusakan) dengan populasi terhitung: getaran lateral, stick-slip torsional, keausan bit, stuck pipe, anomali hidraulik, getaran aksial, keausan mata bor.
- **Fitur** berupa statistik jendela waktu dari kanal sensor (mean, std, slope, last, fraksi) — 55 fitur dari 11 kanal MWD untuk mesin getaran, serta fitur turunan fisika (MSE, SSI, UCS) bila relevan.
- **Pembagian data**: *Leave-One-Wellbore-Out* (LOWO) antar sumur untuk mengukur generalisasi; kanal pembentuk label dilarang menjadi fitur (anti-sirkularitas).

### 8.3 Prapemrosesan

Imputasi nilai hilang (median) di-fit **hanya di dalam fold latih**; normalisasi bila diperlukan model; pembuangan jendela tanpa data disimetriskan antara latih dan uji; pemeriksaan kebocoran waktu (fitur selalu berstempel waktu lebih awal daripada peristiwa).

## 9. Metodologi

### 9.1 Pembingkaian Masalah

Pembingkaian mengikuti tugas tiap mesin. Tidak semua kegagalan diperlakukan sebagai "prediksi kejadian mendatang"; sebagian adalah deteksi anomali, deteksi kondisi, atau diagnosis. Pembingkaian yang tepat per tugas mencegah kesalahan paling umum: menuntut prediksi tanggal dari mesin yang sebenarnya mendeteksi kondisi.

### 9.2 Pemilihan dan Peran Model

| Model | Peran | Alasan |
|---|---|---|
| Aturan if-then & *canary* | Pembanding wajib per tugas | Menjawab apakah mesin menambah nilai di atas aturan sederhana; ditetapkan sebelum pengujian |
| *Persistence* (status-quo) | Pembanding status-quo | Menjawab jujur apakah model mengalahkan "keadaan berlanjut"; pada sebagian tugas *persistence* terbukti terbaik dan dicatat sebagai kemampuan |
| Deteksi statistik (median/MAD, change-point, skor-z) | Deteksi kondisi & pembentuk label | Mendeteksi perubahan pola operasi tanpa pelatihan |
| Regresi logistik | *Baseline* interpretable | Koefisien dapat dibaca sebagai pengaruh tiap fitur |
| *Random Forest* | Model utama | Tahan fitur berskala berbeda; sesuai fitur campuran |
| *Histogram-based Gradient Boosting* | Model utama kedua | Menguji apakah kinerja RF kebetulan |
| Mesin hibrida (aturan + statistik + ML) | Arsitektur dipilih | Tiap mesin memakai metode paling cocok untuk tugasnya |

*Deep learning* ujung-ke-ujung tidak dipakai karena jumlah unit positif per lipatan kecil (risiko peng-fittingan). Pencarian hiperparameter berskala luas sengaja tidak dilakukan karena meng-fittingkan model pada data uji; prinsip satu desain per kampanye diterapkan.

### 9.3 Protokol Pra-Registrasi

Sebelum tiap kampanye, ditetapkan dan diberi stempel waktu: desain eksperimen, syarat keterlibatan data, ambang keberhasilan, dan identitas pembanding. Ambang tidak diubah setelah hasil diketahui.

## 10. Pendekatan Teknis

| Komponen | Implementasi |
|---|---|
| Pipeline fitur | Skrip pembangunan dan skrip verifikasi terpisah |
| Kampanye evaluasi | Skrip kampanye dengan pembanding bawaan + verifier independen yang menghitung ulang dari berkas mentah |
| Pengujian kebocoran waktu | Pemeriksa menghitung stempel waktu setiap baris fitur terhadap peristiwa; pelanggaran tercatat |
| Determinisme | Benih acak tetap (42); pelaksanaan ulang wajib identik |
| Reproduksi klaim | Setiap angka dihitung ulang dari JSON primer oleh pemeriksa independen |
| Tata kelola | Papan kerja dengan pemisahan peran: pemeriksa data, insinyur data, insinyur ML, auditor independen, penilai akhir |

## 11. Strategi Validasi

### 11.1 *Leave-One-Wellbore-Out* (LOWO)

Model diuji dengan LOWO: dari tujuh sumur, enam untuk latih dan satu untuk uji, bergantian hingga semua sumur pernah jadi uji. Ini menjawab pertanyaan bisnis yang benar — apakah mesin berguna pada sumur yang belum pernah dilihat. Pembagian acak per-baris ditolak karena baris satu sumur saling berkorelasi (kedalaman, formasi, rig sama), sehingga metrik terangkat semu. LOWO memberi tujuh nilai lipatan sehingga dapat ditetapkan syarat kemenangan minimal, bukan rata-rata yang ditopang satu sumur besar. Seluruh prapemrosesan (termasuk imputasi) dihitung hanya dari data latih.

### 11.2 Penilaian Bertingkat Tiga Lapisan (A/B/C)

Bersamaan dengan LOWO, tiap mesin dinilai:

- **Lapisan A — Apakah deteksi bekerja?** Presisi, recall, tingkat alarm palsu, waktu deteksi, dibandingkan ke *baseline relevan* untuk tugas mesin itu (bukan satu baseline universal).
- **Lapisan B — Apakah bernilai pemeliharaan?** Adanya peringatan sebelum kondisi memburuk, lamanya waktu untuk bertindak, dan pengurangan pemeriksaan tidak perlu. Waktu peringatan terhadap kejadian nyata adalah ukuran kunci.
- **Lapisan C — Cukup tepercaya untuk dipakai?** Ketahanan hasil pada periode, kondisi operasi, dan peralatan berbeda; penanganan kualitas sensor dan ketidakpastian.

Keputusan akhir tiap mesin dinyatakan sebagai **batas pemakaian** (layak untuk tren, layak untuk peringatan berpengawas manusia, atau belum layak untuk alarm otomatis), bukan vonis tunggal lulus/tidak lulus. Mesin yang layak untuk tren tetapi belum untuk alarm kritis otomatis adalah keputusan wajar, bukan kegagalan.

### 11.3 Keterbatasan Validasi

Satu lapangan (generalisasi lintas lapangan tidak teruji). Label sebagian bersifat proxy. Pembagian waktu murni (latih masa lalu, uji masa depan) belum terpisah dari LOWO.

## 12. Alasan Pemilihan Metode

| Keputusan | Alternatif ditolak | Alasan |
|---|---|---|
| Metode dipilih per tugas | Satu metode untuk semua | Tiap kegagalan mengerjakan tugas berbeda; aturan/statistik dapat lebih cocok daripada ML |
| LOWO berbasis sumur | Pembagian acak baris | Baris satu sumur berkorelasi; pembagian acak menimbulkan kebocoran |
| Baseline relevan per tugas | Satu baseline universal | Kecocokan baseline mengikuti tugas (rule, persistence, statistik, canary) |
| AUPRC + presisi/recall/FAR | Akurasi tunggal | Akurasi menyesatkan pada kelas tak seimbang |
| Penilaian berlapis A/B/C | Satu ambang pakai/tidak-pakai | Menyembunyikan mesin yang bernilai untuk tugas lain |
| Pemisahan peran pemeriksa | Satu tim menilai karyanya sendiri | Mengendalikan bias evaluasi |

## 13. Metrik Evaluasi

| Metrik | Lapisan | Fungsi |
|---|---|---|
| AUPRC | A | Tahan ketidakseimbangan kelas |
| Presisi, recall, tingkat alarm palsu pada titik operasi praktis | A | Kejadian tertangkap dengan alarm keliru yang dapat ditangani |
| Waktu peringatan terhadap kejadian nyata | B | Waktu untuk bertindak |
| Ketahanan antar-periode/sumur/alat | C | Dapat dipercaya untuk dipakai |
| Kemenangan lipatan (mayoritas LOWO) | A | Konsistensi antarsumur |
| Baseline relevan per tugas | A/B | Nilai tambah di atas cara sederhana |
| Skor Brier & ECE | A | Kejujuran skor probabilistik |

Akurasi tunggal tidak dipakai sebagai penentu.

## 14. Arsitektur

| Lapisan | Komponen | Status |
|---|---|---|
| Data | Akuisisi volume, ekstraksi arsip, parsing WITSML → CSV | Selesai, teraudit |
| Fitur | Jendela waktu + baseline + metadata; pemeriksaan anti-bocor | Selesai |
| Mesin deteksi (7) | Aturan, statistik, persistence, ML terawasi, hibrida | Dievaluasi berlapis A/B/C |
| Lapisan penilaian | A (deteksi), B (nilai pemeliharaan), C (kepercayaan) | Diterapkan ketujuh mesin |
| Peta kemampuan | Kemampuan, batas, kekuatan bukti per mesin | Tersusun & diaudit (121 klaim, 0 fabrikasi) |
| Lapisan keputusan | Konfirmasi status · peringatan berpengawas manusia · dasbor tren | Rencana prototipe |
| Tata kelola | Papan lima peran, pra-registrasi, audit, penilaian | Berjalan |
| Penerapan | Belum dibangun | Rencana Tahap 1a–3a (§17) |

---

# BAGIAN C: KEMAMPUAN, RISIKO, DAN RENCANA

## 15. Peta Kemampuan dan Status Terkini

### 15.1 Peta Ketujuh Mesin

| Mesin | Jenis tugas | Jenis engine | Tingkat pemakaian terbukti | Batas (BELUM untuk) |
|---|---|---|---|---|
| Getaran lateral (whirl) | Deteksi kondisi + peringatan | Hibrida (rule + persistence + RF) | Peringatan bersyarat | Alarm otomatis (FAR belum terukur) |
| Stick-slip torsional | Deteksi kondisi + peringatan | Hibrida (rule + RF) | Peringatan bersyarat | Alarm otomatis (FAR belum terukur) |
| Getaran aksial (shock) | Peringatan dini | RF terawasi | Peringatan terbukti (lead beberapa menit) | Alarm otomatis; lead panjang |
| Stuck pipe | Peringatan + triage manual | Rule + statistik + RF | Peringatan terbukti, triage manual | Prediksi lintas-sumur tanpa kalibrasi |
| Anomali hidraulik | Deteksi kondisi | Statistik (median/MAD) + persistence | Indikasi dini (label lemah) | Prediksi kegagalan hidraulik independen |
| Keausan bit | Konfirmasi status / tren | RF + persistence + canary | Konfirmasi status terukur | Peringatan dini onset |
| Keausan mata bor | Perubahan regime | Change-point statistik + anomaly | Skor tren lintas-alat | Generalisasi ke alat belum dilihat |

### 15.2 Tingkat Pemakaian

- **Tingkat 1 — Pemantauan tren:** nilai terukur untuk mendeteksi kondisi/perubahan pola dibanding baseline relevan; ketidakpastian dinyatakan.
- **Tingkat 2 — Peringatan berpengawas manusia:** peringatan sebelum kondisi memburuk dengan waktu terukur dan alarm palsu yang dapat ditangani; keputusan akhir tetap manusia.
- **Tingkat 3 — Alarm otomatis kritis:** hanya setelah alarm palsu rendah terukur lintas periode/sumur dan validitas label terverifikasi. **Belum dicapai mesin mana pun; tidak diklaim.**

Dari tujuh mesin: **3 memenuhi Tingkat 2, 2 Tingkat 2 bersyarat, 2 Tingkat 1, dan 0 Tingkat 3** [A-19][A-20].

### 15.3 Kejujuran Batas

Ketujuh mesin dinyatakan dengan kemampuan **dan** batasnya. Tidak ada mesin yang diklaim melampaui buktinya. Audit independen menghitung ulang 121 klaim numerik dengan hasil 0 fabrikasi; enam selisih penyajian (median/rentang) tercatat dan tidak satu pun membalikkan tingkat pemakaian mesin mana pun [A-20]. Gap yang tersisa (pengukuran alarm palsu, validitas label lintas sumur, lead panjang, generalisasi lintas-alat) memblokir **ekspansi** tingkat pemakaian, bukan fungsi dasar alat.

## 16. Risiko dan Keterbatasan

| No. | Risiko | Dampak | Penanganan |
|---|---|---|---|
| R1 | Satu lapangan (Volve) | Generalisasi lintas lapangan tidak teruji | Dinyatakan sebagai keterbatasan muktamad |
| R2 | Label sebagian bersifat proxy | Membatasi metrik tertinggi | Dinyatakan terbuka; audit ketidakpastian label |
| R3 | Validitas label lintas sumur (kontrol positif stuck 0/10; label hidraulik proxy) | Ketidakpastian label = kekuatan bukti terendah | Dianotasi; jadi syarat sebelum naik tingkat |
| R4 | Alarm palsu belum terukur nyata untuk beberapa mesin | Membatasi kenaikan ke alarm otomatis | Diukur di Tahap 2a |
| R5 | Data petrofisik (DLIS/LAS) belum sepenuhnya diekstraksi | Fitur geologi belum termanfaatkan | Rencana |
| R6 | Pembagian temporal murni belum terpisah dari LOWO | Kebocoran waktu belum teruji terpisah | Rencana |
| R7 | Peng-fittingan akibat kampanye berulang | Pintu ke kesimpulan terpaksa | Dimitigasi pra-registrasi |

## 17. Rencana Penerapan dan Implementasi

1. **Tahap 1a: Prototipe advisori (dapat dimulai).** Tujuh mesin dengan batas pemakaian dipasang pada satu lapisan keputusan: konfirmasi status otomatis, peringatan berpengawas manusia pada sumur terkalibrasi, dasbor tren/skor. Tanpa alarm otomatis kritis.
2. **Tahap 2a: Pengukuran tingkat lanjut.** Mengukur tingkat alarm palsu nyata dan waktu peringatan pada sumur terkalibrasi sebagai syarat kenaikan tingkat pemakaian.
3. **Tahap 3a: Penguatan label.** Memperbaiki validitas label lintas sumur (R3) sebelum klaim dinaikkan ke alarm otomatis.
4. **Tahap 4a: Operasional (perlu persetujuan institusi).** Pemantauan berkelanjutan, umpan balik label, jadwal evaluasi ulang. Syarat mutlak: validasi di luar kumpulan Volve.

Pertimbangan etis: keputusan pemeliharaan tetap pada manusia; sistem tidak boleh menjadi satu-satunya dasar penghentian operasi; keterbatasan satu lapangan harus tercantum pada antarmuka.

## 18. Lini Masa

| Fase | Tonggak | Status |
|---|---|---|
| Sept 2026 | Pendataan awal: 1.759 laporan DDR, 884 label, gerbang kualitas data | Selesai |
| Okt 2026 | Akuisisi 17.368 berkas, parsing WITSML → 8 CSV | Selesai |
| Okt 2026 | Pembukaan seluruh volume Volve oleh 8 tim pembaca; taksonomi 7 jenis dengan populasi terhitung | Selesai |
| Okt 2026 | Riset ilmiah turunan label (Teale, SSI, MSE/DS, UCS) diuji di data Volve | Selesai |
| Okt 2026 | Penilaian berlapis A/B/C ketujuh mesin; peta kemampuan + audit 121 klaim | Selesai |
| Nov 2026 (rencana) | Prototipe advisori Tahap 1a; pengukuran alarm palsu Tahap 2a | Belum dimulai |
| Belum ditetapkan | Penyusunan naskah akhir PPT I (Bab II–IV), poster, sesi tinjauan dosen | Belum dimulai |

Riwayat terperinci tiap kampanye (termasuk yang tidak memenuhi ambang) ada di `CHANGELOG.md` [A-21].

## 19. Kriteria Keberhasilan

### 19.1 Kriteria Tingkat Pemakaian (Dipra-registrasikan)

1. **Tingkat 1 (tren):** mesin menunjukkan nilai terukur mendeteksi kondisi/perubahan pola dibanding baseline relevan; ketidakpastian dinyatakan.
2. **Tingkat 2 (peringatan berpengawas manusia):** mesin memberi peringatan sebelum kondisi memburuk dengan waktu terukur dan alarm palsu yang dapat ditangani; keputusan akhir manusia.
3. **Tingkat 3 (alarm otomatis kritis):** hanya setelah alarm palsu rendah terukur lintas periode/sumur dan validitas label terverifikasi. Belum dicapai; tidak diklaim.

*Status per 12 Oktober 2026: 3 mesin di Tingkat 2, 2 Tingkat 2 bersyarat, 2 Tingkat 1, 0 Tingkat 3 [A-19][A-20].*

### 19.2 Kriteria Proses

- Keputusan metodologis tercatat sebelum hasil, dengan stempel waktu.
- Hasil yang tidak memenuhi didokumentasikan apa adanya (terarsip di `CHANGELOG.md`).
- Tiap keluaran kerja mencantumkan rujukan riset pendahuluan (protokol internal).

### 19.3 Sitasi Dokumen Primer

| Kode | Dokumen | Berkas |
|---|---|---|
| [A-1] | Penilaian akhir V6: vonis SAH ">3 jenis kerusakan dari data nyata" (7 jenis, 3 lolos gate pra-reg) | `docs/V6_PM_VERDICT.md` |
| [A-2] | Desain + hasil kampanye ML tujuh kelas (4 pra-registrasi ber-hash) | `docs/V6_E1_ML_DESIGN.md`, `docs/V6_E1*_PREREG*.md` |
| [A-3] | Riset ilmiah pemecah buntu: rumus turunan label diuji di Volve | `docs/V6_R1_SCIENCE.md` |
| [A-4] | Pembukaan seluruh volume Volve oleh 8 tim pembaca + sintesis | `docs/V6_D0_READERS_SYNTHESIS.md`, `docs/V6_D1a..h_*.md` |
| [A-5] | Penilaian V7: solusi metode-sah (onset reframing, wellbore baru) | `docs/V7_PM_VERDICT.md` |
| [A-6] | Spesifikasi penilaian berlapis A/B/C + 7 profil kemampuan | `docs/V8_R1_ABC_SPEC.md`, `docs/V8_E_*_CAPABILITY.md` |
| [A-7] | Peta alat pemeliharaan berbasis prediksi (kemampuan+batas+bukti) | `docs/V8_M1_CAPABILITY_MAP.md` |
| [A-8] | Audit kemampuan (121 klaim, 0 fabrikasi) + penilaian akhir advisori | `docs/V8_A1_CAPABILITY_AUDIT.md`, `docs/V8_PM_VERDICT.md` |
| [A-9] | Inventaris akuisisi data & parsing WITSML | `docs/V3_DATA_ACQUISITION_INVENTORY.md`, `docs/V3_WITSML_PARSE_REPORT.md` |
| [A-10] | Laporan fitur time-series & pemeriksaan anti-bocor | `docs/V3_TS_FEATURES.md` |
| [A-11] | Kurasi label & audit ketidakpastian | `docs/V2_LABEL_CURATION.md`, `docs/V2_LABEL_AUDIT_UNCERTAIN.md` |
| [A-12] | Protokol riset internal & riwayat perubahan | `docs/PROTOCOL_RISET_TIM.md`, `CHANGELOG.md` |
| [A-13] | Dataset benchmark ROP (Tunkiel et al. 2021) | `Reference/Tunkiel et al. 2021…pdf` |

**Pernyataan keterbatasan isi.** Belum diverifikasi/dikerjakan: kuantifikasi biaya, silang-verifikasi zonasi waktu, ekstraksi penuh petrofisik, pembagian temporal murni. Seluruh angka kemampuan pada §15 berasal dari hitung ulang berkas primer per 12 Oktober 2026.

---

### PENGESAHAN

| Peran | Nama | Tanggal | Tanda Tangan |
|---|---|---|---|
| Penyusun | | | |
| Pemeriksa Teknis | | | |
| Penilai Akhir | | | |
| Dosen Pembimbing | | | |

---

### LAMPIRAN A: ARSIP BUKTI (RIWAYAT)

Lampiran ini bersifat internal. Riwayat pengembangan lengkap — termasuk seluruh kampanye evaluasi, hasil yang tidak memenuhi ambang, dan penilaian berturut-turut — tercatat pada `CHANGELOG.md` [A-12] dan dokumen kerja primer di atas. Arsip dipertahankan sebagai bukti transparansi; angka penutup kampanye lama tidak dihapus maupun diubah. Dokumen proposal ini sendiri hanya memuat solusi aktual.
