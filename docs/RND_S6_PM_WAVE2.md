# RND-S6: VONIS PM GELOMBANG 2 DAN PEMILIHAN KOMPOSISI TERBAIK

Status: LENGKAP. Sembilan bagian terisi, tidak ada bagian kosong.
Kartu: t_b5830542. Induk: t_b5b16adc (RND-S5).
Bahan: hasil run S6 di `scratch/rnd/s6/`, ditambah `scratch/rnd/s6_digest.md` yang mengutip angka dari S1 sampai S5, PM, R8, dan POL.

Riset pendahuluan: scientific-critical-thinking, statistical-analysis, verification-mandatory.

Aturan angka: titik desimal, tanpa pemisah ribuan. Angka 23.922 pada dokumen sumber ditulis 23922 di sini.
Baris ledger baru memakai prefiks `S6-`, dan blok itu sudah ada di `docs/RND_PROVENANCE_LEDGER.md`: header bagian di baris 3228, lalu 191 baris data `S6-001` sampai `S6-191`, dengan berkas berakhir di baris 3425.

---

## 1. Mandat, bahan, dan cara membaca vonis

Mandat user, dikutip apa adanya: "Intinya pilih yang terbaik. Bisa saja yang sebelum riset R&D ini hasilnya
lebih baik, tapi bisa saja setelah riset adalah yang terbaik. Atau barangkali S6 bisa menghasilkan algoritma
yang lebih baik dari angka lintas seed? Intinya saya setuju. Semuanya untuk performa terbaik alat ini."

Mandat itu menuntut tiga hal yang harus dijawab dengan angka: apakah kandidat pra-riset lebih baik, apakah
kandidat pasca-riset lebih baik, dan apakah S6 sendiri dapat melahirkan kandidat yang lebih baik. Ketiganya
dijawab di bawah, dan jawabannya tidak seragam antar kelas.

Tiga kolom yang dipakai di seluruh dokumen, dengan pemetaan bahan yang eksplisit:

| Kolom | Isi | Sumber angka |
|---|---|---|
| Pra-riset | konfigurasi detektor sebelum gelombang riset, beserta tier yang berlaku | `docs/V9_EVAL_C_LAYERC.md` dan `scratch/v9_i1/v9_i1_RESULTS.json`, dibaca ulang di S1 bagian 7 |
| Gelombang 1 | empat uji hybrid R8 dengan baseline per tugas, lalu vonis PM | `docs/RND_R8_EVALUASI_BERLAPIS.md` bagian 8 dan 9, `docs/RND_PM_VERDICT.md` bagian 3 dan 4 |
| Gelombang 2 | lima kartu S1 sampai S5, ditambah run S6 pada kartu ini | `docs/RND_S1_SEED_ROBUSTNESS.md` sampai `docs/RND_S5_AUDIT_WAVE2.md`, dan `scratch/rnd/s6/s6_kandidat.json` |

### 1.1 Apa yang benar-benar dijalankan kartu ini

Kartu ini tidak berhenti pada sintesis dokumen. Pada 2026-10-28 07:44:57 dijalankan harness bersama
`code/rnd_hybrid_harness.py` selama 170,4 detik dengan Python 3.11.15, pandas 3.1.0, dan numpy 2.4.6, pada tiga
kelas dan dua seed, dengan anggaran alarm `alpha = 6/1440` per menit, ambang gate FAR maksimum 6 per 24 jam, dan
recall minimum 0,5. Keluarannya ada di `scratch/rnd/s6/s6_kandidat.json` (371 KB, 141 record: 63 hyd, 24 vib,
54 ssi per seed) dan ringkasannya di `scratch/rnd/s6/s6_verifikasi.json`.

Yang diuji adalah dua komposisi baru yang belum pernah dijalankan sebelumnya pada seluruh kelas:

| Kode | Komposisi | Alasan diuji |
|---|---|---|
| H1p | rule kanal DAN gerbang persistence | S1 bagian 7 menunjukkan komposisi pra-riset ini mengalahkan H1 pada segmen F-14 |
| H1p3 | rule kanal DAN persistence DAN statistik | menguji apakah penambahan gerbang ketiga memperbaiki beban alarm |

Empat lapis pemeriksaan yang menyertai run itu, semuanya bisa diperiksa ulang:

1. Reproduksi angka terbit R8: 30 pemeriksaan bernama, 30 lulus, termasuk H1 FP 935 lawan `R8-001`, TP 3804
   lawan `R8-006`, presisi 0,778947 lawan 0,7789, recall 0,563815 lawan 0,5638, FAR 3,5302 lawan `R8-012`,
   lead 11,5 lawan `R8-016`, dan 219 onset lawan `R8-018`. Angka rule juga cocok: FP 2105 dan TP 5579.
2. Reproduksi angka S2: seluruh model vib dan ssi berstatus COCOK, dan `galat_reproduksi_s2` kosong.
3. Pemeriksaan seed: `beda_sel` 0 pada 45 sel hyd, 20 sel vib, dan 45 sel ssi, yaitu tiga komposisi per kelas,
   sehingga komposisi deterministik ini memang menghasilkan angka identik di seed 42 dan seed 13.
4. Kontrol negatif: kontrol ML berubah di 2 dari 2 fold antar seed, yaitu F-14 dari 362 FP dan 42 TP menjadi 534
   FP dan 71 TP, dan F-5 dari 61 FP dan 69 TP menjadi 128 FP dan 74 TP. Artinya harness ini bisa berubah karena
   seed ketika memang ada komponen acak, sehingga hasil identik pada komposisi deterministik bukan efek harness
   yang mengabaikan seed.

Tanpa kontrol negatif nomor empat, klaim "identik antar seed" tidak sah, karena alat yang selalu memberi angka
sama juga akan memberi hasil identik.

5. Blok ledger `S6-` diuji ulang terhadap artefak, bukan dipercaya karena dibuat oleh run sebelumnya. Hasilnya:
   147 sel angka cocok persis ke path JSON, 4 baris yang rujukannya berupa prosa, yaitu jumlah rekaman 63 hyd, 24
   vib, 54 ssi, dan panjang galat 0, diperiksa manual dan cocok, sedangkan 40 baris sisanya bukan sel angka
   tunggal sehingga tidak diuji mesin. Satu jebakan yang perlu dicatat: `s6_verifikasi.json` memakai nama kunci
   `presisi_median` sedangkan `s6_kandidat.json` memakai `precision_median`, sehingga resolver yang memakai satu
   nama kunci saja akan melaporkan 16 baris ledger seolah rusak padahal nilainya benar.

### 1.2 Dua aturan yang mengikat seluruh vonis

