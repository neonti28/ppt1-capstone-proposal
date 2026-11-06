# V8-E_hyd — EVALUASI KEMAMPUAN kelas `hyd` (KERANGKA 3 LAPISAN A/B/C)

Task: `t_774cc5e4` [Evaluator] · Board: capstone-v8-capability · Tanggal: 2026-10-11 (WIB)
Kerangka: `docs/V8_R1_ABC_SPEC.md` §2.5 + §3.2 (mengganti gate biner V6/V7).
Status: HASIL UJI NYATA — kemampuan + batas + kekuatan bukti. BUKAN vonis LULUS/GAGAL.

> **Riset pendahuluan: `statistical-analysis`** — AUPRC+lift dengan CI95 moving-block
> bootstrap (blok 60, 1.000 resample, seed 42, metode V6 dipertahankan); ambang operasi
> dipilih di TRAIN (bukan pasca-hasil test); <30 positif/fold = UNDERPOWERED dilaporkan.
> **Riset pendahuluan: `scientific-critical-thinking`** — klaim dipisah OBSERVED (angka
> eksekusi run ini) vs hasil replikasi-V6 vs EKSPLORATIF (sensitivitas label ditandai);
> tes pembeda R1 §3.2 dievaluasi dengan outcome jujur; korelasi-vs-kausalitas diuji pada
> uji kejadian-nyata (n=1 episode → klaim kausal TIDAK dinaikkan).
> **Riset pendahuluan: `verification-mandatory`** — semua angka dari eksekusi nyata
> (bukti: skrip + JSON di workspace); replikasi LOWO cocok eksak dengan V6 = cross-check;
> daftar "belum diverifikasi" di §7.
> **Riset pendahuluan: `sequentialthinking`** (5 pikiran) — penataan desain uji per klaim
> sebelum eksekusi, sinkron hasil→penilaian.

## 0. RINGKASAN EKSEKUTIF

Kelas `hyd` = 2 klaim tugas TERPISAH (per R1 §2.5), dinilai terpisah:

1. **Klaim (i) — deteksi kondisi** (status `|z|>2` residu SPPA vs median/MAD per bin
   qcut(TFLO,10)): engine terbaik = **persistence** (bukan RF — ΔB negatif 7/7 fold,
   direplikasi eksak). Kemampuan: **pemantauan tren status hidrolik + konfirmasi kondisi
   saat kejadian** (P 0,615–0,793; deteksi ≤10 mnt pada 32–65% onset; pos_frac 0,88 saat
   episode loss nyata vs base 0,119). Belum: peringatan-dini (0/1 episode nyata terdeteksi
   sebelum onset) dan alarm otomatis (FAR 39–111/24jam-neg >> target ≤1).
2. **Klaim (ii) — prediksi kegagalan independen** (kick/loss proxy dari z-score ΔV_pit,
   F-9 A, fitur non-pit/non-SPPA/non-TFLO/non-SPM): sinyal prediktor ADA dan konsisten
   arah di 3 varian label (lift titik 8–151), **terutama dengan fitur aliran
   (mass-balance)**: AUPRC_test 0,228 (CI95 [0,009; 0,629]), T_lead median 7 menit.
   Belum: alarm otomatis & generalisasi lintas-sumur — onset test hanya 3 (UNDERPOWERED),
   FAR monitoring 25,9/24jam, 1 wellbore saja, tanpa validasi kejadian-nyata.

## 1. JENIS TUGAS + ENGINE (dicatat, bukan dinilai biner)

| Klaim | Jenis tugas | Jenis engine | Label (sumber fisik) | Fitur |
|---|---|---|---|---|
| (i) hyd-status | **Deteksi kondisi** (bukan prediksi kegagalan mendatang) | Statistical (median/MAD per bin qcut TFLO) sbg pembentuk-label; **persistence** = engine deteksi terbaik terukur; RF = kandidat ML (terbukti TIDAK menambah) | SPPA/TFLO (kanal sumber-label) | 40 fitur mekanis (TQA/RPM/SWOB/HKLD/ROP/BPOS/depth/dbtm ×5); SPPA/TFLO/SPM DILARANG (asersi anti-sirkular lolos) |
| (ii) kick/loss-independen | **Prediksi kejadian mendatang** (onset, H=10 mnt) | Hybrid: ML (RF) + fitur aliran (Q_in) — rule z-pit = baseline "sistem hari-ini" (deteksi DI onset, T_lead=0) | ΔV_pit z-score/sumur (kanal pit — DILARANG jadi fitur) | Gas%+ECD+choke+HKLD+RPM+WOB+ROP+BPOS+shocks+depth (konservatif); +Flow Pumps+Mud Flow In (varian sensitivitas) |

