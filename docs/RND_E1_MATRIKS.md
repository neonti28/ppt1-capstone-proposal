# RND-E1: MATRIKS KELAYAKAN ALGORITMA x Detektor DAN SHORTLIST

Kartu: `t_9abcb3b3` · Board: `rnd-algo-2026` · Tanggal: 2026-10-27 (WIB)
Workspace: `/mnt/d/Capstone 1(v2)` · Arsip `/mnt/d/Capstone 1` tidak disentuh
Masukan: R1, R2, R3, R4, R5, R6, D0, P0, E0, dan tabel tier `docs/V9_EVAL_C_LAYERC.md`.
Keluaran: matriks 28 algoritma x 7 mode (196 sel), skor prioritas berbobot, 6 kandidat, 3 finalis.

## Riset pendahuluan

Riset pendahuluan: what-if-oracle, statistical-analysis, verification-mandatory, scientific-critical-thinking

- `what-if-oracle` dipakai untuk memetakan empat cabang hasil pilot (finalis berhasil menurunkan FAR, finalis berhasil tetapi biayanya tidak terbayar, finalis gagal karena label, dan cabang liar berupa perubahan definisi label), lalu memilih tindakan tanpa penyesalan yang berlaku di semua cabang.
- `statistical-analysis` dipakai untuk menolak membandingkan angka antar kelas yang desainnya berbeda: uji yang sah ditentukan per pertanyaan (Wilson untuk presisi, Poisson eksak Garwood untuk rasio FAR, uji tanda untuk arah per well), dan efek minimum yang dapat dideteksi dipakai sebagai syarat sebelum menjanjikan kenaikan tier, bukan sesudahnya.
- `verification-mandatory` dipakai sebagai gerbang tulis: setiap angka di dokumen ini menunjuk baris ledger, skor yang merupakan penilaian diberi kelas KONVENSI, dan angka yang tidak terukur ditulis BELUM TERUKUR tanpa dibulatkan menjadi tebakan.
- `scientific-critical-thinking` dipakai untuk memisahkan "metode ini bagus di literatur" dari "metode ini bisa menyerang gate C, A, atau B pada data ini", dan untuk menandai tiga sumber bias yang nyata di proyek ini: sirkularitas label, pemilihan titik operasi setelah melihat hasil, serta penyebut FAR yang bukan kalender.

Riset pendahuluan: sequentialthinking, 6 pikiran (`mcp__sequentialthinking__sequentialthinking`, thoughtNumber 1..6, thoughtHistoryLength 6). Ringkas: (1) tiga skala skor R1-R6 tidak boleh dijahit tanpa rubrik, (2) skor kesesuaian dan status data wajib dipisah, (3) bobot diturunkan dari plan bagian 6 dan temuan D0 serta E0, bukan dari hasil yang diinginkan, (4) uji balik bobot: menurunkan bobot risiko akan menaikkan metode yang menang karena artefak, (5) pemilihan tiga finalis dari kegagalan gate yang paling umum, (6) pemisahan tegas antara ditolak dan ditunda.

---

## 0. Ringkasan keputusan

| Butir | Keputusan |
|---|---|
| Algoritma yang masuk matriks | 28 baris, 196 sel, 7 mode |
| Algoritma dengan skor prioritas di atas 2,0 | 7 dari 28 |
| Shortlist | 6 kandidat |
| Finalis pilot | 3 kandidat |
| Ditolak permanen | 13 algoritma atau keluarga algoritma |
| Ditunda | 5 algoritma atau keluarga algoritma |
| Temuan terpenting | pembatas utama bukan pilihan algoritma, melainkan portabilitas ambang antar unit (sebar FAR 119 kali pada vib, ledger R5-072) dan kualitas label (bit_wear, ledger R5-068) |

---

## 1. Cara membaca matriks

### 1.1 Rubrik skor kesesuaian sel (0 sampai 3)

| Skor | Arti |
|---|---|
| 0 | Tidak ada peran pada detektor itu: metode tidak menyentuh gate C, A, atau B di kelas tersebut |
| 1 | Peran pinggiran atau pembanding: bisa dipakai, tetapi tidak mengubah keputusan tier |
| 2 | Menyerang satu syarat gate pada detektor itu |
| 3 | Menyerang syarat gate yang justru menjadi kegagalan utama detektor itu |

Rubrik ini keputusan dokumen (KONVENSI, ledger E1-006). Ia tidak boleh dibaca sebagai hasil ukur.

### 1.2 Status data (dari D0, bukan taksiran)

| Status | Arti |
|---|---|
| `A` | ADA: kanal dan label tersedia, jumlah jendela terukur |
| `S` | SEBAGIAN: kanal atau label hanya ada di sebagian well, atau kanal penentu absen |
| `T` | TIDAK: prasyarat fisik tidak terpenuhi, misalnya laju sampel di bawah pita diagnostik |

### 1.3 Aturan angka

Setiap angka di tabel alasan menunjuk baris ledger. Angka yang tidak punya baris ledger tidak ditulis. Daftar baris baru untuk kartu ini ada di `docs/RND_PROVENANCE_LEDGER.md` bagian E1.

---

## 2. MATRIKS A: algoritma x 7 mode

Format sel: `skor/status`, contoh `2/A` berarti skor kesesuaian 2 dan data ADA.
Baris diurutkan menurut skor prioritas tertinggi algoritma tersebut (lihat bagian 5).

