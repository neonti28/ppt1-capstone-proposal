# V8-E_stuck — EVALUASI KEMAMPUAN kelas `stuck` (KERANGKA 3 LAPISAN A/B/C)

Task: `t_d7fa8c16` [Evaluator] · Board: capstone-v8-capability · Tanggal: 2026-10-11 (WIB)
Kerangka: `docs/V8_R1_ABC_SPEC.md` §2.4 + §3.1 (mengganti gate biner V6/V7).
Status: HASIL UJI NYATA — kemampuan + batas pemakaian + kekuatan bukti. **BUkan vonis LULUS/GAGAL.**
Prareg: `prereg_v8_e_stuck.md` (terkunci 2026-10-11 17:05+07:00, SEBELUM metrik dihitung).

> **Riset pendahuluan: `statistical-analysis`** — ambang operasi dipilih di TRAIN (q95,
> dikunci prareg, bukan dioptimasi pasca-hasil); CI95 moving-block bootstrap AUPRC
> (blok 60, n=1.000, seed 42) + onset-level bootstrap recall; lift = AUPRC/prev dengan
> plafon lift = 1/prev wajib dilaporkan; <30 onset/fold = UNDERPOWERED.
> **Riset pendahuluan: `scientific-critical-thinking`** — OBSERVED (angka eksekusi run
> ini) dipisah dari kutipan V6/V7 dan dari hipotesis; kontrol-positif kejadian kurasi
> (`bha_stuck_fishing`) dipakai sbg tes falsifikasi validitas label; bug E3 ditemukan
> lewat tes pembeda (lift ≡ 1,0 = mustahil jika skor tak konstan) lalu diperbaiki & gerbang ulang.
> **Riset pendahuluan: `verification-mandatory`** — SEMUA angka dari eksekusi nyata di
> file data (bukti: skrip + `results/*.json` + log bertimestamp di workspace); gerbang
> eksak F-10 sebelum & sesudah refactor; daftar "belum terukur / belum diverifikasi" di §6–§7.
> **Riset pendahuluan: `sequentialthinking`** (4 pikiran) — diagnosis OOM vs bug vs data
> sebelum patch; verifikasi urutan sebab-akibat tiap perbaikan.

## 0. RINGKASAN EKSEKUTIF

Kelas `stuck` = 2 klaim (R1 §2.4). Fokus run ini = **klaim (ii) prediksi onset** (0→1,
H=10 menit) diuji nyata pada 3 fold temporal (F-9_A, F-10, F-14) + 2 arah LOWO +
kontrol-positif kejadian kurasi. Klaim (i) deteksi-status tidak diuji ulang (prareg =
onset; angka V6 dipertahankan sbg OBSERVED).

1. **Onset terdeteksi, tapi jauh di bawah ambang kelayakan operasional.** Cakupan
   peringatan-dini B1 terbaik = **31,8%** (E2/F-10) — di bawah 50% (bar layak-tren) dan
   80% (bar alarm). FAR semua engine 9,9–185 per 24 jam-negatif — di atas 6/24 jam
   (batas layak-tren shk-like §4). Persistence-onset = 0% recall di SEMUA fold (lemah
   per konstruksi, terkonfirmasi).
2. **Yang TERBUKTI = nilai ranking, bukan alarm.** E3_RF: AUPRC > prevalensi di **4/4
   fold/arah terukur** (lift 1,65 · 1,30 · 9,72 · 1,12); signifikan (CI95 AUPRC seluruhnya
   di atas prev) hanya **1/4** (LOWO F-9_A→F-14, lift 9,72 CI [0,018; 0,078] vs prev 0,004).
   Ambang operasi q95-prareg TIDAK bisa dipakai (jenuh 1,0 temporal / 0,0 LOWO) → P tak
   terukur di ambang → **layak sbg skor-ranking/triage, BELUM sbg alarm**.
