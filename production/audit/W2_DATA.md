# W2 · Data dan provenance

Kartu: `t_becb7db0`. Lingkup: `production/js/data.js` saja. `index.html`,
`css/styles.css`, `js/views.js`, dan `js/app.js` tidak disentuh.

Berkas hasil:

- Path absolut: `/mnt/d/Capstone 1(v2)/production/js/data.js`
- Ukuran: 38.548 byte, 570 baris
- mtime: 2026-11-01 07:46:01 +0700
- sha256: `d0b43a22c8ff1293c956a306cc5ba4e0b896a36951ab0bace421e92775105bf2`
- Em dash: 13 kemunculan, semuanya nilai `age` (10 antrean + 3 fokus) sesuai
  perintah kartu. Nol em dash di prosa atau komentar.

## 1. Ringkasan hasil

| Target | Sebelum | Sesudah | Status |
|---|---|---|---|
| `focus.length` | 3 | 3 | OK |
| `queue.length` | 10 (sudah 10, isi belum terlacak) | 10 | OK |
| `damages.length` | 11 | 11 | OK |
| `minutes` antrean | 6,4,4,4,4,2,2,2,2,0 | 6,4,4,4,4,2,2,2,2,0 | OK |
| `well` per baris antrean | F-14 semua (sudah benar) | F-14 semua | OK |
| `age` per baris antrean | "—" semua (sudah benar) | "—" semua | OK |
| Total menit | 30 | 30 | OK |
| Komentar provenance per blok | hanya satu komentar global di kepala berkas | 14 blok berkomentar | OK |
| `node --check js/data.js` | lolos | lolos | OK |
| Error konsol saat situs dijalankan | tidak diuji | 0 error, 10 tampilan | OK |

## 2. Tabel angka sebelum dan sesudah, per blok

### 2.1 `focus`

Sumber: `planning/04_ANTREAN_TINJAUAN.md:411` (hyd), `:412` (vib), `:413` (shk).

| Butir | Sebelum | Sesudah | Sumber |
|---|---|---|---|
| hyd K-i confidence | 0,6100 | 0,6100 | 04:411 |
| hyd K-i pita | P4 | P4 | 04:411 |
| hyd K-i kepala / jendela / lead | 3 / 20 / 8,0 menit | sama | 04:411 |
| vib confidence | 0,4950 | 0,4950 | 04:412 |
| vib pita | P3 | P3 | 04:412 |
| vib kepala / jendela / lead | 3 / 429 / tidak ada | sama | 04:412 |
| shk confidence | 0,5188 | 0,5188 | 04:413 |
| shk pita | P3 | P3 | 04:413 |
| shk kepala / jendela / lead | 3 / 20 / tidak ada | sama | 04:413 |
| vib sinyal | "AUPRC 0,6204" | "AUPRC 0,4806 sampai 0,8481" | ledger S2-018, S2-025, S2-032, S2-039 |
| `age` | "belum dihitung" | "—" | 04 bagian 6.2 tidak punya kolom umur |

Catatan: angka 0,6204 tidak ada di `docs/RND_PROVENANCE_LEDGER.md` maupun di
`planning/`. Ledger mencatat AUPRC vib per sumur: 0,8481 / 0,5452 / 0,4806 /
0,6073 (`docs/RND_PROVENANCE_LEDGER.md:2393, 2400, 2407, 2414`).

### 2.2 `queue` (10 baris)

Sumber tunggal: `planning/04_ANTREAN_TINJAUAN.md:411-420`. Isi baris sudah
sesuai 04 sebelum kartu ini dikerjakan; yang diperbaiki adalah provenance,
status awal, dan sinyal vib.

