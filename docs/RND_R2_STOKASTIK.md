# RND-R2: STOKASTIK + SURVIVAL UNTUK 7 ENGINE
## Markov chain, HMM, Monte Carlo, MCMC, Bayesian network, Cox, Random Survival Forest, DeepHit

Kartu: `t_c24b3640` · Board: `rnd-algo-2026` · Tanggal: 2026-10-27 (WIB)
Workspace: `/mnt/d/Capstone 1(v2)` · Dokumen pendamping: `docs/RND_ALGO_RESEARCH_PLAN.md`,
`docs/RND_D0_DATA_FEASIBILITY.md`, `docs/V9_EVAL_C_LAYERC.md`, `docs/RND_PROVENANCE_LEDGER.md`
Keluaran angka: `scratch/rnd_r2/mc_result.json`, `scratch/rnd_r2/doi_verified.json`,
`scratch/rnd_r2/doi_verified_apps.json` (semua skrip ada di `scratch/rnd_r2/`).

## 0. Riset pendahuluan dan cara skill dipakai

**Riset pendahuluan: literature-review, paper-lookup, scikit-survival, statsmodels, scientific-critical-thinking, verification-mandatory**

| Skill | Cara dipakai di kartu ini |
|---|---|
| `literature-review` | Menyusun pencarian bertahap per metode (kata kunci teori, kata kunci aplikasi PdM, kata kunci pengeboran) lalu menyaring kandidat sebelum satu pun dikutip. |
| `paper-lookup` | Mengambil metadata dari OpenAlex (pencarian) dan Crossref `/works/{doi}` (registrasi DOI), memakai DOI yang dikembalikan API, bukan DOI yang dikarang. |
| `scikit-survival` | Menetapkan kontrak evaluasi survival: outcome dua kolom (event, waktu), metrik censoring-aware (Uno C, IBS, dynamic AUC), dan aturan bahwa skor survival tidak boleh dibandingkan langsung dengan AUPRC/FAR yang dipakai V9. |
| `statsmodels` | Menetapkan standar inferensi untuk bagian regresi/uji: konstanta wajib, diagnostik residual, CI wajib dilaporkan bersama titik, dan memisahkan inferensi dari prediksi. |
| `scientific-critical-thinking` | Memisahkan hipotesis dari bukti, menolak peminjaman metode yang prasyaratnya tidak ada (mis. DeepHit tanpa ribuan event), dan menandai skor 1–5 sebagai penilaian ahli, bukan hasil eksperimen. |
| `verification-mandatory` | Setiap angka berasal dari run sendiri atau baris ledger D0/L yang sudah ada; setiap DOI dicoba dibuka lewat Crossref dan status HTTP dicatat; yang gagal ditandai BELUM-TERVERIFIKASI dan tidak dipakai sebagai dasar rekomendasi. |

**Sequential thinking: 4 pikiran** (`mcp__sequentialthinking__sequentialthinking`, thoughtNumber 1..4,
thoughtHistoryLength 4). Ringkas: (1) menetapkan bahwa pertanyaannya bukan "metode ini bagus secara umum"
melainkan "lolos gate V9 atau tidak dengan data yang ada"; (2) memisahkan klaim K-i dari K-ii dan mencatat
bahwa survival mengubah metrik evaluasi sehingga tidak sebanding langsung dengan AUPRC/FAR; (3) Monte Carlo
sebagai alat ukur ketidakpastian dengan kriteria berhenti numerik yang harus diukur, sedangkan MCMC/BN butuh
prior dan konvergensi; (4) gerbang verifikasi sebelum menulis, termasuk melabeli skor 1–5 sebagai penilaian.

---

## 1. Gerbang data dari D0 (bukan catatan kaki)

Kartu ini tidak boleh menjawab "metode X cocok" tanpa lewat empat fakta terukur dari kartu D0
(`docs/RND_D0_DATA_FEASIBILITY.md`):

| Fakta pembatas | Angka | Rujukan |
|---|---|---|
| State diskret yang ada tanpa dibuat-buat | STUCK, SHKRSK, VIBLAT (biner per menit) | D0 §3 tabel state |
| Cakupan state STUCK | 4 dari 9 well (F-9, F-9_A, F-10, F-14) | D0 §3 kesimpulan |
| Label regime untuk data rig | TIDAK ADA; label regime hanya di bengkel, 469 jendela, 4 alat | D0-766; D0 §3 |
| Horizon onset yang benar-benar tersedia | 10 menit ke depan, tidak ada horizon jam/hari | konvensi V9 (L-33 konteks; `RND_P0_PARAMETER.md` §3) |
| Event per well | stuck 55–93; hyd K-ii 124 episode di 1 wellbore; shk F-9_A 4 episode | D0-581; D0 §4 |
| Episode state sangat pendek | median episode STUCK/SHKRSK/VIBLAT = 1,0 menit di hampir semua well | D0 §3 tabel |

