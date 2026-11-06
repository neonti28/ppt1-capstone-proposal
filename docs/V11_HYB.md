# V11-E_HYB: Uji Rule / Persistence / Hibrida + Workflow Kedua Kandidat vs Kode E_RULE

Kartu: `t_2cd06fc3` (board capstone-v11-vs, 2026-10-15). Ruang kerja kartu:
`/home/neonti/.hermes/kanban/boards/capstone-v11-vs/workspaces/t_2cd06fc3`.
Dokumen ini penilaian paruh-atas: pengamatan per kandidat + lembar skor per sub-kriteria.
Pemetaan versi dan keputusan menang bukan milik kartu ini (protokol §2.6, §3).

**Riset pendahuluan: `scientific-critical-thinking`** - klaim dipisah OBSERVED (JSON/kode/eksekusi)
vs DITULIS KANDIDAT; klaim "rule ≡ label (sirkular)" diperiksa ulang lewat field
`identity_rule_window_vs_label` (mismatch 0 di 5/5 kelas); temuan diskrepansi kandidat 2
diuji dengan membaca ulang primer, bukan dengan membaca dokumen induk (§4.7); satu keberatan
"far belum terukur" pada kandidat 1 diuji terhadap JSON sebelum dinilai (§3.3).

**Riset pendahuluan: `verification-mandatory`** - seluruh angka di dokumen ini = hasil
recompute skrip `_hyb_recompute.py` terhadap `scratch/v9_e_rule/v9_e_RULE_01_status_results.json`
dan `v9_e_RULE_02_stuck_onset_results.json` (primer dijadikan `v11_hyb_primary_facts.json`);
 parity md/ipynb dihitung ulang dengan metode independen `_parity_recheck.py` (parse JSON ipynb
langsung); daftar BELUM dicek eksplisit di §7.

**Riset pendahuluan: `statistical-analysis`** - baseline dinilai relevan per jenis tugas;
fold UNDERPOWERED (positif < 30) dilabeli dan dikecualikan dari denominator "fold layak"
(ssi F-7/F-9); makro mean P/R dihitung hanya fold dengan nilai terdefinisi (presisi `None`
pada fold tanpa TP/FP dikecualikan, konsisten dengan tanda "–" di dokumen induk); plafon
lift 1/prev dilaporkan per kelas.

**Riset pendahuluan: `sequentialthinking`** (sequ-mcp, 4 pikiran, 4/4 sukses) - peta 5 tugas
kartu vs primer; kebenaran ambang per kelas termasuk koreksi angka 32,17405 terhadap angka
di badan kartu; rencana verifikasi per tugas; mekanisme pengaruh antar-komponen hibrida
sebagai kriteria penilaian sub-tugas 3.

---

## 1. Metode uji (semua klaim = eksekusi nyata)

Sumber primer yang dibaca/dijalankan:

| Primer | Isi | Cara diuji |
|---|---|---|
| `code/v9_e_RULE_01_status.py` | ambang rule, resep persistence, rumus E1, hibrida | grep literal (baris 49, 50, 180-181, 202-203, 301-303) |
| `code/v9_e_RULE_02_stuck_onset.py` | persistence horizon/event + E1 onset | dibaca via field JSON hasil |
| `scratch/v9_e_rule/v9_e_RULE_01_status_results.json` | 33 fold status + identity per kelas | recompute penuh `_hyb_recompute.py` |
| `scratch/v9_e_rule/v9_e_RULE_02_stuck_onset_results.json` | 4 fold onset stuck | recompute penuh (bagian `onset`) |
| `docs/V9_E_RULE_ENGINE.md` (414 baris) | dokumen induk E_RULE | dibaca penuh, dipakai silang-rujuk |
| `docs/V11_PROTOCOL.md` | rubrik 100 poin, aturan paket, aturan em-dash | dibaca bagian §2, §5, §6, §7 |
| kedua paket kandidat (.md + .ipynb) | objek penilaian | pembacaan penuh K1 (352 baris), ekstraksi + grep K2 (3.557 baris), parity ulang |

Skrip di workspace (dijalankan, hasil disimpan):
`_hyb_recompute.py` (angka rule/persistence/hibrida), `_parity_recheck.py` (parity
md/ipynb metode kedua), `_emdash711.py` (hitung U+2014 + pola kata), `_audit_emdash.py`
(konteks penuh em-dash + daftar cell code), digabung ke `v11_hyb_primary_facts.json`.

Nama file kandidat di dokumen ini ditulis lengkap supaya bisa dicek ulang:
- kandidat 1 = `docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.v3_arsip.md` + `....v3_arsip.ipynb`
- kandidat 2 = `docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md` + `....ipynb`

Catatan nomor baris: sitasi `md:NNNN` di bawah adalah nomor baris file `.md` asli
(telah diverifikasi ulang dengan grep langsung ke file).

---

## 2. Ringkas hasil per tugas (pengamatan per kandidat)

