# V8-E_shk — Profil Kemampuan Engine `shk` (Kerangka 3-Lapisan A/B/C)

> Evaluasi nyata kelas `shk` (SHKRSK_RT ≥ 1, grid 60 detik, jendela fitur [t0−10,t0), label [t0,t0+10)).
> Semua angka di dokumen ini dihasilkan eksekusi nyata pada data Volve lokal
> ( artefak: `scratch/v8_e_shk/e_shk_01_layerA.json`, `e_shk_02_layerB.json`,
> `e_shk_03_layerC.json`, `e_shk_04_semantics.json`; skrip: `v8_e_shk_01_oof_9w.py`,
> `v8_e_shk_02b_events.py`, `v8_e_shk_03_robust_9w.py`, `v8_e_shk_04_semantics.py`,
> `v8_e_shk_10_bins_new.py`, `v8_e_shk_20_windows_new.py` ).
> Kerangka penilaian mengikuti `docs/V8_R1_ABC_SPEC.md` §2.6/§3.3/§4 — BUKAN gate biner.

Riset pendahuluan: statistical-analysis — AUPRC/lift dengan CI95 moving-block bootstrap, prevalensi rendah menuntut precision/recall pada titik operasi praktis, bukan satu gerbang lift. scientific-critical-thinking — reproduksi V6 7/7 sebagai kontrol validitas, fold eksternal F-10/F-12 sebagai uji generalisasi, prasyarat semantik lintas-wellbore diverifikasi sebelum klaim. verification-mandatory — semua angka dari eksekusi nyata; klaim tanpa bukti ditandai "belum terukur".

## (a) Jenis Tugas dan Jenis Engine

- **Jenis tugas:** deteksi anomali/dysfunction sedang berlangsung (status SHKRSK_RT ≥ 1 dari MWD shock-risk display) — bukan diagnosis akar-masalah, bukan prediksi kegagalan mendatang jangka panjang. sub-tugas B adalah deteksi-onset blok shock berkelanjutan (peringatan dini dalam horizon H=10 menit).
- **Engine diuji:** `RF` = supervised ML (RandomForest 300 pohon, min_samples_leaf=5, class_weight=balanced_subsample, seed=42, imputer median — hyperparam identik V6) pada 55 fitur statistik 11 kanal MWD (mean/std/slope/last/frac per jendela 10 menit). LOWO antar sumur (leave-one-well-out).
- **Baseline relevan (per §2.6):** (1) `canary-depth` — RF sama, hanya fitur depth/dbtm; (2) `persistence` — skor biner y_prev_shk (status 10 menit sebelumnya); (3) `prevalence-random` — AUPRC = prev (plafon lift).
- **Opsi ordinal S-B3 (0–3):** belum dievaluasi sebagai model terpisah (belum terukur — prioritas lebih rendah dari uji FAR; binarisasi ≥1 yang dipakai, sesuai praktik V6).
- **Desain fold (9 fold, dideklarasikan sebelum run):** 7 fold ORIG (F-14, F-15A, F-15_S, F-5, F-7, F-9, F-9_A) = train 6 well ORIG lain, komposisi V6 persis → reproduksi AUPRC V6 berlaku sebagai kontrol. 2 fold eksternal baru (F-10, F-12) = train seluruh pool 7 well ORIG (tanpa well uji → tanpa kebocoran), menyerang akar "positif langka" V6.
- **Positif nyata terukur pada fold baru (bukan angka spek):** F-10 = 146 jendela positif (prev 1,85%; dari 30 bin menit shk_max≥1 → 7.899 jendela eligible), F-12 = 217 (prev 4,01%; 202 bin menit → 5.405 eligible). Catatan: spek V8_R1 menyebut 798/580 baris label mentah; setelah kontrak jendela V6 (bin 60 dtk + feat_valid) yang lolos evaluasi = 146/217 — angka inilah yang dipakai. Reproduksi AUPRC fold ORIG vs V6: **7/7 cocok < 1e-9** (kontrol validitas lolos).

