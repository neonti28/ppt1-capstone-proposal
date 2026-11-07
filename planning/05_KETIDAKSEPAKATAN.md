# DSS-3 SPESIFIKASI PETA KETIDAKSEPAKATAN ANTAR MESIN

Kartu: `t_cd5e386f` (DSS-3). Disusun 2026-10-31 pada workspace `/mnt/d/Capstone 1(v2)`.
Keluaran: satu berkas markdown ini. Tidak ada berkas .py, .html, .json, atau .csv yang dibuat di
folder `planning/`.

Kerangka wajib yang mengikat dokumen ini sama dengan kartu DSS-1 dan DSS-2: alarm otomatis bukan
tujuan, setiap angka bersumber, tidak ada klaim tanpa bukti, kekurangan data dikemas menjadi fitur,
setiap fitur punya lima field wajib, penutup berupa syarat bukan penyerahan, dan tanpa tanda pisah
panjang.

Notasi angka: naskah ini memakai koma desimal (notasi Indonesia). Bentuk asli di dalam berkas JSON
memakai titik desimal, jadi pencarian teks di JSON harus memakai titik (contoh `0.9444`), sedangkan
pencarian di dokumen ini memakai koma (contoh `0,9444`).

---

## 0. Ringkasan

Ketidaksepakatan bukan cacat yang harus dirapikan menjadi satu label. Pada sistem ini
ketidaksepakatan adalah keluaran utama, karena tujuh mesin dan 27 head memberi putusan pada data yang
sama dengan tugas, ambang, dan cakupan sumur yang berbeda. Enam angka ringkas yang menjadi dasar
seluruh dokumen:

1. Lapisan peringatan L1 berisi 11 head ([JSON] baris 1413), tetapi hanya 7 fungsi keputusan berbeda,
   karena 4 pasangannya identik sampai ke jumlah aktif, true positive, dan alarm palsu (bagian 5.1).
2. Di mesin hyd, tiga head pada jendela yang sama memberi tiga jawaban berbeda: rule menyala 975
   jendela, persistence 876, dan hibrida 626 ([JSON] baris 741, 775, dan 812). Irisan rule dengan
   persistence tepat 626, sehingga 349 jendela hanya rule dan 250 jendela hanya persistence.
3. Derajat kesepakatan status di seluruh jendela terlihat tinggi hampir di semua mesin (92,47 sampai
   99,43 persen), padahal pada kelas positif angkanya jatuh sampai 23,81 persen (shk) dan 0,00 persen
   untuk Jaccard (ssi). Angka kesepakatan tanpa penyebut kelas adalah angka menipu (bagian 4.4).
4. Empat head tidak pernah menyala pada segmennya: ssi rule, ssi hibrida, ssi rf (0 dari 5.455), dan
   shk rf (0 dari 11.205) ([JSON] baris 232, 294, 321, dan 470). Kesepakatan 100 persen dengan head
   seperti ini berarti dua pihak sama-sama diam, bukan dua pihak sepakat.
5. Pemangkasan selalu berharga: hyd menurunkan alarm 35,79 persen dengan presisi naik 0,2017 tetapi
   recall turun 0,1052; tool_wear menurunkan alarm 93,11 persen dengan recall turun 0,6666 (bagian
   5.2 dan 4.3).
6. Tidak ada satu pun slot alarm otomatis di prototipe ([JSON] baris 1414, nilainya 0), dan keputusan
   akhir berada pada manusia. Peta ketidaksepakatan adalah alat bantu manusia memutuskan, bukan mesin
   yang memutuskan.

---

## 1. Kepatuhan kerangka wajib

| Butir kerangka | Cara dipenuhi di dokumen ini | Bukti |
|---|---|---|
| 1. Alarm otomatis bukan tujuan | Semua fitur berbentuk panel informasi dan penanda konflik untuk dibaca manusia. Tidak ada fitur yang memicu tindakan sendiri. Ditegaskan oleh `auto_critical_alarm_slots = 0` ([JSON] baris 1414). | bagian 0 butir 6, bagian 9 |
| 2. Setiap angka bersumber | Angka proyek memakai pasangan berkas dan baris. Singkatan berkas didefinisikan di bagian 2.1. Angka literatur memakai kode LV1 sampai LV16 yang sama dengan katalog dan dokumen riset visualisasi. | bagian 2, sepanjang naskah |
| 3. Tidak mengklaim tanpa bukti | Setiap tabel angka punya blok perintah dan keluaran di bagian 2.2 dan 2.3. Angka yang hanya bisa dihitung sebagai rentang ditulis sebagai rentang, bukan angka tunggal. | bagian 2.2, 2.3, 4.3 |
| 4. Kekurangan data menjadi fitur | Head yang belum dijalankan (L3) dan head yang tidak pernah menyala diperlakukan sebagai keadaan yang ditampilkan, masing-masing punya lencana sendiri. Bukan dikeluhkan. | bagian 5.4, fitur DSS3-02 |
| 5. Lima field wajib per fitur | Setiap fitur di bagian 9 memuat pengguna, momen pakai, masukan, keluaran, dan status bukti, ditambah delapan butir wajib lain dari kartu. | bagian 9 |
| 6. Tidak menutup dengan kata menyerah | Penutup berupa daftar syarat terukur yang dibutuhkan agar bagian yang belum terhitung bisa dihitung. | bagian 13 |
| 7. Keluaran hanya markdown | Satu berkas: `planning/05_KETIDAKSEPAKATAN.md`. Skrip hitung dijalankan dari luar folder `planning/` dan tidak diserahkan sebagai deliverable. | bagian 15 |
| 8. Tanpa tanda pisah panjang | Diperiksa dengan `grep -cP` untuk U+2014 dan U+2013, keduanya harus 0. | bagian 15 |

---

## 2. Berkas masukan dan bukti pembacaan

### 2.1 Berkas yang dibuka, dengan ukuran byte dan jumlah baris

```
$ cd "/mnt/d/Capstone 1(v2)" && stat -c '%s bytes  %n' scratch/v9_i1/v9_i1_RESULTS.json planning/01_KATALOG_FITUR.md planning/02_RISET_VISUALISASI.md docs/V9_EVAL_C_LAYERC.md
57555 bytes  scratch/v9_i1/v9_i1_RESULTS.json
166662 bytes  planning/01_KATALOG_FITUR.md
32141 bytes  planning/02_RISET_VISUALISASI.md
23153 bytes  docs/V9_EVAL_C_LAYERC.md
$ wc -l scratch/v9_i1/v9_i1_RESULTS.json planning/01_KATALOG_FITUR.md planning/02_RISET_VISUALISASI.md docs/V9_EVAL_C_LAYERC.md
  1758 scratch/v9_i1/v9_i1_RESULTS.json
  2780 planning/01_KATALOG_FITUR.md
   335 planning/02_RISET_VISUALISASI.md
   267 docs/V9_EVAL_C_LAYERC.md
  5140 total
```

Singkatan berkas yang dipakai di seluruh naskah:

| Kode | Berkas | Byte | Baris | Peran di dokumen ini |
|---|---|---:|---:|---|
| [JSON] | `scratch/v9_i1/v9_i1_RESULTS.json` | 57.555 | 1.758 | sumber utama semua angka head, jumlah aktif, dan metrik segmen |
| [KAT] | `planning/01_KATALOG_FITUR.md` | 166.662 | 2.780 | kode fitur KEP-08 dan CMP-07 yang diperluas dokumen ini |
| [VR] | `planning/02_RISET_VISUALISASI.md` | 32.141 | 335 | dasar riset penyajian, kode LV1 sampai LV16 |
| [EVC] | `docs/V9_EVAL_C_LAYERC.md` | 23.153 | 267 | tier pemakaian per klaim dan sebaran antar sumur |

Catatan pembacaan: [KAT] tidak dibaca utuh. Yang dibaca hanya potongan yang relevan, diambil dengan
`grep -n` pada kata kunci `ketidaksepakatan`, `konflik`, `kesepakatan`, lalu `read_file` pada rentang
baris 673 sampai 792 (KEP-08) dan 1982 sampai 2064 (CMP-07). Alasan: berkas itu 166.662 byte dan
sebagian besar isinya tidak dipakai kartu ini.

### 2.2 Perintah dan keluaran untuk struktur JSON

```
$ jq -r 'keys[]' scratch/v9_i1/v9_i1_RESULTS.json
decision_layer
engines
human_review_required
keputusan_akhir
meta
nilai_maintenance
profil_kapabilitas
segmen_info
$ jq -r '.engines[]|"\(.engine)  heads=\(.heads|length)"' scratch/v9_i1/v9_i1_RESULTS.json
vib  heads=4
ssi  heads=4
shk  heads=4
stuck  heads=6
hyd  heads=4
bit_wear  heads=2
tool_wear  heads=3
$ jq -r '.decision_layer.ringkasan' scratch/v9_i1/v9_i1_RESULTS.json
{"L0": 5, "L1": 11, "L2": 9, "L3": 2}
```

Tujuh mesin, 27 head, empat lapisan. Lapisan L0 sampai L3 bukan tingkat mutu, melainkan peran:
L0 baseline, L1 peringatan berpengawas, L2 tren dan peringkat, L3 belum layak pakai. Pernyataan peran
ini diambil dari [EVC] baris 84 sampai 86 (legenda tier).

### 2.3 Perintah hitung dan keluarannya

Skrip hitung dijalankan dari `/home/neonti/.hermes/cache/scratch/dss3_calc.py`, yaitu di luar folder
`planning/`, sehingga tidak ada deliverable selain markdown. Keluaran lengkapnya dipakai sebagai dasar
seluruh tabel di bagian 5 dan 6. Tiga blok pertama, apa adanya:

```
$ cd "/mnt/d/Capstone 1(v2)" && python3 /home/neonti/.hermes/cache/scratch/dss3_calc.py
exit=0
====== BAGIAN 0: VERIFIKASI KONVENSI n_aktif = tp + fp ======
hyd       k2_tidak_tersedia            n_aktif=0   metrik=NULL (head tanpa metrik segmen)
bit_wear  k2_onset_belum              n_aktif=0   metrik=NULL (head tanpa metrik segmen)
tool_wear canary_3rms                 n_aktif=282 metrik=NULL (head tanpa metrik segmen)
jumlah head dengan metrik: 24 | mismatch n_aktif vs tp+fp: 0
jumlah head total: 27

====== BAGIAN 1: KESEPAKATAN STATUS SELURUH JENDELA ======
engine    head A                        head B                          n11   n10   n01    n00 KS_status%
vib       rule_display                  persistence                     540     0   602    847     69.73
vib       rule_display                  hybrid_rule_and_persistence     540     0     0   1449    100.00
shk       rule_display                  persistence                     103     0   520  10582     95.36
shk       rule_display                  hybrid_rule_and_persistence     103     0     0  11102    100.00
stuck     rule_display                  persistence                     210     0   241   2750     92.47
stuck     rule_display                  hybrid_rule_and_persistence     210     0     0   2991    100.00
ssi       rule_display                  persistence                       0     0    31   5424     99.43
ssi       rule_display                  hybrid_rule_and_persistence       0     0     0   5455    100.00
hyd       rule_display                  persistence                     626   349   250   9176     94.24
tool_wear op_far_calibrated             calib_5of27                      21     0   284    164     39.45

====== BAGIAN 2: KESEPAKATAN PADA KELAS POSITIF ======
engine    head A                        head B                          n11   n10   n01    n00 KS_pos% Jaccard%
vib       rule_display                  persistence                     510     0   442    172   60.68   53.57
vib       rf_lowo                       persistence                batas n11: 801 sampai 952 ; KS_pos 71.26 sampai 98.13 ; Jaccard 71.26 sampai 97.84
vib       rf_lowo                       rule_display               batas n11: 359 sampai 510 ; KS_pos 31.94 sampai 58.81 ; Jaccard 31.94 sampai 52.42
shk       rule_display                  persistence                      55     0   176    529   76.84   23.81
shk       rf_lowo                       rule_display              batas n11: 0 sampai 0 ; KS_pos 92.76 sampai 92.76 ; Jaccard 0.00 sampai 0.00
ssi       rule_display                  persistence                       0     0     1     74   98.67    0.00
stuck     rule_display                  persistence                     194     0   112    126   74.07   63.40
stuck     rf_lowo                       e1_2of3                   batas n11: 0 sampai 2 ; KS_pos 97.94 sampai 98.97 ; Jaccard 0.00 sampai 33.33
stuck     persistence_event             e1_2of3                   batas n11: 0 sampai 2 ; KS_pos 97.94 sampai 98.97 ; Jaccard 0.00 sampai 33.33
hyd       rule_display                  persistence                     516    91    37    221   85.20   80.12
tool_wear op_far_calibrated             calib_5of27                      13     0   160     67   33.33    7.51
```

Nilai `mismatch n_aktif vs tp+fp: 0` adalah pemeriksaan penting: jumlah jendela menyala selalu sama
dengan true positive ditambah alarm palsu, pada 24 head yang punya metrik segmen. Konvensi inilah yang
membolehkan seluruh hitung himpunan di bagian 4 sampai 6.

### 2.4 Rentang waktu segmen, apa adanya

[EVC] dan [JSON] memakai indeks menit internal, bukan tanggal. [JSON] menyatakannya sendiri di
`segmen_info`:

```
"catatan_waktu": "ts_bin = indeks menit internal D1 (grid 60 dtk, +1 per menit); asal kalender TIDAK diverifikasi di sesi ini (tanda pisah panjang pada aslinya diganti titik dua di sini): jangan dibaca sebagai tanggal"
```