| Kolom | Sebelum | Sesudah | Sumber |
|---|---|---|---|
| jumlah baris | 10 | 10 | 04:411-420 |
| `well` | F-14 (10 baris) | F-14 (10 baris) | 04:1248, seluruh baris 6.2 dari segmen F-14 |
| `age` | "—" | "—" | 04 tidak punya kolom umur |
| `minutes` | 6,4,4,4,4,2,2,2,2,0 | sama | 04:411-420 kolom Menit |
| `conf` | 0,6100 / 0,4950 / 0,5188 / 0,4562 / 0,4550 / 0,3333 / 0,3333 / 0,3030 / 0,2525 / 0,2623 | sama | 04:411-420 kolom K_tampil |
| `pita` | 4,3,3,3,3,2,2,2,2,2 | sama | 04:411-420 kolom Pita |
| `heads` | 3,3,3,3,1,1,1,1,1,1 | sama | 04:411-420 kolom Kepala nyala |
| `status` | Baru/Ditinjau/Ditunda campur tanpa dasar | 9 "Baru", 1 "Ditutup" (ssi) | 04 tidak punya kolom status; baris ssi aksinya "tutup" (04:420) |
| sinyal vib | "AUPRC 0,6204" | "K 0,4950" | 04:412 |
| `note` | parafrase | alasan 04 apa adanya | 04:411-420 kolom Alasan |

### 2.3 `damages` (11 kelas)

Kolom `k` dan `pita` memakai K_tampil dan pita dari 04, bukan K_seg dari 06.
Kolom `vote` dan `weight` tetap dari 06 dan diberi label sumber di komentar blok.

| Kelas | k sebelum | k sesudah | pita sebelum | pita sesudah | vote / weight | Sumber k | Sumber vote |
|---|---|---|---|---|---|---|---|
| hyd K-i | 0,6100 | 0,6100 | P4 | P4 | V-2 Tolak / 3,30 | 04:411 | 06:226 |
| vib | 0,4950 | 0,4950 | P3 | P3 | V-1 Dukung / 1,65 | 04:412 | 06:222 |
| shk | 0,5188 | 0,5188 | P3 | P3 | V-2 Tolak / 1,40 | 04:413 | 06:227 |
| stuck K-i | 0,4562 | 0,4562 | P3 | P3 | V-2 Tolak / 1,40 | 04:414 | 06:225 |
| stuck K-ii | 0,3333 | 0,3333 | P2 | P2 | V-2 Tolak / 0,75 | 04:416 | 06:228 |
| bit_wear K-1 | 0,2525 | 0,2525 | P2 | P2 | V-2 Tolak / 0,25 | 04:419 | 06:224 |
| bit_wear K-2 | tidak ada | tidak ada | P0 | P0 | V-3 AB-1 / 0,00 | 06:302 | 06:302 |
| tool_wear K-i | 0,4550 | 0,4550 | P3 | P3 | V-2 Tolak / 1,25 | 04:415 | 06:223 |
| tool_wear K-ii | **0,6013** | **0,4550** | P3 | P3 | V-1 Dukung / 0,25 | 06:221 | 06:221 |
| hyd K-ii | tidak ada | tidak ada | P0 | P0 | V-3 AB-1 / 0,00 | 06:302 | 06:302 |
| ssi | 0,2623 | 0,2623 | P2 | P2 | V-2 Tolak / 0,40 | 04:420 | 06:229 |

Perbaikan isi teks:

| Butir | Sebelum | Masalah | Sesudah |
|---|---|---|---|
| vib `limit` | "Batas kelas 0,4950 menahan pita di P2" | 04:412 menulis P3 | "menahan pita di P3, bukan P2 (04 bagian 6.2 baris 2)" |
| vib `evidence` | "AUPRC 0,6204. Presisi 0,4527. Recall 0,6292." | tiga angka tidak ada di ledger | AUPRC 0,4806-0,8481 dan 5.429 positif (S2-018/025/032/039, S2-012) |
| stuck K-i `evidence` | "Kesepakatan kelas positif 23,81 persen" | 23,81 milik shk (`planning/05_KETIDAKSEPAKATAN.md:347`), bukan stuck | K_min 1,0000 terpotong 0,4562 (04 bagian 6.2 baris 4) |
| tool_wear K-i `evidence` | "Deteksi 4 dari 4 alat" | sumber menulis "empat alat saja", bukan deteksi 4 dari 4 (RND_S6_PM_WAVE2.md:155) | presisi run 0,50, FP 1 sampai 3 per alat (RND_S6_PM_WAVE2.md:155) |
| hyd K-ii `evidence` | "78,7 persen" tanpa sitasi | sitasi lama menunjuk 06 konflik H-5, yang tidak memuat angka itu | ditambah "(RND_PM_VERDICT.md:131, PM-110)" |
| tool_wear K-ii `evidence` | "K_segmen 0,6013 dipotong ke batas kelas 0,4550" | benar, tapi tanpa sitasi | ditambah "(06 bagian 2.3, baris 221)" |

