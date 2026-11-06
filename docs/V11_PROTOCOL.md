# V11-PM0: PROTOKOL PERTANDINGAN PROPOSAL (DIKUNCI SEBELUM HASIL DILIHAT)

Task: `t_63025a46` [Project Manager] · Board: `capstone-v11-vs` · Tanggal: 2026-10-15 (WIB)
Peran: menyusun protokol pertandingan sebelum penilaian, yaitu anti-shopping.
Status: **RUBRIK DIKUNCI**. Seluruh bobot, definisi menang, checklist angka, dan instrumen
Evaluasi User.txt di bawah ini berlaku mengikat untuk semua penilai. Perubahan setelah skor
dibuka = pelanggaran protokol.

> Riset pendahuluan: `scientific-critical-thinking`: rubrik memisahkan data (angka primer) dari
> interpretasi (kedalaman teknis); setiap kriteria punya falsifier; kekuatan bukti per angka
> diberi status (executed / DIDUKUNG) supaya tingkat kepastian tidak melebihi bukti.
> Riset pendahuluan: `verification-mandatory`: seluruh angka checklist diverifikasi dengan
> eksekusi nyata (modul REGISTRY dijalankan, hitung baris dari disk, baca JSON) sebelum ditulis;
> bagian "belum diverifikasi" ditulis eksplisit di §9.
> Riset pendahuluan: `statistical-analysis`: bobot kriteria akurasi dijaga paling berat (30)
> sejajar kedalaman teknis; menang mensyaratkan tidak kalah pada akurasi, persis seperti larangan
> "signifikan tapi tidak praktis"; angka kampanye dinilai per kampanye (V6/V8/V9), tidak
> dirata-ratakan.
> Riset pendahuluan: `sequentialthinking` (sequ-mcp, 4 pikiran, 4/4 sukses): inventaris bahan
> primer → konstruksi bobot 100 eksak → pemetaan checklist 30 angka beserta status verifikasi →
> keputusan aturan menang/seri/anonimisasi.

---

## 0. PETA KANDIDAT (label; identitas dirahasiakan untuk penilai paruh-atas)

| Label | File .md | File .ipynb (pasangan wajib) |
|---|---|---|
| Kandidat 1 | `/mnt/d/Capstone 1(v2)/docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.v3_arsip.md` | `/mnt/d/Capstone 1(v2)/docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.v3_arsip.ipynb` |
| Kandidat 2 | `/mnt/d/Capstone 1(v2)/docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md` | `/mnt/d/Capstone 1(v2)/docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.ipynb` |

Pemetaan di atas **hanya untuk arsip protokol dan PM-FINAL**. Dokumen penilaian paruh-atas
(penulis bab, auditor klaim) cukup memakai "kandidat 1" dan "kandidat 2" dengan path lengkap
sebagai penanda opaque.

---

## 1. ATURAN ANONIMISASI & ANTI-BIAS

1. Penilai paruh-atas **dilarang menyimpulkan identitas versi** (baru/lama, V10/V3, hasil iterasi
   berapa) dari isi dokumen, nama file, ukuran file, jumlah baris, jumlah cell, mtime, atau
   kutipan dokumen lain.
2. Path file ditulis lengkap di setiap lembar skor supaya bisa dicek ulang, tetapi path diperlakukan
   sebagai **kode kandidat**, bukan petunjuk versi. Kata "arsip" di dalam path tidak boleh
   ditafsirkan sebagai penanda kualitas.
3. Dilarang memakai mtime, ukuran byte, atau jumlah baris sebagai argumen penilaian. Angka-angka
   itu hanya boleh muncul sebagai fakta mekanis pada kriteria 4c (kesesuaian md dengan ipynb).
4. Penilai paruh-atas **dilarang menulis kesimpulan menang/kalah**. Output paruh-atas = lembar
   skor per kandidat + catatan bukti, tanpa perbandingan akhir.
5. Hanya **PM-FINAL** yang membandingkan skor, membuka pemetaan K1/K2, dan menetapkan pemenang
   memakai §3.
6. Jika penilai menyadari sudah mengetahui identitas salah satu kandidat, hal itu dicatat di lembar
   skor ("bias disclosure") dan keputusan akhir tetap berpatokan pada rubrik tertulis, bukan
   ingatan.

