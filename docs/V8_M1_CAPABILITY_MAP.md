# V8-M1 — PETA ALAT PREDICTIVE MAINTENANCE (agregasi 7 profil kemampuan)

Task: `t_4bc96d08` [Master] · Board: capstone-v8-capability · Tanggal: 2026-10-11 (WIB)
Kerangka: `docs/V8_R1_ABC_SPEC.md` (3 lapisan A/B/C — mengganti gate biner V6/V7).
Sumber: 7 dokumen `docs/V8_E_{vib,ssi,bit_wear,stuck,hyd,shk,tool_wear}_CAPABILITY.md`.
Status: KEMAMPUAN + BATAS + KEKUATAN BUKTI per engine — BUKAN label gagal/buang.
Semua angka = kutipan dari 7 dokumen sumber; turunan aritmetika ditandai DERIVED.

> **Riset pendahuluan: `scientific-critical-thinking`** — setiap klaim dipisah OBSERVED
> (angka 7 dokumen sumber) vs DERIVED (turunan) vs BELUM TERUKUR; kontradiksi antar-
> evaluator diselidiki dan direkonsiliasi (§2), bukan dipilih yang nyaman; kontrol
> keabsahan silang: hitungan tier dijumlahkan ulang = 7 engine (§4), gap diverifikasi
> balik ke dokumen (§5).
> **Riset pendahuluan: `statistical-analysis`** — AUPRC/lift TIDAK dirata-ratakan antar
> kelas (prevalensi beda: ssi 0,5–6,5% → plafon lift 15–196; bit_wear K-1 prev s/d 0,544
> → plafon 1,84; tool_wear prev 0,5 → plafon 2,0); hitungan tier per ENGINE (7 unit),
> sub-klaim dicatat di dalam sel; CI95/label UNDERPOWERED dari tiap dokumen dipertahankan
> apa adanya; FAR dilaporkan per skala aslinya (jendela/blok/menit) — jangan dibandingkan
> lintas kelas tanpa anotasi skala.
> **Riset pendahuluan: `what-if-oracle`** — arsitektur alat (§3) di-stress-test dengan
> cabang Ω/α/Δ/Ψ/Φ + tripwire eksplisit, agar usulan tidak bergantung pada satu asumsi
> (kampanye penguatan berhasil / label valid / dst).
> **Riset pendahuluan: `sequentialthinking`** (5 pikiran, 5/5 sukses) — inventaris 7
> dokumen → klasifikasi tugas + tier → koherensi/kontradiksi → arsitektur + what-if →
> gap + gerbang acceptance.

---

## 0. Konteks kerangka

Kerangka V8 (instruksi operator): keberhasilan = membangun ALAT PdM; ML hanya satu
komponen bila beri nilai tambah. Penilaian per engine:

- **LAPISAN A** — apakah deteksi bekerja? (precision/recall/FAR/waktu-deteksi vs
  baseline yang RELEVAN untuk tugas itu).
- **LAPISAN B** — apakah deteksi beri nilai maintenance? (waktu peringatan terhadap
  kejadian nyata = kunci).
- **LAPISAN C** — cukup tepercaya untuk dipakai? (lintas periode/regime/peralatan,
  kualitas sensor, transparansi ketidakpastian).

Gate lift≥1,5 + mayoritas-fold V6 = syarat ambang-atas "TERBUKTI prediksi kuat"
(klasifikasi alarm), BUKAN syarat "engine boleh dipakai sama sekali".

---

## (a) TABEL PETA UTAMA — satu baris per engine