### 2.4 Blok lain yang angkanya salah dan diperbaiki

| Blok | Sebelum | Sesudah | Sumber |
|---|---|---|---|
| `tk.coverage` | 0,87 | 1,00 | 06:427, "9,15 dibagi 9,15 sama dengan 1,00" |
| `hydModes[0].tp` | 3.804 | 5.579 | 04:73 |
| `hydModes[1].folds` | "5 dari 9" | "7 FAR · 6 recall" | 04:74 |
| `hydModes[3].folds` | "5 dari 9" | "9 FAR · 5 recall" | 04:76 |
| `load[0].p50/p95` | 12,4 / 38,7 | 16 / 24 | 04:138 |
| `load[1].p50/p95` | 12,4 / 38,7 | 18 / 26 | 04:142 |
| `load[2].p50/p95` | 8,0 / 21,5 | 5 / 10 | 04:141 |
| `load[3].p50/p95` | 3,1 / 9,8 | 2 / 5 | 04:139 |
| `load[4].p50/p95` | 4,0 / 11,2 | 3 / 6 | 04:140 |
| `load[*].budget` | 24 | 30 | 04 bagian 5.2 dan 6.4, anggaran 30 menit |
| `docs[0].bytes` | 40.064 | 40.271 | `stat` pada 2026-11-01 |
| `docs[0].lines` | "9 bagian" | "437 baris" | `wc -l` |
| `docs[1].lines` | "1.015 baris" | "292 baris" | `wc -l` |
| `features[2].note` | "12 baris, 9 kolom" | "10 baris, 10 kolom" | 04:411-420 |
| `provenance[4]` (vib AUPRC) | "0,6204 ... dirujuk di 06 baris 113" | "0,4806 sampai 0,8481 ... ledger S2-018/025/032/039" | ledger |
| `provenance[5]` (ssi presisi) | "0,0237 ... 06 baris 114" | "12,1 per alarm benar ... ledger S2-448" | ledger |
| `glossary[1].example` | "vib K_seg 0,60 tetap P2" | "tetap P3" | 06:396, P3 = 0,40 sampai 0,59 |
| `glossary[11].example` | "cakupan 0,87" | "cakupan bobot 1,00" | 06:427 |

Catatan `provenance[4]`: sitasi lama menunjuk `06 baris 113`, padahal baris itu
ada di dalam skrip awk, bukan tabel data. `provenance[5]`: angka 0,0237 tidak
muncul di ledger mana pun (`rg '0,0237' planning/ docs/` = 0 hasil).

### 2.5 Blok yang dibuang karena tidak bisa dilacak

| Blok | Isi lama | Alasan | Tindakan |
|---|---|---|---|
| `decisions` | 6 baris dengan jam 06:42 sampai 11:30, nama peran, sumur F-15/F-12/F-3/F-9/F-14, dan besaran "tekanan turun 6,2 persen", "torsi naik 18 persen" | tidak satu pun angka atau peristiwa ini ada di `planning/` atau `docs/`. views.js sendiri menulis foot "Log disimpan di sesi ini. Bukan audit resmi", jadi ini log sesi, bukan riwayat | array dikosongkan, terisi saat pengguna mencatat keputusan lewat `app.js` |
| `wells` | F-1, F-3, F-5, F-7, F-9, F-15 | tidak ada sumber pemetaan kanal per sumur untuk enam sumur itu | menjadi `["F-14"]`, satu-satunya segmen yang punya ukuran kanal |
| `channels[].wells` | 6 x 6 status siap/tipis/absen tanpa sumber | status kanal per sumur tidak terukur selain F-14 | satu kolom: VIB "siap" (356/1.989 kosong = 17,9 persen, 01_KATALOG_FITUR.md:1636), SSI "absen" (96,6 persen kosong, :1635), empat kanal lain "belum" |
| `signalFeasibility` | "Kanal tipis di F-15", "Absen di F-15" | klaim tanpa ukuran | diganti status "Belum dikutip" dengan alasan, kecuali Getaran yang punya angka |
| `channelsInstall` | "Absen di F-15", "Tipis di F-15", "Terisi di 5 dari 6 sumur" | tanpa ukuran | CRPM diberi angka 62,3 dan 96,6 persen; tiga kanal lain ditandai "BELUM KUTIP" |

