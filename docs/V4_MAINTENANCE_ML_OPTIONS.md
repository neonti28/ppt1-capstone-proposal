# OPSI ML MAINTENANCE (TERSIMPAN, BELUM DIEKSEKUSI)

**Status:** Dokumen ini berisi rekomendasi yang **disimpan atas permintaan operator (Neonti) per 6 Oktober 2026** dan **belum dieksekusi**. Operator menyatakan belum memilih jalur. Dokumen ini dibuat agar ketiga rekomendasi dapat dipanggil kembali dengan angka yang persis, bukan ingatan yang luntur.

**Riset pendahuluan:** `exploratory-data-analysis` (audit fill-rate 115 kolom mentah lintas 7 sumur, struktur 77 file `bhaRun`, dan isi 4 dataset TSPP). Seluruh angka bawah berasal dari eksekusi langsung pada 6 Oktober 2026, bukan kutipan dokumen lama.

**Konteks:** dokumen ini muncul setelah verdict #3 (6 Oktober 2026) menutup jalur LULUS PENUH untuk klaim "prediksi dini kegagalan BHA dari sensor permukaan Volve". Ketiga opsi di sini adalah **klaim dan target baru yang berbeda**, bukan percobaan ulang keluarga kampanye T2. Bila dieksekusi, semuanya wajib lewat pra-registrasi baru sebelum hasil diketahui.

---

## 1. Temuan audit yang menjadi dasar (angka terverifikasi, DIPERBARUI 9 Okt 2026)

> **KOREKSI PENTING (9 Okt 2026).** Angka pada versi dokumen pertama keliru dan telah terbukti salah lewat pindaian ulang seluruh 7 file. Kesalahannya: (a) diklaim "115 kolom", padahal itu hanya kolom pada satu file contoh (F-9A); union seluruh sumur = **275 kolom**, dan yang tersedia di semua 7 sumur hanya **29 kolom**. (b) Diklaim `MWD Shock Risk` sebagai data bagus, padahal kolom itu **praktis selalu nol** (hanya 26 baris non-nol di 2 sumur) sehingga tidak bisa dipakai. (c) Diklaim empat kelas siap pakai, padahya setelah diuji prediksi, sinyalnya lemah. Angka yang benar ada di bawah ini, seluruhnya dari pindaian langsung.

### 1.1 Sebaran nyata kolom (pindaian ulang seluruh 7 file)

Total baris seluruh 7 file mentah: **429.520** (angka 198.928 yang lama adalah `USROP_labeled.csv`, yaitu set berbeda, bukan seluruh data mentah). Union kolom: **275**. Kolom yang tersedia di semua 7 sumur: **hanya 29**. Artinya kolom label jarang tersedia lintas sumur, dan ini menentukan kelayakan evaluasi.

### 1.2 Ketersediaan nyata kandidat label (di berapa sumur kolom ada dan punya nilai non-nol)

| Kandidat label | Kolom ada di | Nilai non-nol di | Total baris non-nol |
|---|---|---|---|
| `MWD Shock Peak m/s2` | 7/7 | 6/7 | 2.651 |
| `STUCK_RT unitless` | 2/7 | 1/7 pada pindaian parsial, 2/7 pada pindaian penuh | 628 |
| `MWD Shock Risk unitless` | 7/7 | **2/7** | **26 (tidak layak)** |
| `MWD Total Shocks unitless` | 7/7 | 1/7 | 602 (bernilai 0 semua) |
| `Total Bit Revolutions unitless` | 6/7 | 6/7 | bervariasi lebar |
| `Bit Drill Time h` | 7/7 | 7/7 | — |

### 1.3 `STUCK_RT` ada hanya di 2 sumur, dan itu masalah untuk evaluasi

| Sumur | Baris tersedia | Baris non-nol | Kode yang muncul |
|---|---|---|---|
| F-9A | 1.221 | 510 | 1, 2, 3 |
| F-14 | 3.223 | 118 | 1, 2 |

Lima sumur lainnya **tidak punya kolom `STUCK_RT` sama sekali**. Konsekuensinya: pada evaluasi Leave-One-Well-Out antar 7 sumur, recall untuk kelas stuck **tidak bisa dihitung** di 5 sumur uji yang tidak memiliki kolom itu. Artinya meski labelnya instrumen dan bersih, kelas ini hanya bisa divalidasi di 2 sumur.

### 1.4 Keluarga kolom getaran: bukan beberapa jenis, melainkan getaran dari alat berbeda