3. **E2_stats (z-score TQA/HKLD/ROP-drop) bervariasi per sumur**: F-10 P 25,4% vs prev
   19,8% (lift 1,24); F-9_A lift 0,80; F-14 lift 0,87 (≤ acak). CI95 AUPRC memuat prev
   di SEMUA fold → sinyal statistik tidak terbukti di atas prevalensi.
4. **E1_rule (rule 2-dari-3) hanya bekerja di F-10** (P 45,7% vs prev 19,8%, T_lead median
   10 menit); nol alarm di 30% uji akhir F-9_A (periode penuhnya menyala — P 28,6% via
   LOWO), presisi ~0,5% di F-14 (di bawah prev).
5. **Kontrol-positif TIDAK SELARAS: 0/10** event `bha_stuck_fishing` F-14 punya onset
   instrumen dalam ±30 menit → peringatan terhadap *kejadian nyata kurasi* BELUM terbukti;
   validitas semantik label onset = risiko utama lapisan C (hipotesis alternatif di §4.4).
6. **Fold F-12 = belum terukur** (bukan angka karangan): STUCK_RT F-12 hanya ada di 6 file
   log berindeks *measured-depth* yang di-skip parser deret-waktu (bukti §6.1).

## 1. JENIS TUGAS + ENGINE (dicatat, bukan dinilai biner)

| Klaim | Jenis tugas | Engine (jenis) | Label | Baseline RELEVAN (R1 §2.4) |
|---|---|---|---|---|
| (ii) onset (FOKUS run ini) | **Prediksi kejadian mendatang** (transisi 0→1, jendela [t_e−10, t_e), blok dalam DibuANG) | E0_persistence (persistence) · E1_rule (rule-based: z TQA/HKLD>2 vs median/MAD 60 mnt + ROP-drop ≥30%, ≥2 dari 3) · E2_stats (statistical: skor z+z+ROP-drop, ambang q95-train) · E3_RF (supervised ML: RandomForest 200, fitur rolling 10-window × 10 kanal, STUCK_RT dilarang jadi fitur) | STUCK_RT ffill (PRIMER, dikunci prareg) + strict (sensitivitas) pada grid 60 dtk | persistence-onset (ekspektasi rendah — tes pembeda), prevalence-random (AUPRC=prev), anchor 2,67–7,37 mnt |
| (i) status (konteks) | Deteksi anomali/kondisi (blok STUCK_RT persisten) | persistence (V6: 0,787 F-9_A) — ML terbukti TIDAK menambah (V6 E1 §4.4) | status STUCK_RT | persistence + canary (0,410/0,769) |

Semua engine = tugas yang sama (prediksi-onset) → boleh dibandingkan antar engine;
klaim (i) = tugas berbeda, tidak dicampur.

## 2. LAPISAN A — APAKAH DETEKSI BEKERJA (semua angka = eksekusi nyata, run 2026-10-11)

Sumber: `workspace results/stage_temporal_*.json` + `stage_lowo_*.json` → `eval_results.json`.
Runtutan: F-10 21:04, F-14 21:05–21:07, F-9_A 21:10, LOWO 21:13–21:15, kontrol 19:55 (WIB).

### 2.1 Fold & kerangka (data nyata)

| Fold | Onsets ffill (train/test) | Onsets strict | prev test | jendela eval | jam_neg | blok stuck (median / p90) |
|---|---|---|---|---|---|---|
| F-9_A temporal | 72 (35/37) | 62/62 | 0,255 | 1.003 | 12,5 | 74 blok · 4 mnt / 65 mnt |
| F-10 temporal | 93 (49/44) | 104/88 | 0,198 | 1.908 | 25,5 | 95 blok · 16 mnt / 85 mnt |
| F-14 temporal | 61 (0/61) | 77/66 | 0,0055 | 70.432 | 1.167 | 61 blok · 3 mnt / 16 mnt |
| LOWO F-9_A→F-14 | 61 (uji penuh) | — | 0,0041 | 95.945 | 1.593 | (sama dgn F-14) |
| LOWO F-14→F-9_A | 72 (uji penuh) | — | 0,224 | 2.247 | 29,1 | (sama dgn F-9_A) |