1. Adopsi bukan kenaikan tier (`docs/RND_PM_VERDICT.md` baris 154 sampai 157). Syarat naik tier tetap tiga
   sekaligus: lapisan C stabil, lapisan A dengan FAR di bawah 6 per 24 jam pada titik operasi, dan lapisan B
   berupa beban pemeriksaan manusia yang dapat diterima.
2. Hasil gelombang 2 tidak boleh menaikkan tier sebelum ketiga syarat itu terpenuhi bersamaan
   (`docs/RND_PM_VERDICT.md` baris 282 sampai 283). Hasil negatif wajib ditulis sebagai temuan, bukan disimpan.

---

## 2. Perbandingan tiga kolom: pra-riset, gelombang 1, gelombang 2

### 2.1 hyd K-i, mode peringatan dini

Ini satu-satunya kelas yang punya angka pada ketiga kolom dengan penyebut yang sama, yaitu 9 fold dan 390 onset.
Sumber kolom gelombang 2: `s6_verifikasi.json` bagian `ringkas`, dan `s6_kandidat.json` bagian `records`.

| Ukuran | Pra-riset (V9) | Gelombang 1 (R8, seed 42) | Gelombang 2 (S1 lintas seed, dan S6 untuk kandidat baru) |
|---|---|---|---|
| Komposisi | rule kanal, dengan hybrid rule DAN persistence pada segmen F-14 | H1: rule kanal DAN CUSUM residu | H1 diulang lima seed, lalu H1p dan H1p3 diuji dua seed |
| FP | 368 pada F-14 (S1 baris 219); hybrid pra-riset F-14 FP 110 (baris 232) | 935 | H1 935; H1p 927; H1p3 568 |
| TP | 607 pada F-14; hybrid pra-riset F-14 TP 516 | 3804 | H1 3804; H1p 4924; H1p3 3557 |
| Presisi median | 0,6226 rule F-14; 0,8243 hybrid pra-riset F-14 | 0,7789 | H1 0,7789; H1p 0,8243; H1p3 0,8646 |
| Recall median | 0,7017 rule F-14; 0,5965 hybrid pra-riset F-14 | 0,5638 | H1 0,5638; H1p 0,6519; H1p3 0,5296 |
| FAR median per 24 jam kalender | tidak dilaporkan V9 pada satuan ini | 3,5302 | H1 3,5302; H1p 4,0984; H1p3 2,0323 |
| FAR median per 24 jam baris | 55,57 rule F-14; 16,611 hybrid pra-riset F-14 | 32,256 | H1 32,256; H1p 28,416; H1p3 18,4683 |
| Lead median | tidak dilaporkan per fold di V9 | 11,5 menit | H1 11,5; H1p 8,0; H1p3 12,5 menit |
| Onset diperingatkan dari 390 | tidak dilaporkan per fold di V9 | 219 | H1 219; H1p 218; H1p3 183 |
| Fold dengan FAR tidak lebih dari 6 | tidak dilaporkan | 7 dari 9 | H1 7; H1p 7; H1p3 9 dari 9 |
| Fold dengan recall minimal 0,5 | tidak dilaporkan | 6 dari 9 | H1 6; H1p 9; H1p3 5 dari 9 |
| Fold memenuhi FAR dan recall sekaligus | tidak dilaporkan | 5 dari 9 | H1 5; H1p 7; H1p3 5 dari 9 |

Empat baris terakhir adalah hitungan penulis dokumen ini langsung dari `s6_kandidat.json`, bukan angka yang
tertulis sebagai total pada artefak. Alasannya perlu: syarat gate meminta dua kondisi sekaligus, dan jumlah fold
yang memenuhi keduanya tidak dilaporkan artefak.

### 2.2 Kelas lain

| Kelas dan tugas | Pra-riset (V9) | Gelombang 1 (R8) | Gelombang 2 (S1 sampai S6) |
|---|---|---|---|
| shk K-i | rule FAR 0,67 sampai 6,6 (9,9 kali), lolos FAR tidak lebih dari 6 di 7 dari 9 fold; kanal absen 6831 dari 56495 baris (12,1 persen) | ML saja: FP 2633, TP 192, AUPRC 0,0499 lawan prevalensi 0,0243, FAR median 3,6217, lead 13,0 menit, 64 dari 181 onset. H2: FP turun 74,67 persen, TP turun 76,04 persen, recall 0,0037, 21 dari 181 onset | tidak ada uji baru. S2, S3, dan S6 tidak menyentuh shk |
| stuck K-ii | TREN, triase | H4: FP 41, presisi 0,6404, recall 0,001, 17 dari 148 onset, lead 8,0 menit. ML 0,0322, CUSUM 0,133 | tidak ada uji baru |
| tool_wear K-i | presisi run 0,50, TLead 20 sampai 36 detik, FP 1 sampai 3 per alat | ML default balanced accuracy median 0,3385, TP 63, FP 148. H3a GWO objektif F1: 0,5 dengan semua jendela positif. H3b: 0,3993, naik di 2 alat dan turun di 2 alat | tidak ada uji baru. Stempel waktu per jendela belum ada, jadi lapisan B tetap tidak terukur (`PM-113`) |
| vib K tunggal | RF AUPRC 0,441 sampai 0,912 (2,07 kali), rule presisi 0,87 sampai 0,95, FAR pada ambang 0,5 menyebar 4,1 sampai 496 (119 kali) | hybrid vib belum diuji di R8 (`PM-104`) | S2: 23922 baris, 4 well, 216 jendela onset, hybrid statistik ditolak. S6: H1p FP 183 lawan persistence 1456, tetapi recall 0,1906 sehingga 0 dari 4 fold mencapai 0,5. Tidak ada komposisi yang lolos |
| ssi K tunggal | hybrid hemat menurunkan FP 26 menjadi 7 pada hitungan EVAL_C; FAR pada ambang 0,3 menyebar 0 sampai 15,6; kanal CRPM absen 62,3 persen | hybrid ssi belum diuji di R8 | S2: 35906 baris, 7 fold dapat diuji, hybrid statistik menang tipis recall +0,0271 dengan FAR 1,4191 kali lebih besar. S6 pada 9 fold: H1p hanya 1 TP dan 17 FP dari 132 onset, recall 0,0. Hybrid rule DAN persistence praktis mati pada ssi |
| bit_wear K-1 | persistence sebagai ranking, tier TREN, FAR tidak sah karena satuannya grid kedalaman | K-2 onset belum dijalankan (`PM-121`) | S3: 7 fold, rule kanal torsi presisi median 0,1492 dan recall 0,1134 pada FAR 241,948; ML kanal fisik presisi 0,6496 dan recall 0,9968 pada FAR 110,432; gate A lolos 0 dari 7 fold |

