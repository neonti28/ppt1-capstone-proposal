# V8-R1 — SPESIFIKASI UJI 3 LAPISAN (A/B/C) PER KELAS + BASELINE RELEVAN PER TUGAS

Task: `t_11f7438f` [R&D] · Board: capstone-v8-capability · Tanggal: 2026-10-11 (WIB)
Status: spesifikasi uji EKSEKUTABEL — mengganti gate biner V6/V7 dengan kerangka
3-lapisan nilai per engine (bukan LULUS/GAGAL seragam).

> **Riset pendahuluan: `scientific-critical-thinking`** — setiap klaim "engine layak X"
> dipisah OBSERVED (angka V6/V7 dari dokumen primer) vs DERIVED (turunan logis) vs
> HIPOTESIS (belum teruji); 4 kelas "gagal" dinilai ulang sebagai FORMULASI tugas yang
> bisa dibalik, bukan bukti ketiadaan sinyal (G2 shk 6/7 lolos = sinyal ADA).
> **Riset pendahuluan: `statistical-analysis`** — metrik per lapisan dipilih sesuai
> sifat data: AUPRC+lift untuk kelas langka (prev <5%), FAR per jam operasi negatif
> (bukan per jendela tunggal), CI95 moving-block bootstrap (blok 60/20/10, 1.000
> resample, seed 42 — metode V6 dipertahankan), <30 positif/fold = UNDERPOWERED.
> **Riset pendahuluan: `experimental-design`** — unit = jendela (grid 60 dtk) / stand
> (opsi S-B2); sumur/alat = cluster; LOWO/LOTO anti-pseudoreplication; fitur lampau /
> label depan; kanal pembentuk label dilarang jadi fitur; onset = peristiwa (waktu),
> bukan status (blok) — jendela dalam blok onset DIBUANG, bukan dinegatifkan.
> **Riset pendahuluan: `hypothesis-generation`** — tiap kelas gagal V6 diperlakukan
> sebagai multi-hipotesis (label salah formulasi / data kurang / sinyal lemah);
> tiap spesifikasi §3 punya TES PEMBEDA yang menyatakan apa yang membuktikan
> hipotesis gugur.
> **Riset pendahuluan: `sequentialthinking`** (5 pikiran, 5/5 sukses) — penataan
> baseline-relevan-per-tugas → definisi A/B/C per kelas → ambang tren vs alarm.

---

## 0. APA YANG BERUBAH (kerangka baru — ambang V6 TIDAK digeser)

Kerangka lama (V6/V7): satu gate biner G1 (lift ≥1,5 mayoritas fold) + G2 (RF ≥
canary-kedalaman) memutuskan LULUS/GAGAL untuk SEMUA kelas. Kerangka baru (instruksi
operator, dokumen ini):

1. **Setiap engine diberi NILAI kemampuan di 3 lapisan** (A deteksi · B nilai
   maintenance · C kepercayaan), bukan satu label gagal/buang.
2. **Baseline bersifat RELEVAN PER TUGAS** — tidak ada baseline universal. Persistence,
   canary-kedalaman, aturan ambang absolut, dan prevalence-random masing-masing punya
   peran berbeda per kelas (tabel §2).
3. **G1/G2 V6 TIDAK DIGESER dan TIDAK DIHAPUS** — dipakai HANYA sebagai label
   "engine TERBUKTI prediksi kuat" (syarat kelas alarm-otomatis §4), bukan syarat
   kelolosan pemakaian.
4. **Jenis tugas dibedakan**: deteksi anomali · deteksi kondisi · diagnosis · prediksi
   kejadian mendatang. Satu kelas bisa punya ≥2 klaim tugas (hyd, stuck, tool_wear)
   yang dinilai TERPISAH.
5. **Keputusan wajar "layak tren BELUM layak alarm otomatis"** = hasil sah, bukan
   kegagalan (§4).

Aturan tetap dari V6/V7 (dibawa ke SEMUA uji di dokumen ini): validitas data ·
pengujian temporal benar (LOWO/LOTO, fitur lampau/label depan) · transparansi
ketidakpastian (CI95 bootstrap) · anti-sirkular (kanal sumber-label dilarang jadi
fitur) · <30 positif/fold = UNDERPOWERED (dilaporkan, tidak dihitung dalam mayoritas).

---

## 1. DEFINISI OPERASIONAL UMUM + RUMUS (evaluator tinggal jalankan)

### 1.1 Notasi per fold uji (sumur/alat tak terlihat = 1 fold)
`TP,FP,TN,FN` dihitung pada ambang operasi engine (ambang yang dipilih di pra-reg,
bukan dioptimasi pasca-hasil). `jam_neg` = jam operasi pada jendela label-negatif.
`N_alaram` = jumlah alarm (transisi negatif→positif prediksi, debounce ditiadakan
untuk onset; untuk status: alarm unik per blok).

### 1.2 LAPISAN A — apakah deteksi bekerja (per kelas, vs BASELINE RELEVAN kelas itu)

