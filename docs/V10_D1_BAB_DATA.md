# V10 — BAB 3: DATA — APA YANG DIPAKAI DAN PERANNYA DALAM IDENTIFIKASI KERUSAKAN

| | |
|---|---|
| Nomor dokumen | V10-D1-BAB-DATA |
| Versi | 1.1 (draf bab dari peran Data Engineer — direview & dilengkapi) |
| Tanggal | 2026-10-14 (WIB) |
| Klasifikasi | Internal — bahan penyusunan proposal |
| Peran penyusun | **[Data Engineer] V10-D1** — penerus peran V9-D1 (kartu `t_1ca71445`) |
| Kontrak bab | `docs/V10_PM1_OUTLINE.md` §2 Bab 3 + §3 (DoD Bab 3) |
| Status | Selesai (draf bab) |
| Menutup keluhan operator | **(d) peran data** + porsi data dari **(f) arti 7/11/27** |

**Petunjuk pembacaan.** §3.0 untuk pembaca non-teknis (satu paragraf). §3.1–§3.2 untuk peninjau
teknis (inventaris + isi + peran + keterbatasan tiap dataset). §3.3–§3.5 untuk tim ML/statistik
(kontrak konversi ke dataset latih, diagram alur, daftar kanal terlarang). §3.6–§3.8 penutup
(jawaban pertanyaan proposal dari sudut data, verifikasi, sumber angka).

> **Prinsip bab (kontrak PM1 §4).** Seluruh angka pada bab ini berasal dari dokumen, JSON, dan
> berkas milik peran ini sendiri, dibaca langsung pada sesi penulisan ini. Tidak ada angka yang
> dikarang. Setiap angka yang tidak dapat diverifikasi ditulis apa adanya sebagai keterbatasan.
> Bab ini adalah **solusi** (data apa yang dipakai, isinya apa, masing-masing berperan apa dalam
> deteksi), bukan riwayat kegagalan.

> **Riset pendahuluan: `scientific-critical-thinking`** — setiap besaran dipisah menjadi OBSERVED
> (jumlah baris/kanal yang dihitung dari berkas), PERAN (fungsi data dalam rantai deteksi:
> label, fitur, kontrol, geologi), dan KETERBATASAN (fill-rate, cakupan sumur). Peran data tidak
> disimpulkan dari namanya melainkan dari cara kanal itu masuk ke skema label/fitur.
> **Riset pendahuluan: `verification-mandatory`** — dua angka pada kartu tugas ini terbukti tidak
> cocok dengan berkas primer dan dikoreksi (§3.7): `USROP_labeled.csv` adalah 18 kolom (bukan 115),
> dan `time.csv` F-9A memuat 13 kolom ber-prefix pit (dokumen sumber menyebut 12). Angka yang
> dipakai di bab ini adalah angka hasil hitung ulang dari berkas di disk.
> **Riset pendahuluan: `statistical-analysis`** — fill-rate dilaporkan sebagai pecahan apa adanya
> (bukan dibulatkan menjadi "cukup/tidak cukup"), cakupan sumur per dataset dilaporkan agar
> keterwakilan LOWO dapat dinilai, dan jumlah positif per kelas dibiarkan pada skala aslinya.
> **Riset pendahuluan: `agentmemory`** — fakta tahan-lama peran ini (jumlah baris/kanal tiap dataset,
> koreksi angka, status kelas tanpa label) disimpan sebagai memori lintas-sesi supaya bab turunan
> (ML/statistik/hibrida/eval) tidak menghitung ulang dan tidak mengarang ulang angkanya.

---

## 3.0 RINGKASAN BAB 3 UNTUK DOSEN (satu paragraf)

Alat pemeliharaan prediktif (PdM) ini dibangun dari **satu lapangan nyata (Volve, Equinor — 9
wellbore terparse)**
yang datanya datang dalam banyak format, ditambah **satu dataset bengkel** untuk pengujian keausan
mata bor. Lapisan data bekerja berjenjang: data mentah (log pengeboran WITSML, katalog kejadian,
geometri rangkaian bor, mudlog, log petrofisik, log waktu F-9A, dan data bengkel) diubah menjadi
**grid waktu 60 detik**, lalu menjadi **jendela fitur 10 menit yang hanya melihat ke masa lalu**,
lalu menjadi **matriks latih siap pakai** untuk enam kelas kerusakan rig. Hasil akhirnya adalah
**6 dataset siap-latih berisi 292.954 baris**, dengan **55 fitur** per baris (sebelas kanal
pengeboran dikali lima statistik), dipecah menjadi **37 lipatan uji silang Leave-One-Well-Out**.
Satu aturan kejujuran mengikat seluruh bab ini: **fitur tidak boleh melihat masa depan** — stempel
waktu data terakhir yang masuk ke fitur harus lebih awal daripada stempel waktu label, dan aturan
ini terverifikasi **0 pelanggaran di 6 dari 6 dataset**. Peran data karenanya bukan sekadar bahan
mentah, melainkan penentu kejujuran: kualitas sensor yang buruk diungkap apa adanya (mis. kanal
CRPM di F-14 sebagian besar kosong) sebagai keterbatasan, bukan disembunyikan.

**Kedudukan dalam kosakata PM1 (7 engine / 11 klaim / 27 head).** Bab ini memasok bahan mentah dan
kontrak fitur untuk **7 engine** (vib, ssi, shk, stuck, hyd, bit_wear, tool_wear) dan menjadi dasar
pengukuran **11 klaim** serta **27 head** yang didefinisikan pada `docs/V10_PM1_OUTLINE.md`
§1.1–§1.3. Bab ini tidak menghitung ulang angka 7/11/27; ia menyediakan data dan aturan anti-bocor
yang membuat klaim-klaim tersebut dapat diuji.

---

## 3.1 INVENTARIS DATA (apa yang diolah, berapa banyak, sumbernya)

Tabel berikut merangkum seluruh himpunan data yang diolah peran Data Engineer. Kolom "Berkas/entri"
dan "Baris/isi" adalah angka hasil hitung ulang dari disk pada sesi ini (§3.7).