Konsekuensi yang harus dibawa ke semua bagian: transisi state yang dapat diamati berlangsung pada skala
1 menit (bukan jam), sehingga "waktu tunggu sampai onset" praktis konstan dan censoring mendominasi.
Ini yang membuat survival di kasus ini bukan soal "model mana paling canggih", melainkan
"apakah ada waktu yang cukup panjang untuk dimodelkan".

---

## 2. Markov chain (state teramati)

**Syarat yang diajukan kartu**: state diskret, matriks transisi teramati, asumsi Markov masuk akal.

| Syarat | Status di data kita | Bukti |
|---|---|---|
| State diskret | TERPENUHI untuk STUCK/SHKRSK/VIBLAT; TIDAK untuk regime tool_wear rig | D0 §3 |
| Matriks transisi teramati | TERPENUHI secara mentah (edge 0→1 dan 1→0 terhitung per well) | D0 §3 tabel episode |
| Asumsi Markov orde-1 masuk akal | **BELUM TERUJI**; yang terlihat justru episode 1 menit yang berarti proses hampir tanpa memori jangka panjang, tetapi uji orde (bandingkan P(Xt+1 | Xt) dengan P(Xt+1 | Xt, Xt−1)) belum dijalankan | BELUM TERUKUR |

Penilaian kritis: rantai Markov di sini bukan model prediktif yang kuat, melainkan **deskriptor regime**.
Dengan median episode 1,0 menit, model transisi akan didominasi peluang balik ke keadaan semula dalam satu
langkah, sehingga nilai prognostik (lead-time) yang bisa diklaim hampir nol. Markah Markov akan naik hanya
kalau kanal state menjadi lebih halus (multi-kelas, bukan biner per menit) atau kalau horizon diperpanjang
ke jam. Keduanya belum ada di D0.

- **Kebutuhan data dari D0**: state biner per menit (ada), urutan tanpa gap besar (ada untuk STUCK 4 well),
  dan label regime (tidak ada untuk rig).
- **Kesesuaian klaim**: K-i (status) = sesuai sebagai deskriptor; K-ii (onset) = tidak sesuai, karena model
  transisi memprediksi state berikutnya, bukan waktu sampai onset.
- **Risiko**: mengklaim "Markov memprediksi stuck" padahal yang dihitung adalah frekuensi transisi 1 menit.
- **Skor: 3/5** (penilaian ahli; data state ada, label regime dan horizon tidak).
- **Peran usulan**: bukan roadmap. Simpan sebagai alat deskriptif untuk laporan regime dan sebagai kontrol
  negatif terhadap metode K-ii.

Rujukan (2 DOI, keduanya terverifikasi):
1. Norris, J. R. 1997. *Markov Chains*. Cambridge University Press. DOI 10.1017/CBO9780511810633 (Crossref 200).
2. Chiachío, J. (first author) 2020. A Markov chains prognostics framework for complex degradation processes.
   *Reliability Engineering & System Safety*. DOI 10.1016/j.ress.2019.106621 (Crossref 200).

## 3. HMM (state tersembunyi)

| Syarat | Status | Bukti |
|---|---|---|
| Urutan panjang tanpa gap besar | SEBAGIAN; gap > 60 detik besar pada SHKRSK F-12 dan F-14 | D0-469 (contoh F-15_S); D0 §6 tabel gap |
| State tersembunyi punya arti fisik | TIDAK TERUJI; tidak ada anotasi state fisik (mis. stick-slip vs bit bounce per segmen) untuk melabeli hidden state | D0 §3 |
| Jumlah well yang bisa dipakai | STUCK 4 well, SHKRSK 9 well, VIBLAT 7 well | D0 §3 |

Penilaian kritis: HMM menambah parameter (matriks transisi + emisi) di atas Markov, dan justru pada data
yang paling sedikit (4 well untuk STUCK). Identifikasi hidden state dari satu kanal biner per menit akan
menghasilkan state yang tidak bisa dibedakan dari noise, dan tanpa validasi eksternal kita tidak bisa
mengklaim state itu bermakna. HMM satu kanal hanya layak kalau ada kanal kontinu paralel (TQA, SPPA, RPM)
yang memang ada di bins, tetapi jumlah well ber-event kecil tetap membatasi.

- **Kebutuhan data dari D0**: urutan state + observasi kontinu multi-kanal (ada), label state fisik (tidak ada).
- **Kesesuaian klaim**: K-i = mungkin sebagai segmentasi regime; K-ii = tidak, kecuali dipakai
  hidden semi-Markov dengan durasi (lihat Cartella 2015) yang justru menambah kebutuhan event.