Tidak ada fold UNDERPOWERED (≥30 onset semua; syarat R1 §1). Split temporal = 70% dari
rentang waktu ber-ops (bugfix terdisclosed; angka lama "split grid-span" tidak valid).

### 2.2 Tabel besar lapisan A (per fold × engine, ambang operasi prareg)

| Fold | Engine | P@ambang | Recall-onset@H | FAR/24jam-neg | AUPRC (lift) | CI95 AUPRC (mb) | T_lead median [IQR] |
|---|---|---|---|---|---|---|---|
| F-9_A | E0_persistence | – (0 alarm) | **0/37 = 0%** | 0 | – | – | – |
| F-9_A | E1_rule | – (0 alarm) | 0/37 = 0% | 0 | – | – | – |
| F-9_A | E2_stats | 0,316 | 3/37 = 8,1% | 25,1 | 0,205 (0,80) | [0,106; 0,383] | 3 [2; 4,5] |
| F-9_A | E3_RF | – (ambang jenuh 1,0 → 0 alarm) | 0/37 | 0 | 0,331 (**1,30**) | [0,209; 0,465] | – |
| F-10 | E0_persistence | – | **0/44 = 0%** | 0 | – | – | – |
| F-10 | E1_rule | **0,457** | 3/44 = 6,8% | 23,5 | – (rule biner) | – | 10 [6,5; 10] |
| F-10 | E2_stats | 0,254 | **14/44 = 31,8%** | 185,4 | 0,246 (**1,24**) | [0,157; 0,374] | 9,5 [4; 10] |
| F-10 | E3_RF | – (ambang jenuh 1,0 → 0 alarm) | 0/44 | 0 | 0,326 (**1,65**) | [0,200; 0,457] | – |
| F-14 | E0_persistence | – | **0/61 = 0%** | 0 | – | – | – |
| F-14 | E1_rule | 0,0048 | 2/61 = 3,3% | 29,6 | – | – | 6 [4; 8] |
| F-14 | E2_stats | 0,0026 | 3/61 = 4,9% | 62,4 | 0,0048 (0,87) | [0,0027; 0,0084] | 4 [2,5; 7] |
| F-14 | E3_RF | **belum terukur** (0 positif di train → RF tak bisa difit) | – | – | – | – | – |
| LOWO 9A→14 | E1_rule | 0,0037 | 2/61 = 3,3% | 28,2 | – | – | 6 [4; 8] |
| LOWO 9A→14 | E2_stats | 0,0007 | 3/61 = 4,9% | 173,1 | 0,0036 (0,88) | [0,0020; 0,0065] | 4 [2,5; 7] |
| LOWO 9A→14 | E3_RF | – (ambang q95=0,995 → 0 alarm) | 0/61 | 0 | 0,0394 (**9,72**) | [0,018; 0,078] | – |
| LOWO 14→9A | E1_rule | 0,286 | 1/72 = 1,4% | 20,6 | – | – | 10 [10; 10] |
| LOWO 14→9A | E2_stats | 0,200 | 2/72 = 2,8% | 9,9 | 0,240 (1,07) | [0,146; 0,367] | 1,5 [1,25; 1,75] |
| LOWO 14→9A | E3_RF | 0,224 | 72/72 = 100%† | 1.440 | 0,251 (1,12) | [0,185; 0,347] | 10 [8; 10] |

† ambang q95-train = 0,000 → **100% jendela eval dialarmkan** (TP 503 / FP 1.744 = 2.247
dari 2.247) — recall sempurna TIDAK berarti kelayakan; FAR 1.440/24 jam = gagal operasional.
CI95 recall (onset-level, n=1.000): E2 F-10 [0,182; 0,455]; E2 F-9_A [0; 0,189];
E2 F-14 [0; 0,115]; E1 F-10 [0; 0,159]; E1 F-14 [0; 0,082] — lebar = transparansi C4.

