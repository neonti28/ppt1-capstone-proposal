# INVENTARIS VONIS RND GELOMBANG DUA SAMPAI V11

Kartu: `t_fca63a76`. Tanggal: 2026-10-31 (WIB). Workspace: `/mnt/d/Capstone 1(v2)`.
Keluaran: dokumen ini saja, di folder `planning/`. Tidak ada berkas lain yang dibuat kartu ini.

Kerangka wajib dipatuhi: alarm otomatis bukan tujuan; setiap angka punya sumber berkas dan baris; klaim tanpa bukti tidak ditulis; kekurangan data dikemas menjadi fitur; setiap fitur punya pengguna, momen pakai, masukan, keluaran, dan status bukti; laporan ditutup dengan syarat, bukan dengan kata menyerah; hanya markdown; tanpa tanda pisah panjang.

---

## 0. Ringkasan

Sepuluh dokumen dibuka penuh, 201443 byte dan 2278 baris. Delapan berlaku, dua digantikan, nol diarsipkan penuh. Yang usang bukan dokumen utuh melainkan segmen: tabel sembilan cacat di audit S5, tabel cacat yang sama di S6 bagian 8, dan vonis kesiapan V10. Vonis yang mengikat sekarang adalah komposisi H1p untuk hyd mode peringatan dini dengan FAR kalender median 4,0984 dan 7 dari 9 fold memenuhi FAR serta recall sekaligus, tier tidak naik, slot alarm otomatis tetap nol, dan penahan kenaikan tier adalah lapisan B yang belum punya kolom biaya maupun berkas jadwal inspeksi.

Dari 10 dokumen itu lahir 14 calon fitur. Dua di antaranya, F-11 dan F-12, dibangun justru dari dokumen yang sudah digantikan.

---

## 1. Berkas yang dibuka, ukuran, dan status

Ukuran diambil dengan `ls -l` dan `wc -c -l` pada 2026-10-31. Semua dibuka sampai baris terakhir.

| No | Berkas | Byte | Baris | Status | Alasan | Segmen usang |
|---|---|---|---|---|---|---|
| 1 | `docs/RND_S6_PM_WAVE2.md` | 40271 | 437 | BERLAKU | Vonis terakhir gelombang 2 dan tidak ada S7 atau dokumen sesudahnya di `docs/` (123 berkas diperiksa). Memuat komposisi terpilih per kelas, peta tier, 18 penolakan, dan 11 butir belum terverifikasi | Bagian 8 baris 372 sampai 382 masih menulis sembilan cacat "belum diperbaiki", sedangkan catatan di baris 398 dan `RND_S5_DEFECT_STATUS.md` menyatakan sudah ditangani. Badan bagian 8 tidak disunting |
| 2 | `docs/RND_S5_AUDIT_WAVE2.md` | 27190 | 292 | DIGANTIKAN | Fungsi dokumen ini adalah register cacat, dan register itu digantikan `RND_S5_DEFECT_STATUS.md` yang menutup kesembilan butir. Tabel ukuran berkas di bagian 1 sudah tidak cocok dengan disk (lihat bagian 7 dokumen ini) | Tabel cacat bagian 7 baris 251 sampai 261, seluruhnya berstatus selesai di dokumen pengganti. Bagian 2 tentang rerun 143 sel tetap sah dan tetap dikutip |
| 3 | `docs/RND_S5_DEFECT_STATUS.md` | 3418 | 57 | BERLAKU | Status terakhir kesembilan cacat, dengan angka pengganti dan perintah pemeriksa. Dua klaimnya saya uji ulang dan cocok (bagian 2 dokumen ini) | Tidak ada |
| 4 | `docs/RND_ENGINE_S6_INTEGRATION.md` | 3915 | 76 | BERLAKU | Satu-satunya catatan perubahan engine setelah S6: head utama hyd, blok nilai maintenance, profil kapabilitas tujuh engine, dan pernyataan bahwa keputusan akhir ada pada manusia | Kolom "Sebelum" di bagian 1 baris 9 sampai 15 adalah keadaan pra perubahan, sah sebagai riwayat, bukan keadaan sekarang. Angka gangguan di bagian 2 belum sepakat dengan S4 (bagian 7 dokumen ini) |
| 5 | `docs/RND_S2_HYBRID_VIB_SSI.md` | 25135 | 317 | BERLAKU | Basis bukti vib dan ssi: 23922 baris empat well, 35906 baris sembilan fold, kurva sensitivitas anggaran, dan vonis bahwa tidak ada model lolos gate A di kedua kelas. S6 hanya menambah uji H1p di atasnya | Tidak ada. Catatan provenance 2026-10-29 sudah masuk di baris 26 sampai 30 |
| 6 | `docs/RND_S3_HYBRID_BITWEAR.md` | 22275 | 224 | BERLAKU | Basis bukti bit_wear: 198928 baris, nol kolom identitas bit, rekonstruksi label dengan akurasi 1,000000, dan gate A lolos 0 dari 7 fold | Tidak ada |
| 7 | `docs/RND_S4_LAYER_B_DATA.md` | 23799 | 213 | BERLAKU | Satu-satunya pendataan lapisan B: 23447 record aktivitas, 1777,75 jam repair dan maintain, 533 record register kegagalan, dan bukti ketiadaan biaya lewat pemindaian token pada 3518 dokumen | Tidak ada. Cacat D1 pada baris ledger S4-013 sudah diperbaiki dan saya buktikan (bagian 2) |
| 8 | `docs/V10_PM2_VERDICT.md` | 8545 | 87 | DIGANTIKAN | Vonis kesiapan "LOLOS sebagai proposal teknis siap pakai" digantikan `V11_PM_FINAL.md` yang menilai proposal yang sama terhadap versi arsip dan menambahkan sembilan syarat perbaikan sebelum dokumen dipakai berkarya. Angka struktural 7 engine, 11 klaim, 27 head di dalamnya dipakai ulang dan diverifikasi ulang oleh V11 bagian 1c butir 8 | Bagian 3 baris 54 sampai 60 adalah log patch P1 sampai P5 yang sudah diterapkan, jadi berlaku sebagai riwayat tertutup. Bagian 5 baris 78 sampai 85 memuat klausa kesiapan yang sudah digantikan |
| 9 | `docs/V11_PM_FINAL.md` | 20660 | 288 | BERLAKU | Vonis terakhir seri V, tidak ada V12 atau sesudahnya. Memuat skor 96 lawan 46,2, uji sensitivitas, dan sembilan perbaikan yang masih terbuka pada pemenang | Tidak ada |
| 10 | `docs/RND_S1_SEED_ROBUSTNESS.md` | 26235 | 287 | BERLAKU | Dirujuk langsung oleh S6 bagian 2.1 sebagai sumber angka F-14 dan cakupan per well. Tidak ada di daftar masukan kartu, tetapi misi kartu meminta S1 sampai S6, jadi berkas ini dibuka dan dihitung | Tidak ada |

