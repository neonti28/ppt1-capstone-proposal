"""Data untuk BAB III 3.4 (MCDM pemilihan alternatif solusi).

Berkas ini HANYA berisi data dan jejak. Seluruh perhitungan ada di build_mcdm.py
sehingga angka pada dokumen dan JSON tidak mungkin berbeda.

Status setiap sel wajib salah satu:
  TERUKUR  : nilai berasal dari berkas hasil, JSON, atau hitungan yang bisa diulang
  RUBRIK   : nilai berasal dari rubrik berjangkar yang tingkatnya menunjuk keadaan proyek
  ASUMSI   : nilai belum terukur dan ditulis apa adanya sebagai asumsi
"""

DOK = "docs/PPT1_BAB3_4_MCDM.md"
JSON_OUT = "scratch/ppt1/mcdm.json"

# ---------------------------------------------------------------------------
# 1. KRITERIA (identik dengan C1-C8 pada 3.3, tanpa perubahan definisi)
# ---------------------------------------------------------------------------
KRITERIA = [
    {
        "id": "C1",
        "nama": "Efektivitas deteksi pada gate yang sudah dikunci",
        "arah": "benefit",
        "satuan": "lift dalam kali dan AUPRC",
        "peringkat": 1,
        "alasan_peringkat": (
            "Gate G1 dan G2 adalah definisi operasional lulus, sehingga kriteria ini "
            "mengukur apakah alternatif bekerja sama sekali. Rubrik 4.1 menuntut pemilihan "
            "memakai performance metrics yang ditetapkan lebih dahulu, dan U1 sebagai "
            "pemilik masalah utama bergantung pada C1."
        ),
        "jejak_peringkat": "docs/V7_R1_SOLUTIONS.md:233; docs/PPT1_BAB3_2.md:466",
        "fungsi_nilai": "rubrik 4 tingkat: 100 gate lolos, 75 dieksekusi dan delta terukur positif, 40 dieksekusi tanpa delta positif, 20 belum dieksekusi",
        "status": "TERUKUR untuk alternatif yang sudah dieksekusi, RUBRIK untuk sisanya",
    },
    {
        "id": "C4",
        "nama": "Kepatuhan mode advisory tanpa alarm otomatis",
        "arah": "benefit",
        "satuan": "jumlah slot alarm otomatis, target nol, dan jumlah head dengan review manusia",
        "peringkat": 2,
        "alasan_peringkat": (
            "Batasan B2 bersifat keras karena pelanggarannya membuat alat tidak boleh dipakai, "
            "bukan sekadar menurunkan skor. Tiga user story bergantung pada kriteria ini, "
            "yaitu U2, U4, dan U6, jumlah terbanyak di antara delapan kriteria."
        ),
        "jejak_peringkat": "scratch/ppt1/affinity.json kunci batasan id B2 dan kunci matriks_us_kriteria",
        "fungsi_nilai": "100 bila slot alarm otomatis nol, 0 bila ada satu saja",
        "status": "TERUKUR",
    },
    {
        "id": "C2",
        "nama": "Kecukupan bukti per fold",
        "arah": "benefit",
        "satuan": "jumlah fold teruji dan jumlah positif per fold",
        "peringkat": 3,
        "alasan_peringkat": (
            "Batasan B4 menetapkan label dibereskan lebih dahulu, dan aturan kampanye menyatakan "
            "fold dengan kurang dari 30 positif berstatus underpowered sehingga tidak boleh "
            "dihitung sebagai mayoritas. Dua user story bergantung pada C2, yaitu U1 dan U5."
        ),
        "jejak_peringkat": "docs/V7_R1_SOLUTIONS.md:97, 233; scratch/ppt1/affinity.json kunci batasan id B4",
        "fungsi_nilai": "100 x jumlah fold layak dibagi 18, dibatasi 100",
        "status": "TERUKUR",
    },
    {
        "id": "C7",
        "nama": "Ketertelusuran dan reproduksibilitas angka",
        "arah": "benefit",
        "satuan": "jumlah klaim tanpa jejak, target nol",
        "peringkat": 4,
        "alasan_peringkat": (
            "Tiga user story bergantung pada C7, yaitu U4, U5, dan U6. Batasan B1 menuntut seluruh "
            "angka dapat diaudit pihak lain, dan rubrik 3.2 menuntut batasan standar yang "
            "dijelaskan dengan justifikasi kuat."
        ),
        "jejak_peringkat": "scratch/ppt1/affinity.json kunci matriks_us_kriteria; docs/PPT1_BAB3_2.md:472",
        "fungsi_nilai": "100 x jumlah klaim berjejak dibagi jumlah klaim",
        "status": "TERUKUR",
    },
    {
        "id": "C3",
        "nama": "Portabilitas antar sumur",
        "arah": "benefit",
        "satuan": "rasio false alarm rate maksimum dibagi minimum per 24 jam",
        "peringkat": 5,
        "alasan_peringkat": (
            "Sebaran false alarm rate terukur 4,15 sampai 496,09 per 24 jam pada titik operasi "
            "yang sama, yaitu rasio 119,6 kali, sehingga satu ambang global tidak portabel. "
            "Dua user story bergantung pada C3, yaitu U1 dan U2."
        ),
        "jejak_peringkat": "docs/V9_PM2_VERDICT.md:114",
        "fungsi_nilai": "rubrik 3 tingkat: 100 kalibrasi per sumur sudah diuji pada dua sumur atau lebih, 60 menambah sumur uji atau memuat rancangan kalibrasi yang belum diuji, 30 tidak menyentuh portabilitas",
        "status": "TERUKUR untuk gejala, RUBRIK untuk tindakan alternatif",
    },
    {
        "id": "C6",
        "nama": "Waktu penyelesaian dalam satu semester",
        "arah": "cost",
        "satuan": "minggu kerja",
        "peringkat": 6,
        "alasan_peringkat": (
            "Batasan B3 bersifat keras karena jadwal Tabel 3.1 mengikat seluruh tim, namun "
            "kriteria ini berlaku hampir sama untuk semua alternatif sehingga daya bedanya "
            "rendah. Tidak ada user story yang bergantung padanya, sehingga peringkatnya "
            "tidak boleh lebih tinggi daripada kriteria yang punya pemangku kepentingan."
        ),
        "jejak_peringkat": "scratch/ppt1/affinity.json kunci batasan id B3; Buku Pedoman PPT Tahap I Tabel 3.1 halaman 32",
        "fungsi_nilai": "100 x (9 dikurangi minggu kerja) dibagi 9, dibatasi 0 sampai 100",
        "status": "ASUMSI untuk minggu kerja per alternatif, BAKU untuk tenggat",
    },
    {
        "id": "C5",
        "nama": "Kebutuhan akuisisi data baru",
        "arah": "cost",
        "satuan": "jumlah wellbore atau berkas yang harus diproses",
        "peringkat": 7,
        "alasan_peringkat": (
            "Biaya data bersifat instrumental karena hanya bermakna lewat kriteria lain. "
            "Satu user story bergantung padanya, yaitu U3, dan sebagian besar kebutuhan parse "
            "sudah dikerjakan pada kampanye V9 sehingga daya bedanya menyusut."
        ),
        "jejak_peringkat": "docs/V7_R1_SOLUTIONS.md:76, 106, 145; docs/V9_PM1_ARCHITECTURE.md:186",
        "fungsi_nilai": "100 dibagi (1 + jumlah wellbore tersisa)",
        "status": "TERUKUR",
    },
    {
        "id": "C8",
        "nama": "Beban kognitif keluaran",
        "arah": "benefit",
        "satuan": "rubrik tiga tingkat",
        "peringkat": 8,
        "alasan_peringkat": (
            "Hanya satu user story yang bergantung padanya, yaitu U2, dan rubriknya belum "
            "divalidasi mitra sehingga statusnya masih asumsi. Peringkat terakhir bukan berarti "
            "kriteria ini tidak penting, melainkan menandakan bukti pendukungnya paling lemah "
            "di antara delapan kriteria."
        ),
        "jejak_peringkat": "scratch/ppt1/affinity.json kunci kriteria id C8; docs/PPT1_BAB3_2.md:473",
        "fungsi_nilai": "tingkat 3 menjadi 100, tingkat 2 menjadi 50, tingkat 1 menjadi 0",
        "status": "ASUMSI",
    },
]