Catatan penyebut untuk ssi: S6 memakai 9 fold termasuk dua fold UNDERPOWERED dari S2, sehingga angka ssi S6 bukan
angka S2 dengan penyebut yang sama. Perbandingan ssi antar kolom karena itu tidak boleh dilakukan tanpa
menyebutkan penyebutnya.

### 2.3 Lapisan B

| Kolom | Pra-riset | Gelombang 1 | Gelombang 2 |
|---|---|---|---|
| Nilai maintenance dalam uang | tidak ada kolom biaya di data | BELUM TERUKUR (`R8-094`, `R8-095`) | S4: tetap tidak ada kolom biaya pada 10 kandidat yang disapu |
| Jam henti | tidak dihitung | BELUM TERUKUR | S4: interruption other 1202 record dan 2680.917 jam; waiting on weather 445 record dan 1925.5 jam; repair 806 record dan 1215.0 jam |
| Beban pemeriksaan manusia per shift | tidak ada | BELUM TERUKUR | BELUM TERUKUR, tidak ada data jadwal inspeksi di repo |
| Register kegagalan peralatan | tidak ada | tidak ada | S4: 325 berkas HTML dari 1759 memuat tabel `equipmentfailureInfoTable`, berisi 533 record |

### 2.4 Apa yang dikatakan tabel ini

Pertama, kandidat pra-riset memang lebih baik pada satu titik: pada F-14 hybrid rule DAN persistence mengalahkan
H1 dengan FP 110 lawan 215. Kedua, ketika kandidat itu dijalankan pada 9 fold dan 2 seed, keunggulannya tidak
berbentuk dominasi penuh melainkan pertukaran: H1p menaikkan TP 1120 (29,4427 persen), menurunkan FP 8,
menaikkan presisi 0,0453 dan recall 0,088, menambah fold yang memenuhi gate dari 5 menjadi 7 dari 9, tetapi
membayar dengan FAR median 0,5682 lebih tinggi dan lead 3,5 menit lebih pendek. Ketiga, H1p3 adalah pilihan
berbeda: FAR di bawah 6 pada 9 dari 9 fold dengan presisi 0,8646, tetapi recall turun ke 0,5296 dan hanya 5 dari
9 fold yang memenuhi syarat recall.

---

## 3. Komposisi terpilih per kelas damage

Definisi kekuatan bukti: TERUKUR berarti lapisan A dan C terukur penuh pada data kita; SEBAGIAN berarti salah
satu lapisan hanya terukur pada sebagian fold atau sebagian komponen; TERBATAS berarti satuannya sendiri tidak
sah untuk gate; BELUM berarti tidak ada angka.

| Kelas dan tugas | Komposisi terpilih | Lapisan A | Lapisan B | Lapisan C | Batas pemakaian | Kekuatan bukti |
|---|---|---|---|---|---|---|
| hyd K-i, peringatan dini | H1p: rule kanal DAN gerbang persistence, dengan h dipilih per well kalibrasi. H1p3 disediakan sebagai mode alarm rendah | FP 927, TP 4924, presisi 0,8243, recall 0,6519, FAR kalender median 4,0984, 7 dari 9 fold memenuhi FAR dan recall sekaligus | lead 8,0 menit, 218 dari 390 onset, 2,3769 alarm per onset. Rupiah dan jam henti tidak ada | identik di dua seed dengan `beda_sel` 0 pada 45 sel, dan H1 yang direproduksi cocok dengan R8 pada 30 pemeriksaan | label berasal dari residu SPPA dan aliran, jadi ini deteksi kondisi yang didefinisikan variabel itu. FAR median 4,0984 lebih tinggi dari H1 3,5302, dan lead lebih pendek dari H1 11,5 menit | TERUKUR untuk A dan C, SEBAGIAN untuk B |
| hyd K-i, mode alarm rendah | H1p3: rule kanal DAN persistence DAN statistik | FP 568, TP 3557, presisi 0,8646, recall 0,5296, FAR kalender median 2,0323, FAR di bawah 6 pada 9 dari 9 fold, tetapi recall minimal 0,5 hanya di 5 dari 9 fold | lead 12,5 menit, 183 dari 390 onset, 1,4564 alarm per onset, paling rendah di antara semua komposisi | identik di dua seed | recall 0,5296 hanya sedikit di atas batas 0,5, sehingga kesalahan kecil pada fold dapat menjatuhkannya di bawah batas | TERUKUR untuk A dan C, SEBAGIAN untuk B |
| hyd K-i, cakupan penuh | rule kanal tunggal | recall median 0,7507 dan 307 dari 390 onset, FAR median 6,932, 3 dari 9 fold di bawah 6 | lead 6,0 menit, 307 onset | stabil antar paruh 9 dari 9 well | beban alarm tertinggi, 5,3974 alarm per onset | TERUKUR |
| shk K-i | single engine ML untuk pemantauan tren, rule kanal untuk peringatan, tanpa hybrid | ML: FP 2633, TP 192, AUPRC 0,0499 lawan prevalensi 0,0243, FAR median 3,6217. H2 ditolak: TP turun 76,04 persen | BELUM TERUKUR | recall positif di kedua paruh pada 4 dari 9 well untuk ML, 1 dari 9 untuk H2 | hanya untuk pemantauan tren. AUPRC 0,0499 hanya dua kali prevalensi | SEBAGIAN |
| stuck K-ii | tanpa komposisi final, verifikasi manual bertarget | H4: FP 41, presisi 0,6404, recall 0,001, 17 dari 148 onset. ML 0,0322, CUSUM 0,133, rule 0,0808 | BELUM TERUKUR | recall positif di kedua paruh pada 0 dari 4 well | bukan alarm | SEBAGIAN |
| tool_wear K-i | detektor terkalibrasi per alat sebagai peringatan, ML logistik default untuk pemantauan | presisi run 0,50, FP 1 sampai 3 per alat; ML default balanced accuracy median 0,3385 dengan TP 63 dan FP 148 | BELUM TERUKUR karena label hanya punya urutan jendela tanpa stempel waktu | tanda delta berubah antar alat | empat alat saja. Peluang minimal satu alarm kebetulan di 4 dari 4 alat adalah 0,5678 | SEBAGIAN |
| vib K tunggal | rule kanal sebagai peringatan, RF hanya untuk pemeringkatan, tanpa hybrid | rule presisi 0,87 sampai 0,95; RF AUPRC 0,441 sampai 0,912. Dua hybrid ditolak: statistik DAN rule FAR 19,2783 dengan recall 0,1426, dan rule DAN persistence FAR 1,4934 tetapi recall 0,1906 | BELUM TERUKUR | 4 well saja, tanpa seed berulang | ambang global tidak portabel, FAR menyebar 4,1 sampai 496 (119 kali). Tidak ada komposisi yang mencapai recall 0,5 di satu fold pun pada S6 | SEBAGIAN |
| ssi K tunggal | persistence sebagai pemeringkatan, rule kanal untuk peringatan, tanpa hybrid | seluruh komposisi gagal pada syarat recall. H1p: FP 17 dengan 1 TP dari 132 onset dan recall 0,0. Persistence: presisi 0,0940 dan recall 0,0323. Terbaik pada FAR, terburuk pada deteksi | BELUM TERUKUR | 7 fold dapat diuji pada S2, 9 fold pada S6 termasuk 2 fold UNDERPOWERED | kanal CRPM absen 62,3 persen. Pada S2 anggaran 24 memberi presisi 0,0762, yaitu sekitar 12,1 alarm palsu per alarm benar | SEBAGIAN |
| bit_wear K-1 | persistence sebagai pemeringkatan, tanpa alarm | gate A lolos 0 dari 7 fold untuk seluruh model bukan-sirkular; rule kanal torsi presisi 0,1492 dan FAR 241,948; ML kanal fisik presisi 0,6496 dengan FAR 110,432 | BELUM TERUKUR, tidak ada kunci bit maupun biaya | cakupan menit 0,0663 sampai 0,5303 sedangkan syarat 0,50, jadi 1 dari 7 fold lolos syarat cakupan | label praktis dapat direkonstruksi dari kanal fisik: ML kanal fisik recall 0,9968 hampir sama dengan ML ber-`MSE` dan `ROC_coef` 1,0000 | TERBATAS |
| hyd K-ii | tidak ada komposisi, tetap eksplorasi | GAGAL C: satu split temporal, 78,7 persen jendela berbalik tanda | BELUM TERUKUR | tidak stabil | kanal aliran tidak tersedia | BELUM |

