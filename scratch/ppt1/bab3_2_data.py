"""Data untuk BAB III subbab 3.2 dan 3.3.

Semua angka di sini membawa jejak (berkas + baris, kunci JSON, atau skrip).
Struktur ini adalah sumber tunggal: dokumen markdown dirender dari sini,
lalu diperiksa ulang oleh scratch/ppt1/check_bab3_2.py.
"""

META = {
    "dokumen": "Proposal Proyek Perancangan Terpadu I, BAB III subbab 3.2 dan 3.3",
    "versi": "1.0",
    "dibuat": "2026-10-25",
    "mitra": "PT Halliburton Indonesia, divisi Sperry Drilling",
    "acuan_format": "Buku Pedoman PPT Tahap I subbab 3.2 Format Proposal, halaman 33 sampai 36",
    "acuan_rubrik": "Rubrik Penilaian PPT oleh Dosen, halaman 38 dan berikutnya, butir 2.2, 3.1, 3.2, 3.3",
    "acuan_bok": "Buku Pedoman PPT Tahap I Tabel 2.1, empat belas IEBoK, selaras IISE ISEBoK 2021",
    "sumber_utama": [
        "docs/PPT1_BAB3_1.md",
        "scratch/ppt1/alternatif.json",
        "docs/V7_R1_SOLUTIONS.md",
        "docs/V4_MAINTENANCE_ML_OPTIONS.md",
        "docs/V8_PM_VERDICT.md",
        "docs/V8_R1_ABC_SPEC.md",
        "docs/V8_E_shk_CAPABILITY.md",
        "docs/V9_PM1_ARCHITECTURE.md",
        "docs/V9_PM2_VERDICT.md",
        "docs/V9_EVAL_B_LAYERB.md",
        "docs/V9_EVAL_C_LAYERC.md",
        "docs/V10_D1_BAB_DATA.md",
        "docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md",
        "docs/PPT1_LEDGER_ANGKA.md",
        "scratch/v9_i1/v9_i1_RESULTS.json",
    ],
}

RISET = [
    "Riset pendahuluan: `ppt-halliburton` (berkas pendamping `references/alternative-solutions-guide.md` dan `references/ppt1-proposal-build.md`) - syarat pedoman untuk 3.2 dan 3.3, yaitu affinity map untuk clustering ide, minimal tiga BoK, kriteria pemilihan berbasis functional requirement stakeholder, dan format user story sebagai kalimat peran, kebutuhan, manfaat.",
    "Riset pendahuluan: `sequentialthinking` (sequ-mcp, lima pikiran) - uji apakah peta afinitas cukup memakai sumbu keanggotaan (ditolak karena hanya menyalin 3.1), lalu penetapan sumbu objek intervensi, uji kasus batas A7, pemilihan empat BoK yang didalami, dan pemisahan tugas 3.3 dari bobot MCDM.",
    "Riset pendahuluan: `grounded-citations` - setiap angka pada 3.2 dan 3.3 melekat pada berkas dan nomor baris atau kunci JSON, dan diperiksa ulang oleh skrip pemeriksa, bukan dari ingatan.",
]

ATURAN_BUKTI = [
    "Setiap angka menyebut berkas dan nomor baris, kunci JSON, atau skrip yang dapat dijalankan ulang.",
    "Angka yang belum dihitung ditulis eksplisit sebagai asumsi atau perkiraan desain, dan tidak disamarkan sebagai hasil pengukuran.",
    "Status pelaksanaan hanya memakai tiga nilai baku yang sama dengan subbab 3.1, yaitu Selesai, Berjalan, dan Rencana (belum terealisasi).",
    "Dokumen tim tidak disebut dengan kata yang menyiratkan tuduhan. Yang dilakukan adalah menelusuri asal angka dan menguatkannya.",
]

