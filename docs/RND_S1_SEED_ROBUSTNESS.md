# RND-S1: ketahanan lintas seed H1 hyd dan harness bersama (kartu t_6890a1c7)

Riset pendahuluan: statistical-analysis, scikit-learn, scientific-critical-thinking, verification-mandatory.

Cara pemakaian skill:

- **statistical-analysis** dipakai untuk memilih satuan metrik: FAR pada satuan kalender (satuan gate) berdampingan dengan satuan baris negatif supaya sebanding dengan angka V9; setiap sebaran dilaporkan sebagai median, min, maks, dan rentang, bukan satu angka tunggal; sel yang meleset ditulis apa adanya, bukan dibulatkan menjadi keberhasilan.
- **scikit-learn** dipakai untuk kontrol stokastik ML: LightGBM dengan random_state=seed pada dataset hyd yang sama dan fold yang sama. Kolom turunan label (y_*, valid_prev_*, obs_*, anom_*, lab_*), ts_bin, feat_ts_max, dan kolom meta dilarang masuk matriks fitur, dan larangan itu ditegakkan oleh assert di fungsi fitur_dari.
- **scientific-critical-thinking** dipakai untuk menguji penjelasan alternatif: varians nol H1 dapat berarti arsitektur deterministik ATAU acuan seed yang tidak tersambung. Kontrol ML pada seed yang sama adalah tes pembeda yang bisa gagal.
- **verification-mandatory** dipakai untuk menegakkan bukti mentah: seluruh angka dokumen ini disisipkan generator ini dari berkas JSON dengan assert sebelum menulis, dan artefak JSON mentah wajib ada di scratch/rnd/s1. Run ulang segar menghasilkan angka identik.

sequ-mcp dipakai 10 pikiran lintas dua run: 6 pikiran pada run verifikasi ini (pemisahan klaim yang harus diuji, tes pembeda seed lewat kontrol ML, temuan konstanta R8 yang masih hardcode, pemeriksaan angka per fold, pemeriksaan angka V9 dan ledger, dan keputusan perbaikan) serta 4 pikiran pada run awal (desain uji lintas seed, urutan fail-fast plus jalur silang V9, pembagian lapisan A/B/C beserta batas kalibrasi, dan daftar yang belum terukur). Jumlah run awal tercatat dari sesi sebelumnya dan tidak dapat dibuktikan ulang dari artefak.

Artefak mentah: scratch/rnd/s1/s1_hyd_seeds.json, s1_meta.json, s1_h_saturasi.json, s1_hluas.json. Kode: code/rnd_hybrid_harness.py (harness bersama), code/rnd_s1_run.py (runner), code/rnd_s1_hcheck.py (saturasi ambang), code/rnd_s1_ledger.py (ledger), code/rnd_s1_dokumen.py (dokumen ini). Setiap angka punya baris S1-nnn di docs/RND_PROVENANCE_LEDGER.md.

### Catatan provenance (revisi 2026-10-29)

Cakupan ledger terukur pada dokumen ini: 64 dari 441 sel angka tabel (14.51 persen) punya padanan nilai pada blok `S1-` di `docs/RND_PROVENANCE_LEDGER.md`. Sel yang tidak punya padanan adalah agregat turunan antar fold atau antar berkas, dan tidak diklaim punya baris tersendiri.

Rujukan metode: konstanta metode di dokumen ini adalah konvensi internal repo dengan jejak berkas dan baris. Satu-satunya standar eksternal yang dipakai adalah ISO 2041:2018 §3.1.4 untuk nilai g, tercatat pada baris ledger L-01. Dokumen ini tidak mengklaim DOI luar, jadi butir audit DOI tidak berlaku di sini.

sequ-mcp: 6 pikiran pada run verifikasi ini tersimpan di transkrip sesi; 4 pikiran run awal tidak punya transkrip tersimpan, jadi dihitung 6 bukan 10.

---

## 1. Lingkup dan kebijakan pengikat

Kebijakan pengikat: docs/RND_EVALUATION_POLICY.md. Pertanyaan kartu: apakah angka H1 (statistik DAN rule pada hyd K-i) dari R8 bertahan kalau seed diubah, dan apakah harness bersama layak dipakai S2 dan S3.

Prinsip eksekusi: reproduksi dulu angka seed 42 terhadap R8 dan berhenti bila meleset, lalu jalankan seed lain, lalu kontrol stokastik sebelum klaim determinisme dipakai. Tidak ada run yang diklaim nyata tanpa artefak JSON, dan tidak ada angka dokumen yang ditulis tangan.