| Kelas | Jenis tugas | Jenis engine | Lapisan A tercapai | Lapisan B tercapai | Lapisan C tercapai | LAYAK UNTUK (tier tertinggi) | BELUM UNTUK | Kekuatan bukti |
|---|---|---|---|---|---|---|---|---|
| **vib** | Deteksi kondisi (`VIBLAT_RT ≥32,17`), bukan onset | Hybrid: rule ambang-absolut + persistence + RF (V6 E1a) | **KUAT**: lift 4/4 ≥1,5 (1,61–3,50); RF≥canary 4/4; vs persistence menang 2/4 (=50% ambang) | **Belum terukur** — B3/B4/FAR tidak pernah dicetak V6 (celah struktural, bukan gagal) | **SEDANG**: C4 penuh (CI95 semua fold, tanpa fold underpowered); C2 parsial (canary 4/4); C1 spread AUPRC 0,471 (lebar); C3 nol-bukti | **Tren** + **peringatan advisory BERSYARAT** (syarat: ukur FAR_t + B4 di kampanye penguatan F-4/F-10/F-15) | Alarm otomatis kritis; klaim lead-time berapa menit (B belum diukur); generalisasi non-Volve | A **KUAT** · B **nol-bukti** · C **sedang** |
| **ssi** | Deteksi kondisi (`SSI(CRPM_RT) ≥1`), bukan onset/diagnosis | Hybrid: rule definisi kanal + RF (300 pohon) | **ΔB>0 di 5/5 fold** vs canary (0,0055–0,0676) dan vs persistence (persistence menang 0/5); G1 4/5, G2 5/5 | **Belum terukur** — B1–B4 semua belum (konsekuensi tugas status) | **SEDANG**: C4 penuh; CI-bawah > no-skill hanya **2/5 fold**; C2 canary 5/5 (bin eksplisit belum); C3 belum; re-run S-E1 11 fold belum jalan | **Tren** + **peringatan human-in-loop BERSYARAT** (syarat: FAR diukur dulu; wajib label keyakinan, bukan angka tunggal) | Alarm otomatis kritis; klaim onset/lead-time; satu-satunya detektor SSI (layer rule tetap dasar) | A **tinggi** · B **belum** · C **sedang** |
| **bit_wear** | K-1 deteksi kondisi (status high_MSE); K-2 prediksi onset (**BELUM terukur**) | K-1: persistence (engine status terbaik) + RF + canary; K-2: RF-onset dirancang (relabel S-F1, nol parse) | K-1: RF≥canary **4/4** (ΔB +0,058…+0,107); RF **kalah persistence 4/4** (−0,087…−0,381) → persistence AUPRC 0,679–0,984 = engine status terukur terbaik; K-2: **belum ada angka** (hanya 481/329 onset terverifikasi A1+PM) | K-1: konfirmasi-status murah terukur; lead masuk blok ≈0 (TERLAMBAT +1 jendela ≈10 mnt, DERIVED); B3/B4 belum. K-2: semua ukuran B belum | K-1: C4 penuh; C1 spread 0,515 (lebar); C2 risiko terukur (SHAP didominasi MD/TVD); C3 belum; 4/7 sumur layak. K-2: belum ada C | **Tren/screening** (K-1, 4 wellbore teruji) + **konfirmasi-status** (persistence K-1) | Alarm otomatis; peringatan dini masuk blok (K-2 belum dijalankan); klaim diagnosis/identitas bit (EDM BLOCKED) | RF>canary 4/4 **KUAT** · persistence-beats-RF 4/4 **KUAT** · K-2 **nol bukti** |
| **stuck** | K-ii prediksi onset (0→1, H=10 mnt) = fokus run; K-i deteksi status (angka V6 dipertahankan) | 4 engine: E0 persistence · E1 rule (2-dari-3) · E2 statistical (z TQA/HKLD/ROP) · E3 RF | E3 lift **4/4 >1** (1,65/1,30/9,72/1,12; CI signifikan 1/4); E2 lift 0,80–1,24, CI memuat prev 5/5; E1 P 0,457 hanya di F-10; kontrol-positif **0/10** | Arah benar tapi kuantitas kurang: **B1 maks 31,8%** (<50% bar tren, <80% alarm); T_lead 1,5–10 mnt (E1/F-10 median 10 mnt = di atas anchor 2,67–7,37); B3 formal belum (proxy FP: E1 8–∞× lebih hemat dari E2) | C4 penuh (prareg terkunci, CI95, ≥30 onset/fold); C1 lebar; C2 **ambang tak transfer** (q95 jenuh 1,0/0,0); C3 ablasi (tak ada kanal dominan); C-semantik STUCK_RT 0–3 lintas-well belum terdokumentasi | **Triage/inspeksi-manual terbantu** (sumur mirip F-10: E1 P 0,457, lead 10 mnt) + **riset ranking onset** (E3) + **deteksi-status via persistence** (V6) | Alarm otomatis (B1≤31,8%, FAR 9,9–1.440); pemantauan-tren otomatis pada ambang prareg (FAR semua fold >6); transfer lintas-wellbore; fold F-12 (belum terukur) | **RENDAH–SEDANG** (prareg+CI kuat; kontrol-positif 0, signifikansi 1/4, 1 fold hilang) |
| **hyd** | K-i deteksi kondisi (status residu SPPA); K-ii prediksi onset kick/loss (proxy) | K-i: **persistence** = engine terbaik (RF tidak menambah — ΔB negatif 7/7, replikasi eksak V6); K-ii: hybrid RF + fitur aliran (mass-balance) | K-i: persistence P **0,615–0,793** (CI non-tumpang vs RF 6/7 fold); RF TIDAK beri nilai tambah (kemampuan negatif terukur). K-ii: AUPRC_test **0,228** [0,009;0,629], lift titik 8–151 konsisten 3 varian label; onset test **3 (UNDERPOWERED)** | K-i: konfirmasi saat kejadian nyata **pos_frac 0,884** (7,4× base) tapi **peringatan-dini 0/1 episode**; FAR 39–111/24jam; beban blok 0,16–4,7/hari. K-ii: **T_lead median 7 mnt**, B1 66,7% (2/3 tier alarm +flow); B3 belum | K-i: C4 penuh, 7 fold ≥30 positif, coverage sensor 94–98,7%; C3 ablasi (RF bergantung depth di sebagian fold), persistence IMUN. K-ii: C1 gagal (CI sangat lebar), 1 wellbore, label proxy | K-i: **tren status hidrolik** + **konfirmasi kondisi saat kejadian**; K-ii: **indikasi dini bertingkat-menit** dengan anotasi ketidakpastian | Alarm otomatis (K-i FAR 39–111; K-ii FAR 5,9 >1); peringatan-dini K-i; generalisasi K-ii (1 wellbore; GAINLOSSTOT F-1C/F-11 belum parse); klaim kausal (n=1 episode) | K-i **KUAT** (7/7 konsisten, replikasi eksak) · konfirmasi-kejadian **LEMAH** (n=1) · K-ii **SEDANG-LEMAH** |
| **shk** | Deteksi anomali/dysfunction sedang berlangsung (`SHKRSK_RT ≥1`) + sub-tugas onset H=10 mnt | Hybrid: RF (55 fitur, LOWO 9 fold) + persistence; reproduksi V6 7/7 <1e-9 | Grid titik-operasi pra-reg: **FAR≤1/24jam dgn recall>0 = 0 dari 9 fold**; FAR≤6 dgn recall>0 = 4 titik (P 0,18–0,55); fold eksternal F-10/F-12 lift 0,96/1,06 (kalah canary) → sinyal lokal-wellbore | **Peringatan situasional lead 2–9 mnt** (median global 5,0; B1 0–0,348 @tau0,05); **RF≥persistence B1 di 9/9 fold** (nilai tambah ML terukur utk onset); **B3 NEGATIF** (−0,11…−53,75: engine MENAMBAH beban cek pada tau≤0,20) | C4 penuh (CI95 per fold); C1 spread lift 8,85; C2 drop AUPRC 49–93% pada kuartil depth/RPM/SWOB (7/9 fold); C-semantik severity-mix beda antar well; C3 6–8/9 fold robust | **Screening berbiaya-cek-tinggi** (tau 0,05–0,10) + **peringatan situasional pada well terkalibrasi lokal** + 4 titik operasi hemat-awas (FAR≤6) | Alarm otomatis FAR≤1 (tidak ada di kurva); kalibrasi ambang lintas-wellbore (0 alarm di semua fold uji); generalisasi ke wellbore baru; pengurangan pemeriksaan (B3); pemakaian buta lintas-regime | A&B **SEDANG-KUAT** (9 fold nyata, pra-reg, reproduksi 7/7) · C **SEDANG** |
| **tool_wear** | K-ii prediksi status keausan lintas-alat (LOTO); K-i deteksi perubahan-regime dalam-run | K-ii: RF (300 pohon) + ambang inner-LOO F1 + titik operasi FAR-terkalibrasi; K-ii domain **bengkel** (Mendeley, 4 alat, 50–62 dtk) | K-ii: AUPRC 0,543–0,768, ΔB vs canary **4/4 positif** (+0,027…+0,174), lift 1,09–1,42 (G1 0/4, plafon 2,0); precision biner 0,50–0,56 ≈ peluang; K-i: change-point signifikan 8/8 run **termasuk 8/8 alat baru** → spesifisitas keausan GAGAL (precision run 0,50), artefak termal 0/8 | Titik operasi FAR-terkalibrasi ≤1/menit: **deteksi 4/4, T_lead median 47,5 dtk** (35–59) sebelum tumpul, 1–3 FP di baseline; K-i: cp = gating kapan inspeksi layak (bukan onset keausan) | C4 penuh; C1 spread 0,225, CI lebar; C2 "menang tipis" (lift<1,5 di 4/4); C3 dropout 1 kanal <20% (robust), 2 kanal marginal (26,2%); C-domain: transfer ke drilling **TIDAK diklaim** (confound urutan-run R02>R01) | **Skor/indikasi tren keausan** (ranking lintas-alat, bengkel) + **detektor perubahan-regime dalam-run** (gating inspeksi) | Alarm kritis otomatis (precision ≈0,5; G1 0/4); klaim onset progresi keausan (spesifisitas gagal); transfer ke rig drilling (tidak ada data); SLA operasional rig (waktu = detik bengkel) | K-ii **SEDANG** (4/4 fold menang, re-run identik 4 digit, tapi 4 alat + confound) · K-i utk klaim keausan **TERDUKU LEMAH** |

