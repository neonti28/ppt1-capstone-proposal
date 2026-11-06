# RND-S4: PENDATAAN LAPISAN B (INSPEKSI, WORK ORDER, JAM HENTI, BIAYA)

Kartu: `t_ad4e3f55` · Board: `rnd-algo-2026` · Tanggal: 2026-10-28 (WIB)
Workspace: `/mnt/d/Capstone 1(v2)`
Kebijakan pengikat: `docs/RND_EVALUATION_POLICY.md` (tiga lapisan A/B/C, tanpa gate biner, engine boleh berbeda antar kelas kerusakan)
Artefak mentah: `scratch/rnd/s4/inventory.json`, `ddr_activity_stats.json`, `labels_duration.json`, `inventory_raw.json`, `ddr_downtime_table.json`, `ddr_downtime_records.jsonl`, `crosscheck.json`, `token_scan.json`
Skrip: `scratch/rnd/s4/s4a_ddr_activity.py`, `s4b_labels_duration.py`, `s4c_inventory.py`, `s4d_downtime_table.py`, `s4e_crosscheck.py`, `s4f_merge.py`, `s4i_token_scan.py`

Riset pendahuluan: exploratory-data-analysis (dipakai untuk kerangka kerja terbatas dan lokal: setiap berkas dibaca read-only, ukuran dan jumlah baris dihitung, tidak ada penulisan ulang data mentah, dan setiap laporan menyebut cakupan yang dipindai beserta batasannya; prinsip "not detected bukan tidak ada" dipakai saat menyimpulkan ketiadaan biaya dan work order), verification-mandatory (setiap angka diambil dari eksekusi nyata lalu di-assert di `s4f_merge.py` terhadap JSON sumbernya, sehingga dokumen tidak bisa menyimpang dari bukti; klaim ketiadaan dibuktikan dengan hitungan token, bukan dengan ingatan dokumen lama), scientific-critical-thinking (memisahkan tiga hal yang sebelumnya tercampur di dokumen R7/R8/E3/E4/PM: jam henti, biaya, dan jadwal inspeksi; pembingkaian lama "nilai maintenance belum terukur" diuji ulang lalu dipersempit menjadi "biaya, work order, jadwal inspeksi, dan jam henti terhindar belum terukur").

Riset pendahuluan: sequentialthinking, 4 pikiran (`mcp__sequentialthinking__sequentialthinking`, thoughtNumber 1..4, thoughtHistoryLength 4). Ringkas: (1) klaim lama "data lapisan B tidak ada" diperlakukan sebagai hipotesis yang harus diuji dengan enumerasi, bukan diwarisi; (2) kandidat terkuat adalah record activity DDR karena membawa waktu mulai dan selesai per pekerjaan, dan tabel equipment failure pada DDR versi HTML; (3) pemisahan tiga skrip agar kegagalan satu jalur tidak menghapus bukti lain, termasuk pencatatan pemasangan pyarrow ke venv `rnd_e3` sebagai langkah nyata; (4) pengelompokan akhir tiga tingkat dan pembatasan metrik hanya pada yang penyebutnya benar-benar ada.

---

### Catatan provenance (revisi 2026-10-29)

Cakupan ledger terukur pada dokumen ini: 27 dari 91 sel angka tabel (29.67 persen) punya padanan nilai pada blok `S4-` di `docs/RND_PROVENANCE_LEDGER.md`. Sel yang tidak punya padanan adalah agregat turunan antar fold atau antar berkas, dan tidak diklaim punya baris tersendiri.

Rujukan metode: konstanta metode di dokumen ini adalah konvensi internal repo dengan jejak berkas dan baris. Satu-satunya standar eksternal yang dipakai adalah ISO 2041:2018 §3.1.4 untuk nilai g, tercatat pada baris ledger L-01. Dokumen ini tidak mengklaim DOI luar, jadi butir audit DOI tidak berlaku di sini.