# Peringkat 1 sampai 8 dipakai untuk menurunkan bobot kardinal dengan
# Rank-Order Centroid (ROC). ROC dipilih karena sumber daya yang ada hanya
# memberi urutan prioritas, bukan perbandingan berpasangan, sehingga tidak ada
# angka yang perlu dikarang.
BOBOT_METODE = "Rank-Order Centroid (ROC) atas peringkat kriteria"

# ---------------------------------------------------------------------------
# 2. MATRIKS KEPUTUSAN
# Setiap sel: nilai baku (yang masuk hitungan), unit mentah (yang bisa
# diperiksa di berkas), status, dasar, jejak.
# ---------------------------------------------------------------------------
ALTERNATIF = [
    ("A1", "Relabeling onset peristiwa: dari status menjadi kejadian"),
    ("A2", "Perluasan wellbore berkanal disfungsi F-10, F-4, F-12, F-15"),
    ("A3", "Penjaminan mutu label dan label probabilistik multi-sumber"),
    ("A4", "Unit analisis per-stand pengeboran"),
    ("A5", "Prediksi severity ordinal dengan evaluasi stabilitas fold"),
    ("A6", "Formulasi survival dan sisa umur pakai"),
    ("A7", "Penguatan kampanye keausan alat bengkel"),
    ("A8", "Label fisika pengganti label proksi"),
    ("A9", "Lapisan keputusan operasional: kalibrasi ambang per sumur dan purwarupa peringatan dini"),
]

