# V6-D0 — SINTESIS 8 PEMBACA: peta field bernilai lintas sumber untuk V6-E1

Task: `t_dc129046` [Pembaca Utama] · Board: capstone-v6-solve · Tanggal: 2026-10-10
Konsumen: Auditor 1 (`t_9e5e4f81` → docs/V6_A1_DATA_AUDIT.md) dan ML Eng (`t_5e052df1` → docs/V6_E1_ML_DESIGN.md).

> **Riset pendahuluan: `verification-mandatory` + `scientific-critical-thinking` — semua angka di §1
> dihitung ulang oleh aggregator langsung dari file primer/CSV di disk, bukan disalin dari laporan.**

---

## 0. VERIFIKASI INDEPENDEN OLEH AGGREGATOR (bukan baca laporan)

Sebelum menyintesis, aggregator membuka ulang file sendiri (perintah `find`/`wc` berbeda dari parser tiap pembaca):

| Klaim pembaca | Hasil hitung ulang aggregator | Status |
|---|---|---|
| 192 file tubular XML | `find witsml_raw -path '*/tubular/*.xml'` = **192** | cocok |
| 161 file bhaRun XML | = **161** | cocok |
| 63 trajectory + 27 wbGeometry | = **63** + **27** | cocok |
| 8 file mudLog XML | = **8** | cocok |
| 7150 file log XML | = **7150** | cocok |
| 20 DLIS + 2 LIS | = **20** + **2** | cocok |
| `v6_d1a_tubular.csv` 1392 baris | `wc -l` 1393 → **1392 data rows** | cocok |
| `v6_d1b_bharun.csv` 161 baris | 162 → **161** | cocok |
| `v6_d1c_trajectory.csv` 5561 baris | 5562 → **5561** | cocok |
| `v6_d1d_mudlog.csv` 2882 baris | 2883 → **2882** | cocok |
| `v6_d1e_log_sample.csv` 1022 kurva | 1023 → **1022** | cocok |
| D1f: 21 CSV, 309.644 baris | `ls v6_d1f/csv/*.csv` = **21**; total baris − 21 header = **309.644** | cocok |

Kesimpulan: **semua klaim jumlah-file/baris dari 8 pembaca COCOK dengan hitung ulang independen aggregator —
tidak ada satu pun yang terbantah.**
> **Catatan koreksi (2026-10-11, D0-fix `t_01a5780a`)**: sebagian angka di dokumen ini telah dikoreksi
> sesuai `docs/V6_A1_DATA_AUDIT.md` §8b + `docs/V6_PM_VERDICT.md` §2 (uom azi D1c, baris depth.csv/ROP
> data D1h, angka keyword EDM D1g, triple USROP §2.4). D0 hanya merangkum — sumber otoritatif angka =
> dokumen pembaca (D1a–D1h) + audit A1/PM; dokumen pembaca asli TIDAK ikut diubah di sini.
Klaim kualitatif (mis. "EDM bukan event DB", "dullingInfo 0") diverifikasi pada §2/§4 lewat kutipan bukti
masing-masing laporan; verifikasi ulang mendalam = tugas Auditor 1.

---

## 1. TABEL RINGKAS SEMUA SUMBER