Jumlah sembilan berkas masukan resmi: 175208 byte dan 1991 baris. Dengan S1 menjadi 201443 byte dan 2278 baris.

Catatan definisi status:

- BERLAKU berarti isinya masih menjadi rujukan keputusan dan tidak ada dokumen lebih baru yang mengambil alih fungsinya.
- DIGANTIKAN berarti fungsi dokumen sudah diambil alih dokumen lain, sedangkan isinya tetap dipakai sebagai riwayat atau sebagai sumber angka tertentu.
- ARSIP berarti tidak ada fungsi aktif sama sekali. Tidak ada dokumen pada daftar ini yang masuk kategori itu, karena setiap dokumen masih menyumbang minimal satu angka atau satu bukti. Yang masuk kategori arsip adalah segmen, dan segmen itu dicatat pada kolom terakhir tabel di atas.

---

## 2. Bukti perintah

Bagian ini menempelkan keluaran perintah yang dipakai untuk memeriksa angka, sesuai kerangka butir 3.

Dua hal pada penyajian di bawah perlu dinyatakan lebih dulu supaya tidak terbaca sebagai kutipan verbatim. Pertama, keluaran `ls -l` diringkas pada kolom ukuran, tanggal, dan nama berkas, sedangkan kolom izin, pemilik, dan grup dihapus. Kedua, daftar sembilan berkas pada perintah `for` diganti dengan penanda `<sembilan berkas masukan>` agar baris tidak melebar. Nilai ukuran, tanggal, dan seluruh keluaran hitung lain disalin apa adanya.

### 2.1 Ukuran berkas

```
$ ls -l RND_ENGINE_S6_INTEGRATION.md RND_S2_HYBRID_VIB_SSI.md RND_S3_HYBRID_BITWEAR.md \
      RND_S4_LAYER_B_DATA.md RND_S5_AUDIT_WAVE2.md RND_S5_DEFECT_STATUS.md \
      RND_S6_PM_WAVE2.md V10_PM2_VERDICT.md V11_PM_FINAL.md
  3915 2026-10-29 11:24 RND_ENGINE_S6_INTEGRATION.md
 25135 2026-10-29 11:23 RND_S2_HYBRID_VIB_SSI.md
 22275 2026-10-29 11:23 RND_S3_HYBRID_BITWEAR.md
 23799 2026-10-29 11:23 RND_S4_LAYER_B_DATA.md
 27190 2026-10-28 06:59 RND_S5_AUDIT_WAVE2.md
  3418 2026-10-29 11:24 RND_S5_DEFECT_STATUS.md
 40271 2026-10-29 11:24 RND_S6_PM_WAVE2.md
  8545 2026-10-15 06:18 V10_PM2_VERDICT.md
 20660 2026-10-15 13:29 V11_PM_FINAL.md

$ wc -c -l <sembilan berkas yang sama>
   437  40271 RND_S6_PM_WAVE2.md
   292  27190 RND_S5_AUDIT_WAVE2.md
    57   3418 RND_S5_DEFECT_STATUS.md
    76   3915 RND_ENGINE_S6_INTEGRATION.md
   317  25135 RND_S2_HYBRID_VIB_SSI.md
   224  22275 RND_S3_HYBRID_BITWEAR.md
   213  23799 RND_S4_LAYER_B_DATA.md
    87   8545 V10_PM2_VERDICT.md
   288  20660 V11_PM_FINAL.md
  1991 175208 total
```

S1, berkas kesepuluh:

```
$ ls -l docs/RND_S1_SEED_ROBUSTNESS.md
 26235 2026-10-29 11:23 docs/RND_S1_SEED_ROBUSTNESS.md
$ wc -c -l docs/RND_S1_SEED_ROBUSTNESS.md
  287 26235 docs/RND_S1_SEED_ROBUSTNESS.md
```

### 2.2 Blok ledger S6 dan cacat D1

```
$ wc -l docs/RND_PROVENANCE_LEDGER.md
3434 docs/RND_PROVENANCE_LEDGER.md

$ sed -n '3228p' docs/RND_PROVENANCE_LEDGER.md
## Bagian S6: vonis PM gelombang 2 dan pemilihan komposisi (kartu `t_b5830542`)

$ grep -c '^| S6-' docs/RND_PROVENANCE_LEDGER.md
191

$ sed -n '3425p' docs/RND_PROVENANCE_LEDGER.md
| S6-191 | BELUM | tidak terukur | BELUM-TERUKUR | H1p dan H1p3 pada shk, stuck, bit_wear, tool_wear: belum dijalankan | bagian 8 | BELUM (kartu S6) |

$ grep -n '^| S4-013' docs/RND_PROVENANCE_LEDGER.md
2182:| S4-013 | 884 record / 20 kolom | record / kolom | RUN-KITA | labels_duration.json:n_baris | bagian 2 baris 2 | TERUKUR |
```