# unit mentah per (alternatif, kriteria). Kunci nilai baku dihitung skrip
# dari unit mentah memakai fungsi nilai pada KRITERIA.
SEL = [
    # ---------------- A1 ----------------
    {"alt": "A1", "c": "C1", "unit": "L75", "status": "TERUKUR",
     "dasar": "Mekanisme sudah dieksekusi untuk stuck dan hyd. Stuck memberi B1 0,51 sampai 1,00 dengan TLead 10 sampai 11,5 menit. Hyd memberi B1 nol dari tiga onset, jadi hasil negatifnya terukur.",
     "jejak": "docs/V9_EVAL_B_LAYERB.md:101, 103"},
    {"alt": "A1", "c": "C2", "unit": 13, "status": "TERUKUR",
     "dasar": "Tiga kelas sasaran dengan fold layak terukur: stuck 2 fold, hyd 7 fold, bit_wear 4 fold.",
     "jejak": "docs/V7_R1_SOLUTIONS.md:69, 127, 203"},
    {"alt": "A1", "c": "C3", "unit": "L30", "status": "RUBRIK",
     "dasar": "Relabel mengubah definisi target, bukan ambang. Kalibrasi per sumur tidak termasuk lingkup, sehingga gejala 119,6 kali tetap tidak tersentuh.",
     "jejak": "docs/V9_PM2_VERDICT.md:114"},
    {"alt": "A1", "c": "C4", "unit": 0, "status": "TERUKUR",
     "dasar": "Keluaran berupa peringatan berpengawas manusia. Registry mencatat nol slot alarm otomatis.",
     "jejak": "scratch/v9_i1/v9_i1_RESULTS.json kunci auto_critical_alarm_slots"},
    {"alt": "A1", "c": "C5", "unit": 0, "status": "TERUKUR",
     "dasar": "Relabel tidak memerlukan parse baru karena deret sumber sudah berbentuk CSV.",
     "jejak": "docs/V7_R1_SOLUTIONS.md:76"},
    {"alt": "A1", "c": "C6", "unit": 2, "status": "ASUMSI",
     "dasar": "Beban dinilai rendah pada V7 bagian 7 karena relabel dan run ulang tanpa parse. Dua minggu adalah asumsi perkiraan desain.",
     "jejak": "docs/V7_R1_SOLUTIONS.md:215"},
    {"alt": "A1", "c": "C7", "unit": [3, 3], "status": "TERUKUR",
     "dasar": "Tiga dari tiga butir bukti pada 3.1.4.1 membawa jejak berkas dan baris.",
     "jejak": "scratch/ppt1/alternatif.json alternatif id A1 kunci bukti"},
    {"alt": "A1", "c": "C8", "unit": 3, "status": "RUBRIK",
     "dasar": "Keluaran satu peringatan per onset dengan waktu, keyakinan, dan tindakan yang disarankan. Tingkat 3 pada rubrik 3.3.",
     "jejak": "scratch/ppt1/affinity.json kunci kriteria id C8"},

    # ---------------- A2 ----------------
    {"alt": "A2", "c": "C1", "unit": "L20", "status": "TERUKUR",
     "dasar": "Parse empat wellbore selesai dan terukur, namun evaluasi ulang fold belum dijalankan sehingga dampak ke gate belum dapat diklaim.",
     "jejak": "docs/V9_PM1_ARCHITECTURE.md:186; docs/PPT1_BAB3_1.md:103"},
    {"alt": "A2", "c": "C2", "unit": 18, "status": "TERUKUR",
     "dasar": "Empat kelas sasaran dengan fold layak terukur: shk 7, ssi 5, vib 4, stuck 2.",
     "jejak": "docs/V7_R1_SOLUTIONS.md:97, 197, 55, 69"},
    {"alt": "A2", "c": "C3", "unit": "L60", "status": "RUBRIK",
     "dasar": "Menambah empat sumur uji sehingga portabilitas diuji pada jumlah sumur lebih banyak, tanpa memuat kalibrasi ambang per sumur.",
     "jejak": "docs/V7_R1_SOLUTIONS.md:43-48"},
    {"alt": "A2", "c": "C4", "unit": 0, "status": "TERUKUR",
     "dasar": "Tidak menambah slot alarm otomatis karena hanya menambah data, bukan keluaran baru.",
     "jejak": "scratch/v9_i1/v9_i1_RESULTS.json kunci auto_critical_alarm_slots"},
    {"alt": "A2", "c": "C5", "unit": 3, "status": "TERUKUR",
     "dasar": "Jalur CRPM sudah diparse pada empat wellbore dengan baris terukur, namun jalur VIBLAT untuk F-4, F-10, dan F-15 masih berstatus belum diparse, sehingga tiga wellbore tersisa untuk kelas vib.",
     "jejak": "docs/V9_PM1_ARCHITECTURE.md:186, 169"},
    {"alt": "A2", "c": "C6", "unit": 2, "status": "ASUMSI",
     "dasar": "Sisa pekerjaan hanya evaluasi ulang fold karena parse selesai. Dua minggu adalah asumsi perkiraan desain.",
     "jejak": "docs/PPT1_BAB3_1.md:103"},
    {"alt": "A2", "c": "C7", "unit": [3, 3], "status": "TERUKUR",
     "dasar": "Tiga dari tiga butir bukti pada 3.1.4.2 membawa jejak berkas dan baris.",
     "jejak": "scratch/ppt1/alternatif.json alternatif id A2 kunci bukti"},
    {"alt": "A2", "c": "C8", "unit": 2, "status": "RUBRIK",
     "dasar": "Tidak menghasilkan bentuk keluaran sendiri. Beban kognitif mengikuti alternatif yang memakai datanya, sehingga dinilai netral pada tingkat 2.",
     "jejak": "scratch/ppt1/affinity.json kunci kriteria id C8"},

    # ---------------- A3 ----------------
    {"alt": "A3", "c": "C1", "unit": "L20", "status": "TERUKUR",
     "dasar": "Belum dieksekusi. Cacat label yang diserang sudah terukur, yaitu kontrol-positif stuck nol dari sepuluh.",
     "jejak": "docs/V8_PM_VERDICT.md:202; docs/PPT1_BAB3_1.md:51"},
    {"alt": "A3", "c": "C2", "unit": 9, "status": "TERUKUR",
     "dasar": "Dua kelas sasaran dengan fold layak terukur: stuck 2 fold dan hyd 7 fold.",
     "jejak": "docs/V7_R1_SOLUTIONS.md:69, 127"},
    {"alt": "A3", "c": "C3", "unit": "L30", "status": "RUBRIK",
     "dasar": "Audit semantik label lintas sumur menyentuh konsistensi antar sumur, namun tidak menetapkan kalibrasi ambang per sumur.",
     "jejak": "docs/V9_PM2_VERDICT.md:114"},
    {"alt": "A3", "c": "C4", "unit": 0, "status": "TERUKUR",
     "dasar": "Bekerja pada mutu label, tidak menerbitkan alarm.",
     "jejak": "scratch/v9_i1/v9_i1_RESULTS.json kunci auto_critical_alarm_slots"},
    {"alt": "A3", "c": "C5", "unit": 0, "status": "TERUKUR",
     "dasar": "Memakai label kurasi dan CSV yang sudah ada, tanpa parse baru.",
     "jejak": "docs/V7_R1_SOLUTIONS.md:88"},
    {"alt": "A3", "c": "C6", "unit": 4, "status": "ASUMSI",
     "dasar": "Dua tahap berurutan, audit label lalu label probabilistik. Empat minggu adalah asumsi perkiraan desain.",
     "jejak": "docs/V7_R1_SOLUTIONS.md:89"},
    {"alt": "A3", "c": "C7", "unit": [3, 3], "status": "TERUKUR",
     "dasar": "Tiga dari tiga butir bukti pada 3.1.4.3 membawa jejak berkas dan baris.",
     "jejak": "scratch/ppt1/alternatif.json alternatif id A3 kunci bukti"},
    {"alt": "A3", "c": "C8", "unit": 2, "status": "RUBRIK",
     "dasar": "Keluaran berupa label, bukan peringatan operator. Beban kognitif operator tidak berubah, sehingga dinilai netral pada tingkat 2.",
     "jejak": "scratch/ppt1/affinity.json kunci kriteria id C8"},

    # ---------------- A4 ----------------
    {"alt": "A4", "c": "C1", "unit": "L20", "status": "TERUKUR",
     "dasar": "Belum dieksekusi. Akar yang diserang terukur, yaitu dua fold underpowered pada ssi dengan 3 dan 12 positif.",
     "jejak": "docs/V7_R1_SOLUTIONS.md:197; docs/PPT1_BAB3_1.md:52"},
    {"alt": "A4", "c": "C2", "unit": 12, "status": "TERUKUR",
     "dasar": "Dua kelas sasaran dengan fold layak terukur: shk 7 fold dan ssi 5 fold.",
     "jejak": "docs/V7_R1_SOLUTIONS.md:97, 197"},
    {"alt": "A4", "c": "C3", "unit": "L30", "status": "RUBRIK",
     "dasar": "Perubahan unit analisis tidak menetapkan kalibrasi ambang per sumur.",
     "jejak": "docs/V9_PM2_VERDICT.md:114"},
    {"alt": "A4", "c": "C4", "unit": 0, "status": "TERUKUR",
     "dasar": "Tidak menerbitkan alarm otomatis.",
     "jejak": "scratch/v9_i1/v9_i1_RESULTS.json kunci auto_critical_alarm_slots"},
    {"alt": "A4", "c": "C5", "unit": 0, "status": "TERUKUR",
     "dasar": "Memakai CSV terparse dan batas stand yang diturunkan dari kolom yang sudah ada.",
     "jejak": "docs/V7_R1_SOLUTIONS.md:112"},
    {"alt": "A4", "c": "C6", "unit": 3, "status": "ASUMSI",
     "dasar": "Beban rendah sampai sedang pada V7 bagian 7. Tiga minggu adalah asumsi perkiraan desain.",
     "jejak": "docs/V7_R1_SOLUTIONS.md:222"},
    {"alt": "A4", "c": "C7", "unit": [3, 3], "status": "TERUKUR",
     "dasar": "Tiga dari tiga butir bukti pada 3.1.4.4 membawa jejak berkas dan baris.",
     "jejak": "scratch/ppt1/alternatif.json alternatif id A4 kunci bukti"},
    {"alt": "A4", "c": "C8", "unit": 2, "status": "RUBRIK",
     "dasar": "Unit stand memperlebar horizon prediksi menjadi stand berikutnya, sehingga keluaran menjadi daftar kandidat tanpa urutan. Tingkat 2 pada rubrik 3.3.",
     "jejak": "docs/V7_R1_SOLUTIONS.md:113"},

    # ---------------- A5 ----------------
    {"alt": "A5", "c": "C1", "unit": "L20", "status": "TERUKUR",
     "dasar": "Belum dieksekusi. Akar yang diserang terukur, yaitu varians AUPRC pada fold dengan 30 sampai 41 positif.",
     "jejak": "docs/V7_R1_SOLUTIONS.md:99; docs/PPT1_BAB3_1.md:53"},
    {"alt": "A5", "c": "C2", "unit": 9, "status": "TERUKUR",
     "dasar": "Dua kelas sasaran dengan fold layak terukur: ssi 5 fold dan bit_wear 4 fold.",
     "jejak": "docs/V7_R1_SOLUTIONS.md:197, 203"},
    {"alt": "A5", "c": "C3", "unit": "L30", "status": "RUBRIK",
     "dasar": "Formulasi ordinal tidak menetapkan kalibrasi ambang per sumur.",
     "jejak": "docs/V9_PM2_VERDICT.md:114"},
    {"alt": "A5", "c": "C4", "unit": 0, "status": "TERUKUR",
     "dasar": "Tidak menerbitkan alarm otomatis.",
     "jejak": "scratch/v9_i1/v9_i1_RESULTS.json kunci auto_critical_alarm_slots"},
    {"alt": "A5", "c": "C5", "unit": 0, "status": "TERUKUR",
     "dasar": "Kanal sudah tersedia di CSV sehingga tidak ada parse baru.",
     "jejak": "docs/V7_R1_SOLUTIONS.md:118"},
    {"alt": "A5", "c": "C6", "unit": 2, "status": "ASUMSI",
     "dasar": "Beban rendah pada V7 bagian 7. Dua minggu adalah asumsi perkiraan desain.",
     "jejak": "docs/V7_R1_SOLUTIONS.md:222"},
    {"alt": "A5", "c": "C7", "unit": [3, 3], "status": "TERUKUR",
     "dasar": "Tiga dari tiga butir bukti pada 3.1.4.5 membawa jejak berkas dan baris.",
     "jejak": "scratch/ppt1/alternatif.json alternatif id A5 kunci bukti"},
    {"alt": "A5", "c": "C8", "unit": 2, "status": "RUBRIK",
     "dasar": "Keluaran berupa tingkat severitas tanpa urutan prioritas tindakan. Tingkat 2 pada rubrik 3.3.",
     "jejak": "docs/V7_R1_SOLUTIONS.md:117"},

    # ---------------- A6 ----------------
    {"alt": "A6", "c": "C1", "unit": "L20", "status": "TERUKUR",
     "dasar": "Belum dieksekusi. Hasil negatif pada hyd sudah terukur, yaitu B1 nol dari tiga onset, sehingga formulasi survival tidak punya sinyal pendukung pada kelas itu.",
     "jejak": "docs/V9_EVAL_B_LAYERB.md:103; docs/PPT1_BAB3_1.md:54"},
    {"alt": "A6", "c": "C2", "unit": 11, "status": "TERUKUR",
     "dasar": "Dua kelas sasaran dengan fold layak terukur: hyd 7 fold dan bit_wear 4 fold.",
     "jejak": "docs/V7_R1_SOLUTIONS.md:127, 203"},
    {"alt": "A6", "c": "C3", "unit": "L30", "status": "RUBRIK",
     "dasar": "Survival mengubah formulasi, bukan ambang, sehingga gejala 119,6 kali tidak tersentuh.",
     "jejak": "docs/V9_PM2_VERDICT.md:114"},
    {"alt": "A6", "c": "C4", "unit": 0, "status": "TERUKUR",
     "dasar": "Skor risiko per horizon tetap advisory, tanpa alarm otomatis.",
     "jejak": "scratch/v9_i1/v9_i1_RESULTS.json kunci auto_critical_alarm_slots"},
    {"alt": "A6", "c": "C5", "unit": 0, "status": "TERUKUR",
     "dasar": "Diturunkan dari label yang sudah ada, tanpa parse baru.",
     "jejak": "docs/V7_R1_SOLUTIONS.md:151"},
    {"alt": "A6", "c": "C6", "unit": 4, "status": "ASUMSI",
     "dasar": "Beban sedang pada V7 bagian 7. Empat minggu adalah asumsi perkiraan desain.",
     "jejak": "docs/V7_R1_SOLUTIONS.md:222"},
    {"alt": "A6", "c": "C7", "unit": [3, 3], "status": "TERUKUR",
     "dasar": "Tiga dari tiga butir bukti pada 3.1.4.6 membawa jejak berkas dan baris.",
     "jejak": "scratch/ppt1/alternatif.json alternatif id A6 kunci bukti"},
    {"alt": "A6", "c": "C8", "unit": 2, "status": "RUBRIK",
     "dasar": "Keluaran berupa hazard atau sisa umur yang masih perlu ditafsirkan pengguna. Tingkat 2 pada rubrik 3.3.",
     "jejak": "docs/V7_R1_SOLUTIONS.md:150"},

    # ---------------- A7 ----------------
    {"alt": "A7", "c": "C1", "unit": "L75", "status": "TERUKUR",
     "dasar": "Mekanisme progresi sudah dijalankan pada empat dari empat alat dengan TLead 20 sampai 36 detik dan false alarm terkalibrasi 1 sampai 3 per alat, sehingga delta terukur positif, namun gate G1 tetap nol dari empat dan presisi run hanya 0,50 sehingga makna delta terbatas.",
     "jejak": "docs/V9_EVAL_C_LAYERC.md:98; docs/V7_R1_SOLUTIONS.md:160"},
    {"alt": "A7", "c": "C2", "unit": 4, "status": "TERUKUR",
     "dasar": "Satu domain sasaran dengan empat fold alat terukur.",
     "jejak": "docs/V7_R1_SOLUTIONS.md:160"},
    {"alt": "A7", "c": "C3", "unit": "L30", "status": "RUBRIK",
     "dasar": "Domain bengkel memakai empat alat dan bukan sumur, sehingga kalibrasi per sumur tidak berlaku dan tidak dirancang.",
     "jejak": "scratch/ppt1/affinity.json kunci batasan id B5"},
    {"alt": "A7", "c": "C4", "unit": 0, "status": "TERUKUR",
     "dasar": "Keluaran berupa status dan tren alat, tanpa alarm otomatis.",
     "jejak": "scratch/v9_i1/v9_i1_RESULTS.json kunci auto_critical_alarm_slots"},
    {"alt": "A7", "c": "C5", "unit": 0, "status": "TERUKUR",
     "dasar": "Delapan berkas akselerometer sudah tersedia dan terverifikasi SHA-256, tanpa parse baru.",
     "jejak": "docs/V7_R1_SOLUTIONS.md:170"},
    {"alt": "A7", "c": "C6", "unit": 5, "status": "ASUMSI",
     "dasar": "Pengembangan baru berskala sedang sampai besar karena dekomposisi mode dan ranking ditambahkan. Lima minggu adalah asumsi perkiraan desain.",
     "jejak": "docs/V7_R1_SOLUTIONS.md:219; scratch/ppt1/affinity.json kunci batasan id B3"},
    {"alt": "A7", "c": "C7", "unit": [4, 4], "status": "TERUKUR",
     "dasar": "Empat dari empat butir bukti pada 3.1.4.7 membawa jejak berkas dan baris.",
     "jejak": "scratch/ppt1/alternatif.json alternatif id A7 kunci bukti"},
    {"alt": "A7", "c": "C8", "unit": 2, "status": "RUBRIK",
     "dasar": "Keluaran berupa peringkat alat yang masih perlu dibaca sebagai daftar. Tingkat 2 pada rubrik 3.3.",
     "jejak": "docs/V7_R1_SOLUTIONS.md:185"},

    # ---------------- A8 ----------------
    {"alt": "A8", "c": "C1", "unit": "L20", "status": "TERUKUR",
     "dasar": "Belum dieksekusi. Akar yang diserang terukur, yaitu label hyd masih proksi residual SPPA dan label keausan fisik tidak tersedia.",
     "jejak": "docs/V8_PM_VERDICT.md:202; docs/V4_MAINTENANCE_ML_OPTIONS.md:62"},
    {"alt": "A8", "c": "C2", "unit": 11, "status": "TERUKUR",
     "dasar": "Dua kelas sasaran dengan fold layak terukur: hyd 7 fold dan bit_wear 4 fold.",
     "jejak": "docs/V7_R1_SOLUTIONS.md:127, 203"},
    {"alt": "A8", "c": "C3", "unit": "L60", "status": "RUBRIK",
     "dasar": "Parse kanal pit dan flow pada F-9 serta F-1 C dan F-11 menambah sumur uji, tanpa rancangan kalibrasi ambang per sumur.",
     "jejak": "docs/V7_R1_SOLUTIONS.md:145"},
    {"alt": "A8", "c": "C4", "unit": 0, "status": "TERUKUR",
     "dasar": "Label fisika dipakai sebagai label pelatihan, bukan alarm otomatis, sehingga batasan B2 tetap terpenuhi.",
     "jejak": "scratch/ppt1/affinity.json kunci batasan id B2"},
    {"alt": "A8", "c": "C5", "unit": 2, "status": "TERUKUR",
     "dasar": "Dua sumur memerlukan parse tambahan, yaitu kanal pit mentah F-9 dan F-1 C atau F-11.",
     "jejak": "docs/V7_R1_SOLUTIONS.md:145"},
    {"alt": "A8", "c": "C6", "unit": 5, "status": "ASUMSI",
     "dasar": "Beban rendah untuk label MSE dan DS ditambah beban sedang sampai besar untuk parse pit dan flow. Lima minggu adalah asumsi perkiraan desain.",
     "jejak": "docs/V7_R1_SOLUTIONS.md:146, 183"},
    {"alt": "A8", "c": "C7", "unit": [3, 3], "status": "TERUKUR",
     "dasar": "Tiga dari tiga butir bukti pada 3.1.4.8 membawa jejak berkas dan baris.",
     "jejak": "scratch/ppt1/alternatif.json alternatif id A8 kunci bukti"},
    {"alt": "A8", "c": "C8", "unit": 2, "status": "RUBRIK",
     "dasar": "Mengubah sumber label tanpa mengubah bentuk keluaran, sehingga beban kognitif operator dinilai netral pada tingkat 2.",
     "jejak": "scratch/ppt1/affinity.json kunci kriteria id C8"},

    # ---------------- A9 ----------------
    {"alt": "A9", "c": "C1", "unit": "L20", "status": "TERUKUR",
     "dasar": "Belum dieksekusi. Gejala yang diserang terukur, yaitu sebaran false alarm 4,15 sampai 496,09 per 24 jam.",
     "jejak": "docs/V9_PM2_VERDICT.md:114; docs/PPT1_BAB3_1.md:57"},
    {"alt": "A9", "c": "C2", "unit": 6, "status": "TERUKUR",
     "dasar": "Dua kelas sasaran dengan fold layak terukur: vib 4 fold dan stuck 2 fold.",
     "jejak": "docs/V7_R1_SOLUTIONS.md:55, 69"},
    {"alt": "A9", "c": "C3", "unit": "L60", "status": "RUBRIK",
     "dasar": "Memuat rancangan kalibrasi ambang per sumur sebagai inti pekerjaan, namun belum diuji pada dua sumur atau lebih.",
     "jejak": "docs/V9_PM2_VERDICT.md:114; docs/PPT1_BAB3_1.md:57"},
    {"alt": "A9", "c": "C4", "unit": 0, "status": "TERUKUR",
     "dasar": "Purwarupa peringatan dini tetap advisory dengan review manusia, sesuai batasan B2.",
     "jejak": "scratch/v9_i1/v9_i1_RESULTS.json kunci auto_critical_alarm_slots"},
    {"alt": "A9", "c": "C5", "unit": 0, "status": "TERUKUR",
     "dasar": "Memakai registry head dan CSV yang sudah ada, tanpa parse baru.",
     "jejak": "docs/V4_MAINTENANCE_ML_OPTIONS.md:58"},
    {"alt": "A9", "c": "C6", "unit": 4, "status": "ASUMSI",
     "dasar": "Kalibrasi ambang ditambah purwarupa peringatan. Empat minggu adalah asumsi perkiraan desain.",
     "jejak": "scratch/ppt1/affinity.json kunci batasan id B3"},
    {"alt": "A9", "c": "C7", "unit": [4, 4], "status": "TERUKUR",
     "dasar": "Empat dari empat butir bukti pada 3.1.4.9 membawa jejak berkas dan baris, termasuk kunci JSON registry.",
     "jejak": "scratch/ppt1/alternatif.json alternatif id A9 kunci bukti"},
    {"alt": "A9", "c": "C8", "unit": 3, "status": "RUBRIK",
     "dasar": "Rancangan keluaran berupa satu baris peringatan dengan waktu, keyakinan, dan tindakan, serta frekuensi pemeriksaan satu kali per empat jam. Tingkat 3 pada rubrik 3.3.",
     "jejak": "docs/V8_R1_ABC_SPEC.md:240; docs/PPT1_BAB3_2.md:471"},
]