| Ukuran | Rumus | Catatan per kelas |
|---|---|---|
| Precision | `P = TP/(TP+FP)` | di ambang operasi; untuk langka (shk, ssi, stuck-onset) laporkan juga `P@k` (top-k skor per fold) |
| Recall | `R = TP/(TP+FN)` | untuk onset: FN = onset tanpa alarm dalam `[t_e−H, t_e)` |
| AUPRC | rata-rata PR-curve (OOF fold) | metrik primer V6 dipertahankan |
| lift | `lift = AUPRC / prev_fold` | prev = prevalensi fold uji; plafon lift = `1/prev` WAJIB dilaporkan (tool_wear prev 0,5 → plafon 2,0) |
| FAR_w | `FP / (N_window_negatip/1000)` | false alarm per 1.000 jendela negatif |
| FAR_t | `FP / jam_neg` | false alarm per jam operasi negatif — ukuran utama utk kelas alarm |
| T_lead | `t_event − t_alarm` (menit) | hanya kelas prediksi-onset/kejadian; laporkan median, IQR, `% onset dengan T_lead>0` |
| Delta-baseline | `ΔB = metrik_engine − metrik_baseline_relevan` | INI penilai A sesungguhnya di kerangka baru: nilai A = seberapa jauh engine mengalahkan baseline tugasnya |

**Aturan penilaian A (bukan ambang universal):** engine dinilai SUDAH BEKERJA pada
lapisan A bila `ΔB > 0` untuk metrik primer kelas itu pada ≥50% fold layak dinilai
(bukan ≥1,5 — itu syarat alarm §4). Bila `ΔB ≤ 0` mayoritas: A = "tidak menambah di
atas baseline" — tetap dicatat sebagai kemampuan (mis. persistence = engine sendiri).

### 1.3 LAPISAN B — apakah deteksi memberi nilai maintenance

| Ukuran | Rumus | Kelas berlaku |
|---|---|---|
| B1 cakupan peringatan-dini | `% onset terdeteksi dalam [t_e−H, t_e)`, H = 10 mnt (sensitivitas 5/30) | stuck-onset, bit_wear-onset, hyd-onset, tool_wear-progresi |
| B2 waktu-untuk-bertindak | `T_lead_median` vs anchor tindakan (stand change/POOH); laporan kategorikal: ≥30 mnt / 10–30 / <10 / nol | kelas onset |
| B3 pengurangan pemeriksaan tak perlu | `kurangi_ragu = 1 − (FP_engine / FP_baseline_rule)` — baseline_rule = aturan ambang absolut yang berlaku saat ini (mis. VIBLAT ≥32,17 ft/s² utk vib) | vib, ssi, shk, hyd-status |
| B4 margin status-awal | median jendela antara alarm dan masuknya blok label-status berkelanjutan (≥k menit) | vib, ssi, shk (tugas deteksi kondisi) |

Anchor preseden (bukan syarat): peringatan 2,67–7,37 menit sebelum stuck terbukti di
Volve dengan data surface [R1-S1 §2.2]. B dinilai POSITIF bila B1 ≥ 50% (onset) atau
B4 median ≥ 1 jendela (status) — bukan angka universal kelayakan alarm (itu §4).

### 1.4 LAPISAN C — cukup tepercaya untuk dipakai

| Ukuran | Rumus | Interpretasi |
|---|---|---|
| C1 stabilitas temporal | `spread_AUPRC = max−min` AUPRC antar fold layak; `CI95` (moving-block bootstrap 60/20/10, 1.000, seed 42) | spread kecil + CI ketat = tepercaya |
| C2 ketahanan lintas-regime | ΔAUPRC per bin regime (kedalaman kuartil; operasi: RPM/WOB regime kuartil) — `regime_drop = max_bin ΔAUPRC_negatif` | canary-kedalaman V6 = kasus khusus C2 lama; sekarang eksplisit per kelas |
| C3 toleransi kualitas sensor | ΔAUPRC saat kanal fitur di-dropout {1 kanal teratas SHAP, 2 kanal} + noise σ/10 | robust bila drop kedua-atas <20% relatif |
| C4 transparansi ketidakpastian | CI95 dilaporkan SEMUA fold; fold UNDERPOWERED diberi label | syarat mutlak — tanpa ini C gagal terlepas dari A/B |

**Aturan penilaian C:** C1–C4 dinilai per kelas; satu kegagalan C4 = engine hanya
LAYAK TREN (§4), berapa pun A/B-nya.

---

## 2. SPESIFIKASI PER KELAS (7 kelas)

### 2.0 Tabel induk