METODE_AFINITAS = [
    "Himpunan yang dikelompokkan adalah sembilan alternatif yang sudah berkode pada subbab 3.1. Tidak ada alternatif baru yang ditambahkan pada langkah pengelompokan, sehingga peta tidak memunculkan ide hantu.",
    "Sumbu pengelompokan ditetapkan sebelum hasil dilihat, yaitu objek yang diubah pada sistem kerja: definisi target, basis bukti, formulasi model, dan titik operasi keputusan. Sumbu ini dipilih karena sembilan alternatif pada 3.1 sudah dibedakan oleh mekanisme, bukan oleh kelas disfungsi.",
    "Uji keterpisahan: satu alternatif hanya boleh masuk satu klaster, ditentukan oleh mekanisme utamanya. Alternatif yang menyentuh dua klaster dicatat sebagai kasus batas dan tetap ditempatkan pada mekanisme dominannya.",
    "Penamaan klaster memakai kata kerja dan objek, bukan nama bidang, supaya nama langsung menyatakan apa yang diubah.",
    "Sumbu keanggotaan (anggota 1, 2, dan 3) sengaja tidak dipakai sebagai sumbu pengelompokan. Alasan terukur: bila sumbunya keanggotaan, peta hanya menyalin pembagian pada subbab 3.1 dan tidak menghasilkan informasi baru. Hasil pengelompokan menunjukkan dua dari empat klaster melintasi batas anggota, sehingga kedua peta memang berbeda.",
]

