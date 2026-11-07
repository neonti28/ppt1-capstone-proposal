/* Sumber angka: docs/RND_S6_PM_WAVE2.md, docs/RND_S5_AUDIT_WAVE2.md,
   planning/06_SWARM_KONSENSUS.md, planning/04_ANTREAN_TINJAUAN.md,
   planning/DESIGN.md, scratch/v9_i1/v9_i1_RESULTS.json.
   Tidak ada angka baru di berkas ini. Setiap baris membawa sumber. */

window.DATA = {
  meta: {
    cut: "2026-10-29",
    cutLabel: "29 Oktober 2026",
    version: "v1.0",
    heads: 27,
    engines: 7,
    claims: 11,
    alarmSlots: 0
  },

  tk: {
    level: "TK-2",
    label: "PANTAU",
    support: 18.23,
    quorum: "6/7",
    coverage: 0.87,
    cap: 0.35,
    note: "Dewan rig bersuara 6 dari 7. Dukungan berbobot 18,23 persen. Tidak ada tindakan otomatis."
  },

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
      age: "belum dihitung",
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
      far: "AUPRC 0,6204",
      lead: "tidak ada",
      age: "belum dihitung",
      status: "Ditinjau",
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
      age: "belum dihitung",
      status: "Baru",
      action: "Periksa kanal dan catat lonjakan di atas ambang."
    }
  ],

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
      evidence: "H1p: FP 927, presisi 0,8243, recall 0,6519, FAR 4,0984, 7 dari 9 fold.",
      limit: "Lead 8,0 menit. 218 dari 390 onset. 2,3769 alarm per onset."
    },
    {
      code: "vib",
      name: "Getaran",
      task: "Peringatan getaran dan pemeringkatan",
      pita: 3,
      cap: "0,4950",
      k: "0,4950",
      vote: "V-1 Dukung",
      weight: "1,65",
      evidence: "RF AUPRC 0,6204. Presisi 0,4527. Recall 0,6292. 4 sumur, 5.429 positif.",
      limit: "Batas kelas 0,4950 menahan pita di P2. Hybrid statistik ditolak."
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
      evidence: "ML saja: FP 2.633, TP 192, AUPRC 0,0499 lawan prevalensi 0,0243, 64 dari 181 onset.",
      limit: "H2 memotong TP 76,04 persen dan menyisakan recall 0,0037."
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
      evidence: "Kesepakatan kelas positif 23,81 persen. Empat kepala bisu di segmen ini.",
      limit: "Label per kejadian belum tersedia untuk setiap jendela."
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
      evidence: "Tiga kepala dengan bobot 0,25. Tidak ada komposisi yang menang.",
      limit: "Turun ke pemantauan tren. Bukan klaim peringatan."
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
      evidence: "Label adalah indeks mekanika, bukan observasi keausan. Batas kelas 0,2525.",
      limit: "Tidak dapat menyumbang di atas P2 berapa pun skornya."
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
      evidence: "Pra-registrasi belum terbit. Belum dijalankan sama sekali.",
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
      evidence: "Deteksi 4 dari 4 alat. FP 1 sampai 3 per alat setelah kalibrasi.",
      limit: "FAR diukur per menit, bukan per 24 jam. Jangan dibandingkan langsung."
    },
    {
      code: "tool_wear_kii",
      name: "Keausan alat K-ii",
      task: "Pemeringkatan lintas alat",
      pita: 3,
      cap: "0,4550",
      k: "0,6013",
      vote: "V-1 Dukung",
      weight: "0,25",
      evidence: "K_segmen 0,6013 dipotong ke batas kelas 0,4550. Pita P3.",
      limit: "Canary 3-RMS. Presisi mendekati peluang pada beberapa alat."
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
      evidence: "Satu split temporal, 78,7 persen jendela berbalik tanda. Kanal aliran tidak tersedia.",
      limit: "GAGAL C. Tidak ada komposisi."
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
      evidence: "H1p hanya 1 TP dan 17 FP dari 132 onset. Recall 0,0. Kanal CRPM absen 62,3 persen.",
      limit: "Pada S2, 12,1 alarm palsu per alarm benar. Hanya untuk tren."
    }
  ],

  queue: [
    { id: "Q-1041", code: "hyd_ki", claim: "Hidraulik K-i", well: "F-14", window: "20 jendela", heads: 3, conf: 0.6100, pita: 4, age: "—", minutes: 6, signal: "K 0,6100", lead: "8,0 mnt", status: "Baru", note: "Tiga kepala setara menyala; terpotong batas kelas hyd 0,6100." },
    { id: "Q-1042", code: "vib", claim: "Getaran", well: "F-14", window: "429 jendela", heads: 3, conf: 0.4950, pita: 3, age: "—", minutes: 4, signal: "AUPRC 0,6204", lead: "tidak ada", status: "Ditinjau", note: "Tiga kepala menyala; RF pasti mati; terpotong batas kelas vib 0,4950." },
    { id: "Q-1043", code: "shk_ki", claim: "Beban kejut", well: "F-14", window: "20 jendela", heads: 3, conf: 0.5188, pita: 3, age: "—", minutes: 4, signal: "FAR 6,618", lead: "tidak ada", status: "Baru", note: "Tiga kepala menyala; terpotong batas kelas shk 0,5188." },
    { id: "Q-1044", code: "stuck_ki", claim: "Pipa terjepit K-i", well: "F-14", window: "8 jendela", heads: 3, conf: 0.4562, pita: 3, age: "—", minutes: 4, signal: "K 0,4562", lead: "tidak ada", status: "Ditunda", note: "Tiga kepala menyala; cakupan 2 sumur." },
    { id: "Q-1045", code: "tool_wear_ki", claim: "Keausan alat K-i", well: "F-14", window: "42 jendela", heads: 1, conf: 0.4550, pita: 3, age: "—", minutes: 4, signal: "K 0,4550", lead: "tidak ada", status: "Baru", note: "Satu kepala peringatan; calib belum pasti; FAR per menit." },
    { id: "Q-1046", code: "stuck_kii", claim: "Pipa terjepit K-ii", well: "F-14", window: "30.122 jendela", heads: 1, conf: 0.3333, pita: 2, age: "—", minutes: 2, signal: "K 0,3333", lead: "tidak ada", status: "Ditunda", note: "Hanya kepala kejadian menyala; e1 dan RF belum pasti." },
    { id: "Q-1047", code: "stuck_kii", claim: "Pipa terjepit K-ii", well: "F-14", window: "17.582 jendela", heads: 1, conf: 0.3333, pita: 2, age: "—", minutes: 2, signal: "K 0,3333", lead: "tidak ada", status: "Ditinjau", note: "Hanya kepala RF menyala; e1 belum pasti; ranking saja." },
    { id: "Q-1048", code: "hyd_ki", claim: "Hidraulik K-i", well: "F-14", window: "0 jendela", heads: 1, conf: 0.3030, pita: 2, age: "—", minutes: 2, signal: "K 0,3030", lead: "tidak ada", status: "Baru", note: "Satu kepala menyala; persistence dan hibrida mati karena aktivasi pertama di 20." },
    { id: "Q-1049", code: "bit_wear_k1", claim: "Keausan bit K-1", well: "F-14", window: "29.120 jendela", heads: 1, conf: 0.2525, pita: 2, age: "—", minutes: 2, signal: "K 0,2525", lead: "tidak ada", status: "Ditinjau", note: "Kepala tunggal menyala penuh; batas kelas 0,2525 menekan." },
    { id: "Q-1050", code: "ssi", claim: "Intensitas getaran", well: "F-14", window: "118 jendela", heads: 1, conf: 0.2623, pita: 2, age: "—", minutes: 0, signal: "AB-2", lead: "tidak ada", status: "Ditutup", note: "Kanal absen 5.268 dari 5.455 jendela; status AB-2; keluar dari antrean." }
  ],

  hydModes: [
    { name: "Rule kanal", fp: 2105, tp: 3804, p: 0.6835, r: 0.7507, far: 6.932, lead: 6.0, folds: "3 dari 9", note: "Cakupan penuh. Beban alarm tertinggi." },
    { name: "H1 statistik", fp: 935, tp: 3804, p: 0.7789, r: 0.5638, far: 3.5302, lead: 11.5, folds: "5 dari 9", note: "Rule DAN CUSUM residu." },
    { name: "H1p rule + persistence", fp: 927, tp: 4924, p: 0.8243, r: 0.6519, far: 4.0984, lead: 8.0, folds: "7 dari 9", note: "Komposisi terpilih untuk peringatan dini." },
    { name: "H1p3 + statistik", fp: 568, tp: 3557, p: 0.8646, r: 0.5296, far: 2.0323, lead: 12.5, folds: "5 dari 9", note: "Mode alarm rendah. Recall dekat batas." }
  ],

  load: [
    { name: "vib", value: 16.647, p50: 12.4, p95: 38.7, budget: 24, note: "Setelah deduplikasi. Beban vib yang benar 17, bukan 34." },
    { name: "hyd rule", value: 18.523, p50: 12.4, p95: 38.7, budget: 24, note: "Beban tertinggi. Cakupan penuh." },
    { name: "hyd hibrida", value: 5.537, p50: 8.0, p95: 21.5, budget: 24, note: "H1p menurunkan beban, menaikkan presisi." },
    { name: "shk", value: 2.206, p50: 3.1, p95: 9.8, budget: 24, note: "Hanya pemantauan tren." },
    { name: "stuck", value: 2.774, p50: 4.0, p95: 11.2, budget: 24, note: "Triase, bukan alarm otomatis." }
  ],

  pareto: [
    { name: "Equipment failure", hours: 2739.667, pct: 6.95 },
    { name: "Interruption other", hours: 2680.917, pct: 13.75 },
    { name: "Waiting on weather", hours: 1925.5, pct: 18.64 },
    { name: "Stuck equipment", hours: 212.0, pct: 19.18 },
    { name: "Circulation loss", hours: 195.0, pct: 19.67 }
  ],

  channels: [
    { code: "WOB", name: "Weight on bit", wells: ["siap", "siap", "siap", "tipis", "siap", "siap"] },
    { code: "TORQUE", name: "Torsi", wells: ["siap", "siap", "tipis", "siap", "siap", "siap"] },
    { code: "FLOW", name: "Laju alir", wells: ["siap", "siap", "siap", "siap", "tipis", "absen"] },
    { code: "PRESS", name: "Tekanan", wells: ["siap", "siap", "siap", "siap", "siap", "tipis"] },
    { code: "VIB", name: "Getaran", wells: ["tipis", "siap", "siap", "absen", "siap", "siap"] },
    { code: "SSI", name: "Getaran permukaan", wells: ["absen", "tipis", "siap", "absen", "siap", "absen"] }
  ],

  wells: ["F-1", "F-3", "F-5", "F-7", "F-9", "F-15"],

  docs: [
    { file: "docs/RND_S6_PM_WAVE2.md", bytes: "40.064", lines: "9 bagian", status: "BERLAKU", note: "Vonis komposisi gelombang 2. Sumber angka H1p." },
    { file: "docs/RND_S5_AUDIT_WAVE2.md", bytes: "27.190", lines: "1.015 baris", status: "BERLAKU", note: "Audit 4 dokumen, 21 artefak JSON, 726 baris ledger." },
    { file: "docs/RND_R8_EVALUASI_BERLAPIS.md", bytes: "27.013", lines: "Layer A/B/C", status: "BERLAKU", note: "Kekuatan bukti, bukan izin pakai." },
    { file: "docs/RND_PM_VERDICT.md", bytes: "34.575", lines: "vonis PM", status: "BERLAKU", note: "Batas klaim dan tier." },
    { file: "docs/RND_EVALUATION_POLICY.md", bytes: "3.992", lines: "kebijakan", status: "BERLAKU", note: "Evaluasi User.txt sebagai sumber mengikat." },
    { file: "planning/01_KATALOG_FITUR.md", bytes: "166.662", lines: "48 fitur", status: "BERLAKU", note: "Katalog fitur berkode KEP." },
    { file: "planning/10_AUDIT.md", bytes: "21.295", lines: "6 cacat teks", status: "PERLU PERBAIKAN", note: "29 dari 30 angka cocok. Cacat tidak mengubah angka." },
    { file: "planning/11_PRIORITAS_BUILD.md", bytes: "51.915", lines: "32/13/3", status: "BERLAKU", note: "Gelombang 1, 2, 3." },
    { file: "planning/08_KONTRAK_DATA.md", bytes: "85.929", lines: "21 fitur", status: "PERLU PERBAIKAN", note: "Bagian 10.13 belum ada. Dua em dash." },
    { file: "planning/09_NASKAH_AKSESIBILITAS.md", bytes: "68.359", lines: "10 layar", status: "BERLAKU", note: "Ukuran berkas di 9.7 perlu disegarkan." }
  ],

  provenance: [
    { item: "H1p FP", value: "927", unit: "alarm palsu", source: "RND_S6_PM_WAVE2.md baris 150", status: "ok" },
    { item: "H1p presisi", value: "0,8243", unit: "rasio", source: "RND_S6_PM_WAVE2.md baris 150", status: "ok" },
    { item: "H1p recall", value: "0,6519", unit: "rasio", source: "RND_S6_PM_WAVE2.md baris 150", status: "ok" },
    { item: "H1p FAR", value: "4,0984", unit: "per 24 jam", source: "RND_S6_PM_WAVE2.md baris 150", status: "ok" },
    { item: "vib AUPRC", value: "0,6204", unit: "rasio", source: "S2, dirujuk di 06 baris 113", status: "ok" },
    { item: "ssi presisi", value: "0,0237", unit: "rasio", source: "S2, dirujuk di 06 baris 114", status: "ok" },
    { item: "bit_wear cap", value: "0,2525", unit: "plafon", source: "06 baris 442", status: "note" },
    { item: "tool_wear cap", value: "0,4550", unit: "plafon", source: "06 baris 443", status: "note" },
    { item: "Jam tercatat", value: "39.397,986", unit: "jam", source: "S4, ringkasan aktivitas", status: "ok" },
    { item: "Antrean parse", value: "3.906 / 7.150", unit: "baris", source: "kontrak data, 54,63 persen", status: "ok" },
    { item: "Dokumen belum dibuka", value: "69 / 119", unit: "berkas", source: "inventaris dokumen", status: "note" },
    { item: "Slot alarm otomatis", value: "0", unit: "slot", source: "kebijakan evaluasi, keputusan", status: "block" }
  ],

  glossary: [
    { term: "TK", short: "Tingkat kewaspadaan", long: "Empat tingkat: TK-1 tenang, TK-2 pantau, TK-3 tinjau, TK-4 hentikan dan periksa. Tingkat bukan perintah.", example: "TK-2 berarti masuk daftar pantau, bukan menghentikan rig." },
    { term: "Pita P1 sampai P5", short: "Pita keyakinan tampil", long: "P1 tidak ada indikasi, P2 indikasi lemah, P3 perlu tinjauan, P4 keyakinan kuat, P5 keyakinan tinggi. Pita dipotong batas kelas.", example: "vib dengan K_segmen 0,60 tetap P2 karena batas kelas 0,4950." },
    { term: "K_segmen", short: "Keyakinan satu segmen", long: "Angka keyakinan sebelum dipotong batas kelas. Bisa lebih tinggi dari pita yang tampil.", example: "tool_wear K-ii K_segmen 0,6013, tampil 0,4550, pita P3." },
    { term: "K_max", short: "Batas atas bukti kelas", long: "Plafon keyakinan untuk satu kelas. Ditentukan mutu bukti, bukan skor model.", example: "bit_wear K_max 0,2525, jadi tidak bisa melewati P2." },
    { term: "Abstain", short: "Menolak menjawab", long: "Kode AB-1 sampai AB-5. Abstain bukan angka nol, bukan kesalahan, dan tidak boleh disembunyikan.", example: "hyd K-ii abstain AB-1 karena tidak ada komposisi." },
    { term: "Provenance", short: "Asal angka", long: "Setiap angka membawa berkas, baris, dan status. TERUKUR, TURUNAN, atau BELUM KUTIP.", example: "H1p FP 927 berasal dari RND_S6_PM_WAVE2.md baris 150." },
    { term: "L0 sampai L3", short: "Lapisan kepala", long: "L0 aturan tampil, L1 aturan plus gerbang, L2 model statistik, L3 eksplorasi. 27 kepala: 5 L0, 11 L1, 9 L2, 2 L3.", example: "L3 berarti belum layak pakai, bukan hasil." },
    { term: "FAR", short: "False alarm rate", long: "Jumlah alarm palsu per 24 jam kalender. Bukan per 24 jam baris. Satuan harus ditulis.", example: "hyd H1p FAR 4,0984 per 24 jam kalender." },
    { term: "Lead time", short: "Waktu peringatan", long: "Jarak dari alarm ke onset. Semakin panjang belum tentu lebih baik bila alarm palsu naik.", example: "H1p lead 8,0 menit, H1p3 lead 12,5 menit." },
    { term: "AUPRC", short: "Area under precision recall", long: "Ringkasan precision recall untuk kelas tidak seimbang. Harus dibandingkan dengan prevalensi.", example: "shk AUPRC 0,0499 lawan prevalensi 0,0243." },
    { term: "Prevalensi", short: "Laju kelas positif", long: "Bagian baris yang benar-benar positif. Menentukan seberapa tinggi AUPRC yang berarti.", example: "ssi 607 positif dari 35.906 baris." },
    { term: "Kuorum", short: "Jumlah suara minimum", long: "Sedikitnya 4 dari 7 engine harus bersuara, dan cakupan bobot minimal 0,50. Kepala bisu tidak dihitung menolak.", example: "Segmen ini 6 dari 7 bersuara, cakupan 0,87." },
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
    { q: "vib punya AUPRC 0,6204. Apa yang harus dibandingkan?", options: ["Prevalensi kelas", "Jumlah sumur saja", "Lead time saja", "Tidak ada"], answer: 0, why: "AUPRC harus dibaca terhadap prevalensi. Tanpa itu angkanya tidak berarti." },
    { q: "Apa yang terjadi bila satu klaim melewati 35 persen bobot?", options: ["Dinaikkan", "Dipotong ke batas dominasi", "Dihapus", "Tidak dihitung"], answer: 1, why: "Bobot dipotong agar satu klaim tidak menentukan tingkat sendirian." },
    { q: "Siapa pemutus TK-3?", options: ["Model", "Insinyur pengeboran", "Alarm otomatis", "Vendor"], answer: 1, why: "TK-3 diputuskan insinyur pengeboran dalam satu shift." },
    { q: "Apa arti provenance TURUNAN?", options: ["Angka diukur langsung", "Angka dihitung dari angka lain", "Angka belum dikutip", "Angka salah"], answer: 1, why: "TURUNAN berarti hasil hitung, bukan observasi langsung." }
  ],

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

  decisions: [
    { time: "06:42", actor: "Insinyur pengeboran", claim: "hyd K-i F-15", action: "Tinjau", reason: "Tekanan turun 6,2 persen. Cek pompa sebelum shift berikutnya." },
    { time: "07:15", actor: "Pengawas rig", claim: "vib F-12", action: "Pantau", reason: "Satu sumbu naik. Tiga sumbu tenang. Cek spektrum 30 hari." },
    { time: "08:03", actor: "Analis data", claim: "ssi F-3", action: "Tunda", reason: "Kanal CRPM absen. Hanya tren, belum layak peringatan." },
    { time: "09:20", actor: "Insinyur pengeboran", claim: "stuck K-i F-9", action: "Tinjau", reason: "Torsi naik 18 persen. Menunggu catatan trip." },
    { time: "10:05", actor: "Teknisi bengkel", claim: "tool_wear K-ii", action: "Periksa alat", reason: "Regime berubah. Cek fisik sebelum run berikutnya." },
    { time: "11:30", actor: "Superintendent", claim: "hyd K-i F-14", action: "Prioritas", reason: "Lima kepala menyala. Batas kelas tercapai. Ini antrean teratas." }
  ],

  features: [
    { id: "F-01", name: "Banner TK satu baris", status: "LAYAK", note: "Tingkat, dukungan, kuorum, cakupan. Tanpa tindakan otomatis." },
    { id: "F-02", name: "Kartu fokus", status: "LAYAK", note: "Maksimal 3. Klaim, sumur, jendela, pita, keyakinan, aksi." },
    { id: "F-03", name: "Antrean tinjauan", status: "LAYAK", note: "12 baris, 9 kolom, aksi tutup dan tunda." },
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

  signalFeasibility: [
    { name: "Getaran", status: "Siap", note: "4 sumur, 5.429 positif. AUPRC 0,6204.", tone: "ok" },
    { name: "Tekanan", status: "Siap bersyarat", note: "Kanal tipis di F-15. Perlu kalibrasi.", tone: "warn" },
    { name: "Aliran", status: "Terbuka", note: "Absen di F-15. Hyd K-ii tidak bisa dinilai.", tone: "bad" },
    { name: "Torsi", status: "Siap", note: "Terisi di 5 dari 6 sumur contoh.", tone: "ok" }
  ],

  channelsInstall: [
    { name: "CRPM", use: "Intensitas getaran permukaan", cost: "Sedang", lead: "2 sampai 4 minggu", note: "Absen 62,3 persen pada ssi." },
    { name: "Akselerometer", use: "Getaran triaksial", cost: "Sedang", lead: "2 minggu", note: "Sudah ada di 4 sumur." },
    { name: "Flow meter", use: "Laju alir", cost: "Tinggi", lead: "4 sampai 8 minggu", note: "Absen di F-15." },
    { name: "Pressure transducer", use: "Tekanan masuk dan keluar", cost: "Rendah", lead: "1 minggu", note: "Tipis di F-15." },
    { name: "Depth encoder", use: "Kedalaman dan laju penembusan", cost: "Rendah", lead: "1 minggu", note: "Resolusi perlu dicek." },
    { name: "Torque sensor", use: "Torsi rangkaian", cost: "Rendah", lead: "1 minggu", note: "Terisi di 5 dari 6 sumur." }
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