---

## 2. RUBRIK SKOR PM-0 (TOTAL EKSAK 100 POIN)

### 2.1 Kriteria 1: Kedalaman teknis = 30 poin

| Sub | Sub-kriteria | Poin | Cara menilai |
|---|---|---|---|
| 1a | Rumus/definisi operasional per engine dan per head (statistik, ML, rule, hibrida) | 10 | 10 = seluruh keluarga metode punya rumus eksak (mis. median/MAD per bin qcut, z-score, SSE 1-split, RF kontrak); 6-9 = sebagian head tanpa rumus; 1-5 = minim; 0 = tanpa rumus sama sekali |
| 1b | Labeling per kelas + konstruksi label onset + anti-sirkularitas (kanal pembentuk label dilarang jadi fitur) | 7 | 7 = labeling lengkap + asersi anti-sirkular; 4-6 = ada tapi celah; 1-3 = dangkal; 0 = tidak ada |
| 1c | Workflow hybrid: bagaimana rule + statistik + ML dirangkai + pengaruh antar-komponen (konfirmasi dua langkah, pemangkasan FP, beban cek) | 7 | 7 = workflow + interaksi dijelaskan berbukti; 4-6 = workflow ada tanpa interaksi; 1-3 = disebut tanpa mekanisme; 0 = tidak ada |
| 1d | Bukti per klaim: setiap klaim menaut bukti (angka JSON/EVAL, sitasi, eksekusi kode) | 6 | 6 = semua klaim berbukti; 3-5 = sebagian; 1-2 = mayoritas klaim tanpa bukti; 0 = tanpa bukti |

### 2.2 Kriteria 2: Akurasi terhadap primer = 30 poin

| Sub | Sub-kriteria | Poin | Cara menilai |
|---|---|---|---|
| 2a | Checklist 30 angka kunci (§4): muncul di dokumen kandidat DAN cocok 1:1 dengan sumber primer | 18 | Skor = 18 × (jumlah item cocok / 30). Item yang **tidak muncul** di dokumen kandidat dihitung **tidak cocok** (checklist = angka kunci yang wajib ditanggung jawabkan, berlaku sama untuk kedua kandidat). Angka yang muncul tapi salah = tidak cocok |
| 2b | Angka lain di luar checklist yang dikutip dapat ditelusuri 1:1 ke primer (JSON scratch, REGISTRY kode, dokumen V6/V7/V8/V9/V10, file data) | 6 | 6 = semua dapat ditelusuri; 4-5 = satu dua gagal; 2-3 = banyak gagal; 0 = mayoritas tidak dapat ditelusuri |
| 2c | Nihil angka karangan (klaim tak terbukti = nol pada sub-kriteria ini) | 6 | 6 = nol angka tanpa sumber; setiap angka karangan yang terbukti mengurangi 2 poin sampai nol. "Belum terukur / belum tersedia" yang ditulis jujur **bukan** angka karangan |

### 2.3 Kriteria 3: Kepatuhan Evaluasi User.txt = 25 poin

| Sub | Sub-kriteria (poin a-e, lihat §5) | Poin | Cara menilai |
|---|---|---|---|
| 3a | Lapisan A/B/C diterapkan per tugas (a) | 6 | 6 = ketiga lapisan ada dan dipakai konsisten; 3-5 = dua lapisan; 1-2 = satu; 0 = tidak ada |
| 3b | Baseline relevan per tugas, bukan satu baseline universal (b) | 5 | 5 = tiap tugas punya baseline yang relevan dengannya; 2-4 = sebagian; 0 = satu baseline universal |
| 3c | Jenis tugas dibedakan: deteksi anomali, deteksi kondisi, diagnosis, prediksi kejadian mendatang (c) | 5 | 5 = dibedakan tegas (label & baseline berbeda per jenis); 2-4 = dibedakan sebagian; 0 = dicampur |
| 3d | Kemampuan + batas + kekuatan bukti per engine, tanpa vonis biner pada tingkat alat; "belum terukur" dipisah dari "gagal" (d) | 6 | 6 = ketiganya ada untuk semua engine; 3-5 = sebagian; 0 = ada vonis biner LULUS/GAGAL pada tingkat alat |
| 3e | Nilai dinilai pada tingkat alat predictive maintenance, bukan jumlah model ML yang lolos gate (e) | 3 | 3 = ada sintesis tingkat alat; 1-2 = parsial; 0 = tidak ada |