| # | Dataset | Berkas / entri | Baris / isi | Sumber | Peran utama |
|---|---|---|---|---|---|
| 1 | WITSML time-series terparse | 8 CSV | **7.080.457 baris** | `data/volve/witsml_parsed/` (hasil parse 20.086 XML dari zip Realtime) | **Fitur** + sumber label instrumen |
| 2 | USROP_labeled | 1 CSV | **198.928 baris, 18 kolom** | `data/USROP_labeled.csv` (turunan USROP 7 sumur) | **Fitur mekanis** + label bit_wear |
| 3 | Label kejadian terkurasi | 1 CSV | **884 kejadian** | `data/volve/labels_curated_v2.csv` | **Kontrol / konteks kejadian** |
| 4 | WITSML tubular | 192 XML | **1.392 komponen** | `data/volve/witsml_raw/**/tubular/*.xml` | **Geometri** (fitur drag/buckling) |
| 5 | WITSML bhaRun | 161 XML | 161 run | `data/volve/witsml_raw/**/bhaRun/*.xml` | **Kontrol konteks** (batas run) |
| 6 | WITSML trajectory | 63 XML | **5.561 stasiun survei** | `data/volve/witsml_raw/**/trajectory/*.xml` | **Geologi/geometri** (MD→TVD, inklinasi) |
| 7 | WITSML wbGeometry | 27 XML | **109 section** | `data/volve/witsml_raw/**/wbGeometry/*.xml` | **Geometri sumur** (casing shoe, open hole) |
| 8 | WITSML mudLog | 8 XML | **2.882 interval** | `data/volve/witsml_raw/**/mudLog/*.xml` | **Label geologi** (litologi, gas) |
| 9 | Log petrofisik DLIS/LIS | 21 CSV | **309.644 baris** | `scratch/v6_d1f/csv/` (20 DLIS + 1 LIS terparse) | **Label geologi/petro** (SW/VSH/flag) |
| 10 | Log waktu F-9A | 1 CSV | **419.747 baris, 239 kolom** | `data/witsml/Norway-NA-15_47_9-F-9 A time.csv` | **Fitur + label pit/flow** (hyd K-ii) |
| 11 | Data bengkel tool_wear | 8 xlsx → 1 CSV | **469 jendela, 27 fitur** | Mendeley `th4yv974r2` → `scratch/v6_e1/toolwear_windows.csv` | **Fitur getaran** (engine tool_wear) |
| 12 | Peta katalog Volve | 1 CSV | 4.035 baris | `data/volve_catalog_target_paths.csv` | **Rujukan kelengkapan** (bukan fitur) |
| 13 | TSPP (time-series permukaan) | 4 CSV utama | **52.905 baris** | `data/bo_tspp/` (TSPP1–TSPP4) | **Fitur kandidat frekuensi-tinggi** (kanal permukaan) |

Dua dataset pendukung tambahan dipakai sebagai penguat konteks: **EDM DATABASE** (tag `CD_*`:
pore pressure, frac gradient, survey, assembly) dan **Well_picks_Volve_v1.dat** (**409 formation
pick** di 35 wellbore). Keduanya berperan sebagai fitur konteks geologi/kedalaman, bukan pembentuk
label kegagalan (§3.2.9).

---

## 3.2 ISI, PERAN, DAN KETERBATASAN TIAP DATASET

### 3.2.1 WITSML time-series terparse — 8 CSV, 7.080.457 baris

**Isi.** Log pengeboran berbasis waktu (WITSML 1.4 `log`/`chunk`) yang sudah diparse menjadi CSV.
Delapan berkas: F-14 (1.648.026), F-15_S (1.883.062), F-5 (1.286.967), F-15A (778.162), F-7
(547.500), F-9 (457.545), F-9_A (419.706), dan VAR_F-5_alt (59.489). Setiap sumur membawa 60–281
kanal; kanal yang terisi ≥50% hanya 37–48 kanal per sumur. Kanal inti pengeboran yang dipakai:
`TQA` (torsi permukaan), `SPPA` (tekanan standpipe), `TFLO` (laju alir masuk), `RPM`, `SWOB`
(berat pada bit), `HKLD` (hookload), `ROP`, `BPOS` (posisi block), `SPM` (laju pompa), `depth`,
`dbtm` (kedalaman bit). Kanal instrumen MWD yang menjadi sumber label: `VIBLAT_RT` (getaran
lateral), `SHKRSK_RT` (risiko shock), `STUCK_RT` (status stuck), `CRPM_RT` (collar RPM).

**Peran.** (a) **Fitur** utama untuk seluruh kelas rig — kanal inti di atas masuk ke kontrak fitur
jendela (§3.3). (b) **Sumber label** untuk kelas status: vib (`VIBLAT_RT`), shk (`SHKRSK_RT`),
stuck (`STUCK_RT`), ssi (turunan `CRPM_RT`). (c) **Kontrol** untuk crosscheck resep (bins V9
identik resep V6 pada 7/7 sumur).

**Keterbatasan.** Fill-rate tidak seragam: kanal label jarang terisi di sebagian sumur (mis.
`SHKRSK_RT` F-7 hanya 0,67% baris terisi; `CRPM_RT` F-7 0,51% — sedangkan F-14 `CRPM_RT` 1,40% dan
`VIBLAT_RT` hanya 0,14%). Rentang F-14 2007–2015 sangat renggang relatif grid penuh: dari **96.698
bin menit** hanya **12.635 bin (13,1%)** berstatus drilling (`n_bins_drill`, `v9_d1_01_summary.json`),
sehingga grid penuh dibutuhkan demi konsistensi resep. Sebagian kanal tidak ada sama sekali di sumur
tertentu (mis. `STUCK_RT` hanya ada di F-9, F-9_A, F-10, F-14), sehingga tidak semua kelas dapat
dibentuk di semua sumur.

### 3.2.2 USROP_labeled — 198.928 baris, 18 kolom

**Isi.** Dataset laju penembusan pengeboran untuk 7 sumur. Kolom: `Measured Depth m`, `Weight on
Bit kkgf`, `Average Standpipe Pressure kPa`, `Average Surface Torque kN.m`, `Rate of Penetration
m/h`, `Average Rotary Speed rpm`, `Mud Flow In L/min`, `Mud Density In g/cm3`, `Diameter mm`,
`Average Hookload kkgf`, `Hole Depth (TVD) m`, `USROP Gamma gAPI`, `well`, `label`, `MSE`,
`D_exp`, `ROC_coef`. Kolom kunci WOB/ROP/RPM/MSE/label terisi 100%.

