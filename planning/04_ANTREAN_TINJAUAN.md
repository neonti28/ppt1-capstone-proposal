# 04 SPESIFIKASI ANTREAN TINJAUAN DAN ANGGARAN WAKTU (DSS-2)

Kartu: `t_58a80eea` (DSS-2). Board: `fitur-v9-swarm`. Tanggal: 2026-10-31 (WIB).
Workspace: `/mnt/d/Capstone 1(v2)`. Keluaran: berkas ini saja, di folder `planning/`.

Dokumen ini menetapkan satu antrean tinjauan untuk satu shift: baris apa yang layak dilihat manusia,
dalam urutan apa, dengan alasan apa, dan berapa menit yang dihabiskan. Isinya: muatan baris, aturan
urutan berlapis, aturan anggaran waktu dengan neraca penundaan, sepuluh baris contoh yang angkanya
diturunkan dari berkas yang sudah ada, tiga keadaan antrean, saran penyajian, dan tujuh fitur dengan
format lengkap. Tidak ada model yang dijalankan ulang di sini. Keputusan akhir tetap milik manusia,
dan dokumen ini tidak menambah satu pun jalur alarm otomatis.

Riset pendahuluan: `mcp__sequentialthinking__sequentialthinking`, lima pikiran (thoughtNumber 1
sampai 5, thoughtHistoryLength 5). Ringkas: (1) memisahkan yang sudah terukur (volume antrean per
shift dari simulasi Poisson di berkas [H]) dari yang belum (menit per pemeriksaan, log keputusan,
peta sumur per jendela), (2) menemukan tiga tabrakan angka di sumber (penghitungan ganda rule dan
hibrida, satuan FAR tool_wear per menit, pembulatan ke atas) dan menetapkan cara menyelesaikannya,
(3) memilih jalan penurunan status kepala per jendela yang tidak menebak, yaitu memakai daftar
`contoh_idx_aktif` ditambah definisi hibrida dari [J], (4) menguji anggaran 30 menit terhadap beban
40,15 baris per shift dengan jangkar EEMUA 191, (5) menetapkan apa yang harus ditulis sebagai
parameter dan apa yang harus ditulis sebagai syarat.

Notasi. Keluaran perintah di dokumen ini memakai titik desimal (format `python3` dan `awk`),
sedangkan teks memakai koma desimal mengikuti gaya dokumen proyek lain. Keduanya angka yang sama.
Pengenal jendela adalah indeks posisi di dalam segmen, bukan tanggal. [J] baris 22 menulis bahwa
`ts_bin` adalah indeks menit internal D1 dan asal kalender belum diverifikasi, jadi tidak satu pun
baris di dokumen ini boleh dibaca sebagai tanggal.

## 0. Kepatuhan kerangka wajib

| Butir kerangka | Cara dipenuhi di dokumen ini |
|---|---|
| 1. Alarm otomatis bukan tujuan | Seluruh antrean berhenti di papan tinjauan manusia. [J] baris 1414 menulis `auto_critical_alarm_slots` = 0 dan baris 1415 menulis keputusan akhir MANUSIA. Tidak ada tombol kirim alarm, dan pita tertinggi pada antrean hanya berbunyi "konfirmasi lapangan", bukan "tindakan otomatis". |
| 2. Setiap angka bersumber | Setiap angka proyek memakai kode berkas [J], [H], [K], [VR], [S6], [ENG], [DSS1], [P] beserta nomor baris, atau baris ledger [L]. Angka literatur memakai kode LV4, LV6, LV7, LV14 dari [VR] bagian 9, ditambah LV17 sampai LV19 yang daftarnya ada di bagian 8.4 dan tidak ada di daftar [VR]. |
| 3. Tidak ada klaim tanpa bukti | Bagian 1 memuat ukuran byte tiap berkas yang dibuka. Bagian 14 menempelkan keluaran perintah yang dipakai memeriksa angka dan memeriksa berkas ini. |
| 4. Kekurangan data jadi fitur | Peta sumur yang belum ada menjadi kolom "segmen" dengan label wajib, bukan kolom kosong. Status kepala yang belum bisa dipastikan menjadi penanda interval `K_min` sampai `K_up` (fitur ANT-07), bukan angka nol. Kanal absen pada ssi menjadi label AB-2 pada baris, bukan baris yang dihapus. |
| 5. Lima field wajib per fitur | Setiap fitur di bagian 9 memuat pengguna, momen pakai, masukan, keluaran, dan status bukti, ditambah delapan field lain sesuai format kartu. |
| 6. Tidak menutup dengan kalimat menyerah | Bagian 12 menuliskan syarat yang dibutuhkan beserta pemilik datanya, dan bagian 13 memisahkan yang belum diverifikasi dari yang sudah. |
| 7. Hanya markdown di `planning/` | Satu berkas keluaran, yaitu berkas ini. Skrip pemeriksa sementara ditulis di luar `planning/` dan bukan deliverable; keluarannya ditempel di bagian 14. |
| 8. Tanpa tanda pisah panjang | Diperiksa pada bagian 14 dengan `grep`, keluarannya 0. |

## 1. Berkas masukan, ukuran byte, dan cara dibuka

Ukuran diambil dengan `stat -c '%s'` dan `wc -l` pada 2026-10-31. Keluaran mentahnya ada di
bagian 14.1.

| Kode | Berkas | Byte | Baris | Cara dibuka di sesi ini |
|---|---|---:|---:|---|
| [J] | `scratch/v9_i1/v9_i1_RESULTS.json` | 57.555 | 1.759 | dibaca penuh lewat pengurai JSON, lalu baris tertentu dibaca langsung |
| [H] | `dashboard/data/head_pages.json` | 456.685 | 31.946 | dibaca penuh lewat pengurai JSON, lalu baris tertentu dibaca langsung |
| [K] | `planning/01_KATALOG_FITUR.md` | 166.662 | 2.780 | dibaca sebagian: baris 121, 125, 136 sampai 175, 871 sampai 1010, 1099 sampai 1129 |
| [VR] | `planning/02_RISET_VISUALISASI.md` | 32.141 | 335 | dibaca sebagian: baris 10 sampai 13, 44 sampai 54, 115 sampai 148, 165 sampai 175, 234 sampai 268, 280 sampai 300 |
| [S6] | `docs/RND_S6_PM_WAVE2.md` | 40.271 | 437 | dibaca sebagian: baris 26 sampai 36, 80 sampai 160, 178 sampai 235, 250 sampai 260, 332 sampai 360, 400 sampai 420 |
| [ENG] | `docs/RND_ENGINE_S6_INTEGRATION.md` | 3.915 | 76 | dibaca penuh |
| [DSS1] | `planning/03_SKOR_KEYAKINAN.md` | 66.698 | 1.060 | dibaca sebagian: baris 12 sampai 27, 83 sampai 260, 869 sampai 1000, 1032 sampai 1060 |
| [P] | `code/v9_i1_pipeline.py` | 44.359 | 861 | dibaca sebagian: baris 360 sampai 402 |
| [L] | `docs/RND_PROVENANCE_LEDGER.md` | 471.945 | 3.434 | dibaca sebagian lewat pencarian: baris 61, 62, 64, 1106, 1155, 1767, 3292, 3433, dan 3425 sampai 3445 |

Berkas yang dipakai sebagai sumber angka dan bukan sebagai masukan [J] dicatat apa adanya: [H] adalah
turunan [J] yang menambah simulasi per shift, jadi dua berkas ini tidak boleh dibaca sebagai dua
pengukuran berbeda.

## 2. Angka yang mengikat: FAR, lead time, dan beban per shift

### 2.1 FAR dan lead per komposisi hyd

Fuel Anggaran Risiko yang dipakai dokumen ini adalah FAR per 24 jam kalender, karena satuan inilah
yang bisa dibagi ke panjang shift. [S6] baris 189 sampai 197 memuat tujuh komposisi dengan angka
lengkap, dan empat di antaranya yang paling penting untuk antrean:

| Komposisi | FP | TP | Presisi | Recall | FAR kalender median | Lead median | Fold FAR tidak lebih 6 | Fold recall minimal 0,5 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| rule kanal | 2.105 | 5.579 | 0,6835 | 0,7507 | 6,9320 | 6,0 menit | 3 | 9 |
| H1 stat DAN rule | 935 | 3.804 | 0,7789 | 0,5638 | 3,5302 | 11,5 menit | 7 | 6 |
| H1p rule DAN persistence | 927 | 4.924 | 0,8243 | 0,6519 | 4,0984 | 8,0 menit | 7 | 9 |
| H1p3 rule DAN persistence DAN stat | 568 | 3.557 | 0,8646 | 0,5296 | 2,0323 | 12,5 menit | 9 | 5 |

Sumber tiap sel: [S6] baris 191 sampai 197. Angka FAR 4,0984 juga tercatat di ledger [L] baris 3292
(S6-058) dengan satuan "alarm per 24 jam kalender" dan kelas sumber RUN-KITA. Lead 8,0 menit untuk
H1p tercatat di [L] baris 3436 (E5-007) dengan menit sebagai satuan.

### 2.2 FAR per head dan beban tinjauan per shift

[J] menyimpan FAR per segmen untuk tiap head, dan [ENG] baris 29 sampai 43 menerjemahkannya menjadi
tinjauan per shift 8 jam dengan membagi tiga. Pembagian tiga itu bisa diperiksa ulang: 24 jam dibagi
tiga sama dengan satu shift 8 jam, dan pembulatannya ke atas. Keluaran pemeriksaan ada di bagian 14.2.

| Mesin | Head | FAR per 24 jam | Tinjauan per shift 8 jam | Sumber |
|---|---|---:|---:|---|
| vib | `rule_display` | 49,942 | 17 | [J] baris 95 dan 77; [ENG] baris 33 |
| vib | `hybrid_rule_and_persistence` | 49,942 | 17 | [J] baris 163; [ENG] baris 34 |
| ssi | `rule_display` | 0,0 | 0 | [J] baris 244 dan 232; [ENG] baris 35 |
| ssi | `hybrid_rule_and_persistence` | 0,0 | 0 | [J] baris 306; [ENG] baris 36 |
| shk | `rule_display` | 6,618 | 3 | [J] baris 387 dan 369; [ENG] baris 37 |
| shk | `hybrid_rule_and_persistence` | 6,618 | 3 | [J] baris 455; [ENG] baris 38 |
| stuck | `rule_display` | 8,321 | 3 | [J] baris 536 dan 518; [ENG] baris 39 |
| stuck | `hybrid_rule_and_persistence` | 8,321 | 3 | [J] baris 604; [ENG] baris 40 |
| hyd | `rule_display` | 55,570 | 19 | [J] baris 759 dan 741; [ENG] baris 41 |
| hyd | `hybrid_rule_and_persistence` | 16,611 | 6 | [J] baris 830 dan 812; [ENG] baris 42; [L] baris 3433 (E5-008) |
| tool_wear | `op_far_calibrated` | 2,096 | 1 | [J] baris 1076 dan 1058; [ENG] baris 43 |

### 2.3 Tiga tabrakan angka yang diselesaikan di sini

Ketiganya nyata dan bisa diperiksa. Menyembunyikannya akan membuat antrean menghitung volume yang
salah.

**Tabrakan pertama, penghitungan ganda rule dan hibrida.** [ENG] baris 33 sampai 40 menulis vib rule
17 dan vib hibrida 17, begitu juga shk dan stuck. Padahal [J] baris 166, 309, 458, 607, dan 833
menulis definisi hibrida sebagai `rule(t0-1) AND persistence(t)`. Setiap alarm hibrida juga alarm
rule, dan setiap jendela hibrida ada di dalam himpunan jendela rule. Menjumlahkan keduanya
menghitung jendela yang sama dua kali. Keputusan: satu baris antrean per klaim per jendela, dengan
kepala hibrida tampil sebagai penanda di dalam baris, bukan sebagai baris kedua. Akibatnya beban vib
menjadi 17, bukan 34, dan beban hyd memakai rule 19, bukan 19 ditambah 6.

**Tabrakan kedua, satuan FAR tool_wear.** [ENG] baris 43 membagi 2,096 dengan tiga dan mendapat
1 tinjauan per shift. Ledger [L] baris 1155 (E0-022) menulis angka yang sama dengan satuan
`FP/menit`, dan [H] baris 29846 memberi simulasi Poisson untuk head yang sama dengan lambda 1006,08
per shift. Ketiganya memakai angka 2,096 tetapi dua di antaranya memakai satuan menit. Keputusan:
baris tool_wear tidak dihitung sebagai 1 per shift, karena jendela tool_wear berdurasi 1 detik dan
FAR-nya per menit. Untuk antrean shift, tool_wear masuk sebagai satu pemeriksaan bengkel per shift
dengan label satuan, dan angka 1006,08 ditampilkan sebagai konsekuensi bila dibaca sebagai kalender.
Ini bukan penyelarasan kosmetik: tanpa label satuan, satu baris dapat mewakili 1 atau 1006 tinjauan.

**Tabrakan ketiga, pembulatan.** [J] baris 1687 sampai 1753 membulatkan ke atas sehingga 2,096/3
menjadi 1, bukan 0,7. Pembulatan ke atas benar untuk perencanaan tenaga kerja, tetapi salah bila
dipakai sebagai bobot rata-rata beban. Keputusan: volume memakai bilangan bulat hasil pembulatan ke
atas (untuk tenaga kerja), sedangkan perhitungan anggaran memakai lambda tanpa pembulatan dari [H]
baris 271 dan seterusnya. Dua angka dipakai untuk dua tujuan berbeda, dan itu ditulis di layar.

### 2.4 Beban per shift dari simulasi, angka yang dipakai antrean

[H] memuat `montecarlo.alarms_per_shift` per head, dengan `n_draw` 20000, `seed` 20261029, dan basis
"Beta(tp+1, fp+1) dan Beta(tp+1, fn+1); Poisson(FAR/3) untuk satu shift 8 jam". Setelah aturan dedup
pada 2.3, baris yang benar-benar berbeda per shift adalah:

| Klaim | Head penentu | Lambda per shift | p05 | p50 | p95 | Sumber |
|---|---|---:|---:|---:|---:|---|
| vib | `rule_display` | 16,647 | 10 | 16 | 24 | [H] baris 271 |
| shk | `rule_display` | 2,206 | 0 | 2 | 5 | [H] baris 10399 |
| stuck K-i | `rule_display` | 2,774 | 0 | 3 | 6 | [H] baris 15457 |
| hyd K-i | `hybrid_rule_and_persistence` | 5,537 | 2 | 5 | 10 | [H] baris 25883 |
| hyd K-i | `rule_display` | 18,523 | 12 | 18 | 26 | [H] baris 23136 |
| tool_wear K-i | `op_far_calibrated` | 1.006,08 | 954 | 1.006 | 1.059 | [H] baris 29846, satuan per menit |