### 2.3 ΔB vs baseline relevan (penilai A sesungguhnya, R1 §1.2)

- **vs persistence-onset** (terukur 0% recall di 3/3 fold): ΔB > 0 untuk SEMUA engine
  pengingat-dini — namun baseline ini memang diharapkan mati per konstruksi (prareg:
  "ekspektasi rendah; tes pembeda"). Hasil tes pembeda: **persistence-onset 0% ≠ RF** →
  hipotesis reframing TIDAK ditolak, tetapi kemenangan di sini = ambang minimum terendah.
- **vs prevalence-random (AUPRC = prev)**: E3 lift > 1 di **4/4 fold/arah** (1,65 · 1,30 ·
  9,72 · 1,12) → ΔB > 0 mayoritas; E2 lift > 1 hanya **2/5** (1,24 · 1,07 vs 0,80 · 0,87 · 0,88)
  → **ΔB ≤ 0 mayoritas** = "tidak menambah di atas acak" pada fold ini.
- **vs anchor 2,67–7,37 mnt (B2)**: T_lead engine yang mendeteksi = 1,5–10 menit —
  median E1/F-10 = 10 mnt (di atas anchor), E2/F-9_A = 3 mnt (di dalam kisaran anchor).
- **AUPRC vs canary-kedalaman (G2, ambang-atas §4)**: E3 0,326–0,331 < canary 0,410 →
  G2 TIDAK terpenuhi (angka V6 canary dikutip sbg OBSERVED, tidak dihitung ulang).

**Penilaian A (bukan ambang universal):** E3_RF = "menambah di atas baseline relevan
untuk RANKING" (mayoritas fold, 1 signifikan); E2_stats & E1_rule = "tidak menambah
di atas prevalensi secara konsisten" — kemampuan tercatat, bukan gagal.

## 3. LAPISAN B — APAKAH DETEKSI MEMBERI NILAI MAINTENANCE

| Ukuran (R1 §1.3) | Hasil nyata | Nilai |
|---|---|---|
| **B1 cakupan peringatan-dini** (% onset terdeteksi [t_e−10, t_e) pada ambang prareg) | E2: 31,8% (F-10) · 8,1% (F-9_A) · 4,9% (F-14) · 4,9%/2,8% LOWO; E1: 6,8% terbaik; E3: 0% pada ambang prareg (jenuh) | **Maks 31,8% < 50%** (bar layak-tren) dan < 80% (bar alarm) → B arah benar (deteksi > persistence), kuantitas BELUM cukup |
| **B2 waktu-untuk-bertindak** | T_lead median 1,5–10 menit saat alarm menyala (E1 F-10: 10 [6,5;10]; E2 F-9_A: 3 [2;4,5]; E2 F-14: 4 [2,5;7]); anchor preseden 2,67–7,37 mnt | Kategorikal **<10 menit** (mayoritas) → waktu reaksi driller pendek; setara anchor hanya di fold dgn T_lead 3–7 mnt |
| **B3 pengurangan pemeriksaan tak perlu** | Baseline "aturan ambang-absolut onset" TIDAK ADA (status-quo stuck tidak punya peringatan-dini) → B3 formal **belum terukur**; proxy: FP per engine (E1 25/0/1.442 vs E2 197/13/3.035 di F-10/F-9_A/F-14) | E1 memangkas FP 8–∞× vs E2 tapi recall ikut turun → tradeoff terukur, penghematan riil belum diuji |
| **Validasi terhadap kejadian NYATA** (kontrol-positif) | **F-14: 0/10** event `bha_stuck_fishing` (4 Des 2007 + 6–7 Jun 2008) punya onset ±30 mnt; F-9_A & F-10: 0 event kategori ini; F-12: belum terukur | **Kejadian kurasi TIDAK selaras dgn onset instrumen** → "peringatan sebelum kondisi memburuk versi kejadian nyata" BELUM terbukti (lihat §4.4 hipotesis) |