### 3.1 Peta tier yang berlaku sekarang

Tier diambil dari `docs/V9_EVAL_C_LAYERC.md` dan tidak berubah di kartu ini: vib rule PERINGATAN-BERPENGAWAS dan
RF TREN; ssi hybrid PERINGATAN-BERPENGAWAS dan RF TREN; shk rule PERINGATAN-BERPENGAWAS dan ML TREN; stuck K-i
PERINGATAN-BERPENGAWAS dengan cakupan dua well dan stuck K-ii TREN; hyd K-i PERINGATAN-BERPENGAWAS pada kedua
mode dan hyd K-ii BELUM LAYAK PAKAI; bit_wear K-1 TREN; tool_wear `op_far_calibrated` PERINGATAN-BERPENGAWAS dan
`calib_5of27` TREN. Slot ALARM-OTOMATIS tetap nol.

### 3.2 Satu hal yang tidak boleh disederhanakan

Komposisi terpilih pada vib dan ssi adalah komposisi yang lebih dekat ke pra-riset, bukan komposisi gelombang 2,
dan itu bukan karena gelombang 2 kalah tipis. Pada kedua kelas itu tidak ada satu komposisi pun yang memenuhi
syarat recall, sehingga yang benar adalah menahan diri: memilih yang terbaik di antara semua yang gagal bukan
pilihan yang lebih baik daripada mengakui tidak ada pemenang.

---

## 4. Keputusan atas komposisi R8: berubah pada hyd, bertahan pada kelas lain

Jawaban singkat: komposisi R8 berubah pada hyd mode peringatan dini, dari H1 menjadi H1p, dan bertahan pada shk,
stuck, tool_wear, vib, ssi, dan bit_wear. Perubahan itu diusulkan dengan angka, dan tetap memerlukan persetujuan
user sebelum dipakai di detektor.

### 4.1 Perubahan pada hyd, dengan angka

Perbandingan di bawah memakai penyebut yang sama, yaitu 9 fold dan 390 onset, dua seed identik, dan baseline
yang dihitung ulang oleh harness yang sama.

| Komposisi | FP | TP | Presisi | Recall | FAR kalender | Lead | Fold FAR tidak lebih 6 | Fold recall minimal 0,5 | Fold memenuhi keduanya |
|---|---|---|---|---|---|---|---|---|---|
| rule kanal | 2105 | 5579 | 0,6835 | 0,7507 | 6,9320 | 6,0 | 3 | 9 | 3 |
| persistence | 1941 | 5243 | 0,7114 | 0,6791 | 6,7404 | 6,0 | 4 | 9 | 4 |
| stat CUSUM | 4361 | 4210 | 0,5052 | 0,5832 | 11,0013 | 8,0 | 2 | 7 | 2 |
| H1 stat DAN rule | 935 | 3804 | 0,7789 | 0,5638 | 3,5302 | 11,5 | 7 | 6 | 5 |
| H1b stat ATAU rule | 5531 | 5985 | 0,4694 | 0,8195 | 14,7156 | 3,0 | 2 | 9 | 2 |
| H1p rule DAN persistence | 927 | 4924 | 0,8243 | 0,6519 | 4,0984 | 8,0 | 7 | 9 | 7 |
| H1p3 rule DAN persistence DAN stat | 568 | 3557 | 0,8646 | 0,5296 | 2,0323 | 12,5 | 9 | 5 | 5 |

Keputusan memakai satu kriteria yang berasal dari definisi gate proyek sendiri, yaitu jumlah fold yang memenuhi
FAR di bawah 6 per 24 jam dan recall minimal 0,5 sekaligus. Dengan kriteria itu H1p menang: 7 dari 9 fold,
sedangkan H1 dan H1p3 masing-masing 5 dari 9. Kemenangan H1p tidak berbentuk dominasi, dan itu harus ditulis
lengkap:

1. Naik dibanding H1: TP 4924 lawan 3804, yaitu 1120 lebih banyak atau 29,4427 persen; presisi 0,8243 lawan
   0,7789 atau 0,0453 lebih tinggi; recall 0,6519 lawan 0,5638 atau 0,088 lebih tinggi; FP 927 lawan 935 atau 8
   lebih sedikit; alarm per onset 2,3769 lawan 2,3974; FAR baris 28,416 lawan 32,256.
2. Turun dibanding H1: FAR kalender median 4,0984 lawan 3,5302 atau 0,5682 lebih tinggi; lead 8,0 lawan 11,5
   menit atau 3,5 menit lebih pendek; onset diperingatkan 218 lawan 219.
3. Naik dibanding rule kanal polos, yaitu baseline pra-riset: FP 927 lawan 2105, presisi 0,8243 lawan 0,6835,
   FAR 4,0984 lawan 6,9320, fold yang memenuhi kedua syarat 7 lawan 3. Yang turun hanya recall 0,6519 lawan
   0,7507 dan lead 8,0 lawan 6,0 menit, dan yang kedua justru lebih baik.

### 4.2 Mengapa H1p3 tidak dipilih sebagai komposisi utama