Definisi stabil yang dipakai di sini, dinyatakan sebelum hasil: stabil berarti rentang antar seed nol pada metrik utama (FP total, presisi median, recall median, FAR, lead). Stabilitas lintas seed bukan bukti bahwa ambangnya benar, karena stabilitas bisa lahir dari arsitektur yang memang tidak memakai angka acak.

---

## 2. Metode: harness bersama code/rnd_hybrid_harness.py

| Kelompok | Fungsi | Keterangan |
|---|---|---|
| Muat data | muat_dataset, pecah_well, muat_fold | CSV menit, dict per well terurut ts_bin, fold LOWO |
| Detektor | seri_z, gerbang_rule, cusum_alarm, jendela_alarm, pilih_h, detektor_stat_rule | rule kanal kausal bin t-1, CUSUM dua sisi dengan reset, zona peringatan 10 menit, ambang h dari well kalibrasi |
| ML (S2/S3 dan kontrol S1) | fitur_dari, latih_lgb, threshold_conformal, skor_ml_fold | kolom bocor dibuang dengan assert, ambang conformal kuantil (1-alpha) skor negatif kalibrasi |
| Evaluasi | evaluasi_fold, ringkas_records, sidik_metrik | FAR dua satuan, batas Garwood dua sisi, lead, separuh waktu |
| Penulisan | tulis_json | artefak JSON mentah |

Aturan modul yang mengikat S2 dan S3: keputusan pada menit t hanya memakai informasi sampai t-1 untuk gerbang rule, CUSUM hanya mengonsumsi z yang sudah tersedia, ambang tidak pernah dilihatkan ke well uji, FAR dilaporkan pada dua satuan, dan seed hanya menyentuh komponen ML. H1 (rule plus CUSUM) dinyatakan deterministik penuh di docstring, sehingga pemanggil yang butuh komponen stokastik wajib memakai skor_ml_fold dan merakit sendiri.

Konstanta yang dipegang: alpha_budget 0,004167 (setara 6 per 1440 menit), horizon lead 60 menit, jendela alarm 10 menit, cusum_k 0,5, grid h 0,5 sampai 30, FAR maksimum 6 dan recall minimum 0,5 untuk definisi gate baru.

---

## 3. Data dan pemeriksaan awal

Dataset scratch/v9_d1/datasets/hyd_ki.csv.gz: 52509 baris, 50 kolom, sha256 4a701ed63291e455 (16 karakter awal), 9 well, 9 fold LOWO dari scratch/v9_d1/lowo_hyd_ki.json.

| Well | Baris | Positif y_hyd | Menit kalender | Cakupan baris/kalender |
|---|---|---|---|---|
| F-10 | 7571 | 1394 | 11249 | 0,673 |
| F-12 | 7390 | 1426 | 86454 | 0,0855 |
| F-14 | 10401 | 865 | 317679 | 0,0327 |
| F-15A | 6156 | 698 | 32141 | 0,1915 |
| F-15_S | 8355 | 993 | 92488 | 0,0903 |
| F-5 | 6332 | 621 | 369549 | 0,0171 |
| F-7 | 2482 | 421 | 23011 | 0,1079 |
| F-9 | 1616 | 423 | 22858 | 0,0707 |
| F-9_A | 2206 | 331 | 7344 | 0,3004 |

Cakupan rekaman rendah bila penyebut kalender dibaca sebagai waktu operasi nyata: cakupan median fold 0,0903, dan cakupan tiap fold ada di tabel bagian 6.1. Karena itu FAR kalender dipakai sebagai satuan gate sesuai kebijakan, sementara FAR baris dipakai untuk membandingkan dengan angka pra-riset V9, dan kedua satuan tidak boleh dicampur dalam satu klaim.

---

## 4. Reproduksi angka terbit R8 pada seed 42

| Metrik | Terbit R8 | Replikasi S1 | Selisih | Lulus |
|---|---|---|---|---|
| FP total | 935 | 935 | 0 | ya |
| TP total | 3804 | 3804 | 0 | ya |
| Presisi median | 0,7789 | 0,7789 | 0 | ya |
| Recall median | 0,5638 | 0,5638 | 0 | ya |
| Lead median | 11,5 | 11,5 | 0 | ya |
| Onset | 390 | 390 | 0 | ya |
| Diperingatkan | 219 | 219 | 0 | ya |