**Penilaian B:** arah benar (ada peringatan sebelum onset dengan lead menit-scale, di atas
persistence yang nol), tetapi **cakupan & validasi kejadian nyata belum mencapai bar
"layak tren"**. Angka B1/FAR di atas berarti pada pemakaian riil: dari 61 onset F-14,
engine terbaik hanya mengingatkan 3 di antaranya — 58 tersesori.

## 4. LAPISAN C — CUKUP TEPERCAYA UNTUK DIPAKAI

### 4.1 C1 stabilitas antar-fold + CI95 (C4 dipenuhi)
- Spread AUPRC E2 temporal: 0,0048–0,246 (SANGAT lebar — fold F-14 vs F-10 beda 50×);
  E3 temporal: 0,326–0,331 (rapat di 2 fold terukur, F-14 kosong).
- **Uji ketertanda CI95 vs prev**: E2 — CI AUPRC MEMUAT prev di 5/5 fold → lift E2
  **tidak dapat dibedakan dari acak** pada data ini. E3 — CI di atas prev hanya 1/4
  (LOWO 9A→14); 3 lainnya memuat prev. → klaim ranking E3 = nyata tapi BELUM kuat.
- Sensitivitas label strict vs ffill: recall/E2 berubah sedikit (F-10 35,7% vs 31,8%;
  F-14 4,5% vs 4,9%; F-9_A 9,7% vs 8,1%) → kesimpulan TIDAK bergantung pada varian onset.

### 4.2 C2 ketahanan lintas-regime / lintas-wellbore
- **LOWO (2 arah, nyata): ambang TIDAK transfer.** q95 E3: F-9_A train = 1,0 (jenuh)
  → 0 alarm di F-14; F-14 train = 0,0 → alarm 96% jendela di F-9_A (FAR 1.440).
  q95 E2: 15,6 → 24,4 → 174.251 (skala skor beda sumur; MAD→0 pada F-14).
- **Ranking transfer mixed**: lift E3 LOWO 9,72 (signifikan) & 1,12 (tidak); E2 0,88 & 1,07.
- Bin regime (kedalaman/RPM/WOB, ΔAUPRC per kuartil) = **belum dijalankan** (§6).

### 4.3 C3 toleransi kualitas sensor + ablasi
- Ablasi istilah skor E2 (nyata, per fold): F-10 drop_TQA lift 1,53 / drop_HKLD 1,12 /
  drop_ROP 1,22 (full 1,24) — TQA paling berkontribusi; F-9_A drop_HKLD 0,91 > full 0,80
  (HKLD merugikan di fold ini); F-14 semua-drop 0,79–0,97 (full 0,87). Rentang perubahan
  <0,31 absolut → **tidak ada kanal dominan; ablasi tidak menyelamatkan lift yang memang ≈1**.
- Kualitas data (terukur): STUCK_RT non-null hanya 45.712/419.706 baris F-9_A (10,9%) ·
  9.545/286.781 F-10 (3,3%) · 5.147/1.648.026 F-14 (0,3%); jendela ber-ops = 0,13% / 44,7% /
  2,33% baris grid → grid didominasi lubang waktu (rolling window count≥3 menangani NaN).
- Ambang E2 satuan skor sangat sensitif MAD→0 (q95 F-14 = 244.091 vs F-10 = 2,65) →
  ambang NON-portabel antar sumur (bagian dari C2).

### 4.4 C-semantik + kontrol-positif (risiko utama kelas ini)
- Distribusi nilai STUCK_RT (raw): F-9_A {0:23.122, 3:19.056, 1:3.171, 2:363} · F-10
  {0:5.462, 3:3.982, 1:74, 2:27} · F-14 {0:4.753, 1:371, 2:19, 3:4} → **skala didominasi
  "3" di F-9_A/F-10 tetapi "1" di F-14** — semantik 0/1/2/3 lintas wellbore belum
  terdokumentasi (blind spot V7 §5, spec §6.3) → label lintas-wellbore BELUM terverifikasi.