H1p3 adalah satu-satunya komposisi yang memenuhi FAR di bawah 6 pada 9 dari 9 fold, dengan presisi tertinggi
0,8646 dan beban alarm terendah 1,4564 per onset. Itu bukan alasan untuk memilihnya sebagai komposisi utama,
karena syarat recall gagal: hanya 5 dari 9 fold mencapai recall 0,5, dan recall median 0,5296 hanya 0,0296 di atas
batas. Memilih komposisi yang lolos satu syarat sambil menggantung pada syarat kedua adalah pola yang sudah
ditolak pada gelombang 1, yaitu ketika H1 dinyatakan menang hanya karena FAR turun tanpa melihat TP yang hilang.

H1p3 tetap dipakai sebagai mode alarm rendah, dengan konsekuensi tertulis: ia menerima 247 TP lebih sedikit
daripada H1, dan pemakainya harus tahu itu.

### 4.3 Kelas yang komposisinya tidak berubah

| Kelas | Komposisi berlaku | Kandidat pengganti | Alasan bertahan, dengan angka |
|---|---|---|---|
| shk K-i | single ML untuk tren, rule untuk peringatan | H2 ML DAN statistik | H2 memotong TP 76,04 persen dan menyisakan recall 0,0037 dengan 21 dari 181 onset, sedangkan ML saja memberi 64 dari 181 pada FAR 3,6217 |
| stuck K-ii | triase TREN, H4 untuk verifikasi manual | tidak ada kandidat baru | recall median semua komponen tidak lebih dari 0,133, dan H4 memberi recall 0,001 dengan 17 dari 148 onset |
| tool_wear K-i | detektor terkalibrasi per alat | H3a dan H3b GWO | H3a degenerat dengan balanced accuracy 0,5 dan semua jendela positif. H3b 0,3993 naik di 2 alat dan turun di 2 alat |
| vib | rule kanal peringatan, RF pemeringkatan | H1p rule DAN persistence | H1p menurunkan FP dari 1456 menjadi 183 dan FAR dari 22,0218 menjadi 1,4934 pada 3 dari 4 fold, tetapi recall 0,1906 dan 0 dari 4 fold mencapai 0,5. Menukar deteksi dengan ketenangan alarm bukan perbaikan |
| ssi | persistence pemeringkatan, rule peringatan | H1p rule DAN persistence | H1p pada 9 fold menghasilkan 1 TP dan 17 FP dari 132 onset, dengan recall 0,0. Komposisi ini praktis tidak menyala pada positif |
| bit_wear K-1 | persistence pemeringkatan | H5 dan H6 | gate A lolos 0 dari 7 fold; H6 punya presisi 0,6132 tetapi FAR median 12,270, yaitu 2,05 kali anggaran 6,0 |

### 4.4 Apakah S6 melahirkan algoritma yang lebih baik dari angka lintas seed

Ya, tetapi hanya untuk hyd, dan hanya pada kriteria gate yang dipakai proyek ini sendiri. H1p adalah komposisi
baru yang belum ada di pra-riset maupun gelombang 1, diuji pada 9 fold dan 2 seed, identik antar seed dengan
`beda_sel` 0, dan lebih baik daripada H1 pada jumlah fold yang memenuhi FAR dan recall sekaligus, yaitu 7 lawan
5, dengan biaya FAR median 0,5682 lebih tinggi dan lead 3,5 menit lebih pendek.

Untuk vib dan ssi, jawabannya tidak. Kedua kelas itu tidak punya komposisi yang memenuhi syarat recall, sehingga
menyebut salah satunya lebih baik akan menjadi klaim tanpa dasar.

---

## 5. Keputusan tier

Keputusan: tidak ada kenaikan tier, dan tidak ada penurunan baru terhadap tier yang berlaku. Slot ALARM-OTOMATIS
tetap nol. Penurunan yang tercatat pada gelombang 1, yaitu `rule_display` ssi dari PERINGATAN-BERPENGAWAS, tetap
berlaku dan tidak dibalik.

| Kelas dan komponen | Tier sekarang | Usulan S6 | Alasan berbasis angka | Syarat yang masih menggantung |
|---|---|---|---|---|
| hyd K-i, H1p | PERINGATAN-BERPENGAWAS | tetap | dua dari tiga syarat terpenuhi: lapisan C identik di dua seed dengan `beda_sel` 0, dan lapisan A memenuhi FAR serta recall di 7 dari 9 fold | lapisan B tidak terukur. Cakupan di atas 50 persen hanya pada satu well, F-10 dengan 0,673, sedangkan F-5 hanya 0,0171 |
| hyd K-i, H1p3 | PERINGATAN-BERPENGAWAS | tetap | FAR di bawah 6 pada 9 dari 9 fold, presisi 0,8646, beban alarm 1,4564 per onset | recall minimal 0,5 hanya di 5 dari 9 fold, dan lapisan B tidak terukur |
| hyd K-i, rule cakupan penuh | PERINGATAN-BERPENGAWAS | tetap | FAR median 6,9320, yaitu di ambang anggaran | beban manusia per shift tidak ada datanya |
| ssi `rule_display` | turun ke TREN pada gelombang 1 | tidak dibalik | varian CUSUM ATAU rule menaikkan FAR median 1,4191 kali, dan S6 menunjukkan komposisi rule DAN persistence memberi 1 TP dari 132 onset | membuka kembali butuh presisi di atas 0,1111 pada FAR yang sama |
| vib rule | PERINGATAN-BERPENGAWAS | tetap | presisi rule 0,87 sampai 0,95 | FAR menyebar 119 kali, hanya 4 well, dan tidak ada komposisi yang mencapai recall 0,5 |
| shk rule | PERINGATAN-BERPENGAWAS | tetap | FAR 0,67 sampai 6,6 dan lolos FAR tidak lebih dari 6 di 7 dari 9 fold | kanal absen 12,1 persen, tidak ada uji baru |
| tool_wear `op_far_calibrated` | PERINGATAN-BERPENGAWAS | tetap | stabil di 4 alat pada ambang terkalibrasi | presisi run 0,50, peluang alarm kebetulan di 4 dari 4 alat 0,5678 |
| stuck K-i | PERINGATAN-BERPENGAWAS, cakupan 2 well | tetap | presisi kondisional 0,92 sampai 0,97 pada 2 fold | portabilitas belum terukur |
| stuck K-ii | TREN | tetap | recall maksimum satu fold 0,0635 dan median tidak lebih dari 0,133 | butuh event jauh lebih banyak |
| bit_wear K-1 | TREN | tetap | gate A lolos 0 dari 7 fold, satuannya grid kedalaman | label dapat direkonstruksi dari kanal fisik |
| hyd K-ii | BELUM LAYAK PAKAI | tetap | 78,7 persen jendela berbalik tanda pada satu split temporal | kanal aliran keluaran belum ada |