| Kode | Algoritma | Sumber | vib | ssi | shk | stuck | hyd | bit_wear | tool_wear |
|---|---|---|---|---|---|---|---|---|---|
| A10 | Conformal (kuantil lintas-well dan dalam-well) | R4 | 3/A | 2/S | 2/A | 2/S | 3/A | 0/T | 3/A |
| A19 | Uji KS dua sampel | R5 | 2/A | 1/S | 1/A | 1/S | 2/A | 1/T | 1/A |
| A16 | Page-Hinkley | R5 | 0/A | 0/S | 0/A | 1/S | 1/A | 2/S | 2/A |
| A17 | ADWIN | R5 | 0/A | 0/S | 0/A | 0/S | 0/A | 1/S | 2/A |
| A04 | SVM (RBF dan linear) sebagai pembanding murah | R3 | 2/A | 1/S | 1/A | 1/S | 1/A | 0/T | 3/A |
| A15 | CUSUM | R5 | 0/A | 0/S | 0/A | 1/S | 1/A | 2/S | 2/A |
| A06 | LightGBM atau XGBoost | R4 | 1/A | 2/S | 2/A | 2/S | 1/A | 0/T | 1/A |
| A01 | BGWO (binary GWO) | R1 | 2/A | 2/S | 2/A | 1/S | 1/A | 0/T | 1/A |
| A07 | CatBoost (lintas alat, LOTO) | R4 | 1/A | 1/S | 1/A | 2/S | 1/A | 0/T | 2/A |
| A05 | Matrix profile (pengganti DTW) | R3, R5 | 2/A | 1/S | 1/A | 1/S | 2/A | 0/T | 0/A |
| A09 | Kalibrasi isotonic atau Platt | R4 | 1/A | 1/S | 1/A | 1/S | 1/A | 0/T | 1/A |
| A08 | RF kontrak V9 (baseline yang berjalan) | R4 | 2/A | 2/S | 1/A | 1/S | 1/A | 0/T | 1/A |
| A02 | GWO atau WOA (tuning hyperparameter) | R1 | 1/A | 1/S | 1/A | 1/S | 2/A | 1/T | 1/A |
| A03 | SMA (Slime Mould Algorithm) | R1 | 1/A | 1/S | 1/A | 1/S | 1/A | 0/T | 1/A |
| A20 | Isolation Forest | R5 | 1/A | 1/S | 1/A | 1/S | 2/S | 2/T | 1/A |
| A11 | Cox proportional hazards | R2 | 0/A | 0/S | 0/A | 2/S | 1/A | 0/T | 0/A |
| A18 | BOCPD | R5 | 0/A | 0/S | 0/A | 0/S | 0/A | 1/S | 1/A |
| A26 | RSF dan DeepHit | R2 | 0/A | 0/S | 0/A | 1/S | 0/A | 0/T | 0/A |
| A12 | Markov chain | R2 | 0/A | 0/S | 0/A | 1/S | 0/A | 0/T | 1/A |
| A13 | HMM | R2 | 0/A | 0/S | 0/A | 1/S | 0/A | 0/T | 0/A |
| A14 | Monte Carlo (pelaporan CI) | R2 | 1/A | 1/S | 1/A | 1/S | 1/A | 1/T | 1/A |
| A21 | LOF | R5 | 0/A | 0/S | 0/A | 0/S | 1/S | 1/T | 0/A |
| A22 | Autoencoder | R5 | 0/A | 0/S | 0/A | 0/S | 0/S | 0/T | 0/A |
| A23 | One-Class SVM | R5 | 0/A | 0/S | 0/A | 0/S | 0/S | 0/T | 0/A |
| A24 | VMD, EMD, wavelet | R3, D0 | 0/T | 0/T | 0/T | 0/T | 0/T | 0/T | 0/T |
| A25 | kNN-DTW | R3 | 0/A | 0/S | 0/A | 0/S | 0/A | 0/T | 0/A |
| A27 | MCMC dan Bayesian network | R2 | 0/A | 0/S | 0/A | 0/S | 0/A | 0/T | 0/A |
| A28 | Metaheuristik lain (EO, Horse Herd, HBO, Honey Badger, HHO, EPO, SSA-Salp, SSA-Sparrow, WOA+GWO) | R1 | 0/A | 0/A | 0/A | 0/A | 0/A | 0/A | 0/A |

Bacaan cepat: sel `0/T` menandai prasyarat fisik yang tidak terpenuhi, misalnya laju sampel di bawah pita diagnostik, bukan penilaian bahwa metodenya jelek.

---

## 3. Alasan satu baris untuk tiap sel

Sel dengan skor 0 yang bukan karena prasyarat fisik dikelompokkan di akhir tiap mode, karena alasannya sama dan menuliskannya 12 kali tidak menambah informasi.

### 3.1 mode `vib`

| Kode | Algoritma | Skor | Data | Alasan satu baris |
|---|---|---|---|---|
| A10 | Conformal (kuantil lintas-well dan dalam-well) | 3 | ADA | sebar FAR ambang RF 119 kali antar well adalah sasaran langsung conformal per well (ledger R5-072) |
| A19 | Uji KS dua sampel | 2 | ADA | gerbang sebelum memakai ambang pinjaman, langsung menyentuh sebar 119 kali (ledger R5-072) |
| A04 | SVM (RBF dan linear) sebagai pembanding murah | 2 | ADA | median AUC 0,8245 pada satu split dan biaya RBF 7,99 detik, layak sebagai pembanding rule (ledger R3-35) |
| A06 | LightGBM atau XGBoost | 1 | ADA | R4 menyatakan RF dipertahankan; boosting hanya masuk bila menang di 75 persen fold LOWO (ledger R4-15) |
| A01 | BGWO (binary GWO) | 2 | ADA | 55 fitur kontrak memberi ruang seleksi nyata; ukuran baris 23.922 cukup untuk LOWO (ledger R4-01) |
| A07 | CatBoost (lintas alat, LOTO) | 1 | ADA | tidak ada variabel kategori alat pada kelas rig (ledger R4-01) |
| A05 | Matrix profile (pengganti DTW) | 2 | ADA | 0,00039 detik per query pada 3.000 titik, murah untuk menunjuk episode mirip (ledger R3-41) |
| A09 | Kalibrasi isotonic atau Platt | 1 | ADA | kalibrasi monoton, tidak mengubah AUPRC 0,9117 (ledger R4-15) |
| A08 | RF kontrak V9 (baseline yang berjalan) | 2 | ADA | AUPRC 0,9117 pada fold F-14 dengan prevalensi 0,5651, selisih +0,3466 (ledger R4-15) |
| A02 | GWO atau WOA (tuning hyperparameter) | 1 | ADA | ruang hyperparameter 4 sampai 6 dimensi terlalu kecil untuk memberi kenaikan tier (ledger R4-01) |
| A03 | SMA (Slime Mould Algorithm) | 1 | ADA | diusulkan R1 sebagai pemeriksaan silang BGWO, bukan jalur utama (ledger R4-01) |
| A20 | Isolation Forest | 1 | ADA | kelas sudah berlabel, detektor tanpa label tidak menambah gate (ledger R4-01) |
| A14 | Monte Carlo (pelaporan CI) | 1 | ADA | perannya pelaporan selang FAR, bukan menaikkan deteksi (ledger R4-01) |
| lainnya | 15 algoritma | 0 | campuran | tidak ada peran pada detektor ini; alasan per algoritma ada di bagian 8 dan di sel detektor lain |

### 3.2 mode `ssi`

| Kode | Algoritma | Skor | Data | Alasan satu baris |
|---|---|---|---|---|
| A10 | Conformal (kuantil lintas-well dan dalam-well) | 2 | SEBAGIAN | hybrid sudah memangkas FP 26 ke 7, conformal menjaga laju itu prospektif (ledger R4-26) |
| A19 | Uji KS dua sampel | 1 | SEBAGIAN | nodata membuat dua sampel tidak sebanding (ledger R4-26) |
| A04 | SVM (RBF dan linear) sebagai pembanding murah | 1 | SEBAGIAN | pembanding saja, tidak menyerang 62,3 persen nodata (ledger R4-26) |
| A06 | LightGBM atau XGBoost | 2 | SEBAGIAN | 36 ribu baris dan banyak missing adalah kondisi yang justru ditangani boosting modern (ledger R4-08) |
| A01 | BGWO (binary GWO) | 2 | SEBAGIAN | seleksi fitur bisa memangkas kolom yang 62,3 persen barisnya tanpa data CRPM (ledger R4-26) |
| A07 | CatBoost (lintas alat, LOTO) | 1 | SEBAGIAN | keunggulan kategorikal tidak terpakai, nodata tetap pembatas (ledger R4-26) |
| A05 | Matrix profile (pengganti DTW) | 1 | SEBAGIAN | kanal CRPM tidak lengkap, motif tidak bisa dihitung konsisten (ledger R4-26) |
| A09 | Kalibrasi isotonic atau Platt | 1 | SEBAGIAN | tidak menyentuh nodata, hanya membuat probabilitas bisa dibaca (ledger R4-26) |
| A08 | RF kontrak V9 (baseline yang berjalan) | 2 | SEBAGIAN | berjalan di 35.906 jendela, tetapi 62,3 persen tanpa CRPM (ledger R4-26) |
| A02 | GWO atau WOA (tuning hyperparameter) | 1 | SEBAGIAN | tuning tidak menyembuhkan 62,3 persen baris tanpa data CRPM (ledger R4-26) |
| A03 | SMA (Slime Mould Algorithm) | 1 | SEBAGIAN | sama seperti BGWO tetapi bukti domain lebih lemah (ledger R4-26) |
| A20 | Isolation Forest | 1 | SEBAGIAN | idem, dan nodata mendominasi (ledger R4-26) |
| A14 | Monte Carlo (pelaporan CI) | 1 | SEBAGIAN | idem, dan CI sudah bisa dihitung analitik (ledger R4-26) |
| lainnya | 15 algoritma | 0 | campuran | tidak ada peran pada detektor ini; alasan per algoritma ada di bagian 8 dan di sel detektor lain |

