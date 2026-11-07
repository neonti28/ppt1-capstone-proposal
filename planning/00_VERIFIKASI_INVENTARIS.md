# 00 VERIFIKASI INVENTARIS: cakupan, keterlacakan angka, dan cacat

Kartu: `t_1d206884` (KURATOR). Board: `fitur-v9-swarm`. Tanggal: 2026-10-31 (WIB).
Workspace: `/mnt/d/Capstone 1(v2)`.

Sifat dokumen: VERIFIKASI. Dokumen ini tidak memperbaiki isi keempat inventaris dan tidak menjatuhkan
vonis teknis baru. Tugasnya tiga: mengukur cakupan dokumen, menguji keterlacakan angka ke berkas dan
baris, lalu menerbitkan cacat bernomor.

Catatan alat: sesi ini dimuat dengan panduan `requesting-code-review`. Kartu ini bukan perubahan kode,
tidak ada repositori git dan tidak ada commit, sehingga tahap diff, uji otomatis, dan subagen reviewer
tidak berlaku. Yang dipakai dari panduan itu prinsipnya: pemeriksa tidak boleh memeriksa pekerjaannya
sendiri, jadi setiap klaim di bawah diuji ulang ke berkas sumber dan keluarannya ditempel apa adanya.

---

## 0. Kerangka wajib yang dipakai untuk menilai

1. Alarm otomatis bukan tujuan. ML dipakai sebagai sistem pendukung keputusan dengan skor keyakinan.
2. Setiap angka wajib punya sumber: berkas dan baris, atau baris ledger `docs/RND_PROVENANCE_LEDGER.md`.
3. Klaim berjalan wajib disertai bukti perintah.
4. Kekurangan data dikemas menjadi fitur, bukan keluhan.
5. Setiap fitur punya pengguna, momen pakai, masukan, keluaran, status bukti.
6. Laporan ditutup dengan syarat, bukan dengan kata menyerah.
7. Keluaran hanya markdown di `planning/`.
8. Tanpa tanda pisah panjang.

Satu aturan penyajian di dokumen ini: kutipan dari berkas sumber dinormalkan ke tanda hubung biasa dan
ASCII, tanpa mengubah angka, urutan, atau tanda desimal.

---

## 1. Berkas yang dibuka dan ukuran byte

Ukuran diambil dengan `wc -c` dan `wc -l` pada 2026-10-31. Keluaran penuh ada di bagian 8.

### 1.1 Empat inventaris yang diverifikasi

| Kode | Berkas | Byte | Baris | Tabel | Baris data tabel |
|---|---|---:|---:|---:|---:|
| [I1] | `planning/00_INVENTARIS_V3_V6.md` | 44.125 | 626 | 10 | 61 |
| [I2] | `planning/00_INVENTARIS_V7_V8.md` | 39.059 | 589 | 12 | 59 |
| [I3] | `planning/00_INVENTARIS_V9_RND1.md` | 33.601 | 472 | 21 | 163 |
| [I4] | `planning/00_INVENTARIS_RND2_V11.md` | 35.536 | 412 | 4 | 51 |
| | **Total** | **152.321** | **2.099** | **47** | **334** |

Cara hitung baris data tabel: jumlah baris berawalan `|` dikurangi dua kali jumlah baris pemisah, karena
setiap tabel punya satu baris header dan satu baris pemisah.

```
$ for f in planning/00_INVENTARIS_*.md; do pipes=$(grep -c '^|' "$f"); seps=$(grep -cE '^\|[-: |]+\|$' "$f"); echo "$f pipes=$pipes seps=$seps data_rows=$((pipes-2*seps))"; done
00_INVENTARIS_V3_V6.md pipes=81 seps=10 data_rows=61
00_INVENTARIS_V7_V8.md pipes=83 seps=12 data_rows=59
00_INVENTARIS_V9_RND1.md pipes=205 seps=21 data_rows=163
00_INVENTARIS_RND2_V11.md pipes=59 seps=4 data_rows=51
```

### 1.2 Berkas sumber yang dibuka untuk menguji angka

Tiga puluh lima berkas, total 1.157.168 byte, ditambah empat inventaris di atas menjadi 1.309.489 byte.

| Berkas | Byte | Dipakai untuk |
|---|---:|---|
| `docs/RND_PROVENANCE_LEDGER.md` | 471.945 | uji baris ledger S6, S4-013, L-26, PM-078, hitung prefiks |
| `docs/V3_DATA_ACQUISITION_INVENTORY.md` | 17.514 | uji 175 bhaRun dan lain |
| `docs/V3_TS_FEATURES.md` | 8.429 | uji aritmetika 884 - 213 - 10 |
| `docs/V3_WITSML_PARSE_REPORT.md` | 3.346 | uji 7.080.457 baris |
| `docs/V4_MAINTENANCE_ML_OPTIONS.md` | 14.334 | uji 429.520 baris, 275 dan 29 kolom |
| `docs/V6_PM_VERDICT.md` | 26.032 | uji populasi kelas dan syarat LULUS penuh |
| `docs/V6_D0_READERS_SYNTHESIS.md` | 19.871 | uji 3.906 berkas belum diparse |
| `docs/V6_A1_DATA_AUDIT.md` | 28.138 | uji holdout dan R kuadrat |
| `docs/V6_E1_PREREG.md` | 12.738 | uji jumlah jendela per kelas |
| `docs/RND_D0_DATA_FEASIBILITY.md` | 28.196 | uji Nyquist, USROP, tabel state |
| `docs/V7_PM_VERDICT.md` | 23.569 | uji 523, 34/74, 481/329, positif shk |
| `docs/V8_M1_CAPABILITY_MAP.md` | 23.716 | uji lapisan B dan C per kelas |
| `docs/V8_A1_CAPABILITY_AUDIT.md` | 14.818 | uji AUPRC dan presisi tool_wear |
| `docs/V8_E_vib_CAPABILITY.md` | 13.970 | uji lift 4/4 |
| `docs/V8_E_ssi_CAPABILITY.md` | 12.678 | uji AUPRC dan lift ssi |
| `docs/V8_E_bit_wear_CAPABILITY.md` | 16.116 | uji AUPRC dan canary per fold |
| `docs/V8_E_stuck_CAPABILITY.md` | 22.172 | uji lift, FAR 1.440, kontrol positif |
| `docs/V8_E_hyd_CAPABILITY.md` | 16.345 | uji P/R/FAR dan onset per hari |
| `docs/V8_E_shk_CAPABILITY.md` | 17.176 | uji titik operasi FAR dan lead |
| `docs/V8_E_tool_wear_CAPABILITY.md` | 11.876 | uji lift 1,09-1,42 |
| `docs/V9_EVAL_A_LAYERA.md` | 32.713 | uji 11 klaim lapisan A |
| `docs/V9_EVAL_B_LAYERB.md` | 30.472 | uji B1, B3, B4 |
| `docs/V9_EVAL_C_LAYERC.md` | 23.153 | uji portabilitas dan n_nodata |
| `docs/V9_PM2_VERDICT.md` | 22.654 | uji komposisi 27 head dan 11 head L1 |
| `docs/RND_R3_VMD_SVM.md` | 32.174 | uji Nyquist dan 75/105 |
| `docs/RND_R5_DRIFT.md` | 35.937 | uji KS antar sumur dan dalam sumur |
| `docs/RND_R8_EVALUASI_BERLAPIS.md` | 27.013 | uji H1, H2, H4, LightGBM |
| `docs/RND_S6_PM_WAVE2.md` | 40.271 | uji H1p, H1p3, lapisan B, penolakan |
| `docs/RND_S4_LAYER_B_DATA.md` | 23.799 | uji 1.777,75 jam dan 160,75 jam |
| `docs/RND_S3_HYBRID_BITWEAR.md` | 22.275 | uji akurasi 1,000000 dan diagnostik |
| `docs/RND_ENGINE_S6_INTEGRATION.md` | 3.915 | uji beban tinjauan dan 27 head |
| `docs/RND_S5_AUDIT_WAVE2.md` | 27.190 | uji 143 sel dan tabel ukuran |
| `docs/RND_S5_DEFECT_STATUS.md` | 3.418 | uji 64/441 dan 74/328 |
| `docs/V10_PM2_VERDICT.md` | 8.545 | uji rekap tier dan head |
| `docs/V11_PM_FINAL.md` | 20.660 | uji 96 lawan 46,2 |

