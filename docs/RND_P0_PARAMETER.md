# RND-P0: INVENTARIS PARAMETER ALAT PdM DAN APA YANG DIPERLUKAN UNTUK MENAIKKAN BUKTINYA

Kartu: `t_b90b3272` · Board: `rnd-algo-2026` · Tanggal: 2026-10-27 (WIB)
Workspace: `/mnt/d/Capstone 1(v2)` (folder arsip `/mnt/d/Capstone 1` tidak disentuh)
Ledger pendamping: `docs/RND_PROVENANCE_LEDGER.md` (39 baris, rujukan silang L-01 sampai L-39)

Riset pendahuluan: literature-review (pencarian standar dan literatur primer untuk getaran, stick-slip, MSE, dan statistik robust; setiap nomor standar/bagian diperiksa halaman resminya), scientific-critical-thinking (memisahkan "nilai yang bisa diturunkan" dari "ambang yang dipilih", serta menolak standar yang ruang lingkupnya tidak cocok meski topiknya mirip), verification-mandatory (setiap klaim pada dokumen ini menunjuk file dan baris kode atau DOI/URL yang benar-benar dibuka; yang tidak bisa dibuka ditulis belum terverifikasi dan tidak dipakai sebagai dasar rekomendasi).

Riset pendahuluan: sequentialthinking, 5 pikiran (`mcp__sequentialthinking__sequentialthinking`, thoughtNumber 1 sampai 5, `thoughtHistoryLength` = 5).

---

## 1. RINGKASAN TEMUAN

Dari 39 baris ledger, hanya 8 baris yang bersandar pada sumber eksternal kuat (5 STANDAR termasuk 2 turunan aritmetik, 3 JURNAL), 1 baris derivasi aritmetik murni, 6 baris adalah hasil eksekusi kita sendiri, dan 24 baris adalah KONVENSI internal. Artinya, klaim tingkat alat PdM ini sebagian besar berdiri di atas pilihan desain, bukan di atas ambang yang diterbitkan lembaga standar.

Tiga hasil yang paling menentukan arah riset berikutnya:

1. Angka 32,17405 bukan angka sembarang. Ia 1 g, dan sekarang dapat dikutip dengan nomor bagian: ISO 2041:2018 §3.1.4.
2. Ambang SSI >= 1 bukan selera. Ia batas bawah kelas "moderate stick-slip" pada kriteria grading yang diterbitkan (Liu et al. 2025, persamaan 2).
3. Ambang operasional (FAR <= 6 per 24 jam, <= 1 alarm/menit, horizon 10 menit) tidak punya padanan standar. Semuanya keputusan desain internal dan harus terus ditulis sebagai konvensi, bukan sebagai bukti ilmiah.

---

## 2. PETA ENGINE, KLAIM, DAN PARAMETER PENGGERAK

Alat PdM terdiri dari 7 engine dan 11 klaim (K-i/K-ii). Registry tier ada di `code/v9_i1_pipeline.py:74` (`REGISTRY = {`, dengan komentar sumber di `:72`), dan sumber tier per engine berupa rujukan dokumen (`docs/V9_EVAL_C_LAYERC.md`). Dokumen ini tidak mengubah tier apa pun.