Per fold, FP, TP, dan ambang h cocok persis:

| Fold | FP R8 | FP S1 | Delta FP | TP R8 | TP S1 | Delta TP | h R8 | h S1 |
|---|---|---|---|---|---|---|---|---|
| F-10 | 61 | 61 | 0 | 794 | 794 | 0 | 30 | 30 |
| F-12 | 149 | 149 | 0 | 804 | 804 | 0 | 30 | 30 |
| F-14 | 215 | 215 | 0 | 443 | 443 | 0 | 30 | 30 |
| F-15A | 101 | 101 | 0 | 288 | 288 | 0 | 30 | 30 |
| F-15_S | 123 | 123 | 0 | 390 | 390 | 0 | 30 | 30 |
| F-5 | 104 | 104 | 0 | 410 | 410 | 0 | 30 | 30 |
| F-7 | 85 | 85 | 0 | 271 | 271 | 0 | 30 | 30 |
| F-9 | 55 | 55 | 0 | 256 | 256 | 0 | 30 | 30 |
| F-9_A | 42 | 42 | 0 | 148 | 148 | 0 | 30 | 30 |

**Kesimpulan replikasi: LULUS.** Ketujuh metrik cocok persis dengan toleransi yang ditetapkan runner (FP, TP, dan jumlah onset wajib nol delta; presisi, recall, dan lead toleransi 0,0001). Jalur silang kedua di luar R8 juga cocok: model rule_kanal pada fold F-14 memberi TP 607 dan FP 368, persis sama dengan head rule_display V9 pada segmen yang sama (bagian 7). Karena replikasi lulus, generator lintas seed dilanjutkan.

---

## 5. Lintas seed H1 dan kontrol stokastik

### 5.1 H1 eksak protokol R8, lima seed, sembilan fold per seed

| Metrik | 42 | 7 | 13 | 21 | 33 | Median | Min | Maks | Rentang |
|---|---|---|---|---|---|---|---|---|---|
| fp_total | 935 | 935 | 935 | 935 | 935 | 935 | 935 | 935 | 0 |
| tp_total | 3804 | 3804 | 3804 | 3804 | 3804 | 3804 | 3804 | 3804 | 0 |
| precision_median | 0,7789 | 0,7789 | 0,7789 | 0,7789 | 0,7789 | 0,7789 | 0,7789 | 0,7789 | 0 |
| recall_median | 0,5638 | 0,5638 | 0,5638 | 0,5638 | 0,5638 | 0,5638 | 0,5638 | 0,5638 | 0 |
| far24_kalender_median | 3,5302 | 3,5302 | 3,5302 | 3,5302 | 3,5302 | 3,5302 | 3,5302 | 3,5302 | 0 |
| far24_kalender_min | 0,4059 | 0,4059 | 0,4059 | 0,4059 | 0,4059 | 0,4059 | 0,4059 | 0,4059 | 0 |
| far24_kalender_maks | 8,9132 | 8,9132 | 8,9132 | 8,9132 | 8,9132 | 8,9132 | 8,9132 | 8,9132 | 0 |
| far24_baris_median | 32,256 | 32,256 | 32,256 | 32,256 | 32,256 | 32,256 | 32,256 | 32,256 | 0 |
| lead_median_median | 11,5 | 11,5 | 11,5 | 11,5 | 11,5 | 11,5 | 11,5 | 11,5 | 0 |
| n_diperingatkan | 219 | 219 | 219 | 219 | 219 | 219 | 219 | 219 | 0 |
| fold_far_le6 | 7 | 7 | 7 | 7 | 7 | 7 | 7 | 7 | 0 |
| fold_gate_A_baru | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cakupan_median | 0,0903 | 0,0903 | 0,0903 | 0,0903 | 0,0903 | 0,0903 | 0,0903 | 0,0903 | 0 |

Setiap sel identik antar seed, dan delta fold terhadap seed pertama nol pada seluruh kanal sidik (0 fold berbeda maksimum, dari 9 fold). Sebabnya arsitektural: H1 tidak memiliki komponen acak. Rule kanal, residual, CUSUM, dan pemilihan h semuanya deterministik, dan parameter seed hanya dicatat ke rekaman.

### 5.2 Kontrol stokastik ML pada seed yang sama

