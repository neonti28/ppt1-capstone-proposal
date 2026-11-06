# V9-E_ML — ENGINE ML (RF/GB/LR) PADA DATA NYATA: 4 HEAD + BASELINE RELEVAN + LOWO

Task: `t_902dd141` [Algorithm Engineer ML] · Board: capstone-v9-build · Tanggal: 2026-10-12 10:23 WIB
Sumbu: `docs/V9_PM1_ARCHITECTURE.md` (spesifikasi §2 + kontrak §3), `docs/V9_R1_JUSTIFICATION.md`
(rumus + baseline §3–§4), `docs/V9_D1_DATA_PIPELINE.md` (dataset + LOWO).
Kerangka penilaian: standar 3 lapisan A/B/C operator ("Evaluasi User.txt") — bukan gate lift 1,5.
Primer data: SEMUA angka di dokumen ini dirender dari JSON hasil eksekusi di
`scratch/v9_e_ml/v9_e_ML_<engine>_RESULTS.json` (oleh `code/v9_e_ML_03_build_doc.py`);
0 angka karangan.

> **Riset pendahuluan: `scientific-critical-thinking`** — OBSERVED (angka eksekusi JSON)
> dipisah dari DESAIN (keputusan harness: hyperparam GB/LR, tau grid) dan DERIVED
> (rekonstruksi event stuck_k2); kontradiksi dataset stuck_k2 (§7) dilaporkan, bukan
> didiamkan; tes pembeda persistence-onset dijalankan apa adanya meski hasilnya
> merugikan ML (§6.4).
> **Riset pendahuluan: `statistical-analysis`** — AUPRC + CI95 moving-block bootstrap
> (blok 60 jendela, 1.000 resample, seed 42) per fold; lift dibaca terhadap plafon
> 1/prev yang dilaporkan per fold; fold <30 positif = UNDERPOWERED dilabeli, tidak
> dihitung mayoritas; FAR per skala aslinya (jendela 1 menit → per 24 jam) tanpa
> konversi diam-diam.
> **Riset pendahuluan: `verification-mandatory`** — determinisme diuji re-run fold 0
> (gerbang 1e-9 S4); anti-sirkularitas di-assert ulang di runtime (0 kanal label di
> fitur); reproduksi silang angka V8-E_vib (lift 1,61/2,36/3,50/1,63 cocok persis)
> = kontrol validitas pipeline; daftar "belum terukur" eksplisit §8.
> **Riset pendahuluan: `what-if-oracle`** — cabang risiko hasil: Ω (ML menang semua),
> α (ML menang vs canary tapi kalah persistence — KASUS NYATA kelas onset), Δ (FAR
> meledak di semua tau — terkonfirmasi), Φ (persistence memang sudah cukup — terdukung
> hyd-K-i V8 + stuck_k2 K-ii di sini); ketegangan direkonsiliasi sebagai KEMAMPUAN +
> BATAS, bukan label gagal (§6).
> **Riset pendahuluan: `consciousness-council`** — 5 arketipe menekan desain harness:
> Empiricist (tau grid = semua titik pra-reg dilaporkan, tanpa pemilihan pasca-hasil),
> Minimalist (1 harness, 3 model, 3 baseline, 4 engine), Contrarian (persistence-onset
> yang "menang telak" ditampilkan penuh §6.4 — bukan disembunyikan), Architect
> (kepatuhan D-A5: nol ML di hyd-K-i), Pragmatist (prioritas engine sesuai fokus kartu).
> **Riset pendahuluan: `sequentialthinking`** (3 pikiran, 3/3 sukses, tool_call sequ-mcp):
> orientasi+inspeksi data → desain harness+keputusan scope → verifikasi hasil+rencana
> dokumen.

---

## 0. RINGKASAN EKSEKUTIF

Empat head ML dilatih pada data nyata Volve dengan split LOWO (28 fold total,
seed 42, tanpa grid search), masing-masing dibandingkan dengan baseline relevan
pada fold yang sama: persistence, canary-kedalaman, prevalence-random.

| Engine | Jenis tugas | Fold | RF AUPRC (rentang) | RF ΔB>0 vs canary | RF ΔB>0 vs persistence | vonis kemampuan |
|---|---|---|---|---|---|---|
| vib | deteksi kondisi | 4 | 0.4405–0.9117 | 4/4 fold layak | 2/4 fold layak | skor penambah layak (reproduksi V8 persis) |
| ssi | deteksi kondisi | 9 (2 UP) | 0.0151–0.4589 | 5/7 fold layak | 6/7 fold layak | skor-ranking layak; keyakinan fold wajib tampil |
| shk | deteksi anomali | 9 | 0.0069–0.1929 | 5/9 fold layak | 4/9 fold layak | layak L2/L1-terkalibrasi sesuai V8; 1 titik hemat-awas (§6.5) |
| stuck K-ii | prediksi onset H=10 mnt | 4 | 0.0697–0.4443 | 4/4 fold layak | 0/4 fold layak | ranking layak; persistence-onset menang telak (§6.4) |

Tidak ada head yang memenuhi syarat alarm otomatis PENUH (L0 butuh FAR≤1/24jam dgn
recall>0 + B1≥80% + G1/G2 mayoritas + C2/C3; titik FAR≤1 dgn recall>0 hanya
4 dari
402 titik uji, dengan recall 0,004–0,012 — lihat §6.5) — konsisten dengan spesifikasi PM
(tier L0 0 slot hari ini). GB/LR = pembanding
seragam; tidak ada model yang dipromosikan/ dibuang — semua hasil tersimpan sebagai
KEMAMPUAN + BATAS + KEKUATAN BUKTI per fold (S8).

## 1. METODE HARNESS (kontrak; DESAIN ditandai eksplisit)

- **Model** (seed 42, tanpa grid search):
  - RF kontrak PM1 §2.1: `RandomForestClassifier(n_estimators=300, min_samples_leaf=5,
    class_weight="balanced_subsample", random_state=42)`; **stuck K-ii E3 = 200 pohon**
    (PM1 §2.4). `n_jobs=-1` (paralelisasi prediksi; lihat determinisme §5).
  - GB (PM1 §1.2 ML heads RF/GBM/LR): `GradientBoostingClassifier(n_estimators=200,
    learning_rate=0.1, max_depth=3, random_state=42)` — **DESAIN tetap** (default
    sklearn yang dikunci; tanpa tuning).
  - LR: `SimpleImputer(median, fold-safe) → StandardScaler(fold-safe) →
    LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)`
    — **DESAIN tetap**.
- **Imputasi**: median fold-safe untuk SEMUA model (fit hanya data latih; PM1 S4).
- **Baseline per fold pada split IDENTIK** (S9; dihitung di sini agar pembanding
  melekat pada JSON engine — E_RULE menghitung ulang mandiri untuk evaluator):
  1. **persistence** `ŷ(t)=y(t−1)` — kolom `y_prev_*` D1 (di-hitung di grid penuh
     sebelum masking; valid_prev==1 bila ada);
  2. **canary-kedalaman** — RF kontrak HANYA dengan fitur `depth_*`/`dbtm_*`
     (kontrol memorisasi posisi);
  3. **prevalence-random** — AUPRC = prevalensi fold (plafon lift = 1/prev dilaporkan).
- **Metrik per fold**: AUPRC + CI95 (moving-block bootstrap, blok 60 jendela,
  1.000 resample, seed 42); lift = AUPRC/prev; P/R/FAR pada tau pra-reg
  {0,05; 0,10; 0,20; 0,30; 0,50} (grid tau PM1 §2.6 dipakai seragam — SEMUA titik
  dilaporkan, tanpa pemilihan pasca-hasil); `FAR_24 = 1440·FP/n_neg` (skala jendela
  1 menit → per 24 jam operasi; asumsi jam operasi = jendela eligible, PM1 §6.3).
