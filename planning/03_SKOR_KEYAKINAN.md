# 03 SPESIFIKASI SKOR KEYAKINAN DAN KALIBRASI (DSS-1)

Kartu: `t_845ead46` (DSS-1). Board: `fitur-v9-swarm`. Tanggal: 2026-10-31 (WIB).
Workspace: `/mnt/d/Capstone 1(v2)`. Keluaran: berkas ini saja, di folder `planning/`.

Dokumen ini menetapkan satu skala keyakinan 0 sampai 1 untuk keluaran tujuh engine, lima pita
keyakinan dengan tindakan per pita, satu pita abstain, cara menghitung kurva reliabilitas dan ECE,
serta penyajiannya di layar. Skala ini alat bantu membaca bukti, bukan pemutus tindakan. Tidak ada
model yang dijalankan ulang di sini. Seluruh angka masuk diambil dari berkas yang sudah ada, dan
setiap angka membawa kode berkas serta nomor baris.

## 0. Kepatuhan kerangka wajib

| Butir kerangka | Cara dipenuhi di dokumen ini |
|---|---|
| 1. Alarm otomatis bukan tujuan | Skor 0 sampai 1 berhenti di pita tindakan manusia. Pita tertinggi pun berbunyi "eskalasi ke supervisor", dan seluruh tampilan memakai komponen `human_review_required` yang di berkas [J] baris 1757 bernilai `true`. Tidak ada tombol kirim alarm. |
| 2. Setiap angka bersumber | Seluruh angka proyek memakai kode berkas [J], [P], [K], [VR], [EVA], [EVC], [PM1], [I2], [I4], [L] beserta nomor baris. Angka literatur memakai kode [LV1] sampai [LV16] yang daftarnya ada di [VR] bagian 9. |
| 3. Tidak ada klaim tanpa bukti | Bagian 1 memuat ukuran byte tiap berkas yang dibuka. Bagian 10 menempelkan keluaran perintah yang dipakai memeriksa angka dan memeriksa berkas ini. |
| 4. Kekurangan data jadi fitur | Pita abstain (bagian 4.2) dan slot "3 dari 4 kepala" pada contoh E3 (bagian 6) mengubah data yang tidak ada menjadi informasi yang terbaca, bukan keluhan. |
| 5. Lima field wajib per fitur | Setiap butir di bagian 7 memuat pengguna, momen pakai, masukan, keluaran, dan status bukti, ditambah delapan field lain sesuai format kartu. |
| 6. Tidak menutup dengan kalimat menyerah | Bagian 11 menuliskan syarat yang dibutuhkan beserta pemilik datanya. |
| 7. Hanya markdown di `planning/` | Satu berkas keluaran, yaitu berkas ini. |
| 8. Tanpa tanda pisah panjang | Diperiksa pada bagian 10 dengan dua perintah `grep`, keduanya mengeluarkan 0. |

Catatan notasi: keluaran alat di dokumen ini memakai titik desimal (format `awk`), sedangkan teks
memakai koma desimal mengikuti gaya dokumen proyek lain. Keduanya angka yang sama.

## 1. Berkas masukan, ukuran byte, dan cara dibuka

Ukuran diambil dengan `stat -c '%s'` dan `wc -l` pada 2026-10-31. Keluaran mentahnya ada di bagian 10.

| Kode | Berkas | Byte | Baris | Cara dibuka |
|---|---|---:|---:|---|
| [J] | `scratch/v9_i1/v9_i1_RESULTS.json` | 57.555 | 1.759 | dibaca penuh, baris 1 sampai 1.759 |
| [P] | `code/v9_i1_pipeline.py` | 44.359 | 861 | dibaca penuh |
| [K] | `planning/01_KATALOG_FITUR.md` | 166.662 | 2.780 | dibaca baris 1 sampai 500, sisanya lewat pencarian judul |
| [VR] | `planning/02_RISET_VISUALISASI.md` | 32.141 | 335 | dibaca penuh |
| [EVA] | `docs/V9_EVAL_A_LAYERA.md` | 32.713 | 315 | dibaca penuh |
| [EVC] | `docs/V9_EVAL_C_LAYERC.md` | 23.153 | 267 | dibaca penuh |
| [PM1] | `docs/V9_PM1_ARCHITECTURE.md` | 50.456 | 528 | hanya lewat pencarian baris 128 sampai 132, 234, 268, 357, 365, 371, 399 |
| [I2] | `planning/00_INVENTARIS_V7_V8.md` | 39.059 | 589 | dibaca baris 136 sampai 195, sisanya lewat pencarian |
| [I4] | `planning/00_INVENTARIS_RND2_V11.md` | 35.536 | 412 | dibaca baris 228 sampai 267, sisanya lewat pencarian |
| [L] | `docs/RND_PROVENANCE_LEDGER.md` | 471.945 | 3.434 | hanya lewat pencarian baris `L-18` sampai `L-39` dan kata kunci kalibrasi |

Berkas [PM1] dan [L] tidak dibaca penuh. Kutipan dari keduanya dibatasi pada baris yang benar-benar
dibuka, dan hal ini dicatat lagi di bagian 12.

## 2. Struktur JSON: kunci yang benar-benar ada

Berkas [J] punya delapan kunci tingkat atas. Ini hasil `grep -n '^  "[a-z_]*":'` di bagian 10.

| Kunci | Baris | Isi |
|---|---:|---|
| `meta` | 2 | task, segmen rig F-14, jumlah jendela, seed 42, `n_engine` 7 (baris 14) |
| `segmen_info` | 16 | enam segmen: vib, ssi, shk, stuck_k1, stuck_k2, hyd_ki, masing-masing dengan `n`, `ts_bin_min`, `ts_bin_max` |
| `engines` | 60 | tujuh blok engine, 27 entri kepala seluruhnya (dihitung di bagian 10) |
| `decision_layer` | 1.153 | `layers.L0` 5 entri, `L1` 11, `L2` 9, `L3` 2, ditambah `ringkasan` (baris 1.407) dan `auto_critical_alarm_slots` 0 (baris 1.414) |
| `profil_kapabilitas` | 1.417 | tujuh profil, tiap profil memuat `lapisan_A_deteksi`, `lapisan_B_nilai_maintenance`, `lapisan_C_ketepatan`, dan `kekuatan_bukti` (nilai `SEDANG` di baris 1.451 sampai 1.599, `LEMAH` di baris 1.630) |
| `nilai_maintenance` | 1.665 | jam henti DDR dan `beban_tinjauan_L1` 11 baris (baris 1.687 sampai 1.754) |
| `human_review_required` | 1.757 | `true` |
| `keputusan_akhir` | 1.758 | "MANUSIA", alat menyiapkan status dan bahan rencana inspeksi |

Kunci di dalam satu entri kepala yang tersedia dan dipakai dokumen ini: `head`, `klaim`, `tier`,
`layer`, `badge_far`, `keyakinan`, `batas_pemakaian`, `human_review_required`, `n_windows`,
`n_aktif`, `frac_aktif`, `contoh_idx_aktif`, `metrik_segmen`, `definisi`, `n_nodata`,
`n_valid_prev`, `auprc_segmen`, `skor_ringkas`, `latih_well`, `n_fitur`, `n_estimators`,
`ambang_operasi`, `per_alat`, `lead_menit`, `head_utama`, `status`, `alasan`, `tindakan`,
`persistence_horizon_ref`, `label_pos`, `label_komposisi`.

Kunci yang tidak ada di [J], dan ini yang menentukan status bukti dokumen ini:

1. Tidak ada deret skor per jendela. Yang ada hanya `skor_ringkas` berisi `min`, `median`, `maks`,
   misalnya kepala `vib.rf_lowo` di baris 200 sampai 204 dan kepala `tool_wear.canary_3rms` di baris
   1.143 sampai 1.146.
2. Tidak ada kunci `ece`, `reliability`, `bins`, atau `kalibrasi`. Kurva reliabilitas pada bagian 5
   karena itu berstatus rancangan, dan bentuk yang bisa dihitung hari ini adalah bentuk biner satu
   bin (bagian 5.4).
3. Tidak ada kunci `keyakinan` berbentuk angka. Kunci `keyakinan` di [J] berisi teks alasan, misalnya
   baris 83 dan baris 173.
4. Tidak ada kunci pita atau ambang keputusan. Lima pita di bagian 4 adalah keputusan dokumen ini,
   bukan angka yang sudah ada di [J].

## 3. Rumus: dari skor mentah tujuh engine ke keyakinan 0 sampai 1

Ada tiga lapis, dan urutannya mengikat. Lapis 1 menormalkan skor mentah tiap kepala menjadi
`0..1`. Lapis 2 menggabungkan kepala di dalam satu klaim. Lapis 3 memotong hasilnya dengan batas
atas bukti kelas itu. Angka yang tampil adalah hasil lapis 3.

### 3.1 Normalisasi skor mentah per jenis kepala

Empat jenis skor mentah muncul di [J] dan [P], dan masing-masing butuh satu rumus berbeda.

| Jenis kepala | Contoh kepala | Skor mentah | Normalkan jadi `s` di 0..1 | Alasan |
|---|---|---|---|---|
| Biner kanal | `rule_display`, `persistence`, `hybrid_rule_and_persistence`, `e1_2of3`, `persistence_event`, `op_far_calibrated`, `persistence` bit_wear | 0 atau 1 ([J] baris 389, 465, 468) | `s = 1` bila menyala, `s = 0` bila tidak | Kepala ini memang keputusan biner pada jendela t, jadi tidak ada derajat di antaranya |
| Hitungan fitur | `calib_5of27` | bilangan bulat 0 sampai 27, batas alarm 5 dari 27 ([P] baris 613 dan 635; [L] baris `L-21`) | `s = 0` bila `n_z < 5`; `s = 0,5 + 0,5 x (n_z - 5) / 22` bila `5 <= n_z <= 27` | Ambang alarm di 5, jadi 5 adalah titik "cukup bukti" dan 27 adalah semua fitur menyimpang. Pemetaan linier dua potong menjaga urutan dan tidak mengarang lengkungan |
| Rerata z mutlak | `canary_3rms` | bilangan real, batas alarm 3 ([P] baris 687) | `s = min(1, z / 3)` | Titik alarm di 3 sigma sama dengan [L] baris `L-22`; di atas 3 tidak menambah bukti baru |
| Probabilitas RF | `rf_lowo` | `predict_proba[:, 1]` di [P] baris 435 | `s = p` bila terkalibrasi; bila belum, `s = p` dengan badge "belum terkalibrasi", dan bila ECE lebih dari 0,05 maka `p` diganti hasil isotonik yang dilatih hanya pada fold latih | Probabilitas mentah boleh dibaca sebagai skor urut, bukan sebagai frekuensi, sampai bagian 5 membuktikan kalibrasinya |

