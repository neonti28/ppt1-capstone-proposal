# V9-EVAL_B — PENILAIAN LAPISAN B UNTUK 7 ENGINE (kerangka operator A/B/C)

Status: HASIL EVALUASI (kemampuan + batas penggunaan + kekuatan bukti per engine —
**BUKAN vonis LULUS/GAGAL**).
Sumber angka: JSON primer `scratch/v9_eval_b/v9_eval_b_RESULTS.json`
(turunan dari `_A_json.json` = ekstrak JSON primer E_ML/E_STAT/E_RULE, dan
`_B_b4.json` = B4 + retrain RF terverifikasi identitas). Dihitung skrip
`code/v9_eval_b_01_json_extract.py`, `v9_eval_b_02_b4_compute.py`,
`v9_eval_b_03_merge_verify.py`. Verifikasi: V1 17/17 · V1b ✓ · V2 ✓ · V3 ✓ ·
V4 22/22 AUPRC (diff 0) + 110/110 TP/FP · V5 16/16 · V6 62/62 (§4).

## Baris riset pendahuluan

- Riset pendahuluan: scientific-critical-thinking — B1/TLead/B4 hanyalah "waktu" tanpa
  beban; keputusan kunci = MENGIKAT tiap metrik waktu ke B3 (pengurangan pemeriksaan)
  pada tabel joint, supaya "cakupan peringatan tinggi yang menambah 77× pekerjaan"
  tidak terbaca sebagai nilai; hipotesis alternatif (definisi alarm-transisi, definisi
  blok ≥5 mnt) diuji lewat sensitivitas L=30 dan recompute independen, bukan dilindungi.
- Riset pendahuluan: verification-mandatory — semua angka = kutipan JSON primer;
  B3 dire-sum dari FP mentah E_RULE (17/17), B1 diekstrak ulang dari E_ML (✓),
  B4 dihitung ulang dengan implementasi berbeda (27=27 margin, 216=216 blok),
  retrain RF lolos gate identitas (AUPRC selisih 0 tepat + TP/FP per tau eksak 110/110);
  kegagalan verifikasi pertama V3 (implementasi alternatif tak menerapkan spesifikasi
  gap-split) dilaporkan lalu diperbaiki — bukan disembunyikan; daftar "belum terukur"
  terpisah dari "gagal" (§5).
- Riset pendahuluan: statistical-analysis — metrik dilaporkan sebagai rentang/median+
  IQR per fold (bukan satu titik), fold UNDERPOWERED dilabeli (hyd K-ii 3 onset,
  tool_wear n run=8, bit_wear 3 fold), coverage ≠ margin (keduanya selalu berpasangan),
  dan FP/BEBAN diberi satuan aslinya (jendela 1 menit rig; detik bengkel) — FAR/24jam
  tidak dihitung ulang di dokumen ini (milik EVAL_A).
