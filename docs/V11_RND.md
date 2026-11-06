# V11-R1: Uji Alasan Pemilihan Metode dan Buka Sitasi Kedua Kandidat

Task: `t_e2ee149b` · Papan: `capstone-v11-vs` · Tanggal: 2026-10-15 (WIB)
Peran: [R&D] menguji bagian alasan pemilihan & keaslian sitasi. Identitas kandidat dirahasiakan di seluruh dokumen ini.

- **Kandidat 1** = `/mnt/d/Capstone 1(v2)/docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.v3_arsip.md` + `.ipynb` pasangannya
- **Kandidat 2** = `/mnt/d/Capstone 1(v2)/docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md` + `.ipynb` pasangannya

> **Riset pendahuluan: `scientific-critical-thinking`**: tiap klaim dipisah OBSERVED (baca file primer/eksekusi web) vs DERIVED vs HIPOTESIS; klaim provenance (angka V8 dipakai di bagian berlabel V9) diperiksa sebagai temuan, bukan diabaikan; contraints: kutipan dinilai cocok-tidaknya dengan makna yang dipakai, bukan sekadar hidup-matinya URL.
> **Riset pendahuluan: `verification-mandatory`**: semua klaim dibuka dengan tool nyata (web_extract, curl, api.crossref.org, baca file primer); bagian "Belum diverifikasi" ditulis eksplisit di akhir; DOI 404 pada resolver reader diuji silang dengan Crossref sebelum disebut mati (klaim ketiadaan wajib lolos tes termurah).
> **Riset pendahuluan: `statistical-analysis`**: penilaian bukti memakai kriteria: kecukupan fold, penandaan underpowered, ketidak-tumpang-tindihan CI, dan larangan merata-ratakan metrik antar kelas; angka 4/4 dan 7/7 dinilai beserta desain pra-registrasinya (prereg hash, JSON per fold), bukan hanya hitungannya.
> **Riset pendahuluan: `sequentialthinking`**: tool sequentialthinking/sequ-mcp TIDAK tersedia di sesi ini (tool_search: 0 hasil). Pengganti: penalaran berlapis dicatat manual sebagai 4 pikiran: (1) inventaris sitasi + alasan per kandidat, (2) uji dua klaim kunci ke file primer V8/V9, (3) bedah parity md vs ipynb + kode sitasi menggantung, (4) susun ledger + dokumen.
> **Riset pendahuluan: agentmemory**: fakta tahan-lama dicatat: pola reader-404 doi.org untuk DOI Elsevier (palsu-mati), lokasi ledger 27 sumber, dan temuan provenance V8 di bagian berlabel V9.

Aturan umum dipatuhi: seluruh angka di bawah berasal dari eksekusi/berkas primer; JSON primer disimpan di scratch papan (`citation_crossref.json`, `citation_ledger.json` pada workspace t_e2ee149b).

---

## 1. Alasan Pemilihan per Engine (fisika kegagalan -> sensor -> metode)

### Kandidat 1

Bab alasan pemilihan memuat (a) tabel model 7 baris dengan kolom peran + alasan pendek, dan (b) tabel keputusan 6 baris (metode per tugas, LOWO, baseline relevan, metrik, lapisan A/B/C, pemisahan peran). Penilaian per engine:

| Aspek | Temuan (status: OBSERVED) |
|---|---|
| Cakupan 7 engine | §15.1 memuat 7 engine dengan jenis tugas + jenis engine + tingkat pemakaian + batas. Cakupan penuh. |
| Rantai fisika -> sensor -> metode | TIDAK ada per engine. Alasan bersifat prinsip (mis. "tahan fitur berskala berbeda" untuk RF, "menguji apakah kinerja RF kebetulan" untuk GB) tanpa tautan angka/fisika per kelas di dalam dokumen. |
| Bukti angka per keputusan | Angka kemampuan ada di §15 (tingkat pemakaian) dengan rujukan [A-19][A-20], tetapi kedua kode itu MENGGANTUNG (lihat §4). Alasan pemilihan di §12 tidak menempel ke angka kampanye mana pun. |
| Baseline | Prinsip baseline relevan per tugas dinyatakan, contoh "ambang lift 1,5" disebut sebagai hal yang tidak mutlak. |

### Kandidat 2