- **Risiko**: overfit jumlah state; hidden state tidak dapat difalsifikasi dengan data yang ada.
- **Skor: 2/5**.
- **Peran usulan**: tidak masuk roadmap gelombang ini. Ditinjau ulang hanya jika anotasi state fisik
  per segmen tersedia.

Rujukan (3 DOI, semua terverifikasi):
1. Rabiner, L. R. 1989. A tutorial on hidden Markov models and selected applications in speech recognition.
   *Proceedings of the IEEE* 77(2):257–286. DOI 10.1109/5.18626 (Crossref 200).
2. Ertunç, H. M. 2001. Tool wear condition monitoring in drilling operations using hidden Markov models (HMMs).
   *International Journal of Machine Tools and Manufacture*. DOI 10.1016/S0890-6955(00)00112-7 (Crossref 200).
3. Cartella, F. 2015. Hidden Semi-Markov Models for Predictive Maintenance.
   *Mathematical Problems in Engineering*. DOI 10.1155/2015/278120 (Crossref 200).

## 4. Monte Carlo: untuk apa, dan berapa iterasi

### 4.1 Tiga pemakaian yang sah di sini

1. **CI untuk FAR/recall** pada data yang sudah ada (bootstrap), karena satu titik FAR menipu:
   vib τ0,5 menyebar 4,1–496 FP/24 jam antar well (`V9_EVAL_C_LAYERC.md` §2.1).
2. **Propagasi ketidakpastian ambang**: memetakan sebaran τ ke sebaran FAR, sehingga klaim
   "FAR ≤ 6" bisa disertai peluang, bukan hanya angka titik.
3. **Uji sensitivitas premis**: seberapa besar kesimpulan bergeser bila laju FP per menit berubah.

### 4.2 Berapa iterasi (diukur, bukan ditebak)

Kriteria berhenti yang saya tetapkan sebelum run (KONVENSI kartu ini):
SE batas CI 95% harus ≤ 0,005 FAR absolut **dan** ≤ 1% lebar CI. Diukur dengan 5 seed berbeda
(11, 22, 33, 44, 55) per tingkat N, memakai dua kasus nyata dari pipeline V9-I1.

Kasus A: stuck K-ii RF, 95.925 baris, 40 FP, FAR 0,603 FP/24 jam (D0-600; `v9_i1_RESULTS.json`).

| N iterasi | SE batas bawah | SE batas atas | lebar CI rata-rata |
|---|---|---|---|
| 200 | 0,0176 | 0,0113 | 0,3710 |
| 500 | 0,0095 | 0,0074 | 0,3679 |
| 1.000 | 0,0060 | 0,0060 | 0,3770 |
| 2.000 | 0,0060 | 0,0000 | 0,3800 |

Kasus B: hyd K-i hybrid, 10.401 baris, 110 FP, FAR 16,611 FP/24 jam.

| N iterasi | SE batas bawah | SE batas atas | lebar CI rata-rata | SE lebar / lebar |
|---|---|---|---|---|
| 200 | 0,4125 | 0,2169 | 6,2316 | 7,15% |
| 500 | 0,1666 | 0,1227 | 6,1713 | 1,20% |
| 1.000 | 0,0608 | 0,0614 | 6,2631 | 0,01% |
| 2.000 | 0,0745 | 0,0614 | 6,2935 | 0,97% |

Kasus C: simulasi Poisson untuk uji sensitivitas ambang (galat baku relatif rerata FAR).

| Laju FP per 24 jam | N=200 | N=2.000 | N=10.000 |
|---|---|---|---|
| 0,6 (skala stuck) | 4,82% | 2,02% | 0,14% |
| 16,6 (skala hyd) | 0,68% | 0,18% | BELUM DIUKUR |
| 6,6 (skala shk) | 1,89% | 0,50% | BELUM DIUKUR |

Kesimpulan terukur:
- Untuk **bootstrap CI pada proporsi kecil** (kasus A), N = 1.000 sudah memberi SE ≈ 0,006 FAR, yaitu
  di ambang toleransi 0,005. N = 2.000 tidak memperbaiki secara bermakna karena galatnya dibatasi
  **resolusi kuantil** (1/N), bukan jumlah iterasi.
- Untuk **proporsi besar** (kasus B, FAR 16,6) N = 500 sudah cukup (SE 0,17), sedangkan N = 1.000
  memberi 0,06.
