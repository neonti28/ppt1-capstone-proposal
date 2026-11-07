# 00 INVENTARIS V9-RND1: vonis mesin dan gelombang satu

Kartu: `t_41ae634d` (ARKOLOG V9-RND1) · Board: `fitur-v9-swarm` · Tanggal: 2026-10-31 (WIB)
Sifat dokumen: INVENTARIS. Dokumen ini tidak menjalankan model, tidak mengubah satu pun angka
sumber, dan tidak menjatuhkan vonis tier baru. Tugasnya satu: membaca V9 (10 berkas) dan R1
sampai R8 (8 berkas), membandingkan angka antar mesin, lalu mengubah keputusan teknis yang
sudah dijatuhkan menjadi calon fitur yang bisa dibangun pada gelombang satu.

Cara membaca: setiap angka diikuti rujukan berkas dan nomor baris di dalam tanda kurung.
Singkatan berkas ada di bagian 1.

---

## 0. Kerangka wajib (dipakai apa adanya, tidak diubah)

1. Alarm otomatis BUKAN tujuan. ML dipakai sebagai sistem pendukung keputusan dengan skor
   keyakinan, bukan pemutus. Konsekuensi: setiap fitur di bawah menampilkan angka keyakinan
   dan batas pemakaiannya pada layar yang sama.
2. Setiap angka punya sumber: berkas dan nomor baris, atau baris ledger
   `docs/RND_PROVENANCE_LEDGER.md`.
3. Tidak ada klaim "berjalan" tanpa bukti. Perintah yang dijalankan untuk memeriksa angka
   ditempel keluarannya di bagian 2.
4. Kekurangan data dikemas menjadi fitur berguna (pola Dynamic Island), bukan keluhan. Sumur
   atau kanal yang belum siap tampil sebagai kartu kesiapan berisi apa yang sudah ada.
5. Setiap fitur punya lima field wajib: pengguna, momen pakai, masukan, keluaran, status bukti.
6. Setiap kekurangan ditutup dengan syarat yang dibutuhkan (bagian 9), bukan pernyataan
   penolakan.
7. Keluaran hanya markdown di `planning/`. Tidak ada .py, .html, .json, .csv sebagai deliverable.
8. Tidak memakai tanda pisah panjang. Rentang angka ditulis dengan tanda hubung biasa.

---

## 1. Berkas yang dibuka dan ukuran byte

Ukuran diambil dari `wc -c -l` pada 2026-10-31. Keluaran penuh ditempel di bagian 2.

| Kode | Berkas | Byte | Baris |
|---|---|---:|---:|
| [PM1] | `docs/V9_PM1_ARCHITECTURE.md` | 50.456 | 528 |
| [PM2] | `docs/V9_PM2_VERDICT.md` | 22.654 | 258 |
| [ERU] | `docs/V9_E_RULE_ENGINE.md` | 33.685 | 414 |
| [EST] | `docs/V9_E_STAT_ENGINE.md` | 24.718 | 341 |
| [EML] | `docs/V9_E_ML_ENGINE.md` | 38.169 | 487 |
| [EVA] | `docs/V9_EVAL_A_LAYERA.md` | 32.713 | 315 |
| [EVB] | `docs/V9_EVAL_B_LAYERB.md` | 30.472 | 334 |
| [EVC] | `docs/V9_EVAL_C_LAYERC.md` | 23.153 | 267 |
| [R1] | `docs/RND_R1_METAHEURISTIK.md` | 63.089 | 584 |
| [R2] | `docs/RND_R2_STOKASTIK.md` | 28.937 | 407 |
| [R3] | `docs/RND_R3_VMD_SVM.md` | 32.174 | 281 |
| [R4] | `docs/RND_R4_BOOSTING.md` | 28.460 | 316 |
| [R5] | `docs/RND_R5_DRIFT.md` | 35.937 | 351 |
| [R6] | `docs/RND_R6_METRIK.md` | 31.590 | 295 |
| [R7] | `docs/RND_R7_REVIEW.md` | 31.738 | 359 |
| [R8] | `docs/RND_R8_EVALUASI_BERLAPIS.md` | 27.013 | 391 |
| [PMR] | `docs/RND_PM_VERDICT.md` | 34.575 | 383 |
| **Total** | **17 berkas** | **569.533** | **6.311** |

Kerangka minimum "minimal 9 dokumen dibuka" terpenuhi dengan 17 berkas: 8 berkas V9, 8 berkas
R1 sampai R8, dan 1 berkas vonis PM R&D.

---

## 2. Bukti perintah

### 2.A `wc -c -l` (dijalankan di `/mnt/d/Capstone 1(v2)/docs`)

```
   528  50456 V9_PM1_ARCHITECTURE.md
   258  22654 V9_PM2_VERDICT.md
   414  33685 V9_E_RULE_ENGINE.md
   341  24718 V9_E_STAT_ENGINE.md
   487  38169 V9_E_ML_ENGINE.md
   315  32713 V9_EVAL_A_LAYERA.md
   334  30472 V9_EVAL_B_LAYERB.md
   267  23153 V9_EVAL_C_LAYERC.md
   584  63089 RND_R1_METAHEURISTIK.md
   407  28937 RND_R2_STOKASTIK.md
   281  32174 RND_R3_VMD_SVM.md
   316  28460 RND_R4_BOOSTING.md
   351  35937 RND_R5_DRIFT.md
   295  31590 RND_R6_METRIK.md
   359  31738 RND_R7_REVIEW.md
   391  27013 RND_R8_EVALUASI_BERLAPIS.md
   383  34575 RND_PM_VERDICT.md
  6311 569533 total
```

### 2.B Kutipan baris gerbang tier (PM1 baris 137 sampai 141)