## 1. CARA SAPUAN DILAKUKAN

Sapuan tidak memakai ingatan dokumen lama. Urutannya:

1. Enumerasi folder `data/volve/external/dbx_volume/Well_technical_data`: 5.473 berkas, 409.920.771 byte, 11 subfolder (`S4-028`).
2. Hitung dokumen DDR per format: 1.759 HTML (30.971.159 byte), 1.759 XML (21.315.879 byte), 1.759 PDF (56.814.977 byte) (`S4-041`).
3. Baca `data/volve/ddr.parquet` dengan pyarrow setelah memasang `pyarrow==26.0.0` ke venv `/home/neonti/.venvs/rnd_e3` (venv lama tidak punya pyarrow, dan itu sebab klaim "gagal dibaca" di `docs/RND_D0_DATA_FEASIBILITY.md` baris 398).
4. Pindai seluruh 1.759 XML dan 1.759 HTML untuk token biaya dan work order (17 token literal plus 5 pola regex), terpisah dari pemindaian token downtime dan inspeksi (`S4-070`, `S4-072`).
5. Parse tabel `equipmentfailureInfoTable` dari 1.759 HTML memakai BeautifulSoup, lalu simpan 533 record mentah ke JSONL.
6. Pindai header 53 berkas CSV/TSV di `data/` untuk kolom bernuansa biaya, inspeksi, work order, dan durasi (`S4-030`). Tujuh di antaranya berasal dari `witsml_parsed`, dan tiga berkas `witsml_parsed` (F-12, F-14, F-15_S) dilewati karena melewati batas ukuran 500 MB (`S4-068`). Hanya satu berkas yang punya kata kunci header, yaitu `USROP_health.csv` dengan kolom `maintenance_recommendation`, dan kolom itu turunan sendiri dari `code/06_xgb_fuzzy.py:90`, bukan catatan maintenance nyata.
7. Uji silang jam henti dari dua jalur berbeda: record activity DDR lawan label terkurasi.

Poin 4 adalah pembeda penting: ketiadaan biaya dan work order di sini adalah hasil hitungan token pada 3.518 dokumen, bukan kesan dari membaca beberapa berkas.

---

## 2. KANDIDAT YANG DITEMUKAN (path absolut, ukuran, jumlah record, kolom relevan)

