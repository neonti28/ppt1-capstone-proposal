# V11-A_CLAIM: AUDIT ARITMETIKA KLAIM KEDUA KANDIDAT

Task: `t_ed19957f` [Auditor Klaim] · Board: `capstone-v11-vs` · 2026-10-15 (WIB).
Peran: auditor hitung-ulang independen. Seluruh angka di bawah dihitung ulang dari file primer
(JSON scratch, REGISTRY kode, file data, dokumen V8/V9/V10) dengan eksekusi nyata, bukan kutip
dokumen lain. Kandidat 1 = `docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.v3_arsip.md` + `.ipynb`;
kandidat 2 = `docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md` + `.ipynb`. Dokumen ini tidak
menyimpulkan versi baru/lama maupun pemenang (kewenangan PM-FINAL).

> Riset pendahuluan: `scientific-critical-thinking` - memisahkan OBSERVED (angka recompute)
> dari DERIVED/HYPOTHESIS; setiap klaim diberi falsifier (nilai primer yang bisa membatalkannya);
> status kepastian per angka (COCOK / SALAH / TIDAK-TERVERIFIKASI / DIDUKUNG-primer).
> Riset pendahuluan: `verification-mandatory` - bukti mentah per klaim dari eksekusi sesi ini;
> bagian "belum diverifikasi" ditulis eksplisit (§G); larangan mengarang angka dipatuhi:
> semua nilai primer di bawah berasal dari skrip yang dijalankan (daftar skrip §H).
> Riset pendahuluan: `statistical-analysis` - rasio kebenaran klaim dihitung per kandidat dengan
> penyebut = jumlah klaim yang benar-benar diklaim (bukan checklist), sehingga ketidakhadiran
> angka tidak dihitung sebagai kesalahan aritmetika, hanya sebagai cakupan; angka kampanye
> dinilai per kampanye (V6/V8/V9) sesuai anotasi sumbernya.
> Riset pendahuluan: `sequentialthinking` (sequ-mcp, 6 pikiran): inventaris checklist 30 angka
> -> recompute primer -> pemindaian kehadiran angka di kedua kandidat -> verifikasi angka
> tambahan -> parity md-ipynb -> susun ledger + rasio.

---

## A. SUMBER PRIMER YANG SAYA HITUNG ULANG SENDIRI (eksekusi sesi ini)

