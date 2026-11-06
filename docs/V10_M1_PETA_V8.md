# V10-M1 — PETA ALAT PdM V8: 7 ENGINE, HITUNGAN ALAT, DAN CARA MEMBACANYA UNTUK DOSEN

Task: `t_e7155a1c` [KONSULTASI V10 · Master M1 V8] · Papan: capstone-v8-capability · Tanggal: 2026-10-14 (WIB)
Peran: **PENERUS [Master] V8-M1** (`t_3b98266a` / `t_4bc96d08`) — menjawab langsung kebutuhan bab
proposal dari sudut pandang peran M1 (agregasi peta kemampuan alat PdM).
Sumbu: `docs/V9_PM1_ARCHITECTURE.md` §1–§2 · Proposal V10 sumbu PM1 `t_cf741053`.
Sumber angka (dibaca langsung sesi ini): `docs/V8_M1_CAPABILITY_MAP.md`,
`docs/V8_PM_VERDICT.md`, 7 × `docs/V8_E_*_CAPABILITY.md`, `docs/V9_R1_JUSTIFICATION.md`,
`docs/V9_PM1_ARCHITECTURE.md`, `docs/V9_I1_INTEGRATION.md`, `docs/V9_PM2_VERDICT.md`,
`docs/V8_R1_ABC_SPEC.md`.

> **Prinsip dokumen ini:** SEMUA angka berasal dari dokumen/JSON milik peran sendiri
> (peta M1 + 7 profil + kampanye V9) — tidak ada angka baru yang dikarang. Dokumen ini
> adalah **solusi** untuk bab proposal, bukan riwayat kegagalan: yang ditulis = apa yang
> alat deteksi, bagaimana, mengapa, dan pada tingkat apa ia layak dipakai.

> **Riset pendahuluan: `scientific-critical-thinking`** — setiap klaim dipisah
> OBSERVED (angka profil M1/kampanye) vs DESAIN (keputusan arsitektur PM) vs BELUM-TERUKUR;
> hitungan tier dijumlahkan ulang (0+3+2+2=7) sebagai kontrol keabsahan silang.
> **Riset pendahuluan: `statistical-analysis`** — AUPRC/lift tidak dirata-ratakan antar kelas
> (plafon lift beda per kelas); FAR dilaporkan per skala aslinya; "belum terukur" ≠ 0 ≠ gagal.
> **Riset pendahuluan: `what-if-oracle`** — pembacaan peta diuji pada 5 cabang Ω/α/Δ/Ψ/Φ agar
> kesimpulan tidak bergantung pada satu asumsi (kampanye penguatan berhasil / label valid).
> **Riset pendahuluan: `sequentialthinking`** — inventaris 7 profil → hitungan alat →
> pemetaan pertanyaan proposal (a–f) → cara-baca L0–L3 untuk dosen.

---

## 0. RINGKASAN UNTUK DOSEN (satu paragraf)

Alat PdM yang dibangun menilai **tujuh kelas kegagalan BHA** (vibrasi lateral, stick-slip,
keausan bit, stuck pipe, anomali hidrolik, bit bounce/shock, keausan mata bor bengkel) dengan
**tiga lapisan penilaian** (A: apakah deteksi bekerja; B: apakah deteksi memberi nilai
maintenance; C: apakah cukup tepercaya untuk dipakai), **bukan** dengan satu gerbang
lulus/gagal. Hasilnya jujur dan tegas: **0 dari 7 engine layak sebagai alarm otomatis**,
**3 engine sudah terbukti** layak sebagai peringatan human-in-loop, **2 menunggu satu
pengukuran** (bersyarat), dan **2 layak pada tingkat tren/skor**. Seluruh 7 engine tetap
punya peran terdefinisi — tidak ada yang dibuang. Yang membatasi bukan ketiadaan sinyal
deteksi, melainkan bukti beban-kerja (FAR) dan waktu-peringatan (B) yang belum diukur atau
sudah terukur di atas ambang. Angka ini berasal dari eksekusi nyata pada data lapangan
Volve, bukan estimasi.

---

## 1. (a) TUJUH ENGINE KELAS DAN APA YANG MASING-MASING DETEKSI

