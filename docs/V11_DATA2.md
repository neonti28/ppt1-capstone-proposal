# V11-D2: Uji klaim LABELING & anti-sirkularitas kedua kandidat vs kode D1

Kartu: `t_233abb36` [DataQA staf] · Papan: `capstone-v11-vs` · 2026-10-15 (WIB)
Ruang kerja: `/mnt/d/Capstone 1(v2)`. Seluruh angka di bawah dihitung ulang lewat eksekusi
nyata terhadap file primer (bukan kutipan dokumen). JSON primer disimpan ke scratch:
`~/.hermes/cache/scratch/scratch_v11_d2_recount3.json`, `scratch_v11_d2_onsets.json`,
`scratch_v11_d2_ipynb.json`. Skrip: `v11_d2_recount3.py` (hitung ulang), `v11_d2_ipynb_check.py`,
`v11_d2_headcheck.py`, `v11_d2_para.py`, `v11_d2_minutediff.py` (tes pembeda).

Dua kandidat yang diuji (identitas dirahasiakan sebagai K1/K2 sesuai aturan kartu):
Kandidat 1 = `/mnt/d/Capstone 1(v2)/docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.v3_arsip.md`
+ `.ipynb` pasangannya. Kandidat 2 =
`/mnt/d/Capstone 1(v2)/docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md` + `.ipynb`
pasangannya. Dokumen ini tidak menyimpulkan mana versi baru/lama; hanya membandingkan
isi terhadap primer.

Riset pendahuluan: scientific-critical-thinking - memisahkan OBSERVED (angka eksekusi)
dari klaim dokumen; setiap hipotesis diverifikasi dengan tes pembeda; klaim tanpa bukti
ditandai bukan dibulatkan.
Riset pendahuluan: verification-mandatory - semua angka dihitung ulang dari file primer
dengan kode independen (bukan menyalin JSON QC); daftar "belum diverifikasi" eksplisit
di bagian akhir; retractor klaim disertai jawaban penggantinya.
Riset pendahuluan: statistical-analysis - distribusi label diperiksa sebagai hitungan
frequensi (bukan uji statistik, karena populasi penuh tersedia); kuantil P75 dihitung
dari 198.928 nilai MSE; rekap jumlah baris/positif per dataset dengan pemeriksaan
konsistensi aritmetika (jumlah = jumlahan bagian).

Catatan alat: tool `sequentialthinking` (sequ-mcp) TIDAK tersedia pada sesi worker ini,
sehingga klaim kegiatan sequ-mcp TIDAK dicatat (mengikuti preseden V9_D1: kegiatan yang
tidak terbukti tidak ditulis retroaktif). Pengganti yang benar-benar dijalankan: daftar
hipotesis + tes pembeda tertulis di §0.3.

---

## 0.3 Hipotesis dan tes pembeda (pengganti sequ-mcp, dijalankan nyata)

| Hipotesis alternatif tentang angka onset | Tes pembeda | Hasil |
|---|---|---|
| H1: angka onset di dokumen hanya salinan QC JSON, tidak reproduksi | hitung ulang dari CSV mentah 4 well dengan resep identik (kode independen murni-python) | 4/4 well cocok (55/72/93/61) => H1 ditolak, angka reproduksi |
| H2: selisih onset 1-2 antar implementasi disebabkan duplikasi timestamp | cek timestamp duplikat dengan nilai STUCK konflik di 4 well | 0 duplikat di 4 well => H2 ditolak |
| H3: selisih disebabkan parsing timestamp saya lebih ketat dari pandas ISO8601 | hitung baris yang gagal parse `fromisoformat` di 4 well | 0 gagal parse => H3 ditolak |
| H4: selisih disebabkan aturan ffill saya salah (running-max vs last-value, aturan menit leadnan, menit semua-NaN) | diff menit-per-menit vs jalur pandas resep identik (`v11_d2_minutediff.py`) | 3 bug implementasi verifier ditemukan dan diperbaiki; setelah benar 4/4 cocok => H4 terkonfirmasi, primer benar |

---

## 1. Tugas 1: Skema label per kelas vs kode scratch/v9_d1 + docs/V9_D1

Primer yang dipakai: `code/v9_d1_02_rig_windows.py`, `code/v9_d1_03_rig_datasets.py`,
`code/v9_d1_04_stuck_k2.py`, `code/v9_e_ML_01_train.py`, `docs/V9_D1_DATA_PIPELINE.md` §3,
`docs/V6_E1d_PREREG_BITWEAR.md`, `docs/V8_E_vib_CAPABILITY.md`,
`docs/V8_E_tool_wear_CAPABILITY.md`.