Kontrol ini menjawab satu penjelasan alternatif: apakah nol varians itu berarti acuan seed tidak tersambung sama sekali di harness. Jalur kontrol sengaja stokastik, memakai LightGBM dengan random_state=seed, fitur 40 kolom setelah kolom label dan kolom meta dibuang, dan ambang conformal dari well kalibrasi.

| Seed | FP total | TP total | Presisi median | Recall median | FAR24 kalender median | Lead median | Diperingatkan |
|---|---|---|---|---|---|---|---|
| 42 | 1076 | 239 | 0,104 | 0,0451 | 2,2465 | 27,5 | 61 |
| 7 | 1310 | 250 | 0,1162 | 0,0363 | 1,5908 | 24 | 64 |
| 13 | 1337 | 263 | 0,1377 | 0,0574 | 2,4272 | 22 | 54 |
| 21 | 1114 | 203 | 0,0769 | 0,0121 | 1,8572 | 33 | 37 |
| 33 | 1421 | 241 | 0,1343 | 0,0214 | 1,6688 | 30,5 | 56 |

Sebaran lintas seed pada jalur kontrol: FP minimum 1076, FP maksimum 1421, rentang 345 FP; rentang presisi 0,0608; rentang recall 0,0453. Varians jalur kontrol ada: ya.

Jalur kontrol juga memperlihatkan bahwa ML saja pada konfigurasi ini jauh lebih lemah dari H1: presisi median kontrol 0,0769 sampai 0,1377, sedangkan H1 0,7789 pada semua seed. Angka ini dipakai sebagai konteks, bukan sebagai klaim keunggulan, karena kontrol tidak memakai gerbang rule kanal.

**Kesimpulan bagian 5, pernyataan stabil atau tidak:** H1 **stabil lintas seed** dengan rentang nol pada FP total, presisi, recall, FAR, dan lead. Stabilitas itu berasal dari arsitektur deterministik, bukan dari kalibrasi ambang, dan kontrol stokastik membuktikan bahwa seed benar-benar tersambung di jalur yang memakai angka acak. Jadi klaim yang sah adalah: mengubah seed tidak mengubah H1. Klaim yang tidak sah adalah: H1 sudah tervalidasi karena stabil lintas seed. Sumber variasi H1 yang nyata ada pada well dan satuan FAR, dan itu diukur di bagian 6 dan 7.

---

## 6. Nilai lapisan A/B/C pada H1 (berlaku untuk kelima seed karena hasilnya identik)

### 6.1 Lapisan A, per fold (H1_stat_dan_rule)

| Fold | TP | FP | Presisi | Recall | FAR24 kalender | FAR24 baris | Lead median | Diperingatkan | Cakupan | h | Gate A baru |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-10 | 794 | 61 | 0,9287 | 0,5696 | 8,9132 | 14,2205 | 18,5 | 10 | 0,673 | 30 | tidak |
| F-12 | 804 | 149 | 0,8437 | 0,5638 | 2,5234 | 35,9759 | 11,5 | 56 | 0,0855 | 30 | tidak |
| F-14 | 443 | 215 | 0,6733 | 0,5121 | 0,9772 | 32,4664 | 11 | 37 | 0,0327 | 30 | tidak |
| F-15A | 288 | 101 | 0,7404 | 0,4126 | 4,6255 | 26,6471 | 8 | 22 | 0,1915 | 30 | tidak |
| F-15_S | 390 | 123 | 0,7602 | 0,3927 | 1,9358 | 24,0587 | 12 | 27 | 0,0903 | 30 | tidak |
| F-5 | 410 | 104 | 0,7977 | 0,6602 | 0,4059 | 26,2231 | 5 | 25 | 0,0171 | 30 | tidak |
| F-7 | 271 | 85 | 0,7612 | 0,6437 | 5,4183 | 59,3886 | 16 | 15 | 0,1079 | 30 | tidak |
| F-9 | 256 | 55 | 0,8232 | 0,6052 | 3,5302 | 66,3873 | 2 | 18 | 0,0707 | 30 | tidak |
| F-9_A | 148 | 42 | 0,7789 | 0,4471 | 8,624 | 32,256 | 38 | 9 | 0,3004 | 30 | tidak |

Ringkasan lapisan A: FP total 935, TP total 3804; presisi median 0,7789 (rentang antar fold 0,6733 sampai 0,9287); recall median 0,5638 (rentang 0,3927 sampai 0,6602); FP pada satuan kejadian (satu run alarm berurutan dihitung satu kejadian) 263 kejadian.