Tujuh kelas = tujuh **jenis masalah pengeboran** yang masing-masing ditangani satu engine.
Sumber: `docs/V8_M1_CAPABILITY_MAP.md` §a (satu baris per engine) + `docs/V9_PM1_ARCHITECTURE.md` §2.

| # | Kelas | Jenis tugas | Apa yang dideteksi (sinyal/label) |
|---|---|---|---|
| 1 | **vib** | Deteksi kondisi (status sekarang) | Getaran lateral berlebih — status `VIBLAT_RT ≥ 32,17405 ft/s²` (ambang operasional rig). Bukan prediksi onset. |
| 2 | **ssi** | Deteksi kondisi | Stick-slip torsional sedang berlangsung — status `SSI(CRPM_RT) ≥ 1`, dengan `SSI = (max−min)/(2·mean)` atas jendela CRPM. Bukan onset/diagnosis. |
| 3 | **bit_wear** | K-1 deteksi kondisi · K-2 prediksi onset | **K-1:** status blok inefisiensi MSE (`high_MSE`, Teale MSE). **K-2:** prediksi onset blok keausan (H=10 mnt) — *belum terukur*. |
| 4 | **stuck** | K-i deteksi kondisi · K-ii prediksi onset | **K-i:** status blok `STUCK_RT` (pipa terjepit). **K-ii:** prediksi onset 0→1, horizon H=10 menit (fokus run). |
| 5 | **hyd** | K-i deteksi kondisi · K-ii prediksi onset | **K-i:** status anomali hidrolik = residu tekanan `SPPA` (`\|z\|>2` vs bin TFLO). **K-ii:** prediksi kick/loss (proxy `ΔV_pit`), H=10 mnt. |
| 6 | **shk** | Deteksi anomali berlangsung + sub-onset | Bit bounce/shock sedang berlangsung — status `SHKRSK_RT ≥ 1`; plus sub-tugas onset H=10 mnt. |
| 7 | **tool_wear** | K-i deteksi perubahan-regime · K-ii klasifikasi lintas-alat | **K-i:** deteksi perubahan-regime dalam-run (bengkel). **K-ii:** prediksi status keausan lintas-alat (LOTO, domain bengkel). |

**Catatan penting pembacaan:** lima kelas adalah **deteksi kondisi/status** (vib, ssi,
bit_wear K-1, stuck K-i, hyd K-i) dan sisanya **prediksi onset** (stuck K-ii, hyd K-ii,
shk sub-onset, bit_wear K-2). Dua jenis tugas ini **sengaja dibedakan** karena metriknya
berbeda: kelas status dinilai dengan margin/konfirmasi, kelas onset dinilai dengan
cakupan-peringatan (B1) dan waktu-peringatan (TLead). Mencampur keduanya adalah kesalahan
framing yang secara eksplisit dihindari (0 kasus salah-framing, `V9_R1` §4.3).

---

## 2. (b) CARA KERJA ENGINE

Setiap kelas tidak memakai satu metode tunggal, melainkan **kombinasi (hybrid) yang dipilih
per tugas**. Ada empat jenis mesin dasar yang dipakai ulang lintas kelas (bukan 15 varian):

1. **Rule ambang-absolut / rule definisi kanal** — nol pelatihan, transparan:
   `status(t)=1[VIBLAT_RT(t) ≥ 32,17405]` (vib), `SSI ≥ 1` (ssi), `SHKRSK_RT ≥ 1` (shk),
   rule 3-RMS (tool_wear).
2. **Persistence** `ŷ(t)=y(t−1)` — konfirmasi status berbasis satu grid (60 detik);
   baseline naive standar deret waktu.
3. **Statistik robust** — median/MAD: `z = 0,6745·(x − median)/MAD` (label hyd K-i,
   skor stuck E2), dan **change-point** `SSE(τ)` + permutation test 500× (tool_wear K-i).
4. **Machine Learning** — `RandomForestClassifier(n_estimators=300, min_samples_leaf=5,
   class_weight="balanced_subsample", random_state=42)` dengan fitur statistik jendela
   10 menit (mean/std/slope/last/frac).

Tabel cara kerja per engine (jenis engine + mekanisme):