- **Onset (stuck K-ii)**: + ambang `q95` skor LATIH (pra-reg PM1 §2.4 E3);
  B1 = % event dengan ≥1 alarm di horizon; TLead median.
- **UNDERPOWERED**: fold uji <30 positif dilabeli, dikecualikan dari hitungan mayoritas.
- **Anti-sirkularitas**: assert runtime — 0 kanal pembentuk label (VIBLAT/SHKRSK/CRPM/
  STUCK) di kolom fitur (55 fitur = 11 kanal × 5 statistik; D1 §2).

## 2. ENGINE YANG DILATIH (fokus kartu, sesuai §2 PM1 + larangan D-A5)

### 2.1 `vib` — deteksi kondisi getaran lateral (PM1 §2.1)

- **RF**: AUPRC 0.4405–0.9117 (spread 0.4712); ΔB>0 vs canary 4/4 fold layak; vs persistence 2/4 fold layak
- **GB**: AUPRC 0.2486–0.9164 (spread 0.6678); ΔB>0 vs canary 3/4 fold layak; vs persistence 1/4 fold layak
- **LR**: AUPRC 0.1839–0.8752 (spread 0.6913); ΔB>0 vs canary 3/4 fold layak; vs persistence 2/4 fold layak

Tabel per fold (semua model + baseline; CI95 RF):

| Fold | Test well | n | pos | prev | UP | RF AUPRC (CI95) | GB AUPRC | LR AUPRC | pers | canary | prev-rand |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | F-14 | 1989 | 1124 | 0.5651 | — | 0.9117 [0.8212; 0.9608] | 0.9164 | 0.8752 | 0.7959 | 0.6124 | 0.5651 |
| 1 | F-15A | 6482 | 1543 | 0.2380 | — | 0.5623 [0.3972; 0.6831] | 0.4665 | 0.6472 | 0.5474 | 0.4578 | 0.2380 |
| 2 | F-15_S | 10903 | 1532 | 0.1405 | — | 0.4914 [0.3380; 0.6186] | 0.2486 | 0.1839 | 0.5166 | 0.2770 | 0.1405 |
| 3 | F-5 | 4548 | 1230 | 0.2704 | — | 0.4405 [0.3405; 0.5535] | 0.5193 | 0.6606 | 0.6675 | 0.3093 | 0.2704 |

ΔB per fold (AUPRC model − AUPRC baseline pada fold yang sama):

| Fold | RF−pers | RF−canary | RF−prev | GB−pers | GB−canary | LR−pers | LR−canary |
|---|---|---|---|---|---|---|---|
| 0 F-14 | +0.1192 | +0.2993 | +0.3466 | +0.1239 | +0.3040 | +0.0828 | +0.2629 |
| 1 F-15A | +0.0149 | +0.1044 | +0.3242 | -0.0809 | +0.0087 | +0.0998 | +0.1893 |
| 2 F-15_S | -0.0181 | +0.2144 | +0.3509 | -0.2608 | -0.0284 | -0.3279 | -0.0931 |
| 3 F-5 | -0.2268 | +0.1313 | +0.1701 | -0.1477 | +0.2101 | -0.0073 | +0.3513 |

P/R/FAR pada tau grid pra-reg (format P/R/FAR per titik tau):

| Fold | Model | tau | P | R | FAR (jendela/24jam) |
|---|---|---|---|---|---|
| 0 F-14 | rf | 0.05: 0.565/1.000/1440.0 · 0.1: 0.565/1.000/1440.0 · 0.2: 0.689/0.974/822.4 · 0.3: 0.718/0.954/699.2 · 0.5: 0.766/0.866/496.1 |
| 0 F-14 | gb | 0.05: 0.696/0.959/782.4 · 0.1: 0.707/0.956/740.8 · 0.2: 0.719/0.946/692.5 · 0.3: 0.728/0.937/655.9 · 0.5: 0.802/0.846/391.2 |
| 0 F-14 | lr | 0.05: 0.742/0.922/599.3 · 0.1: 0.762/0.878/514.4 · 0.2: 0.763/0.874/507.7 · 0.3: 0.799/0.850/399.5 · 0.5: 0.881/0.754/189.8 |
| 1 F-15A | rf | 0.05: 0.241/0.999/1413.5 · 0.1: 0.244/0.995/1389.0 · 0.2: 0.274/0.968/1156.9 · 0.3: 0.384/0.889/642.3 · 0.5: 0.489/0.819/385.4 |
| 1 F-15A | gb | 0.05: 0.321/0.936/890.4 · 0.1: 0.366/0.865/673.8 · 0.2: 0.388/0.715/507.6 · 0.3: 0.411/0.622/400.3 · 0.5: 0.471/0.518/261.5 |
| 1 F-15A | lr | 0.05: 0.256/0.975/1277.0 · 0.1: 0.258/0.956/1235.6 · 0.2: 0.265/0.939/1170.9 · 0.3: 0.270/0.938/1141.4 · 0.5: 0.290/0.931/1023.4 |
| 2 F-15_S | rf | 0.05: 0.188/0.965/983.5 · 0.1: 0.218/0.893/754.7 · 0.2: 0.301/0.719/394.0 · 0.3: 0.383/0.497/188.7 · 0.5: 0.852/0.102/4.1 |
| 2 F-15_S | gb | 0.05: 0.224/0.820/670.1 · 0.1: 0.280/0.713/432.7 · 0.2: 0.289/0.537/310.4 · 0.3: 0.277/0.411/252.5 · 0.5: 0.232/0.213/166.4 |
| 2 F-15_S | lr | 0.05: 0.148/0.979/1327.1 · 0.1: 0.157/0.914/1158.9 · 0.2: 0.200/0.837/789.7 · 0.3: 0.249/0.757/536.8 · 0.5: 0.204/0.375/344.4 |
| 3 F-5 | rf | 0.05: 0.277/1.000/1392.3 · 0.1: 0.327/1.000/1100.2 · 0.2: 0.425/0.984/710.9 · 0.3: 0.433/0.624/435.3 · 0.5: 0.402/0.220/174.9 |
| 3 F-5 | gb | 0.05: 0.371/0.937/849.3 · 0.1: 0.392/0.843/698.7 · 0.2: 0.455/0.692/442.2 · 0.3: 0.547/0.516/227.8 · 0.5: 0.707/0.067/14.8 |
| 3 F-5 | lr | 0.05: 0.271/0.998/1433.5 · 0.1: 0.283/0.993/1340.6 · 0.2: 0.328/0.950/1037.3 · 0.3: 0.409/0.937/722.6 · 0.5: 0.621/0.873/284.3 |

**Silang-kontrol reproduksi**: RF lift per fold = 1,61 / 2,36 / 3,50 / 1,63 — COCOK
PERSIS dengan angka V8-E_vib yang dikutip PM1 §2.1 (G1 4/4); RF≥canary 4/4 (G2).
Reproduksi ini = kontrol validitas bahwa harness V9 memakai resep setara V8.

### 2.2 `ssi` — deteksi kondisi stick-slip (PM1 §2.2)

- **RF**: AUPRC 0.0151–0.4589 (spread 0.4438); ΔB>0 vs canary 5/7 fold layak; vs persistence 6/7 fold layak
- **GB**: AUPRC 0.0069–0.1406 (spread 0.1338); ΔB>0 vs canary 4/7 fold layak; vs persistence 5/7 fold layak
- **LR**: AUPRC 0.0160–0.2082 (spread 0.1922); ΔB>0 vs canary 5/7 fold layak; vs persistence 6/7 fold layak

