# V11-E_STAT: Uji Rumus Statistik & Angka Hasil Kedua Kandidat vs Kode E_STAT

Kartu: `t_dae5389f` · Board: `capstone-v11-vs` · 2026-10-15 (WIB)
Peran: **[Algorithm Engineer Statistik] V11-E_STAT** · ruang kerja: `/mnt/d/Capstone 1(v2)`

**Anonimisasi (aturan kartu):** dokumen ini menyebut **kandidat 1** dan **kandidat 2** saja,
dengan path lengkap agar bisa dicek ulang. Tidak ada kesimpulan versi baru/lama di sini;
perbandingan skor dan keputusan akhir = kewenangan PM-FINAL.

- **kandidat 1** = `/mnt/d/Capstone 1(v2)/docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.v3_arsip.md`
  + pasangan `.v3_arsip.ipynb`
- **kandidat 2** = `/mnt/d/Capstone 1(v2)/docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md`
  + pasangan `.ipynb`

**Riset pendahuluan: `scientific-critical-thinking`** - klaim dipisah OBSERVED (JSON/kode)
vs INTERPRETASI vs BELUM-TERUKUR; tiap hipotesis diberi falsifier (mis. "kandidat 1 tidak
punya isi statistik" diuji dengan cek dua arah md↔ipynb, bukan sekadar grep satu arah).
**Riset pendahuluan: `verification-mandatory`** - bukti mentah per klaim, cross-check sumber
kedua (JSON vs kode vs dokumen hasil induk), hitung-ulang independen, daftar "belum diverifikasi"
di bagian akhir, dan tes pembeda saat ada angka yang bertabrakan (metode korelasi pairwise).
**Riset pendahuluan: `statistical-analysis`** - baseline dinilai relevan per jenis tugas
(deteksi kondisi ≠ prediksi onset ≠ deteksi regime bengkel), CI95 dan signifikansi dibaca
sesuai resep (moving-block bootstrap, CI memuat prev = tidak signifikan), plafon lift 1/prev
dilaporkan, dan n<30 dilabeli UNDERPOWERED.
**Riset pendahuluan: `sequentialthinking`** (sequ-mcp, 4 pikiran, 4/4 sukses) - peta scope,
beda kedalaman sebagai observasi, ledger diskrepansi + falsifier, skoring rubrik + anonimisasi.

---

## 1. Metode uji (semua klaim = eksekusi nyata)

| Langkah | Artefak (workspace kartu) |
|---|---|
| Ekstrak seluruh angka primer dari 4 JSON E_STAT + hitung baris dataset | `v11_stat_primary_facts.json` (skrip `extract_primary.py`) |
| Salinan JSON primer (S6) | `scratch/v9_e_stat_01..04_*_RESULTS.json` |
| Probe diskriminatif klaim flow-out F-9A (239 kolom, non-null, korelasi, kolom flow-out) | `v11_stat_probe_f9a.json`, `v11_stat_probe_f9a_pairwise.json` |
| Perbandingan dua arah md↔ipynb kedua kandidat | `v11_stat_md_ipynb_compare.json`, `v11_stat_ipynb_reverse.json` |
| Uji determinisme: backup md5 → re-run modul → diff | `backup_primary/*.json` |
| sequ-mcp 4 pikiran | `v11_stat_sequ_mcp.json` |

Primer yang dijadikan rujukan: `code/v9_e_STAT_01_hyd_ki.py`, `v9_e_STAT_02_stuck_e2.py`,
`v9_e_STAT_03_tool_wear.py`, `v9_e_STAT_04_fisher_pearson.py`; `scratch/v9_e_stat/*.json`;
`docs/V9_E_STAT_ENGINE.md`; silang: `docs/V9_D1_DATA_PIPELINE.md` §9, `docs/V10_R1_ALASAN.md`,
`docs/V8_E_hyd_CAPABILITY.md`, `docs/V8_A1_CAPABILITY_AUDIT.md`, run log `scratch/v9_e_stat/*_run_log.txt`.

---

## 2. Ringkas hasil per tugas (status per kandidat)

Legenda: **ADA+COCOK** = klaim ada dan angkanya telusur 1:1 ke primer · **ADA+SELISIH** = klaim
ada tetapi bertabrakan dengan primer · **ABSEN** = kandidat tidak memuat klaim yang bisa diuji ·
**KUALITATIF BENAR** = hanya jenis metode yang disebut, tanpa rumus/angka.

| # | Tugas uji | kandidat 1 | kandidat 2 |
|---|---|---|---|
| 1 | Rumus hyd K-i (z=0,6745 per desil TFLO, window W=10, persistence) | ABSEN (hanya keluarga "median/MAD + persistence"); KUALITATIF BENAR | ADA+COCOK (4/4 langkah + sitasi baris kode literal) |
| 2 | Rumus stuck E2 (z(TQA)+z(HKLD)+ROP-drop, q95 di TRAIN) | ABSEN ("Rule + statistik + RF", tanpa rumus) | ADA+COCOK (rumus, ambang per fold, tabel hasil) |
| 3 | Rumus tool_wear (SSE+permutation 500×, kalibrasi 30% R01, ≥5/27 \|z\|>3, FAR-terkalibrasi) | ABSEN ("Change-point statistik + anomaly") | ADA+COCOK (arah ≥, dua ambang, seluruh hasil part A/B/C/D) |
| 4 | Fisher/Pearson + hasil P=R=0 @ q95 | ABSEN (0 kemunculan Fisher/Pearson/atanh) | ADA+COCOK (rumus + status literal + hasil; probe flow-out tereproduksi) |
| 5 | Angka hasil vs JSON (lift 1,06–1,80 CI memuat prev 4/4; deteksi 4/4, FP 1–3, lead 20–36 dtk) | ABSEN (0 angka hasil E_STAT) | ADA+COCOK (semua angka tereproduksi) |
| 6 | md vs ipynb; kelengkapan relatif | PAKET PENUH (md 100% ada di ipynb) tetapi isi E_STAT nihil | PAKET PENUH (md 100% ada di ipynb) + Bab 5 lengkap |

---

## 3. kandidat 1: hasil uji

Dokumen: `docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.v3_arsip.md` (255 baris) +
`docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.v3_arsip.ipynb`.

### 3.1 Tugas 1–5: tidak ada klaim rumus/angka E_STAT yang bisa diuji

Pencarian frasa kunci (di `v11_stat_primary_facts.json` tidak ada; hitung langsung dari file):

| Frasa kunci | Jumlah kemunculan di kandidat 1 |
|---|---|
| `0,6745` / `1,4826` | 0 / 0 |
| `q95`, `permutasi`, `Fisher`, `Pearson`, `atanh` | 0 |
| `qcut`, `TFLO`, `SPPA`, `TQA`, `HKLD`, `SSE`, `5/27`, `\|z\|>3` | 0 |
| `MAD` (hanya sebagai nama metode) | 3 |
| `E_STAT` | 0 |

Isi statistik yang benar-benar ada (dan diverifikasi cocok dengan kode):

- baris 87 & 155: "Deteksi statistik (median/MAD, change-point, skor-z)" sebagai keluarga metode → cocok dengan 4 modul E_STAT (label median/MAD, change-point SSE, skor-z).
- baris 250: "Anomali hidraulik | Deteksi kondisi | Statistik (median/MAD) + persistence" → cocok dengan `v9_e_STAT_01` (label median/MAD per bin + engine persistence).
- baris 252: "Keausan mata bor | Perubahan regime | Change-point statistik + anomaly" → cocok dengan `v9_e_STAT_03`.
- baris 249: "Stuck pipe | Rule + statistik + RF" → konsisten dengan adanya engine E2 statistik (`v9_e_STAT_02`), tanpa detail rumus.
- Baseline relevan per tugas (baris 188, 204), jenis tugas berbeda per mesin (baris 147), persistence sebagai pembanding status-quo (baris 154) → prinsip yang sama dengan primer, tetapi tanpa satu pun angka hasil.

Kesimpulan tugas 1–5: **ABSEN**. Tidak ada klaim keliru (tidak ada yang bisa salah), tetapi
juga tidak ada bukti rumus/angka yang dapat ditelusuri ke primer.

### 3.2 Tugas 6: paket md = ipynb

- md: 255 baris total, **163 baris substansial (≥40 karakter), 100% ditemukan di ipynb**.
- ipynb: 37 sel (25 markdown + 12 code), 42 output, markdown 24.657 karakter vs md 24.094 karakter.
- Arah terbalik: 7 baris ipynb tidak ada di md, semuanya satu blok kutipan pembuka
  "ARSIP VISUALISASI KAMPANYE LAMA (BUKAN BAGIAN NARASI PROPOSAL)" yang menandai 12 code cell
  arsip sebagai bukan bagian narasi. Artinya ipynb = md + blok penanda arsip, bukan konten berbeda.
- `permutation` muncul hanya di code cell arsip (`VIS 9: ... PERMUTATION IMPORTANCE`), bukan isi statistik tersembunyi.

---

## 4. kandidat 2: hasil uji

Dokumen: `docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md` (3.557 baris) + pasangan `.ipynb`.
Bagian yang diuji: **Bab 5 "Metode Statistik" baris 1922–2416**.

### 4.1 Tugas 1: rumus hyd K-i → ADA, COCOK 1:1 dengan kode

| Elemen klaim (Bab 5) | Kode (`v9_e_STAT_01_hyd_ki.py`) | Status |
|---|---|---|
| `q_j = qcut(TFLO, 10)` sitasi "baris 111" | baris 111 `pd.qcut(d["TFLO_mean"], NQ, ...)` | COCOK |
| `z = 0,6745·(SPPA−median_bin)/MAD_bin = (SPPA−med)/(1,4826·MAD)` sitasi "baris 114–117" | baris 117 `z = (d["SPPA_mean"]-med)/(1.4826*MAD...)`; 1/1,4826 = 0,6745 | COCOK (ekuivalen algebrais) |
| `anom = 1[\|z\|>2]` sitasi "baris 118" | baris 118 `(z.abs() > 2)` | COCOK |
| window `n_obs≥MIN_OBS=5`, `n_anom/n_obs ≥ 0,5`, W=10 menit sitasi "baris 142–150" | `W, NQ, MIN_OBS = 10, 10, 5`; loop baris 142–150; `valid & (n_anom/n_obs >= 0.5)` | COCOK |
| persistence `ŷ(t)=y(t−W)` sitasi "baris 195" | baris 195 `"engine": "persistence y_hat(t)=y(t-W)"` | COCOK |
| 52.509 baris, 9 wellbore, LOWO 9 fold | hitung ulang dari `hyd_ki.csv.gz` = **52.509**; JSON 9 fold | COCOK |
| kontrol label: **0 mismatch / 52.509**; `y_prev` **0/45.758** | JSON `label_crosscheck`: total_y_mismatch 0, prev_pairs 45.758, prev_mismatch 0 | COCOK |
| RF dilarang, ΔB negatif 7/7 | `docs/V10_R1_ALASAN.md` baris 57 + `docs/V9_E_STAT_ENGINE.md` baris 80 | COCOK (sumber silang) |

Tabel 9 fold (baris 2077–2085) vs JSON: **90 sel angka (9 fold × 10 kolom) semuanya cocok**
setelah pembulatan (contoh F-10: 7.571/1.394/0,1841/0,843 [0,734;0,915]/4,58 (5,43)/0,899/0,922/
32,4/3,5 = JSON persis; F-5: n 6.332, lift 6,102→6,10; F-9_A: 3,609→3,61). Ringkas JSON juga
cocok: AUPRC 0,4245–0,8426, lift 2,388–6,102 (9/9 >1), ΔB>0 9/9, P 0,6145–0,8986, delay 0–3,5 mnt,
ΔB vs prev 0,3057–0,6585 (klaim 0,306–0,659).

### 4.2 Tugas 2: rumus stuck E2 → ADA, COCOK

- Rumus Bab 5 §5.2.1 (med60 rolling 60 mnt min 20 `shift(1)`, mad60, mean10, z dengan ε=1e-9,
  ROP-drop clip, jumlahan) = kode baris 79–88, sitasi "68–89" (fungsi `e2_score` baris 68–89) COCOK;
  segmen gap >30 mnt (`GAP_SEG_MIN=30`) COCOK; `shift(1)` = strict-past COCOK.
- Ambang q95 dari TRAIN pooled (ops & ~in-block), sitasi "baris 153–165": kode baris 153–159
  (`np.quantile(concat(train_scores), 0.95)`) dan 165 (`pred = s >= thr`) COCOK; anti-sirkular
  `STUCK_RT` hanya mask in-block COCOK (docstring baris 18).
- Ambang per fold **2,4649 / 2,8219 / 2,7621 / 2,5144** = JSON 2,464889 / 2,821882 / 2,762111 / 2,51442 COCOK.
- Tabel 4 fold (§5.2.3) = JSON: F-10 4.216/772/0,183112→0,1831/AUPRC 0,2313→0,231 CI [0,1674;0,3058]→
  [0,167;0,306]/lift 1,263→1,26 (5,461→5,46)/P 0,3125→0,313/R 0,1036→0,104/FAR 73,59→73,6/onset 93/
  R@H 0,1613→0,161/TLead 7,0; F-14 95.925/389/0,004055→0,00406/0,0073/CI [0,0036;0,0149]/1,797→1,80
  (246,6)/0,022/0,031/7,99→8,0/61/0,131/2,5; F-9 16.184/311/0,0192/0,0203/CI [0,0085;0,0352]/1,057→1,06
  (52,0)/0,0/0,0/2,36→2,4/55/0,0/–; F-9_A 2.242/503/0,2244/0,3244→0,324/CI [0,1919;0,4962]→[0,192;0,496]/
  1,446→1,45 (4,457→4,46)/0,487/0,151/66,24→66,2/72/0,181/8,0. **Semua COCOK.**
- Ringkas: AUPRC 0,0073–0,3244, lift **1,057–1,797 (= 1,06–1,80)**, lift>1 **4/4**, CI memuat prev
  **4/4**, onset-run total **281** = JSON persis.
- Onset 93/61/55/72: JSON per fold = 93 (F-10), 61 (F-14), 55 (F-9), 72 (F-9_A) dan cocok dengan
  tabel invarian `docs/V9_D1_DATA_PIPELINE.md` §9 (Onsets ffill 93/61/55/72; catatan D1: F-9 tanpa
  REF V8, bukti lebih lemah; Bab 5 tidak menyalahkankan angkanya).
- Baseline persistence literal: klaim AUPRC 0,827–0,902 dan R@H 0,78–0,94 = JSON 0,8265–0,9016 dan
  0,7818–0,9355 COCOK; penandaan ORACLE + konstruksi V8 recall@H=0 by construction sesuai kode.

### 4.3 Tugas 3: rumus tool_wear → ADA, COCOK

- SSE 1-split dan `p = (1+#{SSE_perm ≥ drop_obs})/(1+500)`: kode `perm_p` baris 76–84
  (`if d >= obs: cnt += 1`; `(cnt+1)/(N_PERM+1)`, `N_PERM=500`) = sitasi Bab 5 "56–84" COCOK.
  Arah `≥` = arah benar (arah V8); klaim CC-1 (R1 §3.7 menulis `≤`, terbalik) sesuai docstring
  modul 03 baris 11–15. Dua ambang p≤0,05 dan p≤0,002 (`P_V8, P_LIT = 0.05, 0.002`) COCOK;
  1/501 = 0,001996 COCOK.
- Kalibrasi: `CAL_FRAC=0.30`, `Z_THR=3.0`, `N_FEAT_ALARM=5`, MAD ×1,4826, alarm ≥5 fitur dari 27,
  baseline 3-RMS ≥1 kanal: kode baris 190–238 (sitasi Bab 5 "190–238") COCOK.
- FAR-terkalibrasi: kode baris 243–277, `q = 1 − target·(len(ev1)/60)/len(ev1)`, target 1,0 dan 0,2
  (sitasi "243–277") COCOK.
- Data: hitung ulang `toolwear_windows.csv` = **469 baris**, 32 kolom − 5 meta = **27 fitur**,
  4 alat (T01–T04) × 2 run (R01/R02) = 8 run → semua angka Bab 5 COCOK.
- Hasil part A vs JSON: signifikan p≤0,05 **8/8**, p≤0,002 **8/8** (semua `perm_p` = 0,002);
  early `<5 dtk` **0/8** (verdict "lanjut dinilai"); spesifisitas R01 **4/4 signifikan** →
  precision run-level 4/8 = **0,50**, recall 1,0; TLead cp → akhir R02 **34/36/39/27, median 35,
  min 27**; selisih antar-family median **16,5 dtk, rentang 8–40**; per family p≤0,05
  **kurt 7/8, crest 8/8, fdom 8/8, rms 8/8** (dihitung ulang dari `runs[].perm_p_*`), cp gabungan
  12-dim 8/8 dua ambang. Semua COCOK.
- Hasil part B vs JSON (per alat): T01 FP 41/42, FAR 58,6, 97,6%, first 0, TLead 60, rule 41, kurangi_ragu 0,00;
  T02 27/35, 46,3, 77,1%, 14, 48, 33, 0,18; T03 30/42, 42,9, 71,4%, 0, 60, 40, 0,25; T04 34/40, 51,0,
  85,0%, 0, 58, 36, 0,06 → COCOK semua; rentang "71–98% di alat baru" dan "FAR 43–59 alarm/menit" COCOK
  (42,857–58,571).
- Hasil part C vs JSON: target 1,0 → FP **1/3/1/3**, deteksi **4/4**, first alarm **35/26/36/38**,
  TLead **25/36/24/20**, % R02 3,3–6,9%; target 0,2 → angka sama (skor diskrit) → klaim
  "**1–3 alarm palsu**", "**lead 20–36 detik**", "deteksi 4/4" COCOK.
- Hasil part D vs JSON: AUPRC 0,5888→**0,589**, prev 0,5117→**0,512**, lift **1,151**, plafon
  **1,954**, ΔB **+0,077**, persistence N/A dinyatakan → COCOK.
- n=8 run UNDERPOWERED (<30) → dilabeli apa adanya, sesuai kode (`underpowered: n_runs<30`).

### 4.4 Tugas 4: Fisher/Pearson → ADA, COCOK (termasuk tes pembeda flow-out)

- Rumus §5.4.1: Pearson, `z' = atanh(r)`, `score = |z' − med_base|/(1,4826·MAD_base)` dengan
  baseline rolling 60 mnt `shift(1)`, alarm `score ≥ q95_TRAIN`: kode baris 165–169 (sitasi "165–169")
  COCOK; jendela korelasi 30 mnt (`WIN_R=30`) COCOK.
- Status literal "TIDAK BISA DIJALANKAN karena FlowOut absen" → **probe ulang saya sendiri** terhadap
  `data/witsml/Norway-NA-15_47_9-F-9 A time.csv`:
  - jumlah kolom = **239** (klaim 239) ✓;
  - kolom yang mengandung flow-out (nama `flow out`/`flowout`) = **0** ✓;
  - non-null: Flow Pumps **345.442**, Mud Flow In **83.565**, TFLO30s **64.757**, FLOW-TRPM
    **34.115** → **persis** angka Bab 5 ✓;
  - korelasi pairwise (metode pandas default): **min 0,99548, maks 1,00000** → klaim
    "r = 0,995–1,000" **BENAR** ✓. (Tes pembeda: perhitungan awal saya dengan complete-case
    `dropna()` menghasilkan 0,9940 dan tampak menyangkal klaim; retest dengan metode asli membalikkan
    hasilnya menjadi cocok, jadi klaim kandidat yang benar, bukan sebaliknya.)
  - jumlah baris file = **419.747** (wc -l 419.748 − header).
- Hasil §5.4.3 vs JSON: 124 episode (**39 kick / 85 loss**), 13 kolom pit (CC-4: PM1 menyebut 12,
  kode memakai 13, probe saya = 13 ✓), split temporal 70/30, test n=**8.107** pos=**30**,
  prev **0,003701**, AUPRC **0,022** CI **[0,0025; 0,0684]** memuat prev, lift **5,945→5,95**
  (plafon 270,233→270,2), **P 0,000 / R 0,000** dengan **TP=0, FP=177, FN=30**, FAR **31,56→31,6**,
  B1 **0/3 onset uji**, baseline prevalence = 0,0037, rule z-pit TLead=0 by construction →
  **semua COCOK**.
- Silang-rujukan "AUPRC RF K-ii V8 = 0,2279 vs varian 0,022": ditemukan di primer dokumen V8
  (`docs/V8_E_hyd_CAPABILITY.md` baris 101: 0,2279 [0,009;0,629]; `docs/V8_A1_CAPABILITY_AUDIT.md`
  baris 66) → COCOK sebagai kutipan dokumen (pembacaan ulang dari JSON V8: lihat §6 belum-diverifikasi).

### 4.5 Tugas 5: angka hasil kunci → ADA, COCOK

| Klaim Bab 5 | Primer | Status |
|---|---|---|
| lift stuck 1,057–1,797 (1,06–1,80) | JSON summary `lift_range_layak [1.057, 1.797]` | COCOK |
| CI95 memuat prev 4/4 fold | JSON `ci95_contains_prev_folds: 4` | COCOK |
| deteksi 4/4 alat, FP 1–3, lead 20–36 dtk (part C) | JSON part C: det 4/4 tiap target, FP 1/3/1/3, TLead 20–36 | COCOK |
| kontrol label hyd 0/52.509, y_prev 0/45.758 | JSON crosscheck (re-run saya 10:18 identik) | COCOK |
| determinisme "4/4 JSON IDENTIK kecuali elapsed_s" | lihat §5 | COCOK (dengan catatan sumber re-run) |
| 8/8 change-point di dua ambang; 0 TP Fisher | JSON part A + part D J4 | COCOK |
| 0 mismatch, 124 episode, 281 onset-run | JSON | COCOK |

### 4.6 Tugas 6: md vs ipynb

- md 2.829 baris total; **2.405 baris substansial, 100% ditemukan di ipynb**.
- ipynb 221 sel (209 markdown + 12 code), 42 output; markdown ipynb 241.137 karakter vs md 240.573.
- Arah terbalik: 8 baris ipynb tidak ada di md = 7 baris blok penanda "ARSIP VISUALISASI KAMPANYE
  LAMA" (struktur sama dengan kandidat 1) + 1 baris gabungan yang di md terpecah dua baris
  (frasa identik ada di md, beda pembungkusan).
- Kesimpulan: paket **kandidat 2 md = ipynb penuh**; 12 code cell arsip identik dengan punya
  kandidat 1 (23.015 karakter kode sama-sama).

### 4.7 Ledger diskrepansi kandidat 2 (dihitung jujur)

| # | Klaim kandidat 2 | Primer | Status |
|---|---|---|---|
| D1 | §5.1.4: "perannya = B3 (beban alarm: **32–111** alarm/24jam-negatif **pada label itu sendiri**)" | JSON `baseline_rule_z_manual.rule_far_per_24h_neg_definitional` = **130,6–510,6**; angka **32–111** = FAR engine persistence (32,38–110,71) | **SELISIH atribusi**. Sumber induk `docs/V9_E_STAT_ENGINE.md` baris 113 menulis kalimat yang sama, jadi kesalahan diwarisi, bukan mengarang; tetapi bertabrakan dengan JSON primer |
| D2 | §5.6: data `...F-9 A time.csv` (**419.745**) padahal §3.2.10 menulis **419.747** | file = 419.747 baris; 419.745 = `raw rows` run log modul 04 setelah drop baris `Time s` gagal parse | **INKONSISTENSI INTERNAL** (dua angka untuk file yang sama; keduanya punya dasar, labelnya tidak konsisten) |
| D3 | §5.4.2 & docstring modul 04 merujuk `probe_03_flow.py` | file itu **tidak ada** di seluruh tree `/mnt/d/Capstone 1(v2)` (find = 0) | **RUJUKAN FILE HILANG**; namun seluruh angkanya tereproduksi ulang dari data primer (§4.4) |

Sisanya: **tidak ditemukan selisih**. Semua sel angka tabel §5.1.4 (90), §5.2.3 (±56),
§5.3.4 (±60), §5.4.3 (±12), rumus/konstanta/sitasi baris kode (±30) cocok dengan primer.

---

## 5. Uji determinisme (klaim "4/4 JSON IDENTIK kecuali elapsed_s")

Backup md5 diambil 10:15, lalu modul dijalankan ulang dan di-diff:

| Modul | elapsed_s sebelum → sesudah | Isi selain elapsed | Siapa re-run |
|---|---|---|---|
| 01 hyd_ki | 14,0 → 23,3 | **identik byte-per-byte** | re-run saya (10:18) |
| 02 stuck_e2 | 25,9 → 31,9 | **identik byte-per-byte** | proses lain di sesi ini; re-run pribadi saya **gagal ENOMEM** |
| 03 tool_wear | 12,7 → 10,1 | **identik byte-per-byte** | re-run saya (10:18) |
| 04 fisher_pearson | 9,9 → 12,2 → 15,3 | **identik byte-per-byte** | dua re-run proses lain (10:04 dan setelahnya) |

Catatan jujur: re-run pribadi modul 02 berhenti dengan `OSError: [Errno 12] Cannot allocate memory`
saat membaca `stuck_k2.csv.gz` (kondisi memori saat itu 7,2/7,6 Gi terpakai, swap penuh; dokumen D1
mencatat kasus ENOMEM serupa pada pembacaan F-14). Karena file JSON 02 tetap berubah isinya
identik-kecuali-elapsed lewat re-run lain pada jendela waktu yang sama, klaim determinisme untuk
02 bertumpu pada re-run sesi, bukan pada tangan saya sendiri. Perubahan file primer ini juga
menandai **hotspot**: `scratch/v9_e_stat/*` ditulis oleh lebih dari satu task di sesi ini
(catatan hotspot dikirim ke papan).

---

## 6. Skor kartu ini (rubrik PM-0, cakupan tugas 1–6)

Disajikan per kandidat secara terpisah; **perbandingan dan keputusan menang = PM-FINAL**.

### kandidat 1 (`...v3_arsip.md` + `.v3_arsip.ipynb`)

| Kriteria | Skor | Dasar |
|---|---|---|
| (1) Kedalaman teknis /30 | **11** | Rumus per engine 0/4; labeling & workflow E_STAT tidak dijabarkan; yang ada: prinsip benar (jenis tugas beda, baseline relevan per tugas, persistence sbg pembanding, AUPRC, anti-sirkular, LOWO) |
| (2) Akurasi terhadap primer /30 | **8** | 0 angka hasil/rumus E_STAT untuk ditelusuri; klaim kualitatif jenis metode (median/MAD+persistence hyd, change-point tool_wear, statistik stuck) = benar vs kode; sisa skor menunggu angka yang tidak ada |
| (3) Kepatuhan Evaluasi User.txt /25 | **24** (provisional) | Dari bacaan kartu ini: lapisan A/B/C eksplisit (§11.2), baseline relevan per tugas, kemampuan+batas+kekuatan bukti (§15), nilai di tingkat alat (tingkat 1/2/3), tanpa vonis biner. Penilaian final = kartu evaluasi User.txt |
| (4) Struktur & keterbacaan /15 | **10** | Outline 19 seksi rapi; md=ipynb 100%; tetapi penjelasan 7/11/27 tidak ada dan konten statistik yang diuji tidak tersedia |
| **Total sementara** | **53/100** | |

### kandidat 2 (`...TECHNICAL_DESIGN.md` + `.ipynb`)

| Kriteria | Skor | Dasar |
|---|---|---|
| (1) Kedalaman teknis /30 | **28** | 4/4 engine dengan rumus notasi matematika + penjelasan awam + sitasi baris kode (semua sitasi diperiksa literal, cocok), labeling, anti-peeking/strict-past, baseline per tugas, change-control CC-1..CC-5, ledger verifikasi; kecil: sebagian rumus hanya dijelaskan kata (mis. kuantil FAR), bagian kepala bab berupa metadata kartu kerja |
| (2) Akurasi terhadap primer /30 | **26** | ±240 sel angka diperiksa, 3 isu: D1 salah atribusi 32–111 (JSON 130,6–510,6), D2 inkonsistensi 419.745/419.747, D3 rujukan `probe_03_flow.py` hilang (angkanya reproduksi) |
| (3) Kepatuhan Evaluasi User.txt /25 | **24** (provisional) | Bab 5: jenis tugas dibedakan (deteksi kondisi vs onset vs regime detik), baseline relevan per tugas, kemampuan+batas+kekuatan bukti, nilai di tingkat alat (L0–L3), tanpa vonis biner ("belum terukur" ≠ 0 ≠ gagal) |
| (4) Struktur & keterbacaan /15 | **14** | Bab 5 berpola tetap (ringkas dosen → 4 sub-bagian → verifikasi → batas → traceability), tabel rapi, md=ipynb 100%, penjelasan 7/11/27 ada (§5.0, §5.5.1(f)); kecil: metadata kartu di kepala bab |
| **Total sementara** | **92/100** | |

---

## 7. Belum diverifikasi (verification-mandatory #3)

1. **Re-run pribadi modul 02** terblokir ENOMEM; determinisme 02 memakai re-run sesi (proses lain),
   bukan eksekusi saya sendiri.
2. **Angka 0,2279 (RF K-ii V8)** diverifikasi sebagai kutipan di dokumen V8, **tidak** dihitung
   ulang dari JSON V8.
3. **Kutipan V8 "CI memuat prev 5/5"** (silang-rujukan §5.2.3) tidak dicek ke JSON V8.
4. **Invarian onset 93/61/55/72** dibandingkan ke tabel `V9_D1_DATA_PIPELINE.md` §9, bukan dengan
   menjalankan ulang pembuatan dataset `stuck_k2`.
5. **Kriteria (3)** dinilai terbatas dari bacaan Bab 5 (kandidat 2) dan §9–§15 (kandidat 1);
   Evaluasi User.txt tidak dibaca penuh di kartu ini.
6. **Angka non-statistik kandidat 1** (121 klaim, 8.474.172 baris, dsb.) di luar cakupan tugas 1–6.
7. **Isi `probe_03_flow.py`** tidak dapat diperiksa (file tidak ada); hanya hasil reproduksinya
   yang diuji.
8. **Run log** primer ikut tertimpa oleh re-run sesi (isi baris sama, stempel waktu baru);
   salinan log lama ada di `backup_primary/`.

---

*Sumber angka kartu ini: `v11_stat_primary_facts.json`, `v11_stat_probe_f9a*.json`,
`v11_stat_md_ipynb_compare.json`, `v11_stat_ipynb_reverse.json`, `v11_stat_sequ_mcp.json`,
`backup_primary/` (semua di workspace kartu `t_dae5389f`), ditambah eksekusi langsung terhadap
4 modul `code/v9_e_STAT_*.py` dan file primer `scratch/v9_e_stat/*`.*