| Kelas | Jenis engine | Mekanisme ringkas |
|---|---|---|
| **vib** | Hybrid: rule ambang-absolut + persistence + RF | Rule menandai status; persistence = pembanding wajib; RF (300 pohon, 55 fitur) = penambah nilai di atas rule — menang vs canary 4/4. |
| **ssi** | Hybrid: rule definisi kanal + RF | Rule `SSI≥1` = detektor paling langsung; RF menambah daya ranking (RF ≥ canary 5/5; persistence kalah 0/5). |
| **bit_wear** | K-1: persistence (engine utama) + RF screening + canary · K-2: RF-onset | K-1: persistence terukur terbaik (AUPRC 0,679–0,984); RF menang vs canary 4/4 tapi **kalah persistence 4/4**. K-2 dirancang (relabel, nol parse) — belum dijalankan. |
| **stuck** | 4 engine setara-tugas: E0 persistence · E1 rule (2-dari-3) · E2 statistik (z TQA/HKLD/ROP) · E3 RF | `E1: alarm=1[(z(TQA)>2)+(z(HKLD)>2)+(ROP-drop≥30%) ≥ 2]` (z median/MAD jendela 60 mnt). E3 RF = ranking onset. |
| **hyd** | K-i: **persistence** (RF DILARANG) · K-ii: hybrid RF + fitur aliran | K-i: persistence mengalahkan RF (ΔB negatif 7/7) → ML tidak dipakai, keputusan empiris. K-ii: RF + fitur mass-balance (FlowIn/FlowOut). |
| **shk** | Hybrid: RF (55 fitur, LOWO 9 fold) + persistence | RF = penambah nilai untuk onset (RF≥persistence B1 di 9/9 fold); status tetap ber-orchestrasi rule/persistence; reproduksi V6 7/7 <1e-9 = kontrol validitas pipeline. |
| **tool_wear** | K-i: change-point SSE + permutation · K-ii: RF + ambang inner-LOO F1 | K-i: cari titik perubahan `τ* = argmin_τ SSE(τ)`, uji signifikansi permutation 500×. K-ii: RF klasifikasi LOTO + kalibrasi ambang FAR. |

**Rumus kunci (persis, dari `V9_R1_JUSTIFICATION.md` §3):**
- Stick-slip: `SSI = (max − min) / (2·mean)` atas jendela CRPM ≥10 sampel.
- Teale MSE (label bit_wear): `MSE = WOB/A + (120·π·N·T)/(A·ROP)` (field units).
- z robust: `z = 0,6745·(x − median)/MAD` (faktor 0,6745 = konversi MAD→σ untuk normal).
- Change-point: `SSE(τ) = Σ_{t≤τ}(x_t − μ₁)² + Σ_{t>τ}(x_t − μ₂)²`; signifikansi `p = (1+#{SSE_perm ≤ SSE_obs})/(1+500)`.
- Beban-kerja: `FAR = FP / jam_operasi_negatif` (per 24 jam, kelas rig) · `B3 = 1 − FP_engine/FP_display_status_quo`.
- Fisher/Pearson literal (baseline hyd K-ii): `r = Σ(x−x̄)(y−ȳ)/√(Σ(x−x̄)²·Σ(y−ȳ)²)`, transformasi `z' = atanh(r) = ½·ln((1+r)/(1−r))`, `SE(z') = 1/√(n−3)`.

---

## 3. (c) KENAPA METODE ITU DIPILIH

Metode dipilih **per tugas** dan diuji terhadap **baseline yang relevan untuk tugas itu** —
bukan satu baseline universal. Empat alasan pokok:

1. **Rule ambang-absolut dipakai sebagai "sistem hari-ini".** Ia adalah tolok ukur "apa yang
   sudah bisa dilakukan tanpa ML". Rule `VIBLAT ≥ 32,17405` dan `SSI ≥ 1` adalah definisi
   operasional/kanal yang sudah ada di rig, jadi detektor paling langsung dan paling murah.
2. **Persistence dipakai karena status membentuk blok temporal panjang.** Untuk kelas status,
   label cenderung persisten antar-grid; persistence justru **sulit dikalahkan** (kompetisi
   M4 membuktikan metode naive sering menang). Karena itu persistence = **pembanding wajib**:
   ML hanya bernilai bila mengalahkannya. Terbukti koheren di 4 kelas (hyd ΔB− 7/7;
   bit_wear kalah 4/4; vib menang 2/4; shk 4/9).