| No | Path absolut | Ukuran | Jumlah baris/record | Kolom relevan |
|---|---|---|---|---|
| 1 | `/mnt/d/Capstone 1(v2)/data/volve/ddr.parquet` | 2.180.278 byte | 1.759 laporan, 17 kolom, 23.447 record `activity` (`S4-001`, `S4-003`, `S4-004`) | `activity.dTimStart`, `activity.dTimEnd`, `activity.proprietaryCode`, `activity.state`, `activity.stateDetailActivity`, `activity.comments` |
| 2 | `/mnt/d/Capstone 1(v2)/data/volve/labels_curated_v2.csv` | 519.171 byte | 884 record, 20 kolom (`S4-013`) | `act_start`, `act_end`, `category`, `state_detail`, `source_code`, `outcome`, `component` |
| 3 | `/mnt/d/Capstone 1(v2)/data/volve/external/dbx_volume/Well_technical_data/Daily Drilling Report - HTML Version/*.html` | 1.759 berkas, 30.971.159 byte | 325 berkas memuat tabel `equipmentfailureInfoTable`, 533 record (`S4-020`, `S4-021`) | Start time, Depth mMD, Depth mTVD, Sub Equip - Syst Class, Operation Downtime (min), Equipment Repaired, Remark |
| 4 | `/mnt/d/Capstone 1(v2)/data/volve/external/dbx_volume/Well_technical_data/Daily Drilling Report - XML Version/*.xml` | 1.759 berkas, 21.315.879 byte | 1.759 dokumen | struktur WITSML drillReport: `activity`, `statusInfo`, `fluid`, `lithShowInfo` (tanpa elemen biaya) |
| 5 | `/mnt/d/Capstone 1(v2)/data/volve/external/dbx_volume/Well_technical_data/Daily Drilling report - PDF Version/*.pdf` | 1.759 berkas, 56.814.977 byte | 1.759 dokumen | tidak dipindai teks pada kartu ini |
| 6 | `/mnt/d/Capstone 1(v2)/data/volve/external/volve_catalog_target_paths.csv` | 645.763 byte | 4.035 record data, 4.036 baris teks termasuk header (`S4-029`) | `category`, `well`, `ext`, `path` |
| 7 | `/mnt/d/Capstone 1(v2)/data/predictive/features_timeseries_events.csv` | 85.613 byte | 661 record, 17 kolom | `event_id`, `fold`, `wellbore`, `act_start`, jendela `w30m/w2h/w6h` |
| 8 | `/mnt/d/Capstone 1(v2)/data/USROP_health.csv` | 56.815.359 byte | 198.928 record, 20 kolom | `health_index`, `maintenance_recommendation` (turunan sendiri, `code/06_xgb_fuzzy.py:90`, bukan catatan maintenance nyata) |
| 9 | `/mnt/d/Capstone 1(v2)/data/volve/usrop_wellbores_events.csv` | 218.119 byte | 884 record, 8 kolom | `wellbore`, `ddr_date_start`, `act_start`, `act_end`, `code`, `state_detail`, `comments` |
| 10 | `/mnt/d/Capstone 1(v2)/data/volve/witsml_parsed/*.csv` | 10 berkas, 4.606.027.369 byte total | kanal realtime per sumur | tidak memuat kolom maintenance, biaya, atau inspeksi |

Catatan metode: `ddr.parquet` adalah versi datar dari 1.759 DDR. Kolom `activity` berisi array objek (bukan list Python), sehingga pembacaan pertama dengan `isinstance(x, list)` memberi 0 record. Kesalahan itu ditemukan lewat uji pembeda (kolom `activity` dilaporkan `rows_nonempty=0` padahal contoh baris menunjukkan isi), lalu diperbaiki dengan menangani `numpy.ndarray`. Angka 23.447 berasal dari versi yang sudah diperbaiki.

Catatan metode kedua: jumlah baris teks tidak dipakai sebagai jumlah record. `wc -l` memberi 1.413 pada `labels_curated_v2.csv` dan 1.190 pada `usrop_wellbores_events.csv`, sedangkan jumlah record sebenarnya 884 pada keduanya, karena kolom komentar memuat baris baru di dalam tanda kutip. Semua angka record di dokumen ini diambil dari `pandas.read_csv` (hasil `scratch/rnd/s4/p_rows.py`), bukan dari `wc -l`.

---

## 3. TIGA KELOMPOK

### 3.1 Tersedia dan bisa dipakai

**S4-C1. Record activity DDR sebagai register pekerjaan dan henti.**
Path `data/volve/ddr.parquet`. 23.447 record pada 1.750 dari 1.759 laporan (`S4-004`, `S4-006`), 64 kode kerja unik (`S4-005`). Setiap record punya `dTimStart` dan `dTimEnd`, sehingga durasi dapat dihitung langsung. Total jam seluruh activity 39.397,986 jam (`S4-012`). Rincian kode interruption:

| Kode | Record | Jam | Median jam | p90 jam | Maks jam |
|---|---:|---:|---:|---:|---:|
| interruption -- other | 1.202 | 2.680,917 | 1,0 | 5,5 | 24,0 |
| interruption -- waiting on weather | 445 | 1.925,5 | 2,5 | 10,9 | 24,0 |
| interruption -- repair | 806 | 1.215,0 | 1,0 | 3,5 | 12,5 |
| interruption -- sidetrack | 202 | 590,0 | 1,5 | 6,0 | 18,0 |
| interruption -- fish | 246 | 568,333 | 1,5 | 5,0 | 16,0 |
| interruption -- maintain | 310 | 562,75 | 1,0 | 4,5 | 15,0 |
| interruption -- wait | 229 | 522,003 | 1,333 | 5,75 | 20,0 |
| interruption -- lost circulation | 75 | 160,75 | 2,0 | 4,3 | 7,0 |
| interruption -- rig up/down | 33 | 62,25 | 1,25 | 4,3 | 6,0 |
| interruption -- well control | 29 | 55,75 | 1,75 | 3,05 | 5,75 |

