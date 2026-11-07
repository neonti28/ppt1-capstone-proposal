# 00 INVENTARIS V7-V8: vonis era kapabilitas menjadi calon fitur

Kartu: `t_daab65b3` (ARKOLOG V7-V8) · Board: `fitur-v9-swarm` · Tanggal: 2026-10-31 (WIB)
Sifat dokumen: INVENTARIS. Dokumen ini tidak menjatuhkan vonis baru, tidak menjalankan model,
dan tidak mengubah angka sumber. Tugasnya satu: membaca vonis V7 dan V8, lalu mengubah
kapabilitas per kelas kerusakan menjadi calon fitur yang bisa dibangun.

Cara membaca: setiap angka diikuti rujukan berkas dan nomor baris dalam tanda kurung.
Singkatan berkas ada di bagian 1.

---

## 0. Kerangka wajib (dipakai apa adanya, tidak diubah)

1. Alarm otomatis BUKAN tujuan. ML dipakai sebagai sistem pendukung keputusan dengan skor
   keyakinan, bukan pemutus. Konsekuensi operasional: setiap fitur di bawah wajib menampilkan
   angka keyakinan dan menyebut batas pemakaiannya di layar yang sama.
2. Setiap angka wajib punya sumber berkas dan baris, atau baris ledger
   `docs/RND_PROVENANCE_LEDGER.md`.
3. Tidak ada klaim "berjalan" tanpa bukti. Perintah yang dijalankan untuk memeriksa angka
   ditempel keluarannya di bagian 15.
4. Kekurangan data dikemas menjadi fitur berguna (pola Dynamic Island), bukan keluhan. Contoh
   penerapan: sumur yang belum terkalibrasi tidak disembunyikan, tetapi ditampilkan sebagai
   kartu kesiapan dengan daftar berkas yang sudah tersedia.
5. Setiap fitur punya lima field wajib: pengguna, momen pakai, masukan, keluaran, status bukti.
6. Setiap kekurangan data ditutup dengan syarat yang dibutuhkan (bagian 13), bukan dengan
   pernyataan penolakan. Bila sesuatu belum tersedia, yang ditulis adalah syaratnya.
7. Keluaran hanya markdown di `planning/`. Tidak ada berkas .py, .html, .json, .csv sebagai
   deliverable kartu ini.
8. Tidak memakai tanda pisah panjang. Rentang angka ditulis dengan tanda hubung biasa.

---

## 1. Berkas yang dibuka dan ukuran byte

Ukuran diambil dari `wc -c -l` yang dijalankan pada 2026-10-31 (keluaran penuh di bagian 15.A).

| Kode | Berkas | Byte | Baris |
|---|---|---:|---:|
| [PM7] | `docs/V7_PM_VERDICT.md` | 23.569 | 286 |
| [R1] | `docs/V7_R1_SOLUTIONS.md` | 34.950 | 270 |
| [A1-7] | `docs/V7_A1_SOLUTION_AUDIT.md` | 17.731 | 232 |
| [PM8] | `docs/V8_PM_VERDICT.md` | 23.720 | 364 |
| [M1] | `docs/V8_M1_CAPABILITY_MAP.md` | 23.716 | 229 |
| [A1-8] | `docs/V8_A1_CAPABILITY_AUDIT.md` | 14.818 | 118 |
| [Eh] | `docs/V8_E_hyd_CAPABILITY.md` | 16.345 | 231 |
| [Es] | `docs/V8_E_stuck_CAPABILITY.md` | 22.172 | 293 |
| [Eb] | `docs/V8_E_bit_wear_CAPABILITY.md` | 16.116 | 225 |
| [Ev] | `docs/V8_E_vib_CAPABILITY.md` | 13.970 | dipakai untuk angka `vib` |
| [Ess] | `docs/V8_E_ssi_CAPABILITY.md` | 12.678 | dipakai untuk angka `ssi` |
| [Ek] | `docs/V8_E_shk_CAPABILITY.md` | 17.176 | dipakai untuk angka `shk` |
| [Ew] | `docs/V8_E_tool_wear_CAPABILITY.md` | 11.876 | dipakai untuk angka `tool_wear` |
| [L] | `docs/RND_PROVENANCE_LEDGER.md` | 471.945 | ledger provenance |

Total sembilan berkas masukan wajib: 193.137 byte pada 2.248 baris (bagian 15.A). Empat profil
`[Ev] [Ess] [Ek] [Ew]` tidak ada dalam daftar masukan kartu, tetapi keberadaannya terverifikasi
di `docs/` (bagian 15.F) dan dipakai hanya untuk mengutip angka yang juga sudah muncul di [M1]
dan [A1-8]. Setiap angka tetap menyebut baris berkasnya.

---

## 2. Vonis V7 dan vonis V8 dalam ringkas

### 2.1 V7: vonis atas JALUR metode, bukan atas hasil run

- Vonis: LEBIH BAIK, dengan syarat eksekusi, "bukan mungkin" ([PM7] baris 29).
- Baseline V6 yang dikutip: 2 LULUS penuh (`vib`, `ssi`) + 1 LAYAK BERSYARAT (`bit_wear`) +
  4 GAGAL (`stuck`, `shk`, `hyd`, `tool_wear`) ([PM7] baris 31-33).
- Kriteria vonis: jalur metode-sah ke minimal 5 kelas lolos gate, gate G1/G2 tidak digeser
  ([PM7] baris 7-8, 48-51).
- Lantai skenario terburuk 4 kelas, target 5, upside 7 ([PM7] baris 61-63, 161-166).
- Estimasi peluang: P(capai >=5) sekitar 60-70 persen, P(lantai 4) sekitar 25 persen,
  P(<4) di bawah 10 persen ([PM7] baris 258-259). Ini estimasi berbasis kekuatan bukti per
  jalur, bukan janji.
- Angka yang dikoreksi dan dipakai seterusnya: onset stuck ketat 34, ffill 74, angka "50" tidak
  terreproduksi oleh definisi mana pun ([PM7] baris 137); kandidat onset bit_wear 481 awal blok,
  329 dari kondisi normal ([PM7] baris 139); event kurasi dalam rentang 523, bukan 582
  ([PM7] baris 136); inefisiensi USROP non-normal 64.915, bukan 78.212 ([PM7] baris 140);
  positif shk F-10 798 dan F-12 580 ([PM7] baris 141).
- Anti-geser-gate: LULUS, G1 lift >=1,5 mayoritas, G2 AUPRC >= canary, <30 positif =
  UNDERPOWERED, persistence > RF = layak bersyarat, LOWO, kanal pembentuk label dilarang jadi
  fitur, semuanya identik V6 ([A1-7] baris 98-109).

Kesimpulan untuk inventaris ini: V7 memberi DAFTAR JALAN (label onset, penambahan data, unit
stand, reformulasi), dan angka jalannya sudah diverifikasi silang. V8 kemudian mengukur apa yang
sudah berjalan hari ini.