# ---------------------------------------------------------------------------
# 3. FUNGSI NILAI (dipakai untuk menghitung nilai baku dari unit mentah)
# ---------------------------------------------------------------------------
AMBANG_FOLD = 18      # jumlah fold layak terbesar pada satu alternatif (A2), dipakai sebagai titik jenuh
MINGGU_TERSEDIA = 9   # asumsi: 25 Oktober 2026 sampai akhir Desember 2026, presentasi akhir Desember minggu ke-4
RUBRIK_C1 = {"L100": 100, "L75": 75, "L40": 40, "L20": 20}
RUBRIK_C3 = {"L100": 100, "L60": 60, "L30": 30}
RUBRIK_C8 = {3: 100, 2: 50, 1: 0}

# ---------------------------------------------------------------------------
# 4. SKENARIO BOBOT (uji sensitivitas)
# P0 dasar ROC, P1 bobot sama, P2 gate dominan, P3 label dahulu,
# P4 kelayakan dahulu, P5 konvensi skor netral (matriks berubah, bobot tetap).
# ---------------------------------------------------------------------------
SKENARIO = [
    {"id": "P0", "nama": "Dasar, ROC atas peringkat", "jenis": "bobot", "catatan": "Peringkat 1 sampai 8 diturunkan dari aturan R1 sampai R8 pada 3.4.4, lalu diubah menjadi bobot dengan Rank-Order Centroid."},
    {"id": "P1", "nama": "Bobot sama", "jenis": "bobot", "catatan": "Delapan kriteria berbobot 0,125. Menguji apakah hasil bergantung pada penurunan ROC."},
    {"id": "P2", "nama": "Gate dominan", "jenis": "bobot", "catatan": "C1 ditetapkan 0,55 dan sisanya dibagi proporsional dari bobot dasar. Menguji pembacaan paling ketat terhadap gate G1 dan G2."},
    {"id": "P3", "nama": "Label dahulu", "jenis": "bobot", "catatan": "C2 ditetapkan 0,35 dan C7 0,25, sisanya proporsional. Menguji pembacaan V8_PM_VERDICT:202 yang menaruh mutu label sebagai prasyarat."},
    {"id": "P4", "nama": "Kelayakan dahulu", "jenis": "bobot", "catatan": "C5 ditetapkan 0,30 dan C6 0,30, sisanya proporsional. Menguji pembacaan yang mengutamakan selesai dalam satu semester."},
    {"id": "P5", "nama": "Konvensi skor netral", "jenis": "skor", "catatan": "Bobot kembali ke ROC, tetapi alternatif yang belum dieksekusi diberi nilai C1 50 dan A7 60, sehingga penalti bukti dihapus."},
    {"id": "P6", "nama": "Tanpa kriteria penyaring", "jenis": "bobot", "catatan": "C4 dan C7 diberi bobot nol karena kolomnya tidak membedakan, lalu enam kriteria yang tersisa dinormalkan ulang. Menguji apakah keputusan berubah bila kriteria penyaring dipakai sebagai saringan lulus atau gagal, bukan sebagai bobot."},
    {"id": "P7", "nama": "Beban kognitif dinolkan", "jenis": "bobot", "catatan": "C8 diberi bobot nol. Alasannya terbuka: subbab 3.3.6 butir 8 menyatakan antarmuka peringatan belum dirancang, sehingga C8 pada kartu ini berstatus niat desain, bukan hasil uji. Skenario ini membuktikan keputusan tidak bergantung pada kriteria yang belum divalidasi."},
    {"id": "P8", "nama": "Portabilitas dominan", "jenis": "bobot", "catatan": "C3 ditetapkan 0,30 dan sisanya dibagi proporsional. Menguji pembacaan yang menempatkan ketidakportabelan ambang, yaitu sebaran 4,15 sampai 496,09 per 24 jam, sebagai masalah utama sebagaimana dinyatakan pada V9_PM2_VERDICT.md:114."},
]