| Kelas | Definisi primer (kode) | Kandidat 1 | Kandidat 2 | Verdict |
|---|---|---|---|---|
| vib | `VIB_THRESH = 32.17405` (v9_d1_02 baris 35); V8_E_vib "32,17405" | tidak ditulis | `VIBLAT_RT >= 32,17405` (12 kemunculan konsisten; varian "32,174405" = 0) | K2 cocok primer; K1 absen |
| ssi | `SSI=(max-min)/(2*mean)` CRPM, `SSI_MIN_SAMPLES=10`, `mean>0` (v9_d1_02 baris 34, 92-95) | tidak ditulis | persis: `(max−min)/(2·mean)`, >=1, >=10 sampel, mean>0 | K2 cocok; K1 absen |
| shk | `SHKRSK >= 1` (LABDEF v9_d1_02 baris 41) | tidak ditulis | `SHKRSK_RT >= 1` | K2 cocok; K1 absen |
| stuck K-i | `STUCK >= 1` status blok | tidak ditulis | `STUCK_RT >= 1` | K2 cocok; K1 absen |
| stuck K-ii | ffill `STUCK_RT`, edge 0->1, H=10 menit, baris dalam blok (`STUCK_ffill>=1`) Dibuang, positif `[t_e-10, t_e)` (v9_d1_04 docstring + baris 165-186) | tidak ditulis | persis sama (onset 0->1 ffill, H=10, inblock dibuang) | K2 cocok; K1 absen |
| hyd K-i | z = (SPPA-median_bin)/(1,4826*MAD_bin), `|z|>2`, `qcut(TFLO,10)` (NQ=10), agregasi jendela W=10 dengan >=50% menit anom, `MIN_OBS=5` (v9_d1_03 baris 27-29, 55-76, 100-103) | tidak ditulis | `z = 0,6745·(SPPA − median_bin)/MAD_bin` atas `qcut(TFLO,10)`, `|z|>2`, ">=50% menit anom" | K2 ekuivalen benar (0,6745 = 1/1,4826); MIN_OBS=5 tidak disebut eksplisit di K2 (minor); K1 absen |
| bit_wear K-1 | `high_MSE` = Teale MSE > P75 (V6-E1d: P75 = 256.600 psi; recount P75 = 256.600,42 psi dari 198.928 nilai MSE) | hanya menyebut "Teale, SSI, MSE/DS, UCS" sebagai riset turunan label di lini masa, tanpa skema | `high_MSE` Teale, kuantil P75 = 256.600 psi, kolom `label` tersimpan USROP | K2 cocok; K1 tanpa skema |
| tool_wear | label = identitas run, 4 alat (T01-T04) x 2 run (V8_E_tool_wear baris 29-32) | tidak ditulis | "identitas run (4 alat x 2 run)", bukan turunan fitur | K2 cocok; K1 absen |

Temuan khusus Kandidat 1: dokumennya TIDAK memuat skema label per kelas sama sekali
(0 dari 7 kelas dirinci; verifikasi regex: `VIBLAT|SHKRSK|STUCK_RT|ffill|Teale (skema)|
identitas-run|feat_ts_max` = 0 hitungan). Satu kalimat relevan justru berisiko: §8.2
menulis fitur = "statistik jendela waktu dari kanal sensor ... serta fitur turunan fisika
(MSE, SSI, UCS) bila relevan", tanpa larangan per kelas untuk turunan kanal. Pada primer,
SSI dilarang jadi fitur untuk kelas ssi dan kolom turunan MSE dilarang untuk bit_wear
(V6-E1d §4), sehingga frasa "bila relevan" tanpa pengecualian per kelas tidak selaras
dengan aturan anti-sirkularitas primer.

Catatan badan kartu: angka "VIBLAT>=32,174405" pada teks kartu TIDAK ada di primer maupun
kedua kandidat; nilai primer = 32,17405 (kode V8_E_vib dan v9_d1_02). Kedua kandidat tidak
memakai varian 32,174405.

## 2. Tugas 2: Tabel anti-sirkularitas (kanal terlarang jadi fitur)

Primer: `docs/V9_D1_DATA_PIPELINE.md` §3 (tabel per engine), `docs/V6_E1d_PREREG_BITWEAR.md`
§4 (8 kanal pembentuk label bit_wear), `code/v9_d1_03_rig_datasets.py` (`HYD_EXCLUDE =
["SPPA","TFLO","SPM"]`), `code/v9_e_ML_01_train.py` baris 192-193 (assert runtime:
`VIBLAT/SHKRSK/CRPM/STUCK` dilarang di fitur), `docs/V9_E_STAT_ENGINE.md` (hyd K-ii memakai
kolom pit + GAINLOSSTOT).