**Peran.** (a) **Fitur mekanis** berbasis kedalaman (WOB, ROP, RPM, torsi, MSE). (b) **Sumber
label** kelas bit_wear melalui blok inefisiensi MSE (Teale): `MSE = WOB/A + (120·π·N·T)/(A·ROP)`;
blok `high_MSE` pada kuantil atas menjadi label K-1. Distribusi kolom `label` (dihitung ulang):
`normal` **134.013**, `high_MSE_bit_wear` **49.732**, `low_ROP_efficiency` **15.183** — dua kelas
inefisiensi berjumlah **64.915 baris (32,6%)**, cukup berpenduduk untuk latih/uji. (c) Kolom `well`
menjadi sumbu pemisah LOWO.

**Keterbatasan.** Dataset ini berbasis kedalaman, bukan waktu — tanpa kolom waktu langsung,
sehingga jembatan ke data time-series harus melalui kedalaman atau label kejadian. `Diameter mm`
diperlukan untuk menghitung `DOC = ROP/(60·RPM)` dan `DS = WOB/(R·DOC)`; satuan WOB (kkgf) wajib
dikonversi ke kN (×9,80665) sebelum dipakai. Angka "115 kolom" pada kartu tugas adalah keliru
(§3.7) — 115 adalah jumlah kolom `depth.csv` F-9A, bukan USROP.

### 3.2.3 Label kejadian terkurasi — 884 kejadian

**Isi.** Katalog kejadian operasional yang dikurasi dari laporan DDR, satu baris per kejadian,
20 kolom (`event_id`, `wellbore`, `event_date`, `act_start`, `act_end`, `md`, `source_code`,
`category`, `bha_relevant`, `evidence`, `outcome`, `component`, dll.). Distribusi kategori:
`routine_no_failure_evidence` 496, `surface_rig_equipment` 216, `mixed_evidence` 47,
`bha_stuck_fishing` 38, `failure_unlocated` 28, `wellbore_fluid` 25,
`wireline_completion_intervention` 21, `bha_downhole_equipment` 12, `safety_personnel` 1.
Kolom `bha_relevant`: `yes` 50, `no` 263, `uncertain` 571.

**Peran.** **Kontrol dan konteks kejadian** — dipakai untuk memverifikasi bahwa label instrumen
(mis. blok `STUCK_RT`) selaras dengan kejadian nyata (kategori `bha_stuck_fishing`), dan untuk
menandai jendela yang harus dikecualikan. Dataset ini bukan pembentuk fitur.

**Keterbatasan.** Sebagian besar kejadian berstatus `uncertain` untuk relevansi BHA (571/884), dan
hanya 582 dari 884 kejadian yang rentang waktunya masuk ke rentang CSV terparse — sehingga tidak
semua kejadian dapat dipakai sebagai pembanding. Angka 884 adalah jumlah kejadian; berkas mentah
memuat 1.413 baris termasuk header dan baris bantu (selisih ini sudah direkonsiliasi pada kampanye
sebelumnya menjadi 884 kejadian eksak).

### 3.2.4 WITSML tubular — 192 XML, 1.392 komponen

**Isi.** 192 assembly rangkaian bor, berisi 1.392 komponen dengan kolom geometri: tipe komponen,
`od` (diameter luar), `id` (diameter dalam), `len` (panjang), `wtPerLen` (berat per panjang).
Komposisi: 1.222 komponen drill string, sisanya collar/casing/alat. Satu komponen tercatat dengan
`od=id=len=−999,25` (nilai sentinel sumber data).

**Peran.** **Geometri** — membuka kalibrasi ulang gaya drag dan fitur buckling/differential
sticking. Luas kontak `A_kontak = Σ π·od·len` per assembly dipakai sebagai penanda relatif risiko
differential sticking (LF3), bukan sebagai label.

**Keterbatasan.** Rating motor (`torqueMax`/`Pmax`) **0 dari 192 berkas** — absen terverifikasi,
sehingga perhitungan torque-on-bit tetap terblokir. Dua berkas assembly tidak mengirim komponen
(sumber data, bukan galat parser). Berat formula `(π/4)(od²−id²)·7850·9,80665` hanya estimasi
kasar: akurat untuk drill collar & casing, tetapi *underestimate* 15–22% untuk drill string.

### 3.2.5 WITSML bhaRun — 161 XML

**Isi.** 161 konfigurasi rangkaian lubang bawah (BHA run), 14 wellbore, memuat `dTimStart`/
`dTimStop`, `numStringRun`, `numBitRun` (11 record), `mdHoleStart`/`mdHoleStop` (19 record),
`comments` (56 record).

**Peran.** **Kontrol konteks** — menandai batas tiap run bor sehingga jendela latih tidak
melintasi pergantian rangkaian, dan menjadi anchor interval untuk penautan ke geometri tubular
(`uidRef` bhaRun→tubular cocok **154/161**).

**Keterbatasan.** Tidak ada label keausan bit (`dullingInfo`/`dullGrade`/`bitName` = 0/161).
Jembatan waktu→kedalaman tipis: `mdHoleStart/Stop` hanya 19/161 record, 3 di antaranya berdurasi
nol. `comments` (56/161) belum diekstrak isinya.

### 3.2.6 WITSML trajectory — 63 XML, 5.561 stasiun

**Isi.** 63 berkas lintasan sumur berisi 5.561 stasiun survei dengan `md`, `tvd`, `incl`
(inklinasi), `azi` (azimut), `dTimStn`. Unit tercampur dan wajib dikonversi: `incl` = 2.574 rad +
2.987 derajat; `azi` = 2.574 rad + 2.920 derajat + 67 stasiun tanpa tag `azi`.

**Peran.** **Geologi/geometri** — menyediakan konversi MD→TVD yang benar untuk interpretasi
kedalaman, dan inklinasi tinggi sebagai penanda risiko differential sticking. Join ke data
berbasis kedalaman melalui wellbore + interpolasi MD.

**Keterbatasan.** 67 stasiun tanpa `azi` (semuanya di satu berkas F-4), dan `dTimStn` hanya
5.415/5.561. Konversi satuan rad/derajat wajib dilakukan eksplisit sebelum dipakai.