3. **ML (RF) dipakai hanya bila memberi nilai tambah terukur (ΔB>0).** RF dipilih karena
   tahan overfitting pada fitur noise dan termasuk klasifikator terkuat di benchmark
   dunia-nyata. Namun pada kelas yang ML **merugikan**, ML **dilarang**: `hyd-K-i` dilarang
   memakai RF (ΔB negatif 7/7, replikasi eksak) — ini keputusan empiris, bukan dogma anti-ML.
4. **Statistik robust (median/MAD, change-point) dipakai karena data sensor skewed** dan
   tidak normal (uji asumsi normalitas tidak berlaku). z median/MAD tahan outlier;
   permutation test dipakai karena 469 jendela 1 detik non-normal dan n kecil per run.

**Baseline relevan per tugas** (ringkas, `V9_R1` §4.1): persistence (apakah ML mengalahkan
korelasi waktu?), canary-kedalaman (apakah model cuma "mengingat posisi"?), prevalence-random
(apakah lift terbaca benar untuk kelas langka?), rule/display status-quo (apakah alat
mengungguli sistem hari-ini?). Setiap baseline menjawab ancaman validitas yang **berbeda** —
inilah mengapa satu baseline universal ditolak.

---

## 4. (d) PERAN DATA

Data adalah **tulang punggung** dan sumber tunggal semua angka; arsitekturnya berlapis
(`V9_PM1_ARCHITECTURE.md` §1.1):

- **LAYER-0 DATA:** WITSML parsed CSV **9 wellbore**; USROP **198.928 baris**;
  F-9A `time.csv` **419.747 baris**; data eksternal (trajectory MD→TVD, tubular, bhaRun,
  mudLog, DLIS COMPUTED_OUTPUT, EDM phase=ACTUAL, **409 formation picks**); plus dataset
  **bengkel** tool_wear (Mendeley `th4yv974r2`, 4 alat × 2 run, 469 jendela 1 detik @1000 Hz).
- **LAYER-1 FITUR:** kontrak **grid 60 detik** + **jendela [t0−10, t0)**; statistik per kanal
  `mean/std/slope/last/frac`; imputasi median fold-safe. Untuk kelas rig = **55 fitur**
  (11 kanal MWD × 5 statistik). Data bengkel memakai **27 fitur getaran** (kurt/crest/fdom/
  rms/skew/p2p/zcr/mean/std per sumbu X/Y/Z) + fitur VMD.
- **Anti-bocor:** stempel-waktu fitur < stempel-waktu label (pelanggaran = 0); kanal
  sumber-label **DILARANG** menjadi fitur (mis. `VIBLAT_RT`, `CRPM_RT`, `STUCK_RT`,
  `SHKRSK_RT`, `SPPA/TFLO`, `WOB/ROP/RPM/TORQ`).
- **Satu segmen pembuktian nyata:** F-14 = satu-satunya wellbore yang ada di keenam dataset
  rig (vib 1.989 · ssi 5.455 · shk 11.205 · stuck_k1 3.201 · stuck_k2 95.925 · hyd_ki 10.401
  jendela) → prototipe dijalankan pada data nyata ini (`V9_I1`).

Peran data karenanya bukan sekadar bahan mentah, melainkan **penentu kejujuran**: kualitas
sensor yang terukur diungkap apa adanya (mis. nodata CRPM F-14 = 96,6% → deteksi SSI F-14
praktis mati; ini dilaporkan sebagai keterbatasan, bukan disembunyikan).

---

## 5. (e) LABELING ML, RUMUS STATISTIK, DAN WORKFLOW HYBRID

### 5.1 Sumber label per engine (dan risiko sirkularitasnya)