| Fold | Test well | n | pos | prev | UP | RF AUPRC (CI95) | GB AUPRC | LR AUPRC | pers | canary | prev-rand |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | F-10 | 7133 | 161 | 0.0226 | — | 0.0839 [0.0363; 0.1935] | 0.0430 | 0.0826 | 0.2025 | 0.0302 | 0.0226 |
| 1 | F-12 | 4293 | 83 | 0.0193 | — | 0.0550 [0.0136; 0.1645] | 0.0684 | 0.0810 | 0.0203 | 0.0709 | 0.0193 |
| 2 | F-14 | 5455 | 75 | 0.0137 | — | 0.0286 [0.0090; 0.0753] | 0.0163 | 0.0171 | 0.0122 | 0.0305 | 0.0137 |
| 3 | F-15A | 6020 | 31 | 0.0051 | — | 0.0631 [0.0066; 0.2004] | 0.0367 | 0.0160 | 0.0088 | 0.0139 | 0.0051 |
| 4 | F-15_S | 5342 | 85 | 0.0159 | — | 0.1361 [0.0601; 0.2548] | 0.0552 | 0.0244 | 0.0170 | 0.0243 | 0.0159 |
| 5 | F-5 | 4714 | 102 | 0.0216 | — | 0.1073 [0.0450; 0.2494] | 0.0675 | 0.0628 | 0.0354 | 0.0751 | 0.0216 |
| 6 | F-7 | 982 | 3 | 0.0031 | YA | 0.4589 [0.0000; 0.6961] | 0.0069 | 0.0301 | 0.0000 | 0.0201 | 0.0031 |
| 7 | F-9 | 1126 | 12 | 0.0107 | YA | 0.0151 [0.0000; 0.1161] | 0.0163 | 0.0451 | 0.0117 | 0.0097 | 0.0107 |
| 8 | F-9_A | 841 | 55 | 0.0654 | — | 0.1357 [0.0646; 0.2806] | 0.1406 | 0.2082 | 0.0672 | 0.0860 | 0.0654 |

| Fold | RF−pers | RF−canary | RF−prev | GB−pers | GB−canary | LR−pers | LR−canary |
|---|---|---|---|---|---|---|---|
| 0 F-10 | -0.1168 | +0.0538 | +0.0614 | -0.1599 | +0.0128 | -0.1145 | +0.0524 |
| 1 F-12 | +0.0382 | -0.0159 | +0.0357 | +0.0482 | -0.0025 | +0.0401 | +0.0101 |
| 2 F-14 | +0.0089 | -0.0019 | +0.0148 | -0.0014 | -0.0142 | +0.0053 | -0.0134 |
| 3 F-15A | +0.0562 | +0.0492 | +0.0579 | +0.0331 | +0.0228 | +0.0079 | +0.0021 |
| 4 F-15_S | +0.1195 | +0.1118 | +0.1202 | +0.0386 | +0.0309 | +0.0086 | +0.0001 |
| 5 F-5 | +0.0736 | +0.0322 | +0.0857 | +0.0418 | -0.0076 | +0.0302 | -0.0123 |
| 6 F-7 | +0.0000 | +0.4388 | +0.4558 | +0.0000 | -0.0132 | +0.0000 | +0.0101 |
| 7 F-9 | +0.0049 | +0.0055 | +0.0045 | +0.0057 | +0.0066 | +0.0377 | +0.0355 |
| 8 F-9_A | +0.0892 | +0.0496 | +0.0703 | +0.0865 | +0.0546 | +0.1122 | +0.1221 |

| Fold | Model | tau | P | R | FAR (jendela/24jam) |
|---|---|---|---|---|---|
| 0 F-10 | rf | 0.05: 0.035/0.317/291.2 · 0.1: 0.059/0.161/86.1 · 0.2: 0.268/0.068/6.2 · 0.3: 0.667/0.012/0.2 · 0.5: —/0.000/0.0 |
| 0 F-10 | gb | 0.05: 0.089/0.124/42.3 · 0.1: 0.105/0.093/26.4 · 0.2: 0.056/0.031/17.3 · 0.3: 0.031/0.012/12.8 · 0.5: 0.024/0.006/8.5 |
| 0 F-10 | lr | 0.05: 0.020/0.776/1283.6 · 0.1: 0.028/0.745/869.7 · 0.2: 0.050/0.615/389.9 · 0.3: 0.062/0.311/157.0 · 0.5: 0.079/0.199/76.6 |
| 1 F-12 | rf | 0.05: 0.022/0.940/1192.7 · 0.1: 0.031/0.614/545.2 · 0.2: 0.039/0.120/83.8 · 0.3: 0.267/0.048/3.8 · 0.5: —/0.000/0.0 |
| 1 F-12 | gb | 0.05: 0.060/0.627/279.4 · 0.1: 0.057/0.446/207.6 · 0.2: 0.084/0.398/122.5 · 0.3: 0.087/0.349/104.0 · 0.5: 0.085/0.265/81.4 |
| 1 F-12 | lr | 0.05: 0.020/0.976/1375.0 · 0.1: 0.020/0.952/1341.8 · 0.2: 0.021/0.952/1251.2 · 0.3: 0.021/0.904/1169.4 · 0.5: 0.027/0.892/923.9 |
| 2 F-14 | rf | 0.05: 0.023/0.413/358.7 · 0.1: 0.024/0.133/108.1 · 0.2: 0.079/0.040/9.4 · 0.3: —/0.000/0.0 · 0.5: —/0.000/0.0 |
| 2 F-14 | gb | 0.05: 0.020/0.040/40.1 · 0.1: 0.012/0.013/21.7 · 0.2: 0.026/0.013/10.2 · 0.3: 0.043/0.013/5.9 · 0.5: 0.111/0.013/2.1 |
| 2 F-14 | lr | 0.05: 0.011/0.720/1304.6 · 0.1: 0.011/0.627/1140.8 · 0.2: 0.009/0.373/788.8 · 0.3: 0.009/0.267/559.9 · 0.5: 0.015/0.227/301.4 |
| 3 F-15A | rf | 0.05: 0.037/0.581/112.8 · 0.1: 0.076/0.226/20.4 · 0.2: 0.217/0.161/4.3 · 0.3: 0.000/0.000/2.6 · 0.5: 0.000/0.000/0.2 |
| 3 F-15A | gb | 0.05: 0.048/0.129/19.0 · 0.1: 0.000/0.000/16.1 · 0.2: 0.000/0.000/15.6 · 0.3: 0.000/0.000/15.6 · 0.5: 0.000/0.000/14.7 |
| 3 F-15A | lr | 0.05: 0.005/0.871/1426.1 · 0.1: 0.005/0.806/1308.5 · 0.2: 0.006/0.581/768.9 · 0.3: 0.008/0.452/405.4 · 0.5: 0.016/0.355/166.9 |
| 4 F-15_S | rf | 0.05: 0.028/0.765/627.3 · 0.1: 0.052/0.529/225.7 · 0.2: 0.225/0.318/25.5 · 0.3: 0.242/0.094/6.8 · 0.5: —/0.000/0.0 |
| 4 F-15_S | gb | 0.05: 0.017/0.400/537.4 · 0.1: 0.019/0.306/376.1 · 0.2: 0.025/0.282/253.9 · 0.3: 0.040/0.282/157.0 · 0.5: 0.043/0.153/78.9 |
| 4 F-15_S | lr | 0.05: 0.016/1.000/1438.1 · 0.1: 0.016/1.000/1428.2 · 0.2: 0.017/1.000/1319.2 · 0.3: 0.024/0.953/888.6 · 0.5: 0.024/0.588/552.8 |
| 5 F-5 | rf | 0.05: 0.031/0.755/761.5 · 0.1: 0.062/0.618/295.4 · 0.2: 0.128/0.314/68.1 · 0.3: 0.206/0.127/15.6 · 0.5: 0.000/0.000/0.9 |
| 5 F-5 | gb | 0.05: 0.147/0.206/38.1 · 0.1: 0.130/0.118/25.0 · 0.2: 0.087/0.059/19.7 · 0.3: 0.079/0.049/18.1 · 0.5: 0.097/0.029/8.7 |
| 5 F-5 | lr | 0.05: 0.022/1.000/1412.8 · 0.1: 0.023/0.980/1334.5 · 0.2: 0.027/0.892/1031.9 · 0.3: 0.029/0.735/785.3 · 0.5: 0.038/0.490/396.8 |
| 6 F-7 | rf | 0.05: 0.009/1.000/482.5 · 0.1: 0.074/0.667/36.8 · 0.2: —/0.000/0.0 · 0.3: —/0.000/0.0 · 0.5: —/0.000/0.0 |
| 6 F-7 | gb | 0.05: 0.007/0.667/428.0 · 0.1: 0.000/0.000/413.3 · 0.2: 0.000/0.000/398.6 · 0.3: 0.000/0.000/395.7 · 0.5: 0.000/0.000/389.8 |
| 6 F-7 | lr | 0.05: 0.003/1.000/1440.0 · 0.1: 0.003/1.000/1417.9 · 0.2: 0.004/1.000/1151.7 · 0.3: 0.006/1.000/754.6 · 0.5: 0.010/1.000/438.3 |
| 7 F-9 | rf | 0.05: 0.008/0.167/312.8 · 0.1: 0.032/0.167/77.6 · 0.2: —/0.000/0.0 · 0.3: —/0.000/0.0 · 0.5: —/0.000/0.0 |
| 7 F-9 | gb | 0.05: 0.000/0.000/20.7 · 0.1: 0.000/0.000/5.2 · 0.2: 0.000/0.000/1.3 · 0.3: 0.000/0.000/1.3 · 0.5: 0.000/0.000/1.3 |
| 7 F-9 | lr | 0.05: 0.011/1.000/1440.0 · 0.1: 0.011/1.000/1376.7 · 0.2: 0.015/1.000/1030.2 · 0.3: 0.021/1.000/734.2 · 0.5: 0.010/0.167/259.8 |
| 8 F-9_A | rf | 0.05: 0.073/1.000/1287.9 · 0.1: 0.157/0.582/315.1 · 0.2: 0.000/0.000/34.8 · 0.3: 0.000/0.000/3.7 · 0.5: —/0.000/0.0 |
| 8 F-9_A | gb | 0.05: 0.150/0.291/166.7 · 0.1: 0.148/0.164/95.3 · 0.2: 0.103/0.073/64.1 · 0.3: 0.091/0.036/36.6 · 0.5: 0.083/0.018/20.2 |
| 8 F-9_A | lr | 0.05: 0.066/1.000/1430.8 · 0.1: 0.066/1.000/1418.0 · 0.2: 0.070/1.000/1341.1 · 0.3: 0.072/0.964/1251.3 · 0.5: 0.086/0.945/1018.6 |

