# V7-M1 — DELEGASI: solusi R&D diteruskan ke 8 pembaca + spesifikasi cek per jenis file

Task: `t_0d02b12f` [Master Data Reader] · Board: capstone-v7-solve · Tanggal: 2026-10-11 (WIB)
Sumber solusi: `docs/V7_R1_SOLUTIONS.md` (parent `t_d2cab982`). Peta data: `docs/V6_D0_READERS_SYNTHESIS.md` + `docs/V6_D1a..h` + `docs/V6_E1_ML_DESIGN.md` §4.4.
Kartu bawahan (8): `t_5f46ecdc` (D1a TUBULAR), `t_3e886804` (D1b BHARUN), `t_8200703b` (D1c TRAJECTORY+WBGEOMETRY), `t_352301b3` (D1d MUDLOG), `t_515137cd` (D1e LOG XML), `t_3b4c9512` (D1f PETRO), `t_f948943d` (D1g EDM), `t_4ec90702` (D1h KAGGLE+CATALOG).

> **Riset pendahuluan: `scientific-critical-thinking`** — pemetaan solusi→bawahan diperiksa dengan prinsip klaim-vs-bukti: dokumen ini HANYA berisi spesifikasi cek dan pertanyaan; setiap klaim "data ada" di dalamnya dikutip dari sumber ber-angka (V7-R1 §1/§9, D0 §1) dengan atribusi, bukan ditegakkan ulang oleh Master (pembacaan data = tugas bawahan, aturan #5 body task). Tes pembeda tiap solusi (V7-R1 §2–§6) diterjemahkan jadi pertanyaan "ada/tidak + baris non-null + proses apa" agar kegagalan prasyarat terbaca sebelum eksekusi.
> **Riset pendahuluan: `verification-mandatory`** — (a) daftar solusi dibaca ulang langsung dari `V7_R1_SOLUTIONS.md` (270 baris, tidak dari ingatan); (b) 8 kartu bawahan dibuka satu per satu lewat `kanban_show` — domain tiap kartu diverifikasi dari body kartu, bukan asumsi; (c) gate G1/G2 pra-reg V6 TIDAK disentuh (V7-R1 §8) — tidak ada pertanyaan cek yang meminta perubahan ambang; (d) keberadaan komentar terverifikasi pascapengiriman dengan `kanban_show` ulang (bukan klaim terkirim).

---

## 0. PERAN, LINGKUP, DAN ATURAN UNTUK SEMUA BAWAHAN

- Master MENYUSUN + MENERUSKAN. Bawahan MENGECEK data. Bawahan TIDAK menjalankan kampanye ML, TIDAK mengubah gate, TIDAK mengecek domain bawahan lain.
- Status wajib per item cek: **ADA LANGSUNG** (kolom/kurva siap pakai) / **ADA SETELAH DIOLAH** (perlu proses: extract, resample, join, turunan rumus) / **TIDAK ADA** (wajib dibuktikan grep/ls — klaim ketiadaan tanpa bukti = gagal).
- Setiap jawaban wajib memuat 3 hal: **(1) kolom/kurva-nya ada/tidak, (2) berapa baris non-null + path, (3) proses apa agar jadi fitur/label.**
- Semua path yang disebut di bawah adalah klaim V7-R1/D0 yang SUDAH diverifikasi penulisnya; tugas pembaca = konfirmasi/koreksi dengan bukti cetak sendiri, bukan mengulang klaim.
- Jebakan yang sudah diketahui (D0 §2.5) wajib diperhatikan saat join: `folder ≠ nameWellbore` (join pakai field XML), satuan campuran (trajectory rad/dega, DLIS 0.1 in, EDM ft), `WHIRL_RT == BOUNCE_RT` (jangan dihitung 2 fitur).

---

## 1. TABEL UTAMA: solusi | data needed | bawahan (kartu) | pertanyaan cek

| # | Solusi (V7-R1) | Kelas dituju | Data needed (path sumber) | Bawahan (kartu) | Pertanyaan cek (ringkas — detail §2) |
|---|---|---|---|---|---|
| 1 | **S-A1** stuck onset (label ONSET 0→1, bukan status) | `stuck` | `data/witsml/Norway-NA-15_47_9-F-9 A time.csv` (langsung, STUCK_RT) + `data/volve/witsml_parsed/F-14.csv`, `F-9_A.csv` + parse F-10/F-12 (S-A2) | 08 KAGGLE (`t_4ec90702`) + 05 LOG XML (`t_515137cd`) | 08: kolom `STUCK_RT` di time.csv — ada? berapa baris non-null & berapa transisi 0→1? perlu proses apa jadi label onset? 05: di raw F-10/F-12, file mana yang mendaftarkan `STUCK_RT` — jumlah file + baris data? |
| 2 | **S-A2** parse 2 sumur eligible baru F-10 & F-12 | `stuck` | `witsml_raw/…-15_47_9-F-10/1/log/**` (18 file STUCK_RT) & `…-F-12/…` (6 file) — perlu diolah ke CSV | 05 LOG XML (`t_515137cd`) | Ada berapa file log & berapa yang punya `STUCK_RT`? Ikut punya `HKLD/TQA/RPM/TFLO/SPPA` (fitur wajib jendela)? Perlu proses apa (parser V6, grid 60 dtk)? |
| 3 | **S-A3** weak supervision Snorkel (LF1 STUCK_RT, LF2 event kurasi, LF3 overbalance, LF4 overpull/torsi) | `stuck` | `data/labels_curated_v2.csv` (LANGSUNG, 1.413 baris — selisih 884 vs 1.412 WAJIB direkonsiliasi) + kanal `HKLD/TQA` (05) + USROP (08) + pore pressure overbalance (07) | 08 + 05 + 07 EDM (`t_f948943d`) | 08: hitung baris event labels_curated_v2 per tipe; kolom apa saja (timestamp/wellbore)? 05: `HKLD_AVG/TQA_AVG` non-null di CSV/raw? 07: ada tabel tekanan ACTUAL (pore pressure) depth-indexed untuk proxy overbalance? |
| 4 | **S-B1** parse 4 wellbore kaya shk: F-10/F-4/F-12/F-15 | `shk` (+`ssi`,`vib`,`stuck`) | `witsml_raw/…-F-10` (188), `…-F-4` (135), `…-F-12` (91), `…-F-15` (77) file `SHKRSK_RT` — total ~825 file, perlu diolah | 05 LOG XML (`t_515137cd`) | Tiap wellbore: jumlah file `SHKRSK_RT`/`CRPM_RT`/`VIBLAT_RT`/`STICK_RT` (recount independen vs V7-R1 §1.2)? Baris data per file? Fitur wajib ikut ada? Proses apa → CSV? |
| 5 | **S-B2** ganti unit jendela → PER-STAND | `shk` | `witsml_parsed/*.csv` + boundary stand dari `BPOS`/gap waktu (perlu diolah) + interval run bhaRun (kandidat anchor) | 05 + 02 BHARUN (`t_3e886804`) | 05: kolom `BPOS` ada di berapa CSV/wellbore, non-null berapa? Gap waktu terdeteksi berapa? 02: `dTimStart/Stop` 161 run — berapa yang valid (bukan durasi negatif) & bisa jadi batas trip/stand? |
| 6 | **S-B3** ordinal/regresi level shock 0–3 | `shk` | kanal `SHKRSK_RT` di 7 CSV + 4 wellbore baru (langsung) | 05 LOG XML (`t_515137cd`) | Distribusi nilai `SHKRSK_RT` (0/1/2/3) per wellbore — hitung kemunculan tiap skala? Semantik skala terdokumentasi di header WITSML? |
| 7 | **S-C1** hyd ONSET (bukan status ambang) | `hyd` | `witsml_parsed/*.csv` kolom `SPPA/TFLO/SPM` (langsung; label dihitung ulang) | 05 LOG XML (`t_515137cd`) | Kolom `SPPA`, `TFLO`, `SPM_*` ada di 8 CSV parser lama? Non-null berapa baris per wellbore? Ada di raw wellbore baru? |
| 8 | **S-C2** label fisika well-control: pit gain / flow mismatch / gas | `hyd` | raw F-9 `PIT1..PIT30`, `GAINLOSSTOT`, `FLOWOUT/FLOWOUTPC` (ADA di raw, belum CSV — D1e) + F-1 C/F-11 (`GAINLOSSTOT` 575/517 file, `PITTOT` 565/506) + time.csv F-9 A (08) + mud gas C1–C5 (04) | 05 + 08 + 04 MUDLOG (`t_352301b3`) | 05: `PIT*/GAINLOSSTOT/FLOWOUT*` muncul di berapa file F-9/F-1C/F-11, non-null? 08: kolom pit/flow di time.csv? 04: kolom `C1..C5`/total gas non-null berapa baris, joint bagaimana ke time/depth? |
| 9 | **S-C3** survival/hazard time-to-event | `hyd` | turunan dari label S-C1/S-C2 (tidak ada data baru) | 05 + 08 (sumber label) | Konfirmasi label sumber S-C1/S-C2 terpetakan (baris per label) sebelum model survival dipakai. |
| 10 | **S-D1** label PROGRESI keausan (change-point per run) | `tool_wear` | 8 xlsx akselerometer 1000 Hz: `scratch/v6_e1/toolwear/DrillingToolWearDataset_T0{1..4}_R0{1,2}.xlsx` (LANGSUNG) | 08 KAGGLE (`t_4ec90702`) | 8 file ada? Nama sheet/kolom? Baris non-null per file? Timestamp/sampling rate konstan? |
| 11 | **S-D2** fitur VMD + BP-NN | `tool_wear` | 8 xlsx (sama) | 08 | Panjang deret per run (baris)? Kanal X/Y/Z ada semua? Nilai hilang/NaN berapa? |
| 12 | **S-D3** label keausan turunan MSE/DS (Menand & Mills) | `tool_wear`/`bit_wear` | `data/USROP_labeled.csv` (LANGSUNG, 198.928 baris; WOB/ROP/RPM/MSE ada) | 08 (+05 cross-check sumber MSE) | Kolom `WOB/ROP/RPM/MSE/label` ada? Non-null per kolom? Kolom kedalaman/waktu untuk hitung `DS` & `DOC`? |
| 13 | **S-D4** learning-to-rank pairwise | `tool_wear` | 8 xlsx (sama) | 08 | Cukupkah jumlah sampel per run untuk pasangan (baris/run)? |
| 14 | **S-E1** parse F-10/F-4/F-12/F-15 untuk `ssi` (`CRPM_RT` 186/135/90/76) | `ssi` | raw 4 wellbore (sama dengan S-B1) | 05 LOG XML (`t_515137cd`) | `CRPM_RT` per wellbore: jumlah file + baris; kolom pendukung `STKSLP/STICK_RT` ikut ada? |
| 15 | **S-E2** prereg-ulang stabilitas fold (bootstrap per fold) | `ssi` | turunan: jumlah positif per fold dari CSV label (tidak ada data baru) | 05 + 08 | Siapkan angka: baris label per wellbore per kelas (stuck/shk/ssi/vib) agar fold UNDERPOWERED bisa dihitung ulang. |
| 16 | **S-F1** onset-of-high-MSE | `bit_wear` | `data/USROP_labeled.csv` (LANGSUNG; kolom `label` terverifikasi) + anchor bit-run (02) | 08 + 02 BHARUN (`t_3e886804`) | 08: kolom `label` distribusi (normal/high_MSE_bit_wear/low_ROP) + kolom depth/waktu untuk deteksi blok? 02: `numBitRun` + `dTimStart/Stop` — bisa dipakai memotong USROP per bit-run? |
| 17 | **S-F2** label silang MSE/DS | `bit_wear` | `data/USROP_labeled.csv` (sama) | 08 | Kolom turunan `MSE/DS` butuh `DOC/ROP/RPM/WOB` — semua ada? Berapa baris lengkap (non-null semua)? |

Catatan lintas-solusi: S-B1/S-A2/S-E1 adalah SATU pekerjaan parse yang melayani 4 kelas — satu set bukti kanal dari Pembaca 05 dipakai untuk ketiganya.

---

## 2. SPESIFIKASI CEK PER BAWAHAN (dikirim sebagai komentar ke kartu masing-masing)

### 2.1 Pembaca 01 — TUBULAR (`t_5f46ecdc`, D1a)
Domain: 192 file `tubular/*.xml`, 1.392 komponen (od/id/len/wtPerLen), 62 tipe komponen.
Solusi terkait: **S-A3** (LF3 differential sticking `F = μ·A·ΔP` — butuh geometri kontak/BHA), **S-B1/S-E1** (fitur pemisah shk/ssi/vib: stabilizer spacing, motor, komposisi drill string), **S-F1/S-D3** (identitas/ukuran bit sebagai konteks keausan).
Pertanyaan cek (ketiganya wajib berformat ada/tidak + baris non-null + proses):
1. Apakah ada komponen tipe **bit** di 192 file (kolom apa: bitType/OD/blade count)? Berapa file & baris non-null? Perlu proses apa untuk jadi fitur kelas `bit_wear` (join ke wellbore via field `nameWellbore`, bukan path)?
2. Apakah **stabilizer** (od, length, posisi axial) tercatat berapa komponen? Berapa baris non-null? Proses apa jadi fitur jarak stabilizer → prediktor stick-slip/whirl?
3. Konfirmasi/koreksi klaim D0: rating motor (`torqueMax/Pmax`) = **0/192 file** — buktikan dengan grep; kalau ternyata ada, sebut file-nya (membuka I1/TOB).

### 2.2 Pembaca 02 — BHARUN (`t_3e886804`, D1b)
Domain: 161 file `bhaRun/*.xml`, 161 run, 14 wellbore, `dTimStart/Stop`, numBitRun 11, 9 drilling window.
Solusi terkait: **S-B2** (anchor interval/stand), **S-F1** (potong USROP per bit-run untuk onset keausan), **S-B1/S-A2** (kelayakan fold wellbore baru: apakah F-10/F-4/F-12/F-15 punya run interval sama sekali).
Pertanyaan cek:
1. Untuk wellbore **F-10, F-4, F-12, F-15**: ada berapa run di 161 file (filter `nameWellbore` field, bukan path)? Kolom `dTimStart/Stop` non-null berapa? → status: ada/tidak sebagai anchor waktu fold baru.
2. Kolom `numBitRun`: berapa nilai integer valid, berapa non-integer ("3 RR 1") & durasi negatif? Perlu proses apa agar jadi pemotong interval bit-run untuk S-F1?
3. `dTimStart/Stop` bisa diolah jadi batas trip/stand untuk S-B2? Berapa interval yang tumpang-tindih dengan 8 wellbore CSV parser lama (join by nameWellbore + rentang waktu)?

### 2.3 Pembaca 03 — TRAJECTORY + WBGEOMETRY (`t_8200703b`, D1c)
Domain: 63 trajectory + 27 wbGeometry, 5.561 survey station, MD/TVD/incl/azim, casing seat.
Solusi terkait: **S-F1** (SHAP `bit_wear` didominasi `TVD_mean/last` → koreksi MD→TVD wajib sebelum label kedalaman dipakai), **S-A3 LF3** (incl tinggi = risiko differential sticking), **S-C1/S-C2** (TVD untuk hidrostatik/overbalance).
Pertanyaan cek:
1. Untuk 4 fold `bit_wear` (F-14, F-15, F-15S, F-5) + F-9_A: apakah ada survey station MD→TVD yang menutup rentang kedalaman USROP? Berapa baris station non-null per wellbore? Proses apa untuk join MD→TVD ke baris time-based (interpolasi MD terbesar naik)?
2. `incl` dalam satuan apa per file (rad/dega campuran — konfirmasi angka D0: 2574 rad + 2987 dega)? Berapa stasiun tanpa `azi`? Proses konversi apa wajib sebelum join?
3. wbGeometry: `casingSeat`/casing shoe MD — berapa section non-null? Bisa jadi konteks tekanan (lubang terbuka) untuk S-C1/S-C2? Status: ada langsung / setelah diolah / tidak ada.

### 2.4 Pembaca 04 — MUDLOG (`t_352301b3`, D1d)
Domain: 8 file `mudLog/*.xml`, 2.882 geologyInterval, 44 kolom, litologi 100%, C1–C5 45,7%, gas show 17/576.
Solusi terkait: **S-C2** (label kick/awal kejadian dari kenaikan gas C1–C5 — sumber label BERBEDA dari fitur), **S-A3** (litologi = auxiliary label anti-konfond: model jangan belajar formasi = kegagalan), **S-C1** (litologi/gas sebagai konteks hidrolik: formation pore context).
Pertanyaan cek:
1. Kolom **chromatograph `C1..C5` + total gas**: ada di berapa file/interval? Berapa baris non-null (angka riil, bukan persen D0)? Intervalnya depth-based atau time-based — kolom apa join key-nya ke WITSML time-series? Proses apa (interpolasi depth→time via MD) agar jadi label onset gas-rise?
2. Kolom **litologi** (`lithology`/qualifier): 2.882 interval — berapa non-null per kategori (claystone/sandstone/…)? Proses apa jadi auxiliary label per jendela 10 menit?
3. Buktikan klaim negatif: apakah ada kolom/tag apa pun yang menyebut **stuck/losses/kick/NPT** di 8 file (grep)? Kalau tidak ada → status TIDAK ADA dengan bukti grep.

### 2.5 Pembaca 05 — LOG XML (`t_515137cd`, D1e) — BEBAN TERBESAR
Domain: 7.150 file log XML; parser lama = 8 CSV; F-1 C (2.156) + F-11 (1.750) belum diparse.
Solusi terkait: **S-A2, S-B1, S-B3, S-C1, S-C2, S-E1, S-E2** + verifikasi independen scan V7-R1 §1.
Pertanyaan cek:
1. **Recount independen** (jangan salin V7-R1): di raw `…-F-10`, `…-F-4`, `…-F-12`, `…-F-15` — berapa file mendaftarkan `SHKRSK_RT`, `CRPM_RT`, `STICK_RT`, `VIBLAT_RT`, `STUCK_RT`, `STKSLP`? Cetak jumlahnya per wellbore; bandingkan dengan klaim §1.2 (188/135/91/77 dst.) — cocok atau beda?
2. Untuk tiap kanal di (1): **baris data nyata** di `<logData>` berapa (bukan jumlah file)? Sampling interval berapa detik? → status ADA LANGSUNG/SETELAH DIOLAH untuk label onset (S-A2/S-B1/S-E1).
3. **Fitur wajib jendela** ikut ada di 4 wellbore baru: `HKLD_AVG`, `TQA/TORQUE_*`, `RPM/SURF_RPM`, `WOB`, `TFLO/FLOWIN`, `SPPA`, `ROP`, `BPOS`, `dbtm/HAS`? Tiap kanal: berapa file & baris non-null → menentukan S-B1/S-A2 layak-tidak.
4. **S-C2**: `PIT*`, `GAINLOSSTOT`, `PITTOT`, `FLOWOUT`, `FLOWOUTPC` — berapa file di F-9 raw, F-1 C, F-11 yang mendaftarkan (klaim 575/517/565/506)? Berapa baris non-null? → label pit/flow-mismatch.
5. **S-C1**: `SPPA`, `TFLO`, `SPM` non-null di 8 CSV parser lama per wellbore (baris)? → relabel onset hyd.
6. **S-B2**: kolom `BPOS` ada di berapa CSV; gap waktu >N menit per wellbore berapa banyak (proses → kandidat batas stand)?
7. **S-B3**: distribusi nilai `SHKRSK_RT` (0/1/2/3) per wellbore — hitung kemunculan tiap nilai; apakah unit/skala terdokumentasi di `logCurveInfo`?
8. Konfirmasi klaim §1.1 (negatif): F-1 C/F-11 **nol** kanal `SHKRSK_RT/STUCK_RT/VIBLAT_RT/CRPM_RT` — buktikan grep sendiri pada sampel ≥100 file; kalau ada 1 file berisi → klaim R1 salah, laporkan.
9. **S-E2**: siapkan hitungan baris label per wellbore (untuk fold UNDERPOWERED): dari CSV mana pun yang relevan, berapa baris & positif per kelas — angka riil.

### 2.6 Pembaca 06 — PETRO DLIS/LIS/LAS (`t_3b4c9512`, D1f)
Domain: 20/20 DLIS + 1/2 LIS (F-7 korup), 504 channel, 309.644 baris, label SW/VSH/BVW/CARB/COAL di 6 wellbore.
Solusi terkait: **S-B1/S-E1** (kanal drilling petro `ROP5/CRPM/ROPAVG/WOBAVG` = sumber fitur/label alternatif untuk wellbore yang WITSML-nya tipis), **S-A3 LF3 / S-C2** (overbalance: butuh indikator tekanan formasi — apakah ada kurva tekanan/mud-weight?), **S-F1** (formation tops = konteks depth untuk blok high-MSE).
Pertanyaan cek:
1. Kanal drilling `ROP5`, `CRPM`, `ROPAVG`, `WOBAVG`: ada di berapa file/wellbore? Baris non-null? Status: bisa jadi fitur lintas-sumur (S-B1) atau hanya cross-check?
2. Kurva **tekanan/pressure** (RM, mud weight, hydrostatic, pore-pressure proxy) ada tidak di 504 channel? Sebut nama channel + baris non-null → bahan overbalance S-A3 LF3; kalau tidak ada → TIDAK ADA + bukti daftar channel.
3. Formation tops/flags (`CARB_FLAG`, `COAL_FLAG`, tops): berapa interval non-null, di wellbore mana? Proses apa → label konteks kedalaman untuk S-F1?
4. Unit trap: mayoritas 0.1 in (×0.00254) — konfirmasi pada sampel + sebutkan kolom mana yang butuh konversi sebelum join.

### 2.7 Pembaca 07 — EDM (`t_f948943d`, D1g)
Domain: `Volve F.edm.zip` → XML 211 MB, 142 tag, 21 well/54 wellbore, `phase=ACTUAL/PLAN`.
Solusi terkait: **S-A3** (LF2 = event kurasi — apakah EDM punya tabel event operasional time-stamped yang layak? D0 memvonis BUKAN event DB; tugas: konfirmasi/koreksi dengan grep sendiri), **S-A3 LF3 / S-C2** (pore pressure 39.084 + frac 37.257 baris = proxy overbalance depth-indexed), **S-F1** (CD_BHA_COMP_BIT = identitas bit; `bit_size` 4 terisi).
Pertanyaan cek:
1. Dengan **filter `phase=ACTUAL`**: berapa baris `CD_` pore pressure & frac gradient per wellbore? Kolom depth/uom apa (ft?)? Status → fitur overbalance (ADA SETELAH DIOLAH: konversi ft→m + join depth) untuk S-A3 LF3/S-C2.
2. Tag **bit**: `CD_BHA_COMP_BIT` (atau sejenis) — berapa baris terisi selain `bit_size` (bit type/serial/dull)? Tunjukkan field-nya → untuk S-F1/S-D3 identitas bit; kalau hanya 4 baris → laporkan apa adanya.
3. **Event/NPT**: grep tag yang benar-benar berupa event (waktu mulai–selesai) — bukan substring. Sebut nama tag + jumlah baris + 3 contoh isi. Konfirmasi atau bantah klaim D0 "EDM bukan event DB" dengan bukti Anda sendiri. Ini penting untuk LF2 S-A3.
4. **Wellpath ACTUAL**: berapa survey baris per wellbore untuk F-2/F-3/F-6/F-8 (well tanpa WITSML)? Bisa jadi sumber MD→TVD alternatif? Status: langsung/diolah/tidak ada.

### 2.8 Pembaca 08 — KAGGLE + CATALOG (`t_4ec90702`, D1h)
Domain: time.csv (239 kolom, 419.747 baris, F-9 A), depth.csv (115 kolom, 16.670 baris), 2 zip (duplikat), catalog, `VOLVE_INVENTORY.xlsx`, well picks (409), USROP_labeled.csv & toolwear xlsx di lingkup csv/dataset turunan.
Solusi terkait: **S-A1** (STUCK_RT onset di time.csv), **S-A3** (`labels_curated_v2.csv` rekonsiliasi 884 vs 1.412), **S-C2** (kolom pit/flow di time.csv), **S-D1/D2/D4** (8 xlsx toolwear), **S-D3/S-F1/S-F2** (USROP_labeled.csv), **S-E2** (angka label per fold).
Pertanyaan cek:
1. `time.csv` F-9 A: kolom `STUCK_RT` — ada? berapa baris non-null, berapa **transisi 0→1** (kandidat onset)? Kolom `CRPM/STKSLP/SHKRSK/VIBLAT/STICK` juga ada? → proses apa jadi label onset S-A1?
2. `time.csv`: kolom `PITTOT`, `GAINLOSSTOT`, `FLOWOUT`, `FLOWOUTPC`, `PIT*`, `SPPA`, `TFLO`, `SPM` — mana yang ada di 239 kolom? non-null berapa? → S-C2/S-C1 di F-9 A tanpa parse XML.
3. `labels_curated_v2.csv` (`data/`): hitung ULANG baris (klaim: 1.413 termasuk header = 1.412 event; V6_R1 menulis 884). Kolom apa saja (waktu/wellbore/tipe event)? Rekonsiliasi selisih — ini PRASYARAT S-A3.
4. `USROP_labeled.csv` (198.928 baris): kolom `WOB/ROP/RPM/MSE/label/depth/time` — masing-masing non-null berapa? Distribusi `label` (normal/high_MSE_bit_wear/low_ROP_efficiency)? Kolom apa untuk hitung `DS=DOC` → `MSE/DS` (S-F2)? Transisi blok `label` (kandidat onset S-F1) berapa?
5. 8 xlsx toolwear (`scratch/v6_e1/toolwear/`): file ada semua? per file: nama sheet, kolom (time/X/Y/Z?), baris, sampling 1000 Hz konstan?, NaN berapa? → status S-D1 (change-point per run), S-D2 (VMD), S-D4 (ranking pasangan).
6. Well picks 409 + WBS* codes: baris non-null, join key → label litologi/stratigrafi lintas 35 wellbore (aux label, pengganti/lengkap mudLog)?
7. Zip kaggle F-9 A: konfirmasi duplikat identik (checksum) — jangan dijual sebagai data baru.

---

## 3. MATRIS TRACEABILITY (acceptance-a: 15/15 solusi punya ≥1 bawahan)

| Solusi | 01 TUB | 02 BHAR | 03 TRAJ | 04 MUD | 05 LOG | 06 PET | 07 EDM | 08 KAG |
|---|---|---|---|---|---|---|---|---|
| S-A1 | | | | | ✓ | | | **✓** |
| S-A2 | | | | | **✓** | | | |
| S-A3 | ✓ | | ✓ | ✓ | ✓ | ✓ | ✓ | **✓** |
| S-B1 | ✓ | | | | **✓** | ✓ | | |
| S-B2 | | ✓ | | | **✓** | | | |
| S-B3 | | | | | **✓** | | | |
| S-C1 | | | ✓ | ✓ | **✓** | ✓ | | ✓ |
| S-C2 | | | ✓ | ✓ | **✓** | ✓ | ✓ | **✓** |
| S-C3 | | | | | ✓ | | | ✓ |
| S-D1/D2/D4 | | | | | | | | **✓** |
| S-D3 | ✓* | | | | | | | **✓** |
| S-E1 | | | | | **✓** | ✓ | | |
| S-E2 | | ✓ | | | ✓ | | | ✓ |
| S-F1 | ✓ | ✓ | ✓ | | | ✓ | ✓ | **✓** |
| S-F2 | | | | | | | | **✓** |

✓ tebal = pemilik utama cek; ✓ = pendukung/konteks; `✓*` S-D3 via identitas bit/konteks geometri.

---

## 4. CATATAN & BELUM DIVERIFIKASI (verification-mandatory #3)

1. Semua "path ADA" di tabel §1 adalah **kutipan** V7-R1 §9.2 / D0 §1 yang sudah diverifikasi penulisnya — Master tidak membuka ulang file data (aturan #5 body task). Pembaca wajib konfirmasi dengan cetak bukti sendiri; kalau path salah/ketemu beda → laporkan, jangan disesuaikan diam-diam.
2. Selisih `labels_curated_v2.csv` (1.412 vs 884 event) dan `16 vs 20 file DLIS` adalah titik rekonsiliasi eksplisit (soal 1 & D0 §4.8).
3. Angka per-fold kegagalan (§4.4 E1) dikutip apa adanya; perubahan apa pun pada gate = di luar lingkup seluruh kartu di board ini.
4. Belum diverifikasi oleh Master (by design): keberadaan/nilai setiap kolom di 8 domain — itu memang deliverable 8 kartu di §2.