---

## (b) CEK KOHERENSI + KONTRADIKSI ANTAR-EVALUATOR

### B.1 Temuan yang KOHEREN lintas evaluator (penguat, bukan kontradiksi)

1. **"Persistence mengalahkan RF untuk deteksi-status" muncul di 4 evaluator berbeda:**
   hyd (ΔB RF−persistence **negatif 7/7 fold**, CI non-tumpang 6/7), bit_wear (**4/4**,
   RF kalah telak −0,087…−0,381), shk (persistence AUPRC > RF di **4/9 fold**; persistence
   bangkit di well prev-tinggi), vib (persistence menang **2/4**). Kesimpulan koheren:
   **persistence = engine status default di semua kelas** — label status membentuk blok
   temporal panjang, dan RF hanya bernilai di sub-tugas ONSET/lead-time (shk B1 9/9 RF≥
   persistence; hyd K-ii dgn fitur aliran). Ini pola silang-evaluator yang sama, bukan
   pertentangan.
2. **Aturan FAR-ke-tier yang konsisten** (lihat B.3 rekonsiliasi): shk dan stuck memakai
   batas yang sama (≤6/24jam = tren; ≤1 = alarm) dan menyimpul konsisten dgn hasil masing-
   masing (shk: 4 titik ≤6 → layak; stuck: semua >6 → belum).