## (b) LAPISAN A — Apakah deteksi bekerja? (semua angka eksekusi nyata, 9 fold)

### A.1 Discrimination (AUPRC + lift vs 3 baseline relevan)

| Fold | pos | prev | AUPRC RF | lift RF | AUPRC depth (canary) | AUPRC persistence | CI95 RF (bootstrap blok 60, 1000x) |
|---|---|---|---|---|---|---|---|
| F-14 | 760 | 6,78% | 0,0918 | 1,35 | 0,0631 | 0,1673 | [0,060; 0,140] |
| F-15A | 41 | 0,63% | 0,0079 | 1,24 | 0,0074 | 0,0063 | [0,002; 0,020] |
| F-15_S | 259 | 2,27% | 0,0285 | 1,26 | 0,0252 | 0,0393 | [0,017; 0,043] |
| F-5 | 240 | 3,36% | 0,1129 | 3,36 | 0,0513 | 0,0452 | [0,060; 0,211] |
| F-7 | 267 | 9,67% | 0,0911 | 0,94 | 0,0818 | 0,4457 | [0,042; 0,154] |
| F-9 | 45 | 2,43% | 0,2381 | 9,79 | 0,0862 | 0,0384 | [0,034; 0,560] |
| F-9_A | 30 | 1,27% | 0,0294 | 2,31 | 0,1727 | 0,0144 | [0,006; 0,080] |
| **F-10 (baru)** | **146** | **1,85%** | **0,0177** | **0,96** | 0,0231 | 0,0236 | — (fold eksternal, V6 match = None) |
| **F-12 (baru)** | **217** | **4,01%** | **0,0425** | **1,06** | 0,0665 | 0,0492 | — (fold eksternal) |

Temuan A.1 (interpretasi, bukan vonis):
- RF mengalahkan canary-depth di 6/9 fold (semua fold ORIG kecuali F-9_A; di F-9_A depth canary 0,1727 ≫ RF 0,0294). Konsisten dengan G2 V6 6/7 — fitur non-depth MENAMBAH di atas kedalaman di mayoritas well lama.
- **Di 2 fold eksternal berpositif-banyak (F-10/F-12), RF lift ≈ 1 (0,96/1,06) dan KALAH dari canary-depth (1,25/1,66) maupun persistence (1,28/1,23).** Ini hasil jujur: akar masalah V6 "positif langka" TERBUKTI bukan satu-satunya penyebab lift tidak mayoritas — pada wellbore baru, sinyal fitur MWD untuk shk lemah bahkan dengan 6–7× lebih banyak positif. Sinyal shk dari fitur MWD bersifat lokal-wellbore.
- Persistence bangkit tinggi di F-7 (0,4457) dan F-14 (0,1673) — dua well dengan prev tertinggi: shk di well ini banyak berupa blok panjang → deteksi "status kemarin-menit" sudah kuat. Persistence mengalahkan RF AUPRC di 4/9 fold (F-7, F-14, F-10, F-12).

### A.2 FAR pada titik operasi praktis (inti §3.3 — bukan cuma lift)

Grid tau tetap (pra-reg sebelum hasil): alarm = transisi negatif→positif prediksi; FP_alarm = alarm tanpa y=1 dalam [t, t+H), H=10 menit; FAR dihitung per 24 jam operasi negatif.