Jumlah baris berbeda per shift, dengan hyd dihitung sekali memakai `rule_display` karena hibrida
adalah himpunan bagian rule: 16,647 ditambah 2,206 ditambah 2,774 ditambah 18,523 sama dengan 40,15
baris per shift. Nilai tengah gabungan adalah 39 baris, dan nilai persentil 95 gabungan adalah 61
baris. tool_wear tidak dijumlahkan karena satuannya per menit dan diperlakukan terpisah mengikuti
2.3. Keluaran aritmetikanya ada di bagian 14.3.
## 3. Muatan baris antrean

Satu baris mewakili satu klaim pada satu jendela, bukan satu kepala dan bukan satu engine. Aturan ini
mengikuti 2.3 dan [DSS1] bagian 3.5 yang melarang menjumlahkan antar engine.

| Kolom | Isi | Satuan | Rentang hari ini | Sumber | Wajib tampil |
|---|---|---|---|---|---|
| `id_baris` | pengenal terbaca manusia, berbentuk `klaim` lalu `jendela`, contoh `hyd K-i 20` | teks | 11 klaim | [VR] baris 173 (kolom pertama harus terbaca manusia) | selalu |
| `waktu` | indeks jendela di dalam segmen, dan `ts_bin` bila tersedia | indeks menit | 0 sampai 95.924 | [J] baris 22 dan 618 | selalu |
| `segmen` | nama segmen rig, hari ini F-14 untuk seluruh baris | teks | 1 nilai | [J] baris 4 dan 54 | selalu, sampai peta sumur ada |
| `klaim` | engine dan jenis klaim, contoh `hyd K-i` atau `stuck K-ii` | kategori | 11 nilai | [J] baris 723 (K-i dan K-ii klaim terpisah) | selalu |
| `kepala_nyala` | daftar kepala yang menyala, contoh `rule, persistence, hibrida` | kategori | 0 sampai 4 kepala per klaim | [J] baris 79 sampai 83 dan 814 sampai 819 | selalu |
| `K_tampil` | keyakinan bukti 0 sampai 1 dari [DSS1] bagian 3.3 dan 3.4 | rasio | 0 sampai 0,6100 | [DSS1] baris 170 sampai 177 | selalu |
| `K_interval` | `K_min` sampai `K_up` karena status sebagian kepala belum diketahui | rasio | 0 sampai 1 sebelum dipotong | [J] `contoh_idx_aktif` per head | bila `K_up` berbeda pita dengan `K_min` |
| `pita` | P1 sampai P5 menurut [DSS1] bagian 4.1 | kategori | P1 sampai P4 hari ini | [DSS1] baris 219 sampai 225 | selalu |
| `badge_far` | FAR per 24 jam atau per menit, wajib berlabel satuan | alarm per 24 jam atau per menit | 0 sampai 1006,08 | [J] baris 95 dan 1076; aturan satuan di 2.3 | selalu |
| `lead` | perkiraan waktu menuju onset, hanya tersedia untuk hyd | menit | 8,0 | [J] baris 809 dan 1571 sampai 1577 | hanya bila ada; klaim lain diberi label "tidak tersedia" |
| `umur` | selisih indeks jendela sekarang dengan jendela pertama episode | menit (batas bawah) | 0 sampai 87 | dihitung dari `series.bins` [H] baris 421 | selalu |
| `menit` | anggaran waktu pemeriksaan baris menurut pita dan panjang episode | menit | 0 sampai 15 | bagian 5.2 | selalu |
| `alasan` | satu kalimat yang menyebut kepala mana yang menyala dan batas kelas mana yang menekan | teks | 11 pola | [J] `badge_far` dan `batas_pemakaian` per head | selalu |
| `aksi` | `konfirmasi lapangan`, `periksa kanal`, `pantau`, atau `tutup` | kategori | 4 nilai | [DSS1] kolom tindakan, baris 222 sampai 228 | selalu |

Aturan wajib yang melekat pada baris:

1. Tidak ada baris tanpa `alasan`. Baris yang alasannya kosong ditolak oleh pemeriksa tampilan, dan
   alasan pertama yang dibaca adalah alasan batas kelas, bukan alasan kepala, mengikuti [DSS1]
   baris 935 sampai 940.
2. Tidak ada baris tanpa satuan pada `badge_far`. Alasannya ada di 2.3: satu angka yang sama bisa
   berarti 1 atau 1006 tinjauan.
3. `segmen` wajib tampil selama peta sumur per jendela belum ada. [J] hanya memberi segmen per
   engine ([J] baris 19 sampai 57), bukan pemetaan jendela ke sumur. Menulis nama sumur per baris
   hari ini akan menjadi tebakan.
4. `lead` hanya diisi bila [J] menyediakannya. [J] baris 1571 sampai 1577 menulis hanya
   `hybrid_rule_and_persistence` yang punya lead (8,0 menit), dan [J] baris 74 menulis larangan
   mengklaim lead menit untuk vib sampai ambangnya dikalibrasi per sumur. Klaim lain harus berbunyi
   "tidak tersedia", bukan kosong dan bukan nol.

## 4. Aturan urutan

### 4.1 Empat lapis, bukan satu skor

Urutan ditentukan berlapis supaya bisa diperiksa manual tanpa menghitung skor gabungan. Lapis
pertama pita, lapis kedua keyakinan, lapis ketiga waktu, lapis keempat umur.

```
urutkan baris dengan kunci:
  1. pangkat(pita) menurun            P4 = 4, P3 = 3, P2 = 2, P1 = 1
  2. ada_lead menurun                 baris berlead (hyd) mendahului baris tanpa lead
  3. K_tampil menurun                 keyakinan bukti lebih tinggi lebih dulu
  4. umur menurun                     yang lebih lama menggantung lebih dulu
  5. kepela_nyala menurun             jumlah kepala yang menyala
  6. waktu naik                       jendela lebih awal lebih dulu, supaya urutan stabil
```

Alasan tiap lapis, semuanya bisa diperiksa:

1. Pita mendahului keyakinan karena `K_tampil` sudah dipotong batas kelas. [DSS1] baris 374 sampai
   395 memberi batas atas 0,4950 untuk vib dan 0,6100 untuk hyd K-i. Bila keyakinan dijadikan lapis
   pertama, baris vib tidak akan pernah mengalahkan baris hyd walaupun tiga kepala vib menyala
   penuh, sehingga kelas dengan batas atas rendah akan selalu tunda. Itu bias sistematis, bukan
   prioritas.
2. Baris berlead mendahului baris tanpa lead pada pita yang sama karena lead memberi tenggat alami.
   [J] hanya memberi satu lead, yaitu 8,0 menit untuk hyd ([J] baris 809 dan 1575 sampai 1577),
   sehingga kunci ini praktis memihak hyd. Itu disengaja: hyd satu-satunya klaim dengan waktu menuju
   onset yang terukur, sedangkan baris tanpa lead tidak punya tenggat, jadi menunggu hanya menambah
   umur tanpa menambah alasan untuk menunggu.
3. Umur dipakai sebagai lapis keempat dan bukan yang pertama, karena umur mengukur beban, bukan
   risiko. [VR] baris 173 menulis "age distribution matters more than a single open count", yang
   artinya umur harus terlihat dan terbagi, bukan bahwa umur mengalahkan keyakinan.
4. Kunci terakhir `waktu` membuat urutan stabil dan bisa direproduksi, sehingga dua orang yang
   menyusun antrean dari data sama mendapat urutan sama.

### 4.2 Jatah minimum per klaim

Tanpa jatah, satu klaim dengan volume besar bisa menghabiskan seluruh anggaran. [H] baris 23136
memberi hyd `rule_display` 18,523 baris per shift, hampir separuh beban 40,15. Aturan jatah:

```
untuk setiap klaim yang punya minimal satu baris P3 atau P4:
  sediakan satu slot sebelum baris kedua dari klaim mana pun
  (kecuali bila anggaran tersisa kurang dari menit baris itu)
```

Jumlah klaim aktif hari ini lima (vib, shk, stuck, hyd, tool_wear) karena ssi bernilai 0 pada
[J] baris 232 dan bit_wear tidak punya head L1 ([J] baris 859 sampai 886 hanya berisi `persistence`
dan `k2_onset_belum`). Lima slot itu berbiaya 22 menit dari anggaran 30 menit, yaitu satu slot P4 enam
menit ditambah empat slot P3 empat menit, jadi jatah minimum menyisakan 8 menit dan itu sama dengan
hitungan jadwal bagian 6.4. Bila kelak klaim aktif bertambah menjadi delapan, aturan yang sama
tidak lagi muat dan anggaran harus naik; angka itu bisa dihitung langsung dari 8 kali 4 menit sama
dengan 32 menit.

### 4.3 Yang tidak dipakai sebagai kunci urutan

Tiga hal sengaja tidak dipakai, dengan alasan yang bisa diperiksa.

Pertama, FAR mentah tidak dipakai sebagai kunci. [S6] baris 150 menulis FAR hyd H1p 4,0984 sedangkan
[J] baris 95 menulis FAR vib 49,942 pada satuan segmen yang sama. Memakai FAR sebagai kunci akan
menenggelamkan vib secara permanen, padahal FAR tinggi berarti beban tinjauan tinggi, bukan risiko
tinggi per baris.

Kedua, presisi segmen tidak dipakai sebagai kunci. Presisi segmen dihitung pada seluruh segmen,
bukan pada jendela itu ([J] baris 93 sampai 95), jadi ia tidak membedakan dua baris dari klaim yang
sama.

Ketiga, jam henti tidak dipakai karena belum terpetakan ke alarm. [J] baris 1756 menulis bahwa jam
henti tidak dapat dipetakan ke satu alarm tertentu karena tidak ada kunci bit atau work order. Memakai
jam henti sebagai bobot berarti mengarang hubungan yang sumbernya menyatakan belum ada.
## 5. Aturan anggaran waktu

### 5.1 Bentuk aturannya

Anggaran dinyatakan sebagai satu angka menit per shift, bukan per jam, karena satu-satunya satuan
beban yang tersedia juga per shift 8 jam ([H] baris 271 dan seterusnya). Bentuknya dua lapis:
menit per baris dari pita, dan tambahan menit per jendela tambahan di dalam satu episode.

**Menit per pita.** Tabel berikut adalah parameter desain, bukan hasil ukur. Kolom dasarnya menyebut
alasan pemilihan, dan bagian 12 menulis syarat pengukurannya.

| Pita | Menit | Isi pemeriksaan yang dihitung | Dasar |
|---|---:|---|---|
| P4 | 6 | buka grafik kanal, periksa tiga kepala yang menyala, cek kanal masukan, tulis alasan, tutup baris | parameter desain, diturunkan dari [DSS1] baris 226 yang mewajibkan konfirmasi operator |
| P3 | 4 | buka satu kanal, cocokkan label, tulis alasan, tutup baris | parameter desain |
| P2 | 2 | lihat kanal, tandai pantau atau tutup | parameter desain, tindakan [DSS1] baris 224 yang memang "pantau" |
| P1 | 0 | tidak masuk antrean | [DSS1] baris 222, tindakan "tidak ada tindakan" |
| abstain AB-1 sampai AB-4 | 0 | tidak masuk antrean, hanya tampil dengan penanda | [DSS1] baris 240 sampai 246 |

**Tambahan per episode.** Jendela berurutan dalam satu klaim dianggap satu episode bila jarak antar
jendela aktif tidak lebih dari 5 menit. Episode pertama dihitung penuh, setiap jendela tambahan
dihitung 1 menit, dan tambahan dibatasi 6 menit. Aturan ini diuji pada data nyata dan hasilnya bisa
diperiksa: hyd K-i punya lima jendela aktif berurutan 20 sampai 24 ([J] baris 814 sampai 819).
Tanpa episode, lima baris bernilai 30 menit. Sebagai satu episode, nilainya 6 ditambah 4 sama dengan
10 menit. Untuk stuck K-i, jendela 8 sampai 12 ([J] baris 520 sampai 524) memberi 20 menit tanpa
episode dan 8 menit sebagai satu episode. Batas 5 menit dipilih karena jarak antar jendela pada
contoh nyata vib adalah 15, 28, 6, dan 11 ([J] baris 79 sampai 83), sehingga hanya pasangan berjarak
6 yang nyaris masuk; memakai batas 5 menit menjaga pasangan itu tetap dua baris dan mencegah
penggabungan yang tidak disengaja.

### 5.2 Algoritma pemilihan baris dengan anggaran

Nama metode: greedy berurut dengan jatah minimum. Ini bukan model, jadi tidak ada pelatihan dan tidak
ada parameter yang dipelajari dari data.

```
masukan : daftar baris sudah terurut (bagian 4.1), A = anggaran menit shift, jatah = 1 slot per klaim
keluaran: jadwal (baris, menit), tunda (baris), sisa menit, jumlah tunda

1. sisa = A; jadwal = []; tunda = []
2. untuk setiap klaim yang punya baris P3 atau P4:
     ambil baris teratas klaim itu, m = menit_baris(baris)
     bila m tidak lebih dari sisa: masukkan ke jadwal, sisa = sisa - m, tandai klaim terlayani
3. untuk setiap baris lain dalam urutan bagian 4.1:
     m = menit_baris(baris)
     bila m tidak lebih dari sisa: masukkan ke jadwal, sisa = sisa - m
     selain itu: masukkan ke tunda
4. bila baris P4 ada di daftar tunda: naikkan A sampai seluruh P4 muat, lalu ulangi langkah 1
5. tampilkan jadwal, jumlah tunda, kekurangan menit, dan sisa menit
```

`menit_baris(baris)` = menit pita ditambah tambahan episode, dengan tambahan dibatasi 6 menit.

Dua sifat yang harus benar dan bisa diuji:

1. P4 tidak pernah ditunda. Langkah 4 memaksa anggaran naik. Alasannya keputusan: P4 adalah pita
   "keyakinan kuat" yang menuntut konfirmasi operator menurut [DSS1] baris 226, dan menundanya
   berarti menunda satu-satunya kelas baris yang buktinya paling kuat.
2. Urutan hasil tidak bergantung pada urutan masukan. Kunci terakhir `waktu` di bagian 4.1
   menjaminnya, sehingga dua penyusun antrean mendapat jadwal sama dari data sama.

### 5.3 Apakah 30 menit masuk akal, dengan angka

Anggaran bawaan 30 menit per shift. Tiga perhitungan berikut memakai angka bagian 2.4 dan 5.1.