3. **C4/transparansi ketidakpastian TERPENUHI di SEMUA 7 engine** (CI95 dilaporkan, fold
   underpowered dilabeli) — standar minimal kerangka terpenuhi seragam.

### B.2 Potensi kontradiksi yang DIHADAPI, bukan disembunyikan

| # | Tampak sebagai | Penyebab sebenarnya | Resolusi (keputusan peta ini) |
|---|---|---|---|
| C1 | hyd: "**JANGAN pakai ML (RF)** di kelas ini" vs vib: "RF = penambah nilai" | Baseline relevan BERBEDA per tugas (V8-R1 §2): hyd-status didominasi persistence, vib-status RF menang 4/4 vs canary & 2/4 vs persistence | **Bukan kontradiksi.** Aturan tetap: pilih engine per KELAS dari ΔB vs baseline relevan kelas itu. Larangan RF berlaku hanya untuk hyd-status; jangan digeneralisasi ke kelas lain, dan jangan sebaliknya meng-generalisasi "RF bagus" dari vib ke hyd |
| C2 | bit_wear "**LAYAK tren**" vs stuck "**BELUM layak tren otomatis**" — keduanya menilai B belum cukup | Aplikasi aturan §4 yang BEDA kondisi: bit_wear FAR **belum pernah diukur** → aturan memberi "tren + anotasi"; stuck FAR **terukur >6/24jam di semua fold** → aturan menurunkan ke "belum tren otomatis" | **Konsisten setelah dirumuskan eksplisit:** FAR belum terukur = LAYAK TREN dengan anotasi beban-kerja (vib, ssi, bit_wear); FAR terukur >6 = BELUM tren otomatis (stuck). Rumusan ini WAJIB dibawa ke dokumen mana pun |
| C3 | FAR dilaporkan dalam 3 SKALA berbeda: per jendela/24jam (shk, hyd, stuck, ssi, vib), per blok unik (hyd K-i: 0,16–4,7 blok/hari), per menit (tool_wear: 46–60 FP/menit) | Definisi unit alarm berbeda per tugas (jendela 60 dtk vs blok transisi vs run 1 dtk) | Semua FAR **dilaporkan per skala aslinya** di peta ini; perbandingan lintas-kelas TANPA konversi-skala dilarang (statistical-analysis: beda unit = beda populasi) |
| C4 | hyd-K-i FAR 39–111/24jam (skala jendela) terdengar "banyak" tapi beban riil 0,16–4,7 blok/hari terdengar "ringan" | Skala jendela menghitung tiap menit alarm berulang dalam blok yang sama; skala blok menghitung per transisi | Keduanya benar untuk pertanyaan berbeda: jendela = beban notifikasi; blok = beban pemeriksaan. Peta memakai keduanya dengan label |
| C5 | tool_wear (bengkel, detik) dicampur dlm hitungan alat Volve (menit) | Domain berbeda | tool_wear = **modul terpisah** dalam arsitektur (§3); lead-time-nya (detik) tidak dijumlahkan dengan lead-time rig (menit) |
| C6 | shk B3 **NEGATIF** vs evaluator lain yang melaporkan B "belum terukur" | shk satu-satunya yang BENAR-BENAR menghitung B3 (punya baseline display status-quo); yang lain belum | Bukan kontradiksi — justru menunjukkan B3 = metrik paling mahal. Tercatat sebagai gap G3 |