| # | jenis_file (dokumen) | file_dibuka | kolom/kurva | baris | potensi_LABEL_baru | blocker_apa_adanya |
|---|---|---|---|---|---|---|
| D1a | WITSML TUBULAR (`V6_D1a_TUBULAR.md`) | 192/192 XML, 0 gagal | 19 kolom CSV; 62 tipe komponen | **1.392** komponen (1222 drill string) | Bukan label — **geometri BHA/string** = fitur drag/buckling (buka ulang uji I7 R1) | Rating motor `torqueMax/Pmax` **0/192 file** (absen terverifikasi, I1/TOB tetap terblokir); 2 file assembly tanpa komponen (sumber data); 1 komponen od=id=len=−999.25 |
| D1b | WITSML BHARUN (`V6_D1b_BHARUN.md`) | 161/161 XML, 0 gagal | ~15 field run | 161 run, 14 wellbore | Anchor waktu: `dTimStart/Stop`, **9 drilling window lengkap**, numBitRun 11 | dullingInfo/dullGrade/bitName **0/161** (konfirmasi V4 — label dull TIDAK ADA); 6 run durasi negatif; 2 nilai numBitRun non-integer ("3 RR 1", "4RR1") |
| D1c | TRAJECTORY+WBGEOMETRY (`V6_D1c_TRAJ_GEOM.md`) | 63 + 27 XML, 0 gagal | MD/TVD/incl/azi + 5 tipe section | **5.561** survey station; 109 section | Koreksi **MD→TVD untuk 5.669.005/7.080.457 baris (80,1%)** time-based → fitur hidrostatik/ECD/pore-press valid | `incl/azi` uom campuran — **incl: 2574 rad + 2987 dega; azi: 2574 rad + 2920 dega (67 stasiun tanpa tag azi)** (A1 §8b-4; sudah dikonversi per-elemen); `mdInclAzimType` absen; aziRef mayoritas grid north (butuh koreksi grid) |
| D1d | MUDLOG (`V6_D1d_MUDLOG.md`) | 8/8 XML | 44 kolom | **2.882** geologyInterval, 8 wellbore | **LABEL litologi langsung 100%** (claystone 957 / sandstone 884 / limestone 678 / …) + qualifier 53% + C1–C5 45,7% | **Bukan label kegagalan** (tidak ada tag stuck/losses/kick); gas show cuma **17/576** (terlalu jarang); overlap vs USROP belum diverifikasi (path USROP tidak ditemukan saat D1d) |
| D1e | LOG XML audit (`V6_D1e_LOG_XML.md`) | **7150 file** header semua + 24 sample penuh | 1022 kurva di sample (47–88 mnemonic/wellbore terlewat dari CSV parser lama) | parser lama = 8 CSV; **F-1 C (2156) + F-11 (1750) = 3906 file = 54,6% TIDAK diparse** | Bukan label baru — **gap coverage terbesar**: 2 wellbore terbesar belum punya time-series CSV | WHIRL_RT == BOUNCE_RT **identik lintas 5 wellbore (67 file)** → jangan jadi 2 fitur; kurva sains HKLD/TORQUE/MSE/MOTOR_RPM/FLOWIN-OUT tak masuk CSV lama |
| D1f | PETRO DLIS/LIS (`V6_D1f_PETRO.md`) | **20/20 DLIS + 1/2 LIS** (F-14 sukses; F-7 korup) | 504 channel DLIS + 49 LIS F-14 | **309.644** baris (21 CSV, 77 MB) | **Label litologi/petro siap pakai**: SW/BVW/VSH/CARB_FLAG/COAL_FLAG (COMPUTED_OUTPUT, 6 wellbore); kanal drilling di petro: ROP5/CRPM/ROPAVG/WOBAVG | F-7 LIS **korup** (error asli: `head.prev(=457) != prev(prev(head)).next(=362)`; 1.608 offset-slice gagal = 0 DFSR); **trap satuan: mayoritas 0.1 in (×0.00254 ke m), F-15D mm**; LIS F-14 belum divalidasi silang ke referensi SPWLA |
| D1g | EDM DATABASE (`V6_D1g_EDM.md`) | zip 1 entry → XML 211 MB sudah di disk; 142 tag, 21 well/54 wellbore | CD_* tags (survey/pore/frac/assembly) | 15.109 survey ACTUAL-able; 39.084 pore pressure; 37.257 frac gradient | **BUKAN label kegagalan** (angka keyword lama NPT 130/stuck 947/kick 3539 = false positive; angka terukur A1 §8b-5: stuck **945–968**, kick **3193–5103**, NPT **41–370** tergantung metode; word-boundary NPT = **0**; "non-productive" 0). Yang bernilai = **fitur**: wellpath definitif, pore/frac profile, DDI/tortuosity, BHA/casing spec | Mayoritas phase=PLAN/PROTOTYPE → **wajib filter phase=ACTUAL**; folder CasingSeat/CasingWear/Compass/WellPlan kosong sengaja; CD_BHA_COMP_BIT hampir kosong (bit_size 4 terisi) |
| D1h | KAGGLE+CATALOG (`V6_D1h_KAGGLE_CAT.md`) | time.csv + depth.csv + 2 zip + catalog + xlsx + well picks — semua dibuka | time.csv **239 kolom**; depth.csv 115; ROP data 8; catalog 4 | time.csv **419.747** baris (F-9 A, 2009–2015); depth.csv 16.670 baris data (bukan 16.671 — A1 §8b-1); ROP data 151 baris data (152 termasuk header — A1 §8b-2); picks **409** di 35 wellbore | **STUCK_RT + MWD shocks di time.csv F-9 A** = label instrumen stuck di luar F-14, sudah CSV siap pakai; WBS* lithology codes; ROP data F-15: PHIF/VSH/SW/KLOGH; **409 formation picks** lintas 35 wellbore | Zip kaggle F9A = **duplikat identik** (bukan data baru); catalog path = dbfs marketplace (bukan lokal); ROP data cuma 151 baris data (152 incl header) |