# ---------------------------------------------------------------------------
# 4b. BUKTI TERUKUR PER KELAS SASARAN
# Angka di bawah ini adalah jangkar rubrik C1, bukan hiasan. Setiap baris
# menunjuk berkas dan baris yang memuat angka tersebut.
# ---------------------------------------------------------------------------
BUKTI_KELAS = [
    {"kelas": "stuck", "alternatif": ["A1", "A2", "A9"],
     "lift": "3,12 pada F-14 dan 0,97 pada F-9_A",
     "gate": "G1 1 dari 2 fold, G2 1 dari 2 fold",
     "catatan": "Pada F-9_A persistence 0,787 mengalahkan Random Forest 0,651 dan canary 0,769",
     "jejak": "docs/V7_R1_SOLUTIONS.md:66"},
    {"kelas": "shk", "alternatif": ["A2", "A4"],
     "lift": "1,35 / 1,24 / 1,26 / 3,36 / 0,94 / 9,79 / 2,31",
     "gate": "G1 3 dari 7 fold, G2 6 dari 7 fold",
     "catatan": "Tujuh fold dengan 30 sampai 760 positif per fold",
     "jejak": "docs/V7_R1_SOLUTIONS.md:97"},
    {"kelas": "hyd", "alternatif": ["A1", "A3", "A6", "A8"],
     "lift": "1,40 / 1,00 / 1,02 / 2,03 / 0,80 / 2,35 / 1,07",
     "gate": "G1 2 dari 7 fold, G2 4 dari 7 fold",
     "catatan": "Persistence 0,42 sampai 0,63 mengalahkan Random Forest 0,11 sampai 0,61 pada 7 dari 7 fold",
     "jejak": "docs/V7_R1_SOLUTIONS.md:127"},
    {"kelas": "tool_wear", "alternatif": ["A7"],
     "lift": "1,09 / 1,39 / 1,42 / 1,30",
     "gate": "G1 0 dari 4 alat, G2 4 dari 4 alat",
     "catatan": "AUPRC 0,54 sampai 0,77 dengan prevalensi sekitar 0,5 sehingga plafon lift 2,0",
     "jejak": "docs/V7_R1_SOLUTIONS.md:160"},
    {"kelas": "ssi", "alternatif": ["A2", "A4", "A5"],
     "lift": "2,61 / 3,59 / 6,64 / 3,74 / 1,47",
     "gate": "G1 4 dari 5 fold, G2 5 dari 5 fold",
     "catatan": "Persistence kalah 0 dari 5 fold, dua fold underpowered dengan 3 dan 12 positif",
     "jejak": "docs/V9_PM1_ARCHITECTURE.md:186; docs/V7_R1_SOLUTIONS.md:197"},
    {"kelas": "bit_wear", "alternatif": ["A1", "A5", "A6", "A8"],
     "lift": "1,495 pada F-15S gagal tipis",
     "gate": "G1 3 dari 4 fold, G2 4 dari 4 fold",
     "catatan": "Persistence lebih tinggi daripada Random Forest pada 4 dari 4 fold sehingga verdict turun menjadi layak bersyarat",
     "jejak": "docs/V7_R1_SOLUTIONS.md:203"},
    {"kelas": "vib", "alternatif": ["A2", "A9"],
     "lift": "1,61 / 2,36 / 3,50 / 1,63",
     "gate": "LULUS penuh pada baseline, direproduksi pada V9",
     "catatan": "False alarm rate menyebar 4,15 sampai 496,09 per 24 jam, yaitu rasio 119,6 kali antar sumur",
     "jejak": "docs/V8_PM_VERDICT.md:155; docs/V6_PM_VERDICT.md:131; docs/V9_PM2_VERDICT.md:126, 114"},
]

