# RND-PM: VONIS AKHIR DAN ROADMAP TIER

Kartu: `t_776c0a03` · Board: `rnd-algo-2026` · Tanggal: 2026-10-27 (WIB)
Workspace: `/mnt/d/Capstone 1(v2)` · Folder arsip `/mnt/d/Capstone 1` tidak disentuh.
Masukan yang dibaca: `RND_ALGO_RESEARCH_PLAN.md`, `RND_EVALUATION_POLICY.md`, `RND_D0_DATA_FEASIBILITY.md`,
`RND_P0_PARAMETER.md`, `RND_E0_AUDIT_ENGINE.md`, `RND_E1_MATRIKS.md`, `RND_E2_PROTOKOL.md`,
`RND_E3_HASIL.md`, `RND_E4_PERBAIKAN.md`, `RND_R1_METAHEURISTIK.md`, `RND_R2_STOKASTIK.md`,
`RND_R3_VMD_SVM.md`, `RND_R4_BOOSTING.md`, `RND_R5_DRIFT.md`, `RND_R6_METRIK.md`,
`RND_R7_REVIEW.md`, `RND_R8_EVALUASI_BERLAPIS.md`, `RND_V1_AUDIT.md`, `V9_EVAL_C_LAYERC.md`,
`code/v9_i1_pipeline.py` (REGISTRY), `scratch/v9_i1/v9_i1_RESULTS.json`.

Riset pendahuluan: what-if-oracle, consciousness-council, scientific-critical-thinking, verification-mandatory

- **what-if-oracle**: dipakai untuk memetakan enam cabang keputusan (naik tier sekarang, kalibrasi per well,
  tolak semua, hibrida, tunda sampai data baru, bongkar label) lalu memilih tindakan yang aman di semua cabang,
  yaitu komposisi detektor yang sudah terukur tanpa kenaikan tier.
- **consciousness-council**: dipakai untuk mempertahankan ketegangan antara arketipe Pragmatist (ada detektor
  yang siap dipakai sekarang), Contrarian (angka R8 justru menunjukkan dua dari empat hybrid tidak menambah nilai),
  Empiricist (hanya angka yang boleh menaikkan tier), dan Minimalist (hapus komponen yang tidak memberi nilai),
  sehingga vonis tidak jatuh ke "pakai semua" atau "buang semua".
- **scientific-critical-thinking**: dipakai untuk memisahkan OBSERVASI (angka JSON hasil run) dari INFERENSI
  (komposisi yang diusulkan) dan dari KLAIM YANG BELUM DIUJI (misalnya nilai maintenance), serta untuk menolak
  tiga kesalahan penalaran yang muncul di dokumen sebelumnya: FAR rendah dianggap prestasi padahal recall nol,
  presisi kondisional dianggap kemampuan deteksi, dan generalisasi lintas alat dianggap terbukti dari empat alat.
- **verification-mandatory**: dipakai pada setiap angka di dokumen ini, yaitu setiap angka di-assert terhadap
  berkas JSON mentah oleh `code/rnd_pm_ledger.py` sebelum ditulis ke ledger, DOI diuji dua lapis hari ini,
  dan hal yang tidak terukur ditulis BELUM TERUKUR, bukan ditebak.

Riset pendahuluan: sequentialthinking, 4 pikiran pada eksekusi final kartu ini
(`mcp__sequentialthinking__sequentialthinking`, thoughtNumber 1 sampai 4, thoughtHistoryLength 4).
Ringkas: (1) kunci target, yaitu verifikasi dokumen dan ledger yang sudah ditulis run sebelumnya, bukan
menulis ulang, (2) inventaris bukti mentah yang bisa diuji, termasuk temuan bahwa dokumen mengklaim 120 baris
padahal ledger berisi 121, (3) rancangan pemeriksa yang menguji sitasi, komposisi kelas, tujuh kolom, dan
karakter terlarang, (4) gerbang penutup, yaitu pemeriksa harus bersih dan idempotensi ledger dibuktikan
dengan run ulang, bukan diklaim.

---

## 0. CARA MEMBACA VONIS INI

Vonis tidak diberikan pada satu tingkat saja, karena kebijakan evaluasi yang mengikat menolak itu.
Tiga sumbu dipakai bersamaan:

1. **Sumbu keluarga algoritma**: ADOPSI, PILOT, atau TOLAK, beserta alasan dan batas biaya.
2. **Sumbu kelas kerusakan dan tugas**: detektor tidak harus sama antar kelas, dan tiap kelas dinilai dengan
   baseline tugasnya sendiri.
3. **Sumbu tier pemakaian**: `TREN`, `PERINGATAN-BERPENGAWAS`, `ALARM-OTOMATIS`, atau `BELUM LAYAK PAKAI`,
   dengan tier yang berlaku saat ini diambil dari `docs/V9_EVAL_C_LAYERC.md` dan REGISTRY
   (tujuh detektor, dua puluh tujuh head, PM-076 dan PM-077).

Empat aturan yang mengikat seluruh dokumen ini:

- Gate C/A/B menyatakan **kekuatan bukti kemampuan**, bukan izin pakai (kebijakan bagian 1).
- Detektor yang gagal gate tidak dibuang, tetapi ditulis kemampuan, batas penggunaan, dan kekuatan buktinya
  (kebijakan bagian 5).
- Hybrid dan perpaduan tiga komponen dinilai sebagai kandidat tersendiri, dan hasilnya boleh negatif
  (kebijakan bagian 4).