### 2.2 V8: vonis atas KAPABILITAS hari ini

- Vonis: KOHEREN dan LAYAK PAKAI sebagai alat PdM kelas advisory atau human-in-loop. BUKAN
  sebagai alat alarm otomatis kritis, karena 0 dari 7 engine memenuhi syarat alarm
  ([PM8] baris 29-31).
- Angka audit: 121 klaim numerik unik dihitung ulang plus 45 sel tabel per-well shk, hasil 114
  terverifikasi, 6 selisih nyata, 0 klaim karangan ([A1-8] baris 19-25).
- Enam selisih penyajian dan adjudikasinya: dipakai angka hitung ulang A1, tidak satu pun
  membalikkan tier engine ([PM8] baris 100-116).
- Tier akhir: 0 layak alarm otomatis, 3 layak peringatan human-in-loop terbukti, 2 layak
  peringatan bersyarat, 2 tier tertinggi hanya tren atau skor, 7 dari 7 punya peran
  ([PM8] baris 180-184; [M1] baris 169-174).

### 2.3 Tabel tier per kelas (bahan utama inventaris)

| Kelas | Tier tertinggi hari ini | Angka kapabilitas kunci | Batas pemakaian yang wajib tampil |
|---|---|---|---|
| `vib` | Tren + peringatan advisory BERSYARAT ([M1] baris 50) | lift 4/4 >=1,5 pada rentang 1,61-3,50 ([Ev] baris 52, 69); RF >= canary 4/4; persistence menang 2/4 ([Ev] baris 53) | B3, B4, FAR belum pernah dicetak ([M1] baris 50) |
| `ssi` | Tren + peringatan human-in-loop BERSYARAT ([M1] baris 51) | AUPRC 0,0185-0,1057, lift 2,61-6,64, lift >=1,5 di 4/5 fold, RF >= canary 5/5 ([Ess] baris 58); persistence kalah 0/5 ([Ess] baris 59) | B1 sampai B4 belum terukur; CI-bawah di atas no-skill hanya 2/5 fold ([M1] baris 51) |
| `bit_wear` | Tren/screening K-1 + konfirmasi status ([M1] baris 52) | RF >= canary 4/4 dengan delta B +0,058 sampai +0,107; RF kalah persistence 4/4 dengan delta B -0,087 sampai -0,381; persistence AUPRC 0,679-0,984 ([Eb] baris 40, 66, 68) | precision, recall, FAR belum terukur; K-2 onset belum berangka ([Eb] baris 98, 111-114) |
| `stuck` | Triage manual terbantu pada sumur mirip F-10 ([Es] baris 228) | E3 lift 4/4 di atas 1 (1,65 / 1,30 / 9,72 / 1,12), CI signifikan 1/4 ([Es] baris 113-114); E1 P 0,457 hanya di F-10, lead median 10 menit ([Es] baris 88) | B1 maksimum 31,8 persen, FAR 9,9 sampai 1.440, kontrol-positif 0/10 ([Es] baris 129, 132, 226) |
| `hyd` | K-ii indikasi dini menit + K-i tren status ([M1] baris 54) | persistence P 0,615-0,793, delta B negatif 7/7 ([Eh] baris 76, 62); K-ii AUPRC test 0,228, lift titik 61,6, T_lead median 7 menit, B1 66,7 persen ([Eh] baris 101, 141) | FAR K-i 38,8-110,7 per 24 jam; peringatan dini K-i 0/1 episode; K-ii 1 wellbore dan 3 onset test ([Eh] baris 125, 76, 95) |
| `shk` | Screening berbiaya cek tinggi + peringatan situasional ([M1] baris 55) | lead 2-9 menit, median global 5,0 ([Ek] baris 82); RF >= persistence B1 di 9/9 fold ([Ek] baris 107); 4 titik operasi FAR <=6 di rentang P 0,26-0,55 ([Ek] baris 60) | B1 0-0,348, B3 NEGATIF -0,11 sampai -53,75, FAR <=1 dengan recall>0 hanya 1 titik ([Ek] baris 82, 84; [A1-8] baris 45) |
| `tool_wear` | Skor LOTO lintas-alat + detektor perubahan regime ([M1] baris 56) | AUPRC 0,5433 / 0,7684 / 0,7031 / 0,6497; precision 0,516 / 0,559 / 0,509 / 0,500 ([A1-8] baris 68); lift 1,09-1,42, G1 0/4 ([Ew] baris 120) | precision biner mendekati peluang; change-point signifikan 8/8 termasuk 8/8 alat baru sehingga spesifisitas keausan gagal ([M1] baris 56; [Ew] baris 74) |

---

## 3. Hitungan tier dan syarat naik tingkat

Tier dijumlahkan per ENGINE, tujuh unit: 0 + 3 + 2 + 2 = 7, tanpa engine dihapus dan tanpa
engine dobel ([M1] baris 174; [PM8] baris 176-177).

Syarat naik tingkat yang sudah tertulis dan tidak boleh digeser:

| Tingkat tujuan | Syarat | Sumber |
|---|---|---|
| Masuk LAYER-1 (peringatan human-in-loop) | FAR <=6 per 24 jam negatif TERUKUR dengan recall > 0, T_lead atau B4 terukur, C4 terpenuhi, kalibrasi lokal per sumur | [M1] baris 141-143 |
| Masuk LAYER-0 alarm otomatis | FAR <=1 per 24 jam negatif dengan recall > 0, B1 >= 80 persen, C2 per bin, C3 dropout < 20 persen, validasi kejadian nyata | [M1] baris 144-145 |
| Ambang FAR <= 6 sebagai gerbang tier | konvensi operasional, bukan standar eksternal | [L] baris 56 (L-26), status BELUM |
| Slot alarm otomatis hari ini | 0 slot | [L] baris 2024 (PM-078), status TERUKUR |

Delapan gap yang memblokir ekspansi dan tidak memblokir fungsi dasar: G1 diagnosis nol engine,
G2 alarm otomatis 0/7, G3 B3 negatif di shk, G4 horizon peringatan <=10 menit, G5 generalisasi
lintas-wellbore, G6 C3 baru teruji di 2 engine, G7 validitas label lintas-well, G8 onset
bit_wear nol angka ([PM8] baris 194-203).

---

## 4. Skor keyakinan: definisi dan hasil hitung

Skor keyakinan (SK) 0-100 adalah USULAN DESAIN untuk kartu-kartu fitur berikutnya. Ia bukan
metrik tervalidasi, dan seluruh masukannya adalah angka yang sudah terukur di dokumen sumber.
Status bukti: usulan desain. Yang divalidasi baru aritmetikanya, bukan daya pisahnya.

Rumus:

```
SK = 100 x ( 0,40 x S_A + 0,35 x S_B + 0,25 x S_C )
```

- `S_A` kekuatan sinyal. 0,75 bila lift >=1,5 di mayoritas fold, menang terhadap baseline utama
  mayoritas, dan baseline sekunder tidak kalah di mayoritas fold. 0,60 bila lift >1 di mayoritas
  fold tetapi CI95 belum signifikan mayoritas. 0,30 bila menang terhadap baseline lemah tetapi
  kalah terhadap baseline terbaik kelas itu. 0,20 bila belum terukur.
- `S_B` kesiapan operasional. 1,00 bila B1 >= 80 persen dan FAR <= 1 terukur. 0,60 bila B1
  50-79 persen atau FAR 2-6. 0,35 bila B1 < 50 persen atau FAR > 6 terukur. 0,20 bila belum
  terukur sama sekali.
- `S_C` keterpercayaan, rata-rata C1 sampai C4, masing-masing dinilai 1, 0,5, atau 0.

Hasil hitung per kelas. Semua masukan S_A, S_B, S_C diambil dari angka di bagian 2.3.

| Kelas | S_A | S_B | S_C | Perhitungan | SK |
|---|---:|---:|---:|---|---:|
| `vib` | 0,75 | 0,20 | 0,50 | 0,40x0,75 + 0,35x0,20 + 0,25x0,50 = 0,495 | 50 |
| `ssi` | 0,75 | 0,20 | 0,625 | 0,40x0,75 + 0,35x0,20 + 0,25x0,625 = 0,526 | 53 |
| `bit_wear` | 0,30 | 0,20 | 0,25 | 0,40x0,30 + 0,35x0,20 + 0,25x0,25 = 0,253 | 25 |
| `stuck` | 0,60 | 0,35 | 0,375 | 0,40x0,60 + 0,35x0,35 + 0,25x0,375 = 0,456 | 46 |
| `hyd` K-i | 0,75 | 0,35 | 0,75 | 0,40x0,75 + 0,35x0,35 + 0,25x0,75 = 0,610 | 61 |
| `hyd` K-ii | 0,60 | 0,60 | 0,25 | 0,40x0,60 + 0,35x0,60 + 0,25x0,25 = 0,512 | 51 |
| `shk` | 0,60 | 0,35 | 0,625 | 0,40x0,60 + 0,35x0,35 + 0,25x0,625 = 0,519 | 52 |
| `tool_wear` | 0,30 | 0,60 | 0,50 | 0,40x0,30 + 0,35x0,60 + 0,25x0,50 = 0,455 | 46 |

Catatan pembacaan:
- SK menilai keyakinan pada bukti untuk pernyataan yang dinyatakan, bukan peringkat tier. `vib`
  dapat SK 50 karena B belum diukur, bukan karena sinyalnya lemah; ini justru pesan yang harus
  tampil di layar.
- `tool_wear` mendapat S_B 0,60 karena B1 4/4 alat dan FAR <= 1 per menit memang terukur, tetapi
  sampel hanya 4 alat dan domainnya bengkel berdetik, sehingga tidak dinaikkan ke 1,00
  ([Ew] baris 53, 58, 119).
- `bit_wear` mendapat S_A 0,30 karena menang terhadap canary tetapi kalah terhadap persistence di
  4/4 fold, dan baseline terbaik kelas status ini adalah persistence ([Eb] baris 40).
- Angka SK tidak boleh dipakai sebagai ambang keputusan sebelum ada uji daya pisah. Bila nanti
  dipakai, pemetaan S_A, S_B, S_C wajib dibekukan lebih dulu sebagai pra-registrasi.

---

## 5. Kelas `vib`

**Vonis.** V6 LULUS penuh ([PM7] baris 40). V8 menempatkannya pada tier Tren + peringatan
advisory BERSYARAT, dengan syarat mengukur FAR_t dan B4 di kampanye penguatan F-4, F-10, F-15
([M1] baris 50).

**Angka kapabilitas.**
- Gate V6: G1 4/4 dengan lift 1,61-3,50, semua di atas 1,5; G2 4/4 RF >= canary ([Ev] baris 52).
- Lift per fold 1,61 / 2,36 / 3,50 / 1,63, tercatat OBSERVED ([Ev] baris 69).
- Persistence mengalahkan RF di 2/4 fold, tidak mayoritas ([Ev] baris 53).
- Baseline persistence AUPRC 0,517-0,796, canary kedalaman 0,277-0,612 ([Ev] baris 39).
- Lapisan B belum terukur karena B3, B4, dan FAR tidak pernah dicetak V6 ([M1] baris 50).
- Lapisan C sedang: C4 penuh, C2 parsial, C1 spread AUPRC 0,471 lebar, C3 nol bukti
  ([M1] baris 50).

**Batas.** Bukan alarm otomatis. Klaim lead time menit belum boleh dibuat. Generalisasi non-Volve
belum diuji. GETARAN status dikonfirmasi, bukan onset diprediksi.

**Fitur.**

| Fitur | Pengguna | Momen pakai | Masukan | Keluaran | Status bukti |
|---|---|---|---|---|---|
| V-1 Panel status getaran dengan badge keyakinan | Driller dan mudlogger di rig | Shift dimulai, layar status dibuka | `VIBLAT_RT` grid 60 detik, status persistence jendela sebelumnya, skor RF | Status normal atau perhatian, SK 0-100 dari rumus bagian 4, satu baris alasan | A kuat: lift 4/4 >=1,5 ([Ev] baris 52). B belum terukur, badge wajib berbunyi "advisory" |
| V-2 Kartu kesiapan kalibrasi per sumur (pola Dynamic Island) | Engineer PdM sebelum menyalakan panel di sumur baru | Sebelum instalasi, dan setiap kali pindah sumur | Daftar berkas kanal per wellbore: F-4 86 file, F-10 66 file, F-15 76 file `VIBLAT_RT` ([R1] baris 45-48; [A1-7] baris 83) | Status siap atau belum, jumlah berkas tersedia, tombol permintaan kalibrasi | Jumlah berkas terverifikasi dua pihak. Efek kalibrasi belum diukur |
| V-3 Buku catatan keputusan operator | Engineer PdM dan supervisor | Setiap notifikasi ditutup dengan keputusan | Notifikasi, tindakan yang diambil, hasil 24 jam | Rekap hitungan peringatan yang benar dan salah, dasar pengukuran B3 | Belum ada angka. Fitur ini yang MENGUMPULKAN B3 yang sekarang belum terukur ([M1] baris 194, G3) |

**Catatan.** Fitur V-2 adalah contoh langsung pola Dynamic Island: yang hari ini dianggap
kekurangan (sumur belum terkalibrasi) menjadi informasi yang bisa dibaca dan ditindak.

---

## 6. Kelas `ssi`