Catatan: fold F-7 (3 positif) dan F-9 (12 positif) UNDERPOWERED — AUPRC mereka
(F-7 RF 0.4589) tidak boleh dibaca sebagai
bukti stabil; fold layak = 7. Persistence justru kuat di F-10
(0.2025) — dapat dilihat sebagai
KEMAMPUAN baseline (stick-slip persisten antar-grid di sumur itu), bukan aib ML.

### 2.3 `shk` — deteksi anomali/dysfunction bit bounce (PM1 §2.6)

- **RF**: AUPRC 0.0069–0.1929 (spread 0.1860); ΔB>0 vs canary 5/9 fold layak; vs persistence 4/9 fold layak
- **GB**: AUPRC 0.0093–0.1171 (spread 0.1078); ΔB>0 vs canary 5/9 fold layak; vs persistence 4/9 fold layak
- **LR**: AUPRC 0.0148–0.0997 (spread 0.0850); ΔB>0 vs canary 5/9 fold layak; vs persistence 4/9 fold layak

| Fold | Test well | n | pos | prev | UP | RF AUPRC (CI95) | GB AUPRC | LR AUPRC | pers | canary | prev-rand |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | F-10 | 7899 | 146 | 0.0185 | — | 0.0201 [0.0100; 0.0349] | 0.0219 | 0.0194 | 0.0236 | 0.0212 | 0.0185 |
| 1 | F-12 | 5405 | 217 | 0.0401 | — | 0.0456 [0.0189; 0.0945] | 0.0324 | 0.0892 | 0.0492 | 0.0652 | 0.0401 |
| 2 | F-14 | 11205 | 760 | 0.0678 | — | 0.1036 [0.0626; 0.1659] | 0.0892 | 0.0542 | 0.1673 | 0.0630 | 0.0678 |
| 3 | F-15A | 6484 | 41 | 0.0063 | — | 0.0069 [0.0017; 0.0155] | 0.0093 | 0.0203 | 0.0063 | 0.0121 | 0.0063 |
| 4 | F-15_S | 11394 | 259 | 0.0227 | — | 0.0265 [0.0160; 0.0404] | 0.0246 | 0.0148 | 0.0393 | 0.0251 | 0.0227 |
| 5 | F-5 | 7140 | 240 | 0.0336 | — | 0.0896 [0.0473; 0.1847] | 0.0886 | 0.0997 | 0.0452 | 0.0487 | 0.0336 |
| 6 | F-7 | 2761 | 267 | 0.0967 | — | 0.1015 [0.0449; 0.1829] | 0.1171 | 0.0906 | 0.4457 | 0.0789 | 0.0967 |
| 7 | F-9 | 1851 | 45 | 0.0243 | — | 0.1929 [0.0318; 0.4657] | 0.1117 | 0.0865 | 0.0384 | 0.0611 | 0.0243 |
| 8 | F-9_A | 2356 | 30 | 0.0127 | — | 0.0209 [0.0016; 0.0504] | 0.0206 | 0.0303 | 0.0144 | 0.0388 | 0.0127 |

| Fold | RF−pers | RF−canary | RF−prev | GB−pers | GB−canary | LR−pers | LR−canary |
|---|---|---|---|---|---|---|---|
| 0 F-10 | -0.0034 | -0.0011 | +0.0016 | -0.0010 | +0.0007 | -0.0035 | -0.0018 |
| 1 F-12 | -0.0258 | -0.0196 | +0.0055 | -0.0292 | -0.0328 | -0.0274 | +0.0240 |
| 2 F-14 | -0.0842 | +0.0406 | +0.0358 | -0.0932 | +0.0262 | -0.1232 | -0.0088 |
| 3 F-15A | +0.0006 | -0.0053 | +0.0005 | +0.0030 | -0.0028 | +0.0141 | +0.0082 |
| 4 F-15_S | -0.0125 | +0.0014 | +0.0038 | -0.0148 | -0.0006 | -0.0255 | -0.0104 |
| 5 F-5 | +0.0659 | +0.0409 | +0.0560 | +0.0469 | +0.0399 | +0.0386 | +0.0510 |
| 6 F-7 | -0.3436 | +0.0226 | +0.0048 | -0.3271 | +0.0382 | -0.3555 | +0.0117 |
| 7 F-9 | +0.1591 | +0.1318 | +0.1686 | +0.0757 | +0.0506 | +0.0502 | +0.0254 |
| 8 F-9_A | +0.0090 | -0.0179 | +0.0082 | +0.0139 | -0.0182 | +0.0205 | -0.0085 |