| Kelas | Sumber label | Kanal terlarang jadi fitur | Risiko utama |
|---|---|---|---|
| vib | kanal MWD `VIBLAT_RT` | VIBLAT + WHIRL/BOUNCE (duplikat) | drift instrumen antar-well |
| ssi | turunan `CRPM_RT` | CRPM_RT | label = fungsi kanal; ML bisa "belajar rumus" dari proxy |
| bit_wear | blok `high_MSE` (Teale, kuantil P75) | WOB/ROP/RPM/TORQ | label kuantil ≠ kejadian perawatan nyata |
| stuck | `STUCK_RT` (+ kontrol-positif DDR) | STUCK_RT | semantik skala 0–3 beda antar-well |
| hyd K-i | residu `SPPA` vs bin TFLO | SPPA/TFLO/SPM | label = z kanal yang sama → persistence = konfirmasi diri |
| hyd K-ii | z `ΔV_pit` (PROXY) | 13 kolom pit + GAINLOSSTOT | proxy ≠ kick nyata |
| shk | `SHKRSK_RT` | SHKRSK_RT | severity-mix beda antar-well |
| tool_wear | identitas run (desain dataset) | (tidak ada) | confound urutan-run R02>R01 |

Prinsip labeling: **label diambil dari kanal fisik/status operasional**, kanal pembentuk label
dilarang jadi fitur (asersi anti-sirkular lolos), dan kelas tanpa angka (bit_wear K-2) dilarang
dipakai di tingkat apa pun sampai kampanye berangka terbit.

### 5.2 Workflow hybrid (bagaimana rule/statistik/ML disatukan)

Hybrid di sini = **infrastruktur bersama, bukan bobot bersama**:

- **Satu status-confirmation module** (persistence + rule, nol training) dipakai bersama oleh
  vib, ssi, stuck-K-i, hyd-K-i, bit_wear-K-1 — murah dan seragam.
- **Satu onset-layer bersama** (grid 60 detik + feature store + calibration harness bersama),
  **TAPI head prediktor terpisah per kelas** — karena label beda fisika (STUCK_RT vs ΔV_pit vs
  SHKRSK vs blok high_MSE) dan tindakan beda (releasing vs well-control vs kurangi parameter vs
  bit-change). Satu model gabungan akan mencampur estimand.
- **ML ditambahkan hanya bila ΔB>0** di atas baseline relevan kelas itu; kalau tidak, ML
  dilarang (contoh: hyd-K-i).
- **Kalibrasi ambang SELALU lokal per wellbore** (kalibrasi lintas-well dilarang otomatis),
  karena ambang terbukti tidak transfer (shk 0 alarm lintas-well; stuck q95 jenuh; hyd FAR
  meledak 26–300×).

---

## 6. (f) MENJELASKAN "7 vs 11 vs 27"

Tiga angka ini sering membingungkan; ketiganya benar dan menjawab pertanyaan berbeda:

| Angka | Apa yang dihitung | Isi |
|---|---|---|
| **7** | **Kelas engine** (jenis masalah BHA) | vib, ssi, bit_wear, stuck, hyd, shk, tool_wear |
| **11** | **Klaim/sub-tugas** yang dievaluasi | 7 kelas + 4 kelas yang punya dua sub-tugas: bit_wear (K-1/K-2), stuck (K-i/K-ii), hyd (K-i/K-ii), tool_wear (K-i/K-ii) → 7 + 4 = **11 klaim** |
| **27** | **Head** pada registry prototipe (implementasi konkret tiap engine × metode/head) | hasil perakitan `V9_I1_INTEGRATION.md` §2 — 7 engine = **27 head** (rule/persistence/hybrid/RF per kelas) |

Jadi: **7 = jumlah masalah**, **11 = jumlah klaim yang dinilai A/B/C**, **27 = jumlah head yang
benar-benar dirakit jadi alat** (tiap head punya tier + layer + badge FAR + batas pemakaian).
Dua "27" lain yang muncul di dokumen (27 fitur getaran bengkel, 27 sumber sitasi R1) adalah
kebetulan angka dan **tidak berhubungan** dengan 27 head — jangan tertukar.

---

## 7. HITUNGAN ALAT V8: 0 ALARM · 3 PERINGATAN · 2 BERSYARAT · 2 TREN

Sumber: `docs/V8_M1_CAPABILITY_MAP.md` §d + `docs/V8_PM_VERDICT.md` §d. Dihitung **per engine
(7 unit)**; tier = kemampuan **tertinggi yang terbukti hari ini**.