| Ukuran | Nilai | Cara memperoleh |
|---|---:|---|
| Beban lambda per shift | 40,15 baris | jumlah 16,647 + 2,206 + 2,774 + 18,523, bagian 2.4 |
| Beban nilai tengah per shift | 39 baris | jumlah p50 per klaim, bagian 2.4 |
| Beban persentil 95 per shift | 61 baris | jumlah p95 per klaim, bagian 2.4 |
| Porsi anggaran terhadap shift | 6,25 persen | 30 dibagi 480 |
| Laju kedatangan baris pada beban tengah | 1 baris per 12,31 menit | 480 dibagi 39 |
| Kapasitas pada 4 menit per baris | 7,5 baris | 30 dibagi 4 |
| Cakupan pada beban tengah | 17,95 persen | 7 dibagi 39 |
| Kebutuhan waktu bila setiap baris diperiksa 10 menit | 390 menit, 81,25 persen shift | 39 kali 10 dibagi 480 |
| Kekurangan waktu pada beban persentil 95, bila 9 baris terlayani | 208 menit | 52 baris sisa kali 4 menit |

Jangkar luar untuk angka 10 menit per baris. EEMUA 191 edisi ketiga halaman 96 menyatakan laju satu
alarm per sepuluh menit sebagai batas nyaman pada operasi tunak, satu per lima menit sebagai batas
yang masih terkelola, satu per dua menit sebagai di atas permintaan, dan lebih dari satu per menit
sebagai sangat tidak dapat diterima. Pada halaman yang sama, dokumen itu juga menyatakan bahwa pada
laju satu alarm per sepuluh menit, operator dapat memakai sampai sepuluh menit untuk menangani satu
alarm (LV17 halaman 3, kutipan langsung dari EEMUA 191 edisi ketiga halaman 96 dan 97; LV18 menulis
kalimat yang sama untuk laju tunak). EEMUA 191 edisi keempat masih memuat bagian "Operator response
times" dan tabel laju maksimum per prioritas (LV19 daftar isi, bagian 2.7.4 dan tabel 18).

Perbandingan yang harus dibaca apa adanya: laju kedatangan baris kita, 1 per 12,31 menit, lebih
lambat daripada jangkar EEMUA, sehingga secara laju tidak tampak berat. Yang membuatnya berat adalah
bahwa satu baris bukan satu alarm yang bisa diakui dalam hitungan detik, melainkan satu jendela yang
harus dicocokkan dengan tiga kepala dan satu batas kelas. Bila setiap baris benar-benar diperiksa 10
menit, kebutuhan waktunya 390 menit atau 81,25 persen shift, dan itu melampaui jam kerja satu orang
berdampingan dengan pekerjaan pengeboran. Karena itu anggaran 30 menit bukan anggaran pemeriksaan
penuh, dan aturan penundaan pada 5.2 menjadi bagian dari spesifikasi, bukan tambahan opsional.

### 5.4 Anggaran yang bisa diubah, dan apa yang berubah

| Anggaran A | Baris yang muat pada 4 menit per baris | Cakupan beban tengah 39 baris | Cakupan beban persentil 95 61 baris |
|---:|---:|---:|---:|
| 15 menit | 3 | 7,69 persen | 4,92 persen |
| 30 menit | 7 | 17,95 persen | 11,48 persen |
| 45 menit | 11 | 28,21 persen | 18,03 persen |
| 60 menit | 15 | 38,46 persen | 24,59 persen |
| 120 menit | 30 | 76,92 persen | 49,18 persen |

Angka pada kolom tiga dan empat dihitung dari pembagian langsung, dan keluarannya ada di bagian 14.4.
Tabel ini dipakai saat supervisor meminta tambahan tenaga: yang dibeli oleh tambahan 30 menit adalah
7 sampai 8 baris, bukan lipat dua cakupan.

### 5.5 Neraca penundaan

Setiap shift wajib mencetak empat angka: jumlah baris masuk, jumlah baris terlayani, jumlah baris
ditunda, dan kekurangan menit. Tanpa keempatnya, antrean yang terlihat rapi menyembunyikan beban.
Aturan tampilannya:

1. Jumlah ditunda ditulis sebagai angka, bukan warna. [K] baris 203 sampai 207 melarang warna tanpa
   label manusia-peninjau.
2. Baris ditunda tetap bisa dibuka dan dicari, tetapi tidak dihitung ke dalam anggaran shift ini.
3. Baris yang ditunda lebih dari 15 menit naik ke puncak urutan shift berikutnya, kecuali ada P4
   baru. Ini satu-satunya tempat umur mengalahkan pita, dan alasannya karena penundaan berulang
   membuat antrean berhenti bermakna.
## 6. Sepuluh baris contoh dengan angka nyata

### 6.1 Cara angka diturunkan tanpa menebak

Status tiap kepala pada satu jendela diturunkan dari `contoh_idx_aktif` di [J], yaitu lima indeks
jendela aktif pertama per kepala yang dibangun dengan `np.where(active)[0]` di [P] baris 384. Karena
daftar itu menaik, berlaku tiga aturan turunan:

1. Indeks yang ada di dalam daftar berarti kepala menyala pada jendela itu.
2. Indeks yang lebih kecil daripada elemen pertama daftar berarti kepala pasti tidak menyala pada
   jendela itu.
3. Karena definisi hibrida adalah `rule(t0-1) AND persistence(t)` ([J] baris 833, juga baris 166,
   309, 458, 607), hibrida menyala berarti rule dan persistence menyala, dan persistence tidak
   menyala berarti hibrida tidak menyala.

Kepala yang belum dapat dipastikan dengan tiga aturan di atas dicatat sebagai tidak diketahui, dan
baris mendapat dua angka: `K_min` bila kepala tak diketahui dianggap 0, dan `K_up` bila dianggap 1.
Rumusnya dari [DSS1] bagian 3.3, dan batas atas kelasnya dari [DSS1] bagian 3.4:

```
K_min  = jumlah w_h untuk kepala yang pasti menyala / jumlah seluruh w_h klaim
K_up   = jumlah w_h untuk kepala yang menyala atau belum dipastikan / jumlah seluruh w_h klaim
K_tampil = min(K_min, K_max_kelas)
```

Bobot `w_h` memakai [DSS1] baris 111 sampai 138: rule 1,00; persistence 0,80; hibrida 1,00 dengan
pengali 1,50 bila `head_utama` benar; rf_lowo 0,25; e1_2of3 0,25; persistence_event 0,25;
op_far_calibrated 1,00; calib_5of27 0,25. Batas atas kelas dari [DSS1] baris 170 sampai 177: vib
0,4950; ssi 0,5263; shk 0,5188; stuck 0,4562; hyd K-i 0,6100; tool_wear 0,4550; bit_wear 0,2525.

### 6.2 Tabel sepuluh baris

| No | Klaim | Jendela | Kepala nyala | K_min | K_up | K_tampil | Pita | Menit | Alasan | Aksi |
|---|---|---:|---|---:|---:|---:|---|---:|---|---|
| 1 | hyd K-i | 20 | rule, persistence, hibrida | 1,0000 | 1,0000 | 0,6100 | P4 | 6 | tiga kepala setara menyala, terpotong batas kelas hyd 0,6100; lead 8,0 menit | konfirmasi lapangan |
| 2 | vib | 429 | rule, persistence, hibrida | 0,9180 | 0,9180 | 0,4950 | P3 | 4 | tiga kepala menyala, RF pasti mati, terpotong batas kelas vib 0,4950; tidak ada lead | periksa kanal |
| 3 | shk | 20 | rule, persistence, hibrida | 0,9180 | 0,9180 | 0,5188 | P3 | 4 | tiga kepala menyala, terpotong batas kelas shk 0,5188; FAR 6,618 per 24 jam | periksa kanal |
| 4 | stuck K-i | 8 | rule, persistence, hibrida | 1,0000 | 1,0000 | 0,4562 | P3 | 4 | tiga kepala menyala, terpotong batas kelas stuck 0,4562; cakupan 2 sumur | periksa kanal |
| 5 | tool_wear K-i | 42 | op_far_calibrated | 0,8000 | 1,0000 | 0,4550 | P3 | 4 | satu kepala peringatan menyala, calib belum pasti, satuan FAR per menit | periksa kanal |
| 6 | stuck K-ii | 30.122 | persistence_event | 0,3333 | 1,0000 | 0,3333 | P2 | 2 | hanya kepala kejadian menyala, e1 dan RF belum pasti; tidak ada lead | pantau |
| 7 | stuck K-ii | 17.582 | rf_lowo | 0,3333 | 0,6667 | 0,3333 | P2 | 2 | hanya kepala RF menyala, e1 belum pasti, ranking saja | pantau |
| 8 | hyd K-i | 0 | rule | 0,3030 | 0,3030 | 0,3030 | P2 | 2 | satu kepala menyala, persistence dan hibrida pasti mati karena aktivasi pertama di 20 | pantau |
| 9 | bit_wear K-1 | 29.120 | persistence | 1,0000 | 1,0000 | 0,2525 | P2 | 2 | kepala tunggal menyala penuh, batas kelas bit_wear 0,2525 menekan | pantau |
| 10 | ssi | 118 | persistence | 0,2623 | 0,2623 | 0,2623 | P2 | 0 | kanal absen 5.268 dari 5.455 jendela, status AB-2, keluar dari antrean | tutup |
| | | | | | | | | **30** | sembilan baris masuk antrean, satu keluar | |

Sumber kepala dan indeks per baris: vib `contoh_idx_aktif` rule dan hibrida pada [J] baris 79 sampai
83 dan 147 sampai 151, rf_lowo pada baris 180 sampai 184; shk rule, persistence, hibrida pada
[J] baris 371 sampai 375, 405 sampai 409, 439 sampai 443; stuck rule, persistence, hibrida pada
[J] baris 520 sampai 524, 554 sampai 558, 588 sampai 592; stuck K-ii `persistence_event` dan
`rf_lowo` pada [J] baris 655 sampai 659 dan 692 sampai 696; hyd rule pada [J] baris 743 sampai 747,
hyd persistence dan hibrida pada [J] baris 777 sampai 781 dan 814 sampai 819; bit_wear
`persistence` pada [J] baris 869 sampai 873; tool_wear `op_far_calibrated` pada [J] baris 1060
sampai 1064; ssi `persistence` pada [J] baris 262 sampai 266.

### 6.3 Perhitungan tiap baris, satu per satu

Baris 1, hyd K-i jendela 20. Hibrida ada di daftar, jadi rule dan persistence juga menyala. Bobot
1,00 ditambah 1,50 ditambah 0,80 sama dengan 3,30 dari total 3,30, sehingga `K_min` sama dengan
1,0000. Batas kelas hyd K-i 0,6100 ([DSS1] baris 391), jadi `K_tampil` 0,6100 dan pita P4.

Baris 2, vib jendela 429. Rule dan hibrida ada di daftar, persistence dipaksa menyala oleh aturan
ketiga, rf_lowo pasti mati karena aktivasi pertamanya 517, jauh di atas 429. Jumlah 1,00 ditambah
1,00 ditambah 0,80 sama dengan 2,80 dari 3,05, yaitu 0,9180. Batas kelas vib 0,4950 menekan, jadi
pita P3.

Baris 3, shk jendela 20. Ketiga kepala ada di daftar dan RF aktifnya nol di seluruh segmen
([J] baris 472 menulis daftar kosong), sehingga 2,80 dari 3,05 sama dengan 0,9180, ditekan batas
0,5188 menjadi P3.

Baris 4, stuck K-i jendela 8. Rule dan hibrida ada di daftar, persistence pertama aktif di indeks 0
sampai 4 ([J] baris 554 sampai 558) lalu dipaksa menyala oleh hibrida. Jumlah 2,80 dari 2,80 sama
dengan 1,0000, ditekan batas stuck 0,4562 menjadi P3.

Baris 5, tool_wear K-i jendela 42. `op_far_calibrated` ada di daftar ([J] baris 1060). `calib_5of27`
aktif pada 19 sampai 23 ([J] baris 1720? lihat [J] head tool_wear calib contoh indeks 19, 20, 21, 22,
23) sehingga statusnya pada 42 tidak dapat dipastikan. `K_min` 1,00 dari 1,25 sama dengan 0,8000 dan
`K_up` 1,0000. Batas kelas 0,4550 menekan keduanya, jadi pita P3 pada kedua batas.

Baris 6, stuck K-ii jendela 30.122. Hanya `persistence_event` yang pasti menyala. `e1_2of3` aktif
pertama pada 3.560 dan `rf_lowo` pada 17.582, keduanya di bawah 30.122 sehingga status pada jendela
ini tidak dapat dipastikan. `K_min` 0,25 dari 0,75 sama dengan 0,3333, `K_up` 1,0000. Pita bawah P2,
pita atas P3, dan baris ditampilkan sebagai P2 dengan penanda "batas atas P3".

Baris 7, stuck K-ii jendela 17.582. `rf_lowo` menyala pada indeks aktivasi pertamanya. `e1_2of3`
tidak dapat dipastikan, `persistence_event` tidak dapat dipastikan pada jendela sebesar ini karena
hanya empat jendela aktifnya yang tercatat (30.122, 30.126, 31.473, 34.343). `K_min` 0,3333,
`K_up` 0,5000 dari 0,75 sama dengan 0,6667. Pita bawah P2, atas P3.

Baris 8, hyd K-i jendela 0. Hanya rule yang menyala. Persistence aktivasi pertama pada 20, jadi
pasti mati pada 0, dan hibrida ikut pasti mati. Angka 1,00 dari 3,30 sama dengan 0,3030 tanpa
interval, karena tidak ada kepala yang belum dipastikan. Pita P2.

Baris 9, bit_wear jendela 29.120. Klaim K-1 hanya punya satu kepala, yaitu `persistence` berbobot
0,25 dari 0,25, jadi `K_min` sama dengan 1,0000. Batas kelas bit_wear 0,2525 ([DSS1] baris 393)
menekan angka itu menjadi P2. Baris ini contoh paling jelas bahwa keyakinan jendela dan keyakinan
kelas dua hal berbeda.

Baris 10, ssi jendela 118. `persistence` menyala, sedangkan rule, hibrida, dan rf_lowo semua pasti
mati karena `n_aktif` ketiganya 0 ([J] baris 232, 294, 321). Angka 0,80 dari 3,05 sama dengan
0,2623. Baris ini berhenti di aturan abstain AB-2 dari [DSS1] baris 244: `n_nodata` 5.268 dari
5.455 jendela sama dengan 0,9657, di atas ambang 0,50. Baris tetap tampil dengan alasan kanal
absen, tetapi tidak masuk antrean dan menitnya 0.

### 6.4 Jadwal yang dihasilkan aturan 5.2 pada sepuluh baris itu

