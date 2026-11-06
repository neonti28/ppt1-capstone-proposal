# V10-EVAL — BAB 7: APA YANG DIDETEKSI TIAP ENGINE · SEBERAPA BEKERJA · TIER PEMAKAIAN

Task: `t_de420dbc` [KONSULTASI V10 · Evaluator] · Papan: `capstone-v10-proposal` · Tanggal: 2026-10-14 (WIB)
Peran: **Penerus Evaluator Lapisan A/B/C V9** (kartu induk `t_e43490bf` EVAL_C; ringkasan A `t_8a7a33d4`,
B `t_019ce414`; dokumen hasil `docs/V9_EVAL_{A,B,C}_LAYER*.md`; tabel tier `docs/V9_PM2_VERDICT.md` §e).
Sumbu bab: `docs/V10_PM1_OUTLINE.md` §1 (kosakata angka 7/11/27 mengikat) + §2 Bab 7.

Status: **HASIL EVALUASI** — kemampuan + batas pemakaian + kekuatan bukti per klaim.
**BUKAN vonis LULUS/GAGAL.** Tiap klaim ditutup dengan "memenuhi untuk X / belum untuk Y / belum terukur
untuk Z" + angka. Bab ini menutup keluhan operator **(a)** apa yang dideteksi tiap engine, **(b)** engine
mana yang bekerja & bagaimana, dan **(f)** arti tegas 7 vs 11 vs 27, pada **level hasil**.

> **Sumber angka (nol angka karangan).** Semua angka ditarik dari JSON primer milik tim lalu **dihitung
> ulang independen di sesi ini** (`scratch/v10_eval_bab/t_de420dbc_verify.py`,
> `t_de420dbc_extract.py`; lihat §5): `scratch/v9_eval_c/v9_eval_c_RESULTS.json`,
> `scratch/v9_i1/v9_i1_RESULTS.json`, `scratch/v9_e_{ml,stat,rule}/*.json`. Dokumen acuan:
> `docs/V9_EVAL_A_LAYERA.md`, `docs/V9_EVAL_B_LAYERB.md`, `docs/V9_EVAL_C_LAYERC.md`,
> `docs/V8_M1_CAPABILITY_MAP.md`, `docs/V9_PM2_VERDICT.md` §e.

## Baris riset pendahuluan

- Riset pendahuluan: `scientific-critical-thinking` — hipotesis terpusat: bab hasil harus menjawab
  "apa yang dideteksi + seberapa andal + seberapa tepercaya", bukan "model mana lolos gate".
  Hipotesis alternatif ("satu tabel ranking tunggal cukup") diuji lalu ditolak karena mencampur **tugas**
  (deteksi-kondisi vs prediksi-onset vs klasifikasi-lintas-alat) dan **skala** (menit rig vs detik bengkel);
  OBSERVED (angka JSON) dipisah dari DERIVED (sintesis tier) dan BELUM-TERUKUR.
- Riset pendahuluan: `verification-mandatory` — SEMUA angka kunci di tabel §1 ditarik ulang dari JSON primer
  dengan skrip sendiri (§5), bukan disalin dari dokumen tim; "belum terukur" tetap dipisahkan dari "gagal" (§4);
  selisih pembulatan (mis. "119×" vs 119,57×) dilaporkan apa adanya.
- Riset pendahuluan: `statistical-analysis` — angka dilaporkan sebagai **rentang antar-fold**, bukan satu titik;
  CI95 yang **memuat prevalensi** dibaca sebagai "sinyal tidak terbukti"; FAR dilaporkan pada **skala aslinya**
  (per 24 jam-rig vs per menit-bengkel) dan dilarang diseragamkan; AUPRC/lift dilarang dirata-ratakan antar kelas
  (plafon lift beda per prevalensi) — perbandingan wajib memakai **ΔB pada fold yang sama**; fold UNDERPOWERED
  (<30 positif) dilabeli, tidak dihitung mayoritas.
- Riset pendahuluan: `multi-engine-detection-evaluation` — tiap engine dinilai pada 3 lapisan
  (A: deteksi bekerja · B: nilai pemeliharaan · C: layak dipercaya) dengan **baseline yang relevan per tugas**,
  lalu diberi **tier pemakaian**; vonis ditaruh di tingkat **alat**, bukan "N model lolos gate".
- Riset pendahuluan: `sequentialthinking` (5 pikiran, 5/5 sukses, `sequ-mcp`): (1) inventaris 7 engine/11 klaim/
  27 head dari registry → (2) desain kolom tabel (apa-dideteksi → jenis tugas → metode → angka → tier → batas) →
  (3) bahaya penyajian yang dilarang (rata-rata antar-kelas, FAR diseragamkan, CI-dibaca-bukti) → (4) definisi
  arti tier bagi pengguna rig + aturan perakitan → (5) gerbang verifikasi angka sebelum dokumen ditulis.

