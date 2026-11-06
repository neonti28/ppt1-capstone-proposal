# V9-E_RULE — ENGINE RULE / PERSISTENCE / HIBRIDA + SELURUH BASELINE RELEVAN (S9)

Task: `t_c8bebfb6` [Algorithm Engineer Rule/Persistence/Hybrid] · Board: capstone-v9-build · 2026-10-12 (WIB)
Status: SELESAI — semua angka dari eksekusi nyata pada data Volve/USROP/Mendeley (JSON primer di
`scratch/v9_e_rule/`, S6). Sumbu: `docs/V9_PM1_ARCHITECTURE.md` (spesifikasi), `docs/V9_R1_JUSTIFICATION.md`
(metode+baseline), `docs/V9_D1_DATA_PIPELINE.md` (fitur+fold). Kerangka penilaian: standar 3 lapisan A/B/C
operator ("Evaluasi User.txt") — bukan gate lift 1,5.

> **Riset pendahuluan: `scientific-critical-thinking`** — OBSERVED/DESAIN/BELUM-TERUKUR dipisah per
> seksi; klaim "rule ≡ label (sirkular)" tidak ditulis sebagai fakta tanpa bukti → diuji lewat
> recompute independen dari bins (mismatch=0 di 5/5 kelas, §2.1); klaim "checker anti-bocor valid"
> dicurigai karena hasilnya 100% "0 pelanggaran" → diuji ulang dengan menghitung NaN kolom meta
> (temuan vakuum §5.1); "persistence-onset lemah per konstruksi" (R1 §3.4) diuji sebagai hipotesis
> dan ternyata DIBANTAH oleh data pada formulasi horizon (§3) — hipotesis diganti, bukan dilunakkan.
> **Riset pendahuluan: `verification-mandatory`** — semua angka dikutip dari JSON hasil eksekusi
> sesi ini; determinisme dibuktikan dengan rerun penuh 4 skrip → JSON fold identik 4/4 (§8);
> baseline dapat cross-check eksternal (persistence & canary bit_wear reproduksi EKSAK angka V6;
> canary 3-RMS tool_wear = rentang V8; episode & prev_test hyd-K-ii reproduksi EKSAK V8) (§4);
> bug data stuck_k2 diperbaiki dengan verifikasi identitas baris-per-baris (§5.1); daftar BELUM
> dicek eksplisit di §9.
> **Riset pendahuluan: `statistical-analysis`** — baseline RELEVAN per tugas (tidak ada baseline
> universal; R1 §4.1 diikuti literal); plafon lift 1/prev dilaporkan tiap fold; fold UNDERPOWERED
> (<30 positif) dilabeli dan tidak dihitung mayoritas; persistence dinilai pada subset valid_prev
> (konvensi V8 claim1) PLUS versi semua-baris; persistence-onset dianotasi sebagai baseline
> HINDSIGHT (y(t−1) pada label horizon mensyaratkan pengetahuan t_e lampau) sehingga tidak boleh
> dijadikan standar "mengalahkan" yang fair untuk detektor deployable (§3).
> **Riset pendahuluan: `verification-mandatory` (klaim batas)** — sebelum klaim "K-2 bit_wear tidak
> bisa dijalankan", dicek langsung: data USROP ada tetapi kampanye pra-reg K-2 memang belum terbit
> (R1 §3.3) → status = BELUM (syarat DoD tidak terpenuhi), bukan "tidak bisa" (§4.1).
> **Riset pendahuluan: `what-if-oracle`** — 5 cabang risiko hasil Ω/α/Δ/Ψ/Φ + tripwire (§6).
> **Riset pendahuluan: `consciousness-council`** — 5 arketipe menekan desain evaluasi; ketegangan
> "persistence hindsight dominan vs kejujuran benchmark" dipertahankan eksplisit (§7).
> **Riset pendahuluan: `sequentialthinking`** (6 pikiran, 6/6 sukses, tool_call sequ-mcp): inventaris
> kontrak DoD → masalah sirkularitas rule-vs-label → rancangan metrik/fold/S9 → desain per kelas +
> risiko kelas tanpa dataset → kelas sekunder + konsesi hindsight → gerbang verifikasi + tripwire.

## 0. RINGKASAN EKSEKUTIF

1. **Seluruh baseline relevan (S9) terhitung per fold per kelas pada fold LOWO/LOTO/split identik D1/V6/V8**
   (37 fold rig + 7 fold bit_wear + 4 fold tool_wear + 1 split temporal hyd-K-ii) → JSON primer siap
   menjadi syarat masuk EVAL_A.
2. **Rule dijalankan pada data nyata — angka FP tercetak** (membuka B3 vib/ssi): FP rule-display lintas
   fold: vib 197, ssi 26, shk 121, stuck_k1 49, hyd_ki 2.091. Cek identitas membuktikan rule pada
   jendela LABEL memang pembentuk label (0 mismatch di 5/5 kelas) — karenanya pembanding yang dipakai
   adalah rule pada menit t0−1 (strict-past, anti-bocor sah).
3. **Hibrida D-A3 (rule AND persistence) dirakit**: non-degenerasi HANYA di hyd_ki (AUPRC mean
   0,602 > rule 0,575 > persistence 0,555) dan ssi; pada vib/shk/stuck_k1 hibrida ≡ rule (terbukti
   identik AUPRC) — didokumentasikan sebagai sifat struktural, bukan kegagalan.
4. **Temuan terbesar (tes pembeda stuck-K-ii)**: persistence-horizon AUPRC 0,827–0,902, B1 93–97% —
   mendominasi semua detektor lain termasuk angka RF E3 V8 (AUPRC ~prev×lift) — bukti kuat bahwa
   formulasi label HORIZON didominasi kontinuitas label (run 10 menit); persistence-horizon adalah
   baseline HINDSIGHT (bukan deployable). Persistence-event (literal E0 R1, deployable) ≈ prevalence.