| Fold | tau=0.05: P / R / FAR24h | tau=0.10 | tau=0.20 | tau=0.30 | tau=0.50 |
|---|---|---|---|---|---|
| F-14 | 0,080 / 0,312 / 48,1 | 0,099 / 0,126 / 18,9 | 0,260 / 0,045 / 4,8 | 0,259 / 0,009 / 0,7 | — / 0 / 0 |
| F-15A | 0,007 / 0,341 / 31,1 | 0,007 / 0,122 / 24,1 | 0 / 0 / 3,1 | 0 / 0 / 0,7 | — / 0 / 0 |
| F-15_S | 0,033 / 0,533 / 48,8 | 0 / 0 / 22,5 | 0 / 0 / 0,1 | — / 0 / 0 | — / 0 / 0 |
| F-5 | 0,039 / 0,792 / 45,9 | 0,064 / 0,496 / 48,8 | 0,185 / 0,212 / 8,3 | 0,319 / 0,121 / 2,9 | — / 0 / 0 |
| F-7 | 0,119 / 0,730 / 47,3 | 0,059 / 0,154 / 57,7 | 0 / 0 / 12,1 | 0 / 0 / 5,8 | — / 0 / 0 |
| F-9 | 0,023 / 0,711 / 48,6 | 0,031 / 0,644 / 53,4 | 0,096 / 0,556 / 35,9 | 0,177 / 0,489 / 14,4 | 0,552 / 0,356 / 3,2 |
| F-9_A | 0,015 / 1,000 / 35,9 | 0,025 / 0,800 / 63,1 | 0,052 / 0,167 / 19,8 | 0 / 0 / 5,6 | — / 0 / 0 |
| F-10 | 0,013 / 0,178 / 40,7 | 0,012 / 0,041 / 18,4 | 0 / 0 / 0,9 | — / 0 / 0 | — / 0 / 0 |
| F-12 | 0,045 / 0,756 / 43,9 | 0,047 / 0,419 / 41,9 | 0,020 / 0,028 / 10,0 | 0 / 0 / 2,2 | — / 0 / 0 |

Klasifikasi pemakaian §3.3 ( FAR ≤ 1/24 jam = alarm otomatis; ≤ 6/24 jam = tren/pemantauan; > 6 = screening ):
- **FAR ≤ 6/24 jam DENGAN recall > 0 hanya tercapai di 4 titik dari 9 fold:** F-14 tau 0,20 (P 0,26 / R 0,045 / FAR 4,8) dan tau 0,30 (FAR 0,7), F-5 tau 0,30 (P 0,32 / R 0,121 / FAR 2,9), F-9 tau 0,50 (P 0,55 / R 0,356 / FAR 3,2). Di fold lain, menekan FAR ke ≤ 6/24 jam menghasilkan recall = 0.
- **FAR ≤ 1/24 jam dengan recall > 0: TIDAK tercapai di fold mana pun** (semua ambang yang menghasilkan FAR ≤ 1 menghasilkan 0 alarm / recall 0).
- Ambang anggaran-FAR yang DIKALIBRASI dari kelas latih (target 1/24 jam dan 6/24 jam) menghasilkan **0 alarm di SEMUA fold uji** (tau 0,97–0,999; test window rate ~0) → kalibrasi ambang lintas sumur TIDAK transfer. Ini batas nyata, bukan kegagalan hitung.
- Kesimpulan A: deteksi BEKERJA sebagai pemilah berbiaya-cek (screening): pada tau rendah recall 0,18–1,0 dengan FAR 31–49/24 jam (≈ 1–2 alarm/jam negatif — beban besar); presisi pada titik hemat-awas (FAR ≤ 6/24 jam) 0,18–0,55 dengan recall 0,009–0,356. Tidak ada titik operasi terukur yang memenuhi syarat alarm-otomatis.

## (c) LAPISAN B — Nilai maintenance (peringatan sebelum kondisi memburuk)

Definisi pra-reg (v8_e_shk_02b): event = run anchor y=1 berurutan (gap ≤ 2 menit digabung); **event berkelanjutan** = run ≥ 5 menit; B1 = fraksi onset event berkelanjutan yang punya alarm engine dalam horizon [te−H, te), H=10 menit; T_lead = menit dari alarm terakhir ke onset. Baseline = persistence (y_prev_shk).