### 3.3 mode `shk`

| Kode | Algoritma | Skor | Data | Alasan satu baris |
|---|---|---|---|---|
| A10 | Conformal (kuantil lintas-well dan dalam-well) | 2 | ADA | rule sudah lolos FAR 0,67 sampai 6,6 di 7 dari 9 fold, conformal membuatnya dapat dijanjikan (ledger R3-51) |
| A19 | Uji KS dua sampel | 1 | ADA | rule sudah lolos FAR tanpa pinjaman ambang (ledger R3-51) |
| A04 | SVM (RBF dan linear) sebagai pembanding murah | 1 | ADA | pembanding di bawah rule yang sudah lolos FAR di 7 dari 9 fold (ledger R3-51) |
| A06 | LightGBM atau XGBoost | 2 | ADA | 56 ribu baris dan prevalensi 0,0355 memberi ruang bagi model berkapasitas lebih (ledger R4-29) |
| A01 | BGWO (binary GWO) | 2 | ADA | volume 56.495 baris dan fitur lebar, seleksi menurunkan dimensi tanpa kehilangan unit (ledger R4-09) |
| A07 | CatBoost (lintas alat, LOTO) | 1 | ADA | tidak ada kolom kategorikal yang menonjol (ledger R4-09) |
| A05 | Matrix profile (pengganti DTW) | 1 | ADA | kanal terkuantisasi 4 nilai unik membatasi motif yang bisa dibedakan (ledger R3-51) |
| A09 | Kalibrasi isotonic atau Platt | 1 | ADA | presisi rule sudah stabil, kalibrasi tidak menambah gate (ledger R3-51) |
| A08 | RF kontrak V9 (baseline yang berjalan) | 1 | ADA | CI memuat prevalensi di 7 dari 9 fold, jadi RF belum terbukti di atas no-skill (ledger R1-030) |
| A02 | GWO atau WOA (tuning hyperparameter) | 1 | ADA | tuning hanya menggeser titik operasi, bukan menutup CI yang memuat no-skill di 7 dari 9 fold (ledger R1-030) |
| A03 | SMA (Slime Mould Algorithm) | 1 | ADA | pemeriksaan silang hasil seleksi fitur (ledger R4-09) |
| A20 | Isolation Forest | 1 | ADA | idem (ledger R4-09) |
| A14 | Monte Carlo (pelaporan CI) | 1 | ADA | idem (ledger R4-09) |
| lainnya | 15 algoritma | 0 | campuran | tidak ada peran pada detektor ini; alasan per algoritma ada di bagian 8 dan di sel detektor lain |

### 3.4 mode `stuck`

| Kode | Algoritma | Skor | Data | Alasan satu baris |
|---|---|---|---|---|
| A10 | Conformal (kuantil lintas-well dan dalam-well) | 2 | SEBAGIAN | B1 0 sampai 0,115 adalah masalah daya deteksi, conformal hanya mengendalikan alarm (ledger R2-015) |
| A19 | Uji KS dua sampel | 1 | SEBAGIAN | 2 well terlalu sedikit untuk uji dua sampel yang kuat (ledger R4-10) |
| A16 | Page-Hinkley | 1 | SEBAGIAN | idem (ledger R4-10) |
| A04 | SVM (RBF dan linear) sebagai pembanding murah | 1 | SEBAGIAN | 2 well tidak cukup untuk melatih kernel dengan jujur (ledger R4-10) |
| A15 | CUSUM | 1 | SEBAGIAN | onset sudah punya detektor rule, CUSUM hanya menambah alarm (ledger R4-10) |
| A06 | LightGBM atau XGBoost | 2 | SEBAGIAN | 118.567 jendela dengan prevalensi 0,0167 adalah kasus imbalance yang jadi alasan utama boosting (ledger R4-29) |
| A01 | BGWO (binary GWO) | 1 | SEBAGIAN | hanya 5.555 jendela di 2 well, ruang seleksi lebih sempit dari jumlah fitur (ledger R4-10) |
| A07 | CatBoost (lintas alat, LOTO) | 2 | SEBAGIAN | imbalance ekstrem 0,0167 adalah target alami boosting (ledger R4-29) |
| A05 | Matrix profile (pengganti DTW) | 1 | SEBAGIAN | 2 well membatasi motif lintas unit (ledger R4-10) |
| A09 | Kalibrasi isotonic atau Platt | 1 | SEBAGIAN | jumlah positif per well kecil, syarat sampel kalibrasi kemungkinan gagal (ledger R4-10) |
| A08 | RF kontrak V9 (baseline yang berjalan) | 1 | SEBAGIAN | K-i hanya 2 well, K-ii B1 rendah (ledger R4-10) |
| A02 | GWO atau WOA (tuning hyperparameter) | 1 | SEBAGIAN | tuning tidak menambah well; cakupan tetap 2 fold (ledger R4-10) |
| A03 | SMA (Slime Mould Algorithm) | 1 | SEBAGIAN | cakupan 2 well membatasi manfaat apa pun dari tuning (ledger R4-10) |
| A20 | Isolation Forest | 1 | SEBAGIAN | idem (ledger R4-10) |
| A11 | Cox proportional hazards | 2 | SEBAGIAN | hanya K-ii yang punya onset; Cox diusulkan R2 sebagai pembanding TLead (ledger L-28) |
| A26 | RSF dan DeepHit | 1 | SEBAGIAN | event per well kecil dan horizon 10 menit, sehingga survival rakus data gugur (ledger L-28) |
| A12 | Markov chain | 1 | SEBAGIAN | median episode satu menit berarti memori hampir nol sehingga orde-1 tidak informatif (R2 bagian 3) |
| A13 | HMM | 1 | SEBAGIAN | state fisik tidak ada, jadi HMM hanya menghasilkan state yang kita karang (ledger R4-10) |
| A14 | Monte Carlo (pelaporan CI) | 1 | SEBAGIAN | idem (ledger R4-10) |
| lainnya | 9 algoritma | 0 | campuran | tidak ada peran pada detektor ini; alasan per algoritma ada di bagian 8 dan di sel detektor lain |

### 3.5 mode `hyd`