---

## 0. KERANGKA: (a) 7 ENGINE · (b) CARA KERJA · (f) 7 vs 11 vs 27

### 0.1 (a) Tujuh engine = tujuh jenis kegagalan/disfungsi berbeda fisika

Alat PdM advisory ini **bukan satu model untuk semua masalah**. Ia menyusun **7 engine**, masing-masing
menargetkan satu kelas kegagalan BHA/bengkel dengan fisika, label, dan tindakan pemeliharaan berbeda.
Nama engine = kunci REGISTRY `code/v9_i1_pipeline.py` (daftar eksak V10_PM1_OUTLINE §1.1).

| # | Engine | Yang dideteksi (fisik-operasional) | Kanal/label sumber | Jml klaim |
|---|--------|-------------------------------------|--------------------|-----------|
| 1 | `vib` | Getaran lateral berlebih (whirl/GET) — kondisi `VIBLAT_RT ≥ 32,17405 ft/s²` | kanal instrumen MWD | 1 |
| 2 | `ssi` | Stick-slip torsional — bit tersendat-sendat memutar, `SSI(CRPM_RT) ≥ 1` | turunan kanal `CRPM_RT` | 1 |
| 3 | `shk` | Bit bounce / shock risk sedang berlangsung — `SHKRSK_RT ≥ 1` | kanal instrumen MWD | 1 |
| 4 | `stuck` | Pipa terjepit (stuck pipe) — blok `STUCK_RT` (K-i status) & onsetnya (K-ii, H=10 mnt) | kanal instrumen + kurasi DDR | 2 |
| 5 | `hyd` | Anomali hidraulik / kick-loss proxy — residu SPPA `\|z\|>2` (K-i) & onset ΔV_pit (K-ii) | residu z-score SPPA / 13 kolom pit | 2 |
| 6 | `bit_wear` | Keausan/balling mata bor — blok `high_MSE` (Teale) (K-1) & onsetnya (K-2) | kolom label USROP (Teale) | 2 |
| 7 | `tool_wear` | Keausan mata bor domain bengkel — perubahan-regime dalam-run (K-i) & status lintas-alat (K-ii) | identitas run (desain dataset) | 2 |

### 0.2 (b) Bagaimana engine bekerja — lima keluarga metode, dirangkai hibrida per tugas

Setiap engine adalah **hibrida per tugas**, bukan satu metode seragam. Metode dipilih sesuai **jenis tugas**;
ML hanya dipakai bila memberi **nilai tambah terukur** (ΔB>0). Di kelas di mana ML merugikan, ML **dilarang**
(contoh nyata: RF di `hyd K-i` dilarang, ΔB RF−persistence negatif 7/7 — keputusan D-A5).

| Keluarga metode | Cara kerja | Dipakai untuk |
|---|---|---|
| **Rule** (ambang/aturan) | `status(t)=1[kanal(t) ≥ ambang]` atau aturan mayoritas 2-dari-3 z-kanal; meniru "sistem hari-ini" | lapisan dasar vib/ssi/shk/stuck |
| **Persistence** | `ŷ(t)=y(t−1)` — prediksi naif dari 1 grid (60 dtk) sebelumnya | konfirmasi status + baseline pembanding jujur |
| **Statistik robust** | `z = 0,6745·(x−median)/MAD`; median/MAD tahan outlier (NIST/Rousseeuw) | label & deteksi hyd K-i; change-point tool_wear |
| **Change-point** | `SSE(τ)` 1-split + permutation test 500× (p=0,002) → deteksi perubahan regime | tool_wear K-i (bengkel) |
| **ML terawasi** | RF/GB/LR kontrak seragam (seed 42, fitur statistik jendela 10 mnt, imputer fold-safe, tanpa grid search) | penambah ranking/onset vib/ssi/shk/stuck-K-ii |
| **Hibrida** | gabungan: rule ∧ persistence (konfirmasi 2-langkah), atau rule dasar + ML ranking | mesin per kelas (arsitektur D-A3) |

### 0.3 (f) Mengapa 7 · 11 · 27 — tiga tingkat pengelompokan objek yang SAMA

Tiga angka itu **bukan tiga populasi terpisah** (7+11+27=45 = salah kategori), melainkan tiga **level**
berjenjang (**7 ⊂ 11 ⊂ 27**):