## 2. LAPISAN A — APAKAH DETEKSI BEKERJA (semua angka = eksekusi run ini)

### 2.1 Klaim (i): LOWO 7 fold, replikasi eksak V6-E1b + metrik operasi BARU

Replikasi: AUPRC_rf & persistence COCOK EKSAK dengan `E1b_LOWO_RESULTS.json` (mis. F-14
0,1165/0,4441) → cross-check replikasi lolos. Baseline relevan = **persistence** (V6 §4.1:
persistence = status-quo).

| Fold uji | n_test (pos) | prev | AUPRC_RF (CI95) | AUPRC_pers (CI95) | lift_RF | lift_pers | **ΔB = RF−pers** |
|---|---|---|---|---|---|---|---|
| F-14 | 10.401 (865) | 0,083 | 0,117 [0,058;0,200] | 0,444 [0,284;0,580] | 1,40 | 5,34 | **−0,328** |
| F-15A | 6.156 (698) | 0,113 | 0,113 [0,067;0,167] | 0,490 [0,269;0,677] | 1,00 | 4,32 | **−0,377** |
| F-15_S | 8.355 (993) | 0,119 | 0,121 [0,083;0,168] | 0,425 [0,279;0,553] | 1,02 | 3,57 | **−0,304** |
| F-5 | 6.332 (621) | 0,098 | 0,199 [0,072;0,398] | 0,599 [0,383;0,757] | 2,03 | 6,10 | **−0,400** |
| F-7 | 2.482 (421) | 0,170 | 0,136 [0,081;0,207] | 0,506 [0,321;0,648] | 0,80 | 2,98 | **−0,370** |
| F-9 | 1.616 (423) | 0,262 | 0,615 [0,283;0,829] | 0,625 [0,394;0,799] | 2,35 | 2,39 | **−0,010** |
| F-9_A | 2.206 (331) | 0,150 | 0,161 [0,088;0,249] | 0,542 [0,266;0,715] | 1,07 | 3,61 | **−0,381** |

**ΔB < 0 di 7/7 fold** (kemampuan negatif terukur): fitur non-kanal TIDAK menambah nilai
untuk status hidrolik di atas persistence. CI95 persistence vs RF **tidak tumpang tindih
di 6/7 fold** (F-9 satu-satunya tumpang tindih) → keunggulan persistence statistik kuat.

### 2.2 Metrik operasi klaim (i) (V6 tidak mencetak ini — BARU dari run ini)

Ambang operasi RF dipilih di TRAIN (pra-deklarasi skrip): tier alarm = FAR_train ≤ 1/24jam-neg;
tier monitoring ≤ 6/24jam-neg. P = precision, R = recall, FAR_t = FP per 24 jam operasi-negatif
(jam_neg = jendela eligible negatif/60, grid 60 dtk).

| Engine | P | R | FAR_t (per 24jam-neg) | Waktu deteksi |
|---|---|---|---|---|
| RF tier-alarma (test) | 0,00–0,50 | 0,00–0,35 | **26,6–304,9** (target ≤1 TIDAK transfer) | onset terdeteksi ≤10 mnt: 0–37,5% |
| RF tier-monitoring (test) | 0,09–0,41 | 0,32–1,00 | 407–1.244 | B1: 50–100%, delay median 0 |
| **persistence (biner)** | **0,615–0,793** | **0,617–0,764** | **38,8–110,7** | B1 (≤10 mnt): **31,6–65,4%**; delay median **0–3 mnt**; IQR [0;10] |

Interpretasi A:
- **Ambang RF dari train GAGAL transfer antar-sumur** (FAR test meledak 26×–300× target) —
  RF bahkan tidak layak sbg alarm terkalibrasi lintas-wellbore pada kelas ini.
- Persistence: P ~0,6–0,8 dengan **nol-look-ahead** (deteksi = echo status; delay 0–3 mnt =
  mendeteksi DI/SETELAH onset, bukan sebelum). FAR_t 39–111/24jam-jauh di atas ambang alarm
  (§4 R1) dan monitoring (≤6) pada skala jendela; pada skala BLOK (alarm unik per transisi
  0→1) beban = **0,16–4,7 onset/hari span-campaign** (lihat §4) — inilah beban pemeriksaan
  nyata bagi operator.