# ---------------------------------------------------------------------------
# 5. DRAFT LAMA (13 Agustus 2026) untuk dibandingkan dan dihitung ulang
# Sumber: scratch/ppt1/docx_draft_text.txt baris 228 sampai 279
# ---------------------------------------------------------------------------
DRAFT_LAMA = {
    "sumber": "scratch/ppt1/docx_draft_text.txt:228-279",
    "kriteria": ["K1 Recall", "K2 Lead time", "K3 Explainability", "K4 Biaya", "K5 Integrasi", "K6 ROI"],
    "bobot": [0.25, 0.20, 0.15, 0.10, 0.15, 0.15],
    "alternatif": [
        {"nama": "A1 ML Classifier", "skor": [5, 5, 4, 3, 4, 4], "total_tertulis": 4.35},
        {"nama": "A2 IsoForest", "skor": [4, 3, 3, 4, 3, 3], "total_tertulis": 3.40},
        {"nama": "A3 SHAP Dash", "skor": [3, 2, 5, 4, 5, 3], "total_tertulis": 3.55},
        {"nama": "A4 Rule-based", "skor": [3, 2, 2, 5, 5, 2], "total_tertulis": 2.95},
        {"nama": "A6 LOGIX Intg", "skor": [2, 1, 3, 2, 5, 2], "total_tertulis": 2.45},
    ],
    "pilihan_draft": "A1 ML Classifier (Random Forest atau XGBoost) dipadukan A3 SHAP dashboard",
    "skala": "1 sampai 5 tanpa rubrik",
}