| Kode | Algoritma | Skor | Data | Alasan satu baris |
|---|---|---|---|---|
| A10 | Conformal (kuantil lintas-well dan dalam-well) | 3 | ADA | satu-satunya gerbang yang tersisa pada kandidat terkuat adalah FAR 14,6 sampai 58,4 (ledger E1-021) |
| A19 | Uji KS dua sampel | 2 | ADA | 9 well memberi bahan uji antar well yang memadai (ledger R1-032) |
| A16 | Page-Hinkley | 1 | ADA | idem (ledger R4-12) |
| A04 | SVM (RBF dan linear) sebagai pembanding murah | 1 | ADA | pembanding untuk hybrid, bukan pengganti aturan ambang (ledger R1-032) |
| A15 | CUSUM | 1 | ADA | hybrid aturan sudah menangani status (ledger R4-12) |
| A06 | LightGBM atau XGBoost | 1 | ADA | hybrid aturan sudah kuat, boosting hanya mengganti lapisan ranking (ledger R1-032) |
| A01 | BGWO (binary GWO) | 1 | ADA | 52.509 jendela, tetapi masalah hyd adalah ambang FAR bukan dimensi fitur (ledger R4-12) |
| A07 | CatBoost (lintas alat, LOTO) | 1 | ADA | sama seperti kelas status lain, tidak ada kategori alat (ledger R4-12) |
| A05 | Matrix profile (pengganti DTW) | 2 | ADA | dipakai R5 sebagai penunjuk potongan waktu untuk pemeriksaan manual (ledger R4-12) |
| A09 | Kalibrasi isotonic atau Platt | 1 | ADA | kalibrasi tidak menurunkan FAR yang jadi satu-satunya gerbang gagal (ledger R1-032) |
| A08 | RF kontrak V9 (baseline yang berjalan) | 1 | ADA | persistence dan hybrid sudah memenuhi C lebih lengkap dari RF (ledger R1-032) |
| A02 | GWO atau WOA (tuning hyperparameter) | 2 | ADA | ambang hybrid adalah inti masalah hyd, sehingga pencarian ambang terarah relevan (ledger R1-032) |
| A03 | SMA (Slime Mould Algorithm) | 1 | ADA | alternatif tuning ambang bila GWO gagal konvergen (ledger R4-12) |
| A20 | Isolation Forest | 2 | SEBAGIAN | K-ii tanpa label yang dapat dipercaya, triase adalah peran yang sah (ledger R5-067) |
| A11 | Cox proportional hazards | 1 | ADA | K-ii punya horizon 10 menit sehingga survival hampir tidak punya ruang (ledger L-28) |
| A14 | Monte Carlo (pelaporan CI) | 1 | ADA | idem (ledger R4-12) |
| A21 | LOF | 1 | SEBAGIAN | dijalankan sebagai pembanding, hasilnya jenuh menyala (ledger R5-067) |
| lainnya | 11 algoritma | 0 | campuran | tidak ada peran pada detektor ini; alasan per algoritma ada di bagian 8 dan di sel detektor lain |

### 3.6 mode `bit_wear`

| Kode | Algoritma | Skor | Data | Alasan satu baris |
|---|---|---|---|---|
| A19 | Uji KS dua sampel | 1 | TIDAK | 7 well USROP hanya 5 yang punya positif (ledger D0-756) |
| A16 | Page-Hinkley | 2 | SEBAGIAN | pembanding CUSUM untuk K-2 tanpa label (ledger D0-752) |
| A17 | ADWIN | 1 | SEBAGIAN | butuh baseline lebih pendek dari BOCPD, tetapi label belum ada (ledger D0-752) |
| A15 | CUSUM | 2 | SEBAGIAN | K-2 belum berlabel sehingga detektor tanpa label adalah satu-satunya jalan (ledger D0-752) |
| A02 | GWO atau WOA (tuning hyperparameter) | 1 | TIDAK | tanpa CI, presisi, dan FAR yang terukur, tuning tidak punya sasaran yang bisa dievaluasi (ledger R5-068) |
| A20 | Isolation Forest | 2 | TIDAK | K-2 belum berlabel, triase satu-satunya jalan (ledger D0-752) |
| A18 | BOCPD | 1 | SEBAGIAN | ditunda sampai baseline kontigu mencukupi (ledger D0-752) |
| A14 | Monte Carlo (pelaporan CI) | 1 | TIDAK | tanpa FAR terdefinisi, simulasi CI tidak punya besaran (ledger D0-752) |
| A21 | LOF | 1 | TIDAK | idem, jenuh (ledger D0-752) |
| lainnya | 19 algoritma | 0 | campuran | tidak ada peran pada detektor ini; alasan per algoritma ada di bagian 8 dan di sel detektor lain |

### 3.7 mode `tool_wear`

| Kode | Algoritma | Skor | Data | Alasan satu baris |
|---|---|---|---|---|
| A10 | Conformal (kuantil lintas-well dan dalam-well) | 3 | ADA | FP 1 sampai 3 per alat sudah terkalibrasi; conformal membuatnya janji bukan hasil satu run (ledger L-33) |
| A19 | Uji KS dua sampel | 1 | ADA | 4 alat terlalu sedikit untuk uji antar alat (ledger L-33) |
| A16 | Page-Hinkley | 2 | ADA | pembanding CUSUM yang lebih jujur pada data berautokorelasi (ledger L-33) |
| A17 | ADWIN | 2 | ADA | tidak menuntut baseline bersih panjang, cocok untuk run bengkel pendek (ledger L-33) |
| A04 | SVM (RBF dan linear) sebagai pembanding murah | 3 | ADA | 27 fitur tabular dan 469 jendela adalah bentuk paling cocok untuk SVM lintas alat (ledger D0-766) |
| A15 | CUSUM | 2 | ADA | perubahan regime per alat adalah definisi kerja CUSUM (ledger L-33) |
| A06 | LightGBM atau XGBoost | 1 | ADA | 469 jendela terlalu kecil untuk boosting yang lebih rakus data (ledger D0-766) |
| A01 | BGWO (binary GWO) | 1 | ADA | hanya 27 fitur dan 469 jendela sehingga seleksi tidak mendesak (ledger D0-766) |
| A07 | CatBoost (lintas alat, LOTO) | 2 | ADA | ada identitas alat T01 sampai T04 sehingga LOTO memakai keunggulan CatBoost (ledger D0-766) |
| A09 | Kalibrasi isotonic atau Platt | 1 | ADA | skor per alat sudah dipakai untuk kalibrasi ambang, bukan probabilitas (ledger L-33) |
| A08 | RF kontrak V9 (baseline yang berjalan) | 1 | ADA | FAR terkalibrasi lebih penting dari penggantian model (ledger L-33) |
| A02 | GWO atau WOA (tuning hyperparameter) | 1 | ADA | FAR sudah terkalibrasi per alat, ruang perbaikan tuning kecil (ledger L-33) |
| A03 | SMA (Slime Mould Algorithm) | 1 | ADA | ruang 27 fitur terlalu kecil untuk metaheuristik (ledger D0-766) |
| A20 | Isolation Forest | 1 | ADA | label konstan dalam run membuat triase tidak bisa dievaluasi (ledger L-33) |
| A18 | BOCPD | 1 | ADA | prior panjang rezim belum bisa diuji pada run pendek (ledger L-33) |
| A12 | Markov chain | 1 | ADA | dua kondisi run memberi transisi regime yang bisa dihitung (ledger D0-766) |
| A14 | Monte Carlo (pelaporan CI) | 1 | ADA | idem (ledger D0-766) |
| lainnya | 11 algoritma | 0 | campuran | tidak ada peran pada detektor ini; alasan per algoritma ada di bagian 8 dan di sel detektor lain |

---

## 4. MATRIKS B: lapisan evaluasi (R6) dan gate

R6 tidak memberi skor per mode, karena isinya metode evaluasi, bukan model prediksi. Karena itu R6 tidak dipaksa masuk sebagai baris matriks A: memasukkannya akan membuat kolom detektor berisi angka yang tidak bermakna. R6 dilaporkan sebagai matriks B dengan kolom gate.