Bab "Alasan Pemilihan Tiap Engine" memuat 7 sub-bab per engine dengan format tetap: (i) fisika kegagalan, (ii) mengapa sensor X relevan, (iii) mengapa metode Y, (iv) bukti empiris, (v) batas; lalu peta keputusan metode 11 baris, tiga temuan penentu, tabel sitasi per rumus 27 baris, dan what-if 5 cabang.

| Aspek | Temuan (status: OBSERVED) |
|---|---|
| Cakupan 7 engine | Penuh: vib, ssi, bit_wear, stuck, hyd, shk, tool_wear; sub-klasifikasi K-1/K-2 dan K-i/K-ii dinyatakan (11 klaim). |
| Rantai fisika -> sensor -> metode | Ada dan lengkap di ketujuh engine, tiap keputusan ditaut ke angka (AUPRC, ΔB, FAR, fold menang) atau ke fisika/kanal, plus sitasi rumus [1]..[27]. |
| Bukti angka per keputusan | Setiap sub-bab memuat angka dengan penyebut fold/well dan penanda "belum terukur" terpisah dari "gagal". Bagian §7 sendiri menyatakan angka V9 dikutip dari JSON/dokumen primer, tidak dihitung ulang di sana. |
| Baseline | Empat baseline berbeda (persistence, canary-kedalaman, prevalence-random, rule/display) dengan ancaman validitas berbeda per baseline; larangan baseline universal dinyatakan. |

**Jawaban T1:** kandidat 2 memenuhi syarat "tiap keputusan ditaut ke bukti angka/fisika" di ketujuh engine; kandidat 1 memenuhi di tingkat prinsip dan tingkat pemakaian, tetapi tidak memuat rantai bukti per engine di dalam dokumennya, dan rujukan buktinya memakai kode yang menggantung.

---

## 2. Tabel Sitasi (dibuka satu per satu)

Ledger kandidat 2 = 27 sumber eksternal di `docs/V9_R1_JUSTIFICATION.md` §11 (dipakai ulang oleh Bab 2 §4 "SITASI PER RUMUS"). Pembukaan: 13 URL dibuka sampai teks (web_extract/curl), 20 DOI dicek Crossref (beberapa tercatat dua kali di kedua kategori). Status "cocok" = judul/isinya mendukung makna pemakaian di dokumen.

### Kandidat 2 (27 sumber)