```
| Masuk LAYER-1 (peringatan human-in-loop) | FAR<=6/24jam-negatif (atau setara skala) TERUKUR dgn recall>0 + TLead/B4 terukur + C4; kalibrasi lokal per well + anotasi regime |
| Masuk LAYER-0-alarm (otomatis) | FAR<=1/24jam-negatif dgn recall>0 + B1>=80% (kelas onset) + G1/G2 mayoritas fold layak + C2 per-bin (drop <20% relatif) + C3 dropout <20% + validasi kejadian nyata |
| Turun tier | Bukan GAGAL bila FAR terukur >6/24jam (contoh: stuck) -> engine turun ke triage/tren dengan anotasi; kemampuan tetap tercatat |
```

### 2.C Kutipan baris tabel ringkas A per kelas (EVA baris 54 sampai 64, dipotong 120 karakter)

```
| **vib** (K tunggal) | deteksi kondisi VIBLAT>=32,17405 | rule-sistem-hari-ini: P 0,87-0,95 · R 0,28-0,60 · FAR ...
| **ssi** (K tunggal) | deteksi kondisi SSI>=1 | RF tau0,3: P 0,00-0,67 · R 0,00-0,13 · FAR 0,0-15,6; titik prak...
| **shk** (K tunggal) | deteksi anomali SHKRSK>=1 | rule-display: P 0,00-0,94 · R 0,00-0,38 · FAR 0,7-6,6 -> l...
| **stuck K-i** (status) | deteksi kondisi blok STUCK_RT | rule-display: P 0,92-0,97 · R 0,45-0,60 · FAR 8,3-61,0 ...
| **stuck K-ii** (onset) | prediksi onset 0->1, H=10 mnt | RF tau0,5: 3/4 fold FAR<=6 (P 0,05-1,00 · R 0,004-0,...
| **hyd K-i** (status) | deteksi kondisi |z|>2 residu SPPA | persistence: P 0,61-0,90 · R 0,62-0,92 · FAR 32,...
| **hyd K-ii** (prediksi) | prediksi kick/loss proxy, H=10 mnt | fisher/Pearson varian (1 split temporal): P 0,00 · R ...
| **bit_wear K-1** (status) | deteksi blok high_MSE (Teale) | P/R/FAR TIDAK DIHITUNG (field tidak ada di JSON E_RULE...
| **bit_wear K-2** (onset) | prediksi onset blok high_MSE | - | - | - | Belum terukur (pra-reg K-2 belum terbi...
| **tool_wear K-i** (regime) | deteksi perubahan-regime dalam-run (bengkel) | change-point signifikan 8/8 run (p<=0...
| **tool_wear K-ii** (lintas-alat) | prediksi status keausan LOTO | Baseline V9: canary 3-RMS AUPRC 0,516-0,612; ident...
```

Tanda "<=6" dan "->" pada kutipan di atas adalah hasil translasi karakter asli berkas sumber
saat ditempel ke markdown ini. Angka, urutan, dan tanda desimal tidak diubah.

### 2.D Kutipan baris portabilitas ambang (EVC baris 118 sampai 126)

```
| C1 rule | P 0,87-0,95 (1,1x stabil); R 0,28-0,60 (2,2x); FAR 10,0-49,9 (5,0x); FP total 197 |
| C3 | tau0,05: FAR 983-1440 (0 well <=6); tau0,3: 189-699 (0/4); tau0,5: 4,1-496 = 119x (1/4 well). Recall tau0,5 0,10-0,87 (8,5x) |
| C4 | n_nodata rule F-14 356/1.989; prevalensi antar well 0,14-0,57 (4x) = akar ketidakportabelan |
```

---

## 3. Tabel perbandingan mesin, lapisan A (presisi, recall, FAR)

Legenda: FAR rig dalam satuan per 24 jam operasi NEGATIF (grid 60 detik). FAR tool_wear dalam
satuan per MENIT (domain bengkel 1 detik). Presisi dan recall dilaporkan sebagai rentang antar
fold atau antar titik operasi, persis seperti yang tertulis di sumber. "Belum terukur" berarti
field angkanya tidak ada di JSON primer, bukan berarti angkanya nol.