| # | Tugas kartu | kandidat 1 | kandidat 2 |
|---|---|---|---|
| 1 | Definisi rule per kelas + pemahaman strict-past | Tidak ada definisi rule per kelas (0/5); istilah VIBLAT/SHKRSK/32,17405/strict-past/2-dari-3 = 0 kemunculan; anti-bocor hanya dibahas umum untuk fitur | Lengkap 5/5 rumus, semua cocok literal dengan kode; strict-past dijelaskan benar (membaca bin t0 = membaca label) + bukti recompute identity 5/5 kelas |
| 2 | Persistence y(t-1) sbg baseline sekaligus engine status | Dua peran disebut kualitatif (baris 88, 112, 154) tanpa rumus/resep/angka | Rumus + resep D1 + subset valid_prev + tabel AUPRC per kelas (semua cocok JSON) + batas jujur |
| 3 | Workflow hibrida + mekanisme pengaruh + angka FP | Tidak ada; hibrida didefinisikan berbeda ("aturan + statistik + ML", baris 90/159; "rule + persistence + RF", baris 246); 0 angka FP | Workflow 4 langkah + mekanisme dua pemotong + semua angka cocok (26→7, 2.091→927, AUPRC 0,6024); 1 imprecision label (§4.7) |
| 4 | Baseline S9 + alasan baseline per tugas | Parsial: prinsip "baseline relevan per tugas" + komponen rule/persistence/canary; tanpa prevalence-random, canary-depth, dan angka per fold | Lengkap: 4 komponen S9 (persistence, canary-kedalaman, prevalence-random, rule ambang) + 5 alasan, beberapa diuji ulang dan cocok |
| 5 | md vs ipynb; kelengkapan relatif | md seluruhnya ada di ipynb (0 baris hilang); ipynb = md + catatan arsip + 12 cell VIS | Sama: 0 baris md hilang; 1 selisih teknis selipan baris yang teksnya identik; 12 cell VIS identik label dengan kandidat 1 |

---

## 3. kandidat 1 (`docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.v3_arsip.md` + `.ipynb`)

### 3.1 Tugas 1: definisi rule per kelas + strict-past

Pembacaan penuh seluruh 352 baris md + hitung pola pada md dan sel markdown ipynb
(keduanya identik jumlahnya): `VIBLAT` 0, `32,17405` 0, `32.17405` 0, `SHKRSK` 0,
`2-dari-3` 0, `strict-past` 0; token `E1` hanya muncul 2× sebagai nama dokumen
(`V6_E1_ML_DESIGN.md`, `V6_E1*_PREREG*`, md:322), bukan sebagai aturan 2-dari-3.

- Yang ada hanya contoh generik: "tekanan tidak normal, ambang torsi" (md:86) dan
  penyebutan SSI sebagai fitur turunan fisika "MSE, SSI, UCS" (md:136), bukan definisi
  aturan deteksi.
- Seluruh ambang primer TIDAK muncul: `VIBLAT ≥ 32,17405` (kode `v9_e_RULE_01_status.py:49`),
  `SSI >= 1` dgn min 10 sampel (baris 50, 202-203), `SHKRSK >= 1` dan `stuck_max >= 1`
  (baris 180-181), E1 2-dari-3 `z = 0,6745(x-median)/MAD` jendela 60 menit (baris 301-303).
- Pemahaman "membaca bin t0 = membaca label" TIDAK dibahas; anti-bocor yang ada hanya
  untuk fitur ("fitur selalu berstempel waktu lebih awal daripada peristiwa", md:141;
  md:182) dan tidak tersambung ke rule-display t0-1.
- Status: TIDAK TERSEDIA untuk diuji (bukan klaim keliru; memang tidak ada).

### 3.2 Tugas 2: persistence y(t-1) sbg baseline + engine status

Dua peran ADA secara kualitatif:

- md:88 "Persistence (status-quo) | Konfirmasi status + pembanding jujur | keadaan
  berlanjut dari kondisi sebelumnya" (peran ganda: engine status + pembanding).
- md:112 "Konfirmasi status otomatis ... berdasarkan aturan dan persistence, tanpa perlu
  pelatihan" (persistence sebagai engine status).
- md:154 "Pembanding status-quo | ... pada sebagian tugas persistence terbukti terbaik dan
  dicatat sebagai kemampuan" (kemampuan terbaik dicatat terbuka, sejalan primer).
- md:250-251: kelas anomali hidraulik "Statistik (median/MAD) + persistence", keausan bit
  "RF + persistence + canary" (komposisi kelas sesuai semangat primer).

Yang TIDAK ada: rumus `ŷ(t)=y(t−1)`, resep kolom `y_prev_*` jendela `[t0-10, t0)`,
subset `valid_prev`, tabel angka AUPRC persistence per kelas, anotasi hindsight untuk
persistence-horizon onset, dan batas FAR persistence.

### 3.3 Tugas 3: workflow hibrida + mekanisme pengaruh + angka pemangkasan FP

- Formula primer `h(t) = rule(t0−1) AND persistence(t)` TIDAK muncul: pola `rule(t0−1)`
  dan `persistence(t)` = 0 kemunculan di md dan ipynb; kata `hibrida` ada (5×) tetapi hanya
  sebagai nama kelompok metode, bukan rumus mesin.
- Hibrida kandidat 1 didefinisikan berbeda: "Mesin hibrida (aturan + statistik + ML) |
  Arsitektur per mesin | gabungan lapisan dasar + prediksi" (md:90 dan md:159), serta
  baris peta mesin: whirl = "Hibrida (rule + persistence + RF)" (md:246), stick-slip =
  "Hibrida (rule + RF)" (md:247). Ini usulan arsitektur, bukan penjelasan mesin hibrida
  E_RULE; komposisinya juga tidak sama dengan kontrak D-A3 (rule AND persistence, tanpa RF).