Aturan tambahan. Kepala yang statusnya tidak tersedia tidak dinormalkan menjadi 0, karena 0 berarti
"tidak ada indikasi", sedangkan tidak tersedia berarti "tidak dinilai". [J] baris 847 menulis status
eksplisit "BUKAN skor 0" untuk kepala `hyd.k2_tidak_tersedia`, dan baris 909 menulis
`"jangan pakai K-2 di tingkat apa pun"` untuk `bit_wear.k2_onset_belum`. Kedua kepala itu
diperlakukan sebagai abstain pada bagian 4.2.

### 3.2 Bobot per kepala, diambil dari dokumen evaluasi

Bobot disusun dari tiga sifat yang sudah tertulis di dokumen evaluasi, bukan dari selera.

```
w_h = w_tier x w_layer x m_utama
```

| Komponen | Nilai | Sumber | Alasan |
|---|---:|---|---|
| `w_tier` PERINGATAN-BERPENGAWAS | 1,00 | [EVC] baris 88 sampai 99 (kolom TIER) | Tier tertinggi yang ada hari ini; 0 dari 7 engine lolos tier ALARM-OTOMATIS ([J] baris 1.414, [EVC] baris 101) |
| `w_tier` TREN | 0,50 | [EVC] baris 38 sampai 39 (arketipe Pragmatist: lapisan alarm harian rule/persistence, ML untuk ranking dan tren) | Kepala tren tidak boleh menyumbang setara kepala peringatan, karena fungsinya mengurutkan, bukan memutuskan |
| `w_tier` BELUM LAYAK PAKAI | 0,00 | [EVC] baris 96 dan 97 (hyd K-ii, bit_wear K-2) | Klaim yang belum dljalankan tidak boleh memberi angka, karena bobot 0 memaksa jalur abstain |
| `w_layer` L1 | 1,00 | [P] baris 294 sampai 299, [PM1] baris 131 | L1 adalah peringatan yang wajib konfirmasi manusia |
| `w_layer` L0 | 0,80 | [P] baris 295 | L0 status otomatis tanpa notifikasi, dipakai sebagai konfirmasi, bukan sebagai pemicu |
| `w_layer` L2 | 0,50 | [P] baris 297 | L2 dasbor tren, tanpa notifikasi |
| `w_layer` L3 | 0,00 | [P] baris 298 | L3 keputusan manusia, kepala di lapis ini tidak memberi skor |
| `m_utama` | 1,50 bila `head_utama` benar, selain itu 1,00 | [J] baris 811 (`"head_utama": true` pada `hyd.hybrid_rule_and_persistence`), [P] baris 230 | Satu kepala utama per klaim sudah ditetapkan pemilik arsitektur; pengali ini membuat kepala utama mengalahkan kepala pendukung saat berbeda pendapat |

Hasilnya per klaim, dan jumlah bobotnya dipakai sebagai penyebut:

| Engine / klaim | Kepala dan bobot | Jumlah bobot |
|---|---|---:|
| vib | rule 1,00; persistence 0,80; hybrid 1,00; rf_lowo 0,25 | 3,05 |
| ssi | rule 1,00; persistence 0,80; hybrid 1,00; rf_lowo 0,25 | 3,05 |
| shk | rule 1,00; persistence 0,80; hybrid 1,00; rf_lowo 0,25 | 3,05 |
| stuck K-i | rule 1,00; persistence 0,80; hybrid 1,00 | 2,80 |
| stuck K-ii | e1_2of3 0,25; persistence_event 0,25; rf_lowo 0,25 | 0,75 |
| hyd K-i | rule 1,00; persistence 0,80; hybrid 1,50 | 3,30 |
| hyd K-ii | k2_tidak_tersedia 0,00 | 0,00 |
| bit_wear K-1 | persistence 0,25 | 0,25 |
| bit_wear K-2 | k2_onset_belum 0,00 | 0,00 |
| tool_wear K-i | calib_5of27 0,25; op_far_calibrated 1,00 | 1,25 |
| tool_wear K-ii | canary_3rms 0,25 | 0,25 |

K-i dan K-ii dihitung terpisah. [J] baris 723 menulis bahwa keduanya klaim terpisah dengan jumlah
jendela berbeda (K-i 3.201, K-ii 95.925), sehingga satu angka gabungan untuk `stuck` akan mencampur
dua tugas berbeda.

### 3.3 Gabungan di dalam satu klaim

```
K_klaim(t) = jumlah_h ( w_h x s_h(t) ) / jumlah_h w_h
```

Penyebut hanya memuat kepala yang tersedia pada jendela itu. Bila satu kepala tidak tersedia,
penyebut menyusut dan kartu wajib mencetak berapa kepala yang ikut, seperti pada contoh E3
(bagian 6). Ini pola Dynamic Island: yang hilang menjadi label, bukan menjadi nol.

### 3.4 Batas atas dari bukti kelas

Skor mentah yang sempurna pada satu jendela tidak boleh melampaui mutu bukti kelasnya. Batas atas
diambil dari skor keyakinan kelas yang sudah ada, yaitu `SK = 100 x (0,40 S_A + 0,35 S_B + 0,25 S_C)`
([I2] baris 145), dengan tambahan aturan potong dari [I4] baris 233, yaitu skor maksimum 70 selama
lapisan B belum terukur.

```
SK_efektif = min( SK , 70 )        (potong [I4] baris 233)
K_max       = SK_efektif / 100
K_tampil(t) = min( K_klaim(t) , K_max )
```

| Kelas | S_A | S_B | S_C | SK di [I2] | SK hitung ulang | K_max | Pita tertinggi |
|---|---:|---:|---:|---:|---:|---:|---|
| vib | 0,75 | 0,20 | 0,50 | 50 ([I2] baris 161) | 0,4950 | 0,4950 | P3 |
| ssi | 0,75 | 0,20 | 0,625 | 53 ([I2] baris 162) | 0,5263 | 0,5263 | P3 |
| shk | 0,60 | 0,35 | 0,625 | 52 ([I2] baris 167) | 0,5188 | 0,5188 | P3 |
| stuck (satu baris kelas) | 0,60 | 0,35 | 0,375 | 46 ([I2] baris 164) | 0,4562 | 0,4562 | P3 |
| hyd K-i | 0,75 | 0,35 | 0,75 | 61 ([I2] baris 165) | 0,6100 | 0,6100 | P4 |
| hyd K-ii | 0,60 | 0,60 | 0,25 | 51 ([I2] baris 166) | 0,5125 | 0,5125 | P3 |
| bit_wear | 0,30 | 0,20 | 0,25 | 25 ([I2] baris 163) | 0,2525 | 0,2525 | P2 |
| tool_wear | 0,30 | 0,60 | 0,50 | 46 ([I2] baris 168) | 0,4550 | 0,4550 | P3 |

Kolom SK di [I2] dan kolom SK hitung ulang berbeda hanya karena pembulatan ke bilangan bulat:
0,4550 menjadi 46 dan 0,5188 menjadi 52, persis seperti tertulis di [I2]. Aritmetika kedelapan baris
dihitung ulang dengan `awk` dan keluarannya ditempel di bagian 6. Konsekuensi yang harus ditampilkan
apa adanya: pita P5 (0,80 sampai 1,00) tidak bisa dicapai kelas mana pun hari ini, karena SK
tertinggi adalah 61 pada `hyd` K-i. Pita itu bukan hiasan, ia gerbang yang menunggu bukti, dan
syaratnya ada di bagian 11.

Dua baris pada tabel di atas memakai batas atas pinjaman dari baris kelas. `stuck K-ii` dan
`tool_wear K-ii` belum punya baris SK sendiri di [I2], jadi keduanya memakai SK kelasnya dan kartu
wajib mencetak label "batas atas mengikuti baris kelas, belum dipisah per klaim". Ini asumsi
terbuka, bukan angka yang sudah disetujui.

### 3.5 Larangan menggabungkan antar engine

Tujuh engine tidak dijumlahkan menjadi satu angka keyakinan, dan tidak dirata-ratakan. Tiga alasan
yang bisa diperiksa:

1. [EVA] baris 31 (keputusan EA-1) menetapkan 7 engine dinilai pada 11 klaim, karena klaim terpisah
   punya tugas, label, dan baseline berbeda. Satu angka gabungan akan mencampur tugas yang tidak
   sebanding.
2. [K] baris 198 sampai 201 menetapkan satu kepala tidak boleh dipakai sebagai alasan menaikkan tier
   kelas lain. Penjumlahan antar engine adalah bentuk lain dari pelanggaran itu.
3. Skala waktunya berbeda: domain rig memakai jendela 60 detik dan FAR per 24 jam, domain bengkel
   memakai jendela 1 detik dan FAR per menit ([J] baris 96 dan 948; [PM1] baris 132 keputusan D-A7).
   Menjumlahkan keduanya akan mencampur dua satuan.

Yang diizinkan antar engine hanya tiga operasi: mengurutkan klaim berdasarkan `K_tampil`,
menampilkan panel ketidaksepakatan antar kepala pada jendela yang sama (fitur KEP-08 di [K] baris
673), dan menjumlahkan beban tinjauan per shift dalam satuan tinjauan, bukan dalam satuan keyakinan
([J] baris 1.687 sampai 1.754).

## 4. Lima pita keyakinan dan pita abstain

### 4.1 Lima pita

Batas pita diturunkan dari ambang yang sudah ada di dokumen evaluasi, bukan dari pembagian rata
semata. Tiga jangkar yang dipakai: 0,80 adalah syarat alarm pada keputusan D-A6 ([PM1] baris 131,
"B1 lebih atau sama dengan 80 persen"), 0,60 adalah batas bawah komponen S_B kelas 1,00 dan 0,60 di
[I2] baris 152 sampai 154, dan 0,20 adalah batas komponen S_B "belum terukur" di baris 154.

| Pita | Rentang `K_tampil` | Nama | Arti | Tindakan yang dianjurkan | Tampilan angka |
|---|---|---|---:|---|---|
| P1 | 0,00 sampai 0,19 | Tidak ada indikasi | Semua kepala pendukung diam atau bukti kelas sangat tipis | Tidak ada tindakan. Catat sebagai jendela tenang untuk hitungan beban tinjauan | Angka disembunyikan, hanya nama pita dan jumlah kepala yang ikut |
| P2 | 0,20 sampai 0,39 | Indikasi lemah | Ada satu kepala menyala, atau sinyal kuat tetapi batas atas kelas menekan (contoh bit_wear 0,2525) | Pantau, periksa kanal masukan. Tidak masuk antrean kerja | Persen kecil, warna redup, alasan batas atas tampil |
| P3 | 0,40 sampai 0,59 | Perlu tinjauan | Sinyal terbaca, dukungan bukti kelas sedang | Satu langkah pemeriksaan data atau lapangan, dicatat di log keputusan | Persen sedang, badge FAR wajib tampil berdampingan |
| P4 | 0,60 sampai 0,79 | Keyakinan kuat | Mayoritas kepala menyala dan kelas punya bukti lapisan A kuat | Masuk antrean kerja shift ini, wajib konfirmasi operator | Persen besar, tiga komponen S_A S_B S_C tampil terbuka |
| P5 | 0,80 sampai 1,00 | Keyakinan tinggi | Syarat alarm pada D-A6 terpenuhi kelas itu dan skor jendela tinggi | Eskalasi ke supervisor insinyur pengeboran | Persen besar, label "syarat alarm terpenuhi" |