### 2.4 Kriteria 4: Struktur & keterbacaan = 15 poin

| Sub | Sub-kriteria | Poin | Cara menilai |
|---|---|---|---|
| 4a | Outline jelas (hierarki bab/seksi, tiap bab punya tujuan yang terlihat) | 4 | 4 = jelas; 2-3 = cukup; 1 = rancu; 0 = tanpa struktur |
| 4b | Penjelasan tegas 7 engine / 11 klaim / 27 head (arti ketiganya + hubungan berjenjang) | 4 | 4 = tegas dan konsisten; 2-3 = ada tapi rancu di tempat; 0 = salah atau tidak ada |
| 4c | Konsistensi paket md = ipynb (§6): isi kedua format sama substantif | 4 | 4 = lolos cek mekanis; 0 = ada selisih substantif (angka/klaim berbeda) yang terbukti |
| 4d | Aturan em-dash (§7): tidak dipakai sebagai penghubung klausa sembarangan | 3 | 3 = nol pelanggaran; 1,5 = 1-3 pelanggaran; 0 = 4 pelanggaran atau lebih |

### 2.5 Verifikasi aritmetika bobot

30 + 30 + 25 + 15 = **100**.
1a-1d: 10+7+7+6 = 30. 2a-2c: 18+6+6 = 30. 3a-3e: 6+5+5+6+3 = 25. 4a-4d: 4+4+4+3 = 15.

---

## 3. DEFINISI MENANG DAN ATURAN SERI

**MENANG.** Kandidat X menang bila **kedua** syarat terpenuhi:
1. X unggul poin pada **mayoritas kriteria**, yaitu unggul di minimal 3 dari 4 kriteria
   (kriteria 1, 2, 3, 4); dan
2. X **tidak kalah** pada kriteria 2 (akurasi terhadap primer):
   skor_2(X) >= skor_2(Y).

**SERI.** Bila tidak ada kandidat yang memenuhi kedua syarat di atas, hasil pertandingan =
SERI. Ketentuan lanjutan:
- Seri adalah hasil **final**. PM-FINAL dilarang menambah kriteria, mengubah bobot, atau membuat
  tiebreaker baru setelah skor dibuka (itulah inti anti-shopping).
- Selisih total poin **bukan** penentu menang. Total poin hanya pelengkap laporan; penentu tetap
  syarat mayoritas kriteria + tidak kalah di akurasi.
- Jika kriteria 2 imbang tapi syarat 1 terpenuhi oleh satu kandidat, kandidat itu menang.
- Jika syarat 1 terpenuhi oleh kedua kandidat secara bersamaan (mustahil menurut definisi
  mayoritas, tetapi dicatat jika terjadi akibat skor imbang), hasil = SERI.

**Lembar skor wajib** memuat, per kandidat: skor tiap sub-kriteria (2.1-2.4), jumlah per kriteria,
jumlah total, dan daftar bukti per sub-kriteria. Format JSON disimpan di scratch sebelum PM-FINAL
membuka pemetaan.

---

## 4. CHECKLIST 30 ANGKA KUNCI (WAJIB DITELUSURI AUD-CLAIM)

Kolom "verif PM0" = status verifikasi oleh PM0 pada 2026-10-15. `executed` = dihitung/dijalankan
langsung di sesi ini dan disimpan ke JSON scratch; `DIDUKUNG` = angka ada di dokumen primer yang
dibaca, tetapi belum dihitung ulang oleh PM0; AUD-CLAIM tetap wajib menelusuri ulang per kandidat.

Sumber primer PM0 (JSON scratch):
- `~/.hermes/kanban/boards/capstone-v11-vs/workspaces/t_63025a46/scratch_registry_facts.json`
- `~/.hermes/kanban/boards/capstone-v11-vs/workspaces/t_63025a46/scratch_primary_recount.json`