- Tidak ada langkah kerja berurutan, tidak ada mekanisme pengaruh antar-komponen.
- Seluruh angka pemangkasan FP TIDAK muncul: `26→7` 0, `73,1` 0, `2.091` 0, `927` 0,
  `55,7` 0, `0,6024` 0, `D-A3` 0.
- Satu klaim terkait yang bisa diuji: md:246-247 "Alarm otomatis (FAR belum terukur)".
  OBSERVED: JSON primer MEMILIKI FAR24 untuk rule/persistence/hibrida kelas ini
  (hyd di luar cakupan; vib: rule & hibrida FAR24 10,0-49,9 per 24 jam, persistence
  74,7-316,3). Bila "belum terukur" dimaksudkan untuk komponen RF, pernyataan itu benar
  dan konsisten dengan batas V9 §2.1; bila dibaca untuk seluruh mesin hibrida, ia bertabrakan
  dengan angka FAR yang sudah tercetak. Status: AMBIGU, dicatat sebagai kekaburan cakupan,
  bukan angka karangan (rubrik 2c memisahkan keduanya).

### 3.4 Tugas 4: baseline S9 + alasan baseline per tugas

- Prinsip ADA: "Baseline relevan per tugas | Satu baseline universal | Kecocokan baseline
  mengikuti tugas (rule, persistence, statistik, canary)" (md:204); lapisan A memakai
  "baseline relevan untuk tugas mesin itu (bukan satu baseline universal)" (md:188);
  tabel metrik "Baseline relevan per tugas" (md:218); pembanding wajib "Aturan if-then &
  canary" dan "Persistence (status-quo)" (md:153-154).
- Komponen S9 yang ADA: rule ambang (if-then), persistence, canary (generik).
- Komponen S9 yang TIDAK ADA: `prevalence-random` (0 kemunculan; pola `prevalen` juga 0),
  `canary-depth`/kedalaman (0 kemunculan), penamaan "S9" (0), angka baseline per fold
  (0), plafon lift 1/prev (tidak disebut), label fold UNDERPOWERED (tidak disebut).
- Alasan per tugas: ada pada level prinsip (jenis tugas beda, md:92; baseline cocok tugas,
  md:204) tetapi tanpa pemetaan tugas-ke-baseline dan tanpa bukti angka.

### 3.5 Tugas 5: paket md vs ipynb

Recompute independen (`_parity_recheck.py`, parse JSON ipynb langsung):

- Sel markdown ipynb: 25 markdown cell + 12 code cell.
- Baris md yang HILANG dari ipynb: **0** (seluruh isi md ada di ipynb; md ⊂ ipynb terbukti
  untuk semua 352 baris).
- Selisih ipynb-di-atas-md: 1 blok markdown "ARSIP VISUALISASI KAMPANYE LAMA (BUKAN BAGIAN
  NARASI PROPOSAL)" (9 baris, dinyatakan sendiri sebagai arsip) + 12 cell code VIS 0..VIS 11.
- Hitung kemunculan pola kunci di md vs sel markdown ipynb: identik untuk semua pola
  (dari `patterns_ipynb_md` = `patterns_md` di JSON primer).
- Kesimpulan: isi substantif sama; tidak ada angka/klaim yang hanya ada di satu format.

### 3.6 Struktur

- Outline 19 bab berhirarki jelas, tiap bab berlabel tujuan (§3.1 md baris 16-36).
- Penjelasan 7/11/27: 0 kemunculan pola `7/11/27`; kata `27` tidak muncul sama sekali.
- Em-dash (U+2014): 14 kemunculan di md, 14 di sel markdown ipynb (identik). Audit konteks
  penuh ke-14 kemunculan (`_audit_emdash.py`): ≥6 dipakai sebagai penghubung klausa,
  contoh (tanda [em-dash] = U+2014 apa adanya di dokumen kandidat): "Kegagalan BHA
  [em-dash] mencakup ..." (penjelas), "komponen [em-dash] menyebabkan non-productive time"
  (kausalitas, seharusnya "sehingga"), "(fraksi) [em-dash] 55 fitur" (penjelas),
  "benar [em-dash] apakah mesin berguna" (penjelas), "lengkap [em-dash] termasuk seluruh
  kampanye", "berturut-turut [em-dash] tercatat pada". Sisanya pola label ("Lapisan A
  [em-dash] ...", "Tingkat 1 [em-dash] ...") yang bukan penghubung klausa.
  ≥4 pelanggaran → sub-kriteria 4d = 0 (protokol §7.5).

---

## 4. kandidat 2 (`docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md` + `.ipynb`)

### 4.1 Tugas 1: definisi rule per kelas + strict-past

Tabel rumus di md:2477-2481, diuji satu per satu terhadap kode:

| Kelas | Klaim kandidat 2 (md:baris) | Primer (kode) | Status |
|---|---|---|---|
| vib | `status(t) = 1[VIBLAT_RT(t) ≥ 32,17405 ft/s²]`, basis t0−1 (2477) | `VIB_THRESH = 32.17405` (`v9_e_RULE_01_status.py:49`); doc induk §2.1 "VIBLAT≥32,17405" | COCOK |
| ssi | `SSI = (max-min)/(2·mean)`, alarm `SSI ≥ 1`, min 10 sampel, `crpm_mean>0` (2478) | `(mx-mn)/(2.0*me)` dgn `>= 1.0`, `SSI_MIN_SAMPLES=10`, `me>0` (baris 50, 201-203) | COCOK |
| shk | `1[SHKRSK_RT(t) ≥ 1]` (2479) | `colmap: "shk": ("shk_max", 1.0)` (baris 180-181) | COCOK |
| stuck_k1 | `stuck_max(t0−1) ≥ 1` + E1 `1[(z(TQA)>2)+(z(HKLD)>2)+(ROP-drop≥30%) ≥ 2]`, `z=0,6745(x-median)/MAD`, jendela 60 mnt (2480, 2583) | `colmap: "stuck": ("stuck_max", 1.0)` (181); fungsi E1 (301-303): z, MAD==0 → z=0, ROP-drop≥30%, jendela 60 menit | COCOK |
| hyd_ki | `\|z\|>2` atas `SPPA_mean` vs bin `TFLO_mean` (qcut-10, median/MAD per bin), `anom/obs ≥ 0,5`, `MIN_OBS=5` (2481) | komentar baris 169 "qcut(TFLO,10)+median/MAD per well = resep label V6-31"; `hyd_bin_anom` (210) | COCOK |

Catatan angka badan kartu: badan kartu E_HYB menulis ambang vib "32,174405". Pencarian
literal `32,174405`/`32.174405` di seluruh `docs/` dan `code/` = 0 temuan; kebenaran primer
= 32,17405 (kode + dokumen induk). Kandidat 2 menulis 32,17405 = cocok primer
(12 kemunculan `32,17405` + 1 `32.17405`, md dan ipynb identik).

Penjelasan strict-past (md:2489-2507), diuji tiap kalimat:

- "Label setiap kelas dibentuk dari jendela [t0, t0+10)" = konsisten resep D1/JSON.
- Cek identitas recompute: "mismatch = 0 di 5/5 kelas" dgn baris 23.922 / 35.906 /
  56.495 / 5.555 / 52.509. Recompute JSON: `identity.n_mismatch = 0` dan `n_checked`
  persis kelima angka itu (kandidat 2 menyebut angka 23.922 memakai titik pemisah ribuan,
  nilai sama persis). COCOK.
- "membaca bin t0 (bagian dari jendela label) = membaca label sendiri (bocor)" = pemahaman
  yang benar, identik dengan §2.0 dokumen induk.
- "pembanding operasional sah = rule pada menit t0−1 ... invariant S5 `feat_ts_max < lab_ts`"
  = benar dan konsisten `meta.rule_time_basis`.
- "FP rule t0−1 NYATA dan besar (vib 197 … hyd 2.091)" = cocok recompute (197, 26, 121,
  49, 2.091, lihat §5).
- E1 "MAD=0 → z=0 (konservatif)" = cocok kode (baris 323, 330).

### 4.2 Tugas 2: persistence y(t-1) sbg baseline + engine status

Rumus dan resep (md:2513-2514): `ŷ(t)=y(t−1)` grid 60 detik, kolom `y_prev_*`, jendela
`[t0−10, t0)`, subset `valid_prev=1` + versi semua-baris. Cocok `meta.persistence_recipe`
JSON ("D1 y_prev_* (jendela [t0-10,t0)); subset valid_prev dicetak terpisah").

Dua peran dinyatakan terpisah (md:2516-2521): (1) baseline naive S9 dengan lift
`AUPRC/prevalence` dan plafon `1/prev`; (2) engine status terbaik = kemampuan, bukan aib.
Tabel AUPRC rata-rata (md:2523-2529) diuji seluruh selnya terhadap `aggregate` JSON:

| Kelas | persistence | rule(t0−1) | canary | random | pemenang fold (klaim) | Recompute JSON |
|---|---|---|---|---|---|---|
| vib | 0,6299 | 0,5625 | 0,4141 | 0,3029 | persistence 3/4 | 0,6299/0,5625/0,4141/0,3029; rule>pers 1 fold → pers 3 menang. COCOK |
| ssi | 0,0410 | 0,0226 | 0,0401 | 0,0209 | persistence 5/9 | 0,0410/0,0226/0,0401/0,0209; rule>pers 2, seri 2 → pers 5. COCOK |
| shk | 0,0913 | 0,0836 | 0,0460 | 0,0371 | seri 4/9-4/9 | 0,0913/0,0836/0,0460/0,0371; pers 4, rule 4, seri 1. COCOK |
| stuck_k1 | 0,6516 | 0,6682 | 0,5893 | 0,3934 | rule 1/2 | 0,6516/0,6682/0,5893/0,3934; pers menang fold 0, rule menang fold 1. COCOK |
| hyd_ki | 0,5555 | 0,5751 | 0,1980 | 0,1502 | rule 7/9 | 0,5555/0,5751/0,1980/0,1502; rule>pers 7 fold. COCOK |