| Kelas | Jenis tugas engine | Engine paling cocok + alasan | Baseline RELEVAN (bukan universal) | Nilai A/B/C kunci |
|---|---|---|---|---|
| `vib` | Deteksi kondisi (status whirl/GET tinggi) | Hybrid: rule ambang absolut (VIBLAT ≥32,17405 ft/s², R1 §4.2) SEBAGAI layer pertama + persistence + ML (RF) utk lead-time | (a) aturan ambang absolut R1 §4.2 (baseline operasional rig); (b) persistence (V6: 0,517–0,796; kalahkan RF 2/4); (c) canary-kedalaman (0,277–0,612) | A: ΔB vs persistence; B4 margin status-awal; C2 per regime |
| `ssi` | Deteksi kondisi (stick-slip torsional) | Hybrid: rule SSI(CRPM)≥1 (definisi kanal) + ML; persistence LEMAH di kelas ini (0/5) → ML = penambah nilai nyata | (a) persistence (kalah 0/5 vs RF — angka per-fold V6 §4.2 tidak dicetak di tabel); (b) canary-kedalaman (0,0055–0,0676); (c) fold UNDERPOWERED (F-7 3 pos, F-9 12 pos) = sampel, bukan baseline | A: lift vs prev (2,61–6,64 sudah terukur); B4; C1 spread CI (2 fold rapuh) |
| `bit_wear` | Prediksi kejadian mendatang (onset-of-high-MSE, S-F1) — BUKAN deteksi status | Supervised ML (RF) pada label onset; persistence dibunuh per konstruksi; fitur geologi join R3 melawan "mengingat kedalaman" | (a) persistence STATUS (0,679–0,984 — dominan 4/4; alasan reframing); (b) canary-kedalaman (0,191–0,756); (c) persistence pada label ONSET (dihitung baru; ekspektasi rendah — tes pembeda) | A: lift onset (G1 V6 3/4 utk status); B1/B2 lead time; C2 kedalaman (SHAP MD/TVD) |
| `stuck` | 2 klaim TERPISAH: (i) deteksi anomali proses (status STUCK_RT); (ii) prediksi kejadian mendatang (onset 0→1, S-A1) | (i) stats/anomaly (label status = blok persisten); (ii) ML onset + horizon H=10 mnt; hybrid dgn rule overpull/torsi (S-A3 LF4) | (i) persistence status 0,787 (F-9_A) + canary 0,410/0,769; (ii) persistence onset (≈lemah by konstruksi) + prevalence-random + anchor Crossformer 2,67–7,37 mnt | A: klaim-ii lift onset; B1 cakupan peringatan; C1 fold 2→4 (F-10/F-12) |
| `hyd` | 2 klaim TERPISAH: (i) deteksi kondisi anomali hidrolik (status \|z\|>2 residu SPPA); (ii) prediksi kegagalan independen (kick/loss/washout, S-C2 fisika pit/flow) | (i) statistical (median/MAD per bin qcut(TFLO,10)) — persistence = baseline jujur; (ii) hybrid: rule fisika well-control (ΔV_pit, Q_out−Q_in) + ML pada fitur non-kanal-sumber | (i) persistence 0,42–0,63 (mengalahkan RF 7/7 → ΔB negatif = hasil A jujur); (ii) prevalence-random + aturan z-score pit (baseline fisika) | A klaim-i: ΔB vs persistence (negatif terukur V6); A klaim-ii: lift pit-label; B1 lead time kick/loss |
| `shk` | Deteksi anomali/dysfunction (bit bounce, SHKRSK_RT ordinal 0–3) | ML (RF) + ordinal (S-B3) — G2 V6 6/7 lolos = fitur BUKAN masalah; akar = positif langka (F-15A 41, F-9 45, F-9_A 30) | (a) canary-kedalaman (V6 G2 lolos 6/7); (b) prevalence-random (prev 0,6–2,4%; plafon lift besar); (c) fold kuat baru F-10 (798 pos, 0,27%) + F-12 (580 pos, 1,59%) = eliminasi "underpowered", bukan baseline | A: FAR yang bisa ditangani (§3.3); B3/B4; C1 stabilitas lift antar 11 fold |
| `tool_wear` | 2 sub-klaim TERPISAH: (i) pemantauan-alat-dikenal (progresi within-tool, S-D1 change-point onset); (ii) generalisasi-lintas-alat (LOTO) | (i) change-point statistics (kurtosis/crest/f_dom per segmen) — cluster efektif naik (banyak onset/alat); (ii) ML VMD-features (S-D2) — tapi plafon lift prev 0,5 = 2,0 | (i) t_cp-validity test (bila t_cp selalu detik awal = artefak termal → klaim gugur); (ii) identity-run majority (prev 0,5) + canary 3-RMS (E1c); lift terukur 1,09–1,42 = kemampuan+batas, bukan label gagal | A(i): onset cluster count + deteksi progresi; A(ii): lift 1,09–1,42 dicatat sbg capability; C3 noise akselerometer |

---

### 2.1 `vib` — deteksi kondisi (VIBLAT_RT ≥32,17405 ft/s²)

- **Jenis tugas:** deteksi kondisi (status keadaan GET tinggi), BUKAN prediksi kegagalan
  mendatang. Engine: HYBRID — rule ambang absolut sebagai layer dasar (sudah dipakai
  operasional), persistence sebagai banding, RF untuk lead-time/peringatan dini.
- **Baseline relevan:** (a) ATURAN AMBANG ABSOLUT R1 §4.2 (kanal sumber = definisi;
  ini baseline "sistem hari-ini"); (b) persistence (AUPRC 0,517–0,796, kalahkan RF di
  2/4 fold — sinyal label membentuk blok); (c) canary-kedalaman (0,277–0,612).