| # | Angka kunci (bisa muncul dengan format pemisah ribuan berbeda) | Sumber primer | Verif PM0 |
|---|---|---|---|
| 1 | 7 engine: vib, ssi, shk, stuck, hyd, bit_wear, tool_wear | eksekusi REGISTRY `code/v9_i1_pipeline.py` | executed |
| 2 | 11 klaim = 3 engine x 1 + 4 engine x 2 | REGISTRY `klaim_tugas` | executed |
| 3 | 27 head, sebaran 4+4+4+6+4+2+3 | eksekusi REGISTRY | executed |
| 4 | Rekap tier: PERINGATAN-BERPENGAWAS 12, TREN 13, BELUM LAYAK PAKAI 2 | eksekusi REGISTRY | executed |
| 5 | Rekap lapisan: L0 5, L1 11, L2 9, L3 2 | eksekusi REGISTRY | executed |
| 6 | AUTO_CRITICAL_SLOTS = 0 (tidak ada slot alarm otomatis) | eksekusi REGISTRY | executed |
| 7 | Ambang vib: VIBLAT_RT >= 32,17405 ft/s2 | REGISTRY `klaim_tugas` vib | executed |
| 8 | stuck onset 0->1 dengan H = 10 menit | REGISTRY `klaim_tugas` stuck | executed |
| 9 | hyd K-i: residu SPPA dengan abs(z) > 2 | REGISTRY `klaim_tugas` hyd | executed |
| 10 | seed 42 (kontrak RF) | REGISTRY `SEED` + JSON `scratch/v9_e_ml/*_RESULTS.json` | executed |
| 11 | USROP_labeled 198.928 baris data / 18 kolom | `wc -l` + header `data/USROP_labeled.csv` | executed |
| 12 | labels_curated_v2: 884 kejadian; bha 571/263/50 (uncertain/no/yes) | `data/volve/labels_curated_v2_log.json` | executed |
| 13 | 6 dataset latih total 292.954 baris (23.922+35.906+56.495+5.555+52.509+118.567) | hitung ulang `scratch/v9_d1/datasets/*.csv.gz` | executed |
| 14 | 37 fold LOWO (4+9+9+2+9+4) | `scratch/v9_d1/lowo_*.json` | executed |
| 15 | n_features 55 (11 kanal x 5 statistik) | `scratch/v9_e_ml/*_RESULTS.json` | executed |
| 16 | 26 fold kampanye ML (vib 4 + ssi 9 + shk 9 + stuck_k2 4) | jumlah `folds` JSON v9_e_ml | executed |
| 17 | tool_wear 469 jendela / 27 fitur | `wc -l scratch/v6_e1/toolwear_windows.csv` | executed (baris); 27 fitur DIDUKUNG |
| 18 | TSPP 52.905 baris dari 4 file TSPP1..TSPP4.csv | hitung ulang per file `data/bo_tspp/TSPP{1..4}.csv` | executed (21.120+8.499+12.533+10.753) |
| 19 | WITSML tiga jenjang: folder 10 CSV 9.935.698 baris; pipeline V9 9 CSV; parser V3 8 CSV 7.080.457 | `wc -l` 10 CSV `data/volve/witsml_parsed/`; daftar FILES `code/v9_d1_01_bins.py` | executed (10 CSV & 9.935.698; 8 CSV = 9.935.698-773.674-2.081.567) |
| 20 | XML per jenis: tubular 192, bhaRun 161, trajectory 63, wbGeometry 27, mudLog 8 | hitung berbasis path `data/volve/witsml_raw/` | executed |
| 21 | 409 formation picks di 35 wellbore | parse `Well_picks_Volve_v1.dat` (557 baris - komentar - header - pemisah) | executed (409 baris data; 35 blok wellbore) |
| 22 | time.csv F-9A 419.747 baris data / 239 kolom | isi zip `data/volve/external/kaggle/kaggle_volve_witsml_F9A.zip` | executed (baris: 419.748 termasuk header di dalam zip); 239 kolom DIDUKUNG |
| 23 | hyd K-i hybrid: FAR 14,6-58,4; FP 2091->927 (-55,7%) di 9/9 fold | `docs/V9_EVAL_C_LAYERC.md` baris 95/177 | DIDUKUNG |
| 24 | ssi hybrid: FP 26->7 (-73,1%), hybrid <= rule di 7/7 fold layak | `docs/V9_EVAL_C_LAYERC.md` baris 91/133 | DIDUKUNG |
| 25 | stuck E3: RF AUPRC 0,326-0,331 < canary 0,410 | `docs/V9_R1_JUSTIFICATION.md` baris 144 | DIDUKUNG |
| 26 | tool_wear K-i: change-point 8/8 run; precision 0,50; FP 1-3/alat; TLead 20-36 detik; tes artefak termal 0/8 | `docs/V9_E_STAT_ENGINE.md`, `docs/V9_EVAL_C_LAYERC.md` (rekap V10_EVAL_BAB baris 113) | DIDUKUNG |
| 27 | hyd K-ii: q95 P=R=0 (0 TP, FP 177); sign-flip 6.377/8.107 = 78,7% jendela; CI fisher memuat prevalensi | `docs/V9_EVAL_C_LAYERC.md` baris 96/186; rehit JSON di `docs/V9_A1_AUDIT.md` baris 80 | DIDUKUNG |
| 28 | canary 3-RMS AUPRC 0,516-0,612 (1,19x); vib AUPRC 0,441-0,912; stuck TLead persistence-EVENT 4,5-8,5 (median 7,0) | `docs/V8_E_tool_wear_CAPABILITY.md`; `docs/V9_EVAL_A_LAYERA.md` baris 54/74; `docs/V9_EVAL_B_LAYERB.md` baris 101/190 | DIDUKUNG |
| 29 | Rekap tier V8: 0 alarm + 3 peringatan + 2 bersyarat + 2 tren = 7 | `docs/V8_M1_CAPABILITY_MAP.md` baris 167-174 | DIDUKUNG |
| 30 | Kontrak grid/jendela: grid 60 detik (rig) dan 1 detik (bengkel); jendela [t0-10, t0); statistik mean/std/slope/last/frac | `docs/V9_PM1_ARCHITECTURE.md` (S1-S9); kontrak PM1 `docs/V10_PM1_OUTLINE.md` baris 164 | DIDUKUNG (dibaca PM0 di outline; angka sumber = dokumen primer) |