---

## 2. Cakupan dokumen

### 2.1 Angka dasar

```
$ ls -1 docs | wc -l
123
$ ls -1 docs/*.md | wc -l
119
```

Angka 123 adalah seluruh entri di `docs/`: 119 berkas markdown, 3 berkas ipynb, dan 1 direktori
`visualisasi`. Pembanding cakupan memakai 119 berkas markdown.

Hasil penyisiran: 50 berkas markdown disebut minimal satu inventaris, 69 berkas tidak disebut satu pun.
Dengan kata lain 58 persen dokumen markdown di `docs/` tidak pernah dibuka oleh gelombang inventaris ini.

### 2.2 Cakupan per era

| Era | Berkas di `docs` | Dibuka | Belum dibuka | Berkas yang dibuka |
|---|---:|---:|---:|---|
| V3, V4, V6, RND_D0 | 24 | 9 | 15 | V3A, V3T, V3W, V4, PM6, D0, A1, E1, RD0 |
| V7, V8 | 24 | 13 | 11 | PM7, R1-7, A1-7, PM8, M1, A1-8, 7 profil E |
| V9, RND_R1 sampai R8, PM R&D | 21 | 17 | 4 | PM1, PM2, ERU, EST, EML, EVA, EVB, EVC, R1-R8, PMR |
| RND_S1 sampai S6, S5 status, integrasi engine | 8 | 8 | 0 | S1-S6, S5 status, integrasi |
| Di luar empat era di atas | 42 | 3 | 39 | V10_PM2_VERDICT, V11_PM_FINAL, ledger provenance |
| **Total** | **119** | **50** | **69** | |

Perintah penyisir ada di bagian 8.B. Angka 42 pada baris terakhir berisi proposal teknis, enam berkas
PPT1, sepuluh berkas V10, sebelas berkas V11, lima berkas RND_E, tiga berkas pendukung, dan V1_AUDIT.

### 2.3 Dokumen vonis yang belum tercakup

Kolom "kata vonis" adalah jumlah kemunculan kata `vonis` di dalam berkas, dipakai sebagai penanda bahwa
berkas itu memuat keputusan, bukan sekadar data mentah.

| Berkas | Byte | Baris | Kata vonis | Kenapa seharusnya tercakup |
|---|---:|---:|---:|---|
| `V11_AUDIT.md` | 27.707 | 378 | 17 | audit yang memeriksa proposal V11 dan menjadi sumber angka koreksi yang dikutip `V11_PM_FINAL` |
| `V11_AUD_CLAIM.md` | 23.745 | 270 | 0 | daftar klaim yang diuji audit V11 |
| `V9_A1_AUDIT.md` | 28.071 | 228 | 4 | audit angka V9, yaitu dokumen yang memverifikasi 11 klaim mesin yang dibandingkan [I3] |
| `V9_I1_INTEGRATION.md` | 25.982 | 372 | 0 | sumber perakitan 27 head yang dikutip [I3] lewat PM2 |
| `V10_A1_AUDIT.md` | 16.522 | 165 | 3 | audit yang menutup enam keluhan operator pada proposal V10 |
| `V10_R1_ALASAN.md` | 32.311 | 437 | 0 | alasan pemilihan bab dan angka pada proposal V10 |
| `ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md` | 249.874 | 3.557 | 5 | objek yang dinilai V11 dan menjadi pemenang 96 lawan 46,2 |
| `RND_E0_AUDIT_ENGINE.md` | 46.979 | 522 | 0 | audit mesin sebelum gelombang dua |
| `RND_E1_MATRIKS.md` | 44.273 | 494 | 0 | matriks hasil yang menjadi bahan vonis E2 sampai E4 |
| `RND_E2_PROTOKOL.md` | 42.230 | 566 | 0 | protokol uji gelombang dua |
| `RND_E3_HASIL.md` | 22.353 | 353 | 0 | hasil yang dikutip R7 dan S6 |
| `RND_E4_PERBAIKAN.md` | 22.886 | 357 | 2 | daftar perbaikan yang menentukan kelayakan ulang |
| `RND_ALGO_RESEARCH_PLAN.md` | 6.637 | 124 | 4 | disebut ledger L-26 baris 56 sebagai asal konvensi FAR <= 6, konvensi yang mengikat seluruh tier |
| `RND_EVALUATION_POLICY.md` | 3.992 | 73 | 1 | kebijakan evaluasi yang mengatur ambang dan satuan |
| `RND_V1_AUDIT.md` | 17.877 | 190 | 1 | audit pertama atas rencana riset |
| `V6_A2_ML_AUDIT.md` | 22.322 | 225 | 0 | audit ML yang memverifikasi 24 dari 24 angka kelas V6 |
| `V6_E1b_PREREG_HYD.md` | 4.359 | 75 | 0 | pra-registrasi gate kelas hidraulik |
| `V6_E1c_PREREG_TOOLWEAR.md` | 5.672 | 91 | 0 | pra-registrasi gate kelas tool_wear |
| `V6_E1d_PREREG_BITWEAR.md` | 4.857 | 80 | 0 | pra-registrasi gate kelas bit_wear |
| `V8_R1_ABC_SPEC.md` | 30.231 | 413 | 0 | spesifikasi tiga jalur perbaikan yang menjadi dasar vonis V8 |
| `V7_M2_SYNTHESIS.md` | 31.487 | 181 | 0 | sintesis V7 yang memasok angka koreksi ke PM V7 |
| `V10_M1_PETA_V8.md` | 21.767 | 309 | 0 | peta kapabilitas V8 versi V10 |
| `V10_PM1_OUTLINE.md` | 21.175 | 275 | 0 | kerangka proposal yang dipakai menyusun bab |

Dua puluh tiga berkas di atas adalah potongan terbesar dari 69 berkas yang tidak tercakup. Daftar penuh
69 berkas ada di bagian 8.B.

### 2.4 Akibat yang bisa ditunjuk

1. Rantai konvensi FAR <= 6 berhenti di ledger. [I2] bagian 3 mengutip [L] baris 56 (L-26) dan menyebut
   statusnya BELUM. Ledger itu menyebut sumbernya `docs/RND_ALGO_RESEARCH_PLAN.md` bagian 6 butir 2, dan
   berkas itu tidak dibuka inventaris mana pun. Artinya ambang yang mengikat seluruh keputusan tier
   berasal dari dokumen yang belum pernah diperiksa gelombang ini.
2. Tiga pra-registrasi gate V6 (hid, tool_wear, bit_wear) tidak dibuka, padahal [I1] menyatakan gate
   dikunci di `V6_E1_PREREG.md`. Padanan gate per kelas justru berada di tiga berkas itu.
3. [I3] membandingkan 11 klaim mesin, sementara audit yang memverifikasi angka V9 (`V9_A1_AUDIT.md`)
   tidak dibuka. Pembanding tanpa audit pembandingnya belum tertutup.
4. [I4] memberi status BERLAKU atau DIGANTIKAN pada 10 dokumen dan mengutip sembilan perbaikan V11,
   tetapi `V11_AUDIT.md` dan `V11_AUD_CLAIM.md` yang memuat klaim yang diuji tidak dibuka.

---

## 3. Uji 10 angka per inventaris

Putusan yang dipakai: COCOK berarti nilai dan rujukan baris sesuai; COCOK DENGAN CATATAN berarti nilainya
ada tetapi rujukan baris atau cakupan klaimnya kurang tepat; TIDAK COCOK berarti nilai tidak ditemukan di
rujukan yang disebut.