| Engine | Klaim | Parameter penggerak utama | Baris ledger |
|---|---|---|---|
| vib | K-i (status getaran lateral) | 32,17405 ft/s²; jendela 10 menit; FAR <= 6 konvensi | L-01, L-29, L-26 |
| ssi | K-i (status stick-slip torsional) | SSI >= 1; SSI_MIN_SAMPLES 10 | L-04, L-05, L-07 |
| shk | K-i (status bit bounce) | SHKRSK_RT >= 1 | L-08 |
| stuck | K-i (status) | stuck_max >= 1 | L-09 |
| stuck | K-ii (onset) | z(TQA) > 2; z(HKLD) > 2; ROP drop >= 30%; jendela 60 menit; E1_MIN_OBS 10; Z_SCALE 0,6745 | L-10, L-11, L-12, L-13, L-14, L-15 |
| hyd | K-i (status) | abs(z) > 2; qcut TFLO 10 bin; min 50 bin | L-17, L-18, L-19 |
| hyd | K-ii (prediksi) | horizon 10 menit; sustain 5 menit; merge 30 menit; syarat sirkulasi | L-28 |
| bit_wear | K-1 (status) | MSE > P75 | L-20 |
| bit_wear | K-2 (onset) | belum dijalankan, tidak ada parameter aktif | tidak ada |
| tool_wear | K-i (regime bengkel) | 5 dari 27 fitur; abs(z) > 3; kalibrasi 30%; min 5 jendela; target 1 alarm/menit | L-21, L-22, L-23, L-24, L-25 |
| tool_wear | K-ii (lintas alat) | ranking 3-RMS dengan abs(z) >= 3 sebagai ilustrasi skor | L-22 |

Catatan: `hyd` K-ii pada prototipe ditandai "BELUM TERSEDIA" (`code/v9_i1_pipeline.py`, head `k2_tidak_tersedia`), sehingga yang aktif hanyalah basis aturan z-pit di `code/v9_e_RULE_04_hyd_k2.py`.

---

## 3. INVENTARIS PARAMETER: NILAI, LOKASI, KELAS BUKTI, DAN JALAN MENAIKKAN

Format tiap baris: nilai dan satuan · sumber saat ini (file:baris) · kelas bukti · apa yang diperlukan agar naik jadi bukti kuat.

### 3.1 vib

**VIB_THRESH = 32,17405 ft/s²**
- Sumber: `code/v9_d1_02_rig_windows.py:35` (definisi label) dan `code/v9_e_RULE_01_status.py:49` (aturan display), dipakai sebagai pembanding `vib_max >= VIB_THRESH` di `code/v9_d1_02_rig_windows.py:42`.
- Kelas: STANDAR untuk konversi satuannya (L-01, L-02, L-03). Yang terverifikasi adalah bahwa 32,17405 ft/s² = 1 g, bukan bahwa 1 g adalah ambang kerusakan.
- Yang masih perlu: pemisahan tegas dua hal. (a) Satuan kanal: apakah `VIBLAT_RT` memang terkalibrasi dalam g atau dalam ft/s². Bukti yang dibutuhkan: dokumentasi kalibrasi sensor atau manual tool downhole. Tanpa ini, pemakaian 1 g sebagai batas label hanya konvensi pembulatan satuan. (b) Ambang severity: bila ingin mengklaim 1 g sebagai batas bahaya, rujukan primer yang tersedia (Reckmann et al. 2010, SPE-127413-MS) membahas vibrasi lateral kumulatif terhadap kegagalan tool, tetapi angka ambangnya ada di teks berbayar yang belum saya buka, sehingga BELUM-TERVERIFIKASI.
- Catatan teknis: ISO 2041:2018 Note 2 menulis ≈ 32,174 0 ft/s² (4 desimal), sedangkan kode memakai 32,17405 (5 desimal). Konversi eksak 9,80665 × 3,280839895 = 32,1740486. Selisih 5·10⁻⁵ ft/s² tidak berdampak pada keputusan, tetapi sebaiknya diseragamkan agar angka di dokumen dan kode identik.

### 3.2 ssi

**SSI >= 1**
- Sumber: `code/v9_d1_02_rig_windows.py:96` (label) dan `code/v9_e_RULE_01_status.py:203` serta `:260` (display).
- Rumus: `(max − min) / (2 × mean)` pada `code/v9_d1_02_rig_windows.py:92`.
- Kelas: JURNAL, terverifikasi (L-04, L-05). Liu et al. 2025 persamaan (2): SSI < 1 torsional vibration, 1 <= SSI < 3 moderate stick-slip, SSI >= 3 severe stick-slip.
- Turunan tambahan: untuk kasus ideal RPM_min = 0 dan mean = (max+min)/2, rumus menghasilkan SSI = 1 tepat, apa pun nilai mean-nya (diuji pada mean 50, 80, 120 RPM). Jadi 1 bermakna "bit berhenti penuh pada tiap siklus" untuk idealisasi sinusoidal (L-06). Asumsi midrange ini harus ditulis bila dipakai sebagai penjelasan fisik.
- Yang masih perlu untuk naik ke bukti kuat di konteks sumur Volve: verifikasi bahwa `CRPM_RT` adalah RPM downhole (bukan surface RPM). Liu et al. memakai data downhole; bila kanal kita surface, SSI akan under-estimate dan ambang 1 menjadi terlalu longgar.