Klaim pendukung lain yang diuji: "hyd persistence > canary & > random 9/9 fold"
(recompute: 9 dan 9, COCOK); "ssi persistence ≥ random 7/9, > canary hanya 2/9"
(recompute: 7 dan 2, COCOK); "vib persistence > canary 4/4 & > random 4/4" (recompute: 4
dan 4, COCOK); bit_wear "identik digit E1d V6 (F-14 0,6792052825924018)" cocok dokumen
induk §4.1; tool_wear persistence N/A + diagnostik 0,9915-0,9929 cocok §4.2; persistence
ke-2 yang diklaim di hyd: angka pendukungnya benar, yaitu persistence hanya kalah tipis
dari rule (0,5751 vs 0,5555); peringkat "terkuat kedua" dianotasi ambigu di §4.7 D3;
batas recall/FAR persistence disebut (md:2547-2549); anotasi HINDSIGHT persistence-horizon ada (md:2445).

### 4.3 Tugas 3: workflow hibrida + mekanisme pengaruh + angka FP

- Rumus: `h(t) = rule(t0−1) AND persistence(t)` (md:2558) dengan anotasi dua pemotong
  "status-kini" dan "status-kemarin" (md:2559-2563). COCOK dengan kontrak D-A3 dokumen induk.
- Workflow langkah-demi-langkah: diagram 4 langkah (md:2572-2608): (1) rule t0−1 per kelas
  dgn lima ambang, (2) persistence `y_prev_*` subset valid_prev, (3) gerbang AND, (4) metrik
  per fold (AUPRC, lift, plafon 1/prev, P/R/TP/FP/FN/TN, `FAR_24h = FP/(n_neg/60)·24`),
  menuju JSON primer. Konvensi FAR cocok `meta.far_convention` JSON. ADA dan lengkap.
- Mekanisme pengaruh antar-komponen (md:2610-2649): rule = pemotong status-kini (risiko
  transien sesaat → FP), persistence = pemotong status-kemarin (menuntut kontinuitas),
  AND hanya meloloskan alarm lolos dua saringan → alarm rule yang terisolasi dibuang;
  ditutup dengan tabel trade-off recall per kelas (vib/shk/stuck +0,0000; ssi −0,0091;
  hyd −0,0960). MEKANISME + interaksi dijelaskan berbukti.
- Degenerasi dijelaskan (md:2651-2659): di vib/shk/stuck_k1 hibrida ≡ rule karena
  rule(t0−1) himpunan-bagian persistence. Recompute: `hyb_eq_rule_auprc_allfolds = true`
  untuk ketiga kelas dan FP per fold identik (vib 30/65/65/37; shk 15/8/48/3/22/14/7/2/2;
  stuck 16/33). COCOK.

Angka pemangkasan FP (semua direcompute dari JSON):

| Klaim kandidat 2 (md:baris) | Recompute JSON | Status |
|---|---|---|
| ssi FP 26 → 7, −73,1% (2461, 2626, 2629, 2730) | sum rule 26, sum hybrid 7, reduksi 73,077% → 73,1% | COCOK |
| ssi "tak memburuk di 7/7 fold (memotong 6/7)" (560, 817) | fold layak (tanpa F-7/F-9 underpowered) = 7; memotong 6; seri (tie) 1; fold memburuk 0 | COCOK |
| hyd FP 2.091 → 927, −55,7%, 9/9 well (2462, 2627, 2632, 2774) | sum 2.091 → 927, reduksi 55,667% → 55,7%; 9/9 fold memotong; tiap fold = 1 well berbeda | COCOK |
| hyd AUPRC 0,6024 > rule 0,5751 > persistence 0,5555 (2462, 2774) | aggregate: hybrid 0,6024; rule 0,5751; persistence 0,5555 | COCOK |
| hyd "mengalahkan persistence 8/9 fold (F-9 kalah −0,017)" (2634, 2775) | hybrid>pers 8 fold, kalah 1 fold | COCOK |
| hyd precision 0,709 → 0,833; recall 0,7515 → 0,6555 (2627, 2632) | mean P 0,7094 → 0,8334; mean R 0,7515 → 0,6555 | COCOK |
| ssi P 0,2435 → 0,1333; R 0,0105 → 0,0014; AUPRC 0,0226 → 0,0206 (2626) | mean P 0,2435 → 0,1333; mean R 0,0105 → 0,0014; AUPRC mean 0,0226 → 0,0206 | COCOK |
| ssi F-10 FAR24 0,62 → 0,21 (2631) | 0,6196 → 0,2065 | COCOK |
| FP rule lintas fold: vib 197, ssi 26, shk 121, stuck 49, hyd 2.091 (2487, 2487-2488) | 197 / 26 / 121 / 49 / 2.091 | COCOK |
| recall delta: vib/shk/stuck +0,0000; ssi −0,0091; hyd −0,0960 (2639-2645) | mean R: identik utk tiga kelas degenerasi; ssi 0,0105−0,0014 = 0,0091; hyd 0,7515−0,6555 = 0,0960 | COCOK |
| FAR hybrid hyd 14,6-58,4 >6 di 9/9 (633) | FAR24 hybrid per fold: min 14,6, max 58,4; seluruh 9 fold >6 | COCOK |
| hibrida E1 stuck: F-14 FP 125→12, lift E1 0,99 (2663-2665, 2754) | hybrid_E1_and_persistence FP F-14 = 12; E1 FP 125; lift 0,9908 | COCOK |
| tabel 5.4: hybrid-E1 F-9_A FP 29; total E1 FP 160 (2755, 2758) | hybrid_E1 FP F-9_A = 29; E1 FP 125+35 = 160 | COCOK |