**Vonis.** V6 LULUS tetapi rapuh ([PM7] baris 41). V8 menempatkannya pada tier Tren +
peringatan human-in-loop BERSYARAT, syaratnya FAR diukur dan label keyakinan wajib tampil, bukan
angka tunggal ([M1] baris 51).

**Angka kapabilitas.**
- AUPRC 0,0185-0,1057, lift 2,61-6,64, lift >=1,5 di 4/5 fold atau G1, RF >= canary 5/5 atau G2
  ([Ess] baris 58).
- RF tidak dikalahkan persistence di 5/5 fold, persistence menang 0/5; catatan jujur, angka
  AUPRC persistence per fold tidak dicetak di V6 ([Ess] baris 59).
- Delta B terhadap canary positif di 5/5 fold, dengan canary pada rentang 0,0055-0,0676
  ([Ess] baris 34, 60).
- CI-bawah di atas no-skill hanya 2/5 fold ([M1] baris 51).
- Lapisan B belum terukur seluruhnya, konsekuensi dari tugas status ([M1] baris 51).

**Batas.** Bukan alarm otomatis. Klaim onset dan lead time belum boleh dibuat. Satu-satunya
detektor SSI, lapisan rule tetap menjadi dasar. Fold F-7 dengan 3 positif dan F-9 dengan 12
positif berstatus UNDERPOWERED ([R1] baris 197).

**Fitur.**

| Fitur | Pengguna | Momen pakai | Masukan | Keluaran | Status bukti |
|---|---|---|---|---|---|
| S-1 Skor keyakinan stick-slip per jendela | Driller | Setiap jendela 60 detik saat putaran aktif | Rumus SSI dari CRPM, probabilitas RF, jumlah positif fold latih | SK 53, label sumber (rule atau ML), indikator "CI lebar" bila fold latih kecil | A tinggi, B belum; SK 53 dari bagian 4 |
| S-2 Penanda daya statistik per sumur | Engineer PdM | Sebelum mempercayai S-1 di sumur tertentu | Jumlah positif per sumur: F-7 3, F-9 12, sisanya di atas 30 ([R1] baris 197) | Label UNDER di layar, panel S-1 dinonaktifkan untuk sumur itu | Terverifikasi sebagai angka; aturan nonaktif adalah usulan desain |
| S-3 Watchlist severe stick-slip lintas sumur | Supervisor operasi | Rapat pagi dan serah terima shift | Skor S-1 seluruh sumur, kelas severitas SSI >= 3 ([L] baris 5, L-05) | Daftar sumur urut risiko harian, tanpa notifikasi otomatis | Kelas severitas punya rujukan jurnal terverifikasi; agregasi lintas sumur belum diuji |

---

## 7. Kelas `bit_wear`

**Vonis.** V6 LAYAK BERSYARAT ([PM7] baris 43). V8 menempatkannya pada tier Tren/screening K-1
untuk 4 wellbore teruji, ditambah konfirmasi status ([M1] baris 52).

**Angka kapabilitas.**
- K-1 status: RF menang terhadap canary 4/4 dengan delta B +0,058 sampai +0,107, dan kalah
  terhadap persistence 4/4 dengan delta B -0,087 sampai -0,381 ([Eb] baris 76-81).
- Persistence AUPRC 0,679-0,984, disebut engine status terukur terbaik ([Eb] baris 40, 88).
- AUPRC per fold: 0,298 / 0,365 / 0,813 / 0,783; canary 0,191 / 0,288 / 0,756 / 0,692
  ([Eb] baris 66-69).
- Cakupan 4 dari 7 sumur, tiga fold UNDERPOWERED ([Eb] baris 71-72).
- B2 lead masuk blok sekitar nol, transisi terdeteksi satu jendela atau sekitar 10 menit
  TERLAMBAT, ditandai DERIVED ([Eb] baris 167; [M1] baris 52).
- K-2 onset: hanya inventaris 481 kandidat, 329 transisi dari normal ([Eb] baris 103-105;
  [PM7] baris 139). Semua metrik K-2 belum terukur ([Eb] baris 111-114).
- Precision, recall, dan FAR K-1 belum terukur; bukti ketiadaan dari grep artefak
  `E1d_LOWO_RESULTS.json` ([Eb] baris 96-98).

**Batas.** Bukan alarm. Bukan peringatan dini masuk blok. Klaim diagnosis atau identitas bit
tidak tersedia karena EDM BLOCKED ([Eb] baris 54-56; [PM8] baris 196).

**Fitur.**

| Fitur | Pengguna | Momen pakai | Masukan | Keluaran | Status bukti |
|---|---|---|---|---|---|
| B-1 Kurva tren keausan dengan cap keterlambatan | Engineer drilling dan supervisor | Evaluasi performa bor harian | Status `high_MSE` persistence, AUPRC 0,679-0,984 sebagai dasar bobot, skor RF screening | Kurva tren, SK 25, cap eksplisit "terlambat satu jendela sekitar 10 menit" | A terukur, B hanya lead negatif, C lemah; SK 25 dari bagian 4 |
| B-2 Penghitung kesiapan onset K-2 | Engineer PdM dan peneliti | Sebelum menjadwalkan kampanye K-2 | Inventaris onset 481 dan 329, daftar metrik yang belum ada | Kartu "481 kesempatan deteksi terverifikasi, 0 metrik terukur", daftar syarat kampanye | Angka onset terverifikasi dua pihak ([Eb] baris 185); metrik nol, dinyatakan apa adanya |
| B-3 Pengingat jendela bit-change berbasis blok inefisiensi | Supervisor dan toolpusher | Sebelum keputusan POOH atau ganti bit | Riwayat blok `high_MSE`, kedalaman, TVD, tren MSE/DS ([Eb] baris 156-158) | Daftar jendela yang layak dinilai, tanpa rekomendasi otomatis | Aturan MSE/DS punya rujukan terverifikasi ([A1-7] baris 59); efek operasional belum diuji |

---

## 8. Kelas `stuck`

**Vonis.** V6 GAGAL dengan mayoritas satu suara ([PM7] baris 44; [R1] baris 22). V8
menempatkannya pada tier triage atau inspeksi manual terbantu untuk sumur mirip F-10, ditambah
riset ranking onset dan deteksi status lewat persistence ([Es] baris 228-230).

**Angka kapabilitas.**
- E3 RF: lift 4/4 di atas 1, yaitu 1,65 / 1,30 / 9,72 / 1,12, CI95 signifikan hanya 1/4
  ([Es] baris 113-114; [M1] baris 53).
- E1 rule: P 0,457 di F-10, T_lead median 10 menit, FP 25 berbanding E2 197 ([Es] baris 88, 131).
- E2 statistik: lift 0,80 sampai 1,24, CI memuat prevalensi di semua fold ([Es] baris 113-115).
- B1 maksimum 31,8 persen di E2 F-10, bar tren 50 persen, bar alarm 80 persen ([Es] baris 129).
- FAR 9,9 sampai 1.440 per 24 jam negatif; angka 1.440 berasal dari E3 RF LOWO F-14 ke F-9_A
  ([Es] baris 100, 103; [A1-8] baris 46).