Arti bila angka naik atau turun, karena ini yang paling sering salah dibaca:

1. Naik karena kepala bertambah yang menyala: bukti jendela menguat.
2. Naik karena batas atas kelas naik setelah kampanye baru: mutu bukti kelas membaik.
3. Turun padahal sinyal lapangan sama: ada komponen yang sebelumnya diasumsikan kini terukur dan
   ternyata rendah. [K] baris 295 sampai 299 sudah menulis aturan ini untuk skor 0 sampai 100, dan
   aturan yang sama berlaku untuk skala 0 sampai 1.
4. Turun mendadak ke pita abstain: data masukan hilang, bukan kondisi rig membaik.

### 4.2 Pita abstain

Abstain bukan pita keenam dalam skala angka. Abstain adalah status yang menggantikan angka, dan
kartu wajib menyebut kodenya.

| Kode | Nama | Syarat terpicu | Yang ditampilkan | Contoh nyata |
|---|---|---|---|---|
| AB-1 | Tanpa kepala berskor | Jumlah bobot klaim sama dengan 0 | "Tidak dinilai: belum ada kepala berskor" dan daftar kepala yang menunggu | `hyd` K-ii ([J] baris 836 sampai 848, bobot 0) dan `bit_wear` K-2 ([J] baris 897 sampai 910, bobot 0) |
| AB-2 | Data sensor kurang | `n_nodata / n_windows` lebih dari 0,50 | "Tidak dinilai: kanal absen pada X persen jendela", plus tautan ke kartu kesiapan kanal | `ssi.rule_display` [J] baris 247: `n_nodata` 5.268 dari 5.455 jendela, yaitu 0,9657 (perhitungan di bagian 10) |
| AB-3 | Skor per jendela tidak tersedia | Hanya ringkasan `min`, `median`, `maks` yang ada untuk kepala penentu | "Tidak dinilai: skor jendela belum diekspor", plus pita ringkasan yang ada | `vib.rf_lowo` [J] baris 200 sampai 204 dan `tool_wear.canary_3rms` baris 1.143 sampai 1.146 |
| AB-4 | Klaim di lapis L3 | Tier `BELUM LAYAK PAKAI` atau lapisan L3 | "Tidak dinilai menurut desain", plus alasan dari [J] | `hyd.k2_tidak_tersedia` ([J] baris 838 sampai 840, lapisan L3) |

Aturan tampilan abstain: warna abu dengan pola garis miring, angka diganti tanda pisah pendek dan
teks alasan, kartu tetap muncul di urutan dengan penanda "menunggu data", dan kartu tidak pernah
masuk antrean kerja. Alasan memakai pola garis miring, bukan warna merah: [K] baris 203 sampai 207
melarang warna merah tanpa label manusia-peninjau, dan abstain bukan bahaya.

### 4.3 Peta pita ke tier dan lapisan

| Tier di [J] | Lapisan | Pita yang boleh dipakai |
|---|---|---|
| PERINGATAN-BERPENGAWAS | L1 | P1 sampai P5, dengan P5 menunggu syarat bagian 11 |
| PERINGATAN-BERPENGAWAS | L0 | P1 sampai P4, P5 hanya bila kelas itu naik tier |
| TREN | L2 | P1 sampai P3. Kartu L2 tidak boleh menampilkan P4 dan P5, karena keputusan inspeksi bukan wewenang kepala tren |
| BELUM LAYAK PAKAI | L3 | abstain saja |

## 5. Kurva reliabilitas dan ECE: cara menghitung dan cara membacanya

### 5.1 Apa yang digambarkan

Kurva reliabilitas membandingkan peluang prediksi dengan frekuensi kejadian nyata. Sumbu x adalah
rata-rata peluang prediksi per bin, sumbu y adalah fraksi positif nyata per bin, dan garis diagonal
adalah acuan sempurna. Definisi yang dipakai: di antara sampel yang diberi peluang mendekati 0,8,
sekitar 80 persen benar-benar positif ([VR] baris 165, sumber [LV1]). Bila titik menyimpang ke atas
diagonal, model terlalu percaya diri. Bila menyimpang ke bawah, model terlalu ragu.

Peringatan dari sumber yang sama dan dipakai sebagai larangan di sini: skor tunggal seperti Brier
mencampur kalibrasi, daya pisah, dan keacakan data, sehingga skor rendah tidak otomatis berarti
terkalibrasi baik ([VR] baris 167). Karena itu ECE tidak pernah ditampilkan sendirian, selalu
berdampingan dengan kurva dan jumlah bin.

### 5.2 ECE: rumus dan sumber

```
ECE = jumlah_m ( |B_m| / n ) x | acc(B_m) - conf(B_m) |
```

Keterangan: `B_m` adalah himpunan sampel di bin ke-m, `n` jumlah sampel, `acc(B_m)` fraksi positif
nyata di bin itu, `conf(B_m)` rata-rata peluang prediksi di bin itu. Bentuk ini adalah rumus ECE
pada Guo dan kawan-kawan (2017), Proceedings of Machine Learning Research 70, persamaan (3), yang
menyebut ECE berasal dari Naeini dan kawan-kawan (2015) dan memakai M bin berjarak sama. Rujukan
diperiksa lewat pencarian web pada 2026-10-31, dan kutipan Persamaan (3) ada di
`proceedings.mlr.press/v70/guo17a/guo17a.pdf`.

### 5.3 Langkah hitung, dengan parameter yang dibekukan sebelum hasil dilihat

1. Ekspor pasangan `(skor, label)` per kepala per fold. Sumbernya keluaran `train_lowo` di [P] baris
   435, yang saat ini tidak disimpan.
2. Bekukan jumlah bin dan cara pemotongan bin. Keputusan dokumen ini: 10 bin kuantil (desil), sama
   dengan jumlah kuartil pada normalisasi [L] baris `L-18` dan dengan usulan [K] baris 454.
3. Buang bin yang beranggota kurang dari 50 sampel, lalu gabungkan ke bin sebelahnya, mengikuti
   konvensi "min 50 bin" yang tercatat di [L] baris 121.
4. Hitung `conf(B_m)` dan `acc(B_m)` per bin, lalu `ECE` dan `MCE` (galat terbesar satu bin).
5. Hitung arah penyimpangan: positif bila `acc` lebih besar dari `conf` (model ragu), negatif bila
   sebaliknya (model terlalu percaya diri).
6. Simpan satu gambar per kepala, bukan satu gambar gabungan, mengikuti [K] baris 493.
7. Ulangi dengan 5 dan 20 bin sebagai uji ketahanan. Kesimpulan arah tidak boleh berubah, mengikuti
   [K] baris 497.

Ambang tampil yang dipakai dokumen ini: ECE 0,05 atau kurang berarti skor boleh dicetak sebagai
persen frekuensi. ECE lebih dari 0,05 berarti skor hanya boleh dicetak sebagai peringkat, dan kartu
wajib menampilkan badge "belum terkalibrasi". Angka 0,05 adalah keputusan dokumen ini, bukan angka
yang sudah disetujui, dan dicatat di bagian 12.

### 5.4 Bentuk yang bisa dihitung hari ini: ECE biner satu bin

Untuk kepala biner, skor hanya 0 atau 1, sehingga kurva reliabilitas punya dua bin dan bin skor 0
selalu akurat secara definisi. Yang tersisa adalah satu suku:

```
ECE_biner = ( (TP + FP) / n ) x ( 1 - presisi )
```

Angka masuknya sudah ada di [J] pada blok `metrik_segmen`, jadi tiga contoh di bawah adalah angka
terukur, bukan rancangan. Perhitungannya dijalankan dengan `awk` dan keluarannya ditempel di bagian 6.

| Kepala | TP | FP | n | Presisi | `ECE_biner` |
|---|---:|---:|---:|---:|---:|
| `vib.rule_display` ([J] baris 91 sampai 96) | 510 | 30 | 1.989 | 0,9444 | 0,0151 |
| `hyd.hybrid_rule_and_persistence` ([J] baris 825 sampai 831) | 516 | 110 | 10.401 | 0,8243 | 0,0106 |
| `shk.rule_display` ([J] baris 383 sampai 388) | 55 | 48 | 11.205 | 0,5340 | 0,0043 |

Catatan pembacaan: ECE biner yang kecil tidak berarti kepala itu bagus. Kepala `shk.rule_display`
punya ECE 0,0043 karena ia hampir tidak pernah menyala (103 dari 11.205 jendela, [J] baris 368 dan
369), sehingga jumlah prediksi positifnya kecil dan sukunya kecil. Inilah contoh persis dari
peringatan [VR] baris 167: satu angka kalibrasi tanpa daya pisah menyesatkan. Karena itu ECE selalu
tampil bersama presisi, recall, dan FAR pada kartu yang sama.

## 6. Tiga contoh perhitungan dengan angka nyata

Seluruh angka di bagian ini dihitung dengan perintah `awk` yang ditempel utuh di bawah, sehingga
pembaca bisa menjalankan ulang dan membandingkan. Tidak ada angka yang dibulatkan di tengah jalan.

### 6.1 Perintah yang dijalankan

```
awk 'BEGIN{
printf "SK kelas (0.40A+0.35B+0.25C)\n";
split("vib ssi shk stuck hydKi hydKii bitwear toolwear",n," ");
A[1]=0.75;A[2]=0.75;A[3]=0.60;A[4]=0.60;A[5]=0.75;A[6]=0.60;A[7]=0.30;A[8]=0.30;
B[1]=0.20;B[2]=0.20;B[3]=0.35;B[4]=0.35;B[5]=0.35;B[6]=0.60;B[7]=0.20;B[8]=0.60;
C[1]=0.50;C[2]=0.625;C[3]=0.625;C[4]=0.375;C[5]=0.75;C[6]=0.25;C[7]=0.25;C[8]=0.50;
for(i=1;i<=8;i++){sk=0.40*A[i]+0.35*B[i]+0.25*C[i]; printf "%-9s SK=%7.4f  K_max=%6.4f  SK_bulat=%d\n", n[i], sk, sk, int(sk*100+0.5)}
num=1.00*1+0.80*1+1.50*1; den=1.00+0.80+1.50;
printf "E1 num=%.4f den=%.4f K=%.4f final=%.4f\n", num, den, num/den, (num/den<0.61?num/den:0.61);
num=0.25*1; den=0.25;
printf "E2 num=%.4f den=%.4f K=%.4f final=%.4f\n", num, den, num/den, (num/den<0.2525?num/den:0.2525);
num=1.00*1+0.80*1+1.00*0; den=1.00+0.80+1.00;
printf "E3 num=%.4f den=%.4f K=%.4f final=%.4f\n", num, den, num/den, (num/den<0.495?num/den:0.495);
printf "vib rule    presisi=%.4f ECE=%.4f\n", 510/(510+30), ((510+30)/1989)*(1-510/(510+30));
printf "hyd hybrid  presisi=%.4f ECE=%.4f\n", 516/(516+110), ((516+110)/10401)*(1-516/(516+110));
printf "shk rule    presisi=%.4f ECE=%.4f\n", 55/(55+48), ((55+48)/11205)*(1-55/(55+48));
printf "rasio nodata ssi = 5268/5455 = %.4f\n", 5268/5455;
printf "tinjauan per shift vib = %.4f -> %d\n", 49.942/3, int(49.942/3)+1;
printf "tinjauan per shift hyd hybrid = %.4f -> %d\n", 16.611/3, int(16.611/3)+1;
}'
```