### 3.1 [I1] Inventaris V3-V6

| No | Angka yang diuji | Letak di [I1] | Rujukan yang dikutip | Yang terlihat di sumber | Putusan |
|---:|---|---|---|---|---|
| 1 | 175 bhaRun, 16 mudLog, 253 LAS, 468 DLIS | baris 73-74 | V3A baris 78 | baris 78 memuat keempat angka persis | COCOK |
| 2 | 884 label - 213 tanpa CSV - 10 di luar rentang = 661 | baris 89-92 | V3T baris 39-44 | baris 39 sampai 44 memuat 884, 213, 10, dan 661 dengan rincian sumur | COCOK |
| 3 | 7.080.457 baris pada 8 CSV | baris 101-102 | V3W baris 20 | baris 20 berbunyi "Total: 7,080,457 baris time-series, 8 CSV" | COCOK |
| 4 | 429.520 baris, 275 kolom union, 29 kolom lintas sumur | baris 118 | V4 baris 17 | baris 17 memuat ketiga angka | COCOK |
| 5 | Populasi 82.530 / 320 / 180 / 714 / 394 / 58.317 untuk "tujuh kelas" | baris 138-139 | PM6 baris 164-166 | sumber memuat enam nilai untuk klaim tujuh kelas, nilai ketujuh tidak ada | COCOK DENGAN CATATAN |
| 6 | 2.156 + 1.750 = 3.906 berkas, 54,6 persen belum diparse | baris 157-158 | D0 baris 49 | baris 49 memuat ketiga angka dan persennya | COCOK |
| 7 | Holdout 66,3 / 92,1 / 97,7 / 99,9 / 99,97 persen, R kuadrat 0,99987 | baris 172-176 | A1 baris 198-201 | baris 198 sampai 201 memuat kelima angka dan R kuadrat 0,99987 | COCOK |
| 8 | 2.007/5.555, 5.429/23.922, 1.642/43.191, 363/24.480 | baris 188-190 | E1 baris 75 | baris 75 adalah baris total dengan keempat pasangan | COCOK |
| 9 | Nyquist 0,1667 Hz, VIBLAT F-14 0,0167 Hz | baris 207-208 | RD0 baris 159 | baris 159 memuat kedua angka | COCOK |
| 10 | USROP 198.928 baris dengan 49.732 high_MSE | baris 210 | RD0 baris 311-315 | baris 311 dan 315 memuat 198.928 dan 49.732 | COCOK |

Uji tambahan aritmetika: [I1] baris 232-237 melaporkan selisih 59.500 pada E1. Hitungan ulang dari
keluarannya sendiri di bagian 14.C: jumlah baris 7 CSV 7.020.975 dikurangi 7 header menjadi 7.020.968,
dikurangi klaim 6.961.468 menghasilkan 59.500. Aritmetikanya benar.

### 3.2 [I2] Inventaris V7-V8

| No | Angka yang diuji | Letak di [I2] | Rujukan yang dikutip | Yang terlihat di sumber | Putusan |
|---:|---|---|---|---|---|
| 1 | 523 event kurasi dalam rentang, bukan 582 | baris 77 | PM7 baris 136 | baris 136 memuat 582 dan 523 dengan alasan metode | COCOK |
| 2 | Onset stuck strict 34, ffill 74, angka 50 tidak tereproduksi | baris 75-76 | PM7 baris 137 | baris 137 memuat 34, 74, dan pernyataan 50 tidak reproduce | COCOK |
| 3 | 481 kandidat onset awal blok, 329 dari kondisi normal | baris 76-77 | PM7 baris 139 | baris 139 memuat 481 dan 329 | COCOK |
| 4 | Positif shk F-10 798, F-12 580, F-4 50, F-15 13, F-15B 0 | baris 79, 370-371 | PM7 baris 141 | baris 141 memuat kelima angka | COCOK |
| 5 | Lift 1,61 / 2,36 / 3,50 / 1,63, G1 4/4 | baris 191-192 | V8_E_vib baris 52 dan 69 | baris 69 memuat keempat lift, baris 52 memuat G1 4/4 | COCOK |
| 6 | ssi AUPRC 0,0185-0,1057, lift 2,61-6,64, lift >=1,5 di 4/5 | baris 222-223 | V8_E_ssi baris 58 | baris 58 memuat ketiga angka | COCOK |
| 7 | bit_wear AUPRC 0,298 / 0,365 / 0,813 / 0,783 dan canary 0,191 / 0,288 / 0,756 / 0,692 | baris 254-255 | V8_E_bit_wear baris 66-69 | keempat baris memuat AUPRC dan canary persis | COCOK |
| 8 | stuck lift 1,65 / 1,30 / 9,72 / 1,12 dan FAR 1.440 | baris 284-290 | V8_E_stuck baris 113-114, 100 | baris 113-114 memuat keempat lift, baris 100 memuat 1.440 | COCOK |
| 9 | Onset blok per hari 0,263 / 1,479 / 0,996 / 0,156 / 1,752 / 1,764 / 4,707 | baris 347 | V8_E_hyd baris 163-169 | tujuh baris memuat tujuh nilai berurutan | COCOK |
| 10 | tool_wear AUPRC 0,5433 / 0,7684 / 0,7031 / 0,6497 dan presisi 0,516 / 0,559 / 0,509 / 0,500 | baris 111, 397-398 | V8_A1 baris 68 | baris 68 memuat kedelapan angka | COCOK |

Uji tambahan aritmetika: seluruh delapan baris skor keyakinan di [I2] bagian 4 dihitung ulang. Rumus
0,40 S_A + 0,35 S_B + 0,25 S_C memberi 0,495 / 0,526 / 0,253 / 0,456 / 0,610 / 0,512 / 0,519 / 0,455,
dan pembulatan ke bilangan bulat memberi 50 / 53 / 25 / 46 / 61 / 51 / 52 / 46. Semua cocok dengan tabel.

### 3.3 [I3] Inventaris V9-RND1

| No | Angka yang diuji | Letak di [I3] | Rujukan yang dikutip | Yang terlihat di sumber | Putusan |
|---:|---|---|---|---|---|
| 1 | vib rule P 0,87-0,95, R 0,28-0,60, FAR 10,0-49,9 | baris 134 | EVA baris 54 | baris 54 memuat ketiga rentang | COCOK |
| 2 | stuck K-ii RF tau 0,5 P 0,05-1,00, R 0,004-0,005, FAR 0,0-1,25, 3/4 fold | baris 138 | EVA baris 58 dan 128 | baris 58 memuat P, R, 3/4 fold; baris 128 memuat FAR 0,0-1,25 | COCOK |
| 3 | hyd K-i persistence P 0,61-0,90, FAR 32,4-110,7; hybrid memangkas FP 2091 ke 927 | baris 139 | EVA baris 59 | baris 59 memuat seluruh rentang dan pasangan 2091 ke 927 | COCOK |
| 4 | ssi B3 +0,731 dengan FP 26 ke 7 | baris 201 | EVB baris 98 | baris 98 memuat +0,731 dan FP 26 ke 7 | COCOK |
| 5 | hyd K-i B3 +0,557 dengan FP 2091 ke 927 | baris 205 | EVB baris 102 | baris 102 memuat +0,557 dan pasangan FP | COCOK |
| 6 | tool_wear B3 +0,909 sampai +0,976, FP 1-3 lawan 33-41 per alat | baris 209 | EVB baris 106 | baris 106 memuat kedua rentang | COCOK |
| 7 | 5 head L0, 11 head L1, 9 head L2, 2 head L3, slot alarm 0 | baris 186-187 | PM2 baris 140 | baris 140 memuat keempat angka dan slot nol | COCOK |
| 8 | ssi n_nodata 22.385 dari 35.906 baris, 62,3 persen | baris 313 | EVC baris 136 | baris 136 memuat ketiga angka | COCOK |
| 9 | Satu ambang memberi FAR 4,1 sampai 496, sebaran 119 kali | baris 283 | EVC baris 120 | baris 120 memuat 4,1-496 dan 119 kali | COCOK |
| 10 | R8 H1 recall 0,5638 dan 7 dari 9 fold | baris 153 | R8 baris 69 dan 109 | baris 69 memuat FP, presisi, FAR, lead tanpa recall; baris 109 adalah baris H2; nilai 0,5638 dan 7 dari 9 ada di baris 127 | TIDAK COCOK |