Petunjuk telusur untuk AUD-CLAIM:
- Pemisah ribuan boleh berupa titik atau koma; pemisah desimal boleh berupa koma atau titik.
  Nilailah angkanya, bukan formatnya.
- Sebuah angka dihitung cocok bila **nilai**nya sama dengan primer, meski satuan/frasa pembungkus
  berbeda.
- Angka yang dikutip kandidat dengan anotasi kampanye (mis. "angka V8, bukan V9") dinilai terhadap
  klaim beranotasinya, bukan terhadap angka telanjang.

---

## 5. CHECKLIST EVALUASI USER.TXT (INSTRUMEN KHUSUS, POIN a-e)

Sumber: `/mnt/d/Capstone 1(v2)/Evaluasi User.txt` (39 baris). File itu tidak memakai label a-e
secara harfiah, maka PM0 memetakan lima poin ke butir butirnya dengan nomor baris agar dapat
dicek ulang:

| Poin | Isi instrumen | Baris sumber | Yang dicari di tiap kandidat |
|---|---|---|---|
| (a) | Lapisan A: apakah deteksi bekerja (precision, recall, false alarm, waktu deteksi); Lapisan B: apakah deteksi bernilai maintenance (peringatan sebelum memburuk, waktu bertindak, mengurangi pemeriksaan tidak perlu; waktu peringatan terhadap kejadian nyata); Lapisan C: apakah cukup tepercaya (periode berbeda, kondisi operasi berbeda, peralatan relevan, kualitas sensor, ketidakpastian) | 17-30 | Ketiga lapisan hadir per tugas dan dipakai untuk menilai, bukan sekadar disebut |
| (b) | Bandingkan setiap metode dengan baseline yang relevan, bukan satu baseline universal | 36 (prinsip 2) | Ada baseline berbeda untuk tugas berbeda (deteksi kondisi vs prediksi onset vs ranking) |
| (c) | Bedakan deteksi anomali, deteksi kondisi, diagnosis, dan prediksi kejadian mendatang | 37 (prinsip 3) | Jenis tugas dibedakan tegas; label dan baseline mengikuti jenis tugas |
| (d) | Jangan memberi label sederhana gagal/buang berdasar satu ambang; simpan hasil sebagai informasi kemampuan, batas penggunaan, dan kekuatan bukti | 15, 30 | Tiap engine disertai kemampuan + batas + kekuatan bukti; "belum terukur" tidak digabung dengan "gagal"; tanpa vonis biner tingkat alat |
| (e) | Nilai keberhasilan pada tingkat alat predictive maintenance secara keseluruhan, bukan jumlah model ML yang melewati gate; jangan menuntut lift/fold sama untuk semua engine tanpa alasan operasional; tetap tuntut validitas data, uji temporal benar, transparansi ketidakpastian | 38-39 (prinsip 4-6), 34 (prinsip 1) | Ada sintesis tingkat alat (komposisi L0/L1/L2/L3, keputusan pada manusia); syarat per engine tidak seragam tanpa alasan; validitas data dan uji temporal tetap dituntut |