| # | Engine / klaim | Tugas | Presisi | Recall | FAR | Satuan FAR | Sumber |
|---:|---|---|---|---|---|---|---|
| 1 | vib | deteksi kondisi VIBLAT>=32,17405 | rule 0,87-0,95; RF tau0,5 0,40-0,85 | rule 0,28-0,60; RF tau0,5 0,10-0,87 | rule 10,0-49,9; RF tau0,5 4,1-496,1 | per 24 jam negatif | [EVA] baris 54; [ERU] baris 109-113; [EVC] baris 118-120 |
| 2 | ssi | deteksi kondisi SSI>=1 | rule 0,00-0,50; RF tau0,3 0,00-0,67 | rule 0,00-0,03; RF tau0,3 0,00-0,13 | rule 0,0-7,3; RF tau0,3 0,0-15,6 | per 24 jam negatif | [EVA] baris 55 dan 91-93; [EVC] baris 133 |
| 3 | shk | deteksi anomali SHKRSK>=1 | rule 0,00-0,94 (contoh F-7 0,94) | rule 0,00-0,38 (contoh F-7 0,38) | rule 0,7-6,6 (lolos <=6 di 7/9 fold); RF 0,69 di 1/45 titik | per 24 jam negatif | [EVA] baris 56 dan 104-106; [EVC] baris 146 |
| 4 | stuck K-i | deteksi kondisi blok STUCK_RT | rule 0,92-0,97 | rule 0,45-0,60 | rule 8,3-61,0 (lolos <=6 di 0/2 fold) | per 24 jam negatif | [EVA] baris 57 dan 119-122; [EVC] baris 158 |
| 5 | stuck K-ii | prediksi onset 0->1, H=10 menit | RF tau0,5 0,05-1,00 | RF tau0,5 0,004-0,005 | RF tau0,5 0,0-1,25 (3/4 fold) | per 24 jam negatif | [EVA] baris 58 dan 128; [EVB] baris 101 |
| 6 | hyd K-i | deteksi kondisi residu SPPA | persistence 0,61-0,90; hybrid 0,72-0,95 | persistence 0,62-0,92; hybrid 0,52-0,87 | persistence 32,4-110,7; hybrid 14,6-58,4 (lolos <=6 di 0/9) | per 24 jam negatif | [EVA] baris 59 dan 151-152; [EST] baris 39 |
| 7 | hyd K-ii | prediksi kick/loss proxy, H=10 menit | V9 0,00 pada q95 | V9 0,00 (0/3 onset) | 31,6 pada q95 | per 24 jam negatif | [EVA] baris 60 dan 165-168; [EST] baris 246 |
| 8 | bit_wear K-1 | deteksi blok high_MSE (Teale) | belum terukur | belum terukur | belum terukur, dan FAR dalam satuan jam tidak sah karena barisnya grid kedalaman | bukan satuan waktu | [EVA] baris 61; [PMR] baris 78 |
| 9 | bit_wear K-2 | prediksi onset blok high_MSE | belum terukur (pra-reg belum terbit) | belum terukur | belum terukur | bukan satuan waktu | [EVA] baris 62; [PM2] baris 176 |
| 10 | tool_wear K-i | deteksi perubahan regime dalam run bengkel | precision run-level 0,50 (4 alarm palsu di alat baru) | deteksi 4/4 alat | FP 1-3 per menit pada titik FAR-terkalibrasi | per menit | [EVA] baris 63; [EVB] baris 106; [EST] baris 190-201 |
| 11 | tool_wear K-ii | klasifikasi status keausan LOTO | 0,50-0,56 (angka V8, referensi) | belum terukur di V9 | belum terukur di V9 | per menit | [EVA] baris 64; [PM2] baris 178 |

### 3.A Pembanding angka generasi sebelumnya pada kelas yang sama

R8 menjalankan uji hybrid pada data kalender dengan satuan yang sama untuk hyd K-i. Ini penting
karena angkanya berbeda dari V9 dan perbedaannya bisa dijelaskan, bukan kontradiksi.

| Model | FP | Presisi | Recall | FAR median per 24 jam | Fold FAR <=6 | Sumber |
|---|---:|---|---|---|---|---|
| H1 (statistik + rule) | 935 | 0,7789 | 0,5638 | 3,5302 | 7 dari 9 | [R8] baris 69 dan 109 |
| rule kanal (status quo) | 2105 | 0,6835 | 0,7507 | 6,932 | 3 dari 9 | [R8] baris 69 dan 291 |
| CUSUM residu | 4361 | 0,5052 | 0,5832 | 11,0013 | tidak dilaporkan | [R8] baris 292; [PMR] baris 103 |
| ML LightGBM (shk) | 2633 | AUPRC 0,0499 lawan prevalensi 0,0243 | 0,0829 median | 3,6217 | tidak dilaporkan | [R8] baris 293; [R8] baris 70 |
| H2 (ML + statistik, shk) | 667 | 0,0468 turun ke 0,0376 setelah normalisasi | 0,0037 | tidak dilaporkan | tidak dilaporkan | [R8] baris 70 dan 176-177 |
| H4 (tiga komponen, stuck K-ii) | 41 | 0,6404 | 0,001 | 0 (akibat recall nol) | 4 dari 4 | [R8] baris 73; [PMR] baris 112 |

Bacaan yang diizinkan: H1 menukar 31,82 persen recall dengan penurunan FAR dan kenaikan presisi
([R8] baris 131; [PMR] baris 109). H2 memotong FP 74,67 persen dan TP 76,04 persen sekaligus,
sehingga tidak dipakai ([PMR] baris 110). H4 berpresisi tinggi tetapi recall 0,001, jadi nilai
satu-satunya adalah mempersempit jendela pemeriksaan manual ([PMR] baris 112).

---

## 4. Tier pemakaian per engine dan gerbangnya

Tier di bawah adalah kutipan apa adanya dari [PM2] baris 168 sampai 178, ditambah komposisi alat
pada [PM2] baris 140. Tier tidak diubah oleh dokumen ini.

