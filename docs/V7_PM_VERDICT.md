# V7-PM — VERDICT: Apakah Solusi V7 LEBIH BAIK dari Kondisi V6?

Task: `t_dd0f1591` [Project Manager] · Board: capstone-v7-solve · Tanggal: 2026-10-11 (WIB)
Prinsip penilaian (instruksi operator, dikunci): **nilai VALIDITAS METODE, bukan angka akurasi**
(analogi detektor diabetes prevalensi 11% dengan akurasi 80% = SAH karena metode benar;
classifier spam 89% yang "menghindari" prediksi diabetes = TIDAK VALID karena main class/exclude).
Kriteria vonis (operator, via session_search 2026-10-11): **LEBIH BAIK = solusi V7 punya jalur
METODE-SAH ke minimal 5 kelas lolos gate** (ideal 7, batas terendah 3), gate G1/G2 V6 tidak digeser.

> **Riset pendahuluan: `what-if-oracle`** — 5 cabang skenario (Ω best / α likely / Δ worst /
> Φ contrarian / ∞ second-order) dipetakan sebelum vonis: lantai skenario = 4 kelas, target 5,
> upside 7; cabang Φ (TIDAK LEBIH BAIK) diuji eksplisit dan ditolak dengan bukti kriteria operator.
> **Riset pendahuluan: `scientific-critical-thinking`** — OBSERVED vs DERIVED vs HIPOTESIS dipisah
> di setiap butir bukti; 4 klaim kunci dihitung ULANG oleh PM dengan skrip mandiri
> (`~/.hermes/cache/scratch/pm_verify_t_dd0f1591.py`, `pm_onset_variants.py`), termasuk uji ulang
> 2 temuan koreksi A1; kontradiksi (onset 34 vs 74 vs M2 "50") dilaporkan apa adanya, tidak diluruskan.
> **Riset pendahuluan: `consciousness-council`** — 5 arketip (Empiricist, Contrarian, Pragmatist,
> Architect, Strategist) berdebat tentang status vonis "lebih baik tanpa satu pun kelas baru terbukti
> lolos"; sintesis §5.
> **Riset pendahuluan: `sequentialthinking`** (3 pikiran, 3/3 sukses, thoughtHistoryLength 3) —
> premis vonis → devil's advocate (tes pembeda vonis) → sintesis + kerangka eksekusi.
> **Riset pendahuluan: `session_search`** — riwayat kegagalan V6 & instruksi asli operator diverifikasi
> ke sesi `20261010_144843_ae785a` (target ≥5, prinsip diabetes-80%, alur R&D→Master→Pembaca→Auditor→PM).

---

## 0. RINGKASAN EKSEKUTIF — VONIS

**VONIS: LEBIH BAIK — dengan syarat eksekusi tegas (§7). Bukan "mungkin".**

V6 (baseline terverifikasi langsung dari `docs/V6_E1_ML_DESIGN.md` §4.4): **2 LULUS penuh**
(`vib`, `ssi`) + **1 LAYAK BERSYARAT** (`bit_wear`) + **4 GAGAL** (`stuck`, `shk`, `hyd`,
`tool_wear`).

V7 tidak menjalankan kampanye ML baru — V7 menghasilkan **portofolio solusi terverifikasi** yang
mempunyai **jalur metode-sah ke 5 kelas lolos gate**:

| # | Kelas | Status V6 | Jalur V7 | Kekuatan jalur (bukti terverifikasi) |
|---|---|---|---|---|
| 1 | `vib` | LULUS | dipertahankan + diperkuat 3 wellbore baru (VIBLAT_RT F-4 86 / F-10 66 / F-15 76 file) | TINGGI (recount 3 pihak: R1 scan → D1e COCOK PERSIS → A1 D6 EKSAK) |
| 2 | `ssi` | LULUS (rapuh) | S-E1: fold UNDERPOWERED (F-7 3 pos, F-9 12 pos) diganti fold kuat dari CRPM_RT wellbore baru (281.030 / 42.010 / 178.430 / 57.846 baris) | TINGGI (data nyata; mekanisme label tidak berubah) |
| 3 | `shk` | GAGAL (3/7; G2 6/7 lolos = sinyal ADA) | S-B1: parse F-10 + F-12 → **798 + 580 positif SHKRSK_RT nyata** (prev 0,27% / 1,59%) menyerang akar "positif terlalu sedikit" | TINGGI — G2 sudah 6/7; angka positif direcount D1e + dikoreksi M2 (bukan estimasi R1) |
| 4 | `bit_wear` | LAYAK BERSYARAT (persistence > RF 4/4) | S-F1 onset-of-high-MSE: **481 kandidat onset nyata (329 dari normal)** — hukuman persistence dihapus per konstruksi; G1 sudah 3/4 | TINGGI — jumlah onset jujur diverifikasi A1 + PM (481/329); jalur termurah kedua |
| 5 | `stuck` | GAGAL (mayoritas = 1 suara) | S-A1 onset + S-A2 parse F-10/F-12 (15.300 + 3.463 baris STUCK_RT) → fold 2 → 4 | **SEDANG** — onset ketat F-9_A hanya 34 (PM reproduce EKSAK); F-14 onset sporadis; daya statistik = risiko nyata yang harus dihitung di Fase 0 |
| 6 | `hyd` | GAGAL | S-C1 onset (tes pembeda) + S-C2 label fisika pit/flow (345.442 baris F-9 A LANGSUNG, nol parse) | SEDANG-RENDAH (upside; sinyal precursor lintas-kanal belum teruji) |
| 7 | `tool_wear` | GAGAL | S-D1 change-point progresi + S-D2 VMD | SEDANG-RENDAH (upside; tes artefak termal = pemecah) |

**Mengapa memenuhi syarat "LEBIH BAIK" versi operator (jalur METODE-SAH, bukan hasil run):**
1. **Gate TIDAK digeser** — diverifikasi A1 §3 terhadap pra-reg V6 asli: G1 (lift ≥1,5 mayoritas),
   G2 (RF ≥ canary), <30 positif = UNDERPOWERED, persistence→bersyarat, LOWO, larangan
   kanal-sumber-label jadi fitur = **identik**. PM cocokkan langsung ke `V6_E1_ML_DESIGN.md` §4.4 —
   seluruh angka kegagalan yang dikutip R1 cocok persis.
2. **Metode sah menurut prinsip diabetes-80%**: onset-reframing adalah **koreksi definisi tugas**
   ("alat X akan SEGERA RUSAK" = peristiwa onset, bukan status instrumen) — setara memperbaiki
   test yang benar, BUKAN mengejar akurasi dengan exclude/main-class. Label non-sirkular dipertahankan.
3. **Data nyata, terverifikasi silang**: temuan terbesar V7 (4 wellbore belum diparse yang kaya
   kanal dysfungsi) dihitung ulang oleh 3 pihak independen dengan angka identik. Sitasi ilmiah
   dibuka 8/9 oleh auditor, 0 paper karangan (A1 §1).
4. **Koreksi angka jujur**: 4 temuan overstated/stale dilaporkan sendiri oleh auditor, dan 2 di
   antaranya **PM reproduksi independen** (§3) — metode audit berfungsi, tidak menutupi.
5. **Lantai skenario terburuk (Δ, §4)**: jika stuck gagal daya DAN hyd/tool_wear gagal tes
   pembeda → tetap **4 kelas LULUS** (vib+ssi+shk+bit_wear) > baseline V6 = 2. Vonis tidak
   bergantung pada kelas yang berisiko.

**Batasan vonis (jujur, bukan penggeser):** V7 membuktikan KELAYAKAN JALUR (data ada, mekanisme
akar terbukti, metode sah) — bukan kelas yang sudah LULUS. Eksekusi (Fase 0–3, §7) adalah satu-satunya
jalan mengubah jalur jadi hasil; vonis ini mengikat kerangka eksekusi, bukan mengklaim kemenangan.

---