| Tier alat | Jumlah | Engine | Alasan satu kalimat |
|---|---|---|---|
| **LAYAK alarm otomatis kritis** | **0 dari 7** | — | Syarat alarm (FAR≤1/24jam dgn recall>0 **+** B1≥80% **+** C2/C3) belum tercapai engine mana pun — sebagian karena FAR/B belum diukur, sebagian sudah terukur tapi di atas ambang. |
| **LAYAK peringatan human-in-loop (terbukti)** | **3 dari 7** | shk · stuck · hyd | Ketiganya punya waktu-peringatan (TLead) terukur pada well terkalibrasi: shk lead 2–9 mnt, stuck triage sumur mirip F-10 lead 10 mnt, hyd K-ii indikasi dini lead 7 mnt — cukup untuk *menyarankan*, belum untuk *memutuskan*. |
| **LAYAK peringatan BERSYARAT** | **2 dari 7** | vib · ssi | Deteksi lapisan A sudah kuat (vib lift 4/4 ≥1,5; ssi ΔB>0 di 5/5 fold), tetapi FAR/B belum pernah diukur — tinggal satu kampanye pengukuran untuk naik ke peringatan penuh. |
| **Tier tertinggi = TREN/skor saja** | **2 dari 7** | bit_wear · tool_wear | Keduanya menang atas canary tapi belum cukup untuk notifikasi: bit_wear K-1 = konfirmasi-status (persistence 0,679–0,984) + skor screening; tool_wear = skor LOTO lintas-alat + detektor perubahan-regime (precision ≈0,5 → bukan alarm). |
| **Punya peran dalam alat** | **7 dari 7** | semua | Tidak ada engine dibuang atau dilabeli "gagal/buang" — tiap engine punya peran + batas tertulis. |

**Cek aritmetika:** 0 + 3 + 2 + 2 = **7 ✓** (tanpa engine dihapus, tanpa engine dobel).

**Angka ringkas:** 0/7 alarm otomatis · 3/7 peringatan operasional terbukti · **5/7 punya jalur
peringatan** (3 terbukti + 2 bersyarat) · 7/7 layak setidaknya konfirmasi-status/tren/indikasi
pada batasnya. Yang membatasi 0-alarm = **bukti B & FAR belum diukur** (vib, ssi, bit_wear)
atau **sudah terukur di atas ambang** (shk, stuck, hyd, tool_wear), bukan ketiadaan sinyal
deteksi.

**Catatan V9 (penyempurnaan, bukan perubahan hitungan V8):** kampanye V9 menambah bukti
(rule-display vib/shk naik ke PERINGATAN-BERPENGAWAS; hyd K-i hybrid = kandidat terkuat dengan
FP −55,7%). Pada perakitan alat `V9_I1`, komposisi lapisan keputusan = **L0 5 head · L1 11
head · L2 9 head · L3 2 head · slot alarm otomatis = 0** — konsisten dengan 0/7 alarm di atas.

---

## 8. CARA MEMBACA PETA KEMAMPUAN BAGI DOSEN (L0–L3)

Peta kemampuan tidak berbunyi "lulus/gagal", melainkan **"pada tingkat pemakaian apa engine ini
terbukti"**. Ada dua kerangka yang perlu dibedakan:

### 8.1 Tiga lapisan penilaian A/B/C (dasar penentuan tier)

- **LAPISAN A — apakah deteksi bekerja?** precision/recall/FAR/waktu-deteksi vs baseline
  relevan kelas itu.
- **LAPISAN B — apakah deteksi beri nilai maintenance?** waktu peringatan terhadap kejadian
  nyata (TLead/B1) = kunci; juga pengurangan pemeriksaan tak perlu (B3).
- **LAPISAN C — cukup tepercaya untuk dipakai?** lintas periode/regime/peralatan, kualitas
  sensor, transparansi ketidakpastian (C1–C4).

Gate `lift≥1,5` + mayoritas-fold V6 = syarat **ambang-atas "terbukti prediksi kuat"** (untuk
alarm), **bukan** syarat "engine boleh dipakai sama sekali".

### 8.2 Empat lapisan keputusan L0–L3 (tingkat pemakaian alat)

Inilah "L0–L3" yang dipakai di alat (bukan LAYER-0..4 pipeline data):