- **Kontrol-positif 0/10 (F-14).** Hipotesis alternatif (belum terbukti, dicatat jujur):
  (a) `bha_stuck_fishing` = kegiatan PANCUNG yang dimulai berjam-jam/hari SETELAH onset
  stuck sesungguhnya → jendela ±30 mnt salah sasaran; (b) STUCK_RT F-14 sangat jarang
  (0,3% non-null) sehingga onset tak muncul dekat kejadian; (c) selisih zona waktu
  label kurasi (belum diperiksa). Yang TERAMATI: onset instrumen ≠ jadwal kegiatan kurasi.

### 4.5 Kekuatan bukti lapisan C
C4 (CI95 + label UNDERPOWERED) **terpenuhi penuh** (semua fold ≥30 onset, CI tercetak);
C1 = lebar (diannotasi); C2 transfer = **gagal di ambang, mixed di ranking**; C3 = moderat;
C-semantik + kontrol-positif = **titik rapuh utama** klaim onset.

## 5. KESIMPULAN — LAYAK UNTUK X, BELUM UNTUK Y (+ kekuatan bukti)

### 5.1 Per engine

**E3_RF (supervised ML, prediksi-onset)**
- **LAYAK untuk:** (a) skor-ranking relatif risiko onset *di dalam satu wellbore* —
  AUPRC > prev 4/4 fold/arah, signifikan 1/4 (LOWO 9A→14: lift 9,72 CI [0,018; 0,078]);
  (b) bahan TRIAGE manual ("jam/periode mana yang didahulukan dicek inspeksi");
  (c) eksperimen ambang BARU (pra-reg baru: q95 validasi-OOS / kalibrasi isotonic) —
  ambang prareg q95-train terbukti jenuh (1,0/0,0) dan TIDAK boleh diganti pasca-hasil
  dalam run ini.
- **BELUM untuk:** alarm otomatis (0 TP/0 FP pada ambang prareg temporal; FAR 1.440 di
  salah satu arah LOWO); pemantauan rutin otomatis; F-14 temporal (**belum terukur**:
  0 positif di split train).
- **Kekuatan bukti: SEDANG-RENDAH** — 4/4 arah konsisten >1 tapi 3/4 CI memuat prev;
  1 fold kosong; bugfix E3 diverifikasi gerbang eksak F-10 (§7).

**E2_stats (statistical, z TQA/HKLD + ROP-drop)**
- **LAYAK untuk:** indikasi jam berisiko pada sumur *mirip F-10* (P 25,4% vs prev 19,8%,
  lead 9,5 mnt, recall 31,8% tertinggi) dengan anotasi beban-kerja; eksperimen riset
  threshold.
- **BELUM untuk:** generalisasi ke F-9_A/F-14 (lift 0,80/0,87 = ≤ acak; CI memuat prev
  di semua fold); alarm/pemantauan otomatis (FAR 25–185/24 jam ≫ 6).
- **Kekuatan bukti: RENDAH** — tidak ada fold di mana lift E2 terbukti signifikan di atas prev.

**E1_rule (rule-based precursor 2-dari-3)**
- **LAYAK untuk:** pre-kualifikasi/fokus cek di sumur mirip F-10 (P 45,7% — tertinggi
  semua engine, T_lead median 10 menit, FP 25 vs E2 197) sebagai *pengurang area cek*,
  dengan inspeksi manual lanjutan.
- **BELUM untuk:** F-9_A (rule nol alarm di 30% uji temporal), F-14
  (P 0,48% < prev 0,55%), pemakaian lintas-wellbore.
- **Kekuatan bukti: RENDAH** — menguntungkan hanya 1/3 fold.