| Langkah | Baris | Pita | Menit | Kumulatif | Status |
|---:|---|---|---:|---:|---|
| 1 | hyd K-i 20 | P4 | 6 | 6 | masuk, jatah klaim hyd |
| 2 | vib 429 | P3 | 4 | 10 | masuk, jatah klaim vib |
| 3 | shk 20 | P3 | 4 | 14 | masuk, jatah klaim shk |
| 4 | stuck K-i 8 | P3 | 4 | 18 | masuk, jatah klaim stuck |
| 5 | tool_wear K-i 42 | P3 | 4 | 22 | masuk, jatah klaim tool_wear |
| 6 | stuck K-ii 30.122 | P2 | 2 | 24 | masuk |
| 7 | stuck K-ii 17.582 | P2 | 2 | 26 | masuk |
| 8 | hyd K-i 0 | P2 | 2 | 28 | masuk |
| 9 | bit_wear K-1 29.120 | P2 | 2 | 30 | masuk, anggaran habis |
| 10 | ssi 118 | abstain | 0 | 30 | tidak masuk, alasan AB-2 |

Hasilnya sembilan baris terlayani dalam 30 menit dengan sisa 0 menit, dan satu baris keluar karena
status abstain. Angka ini bukan kebetulan yang dipilih supaya pas: menit hanya bergantung pada pita,
dan sebaran pita pada sepuluh contoh ini adalah satu P4, empat P3, dan empat P2 yang benar-benar
masuk hitungan. Bila ada baris P2 kelima yang bukan abstain, aturan 5.2 akan menaruhnya di daftar
tunda dengan kekurangan 2 menit, dan bagian 5.5 mewajibkan angka itu tampil.

### 6.5 Uji tekanan pada beban nyata, bukan pada contoh

Sepuluh baris di atas adalah contoh untuk memeriksa aritmetika. Beban sesungguhnya per shift adalah
40,15 baris pada nilai tengah dan 61 baris pada persentil 95 (bagian 2.4). Dengan kapasitas 7 sampai
9 baris pada anggaran 30 menit, shift pada persentil 95 menunda sekitar 52 baris dan kekurangan
sekitar 208 menit. Dua konsekuensi yang harus tertulis di layar: pita P4 dan P3 selalu dilayani lebih
dulu sesuai 5.2, dan jumlah tunda adalah angka yang wajib dibaca supervisor, bukan catatan kaki.
## 7. Tiga keadaan antrean

Tiga keadaan ini bukan hiasan. Masing-masing punya pemicu angka, perilaku tampilan, dan kegagalan
yang dicegah.

### 7.1 Keadaan kosong

**Pemicu.** Tidak ada baris P3 atau P4 pada shift itu. Angka pendukungnya nyata dan hari ini benar
untuk satu klaim: ssi `rule_display` punya `n_aktif` 0 dari 5.455 jendela ([J] baris 232), FAR 0,0
([J] baris 244), dan daftar contoh aktifnya kosong ([J] baris 234). Pada [H], bin jendela untuk
bit_wear 0, 1, dan 2 masing-masing berisi 398 jendela dengan a sama dengan 0, artinya tiga blok awal
segmen bit_wear tidak menyala sama sekali.

**Perilaku tampilan.** Layar menampilkan empat hal: tulisan "tidak ada baris berprioritas", jumlah
baris pantau P2 yang tersedia, waktu pembaruan terakhir, dan satu baris status kanal per klaim.
Anggaran tidak dialihkan otomatis ke baris P2, sesuai [DSS1] baris 222 yang menyatakan P1 tanpa
tindakan dan baris 224 yang menyatakan P2 hanya dipantau.

**Salah tafsir yang dicegah.** Kosong bukan bukti rig sehat. Kanal yang absen menghasilkan nol palsu,
dan itu sudah terukur: ssi `rule_display` punya `n_nodata` 5.268 dari 5.455 jendela ([J] baris 247),
yaitu 96,57 persen. Karena itu keadaan kosong wajib menampilkan label kanal, dan bila rasio kanal
absen di atas 0,50, label yang tampil adalah "tidak dinilai, kanal absen", bukan "aman". Ini pola
Dynamic Island: yang hilang menjadi label, bukan angka nol.

### 7.2 Keadaan panjang

**Pemicu.** Jumlah baris pada satu shift melewati kapasitas anggaran, atau satu klaim menyala
beruntun. Dua pemicu ini berbeda dan keduanya terukur.

Pemicu pertama, lonjakan beruntun, punya bukti langsung di [H]: hyd `rule_display` bin 65 menyala 87
dari 87 jendela, stuck `rule_display` bin 1 menyala 25 dari 27 dan bin 2 menyala 26 dari 27, vib
`rule_display` bin 94 menyala 17 dari 17, dan shk `rule_display` bin 74 menyala 20 dari 94.

Pemicu kedua, volume shift, dihitung dari lambda gabungan 40,15: peluang sedikitnya 30 baris adalah
0,9588, sedikitnya 40 baris 0,5305, sedikitnya 50 baris 0,0737, dan sedikitnya 61 baris 0,0013
(keluaran hitung di bagian 14.3). Artinya hampir separuh shift akan melewati 40 baris.

**Perilaku tampilan.** Empat aturan, semuanya bisa diperiksa:

1. Pengelompokan episode dijalankan sebelum menghitung menit. Tujuh puluh delapan jendela beruntun
   pada satu klaim adalah satu episode, bukan 78 baris, dan itu yang membuat keadaan panjang masih
   bisa dibaca.
2. Batas keras 8 baris per klaim per shift, dengan sisanya masuk daftar tunda bernomor. Tanpa batas,
   hyd `rule_display` dengan 18,523 baris per shift ([H] baris 23136) menghabiskan seluruh anggaran.
3. Banner angka, bukan warna: "N baris ditunda, kekurangan X menit". Angka ini wajib pada keadaan
   panjang dan wajib nol pada keadaan normal.
4. Mode sapu: satu keputusan menutup satu episode, dan keputusan itu tercatat sekali dengan daftar
   jendela yang dicakup. Tanpa mode sapu, antrean memaksa satu keputusan per menit selama 87 menit,
   dan itu bukan pekerjaan yang bisa diselesaikan manusia.

**Salah tafsir yang dicegah.** Antrean panjang dibaca sebagai tanda bahaya. Panjang antrean mengukur
beban, bukan risiko. [VR] baris 251 menulis larangan memakai satu angka backlog karena jumlah terbuka
menyembunyikan bentuk pekerjaan, dan [VR] baris 173 menulis bahwa sebaran umur lebih informatif
daripada satu hitungan terbuka. Karena itu keadaan panjang selalu menampilkan sebaran umur, bukan
hanya jumlah.

### 7.3 Keadaan keyakinan rendah

**Pemicu.** Baris dengan pita P1 atau P2, atau baris yang `K_up` dan `K_min` jatuh di pita berbeda,
atau baris dengan status abstain.

Bukti nyata bahwa keadaan ini akan sering muncul: batas atas kelas menekan banyak baris. vib mentok
di 0,4950 dan bit_wear di 0,2525 walaupun kepala pada jendela itu menyala penuh ([DSS1] baris 374
sampai 395, dengan contoh perhitungan di bagian 6.3 baris 2 dan baris 9). Baris 6 dan 7 pada bagian
6.2 punya `K_min` P2 dan `K_up` P3 sekaligus.

**Perilaku tampilan.**

1. Baris P2 tidak masuk anggaran kerja. Ia tampil di blok terpisah bernama "pantau", tanpa tombol
   tindakan, sesuai [DSS1] baris 224 dan paragraf perilaku kartu di [DSS1] baris 947 sampai 952.
2. Baris dengan dua pita menampilkan rentang, contoh "P2, batas atas P3", dan diurutkan memakai pita
   bawah. Alasan memilih pita bawah: menaikkan baris karena kemungkinan tertinggi adalah cara
   tercepat mengubah ketidakpastian menjadi beban kerja.
3. Baris abstain menampilkan kode dan alasan, dengan angka diganti tanda, sesuai [DSS1] baris 236
   sampai 250.
4. Ketiga keadaan keyakinan rendah tidak boleh diwarnai merah. [K] baris 203 sampai 207 melarang
   warna tanpa label manusia-peninjau.

**Salah tafsir yang dicegah.** Keyakinan rendah dibaca sebagai model rusak. Yang sering terjadi
sebaliknya: keyakinan rendah adalah batas bukti kelas yang bekerja benar. bit_wear dengan `K_tampil`
0,2525 bukan model yang salah menilai jendela, melainkan kelas yang buktinya belum cukup untuk
menaikkan tindakan.

## 8. Saran penyajian, dengan dasar riset

### 8.1 Bentuk utama: tabel terurut

Bentuk utama antrean adalah tabel terurut, bukan kartu dan bukan papan kanban. Tiga alasan yang bisa
diperiksa:

1. Beban nyata puluhan baris per shift. Lambda gabungan 40,15 (bagian 2.4) dan persentil 95 61 baris.
   [VR] baris 175 sudah mencatat bahwa tata letak kartu lima baris tidak cukup untuk volume itu.
2. Tiap baris butuh sepuluh atribut sekaligus: klaim, jendela, kepala, keyakinan, interval, pita,
   FAR, lead, umur, menit. Tabel adalah bentuk yang memang dirancang untuk banyak atribut per baris,
   dan LV6 terdaftar pada [VR] baris 46, dipakai untuk nilai yang harus dibaca tepat.
3. Tugas yang dilayani adalah mencari, membandingkan, dan memutuskan. [VR] baris 121 menyebut tiga
   tugas itu untuk keluaran antrean, dengan sumber LV4.

Tata letak dalam teks:

```
+--------------------------------------------------------------------------------------+
| ANTREAN TINJAUAN SHIFT        anggaran 30 menit   terlayani 9   ditunda 0   tunda 0 m|
+----+-------------------+----------+----------------+-----+----+--------+------+------+
| No | Klausa            | Jendela  | Kepala         | K   | Pita| Umur  | Menit| Aksi |
+----+-------------------+----------+----------------+-----+----+--------+------+------+
|  1 | hyd K-i           |     20   | rule+pers+hib  | 61% | P4  | 0 mnt |   6  | cek  |
|  2 | vib               |    429   | rule+pers+hib  | 50% | P3  | 0 mnt |   4  | cek  |
|  3 | shk               |     20   | rule+pers+hib  | 52% | P3  | 0 mnt |   4  | cek  |
|  4 | stuck K-i         |      8   | rule+pers+hib  | 46% | P3  | 0 mnt |   4  | cek  |
|  5 | tool_wear K-i     |     42   | op_far         | 46% | P3  | 0 mnt |   4  | cek  |
+----+-------------------+----------+----------------+-----+----+--------+------+------+
| P A N T A U (tidak masuk anggaran, tanpa tombol tindakan)                             |
|  6 | stuck K-ii        | 30.122   | pers_event     | 33% | P2  | 4 mnt |   2  | lihat|
+--------------------------------------------------------------------------------------+
| tidak dinilai (abstain): ssi 118, kanal absen 96,6 persen                             |
+--------------------------------------------------------------------------------------+
```

Aturan bentuk tabel yang wajib:

1. Kolom pertama berisi nama klaim dan jendela, bukan ID otomatis. [VR] baris 173 mengutip LV4:
   kolom pertama harus pengenal yang terbaca manusia, bukan ID yang tidak bermakna.
2. Kolom umur memakai empat pita: 0 sampai 15 menit, 16 sampai 60 menit, 61 sampai 120 menit, di
   atas 120 menit. Ini adaptasi dari bucket LV14 yang ber satuan hari (0 sampai 2 hari, 3 sampai 7
   hari, 8 sampai 15 hari, di atas 30 hari) ke satuan menit karena antrean ini per shift. Adaptasi
   satuan dicatat sebagai pilihan desain, bukan kutipan sumber.
3. Angka keyakinan ditulis sebagai persen bulat dengan label "keyakinan bukti", dan badge FAR selalu
   di sebelahnya, sesuai [DSS1] baris 222 sampai 228.
4. Kepala tabel lengket, dan baris pada pita umur tertinggi diberi latar berbeda. Warna tetap
   disertai teks agar terbaca pada skala abu ([K] baris 203 sampai 207).

### 8.2 Bentuk pendamping: tiga kartu fokus

Di atas tabel, maksimal tiga kartu. Alasannya bukan estetika: [VR] baris 175 menyebut beban puluhan
baris, sehingga kartu hanya dipakai untuk baris teratas yang harus dibaca sebelum tabel. Tiga, bukan
lima, karena [H] baris 25883 memberi hyd K-i p95 hanya 10 baris dan p50 5, sehingga kartu lebih dari
tiga akan menampilkan baris yang sama dengan tabel di bawahnya.

Kartu berisi: nama klaim dan jendela, pita sebagai lencana bertulisan, satu batang mendatar 0 sampai
1 dengan garis batas kelas, jumlah kepala yang dinilai, badge FAR, lead bila ada, dan umur. Batang
mendatar dipilih karena panjang dan posisi adalah kanal terbaik untuk besaran ([VR] baris 248, LV7),
sedangkan gauge dan cakram justru harus dihindari.

### 8.3 Bentuk ketiga: papan tiga kolom, hanya untuk serah terima

Papan kanban dipakai hanya pada serah terima shift, dengan tiga kolom: "baru", "sedang diperiksa",
"ditunda". Alasannya karena pertanyaan pada serah terima adalah "apa yang belum selesai", bukan
"seberapa tinggi keyakinannya", dan [VR] baris 10 menulis bahwa pilihan visual ditentukan pertanyaan
yang harus dijawab pembaca (LV13). Papan tidak menggantikan tabel, karena papan kehilangan angka dan
tidak dapat diurutkan.

Aturan papan yang mencegah kesalahan: setiap kartu pada papan membawa angka `K_tampil` dan umur, dan
jumlah kartu di kolom "ditunda" wajib sama dengan angka tunda pada banner 7.2. Bila berbeda, tampilan
salah, bukan datanya.

### 8.4 Rujukan riset penyajian

| Kode | Sumber | Dipakai untuk |
|---|---|---|
| LV4 | Data Tables: Four Major User Tasks, Nielsen Norman Group, 2022, https://www.nngroup.com/articles/data-tables | kolom pertama harus pengenal terbaca manusia; tabel untuk tugas cari, banding, aksi |
| LV6 | Financial Times Visual Vocabulary, https://raw.githubusercontent.com/Financial-Times/chart-doctor/main/visual-vocabulary/README.md | angka tepat untuk nilai yang harus dibaca persis |
| LV7 | Dashboards: Making Charts and Graphs Easier to Understand, NN/g, 2017, https://www.nngroup.com/articles/dashboards-preattentive | panjang dan posisi untuk besaran; penolakan gauge |
| LV13 | Choosing Chart Types: Consider Context, NN/g, 2022, https://www.nngroup.com/articles/choosing-chart-types | pilihan visual ditentukan pertanyaan pembaca |
| LV14 | Queue Aging Report for Operations Teams, Workhint, https://blog.workhint.com/blog/queue-aging-report-operations-teams | sebaran umur lebih informatif daripada satu hitungan terbuka; bucket umur |
| LV17 | The sense and nonsense of Alarm system performance KPIs, M.A.C. Solutions (UK) Ltd, https://www.processvue.com/downloads/Alarm_system_performance_KPIs_V1_0.pdf | jangkar laju alarm dan waktu per alarm dari EEMUA 191 edisi ketiga halaman 96 dan 97 |
| LV18 | Effective alarm management for optimal human performance, Human Factors 101, https://humanfactors101.com/topics/alarms | kalimat yang sama untuk laju tunak satu alarm per sepuluh menit |
| LV19 | EEMUA Publication 191 Edition 4, daftar isi, November 2024, https://www.eemua.org/getattachment/9d3f8071-55c3-49bf-a74a-3bf6ad4a2e0f/Contents-EEMUA-Publication-191-Edition4-November-2024.pdf | bukti bahwa bagian "Operator response times" dan tabel laju per prioritas masih ada di edisi keempat |