### 6.2 Keluaran apa adanya

```
SK kelas (0.40A+0.35B+0.25C)
vib       SK= 0.4950  K_max=0.4950  SK_bulat=50
ssi       SK= 0.5263  K_max=0.5263  SK_bulat=53
shk       SK= 0.5188  K_max=0.5188  SK_bulat=52
stuck     SK= 0.4562  K_max=0.4562  SK_bulat=46
hydKi     SK= 0.6100  K_max=0.6100  SK_bulat=61
hydKii    SK= 0.5125  K_max=0.5125  SK_bulat=51
bitwear   SK= 0.2525  K_max=0.2525  SK_bulat=25
toolwear  SK= 0.4550  K_max=0.4550  SK_bulat=45

E1 hyd K-i: rule=1 pers=1 hybrid=1
num=3.3000 den=3.3000 K=1.0000 cap=0.6100 final=0.6100
E2 bit_wear K-1: persistence=1
num=0.2500 den=0.2500 K=1.0000 cap=0.2525 final=0.2525
E3 vib: rule=1 pers=1 hybrid=0 (rf tidak tersedia, penyebut 2.80)
num=1.8000 den=2.8000 K=0.6429 cap=0.4950 final=0.4950

ECE biner satu bin
vib rule      (510+30)/1989=0.271493 presisi=0.9444 ECE=0.0151
hyd hybrid    (516+110)/10401=0.060187 presisi=0.8243 ECE=0.0106
shk rule      (55+48)/11205=0.009192 presisi=0.5340 ECE=0.0043

rasio nodata ssi = 5268/5455 = 0.9657
tinjauan per shift vib = 49.942/3 = 16.6473 -> 17
tinjauan per shift hyd hybrid = 16.611/3 = 5.5370 -> 6
```

Satu baris keluaran perlu dibaca hati-hati: `toolwear SK_bulat=45`. Angka sebenarnya 0,4550, dan
0,4550 x 100 = 45,5, dibulatkan setengah ke atas menjadi 46 seperti tertulis di [I2] baris 168.
Nilai 45 muncul karena `awk` menyimpan 0,455 sebagai 45,49999 dan `int` memotong ke bawah. Dokumen
ini memakai 46 mengikuti sumber, dan `K_max` tetap 0,4550 karena potongannya memakai nilai desimal,
bukan nilai bulat.

### 6.3 Contoh E1: keyakinan kuat yang tertahan batas atas, `hyd` K-i

Jendela t: `rule_display` menyala, `persistence` menyala, `hybrid_rule_and_persistence` menyala.

```
K_klaim = (1,00x1 + 0,80x1 + 1,50x1) / (1,00 + 0,80 + 1,50) = 3,30 / 3,30 = 1,0000
K_max   = SK hyd K-i / 100 = 0,6100
K_tampil = min(1,0000 ; 0,6100) = 0,6100   -> pita P4 (0,60 sampai 0,79)
```

Bacaan untuk pengguna: tiga kepala sepakat pada jendela ini, dan yang paling berbobot adalah kepala
utama `hybrid` ([J] baris 811). Angka yang tampil tetap 61 karena kelas `hyd` baru punya S_B 0,35
([I2] baris 165), artinya kesiapan operasionalnya sedang. Kartu harus menuliskan alasan ini, supaya
operator tidak menyimpulkan "sistem hanya 61 persen yakin padahal semua kepala menyala".

### 6.4 Contoh E2: sinyal tunggal yang tertahan bukti kelas, `bit_wear` K-1

Jendela t: `persistence` bit_wear menyala, dan itu satu-satunya kepala berskor pada klaim K-1.

```
K_klaim = (0,25x1) / 0,25 = 1,0000
K_max   = SK bit_wear / 100 = 0,2525
K_tampil = min(1,0000 ; 0,2525) = 0,2525   -> pita P2 (0,20 sampai 0,39)
```

Bacaan untuk pengguna: kepala menyala penuh, tetapi kelas `bit_wear` punya S_A 0,30 dan S_C 0,25
([I2] baris 163), jadi bukti kelasnya sendiri baru level lemah. Kartu menampilkan "indikasi lemah"
dan tindakan "pantau", bukan "ganti bit". Inilah beda antara sinyal jendela dan mutu bukti kelas,
dan itu pesan yang paling penting untuk dicegah salah tafsir.

### 6.5 Contoh E3: kepala yang tidak tersedia menyusutkan penyebut, `vib`

Jendela t: `rule_display` menyala, `persistence` menyala, `hybrid_rule_and_persistence` diam, dan
`rf_lowo` tidak punya skor per jendela (hanya ringkasan di [J] baris 200 sampai 204), sehingga
terkena AB-3 dan keluar dari penyebut.

```
K_klaim = (1,00x1 + 0,80x1 + 1,00x0) / (1,00 + 0,80 + 1,00) = 1,80 / 2,80 = 0,6429
K_max   = SK vib / 100 = 0,4950
K_tampil = min(0,6429 ; 0,4950) = 0,4950   -> pita P3 (0,40 sampai 0,59)
```

Bacaan untuk pengguna: dua dari tiga kepala yang tersedia menyala, satu kepala penuh tidak tersedia.
Kartu wajib mencetak "3 dari 3 kepala dinilai, 1 kepala tidak tersedia (skor jendela belum
diekspor)". Penyebut 2,80 dipakai, bukan 3,05, karena kepala `rf_lowo` tidak dinilai pada jendela
itu. Bila ada yang menghitung dengan penyebut 3,05, hasilnya 0,5902 dan pitanya berubah menjadi P3
dengan angka berbeda, sehingga aturan penyebut ini harus ditulis di kode, bukan diserahkan ke
pembaca.

### 6.6 Contoh E4: abstain, `hyd` K-ii

Jendela t: seluruh kepala K-ii berstatus tidak tersedia ([J] baris 838 sampai 848).

```
jumlah bobot = 0,00   -> AB-1, dan AB-4 karena lapisan L3
K_tampil = tidak ada angka
tampil   = "Tidak dinilai menurut desain" + alasan dari [J] baris 847
```

Bacaan untuk pengguna: kelas ini tidak punya kanal yang bisa dihitung, jadi tidak ada angka yang
jujur untuk ditampilkan. Kartu tetap muncul di halaman, dengan penanda "menunggu data", dan tidak
masuk antrean kerja. Yang dibutuhkan untuk mengubah status ini ada di bagian 11.

## 7. Spesifikasi lima fitur

Setiap fitur memuat tiga belas butir wajib. Status bukti ditulis jujur di butir kesebelas, dan
kode fitur yang sudah ada di katalog [K] disebut agar tidak ada dua nama untuk satu benda.

### 7.1 DSS-01 Skor keyakinan per jendela

**ID dan nama fitur.** DSS-01, "Skor keyakinan per jendela". Kode katalog terkait: KEP-02 ([K] baris
613), yang memakai skala 0 sampai 100. DSS-01 adalah versi 0 sampai 1 dari skala yang sama, dan
keduanya wajib memakai satu fungsi konversi supaya tidak bercabang.

**Tujuan.** Menjawab satu pertanyaan yang sekarang tidak terjawab: pada jendela waktu ini, seberapa
kuat bukti yang dimiliki sistem untuk klaim yang sedang tampil. Tanpa angka ini, pengguna hanya
melihat kepala mana yang menyala dan harus menimbang sendiri. Penggunanya operator monitoring di
ruang kontrol dan insinyur yang meninjau log keputusan.

**Menggambarkan apa.** Menggambarkan kekuatan bukti jendela, bukan peluang kerusakan. Naik berarti
lebih banyak kepala berskor menyala, atau kepala berbobot tinggi menyala. Turun berarti kepala
padam, atau ada kepala yang sebelumnya diasumsikan kini terukur dan diam. Angka ini tidak berubah
menjadi pernyataan frekuensi sampai bagian 5 membuktikan kalibrasinya.

**Pengguna dan momen pakai.** Operator monitoring: setiap kali daftar jendela dibuka, 1 sampai 3
kali per shift, untuk memilih mana yang dibaca dulu. Insinyur pengeboran: saat meninjau log
keputusan, 1 kali per shift, untuk menilai apakah keputusan kemarin diambil pada bukti yang cukup.
Pengawas: saat rapat pagi, 1 kali per hari, untuk melihat sebaran keyakinan semalam.

**Masukan.** Keluaran tujuh engine dari `scratch/v9_i1/v9_i1_RESULTS.json` [J], khususnya 27 entri
kepala pada blok `engines` (baris 60 sampai 1.152). Kolom yang dipakai per kepala: `head`, `klaim`,
`tier`, `layer`, `head_utama`, `n_windows`, `n_aktif`, `metrik_segmen`, `skor_ringkas`. Satuan
masukan: hitungan jendela, dan skor mentah 0 atau 1 untuk kepala biner. Rentang: `n_windows` dari 95
(`stuck` K-ii, [J] baris 741) sampai 95.925 ([J] baris 723 disebut untuk K-i dan K-ii, angka
per kepala ada di tiap entri). Cara memperoleh: membaca berkas hasil pipeline, bukan menghitung ulang
dari data mentah.

**Algoritma.** Nama metode: agregasi terbobot dengan potong batas atas, tiga lapis seperti bagian 3.

```
s_h  = normalisasi skor mentah kepala h          (bagian 3.1)
w_h  = w_tier x w_layer x m_utama                (bagian 3.2)
K    = jumlah(w_h x s_h) / jumlah(w_h)           (bagian 3.3)
K_tampil = min(K, K_max)                         (bagian 3.4)
```

Parameter: `w_tier` 1,00 / 0,50 / 0,00; `w_layer` 1,00 / 0,80 / 0,50 / 0,00; `m_utama` 1,50.
Ambang: tidak ada ambang keputusan di dalam rumus. Pita ditentukan terpisah pada DSS-03. Alasan
memilih agregasi terbobot, bukan rata-rata sederhana: kepala berbeda tier dan lapisan, dan [EVC]
baris 38 sampai 39 menetapkan peran berbeda untuk kepala alarm dan kepala tren.