Konsekuensi untuk dokumen ini: semua sumbu waktu di fitur DSS3-04 harus diberi label "indeks menit"
dan tidak boleh diberi label tanggal. Jumlah jendela per segmen berbeda jauh, dari 469 (tool_wear,
jendela 1 detik) sampai 95.925 (stuck K-ii). Karena itu perbandingan antar mesin pada tingkat jendela
tidak boleh memakai nomor indeks, dan bagian 7 menjelaskan sebabnya.

---

## 3. Inventaris head per mesin dan nilainya

27 head, seluruhnya dari [JSON]. Kolom FAR memakai satuan yang tertulis di berkas: FP per 24 jam
negatif untuk jendela 60 detik, dan FP per menit negatif untuk tool_wear yang jendelanya 1 detik.
Mencampur kedua satuan itu tanpa keterangan adalah salah tafsir nomor satu yang harus dicegah, dan
karena itu satuannya ditulis di kolom, bukan di catatan kaki.

| Mesin | Head | Klaim | Tier | Lapis | n jendela | n aktif | aktif % | TP | FP | FN | Presisi | Recall | FAR | Satuan FAR |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| vib | rule_display | tunggal | PERINGATAN-BERPENGAWAS | L1 | 1.989 | 540 | 27,15 | 510 | 30 | 614 | 0,9444 | 0,4537 | 49,942 | FP/24jam |
| vib | persistence | tunggal | TREN | L0 | 1.989 | 1.142 | 57,42 | 952 | 190 | 172 | 0,8336 | 0,8470 | 316,301 | FP/24jam |
| vib | hybrid_rule_and_persistence | tunggal | PERINGATAN-BERPENGAWAS | L1 | 1.989 | 540 | 27,15 | 510 | 30 | 614 | 0,9444 | 0,4537 | 49,942 | FP/24jam |
| vib | rf_lowo | tunggal | TREN | L2 | 1.989 | 1.271 | 63,90 | 973 | 298 | 151 | 0,7655 | 0,8657 | 496,092 | FP/24jam |
| ssi | rule_display | tunggal | PERINGATAN-BERPENGAWAS | L1 | 5.455 | 0 | 0,00 | 0 | 0 | 75 | n/a | 0,0000 | 0,000 | FP/24jam |
| ssi | persistence | tunggal | TREN | L0 | 5.455 | 31 | 0,57 | 1 | 30 | 74 | 0,0323 | 0,0133 | 8,030 | FP/24jam |
| ssi | hybrid_rule_and_persistence | tunggal | PERINGATAN-BERPENGAWAS | L1 | 5.455 | 0 | 0,00 | 0 | 0 | 75 | n/a | 0,0000 | 0,000 | FP/24jam |
| ssi | rf_lowo | tunggal | TREN | L2 | 5.455 | 0 | 0,00 | 0 | 0 | 75 | n/a | 0,0000 | 0,000 | FP/24jam |
| shk | rule_display | tunggal | PERINGATAN-BERPENGAWAS | L1 | 11.205 | 103 | 0,92 | 55 | 48 | 705 | 0,5340 | 0,0724 | 6,618 | FP/24jam |
| shk | persistence | tunggal | TREN | L0 | 11.205 | 623 | 5,56 | 231 | 392 | 529 | 0,3708 | 0,3039 | 54,043 | FP/24jam |
| shk | hybrid_rule_and_persistence | tunggal | PERINGATAN-BERPENGAWAS | L1 | 11.205 | 103 | 0,92 | 55 | 48 | 705 | 0,5340 | 0,0724 | 6,618 | FP/24jam |
| shk | rf_lowo | tunggal | TREN | L2 | 11.205 | 0 | 0,00 | 0 | 0 | 760 | n/a | 0,0000 | 0,000 | FP/24jam |
| stuck | rule_display | K-i | PERINGATAN-BERPENGAWAS | L1 | 3.201 | 210 | 6,56 | 194 | 16 | 238 | 0,9238 | 0,4491 | 8,321 | FP/24jam |
| stuck | persistence | K-i | TREN | L0 | 3.201 | 451 | 14,09 | 306 | 145 | 126 | 0,6785 | 0,7083 | 75,406 | FP/24jam |
| stuck | hybrid_rule_and_persistence | K-i | PERINGATAN-BERPENGAWAS | L1 | 3.201 | 210 | 6,56 | 194 | 16 | 238 | 0,9238 | 0,4491 | 8,321 | FP/24jam |
| stuck | e1_2of3 | K-ii | TREN | L2 | 95.925 | 313 | 0,33 | 6 | 307 | 383 | 0,0192 | 0,0154 | 4,627 | FP/24jam |
| stuck | persistence_event | K-ii | TREN | L2 | 95.925 | 4 | 0,00 | 2 | 2 | 387 | 0,5000 | 0,0051 | 0,030 | FP/24jam |
| stuck | rf_lowo | K-ii | TREN | L2 | 95.925 | 42 | 0,04 | 2 | 40 | 387 | 0,0476 | 0,0051 | 0,603 | FP/24jam |
| hyd | rule_display | K-i | PERINGATAN-BERPENGAWAS | L1 | 10.401 | 975 | 9,37 | 607 | 368 | 258 | 0,6226 | 0,7017 | 55,570 | FP/24jam |
| hyd | persistence | K-i | PERINGATAN-BERPENGAWAS | L0 | 10.401 | 876 | 8,42 | 553 | 323 | 312 | 0,6313 | 0,6393 | 48,775 | FP/24jam |
| hyd | hybrid_rule_and_persistence | K-i | PERINGATAN-BERPENGAWAS | L1 | 10.401 | 626 | 6,02 | 516 | 110 | 349 | 0,8243 | 0,5965 | 16,611 | FP/24jam |
| hyd | k2_tidak_tersedia | K-ii | BELUM LAYAK PAKAI | L3 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| bit_wear | persistence | K-1 | TREN | L2 | 47.645 | 4.917 | 10,32 | 4.881 | 36 | 37 | 0,9927 | 0,9925 | 1,213 | FP/24jam |
| bit_wear | k2_onset_belum | K-2 | BELUM LAYAK PAKAI | L3 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| tool_wear | calib_5of27 | K-i | TREN | L2 | 469 | 305 | 65,03 | 173 | 132 | 67 | 0,5672 | 0,7208 | 34,585 | FP/menit |
| tool_wear | op_far_calibrated | K-i | PERINGATAN-BERPENGAWAS | L1 | 469 | 21 | 4,48 | 13 | 8 | 227 | 0,6190 | 0,0542 | 2,096 | FP/menit |
| tool_wear | canary_3rms | K-ii | TREN | L2 | 469 | 282 | 60,13 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

Sumber tiap baris: [JSON] baris 68, 102, 136, 169 (vib); 223, 251, 285, 312 (ssi); 360, 394, 428, 461
(shk); 509, 543, 577, 610, 644, 681 (stuck); 732, 766, 800, 836 (hyd); 859, 898 (bit_wear); 920,
1049, 1124 (tool_wear). Jumlah `n_aktif` tiap baris berada pada baris 77, 111, 145, 178, 232, 260,
294, 321, 369, 403, 437, 470, 518, 552, 586, 619, 653, 690, 741, 775, 812, 868, 929, 1058, 1133.

Tiga hal yang harus dibaca dari tabel ini sebelum apa pun yang lain:

1. `canary_3rms` dan kedua head L3 tidak punya metrik segmen, jadi tidak boleh diikutkan dalam
   perhitungan kesepakatan berbasis kelas positif. `canary_3rms` tetap punya jumlah aktif (282), jadi
   ikut dalam perhitungan kesepakatan status dengan tanda "tanpa kelas".
2. Sembilan head berada di jendela 60 detik dan tiga head tool_wear di jendela 1 detik. FAR kedua
   kelompok tidak sebanding.
3. `stuck` memakai dua grid berbeda di dalam satu mesin: K-i pada 3.201 jendela dan K-ii pada 95.925
   jendela. Head dari dua klaim itu tidak boleh diadu langsung; nomor indeksnya bukan peristiwa yang
   sama.

---

## 4. Definisi derajat kesepakatan

### 4.1 Tiga ukuran, dan alasan memilih ketiganya

Untuk dua head A dan B pada himpunan jendela yang sama, dengan S(A) himpunan jendela tempat head A
menyala:

| Ukuran | Rumus | Pertanyaan yang dijawab | Kelemahan yang diakui |
|---|---|---|---|
| KS_status | (n11 + n00) / n | seberapa sering dua head memberi status sama, menyala maupun padam | didominasi kelas padam; bisa tinggi karena dua-duanya diam |
| KS_pos | (n11_pos + n00_pos) / pos | seberapa sering dua head sepakat pada jendela berlabel positif | hanya sah bila label positifnya sama untuk kedua head |
| Jaccard positif | n11_pos / (TP_A + TP_B − n11_pos) | seberapa besar irisan true positive dibanding gabungannya | menghukum perbedaan ukuran cakupan, bukan hanya perbedaan putusan |

n11 berarti kedua head menyala, n10 berarti hanya A, n01 berarti hanya B, n00 berarti kedua padam.
Subskrip pos berarti perhitungan dibatasi pada jendela berlabel positif.

Alasan memakai tiga ukuran sekaligus: satu angka tidak cukup. Pada mesin ssi, KS_status bernilai 99,43
persen sementara Jaccard positif bernilai 0,00 persen ([JSON] baris 232 dan 260). Angka pertama
mengatakan "hampir selalu sama", angka kedua mengatakan "tidak pernah sepakat saat ada kejadian".
Keduanya benar, dan yang kedua yang berguna untuk keputusan.

### 4.2 Dasar hitung: dari metrik segmen ke himpunan

Setiap head punya `metrik_segmen` dengan `pos`, `neg`, `tp`, `fp`, `fn` ([JSON], blok metrik tiap
head). Karena `n_aktif = tp + fp` berlaku pada 24 head tanpa kecuali (bagian 2.3), jumlah jendela
menyala terbaca langsung dari hitungan mentah, bukan dari persentase yang dibulatkan. Seluruh isi
bagian 5 dan 6 dihitung dari lima angka itu, ditambah satu deklarasi definisi per mesin.

### 4.3 Apa yang dapat dan belum dapat dihitung dari berkas ini

| Keadaan | Dasar | Yang dilaporkan |
|---|---|---|
| Dua head identik | metrik segmen sama persis dan jumlah aktif sama | angka tunggal, tepat |
| A himpunan bagian B | deklarasi definisi, misalnya hibrida = rule DAN persistence, atau ambang monoton | angka tunggal, tepat |
| Dua head lepas | hanya TP dan jumlah aktif yang diketahui | batas bawah dan batas atas, bukan angka tunggal |
| Matriks antar mesin pada tingkat jendela | butuh deret per menit yang belum diekspor | belum dihitung; syaratnya di bagian 13 |

Contoh batas atas dan bawah yang benar: vib `rf_lowo` dengan `persistence` pada kelas positif. TP
rf_lowo 973, TP persistence 952, jumlah positif 1.124 ([JSON] baris 169 dan 102). Irisan TP tidak
mungkin kurang dari 973 + 952 − 1.124 = 801 dan tidak lebih dari 952. Jadi Jaccard-nya
terletak antara 71,26 dan 97,84 persen. Menulis satu angka di sel itu akan menjadi karangan, jadi
yang ditulis adalah rentang.

### 4.4 Mengapa KS_status saja berbahaya

Empat contoh dari [JSON], semuanya nyata:

1. ssi rule dengan ssi persistence: KS_status 99,43 persen, tetapi irisan TP 0 dari 75 positif.
   Kesepakatan itu berasal dari 5.424 jendela di mana keduanya padam ([JSON] baris 232 dan 260).
2. shk rf_lowo dengan shk rule: KS_status 99,08 persen, irisan TP 0 dari 760 positif, karena rf_lowo
   tidak pernah menyala ([JSON] baris 461 dan 360).
3. tool_wear op_far_calibrated dengan calib_5of27: KS_status 39,45 persen, paling rendah di seluruh
   berkas, justru karena keduanya sama-sama aktif di banyak jendela pada alat yang sama ([JSON]
   baris 1049 dan 920).
4. vib rule dengan vib hibrida: KS_status 100,00 persen dan Jaccard 100,00 persen, karena keduanya
   fungsi yang sama untuk kelas itu ([JSON] baris 68 dan 136).

Pelajaran operasional: KS_status yang tinggi bisa berarti sepakat, bisa berarti dua-duanya diam, dan
bisa berarti dua-duanya ramai. Karena itu setiap sel matriks di fitur DSS3-01 wajib menampilkan dua
angka berdampingan (status dan kelas positif), bukan satu.

---

## 5. Tiga pola konflik

Ketiga pola di bawah didefinisikan secara operasional, masing-masing dengan contoh angka nyata dari
[JSON] dan contoh jendela yang dapat dibuka kembali. Istilah "komponen" pada kartu ini berarti head,
yaitu satu fungsi keputusan di dalam satu mesin.

### 5.1 Pola A: KEMBAR (dua head adalah fungsi yang sama)

Ciri terukur: n10 = 0, n01 = 0, dan seluruh metrik segmen identik. KS_status 100,00 persen, Jaccard
positif 100,00 persen. Ketidaksepakatan nol, dan bukan karena keduanya saling memeriksa, melainkan
karena keduanya komputasi yang sama dengan nama berbeda.

Bukti dari berkas, empat pasangan, delapan head, semuanya di lapisan L1:

| Mesin | Head A | Head B | n11 | n10 | n01 | n00 | n aktif | TP | FP | FN |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| vib | rule_display | hybrid_rule_and_persistence | 540 | 0 | 0 | 1.449 | 540 | 510 | 30 | 614 |
| ssi | rule_display | hybrid_rule_and_persistence | 0 | 0 | 0 | 5.455 | 0 | 0 | 0 | 75 |
| shk | rule_display | hybrid_rule_and_persistence | 103 | 0 | 0 | 11.102 | 103 | 55 | 48 | 705 |
| stuck | rule_display | hybrid_rule_and_persistence | 210 | 0 | 0 | 2.991 | 210 | 194 | 16 | 238 |