## 1. TABEL KEPATUHAN SKILL + TOOL PER TIM

Dicek dengan `search_files` (grep) ke seluruh 12 dokumen output.

| Tim | Output | Baris "Riset pendahuluan" | Skill sci dipakai | sequ-mcp | Tool wajib | Pelanggaran |
|---|---|---|---|---|---|---|
| R&D (R1) | V7_R1_SOLUTIONS.md | ✅ 5 baris | literature-review, paper-lookup, hypothesis-generation, scientific-critical-thinking, grounded-citations | ❌ tidak dinyatakan | web_search/terminal/read_file (bukti ledger 22 entri, skrip scan 3×) | sequ-mcp tidak dinyatakan (task body mewajibkan); sitasi [16] Saini gagal CAPTCHA tapi dilaporkan jujur |
| Master M1 | V7_M1_DELEGASI.md | ✅ 2 baris | scientific-critical-thinking, verification-mandatory | ❌ tidak dinyatakan | read_file + kanban_show 8 kartu (bukti §1) | sequ-mcp tidak dinyatakan |
| Pembaca 01 (D1a) | V7_D1a_DATA_CHECK.md | ✅ 2 baris | verification-mandatory, scientific-critical-thinking | ❌ tidak dinyatakan | 6 skrip recount mandiri | sequ-mcp tidak dinyatakan |
| Pembaca 02 (D1b) | V7_D1b_DATA_CHECK.md | ✅ 2 baris | verification-mandatory, scientific-critical-thinking | ❌ tidak dinyatakan | parse 161 file + verifikasi ganda rg/Python | sequ-mcp tidak dinyatakan |
| Pembaca 03 (D1c) | V7_D1c_DATA_CHECK.md | ✅ 2 baris | verification-mandatory, scientific-critical-thinking | ❌ tidak dinyatakan | parse + recount independen | sequ-mcp tidak dinyatakan |
| Pembaca 04 (D1d) | V7_D1d_DATA_CHECK.md | ✅ 2 baris | scientific-critical-thinking, verification-mandatory | ⚠️ wrapper bug (dilaporkan M2 §7) | grep ganda + reproduksi angka D0 | sequ-mcp gagal transport (dilaporkan, bukan disembunyikan) |
| Pembaca 05 (D1e) | V7_D1e_DATA_CHECK.md | ✅ 2 baris | verification-mandatory, scientific-critical-thinking | ❌ tidak dinyatakan | scan 4 wellbore + 300 sampel F-1 C/F-11 | scan penuh F-1 C timeout 300 s → klaim 575/517 GAINLOSSTOT **belum dihitung ulang** (dilaporkan A1 §6c) |
| Pembaca 06 (D1f) | V7_D1f_DATA_CHECK.md | ✅ 3 baris | verification-mandatory, scientific-critical-thinking, sequentialthinking | ✅ 3 pikiran | 4 lapis scan klaim ketiadaan | — |
| Pembaca 07 (D1g) | V7_D1g_DATA_CHECK.md | ✅ 2 baris | verification-mandatory, scientific-critical-thinking | ⚠️ wrapper bug (dilaporkan M2 §7) | join phase EDM → 8 baris ACTUAL | sequ-mcp gagal transport (dilaporkan) |
| Pembaca 08 (D1h) | V7_D1h_DATA_CHECK.md | ✅ 2 baris | verification-mandatory, scientific-critical-thinking | ❌ tidak dinyatakan | 5 skrip + rekonsiliasi 884-vs-1.412 | klaim "94 event F-9 A tervalidasi" salah → dikoreksi M2 (12/94) |
| Master M2 | V7_M2_SYNTHESIS.md | ✅ 4 baris | verification-mandatory, scientific-critical-thinking, statistical-analysis, sequentialthinking | ✅ 3/3 sukses | 4 skrip verifikasi mandiri + kanban_show | — |
| Auditor A1 | V7_A1_SOLUTION_AUDIT.md | ✅ 4 baris | scientific-critical-thinking, verification-mandatory, peer-review, statistical-analysis | ❌ **DILEWATI** (klaim "blokir transport" — padahal M2 buktikan sequ-mcp jalan hari yang sama) | web_extract 8 paper + 6 skrip hitung ulang | **PELANGGARAN sequ-mcp** (dicatat; tidak membatalkan substansi: 4 skill lain dipakai + audit independen) |
| **PM (kartu ini)** | V7_PM_VERDICT.md | ✅ baris di atas | what-if-oracle, scientific-critical-thinking, consciousness-council | ✅ 3/3 sukses (thoughtHistoryLength 3) | read_file, session_search, agentmemory, terminal (2 skrip verifikasi mandiri) | — |