### 5.1 Apa yang akan membuka kenaikan tier

Syaratnya tidak berubah dan harus terpenuhi bersamaan: lapisan C stabil, lapisan A dengan FAR di bawah 6 per 24
jam pada titik operasi, dan lapisan B berupa beban pemeriksaan manusia yang dapat diterima. Untuk hyd dengan H1p3,
dua syarat pertama sudah terpenuhi pada satuan kalender. Yang gagal adalah lapisan B, dan penahannya bukan mutu
deteksi melainkan ketiadaan data biaya dan jadwal inspeksi.

Konsekuensi yang harus ditulis terang: angka lintas seed pada S6 mendukung kestabilan, tetapi kestabilan bukan
syarat tunggal. Mengusulkan kenaikan tier berlandaskan S6 saja berarti memakai dua dari tiga syarat, dan itu
ditolak di sini. Kenaikan tetap memerlukan persetujuan user setelah lapisan B terukur.

### 5.2 Satu penurunan cakupan yang diusulkan

Bukan penurunan tier, melainkan penurunan luas klaim: badge peringatan hyd harus diberi label bersyarat per well,
bukan global, karena F-10 dengan cakupan 0,673 dan F-5 dengan 0,0171 dihitung pada aturan yang sama.

---

## 6. Algoritma yang diuji dan ditolak

Daftar ini memisahkan yang ditolak karena angkanya menolak dari yang belum dijalankan.

| Algoritma atau komposisi | Gelombang | Peran yang diuji | Angka penolak | Syarat pembuka |
|---|---|---|---|---|
| Metaheuristik kontinu: GWO, WOA, PSO, HHO, SSA, SMA | 1 (R1, R8 H3) | tuning hyperparameter | tidak ada run di repo yang menunjukkan kenaikan dari tuning (R1 bagian 5.2). GWO objektif F1 memberi balanced accuracy 0,5 dengan 240 TP dan 229 FP (`PM-038`, `PM-040`, `PM-041`); objektif balanced accuracy 0,3993 lawan 0,3385 dengan tanda berubah antar alat | wajib disandingkan random search pada jumlah evaluasi identik |
| Dekomposisi sinyal: VMD, EMD, wavelet | 1 (R3) | pra-olahan getaran | laju sampel tertinggi 0,3333 Hz memberi Nyquist 0,1667 Hz (`PM-103`, `PM-104`), sedangkan pita diagnostik bantalan orde ratusan Hz. 105 percobaan VMD dengan 75 gagal (`PM-105`, `PM-106`) | kanal dengan laju minimal orde Hz |
| Kernel SVM | 1 (E1) | pengganti rule | skor shortlist 2,25 tetapi bukan finalis, dan tidak ada angka kita yang menunjukkan SVM mengalahkan rule pada FAR yang sama | hanya sebagai pembanding pada anggaran sisa |
| kNN-DTW | 1 (R6) | klasifikasi bentuk gelombang | biaya 134,01 sampai 137374.35 jam untuk satu klasifikasi penuh (`PM-107`) | tidak ada |
| Markov chain, HMM, Bayesian network, MCMC | 1 (R2, D0) | pemodelan state | label state fisik tidak tersedia dan episode sangat pendek sehingga memori praktis nol | label state fisik dan uji orde Markov |
| Survival: Random Survival Forest, DeepHit | 1 (R2, D0) | prediksi waktu kegagalan | event per well kecil dan horizon 10 menit | event jauh lebih banyak |
| H2: ML DAN statistik pada shk | 1 (R8) | peringatan dini stick-slip | FP turun 74,67 persen tetapi TP turun 76,04 persen, menyisakan recall 0,0037 dan 21 dari 181 onset | harus menaikkan TP pada FAR yang sama |
| H3a: GWO objektif F1 pada tool_wear | 1 (R8) | klasifikasi status per jendela | degenerate, semua jendela positif, balanced accuracy 0,5 di 4 dari 4 alat | objektif yang tidak dapat dimainkan |
| H3b: GWO objektif balanced accuracy | 1 (R8) | klasifikasi status per jendela | 0,3993 lawan 0,3385, tetapi naik di 2 alat dan turun di 2 alat | tanda efek konsisten lintas alat |
| H5: CUSUM DAN rule pada bit_wear | 2 (S3) | deteksi keausan bit | presisi median 0,1155, recall 0,0377, FAR median 65,617, gate A lolos 0 dari 7 fold | gate A lolos lebih dari satu fold |
| H6: ML DAN CUSUM pada bit_wear | 2 (S3) | deteksi keausan bit | presisi 0,6132 dan recall 0,1784, tetapi FAR median 12,270 yaitu 2,05 kali anggaran | FAR di bawah 6 pada titik operasi |
| CUSUM DAN rule pada vib | 2 (S2) | peringatan dini getaran | FAR median 19,2783 dengan recall 0,1426, sementara persistence memberi recall 0,7405 | harus melampaui persistence pada recall dan FAR |
| CUSUM ATAU rule pada vib | 2 (S2) | peringatan dini getaran | FAR median 46,4076 dengan presisi 0,4276 | mengalahkan persistence pada tiga sumbu |
| CUSUM ATAU rule pada ssi | 2 (S2) | peringatan dini stick-slip | recall median hanya +0,0271, presisi median 0,0010 lebih rendah, FAR 1,4191 kali lebih besar | presisi di atas 0,1111 pada FAR yang sama |
| CUSUM DAN rule pada ssi | 2 (S2) | peringatan dini stick-slip | recall median 0,0000 karena CUSUM tersaturasi pada h tertinggi grid di 8 dari 13 fold | grid ambang yang tidak tersaturasi |
| H1b stat ATAU rule pada hyd | 2 (S6) | peringatan dini hidraulik | recall 0,8195 memang tertinggi, tetapi FP 5531 yaitu 2,63 kali rule kanal polos, presisi 0,4694, FAR median 14,7156, dan hanya 2 dari 9 fold memenuhi FAR serta recall | tidak ada, karena beban alarmnya melebihi baseline yang digantikannya |
| H1p pada vib | 2 (S6) | peringatan dini getaran | FP 183 dan FAR 1,4934 pada 3 dari 4 fold, tetapi recall 0,1906 dan 0 dari 4 fold mencapai 0,5 | harus mencapai recall 0,5 pada minimal satu fold |
| H1p pada ssi | 2 (S6) | peringatan dini stick-slip | 17 FP dan 1 TP dari 132 onset, recall 0,0, presisi 0,0 pada median | tidak ada dengan data saat ini |

### 6.1 Pola yang muncul dari daftar ini