| Fold | event sht/telanjut | B1 @tau0.05 | T_lead med (mnt) | B1 persistence | FP engine (tau0.20) | FP display baseline | kurangi_ragu (tau0.20) |
|---|---|---|---|---|---|---|---|
| F-14 | 8 / 60 | 0,217 | 3,0 | 0,167 | 35 | 31 | −0,13 |
| F-15A | 2 / 4 | 0,000 | — | 0,000 | 14 | 5 | −1,80 |
| F-15_S | 2 / 23 | 0,348 | 6,0 | 0,087 | 1 | 7 | +0,86 |
| F-5 | 6 / 24 | 0,208 | 2,0 | 0,083 | 40 | 23 | −0,74 |
| F-7 | 5 / 14 | 0,286 | 5,0 | 0,071 | 21 | 19 | −0,11 |
| F-9 | 3 / 3 | 0,333 | 9,0 | 0,000 | 45 | 13 | −2,46 |
| F-9_A | 0 / 3 | 0,000 | — | 0,000 | 32 | 0 | n/a (display 0) |
| F-10 | 1 / 14 | 0,071 | 5,0 | 0,071 | 5 | 4 | −0,25 |
| F-12 | 8 / 18 | 0,111 | 5,5 | 0,056 | 36 | 27 | −0,33 |

Nilai B terukur:
- **Waktu peringatan:** pada tau 0,05, onset event berkelanjutan yang terdeteksi diawali alarm median 2–9 menit sebelum onset (median global antar-fold = 5,0 menit; fold dengan deteksi: 7 dari 9). Sebagian onset punya lead ≥ 30 menit (field pct_onset_Tlead_ge_30menit di JSON per fold). Cakupan onset (B1) 0–0,348 — artinya 65–100% onset TIDAK berperingatan pada ambang ini.
- **RF ≥ persistence untuk B1 di 9/9 fold** (persistence 0–0,167) → engine ML MENAMBAH nilai peringatan dini di atas status-kemarin, meski AUPRC-nya sering kalah (persistence AUPRC tinggi justru karena blok panjang = event mudah "terlanjur").
- **B3 (pengurangan pemeriksaan vs display status-quo): NEGATIF di sebagian besar titik operasi** — pada tau ≤ 0,20, FP engine 1–45 per fold vs FP display 0–31 → kurangi_ragu −0,11 s/d −53,75 (engine menambah beban cek, bukan mengurangi). Positif hanya pada tau ≥ 0,30 (mis. F-14 tau 0,30: +0,84; F-9 tau 0,50: +0,69) atau saat n_alarm = 0 (trivial, bukan prestasi).
- **B4 (margin status-awal):** ≈ T_lead di atas — 2–9 menit median. Ini margin tipis; berguna untuk "cek sekarang / kurangi parameter" bukan untuk perbaikan berat terencana.
- Ambang anggaran-FAR (1/24h & 6/24h) dari kelas latih: 0 alarm di semua fold → B1 = 0 di semua fold. Kalibrasi lintas sumur tidak menghasilkan peringatan sama sekali.

Ringkasan B: ada nilai peringatan dini nyata (lead 2–9 menit, cakupan ≤ 35%, ML > persistence 9/9) tetapi **hanya pada pengaturan ber-FAR-tinggi**; pada pengaturan hemat-awas cakupan mendekati 0 dan klaim "mengurangi pemeriksaan" tidak terpenuhi. Nilai maintenance = **peringatan situasional untuk operator yang siap menindak cepat**, bukan pengganti display MWD.

## (d) LAPISAN C — Robustness (kelangsungan pakai)