### 3.2.7 WITSML wbGeometry — 27 XML, 109 section

**Isi.** 27 berkas geometri sumur berisi 109 section dengan `mdTop`, `mdBottom`, `tvdTop`,
`tvdBottom` (109/109 terisi), dan `typeHoleCasing` (casing 45, riser 31, open hole 23, liner 9,
conductor 1).

**Peran.** **Geometri sumur** — menyediakan kedalaman casing shoe dan batas open hole, yang
diperlukan untuk konteks hidrostatik/overbalance (kelas hyd) dan validasi rentang kedalaman.

**Keterbatasan.** Tag `casingSeat` literal tidak ada; padanan fungsionalnya adalah
`wbGeometrySection`. Root `mdBottom` hanya 26/27 berkas.

### 3.2.8 WITSML mudLog — 8 XML, 2.882 interval

**Isi.** 8 berkas mudlog berisi 2.882 interval geologi (`geologyInterval`), 44 kolom. Litologi
pertama per interval: claystone 957, sandstone 884, limestone 678, marl 178, siltstone 151,
dolomite 17, no sample 10, coal 5, tuff 2. Data gas: `chromatograph` C1–C5 pada 1.316/2.882
interval (45,7%); `mudGas` (gasAv/gasPeak/gasBackgnd) pada 576/2.882 (20,0%).

**Peran.** **Label geologi** — litologi per interval 100% terisi menjadi label auxiliar
(konfidensial konfound per jendela 10 menit) dan fitur geologi one-hot. Interval memuat `dTim` +
`mdTop`/`mdBottom` 100%, sehingga dapat ditautkan ke time-series maupun kedalaman.

**Keterbatasan.** Bukan label kegagalan: tidak ada tag stuck/losses/kick. Gas show (gasAv >
1,5×gasBackgnd) hanya 17/576 — terlalu jarang untuk dijadikan kelas tersendiri. Cakupan sumur
terbatas: dari 7 wellbore target hanya F-15 (dan beberapa sumur di luar target) yang punya mudlog
WITSML.

### 3.2.9 Log petrofisik DLIS/LIS — 21 CSV, 309.644 baris

**Isi.** Hasil parse 20 DLIS + 1 LIS menjadi 21 CSV (309.644 baris). Memuat 504 kanal DLIS + 49
kanal LIS. Kanal label petrofisik siap pakai: `SW` (saturasi air), `BVW`, `VSH` (volume shale),
`CARB_FLAG`, `COAL_FLAG`, `SAND_FLAG` (32.988 valid), dari grup COMPUTED_OUTPUT pada 6 wellbore.
Kanal pengeboran yang ada: `ROP5`, `CRPM`, `ROPAVG`, `WOBAVG`.

**Peran.** **Label geologi/petrofisik** — menyediakan flag litologi dan saturasi sebagai fitur
geologi eksplisit per kedalaman, untuk melawan risiko model bit_wear "hanya mengingat posisi
kedalaman".

**Keterbatasan.** LIS F-7 korup (galat asli `head.prev(=457) != prev(prev(head)).next(=362)`;
1.608 offset-slice gagal), sehingga hanya 1 dari 2 LIS yang terparse. Ada trap satuan: mayoritas
0,1 in (×0,00254 ke meter), sedangkan F-15D memakai mm. Kurva tekanan = 0, sehingga tidak sah
dijadikan label tekanan/kebocoran (hanya fitur pra-lubang).

### 3.2.10 Log waktu F-9A — 419.747 baris, 239 kolom

**Isi.** Satu berkas log waktu berbasis timestamp untuk F-9A (rentang 2009-06-27 → 2015-09-22),
239 kolom. Memuat label instrumen `STUCK_RT` dan kolom volume lumpur ber-prefix
`MudPit Volume Average` (**13 kolom** menurut hitung ulang; dokumen sumber menyebut 12 — lihat
§3.7), kolom `Tank volume (active)`, `Stand Pipe Pressure kPa`, `Flow Pumps L/min`,
`Mud Flow In L/min`, dan kanal gas C1–C5.

**Peran.** (a) **Sumber label** stuck instrumen di sumur kedua di luar F-14. (b) **Fitur aliran**
untuk kelas hyd: label K-ii = z `ΔV_pit` (perubahan volume lumpur) sebagai proxy kick/loss; kanal
`Stand Pipe Pressure` dan `TFLO30s` untuk residu SPPA (K-i).

**Keterbatasan.** Hanya satu sumur (F-9A), sehingga kelas hyd K-ii hanya punya satu wellbore →
kekuatan bukti lintas-sumur lemah. Kanal disfungsi terisi hanya ~45–47 ribu dari 419.747 baris
(~11%), sehingga jendela fitur hanya dapat dibentuk di rentang itu. Mnemonic mentah (`PITTOT`,
`GAINLOSSTOT`, `FLOWOUT`) tidak ada sebagai nama kolom; padanan fungsionalnya yang dipakai.

### 3.2.11 Data bengkel tool_wear — 469 jendela, 27 fitur

**Isi.** Dataset eksternal (Mendeley `th4yv974r2`, CC BY 4.0, SHA-256 8/8 cocok dengan API), 4
alat × 2 run (R01 = baru, R02 = tumpul), dipotong menjadi **469 jendela 1 detik @1000 Hz**, **27
fitur getaran**: `mean/std/rms/kurt/skew/p2p/crest/zcr/fdom` per sumbu X/Y/Z. Distribusi per alat:
T01 120 (60/60), T02 112 (62/50), T03 121 (60/61), T04 116 (58/58).

**Peran.** **Fitur getaran** untuk engine tool_wear (K-i deteksi perubahan-regime, K-ii klasifikasi
lintas-alat). Label = identitas run (R01 vs R02), yang ditetapkan oleh desain dataset, bukan
turunan fitur.

**Keterbatasan.** Domain bengkel terpisah dari domain rig: skala waktu dalam detik (bukan menit),
hanya 4 alat sehingga generalisasi lintas-alat terbatas, dan jendela berelasi waktu (n efektif
jauh lebih kecil dari 469). Transfer ke pengeboran nyata tidak diklaim.

### 3.2.12 Penguat konteks: EDM dan formation picks