- **Lapisan A (rumus eksekutor):** `P,R` pada ambang operasi; `lift = AUPRC/prev`;
  `ΔB_status = AUPRC_RF − AUPRC_persistence`; `ΔB_rule = kurangi_ragu (B3)`.
  Angka terukur V6 (OBSERVED): F-14 lift 1,61 · F-15A 2,36 · F-15_S 3,50 · F-5 1,63
  (AUPRC 0,912/0,562/0,491/0,441). A-positif jika `ΔB_status > 0` di ≥50% fold —
  V6: ΔB_status negatif di 2 fold (persistence menang) → A = "sebagian" (tercatat,
  bukan gagal).
- **Lapisan B:** B4 margin status-awal = median jendela antara prediksi-RF dan blok
  GET berkelanjutan; B3 = FP rule absolut vs FP engine (rule = baseline operasional).
- **Lapisan C:** C2 per bin kedalaman + regime RPM/WOB (canary-lama = kasus khusus);
  C3 dropout TFLO/HKLD (fitur SHAP teratas vib: TFLO_mean/last, depth, dbtm).

### 2.2 `ssi` — deteksi kondisi (SSI(CRPM_RT) ≥1)

- **Jenis tugas:** deteksi kondisi torsional. Persistence LEMAH (0/5 kalah) → kelas
  ini di mana ML terbukti menambah nilai di atas status-quo.
- **Baseline relevan:** (a) persistence (kalah 0/5 vs RF; angka per-fold tidak dicetak
  di tabel V6 §4.2 — hanya verdict 0/5); (b) canary-kedalaman (0,0055–0,0676);
  (c) rule definisi kanal SSI≥1 (min 10 sampel, Liu 2025).
- **Lapisan A:** angka terukur V6 (OBSERVED): lift 2,61/3,59/6,64/3,74/1,47(F-9_A ✗);
  AUPRC 0,0185–0,1057; persistence 0/5. Fold UNDERPOWERED F-7 (3 pos), F-9 (12 pos)
  dilaporkan terpisah, TIDAK dihitung mayoritas. A-positif = lift>1 mayoritas fold
  layak (sudah 4/5 terukur).
- **Lapisan B:** B4 (alarm sebelum blok SSI berkelanjutan ≥k menit); B3 vs rule.
- **Lapisan C:** C1 spread CI95 2 fold rapuh (F-14 CI [0,0096;0,0797], F-15A
  [0,0043;0,0634] — lebar = ketidakpastian transparan); S-E1 (parse F-10/F-4/F-12/
  F-15: CRPM 281.030/42.010/178.430/57.846 baris) mengganti fold underpowered → C1
  dihitung ulang pada 11 fold.

### 2.3 `bit_wear` — prediksi onset-of-high-MSE (S-F1), bukan status

- **Jenis tugas:** PREDIKSI KEJADIAN MENDATANG (masuknya blok high_MSE Teale).
  Reframing menghapus hukuman persistence per konstruksi (onset tidak persisten).