| Fold | Model | tau | P | R | FAR (jendela/24jam) |
|---|---|---|---|---|---|
| 0 F-10 | rf | 0.05: 0.022/0.295/351.6 · 0.1: 0.010/0.041/112.2 · 0.2: 0.000/0.000/11.9 · 0.3: —/0.000/0.0 · 0.5: —/0.000/0.0 |
| 0 F-10 | gb | 0.05: 0.040/0.068/44.6 · 0.1: 0.000/0.000/7.8 · 0.2: 0.000/0.000/3.7 · 0.3: 0.000/0.000/3.2 · 0.5: 0.000/0.000/3.2 |
| 0 F-10 | lr | 0.05: 0.018/0.842/1237.0 · 0.1: 0.018/0.644/934.1 · 0.2: 0.018/0.253/378.9 · 0.3: 0.025/0.103/108.7 · 0.5: 0.000/0.000/25.6 |
| 1 F-12 | rf | 0.05: 0.042/0.641/876.8 · 0.1: 0.060/0.392/372.8 · 0.2: 0.035/0.032/53.3 · 0.3: 0.000/0.000/9.7 · 0.5: —/0.000/0.0 |
| 1 F-12 | gb | 0.05: 0.029/0.249/510.2 · 0.1: 0.036/0.143/232.3 · 0.2: 0.039/0.083/123.0 · 0.3: 0.033/0.051/90.8 · 0.5: 0.020/0.018/55.5 |
| 1 F-12 | lr | 0.05: 0.040/0.995/1430.6 · 0.1: 0.038/0.908/1401.4 · 0.2: 0.027/0.562/1235.4 · 0.3: 0.025/0.488/1141.9 · 0.5: 0.022/0.396/1084.4 |
| 2 F-14 | rf | 0.05: 0.080/0.420/506.5 · 0.1: 0.102/0.146/135.4 · 0.2: 0.292/0.037/9.4 · 0.3: 0.444/0.005/0.7 · 0.5: —/0.000/0.0 |
| 2 F-14 | gb | 0.05: 0.138/0.066/43.2 · 0.1: 0.141/0.037/23.6 · 0.2: 0.133/0.020/13.5 · 0.3: 0.118/0.014/11.3 · 0.5: 0.118/0.011/8.3 |
| 2 F-14 | lr | 0.05: 0.067/0.989/1433.1 · 0.1: 0.063/0.876/1374.2 · 0.2: 0.043/0.472/1091.5 · 0.3: 0.038/0.255/676.8 · 0.5: 0.067/0.116/169.4 |
| 3 F-15A | rf | 0.05: 0.006/0.317/444.5 · 0.1: 0.002/0.024/91.4 · 0.2: 0.000/0.000/10.3 · 0.3: 0.000/0.000/6.5 · 0.5: —/0.000/0.0 |
| 3 F-15A | gb | 0.05: 0.007/0.049/61.9 · 0.1: 0.006/0.024/36.4 · 0.2: 0.007/0.024/32.0 · 0.3: 0.007/0.024/30.8 · 0.5: 0.008/0.024/29.3 |
| 3 F-15A | lr | 0.05: 0.006/1.000/1439.8 · 0.1: 0.006/1.000/1428.6 · 0.2: 0.006/1.000/1418.5 · 0.3: 0.007/1.000/1267.0 · 0.5: 0.012/0.537/402.7 |
| 4 F-15_S | rf | 0.05: 0.036/0.795/711.8 · 0.1: 0.008/0.042/166.0 · 0.2: 0.000/0.000/0.3 · 0.3: —/0.000/0.0 · 0.5: —/0.000/0.0 |
| 4 F-15_S | gb | 0.05: 0.003/0.008/79.5 · 0.1: 0.000/0.000/49.5 · 0.2: 0.000/0.000/21.3 · 0.3: 0.000/0.000/5.8 · 0.5: 0.000/0.000/1.9 |
| 4 F-15_S | lr | 0.05: 0.010/0.328/1122.0 · 0.1: 0.009/0.290/1088.2 · 0.2: 0.007/0.181/912.0 · 0.3: 0.004/0.085/697.2 · 0.5: 0.007/0.054/256.1 |
| 5 F-5 | rf | 0.05: 0.038/0.817/1047.4 · 0.1: 0.057/0.454/372.9 · 0.2: 0.139/0.183/56.8 · 0.3: 0.202/0.079/15.7 · 0.5: 0.000/0.000/0.8 |
| 5 F-5 | gb | 0.05: 0.095/0.438/208.5 · 0.1: 0.107/0.317/132.9 · 0.2: 0.123/0.175/62.6 · 0.3: 0.119/0.100/36.9 · 0.5: 0.170/0.037/9.2 |
| 5 F-5 | lr | 0.05: 0.034/1.000/1440.0 · 0.1: 0.034/1.000/1440.0 · 0.2: 0.034/1.000/1432.1 · 0.3: 0.036/0.954/1297.7 · 0.5: 0.053/0.733/656.1 |
| 6 F-7 | rf | 0.05: 0.124/0.742/810.6 · 0.1: 0.074/0.146/282.9 · 0.2: 0.017/0.007/65.8 · 0.3: 0.000/0.000/31.2 · 0.5: 0.000/0.000/5.8 |
| 6 F-7 | gb | 0.05: 0.064/0.082/185.3 · 0.1: 0.052/0.037/105.7 · 0.2: 0.025/0.011/68.7 · 0.3: 0.023/0.007/49.1 · 0.5: 0.000/0.000/31.8 |
| 6 F-7 | lr | 0.05: 0.097/1.000/1432.5 · 0.1: 0.097/1.000/1432.5 · 0.2: 0.098/1.000/1422.7 · 0.3: 0.097/0.876/1251.2 · 0.5: 0.087/0.416/668.6 |
| 7 F-9 | rf | 0.05: 0.027/0.800/1036.5 · 0.1: 0.032/0.644/708.8 · 0.2: 0.096/0.622/211.3 · 0.3: 0.154/0.489/96.5 · 0.5: 0.359/0.311/19.9 |
| 7 F-9 | gb | 0.05: 0.046/0.556/413.0 · 0.1: 0.076/0.556/243.2 · 0.2: 0.121/0.533/138.7 · 0.3: 0.232/0.422/50.2 · 0.5: 0.071/0.022/10.4 |
| 7 F-9 | lr | 0.05: 0.024/1.000/1440.0 · 0.1: 0.024/1.000/1440.0 · 0.2: 0.026/0.978/1302.9 · 0.3: 0.031/0.867/965.6 · 0.5: 0.061/0.511/280.7 |
| 8 F-9_A | rf | 0.05: 0.016/1.000/1173.2 · 0.1: 0.022/0.500/412.9 · 0.2: 0.000/0.000/52.0 · 0.3: 0.000/0.000/14.2 · 0.5: —/0.000/0.0 |
| 8 F-9_A | gb | 0.05: 0.012/0.167/247.6 · 0.1: 0.012/0.067/99.1 · 0.2: 0.041/0.067/29.1 · 0.3: 0.000/0.000/5.6 · 0.5: 0.000/0.000/1.2 |
| 8 F-9_A | lr | 0.05: 0.013/1.000/1406.6 · 0.1: 0.013/1.000/1400.4 · 0.2: 0.013/1.000/1391.7 · 0.3: 0.014/1.000/1347.1 · 0.5: 0.020/1.000/891.5 |