- **Tidak ada satu pun kenaikan tier di kartu ini.** Slot `ALARM-OTOMATIS` tetap nol (PM-078), karena syarat
  naik tier di EVAL_C bagian 4 belum terpenuhi oleh angka mana pun.

---

## 1. BUKTI YANG DIPAKAI DAN BUKTI YANG TIDAK DIPAKAI

| Sumber | Yang diambil | Status bukti |
|---|---|---|
| `scratch/rnd/r8/*.json` | empat uji hybrid dengan baseline per tugas, seed 42 | RUN-KITA, ter-assert (PM-001 sampai PM-056) |
| `scratch/rnd/e4/*.json` | baseline jujur dari bins, dekomposisi gate, jumlah fitur | RUN-KITA, ter-assert (PM-057 sampai PM-066) |
| `scratch/rnd/e3/*.json` | kegagalan pilot conformal dan cakupan waktu per well | RUN-KITA, ter-assert (PM-067 sampai PM-075) |
| `scratch/v9_i1/v9_i1_RESULTS.json` | tier per head, jumlah head, slot alarm otomatis | RUN-KITA dan KONVENSI (PM-076 sampai PM-078) |
| `docs/RND_R1`, `R2`, `R3`, `R4`, `R5`, `E0` | penilaian keluarga algoritma dan temuan audit | kutipan baris ledger lama (PM-099 sampai PM-110) |
| `scratch/rnd/pm/pm_doi.json` | status dua lapis untuk sepuluh rujukan yang dipakai | JURNAL, ter-assert (PM-079 sampai PM-098) |

Yang **tidak** dipakai sebagai dasar keputusan di dokumen ini:

- Angka yang dicabut audit V1, yaitu angka retoris 55.000 di R1.
- Dua DOI yang gagal registrasi di V1 (`10.1109/TII.2019.2950661`, `10.2307/4615733`).
- Angka FAR bit_wear dalam satuan 24 jam, karena barisnya pada grid kedalaman, bukan deret waktu (E0 S-6).
- Angka TLead `persistence_event` versi lama, karena audit E0 K-2 menemukan kredit lead ke onset yang salah.
- Laporan A1b di E3, karena memakai fitur lag label dan melanggar aturan anti-bocor E2.

---

## 2. VONIS PER KELUARGA ALGORITMA

Kode vonis: **ADOPSI** berarti masuk komposisi detektor sekarang tanpa kenaikan tier, **PILOT** berarti boleh
dijalankan sebagai eksperimen dengan gate dan kriteria berhenti tertulis, **TOLAK** berarti tidak dijalankan
pada gelombang ini dengan alasan yang bisa dibantah.