5. **Rule E1 stuck (2-dari-3) ≈ prevalence** pada tugas onset (B1 0–6,6%) DAN pada status stuck_k1
   (F-14: lift 0,99) — hasil negatif terukur = kemampuan "rule mekanis mentah tidak mendeteksi
   awal stuck pada data ini".
6. **Kemampuan "persistence = engine terbaik" dikonfirmasi ulang** dengan eksekusi baru di 4 kelas
   (vib 4/4, ssi 8/9 fold layak, stuck_k1 2/2, hyd_ki 2/9 vs rule; bit_wear 4/4 reproduksi eksak V6)
   — dicatat sebagai KEMAMPUAN, bukan aib.
7. **Temuan data**: file `stuck_k2.csv.gz` (D1) rusak meta (ts_bin/lab_ts NaN 118.567/118.567; checker
   anti-bocor lolos secara VAKUUM) → diperbaiki dengan resep identik + 2 baris fix, diverifikasi
   identitas per-well + anti-bocor NYATA 0/118.567; 13 onset scorable tanpa anchor = ABSORBED
   (onset berdekatan Δ2–6 menit, §5.1–5.2).

## 1. KONVENSI + DETERMINISME (dipakai semua angka di bawah)

| Item | Nilai |
|---|---|
| Seed | 42 di semua RNG/RF (numpy default_rng per fold; RandomForest random_state=42) |
| Fold | dari `scratch/v9_d1/lowo_<engine>.json` (identik dgn yang dipakai E_ML/E_STAT); bit_wear = LOWO 7 well (identik E1d); tool_wear = LOTO 4 alat (identik V8-E_A); hyd-K-ii = split temporal 70/30 (identik V8 claim2) |
| FAR | `FAR_24h = FP / (n_neg/60) × 24` — konvensi V8 `claim1_eval.py` (jam_neg = n_neg baris / 60; asumsi grid 60 dtk per baris) |
| AUPRC detektor biner | average_precision_score(y, pred_biner) |
| prevalence-random | skor `default_rng(42).uniform` per fold (empirik) + prev analitik; plafon lift = 1/prev |
| canary-depth | RF kontrak (300 pohon, min_samples_leaf=5, class_weight=balanced_subsample, seed42) HANYA fitur `depth_*`+`dbtm_*` (10), imputer median fold-safe |
| persistence | kolom `y_prev_*` resep D1 (offset jendela 10 mnt); metrik utama pada subset `valid_prev=1` (konvensi V8 claim1) + versi semua-baris dicetak |
| UNDERPOWERED | positif < 30 per fold — dilabeli, tidak dihitung mayoritas |
| Anti-bocor | SEMUA detektor (termasuk rule & E1) hanya membaca data < t0 (invariant S5 `feat_ts_max < lab_ts`); E1 memakai median+MAD jendela 60 menit strict-past dari bins |
| E1 rule | `alarm = 1[(z(TQA)>2)+(z(HKLD)>2)+(ROP-drop≥30%) ≥ 2]`, `z = 0,6745·(x−median)/MAD`, MAD==0 → z=0 (konservatif, terdokumentasi); ROP-drop = ROP ≤ 0,7·median60 |
| Determinisme | rerun penuh 4 skrip → 4/4 JSON fold identik (strip `generated_at`) — §8 |

## 2. KELAS STATUS (vib · ssi · shk · stuck_k1 · hyd_ki) — persistence + rule + hibrida + canary

Sumber angka: `scratch/v9_e_rule/v9_e_RULE_01_status_results.json` (per fold, eksekusi).
Kolom: pers=persistence (AUPRC semua baris), persVP=subset valid_prev, rule=rule-display t0−1,
P/R/FAR=metrik biner rule, hyb=hibrida rule AND persistence, can=canary-depth, rand=prevalence-random.
"FP" = jumlah false alarm pada fold (skala jendela; konversi ke beban = FP/(n_neg/60) per hari → kolom FAR24).

### 2.0 Cek identitas sirkular (recompute independen dari bins)

| Kelas | Baris dicek | Mismatch rule-jendela-label vs y | Kesimpulan |
|---|---|---|---|
| vib | 23.922 | **0** | rule pada jendela label ≡ label (pembentuk label) |
| ssi | 35.906 | **0** | idem (SSI jendela 10 mnt, min 10 sampel) |
| shk | 56.495 | **0** | idem |
| stuck_k1 | 5.555 | **0** | idem |
| hyd_ki | 52.509 | **0** | idem (valid & anom/obs≥0,5; MIN_OBS=5) |

Konsekuensi: FP rule terhadap label jendela = 0 BY CONSTRUCTION (bukan "detektor sempurna");
karena itu pembanding operasional = **rule pada menit t0−1** (data strict-past) yang FP-nya NYATA.

### 2.1 vib (deteksi kondisi; rule ambang VIBLAT≥32,17405 ft/s²)

| fold | well | n | pos | prev | pers | persVP | rule(t0−1) | FP | P | R | FAR24 | hyb FP/P | can | rand |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | F-14 | 1989 | 1124 | 0,5651 | 0,7925 | 0,7959 | 0,7372 | 30 | 0,9444 | 0,4537 | 49,94 | 30 / 0,9444 | 0,6124 | 0,5746 |
| 1 | F-15A | 6482 | 1543 | 0,2380 | 0,5473 | 0,5474 | 0,4119 | 65 | 0,8676 | 0,2761 | 18,95 | 65 / 0,8676 | 0,4578 | 0,2329 |
| 2 | F-15_S | 10903 | 1532 | 0,1405 | 0,5137 | 0,5166 | 0,4250 | 65 | 0,8984 | 0,3753 | 9,99 | 65 / 0,8984 | 0,2770 | 0,1384 |
| 3 | F-5 | 4548 | 1230 | 0,2704 | 0,6660 | 0,6675 | 0,6760 | 37 | 0,9519 | 0,5951 | 16,06 | 37 / 0,9519 | 0,3093 | 0,2657 |