**Workflow.**
1. Pipeline menulis `v9_i1_RESULTS.json` (berkas [J]).
2. Lapisan pembaca memuat 27 entri kepala dan menyaring kepala dengan `status` tidak tersedia.
3. Untuk tiap kepala tersedia, hitung `s_h` menurut jenisnya (biner, hitungan fitur, rerata z, atau
   probabilitas).
4. Hitung `w_h` dari `tier`, `layer`, dan `head_utama`.
5. Jumlahkan `w_h x s_h` dan `w_h`, lalu bagi.
6. Periksa syarat abstain bagian 4.2. Bila terpicu, hentikan dan tampilkan kartu abstain.
7. Potong dengan `K_max` kelas.
8. Bulatkan ke dua desimal untuk data, tampilkan sebagai persen bulat di layar.
9. Kirim ke kartu DSS-05 bersama jumlah kepala yang ikut dinilai.

**Keluaran.** Bentuk data: satu bilangan real 0 sampai 1 per klaim per jendela, ditambah tiga field
pendukung, yaitu `n_kepala_dinilai`, `n_kepala_tersedia_total`, dan `kepala_dinilai` (daftar nama).
Satuan: tanpa satuan, skala rasio semu 0 sampai 1. Rentang yang mungkin hari ini: 0 sampai 0,61
karena batas atas tertinggi 0,6100. Arti nilai: 0 berarti tidak ada kepala berskor yang menyala,
0,61 berarti bukti jendela penuh tetapi mutu bukti kelas membatasi.

**Saran penyajian.** Batang mendatar pendek per jendela dalam daftar, dengan angka persen di ujung
batang, bukan donat dan bukan pengukur bulat. Alasan: panjang adalah kanal yang paling tepat untuk
perbandingan kuantitatif, sedangkan sudut dan luas lebih lemah ([VR] baris 248, sumber [LV7]); untuk
sebaran per jendela dipakai titik kuantil pada garis 0 sampai 1 karena cara itu paling akurat dibaca
dan hanya memakan sedikit ruang, 1,15 kali lebih ringkas daripada kotak garis pada uji yang dikutip
([VR] baris 157 sampai 159, sumber [LV5]).

Contoh tata letak dalam teks:

```
Klaim hyd K-i        [=========|----]  61%   P4  Keyakinan kuat
                     0        0.61  1.0
Klaim vib            [======|-------]  50%   P3  Perlu tinjauan
Klaim bit_wear K-1   [==|-----------]  25%   P2  Indikasi lemah
Klaim hyd K-ii       [  menunggu data  ]      AB-1
```

**Dasar riset penyajian.** Tiga rujukan yang dipakai: kanal panjang dan posisi untuk besaran
kuantitatif ([VR] baris 248, [LV7]); titik kuantil untuk sebaran padat ruang ([VR] baris 157 sampai
159, [LV5]); dan larangan sumbu ganda saat menampilkan dua besaran berbeda satuan ([VR] baris 244,
[LV8]), yang di sini dipatuhi dengan memisahkan batang keyakinan dan batang FAR ke dua baris.

**Status bukti.** Rumus dan bobot: rancangan, disusun dari dokumen evaluasi. `K_max`: terhitung dari
data nyata [I2] dan cocok dengan `awk`. Skor per jendela: belum ada, karena [J] hanya menyimpan
ringkasan. Tiga contoh angka pada bagian 6 memakai skor jendela yang ditetapkan sebagai skenario,
bukan keluaran pipeline. Ini dicatat lagi di bagian 12.

**Salah tafsir yang harus dicegah.**
1. Dibaca sebagai peluang kerusakan. Pencegahan: label kartu "keyakinan bukti", dan badge
   "belum terkalibrasi" selama ECE belum terukur.
2. Dibandingkan antar engine. Pencegahan: batang hanya bisa diurutkan dalam satu klaim, dan angka
   antar engine diberi pemisah visual per domain (rig dan bengkel).
3. Naik dianggap berita buruk. Pencegahan: teks "naik berarti bukti menguat, bukan kerusakan makin
   dekat".
4. Penyebut lupa menyusut saat kepala tidak tersedia. Pencegahan: field `n_kepala_dinilai` selalu
   tercetak.

**Cara menguji.**
1. Uji monoton: tambah satu kepala menyala, `K` tidak boleh turun. Jalankan pada semua 27 entri.
2. Uji batas: `K_tampil` tidak boleh melebihi 0,6100 untuk kelas apa pun hari ini.
3. Uji penyebut: satu kepala dihapus, hasil harus sama dengan hitungan manual dengan penyebut
   menyusut (contoh E3: 0,6429, bukan 0,5902).
4. Uji abstain: set `jumlah w_h` menjadi 0, kartu harus menjadi AB-1 dan tidak menampilkan angka.
5. Uji regresi angka: jalankan blok `awk` bagian 6.1, delapan nilai `K_max` harus sama persis.

### 7.2 DSS-02 Batas atas bukti kelas

**ID dan nama fitur.** DSS-02, "Batas atas bukti kelas". Terkait KEP-03 dan KEP-04 di [K] baris 620
sampai 630 yang membahas tier dan alasan batas.

**Tujuan.** Mencegah satu jendela bagus menutupi kenyataan bahwa kelasnya sendiri belum terbukti.
Penggunanya insinyur yang menilai apakah angka tinggi boleh dipakai untuk keputusan lapangan, dan
pengawas yang memutuskan apakah kelas layak masuk uji coba.

**Menggambarkan apa.** Menggambarkan mutu bukti yang dimiliki satu kelas, bukan mutu satu jendela.
Naik hanya terjadi bila komponen S_A, S_B, atau S_C berubah karena pengukuran baru. Turun terjadi
bila komponen yang sebelumnya diasumsikan kini terukur dan ternyata lebih rendah. Angka ini sengaja
bergerak lambat, karena ia tidak boleh berubah karena satu jendela.

**Pengguna dan momen pakai.** Insinyur pengeboran: saat memutuskan memakai angka keyakinan untuk
langkah lapangan, beberapa kali per minggu. Pengawas: saat rapat mingguan, 1 kali per minggu.
Peneliti internal: setiap kali kampanye pengukuran selesai, beberapa kali per bulan.

**Masukan.** `S_A`, `S_B`, `S_C` per kelas dari [I2] baris 161 sampai 168, ditambah aturan potong
dari [I4] baris 233 dan status lapisan B per engine dari [J] `profil_kapabilitas` (baris 1.417 sampai
1.665). Satuan: skor 0 sampai 1 per komponen. Rentang: S_A 0,20 sampai 0,75; S_B 0,20 sampai 0,60;
S_C 0,25 sampai 0,75 pada delapan baris yang ada. Cara memperoleh: membaca dokumen inventaris dan
profil kapabilitas, bukan menghitung dari data mentah.

**Algoritma.** Nama metode: skor komposit terbobot dengan potong kebijakan.

```
SK  = 100 x (0,40 S_A + 0,35 S_B + 0,25 S_C)        ([I2] baris 145)
SK' = min(SK, 70)                                   ([I4] baris 233)
K_max = SK' / 100
```

Parameter: bobot 0,40 / 0,35 / 0,25 dan potong 70. Ambang: SK 70 adalah gerbang lapisan B; di bawah
70, kelas boleh tampil tetapi tidak boleh mengklaim alarm otomatis. Alasan memilih: rumus ini sudah
ada di proyek dan dipakai katalog, sehingga tidak perlu rumus kedua. Membuat rumus baru akan
memecah satu angka menjadi dua definisi.

**Workflow.**
1. Ambil tiga komponen per kelas dari [I2].
2. Hitung SK dan bulatkan dua desimal.
3. Terapkan potong 70 bila lapisan B belum terukur untuk kelas itu.
4. Bagi 100 menjadi `K_max`.
5. Tandai baris yang memakai pinjaman kelas (stuck K-ii, tool_wear K-ii).
6. Kirim `K_max` ke DSS-01 sebagai pemotong dan ke DSS-05 sebagai garis batas di kartu.
7. Simpan jejak: nama berkas, nomor baris, dan tanggal baca.

**Keluaran.** Bentuk data: satu bilangan 0 sampai 1 per kelas, ditambah tiga komponen asal dan
tanggal rujukan. Satuan: tanpa satuan. Rentang hari ini: 0,2525 (bit_wear) sampai 0,6100 (hyd K-i).
Arti nilai: 0,2525 berarti kelas itu paling banyak boleh tampil di pita P2 walau semua kepala
menyala.

**Saran penyajian.** Garis batas mendatar abu pada batang DSS-01, dengan label angka di ujung garis,
dan tabel komponen S_A S_B S_C yang bisa dibuka. Alasan: garis acuan pada skala yang sama dibaca
tanpa perlu sumbu kedua ([VR] baris 244 melarang sumbu ganda), dan membuka komponen menjawab
pertanyaan "kenapa batasnya segitu" tanpa memindahkan pengguna ke halaman lain.

Contoh tata letak:

```
hyd K-i      [=========|----] 61%   batas kelas 61  (S_A 0,75  S_B 0,35  S_C 0,75)
vib          [======|-------] 50%   batas kelas 50  (S_A 0,75  S_B 0,20  S_C 0,50)
bit_wear     [==|-----------] 25%   batas kelas 25  (S_A 0,30  S_B 0,20  S_C 0,25)
```

**Dasar riset penyajian.** Garis acuan dan anotasi langsung pada skala yang sama menghindari sumbu
kedua ([VR] baris 244 sampai 245, [LV8]); tabel kecil untuk komponen mengikuti pola "tabel untuk
nilai yang harus dibaca tepat" ([VR] baris 46, [LV6]). Alasan memakai tabel, bukan diagram batang
bertumpuk untuk tiga komponen: tiga angka pendek lebih cepat dibaca sebagai angka.

**Status bukti.** Terhitung dari data nyata. Delapan nilai `K_max` dihitung ulang dengan `awk` dan
sama dengan [I2] setelah pembulatan (bagian 6.2). Yang belum: baris SK terpisah untuk `stuck` K-ii
dan `tool_wear` K-ii.

**Salah tafsir yang harus dicegah.**
1. Dikira batas kemampuan model. Pencegahan: label "batas bukti kelas, bukan batas model", dan
   komponen S_A S_B S_C ditampilkan.
2. Dikira angka tetap selamanya. Pencegahan: tanggal rujukan dicetak di kartu.
3. Batas 25 pada bit_wear dikira bug. Pencegahan: teks "kelas ini baru punya bukti level lemah
   ([I2] baris 163), jadi angka tinggi tidak mungkin muncul hari ini".