| Aspek | Kandidat 1 | Kandidat 2 |
|---|---|---|
| Tabel per kelas | TIDAK ADA; satu kalimat generik "kanal pembentuk label dilarang menjadi fitur (anti-sirkularitas)" (§8.2) | DUA tabel: §3.5 (7 baris per kelas) + Bab 4 §1.1 (7 baris + bukti assert runtime) |
| Kecocokan vs primer | kalimat generik arahnya benar, tetapi tidak dapat diaudit per kelas dan tidak menutup fitur turunan (lihat risiko §8.2 di §1 dokumen ini) | vib/ssi/shk/stuck cocok persis; hyd K-i `SPPA/TFLO/SPM` cocok `HYD_EXCLUDE`; hyd K-ii "kolom pit + GAINLOSSTOT" cocok V9_E_STAT; tool_wear "tidak ada" cocok (label identitas run) |
| Ketidakcocokan internal | tidak berlaku | bit_wear: §3.5 menulis hanya 4 kanal (`WOB, ROP, RPM, TQA`), primer V6-E1d §4 = 8 kolom (`WOB, TQ, RPM, ROP, Hookload, MSE, D_exp, ROC_coef`); Bab 4 §1.1 K2 justru menulis 8 = benar. Jadi §3.5 K2 TIDAK LENGKAP (kurang 4 butir, termasuk kolom turunan MSE/D_exp/ROC_coef yang justru paling rawan sirkular) |
| Bukti pelaksanaan | tidak ada klaim pelaksanaan | assert runtime diverifikasi ada di kode (`v9_e_ML_01_train.py` baris 192-193); daftar kanal fitur 11 berisi TQA..dbtm tanpa kanal label (verifikasi kolom dataset) |

Verdict tugas 2: Kandidat 2 lebih lengkap dan mayoritas benar; satu bagian incompleteness
di §3.5 (bit_wear 4 vs 8 kolom primer). Kandidat 1 tidak salah secara eksplisit, tetapi
hanya kalimat generik sehingga tidak dapat diverifikasi per kelas, dan justru membuka
celah "MSE/SSI sebagai fitur bila relevan" yang pada primer dilarang untuk kelas terkait.

## 3. Tugas 3: Hitung ulang populasi label

Seluruh baris di bawah = hasil eksekusi `v11_d2_recount3.py` terhadap file di disk.

| Klaim | Hasil hitung ulang primer | Status |
|---|---|---|
| USROP distribusi `normal` 134.013 / `high_MSE_bit_wear` 49.732 / `low_ROP_efficiency` 15.183 (K2 §3.2.2) | 198.928 baris, 18 kolom, 7 well; `label` = normal 134.013, high_MSE_bit_wear 49.732, low_ROP_efficiency 15.183 | TERBUKTI persis (K2). K1 tidak mengklaim distribusi ini |
| P75 MSE = 256.600 psi (K2 Bab 4; V6-E1d) | P75 dari 198.928 nilai MSE = 256.600,42 psi | TERBUKTI (pembulatan 256,600 wajar) |
| 884 kejadian terkurasi; `bha_relevant` yes 50 / uncertain 571 / no 263; 9 kategori (K2 §3.2.3) | `data/volve/labels_curated_v2.csv` = 884 baris; yes 50, no 263, uncertain 571; kategori: routine_no_failure_evidence 496, surface_rig_equipment 216, mixed_evidence 47, bha_stuck_fishing 38, failure_unlocated 28, wellbore_fluid 25, wireline_completion_intervention 21, bha_downhole_equipment 12, safety_personnel 1 | TERBUKTI persis (K2). K1 mengklaim "884 label peristiwa terkurasi" (2 tempat) = TERBUKTI |
| "berkas mentah memuat 1.413 baris termasuk header dan baris bantu" (K2 §3.2.3) | file di disk sekarang (v1 dan v2) keduanya = 884 baris data; keadaan 1.413 baris tidak ada lagi di disk | TIDAK DAPAT DIVERIFIKASI ULANG dari disk sekarang (klaim reconciliasi historis); angka operasional 884 tetap terbukti |
| Onset ffill F-9_A 72 / F-14 61 / F-10 93; F-9 55 tanpa referensi (K2 Bab 4 §1, §7) | hitung ulang independen murni-python dari `witsml_parsed/*.csv` dengan resep identik v9_d1_04 (dedup timestamp, ffill STUCK_RT, resample 60 detik max, edge 0->1 lewati NaN): F-9 55, F-9_A 72, F-10 93, F-14 61 | TERBUKTI persis 4/4 (K2). Cross-check jalur pandas resep identik memberi F-9_A = 72 |
| Jumlah baris & positif 6 dataset latih (K2 §3.3.4) | vib 23.922/5.429 (4 well), ssi 35.906/607 (9), shk 56.495/2.005 (9), stuck_k1 5.555/2.007 (2), hyd_ki 52.509/7.172 (9), stuck_k2 118.567/1.975 (4); total 292.954 baris / 19.195 positif | TERBUKTI persis; aritmetika total cocok |
| "7 kelas target dengan populasi terhitung" (K1 §8.2) | K1 tidak menulis satu pun angka populasi | klaim tanpa angka: tidak dapat dinilai akurasi (bukan salah, tetapi tidak dapat diaudit) |