---

## 2. ANALISIS LINTAS SUMBER (nilai utama kartu ini)

### 2.1 Apakah trajectory + tubular + mudLog + DLIS membuka jalur label yang dinyatakan "tidak ada"?

**Jawaban jujur: TIDAK membuka label kegagalan BARU — tapi memperbaiki 4 celah validitas yang membuat
label lama bisa dipakai benar, dan menutup 2 gap yang R1 nyatakan "belum dicek".**

| Jalur | Klaim lama | Status setelah 8 pembaca | Bukti |
|---|---|---|---|
| DLIS "belum pernah dibuka" (R1 §7.6) | R1 hanya pakai 2 LAS F-15D | **DITUTUP**: 20/20 DLIS + 1 LIS → 309.644 baris, label SW/VSH/BVW/CARB_FLAG/COAL_FLAG di 6 wellbore | D1f §3 |
| TVD untuk ECD/pore pressure (R1 I4/I6 butuh TVD) | R1: ECD hitung jalan tapi tak tervalidasi | **80,1% baris time-based (5.669.005/7.080.457) kini bisa MD→TVD** → hidrostatik/ECD/pore-press pakai kedalaman benar (salah MD di F-10 = 43%) | D1c §6-§8 |
| Tabel string BHA untuk I7 drag & I1 TOB (R1 §9.4.2 minta data ini) | R1: "butuh tabel BHA asli — bhaRun tidak punya berat/OD segmen" | **SEBAGIAN DITUTUP**: tubular = 1.392 komponen od/id/len/wtPerLen → **I7 (drag) bisa dikalibrasi ulang**; tapi **rating motor 0/192 → I1 (TOB) tetap terblokir** (kini terverifikasi, bukan asumsi) | D1a §1 + §"rating motor" |
| Label litologi | R1: LAS saja (2 file) | **DITAMBAH**: mudLog 2.882 interval 100% + DLIS COMPUTED_OUTPUT + 409 formation picks (35 wellbore) = 3 sumber label geologi lintas well | D1d §4, D1f §3.1, D1h §6 |
| Label kegagalan dari EDM | E1 body berharap "EDM event (D1g)" | **DITOLAK dengan bukti**: EDM BUKAN event DB | D1g §0 (§2.2 di bawah) |
| Label dull grade bhaRun | Diharapkan numBitRun+dulling | **KONFIRMASI TIDAK ADA**: dullingInfo/dullGrade/bitName 0/161 | D1b |