| Keluarga algoritma | Vonis | Alasan berbasis angka | Batas biaya dan syarat |
|---|---|---|---|
| Metaheuristik kontinu untuk tuning hyperparameter (GWO, WOA, PSO, HHO, SSA, SMA) | **TOLAK** untuk peran tuning | Tidak ada satu pun run di repo yang menunjukkan kenaikan metrik dari tuning (R1 bagian 5.2). Uji metaheuristik yang benar-benar dijalankan, yaitu GWO membungkus ML pada tool_wear, tidak menambah nilai: objektif F1 menghasilkan balanced accuracy 0,5 dengan 240 TP dan 229 FP (PM-038, PM-040, PM-041), sedangkan objektif balanced accuracy memberi 0,3993 lawan 0,3385 pada default (PM-039, PM-037) dengan tanda yang berubah antar alat. Pembatas sebenarnya adalah portabilitas ambang, bukan hyperparameter (R1 bagian 4.4) | Setiap run wajib disandingkan random search pada jumlah evaluasi identik dan baseline tanpa tuning pada fold yang sama; tanpa itu kenaikan tidak bisa diatribusikan |
| BGWO untuk seleksi fitur (T2) | **PILOT** | Belum pernah dijalankan pada data kita, jadi statusnya belum terukur, bukan gagal (PM-117). Ruang masalahnya nyata: jalur ML resmi memakai 40 fitur setelah `ts_bin` dibuang (PM-061) | Anggaran evaluasi harus muat, protokol bersarang wajib, dan fitness harus menghukum dispersi antar well; risiko utama adalah overfit seleksi pada sembilan unit |
| Dekomposisi sinyal VMD, EMD, wavelet | **TOLAK permanen** | Laju sampel tertinggi 0,3333 Hz memberi Nyquist 0,1667 Hz (PM-103, PM-104), sedangkan pita diagnostik bantalan berada pada orde ratusan Hz. Percobaan yang sudah dijalankan: 105 percobaan VMD dengan 75 gagal (PM-105, PM-106) | Tidak ada anggaran yang bisa menutup selisih dua orde laju sampel. Syarat pembuka: kanal dengan laju minimal orde Hz, yang belum ada |
| Kernel SVM | **TOLAK** sebagai pengganti rule, dicatat sebagai pembanding murah | E1 menempatkannya di shortlist dengan skor 2,25 tetapi bukan finalis karena bukan pengganti rule. Tidak ada angka kita yang menunjukkan SVM mengalahkan rule pada FAR yang sama | Boleh dijalankan hanya sebagai pembanding pada anggaran sisa, tidak boleh menjadi dasar kenaikan tier |
| kNN-DTW | **TOLAK** | Biaya 134,01 sampai 137.374,35 jam untuk satu klasifikasi penuh (PM-107) | Biaya melampaui anggaran kartu dan anggaran operasional |
| Matrix profile | **PILOT** gelombang ketiga | Berguna sebagai penunjuk episode mirip untuk pemeriksaan manual, bukan alarm. Data pendukung hanya SEBAGIAN karena butuh deret rapat | Wajib lulus uji manfaat lebih dulu: waktu pencarian manual turun, bukan AUPRC naik |
| Markov chain, HMM, Bayesian network, MCMC | **TOLAK** untuk gelombang ini | Prasyarat datanya tidak ada: label state fisik tidak tersedia, dan episode sangat pendek sehingga memori praktis nol (D0 bagian 7, R2 bagian 8). MCMC dan Bayesian network ditolak karena prior dan DAG belum ada, sehingga model akan menjelaskan prior kita, bukan data | Dapat dibuka kembali bila label state fisik tersedia dan uji orde Markov dijalankan |
| Monte Carlo | **ADOPSI** sebagai kewajiban pelaporan | R2 menilainya satu-satunya metode dari delapan yang menaikkan mutu keputusan tanpa asumsi baru, dengan peran pelaporan selang, bukan deteksi (skor 5) | Biaya komputasi kecil. Wajib dipakai untuk CI FAR dan recall pada laporan detektor |
| Survival: Cox PH | **PILOT** kecil | Murah dan auditable, relevan hanya untuk klaim K-ii, dan belum dijalankan pada data kita | Wajib pra-registrasi TLead dan uji asumsi proportional hazards; event berulang adalah risiko utama |
| Survival: Random Survival Forest, DeepHit | **TOLAK** | Event per well kecil dan horizon hanya sepuluh menit, sehingga model kovariat banyak rawan underpowered (D0 bagian 7, R2 bagian 8) | Tidak ada syarat pembuka dalam waktu dekat karena butuh event jauh lebih banyak |
| Boosting dan kalibrasi, termasuk conformal | **PILOT** gelombang kedua | Biaya dan AUPRC LightGBM, XGBoost, CatBoost pada data kita belum terukur (PM-118). Conformal sudah diuji dan gagal gate A: 3 dari 45 fold-run (PM-070, PM-071), dan CUSUM residu 0 dari 9 (PM-072). Tetapi conformal tetap satu-satunya mekanisme yang menyerang portabilitas ambang, jadi penolakannya harus berbasis kegagalan mekanisme, bukan ketiadaan minat | Risiko kegagalan terukur: pada titik operasi anggaran, 12 dari 18 fold-run tidak menyala sama sekali (PM-065), sehingga jaminan FAR dipenuhi dengan cara menghapus alarm |
| Deteksi perubahan CUSUM dan Page-Hinkley | **ADOPSI** hanya sebagai lapisan penstabil dan pemberi lead | Statistik saja bukan alarm yang layak: FP 4361 dengan FAR median 11,0013 dan recall 0,5832 (PM-021, PM-022). Tanpa mekanisme reset, alarm menyala 52,293 sampai 60,000 menit per jam (PM-108). Sebagai gerbang kedua di hybrid, komponen ini yang memberi lead lebih panjang | Wajib dengan reset dan kalibrasi per well atau per alat. Dilarang dipakai sebagai alarm tunggal |
| ADWIN | **PILOT** | Belum dijalankan sama sekali pada data kita, sedangkan kebutuhannya paling ringan untuk tool_wear | Wajib satu run pembanding dengan laju alarm terukur sebelum boleh diusulkan sebagai komponen |
| BOCPD | **TOLAK** (ditunda) | Butuh baseline kontinu yang jauh lebih panjang dari yang tersedia | Dibuka bila baseline kontigu per well memadai |
| Anomali tanpa label: Isolation Forest | **PILOT** untuk triase | Satu-satunya detektor tanpa label yang tidak jenuh pada uji kita, dengan laju alarm baseline median 0,0109 (PM-109) | Hanya untuk triase peringkat; `contamination` adalah parameter masukan, bukan temuan |
| Anomali tanpa label: LOF, autoencoder, one-class SVM | **TOLAK** | LOF dan autoencoder jenuh menyala, sedangkan one-class SVM memberi laju alarm 6,65 kali parameternya (E1 bagian 8.1) | Tidak ada dasar untuk memakai laju alarmnya |
| Uji KS dua sampel | **ADOPSI** sebagai gerbang diagnosis | Sudah dijalankan pada data kita dan menempati skor tertinggi di R5 (4,6), berperan sebagai gerbang sebelum meminjam ambang antar well | Tidak boleh menjadi detektor; perannya memutus keputusan peminjaman ambang |
| Hybrid H1: statistik dan rule pada hyd K-i | **ADOPSI** untuk mode peringatan dini | FP turun dari 2105 ke 935, yaitu 55,58 persen (PM-001, PM-002, PM-003), presisi median naik dari 0,6835 ke 0,7789 (PM-004, PM-005), lead median naik dari 6 menjadi 11,5 menit (PM-008, PM-009), dan fold dengan FAR di bawah 6 naik dari 3 ke 7 dari sembilan (PM-010, PM-011) | Biayanya recall median turun dari 0,7507 ke 0,5638 (PM-006, PM-007), jadi H1 tidak boleh dipakai untuk mode cakupan penuh |
| Hybrid H2: ML dan statistik pada shk K-i | **TOLAK** | FP turun 74,67 persen (PM-027) tetapi TP turun 76,04 persen (PM-028), dengan 46 TP dan recall median 0,0037 (PM-026, PM-031). Memindahkan beban alarm ke alarm yang hilang bukan perbaikan | Tidak ada syarat pembuka sebelum ada titik operasi yang mempertahankan recall |
| Hybrid H3a dan H3b: metaheuristik dan ML pada tool_wear | **TOLAK** | H3a degenerat semua-positif di empat dari empat alat (PM-038, PM-046), H3b hanya unggul di dua alat dan kalah di dua alat lain (PM-039) | Tidak diulang tanpa titik operasi yang mengikat recall |
| Hybrid H4: tiga komponen pada stuck K-ii onset | **PILOT** sebagai verifikasi manual bertarget | Presisi 0,6404 dengan 41 FP dan 17 TP (PM-049, PM-047, PM-048), tetapi recall median 0,001 dan hanya 13 dari 148 onset diperingatkan (PM-050, PM-051, PM-052). FAR median nol di empat dari empat fold (PM-056) adalah akibat recall nol, bukan prestasi | Dilarang dipakai sebagai alarm. Nilai satu-satunya adalah mempersempit jendela yang harus diperiksa manusia |