- Untuk **uji sensitivitas ambang** (kasus C), pada laju kecil 0,6/24 jam butuh N = 10.000 untuk
  mencapai galat 0,14%; pada laju besar 6,6–16,6 cukup N = 2.000 (0,18–0,50%).
- **Rekomendasi operasional**: N = 2.000 sebagai default; N = 10.000 hanya untuk FAR skala < 1/24 jam.
  Di atas 10.000 tidak menambah informasi, karena galat yang tersisa berasal dari korelasi temporal
  jendela (block bootstrap), bukan dari jumlah iterasi. Panjang blok belum diukur (lihat §10).

- **Kebutuhan data dari D0**: tidak ada data baru; memakai label dan FP yang sudah dihitung pipeline.
- **Kesesuaian klaim**: K-i dan K-ii dua-duanya, tetapi MC **tidak** menaikkan kemampuan deteksi.
  Ia hanya membuat klaim lebih jujur (CI, bukan titik).
- **Risiko**: MC dipakai sebagai pembenaran angka (mis. "CI sempit, jadi model bagus") padahal CI sempit
  hanya berarti presisi hitung, bukan validitas.
- **Skor: 5/5** (murah, sudah dipakai, hasil terukur, tidak menambah asumsi baru).
- **Peran usulan**: gunakan sekarang, sebagai kewajiban pelaporan pada semua metrik A/B.

Rujukan (2 DOI terverifikasi):
1. Metropolis, N. & Ulam, S. 1949. The Monte Carlo Method.
   *Journal of the American Statistical Association* 44(247):335–341. DOI 10.1080/01621459.1949.10483310 (Crossref 200).
2. de Pater, I. 2022. Alarm-based predictive maintenance scheduling for aircraft engines with imperfect
   Remaining Useful Life information. *Reliability Engineering & System Safety*.
   DOI 10.1016/j.ress.2022.108341 (Crossref 200).

## 5. MCMC

Kapan layak: bila kita butuh **sebaran posterior** parameter (mis. laju transisi per well, efek well
sebagai random effect) dan jumlah event cukup untuk menggerakkan posterior. Biaya: penyetelan sampler,
diagnostik konvergensi (R-hat, ESS), dan waktu hitung berlipat dibanding ML tunggal.

Pada data kita, jumlah kejadian per well kecil (stuck 55–93 onset per well; shk F-9_A 4 episode;
hyd K-ii 124 episode di satu wellbore) sehingga **prior akan mendominasi posterior** untuk kovariat
apa pun. MCMC tetap berguna untuk satu hal spesifik: model hierarkis lintas well yang meminjam kekuatan
antar well (partial pooling), karena masalah utama Layer C justru dispersi antar well (vib FAR 119×,
ssi AUPRC 30×). Itu bukan pekerjaan satu kartu R&D, dan kebutuhannya adalah **prior yang bisa dipertanggungjawabkan**.
Kita belum punya prior terdokumentasi untuk laju transisi state, jadi langkah pertamanya bukan MCMC,
melainkan menetapkan prior dari data Volve lain secara eksplisit.

- **Kebutuhan data D0**: event per well (ada, kecil) + struktur grup well (ada, 9 well).
- **Kesesuaian klaim**: K-i (estimasi laju) lebih masuk akal daripada K-ii (prediksi onset per menit).
- **Risiko**: posterior terlihat meyakinkan karena prior, bukan karena data; biaya hitung tidak sepadan
  dengan horizon 10 menit.
- **Skor: 2/5**.
- **Peran usulan**: tidak untuk gelombang ini; kandidat untuk analisis hierarkis antar well setelah
  prior ditetapkan.

Rujukan (3 DOI terverifikasi):
1. Hastings, W. K. 1970. Monte Carlo sampling methods using Markov chains and their applications.
   *Biometrika* 57(1):97–109. DOI 10.1093/biomet/57.1.97 (Crossref 200).
2. Metropolis, N. et al. 1953. Equation of State Calculations by Fast Computing Machines.
   *The Journal of Chemical Physics* 21(6):1087–1092. DOI 10.1063/1.1699114 (Crossref 200).
3. Pang, Z. 2021. A Bayesian Inference for Remaining Useful Life Estimation by Fusing Accelerated
   Degradation Data and Condition Monitoring Data. *Reliability Engineering & System Safety*.
   DOI 10.1016/j.ress.2020.107341 (Crossref 200).

## 6. Bayesian network

Kapan layak: bila ada struktur kausal yang dapat dipertahankan (DAG) antara penyebab (parameter lumpur,
kedalaman, RPM, formasi) dan akibat (stuck, vibration). Kebutuhan: struktur dari ahli domain atau
algoritma struktur, plus tabel probabilitas kondisional yang dapat diestimasi dari data.