- Kontrol-positif 0/10 event `bha_stuck_fishing` F-14 punya onset dalam jendela plus minus 30
  menit ([Es] baris 132).
- Fold F-12 belum terukur karena STUCK_RT hanya ada di log berindeks measured depth
  ([Es] baris 239-245).
- Prareg terkunci sebelum metrik dihitung, C4 penuh ([Es] baris 6, 180).

**Batas.** Bukan alarm otomatis: B1 di bawah 32 persen dan FAR jauh di atas 1. Bukan pemantauan
tren otomatis pada ambang prareg, karena FAR semua fold di atas 6. Ambang tidak transfer lintas
sumur, q95 jenuh 1,0 atau 0,0 ([Es] baris 151-153). Validitas label adalah titik rapuh utama
([Es] baris 182).

**Fitur.**

| Fitur | Pengguna | Momen pakai | Masukan | Keluaran | Status bukti |
|---|---|---|---|---|---|
| T-1 Daftar triage onset per shift | Night shift engineer dan toolpusher | Awal shift dan setiap dua jam | Skor ranking E3, rule E1 2-dari-3, FAR terukur per fold | Daftar jam berisiko urut, SK 46, badge FAR 9,9 sampai 1.440 pada skala aslinya | Ranking layak dengan bukti sedang-rendah; alarm tidak layak ([Es] baris 198-199, 226) |
| T-2 Kartu keselarasan kontrol-positif | Engineer PdM dan auditor internal | Sebelum memakai label onset di sumur baru | 10 event `bha_stuck_fishing` F-14, onset instrumen, selisih zona waktu | Rasio 0/10 dan tiga hipotesis penyebab yang bisa diuji ([Es] baris 173-177) | Angka 0/10 terverifikasi; penyebab belum terverifikasi |
| T-3 Formulir kalibrasi ambang OOS | Engineer PdM | Sebelum menetapkan ambang di sumur baru | q95 latih per sumur, distribusi skor validasi | Peringatan jenuh (1,0 atau 0,0) dan usulan ambang pengganti untuk pra-reg baru | Bukti jenuh terukur di dua arah LOWO ([Es] baris 151-153) |

**Catatan.** T-3 tepat menjadi fitur, bukan keluhan: ambang prareg yang jenuh adalah informasi
operasional yang harus muncul sebelum orang memakai ambang itu.

---

## 9. Kelas `hyd`

**Vonis.** V6 GAGAL ([PM7] baris 45). V8 memisahkan dua klaim: K-i deteksi kondisi dengan
persistence sebagai engine terbaik, K-ii prediksi onset kick atau loss dengan hybrid plus fitur
aliran. K-i tier tren dan konfirmasi kejadian, K-ii tier indikasi dini bertingkat menit
([M1] baris 54; [Eh] baris 176-199).

**Angka kapabilitas.**
- K-i persistence: P 0,615-0,793, R 0,617-0,764, FAR_t 38,8-110,7 per 24 jam negatif, B1
  31,6-65,4 persen, delay median 0-3 menit ([Eh] baris 76).
- K-i delta B RF minus persistence negatif di 7/7 fold, kemampuan negatif terukur ([Eh] baris 62).
- CI95 persistence dan RF tidak tumpang tindih di 5/7 fold, bukan 6/7; F-5 dan F-9 yang
  tumpang tindih ([A1-8] baris 43; [PM8] baris 102).
- K-i uji kejadian nyata: pos_frac 0,884 saat episode loss, 7,4 kali base rate, tetapi peringatan
  sebelum onset 0/1 episode ([Eh] baris 125-127).
- Beban pemeriksaan nyata pada skala blok: 0,16 sampai 4,7 onset per hari, blok median 3,5 sampai
  10 menit ([Eh] baris 161-171).
- Coverage sensor SPPA dan TFLO 94,0-98,7 persen ([Eh] baris 157).
- K-ii: AUPRC test 0,228 dengan CI95 0,009 sampai 0,629, lift titik 61,6, T_lead median 7 menit,
  B1 66,7 persen atau 2 dari 3, FAR alarm 5,9 dan monitoring 25,9 ([Eh] baris 101, 141).
- K-ii onset test hanya 3, UNDERPOWERED, dan hanya 1 wellbore ([Eh] baris 95, 196).

**Batas.** Bukan alarm. K-i bukan peringatan dini. K-ii bukan generalisasi lintas sumur. Klaim
kausalitas tidak dibuat karena n=1 episode ([Eh] baris 134). ML atau RF dilarang dipakai untuk
K-i karena delta B negatif 7/7 ([Eh] baris 186-187).

**Fitur.**

| Fitur | Pengguna | Momen pakai | Masukan | Keluaran | Status bukti |
|---|---|---|---|---|---|
| H-1 Indikator status hidrolik | Mudlogger dan driller | Saat tekanan atau flow mencurigakan | Residu SPPA terhadap median dan MAD per bin TFLO, status jendela sebelumnya | Status dan SK 61, coverage sensor, jumlah blok per hari | Kuat: 7/7 fold konsisten, CI 5/7 tidak tumpang tindih ([Eh] baris 62, 179) |
| H-2 Kartu ketidakpastian kick atau loss | Engineer well control | Sebelum menaikkan level kewaspadaan | Probabilitas hybrid plus fitur aliran, CI95, jumlah onset test | SK 51, label UNDERPOWERED wajib tampil, T_lead median 7 menit | Sedang-lemah: CI sangat lebar, 1 wellbore, 3 onset test ([Eh] baris 191-193) |
| H-3 Penghitung beban pemeriksaan blok per hari | Supervisor dan engineer PdM | Perencanaan inspeksi harian | Onset blok per hari per sumur: 0,263 / 1,479 / 0,996 / 0,156 / 1,752 / 1,764 / 4,707 ([Eh] baris 161-169) | Beban blok harian per sumur, durasi median dan p90 | Angka terukur. Ini pengganti jujur untuk B3 yang belum terukur ([Eh] baris 228-229) |

---

## 10. Kelas `shk`

**Vonis.** V6 GAGAL dengan G2 6/7 lolos, artinya sinyal ada dan yang kurang adalah jumlah positif
([PM7] baris 42; [R1] baris 99). V8 menempatkannya pada tier screening berbiaya cek tinggi
ditambah peringatan situasional pada wellbore terkalibrasi lokal ([M1] baris 55).

**Angka kapabilitas.**
- Lead 2 sampai 9 menit sebelum onset pada tau 0,05, median global 5,0 menit, terdeteksi di 7
  dari 9 fold ([Ek] baris 82).