Konsistensi md/ipynb untuk seluruh pola angka di atas: jumlah kemunculan identik antara
md dan sel markdown ipynb (semua pola: `26→7` 9 dan 9; `73,1` 9 dan 9; `2.091` 10 dan 10;
`927` 15 dan 15; `55,7` 11 dan 11; `VIBLAT` 34 dan 34; `strict-past` 13 dan 13; dst.).

### 4.4 Tugas 4: baseline S9 + alasan baseline per tugas

Definisi S9 (md:2677-2680): persistence, canary-kedalaman, prevalence-random, rule ambang,
dihitung per tugas pada fold identik; konvensi seed 42, FAR V8, AUPRC
`average_precision_score`, fold dari `lowo_<engine>.json`. Cocok `meta` JSON + dokumen induk §1.

Lima alasan tidak ada baseline universal (md:2682-2696), diuji:

1. beda tugas → beda baseline, persistence-event onset ≈ prevalence sementara
   persistence-horizon hindsight: cocok JSON onset (persistence-event AUPRC 0,1860 / 0,0066 /
   0,0333 / 0,2244 vs prev 0,1831 / 0,0041 / 0,0192 / 0,2244; meta E0a caveat ada).
2. beda prevalensi → beda plafon `1/prev`: cocok field `plafon_1_over_prev` per fold.
3. kelas langka → canary bisa lebih relevan (ssi persistence > canary hanya 2/9): recompute 2/9. COCOK.
4. prevalence-random = lantai statistik `default_rng(42)`: cocok `meta.prevalence_random`.
5. rule ambang = sistem hari-ini: konsisten peran rule-display di JSON.

### 4.5 Tugas 5: paket md vs ipynb

- Sel markdown ipynb: 209 markdown cell + 12 code cell.
- Baris md HILANG dari ipynb: **0** (seluruh isi md ada di ipynb).
- Selisih: (i) blok arsip visualisasi 9 baris yang juga ada di kandidat 1 (deklarasi diri
  "bukan bagian narasi proposal"); (ii) satu paragraf terpecah dua baris di md menjadi satu
  baris di ipynb (teks identik, terbukti dari kedua baris md yang sama-sama ditemukan di ipynb).
- cell code VIS 0..VIS 11 identik labelnya dengan kandidat 1 (arsip visualisasi lama).
- Tidak ada angka/klaim/tabel yang hanya ada di satu format (semua pola angka identik hitungannya).

### 4.6 Struktur

- Bab E_RULE berpola tetap: ringkas dosen (§0) → 5 sub-tugas kartu (§1-§5) → ringkas
  7/11/27 dari sudut rule/hibrida (§6) → verifikasi & batas (§7).
- 7/11/27: pola `7/11/27` muncul 16 kali di md dan 16 kali di sel markdown ipynb;
  §6 menjelaskan arti ketiganya dan hubungannya dengan peran rule/persistence/hibrida
  (7 kelas, 11 sub-tugas klaim `3×1+4×2`, 27 head registry dengan 3 head non-ML per kelas).
- Em-dash (U+2014): **0** di md dan **0** di sel markdown ipynb → sub-kriteria 4d = 3.

### 4.7 Ledger diskrepansi kandidat 2 (dihitung jujur)

| # | Temuan | Bukti primer | Status |
|---|---|---|---|
| D1 | md:2629 dan md:2730 menulis "6/7 fold ber-FP" | fold dengan FP rule > 0 = 6 (bukan 7); fold layak non-underpowered = 7; keduanya memotong 6, tie 1 (F-14, FP 0→0), memburuk 0 | IMPRECISION LABEL: angka 6, 7, dan fakta tie semuanya benar; sebutan "ber-FP" untuk denominator 7 keliru (canonical EVAL_C: "hybrid ≤ rule di 7/7 fold layak"; kandidat 2 sendiri mencatat koreksi ini di md:817/835) |
| D2 | md:2528 pemenang stuck_k1 "rule 1/2 (seri 1/2)" | fold: persistence menang di F-14, rule menang di F-9_A (0 fold seri); AUPRC mean rule 0,6682 > persistence 0,6516 | AMBIGU BUKAN ANGKA KELIRU: terbaca benar sebagai "kedudukan head-to-head 1-1"; terbaca keliru bila "seri" diartikan jumlah fold seri |
| D3 | md:2535 "persistence = engine status non-ML terkuat kedua ... (rule sedikit lebih baik; hibrida terbaik)" | urutan agregat: hibrida 0,6024 > rule 0,5751 > persistence 0,5555 | AMBIGU BUKAN ANGKA KELIRU: benar bila "kedua" diartikan peringkat persistence di antara pembanding tunggal setelah rule; rancu bila diartikan urutan tiga posisi |

Tidak ditemukan angka karangan pada kandidat 2 dalam cakupan tugas 1-5: puluhan sel angka
pada bab E_RULE dan ringkasan terkait (tabel §4.1-§4.4 di atas) semuanya berstatus COCOK
terhadap JSON primer.

---

## 5. Fakta primer recompute (bukti mentah ringkas)

Sumber: `v11_hyb_primary_facts.json` (workspace kartu), dihasilkan `_hyb_recompute.py`
dari `scratch/v9_e_rule/v9_e_RULE_01_status_results.json` + `..._02_stuck_onset_results.json`.