Tiga hal terbukti di sini. Pertama, klaim S6 baris 10 bahwa blok `S6-` berheader di baris 3228 dan berisi 191 baris data sampai baris 3425 cocok persis dengan berkas. Kedua, cacat D1 sudah benar di baris 2182, isinya sekarang "884 record / 20 kolom", bukan "884 kolom". Ketiga, jumlah baris per prefiks pada ledger adalah S1 84, S2 455, S3 92, S4 95, S5 387, S6 191, dan jumlah itu cocok dengan tabel audit S5 bagian 4 untuk keempat kartu gelombang dua.

### 2.3 Gaya angka ribuan di ledger

```
$ awk -F'|' 'NF>6 {gsub(/^ +| +$/,"",$3); if ($3 ~ /^[0-9]{1,3}(\.[0-9]{3})+$/) c++} END {print "jumlah:", c+0}' \
      docs/RND_PROVENANCE_LEDGER.md
jumlah: 0
```

Cacat D4 yang dilaporkan berjumlah 61 sel tidak lagi ditemukan pada kolom angka. Sisa nol, sesuai klaim `RND_S5_DEFECT_STATUS.md` baris 21.

### 2.4 Tanda pisah panjang pada berkas masukan

```
$ for f in <sembilan berkas masukan>; do printf "%s " "$(grep -c $'\u2014' "$f")"; echo "$f"; done
0 docs/RND_S6_PM_WAVE2.md
0 docs/RND_S5_AUDIT_WAVE2.md
0 docs/RND_S5_DEFECT_STATUS.md
2 docs/RND_ENGINE_S6_INTEGRATION.md
0 docs/RND_S2_HYBRID_VIB_SSI.md
0 docs/RND_S3_HYBRID_BITWEAR.md
0 docs/RND_S4_LAYER_B_DATA.md
0 docs/V10_PM2_VERDICT.md
0 docs/V11_PM_FINAL.md
```

Dua kemunculan di `RND_ENGINE_S6_INTEGRATION.md` ada di baris 49 dan baris 61. S6 sendiri menutup dengan pernyataan nol tanda pisah panjang di baris 437, dan itu cocok.

### 2.5 Tidak ada dokumen sesudah S6 dan V11

```
$ ls -1 docs/ | grep -E 'S[7-9]|V1[2-9]'
(kosong)
$ ls -1 docs/ | wc -l
123
```

Ini dasar pernyataan bahwa S6 dan V11 adalah vonis terakhir pada masing masing seri.

---

## 3. Angka S6 dan sumbernya

Semua angka di bawah dikutip dari `docs/RND_S6_PM_WAVE2.md` dengan nomor baris. Tidak ada angka yang dihitung ulang oleh kartu ini.

| Angka | Nilai | Sumber | Arti |
|---|---|---|---|
| H1p: FP, TP | 927 dan 4924 | bagian 4.1, baris 196 | komposisi terpilih hyd mode peringatan dini, rule kanal DAN gerbang persistence |
| H1p: presisi, recall | 0,8243 dan 0,6519 | bagian 4.1, baris 196 | presisi dan recall median lintas 9 fold, 2 seed |
| H1p: FAR kalender median | 4,0984 per 24 jam | bagian 4.1, baris 196 | di bawah anggaran 6 |
| H1p: lead median | 8,0 menit | bagian 4.1, baris 196 | lebih pendek 3,5 menit dari H1 |
| H1p: fold memenuhi FAR dan recall | 7 dari 9 | bagian 4.1, baris 196 | kriteria keputusan yang dipakai S6 |
| H1 pembanding | FP 935, TP 3804, presisi 0,7789, recall 0,5638, FAR 3,5302, lead 11,5, 5 dari 9 fold | bagian 4.1, baris 194 | komposisi R8 yang digantikan pada hyd |
| H1p3 mode alarm rendah | FP 568, TP 3557, presisi 0,8646, recall 0,5296, FAR 2,0323, lead 12,5, FAR lolos 9 dari 9, recall lolos 5 dari 9 | bagian 4.1, baris 197 | satu satunya komposisi yang memenuhi FAR di semua fold |
| Selisih H1p terhadap H1 | TP +1120 atau 29,4427 persen, FP -8, presisi +0,0453, recall +0,088, FAR +0,5682, lead -3,5 menit, onset 218 lawan 219 | bagian 4.1, baris 204 sampai 208 | pertukaran, bukan dominasi |
| Beban alarm per onset | 2,3769 H1p, 2,3974 H1, 1,4564 H1p3 | bagian 3, baris 150 dan 151 | biaya perhatian per kejadian |
| Biaya memilih H1p3 | 247 TP lebih sedikit daripada H1 | bagian 4.2, baris 221 | konsekuensi yang wajib ditulis pada mode alarm rendah |
| Stabilitas seed | `beda_sel` 0 pada 45 sel hyd, 20 sel vib, 45 sel ssi | bagian 1.1, baris 53 | komposisi deterministik memang identik di dua seed |
| Reproduksi R8 | 30 pemeriksaan bernama, 30 lulus | bagian 1.1, baris 49 | termasuk FP 935 dan TP 3804 |
| Kontrol negatif | 2 dari 2 fold berubah antar seed, F-14 dari 362 FP dan 42 TP menjadi 534 FP dan 71 TP | bagian 1.1, baris 55 sampai 57 | bukti harness peka seed, tanpa ini klaim identik tidak sah |
| Penolakan algoritma | 18 penolakan, 7 di antaranya kegagalan bentuk DAN | bagian 6.1, baris 312 | dasar aturan prasaring komposisi DAN |
| vib pada S6 | H1p FP 183 lawan persistence 1456, recall 0,1906, 0 dari 4 fold mencapai 0,5 | bagian 2.2, baris 113 | tidak ada komposisi yang lolos |
| ssi pada S6 | H1p 1 TP dan 17 FP dari 132 onset, recall 0,0 | bagian 2.2, baris 114 | komposisi praktis tidak menyala |
| bit_wear pada S3 | gate A lolos 0 dari 7 fold, rule presisi 0,1492 dan FAR 241,948, ML kanal fisik presisi 0,6496 dan FAR 110,432 | bagian 2.2, baris 115 | penyebabnya satuan dan kunci, bukan model saja |
| Lapisan B waktu | 2453 record dan 5821,417 jam pada tiga kategori, repair 806 record dan 1215,0 jam, median 1,0 jam, p90 3,5 jam | bagian 7.1, baris 351 sampai 354 | nilai waktu terukur, rupiah tidak |
| Register kegagalan | 325 dari 1759 laporan memuat `equipmentfailureInfoTable`, 533 record | bagian 7.1, baris 348 | isinya downtime menit, bukan uang |
| Butir belum terverifikasi | 27 butir pada empat dokumen: 8 S1, 6 S2, 6 S3, 7 S4 | bagian 7.2, baris 361 | batas klaim gelombang 2 |
| Cakupan per well | F-10 0,673 dan F-5 0,0171 | bagian 5, baris 255 | alasan badge hyd harus bersyarat per well |
| Slot alarm otomatis | 0 | bagian 3.1, baris 167 | tidak ada pemutus otomatis |