EDM DATABASE (`CD_*`) menyumbang fitur konteks: 39.084 baris pore pressure, 37.257 baris frac
gradient, 15.109 stasiun survey, 10.650 komponen assembly, 632 identitas bit. Well_picks memuat
**409 formation pick di 35 wellbore** dengan `MD`+`TVD`+`TVDSS`, dipakai sebagai label stratigrafi
untuk stratifikasi interval. Keterbatasan: profil tekanan pori "ACTUAL" hanya berisi titik datum
(8 baris di datum air laut), sehingga overbalance hanya tersedia sebagai PLAN/PROTOTYPE (fitur
pra-lubang, tidak sah sebagai label pengukuran).

### 3.2.13 TSPP — time-series permukaan (4 CSV utama, 52.905 baris)

**Isi.** Empat berkas frekuensi-tinggi ber-timestamp di `data/bo_tspp/`, satu baris per sampel,
dengan 11 kolom kanal permukaan seragam: `date, Average Hookload kkgf, Hole depth (MD) m, Weight on
Bit kkgf, Block Position m, Average Rotary Speed rpm, Average Surface Torque kN.m, Bit Depth (MD) m,
Average Standpipe Pressure kPa, Mud Flow In L/min, Rate of Penetration m/h`. Volume: TSPP1 21.120 ·
TSPP2 8.499 · TSPP3 12.533 · TSPP4 10.753 = **52.905 baris** (TSPP1-long 59.163 dan TSPP1-15s
5.633 = resolusi berbeda dari TSPP1, bukan data baru).

**Peran.** **Fitur kandidat frekuensi-tinggi** untuk kelas stuck/hidrolik: kanal permukaan lengkap
(torsi, standpipe, flow, hookload, WOB, RPM) ber-timestamp resolusi halus — melengkapi 11 kanal
grid-60-detik dengan respons menit/detik menjelang stuck.