FAR kalender: fold dengan FAR tidak lebih dari 6 per 24 jam berjumlah 7 dari 9, maksimum 8,9132 pada F-10 dan minimum 0,4059 pada F-5, rentang 8,5073 atau sekitar 22 kali. FAR pada satuan baris jauh lebih besar: fold yang memenuhi 6 per 24 jam baris berjumlah 0 dari 9, maksimum 66,3873 pada F-9 dan minimum 14,2205 pada F-10. Rasio median kedua satuan 9,1372, jadi lulus atau tidaknya gate FAR bergantung penuh pada satuan yang dipilih. Ini temuan utama kartu ini dan bukan detail teknis.

Definisi gate A baru (FAR kalender tidak lebih dari 6 DAN cakupan tidak kurang dari 0,5 DAN recall tidak kurang dari 0,5) dipenuhi oleh 0 dari 9 fold, karena cakupan rekaman berkisar 0,0903 secara median. Sesuai kebijakan evaluasi, gate ini dicatat sebagai informasi kekuatan bukti, bukan sebagai vonis buang.

### 6.2 Lapisan B, nilai maintenance

| Ukuran | rule kanal (R8) | H1 (S1) | Selisih |
|---|---|---|---|
| Lead median sebelum onset | 6 menit | 11,5 menit | +5,5 menit untuk H1 |
| Onset diperingatkan dalam 60 menit | 307 dari 390 | 219 dari 390 | H1 memperingatkan 88 onset lebih sedikit |
| Alarm tidak perlu per 24 jam kalender | 6,932 | 3,5302 | -3,4018 alarm per 24 jam |
| Presisi median | 0,6835 | 0,7789 | +0,0954 |
| Recall median | 0,7507 | 0,5638 | -0,1869 |

Nilai maintenance yang terukur: H1 memotong beban alarm tidak perlu sebesar 3,4018 per 24 jam kalender dan menaikkan presisi median sebesar 0,0954, dengan harga 88 onset tidak lagi diperingatkan. Lead median H1 11,5 menit memang lebih besar dari rule 6 menit, tetapi angka itu berlaku hanya pada subset onset yang masih berhasil diperingatkan, jadi bukan keunggulan mutlak.

Nilai dalam rupiah atau jam henti yang dihindari BELUM TERUKUR, karena repo tidak memuat data biaya dan jadwal inspeksi. Ini dicatat sebagai baris BELUM di ledger, bukan dikosongkan.

### 6.3 Lapisan C, ketepatan dan ketahanan

Kestabilan antar well pada H1 buruk dan harus disebut lebih dulu: FAR kalender terburuk 8,9132 (F-10) dan terbaik 0,4059 (F-5), rentang 8,5073 atau sekitar 22 kali. Artinya ambang yang sama tidak menghasilkan beban alarm yang sama antar well, sehingga klaim FAR terkendali hanya berlaku pada 7 dari 9 well.

Recall positif di semua fold (9 dari 9), jadi H1 bukan detektor yang mati di sebagian well. Lead median antar fold berkisar 2 sampai 38 menit.

### 6.4 Saturasi ambang CUSUM, batas yang paling penting

Ambang h yang terpilih pada 9 dari 9 fold adalah 30, yaitu nilai terbesar grid. Pemeriksaan laju alarm pada h tersebut terhadap anggaran 0,004167 menunjukkan anggaran TIDAK terpenuhi di seluruh fold: laju paling ringan 0,017567 dan paling berat 0,044114, keduanya di atas anggaran. Pemindaian di luar grid pada well kalibrasi F-12 menunjukkan ambang terkecil yang benar-benar memenuhi anggaran adalah 300.

Konsekuensinya harus dinyatakan tegas: pemilihan h pada H1 bukan kalibrasi yang berhasil, melainkan pemilihan nilai maksimum yang tersedia. Karena itu FAR H1 yang dilaporkan di bagian 6.1 adalah akibat langsung dari plafon grid, bukan akibat kendali anggaran. Well kalibrasi juga hanya dua (F-10, F-12) karena aturan train_wells[0], sehingga beban kalibrasi sangat bergantung pada dua well itu.

### 6.5 Perluasan grid ambang (eksploratif, bukan protokol R8)