Ditemukan kolom getaran dari enam alat berbeda: `MWD Shock Peak`, `ARC Shock Level`, `CRS Shock Level`, `Isonic Shock`, `PowerDrive Shock Risk`, `Shock Level Computed DH`. Pada F-14 yang memilikinya paling banyak, jumlah baris non-nol tiap kolom hanya 7 hingga 1.474, dan **hampir tidak pernah non-nol di baris yang sama** (pasangan paling tinggi hanya 16 baris). Ini berarti keduanya: bukan pengukuran ganda pada waktu sama (bukan redundansi murni), tetapi juga **bukan jenis dysfungsi berbeda**, karena semuanya mengukur getaran, hanya alatnya aktif di kedalaman berbeda. Menghitungnya sebagai jenis kerusakan terpisah akan keliru.

Gabungan seluruh kolom getaran (union) memberi **6.927 baris di semua 7 sumur**, dengan prevalensi 0,4% hingga 6,4% per sumur.

### 1.5 Dataset TSPP sudah ada lokal dan sudah berlabel

Lokasi: `data/bo_tspp/`. Empat file utama (frekuensi tinggi, format `date` + 10 kanal permukaan):

| File | Baris | Rentang waktu | Kanal |
|---|---|---|---|
| `TSPP1.csv` | 21.120 | 2007-07-06 hingga 2007-07-07 | date, hookload, hole depth, WOB, block position, rotary speed, surface torque, bit depth, standpipe pressure, mud flow in, ROP |
| `TSPP2.csv` | 8.499 | 2007-10-23 | sama, rotary speed tersedia |
| `TSPP3.csv` | 12.533 | 2009-07-03 | memakai `RPM30s` dan `Averaged WOB` |
| `TSPP4.csv` | 10.753 | 2007-12-01 | sama dengan TSPP1 |

Jumlah keempat file utama: **52.905 baris**. Varian tambahan `TSPP1-long.csv` (59.163 baris), `TSPP1-15s.csv` (5.633 baris), `TSPP2.csv` (1.034 KB) membuat total seluruh isi folder 117.701 baris, yang sebagian merupakan duplikat TSPP1 dalam resolusi berbeda.

**Catatan jujur soal artefak AE:** `docs/V2_TSPP_AE_SCORES.csv` menunjukkan autoencoder pernah dijalankan di TSPP, tetapi angkanya tidak diskriminatif (`share_above_threshold` 75 hingga 99% baris terdeteksi) dan **tidak terdokumentasi di MD mana pun**. Artefak itu tidak boleh dikutip sebagai bukti; TSPP harus dikerjakan ulang dengan desain berlabel.

### 1.6 `bhaRun` berisi interval per run, bukan penilaian keausan

77 file XML `bhaRun` terdeteksi di disk (dokumen akuisisi mencatat 161 total, perlu rekonsiliasi). Tag yang ada di seluruh sampel: `nameWell`, `nameWellbore`, `name`, `dTimStart`, `dTimStop`, `numStringRun`, `commonData`. Satu file di antaranya memuat `numBitRun`, `dTimStartDrilling`, `dTimStopDrilling`. **Tidak ditemukan** tag `dullingInfo`, `dullGrade`, atau `bitName`, sehingga `bhaRun` hanya memberi label "kapan run dimulai dan berakhir", bukan tingkat keausan fisik.

---

### 1.7 Hasil tes prediksi (9 Okt 2026): sinyalnya LEMAH, dan ini harus dipahami sebelum memilih jalur

Untuk menguji apakah getaran benar-benar bisa diprediksi dari sensor permukaan (klaim kunci Opsi 2), dijalankan tes langsung: model Random Forest memprediksi kejadian getaran 5 baris ke depan dari window 10 baris sensor permukaan, dievaluasi Leave-One-Well-Out antar 7 sumur, 211.205 unit, prevalensi 2,11%.

| Sumur uji | n | Prevalensi | AUPRC | ROC-AUC |
|---|---|---|---|---|
| F-14 | 30.285 | 0,076 | 0,0608 | 0,385 |
| F-15 | 59.608 | 0,000 | 0,0002 | 0,561 |
| F-15S | 84.143 | 0,015 | 0,0139 | 0,465 |
| F-5 | 9.111 | 0,009 | 0,0101 | 0,538 |
| F-7 | 6.989 | 0,022 | 0,0224 | 0,443 |
| F-9A | 16.117 | 0,034 | 0,0669 | 0,655 |
| F-9 | 4.952 | 0,015 | 0,0592 | 0,831 |

**Hasil: AUPRC rata-rata 0,0333 terhadap prevalensi 0,0245, yaitu lift hanya 1,36 kali.** ROC-AUC di tiga sumur berada di bawah 0,5, artinya lebih buruk daripada tebakan acak pada sumur-sumur itu.

Pemeriksaan pendukung: torsi permukaan sebelum kejadian getaran memang berbeda dari baseline (efek size rata-rata +0,39), tetapi **arah perubahannya tidak konsisten antar sumur** (F-15S +0,01, F-5 -0,42, F-7 +0,05). Ketidakcocokan arah antar sumur adalah tanda bahwa pola tidak generalisir, dan itu persis prasyarat yang membuat kampanye lama gagal.