**Keterbatasan.** **Tidak berlabel** — kolom label stuck hanya diklaim di README repo sumber
(`promiseeee`), sedangkan CSV yang dibuka tidak memuat kolom label (D2 §1 #7). Artefak
`TSPP_AE_SCORES.csv` tidak diskriminatif (75–99% baris di atas ambang) dan tidak terdokumentasi →
tidak boleh dikutip sebagai bukti. Karena itu TSPP dipakai hanya sebagai **sumber fitur**, bukan
sumber label; label tetap dari kanal instrumen.

---

## 3.3 ALUR KONVERSI KE DATASET LATIH (dari data mentah ke matriks siap-latih)

Konversi dijalankan oleh lima skrip pipeline pada berkas nyata (bukan simulasi), dengan seed 42
di seluruh tahap. Resep bins identik dengan resep kampanye V6 (crosscheck `ts_index_identical=true`
pada 7/7 sumur, `col_diffs={}`).

### 3.3.1 Tahap 1 — Grid bin 60 detik

Log time-series diubah menjadi **grid menit (60 detik)** dengan mode ALL-rows: setiap menit pada
rentang sumur dibentuk sebagai satu baris, baik terisi maupun kosong. Nilai per kanal diagregasi ke
satu nilai per menit. Pemilihan 60 detik menjaga keseimbangan antara resolusi sinyal pengeboran dan
jumlah baris yang dapat diolah. Tahap ini menghasilkan bins untuk 9 wellbore; crosscheck terhadap
resep V6 identik pada 7 wellbore yang dapat dibandingkan.

### 3.3.2 Tahap 2 — Jendela fitur dan jendela label

Untuk setiap menit anchor `t0` dibentuk dua jendela:

- **Jendela fitur (ketat-lalu):** `[t0−10, t0)` — sepuluh menit data **sebelum** anchor, tidak
  termasuk anchor.
- **Jendela label:** `[t0, t0+10)` — sepuluh menit data **setelah** anchor, menentukan apakah
  kejadian terjadi.

Pemisahan ketat ini adalah inti anti-bocor: fitur selalu berasal dari masa lalu relatif label.

### 3.3.3 Tahap 3 — Fitur: 11 kanal × 5 statistik = 55 fitur

Setiap kanal di jendela fitur diringkas menjadi lima statistik: `mean`, `std` (ddof=1), `slope`
(regresi OLS per menit), `last` (nilai terakhir), `frac` (pecahan nilai valid). Kanal fitur untuk
kelas rig adalah **11 kanal**:

```
TQA, SPPA, TFLO, RPM, SWOB, HKLD, ROP, BPOS, SPM, depth, dbtm
```

sehingga jumlah fitur = 11 × 5 = **55 fitur**. Khusus kelas hyd K-i, kanal `SPPA`, `TFLO`, dan
`SPM` dikecualikan (anti-sirkularitas karena kanal ini membentuk label), sehingga tersisa 8 kanal ×
5 = **40 fitur**. Data bengkel memakai 27 fitur getaran (§3.2.11).

### 3.3.4 Tahap 4 — Enam dataset latih (292.954 baris) dan 37 fold LOWO

Hasil akhir adalah enam matriks siap-latih. Jumlah baris dan fitur per dataset (dihitung ulang dari
berkas `datasets/*.csv.gz` pada sesi ini):

| Dataset | Baris | Fitur | Positif | Sumur | Fold LOWO |
|---|---:|---:|---:|---:|---:|
| vib | 23.922 | 55 | 5.429 | 4 | 4 |
| ssi | 35.906 | 55 | 607 | 9 | 9 |
| shk | 56.495 | 55 | 2.005 | 9 | 9 |
| stuck_k1 | 5.555 | 55 | 2.007 | 2 | 2 |
| hyd_ki | 52.509 | 40 | 7.172 | 9 | 9 |
| stuck_k2 | 118.567 | 55 | 1.975 | 4 | 4 |
| **Total** | **292.954** | — | **19.195** | — | **37** |

**Split Leave-One-Well-Out (LOWO).** Setiap lipatan menahan satu sumur sebagai uji dan memakai
sumur lainnya sebagai latih — total **37 lipatan** (4+9+9+2+9+4). Skema ini menguji daya generalisasi
antar-sumur, bukan sekadar interpolasi waktu dalam satu sumur. Sumur dengan jumlah positif terlalu
kecil (mis. ssi F-7 = 3 positif) ditandai `underpowered` agar validasi tidak menuntut metrik stabil
pada lipatan tanpa daya statistik. Imputasi dan normalisasi dilakukan fold-safe (hanya dari data
latih tiap lipatan).

### 3.3.5 Anti-bocor: `feat_ts_max < lab_ts`

Setiap baris membawa lima kolom stempel: `well` (identitas sumur, untuk LOWO), `ts_bin` (menit
anchor), `feat_ts_max` (menit data terakhir yang masuk jendela fitur), `lab_ts` (menit peristiwa/
label), `lab_kind` (jenis baris). Invariant yang mengikat: **`feat_ts_max < lab_ts`** untuk semua
baris. Hasil verifikasi ulang langsung dari berkas ter-merge (bukan dari klaim pembuat dataset):

| Dataset | Baris | Pelanggaran `feat_ts_max ≥ lab_ts` | Baris `feat_ts_max` NaN |
|---|---:|---:|---:|
| vib | 23.922 | 0 | 0 |
| ssi | 35.906 | 0 | 0 |
| shk | 56.495 | 0 | 0 |
| stuck_k1 | 5.555 | 0 | 0 |
| hyd_ki | 52.509 | 0 | 0 |
| stuck_k2 | 118.567 | 0 | 0 |

**Total: 0 pelanggaran di 6 dari 6 dataset.** Ini adalah bukti utama bahwa matriks latih tidak
mengandung kebocoran waktu.

### 3.3.6 Skema label per kelas dan anti-sirkularitas

| Kelas | Label | Sumber | Kanal terlarang jadi fitur |
|---|---|---|---|
| vib | `VIBLAT_RT ≥ 32,17405` | kanal MWD instrumen | `VIBLAT_RT` |
| ssi | `SSI = (max−min)/(2·mean)` dari `CRPM` ≥ 1, ≥10 sampel | turunan fisika | `CRPM_RT` |
| shk | `SHKRSK_RT ≥ 1` | kanal MWD instrumen | `SHKRSK_RT` |
| stuck K-i | `STUCK_RT ≥ 1` (status blok) | kanal MWD | `STUCK_RT` |
| stuck K-ii | onset edge 0→1 `STUCK` ffill, horizon H=10 menit | label terkurasi | `STUCK_RT` |
| hyd K-i | hydraulic imbalance (residu SPPA vs bin TFLO) | turunan fisika | `SPPA`/`TFLO`/`SPM` |
| bit_wear K-1 | blok `high_MSE` (Teale, kuantil P75) | USROP | `WOB`/`ROP`/`RPM`/`TQA` |
| tool_wear | identitas run (desain dataset) | Mendeley | (tidak ada) |

Kanal `VIBLAT_RT`, `SHKRSK_RT`, `STUCK_RT`, dan `CRPM_RT` **tidak** termasuk dalam 11 kanal fitur,
sehingga kanal pembentuk label tidak pernah menjadi fitur. Asersi anti-sirkularitas lolos pada
seluruh kelas.

---

## 3.4 DIAGRAM ALUR DATA (mentah → bin → jendela → fitur + label)

```
                 SUMBER DATA MENTAH
  ┌───────────────────────┬────────────────────────┬──────────────────────┐
  │ WITSML time-series    │ USROP_labeled          │ Bengkel tool_wear    │
  │ 8 CSV · 7.080.457 brs │ 198.928 brs · 18 kol   │ 469 jendela · 27 ftr │
  │ (F-5..F-15_S, VAR)    │ (7 sumur, per-MD)      │ (4 alat × 2 run)     │
  └───────────┬───────────┴───────────┬────────────┴──────────┬───────────┘
              │                       │                       │
  Penguat konteks:            Geometri/geologi:        (domain terpisah —
  labels_curated_v2 (884)     tubular 192/1.392,        tetap pada grid 1 dtk)
  bhaRun 161, EDM CD_*        bhaRun 161, traj 63/5.561,
  Well_picks 409              wbGeometry 27/109,
                              mudLog 8/2.882, DLIS 21/309.644
              │
              ▼
  ┌───────────────────────────────────────────────────────────────┐
  │ TAHAP 1 — GRID BIN 60 DETIK (mode ALL-rows, seed 42)          │
  │ setiap menit = satu baris; kanal diagregasi per menit         │
  └───────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
  ┌───────────────────────────────────────────────────────────────┐
  │ TAHAP 2 — JENDELA (anchor t0)                                 │
  │                                                               │
  │   fitur: [t0−10, t0)  ◄── KETAT-LALU (tidak termasuk t0)      │
  │   label: [t0, t0+10)  ◄── masa depan relatif fitur            │
  └───────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
  ┌───────────────────────────────────────────────────────────────┐
  │ TAHAP 3 — FITUR: 11 kanal × 5 statistik = 55 fitur            │
  │   kanal: TQA SPPA TFLO RPM SWOB HKLD ROP BPOS SPM depth dbtm  │
  │   stat : mean · std(ddof=1) · slope(OLS/menit) · last · frac  │
  │   (hyd K-i: 8 kanal → 40 fitur; kanal label dikecualikan)     │
  └───────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
  ┌───────────────────────────────────────────────────────────────┐
  │ TAHAP 4 — MATRIKS LATIH: 6 dataset · 292.954 baris            │
  │   vib 23.922 · ssi 35.906 · shk 56.495 · stuck_k1 5.555       │
  │   hyd_ki 52.509 · stuck_k2 118.567                            │
  │   stempel: well · ts_bin · feat_ts_max · lab_ts · lab_kind    │
  │   INVARIANT ANTI-BOCOR: feat_ts_max < lab_ts  (0 pelanggaran) │
  └───────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
  ┌───────────────────────────────────────────────────────────────┐
  │ SPLIT LOWO — 37 lipatan (4+9+9+2+9+4)                         │
  │   tiap lipatan: 1 sumur = uji, sisanya = latih                │
  │   imputasi/normalisasi fold-safe (hanya dari data latih)      │
  └───────────────────────────────────────────────────────────────┘
```

---

## 3.5 DAFTAR KANAL TERLARANG JADI FITUR (anti-sirkularitas)

Tabel ini mengikat tim ML dan statistik: kanal yang membentuk label tidak boleh muncul sebagai
fitur pada kelas yang sama.

| Kelas | Kanal terlarang menjadi fitur | Alasan |
|---|---|---|
| vib | `VIBLAT_RT` | label = ambang kanal itu sendiri |
| ssi | `CRPM_RT` | label = turunan kanal itu sendiri |
| shk | `SHKRSK_RT` | label = ambang kanal itu sendiri |
| stuck K-i/K-ii | `STUCK_RT` | label = status kanal itu sendiri |
| hyd K-i | `SPPA`, `TFLO`, `SPM` | label = residu SPPA terhadap bin TFLO |
| hyd K-ii | kolom pit + `GAINLOSSTOT` | label = z `ΔV_pit` |
| bit_wear K-1 | `WOB`, `ROP`, `RPM`, `TQA` | label = blok MSE turunan kanal-kanal ini |
| tool_wear | (tidak ada) | label = identitas run, bukan turunan fitur |

Kanal fitur kelas rig (`TQA SPPA TFLO RPM SWOB HKLD ROP BPOS SPM depth dbtm`) tidak memuat kanal
label mana pun. Kelas hyd K-i memakai subset 8 kanal tanpa `SPPA`/`TFLO`/`SPM`.

---

## 3.6 JAWABAN PERTANYAAN PROPOSAL DARI SUDUT DATA

### 3.6.1 (d) Peran data

Data berperan pada tiga tingkat. **Pertama, sebagai bahan mentah** yang memasok kanal fisik
pengeboran (11 kanal inti) dan kanal getaran bengkel (27 fitur). **Kedua, sebagai pembentuk
label**: label tidak dikarang dari luar, melainkan diturunkan dari kanal fisik/status operasional
yang terukur (`VIBLAT_RT`, `SHKRSK_RT`, `STUCK_RT`, `CRPM_RT`, MSE Teale, `ΔV_pit`) atau dari
desain dataset (identitas run bengkel). **Ketiga, sebagai penentu kejujuran**: kualitas sensor yang
buruk dan cakupan sumur yang terbatas diungkap sebagai keterbatasan, dan invariant anti-bocor
`feat_ts_max < lab_ts` memastikan fitur tidak melihat masa depan. Peran data karenanya bukan
sekadar bahan mentah, melainkan penjaga validitas seluruh klaim.

### 3.6.2 (a) Apa yang dideteksi dan data mana yang menopangnya

| Engine | Hal yang dideteksi | Data penopang utama |
|---|---|---|
| vib | getaran lateral berlebih | `VIBLAT_RT` (label) + 11 kanal fitur |
| ssi | stick-slip torsional | `CRPM_RT` (label) + 11 kanal fitur |
| shk | bit bounce/shock risk | `SHKRSK_RT` (label) + 11 kanal fitur |
| stuck | pipa terjepit (status + onset) | `STUCK_RT` (label) + USROP + tubular + bhaRun |
| hyd | anomali hidrolik + proxy kick/loss | `SPPA`/`TFLO` (label) + 13 kolom pit F-9A + TSPP (52.905 baris kanal permukaan) |
| bit_wear | keausan bit (blok MSE) | USROP (WOB/ROP/RPM/MSE) + DLIS flag + picks |
| tool_wear | keausan mata bor (bengkel) | 27 fitur getaran Mendeley |

### 3.6.3 (f) Peran angka 7 vs 11 vs 27 dari sudut data

Bab ini memasok data untuk **7 engine** (kelas kerusakan), menjadi dasar pengukuran **11 klaim**
(pertanyaan tugas terpisah: deteksi-kondisi vs prediksi-onset), dan menyediakan fitur/label bagi
**27 head** (varian metode terukur). Angka 7/11/27 didefinisikan eksak pada
`docs/V10_PM1_OUTLINE.md` §1.1–§1.3; bab data tidak menjumlahkannya, melainkan menyediakan bahan
yang membuat ketiganya dapat diuji.

---

## 3.7 VERIFIKASI DAN KOREKSI (hasil hitung ulang dari berkas primer)

Seluruh angka pada bab ini dihitung ulang dari berkas di disk pada sesi penulisan ini, bukan
dikutip dari ingatan. Dua angka pada kartu tugas terbukti tidak cocok dengan berkas primer dan
dikoreksi sebagai berikut.

1. **`USROP_labeled.csv` = 18 kolom, bukan 115.** Kartu tugas menyebut "USROP_labeled (198.928/115
   kolom)". Hitung ulang header berkas `data/USROP_labeled.csv` menunjukkan **18 kolom** (baris data
   198.928). Angka **115** adalah jumlah kolom berkas `depth.csv` F-9A
   (`data/witsml/Norway-NA-15_47_9-F-9 A depth.csv`, 115 kolom, 16.670 baris), yaitu dataset
   berbeda. Angka yang dipakai di bab ini: USROP = 198.928 baris / 18 kolom.