**SSI_MIN_SAMPLES = 10**
- Sumber: `code/v9_d1_02_rig_windows.py:34` dan `code/v9_e_RULE_01_status.py:50`.
- Kelas: KONVENSI (L-07).
- Yang perlu: analisis sensitivitas jumlah sampel minimum terhadap nilai SSI dan terhadap laju nodata (nodata CRPM tercatat 62,3% di EVAL_C). Keluaran yang dibutuhkan: kurva SSI dan FAR sebagai fungsi ambang sampel (5, 10, 20, 30) pada well yang sama. Bila hasilnya datar, 10 boleh dipertahankan sebagai pilihan murah; bila tidak datar, ambang harus ditetapkan dari kurva, bukan dari kebiasaan.

### 3.3 shk

**SHKRSK_RT >= 1**
- Sumber: `code/v9_e_RULE_01_status.py:180`; definisi label `code/v9_d1_02_rig_windows.py:42`.
- Kelas: KONVENSI (L-08). Kanal ini bersifat diskret/hitungan kejadian dari vendor, sehingga ambang 1 berarti "ada kejadian", bukan ambang fisik.
- Yang perlu: definisi resmi kanal dari dokumentasi tool (apakah SHKRSK_RT hitungan per interval, dan panjang intervalnya). Tanpa itu, ">= 1" tidak dapat dibandingkan dengan literatur bit bounce.

### 3.4 stuck K-i

**stuck_max >= 1**
- Sumber: `code/v9_e_RULE_01_status.py:181`; label `code/v9_d1_02_rig_windows.py:41`.
- Kelas: KONVENSI (L-09), sama seperti shk: kanal diskret.
- Yang perlu: dokumentasi kanal `STUCK_RT` (interval, satuan) dan pembanding literatur deteksi stuck pipe berbasis surface data (mis. perubahan torsi dan drag). Parameter ini juga penyebab utama sirkularitas bila label dan aturan memakai kanal yang sama, sehingga audit leakage (kartu E0) wajib mendahului kenaikan tier.

### 3.5 stuck K-ii (E1 2-dari-3)

**z(TQA) > 2 dan z(HKLD) > 2**
- Sumber: `code/v9_e_RULE_01_status.py:326` dan `:327`; skala z lewat `Z_SCALE` di `:54`, dipakai `:319` dan `:320`.
- Kelas: KONVENSI (L-10, L-11). Tidak ada standar yang menetapkan 2 sigma untuk hook load atau torque sebagai penanda stuck.
- Yang perlu: kurva sensitivity terhadap ambang z (1,5 / 2 / 2,5 / 3) dengan metrik B1 dan FAR pada well yang sama, lalu pemilihan ambang dari kurva itu. Butuh juga pembanding literatur deteksi stuck berbasis wireline/surface; bila tidak ditemukan, tulis sebagai konvensi yang diuji, bukan konvensi yang diwarisi.

**ROP drop >= 30%**
- Sumber: `code/v9_e_RULE_01_status.py:55` (`ROP_DROP = 0.30`), dipakai `:328` sebagai `ROP <= 0,7 × median60`.
- Kelas: KONVENSI (L-12).
- Yang perlu: distribusi penurunan ROP pada onset stuck yang teranotasi (bukan pada menit acak). Bila penurunan pada 90% onset memang di atas 30%, angka ini punya dukungan empiris internal dan bisa naik jadi RUN-KITA. Selama belum dihitung, statusnya tetap konvensi.