| Metode | Gate C | Gate A | Gate B | Status pada data kita | Rujukan |
|---|---|---|---|---|---|
| Wilson (presisi) | ya, lebar CI | tidak | tidak | TERUKUR | R6 bagian 2.9 |
| Poisson eksak Garwood (rasio FAR) | tidak | ya | tidak | TERUKUR | R6 bagian 2.9 |
| Fisher eksak (dua well berbeda) | ya | tidak | tidak | TERUKUR | R6 bagian 2.9 |
| Uji tanda (arah per well) | ya | tidak | tidak | TERUKUR, n = 4, 7, 9 | R6 bagian 3.1 |
| Bootstrap blok per well | ya | ya | tidak | TERUKUR pada simulasi, data nyata butuh skor per jendela | R6 bagian 2.9 |
| DeLong | ya | tidak | tidak | BELUM TERUKUR, skor per jendela tidak disimpan | R6 bagian 2.9 |
| McNemar | tidak | tidak | ya | BELUM TERUKUR, hitungan berpasangan tidak ada | R6 bagian 2.9 |
| Holm dan BH | ya | ya | ya | TERUKUR | R6 bagian 2.9 |
| MDE rasio laju FAR | tidak | ya | tidak | TERUKUR, MDE pada rasio 1,40 | R6 bagian 3.2 |

Konsekuensi yang harus dibaca sebelum memilih finalis: dua uji yang paling sering diminta untuk klaim "algoritma X lebih baik", yaitu DeLong dan McNemar, tidak dapat dijalankan pada artefak yang ada. Artinya setiap klaim perbandingan antar model pada gelombang ini harus disandarkan pada uji tanda, Fisher, dan bootstrap, atau harus lebih dulu menyimpan skor per jendela.

---

## 5. Skor prioritas, bobot, dan alasan bobot

### 5.1 Bobot

| Komponen | Bobot | Alasan bobot |
|---|---|---|
| Potensi naik tier (0-3) | 0,50 | Plan bagian 6 menyatakan tier hanya naik bila C stabil, A FAR memadai, dan B beban wajar terpenuhi bersamaan. Metode yang tidak menyentuh salah satu syarat itu tidak punya nilai proyek, seberapa pun bagusnya di literatur. Bobot terbesar karena alasan ini, bukan karena selera. |
| Kelayakan data (0,25) | 0,25 | D0 menunjukkan blokir data bersifat mutlak dan tidak dapat diperbaiki algoritma apa pun: Nyquist 0,1667 Hz (ledger R3-02), STUCK_RT hanya di 4 dari 9 well, FlowOut absen. Blokir seperti ini membunuh kandidat lebih cepat daripada kelemahan metode. |
| Risiko (0,15, terbalik) | 0,15 | E0 menemukan 5 temuan Kritis di mana angka terlihat bagus padahal artefak: presisi rule yang tidak pernah menyala saat status belum aktif (K-1), lead time yang dikreditkan ke kejadian salah (K-2), dan kriteria "pernah menyala sekali" (K-3). Bobot ini menahan kandidat yang menang karena artefak. |
| Biaya (0,10, terbalik) | 0,10 | Biaya membatasi berapa varian yang bisa dicoba, bukan apakah metodenya sah. Pembatas biaya yang ekstrem sudah tertangkap di sel skor, misalnya kNN-DTW 137.374,35 jam (ledger R3-40). Memberi bobot besar akan menghukum dua kali. |

Rumus: skor = 0,50 x tier + 0,25 x data + 0,15 x risiko + 0,10 x biaya, dengan skala 0 sampai 3.
Gerbang: bila potensi tier pada detektor itu 0, skor dipaksa 0. Tanpa gerbang ini, metode pendukung seperti Monte Carlo menang karena dua komponen terbalik memberi lantai nilai, padahal kontribusinya ke tier nol. Gerbang dan koreksinya dicatat terbuka di ledger E1-005 dan E1-017.

Tiga hal yang perlu dinyatakan jujur:

1. Bobot dan skor komponen adalah KONVENSI rekayasa, bukan hasil ukur. Yang terukur adalah angka di kolom alasan; bobot hanya cara mengurutkan. Dokumen ini menyebutnya terbuka supaya bisa dibantah dengan argumen, bukan disembunyikan di balik angka desimal.
2. Skor komponen biaya untuk LightGBM dan XGBoost (1) adalah batas bawah, karena biaya latihnya BELUM TERUKUR (ledger E1-018). Kalau nanti biaya terukur murah, skornya naik dan peringkatnya berubah. Itu dinyatakan sekarang supaya tidak dibaca sebagai penilaian final.
3. Memilih enam kandidat lalu tiga finalis dari satu tabel berbobot adalah bentuk pemilihan setelah melihat hasil. Mitigasinya: kriteria finalis dikunci sebelum tabel dihitung, yaitu data ADA atau SEBAGIAN dan jalur eksplisit ke gate C, A, B. Semua finalis di bagian 7 memenuhi kriteria itu, dan kandidat yang skornya lebih tinggi tetapi tidak memenuhi kriteria dicatat sebagai bukan finalis beserta alasannya.

### 5.2 Peringkat per mode sasaran

| # | Kode | Algoritma | Mode sasaran | Tier | Data | Risiko | Biaya | Skor |
|---|---|---|---|---|---|---|---|---|
| 1 | A10 | Conformal (kuantil lintas-well dan dalam-well) | hyd | 3 | 3 | 2 | 3 | **2,85** |
| 2 | A19 | Uji KS dua sampel | vib | 2 | 3 | 3 | 3 | **2,50** |
| 3 | A16 | Page-Hinkley | tool_wear | 2 | 3 | 2 | 3 | **2,35** |
| 4 | A17 | ADWIN | tool_wear | 2 | 3 | 2 | 3 | **2,35** |
| 5 | A04 | SVM (RBF dan linear) sebagai pembanding murah | tool_wear | 2 | 3 | 2 | 2 | **2,25** |
| 6 | A15 | CUSUM | tool_wear | 2 | 3 | 1 | 3 | **2,20** |
| 7 | A06 | LightGBM atau XGBoost | shk | 2 | 3 | 2 | 1 | **2,15** |
| 8 | A01 | BGWO (binary GWO) | vib | 2 | 3 | 1 | 1 | **2,00** |
| 9 | A07 | CatBoost (lintas alat, LOTO) | tool_wear | 2 | 3 | 1 | 1 | **2,00** |
| 10 | A05 | Matrix profile (pengganti DTW) | vib | 1 | 3 | 3 | 2 | **1,90** |
| 11 | A09 | Kalibrasi isotonic atau Platt | hyd | 1 | 3 | 2 | 3 | **1,85** |
| 12 | A08 | RF kontrak V9 (baseline yang berjalan) | vib | 1 | 3 | 2 | 2 | **1,75** |
| 13 | A02 | GWO atau WOA (tuning hyperparameter) | hyd | 1 | 3 | 1 | 2 | **1,60** |
| 14 | A03 | SMA (Slime Mould Algorithm) | vib | 1 | 3 | 1 | 2 | **1,60** |
| 15 | A20 | Isolation Forest | hyd | 1 | 1 | 2 | 2 | **1,25** |
| 16 | A11 | Cox proportional hazards | stuck | 1 | 1 | 1 | 2 | **1,10** |
| 17 | A18 | BOCPD | bit_wear | 1 | 1 | 1 | 1 | **1,00** |
| 18 | A26 | RSF dan DeepHit | stuck | 1 | 1 | 1 | 1 | **1,00** |
| 19 | A12 | Markov chain | tool_wear | 0 | 3 | 0 | 3 | **0,00** |
| 20 | A13 | HMM | stuck | 0 | 1 | 0 | 2 | **0,00** |
| 21 | A14 | Monte Carlo (pelaporan CI) | hyd | 0 | 3 | 3 | 3 | **0,00** |
| 22 | A21 | LOF | hyd | 0 | 1 | 1 | 2 | **0,00** |
| 23 | A22 | Autoencoder | hyd | 0 | 1 | 0 | 1 | **0,00** |
| 24 | A23 | One-Class SVM | hyd | 0 | 1 | 0 | 2 | **0,00** |
| 25 | A24 | VMD, EMD, wavelet | vib | 0 | 0 | 0 | 0 | **0,00** |
| 26 | A25 | kNN-DTW | vib | 0 | 3 | 1 | 0 | **0,00** |
| 27 | A27 | MCMC dan Bayesian network | vib | 0 | 3 | 0 | 1 | **0,00** |
| 28 | A28 | Metaheuristik lain (EO, Horse Herd, HBO, Honey Badger, HHO, EPO, SSA-Salp, SSA-Sparrow, WOA+GWO) | vib | 0 | 3 | 1 | 1 | **0,00** |