## 4. Tugas 4: Anti-bocor waktu (feat_ts_max < lab_ts; jendela dalam blok dibuang)

| Aspek | Primer | Kandidat 1 | Kandidat 2 |
|---|---|---|---|
| Invariant stempel | kolom `well/ts_bin/feat_ts_max/lab_ts/lab_kind`; checker `v9_d1_05_leak_lowo.py` | "pemeriksaan kebocoran waktu (fitur selalu berstempel waktu lebih awal daripada peristiwa)" (§8.3): pemahaman BENAR tetapi generik, tanpa nama invariant/kolom | `feat_ts_max < lab_ts` eksplisit + tabel pelanggaran per dataset |
| Hitung ulang ulang 0 pelanggaran | recount independen dari 6 file `datasets/*.csv.gz` (parsing murni-python): pelanggaran `feat_ts_max >= lab_ts` = 0 di 6/6, baris NaN `feat_ts_max` = 0 di 6/6, baris = persis tabel K2 | tidak diklaim | TERBUKTI persis (K2) |
| Jendela ketat-lalu [t0-10, t0) | kode v9_d1_02 (fitur) vs [t0, t0+10) (label) | implisit "fitur lebih awal daripada peristiwa" | eksplisit + alasan (fitur dari masa lalu relatif label) |
| Jendela dalam blok dibuang (onset stuck) | `v9_d1_04`: `elig = hor[~stuckf]`, baris inblock dibuang dari jendela positif | TIDAK DISEBUT (K1 tidak membahas onset sama sekali) | eksplisit: "baris dalam blok (STUCK>=1) dibuang" |

Verdict tugas 4: kedua kandidat TIDAK salah; Kandidat 2 benar secara spesifik dan dapat
diaudit (invariant + aturan inblock + angka 0 pelanggaran terverifikasi ulang); Kandidat 1
benar pada tingkat prinsip tanpa detail yang dapat diuji.

## 5. Tugas 5: Konsistensi md vs ipynb (bab labeling)

Metode: ekstrak seluruh sumber sel `markdown`+`code` dari .ipynb, lalu (a) cocokkan 28
kunci pola labeling/anti-sirkularitas antara .md dan .ipynb, (b) cocokkan heading dua arah,
(c) cocokkan paragraf .md >80 karakter terhadap teks ipynb ternormalisasi.

| Uji | Kandidat 1 | Kandidat 2 |
|---|---|---|
| 28 kunci pola (threshold, ffill, onset, qcut, P75, distribusi USROP, 884, onset well, feat_ts_max, identitas-run, dst) | semua kunci berjumlah identik md vs ipynb (termasuk ketiadaan skema label di keduanya) | semua 28 kunci berjumlah identik md vs ipynb (contoh: "32,17405" 13/13, ffill 4/4, P75 13/13, USROP 134.013 2/2) |
| Heading md ada di ipynb | 42/42 | 205/205 |
| Paragraf md hilang di ipynb | 0 dari 48 paragraf >80 karakter | 1 kandidat "hilang" ternyata FALSE NEGATIVE normalisasi: paragraf "Fisika kegagalan. Bit bounce (aksial)" terverifikasi identik di ipynb lewat pencarian konteks |
| Konten ekstra ipynb | ipynb memuat sel kode/gambar ekstra (mis. figure "Status relevansi BHA (n=884)"); ini TIDAK kontradiktif dengan md | ipynb memuat sel kode/gambar ekstra serupa; TIDAK kontradiktif |

Verdict tugas 5: KEDUA kandidat konsisten md=ipynb untuk bab labeling (ketentuan paket
md+ipynb terpenuhi; isi dokumen .md seluruhnya hadir di .ipynb masing-masing).

## 6. Rekap ledger klaim (status per verifikasi)