**Jendela median/MAD 60 menit dan E1_MIN_OBS 10**
- Sumber: `code/v9_e_RULE_01_status.py:52` dan `:53`, dipakai `:314`.
- Kelas: KONVENSI (L-13, L-14).
- Yang perlu: waktu karakteristik onset stuck terukur (EVAL_C menyebut lead time 4,5 sampai 8,5 menit dan anchor onset 2,67 sampai 7,37 menit). Bila skala onset memang menit, jendela 60 menit wajar sebagai basis pembanding; tetapi angka 60 sendiri harus diuji dengan variasi (30 / 60 / 120) terhadap B1 dan FAR.

**Z_SCALE 0,6745**
- Sumber: `code/v9_e_RULE_01_status.py:54`, dipakai `:319` dan `:320`.
- Kelas: STANDAR sebagai aritmetika (L-15). 0,6745 = Φ⁻¹(0,75) = 0,6744898; kebalikan 1,4826.
- Catatan penting: komentar kode mengatribusikan angka ini ke "NIST, R1 [7][8]". Halaman NIST §1.3.5.6 yang saya buka mendefinisikan MAD dan sifat robustnya, tetapi tidak mencetak 0,6745 maupun 1,4826. Atribusi NIST pada komentar itu karena itu belum terbukti; yang terbukti adalah turunan aritmetiknya.
- Yang perlu: tidak ada untuk nilai; yang perlu hanya perbaikan atribusi di komentar kode agar tidak mengklaim sumber yang tidak memuatnya.

### 3.6 hyd K-i

**abs(z) > 2 pada SPPA, setelah normalisasi qcut(TFLO, 10)**
- Sumber: `code/v9_d1_03_rig_datasets.py:69` dan `:70` (label), `code/v9_e_RULE_01_status.py:224` dan `:225` (display); jumlah bin `code/v9_d1_03_rig_datasets.py:28` dan `:63`, `code/v9_e_RULE_01_status.py:217`; syarat minimal 50 bin `code/v9_d1_03_rig_datasets.py:61`.
- Kelas: KONVENSI (L-17, L-18, L-19).
- Yang perlu: pembanding fisik. SPPA (standpipe pressure) bergantung pada laju alir, sehingga normalisasi per bin TFLO adalah pilihan yang wajar, tetapi jumlah bin 10 tidak diuji. Keluaran yang dibutuhkan: sensitivitas jumlah bin (5 / 10 / 20) terhadap prevalensi label dan AUPRC; bila label berubah banyak, jumlah bin adalah parameter model yang harus dilaporkan di bab metodologi. Untuk ambang 2 sigma, sama seperti E1: butuh kurva sensitivitas, bukan standar.

### 3.7 bit_wear K-1

**MSE > P75**
- Sumber: ambang di `code/06_xgb_fuzzy.py:77` (`np.percentile(mse[mse > 0], 75)`); audit label di `code/10_audit_maintenance_claim.py:86`.
- Kelas: JURNAL untuk rumus MSE (Teale 1965, DOI 10.1016/0148-9062(65)90022-7, terkonfirmasi Crossref, L-20); BELUM untuk ambang P75 karena Teale mendefinisikan specific energy, bukan kuantil ke-75.
- Yang perlu: (a) alasan pemilihan P75 (mengapa bukan P80 atau ambang berbasis CCS), (b) pengakuan eksplisit bahwa label yang didefinisikan dari kuantil akan memaksa prevalensi 25% secara desain, sehingga metrik presisi/recall berbagi basis dengan definisi label. Ini masalah sirkularitas yang harus ditangani di kartu E0, bukan ditutupi dengan angka FAR.

### 3.8 tool_wear K-i (domain bengkel, jendela 1 detik)