KLASTER = [
    {
        "id": "K1",
        "nama": "Definisi target dan mutu label",
        "label_g1": "Target dan mutu label",
        "warna": "#2563eb",
        "prinsip": "Ketiga alternatif mengubah apa yang dihitung sebagai kejadian positif, atau menguji kebenaran label yang sudah ada. Tidak ada yang mengubah model dan tidak ada yang menambah data baru.",
        "anggota": ["A1", "A3", "A8"],
        "mekanisme": [
            ("A1", "Memindahkan definisi target dari status yang bertahan menjadi titik masuk peristiwa, lalu membuang jendela di dalam blok setelah onset."),
            ("A3", "Mengaudit semantik label lebih dahulu, mengunci satu varian onset, lalu menambah sumbu bukti melalui label multi-sumber bila noise antar sumber masih besar."),
            ("A8", "Mengganti sumber label dari ambang statistik menjadi mekanisme fisika, yaitu perubahan volume pit dan selisih laju alir untuk hidrolik, serta rasio energi spesifik untuk keausan bit."),
        ],
        "kesamaan": "Ketiganya menyerang akar yang sama, yaitu label berbentuk blok status. Persistence menang atas model karena label bertahan panjang, bukan karena fitur lemah.",
        "pembeda": "A1 mengubah bentuk target. A3 mengubah tingkat kepercayaan label. A8 mengubah asal label. Ketiganya dapat dijalankan bersama, tetapi masing-masing cukup untuk menguji hipotesis yang berbeda.",
        "masalah": ["P1", "P3", "P5", "P7"],
        "bok": [14, 11, 5, 10],
        "lapisan": ["L1"],
        "status": "A1 Berjalan, A3 Rencana, A8 Rencana",
        "angka": [
            ("B1 dan TLead stuck K-ii setelah label onset", "B1 0,51 sampai 1,00 dan TLead 10 sampai 11,5 menit pada titik operasi 0,05", "docs/V9_EVAL_B_LAYERB.md:101"),
            ("Hasil negatif label onset pada hyd", "0 dari 3 onset terdeteksi, TLead nol", "docs/V9_EVAL_B_LAYERB.md:103"),
            ("Kontrol-positif label stuck", "0 dari 10", "docs/V8_PM_VERDICT.md:202"),
            ("Kanal sumber label fisika", "GAINLOSSTOT 575 dan 517 berkas, PITTOT 565 dan 506, FLOWOUT 688, FLOWOUTPC 949", "docs/V7_R1_SOLUTIONS.md:37-38"),
            ("Basis label kurasi", "884 kejadian, 50 relevan BHA, total durasi 73.500 menit atau 1.225 jam", "docs/PPT1_LEDGER_ANGKA.md:145, 193"),
        ],
        "dependensi_keluar": [("K4", "Prasyarat. Kalibrasi ambang menyetel keluaran terhadap label, sehingga label yang belum diaudit menghasilkan presisi palsu.", "docs/V4_MAINTENANCE_ML_OPTIONS.md:164")],
        "dependensi_masuk": [("K2", "Penyuplai bukti. Sumur baru menambah jumlah positif yang dipakai audit label.", "docs/V9_PM1_ARCHITECTURE.md:186")],
        "risiko": "Bila klaster ini dipilih sendirian, label menjadi benar tetapi tidak ada titik operasi yang dipakai, sehingga tidak ada keluaran yang bisa dipakai di rig. Perbaikan label tanpa kalibrasi hanya memperbaiki angka evaluasi.",
        "catatan_g1": "Klaster terbesar dengan tiga alternatif. Warna biru.",
    },
    {
        "id": "K2",
        "nama": "Basis bukti dan unit analisis",
        "label_g1": "Basis bukti dan unit analisis",
        "warna": "#059669",
        "prinsip": "Kedua alternatif mengubah jumlah dan satuan bukti, yaitu berapa sumur yang masuk dan satu unit analisis sama dengan apa. Definisi label dan bentuk model tidak diubah.",
        "anggota": ["A2", "A4"],
        "mekanisme": [
            ("A2", "Memparse empat wellbore yang terbukti memiliki kanal disfungsi, lalu menggabungkannya ke kampanye leave-one-well-out sehingga jumlah fold dan jumlah positif naik."),
            ("A4", "Mengganti unit jendela waktu dengan unit stand pengeboran, sehingga prevalensi naik tetapi horizon prediksi melebar menjadi stand berikutnya."),
        ],
        "kesamaan": "Keduanya menyerang underpowering dengan mengubah himpunan atau agregasi sampel, bukan dengan mengubah model atau menurunkan ambang.",
        "pembeda": "A2 menambah observasi independen berupa sumur baru. A4 mengubah resolusi dengan menggabungkan jendela menjadi stand. A2 menaikkan jumlah positif tanpa mengubah arti gate, sedangkan A4 menaikkan prevalensi sekaligus mengubah arti gate.",
        "masalah": ["P2", "P6"],
        "bok": [5, 7, 11, 14],
        "lapisan": ["L1", "L2"],
        "status": "A2 Berjalan, A4 Rencana",
        "angka": [
            ("Kanal disfungsi pada empat wellbore yang belum diparse", "F-10 SHKRSK_RT 188, CRPM_RT 186, STKSLP 125, VIBLAT_RT 66, STUCK_RT 18; F-4 135/135/135/86; F-12 91/90/52/6; F-15 77/76/76/76", "docs/V7_R1_SOLUTIONS.md:45-48"),
            ("Baris CRPM hasil parse", "281.030 / 42.010 / 178.430 / 57.846 baris, re-run 11 fold belum dijalankan", "docs/V9_PM1_ARCHITECTURE.md:186"),
            ("Fold underpowered yang diserang", "F-7 tiga positif, F-9 dua belas positif, F-9_A lift 1,47 gagal tipis", "docs/V9_PM1_ARCHITECTURE.md:186"),
            ("Prevalensi unit stand", "10 sampai 40 persen, berstatus perkiraan desain dan belum dihitung", "docs/V7_R1_SOLUTIONS.md:111"),
            ("Batas stand tanpa akuisisi baru", "Dapat diturunkan dari BPOS dan celah waktu pada CSV yang sudah ada", "docs/V7_R1_SOLUTIONS.md:112"),
        ],
        "dependensi_keluar": [
            ("K1", "Penyuplai bukti. Sumur baru memasok positif untuk audit label dan uji ulang.", "docs/V7_R1_SOLUTIONS.md:43-48"),
            ("K3", "Penyuplai bukti. Jumlah positif per fold menentukan lebar selang estimasi ordinal dan survival.", "docs/V7_R1_SOLUTIONS.md:197"),
        ],
        "dependensi_masuk": [],
        "risiko": "A2 sudah menghasilkan baris data terukur tetapi dampaknya terhadap gate belum terukur karena re-run fold belum dijalankan. A4 berisiko mengubah arti gate secara diam-diam, karena horizon prediksi melebar dari sepuluh menit menjadi stand berikutnya.",
        "catatan_g1": "Dua alternatif. Warna hijau.",
    },
    {
        "id": "K3",
        "nama": "Formulasi model dan evaluasi",
        "label_g1": "Formulasi model dan evaluasi",
        "warna": "#7c3aed",
        "prinsip": "Kedua alternatif mempertahankan himpunan data dan label, lalu mengubah bentuk hipotesis dan cara evaluasinya. Gate biner tetap dihitung pada ambang yang sama.",
        "anggota": ["A5", "A6"],
        "mekanisme": [
            ("A5", "Melatih model pada skala severitas 0 sampai 3, menurunkan keputusan biner pada ambang minimal 1, lalu menambah evaluasi stabilitas fold berupa stratified bootstrap dan pelaporan jumlah positif."),
            ("A6", "Memodelkan waktu sampai peristiwa dengan hazard proporsional, sehingga keluaran berupa risiko per horizon dan sisa umur pakai."),
        ],
        "kesamaan": "Keduanya tidak menyentuh data dan tidak menyentuh label. Yang berubah adalah bentuk keluaran dan cara menguji kestabilannya.",
        "pembeda": "A5 menambah informasi dari label yang sudah ada, yaitu skala severitas, dan menambah rigor evaluasi. A6 mengubah target menjadi waktu, tetapi tidak menambah informasi baru.",
        "masalah": ["P6", "P7", "P9", "P3"],
        "bok": [2, 3, 5, 11],
        "lapisan": ["L2"],
        "status": "A5 Rencana, A6 Rencana",
        "angka": [
            ("Kinerja ssi dan dua fold underpowered", "G1 4 dari 5, G2 5 dari 5, persistence 0 dari 5, F-7 tiga positif, F-9 dua belas positif", "docs/V7_R1_SOLUTIONS.md:197"),
            ("Posisi survival menurut penulis solusi", "Mengubah formulasi tanpa menambah informasi, sehingga diposisikan sebagai opsi pembanding dan bukan solusi primer", "docs/V7_R1_SOLUTIONS.md:152"),
            ("Berkas bhaRun tanpa label keausan fisik", "77 berkas tanpa dullingInfo, dullGrade, maupun bitName", "docs/V4_MAINTENANCE_ML_OPTIONS.md:62"),
            ("Klasifikasi severitas stick-slip sudah mapan", "Sitasi Hegde 2019, doi 10.1016/j.petrol.2019.05.021", "docs/V7_R1_SOLUTIONS.md:197"),
            ("Ambang underpowered", "Fold dengan kurang dari 30 positif dilabeli UNDERPOWERED dan tidak dihitung sebagai mayoritas", "docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md:158"),
        ],
        "dependensi_keluar": [],
        "dependensi_masuk": [
            ("K1", "Prasyarat. Skala 0 sampai 3 dan label waktu hanya bermakna bila semantik label sudah dikunci.", "docs/V4_MAINTENANCE_ML_OPTIONS.md:145"),
            ("K2", "Penyuplai bukti. Jumlah positif menentukan lebar selang.", "docs/V9_PM1_ARCHITECTURE.md:186"),
        ],
        "risiko": "A6 berisiko menjadi pengulangan berbiaya, karena mengubah formulasi tanpa menambah informasi. A5 tidak menambah kelas, sehingga tidak dapat menggantikan A1 atau A2 sebagai perbaikan akar.",
        "catatan_g1": "Dua alternatif. Warna ungu.",
    },
    {
        "id": "K4",
        "nama": "Sinyal fisik dan titik operasi keputusan",
        "label_g1": "Sinyal fisik dan titik operasi",
        "warna": "#b45309",
        "prinsip": "Kedua alternatif bekerja pada sinyal dan pada titik tempat keluaran menyala, yaitu ambang, kalibrasi, purwarupa peringatan, dan urutan prioritas. Definisi label global tidak diubah.",
        "anggota": ["A7", "A9"],
        "mekanisme": [
            ("A7", "Mendeteksi titik perubahan pada sinyal keausan alat bengkel, menambah fitur dekomposisi mode, dan menyiapkan ranking antar status sebagai cadangan bila validasi titik ubah gagal."),
            ("A9", "Mengkalibrasi ambang per sumur, menjalankan purwarupa peringatan dini pada data berlabel, dan menyusun indeks kondisi untuk disfungsi yang labelnya belum tersedia."),
        ],
        "kesamaan": "Keduanya menghasilkan keputusan pada tingkat sinyal, dan keduanya diukur dengan anggaran alarm, bukan dengan AUPRC saja.",
        "pembeda": "Domain berbeda, yaitu bengkel alat pada A7 dan rig pada A9. Status eksekusi juga berbeda, karena A7 sudah memiliki kalibrasi alarm terukur sedangkan A9 belum.",
        "masalah": ["P8", "P1", "P4"],
        "bok": [1, 3, 5, 6, 12, 14],
        "lapisan": ["L3"],
        "status": "A7 Berjalan, A9 Rencana",
        "angka": [
            ("Deteksi titik ubah alat bengkel", "4 dari 4 alat, TLead 20 sampai 36 detik atau 1,8 kali, presisi run 0,50", "docs/V9_EVAL_C_LAYERC.md:98"),
            ("False alarm terkalibrasi per alat", "1 sampai 3 per alat", "docs/V9_EVAL_C_LAYERC.md:98"),
            ("Baseline ranking lintas alat", "AUPRC 0,516 sampai 0,612 atau 1,19 kali, engine Random Forest belum dijalankan", "docs/V9_EVAL_C_LAYERC.md:99"),
            ("Sebaran false alarm antar sumur pada ambang global", "4,15 sampai 496,09 per 24 jam, rasio 119,6 kali", "docs/V9_PM2_VERDICT.md:114"),
            ("Kanal permukaan frekuensi tinggi yang tersedia", "TSPP 52.905 baris pada empat berkas", "docs/V10_D1_BAB_DATA.md:86, 296"),
            ("Kelayakan pemantauan menurut ambang operator", "FAR maksimal 6 per 24 jam, setara satu pemeriksaan driller per empat jam", "docs/V8_R1_ABC_SPEC.md:240"),
            ("Keluaran screening shk saat ini", "FAR 18 sampai 63 per 24 jam pada titik operasi 0,05 sampai 0,10, presisi 0,00 sampai 0,12", "docs/V8_E_shk_CAPABILITY.md:106"),
        ],
        "dependensi_keluar": [],
        "dependensi_masuk": [("K1", "Prasyarat. Kalibrasi ambang tidak sah sebelum label diaudit.", "docs/V4_MAINTENANCE_ML_OPTIONS.md:164")],
        "risiko": "Bila dipilih sebelum label dibereskan, klaster ini menghasilkan alarm yang rapi secara statistik tetapi menunjuk peristiwa yang salah. Bukti pendukungnya sudah ada pada tingkat label, yaitu kontrol-positif 0 dari 10.",
        "kasus_batas": "A7 menyentuh dua klaster. Mekanisme label progresi di dalam A7 membentuk label dari titik ubah, sehingga ia juga menyentuh K1. Penempatan pada K4 memakai mekanisme dominan, yaitu titik operasi dan anggaran alarm, dan hubungan silang ini dinyatakan terbuka, bukan disembunyikan.",
        "catatan_g1": "Dua alternatif. Warna jingga. A7 diberi penanda kasus batas.",
    },
]