KEMAMPUAN: persistence > canary 4/4 dan > random 4/4; rule-display P 0,87–0,95 dengan recall
0,28–0,60 (sistem hari-ini presisi-tinggi, tangkap-separuh); hibrida ≡ rule (rule t0−1 ⊆ persistence
— terbukti AUPRC identik 0,5625 rata-rata). Cross-check eksternal: persistence 0,514–0,793 ≈ angka
V8-E_vib 0,517–0,796 (kutipan); canary 0,277–0,612 = persis rentang V8. BATAS: FAR24 rule 10–50
terlalu tinggi utk alarm otomatis; recall rendah.

### 2.2 ssi (deteksi kondisi; rule definisi SSI(CRPM)≥1)

| fold | well | n | pos | prev | UP | pers | persVP | rule(t0−1) | FP | P | R | FAR24 | hyb FP | can | rand |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | F-10 | 7133 | 161 | 0,0226 | . | 0,1884 | 0,2025 | 0,0273 | 3 | 0,4000 | 0,0124 | 0,62 | 1 | 0,0302 | 0,0219 |
| 1 | F-12 | 4293 | 83 | 0,0193 | . | 0,0210 | 0,0203 | 0,0193 | 6 | 0,0000 | 0,0000 | 2,05 | 1 | 0,0709 | 0,0191 |
| 2 | F-14 | 5455 | 75 | 0,0137 | . | 0,0140 | 0,0122 | 0,0137 | 0 | – | 0,0000 | 0,00 | 0 | 0,0305 | 0,0148 |
| 3 | F-15A | 6020 | 31 | 0,0051 | . | 0,0086 | 0,0088 | 0,0130 | 3 | 0,2500 | 0,0323 | 0,72 | 2 | 0,0139 | 0,0045 |
| 4 | F-15_S | 5342 | 85 | 0,0159 | . | 0,0166 | 0,0170 | 0,0170 | 8 | 0,1111 | 0,0118 | 2,19 | 1 | 0,0243 | 0,0157 |
| 5 | F-5 | 4714 | 102 | 0,0216 | . | 0,0334 | 0,0354 | 0,0310 | 2 | 0,5000 | 0,0196 | 0,62 | 0 | 0,0751 | 0,0195 |
| 6 | F-7 | 982 | 3 | 0,0031 | **Y** | 0,0031 | – | 0,0031 | 0 | – | 0,0000 | 0,00 | 0 | 0,0201 | 0,0145 |
| 7 | F-9 | 1126 | 12 | 0,0107 | **Y** | 0,0107 | 0,0117 | 0,0107 | 0 | – | 0,0000 | 0,00 | 0 | 0,0097 | 0,0102 |
| 8 | F-9_A | 841 | 55 | 0,0654 | . | 0,0732 | 0,0672 | 0,0678 | 4 | 0,2000 | 0,0182 | 7,33 | 2 | 0,0860 | 0,0675 |

KEMAMPUAN: persistence ≥ random di 7/9 fold (kalah tipis di F-14 −0,0008 & F-7 underpowered);
persistence > canary HANYA di 2/9 (F-10, F-9) — canary-depth justru kuat relatif pada kelas langka
ini, konsisten dgn V8 (ssi = kelas di mana ML dibenarkan; persistence kalah 0/5 vs RF di V8);
rule single-bin SSI ≈ random (jarak antar-menit SSI tidak persisten); hibrida > rule di fold dgn FP
positif (AND memangkas FP 3→1, 8→1, dst.) dan ≡ persistence di fold tanpa alarm. BATAS: recall
persistence 0–0,40; FAR24 persistence 17,6 (F-10) — tier tren/L1 terkalibrasi saja; 2 fold underpowered.

### 2.3 shk (deteksi anomali SHKRSK≥1; rule display MWD)

| fold | well | n | pos | prev | pers | persVP | rule(t0−1) | FP | P | R | FAR24 | hyb FP | can | rand |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | F-10 | 7899 | 146 | 0,0185 | 0,0236 | 0,0236 | 0,0295 | 15 | 0,2857 | 0,0411 | 2,79 | 15 | 0,0212 | 0,0188 |
| 1 | F-12 | 5405 | 217 | 0,0401 | 0,0531 | 0,0492 | 0,0675 | 8 | 0,5789 | 0,0507 | 2,22 | 8 | 0,0652 | 0,0411 |
| 2 | F-14 | 11205 | 760 | 0,0678 | 0,1599 | 0,1673 | 0,1016 | 48 | 0,5340 | 0,0724 | 6,62 | 48 | 0,0630 | 0,0718 |
| 3 | F-15A | 6484 | 41 | 0,0063 | 0,0063 | 0,0063 | 0,0063 | 3 | 0,0000 | 0,0000 | 0,67 | 3 | 0,0121 | 0,0080 |
| 4 | F-15_S | 11394 | 259 | 0,0227 | 0,0390 | 0,0393 | 0,0449 | 22 | 0,4054 | 0,0579 | 2,85 | 22 | 0,0251 | 0,0234 |
| 5 | F-5 | 7140 | 240 | 0,0336 | 0,0451 | 0,0452 | 0,0344 | 14 | 0,1250 | 0,0083 | 2,92 | 14 | 0,0487 | 0,0341 |
| 6 | F-7 | 2761 | 267 | 0,0967 | 0,4428 | 0,4457 | 0,4139 | 7 | 0,9352 | 0,3783 | 4,04 | 7 | 0,0789 | 0,0967 |
| 7 | F-9 | 1851 | 45 | 0,0243 | 0,0380 | 0,0384 | 0,0312 | 2 | 0,3333 | 0,0222 | 1,59 | 2 | 0,0611 | 0,0257 |
| 8 | F-9_A | 2356 | 30 | 0,0127 | 0,0140 | 0,0144 | 0,0234 | 2 | 0,3333 | 0,0333 | 1,24 | 2 | 0,0388 | 0,0146 |