### B.3 Overlap antar-engine (pertanyaan operator: "stuck-onset + hyd bisa jadi satu hybrid?")

- **Onset layer (stuck K-ii, hyd K-ii, shk sub-tugas onset, bit_wear K-2 belum):**
  grid sama (60 detik), horizon sama (H=10 menit), fitur tumpang tindih (HKLD/RPM/WOB/
  ROP/BPOS/depth), TAPI label beda fisika (STUCK_RT vs ΔV_pit vs SHKRSK_RT vs blok
  high_MSE) dan tindakan beda (releasing/spotting vs well-control vs kurangi parameter vs
  bit-change).
  **KEPUTUSAN: SATU onset-layer BERSAMA (shared grid + shared feature store + shared
  calibration harness), TAPI head prediktor TERPISAH per kelas** — satu model gabungan
  akan mencampur estimand dan melanggar baseline-per-kelas. Hybrid = infrastruktur
  bersama, bukan bobot bersama.
- **Status layer (vib, ssi, bit_wear K-1, hyd K-i, stuck K-i):** persistence/rule engine
  benar-benar seragam → **boleh disatukan jadi satu modul "status-confirmation" murah**
  (nol training, output = konfirmasi status + tren). RF per-kelas di atasnya hanya jika
  ΔB vs persistence positif (vib: ya di separuh fold; ssi: ya 5/5; hyd: TIDAK; bit_wear:
  TIDAK).