Total interruption 3.577 record dan 8.343,253 jam (`S4-007`). Dua kode yang termasuk kerja maintenance, `repair` dan `maintain`, berjumlah 1.116 record dan 1.777,75 jam (`S4-008`, `S4-009`, `S4-010`). Record dengan `state = fail` berjumlah 480 dengan 1.265,5 jam dan median 2,0 jam (`S4-011`).

**S4-C2. Label kejadian terkurasi dengan waktu mulai dan selesai.**
Path `data/volve/labels_curated_v2.csv`. 884 kejadian, seluruhnya punya durasi valid (0 durasi nol, 0 durasi negatif, `S4-015`), total 1.225,0 jam, median 0,75 jam, p90 3,0 jam, maksimum 13,0 jam (`S4-013`, `S4-014`). Untuk 7 well yang dipakai engine: 671 kejadian dan 927,0 jam (`S4-016`). Subset `state_detail = equipment failure`: 770 kejadian, 1.071,5 jam (`S4-017`). Subset kegagalan beralasan (`category` selain `routine_no_failure_evidence`): 388 kejadian, 623,917 jam (`S4-018`).

**S4-C3. Taksonomi kode kerja DDR sebagai pengganti kode work order.**
64 kode (`S4-005`), dengan 10 kode interruption di atas. Ini bukan nomor work order, tetapi memberi kelas pekerjaan yang dapat dipakai sebagai penyebut dan pembilang beban maintenance.

### 3.2 Ada tetapi tidak memadai

**S4-P1. Tabel equipment failure pada DDR versi HTML.**
Ada pada 325 dari 1.759 laporan (18,48 persen), 533 record (`S4-020`, `S4-021`). Kolomnya menjanjikan: kelas sistem peralatan, kedalaman, downtime menit, peralatan yang diperbaiki, remark. Kenyataannya kolom `Operation Downtime (min)` bernilai 0 pada 533 dari 533 record, dan `Equipment Repaired` bernilai `00:00` pada 533 dari 533 record. Hanya 26 dari 533 remark memuat durasi dalam teks dengan pola `(\d+[.,]?\d*)\s*(hrs?|hours?|h|min|minutes?)`, dan angkanya turun menjadi 20 bila pola hanya menerima jam (`S4-022`). Jadi tabel ini register kegagalan independen (41 kelas sistem unik, tanggal, kedalaman, deskripsi), bukan sumber jam henti.

**S4-P2. Ringkasan dan prakiraan 24 jam per laporan.**
`statusInfo.sum24Hr` dan `forecast24Hr` berisi teks bebas. Berguna sebagai konteks, tidak terstruktur, tidak memuat kuantifikasi jam henti atau biaya.

**S4-P3. Jenis uji integritas sumur.**
1.212 laporan memuat `presTestType`: formation integrity test 1.072, leak off test 140 (`S4-025`). Ini catatan uji berjenis, tetapi tanpa tanggal uji terpisah, tanpa hasil lolos/gagal, dan bukan inspeksi peralatan.

**S4-P4. Versi PDF dan XML dari DDR.**
1.759 berkas per format (`S4-041`). Isi terstrukturnya sama dengan parquet. PDF tidak dipindai teks pada kartu ini, sehingga klaim ketiadaan biaya untuk PDF tidak dibuat (lihat bagian 7).