LV4, LV6, LV7, LV13, dan LV14 sudah terdaftar di [VR] bagian 9 dengan ukuran byte nyata. LV17 sampai
LV19 adalah tambahan dokumen ini untuk jangkar beban kerja, bukan untuk bentuk visual, dan ketiganya
dibuka pada 2026-10-31. Pemisahan ini penting: rujukan bentuk visual tidak boleh dicampur dengan
rujukan beban kerja.
## 9. Spesifikasi fitur

Tujuh fitur, masing-masing dengan tiga belas butir wajib. Kode ANT dipakai karena katalog belum punya
kode untuk antrean per shift; padanannya di [K] adalah MNT-01 (antrean triage onset per shift, baris
871), MNT-02 (kalkulator anggaran pemeriksaan, baris 940), MNT-05 (penaksir beban tinjauan per shift,
baris 1099), dan LIN-01 (log keputusan, baris 2073).

### ANT-01 Baris antrean tinjauan

**ID dan nama fitur.** ANT-01, "Baris antrean tinjauan". Satu baris berarti satu klaim pada satu
jendela.

**Tujuan.** Menyatukan semua yang dibutuhkan satu keputusan ke dalam satu baris yang sulit
dibaca salah, sehingga insinyur tidak perlu membuka empat dokumen sebelum memutuskan. Masalah yang
diselesaikan: hari ini angka keyakinan ada di satu dokumen, FAR di dokumen lain, dan beban per shift
di dokumen ketiga.

**Menggambarkan apa.** Satu jendela waktu 60 detik pada satu klaim, beserta bukti yang menyala dan
mutu bukti kelasnya. Bila `K_tampil` naik, bukti pada jendela itu menguat. Bila `K_tampil` turun
padahal sinyal lapangan sama, penyebabnya batas kelas yang turun setelah komponennya terukur, bukan
sinyal yang melemah ([DSS1] baris 246 sampai 252).

**Pengguna dan momen pakai.** Insinyur pengeboran shift malam: awal shift, lalu setiap dua jam, jadi
lima kali per shift 12 jam ([K] baris 882). Toolpusher: saat menanyakan status ke insinyur, dua sampai
tiga kali per shift. Supervisor pagi: sekali, pada serah terima.

**Masukan.** [J] untuk `n_aktif`, `frac_aktif`, `metrik_segmen`, `contoh_idx_aktif`, `lead_menit`,
`human_review_required` per head; [H] untuk `series` dan `montecarlo`; [DSS1] untuk bobot kepala,
batas kelas, dan pita. Kolom dan satuan yang dipakai ada di tabel bagian 3. Rentang nilai hari ini:
`K_tampil` 0 sampai 0,6100; `n_aktif` 0 sampai 4.917; jendela 0 sampai 95.924.

**Algoritma.** Nama metode: penyusunan baris deterministik dari kunci JSON, tanpa model.
Langkahnya: (1) untuk setiap klaim, ambil daftar kepala dan bobotnya dari [DSS1] baris 118 sampai
143; (2) untuk setiap jendela aktif pada satu kepala, tandai status 1; (3) turunkan status kepala
lain memakai tiga aturan bagian 6.1; (4) hitung `K_min` dan `K_up` dengan rumus bagian 6.1; (5)
potong dengan batas kelas; (6) tetapkan pita; (7) isi `alasan` dari `badge_far` dan `batas_pemakaian`
head yang menyala. Parameter: bobot kepala dan batas kelas, keduanya diambil apa adanya dari [DSS1]
dan tidak diubah di sini. Alasan memilih cara ini: seluruh angka masukan sudah ada, sehingga tidak
perlu menjalankan ulang model atau menambah asumsi baru.

**Workflow.**
1. Muat [J] dan [H], catat ukuran byte dan waktu muat.
2. Untuk setiap klaim, susun daftar kepala dan bobotnya.
3. Untuk setiap kepala, baca `contoh_idx_aktif` dan bangun tiga himpunan: pasti menyala, pasti mati,
   belum pasti.
4. Untuk setiap jendela yang punya minimal satu kepala menyala, bangun satu baris.
5. Hitung `K_min`, `K_up`, dan `K_tampil`.
6. Tetapkan pita dan tindakan.
7. Periksa aturan abstain, tandai baris yang keluar dari antrean.
8. Isi `alasan` dan `aksi`, lalu kirim ke pengurut pada bagian 4.
9. Tampilkan dengan bentuk bagian 8.

**Keluaran.** Bentuk data: satu objek per baris dengan empat belas kolom pada bagian 3. Satuan:
campuran, dan setiap angka membawa satuannya sendiri. Rentang: `K_tampil` 0 sampai 0,6100 hari ini;
`menit` 0 sampai 15; `umur` 0 sampai 87 menit pada contoh. Arti tiap nilai ada di bagian 3, dan arti
paling penting: `K_tampil` 0,61 berarti keyakinan bukti 61 persen pada skala [DSS1], bukan peluang
kerusakan 61 persen.

**Saran penyajian.** Tabel terurut, satu baris satu baris antrean, dengan kolom pertama nama klaim dan
jendela. Alasan: sepuluh atribut per baris dan volume puluhan baris per shift (bagian 8.1). Contoh
tata letak ada di bagian 8.1.

**Dasar riset penyajian.** LV4 untuk kolom pertama yang terbaca manusia dan tugas tabel; LV6 untuk
nilai yang harus dibaca tepat; LV14 untuk keharusan menampilkan umur. Ketiganya dirujuk lewat
[VR] baris 173, 175, dan 121.

**Status bukti.** Sebagian sudah dihitung dari data nyata: seluruh sepuluh baris bagian 6.2 dan semua
angka bagian 2. Belum: menit, umur, dan peta sumur, ketiganya disebut di bagian 12 dan 13. Baris
belum pernah dirender di layar.

**Salah tafsir yang harus dicegah.**
1. Membaca pita sebagai peluang. Pencegahan: label "keyakinan bukti" pada setiap angka, dan badge
   kalibrasi dari [DSS1].
2. Membaca baris tanpa kepala RF sebagai bukti RF setuju. Pencegahan: kolom kepala hanya menyebut
   yang menyala, dan baris dengan kepala belum pasti menampilkan interval.
3. Membaca `K_tampil` yang mentok sebagai model lemah. Pencegahan: batas kelas tampil di samping
   angka, dengan tanggal rujukan.

**Cara menguji.**
1. Uji turunan: ambil sepuluh baris bagian 6.2, hitung ulang `K_min` dengan tangan, cocokkan.
2. Uji kelengkapan: setiap baris punya empat belas kolom terisi, tidak ada `alasan` kosong.
3. Uji satuan: setiap `badge_far` menyebut per 24 jam atau per menit, dan pemeriksa menolak baris
   tanpa satuan.
4. Uji abstain: baris ssi 118 harus keluar dari antrean dengan kode AB-2, dan baris hyd K-ii serta
   bit_wear K-2 harus keluar dengan kode AB-1.

### ANT-02 Peringkat berlapis

**ID dan nama fitur.** ANT-02, "Peringkat berlapis". Mengurutkan baris dengan empat lapis kunci.

**Tujuan.** Memberi satu urutan yang bisa dipertanggungjawabkan ketika baris lebih banyak daripada
anggaran, tanpa membuat skor gabungan baru yang tidak dapat diperiksa. Untuk insinyur shift dan
supervisor.

**Menggambarkan apa.** Mendekati kepentingan relatif antar baris. Bila urutan berubah, penyebabnya
salah satu dari empat: pita berubah, ada tidaknya lead, keyakinan berubah, atau umur bertambah.
Perubahan urutan karena keyakinan turun berarti bukti kelas berubah, bukan bahaya baru.

**Pengguna dan momen pakai.** Insinyur shift: setiap kali antrean disusun, lima kali per shift.
Supervisor: saat memeriksa apakah urutan masuk akal, sekali per shift.

**Masukan.** `pita`, `K_tampil`, `umur`, `waktu`, `lead`, dari ANT-01. Satuan: kategori, rasio, menit,
indeks. Rentang: lihat bagian 3.

**Algoritma.** Nama metode: pengurutan leksikografis enam kunci (bagian 4.1). Tidak ada skor
gabungan, tidak ada bobot baru. Parameter: pangkat pita P4 sama dengan 4 sampai P1 sama dengan 1, dan
`ada_lead` sebagai nilai benar atau salah. Alasan memilih leksikografis: setiap kunci bisa diperiksa
sendiri, dan tidak ada cara menyembunyikan kompromi di dalam satu angka. Alasan menaruh pita di
depan keyakinan ada di bagian 4.1 butir 1, dengan angka batas kelas 0,4950 lawan 0,6100.

**Workflow.**
1. Terima daftar baris dari ANT-01.
2. Buang baris abstain dan P1.
3. Terapkan jatah minimum per klaim (bagian 4.2).
4. Urutkan dengan enam kunci.
5. Simpan kunci yang menentukan pada tiap baris, supaya bisa diaudit.
6. Kirim ke ANT-03 untuk pemotongan anggaran.

**Keluaran.** Daftar berurut dengan medan tambahan `kunci_penentu` yang menyebut lapis mana yang
memutuskan urutan dua baris bersebelahan. Satuan: tidak ada, keluarannya urutan. Arti: bila
`kunci_penentu` sama dengan "pita", dua baris itu berbeda pita, dan pemeriksa bisa mencocokkan pita
keduanya.

**Saran penyajian.** Nomor urut pada tabel, plus satu kolom sempit "dasar urut" yang berisi satu kata:
pita, lead, yakin, umur, kepala. Alasan: urutan tanpa alasan tidak dapat dibantah, dan pembandingan
antar shift butuh alasan yang terbaca. Rujukan bentuk: LV13 lewat [VR] baris 10, bahwa visual dipilih
menurut pertanyaan pembaca, yang di sini berbunyi "mengapa baris ini di atas".

**Dasar riset penyajian.** LV13 dan LV14 lewat [VR] baris 10 dan 11. LV14 relevan karena umur adalah
salah satu kunci, dan sumber menyatakan sebaran umur lebih informatif daripada satu hitungan.

**Status bukti.** Aturan urutan: rancangan dokumen ini, sudah diuji pada sepuluh baris contoh bagian
6.4. Belum diuji pada beban nyata 40 baris, karena larik status penuh per jendela belum diekspor
(bagian 12).

**Salah tafsir yang harus dicegah.**
1. Nomor satu dibaca sebagai kejadian paling mungkin. Pencegahan: kolom pita dan keyakinan selalu
   tampil, dan urutan P3 bisa berada di atas P4 hanya bila P4 sudah tidak ada.
2. Baris dengan kelas batas atas rendah dianggap kurang penting. Pencegahan: jatah minimum per klaim
   pada bagian 4.2, dan kolom "batas kelas" pada kartu.
3. Urutan berubah karena umur dianggap bahaya meningkat. Pencegahan: `kunci_penentu` menyebut "umur"
   secara terang.

**Cara menguji.**
1. Uji stabilitas: jalankan dua kali dengan urutan masukan dibalik, hasil harus identik.
2. Uji jatah: dengan lima klaim aktif dan anggaran 30 menit, kelima klaim harus terwakili.
3. Uji dominasi: buat data uji dengan satu klaim 20 baris P3 dan klaim lain 1 baris P3, pastikan
   klaim kecil tetap dapat slot.
4. Uji keterbacaan: minta satu insinyur menjelaskan mengapa baris nomor tiga di atas nomor empat,
   dan jawabannya harus bisa dibaca dari `kunci_penentu`.

### ANT-03 Anggaran waktu shift dan neraca penundaan

**ID dan nama fitur.** ANT-03, "Anggaran waktu shift dan neraca penundaan".

**Tujuan.** Mengubah antrean menjadi jadwal yang benar-benar muat dalam menit yang tersedia, dan
mencetak apa yang tidak muat. Masalah yang diselesaikan: antrean tanpa anggaran selalu terlihat
penuh, dan pekerjaan yang tidak selesai menjadi tidak terlihat.

**Menggambarkan apa.** Kapasitas perhatian manusia per shift, bukan jumlah kejadian. Bila anggaran
terpakai penuh dan tunda bertambah, artinya beban melebihi kapasitas, bukan rig memburuk. Bila tunda
nol selama beberapa shift, artinya anggaran mungkin terlalu besar untuk beban saat itu, dan itu juga
informasi.

**Pengguna dan momen pakai.** Insinyur shift: setiap penyusunan antrean. Supervisor shift: sekali
per shift, saat menandatangani beban. Perencana tenaga kerja: sekali per minggu, saat memutuskan
jumlah orang.

**Masukan.** `pita`, `menit` per baris, panjang episode, dan `A` anggaran. Satuan: menit. Rentang:
`menit` 0 sampai 15 per baris; `A` 15 sampai 120 menit (tabel 5.4). Cara memperoleh: `menit` dari
tabel 5.1, `A` dari kebijakan supervisor, bukan dari data.

**Algoritma.** Nama metode: greedy berurut dengan jatah minimum dan pengaman P4 (bagian 5.2).
Parameter: menit per pita 6, 4, 2, 0; tambahan episode 1 menit dengan batas 6; batas keras 8 baris per
klaim; batas jarak episode 5 menit. Alasan memilih greedy dan bukan knapsack: greedy menghasilkan
jadwal yang sama setiap kali tanpa perlu fungsi tujuan yang disepakati, dan pada ukuran 40 baris
selisih terhadap solusi optimal tidak sepadan dengan tambahan kerumitan yang harus diaudit. Alasan
pengaman P4: menunda pita dengan bukti terkuat adalah satu-satunya keputusan yang tidak boleh
diambil otomatis.

**Workflow.**
1. Terima daftar berurut dari ANT-02.
2. Hitung `menit` per baris, termasuk tambahan episode.
3. Jalankan jatah minimum per klaim.
4. Jalankan pengisian sampai anggaran habis.
5. Bila ada P4 di daftar tunda, naikkan `A` dan ulangi.
6. Cetak jadwal, jumlah tunda, kekurangan menit, dan sisa menit.
7. Simpan ke log keputusan (ANT-06) supaya bisa dibandingkan antar shift.