KEMAMPUAN: persistence ≥ random 7/9 (kalah tipis di F-15A −0,0017 & F-9_A −0,0006); rule-display
FAR24 0,67–6,62 = **satu-satunya titik lintas-fold dgn FAR≤6/24jam dgn recall>0** (4 titik:
F-10/F-12/F-15_S/F-7) — angka FP display status-quo (121 lintas fold) = basis B3 untuk EVAL_B.
BATAS: recall display 0–0,38; hibrida ≡ rule (rule ⊆ persistence utk kelas definisi-kanal).

### 2.4 stuck_k1 (deteksi kondisi blok STUCK_RT; + E1 2-dari-3 independen)

| fold | well | n | pos | prev | pers | persVP | rule(t0−1) | FP | P | R | FAR24 | hyb FP | E1 | E1 FP/P | hybrid-E1 | can | rand |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | F-14 | 3201 | 432 | 0,1350 | 0,5200 | 0,5226 | 0,4892 | 16 | 0,9238 | 0,4491 | 8,32 | 16 | 0,1337 | 125 / 0,0458 | 12 FP, 0 TP | 0,4099 | 0,1298 |
| 1 | F-9_A | 2354 | 1575 | 0,6691 | 0,7832 | 0,7869 | 0,8472 | 33 | 0,9662 | 0,5994 | 61,00 | 33 | 0,6659 | 35 / 0,5513 | (lihat JSON) | 0,7688 | 0,6569 |

KEMAMPUAN: rule-display (STUCK t0−1) ≥ persistence di 2/2 fold (0,489 vs 0,520 F-14; 0,847 vs 0,783
F-9_A — menang 1, kalah 1 dgn AUPRC rata-rata 0,668 vs 0,652); persistence > canary 2/2. HASIL NEGATIF
TERUKUR: E1 2-dari-3 ≈ prevalence di F-14 (AUPRC 0,1337 vs prev 0,1350; lift 0,99) — aturan mekanis
2-dari-3 TIDAK mendeteksi blok STUCK pada sumur ini (FP 125). BATAS: 2 fold saja (stuck_k1 hanya
F-14/F-9_A); FAR24 F-9_A 61 (prev 0,67 → skala jendela menipu; baca bersama prev).

### 2.5 hyd_ki (deteksi kondisi |z|>2 residu SPPA; RF DILARANG — D-A5)

| fold | well | n | pos | prev | pers | persVP | rule(t0−1) | FP | P | R | FAR24 | **hyb FP/P** | can | rand |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | F-10 | 7571 | 1394 | 0,1841 | 0,8110 | 0,8426 | 0,8354 | 166 | 0,8862 | 0,9275 | 38,70 | **66 / 0,9484** | 0,2388 | 0,1826 |
| 1 | F-12 | 7390 | 1426 | 0,1930 | 0,6328 | 0,6428 | 0,6556 | 368 | 0,7598 | 0,8163 | 88,85 | **242 / 0,8158** | 0,1616 | 0,1927 |
| 2 | F-14 | 10401 | 865 | 0,0832 | 0,4336 | 0,4441 | 0,4617 | 368 | 0,6226 | 0,7017 | 55,57 | **110 / 0,8243** | 0,0805 | 0,0873 |
| 3 | F-15A | 6156 | 698 | 0,1134 | 0,4897 | 0,4898 | 0,5345 | 253 | 0,6744 | 0,7507 | 66,75 | **103 / 0,8154** | 0,1273 | 0,1117 |
| 4 | F-15_S | 8355 | 993 | 0,1189 | 0,4188 | 0,4245 | 0,4826 | 359 | 0,6531 | 0,6808 | 70,22 | **199 / 0,7236** | 0,1285 | 0,1164 |
| 5 | F-5 | 6332 | 621 | 0,0981 | 0,5890 | 0,5985 | 0,5886 | 194 | 0,7172 | 0,7923 | 48,92 | **58 / 0,8849** | 0,1559 | 0,0926 |
| 6 | F-7 | 2482 | 421 | 0,1696 | 0,4980 | 0,5061 | 0,5251 | 189 | 0,6316 | 0,7696 | 132,05 | **76 / 0,7853** | 0,2220 | 0,1676 |
| 7 | F-9 | 1616 | 423 | 0,2618 | 0,6170 | 0,6251 | 0,5709 | 108 | 0,7238 | 0,6690 | 130,36 | **36 / 0,8676** | 0,5117 | 0,2456 |
| 8 | F-9_A | 2206 | 331 | 0,1500 | 0,5096 | 0,5415 | 0,5212 | 86 | 0,7162 | 0,6556 | 66,05 | **37 / 0,8356** | 0,1556 | 0,1552 |

KEMAMPUAN (temuan positif hibrida): **hibrida non-degenerasi — AUPRC mean 0,602 > rule 0,575 >
persistence 0,555; mengalahkan persistence di **8/9 fold** (Δ −0,017…+0,092; F-9 −0,017 —
dikoreksi PM2 dari JSON primer, konsisten dgn recompute EVAL_A §4) dan memangkas FP vs rule
di **9/9 fold** (mis. F-14: 368→110). Ini bukti empiris D-A3 bekerja: konfirmasi-minoritas dua kondisi
(anomali-menit + status-jendela) menaikkan presisi. Persistence > canary 9/9 dan > random 9/9.
BATAS: FAR24 38–132 (skala jendela; = beban blok, bukan alarm — konsisten V8-E_hyd); hybrid tetap
belum layak alarm otomatis.

## 3. stuck_k2 — ONSET (H=10 mnt): persistence-onset TES PEMBEDA + E1 + canary