| Primer | Metode eksekusi | Hasil |
|---|---|---|
| REGISTRY `code/v9_i1_pipeline.py` | importlib exec modul, hitung dict REGISTRY | 7 engine; 27 head (4+4+4+6+4+2+3); tier 12 PERINGATAN-BERPENGAWAS / 13 TREN / 2 BELUM LAYAK PAKAI; lapisan L0 5 / L1 11 / L2 9 / L3 2; AUTO_CRITICAL_SLOTS 0; SEED 42; ambang vib 32,17405; stuck H=10 mnt; hyd abs(z)>2 |
| `data/USROP_labeled.csv` | csv reader | 198.928 baris, 18 kolom; 12 kolom sensor/measurement (sisa: Unnamed:0, well, label, MSE, D_exp, ROC_coef) |
| `data/volve/labels_curated_v2_log.json` | json | 884 kejadian; uncertain 571 / no 263 / yes 50 |
| `scratch/v9_d1/datasets/*.csv.gz` | gzip+csv hitung baris | 6 dataset: 23.922+35.906+56.495+5.555+52.509+118.567 = 292.954 baris; positif (kolom y_*) 19.195 total |
| `scratch/v9_d1/lowo_*.json` | json | fold 4+9+9+2+4+9 (vib, ssi, shk, stuck_k1, stuck_k2, hyd_ki) = 37 fold |
| `scratch/v9_e_ml/*_RESULTS.json` | json | n_features 55 (4/4 engine); seed 42; fold 4+9+9+4 = 26 fold |
| `scratch/v6_e1/toolwear_windows.csv` | csv | 469 baris; 32 kolom = 27 fitur (9 stat x 3 sumbu) + 5 meta |
| `data/bo_tspp/TSPP{1..4}.csv` | csv | 21.120+8.499+12.533+10.753 = 52.905 baris |
| `data/volve/witsml_parsed/*.csv` | hitung baris biner | 10 CSV = 9.935.698 baris; daftar FILES `code/v9_d1_01_bins.py` = 9 CSV (tanpa VAR_F-5_alt) |
| 8 CSV parser V3 | turunan aritmetika dari wc per file | 9.935.698 - 773.674 (F-10) - 2.081.567 (F-12) = 7.080.457; jumlah eksplisit 8 file non-F10/F12 = 7.080.457 (cocok) |
| `data/volve/witsml_raw/` | os.walk path-based | tubular 192; bhaRun 161; trajectory 63; wbGeometry 27; mudLog 8; total file 20.086 = 18.814 XML + 1.272 txt |
| `Well_picks_Volve_v1.dat` | parse blok | 557 baris; 409 baris data; 35 blok wellbore |
| `kaggle_volve_witsml_F9A.zip` (time.csv) | zipfile+csv | 419.747 baris data; 239 kolom (modul csv) |
| `scratch/v9_eval_c/v9_eval_c_RESULTS.json` | json | hyd hybrid FP 2091->927 (-55,7%) 9/9; hybrid FAR 14,624-58,431; ssi hybrid FP 26->7 (-73,1%) 7/7; hyd K-ii q95 TP 0 FP 177, sign-flip 6.377/8.107 = 78,66%, CI memuat prev; canary 3-RMS 0,5164-0,6124; tool_wear K-i cp 8/8, precision run 0,50, FP 1-3, TLead 20-36 dtk; vib RF AUPRC 0,4405-0,9117 |
| `scratch/v9_e_ml/v9_e_ML_vib_RESULTS.json` | json | lift per fold 1,6133 / 2,3620 / 3,4972 / 1,6289; determinism_check rerun_identical=False, max_abs_diff 2,22e-16 |
| `scratch/v9_eval_a/v9_eval_a_RESULTS.json` | json | vib RF tau0,5 FAR 4,149-496,09 (119,6x); vib rule P 0,868-0,952; hyd persistence P 0,6145-0,8986; hyd persistence FAR_24jam 32,17-109,69; stuck_k1 rule P 0,9238-0,9662; hyd hybrid P 0,7236-0,9484 |
| `docs/V9_R1_JUSTIFICATION.md` baris 143-145 | baca | stuck E3 V8: AUPRC 0,326-0,331 < canary 0,410 (beranotasi V8); kontrol positif 0/10; FAR stuck 9,9-1.440; anchor Crossformer 2,67-7,37 mnt |
| `docs/V9_EVAL_B_LAYERB.md` baris 99-195 | baca | persistence-EVENT stuck TLead 4,5-8,5 mnt, median fold-median 7,0; RF tau0,05 B1 0,51-1,00 TLead 10-11,5 |
| `docs/V8_M1_CAPABILITY_MAP.md` baris 160-178 | baca | rekap tier V8: 0 alarm + 3 peringatan + 2 bersyarat + 2 tren = 7 |
| `docs/V10_PM1_OUTLINE.md` baris 158-172 | baca | kontrak grid 60 dtk (rig) / 1 dtk (bengkel); jendela [t0-10, t0); statistik mean/std/slope/last/frac |
| `docs/V8_A1_CAPABILITY_AUDIT.md` baris 110 | baca | 114/121 klaim terverifikasi persis, "Tidak ada karangan", 6 selisih penyajian |
| `docs/V8_E_hyd_CAPABILITY.md` baris 33,100 | baca | hyd K-ii RF V8 AUPRC 0,228; konservatif 0,0301 |
| `code/v9_e_ML_01_train.py` | grep | GradientBoostingClassifier x3; HistGradientBoosting x0; RandomForestClassifier x5; LogisticRegression x3 |
| Field brier/ece di JSON kampanye V9 | grep code/ + json | 0 field di `v9_e_ML_*_RESULTS.json`; kata "brier/ece" hanya di kode eksperimen lama (42-64) dan komentar 2 modul V9 |
---

## B. LEDGER CHECKLIST 30 ANGKA (V11_PROTOCOL sec.4): K1 vs PRIMER vs K2

Status: COCOK = nilai klaim sama dengan primer; SALAH = nilai keliru (nilai benar dicatat);
PARSIAL = sebagian butir cocok; TIDAK-HADIR = angka tidak diklaim di dokumen kandidat
(mengikuti aturan 2a PM-0: tidak dihitung cocok); DIDUKUNG = klaim bertaut dokumen primer
yang saya baca tetapi bukan angka yang bisa dihitung ulang dari data mentah di sesi ini.