- A-positif menurut R1 §1.2 (ΔB>0 mayoritas): **TIDAK terpenuhi** — tercatat sebagai kemampuan
  "persistence = engine deteksi-status terbaik; ML tidak menambah" (R1 §2.5 ekspektasi
  terkonfirmasi dengan angka run ini).

### 2.3 Klaim (ii): F-9 A time.csv — 124 episode proxy, split temporal 70/30

Label pra-reg: z-score r10(ΔV_pit 10-mnt), median+MAD per well, |z|>2 sustain ≥5 mnt,
syarat sirkulasi (Flow Pumps ≥500 L/min), merge <30 mnt → **124 episode (39 gain-proxy,
85 loss-proxy)**; prev (evaluable) 4,15%. **Test period (2009-07-10 23:35 → 07-16)
hanya berisi 3 onset (30 jendela positif, prev_test 0,37%) → onset-level UNDERPOWERED
(<30) — dilaporkan, tidak disembunyikan.**

| Engine (test) | AUPRC (CI95) | prev_test | lift | P (tier) | R (tier) | FAR_t/24jam |
|---|---|---|---|---|---|---|
| konservatif (tanpa fitur aliran) | 0,0301 | 0,0037 | 8,1 | 0,00 (alarm) / 0,021 (monit) | 0,00 / 0,33 | 0,36 / 82,5 |
| **+ flow-in (varian fisika)** | **0,2279 [0,009;0,629]** | 0,0037 | **61,6** | **0,298 (alarm)** / 0,127 (monit) | 0,467 / 0,700 | **5,9** / 25,9 |

Baseline relevan: prevalence-random (AUPRC = prev_test 0,0037) — **kedua varian lift > 1
pada titik**; aturan z-pit (sistem hari-ini) = detector label → T_lead = 0 by construction.
Sensitivitas EKSPLORATIF label (ditandai eksploratif, bukan pra-reg): z>3 sustain-10 =
89 episode, AUPRC_test 0,209 [0,084;0,701]; |ΔV|≥0,5 m³ sustain-10 = 37 episode, AUPRC_test
0,372 [0,029;0,900] — **arah sinyal konsisten di ketiga varian label**, ketidakpastian lebar.

**Hasil tes pembeda R1 §3.2:** lift >> 1 (titik) dengan lower-CI masih > prev → data cenderung
ke arah "prediktor lintas-kanal utk kick/loss-proxy ADA (terutama fitur aliran/mass-balance)",
BUKAN ke "sinyal tidak ada". Tapi kekuatan bukti DIBATASI: 1 wellbore, label proxy, test
onset = 3, CI95 lebar (lower bound AUPRC 0,009 ≈ lift 2,4; upper 0,63).

## 3. LAPISAN B — NILAI MAINTENANCE (waktu peringatan = kunci)

### 3.1 Klaim (i) vs KEJADIAN NYATA (uji eksternal, F-15_S ↔ 24 event kurasi)

24 event kurasi `circulation loss`/`mud loss` NO 15/9-F-15 (2008-11-14 18:15 → 11-16 23:00
UTC) = **1 episode**; jatuh dalam cakupan windows F-15_S (2008-09-24 → 11-28). (Catatan
atribusi: event dilabeli wellbore induk F-15; overlap waktu dengan F-15_S persis —
ketidakpastian induk-vs-sidetrack dicatat.)

| Ukuran | Hasil |
|---|---|
| Peringatan SEBELUM onset (24 jam window) | **0/1 episode** — y_hyd & persistence 0% positif; hanya 173 jendela eligible (7,2 jam dari 24) |
| Selama episode (per hari) | 2008-11-15: **pos_frac 0,884** (n=199); 11-16: 0,054; 11-17: 0,271; base rate keseluruhan 0,119 |
| T_lead vs kejadian nyata | **n/a (tidak ada peringatan)** |

Interpretasi B: detektor hyd-status **mengonfirmasi kondisi saat kejadian nyata nyata
menyala (88% jendela positif di hari-2 episode, ~7,4× base rate), tetapi TIDAK memberi
peringatan-dini** dalam sampel ini. Nilai maintenance = verifikasi/observasi kondisi
(mengurangi "ragu apakah hidrolik bermasalah"), BUKAN waktu-untuk-bertindak. Batas bukti:
n=1 episode; korelasi saat-kejadian bisa pula dipicu perubahan operasi remediasi
(pump-rate changes saat loss handling) — kausalitas TIDAK diklaim.

### 3.2 Klaim (ii): waktu peringatan terhadap onset proxy (test: 3 onset — UNDERPOWERED)