Cara pakai: poin (a)-(e) dinilai pada kriteria 3 (sub 3a-3e) dengan bobot di §2.3. Nilai tiap
poin = pengamatan seksi per kandidat, tanpa perbandingan antar kandidat di tingkat paruh-atas.

---

## 6. ATURAN PAKET .md = .ipynb

1. Deliverable tiap kandidat adalah **satu paket**: file `.md` dan `.ipynb` pasangannya. Keduanya
   dinilai. Tidak ada pilihan salah satu.
2. Isi `.ipynb` wajib memuat isi `.md` pasangannya secara substantif: bab, seksian, tabel angka,
   dan klaim yang sama. Sel markdown dalam `.ipynb` diekstrak, disambung, lalu dibandingkan dengan
   `.md`.
3. **Selisih isi = cacat** pada sub-kriteria 4c (skor 4c = 0 bila selisih substantif terbukti,
   yaitu angka, klaim, tabel, atau struktur bab yang berbeda antara kedua format).
4. Cell code di `.ipynb` tidak wajib identik apa pun isi antar kandidat; yang diwajibkan: angka
   yang diklaim di cell code konsisten dengan angka di markdown pasangannya.
5. Angka yang hanya ada di satu dari dua format tidak boleh dipakai sebagai dasar penilaian
   kedalaman; catat sebagai selisih.
6. AUD-CLAIM wajib menjalankan cek mekanis: hitung kemunculan tiap angka checklist di `.md` dan di
   sel markdown `.ipynb`, lalu laporkan selisihnya per kandidat.

---

## 7. ATURAN EM-DASH

1. Em-dash (U+2014) **dilarang** dipakai sebagai penghubung klausa sembarangan di `.md` maupun
   sel markdown `.ipynb`.
2. Penghubung klausa yang sah: konjungsi sesuai hubungan (karena/sehingga untuk kausalitas;
   namun/sedangkan untuk kontras; yaitu/misalnya untuk penjelas; dan/atau untuk koordinasi),
   atau koma, titik koma, titik dua.
3. Em-dash sebagai **penegasan tegas yang terpisah koma dan dipakai jarang** masih dianggap sah
   dan tidak dihitung pelanggaran; catat saja keberadaannya.
4. Metode hitung: `grep -c` karakter U+2014 pada `.md` dan pada sel markdown `.ipynb`; setiap
   kemunculan diperiksa konteksnya secara manual terhadap butir 1-3.
5. Skoring 4d: 0 pelanggaran = 3 poin; 1-3 pelanggaran = 1,5 poin; 4 pelanggaran atau lebih = 0.

---

## 8. PROSEDUR PENILAIAN (ANTI-SHOPPING)

1. Protokol ini dikunci dan diarsipkan **sebelum** penilai membuka isi kedua kandidat.
2. Penilaian dilakukan per kandidat secara terpisah, memakai rubrik yang sama, urutan seksi yang
   sama, dan lembar skor JSON yang sama.
3. Setiap penilai paruh-atas menyerahkan: skor per sub-kriteria, daftar bukti (path + baris/eksekusi),
   dan disclosure bias bila ada.
4. AUD-CLAIM menelusuri 30 angka §4 terhadap primer dengan eksekusi (bukan sekadar membaca
   kandidat), lalu menyerahkan status cocok/tidak per item per kandidat.