- **Tidak ada engine yang saling MENUTUPI kelemahan kelas lain** — tidak ada yang perlu
  dihapus; semua tetap tampil dengan batasnya.

---

## (c) USULAN ARSITEKTUR ALAT PdM

Satu grid waktu 60 detik + jendela fitur 10 menit sebagai tulang punggung; empat lapis
output; kalibrasi ambang SELALU lokal per wellbore (bukti: ambang lintas-well TIDAK
transfer — shk tau-budget 0 alarm semua fold, stuck q95 jenuh 1,0/0,0, hyd FAR test
meledak 26–300×).

```
LAYER-0  STATUS OTOMATIS (rule/persistence — sistem hari-ini, tanpa ML)
  rule ambang-absolut VIBLAT 32,17 · rule SSI≥1 · rule display shock ·
  persistence-status: hyd-K-i (P 0,615–0,793) · bit_wear-K-1 (0,679–0,984) ·
  stuck-K-i (V6 0,787) · vib-status
  → indikator status otomatis di layar rig; KONFIRMASI kondisi, bukan alarm PdM baru
LAYER-1  PERINGATAN HUMAN-IN-LOOP (butuh konfirmasi operator)
  hari ini: shk-RF (well terkalibrasi; lead 2–9 mnt; badge FAR & beban kerja) ·
            stuck E1-triage (sumur mirip F-10; P 0,457; lead 10 mnt) ·
            hyd K-ii (F-9A; lead 7 mnt; label UNDERPOWERED wajib tampil)
  masuk setelah ukur FAR: vib (syarat FAR_t + B4) · ssi (syarat FAR)
  → notifikasi + label keyakinan + badge beban-kerja (FAR terukur per fold)
LAYER-2  TREN / SKOR (dashboard, tanpa notifikasi)
  vib-RF · ssi-RF · bit_wear (persistence + RF screening) · tool_wear LOTO-score ·
  stuck E3 ranking · hyd persistence trend
LAYER-3  HUMAN DECISION (semua yang BELUM layak alarm)
  semua kelas hari ini — alat PdM menyarankan, manusia memutuskan
```

**Alarm otomatis tanpa manusia: TIDAK ADA slot hari ini (0/7 engine).** Satu-satunya
keluaran otomatis adalah rule ambang-absolut Layer-0 = sistem yang sudah ada di rig,
bukan hasil proyek PdM. Ini keputusan wajar, bukan kegagalan: syarat alarm
(FAR ≤1/24jam dgn recall>0 + B1≥80% + C2/C3) memang belum tercapai engine mana pun.

**Gate kenaikan tier (dari dokumen sumber, bukan angka baru):**
- Masuk LAYER-1: FAR≤6/24jam (atau setara skala) TERUKUR dgn recall>0 + T_lead/B4
  terukur + C4; kalibrasi lokal per well + anotasi regime.
- Masuk LAYER-0-alarm (otomatis): FAR≤1/24jam dgn recall>0 + B1≥80% + C2 per-bin +
  C3 dropout <20% + validasi kejadian nyata.

**Stress-test arsitektur (what-if-oracle):**

| Cabang | Bobot | Skenario | Konsekuensi |
|---|---|---|---|
| Ω Best | 15% | Kampanye penguatan (parse VIBLAT F-4/F-10/F-15, S-E1 re-run 11 fold, K-2 bit_wear jalan) mencetak FAR+B4 | vib & ssi naik penuh ke LAYER-1; tetap 0 alarm hingga B1≥80% terbukti |
| α Likely | 45% (prioritas 61,8% utk aksi) | Alat live sebagai L0+L2+L1-terbatas (shk/stuck/hyd per-well) | Nilai PdM = konfirmasi status + triage + indikasi menit; alarm tetap 0 |
| Δ Worst | 20% | FAR/B tak pernah terukur utk vib/ssi/bW (kampanye batal) | Alat tetap koheren di L0+L2 (+L1 shk/stuck/hyd) — bukan kegagalan, batas jujur |
| Ψ Wildcard | 10% | Label semantik salah lintas-well (STUCK_RT 0–3, shk severity-mix, hyd proxy) | Onset layer salah sasaran — TRIPWIRE sudah ada: kontrol-positif stuck 0/10 |
| Φ Contrarian | 10% | Ternyata persistence/rule SUDAH cukup utk nilai PdM kelas status | ML hanya dipertahankan shk/stuck/hyd-onset — arsitektur tetap sama (L0 kuat) |

