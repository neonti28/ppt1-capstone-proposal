# V9-R1 — JUSTIFIKASI ILMIAH TIAP ENGINE (PAPER · RUMUS · BASELINE · TUGAS)

Task: `t_5c5c77e8` [R&D] · Board: capstone-v9-build · Tanggal: 2026-10-12 (WIB)
Status: SELESAI — 7 engine terjustifikasi, 27 sumber terverifikasi sesi ini (bukan karangan).
Sumbu: `docs/V9_PM1_ARCHITECTURE.md` (spesifikasi PM, §2 per engine) — dokumen ini TIDAK
mengubah spesifikasi; temuan penyimpangan metode → §10 (change-control, bukan ubah sepihak).
Kerangka penilaian: standar 3 lapisan A/B/C dari operator ("Evaluasi User.txt") — bukan gate lift 1,5.

> **Riset pendahuluan: `scientific-critical-thinking`** — tiap klaim metode dipisah
> OBSERVED (hasil verifikasi DOI/URL sesi ini, tercatat §1) vs DESAIN (keputusan PM yang
> saya kutip) vs INTERPRETASI R1 (§4.5 Fisher/Pearson — hipotesis dengan pembeda, bukan fakta);
> hipotesis "metode dipakai di luar tugasnya" diuji balik per engine (§2) dan TIDAK ditemukan.
> **Riset pendahuluan: `verification-mandatory`** — 27 sumber diverifikasi lewat
> api.openalex.org / api.crossref.org / doi.org / liveness URL pada 2026-10-12 (skrip
> `scratch/r1_verify_dois.py`, `r1_verify_batch2-5.py`, output mentah di §1); DOI yang gagal
> diverifikasi (10.1093/biomet/7.1.11, 10.1080/01621459.2012.710061, 10.1007/978-1-4757-3237-5)
> DITOLAK dan diganti kandidat benar yang lolos verifikasi — 0 sitasi tanpa verifikasi.
> **Riset pendahuluan: `statistical-analysis`** — baseline dinilai KESUAIAN-TUGAS-nya:
> deteksi status vs prediksi onset vs klasifikasi lintas-alat butuh baseline berbeda
> (persistence untuk kelas temporal, prevalence-random untuk AUPRC onset langka, majority-identity
> untuk LOTO, canary untuk kontrol memorisasi) — tidak ada baseline universal; rumus z median/MAD
> dipilih atas z parametrik karena data sensor skewed (uji asumsi normalitas tidak berlaku).
> **Riset pendahuluan: `what-if-oracle`** — 5 cabang risiko justifikasi Ω/α/Δ/Ψ/Φ + tripwire §9.
> **Riset pendahuluan: `consciousness-council`** — 5 arketipe menekan dokumen ini; ketegangan
> "sitasi kuat sedikit vs banyak" dan "temuan rumus PM1 salah" direkonsiliasi §10–§11.
> **Riset pendahuluan: `sequentialthinking`** (5 pikiran, 5/5 sukses, tool_call sequ-mcp):
> inventaris sumber → pemetaan 7 engine → hipotesis Fisher/Pearson → rencana verifikasi sitasi
> → lapisan tambahan + acceptance.
> **Riset pendahuluan: `literature-review`** — pencarian multi-sumber terdokumentasi (web_search
> 12 query, OpenAlex 7 query, Crossref 3 query, liveness 20 URL; akses 2026-10-12, §1);
> sintesis dikelompokkan per engine, bukan ringkasan per-paper.
> **Riset pendahuluan: `paper-lookup`** — DOI dicari/diverifikasi via OpenAlex + Crossref +
> doi.org resolve (3 jalur); kegagalan 429 Crossref dipindah ke OpenAlex (fallback terdokumentasi);
> "HTTP 403 dari penerbit = bot-block, bukan DOI mati" dipisahkan dari "404 = DOI salah".
> **Riset pendahuluan: `grounded-citations`** — ledger `sources.py` (27 entri, [1]–[27]);
> blok Sources dirender mesin, bukan diketik tangan; `verify` dijalankan sebelum final (§12).
> **Riset pendahuluan: `hypothesis-generation`** — interpretasi "Fisher/Pearson literal (R1)"
> diperlakukan sebagai 3 kandidat kompetitif (H1 Pearson-r+Fisher-z, H2 Fisher-exact+chi-2,
> H3 Fisher-information) dengan tes pembeda (§4.5); H2/H3 ditolak dengan alasan data, bukan asumsi.

---

## 1. METODE VERIFIKASI SITASI (bukti 0 karangan)

| Kode | Kondisi | Jumlah | Bukti |
|---|---|---|---|
| A | Lolos `api.openalex.org/works/https://doi.org/…` (judul+tahun cocok) | 22 | output `r1_verify_dois.py` / `r1_verify_batch3.py` — baris `OK` |
| B | Lolos `api.crossref.org` bibliographic query (judul cocok persis) | 3 ([25][26] + kandidat Iglewicz) | output `r1_verify_batch4.py` |
| C | Lolos liveness URL (HTTP 200, judul halaman cocok) | 8 dari 27 entri URL non-DOI | output `r1_verify_batch2/5.py` |
| D | GAGAL diverifikasi → DITOLAK, diganti | 4 kandidat | §13 |

Kandidat yang DITOLAK (tercatat agar tidak dikutip ulang): `10.1093/biomet/7.1.11` (404 —
pagination salah; Fisher 1915 yang benar = Biometrika 10:507–521 → `10.2307/2331838` = [15]),
`10.1080/01621459.2012.710061` (404 → PELT benar `10.1080/01621459.2012.737745` = [11]),
`10.1007/978-1-4757-3237-5` (404 → Good 2000 benar `10.1007/978-1-4757-3235-1` = [12]),
`10.1016/j.eswa.2014.01.041` (DOI milik paper UNRELATED — judul Crossref ≠ Fernández-Delgado;
diganti sumber JMLR resmi [6]). Catatan: `10.1023/A:1010933404324`, `10.1016/0148-9062(65)90022-7`
lolos doi.org resolve; `10.1080/01621459.2012.737745` & `10.1002/widm.1236` mengembalikan 403 di
doi.org (bot-block penerbit) tetapi judul+tahun cocok di OpenAlex → tetap dipakai dengan catatan.

## 2. PETA METODE ↔ TUGAS (cek anti salah-framing — tugas wajib #4)