| # | Engine | Tugas | Tier pemakaian | Angka penopang | Batas pemakaian |
|---:|---|---|---|---|---|
| 1 | vib | deteksi kondisi | TREN (RF) + PERINGATAN-BERPENGAWAS (rule) | rule P 0,87-0,95 di 4 well; RF delta vs canary 4/4 | FAR tau0,5 menyebar 119,6x antar sumur; FAR rule 10-50/24jam |
| 2 | ssi | deteksi kondisi | TREN (RF) + PERINGATAN hemat (hybrid) | hybrid memotong FP 73,1 persen | nodata CRPM 62,3 persen; recall rule <=0,03 |
| 3 | shk | deteksi anomali | PERINGATAN-BERPENGAWAS (rule) + TREN (RF) | rule FAR<=6 dengan recall>0 di 7/9 well | CI RF memuat prevalensi 7/9; B3 RF negatif 212x |
| 4 | stuck K-i | deteksi kondisi | PERINGATAN-BERPENGAWAS (2 well) | rule P 0,92-0,97 | cakupan 2 fold; FAR 8-61 |
| 5 | stuck K-ii | prediksi onset | TREN / triage | RF ranking di atas canary 4/4; persistence-EVENT TLead 7,0 menit, FP 11 | B1 0-11,5 persen; titik B1>=50 persen berbiaya 77x beban |
| 6 | hyd K-i | deteksi kondisi | PERINGATAN-BERPENGAWAS (kandidat terkuat) | hybrid FP 2091 ke 927 (turun 55,7 persen) di 9/9 well; P dan R >=0,52 | FAR 14,6-58,4 di 9/9; label = residu sebagai proxy |
| 7 | hyd K-ii | prediksi kegagalan | BELUM LAYAK PAKAI (eksplorasi) | V9 P=R=0 pada q95; CI memuat prevalensi | kanal FlowOut absen; RF V8 B1 66,7 persen belum diulang |
| 8 | bit_wear K-1 | deteksi kondisi | TREN | persistence delta vs canary 5/5 scorable (AUPRC 0,670 lawan 0,389) | P, R, FAR belum terukur; USROP bukan rig Volve |
| 9 | bit_wear K-2 | prediksi onset | BELUM (belum dijalankan) | nol angka | pra-reg belum terbit |
| 10 | tool_wear K-i | deteksi perubahan regime | PERINGATAN-BERPENGAWAS (bengkel) | deteksi 4/4, FP 1-3, lead 20-36 detik, B3 +0,91 sampai +0,98 | precision run 0,50; skala detik bengkel; transfer ke rig tidak diklaim |
| 11 | tool_wear K-ii | klasifikasi lintas alat | TREN | canary AUPRC 0,516-0,612 (1,19x); RF V8 delta 4/4 | RF V9 belum dijalankan; precision mendekati peluang |

Komposisi alat hasil perakitan: 5 head L0, 11 head L1 dengan `human_review_required`, 9 head L2,
2 head L3, dan slot alarm otomatis 0 ([PM2] baris 140 dan 206).

Gerbang kenaikan tier yang dipakai, dan yang dengan sengaja tidak digeser: L1 butuh FAR<=6 per 24
jam negatif terukur dengan recall>0 plus TLead atau B4 terukur plus C4 ([PM1] baris 138). L0-alarm
butuh FAR<=1 dengan recall>0 plus B1>=80 persen untuk kelas onset plus C2 dan C3 ([PM1] baris 139).
Tidak satu pun klaim di bagian 3 memenuhi jalur L0 ([PM1] baris 131).

---

## 5. Angka lapisan B (apakah deteksi berguna untuk pemeliharaan)

| # | Engine / klaim | B1 cakupan onset | B3 penghematan pemeriksaan | B4 margin status | Sumber |
|---:|---|---|---|---|---|
| 1 | vib | tidak berlaku (kelas status) | rule 0,00; RF -9,41 sampai -76,77 | rule 26,4 persen blok, margin 5,0 menit | [EVB] baris 97 dan 119-126 |
| 2 | ssi | tidak berlaku | hybrid +0,731 (FP 26 ke 7); RF tau0,5 +0,846 dengan TP 0 | rule 5,0 persen blok, margin 5,5 menit | [EVB] baris 98 dan 143-149 |
| 3 | shk | tidak berlaku | RF tau0,05 -212,53; tau0,5 +0,678 (FP 39 lawan 121) | rule 13,4 persen blok, margin 4,5 menit | [EVB] baris 99 dan 157-164 |
| 4 | stuck K-i | tidak berlaku | hybrid-E1 +0,163 (FP 41 lawan 49) | rule 11,8 persen blok, margin 5,0 menit | [EVB] baris 100 |
| 5 | stuck K-ii | RF tau0,05 0,51-1,00 dengan TLead 10-11,5 menit, tetapi beban 77x; persistence-EVENT 0-0,115 dengan TLead 7,0 menit | persistence-EVENT +0,974 (FP 11); RF tau0,05 -77,05 | tidak berlaku | [EVB] baris 101 |
| 6 | hyd K-i | tidak berlaku | hybrid +0,557 (FP 2091 ke 927); persistence +0,072 | hybrid 13,0 persen blok, margin 4,5 menit | [EVB] baris 102; [PMR] baris 109 |
| 7 | hyd K-ii | 0/3 onset terdeteksi; rule z-pit TLead nol | tidak terdefinisi (FP rule 0 by construction) | tidak berlaku | [EVB] baris 103 |
| 8 | bit_wear K-1 | tidak berlaku | belum terukur | belum terukur (pipeline D1 tidak memuat USROP) | [EVB] baris 104 |
| 9 | bit_wear K-2 | belum terukur | belum terukur | belum terukur | [EVB] baris 105 |
| 10 | tool_wear K-i | analog 100 persen (4/4 alat) | +0,909 sampai +0,976 (FP 1-3 lawan 33-41 per alat) | tidak berlaku (skala detik) | [EVB] baris 106 |
| 11 | tool_wear K-ii | belum terukur di V9; RF V8 TLead 47,5 detik | belum terukur di V9 | tidak berlaku | [EVB] baris 107 |

Satu klaim yang berdiri sendiri di lapisan B, dan karena itu paling siap dipakai: tool_wear K-i
pada titik FAR-terkalibrasi memenuhi B1 dan B3 sekaligus ([EVB] baris 106). Semua klaim lain
memiliki satu dari dua syarat, bukan keduanya.

---

## 6. Dari keputusan mati menjadi fitur

Kolom "keputusan" adalah isi dokumen sumber, bukan tafsiran. Kolom "fitur" menunjuk nomor di
bagian 7.