Dari 18 penolakan di atas, 7 di antaranya adalah kegagalan bentuk komposisi DAN, yaitu gerbang kedua yang memaksa
keluaran hampir selalu nol: H2, H5, H6, CUSUM DAN rule pada vib, CUSUM DAN rule pada ssi, H1p pada vib, dan H1p
pada ssi. Mekanismenya sama di empat kelas: CUSUM tersaturasi pada ambang tertinggi grid (hyd 8 dari 13 fold,
bit_wear 7 dari 7 fold, ssi recall 0,0000, vib recall 0,1426). Temuan S6 menambahkan satu varian baru dari pola
yang sama: pada ssi, gerbang persistence juga mematikan sinyal, dengan 1 TP dari 132 onset.

Karena itu aturan yang diusulkan menjadi permanen: sebelum komposisi DAN dipakai, laju alarm komponennya wajib
diperiksa lebih dulu, dan komposisi DAN dilarang dipakai bila salah satu komponen menghasilkan hampir nol
keluaran pada anggaran yang sama.

### 6.2 Yang belum dijalankan dan tidak boleh disebut ditolak

1. BGWO untuk seleksi fitur (T2): belum pernah dijalankan pada data kita (`PM-117`). Status: PILOT.
2. Pilot gelombang 2 lain di roadmap PM, yaitu P-2 boosting dan conformal, P-3 Cox, P-5 ADWIN, dan P-6 Isolation
   Forest: tidak satu pun dieksekusi pada kartu S1 sampai S6. Status: belum terukur.
3. H1p3 pada vib dan ssi: hanya H1p yang diuji pada kedua kelas itu. Status: belum dijalankan.
4. Kalibrasi ambang per well prospektif (`PM-119`): belum dijalankan.

---

## 7. Pemisahan lapisan A, B, dan C

| Kelas | Lapisan A | Lapisan B | Lapisan C | Yang belum terukur dan sebabnya |
|---|---|---|---|---|
| hyd K-i | terukur: 9 fold, 2 seed, 390 onset, H1p memenuhi FAR dan recall di 7 dari 9 fold | sebagian: lead 8,0 menit, 218 dari 390 onset, 2,3769 alarm per onset. Rupiah dan jam henti tidak ada | terukur: `beda_sel` 0 pada 45 sel antar dua seed, H1 direproduksi cocok pada 30 pemeriksaan | biaya per kejadian dan jadwal inspeksi tidak ada di repo |
| vib | terukur: 4 fold, 216 onset | belum terukur | terukur pada 4 well saja, tanpa seed berulang | hanya 4 well, generalisasi lemah secara desain (S2 bagian 2.1) |
| ssi | terukur: 9 fold pada S6 termasuk 2 fold UNDERPOWERED, 7 fold pada S2, 132 onset | belum terukur | terukur, tetapi tidak ada komposisi yang mencapai recall 0,5 | kanal CRPM absen 62,3 persen |
| bit_wear K-1 | terukur tetapi gagal: gate A lolos 0 dari 7 fold | belum terukur | terbatas: cakupan menit 0,0663 sampai 0,5303, syarat 0,50, lolos 1 dari 7 fold | tidak ada kunci bit dan tidak ada biaya |
| stuck K-ii | terukur: 4 well, 148 onset | belum terukur | terukur: recall positif di kedua paruh pada 0 dari 4 well | event terlalu sedikit, horizon 10 menit |
| tool_wear K-i | terukur: 4 alat, presisi run 0,50, FP 1 sampai 3 per alat | belum terukur | tanda delta berubah antar alat | label tanpa stempel waktu (`PM-113`) |

### 7.1 Bukti hitungan mengapa lapisan B belum terukur

S4 menyapu 10 kandidat data dan tidak satu pun memuat kolom biaya. Pemindaian token biaya pada 18 kolom USROP,
yaitu `cost`, `downtime`, `npt`, `price`, `usd`, `opex`, `rig_rate`, dan `standby`, memberi hasil kosong (S3
bagian 6). `labels_curated_v2.csv` memuat 884 record dan 20 kolom tanpa kolom biaya. Dari 1759 laporan harian, 325
berkas HTML memuat tabel `equipmentfailureInfoTable` dengan 533 record, dan isinya downtime dalam menit, bukan
uang.

Yang terukur dari lapisan B adalah waktu, bukan nilai. Tiga kategori gangguan pada `ddr.parquet` memberi 2453
record dan 5821.417 jam: interruption other 1202 record dan 2680.917 jam, waiting on weather 445 record dan
1925.5 jam, repair 806 record dan 1215.0 jam. Median jam untuk repair adalah 1,0 dengan p90 3,5 dan maksimum
12,5, sehingga durasi dapat dipakai untuk beban waktu tetapi tidak dapat dikonversi menjadi rupiah tanpa tarif.

Beban pemeriksaan manusia per shift tidak terukur karena tidak ada satu pun berkas jadwal inspeksi di repo.
Inilah syarat yang menahan kenaikan tier pada seluruh kelas, dan penahannya bukan mutu deteksi.

### 7.2 Jumlah butir yang belum terverifikasi menurut audit S5

S5 menghitung 27 butir daftar belum terverifikasi pada empat dokumen, yaitu 8 pada S1, 6 pada S2, 6 pada S3, dan
7 pada S4, ditambah 8 butir pada audit S5 sendiri. Dua di antaranya mengikat dokumen ini langsung: rerun S1 hanya
dua dari lima seed, dan S2 sampai S4 tidak dijalankan ulang.

---

## 8. Sembilan cacat minor temuan S5 dan statusnya

Kolom status diisi dengan pemeriksaan hari ini, bukan dengan asumsi bahwa cacat sudah diperbaiki karena sudah
dilaporkan.