| Engine | Jenis tugas sesungguhnya | Metode utama | Boleh untuk tugas ini? |
|---|---|---|---|
| vib | deteksi kondisi (status sekarang) | rule ambang + persistence + RF klasifikasi | ✅ klasifikasi status = deteksi; RF = penambah nilai, bukan pengganti rule |
| ssi | deteksi kondisi (status sekarang) | rule definisi SSI + RF | ✅ sama |
| bit_wear K-1 | deteksi kondisi (blok high_MSE) | persistence (engine utama) + RF screening | ✅ |
| bit_wear K-2 | prediksi onset (H=10 mnt) | RF-onset + persistence-onset (tes pembeda) | ✅ prediksi memang tugas K-2 |
| stuck K-i | deteksi anomali/kondisi (blok STUCK_RT) | persistence | ✅ |
| stuck K-ii | prediksi kejadian (onset) | E0 persistence · E1 rule · E2 z-stats · E3 RF | ✅ 4 engine setara-tugas, semua prediktor onset |
| hyd K-i | deteksi kondisi (residu SPPA) | median/MAD label + persistence (RF DILARANG, D-A5) | ✅ — sengaja TANPA ML |
| hyd K-ii | prediksi kegagalan (kick/loss proxy) | RF + fitur aliran; baseline statistik literal | ✅ |
| shk | deteksi anomali berlangsung + sub-onset H=10 | RF + persistence | ✅ (sub-onset = prediksi dini, sah) |
| tool_wear K-i | deteksi perubahan-regime dalam-run | change-point SSE + permutation + kalibrasi MAD | ✅ deteksi perubahan, bukan prediksi |
| tool_wear K-ii | klasifikasi status keausan lintas-alat (LOTO) | RF + ambang inner-LOO | ✅ — klaimnya GENERALISASI lintas-alat, BUKAN horizon prediksi waktu |

**Hasil cek: 0 kasus "ML prediksi dipakai untuk tugas deteksi kondisi".** RF muncul di kelas
status hanya sebagai lapisan skor penambah di atas engine dasar rule/persistence; kelas dengan
bukti RF merugikan (hyd-K-i, ΔB− 7/7) justru DILARANG memakai RF (keputusan PM D-A5).
Satu koreksi framing yang perlu ditulis terbuka: `tool_wear` K-ii di PM1 §2.7 disebut
"prediksi status keausan lintas-alat" — sifat sebenarnya = klasifikasi status dengan fold
LOTO (generalisasi antar-alat), lead 47,5 detik = TLead pada ambang operasi, BUKAN horizon
forecast; jangan menuntut metrik onset (B1) dari klaim ini (lihat §8).

---

## 3. JUSTIFIKASI PER ENGINE

Format: tugas · metode+rumus persis · sitasi · kecocokan-tugas · baseline relevan (+alasan) ·
sumber label + risiko sirkularitas · batas.

### 3.1 `vib` — deteksi kondisi getaran lateral

- **Tugas:** deteksi kondisi `VIBLAT_RT ≥ 32,17405 ft/s²` (status sekarang; TLead tidak berlaku).
- **Metode + rumus persis:**
  1. Rule ambang: `status(t) = 1[VIBLAT_RT(t) ≥ 32,17405]` (ambang definisi operasional rig — DESAIN PM, V6_R1 §4.2 menurunkan populasi 714 baris F-14 dengan ambang ini).
  2. Persistence: `ŷ(t) = y(t−1)` (satu grid 60 dtk). Justifikasi: metode naive/persistence adalah baseline standar deret waktu ketika status punya korelasi temporal kuat [13], dan pada kompetisi M4 metode sederhana terbukti sangat sulit dikalahkan model kompleks [14] — karena itu persistence BUKAN "baseline lemah" melainkan pembanding wajib yang harus dikalahkan ML untuk membuktikan nilai tambah.
  3. RF: `RandomForestClassifier(n_estimators=300, min_samples_leaf=5, class_weight="balanced_subsample", random_state=42)`, fitur statistik jendela 10 menit (mean/std/slope/last/frac), imputer median fold-safe. Justifikasi: Breiman [5] — akurasi ensemble pohon terdekorrelasi via bagging + subsampling fitur, tahan overfitting pada fitur noise; Fernandez-Delgado [6] — RF termasuk kelompok klasifikator terkuat pada benchmark masalah klasifikasi dunia-nyata (bukan klaim pasti-menang, dipakai sebagai justifikasi pemilihan awal, hasil tetap diukur per fold); preseden klasifikasi dysfungsi pengeboran dari data surface: Saini 2020 [23], Liu 2025 [24].
- **Baseline relevan + alasan:** (a) rule ambang = sistem hari-ini, tolok ukur "apa yang sudah bisa dilakukan tanpa ML"; (b) persistence = tolok korelasi temporal (harus dikalahkan agar RF bernilai); (c) canary-kedalaman (RF hanya fitur depth/dbtm) = KONTROL memorisasi posisi — detektor yang skornya didominasi kedalaman sedang "mengingat peta", bukan membaca getaran.
- **Sumber label + risiko sirkularitas:** kanal MWD `VIBLAT_RT`; `VIBLAT_RT` dan seluruh turunannya DILARANG jadi fitur (tabel PM1 §2.8); `WHIRL_RT`/`BOUNCE_RT` dilarang total (duplikat identik row-level, bug V6_R1 §4.3). Risiko tersisa: label getaran berasal dari instrumen yang bisa drift antar-wellbore → C-semantik.
- **Batas:** input = surface+depth; kecukupan surface untuk memprediksi getaran downhole terdukung Saadeldin 2023 (R>0,9, 3 tipe getaran, well tak terlihat) [22] — tetapi bukti lemah untuk getaran aksial/lateral (V6_R1 §3.3: univariat AUC ≈0,54) → klaim hanya "skor penambah", bukan detektor tunggal.

### 3.2 `ssi` — deteksi kondisi stick-slip torsional

- **Tugas:** deteksi kondisi `SSI(CRPM_RT) ≥ 1` (status sekarang).
- **Metode + rumus persis:**
  1. Label/rule definisi: `SSI = (max − min) / (2 · mean)` atas jendela CRPM minimal 10 sampel; label 1 bila `SSI ≥ 1` — rumus + grading persis dari Liu et al. 2025 *Thermal Science* (Eq. SSI; grading `SSI<1 / 1<SSI≤3 / SSI≥3`) [3]; klasifikasi severity stick-slip dengan ML sudah mapan (Hegde et al. 2019, label SSI dilatih dari data permukaan) [4].
  2. RF kontrak seragam §3.1 (parameter identik, seed 42).
  3. Persistence `ŷ(t)=y(t−1)`.