- **C1 stabilitas antar-fold:** lift RF spread 0,94–9,79 (max−min = 8,85); AUPRC spread 0,230; lebar CI95 median 0,074, maks 0,525 (F-9, fold kecil). Ketidakstabilan lift yang ditandai V6 **terkonfirmasi terukur** — dan fold eksternal F-10/F-12 (lift 0,96/1,06) menunjukkan sebarannya tidak sekadar noise fold kecil: ada wellbore tempat sinyal ~nol.
- **C2 regime operasi (kuartil depth/RPM/SWOB per fold uji):** worst-case penurunan relatif AUPRC vs overall fold: depth −0,49 s/d −0,93 di 7/9 fold (positif hanya F-15A +0,40, F-9_A +0,82); RPM −0,05 s/d −0,87; SWOB −0,14 s/d −0,86. **Performa memburuk tajam pada kuartil kedalaman/RPM/SWOB tertentu** → engine tidak boleh dipakai buta lintas-regime tanpa anotasi kondisi operasi.
- **C3 drop-channel & noise:** retrain tanpa TFLO: rel_drop > 0,20 hanya F-9 (0,379); tanpa TFLO+SPPA: hanya F-9 (0,377) & F-9_A (0,378); 6/9 fold robust (rel_drop < 0,20 atau negatif = skor naik). Noise gauss σ/10 pada fitur uji: rel_drop > 0,20 hanya F-9 (0,400); 8/9 fold robust. F-9 (fold dengan lift tertinggi 9,79!) justru paling rapuh — lift tertinggi datang dari ketergantungan kanal tunggal = waspada terhadap hasil "spektakuler" per fold.
- **C4 ketidakpastian & underpowered:** CI95 bootstrap blok 60 dilaporkan per fold (tabel A.1); n_pos < 30 = underpowered — tidak ada fold 9-well yang di bawah 30 (F-9_A = 30, F-15A = 41, F-9 = 45 = marginal). Fold lama V6 F-4 (50) & F-15 (13) tidak ada di pool windows V6-E1 (F-15 = 13 underpowered menurut spek; tidak dievaluasi ulang di sini — **belum terukur** di run ini).
- **C-semantik skala ordinal 0–3 (prasyarat lintas-wellbore, e_shk_04_semantics.json):** skala 0–3 ada di SEMUA well (F-10: 69.062/53/54/23; F-12: 25.396/193/224/157; F-14: 21.463/93/55/32; dst.). Tapi **severity-mix berbeda nyata**: F-12 punya 66% non-null pada level ≥ 2 (381/574), F-14 hanya 40% (87/218), F-15_S 49%. Binarisasi ≥ 1 menyatukan event yang severity-nya berbeda antar well → salah satu sumber lift lintas-wellbore yang tidak stabil. VAR_F-5_alt: SHKRSK_RT tidak ada di kolom (error, dilaporkan).
- **Kualitas sensor:** non-null SHKRSK_RT hanya 0,7–8% dari baris (mis. F-10: 69.192/773.674) — kanal shock hanya di-log saat drilling aktif; ini menaikkan noise prevalence estimasi tapi tidak membatalkan metrik (eligible = jendela feat_valid & valid_shk).

Ringkasan C: cukup tepercaya untuk **pemantauan dengan anotasi beban-kerja dan kalibrasi lokal per wellbore**; tidak cukup untuk klaim generalisasi otomatis — spread lift 8,85 + drop regime 50–93% + severity-mix beda adalah tiga batas terukur.

## (e) KESIMPULAN — KEMAMPUAN, BATAS PAKAI, KEKUATAN BUKTI

**Jenis engine:** ML (RF, supervised) + baseline persistence — tugas deteksi anomali/dysfunction (bukan diagnosis, bukan prediksi kegagalan jauh).

### LAYAK untuk (dengan bukti):
1. **Pemantauan-tren / screening berbiaya-cek-tinggi** — bukti: pada tau 0,05–0,10, recall 0–1,00 (mayoritas well 0,18–0,79 pada tau 0,05) dengan FAR 18–63/24 jam; presisi 0,00–0,12. Cocok sebagai panel anotasi sekunder di ruang rig: menandai menit-menit yang layak driller cek, dengan pemahaman 1–3 alarm per jam negatif.
2. **Peringatan dini situasional (lead 2–9 menit) pada wellbore yang sudah dikalibrasi lokal** — bukti: B1 0,07–0,348 @tau0,05, T_lead median 2–9 menit (median global 5,0), RF ≥ persistence B1 di 9/9 fold. Nilai tambah ML di atas persistence TERUKUR untuk sub-tugas onset.
3. **Titik operasi hemat-awas (FAR ≤ 6/24 jam) pada SEBAGIAN well** — bukti: 4 titik terukur (F-14 tau 0,20/0,30; F-5 tau 0,30; F-9 tau 0,50) dengan P 0,18–0,55, R 0,009–0,356. Pemakaian wajar: alarm bernada "periksa/mengurangi parameter" yang outcome-nya murah.
4. **Sinyal fitur non-depth MENAMBAH di atas kedalaman di well lama** — bukti: RF > canary-depth di 6/9 fold (A.1); G2 V6 6/7 tereplikasi (reproduksi AUPRC 7/7 < 1e-9).