**E0_persistence-onset (baseline)**
- **Kemampuan tercatat (bukan gagal):** recall@H = 0% di 3/3 fold + CI95 [0;0] —
  status-quo TIDAK MAMPU memberi peringatan-dini; ini konfirmasi terukur dari ekspektasi
  prareg dan menjadikan persistence detektor-status terbaik (klaim-i, V6) yang hidup terpisah.

### 5.2 Tingkat pemakaian kelas (vs ambang §4)

| Tingkat | Status | Bukti |
|---|---|---|
| **Alarm kritis otomatis** | **BELUM** | B1 ≤31,8% (butuh ≥80%); FAR 9,9–1.440 (butuh ≤1); G1 lift ≥1,5 mayoritas TIDAK (2/4); G2 AUPRC < canary (0,33 < 0,41); kontrol-positif 0/10 |
| **Pemantauan/tren operasional otomatis** | **BELUM pada ambang prareg** | B1 < 50% semua fold; FAR semua fold > 6/24 jam-neg |
| **Triage/inspeksi-manual terbantu (per-sumur, mirip F-10)** | **LAYAK dengan anotasi beban-kerja** | E1 P 45,7% · E2 lead 9,5 mnt · T_lead 3–10 menit (setara/atas anchor) |
| **Riset ranking onset + rekayasa ambang lanjutan** | **LAYAK** | E3 lift 1,12–9,72 di 4/4 arah; prareg + CI lengkap tersedia |
| **Deteksi-status stuck (klaim-i)** | **LAYAK (angka V6, tidak diuji ulang)** | persistence 0,787 F-9_A; ΔB ML-vs-persistence negatif terukur V6 |

**Kekuatan bukti kelas: RENDAH–SEDANG.** Pendukung: prareg terkunci sebelum metrik;
gerbang eksak lolos; CI95 lengkap; 5 fold/arah nyata; sensitif-label konsisten.
Penghalang: kontrol-positif nol (validitas label), 1 fold hilang (F-12), ambang tak
portabel, signifikansi statistik hanya 1/4 untuk klaim terkuat, FAR semua di atas batas.

## 6. BELUM TERUKUR + ALASAN (tanpa angka karangan)

1. **Fold F-12** — `results/stage_temporal_F-12.json`: STUCK_RT F-12 hanya ada di 6 file
   log berindeks *measured depth* (`1/log/1/1/1/0000{1..4}.xml`, `1/log/8/1/0000{1,2}.xml`;
   `indexType=measured depth`, `indexCurve=DEPTH` — verifikasi `grep -rl STUCK_RT`, 2026-10-11),
   semua di-skip parser deret-waktu (`F-12.qc.json` → `depth_logs_skipped`, 18 file) sehingga
   `F-12.csv` (840 MB, 188 kolom) TIDAK punya kolom STUCK*; nol file berbasis-waktu F-12
   mengandung STUCK_RT. Grid 60 dtk + onset butuh join kedalaman→waktu via trajectory
   (belum dieksekusi). Angka 3.463 baris STUCK_RT F-12 (V7_M2 §S-A2) = baris depth-log mentah.
2. **E3_RF F-14 temporal** — 0 jendela positif di split train (61 onset semuanya jatuh di
   test) → RF tidak bisa difit pada y kelas tunggal (status code: "belum terukur" di JSON).
3. **C2 bin regime** (ΔAUPRC per kuartil kedalaman/RPM/WOB) — belum dijalankan (butuh join
   MD/TVD ke grid; di luar run ini).