- B1 atau cakupan onset 0 sampai 0,348; artinya 65 sampai 100 persen onset tanpa peringatan pada
  ambang itu ([Ek] baris 82).
- RF >= persistence pada B1 di 9/9 fold, tetapi 4 di antaranya seri, sehingga "menambah nilai"
  ketat hanya 4/9 ([A1-8] baris 53; [PM8] baris 109-111).
- FAR <= 6 per 24 jam dengan recall > 0 tercapai di 4 titik: F-14 tau 0,20 dengan P 0,26 dan
  FAR 4,8; F-14 tau 0,30; F-5 tau 0,30 dengan P 0,32; F-9 tau 0,50 dengan P 0,55 ([Ek] baris 60).
- FAR <= 1 dengan recall > 0 hanya 1 titik di seluruh grid: F-14 tau 0,30, FAR 0,69, recall 0,92
  persen, tidak operasional ([A1-8] baris 45; [PM8] baris 104).
- B3 NEGATIF: pengurangan pemeriksaan -0,11 sampai -53,75 pada tau <= 0,20, positif hanya pada
  tau >= 0,30 ([Ek] baris 84).
- Positif per wellbore: F-10 798 dengan prev 0,27 persen, F-12 580 dengan prev 1,59 persen, F-4 50,
  F-15 13, F-15B 0 ([PM7] baris 141).
- Lift lintas well F-10 dan F-12 hanya 0,96 dan 1,06, kalah canary, sehingga sinyal bersifat lokal
  wellbore ([M1] baris 55).
- Reproduksi V6 7/7 di bawah 1e-9 ([M1] baris 55).

**Batas.** Bukan alarm otomatis: tidak ada titik dengan FAR <= 1 dan recall operasional. Kalibrasi
ambang tidak transfer lintas wellbore. Pemakaian buta lintas regime dilarang. Pengurangan
pemeriksaan tidak boleh diklaim, karena B3 negatif.

**Fitur.**

| Fitur | Pengguna | Momen pakai | Masukan | Keluaran | Status bukti |
|---|---|---|---|---|---|
| K-1 Panel titik operasi hemat-awas | Driller dan supervisor | Sebelum memilih tingkat kepekaan alarm | Empat titik FAR <= 6 beserta P dan R, tau terpilih | SK 52, badge FAR pada skala asli per 24 jam, cakupan onset yang dikorbankan | A dan B sedang-kuat, 9 fold nyata, prareg ([M1] baris 55) |
| K-2 Penggeser tau dengan tampilan biaya cek | Engineer PdM | Saat menyetel kepekaan per sumur | Kurva tau 0,05 sampai 0,30, FP engine, FP display | Grafik trade-off, angka B3 negatif -0,11 sampai -53,75 ditampilkan terang | Terukur dan negatif; fitur ini menampilkan kerugian, bukan menyembunyikannya ([Ek] baris 84) |
| K-3 Kartu kesiapan jumlah positif per sumur | Engineer PdM | Sebelum memakai K-1 di sumur baru | Jumlah positif per wellbore: 798 / 580 / 50 / 13 / 0 ([PM7] baris 141) | Status siap atau tidak, saran sumur yang layak dipakai | Angka terverifikasi; ambang kelayakan 30 positif adalah konvensi prareg ([A1-7] baris 100) |

---

## 11. Kelas `tool_wear`

**Vonis.** V6 GAGAL, G1 0/4 ([R1] baris 160). V8 menempatkannya pada tier skor dan indikasi tren
keausan ditambah detektor perubahan regime dalam-run, domain bengkel, terpisah dari alat Volve
([M1] baris 56; [PM8] baris 308).

**Angka kapabilitas.**
- AUPRC T01 sampai T04: 0,5433 / 0,7684 / 0,7031 / 0,6497; precision 0,516 / 0,559 / 0,509 /
  0,500 ([A1-8] baris 68; [Ew] baris 53).
- Lift 1,09 sampai 1,42, lift >= 1,5 di 0/4 fold, G1 0/4 ([Ew] baris 120).
- Delta B terhadap canary positif 4/4 dengan rentang +0,027 sampai +0,174 ([M1] baris 56).
- Precision median 0,512, recall median 0,983, FAR 46,0 sampai 60,0 per menit ([Ew] baris 58;
  [A1-8] baris 68).
- T_lead median engine (ii) 47,0 detik dengan rentang 35-59, dikoreksi dari 47,5 di dokumen
  sumber ([A1-8] baris 48, 118).
- T_lead median engine (i) 24,5 detik dengan rentang 20-36, dikoreksi dari 30
  ([A1-8] baris 47, 118).
- Change-point signifikan 8/8 run termasuk 8/8 run alat baru, sehingga spesifisitas keausan gagal,
  precision run 0,50, artefak termal 0/8 ([Ew] baris 74, 146).
- C3 dropout 1 kanal di bawah 20 persen atau robust, 2 kanal marginal 26,2 persen
  ([M1] baris 56).

**Batas.** Bukan alarm kritis: precision mendekati peluang. Klaim onset progresi keausan tidak
dibuat karena spesifisitas gagal. Transfer ke rig drilling tidak diklaim, tidak ada data. Waktu
dalam detik bengkel, tidak dijumlahkan dengan menit rig ([M1] baris 56, 86).

**Fitur.**

| Fitur | Pengguna | Momen pakai | Masukan | Keluaran | Status bukti |
|---|---|---|---|---|---|
| W-1 Skor LOTO lintas-alat | Teknisi bengkel dan perencana perawatan | Sebelum alat dipasang pada run berikutnya | Spektrum akselerometer per run, AUPRC 0,543-0,768, model LOTO | Ranking alat berisiko, SK 46, catatan "precision mendekati peluang" | Sedang: 4/4 fold menang tetapi 4 alat dan ada confound urutan run ([M1] baris 56) |
| W-2 Detektor perubahan regime dalam-run | Teknisi bengkel dan supervisor | Selama run berjalan, saat ada kecurigaan | Deret fitur kurtosis, crest, frekuensi dominan per jendela pendek | Penanda "saat ini berbeda dari awal run", pemicu inspeksi, T_lead median 47,0 detik | Change-point 8/8 run; untuk klaim keausan statusnya terduga lemah ([Ew] baris 146) |
| W-3 Kalkulator plafon lift | Engineer PdM dan auditor | Saat menilai apakah G1 realistis | Prevalensi fold, plafon 1/prev, misal F-15S prev 0,544 memberi plafon 1,84 ([Eb] baris 91-95) | Angka plafon per fold dan putusan "ambang 1,5 tidak tercapai secara matematis" | Terverifikasi sebagai aritmetika; dipakai sebagai konteks, bukan penurunan ambang |

---

## 12. Fitur lintas kelas: satu grid, empat lapis