Mode sasaran adalah detektor tempat algoritma itu direkomendasikan R1 sampai R6, bukan detektor dengan skor tertinggi. Aturan ini dipakai supaya algoritma tidak diberi panggung pada detektor yang jelas tidak membutuhkannya: tanpa aturan ini, Isolation Forest akan dinilai pada shk yang sudah berlabel dan tampak lebih baik daripada perannya yang sebenarnya, yaitu triase pada kelas tanpa label. Pemetaan mode sasaran ada di `scratch/rnd_e1/e1_build.py` konstanta `TARGET`.

Kolom tier, data, risiko, biaya adalah skor komponen 0 sampai 3. Kolom Skor adalah hasil rumus 5.1. Algoritma dengan skor 0 tidak muncul karena gerbang tier memaksanya ke 0.

---

## 6. SHORTLIST: 6 kandidat

Enam kandidat dipilih dari peringkat 5.2 dengan satu syarat tambahan: tiap kandidat harus punya detektor dengan data ADA atau SEBAGIAN dan satu jalur gate yang bisa ditunjuk. Nomor urut adalah peringkat skor.

| # | Kode | Kandidat | Detektor target | Skor | Kenapa masuk shortlist |
|---|---|---|---|---|---|
| 1 | A10 | Conformal (kuantil lintas-well dan dalam-well) | hyd | **2,85** | satu-satunya metode yang menyerang kegagalan C paling umum, yaitu portabilitas ambang; pada hyd satu-satunya gerbang tersisa adalah FAR |
| 2 | A19 | Uji KS dua sampel | vib | **2,50** | gerbang diagnosis sebelum meminjam ambang antar well; R5 menempatkannya sebagai prioritas kedua setelah CUSUM dan PH |
| 3 | A16 | Page-Hinkley | tool_wear | **2,35** | detektor perubahan level yang biayanya rendah dan interpretasinya bisa diaudit; satu paket dengan CUSUM |
| 4 | A06 | LightGBM atau XGBoost | shk | **2,15** | satu-satunya jalur yang bisa menaikkan daya deteksi pada kelas bervolume besar, dan biayanya belum pernah diukur |
| 5 | A04 | SVM (RBF dan linear) sebagai pembanding murah | tool_wear | **2,25** | pembanding murah yang bisa menandingi rule pada fitur tabular, khususnya pada tool_wear yang 27 fitur |
| 6 | A07 | CatBoost (lintas alat, LOTO) | tool_wear | **2,00** | keunggulan kategorikal alat pada LOTO, satu-satunya kelas dengan identitas alat eksplisit |

---

## 7. FINALIS: 3 kandidat pilot

Kriteria finalis dikunci sebelum tabel 5.2 dihitung: (a) data ADA atau SEBAGIAN, (b) ada jalur eksplisit ke gate C, A, dan B, (c) tiga finalis tidak menguji hal yang sama.

Tiga syarat yang berlaku untuk KETIGA finalis sebelum run dijalankan:

1. Pra-registrasi titik operasi ditulis lebih dulu, termasuk alpha, ambang, dan aturan penolakan. Tanpa ini, memilih titik operasi setelah melihat hasil adalah p-hacking yang tidak bisa dibedakan dari temuan.
2. Skor per jendela disimpan per fold per model. Saat ini skor itu tidak disimpan, sehingga DeLong dan McNemar tidak dapat dijalankan (R6 bagian 2.9), dan setiap klaim perbandingan antar model akan tetap berstatus hipotesis tanpa artefak ini.
3. FAR dilaporkan sebagai laju kalender beserta cakupan waktu teramati, bukan laju per menit teramati. Temuan Kritis E0 K-4 menunjukkan cakupan menit teramati hanya 1,46 sampai 71,7 persen, sehingga FAR yang dilaporkan tanpa cakupan menyesatkan ke arah optimistis.

### 7.1 Finalis 1: Conformal (kuantil lintas-well dan dalam-well) pada `hyd`

Peran pilot: Kalibrasi ambang per well secara prospektif (conformal V3).

- Skor prioritas 2,85 (tier 3, data 3, risiko 2, biaya 3).
- Status data: ADA. Alasan sel: satu-satunya gerbang yang tersisa pada kandidat terkuat adalah FAR 14,6 sampai 58,4 (ledger E1-021).
- Jalur ke gate C: hyd sudah memenuhi C paling lengkap di antara kelas status: CI persistence tidak memuat prevalensi di 0 dari 9 well (ledger R1-032). Klaim pilot tidak boleh melemahkan itu, jadi hasil per well dilaporkan utuh dan uji tanda dipakai dengan syarat 8 dari 9 well sepakat pada tingkat 0,05 (R6 bagian 3.1).
- Jalur ke gate A: satu-satunya gerbang yang kini gagal adalah FAR hybrid 14,6 sampai 58,4 per 24 jam terhadap gerbang 6. Alpha conformal dipilih supaya laju alarm yang dijanjikan berada di bawah 6, lalu FAR dilaporkan sebagai laju kalender dengan cakupan waktu (menjawab temuan Kritis E0 K-4).
- Jalur ke gate B: hybrid sudah memangkas FP dari 2.091 ke 927 (55,7 persen) secara konsisten di 9 dari 9 well. Target pilot adalah mempertahankan pemangkasan itu sambil menurunkan jumlah alarm yang harus diperiksa manusia per shift, bukan per menit.
- Kriteria berhenti: alpha yang dibutuhkan untuk mencapai FAR 6 ternyata menghasilkan nol alarm pada baseline, sehingga detektor tidak lagi berguna. Pada kondisi itu statusnya bukan gagal, melainkan bukti bahwa ambang tunggal tidak bisa melayani 9 well sekaligus, dan hasilnya dilaporkan sebagai temuan.

### 7.2 Finalis 2: Page-Hinkley pada `tool_wear`

Peran pilot: Page-Hinkley dan CUSUM dengan reset, terkalibrasi per alat.