---

## 3. VONIS PER KELAS DAN PER TUGAS (KOMPOSISI FINAL)

Tier di kolom kanan adalah tier yang berlaku sekarang, diambil dari EVAL_C dan REGISTRY. Tidak ada perubahan
tier di kartu ini. Kolom "kekuatan bukti" menyatakan seberapa jauh vonis didukung angka, bukan seberapa bagus
detektor.

| Mode / klaim | Tugas | Komposisi final | Tier sekarang | Kekuatan bukti | Batas penggunaan |
|---|---|---|---|---|---|
| vib (K tunggal) | deteksi kondisi getaran | rule kanal sebagai peringatan, RF hanya untuk ranking | rule: PERINGATAN-BERPENGAWAS; RF: TREN | SEBAGIAN, dari EVAL_C dan E_RULE, bukan dari uji hybrid di R8 | Ambang global tidak portabel: FAR menyebar 4,1 sampai 496, yaitu 119 kali (PM-099). Hybrid untuk vib belum diuji (PM-104) |
| ssi (K tunggal) | deteksi stick-slip | hybrid rule dan persistence untuk menghemat pemeriksaan, RF untuk ranking | hybrid: PERINGATAN-BERPENGAWAS; RF: TREN | SEBAGIAN, dari EVAL_C | Kanal CRPM absen pada 62,3 persen baris (PM-100), sehingga keterbatasan sensor tidak boleh dibaca sebagai kegagalan model |
| shk (K tunggal) | deteksi anomali sedang berlangsung | rule sebagai peringatan, ML sebagai pemantau tren, tanpa hybrid | rule: PERINGATAN-BERPENGAWAS; ML: TREN | TERUKUR untuk penolakan hybrid (PM-023 sampai PM-031) | AUPRC ML 0,0499 di atas prevalensi 0,0243 (PM-029, PM-030, nilai eksak prevalensi 0,024311), tetapi 21 dari 181 onset diperingatkan oleh H2 (PM-033, PM-032). ML hanya untuk tren |
| stuck K-i | status stuck | rule kanal sebagai peringatan bercakupan terbatas | PERINGATAN-BERPENGAWAS | SEBAGIAN: cakupan hanya dua well di EVAL_C, presisi kondisional menurut E0 K-1 | Tidak boleh diklaim portabel ke well lain sebelum replikasi |
| stuck K-ii | onset | TREN untuk triase risiko, H4 hanya untuk verifikasi manual bertarget | TREN | TERUKUR untuk penolakan alarm (PM-050, PM-052) | Recall semua komponen rendah: ML 0,0322, statistik 0,133, rule 0,0808 (PM-053, PM-054, PM-055) |
| hyd K-i mode peringatan dini | deteksi dini kondisi hidraulik | hybrid statistik dan rule, yaitu H1 | PERINGATAN-BERPENGAWAS | TERUKUR (PM-001 sampai PM-019) | Peringatan bersyarat hanya pada well dengan cakupan di atas 50 persen, yaitu F-10 dengan 0,673 (PM-067), sedangkan F-5 hanya 0,0171 (PM-068) dan hanya satu well memenuhi syarat cakupan (PM-069) |
| hyd K-i mode cakupan penuh | cakupan seluruh onset | rule kanal tunggal | PERINGATAN-BERPENGAWAS | TERUKUR (PM-006, PM-015, PM-017) | Beban alarm tinggi: FAR median 6,932 (PM-012). H1 kehilangan 31,82 persen TP dibanding rule (PM-019) |
| hyd K-ii | prediksi kejadian mendatang | tidak ada, tetap eksplorasi | BELUM LAYAK PAKAI | GAGAL C: satu split temporal, dan 78,7 persen jendela berbalik tanda (PM-110) | Penyebab terukur adalah kanal aliran tidak tersedia, bukan pilihan metode |
| bit_wear K-1 | status keausan bit | persistence sebagai ranking | TREN | TERBATAS: FAR tidak dapat dipakai karena satuannya grid kedalaman | K-2 onset belum dijalankan (PM-121) |
| tool_wear K-i | perubahan regime bengkel | detektor terkalibrasi per alat sebagai peringatan, ML default untuk pemantauan | op_far_calibrated: PERINGATAN-BERPENGAWAS; calib_5of27: TREN | TERUKUR untuk penolakan H3 (PM-037 sampai PM-045) | Presisi biner mendekati peluang: peluang minimal satu alarm kebetulan 4 dari 4 alat adalah 0,5678 (PM-101) dan recall segmen 0,0542 (PM-102), jadi klaim deteksi keausan spesifik dilarang |
| tool_wear K-ii | ranking lintas alat | canary sebagai pembanding stabil | TREN | SEBAGIAN, dari EVAL_C | Empat alat saja, generalisasi tidak boleh diklaim |