### BELUM LAYAK untuk (dengan bukti):
1. **Alarm otomatis kritis (FAR ≤ 1/24 jam)** — bukti: TIDAK ada titik operasi terukur di 9 fold yang mencapai FAR ≤ 1/24 jam dengan recall > 0; semua ambang hemat-awas menghasilkan recall = 0. Syarat §4 tidak terpenuhi — bukan soal ambang digeser, memang tidak ada di kurva.
2. **Kalibrasi ambang otomatis lintas-wellbore** — bukti: ambang anggaran-FAR dari kelas latih (tau 0,97–0,999) menghasilkan 0 alarm di SEMUA fold uji; kalibrasi harus lokal per well.
3. **Generalisasi prediksi ke wellbore baru** — bukti: fold eksternal F-10/F-12 (146/217 positif — fold TERKUAT kedua/ketiga dari sisi jumlah positif) lift RF 0,96/1,06 dan kalah dari canary-depth. Prediktor shk lintas-wellbore dari fitur MWD tidak terbukti.
4. **Pengurangan pemeriksaan tak perlu (B3)** — bukti: kurangi_ragu negatif (−0,11 s/d −53,75) di hampir semua titik tau ≤ 0,20; engine MENAMBIH beban cek vs display status-quo pada pengaturan yang menghasilkan peringatan bermakna.
5. **Pemakaian buta lintas-regime operasi** — bukti: penurunan AUPRC hingga 49–93% pada kuartil kedalaman/RPM/SWOB tertentu di 7/9 fold (C2).
6. **Ordinal S-B3 (0–3) sebagai model** — belum terukur (binarisasi ≥ 1 yang dievaluasi). Severity-mix antar well berbeda nyata (C-semantik) → peluang, bukan klaim.

### Kekuatan bukti:
- **Sedang-kuat untuk A & B:** reproduksi AUPRC V6 7/7 < 1e-9 (validitas pipeline), 9 fold nyata termasuk 2 fold eksternal tanpa kebocoran, grid titik operasi pra-reg, CI95 bootstrap.
- **Sedang untuk C:** drop-channel/noise/regime terukur penuh; CI fold kecil lebar (maks 0,525) → kesimpulan fold kecil dijaga konservatif.
- **Belum terukur:** model ordinal 0–3; fold F-4/F-15 (tidak ada di pool windows); kalibrasi ambang per-well (hanya uji transfer lintas-well yang gagal — per-well calibration sendiri belum diuji); onset lead ≥ 30 menit hanya dilaporkan per-fold di JSON, belum diringkas silang-fold.

### Baris status (bukan LULUS/GAGAL):
`shk` = **kapabilitas TERBATAS-TERVERIFIKASI**: deteksi kondisi + peringatan dini berguna pada pengaturan berbiaya-cek-tinggi dan well terkalibrasi; TIDAK memenuhi syarat alarm-otomatis dan TIDAK generalisasi otomatis ke wellbore baru. Rekomendasi pemakaian dalam alat PdM: **komponen anotasi/pemantauan dengan beban-kerja ditampilkan ke operator**, digabung dengan persistence sebagai engine murah, bukan pengendali otomatis.

---
Sumber data: `data/volve/witsml_parsed/*.csv` (9 well), binning+jendela kontrak V6 (`scratch/v8_e_shk/bins_new`, `windows_new`, `scratch/v6_e1/windows`). Artefak hasil: `scratch/v8_e_shk/e_shk_01_layerA.json` (9 fold, grid + budget + CI), `e_shk_02_layerB.json` (B1/T_lead/B3 per fold), `e_shk_03_layerC.json` (C1–C4), `e_shk_04_semantics.json` (skala 0–3 per well). Pra-registrasi: header skrip 01/02b/03.