5. PM-FINAL membuka pemetaan, membandingkan skor per kriteria, menerapkan §3, lalu menetapkan
   MENANG atau SERI dengan alasan yang menunjuk syarat rubrik, bukan kesan umum.
6. Dilarang menambah kriteria, mengubah bobot, atau membuang temuan setelah skor dibuka.

---

## 9. BATAS DAN BELUM DIVERIFIKASI (oleh PM0)

1. Angka kampanye pada butir 23-30 checklist berstatus DIDUKUNG: sudah terbaca di dokumen primer
   (V9_EVAL_*, V9_R1, V8_M1, V9_A1 yang merehit dari JSON), tetapi belum dihitung ulang oleh PM0
   dari JSON mentah. AUD-CLAIM wajib menelusuri ulang.
2. 239 kolom time.csv (butir 22) berstatus DIDUKUNG (dihitung A1 dengan modul csv); PM0 hanya
   memverifikasi jumlah baris dari isi zip.
3. 27 fitur tool_wear (butir 17) berstatus DIDUKUNG dari dokumen bab; PM0 memverifikasi 469
   jendela dari disk.
4. Isi kedua kandidat **tidak dibaca** oleh PM0 selain sifat mekanis (keberadaan file, jumlah
   kemunculan U+2014 untuk keperluan metode §7). Penilaian isi = tugas penilai paruh-atas.
5. Pemetaan K1/K2 di §0 tidak boleh dipakai sebagai dasar penilaian oleh siapa pun selain
   PM-FINAL setelah skor terkunci.

---

## 10. SUMBER PRIMER (dibaca/dijalankan di sesi ini)

Eksekusi langsung: `code/v9_i1_pipeline.py` (modul dijalankan: 7 engine, 27 head, tier 12/13/2,
lapisan 5/11/9/2, AUTO_CRITICAL_SLOTS 0, SEED 42) · hitung ulang `data/USROP_labeled.csv`,
`scratch/v9_d1/datasets/*.csv.gz`, `scratch/v9_d1/lowo_*.json`, `scratch/v9_e_ml/*_RESULTS.json`,
`scratch/v6_e1/toolwear_windows.csv`, `data/bo_tspp/TSPP{1..4}.csv`, 10 CSV
`data/volve/witsml_parsed/`, path XML `data/volve/witsml_raw/`, parse
`data/volve/external/spwla_volve_logs/Well_picks_Volve_v1.dat`, baca isi zip
`kaggle_volve_witsml_F9A.zip` (419.748 baris termasuk header).
Dokumen dibaca: `docs/V10_PM1_OUTLINE.md` (keluhan operator a-f verbatim, baris 8-11),
`docs/V10_A1_AUDIT.md` (tabel 28 angka), `docs/V10_PM2_VERDICT.md`,
`docs/V9_EVAL_C_LAYERC.md`, `docs/V9_R1_JUSTIFICATION.md`, `docs/V9_A1_AUDIT.md`,
`docs/V6_D1h_KAGGLE_CAT.md`, `Evaluasi User.txt`.
JSON primer disimpan di: `scratch_registry_facts.json`, `scratch_primary_recount.json`
(pada workspace task `t_63025a46`).

---

## 11. BARIS RISET PENDAHULUAN (ringkas)

- Riset pendahuluan: `scientific-critical-thinking`: pemisahan data vs interpretasi; falsifier
  per kriteria; status kepastian per angka.
- Riset pendahuluan: `verification-mandatory`: angka checklist diverifikasi eksekusi sebelum
  ditulis; bagian belum-diverifikasi ditulis eksplisit (§9).
- Riset pendahuluan: `statistical-analysis`: bobot akurasi setara kedalaman teknis; menang
  mensyaratkan tidak kalah di akurasi; angka per kampanye tidak dirata-ratakan.
- Riset pendahuluan: `sequentialthinking` (sequ-mcp, 4 pikiran, 4/4 sukses): inventaris bahan
  → bobot 100 → checklist 30 angka + status → aturan menang/seri/anonimisasi.

*Selesai V11-PM0 (`t_63025a46`). Protokol dikunci: rubrik 100 poin eksak, 30 angka kunci,
instrumen Evaluasi User.txt a-e, aturan anonimisasi, paket md=ipynb, aturan em-dash, syarat
menang dan aturan seri.*