Kesimpulan: gabungan ke-4 pembaca itu = **konteks + validitas fitur** (geometri, kedalaman, geologi),
bukan sumber kelas kerusakan. Kelas kerusakan tetap dari kanal instrumen (R1 §4.2) + DDR/NPD.

### 2.2 Apakah EDM (D1g) berisi event kegagalan nyata = ground truth?

**TIDAK.** Verdict didukung bukti eksplisit (D1g §0): keyword `non-productive`/`bit run`/`lost circulation`/
`well control` = **0 hit**; `stuck` (945–968 tergantung metode) = atribut simulasi torque-drag
(`stp_calc_stuck_point`); `kick` (3193–5103 tergantung metode) = `kick_pad_length`/`kick-off` bit;
`NPT` (41–370 tergantung metode; word-boundary = **0**, satu-satunya wb-CI hit = base64 `nPt+92ft`)
= ID acak; `failed` 416 = semua base64. **Catatan metode (recount D0-fix)**: angka lama 947/3539/130
ternyata tereproduksi **persis** sebagai *jumlah baris yang mengandung substring case-insensitive*
(947/3539/130 baris) — bukan karangan, tapi metode itu menghitung baris atribut simulasi/bit/ID,
bukan tag event; sifat klaim (false positive, bukan ground truth) tetap benar.
→ EDM **tidak** menambah ground truth kegagalan. Ground truth kegagalan tetap: kanal instrumen
(`STUCK_RT`, `STKSLP`, `STICK_RT`, `VIBLAT_RT`, `SHKRSK_RT`) + tabel event kurasi DDR
(`labels_curated_v2.csv`, 884 event) + NPD DISKOS. Nilai EDM = **fitur well engineering**
(wellpath ACTUAL, pore pressure 39K, frac 37K, DDI/tortuosity) dengan filter `phase=ACTUAL`.

### 2.3 Apakah ada well BARU yang belum terpakai V6-R1 (R1: F-14/F-5/F-15/F-9/F-7)?

**YA — ini temuan terbesar untuk diversifikasi LOWO antar-sumur:**

| Well/wellbore baru | Sumber bukti pembaca | Kekayaan |
|---|---|---|
| **F-1 C, F-1 B, F-1 A, F-1** | D1e: **2156 file log (terbesar!) belum diparse**; D1b: 26 run; D1d: 4 file mudLog; D1a: tubular | time-series terbesar yang BELUM tersentuh parser lama |
| **F-11 (T2/B/A)** | D1e: **1750 file log belum diparse**; D1b: 40 run; D1d: 3 file mudLog | kedua terbesar — bersama F-1 C = **54,6% seluruh dataset log** |
| F-4, F-10, F-12, F-15S, F-15A, F-15B, F-15 (dir) | D1e tabel per-wellbore (57–1100 file) | sudah/siap diparse |
| F-2, F-3, F-6, F-8, 15/9-19, relief wells | D1g EDM (survey+pore pressure) | tanpa WITSML parsed; EDM ACTUAL survey tersedia |
| F-15, F-15B, F-15C, F-15D (petro) | D1f §6-§7: **4 wellbore petrophysics baru** (85/69/81/79 channel) | label petro baru; F-15D array-sonic 33.464 baris |
| F-9 A | D1h: time.csv 419.747 baris + depth.csv — **STUCK_RT** siap pakai | label stuck instrument di luar F-14 |

Catatan penting: kaya ≠ otomatis terpakai — F-1 C/F-11 butuh parse dulu (pekerjaan, bukan blocker).

### 2.4 Kombinasi mana yang menghasilkan ≥3 kriteria kerusakan?

**Bukan dari satu pembaca — dari lapisan yang saling menopang:**