**>= 5 dari 27 fitur dengan abs(z) > 3, kalibrasi 30% awal, minimal 5 jendela kalibrasi**
- Sumber: `code/v9_e_STAT_03_tool_wear.py:40` (`CAL_FRAC, Z_THR, N_FEAT_ALARM = 0.30, 3.0, 5`), `:195`, `:203`, `:206`; `code/v9_i1_pipeline.py:605` (asersi 27 fitur), `:616`, `:619`, `:624`, `:627`.
- Kelas: KONVENSI seluruhnya (L-21, L-22, L-23, L-24). Jumlah 27 fitur bukan pilihan statistik tetapi konsekuensi jumlah fitur yang diekstrak dari sinyal getaran.
- Yang perlu: (a) uji jumlah fitur alarm (3 / 5 / 8) terhadap presisi dan lead time per alat; (b) uji panjang jendela kalibrasi (20% / 30% / 50% run R01) terhadap pergeseran ambang, karena kalibrasi 30% mengasumsikan rezim awal bebas keausan, asumsi yang perlu dibuktikan; (c) pernyataan bahwa abs(z) > 3 adalah konvensi statistik (aturan 3 sigma), bukan ambang keausan terbit.

**Target <= 1 alarm/menit**
- Sumber: `code/v9_i1_pipeline.py:612` (`TARGET_FP_PER_MIN = 1.0`), dipakai `:631`.
- Kelas: KONVENSI (L-25). Ini target desain titik operasi, bukan hasil ukur dan bukan standar.
- Yang perlu: beban pemeriksaan nyata di bengkel (berapa alarm per shift yang bisa ditangani). Tanpa data itu, angka 1 hanya asumsi. Hasil run yang ada menunjukkan FP 1 sampai 3 per alat pada target ini (L-33), sehingga klaim yang jujur adalah "sesuai target", bukan "FAR rendah".

### 3.9 Parameter lintas engine

**Panjang jendela 10 menit dan horizon 10 menit**
- Sumber: `code/v9_d1_02_rig_windows.py:31` (`W = 10`), `code/v9_e_RULE_01_status.py:51` (`W = 10`), `code/v9_e_RULE_04_hyd_k2.py:30` (`H = 10`).
- Kelas: KONVENSI (L-28, L-29).
- Yang perlu: justifikasi panjang jendela dari laju sampling kanal dan dari skala waktu onset yang terukur, bukan dari kebiasaan. Data yang tersedia (lead time stuck 4,5 sampai 8,5 menit) hanya menunjukkan bahwa 10 menit sebanding, bukan bahwa 10 menit optimal. Uji pembeda: ulang evaluasi dengan jendela 5 dan 15 menit pada well yang sama.

**FAR <= 6 per 24 jam dan rumus FAR**
- Sumber: gerbang di `docs/RND_ALGO_RESEARCH_PLAN.md` §6 butir 2; implementasi gerbang `code/v9_eval_a_01_compute.py:37` dan `:108`; rumus `code/v9_i1_pipeline.py:307` sampai `:325`.
- Kelas: KONVENSI untuk ambang (L-26); TERVERIFIKASI sebagai kode untuk rumusnya (L-27).
- Yang perlu: rujukan operasional yang bisa dikutip (mis. praktik alarm management seperti EEMUA 191 atau ISA 18.2 untuk laju alarm yang dapat ditangani operator). Keduanya belum saya buka, jadi sekarang masih BELUM-TERVERIFIKASI dan tidak boleh dikutip sebagai dasar. Bila nanti diverifikasi, FAR <= 6 perlu dipetakan ke satuan standar itu (alarm per jam per operator), bukan disamakan begitu saja.

**MIN_DRILL_BINS 5 dan MIN_DRILL_ROWS 60**
- Sumber: `code/v9_d1_02_rig_windows.py:32` dan `:33`.
- Kelas: KONVENSI (L-30).
- Yang perlu: analisis berapa banyak jendela yang gugur karena syarat ini per well, dan apakah jendela yang gugur berbeda karakter (mis. saat connection) sehingga menimbulkan bias seleksi.

---

## 4. STANDAR: YANG DIPAKAI DAN YANG DITOLAK