**Tripwire (sinyal observabel → perbarui cabang):** FAR≤1 terukur per kelas · K-2
bit_wear dijalankan · kontrol-positif stuck disinkronkan (zona waktu) · S-E1 re-run ssi
· parse VIBLAT F-4/F-10/F-15 · GAINLOSSTOT F-1C/F-11.

---

## (d) HITUNGAN — angka keberhasilan alat PdM (prinsip operator #6)

Dihitung per ENGINE (7 unit), tier = kemampuan TERTINGGI yang terbukti hari ini:

| Tier | Jumlah | Engine |
|---|---|---|
| **LAYAK alarm otomatis** | **0 dari 7** | — (tidak ada: shk 0/9 fold FAR≤1 dgn recall>0; stuck FAR 9,9–1.440; hyd FAR 39–111/5,9; ssi/vib B+FAR belum terukur; bit_wear P/R/FAR belum + kalah persistence; tool_wear precision ≈0,5, G1 0/4) |
| **LAYAK peringatan (human-in-loop) — terbukti hari ini** | **3 dari 7** | shk (lead 2–9 mnt, well terkalibrasi) · stuck (triage manual, sumur mirip F-10) · hyd (K-ii indikasi dini lead 7 mnt, anotasi UNDERPOWERED) |
| **LAYAK peringatan BERSYARAT (menunggu ukur FAR/B4)** | **2 dari 7** | vib · ssi |
| **Tier tertinggi = TREN/indikasi saja** | **2 dari 7** | bit_wear (K-1) · tool_wear (skor LOTO + regime detector) |

Check: 0 + 3 + 2 + 2 = **7 ✓** (tanpa engine dihapus, tanpa engine dobel).

Angka ringkas keberhasilan alat PdM:
- **7/7 engine** punya peran terdefinisi dalam alat (tidak ada yang dibuang; 0 engine
  "gagal/buang" menurut kerangka baru).
- **0/7** layak alarm otomatis · **3/7** layak peringatan operasional hari ini ·
  **5/7** punya jalur peringatan (3 terbukti + 2 bersyarat) · **7/7** layak setidaknya
  konfirmasi-status/tren/indikasi pada batasnya masing-masing.
- Yang membatasi 0-alarm = **bukti B & FAR belum diukur** (vib, ssi, bit_wear) atau
  **sudah terukur dan di atas ambang** (shk, stuck, hyd, tool_wear) — BUKAN ketiadaan
  sinyal A.

---

## (e) GAP — kemampuan yang belum terisi engine mana pun