Sumber: [JSON] baris 68 dan 136 (vib), 223 dan 285 (ssi), 360 dan 428 (shk), 509 dan 577 (stuck).
Vib menyatakannya sendiri di medan `badge_far`: "hibrida ≡ rule utk kelas ini (E_RULE §2.1: FP =
rule)". Mesin lain tidak menyatakannya, tetapi angkanya sama, dan itulah gunanya peta ini.

Arti operasional: lapisan peringatan L1 mengklaim 11 head ([JSON] baris 1413), tetapi hanya 7 fungsi
keputusan berbeda. Empat head L1 adalah duplikat, sehingga: (a) jumlah tinjauan per shift tidak
bertambah karena adanya duplikat ini, (b) panel yang menampilkan keduanya sebagai dua baris dapat
dibaca sebagai "dua langkah konfirmasi" padahal hasilnya satu komputasi, dan (c) setiap angka
"jumlah head yang sepakat" menjadi menggelembung tanpa menambah bukti.

Contoh jendela yang dapat dibuka: vib indeks 429, 444, 472, 478, dan 489. Pada kelima jendela itu
kedua head menyala bersama ([JSON] baris 79 dan 147, medan `contoh_idx_aktif` berisi lima indeks yang
sama persis).

### 5.2 Pola B: CAKUPAN SEBAGIAN (satu head memangkas head lain)

Ciri terukur: n10 = 0 dan n01 > 0, artinya head B menyala di semua tempat head A menyala, ditambah
tempat-tempat lain. Kesepakatan bersifat asimetris: setiap alarm A adalah alarm B, tetapi tidak
sebaliknya. Harga pemangkasan selalu berupa recall yang turun, dan harga itu harus tercetak di baris
yang sama dengan kenaikan presisi.

| Mesin | A (ketat) | B (longgar) | n01 | KS_status % | Jaccard positif % | Alarm turun % | Presisi naik | Recall turun |
|---|---|---|---:|---:|---:|---:|---:|---:|
| vib | rule_display | persistence | 602 | 69,73 | 53,57 | 52,71 | +0,1108 | −0,3933 |
| shk | rule_display | persistence | 520 | 95,36 | 23,81 | 83,47 | +0,1632 | −0,2315 |
| stuck | rule_display | persistence | 241 | 92,47 | 63,40 | 53,44 | +0,2453 | −0,2592 |
| tool_wear | op_far_calibrated | calib_5of27 | 284 | 39,45 | 7,51 | 93,11 | +0,0518 | −0,6666 |

Sumber angka kolom n01 dan KS_status: bagian 2.3, blok BAGIAN 1. Sumber kolom harga: blok BAGIAN 3,
dihitung dari `precision` dan `recall` tiap head di [JSON].

Bacaan per baris, dengan satu pelajaran berbeda di masing-masing:

1. vib: rule adalah 52,71 persen dari alarm persistence. Presisi 0,9444 lawan 0,8336, recall 0,4537
   lawan 0,8470. Ini pertukaran yang jelas: rule memberi alarm yang lebih sedikit dan lebih tepat,
   dengan biaya kehilangan separuh lebih kejadian.
2. shk: pemangkasan 83,47 persen terlihat paling agresif, tetapi Jaccard positif hanya 23,81 persen,
   artinya dari seluruh true positive gabungan, hanya seperempat yang ditemukan kedua head. Pada
   kelas ini kesepakatan pada jendela positif paling rapuh di seluruh mesin rig.
3. stuck: Jaccard positif 63,40 persen, tertinggi di antara empat baris, sesuai catatan [EVC] baris
   158 bahwa presisi rule stabil 0,92 sampai 0,97 tetapi cakupannya hanya dua sumur.
4. tool_wear: pemangkasan 93,11 persen dengan recall jatuh dari 0,7208 ke 0,0542. Ini bukan mutu,
   ini titik operasi berbeda untuk tujuan berbeda, dan [JSON] menyebutnya sendiri di medan
   `batas_pemakaian`: "titik operasi layak = op_far_calibrated" untuk peringatan, sedangkan
   `calib_5of27` untuk gating inspeksi.

### 5.3 Pola C: SALING MENIADAKAN (dua head setara memberi jawaban berbeda)

Ciri terukur: n10 > 0 dan n01 > 0, dan keduanya head lapisan yang sama atau setara, sehingga pembaca
tidak punya alasan mendahulukan salah satu. Ini pola yang paling perlu ditampilkan, karena inilah
yang dimaksud [VR] bagian 5.4: "proyek ini sudah punya beberapa head setara per engine".

Kasus terjelas, mesin hyd K-i, ambang yang sama (`|z|>2` pada residu SPPA untuk rule, konfirmasi
status untuk persistence, keduanya lapisan peringatan):

| Sel | Jumlah jendela | Arti |
|---|---:|---|
| keduanya menyala | 626 | residu melewati ambang dan status bertahan |
| hanya rule_display | 349 | residu melewati ambang, status tidak bertahan |
| hanya persistence | 250 | status bertahan, residu tidak melewati ambang |
| keduanya padam | 9.176 | tidak ada indikasi menurut keduanya |
| total | 10.401 | seluruh jendela segmen hyd |

Turunan: KS_status 94,24 persen, ketidaksepakatan 599 dari 10.401 jendela atau 5,76 persen. Pada kelas
positif (865 jendela): irisan 516, hanya rule 91, hanya persistence 37, kedua padam 221. KS_pos 85,20
persen, Jaccard positif 80,12 persen, ketidaksepakatan pada kelas positif 128 dari 865 atau 14,80
persen. Sumber: [JSON] baris 732, 766, dan 800, medan `n_aktif`, `metrik_segmen.tp`, dan `definisi`
head hibrida yang menyatakan "rule(t0-1) AND persistence(t) [D-A3]".

Contoh jendela yang dapat dibuka: hyd indeks 0 sampai 4. Pada kelima jendela itu rule menyala
([JSON] baris 743, `contoh_idx_aktif` mulai dari 0) sedangkan persistence dan hibrida padam (baris 777
dan 814, keduanya mulai dari indeks 20). Inilah tampilan yang harus muncul di layar: satu baris
menyala, dua baris padam, dan satu baris alasan "syarat AND tidak terpenuhi".

Kasus kedua, ssi, dengan bentuk paling ekstrem: rule 0 dari 5.455, persistence 31. KS_status 99,43
persen tetapi Jaccard positif 0,00 persen. Satu pihak tidak pernah menyala, sehingga "kesepakatan"
adalah kesepakatan satu pihak dengan dirinya sendiri.

Kasus ketiga, stuck K-ii, tiga head prediksi onset pada 95.925 jendela: `e1_2of3` 313 aktif,
`rf_lowo` 42, `persistence_event` 4. Irisan maksimum `e1_2of3` dengan `rf_lowo` adalah 2 jendela,
sehingga Jaccard positif terletak antara 0,00 dan 33,33 persen. Ketiga head ini hampir tidak pernah
sepakat pada jendela yang sama, dan jumlahnya pun berbeda satu orde besaran ([JSON] baris 610, 644,
681).

### 5.4 Pola khusus: BISU (kesepakatan semu karena satu pihak tidak pernah menyala)

Ini bukan pola keempat yang setara, melainkan keadaan yang harus dilabeli agar tidak dibaca sebagai
pola A. Empat head tidak pernah menyala pada segmennya:

| Mesin | Head | n jendela | n aktif | Positif | Kelas masalah |
|---|---|---:|---:|---:|---|
| ssi | rule_display | 5.455 | 0 | 75 | ambang tidak pernah tercapai pada segmen ini |
| ssi | hybrid_rule_and_persistence | 5.455 | 0 | 75 | turunan rule, ikut nol |
| ssi | rf_lowo | 5.455 | 0 | 75 | skor tidak melewati ambang cetak |
| shk | rf_lowo | 11.205 | 0 | 760 | skor tidak melewati ambang cetak |

Sumber: [JSON] baris 232, 294, 321, dan 470. Bandingkan dengan dua head L3 (`hyd k2_tidak_tersedia`
dan `bit_wear k2_onset_belum`) yang juga bernilai 0 tetapi berbeda sebab: keduanya belum dijalankan,
dengan `n_windows` 0 ([JSON] baris 836 dan 898), sehingga tidak boleh diberi lencana BISU melainkan
lencana BELUM DIJALANKAN. Membedakan kedua sebab itu adalah inti butir kerangka nomor 4.

Catatan penting untuk ssi: `n_nodata` untuk CRPM adalah 62,3 persen ([EVC] baris 136), jadi keadaan
bisu pada ssi punya sebab yang terukur dan sudah dilaporkan, bukan anomali tak dijelaskan. Fitur
DSS3-02 wajib menampilkan angka itu di sebelah lencana BISU.

---

## 6. Matriks kesepakatan sampai tingkat komponen

### 6.1 Bentuk matriks yang dipakai

Matriks persegi berukuran jumlah head kali jumlah head, sel berisi Jaccard positif, diagonal 100
persen, dan sel di luar diagonal yang tidak dapat dipastikan berisi rentang. Untuk mesin dengan empat
head, satu sel tambahan diperlukan: jumlah jendela. Tata letak sel: angka Jaccard di tengah, jumlah
irisan di bawahnya dalam huruf kecil. Alasan memakai Jaccard, bukan persentase kesepakatan status:
Jaccard tidak terpengaruh jendela padam, sehingga pola BISU tidak menyamar sebagai pola A.

### 6.2 vib, empat head, 1.989 jendela, 1.124 positif

| | rule_display | persistence | hybrid | rf_lowo |
|---|---|---|---|---|
| rule_display | 100,00 | 53,57 | 100,00 | 31,94 sampai 52,42 |
| persistence | 53,57 | 100,00 | 53,57 | 71,26 sampai 97,84 |
| hybrid | 100,00 | 53,57 | 100,00 | 31,94 sampai 52,42 |
| rf_lowo | 31,94 sampai 52,42 | 71,26 sampai 97,84 | 31,94 sampai 52,42 | 100,00 |

Bacaan: baris hybrid dan baris rule identik, sesuai pola A. Sel rf_lowo terhadap rule paling longgar
(31,94 sampai 52,42), sesuai catatan [EVC] baris 117 bahwa ΔB rf terhadap persistence hanya 2 dari 4
fold, artinya rf dan persistence sering menunjuk kejadian yang sama sementara rule memangkas banyak.
Angka diagonal 100,00 adalah definisi, bukan temuan.

### 6.3 hyd, tiga head bermetrik, 10.401 jendela, 865 positif

| | rule_display | persistence | hybrid |
|---|---|---|---|
| rule_display | 100,00 | 80,12 | 85,01 |
| persistence | 80,12 | 100,00 | 93,31 |
| hybrid | 85,01 | 93,31 | 100,00 |

Jaccard hibrida terhadap rule = 516 / 607 = 85,01 persen, terhadap persistence = 516 / 553 = 93,31
persen, keduanya tepat karena hibrida adalah irisan keduanya ([JSON] baris 800, medan `definisi`).
Sel ini adalah pola C dalam bentuk paling rapi: dua pihak setara, satu pihak penengah, dan tiga angka
berbeda untuk fenomena yang sama.

### 6.4 shk, empat head, 11.205 jendela, 760 positif

| | rule_display | persistence | hybrid | rf_lowo |
|---|---|---|---|---|
| rule_display | 100,00 | 23,81 | 100,00 | 0,00 |
| persistence | 23,81 | 100,00 | 23,81 | 0,00 |
| hybrid | 100,00 | 23,81 | 100,00 | 0,00 |
| rf_lowo | 0,00 | 0,00 | 0,00 | 100,00 |

Bacaan: kolom rf_lowo seluruhnya nol (pola BISU), dan sel rule dengan persistence 23,81 persen adalah
Jaccard positif terendah di antara mesin rig yang punya dua head aktif. Artinya pada kelas bit bounce,
dua head setara hampir tidak berbagi kejadian: 55 true positive milik rule dan 231 milik persistence
hanya beririsan 55.

### 6.5 stuck, dua grid, jangan diaduk

K-i, 3.201 jendela, 432 positif:

| | rule_display | persistence | hybrid |
|---|---|---|---|
| rule_display | 100,00 | 63,40 | 100,00 |
| persistence | 63,40 | 100,00 | 63,40 |
| hybrid | 100,00 | 63,40 | 100,00 |

K-ii, 95.925 jendela, 389 positif: Jaccard `rf_lowo` dengan `e1_2of3` antara 0,00 dan 33,33 persen,
`persistence_event` dengan `e1_2of3` antara 0,00 dan 33,33 persen, `rf_lowo` dengan
`persistence_event` antara 0,00 dan 50,00 persen. Ketiganya ditulis sebagai rentang karena tidak ada
deklarasi relasi himpunan di antara mereka, dan rentang lebar itu sendiri adalah temuan: berkas ini
tidak menyimpan cukup informasi untuk menyatakan ketiga head prediksi itu sepakat atau tidak.

### 6.6 ssi dan tool_wear

ssi, 5.455 jendela, 75 positif: seluruh sel di luar diagonal bernilai 0,00 persen, kecuali diagonal.
Satu-satunya true positive milik persistence, dan tidak satu pun head lain menyala.

tool_wear, 469 jendela, 240 positif:

| | calib_5of27 | op_far_calibrated | canary_3rms |
|---|---|---|---|
| calib_5of27 | 100,00 | 7,51 | 25,16 sampai 92,46 |
| op_far_calibrated | 7,51 | 100,00 | 0,00 sampai 7,45 |
| canary_3rms | 25,16 sampai 92,46 | 0,00 sampai 7,45 | 100,00 |