## 3. Hasil `rg` wajib

Perintah: `rg -n 'F-15|F-12|F-10|F-9|F-7|Bengkel|0,58|0,47|0,51|0,35' js/data.js`

Delapan hit, semuanya dijelaskan:

| Baris | Teks | Penjelasan |
|---|---|---|
| 31 | `batas dominasi 0,35, S = 18,23 persen` | komentar provenance. 0,35 adalah batas dominasi yang benar dan bersumber di `06_SWARM_KONSENSUS.md:452` ("0,35 x 9,15"). Bukan angka yatim |
| 52 | `shk 0,5188 P3 ... (04 baris 413)` | komentar provenance. Cocokkan pola `0,51` di dalam `0,5188`, bukan angka 0,51 |
| 147 | `cap: "0,5188"` | batas kelas shk, `06:439`. Substring `0,51` |
| 148 | `k: "0,5188"` | K_tampil shk, `04:413`. Substring `0,51` |
| 231 | `cap: "0,5125"` | batas kelas hyd K-ii, `06:121` (`wcap` hyd K-ii 0.5125) dan `06:545`. Substring `0,51` |
| 236 | `Batas kelas hyd K-ii 0,5125` | teks limit yang sama, disitasi ke 06 bagian 2.3. Substring `0,51` |
| 267 | `conf: 0.5188 ... shk 0,5188` | baris antrean Q-1043, `04:413`. Substring `0,51` |
| 479 | `{ id: "F-10", name: "Kamus istilah" }` | `F-10` di sini adalah **kode fitur**, bukan sumur. Sumber `planning/11_PRIORITAS_BUILD.md` daftar fitur |

Hasil untuk token yang benar-benar dilarang sebagai nilai data:

- `F-15`, `F-12`, `F-9`, `F-7`: **0 hit** setelah perbaikan. Semua sudah dibuang dari `wells`, `decisions`, `signalFeasibility`, dan `channelsInstall`.
- `Bengkel`: **0 hit**. Kata "bengkel" hanya muncul sebagai istilah operasi di `task` kelas tool_wear K-i ("Deteksi perubahan regime di bengkel"), yang berasal dari `planning/04_ANTREAN_TINJAUAN.md:120` ("satu pemeriksaan bengkel per shift"). Itu bukan nama sumur. Huruf besar `Bengkel` tidak ada.
- `0,58`, `0,47`: **0 hit**.
- `0,51` sebagai angka berdiri sendiri: **0 hit**; semua kemunculan adalah bagian dari 0,5188 atau 0,5125.

## 4. Verifikasi yang dijalankan

### 4.1 Sintaks dan hitungan

```
$ node --check js/data.js
SYNTAX OK

$ node <skrip verifikasi>
focus.length   = 3 OK
queue.length   = 10 OK
damages.length = 11 OK
minutes        = 6,4,4,4,4,2,2,2,2,0 OK
queue wells    = F-14 OK
queue ages     = — OK
focus conf     = hyd_ki 0.6100 P4 3k 20 jendela lead=8,0 menit ; vib 0.4950 P3 3k 429 jendela lead=tidak ada ; shk_ki 0.5188 P3 3k 20 jendela lead=tidak ada
focus wells    = F-14
damages k/pita = hyd_ki:0,6100/P4 vib:0,4950/P3 shk_ki:0,5188/P3 stuck_ki:0,4562/P3 stuck_kii:0,3333/P2 bit_wear_k1:0,2525/P2 bit_wear_k2:tidak ada/P0 tool_wear_ki:0,4550/P3 tool_wear_kii:0,4550/P3 hyd_kii:tidak ada/P0 ssi:0,2623/P2
decisions      = 0
wells          = ["F-14"]
tk.coverage    = 1
total minutes  = 30
```