Peta tier yang berlaku, dari bagian 3.1 baris 163 sampai 167: vib rule PERINGATAN-BERPENGAWAS dan RF TREN; ssi hybrid PERINGATAN-BERPENGAWAS dan RF TREN; shk rule PERINGATAN-BERPENGAWAS dan ML TREN; stuck K-i PERINGATAN-BERPENGAWAS dengan cakupan dua well dan K-ii TREN; hyd K-i PERINGATAN-BERPENGAWAS pada dua mode dan K-ii BELUM LAYAK PAKAI; bit_wear K-1 TREN; tool_wear `op_far_calibrated` PERINGATAN-BERPENGAWAS dan `calib_5of27` TREN.

Keadaan engine setelah integrasi, dari `RND_ENGINE_S6_INTEGRATION.md`: head utama hyd adalah `hybrid_rule_and_persistence` (bagian 1 baris 11), tujuh engine dengan 27 head, lapisan L0 5, L1 11, L2 9, L3 2, dan keputusan akhir ada pada manusia (bagian 4 baris 59 sampai 61). Dokumen yang sama menyatakan angka beban tinjauan berasal dari segmen F-14, bukan median lintas fold (bagian 5 butir 3 baris 67). Itu batas yang wajib ikut tercetak setiap kali angka beban tinjauan dipakai.

---

## 4. Yang berlaku dan yang tidak lagi berlaku

### 4.1 Berlaku

1. Komposisi hyd mode peringatan dini: H1p, rule kanal DAN gerbang persistence, dengan h dipilih per well kalibrasi (S6 bagian 3 baris 150).
2. Mode alarm rendah hyd: H1p3, dengan konsekuensi 247 TP lebih sedikit (S6 bagian 4.2 baris 221).
3. Komposisi kelas lain tidak berubah: shk single ML untuk tren dan rule untuk peringatan, stuck triase, tool_wear engine terkalibrasi per alat, vib rule untuk peringatan dan RF untuk pemeringkatan, ssi persistence untuk pemeringkatan, bit_wear persistence untuk pemeringkatan (S6 bagian 4.3 baris 226 sampai 233).
4. Tidak ada kenaikan tier dan slot alarm otomatis tetap nol (S6 bagian 5 baris 249 dan 265).
5. Badge hyd bersyarat per well, bukan klaim global (S6 bagian 5.2 baris 280).
6. Aturan prasaring: komposisi DAN dilarang dipakai bila salah satu komponen menghasilkan hampir nol keluaran pada anggaran yang sama (S6 bagian 6.1 baris 318 sampai 320).
7. Vonis proposal: V10 menang 96 lawan 46,2, selisih 49,8, memimpin 4 dari 4 kriteria, dengan sembilan perbaikan terbuka (V11 bagian 3(i) baris 122 dan bagian 3(iii) baris 163 sampai 184).
8. Sembilan cacat audit ditutup, dengan dua klaim yang saya uji ulang cocok: D1 di baris ledger 2182 dan D4 dengan sisa nol sel bergaya ribuan.

### 4.2 Digantikan atau usang

1. Tabel sembilan cacat di `RND_S5_AUDIT_WAVE2.md` bagian 7, digantikan `RND_S5_DEFECT_STATUS.md`.
2. Tabel cacat yang sama di `RND_S6_PM_WAVE2.md` bagian 8 baris 372 sampai 382, sudah tidak sesuai dengan keadaan dan hanya dinetralkan oleh catatan di baris 398.
3. Vonis kesiapan di `V10_PM2_VERDICT.md` bagian 5, digantikan vonis V11 beserta sembilan syarat perbaikan.
4. Kolom "Sebelum" pada `RND_ENGINE_S6_INTEGRATION.md` bagian 1, berlaku sebagai riwayat perubahan, bukan keadaan sekarang.
5. Log patch P1 sampai P5 pada `V10_PM2_VERDICT.md` bagian 3, berlaku sebagai riwayat tertutup, bukan daftar pekerjaan.
6. Tabel ukuran berkas pada `RND_S5_AUDIT_WAVE2.md` bagian 1, tidak lagi cocok dengan disk (lihat bagian 7).

---

## 5. Daftar fitur

Definisi status bukti yang dipakai di sini:

- TERUKUR berarti angka pendukungnya ada di dokumen sumber dengan nomor baris dan sudah diperiksa kartu ini.
- SEBAGIAN berarti sebagian komponen terukur dan sebagian belum.
- BELUM berarti tidak ada angka pendukung, dan fitur masih berupa rancangan.
- HIPOTESIS berarti ada angka pendukung tetapi bentuk keluarannya belum diuji.

Empat belas fitur di bawah semuanya menempatkan manusia sebagai pemutus. Tidak ada satu pun yang mengusulkan alarm otomatis.

### F-01 Papan vonis per kelas kerusakan