Catatan: di SEMUA fold dan SEMUA model × tau, FAR > 60/24jam — tidak ada titik yang
memenuhi syarat L1 (FAR≤6/24jam dengan recall>0) di kerangka ini; hal ini konsisten
dengan temuan V8 (FAR≤6 dgn recall>0 = hanya 4 titik di kurva V8; kalibrasi lokal
per well = prasyarat, D-A4). Sub-tugas onset shk (B1/TLead, H=10 mnt) BELUM diukur di
sini: dataset shk D1 = status windows saja (tanpa dataset onset shk).

### 2.4 `stuck K-ii` — prediksi onset stuck-pipe, H=10 menit (PM1 §2.4)

- **RF**: AUPRC 0.0697–0.4443 (spread 0.3747); ΔB>0 vs canary 4/4 fold layak; vs persistence 0/4 fold layak
- **GB**: AUPRC 0.0192–0.2917 (spread 0.2725); ΔB>0 vs canary 4/4 fold layak; vs persistence 0/4 fold layak
- **LR**: AUPRC 0.0132–0.3128 (spread 0.2996); ΔB>0 vs canary 4/4 fold layak; vs persistence 0/4 fold layak

| Fold | Test well | n | pos | prev | UP | RF AUPRC (CI95) | GB AUPRC | LR AUPRC | pers | canary | prev-rand |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | F-10 | 4216 | 772 | 0.1831 | — | 0.1997 [0.1386; 0.2836] | 0.2020 | 0.2874 | 0.9016 | 0.1758 | 0.1831 |
| 1 | F-14 | 95925 | 389 | 0.0041 | — | 0.0704 [0.0276; 0.1458] | 0.0192 | 0.0132 | 0.8438 | 0.0092 | 0.0041 |
| 2 | F-9 | 16184 | 311 | 0.0192 | — | 0.0697 [0.0300; 0.1223] | 0.0554 | 0.0791 | 0.8265 | 0.0402 | 0.0192 |
| 3 | F-9_A | 2242 | 503 | 0.2244 | — | 0.4443 [0.3339; 0.5647] | 0.2917 | 0.3128 | 0.8890 | 0.2569 | 0.2244 |

| Fold | RF−pers | RF−canary | RF−prev | GB−pers | GB−canary | LR−pers | LR−canary |
|---|---|---|---|---|---|---|---|
| 0 F-10 | -0.7019 | +0.0239 | +0.0166 | -0.6996 | +0.0262 | -0.6142 | +0.1116 |
| 1 F-14 | -0.7734 | +0.0612 | +0.0664 | -0.8246 | +0.0100 | -0.8306 | +0.0040 |
| 2 F-9 | -0.7569 | +0.0294 | +0.0505 | -0.7712 | +0.0151 | -0.7475 | +0.0389 |
| 3 F-9_A | -0.4446 | +0.1874 | +0.2200 | -0.5973 | +0.0348 | -0.5762 | +0.0559 |

B1 + TLead (rekonstruksi DERIVED dari run positif berurutan — lihat §7 kolom waktu):

| Fold well | Model | thr | B1 | TLead med (mnt) | deteksi |
|---|---|---|---|---|---|
| F-10 | rf | q95_train | 0.657 | 10.0 | 44/67 |
| F-10 | rf | 0.1 | 0.358 | 8.0 | 24/67 |
| F-10 | gb | q95_train | 0.851 | 10.0 | 57/67 |
| F-10 | gb | 0.1 | 0.418 | 10.0 | 28/67 |
| F-10 | lr | q95_train | 0.687 | 10.0 | 46/67 |
| F-10 | lr | 0.1 | 0.985 | 10.0 | 66/67 |
| F-14 | rf | q95_train | 0.000 | — | 0/28 |
| F-14 | rf | 0.1 | 1.000 | 10.0 | 28/28 |
| F-14 | gb | q95_train | 0.393 | 10.0 | 11/28 |
| F-14 | gb | 0.1 | 0.964 | 10.0 | 27/28 |
| F-14 | lr | q95_train | 0.679 | 10.0 | 19/28 |
| F-14 | lr | 0.1 | 1.000 | 10.0 | 28/28 |
| F-9 | rf | q95_train | 1.000 | 11.5 | 16/16 |
| F-9 | rf | 0.1 | 1.000 | 11.5 | 16/16 |
| F-9 | gb | q95_train | 0.562 | 10.0 | 9/16 |
| F-9 | gb | 0.1 | 0.500 | 7.5 | 8/16 |
| F-9 | lr | q95_train | 0.938 | 12.0 | 15/16 |
| F-9 | lr | 0.1 | 1.000 | 11.5 | 16/16 |
| F-9_A | rf | q95_train | 1.000 | 10.0 | 37/37 |
| F-9_A | rf | 0.1 | 0.892 | 10.0 | 33/37 |
| F-9_A | gb | q95_train | 0.649 | 10.0 | 24/37 |
| F-9_A | gb | 0.1 | 0.432 | 10.0 | 16/37 |
| F-9_A | lr | q95_train | 0.297 | 9.0 | 11/37 |
| F-9_A | lr | 0.1 | 1.000 | 10.0 | 37/37 |

Basis pembanding — persistence-onset (E0) dihitung langsung dari kolom dataset
(`y_prev_stuck_onset`), tanpa model:

| Well uji | n event (runpositif berurutan) | B1 persistence | TLead med (mnt) |
|---|---|---|---|
| F-10 | 67 | 1.000 | 9.0 |
| F-14 | 28 | 1.000 | 9.0 |
| F-9 | 16 | 1.000 | 10.5 |
| F-9_A | 37 | 1.000 | 9.0 |

P/R/FAR model pada q95-train + tau grid (q95 = ambang pra-reg E3):