| # | url | status buka | cocok / karangan |
|---|---|---|---|
| [1] | https://doi.org/10.1016/0148-9062(65)90022-7 | Crossref OK 1965 + curl -L 200 (bentuk %-encode %28%29 memberi 404 di resolver reader; DOI asli hidup) | cocok: asal-usul MSE Teale; bukan karangan |
| [2] | hpinc.com ... AADE-17-NTCE-033_Extract.pdf | terbuka teks penuh | cocok: MSE+DS membedakan vibrasi/keausan/balling; bukan karangan |
| [3] | https://doi.org/10.2298/TSCI2502521L | Crossref OK 2025; reader kena 422 | cocok sebagian: judul stick-slip identification cocok; formula SSI (max−min)/(2·mean) belum diverifikasi dari teks penuh |
| [4] | https://doi.org/10.1016/j.petrol.2019.05.021 | Crossref OK 2019 | cocok: ML klasifikasi severity stick-slip (Hegde); bukan karangan |
| [5] | https://doi.org/10.1023/A:1010933404324 | terbuka Springer | cocok: Breiman Random Forests; bukan karangan |
| [6] | https://www.jmlr.org/papers/v15/delgado14a.html | terbuka teks penuh | cocok: RF = keluarga klasifikator terbaik di benchmark; bukan karangan |
| [7] | https://www.itl.nist.gov/div898/handbook/eda/section3/eda356.htm | terbuka teks penuh | cocok: definisi MAD; bukan karangan |
| [8] | https://www.itl.nist.gov/div898/software/dataplot/refman2/auxillar/mad.htm | terbuka teks penuh | cocok: scaled MAD = MAD/0,6745 ≈ sd untuk normal; bukan karangan |
| [9] | https://doi.org/10.1002/widm.1236 | Crossref OK 2017 | cocok: anomaly detection robust statistics; bukan karangan |
| [10] | https://doi.org/10.1016/j.sigpro.2019.107299 | Crossref OK 2020 | cocok: survei change point offline (keluarga least-squares); bukan karangan |
| [11] | https://doi.org/10.1080/01621459.2012.737745 | Crossref OK 2012 | cocok: PELT (Killick); bukan karangan |
| [12] | https://doi.org/10.1007/978-1-4757-3235-1 | Crossref OK 2000 | cocok: Permutation Tests (Good); bukan karangan |
| [13] | https://otexts.com/fpp3/simple-methods.html | terbuka teks penuh | cocok: naive ŷ(t)=y(t−1) "works remarkably well" + wajib jadi benchmark; bukan karangan |
| [14] | https://doi.org/10.1016/j.ijforecast.2019.04.014 | Crossref OK 2020 | cocok: M4 Competition (metode naive sulit dikalahkan); bukan karangan |
| [15] | https://doi.org/10.2307/2331838 | Crossref OK 1915 | cocok: Fisher 1915 Biometrika; bukan karangan |
| [16] | bibbase.org ... Fisher probable-error 1921 | terbuka metadata | cocok sebagian: judul+jurnal (Metron 1:3–32, 1921) cocok; rumus z' = atanh(r), SE = 1/√(n−3) belum diverifikasi dari teks |
| [17] | https://doi.org/10.2118/178821-pa | Crossref OK 2016; onepetro kena CAPTCHA | cocok: IDAPS, deteksi influx saat pompa berhenti; bukan karangan |
| [18] | https://doi.org/10.1016/j.ejbas.2015.09.006 | Crossref OK (online 2015) | cocok: sinyal dini kick via mud logging; bukan karangan |
| [19] | https://arxiv.org/abs/2503.07440 + PDF | terbuka teks penuh PDF | cocok + ANGKA: Table 4 W_t = 2,67 (τ15) / 4,67 (τ30) / 7,37 (τ45) / 6,73 (τ60) menit. Klaim "2,67–7,37 menit" = rentang persis; bukan karangan |
| [20] | https://doi.org/10.3390/app15095042 | terbuka teks penuh MDPI | cocok: AE hanya-data-normal, Volve, AUC 0,958; bukan karangan |
| [21] | https://doi.org/10.1016/j.petrol.2021.109489 | Crossref OK 2022 | cocok: LSTM-AE unsupervised stuck pipe; bukan karangan |
| [22] | https://doi.org/10.1038/s41598-023-33411-9 | terbuka teks penuh | cocok: surface -> getaran downhole, R > 0,9, MAPE < 7,5%; bukan karangan |
| [23] | https://doi.org/10.2118/200006-MS | Crossref OK 2020; onepetro CAPTCHA | cocok sebagian: judul taksonomi dysfunctions cocok; klaim "10 kelas" belum diverifikasi dari teks |
| [24] | https://doi.org/10.2118/228303-PA | Crossref OK 2025 | cocok: dysfunctions dari surface + forensik bit (SPE J); bukan karangan |
| [25] | https://doi.org/10.2118/56017-PA | Crossref OK 2001; onepetro CAPTCHA | cocok sebagian: judul korelasi empiris shale cocok; rumus UCS = 2,922·φ^(−0,96) belum diverifikasi dari teks |
| [26] | https://doi.org/10.1016/j.petrol.2006.01.003 | Crossref OK 2006 | cocok: hubungan kekuatan batuan vs properti fisik; rumus e^(−6,95φ) belum diverifikasi dari teks |
| [27] | https://doi.org/10.1016/j.petrol.2020.108069 | Crossref OK 2021 | cocok: dataset benchmark ROP (Tunkiel); PDF lokal `Reference/` ada (5,2 MB); bukan karangan |