**Ringkasan kepatuhan:** 12/12 output punya baris "Riset pendahuluan" + skill sci ✅ ·
sequ-mcp: 3 dokumen menyatakan sukses, 2 wrapper bug (dilaporkan jujur), **7 tidak dinyatakan**
(R1, M1, D1a, D1b, D1c, D1e, D1h) + **1 dilewati eksplisit (A1)** — pelanggaran proses, dicatat
di sini; substansi tidak terbukti terpengaruh (angka kunci diperiksa silang lintas-tim dan 4 di
antaranya diverifikasi ulang oleh PM).

**Underuse tool (laporan potensial Hermes):**
1. `session_search` tidak dipakai satupun tim selain PM — riwayat kegagalan V5/V6 (mis. persistence
   warning V5-J2, T2-f gate) tidak ditarik ulang oleh tim solver.
2. `agentmemory`/`memory_save` tidak dinyatakan di dokumen mana pun (hanya slot pinned); durabilitas
   temuan bergantung pada file MD.
3. Scan GAINLOSSTOT F-1 C (300 s timeout) tidak dilanjutkan dengan chunking/daftar file — padahal
   M2 sendiri menunjukkan pola chunk 250k baris (D1e §11.1). Ini satu-satunya angka kunci yang
   tetap tak terverifikasi ulang (A1 §6c).
4. Adaptasi positif: `execute_code` diblokir kebijakan → semua tim pindah ke skrip `.py` + terminal
   (dokumentasi M2 §2) — respons yang benar terhadap tool failure, bukan objective failure.

---

## 2. CEK DOKUMEN FIKTIF + ANTI-GESER-GATE

**Dokumen fiktif: TIDAK DITEMUKAN.**
- 12 file output ada fisik di `docs/` (ls diverifikasi PM, ukuran 11–35 KB).
- A1 membuka 8/9 sitasi langsung (0 URL palsu, 0 rumus salah kutip; 1 CAPTCHA = dilaporkan
  "tidak bisa diverifikasi", bukan dipakai menopang klaim).
- 9 klaim data dihitung ulang A1 ke file primer: 6 EKSAK, 3 dikoreksi terbuka (§3).
- PM menguji 4 klaim sendiri ke file primer: labels_curated 884 EKSAK; F-9 A 419.747/45.715 EKSAK;
  onset strict-34 EKSAK; kolom STUCK_RT 0/1/2/3 EKSAK. **Nol klaim karangan terkonfirmasi.**

**Anti-geser-gate: LULUS (A1 §3 + konfirmasi PM).**
- G1 lift ≥1,5 mayoritas · G2 RF ≥ canary · <30 positif = UNDERPOWERED · persistence → bersyarat ·
  LOWO · fitur lampau/label depan · kanal pembentuk label dilarang jadi fitur: **identik V6**.
- Yang berubah = (a) definisi LABEL (status→onset/progresi/fisika), (b) TAMBAH DATA (wellbore baru
  yang benar-benar punya kanal), (c) opsi UNIT (stand), (d) reformulasi model — **semuanya menuntut
  pra-registrasi baru yang di-hash sebelum training** (R1 §8, M2 §9). Ini koreksi estimand yang
  dinyatakan terbuka, bukan geseran diam-diam. Selaras prinsip diabetes-80%: memperbaiki definisi
  "apa yang diprediksi" = metode sah; menurunkan ambang = curang (tidak dilakukan).