Karena bagian 6.4 berhenti pada pertanyaan yang belum terjawab, yaitu apa yang terjadi kalau kalibrasi benar-benar diizinkan memilih ambang di atas 30, satu run eksploratif dijalankan dengan grid diperluas sampai 600. Varian ini diberi nama H1_hluas dan tidak menggantikan H1 pada tabel mana pun di atas. Artefaknya scratch/rnd/s1/s1_hluas.json dan kodenya code/rnd_s1_hluas.py.

| Fold | h terpilih | Laju alarm kalibrasi | Lolos anggaran | TP | FP | Presisi | Recall | FAR kalender | FAR baris | Lead | Diperingatkan |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-10 | 300 | 0,003924 | ya | 69 | 4 | 0,9452 | 0,0495 | 0,5845 | 0,9325 | 27,5 | 2 |
| F-12 | 150 | 0,003038 | ya | 326 | 39 | 0,8932 | 0,2286 | 0,6605 | 9,4165 | 17,5 | 30 |
| F-14 | 150 | 0,003038 | ya | 126 | 64 | 0,6632 | 0,1457 | 0,2909 | 9,6644 | 25 | 20 |
| F-15A | 150 | 0,003038 | ya | 57 | 14 | 0,8028 | 0,0817 | 0,6412 | 3,6937 | 35 | 12 |
| F-15_S | 150 | 0,003038 | ya | 56 | 12 | 0,8235 | 0,0564 | 0,1889 | 2,3472 | 11 | 5 |
| F-5 | 150 | 0,003038 | ya | 114 | 31 | 0,7862 | 0,1836 | 0,121 | 7,8165 | 35 | 15 |
| F-7 | 150 | 0,003038 | ya | 132 | 37 | 0,7811 | 0,3135 | 2,3586 | 25,8515 | 24,5 | 10 |
| F-9 | 150 | 0,003038 | ya | 213 | 34 | 0,8623 | 0,5035 | 2,1823 | 41,0394 | 2 | 14 |
| F-9_A | 150 | 0,003038 | ya | 20 | 2 | 0,9091 | 0,0604 | 0,4107 | 1,536 | 47 | 1 |

Hasil perluasan grid, dibandingkan H1 protokol R8 pada tabel yang sama: anggaran terpenuhi di 9 dari 9 fold, FP total turun dari 935 menjadi 237, presisi median naik dari 0,7789 menjadi 0,8235, FAR kalender median turun dari 3,5302 menjadi 0,5845 sehingga fold yang lulus 6 per 24 jam kalender menjadi 9 dari 9.

Harganya juga terukur dan besar: recall median turun dari 0,5638 menjadi 0,1457, onset yang mendapat peringatan turun dari 219 menjadi 109 dari 390, dan definisi gate A baru tetap dipenuhi 0 dari 9 fold karena recall minimum 0,5 tidak tercapai di fold mana pun. Lead median memang naik ke 25 menit, tetapi itu berlaku hanya pada 109 onset yang masih terperingatkan.

Kesimpulan 6.5, dan ini yang mengubah pembacaan bagian 6.4: masalahnya bukan hanya grid yang terlalu pendek. Kalau grid diperluas, kalibrasi memang berhasil menekan beban alarm sampai di bawah anggaran, tetapi detektor yang tenang itu berhenti berguna untuk peringatan dini. Dengan konfigurasi CUSUM sekarang, anggaran FAR 6 per 24 jam dan syarat recall 0,5 tidak dapat dipenuhi bersamaan pada data ini. Jadi H1 yang dilaporkan di R8 adalah titik operasi boros alarm yang mempertahankan recall, bukan titik operasi yang gagal kalibrasi karena salah hitung. Pilihan di antara keduanya adalah keputusan operasional, bukan keputusan teknis.

**Status tiga lapisan.** Lapisan A terukur penuh untuk 9 fold dan 5 seed, dan tambahan satu varian operasi pada bagian 6.5. Lapisan B terukur untuk lead dan beban alarm, belum terukur untuk nilai rupiah atau jam henti. Lapisan C terukur untuk kestabilan antar well, antar seed, dan antar titik operasi (grid sekarang lawan grid diperluas), belum terukur untuk lintas kampanye pengeboran karena tanggal kampanye tidak tersedia per baris.

---

## 7. Banding dengan konfigurasi detektor pra-riset (V9)