### 4.1 Dipakai

**ISO 2041:2018, Mechanical vibration, shock and condition monitoring: Vocabulary, §3.1.4.**
Isi terverifikasi: "standard acceleration due to gravity, gn: 9,806 65 m/s²"; Note 1 menyatakan nilai diadopsi 1901 oleh Resolusi CGPM ke-3; Note 2 menyebut ≈ 386,089 in/s² dan ≈ 32,174 0 ft/s².
Kegunaan: menutup pertanyaan asal 32,17405 ft/s². Ini juga menutup klaim "1 g" sebagai satuan, bukan sebagai ambang.

**NIST/SEMATECH e-Handbook of Statistical Methods §1.3.5.6, Measures of Scale.**
Isi terverifikasi: definisi median absolute deviation dan argumen robustness terhadap ekor distribusi. Tidak memuat konstanta 1,4826.
Kegunaan: dasar definisi MAD yang dipakai semua z robust di engine (hyd, stuck E1, tool_wear). Konstanta penyekala dihitung sendiri (1/0,67449 = 1,4826), bukan dikutip.

### 4.2 Ditolak sebagai dasar ambang

**ISO 20816-1:2016, Mechanical vibration: Measurement and evaluation of machine vibration, Part 1: General guidelines.**
Alasan penolakan, dari §1 Scope pada pratinjau resmi: berlakunya untuk pengukuran pada bagian berputar dan tidak berputar dari mesin lengkap (poros, rumah bantalan), dan secara eksplisit "does not include consideration of torsional vibration". Catatan §1 juga merujuk getaran torsional ke ISO 3046-5, ISO 22266-1, atau VDI 2039.
Konsekuensi: standar ini tidak bisa dipakai untuk membenarkan VIB_THRESH (kanal getaran lateral downhole, bukan rumah bantalan mesin permukaan) maupun SSI (torsional, yang justru dinyatakan di luar lingkup).

**API RP 7G, Recommended Practice for Drill Stem Design and Operating Limits, edisi 16.**
Alasan penolakan: ruang lingkup terverifikasi adalah desain drill stem dan batas operasi aman. Tidak ditemukan klausul ambang severity getaran atau stick-slip. Teks penuh berbayar dan tidak dibuka, sehingga nomor klausul tidak dapat dikutip; karena itu standar ini hanya dicatat sebagai "tidak memberi ambang", bukan dipakai sebagai rujukan.

### 4.3 Konsekuensi jujur

Tidak ada standar ISO atau API yang, sejauh yang dapat diverifikasi hari ini, menerbitkan ambang numerik untuk stick-slip severity atau getaran lateral drillstring. Ambang yang kita pakai untuk SSI berasal dari literatur jurnal (Liu et al. 2025), sedangkan ambang getaran lateral kita tetap konvensi internal sampai angka dari literatur primer (Reckmann et al. 2010 dan turunannya) benar-benar dibuka.

---

## 5. REKOMENDASI (HANYA YANG BERSANDAR BUKTI TERVERIFIKASI)

Rekomendasi ini tidak mengubah ambang apa pun. Semua bersifat dokumentasi dan pengujian, sesuai larangan plan §9 ("tidak mengubah ambang engine yang sudah ada tanpa bukti pilot").

