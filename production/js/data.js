/* ============================================================================
   production/js/data.js: W2 data dan provenance
   Aturan berkas ini: setiap angka wajib punya sumber file:baris.
   Angka tanpa sumber ditandai "BELUM KUTIP" dan tidak ditampilkan sebagai fakta.
   Tidak ada angka baru di berkas ini. Yang ada hanya angka yang bisa dilacak.
   ============================================================================ */

/* ----------------------------------------------------------------------------
   PROVENANCE: meta
   Sumber: planning/06_SWARM_KONSENSUS.md:38 (tujuh engine, 27 kepala),
   planning/04_ANTREAN_TINJAUAN.md:33 ([J] baris 1414: auto_critical_alarm_slots = 0),
   planning/04_ANTREAN_TINJAUAN.md:3 (11 klaim).
   cut "2026-10-29": tanggal potong data, sama dengan tanggal provenance di
   docs/RND_PROVENANCE_LEDGER.md baris 3430.
   -------------------------------------------------------------------------- */
window.DATA = {
  meta: {
    cut: "2026-10-29",
    cutLabel: "29 Oktober 2026",
    version: "v1.1",
    heads: 27,
    engines: 7,
    claims: 11,
    alarmSlots: 0
  },

  /* --------------------------------------------------------------------------
     PROVENANCE: tk
     Sumber: planning/06_SWARM_KONSENSUS.md bagian 5.2 (kuorum 4 dari 7, engine
     bersuara 6 dari 7, cakupan bobot 9,15/9,15 = 1,00) dan bagian 5.3
     (batas dominasi 0,35, S = 18,23 persen setelah potong).
     Sebelumnya berkas ini menulis cakupan 0,87. Angka itu tidak ada di sumber
     mana pun; yang benar 1,00.
     ------------------------------------------------------------------------ */
  tk: {
    level: "TK-2",
    label: "PANTAU",
    support: 18.23,
    quorum: "6/7",
    coverage: 1.00,
    cap: 0.35,
    note: "Dewan rig bersuara 6 dari 7. Dukungan berbobot 18,23 persen. Tidak ada tindakan otomatis."
  },

  /* --------------------------------------------------------------------------
     PROVENANCE: focus
     Sumber: planning/04_ANTREAN_TINJAUAN.md bagian 6.2, baris 1 (hyd K-i),
     baris 2 (vib), baris 3 (shk). Kolom yang dipakai: K_tampil, pita, kepala
     nyala, jendela, alasan (lead).
     - hyd 0,6100 P4 3 kepala 20 jendela lead 8,0 menit (04 baris 411)
     - vib 0,4950 P3 3 kepala 429 jendela tanpa lead (04 baris 412)
     - shk 0,5188 P3 3 kepala 20 jendela tanpa lead (04 baris 413)
     Umur jendela tidak ada di 04, jadi diisi placeholder kosong, bukan angka karangan.
     Sinyal vib: AUPRC 0,4806 sampai 0,8481 per sumur
     (docs/RND_PROVENANCE_LEDGER.md S2-018, S2-025, S2-032, S2-039).
     Angka lama 0,6204 tidak ada di ledger maupun di planning.
     ------------------------------------------------------------------------ */
  focus: [
    {
      code: "hyd_ki",
      claim: "Kebocoran tekanan hidraulik",
      well: "F-14",
      window: "20 jendela",
      heads: 3,
      confidence: 0.6100,
      cap: 0.61,
      pita: 4,
      far: "FAR 4,0984",
      lead: "8,0 menit",
      age: "—",
      status: "Baru",
      action: "Konfirmasi lapangan sebelum shift berikutnya."
    },
    {
      code: "vib",
      claim: "Getaran di atas ambang kelas",
      well: "F-14",
      window: "429 jendela",
      heads: 3,
      confidence: 0.4950,
      cap: 0.495,
      pita: 3,
      far: "AUPRC 0,4806 sampai 0,8481",
      lead: "tidak ada",
      age: "—",
      status: "Baru",
      action: "Periksa kanal dan bandingkan dengan baseline 30 hari."
    },
    {
      code: "shk_ki",
      claim: "Beban kejut pada rangkaian",
      well: "F-14",
      window: "20 jendela",
      heads: 3,
      confidence: 0.5188,
      cap: 0.5188,
      pita: 3,
      far: "FAR 6,618",
      lead: "tidak ada",
      age: "—",
      status: "Baru",
      action: "Periksa kanal dan catat lonjakan di atas ambang."
    }
  ],

  /* --------------------------------------------------------------------------
     PROVENANCE: damages (11 kelas)
     Kolom k dan pita: planning/04_ANTREAN_TINJAUAN.md bagian 6.2 dan 6.3
     (K_tampil, bukan K_seg dari 06). Untuk dua kelas yang tidak punya baris di
     04 (tool_wear K-ii dan hyd K-ii) dipakai K_tampil 06 bagian 2.3 dan 5.3.
     Kolom vote dan weight: planning/06_SWARM_KONSENSUS.md bagian 2.3
     (keluaran "ringkasan per klaim", baris 221 sampai 229).
     Kolom cap: planning/06_SWARM_KONSENSUS.md bagian 5.3, baris 437 sampai 444.
     Kolom evidence dan limit: berkas yang disebut di dalam teks tiap butir.
     Angka yang tidak bisa dilacak sudah dibuang, bukan dipertahankan.
     ------------------------------------------------------------------------ */
  damages: [
    {
      code: "hyd_ki",
      name: "Hidraulik K-i",
      task: "Peringatan dini kebocoran tekanan",
      pita: 4,
      cap: "0,6100",
      k: "0,6100",
      vote: "V-2 Tolak",
      weight: "3,30",
      evidence: "H1p: FP 927, TP 4.924, presisi 0,8243, recall 0,6519, FAR kalender 4,0984, 7 dari 9 fold (RND_S6_PM_WAVE2.md:150).",
      limit: "Lead 8,0 menit, 218 dari 390 onset, 2,3769 alarm per onset (RND_S6_PM_WAVE2.md:150)."
    },
    {
      code: "vib",
      name: "Getaran",
      task: "Peringatan getaran dan pemeringkatan",
      pita: 3,
      cap: "0,4950",
      k: "0,4950",
      vote: "V-1 Dukung lemah",
      weight: "1,65",
      evidence: "RF AUPRC 0,4806 sampai 0,8481 pada 4 sumur (ledger S2-018, S2-025, S2-032, S2-039). 5.429 baris positif (S2-012).",
      limit: "Batas kelas 0,4950 menahan pita di P3, bukan P2 (04 bagian 6.2 baris 2). Hybrid statistik ditolak: 0 dari 4 fold mencapai recall 0,5 (06, konflik H-4)."
    },
    {
      code: "shk_ki",
      name: "Beban kejut",
      task: "Peringatan dan pemantauan tren",
      pita: 3,
      cap: "0,5188",
      k: "0,5188",
      vote: "V-2 Tolak",
      weight: "1,40",
      evidence: "ML saja: FP 2.633, TP 192, AUPRC 0,0499 lawan prevalensi 0,0243, 64 dari 181 onset (RND_S6_PM_WAVE2.md:110).",
      limit: "H2 memotong TP 76,04 persen dan menyisakan recall 0,0037 (RND_S6_PM_WAVE2.md:110)."
    },
    {
      code: "stuck_ki",
      name: "Pipa terjepit K-i",
      task: "Triase dan peringatan",
      pita: 3,
      cap: "0,4562",
      k: "0,4562",
      vote: "V-2 Tolak",
      weight: "1,40",
      evidence: "Tiga kepala menyala, K_min 1,0000, terpotong batas kelas stuck 0,4562 (04 bagian 6.2 baris 4).",
      limit: "Cakupan 2 sumur. Label per kejadian belum tersedia untuk setiap jendela (04 bagian 6.2 baris 4)."
    },
    {
      code: "stuck_kii",
      name: "Pipa terjepit K-ii",
      task: "Pemantauan tren",
      pita: 2,
      cap: "0,4562",
      k: "0,3333",
      vote: "V-2 Tolak",
      weight: "0,75",
      evidence: "Hanya kepala kejadian menyala: K_min 0,3333, K_up 1,0000 pada jendela 30.122 (04 bagian 6.2 baris 6).",
      limit: "Tanpa komposisi final, verifikasi manual bertarget: H4 FP 41, presisi 0,6404, recall 0,001 (RND_S6_PM_WAVE2.md:154)."
    },
    {
      code: "bit_wear_k1",
      name: "Keausan bit K-1",
      task: "Pemeringkatan onset blok high_MSE",
      pita: 2,
      cap: "0,2525",
      k: "0,2525",
      vote: "V-2 Tolak",
      weight: "0,25",
      evidence: "Kepala tunggal persistence 0,25 dari 0,25, K_min 1,0000, ditekan batas kelas 0,2525 (04 bagian 6.3 baris 9).",
      limit: "Label adalah indeks mekanika, bukan observasi keausan. Tidak dapat menyumbang di atas P2 berapa pun skornya (06 bagian 5.3)."
    },
    {
      code: "bit_wear_k2",
      name: "Keausan bit K-2",
      task: "Prediksi onset",
      pita: 0,
      cap: "0,2525",
      k: "tidak ada",
      vote: "V-3 Abstain AB-1",
      weight: "0,00",
      evidence: "Pra-registrasi belum terbit. Tier BELUM LAYAK PAKAI (06 bagian 4.4).",
      limit: "Tidak ada angka. Tidak boleh tampil sebagai hasil."
    },
    {
      code: "tool_wear_ki",
      name: "Keausan alat K-i",
      task: "Deteksi perubahan regime di bengkel",
      pita: 3,
      cap: "0,4550",
      k: "0,4550",
      vote: "V-2 Tolak",
      weight: "1,25",
      evidence: "Presisi run 0,50, FP 1 sampai 3 per alat, empat alat saja (RND_S6_PM_WAVE2.md:155).",
      limit: "FAR diukur per menit, bukan per 24 jam. Jangan dibandingkan langsung (04 bagian 2.3)."
    },
    {
      code: "tool_wear_kii",
      name: "Keausan alat K-ii",
      task: "Pemeringkatan lintas alat",
      pita: 3,
      cap: "0,4550",
      k: "0,4550",
      vote: "V-1 Dukung",
      weight: "0,25",
      evidence: "K_seg 0,6013 dipotong batas kelas 0,4550 menjadi K_tampil 0,4550 P3 (06 bagian 2.3, baris 221).",
      limit: "Empat alat saja. Peluang minimal satu alarm kebetulan di 4 dari 4 alat adalah 0,5678 (RND_S6_PM_WAVE2.md:155)."
    },
    {
      code: "hyd_kii",
      name: "Hidraulik K-ii",
      task: "Eksplorasi, belum layak pakai",
      pita: 0,
      cap: "0,5125",
      k: "tidak ada",
      vote: "V-3 Abstain AB-1",
      weight: "0,00",
      evidence: "Satu split temporal, 78,7 persen jendela berbalik tanda (RND_PM_VERDICT.md:131, PM-110). Kanal aliran tidak tersedia.",
      limit: "GAGAL C. Tidak ada komposisi. Batas kelas hyd K-ii 0,5125 (06 bagian 2.3)."
    },
    {
      code: "ssi",
      name: "Intensitas getaran permukaan",
      task: "Pemeringkatan, bukan peringatan",
      pita: 2,
      cap: "0,5263",
      k: "0,2623",
      vote: "V-2 Tolak, sebagian bisu",
      weight: "0,40",
      evidence: "H1p hanya 1 TP dan 17 FP dari 132 onset, recall 0,0 (RND_S6_PM_WAVE2.md:114). Kanal CRPM absen 62,3 persen (01_KATALOG_FITUR.md:1634).",
      limit: "12,1 alarm palsu per alarm benar (ledger S2-448). Status AB-2: 5.268 dari 5.455 jendela tanpa data (04 bagian 6.3 baris 10)."
    }
  ],

  /* --------------------------------------------------------------------------
     PROVENANCE: queue (10 baris)
     Sumber tunggal: planning/04_ANTREAN_TINJAUAN.md bagian 6.2, baris 411
     sampai 420. Sepuluh baris, bukan dua belas.
     Semua baris memakai well "F-14" karena 04 bagian 9 (baris 1248) menyatakan
     peta sumur per jendela belum ada dan seluruh baris 6.2 berasal dari segmen
     F-14. Nama sumur per baris tidak tersedia, jadi tidak dikarang.
     age placeholder kosong: 04 tidak punya kolom umur jendela.
     minutes: 6,4,4,4,4,2,2,2,2,0 sesuai kolom Menit di 04.
     status awal: sembilan baris "Baru" karena belum ada yang ditinjau; baris
     ssi "Ditutup" karena aksinya di 04 adalah "tutup".
     ------------------------------------------------------------------------ */
  queue: [
    { id: "Q-1041", code: "hyd_ki", claim: "Hidraulik K-i", well: "F-14", window: "20 jendela", heads: 3, conf: 0.6100, pita: 4, age: "—", minutes: 6, signal: "K 0,6100", lead: "8,0 mnt", status: "Baru", note: "Tiga kepala setara menyala, terpotong batas kelas hyd 0,6100. Lead 8,0 menit." },
    { id: "Q-1042", code: "vib", claim: "Getaran", well: "F-14", window: "429 jendela", heads: 3, conf: 0.4950, pita: 3, age: "—", minutes: 4, signal: "K 0,4950", lead: "tidak ada", status: "Baru", note: "Tiga kepala menyala, RF pasti mati, terpotong batas kelas vib 0,4950. Tidak ada lead." },
    { id: "Q-1043", code: "shk_ki", claim: "Beban kejut", well: "F-14", window: "20 jendela", heads: 3, conf: 0.5188, pita: 3, age: "—", minutes: 4, signal: "FAR 6,618", lead: "tidak ada", status: "Baru", note: "Tiga kepala menyala, terpotong batas kelas shk 0,5188. FAR 6,618 per 24 jam." },
    { id: "Q-1044", code: "stuck_ki", claim: "Pipa terjepit K-i", well: "F-14", window: "8 jendela", heads: 3, conf: 0.4562, pita: 3, age: "—", minutes: 4, signal: "K 0,4562", lead: "tidak ada", status: "Baru", note: "Tiga kepala menyala, terpotong batas kelas stuck 0,4562. Cakupan 2 sumur." },
    { id: "Q-1045", code: "tool_wear_ki", claim: "Keausan alat K-i", well: "F-14", window: "42 jendela", heads: 1, conf: 0.4550, pita: 3, age: "—", minutes: 4, signal: "K 0,4550", lead: "tidak ada", status: "Baru", note: "Satu kepala peringatan menyala, calib belum pasti, satuan FAR per menit." },
    { id: "Q-1046", code: "stuck_kii", claim: "Pipa terjepit K-ii", well: "F-14", window: "30.122 jendela", heads: 1, conf: 0.3333, pita: 2, age: "—", minutes: 2, signal: "K 0,3333", lead: "tidak ada", status: "Baru", note: "Hanya kepala kejadian menyala, e1 dan RF belum pasti. Tidak ada lead." },
    { id: "Q-1047", code: "stuck_kii", claim: "Pipa terjepit K-ii", well: "F-14", window: "17.582 jendela", heads: 1, conf: 0.3333, pita: 2, age: "—", minutes: 2, signal: "K 0,3333", lead: "tidak ada", status: "Baru", note: "Hanya kepala RF menyala, e1 belum pasti, ranking saja." },
    { id: "Q-1048", code: "hyd_ki", claim: "Hidraulik K-i", well: "F-14", window: "0 jendela", heads: 1, conf: 0.3030, pita: 2, age: "—", minutes: 2, signal: "K 0,3030", lead: "tidak ada", status: "Baru", note: "Satu kepala menyala, persistence dan hibrida pasti mati karena aktivasi pertama di 20." },
    { id: "Q-1049", code: "bit_wear_k1", claim: "Keausan bit K-1", well: "F-14", window: "29.120 jendela", heads: 1, conf: 0.2525, pita: 2, age: "—", minutes: 2, signal: "K 0,2525", lead: "tidak ada", status: "Baru", note: "Kepala tunggal menyala penuh, batas kelas bit_wear 0,2525 menekan." },
    { id: "Q-1050", code: "ssi", claim: "Intensitas getaran", well: "F-14", window: "118 jendela", heads: 1, conf: 0.2623, pita: 2, age: "—", minutes: 0, signal: "AB-2", lead: "tidak ada", status: "Ditutup", note: "Kanal absen 5.268 dari 5.455 jendela, status AB-2, keluar dari antrean." }
  ],

  /* --------------------------------------------------------------------------
     PROVENANCE: hydModes
     Sumber: planning/04_ANTREAN_TINJAUAN.md bagian 2.1, baris 73 sampai 76.
     Kolom FP, TP, presisi, recall, FAR kalender median, lead median, lalu dua
     kolom fold. Nilai TP rule kanal sebelumnya 3.804; yang benar 5.579.
     folds ditulis sebagai "<fold FAR> FAR · <fold recall> recall" supaya dua
     kolom fold di 04 tidak tertukar.
     ------------------------------------------------------------------------ */
  hydModes: [
    { name: "Rule kanal", fp: 2105, tp: 5579, p: 0.6835, r: 0.7507, far: 6.9320, lead: 6.0, folds: "3 FAR · 9 recall", note: "Cakupan penuh. Beban alarm tertinggi, 5,3974 alarm per onset." },
    { name: "H1 statistik", fp: 935, tp: 3804, p: 0.7789, r: 0.5638, far: 3.5302, lead: 11.5, folds: "7 FAR · 6 recall", note: "Rule DAN CUSUM residu. Lead 11,5 menit." },
    { name: "H1p rule + persistence", fp: 927, tp: 4924, p: 0.8243, r: 0.6519, far: 4.0984, lead: 8.0, folds: "7 FAR · 9 recall", note: "Komposisi terpilih untuk peringatan dini." },
    { name: "H1p3 + statistik", fp: 568, tp: 3557, p: 0.8646, r: 0.5296, far: 2.0323, lead: 12.5, folds: "9 FAR · 5 recall", note: "Mode alarm rendah. Recall 0,5296 hanya sedikit di atas batas 0,5." }
  ],

  /* --------------------------------------------------------------------------
     PROVENANCE: load
     Sumber: planning/04_ANTREAN_TINJAUAN.md bagian 2.4, baris 138 sampai 143.
     Lambda, p50, dan p95 per klaim. Jumlah empat lambda teratas 40,15 baris per
     shift (04 baris 146); p95 gabungan 61 baris (04 baris 147).
     Nilai p50 dan p95 sebelumnya 12,4 dan 38,7; keduanya tidak ada di 04.
     Anggaran 30 menit per shift (04 bagian 5.2 dan 6.4).
     ------------------------------------------------------------------------ */
  load: [
    { name: "vib", value: 16.647, p50: 16, p95: 24, budget: 30, note: "Rule display setelah deduplikasi. Beban vib yang benar 17, bukan 34." },
    { name: "hyd rule", value: 18.523, p50: 18, p95: 26, budget: 30, note: "Beban tertinggi. Cakupan penuh." },
    { name: "hyd hibrida", value: 5.537, p50: 5, p95: 10, budget: 30, note: "H1p menurunkan beban, menaikkan presisi." },
    { name: "shk", value: 2.206, p50: 2, p95: 5, budget: 30, note: "Hanya pemantauan tren." },
    { name: "stuck", value: 2.774, p50: 3, p95: 6, budget: 30, note: "Triase, bukan alarm otomatis." }
  ],

  /* --------------------------------------------------------------------------
     PROVENANCE: pareto
     Sumber jam: docs/RND_ENGINE_S6_INTEGRATION.md:24 sampai 26 dan
     planning/DESIGN.md:360. Penyebut 39.397,986 jam dari
     docs/RND_S4_LAYER_B_DATA.md:63.
     pct adalah pangsa kumulatif, bukan pangsa tunggal:
     2.739,667/39.397,986 = 6,95; +2.680,917 = 13,75; +1.925,5 = 18,64;
     +212,0 = 19,18; +195,0 = 19,67.
     ------------------------------------------------------------------------ */
  pareto: [
    { name: "Equipment failure", hours: 2739.667, pct: 6.95 },
    { name: "Interruption other", hours: 2680.917, pct: 13.75 },
    { name: "Waiting on weather", hours: 1925.5, pct: 18.64 },
    { name: "Stuck equipment", hours: 212.0, pct: 19.18 },
    { name: "Circulation loss", hours: 195.0, pct: 19.67 }
  ],

  /* --------------------------------------------------------------------------
     PROVENANCE: wells dan channels
     Satu kolom saja, F-14, karena seluruh baris 04 bagian 6.2 berasal dari
     segmen itu (04 baris 1248) dan hanya F-14 yang punya ukuran kanal per sumur
     di repo ini.
     Angka terukur:
     - VIB: VIBLAT 356 dari 1.989 baris kosong di F-14, yaitu 17,9 persen,
       di bawah ambang 20 persen, jadi "siap" (01_KATALOG_FITUR.md:1636).
     - SSI: CRPM 96,6 persen kosong di F-14, di atas 60 persen, jadi "absen"
       (01_KATALOG_FITUR.md:1635).
     - WOB, TORQUE, FLOW, PRESS: tidak ada ukuran per sumur di repo. Ditandai
       "belum", bukan dikarang siap atau absen. 01_KATALOG_FITUR.md:1666
       menyatakan daftar kanal per engine belum lengkap diinventarisasi.
     ------------------------------------------------------------------------ */
  channels: [
    { code: "WOB", name: "Weight on bit", wells: ["belum"] },
    { code: "TORQUE", name: "Torsi", wells: ["belum"] },
    { code: "FLOW", name: "Laju alir", wells: ["belum"] },
    { code: "PRESS", name: "Tekanan", wells: ["belum"] },
    { code: "VIB", name: "Getaran", wells: ["siap"] },
    { code: "SSI", name: "Getaran permukaan", wells: ["absen"] }
  ],

  wells: ["F-14"],

  /* --------------------------------------------------------------------------
     PROVENANCE: docs
     Ukuran byte dan jumlah baris diukur ulang dengan stat dan wc pada
     2026-11-01. Dua entri sebelumnya salah: RND_S6_PM_WAVE2.md 40.064 menjadi
     40.271, dan RND_S5_AUDIT_WAVE2.md "1.015 baris" menjadi 292 baris.
     ------------------------------------------------------------------------ */
  docs: [
    { file: "docs/RND_S6_PM_WAVE2.md", bytes: "40.271", lines: "437 baris", status: "BERLAKU", note: "Vonis komposisi gelombang 2. Sumber angka H1p." },
    { file: "docs/RND_S5_AUDIT_WAVE2.md", bytes: "27.190", lines: "292 baris", status: "BERLAKU", note: "Audit 4 dokumen, 21 artefak JSON, 726 baris ledger." },
    { file: "docs/RND_R8_EVALUASI_BERLAPIS.md", bytes: "27.013", lines: "Layer A/B/C", status: "BERLAKU", note: "Kekuatan bukti, bukan izin pakai." },
    { file: "docs/RND_PM_VERDICT.md", bytes: "34.575", lines: "vonis PM", status: "BERLAKU", note: "Batas klaim dan tier." },
    { file: "docs/RND_EVALUATION_POLICY.md", bytes: "3.992", lines: "kebijakan", status: "BERLAKU", note: "Evaluasi User.txt sebagai sumber mengikat." },
    { file: "planning/01_KATALOG_FITUR.md", bytes: "166.662", lines: "48 fitur", status: "BERLAKU", note: "Katalog fitur berkode KEP." },
    { file: "planning/10_AUDIT.md", bytes: "21.295", lines: "6 cacat teks", status: "PERLU PERBAIKAN", note: "29 dari 30 angka cocok. Cacat tidak mengubah angka." },
    { file: "planning/11_PRIORITAS_BUILD.md", bytes: "51.915", lines: "32/13/3", status: "BERLAKU", note: "Gelombang 1, 2, 3." },
    { file: "planning/08_KONTRAK_DATA.md", bytes: "85.929", lines: "21 fitur", status: "PERLU PERBAIKAN", note: "Bagian 10.13 belum ada. Dua em dash." },
    { file: "planning/09_NASKAH_AKSESIBILITAS.md", bytes: "68.359", lines: "10 layar", status: "BERLAKU", note: "Ukuran berkas di 9.7 perlu disegarkan." }
  ],

  /* --------------------------------------------------------------------------
     PROVENANCE: provenance
     Setiap baris menyebut berkas dan baris asalnya.
     Dua baris lama salah sumber dan sudah diganti:
     - vib AUPRC 0,6204 tidak ada di ledger. Diganti 0,4806 sampai 0,8481
       (ledger S2-018, S2-025, S2-032, S2-039).
     - ssi presisi 0,0237 tidak ada di ledger. Diganti 12,1 alarm palsu per
       alarm benar (ledger S2-448).
     ------------------------------------------------------------------------ */
  provenance: [
    { item: "H1p FP", value: "927", unit: "alarm palsu", source: "RND_S6_PM_WAVE2.md:150", status: "ok" },
    { item: "H1p presisi", value: "0,8243", unit: "rasio", source: "RND_S6_PM_WAVE2.md:150", status: "ok" },
    { item: "H1p recall", value: "0,6519", unit: "rasio", source: "RND_S6_PM_WAVE2.md:150", status: "ok" },
    { item: "H1p FAR", value: "4,0984", unit: "per 24 jam", source: "RND_S6_PM_WAVE2.md:150", status: "ok" },
    { item: "vib AUPRC", value: "0,4806 sampai 0,8481", unit: "rasio per sumur", source: "ledger S2-018, S2-025, S2-032, S2-039", status: "ok" },
    { item: "ssi alarm palsu", value: "12,1", unit: "per alarm benar", source: "ledger S2-448", status: "ok" },
    { item: "bit_wear cap", value: "0,2525", unit: "plafon", source: "06 bagian 5.3 baris 442", status: "note" },
    { item: "tool_wear cap", value: "0,4550", unit: "plafon", source: "06 bagian 5.3 baris 443", status: "note" },
    { item: "Jam tercatat", value: "39.397,986", unit: "jam", source: "RND_S4_LAYER_B_DATA.md:63", status: "ok" },
    { item: "Antrean parse", value: "3.906", unit: "berkas", source: "00_INVENTARIS_V3_V6.md:303, 54,6 persen", status: "ok" },
    { item: "Dokumen belum dibuka", value: "69 / 119", unit: "berkas", source: "00_VERIFIKASI_INVENTARIS.md:378", status: "note" },
    { item: "Slot alarm otomatis", value: "0", unit: "slot", source: "04 baris 33, [J] baris 1414", status: "block" }
  ],

  /* --------------------------------------------------------------------------
     PROVENANCE: glossary
     Definisi dari planning/03_SKOR_KEYAKSINAN.md dan 06. Contoh angka memakai
     sumber yang sama dengan blok di atas. Dua contoh lama salah:
     "cakupan 0,87" menjadi 1,00 (06 bagian 5.2), dan "vib 0,60 tetap P2"
     menjadi P3 karena 0,4950 masuk pita P3 (06 baris 396).
     ------------------------------------------------------------------------ */
  glossary: [
    { term: "TK", short: "Tingkat kewaspadaan", long: "Empat tingkat: TK-1 tenang, TK-2 pantau, TK-3 tinjau, TK-4 hentikan dan periksa. Tingkat bukan perintah.", example: "TK-2 berarti masuk daftar pantau, bukan menghentikan rig." },
    { term: "Pita P1 sampai P5", short: "Pita keyakinan tampil", long: "P1 tidak ada indikasi, P2 indikasi lemah, P3 perlu tinjauan, P4 keyakinan kuat, P5 keyakinan tinggi. Pita dipotong batas kelas.", example: "vib dengan K_seg 0,60 tetap P3 karena batas kelas 0,4950." },
    { term: "K_segmen", short: "Keyakinan satu segmen", long: "Angka keyakinan sebelum dipotong batas kelas. Bisa lebih tinggi dari pita yang tampil.", example: "tool_wear K-ii K_seg 0,6013, tampil 0,4550, pita P3." },
    { term: "K_max", short: "Batas atas bukti kelas", long: "Plafon keyakinan untuk satu kelas. Ditentukan mutu bukti, bukan skor model.", example: "bit_wear K_max 0,2525, jadi tidak bisa melewati P2." },
    { term: "Abstain", short: "Menolak menjawab", long: "Kode AB-1 sampai AB-5. Abstain bukan angka nol, bukan kesalahan, dan tidak boleh disembunyikan.", example: "hyd K-ii abstain AB-1 karena tidak ada komposisi." },
    { term: "Provenance", short: "Asal angka", long: "Setiap angka membawa berkas, baris, dan status. TERUKUR, TURUNAN, atau BELUM KUTIP.", example: "H1p FP 927 berasal dari RND_S6_PM_WAVE2.md baris 150." },
    { term: "L0 sampai L3", short: "Lapisan kepala", long: "L0 aturan tampil, L1 aturan plus gerbang, L2 model statistik, L3 eksplorasi. 27 kepala: 5 L0, 11 L1, 9 L2, 2 L3.", example: "L3 berarti belum layak pakai, bukan hasil." },
    { term: "FAR", short: "False alarm rate", long: "Jumlah alarm palsu per 24 jam kalender. Bukan per 24 jam baris. Satuan harus ditulis.", example: "hyd H1p FAR 4,0984 per 24 jam kalender." },
    { term: "Lead time", short: "Waktu peringatan", long: "Jarak dari alarm ke onset. Semakin panjang belum tentu lebih baik bila alarm palsu naik.", example: "H1p lead 8,0 menit, H1p3 lead 12,5 menit." },
    { term: "AUPRC", short: "Area under precision recall", long: "Ringkasan precision recall untuk kelas tidak seimbang. Harus dibandingkan dengan prevalensi.", example: "shk AUPRC 0,0499 lawan prevalensi 0,0243." },
    { term: "Prevalensi", short: "Laju kelas positif", long: "Bagian baris yang benar-benar positif. Menentukan seberapa tinggi AUPRC yang berarti.", example: "ssi 607 positif dari 35.906 baris." },
    { term: "Kuorum", short: "Jumlah suara minimum", long: "Sedikitnya 4 dari 7 engine harus bersuara, dan cakupan bobot minimal 0,50. Kepala bisu tidak dihitung menolak.", example: "Segmen ini 6 dari 7 bersuara, cakupan bobot 1,00." },
    { term: "Batas dominasi", short: "Plafon satu klaim", long: "Satu klaim tidak boleh lebih dari 35 persen bobot dewan. Bila lewat, bobotnya dipotong.", example: "hyd K-i 36,07 persen dipotong ke 3,2025." },
    { term: "Operating point", short: "Titik operasi", long: "Pilihan ambang yang menukar alarm palsu dengan recall. Bukan satu angka benar.", example: "H1p seimbang, H1p3 alarm rendah, rule cakupan penuh." },
    { term: "LOWO", short: "Leave one well out", long: "Uji dengan satu sumur dikeluarkan dari latihan. Mengukur apakah model bertahan di sumur baru.", example: "7 dari 9 fold memenuhi FAR dan recall untuk H1p." }
  ],

  quiz: [
    { q: "Pita P4 berarti apa?", options: ["Keyakinan kuat, tetap bukan perintah", "Rig harus segera dihentikan", "Alarm otomatis dikirim", "Tidak ada indikasi"], answer: 0, why: "Pita adalah kekuatan bukti. Tindakan tetap keputusan manusia." },
    { q: "Kelas dengan K_max 0,2525 bisa mencapai pita apa?", options: ["P5", "P4", "P2", "P1 saja"], answer: 2, why: "Batas kelas menahan di P2, berapa pun skornya." },
    { q: "Apa arti abstain AB-1?", options: ["Model yakin negatif", "Tidak ada komposisi yang layak", "Data hilang total", "Alarm palsu"], answer: 1, why: "AB-1 berarti tidak ada komposisi, bukan nol dan bukan negatif." },
    { q: "FAR hyd H1p 4,0984 diukur per apa?", options: ["Per 24 jam kalender", "Per 24 jam baris", "Per menit", "Per sumur"], answer: 0, why: "Satuannya 24 jam kalender. Jangan dicampur dengan FAR per baris." },
    { q: "Berapa kepala yang ada di mesin?", options: ["7", "11", "27", "48"], answer: 2, why: "27 kepala dalam 7 mesin: 5 L0, 11 L1, 9 L2, 2 L3." },
    { q: "Berapa slot alarm otomatis?", options: ["0", "7", "11", "27"], answer: 0, why: "Tidak ada kepala yang boleh memicu alarm sendiri." },
    { q: "vib punya AUPRC 0,4806 sampai 0,8481 antar sumur. Apa yang harus dibandingkan?", options: ["Prevalensi kelas", "Jumlah sumur saja", "Lead time saja", "Tidak ada"], answer: 0, why: "AUPRC harus dibaca terhadap prevalensi. Tanpa itu angkanya tidak berarti." },
    { q: "Apa yang terjadi bila satu klaim melewati 35 persen bobot?", options: ["Dinaikkan", "Dipotong ke batas dominasi", "Dihapus", "Tidak dihitung"], answer: 1, why: "Bobot dipotong agar satu klaim tidak menentukan tingkat sendirian." },
    { q: "Siapa pemutus TK-3?", options: ["Model", "Insinyur pengeboran", "Alarm otomatis", "Vendor"], answer: 1, why: "TK-3 diputuskan insinyur pengeboran dalam satu shift." },
    { q: "Apa arti provenance TURUNAN?", options: ["Angka diukur langsung", "Angka dihitung dari angka lain", "Angka belum dikutip", "Angka salah"], answer: 1, why: "TURUNAN berarti hasil hitung, bukan observasi langsung." }
  ],

  /* --------------------------------------------------------------------------
     PROVENANCE: conflicts
     Sumber: planning/06_SWARM_KONSENSUS.md bagian 6.2 (H-1 sampai H-5) dan
     planning/05_KETIDAKSEPAKATAN.md untuk pasangan kepala kembar.
     ------------------------------------------------------------------------ */
  conflicts: [
    { id: "K-1", topic: "Definisi onset", a: "390 onset", b: "181 onset", status: "Terbuka", note: "Penyebut berbeda antara S1 dan S6. Tidak boleh dibandingkan tanpa penyesuaian." },
    { id: "K-2", topic: "Jumlah fold ssi", a: "7 fold S2", b: "9 fold S6", status: "Terbuka", note: "Dua fold UNDERPOWERED ikut di S6. Angka ssi tidak sebanding." },
    { id: "K-3", topic: "Satuan FAR hyd", a: "per 24 jam kalender", b: "per 24 jam baris", status: "Selesai", note: "Satuan ditulis di setiap tabel. Tidak ada konversi diam-diam." },
    { id: "K-4", topic: "Jumlah sumur vib", a: "4 sumur", b: "9 fold", status: "Selesai", note: "Cakupan ditulis di kartu. Bukan 9 sumur." },
    { id: "K-5", topic: "Label bit_wear", a: "indeks mekanika", b: "keausan fisik", status: "Selesai", note: "Banner tetap: label adalah indeks, bukan observasi." },
    { id: "K-6", topic: "FAR tool_wear", a: "per menit", b: "per 24 jam", status: "Selesai", note: "Tidak dibandingkan langsung. Satuannya berbeda." },
    { id: "K-7", topic: "shk AUPRC", a: "0,0499", b: "prevalensi 0,0243", status: "Selesai", note: "Hanya dua kali prevalensi. Tidak boleh disebut kuat." },
    { id: "H-1", topic: "H1p menang?", a: "7 dari 9 fold", b: "FAR naik 0,5682", status: "Selesai", note: "Menang pada syarat gabungan, membayar FAR dan lead lebih pendek." },
    { id: "H-2", topic: "H2 untuk shk?", a: "FP turun 74,67%", b: "TP turun 76,04%", status: "Ditolak", note: "Recall 0,0037. Tidak layak." },
    { id: "H-3", topic: "H1p untuk ssi?", a: "1 TP", b: "17 FP", status: "Ditolak", note: "Recall 0,0 dari 132 onset. Praktis mati." },
    { id: "H-4", topic: "vib hybrid?", a: "FP 183", b: "recall 0,1906", status: "Ditolak", note: "0 dari 4 fold mencapai recall 0,5." },
    { id: "H-5", topic: "hyd K-ii?", a: "satu split", b: "78,7% berbalik tanda", status: "Gagal", note: "GAGAL C. Tidak ada komposisi." }
  ],

  /* --------------------------------------------------------------------------
     PROVENANCE: decisions
     Ini log keputusan SESI, bukan riwayat. app.js menambah baris lewat
     setQueueStatus dan tombol "Catat keputusan", dan foot kartu di views.js
     menulis "Log disimpan di sesi ini. Bukan audit resmi."
     Sebelumnya berkas ini memuat enam baris dengan jam, nama orang, sumur, dan
     besaran turun-naik tekanan yang tidak ada di dokumen mana pun. Enam baris
     itu dibuang, bukan diperbaiki, karena tidak ada satu pun yang bisa
     dilacak. Log mulai kosong dan terisi saat pengguna mencatat keputusan.
     ------------------------------------------------------------------------ */
  decisions: [],

  /* --------------------------------------------------------------------------
     PROVENANCE: features
     Sumber: planning/11_PRIORITAS_BUILD.md (48 fitur, gelombang 1/2/3) dan
     planning/01_KATALOG_FITUR.md. F-03 sebelumnya menulis "12 baris"; antrean
     di 04 bagian 6.2 berisi 10 baris.
     ------------------------------------------------------------------------ */
  features: [
    { id: "F-01", name: "Banner TK satu baris", status: "LAYAK", note: "Tingkat, dukungan, kuorum, cakupan. Tanpa tindakan otomatis." },
    { id: "F-02", name: "Kartu fokus", status: "LAYAK", note: "Maksimal 3. Klaim, sumur, jendela, pita, keyakinan, aksi." },
    { id: "F-03", name: "Antrean tinjauan", status: "LAYAK", note: "10 baris, 10 kolom, aksi tutup dan tunda." },
    { id: "F-04", name: "Batang keyakinan lawan batas", status: "LAYAK", note: "Satu batang per klaim, garis batas kelas." },
    { id: "F-05", name: "Pareto jam henti", status: "LAYAK", note: "Batang dan garis kumulatif. Tanpa donat." },
    { id: "F-06", name: "Matriks kesiapan kanal", status: "LAYAK BERSYARAT", note: "Butuh data per sumur yang lengkap." },
    { id: "F-07", name: "Peta ketidaksepakatan", status: "LAYAK", note: "7 mesin x 11 klaim. Sel kosong berarti bisu." },
    { id: "F-08", name: "Kalkulator beban", status: "LAYAK", note: "Input menit per pemeriksaan, output jam." },
    { id: "F-09", name: "Buku konflik", status: "LAYAK", note: "12 entri, status terbuka atau selesai." },
    { id: "F-10", name: "Kamus istilah", status: "LAYAK", note: "15 istilah, contoh benar dan salah." }
  ],

  owners: [
    { area: "Data historian", owner: "Data Engineer", need: "Ekspor kanal per sumur, resolusi 1 detik", status: "Sebagian" },
    { area: "Sensor permukaan", owner: "Instrumentation", need: "Kalibrasi CRPM dan akselerometer", status: "Terbuka" },
    { area: "Catatan perawatan", owner: "Reliability", need: "Kode pekerjaan dan durasi", status: "Siap" },
    { area: "Catatan pengeboran", owner: "Drilling Engineer", need: "Onset dan label per kejadian", status: "Sebagian" },
    { area: "Keputusan operasi", owner: "Superintendent", need: "Ambang biaya dan jadwal inspeksi", status: "Terbuka" }
  ],

  l3: [
    { name: "Rating motor", reason: "Data terblokir. Tidak dinilai menurut desain.", code: "AB-4" },
    { name: "Tekanan EDM", reason: "Data terblokir. Tidak dinilai menurut desain.", code: "AB-4" }
  ],

  /* PROVENANCE: layerB. Sumber jam: docs/RND_S4_LAYER_B_DATA.md:63 dan :68. */
  layerB: [
    { slot: "Biaya rupiah", status: "Tidak ada", note: "Tidak ada kolom biaya. Jangan mengarang rupiah." },
    { slot: "Jadwal inspeksi", status: "Tidak ada", note: "Tidak ada kalender inspeksi di repo." },
    { slot: "Produksi tertunda", status: "Tidak ada", note: "Tidak ada berkas deferred production." },
    { slot: "Jam henti", status: "Terukur", note: "39.397,986 jam tercatat. 1.215,0 jam perbaikan interupsi." },
    { slot: "Cuaca", status: "Terukur", note: "1.925,5 jam menunggu cuaca." }
  ],

  forbidden: [
    { name: "Gauge", why: "Menyembunyikan ketidakpastian di balik jarum.", right: "Batang dengan garis batas kelas." },
    { name: "Donat", why: "Sulit dibandingkan dan memakan ruang.", right: "Batang mendatar atau angka langsung." },
    { name: "Radar", why: "Bentuk tidak cocok untuk 11 kelas dan 27 kepala.", right: "Matriks atau tabel." },
    { name: "Dua sumbu Y", why: "Membuat korelasi palsu.", right: "Dua panel terpisah." },
    { name: "Pai 3D", why: "Distorsi sudut dan kedalaman.", right: "Pareto batang." },
    { name: "Gradien dekoratif", why: "Menambah tinta tanpa informasi.", right: "Warna datar dengan peran." },
    { name: "Sirene alarm", why: "Menyiratkan tindakan otomatis.", right: "Pita dan teks keputusan." },
    { name: "Keputusan otomatis", why: "Melampaui bukti dan tanggung jawab.", right: "Tombol tinjau dan catat alasan." },
    { name: "Presisi palsu", why: "Empat desimal tanpa satuan menyesatkan.", right: "Angka, satuan, sumber, status." }
  ],

  axes: [
    { name: "Bukti", value: "Sedang", note: "Angka terukur ada, tetapi beberapa kelas masih P1." },
    { name: "Cakupan", value: "Sempit", note: "4 sampai 9 sumur per kelas, bukan seluruh lapangan." },
    { name: "Kesiapan", value: "Pilot", note: "Alat bantu, bukan sistem operasi penuh." }
  ],

  readExamples: [
    { text: "P 0,8243", right: "Presisi 82,43 persen pada titik operasi ini.", wrong: "Akurasi model 82,43 persen untuk semua data." },
    { text: "FAR 4,0984", right: "Sekitar 4 alarm palsu per 24 jam kalender.", wrong: "4 alarm palsu per 24 jam baris." },
    { text: "Recall 0,6519", right: "65,19 persen onset berhasil diperingatkan.", wrong: "65,19 persen sumur aman." },
    { text: "AUPRC 0,0499", right: "Sedikit di atas prevalensi 0,0243. Lemah.", wrong: "Model akurat 4,99 persen." }
  ],

  /* --------------------------------------------------------------------------
     PROVENANCE: signalFeasibility dan channelsInstall
     Hanya angka yang terukur di repo yang dipakai:
     - VIBLAT 356 dari 1.989 baris kosong di F-14 (01_KATALOG_FITUR.md:1636).
     - CRPM 96,6 persen kosong di F-14, 62,3 persen lintas data
       (01_KATALOG_FITUR.md:1634 sampai 1636).
     - vib 4 sumur dan 5.429 baris positif (ledger S2-007, S2-012).
     Sebelumnya blok ini menyebut kanal tekanan dan aliran "tipis" dan "absen"
     pada satu sumur tanpa ukuran apa pun. Klaim itu dibuang.
     ------------------------------------------------------------------------ */
  signalFeasibility: [
    { name: "Getaran", status: "Siap", note: "VIBLAT 356 dari 1.989 baris kosong di F-14, 17,9 persen. 4 sumur, 5.429 positif.", tone: "ok" },
    { name: "Tekanan", status: "Belum dikutip", note: "Tidak ada ukuran kanal tekanan per sumur di repo.", tone: "warn" },
    { name: "Aliran", status: "Belum dikutip", note: "Tidak ada ukuran kanal aliran per sumur di repo.", tone: "bad" },
    { name: "Torsi", status: "Belum dikutip", note: "Tidak ada ukuran kanal torsi per sumur di repo.", tone: "warn" }
  ],

  channelsInstall: [
    { name: "CRPM", use: "Intensitas getaran permukaan", cost: "Sedang", lead: "2 sampai 4 minggu", note: "Absen 62,3 persen lintas data dan 96,6 persen di F-14." },
    { name: "Akselerometer", use: "Getaran triaksial", cost: "Sedang", lead: "2 minggu", note: "Sudah ada di 4 sumur." },
    { name: "Flow meter", use: "Laju alir", cost: "Tinggi", lead: "4 sampai 8 minggu", note: "BELUM KUTIP. Tidak ada ukuran per sumur." },
    { name: "Pressure transducer", use: "Tekanan masuk dan keluar", cost: "Rendah", lead: "1 minggu", note: "BELUM KUTIP. Tidak ada ukuran per sumur." },
    { name: "Depth encoder", use: "Kedalaman dan laju penembusan", cost: "Rendah", lead: "1 minggu", note: "Resolusi perlu dicek." },
    { name: "Torque sensor", use: "Torsi rangkaian", cost: "Rendah", lead: "1 minggu", note: "BELUM KUTIP. Tidak ada ukuran per sumur." }
  ],

  qualityChecklist: [
    { text: "Angka punya satuan", hint: "FAR per 24 jam kalender, bukan per baris." },
    { text: "Angka punya sumber", hint: "Berkas dan baris, bukan ingatan." },
    { text: "Abstain tidak disembunyikan", hint: "AB-1 sampai AB-5 tampil." },
    { text: "Pita tidak melewati batas kelas", hint: "Bandingkan K_tampil dengan K_max." },
    { text: "Tidak ada keputusan otomatis", hint: "Tombol hanya mencatat, bukan memerintah." },
    { text: "Tidak ada grafik terlarang", hint: "Gauge, donat, radar, dua sumbu Y, pai 3D." }
  ],

  wizardSteps: [
    { title: "Pilih kelas", body: "Mulai dari kelas yang punya bukti, bukan dari grafik yang paling menarik." },
    { title: "Cek data", body: "Pastikan kanal dan label cukup. Bila tidak, abstain." },
    { title: "Pilih mode", body: "Peringatan dini, alarm rendah, atau pemantauan tren." },
    { title: "Baca hasil", body: "Baca pita, batas kelas, FAR, lead, dan sumber. Catat keputusan." }
  ]
};