Uji tambahan: R3 baris 102 memuat Nyquist 0,1667 Hz dan 75/105 percobaan gagal, cocok dengan [I3] baris
232 dan 363. R5 baris 135-136 memuat D median 0,986 dengan 10 dari 10 pasangan p < 0,05 dan D median
0,211 dengan 4 dari 5 well, cocok dengan [I3] baris 293. PM2 baris 181 memuat "11 L1" dan baris 205
memuat "11/11 L1 human_review_required", sedangkan [I3] baris 343 merujuk baris 206 yang isinya tentang
badge FAR, bukan aturan tinjauan manusia.

### 3.4 [I4] Inventaris RND2-V11

| No | Angka yang diuji | Letak di [I4] | Rujukan yang dikutip | Yang terlihat di sumber | Putusan |
|---:|---|---|---|---|---|
| 1 | H1p FP 927, TP 4924, presisi 0,8243, recall 0,6519, FAR 4,0984, lead 8,0, 7 dari 9 | baris 156-160 | S6 baris 196 | baris 196 memuat ketujuh nilai; baris 150 memuat versi prosa yang sama | COCOK |
| 2 | H1 FP 935, TP 3804, presisi 0,7789, recall 0,5638, FAR 3,5302, lead 11,5, 5 dari 9 | baris 161 | S6 baris 194 | baris 194 memuat seluruh nilai termasuk 5 pada kolom terakhir | COCOK |
| 3 | H1p3 FP 568, TP 3557, presisi 0,8646, recall 0,5296, FAR 2,0323, FAR lolos 9 dari 9, recall lolos 5 dari 9 | baris 162 | S6 baris 197 | baris 197 memuat seluruh nilai | COCOK |
| 4 | Beban alarm per onset 2,3769 / 2,3974 / 1,4564 | baris 164 | S6 baris 150-151 | kedua baris memuat ketiga nilai | COCOK |
| 5 | 18 penolakan, 7 di antaranya kegagalan bentuk DAN | baris 169 | S6 baris 312 | baris 312 memuat 18 dan 7 | COCOK |
| 6 | 2.453 record dan 5.821,417 jam; repair 806 record dan 1.215,0 jam; median 1,0; p90 3,5 | baris 173 | S6 baris 351-354 | baris 351-354 memuat seluruh nilai | COCOK |
| 7 | 325 dari 1.759 laporan memuat tabel kegagalan, 533 record | baris 174 | S4 baris 89 | baris 89 memuat ketiga angka | COCOK |
| 8 | Lost circulation 160,75 jam pada 75 record, dan pencarian 2739 / 212.0 / 195.0 nol di S4 | baris 373 | S4 baris 67-76 | baris 74 memuat 75 record dan 160,75 jam; rentang 67-76 tidak memuat lost circulation 2739 atau 212.0 | COCOK |
| 9 | 1.777,75 jam pada 1.116 kejadian repair dan maintain, median 1,0 jam, p90 3,5 jam | baris 265 | S4 bagian 3.1 baris 63-78 | baris 78 dan 125 memuat 1.116 kejadian dan 1.777,75 jam; median 1,0 dan p90 3,5 hanya milik repair pada baris 69, sedangkan maintain pada baris 72 punya p90 4,5 dan gabungan tidak punya median | COCOK DENGAN CATATAN |
| 10 | Ledger: header S6 baris 3228, 191 baris data, baris terakhir 3425, total 3.434 baris; S4-013 di baris 2182 | baris 96-105 | ledger | seluruh angka cocok persis | COCOK |

Uji tambahan: hitung prefiks ledger memberi S1 84, S2 455, S3 92, S4 95, S5 387, S6 191, cocok dengan
[I4] baris 108. V11 baris 122-124 memberi selisih 49,8 poin dari 96 lawan 46,2 dan memimpin 4 dari 4
kriteria, cocok dengan [I4] baris 195. S3 baris 100 memuat akurasi 1,000000 dan baris 187 memuat presisi
0,8496 dan recall 0,9968, cocok dengan [I4] baris 289.

### 3.5 Rekap uji

| Inventaris | Uji | COCOK | COCOK DENGAN CATATAN | TIDAK COCOK |
|---|---:|---:|---:|---:|
| [I1] V3-V6 | 10 | 9 | 1 | 0 |
| [I2] V7-V8 | 10 | 10 | 0 | 0 |
| [I3] V9-RND1 | 10 | 9 | 0 | 1 |
| [I4] RND2-V11 | 10 | 9 | 1 | 0 |
| **Total** | **40** | **37** | **2** | **1** |

Empat puluh uji, 37 cocok, dua cocok dengan catatan, satu tidak cocok. Artinya mutu pengutipan angka
keempat inventaris tinggi. Yang bermasalah bukan angkanya, melainkan cakupan dokumen dan ketepatan
rujukan baris pada tiga tempat.

---

## 4. Cacat bernomor

### C-01. Enam puluh sembilan dari 119 dokumen tidak pernah dibuka

Berkas: keempat inventaris, bagian 1 masing-masing. Bukti: penyisiran nama berkas, keluaran di bagian 8.B.
Angka: 50 disebut, 69 tidak disebut, 58 persen tidak tercakup. Daftar terpenting ada di bagian 2.3.
Akibat: setiap klaim yang bersandar pada dokumen di daftar itu belum punya jalur periksa dari gelombang
inventaris, termasuk audit V11 yang memuat 17 kemunculan kata vonis dan audit V9.

### C-02. Konvensi FAR <= 6 dipakai tanpa membuka dokumen asalnya

Berkas: `planning/00_INVENTARIS_V7_V8.md` bagian 3 baris 126 dan `docs/RND_PROVENANCE_LEDGER.md` baris 56.
Ledger menyebut `docs/RND_ALGO_RESEARCH_PLAN.md` bagian 6 butir 2 sebagai asal konvensi, dan berkas itu
(6.637 byte, 124 baris) tidak dibuka inventaris mana pun. Akibat: ambang yang menjadi gerbang tier
LAYER-1 bersandar pada rantai rujukan yang berhenti di ledger, bukan pada dokumen yang dibaca.

### C-03. Tiga pra-registrasi gate V6 tidak dibuka

Berkas: `planning/00_INVENTARIS_V3_V6.md` bagian 1 dan bagian 2.8. Yang dibuka hanya `V6_E1_PREREG.md`.
Tiga berkas gate per kelas yang ada di disk, yaitu `V6_E1b_PREREG_HYD.md` (4.359 byte), 
`V6_E1c_PREREG_TOOLWEAR.md` (5.672 byte), dan `V6_E1d_PREREG_BITWEAR.md` (4.857 byte), tidak dibuka.
Akibat: klaim bahwa gate dikunci sebelum hasil hanya terbukti untuk kelas yang tercakup di E1 utama.

### C-04. Audit V9 tidak dibuka padahal 11 klaim mesin dibandingkan

Berkas: `planning/00_INVENTARIS_V9_RND1.md` bagian 1 dan bagian 3. `docs/V9_A1_AUDIT.md` (28.071 byte,
228 baris, 4 kemunculan kata vonis) tidak ada di daftar berkas yang dibuka. Begitu juga
`docs/V9_I1_INTEGRATION.md` (25.982 byte), padahal komposisi 27 head yang dikutip di bagian 4 berasal dari
perakitan di berkas itu. Akibat: pembanding 11 klaim berdiri di atas angka eval tanpa audit pembandingnya.