4. **Sensitivitas H = 5 / 30 menit** (R1 §3.1#2) — belum dijalankan; H = 10 dikunci prareg.
5. **Uji durasi-blok 2× (R1 §3.1#4)** — median blok terukur (3/4/16 mnt) dicatat, tetapi
   pembanding "onset semu di jendela negatif" belum dihitung → uji 2× = belum dijalankan.
6. **B3 formal** — tidak ada baseline aturan-ambang-absolut operasional untuk onset stuck
   (status-quo kelas ini tanpa peringatan-dini) → hanya proxy FP (§3).
7. **P@k top-k** (R1 §1.2 utk kelas langka) — belum dihitung.
8. **Klaim (i) status** tidak diuji ulang (prareg fokus onset); angka V6 dikutip sbg OBSERVED.

## 7. INTEGRITAS EKSEKUSI (bukti, gerbang, pembetulan)

- **Sumber data nyata lokal**: `grids/grid_{F-9_A,F-10,F-14}.csv` (60 dtk, dari
  `witsml_parsed/*.csv` via `extract_folds2.py`) + onsets ffill/strict + `labels_curated_v2.csv`
  (kontrol-positif). Semua metrik dari `eval_stage.py` → `results/*.json` → `eval_results.json`
  (log bertimestamp: F-10 21:04, F-14 21:05–07, F-9_A 21:10, LOWO 21:13–15, kontrol 19:55 WIB).
- **Gerbang eksak**: `verify_f10_v2.py` — rerun F-10 pasca-refactor memory-lean:
  E0/E1/E2/sensitivitas-strict/ablasi-C3/meta-fold **identik eksak** (tol 1e-9); diff hanya
  di E3_RF (sengaja, lihat bugfix). Lolos 21:04.
- **Bugfix diajukan terbuka (bukan disembunyikan):**
  1. *Bug E3 temporal*: tahap temporal menreshold `proba_TRAIN` pada mask test → alarm
     selalu 0 dan skor test = konstan (NaN→0) sehingga lift E3 ≡ 1,0 pada run 19:52/19:53
     (terbaca di log lama). Diperbaiki memakai `proba_TEST` (ambang q95 tetap dari train,
     sesuai prareg) — konsisten dgn stage_lowo yang benar sejak awal. Run ulang F-9_A/F-14.
  2. *Bug index-y LOWO* (patch attempt-6): y diindeks dgn posisi-fitur → train jadi
     kelas-tunggal → `predict_proba` 1 kolom → kedua LOWO crash (exit 1); diperbaiki
     (reindex y ke indeks feats) + rerun sukses (exit 0).
  3. *OOM global* (dmesg 19:55:07 & 20:18:42, korban F-14 rss 3,4 GB/2,17 GB di box 7,7 GB):
     refactor memory-lean (fitur hanya disimpan di baris ber-ops, baca float32 langsung,
     istilah skor dihitung sekali) → peak F-14 turun ke **1.134 MB**, run 129,5 dtk, exit 0.
- **Ketidakcocokan terdisclose (belum direkonsiliasi):** hitung onset prareg run ini
  (F-9_A 72 ffill/62 strict; F-14 61/77; F-10 93/104) ≠ angka PM V7 (F-9_A 74/34; F-14 87/0;
  spec §6.2) — basis resolusi/agregasi berbeda; prareg mengunci definisi SEBELUM hasil.
- **Belum diverifikasi** (aturan 3): zona waktu label kurasi; isi depth-log F-12 terhadap
  kebutuhan fitur (kemungkinan lengkap, tetapi butuh join trajectory); apakah 0/10 kontrol
  murni semantik-event vs selisih waktu (hipotesis §4.4).

## 8. BARIS RISET PENDAHULUAN (ringkas)

- Riset pendahuluan: `statistical-analysis` — prareg ambang q95 di train; CI95 bootstrap
  (moving-block AUPRC + onset-level recall); lift vs prev + plafon 1/prev; UNDERPOWERED <30.
- Riset pendahuluan: `scientific-critical-thinking` — OBSERVED vs hipotesis dipisah;
  kontrol-positif sbg falsifier; tes pembeda lift≡1,0 menemukan bug E3.
- Riset pendahuluan: `verification-mandatory` — semua angka dari eksekusi; gerbang eksak
  F-10; "belum terukur + alasan" menggantikan tebakan; daftar belum-diverifikasi §7.
- Riset pendahuluan: `sequentialthinking` (4 pikiran) — diagnisa OOM/bug/data sebelum patch.