- **Kecocokan-tugas:** SSI adalah definisi statistik jendela (bukan kejadian mendatang) → tugas = deteksi status; rule definisi = detektor paling langsung (nol pelatihan); nilai RF di sini = skor ranking di atas status (terukur: RF≥canary 5/5; persistence kalah 0/5 — hasil OBSERVED V8, dipakai ulang sebagai dasar keputusan).
- **Baseline relevan + alasan:** (a) rule SSI definisi = sistem hari-ini; (b) persistence = detektor otomatis apabila stick-slip persisten antar-grid (terbukti lemah 0/5 → dicatat sebagai KEMAMPUAN baseline, bukan aib); (c) canary-kedalaman = kontrol memorisasi posisi (kanal SSI sangat depth-correlated di Volve).
- **Sumber label + risiko sirkularitas:** turunan `CRPM_RT` → `CRPM_RT` dilarang jadi fitur. Risiko: sumber Liu memakai RPM downhole — konsistensi Volve memakai collar RPM juga (V6_A2 §150); wajib verifikasi semantik lintas-wellbore sebelum 11-fold re-run.
- **Batas:** 3/5 fold CI-bawah menyentuh no-skill + 2 fold UNDERPOWERED (<30 positif) → layer keyakinan wajib tampil (bukan angka tunggal).

### 3.3 `bit_wear` — keausan/balling (K-1 status · K-2 onset)