| # | Butir (primer hasil recompute saya) | Kandidat 1 (v3_arsip.md) | Kandidat 2 (.md terbaru) |
|---|---|---|---|
| 1 | 7 engine (registry) | COCOK ("tujuh mesin", "7 dari 7") | COCOK ("7 engine", Bab 1) |
| 2 | 11 klaim = 3x1+4x2 (registry) | TIDAK-HADIR | COCOK (Bab 1 paragraf + tabel 11 klaim) |
| 3 | 27 head sebaran 4+4+4+6+4+2+3 | TIDAK-HADIR | COCOK (tabel 27 baris head + rekap) |
| 4 | tier head 12/13/2 (registry) | TIDAK-HADIR (K1 hanya klaim tier level engine, lihat #29) | COCOK (baris 260 dan 3040) |
| 5 | lapisan L0 5 / L1 11 / L2 9 / L3 2 | TIDAK-HADIR | COCOK (baris 261, 3039, 3116, 3142) |
| 6 | AUTO_CRITICAL_SLOTS 0 (registry) + 0/7 engine layak alarm | COCOK ("Alarm otomatis kritis 0"; benar di tingkat engine, konsisten dgn registry 0 slot) | COCOK (AUTO_CRITICAL_SLOTS = 0, baris 178/261/3026) |
| 7 | ambang vib VIBLAT_RT >= 32,17405 | TIDAK-HADIR | COCOK (tabel 1.1, 1.2, Bab 2, Bab 6) |
| 8 | stuck onset H = 10 menit | TIDAK-HADIR | COCOK (baris 202/215/300/1257) |
| 9 | hyd K-i abs(z) > 2 | TIDAK-HADIR | COCOK (baris 619/1569/1987) |
| 10 | SEED 42 | COCOK (baris 174 "Benih acak tetap (42)") | COCOK (baris 303/1171/1495 dll) |
| 11 | USROP 198.928 baris / 18 kolom | COCOK (198.928 baris x 12 sensor; 12 sensor benar dari 18 kolom; baris 127) | COCOK (198.928 baris, 18 kolom; baris 929/979) |
| 12 | 884 kejadian; 571/263/50 | COCOK (884; 571/263/50 tidak diklaim; baris 127/291) | COCOK (884 kejadian; 571/884 uncertain; baris 930/1014) |
| 13 | 6 dataset latih 292.954 baris | TIDAK-HADIR | COCOK (baris 905/1208/1221; positif 19.195 juga cocok) |
| 14 | 37 fold LOWO (4+9+9+2+9+4) | TIDAK-HADIR, dan mengklaim angka tandingan yang SALAH: "tujuh nilai lipatan" (lihat K1-X9/X10) | COCOK ("37 lipatan (4+9+9+2+9+4)", baris 1208/1224/1317) |
| 15 | n_features 55 (11 kanal x 5 stat) | COCOK (baris 136) | COCOK (baris 905/1194/1204) |
| 16 | 26 fold kampanye ML | TIDAK-HADIR | COCOK (baris 1532/1662/1712) |
| 17 | tool_wear 469 jendela / 27 fitur | TIDAK-HADIR | COCOK (baris 663/938/1124) |
| 18 | TSPP 52.905 baris | TIDAK-HADIR | COCOK (baris 940/1148/1154; per file juga cocok) |
| 19 | WITSML: 10 CSV 9.935.698; 8 CSV 7.080.457 | SALAH ("8 CSV WITSML berbasis waktu (8.474.172 baris)", baris 127; primer 7.080.457; 8.474.172 nihil di seluruh primer) | COCOK (10 CSV 9.935.698; 8 CSV parser V3 7.080.457 dengan jumlah eksplisit per file; baris 928/951-957/1415) |
| 20 | XML 192/161/63/27/8 | PARSIAL (192 tubular, 161 bhaRun, 63 trajectory, 8 mudLog benar; wbGeometry 27 tidak disebut; baris 128) | COCOK (192/161/63/27 + 8 mudLog pada tabel inventaris, baris 931-935) |
| 21 | 409 picks / 35 wellbore | TIDAK-HADIR | COCOK (baris 943/1143) |
| 22 | F-9A time.csv 419.747 baris / 239 kolom | TIDAK-HADIR | COCOK (baris 937/1107) |
| 23 | hyd hybrid FAR 14,6-58,4; FP 2091->927 (-55,7%) 9/9 | TIDAK-HADIR | COCOK (baris 630/633/814; JSON eval_c cocok persis) |
| 24 | ssi hybrid FP 26->7 (-73,1%), <= rule 7/7 | TIDAK-HADIR | COCOK (baris 560/689/776) |
| 25 | stuck E3 V8 0,326-0,331 < canary 0,410 | TIDAK-HADIR | COCOK dengan anotasi V8 (baris 712/816; sesuai petunjuk protokol angka beranotasi) |
| 26 | tool_wear cp 8/8; precision 0,50; FP 1-3; TLead 20-36 dtk; artefak termal 0/8 | TIDAK-HADIR | COCOK (baris 506/671-673; JSON eval_c cocok; "0/8" DIDUKUNG dokumen EVAL_C) |
| 27 | hyd K-ii q95 TP0 FP177; 6.377/8.107 = 78,7%; CI memuat prev | TIDAK-HADIR | COCOK (baris 636/2335/3112; JSON eval_c cocok) |
| 28 | canary 0,516-0,612; vib AUPRC 0,441-0,912; stuck TLead 4,5-8,5 (med 7,0) | TIDAK-HADIR | COCOK (baris 675/1727; EVAL_B persistence-EVENT cocok) |
| 29 | rekap tier V8 0+3+2+2 = 7 | COCOK (baris 50-56, 260, 309) | COCOK (baris 63-67, 3174, 3384, 3514) |
| 30 | grid 60/1 dtk; jendela [t0-10,t0); 5 statistik | PARSIAL (5 statistik benar, baris 136; grid dan jendela tidak disebut) | COCOK (baris 296/1187/1294) |

Rekap checklist: Kandidat 1 = 7 COCOK penuh (butir 1,6,10,11,12,15,29) + 2 PARSIAL (20,30)
+ 1 SALAH (19) + 20 TIDAK-HADIR. Kandidat 2 = 30 COCOK, 0 SALAH, 0 TIDAK-HADIR.
Skor baku 2a (PM-0: 18 x cocok/30): K1 = 18 x 7/30 = 4,2 (parsial tidak dihitung cocok);
K2 = 18,0. Angka ini diserahkan apa adanya; penilaian akhir kriteria = PM-FINAL.
---

## C. LEDGER ANGKA TAMBAHAN (di luar checklist; >=10 per kandidat)

### C.1 Kandidat 1 (15 angka tambahan)

| ID | Klaim kandidat 1 | Primer (recompute/baca sesi ini) | Verdict |
|---|---|---|---|
| K1-X1 | 8 CSV WITSML = 8.474.172 baris (baris 127) | 8 CSV parser V3 = 7.080.457 (wc per file; turunan 9.935.698-773.674-2.081.567); sumber primer K1 sendiri `V3_WITSML_PARSE_REPORT` juga 7.080.457 | SALAH (nilai benar 7.080.457) |
| K1-X2 | 17.368 berkas Databricks (baris 128/292) | recount `find -type f` oleh kartu D1 = 17.368 (V11_DATA1 P22) | COCOK (recount D1; tidak saya ulang) |
| K1-X3 | 20.086 XML WITSML mentah (baris 128) | os.walk saya: total 20.086 file = 18.814 XML + 1.272 txt | COCOK sebagai total file; label "XML" longgar (1.272 bukan XML) |
| K1-X4 | 7.150 log XML (baris 128) | recount V6_A1 E1 (os.walk log/*.xml) = 7.150; D1 P11 7.150 | COCOK |
| K1-X5 | 1.759 laporan DDR (baris 291) | `ddr.parquet` = 1.759 baris (pyarrow, D1 P23) | COCOK |
| K1-X6 | 121 klaim, 0 fabrikasi, 6 selisih penyajian (baris 231/264/295/328) | V8_A1 baris 110: 114/121 terverifikasi, "Tidak ada karangan", 6 selisih | COCOK |
| K1-X7 | USROP "198.928 x 12 sensor" | header 18 kolom, 12 di antaranya kolom sensor | COCOK |
| K1-X8 | "Leave-One-Wellbore-Out: dari tujuh sumur, enam untuk latih" (baris 182) | 9 wellbore CSV dipakai; fold per engine 4/9/9/2/4/9 | SALAH (primer: 9 wellbore; tidak ada skema 7-sumur) |
| K1-X9 | "LOWO memberi tujuh nilai lipatan" (baris 182) | 37 fold total; per engine 2,4,4,9,9,9; nihil engine dgn 7 fold | SALAH |
| K1-X10 | "Histogram-based Gradient Boosting" sbg model utama kedua (baris 158) | `v9_e_ML_01_train.py`: GradientBoostingClassifier x3, HistGradientBoosting x0 | SALAH (kode memakai GradientBoostingClassifier) |
| K1-X11 | "Skor Brier & ECE" sbg metrik evaluasi (baris 219) | 0 field brier/ece di 4 JSON kampanye V9; hanya di kode eksperimen lama | TIDAK-TERVERIFIKASI utk kampanye V9 (boleh sbg rencana, tidak ada angkanya) |
| K1-X12 | "Benih acak tetap (42); pelaksanaan ulang wajib identik" (baris 174) | benih 42 COCOK; JSON vib determinism_check: rerun_identical=False (max_abs_diff 2,22e-16) | KOIN: benih COCOK; klaim "wajib identik" bertentangan dgn primer (E_ML kartu sebelumnya: KOREKSI) |
| K1-X13 | "kontrol positif stuck 0/10" (baris 272) | V9_R1 baris 145: kontrol-positif 0/10 | COCOK |
| K1-X14 | "ambang lift 1,5" sbg pembanding historis (baris 92) | gate lift>=1,5 tercatat di dokumen V6/V10 (baris 3380/3413); bukan bagian kampanye V9 | DIDUKUNG (konteks historis, bukan klaim hasil V9) |
| K1-X15 | "4 dataset eksternal terverifikasi" (baris 12) | konsisten dgn V6_D2 (4 dataset eksternal); tidak saya hitung ulang unduhan | DIDUKUNG |

### C.2 Kandidat 2 (15 angka tambahan)

| ID | Klaim kandidat 2 | Primer (recompute/baca sesi ini) | Verdict |
|---|---|---|---|
| K2-X1 | 8 CSV parser V3 = 7.080.457 (baris 928/951-957,1415) | jumlah eksplisit 8 file = 7.080.457 (saya hitung dari wc per file) | COCOK eksak |
| K2-X2 | F-10 + F-12 = 2.855.241 (baris 928) | 773.674 + 2.081.567 = 2.855.241 | COCOK |
| K2-X3 | per file: F-7 547.500; F-9 457.545; F-9_A 419.706; VAR_F-5_alt 59.489 (baris 955) | wc saya per file identik | COCOK |
| K2-X4 | total positif 19.195 (baris 1221) | hitung kolom y_* 6 dataset = 19.195 | COCOK eksak |
| K2-X5 | TSPP per file 21.120/8.499/12.533/10.753 (baris 1154) | csv count identik | COCOK |
| K2-X6 | lift vib 1,61/2,36/3,50/1,63 "cocok persis" V8 (baris 537/1735) | JSON vib lift 1,6133/2,3620/3,4972/1,6289 | COCOK |
| K2-X7 | vib FAR tau0,5 menyebar 119x; 4,1-496 (baris 539) | eval_c JSON vib rf far_by_tau 0.5: 4,149-496,09; rasio 119,57 | COCOK |
| K2-X8 | vib rule P stabil 0,87-0,95 (1,1x) | eval_a JSON precision_disp 0,868-0,952, rasio 1,1 | COCOK |
| K2-X9 | shk rule FAR 0,67-6,6, lolos FAR<=6 di 7/9 fold | eval_c JSON far 0,670-6,618 | COCOK |
| K2-X10 | stuck K-i rule P 0,92-0,97 (2 fold) | eval_a JSON stuck_k1 rule P 0,9238-0,9662 | COCOK |
| K2-X11 | hyd hybrid P 0,72-0,95 di 9/9 well | eval_a/eval_c JSON hybrid P 0,7236-0,9484 | COCOK |
| K2-X12 | "K-i persistence P 0,615-0,793" (baris 628) | JSON eval_a persistence P 0,6145-0,8986; V9_EVAL_A baris 151 juga 0,615-0,899; 0,793 = nilai fold F-9 | SALAH (nilai benar 0,615-0,899; 0,793 adalah salah satu fold, bukan maksimum) |
| K2-X13 | "FAR_t 32-111/24jam" (baris 628) | JSON FAR_24jam persistence 32,17-109,69; V9_E_STAT_ENGINE baris 39 menulis "32-111" | DIDUKUNG (kutipan dokumen sumber; JSON ujung atas 109,7, pembulatan sumber tidak ketap) |
| K2-X14 | persistence bit_wear AUPRC 0,679-0,984 (V8) dan 0,119-0,984 (V9, 5/7 fold) | EVAL_C baris bit_wear: 0,119-0,984; anotasi V8 terpisah | COCOK |
| K2-X15 | "481/329 kandidat onset terverifikasi" (baris 585) | hanya ditemukan sebagai kutipan di V10_R1_ALASAN; tidak ada primer data yang saya temukan | TIDAK-TERVERIFIKASI |

Angka tambahan K2 lain yang terverifikasi (dicatat singkat): AUPRC hyd K-ii 0,228 vs 0,030
(V8_E_hyd baris 33/100 COCOK); 62,3% nodata CRPM = 22.385/35.906 (EVAL_C; aritmetika benar,
35.906 = baris dataset ssi); 582/884 kejadian dalam rentang CSV (D1 recount); FAR stuck
9,9-1.440 (V9_R1); delay median hyd 0-3,5 mnt (EVAL_B).

---

## D. RASIO KEBENARAN KLAIM

Penyebut = jumlah klaim angka yang benar-benar tertulis di dokumen kandidat (angka yang bisa
diverifikasi ulang), bukan jumlah butir checklist; ketidakhadiran tidak dihitung sebagai
kesalahan aritmetika (tercatat sebagai cakupan di §B).

| Kandidat | Klaim angka terverifikasi | COCOK | SALAH | TIDAK-TERVERIFIKASI | DIDUKUNG-primer | % terbukti ketat (COCOK/total) | % dgn DIDUKUNG | Angka karangan terbukti |
|---|---|---|---|---|---|---|---|---|
| Kandidat 1 | 34 | 26 | 5 | 1 | 2 | 76,5% | 82,4% | 0 (kesalahan = salah/keliru kutipan, bukan fabrikasi angka baru) |
| Kandidat 2 | 48 | 44 | 1 | 1 | 2 | 91,7% | 95,8% | 0 |

Rincian SALAH Kandidat 1 (5 klaim unik): 8.474.172 baris WITSML (nilai benar 7.080.457);
"tujuh sumur LOWO / enam latih" (primer 9 wellbore); "tujuh nilai lipatan" (primer 37 fold,
nihil engine dgn 7 fold); "Histogram-based Gradient Boosting" (kode:
GradientBoostingClassifier); "pelaksanaan ulang wajib identik" (JSON:
rerun_identical=False). TIDAK-TERVERIFIKASI (1): "Brier & ECE" sbg metrik kampanye V9
(0 field di JSON). DIDUKUNG (2): gate lift 1,5 (dokumen V6/V10, historis); 4 dataset
eksternal (V6_D2). PARSIAL checklist (wbGeometry 27 tidak disebut; grid/jendela tidak
disebut) tidak dihitung sebagai salah.

Rincian SALAH Kandidat 2 (1 klaim): "K-i persistence P 0,615-0,793" (nilai primer
0,615-0,899; 0,793 = fold F-9, bukan maksimum). TIDAK-TERVERIFIKASI (1): "481/329 kandidat
onset terverifikasi" (hanya ada sbg kutipan dokumen, primer data tidak ditemukan).
DIDUKUNG (2): FAR_t persistence "32-111/24jam" (JSON 32,17-109,69; dokumen sumber
V9_E_STAT_ENGINE menulis 32-111); 582/884 kejadian (recount kartu D1).
---

## E. ANGKA YANG SAMA DIKUTIP KEDUA KANDIDAT: KONSISTENSI & SIAPA YANG BENAR

| Subjek | Kandidat 1 | Kandidat 2 | Primer | Konsistensi |
|---|---|---|---|---|
| 7 engine / 7 dari 7 | 7 | 7 | registry 7 | konsisten, benar |
| Tier engine 0/3/2/2 | 0 alarm, 3 terbukti, 2 bersyarat, 2 tren | identik + rekap head 12/13/2 | V8_M1 + registry | konsisten, benar |
| USROP | 198.928 x 12 sensor | 198.928, 18 kolom | 198.928 baris, 18 kolom (12 sensor) | konsisten (angka baris identik; klaim kolom berbeda tapi dua-duanya benar) |
| Label 884 | 884 | 884 (571/884 uncertain) | 884; 571/263/50 | konsisten, benar |
| Seed 42 | 42 | 42 | SEED=42 | konsisten, benar |
| 55 fitur / 11 kanal | 55 fitur dari 11 kanal | 11 x 5 = 55 | n_features 55 | konsisten, benar |
| 1.759 laporan DDR | 1.759 | 1.759 (baris 3496) | ddr.parquet 1.759 | konsisten, benar |
| 17.368 berkas | 17.368 | 17.368 (baris 3497) | find 17.368 (D1) | konsisten, benar |
| XML per jenis 192/161/63/8 | 192/161/63/8 | 192/161/63/27/8 | os.walk identik | konsisten (K2 lebih lengkap) |
| lift 1,5 (gate historis) | "ambang lift 1,5" | "lift 1,5 tunggal" (baris 424, 3380, 3413) | dokumen V6/V10 | konsisten, konteks historis |
| Jumlah baris WITSML | "8 CSV (8.474.172 baris)" | "10 CSV 9.935.698; 8 CSV parser V3 7.080.457" | wc per file: 10 CSV 9.935.698; 8 CSV 7.080.457 | TIDAK konsisten: K1 8.474.172 salah, K2 benar (jumlah eksak per file) |
| Jumlah fold LOWO | "tujuh nilai lipatan" | "37 lipatan (4+9+9+2+9+4)" | 37 fold; per engine 2/4/4/9/9/9 | TIDAK konsisten: K1 salah, K2 benar |
| Model GB | "Histogram-based Gradient Boosting" | (K2 tidak mengklaim nama model GB di Bab yang saya audit; daftar model = RF/LR/GB) | GradientBoostingClassifier | K1 salah vs kode |
| Determinisme rerun | "pelaksanaan ulang wajib identik" | tidak mengklaim "wajib identik" (K2 menyebut reproduksi ulang dengan hasil cocok pada kampanye terpilih) | rerun_identical=False (vib) | K1 bertentangan primer |

---

## F. PARITAS MD vs IPYNB (mekanis)

Metode: ekstrak sel markdown `.ipynb`, banding token angka dengan `.md` (re,
`\d+([.,]\d+)*`), plus pemetaan kehadiran 30 butir checklist di kedua format.

| Kandidat | Token angka di md | Token di ipynb md | Angka di md yang hilang di ipynb | Selisih | Kehadiran 30 butir md vs ipynb |
|---|---|---|---|---|---|
| Kandidat 1 | 224 | 226 | 0 | token "2" +2 (blok arsip visualisasi 9 baris di ipynb: "versi dokumen sebelumnya" dll) | 30/30 identik (hadir-hadir / tidak-hadir-keduanya) |
| Kandidat 2 | 7.510 | 7.512 | 0 | token "2" +2 (blok arsip visualisasi + artefak literal `\n` di 1 sel Bab 2 yang memecah satu baris menjadi dua) | 30/30 identik |

Kesimpulan parity: substansinya identik di kedua kandidat; selisih hanya blok arsip
visualisasi yang memang hanya ada di `.ipynb` (berlabel "bukan bagian narasi proposal"),
tanpa satu pun angka `.md` yang hilang. Status 4c (parity) lolos untuk kedua kandidat
menurut cek mekanis kartu ini.

---

## G. BELUM DIVERIFIKASI / DI LUAR CAKUPAN (verification-mandatory #3)

1. Angka yang hanya dikutip dari dokumen tanpa primer hitung-ulang di sesi ini:
   17.368 berkas (recount D1, bukan saya), 7.150 log XML (recount V6_A1/D1),
   1.759 DDR (D1 pyarrow), 582/884 (D1), 121 klaim/6 selisih (V8_A1), artefak termal 0/8
   (dokumen EVAL_C; JSON memuat "t_cp TIDAK dominan awal" tanpa angka 0/8 eksplisit),
   62,3% nodata (22.385 tidak saya hitung dari CSV bins).
2. Klaim kandidat 2 yang tidak saya telusuri ke primer: "1.392 komponen tubular",
   "5.561 stasiun survei", "109 section wbGeometry", "124 episode hyd",
   "20.086 XML dari zip Realtime" (bagian lain dari klaim 20.086), jumlah 2.544/2.829 baris
   parity dari kartu lain (kartu ini hanya menghitung token & kehadiran checklist).
3. Kampanye ML tidak dilatih ulang; determinisme diverifikasi lewat JSON
   determinism_check, bukan re-run penuh.
4. Tabel fold per kelas (286 sel Bab 4 K2) tidak diverifikasi ulang di kartu ini
   (cakupan kartu E_ML; kartu ini menghitung ulang sumber primer yang sama untuk angka kunci).
5. `ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN - Copy.md/.ipynb` tidak diaudit (bukan kandidat).
6. Sitasi eksternal (DOI dsb) di luar cakupan kartu ini (cakupan R1).

---

## H. SKRIPT EKSEKUSI, DOKUMEN HASIL, DAN BARIS RISET PENDAHULUAN

Skrip yang dijalankan (workspace `t_ed19957f`): `probe_sizes.py`, `recompute_part1.py`
(registry, USROP, labels, dataset, lowo, ML results, toolwear, TSPP), `recompute_part2.py`
(WITSML wc, XML walk, picks, zip F-9A, labels detail, folds), `recompute_part3.py`
(picks parse proper, ncols csv module, FILES pipeline), `probe_evalc.py`, `probe_numbers.py`,
`probe_numbers2.py`, `verify_extra.py`, `verify_extra2.py` (positif 19.195, lift vib,
grep klaim), `verify_extra3.py` (FAR 119x, hyd persistence P), `verify_extra4.py`,
`verify_extra5.py`, `scan_checklist.py`, `parity_check.py`, `parity_diff.py`,
`parity_lines.py`.

JSON primer di scratch (workspace task ini): `scratch_primary_part1.json`,
`scratch_primary_part2.json`, `scratch_primary_part3.json`, `scratch_primary_part4.json`,
`checklist_scan.json`, `extra_verify.json`, `extra_verify2.json`, `extra_verify3.json`,
`extra_verify4.json`, `extra_verify5.json`, `md_ipynb_parity.json`,
`scratch_v11_a_claim_ledger.json` (rekapan ledger).

Baris riset pendahuluan:
- Riset pendahuluan: `scientific-critical-thinking` - pemisahan data vs interpretasi;
  falsifier per angka (nilai primer yang membatalkan klaim); status kepastian per butir;
  kesalahan kutipan dilaporkan dengan nilai benar, bukan dilunakkan.
- Riset pendahuluan: `verification-mandatory` - bukti mentah per klaim dari eksekusi;
  cross-check dua sumber bila memungkinkan (mis. wc per file + turunan aritmetika;
  EVAL_A JSON + EVAL_C JSON); daftar belum-diverifikasi eksplisit (§G).
- Riset pendahuluan: `statistical-analysis` - rasio dihitung dengan penyebut klaim nyata;
  angka kampanye dinilai per anotasi kampanye (V6/V8/V9); pembulatan sumber dibedakan dari
  kesalahan nilai (mis. "32-111" vs JSON 109,7).
- Riset pendahuluan: `sequentialthinking` (sequ-mcp, 6 pikiran): inventaris checklist ->
  recompute primer -> pemindaian kandidat -> verifikasi tambahan -> parity -> ledger+rasio.

*Selesai V11-A_CLAIM (`t_ed19957f`). Ringkas: Kandidat 1 = 34 klaim angka, 26 cocok,
5 salah, 1 tidak terverifikasi, 2 didukung (76,5% terbukti ketat); Kandidat 2 = 48 klaim,
44 cocok, 1 salah (P hyd persistence 0,615-0,793), 1 tidak terverifikasi (481/329),
2 didukung (91,7% terbukti ketat); nol angka karangan di kedua kandidat; parity md-ipynb
lolos di kedua kandidat; keputusan menang/kalah = PM-FINAL.*