**S4-P5. Katalog target unduhan Volve.**
4.035 record data, 4.036 baris teks termasuk header (`S4-029`), kategori: other_target 3.123, dlis_target 468, las_target 253, bhaRun 175, mudLog 16. Tidak ada kategori laporan inspeksi, work order, atau biaya.

### 3.3 Tidak ada

**S4-N1. Biaya.** Pemindaian penuh 1.759 XML dan 1.759 HTML untuk token biaya memberi 0 kemunculan `cost`, 0 `daycost`, 0 `day cost`, 0 `invoice`, 0 `budget`, 0 `usd`, 0 `nok`, dan 0 `tariff` (`S4-023`, `S4-070`). Satu-satunya kemunculan kata berakar `pric` adalah nama kapal "Ocean Price" pada `15_9_F_15_D_2013_11_12` di kolom komentar, bukan nilai biaya (`S4-071`). Tidak ada kolom biaya di 17 kolom parquet.

**S4-N2. Work order bernomor.** Token `work order`, `workorder`, `work-order`, `service order`, dan `purchase order` 0 kemunculan pada 1.759 XML dan 0 pada 1.759 HTML, dan pola nomor `WO-<angka>` juga 0 (`S4-024`, `S4-072`).

**S4-N3. Jadwal inspeksi fisik dan jam orang.** Tidak ada kode activity yang mengandung `inspect` (0 dari 23.447 record, `S4-026`). Kata `inspect` hanya muncul 630 kali di teks bebas dari 1.759 laporan, dan 154 di antaranya adalah bentuk `inspection` (`S4-027`). Tidak ada field jadwal, tidak ada durasi inspeksi.

**S4-N4. Produksi tertunda dan nilai rupiah.** Pencarian nama berkas production, onstream, barrel, dan oil rate di workspace memberi 0 hasil. Tidak ada data produksi di repo ini.

**S4-N5. Durasi henti terstruktur per kegagalan peralatan.** Kolom downtime nol pada 533 dari 533 record (`S4-021`).

---

## 4. METRIK LAPISAN B YANG BENAR-BENAR DAPAT DIHITUNG

Semua angka di bawah berasal dari `scratch/rnd/s4/inventory.json` bagian `metrik_lapisan_b`, yang di-assert di `s4f_merge.py` terhadap JSON sumbernya.

| Kode | Metrik | Nilai | Penyebut | Arti untuk maintenance |
|---|---|---|---|---|
| B1 | Henti perbaikan per kejadian | 806 kejadian, 1.215,0 jam, median 1,0 jam, p90 3,5 jam, maks 12,5 jam | record `interruption -- repair` | ukuran langsung waktu perbaikan yang bisa dihemat bila peringatan datang sebelum kegagalan |
| B2 | Henti maintenance per kejadian | 310 kejadian, 562,75 jam, median 1,0 jam, p90 4,5 jam, maks 15,0 jam | record `interruption -- maintain` | beban pekerjaan maintenance terjadwal |
| B3 | Beban maintenance gabungan | 1.116 kejadian, 1.777,75 jam, 0,6345 kejadian per laporan harian, 1,0107 jam per laporan harian (`S4-031`, `S4-032`) | 1.759 laporan harian | laju kerja maintenance yang harus dilayani tiap hari rig |
| B4 | Henti kegagalan peralatan berlabel | 770 kejadian, 1.071,5 jam, median 0,75 jam, p90 3,0 jam | label `state_detail = equipment failure` | beban henti yang sudah punya label, siap dipakai sebagai target evaluasi |
| B5 | Laju kejadian berlabel | 0,5026 kejadian per laporan harian (`S4-033`) | 884 kejadian / 1.759 laporan | kepadatan kejadian yang dapat dijadikan target engine |
| B6 | Cakupan jam henti berlabel | 0,1468 (`S4-019`) | 1.225,0 jam label / 8.343,253 jam interruption | 14,68 persen jam henti DDR sudah diberi label, sisanya belum, dan itu batas klaim |
| B7 | Peringatan terhadap durasi henti | lead 11,5 menit H1 = 19,17 persen dari median henti repair 1,0 jam, dan 5,48 persen dari p90 3,5 jam (`S4-034`, `S4-035`) | lead R8/S1 (RUN-KITA) | peringatan datang jauh sebelum perbaikan selesai, tetapi hanya menutup seperlima durasi henti median |
| B8 | Beban alarm per kejadian | H1 2,3974 alarm palsu per onset (935/390), rule 5,3974 (2105/390) (`S4-036`, `S4-037`) | FP dari R8, onset 390 | biaya perhatian per kejadian yang harus dibayar operator |