- Skor prioritas 2,35 (tier 2, data 3, risiko 2, biaya 3).
- Status data: ADA. Alasan sel: pembanding CUSUM yang lebih jujur pada data berautokorelasi (ledger L-33).
- Jalur ke gate C: hanya ada 4 alat, dan uji tanda dengan 4 unit berdaya 0 pada semua tingkat konkordansi (R6 bagian 3.1). Karena itu klaim C untuk tool_wear tidak boleh memakai uji tanda: yang sah adalah LOTO 4 fold yang dilaporkan per alat, dan klaim lintas alat hanya dibuat bila keempatnya searah, bukan dari rata-rata.
- Jalur ke gate A: gate A relatif sudah terpenuhi: FP 1 sampai 3 per alat dengan ambang terkalibrasi (ledger L-33). Target pilot adalah menjaga FAR itu ketika ambang dipindah ke alat baru, yaitu menguji apakah kalibrasi bertahan di luar alat yang dipakai untuk mengalibrasi.
- Jalur ke gate B: masalah utama kelas ini bukan FAR melainkan beban pemeriksaan: presisi run 0,50 dengan 4 FP pada alat baru. Target pilot adalah menurunkan FP per shift tanpa mengorbankan TLead 1,8 kali yang sudah terukur.
- Kriteria berhenti: bila FP pada alat baru tidak turun setelah reset diaktifkan, kesimpulannya metode ini menangkap perubahan regime yang bukan keausan, dan itu dilaporkan sebagai batas klaim, bukan sebagai kegagalan alat.

### 7.3 Finalis 3: LightGBM atau XGBoost pada `shk`

Peran pilot: Boosting terkalibrasi (LightGBM atau XGBoost) pada kelas bervolume besar.

- Skor prioritas 2,15 (tier 2, data 3, risiko 2, biaya 1).
- Status data: ADA. Alasan sel: 56 ribu baris dan prevalensi 0,0355 memberi ruang bagi model berkapasitas lebih (ledger R4-29).
- Jalur ke gate C: shk punya 9 well, tetapi CI RF memuat prevalensi di 7 dari 9 fold (ledger R1-030). Target pilot adalah menutup CI itu, dan itu hanya bisa diklaim bila boosting menang di hampir semua well, karena uji tanda butuh 8 dari 9 sepakat dan daya baru 0,775 pada konkordansi 0,90 (R6 bagian 3.1).
- Jalur ke gate A: rule di kelas ini sudah lolos FAR 0,67 sampai 6,6 per 24 jam di 7 dari 9 fold (ledger R3-51). Karena itu kriteria gate A bersifat mempertahankan, bukan memperbaiki: boosting yang AUPRC-nya naik tetapi FAR-nya melewati 6 di lebih banyak fold dinyatakan gagal, walau AUPRC lebih tinggi.
- Jalur ke gate B: prevalensi 0,0355 (ledger R4-29) berarti pada 24 jam jumlah alarm yang bisa diterima manusia jauh lebih kecil dari jumlah jendela positif. Beban dilaporkan sebagai pemeriksaan per shift pada titik operasi yang dipatok, bukan sebagai presisi di titik operasi terbaik.
- Kriteria berhenti: bila biaya latih terukur melebihi anggaran run sehingga hanya satu fold yang bisa diselesaikan, hasilnya tidak boleh dilaporkan sebagai perbandingan, dan statusnya kembali BELUM TERUKUR.

### 7.4 Kandidat yang skornya lebih tinggi atau setara tetapi bukan finalis

| Kode | Skor | Alasan bukan finalis |
|---|---|---|
| A19 | 2,50 | skor 2,50 tetapi perannya gerbang diagnosis sebelum meminjam ambang, bukan detektor; gerbang tidak dipilotkan sebagai model |
| A04 | 2,25 | skor 2,25 tetapi R3 menyebutnya pembanding murah, bukan pengganti rule; menaikkan tier tidak berasal dari SVM |
| A07 | 2,00 | skor 2,00 dan bersaing langsung dengan A06 pada tujuan yang sama; dua finalis tidak boleh menguji hal yang sama |
| A15 | 2,20 | skor 2,20 dan satu paket dengan A16; CUSUM tanpa reset sudah terbukti menyala 52,293 sampai 60,000 menit tiap jam (ledger R5-032) |
| A17 | 2,35 | skor 2,35 tetapi belum dijalankan sama sekali pada data kita; masuk shortlist sebagai pembanding A16, bukan finalis |
| A01 | 2,00 | skor 2,00; R1 sendiri menyatakan pembatas sebenarnya adalah portabilitas ambang, bukan dimensi fitur |

---

## 8. Ditolak, ditunda, dan alasannya

### 8.1 Ditolak permanen (alasan fisik atau biaya, bukan selera)

| Algoritma | Alasan penolakan | Bukti |
|---|---|---|
| VMD, EMD, wavelet | laju sampel tertinggi 0,3333 Hz memberi Nyquist 0,1667 Hz, sementara pita diagnostik bantalan berada pada orde ratusan Hz; 105 percobaan VMD dijalankan dan 75 gagal | ledger R3-02, R3-29, R3-30 |
| kNN-DTW | biaya 134,01 sampai 137.374,35 jam per klasifikasi penuh | ledger R3-40 |
| EO dan Horse Herd | nol bukti domain fault diagnosis, getaran, pengeboran, atau PdM setelah pencarian khusus | R1 bagian 4.3 |
| HBO (Heap-Based) | bukti diagnosis hanya tersedia dalam bentuk hibrida dengan GWO sehingga tidak bisa dipisahkan | R1 bagian 4.3 |
| HHO | risiko implementasi tertinggi, tujuh fase, tanpa keunggulan yang bisa dibuktikan pada ruang 4 sampai 6 dimensi | R1 bagian 4.3 |
| EPO dan SSA-Salp | hanya mendukung peran seleksi fitur, dan peran itu sudah ditempati BGWO dengan bukti lebih kuat | R1 bagian 4.3 |
| SSA-Sparrow | bukti berpusat pada jaringan mendalam dan VMD, sedangkan VMD sudah ditolak | R1 bagian 4.3 |
| Honey Badger | peran identik GWO dan WOA tanpa keunggulan terukur | R1 bagian 4.3 |
| Autoencoder | dijalankan sebagai pembanding, hasilnya jenuh: recall 1,0 dengan 96 persen menit menyala | ledger R5-067 |
| One-Class SVM | laju alarm 6,65 kali parameter, tidak layak dipakai menetapkan laju alarm | ledger R5-045 |
| LOF | dijalankan sebagai pembanding, jenuh menyala seperti autoencoder | ledger R5-067 |
| MCMC dan Bayesian network | prior dan DAG belum ada, sehingga model menjelaskan prior kita, bukan data | R2 bagian 10 |
| RSF dan DeepHit | event per well kecil dan horizon hanya 10 menit | ledger L-28 |

### 8.2 Ditunda (alasan keadaan, bisa berubah)

| Algoritma | Alasan penundaan | Syarat pencairan |
|---|---|---|
| BOCPD | butuh baseline kontinu yang jauh lebih panjang dari yang tersedia | baseline kontigu memadai per well (R5 bagian 6) |
| ADWIN | belum dijalankan sama sekali pada data kita | satu run pembanding pada tool_wear dengan laju alarm terukur |
| Cox | relevan hanya untuk K-ii, dan survival tidak otomatis memperbaiki lead time | pra-registrasi TLead dan uji asumsi proportional hazards |
| Markov chain dan HMM | median episode 1,0 menit membuat memori hampir nol; state fisik tidak ada | uji orde Markov dijalankan dan label state fisik tersedia |
| Monte Carlo | perannya pelaporan selang, bukan menaikkan deteksi | dipakai bersama finalis, bukan sebagai finalis |

### 8.3 Yang ditolak sebagai rujukan, bukan sebagai algoritma