| Tingkat | Jumlah | Satuannya | Alasan |
|---|---|---|---|
| **7 engine** | 7 | **kelas kegagalan** (fisis) | 7 fisika berbeda → label, tindakan, bukti berbeda; satu model gabungan = mencampur estimand (D-A2) |
| **11 klaim** | 11 | **estimand / tugas terpisah** | 4 engine mengerjakan **dua tugas berbeda** dan dipisah: `stuck` (K-i status + K-ii onset), `hyd` (K-i status + K-ii prediksi), `bit_wear` (K-1 status + K-2 onset), `tool_wear` (K-i regime + K-ii lintas-alat). **3×1 + 4×2 = 11**; tiap klaim punya tugas, label, baseline sendiri (EA-1/EB-1/EC-1) |
| **27 head** | 27 | **varian metode terukur** | satu klaim dijalankan **beberapa cara** (rule/persistence/hybrid/statistik/ML) yang diukur terpisah. Registry I1 mencatat **27 head**: vib 4 + ssi 4 + shk 4 + stuck 6 + hyd 4 + bit_wear 2 + tool_wear 3 = 27 |

**Kenapa penting:** "**7**" menjawab *apa saja yang dideteksi*; "**11**" menjawab *berapa klaim yang harus
dibuktikan* (dasar tabel §1 & tier); "**27**" menjawab *bagaimana alat diperakitan* (dasar §3 & jumlah baris
registry). Menyamakan ketiganya = kesalahan framing (tugas berbeda dituntut metrik sama).

---

## 1. TABEL BESAR 11 KLAIM — APA DIDETEKSI · TUGAS · METODE · ANGKA KUNCI · TIER · BATAS

Legenda: FAR **rig** = alarm palsu **per 24 jam operasi negatif** (grid 60 dtk); FAR **bengkel** = **per menit**
(jendela 1 dtk). "ΔB" = selisih vs baseline pada fold yang sama. CI = CI95 AUPRC; "memuat prev" = sinyal
tidak terbukti. UP = fold underpowered (<30 positif). Angka = **rentang antar-fold** (bukan satu titik).
Tier = keputusan pemakaian (lihat §2). Tiap angka dilacak ke JSON primer & dihitung ulang di §5.