Sel `calib_5of27` dengan `canary_3rms` dilebarkan rentangnya karena `canary_3rms` tidak punya metrik
segmen ([JSON] baris 1124), sehingga hanya jumlah aktifnya (282) yang diketahui. Menulis angka tunggal
di sel itu akan mengarang kelas positif yang tidak pernah dihitung.

### 6.7 bit_wear, satu head bermetrik

Tidak ada matriks yang bermakna: hanya satu head punya metrik ([JSON] baris 859) dan satu lagi belum
dijalankan (baris 898). Yang dapat ditampilkan hanyalah kartu tunggal dengan angka presisi 0,9927 dan
recall 0,9925 pada 47.645 jendela grid kedalaman. Angka setinggi itu pada head persistence adalah
tanda label sangat terkait dengan nilai sebelumnya, bukan tanda model pintar, dan [KAT] baris 764
sudah memerintahkan banner yang menyebut larangan menerjemahkan label keausan menjadi umur bit.
---

## 7. Matriks mesin lawan mesin

### 7.1 Mengapa tidak ada matriks persegi antar mesin pada tingkat jendela

Tujuh mesin tidak hidup pada grid yang sama. Jumlah jendela berbeda dari 469 sampai 95.925 (bagian 3),
rentang indeks menit berbeda dari 3.018 menit (vib) sampai 359.604 menit (stuck K-ii) ([JSON]
`segmen_info`), dan satuan FAR berbeda antara jendela 60 detik dan jendela 1 detik. Menyatukan
keduanya menjadi satu sel matriks persegi tanpa penyejajaran waktu akan menghasilkan angka yang terlihat
rapi dan salah.

Yang tersedia hari ini, dan dipakai di bawah: perbandingan pada tingkat klaim, memakai tier dan
sebaran bukti antar sumur dari [EVC]. Yang dibutuhkan untuk matriks persegi pada tingkat jendela: deret
putusan per menit dari tiap head, disimpan bersama `ts_bin`, lalu digabung pada kunci waktu yang sama.
Syaratnya ditulis di bagian 13 butir 1.

### 7.2 Matriks klaim: tujuh mesin, sepuluh baris klaim, enam sisi bukti

Tabel ini adalah "matriks mesin lawan mesin" yang jujur untuk keadaan hari ini: setiap baris satu
klaim, setiap kolom satu sisi penilaian, dan sel yang tidak terukur ditandai apa adanya.

| Klaim | Tier pemakaian | C1 ketahanan antar sumur | C2 ketidakpastian | C3 portabilitas ambang | C4 sensor | Bukti |
|---|---|---|---|---|---|---|
| vib rule | PERINGATAN-BERPENGAWAS | presisi 0,87 sampai 0,95 (1,1x) | Wilson presisi per sumur 0,82 sampai 0,99 | FAR 10,0 sampai 49,9 (5,0x) | nodata rule 356 dari 1.989 | SEDANG |
| vib rf | TREN | AUPRC 0,441 sampai 0,912 (2,07x) | CI memuat prevalensi 0 dari 4 | FAR 4,1 sampai 496 (119x), 1 dari 4 sumur | prevalensi 0,14 sampai 0,57 | SEDANG |
| ssi hybrid | PERINGATAN-BERPENGAWAS | tidak pernah lebih buruk dari rule di 7 dari 7 fold | n/a | FAR 0 sampai 3,7 | nodata CRPM 62,3 persen | SEDANG |
| ssi rf | TREN | AUPRC 0,015 sampai 0,459 (30,4x) | CI memuat prevalensi 3 dari 7 fold layak | recall 0 di semua fold pada tau 0,5 | sama dengan di atas | SEDANG |
| shk rule | PERINGATAN-BERPENGAWAS | FAR 0,67 sampai 6,6 (9,9x), lolos di 7 dari 9 sumur | presisi 0,00 sampai 0,94 | lolos mayoritas sumur tanpa kalibrasi | nodata 12,1 persen | SEDANG |
| shk rf | TREN | AUPRC 0,007 sampai 0,193 (28,1x) | CI memuat prevalensi 7 dari 9 | FAR 0 sampai 96,5, 1 dari 9 sumur | sama dengan di atas | SEDANG |
| stuck K-i | PERINGATAN-BERPENGAWAS | presisi 0,92 sampai 0,97 (1,05x) | Wilson lebar, n kecil | cakupan 2 sumur, belum terukur di luar itu | n/a | SEDANG |
| stuck K-ii | TREN | TLead 4,5 sampai 8,5 menit (1,89x) | CI memuat prevalensi 4 dari 4 | FAR 2,1 sampai 29,0 (13,9x) | anchor absorbed 4,6 persen | SEDANG |
| hyd K-i | PERINGATAN-BERPENGAWAS | presisi 0,72 sampai 0,95 di 9 dari 9 sumur | CI memuat prevalensi 0 dari 9 | FAR 14,6 sampai 58,4 (4,0x) | label = residu SPPA, proxy | SEDANG |
| tool_wear K-i | PERINGATAN-BERPENGAWAS | deteksi 4 dari 4 alat, TLead 20 sampai 36 detik | p signifikan 8 dari 8 run | FP 1 sampai 3 per alat setelah kalibrasi | tes artefak termal 0 dari 8 | SEDANG |

Sumber tiap sel: [EVC] baris 90 (vib), 91 (ssi), 92 (shk), 93 (stuck K-i), 94 (stuck K-ii), 95 (hyd
K-i), 98 (tool_wear K-i). Kolom bukti dari [JSON] `profil_kapabilitas` medan `kekuatan_bukti` per
mesin: vib, ssi, shk, stuck, hyd, tool_wear SEDANG, bit_wear LEMAH ([JSON] baris 1417 sampai 1664).

Catatan hitung klaim: [EVC] baris 66 menyatakan 7 mesin sama dengan 11 klaim, sedangkan tabel ringkas
[EVC] memuat 10 baris karena baris bit_wear menggabungkan K-1 dengan catatan K-2 belum dijalankan
([EVC] baris 97). Selisih satu itu adalah klaim bit_wear K-2, dan baris itu tidak saya tambahkan ke
tabel karena tidak punya angka sama sekali. Ini inferensi saya atas kedua bagian [EVC], bukan kutipan.

### 7.3 Kolom yang paling sering tidak disepakati antar mesin

Dari sepuluh baris di atas, kolom C3 (portabilitas ambang) adalah tempat mesin paling tidak sepakat
dengan dirinya sendiri di sumur berbeda, dan itu terbaca dari satu angka: rasio sebaran FAR.

| Klaim | Ambang | FAR terendah | FAR tertinggi | Rasio | Sumur yang lolos FAR 6 |
|---|---|---:|---:|---:|---|
| vib rf | tau 0,5 | 4,1 | 496 | 119x | 1 dari 4 |
| ssi rf | tau 0,3 | 0 | 15,6 | n/a (nol) | 2 dari 7 |
| shk rule | bawaan | 0,67 | 6,6 | 9,9x | 7 dari 9 |
| stuck K-i | bawaan | 8,3 | 61,0 | 7,3x | 0 dari 2 |
| hyd hybrid | bawaan | 14,6 | 58,4 | 4,0x | 0 dari 9 |
| tool_wear op_far | kuantil per alat | 1 FP | 3 FP | 3,0x | 4 dari 4 alat (target 1 alarm per menit, bukan FAR 6 per 24 jam) |

Sumber: [EVC] baris 120 (vib tau 0,5), 135 (ssi tau 0,3), 146 (shk), 158 (stuck K-i), 177 (hyd), 203
(tool_wear). Satuan: FP per 24 jam negatif untuk lima baris pertama, FP per menit negatif untuk
tool_wear.

Pelajaran yang harus muncul di layar, bukan hanya di laporan: "lolos FAR 6" bukan sifat mesin, tetapi
sifat pasangan mesin dengan sumur. shk rule lolos di 7 dari 9 sumur, hyd hybrid lolos di 0 dari 9,
dan keduanya bertier sama. Peta ketidaksepakatan yang tidak menampilkan penyebut sumur akan
menyamakan keduanya.

---

## 8. Contoh nyata tiap pola, dengan jendela yang dapat dibuka kembali

Medan `contoh_idx_aktif` di [JSON] berisi lima indeks aktif pertama, terurut menaik. Dari situ
hubungan antar head pada satu jendela tertentu dapat dibuktikan untuk kasus-kasus berikut, tanpa perlu
deret penuh. Kolom "dasar bukti" menyebut alasan yang membuat kesimpulan itu sah.

| Pola | Mesin | Jendela | Keadaan | Dasar bukti |
|---|---|---|---|---|
| A KEMBAR | vib | 429, 444, 472, 478, 489 | rule dan hibrida menyala bersama | dua daftar `contoh_idx_aktif` identik ([JSON] baris 79 dan 147) |
| A KEMBAR | shk | 20 | rule dan hibrida menyala bersama | idem, daftar mulai 20 ([JSON] baris 371 dan 439) |
| B CAKUPAN | vib | 382, 383, 384, 385, 386 | persistence menyala, rule dan rf padam | persistence mulai 382, rule mulai 429, rf mulai 517 |
| B CAKUPAN | tool_wear | 19, 20, 21, 22 | calib menyala, op_far dan canary padam | calib mulai 19, op_far mulai 42, canary mulai 23 |
| C MENIADAKAN | hyd | 0, 1, 2, 3, 4 | rule menyala, persistence dan hibrida padam | rule mulai 0, dua lainnya mulai 20 ([JSON] baris 743, 777, 814) |
| C MENIADAKAN | ssi | 118, 119, 120, 303, 304 | persistence menyala, rule dan rf padam | rule dan rf punya daftar kosong ([JSON] baris 234, 323) |
| C MENIADAKAN | stuck K-ii | 3.560 sampai 3.564 | hanya e1_2of3 menyala, dua head lain padam | e1 mulai 3.560, rf mulai 17.582, persistence_event mulai 30.122 |
| BISU | ssi | seluruh 5.455 | rule dan rf tidak pernah menyala | daftar kosong pada dua head ([JSON] baris 234 dan 323) |
| BISU | shk | seluruh 11.205 | rf tidak pernah menyala | daftar kosong ([JSON] baris 472) |
| SEPAKAT | shk | 20 | rule dan persistence menyala bersama | indeks 20 muncul di kedua daftar ([JSON] baris 371 dan 405) |

Batas kejujuran tabel ini: `contoh_idx_aktif` hanya lima indeks pertama per head, jadi tabel ini
membuktikan keadaan pada jendela yang disebut, bukan pola pada seluruh segmen. Pola pada seluruh segmen
dibuktikan oleh jumlah dan metrik di bagian 5 dan 6, bukan oleh tabel ini.

Dua jendela terakhir layak dibaca berdampingan: shk indeks 20 adalah satu-satunya contoh kesepakatan
dua head yang dapat dibuktikan langsung dari berkas, sementara hyd indeks 0 sampai 4 adalah contoh
ketidaksepakatan. Menampilkan keduanya di layar yang sama, dengan lencana berbeda, adalah uji baca
paling murah untuk fitur DSS3-02.

---

## 9. Spesifikasi fitur

Lima fitur. Setiap fitur memuat tiga belas butir wajib dari kartu, tidak diringkas. Kode fitur induk
di katalog disebut supaya tidak ada fitur baru yang lahir tanpa rujukan: DSS3-01 memperluas KEP-08
([KAT] baris 673), DSS3-02 memperluas KEP-08 butir salah tafsir ([KAT] baris 734), DSS3-03 memperluas
CMP-07 ([KAT] baris 1982), DSS3-04 memperluas LIN-01 dan MNT-07 ([KAT] baris 2071 dan 1186), DSS3-05
memperluas bagian penjelasan tiap mesin di KEP-08 ([KAT] baris 685).

### 9.1 DSS3-01 Matriks kesepakatan komponen

**ID dan nama fitur.** DSS3-01 Matriks kesepakatan komponen per mesin. Memperluas KEP-08 Panel
ketidaksepakatan antar head.

**Tujuan.** Menyelesaikan masalah satu label gabungan yang membuat pembaca mengira semua head sepakat
([KAT] baris 676 sampai 678). Untuk penilai model, pengawas, dan insinyur yang harus tahu apakah dua
head pada mesin yang sama sebenarnya satu fungsi, dua cakupan berbeda, atau dua jawaban yang saling
meniadakan.

**Menggambarkan apa.** Bentuk kesepakatan antar head, bukan tingkat bahaya. Naiknya Jaccard berarti dua
head makin sering menemukan kejadian yang sama, bukan makin berbahaya. Turunnya Jaccard pada pasangan
yang satu himpunan bagian yang lain berarti pemangkasan makin agresif, bukan deteksi makin buruk.
Angka 100,00 persen pada dua head yang identik adalah temuan pola A, bukan prestasi.

**Pengguna dan momen pakai.** Penilai model saat menyiapkan bab evaluasi dan saat memeriksa klaim
klaim "dua langkah konfirmasi", sekali per kampanye. Pengawas saat menanyakan mengapa dua peringatan
muncul bersamaan untuk satu kejadian, dua sampai empat kali per shift. Insinyur pengeboran saat
membuka satu peringatan dan melihat asal-usulnya, setiap kali peringatan dibuka.

**Masukan.** [JSON] `engines[].heads[]`: medan `n_windows`, `n_aktif`, `metrik_segmen.pos`,
`metrik_segmen.tp`, `metrik_segmen.fp`, `metrik_segmen.fn`, dan `definisi` per head. Satuan: hitungan
jendela (bilangan bulat), jendela 60 detik untuk enam mesin dan 1 detik untuk tool_wear. Rentang nilai:
n dari 0 sampai 95.925, n_aktif dari 0 sampai 4.917, tp dari 0 sampai 4.881. Cara memperoleh: dibaca
dari berkas, tidak dihitung ulang; verifikasi konvensi `n_aktif = tp + fp` wajib lulus pada semua head
bermetrik sebelum matriks disusun (bagian 2.3).