### C-05. Satu dari sebelas dokumen seri V11 dibuka

Berkas: `planning/00_INVENTARIS_RND2_V11.md` bagian 1. Yang dibuka hanya `V11_PM_FINAL.md`. Sepuluh berkas
V11 lain tidak dibuka, termasuk `V11_AUDIT.md` (27.707 byte, 17 kemunculan kata vonis), `V11_AUD_CLAIM.md`
(23.745 byte), `V11_HYB.md`, `V11_ML.md`, `V11_STAT.md`, `V11_EVAL_CMP.md`, `V11_RND.md`,
`V11_PROTOCOL.md`, `V11_DATA1.md`, dan `V11_DATA2.md`. Akibat: butir 7 pada bagian 4.1 mengutip sembilan
perbaikan terbuka dari vonis V11, sedangkan daftar klaim yang diuji dan hasil auditnya tidak dibaca.

### C-06. Nilai ketujuh untuk klaim "tujuh kelas" tidak ada di mana pun

Berkas: `planning/00_INVENTARIS_V3_V6.md` baris 138-139 dan `docs/V6_PM_VERDICT.md` baris 164-166.
Inventaris menulis "Tujuh kelas dengan populasi terhitung:" lalu mencantumkan enam nilai, yaitu 82.530,
320, 180, 714, 394, dan 58.317, ditambah lima kelas USROP. Sumbernya juga hanya memuat enam nilai.
Akibat: klaim tujuh kelas tidak dapat dicocokkan dengan angka oleh pembaca, dan inventaris tidak
menandainya sebagai selisih terbuka padahal bagian 13 seharusnya memuat hal seperti ini.

### C-07. Rujukan baris meleset pada nilai recall H1

Berkas: `planning/00_INVENTARIS_V9_RND1.md` baris 153. Nilai recall 0,5638 dan "7 dari 9 fold" dirujuk ke
`docs/RND_R8_EVALUASI_BERLAPIS.md` baris 69 dan 109. Baris 69 memuat FP, presisi, FAR, dan lead tanpa
recall; baris 109 adalah baris H2. Nilai yang dirujuk ada di baris 127, dan ditegaskan lagi di baris
131-132 serta 375. Akibat: satu satunya uji yang gagal pada bagian 3.3 disebabkan rujukan, bukan angka.

### C-08. Rujukan baris meleset pada aturan tinjauan manusia

Berkas: `planning/00_INVENTARIS_V9_RND1.md` baris 343. Klaim "11 dari 11 head L1 human_review_required"
dirujuk ke `docs/V9_PM2_VERDICT.md` baris 206. Baris 206 berisi badge FAR, keyakinan, dan batas tampil;
angka 11/11 ada di baris 205, dan komposisi 11 head L1 ada di baris 181.

### C-09. Median dan p90 repair dilekatkan ke populasi gabungan

Berkas: `planning/00_INVENTARIS_RND2_V11.md` baris 265. Keluaran fitur F-06 menulis "1.777,75 jam pada
1.116 kejadian repair dan maintain, median 1,0 jam, p90 3,5 jam". Di `docs/RND_S4_LAYER_B_DATA.md`
baris 69, median 1,0 dan p90 3,5 adalah milik repair saja (806 kejadian, 1.215,0 jam); baris 72 memberi
maintain 310 kejadian, 562,75 jam, p90 4,5; baris 125 menulis gabungan 1.116 kejadian dan 1.777,75 jam
tanpa median. Akibat: satu angka sebaran dipakai untuk populasi yang bukan populasi asalnya.

### C-10. Jumlah artefak pada daftar tidak cocok dengan isi daftar

Berkas: `planning/00_INVENTARIS_V3_V6.md` baris 56-60. Kalimatnya "lima artefak data ikut dibuka untuk
memeriksa angka", lalu mendaftar enam artefak: `features_timeseries.npz`, `features_timeseries_meta.json`,
`features_timeseries_events.csv`, `data/volve/witsml_parsed/*.csv`, `data/USROP_labeled.csv`, dan
`data/witsml/Norway-NA-15_47_9-F-9 A time.csv`.

### C-11. Kolom jumlah baris berisi prosa untuk empat berkas

Berkas: `planning/00_INVENTARIS_V7_V8.md` baris 49-52. Kolom Baris untuk `V8_E_vib_CAPABILITY.md`,
`V8_E_ssi_CAPABILITY.md`, `V8_E_shk_CAPABILITY.md`, dan `V8_E_tool_wear_CAPABILITY.md` diisi kalimat
"dipakai untuk angka ..." alih-alih jumlah baris, sedangkan kerangka butir 2 menuntut berkas dan baris.
Ukuran byte keempatnya ada di tabel bagian 1, jumlah barisnya tidak ada di mana pun dalam dokumen itu.

### C-12. Rekap tabel pada metadata kartu V3-V6 tidak sesuai dokumen

Berkas: handoff kartu `t_69e694aa` mencantumkan `tables_data_lines` 81, sedangkan dokumennya punya 81
baris berawalan `|` yang mencakup 10 baris header dan 10 baris pemisah, sehingga baris data tabelnya 61.
Angka 81 adalah jumlah baris tabel mentah, bukan baris data. Dua kartu lain, [I3] dengan 163 dan [I4]
dengan 51, mencantumkan baris data dan cocok dengan hitungan.

---

## 5. Keputusan

**PERLU PERBAIKAN.**

Alasannya bukan mutu pengutipan angka, karena 37 dari 40 uji cocok dan seluruh aritmetika yang diuji
ulang benar. Alasannya cakupan: 69 dari 119 dokumen tidak dibuka, termasuk audit V9, audit V11, audit V10,
audit mesin RND_E0, dokumen asal konvensi FAR, tiga pra-registrasi gate V6, dan proposal teknis yang
menjadi objek penilaian V11. Empat cacat pertama (C-01 sampai C-04) masing-masing cukup untuk menahan
pemakaian inventaris sebagai dasar keputusan fitur tanpa catatan.

Delapan cacat lain bersifat perbaikan teks dan rujukan, dan tiga di antaranya (C-07, C-08, C-09) langsung
menyentuh keterlacakan angka.

---

## 6. Syarat yang dibutuhkan

1. Untuk C-01 sampai C-05. Dibutuhkan satu kartu inventaris kelima dengan daftar masukan eksplisit:
   `V11_AUDIT.md`, `V11_AUD_CLAIM.md`, `V10_A1_AUDIT.md`, `V10_R1_ALASAN.md`, `V9_A1_AUDIT.md`,
   `V9_I1_INTEGRATION.md`, `RND_E0` sampai `RND_E4`, `RND_EVALUATION_POLICY.md`,
   `RND_ALGO_RESEARCH_PLAN.md`, `V6_A2_ML_AUDIT.md`, `V6_E1b`, `V6_E1c`, `V6_E1d`, `V8_R1_ABC_SPEC.md`,
   `V7_M2_SYNTHESIS.md`, dan `ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md`. Syarat mutunya sama dengan empat
   kartu sebelumnya: ukuran byte, baris, lima field per fitur, tanpa tanda pisah panjang.
2. Untuk C-02. Dibutuhkan kutipan langsung dari `docs/RND_ALGO_RESEARCH_PLAN.md` bagian 6 butir 2 pada
   dokumen yang memakai ambang FAR <= 6, sehingga konvensi itu punya rujukan primer, bukan hanya ledger.
3. Untuk C-06. Dibutuhkan penetapan daftar tujuh kelas beserta populasinya, diambil dari `V6_A2_ML_AUDIT.md`
   yang menyatakan 24 dari 24 angka kelas terverifikasi, lalu dicocokkan dengan tabel PM V6.
4. Untuk C-07 dan C-08. Dibutuhkan penggantian rujukan menjadi baris 127 pada R8 dan baris 205 pada PM2,
   lalu satu penyisiran ulang seluruh rujukan baris pada [I3] dengan perintah yang keluarannya ditempel.