| # | Engine / klaim | APA YANG DIDETEKSI (bahasa manusia rig) | Jenis tugas | Metode (cara kerja) | Angka kunci | Tier | Batas pemakaian |
|---|---|---|---|---|---|---|---|
| 1 | **vib** | Getaran lateral BHA melebihi ambang operasional (whirl/GET tinggi) | deteksi **kondisi** (TLead tidak berlaku) | rule ambang + persistence + RF | rule **P 0,868–0,952** (1,10×) · R 0,276–0,595 · **FAR 9,99–49,94** · FP 197; RF **AUPRC 0,441–0,912** (2,07×) · CI memuat prev **0/4** · ΔB vs canary **4/4** · τ0,5 FAR **4,15–496,09 = 119,57×** | **TREN** (RF) + **PERINGATAN-BERPENGAWAS** (rule) | jangan ambang global (FAR menyebar 119× antar-well); FAR rule 10–50/24 jam; tanpa klaim lead-time; kalibrasi per-well dulu (D-A4) |
| 2 | **ssi** | Stick-slip torsional (putaran drillstring tersendat-lepas) | deteksi **kondisi** | rule definisi SSI + persistence + RF + hybrid | RF **AUPRC 0,015–0,459** (30,36×) · CI memuat prev **3/7 layak** (5/9 all) · ΔB vs prevalensi **7/7**; rule **R 0,000–0,032** · FAR 0,0–7,33 (≤6: 4/9); hybrid **FP 26→7 (−73,1 %)** · ≤rule **7/7** | **TREN** (RF) + **PERINGATAN hemat** (hybrid) | belum detektor andal per well (spread 30×); nodata kanal CRPM **22.385/35.906 = 62,34 %** = keterbatasan sensor; 2 fold UP |
| 3 | **shk** | Bit bounce / shock risk sedang berlangsung (disfungsi getaran aksial-torsional) | deteksi **anomali** berlangsung | rule display + persistence + RF | rule **FAR 0,670–6,618** (9,87×) → **≤6 di 7/9 well** · P 0,00–0,935 · FP 121; RF **AUPRC 0,0069–0,1929** (28,07×) · CI memuat prev **7/9** · B3 **−212,5×** | **PERINGATAN-BERPENGAWAS** (rule) + **TREN** (RF) | RF jangan sbg alarm (CI 7/9 no-skill); kalibrasi lintas-well dilarang; RF menambah beban inspeksi |
| 4 | **stuck K-i** | Pipa terjepit (blok status `STUCK_RT` persisten) — konfirmasi, bukan ramalan | deteksi **kondisi** | rule display + persistence + hybrid | rule **P 0,9238–0,9662** (1,05×) · R 0,449–0,599 · FAR 8,32–61,0 (≤6 **0/2**) · FP 49; hanya **2 fold** (F-14, F-9_A) | **PERINGATAN-BERPENGAWAS** (cakupan terbatas) | FAR >6; portabilitas ke well lain **belum terukur** (cakupan 2/9 well); replikasi F-9/F-10/F-15 diperlukan |
| 5 | **stuck K-ii** | Akan masuk kondisi terjepit dalam **≤10 menit** (onset 0→1) | prediksi **kejadian** | persistence-EVENT + rule E1 (2-dari-3) + E2 z-stat + RF | persistence-EVENT **B1 0–0,115** · **TLead 4,5–8,5 mnt** (med 7,0; 1,89×) · FAR 0–2,93 · FP 11; RF τ0,5 B1 0–0,045 · TLead 2–159; E2 CI memuat prev **4/4**; anchor absorbed **13/281 = 4,63 %** | **TREN / triage** | B1 jauh dari syarat alarm (80 %); titik B1≥50 % berbiaya **77×** beban; semantik label lintas-well = risiko pra-reg Fase 0 |
| 6 | **hyd K-i** | Anomali hidraulik (tekanan standpipe menyimpang dari pola normal) — konfirmasi status | deteksi **kondisi** | median/MAD pembentuk label + persistence + hybrid | hybrid **P 0,724–0,948** (1,31×) · R 0,52–0,87 · **FAR 14,62–58,43** (4,0×) · **FP 2091→927 (−55,7 %) 9/9**; persistence **CI memuat prev 0/9** (satu-satunya kelas); delay **0–3,5 mnt** | **PERINGATAN-BERPENGAWAS** (kandidat terkuat) | FAR >6 di 9/9 → belum alarm; label = residu SPPA (**proxy**, anotasi wajib); naik tier bila kalibrasi per-well terukur |
| 7 | **hyd K-ii** | Akan terjadi kick/loss (masuk-keluarnya fluida) dalam ≤10 menit | prediksi **kegagalan** | RF + fitur aliran; baseline Fisher/Pearson literal + rule z-pit | fisher varian **AUPRC 0,022** CI [0,0025;0,0684] **memuat prev 0,0037** · q95 **P=R=0** (FP 177, FAR 31,56) · **sign-flip 78,66 %** (6.377/8.107 jendela) | **BELUM LAYAK PAKAI** (eksplorasi) | 1 split temporal (dispersi antar-periode tak terukur); **FlowOut absen** (kendala sensor terukur); RF V8 (B1 66,7 %) = referensi, belum diulang di V9 |
| 8 | **bit_wear K-1** | Zona inefisiensi MSE (keausan/balling mata bor) — status blok `high_MSE` | deteksi **kondisi** | persistence (engine utama) + RF screening + canary | **AUPRC 0,119–0,984** (8,3×) · 5/7 fold scorable · **ΔB vs canary 5/5** · lift 1,81–10,67 | **TREN** | **P/R/FAR belum terukur** (field TP/FP tidak ada di JSON); dataset **USROP ≠ rig Volve** (transfer lintas-dataset); 2 fold 0 positif |
| 9 | **bit_wear K-2** | Akan masuk zona inefisiensi MSE (onset blok `high_MSE`) | prediksi **onset** | RF-onset + persistence-onset (dirancang) | **nol angka** — pra-reg K-2 belum terbit; kampanye belum dijalankan | **BELUM (belum dijalankan)** | dilarang dipakai di tingkat apa pun sampai kampanye berangka; bukan "gagal" |
| 10 | **tool_wear K-i** | Perubahan regime getaran alat (bengkel) — awal keausan, skala **detik** | deteksi **perubahan-regime** | change-point SSE + permutation 500× + kalibrasi within-tool | cp signifikan **8/8 run** (p≤0,05 & ≤0,002) · **precision run 0,50**; FAR-terkalibrasi **deteksi 4/4** · **FP 1–3/alat** · **TLead 20–36 dtk** (1,8×) · tes artefak termal **0/8** | **PERINGATAN-BERPENGAWAS** (bengkel) | precision 0,50 → bukan "keausan spesifik"; **domain bengkel** (transfer ke rig TIDAK diklaim, D-A7); n run=8 underpowered |
| 11 | **tool_wear K-ii** | Status keausan mata bor **lintas-alat** (alat belum pernah dilihat) — LOTO | klasifikasi **lintas-alat** | RF LOTO + ambang inner-LOO; baseline canary 3-RMS + identity-majority | canary **AUPRC 0,516–0,612** (1,19×) · identity = prev (plafon lift **2,0**); **RF V9 belum dijalankan**; RF V8 (ref) ΔB vs canary **4/4**, precision biner 0,50–0,56 | **TREN** | RF V9 belum jalan (kekuatan bukti = referensi V8); precision ≈ peluang → jangan alarm; persistence N/A dinyatakan (label konstan dalam run) |

### 1.1 Temuan pusat (evaluasi, bukan vonis)