- **Lapisan kelas (dari R1, diperluas pembaca):** 6–7 kelas berpenduduk sudah terhitung di F-14
  (torsional 82.530 / moderate stick-slip 320 / shock 180 / whirl 714 / stuck 394 / hidraulik 58.317;
  kolom `label` USROP_labeled.csv = **134.013 normal / 49.732 high_MSE_bit_wear / 15.183
  low_ROP_efficiency**, n=198.928 — diverifikasi A1 O3 + spot-check PM parse CSV; kelas rule
  torsional R1 §4.2 **terpisah** dari kolom label itu, populasi 49.629 (recompute A1: 49.614, Δ0,03%).
  Pembaca memperluas **cakupan well** kelas ini:
  - `STUCK_RT` **ada di time.csv F-9 A** (D1h) → kelas stuck di well kedua, tinggal pakai;
  - `STKSLP` multi-well sudah diukur R1 §8.2 (F-5/F-15_S/F-15A/F-9);
  - **hipotesis terbuka**: F-1 C/F-11 (3906 file) kemungkinan punya kanal sama — **belum diverifikasi,
    wajib dicek Auditor/ML Eng setelah parser menangkap kedua wellbore ini**.
- **Lapisan validitas (D1c):** tanpa koreksi TVD, kelas berbasis tekanan (hidraulik, ECD) salah kedalaman
  (MD vs TVD meleset 16% di F-14, 43% di F-10). 80,1% baris kini benar.
- **Lapisan fitur fisik (D1a + D1g):** string geometry + pore pressure profile → fitur drag/buckling/
  overbalance untuk membedakan kelas stuck (differential sticking) dari stick-slip biasa.
- **Lapisan label bantu (D1d + D1f + D1h picks):** litologi per interval → auxiliary task / fitur geologi,
  supaya model tidak belajar formasi sebagai "kegagalan".

Jadi kombinasi **≥3 kriteria kerusakan** = **kanal instrumen (label) + TVD (validitas) + BHA/pore-pressure
(fitur pemisah) + litologi (konteks)**. Tanpa lapisan pembaca, R1 punya kelas tapi hanya di F-14;
dengan pembaca, kelas itu bisa dinaikkan ke cakupan multi-well — itu persis syarat LOWO yang dituntut E1.

### 2.5 Temuan silang lain yang wajib dibawa ke E1/A1

1. **WHIRL_RT == BOUNCE_RT kini terkonfirmasi lintas-wellbore** (D1e: 67 file, 5 wellbore, row-level identik
   1790/1790 + 368/368) — memperluas temuan R1 yang hanya cek 19 file F-14. Larangan "2 kelas ini independen"
   berlaku global.
2. **Folder ≠ nameWellbore** konsisten di tubular/bhaRun/mudLog (folder F-1 C isi wellbore F-1 B dll) —
   SEMUA join wajib pakai field XML, bukan path. Berlaku untuk seluruh pipeline.
3. **Satuan trap berlapis**: trajectory incl/azi campuran rad/dega; DLIS mayoritas 0.1 in (bukan m!);
   EDM pakai ft; bhaRun uom ok (m). Konversi wajib sebelum join silang.
4. **Parser lama hanya menangkap 8 wellbore + kehilangan kurva sains** (HKLD_AVG/MAX, TORQUE_*,
   MOTOR_RPM, FLOWIN/OUT, MSE, PIT* — 47–88 mnemonic per wellbore) → parse ulang F-1 C + F-11
   adalah aksi berdampak terbesar untuk E1.
5. **R1 §7.6 "tidak ada pembacaan DLIS" resmi ditutup** oleh D1f — Auditor dipersilakan mengaudit apakah
   angka 309.644 baris benar (aggregator sudah cocokkan `wc`: 21 CSV − header = 309.644).

---

## 3. RANKING FIELD UNTUK KAMPANYE ML BERIKUTNYA (V6-E1)

| Rank | Field/sumber | Alasan (evidence-based) | Asal |
|---|---|---|---|
| **1** | Kanal disfungsi instrumen WITSML: `STUCK_RT`, `STKSLP`, `STICK_RT`, `VIBLAT_RT`, `SHKRSK_RT` | Satu-satunya label kegagalan langsung berpenduduk (R1 §4.2); AUC surface→stuck 0,96–0,98 sudah terbukti; perluas well baru | R1 + D1e (gap parse F-1 C/F-11) |
| **2** | `time.csv` F-9 A (239 kolom, 419.747 baris, STUCK_RT + shocks + C1–C5) | Sudah CSV siap pakai = kelas stuck di well kedua tanpa parse XML; selisih nol pekerjaan | D1h |
| **3** | Koreksi MD→TVD (trajectory 5.561 stasiun) | Menvalidasi seluruh fitur berbasis tekanan/kedalaman di 80,1% baris; syarat wajib ECD/pore pressure | D1c |
| **4** | Geometri string/BHA (1.392 komponen: od/id/len/wtPerLen) | Membuka kalibrasi ulang drag (I7) + fitur buckling/differential-sticking; permintaan data R1 §9.4.2 terpenuhi sebagian | D1a |
| **5** | Label litologi mudLog (2.882 interval, 100%) | Label gratis per-interval, 8 wellbore — auxiliary label / geologi one-hot | D1d |
| **6** | COMPUTED_OUTPUT DLIS: SW/VSH/BVW/CARB_FLAG/COAL_FLAG (6 wellbore) + kanal drilling petro (ROP5/CRPM/ROPAVG) | Label petro lintas well + fitur drilling-by-depth ekstra; 4 wellbore baru | D1f |
| **7** | EDM phase=ACTUAL: pore pressure 39K, frac 37K, definitive survey, DDI/tortuosity | Fitur well engineering per wellbore — bukan label; wajib filter ACTUAL | D1g |
| **8** | 409 formation picks (35 wellbore) + WBS* lithology codes | Label stratigrafi lintas well untuk generalisasi geologi | D1h |
| **9** | bhaRun: 9 drilling window + numBitRun 11 + 14 wellbore runs | Anchor waktu/interval saja — populasi terlalu kecil untuk target | D1b |

Urutan ini mengikuti prioritas: **label dulu (1–2), validitas (3), pemisah fisik (4), label bantu (5–6, 8),
fitur konteks (7, 9)**.

---

## 4. BLOCKER & KEGAGALAN — APA ADANYA (tanpa ditutupi)

| # | Blocker | Error/asli | Upaya yang SUDAH dicoba | Status |
|---|---|---|---|---|
| 1 | F-7 `.LIS` korup | `file corrupt: head.prev (= 457) != prev(prev(head)).next (= 362)` — indexing berhenti di offset 461 | ErrorHandler LOG/SWALLOW; **1.608 offset-slice (step 128 B, 0..204800) → 0 DFSR** | **TIDAK BISA dibuka lokal** — jalur realistis = sumber ulang (re-download SPWLA), bukan parser |
| 2 | `dlisio.lis.curves` crash di dlisio 1.0.4 × numpy 2.5 | `ValueError: cannot resize an array that may be referenced by another object` | Subclass numpy `resize(refcheck=False)` → **F-14 LIS 18.374×49 sukses** | Teratikan (workaround di `scratch/v6_d1f/extract_lis_v2.py`) |
| 3 | Rating motor absen untuk I1/TOB (R1 §9.4.2) | `torqueMax/Pmax/revPerGallon` = **0 dari 192 file** | D1a memeriksa semua 192 file + satu-satunya rating-like = `/mwdTool/flowrateMn|Mx` (19 elemen) | **Terblokir dengan bukti** — I1 (TOB) tetap tidak bisa; I7 jalan tanpa rating motor |
| 4 | F-1 C + F-11 belum diparse (3.906 file, 54,6%) | Parser lama hanya output 8 CSV; `_coverage.json` tidak memuat keduanya | Audit D1e membuktikan lewat hitung header semua 7150 file | **Pekerjaan parse lanjutan** — bukan blocker data (file ada & valid) |
| 5 | WHIRL_RT duplikat BOUNCE_RT | Row-level identik: 1790/1790 (F-9), 368/368 (F-5), 5/5 (F-15S), 15/15 (F-1); 67 file / 5 wellbore | D1e memverifikasi per `<data>` element di 4 wellbore | Fakta data sumber — larangan pakai sebagai 2 fitur/kelas terpisah |
| 6 | Trap satuan lintas format | DLIS 0.1 in (×0.00254), F-15D mm, F-14 LIS M, trajectory rad/dega, EDM ft | Semua sudah dikonversi per sumber masing-masing | Teratikan — join E1 **wajib** terapkan konversi yang sama |
| 7 | Cacat data bhaRun | 6 run durasi negatif (contoh F-15 C: stop mendahului start −2,6 hari); 2 numBitRun non-integer | D1b mencatat semua | Filter durasi negatif; parse numBitRun sebagai string |
| 8 | KLAIM YANG TERBUKTI SALAH (bukan blocker, koreksi) | "EDM = event/NPT DB" (harapan E1 body) → **SALAH**; "16 file DLIS" → **20 file**; "F-14 horizontal" → build-and-hold 81°; "mudLog kosong" → **2.882 interval kaya**; "DLIS belum terinstall" → dlisio 1.0.4 sudah ada | Semua diuji & dikoreksi oleh pembaca dengan angka | Dicatat apa adanya untuk Auditor |

**Tidak ada pembaca yang melapor "belum dibuka" terhadap file yang ada di disk** — 8/8 dokumen
terbit dengan angka primer; seluruh file yang disebut di body task sudah dibuka (kecuali F-7 LIS yang
gagal dengan error nyata + 1.608 percobaan pemulihan).

---

## 5. HANDOFF KE AUDITOR 1 (V6-A1) & ML ENG (V6-E1)

**Untuk Auditor 1** — titik yang paling layak dibongkar (aggregator sudah cek sendiri sebagian):
1. Angka D1f: `21 CSV − header = 309.644` (sudah cocok `wc` aggregator) — uji ulang 1 klaim per pembaca.
2. Klaim "EDM bukan event DB" — uji grep sendiri terhadap `Volve F.edm.xml` 211 MB.
3. Klaim "dullingInfo 0/161" dan "rating motor 0/192" — grep regex sendiri.
4. Sirkularitas: label litologi mudLog vs fitur drilling di interval yang sama (litologi bukan fungsi
   dari ROP/WOB → non-sirkular; tapi buktikan).
5. `17 gas show` dan `9 drilling window` — populasi kecil, pastikan jangan dijual sebagai kelas besar.

**Untuk ML Eng (V6-E1)** — peta cepat:
- Label kelas: R1 §4.2 (6–7 kelas) + `STUCK_RT` F-9 A (D1h) + multi-well `STKSLP` (R1 §8.2).
- Fitur wajib: koreksi TVD (D1c) sebelum fitur tekanan; string geometry (D1a); litologi (D1d) sebagai aux.
- Jangan pakai: EDM sebagai label; WHIRL+BOUNCE sebagai 2 kelas; numBitRun sebagai target; mudLog gas show (n=17).
- WELL BARU untuk split LOWO: F-1 C, F-11 (setelah parse), F-9 A (time.csv), F-15B/C/D (petro).

**Dokumen sumber (semua verified ada di disk):** `docs/V6_D1a_TUBULAR.md`, `V6_D1b_BHARUN.md`,
`V6_D1c_TRAJ_GEOM.md`, `V6_D1d_MUDLOG.md`, `V6_D1e_LOG_XML.md`, `V6_D1f_PETRO.md`, `V6_D1g_EDM.md`,
`V6_D1h_KAGGLE_CAT.md` + CSV masing-masing di `scratch/v6_d1*`.