V8 sudah menetapkan arsitektur yang boleh dipakai apa adanya ([M1] baris 117-134; [PM8] baris
282-304). Inventaris ini hanya menerjemahkannya menjadi daftar fitur yang bisa dibangun.

| Lapis | Isi | Status |
|---|---|---|
| LAYER-0 konfirmasi status otomatis | rule VIBLAT >= 32,17; rule SSI >= 1; rule display shock; persistence hyd 0,615-0,793; bit_wear 0,679-0,984; stuck 0,787 dari V6 | Terbukti, tanpa ML ([PM8] baris 283-287) |
| LAYER-1 peringatan human-in-loop | shk RF lead 2-9 menit; stuck E1 triage P 0,457 lead 10 menit; hyd K-ii lead 7 menit; vib dan ssi bersyarat | 3 terbukti + 2 bersyarat ([PM8] baris 289-294) |
| LAYER-2 tren dan skor | vib RF, ssi RF, bit_wear persistence plus RF screening, tool_wear LOTO score, stuck E3 ranking, hyd persistence trend | 5 sampai 6 engine ([PM8] baris 296-298) |
| LAYER-3 keputusan manusia | semua kelas | Semua kelas hari ini ([PM8] baris 300-301) |
| Alarm otomatis kritis | 0 slot | 0/7 engine ([PM8] baris 303; [L] baris 2024, PM-078) |

Satu keputusan arsitektur yang mengikat fitur: onset layer memakai grid, feature store, dan
harness kalibrasi bersama, tetapi head prediktor TERPISAH per kelas; hybrid berarti infrastruktur
bersama, bukan bobot bersama ([M1] baris 96-99).

---

## 13. Syarat yang dibutuhkan (menggantikan kalimat penutup)

Yang belum tersedia hari ini, beserta syarat konkret agar fitur terkait bisa naik tingkat:

1. Untuk `vib` dan `ssi` naik ke peringatan penuh: ukur FAR_t dan B4 di kampanye penguatan, yaitu
   parse VIBLAT F-4, F-10, F-15 dan re-run S-E1 11 fold ([PM8] baris 331-332; [M1] baris 157-159).
2. Untuk `bit_wear` K-2: jalankan kampanye pra-reg onset memakai 481 kandidat dan 329 transisi
   dari normal, sekaligus menghitung persistence-onset sebagai tes pembeda ([Eb] baris 201-207).
3. Untuk `stuck` naik dari triage: sinkronkan kontrol-positif dengan zona waktu yang benar,
   dokumentasikan semantik STUCK_RT 0 sampai 3 lintas wellbore, dan selesaikan join kedalaman ke
   waktu untuk F-12 ([Es] baris 239-245, 173-177; [PM8] baris 334-336).
4. Untuk `hyd` K-ii lintas sumur: parse GAINLOSSTOT F-1C dan F-11 agar fold tambahan terbentuk
   ([Eh] baris 196-199).
5. Untuk B3 di semua kelas: definisikan baseline aturan operasional dan kumpulkan data beban kerja
   rig, yang tidak ada di Volve ([M1] baris 194). Fitur V-3 dan H-3 adalah jalur pengumpulannya.
6. Untuk C3 pada lima engine yang belum diuji: jalankan uji dropout kanal SHAP-atas dan noise
   sigma per 10, paket murah tanpa data baru ([M1] baris 197).
7. Untuk SK dipakai sebagai ambang: bekukan pemetaan S_A, S_B, S_C sebagai pra-registrasi lebih
   dulu, lalu uji daya pisahnya. Sampai itu terjadi, SK hanya ditampilkan sebagai angka pendamping.

---

## 14. Yang belum diverifikasi

1. Skor keyakinan SK adalah usulan desain. Aritmetikanya sudah diperiksa, daya pisahnya belum.
2. Angka `vib`, `ssi`, `shk`, `tool_wear` di dokumen ini dikutip dari profil kelas masing-masing
   dan dari [M1] dan [A1-8]. Dokumen ini tidak menghitung ulang ke artefak JSON primer; yang
   menghitung ulang adalah [A1-8] dengan 121 klaim dan 45 sel tabel.
3. Enam selisih penyajian V8 (hyd 5/7 bukan 6/7, shk 5/9 bukan 4/9, shk satu titik FAR <= 1,
   shk 4/9 ketat bukan 9/9, stuck 1.440 bukan 185, tool_wear 24,5 dan 47,0) dilaporkan sebagai
   koreksi yang SUDAH diadjudikasi di [PM8] baris 100-116. Dokumen sumbernya belum dipatch pada
   saat inventaris ini ditulis, sehingga pengutipan langsung dari dokumen sumber masih berisiko
   membawa angka lama.
4. Terdapat ketidakkonsistenan basis hitung onset `stuck` antara angka prareg evaluator (F-9_A 72
   ffill dan 62 strict) dan angka PM V7 (74 dan 34). Keduanya dinyatakan terbuka di [Es] baris
   278-280 dan [PM7] baris 137. Dokumen ini memakai angka PM V7 untuk keperluan inventaris dan
   menandai bahwa definisi wajib dikunci sebelum kampanye.
5. Angka beban parse dan peluang sukses di [PM7] baris 255-259 adalah estimasi, bukan hasil ukur.
6. Dua pelanggaran prosedural tercatat dan tidak mempengaruhi angka: deklarasi sequ-mcp yang
   tidak ada di dokumen shk, dan tidak ada jejak log di dokumen A1 ([PM8] baris 79-85).
7. Fitur V-2, S-2, T-2, K-3, dan W-3 memakai angka yang terverifikasi, tetapi keputusan tampilan
   (misalnya kapan panel dinonaktifkan) adalah usulan desain yang belum diuji dengan pengguna.

---

## 15. Bukti perintah (keluaran apa adanya)

### 15.A Ukuran berkas masukan

```
$ wc -c -l docs/V7_PM_VERDICT.md docs/V7_R1_SOLUTIONS.md docs/V7_A1_SOLUTION_AUDIT.md \
  docs/V8_PM_VERDICT.md docs/V8_M1_CAPABILITY_MAP.md docs/V8_A1_CAPABILITY_AUDIT.md \
  docs/V8_E_hyd_CAPABILITY.md docs/V8_E_stuck_CAPABILITY.md docs/V8_E_bit_wear_CAPABILITY.md
   286  23569 docs/V7_PM_VERDICT.md
   270  34950 docs/V7_R1_SOLUTIONS.md
   232  17731 docs/V7_A1_SOLUTION_AUDIT.md
   364  23720 docs/V8_PM_VERDICT.md
   229  23716 docs/V8_M1_CAPABILITY_MAP.md
   118  14818 docs/V8_A1_CAPABILITY_AUDIT.md
   231  16345 docs/V8_E_hyd_CAPABILITY.md
   293  22172 docs/V8_E_stuck_CAPABILITY.md
   225  16116 docs/V8_E_bit_wear_CAPABILITY.md
  2248 193137 total
```