Rekap kandidat 2: 27/27 terdaftar dan hidup (Crossref OK untuk 20 DOI; 7 non-DOI terbuka langsung); 13 dibuka sampai isi; **0 karangan**; 5 klaim bentuk-rumus (formula SSI, rumus z', UCS Horsrud, UCS Chang, jumlah 10 kelas Saini) masih pada taraf metadata/judul. R1 lama juga menyimpan daftar 5 kandidat DOI yang ditolak (§13, sudah diganti), jadi klaim "0 karangan" di dokumen kandidat 2 konsisten dengan jejak verifikasinya.

### Kandidat 1

Kandidat 1 hanya memuat **1 sitasi eksternal**: [A-13] Tunkiel et al. 2021 (identik dengan [27], hidup, judul cocok, PDF ada di `Reference/`). 12 rujukan sisanya dokumen internal workspace, dibuka sebagai berikut:

| Kode | rujukan | status buka | cocok / karangan |
|---|---|---|---|
| [A-1] | docs/V6_PM_VERDICT.md | ada | cocok: vonis SAH ">3 kriteria kerusakan dari data nyata" (baris 25) |
| [A-2] | docs/V6_E1_ML_DESIGN.md + V6_E1*_PREREG*.md | ada | file pra-reg V6_E1b/c/d terlihat |
| [A-3] | docs/V6_R1_SCIENCE.md | ada | terbuka |
| [A-4] | docs/V6_D0_READERS_SYNTHESIS.md + V6_D1a..h | ada | 8 file D1 terlihat di ls docs |
| [A-5] | docs/V7_PM_VERDICT.md | ada | terbuka |
| [A-6] | docs/V8_R1_ABC_SPEC.md + V8_E_*_CAPABILITY.md | ada | 7 file capability terlihat |
| [A-7] | docs/V8_M1_CAPABILITY_MAP.md | ada | terbuka |
| [A-8] | docs/V8_A1_CAPABILITY_AUDIT.md | ada | cocok dengan nuansa: audit menyatakan 114/121 klaim persis, 6 selisih penyajian, "Tidak ada karangan"; frasa kandidat 1 "121 klaim, 0 fabrikasi, enam selisih penyajian" akurat |
| [A-9] | docs/V3_DATA_ACQUISITION_INVENTORY.md + V3_WITSML_PARSE_REPORT.md | ada | terbuka |
| [A-10] | docs/V3_TS_FEATURES.md | ada | terbuka |
| [A-11] | docs/V2_LABEL_CURATION.md + V2_LABEL_AUDIT_UNCERTAIN.md | **tidak ada di v2/docs**; keduanya ada di `/mnt/d/Capstone 1/docs/` | path basi relatif workspace v2 (bukan karangan, file nyata di folder lama) |
| [A-12] | docs/PROTOCOL_RISET_TIM.md + CHANGELOG.md | ada | terbuka |
| [A-13] | Reference/Tunkiel et al. 2021 ...pdf | ada (5,2 MB) | eksternal hidup, judul cocok |
| [A-16] | tidak didefinisikan | **menggantung**: dipakai 1x (baris 131) | tidak ada definisi di md maupun ipynb |
| [A-19] | tidak didefinisikan | **menggantung**: dipakai 2x (baris 260, 309) | klaim "3 mesin Tingkat 2, 2 bersyarat, 2 Tingkat 1" sejalan dengan V8_M1_CAPABILITY_MAP baris 180 ("5/7 punya jalur peringatan (3 terbukti + 2 bersyarat) · 7/7 layak setidaknya"), tetapi kodenya tidak ada di tabel sitasi |
| [A-20] | tidak didefinisikan | **menggantung**: dipakai 3x (baris 260, 264, 309) | idem |
| [A-21] | tidak didefinisikan | **menggantung**: dipakai 1x (baris 299) | idem |

**Jawaban T2:** kandidat 2 memenuhi syarat minimal 8 sitasi dibuka (13 dibuka sampai isi, 27/27 hidup, 0 karangan). Kandidat 1 secara struktural tidak memuat 8 sitasi eksternal (hanya 1); seluruh rujukan internal dibuka, 2 di antaranya bermasalah: [A-11] path basi dan 4 kode menggantung ([A-16][A-19][A-20][A-21]). Kode menggantung yang sama ([A-19][A-20][A-21]) juga dipakai di BAGIAN C kandidat 2 (baris 3504, 3514) dengan tabel 19.3 yang sama-sama hanya mendefinisikan [A-1]..[A-13], jadi cacat ini dimiliki kedua kandidat pada bagian yang dimiliki bersama.

---

## 3. Verdict Dua Klaim Kunci

### 3.1 "RF dilarang di hyd = keputusan berbukti" (D-A5)

Ledger per klaim:

1. Klaim literal (kandidat 2, Bab 2 §2.5 dan Bab 8 §3): "RF DILARANG di kelas hyd-K-i (D-A5) karena ΔB RF−persistence negatif di 7/7 fold (−0,010…−0,400), CI non-tumpang tindih 6/7".
2. Bukti mentah: `V8_E_hyd_CAPABILITY.md` baris 57 (F-5 ΔB = −0,400), baris 59 (F-9 ΔB = −0,010), baris 62 ("ΔB < 0 di 7/7 fold"), baris 64 ("CI tidak tumpang tindih di 6/7 fold; F-9 satu-satunya tumpang"), baris 179 ("KUAT, 7/7 fold konsisten, CI tidak tumpang tindih 6/7, replikasi eksak"). `V9_PM1_ARCHITECTURE.md` baris 129–130: D-A5 "hyd-K-i DILANGGAN (ΔB negatif 7/7, replikasi eksak) TIDAK digeneralisasi ke kelas lain". `V9_E_ML_ENGINE.md` baris 352 dan 472: V9 "sengaja TANPA ML" di hyd-K-i, harness menolak engine di luar daftar.
3. Rantai inferensi: 7 fold LOWO semua negatif + CI dominan -> persistence terukur lebih baik dari RF untuk tugas status itu -> melarang RF di kelas itu = keputusan empiris, bukan selera. Larangan dibatasi kelas (tidak digeneralisasi), sesuai bukti.
4. Status: **TERBUKTI**. Angka kandidat 2 cocok 1:1 dengan primer V8. Catatan provenance: angka ini berasal dari kampanye V8; V9 mematuhi larangan dengan tidak menjalan-kan RF (bukan mengulang pengukuran), sedangkan sub-bab kandidat 2 berjudul "Bukti empiris V9" mencampurkan angka V8 dan V9 di butir yang sama.

Kandidat 1: klaim serupa tidak ada. Kandidat 1 menyebut hyd = "Statistik (median/MAD) + persistence" tanpa RF dan tanpa angka pendukung; keputusannya sejalan dengan D-A5, tetapi tidak dibuktikan di dalam dokumennya.

### 3.2 "persistence menang 4/4 di bit_wear"

1. Klaim literal (kandidat 2, Bab 2 §0, §2.3, §3.1, §3.2): "bit_wear persistence menang 4/4 (vs RF), ΔB −0,087…−0,381, AUPRC 0,679–0,984".
2. Bukti mentah: `V8_E_bit_wear_CAPABILITY.md` baris 40 ("RF TIDAK menambah di atas rule persistence di 4/4 fold, ΔB_vs_persistence −0,087…−0,381"), baris 78/81 (tabel per fold: F-14 −0,381, F-5 −0,087), baris 183–184 (dua klaim 4/4 diberi kekuatan KUAT dengan artefak primer JSON per fold, pra-reg E1d ber-hash SHA-256 986f45a1 sebelum training, persistence dihitung pada fold yang sama). `V6_E1d_PREREG_BITWEAR.md` ada dan menyatakan hash dicatat sebelum training. Silang V9: `V9_EVAL_A_LAYERA.md` baris 61 (persistence V9 AUPRC 0,119–0,984, mean 0,670, 5/7 fold scorable) dan `V9_E_RULE_ENGINE.md` baris 349 (baseline persistence/canary V9 identik digit dengan V6).
3. Rantai inferensi: label high_MSE membentuk blok kedalaman -> y(t−1) membawa hampir semua sinyal -> persistence unggul; RF terukur kalah di 4/4 fold pada kampanye pra-reg; karena itu engine utama K-1 = persistence. Logikanya koheren dan mekanismenya dinyatakan.
4. Status: **TERBUKTI** sebagai angka kampanye V8 pra-reg; reproduksi V9 hanya untuk baseline (persistence/canary identik digit), RF bit_wear tidak dijalankan ulang di V9 (`V9_E_ML_ENGINE.md` baris 355: "bit_wear K-1 RF / K-2 onset RF = belum terukur"). Catatan provenance sama dengan 3.1: sub-bab "Bukti empiris V9" memuat angka V8; tabel §3.1 kandidat 2 justru menyatakannya dengan jujur ("5/7 fold scorable; angka V8: 0,679–0,984"), jadi dokumennya tidak salah, hanya label bagianannya yang kabur.

Kandidat 1: klaim serupa tidak ada; §15.1 menyebut bit_wear = "RF + persistence + canary" dengan status "konfirmasi status terukur" tanpa menyebut bahwa RF terukur kalah 4/4 dari persistence di kelas itu.

---

## 4. Alasan Pemilihan Tanpa Bukti (klaim kosong)

**Kandidat 1:**
- Alasan pemilih RF ("tahan fitur berskala berbeda; sesuai fitur campuran") dan penolakan deep learning ("jumlah unit positif per lipatan kecil") dinyatakan tanpa sitasi maupun angka di dalam dokumen.
- Enam baris tabel alasan (§12) semuanya prinsip metodologis; tidak satu pun menempel ke angka kampanye tertentu.
- §15.2 dan §19.1 menempelkan angka tingkat pemakaian (3/2/2/0) ke kode [A-19][A-20] yang tidak didefinisikan di mana pun (dibuktikan di md dan ipynb: tabel sitasi hanya berisi [A-1]..[A-13]). Angka itu sendiri konsisten dengan `V8_M1_CAPABILITY_MAP.md` baris 180, jadi isi klaim benar, tetapi tautan buktinya putus.

**Kandidat 2:**
- Dari 7 engine, ketujuhnya memuat angka atau rujukan primer; tidak ditemukan pemilihan metode tanpa bukti (status: OBSERVED dari pembacaan Bab 2 §2–§3).
- Dua temuan bukan klaim kosong, melainkan label provenance kabur: (a) sub-bab "Bukti empiris V9" pada bit_wear memuat angka kampanye V8; (b) hal yang sama pada hyd-K-i untuk ΔB 7/7. Kedua angka terbukti benar terhadap primer; yang kurang adalah penyebutan sumber versi kampanye di sub-bab tersebut.
- Kode [A-19][A-20][A-21] juga dipakai di BAGIAN C kandidat 2 (baris 3504, 3514) tanpa definisi, sama seperti kandidat 1.

---

## 5. md vs ipynb (parity isi)

| Kandidat | Hasil (OBSERVED, skrip `v11_r1_nb_parity.py`) |
|---|---|
| Kandidat 1 | 0 dari 255 baris non-kosong `.md` yang tidak ditemukan di `.ipynb` (isi notebook mencakup seluruh markdown + output). Paritas penuh. |
| Kandidat 2 | 0 dari 2.829 baris non-kosong `.md` yang tidak ditemukan di `.ipynb`. Paritas penuh. |

Kedua kandidat memenuhi syarat paket md = ipynb. Tidak ada konten eksklusif ipynb yang bertentangan dengan md (satu-satunya URL yang muncul di ipynb tetapi bukan di md adalah tautan instalasi ipywidgets bawaan notebook, bukan sitasi ilmiah).

---

## 6. Ringkasan Temuan (untuk PM-FINAL)

| No | Temuan | Kandidat 1 | Kandidat 2 | Kekuatan bukti |
|---|---|---|---|---|
| 1 | Rantai fisika -> sensor -> metode per engine | tidak ada di dokumen (prinsip saja) | penuh 7 engine, tiap keputusan berangka | OBSERVED |
| 2 | Sitasi eksternal hidup | 1 dari 1 (Tunkiel); 12 internal; 4 kode menggantung; 1 path basi | 27/27 hidup; 13 dibuka sampai isi; 0 karangan | OBSERVED (Crossref + web_extract) |
| 3 | Klaim "RF dilarang hyd" | tidak diklaim (sejalan, tanpa bukti) | diklaim + angka cocok 1:1 dengan primer V8 | TERBUKTI |
| 4 | Klaim "persistence menang 4/4 bit_wear" | tidak diklaim | diklaim + angka cocok 1:1 dengan primer V8 (pra-reg E1d) | TERBUKTI |
| 5 | Klaim kosong | alasan RF/DL tanpa sitasi/angka; angka tingkat pemakaian menempel ke kode gantung | tidak ditemukan; dua label provenance kabur (V8 di bagian berlabel V9) | OBSERVED |
| 6 | Paritas md/ipynb | penuh | penuh | OBSERVED |

Belum diverifikasi (eksplisit): teks penuh untuk [3] formula SSI, [16] rumus z', [23] jumlah 10 kelas, [25]/[26] rumus UCS (hanya metadata/judul); pembacaan ulang JSON fold per kelas dari disk tidak dilakukan penuh (angka dibuktikan lewat dokumen primer V8 yang memuat tabel per fold dan keberadaan artefak JSON di scratch); kampanye ML tidak dijalankan ulang; tool sequ-mcp tidak tersedia di sesi ini sehingga pikiran berlapis dicatat manual.

Ledger sitasi primer: `citation_ledger.json` + `citation_crossref.json` (workspace t_e2ee149b).