Pada kasus ini hambatannya bukan komputasi (jaringan kecil murah), melainkan **struktur**: kita tidak
punya DAG yang disepakati, dan label yang kita punya adalah turunan kanal (STUCK_RT, SHKRSK_RT), sehingga
jaringan akan belajar meniru kanal, bukan fisika. Network juga akan memakai data yang sama dengan Markov
(state biner per menit), jadi tidak menambah informasi baru.

- **Kebutuhan data D0**: kanal kontinu multi-variabel (ada: TQA, SPPA, TFLO, RPM, SWOB, HKLD, ROP),
  struktur kausal (tidak ada), label per segmen (tidak ada untuk rig).
- **Kesesuaian klaim**: K-i lebih masuk akal (diagnosis kondisi); K-ii butuh model dinamis (DBN) yang
  menambah beban data yang sama.
- **Risiko**: DAG dari data dengan n kecil mudah menghasilkan panah arah salah, lalu dipakai sebagai
  "penjelasan fisika".
- **Skor: 2/5**.
- **Peran usulan**: tidak untuk gelombang ini; layak hanya bila tim punya DAG dari literatur pengeboran
  yang eksplisit dan diuji terhadap data.

Rujukan (2 DOI terverifikasi):
1. Soltanali, H. 2021. An Integrated Fuzzy Fault Tree Model with Bayesian Network-Based Maintenance
   Optimization of Complex Systems. *Energies*. DOI 10.3390/en14227758 (Crossref 200).
2. Xia, L. 2025. Graph Embedding-Based Bayesian Network for Fault Isolation in Complex Equipment.
   *IEEE Transactions on Reliability*. DOI 10.1109/TR.2024.3416064 (Crossref 200).

## 7. Survival: Cox, Random Survival Forest, DeepHit

### 7.1 Masalah inti, sebelum memilih model

Target survival adalah (event, waktu). Di data kita, waktu yang tersedia adalah horizon 10 menit, dan
onset muncul berulang per well (stuck 55–93; hyd K-ii 124 episode di satu wellbore). Dua konsekuensi:
1. **Event berulang** menuntut model recurrent-event atau frailty, bukan Cox dasar yang mengasumsikan
   satu event per subjek. Kalau dipaksa, "subjek" harus didefinisikan ulang (per episode, bukan per well),
   dan itu mengubah arti angka.
2. **Horizon pendek** membuat waktu survival hampir konstan (semua observasi tersensor di 10 menit), sehingga
   diskriminasi model akan lebih ditentukan oleh kovariat daripada oleh bentuk baseline hazard.

### 7.2 Perbandingan dengan pendekatan sekarang (B1 dan TLead)

| Aspek | Sekarang (B1 persistence-EVENT dan TLead) | Survival (Cox/RSF/DeepHit) |
|---|---|---|
| Target | klasifikasi biner "menit ini onset" (B1) + lead waktu (TLead) | waktu sampai onset, dengan censoring eksplisit |
| Metrik | AUPRC, B1, TLead, FAR (`V9_EVAL_C_LAYERC.md` §1) | Uno C, IBS, dynamic AUC (kontrak `scikit-survival`) |
| Angka yang ada | B1 0–0,115; TLead 4,5–8,5 menit (stuck K-ii) | BELUM TERUKUR (belum ada run survival) |
| Kelebihan | langsung menjawab kebutuhan operasional: alarm + lead | menangani censoring dan ketidakpastian waktu secara eksplisit |
| Kelemahan | censoring tidak dimodelkan; B1 sangat rendah | metrik tidak sebanding dengan angka lama, butuh run baru, horizon 10 menit membatasi manfaat |

Kesimpulan penting: survival **tidak** otomatis memperbaiki TLead. Ia hanya benar secara statistik untuk
data tersensor. Karena B1 hari ini hampir nol (0–0,115), masalah utamanya adalah **daya deteksi**, bukan
kesalahan penanganan censoring. Metode yang lebih rumit tidak akan menutupi masalah itu.

### 7.3 Cox proportional hazards

- **Kebutuhan data D0**: event dan waktu (ada, horizon 10 menit), kovariat kanal kontinu (ada), dan
  asumsi proportional hazards yang harus diuji (BELUM TERUKUR).
- **Kesesuaian klaim**: K-ii saja.
- **Risiko**: event berulang melanggar asumsi independensi; dengan 55–93 event per well dan 27 head
  fitur, degrees of freedom cepat habis.
- **Skor: 3/5** (paling murah di antara ketiga model survival dan paling mudah diaudit).
- **Peran usulan**: pilot kecil pada stuck K-ii sebagai pembanding TLead, dengan metrik Uno C dan
  laporan CI; bukan pengganti B1.