**Cara menguji.**
1. Hitung ulang delapan baris dengan `awk` bagian 6.1, bandingkan dengan [I2].
2. Ubah satu komponen, `K_max` harus berubah sesuai bobotnya, dan tidak boleh berubah bila komponen
   lain yang diubah.
3. Potong 70: kelas dengan SK di atas 70 harus turun ke 0,70. Hari ini tidak ada yang terpicu,
   sehingga uji ini memakai kelas rekaan dan hasilnya dicatat sebagai uji unit.
4. Uji silang: `K_tampil` dari DSS-01 tidak boleh melebihi `K_max` untuk seluruh 27 entri.

### 7.3 DSS-03 Pita keyakinan dan tindakan

**ID dan nama fitur.** DSS-03, "Pita keyakinan dan tindakan". Terkait KEP-04 di [K] baris 620 sampai
630 (tier dan alasan) dan KEP-07 (panel ketidaksepakatan) di [K] baris 665.

**Tujuan.** Menerjemahkan angka 0 sampai 1 menjadi lima tindakan yang bisa dieksekusi, tanpa
menyerahkan penilaian ke pembaca. Penggunanya operator di ruang kontrol yang harus tahu apakah
sebuah kartu masuk antrean kerja shift ini atau cukup dipantau.

**Menggambarkan apa.** Menggambarkan tingkat dukungan bukti dan tingkat tindakan yang sepadan.
Naik satu pita berarti satu langkah tindakan bertambah, dari pantau ke tinjauan ke antrean kerja ke
eskalasi. Turun satu pita berarti langkahnya berkurang. Pita tidak menggambarkan bahaya. Pita
tertinggi pun berbunyi "eskalasi ke manusia", bukan "kirim alarm".

**Pengguna dan momen pakai.** Operator monitoring: setiap kali kartu muncul, puluhan kali per shift.
Supervisor insinyur pengeboran: saat menerima eskalasi, 1 sampai 5 kali per shift. Perencana
maintenance: saat menyusun rencana, 1 kali per hari, karena sumber daya bulanan tidak dikelola per
pita (beban tinjauan di [J] baris 1.687 sampai 1.754 dirancang untuk antrean harian).

**Masukan.** `K_tampil` dari DSS-01, `tier` dan `layer` kepala dari [J], dan `badge_far` dari [J]
(misalnya baris 88 dan 371). Satuan: bilangan 0 sampai 1 tanpa satuan. Rentang: 0 sampai 0,61 hari
ini. Cara memperoleh: fungsi pita, bukan tabel ketik tangan.

**Algoritma.** Nama metode: pemetaan ambang berjenjang dengan pengunci tier.

```
P1 jika 0,00 <= K < 0,20
P2 jika 0,20 <= K < 0,40
P3 jika 0,40 <= K < 0,60
P4 jika 0,60 <= K < 0,80
P5 jika 0,80 <= K <= 1,00
```

Pengunci: pita dibatasi oleh tier dan lapisan sesuai bagian 4.3. Kepala L2 maksimum P3, kepala L3
hanya abstain. Parameter: lima batas 0,20 / 0,40 / 0,60 / 0,80. Ambang 0,80 dipakai karena sama
dengan syarat alarm keputusan D-A6 ([PM1] baris 131), sehingga P5 berarti "kalau kelas ini sudah
naik tier, syarat alarmnya terpenuhi". Alasan memilih lima pita, bukan tiga atau tujuh: tiga pita
menghapus perbedaan antara "pantau" dan "tinjau", yang di lapangan adalah dua orang berbeda;
tujuh pita menghasilkan dua pita yang hari ini kosong karena angka maksimum 0,61 dan itu melatih
pengguna mengabaikan warna.

**Workflow.**
1. Terima `K_tampil` dan metadata tier serta lapisan dari DSS-01.
2. Cek pengunci tier: bila L3, keluarkan abstain AB-4 dan berhenti.
3. Petakan angka ke pita memakai lima batas.
4. Tempelkan nama pita, tindakan, dan warna dari tabel bagian 4.1.
5. Bila pita P5, tambahkan syarat tambahan: kelas harus tier PERINGATAN-BERPENGAWAS dan SK kelas
   di atas 70.
6. Bila P3 atau lebih, ambil teks tindakan dari tabel dan tampilkan bersama badge FAR.
7. Kirim ke kartu DSS-05 untuk tata letak.

**Keluaran.** Bentuk data: satu objek per kartu berisi `pita` (P1 sampai P5), `nama_pita`,
`tindakan`, `warna`, `alasan_pengunci`. Satuan: kategori, bukan angka. Arti tiap nilai ada di tabel
bagian 4.1. Rentang: P1 sampai P5 ditambah empat kode abstain.

**Saran penyajian.** Lencana pita berupa teks berwarna, bukan gradasi warna pada seluruh kartu, dan
warna tidak pernah berdiri sendiri tanpa teks. Untuk sebaran keyakinan satu shift, dipakai strip
titik kuantil 0 sampai 1 dengan penanda batas pita, karena sebaran padat lebih jujur ditampilkan
sebagai sebaran daripada sebagai rata-rata ([VR] baris 157 sampai 159, [LV5]). Untuk antrean yang
menumpuk, dipakai tampilan umur antrean, satu baris per kartu dengan panjang sebanding lama tunggu,
karena sumber yang sama mencatat bahwa antrean yang menua cepat kehilangan nilai ([VR] baris 173,
[LV14]).

Contoh tata letak:

```
Pita keyakinan, shift malam (48 kartu)
P1 ####################  21
P2 ############ 12
P3 ######### 9
P4 ###### 6
P5  0     (menunggu syarat bagian 11)
AB ##### 5   (4 AB-1, 1 AB-2)
```

**Dasar riset penyajian.** Tiga rujukan: kategori berlabel lebih aman daripada warna tanpa teks
([K] baris 203 sampai 207, dan [VR] baris 248 soal kanal yang diproses cepat); sebaran titik untuk
data padat ([VR] baris 157, [LV5]); tampilan umur antrean untuk pekerjaan yang menunggu ([VR] baris
173, [LV14]). Alasan menolak pengukur bulat untuk pita: [VR] baris 248 mencatat sudut dan luas
bukan kanal yang diproses cepat untuk informasi kuantitatif.

**Status bukti.** Batas pita dan tabel tindakan: rancangan dokumen ini, diturunkan dari ambang
[PM1] baris 131 dan [I2] baris 152 sampai 154. Sebaran pita per shift: belum dihitung, karena
Butuh `K_tampil` per jendela yang belum diekspor. Angka 48 kartu pada contoh tata letak adalah
ilustrasi tata letak, bukan hasil hitung, dan diberi label demikian.

**Salah tafsir yang harus dicegah.**
1. Pita dibaca sebagai tingkat bahaya. Pencegahan: nama pita memakai kata bukti dan tindakan, bukan
   kata bahaya, dan tidak ada warna merah kecuali kartu sudah punya label manusia-peninjau.
2. P2 dikira "sistem bilang aman". Pencegahan: teks P2 "indikasi lemah, pantau", bukan "normal".
3. P5 kosong dikira fitur rusak. Pencegahan: label "(menunggu syarat bagian 11)" tampil di tempat
   pita itu.
4. Pindah pita karena batas atas berubah dikira perubahan kondisi. Pencegahan: setiap perubahan pita
   mencatat penyebabnya, jendela atau batas kelas.

**Cara menguji.**
1. Uji batas: nilai 0,1999 masuk P1, 0,20 masuk P2, 0,495 masuk P3, 0,61 masuk P4. Uji dengan lima
   nilai pada tiap batas.
2. Uji pengunci: kepala L2 dengan `K_tampil` 0,61 harus diturunkan ke P3, dan penurunan dicatat pada
   `alasan_pengunci`.
3. Uji P5: kelas dengan SK 61 tidak boleh pernah menghasilkan P5.
4. Uji hitung: jumlah kartu pada diagram batang harus sama dengan jumlah jendela yang diproses.
5. Uji aksesibilitas: setiap pita harus terbaca tanpa warna, diuji dengan tangkapan layar skala abu.

### 7.4 DSS-04 Kurva reliabilitas dan ECE

**ID dan nama fitur.** DSS-04, "Kurva reliabilitas dan ECE per kepala". Terkait W1-03 dan usulan
kalibrasi di [K] baris 448 sampai 500.

**Tujuan.** Menjawab apakah angka persen pada kartu berarti frekuensi atau hanya urutan. Tanpa
fitur ini, seluruh persen di DSS-01 dan DSS-03 hanya bisa dibaca sebagai peringkat. Penggunanya
insinyur yang harus memutuskan apakah layak memasang ambang numerik, dan pengawas yang menilai
kesiapan sebelum naik tier.

**Menggambarkan apa.** Menggambarkan kesesuaian antara peluang yang dinyatakan dan frekuensi nyata.
Titik di atas diagonal berarti model terlalu ragu, titik di bawah berarti terlalu percaya diri,
titik di diagonal berarti sesuai. ECE merangkum jarak rata-rata itu menjadi satu angka, dan angka
kecil berarti sesuai, sedangkan angka besar berarti meleset. ECE turun tidak otomatis berarti model
lebih berguna, karena bisa turun hanya karena model jarang menyala (contoh `shk` pada bagian 5.4).

**Pengguna dan momen pakai.** Insinyur pengeboran: sekali per kampanye evaluasi, saat memutuskan
ambang. Pengawas: saat rapat kesiapan, 1 kali per bulan. Peneliti internal: setiap kali model
dilatih ulang, beberapa kali per bulan, untuk membandingkan fold.

**Masukan.** Pasangan `(skor, label)` per jendela per fold. Saat ini yang tersedia hanya agregat
`metrik_segmen` berisi `tp`, `fp`, `fn`, `tn`, `presisi`, `recall`, `far`, `n` untuk 24 kepala
(dihitung di bagian 10). Satuan: peluang 0 sampai 1 dan label 0 atau 1. Rentang: `n` dari 95 sampai
95.925. Cara memperoleh: menambah ekspor dari `train_lowo` di [P] baris 435, yang saat ini tidak
menyimpan pasangan skor dan label.

**Algoritma.** Nama metode: kurva reliabilitas berbinned dan expected calibration error.

```
bin m: B_m = { i : skor_i di bin m }, 10 bin kuantil
conf(B_m) = rata-rata skor di B_m
acc(B_m)  = rata-rata label di B_m
ECE = jumlah_m ( |B_m| / n ) x | acc(B_m) - conf(B_m) |
MCE = maks_m | acc(B_m) - conf(B_m) |
```

Untuk kepala biner dipakai bentuk satu suku pada bagian 5.4. Parameter: 10 bin, minimal 50 sampel
per bin, uji ketahanan 5 dan 20 bin. Ambang tampil: ECE 0,05. Alasan memilih 10 bin kuantil: sama
dengan jumlah kuartil pada normalisasi [L] baris `L-18`, sehingga satu berkas tidak memakai dua
konvensi binning, dan [K] baris 454 sudah mengusulkan angka yang sama.