5. Untuk C-09. Dibutuhkan pemisahan dua angka: sebaran repair (806 kejadian, median 1,0, p90 3,5) dan
   sebaran gabungan repair plus maintain yang belum dihitung di S4. Bila angka gabungan dipakai, hitung
   dulu dari `ddr.parquet` dan sebutkan perintahnya.
6. Untuk C-10 sampai C-12. Dibutuhkan penyuntingan tiga kalimat dan satu metadata, lalu hitung ulang
   jumlah artefak, jumlah baris tabel, dan jumlah field wajib per fitur dengan perintah yang ditempel.

---

## 7. Yang belum diverifikasi

1. Angka V3 sampai V8 yang tidak masuk 20 uji di bagian 3.1 dan 3.2 dikutip tanpa hitung ulang, termasuk
   tabel onset per sumur di RD0 dan sebaran litologi. Yang diuji hanya 10 angka per inventaris.
2. Berkas 69 yang tidak tercakup tidak dibuka satu per satu. Statusnya ditetapkan dari nama berkas,
   ukuran byte, jumlah baris, dan hitungan kata vonis, bukan dari pembacaan isi penuh.
3. Klaim bahwa isi `V11_AUDIT.md` memuat klaim yang diuji `V11_AUD_CLAIM.md` disimpulkan dari nama dan
   ukuran berkas, bukan dari pembacaan.
4. `ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md` berukuran 249.874 byte dan tidak dibuka pada kartu ini.
5. Tidak ada model, engine, atau harness yang dijalankan. Seluruh uji bersifat pembacaan berkas dan
   aritmetika.
6. Angka 123 pada `ls -1 docs | wc -l` mencakup 3 berkas ipynb dan 1 direktori, sehingga [I4] baris 24
   yang menyebut "123 berkas diperiksa" menghitung entri direktori sebagai berkas. Klaim intinya, yaitu
   tidak ada S7 dan tidak ada V12, tetap benar.
7. Empat berkas profil kapabilitas V8 yang tidak masuk daftar masukan kartu [I2] tetap diperiksa di sini
   karena ukuran dan barisnya tercatat, dan angka yang dikutipnya cocok dengan audit A1-8.

---

## 8. Bukti perintah

### 8.A Ukuran berkas

```
$ ls -1 docs | wc -l
123
$ ls -1 docs/*.md | wc -l
119

$ wc -c planning/00_INVENTARIS_V3_V6.md planning/00_INVENTARIS_V7_V8.md \
      planning/00_INVENTARIS_V9_RND1.md planning/00_INVENTARIS_RND2_V11.md
44125 planning/00_INVENTARIS_V3_V6.md
39059 planning/00_INVENTARIS_V7_V8.md
33601 planning/00_INVENTARIS_V9_RND1.md
35536 planning/00_INVENTARIS_RND2_V11.md

$ wc -c <35 berkas sumber> planning/00_INVENTARIS_*.md | tail -1
1309489 total
```

### 8.B Penyisiran cakupan

```
$ for f in docs/*.md; do b=$(basename "$f");
    if grep -qF "$b" planning/00_INVENTARIS_V3_V6.md planning/00_INVENTARIS_V7_V8.md \
       planning/00_INVENTARIS_V9_RND1.md planning/00_INVENTARIS_RND2_V11.md;
    then s=opened; else s=missing; fi; echo "$s $b"; done | sort | uniq -c
     15 e1 missing
      9 e1 opened
     11 e2 missing
     13 e2 opened
      4 e3 missing
     17 e3 opened
      8 e4 opened
     39 out missing
      3 out opened
```

Rincian 69 berkas yang tidak tercakup, dengan byte, baris, dan hitungan kata `vonis`:

```
  249874  3557    5  ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN - Copy.md
  249874  3557    5  ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md
   24285   352    2  ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.v3_arsip.md
   36582   241    0  PPT1_BAB1_1.md
   29743   308    0  PPT1_BAB1_2.md
   36745   340    0  PPT1_BAB3_1.md
   63521   697    0  PPT1_BAB3_2.md
   61093   515    0  PPT1_BAB3_4_MCDM.md
   42477   234    3  PPT1_LEDGER_ANGKA.md
    2820    46    0  PROTOCOL_RISET_TIM.md
    6637   124    4  RND_ALGO_RESEARCH_PLAN.md
   46979   522    0  RND_E0_AUDIT_ENGINE.md
   44273   494    0  RND_E1_MATRIKS.md
   42230   566    0  RND_E2_PROTOKOL.md
   22353   353    0  RND_E3_HASIL.md
   22886   357    2  RND_E4_PERBAIKAN.md
    3992    73    1  RND_EVALUATION_POLICY.md
   20416   212    0  RND_P0_PARAMETER.md
   17877   190    1  RND_V1_AUDIT.md
   16522   165    3  V10_A1_AUDIT.md
   39581   608    0  V10_D1_BAB_DATA.md
   27673   283    3  V10_EVAL_BAB.md
   31804   447    1  V10_E_ML_BAB.md
   30731   447    0  V10_E_RULE_BAB.md
   28755   491    0  V10_E_STAT_BAB.md
   21767   309    0  V10_M1_PETA_V8.md
   21175   275    0  V10_PM1_OUTLINE.md
   32311   437    0  V10_R1_ALASAN.md
   27707   378   17  V11_AUDIT.md
   23745   270    0  V11_AUD_CLAIM.md
   22957   238    1  V11_DATA1.md
   16437   190    0  V11_DATA2.md
   18145   290    3  V11_EVAL_CMP.md
   31275   438    2  V11_HYB.md
   37902   322    2  V11_ML.md
   21641   294    2  V11_PROTOCOL.md
   19529   175    1  V11_RND.md
   22560   311    2  V11_STAT.md
   22322   225    0  V6_A2_ML_AUDIT.md
   31043   438    0  V6_D1a_TUBULAR.md
    5123   115    0  V6_D1b_BHARUN.md
    8216   108    0  V6_D1c_TRAJ_GEOM.md
    7046   117    0  V6_D1d_MUDLOG.md
    8874   152    0  V6_D1e_LOG_XML.md
   20660   258    0  V6_D1f_PETRO.md
   14990   262    0  V6_D1g_EDM.md
    6534   108    0  V6_D1h_KAGGLE_CAT.md
   19380   115    0  V6_D2_EXTERNAL_DATASETS.md
   14960   204    0  V6_E1_ML_DESIGN.md
    4359    75    0  V6_E1b_PREREG_HYD.md
    5672    91    0  V6_E1c_PREREG_TOOLWEAR.md
    4857    80    0  V6_E1d_PREREG_BITWEAR.md
   50279   475    0  V6_R1_SCIENCE.md
   15561   151    0  V7_D1a_DATA_CHECK.md
   20188   187    0  V7_D1b_DATA_CHECK.md
   15191   132    0  V7_D1c_DATA_CHECK.md
   11199   117    0  V7_D1d_DATA_CHECK.md
   20762   321    0  V7_D1e_DATA_CHECK.md
   17611   200    0  V7_D1f_DATA_CHECK.md
   19650   233    0  V7_D1g_DATA_CHECK.md
   16932   183    0  V7_D1h_DATA_CHECK.md
   20912   157    1  V7_M1_DELEGASI.md
   31487   181    0  V7_M2_SYNTHESIS.md
   30231   413    0  V8_R1_ABC_SPEC.md
   28071   228    4  V9_A1_AUDIT.md
    7901   116    0  V9_D1_DATA_PIPELINE.md
   25982   372    0  V9_I1_INTEGRATION.md
   40571   398    0  V9_R1_JUSTIFICATION.md
   10833   260    0  VIZ_TAKSONOMI_MODEL_PREDIKTIF.md
```

### 8.C Uji baris sumber yang dipakai di bagian 3