**Batas klaim atas hasil ini:** tes ini hanya satu desain sederhana (window tetap, prediksi 5 baris, fitur mean/std/baris terakhir). Ia **bukan bukti bahwa sinyal tidak ada**, tetapi juga **bukan bukti bahwa sinyal ada**. Statusnya: belum terbukti. Yang tes ini tetapkan dengan pasti: pernyataan bahwa getaran "pasti bisa diprediksi dari permukaan" tidak dapat dipertahankan.

## 2. Tiga rekomendasi (TERSIMPAN, belum dipilih operator)

### Opsi 1: Sistem pencegahan stuck-pipe (rekomendasi tertinggi)

- **Target:** klasifikasi status stuck (`STUCK_RT` kode 0/1/2/3) dan deteksi dini beberapa menit sebelum status memburuk.
- **Data:** `STUCK_RT` F-9A (510 baris berlabel) dan F-14 (118 baris berlabel), ditambah 4 dataset TSPP (52.905 baris, kanal permukaan lengkap dengan timestamp).
- **Alasan dapat berhasil bila ML lama gagal:** (a) label instrumen, sehingga akar #1 hilang; (b) horizon menit, bukan jam, dan pada rentang ini fisika merespons secara nyata: torsi naik, standpipe naik, flow turun, hookload lengket; (c) sinyalnya berada di sensor permukaan yang sudah kita miliki; (d) literatur mendukung, yaitu Aramco JOT 2020 melaporkan 2 alert sebelum insiden saat playback, dan paper Crossformer 2025 memakai tipe data Volve yang sama.
- **Framing maintenance:** stuck-pipe adalah pos NPT terbesar dalam pengeboran; mencegahnya berarti menjaga integritas peralatan (menghindari fishing, kehilangan bit, kerusakan well).
- **Risiko jujur:** jumlah peristiwa kecil (TSPP hanya 4 kasus; `STUCK_RT` hanya di 2 sumur).

### Opsi 2: Deteksi dysfungsi drill-string (stick-slip, shock, whirl)

- **Target:** anomaly detection per sumur (autoencoder, resep MDPI) yang menghasilkan indeks kondisi sepanjang pengeboran.
- **Data:** `MWD Shock Risk`, `MWD Shock Peak`, `MWD Turbine RPM` hadir di **semua 7 sumur**; torsi dan RPM permukaan tersedia penuh.
- **Framing maintenance:** condition monitoring klasik; getaran destruktif inilah yang memperpendek umur BHA dan MWD.
- **Risiko jujur:** label "kerusakan" tidak tersedia langsung, sehingga validasinya lewat korelasi dengan event bit run atau stuck, bukan angka presisi tinggi.

### Opsi 3: Prediksi sisa umur bit (RUL bit)

- **Target:** time-to-pull (survival analysis) atau kelas keausan bit.
- **Data:** `Total Bit Revolutions` (33,6% di F-9A, 30,7% di F-7), `Bit Drilling Time`, ditambah interval `dTimStart`/`dTimStop` dari 77 file `bhaRun` sebagai label kapan bit ditarik.
- **Framing maintenance:** contoh textbook predictive maintenance, sangat sesuai rubrik.
- **Risiko jujur:** fill rate timpang antar sumur; label = peristiwa penarikan, bukan pengukuran keausan fisik (lihat §1.4).

---

## 3. Kandidat yang dibuang setelah dicek (bukan lupa, tetapi tidak layak)

| Kandidat lama (dari jawaban 28 September) | Alasan dibuang (bukti) |
|---|---|
| Prediksi kick/kontrol sumur dari kromatografi gas | `Iso-butane` hanya terisi 2,4 hingga 3,2%, hanya di F-9A dan F-15 |
| Prediksi kegagalan MWD dari confidence flag | jumlah event terlalu sedikit untuk evaluasi |
| Segala sesuatu yang bergantung pada seismic | seismic adalah citra bawah permukaan, tidak berkaitan dengan peralatan |
| LAS logs sebagai input utama | hanya konteks geologi, bukan sinyal peralatan |

---

## 4. Selisih pokok dengan ML lama (verdict #3)

| Aspek | ML lama (ditutup) | Opsi baru di dokumen ini |
|---|---|---|
| Sumber label | naratif harian, 65% `uncertain` | instrumen rig (`STUCK_RT`) atau peristiwa TSPP |
| Horizon | 6 hingga 24 jam sebelum kejadian | detik hingga menit menjelang stuck |
| Keberadaan sinyal di permukaan | tidak ada, terbukti 5 kampanye | ada (torsi, tekanan, flow merespons mekanis) |