Sumber: scratch/v9_i1/v9_i1_RESULTS.json dan docs/V9_EVAL_C_LAYERC.md. Tidak ada run ulang untuk V9; yang dipakai adalah angka yang sudah ada di repo. Satu hal wajib disebut lebih dulu: segmen hyd_ki pada V9 hanya 10401 baris (well F-14) dengan 865 baris positif, sedangkan S1 memakai 9 fold LOWO dengan 52509 baris. Jadi membandingkan angka agregat 9 fold dengan angka satu well adalah perbandingan yang tidak sah, dan yang dilakukan di sini adalah perbandingan pada segmen yang sama, yaitu F-14.

### 7.1 Bukti satuan sebanding

| Ukuran pada F-14 | V9 pra-riset | Harness S1 (rule_kanal) | Sama |
|---|---|---|---|
| TP | 607 | 607 | ya |
| FP | 368 | 368 | ya |
| Presisi | 0,6226 | 0,6226 | ya |
| Recall | 0,7017 | 0,7017 | ya |
| FAR per 24 jam baris | 55,57 | 55,5705 | ya |

Kecocokan ini penting bukan sebagai pujian, melainkan sebagai bukti bahwa satuan FAR baris di harness memang sebanding dengan satuan V9, sehingga selisih di bagian 7.2 bisa ditafsirkan.

### 7.2 Perbandingan pada segmen F-14

| Konfigurasi | TP | FP | Presisi | Recall | FAR per 24 jam baris |
|---|---|---|---|---|---|
| V9 rule kanal (rule_display) | 607 | 368 | 0,6226 | 0,7017 | 55,57 |
| V9 persistence | 553 | 323 | 0,6313 | 0,6393 | 48,775 |
| V9 rule DAN persistence | 516 | 110 | 0,8243 | 0,5965 | 16,611 |
| S1 H1 rule DAN CUSUM | 443 | 215 | 0,6733 | 0,5121 | 32,4664 |

Hasilnya tidak menguntungkan H1 dan ditulis apa adanya: pada F-14, hybrid pra-riset (rule DAN persistence) mengungguli H1 (rule DAN CUSUM) pada keempat ukuran sekaligus, yaitu FP 110 lawan 215, presisi 0,8243 lawan 0,6733, recall 0,5965 lawan 0,5121, dan FAR baris 16,611 lawan 32,4664. H1 hanya lebih baik dari rule kanal polos dan dari CUSUM saja.

Batas perbandingan ini dinyatakan: definisi gerbang keduanya berbeda (persistence memakai y_prev pada jendela 10 menit, CUSUM memakai akumulator residual), dan penyebut baris valid berbeda tipis karena persistence membutuhkan riwayat 10 menit. Perbedaan itu tidak cukup besar untuk membalik arah selisih FP sebesar 105 alarm.

Implikasi untuk S2 dan S3, ditulis sebagai arahan bukan sebagai hasil: H1 bukan titik operasi terbaik untuk hyd pada segmen F-14, sehingga S2 dan S3 tidak boleh mengasumsikan pola statistik DAN rule selalu menang. Keduanya wajib menyertakan pembanding gerbang persistence, karena pada hyd pembanding itu sudah terbukti lebih baik pada segmen yang sama.

---

## 8. Batas pemakaian, yang belum terukur, dan penutup

### 8.1 Batas pemakaian yang mengikat

1. Angka H1 stabil lintas seed, tetapi grid ambang berhenti di 30 dan tidak satu pun fold memenuhi anggaran, sehingga FAR yang dilaporkan bukan hasil kalibrasi yang berhasil. Varian dengan grid diperluas di bagian 6.5 menunjukkan kalibrasi bisa berhasil, tetapi dengan harga recall yang jatuh. Pemakaian H1 sebagai alarm dengan beban tertentu belum sah sampai titik operasinya dipilih secara eksplisit.
2. Lulus atau tidaknya gate FAR bergantung satuan: 7 dari 9 fold lulus pada satuan kalender, 0 dari 9 lulus pada satuan baris. Setiap klaim gate wajib menyebut satuannya.
3. Cakupan rekaman median 0,0903, jadi penyebut kalender bukan waktu operasi nyata. Beban alarm per 24 jam kalender tidak boleh dibaca sebagai beban per hari kerja di lapangan.
4. Kestabilan antar well buruk (0,4059 sampai 8,9132), sehingga ambang wajib dikalibrasi per well sebelum dipakai lintas well.
5. Label hyd K-i berasal dari residu SPPA dan aliran, jadi H1 mendeteksi kondisi yang didefinisikan oleh variabel itu. Klaim prediksi kegagalan hidraulik independen adalah klaim lain yang belum diuji di sini.