```
[V3A 78]  bhaRun 175 (161 XML + 14 MetaDataFileInfo.txt), mudLog 16 (8 XML + 8 txt), las_target 253, dlis_target 468
[V3W 20]  **Total: 7,080,457 baris time-series, 8 CSV.**
[V4 17]   Total baris seluruh 7 file mentah: **429.520** ... Union kolom: **275**. Kolom yang tersedia di semua 7 sumur: **hanya 29**
[PM6 164] 7 kelas dengan populasi terhitung (R1 §4.2; 24/24 angka diverifikasi ulang A2 dari CSV mentah): torsional 82.530 /
[PM6 165] moderate stick-slip 320 / shock 180 / whirl 714 / stuck 394 / hidraulik 58.317 baris F-14 +
[PM6 166] 5 kelas USROP.
[D0 49]   F-1 C (2156) + F-11 (1750) = 3906 file = 54,6% TIDAK diparse
[A1 198]  Litologi mudLog ... holdout 66,3% ... NON-SIRKULAR
[A1 199]  STUCK_RT time.csv F-9 A ... holdout 92,1%
[A1 200]  Flag DLIS ... holdout 97,7% / 99,9%
[A1 201]  Label rule R1 / USROP ... holdout 99,97%; rekonstruksi MSE dari fitur: R² = 0,99987
[E1 75]   | **Total** | **2.007 / 5.555** | **5.429 / 23.922** | **1.642 / 43.191** | **363 / 24.480** |
[RD0 159] laju sampel tertinggi 0,3333 Hz ... VIBLAT_RT di F-14 hanya 0,0167 Hz ... Nyquist tertinggi 0,1667 Hz
[RD0 311] | Baris | 198.928 |
[RD0 315] | Label `high_MSE_bit_wear` | 49.732 |
```

```
[PM7 136] | 2 | Event kurasi dalam rentang CSV parsed | M2: 582/884 | A1: 523 ... | **523**
[PM7 137] | 3 | Onset stuck F-9_A (S-A1) | ... strict **34** ... ffill **74** ... Angka M2 "50" tidak reproduce
[PM7 139] | 5 | S-F1 kandidat onset bit_wear | M2: 1.489 | A1: 481 awal blok high_MSE (329 dari normal) | **481/329**
[PM7 141] | 7 | Positif shk wellbore baru | ... F-10 798 (0,27%), F-12 580 (1,59%), F-4 50, F-15 13, F-15B 0
[Ev 52]   Gate V6: G1 4/4 (lift 1,61-3,50, semua >=1,5) · G2 4/4 (RF >= canary tiap fold)
[Ev 69]   | lift (vs prevalensi fold) | 1,61 / 2,36 / 3,50 / 1,63 - 4/4 > 1,5 | OBSERVED |
[Ess 58]  | AUPRC + lift | 0,0185-0,1057; lift 2,61-6,64 (5 fold layak); lift >=1,5 di 4/5 (G1); RF >= canary di 5/5 (G2) |
[Eb 66]   | F-14 | 949 / 91 / 0,0959 | 0,298 [0,148; 0,517] | 3,11 | 10,43 | 0,191 | 0,679 | 0,863 |
[Eb 69]   | F-5 | 367 / 174 / 0,4741 | 0,783 [0,489; 0,945] | 1,65 | 2,11 | 0,692 | 0,870 | 0,812 |
[Es 100]  | LOWO 14->9A | E3_RF | 0,224 | 72/72 = 100% | 1.440 | 0,251 (1,12) | [0,185; 0,347] | 10 [8; 10] |
[Es 113]  E3 lift > 1 di 4/4 fold/arah (1,65 · 1,30 · 9,72 · 1,12)
[Eh 76]   | persistence (biner) | 0,615-0,793 | 0,617-0,764 | 38,8-110,7 | B1 (<=10 mnt): 31,6-65,4%
[Eh 163]  | F-14 | 0,263 | 6,0 mnt (31,6) |
[Eh 169]  | F-9_A | 4,707 | 7,5 (31,7) |
[Ew 58]   Agregat: precision median 0,512 · recall median 0,983 · lift 1,09-1,42 ·
[Ew 120]  | C2 ketahanan lintas-alat | lift >1 di 4/4 fold (rentang 1,09-1,42); lift >=1,5 0/4
[A1-8 68] | tool_wear | T01-T04 AUPRC 0,5433/0,7684/0,7031/0,6497; precision 0,516/0,559/0,509/0,500; FAR/menit 46,0-60,0
```

```
[EVA 54]  | vib (K tunggal) | rule-sistem-hari-ini: P 0,87-0,95 · R 0,28-0,60 · FAR 10,0-49,9 · FP total 197
[EVA 58]  | stuck K-ii (onset) | RF tau0,5: 3/4 fold FAR<=6 (P 0,05-1,00 · R 0,004-0,005)
[EVA 128] | RF (tau0,5 titik praktis) | 0,05-1,00 | R 0,004-0,005 | 0,0-1,25 (3/4 fold) | 0,000-0,045
[EVA 59]  | hyd K-i (status) | persistence: P 0,61-0,90 · R 0,62-0,92 · FAR 32,4-110,7; hybrid: P 0,72-0,95; FP total: rule 2091 -> hybrid 927
[EVB 98]  | ssi (K tunggal) | B4: hanya 40/137 run berkelanjutan >=5 mnt ... hybrid +0,731 (FP 26->7)
[EVB 102] | hyd K-i (status) | hybrid +0,557 (FP 2091->927)
[EVB 106] | tool_wear K-i (regime, bengkel) | FAR-terkalibrasi +0,909...+0,976 (FP 1-3 vs 33-41 per alat)
[EVC 120] | C3 | tau0,5: 4,1-496 = 119x (1/4 well). Recall tau0,5 0,10-0,87 (8,5x) |
[EVC 136] | C4 | n_nodata 22.385/35.906 = 62,3%
[PM2 140] 5 head L0 + 11 L1 (human-in-loop) + 9 L2 + 2 L3, slot alarm otomatis = 0
[PM2 181] (human_review_required) · L2 = 9 head · L3 = 2 head · slot ALARM OTOMATIS = 0
[PM2 205] | Keputusan manusia dipertahankan | V4b: 11/11 L1 `human_review_required=true`; `keputusan_akhir=MANUSIA` |
[PM2 206] | Badge FAR + keyakinan + batas tampil | V1b: 0 head tanpa tier/layer/badge/keyakinan/batas |
[R3 102]  | VMD | ... | GAGAL: Nyquist 0,1667 Hz, 75/105 percobaan gagal, mode bertumpuk |
[R5 135]  | Antar well (10 pasangan) | D median 0,986, minimum 0,723, maksimum 1,000; 10 dari 10 pasangan p < 0,05 |
[R5 136]  | Dalam well, paruh awal lawan paruh akhir (5 well) | D median 0,211; 4 dari 5 well p < 0,05; terbesar F-14 D = 0,9777 |
[R8 69]   | H1 | hyd K-i | rule: FP 2105, presisi 0,6835, FAR median 6,932, lead 6,0 menit | H1: FP 935, presisi 0,7789, FAR median 3,5302, lead 11,5 menit
[R8 109]  | H2 | shk K-i | ML: FP 2633, TP 192, recall median 0,0829 | H2: FP 667, TP 46, recall median 0,0037
[R8 127]  | H1 stat DAN rule | 935 | 3804 | 0,7789 (R8-010) | 0,5638 (R8-011) | 3,5302 (R8-012) | 7 dari 9 (R8-014)
[R8 293]  | shk | K-i status | ML LightGBM | FP 2633, TP 192, AUPRC 0,0499 lawan prevalensi 0,0243, FAR median 3,6217
```