- **Baseline relevan:** (a) persistence STATUS 0,679–0,984 (mengalahkan RF 4/4 =
  alasan reframing, tercatat sebagai batas kemampuan pendekatan lama); (b)
  canary-kedalaman 0,191–0,756 (SHAP V6 didominasi MD_last/mean + TVD → "mengingat
  posisi"); (c) persistence pada label ONSET (dihitung di kampanye baru — ekspektasi
  rendah; TES PEMBEDA: bila persistence-onset ≥ RF mayoritas → hipotesis "kegagalan =
  formulasi status" DITOLAK).
- **Lapisan A:** label onset = transisi blok ke high_MSE; kandidat 481/329 (A1+PM,
  diverifikasi); jendela dalam blok DIBUANG; jendela positif = [t0−H,t0), H=10 mnt
  (sensitivitas 30). Ukur: lift_onset, P, R, FAR_t. G1 V6 status 3/4 = konteks
  kemampuan fitur (OBSERVED), bukan hasil onset.
- **Lapisan B:** B1 = % onset dengan alarm dalam horizon; B2 = T_lead median vs
  anchor "kerja pemborosan-efisiensi" (onset high-MSE = tanda keausan/balling).
- **Lapisan C:** C2 eksplisit per kedalaman (fitur geologi join picks 409/flags
  SAND 32.988/CARB 33.386 per MD, relasi R3 — melawan memorisasi depth); C1 spread
  antar 4 fold layak (F-14/F-15/F-15S/F-5).

### 2.4 `stuck` — 2 klaim, evaluasi onset mendominasi

- **Klaim (i) deteksi anomali proses** (status STUCK_RT): persistence 0,787 (F-9_A),
  canary 0,410/0,769, prev 66,9% (jendela) — angka V6 (OBSERVED). Nilai A klaim-i
  = ΔB vs persistence; V6 mengukur ΔB negatif di F-9_A → klaim-i "tidak menambah
  di atas status-quo" (kemampuan dicatat).
- **Klaim (ii) prediksi kejadian** (onset 0→1, S-A1): label onset ketat F-9_A = 34
  (PM EKSAK; ffill 74 — definisi onset WAJIB dikunci pra-reg Fase 0); F-14 strict 0
  / ffill 87 / runs 394 (sporadis); F-10 15.300 baris + F-12 3.463 (≥1 = 21) menaikkan
  fold 2→4 setelah parse. Baseline klaim-ii: persistence-onset (lemah by konstruksi),
  prevalence-random, anchor Crossformer 2,67–7,37 mnt [R1].
- **Lapisan A klaim-ii:** `lift_onset = AUPRC_onset/prev_onset`; `P,R@H`; FAR_t;
  UNDERPOWERED bila onset <30/fold (F-14 strict-0 = fold otomatis underpowered untuk
  label onset ketat — dilaporkan, bukan disembunyikan).
- **Lapisan B:** B1 cakupan peringatan-dini onset stuck (kunci nilai maintenance
  kelas ini — "berapa menit sebelum string tersendat"); B2 vs anchor POOH/stand.
- **Lapisan C:** C1 spread 4 fold (F-9_A + F-10 + F-12 + F-14-ffill); C-semantik:
  verifikasi nilai 0/1/2/3 STUCK_RT lintas wellbore (F-10 didominasi nilai 3 —
  risiko sebanding-label, prasyarat pra-reg, blind spot V7 §5).

---

### 2.5 `hyd` — 2 klaim TERPISAH (deteksi kondisi vs prediksi kegagalan independen)

- **Klaim (i) deteksi kondisi** (status anomali `|z|>2` residu SPPA vs median/MAD per
  bin qcut(TFLO,10), R1 §4.2 #7): ini detektor PROSES, persistence = baseline jujur.
  Angka V6 (OBSERVED): persistence 0,42–0,63 MENGALAHKAN RF (0,11–0,61) di 7/7 fold;
  lift 1,40/1,00/1,02/2,03/0,80/2,35/1,07; prev 8,3–26,2%. Nilai A klaim-i =
  **ΔB negatif terukur** → kemampuan: "label status hidrolik TIDAK dapat ditambah
  nilainya oleh fitur non-kanal (RF)" — bukan label GAGAL, ini KEMAMPUAN NEGATIF
  yang terukur (persistence = engine terbaik utk klaim ini).
- **Klaim (ii) prediksi kegagalan independen** (S-C2, label dari SUMBER FISIKA
  berbeda dari fitur): (a) kick/loss = z-score per well terhadap ΔV_pit /
  GAINLOSSTOT (median+MAD per sumur); (b) washout/clog = |Q_out−Q_in| menyimpang
  terus-menerus + tren SPPA turun pada flow tetap. Data: jalur cepat F-9 A time.csv
  — 12 kolom pit + Tank volume active + Flow Pumps + Mud Flow In, 345.442 non-null,
  NOL parse (M2 §1); jalur penuh F-1C/F-11: GAINLOSSTOT 575/517 file, PITTOT
  565/506, FLOWOUTPC 949/731. Baseline klaim-ii: aturan z-score pit (fisika, sistem
  hari-ini) + prevalence-random.
- **Lapisan A klaim-ii:** `lift_pit = AUPRC_engine/prev_kickloss`; `P,R`; FAR_t;
  anti-sirkular: SPPA/TFLO/SPM + kolom pit DILARANG dari fitur (label-source
  channels).
- **Lapisan B klaim-ii:** B1 = % kick/loss onset dengan alarm dalam [t_e−H,t_e);
  B2 = T_lead vs anchor respons well-control (menit kritis — ini kelas di mana B
  paling mahal nilainya).
- **Lapisan C:** C2 per sumur (7 fold V6 + F-9 A baru); C-semantik fase EDM/pit
  baseline operasi (pit operational gains vs kick = keputusan pra-reg).

### 2.6 `shk` — deteksi anomali; ukur FAR yang BISA DITANGANI

- **Jenis tugas:** deteksi anomali/dysfunction (SHKRSK_RT ≥1; ordinal 0–3 = opsi
  S-B3). G2 V6 6/7 lolos (OBSERVED) = fitur BUKAN masalah; akar kegagalan lama =
  positif langka (30–45 jendela/fold kecil) → lift tidak mayoritas (3/7).
- **Baseline relevan:** (a) canary-kedalaman (lolos 6/7 — sinyal ada); (b)
  prevalence-random (prev 0,6–2,4%; plafon lift besar); (c) fold F-10 (798 positif,
  prev 0,27%) + F-12 (580, 1,59%) = eliminasi underpowered; F-4 (50) & F-15 (13)
  terlalu kecil → fold UNDERPOWERED, dilaporkan.
- **Lapisan A — FAR YANG BISA DITANGANI (inti §3.3):** ukur `FAR_t = FP/jam_neg`
  pada ambang operasi. Dua ambang pemakaian (bukan ambang gate):
  (1) **FAR_alarm ≤ 1 per 24 jam operasi negatif** → layak alarm-otomatis (§4);
  (2) **FAR_t ≤ 6 per 24 jam** (≈1 check driller per 4 jam) → layak pemantauan
  /tren dengan anotasi beban-kerja; di atas itu = kemampuan dicatat + batas
  penggunaan "screening saja". Lift & AUPRC tetap dilaporkan (V6: 0,94–9,79;
  G2 6/7) sebagai lapisan-A konteks.
- **Lapisan B:** B3 = pengurangan pemeriksaan vs status-quo (baseline: MWD shock
  risk display); B4 = margin sebelum blok shock berkelanjutan.
- **Lapisan C:** C1 spread lift antar ~9–11 fold (varians lift V6 0,94–9,79 =
  perhatian utama); C-semantik skala 0–3 (F-10: 651/123/24; F-12: 196/226/158 —
  semantik lintas-wellbore wajib diverifikasi, prasyarat).

### 2.7 `tool_wear` — pemantauan-alat-dikenal vs generalisasi-lintas-alat

- **Sub-klaim (i) pemantauan-alat-dikenal** (within-tool, S-D1): label = progresi
  keausan (change-point onset `t_cp` pada deret kurtosis/crest/f_dom per segmen
  1–2 dtk dari 8 xlsx, 471.400 sampel, 1000 Hz, 8 run × 50–62 dtk). Baseline: t_cp
  VALIDITY TEST — bila `t_cp` selalu di detik awal semua run = artefak termal →
  sub-klaim GUGUR (tes pembeda eksplisit R1 §5.2). Cluster efektif naik: dari
  2 status × 4 alat menjadi banyak onset/alat → statistik layak.
  Ukur A(i): jumlah onset valid per run; `recall onset` dalam horizon; FAR per
  menit run (unit kecil → laporkan per-menit, bukan per-jam operasi).
- **Sub-klaim (ii) generalisasi-lintas-alat** (LOTO): angka V6 terukur (OBSERVED):
  lift 1,09/1,39/1,42/1,30; AUPRC 0,54–0,77 vs prev ~0,5 (plafon lift 2,0);
  G2 4/4 (canary 3-RMS kalah) → fitur spektral (SHAP T03: Z_kurt, X_fdom, X_crest,
  Z_fdom) MENAMBAH di atas amplitudo. Baseline: identity-run majority + 3-RMS.
  Nilai A(ii) = **kemampuan terbatas**: AUPRC > baseline RMS di 4/4 (G2) tapi
  plafon lift membatasi; dicatat sebagai "sinyal keausan terukur lintas-alat,
  kekuatan sedang" — BUKAN gagal.
- **Lapisan B:** B1(i) = % onset progresi terdeteksi sebelum t_cp (target: beberapa
  detik–menit; anchor RUL/degradation); B2 tidak berlaku (durasi run 50–62 dtk —
  batas jujur domain bengkel, bukan sumur).
- **Lapisan C:** C3 noise/dropout kanal X/Y/Z; C2 antar-alat (spread AUPRC LOTO);
  C-domain: transfer ke drilling = TIDAK DIKLAIM (domain bengkel ≠ sumur, V6 §6.5).

---

## 3. SPESIFIKASI UJI MEMBALIK PENILAIAN — 4 KELAS "GAGAL" V6

Prinsip: kegagalan V6 = kegagalan FORMULASI/UNIT/INFORMASI, bukan bukti ketiadaan
sinyal (G2 shk 6/7 = sinyal ADA). Setiap spesifikasi di bawah MENGGANTI pertanyaan
yang dijawab data, bukan menurunkan ambang.

### 3.1 `stuck` → uji onset + durasi abnormal (bukan status)

1. Definisi label (pra-reg dikunci Fase 0 V7): onset = edge `STUCK_RT 0→1` pada grid
   60 dtk; varian dikunci SEBELUM training: strict (PM: F-9_A 34, F-14 0) vs ffill
   (74 / 87) — PILIH SATU, jangan keduanya pasca-hasil.
2. Jendela positif `[t0−H, t0)`, H=10 (sensitivitas 5/30); jendela DALAM blok
   Dibuang (bukan negatif).
3. Ukur: `lift_onset`, `P@H`, `recall@H` (% onset dengan alarm di horizon), `FAR_t`,
   `T_lead` median/IQR; persistence-onset = baseline (ekspektasi rendah — tes
   pembeda: bila persistence-onset ≥ RF mayoritas → hipotesis reframing DITOLAK,
   penyebab pindah ke "sinyal fitur lemah untuk stuck-onset").
4. Durasi-abnormal (ukuran B tambahan): `durasi_blok_prediksi(onset) vs durasi blok
   normal` — median blok pasca-onset harus ≥2× median durasi "onset semu" pada
   jendela negatif, agar onset = peristiwa bermakna, bukan noise biner.
5. Fold: F-9_A + F-14(-ffill) + F-10 + F-12 (parse 24 file STUCK_RT, 15.300+3.463
   baris); <30 onset/fold = UNDERPOWERED (F-14 strict masuk kategori ini — jujur).
6. Validasi naratif: 582/884 event labels_curated dalam rentang CSV (M2) → sampel
   onset instrumen dicek silang ±30 mnt dengan event kurasi (`bha_stuck_fishing`
   38 event) = positive-control kejadian nyata.

### 3.2 `hyd` → pisahkan 2 klaim (deteksi kondisi vs prediksi kegagalan independen)

1. Klaim-i (deteksi kondisi, status |z|>2): evaluasi A = **ΔB vs persistence**;
   V6 sudah mengukur ΔB<0 di 7/7 → hasil A tercatat: "RF tidak menambah di atas
   persistence utk status hidrolik" — kemampuan persistence DIPAKAI sebagai engine
   deteksi-status (bukan dibuang). B(i): B3 pengurangan pemeriksaan vs aturan-|z|
   manual.
2. Klaim-ii (prediksi kegagalan = kick/loss/washout independen, S-C2): label dari
   kanal fisika pit/flow (SUMBER BERBEDA dari fitur; kanal pit/SPPA/TFLO/SPM
   dilarang jadi fitur). Uji cepat F-9 A (345.442 baris, nol parse) dulu =
   hedge-prevalensi sebelum parse besar F-1C/F-11.
3. Ukur klaim-ii: `lift_pit`, `recall@H` kick/loss onset, `T_lead` (menit sebelum
   lonjakan pit/defisit flow — anchor operasi well-control), FAR_t.
4. TES PEMBEDA: klaim-ii lift mayoritas → kelas hidrolik PUNYA prediktor lintas-
   kanal utk kegagalan; klaim-ii lift ~1 → "sinyal precursor hyd tidak ada dari
   kanal non-label" berstatus TERDUKUAT KUAT (hasil ilmiah, dicatat).

### 3.3 `shk` → ukur FAR yang BISA DITANGANI (bukan hanya lift)

1. Hitung `FAR_t` + `FAR_w` pada ambang operasi tiap fold; laporkan sebaran antar
   fold (V6 lift 0,94–9,79 = indikasi ketidakstabilan yang persis diukur ini).
2. Klasifikasi pemakaian (§2.6): FAR ≤1/24 jam-negatif = alarm-otomatis layak;
   FAR ≤6/24 jam = tren/pemantauan layak (anotasi beban kerja wajib); >6/24 jam =
   screening-saja. Lift G1 tetap dilaporkan tapi TIDAK menjadi satu-satunya gerbang.
3. Fold kuat baru F-10 (798 pos) + F-12 (580 pos) menyerang akar "positif langka";
   F-4 (50) / F-15 (13) = UNDERPOWERED, dilaporkan terpisah.
4. S-B3 ordinal (0–3): latih regresi/ordinal, turunkan keputusan pada ambang ≥1
   yang SAMA — gate/biner tidak digeser; FAR dihitung pada keputusan biner hasil.

### 3.4 `tool_wear` → pisah pemantauan-alat-dikenal vs generalisasi-lintas-alat

1. Sub-klaim (i) within-tool (S-D1): onset progresi per run (change-point);
   VALIDASI t_cp: bila t_cp ∈ detik awal di >50% run = artefak termal → sub-klaim
   GUGUR (hasil jujur). Jika valid: ukur recall-onset + FAR/menit + jumlah cluster
   onset (statistik layak naik dari n=4 alat).
2. Sub-klaim (ii) LOTO: pertahankan angka V6 (lift 1,09–1,42; AUPRC 0,54–0,77;
   G2 4/4) sebagai KEMAMPUAN + BATAS: "sinyal spektral keausan terukur lintas-alat
   dengan kekuatan sedang, terbatas plafon lift prev 0,5" — bukan label gagal.
3. Batas domain dinyatakan: 4 alat bengkel, run berurutan (R02 selalu sesudah R01 =
   confound termal), run 50–62 dtk — transfer ke drilling TIDAK diklaim tanpa data
   baru (D2: tidak ada dataset tool-wear drilling nyata tambahan).
4. S-D2 (VMD features) = pengangkat AUPRC per fold; S-D4 (ranking) = cadangan dgn
   estimand baru → pra-reg baru.

---

## 4. AMBANG "LAYAK TREN" vs "LAYAK ALARM OTOMATIS" (tingkat keyakinan berbeda)

| Syarat | LAYAK TREN (pemantauan/indikasi) | LAYAK ALARM OTOMATIS (kritikal) |
|---|---|---|
| Lapisan A | `ΔB > 0` vs baseline relevan di ≥50% fold layak (lift >1 boleh minoritas) | **G1 V6: lift RF ≥1,5 mayoritas fold layak** + **G2: AUPRC RF ≥ canary mayoritas** (= label TERBUKTI-KUAT; gate lama tidak digeser) |
| Lapisan B | B-arah benar: B1 ≥ 50% onset terdeteksi dalam H (kelas onset) ATAU B4 median ≥ 1 jendela (kelas status) | B1 ≥ 80% onset terdeteksi dalam H + T_lead_median ≥ anchor tindakan kelasnya (mis. ≥1 stand / waktu POOH) |
| Lapisan C | C4 wajib (CI95 + label UNDERPOWERED dilaporkan); C1 spread boleh lebar (dianotasi) | C1: tidak ada fold layak dengan lift < 1; C2: tidak ada bin regime dengan ΔAUPRC negatif > 20% relatif; C3: drop-out 1 kanal teratas < 20% penurunan relatif |
| FAR | DILAPORKAN + batas layak: FAR ≤ 6 per 24 jam-negatif (kelas shk-like; kelas run pendek tool_wear: per-menit) | FAR ≤ 1 per 24 jam operasi negatif (setara per-menit utk run 50–62 dtk) |
| Output | Kemampuan + batas pemakaian: "layak tren/pemantauan, BELUM alarm otomatis" | "Layak alarm kritis otomatis" |
| Bila tidak tercapai | Bukan GAGAL — keputusan wajar (instruksi operator §5) | Tidak tercapai → engine tetap dinilai di tingkat tren; TIDAK diturunkan ambangnya |

Catatan: G1/G2 lama TIDAK digeser dan TIDAK dihapus — dipindahkan dari "gerbang
kelolosan tunggal" menjadi **syarat ambang atas** (label "TERBUKTI prediksi kuat").
Kelas yang G1-nya gagal (shk 3/7, tool_wear 0/4, hyd 2/7, stuck 1/2) TIDAK dibuang:
punya jalur nilai di tingkat tren + spesifikasi uji balik §3.

---

## 5. PERNYATAAN GATE + ANTI-PENGGESERAN

- G1 (lift ≥1,5 mayoritas fold layak dinilai), G2 (AUPRC RF ≥ canary-kedalaman
  mayoritas), <30 positif = UNDERPOWERED, LOWO/LOTO, fitur lampau/label depan, kanal
  pembentuk-label dilarang jadi fitur, persistence > RF = layak bersyarat (V6):
  **TIDAK DIGESER, TIDAK DIHAPUS** — dipakai sebagai syarat ambang-atas §4.
- Kerangka baru MENAMBAH ukuran (ΔB, FAR_t, T_lead, B1–B4, C1–C4) — tidak ada ambang
  V6 yang dilunakkan. Setiap kampanye baru (onset stuck/bit_wear, shk wellbore baru,
  hyd S-C2) tetap butuh pra-registrasi baru di-hash sebelum training
  (PROTOCOL_RISET_TIM.md).
- Semua angka baseline di dokumen ini dikutip dari dokumen primer V6/V7 (daftar di
  bawah) — tanpa angka karangan; dokumen ini spesifikasi uji, bukan hasil run.

## 6. BATASAN JUJUR + BELUM DIREKONSILIASI

1. Prev stuck F-9_A: 66,9% (jendela V6) vs 49,4% (baris mentah) — BELUM
   direkonsiliasi (M2 §8#1) → semua metrik prev-stuck dikunci pra-reg Fase 0.
2. Definisi onset stuck: strict-34 vs ffill-74 — pilihan menentukan fold UNDERPOWERED
   atau tidak; WAJIB dikunci pra-reg, bukan dipilih pasca-hasil.
3. Semantik skala 0/1/2/3 STUCK_RT/SHKRSK_RT lintas wellbore belum terdokumentasi
   (F-10 didominasi nilai 3) — prasyarat label onset shk/stuck lintas wellbore.
4. FAR per 24 jam mengasumsikan skala operasi Volve (jam operasi dari grid waktu
   CSV); bila unit stand dipakai (S-B2) FAR dihitung per stand dan ambang §4
   diskalakan ulang dengan justifikasi pra-reg.
5. `hyd` klaim-ii & `tool_wear` klaim-i = jalur dengan tes pembeda eksplisit —
   keduanya TIDAK dijanjikan lolos; target minimum 5 kelas tidak bergantung padanya
   (V7 PM §0).
6. Anchor B2 (waktu-untuk-bertindak) bersifat kategorikal + preseden ilmiah —
   bukan SLA operasional rig (butuh validasi driller, di luar data Volve).
7. Dokumen ini adalah SPESIFIKASI; semua ambang di dalamnya (B1 50%/80%, FAR 1/6
   per 24 jam, C2 20%) adalah desain pra-reg — boleh disesuaikan SEKALI di paket
   pra-reg awal (di-hash sebelum run pertama), tidak boleh berubah setelah hasil
   diketahui (anti shopping-for-significance, V6 §6.8).

## Sources (sumber angka — dokumen primer proyek)

- `docs/V6_E1_ML_DESIGN.md` §2 (7 kelas + populasi sampel), §4.1–§4.4 (angka LOWO
  per kelas: AUPRC/lift/canary/persistence), §5 (SHAP per kelas), §6 (kelemahan
  jujur), §3 (pra-reg + anti-sirkular).
- `docs/V7_PM_VERDICT.md` §0 (jalur per kelas; onset bit_wear 481/329; shk F-10
  798 + F-12 580), §3 (onset stuck strict-34/ffill-74 EKSAK; prev), §7 (fase
  eksekusi + stop/go).
- `docs/V7_R1_SOLUTIONS.md` §1.2 (peta kanal wellbore baru), §2–§6 (solusi S-A1…
  S-F2 + preseden: Crossformer 2,67–7,37 mnt, AE Volve AUC 0,958), §8 (pernyataan
  gate).
- `docs/V7_M2_SYNTHESIS.md` §1 (status data per solusi + angka baris non-null),
  §2 (relasi R1–R12), §3 (jalur olah per solusi), §6 (kontradiksi/koreksi angka),
  §8 (belum diverifikasi).
- `docs/V6_D1a..h_DATA_CHECK.md` (peta data per domain — keberadaan kanal baseline).