**Algoritma.** Langkah satu, untuk setiap mesin, ambil daftar head yang punya `metrik_segmen`. Langkah
dua, tentukan relasi tiap pasangan dalam satu mesin dengan tiga kemungkinan: identik (metrik sama
persis), himpunan bagian (deklarasi `definisi` atau ambang monoton), atau lepas. Langkah tiga, hitung
matriks kesepakatan status dengan rumus KS_status = (n11 + n00) / n dan matriks kelas positif dengan
KS_pos = (n11_pos + n00_pos) / pos dan Jaccard = n11_pos / (TP_A + TP_B − n11_pos). Langkah empat,
untuk pasangan lepas, hitung batas bawah dan batas atas irisan: bawah = max(0, TP_A + TP_B − pos),
atas = min(TP_A, TP_B), lalu laporkan sebagai rentang. Langkah lima, tandai setiap head dengan
n_aktif = 0 sebagai BISU dan head dengan n_windows = 0 sebagai BELUM DIJALANKAN. Parameter: tidak ada
ambang bebas; seluruhnya turunan hitungan mentah. Alasan memilih matriks dan bukan satu label: [VR]
bagian 5.4 mencatat bahwa matriks kesepakatan antar head adalah visual lazim untuk keluaran jenis ini,
dan [KAT] baris 701 sudah menetapkan larangan meringkasnya menjadi satu label.

**Workflow.** (1) Muat [JSON]. (2) Periksa konvensi `n_aktif = tp + fp`, hentikan penyusunan bila ada
satu ketidakcocokan. (3) Tentukan relasi tiap pasangan per mesin. (4) Hitung KS_status, KS_pos, dan
Jaccard, atau batas bawah dan atas bila pasangan lepas. (5) Tandai BISU dan BELUM DIJALANKAN.
(6) Susun matriks persegi per mesin, dengan sel berisi dua angka dan jumlah irisan. (7) Simpan versi
hitungan mentah dan versi ternormalisasi per baris. (8) Tampilkan di halaman kelas, dan tampilkan panel
per jendela saat satu peringatan dibuka.

**Keluaran.** Dua bentuk data. Pertama, matriks persegi per mesin berukuran jumlah head kali jumlah
head, berisi Jaccard positif dalam persen (0 sampai 100) dan jumlah irisan (bilangan bulat) atau
rentang dua angka untuk pasangan lepas. Kedua, tabel pasangan datar berisi n11, n10, n01, n00,
KS_status, KS_pos, dan Jaccard. Arti tiap nilai: 100,00 berarti fungsi sama atau definisi, di atas 75
berarti cakupan hampir sama, 25 sampai 75 berarti cakupan berbeda tetapi beririsan, di bawah 25 berarti
dua head hampir tidak berbagi kejadian, dan 0,00 dengan salah satu head bernilai nol berarti BISU.
Rentang berarti berkas tidak menyimpan cukup informasi untuk satu angka.

**Saran penyajian.** Heatmap matriks bernilai dengan angka di dalam sel, disertai satu versi
ternormalisasi per baris, ukuran 4 kali 4 selebar 360 piksel untuk mesin berempat head. Alasan: sel
diagonal dan luar diagonal punya arti berbeda, dan normalisasi per baris diperlukan supaya kelas jarang
tidak tertutup kelas mayoritas ([VR] bagian 5.9, LV9). Warna hanya pelengkap, angka tetap ditulis.
Tata letak contoh: judul mesin dan jumlah jendela di atas matriks; sel diagonal berlatar abu terang
dengan teks "100,00 (definisi)"; sel di bawah 25 persen diberi ikon peringatan kecil; di bawah matriks
satu baris keterangan "n = 10.401, positif = 865, head BISU: tidak ada". Untuk pasangan lepas, sel
menampilkan "31,94 sampai 52,42" dalam satu baris, bukan angka tunggal.

**Dasar riset penyajian.** [VR] bagian 5.4 menyatakan visual lazim untuk ketidaksepakatan model adalah
matriks kesepakatan antar head atau panel per kejadian, dengan kalimat inti dari LV15: metode penjelas
sering tidak sepakat dan praktisi bisa bergantung pada penjelasan yang menyesatkan. [VR] bagian 5.9 dan
[VR] baris 127 memberi bentuk matriks bernilai dengan normalisasi per baris dari LV9, sumber yang
menyatakan diagonal berarti benar dan luar diagonal berarti salah label serta menambahkan alasan
normalisasi pada kelas tidak seimbang. Larangan meringkas menjadi satu angka diambil dari LV5 lewat
[VR] bagian 6.

**Status bukti.** Sudah dihitung dari data nyata untuk seluruh matriks di bagian 6: 24 head bermetrik,
7 mesin, dan 0 ketidakcocokan konvensi (bagian 2.3). Rentang untuk pasangan lepas juga sudah dihitung.
Yang masih rancangan: tampilan visualnya sendiri belum dibuat, dan versi ternormalisasi per baris baru
dihitung sebagai angka, belum digambar.

**Salah tafsir yang harus dicegah.** Pertama, membaca KS_status 99,43 persen pada ssi sebagai
kesepakatan baik, padahal Jaccard positif 0,00 persen. Kedua, membaca Jaccard 100,00 persen sebagai
bukti mutu, padahal itu pola A, dua head satu fungsi. Ketiga, membaca Jaccard rendah sebagai
pertentangan, padahal pola B dengan pemangkasan sah menghasilkan angka rendah secara sengaja.
Keempat, membandingkan sel antar mesin, misalnya Jaccard shk 23,81 dengan hyd 80,12, karena jumlah
sumur, prevalensi, dan satuan FAR berbeda. Kelima, menganggap rentang sebagai ketidakpastian model,
padahal itu ketidaklengkapan berkas.

**Cara menguji.** Uji satu, hitung ulang satu sel dari TP mentah: hyd hibrida terhadap rule harus
516 / 607 = 85,01 persen. Uji dua, buat data sintetis dua head identik dan pastikan pola A muncul
dengan KS 100,00 persen dan n10 = n01 = 0. Uji tiga, buat data sintetis dua head yang saling meniadakan
total (tidak pernah menyala bersama) dan pastikan Jaccard keluar 0,00 persen sementara KS_status tetap
tinggi, sehingga penandaan BISU terpisah dari penandaan MENIADAKAN. Uji empat, minta satu pembaca
menjelaskan sel 23,81 persen pada shk tanpa melihat keterangan, lalu periksa apakah ia menyebut
penyebut positif.

### 9.2 DSS3-02 Lencana pola konflik dan alasan wajib

**ID dan nama fitur.** DSS3-02 Lencana pola konflik per jendela, dengan alasan yang wajib terisi.
Memperluas butir salah tafsir KEP-08 ([KAT] baris 734 sampai 738).

**Tujuan.** Menjawab pertanyaan yang muncul begitu operator melihat dua status berbeda pada satu
kejadian: "ini tanda bahaya atau ini tanda pemangkasan?". Tanpa lencana dan alasan, dua status berbeda
dibaca sebagai kerusakan sistem. Untuk operator dan pengawas, setiap kali satu peringatan dibuka.

**Menggambarkan apa.** Sebab dari perbedaan, bukan besarnya perbedaan. Empat lencana: KEMBAR (dua head
satu fungsi), CAKUPAN (satu head memangkas yang lain karena syarat AND atau ambang lebih ketat),
MENIADAKAN (dua head setara memberi jawaban berbeda), BISU (satu head tidak pernah menyala pada segmen
ini). Naiknya jumlah lencana MENIADAKAN berarti jendela itu makin ambigu, bukan makin berbahaya.
Lencana BISU berarti ketiadaan bukti, bukan ketenangan.

**Pengguna dan momen pakai.** Operator saat satu peringatan masuk, setiap kali, karena ia yang harus
memutuskan eskalasi. Pengawas saat menyiapkan serah terima shift, dua sampai empat kali per shift.
Penilai model saat mengaudit apakah alasan yang tercetak benar-benar sebabnya, sekali per kampanye.

**Masukan.** Untuk tiap jendela: status biner setiap head pada mesin itu, ambang yang dipakai head
tersebut, jumlah kanal masukan yang kosong, dan medan `definisi` head. Ditambah dua angka segmen dari
[JSON]: `n_aktif` per head (untuk menentukan BISU) dan `n_nodata` bila ada, misalnya rule vib 356 dari
1.989 ([JSON] baris 98). Satuan: status biner dan hitungan kanal. Rentang: jumlah head 2 sampai 6 per
mesin. Cara memperoleh: status per jendela belum tersimpan, sehingga butir masukan ini adalah syarat,
bukan ketersediaan; yang tersedia hari ini adalah agregat dan lima contoh indeks (bagian 8).

**Algoritma.** Langkah satu, untuk setiap jendela kumpulkan vektor status per head. Langkah dua,
bandingkan berpasangan dan tentukan lencana dengan aturan berurutan: bila dua head identik menurut
metrik segmen, beri KEMBAR; bila satu himpunan bagian yang lain, beri CAKUPAN pada pihak longgar dan
pemangkasan pada pihak ketat; bila tidak ada relasi himpunan tetapi keduanya menyala berbeda, beri
MENIADAKAN; bila salah satu head bernilai nol sepanjang segmen, beri BISU dan hentikan penilaian
pasangan itu. Langkah tiga, isi medan alasan dari tiga kategori yang sudah ditetapkan katalog: syarat
AND tidak terpenuhi, kanal masukan kosong, atau ambang jenuh ([KAT] baris 699). Langkah empat, bila
semua head padam dan kanal masukan kosong, beri lencana KETIADAAN DATA, bukan BISU. Parameter: tidak
ada ambang numerik; keputusan berbasis relasi himpunan dan nilai nol. Alasan memilih relasi himpunan
dan bukan selisih persentase: selisih persentase tidak dapat membedakan pemangkasan yang sah dari
pertentangan yang perlu dibaca manusia.

**Workflow.** (1) Simpan status per menit setiap head, bersama ambang dan jumlah kanal kosong.
(2) Tandai head BISU dan BELUM DIJALANKAN sekali per segmen, bukan per jendela. (3) Tentukan relasi
himpunan tiap pasangan dari `definisi`. (4) Untuk setiap jendela, susun vektor status dan tentukan
lencana. (5) Isi alasan dari tiga kategori, dengan kategori keempat untuk ketiadaan data.
(6) Tampilkan panel empat baris saat peringatan dibuka: nama head, status, ambang, alasan.
(7) Catat lencana ke log keputusan LIN-01 supaya bisa ditinjau ulang.

**Keluaran.** Satu vektor lencana per jendela (KEMBAR, CAKUPAN, MENIADAKAN, BISU, KETIADAAN DATA) plus
satu baris alasan teks pendek. Arti: KEMBAR berarti tidak ada informasi baru dari baris kedua; CAKUPAN
berarti perbedaan sah dan biayanya sudah terukur di bagian 5.2; MENIADAKAN berarti butuh penilaian
manusia; BISU berarti tidak ada bukti dari head itu; KETIADAAN DATA berarti sensor yang hilang.
Rentang nilai: satu lencana per pasangan per jendela, dan satu lencana global per head per segmen.

**Saran penyajian.** Panel empat baris teks, bukan empat ikon, dengan latar berbeda untuk baris yang
alasannya kanal kosong ([KAT] baris 719 sampai 722). Alasan: empat baris teks lebih cepat dibaca
daripada ikon, dan alasan harus terbaca sebagai kalimat. Tata letak contoh: satu kartu selebar 360
piksel; baris pertama nama head dan lencana; baris kedua status menyala atau padam dengan ambang;
baris ketiga alasan dalam satu kalimat; baris keempat tautan ke matriks DSS3-01. Lencana BISU diberi
latar abu dan teks "tidak pernah menyala pada segmen ini (0 dari 5.455)", bukan warna merah, karena
ini ketiadaan bukti bukan bahaya.

**Dasar riset penyajian.** [VR] bagian 5.4 menyatakan bentuk lazim untuk keluaran ini adalah panel per
kejadian yang menampilkan putusan tiap head berdampingan, atau matriks kesepakatan, dengan rujukan
LV15. [VR] baris 246 (tabel larangan) menolak satu angka keyakinan tanpa sebaran, yang menjadi dasar
larangan menampilkan satu lencana gabungan tanpa alasan. [VR] bagian 5.10 dan LV16 dipakai untuk
kewajiban menyertakan akibat, bukan hanya label.

**Status bukti.** Rancangan sebagian. Sudah terbukti dari data nyata: keempat lencana punya contoh
yang dapat dibuka pada jendela tertentu (bagian 8), dan seluruh angka pendukungnya terhitung (bagian
5.1 sampai 5.4). Belum: status per jendela belum tersimpan, sehingga lencana belum bisa dihitung untuk
seluruh 5.455 atau 95.925 jendela; yang ada baru agregat dan lima indeks contoh per head.

**Salah tafsir yang harus dicegah.** Pertama, membaca CAKUPAN sebagai kerusakan, padahal itu pemangkasan
yang sudah diukur biayanya. Kedua, membaca BISU sebagai aman. Ketiga, membaca KETIADAAN DATA sebagai
dua head sepakat padam. Keempat, membaca KEMBAR sebagai dua langkah konfirmasi, padahal dua-duanya satu
komputasi. Kelima, memakai lencana MENIADAKAN sebagai dasar eskalasi otomatis, padahal prototipe punya
0 slot alarm otomatis ([JSON] baris 1414).