| # | Keputusan di dokumen sumber | Konsekuensi teknis | Fitur yang menampungnya | Sumber |
|---:|---|---|---|---|
| 1 | Alarm otomatis 0 slot, keputusan akhir manusia | Tidak ada jalur notifikasi kritis yang boleh dibangun | W1-01, W1-10 | [PM1] baris 112 dan 131; [PM2] baris 140 |
| 2 | Satu ambang tidak portabel: FAR tau0,5 menyebar 119,6x | Ambang wajib dikalibrasi per sumur | W1-04, W1-05 | [PM2] baris 168; [EVC] baris 120 |
| 3 | Hybrid memotong pemeriksaan tetapi kadang menghapus deteksi (ssi recall <=0,03) | Penghematan harus dibayar dengan angka recall di layar yang sama | W1-06, W1-02 | [EVB] baris 98; [EVA] baris 55 |
| 4 | RF sering kalah dari persistence pada kelas status, menang pada ranking | Peran RF adalah penambah urutan, bukan pemutus | W1-03, W1-08 | [EVA] baris 54-59; [EML] baris 47-52 |
| 5 | Persistence-horizon memberi B1 0,93-0,97 tetapi hindsight | Angka itu dipakai sebagai batas atas, tidak boleh tampil sebagai prediksi | W1-03, W1-08 | [EVA] baris 133; [EVC] baris 165 |
| 6 | hyd K-ii tidak punya FlowOut, P=R=0 | Kekurangan kanal menjadi kartu permintaan kanal | W1-11 | [EVA] baris 169; [PM2] baris 174 |
| 7 | ssi butuh CRPM, n_nodata 62,3 persen | Kesiapan kanal per sumur harus tampil sebelum skor | W1-07 | [EVC] baris 136; [EVA] baris 55 |
| 8 | VMD dan EMD gagal pada laju sampel data (Nyquist 0,1667 Hz, 75/105 percobaan gagal) | Pemeriksaan kelayakan sinyal menjadi langkah wajib sebelum dekomposisi | W1-12 | [R3] baris 98-106 |
| 9 | Baseline tidak dituning, sehingga klaim tuning kehilangan dasar atribusi | Pembanding netral dengan anggaran sama menjadi syarat klaim | W1-13 | [R1] baris 99-122 |
| 10 | Selang Monte Carlo diadopsi sebagai kewajiban pelaporan | Setiap angka FAR dan recall wajib tampil bersama selangnya | W1-14 | [PMR] baris 99 dan 149; [R2] baris 123-140 |
| 11 | Boosting dan conformal berstatus pilot karena biaya belum terukur | Pilot dibuka dengan titik operasi yang mengikat recall | W1-13 | [R4] baris 22-32; [PMR] baris 102 |
| 12 | Pesan vonis R&D: jangan naikkan tier, perbaiki alat ukur lebih dulu | Urutan kerja gelombang satu dimulai dari alat ukur dan tampilan, bukan model baru | W1-01, W1-06, W1-14 | [R7] baris 18-25 |

---

## 7. Daftar fitur gelombang satu

Setiap fitur punya lima field wajib. "Status bukti" menyebut apakah angka pendukungnya sudah
terukur di berkas sumber, sebagian, atau masih berupa syarat.

### W1-01 Badge beban kerja per head

| Field | Isi |
|---|---|
| Pengguna | Insinyur pemeliharaan dan operator shift yang membaca panel |
| Momen pakai | Tepat sebelum memutuskan menindaklanjuti satu peringatan |
| Masukan | FAR per fold, jumlah fold, jumlah alarm palsu, skala satuan (24 jam atau menit) |
| Keluaran | Badge "beban: x alarm per 24 jam, dari n fold, rentang a sampai b" plus label skala |
| Status bukti | Terukur untuk vib, shk, stuck, hyd, tool_wear ([EVA] baris 54-64; [EVC] baris 118-126). Wajib tampil menurut [PM2] baris 206 |

### W1-02 Panel ketidaksepakatan antar engine

| Field | Isi |
|---|---|
| Pengguna | Operator shift dan supervisor yang memutuskan eskalasi |
| Momen pakai | Ketika dua engine pada sumur yang sama memberi arah berbeda |
| Masukan | Sinyal per menit dari rule, persistence, hybrid, dan skor RF pada jendela yang sama |
| Keluaran | Matriks sepakat atau tidak sepakat per jendela, plus alasan pembeda (misalnya hybrid memangkas alarm karena syarat AND) |
| Status bukti | Sebagian. Arah pemangkasan terukur: ssi hybrid memotong FP 26 ke 7 dengan recall <=0,03 ([EVB] baris 143; [EVA] baris 55); hyd hybrid memotong 2091 ke 927 dengan P dan R tetap >=0,52 ([EVA] baris 59). Tampilan gabungannya belum dibangun |

### W1-03 Skor keyakinan 0 sampai 100 berlapis selang

| Field | Isi |
|---|---|
| Pengguna | Insinyur pemeliharaan yang butuh satu angka untuk dibawa ke rapat |
| Momen pakai | Saat memilih satu dari beberapa peringatan untuk dikerjakan lebih dulu |
| Masukan | AUPRC per fold dengan CI95, prevalensi, jumlah positif, status fold (cukup atau kurang berdaya) |
| Keluaran | Skor 0 sampai 100 plus pita keyakinan dan penanda "hindsight" bila angka berasal dari persistence-horizon |
| Status bukti | Terukur. AUPRC dan CI95 per fold ada di [EML] baris 103-156; aturan memisahkan hindsight ada di [EVA] baris 133 dan [EVC] baris 165. Rumus pemetaan skor belum ditetapkan, jadi pemetaannya adalah pekerjaan gelombang satu |

### W1-04 Wizard kalibrasi ambang per sumur