- Riset pendahuluan: what-if-oracle — 6 cabang penilaian diuji: Ω "semua kelas punya
  titik coverage-tinggi dengan B3≥0" (tidak terjadi di data), α "joint B3×B4" (DIPILIH),
  Δ "nilai B4 tanpa B3" (menghasilkan kesimpulan salah: RF ssi/shk tampak 'layak
  peringatan dini' padahal beban 212–488× status quo), Ψ "tuntut B1≥80% utk kelas
  status" (dilarang PM1 §4.7), Φ "pakai persistence-horizon B1 0,93–0,97 sbg bukti"
  (hindsight — dibuang, dipakai sbg batas-atas), ∞ "alarm-transisi menutup cakupan RF
  tau0,05" (vib coverage 0 dgn 158 alarm = pred persisten jarang bertransisi)
  → dicatat sbg keterbatasan metrik, bukan kegagalan model.
- Riset pendahuluan: consciousness-council — 5 arketipe mempertahankan 4 ketegangan:
  (Empiricist) bukti identitas retrain 22/22 = fondasi semua angka B4; (Pragmatist)
  nilai pemeliharaan terukur hari ini = hyd K-i hybrid, tool_wear FAR-terkalibrasi,
  ssi hybrid; (Contrarian) coverage tertinggi selalu berpasangan dgn B3 terburuk —
  tanpa tabel joint EVAL_B akan "menjual" peringatan dini fiktif; (Architect) B4 =
  fungsi definisi (blok ≥5 mnt: ssi hanya 40/137 run lolos; L30 melipatgandakan
  coverage) → parameter selalu ikut dilaporkan; (Historian) pola V8 terulang:
  B3 shk RF negatif (V8 −0,11…−53,75 → V9 −1,83…−212,5).
- Riset pendahuluan: sequentialthinking — 4 pikiran: (1) kunci definisi B1–B4 +
  larangan biner, (2) inventaris data + anomali sumbu waktu (ts_bin = menit-integer,
  grid 1 mnt), (3) desain joint B3×B4 + gate identitas retrain RF, (4) gerbang
  verifikasi + sintesis council/what-if sebelum dokumen ditulis.

---

## 0. METODE PENILAIAN LAPISAN B

Kerangka (operator, "Evaluasi User.txt" via PM1 §4.7): **Lapisan B = apakah bernilai
pemeliharaan** — peringatan sebelum kondisi memburuk, waktu untuk bertindak (TLead vs
kejadian nyata), pengurangan pemeriksaan tak perlu. Definisi metrik mengikuti
`V8_R1_ABC_SPEC.md §1.3`:

| Metrik | Definisi operasional | Kelas |
|---|---|---|
| **B1** cakupan peringatan-dini | % onset dengan alarm dalam `[t_e − H, t_e)`, H = 10 mnt | onset |
| **B2** waktu-untuk-bertindak | TLead median/IQR vs **anchor kelas**; kategorikal ≥30 / 10–30 / <10 / nol mnt | onset |
| **B3** pengurangan pemeriksaan | `kurangi_ragu = 1 − FP_engine / FP_baseline_rule` (aturan status-quo) | semua dgn FP |
| **B4** margin status-awal | median menit antara alarm terdekat SEBELUM entry blok status **berkelanjutan ≥5 mnt** | status |

Keputusan evaluasi (mengikut dokumen ini):

| # | Keputusan | Alasan |
|---|---|---|
| EB-1 | 7 engine = **11 klaim** (vib, ssi, shk, stuck K-i+K-ii, hyd K-i+K-ii, bit_wear K-1+K-2, tool_wear K-i+K-ii), mengikuti EA-1 | klaim terpisah punya tugas, label, baseline berbeda |
| EB-2 | Grid = **1 menit** (ts_bin integer-menit; konvensi E_ML `FAR=1440·FP/n_neg`); semua margin/TLead dalam menit, tool_wear dalam detik bengkel; unit selalu dinyatakan | konversi-skala wajib dianotasi (PM1 §4.6b) |
| EB-3 | Baseline B3 per kelas: kelas status = **rule status-quo E_RULE**; stuck K-ii = **rule E1** (pemicu pemeriksaan terdekat utk onset; display status-quo tidak memprediksi onset); hyd K-ii = rule z-pit (**FP eval = 0 by construction → B3 tidak terdefinisi; beban dilaporkan terpisah**); tool_wear = rule 3-RMS; bit_wear = belum terukur | baseline harus bisa dijawab "apakah alat ini mengurangi kerja inspeksi?" |
| EB-4 | Resep B4 (dinyatakan pra-komputasi): blok = run `y=1` per sumur, **diputus bila jeda ts > 2 menit** (merge gap ≤2 mnt, resep V8-E_shk), **berkelanjutan = durasi ≥5 menit** (K_SUSTAIN V8 pra-reg); alarm = **transisi pred 0→1** (resep V8 `alarm_events`); margin = `t_entry − t_alarm_terdekat` dalam lookback **L = 10 mnt** (utama) + **L = 30 mnt** (sensitivitas); konfirmasi-delay (alarm pertama pada/setelah entry) dan alarm reaktif (di dalam blok) dilaporkan TERPISAH dari margin | anti pilih-pilih; V8-E_shk 02 = preseden |
| EB-5 | B4 komponen RF (vib/ssi/shk) = **retrain deterministik** (seed 42, resep E_ML identik, fold dari `lowo_*.json`) dengan **GATE IDENTITAS**: AUPRC per fold selisih ≤1e-6 DAN TP/FP per tau eksak vs JSON E_ML — hasil **22/22 AUPRC (selisih 0,00e+00) + 110/110 TP/FP** → skor dijamin identik dgn run E_ML; tanpa lolos gate, B4 RF = "belum terukur" | E_ML tidak menyimpan skor OOF; retrain diverifikasi, bukan asumsi |
| EB-6 | Anchor B2 **per kelas, dilarang dipinjam**: stuck = 2,67–7,37 mnt (Crossformer di Volve, R1-S1 §2.2); tool_wear = akhir run R02 (alat tumpul) — **anchor numerik formal "RUL bengkel" tidak didefinisikan di PM1/R1** → dilaporkan absolut (detik) + kategori, tanpa mengarang angka anchor; kelas status memakai **B4** (bukan TLead) | aturan operator: jangan tuntut standar identik antar tugas |
| EB-7 | Band referensi **bukan vonis**: B1 ≥50% / B4 median ≥1 menit = "arah benar" (V8_R1 §1.3); B1 ≥80% hanya syarat L0-alarm kelas onset; **dilarang menuntut B1≥80% dari kelas status** (PM1 §4.7) | kerangka operator menggantikan gate lift 1,5 |
| EB-8 | Tidak ada vonis biner: tiap klaim ditutup "memenuhi lapisan B untuk X / belum untuk Y / belum terukur untuk Z" + bukti angka; "belum terukur" ≠ "gagal"; korelasi ≠ kausalitas ditegaskan | aturan penilaian operator 1–6 |

Cakupan eksekusi: B1/B2 dari JSON E_ML (28 fold onset + 3 model), E_STAT (4 engine),
E_RULE (37 fold + 7 + 4 + 1 split); B4 dari 5 kelas status (dataset D1, 6 dataset,
grid 1 mnt) + retrain RF 22 fold (vib 4, ssi 9, shk 9).

---

## 1. TABEL RINGKAS — 7 ENGINE, 11 KLAIM (LAPISAN B)

Legenda: **B3** = kurangi_ragu vs rule status-quo (positif = memangkas pemeriksaan);
**cov** = fraksi blok berkelanjutan (≥5 mnt) yang punya alarm di lookback L=10;
**margin** = median menit alarm terdekat sebelum entry blok; **konf** = median menit
alarm pertama SESUDAH entry (konfirmasi, bukan peringatan). "Titik B3≥0" = titik
operasi yang tidak menambah beban inspeksi vs sistem hari-ini.

| Engine / klaim | Tugas | B1 / B2 (onset) atau B4 (status) | B3 vs baseline | Kesimpulan kemampuan / batas |
|---|---|---|---|---|
| **vib** (K tunggal) | status VIBLAT≥32,17405 | B4 rule/hybrid: **cov 26,4% · margin 5,0 mnt [IQR 3–7]** (L30: cov 50,9% · 10 mnt); persistence: cov 12,5% · 5,0; RF: cov **0–8,8%** · margin 2,5–7,0; konf semua = 10 mnt (1 jendela) | rule **0,00** (=status-quo); hybrid 0,00; persistence **−6,39**; RF **−9,41…−76,77** (GB −10,42…−48,96; LR −32,10…−83,67) | **Memenuhi** utk konfirmasi-status + peringatan dini terbatas (margin ≥1 mnt pada 26,4% blok, tanpa menambah beban: rule/hybrid B3=0); **belum** utk RF sbg nilai tambah pemeliharaan (semua tau menambah FP 10–77× vs status-quo; coverage RF justru ≤8,8%); **belum** utk peringatan dini menyeluruh (74% blok tanpa alarm prablok) |
| **ssi** (K tunggal) | status SSI≥1 | B4: hanya **40/137 run** berkelanjutan ≥5 mnt (median run 2 mnt — kelas didominasi event pendek). rule: cov 5,0% · 5,5 mnt; hybrid: cov **0%** (konf 10 mnt); persistence: cov 7,5% · 4,0; RF τ0,05: **cov 27,5% · 5,0 mnt**; RF τ0,3: cov 2,5% · 1,0 mnt; RF τ0,5: cov 0% | rule 0,00; **hybrid +0,731** (FP 26→7); persistence −9,27; RF τ0,05 **−487,77**, τ0,3 −2,85, **τ0,5 +0,846** (FP 4) | **Memenuhi** utk pengurangan pemeriksaan pada hybrid (+73% vs rule) — dengan catatan recall hybrid ≤0,03 (EVAL_A) → "hemat-awas", bukan detektor; **belum** utk peringatan dini berbiaya-wajar (cakupan 27,5% hanya dgn beban 488×; di titik hemat B3≥0 cakupan nol); **belum terukur** utk 97 run pendek (di luar definisi blok berkelanjutan) |
| **shk** (K tunggal) | status SHKRSK≥1 | B4 rule/hybrid: cov **13,4%** · 4,5 mnt [IQR 3–7] (L30: 27,4% · 11); persistence: cov 11,0% · 5,0; RF τ0,05: cov 25,0% · 4,0 mnt; τ0,2: 3,0% · 9,0; **τ0,5: cov 0,6% (1/164 blok) · 4,0**; konf rule/pers 10 mnt | rule 0,00; hybrid 0,00; persistence −7,73; RF τ0,05 **−212,53**, τ0,3 −1,83, **τ0,5 +0,678** (FP 39 vs 121) | **Memenuhi** utk lapisan dasar rule berbiaya-status-quo (B3=0, peringatan menyusut 4,5 mnt pada 13,4% blok); **belum** utk RF sbg pengurang pemeriksaan + peringatan dini (titik B3≥0 hanya menangkap 1 blok); konsisten dgn V8 (B3 RF negatif −0,11…−53,75) → pola lama berulang |
| **stuck K-i** (status) | blok STUCK persisten (2 fold: F-14, F-9_A) | B4 rule: cov **11,8%** · 5,0 mnt [IQR 4–6]; hybrid: cov 11,8% · 5,0; persistence: cov 7,9% · 5,5; E1: cov 2,6% · 5,0 (**konf 58,5 mnt** — E1 jarang menyala pasca-blok); konf rule/pers 10 mnt | rule 0,00; hybrid 0,00; **hybrid-E1 +0,163** (FP 41 vs 49); persistence −7,90; E1 −2,27 | **Memenuhi** utk konfirmasi-status berpresisi tinggi (P 0,92–0,97, EVAL_A) + peringatan menyusut ~5 mnt pada 11,8% blok tanpa menambah beban; hybrid-E1 memangkas 16% FP; **belum** utk peringatan dini menyeluruh; **kekuatan bukti terbatas** (cakupan E_RULE 2 fold; B4 dihitung pada 2 sumur yang sama — dataset = fold) |
| **stuck K-ii** (onset, H=10) | prediksi onset 0→1 | **B1 / TLead (median antar-fold)**: RF τ0,05 **B1 0,51–1,00** · TLead **10–11,5 mnt** (IQR atas s/d 28–33); RF τ0,1 B1 0,36–1,00 · 8–11,5; RF τ0,2 B1 0–1,00 · 7–10; **RF τ0,5 B1 0–0,045 · 2–159**; E2 q95 **B1 0–0,181 · TLead 2,5–8** (IQR 1,75–10); E1 **B1 0–0,066 · 1–5**; persistence-EVENT **B1 0–0,115 · 4,5–8,5 (median fold-median 7,0)**; persistence-HORIZON B1 0,93–0,97 · 1–3 (**HINDSIGHT**) | vs E1 (FP 422): RF τ0,05 **−77,05** (FP 32.938); τ0,1 −54,38; τ0,3 −4,95; **τ0,5 +0,604** (FP 167); q95 −12,77; E2 **−0,924** (FP 812); **persistence-EVENT +0,974** (FP 11); persistence-HORIZON +1,00 (hindsight) | **Memenuhi** utk (i) triage ranking (EVAL_A) dan (ii) peringatan dini pada beban rendah dengan **arah benar tapi kuantitas kurang**: persistence-EVENT TLead 7 mnt ≈ anchor 2,67–7,37 tapi B1 hanya 0–11,5%; **belum** utk peringatan dini operasional: satu-satunya titik B1≥50% (RF τ0,05, TLead 10–11,5 mnt ≥ anchor) berbiaya **77× beban status-quo** (FAR 267–812/24jam); E2 TLead di anchor tapi B1 ≤18% + CI memuat prevalensi (bukti lemah); persistence-HORIZON = batas-atas hindsight, bukan dasar klaim |
| **hyd K-i** (status) | \|z\|>2 residu SPPA (9 fold) | B4 hybrid: cov **13,0%** · 4,5 mnt [IQR 3–8]; persistence: cov 10,5% · **7,0 mnt [IQR 4–9]**; rule (tautologi): cov 20,6% · 3,0 mnt (**konf 4 mnt**); deteksi-transisi JSON: **delay median 0–3,5 mnt**, terdeteksi ≤H10 **31,6–65,4%** | rule 0,00 (pembentuk label); persistence **+0,072**; **hybrid +0,557** (FP 2091→927) | **Memenuhi lapisan B paling kuat di antara kelas status**: hybrid memangkas **56% pemeriksaan** vs tampilan hari-ini sambil mempertahankan P/R ≥0,52 (EVAL_A), plus peringatan menyusut 4,5 mnt pada 13% blok; **belum** utk alarm otomatis (FAR 14,6–58,4/24jam, EVAL_A) dan **belum** utk peringatan dini menyeluruh (87% blok tanpa alarm prablok) |
| **hyd K-ii** (onset, H=10) | prediksi kick/loss proxy (1 split temporal) | **B1 = 0/3 onset** (varian fisher/Pearson, TLead = nol); rule z-pit: **TLead = 0 (10/10 kejadian), B1 = 0%** → kategori **"nol"** (deteksi saat-kejadian, bukan prediksi); selalu-negatif: B1 0; **RF V8 (referensi)**: B1 66,7% (2/3), TLead 7 mnt, FAR 5,9 — 3 onset = UNDERPOWERED | **B3 tidak terdefinisi** (FP rule eval = 0 by construction → pembagi nol). Beban: rule z-pit = **1.348 mnt-episode** total (35 mnt uji); varian fisher FP **177 jendela** @q95 (FAR 31,6/24jam) | **Belum memenuhi** lapisan B utk peringatan dini pada titik operasi V9 (0/3 onset terdeteksi, TLead nol utk rule status-quo); **memenuhi terbatas** sbg eksplorasi ranking (lift 5,95 dgn CI memuat prevalensi); indikasi dini hanya ada sbg **angka referensi V8** (belum diulang di V9); kontrol-positif kurasi **belum tersinkron zona-waktu** (tripwire PM1 §5.1) |
| **bit_wear K-1** (status) | blok high_MSE (Teale), 7 fold USROP | **B4 BELUM TERUKUR** — pipeline D1 tidak memuat dataset USROP (6 dataset rig); persistence per resep `y(t−1)` secara konstruksi menyusul blok (margin ≤0) = sifat metode, BUKAN pengukuran; komponen rule = pembentuk label (E_RULE meta) | **B3 BELUM TERUKUR** — E_RULE/E_STAT tidak menghitung TP/FP utk kelas ini (konsisten EVAL_A §2.6) | **Belum terukur** (bukan gagal): nilai B utk K-1 baru bisa dinyatakan setelah run ulang dgn TP/FP per baris pada fold identik; ranking vs canary (A, ΔB 5/5 scorable) tetap tercatat dari EVAL_A |
| **bit_wear K-2** (onset) | prediksi onset blok high_MSE | — (B1/B2) | — | **Belum terukur** — pra-reg K-2 belum terbit (E_RULE DoD-d); K-2 dilarang dipakai di tingkat apa pun s/d kampanye berangka (PM1 §2.3) |
| **tool_wear K-i** (regime, bengkel) | deteksi perubahan-regime dalam-run (detik) | **B2**: change-point TLead ke akhir R02 **median 35 dtk (27–39)**, spread antar-keluarga fitur 16,5 dtk; kalibrasi 5/27: **median 59 dtk (48–60)**, terdeteksi 4/4 (**B1 analog 100%**); **FAR-terkalibrasi: TLead 20–36 dtk**, % jendela R02 alarm 3,3–6,9 — kategori **<10 mnt**; anchor numerik "RUL bengkel" tak didefinisikan formal (EB-6) | kalibrasi mentah **0,00–0,25** vs rule 3-RMS (FAR 42,9–58,6/mnt → membatalkan penghematan); **FAR-terkalibrasi +0,909…+0,976** (FP 1–3 vs 33–41 per alat) | **Memenuhi** utk gating inspeksi bengkel: peringatan 20–36 dtk sebelum akhir run (alat tumpul) **dengan** pangkas 91–98% alarm palsu vs rule 3-RMS — satu-satunya klaim dgn B1≥50% + B3≥0 bersamaan; **belum** utk kalibrasi mentah (B3 0–0,25 dgn FAR 43–59/mnt); **batas**: skala detik bengkel (transfer ke rig TIDAK diklaim, D-A7), run-level n=8 = underpowered, spesifisitas keausan lemah (precision run 0,50, EVAL_A) |
| **tool_wear K-ii** (lintas-alat) | prediksi status keausan LOTO | V9: **tanpa engine FP/TLead** (hanya baseline ranking canary/identity) → B1/B2/B4 V9 **belum terukur**; **RF V8 (referensi)**: TLead median **47,5 dtk (35–59)** dgn FAR-terkalibrasi ≤1/mnt, FP 1–3, deteksi 4/4 | B3 V9 **belum terukur** (RF tidak dijalankan di V9, EA-7); identity-majority & canary = ranking tanpa alarm | **Belum terukur di V9** utk aspek waktu/beban; kemampuan indikasi-dini hanya sbg **referensi V8**; ranking margin kecil di atas canary (ΔB 4/4 V8) tetap tercatat di EVAL_A |

---

## 2. DETAIL PER ENGINE (angka JSON)

### 2.1 `vib` — B4 (status) + B3

Blok: 240 run, **216 berkelanjutan ≥5 mnt** (median run 11 mnt, maks 347), 24 pendek.

| Engine | FP (jendela) | B3 vs rule=197 | cov L10 | margin med [IQR] | konf med | cov L30 (med) | alarm / reaktif |
|---|---|---|---|---|---|---|---|
| rule (status-quo) | 197 | 0,00 | **26,4%** | 5,0 [3–7] | 10 | 50,9% (10,0) | 668 / 556 |
| hybrid = rule∧pers | 197 | 0,00 | 26,4% | 5,0 [3–7] | 10 | 50,9% (10,0) | 668 / 556 |
| persistence | 1456 | −6,39 | 12,5% | 5,0 [2,5–7] | 10 | 35,6% (14,0) | 195 / 125 |
| RF τ0,05 | 15321 | −76,77 | 0,0% | — | — | 1,4% (18,0) | 158 |
| RF τ0,1 | 13075 | −65,37 | 4,2% | 7,0 [5–8] | — | 7,9% (10,0) | 269 |
| RF τ0,2 | 8664 | −42,98 | 6,5% | 2,5 [2–6,5] | — | 14,8% (11,5) | 378 |
| RF τ0,3 | 4854 | −23,64 | 8,8% | 5,0 [3–7] | — | 23,6% (15,0) | 334 |
| RF τ0,5 | 2050 | −9,41 | 6,5% | 5,0 [3,25–7,5] | — | 20,4% (15,5) | 111 |

- GB/LR juga negatif di semua tau (GB −10,42…−48,96; LR −32,10…−83,67) — pola sama.
- RF τ0,05 coverage 0 meski 158 alarm = **semantik alarm-transisi** (pred persisten 1
  jarang bertransisi) — keterbatasan metrik (konsisten resep V8), bukan bukti "model
  tidak mendeteksi".
- konf = 10 mnt = **1 jendela** untuk persistence/rule → konfirmasi menyusul blok
  persis seperti klaim EVAL_A ("delay konfirmasi 0–1 jendela").

### 2.2 `ssi` — B4 (status) + B3

Blok: 137 run, **hanya 40 berkelanjutan ≥5 mnt** (median run 2 mnt — 97 run pendek;
kelas ini memang didominasi event singkat → B4 hanya berlaku pada 40 blok).

| Engine | FP | B3 vs rule=26 | cov L10 | margin med [IQR] | konf med | catatan |
|---|---|---|---|---|---|---|
| rule | 26 | 0,00 | 5,0% | 5,5 [3,25–7,75] | 7 | nodata 22.385/35.906 baris (EVAL_A) |
| hybrid | **7** | **+0,731** | 0,0% | — | 10 | hanya 9 alarm; recall ≤0,03 |
| persistence | 267 | −9,27 | 7,5% | 4,0 [3–5,5] | 10 | |
| RF τ0,05 | 12708 | −487,77 | **27,5%** | 5,0 [3–6] | — | 1.081 alarm |
| RF τ0,1 | 4527 | −173,11 | 12,5% | 4,0 [4–7] | — | |
| RF τ0,2 | 658 | −24,31 | 10,0% | 5,5 [3,5–7] | — | |
| RF τ0,3 | 100 | −2,85 | 2,5% | 1,0 [1–1] | — | |
| RF τ0,5 | **4** | **+0,846** | 0,0% | — | — | TP 0 (EVAL_A) |

### 2.3 `shk` — B4 (status) + B3

Blok: 199 run, **164 berkelanjutan ≥5 mnt** (median 9 mnt, maks 114).

| Engine | FP | B3 vs rule=121 | cov L10 | margin med [IQR] | cov L30 (med) |
|---|---|---|---|---|---|
| rule (status-quo) | 121 | 0,00 | 13,4% | 4,5 [3–7] | 27,4% (11,0) |
| hybrid | 121 | 0,00 | 13,4% | 4,5 [3–7] | 27,4% (11,0) |
| persistence | 1056 | −7,73 | 11,0% | 5,0 [3–7] | 26,2% (13,0) |
| RF τ0,05 | 25837 | −212,53 | 25,0% | 4,0 [2–6] | 42,1% (8,0) |
| RF τ0,1 | 8455 | −68,88 | 13,4% | 4,5 [3–7] | 25,6% (9,0) |
| RF τ0,2 | 1107 | −8,15 | 3,0% | 9,0 [7–10] | 6,7% (11,0) |
| RF τ0,3 | 342 | −1,83 | 1,2% | 7,0 [6–8] | 2,4% (14,0) |
| RF τ0,5 | **39** | **+0,678** | **0,6% (1 blok)** | 4,0 [4–4] | 0,6% (4,0) |

### 2.4 `stuck` — K-i (status, B4) + K-ii (onset, B1/B2)

**K-i:** dataset = fold (F-14, F-9_A); 89 run → **76 berkelanjutan ≥5 mnt**.

| Engine | FP | B3 vs rule=49 | cov L10 | margin med [IQR] | konf med |
|---|---|---|---|---|---|
| rule | 49 | 0,00 | 11,8% | 5,0 [4–6] | 10 |
| hybrid | 49 | 0,00 | 11,8% | 5,0 [4–6] | 10 |
| persistence | 436 | −7,90 | 7,9% | 5,5 [4,25–7,5] | 10 |
| E1 (2-dari-3) | 160 | −2,27 | 2,6% | 5,0 [3–7] | **58,5** |
| hybrid E1∧pers | **41** | **+0,163** | — | — | — |

**K-ii (H=10, anchor kelas 2,67–7,37 mnt):**

| Engine | B1 (rentang antar-fold) | TLead med (rentang) | B3 vs E1=422 | Band/anchor |
|---|---|---|---|---|
| RF τ0,05 | **0,51–1,00** | **10–11,5 mnt** (IQR atas s/d 28–33) | −77,05 (FP 32.938) | kategori 10–30 mnt; ≥ anchor, tapi beban 77× |
| RF τ0,1 | 0,36–1,00 | 8–11,5 | −54,38 | 10–30 mnt |
| RF τ0,2 | 0–1,00 | 7–10 | −28,40 | <10–10 mnt |
| RF τ0,3 | 0–0,68 | 5–10 | −4,95 | <10 mnt |
| RF τ0,5 | 0–0,045 | 2–159 (outlier) | **+0,604** (FP 167) | arah benar beban, B1 kuantitas kurang |
| RF q95-train | 0–1,00 (median 0,83) | 10–11,5 | −12,77 (FP 5.810) | FAR fold 0–903 (tidak stabil) |
| E2 q95 | 0–0,181 | 2,5–8 (IQR 1,75–10) | −0,924 | TLead DI anchor; CI memuat prev 4/4 (EVAL_A) |
| E1 rule | 0–0,066 | 1–5 | 0,00 (baseline) | < anchor |
| persistence-EVENT | 0–0,115 | 4,5–8,5 (**med fold-median 7,0**) | **+0,974** (FP 11) | DI anchor — arah benar, B1 <50% |
| persistence-HORIZON | 0,93–0,97 | 1–3 | +1,00 (FP 0) | **HINDSIGHT** (label horizon kontigu) — batas-atas, tidak deployable |

- FP window utk B3 dihitung pada grid 1 menit (satuan sama semua engine kelas ini).
- LR: B1 0,76–1,00 di semua tau TAPI FP 28.461–52.272 (B3 −66…−123) — mengonfirmasi
  pertukaran recall↔beban, bukan keunggulan (konsisten EVAL_A).

### 2.5 `hyd` — K-i (status, B4) + K-ii (onset)

**K-i:** 465 run → **277 berkelanjutan ≥5 mnt**.

| Engine | FP | B3 vs rule=2091 | cov L10 | margin med [IQR] | konf med |
|---|---|---|---|---|---|
| rule \|z\| (tautologi=status-quo) | 2091 | 0,00 | 20,6% | 3,0 [2–6] | **4** |
| persistence | 1941 | +0,072 | 10,5% | **7,0 [4–9]** | 10 |
| hybrid | **927** | **+0,557** | 13,0% | 4,5 [3–8] | 10 |

- Deteksi-transisi (JSON E_STAT, 9 fold): **delay median 0–3,5 mnt**, terdeteksi ≤H10
  **31,6–65,4%** (median 57,6%) — konfirmasi/transisi, bukan peringatan jauh.
- FP persistence cross-tim: E_STAT 1941 == E_RULE 1941 ✓ (V5 pendukung).

**K-ii:** lihat tabel ringkas — varian fisher 0/3 onset (TLead nol), rule z-pit
TLead=0 (10/10) + beban 1.348 mnt-episode, RF = referensi V8 (B1 66,7%, TLead 7 mnt,
3 onset underpowered). B3 tidak terdefinisi (pembagi 0).

### 2.6 `bit_wear` — K-1 + K-2

B3/B4 keduanya **belum terukur** (alasan di tabel ringkas: field TP/FP tidak dihitung
E_RULE; dataset USROP di luar pipeline D1; pra-reg K-2 belum terbit). Yang tetap
tercatat dari EVAL_A (bukan klaim B): persistence AUPRC mean 0,670 vs canary 0,389,
ΔB 5/5 scorable → kemampuan ranking.

### 2.7 `tool_wear` — K-i (B2 + B3) + K-ii

| Titik operasi | TLead | FP (R01, alat baru) | B3 vs rule 3-RMS | Deteksi R02 |
|---|---|---|---|---|
| change-point (permutasi) | 35 dtk med (27–39) | — (precision run 0,50) | — | 8/8 signifikan |
| kalibrasi 5/27 mentah | 59 dtk med (48–60) | 41–58/mnt | **0,00–0,25** | 4/4 |
| FAR-terkalibrasi target 1,0/mnt | 20–36 dtk | 1–3/alat | **+0,909…+0,976** | 4/4 |
| FAR-terkalibrasi target 0,2/mnt | 20–36 dtk | 1–3/alat | +0,909…+0,976 | 4/4 |

- B1-analog (deteksi sebelum akhir run R02) kalibrasi = **100% (4/4 alat)**; part C 4/4.
- K-ii V9: belum (tanpa engine alarm); RF V8 TLead 47,5 dtk (35–59) = referensi.

---

## 3. TABEL JOINT B3 × B4 (kelas status) — inti nilai pemeliharaan

Satuan: FP = jendela 1 menit; B3 vs rule status-quo; B4 = margin median (menit) pada
coverage blok ≥5 mnt (L=10). Titik dengan **B3 ≥ 0** = tidak menambah pemeriksaan.

| Kelas | Engine@titik | FP | **B3** | **B4 cov / margin** | Bacaan |
|---|---|---|---|---|---|
| vib | rule / hybrid | 197 | 0,00 | 26,4% / 5,0 | peringatan dini terbatas tanpa biaya tambahan |
| vib | RF (semua tau) | 2050–15321 | −9,4…−76,8 | 0–8,8% / 2,5–7 | menambah beban TANPA cakupan naik |
| ssi | hybrid | 7 | **+0,73** | 0% / — | hemat pemeriksaan, peringatan dini nol |
| ssi | RF τ0,05 | 12708 | −487,8 | **27,5% / 5,0** | cakupan tertinggi, beban ekstrem |
| ssi | RF τ0,5 | 4 | **+0,85** | 0% / — | titik hemat tanpa deteksi (TP 0) |
| shk | rule / hybrid | 121 | 0,00 | 13,4% / 4,5 | lapisan dasar berbiaya-status-quo |
| shk | RF τ0,5 | 39 | **+0,68** | 0,6% / 4,0 | hemat, menangkap 1/164 blok |
| stuck K-i | hybrid E1∧pers | 41 | **+0,16** | (rule: 11,8% / 5,0) | penghematan kecil di titik E1 |
| hyd K-i | hybrid | 927 | **+0,56** | 13,0% / 4,5 | **hemat 56% + deteksi P/R ≥0,52** |
| hyd K-i | persistence | 1941 | +0,07 | 10,5% / 7,0 | margin terbesar di kelas ini |

**Temuan terpusat (bukan vonis):** pada titik operasi yang diuji, **cakupan peringatan
dini yang tinggi selalu berpasangan dengan beban inspeksi yang jauh lebih besar dari
status-quo** (terburuk: ssi RF τ0,05 −487,8; shk RF τ0,05 −212,5; stuck K-ii RF τ0,05
−77,1), sedangkan **titik ber-B3≥0 memberi cakupan 0–13,4%** pada kelas status.
Nilai pemeliharaan yang terukur dan berbeban-wajar ada di tiga tempat: **hyd K-i
hybrid (B3 +0,56 dengan deteksi terjaga)**, **tool_wear FAR-terkalibrasi (B3
+0,91…+0,98, deteksi 4/4, lead 20–36 dtk)**, dan **ssi hybrid (B3 +0,73 sebagai opsi
hemat-awas, recall tipis)**. Untuk onset stuck, TLead kandidat layak berada di/dekat
anchor 2,67–7,37 mnt (persistence-EVENT median 7,0; E2 2,5–8) — **arah benar, tapi
kuantitas peringatan (B1) belum** pada beban yang bisa ditoleransi.

---

## 4. VERIFIKASI (verification-mandatory)

Primer: `scratch/v9_eval_b/v9_eval_b_RESULTS.json` · log: `v9_eval_b_VERIFY.txt`,
`v9_eval_b_SUMMARY.txt`.

| Cek | Hasil | Cara |
|---|---|---|
| V1 FP B3 re-sum dari JSON sumber E_RULE | **17/17 identik** | re-loop fold mentah, banding dgn tersimpan |
| V1b FP E1 onset re-sum | **422 == 422** | idem (RULE02) |
| V2 B1 stuck RF τ0,05 ekstrak ulang dari E_ML | **identik** ([0,507; 1; 1; 1]) | beda jalur kode |
| V3 B4(vib persistence) recompute implementasi BERBEDA | **27 margin == 27; 216 blok == 216** | index-based per sumur, spesifikasi sama |
| V4 identitas retrain RF (gate EB-5) | **AUPRC 22/22 (selisih 0,00e+00); TP/FP per tau 110/110** | ulang latih seed 42, fold E_ML |
| V5 FP prediksi ulang (persistence/rule/hybrid/E1) vs fold E_RULE | **16/16 identik** | per kelas per metode |
| V6 formula B3 self-consistency | **62/62** | recompute `1−FP/FP_rule` dari FP tersimpan |

- **Kegagalan yang ditemukan & diperbaiki (dilaporkan):** percobaan pertama V3 gagal
  (29 vs 27) karena implementasi alternatif tidak menerapkan spesifikasi pemutusan blok
  pada gap >2 menit; setelah spesifikasi diterapkan konsisten → identik. Akar masalah
  = spesifikasi B4 yang belum dijabarkan di implementasi alternatif, bukan angka
  skrip 02 yang salah.
- **Cross-tim:** hyd K-i FP persistence E_STAT 1941 == E_RULE 1941 (V5 turunan).
- **Ketiadaan error ≠ logika benar:** selain recompute, keabsahan logika B4 dibuktikan
  lewat (i) identitas skor RF dgn run E_ML (V4), (ii) reproduksi FP tiga komponen dgn
  E_RULE (V5), (iii) implementasi independen (V3), dan (iv) tes pembeda
  konfirmasi-vs-peringatan (konf persistence = 10 mnt ≠ margin 5 mnt → dua metrik
  memang mengukur hal berbeda).

---

## 5. BELUM TERUKUR / BELUM DIVERIFIKASI (verification-mandatory #3)

- **Belum terukur (bukan gagal):** B3/B4 bit_wear K-1; B1–B4 bit_wear K-2 (pra-reg
  belum terbit); B3/B4 tool_wear K-ii versi V9 (RF tidak dijalankan); B3 hyd K-ii
  (pembagi nol by construction); B4 RF utk GB/LR (hanya RF head utama yang diukur);
  validasi kontrol-positif `labels_curated_v2` (884 event) — **sinkronisasi zona-waktu
  ts_bin↔kurasi masih tripwire terbuka PM1 §5.1** → tidak dilakukan di V9; angka V8
  (kontrol-positif stuck 0/10, RF hyd K-ii, RF tool_wear K-ii) = referensi (EA-7).
- **Belum dicek evaluator ini:** kalibrasi ambang B4 per well secara prospektif
  (menyusul EVAL_C); B4 dengan definisi blok berbeda (k≥10 mnt / tanpa sustain) —
  hanya k≥5 (pra-reg V8) + sensitivitas L yang dijalankan; koreksi multipelitas (tidak
  ada klaim signifikansi tunggal di dokumen ini); semantik label lintas-well
  (prasyarat pra-reg Fase 0) — dampaknya ke B4 tidak diuji di sini.
- **Keterbatasan bukti:** stuck K-i & bit_wear cakupan fold kecil; hyd K-ii 1 split,
  3 onset (underpowered); tool_wear n run = 8 (underpowered); ssi 97/137 run di luar
  definisi blok berkelanjutan; alarm = SEMANTIK TRANSISI (pred persisten-positif tidak
  menyala ulang) → coverage RF τ0,05 vib 0 dibaca bersama jumlah alarm, bukan sendirian.

---

## 6. MASUKAN EVAL_C — tingkat pemakaian per engine (bukan vonis final)

| Engine | Nilai B yang terukur | Syarat B yang tersisa | Arah tingkat pemakaian (masukan, bukan keputusan) |
|---|---|---|---|
| vib | konfirmasi + peringatan dini terbatas (26,4% blok, margin 5 mnt, B3=0) | cakupan & beban RF; parse VIBLAT F-4/F-10/F-15 | tren + konfirmasi; RF belum menambah nilai pemeliharaan |
| ssi | hybrid hemat 73% (recall tipis); RF cakupan 27,5% dgn beban 488× | titik operasi dgn B3≥0 & coverage>0; S-E1 re-run 11 fold | pemantauan tren + hemat-awas |
| shk | rule B3=0 cakupan 13,4%; RF τ0,5 B3+0,68 coverage 0,6% | titik joint B3≥0 dgn coverage memadai; fold eksternal | lapisan dasar rule well-terkalibrasi |
| stuck K-i | konfirmasi presisi 0,92–0,97; hybrid-E1 +16% hemat | fold tambahan (F-10/F-12) | konfirmasi status |
| stuck K-ii | TLead di anchor dgn B1<50% (B3≥0); B1≥50% hanya dgn beban 77× | kalibrasi titik operasi beban-terkendali; kontrol-positif tersinkron | triage beranotasi; alarm otomatis = belum (B1 & FAR) |
| hyd K-i | **hybrid +56% hemat dgn P/R ≥0,52; margin 4,5 mnt (13% blok)** | FAR ≤6 (sisa EVAL_A/C) | tren + konfirmasi hemat-awas |
| hyd K-ii | tidak ada peringatan dini terukur (V9); beban rule 1.348 mnt | ulang RF V8; parse GAINLOSSTOT F-1C/F-11; sinkron kurasi | indikasi dini beranotasi ketidakpastian |
| bit_wear K-1/K-2 | belum terukur (K-2 = pra-reg) | run ulang TP/FP; pra-reg K-2 | ranking saja (dari A); B belum bisa dinilai |
| tool_wear K-i | **lead 20–36 dtk + hemat 91–98% vs rule 3-RMS (deteksi 4/4)** | spesifisitas keausan (precision run 0,50); n=8 | gating inspeksi bengkel (skala detik) |
| tool_wear K-ii | V9 belum (V8 ref lead 47,5 dtk) | re-run RF V9 dgn FP/TLead | ranking lintas-alat (V8 ref) |

Sumber: `scratch/v9_eval_b/v9_eval_b_RESULTS.json` (primer),
`v9_eval_b_SUMMARY.txt`, `v9_eval_b_VERIFY.txt`.
Dihitung: 2026-10-12, skrip EVAL_B (re-sum 17/17, identitas RF 22/22 + 110/110,
recompute B4 independen 27=27, sequ 4/4).