**Cara menguji.** Uji satu, buka hyd indeks 0 sampai 4 dan pastikan lencana yang muncul MENIADAKAN
dengan alasan "syarat AND tidak terpenuhi", bukan CAKUPAN. Uji dua, buka vib indeks 382 sampai 386 dan
pastikan lencana CAKUPAN dengan pihak padam rule dan rf. Uji tiga, buka shk indeks 20 dan pastikan tidak
ada lencana konflik karena kedua head yang diperiksa menyala. Uji empat, minta operator menjelaskan arti
lencana BISU pada kartu ssi, lalu periksa apakah ia menyebut 62,3 persen nodata CRPM.

### 9.3 DSS3-03 Peta ketidaksepakatan antar mesin tingkat klaim

**ID dan nama fitur.** DSS3-03 Peta ketidaksepakatan antar mesin tingkat klaim. Memperluas CMP-07 Panel
kesetaraan head hyd ([KAT] baris 1982) dari satu mesin ke tujuh mesin.

**Tujuan.** Menyelesaikan masalah klaim "naik" yang ditulis ketika satu komposisi menang di satu metrik
([KAT] baris 1985 sampai 1986). Untuk PM, peneliti, dan dosen penguji yang memeriksa apakah dua mesin
yang bertier sama sebenarnya sepakat tentang kelayakan pakainya.

**Menggambarkan apa.** Kesepakatan antar mesin pada tingkat klaim, bukan pada tingkat jendela. Naiknya
jumlah klaim yang lolos pada ambang yang sama berarti mesin-mesin itu sepakat tentang kelayakan ambang
di sumur uji. Turunnya kolom portabilitas berarti mesin itu tidak sepakat dengan dirinya sendiri di
sumur berbeda. Tier yang sama pada dua mesin dengan portabilitas berbeda adalah ketidaksepakatan yang
harus terlihat, bukan diratakan.

**Pengguna dan momen pakai.** PM saat menulis klaim perbaikan di laporan, sekali per laporan. Peneliti
saat memilih mesin untuk kampanye berikutnya, sekali per kampanye. Dosen penguji saat sidang, sekali per
sidang. Pengawas lapangan saat menanyakan "mesin mana yang boleh saya percaya untuk kelas ini", beberapa
kali per bulan.

**Masukan.** [EVC] tabel ringkas baris 88 sampai 99: tier per klaim, C1 sampai C5, dan kesimpulan
kemampuan per baris. Ditambah [EVC] bagian 2 untuk angka sebaran antar sumur. Ditambah [JSON]
`profil_kapabilitas` medan `kekuatan_bukti` dan `layak_untuk` ([JSON] baris 1417 sampai 1664). Satuan:
FAR dalam FP per 24 jam negatif atau FP per menit negatif sesuai mesin; AUPRC tanpa satuan; rasio
sebaran tanpa satuan. Rentang: FAR dari 0 sampai 496, AUPRC dari 0,007 sampai 0,984. Cara memperoleh:
dibaca dari dua berkas, tidak dihitung ulang di fitur ini.

**Algoritma.** Langkah satu, susun daftar klaim: satu baris per mesin per klaim, 10 baris untuk angka
yang ada dan 1 baris tambahan untuk bit_wear K-2 yang belum dijalankan. Langkah dua, isi enam kolom
sisi bukti dari [EVC]. Langkah tiga, tandai sel yang menyebut "belum terukur" secara eksplisit, jangan
diisi nol. Langkah empat, hitung satu kolom turunan: jarak tier terhadap portabilitas, yaitu selisih
antara tier yang diberikan dan jumlah sumur yang lolos FAR 6, karena itulah pasangan yang paling sering
tidak sepakat (bagian 7.3). Langkah lima, urutkan baris menurut tier lalu menurut rasio sebaran
menurun. Parameter: ambang kelayakan FAR 6 mengikuti [EVC] baris 69 (EC-4), bukan pilihan fitur.
Alasan memilih matriks klaim dan bukan rata-rata skor: [VR] bagian 5.4 dan LV15 menunjukkan bahwa
meringkas ketidaksepakatan menjadi satu skor gabungan justru menghilangkan informasinya.

**Workflow.** (1) Baca [EVC] tabel ringkas dan bagian 2. (2) Baca `profil_kapabilitas` di [JSON].
(3) Susun matriks 10 atau 11 baris, 6 kolom. (4) Tandai sel belum terukur dengan lencana khusus.
(5) Hitung kolom turunan jarak tier terhadap portabilitas. (6) Urutkan. (7) Tampilkan sebagai satu
halaman yang bisa disaring per mesin. (8) Tautkan setiap sel ke baris sumbernya di [EVC].

**Keluaran.** Matriks 10 atau 11 baris dan 6 kolom, satu sel per klaim per sisi bukti, plus satu kolom
turunan. Arti: sel berisi angka berarti terukur dengan penyebut yang tercantum; sel berlencana berarti
belum terukur; kolom turunan bernilai besar berarti tier diberikan lebih tinggi daripada dukungan
portabilitasnya. Rentang: rasio sebaran dari 1,05x (stuck K-i presisi) sampai 119x (vib FAR).

**Saran penyajian.** Matriks bernilai dengan penyebut di setiap sel, dan satu grafik sebar per klaim
untuk kolom portabilitas. Alasan: jumlah klaim kecil sehingga matriks selesai dalam satu layar, dan
sebar mencegah kesimpulan dari satu angka agregat ([VR] bagian 5.4 dan [KAT] baris 2038 sampai 2041,
LV9 dan LV6). Tata letak contoh: matriks 11 baris kali 6 kolom, kolom tier diberi warna paling lembut,
kolom portabilitas memuat "119x (1/4)" dalam satu sel, kolom bukti memuat satu kata. Di bawah matriks,
grafik batang horizontal satu baris per klaim dengan sumbu log untuk rasio sebaran, karena rentangnya
1,05x sampai 119x tidak terbaca pada sumbu linear.

**Dasar riset penyajian.** [KAT] baris 2037 sampai 2045 menetapkan matriks pasangan dengan sel berisi
selisih dan lencana status, dengan rujukan LV9 untuk matriks bernilai dan LV6 untuk sebar pada dua
variabel kontinu. [VR] bagian 6 baris 245 melarang sumbu terpotong pada grafik batang, karena itu
pemakaian sumbu log dinyatakan terbuka di sini sebagai pilihan yang harus diberi label, bukan
disembunyikan. [EVC] baris 101 sampai 107 menjadi isi ringkasan temuan.

**Status bukti.** Sudah dihitung dari data nyata untuk seluruh sel yang terisi: 10 baris klaim, angka
dari [EVC], dan seluruh penyebut sumur tercantum. Yang masih rancangan: kolom turunan jarak tier
terhadap portabilitas belum pernah dipakai di dokumen lain, jadi definisinya baru di dokumen ini dan
belum diuji pembaca.

**Salah tafsir yang harus dicegah.** Pertama, membaca "lolos FAR 6 di 7 dari 9" sebagai sifat mesin,
padahal itu sifat pasangan mesin dengan sumur. Kedua, membaca tier sama sebagai mutu sama, padahal hyd
K-i dan shk rule bertier sama dengan portabilitas 0 dari 9 lawan 7 dari 9. Ketiga, membaca sel belum
terukur sebagai nol. Keempat, membandingkan rasio 119x milik vib dengan 4,0x milik hyd tanpa menyebut
bahwa keduanya memakai ambang berbeda dan jumlah sumur berbeda.

**Cara menguji.** Uji satu, ambil satu sel, misalnya hyd K-i FAR 14,6 sampai 58,4, dan periksa ke [EVC]
baris 177. Uji dua, hitung ulang rasio 119x dari 496 dibagi 4,1 dan pastikan hasilnya 120,98, lalu
periksa apakah sumber menulis 119x karena pembulatan nilai mentah, dan laporkan selisih itu apa adanya.
Uji tiga, minta satu pembaca menyebut dua mesin bertier sama dengan portabilitas berlawanan.

### 9.4 DSS3-04 Jalur status per head pada garis waktu

**ID dan nama fitur.** DSS3-04 Jalur status per head pada garis waktu satu shift. Memperluas LIN-01
untuk waktu keputusan ([KAT] baris 2071) dan MNT-07 untuk sumbu waktu ([KAT] baris 1186).

**Tujuan.** Menjawab "kapan perbedaan itu terjadi dan berapa lama", karena matriks menjawab "seberapa
sering" tetapi tidak menjawab urutan. Untuk pengawas yang meninjau ulang satu shift, dan untuk penilai
model yang memeriksa apakah ketidaksepakatan menggerombol pada jam tertentu.

**Menggambarkan apa.** Urutan dan lamanya status tiap head pada satu sumbu waktu. Naiknya panjang satu
jalur berarti head itu menyala lebih lama, bukan lebih benar. Jalur yang saling menimpa berarti dua head
sepakat pada rentang itu. Jalur yang selalu kosong berarti pola BISU. Celah pada semua jalur bisa
berarti sensor hilang, dan itu harus dibedakan dari semua head padam.

**Pengguna dan momen pakai.** Pengawas saat serah terima shift, dua kali per shift. Operator saat
meninjau ulang satu peringatan yang sudah lewat, beberapa kali per shift. Penilai model saat memeriksa
penggerombolan ketidaksepakatan, sekali per kampanye.

**Masukan.** Deret status biner per menit per head, bersama `ts_bin` dari grid D1. Ditambah penanda
kanal kosong per menit. Satuan: indeks menit internal, bukan tanggal (bagian 2.4). Rentang: 3.018 menit
untuk segmen vib, 359.604 menit untuk segmen stuck K-ii ([JSON] `segmen_info`). Cara memperoleh: dibaca
dari deret per menit yang belum tersimpan; hari ini yang tersedia hanya agregat dan lima indeks contoh
per head.

**Algoritma.** Langkah satu, kumpulkan deret status per head pada `ts_bin`. Langkah dua, gabungkan
menjadi satu tabel dengan satu baris per menit dan satu kolom per head. Langkah tiga, tandai menit
dengan kanal kosong memakai kolom terpisah, bukan dengan nilai nol pada kolom head. Langkah empat,
hitung panjang tiap ruas menyala (run length) per head. Langkah lima, tandai ruas yang tumpang tindih
antara dua head sebagai sepakat dan yang tidak tumpang tindih sebagai berbeda. Langkah enam, jika
deret lebih panjang dari satu layar, agregasi ke bin 5 menit dengan aturan mayoritas dan tulis lebar
bin di sumbu. Parameter: lebar bin 5 menit untuk tampilan shift 8 jam, dengan pilihan 1 menit untuk
pemeriksaan rinci. Alasan memilih nilai biner per menit dan bukan skor kontinu: seluruh head peringatan
di prototipe mengeluarkan status biner, sedangkan head skor ada di lapis L2 dan tidak boleh dicampur
pada satu sumbu ([JSON] `decision_layer.layers`).

**Workflow.** (1) Simpan status per menit bersama `ts_bin`. (2) Gabungkan ke satu tabel lebar.
(3) Tandai kanal kosong pada kolom sendiri. (4) Hitung panjang ruas. (5) Tandai tumpang tindih.
(6) Agregasi ke bin 5 menit untuk tampilan shift. (7) Tampilkan satu baris per head dengan warna status
dan satu baris kanal kosong di bawahnya. (8) Tautkan setiap ruas ke panel DSS3-02.

**Keluaran.** Matriks biner berukuran jumlah menit kali jumlah head, ditambah deret panjang ruas per
head dan deret kanal kosong. Arti: ruas panjang berarti status bertahan; ruas pendek berulang berarti
status berkedip; baris kosong berarti BISU; kolom kanal kosong yang tebal berarti ketiadaan data.
Rentang: panjang ruas 1 menit sampai ratusan menit; jumlah ruas per head tidak dibatasi.

**Saran penyajian.** Jalur status horizontal berlapis (satu baris per head) pada satu sumbu waktu
bersama, warna dua tingkat untuk menyala dan padam, ditambah satu lajur tipis kanal kosong di bawah.
Alasan: langkah pertama analisis deret waktu adalah memplot data pada sumbu waktu, karena pola dan
kejadian luar biasa terlihat di grafik (LV3 lewat [VR] bagian 5.7), dan menumpuk beberapa deret pada
satu sumbu x adalah bentuk yang sah selama satuannya sama ([VR] bagian 7 butir 6, LV8). Tata letak
contoh: lebar 900 piksel untuk 8 jam dengan bin 5 menit (96 kolom), tinggi 18 piksel per baris, empat
baris head, satu lajur kanal kosong setinggi 8 piksel; label sumbu x berupa indeks menit, bukan jam
kalender; legenda tiga warna: menyala, padam, kanal kosong.

**Dasar riset penyajian.** [VR] bagian 5.7 dan LV3 untuk kewajiban memplot deret pada sumbu waktu.
[VR] bagian 7 butir 6 dan LV8 untuk aturan satu satuan per grafik, yang menjadi alasan kolom skor L2
tidak dicampur ke jalur biner L1. [VR] bagian 5.10 dan LV16 untuk pola menautkan tiap butir waktu ke
kejadian dan akibatnya. Pemetaan jalur status berlapis ke kategori "perubahan sepanjang waktu" pada
LV6 adalah tafsiran saya, bukan kutipan langsung, dan karena itu disebut terbuka di sini.

**Status bukti.** Rancangan. Angka pendukung yang sudah nyata: jumlah jendela, rentang indeks menit,
dan lima indeks contoh per head (bagian 8). Belum: deret per menit belum tersimpan, sehingga jalur
belum dapat digambar untuk satu shift penuh; yang bisa digambar hari ini hanyalah lima titik contoh
per head, dan itu tidak cukup untuk menyebut fitur ini siap.