| Kelas | FP rule | FP hibrida | Reduksi | Fold motong / tie / buruk | AUPRC pers / rule / hyb / can / rand |
|---|---|---|---|---|---|
| vib | 197 | 197 | 0% | 0 / 4 / 0 | 0,6299 / 0,5625 / 0,5625 / 0,4141 / 0,3029 |
| ssi | 26 | 7 | 73,077% | 6 / 3 / 0 (2 fold underpowered: F-7, F-9; 7 fold layak: 6 motong, 1 tie) | 0,0410 / 0,0226 / 0,0206 / 0,0401 / 0,0209 |
| shk | 121 | 121 | 0% | 0 / 9 / 0 | 0,0913 / 0,0836 / 0,0836 / 0,0460 / 0,0371 |
| stuck_k1 | 49 | 49 | 0% | 0 / 2 / 0 | 0,6516 / 0,6682 / 0,6682 / 0,5893 / 0,3934 |
| hyd_ki | 2.091 | 927 | 55,667% | 9 / 0 / 0 | 0,5555 / 0,5751 / 0,6024 / 0,1980 / 0,1502 |

- Identity recompute rule-jendela-label vs y: mismatch 0 di 5/5 kelas
  (n_checked 23.922 / 35.906 / 56.495 / 5.555 / 52.509).
- E1 stuck: FP 125 (F-14) + 35 (F-9_A) = 160; AUPRC 0,1337 vs prev 0,1350 (lift 0,9908) di F-14.
- Onset stuck (4 fold): persistence-horizon AUPRC 0,8265-0,9016, B1 0,9298-0,9670,
  meta E0a "hindsight ... bukan detektor deployable"; persistence-event ≈ prev per fold.
- FAR24 hybrid hyd: min 14,6, max 58,4; hybrid ssi: 0,0-3,7; vib rule/hybrid: 10,0-49,9.

---

## 6. Skor kartu ini (rubrik PM-0, cakupan tugas 1-5)

Disajikan per kandidat secara terpisah; perbandingan dan keputusan menang = PM-FINAL
(protokol §2.6, §3). Sub-kriteria dinilai sejauh terlihat dari cakupan tugas kartu ini;
sub-kriteria yang bergantung pada seluruh 30 angka checklist dinilai provisional karena
penelusuran penuh milik AUD-CLAIM.

### kandidat 1 (`...v3_arsip.md` + `.v3_arsip.ipynb`)

| Kriteria | Sub | Skor | Dasar |
|---|---|---|---|
| (1) Kedalaman teknis /30 | 1a | 2/10 | 0 rumus rule/persistence/hibrida dalam cakupan; yang ada contoh ambang generik (md:86) |
| | 1b | 4/7 | anti-sirkular + label 7 kelas ada (md:135-137), tetapi konstruksi label jendela/onset dan identity check tidak ada |
| | 1c | 0/7 | workflow hibrida tidak ada; komposisi hibrida berbeda konsep (md:90, 246) |
| | 1d | 3/6 | klaim kualitatif menaut sumber [A-x], tetapi klaim dalam cakupan tugas 1-4 tidak berangka/bukti primer |
| | **jumlah** | **9/30** | |
| (2) Akurasi /30 | 2a | 0/18 | butir checklist dalam cakupan (13, 14, 23, 24, 30) tidak muncul di dokumen = tidak cocok per rubrik |
| | 2b | 4/6 | klaim kualitatif per-kelas benar vs primer (hyd median/MAD+persistence md:250; bit RF+persistence+canary md:251; persistence terbukti terbaik dicatat md:154); "FAR belum terukur" md:246-247 kabur terhadap FAR24 terukur di JSON (§3.3) |
| | 2c | 6/6 | nol angka karangan dalam cakupan (memang nol angka dikutip) |
| | **jumlah** | **10/30** | |
| (3) User.txt /25 | 3a | 6/6 | lapisan A/B/C eksplisit dan dipakai (md:184-192) |
| | 3b | 3/5 | prinsip baseline relevan per tugas ada (md:188, 204, 218) tetapi komponen baseline tidak lengkap (tanpa prevalence-random/canary-depth) dan tanpa pemetaan angka |
| | 3c | 5/5 | jenis tugas dibedakan tegas: deteksi anomali/kondisi/diagnosis/prediksi (md:92, 147) |
| | 3d | 6/6 | kemampuan+batas+kekuatan bukti per mesin (md:244-264), "belum terukur" dipisah dari gagal, tanpa vonis biner |
| | 3e | 3/3 | sintesis tingkat alat (tingkat 1/2/3, 0 alarm otomatis, keputusan di manusia; md:254-260) |
| | **jumlah** | **23/25** | provisional; penilaian final poin a-e = kartu Evaluasi User.txt |
| (4) Struktur /15 | 4a | 4/4 | outline 19 bab jelas |
| | 4b | 0/4 | penjelasan 7/11/27 tidak ada (0 kemunculan) |
| | 4c | 4/4 | md ⊂ ipynb, 0 baris hilang, pola angka identik |
| | 4d | 0/3 | 14 em-dash, ≥6 sebagai penghubung klausa (§3.6) |
| | **jumlah** | **8/15** | |
| **Total sementara** | | **50/100** | |

### kandidat 2 (`...TECHNICAL_DESIGN.md` + `.ipynb`)