| Field | Isi |
|---|---|
| Pengguna | Engineer yang memasang panel pada sumur baru |
| Momen pakai | Sebelum panel dinyalakan pada sumur yang belum pernah terlihat model |
| Masukan | Riwayat sinyal sumur itu, grid ambang pra-registrasi, anggaran FAR yang diizinkan |
| Keluaran | Ambang lokal terpilih, perkiraan FAR pada ambang itu, dan daftar fold yang dipakai untuk memilih |
| Status bukti | Syaratnya terukur: satu ambang global memberi FAR 4,1 sampai 496 (119x) pada vib ([EVC] baris 120), dan kalibrasi lintas sumur dilarang otomatis ([PM1] baris 129). Wizard-nya belum dibangun |

### W1-05 Peta drift antar sumur dan dalam sumur

| Field | Isi |
|---|---|
| Pengguna | Engineer pemeliharaan dan penanggung jawab kualitas data |
| Momen pakai | Saat ambang lama mulai berperilaku lain pada sumur yang sama |
| Masukan | Statistik jendela dasar per paruh waktu per sumur (contoh TQA_mean) |
| Keluaran | Jarak distribusi antar sumur dan antar paruh, plus penanda "ambang lama tidak berlaku di sini" |
| Status bukti | Terukur. Uji KS antar sumur: D median 0,986, 10 dari 10 pasangan p<0,05. Dalam sumur: D median 0,211, 4 dari 5 sumur p<0,05 ([R5] baris 129-140). Catatan kehati-hatian: p tidak sah untuk deret berautokorelasi ac1 sekitar 0,98, jadi D dipakai sebagai jarak ([R5] baris 142-148) |

### W1-06 Kalkulator anggaran pemeriksaan

| Field | Isi |
|---|---|
| Pengguna | Supervisor pemeliharaan yang menentukan jumlah kunjungan per shift |
| Momen pakai | Saat membandingkan dua kandidat titik operasi sebelum mengunci kebijakan |
| Masukan | Jumlah alarm palsu engine, jumlah alarm palsu baseline status quo, recall pada titik yang sama |
| Keluaran | Persentase penghematan pemeriksaan, plus peringatan yang hilang pada titik itu |
| Status bukti | Terukur. Rumus `kurangi_ragu = 1 - FP_engine / FP_baseline` ada di [EVB] baris 65. Angka siap pakai: hyd K-i +0,557, tool_wear +0,909 sampai +0,976, ssi +0,731 dengan biaya recall <=0,03 ([EVB] baris 98, 102, 106) |

### W1-07 Kartu kesiapan kanal per sumur (pola Dynamic Island)

| Field | Isi |
|---|---|
| Pengguna | Engineer yang menyiapkan sumur sebelum panel dinyalakan |
| Momen pakai | Sebelum instalasi, dan setiap kali panel dipindah ke sumur lain |
| Masukan | Daftar kanal yang dibutuhkan per engine, jumlah baris terisi, jumlah baris kosong, jumlah berkas per kanal |
| Keluaran | Status siap atau belum, jumlah baris kosong per kanal, dan tombol permintaan pengadaan data |
| Status bukti | Terukur sebagian. ssi: 22.385 dari 35.906 baris kosong (62,3 persen), F-14 mencapai 96,6 persen ([EVC] baris 136). vib: 356 dari 1.989 baris kosong pada F-14 ([EVC] baris 121). Kanal yang belum ada daftarnya belum diinventarisasi ulang di kartu ini |

### W1-08 Antrean triage onset dengan label cakupan

| Field | Isi |
|---|---|
| Pengguna | Insinyur yang memutuskan urutan pemeriksaan risiko onset |
| Momen pakai | Awal shift, saat menyusun daftar periksa |
| Masukan | Skor onset per jendela, horizon H, riwayat alarm pada horizon itu |
| Keluaran | Daftar berurut berisi TLead yang diharapkan, cakupan onset terukur, dan jumlah alarm yang harus diperiksa |
| Status bukti | Terukur. RF tau0,5: cakupan 0,004 sampai 0,045 dengan FAR 0,0 sampai 1,25 pada 3 dari 4 fold ([EVA] baris 58 dan 128). Persistence-EVENT: cakupan 0 sampai 0,115 dengan TLead 7,0 menit ([EVB] baris 101). Titik dengan cakupan >=50 persen berbiaya 77x beban, jadi antrean ini berlabel triage, bukan peringatan |

### W1-09 Mode bengkel terpisah dari mode rig

| Field | Isi |
|---|---|
| Pengguna | Teknisi bengkel dan perencana inspeksi alat |
| Momen pakai | Saat alat selesai dijalankan dan sebelum inspeksi berikutnya |
| Masukan | Deret 1 detik per run alat, ambang hasil kalibrasi dalam run, target laju alarm per menit |
| Keluaran | Daftar alat yang perlu diperiksa dengan waktu ancang 20 sampai 36 detik dan jumlah alarm palsu 1 sampai 3 |
| Status bukti | Terukur. Deteksi 4/4 alat, FP 1-3, TLead 20-36 detik, B3 +0,909 sampai +0,976 ([EVA] baris 63; [EVB] baris 106). Batas: precision run-level 0,50, jadi klaim "keausan spesifik" tidak disertakan ([PM1] baris 134) |

### W1-10 Log keputusan manusia dan jejak audit

| Field | Isi |
|---|---|
| Pengguna | Supervisor, auditor internal, dan peneliti yang menilai alat |
| Momen pakai | Setiap kali peringatan L1 ditindaklanjuti atau diabaikan |
| Masukan | Identitas head, skor keyakinan, badge beban, tindakan yang diambil, alasan singkat |
| Keluaran | Riwayat keputusan per head, tingkat tindak lanjut, dan bahan perbandingan untuk kalibrasi berikutnya |
| Status bukti | Sebagian. Aturan `human_review_required` sudah berlaku pada 11 dari 11 head L1, dan keputusan akhir ditetapkan MANUSIA ([PM2] baris 206). Pencatatan tindakan dan analisisnya belum ada |