- Pengguna: insinyur pengeboran dan supervisor shift.
- Momen pakai: sebelum mempercayai badge kelas mana pun, dan saat serah terima shift.
- Masukan: tabel komposisi S6 bagian 3 baris 148 sampai 159, peta tier bagian 3.1, dan JSON engine.
- Keluaran: satu kartu per kelas berisi komposisi berlaku, status lapisan A, B, dan C, kekuatan bukti, serta tiga syarat tier yang masih menggantung.
- Status bukti: TERUKUR, karena seluruh isi kartu berasal dari tabel yang sudah ada.

### F-02 Skor keyakinan 0 sampai 100 per head, bukan lulus atau gagal

- Pengguna: insinyur yang membaca badge.
- Momen pakai: saat badge menyala dan harus diputuskan apakah ditindaklanjuti atau ditunda.
- Masukan: FAR kalender median, jumlah fold yang memenuhi FAR dan recall, `beda_sel` antar seed, dan ketersediaan lapisan B.
- Keluaran: skor bulat dengan tiga komponen terbaca, plus batas atas yang dipotong bila lapisan B kosong, misalnya skor maksimum 70 sampai B terukur.
- Status bukti: SEBAGIAN. Komponen A dan C terukur (S6 bagian 2.1 baris 87 sampai 100), komponen B kosong (S6 bagian 7.1). Bobot antar komponen masih usulan, belum disetujui, jadi skornya sendiri berstatus HIPOTESIS.

### F-03 Sakelar dua titik operasi hyd

- Pengguna: supervisor shift.
- Momen pakai: awal shift, ketika harus dipilih antara cakupan deteksi atau ketenangan alarm.
- Masukan: pilihan mode, lalu dua keluaran engine yang sudah ada.
- Keluaran: tabel pertukaran berdampingan berisi FP, TP, presisi, recall, FAR kalender, lead, dan onset diperingatkan untuk H1p dan H1p3.
- Status bukti: TERUKUR (S6 bagian 4.1 baris 196 dan 197).

### F-04 Badge bersyarat per well

- Pengguna: insinyur yang menerima peringatan hyd.
- Momen pakai: saat peringatan datang dari well tertentu.
- Masukan: cakupan menit per well dari S1 bagian 3 baris 58 sampai 66.
- Keluaran: badge dengan label cakupan dan penanda bersyarat, sehingga klaim peringatan tidak terbaca sebagai klaim seluruh lapangan. Contoh yang harus tercetak: F-10 dengan cakupan 0,673 dan F-5 dengan 0,0171.
- Status bukti: TERUKUR (S6 bagian 5.2 baris 280 dan 281, S1 baris 58 sampai 66).

### F-05 Penaksir beban tinjauan per shift dengan label segmen

- Pengguna: supervisor dan perencana tenaga kerja.
- Momen pakai: perencanaan shift 8 jam.
- Masukan: FAR per 24 jam per head dari `RND_ENGINE_S6_INTEGRATION.md` bagian 2 baris 31 sampai 43.
- Keluaran: jumlah tinjauan per shift per engine, dengan label wajib "angka segmen F-14, bukan median lintas fold". Contoh: hyd rule 19 tinjauan, hyd hybrid 6, vib 17, shk 3, stuck 3, tool_wear 1.
- Status bukti: SEBAGIAN. Angka ada, tetapi batas segmennya diakui dokumen sumber (bagian 5 butir 3 baris 67), sehingga angkanya tidak boleh dipakai sebagai beban seluruh armada.

### F-06 Dynamic Island lapisan B: slot nilai yang jujur

- Pengguna: perencana maintenance dan manajer operasi.
- Momen pakai: ketika muncul pertanyaan berapa nilai uang dari peringatan ini.
- Masukan: jam henti dari DDR (S4 bagian 3.1 baris 63 sampai 78), lead peringatan, dan daftar penyebut yang kosong (S4 bagian 6 baris 165 sampai 173).
- Keluaran: panel tiga tingkat. Tingkat pertama nilai waktu terukur: 1777,75 jam pada 1116 kejadian repair dan maintain, median 1,0 jam, p90 3,5 jam. Tingkat kedua rasio: lead 11,5 menit setara 19,17 persen durasi henti median. Tingkat ketiga slot kosong berlabel, berisi lima kebutuhan beserta pemiliknya, yaitu biaya henti, work order, jadwal inspeksi, produksi tertunda, dan hasil uji integritas.
- Status bukti: TERUKUR untuk dua tingkat pertama (S4 bagian 4 baris 121 sampai 131), BELUM untuk rupiah (S4 bagian 3.3 baris 105).

### F-07 Pengunci satuan FAR

- Pengguna: siapa pun yang membaca atau mengutip angka FAR.
- Momen pakai: setiap kali FAR ditampilkan, dihitung, atau dibandingkan.
- Masukan: FAR dua satuan per fold.
- Keluaran: dua angka berdampingan dengan label satuan yang tidak dapat dimatikan. Contoh yang harus muncul: 7 dari 9 fold lulus pada satuan kalender, 0 dari 9 lulus pada satuan baris, rasio median kedua satuan 9,1372.
- Status bukti: TERUKUR (S1 bagian 6.1 baris 162, S6 bagian 2.1 kolom FAR baris 94 dan 95).

### F-08 Register kegagalan peralatan sebagai panel konteks

- Pengguna: maintenance engineer.
- Momen pakai: investigasi kegagalan berulang pada satu kelas sistem peralatan.
- Masukan: 533 record tabel `equipmentfailureInfoTable` dari 325 laporan.
- Keluaran: register per kelas sistem (41 kelas unik) berisi tanggal, kedalaman, dan deskripsi, dengan penanda tegas bahwa kolom downtime bernilai nol pada 533 dari 533 record sehingga panel ini tidak boleh dipakai sebagai sumber durasi.
- Status bukti: TERUKUR untuk register (S4 bagian 3.2 baris 89), BELUM untuk durasi.

### F-09 Kartu transparansi label bit_wear