2. **`time.csv` F-9A memuat 13 kolom ber-prefix pit, dokumen sumber menyebut 12.** Hitung ulang
   header `data/witsml/Norway-NA-15_47_9-F-9 A time.csv` (239 kolom total) menemukan **13 kolom**
   `MudPit Volume Average` bernomor **1–10, 12, 13, 14** (nomor **11** tidak ada di header), plus
   `Tank volume (active)` dan `Tank volume change (active)` sebagai kolom terpisah. Dokumen sumber
   (`V9_R1_JUSTIFICATION.md`) menyebut "12 kolom pit". **Akar selisih ditemukan:** kolom nomor
   **3 dan 13 ditulis tanpa spasi** (`MudPit Volume Average3 m3`, `MudPit Volume Average13 m3`),
   sehingga pencocokan pola berspasi hanya menangkap 11 kolom dan satu kolom terlewat — jadi "12"
   berasal dari pola `Average N` yang tidak menangkap #3/#13. Angka yang dipakai di bab ini: **13
   kolom pit** (hitung ulang pola `Average\s*\d+`).

Angka lain yang diverifikasi ulang dan **cocok**: WITSML 7.080.457 baris / 8 CSV; labels_curated_v2
884 kejadian (distribusi kategori 496/216/47/38/28/25/21/12/1 dan `bha_relevant` yes 50 / no 263 /
uncertain 571 dihitung ulang — cocok persis); tubular 192 XML / 1.392 komponen; bhaRun 161
(uidRef `bhaRun.tubular`→`tubular` cocok **154/161** diverifikasi ulang dengan regex ketat
`<tubular\s+…\buid=` atas 191 uid tubular); trajectory 63 (5.561 stasiun); wbGeometry 27 (109
section); mudLog 8 (2.882 interval); DLIS 21 CSV / 309.644 baris; toolwear 469 jendela / 27 fitur;
TSPP 4 CSV utama / 52.905 baris; EDM 10.650 `CD_ASSEMBLY_COMP` / 632 `CD_BHA_COMP_BIT`;
6 dataset latih 292.954 baris; 37 fold LOWO; anti-bocor 0 pelanggaran 6/6.