### 4.2 Situs dijalankan

Server statis `python3 -m http.server 8899` di `production/`, lalu dimuat di
browser sungguhan.

| Pemeriksaan | Hasil |
|---|---|
| Error konsol saat muat | 0 |
| Jumlah `section.view` yang dirender | 10 dari 10 rute (`#beranda` `#perencanaan` `#data` `#mesin` `#bukti` `#linimasa` `#kepercayaan` `#batas` `#kamus` `#alat-bantu`) |
| Error konsol setelah menelusuri 10 rute | 0 |
| Baris antrean di `#perencanaan` | 10, teks "10 baris · 9 belum ditinjau · 0 ditunda" |
| Total menit di `#perencanaan` | "30 menit untuk 10 baris" |
| Kartu fokus di `#beranda` | 3, keyakinan 0,6100 / 0,4950 / 0,5188 |
| Matriks kanal di `#data` | 1 kolom sumur `F-14`, 6 kanal, sel `belum,belum,belum,belum,siap,absen` |
| Log keputusan di `#linimasa` | 0 baris, kepala "4 gerbang · 12 konflik · 0 keputusan" |
| Overflow horizontal pada 375 / 768 / 1440 px di 4 tampilan | 0 px di semua kombinasi |

## 5. Temuan di luar kartu ini (bukan target edit W2)

Tiga angka di `production/js/views.js` bertentangan dengan sumber, dan berkas
itu dilarang diubah oleh kartu ini. Dicatat untuk pemilik kartu tampilan:

| Lokasi | Isi | Bertentangan dengan |
|---|---|---|
| `js/views.js:149-151` dan `:403-405` | "Median 12,4 menit", "Ekor 38,7 menit", "Sisa anggaran 1.240 menit" | `04:138-143` memberi p50 16/18/5/2/3 dan p95 24/26/10/5/6; anggaran 30 menit, bukan 1.240 |
| `js/views.js:284` dan `:801` | "cakupan bobot 0,87" | `06:427` menghitung 9,15/9,15 = 1,00 |
| `js/views.js:663` | "vib AUPRC 0,6204, prevalensi 0,2542, 2,44x" | angka 0,6204 tidak ada di ledger; AUPRC vib per sumur 0,4806 sampai 0,8481 (S2-018/025/032/039). Prevalensi 0,2542 juga tidak ditemukan |
| `js/views.js:834` | `#decision-body` tanpa keadaan kosong | R-27. Dengan log sesi kosong, tabel tampil tanpa penjelasan |

Konsekuensi yang terlihat: banner `tk` di `#beranda` sekarang menampilkan
cakupan bobot 1,00 dari `data.js`, sedangkan kartu Linimasa menampilkan 0,87
dari views.js. Selisih itu berasal dari views.js, bukan dari data.

## 6. Sumber yang dipakai

- `planning/04_ANTREAN_TINJAUAN.md` bagian 2.1, 2.3, 2.4, 3, 5.2, 6.2, 6.3, 6.4, 9
- `planning/06_SWARM_KONSENSUS.md` bagian 2.3, 4.4, 5.2, 5.3, 6.2
- `planning/05_KETIDAKSEPAKATAN.md` baris 347
- `planning/01_KATALOG_FITUR.md` baris 1634-1636, 1666
- `planning/00_INVENTARIS_V3_V6.md` baris 303
- `planning/00_VERIFIKASI_INVENTARIS.md` baris 378
- `docs/RND_S6_PM_WAVE2.md` baris 110, 114, 150, 154, 155
- `docs/RND_PM_VERDICT.md` baris 131 (PM-110)
- `docs/RND_S4_LAYER_B_DATA.md` baris 63, 68
- `docs/RND_ENGINE_S6_INTEGRATION.md` baris 24-26
- `docs/RND_R8_EVALUASI_BERLAPIS.md` baris 188
- `docs/RND_PROVENANCE_LEDGER.md` S2-007, S2-012, S2-018, S2-025, S2-032, S2-039, S2-448
- `planning/DESIGN.md` baris 360