**TIDAK ada klaim yang memenuhi syarat ALARM-OTOMATIS penuh.** Dua engine paling tepercaya —
**hyd K-i hybrid** (CI persistence 0/9 memuat no-skill; FP-cut −55,7 % konsisten 9/9; delay ≤3,5 mnt) dan
**tool_wear K-i FAR-terkalibrasi** (deteksi 4/4 alat; TLead 1,8× terkecil; FP 1–3) — layak
**PERINGATAN-BERPENGAWAS sekarang** dan merupakan **kandidat naik-tier** bila ambang dikalibrasi
per-well/alat secara prospektif. Kegagalan paling umum = **portabilitas ambang global antar-well**
(vib FAR 119×; shk RF CI 7/9) — **kegagalan portabilitas, bukan kegagalan deteksi.**

### 1.2 Nilai pemeliharaan terukur (Lapisan B: apakah alat mengurangi kerja inspeksi?)

B3 = pengurangan pemeriksaan vs rule status-quo (B3 ≥ 0 = tidak menambah beban). Bukti bahwa peringatan
"sebanyak mungkin" justru merugikan, sehingga nilai ada di titik **ber-B3≥0**:

| Kelas | Engine@titik | FP | **B3** | Cakupan/margin (B4) | Bacaan |
|---|---|---|---|---|---|
| vib | rule / hybrid | 197 | 0,00 | 26,4 % / 5,0 mnt | peringatan dini terbatas tanpa biaya tambahan |
| vib | RF (semua τ) | 2.050–15.321 | −9,4…−76,8 | 0–8,8 % / 2,5–7 | menambah beban TANPA cakupan naik |
| ssi | hybrid | 7 | **+0,73** | 0 % / — | hemat pemeriksaan, peringatan dini nol |
| shk | rule / hybrid | 121 | 0,00 | 13,4 % / 4,5 mnt | lapisan dasar berbiaya status-quo |
| stuck K-i | hybrid E1∧pers | 41 | **+0,16** | 11,8 % / 5,0 mnt | penghematan kecil di titik E1 |
| hyd K-i | hybrid | 927 | **+0,56** | 13,0 % / 4,5 mnt | **hemat 56 % + deteksi P/R ≥0,52** |
| tool_wear K-i | FAR-terkalibrasi | 1–3 | **+0,91…+0,98** | deteksi 4/4 / lead 20–36 dtk | **satu-satunya klaim B1≥50 % + B3≥0 bersamaan** |

Titik ber-cakupan-tinggi (ssi RF τ0,05 B3 **−487,8**; shk RF τ0,05 **−212,5**; stuck K-ii RF τ0,05 **−77,1**)
selalu berbiaya inspeksi jauh lebih besar dari status-quo → tidak dipakai sebagai peringatan.

---

## 2. ARTI SETIAP TIER BAGI PENGGUNA RIG

Tier adalah **keputusan pemakaian**, bukan nilai rapor. Bagi insinyur pengeboran/teknisi rig:

| Tier | Arti bagi pengguna rig | Yang boleh dilakukan | Yang DILARANG | Contoh klaim |
|---|---|---|---|---|
| **ALARM-OTOMATIS** | Boleh memicu tindakan **tanpa** konfirmasi manusia (syarat: FAR≤1/24 jam + B1≥80 % + C2/C3 terukur) | — | — | **0 klaim** (tidak ada yang memenuhi) |
| **PERINGATAN-BERPENGAWAS** | "Perhatikan ini, konfirmasi dulu sebelum bertindak." Bernilai, tetapi **wajib human-in-loop**; badge FAR + label keyakinan + batas tertulis selalu ditampilkan | menaikkan prioritas pemeriksaan; menandai well/alat untuk ditinjau; memicu konfirmasi 2-langkah | memicu stop/penarikan otomatis tanpa tinjauan insinyur | vib rule, ssi hybrid (hemat), shk rule, stuck K-i, hyd K-i hybrid, tool_wear op_far_calibrated |
| **TREN** | "Untuk melihat arah/kecenderungan, bukan dasar keputusan." Skor/ranking di dasbor; tidak ada notifikasi | memantau tren kondisi & skor; membandingkan antar-sumur; ranking triage | memunculkan alarm; memakai ambang global; jadi dasar inspeksi otomatis | vib/ssi/shk RF, stuck K-ii, bit_wear K-1, tool_wear calib_5of27 & K-ii |
| **BELUM LAYAK PAKAI** | "Jangan dipakai dulu — datanya belum cukup." Status eksplisit, bukan angka 0 yang menyamar | eksplorasi riset; menunggu kampanye penguatan | dipakai di tingkat apa pun | hyd K-ii (data pit/FlowOut belum ada), bit_wear K-2 (pra-reg belum terbit) |

**Aturan tier yang ditegakkan otomatis** (I1 `decision_layer()`, diverifikasi 13/13 di PM2 re-run):
(1) `tier != "ALARM-OTOMATIS"` untuk SEMUA head; (2) head bertier TREN/BELUM **tidak boleh** jatuh ke lapisan
peringatan; (3) semua peringatan wajib `human_review_required = true`; (4) slot alarm otomatis = **0**.