Yang **tidak dapat** dihitung, dan penyebabnya terukur:

1. **Rasio alarm per inspeksi.** Penyebutnya jadwal inspeksi, dan jadwal itu tidak ada (`S4-N3`: 0 kode `inspect`, 0 field jadwal). Angka 0 di sini bukan hasil ukur, melainkan ketiadaan penyebut.
2. **Pengurangan pemeriksaan fisik.** Butuh jumlah pemeriksaan manual sebelum dan sesudah pemakaian engine. Tidak ada catatan pemeriksaan, sehingga selisihnya tidak dapat dibentuk.
3. **Jam orang yang dihemat.** Butuh durasi inspeksi per alarm. Tidak ada.
4. **Nilai rupiah henti yang dihindari.** Butuh biaya per jam henti. Tidak ada (`S4-N1`).
5. **Barrel tertunda.** Butuh data produksi. Tidak ada (`S4-N4`).

---

## 5. UJI SILANG DUA JALUR JAM HENTI

Dua jalur independen terhadap kanal sensor: record activity DDR (kode interruption) dan label terkurasi. Keduanya tidak independen satu sama lain karena label dibangun dari komentar DDR, sehingga uji ini mengukur kelengkapan label, bukan validitas sensor.

| Wellbore | Record interruption DDR | Jam interruption DDR | Kejadian label | Jam label | Rasio jam |
|---|---:|---:|---:|---:|---:|
| NO 15/9-F-14 | 271 | 448,917 | 182 | 269,0 | 0,5992 |
| NO 15/9-F-15 | 110 | 211,5 | 112 | 216,5 | 1,0236 |
| NO 15/9-F-15 A | 42 | 63,5 | 32 | 41,0 | 0,6457 |
| NO 15/9-F-5 | 120 | 208,503 | 136 | 146,0 | 0,7002 |
| NO 15/9-F-7 | 54 | 71,75 | 59 | 81,5 | 1,1359 |
| NO 15/9-F-9 | 39 | 60,75 | 56 | 85,25 | 1,4033 |
| NO 15/9-F-9 A | 122 | 122,0 | 94 | 87,75 | 0,7193 |
| Total seluruh well | 3.577 | 8.343,253 | 884 | 1.225,0 | 0,1468 |

Rasio di atas 1 pada F-9, F-7, dan F-15 bukan kontradiksi data, dan ini sudah diuji: label tidak hanya berasal dari kode interruption. Distribusi `source_code` label memuat `drilling -- casing` 135 kejadian, `drilling -- trip` 63, `drilling -- drill` 26, dan `plug abandon -- mill` 20. Kejadian berlabel pada kode non-interruption menambah jam di luar kode interruption, sehingga pembilang dapat melampaui penyebut pada well yang kegagalannya banyak tercatat di dalam aktivitas pengeboran. Rasio 1,4033 pada F-9 dilaporkan apa adanya sebagai konsekuensi definisi, bukan dibulatkan menjadi 1.

---

## 6. YANG HARUS DIKUMPULKAN, DAN DARI SIAPA

Bagian ini tidak mengarang bahwa data itu ada. Untuk setiap butir, disebutkan pemilik data yang wajar di lingkungan operasi pengeboran.