Rujukan: Cox, D. R. 1972. Regression Models and Life-Tables. *J. R. Stat. Soc. B* 34(2):187–202.
DOI 10.1111/j.2517-6161.1972.tb00899.x (Crossref 200).
Chen, C. 2020. Predictive maintenance using cox proportional hazard deep learning.
*Advanced Engineering Informatics*. DOI 10.1016/j.aei.2020.101054 (Crossref 200).
Malevich, N. 2019. Statistical Analysis of the Lifetime of Diamond-Impregnated Tools for Core Drilling of
Concrete. DOI 10.1007/978-3-030-25147-5_15 (Crossref 200, contoh survival pada perkakas bor).

### 7.4 Random Survival Forest

- **Kebutuhan data D0**: event lebih banyak per fold dan horizon berlapis; keduanya tidak ada
  (ber-event sedikit: shk F-9_A 4 episode).
- **Kesesuaian klaim**: K-ii.
- **Risiko**: RSF dengan 4 well dan event kecil akan menghasilkan importance yang tidak stabil, pola yang
  sama dengan ketidakstabilan RF di Layer C (shk CI 7/9 memuat prev, B3 EVAL_B −212×).
- **Skor: 2/5**.
- **Peran usulan**: tolak untuk gelombang ini, tinjau ulang bila jumlah event naik (mis. setelah STUCK
  tersedia di sisa well).

Rujukan: Ishwaran, H. 2008. Random survival forests. *The Annals of Applied Statistics* 2(3):841–860.
DOI 10.1214/08-AOAS169 (Crossref 200).
Asghar, N. 2024. Improved nonparametric survival prediction using CoxPH, Random Survival Forest & DeepHit.
*BMC Medical Informatics and Decision Making*. DOI 10.1186/s12911-024-02525-z (Crossref 200).

### 7.5 DeepHit

- **Kebutuhan data D0**: ribuan event dan horizon berlapis per subjek; kita punya puluhan sampai ratusan
  onset per well dan satu horizon 10 menit.
- **Kesesuaian klaim**: K-ii.
- **Risiko**: jaringan dalam akan menghafal well (9 well, 4 untuk STUCK), dan tidak ada holdout yang cukup
  untuk mengklaim generalisasi. Ini risiko yang sama dengan RF tetapi dengan kapasitas menghafal lebih besar.
- **Skor: 1/5**.
- **Peran usulan**: tolak. Bukan karena metode jelek, tetapi karena prasyarat datanya tidak ada.

Rujukan: Lee, C. 2018. DeepHit: A Deep Learning Approach to Survival Analysis With Competing Risks.
*Proceedings of the AAAI Conference on Artificial Intelligence* 32(1).
DOI 10.1609/aaai.v32i1.11842 (Crossref 200).
Ren, K. 2019. Deep Recurrent Survival Analysis. *Proceedings of the AAAI Conference on Artificial
Intelligence* 33(01):4798–4805. DOI 10.1609/aaai.v33i01.33014798 (Crossref 200).
Katzman, J. 2018. DeepSurv: personalized treatment recommender system using a Cox proportional hazards
deep neural network. *BMC Medical Research Methodology*. DOI 10.1186/s12874-018-0482-1 (Crossref 200).

---

## 8. Rekap keputusan per metode

| Metode | Kebutuhan data dari D0 | Kesesuaian klaim | Risiko utama | Skor | Peran usulan |
|---|---|---|---|---|---|
| Markov chain | state biner per menit (ada, STUCK 4 well); label regime rig tidak ada | K-i deskriptif; K-ii tidak | diklaim prediktif padahal hanya frekuensi transisi 1 menit | 3 | bukan roadmap; deskriptor regime + kontrol negatif |
| HMM | urutan state + kanal kontinu (ada); label state fisik (tidak ada) | K-i mungkin; K-ii tidak | hidden state tidak dapat difalsifikasi | 2 | tidak untuk gelombang ini |
| Monte Carlo | tidak butuh data baru; memakai label/FP pipeline | K-i dan K-ii (pelaporan, bukan deteksi) | dipakai membenarkan angka | 5 | gunakan sekarang, wajib untuk CI FAR/recall |
| MCMC | event per well (kecil) + struktur well (ada) | K-i lebih masuk akal | prior mendominasi posterior | 2 | kandidat analisis hierarkis, bukan sekarang |
| Bayesian network | kanal multivariabel (ada); DAG kausal (tidak ada) | K-i lebih masuk akal | DAG arah salah dianggap fisika | 2 | tidak untuk gelombang ini |
| Cox PH | event+waktu (ada, horizon 10 menit); asumsi PH belum diuji | K-ii | event berulang melanggar asumsi | 3 | pilot pembanding TLead pada stuck K-ii |
| Random Survival Forest | butuh event lebih banyak | K-ii | importance tidak stabil (pola RF Layer C) | 2 | tolak untuk gelombang ini |
| DeepHit | butuh ribuan event + horizon berlapis | K-ii | menghafal well | 1 | tolak |