Rekap Kandidat 1: TERBUKTI 2 (884 kejadian; pemahaman prinsip anti-bocor generik benar);
KLAIM TANPA BUKTI ANGKA 2 ("tujuh kelas dengan populasi terhitung" tanpa angka; "fitur
turunan MSE/SSI/UCS bila relevan" tanpa larangan per kelas); TIDAK ADA SKEMA 7 kelas
(0/7 dirinci).

Rekap Kandidat 2: TERBUKTI 14 (ambang vib; rumus+min-sampel ssi; ambang shk; stuck K-i;
onset K-ii ffill/H10/inblock; hyd z/qcut/agregasi; P75 Teale; identitas-run; distribusi
USROP 3 angka; P75 psi; 884 + yes/no/uncertain + 9 kategori; onset 4 well; 6 dataset
rows/positif/wells; 0 pelanggaran anti-bocor di 6/6); KOREKSI/CATATAN 3 (§3.5 bit_wear
hanya 4 dari 8 kolom primer; klaim historis "1.413 baris" tak dapat diverifikasi ulang;
MIN_OBS=5 hyd tidak eksplisit); INKONSISTENSI ISTILAH MINOR 1 (Bab 4 §0 menyebut "11 kanal
MWD" sedangkan §1.1 Bab 4 dan Bab 3 menyebut 11 kanal surface/depth: TQA..dbtm; istilah
"MWD" untuk 11 kanal fitur tidak tepat, dan K1 punya penyebutan serupa "55 fitur dari
11 kanal MWD").

## 7. Sub-skor slice labeling untuk rubrik PM-0 (bukan skor akhir; PM-FINAL yang memutus)

| Kriteria (slice labeling/anti-sirkular) | Kandidat 1 | Kandidat 2 |
|---|---|---|
| (1) Kedalaman teknis | lemah: 0/7 skema label tertulis; anti-sirkularitas satu kalimat | kuat: skema per kelas + rumus + asersi runtime + aturan inblock |
| (2) Akurasi terhadap primer | klaim yang ada terbukti (884), tetapi frasa "MSE/SSI sbg fitur bila relevan" tidak selaras dgn larangan primer per kelas | hampir seluruh angka terbukti persis; 1 ketidakcocokan internal §3.5 (4 vs 8 kolom) |
| (4) Struktur & konsistensi md=ipynb | konsisten | konsisten (28/28 kunci identik) |

## 8. Belum diverifikasi (eksplisit)

1. Kondisi historis "berkas mentah 1.413 baris" untuk katalog kejadian: keadaan disk
   sekarang sudah 884 baris di kedua file; reconciliasi lama tidak dapat diulang tanpa
   salinan mentah pra-rekonsiliasi.
2. Angka K1 lain di luar cakupan kartu ini (8.474.172 baris WITSML, 17.368 berkas,
   dsb) tidak diuji di sini; kartu DataQA lain yang menangani.
3. Keabsahan ilmiah ambang 32,17405 ft/s² sebagai ambang operasional rig (sumber V8)
   tidak diuji ulang; yang diuji hanya konsistensi angka antara primer dan kandidat.
4. Kelayakan label secara kausal untuk engine tertentu (mis. hyd K-i = proxy) di luar
   cakupan; di sini hanya kecocokan skema vs kode.
5. Tool sequ-mcp tidak tersedia di sesi ini sehingga kegiatan sequ-mcp tidak dapat
   dijalankan maupun diklaim.

## 9. Audit em-dash

Dokumen ini ditulis tanpa tanda em-dash (pencarian karakter U+2014 pada file ini = 0 kemunculan).

Sumber primer yang dibaca/dijalankan: `code/v9_d1_02_rig_windows.py`,
`code/v9_d1_03_rig_datasets.py`, `code/v9_d1_04_stuck_k2.py`, `code/v9_e_ML_01_train.py`,
`docs/V9_D1_DATA_PIPELINE.md`, `docs/V6_E1d_PREREG_BITWEAR.md`,
`docs/V8_E_vib_CAPABILITY.md`, `docs/V8_E_tool_wear_CAPABILITY.md`,
`docs/V9_E_STAT_ENGINE.md`, `data/USROP_labeled.csv`, `data/volve/labels_curated_v2.csv`,
`data/volve/labels_curated.csv`, `data/volve/witsml_parsed/{F-9,F-9_A,F-10,F-14}.csv`,
`scratch/v9_d1/datasets/*.csv.gz`, `scratch/v9_d1/v9_d1_04_qc.json`,
`scratch/v9_d1/v9_d1_05_leak_lowo.json`, kedua pasang `.md`+`.ipynb` kandidat.