| Engine | B1 (% onset terdeteksi [t_e−10, t_e)) | T_lead median (IQR; rentang) |
|---|---|---|
| konservatif alarm / monitoring | 0% / 33% | — / 10 mnt (1 titik) |
| **+ flow-in alarm** | **66,7% (2/3)** | **7 mnt [5,5;8,5] (4–10)** |
| + flow-in monitoring | 100% (3/3) | 10 mnt [5,5;10] |

Nilai maintenance: indikasi **beberapa menit sebelum** lonjakan pit terukur (kategori B2
"<10 menit" R1 §1.3) — lebih dini dari sistem-hari-ini (z-pit: lead 0), tapi di bawah
anchor respons well-control yang berjam-jam. Pengurangan pemeriksaan tak perlu (B3):
**belum terukur** (butuh data inspeksi/pemeriksaan operasional — tidak ada di Volve).

## 4. LAPISAN C — ROBUSTNESS (C1–C4)

| Ukuran | Klaim (i) | Klaim (ii) |
|---|---|---|
| C1 stabilitas temporal/antar-fold | spread AUPRC_pers 0,425–0,625 (Δ0,20); AUPRC_RF 0,113–0,615 (Δ0,50 — RF TIDAK stabil); CI95 semua fold terlaporkan (§2.1) | CI95 [0,009;0,629] = **sangat lebar** (n_pos_test 30); C1 TIDAK terpenuhi → tingkat "indikasi" saja |
| C2 ketahanan regime (kuartil kedalaman) | regime_drop_RF 0,19–0,72 (RAW AUPRC — tercampur variasi prev kuartil 0,005–0,45; caveat) | belum diukur (1 wellbore, split temporal) |
| C3 toleransi kualitas sensor (ablas keluarga fitur) | drop depth/dbtm: F-5 −58,3%, F-9 −42,8%, F-14 −14,3% relatif (RF bergantung "mengingat kedalaman" di sebagian fold — konsisten SHAP V6); F-15A justru +22,9% (drop membantu); persistence IMUN (tanpa fitur) | fitur aliran = syarat sinyal (konservatif AUPRC 0,03 vs +flow 0,23) → ketergantungan kanal eksplisit |
| C4 transparansi ketidakpastian | CI95 semua fold; 0 fold underpowered (semua ≥30 positif) | 3 onset test = UNDERPOWERED dilaporkan; CI95 dihitung; label sensitivitas ditandai eksploratif |
| Kualitas sensor (bonus) | coverage SPPA/TFLO per well **94,0–98,7%**, median 10 obs/jendela → kualitas baik | pit 345.442 non-null (13 kolom; sentinel −888/-333 dibersihkan); grid 1-mnt 27.322 baris |

Alarm workload (klaim (i), blok unik per hari span — beban pemeriksaan operator):

| Well | onset blok/hari | durasi blok median (p90) |
|---|---|---|
| F-14 | 0,263 | 6,0 mnt (31,6) |
| F-15A | 1,479 | 10,0 (36,8) |
| F-15_S | 0,996 | 9,0 (27,9) |
| F-5 | 0,156 | 3,5 (53,9) |
| F-7 | 1,752 | 8,0 (35,0) |
| F-9 | 1,764 | 8,0 (30,3) |
| F-9_A | 4,707 | 7,5 (31,7) |

Blok positif hyd-status SINGKAT (median 3,5–10 mnt) — konsisten dengan sifat "detektor
proses", bukan kondisi persisten berjam-jam.

## 5. KESIMPULAN — LAYAK UNTUK X, BELUM UNTUK Y

### Klaim (i) — deteksi kondisi hyd (engine: persistence / rule median-MAD)
- **LAYAK: pemantauan tren & indikator status hidrolik dalam-sumur** — P 0,615–0,793,
  delay 0–3 mnt, beban 0,16–4,7 blok/hari, sensor coverage 94–98,7%. Kekuatan bukti:
  **KUAT** (7/7 fold konsisten, CI persistence vs RF tidak tumpang tindih 6/7, replikasi
  eksak V6).
- **LAYAK: konfirmasi kondisi saat kejadian** (pos_frac 0,88 saat episode loss nyata) —
  kekuatan bukti: **LEMAH** (n=1 episode; korelasi, bukan kausalitas).
- **BELUM: peringatan-dini kegagalan** — 0/1 episode nyata terdeteksi sebelum onset
  (terdukat kuat negatif di sampel ini; catatan: jendela eligible pra-onset tipis, 173 window).