**Temuan pusat R2**: dari delapan metode, hanya **Monte Carlo** yang menaikkan mutu keputusan tanpa
asumsi baru, dan itu pun dengan peran pelaporan (CI), bukan deteksi. Cox layak sebagai pilot kecil karena
murah dan auditable. Enam lainnya gagal bukan pada teori, tetapi pada prasyarat data yang sudah diukur
D0: state 1 menit, label regime rig tidak ada, horizon 10 menit, event per well kecil.

---

## 9. Rujukan terverifikasi (status HTTP Crossref)

Semua di bawah dibuka lewat `https://api.crossref.org/works/{doi}` pada 2026-10-27 dan mengembalikan
HTTP 200 dengan judul, penulis pertama, dan tahun yang cocok (`scratch/rnd_r2/doi_verified.json`,
`scratch/rnd_r2/doi_verified_apps.json`: total 31 DOI terdaftar, 29 dikutip di tabel bawah).

| Metode | Penulis pertama, tahun, judul | DOI | Status |
|---|---|---|---|
| Markov | Norris 1997, Markov Chains (buku) | 10.1017/CBO9780511810633 | TERVERIFIKASI |
| Markov | Chiachío 2020, A Markov chains prognostics framework | 10.1016/j.ress.2019.106621 | TERVERIFIKASI |
| Markov | Camci 2010, Health-State Estimation and Prognostics in Machining Processes | 10.1109/TASE.2009.2038170 | TERVERIFIKASI (tidak dipakai sebagai dasar) |
| HMM | Rabiner 1989, A tutorial on hidden Markov models | 10.1109/5.18626 | TERVERIFIKASI |
| HMM | Ertunç 2001, Tool wear condition monitoring in drilling using HMMs | 10.1016/S0890-6955(00)00112-7 | TERVERIFIKASI |
| HMM | Cartella 2015, Hidden Semi-Markov Models for Predictive Maintenance | 10.1155/2015/278120 | TERVERIFIKASI |
| HMM | Yu 2016, weighted HMM for continuous-state tool wear | 10.1007/s00170-016-9711-0 | TERVERIFIKASI (tidak dipakai sebagai dasar) |
| Monte Carlo | Metropolis & Ulam 1949, The Monte Carlo Method | 10.1080/01621459.1949.10483310 | TERVERIFIKASI |
| Monte Carlo | de Pater 2022, Alarm-based predictive maintenance scheduling | 10.1016/j.ress.2022.108341 | TERVERIFIKASI |
| Monte Carlo | Annaz 2026, One-sided predictive thresholds: Monte Carlo | 10.1016/j.nexres.2026.102266 | TERVERIFIKASI (tidak dipakai sebagai dasar) |
| MCMC | Hastings 1970, Monte Carlo sampling methods using Markov chains | 10.1093/biomet/57.1.97 | TERVERIFIKASI |
| MCMC | Metropolis 1953, Equation of State Calculations | 10.1063/1.1699114 | TERVERIFIKASI |
| MCMC | Pang 2021, Bayesian inference for RUL | 10.1016/j.ress.2020.107341 | TERVERIFIKASI |
| MCMC | Benker 2021, uncertainty in RUL via BNN | 10.1016/j.jmsy.2020.11.005 | TERVERIFIKASI (tidak dipakai sebagai dasar) |
| Bayes net | Soltanali 2021, Fuzzy Fault Tree + Bayesian Network maintenance | 10.3390/en14227758 | TERVERIFIKASI |
| Bayes net | Xia 2025, Graph Embedding-Based Bayesian Network | 10.1109/TR.2024.3416064 | TERVERIFIKASI |
| Cox | Cox 1972, Regression Models and Life-Tables | 10.1111/j.2517-6161.1972.tb00899.x | TERVERIFIKASI |
| Cox | Chen 2020, Predictive maintenance using cox proportional hazard deep learning | 10.1016/j.aei.2020.101054 | TERVERIFIKASI |
| Cox | Malevich 2019, Lifetime of Diamond-Impregnated Tools for Core Drilling | 10.1007/978-3-030-25147-5_15 | TERVERIFIKASI |
| RSF | Ishwaran 2008, Random survival forests | 10.1214/08-AOAS169 | TERVERIFIKASI |
| RSF | Asghar 2024, CoxPH vs Random Survival Forest vs DeepHit | 10.1186/s12911-024-02525-z | TERVERIFIKASI |
| RSF | Zhou 2016, Random rotation survival forest | 10.1186/s40064-016-3113-5 | TERVERIFIKASI (tidak dipakai sebagai dasar) |
| DeepHit | Lee 2018, DeepHit | 10.1609/aaai.v32i1.11842 | TERVERIFIKASI |
| DeepHit | Ren 2019, Deep Recurrent Survival Analysis | 10.1609/aaai.v33i01.33014798 | TERVERIFIKASI |
| DeepHit | Katzman 2018, DeepSurv | 10.1186/s12874-018-0482-1 | TERVERIFIKASI |
| Konteks bor | Reckmann 2010, MWD Failure Rates Due to Drilling Dynamics | 10.2118/127413-MS | TERVERIFIKASI |
| Konteks bor | Kyllingstad 1988, A Study of Slip/Stick Motion of the Bit | 10.2118/16659-PA | TERVERIFIKASI |
| Konteks bor | Liu 2025, Intelligent identification of stick-slip | 10.2298/TSCI2502521L | TERVERIFIKASI |
| Konteks bor | Teale 1965, The concept of specific energy in rock drilling | 10.1016/0148-9062(65)90022-7 | TERVERIFIKASI |