**Kontrol aritmetika:** total dataset latih `23.922 + 35.906 + 56.495 + 5.555 + 52.509 + 118.567 =
292.954`; total fold `4 + 9 + 9 + 2 + 9 + 4 = 37`; total WITSML `59.489 + 547.500 + 1.883.062 +
1.286.967 + 457.545 + 1.648.026 + 778.162 + 419.706 = 7.080.457` — ketiganya cocok.

---

## 3.8 BATAS JUJUR BAB INI

1. Semua angka adalah hasil hitung ulang dari berkas di disk (dokumen/JSON/CSV milik peran ini).
   Bab ini tidak menjalankan ulang pipeline penuh; ia memverifikasi angka dari artefak yang ada.
2. Dua koreksi angka pada §3.7 (USROP 18 kolom; pit 13 kolom) menggantikan angka pada kartu tugas
   yang tidak cocok dengan berkas primer. Angka koreksi ini yang mengikat bab-bab selanjutnya.
3. "Belum tersedia" dipisah tegas dari "gagal": kelas hyd K-ii hanya tersedia untuk satu sumur
   (F-9A); rating motor tubular 0/192; tekanan pori EDM ACTUAL hanya titik datum. Semua ini adalah
   keterbatasan yang dilaporkan, bukan angka nol yang disamarkan.
4. Bab ini berlaku untuk data Volve pada sumur yang terkalibrasi; generalisasi ke lapangan lain
   tidak diklaim.

## 3.9 SUMBER ANGKA (traceability)

- `data/volve/witsml_parsed/_parse_summary.json` + `docs/V3_WITSML_PARSE_REPORT.md` — WITSML 8 CSV, 7.080.457 baris.
- `data/USROP_labeled.csv` (header + `wc -l`) — 198.928 baris, 18 kolom.
- `data/volve/labels_curated_v2.csv` — 884 kejadian (distribusi kategori dihitung ulang).
- `docs/V6_D1a_TUBULAR.md` (192 XML / 1.392 komponen) · `docs/V6_D1b_BHARUN.md` (161) ·
  `docs/V6_D1c_TRAJ_GEOM.md` (63 / 5.561 · 27 / 109) · `docs/V6_D1d_MUDLOG.md` (8 / 2.882) ·
  `docs/V6_D1f_PETRO.md` (21 CSV / 309.644) · `docs/V6_D1h_KAGGLE_CAT.md` (time.csv 239 kolom).
- `data/witsml/Norway-NA-15_47_9-F-9 A time.csv` (header) — 239 kolom, 13 kolom pit.
- `data/bo_tspp/TSPP{1,2,3,4}.csv` — 52.905 baris kanal permukaan; label nihil (D2 §1 #7).
- `scratch/v6_e1/toolwear_windows.csv` (469 × 27) + `scratch/v6_e1/ch50_toolwear_summary.json`.
- `scratch/v9_d1/datasets/*.csv.gz` (6 dataset, 292.954 baris) + `scratch/v9_d1/lowo_*.json`
  (37 fold) + `scratch/v9_d1/v9_d1_05_leak_lowo.json` (0 pelanggaran 6/6).
- `docs/V9_D1_DATA_PIPELINE.md` — kontrak grid 60 detik, jendela ketat-lalu, skema label.
- `docs/V6_D2_EXTERNAL_DATASETS.md` §1 #7 — TSPP tanpa kolom label (koreksi klaim README).
- `docs/V7_A1_SOLUTION_AUDIT.md` D5 + `docs/V7_M2_SYNTHESIS.md` — uidRef bhaRun→tubular 154/161 (verifikasi mandiri).
- `docs/V10_PM1_OUTLINE.md` §1–§3 — kosakata 7/11/27 dan kontrak Bab 3.

## 3.10 CATATAN REVIEW (Data Engineer, revisi bab)

Bab ini adalah draf dari konsultan peran; pada revisi ini dilakukan **pengecekan angka terhadap
berkas/JSON primer** dan **penyempurnaan penutupan keluhan**:

- **Ditambahkan:** dataset **TSPP** (52.905 baris, 4 CSV utama) yang sebelumnya tidak masuk
  inventaris, padahal ia sumber fitur frekuensi-tinggi untuk kelas stuck/hidrolik (§3.1 #13, §3.2.13).
- **Ditambahkan:** distribusi label USROP yang eksak — `normal` 134.013 · `high_MSE_bit_wear`
  49.732 · `low_ROP_efficiency` 15.183 (§3.2.2) — bukti bahwa kelas bit_wear cukup berpenduduk.
- **Dikoreksi (temuan review):** klaim "`CRPM_RT` F-14 0,5% baris" → nilai benar **F-14 `CRPM_RT`
  1,40%** (angka 0,51% adalah `CRPM_RT` **F-7**); ditambah `VIBLAT_RT` F-14 0,14% (§3.2.1).
- **Dikoreksi (temuan review):** "selisih 1 kolom pit belum diselesaikan" → **akar selisih
  ditemukan**: kolom pit #3 & #13 ditulis tanpa spasi (`Average3`/`Average13`) sehingga pola
  berspasi hanya menangkap 12 dari 13 kolom (§3.7).
- **Diverifikasi ulang & cocok:** distribusi kategori `labels_curated_v2` (496/216/47/38/28/25/21/12/1)
  dan `bha_relevant` (50/263/571); uidRef bhaRun→tubular 154/161; kontrol aritmetika 292.954 / 37 /
  7.080.457 (§3.7).
- **Baris riset:** nama skill disesuaikan menjadi `verification-mandatory` (nama resmi skill yang
  dipakai) dan ditambah baris `agentmemory` (fakta tahan-lama) sesuai kontrak PM1 §4.5.