### 15.B Pemeriksaan angka kunci per kelas

```
--- vib ---
52:- Gate V6: **G1 4/4** (lift 1,61-3,50, semua ≥1,5) · **G2 4/4** (RF ≥ canary tiap fold)
69:| lift (vs prevalensi fold) | 1,61 / 2,36 / 3,50 / 1,63 - **4/4 > 1,5** | OBSERVED |
--- ssi ---
58:| AUPRC + lift | 0,0185-0,1057; lift 2,61-6,64 (5 fold layak); lift ≥1,5 di **4/5** (G1)
--- bit_wear 0,679 ---
40:2. RF TIDAK menambah di atas rule persistence di **4/4 fold** (ΔB_vs_persistence −0,087…−0,381)
66:| F-14 | 949 / 91 / 0,0959 | **0,298** [0,148; 0,517] | 3,11 | 10,43 | 0,191 | 0,679 | 0,863 |
--- stuck 1.440 ---
docs/V8_E_stuck_CAPABILITY.md:100:| LOWO 14→9A | E3_RF | 0,224 | 72/72 = 100%† | 1.440 | 0,251 (1,12) | [0,185; 0,347] | 10 [8; 10] |
docs/V8_E_stuck_CAPABILITY.md:226:| **Alarm kritis otomatis** | **BELUM** | B1 ≤31,8% (butuh ≥80%); FAR 9,9-1.440 (butuh ≤1) |
--- hyd 0,615 ---
76:| **persistence (biner)** | **0,615-0,793** | **0,617-0,764** | **38,8-110,7** | B1 (≤10 mnt): **31,6-65,4%**
126:| Selama episode (per hari) | 2008-11-15: **pos_frac 0,884** (n=199); 11-16: 0,054
--- shk ---
104:| 3 | shk: "FAR≤1 dgn recall>0 **TIDAK tercapai di fold mana pun / 0 dari 9 fold**" | **1 titik**: F-14 tau0,30 → FAR 0,69/24j, recall **0,92%**
180:| **LAYAK alarm otomatis kritis** | **0 / 7** | - (syarat R1 §4 ... shk titik terdekat recall 0,92%)
--- tool_wear 47,0 / 24,5 ---
47:| 5 | tool_wear "T_lead median **30 dtk** (20-36)" | t_lead = 20, 24, 25, 36 dtk | **BERLEIH - median salah** | Median aktual = **24,5 dtk**
48:| 6 | tool_wear "T_lead median **47,5 dtk** (35-59)" | t_lead = 35, 41, 53, 59 dtk | **SLIP KECIL** | Median aktual = **47,0 dtk**
```

Catatan kejujuran kutipan: cuplikan di atas berasal dari keluaran `grep` atas berkas sumber.
Berkas sumber memakai tanda pisah panjang dan tanda pisah sedang di dalam barisnya. Agar dokumen
ini patuh aturan 8, kedua karakter itu dinormalkan menjadi tanda hubung biasa di dalam kutipan.
Tidak ada angka, tanda desimal, atau kata yang diubah selain karakter pisah tersebut.

### 15.C Positif shk per wellbore

```
$ grep -n "798" docs/V7_PM_VERDICT.md
141:| 7 | Positif shk wellbore baru | R1: est. 100-200/well | M2 (recount D1e): F-10 798 (0,27%), F-12 580 (1,59%), F-4 50, F-15 13, F-15B 0 |
```

### 15.D tool_wear G1 0/4 dan lift

```
$ grep -n "G1 0/4\|1,09" docs/V8_M1_CAPABILITY_MAP.md
56:| **tool_wear** | ... K-ii: AUPRC 0,543-0,768, ΔB vs canary **4/4 positif** (+0,027…+0,174),
    lift 1,09-1,42 (G1 0/4, plafon 2,0); precision biner 0,50-0,56 ≈ peluang
```

### 15.E Baris ledger yang dipakai

```
$ grep -n "^| L-26 \|^| PM-078 \|^| E2-008 " docs/RND_PROVENANCE_LEDGER.md
56:| L-26 | FAR <= 6 | alarm palsu per 24 jam | KONVENSI | ... | gerbang tier LAYER-1 | BELUM |
1527:| E2-008 | 12 / 13 / 2 / 0 | head per tier (PERINGATAN / TREN / BELUM LAYAK / ALARM-OTOMATIS)
2024:| PM-078 | 0 | slot | KONVENSI | scratch/v9_i1/v9_i1_RESULTS.json auto_critical_alarm_slots | TERUKUR |
```

### 15.F Keberadaan empat profil kelas yang tidak masuk daftar masukan

```
$ ls -l docs/V8_E_*_CAPABILITY.md
-rwxrwxrwx 1 neonti neonti 16116 Oct 11 17:02 docs/V8_E_bit_wear_CAPABILITY.md
-rwxrwxrwx 1 neonti neonti 16345 Oct 11 18:23 docs/V8_E_hyd_CAPABILITY.md
-rwxrwxrwx 1 neonti neonti 17176 Oct 11 21:12 docs/V8_E_shk_CAPABILITY.md
-rwxrwxrwx 1 neonti neonti 12678 Oct 11 16:59 docs/V8_E_ssi_CAPABILITY.md
-rwxrwxrwx 1 neonti neonti 22172 Oct 11 21:27 docs/V8_E_stuck_CAPABILITY.md
-rwxrwxrwx 1 neonti neonti 11876 Oct 11 17:21 docs/V8_E_tool_wear_CAPABILITY.md
-rwxrwxrwx 1 neonti neonti 13970 Oct 11 16:58 docs/V8_E_vib_CAPABILITY.md
```

---

## 16. Daftar sumber

Berkas masukan kartu: `docs/V7_PM_VERDICT.md`, `docs/V7_R1_SOLUTIONS.md`,
`docs/V7_A1_SOLUTION_AUDIT.md`, `docs/V8_PM_VERDICT.md`, `docs/V8_M1_CAPABILITY_MAP.md`,
`docs/V8_A1_CAPABILITY_AUDIT.md`, `docs/V8_E_hyd_CAPABILITY.md`, `docs/V8_E_stuck_CAPABILITY.md`,
`docs/V8_E_bit_wear_CAPABILITY.md`.
Berkas pendukung angka, dengan ukuran tercatat di bagian 1: `docs/V8_E_vib_CAPABILITY.md`,
`docs/V8_E_ssi_CAPABILITY.md`, `docs/V8_E_shk_CAPABILITY.md`,
`docs/V8_E_tool_wear_CAPABILITY.md`, `docs/RND_PROVENANCE_LEDGER.md`.

Semua jalur relatif terhadap `/mnt/d/Capstone 1(v2)/`.