Kesimpulan sumbu kelas: **detektor tidak sama antar kelas**. hyd memakai hybrid dua mode, shk memakai rule
ditambah ML terpisah, tool_wear memakai detektor terkalibrasi per alat, stuck K-ii hanya triase, dan hyd K-ii
tetap belum layak pakai. Ini bukan inkonsistensi metodologis, melainkan konsekuensi baseline per tugas.

---

## 4. YANG DIADOPSI: PERUBAHAN KONKRET PADA Detektor DAN DAMPAK TIER

| # | Perubahan konkret | Bukti | Dampak tier |
|---|---|---|---|
| A-1 | hyd K-i dipecah menjadi dua mode pada lapisan keputusan: mode peringatan dini memakai H1, mode cakupan penuh memakai rule kanal | PM-001 sampai PM-019 | **Tidak berubah.** Tetap PERINGATAN-BERPENGAWAS. Naik ke ALARM-OTOMATIS ditolak karena beban manusia belum terukur (PM-111, PM-112) dan cakupan hanya satu well yang memenuhi syarat (PM-069) |
| A-2 | Badge peringatan hyd diberi label bersyarat per well, bukan global | PM-067, PM-068, PM-069 | **Tidak berubah**, tetapi klaim cakupan menyempit ke satu well. Ini penurunan luas klaim, bukan kenaikan tier |
| A-3 | Statistik CUSUM dan Page-Hinkley dipakai hanya sebagai gerbang kedua, wajib dengan reset dan kalibrasi per unit | PM-021, PM-022, PM-108 | **Tidak berubah.** Dilarang menjadi alarm tunggal |
| A-4 | Pelaporan setiap angka FAR dan recall wajib memakai selang dari Monte Carlo, termasuk cakupan waktu | R2 bagian 8 dan 9 | **Tidak berubah.** Menambah kewajiban pelaporan, bukan menaikkan tier |
| A-5 | Uji KS dijadikan gerbang sebelum meminjam ambang antar well | R5 bagian 5 | **Tidak berubah** |
| A-6 | Perbaikan audit yang mengubah bunyi klaim: FAR dilaporkan sebagai laju kalender dengan cakupan, `rule_display` ssi diturunkan dari PERINGATAN-BERPENGAWAS, dan klaim tool_wear memakai recall jendela bukan pernah-menyala | E0 K-3, K-4, S-1; PM-101, PM-102 | **Turun untuk ssi `rule_display`**, karena presisi kondisionalnya tidak layak L1. Tidak ada kenaikan |
| A-7 | Baseline resmi untuk perbandingan hyd dipindah ke definisi bins t-1, dan selisih terhadap angka terbit dilaporkan terbuka | PM-057, PM-058, PM-059, PM-060 | **Tidak berubah.** Angka rule 2105 lawan 2091 selisih 0,67 persen, angka hybrid 927 lawan 927 selisih nol |

Aturan yang mengikat untuk seluruh butir di atas: **adoopsi bukan kenaikan tier**. Syarat naik tier tetap
seperti EVAL_C bagian 4, yaitu C stabil, A dengan FAR di bawah 6 per 24 jam pada titik operasi, dan B berupa
beban pemeriksaan manusia yang dapat diterima. Tidak satu pun dari tiga syarat itu terpenuhi bersamaan oleh
kelas mana pun pada hari ini.

---

## 5. YANG DIPILOT: Detektor SASARAN, KLAIM, GATE, DAN RISIKO KEGAGALAN

Setiap pilot wajib lulus gate yang sama seperti finalis E2: pra-registrasi titik operasi lebih dulu, skor per
jendela disimpan, FAR dilaporkan sebagai laju kalender dengan cakupan, dan uji statistik dijalankan pada
fold yang sama.

### P-1 BGWO untuk seleksi fitur pada vib dan shk

- **Klaim yang diuji**: seleksi fitur menurunkan FP pada titik operasi yang sama tanpa menurunkan recall.
- **Gate**: A, yaitu FAR di bawah 6 per 24 jam dan recall minimal 0,5 pada sedikitnya tujuh dari sembilan fold.
  C, yaitu tanda perbaikan searah pada sedikitnya tujuh dari sembilan well. B belum dapat dinilai karena beban
  pemeriksaan belum terukur (PM-112).
- **Risiko kegagalan**: sembilan unit terlalu sedikit untuk ruang subset, sehingga seleksi bisa menang di well
  tertentu dan kalah di well lain. Pembanding wajib random search dengan jumlah evaluasi identik.
- **Kriteria berhenti**: bila tidak mengalahkan random search pada anggaran sama, hasilnya ditulis sebagai
  temuan negatif dan BGWO tidak dipakai.

### P-2 Boosting terkalibrasi dan conformal pada hyd dan shk

- **Klaim yang diuji**: titik operasi per well yang dipilih prospektif memberi FAR di bawah 6 dengan recall
  minimal 0,5 pada tujuh dari sembilan well, dan cakupan waktu minimal 0,50.
- **Gate**: A dan C. Gate B wajib diukur dengan data jadwal inspeksi, yang sekarang belum ada (PM-112).
- **Risiko kegagalan yang sudah terukur**: pada anggaran alpha, dua belas dari delapan belas fold-run tidak
  menyala sama sekali (PM-065), dan hybrid proxy hanya lulus gate baru di satu dari sembilan fold (PM-066).
  Artinya jaminan FAR mudah dipenuhi dengan menghapus alarm. Pilot harus melaporkan pasangan FAR dan recall
  pada titik operasi yang sama, bukan salah satunya.
- **Kriteria berhenti**: bila titik operasi yang memenuhi FAR menghasilkan nol alarm pada baseline, kesimpulannya
  ambang tunggal tidak dapat melayani sembilan well, dan itu dilaporkan sebagai temuan, bukan kegagalan alat.