**Naik tier bukan janji — syaratnya terukur** (EVAL_C §4): hyd K-i naik bila ambang dikalibrasi per-well →
FAR≤6 di ≥7/9 well dengan P/R ≥0,5; tool_wear K-i naik bila precision run ≥0,8.

**Pesan jujur ke pengguna:** "0 alarm otomatis" **bukan** kegagalan alat — ini desain advisory. Alarm dini
tanpa FAR terukur justru **menambah** beban pemeriksaan (bukti terukur: RF shk B3 −212×, RF vib −9…−77×).
Karena itu alat memberi **peringatan berpengawas + dasbor tren**, dan keputusan akhir tetap pada manusia.

---

## 3. PROTOTIPE I1: BAGAIMANA 27 HEAD DIRAKIT JADI SATU ALAT

Registry `scratch/v9_i1/v9_i1_RESULTS.json` (diverifikasi ulang sesi ini: **27 head** = L0 5 · L1 11 · L2 9 ·
L3 2; tier **TREN 13 · PERINGATAN-BERPENGAWAS 12 · BELUM LAYAK PAKAI 2**; slot alarm otomatis **0**;
`keputusan_akhir = MANUSIA`). Perakitan mengikuti pipeline 5 lapis: data → fitur → engine → lapisan
keputusan → antarmuka manusia.

### 3.1 Peta 27 head → lapisan keputusan

| Lapisan | Jumlah | Isi (head) | Tier | Perilaku |
|---|---|---|---|---|
| **L0 — status otomatis** | **5** | persistence vib · persistence ssi · persistence shk · persistence stuck-K-i · persistence hyd-K-i | TREN (baseline konfirmasi) | menampilkan status sistem-hari-ini **tanpa notifikasi** (nol training, nol ML) |
| **L1 — peringatan human-in-loop** | **11** | vib rule + hybrid · ssi rule + hybrid · shk rule + hybrid · stuck K-i rule + hybrid · hyd K-i rule + persistence + hybrid · tool_wear op_far_calibrated | PERINGATAN-BERPENGAWAS | mengusulkan tindakan; **semua** `human_review_required = true`; badge FAR + keyakinan + batas tampil |
| **L2 — tren/skor** | **9** | vib rf · ssi rf · shk rf · stuck e1_2of3 + persistence_event + rf (K-ii) · bit_wear persistence (K-1) · tool_wear calib_5of27 + canary_3rms | TREN | skor/ranking di dasbor; **tidak ada** head TREN yang boleh berbunyi |
| **L3 — keputusan manusia** | **2** | hyd K-ii (`k2_tidak_tersedia`) · bit_wear K-2 (`k2_onset_belum`) | BELUM LAYAK PAKAI | status eksplisit "BELUM DIJALANKAN/BELUM TERSEDIA" (bukan nol diam, tanpa metrik palsu) |
| **ALARM OTOMATIS** | **0** | — | — | **di-assert** di kode & verifikasi |

### 3.2 Aturan perakitan dari sisi evaluasi (mengapa begini, bukan sebaliknya)

1. **Satu head = satu tugas + satu bukti.** Tier head ditetapkan EVAL_C; I1 **dilarang menaikkan tier**
   (cek V2: 27 head, **0 kenaikan tier**). Ini menjaga agar "cepat terlihat berguna" tidak mengalahkan
   "jujur soal bukti".
2. **Head dipisah bila badannya beda.** `tool_wear` dipecah jadi `calib_5of27` (L2 gating, terlalu sensitif:
   memicu 71–98 % jendela pada alat baru) dan `op_far_calibrated` (L1, FP 1–3) — satu badge untuk keduanya
   akan menyesatkan (I1 §5.2).
3. **Kelas status memakai konfirmasi; kelas onset memakai triage.** Kelas status (vib/ssi/shk/stuck-K-i/
   hyd-K-i/bit_wear-K-1) dinilai lewat **B4 margin status-awal**, bukan TLead; kelas onset (stuck-K-ii/
   hyd-K-ii/bit_wear-K-2) dinilai lewat **B1/TLead** vs anchor kelasnya sendiri — dilarang meminjam metrik
   antar tugas.
4. **Skala tidak dicampur.** Lead rig dalam **menit** (grid 60 dtk); lead tool_wear dalam **detik** (bengkel,
   jendela 1 dtk) — D-A7: tidak boleh dijumlahkan atau dibandingkan langsung.
5. **Integrasi = impor, bukan salinan.** Modul rule/persistence diimpor dari kampanye E_RULE; bukti integrasi
   terkuat: replay segmen F-14 menghasilkan **angka identik** dengan fold kampanye (10/10 cocok; mis. vib rule
   P 0,9444 / FP 30 / FAR 49,94 di keduanya) — artinya yang dirakit memang engine kampanye yang sama.