**Keluaran.** Empat angka dan dua daftar. Angka: jumlah masuk, jumlah terlayani, jumlah ditunda,
kekurangan menit. Daftar: jadwal dengan menit per baris, dan daftar tunda berurut. Satuan: menit dan
jumlah baris. Rentang: pada beban tengah 39 baris dan `A` 30 menit, terlayani 7 sampai 9 baris dan
tunda 30 sampai 32 baris (bagian 5.3 dan 6.5). Arti: tunda 30 berarti lebih dari tiga perempat baris
belum dilihat manusia pada shift itu.

**Saran penyajian.** Satu kartu angka di atas tabel berisi empat angka: masuk, terlayani, ditunda,
kekurangan menit. Alasan: empat angka ini yang dipakai supervisor untuk memutuskan penambahan orang,
dan angka tunggal tidak cukup ([VR] baris 251, LV14). Tata letak contoh: satu baris empat kotak
selebar layar, dengan kotak tunda berlabel teks dan bukan warna. Di bawahnya batang mendatar
tertumpuk yang menunjukkan porsi terlayani dan tertunda, karena panjang adalah kanal terbaik untuk
perbandingan bagian ([VR] baris 248, LV7).

**Dasar riset penyajian.** LV7 untuk panjang dan posisi; LV14 untuk larangan satu angka backlog;
LV17 dan LV18 untuk jangkar laju dan waktu per alarm dari EEMUA 191 edisi ketiga halaman 96 dan 97,
yang dipakai menetapkan orde besaran waktu per baris.

**Status bukti.** Aritmetika anggaran: sudah dihitung dari data nyata, keluaran di bagian 14.3 dan
14.4. Menit per pita: parameter desain, belum diukur pada operator. Beban per shift: terukur lewat
simulasi [H] dengan 20.000 undian dan seed tetap.

**Salah tafsir yang harus dicegah.**
1. Tunda nol dibaca sebagai tidak ada masalah. Pencegahan: bila jumlah masuk di bawah kapasitas,
   layar menulis "beban ringan", bukan "aman".
2. Menit dibaca sebagai durasi pasti. Pencegahan: label "perkiraan" dan sumber parameter ditampilkan
   pada tooltip.
3. Kekurangan menit dibaca sebagai kesalahan operator. Pencegahan: baris penjelasan bahwa angka itu
   hasil beban dibagi kapasitas, bukan penilaian kinerja.

**Cara menguji.**
1. Uji jadwal: sepuluh baris bagian 6.2 harus menghasilkan 9 terlayani, 0 ditunda, sisa 0 menit.
2. Uji pengaman: masukkan P4 ke tengah daftar dengan anggaran 5 menit, `A` harus naik otomatis.
3. Uji episode: hyd 20 sampai 24 harus dihitung 10 menit, bukan 30.
4. Uji neraca: jumlah terlayani ditambah jumlah ditunda harus sama dengan jumlah masuk.
5. Uji beban p95: dengan 61 baris dan `A` 30, tunda harus muncul sebagai angka, bukan nol.
### ANT-04 Episode dan umur item

**ID dan nama fitur.** ANT-04, "Episode dan umur item".

**Tujuan.** Mengubah deretan jendela beruntun menjadi satu kejadian yang diperiksa sekali, dan
mengukur berapa lama satu kejadian sudah menunggu. Masalah yang diselesaikan: tanpa episode, satu
gangguan 87 menit menjadi 87 baris, dan tanpa umur, baris yang sudah lama menggantung terlihat sama
dengan baris yang baru masuk.

**Menggambarkan apa.** Kesinambungan kejadian, bukan jumlah jendela. Bila panjang episode bertambah,
artinya kondisi berlangsung lebih lama. Bila umur bertambah tanpa keputusan, artinya beban kerja,
bukan bahaya. Bila jumlah episode naik sementara total jendela tetap, artinya kejadian makin sering
diputus-putus.

**Pengguna dan momen pakai.** Insinyur shift: setiap kali antrean disusun. Supervisor: saat serah
terima, untuk melihat mana yang sudah lama menggantung. Keduanya beberapa kali per shift.

**Masukan.** Indeks jendela aktif per kepala ([J] `contoh_idx_aktif`), dan `series.bins` dari [H] yang
memberi jumlah jendela per blok. Satuan: indeks jendela dan menit. Rentang: jarak antar jendela pada
contoh nyata 1 sampai 1.347 menit; panjang episode terukur sampai 87 jendela ([H] bin 65 hyd rule).
Cara memperoleh: selisih indeks, dengan asumsi satu indeks sama dengan satu menit bila jendela
berurutan ([J] baris 22).

**Algoritma.** Nama metode: pengelompokan berurutan dengan ambang jarak. Langkah: (1) urutkan indeks
aktif satu klaim; (2) bila jarak ke indeks sebelumnya tidak lebih dari 5 menit, gabungkan ke episode
yang sama; (3) bila lebih, buka episode baru; (4) umur episode sama dengan indeks sekarang dikurangi
indeks episode; (5) menit episode sama dengan menit pita ditambah 1 menit per jendela tambahan,
dibatasi 6 menit. Parameter: ambang 5 menit dan batas tambahan 6 menit. Alasan ambang: jarak pada
contoh nyata vib adalah 15, 28, 6, dan 11 ([J] baris 79 sampai 83), sehingga ambang 5 memisahkan
pasangan berjarak 6 dan menggabungkan yang benar-benar berurutan seperti hyd 20 sampai 24 dan stuck 8
sampai 12.

**Workflow.**
1. Ambil indeks aktif per klaim.
2. Urutkan dan kelompokkan dengan ambang 5 menit.
3. Hitung panjang tiap episode.
4. Hitung umur tiap episode terhadap jendela sekarang.
5. Tetapkan menit episode.
6. Tampilkan umur dalam empat pita (bagian 8.1 butir 2).
7. Kirim panjang episode dan umur ke ANT-02 sebagai kunci urut keempat.

**Keluaran.** `episode_id`, `jendela_awal`, `jendela_akhir`, `panjang_jendela`, `umur_menit`,
`menit_episode`. Satuan: indeks, menit, jumlah jendela. Rentang: panjang 1 sampai 87; umur 0 sampai
87 menit pada segmen hyd rule. Arti: panjang 5 berarti lima jendela berurutan, dan menit 10 berarti
satu pemeriksaan sepuluh menit, bukan lima pemeriksaan enam menit.

**Saran penyajian.** Kolom umur dengan empat pita pada tabel, plus satu batang kecil per episode yang
menunjukkan panjangnya. Alasan: umur adalah atribut yang paling sering hilang dari antrean, dan
sumber menyatakan sebaran umur lebih informatif daripada satu hitungan terbuka ([VR] baris 173,
LV14). Tata letak contoh: kolom umur selebar 90 piksel dengan teks "4 mnt" dan pita warna di kiri
sel; batang panjang episode selebar 60 piksel, diskalakan terhadap 87 jendela maksimum.

**Dasar riset penyajian.** LV14 lewat [VR] baris 173 dan 251; LV4 lewat [VR] baris 173 untuk kolom
pertama yang terbaca manusia. Bucket umur LV14 ber satuan hari dan diadaptasi ke menit, dan adaptasi
itu dicatat sebagai pilihan desain.

**Status bukti.** Pengelompokan: sudah diuji pada lima jendela hyd dan lima jendela stuck dari [J], dan
hasilnya di bagian 6.3. Umur: baru bisa dihitung sebagai selisih indeks, yang merupakan batas bawah
menit bila grid waktunya berlubang. Panjang episode maksimum 87: terukur dari [H] bin 65. Larik status
penuh per jendela belum diekspor, sehingga jumlah episode sesungguhnya per shift belum bisa dihitung.

**Salah tafsir yang harus dicegah.**
1. Episode panjang dibaca sebagai risiko naik. Pencegahan: label "panjang kejadian" dan pemisahan
   kolom panjang dari kolom pita.
2. Umur besar dibaca sebagai kelalaian. Pencegahan: umur ditampilkan bersama angka tunda pada neraca
   ANT-03, sehingga terbaca sebagai akibat kapasitas.
3. Episode digabung melintasi klaim berbeda. Pencegahan: episode hanya dihitung di dalam satu klaim
   dan satu segmen.

**Cara menguji.**
1. Uji batas: indeks dengan jarak 5 digabung, jarak 6 dipisah.
2. Uji contoh: hyd 20 sampai 24 harus menjadi satu episode dengan menit 10; stuck 8 sampai 12 menjadi
   satu episode dengan menit 8.
3. Uji umur: umur harus nol pada jendela pertama dan bertambah satu per jendela berurutan.
4. Uji lintas klaim: jendela 429 vib dan jendela yang sama pada klaim lain tidak boleh bergabung.

### ANT-05 Tiga keadaan antrean

**ID dan nama fitur.** ANT-05, "Tiga keadaan antrean": kosong, panjang, keyakinan rendah.

**Tujuan.** Menetapkan apa yang tampil dan apa yang tidak pada tiga situasi yang paling sering
disalahbaca. Masalah yang diselesaikan: antrean kosong terbaca aman, antrean panjang terbaca bahaya,
dan keyakinan rendah terbaca model rusak.

**Menggambarkan apa.** Keadaan sistem penyajian, bukan keadaan rig. Perpindahan dari kosong ke panjang
menggambarkan perubahan beban tinjauan. Perpindahan ke keyakinan rendah menggambarkan batas bukti kelas
yang bekerja, bukan penurunan mutu mendadak.

**Pengguna dan momen pakai.** Insinyur shift: setiap kali membuka layar. Supervisor: saat memutuskan
apakah perlu tambahan orang. Auditor: saat memeriksa apakah layar pernah menampilkan "aman" tanpa
dasar.

**Masukan.** Jumlah baris per pita, jumlah baris abstain, rasio kanal absen per klaim (`n_nodata`
dibagi `n_windows`), dan jumlah tunda dari ANT-03. Rentang: rasio kanal absen 0 sampai 0,9657
([J] baris 247). Satuan: jumlah baris dan rasio.

**Algoritma.** Nama metode: mesin keadaan dengan empat ambang. Aturannya:

```
jika tidak ada baris P3 dan P4            -> KOSONG
selain itu jika jumlah baris > kapasitas  -> PANJANG
selain itu jika lebih dari separuh baris berpita P2 atau abstain -> KEYAKINAN RENDAH
selain itu                                -> NORMAL
```

Parameter: ambang kapasitas dari ANT-03, ambang "separuh" 0,50, dan ambang kanal absen 0,50 dari
[DSS1] baris 244. Alasan memilih "separuh" untuk keadaan keyakinan rendah: bila mayoritas baris tidak
layak ditindak, pertanyaan pembaca berubah dari "mana yang penting" menjadi "apakah datanya cukup",
dan dua pertanyaan itu butuh tampilan berbeda.

**Workflow.**
1. Hitung jumlah baris per pita dan per status abstain.
2. Tentukan keadaan dengan urutan aturan di atas.
3. Terapkan perilaku tampilan keadaan itu (bagian 7).
4. Cetak label keadaan di kepala layar bersama jumlah baris.
5. Simpan label keadaan ke log harian, supaya bisa dihitung berapa persen shift berada di tiap
   keadaan.

**Keluaran.** Satu label keadaan dan empat angka pendukung. Satuan: kategori dan jumlah. Arti: label
PANJANG dengan tunda 30 berarti beban melebihi kapasitas pada shift itu; label KOSONG dengan rasio
kanal absen 0,9657 berarti tidak ada yang dinilai pada klaim itu, bukan rig tenang.

**Saran penyajian.** Satu garis status di kepala layar, teks dan angka, tanpa warna merah. Keadaan
KOSONG memakai teks abu, PANJANG memakai teks tebal dengan angka tunda, KEYAKINAN RENDAH memakai
pola garis miring pada blok pantau. Alasan: [K] baris 203 sampai 207 melarang warna tanpa label, dan
[DSS1] baris 250 memakai pola garis miring untuk abstain.

**Dasar riset penyajian.** LV14 lewat [VR] baris 251 untuk larangan satu angka backlog; LV4 lewat
[VR] baris 173 untuk keterbacaan label; aturan warna dari [K] baris 203 sampai 207 yang sudah dipakai
di [DSS1] bagian 4.2.

**Status bukti.** Pemicu: terukur, dengan contoh nyata untuk ketiga keadaan (ssi `n_aktif` 0 untuk
kosong, hyd bin 65 87 dari 87 untuk panjang, bit_wear 0,2525 dan ssi 0,9657 untuk keyakinan rendah).
Ambang: rancangan. Belum ada tangkapan layar, karena halaman belum dibangun.

**Salah tafsir yang harus dicegah.**
1. Kosong dikira aman. Pencegahan: label kanal wajib pada keadaan kosong.
2. Panjang dikira bahaya. Pencegahan: angka tunda ditampilkan bersama sebaran umur.
3. Keyakinan rendah dikira model rusak. Pencegahan: batas kelas tampil dan tanggal rujukannya
   disebut.

**Cara menguji.**
1. Uji ketiga keadaan dengan data sintetis: nol baris, 80 baris, dan 60 persen baris P2.
2. Uji ambang abstain: klaim dengan kanal absen 0,6 harus memunculkan label, 0,4 tidak.
3. Uji label harian: hitung persentase shift per keadaan pada data satu bulan.
4. Uji keterbacaan: tangkapan layar skala abu, ketiga keadaan harus tetap berbeda.

### ANT-06 Tutup baris dan catat keputusan

**ID dan nama fitur.** ANT-06, "Tutup baris dan catat keputusan". Padanan katalog: LIN-01 ([K] baris
2073).

**Tujuan.** Memberi setiap baris akhir yang tercatat, sehingga umur berhenti bertambah dan antrean
tidak menumpuk tanpa jejak. Masalah yang diselesaikan: tanpa penutupan, antrean hanya bisa bertambah,
dan tidak ada cara mengetahui apakah tinjauan pernah terjadi.

**Menggambarkan apa.** Jejak keputusan manusia. Bila baris ditutup dengan alasan "pantau", artinya
manusia sudah melihat dan memilih menunggu. Bila tidak ada penutupan, artinya baris belum dilihat,
dan itu berbeda dari "sudah diperiksa dan aman".

**Pengguna dan momen pakai.** Insinyur shift: setiap kali selesai memeriksa satu baris, 7 sampai 9 kali
per shift pada beban tengah. Supervisor: saat menutup baris yang ditunda melewati batas 15 menit.

**Masukan.** `id_baris`, `pita`, `K_tampil`, waktu buka, waktu tutup, label keputusan, dan catatan
bebas. Satuan: waktu dan kategori. Rentang label: `konfirmasi lapangan`, `periksa kanal`, `pantau`,
`tutup tanpa tindakan`, `eskalasi`. Waktu buka dan tutup dipakai menghitung menit sesungguhnya,
sehingga parameter 5.1 bisa diukur kelak.