| Lapisan | Nama | Arti bagi dosen | Bukti/contoh |
|---|---|---|---|
| **L0** | **Status otomatis** | Rule/persistence = sistem hari-ini, **tanpa ML**; mengonfirmasi keadaan di layar rig, **bukan** alarm PdM baru. | rule VIBLAT≥32,17 · rule SSI≥1 · persistence hyd/bit_wear/stuck/vib (5 head di I1). |
| **L1** | **Peringatan human-in-loop** | Notifikasi yang **butuh konfirmasi operator**; wajib menampilkan badge FAR + label keyakinan + batas. | terbukti: shk/stuck/hyd; bersyarat (masuk setelah FAR/B diukur): vib/ssi (11 head di I1). |
| **L2** | **Tren/skor (dashboard)** | Menampilkan skor/peringkat **tanpa notifikasi**; engine tren tidak boleh berbunyi. | vib-RF · ssi-RF · bit_wear screening · tool_wear skor LOTO · stuck E3 ranking · hyd trend (9 head). |
| **L3** | **Keputusan manusia** | Semua yang belum layak alarm — alat menyarankan, manusia memutuskan. | hyd K-ii (data belum tersedia) · bit_wear K-2 (pra-reg belum terbit) (2 head). |

**Alarm otomatis kritis tanpa manusia: 0 slot hari ini (0/7 engine).** Ini keputusan wajar,
bukan kegagalan: syarat alarm memang belum terpenuhi engine mana pun.

**Gate kenaikan tier (dari dokumen sumber, bukan angka baru):**
- **Masuk L1:** FAR≤6/24jam (atau setara skala) **terukur** dgn recall>0 + TLead/B4 terukur +
  C4; kalibrasi lokal per well + anotasi regime.
- **Masuk L0-alarm (otomatis):** FAR≤1/24jam dgn recall>0 + B1≥80% + C2 per-bin (drop <20%)
  + C3 dropout <20% + validasi kejadian nyata.
- **Turun tier bukan "gagal":** bila FAR terukur >6/24jam (contoh: stuck) → engine turun ke
  triage/tren dengan anotasi; kemampuannya tetap tercatat.

**Batas pemakaian yang WAJIB tampil (agar tidak overclaim):** hanya well terkalibrasi lokal ·
horizon ≤10 menit · tanpa klaim diagnosis (G1) · tanpa klaim pengurangan inspeksi (G3) ·
tool_wear = domain bengkel terpisah (lead detik, tidak dijumlah dengan lead menit rig) ·
FAR ditampilkan pada skala aslinya.

---

## 9. BATAS JUJUR DOKUMEN INI

1. Semua angka = kutipan dari dokumen/JSON milik peran sendiri (peta M1, 7 profil V8, kampanye
   V9). Dokumen ini **tidak mengeksekusi engine baru** — kesimpulan = agregasi hasil eksekusi
   sebelumnya.
2. "Belum terukur" dipisahkan tegas dari "gagal"; angka V6 yang dikutip di dokumen sumber
   sudah melalui audit V8-A1/V7 dan reproduksi evaluator.
3. Peta ini berlaku untuk data Volve pada well terkalibrasi; transfer ke rig/well lain belum
   diuji (G5) — dokumen ini tidak mengklaim sebaliknya.
4. Kelayakan "advisory" = pada tingkat yang terukur (L0/L2 penuh; L1 pada 3 engine terbukti +
   2 bersyarat) — bukan alarm otomatis.

## Sumber (dibaca langsung sesi ini)

`docs/V8_M1_CAPABILITY_MAP.md` (229 baris) · `docs/V8_PM_VERDICT.md` (364 baris) ·
7 × `docs/V8_E_{vib,ssi,bit_wear,stuck,hyd,shk,tool_wear}_CAPABILITY.md` ·
`docs/V9_R1_JUSTIFICATION.md` (§3 rumus, §4 baseline/label) ·
`docs/V9_PM1_ARCHITECTURE.md` (§1 pipeline 5 lapis, §2 spesifikasi 7 engine, §1.3 gate tier) ·
`docs/V9_I1_INTEGRATION.md` (§2 registry 27 head, §4 lapisan keputusan) ·
`docs/V9_PM2_VERDICT.md` (§d kepatuhan a–e, §e ringkas alat) · `docs/V8_R1_ABC_SPEC.md` (kerangka A/B/C).