- **BELUM: alarm kritis otomatis** — FAR 39–111/24jam-neg (vs syarat ≤1) dan ambang RF
  tidak transfer antar-sumur (test FAR 26–305/24jam pada tier alarm). **Jangan pakai ML
  (RF) di kelas ini** — ΔB negatif 7/7.

### Klaim (ii) — prediksi kick/loss independen (engine: hybrid ML + fitur aliran)
- **LAYAK: indikasi dini bertingkat-menit dengan anotasi ketidakpastian** (T_lead median
  7 mnt, B1 2/3 pada tier alarm varian +flow) — kategori "layak tren/indikasi" R1 §4.
  Kekuatan bukti: **SEDANG-LEMAH** (arah sinyal konsisten di 3 varian label, lift titik
  8–151, lower-CI > prev; TAPI CI95 lebar, test onset 3, 1 wellbore).
- **BELUM: alarm kick/loss otomatis** — FAR 5,9/24jam (tier alarm varian +flow; target ≤1
  belum tercapai), monitoring 25,9/24jam; onset test UNDERPOWERED.
- **BELUM: generalisasi lintas-wellbore** — baru F-9 A (19 hari). Jalur penuh F-1C/F-11
  (GAINLOSSTOT 575/517 file, M2 §1) BELUM diparse → fold tambahan belum terbentuk.
- **BELUM: validasi kejadian-nyata** — 12 event kurasi F-9 A dalam rentang CSV; nihil
  kategori hyd → ground-truth eksternal klaim (ii) di F-9 A tidak tersedia.

### Klasifikasi jenis-tugas (untuk peta PdM)
hyd = **deteksi kondisi** (klaim i, persistence) + **prediksi onset berjangka-menit**
(klaim ii, hybrid); BUKAN diagnosis, BUKAN prediksi kegagalan berjam-hari.

## 6. BUKTI EKSEKUSI (reproducible)

Workspace: `~/.hermes/kanban/boards/capstone-v8-capability/workspaces/t_774cc5e4/`
(salinan durable semua skrip + JSON hasil: `scratch/v8_e_hyd/` di root proyek)
- `claim1_eval.py` + `v8_e_hyd/claim1_results.json` (+ `claim1_run.log`) — LOWO 7 fold + ambang operasi + deteksi + C2/C3 (327 dtk)
- `claim2_eval.py` + `v8_e_hyd/claim2_results.json` (+ `claim2_run.log`) — label pit-z, 2 varian engine
- `claim2b_supplement.py` + `v8_e_hyd/claim2b_supplement.json` — CI95 + sensitivitas label eksploratif
- `layerB_realevent.py` + `v8_e_hyd/layerB_realevent.json`, `layerB_during.py` + `.../layerB_realevent_during.json` — uji kejadian nyata F-15_S
- `layerC_supplement.py` + `v8_e_hyd/layerC_supplement.json` — coverage sensor + beban alarm per well
- Data sumber: `scratch/v6_e1/windows_hyd/*.csv.gz` (7 sumur), `data/witsml/Norway-NA-15_47_9-F-9 A time.csv` (419.747 baris; salinan lokal scratch), `data/volve/labels_curated_v2.csv`

## 7. BELUM DIVERIFIKASI (jujur, sesuai protocol verifikasi)

1. **Atribusi wellbore event loss**: "NO 15/9-F-15" vs F-15_S — overlap waktu persis,
   tapi peta induk↔sidetrack tidak dipastikan dari sumber lain.
2. **Kausalitas pos_frac 0,88 saat episode**: bisa dipicu remediasi operasional (perubahan
   pompa saat loss handling), bukan loss itu sendiri — 1 episode, tanpa kontrol.
3. **Label klaim (ii) = PROXY**: 124 episode kemungkinan campuran kejadian fisika nyata +
   transisi operasi rutin (cluster per jam dalam 1 hari = pola operasi); validasi semantik
   butuh data pit-ops / DDR yang tidak diparse di sini. Sensitivitas 3 varian label
   mengurangi, tidak menghilangkan, keraguan ini.
4. **GAINLOSSTOT F-1C/F-11** (jalur penuh, 575/517 file) belum diparse → klaim (ii) belum
   punya fold lintas-wellbore (prevalence hedge F-9 A sesuai R1 §3.2-2 sudah dijalankan).
5. **B3 (pengurangan pemeriksaan tak perlu)** tidak terukur — tidak ada data pemeriksaan
   operasional di Volve.
6. FAR dihitung dengan asumsi jam-operasi = jendela eligible (V8-R1 §6.4); bila unit stand
   dipakai, skala FAR berubah dengan justifikasi pra-reg.