**Algoritma.** Nama metode: transisi keadaan sederhana dengan empat keadaan baris: `baru`, `dibuka`,
`ditutup`, `ditunda`. Aturan: baris hanya bisa ditutup bila label keputusan terisi; penutupan mencatat
selisih waktu buka dan tutup sebagai `menit_nyata`; `menit_nyata` tidak dipakai mengubah urutan pada
shift berjalan, hanya dipakai sebagai bahan kalibrasi parameter. Alasan: mengubah urutan dengan data
yang sedang dikumpulkan akan membuat aturan berubah di tengah shift dan tidak dapat diaudit.

**Workflow.**
1. Baris masuk dengan keadaan `baru`.
2. Insinyur membuka baris, keadaan menjadi `dibuka`, waktu buka dicatat.
3. Insinyur memilih label dan menulis catatan.
4. Baris ditutup, keadaan menjadi `ditutup`, `menit_nyata` dicatat.
5. Bila baris tidak muat anggaran, keadaan menjadi `ditunda`, tanpa waktu buka.
6. Log ditulis ke berkas harian dan diringkas per shift.
7. Ringkasan dipakai ANT-03 untuk membandingkan anggaran dengan waktu sesungguhnya.

**Keluaran.** Satu record per transisi: `id_baris`, keadaan lama, keadaan baru, waktu, aktor, label,
catatan. Satuan: waktu dan kategori. Rentang: 0 sampai 15 menit per baris menurut anggaran, dan angka
sesungguhnya akan mengoreksi parameter itu. Arti: rasio `menit_nyata` terhadap menit parameter adalah
faktor koreksi yang dipakai pada revisi berikutnya.

**Saran penyajian.** Linimasa per baris pada halaman detail, dan ringkasan harian berupa tabel waktu
tutup per pita. Alasan: [VR] baris 236 menyebut linimasa vertikal berurut waktu dengan kolom aktor
dan keputusan untuk jejak keputusan (LV16, LV11). Tata letak contoh: kolom kiri waktu 60 piksel,
kolom tengah aktor dan label, kolom kanan catatan.

**Dasar riset penyajian.** LV16 dan LV11 lewat [VR] baris 236, yang menyebut linimasa postmortem
sebagai bentuk lazim jejak keputusan.

**Status bukti.** Rancangan. Belum ada log keputusan di repo, dan [K] baris 2073 menyebut LIN-01 baru
berstatus siap sebagian. Parameter menit pada 5.1 adalah pengganti sementara sampai log ini berjalan.

**Salah tafsir yang harus dicegah.**
1. Baris tanpa jejak dikira aman. Pencegahan: keadaan baris selalu tampil, dan baris `baru` tidak
   pernah berwarna hijau.
2. `menit_nyata` dipakai menilai kinerja orang. Pencegahan: kolom aktor dipakai untuk audit, bukan
   untuk peringkat, dan itu ditulis di layar.
3. Penutupan massal tanpa membaca. Pencegahan: tombol tutup hanya aktif setelah baris dibuka minimal
   tiga detik, dan catatan wajib untuk label `konfirmasi lapangan`.

**Cara menguji.**
1. Uji transisi: baris tidak dapat ditutup tanpa label.
2. Uji waktu: `menit_nyata` sama dengan selisih waktu buka dan tutup.
3. Uji agregasi: jumlah baris ditutup per shift sama dengan jumlah terlayani pada ANT-03.
4. Uji koreksi: setelah 30 shift, median `menit_nyata` per pita dibandingkan dengan 6, 4, dan 2 menit.

### ANT-07 Penanda interval keyakinan baris

**ID dan nama fitur.** ANT-07, "Penanda interval keyakinan baris".

**Tujuan.** Menampilkan apa yang belum diketahui tentang satu baris, bukan menyembunyikannya di balik
satu angka. Masalah yang diselesaikan: skor tunggal membuat kepala yang tidak dievaluasi terlihat
seolah setuju.

**Menggambarkan apa.** Kelengkapan bukti pada satu jendela. Bila `K_up` berbeda pita dengan `K_min`,
artinya satu kepala belum dievaluasi dan hasilnya bisa berubah bila kepala itu dinilai. Bila keduanya
sama, artinya seluruh kepala sudah pasti, dan baris tidak punya ketidakpastian penilaian.

**Pengguna dan momen pakai.** Insinyur shift: saat memutuskan apakah perlu membuka kanal tambahan.
Auditor: saat memeriksa apakah angka baris bisa dipertanggungjawabkan. Masing-masing beberapa kali per
shift dan sekali per bulan.

**Masukan.** `contoh_idx_aktif` per kepala ([J]), bobot kepala ([DSS1] baris 111 sampai 138), dan
definisi hibrida ([J] baris 833). Satuan: rasio. Rentang: `K_up` sampai 1,0000 sebelum pemotongan,
dan selisih `K_up` dikurangi `K_min` 0 sampai 0,6667 pada contoh bagian 6.2 baris 7.

**Algoritma.** Nama metode: perhitungan dua batas dengan aturan turunan status. Langkah: (1) tandai
kepala pasti menyala, pasti mati, belum pasti; (2) `K_min` menjumlah bobot yang pasti menyala; (3)
`K_up` menjumlah bobot yang menyala atau belum pasti; (4) bagi keduanya dengan jumlah bobot klaim;
(5) potong keduanya dengan batas kelas; (6) bandingkan pita. Parameter: hanya bobot dan batas kelas
dari [DSS1]. Alasan memilih dua batas dan bukan satu angka: kepala yang belum dievaluasi bukan nol,
dan [DSS1] baris 64 sampai 70 sudah menetapkan aturan bahwa kepala tidak tersedia bukan skor nol.

**Workflow.**
1. Baca daftar indeks aktif per kepala.
2. Terapkan tiga aturan turunan bagian 6.1.
3. Hitung dua batas dan potong dengan batas kelas.
4. Bandingkan pita kedua batas.
5. Bila berbeda, tampilkan rentang dan sebut kepala yang belum pasti.
6. Bila sama, tampilkan satu angka dan tulis "seluruh kepala dinilai".

**Keluaran.** `K_min`, `K_up`, `pita_bawah`, `pita_atas`, `kepala_belum_pasti`. Satuan: rasio dan
kategori. Arti: `K_min` 0,3333 dengan `K_up` 1,0000 pada stuck K-ii jendela 30.122 berarti baris itu
pasti P2 dan bisa menjadi P3 bila `rf_lowo` dan `e1_2of3` ternyata menyala.

**Saran penyajian.** Batang mendatar dengan dua tanda: satu garis penuh pada `K_min` dan satu garis
putus pada `K_up`, dengan garis batas kelas. Alasan: panjang dan posisi adalah kanal terbaik untuk
besaran dan selisih ([VR] baris 248, LV7), sedangkan dua angka berdampingan tanpa gambar sulit
dibandingkan pada layar kecil. Tata letak contoh: batang 200 piksel, garis penuh di 33 persen, garis
putus di 46 persen (setelah pemotongan), label "P2, batas atas P3" di kanan.

**Dasar riset penyajian.** LV7 lewat [VR] baris 248 dan baris 13; LV5 lewat [VR] baris 246, yang menolak satu angka
keyakinan tanpa sebaran atau interval; [DSS1] bagian 7.5 memakai batang dan garis batas kelas untuk
alasan yang sama.

**Status bukti.** Sudah dihitung dari data nyata untuk sepuluh baris bagian 6.2. Belum: larik status
penuh per jendela, sehingga baris di luar lima indeks contoh belum bisa dihitung dua batasnya.

**Salah tafsir yang harus dicegah.**
1. `K_up` dibaca sebagai keyakinan sebenarnya. Pencegahan: garis putus diberi label "batas atas, belum
   dinilai".
2. Interval lebar dibaca sebagai model buruk. Pencegahan: sebut kepala mana yang belum pasti dan
   mengapa, misalnya "hanya lima indeks contoh yang tersimpan".
3. Baris dengan interval dianggap tidak layak ditampilkan. Pencegahan: baris tetap tampil dengan pita
   bawah, dan pita atas hanya sebagai keterangan.

**Cara menguji.**
1. Uji turunan: hyd jendela 20 harus memberi `K_min` sama dengan `K_up` sama dengan 1,0000 sebelum
   pemotongan.
2. Uji interval: stuck K-ii jendela 30.122 harus memberi 0,3333 sampai 1,0000.
3. Uji pemotongan: vib jendela 429 harus mentok di 0,4950 pada kedua batas.
4. Uji konsistensi: `K_min` tidak boleh lebih besar daripada `K_up` pada semua baris.
## 10. Hubungan dengan katalog fitur yang sudah ada

Empat fitur katalog sudah menutup sebagian medan ini, dan dokumen ini tidak menggantikannya. Yang
ditambahkan adalah aturan pemotongan anggaran dan aturan urutan berlapis, karena katalog belum
memuat keduanya.

| Fitur katalog | Isi yang sudah ada | Yang ditambahkan dokumen ini |
|---|---|---|
| MNT-01 ([K] baris 871) | antrean triage onset per shift dengan umur item; pengguna, momen pakai, dan label cakupan | kunci urutan berlapis enam tingkat (bagian 4.1), dan larangan memakai FAR mentah sebagai kunci (bagian 4.3) |
| MNT-02 ([K] baris 940) | kalkulator anggaran pemeriksaan; menit per baris sebagai parameter | algoritma greedy dengan jatah minimum per klaim dan pengaman P4 (bagian 5.2), plus neraca penundaan wajib (bagian 5.5) |
| MNT-05 ([K] baris 1099) | pembagian FAR per 24 jam menjadi tinjauan per shift, dengan perintah "jumlahkan per peran, bukan per head" ([K] baris 1113) | penerapan perintah itu secara eksplisit: aturan dedup rule dan hibrida (bagian 2.3), dan label satuan per baris |
| LIN-01 ([K] baris 2073) | log keputusan | transisi keadaan baris dan pemakaian `menit_nyata` sebagai bahan kalibrasi parameter, bukan pengubah urutan shift berjalan (ANT-06) |

Satu angka di MNT-05 perlu dibaca hati-hati dan dokumen ini menyelesaikannya. [K] baris 1113 menulis
"jumlahkan per peran, bukan per head", sedangkan [ENG] baris 33 sampai 42 mendaftar sepuluh head
termasuk rule dan hibrida untuk mesin yang sama. Menjumlahkan seluruh head memberi vib 34 dan hyd 25,
sedangkan menjumlahkan per peran setelah dedup memberi vib 17 dan hyd 19. Angka 40,15 baris per shift
pada bagian 2.4 memakai cara kedua, sesuai perintah MNT-05. Bila pembaca memakai cara pertama, beban
menjadi 40,15 ditambah 17 ditambah 6 sama dengan 63,15 baris per shift, dan itu menghitung jendela
yang sama dua kali.

## 11. Ringkasan tujuh fitur

| Kode | Nama | Pengguna utama | Momen pakai | Masukan | Keluaran | Status bukti |
|---|---|---|---|---|---|---|
| ANT-01 | Baris antrean tinjauan | insinyur shift, toolpusher | awal shift, tiap dua jam | [J], [H], bobot dan batas [DSS1] | 14 kolom per baris | sebagian terhitung dari data nyata |
| ANT-02 | Peringkat berlapis | insinyur shift, supervisor | tiap penyusunan antrean | pita, keyakinan, umur, lead | urutan plus kunci penentu | rancangan, diuji pada 10 baris |
| ANT-03 | Anggaran waktu dan neraca | supervisor, perencana tenaga kerja | sekali per shift, sekali per minggu | menit per pita, anggaran A | 4 angka dan 2 daftar | aritmetika terhitung, parameter desain |
| ANT-04 | Episode dan umur item | insinyur shift, supervisor | tiap penyusunan, saat serah terima | indeks aktif, bins [H] | episode, umur, menit episode | pengelompokan diuji, umur batas bawah |
| ANT-05 | Tiga keadaan antrean | insinyur, supervisor, auditor | tiap membuka layar | jumlah per pita, rasio kanal absen | label keadaan dan 4 angka | pemicu terukur, ambang rancangan |
| ANT-06 | Tutup baris dan log keputusan | insinyur shift, supervisor | tiap baris selesai | id baris, label, waktu | record transisi | rancangan, log belum ada |
| ANT-07 | Penanda interval keyakinan | insinyur, auditor | saat butuh kanal tambahan | contoh indeks, bobot | dua batas dan dua pita | terhitung untuk 10 baris |

## 12. Syarat yang dibutuhkan agar seluruh angka bisa diukur

Tiap butir ditulis sebagai syarat, bukan sebagai keberatan. Kolom pemilik menyebut siapa yang
memegang datanya, dan kolom cara menyebut bentuk berkas yang dibutuhkan.

| Syarat | Dipakai untuk | Bentuk yang dibutuhkan | Pemilik data |
|---|---|---|---|
| Larik status penuh per jendela, bukan lima indeks contoh | menghitung ANT-07 untuk semua baris, dan menghitung jumlah episode sesungguhnya | matriks `klaim` x `jendela` berisi 0 atau 1 per kepala, atau daftar indeks penuh per kepala | pemilik `code/v9_i1_pipeline.py`, karena `active` sudah ada di memori pada baris 384 dan hanya dipotong menjadi lima |
| Larik `ts` per jendela | mengubah umur dari selisih indeks menjadi menit kalender | kolom `ts_bin` per jendela dengan satuan menit dan asal kalender | pemilik `code/v9_i1_pipeline.py` |
| Pemetaan jendela ke sumur | mengganti kolom `segmen` dari satu nilai menjadi sumur per baris | tabel `segmen, jendela_awal, jendela_akhir, sumur` | pemilik data D1, karena [J] hanya memberi segmen per engine |
| Pengukuran menit per pita pada operator nyata | mengganti parameter 6, 4, dan 2 menit dengan angka terukur | durasi 30 pemeriksaan per pita, dicatat ANT-06 | supervisor operasi, lewat log ANT-06 |
| Kalibrasi satuan tool_wear | memastikan 1 atau 1.006 tinjauan per shift | pernyataan resmi satuan `far_segmen` untuk head itu, plus panjang jendela | pemilik `E_STAT` bagian C, karena [J] baris 1077 menulis satuan per menit sedangkan [ENG] baris 43 membaginya tiga |

Satu catatan mengenai butir pertama: `contoh_idx_aktif` hari ini berisi lima elemen karena dipotong
saat ekspor, bukan karena hanya lima jendela yang aktif. Buktinya `n_aktif` untuk vib rule 540 dari 1.989 jendela ([J] baris 77 dan 78), sedangkan
daftar contohnya lima angka. Contoh kedua: bit_wear persistence 4.917 dari 47.645 jendela, dan
daftar contohnya juga lima angka. Artinya larik penuh ada di
hulu dan hanya tidak diekspor. Ini yang membuat ANT-07 bisa dinaikkan dari sepuluh baris contoh
menjadi seluruh baris tanpa mengubah model apa pun.