DOI `10.1214/18-AOS1801` yang lazim dipakai untuk conformalized quantile regression diperiksa pada run ini dan ternyata menunjuk Chen 2020 tentang inferensi parameter pada stochastic gradient descent, bukan Romano dan rekan. Karena itu DOI tersebut tidak dipakai. Yang dipakai untuk conformal adalah Vovk 2005 (DOI 10.1007/b106715, terverifikasi dua lapis) dan arXiv 1905.03222 yang judulnya cocok.

---

## 9. Yang belum terukur dan belum terverifikasi

Daftar ini bagian dari hasil, bukan lampiran. Semua butir di bawah tidak dipakai sebagai dasar rekomendasi di bagian 6 dan 7.

1. BELUM TERUKUR: biaya latih dan AUPRC LightGBM, XGBoost, CatBoost pada data kita. Run pembanding R4 tidak selesai dalam anggaran waktu (ledger E1-018).
2. BELUM TERUKUR: jumlah sampel kalibrasi minimum yang memadai. Yang ada hanya ukuran himpunan (1.989 sampai 10.903 baris per well pada kelas vib, ledger R4-01), bukan hasil uji kelayakan.
3. BELUM TERUKUR: tiga varian ambang conformal (V1 kuantil-hindsight, V2 lintas-well, V3 dalam-well prospektif) dan selisih FAR empiris terhadap alpha. Belum ada satu pun baris yang dieksekusi.
4. BELUM TERUKUR: DeLong dan McNemar pada data nyata, karena skor per jendela dan hitungan berpasangan tidak disimpan.
5. BELUM TERUKUR: manfaat matrix profile pada kanal VIBLAT. Biaya per query terukur, manfaatnya tidak.
6. BELUM TERVERIFIKASI: teks penuh 10 dari 11 rujukan R5 tidak terbaca dari host ini karena blokir penerbit (403 dan 202). Rekaman Crossref cocok, isi tidak dibaca.
7. BELUM TERVERIFIKASI: label bit_wear K-2. Pra-registrasinya belum terbit, sehingga status datanya SEBAGIAN dan finalis tidak dibangun di atasnya.
8. BELUM TERVERIFIKASI: FAR bit_wear dalam satuan 24 jam, karena barisnya grid kedalaman 0,015 m (temuan E0 S-6). Angka FAR kelas ini tidak dipakai di dokumen ini.
9. BELUM TERUKUR: kestabilan lintas seed. Seluruh run memakai SEED = 42.
10. Penilaian skor komponen (tier, risiko, biaya) adalah KONVENSI, bukan pengukuran. Yang terukur hanya angka di kolom alasan.

---

## 10. Rujukan

Semua DOI diperiksa pada 2026-10-27 dengan dua lapis: resolusi `https://doi.org/<doi>` tanpa mengikuti redirect, dan metadata `https://api.crossref.org/works/<doi>`. Berkas hasil: `scratch/rnd_e1/doi_check.json`, perintah `python3 scratch/rnd_e1/doi_check.py`.

| # | Penulis pertama | Tahun | Judul | DOI atau URL | doi.org | Crossref | Dipakai untuk |
|---|---|---|---|---|---|---|---|
| 1 | Vovk | 2005 | Algorithmic Learning in a Random World | 10.1007/b106715 | 302 | 200 | dasar conformal prediction (finalis 1) |
| 2 | Niculescu-Mizil | 2005 | Predicting good probabilities with supervised learning | 10.1145/1102351.1102430 | 302 | 200 | dasar kalibrasi, bukan dasar angka |
| 3 | Chen | 2016 | XGBoost: A Scalable Tree Boosting System | 10.1145/2939672.2939785 | 302 | 200 | keluarga boosting (finalis 3) |
| 4 | Liu | 2008 | Isolation Forest | 10.1109/ICDM.2008.17 | 302 | 200 | detektor tanpa label pada kelas tanpa anotasi |
| 5 | Page | 1954 | Continuous Inspection Schemes | 10.1093/biomet/41.1-2.100 | 302 | 200 | dasar CUSUM (finalis 2) |
| 6 | DeLong | 1988 | Comparing the Areas under Two or More Correlated ROC Curves | 10.2307/2531595 | 302 | 200 | uji pembanding AUC, belum dapat dijalankan |
| 7 | Teale | 1965 | The concept of specific energy in rock drilling | 10.1016/0148-9062(65)90022-7 | 302 | 200 | konteks kanal mekanis, bukan dasar skor |
| 8 | Ke | 2017 | LightGBM: A Highly Efficient Gradient Boosting Decision Tree | https://papers.nips.cc/paper_files/paper/2017/hash/6449f44a102fde848669bdd9eb6b76fa-Abstract.html | URL | 200 | keluarga boosting (finalis 3) |
| 9 | Romano | 2019 | Conformalized Quantile Regression | https://arxiv.org/abs/1905.03222 | URL | 200 | varian conformal untuk regresi kuantil |
| 10 | Prokhorenkova | 2017 | CatBoost: unbiased boosting with categorical features | https://arxiv.org/abs/1706.09516 | URL | 200 | LOTO pada tool_wear |
| 11 | Angelopoulos | 2021 | A Gentle Introduction to Conformal Prediction | https://arxiv.org/abs/2107.07511 | URL | 200 | definisi cakupan conformal |

Catatan kejujuran atas tabel ini: tujuh rujukan pertama terverifikasi pada lapis registrasi (doi.org) dan lapis metadata (Crossref), masing-masing 302 dan 200. Empat rujukan terakhir adalah arXiv dan halaman prosiding, jadi tidak punya DOI; yang diverifikasi adalah URL terbuka dengan judul halaman yang cocok, bukan DOI. Isi penuh sebagian rujukan tidak dibaca karena blokir penerbit, dan itu tidak dipakai sebagai dasar angka.

---

## Ringkasan 5 baris

1. Matriks 28 algoritma x 7 mode berisi 196 sel, dan 7 algoritma punya skor prioritas di atas 2,0 dari skala 3.
2. Peringkat teratas bukan model yang lebih canggih, melainkan metode yang menyerang portabilitas ambang: conformal per well pada hyd dengan skor 2,85, disusul uji KS dan Page-Hinkley.
3. Tiga finalis pilot adalah kalibrasi ambang prospektif (hyd), Page-Hinkley dan CUSUM dengan reset (tool_wear), serta boosting terkalibrasi (shk, ssi, stuck K-ii); ketiganya punya data ADA atau SEBAGIAN dan jalur gate C, A, B yang bisa ditunjuk.
4. Sebanyak 13 algoritma atau keluarga algoritma ditolak permanen dengan alasan fisik atau biaya, 5 ditunda karena keadaan, dan satu DOI conformal populer ditolak karena menunjuk makalah lain.
5. Yang paling menghambat bukan pilihan algoritma: FAR belum dilaporkan sebagai laju kalender (temuan E0 K-4) dan skor per jendela tidak disimpan, sehingga DeLong dan McNemar belum bisa dijalankan.

### Daftar yang belum terverifikasi

- Biaya latih dan AUPRC LightGBM, XGBoost, CatBoost pada data kita.
- Jumlah sampel kalibrasi minimum yang memadai.
- FAR empiris tiga varian conformal.
- DeLong dan McNemar pada data nyata.
- Manfaat matrix profile pada kanal VIBLAT.
- Teks penuh 10 dari 11 rujukan R5 (blokir penerbit).
- Label bit_wear K-2 (pra-registrasi belum terbit).
- FAR bit_wear dalam satuan 24 jam.
- Kestabilan lintas seed selain 42.