**Salah tafsir yang harus dicegah.** Pertama, membaca sumbu x sebagai tanggal, padahal itu indeks menit
internal tanpa asal kalender terverifikasi. Kedua, membaca jalur kosong sebagai kondisi aman. Ketiga,
membaca jalur panjang sebagai kondisi lebih buruk. Keempat, membaca dua jalur yang tumpang tindih
sebagai dua bukti independen, padahal bisa jadi pola A. Kelima, membandingkan panjang jalur antar mesin
dengan satuan jendela berbeda (60 detik lawan 1 detik).

**Cara menguji.** Uji satu, gambar jalur untuk hyd pada 100 indeks pertama dan pastikan indeks 0 sampai
4 menunjukkan rule menyala sedangkan dua head lain padam, sesuai bagian 8. Uji dua, buat deret sintetis
dengan kanal kosong pada 20 menit dan pastikan lajur kanal kosong terisi sementara jalur head tetap
terbaca padam, bukan kosong. Uji tiga, minta satu pembaca menyebut satuan sumbu x tanpa membuka
keterangan.

### 9.5 DSS3-05 Kartu penjelasan mesin

**ID dan nama fitur.** DSS3-05 Kartu penjelasan per mesin dan per head. Memperluas bagian pengguna dan
momen pakai KEP-08 ([KAT] baris 685 sampai 688).

**Tujuan.** Menyediakan satu tempat yang menjawab "mesin ini mengukur apa, dengan ambang apa, dan
sampai mana boleh dipercaya", supaya angka di matriks dan lencana tidak dibaca tanpa konteks. Untuk
operator baru, pengawas yang berganti mesin, dan penilai model yang menyusun batasan pemakaian.

**Menggambarkan apa.** Batas pemakaian, bukan ringkasan performa. Naiknya angka presisi pada kartu ini
tidak berarti mesin lebih layak untuk alarm, karena tier dan batas pemakaian ditulis di baris lain pada
kartu yang sama. Contoh paling jelas: bit_wear punya presisi 0,9927 tetapi tier TREN dan kekuatan bukti
LEMAH, karena labelnya indeks mekanika, bukan observasi keausan ([JSON] baris 868 dan [KAT] baris 750).

**Pengguna dan momen pakai.** Operator baru saat pertama kali memakai panel, sekali di awal. Pengawas
saat berganti mesin atau kelas, beberapa kali per bulan. Penilai model saat menyusun batasan pemakaian
per klaim, sekali per kampanye. Dosen penguji saat memeriksa apakah batas pemakaian disebut, sekali per
sidang.

**Masukan.** [JSON] per head: `definisi`, `tier`, `layer`, `badge_far`, `keyakinan`,
`batas_pemakaian`, `human_review_required`. Ditambah `profil_kapabilitas` per mesin: `jenis_tugas`,
`klaim_tugas`, `layak_untuk`, `belum_untuk`, `kekuatan_bukti`. Satuan: teks dan satu angka FAR per
head. Rentang: 27 head, 7 mesin. Cara memperoleh: dibaca langsung dari berkas, tanpa hitung ulang.

**Algoritma.** Tidak ada model. Aturan tampil: satu kartu per head, empat baris wajib, dan penolakan
tampil bila salah satu baris kosong. Langkah satu, ambil tujuh medan per head. Langkah dua, susun baris
pertama definisi dan ambang. Langkah ketiga, susun baris kedua tier dan lapis. Langkah keempat, susun
baris ketiga batas pemakaian, termasuk larangan yang tertulis di `batas_pemakaian`. Langkah kelima,
susun baris keempat alasan keyakinan, apa adanya termasuk kalimat yang menyatakan angka masih referensi
V8. Langkah keenam, bila `n_windows` bernilai 0, ganti seluruh kartu dengan satu baris BELUM DIJALANKAN
dan statusnya. Parameter: tidak ada. Alasan memilih kartu dan bukan tabel panjang: 27 head kali tujuh
medan menjadi 189 sel, dan tabel sebesar itu tidak terbaca pada satu layar.

**Workflow.** (1) Muat [JSON]. (2) Untuk tiap head, ambil tujuh medan. (3) Periksa kelengkapan, tandai
medan kosong sebagai temuan, jangan diisi karangan. (4) Susun empat baris. (5) Tautkan kartu ke matriks
DSS3-01 dan ke lencana DSS3-02. (6) Tampilkan kartu saat nama head diklik dari panel mana pun.
(7) Simpan versi cetak satu halaman per mesin untuk serah terima shift.

**Keluaran.** Kartu teks empat baris per head, ditambah satu baris lencana keadaan (AKTIF, BISU, BELUM
DIJALANKAN). Arti: baris ketiga adalah batas yang mengikat, dan baris keempat adalah alasan mengapa
batas itu ada. Rentang: panjang kartu 4 sampai 6 baris, karena medan `batas_pemakaian` pada beberapa
head memuat dua kalimat.

**Saran penyajian.** Kartu teks bertumpuk, satu kartu per head, dengan baris batas pemakaian diberi
latar berbeda dan tidak dapat dilipat. Alasan: peringatan yang bisa dilewati tidak dibaca, dan pembaca
memindai bagian atas lebih dulu ([VR] bagian 5.9 dan [KAT] baris 775 sampai 777, LV7). Tata letak
contoh: kartu selebar 340 piksel, judul nama head dan lencana keadaan, empat baris teks berukuran 12
piksel, baris batas pemakaian berlatar kuning muda dengan teks tebal. Untuk head BISU, baris pertama
berisi "0 dari 5.455 jendela menyala" dan baris ketiga berisi sebab terukur bila ada, misalnya nodata
CRPM 62,3 persen.

**Dasar riset penyajian.** [VR] bagian 5.9 dan LV7 untuk posisi dan keterbacaan elemen yang tidak boleh
dilewati. [KAT] baris 780 sampai 782 memakai LV11 untuk pola menulis akibat dan batas secara eksplisit,
bukan hanya label. [VR] bagian 6 baris 246 melarang satu angka tanpa sebaran, karena itu baris keempat
wajib memuat alasan keyakinan, bukan hanya angka presisi.

**Status bukti.** Siap sekarang untuk 24 head yang punya medan lengkap, karena seluruh isinya dibaca
langsung dari [JSON] tanpa hitung ulang. Untuk tiga head tanpa metrik (hyd K-ii, bit_wear K-2,
tool_wear canary) kartu tetap dapat disusun, tetapi baris pertama harus berbunyi BELUM DIJALANKAN atau
TANPA METRIK, dan itu sudah ditentukan di atas.

**Salah tafsir yang harus dicegah.** Pertama, membaca presisi tinggi sebagai izin alarm, contohnya
bit_wear 0,9927 dengan tier TREN. Kedua, membaca `keyakinan` sebagai skor, padahal medan itu berisi
kalimat dan sebagian menyebut angka referensi V8, bukan hasil V9. Ketiga, membaca tier sebagai mutu,
padahal tier adalah batas pemakaian yang mengutamakan keamanan ([EVC] baris 71). Keempat, melewati
baris batas pemakaian karena dianggap catatan kaki.

**Cara menguji.** Uji satu, buka kartu hyd hibrida dan periksa apakah baris ketiga memuat larangan
membaca presisi run sebagai keausan spesifik, sesuai [JSON] medan `batas_pemakaian`. Uji dua, buka
kartu ssi rule dan periksa apakah lencana BISU muncul bersama angka 0 dari 5.455. Uji tiga, minta satu
pembaca menyebut satu larangan dari kartu tanpa membuka berkas lain.
---

## 10. Saran penyajian dan dasar risetnya

### 10.1 Ringkasan pilihan visual per fitur

| Fitur | Visual yang disarankan | Alasan memilih | Sumber riset |
|---|---|---|---|
| DSS3-01 | Heatmap matriks bernilai, dua versi (mentah dan ternormalisasi per baris), angka di dalam sel | diagonal dan luar diagonal punya arti berbeda; normalisasi per baris perlu supaya kelas jarang tidak tertutup kelas mayoritas | [VR] bagian 5.9, LV9 |
| DSS3-02 | Panel empat baris teks, bukan ikon, satu kartu per jendela | empat baris teks lebih cepat dibaca daripada empat ikon, dan alasan harus terbaca sebagai kalimat | [KAT] baris 719 sampai 722, [VR] bagian 5.4, LV15 |
| DSS3-03 | Matriks 11 baris kali 6 kolom dengan penyebut di setiap sel, plus batang horizontal bersumbu log | jumlah klaim kecil sehingga matriks selesai satu layar; sebar mencegah kesimpulan dari satu angka agregat | [VR] bagian 5.4 dan 5.8, LV9, LV6, LV12 |
| DSS3-04 | Jalur status berlapis pada satu sumbu waktu, satu baris per head, lajur kanal kosong terpisah | langkah pertama analisis deret waktu adalah memplot data pada sumbu waktu; satu grafik satu satuan | [VR] bagian 5.7 dan 7 butir 6, LV3, LV8 |
| DSS3-05 | Kartu teks bertumpuk, baris batas pemakaian berlatar dan tidak dapat dilipat | peringatan yang bisa dilewati tidak dibaca; pembaca memindai bagian atas lebih dulu | [VR] bagian 5.9 dan 6, LV7, LV11 |

### 10.2 Alasan memilih matriks dan bukan satu label

[VR] bagian 5.4 memuat dua kalimat inti LV15: "state-of-the-art explanation methods often disagree in
terms of the explanations they output" dan "practitioners may be relying on misleading explanations
when making consequential decisions". Kalimat pertama menjelaskan mengapa ketidaksepakatan tidak boleh
disembunyikan, kalimat kedua menjelaskan akibatnya bila disembunyikan. Pada sistem ini, akibatnya
konkret dan terukur: empat pasang head identik di lapisan L1 membuat panel dengan dua baris terbaca
sebagai dua konfirmasi, padahal satu komputasi (bagian 5.1).

### 10.3 Visual yang harus dihindari, khusus untuk keluaran ketidaksepakatan

| Visual | Alasan ditolak | Sumber |
|---|---|---|
| Satu lencana gabungan per mesin | meringkas ketidaksepakatan menjadi satu label, persis yang diperingatkan sumber | [VR] bagian 5.4, LV15 |
| Persentase kesepakatan status saja tanpa kelas positif | dua head yang sama-sama diam terlihat sepakat, seperti pada ssi 99,43 persen dengan irisan TP nol | LV9 lewat [VR] baris 249 dan 230 |
| Matriks berisi hitungan mentah tanpa normalisasi | kelas mayoritas mendominasi sel sehingga kelas kecil terlihat benar | [VR] baris 249, LV9 |
| Gauge atau cakram untuk tingkat kesepakatan | luas dan sudut bukan kanal yang diproses cepat untuk informasi kuantitatif | [VR] baris 248, LV7 |
| Dua sumbu Y untuk membandingkan dua mesin | skala kedua sumbu sewenang-wenang, membuat pembaca salah menyimpulkan | [VR] baris 244, LV8 |
| Angka ketidaksepakatan tunggal per shift | prediksi titik dibaca sebagai kepastian; sebaran jendela lebih informatif | [VR] baris 246, LV5 |
| Grafik radar antar mesin | dilarang oleh katalog, bukan oleh sumber web, dan bentuknya menyulitkan pembacaan selisih antar pasangan | [VR] baris 256, [KAT] baris 1825 |

---

## 11. Salah tafsir yang harus dicegah

Sepuluh salah tafsir yang paling mungkin terjadi pada keluaran ketidaksepakatan, dengan angka penangkal
dari berkas.

| # | Salah tafsir | Kenapa salah | Angka penangkal |
|---:|---|---|---|
| 1 | "Kesepakatan 99,43 persen berarti dua head sepakat" | kesepakatan itu dari jendela padam | ssi rule dengan persistence: irisan TP 0 dari 75 positif ([JSON] baris 232 dan 260) |
| 2 | "Presisi 0,9927 berarti mesin ini layak alarm" | label bit_wear adalah indeks mekanika, tier-nya TREN | [JSON] baris 868, [KAT] baris 750, [EVC] baris 97 |
| 3 | "Dua baris peringatan berarti dua konfirmasi" | empat pasangan adalah fungsi yang sama | bagian 5.1, KS 100,00 persen pada empat mesin |
| 4 | "Pemangkasan itu perbaikan mutu" | biaya recall selalu ada dan terukur | hyd recall turun 0,1052; tool_wear turun 0,6666 (bagian 5.2) |
| 5 | "Lencana BISU berarti kondisi aman" | nol alarm adalah ketiadaan bukti | ssi 0 dari 5.455, shk rf 0 dari 11.205 ([JSON] baris 232, 470) |
| 6 | "Tier sama berarti mutu sama" | tier adalah batas pemakaian, bukan skor | hyd K-i lolos FAR 6 di 0 dari 9 sumur, shk rule 7 dari 9 ([EVC] baris 95 dan 92) |
| 7 | "Rentang Jaccard 31,94 sampai 52,42 adalah ketidakpastian model" | itu ketidaklengkapan berkas, bukan variansi | bagian 4.3, lima indeks aktif bukan deret penuh |
| 8 | "Sumbu x jalur status adalah tanggal" | indeks menit internal tanpa asal kalender | [JSON] `segmen_info.catatan_waktu` |
| 9 | "FAR mesin A bisa dibanding langsung dengan mesin B" | satuan dan penyebut sumur berbeda | 60 detik lawan 1 detik, FP/24jam lawan FP/menit (bagian 3) |
| 10 | "Jendela indeks 3.560 di stuck K-i sama dengan 3.560 di stuck K-ii" | dua klaim memakai grid berbeda | K-i 3.201 jendela, K-ii 95.925 jendela ([JSON] baris 509 dan 610) |