### P-3 Cox proportional hazards pada stuck K-ii

- **Klaim yang diuji**: lead time dengan data tersensor lebih jujur daripada TLead yang sekarang.
- **Gate**: B, yaitu lead median harus melampaui anchor, dan A, yaitu laju alarm di luar baseline tetap terkendali.
- **Risiko kegagalan**: event berulang melanggar asumsi proportional hazards, dan jumlah event per well kecil.
- **Kriteria berhenti**: bila asumsi proportional hazards ditolak dan tidak ada stratifikasi yang memperbaiki,
  klaim lead time tidak boleh dibuat.

### P-4 Matrix profile pada vib

- **Klaim yang diuji**: waktu pencarian episode serupa oleh manusia turun, tanpa klaim deteksi.
- **Gate**: hanya B, karena perannya penunjuk potongan waktu. Gate A tidak berlaku untuk alat bantu pencarian.
- **Risiko kegagalan**: butuh deret rapat, sedangkan sebagian kanal punya celah panjang.
- **Kriteria berhenti**: bila tidak ada pengurangan waktu pencarian yang terukur, alat tidak dipakai.

### P-5 ADWIN pada tool_wear

- **Klaim yang diuji**: deteksi perubahan regime tanpa baseline panjang, dengan laju alarm terjaga.
- **Gate**: A, yaitu FP per alat tetap dalam rentang terkalibrasi, dan B berupa beban pemeriksaan per shift.
- **Risiko kegagalan**: hanya empat alat, sehingga tidak ada daya statistik untuk klaim lintas alat.
- **Kriteria berhenti**: bila laju alarm tidak dapat dikalibrasi tanpa data baseline bersih, pilot ditutup
  dan ADWIN tetap belum terukur.

### P-6 Isolation Forest untuk triase pada kelas tanpa label yang layak

- **Klaim yang diuji**: peringkat anomali mempersempit wilayah pemeriksaan pada kelas yang belum punya label.
- **Gate**: hanya triase, yaitu presisi peringkat dan laju alarm baseline. Tidak boleh mengklaim deteksi.
- **Risiko kegagalan**: parameter `contamination` adalah masukan, sehingga hasil mudah tampak baik secara semu.
- **Kriteria berhenti**: bila detektor jenuh seperti LOF dan autoencoder, pilot ditutup.

---

## 6. YANG DITOLAK DAN SYARAT MEMBUKANYA

| Yang ditolak | Alasan utama | Syarat pembuka |
|---|---|---|
| VMD, EMD, wavelet | Laju sampel tidak mencukupi, Nyquist 0,1667 Hz (PM-103, PM-104) | Kanal dengan laju minimal orde Hz |
| kNN-DTW | Biaya 134,01 sampai 137.374,35 jam per klasifikasi (PM-107) | Tidak ada dalam rencana; biaya harus turun beberapa orde |
| Metaheuristik untuk tuning | Tidak ada bukti kenaikan metrik, dan uji GWO pada tool_wear tidak menambah nilai (PM-037 sampai PM-043) | Bukti pembanding anggaran sama yang menunjukkan kenaikan pada fold yang sama |
| H2 pada shk | Memotong TP 76,04 persen (PM-028) | Titik operasi yang mempertahankan recall |
| H3a dan H3b pada tool_wear | Degenerat atau tandanya berubah antar alat (PM-038, PM-039) | Tidak ada dalam rencana sebelum ada titik operasi yang mengikat recall |
| Markov, HMM, Bayesian network, MCMC | Prasyarat data tidak ada (D0 bagian 7) | Label state fisik dan uji orde Markov |
| RSF dan DeepHit | Event per well kecil, horizon pendek | Jumlah event jauh lebih banyak |
| LOF, autoencoder, one-class SVM | Jenuh atau laju alarm tidak terkendali (PM-109 sebagai pembanding Isolation Forest) | Tidak ada dalam rencana |
| BOCPD | Butuh baseline kontinu panjang | Baseline kontigu per well memadai |
| Angka TLead `persistence_event` versi lama | Audit E0 K-2 menemukan kredit lead ke onset yang salah | Perhitungan ulang dengan aturan pemicu sama dengan event |
| Klaim presisi 0,50 tool_wear sebagai bukti keausan | Peluang kebetulan 4 dari 4 alat 0,5678 (PM-101) | Presisi yang jauh di atas peluang pada alat baru |

---

## 7. ROADMAP TIGA GELOMBANG

### Gelombang 1: sekarang, tanpa data baru

Isi gelombang ini adalah hal yang sudah terukur dan bisa langsung dipakai tanpa menaikkan tier.

1. Terapkan komposisi hyd dua mode (A-1) dan label peringatan bersyarat per well (A-2).
2. Tetapkan aturan bahwa statistik hanya menjadi gerbang kedua dengan reset dan kalibrasi (A-3).
3. Wajibkan selang Monte Carlo pada setiap angka FAR dan recall, termasuk cakupan waktu (A-4).
4. Jadikan uji KS gerbang sebelum meminjam ambang antar well (A-5).
5. Jalankan perbaikan bunyi klaim: FAR kalender dengan cakupan, penurunan tier `rule_display` ssi, dan
   recall jendela untuk tool_wear (A-6).
6. Bekukan baseline resmi pada definisi bins t-1 dan laporkan selisih terhadap angka terbit (A-7).
7. Larang seluruh kenaikan tier dan pertahankan slot `ALARM-OTOMATIS` nol (PM-078).