**Workflow.**
1. Ekspor `(skor, label, fold, kepala)` dari pipeline ke berkas terpisah per kepala.
2. Bekukan 10 bin dan catat jumlahnya di kepala laporan sebelum grafik dibuka.
3. Buang bin dengan anggota kurang dari 50, gabungkan ke tetangga, catat jumlah bin final.
4. Hitung `conf`, `acc`, `ECE`, `MCE`, dan arah penyimpangan per kepala.
5. Ulangi dengan 5 dan 20 bin, bandingkan arah.
6. Simpan satu gambar per kepala ditambah satu tabel ringkas.
7. Tempelkan badge "terkalibrasi" atau "belum terkalibrasi" ke kartu DSS-05 sesuai ambang 0,05.

**Keluaran.** Bentuk data: per kepala, satu vektor `conf` dan `acc` sepanjang jumlah bin, satu
bilangan `ECE`, satu bilangan `MCE`, satu tanda arah, dan satu label kalibrasi. Satuan: peluang dan
selisih peluang. Rentang: 0 sampai 1 untuk `ECE` dan `MCE`; arah bernilai ragu, percaya diri, atau
datar. Arti: `ECE` 0,0151 untuk `vib.rule_display` berarti selisih rata-rata 1,5 poin persen antara
peluang dan frekuensi.

**Saran penyajian.** Diagram sebar dengan diagonal acuan, satu panel per kepala, sumbu x peluang
prediksi dan sumbu y fraksi positif, ditambah histogram tipis di bagian bawah untuk jumlah sampel
per bin. Alasan: bentuk ini adalah bentuk baku yang membuat "peluang 0,8 berarti 80 persen" bisa
diperiksa mata ([VR] baris 165, [LV1]); jumlah sampel ditampilkan karena bin berisi sedikit sampel
membuat kurva liar dan mudah salah dibaca; dan skor tunggal tidak ditampilkan sendirian karena
mencampur tiga hal ([VR] baris 167).

Contoh tata letak:

```
vib.rule_display          ECE 0,0151   MCE 0,0301   arah: ragu     n 1.989
  1.0 |            o
      |        o
  0.5 |    o
      | o
  0.0 +-------------------  jumlah bin 2 (biner)
      0.0   0.5   1.0
```

**Dasar riset penyajian.** Bentuk kurva reliabilitas dan batasannya diambil dari [VR] baris 165 dan
167 dengan sumber [LV1], yaitu bahwa peluang harus dibaca sebagai frekuensi dan bahwa skor tunggal
seperti Brier mencampur kalibrasi dengan daya pisah. Keputusan menampilkan jumlah sampel per bin
mengikuti larangan yang sama: tanpa jumlah, pembaca tidak bisa tahu apakah titik liar itu berarti.

**Status bukti.** ECE biner untuk tiga kepala: terhitung dari data nyata, dengan TP, FP, dan n dari
[J] dan keluarannya ditempel di bagian 6.2. Kurva reliabilitas 10 bin: rancangan, menunggu ekspor
pasangan skor dan label. Ambang 0,05: keputusan dokumen ini, belum disetujui.

**Salah tafsir yang harus dicegah.**
1. ECE kecil dikira model bagus. Pencegahan: ECE selalu tampil bersama presisi, recall, dan n, dan
   contoh `shk` (ECE 0,0043 dengan recall rendah) dicetak di kartu sebagai peringatan.
2. Kurva dibaca sebagai kurva ROC. Pencegahan: judul sumbu ditulis penuh, dan tidak ada label AUC.
3. ECE dibandingkan antar engine dengan jumlah sampel berbeda. Pencegahan: `n` selalu ditampilkan,
   dan perbandingan hanya diizinkan dalam satu domain.
4. Kalibrasi dikira memperbaiki daya pisah. Pencegahan: catatan "kalibrasi tidak menambah informasi,
   ia hanya menyelaraskan bacaan".

**Cara menguji.**
1. Uji identitas: model yang selalu mengeluarkan 0,5 harus menghasilkan ECE sama dengan selisih
   terhadap base rate.
2. Uji direktivitas: naikkan semua skor 0,1 tanpa mengubah label, ECE harus naik dan arah harus
   menjadi percaya diri.
3. Uji stabilitas bin: 5, 10, 20 bin, arah harus sama; bila berubah, kesimpulan tidak boleh dipakai.
4. Uji jumlah sampel: kepala dengan `n` kecil harus diberi penanda dan tidak boleh mengubah urutan.
5. Uji reproduksi: hitung ulang tiga baris bagian 5.4 dengan `awk`, hasilnya harus 0,0151 / 0,0106 /
   0,0043.

### 7.5 DSS-05 Kartu keyakinan: pita warna, persen, dan perilaku saat keyakinan rendah

**ID dan nama fitur.** DSS-05, "Kartu keyakinan". Ini pembungkus tampilan untuk DSS-01 sampai DSS-04,
dan pasangannya di katalog adalah KEP-02 ([K] baris 613) serta gaya kartu di [K] baris 203 sampai
207.

**Tujuan.** Menyatukan angka, pita, dan alasan dalam satu kartu yang tidak bisa dibaca salah, serta
menentukan apa yang terjadi ketika keyakinan rendah atau tidak ada. Penggunanya operator yang melihat
kartu di layar tanpa membuka dokumen lain.

**Menggambarkan apa.** Menggambarkan satu klaim pada satu jendela, lengkap dengan mutu buktinya.
Naik pita mengubah tindakan yang dianjurkan. Turun pita, atau pindah ke abstain, mengubah perilaku
kartu: dari kartu penuh menjadi kartu redup, dan dari kartu redup menjadi kartu "menunggu data".

**Pengguna dan momen pakai.** Operator monitoring: setiap kali membuka halaman, puluhan kartu per
shift. Supervisor: saat memeriksa antrean, beberapa kali per shift. Auditor internal: saat menguji
ulang keputusan, sekali per bulan.

**Masukan.** Keluaran DSS-01 (`K_tampil`, jumlah kepala dinilai), DSS-02 (`K_max`, tiga komponen),
DSS-03 (`pita`, `tindakan`), DSS-04 (`ECE`, label kalibrasi), ditambah `badge_far`, `lead_menit`,
dan `n_windows` dari [J]. Satuan: campuran, dan setiap angka pada kartu wajib mencantumkan satuannya.
Rentang: `K_tampil` 0 sampai 0,61 hari ini; `lead_menit` 0 sampai 150 ([J] baris 884 untuk 42,8 dan
baris 1.141 untuk rentang canary).

**Algoritma.** Nama metode: aturan tampilan berjenjang (bukan model).

```
jika abstain (AB-1..AB-4)  -> kartu redup, pola garis miring, tanpa angka, alasan wajib
selain itu
  jika pita P1             -> angka disembunyikan, hanya nama pita dan jumlah kepala
  jika pita P2             -> angka tampil kecil, tanpa tombol tindakan, alasan batas atas dibuka
  jika pita P3             -> angka tampil, tindakan "periksa", badge FAR di samping angka
  jika pita P4 atau P5     -> angka tampil besar, tindakan "antrean kerja" atau "eskalasi",
                              tiga komponen S_A S_B S_C dan `lead_menit` tampil
  selalu: badge kalibrasi, jumlah kepala dinilai, dan tanggal rujukan batas kelas
```

Parameter: lima pita dari DSS-03, empat kode abstain dari bagian 4.2, dan urutan prioritas
penjelasan (alasan batas kelas lebih dulu daripada alasan kepala). Ambang perilaku: keyakinan rendah
didefinisikan sebagai P1 dan P2, yaitu `K_tampil` kurang dari 0,40. Alasan memilih: di bawah 0,40
tindakan lapangan belum sepadan dengan biaya, sehingga kartu tidak boleh mendorong tindakan.

**Workflow.**
1. Terima objek dari DSS-01 sampai DSS-04.
2. Tentukan status: abstain atau berpita.
3. Susun tiga zona kartu: baris judul (nama klaim, pita, persen), baris bukti (jumlah kepala, badge
   kalibrasi, badge FAR), baris alasan (batas kelas, komponen, tanggal).
4. Terapkan aturan tampilan sesuai pita.
5. Urutkan kartu: pita tertinggi lebih dulu, lalu `lead_menit` terkecil, lalu jendela terbaru.
6. Kelompokkan kartu abstain di bawah, dengan penanda "menunggu data", tidak masuk urutan kerja.
7. Catat setiap klik tindakan ke log keputusan (fitur linimasa keputusan di [K] rumpun 4).

**Keluaran.** Bentuk data: satu objek kartu per klaim per jendela, berisi `pita`, `persen` (bulat,
0 sampai 100), `status` (berpita atau abstain), `alasan`, dan `tindakan`. Satuan: persen untuk angka,
kategori untuk pita dan tindakan. Arti: persen 61 berarti `K_tampil` 0,61, bukan peluang 61 persen
kerusakan.

**Saran penyajian.** Tiga lapis. Pertama, lencana pita bertekstur dan berlabel, bukan gradasi kartu
penuh, karena warna tanpa teks gagal di skala abu ([K] baris 203 sampai 207). Kedua, batang mendatar
0 sampai 1 dengan garis batas kelas, karena panjang dan posisi adalah kanal terbaik untuk besaran
([VR] baris 248, [LV7]). Ketiga, persen sebagai teks di ujung batang, bukan di dalam donat, karena
donat memakai sudut dan luas untuk besaran yang sebenarnya butuh perbandingan panjang ([VR] baris
248). Untuk keyakinan rendah, kartu tetap ada di halaman tetapi diredupkan dan tanpa tombol
tindakan, sehingga tidak menarik klik yang tidak perlu.

Contoh tata letak dalam teks:

```
+---------------------------------------------------------------+
| hyd K-i  jendela 14:32:00-14:33:00      [ P4  Keyakinan kuat ]|
|                                                               |
|  [================|----]  61%          batas kelas 61         |
|   kepala dinilai 3 dari 3        badge FAR: 12,4 per 24 jam   |
|   S_A 0,75   S_B 0,35   S_C 0,75        lead 42,8 menit       |
|   belum terkalibrasi (ECE belum diukur)        rujukan 2026-10 |
+---------------------------------------------------------------+

+---------------------------------------------------------------+
| hyd K-ii jendela 14:32:00        [ menunggu data ]   AB-1     |
|   tidak dinilai menurut desain: kanal K-ii belum tersedia     |
+---------------------------------------------------------------+
```

**Dasar riset penyajian.** Empat rujukan: panjang dan posisi untuk besaran kuantitatif, dan penolakan
sudut atau luas ([VR] baris 248, [LV7]); tabel dan angka ringkas untuk nilai yang harus dibaca tepat
([VR] baris 46, [LV6]); label wajib pada status yang bisa memicu tindakan ([K] baris 203 sampai 207);
dan prinsip bahwa pilihan visual ditentukan pertanyaan yang ingin dijawab ([VR] baris 10, [LV13]),
yang di sini berarti "apakah bukti cukup untuk bertindak" dan bukan "seberapa besar risikonya".