- Pengguna: reviewer, dosen pembimbing, dan insinyur yang membaca tren bit_wear.
- Momen pakai: saat tren bit_wear dibuka atau dikutip.
- Masukan: hasil rekonstruksi label dan diagnostik sirkularitas.
- Keluaran: banner yang menyatakan label `high_MSE_bit_wear` adalah indeks mekanika, bukan observasi keausan, dengan dua angka pendukung: rekonstruksi 198928 dari 198928 baris atau akurasi 1,000000, dan perbandingan presisi 0,8496 pada ML yang memakai `MSE` serta `ROC_coef` lawan recall 0,9968 pada ML kanal fisik saja.
- Status bukti: TERUKUR (S3 bagian 2.5 baris 100 sampai 104, bagian 5 butir 4 baris 187).

### F-10 Kartu permintaan identitas bit

- Pengguna: pemilik data dan tim aset.
- Momen pakai: saat menyiapkan data baru atau audit kesiapan data.
- Masukan: hasil pemindaian token pada 18 kolom USROP, yaitu 0 kolom identitas bit, 0 kolom run, 3 nilai unik pada `Diameter mm`, dan 145887 duplikat pada `Unnamed: 0`.
- Keluaran: daftar empat field yang dibutuhkan, yaitu nomor bit, tanggal pasang dan lepas, biaya bit, dan jam henti per bit, disertai analisis yang terbuka bila field itu ada: leave-one-bit-out, kurva keausan per bit terhadap meter tergali, kalibrasi ambang per bit, dan biaya per meter per bit.
- Status bukti: TERUKUR untuk ketiadaan (S3 bagian 2.2 baris 58 sampai 66), BELUM untuk analisis lanjutan (S3 bagian 8 butir 3 baris 206).

### F-11 Panel audit ulang dengan kontrol negatif (dari dokumen yang sudah digantikan)

- Pengguna: auditor internal.
- Momen pakai: sebelum menerbitkan vonis baru atau mengubah angka pada dokumen yang sudah terbit.
- Masukan: dokumen lama, dua mutasi angka yang disengaja (`fp_total` 935 menjadi 936, presisi median 0,7789 menjadi 0,7791), dan toleransi 5e-5.
- Keluaran: status lulus atau gagal pengunci, dengan tiga angka: 143 sel diperiksa, 0 selisih pada dokumen asli, 2 selisih pada dokumen termutasi.
- Status bukti: TERUKUR (S5 bagian 2.3 baris 65, bagian 2.4 baris 71). Dokumen sumbernya berstatus DIGANTIKAN untuk fungsi register cacat, tetapi desain tesnya tetap satu satunya bukti di repo bahwa pengunci dapat gagal, dan justru karena dokumennya usang, desain itu tidak akan terbawa ke dokumen baru kalau tidak diangkat menjadi fitur.

### F-12 Log provenance patch (dari dokumen yang sudah digantikan)

- Pengguna: pemilik dokumen dan pembaca yang menemukan dua angka berbeda untuk klaim yang sama.
- Momen pakai: saat terjadi pertentangan angka antar dokumen.
- Masukan: daftar temuan penyajian P1 sampai P5 beserta berkas dan baris sasaran.
- Keluaran: satu baris per patch berisi id, berkas yang diubah, baris, status, dan bukti sesudah patch. Temuan P5 dicetak khusus sebagai "bukan kontradiksi" dengan alasannya, yaitu 5 dari 7 fold dapat diskor sama dengan 7 fold dikurangi 2 fold tanpa positif.
- Status bukti: TERUKUR untuk P1 sampai P4 (V10 bagian 3 baris 54 sampai 60), dan P5 tercatat sebagai bukan cacat (V10 bagian 4 baris 70). Dokumen sumbernya DIGANTIKAN, sehingga log ini hanya dapat diselamatkan dengan cara dijadikan fitur.

### F-13 Prasaring komposisi DAN

- Pengguna: analis model.
- Momen pakai: sebelum mengusulkan komposisi DAN baru pada kelas apa pun.
- Masukan: laju alarm tiap komponen pada anggaran yang sama.
- Keluaran: keputusan tolak atau lanjut, dengan angka pendukung bahwa 7 dari 18 penolakan di gelombang 1 dan 2 adalah kegagalan bentuk DAN, dan mekanismenya saturasi ambang pada nilai tertinggi grid (hyd 8 dari 13 fold, bit_wear 7 dari 7 fold, ssi recall 0,0000, vib recall 0,1426).
- Status bukti: TERUKUR (S6 bagian 6.1 baris 312 sampai 320).

### F-14 Panel "tidak ada pemenang"

- Pengguna: insinyur yang membandingkan komposisi untuk vib dan ssi.
- Momen pakai: saat memilih komposisi untuk dua kelas yang tidak punya pemenang.
- Masukan: recall median seluruh komposisi pada dua kelas itu.
- Keluaran: panel eksplisit bahwa tidak ada komposisi yang mencapai recall 0,5, dengan angka vib 0 dari 4 fold dan ssi 1 TP dari 132 onset, disertai kalimat bahwa memilih yang terbaik di antara yang gagal bukan pilihan yang lebih baik.
- Status bukti: TERUKUR (S6 bagian 3.2 baris 171 sampai 174, bagian 4.3 baris 231 dan 232).

Ringkasan fitur:

| Fitur | Sumber utama | Status bukti | Memakai dokumen usang |
|---|---|---|---|
| F-01 Papan vonis | S6 bagian 3 | TERUKUR | tidak |
| F-02 Skor keyakinan | S6 bagian 2.1 dan 7.1 | SEBAGIAN | tidak |
| F-03 Sakelar dua mode | S6 bagian 4.1 | TERUKUR | tidak |
| F-04 Badge per well | S6 bagian 5.2, S1 bagian 3 | TERUKUR | tidak |
| F-05 Beban tinjauan | ENGINE bagian 2 | SEBAGIAN | tidak |
| F-06 Dynamic Island lapisan B | S4 bagian 3.1, 4, 6 | TERUKUR dan BELUM | tidak |
| F-07 Pengunci satuan FAR | S1 bagian 6.1 | TERUKUR | tidak |
| F-08 Register kegagalan | S4 bagian 3.2 | TERUKUR dan BELUM | tidak |
| F-09 Transparansi label bit_wear | S3 bagian 2.5 dan 5 | TERUKUR | tidak |
| F-10 Permintaan identitas bit | S3 bagian 2.2 | TERUKUR dan BELUM | tidak |
| F-11 Audit ulang kontrol negatif | S5 bagian 2.3 dan 2.4 | TERUKUR | ya, S5_AUDIT DIGANTIKAN |
| F-12 Log provenance patch | V10 bagian 3 dan 4 | TERUKUR | ya, V10_PM2 DIGANTIKAN |
| F-13 Prasaring komposisi DAN | S6 bagian 6.1 | TERUKUR | tidak |
| F-14 Panel tanpa pemenang | S6 bagian 3.2 dan 4.3 | TERUKUR | tidak |