| Kebutuhan | Isi persis | Dari siapa | Dipakai untuk |
|---|---|---|---|
| Biaya henti | tarif rig harian (atau biaya per operasi per hari) dengan tanggal berlaku | bagian kontrak dan akuntansi operasi pengeboran | mengubah 1.777,75 jam maintenance menjadi nilai uang |
| Work order | nomor WO, tanggal buka dan tutup, komponen, vendor, jam kerja teknisi | pemeliharaan rig (CMMS) | menguji apakah alarm mendahului pembukaan WO, bukan hanya mendahului onset sensor |
| Jadwal dan realisasi inspeksi | tanggal rencana, tanggal realisasi, durasi, temuan, jam orang | pengawas rig dan departemen pemeliharaan | menghitung rasio alarm per inspeksi dan pengurangan pemeriksaan fisik |
| Produksi tertunda | laju produksi atau barrel per periode, status onstream per hari | bagian produksi (bukan bagian pengeboran) | menghitung barrel tertunda per kejadian henti |
| Hasil uji integritas | tanggal uji, jenis, hasil lolos/gagal, tekanan uji | bagian well integrity | memisahkan uji berjadwal dari kegagalan tak terduga |

Batas yang harus dihormati: tarif rig harian bukan pengganti biaya perbaikan komponen. Memakai tarif harian untuk menghitung biaya henti adalah konvensi yang harus dinyatakan sebagai konvensi, bukan sebagai biaya aktual.

---

## 7. NILAI TIGA LAPISAN SETELAH KARTU INI

**Lapisan A, apakah deteksi bekerja.** Tidak berubah oleh kartu ini. Angka A tetap dari R8 dan S1 (FP, presisi, recall, FAR, lead per engine dan per kelas kerusakan). Kartu ini hanya menambah penyebut baru yang sah, yaitu jumlah kejadian maintenance nyata per laporan harian (0,6345).

**Lapisan B, apakah deteksi memberi nilai maintenance.** Terukur sebagian, dan bagian yang terukur adalah yang selama ini disebut "belum terukur" tanpa pembedaan:

1. Jam henti per kejadian sekarang terukur dari dua jalur: 1.777,75 jam untuk repair dan maintain (1.116 kejadian), dan 1.225,0 jam untuk 884 kejadian berlabel.
2. Waktu perbaikan terukur: median 1,0 jam, p90 3,5 jam, maks 12,5 jam untuk `interruption -- repair`.
3. Perbandingan lead terhadap durasi henti terukur: lead H1 11,5 menit menutup 19,17 persen durasi henti median dan 5,48 persen p90. Artinya peringatan datang di dalam jendela henti, bukan sebelum henti dimulai, untuk mayoritas kejadian.
4. Beban alarm per kejadian terukur: 2,3974 alarm palsu per onset untuk H1, 5,3974 untuk rule kanal.
5. Yang tetap BELUM: pengurangan pemeriksaan fisik, jam orang per shift, rasio alarm per inspeksi, dan nilai rupiah. Penyebabnya bukan kelalaian pengukuran, melainkan tidak adanya penyebut (`S4-N1`, `S4-N3`, `S4-N4`).

**Lapisan C, ketepatan dan ketahanan.** Tidak berubah oleh kartu ini. Kartu ini tidak menguji ulang kestabilan antar periode, antar well, atau antar kondisi operasi. Satu kontribusi untuk lapisan C: register 533 kegagalan peralatan dengan kelas sistem (41 kelas) memberi kemungkinan uji ketahanan per jenis peralatan, tetapi uji itu belum dikerjakan di sini dan tidak diklaim.