### 8.2 Yang belum terukur dan mengapa

- Nilai maintenance dalam rupiah atau jam henti terhindar: BELUM, karena repo tidak memuat data biaya dan jadwal inspeksi.
- Ketahanan H1 lintas kampanye pengeboran: BELUM, karena tanggal kampanye tidak tersedia per baris pada dataset menit ini.
- Ambang h yang benar-benar memenuhi anggaran sudah diukur pada bagian 6.5, tetapi hanya untuk satu skema grid (0,5 sampai 600) dan hasilnya h berbeda antar fold (300 pada satu fold, 150 pada delapan fold lainnya), jadi belum ada satu ambang tetap yang terbukti memenuhi anggaran di semua well.
- Perilaku H1 bila komponen CUSUM diberi inisialisasi stokastik: BELUM, karena implementasi sekarang deterministik penuh sehingga tidak ada varians untuk diukur.
- Kinerja H1 pada kelas kerusakan lain: bukan lingkup kartu ini, diserahkan ke S2 (vib, ssi) dan S3 (bit_wear) yang memakai harness yang sama.

### 8.3 Ringkasan lima baris

1. Reproduksi R8 pada seed 42 LULUS persis: FP 935, presisi 0,7789, recall 0,5638, lead 11,5 menit, dan delta per fold nol pada 9 fold.
2. H1 stabil lintas 5 seed dengan rentang nol pada semua metrik, dan kontrol stokastik ML membuktikan varians itu bukan akibat plambing seed yang mati (FP kontrol 1076 sampai 1421).
3. Ketahanan yang sebenarnya menjadi masalah bukan seed, melainkan well: FAR kalender 0,4059 sampai 8,9132, dan gate FAR lulus 7 dari 9 pada satuan kalender tetapi 0 dari 9 pada satuan baris.
4. Ambang CUSUM tersaturasi di plafon grid 30 pada 9 dari 9 fold, dan setelah grid diperluas kalibrasi memang berhasil (9 dari 9 fold di bawah anggaran) tetapi recall median jatuh dari 0,5638 ke 0,1457, jadi anggaran FAR 6 dan recall 0,5 tidak dapat dipenuhi bersamaan.
5. Pada segmen F-14 yang sama, hybrid pra-riset rule DAN persistence lebih baik dari H1 pada FP, presisi, dan recall, sehingga H1 bukan peningkatan atas konfigurasi pra-riset melainkan titik operasi lain, dan harness bersama siap dipakai S2 dan S3 dengan pembanding persistence wajib disertakan.

### 8.4 Daftar yang belum terverifikasi

- Angka V9 dibaca dari artefak repo, tidak dijalankan ulang: kebenaran angka V9 bergantung pada artefak itu sendiri, bukan pada run baru di sesi ini.
- Kecocokan rule F-14 dengan V9 diverifikasi pada satu segmen saja (F-14), belum pada segmen lain karena V9 tidak menyediakan segmen lain untuk hyd.
- Ambang h di luar grid hanya diukur laju alarmnya, belum presisi dan recall-nya.
- Nilai maintenance dalam rupiah, ketahanan lintas kampanye, dan perilaku H1 dengan CUSUM stokastik tidak diukur, dan tidak ada sumber data untuk mengukurnya di repo ini.
- Kelayakan harness untuk S2 dan S3 dinilai dari API dan hasil S1, belum dari run nyata pada vib, ssi, atau bit_wear.
- Runner versi awal (02:48) membandingkan hasil dengan konstanta R8 yang ditulis di dalam skrip, sehingga tes reproduksi tidak bisa gagal bila r8_hyd.json berubah. Pada run verifikasi ini pembanding dibaca dari r8_hyd.json lalu di-assert sama dengan angka kartu, dan pengunci itu sudah diuji bisa gagal (fp_total 936 dan presisi 0,78 memicu AssertionError).
- Dokumen versi 04:37 basi dan tidak memuat bagian 6.5 maupun s1_hluas.json. Berkas ini dihasilkan ulang oleh generator pada run verifikasi, dan seluruh angka yang sudah ada di versi lama tetap sama, jadi yang berubah adalah kelengkapan, bukan nilai.
- Run verifikasi mengulang penuh lima seed plus kontrol ML dan hasilnya identik bit per bit dengan artefak 02:50 pada semua metrik H1 maupun metrik kontrol, sehingga klaim angka reprodusibel di run terpisah kini punya bukti dua artefak, bukan satu.