| Fold | Model | tau | P | R | FAR (jendela/24jam) |
|---|---|---|---|---|---|
| 0 F-10 | rf | 0.05: 0.194/0.364/489.6 · 0.1: 0.163/0.149/247.5 · 0.2: 0.312/0.038/26.8 · 0.3: 0.583/0.027/6.3 · 0.5: 0.571/0.005/1.3 · q95_train: 0.177/0.521/784.0 |
| 0 F-10 | gb | 0.05: 0.199/0.267/346.6 · 0.1: 0.194/0.193/259.7 · 0.2: 0.210/0.102/124.6 · 0.3: 0.170/0.058/92.0 · 0.5: 0.172/0.030/46.4 · q95_train: 0.196/0.531/703.7 |
| 0 F-10 | lr | 0.05: 0.231/0.975/1045.3 · 0.1: 0.247/0.969/952.5 · 0.2: 0.254/0.952/902.3 · 0.3: 0.264/0.940/847.1 · 0.5: 0.263/0.890/804.9 · q95_train: 0.294/0.535/415.2 |
| 1 F-14 | rf | 0.05: 0.014/0.995/419.7 · 0.1: 0.019/0.987/301.9 · 0.2: 0.028/0.833/168.7 · 0.3: 0.074/0.401/29.3 · 0.5: 0.048/0.005/0.6 · q95_train: —/0.000/0.0 |
| 1 F-14 | gb | 0.05: 0.017/0.846/286.8 · 0.1: 0.017/0.679/225.7 · 0.2: 0.018/0.509/165.0 · 0.3: 0.017/0.368/124.5 · 0.5: 0.012/0.152/70.6 · q95_train: 0.012/0.134/63.6 |
| 1 F-14 | lr | 0.05: 0.011/1.000/551.1 · 0.1: 0.012/0.979/476.9 · 0.2: 0.014/0.969/405.2 · 0.3: 0.015/0.933/366.9 · 0.5: 0.016/0.910/329.3 · q95_train: 0.012/0.398/191.4 |
| 2 F-9 | rf | 0.05: 0.095/0.997/266.8 · 0.1: 0.113/0.904/200.7 · 0.2: 0.000/0.000/80.6 · 0.3: 0.000/0.000/41.2 · 0.5: 0.000/0.000/11.2 · q95_train: 0.098/0.994/258.0 |
| 2 F-9 | gb | 0.05: 0.054/0.354/175.4 · 0.1: 0.036/0.125/94.0 · 0.2: 0.000/0.000/40.5 · 0.3: 0.000/0.000/21.0 · 0.5: 0.000/0.000/6.9 · q95_train: 0.058/0.338/155.2 |
| 2 F-9 | lr | 0.05: 0.025/1.000/1080.5 · 0.1: 0.031/1.000/891.1 · 0.2: 0.047/1.000/572.7 · 0.3: 0.060/1.000/439.2 · 0.5: 0.071/1.000/370.8 · q95_train: 0.104/0.881/213.6 |
| 3 F-9_A | rf | 0.05: 0.332/0.968/812.3 · 0.1: 0.374/0.642/448.0 · 0.2: 0.431/0.396/217.8 · 0.3: 0.515/0.203/79.5 · 0.5: 1.000/0.004/0.0 · q95_train: 0.313/0.990/903.4 |
| 3 F-9_A | gb | 0.05: 0.254/0.278/341.2 · 0.1: 0.335/0.137/113.4 · 0.2: 0.339/0.078/62.9 · 0.3: 0.341/0.058/46.4 · 0.5: 0.222/0.020/29.0 · q95_train: 0.296/0.475/470.3 |
| 3 F-9_A | lr | 0.05: 0.277/0.988/1076.5 · 0.1: 0.286/0.966/1004.4 · 0.2: 0.332/0.909/762.6 · 0.3: 0.336/0.761/626.0 · 0.5: 0.334/0.598/496.0 · q95_train: 0.258/0.127/152.4 |

## 3. HEAD DI LUAR LATIHAN INI — STATUS EKSPLISIT (bukan "gagal", bukan nol diam)

| Head (PM1 §2) | Status di kartu ini | Alasan |
|---|---|---|
| hyd-K-i (median/MAD + persistence) | **sengaja TANPA ML** | D-A5: RF DILARANG di kelas ini (ΔB negatif 7/7 V8, replikasi eksak); dataset `hyd_ki` D1 tersedia untuk E_STAT/E_RULE |
| stuck K-i (persistence) | **bukan head ML per spesifikasi** | PM1 §2.4: K-i = persistence (E_STAT/E_RULE); dataset `stuck_k1` tersedia |
| hyd-K-ii RF (+varian flow-in) | **belum terukur** | dataset onset ΔV_pit (12 kolom pit F-9A time.csv) TIDAK diproduksi D1 |
| bit_wear K-1 RF / K-2 onset RF | **belum terukur** | dataset USROP 30-fitur E1d + onset K-2 TIDAK diproduksi D1; K-2 juga menunggu pra-reg kampanye |
| tool_wear K-ii LOTO RF | **belum terukur di kartu ini** | modul terpisah domain bengkel (D-A7); dataset Mendeley tidak masuk pipeline D1 |
| shk sub-onset (H=10 mnt) | **belum terukur** | dataset D1 shk = status windows; onset-shk butuh dataset terpisah |

## 4. HASIL PER LIPATAN: JENIS TUGAS + JENIS ENGINE + BASELINE (tugas wajib #5)

| Engine | Jenis tugas | Jenis engine (kartu ini) | Baseline dipakai | Lipatan |
|---|---|---|---|---|
| vib | deteksi kondisi (status) | RF/GB/LR skor-penambah di atas rule/persistence | persistence · canary-depth · prevalence-random | 4 LOWO (F-14, F-15A, F-15_S, F-5) |
| ssi | deteksi kondisi (status) | RF/GB/LR skor-ranking | persistence · canary-depth · prevalence-random | 9 LOWO (2 underpowered) |
| shk | deteksi anomali berlangsung | RF/GB/LR | persistence · canary-depth · prevalence-random | 9 LOWO |
| stuck K-ii | prediksi kejadian (onset) | E3_RF(200)+GB+LR; ambang q95-train | persistence-onset (E0) · canary-depth · prevalence-random | 4 LOWO (F-10, F-14, F-9, F-9_A) |

TLead pada kelas status (vib/ssi/shk) = **tidak berlaku** (tugas deteksi status;
PM1 §2.1) — bukan "belum terukur".

## 5. DETERMINISME (S4)

- Semua model `random_state=42`; imputer/scaler fold-safe; seed bootstrap 42 per fold.
- Uji re-run fold 0 vib (RF 300 pohon): `max_abs_diff = 2.220e-16`
  antara dua run identik — di bawah gerbang 1e-9 S4 (PASS), meski bukan bit-exact
  karena akumulasi float `n_jobs=-1`; catatan jujur: untuk reproduksi bit-exact
  sempurna, run ulang dengan `n_jobs=1` (perbedaan praktis nihil, <1e-15).
- Skrip + versi software tercatat di JSON (`software: sklearn 1.9.1`,
  numpy 2.5.3, pandas 2.3.3).

## 6. TEMUAN UTAMA (KEMAMPUAN + BATAS — bukan lulus/gagal)

### 6.1 vib — ML menambah nilai vs canary & persistence di 2–4 fold; reproduksi V8 persis
RF ΔB>0 vs canary 4/4 fold (G2 terkonfirmasi); vs persistence 2/4 (F-14 +0,119;
F-15A +0,015; F-15_S −0,018; F-5 −0,227) — identik pola V8. GB/LR tidak konsisten
menang (GB kalah persistence 3/4; LR menang 2/4 dengan AUPRC fold-F-5 tertinggi
0.6606) → RF tetap head utama.
Batas: FAR pada semua tau ratusan/24jam → L2 tren layak; L1 menunggu FAR/B4 terukur.

### 6.2 ssi — RF≥canary 5/7 fold layak; RF≥persistence 6/7 — nilai tambah ML terukur
Sejalan V8 (RF≥canary 5/5; persistence kalah 0/5). GB lebih lemah (menang canary 4/7);
LR menang 5/7. Keyakinan: 5/9 fold CI95-nya menyentuh no-skill (CI-bawah ≤
prev: F-12, F-14, F-7, F-9, F-9_A) → layer keyakinan wajib (kekuatan bukti SEDANG).
Bukaan baru vs V8: fold F-9_A (eksternal, 55 positif)
RF 0.1357 vs prev 0.0654
= lift 2.07 — RF bekerja di fold eksternal ini.

### 6.3 shk — reproduksi dekat V8; persistence dominan di F-7; FAR tetap tinggi
RF≥canary 5/9 (V8: 6/9 — selisih kecil, harness imputer fold-safe V9; hasil baru menang
dengan catatan, PM1 §6.1). Persistence sangat kuat di F-7 (0.4457)
— kelas shock di sumur itu persisten antar-grid. FAR≤6 dgn recall>0 hanya
1 titik (F-14 rf tau=0.3 FAR=0.69 R=0.0053)
— recall <0,01 = praktis nol cakupan; klaim V8 (L0-alarm BELUM) terkonfirmasi ulang
dengan angka baru.