---

## 6. Dokumen usang yang diselamatkan

Dua dokumen berstatus DIGANTIKAN, dan keduanya menyumbang satu fitur yang tidak ada di dokumen penggantinya.

Pertama, `RND_S5_AUDIT_WAVE2.md`. Yang diambil bukan daftar cacatnya, karena daftar itu sudah ditutup, melainkan desain tesnya: 143 sel dibandingkan sel per sel dengan toleransi 5e-5, lalu dua angka dimutasi dan pengunci diuji apakah benar benar gagal. Dokumen pengganti, `RND_S5_DEFECT_STATUS.md`, hanya mencatat status akhir dan tidak membawa desain tes itu. Tanpa diangkat menjadi F-11, satu satunya bukti bahwa pengunci dapat gagal akan berhenti sebagai arsip.

Kedua, `V10_PM2_VERDICT.md`. Yang diambil bukan klausa kesiapannya, karena klausa itu sudah digantikan V11, melainkan disiplin pencatatan patch: lima temuan penyajian, tiap temuan punya berkas, baris, dan bukti sesudah patch, ditambah satu temuan yang dicatat sebagai bukan cacat beserta alasannya. Disiplin itu menjadi F-12.

Satu segmen usang lain juga diselamatkan, meskipun dokumennya tetap berlaku: tabel sembilan cacat di S6 bagian 8. Isinya sudah tidak benar, tetapi tabel itu menunjukkan pola yang berguna, yaitu cacat dilaporkan dengan bukti perintah yang dapat diulang. Pola itu masuk ke F-11 sebagai syarat keluaran.

---

## 7. Pertentangan antar dokumen yang belum selesai

Empat hal di bawah belum sepakat, dan kartu ini tidak menutupnya dengan taksiran.

| Pertentangan | Bukti | Dampak | Cara menutup |
|---|---|---|---|
| Ukuran berkas di audit S5 lawan ukuran di disk | Audit bagian 1 baris 23 sampai 26 menulis S1 279 baris dan 25445 byte, S2 311 dan 24464, S3 218 dan 21573, S4 207 dan 23162. Disk hari ini: S1 287 dan 26235, S2 317 dan 25135, S3 224 dan 22275, S4 213 dan 23799 | Tabel ukuran pada audit sudah tidak dapat dipakai sebagai rujukan keadaan sekarang. Selisihnya +6 baris untuk S2, S3, dan S4, serta +8 baris untuk S1, dan setiap dokumen sekarang memuat blok "Catatan provenance (revisi 2026-10-29)". Apakah seluruh selisih berasal dari blok itu belum diuji | Jalankan ulang penghitung baris dan byte, lalu terbitkan tabel ukuran baru dengan cap tanggal |
| Fraksi cakupan ledger untuk klaim yang sama | Audit bagian 3.3 baris 185 menulis S1 344 dari 508 sel (0,6772) dan S3 139 dari 339 (0,41). Dokumen status baris 13 dan 17 menulis S1 64 dari 441 sel (14,51 persen) dan S3 74 dari 328 (22,56 persen) | Dua angka untuk klaim yang sama, dengan penyebut berbeda. Pembaca tidak dapat memilih tanpa tahu metode mana yang dipakai | Tetapkan satu metode hitung, lalu jalankan pada kedua dokumen dan terbitkan satu angka per kartu |
| Angka gangguan di dokumen integrasi engine lawan tabel S4 | `RND_ENGINE_S6_INTEGRATION.md` baris 25 sampai 27 menulis equipment failure 2739.667 jam, stuck equipment 212.0 jam, circulation loss 195.0 jam. Tabel S4 baris 67 sampai 76 tidak memuat kode equipment failure maupun stuck equipment, dan menulis lost circulation 160,75 jam pada 75 record. Pencarian `2739`, `212.0`, dan `195.0` pada S4 memberi nol kemunculan | Selisih 34,25 jam pada satu kategori, dan dua kategori tanpa padanan. Bila angka integrasi dipakai untuk panel nilai maintenance, sumbernya belum terlacak | Jalankan agregasi ulang dari `ddr.parquet`, sebutkan kolom pengelompoknya (`proprietaryCode` atau `stateDetailActivity`), lalu terbitkan satu tabel |
| S6 bagian 8 lawan catatan baris 398 | Baris 372 sampai 382 menulis sembilan cacat "belum diperbaiki" dengan bukti grep hari itu. Baris 398 menulis cacat sudah ditangani dan menunjuk dokumen status | Isi satu dokumen bertentangan dengan dirinya sendiri. Pembaca yang berhenti di bagian 8 akan menyimpulkan kebalikannya | Sunting badan bagian 8 agar menunjuk dokumen status, atau pindahkan tabelnya ke lampiran bersejarah dengan cap tanggal |

Satu hal yang tidak saya masukkan sebagai pertentangan, tetapi perlu dicatat sebagai jebakan baca: `V10_PM2_VERDICT.md` baris 13 memuat dua rekap berbeda dalam satu kalimat, yaitu rekap tier 0+3+2+2=7 dan rekap head 12/13/2. Keduanya sah karena objeknya berbeda, tier per engine lawan tier per head, tetapi pembaca cepat akan menyebutnya kontradiksi. F-01 dan F-12 sebaiknya mencetak nama objeknya, bukan hanya angkanya.