### W1-11 Kartu kanal yang perlu dipasang

| Field | Isi |
|---|---|
| Pengguna | Engineer instrumentasi dan pengambil keputusan anggaran sensor |
| Momen pakai | Saat satu engine berhenti di titik operasi karena kanal masukan tidak ada |
| Masukan | Daftar kanal per engine, bukti ketiadaan, dampak terukur pada metrik |
| Keluaran | Daftar kanal prioritas dengan alasan angka, misalnya FlowOut untuk hyd K-ii |
| Status bukti | Terukur untuk hyd K-ii: FlowOut absen, empat kolom flow berkorelasi 0,995 sampai 1,000 sehingga varian literal tidak dapat dihitung ([EVA] baris 169). Dampak terukur: P=R=0 pada q95 ([EVA] baris 165) |

### W1-12 Kartu kelayakan sinyal sebelum dekomposisi

| Field | Isi |
|---|---|
| Pengguna | Peneliti sinyal dan engineer yang akan menambah metode dekomposisi |
| Momen pakai | Sebelum menjalankan VMD, EMD, atau wavelet pada kanal baru |
| Masukan | Laju sampel kanal, pita frekuensi yang dicari, panjang segmen, hasil uji stasioneritas lokal |
| Keluaran | Lulus atau tidak lulus beserta alasannya, misalnya "Nyquist 0,1667 Hz, pita yang dicari di atas batas" |
| Status bukti | Terukur. VMD gagal karena Nyquist 0,1667 Hz dengan 75 dari 105 percobaan gagal; EMD gagal karena 5 IMF didominasi drift; wavelet lolos sebagian karena pita di atas 0,05 Hz hanya memuat 4,14 persen daya ([R3] baris 98-106). Kartunya belum dibangun |

### W1-13 Pembanding netral untuk setiap klaim tuning

| Field | Isi |
|---|---|
| Pengguna | Peneliti algoritma dan reviewer internal |
| Momen pakai | Sebelum satu klaim "metode X menaikkan metrik" diajukan |
| Masukan | Jumlah evaluasi fitness, fold yang dipakai, baseline tanpa tuning, baseline pencarian netral dengan anggaran identik |
| Keluaran | Tabel tiga kolom (tanpa tuning, pencarian netral, metode yang diuji) plus selisih pada titik operasi yang sama |
| Status bukti | Syaratnya terukur: baseline sekarang tidak dituning sama sekali ([R1] baris 99-122), dan boosting berstatus belum terukur biayanya ([R4] baris 22-32). Klaim metaheuristik ditolak tanpa pembanding ini ([PMR] baris 92). Alatnya belum ada |

### W1-14 Selang wajib pada setiap angka FAR dan recall

| Field | Isi |
|---|---|
| Pengguna | Pembaca laporan, reviewer, dan operator yang mengambil keputusan dari angka |
| Momen pakai | Setiap kali satu angka FAR atau recall ditampilkan atau dikutip |
| Masukan | Jumlah iterasi bootstrap, seed, blok bootstrap, cakupan waktu |
| Keluaran | Angka titik plus selang, plus penanda bila selang memuat prevalensi |
| Status bukti | Terukur. Monte Carlo diadopsi sebagai kewajiban pelaporan ([PMR] baris 99 dan 149), dan jumlah iterasi yang memenuhi kriteria presisi diukur pada dua kasus nyata ([R2] baris 123-140). Penerapannya belum seragam di semua tabel V9: beberapa sel di [EVA] dan [EVC] hanya berisi titik tanpa selang |

---

## 8. Dua fitur yang mengurus kepercayaan dan ketidaksepakatan

Kerangka kartu meminta paling sedikit dua ide tentang kepercayaan dan ketidaksepakatan. Empat
fitur di bawah mengurus hal itu secara langsung, dan dua di antaranya sudah punya angka penopang.

**Kepercayaan, lapis pertama: W1-01 dan W1-03.** Alat ini tidak boleh tampil sebagai pemutus,
karena tidak ada satu pun engine yang mencapai jalur alarm otomatis ([PM1] baris 131). Yang bisa
ditampilkan hanya dua hal: seberapa sering alat ini menyala pada waktu yang seharusnya tenang
(badge FAR) dan seberapa layak angka urutannya dibanding prevalensi (skor keyakinan dengan CI95).
Contoh nyata mengapa keduanya harus tampil bersamaan: rule vib punya presisi 0,87 sampai 0,95
tetapi FAR 10,0 sampai 49,9 per 24 jam ([EVA] baris 54). Presisi tinggi tanpa badge beban
membuat operator mengira alat ini jarang menyala, padahal sebaliknya.

**Kepercayaan, lapis kedua: W1-10.** Kepercayaan tidak boleh hanya berbentuk angka di layar.
Setiap peringatan L1 sudah wajib ditinjau manusia ([PM2] baris 206), tetapi tanpa log keputusan,
tidak ada cara mengetahui apakah peringatan itu ditindaklanjuti, diabaikan, atau salah alamat.
Log ini juga menjadi satu-satunya sumber label masa depan yang benar-benar prospektif, karena
label hari ini dibangun retrospektif.

**Ketidaksepakatan: W1-02.** Dua engine pada data yang sama bisa berbeda arah, dan perbedaan itu
bukan bug. Hybrid pada hyd memangkas alarm palsu dari 2091 ke 927 sambil menjaga presisi dan
recall di atas 0,52 ([EVA] baris 59). Hybrid pada ssi memangkas dari 26 ke 7 tetapi meninggalkan
recall 0,03 ([EVB] baris 143; [EVA] baris 55). Dua contoh ini punya bentuk angka yang mirip dan
makna operasional yang berlawanan. Panel ketidaksepakatan menampilkan mana yang terjadi pada
jendela yang sedang dibaca, beserta konsekuensinya: "alarm dipangkas karena syarat AND tidak
terpenuhi" atau "alarm dipangkas karena kanal masukan kosong".