6. **Determinisme sebagai fondasi kepercayaan.** Re-run identik (V7); AUPRC ML direproduksi (V8);
   E_STAT 4/4 file identik kecuali `elapsed_s`; E_ML selisih 2,2e-16 (machine epsilon) = numerik identik.

### 3.3 Yang dilihat manusia per head (antarmuka L4)

Tiap head mencetak: `tier` · `layer` · `n_aktif/n` · metrik segmen (P/R/FP/FAR **+ satuan**) · AUPRC (head ML) ·
**badge FAR kampanye** (angka lintas-fold, terpisah dari FAR segmen) · **label keyakinan** ·
**batas pemakaian tertulis** · `human_review_required`. Ketiadaan data selalu ditulis dengan **kata**
("BELUM TERSEDIA"/"BELUM DIJALANKAN"/"nodata n"), bukan angka 0 yang menyamar sebagai hasil.

---

## 4. BELUM TERUKUR / BELUM DIVERIFIKASI (dipisah tegas dari "gagal")

- **Belum terukur (bukan gagal):** P/R/FAR bit_wear K-1; K-2 bit_wear; RF hyd-K-ii, RF bit_wear,
  RF tool_wear-K-ii versi V9 (angka V8 = referensi terpisah, EA-7); portabilitas ambang stuck-K-i
  (>2 well); ketahanan hyd-K-ii antar-periode (1 split); kalibrasi per-well prospektif (D-A4).
- **Keterbatasan bukti:** fold kecil (stuck-K-i 2, tool_wear 4 alat/8 run, hyd-K-ii 1 split, 3 onset);
  prevalensi antar-well sangat berbeda (vib 0,14–0,57; ssi 0,003–0,065) → AUPRC antar-fold tidak
  sebanding langsung, wajib dibandingkan ke baseline pada fold yang sama (ΔB).
- **Tripwire terbuka (pra-reg Fase 0):** semantik skala 0/1/2/3 STUCK_RT/SHKRSK_RT lintas-well;
  rekonsiliasi prevalensi stuck 66,9 % vs 49,4 %; sinkronisasi zona-waktu kontrol-positif.

---

## 5. VERIFIKASI (angka dihitung ulang dari JSON primer di sesi ini)

Skrip verifikasi sesi ini: `scratch/v10_eval_bab/t_de420dbc_verify.py` + `t_de420dbc_extract.py`
(mem-parse langsung `scratch/v9_eval_c/v9_eval_c_RESULTS.json` + `scratch/v9_i1/v9_i1_RESULTS.json` —
**tanpa** memakai skrip tim). Hasil:

| # | Angka yang diuji | Sumber primer | Hasil |
|---|---|---|---|
| V1 | vib RF τ0,5 FAR 4,14897–496,09249 (rasio **119,57×**); n_well FAR≤6 = 1/4 | EVAL_C `C_ml.vib.rf.far_by_tau.0.5.FAR_disp` | ✓ cocok |
| V2 | vib rule P 0,8676–0,9519 (1,10×), FAR 9,988–49,942, FP 197 | EVAL_C `C_rule_status.vib` | ✓ cocok |
| V3 | ssi RF AUPRC 0,01512–0,45887 (30,36×), CI memuat prev 3/7, ΔB vs prevalensi 7/7 | EVAL_C `C_ml.ssi.rf` | ✓ cocok |
| V4 | ssi hybrid FP 26→7 (−73,1 %), ≤rule 7/7; nodata CRPM 22.385/35.906 = 62,34 % | EVAL_C `C_rule_status.ssi` | ✓ cocok |
| V5 | shk rule FAR 0,6705–6,6175 (9,87×), FP 121; RF CI memuat prev 7/9 | EVAL_C `C_rule_status.shk` + `C_ml.shk` | ✓ cocok |
| V6 | stuck K-i rule P 0,9238–0,9662 (1,05×), FAR 8,321–61,001, FP 49, 2 fold | EVAL_C `C_rule_status.stuck_k1` | ✓ cocok |
| V7 | stuck K-ii persistence-EVENT B1 0–0,1154, TLead 4,5–8,5 (med 7,0; 1,89×), FP 11; anchor 13/281 = 4,63 % | EVAL_C `C_onset.stuck_k2` | ✓ cocok |
| V8 | hyd K-i hybrid P 0,7236–0,9484, FAR 14,62–58,43 (4,0×), FP 2091→927 (−55,7 %) 9/9; persistence CI memuat prev 0/9 | EVAL_C `C_rule_status.hyd_ki` + `C_stat.hyd_ki_persistence` | ✓ cocok |
| V9 | hyd K-ii fisher CI [0,0025;0,0684] memuat prev 0,003701; sign-flip 6.377/8.107 = 78,66 %; q95 TP 0/FP 177 | EVAL_C `C_stat.hyd_kii_fisher_variant` | ✓ cocok |
| V10 | bit_wear K-1 AUPRC 0,1185–0,9837 (8,3×), 5/7 scorable, ΔB canary 5/5; P/R/FAR = BELUM TERUKUR | EVAL_C `C_bitwear.K1` | ✓ cocok |
| V11 | tool_wear K-i cp 8/8 signifikan, precision run 0,50, FP 1–3, TLead 20–36 dtk (1,8×), artefak 0/8 | EVAL_C `C_toolwear.K_i` | ✓ cocok |
| V12 | tool_wear K-ii canary 0,5164–0,6124 (1,19×), plafon lift 2,0, RF V9 belum jalan | EVAL_C `C_toolwear.K_ii` | ✓ cocok |
| V13 | registry: **27 head** (L0 5 · L1 11 · L2 9 · L3 2), tier 13 TREN / 12 PERINGATAN / 2 BELUM, slot alarm **0**, keputusan **MANUSIA** | I1 `v9_i1_RESULTS.json` | ✓ cocok |