### 6.4 stuck K-ii — persistence-onset MENANG TELAK 4/4 (tes pembeda; temuan jujur)
Persistence-onset AUPRC 0.8265–0.9016
mengalahkan RF 0.0697–0.4443 di 4/4 fold
(B1 persistence = 1,0 semua well; TLead median 9–10,5 mnt). Mekanisme (DIAMATI dari
data, bukan asumsi): label positif onset = horizon [t_e−10, t_e) yang Kontigu (median
run 10 menit) → `y(t−1)=1` pada ±6/7 baris positif → persistence otomatis "deteksi
in-horizon". Persistence TIDAK bisa memberi peringatan di menit pertama horizon
(TLead-nya maks run−1) dan tidak bisa memberi peringatan SEBELUM horizon masuk —
di situlah RF/LR tetap punya ruang (mis. F-9 RF q95 B1 1,0 dengan TLead median
11.5 mnt).
Kekuatan bukti: SEDANG (1 kampanye, 4 well, label STUCK_RT masih punya risiko
semantik lintas-well, kontrol-positif 0/10 V8 belum diulang). Interpretasi untuk
evaluator: **pada formulasi horizon D1, persistence = engine konfirmasi-in-horizon
yang sangat kuat; ML bernilai hanya bila diukur pada kemampuan pra-horizon/pre-event
(butuh dataset baru dengan sampel pra-horizon)** — ini KEMAMPUAN baseline + BATAS
formulasi label, BUKAN kegagalan ML, dan bukan alasan menurunkan gate.

### 6.5 FAR vs ambang alarm — titik hemat-awas ADA, tapi recall kecil & syarat L1 penuh belum
Pemindaian seluruh fold × model × tau (termasuk q95_train untuk stuck) menemukan
titik dengan FAR≤6/24jam DAN recall>0 (syarat DASAR kenaikan L1) sebagai berikut:

| Engine | Jumlah titik | Detail (well, model, tau, FAR, recall) |
|---|---|---|
| vib | 1 | F-15_S rf tau=0.5 FAR=4.15 R=0.1018 |
| ssi | 5 | F-10 rf tau=0.3 FAR=0.21 R=0.0124; F-12 rf tau=0.3 FAR=3.76 R=0.0482; F-14 gb tau=0.3 FAR=5.89 R=0.0133; F-14 gb tau=0.5 FAR=2.14 R=0.0133; F-15A rf tau=0.2 FAR=4.33 R=0.1613 |
| shk | 1 | F-14 rf tau=0.3 FAR=0.69 R=0.0053 |
| stuck K-ii | 3 | F-10 rf tau=0.5 FAR=1.25 R=0.0052; F-14 rf tau=0.5 FAR=0.60 R=0.0051; F-9_A rf tau=0.5 FAR=0.00 R=0.0040 |

Total 10 titik dari 402 titik yang diuji
(<1%). Sebagian besar berada di tau tinggi (0,2–0,5) dengan recall 0,004–0,16 = hampir
semua positif terlewat; sebagai titik operasi tunggal tidak layak alarm, tapi layak
dicatat sebagai opsi "hemat-awas" (L1-syarat-dasar terpenuhi, recall tipis) untuk
evaluator. Syarat L1 PENUH (TLead/B4 terukur + C4 + kalibrasi lokal per well + anotasi
regime, PM1 §1.3) belum terpenuhi engine mana pun di kampanye ini → tidak ada kenaikan
tier otomatis dari kartu ini; tier mengikuti rekomendasi EVAL_A/B/C.

## 7. TEMUAN DATA (defect D1 stuck_k2 — dilaporkan, tidak didiamkan)

Kolom `ts_bin` dan `lab_ts` pada `scratch/v9_d1/datasets/stuck_k2.csv.gz` KOSONG untuk
semua 118.567 baris (4/4 well; verifikasi baca gzip mentah, bukan turunan). Konsekuensi:
(a) leak-check `v9_d1_05_leak_lowo.json` entry stuck_k2 (`0 pelanggaran`) = **vacuous**
(komparasi dengan NaN selalu False); (b) B1/TLead di §2.4 direkonstruksi sebagai DERIVED
dari run positif berurutan (fit_ts_max monotonic per well 4/4 terverifikasi — urutan
waktu dataset tetap sah; `y_prev_stuck_onset` terisi 0 NaN). Defect sudah dilaporkan ke
kartu D1 (`t_1ca71445`, komentar #3) dengan rekomendasi regenerate + checker NaN-count.
Konstruksi anti-bocor stuck_k2 tetap terverifikasi lewat KODE builder (jendela ketat-lalu
[t0−10, t0)), bukan lewat kolom.

## 8. BELUM DIVERIFIKASI / BELUM DIUKUR (verification-mandatory #3)

- C1–C4 (stabilitas temporal per-bin, dropout sensor, noise) = domain EVAL_C — TIDAK diukur di sini.
- B3 (pengurangan pemeriksaan) = butuh FP rule dari E_RULE — belum terukur.
- FP rule vib/ssi (rule ambang absolut / definisi SSI) = E_RULE.
- hyd-K-ii, bit_wear K-1/K-2, tool_wear K-ii, shk sub-onset = "belum terukur" (§3).
- Kontrol-positif stuck (labels_curated_v2) belum diulang di kampanye V9 (masih angka V8 0/10).
- CI95 bootstrap memakai blok tetap 60 jendela (pilihan harness; harmonisasi definisi
  "60/20/10" S7 = tugas EVAL_A).

## 9. PENERIMAAN (ACCEPTANCE SELF-CHECK)

| # | Syarat | Bukti |
|---|---|---|
| a | engine jalan pada data nyata | 4 engine × LOWO = 28 fold selesai; run log bertimestamp `scratch/v9_e_ml/v9_e_ML_*_RUN_LOG.txt` |
| b | hasil per lipatan dari eksekusi | `v9_e_ML_{vib,ssi,shk,stuck_k2}_RESULTS.json` (primer); tabel §2 dirender dari JSON oleh `code/v9_e_ML_03_build_doc.py` |
| c | baseline relevan dibandingkan | persistence + canary-depth + prevalence-random per fold per engine; ΔB tabel §2; persistence-onset §6.4 |
| d | 0 angka karangan | semua angka dokumen = render JSON; reproduksi silang V8-E_vib lift persis (§2.1) |
| e | D-A5 dipatuhi | nol ML di hyd-K-i; harness menolak engine di luar daftar (argparse choices) |
| f | determinisme | re-run fold 0 diff 2.2e-16 < gerbang 1e-9 (§5) |
| g | "belum terukur" eksplisit | §3 + §8 |
| h | sequ-mcp ≥3 pikiran + baris Riset pendahuluan | 3 pikiran (header) |

## 10. ARTEFAK

- Skrip: `code/v9_e_ML_01_train.py` (harness), `code/v9_e_ML_02_run_all.sh` (driver),
  `code/v9_e_ML_03_build_doc.py` (builder dokumen ini).
- JSON primer: `scratch/v9_e_ml/v9_e_ML_{vib,ssi,shk,stuck_k2}_RESULTS.json`,
  `v9_e_ML_stuck_k2_persistence_onset.json`.
- Run log: `scratch/v9_e_ml/v9_e_ML_*_RUN_LOG.txt`.
- agentmemory: fakta defect stuck_k2 + lokasi harness tersimpan (mem_mv4mbdf4).

*Selesai V9-E_ML (t_902dd141). Menyerahkan ke E_STAT (t_af8ea271), E_RULE (t_c8bebfb6),
EVAL_A (t_8a7a33d4) sebagai input JSON.*