---

## 12. Cara menguji seluruh keluaran

Sepuluh uji, semuanya dapat dijalankan dari berkas yang sudah ada atau dari data sintetis kecil.
Kolom "hasil yang diharapkan" memuat angka yang sudah terverifikasi di dokumen ini, sehingga uji
berfungsi sebagai pemeriksa dokumen, bukan hanya pemeriksa perangkat lunak.

| # | Uji | Langkah | Hasil yang diharapkan | Dasar angka |
|---:|---|---|---|---|
| 1 | Konvensi hitung | hitung `n_aktif - (tp + fp)` untuk seluruh head bermetrik | 0 ketidakcocokan pada 24 head | bagian 2.3 |
| 2 | Sel matriks hyd | hitung 516 / 607 | 0,8501 atau 85,01 persen | bagian 6.3 |
| 3 | Sel matriks shk | hitung 55 / (55 + 48 + 231 - 55) | 0,2381 atau 23,81 persen | bagian 6.4 |
| 4 | Batas irisan | hitung bawah dan atas irisan TP `rf_lowo` dengan `persistence` pada vib | 801 dan 952 | bagian 4.3 |
| 5 | Pola A sintetis | dua head identik pada 100 jendela | n10 = 0, n01 = 0, KS 100,00 persen | [KAT] baris 740 sampai 742 |
| 6 | Pola C sintetis | dua head yang tidak pernah menyala bersama | Jaccard 0,00 persen, KS_status tetap tinggi | bagian 4.4 |
| 7 | Lencana BISU | buka head dengan `n_aktif` 0 | lencana BISU, bukan KEMBAR, bukan aman | bagian 5.4 |
| 8 | Lencana BELUM DIJALANKAN | buka head dengan `n_windows` 0 | lencana BELUM DIJALANKAN, bukan BISU | [JSON] baris 836 dan 898 |
| 9 | Urutan waktu | buka hyd indeks 0 sampai 4 | rule menyala, dua head lain padam | bagian 8 |
| 10 | Uji baca | minta satu pembaca menjelaskan sel 23,81 persen shk dan lencana BISU ssi tanpa keterangan | pembaca menyebut penyebut positif dan menyebut 62,3 persen nodata | bagian 5.4 dan 6.4 |

Uji nomor 5 sampai 10 adalah uji tampilan dan uji baca, sehingga hasilnya berupa kalimat pembaca, bukan
angka. Itu bukan kelemahan uji, melainkan bentuk uji yang tepat untuk keluaran yang tugasnya dibaca
manusia.

---

## 13. Syarat yang dibutuhkan

Daftar ini menyebut apa yang harus tersedia agar bagian yang belum terhitung bisa dihitung. Tidak ada
butir yang berupa penyerahan.

| # | Yang belum tersedia | Syarat agar bisa dikerjakan | Pemilik keputusan |
|---:|---|---|---|
| 1 | Deret putusan per menit per head | simpan status biner per `ts_bin` dari tiap head ke satu tabel panjang (kolom: `ts_bin`, mesin, head, status, ambang, jumlah kanal kosong). Tanpa ini, matriks antar mesin pada tingkat jendela dan seluruh lencana per jendela tetap berupa rancangan. | tim data |
| 2 | Definisi resmi "matriks konflik" | satu paragraf keputusan: pasangan mana yang dibandingkan (head lawan head, mesin lawan mesin, mesin lawan kejadian nyata) dan satuannya. Dokumen ini memakai definisi head lawan head pada jendela yang sama, dan menyatakannya sebagai pilihan, bukan keputusan resmi. | pemilik produk |
| 3 | Label positif yang sama lintas head dalam satu mesin | pastikan `metrik_segmen.pos` dihitung dari label yang identik untuk semua head pada mesin itu, atau simpan label per head. Bila tidak, KS_pos tidak sah dibandingkan antar head. | tim evaluasi |
| 4 | Penomoran waktu yang dapat dirujuk | asal kalender untuk `ts_bin` D1, supaya sumbu waktu di DSS3-04 bisa diberi tanggal dan bisa dicocokkan dengan log keputusan. | tim data |
| 5 | Ambang cetak per head untuk head L0 dan L1 | tulis nilai ambang yang dipakai saat metrik segmen dihitung (bukan hanya nama metode), karena lencana CAKUPAN butuh bukti ambang lebih ketat. | tim evaluasi |
| 6 | Kolom biaya per kejadian | isi slot biaya di KEP-10 ([KAT] baris 796) supaya ketidaksepakatan bisa diterjemahkan ke biaya tinjauan, bukan hanya jumlah jendela. | pemilik data biaya |
| 7 | Data sumur di luar cakupan uji untuk stuck K-i | jalankan ulang pada F-9, F-10, dan F-15 supaya sel matriks stuck bisa menyebut penyebut lebih dari 2 sumur. | tim eksperimen |

---

## 14. Yang belum diverifikasi di dokumen ini

Disebut eksplisit supaya tidak ada yang membacanya sebagai sudah terbukti:

1. Asal kalender `ts_bin` tidak diverifikasi. Berkas menyatakan sendiri bahwa asal kalender belum
   diverifikasi, dan dokumen ini mengikuti pernyataan itu ([JSON] `segmen_info`).
2. Bahwa `contoh_idx_aktif` berisi lima indeks aktif pertama yang terurut menaik adalah inferensi saya
   dari pola data pada 27 head. Bila medan itu ternyata berisi lima indeks acak, maka tabel di bagian 8
   kehilangan dasarnya. Cara memastikannya: periksa kode yang menulis medan itu, yang tidak ada di
   dalam berkas hasil.
3. Relasi "himpunan bagian" untuk `rule_display` terhadap `persistence` diambil dari deklarasi di
   [JSON] medan `definisi` dan `badge_far`, bukan dari perbandingan deret penuh. Bila deklarasi itu
   tidak akurat untuk segmen ini, angka n10 = 0 pada bagian 5.2 ikut gugur.
4. Relasi `op_far_calibrated` himpunan bagian `calib_5of27` diturunkan dari perbandingan ambang
   `thr_featcount` 8,63 sampai 12,32 lawan 5 dari 27 ([JSON] baris 1049 dan 920). Penurunan ini
   mengandaikan skor fitur yang sama dipakai kedua head, yang tidak dinyatakan eksplisit di berkas.
5. Angka klaim 11 pada [EVC] baris 66 dengan 10 baris pada tabel ringkas [EVC] saya jelaskan sebagai
   bit_wear K-2 yang belum dijalankan. Penjelasan itu inferensi, bukan kutipan.
6. Rasio 119x pada [EVC] adalah angka sumber. Hitungan dari 496 dibagi 4,1 menghasilkan 120,98, jadi
   sumber memakai nilai mentah yang tidak dibulatkan pada teks. Selisih itu dilaporkan, tidak
   disembunyikan.
7. Seluruh angka berasal dari satu berkas hasil satu kali jalan (`generated_at` 2026-10-29 11:21:21,
   `elapsed_s` 27,81). Tidak ada jalan ulang di sesi ini, sehingga kestabilan angka antar jalan tidak
   diuji di sini.
---

## 15. Verifikasi berkas ini

Perintah dijalankan dari `/mnt/d/Capstone 1(v2)` setelah seluruh bagian 0 sampai 14 selesai. Keluaran
ditempel apa adanya.

```
$ stat -c '%s' planning/05_KETIDAKSEPAKATAN.md
81920
$ wc -l < planning/05_KETIDAKSEPAKATAN.md
1149
$ grep -c '^|' planning/05_KETIDAKSEPAKATAN.md
189
$ grep -c '^### ' planning/05_KETIDAKSEPAKATAN.md
30
$ grep -cP '\x{2014}' planning/05_KETIDAKSEPAKATAN.md
0
$ grep -cP '\x{2013}' planning/05_KETIDAKSEPAKATAN.md
0
$ grep -c -i -E 'tidak (bisa|mungkin)|terbatas' planning/05_KETIDAKSEPAKATAN.md
0
$ grep -c 'TODO' planning/05_KETIDAKSEPAKATAN.md
0
$ grep -c '\*\*Cara menguji\.\*\*' planning/05_KETIDAKSEPAKATAN.md
5
$ grep -c '\*\*Dasar riset penyajian\.\*\*' planning/05_KETIDAKSEPAKATAN.md
5
$ grep -c '\*\*Status bukti\.\*\*' planning/05_KETIDAKSEPAKATAN.md
5
```

Bacaan keluaran:

1. `0` pada U+2014 dan `0` pada U+2013 berarti tidak ada tanda pisah panjang maupun tanda pisah pendek.
   Satu tanda pisah panjang yang semula ada di dalam kutipan `catatan_waktu` sudah diganti titik dua,
   dan penggantian itu dinyatakan terbuka di badan kutipan, bukan disembunyikan.
2. `0` pada pola frasa penyerahan berarti tidak ada kalimat penutup yang menyatakan pekerjaan mustahil
   atau menyebut cakupan secara mutlak. Kata "tidak dapat" dan "belum" tetap dipakai, karena keduanya
   disertai syarat yang dibutuhkan di bagian 13.
3. Pola pencarian pada perintah di atas ikut tertulis di blok itu, sehingga menjalankan perintah yang
   sama setelah bagian ini ada menghasilkan 1 atau 2 kemunculan, bukan 0. Kemunculan itu berada di blok
   perintah dan di kalimat butir ini sendiri, bukan di badan naskah bagian 0 sampai 14. Hal yang sama
   berlaku untuk kata TODO. Pembaca yang ingin memeriksa badan naskah dapat membatasi pencarian pada
   baris 1 sampai 1149, yaitu panjang berkas sebelum bagian 15 dan 16 ditambahkan.
4. `5` pada tiga penanda fitur berarti kelima fitur di bagian 9 memuat butir dasar riset penyajian,
   status bukti, dan cara menguji, tanpa ada yang terlewat.
5. `30` judul tingkat tiga terdiri dari 25 subbagian dan 5 judul fitur. `189` baris berpipa adalah
   seluruh tabel di berkas ini, dan 22 baris pemisah tabel menandakan 22 tabel.

Catatan kejujuran yang sama dengan dokumen riset visualisasi: angka byte dan baris di blok ini diukur
sebelum bagian 15 dan 16 ditambahkan, karena bagian ini ikut terukur. Angka final setelah seluruh
penyuntingan berhenti dilaporkan di komentar penutup kartu, dan selisih beberapa puluh byte terhadap
blok di atas berasal dari bagian ini sendiri.

---

## 16. Rujukan

### 16.1 Berkas proyek

1. [JSON] `scratch/v9_i1/v9_i1_RESULTS.json`, 57.555 byte, 1.758 baris, dihasilkan 2026-10-29 11:21:21
   dengan `elapsed_s` 27,81. Sumber utama seluruh angka head.
2. [KAT] `planning/01_KATALOG_FITUR.md`, 166.662 byte, 2.780 baris. Dipakai untuk KEP-08 (baris 673
   sampai 742), CMP-07 (baris 1982 sampai 2064), KEP-09 (baris 744 sampai 794), dan MNT-07 (baris 1186).
3. [VR] `planning/02_RISET_VISUALISASI.md`, 32.141 byte, 335 baris. Dipakai untuk bagian 5.4, 5.7, 5.9,
   5.10, bagian 6, dan bagian 7.
4. [EVC] `docs/V9_EVAL_C_LAYERC.md`, 23.153 byte, 267 baris. Dipakai untuk tabel ringkas baris 88
   sampai 99, bagian 2 per mesin, dan EC-1 sampai EC-9 baris 62 sampai 74.

### 16.2 Sumber literatur, kode sama dengan [VR]

Kode LV1 sampai LV16 dipakai konsisten dengan [VR] dan [KAT] supaya satu kode berarti satu sumber di
seluruh rangkaian dokumen.

1. LV3. Time series graphics, Forecasting: Principles and Practice, Hyndman dan Athanasopoulos, OTexts.
   https://otexts.com/fpp3/graphics.html
2. LV5. When (ish) is My Bus? User-centered Visualizations of Uncertainty, Kay, Kola, Hullman, Munson,
   CHI 2016. https://www.mjskay.com/papers/chi_2016_uncertain_bus.pdf
3. LV6. Financial Times Visual Vocabulary. https://raw.githubusercontent.com/Financial-Times/chart-doctor/main/visual-vocabulary/README.md
4. LV7. Dashboards: Making Charts and Graphs Easier to Understand, Nielsen Norman Group.
   https://www.nngroup.com/articles/dashboards-preattentive
5. LV8. Why not to use two axes, and what to use instead, Datawrapper.
   https://www.datawrapper.de/blog/dualaxis
6. LV9. Evaluate the performance of a classifier with Confusion Matrix, scikit-learn.
   https://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html
7. LV11. Postmortem Culture: Learning from Failure, Google SRE Book.
   https://sre.google/sre-book/postmortem-culture
8. LV12. Visualizing distributions: Histograms and density plots, Claus Wilke.
   https://clauswilke.com/dataviz/histograms-density-plots.html
9. LV15. The Disagreement Problem in Explainable Machine Learning: A Practitioner's Perspective, TMLR,
   arXiv 2202.01602. https://arxiv.org/html/2202.01602v6
10. LV16. Postmortems at Loon: a guiding force for rapid development, Google Cloud Blog.
    https://cloud.google.com/blog/products/devops-sre/loon-sre-use-postmortems-to-launch-and-iterate

Sepuluh sumber di atas adalah yang benar-benar dipakai di naskah ini. Enam sumber lain dari [VR]
(LV1, LV2, LV4, LV10, LV13, LV14) dipakai [VR] untuk keluaran yang bukan ketidaksepakatan, dan tidak
dikutip di sini supaya setiap kode yang muncul punya jejak pemakaian.