---

## 3. KONSISTENSI ANGKA (termasuk verifikasi independen PM)

| # | Klaim (sumber) | Angka awal | Koreksi | Status akhir | Verifikasi PM |
|---|---|---|---|---|---|
| 1 | labels_curated_v2 event | R1: 1.412 | M2: 884; A1 EKSAK 884 | **884** | PM hitung ulang sendiri: **884 record, 884 event_id unik** ✅ EKSAK |
| 2 | Event kurasi dalam rentang CSV parsed | M2: 582/884 | A1: 523 (2 baris sentinel 2015-09-22 per CSV mem-blow-up rentang) | **523** | diterima (metode A1 eksplisit: buang sentinel) |
| 3 | Onset stuck F-9_A (S-A1) | M2: 50 (biner 74) | A1: strict 34, tdk reproduce M2 | **method-dependent: strict 34 / ffill 74** | PM hitung 3 varian: strict **34** ✅ EKSAK vs A1; ffill **74**; runs 9.871 (dipecah NaN). Angka M2 "50" **tidak reproduce oleh definisi mana pun** → M2 keliru; definisi onset WAJIB dikunci pra-reg (Fase 0) |
| 4 | Onset stuck F-14 | (M2 tidak rinci) | — | strict **0**; ffill 87; runs 394 (sporadis, 394 baris ≥1 dari 1,65 juta) | PM: F-14 STUCK_RT sangat jarang & terserak → fold F-14 untuk label onset lemah; daya tertumpu pada F-9_A + parse F-10/F-12 |
| 5 | S-F1 kandidat onset bit_wear | M2: 1.489 | A1: 481 awal blok high_MSE (329 dari normal) | **481/329** | diterima (A1 skrip terbuka `a1_usrop_trans.py`) |
| 6 | "Inefisiensi parah" USROP | 78.212 (kutipan V6 R1, dibawa M2) | A1: non-normal 64.915 | **64.915** | diterima (stale; jangan dipakai ulang) |
| 7 | Positif shk wellbore baru | R1: est. 100–200/well | M2 (recount D1e): F-10 798 (0,27%), F-12 580 (1,59%), F-4 50, F-15 13, F-15B 0 | **angka M2** | jalur shk = F-10 + F-12 saja; F-4/F-15 nyaris nol |
| 8 | Kanal dysfungsi F-10/F-4/F-12/F-15 | R1 scan: 188/186/66/18/125 dst | D1e recount COCOK PERSIS; A1 D6 EKSAK | **tripel-terverifikasi** | konsisten |
| 9 | uidRef bhaRun→tubular | M2: 154/161 | A1 D5 EKSAK 154/161 | **154/161** | konsisten |
| 10 | F-9 A time.csv rows / STUCK_RT non-null | M2: 419.747 / 45.715 | A1 D4 EKSAK | **419.747 / 45.715** | PM hitung ulang sendiri ✅ EKSAK |
| 11 | Prev stuck F-9_A | V6: 66,9% (jendela) vs D1h: 49,4% (baris mentah) | **BELUM direkonsiliasi** (diakui M2 §8#1, A1 §7#3) | terbuka | tidak menyangkal jalur (onset reframing membuang label status); wajib direkonsiliasi sebelum pra-reg stuck |

**Kontradiksi tersisa yang harus diselesaikan sebelum eksekusi** (bukan sebelum vonis):
(a) definisi onset stuck (butir 3) → Fase 0; (b) prev 66,9% vs 49,4% (butir 11) → Fase 0;
(c) GAINLOSSTOT F-1 C 575 file belum dihitung ulang (timeout) → relevan hanya untuk S-C2 jalur
penuh (upside), jalur cepat S-C2 F-9 A (345.442 baris) tidak bergantung padanya.

---

## 4. WHAT-IF ORACLE — PETA KEMUNGKINAN (5 cabang)

Pertanyaan yang diasah: "JIKA kerangka eksekusi V7 (Fase 0–3) dijalankan dengan gate identik V6,
berapa kelas LULUS pada akhirnya?"

| Cabang | Prob. | Narasi | Konsekuensi |
|---|---|---|---|
| **Ω Best** | 15% | Onset reframing bekerja di semua kelas; S-C1 menemukan sinyal precursor; change-point tool_wear valid | **7 kelas** LULUS/G1+G2 |
| **α Likely** | 45% | shk lolos (positif nyata 798+580, G2 sudah 6/7); bit_wear lolos (481 onset, persistence hancur per konstruksi); stuck mepet di ambang daya; hyd/tool_wear gagal tes pembeda | **5 kelas** (target minimum tercapai) |
| **Δ Worst** | 20% | stuck jatuh UNDERPOWERED (onset ketat 34, F-14 sporadis); shk fold baru tidak stabil lift; bit_wear lolos | **4 kelas** — masih > V6 (2); vonis tetap LEBIH BAIK, target 5 gagal |
| **Ψ Wild card** | 12% | Semantik kode STUCK_RT 0/1/2/3 / SHKRSK_RT ternyata bukan "kejadian" tapi severity-instrumen yang berubah makna antar wellbore → label onset 4 wellbore tidak sebanding | stuck + shk terdampak; jalur shk perlu re-label semantik; 3–4 kelas |
| **Φ Contrarian** | 8% | "V7 tidak lebih baik — belum ada kelas baru yang LULUS" | Ditolak dengan bukti: kriteria operator (session_search, kutip verbatim di §0) menilai KELAYAKAN JALUR metode-sah, bukan hasil run; jalur shk+bit_wear punya data & mekanisme terverifikasi 3 pihak + auditor |
| **∞ Second-order** | — | Setiap relabel = pra-reg baru → muncul tekanan "prae-reg shopping" (kampanye beruntun E1b–E1d sudah diperingatkan V6 §6.8) | Mitigasi wajib di Fase 0: semua pra-reg (onset stuck, onset bit_wear, shk wellbore baru) di-hash SEKALIGUS sebelum training mana pun |

**Robust moves (menguntungkan di ≥3 cabang):** Fase 0 (kunci definisi + daya), parse F-10/F-12
(melayani stuck + shk sekaligus), S-F1 bit_wear (termurah, G1 3/4).
**Hedge:** S-C2 jalur cepat F-9 A (nol parse) untuk tes prevalensi hyd sebelum investasi parse besar.

---

## 5. COUNCIL SYNTHESIS (consciousness-council, 5 arketip)

🎭 **Empiricist**: Vonis harus berdiri di atas angka terverifikasi — 3 pihak menghitung F-10 identik;
884 dan strict-34 terekak; 4 koreksi auditor jujur. Ini basis fakta terkuat sejauh ini di proyek ini.

🎭 **Contrarian**: "LEBIH BAIK tanpa satu pun kelas baru LULUS = penilaian jalur, bukan hasil.
Risiko self-congratulation." — Tapi kriteria operator memang jalur; dan konsekuensinya nyata:
jalur shk+bit_wear tidak bergantung opini, melainkan pada positif & onset yang sudah terhitung.

🎭 **Pragmatist**: Fase 0–2 = ~1–2 minggu, beban parse ~825 file (chunked, terbukti di V6).
Target 5 layak; lantai 4 layak. Yang tidak layak: menunda eksekusi karena sempurna-syarat.

🎭 **Architect**: Akar kegagalan V6 (persistence/status, positif langka, n=4+confound) semuanya
punya mekanisme pemulihan eksplisit di V7 — ini struktur yang benar, bukan tambal sulam.

🎭 **Strategist**: Urutan Fase 0→1→2 menghasilkan informasi termurah dulu (relabel = nol parse);
keputusan stop/go stuck dipicu hasil hitung daya, bukan perasaan.

**Points of convergence (4/5+):** vonis LEBIH BAIK sah; shk & bit_wear = dua kelas dengan
kekuatan bukti tertinggi; stuck = titik rapuh utama; eksekusi wajib dimulai dengan Fase 0.
**Core tension:** vanis diucapkan pada "jalur", bukan "hasil" — ketegangan ini diselesaikan dengan
mengikat vonis ke kerangka eksekusi + kriteria stop/go yang jelas (§7), bukan dengan menunda vonis.
**Blind spot yang tidak dibahas siapa pun:** semantik kode 0/1/2/3 kanal dysfungsi (Ψ) — bisa
menggugurkan kesebandingan label onset lintas wellbore; masuk sebagai prasyarat pra-reg.

---

## 6. VONIS RESMI + ALASAN STRUKTURAL

**LEBIH BAIK.** Alasan struktural (bukan perasaan):

1. **Akar kegagalan V6 terpetakan dan ditargetkan langsung** (A1 §5): persistence-dominance →
   onset reframing (dibunuh per konstruksi); positif langka shk → wellbore baru dengan positif
   nyata; mayoritas-1-suara stuck → fold 2→4; plafon lift tool_wear → label progresi. V6 gagal
   karena FORMULASI, dan V7 memperbaiki formulasi — bukan memindahkan masalah.
2. **Temuan data empiris baru yang terverifikasi 3 pihak**: 4 wellbore kaya kanal dysfungsi
   (termasuk STUCK_RT F-10 18 file / 15.300 baris) = tambahan positif NYATA, bukan simulasi.
   Di V6, jalur "F-1 C/F-11" yang diaspirasikan ternyata NOL kanal (ditepis R1 dengan scan 3.906
   file, dikonfirmasi D1e) — V7 jujur mengganti jalur mati dengan jalur hidup.
3. **Metode sah menurut prinsip operator**: gate identik; label non-sirkular; data nyata; evaluasi
   jujur (4 koreksi angka dilaporkan sendiri/diaudit); perubahan label = pra-reg baru, bukan
   penggeseran ambang.
4. **Vonis tidak bergantung pada optimism**: lantai 4 kelas lolos (> baseline 2) sudah didukung
   dua jalur dengan bukti terkuat (shk: G2 6/7 + 798/580 positif; bit_wear: G1 3/4 + 481 onset).

**Yang TIDAK diklaim:** tidak ada kelas baru yang LULUS pada saat vonis ini ditulis; tidak ada
janji stuck/hyd/tool_wear; angka onset V6 tidak boleh dibandingkan dengan angka onset V7 (estimand
berbeda — A1 §3).

---

## 7. KERANGKA EKSEKUSI JUJUR (tanpa menggeser gate)

Aturan tetap (dibawa ke setiap kampanye): G1 lift RF ≥1,5 mayoritas fold layak dinilai · G2
AUPRC RF ≥ canary-kedalaman mayoritas · <30 positif = UNDERPOWERED · LOWO · fitur lampau/label
depan · kanal pembentuk label dilarang jadi fitur · persistence > RF = layak bersyarat.

**Fase 0 — Pra-syarat ilmiah (≈0,5 hari, WAJIB sebelum training apa pun)**
1. Kunci definisi onset stuck: resolusi (grid 60 dtk + ffill?) → hitung onset per wellbore;
   jika <30/well setelah definisi dikunci → stuck berstatus "layak diuji, TIDAK dijanjikan LULUS".
2. Rekonsiliasi prev F-9_A 66,9% vs 49,4% (basis jendela vs baris).
3. Tulis + hash SEMUA pra-reg baru sekaligus (onset bit_wear, onset stuck, kampanye shk wellbore
   baru) — satu paket, mencegah prae-reg shopping pasca-hasil (mitigasi V6 §6.8).
4. Verifikasi semantik 0/1/2/3 SHKRSK/STUCK dari sampel nilai lintas wellbore (blind spot §5).

**Fase 1 — Relabel dari data LANGSUNG (≈2–3 hari, nol parse)**
- S-F1 (+S-F2): onset-of-high-MSE dari USROP (481/329 onset jujur) → kampanye `bit_wear` baru.
  Peluang: TINGGI (G1 3/4; hanya hukuman persistence yang dilepas).
- S-A1: onset stuck F-9_A + F-14 → kampanye `stuck` baru. Peluang: SEDANG (tergantung Fase 0).

**Fase 2 — Parse wellbore baru (≈3–5 hari, chunk 250k baris anti-OOM, pola teruji V6)**
- F-10 + F-12 (404 file) → fold `stuck` naik 2→4 (S-A2) + fold `shk` kuat baru.
- F-10 + F-12 + F-4 + F-15 (~825 file total) → kampanye `shk` (798 + 580 positif nyata) +
  memperkuat `ssi`/`vib` (anti-rapuh). Peluang shk: TINGGI (G2 sudah 6/7).

**Fase 3 — Upside dengan tes pembeda (≈3–5 hari, SETELAH jalur 5 diusahakan)**
- S-C1 `hyd` onset: jika lift mayoritas → kelas; jika tidak → "sinyal precursor lintas-kanal
  tidak ada" berstatus terdukuat → beralih ke S-C2 (jalur cepat F-9 A, nol parse, 345.442 baris).
- S-D1 `tool_wear` change-point: jika `t_cp` selalu di detik awal = artefak termal → GUGUR
  (tes pembeda eksplisit R1 §5.2).

**Perkiraan beban total:** ~1,5–2,5 minggu satu pekerja penuh; parse = 825 file XML (~7 GB,
estimasi D1e) — beban terbesar, bisa diparalelkan per wellbore.
**Perkiraan peluang:** bit_wear TINGGI · shk TINGGI · stuck SEDANG (daya) · hyd SEDANG-RENDAH ·
tool_wear SEDANG-RENDAH → **P(capai ≥5) ≈ 60–70%; P(lantai 4) ≈ 25%; P(<4) < 10%** (estimasi
berbasis kekuatan bukti per jalur, bukan janji).

**Stop/go rules (mengikat):** (a) Fase 0 gagal kunci definisi → kampanye stuck ditahan, vonis
turunkan ke "4 kelas terverifikasi jalur"; (b) shk G1 tetap <mayoritas setelah F-10+F-12 →
jalur S-B2 (unit stand) dengan pra-reg baru; (c) TIDAK BOLEH menurunkan ambang mana pun untuk
menyelamatkan kelas — jika sinyal tidak ada, dilaporkan tidak ada.

---

## 8. CATATAN PROSES & BELUM DIVERIFIKASI

1. A1 sempat gagal 1× karena stale_lock (bukan substansi — session_search `20261010_144843_ae785a`);
   rekalm + dispatch ulang → audit selesai. Tidak ada kerja yang diulang dua kali dengan hasil
   berbeda.
2. sequ-mcp dilewati A1 meski terbukti jalan di sesi M2 (hari sama) — pelanggaran proses; masuk
   daftar perbaikan untuk kartu audit berikutnya.
3. GAINLOSSTOT/PITTOT per-file F-1 C/F-11 (klaim 575/517 file) tetap **belum dihitung ulang**
   (timeout 300 s) — hanya relevan untuk S-C2 jalur penuh.
4. Sitasi [16] Saini 2020 tetap tidak terverifikasi (CAPTCHA onepetro) — jangan dipakai menopang
   klaim kunci di dokumen downstream.
5. Isi CSV F-15A/F-15_S (apakah memuat sidetrack C/D) & mapping USROP `N-SH-F-15d` ↔
   `NO 15/9-F-15 D` tetap hipotesis terbuka (M2 §8) — hanya relevan untuk relasi R6/R7 (fitur
   geologi), bukan untuk 5 jalur inti.

---
**Reproduksi verifikasi PM:** `~/.hermes/cache/scratch/pm_verify_t_dd0f1591.py` (884 event;
419.747/45.715; strict-34) dan `pm_onset_variants.py` (3 varian onset F-9_A + F-14/F-9/F-9_A
parsed) — stdlib Python, dijalankan nyata 2026-10-11, output tercetak di sesi.