Keluaran gelombang 1 dapat diverifikasi tanpa data baru, karena seluruh angka pendukungnya sudah ada di
berkas JSON hari ini.

### Gelombang 2: setelah data tambahan

Data yang dibutuhkan, semuanya belum ada hari ini:

- Stempel waktu per jendela pada tool_wear, supaya lapisan B dapat diukur (PM-113).
- Data jadwal inspeksi dan beban pemeriksaan per shift, supaya beban manusia terukur (PM-112).
- Data biaya atau jam henti per kejadian, supaya nilai maintenance terukur dalam satuan uang (PM-111).
- Jumlah well, alat, dan kampanye yang cukup untuk kestabilan lintas seed dan lintas kampanye (PM-114, PM-115).

Pilot yang dijalankan pada gelombang ini: P-1 BGWO, P-2 boosting dan conformal, P-3 Cox, P-5 ADWIN, dan
P-6 Isolation Forest untuk triase. Kalibrasi ambang per well prospektif juga masuk gelombang ini, karena
belum pernah dijalankan (PM-119).

### Gelombang 3: menunggu akuisisi data yang tidak ada

| Kebutuhan data | Yang menunggu |
|---|---|
| Kanal dengan laju minimal orde Hz | dekomposisi VMD, EMD, dan wavelet (PM-103, PM-104) |
| Label state fisik dan uji orde Markov | Markov chain, HMM, Bayesian network |
| Kanal aliran keluaran dan split temporal berlapis | hyd K-ii yang sekarang belum layak pakai (PM-110) |
| Pra-registrasi label dan satuan kedalaman yang benar | bit_wear K-2 onset (PM-121, PM-120) |
| Deret rapat tanpa celah panjang | matrix profile (P-4) |
| Event lebih banyak dan horizon berlapis | RSF dan DeepHit |

Aturan lintas gelombang: hasil gelombang 2 tidak boleh menaikkan tier sebelum gate C, A, dan B terpenuhi
bersamaan, dan hasil negatif wajib ditulis sebagai temuan, bukan disimpan.

---

## 8. YANG BELUM TERUKUR DAN TIDAK BOLEH DIKLAIM

Daftar ini bagian dari hasil, bukan lampiran.

1. **Nilai maintenance dalam rupiah atau jam henti terhindar**: belum terukur, tidak ada data biaya (PM-111).
2. **Pengurangan pemeriksaan fisik per shift**: belum terukur, tidak ada data jadwal inspeksi (PM-112).
3. **Lapisan B untuk tool_wear**: belum terukur karena label hanya urutan jendela (PM-113).
4. **Kestabilan lintas seed**: R8 memakai satu seed, jadi klaim kestabilan tidak boleh dibuat (PM-114).
5. **Kestabilan lintas kampanye**: tanggal kampanye tidak tersedia per baris (PM-115).
6. **Hybrid untuk vib, ssi, dan bit_wear**: tidak diuji, sehingga klaim hybrid untuk tiga kelas itu dilarang (PM-116).
7. **Seleksi fitur BGWO**: belum ada satu run pun (PM-117).
8. **Biaya latih LightGBM, XGBoost, CatBoost pada data kita**: belum terukur karena run pembanding tidak
   selesai dalam anggaran (PM-118).
9. **Kalibrasi ambang per well prospektif**: belum pernah dijalankan, hanya usul (PM-119).
10. **FAR bit_wear dalam satuan waktu**: tidak sah karena barisnya grid kedalaman (PM-120).
11. **Generalisasi lintas alat dan lintas domain rig ke bengkel atau sebaliknya**: tidak diuji, dilarang diklaim.
12. **Prediksi kegagalan hidraulik independen dari label SPPA**: label hyd dibentuk dari statistik yang sama,
    sehingga kenaikan presisi sebagian adalah kecocokan dengan definisi label, bukan bukti prediksi independen.

Selain itu, tiga kalimat berikut dilarang muncul di dokumen lain tanpa angka pendukung baru:

- "detektor X lebih baik" tanpa baseline tugas itu dan angkanya.
- "alarm otomatis siap" untuk kelas mana pun, karena syarat EVAL_C bagian 4 belum terpenuhi.
- "siap produksi" atau "siap dipakai di rig", karena seluruh bukti berasal dari data arsip dan satu domain.

---

## 9. RUJUKAN DAN STATUS VERIFIKASI

Semua DOI diuji dua lapis pada 2026-10-27 dengan `code/rnd_pm_doi.py`: lapis registrasi memakai HEAD ke
`https://doi.org/<doi>` tanpa mengikuti redirect, lapis metadata memakai Crossref atau DataCite. Sepuluh dari
sepuluh terdaftar (status 302) dan sepuluh dari sepuluh memberi metadata 200 dengan judul yang cocok.
Baris ledger PM-079 sampai PM-098.