# ---------------------------------------------------------------------------
# 6. TRIANGULASI: urutan solusi V7 bagian 7 (independen dari kartu ini)
# ---------------------------------------------------------------------------
URUTAN_V7 = [
    ("1", "S-A1 stuck onset", "A1"),
    ("2", "S-F1 dan S-F2 bit_wear onset", "A1 dan A8"),
    ("3", "S-B1 parse F-10, F-4, F-12, F-15", "A2"),
    ("4", "S-C1 hyd onset", "A1"),
    ("5", "S-D1 dan S-D2 tool_wear progresi", "A7"),
    ("6", "S-A2 stuck F-10 dan F-12", "A2"),
    ("7", "S-C2 hyd label pit dan flow", "A8"),
    ("8", "S-A3, S-C3, S-D4, S-B2, S-B3", "A3, A6, A7, A4, A5"),
]

# ---------------------------------------------------------------------------
# 7. METODE YANG DIPERTIMBANGKAN
# ---------------------------------------------------------------------------
METODE_KANDIDAT = [
    {
        "nama": "AHP",
        "kebutuhan": "perbandingan berpasangan antar kriteria oleh pakar pada skala 1 sampai 9, ditambah uji rasio konsistensi",
        "kesesuaian": "tidak tersedia. Belum ada wawancara mitra maupun penilaian pakar, sehingga matriks perbandingan hanya bisa diisi angka karangan",
        "keputusan": "ditolak",
        "alasan": "Angka perbandingan tanpa pakar adalah angka tanpa jejak, dan rasio konsistensi tidak bermakna bila masukannya karangan. Menolak AHP di sini menjaga aturan bukti, bukan menilai AHP sebagai metode lemah.",
    },
    {
        "nama": "TOPSIS",
        "kebutuhan": "matriks keputusan kardinal, arah tiap kriteria, dan vektor bobot",
        "kesesuaian": "tersedia. Empat kolom berisi angka terukur (C2, C4, C5, C7), dua kolom memakai rubrik berjangkar (C1 dan C3), dan dua kolom berstatus asumsi yang ditandai terbuka (C6 minggu kerja, C8 beban kognitif). Seluruh 72 sel terisi",
        "keputusan": "dipakai sebagai metode utama",
        "alasan": "Menerima campuran kriteria benefit dan cost, menghasilkan jarak ke solusi ideal dan anti-ideal sehingga selisih antar alternatif terbaca sebagai angka, dan formulanya publik sehingga dapat direproduksi pihak lain.",
    },
    {
        "nama": "SAW",
        "kebutuhan": "matriks keputusan kardinal dan vektor bobot, keduanya sama dengan TOPSIS",
        "kesesuaian": "tersedia, memakai masukan identik",
        "keputusan": "dipakai sebagai pembanding bebas",
        "alasan": "Bila dua metode dengan cara mengukur jarak berbeda memberi juara sama, hasil tidak bergantung pada pilihan metode. SAW tidak dipakai sendirian karena penjumlahan berbobot dapat menutupi alternatif yang sangat lemah pada satu kriteria.",
    },
]

# ---------------------------------------------------------------------------
# 8. SITASI METODE (diverifikasi lewat pencarian web pada 25 Oktober 2026)
# ---------------------------------------------------------------------------
SITASI = [
    {
        "kunci": "Hwang dan Yoon 1981",
        "teks": "Hwang, C. L., dan Yoon, K. (1981). Multiple Attribute Decision Making: Methods and Applications, A State-of-the-Art Survey. Springer-Verlag, New York.",
        "doi": "10.1007/978-3-642-48318-9",
        "dipakai_untuk": "rumus TOPSIS, yaitu normalisasi vektor, solusi ideal positif dan negatif, serta koefisien kedekatan",
        "verifikasi": "pencarian web 25 Oktober 2026 menemukan entri Springer tahun 1981 dengan DOI tersebut, dan artikel Wikipedia TOPSIS mengutip sumber yang sama",
    },
    {
        "kunci": "Barron dan Barrett 1996",
        "teks": "Barron, F. H., dan Barrett, B. E. (1996). Decision Quality Using Ranked Attribute Weights. Management Science, 42(11), 1515 sampai 1523.",
        "doi": "10.1287/mnsc.42.11.1515",
        "dipakai_untuk": "penurunan bobot kardinal dari urutan prioritas kriteria memakai Rank-Order Centroid",
        "verifikasi": "pencarian web 25 Oktober 2026 menemukan DOI tersebut pada INFORMS, dengan abstrak yang menyatakan ROC lebih akurat daripada formula berbasis urutan lain",
    },
    {
        "kunci": "Kunsch dan Ishizaka 2019",
        "teks": "Kunsch, P. L., dan Ishizaka, A. (2019). A note on using centroid weights in additive multi-criteria decision analysis. European Journal of Operational Research.",
        "doi": "10.1016/j.ejor.2019.02.021",
        "dipakai_untuk": "batas pemakaian ROC. Artikel ini menunjukkan keunggulan ROC bergantung pada cara elisitasi bobot, sehingga ROC pada kartu ini wajib disertai uji sensitivitas",
        "verifikasi": "pencarian web 25 Oktober 2026 menemukan DOI tersebut beserta ringkasan yang menyatakan peringkat kinerja metode bobot pengganti bergantung pada definisi simpleks bobot",
    },
]