| Kode | Kartu | Cacat menurut S5 | Status setelah pemeriksaan S6 | Bukti pemeriksaan |
|---|---|---|---|---|
| D1 | S4 | baris ledger `S4-013` menulis 884 record dan 884 kolom, sedangkan kolom rujukan pada baris yang sama menyebut `sumber.kolom` berisi 20 kolom | belum diperbaiki | `grep` hari ini pada `docs/RND_PROVENANCE_LEDGER.md` baris 2182 masih berbunyi "884 record / 884 kolom" |
| D2 | S1 | hanya 344 dari 508 sel angka tabel (0,6772) punya padanan di blok ledger S1 | belum diperbaiki, tidak diuji ulang | hitung ulang butuh eksekusi kode; 0,6772 tetap klaim S5 |
| D3 | S3 | hanya 139 dari 339 sel angka tabel (0,41) punya padanan di blok ledger S3 | belum diperbaiki, tidak diuji ulang | sama seperti D2 |
| D4 | semua | 61 sel ledger memakai titik sebagai pemisah ribuan sedangkan blok yang sama memakai koma desimal, sehingga 32.256 dapat dibaca 32,256 atau 32256 | belum diperbaiki | `grep` hari ini menemukan 393 baris ledger berpola pemisah ribuan, dan `S1-034` masih berbunyi 32.256 |
| D5 | S2 | 32,17405 ft/s2 diberi kelas STANDAR dengan rujukan API RP 7G tanpa nomor bagian | belum diperbaiki | `docs/RND_S2_HYBRID_VIB_SSI.md` baris 107 masih menyebut "API RP 7G" tanpa bagian |
| D6 | semua | tidak ada DOI dan tidak ada URL pada empat dokumen, sehingga audit DOI tidak punya target dan tidak dapat dinyatakan lulus | belum diperbaiki | `grep` pola DOI hari ini memberi 0 kemunculan pada S1, S2, S3, S4 |
| D7 | S1 | empat dari 10 pikiran sequ-mcp pada run awal tidak dapat dibuktikan dari artefak | belum diperbaiki | tidak dapat diverifikasi tanpa transkrip sesi |
| D8 | S1, S2, S3 | keterlacakan dokumen ke baris ledger lemah: kode S1-nnn, S2-nnn, S3-nnn dikutip 0 kali, sedangkan S4 mengutip 42 kali | belum diperbaiki | `grep` hari ini memberi 0 untuk S1, 0 untuk S2, dan 0 untuk S3 |
| D9 | S4 | 32 dari 95 baris ledger memakai rujukan prosa multi-nilai sehingga tidak dapat diresolusi mesin | belum diperbaiki, tidak diuji ulang | hitung ulang butuh resolver; 32 dari 95 tetap klaim S5 |

### 8.1 Dua cacat yang menyentuh dokumen ini langsung

D4 dan D8 akan terulang di dokumen S6 kalau tidak dicegah. Pencegahan yang dilakukan: seluruh angka memakai titik
desimal tanpa pemisah ribuan, dan setiap angka penting disertai kode baris ledger `S6-nnn` atau nomor baris
dokumen sumber. Yang tidak dilakukan adalah memperbaiki cacatnya di dokumen sumber, karena perbaikan itu mengubah
700 lebih baris ledger dan merupakan pekerjaan tersendiri.

Satu hal yang harus dinyatakan tanpa dibungkus: laporan S5 menyebut "tidak ada cacat kritis", dan itu benar untuk
objek yang diperiksanya. Tetapi audit itu hanya menjalankan ulang S1. Untuk S2, S3, dan S4, yang diperiksa adalah
keberadaan nilai pada artefak dan keterlacakan baris ledger, bukan kebenaran modelnya. Vonis S6 atas ketiga kartu
itu karena itu adalah vonis atas angka yang sudah dilaporkan.

---

> Catatan 2026-10-29: sembilan cacat minor yang disebut di bagian 8 sudah ditangani. Status per butir ada di `docs/RND_S5_DEFECT_STATUS.md`, dan perubahan detektor-nya di `docs/RND_ENGINE_S6_INTEGRATION.md`.

## 9. Ringkasan lima baris dan yang belum terverifikasi

1. Komposisi hyd mode peringatan dini berubah dari H1 menjadi H1p, yaitu rule kanal DAN persistence, karena pada
   9 fold dan 2 seed ia memenuhi FAR di bawah 6 serta recall minimal 0,5 di 7 dari 9 fold, sedangkan H1 hanya 5
   dari 9, dengan biaya FAR median 0,5682 lebih tinggi dan lead 3,5 menit lebih pendek.
2. Kandidat pra-riset memang menang pada satu titik, yaitu F-14 dengan FP 110 lawan 215, tetapi ketika dijalankan
   pada seluruh fold kemenangannya berubah bentuk menjadi pertukaran, bukan dominasi.
3. Komposisi R8 bertahan pada shk, stuck, tool_wear, dan bit_wear, dan tidak ada pemenang pada vib maupun ssi
   karena tidak satu komposisi pun mencapai recall 0,5.
4. Tidak ada kenaikan tier dan slot ALARM-OTOMATIS tetap nol, karena syarat yang gagal adalah lapisan B dengan 0
   kolom biaya dan 0 berkas jadwal inspeksi di repo, bukan mutu deteksi.
5. Sembilan cacat minor S5 belum diperbaiki satu pun, dan dua di antaranya, yaitu format angka dan keterlacakan,
   dicegah agar tidak terulang di dokumen ini.

### 9.1 Yang belum terverifikasi

1. Hasil S6 hanya pada dua seed, yaitu 42 dan 13. Seed lain tidak dijalankan, meskipun komposisi yang diuji
   deterministik dan kontrol negatif membuktikan harness peka seed ketika ada komponen acak.
2. Jumlah fold yang memenuhi FAR dan recall sekaligus pada bagian 2.1 dan 4.1 adalah hitungan penulis dokumen ini
   dari `s6_kandidat.json`, bukan angka yang tersimpan sebagai total pada artefak.
3. shk, stuck, tool_wear, dan bit_wear tidak menerima uji baru pada kartu ini, sehingga vonis gelombang 1 untuk
   keempatnya tidak mendapat bukti tambahan dan statusnya tetap, bukan terkonfirmasi.
4. S2, S3, dan S4 tidak direproduksi. Yang diperiksa S5 adalah artefak, ledger, dan angka yang dikutip.
5. Cacat D2, D3, dan D9 tidak diuji ulang karena hitung ulangnya membutuhkan eksekusi kode baru.
6. Penjumlahan 2453 record dan 5821.417 jam pada bagian 7.1 adalah aritmetika penulis dokumen ini atas tiga baris
   S4, bukan angka total pada dokumen sumber.
7. Peta tier pada bagian 3.1 dibaca dari `docs/V9_EVAL_C_LAYERC.md` dan `docs/RND_PM_VERDICT.md`, tidak
   diverifikasi ulang ke `scratch/v9_i1/v9_i1_RESULTS.json` pada kartu ini.
8. Pemeriksaan DOI tidak berlaku karena nol DOI dan nol URL pada dokumen gelombang 2. Itu bukan lulus, melainkan
   tidak ada objek yang diperiksa.
9. Angka ssi S6 memakai 9 fold termasuk dua fold UNDERPOWERED, sehingga tidak sebanding dengan angka ssi S2 yang
   memakai 7 fold. Perbandingan ssi antar gelombang harus selalu menyebut penyebutnya.
10. Perubahan komposisi hyd dari H1 ke H1p diusulkan di sini dan belum diterapkan pada detektor mana pun. Penerapan
    memerlukan persetujuan user.
11. Jumlah pikiran sequ-mcp untuk kartu ini tidak dilaporkan sebagai bukti, karena tidak dapat diperiksa dari
    artefak.

Jumlah em-dash pada dokumen ini: 0.