**Status bukti.** Tata letak dan aturan perilaku: rancangan dokumen ini. Angka pada contoh tata letak
diambil dari perhitungan nyata bagian 6 untuk `K_tampil` 61 dan batas kelas 61, sedangkan `lead_menit`
42,8 diambil dari [J] baris 884, dan `badge_far` 12,4 per 24 jam dari [J] baris 88. Kartu itu sendiri
belum dirender, karena halaman belum dibangun.

**Salah tafsir yang harus dicegah.**
1. Kartu redup dikira kartu rusak. Pencegahan: teks alasan selalu ada, dan kartu redup tetap
   menampilkan nama pita.
2. Kartu abstain dikira nilai nol. Pencegahan: angka diganti tanda dan alasan, dan abstain diberi
   warna sendiri, bukan warna pita P1.
3. Persen dibaca sebagai peluang. Pencegahan: label "keyakinan bukti" dan badge kalibrasi.
4. Tombol tindakan pada P2 tetap diklik. Pencegahan: tombol tidak dirender pada P1 dan P2.

**Cara menguji.**
1. Uji render: seluruh kombinasi lima pita dan empat kode abstain dirender, sembilan keadaan.
2. Uji aksesibilitas: tangkapan layar skala abu, setiap keadaan masih terbaca.
3. Uji urutan: kartu P4 harus di atas P2, dan abstain di bawah semua kartu berpita.
4. Uji konsistensi angka: persen pada kartu harus sama dengan `round(100 x K_tampil)`.
5. Uji klik: pada P1 dan P2 tidak ada elemen yang bisa memicu tindakan.

## 8. Peta ke katalog fitur dan satu konflik yang diselesaikan

| Fitur dokumen ini | Kode di [K] | Hubungan |
|---|---|---|
| DSS-01 | KEP-02 ([K] baris 613) | KEP-02 memakai skala 0 sampai 100; DSS-01 memakai 0 sampai 1 dengan fungsi konversi tunggal |
| DSS-02 | KEP-03, KEP-04 ([K] baris 620 sampai 630) | DSS-02 hanya menghitung angka batas; KEP-03 dan KEP-04 yang menampilkan tier dan alasannya |
| DSS-03 | KEP-04, KEP-07 ([K] baris 665) | DSS-03 menetapkan batas pita; KEP-07 memakai pita itu untuk panel ketidaksepakatan |
| DSS-04 | Usulan kalibrasi ([K] baris 448 sampai 500) | DSS-04 menetapkan rumus, bin, dan ambang; katalog memuat usulannya |
| DSS-05 | KEP-02, gaya kartu ([K] baris 203) | DSS-05 menetapkan perilaku tampilan; katalog menetapkan isi kartu |

Konflik yang perlu ditutup, karena dua dokumen bisa memakai angka berbeda untuk hal yang sama:
[K] memakai skala 0 sampai 100 dan dokumen ini memakai 0 sampai 1. Keputusan: data disimpan 0 sampai
1 dengan empat desimal, tampilan memakai persen bulat, dan tidak ada tempat lain yang boleh
menghitung ulang dari 0 sampai 100 kecuali fungsi konversi tunggal. Alasan: [I2] sudah memakai
0 sampai 100 untuk SK, sehingga konversi harus eksplisit dan satu arah, bukan dua definisi yang
berjalan sendiri. Rumus yang sama dipakai dua kali dengan satuan berbeda adalah cara paling cepat
menghasilkan dua angka yang berselisih.

## 9. Batas tanggung jawab DSS-1

Yang ditetapkan dokumen ini: skala keyakinan, bobot kepala, batas atas per kelas, lima pita, empat
kode abstain, rumus dan prosedur ECE, serta perilaku kartu.

Yang tidak ditetapkan, dan menjadi milik kartu lain:
1. Tingkat alarm dan notifikasi: milik keputusan tier di [EVC] dan [J] `auto_critical_alarm_slots`
   (baris 1.414, nilainya 0).
2. Definisi label dan horizon: milik [P] `label_pos` dan `persistence_horizon_ref` per kepala.
3. Ambang operasi per kepala: milik blok `ambang_operasi` di [J], bukan milik dokumen ini.
4. Prioritas sumur dan anggaran maintenance: milik `nilai_maintenance` ([J] baris 1.665 sampai 1.754).
5. Definisi pita warna akhir di kode tampilan: milik dokumen desain antarmuka, dengan syarat mengikuti
   batas angka dan larangan warna di bagian 4.

<!-- VERIFIKASI-DISINI -->

## 11. Syarat yang dibutuhkan agar pita dan kalibrasi bisa naik

Setiap baris menulis apa yang dibutuhkan, siapa pemiliknya, apa yang terbuka setelah tersedia, dan
bagaimana memverifikasinya. Tidak ada baris yang berhenti pada pernyataan bahwa sesuatu belum ada.

| Kode | Syarat | Pemilik | Yang terbuka setelah tersedia | Cara memverifikasi |
|---|---|---|---|---|
| S-1 | Ekspor pasangan `(skor, label, fold, kepala)` dari `train_lowo` ([P] baris 435) | pipeline | Kurva reliabilitas 10 bin dan ECE sungguhan untuk 24 kepala berskor; badge kalibrasi berubah dari "belum" menjadi terukur | Berkas ekspor memuat minimal `n` baris sama dengan `n` di `metrik_segmen` tiap kepala, dan histogram jumlah per bin berjumlah sama dengan `n` |
| S-2 | Pengukuran lapisan B per kelas: B1 jaminan dan FAR pada level operasional | pemilik kampanye lapangan | S_B naik dari 0,20 atau 0,35 ke 1,00 pada kelas yang lolos, SK naik di atas 70, potong [I4] baris 233 lepas, dan P4 serta P5 bisa dipakai | SK hitung ulang per kelas melebihi 70 dan dokumen B1 menyebut angka terukur dengan tanggal |
| S-3 | Baris SK terpisah untuk `stuck` K-ii dan `tool_wear` K-ii | pemilik skor keyakinan | Menghapus label "batas atas mengikuti baris kelas" pada dua klaim | Dua baris baru di [I2] dengan komponen sendiri, dan `awk` menghasilkan dua nilai berbeda dari baris kelas |
| S-4 | Kanal K-ii untuk `hyd` | pemilik data sensor | AB-1 pada `hyd` K-ii berubah menjadi skor, dan klaim itu masuk urutan kerja | `jumlah w_h` lebih dari 0 dan `status` kepala bukan lagi tidak tersedia |
| S-5 | Kanal SSI terisi, dari 5.268 dari 5.455 jendela kosong ([J] baris 247) | pemilik data sensor | AB-2 pada `ssi` lepas, dan `rule_display` ssi bisa dipakai | Rasio `n_nodata / n_windows` turun di bawah 0,50 pada run berikutnya |
| S-6 | Uji kalibrasi lintas well, bukan hanya lintas fold | peneliti internal | Klaim G5 di [I2] baris 131 bisa ditutup, dan ECE boleh dipakai sebagai janji frekuensi | ECE pada well yang tidak dipakai latih berada dalam selisih yang sudah dibekukan sebelum uji |
| S-7 | Persetujuan ambang tampil ECE 0,05 dan lima batas pita | pemilik produk | Pita dan badge kalibrasi menjadi keputusan resmi, bukan usulan dokumen | Catatan persetujuan bertanggal, dan kode membaca satu berkas konfigurasi, bukan angka yang ditulis di dua tempat |
| S-8 | Halaman kartu dibangun | pemilik antarmuka | Sembilan keadaan tampilan (lima pita dan empat abstain) bisa diuji di layar | Tangkapan layar skala abu tiap keadaan, dan uji klik pada P1 dan P2 tidak memicu tindakan |

Urutan yang paling besar dampaknya: S-1 lebih dulu, karena tanpa pasangan skor dan label, semua
angka keyakinan tetap berstatus peringkat dan tidak boleh dicetak sebagai persen frekuensi. S-2
paling besar dampaknya pada pita, karena hanya S-2 yang bisa membuka P5.

## 12. Yang belum diverifikasi

Ditulis apa adanya supaya pembaca berikutnya tidak menganggap seluruh isi dokumen sudah teruji.

1. Skor per jendela tidak ada di [J]. Contoh E1, E2, dan E3 memakai kombinasi kepala menyala yang
   ditetapkan sebagai skenario, bukan keluaran pipeline. Angka `K_max` dan `K_tampil` pada contoh itu
   terhitung benar terhadap skenario tersebut, bukan terhadap jendela nyata.
2. ECE 10 bin belum pernah dihitung. Yang terhitung hanya ECE biner satu bin untuk tiga kepala
   (bagian 5.4), dan angka masuknya TP, FP, serta `n` dibaca dari [J], tidak dihitung ulang dari data
   mentah.
3. Berkas [PM1] dan [L] hanya dibuka lewat pencarian baris, tidak dibaca utuh. Rujukan [PM1] baris
   131, [L] baris `L-18`, `L-21`, `L-22`, dan [L] baris 121 diambil dari baris hasil pencarian, dan
   isi penuhnya belum saya cocokkan kalimat per kalimat.
4. Berkas [K] dibaca baris 1 sampai 500. Rujukan ke [K] baris 613, 620 sampai 630, 665, 673, dan 448
   sampai 500 berasal dari pencarian judul dan potongan, bukan pembacaan utuh.
5. Ambang 0,05 untuk ECE, lima batas pita, dan bobot kepala belum disetujui siapa pun. Ketiganya
   usulan dokumen ini dengan alasan tertulis, dan semuanya bisa diubah tanpa merusak rumus.
6. Kutipan Guo dan kawan-kawan (2017) Persamaan (3) berasal dari pencarian web, dan berkas PDF-nya
   tidak dibuka baris per baris. Yang saya periksa adalah keberadaan rumus ECE dalam bentuk yang
   sama, bukan nomor halaman cetaknya.
7. Angka `lead_menit` 42,8 dan `badge_far` 12,4 per 24 jam pada contoh tata letak DSS-05 dibaca dari
   [J] baris 884 dan 88, tetapi tidak saya hitung ulang dari keluaran model.
8. Tabel 27 kepala dan 7 engine dihitung dengan `grep -c` pada rentang baris berkas [J] (bagian 10),
   bukan dengan membaca ulang tiap entri satu per satu di run ini.
9. Tidak ada halaman yang dirender, sehingga perilaku kartu pada DSS-05 adalah rancangan tertulis.

Bagian 10 menempelkan keluaran perintah yang benar-benar dijalankan pada run ini, termasuk perintah
yang memeriksa berkas ini sendiri.