**Koreksi terhadap dokumen sebelumnya, dengan kutipan yang sudah diperiksa baris per baris.** Dokumen lama tidak pernah menulis "jam henti tidak ada". Isi baris yang benar: `docs/RND_E3_HASIL.md` baris 217 dan 300, `docs/RND_E4_PERBAIKAN.md` baris 256 dan 343, dan `docs/RND_R7_REVIEW.md` baris 359 menulis "tidak ada data durasi inspeksi per alarm di repo"; `docs/RND_R8_EVALUASI_BERLAPIS.md` baris 148 dan 234 menulis "tidak ada data biaya dan jadwal inspeksi"; `docs/RND_S1_SEED_ROBUSTNESS.md` baris 170 dan 255 menulis nilai rupiah atau jam henti terhindar BELUM TERUKUR karena repo tidak memuat data biaya dan jadwal inspeksi; `docs/RND_PM_VERDICT.md` baris 182, 263, dan 292 menulis gate B wajib diukur dengan data jadwal inspeksi yang belum ada (`S4-069`). Dua belas kutipan itu benar dan tetap benar. Yang dikoreksi adalah pembingkaian "nilai maintenance" sebagai satu blok yang seluruhnya belum terukur: komponen jam henti terukur dari record activity DDR (1.777,75 jam pada 1.116 kejadian) dan dari label (1.225,0 jam pada 884 kejadian). Kalimat yang sah sekarang adalah "biaya, work order, jadwal inspeksi, dan jam henti terhindar belum terukur", bukan "nilai maintenance belum terukur".

---

## 8. RINGKASAN LIMA BARIS

1. Jam henti tersedia dan terukur: 1.777,75 jam pada 1.116 kejadian repair dan maintain, plus 1.225,0 jam pada 884 kejadian berlabel dengan median 0,75 jam.
2. Biaya, work order bernomor, jadwal inspeksi, dan data produksi tidak ada, dibuktikan dengan 0 kemunculan token `cost` dan `work order` pada 3.518 dokumen DDR serta 0 kode activity `inspect`.
3. Tabel equipment failure DDR HTML ada pada 325 laporan dengan 533 record, tetapi kolom downtime nol pada seluruh 533 record, jadi hanya berguna sebagai register kegagalan.
4. Metrik lapisan B yang sah sekarang: jam henti per kejadian, waktu perbaikan, beban maintenance 0,6345 kejadian per laporan harian, lead 19,17 persen dari durasi henti median, dan 2,3974 alarm palsu per onset.
5. Yang tetap belum terukur: rasio alarm per inspeksi, pengurangan pemeriksaan fisik, jam orang, rupiah, dan barrel tertunda, semuanya karena penyebutnya tidak ada di repo.

---

## 9. BELUM TERVERIFIKASI

1. Isi teks 1.759 berkas PDF DDR tidak dipindai, sehingga klaim ketiadaan biaya tidak diperluas ke PDF. Dasar klaim hanya XML dan HTML.
2. Tabel equipment failure diperiksa pada seluruh 325 berkas yang memuatnya, tetapi tidak diperiksa apakah berkas HTML lain memuat tabel kegagalan dengan id berbeda.
3. `witsml_parsed/*.csv` (4,606,027,369 byte, 10 berkas) baru dipindai header-nya pada 7 berkas; tiga berkas (F-12, F-14, F-15_S) dilewati karena melewati batas ukuran 500 MB (`S4-068`). Klaim ketiadaan kolom maintenance pada tiga berkas itu masih belum terukur.
4. Kesetaraan durasi label dengan durasi activity sumbernya tidak diuji per kejadian, hanya diuji agregat per wellbore.
5. Angka lead 11,5 menit dan 6,0 menit diambil dari R8 dan S1 apa adanya, tidak dihitung ulang di kartu ini.
6. Data produksi Volve yang asli (di luar repo) tidak diunduh pada kartu ini, sehingga "tidak ada" berarti tidak ada di workspace, bukan tidak ada di dunia.
7. `data/USROP_health.csv` kolom `maintenance_recommendation` adalah keluaran `code/06_xgb_fuzzy.py:90`, jadi tidak dipakai sebagai bukti maintenance nyata pada dokumen ini.