## 5. Urutan eksekusi yang disarankan (menunggu perintah operator)

1. **T3-a: baseline stuck-pipe TSPP.** Data mandiri dan sudah berlabel, kecil (52.905 baris), prototype selesai dalam satu kampanye. Kalau TSPP tidak menunjukkan sinyal, kegagalannya diketahui dalam hitungan jam.
2. **T3-b: kampanye `STUCK_RT` lintas sumur** dengan pra-registrasi penuh, hanya bila T3-a positif.
3. **T3-c: dysfungsi dan RUL bit** sebagai opsi menyusul.

Setiap langkah wajib mengikuti protokol `docs/PROTOCOL_RISET_TIM.md`: pra-registrasi sebelum hasil, satu kampanye per desain, verifier independen, lalu audit ulang.

**Berkas sumber:** `data/bo_tspp/*`, `data/USROP/Code/Norway*.csv`, `data/volve/external/dbx_volume/WITSML Realtime drilling data/*/1/bhaRun/*.xml`, `docs/V2_TSPP_AE_SCORES.csv`, `docs/V3_DATA_ACQUISITION_INVENTORY.md`.

## 6. Opsi pasca-V9 — dua lever naik tier (IDE DISIMPAN 12 Okt 2026, BELUM dieksekusi, menunggu perintah operator)

Status saat ini: vonis `docs/V9_PM2_VERDICT.md` = **LAYAK** (alat advisory, 0 alarm otomatis). Dua opsi di bawah hanya diperlukan **kalau operator ingin menaikkan tier**; kalau target capstone cukup di LAYAK, keduanya boleh di-skip. Ini bukan target baru — ini merapikan "syarat yang sudah terdaftar" di PM2 §langkah lanjut #2–#3 menjadi satu rencana terstruktur.

### 6a. Perbaikan label (G7) — urutan PERTAMA

**Mengapa:** bukti V8 `V8_PM_VERDICT.md` baris 217 (verbatim): *"terendah ada di label (G7), bukan di model."*
Tiga cacat label terukur:
1. Kontrol-positif stuck **0/10** gagal (V8 §G7) → precision/recall stuck dihitung dari basis salah.
2. hyd label = **proxy (residu)**, bukan kejadian hidrati nyata → hyd K-ii P=R=0 @q95.
3. Severity-mix beda lintas-well → sebagian CI RF memuat prevalence (ssi 5/9, shk 7/9, vib 0/4) = skor tak mengalahkan tebakan trivial.

Dampak tertulis: **"mengancam kuadran onset"** (V8 baris 202) = head prediksi (stuck K-ii, hyd K-ii) tak akan kredibel sebelum G7 beres.

**Isi kerja:** pra-reg Fase 0 (PM1 §6.2): kunci satu varian onset stuck strict-vs-ffill · verifikasi semantik skala 0/1/2/3 `STUCK_RT`/`SHKRSK_RT` lintas-well · rekonsiliasi prev stuck 66,9% vs 49,4% · sinkronisasi zona-waktu kontrol-positif · ganti/absen label hyd dengan kejadian nyata (bukan residu).

### 6b. Kalibrasi ambang per-well — urutan KEDUA (setelah 6a)

**Mengapa:** ambang global terbukti gagal — **FAR τ0,5 menyebar 119,6× antar sumur** (V9 tabel vib). PM2 langkah lanjut #3 eksplisit: *"Kalibrasi ambang per-well prospektif (D-A4) = syarat UTAMA naik tier hyd K-i & vib/shk RF ke L1 penuh — diukur, bukan diasumsikan."*

**Isi kerja:** setel ambang per sumur (prospektif, tanpa bocor waktu) untuk hyd K-i + vib RF + shk RF · ukur FAR setelah kalibrasi · bandingkan ke baseline persistence. Analogi berlaku: alarm asap dikalibrasi per ruangan (dapur vs kamar tidur), bukan satu ambang global.

**Syarat & batas (jujur):**
- Urutan wajib **6a → 6b**: kalibrasi menyetel ambang terhadap "kebenaran"; kalau label salah → presisi palsu.
- Keduanya **tidak** menyentuh ambang G1/G2 yang sudah dikunci (FAR≤1/24j + B1≥80% + C2/C3) — itu tetap gerbang alarm otomatis (PM1 §1.3).
- Alarm otomatis (Tahap 3a) tetap hanya setelah syarat di atas **terukur**.
- Belum diverifikasi: apakah kalibrasi per-well bertahan lintas periode (butuh uji temporal terpisah) — statusnya hipotesis sampai diukur.

**Ditulis oleh:** asisten, 12 Okt 2026, dari sintesis `V8_PM_VERDICT.md` + `V9_PM2_VERDICT.md`. Belum ada satupun langkah 6a/6b yang dieksekusi — semua masih ide.