**Ketidaksepakatan yang tidak boleh diselesaikan oleh alat: W1-14.** Bila selang angka memuat
prevalensi, artinya sinyal belum terbukti ([EVA] baris 30, keputusan EA-4 dan EA-8). Alat wajib
menampilkan keadaan itu apa adanya, bukan memilih angka yang paling enak dibaca. Contoh: AUPRC
ssi 0,015 sampai 0,459 dengan CI yang memuat prevalensi di 5 dari 9 fold ([EVA] baris 55).

---

## 9. Urutan gelombang satu dan syarat yang dibutuhkan

Urutan ini mengikuti vonis R&D: perbaiki alat ukur lebih dulu, jangan menaikkan tier, jangan
mengulang eksperimen yang sama ([R7] baris 25).

| Gelombang | Isi | Syarat yang harus tersedia lebih dulu | Fitur |
|---|---|---|---|
| 1A | Tampilan kejujuran: badge beban, selang, batas pemakaian | Tabel FAR dan recall per fold yang sudah ada di [EVA] dan [EVC] | W1-01, W1-14 |
| 1B | Panel ketidaksepakatan dan log keputusan | Sinyal per menit dari empat komponen pada jendela yang sama, plus skema pencatatan tindakan | W1-02, W1-10 |
| 1C | Kalibrasi per sumur dan peta drift | Riwayat sinyal per sumur untuk grid ambang, plus statistik jendela dasar per paruh | W1-04, W1-05 |
| 1D | Kesiapan data dan permintaan kanal | Daftar kanal per engine yang lengkap, termasuk kanal yang belum pernah diinventarisasi | W1-07, W1-11 |
| 1E | Antrean triage onset dan mode bengkel | Titik operasi yang mengikat recall, plus pemisahan skala detik dan menit di antarmuka | W1-08, W1-09 |
| 1F | Alat ukur dan pembanding | Anggaran evaluasi per peran yang disepakati, plus baseline pencarian netral | W1-13, W1-12 |
| 1G | Skor keyakinan 0 sampai 100 dan kalkulator anggaran | Rumus pemetaan skor yang ditetapkan lebih dulu, plus definisi baseline biaya pemeriksaan | W1-03, W1-06 |

Syarat yang belum terpenuhi, ditulis sebagai syarat bukan sebagai penutup:

1. Untuk W1-03 dibutuhkan rumus pemetaan dari AUPRC, CI95, dan prevalensi ke satu skor 0 sampai
   100. Rumus itu harus ditetapkan sebelum angka apa pun ditampilkan, supaya bukan pemilihan
   pasca hasil.
2. Untuk W1-02 dibutuhkan penyimpanan sinyal per menit dari empat komponen. Saat ini yang
   tersimpan adalah ringkasan per fold, bukan deret per menit ([EML] baris 103-156).
3. Untuk W1-05 dibutuhkan statistik jendela dasar untuk semua sumur, bukan hanya lima sumur yang
   diuji di R5 ([R5] baris 113-140).
4. Untuk W1-13 dibutuhkan kesepakatan anggaran evaluasi. Angka 300, 100 per sumur, dan 1.000
   pada [R1] baris 108-113 berstatus konvensi kartu, belum hasil ukur.
5. Untuk W1-08 dibutuhkan titik operasi onset yang mempertahankan recall. Hari ini titik dengan
   cakupan >=50 persen berbiaya 77x beban ([EVB] baris 101).

---

## 10. Yang belum terverifikasi

Daftar ini sengaja ditulis apa adanya supaya pembaca tidak mengira lebih dari yang diukur.

1. Presisi, recall, dan FAR bit_wear K-1 belum terukur karena field-nya tidak ada di JSON primer
   ([EVA] baris 61). Angka AUPRC persistence yang dikutip di bagian 3 berasal dari perhitungan
   ulang, bukan dari keluaran engine.
2. bit_wear K-2 belum dijalankan sama sekali karena pra-registrasi belum terbit ([EVA] baris 62).
3. tool_wear K-ii memakai angka RF V8 sebagai referensi, bukan hasil V9 ([EVA] baris 64).
4. hyd K-ii memakai angka RF V8 dengan 3 onset, sehingga berstatus kurang berdaya ([EVA] baris 168).
5. Batas blok B4 pada ssi: hanya 40 dari 137 run berdurasi >=5 menit, sehingga 97 run tidak masuk
   definisi blok ([EVB] baris 98).
6. Biaya waktu dinding untuk satu evaluasi fitness belum diukur ([R1] baris 121-123).
7. Kanal yang belum pernah diinventarisasi per engine tidak dihitung di kartu ini. Angka n_nodata
   hanya tersedia untuk ssi, vib, dan shk ([EVC] baris 121, 136, 146).
8. Seluruh angka FAR memakai konvensi kampanye V9 ([PMR] baris 378). Bila konvensi berubah, angka
   di dokumen ini berubah pula.
9. R8 memakai satuan menit kalender sedangkan V9 memakai per 24 jam operasi negatif. Kedua angka
   dilaporkan terpisah di bagian 3.A dan tidak disatukan.
10. Dokumen ini tidak menjalankan model apa pun. Semua angka adalah kutipan dari berkas di bagian
    1, dan tidak ada berkas .py, .html, .json, atau .csv yang dibuat sebagai deliverable.