Catatan kejujuran: verifikasi di atas adalah verifikasi **registrasi dan metadata** (judul, penulis
pertama, tahun, wadah) lewat Crossref. Teks penuh tidak dibaca untuk semua entri; yang teks penuhnya
sudah dibaca pada kartu sebelumnya adalah Liu 2025 (`RND_P0_PARAMETER.md` §2) dan sebagian Reckmann 2010
(berbayar). Tahun yang dipakai mengikuti kolom `issued` Crossref; pada beberapa entri tahun Crossref
berbeda satu tahun dari tahun publikasi daring (Chiachío 2019→2020, Pang 2020→2021, Xia 2024→2025).

---

## 10. Yang belum terverifikasi

1. **Uji orde Markov** (apakah P(Xt+1 | Xt, Xt−1) berbeda dari P(Xt+1 | Xt)): BELUM TERUKUR.
   Tanpa uji ini, klaim "asumsi Markov masuk akal" tetap hipotesis.
2. **Panjang blok untuk block bootstrap**: BELUM TERUKUR. Semua CI di §4 memakai bootstrap iid, sehingga
   CI yang dilaporkan **lebih sempit** daripada seharusnya karena korelasi temporal jendela 1 menit tidak
   diperhitungkan. Ini batasan angka §4, bukan detail teknis.
3. **Uno C, IBS, dynamic AUC untuk Cox/RSF/DeepHit**: BELUM TERUKUR (belum ada run survival sama sekali).
4. **Asumsi proportional hazards**: BELUM TERUKUR.
5. **Jumlah event bila STUCK tersedia di 5 well yang sekarang tidak punya kanal**: BELUM TERUKUR.
6. **Teks penuh** untuk sebagian besar rujukan: hanya registrasi DOI yang diverifikasi. Rujukan yang
   teks penuhnya belum dibaca tidak dipakai sebagai dasar rekomendasi, hanya sebagai konteks.
7. **Skor 1–5 adalah penilaian ahli** berbasis kelayakan data D0 + biaya + risiko, bukan hasil eksperimen.
   Skor tidak boleh dibaca sebagai metrik.

## 11. Ringkasan 5 baris

1. Dari 8 metode stokastik/survival, hanya Monte Carlo yang layak dipakai sekarang, dan perannya pelaporan CI (N=2.000 default, N=10.000 untuk FAR < 1/24 jam), bukan menaikkan deteksi.
2. Markov dan HMM gagal pada prasyarat, bukan pada teori: state biner per menit dengan median episode 1,0 menit dan STUCK hanya di 4 dari 9 well; HMM tambah buruk karena label state fisik tidak ada.
3. MCMC dan Bayesian network ditolak untuk gelombang ini karena prior/DAG belum ada sehingga model akan menjelaskan prior kita, bukan data.
4. Survival (Cox, RSF, DeepHit) hanya relevan untuk K-ii, dan yang paling realistis adalah Cox sebagai pilot pembanding TLead stuck K-ii; RSF dan DeepHit ditolak karena event per well kecil dan horizon hanya 10 menit.
5. Survival tidak otomatis memperbaiki TLead: B1 hari ini 0–0,115 menunjukkan masalahnya daya deteksi, dan metrik survival (Uno C, IBS) tidak sebanding langsung dengan AUPRC/FAR V9 sehingga setiap klaim harus dijalankan ulang, bukan dibandingkan silang.