---

## 8. Syarat yang dibutuhkan agar yang belum terukur menjadi terukur

Bagian ini menggantikan penutup jenis daftar kekurangan. Setiap butir menyebut apa yang dibutuhkan, dari siapa, dan apa yang terbuka setelahnya.

1. Kolom biaya henti. Dibutuhkan tarif rig harian atau biaya per operasi per hari beserta tanggal berlaku, dari bagian kontrak dan akuntansi operasi pengeboran (S4 bagian 6 baris 167). Setelah ada, 1777,75 jam maintenance dapat dikonversi menjadi nilai uang, dan F-06 naik dari dua tingkat menjadi tiga tingkat penuh.
2. Nomor work order. Dibutuhkan nomor WO, tanggal buka dan tutup, komponen, vendor, dan jam teknisi, dari sistem CMMS pemeliharaan rig (S4 bagian 6 baris 168). Setelah ada, klaim bahwa peringatan mendahului pembukaan WO dapat diuji, bukan hanya mendahului onset sensor.
3. Jadwal dan realisasi inspeksi. Dibutuhkan tanggal rencana, tanggal realisasi, durasi, temuan, dan jam orang, dari pengawas rig dan departemen pemeliharaan (S4 bagian 6 baris 169). Setelah ada, syarat lapisan B yang menahan kenaikan tier dapat diukur, karena penahannya sekarang adalah ketiadaan berkas jadwal, bukan mutu deteksi (S6 bagian 7.1 baris 356 dan 357).
4. Identitas bit. Dibutuhkan nomor bit, tanggal pasang dan lepas, biaya bit, dan jam henti per bit (S3 bagian 8 butir 3 baris 206). Setelah ada, F-10 berubah dari kartu permintaan menjadi kurva keausan per bit.
5. Kanal aliran untuk hyd K-ii. Dibutuhkan keluaran kanal aliran, karena hyd K-ii sekarang berstatus BELUM LAYAK PAKAI dengan 78,7 persen jendela berbalik tanda pada satu split temporal (S6 bagian 5 baris 265).
6. Seed ketiga sampai kelima untuk S6. Hasil S6 baru pada dua seed, 42 dan 13 (S6 bagian 9.1 butir 1 baris 416). Komposisi yang diuji deterministik dan kontrol negatif sudah membuktikan harness peka seed, sehingga penambahan seed menutup satu satunya bagian kestabilan yang belum diuji.
7. Reproduksi S2, S3, dan S4. Ketiganya belum dijalankan ulang, yang diperiksa baru artefak dan ledger (S6 bagian 9.1 butir 4 baris 422). Setelah dijalankan ulang, vonis atas ketiga kartu itu naik dari vonis atas angka yang dilaporkan menjadi vonis atas angka yang dibangkitkan ulang.
8. Persetujuan user atas perubahan komposisi hyd. Perubahan H1 ke H1p diusulkan S6 dan belum diterapkan ke engine mana pun (S6 bagian 9.1 butir 10 baris 432). Tanpa persetujuan itu, F-03 tidak dapat menampilkan dua mode sebagai keadaan engine.
9. Sembilan perbaikan pemenang proposal. V11 bagian 3(iii) baris 163 sampai 184 mendaftarnya, termasuk klaim `stuck_k2` yang gagal direproduksi dan angka baris 628 yang salah. Selama sembilan butir itu terbuka, klausa kesiapan V10 belum dapat dipakai.

---

## 9. Kontrak kejujuran

Berkas yang dibuka dan ukurannya: `RND_S6_PM_WAVE2.md` 40271 byte 437 baris, `RND_S5_AUDIT_WAVE2.md` 27190 byte 292 baris, `RND_S5_DEFECT_STATUS.md` 3418 byte 57 baris, `RND_ENGINE_S6_INTEGRATION.md` 3915 byte 76 baris, `RND_S2_HYBRID_VIB_SSI.md` 25135 byte 317 baris, `RND_S3_HYBRID_BITWEAR.md` 22275 byte 224 baris, `RND_S4_LAYER_B_DATA.md` 23799 byte 213 baris, `V10_PM2_VERDICT.md` 8545 byte 87 baris, `V11_PM_FINAL.md` 20660 byte 288 baris, ditambah `RND_S1_SEED_ROBUSTNESS.md` 26235 byte 287 baris. Total 201443 byte dan 2278 baris.

Yang belum diverifikasi oleh kartu ini:

1. Tidak ada harness atau engine yang dijalankan. Seluruh angka dikutip dari dokumen dengan nomor baris.
2. `scratch/rnd/s6/s6_kandidat.json` tidak dibuka. Jumlah fold yang memenuhi FAR dan recall sekaligus adalah hitungan penulis S6 atas berkas itu, dan S6 sendiri menyatakan hal tersebut di bagian 9.1 butir 2 baris 418.
3. Rekonsiliasi angka gangguan antara dokumen integrasi engine dan tabel S4 belum dilakukan, dan penyebabnya belum diketahui (bagian 7).
4. Dua metode hitung cakupan ledger, 344 dari 508 lawan 64 dari 441, belum disatukan (bagian 7).
5. Cacat D2, D3, dan D9 tidak diuji ulang karena hitung ulangnya memerlukan eksekusi kode baru, sama seperti yang dinyatakan S6 bagian 9.1 butir 5 baris 423.
6. Status sembilan perbaikan pemenang proposal tidak dapat diperiksa karena tidak ada dokumen sesudah V11.
7. Model pada S2, S3, dan S4 tidak dijalankan ulang, sehingga vonis atas ketiganya adalah vonis atas angka yang dilaporkan.
8. Bobot skor keyakinan pada F-02 adalah usulan kartu ini, bukan angka yang sudah disetujui.
9. Artefak JSON pada `scratch/rnd/s1` sampai `s6` dan `scratch/v11` tidak dibuka kartu ini.

Jumlah tanda pisah panjang pada dokumen ini: 0.