RELASI_KLASTER = [
    {
        "dari": "K1",
        "ke": "K4",
        "jenis": "prasyarat",
        "alasan": "Kalibrasi ambang menyetel keluaran terhadap kebenaran label. Bila label salah, hasil kalibrasi berupa presisi palsu.",
        "jejak": "docs/V4_MAINTENANCE_ML_OPTIONS.md:164",
    },
    {
        "dari": "K2",
        "ke": "K1",
        "jenis": "penyuplai bukti",
        "alasan": "Sumur baru memasok jumlah positif yang dipakai untuk mengaudit dan mengunci varian label.",
        "jejak": "docs/V7_R1_SOLUTIONS.md:43-48",
    },
    {
        "dari": "K2",
        "ke": "K3",
        "jenis": "penyuplai bukti",
        "alasan": "Jumlah positif per fold menentukan lebar selang kepercayaan, sehingga menentukan apakah estimasi ordinal dan survival layak dilaporkan.",
        "jejak": "docs/V7_R1_SOLUTIONS.md:197",
    },
    {
        "dari": "K1",
        "ke": "K3",
        "jenis": "prasyarat",
        "alasan": "Skala severitas 0 sampai 3 dan label waktu hanya bermakna bila semantik label sudah dikunci lebih dahulu.",
        "jejak": "docs/V4_MAINTENANCE_ML_OPTIONS.md:145",
    },
]