- **Tugas:** K-1 = deteksi kondisi (blok `high_MSE`); K-2 = prediksi onset blok (H=10 mnt).
- **Metode + rumus persis:**
  1. Teale MSE (label K-1): `MSE = WOB/A + (120·π·N·T)/(A·ROP)` (unit field psi, in², RPM, ft·lb, ft/hr; versi SI setara `MSE = WOB/A + 2π·N_rps·T/(A·ROP)`) — Teale 1965 [1]. Kolom MSE USROP sudah diverifikasi independen di V6_R1 (recompute selisih median 0,005%, korelasi log10 0,9999999999989). Aturan tipologi (MSE vs MSE/DS → vibrasi vs keausan vs balling) dari Menand & Mills [2]: `DS = WOB/(R·DOC)`, `DOC = ROP/(60·RPM)`.
     ⚠ **Temuan (change-control, §10-C1):** rumus yang tertulis di PM1 §2.3 baris 201 —
     `MSE = (WOB/Am) + (480·N·π)/TOR` — TIDAK cocok secara dimensi dengan Teale 1965 (suku kedua
     tanpa ROP dan tanpa luas bit). Rumus benar = bentuk Teale di atas. Label USROP tetap sah
     karena dihitung dari kolom tersimpan yang terverifikasi Teale; yang salah hanya kutipan
     rumus di spesifikasi → usulan koreksi teks via change-control.
  2. Persistence-status: `ŷ(t)=y(t−1)`; persistence-onset: `ŷ_onset(t)=onset(t−1)`.
  3. RF K-1/K-2 kontrak seragam (§3.1); K-2: jendela positif `[t0−H, t0)`, H=10 mnt (sensitivitas 30).
  4. Fitur geologi penguat (korelasi UCS — tugas wajib #1): `UCS = 2,922·φ^(−0,96)` MPa (Horsrud 2001, shale Tertiary North Sea — formasi terdekat geologi Volve) [25]; kompilasi Chang et al. 2006 Eq.(27) `UCS = 143,8·e^(−6,95φ)` MPa (porositas sedang, UCS 30–150 MPa) [26]; varian Rzhevsky & Novick `UCS = 276·(1−3φ)²` MPa dikutip lewat tabel Chang 2006 [26] (sumber primer buku 1971 — diverifikasi sebagai kutipan sekunder, jujur dicatat).
     **Kecocokan-tugas:** korelasi UCS di sini = FITUR konteks formasi (join per MD) untuk
     meningkatkan daya beda K-1/K-2 — BUKAN label keausan dan BUKAN engine prediksi tersendiri;
     rasio φ→UCS dipakai untuk menormalisasi kesulitan batuan, bukan untuk memprediksi waktu kegagalan.
- **Baseline relevan + alasan:** (a) persistence-status (V8: menang 4/4 vs RF → K-1 memang didesain berpusat pada persistence; alasan reframing V7); (b) canary-kedalaman = kontrol "mengingat posisi" (SHAP K-1 didominasi MD/TVD — risiko nyata, terukur); (c) prevalence-random: AUPRC acak = prevalence → plafon lift 1/prev (F-15S 1,84; F-5 2,11) wajib dilaporkan agar lift 1,5 tidak salah baca; (d) **persistence-onset = tes pembeda K-2**: bila persistence-onset ≥ RF mayoritas fold → hipotesis "kegagalan V7 = formulasi status (bukan minimnya ML)" DITOLAK. Persistence-onset relevan karena onset blok di data depth-ordered sangat persisten per grid — ini baseline yang harus dikalahkan, bukan formalitas.
- **Sumber label + risiko sirkularitas:** blok `high_MSE_bit_wear` dari `USROP_labeled.csv` (definisi artefak V2, dikunci pra-reg); kanal pembentuk MSE (WOB/ROP/RPM/TORQ) DILARANG jadi fitur (asersi E1d PASS); K-2: jendela DALAM blok Dibuang (bukan negatif) untuk mencegah label bocor ke jendela pelatihan. Risiko: label = kuantil internal (P75), bukan kejadian perawatan nyata → K-1 terdeteksi ≠ bit rusak; hanya "zona inefisiensi MSE".
- **Batas:** K-2 = nol angka (kampanye pra-reg belum jalan); K-1 P/R/FAR belum terukur; geologi-join kandidat (409 picks, flags SAND/CARB) = penguat C2 yang belum diuji.

### 3.4 `stuck` — stuck pipe (K-i status · K-ii onset)

- **Tugas:** K-i = deteksi kondisi blok `STUCK_RT`; K-ii = prediksi onset 0→1, H=10 mnt.
- **Metode + rumus persis:**
  1. `E1_rule` (2-dari-3): `alarm = 1[ (z(TQA)>2) + (z(HKLD)>2) + (ROP-drop ≥ 30%) ≥ 2 ]`, `z = 0,6745·(x − median)/MAD` jendela 60 menit — z robust median/MAD: definisi MAD NIST [7], faktor skala 0,6745 (= MAD/0,6745 ≈ σ untuk normal) NIST [8], pemakaian median/MAD sebagai detektor anomali tahan-outlier: Rousseeuw & Hubert [9]. Keputusan 2-dari-3 = aturan mayoritas kanal (DESAIN) — menekan FP kanal tunggal; bukan klaim statistik eksternal.
  2. `E2_stats`: skor = `z(TQA) + z(HKLD) + z(ROP-drop)`, ambang q95 di TRAIN (pra-reg) — z yang sama [7][8][9].
  3. `E3_RF`: `RandomForestClassifier(n_estimators=200, random_state=42)`, 55 fitur; ambang q95 train, tidak dioptimasi pasca-hasil [5].
  4. Persistence-onset E0: `ŷ(t)=y(t−1)` pada deret onset — baseline naive [13] yang secara konstruksi recall 0% (onset jarang terjadi tepat di grid setelah perubahan) — diperlakukan sebagai tes pembeda kejujuran: metode yang DIHARAPKAN kalah di sini justru mengkalibrasi apakah metode lain menang karena skill atau karena kebetulan.
- **Kecocokan-tugas:** K-ii = prediksi kejadian mendatang → wajar memakai skor ranking + threshold pra-reg; anchor kelayakan B2 = peringatan dini 2,67–7,37 menit dari Crossformer pada data Volve yang SAMA [19] → tolok "waktu bertindak" berasal dari preseden setara, bukan angka karangan; jalur label-tanpa-anotasi (autoencoder hanya data normal, AUC 0,958 di Volve) [20] dan LSTM-AE unsupervised [21] = preseden bahwa onset stuck bisa dilabeli tanpa anotasi manual (relevan bila kampanye butuh label tambahan).
- **Baseline relevan + alasan:** (a) persistence-onset (tes pembeda, lihat di atas); (b) prevalence-random (AUPRC = prev; kontrol ukuran langka); (c) canary-kedalaman (E3 V8 terukur 0,326–0,331 < canary 0,410 → fakta "RF kalah canary" justru menunjukkan deteksi terbantu posisi, bukan proses stuck); (d) anchor TLead 2,67–7,37 mnt [19] sebagai tolok B2 (khusus kelas ini — dilarang dipinjam ke kelas lain).
- **Sumber label + risiko sirkularitas:** primer `STUCK_RT` (ffill, dikunci pra-reg; strict = sensitivitas); `STUCK_RT` dilarang jadi fitur; kontrol-positif `labels_curated_v2` (884 event) dari kurasi DDR. **Risiko sirkularitas/semantik tertinggi di antara 7 engine:** (i) semantik skala 0/1/2/3 beda antar-well (F-10 didominasi "3", F-14 "1") → prasyarat pra-reg Fase 0; (ii) prevalence 66,9% vs 49,4% belum direkonsiliasi; (iii) kontrol-positif 0/10 → sinyal peringatan-dini belum terbukti terhadap kejadian nyata.
- **Batas:** FAR 9,9–1.440/24jam → L1/L0 BELUM; E1 hanya P 0,457 di F-10; fold F-12 belum terukur.

### 3.5 `hyd` — anomali hidrolik (K-i status · K-ii prediksi)

- **Tugas:** K-i = deteksi kondisi residu `SPPA` (`|z|>2`); K-ii = prediksi kick/loss proxy (H=10 mnt).
- **Metode + rumus persis:**
  1. K-i label: bin `qcut(TFLO, 10)`; `z = 0,6745·(SPPA − median_bin)/MAD_bin`; status = `|z| > 2` [7][8][9]. Catatan sensitivitas terdokumentasi (10 bin → 58.317 baris; 20 bin → 47.359) — jumlah bin = bagian label, dikunci pra-reg.
  2. K-i engine: `ŷ(t) = y(t−1)` persistence (delay 0–3 menit, nol look-ahead) [13][14]. **RF DILARANG di kelas ini** (D-A5): alasan EMPIRIS — ΔB RF−persistence negatif 7/7 (V8-E_hyd, OBSERVED), jadi ini batas tugas yang terukur, bukan dogma anti-ML.
  3. K-i rule pembanding: ambang `|z|` manual (baseline "sistem hari-ini").
  4. K-i label engine = pembentuk label → persistence hanya MEMAKAI label tersebut; klaim deteksi = "status persisten terkonfirmasi", bukan prediksi.
  5. K-ii label: `ΔV_pit(t) = Σ perubahan volume 12 kolom pit`; `z = 0,6745·(r10(ΔV_pit) − median_well)/MAD_well`; episode `|z|>2` sustain ≥5 mnt, merge <30 mnt, syarat sirkulasi ≥500 L/min [7][8]. Proses deteksi volume-pit sebagai indikator kick = praktik mapan: IDAPS (deteksi influx saat pompa berhenti, SPE) [17], peringatan dini kick via sinyal mud-logging [18].
  6. K-ii engine: RF kontrak seragam + fitur aliran (mass-balance) [5]; varian konservatif vs +flow-in (AUPRC 0,030 vs 0,228 = syarat fitur aliran, OBSERVED V8).
  7. **Fisher & Pearson literal (baseline K-ii) — INTERPRETASI R1 (lihat §4.5):**
     `r = Σ(x−x̄)(y−ȳ) / √(Σ(x−x̄)²·Σ(y−ȳ)²)` (Pearson product-moment antara *flow imbalance* `FlowIn−FlowOut` dan `ΔV_pit` per jendela), diuji dengan transformasi Fisher `z' = atanh(r) = ½·ln((1+r)/(1−r))`, `SE(z') = 1/√(n−3)`; detektor literal: `|r|` turun drastis / berganti tanda dari baseline korelasi rolling = anomali mass-balance. Sitasi: distribusi korelasi sampel (Fisher 1915) [15], probable error + inferensi r (Fisher 1921, *Metron*) [16].
- **Kecocokan-tugas:** K-i = deteksi kondisi → statistik robust + persistence (tanpa horizon); K-ii = prediksi → RF + baseline korelasi literal; aturan z-pit punya TLead=0 by construction (menandai saat itu juga) sehingga HANYA relevan sebagai baseline "sistem hari-ini" untuk B3, bukan sebagai pembanding TLead.
- **Baseline relevan + alasan:** K-i: (a) persistence (engine terbaik terukur — tolok mutlak); (b) rule `|z|` manual (B3: berapa banyak pemeriksaan yang dipangkas); K-ii: (a) prevalence-random (prev_test 0,0037 → plafon lift 268, wajib tampil agar lift 61,6 tidak dibaca buta); (b) rule z-pit (sistem hari-ini, TLead=0); (c) Fisher/Pearson literal — detektor statistika klasik termurah yang SEHARUSNYA menangkap ketidakcocokan mass-balance; bila RF tidak mengalahkan korelasi literal + persistence, RF tidak bernilai tambah.
- **Sumber label + risiko sirkularitas:** K-i: label = turunan kanal (`SPPA`, `TFLO`) → kedua kanal DILARANG jadi fitur (asersi lolos V8); K-i label juga menjadi "kebenaran" bagi persistence → deteksi persistence = konfirmasi-status, bukan prediksi. K-ii: label PROXY (z ΔV_pit) — kanal pit DILARANG jadi fitur; risiko: proxy bisa picu pada aktivitas lumpur non-kick (surge/swab) → anotasi wajib; 1 wellbore saja → C1 lemah.
- **Batas:** K-i FAR_t 38,8–110,7/24jam (skala jendela) = beban blok, bukan alarm; peringatan-dini kejadian nyata 0/1 (n=1) → K-ii indikasi dini ber-annotasi ketidakpastian, L0 belum.

### 3.6 `shk` — deteksi anomali/dysfunction bit bounce

- **Tugas:** deteksi anomali sedang berlangsung (`SHKRSK_RT ≥1`; ordinal 0–3 opsional S-B3) + sub-tugas onset blok H=10 mnt.
- **Metode + rumus persis:**
  1. RF kontrak seragam (§3.1; 11 kanal MWD ×5 statistik = 55 fitur; seed 42) [5][6]; reproduksi V6 7/7 <1e-9 = kontrol validitas pipeline (internal).
  2. Persistence `y_prev_shk`; grid tau pra-reg {0,05; 0,10; 0,20, 0,30, 0,50}.
  3. `FAR = FP / jam_operasi_negatif` (per 24 jam) — metrik beban kerja (definisi operasional, S7).
  4. `B3 = kurangi_ragu = 1 − FP_engine / FP_display_status_quo` (pengurangan pemeriksaan relatif terhadap tampilan hari ini — bukan metrik literatur, definisi proyek).
  5. Opsi S-B3 ordinal: latih regresi/ordinal lalu TURUNKAN ke ambang biner `≥1` yang SAMA — keputusan biner tidak berubah, gate tidak digeser (mengikuti pelajaran Liu: klasifikasi dysfungsi dari surface + forensik bit [24]).
- **Kecocokan-tugas:** label `SHKRSK_RT` = status risiko MWD saat ini → deteksi; lapisan onset (B1/TLead) hanya sub-tugas dengan H eksplisit — di sanalah klaim prediksi dini dihitung, terpisah dari metrik status; ML dipertahankan di kelas ini karena terukur RF≥persistence B1 di 9/9 (nilai tambah onset nyata) sementara statusnya tetap ber-orchestrasi rule/persistence.
- **Baseline relevan + alasan:** (a) canary-kedalaman (G2 lolos 6/9 — kontrol memorisasi); (b) persistence (tolok temporal); (c) prevalence-random (prev 0,6–9,7% → plafon lift besar, wajib tampil); (d) display MWD status-quo = baseline B3 (satu-satunya baseline yang bisa menjawab "apakah alat ini mengurangi kerja inspeksi?" — khusus tugas deteksi yang diketahui operator).
- **Sumber label + risiko sirkularitas:** `SHKRSK_RT` dilarang jadi fitur; risiko semantik: severity-mix beda antar-well (F-12 66% non-null ≥2 vs F-14 40%) → verifikasi sebelum fold eksternal; surface-only cukup untuk shock TIDAK diklaim (V6_R1 §3.3) — input memang memakai kanal MWD, jadi kelas ini terikat ketersediaan MWD.
- **Batas:** FAR≤1 dgn recall>0 = 0/9 fold; B3 negatif terukur (−0,11…−53,75) di tau ≤0,20; C2 drop 49–93% per kuartil → tier L2 + L1 well-terkalibrasi saja; kalibrasi lintas-well DILARANG (D-A4).

### 3.7 `tool_wear` — keausan mata bor (K-i change-point · K-ii LOTO)

- **Tugas:** K-i = deteksi perubahan-regime dalam-run (bengkel, detik); K-ii = klasifikasi status keausan lintas-alat (LOTO).
- **Metode + rumus persis:**
  1. K-i change-point 1-split SSE per fitur: `SSE(τ) = Σ_{t≤τ}(x_t − μ₁)² + Σ_{t>τ}(x_t − μ₂)²`, `τ* = argmin_τ SSE(τ)`; signifikansi via **permutation test 500×**: acak urutan seri, hitung ulang `min SSE`, `p = (1 + #{SSE_perm ≤ SSE_obs})/(1+500)`, ambang p=0,002. Justifikasi: survei metode change-point offline [10] (SSE/least-squares segmentation = family dasar); PELT/Killick 2012 [11] = referensi optimalitas deteksi changepoint (konteks: mengapa pencarian pecahan tunggal dengan uji valid adalah deteksi offline yang sah); metode permutation tanpa asumsi distribusi (Good 2000) [12] — cocok karena 469 jendela 1 detik non-normal dan n kecil per run.
  2. Kalibrasi within-tool: `z = (x − median(R01 30% awal))/MAD`, alarm bila ≥5 dari 27 fitur `|z|>3` [7][8] — median/MAD dari sampel awal alat baru = referensi "normal" yang tahan outlier.
  3. K-ii RF kontrak seragam [5]; ambang operasi = pooled inner-LOO F1 (tanpa peeking test); varian FAR-terkalibrasi: kuantile skor R01 agar laju alarm baseline ≤1/menit.
  4. Rule 3-RMS: alarm amplitudo `RMS` 3-sigma kanal (baseline sederhana).
- **Kecocokan-tugas:** K-i = deteksi KETIADAAN-stasioner → statistik perubahan-titik (bukan klasifikasi, bukan prediksi horizon) — tugas dan metode satu-ke-satu; tes pembeda t_cp (bila cp selalu <5 dtk → artefak termal, sub-klaim gugur) sudah dijalankan: hasil 0/8 artefak, TAPI spesifisitas gagal (cp signifikan 8/8 termasuk alat baru, precision 0,50) → kemampuan = "detektor perubahan-regime", klaim "onset progresi keausan" TERDUKUAT lemah. K-ii = generalisasi antar-alat (LOTO), jadi RF klasifikasi + split LOTO = desain yang benar untuk klaim lintas-alat.
- **Baseline relevan + alasan:** (i) rule 3-RMS + validity test t_cp (sistem hari-ini bengkel); (ii) canary 3-RMS AUPRC 0,516–0,612 + **identity-run majority** (prediksi identitas run = peluang 0,5 → plafon lift 2,0; baseline ini spesifik tugas LOTO dengan label identitas-run); (iii) **persistence N/A — DINYATAKAN, bukan dihilangkan**: label konstan dalam satu run sehingga `y(t−1)` ≡ label run → persistence tidak terdefinisi sebagai pembanding di sini; kejujuran mendeklarasikan baseline tidak relevan > menghilangkannya diam-diam (keputusan PM §2.7, sah).
- **Sumber label + risiko sirkularitas:** label = identitas run (desain dataset Mendeley `th4yv974r2`: 4 alat × 2 run) — BUKAN turunan fitur → anti-sirkular terpenuhi; anchor K-i: akhir R02 (alat tumpul) + kontrol R01 (alat baru). Risiko tersisa: **confound urutan-run** (R02 selalu setelah R01 → perubahan termal/wear tak terpisah; transfer ke rig TIDAK diklaim), dan label identitas-run bisa "kebetulan" mudah ditebak dari offset waktu → canary identity-run ada untuk itu.
- **Batas:** K-ii precision biner 0,50–0,56 ≈ peluang (baca sebagai ranking + FAR-terkalibrasi, bukan klasifikasi pasti); K-i G1 0/4 (plafon lift 2,0 — tugas beda, gate lift kelas kejadian TIDAK boleh dituntut di sini); lead = detik bengkel, jangan dijumlah dengan menit rig (D-A7).

---

## 4. ANALISIS TAMBAHAN WAJIB

### 4.1 Ringkasan baseline-relevan per tugas (tugas wajib #3)

| Engine | Baseline relevan | Alasan kesesuaian tugas |
|---|---|---|
| vib | rule ambang · persistence · canary-depth | sistem-hari-ini · korelasi temporal · kontrol memorisasi posisi |
| ssi | rule SSI definisi · persistence · canary-depth | definisi kanal = detektor paling langsung · temporal · posisi |
| bit_wear K-1 | persistence-status · canary · prevalence-random | toleransi naive pada status persisten · posisi · plafon lift AUPRC |
| bit_wear K-2 | persistence-onset · prevalence-random | tes pembeda reframing · langka → AUPRC=prev |
| stuck K-i | persistence · canary | status blok persisten · posisi |
| stuck K-ii | persistence-onset · prevalence-random · canary · anchor 2,67–7,37 mnt [19] | tes pembeda · langka · posisi · B2 khusus kelas |
| hyd K-i | persistence · rule \|z\| manual | engine terbaik terukur · beban-kerja B3 |
| hyd K-ii | prevalence-random · rule z-pit (TLead=0) · Fisher/Pearson literal [15][16] | plafon lift 268 · sistem-hari-ini · detektor statistika termurah |
| shk | canary · persistence · prevalence-random · display status-quo | posisi · temporal · plafon · B3 (satu-satunya baseline beban-kerja) |
| tool_wear K-i | rule 3-RMS + t_cp validity | sistem-hari-ini bengkel |
| tool_wear K-ii | identity-run majority (plafon 2,0) · canary 3-RMS · persistence N/A (dinyatakan) | spesifik LOTO · posisi · label konstan dalam run |

Tidak ada baseline universal; setiap baseline menjawab ancaman validitas yang BERBEDA:
persistence = "apakah ML mengalahkan korelasi waktu?", canary = "apakah model cuma mengingat
kedalaman/identitas?", prevalence = "apakah lift terbaca benar untuk kelas langka?",
rule/display = "apakah alat mengungguli sistem hari-ini?".

### 4.2 Label & risiko sirkularitas per engine (tugas wajib #5)

Tabel ringkas (deskripsi penuh per engine §3):

| Engine | Sumber label | Kanal terlarang jadi fitur | Risiko sirkularitas utama | Mitigasi |
|---|---|---|---|---|
| vib | kanal MWD `VIBLAT_RT` | VIBLAT + WHIRL/BOUNCE (duplikat) | drift instrumen antar-well | asersi anti-sirkular D1 + C-semantik |
| ssi | turunan `CRPM_RT` | CRPM_RT | label = fungsi kanal; ML bisa "belajar rumus" dari proxy | CRPM dilarang; fold lintas-well |
| bit_wear | blok high_MSE (Teale, P75) | WOB/ROP/RPM/TORQ | label kuantil internal ≠ kejadian perawatan | E1d PASS; bahas sebagai zona inefisiensi |
| stuck | `STUCK_RT` + kontrol DDR | STUCK_RT | semantik 0–3 beda-well; prev 66,9 vs 49,4 | prasyarat pra-reg Fase 0 (gerbang keras) |
| hyd K-i | residu SPPA vs bin TFLO | SPPA/TFLO/SPM | label = z(kanal yang sama) → persistence = konfirmasi diri | dinyatakan sbg deteksi-status; klaim prediksi pindah ke K-ii |
| hyd K-ii | z ΔV_pit (PROXY) | 12 kolom pit + GAINLOSSTOT | proxy ≠ kick nyata; non-kick mud activity | anotasi proxy wajib; kontrol-positif |
| shk | `SHKRSK_RT` | SHKRSK_RT | severity-mix beda-well | verifikasi semantik sebelum fold eksternal |
| tool_wear | identitas run (desain) | (tidak ada kanal sumber) | confound urutan-run R02>R01 | transfer ke rig TIDAK diklaim; canary identity-run |

### 4.3 Uji-pembuka: apakah ada metode dipakai di luar tugasnya?

Kerangka hipotesis (hypothesis-generation): H0 "ada Salah framing"; kandidat penemuan:
(a) ML prediksi untuk deteksi kondisi; (b) baseline universal; (c) metrik onset dituntut dari
kelas status; (d) persistence disembunyikan. Hasil pemeriksaan: (a) 0 temuan (§2);
(b) 0 (§4.1); (c) 0 — B4 (margin status) dipakai di kelas status, B1/TLead hanya kelas onset;
(d) 0 — persistence-onset bahkan dipakai sebagai TES PEMBEDA, dan persistence-N/A tool_wear
dinyatakan eksplisit. **Kesimpulan: 0 kasus salah-framing pada spesifikasi PM1 §2.**
Satu-satunya anomali metode = kesalahan kutipan rumus Teale di PM1 §2.3 → §10-C1 (change-control),
bukan perubahan engine.

### 4.4 Cek semantik metrik lintas-tugas (anti-persetaraan gate)

- AUPRC/lift dibaca terhadap plafon 1/prev per kelas (dilaporkan) — lift 1,5 pada kelas
  plafon 1,84 ≠ makna lift 1,5 pada plafon 268.
- FAR per skala aslinya: jendela/24jam (vib/ssi/hyd/shk), blok/hari, menit (tool_wear) —
  konversi-skala wajib dianotasi; FAR lintas-kelas tanpa konversi dilarang.
- tool_wear (detik bengkel) TIDAK digabung lead-time dengan rig (menit) — D-A7.
- Fold UNDERPOWERED (<30 positif) dilabeli, tidak dihitung mayoritas.

### 4.5 Fisher/Pearson literal — 3 hipotesis kompetitif (temuan interpretasi)

PM1 menulis baseline "Fisher & Pearson literal (R1)" tanpa definisi (terverifikasi: grep
seluruh `docs/*.md` hanya menemukan frasa itu di V9_PM1 — tidak ada di V8/V6 → memang tugas R1
mendefinisikan). Kandidat:

| # | Hipotesis | Pembeda | Verdict |
|---|---|---|---|
| H1 | Pearson-r literal (mass-balance in-out vs ΔV_pit) + Fisher z-transformation untuk signifikansi r | butuh data kontinu → ada (12 kolom pit, flow); literal, murah, cocok sbg baseline detektor anomali hubungan | **DIPILIH** |
| H2 | Fisher exact + Pearson chi-square (asosiasi kategorikal) | butuh variabel kategorikal — hyd K-ii kontinu + label biner; tidak cocok sbg detektor mass-basis kontinu | ditolak |
| H3 | Fisher information | tidak "literal"/murah; tak ada di preseden proyek | ditolak |

Rumus H1: lihat §3.5 butir 7; sitasi [15][16]. Risiko H1 salah-tebak maksud PM = rendah
(konsekuensi hanya baseline tambahan, tidak mengubah engine); tetap terbuka lewat change-control
§10-C2. Tes pembeda lanjutan bila ada keraguan: hitung korelasi literal + z-test pada fold yang
sama dengan RF — bila literal ≥ RF, RF K-ii kehilangan justifikasi nilai-tambah.

---

## 5. WHERE-IF-ORACLE (risiko justifikasi — 5 cabang)

| Cabang | Bobot | Skenario | Konsekuensi | Robust action |
|---|---|---|---|---|
| Ω Best | 15% | 27/27 sumber valid + kesesuaian metode 7/7 (kondisi saat ini) | dokumen jadi kontrak sitasi E_ML/E_STAT/E_RULE | pertahankan ledger |
| α Likely | 45% | 1–2 sitasi digugat pihak ketiga | ganti dengan kandidat redundan yang sudah diverifikasi ([13]/[14] untuk persistence; [7][8][9] untuk z-robust; [10]/[11]/[12] untuk change-point) | ledger per metode ≥2 sumber |
| Δ Worst | 20% | ternyata ada metode tersembunyi di luar tugas | pemeriksaan §4.3 sudah dijalankan sebelum hasil → 0 temuan; temuan baru = change-control | cek ulang §2 bila spesifikasi berubah |
| Ψ Wildcard | 10% | "Fisher/Pearson" maksud PM ≠ H1 | interpretasi ditulis eksplisit §4.5, tidak dikubur; perubahan = teks baseline saja | change-control §10-C2 |
| Φ Contrarian | 10% | persistence/rule terbukti sudah cukup (terdukung hyd/bit_wear) | argumen baseline R1 justru MENGUAT — baseline relevan dibuktikan bekerja; alat tetap koheren tanpa menaikkan klaim ML | tidak ada tindakan darurat |

**Tripwire (sinyal → perbarui cabang):** (i) sitasi digugat dengan bukti primer → cek silang
OpenAlex/Crossref dalam 1 run; (ii) ada tim yang menuntut gate seragam → audit A1; (iii) PM
menjawab definisi Fisher/Pearson berbeda → update §4.5 via change-control.

## 6. CONSCIOUSNESS-COUNCIL (5 arketipe)

- **Architect:** struktur "tugas → metode → baseline → label" seragam 7 engine membuat dokumen
  ini jadi kontrak lintas-tim. Risiko over-engineering ditahan: tidak ada tabel yang tidak
  menjawab acceptance.
- **Empiricist:** hanya klaim ber-DOI/URL yang lolos verifikasi masuk; 4 kandidat gagal
  diverifikasi DITOLAK, bukan dilunakkan (§1, §13). Keberatan utama: kutipan V6/V8 (angka OBSERVED)
  tidak dihitung ulang sesi ini — dicatat, bukan diaku ulang.
- **Minimalist:** 27 sumber untuk 7 engine = 2–4 per engine; tidak menambah sitasi hias.
  Persistence/persistence-onset/median-MAD/RF dipakai lintas engine sebagai 4 modul, bukan 15 varian.
- **Pragmatist:** E_ML/E_STAT/E_RULE menerima rumus siap-pakai + baseline siap-hitung (S9);
  tidak ada bagian yang hanya "esai".
- **Contrarian (tekanan inti):** "0 kasus salah-framing" bisa jadi klaim nyaman → diuji dengan
  4 kandidat penemuan eksplisit §4.3 dan 3 hipotesis Fisher/Pearson §4.5; temuan nyata justru
  kesalahan rumus Teale di spesifikasi PM (§10-C1) — kontra-argumen bahwa dokumen PM bebas cacat
  DITOLAK dengan bukti baris.

**Sintesis:** konvergensi = 7 engine terjustifikasi dengan ledger mekanis; ketegangan yang
dipertahankan = "angka V6/V8 dikutip, tidak dihitung ulang di sesi ini" (ikut §7 batas jujur).

## 7. BATAS JUJUR / BELUM DICEK

1. Angka OBSERVED V8 (ΔB, lift, FAR, dst.) dikutip dari PM1/V8 sebagai DESAIN-spasifikasi —
   TIDAK dihitung ulang sesi ini; kualitasnya mengikuti audit A1 V8.
2. Verifikasi sitasi = metadata (judul/tahun/DOI/URL hidup) — TIDAK membaca teks penuh semua
   paper; kecuali ekstrak Menand (hpinc, PDF hidup) + teks Liu Thermal Science (V6 run-3).
3. Rumus persis ditulis mengikuti sumber yang diverifikasi; konsistensi numerik implementasi
   = tanggung jawab E_STAT/E_ML saat run (JSON primer, S6).
4. Definisi "Fisher/Pearson literal" = interpretasi R1 (H1) — menunggu konfirmasi PM bila beda.
5. Liveness URL diukur pada 2026-10-12; DOI penerbit dengan 403 (Taylor & Francis, Wiley)
   = bot-block, dicatat.

## 8. ACCEPTANCE SELF-CHECK

| # | Syarat | Bukti |
|---|---|---|
| a | 7 engine terjustifikasi dgn sitasi asli | §3.1–§3.7 (vib, ssi, bit_wear, stuck, hyd, shk, tool_wear) — semua dikutip dari ledger [1]–[27] terverifikasi §1 |
| b | tiap engine punya baseline relevan + alasannya | kolom "Baseline relevan + alasan" §3.1–3.7 + tabel ringkas §4.1 |
| c | rumus persis tertulis per metode | rule/persistence/RF/SSI/Teale/z-MAD/SSE-permutation/Fisher-z — semua di §3 |
| d | 0 sitasi karangan | 27 entri lolos ≥1 jalur verifikasi (§1); 4 kandidat gagal DITOLAK (§13) |
| d2 | usulan perubahan metode via change-control | §10-C1 (rumus Teale di PM1), §10-C2 (definisi Fisher/Pearson) |
| e | daftar risiko label per engine | §3 (per engine) + tabel §4.2 |
| f | baris "Riset pendahuluan" | header dokumen (10 skill) |
| g | sequ-mcp ≥3 pikiran | 5 pikiran, 5/5 sukses (tool_call) |

## 10. CHANGE-CONTROL (usulan, BUKAN perubahan sepihak)

- **C1 (ke PM):** koreksi teks rumus Teale di `V9_PM1_ARCHITECTURE.md` §2.3 baris 201 dari
  `MSE = (WOB/Am) + (480·N·π)/TOR` menjadi bentuk Teale 1965 terverifikasi
  `MSE = WOB/A + (120·π·N·T)/(A·ROP)` (field units) — alasan: dimensi suku kedua salah pada
  teks PM; label USROP TIDAK berubah (kolom tersimpan terverifikasi Teale, V6_R1 §2.2).
- **C2 (ke PM):** konfirmasi definisi "Fisher & Pearson literal" (R1 = H1, §4.5). Bila maksud
  PM lain → cukup baseline K-ii hyd yang diganti teksnya; engine tidak berubah.
- **C3 (catatan, bukan perubahan):** PM1 §2.7 menyebut tool_wear K-ii "prediksi status" —
  sifat metrik = klasifikasi LOTO (§2 baris terakhir); evaluasi B1 onset TIDAK dituntut dari
  klaim ini.

## 11. DAFTAR SITASI (diverifikasi sesi ini — 27 sumber, 0 karangan)

[1] Teale 1965 · [2] Menand & Mills 2017 (AADE) · [3] Liu et al. 2025 *Thermal Science* ·
[4] Hegde et al. 2019 · [5] Breiman 2001 · [6] Fernández-Delgado et al. 2014 (JMLR) ·
[7][8] NIST/SEMATECH (MAD & scaled-MAD 0,6745) · [9] Rousseeuw & Hubert 2017 ·
[10] Truong et al. 2020 · [11] Killick et al. 2012 (PELT) · [12] Good 2000 ·
[13] Hyndman & Athanasopoulos FPP3 · [14] Makridakis et al. 2020 (M4) ·
[15] Fisher 1915 · [16] Fisher 1921 · [17] IDAPS 2016 (SPE) · [18] kick early detection 2015 ·
[19] Cao et al. 2025 (arXiv) · [20] Al-Mamoori et al. 2025 · [21] Mopuri et al. 2022 ·
[22] Saadeldin et al. 2023 · [23] Saini et al. 2020 · [24] Liu et al. 2025 (SPE J) ·
[25] Horsrud 2001 · [26] Chang et al. 2006 · [27] Tunkiel et al. 2021.
URL/DOI tepatnya = blok Sources di bawah (dirender dari ledger `sources.py`, bukan diketik tangan).

## 12. VERIFIKASI GROUND-CITATIONS

`python sources.py verify <dokumen ini>` dijalankan sebelum finalisasi (§8d) — gagal = perbaiki
sebelum complete.

## 13. SITASI YANG DITOLAK (gagal verifikasi — jangan dikutip ulang)

| Kandidat | Gagal di | Pengganti terverifikasi |
|---|---|---|
| `10.1093/biomet/7.1.11` | doi.org 404 + OpenAlex 404 (pagination salah) | Fisher 1915 asli = Biometrika 10:507–521 → `10.2307/2331838` [15] |
| `10.1080/01621459.2012.710061` | doi.org 404 (PELT) | `10.1080/01621459.2012.737745` [11] |
| `10.1007/978-1-4757-3237-5` | doi.org 404 (Good) | `10.1007/978-1-4757-3235-1` [12] |
| `10.1016/j.eswa.2014.01.041` | OpenAlex = judul paper LAIN | JMLR resmi `jmlr.org/papers/v15/delgado14a.html` [6] |
| `10.1115/1.3341925` | OpenAlex 404 (kandidat Horsrud asal tebak) | Horsrud 2001 asli = `10.2118/56017-PA` [25] |

## Sources

[1] https://doi.org/10.1016/0148-9062%2865%2990022-7
[2] https://www.hpinc.com/wp-content/uploads/2025/08/Use-of-Mechanical-Specific-Energy-Calculation-in-Real-Time-to-Better-Detect-Vibrations-and-Bit-Wear-While-Drilling-AADE-17-NTCE-033_Extract.pdf
[3] https://doi.org/10.2298/TSCI2502521L
[4] https://doi.org/10.1016/j.petrol.2019.05.021
[5] https://doi.org/10.1023/A:1010933404324
[6] https://www.jmlr.org/papers/v15/delgado14a.html
[7] https://www.itl.nist.gov/div898/handbook/eda/section3/eda356.htm
[8] https://www.itl.nist.gov/div898/software/dataplot/refman2/auxillar/mad.htm
[9] https://doi.org/10.1002/widm.1236
[10] https://doi.org/10.1016/j.sigpro.2019.107299
[11] https://doi.org/10.1080/01621459.2012.737745
[12] https://doi.org/10.1007/978-1-4757-3235-1
[13] https://otexts.com/fpp3/simple-methods.html
[14] https://doi.org/10.1016/j.ijforecast.2019.04.014
[15] https://doi.org/10.2307/2331838
[16] https://bibbase.org/network/publication/fisher-ontheprobableerrorofacoefficientofcorrelationdeducedfromasmallsample-1921
[17] https://doi.org/10.2118/178821-pa
[18] https://doi.org/10.1016/j.ejbas.2015.09.006
[19] https://arxiv.org/abs/2503.07440
[20] https://doi.org/10.3390/app15095042
[21] https://doi.org/10.1016/j.petrol.2021.109489
[22] https://doi.org/10.1038/s41598-023-33411-9
[23] https://doi.org/10.2118/200006-MS
[24] https://doi.org/10.2118/228303-PA
[25] https://doi.org/10.2118/56017-PA
[26] https://doi.org/10.1016/j.petrol.2006.01.003
[27] https://doi.org/10.1016/j.petrol.2020.108069