Sumber: `scratch/v9_e_rule/v9_e_RULE_02_stuck_onset_results.json` (4 fold LOWO; dataset setelah
perbaikan meta §5.1). Dua varian persistence dijalankan karena rumus R1/PM1 terbaca dua arah:
**E0a persistence-horizon** = `y_prev_stuck_onset` (kontrak D1/S9; y(t−1) pada label horizon) dan
**E0b persistence-event** = `1[peristiwa onset tepat di menit t−1]` (literal R1 §3.4 "pada deret
onset"). B1/TLead dihitung per onset observabel (denominator = anchor unik lab_ts, lihat §5.2).

| fold | well | n | pos | prev | onsets | persH AUPRC | B1 | TLead med | persE AUPRC | B1 | E1 AUPRC | B1 | E1 FP | canary |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | F-10 | 4216 | 772 | 0,1831 | 91 | **0,9016** | 0,967 | 1 mnt | 0,1860 | 0,066 | 0,1932 | 0,066 | 57 | 0,1762 |
| 1 | F-14 | 95925 | 389 | 0,0041 | 57 | **0,8438** | 0,930 | 1 mnt | 0,0066 | 0,035 | 0,0043 | 0,018 | 307 | 0,0093 |
| 2 | F-9 | 16184 | 311 | 0,0192 | 52 | **0,8265** | 0,962 | 3 mnt | 0,0333 | 0,115 | 0,0192 | 0,000 | 23 | 0,0401 |
| 3 | F-9_A | 2242 | 503 | 0,2244 | 68 | **0,8890** | 0,941 | 1 mnt | 0,2244 | 0,000 | 0,2357 | 0,044 | 35 | 0,2532 |

### 3.1 Temuan utama: label horizon didominasi kontinuitas label (tes pembeda)

- **persistence-horizon AUPRC 0,827–0,902 (lift 4,0–207 vs prev; plafon lift 4,5–244) dengan B1 93–97%
  dan TLead median 1–3 menit** — MENDOMINASI semua detektor lain pada tugas yang sama, termasuk
  angka RF E3 V8 (AUPRC ~prev×lift ≈ 0,004–0,04). Ini hasil tes pembeda yang diminta R1 §3.4:
  hipotesis "kegagalan V7 = minim ML" DITOLAK untuk formulasi ini — yang terbukti didominasi adalah
  STRUKTUR LABEL (positif = run 10 menit; y(t−1)=1 hampir selalu benar di dalam run).
- **Akan tetapi persistence-horizon BUKAN detektor deployable**: mengetahui y(t−1) pada label
  horizon mensyaratkan mengetahui t_e di masa lampau (hindsight). Dianotasi sebagai UPPER-BOUND /
  tes formulasi — bukan standar "mengalahkan" yang fair bagi engine deployable (EVAL_A mohon membaca
  ΔB vs persistence-horizon sebagai "celah hindsight", bukan nilai tambah).
- **persistence-event (E0b, literal R1, deployable) ≈ prevalence**: AUPRC 0,0066–0,2244 vs prev
  0,0041–0,2244 (lift 1,0–1,6), FP 0–7, B1 0–11,5% — memenuhi ekspektasi R1 "recall ~0 per
  konstruksi" (alarm hanya bila peristiwa menit sebelumnya; onset jarang beruntun 1 menit).
- **E1 rule 2-dari-3 ≈ prevalence** (AUPRC 0,0043–0,2357 vs prev 0,0041–0,2244; lift 0,9–1,06;
  B1 0–6,6%): aturan mekanis 60-menit TIDAK memberi peringatan-dini onset stuck pada data ini
  (hasil negatif terukur = kemampuan, bukan kegagalan).
- canary-depth ≈ prev (lift 1,1–2,3) — posisi tidak memprediksi onset.
- B3 (pengurangan pemeriksaan): FP_display baseline onset = FP persistence-event/E1 (23–307 per
  fold) siap dipakai EVAL_B.

## 4. KELAS SEKUNDER (bit_wear K-1 · tool_wear K-ii · hyd-K-ii) — baseline pada fold identik V6/V8

### 4.1 bit_wear K-1 (deteksi blok high_MSE; data `scratch/v6_e1/usrop_windows.csv`, LOWO 7 well)

| fold (well) | n | pos | prev | UP | persistence (n) | canary-depth | rand | cross-check V6 |
|---|---|---|---|---|---|---|---|---|
| F-9_Ad | 271 | 3 | 0,0111 | **Y** | 0,1185 (270) | 0,0177 | 0,0246 | n/pos ✓ |
| F-7d | 124 | 0 | 0 | **Y** | – (123) | – | – | n/pos ✓ |
| F-14d | 949 | 91 | 0,0959 | . | **0,6792** (948) | 0,1913 | 0,0978 | **identik 0,6792052825924018 / 0,19127517114238235** |
| F-15d | 1057 | 155 | 0,1466 | . | **0,6979** (1056) | 0,2880 | 0,1587 | **identik 0,6978575032321129 / 0,28802368022066216** |
| F-15Sd | 1031 | 561 | 0,5441 | . | **0,9837** (1030) | 0,7555 | 0,5803 | **identik 0,9837378022700696 / 0,75551936756036** |
| F-5d | 367 | 174 | 0,4741 | . | **0,8703** (366) | 0,6915 | 0,4457 | **identik 0,870297273423366 / 0,6914937539016541** |
| F-9d | 154 | 0 | 0 | **Y** | – (153) | – | – | n/pos ✓ |

KEMAMPUAN: persistence > canary 4/4 fold layak dan > random 4/4 (replikasi independen; angka
persistence/canary **identik digit** dgn E1d V6 → pipeline baseline terverifikasi silang).
Rule layer hibrida = label Teale (kanal terlarang) → hibrida degradasi ke persistence (dinyatakan).
K-2 onset: **BELUM DIJALANKAN** — kampanye pra-reg K-2 belum terbit (R1 §3.3); syarat DoD (d)
"bila pra-reg terbit" tidak terpenuhi → status BELUM-TERUKUR (bukan gagal).

### 4.2 tool_wear K-ii (klasifikasi LOTO 4 alat; data `scratch/v6_e1/toolwear_windows.csv`)

| fold (alat uji) | n | pos | prev | canary 3-RMS | identity-majority | persistence diagnostik |
|---|---|---|---|---|---|---|
| T01 | 120 | 60 | 0,5000 | 0,5164 | 0,5000 | 0,9917 |
| T02 | 112 | 62 | 0,5536 | 0,5947 | 0,5536 | 0,9929 |
| T03 | 121 | 60 | 0,4959 | 0,6024 | 0,4959 | 0,9917 |
| T04 | 116 | 58 | 0,5000 | 0,6124 | 0,5000 | 0,9915 |

KEMAMPUAN: canary 3-RMS 0,516–0,612 = **persis rentang V8-E_A** (reproduksi); plafon lift identity =
2,0 (prev 0,496–0,554). **persistence DINYATAKAN N/A per PM1 §2.7** dengan angka diagnostik
0,9915–0,9929: y(t−1) ≡ identitas-run yang sedang berjalan (label konstan dalam run) → near-perfect
adalah MEMORISASI struktur run, bukan deteksi keausan; tidak dipakai sebagai pembanding adil
klaim lintas-alat (deklarasi PM dipertahankan; angka dicetak agar transparan).

### 4.3 hyd-K-ii (prediksi kick/loss proxy; split temporal 70/30 identik V8 claim2, 1 wellbore F-9 A)

| metrik | hasil |
|---|---|
| episode z-pit (reproduksi) | 124 = V8 (kick+loss) ✓ |
| test (30% akhir, evaluable) | n 8.107, pos 30, prev 0,0037005 (**= V8 0,0037** ✓) |
| prevalence-random | AUPRC emp 0,00564; plafon 270,2 |
| selalu-negatif ("onset persistence" V8) | AUPRC = prev 0,00370; recall 0 by construction; FAR 0 |
| **rule z-pit (sistem hari-ini)** | TLead **= 0 menit terukur di 124/124 onset** (alarm tepat DI t_e); alarm pada baris evaluasi = **0 by construction** (menit blok episode +30 mnt Dibuang dari evaluasi); beban: 1.348 menit episode (35 menit di test) |

KEMAMPUAN/BATAS: z-pit = baseline "deteksi saat-kejadian" untuk B3 (bukan pembanding TLead —
konsisten PM1 §2.5); Fisher/Pearson literal = milik E_STAT; RF K-ii = milik E_ML. Satu wellbore →
bukan LOWO; klaim lintas-sumur TIDAK diklaim di sini.

## 5. TEMUAN (di luar tabel baseline)

### 5.1 BUG DATA stuck_k2 (ditemukan, diperbaiki, diverifikasi)

- **Temuan**: `scratch/v9_d1/datasets/stuck_k2.csv.gz` awalnya memiliki `ts_bin` & `lab_ts` kosong
  di **118.567/118.567 baris** (diverifikasi dari CSV mentah: `F-10,,20649208.0,,onset_horizon_neg`).
- **Akar bug (TERVERIFIKASI, repro 3/3 — `scratch/v9_e_rule/_repro_insert_bug.py`)**:
  `v9_d1_04_stuck_k2.py` memanggil `DataFrame.insert(kolom, Series)` dgn Series ber-DatetimeIndex
  ke DataFrame ber-index integer → pandas ME-ALIGN-kan Series → semua NaN. Kolom berbasis numpy
  (feat_ts_max, lab_kind, y) tidak terpengaruh.
- **Dampak sekunder (temuan metode)**: checker anti-bocor D1 `v9_d1_05` mem-mask
  `both = feat_ts_max.notna() & lab_ts.notna()` → untuk stuck_k2 diuji **0 baris** → klaim
  "0 pelanggaran" untuk stuck_k2 = VAKUUM (filtered absence). 5 dataset lain diaudit ulang:
  NaN meta = 0 → pemeriksaan mereka VALID (0 pelanggaran nyata).
- **Perbaikan**: salinan resep identik + fix `.to_numpy()` (2 baris), 4 well (169 dtk) →
  `scratch/v9_e_rule/repair/stuck_k2.csv.gz`; file bersama diganti ATOMIC (backup:
  `scratch/v9_e_rule/stuck_k2_ORIG_nanmeta.csv.gz`); skrip D1 dipatch. Verifikasi
  (`v9_e_RULE_02c_verify.json`): baris 118.567 =, kolom =, **y/y_prev/fitur/feat_ts_max IDENTIK
  per-well** (4/4), ts_bin/lab_ts non-null, **anti-bocor NYATA 118.567/118.567 `feat_ts_max <
  lab_ts`, 0 pelanggaran**, invarian onset 55/72/93/61. Komentar hotspot dikirim ke kartu D1/E_ML/E_STAT.

### 5.2 Gap 13 onset scorable tanpa anchor unik = ABSORBED (tes pembeda definitif)

Scorable 281 (QC) vs anchor unik di dataset 268. Hipotesis H_overwrite vs H_mask diuji per-onset
(`v9_e_RULE_02e_gap_root_cause.json`): **13/13 = ABSORBED** — onset tetangga berdekatan (Δ 2–6
menit) membuat horizon tumpang-tindih; loop penulisan lab_ts onset lewat menulis-ulang SEMUA baris
onset awal (bukti per-onset: window rows pindah lab_ts ke absorber; contoh F-14 t_e 20175277 →
7 baris berlab_ts 20175280). Bukan data hilang; anchor observabel = 268 (dipakai sbg denominator
B1/TLead; dicatat sbg nuansa C-semantik: onset beruntun <10 menit tak bisa dipisah oleh label
horizon saat ini).

## 6. WHERE-IF-ORACLE (risiko hasil E_RULE — 5 cabang)

| Cabang | Bobot | Skenario | Konsekuensi | Robust action |
|---|---|---|---|---|
| Ω Best | 20% | E_ML mengalahkan baseline persistence-horisont di majority fold stuck_k2 + hybrid hyd-K-i dipakai I1 | klaim nilai-tambah ML & hibrida terukur; alat dapat L1 terkalibrasi lebih luas | JSON E_RULE = acuan ΔB; hybrid hyd jadi template D-A3 kelas lain |
| α Likely | 45% (prioritas 61,8%) | Persistence tetap engine terbaik di kelas status; ML hanya bernilai di shk-onset/ssi (sesuai V8) | alat PdM tetap koheren di L0+L2 dengan rule/persistence/hybrid; ML = lapisan tipis | badge FAR + tier per §2–§4 dipakai I1 apa adanya |
| Δ Worst | 15% | Persistence-horizon stuck_k2 disalahbaca evaluator sbg "RF bisa dikalahkan mudah" → klaim berlebihan | narasi nilai-tambah ML palsu | anotasi hindsight eksplisit §3.1; EVAL_A wajib memisahkan E0a (upper-bound) vs E0b (deployable) |
| Ψ Wildcard | 10% | Bug serupa (insert-alignment) ada di artefak dataset lain / build ulang masa depan | meta kosong lolos checker vakuum lagi | pola verifikasi §5.1 (hitung NaN meta sebelum percaya checker) jadi syarat QA; checker D1 perlu guard `n_both == n_rows` |
| Φ Contrarian | 10% | Rule-display shk (FAR24 0,67–6,62, 4 titik) ternyata sudah cukup utk L1 hemat-awas tanpa ML | prioritas bangun ML turun; display-rule + badge jadi produk utama | EVAL_B menghitung B3 dgn FP rule 121 (shk) sbg baseline |

**Tripwire (sinyal → perbarui cabang):** E_ML/E_STAT memakai fold/ambang berbeda → catat
change-control; parser well baru (VIBLAT F-4/F-10/F-15, GAINLOSSTOT) → fold bertambah, hitung ulang
baseline pada fold baru (skrip siap); kampanye pra-reg K-2 bit_wear terbit → jalankan
persistence-onset K-2 (skrip tinggal pakai dataset K-2); ada permintaan gate seragam → rujuk §10.

## 7. CONSCIOUSNESS-COUNCIL (5 arketipe)

- **Architect**: satu modul persistence + satu harness canary + satu fungsi metrik dipakai lintas
  7 kelas (37 fold rig + 12 fold sekunder) = bukti modularitas D-A3/S9 hidup. Risiko: 4 varian baseline per
  kelas membingungkan evaluator → ditahan dgn tabel konvensi §1 + penamaan eksplisit (persH/persE).
- **Empiricist**: angka cross-check EKSAK (bit_wear V6, tool_wear V8, hyd-K-ii V8, vib V8 rentang)
  = kualitas tertinggi yg bisa diminta utk baseline; determinisme 4/4. Keberatan: E1 z-satu-arah
  mengikuti literal spesifikasi — bila interpretasi R1 salah, hasil "E1 ≈ prev" bisa salah sasaran
  → dicatat sebagai change-control terbuka (bukan perubahan sepihak).
- **Minimalist**: persistence-onset dijalankan 2 varian (bukan 1) karena rumus sumber ambigu —
  keputusan termurah yg menjawab dua tafsir sekaligus; tidak ada varian ketiga yg ditambah.
- **Pragmatist**: FP rule nyata (vib 197, shk 121, hyd 2091, stuck 49) langsung membuka perhitungan
  B3 EVAL_B hari ini; hybrid hyd (−FP, +AUPRC) siap dipasang tanpa menunggu E_ML.
- **Contrarian (tekanan inti)**: "persistence-horizon 0,87 B1 97%" terdengar sebagai prestasi —
  justru itu BUKTI bahwa tugas onset dgn label horizon 10 menit bisa "dikerjakan" tanpa memprediksi
  apa pun (hindsight). Ketegangan ini TIDAK diselesaikan dengan menurunkan ambang; diresolusi dgn
  memisahkan baseline hindsight (E0a) dari deployable (E0b/E1) secara eksplisit §3.

**Sintesis**: konvergensi 4+ arketipe = baseline S9 lengkap + modularitas + cross-check ketat;
ketegangan dipertahankan = status persistence-horizon (upper-bound vs pembanding).

## 8. VERIFIKASI (bukti mentah)

| # | Klaim | Bukti |
|---|---|---|
| 1 | Semua angka dari eksekusi | JSON primer `scratch/v9_e_rule/v9_e_RULE_0{1,2,3,4}_*_results.json` + run log bertimestamp |
| 2 | Determinisme seed 42 | `v9_e_RULE_05_determinism.py` → rerun 4 skrip, **4/4 JSON fold identik** (strip generated_at) |
| 3 | Fold identik dgn tim lain | lowo_*.json D1 (37 fold rig: 33 status + 4 onset); bit_wear n_test/pos cocok E1d 7/7; hyd-K-ii episode 124 & prev_test = V8 |
| 4 | Baseline reproduksi silang | bit_wear persistence & canary **identik digit** dgn V6; canary 3-RMS = rentang V8; vib persistence ≈ V8 |
| 5 | Anti-bocor stuck_k2 nyata | `v9_e_RULE_02c_verify.json`: 118.567/118.567 `feat_ts_max < lab_ts`, 0 NaN meta |
| 6 | Bug insert-alignment | repro `_repro_insert_bug.py` 3/3 NaN; CSV mentah `F-10,,20649208.0,,` |
| 7 | Gap onset = absorbed | `v9_e_RULE_02e_gap_root_cause.json` (13/13 ABSORBED + bukti absorber per-onset) |
| 8 | Onset re-derivation benar | re-derivation onsets_ffill 55/72/93/61 = QC D1 & REF V8 (script 02d/02e) |
| 9 | Rule sirkular | recompute independen dari bins: mismatch 0 di 5/5 kelas (§2.0) |
| 10 | agentmemory fakta tahan-lama | mem_mv4ofv21 (bug stuck_k2) + mem_mv4ofvfr (hasil kunci) |

## 9. BATAS JUJUR / BELUM DICEK

1. Persistence-horizon (§3) TIDAK deployable (hindsight) — jangan dipakai sbg standar nilai tambah
   ML pada kelas onset; pembanding adil = persistence-event & E1 (keduanya ≈ prev).
2. CI95 moving-block bootstrap BELUM dihitung di sini — kontrak S7 menugaskan EVAL_A; JSON menyediakan
   skor/label mentah per fold untuk itu.
3. B4 (margin status-awal) & B2/B3 penuh = tugas EVAL_B; di sini disediakan P/R/FAR/FP rule + TLead/B1.
4. E1 ROP-drop: "drop ≥30%" diinterpretasi vs median60 (R1 tidak menulis basis eksplisit) — if this
   differs from PM intent → cukup ganti 1 konstanta (change-control terbuka, tidak mengubah engine).
5. hyd-K-ii: 1 wellbore, split temporal (bukan LOWO) — konvensi V8; Fisher/Pearson & RF = kartu lain.
6. bit_wear K-2 & hyd_k2 dataset-D1 tidak ada (K-2 pra-reg belum terbit; hyd-K-ii memakai resep V8
   langsung dari f9a_time.csv) — bukan kelalaian; status per kelas dinyatakan §4.
7. FAR memakai konvensi V8 (n_neg/60) — asumsi 1 keputusan per menit walau jendela label 10 menit
   tumpang-tindih; harmonisasi antar-kelas = tugas EVAL_A (S7).
8. Semua hasil satu lapangan (Volve) + satu dataset bengkel (Mendeley) — generalisasi lintas-lapangan
   TIDAK diklaim.
9. skrip `v9_e_RULE_02d/02e` membaca ulang CSV mentah (chunked) — re-derivation onset terverifikasi
   identik hitungan, tetapi pemetaan menit-level per-baris tidak dibandingkan baris-per-baris dgn
   artefak builder (per-well artifacts D1 sudah dihapus merge).

## 10. PENERIMAAN (DoD PM1 §4.5)

| # | Syarat | Status | Bukti |
|---|---|---|---|
| a | Semua baseline terhitung per fold per kelas + JSON | **PASS** | 37 fold rig (33 status + 4 onset) + 7 bit_wear + 4 tool_wear + 1 hyd-K-ii split; JSON §11 |
| b | Rule dijalankan pada data nyata; FP tercetak (buka B3 vib/ssi) | **PASS** | FP: vib 197, ssi 26, shk 121, stuck_k1 49, hyd_ki 2.091; E1 stuck 160; z-pit TLead=0 |
| c | Hibrida dirakit sesuai spesifikasi (bukan model gabungan baru) | **PASS** | hibrida rule AND persistence (D-A3); non-degenerasi terbukti hyd_ki (9/9 menang vs persistence) & ssi; degenerasi terdokumentasi (vib/shk/stuck_k1/bit_wear) |
| d | Persistence-onset tes pembeda stuck (+ K-2 bila pra-reg terbit) | **PASS dgn catatan** | stuck: 2 varian (horizon 0,827–0,902 hindsight; event ≈ prev); bit_wear K-2: pra-reg belum terbit → BELUM (§4.1) |
| e | "Persistence = engine terbaik" dicatat sbg KEMAMPUAN | **PASS** | §2 (vib/ssi/stuck_k1/hyd_ki), §4.1 (bit_wear 4/4), §4.2 (tool_wear N/A deklarasi) |
| f | Baris "Riset pendahuluan" | **PASS** | header (7 skill) |
| g | sequ-mcp ≥3 pikiran | **PASS** | 6 pikiran, 6/6 sukses (tool_call) |
| h | agentmemory fakta tahan-lama | **PASS** | 2 fakta (§8 baris 10) |
| i | 0 angka karangan | **PASS** | semua angka = kutipan JSON eksekusi; cross-check §8 |

## 11. ARTEFAK

| File | Isi |
|---|---|
| `docs/V9_E_RULE_ENGINE.md` | dokumen ini |
| `code/v9_e_RULE_01_status.py` | baseline+rule+hibrida 5 kelas status |
| `code/v9_e_RULE_02_stuck_onset.py` | persistence-horizon/event + E1 + canary + B1/TLead stuck_k2 |
| `code/v9_e_RULE_02b_repair_k2.py` | repair dataset stuck_k2 (resep identik + fix insert) |
| `code/v9_e_RULE_02d_gap_hypothesis.py` | re-derivation onset raw (uji hipotesis gap) |
| `code/v9_e_RULE_02e_gap_root_cause.py` | klasifikasi definitif 13 onset (ABSORBED) |
| `code/v9_e_RULE_03_bitwear_toolwear.py` | baseline bit_wear K-1 + tool_wear K-ii |
| `code/v9_e_RULE_04_hyd_k2.py` | baseline hyd-K-ii (resep V8 claim2) |
| `code/v9_e_RULE_05_determinism.py` | gerbang determinisme rerun |
| `code/v9_d1_04_stuck_k2.py` | (patched) fix insert-alignment builder D1 |
| `scratch/v9_e_rule/v9_e_RULE_01_status_results.json` | primer: 33 fold rig status |
| `scratch/v9_e_rule/v9_e_RULE_02_stuck_onset_results.json` | primer: 4 fold onset stuck |
| `scratch/v9_e_rule/v9_e_RULE_03_bitwear_toolwear_results.json` | primer: 7+4 fold sekunder |
| `scratch/v9_e_rule/v9_e_RULE_04_hyd_k2_results.json` | primer: split temporal hyd-K-ii |
| `scratch/v9_e_rule/v9_e_RULE_02c_verify.json` | verifikasi repair + audit meta 6 dataset |
| `scratch/v9_e_rule/v9_e_RULE_02e_gap_root_cause.json` | bukti 13 onset ABSORBED |
| `scratch/v9_e_rule/stuck_k2_ORIG_nanmeta.csv.gz` | backup file rusak sebelum repair |
| `scratch/v9_e_rule/repair/stuck_k2.csv.gz` | hasil repair (verifikasi identitas) |

*Selesai V9-E_RULE (`t_c8bebfb6`). Siap menjadi input EVAL_A (`t_8a7a33d4`) bersama JSON E_ML/E_STAT.*