| Kriteria | Sub | Skor | Dasar |
|---|---|---|---|
| (1) Kedalaman teknis /30 | 1a | 10/10 | 5 rumus rule + rumus persistence + rumus hibrida, semua dicocokkan literal ke kode (§4.1-4.3) |
| | 1b | 7/7 | labeling per kelas + jendela label + identity recompute 5/5 + anti-sirkular (kanal terlarang, asersi) + strict-past |
| | 1c | 7/7 | workflow 4 langkah + mekanisme dua pemotong + pemangkasan FP berangka + trade-off recall + degenerasi (§4.3) |
| | 1d | 5/6 | hampir semua klaim menaut JSON/eksekusi (ledger §7, verify per sesi); kecil: rujukan silang ke `V9_EVAL_C_LAYERC`/`V9_PM2_VERDICT` (md:814-817) tidak dibuka di kartu ini |
| | **jumlah** | **29/30** | |
| (2) Akurasi /30 | 2a | 16/18 | butir checklist dalam cakupan (13, 14, 23, 24, 30) muncul dan cocok 1:1 (5/5); sisa butir = AUD-CLAIM (provisional) |
| | 2b | 6/6 | puluhan sel angka bab E_RULE tertelusuri 1:1 (tabel §4.1-§4.4); satu imprecision label D1 tidak mengubah angka |
| | 2c | 6/6 | nol angka karangan dalam cakupan |
| | **jumlah** | **28/30** | |
| (3) User.txt /25 | 3a | 6/6 | lapisan A/B/C hadir dan dipakai per kelas di bab ini |
| | 3b | 5/5 | S9 4 komponen + 5 alasan baseline per tugas, beberapa diuji ulang cocok (§4.4) |
| | 3c | 5/5 | deteksi kondisi vs prediksi onset dibedakan tegas (persistence-event vs horizon, md:2684-2686) |
| | 3d | 6/6 | kemampuan+batas+bukti per kelas; "BELUM" K-2 dipisah; anotasi hindsight; tanpa vonis biner |
| | 3e | 2/3 | sintesis tingkat alat di bab ini baru sebagian (3 head non-ML per kelas → sumber L0/L1, md:2810); komposisi penuh tingkat alat ada di bab lain |
| | **jumlah** | **24/25** | provisional untuk poin a-e global |
| (4) Struktur /15 | 4a | 4/4 | outline sub-tugas 1-5 + verifikasi + batas, jelas |
| | 4b | 4/4 | penjelasan 7/11/27 tegas dan konsisten (§6, 16 kemunculan) |
| | 4c | 4/4 | 0 baris md hilang; selisih hanya selipan baris bernada arsip + selisih pembungkus baris bernada sama |
| | 4d | 3/3 | 0 em-dash di md dan sel markdown ipynb |
| | **jumlah** | **15/15** | |
| **Total sementara** | | **96/100** | |

Bias disclosure: badan kartu memuat penanda tanggal/label versi kedua kandidat; penanda itu
tidak dipakai dalam penilaian (tidak ada kesimpulan versi di dokumen ini) dan skor murni
berdasar isi terhadap primer (protokol §2.6 butir 6).

---

## 7. Belum diverifikasi (verification-mandatory #3)

1. **Rujukan silang kandidat 2 ke `docs/V9_EVAL_C_LAYERC.md` dan `docs/V9_PM2_VERDICT.md`**
   (mis. md:814-817, md:835) tidak dibuka di kartu ini; angka yang bersangkutan sudah
   diverifikasi dari JSON primer, tetapi kecocokan kutipan teks ke dokumen EVAL/PM2 belum diuji.
2. **Seluruh 30 butir checklist §4 protokol**: kartu ini hanya menelusuri butir 13, 14, 23,
   24, 30 (dalam cakupan rule/persistence/hibrida). Sisa butir = AUD-CLAIM, sehingga sub-2a
   masih provisional.
3. **Klaim "identik digit E1d V6" (bit_wear) dan "canary = rentang V8"** dicocokkan ke
   dokumen induk §4.1-4.2, bukan dihitung ulang dari JSON V6/V8 di kartu ini.
4. **Persentase reduksi** dihitung dari pembulatan mentah (73,077% dan 55,667%); pemeriksaan
   apakah kandidat memakai pembulatan 1 desimal yang sama sudah dilakukan, tetapi bukan
   uji terhadap skrip kandidat (skrip `verify*.py` kandidat tidak ada di tree).
5. **Cell code VIS 0..VIS 11** diperiksa judul dan keberadaannya saja; isi numerik di dalam
   cell code tidak dieksekusi (di luar cakupan tugas 1-5; angka yang diklaim di markdown
   sudah diuji ke primer).
6. **Sel markdown ipynb kandidat 1 dan 2 diparse sekali** dengan metode `"".join(source)`;
   tidak diuji apakah ada output tertanam (output tidak dibaca, sesuai §6.4 protokol yang
   hanya mengikat isi sel).
7. **Kriteria (3)** dinilai dari bacaan bab terkait di kedua dokumen; Evaluasi User.txt
   tidak dibaca penuh di kartu ini (kewajiban kartu khusus poin a-e).

---

*Sumber angka kartu ini: `v11_hyb_primary_facts.json` (recompute truth + parity + pola +
em-dash) dan `v11_hyb_scorecard.json` (lembar skor), keduanya di workspace kartu
`t_2cd06fc3`, ditambah eksekusi grep langsung ke `code/v9_e_RULE_01_status.py`,
`docs/V9_E_RULE_ENGINE.md`, dan kedua paket kandidat.*