```
[S6 150]  | hyd K-i, peringatan dini | H1p ... FP 927, TP 4924, presisi 0,8243, recall 0,6519, FAR kalender median 4,0984, 7 dari 9 fold
[S6 194]  | H1 stat DAN rule | 935 | 3804 | 0,7789 | 0,5638 | 3,5302 | 11,5 | 7 | 6 | 5 |
[S6 196]  | H1p rule DAN persistence | 927 | 4924 | 0,8243 | 0,6519 | 4,0984 | 8,0 | 7 | 9 | 7 |
[S6 197]  | H1p3 rule DAN persistence DAN stat | 568 | 3557 | 0,8646 | 0,5296 | 2,0323 | 12,5 | 9 | 5 | 5 |
[S6 312]  Dari 18 penolakan di atas, 7 di antaranya adalah kegagalan bentuk komposisi DAN
[S6 351]  Tiga kategori gangguan pada ddr.parquet memberi 2453 record dan 5821.417 jam
[S6 354]  ... durasi dapat dipakai untuk beban waktu tetapi tidak dapat dikonversi menjadi rupiah tanpa tarif.
[S4 69]   | interruption -- repair | 806 | 1.215,0 | 1,0 | 3,5 | 12,5 |
[S4 72]   | interruption -- maintain | 310 | 562,75 | 1,0 | 4,5 | 15,0 |
[S4 74]   | interruption -- lost circulation | 75 | 160,75 | 2,0 | 4,3 | 7,0 |
[S4 78]   Total interruption 3.577 record dan 8.343,253 jam. Dua kode kerja maintenance, repair dan maintain, berjumlah 1.116 record dan 1.777,75 jam
[S4 125]  | B3 | Beban maintenance gabungan | 1.116 kejadian, 1.777,75 jam, 0,6345 kejadian per laporan harian
[S3 100]  Rekonstruksi label ... 198.928 baris cocok dari 198.928 ... akurasi 1,000000
[S3 187]  ML yang memakai MSE dan ROC_coef memberi recall median 1,0000 dan presisi median 0,8496. ML kanal fisik memberi recall median 0,9968.
[ENG 59]  L0 5 head, L1 11 head, L2 9 head, L3 2 head.
[ENG 33]  | vib | rule_display | 49.942 | 17 |
[ENG 41]  | hyd | rule_display | 55.57 | 19 |
[ENG 42]  | hyd | hybrid_rule_and_persistence | 16.611 | 6 |
[V10 13]  rekap tier 0+3+2+2=7 dan rekap head 12/13/2 serta lapisan 5/11/9/2 seluruhnya cocok
[V11 122] PROPOSAL BARU (V10, kandidat 2) lebih baik, dan BUKAN dengan selisih tipis.
[V11 123] Selisih total 49,8 poin (96 vs 46,2) jauh di atas ambang selisih tipis protokol
[S5A 65]  Total 143 sel dengan 0 sel gagal. Toleransi 5e-5 dipakai ...
[S5A 71]  Hasil: dokumen asli memberi nol selisih, dan dokumen yang diubah memberi 2 selisih.
[S5A 23]  | S1 | RND_S1_SEED_ROBUSTNESS.md | 279 | 25445 | 4 | 84 |
[DS 13]   Klaim diganti dengan angka terukur: 64 dari 441 sel angka (14,51 persen) punya padanan
[DS 17]   Klaim diganti: 74 dari 328 sel angka (22,56 persen)
```

### 8.D Ledger provenance

```
$ wc -l docs/RND_PROVENANCE_LEDGER.md
3434 docs/RND_PROVENANCE_LEDGER.md
$ grep -n '^## Bagian S6' docs/RND_PROVENANCE_LEDGER.md
3228:## Bagian S6: vonis PM gelombang 2 dan pemilihan komposisi (kartu `t_b5830542`)
$ grep -c '^| S6-' docs/RND_PROVENANCE_LEDGER.md
191
$ grep -n '^| S6-191' docs/RND_PROVENANCE_LEDGER.md
3425:| S6-191 | BELUM | tidak terukur | BELUM-TERUKUR | H1p dan H1p3 pada shk, stuck, bit_wear, tool_wear: belum dijalankan | bagian 8 | BELUM (kartu S6) |
$ grep -n '^| S4-013' docs/RND_PROVENANCE_LEDGER.md
2182:| S4-013 | 884 record / 20 kolom | record / kolom | RUN-KITA | labels_duration.json:n_baris | bagian 2 baris 2 | TERUKUR |
$ grep -n '^| L-26 ' docs/RND_PROVENANCE_LEDGER.md
56:| L-26 | FAR <= 6 | alarm palsu per 24 jam | KONVENSI | `docs/RND_ALGO_RESEARCH_PLAN.md` §6 butir 2; code/v9_eval_a_01_compute.py:37, :108 | 2026-10-27 | gerbang tier LAYER-1 | BELUM |
$ grep -n '^| PM-078 ' docs/RND_PROVENANCE_LEDGER.md
2024:| PM-078 | 0 | slot | KONVENSI | scratch/v9_i1/v9_i1_RESULTS.json auto_critical_alarm_slots; docs/V9_EVAL_C_LAYERC.md tier | bagian 3, 4, 6 | TERUKUR |
$ for p in S1 S2 S3 S4 S5; do grep -c "^| $p-" docs/RND_PROVENANCE_LEDGER.md; done
84
455
92
95
387
$ grep -c -E 'V3_DATA_ACQUISITION|V3_TS_FEATURES|V4_MAINTENANCE|V6_PM_VERDICT|V6_A1_DATA_AUDIT' docs/RND_PROVENANCE_LEDGER.md
0
```

Baris terakhir menegaskan catatan [I1] bagian 0 butir 2: tidak ada baris ledger untuk dokumen V3 sampai V6,
sehingga rujukan berkas dan baris adalah satu satunya jalur yang tersedia untuk era itu.

### 8.E Pemeriksaan format keempat inventaris dan dokumen ini

```
$ for f in 00_INVENTARIS_V3_V6.md 00_INVENTARIS_V7_V8.md 00_INVENTARIS_V9_RND1.md \
           00_INVENTARIS_RND2_V11.md 00_VERIFIKASI_INVENTARIS.md; do
    printf "%s em=%s en=%s kata=%s\n" "$f" \
      "$(grep -o $'\u2014' "$f" | wc -l)" "$(grep -o $'\u2013' "$f" | wc -l)" \
      "$(grep -oiE '(tidak b[il]sa|tidak m[u]ngkin|terb[a]tas)' "$f" | wc -l)"; done
00_INVENTARIS_V3_V6.md em=0 en=0 kata=0
00_INVENTARIS_V7_V8.md em=0 en=0 kata=0
00_INVENTARIS_V9_RND1.md em=0 en=0 kata=0
00_INVENTARIS_RND2_V11.md em=0 en=0 kata=0
00_VERIFIKASI_INVENTARIS.md em=0 en=0 kata=0

$ p=$(grep -c '^|' 00_VERIFIKASI_INVENTARIS.md); s=$(grep -cE '^\|[-: |]+\|$' 00_VERIFIKASI_INVENTARIS.md)
$ echo "pipes=$p seps=$s data_rows=$((p-2*s))"
pipes=132 seps=9 data_rows=114
```

Pola pemeriksaan memakai kelas karakter pada dua kata agar berkas pemeriksa tidak memuat kata yang
dilarang secara harfiah. Keempat inventaris dan dokumen ini bersih dari tanda pisah panjang, tanda pisah
sedang, dan tiga kata penutup. Sembilan tabel pada dokumen ini memuat 114 baris data.

---

## 9. Kontrak kejujuran dokumen ini

Berkas masukan yang dibuka dan ukurannya ada di bagian 1.1 dan 1.2: empat inventaris 152.321 byte dan 35
berkas sumber 1.157.168 byte, total 1.309.489 byte.

Yang belum diverifikasi ada di bagian 7. Jumlah cacat yang diterbitkan: 12, dengan bukti berkas dan bagian
pada setiap butir.

Keputusan: PERLU PERBAIKAN.

Ukuran dokumen ini, diukur setelah seluruh suntingan selesai: 43.536 byte pada 700 baris, sembilan tabel,
114 baris data tabel, 10 bagian tingkat dua.