| # | Penulis pertama | Tahun | Judul | DOI | Lapis 1 | Lapis 2 |
|---|---|---|---|---|---|---|
| 1 | Page, E. S. | 1954 | Continuous inspection schemes | 10.1093/biomet/41.1-2.100 | 302 | 200 Crossref |
| 2 | Vovk, V. | 2005 | Algorithmic Learning in a Random World | 10.1007/b106715 | 302 | 200 Crossref (nama penulis pertama kosong pada record, dicocokkan lewat judul dan tahun) |
| 3 | Mirjalili, S. | 2014 | Grey Wolf Optimizer | 10.1016/j.advengsoft.2013.12.007 | 302 | 200 Crossref |
| 4 | Dragomiretskiy, K. | 2014 | Variational Mode Decomposition | 10.1109/TSP.2013.2288675 | 302 | 200 Crossref |
| 5 | Liu, F. T. | 2008 | Isolation Forest | 10.1109/ICDM.2008.17 | 302 | 200 Crossref |
| 6 | Tatbul, N. | 2018 | Precision and Recall for Time Series | 10.48550/arXiv.1803.03639 | 302 | 200 DataCite |
| 7 | Rabiner, L. R. | 1989 | A tutorial on hidden Markov models | 10.1109/5.18626 | 302 | 200 Crossref |
| 8 | Cox, D. R. | 1972 | Regression Models and Life-Tables | 10.1111/j.2517-6161.1972.tb00899.x | 302 | 200 Crossref |
| 9 | Ishwaran, H. | 2008 | Random survival forests | 10.1214/08-AOAS169 | 302 | 200 Crossref |
| 10 | Chandola, V. | 2009 | Anomaly detection: A survey | 10.1145/1541880.1541882 | 302 | 200 Crossref |

Tidak ada rekomendasi di dokumen ini yang bersandar pada rujukan berstatus belum terverifikasi. Teks penuh
rujukan tidak dibaca pada kartu ini, sehingga klaim tentang isi metode bersandar pada judul dan metadata,
bukan pada pembacaan penuh. Batas ini berlaku untuk seluruh sepuluh rujukan.

---

## 10. PROVENANCE

Seluruh angka di dokumen ini punya baris di `docs/RND_PROVENANCE_LEDGER.md` Bagian PM, 121 baris
(PM-001 sampai PM-121), tujuh kolom: nomor, angka, satuan, kelas sumber, rujukan persis, dipakai di, status.
Komposisi kelas: RUN-KITA 80 baris, JURNAL 20 baris, DERIVASI 9 baris, KONVENSI 1 baris, BELUM-TERUKUR
11 baris. Dua belas baris RUN-KITA berstatus kutipan, yaitu angka yang sudah di-assert di bagian R1, R3, R4,
R5, atau E0 dan tidak dihitung ulang di kartu ini.

Skrip `code/rnd_pm_ledger.py` menolak menulis bila assert terhadap JSON mentah gagal, dan idempoten: dua kali
dijalankan menghasilkan 121 baris dan satu bagian PM.

Pemeriksa `code/rnd_pm_doccheck.py` menguji 29 hal pada dokumen dan ledger, termasuk bahwa setiap baris ledger
tercakup sitasi tunggal atau rentang, bahwa klaim jumlah baris dan komposisi kelas cocok dengan hitungan nyata,
dan bahwa tidak ada sel kosong pada baris tujuh kolom.

---

## 11. RINGKASAN LIMA BARIS

1. Dari empat uji hybrid, hanya satu yang menambah nilai terukur, yaitu H1 pada hyd K-i dengan FP turun 55,58 persen, presisi naik ke 0,7789, dan lead naik ke 11,5 menit (PM-003, PM-005, PM-009).
2. Tidak ada kenaikan tier di kartu ini: slot ALARM-OTOMATIS tetap nol, dan yang mengikat gate hyd bukan mutu deteksi melainkan cakupan, karena hanya satu well yang mencapai cakupan di atas 50 persen (PM-069, PM-078).
3. Metaheuristik ditolak untuk peran tuning dan untuk pembungkusan ML karena uji GWO pada tool_wear degenerat atau berubah tanda, tetapi BGWO untuk seleksi fitur tetap PILOT karena belum pernah dijalankan (PM-038, PM-039, PM-105).
4. Lima keluarga masuk ADOPSI tanpa kenaikan tier: komposisi hyd dua mode, statistik sebagai gerbang kedua, Monte Carlo untuk selang, uji KS sebagai gerbang ambang, dan perbaikan bunyi klaim dari audit E0.
5. Roadmap tiga gelombang dipisahkan oleh kebutuhan data: gelombang sekarang tanpa data baru, gelombang kedua setelah data jadwal inspeksi dan biaya, gelombang ketiga menunggu laju sampel tinggi dan label state fisik.

---

## 12. DAFTAR YANG BELUM TERVERIFIKASI

1. Teks penuh sepuluh rujukan tidak dibaca; yang terverifikasi adalah registrasi DOI dan metadata judul,
   penulis pertama, serta tahun.
2. Nama penulis pertama untuk Vovk 2005 kosong pada record Crossref, sehingga identitas dicocokkan lewat
   judul dan tahun, bukan lewat nama.
3. Angka R8 berasal dari satu seed dan satu kali eksekusi per tugas; kestabilan lintas seed belum terukur.
4. Angka hyd memakai satu well kalibrasi di dalam data latih, sehingga recall yang dilaporkan adalah batas
   bawah untuk desain delapan well, bukan angka final.
5. Label hyd dibentuk dari statistik SPPA dan aliran, sehingga kecocokan dengan label bukan bukti prediksi
   kegagalan independen.
6. Angka FAR seluruh dokumen memakai konvensi kampanye dari V9; perubahan konvensi akan mengubah angka.
7. Lapisan B di seluruh kelas belum terukur karena data beban pemeriksaan tidak ada.
8. Tidak ada angka biaya, jam henti, atau nilai produksi yang dipakai di dokumen ini karena tidak tersedia.
9. Penilaian skor prioritas R1, R2, R3, R5 dan EVAL_C sebagian adalah KONVENSI internal, bukan pengukuran.
10. Hybrid untuk vib, ssi, dan bit_wear belum dijalankan, sehingga vonis untuk tiga kelas itu bersandar pada
    EVAL_C dan E_RULE, bukan pada uji hybrid.