## 13. Yang belum diverifikasi, ditulis terbuka

Daftar ini bukan catatan kaki. Setiap butir menyebut apa yang bisa dan apa yang belum bisa diklaim
dengan angka yang ada hari ini.

1. Menit per pita 6, 4, dan 2 adalah parameter desain. Belum ada satu pun pengukuran durasi
   pemeriksaan pada operator. Yang bisa diklaim: jadwal bagian 6.4 konsisten secara aritmetika. Yang
   belum: jadwal itu cocok dengan kecepatan manusia.
2. Umur item dihitung dari selisih indeks jendela, sehingga merupakan batas bawah menit bila grid
   waktunya berlubang. [J] baris 22 menulis asal kalender `ts_bin` belum diverifikasi.
3. Peta sumur per jendela belum ada. Seluruh baris bagian 6.2 berasal dari segmen F-14, dan tidak ada
   klaim bahwa satu baris milik sumur tertentu.
4. Status kepala di luar lima indeks contoh tidak dapat dipastikan. Sepuluh baris bagian 6.2 dipilih
   supaya statusnya pasti atau berinterval jelas; baris lain belum punya perlakuan yang sama.
5. Satuan tool_wear belum selaras antara tiga sumber (bagian 2.3). Angka 1.006,08 per shift bisa
   benar atau bisa salah bergantung satuan, dan dokumen ini tidak menyelesaikannya.
6. Angka 40,15 baris per shift berasal dari simulasi Poisson [H] dengan `n_draw` 20.000 dan seed tetap,
   bukan dari hitungan kejadian nyata. Bila FAR segmen berubah, angka ini berubah.
7. Kebenaran pita P1 sampai P5 diambil dari [DSS1] apa adanya dan tidak diuji ulang di sini.
8. Seluruh baris belum pernah dirender di layar. Bentuk tabel bagian 8.1 adalah gambar dalam teks,
   bukan tangkapan layar.
9. Rujukan LV17, LV18, dan LV19 adalah dokumen baru yang dibuka pada 2026-10-31 dan bukan bagian dari
   daftar [VR]. Kutipan EEMUA 191 edisi ketiga halaman 96 diambil dari LV17 halaman 3, bukan dari
   berkas EEMUA langsung, karena berkas aslinya berbayar.

## 14. Lampiran keluaran perintah

Seluruh keluaran di bawah adalah salinan apa adanya dari perintah yang dijalankan pada 2026-10-31 di
`/mnt/d/Capstone 1(v2)`. Skrip pemeriksa ditulis di luar `planning/` dan bukan deliverable.

### 14.1 Ukuran berkas masukan

```
$ python3 dss2_verify.py   (bagian ukuran berkas)
J        57555 byte    1759 baris  scratch/v9_i1/v9_i1_RESULTS.json
H       456685 byte   31946 baris  dashboard/data/head_pages.json
K       166662 byte    2780 baris  planning/01_KATALOG_FITUR.md
VR       32141 byte     335 baris  planning/02_RISET_VISUALISASI.md
S6       40271 byte     437 baris  docs/RND_S6_PM_WAVE2.md
ENG       3915 byte      76 baris  docs/RND_ENGINE_S6_INTEGRATION.md
DSS1     66698 byte    1060 baris  planning/03_SKOR_KEYAKINAN.md
P        44359 byte     861 baris  code/v9_i1_pipeline.py
L       471945 byte    3434 baris  docs/RND_PROVENANCE_LEDGER.md
```

### 14.2 Pemeriksaan pembagian FAR per 24 jam dengan tiga, dibulatkan ke atas

```
vib rule_display               49.942 / 3 = 16.6473  ceil =  17
vib hibrida                    49.942 / 3 = 16.6473  ceil =  17
ssi rule_display                0.000 / 3 =  0.0000  ceil =   0
ssi hibrida                     0.000 / 3 =  0.0000  ceil =   0
shk rule_display                6.618 / 3 =  2.2060  ceil =   3
shk hibrida                     6.618 / 3 =  2.2060  ceil =   3
stuck rule_display              8.321 / 3 =  2.7737  ceil =   3
stuck hibrida                   8.321 / 3 =  2.7737  ceil =   3
hyd rule_display               55.570 / 3 = 18.5233  ceil =  19
hyd hibrida                    16.611 / 3 =  5.5370  ceil =   6
tool_wear op_far_calibrated     2.096 / 3 =  0.6987  ceil =   1
```

### 14.3 Beban per shift setelah dedup dan ekor Poisson

```
lambda vib               16.647
lambda shk                2.206
lambda stuck K-i          2.774
lambda hyd K-i (rule)    18.523
lambda total             40.150  (dibulatkan 2 desimal: 40.15)
p50 per klaim: 16 + 2 + 3 + 18 = 39
p95 per klaim: 24 + 5 + 6 + 26 = 61
ekor Poisson P(N >= k) dengan lambda total:
  P(N >=  20) = 0.9998
  P(N >=  30) = 0.9588
  P(N >=  40) = 0.5305
  P(N >=  50) = 0.0737
  P(N >=  61) = 0.0013
  P(N >=  70) = 0.0000
```

### 14.4 Aritmetika anggaran waktu

```
30 / 480            = 0.0625  (6.25 persen)
480 / 39            = 12.31 menit per baris
39 x 10 / 480       = 81.25 persen (390 menit)
30 / 4              = 7.50 baris
7 / 39              = 17.95 persen
kekurangan pada p95: (61 - 9) x 4 = 208 menit
tabel anggaran memakai baris utuh (kapasitas dibulatkan ke bawah dari A/4):
  A= 15 menit ->  3 baris utuh, cakupan dari 39:  7.69 persen, dari 61:  4.92 persen
  A= 30 menit ->  7 baris utuh, cakupan dari 39: 17.95 persen, dari 61: 11.48 persen
  A= 45 menit -> 11 baris utuh, cakupan dari 39: 28.21 persen, dari 61: 18.03 persen
  A= 60 menit -> 15 baris utuh, cakupan dari 39: 38.46 persen, dari 61: 24.59 persen
  A=120 menit -> 30 baris utuh, cakupan dari 39: 76.92 persen, dari 61: 49.18 persen
delapan klaim x 4 menit = 32 menit
episode hyd 20-24 dengan pita P4: 6 + 4 x 1 = 10
episode stuck 8-12 dengan pita P3: 4 + 4 x 1 = 8
tanpa episode hyd 5 x 6 = 30 menit; stuck 5 x 4 = 20 menit
```

### 14.5 Tabel kepala dari [J], bukti bahwa lima indeks contoh bukan lima jendela aktif

```
$ python3 dss2_heads.py
engine     head                             layer  n_win  n_akt       far far_unit                           contoh
vib        rule_display                     L1      1989    540    49.942 FP/24jam-negatif (jendela 60 dtk)  [429, 444, 472, 478, 489]
vib        persistence                      L0      1989   1142   316.301 FP/24jam-negatif (jendela 60 dtk)  [382, 383, 384, 385, 386]
vib        hybrid_rule_and_persistence      L1      1989    540    49.942 FP/24jam-negatif (jendela 60 dtk)  [429, 444, 472, 478, 489]
vib        rf_lowo                          L2      1989   1271   496.092 FP/24jam-negatif (jendela 60 dtk)  [517, 518, 519, 520, 521]
ssi        rule_display                     L1      5455      0     0.000 FP/24jam-negatif (jendela 60 dtk)  []
ssi        persistence                      L0      5455     31     8.030 FP/24jam-negatif (jendela 60 dtk)  [118, 119, 120, 303, 304]
ssi        hybrid_rule_and_persistence      L1      5455      0     0.000 FP/24jam-negatif (jendela 60 dtk)  []
ssi        rf_lowo                          L2      5455      0     0.000 FP/24jam-negatif (jendela 60 dtk)  []
shk        rule_display                     L1     11205    103     6.618 FP/24jam-negatif (jendela 60 dtk)  [20, 112, 115, 216, 2124]
shk        persistence                      L0     11205    623    54.043 FP/24jam-negatif (jendela 60 dtk)  [20, 21, 22, 23, 24]
shk        hybrid_rule_and_persistence      L1     11205    103     6.618 FP/24jam-negatif (jendela 60 dtk)  [20, 112, 115, 216, 2124]
shk        rf_lowo                          L2     11205      0     0.000 FP/24jam-negatif (jendela 60 dtk)  []
stuck      rule_display                     L1      3201    210     8.321 FP/24jam-negatif (jendela 60 dtk)  [8, 9, 10, 11, 12]
stuck      persistence                      L0      3201    451    75.406 FP/24jam-negatif (jendela 60 dtk)  [0, 1, 2, 3, 4]
stuck      hybrid_rule_and_persistence      L1      3201    210     8.321 FP/24jam-negatif (jendela 60 dtk)  [8, 9, 10, 11, 12]
stuck      e1_2of3                          L2     95925    313     4.627 FP/24jam-negatif (jendela 60 dtk)  [3560, 3561, 3562, 3563, 3564]
stuck      persistence_event                L2     95925      4     0.030 FP/24jam-negatif (jendela 60 dtk)  [30122, 30126, 31473, 34343]
stuck      rf_lowo                          L2     95925     42     0.603 FP/24jam-negatif (jendela 60 dtk)  [17582, 17912, 18061, 30316, 30317]
hyd        rule_display                     L1     10401    975    55.570 FP/24jam-negatif (jendela 60 dtk)  [0, 1, 2, 3, 4]
hyd        persistence                      L0     10401    876    48.775 FP/24jam-negatif (jendela 60 dtk)  [20, 21, 22, 23, 24]
hyd        hybrid_rule_and_persistence      L1     10401    626    16.611 FP/24jam-negatif (jendela 60 dtk)  [20, 21, 22, 23, 24]
hyd        k2_tidak_tersedia                L3         0      0       nan                                    []
bit_wear   persistence                      L2     47645   4917     1.213 FP/24jam-negatif (jendela 60 dtk)  [29120, 29121, 29122, 29123, 29124]
bit_wear   k2_onset_belum                   L3         0      0       nan                                    []
tool_wear  calib_5of27                      L2       469    305    34.585 FP/menit-negatif (jendela 1 dtk)   [19, 20, 21, 22, 23]
tool_wear  op_far_calibrated                L1       469     21     2.096 FP/menit-negatif (jendela 1 dtk)   [42, 95, 99, 154, 158]
tool_wear  canary_3rms                      L2       469    282       nan                                    [23, 26, 27, 28, 29]
```

Dua hal yang terbaca langsung dari tabel ini dan dipakai di badan dokumen: `tool_wear` memang
memakai satuan `FP/menit-negatif` dengan jendela 1 detik, berbeda dari semua kepala lain yang memakai
`FP/24jam-negatif` dengan jendela 60 detik; dan `contoh_idx_aktif` selalu lima angka walau `n_aktif`
mencapai 4.917, sehingga daftar itu memang potongan ekspor.

### 14.6 Pemeriksaan berkas ini

```
$ wc -c -l planning/04_ANTREAN_TINJAUAN.md
 1428 95168 planning/04_ANTREAN_TINJAUAN.md
baris berpipa: 156   (hitungan mentah grep, termasuk 10 baris gambar tata letak di dalam blok kode)
baris berpipa di luar blok kode: 146, baris pemisah: 15, baris data tabel: 131, tabel markdown: 15
pisah panjang: 0
pisah sedang: 0
kata larangan: 0
berkas non-md di planning: 0
judul bagian: 16
judul fitur: 38
```

Pemeriksaan di atas dijalankan pada berkas ini sendiri setelah seluruh isi selesai ditulis. Dua angka
terakhir menghitung subjudul tingkat dua dan tingkat tiga, bukan jumlah fitur, karena setiap fitur
memakai beberapa subjudul di dalamnya.

### 14.7 Koreksi yang dilakukan setelah pemeriksaan

Pemeriksaan ini menemukan tujuh angka yang salah pada draf dan semuanya sudah diperbaiki. Daftarnya
ditulis supaya pembaca bisa memeriksa sendiri hasil akhirnya.

1. Ukuran baris berkas [J] 1.759 dan [H] 31.946, bukan 1.758 dan 31.945.
2. Ukuran baris [L] adalah 3.434, bukan 39.252. Angka 39.252 adalah ukuran kata, bukan baris.
3. Nomor baris batas kelas di [DSS1] adalah 170 sampai 177, bukan 374 sampai 395.
4. Nomor baris bobot kepala per klaim di [DSS1] adalah 111 sampai 138, bukan 118 sampai 143.
5. Nomor baris tabel pita di [DSS1] adalah 219 sampai 225, dan tabel abstain 240 sampai 246.
6. Cakupan anggaran pada tabel 5.4 dihitung dari baris utuh, sehingga A sama dengan 30 menit memberi
   17,95 persen terhadap 39 baris, bukan 19,23 persen.
7. `n_aktif` vib rule adalah 540 dari 1.989 jendela ([J] baris 77 dan 78). Angka 4.917 dari 47.645
   adalah milik bit_wear persistence, dan itu dipakai sebagai contoh kedua pada bagian 12.
8. Rujukan LV5 di [VR] adalah baris 246, bukan 242; rujukan LV7 ada di baris 13 dan 248.
9. Lead hanya tersedia untuk hyd, 8,0 menit ([J] baris 809 dan 1571 sampai 1577). Draf semula
   menulis lead 7,0 menit untuk stuck K-ii, dan angka itu tidak ada di [J]. Baris 6 pada bagian 6.2
   kini berbunyi "tidak ada lead", dan tabel bagian 3 hanya mencantumkan 8,0 menit.

## 15. Penutup yang bisa diperiksa

Antrean ini punya empat bagian yang bisa diuji terpisah: muatan baris (bagian 3), urutan (bagian 4),
anggaran (bagian 5), dan penyajian (bagian 8). Setiap bagian punya uji sendiri di butir "Cara menguji"
pada fitur terkait, dan setiap angka di dalamnya menunjuk berkas serta baris.

Tiga angka yang paling menentukan sudah dihitung dari data nyata: beban 40,15 baris per shift, nilai
tengah 39, dan persentil 95 sebesar 61. Tiga parameter yang belum diukur sudah dinyatakan sebagai
parameter: menit per pita, pemetaan sumur, dan larik status penuh per jendela. Syarat untuk menutup
ketiganya ada di bagian 12 beserta pemilik datanya.

Keputusan akhir tetap pada insinyur pengeboran, sesuai [J] baris 1415 dan [J] baris 1758. Dokumen ini
tidak menambah satu pun jalur yang memicu tindakan tanpa manusia.