| # | Gap | Bukti | Diisi oleh (kandidat) |
|---|---|---|---|
| G1 | **DIAGNOSIS / akar-masalah** — 0 engine | identitas bit serial/dull/footage EDM BLOCKED (M2 §1b); shk ordinal 0–3 belum dievaluasi; stuck semantik 0/3 belum terdokumentasi | Kampanye ordinal shk +EDM unlock + dokumentasi semantik STUCK_RT |
| G2 | **ALARM OTOMATIS FAR≤1/24jam dgn recall>0** | 0/7 tercapai; bahkan syarat tren FAR≤6 baru 4 titik (shk) | Ukur FAR di kampanye penguatan; kalibrasi per-well OOS |
| G3 | **B3 pengurangan pemeriksaan tak perlu** | shk NEGATIF (−0,11…−53,75); belum terukur di vib/ssi/bit_wear/hyd/stuck (butuh data inspeksi operasional — tidak ada di Volve) | Definisi baseline aturan operasional + data beban-kerja rig |
| G4 | **Peringatan jangka panjang (>10–30 mnt)** | semua horizon ≤10 mnt (shk lead ≥30 mnt hanya per-fold di JSON); anchor bit-change/well-control berjam-jam tak terlayani | Kampanye onset H=30/60 (stuck prareg baru, bit_wear K-2 sensitivitas 30 mnt) |
| G5 | **Generalisasi lintas-wellbore** | hyd K-ii 1 wellbore; stuck F-12 belum terukur (STUCK_RT hanya depth-log); vib F-4/F-10/F-15 BELUM diparse; ssi S-E1 re-run belum jalan; shk F-10/F-12 lift ≈1; bit_wear 3 fold underpowered; tool_wear tak ada data drilling | Parse + fold tambahan (daftar per kelas di §c tripwire) |
| G6 | **C3 toleransi dropout sensor** | teruji hanya tool_wear + shk (+ablasi skor E2 stuck); belum di vib/ssi/bit_wear/hyd | Uji dropout kanal SHAP-atas + noise σ/10 (paket murah, tanpa data baru) |
| G7 | **Validitas label lintas-well** | kontrol-positif stuck 0/10; hyd K-ii label proxy; shk severity-mix beda; STUCK_RT 0–3 semantik belum ada | Verifikasi semantik + zona waktu (sinkron kontrol-positif) |
| G8 | **Onset bit_wear (K-2)** | 481/329 onset terverifikasi A1+PM; semua metrik onset = belum terukur; jalur termurah nol parse | Kampanye K-2 pra-reg (tes pembeda persistence-onset) |

---

## Baris Riset Pendahuluan (ringkas)

- Riset pendahuluan: `scientific-critical-thinking` — OBSERVED/DERIVED/BELUM-TERUKUR
  dipisah per engine; kontradiksi antar-evaluator diselidiki lalu direkonsiliasi (§b.2);
  hitungan tier diverifikasi balik (0+3+2+2=7).
- Riset pendahuluan: `statistical-analysis` — AUPRC/lift tidak dirata-rata antar kelas
  (plafon lift per fold berbeda: 15–196 vs 1,84–2,0 vs 2,0); FAR per skala aslinya;
  label UNDERPOWERED/CI95 tiap sumber dipertahankan.
- Riset pendahuluan: `what-if-oracle` — arsitektur diuji 5 cabang (Ω/α/Δ/Ψ/Φ) +
  tripwire eksplisit, prioritas aksi 61,8% pada cabang α (§c).
- Riset pendahuluan: `sequentialthinking` — 5 pikiran, 5/5 sukses (tool_call sequ-mcp).

## Sumber (7 dokumen primer, semua dibaca via read_file sesi ini)

`docs/V8_E_vib_CAPABILITY.md` · `docs/V8_E_ssi_CAPABILITY.md` ·
`docs/V8_E_bit_wear_CAPABILITY.md` · `docs/V8_E_stuck_CAPABILITY.md` ·
`docs/V8_E_hyd_CAPABILITY.md` · `docs/V8_E_shk_CAPABILITY.md` ·
`docs/V8_E_tool_wear_CAPABILITY.md` · kerangka `docs/V8_R1_ABC_SPEC.md`.

## Belum diverifikasi (verification-mandatory #3)

- Angka V6 yang dikutip di dalam dokumen sumber (mis. persistence vib/si, canary stuck)
  = kutipan dokumen sumber, tidak dihitung ulang di sesi ini (sumbernya sudah melalui
  audit V5_A1/V7 dan reproduksi evaluator masing-masing).
- Peta ini TIDAK mengeksekusi engine baru — semua kesimpulan = agregasi hasil 7
  eksekusi sebelumnya; kualitas keputusan tingkat-tier bergantung pada ketepatan kutipan
  angka per dokumen (dibaca langsung, bukan dari ingatan).