MATRIKS_KLASTER_BOK = {
    "K1": [14, 11, 5, 10],
    "K2": [5, 7, 11, 14],
    "K3": [2, 3, 5, 11],
    "K4": [1, 3, 5, 6, 12, 14],
}

MATRIKS_KLASTER_MASALAH = {
    "K1": ["P1", "P3", "P5", "P7"],
    "K2": ["P2", "P6"],
    "K3": ["P6", "P7", "P9", "P3"],
    "K4": ["P8", "P1", "P4"],
}

OVERLAY_LAPISAN = {
    "L1": "Data dan label",
    "L2": "Formulasi model dan evaluasi",
    "L3": "Sinyal fisik dan operasi",
}

G1 = {
    "kanvas": {
        "lebar_in": 11.69,
        "tinggi_in": 8.27,
        "dpi": 200,
        "orientasi": "A4 landscape",
        "judul": "Peta Afinitas Sembilan Alternatif Solusi",
    },
    "node_klaster": [
        {"id": "K1", "label": "Target dan mutu label", "warna": "#2563eb", "anggota": ["A1", "A3", "A8"], "ringkas": "Mengubah apa yang dihitung sebagai kejadian atau menguji kebenaran label", "x": 0.5, "y": 3.2},
        {"id": "K2", "label": "Basis bukti dan unit analisis", "warna": "#059669", "anggota": ["A2", "A4"], "ringkas": "Mengubah jumlah sumur dan satuan unit analisis", "x": 6.3, "y": 3.2},
        {"id": "K3", "label": "Formulasi model dan evaluasi", "warna": "#7c3aed", "anggota": ["A5", "A6"], "ringkas": "Mengubah bentuk hipotesis dan rigor evaluasi", "x": 0.5, "y": 6.6},
        {"id": "K4", "label": "Sinyal fisik dan titik operasi", "warna": "#b45309", "anggota": ["A7", "A9"], "ringkas": "Mengubah ambang, kalibrasi, dan urutan prioritas", "x": 6.3, "y": 6.6},
    ],
    "node_alternatif": [
        {"id": "A1", "label": "Onset peristiwa", "klaster": "K1", "status": "Berjalan"},
        {"id": "A3", "label": "Audit mutu label", "klaster": "K1", "status": "Rencana"},
        {"id": "A8", "label": "Label fisika", "klaster": "K1", "status": "Rencana"},
        {"id": "A2", "label": "Perluasan sumur", "klaster": "K2", "status": "Berjalan"},
        {"id": "A4", "label": "Unit per stand", "klaster": "K2", "status": "Rencana"},
        {"id": "A5", "label": "Severity ordinal", "klaster": "K3", "status": "Rencana"},
        {"id": "A6", "label": "Survival dan RUL", "klaster": "K3", "status": "Rencana"},
        {"id": "A7", "label": "Keausan alat bengkel", "klaster": "K4", "status": "Berjalan"},
        {"id": "A9", "label": "Ambang per sumur", "klaster": "K4", "status": "Rencana"},
    ],
    "edge": [
        {"dari": "K1", "ke": "K4", "label": "prasyarat label sebelum kalibrasi", "gaya": "putus-putus"},
        {"dari": "K2", "ke": "K1", "label": "penyuplai positif", "gaya": "putus-putus"},
        {"dari": "K2", "ke": "K3", "label": "penyuplai positif per fold", "gaya": "putus-putus"},
        {"dari": "K1", "ke": "K3", "label": "semantik label sebelum skala", "gaya": "putus-putus"},
    ],
    "legenda": [
        {"simbol": "kotak berwarna", "arti": "klaster, warna berbeda per klaster"},
        {"simbol": "kotak kecil di dalam klaster", "arti": "alternatif solusi beserta kode A1 sampai A9"},
        {"simbol": "teks Berjalan", "arti": "mekanisme inti sudah dieksekusi dan berangka pada kampanye V9"},
        {"simbol": "teks Rencana", "arti": "belum ada artefak eksekusi"},
        {"simbol": "panah putus-putus", "arti": "relasi prasyarat atau penyuplai bukti antar klaster"},
    ],
    "penanda_kasus_batas": {"alternatif": "A7", "teks": "menyentuh K1 lewat label progresi"},
    "catatan_desain": "Empat kolom klaster, sembilan kotak alternatif di dalam kolomnya, dan empat panah putus-putus untuk relasi. Status ditulis sebagai teks karena dokumen ini tidak memakai emoji. Warna klaster mengikuti palet yang sama dengan dokumen, yaitu biru, hijau, ungu, dan jingga.",
}