# ---------------------------------------------------------------------------
# 9. ATURAN URUTAN KRITERIA (dasar bobot, dipakai bersama peringkat pada KRITERIA)
# ---------------------------------------------------------------------------
ATURAN_URUT = {"C1": "R1", "C4": "R2", "C2": "R3", "C7": "R4", "C3": "R5",
                "C6": "R6", "C5": "R7", "C8": "R8"}

ATURAN_DEF = [
    {"kode": "R1", "aturan": "kriteria yang menjadi definisi lulus gate", "kriteria": "C1",
     "dasar": "Gate G1 dan G2 adalah definisi operasional lulus pada docs/V7_R1_SOLUTIONS.md:97, 127, 197, 203, 160, sehingga kriteria yang mengukur gate mendahului semua kriteria lain."},
    {"kode": "R2", "aturan": "batasan keras yang menggugurkan, dengan jumlah user story terbanyak", "kriteria": "C4",
     "dasar": "Batasan B2 pada scratch/ppt1/affinity.json menggugurkan alternatif yang mengklaim alarm otomatis, dan tiga user story bergantung pada C4 yaitu U2, U4, dan U6, terbanyak di antara delapan kriteria."},
    {"kode": "R3", "aturan": "batasan keras yang menggugurkan, jumlah user story lebih sedikit", "kriteria": "C2",
     "dasar": "Batasan B4 menetapkan urutan kerja label lebih dahulu, dan dua user story bergantung pada C2 yaitu U1 dan U5."},
    {"kode": "R4", "aturan": "batasan keras yang menuntut jejak, tanpa menggugurkan", "kriteria": "C7",
     "dasar": "Batasan B1 menuntut seluruh angka dapat diaudit, sifatnya administratif sehingga tidak menggugurkan alternatif, dan tiga user story bergantung pada C7 yaitu U4, U5, dan U6."},
    {"kode": "R5", "aturan": "gejala terukur yang belum menjadi batasan", "kriteria": "C3",
     "dasar": "Sebaran false alarm rate 4,15 sampai 496,09 per 24 jam sudah terukur pada docs/V9_PM2_VERDICT.md:114, tetapi belum ada alternatif yang menguji kalibrasi per sumur, sehingga kriteria ini penting namun belum menggugurkan."},
    {"kode": "R6", "aturan": "batasan jadwal dengan daya beda rendah", "kriteria": "C6",
     "dasar": "Tenggat sembilan minggu mengikat seluruh tim menurut Buku Pedoman PPT Tahap I Tabel 3.1 halaman 32, namun seluruh alternatif berada pada rentang dua sampai lima minggu sehingga daya bedanya kecil dan tidak ada user story yang bergantung padanya."},
    {"kode": "R7", "aturan": "biaya data yang bersifat instrumental", "kriteria": "C5",
     "dasar": "Sebagian besar parse sudah selesai pada kampanye V9 menurut docs/V9_PM1_ARCHITECTURE.md:186, sehingga kebutuhan data baru hanya membedakan beberapa alternatif."},
    {"kode": "R8", "aturan": "kriteria dengan bukti terlemah", "kriteria": "C8",
     "dasar": "Rubrik C8 disusun pada subbab 3.3 dan belum divalidasi mitra, bahkan docs/PPT1_BAB3_2.md:665 menyatakan antarmuka peringatan belum dirancang. Peringkat terakhir menandai kekuatan bukti, bukan ketidakpentingan."},
]

# ---------------------------------------------------------------------------
# 10. PETA KRITERIA DRAFT LAMA KE KRITERIA 3.3
# ---------------------------------------------------------------------------
PETA_DRAFT = [
    {"draft": "K1 Recall (bobot 0,25)", "kita": "C1",
     "status": "terpetakan", "catatan": "Keduanya mengukur efektivitas deteksi. Bedanya, K1 memakai skor 1 sampai 5 tanpa rubrik, sedangkan C1 memakai lift dan AUPRC terukur yang sudah ada pada docs/V7_R1_SOLUTIONS.md:97, 127, 197, 203, 160."},
    {"draft": "K2 Lead time (bobot 0,20)", "kita": "tidak punya kriteria sendiri",
     "status": "terpetakan sebagian", "catatan": "Angka lead time memang terukur, yaitu 10 sampai 11,5 menit pada stuck dan 20 sampai 36 detik pada alat bengkel, tetapi hanya untuk dua kelas. Karena tidak tersedia untuk tujuh kelas lain, lead time tidak dapat dipakai sebagai kriteria pemilihan lintas alternatif."},
    {"draft": "K3 Explainability (bobot 0,15)", "kita": "C8",
     "status": "terpetakan sebagian", "catatan": "C8 mengukur beban kognitif keluaran, bukan kualitas penjelasan model. Keduanya bersinggungan pada keterbacaan hasil, dan keduanya berstatus asumsi karena belum divalidasi mitra."},
    {"draft": "K4 Biaya implementasi (bobot 0,10)", "kita": "C5 dan C6",
     "status": "terpetakan", "catatan": "Biaya dipecah menjadi kebutuhan data dan waktu kerja. Rupiah tidak dipakai pada kedua sisi karena tarif rig tidak tersedia pada seluruh 13 dataset, sesuai docs/PPT1_BAB3_2.md:659."},
    {"draft": "K5 Kemudahan integrasi (bobot 0,15)", "kita": "tidak terpetakan",
     "status": "tidak dapat dipertahankan", "catatan": "Tidak ada berkas proyek yang mengukur biaya integrasi ke sistem mitra, dan telemetri mitra tidak dipakai menurut batasan B1. Skor integrasi pada draft karena itu tidak punya jejak."},
    {"draft": "K6 ROI (bobot 0,15)", "kita": "tidak terpetakan",
     "status": "tidak dapat dipertahankan", "catatan": "Tarif rig per jam tidak ada pada seluruh dataset, sehingga ROI dalam rupiah tidak dapat dihitung. Menuliskan angka ROI berarti menulis asumsi sebagai hasil ukur."},
]