1. Perbaiki sitasi di dokumen dan komentar kode: 32,17405 ft/s² dikutip ke ISO 2041:2018 §3.1.4, bukan sebagai "1 g" tanpa sumber. Sekaligus seragamkan jumlah desimal (32,17405 di kode, 32,174 0 di standar) dengan satu catatan konversi.
2. Pertahankan SSI >= 1, sekarang dengan dasar jurnal yang jelas (Liu et al. 2025 persamaan 2), dan tambahkan satu kalimat di metodologi bahwa ambang 3 adalah batas kelas "severe" yang belum kita pakai.
3. Hapus atau koreksi atribusi NIST pada `Z_SCALE` di `code/v9_e_RULE_01_status.py:54`; ganti dengan "Φ⁻¹(0,75), turunan 1/1,4826". Ini perbaikan kejujuran sumber, bukan perubahan perilaku kode.
4. Untuk semua ambang KONVENSI, jalankan satu protokol sensitivitas yang sama (ambang x 3 nilai, well yang sama, metrik B1 dan FAR). Prioritas: ROP drop 30%, z > 2 pada E1, abs(z) > 2 pada hyd, 5/27 fitur tool_wear. Tanpa protokol ini, ambang tidak boleh naik tier.
5. Jangan memakai ISO 20816-1 atau API RP 7G sebagai pembenaran ambang apa pun. Bila penguji eksternal menanyakannya, jawabannya: ruang lingkup tidak cocok, dan itu sudah dicatat dengan nomor bagian.

---

## 6. YANG BELUM TERVERIFIKASI

1. `BELUM-TERVERIFIKASI`: angka ambang akselerasi lateral 25 g untuk keandalan MWD/LWD. Sumber terbaca hanya glosarium vendor yang mengutip Reckmann et al. (2010); teks penuh SPE-127413-MS berbayar.
2. `BELUM-TERVERIFIKASI`: klausul apa pun di dalam API RP 7G (hanya judul, edisi, dan ruang lingkup umum yang terverifikasi).
3. `BELUM-TERVERIFIKASI`: klausul tepat ISO 80000-3:2019 yang memuat gn (nilai gn sendiri terverifikasi lewat ISO 2041:2018 §3.1.4).
4. `BELUM-TERVERIFIKASI`: atribusi 0,6745 dan 1,4826 ke NIST. Halaman NIST §1.3.5.6 mendefinisikan MAD tetapi tidak mencetak kedua angka itu.
5. `BELUM-TERVERIFIKASI`: rujukan praktik alarm management (EEMUA 191, ISA 18.2) untuk memetakan FAR <= 6 dan <= 1 alarm/menit ke satuan standar. Belum dibuka, sehingga tidak dipakai.
6. `BELUM-TERVERIFIKASI`: DOI Hegde et al. (2019) yang hanya dikenal sebagai sitasi sekunder.
7. `BELUM`: 19 parameter KONVENSI tanpa dasar eksternal (daftar lengkap di `docs/RND_PROVENANCE_LEDGER.md` §4 dan §5 butir 5).
8. `BELUM`: kalibrasi kanal. Belum ada bukti bahwa `VIBLAT_RT` dalam g atau ft/s², dan belum ada bukti bahwa `CRPM_RT` adalah RPM downhole. Kedua hal ini menentukan apakah ambang 1 g dan SSI >= 1 bermakna sama seperti di literatur.
9. `BELUM`: sensitivitas seluruh ambang konvensi. Protokol di §5 butir 4 belum dijalankan.

## Ringkasan 5 baris

1. Dari 39 baris ledger: 5 STANDAR, 3 JURNAL, 1 derivasi aritmetik, 6 RUN-KITA, 24 KONVENSI, 0 angka karangan.
2. 32,17405 ft/s² terverifikasi sebagai 1 g lewat ISO 2041:2018 §3.1.4; SSI >= 1 terverifikasi lewat Liu et al. 2025 persamaan 2; keduanya sekarang punya nomor bagian, bukan hanya nama.
3. ISO 20816-1:2016 dan API RP 7G ditolak sebagai dasar ambang karena ruang lingkupnya berbeda, dan alasan itu dicatat dengan nomor bagian.
4. Semua ambang operasional (FAR <= 6/24 jam, <= 1 alarm/menit, horizon dan jendela 10 menit, 30% kalibrasi, 5/27 fitur) tetap konvensi dan wajib diuji sensitivitas sebelum dipakai menaikkan tier.
5. Dua celah terbesar yang menghambat kenaikan bukti adalah kalibrasi satuan kanal (g lawan ft/s², surface lawan downhole) dan teks penuh literatur berbayar (SPE-127413-MS, API RP 7G).