**Selisih/catatan yang dilaporkan apa adanya:** (1) EVAL_C menulis "119×" sedangkan hitung ulang = 119,57×
(beda pembulatan; kesimpulan "tidak portabel" tidak berubah); (2) CI ssi "5/9 all-fold" vs "3/7 fold-layak"
= denominator berbeda, keduanya benar bila dinyatakan; (3) E_ML `rerun_identical=False` dengan selisih
2,2e-16 → ditandai "numerik identik", bukan "identik bit".

---

## 6. RINGKASAN JAWABAN UNTUK BAB PROPOSAL

- **(a) 7 engine + apa yang dideteksi:** vib (getaran lateral), ssi (stick-slip), shk (bit bounce),
  stuck (pipe stuck, status+onset), hyd (anomali hidraulik, status+prediksi), bit_wear (keausan/balling
  MSE, status+onset), tool_wear (keausan bengkel, regime+lintas-alat) — §0.1, tabel §1.
- **(b) cara kerja & engine mana yang bekerja:** 5 keluarga metode (rule · persistence · statistik robust ·
  change-point · ML terawasi) dirangkai **hibrida per tugas**; ML hanya bila ΔB>0 (§0.2). Yang bekerja paling
  andal: **hyd K-i hybrid** dan **tool_wear K-i FAR-terkalibrasi** (kandidat PERINGATAN terkuat) — §1.1.
- **(c) mengapa metode itu dipilih:** tiap kelas = tugas berbeda → metode disesuaikan; RF **dilarang** di
  hyd K-i (ΔB− 7/7) sebagai bukti konsistensi (R1 §2, PM1 D-A5).
- **(d) peran data:** label dari kanal instrumen/turunan/kurasi/identitas-run; kanal pembentuk label
  **dilarang** jadi fitur (anti-sirkular); grid 60 dtk rig, 1 dtk bengkel; anti-bocor waktu (fitur t0−1).
- **(e) labeling/rumus/hybrid:** detail ada di kartu ML/Stat/Rule (`V10_E_ML_BAB.md`, `V10_E_STAT_BAB.md`,
  `V10_E_RULE_BAB.md`); evaluator memakai hasilnya sebagai angka §1.
- **(f) 7 vs 11 vs 27:** 7 kelas kegagalan → 11 klaim (4 kelas berbagi dua tugas) → 27 head (varian metode
  yang dirakit) — §0.3.
- **Tier & artinya:** ALARM-OTOMATIS (0 klaim) / PERINGATAN-BERPENGAWAS (12 head) / TREN (13 head) /
  BELUM LAYAK PAKAI (2 head); arti bagi pengguna rig di §2; perakitan alat (L0 5 · L1 11 · L2 9 · L3 2,
  0 alarm, keputusan MANUSIA) di §3.

---

Sumber primer: `scratch/v9_eval_c/v9_eval_c_RESULTS.json`, `scratch/v9_i1/v9_i1_RESULTS.json`,
`scratch/v9_e_{ml,stat,rule}/*.json`. Dokumen acuan: `docs/V9_EVAL_{A,B,C}_LAYER*.md`,
`docs/V9_I1_INTEGRATION.md`, `docs/V9_PM2_VERDICT.md` (§e), `docs/V9_R1_JUSTIFICATION.md`,
`docs/V9_PM1_ARCHITECTURE.md`, `docs/V8_M1_CAPABILITY_MAP.md`, `docs/V10_PM1_OUTLINE.md`.
Dihitung & diverifikasi: 2026-10-14 (WIB) — V10-EVAL Bab 7 (`t_de420dbc`).
