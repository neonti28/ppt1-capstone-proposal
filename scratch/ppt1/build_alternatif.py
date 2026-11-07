"""Bangun BAB III 3.1 (9 alternatif solusi) + JSON bukti.

Sumber tunggal data: berkas di /mnt/d/Capstone 1(v2)/docs dan scratch.
Skrip ini menulis:
  - /mnt/d/Capstone 1(v2)/scratch/ppt1/alternatif.json
  - /mnt/d/Capstone 1(v2)/docs/PPT1_BAB3_1.md
lalu menjalankan pemeriksaan acceptance (9 unik, 3 per anggota, sumber lengkap,
BoK 1..14, nol em-dash).

Jalankan: python3 scratch/ppt1/build_alternatif.py
"""

import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = "/mnt/d/Capstone 1(v2)"

# ---------------------------------------------------------------- BoK resmi
# Sumber: Buku Pedoman PPT Tahap I, Tabel 2.1 (14 IEBoK), disamakan dengan
# IISE ISEBoK (https://www.iise.org/Details.aspx?id=43631).
BOK = {
    1: "Work Design & Measurement",
    2: "Operations Research & Analysis",
    3: "Engineering Economic Analysis",
    4: "Facilities Engineering & Energy Management",
    5: "Quality & Reliability Engineering",
    6: "Ergonomics & Human Factors",
    7: "Operations Engineering & Management",
    8: "Supply Chain Management",
    9: "Engineering Management",
    10: "Safety",
    11: "Information Engineering",
    12: "Design & Manufacturing Engineering",
    13: "Product Design & Development",
    14: "Systems Design & Engineering",
}

# ------------------------------------------------------------- permasalahan
PROBLEMS = [
    {
        "id": "P1",
        "judul": "Label stuck berbentuk status, bukan peristiwa",
        "uraian": (
            "Label STUCK_RT bertahan sebagai blok panjang sehingga jendela sebelumnya "
            "menjadi prediktor hampir sempurna. Prevalensi F-9_A 66,9%, persistence 0,787 "
            "mengalahkan Random Forest 0,651, dan lift F-9_A turun ke 0,97."
        ),
        "jejak": "docs/V7_R1_SOLUTIONS.md:66-70 (angka turunan docs/V6_E1_ML_DESIGN.md 4.4)",
    },
    {
        "id": "P2",
        "judul": "Jumlah positif shk terlalu sedikit per fold",
        "uraian": (
            "Gate G1 lolos 3 dari 7 fold sedangkan G2 lolos 6 dari 7, sehingga akarnya bukan "
            "mutu fitur melainkan jumlah informasi positif: F-9_A 30 positif dan F-9 45 positif, "
            "dibanding F-14 760 positif."
        ),
        "jejak": "docs/V7_R1_SOLUTIONS.md:97-99",
    },
    {
        "id": "P3",
        "judul": "Label hyd adalah ambang residual dari proses yang persisten",
        "uraian": (
            "Label diturunkan dari residual SPPA dengan ambang nilai mutlak z di atas 2 sehingga mewarisi "
            "persistensi proses. Persistence 0,42 sampai 0,63 mengalahkan Random Forest 0,11 sampai 0,61 pada "
            "7 dari 7 fold, dan G1 hanya lolos 2 dari 7."
        ),
        "jejak": "docs/V7_R1_SOLUTIONS.md:127-131",
    },
    {
        "id": "P4",
        "judul": "tool_wear terbatas 4 alat dengan label identitas run",
        "uraian": (
            "Hanya 4 alat dan 2 run per alat (469 jendela), label berupa identitas run R01/R02 sehingga "
            "urutan percobaan ikut terkorelasi dengan label. Prevalensi sekitar 0,5 membatasi plafon lift "
            "pada 2,0; hasil nyata G1 0 dari 4 dengan lift 1,09 sampai 1,42."
        ),
        "jejak": "docs/V7_R1_SOLUTIONS.md:160-165",
    },
    {
        "id": "P5",
        "judul": "bit_wear dikalahkan persistence pada seluruh fold",
        "uraian": (
            "Gate G1 lolos 3 dari 4 dan G2 lolos 4 dari 4, tetapi persistence lebih tinggi daripada "
            "Random Forest pada 4 dari 4 fold karena label high-MSE membentuk blok lintas kedalaman. "
            "Aturan pra-registrasi menurunkan verdict menjadi layak bersyarat."
        ),
        "jejak": "docs/V7_R1_SOLUTIONS.md:203-205",
    },
    {
        "id": "P6",
        "judul": "Sebagian fold ssi underpowered",
        "uraian": (
            "ssi lolos G1 4 dari 5 dan G2 5 dari 5 dengan persistence 0 dari 5, tetapi F-7 hanya 3 positif "
            "dan F-9 hanya 12 positif sehingga selang kepercayaan melebar dan F-9_A gagal tipis pada lift 1,47."
        ),
        "jejak": "docs/V7_R1_SOLUTIONS.md:197-199",
    },
    {
        "id": "P7",
        "judul": "Validitas label lintas sumur belum terbukti",
        "uraian": (
            "Kontrol-positif stuck 0 dari 10, label hyd masih berupa proksi residual, dan campuran severitas "
            "berbeda antar sumur. Cacat ini mengancam seluruh lapisan onset sebelum model apa pun dipercaya."
        ),
        "jejak": "docs/V8_PM_VERDICT.md:202; docs/V4_MAINTENANCE_ML_OPTIONS.md:145-155",
    },
    {
        "id": "P8",
        "judul": "Ambang global tidak portabel antar sumur",
        "uraian": (
            "Pada titik operasi yang sama, false alarm rate vib menyebar 4,15 sampai 496,09 per 24 jam, "
            "yaitu rasio 119,6 kali antar sumur, sehingga satu ambang global tidak dapat dipakai."
        ),
        "jejak": "docs/V9_PM2_VERDICT.md:114",
    },
    {
        "id": "P9",
        "judul": "Tidak ada label keausan fisik dari rig",
        "uraian": (
            "Seluruh 77 berkas bhaRun tidak memuat dullingInfo, dullGrade, maupun bitName, sehingga label yang "
            "tersedia hanya batas waktu run, bukan tingkat keausan. Prediksi onset keausan bit (K-2) belum "
            "dijalankan sama sekali."
        ),
        "jejak": "docs/V4_MAINTENANCE_ML_OPTIONS.md:62; docs/V9_PM2_VERDICT.md:176",
    },
]

# --------------------------------------------------------------- alternatif
ALTS = [
    {
        "id": "A1",
        "anggota": 1,
        "nama": "Relabeling onset peristiwa: dari status menjadi kejadian",
        "ringkas": (
            "Mengubah definisi target dari status yang bertahan menjadi titik masuk peristiwa, sehingga "
            "dominasi persistence hilang secara konstruksi."
        ),
        "deskripsi": (
            "Untuk setiap deret label instrumen (STUCK_RT, residual SPPA pada hyd, dan label high-MSE pada "
            "bit_wear), onset t_e didefinisikan sebagai titik naik status. Jendela positif adalah jendela fitur "
            "yang berakhir dalam horizon H sebelum t_e, sedangkan jendela di dalam blok setelah onset dibuang "
            "dari evaluasi dan tidak dinegatifkan. Horizon H ditetapkan 10 menit dengan uji sensitivitas pada 5 dan "
            "30 menit. Gate G1 (lift minimal 1,5 pada mayoritas sumur layak) dan G2 (AUPRC minimal AUPRC canary "
            "kedalaman) tidak diubah, sehingga perubahan hanya berada pada definisi label."
        ),
        "masalah": ["P1", "P3", "P5"],
        "bok": [14, 11, 5],
        "bok_alasan": (
            "BoK 14 karena alternatif ini menetapkan ulang fungsi sistem yang diprediksi (kejadian, bukan status); "
            "BoK 11 karena perubahan berada pada rantai data dan label; BoK 5 karena metrik yang dipakai adalah "
            "metrik keandalan dan deteksi kegagalan."
        ),
        "bukti": [
            {
                "klaim": "Formulasi onset sudah dijalankan untuk stuck dan menghasilkan peringatan dengan arah benar pada beban rendah: Random Forest pada titik operasi 0,05 memberi B1 0,51 sampai 1,00 dengan TLead 10 sampai 11,5 menit, sedangkan baseline persistence-EVENT hanya memberi TLead median 7,0 menit dengan B1 0 sampai 11,5 persen.",
                "jejak": "docs/V9_EVAL_B_LAYERB.md:101",
            },
            {
                "klaim": "Untuk hyd, formulasi yang sama menghasilkan B1 nol dari tiga onset dengan TLead nol, jadi hasil negatifnya terukur dan dilaporkan apa adanya.",
                "jejak": "docs/V9_EVAL_B_LAYERB.md:103",
            },
            {
                "klaim": "Relabel tidak memerlukan parse baru karena deret sumber sudah berbentuk CSV.",
                "jejak": "docs/V7_R1_SOLUTIONS.md:76, 136, 204 (data/volve/witsml_parsed/*.csv, data/USROP_labeled.csv)",
            },
        ],
        "status": "Berjalan",
        "status_catatan": (
            "Sudah dieksekusi untuk stuck (K-ii) dan hyd (K-ii) pada kampanye V9. Belum dieksekusi untuk bit_wear "
            "K-2 karena pra-registrasi kampanye tersebut belum terbit."
        ),
        "sumber": ["S-A1", "S-C1", "S-F1"],
        "sumber_jenis": "13 solusi berkode (S-A1, S-C1) dan solusi pendukung V7 6 (S-F1)",
    },
    {
        "id": "A2",
        "anggota": 1,
        "nama": "Perluasan wellbore berkanal disfungsi (F-10, F-4, F-12, F-15)",
        "ringkas": (
            "Menambah sumur dan fold dengan memparse wellbore yang terbukti memiliki kanal disfungsi, bukan "
            "menurunkan ambang label."
        ),
        "deskripsi": (
            "Empat wellbore yang belum diparse (F-10, F-4, F-12, F-15) diproses ke CSV dengan protokol identik "
            "kampanye sebelumnya: grid 60 detik, agregasi menit, syarat kelayakan jendela yang sama. Hasilnya "
            "digabungkan ke kampanye leave-one-well-out per kelas sehingga jumlah fold dan jumlah positif naik "
            "tanpa mengubah definisi label maupun gate. Peta kanal dipakai sebagai syarat masuk: hanya wellbore "
            "yang benar-benar mendaftarkan mnemonic disfungsi yang diambil."
        ),
        "masalah": ["P2", "P6"],
        "bok": [11, 5, 14],
        "bok_alasan": (
            "BoK 11 karena pekerjaan inti adalah akuisisi dan pengelolaan data multi-sumur; BoK 5 karena tujuannya "
            "memulihkan kecukupan sampel untuk estimasi keandalan; BoK 14 karena data dari empat sumur harus "
            "diintegrasikan ke satu protokol evaluasi."
        ),
        "bukti": [
            {
                "klaim": "Peta kanal menunjukkan sumber positif yang nyata: F-10 mendaftarkan SHKRSK_RT pada 188 berkas, CRPM_RT 186, STKSLP 125, VIBLAT_RT 66, dan STUCK_RT 18; F-4 135/135/135/86; F-12 91/90/52/6; F-15 77/76/76/76.",
                "jejak": "docs/V7_R1_SOLUTIONS.md:43-48",
            },
            {
                "klaim": "Akuisisi data sudah berjalan dan terukur: CRPM F-10 281.030 baris, F-4 42.010 baris, F-12 178.430 baris, F-15 57.846 baris, dengan re-run 11 fold belum dilakukan.",
                "jejak": "docs/V9_PM1_ARCHITECTURE.md:186",
            },
            {
                "klaim": "Akar masalah yang diserang terukur pada ssi: G1 4 dari 5, F-9_A lift 1,47 gagal tipis, dan dua fold underpowered (F-7 3 positif, F-9 12 positif).",
                "jejak": "docs/V9_PM1_ARCHITECTURE.md:186",
            },
        ],
        "status": "Berjalan",
        "status_catatan": (
            "Akuisisi dan parsing selesai dengan angka baris terukur. Evaluasi ulang fold belum dijalankan, sehingga "
            "dampak terhadap gate belum dapat diklaim."
        ),
        "sumber": ["S-B1", "S-A2", "S-E1"],
        "sumber_jenis": "13 solusi berkode (S-B1, S-A2) dan solusi pendukung V7 6.1 (S-E1)",
    },
    {
        "id": "A3",
        "anggota": 1,
        "nama": "Penjaminan mutu label dan label probabilistik multi-sumber",
        "ringkas": (
            "Membereskan kebenaran label lebih dahulu, lalu menambah sumbu bukti melalui label model bila noise "
            "antar sumber masih besar."
        ),
        "deskripsi": (
            "Dua tahap berurutan. Tahap pertama adalah audit semantik label: mengunci satu varian onset stuck "
            "(strict atau forward-fill), memverifikasi arti skala 0/1/2/3 pada STUCK_RT dan SHKRSK_RT lintas sumur, "
            "merekonsiliasi prevalensi stuck 66,9 persen dengan 49,4 persen, menyinkronkan zona waktu kontrol-positif, "
            "dan mengganti label hyd proksi dengan kejadian nyata. Tahap kedua adalah label model generatif dengan "
            "labeling function independen (status instrumen, event kurasi, penanda fisika differential sticking, "
            "anomali overpull), dengan syarat kanal pembentuk label dilarang menjadi fitur. Urutan ini wajib karena "
            "kalibrasi ambang apa pun yang dilakukan sebelum label benar hanya menghasilkan presisi palsu."
        ),
        "masalah": ["P7"],
        "bok": [5, 11, 14],
        "bok_alasan": (
            "BoK 5 karena inti pekerjaan adalah analisis kegagalan dan mutu pengukuran; BoK 11 karena label adalah "
            "keluaran sistem informasi; BoK 14 karena keputusan label harus konsisten dengan tujuan sistem, bukan "
            "dengan satu sumur."
        ),
        "bukti": [
            {
                "klaim": "Tiga cacat label sudah terukur: kontrol-positif stuck 0 dari 10, label hyd masih proksi residual, dan campuran severitas berbeda antar sumur.",
                "jejak": "docs/V8_PM_VERDICT.md:202",
            },
            {
                "klaim": "Basis label kurasi memuat 884 kejadian, 50 di antaranya relevan BHA, dengan total durasi 73.500 menit atau 1.225 jam, sehingga bahan rekonsiliasi tersedia dan dapat dihitung ulang.",
                "jejak": "docs/PPT1_LEDGER_ANGKA.md:145, 193; skrip scratch/ppt1/verify_durations.py",
            },
            {
                "klaim": "Urutan 6a sebelum 6b ditetapkan karena kalibrasi ambang menyetel kebenaran, sehingga label yang salah akan menghasilkan presisi palsu.",
                "jejak": "docs/V4_MAINTENANCE_ML_OPTIONS.md:163-166",
            },
        ],
        "status": "Rencana (belum terealisasi)",
        "status_catatan": "Belum ada langkah audit label yang dieksekusi pada kampanye mana pun.",
        "sumber": ["6a", "S-A3"],
        "sumber_jenis": "lever V4 6a dan solusi berkode S-A3",
    },
    {
        "id": "A4",
        "anggota": 2,
        "nama": "Unit analisis per-stand pengeboran",
        "ringkas": (
            "Mengganti unit jendela 10 menit dengan unit operasional rig (stand) agar prevalensi naik dan varians "
            "antar fold turun."
        ),
        "deskripsi": (
            "Label per stand didefinisikan sebagai any(kanal minimal 1) selama stand berlangsung, dan fitur berupa "
            "statistik stand sebelumnya. Batas stand diturunkan dari BPOS atau celah waktu pada CSV yang sudah ada. "
            "Konsekuensi yang harus dinyatakan terbuka: horizon prediksi melebar dari 10 menit menjadi stand "
            "berikutnya, sehingga klaim yang boleh dibuat adalah peringatan risiko per stand, bukan peringatan "
            "10 menit."
        ),
        "masalah": ["P2", "P6"],
        "bok": [7, 5, 11],
        "bok_alasan": (
            "BoK 7 karena unit yang dipakai adalah unit operasi produksi pengeboran; BoK 5 karena tujuannya "
            "menstabilkan estimasi keandalan; BoK 11 karena agregasi dan penyimpanan fitur berubah."
        ),
        "bukti": [
            {
                "klaim": "Rentang prevalensi 10 sampai 40 persen pada unit stand adalah perkiraan desain dan belum dihitung, sehingga berstatus asumsi.",
                "jejak": "docs/V7_R1_SOLUTIONS.md:111 (ditandai sebagai angka yang dihitung saat eksekusi)",
            },
            {
                "klaim": "Batas stand dapat diturunkan dari BPOS dan celah waktu pada data yang sudah tersedia, sehingga tidak memerlukan akuisisi baru.",
                "jejak": "docs/V7_R1_SOLUTIONS.md:112",
            },
            {
                "klaim": "Bila unit stand dipakai, false alarm rate wajib dihitung per stand disertai justifikasinya, karena gate saat ini dihitung per jendela waktu.",
                "jejak": "docs/V9_PM1_ARCHITECTURE.md:470",
            },
        ],
        "status": "Rencana (belum terealisasi)",
        "status_catatan": "Belum dijalankan; belum ada artefak hasil untuk unit stand.",
        "sumber": ["S-B2"],
        "sumber_jenis": "13 solusi berkode",
    },
    {
        "id": "A5",
        "anggota": 2,
        "nama": "Prediksi severity ordinal dengan evaluasi stabilitas fold",
        "ringkas": (
            "Memakai seluruh informasi skala 0 sampai 3, lalu menurunkan keputusan biner pada ambang fisik yang "
            "sama sambil melaporkan stabilitas tiap fold secara eksplisit."
        ),
        "deskripsi": (
            "Model dilatih memprediksi skala (ordinal atau regresi) kemudian keputusan biner diturunkan pada ambang "
            "minimal 1, sehingga gate tetap dihitung pada AUPRC biner dan tidak bergeser. Lapisan kedua adalah "
            "evaluasi: stratified bootstrap per fold dan pelaporan jumlah positif per fold, agar selang kepercayaan "
            "yang lebar tidak menyembunyikan fold underpowered."
        ),
        "masalah": ["P6", "P7"],
        "bok": [5, 2, 11],
        "bok_alasan": (
            "BoK 5 karena pengujian hipotesis dan regresi adalah alat utamanya; BoK 2 karena keputusan ambang adalah "
            "analisis keputusan; BoK 11 karena keluaran skor harus dikelola sebagai informasi operasional."
        ),
        "bukti": [
            {
                "klaim": "Klasifikasi severitas stick-slip dengan pembelajaran mesin sudah mapan pada literatur sehingga jalur ordinal bukan klaim baru.",
                "jejak": "docs/V7_R1_SOLUTIONS.md:197 (sitasi Hegde 2019, doi 10.1016/j.petrol.2019.05.021)",
            },
            {
                "klaim": "ssi sudah lolos G1 4 dari 5 dengan dua fold underpowered (F-7 3 positif, F-9 12 positif), sehingga stabilitas fold adalah variabel yang wajib dilaporkan.",
                "jejak": "docs/V9_PM1_ARCHITECTURE.md:186",
            },
            {
                "klaim": "Penulis solusi sendiri menilai jalur stabilitas fold sebagai pengeras bukti, bukan penambah kelas, sehingga posisinya pelengkap A4 dan A2.",
                "jejak": "docs/V7_R1_SOLUTIONS.md:199",
            },
        ],
        "status": "Rencana (belum terealisasi)",
        "status_catatan": "Belum dijalankan; tidak ada angka ordinal maupun bootstrap pada kampanye yang sudah ada.",
        "sumber": ["S-B3", "S-E2"],
        "sumber_jenis": "13 solusi berkode (S-B3) dan solusi pendukung V7 6.1 (S-E2)",
    },
    {
        "id": "A6",
        "anggota": 2,
        "nama": "Formulasi survival dan sisa umur pakai (time-to-event)",
        "ringkas": (
            "Memodelkan waktu sampai peristiwa, bukan status sesaat, sehingga keluaran berupa risiko per horizon "
            "dan sisa umur pakai peralatan."
        ),
        "deskripsi": (
            "Model hazard proporsional h(t|x) = h0(t) exp(beta transpose x) dipakai untuk waktu sampai peristiwa "
            "hidrolik dan untuk waktu sampai penarikan bit. Skor risiko per horizon H dievaluasi dengan gate biner "
            "yang sama, sehingga formulasi berubah tanpa mengubah gerbang. Label waktu sampai penarikan bit "
            "diturunkan dari interval dTimStart dan dTimStop pada berkas bhaRun."
        ),
        "masalah": ["P9", "P3"],
        "bok": [5, 3, 2],
        "bok_alasan": (
            "BoK 5 karena survival dan sisa umur pakai adalah inti rekayasa keandalan; BoK 3 karena keputusan "
            "penarikan bit adalah trade-off biaya; BoK 2 karena penaksiran hazard adalah model matematis untuk "
            "pengambilan keputusan."
        ),
        "bukti": [
            {
                "klaim": "Label waktu sampai penarikan tersedia dari 77 berkas bhaRun, tetapi berkas itu tidak memuat dullingInfo, dullGrade, maupun bitName, sehingga label hanya berupa batas run dan bukan keausan fisik.",
                "jejak": "docs/V4_MAINTENANCE_ML_OPTIONS.md:62",
            },
            {
                "klaim": "Penulis solusi menilai survival sebagai opsi pembanding karena mengubah formulasi tanpa menambah informasi, sehingga posisinya bukan solusi primer.",
                "jejak": "docs/V7_R1_SOLUTIONS.md:152",
            },
            {
                "klaim": "Titik operasi hidrolik saat ini menghasilkan nol dari tiga onset terdeteksi, sehingga pembanding berformulasi waktu adalah langkah yang masuk akal dan bukan pengulangan.",
                "jejak": "docs/V9_EVAL_B_LAYERB.md:103",
            },
        ],
        "status": "Rencana (belum terealisasi)",
        "status_catatan": "Belum dijalankan; belum ada model hazard pada kampanye mana pun.",
        "sumber": ["S-C3", "V4-Opsi3"],
        "sumber_jenis": "solusi berkode S-C3 dan opsi V4 nomor 3 (sisa umur pakai bit)",
    },
    {
        "id": "A7",
        "anggota": 3,
        "nama": "Penguatan kampanye keausan alat bengkel: progresi, dekomposisi mode, dan ranking",
        "ringkas": (
            "Tiga mekanisme pada dataset yang sama: label progresi dalam-run, fitur hasil dekomposisi, dan "
            "ranking antar status sebagai cadangan."
        ),
        "deskripsi": (
            "Bekerja pada 8 berkas akselerometer 1000 Hz (4 alat, 2 run, 469 jendela). Mekanisme pertama adalah "
            "label progresi: deret fitur keausan dihitung, titik ubah dideteksi per run, dan jendela sebelum titik "
            "ubah menjadi positif. Mekanisme kedua adalah fitur Variational Mode Decomposition berupa energi pita "
            "dan statistik per mode. Mekanisme ketiga adalah learning-to-rank pasangan dalam alat, dipakai hanya "
            "bila validasi titik ubah gagal karena artefak termal."
        ),
        "masalah": ["P4"],
        "bok": [12, 5, 14],
        "bok_alasan": (
            "BoK 12 karena objek yang dipantau adalah keausan pahat pada proses manufaktur; BoK 5 karena keluarannya "
            "metrik keandalan; BoK 14 karena tiga mekanisme harus diintegrasikan ke satu protokol evaluasi."
        ),
        "bukti": [
            {
                "klaim": "Deteksi perubahan regime sudah dijalankan pada 4 dari 4 alat dengan TLead 20 sampai 36 detik (1,8 kali) dan false alarm terkalibrasi 1 sampai 3 per alat, tetapi presisi run hanya 0,50 karena titik ubah juga signifikan pada alat baru.",
                "jejak": "docs/V9_EVAL_C_LAYERC.md:98",
            },
            {
                "klaim": "Uji artefak termal gagal membuktikan confound pada 0 dari 8 run, sehingga kritik urutan run tidak terbukti pada data ini.",
                "jejak": "docs/V9_EVAL_C_LAYERC.md:98",
            },
            {
                "klaim": "Baseline ranking lintas alat stabil pada 1,19 kali (AUPRC 0,516 sampai 0,612) sedangkan engine Random Forest belum dijalankan di V9, sehingga mekanisme ranking masih terbuka.",
                "jejak": "docs/V9_EVAL_C_LAYERC.md:99",
            },
            {
                "klaim": "Fitur dekomposisi mode baru dinyatakan sebagai pengangkat AUPRC pada rancangan, tanpa artefak eksekusi, sehingga statusnya masih rencana.",
                "jejak": "docs/V9_PM1_ARCHITECTURE.md:276",
            },
        ],
        "status": "Berjalan",
        "status_catatan": (
            "Mekanisme progresi dan kalibrasi ambang selesai pada domain bengkel. Dekomposisi mode dan ranking "
            "belum dieksekusi."
        ),
        "sumber": ["S-D1", "S-D2", "S-D4"],
        "sumber_jenis": "13 solusi berkode",
    },
    {
        "id": "A8",
        "anggota": 3,
        "nama": "Label fisika pengganti label proksi",
        "ringkas": (
            "Mengganti label berbasis ambang dengan label berbasis mekanisme: well-control untuk hidrolik dan "
            "kombinasi energi spesifik untuk keausan bit."
        ),
        "deskripsi": (
            "Untuk hidrolik, dua label turunan fisik dipakai sebagai onset: perubahan volume pit (PITTOT dan "
            "GAINLOSSTOT) sebagai penanda kick atau loss, serta selisih laju masuk dan keluar (FLOWOUT dikurangi "
            "FLOWIN) sebagai penanda washout, masing-masing dengan ambang z-score median dan MAD per sumur. Untuk "
            "keausan bit, status high-MSE hanya dihitung sebagai keausan bila disertai penurunan rasio MSE terhadap "
            "energi spesifik, mengikuti aturan Menand dan Mills. Kanal pembentuk label dilarang menjadi fitur."
        ),
        "masalah": ["P3", "P5", "P9"],
        "bok": [10, 5, 11],
        "bok_alasan": (
            "BoK 10 karena kick dan lost circulation adalah bahaya well-control; BoK 5 karena label baru harus "
            "diverifikasi terhadap keandalan alat; BoK 11 karena penurunan label adalah pekerjaan rekayasa informasi."
        ),
        "bukti": [
            {
                "klaim": "Kanal sumber label tersedia dan terhitung: GAINLOSSTOT pada 575 berkas di F-1 C dan 517 di F-11, PITTOT 565 dan 506, FLOWOUT 688, FLOWOUTPC 949.",
                "jejak": "docs/V7_R1_SOLUTIONS.md:37-38",
            },
            {
                "klaim": "Bahan label silang tersedia langsung: USROP_labeled.csv memuat 198.928 baris dengan kolom WOB, ROP, RPM, dan MSE.",
                "jejak": "docs/V7_R1_SOLUTIONS.md:182",
            },
            {
                "klaim": "Aturan MSE dan MSE/DS sudah diverifikasi rumusnya pada dokumen sumber, sehingga label silang bukan gagasan tanpa dasar.",
                "jejak": "docs/V7_R1_SOLUTIONS.md:181 (sitasi Menand dan Mills, AADE-17-NTCE-033)",
            },
        ],
        "status": "Rencana (belum terealisasi)",
        "status_catatan": (
            "Belum ada label pit atau flow yang diparse menjadi deret label; kanal mentahnya sudah teridentifikasi "
            "di F-9, F-1 C, dan F-11."
        ),
        "sumber": ["S-C2", "S-D3", "S-F2"],
        "sumber_jenis": "solusi berkode S-C2, S-D3, dan solusi pendukung V7 6.2 (S-F2)",
    },
    {
        "id": "A9",
        "anggota": 3,
        "nama": "Lapisan keputusan operasional: kalibrasi ambang per sumur dan purwarupa peringatan dini",
        "ringkas": (
            "Menyentuh titik operasi alat, bukan model: ambang per sumur, purwarupa kampanye pada data berlabel, dan "
            "indeks kondisi untuk disfungsi yang labelnya belum tersedia."
        ),
        "deskripsi": (
            "Tiga komponen yang semuanya bersifat operasional. Pertama, kalibrasi ambang per sumur secara prospektif "
            "untuk hyd K-i, vib Random Forest, dan shk Random Forest, lalu pengukuran false alarm rate setelah "
            "kalibrasi dan pembandingan terhadap baseline persistence. Kedua, purwarupa kampanye stuck-pipe pada "
            "dataset TSPP yang sudah berlabel dengan kanal permukaan frekuensi tinggi sebagai uji kelayakan cepat "
            "sebelum kampanye lintas sumur. Ketiga, indeks kondisi drill-string berbasis autoencoder untuk disfungsi "
            "yang labelnya tidak tersedia langsung, dengan validasi berupa korelasi terhadap event bit run atau stuck, "
            "bukan klaim presisi tinggi. Ketiganya tidak menyentuh gate G1 dan G2 yang sudah dikunci."
        ),
        "masalah": ["P8", "P1"],
        "bok": [1, 6, 3],
        "bok_alasan": (
            "BoK 1 karena ambang dan prosedur alarm adalah bagian dari desain sistem kerja driller; BoK 6 karena "
            "beban kognitif dan tampilan alert adalah faktor manusia; BoK 3 karena keputusan biaya false alarm dan "
            "penghematan rig time adalah analisis ekonomi teknik, sekaligus menutup rantai BoK sesuai pedoman."
        ),
        "bukti": [
            {
                "klaim": "Ambang global terbukti gagal: pada titik operasi 0,5 false alarm rate vib menyebar 4,15 sampai 496,09 per 24 jam atau rasio 119,6 kali antar sumur.",
                "jejak": "docs/V9_PM2_VERDICT.md:114",
            },
            {
                "klaim": "Dataset TSPP tersedia dengan 52.905 baris pada empat berkas dan 10 kanal permukaan, sehingga purwarupa dapat dijalankan tanpa akuisisi baru.",
                "jejak": "docs/V10_D1_BAB_DATA.md:86, 296",
            },
            {
                "klaim": "Artefak autoencoder lama tidak diskriminatif karena 75 sampai 99 persen baris berada di atas ambang, sehingga komponen indeks kondisi harus dikerjakan ulang dan tidak boleh mengutip artefak itu sebagai bukti.",
                "jejak": "docs/V4_MAINTENANCE_ML_OPTIONS.md:58",
            },
            {
                "klaim": "Alat saat ini berjalan dengan nol slot alarm otomatis dari 27 head, sehingga lapisan ini adalah syarat naik tier dan bukan tambahan opsional.",
                "jejak": "scratch/v9_i1/v9_i1_RESULTS.json (kunci auto_critical_alarm_slots = 0; total head 4+4+4+6+4+2+3 = 27)",
            },
        ],
        "status": "Rencana (belum terealisasi)",
        "status_catatan": (
            "Kalibrasi ambang per sumur untuk hyd, vib, dan shk belum dijalankan. Kalibrasi false alarm yang sudah "
            "ada hanya di dalam engine tool_wear pada domain bengkel."
        ),
        "sumber": ["6b", "V4-Opsi1", "V4-Opsi2"],
        "sumber_jenis": "lever V4 6b dan opsi V4 nomor 1 dan 2",
    },
]

# Sumber yang wajib terpakai tepat sekali (13 berkode + 4 pendukung + 3 opsi + 2 lever)
WAJIB_SUMBER = [
    "S-A1", "S-A2", "S-A3", "S-B1", "S-B2", "S-B3", "S-C1", "S-C2", "S-C3",
    "S-D1", "S-D2", "S-D3", "S-D4",
    "S-E1", "S-E2", "S-F1", "S-F2",
    "V4-Opsi1", "V4-Opsi2", "V4-Opsi3",
    "6a", "6b",
]
STATUS_SAH = {"Selesai", "Berjalan", "Rencana (belum terealisasi)"}


def periksa():
    galat = []
    if len(ALTS) != 9:
        galat.append(f"jumlah alternatif {len(ALTS)} bukan 9")
    ids = [a["id"] for a in ALTS]
    if len(set(ids)) != len(ids):
        galat.append("id alternatif duplikat")
    for anggota in (1, 2, 3):
        n = sum(1 for a in ALTS if a["anggota"] == anggota)
        if n != 3:
            galat.append(f"anggota {anggota} punya {n} alternatif, wajib 3")
    # nama unik
    nama = [a["nama"].lower() for a in ALTS]
    if len(set(nama)) != len(nama):
        galat.append("nama alternatif duplikat")
    # sumber: tepat sekali, dan himpunannya lengkap
    dipakai = []
    for a in ALTS:
        if not a["sumber"]:
            galat.append(f"{a['id']} tanpa sumber")
        dipakai.extend(a["sumber"])
    dobel = sorted({s for s in dipakai if dipakai.count(s) > 1})
    if dobel:
        galat.append(f"sumber dipakai lebih dari sekali: {dobel}")
    hilang = sorted(set(WAJIB_SUMBER) - set(dipakai))
    if hilang:
        galat.append(f"sumber belum punya rumah: {hilang}")
    asing = sorted(set(dipakai) - set(WAJIB_SUMBER))
    if asing:
        galat.append(f"sumber di luar daftar resmi: {asing}")
    # BoK
    for a in ALTS:
        if len(a["bok"]) < 3:
            galat.append(f"{a['id']} hanya {len(a['bok'])} BoK, minimal 3")
        for b in a["bok"]:
            if b not in BOK:
                galat.append(f"{a['id']} memakai BoK {b} di luar 1..14")
    # status
    for a in ALTS:
        if a["status"] not in STATUS_SAH:
            galat.append(f"{a['id']} status tidak baku: {a['status']}")
    # masalah
    pids = {p["id"] for p in PROBLEMS}
    for a in ALTS:
        if not a["masalah"]:
            galat.append(f"{a['id']} tanpa masalah yang dirujuk")
        for p in a["masalah"]:
            if p not in pids:
                galat.append(f"{a['id']} merujuk masalah tak dikenal {p}")
    # bukti wajib bertrace (punya jejak)
    for a in ALTS:
        if not a["bukti"]:
            galat.append(f"{a['id']} tanpa bukti kelayakan")
        for b in a["bukti"]:
            if not b.get("jejak"):
                galat.append(f"{a['id']} punya bukti tanpa jejak")
    # rantai BoK: mulai 14, berakhir 3
    if 14 not in ALTS[0]["bok"]:
        galat.append("alternatif pertama tidak memuat BoK 14")
    if 3 not in ALTS[-1]["bok"]:
        galat.append("alternatif terakhir tidak memuat BoK 3")
    return galat


def tulis_json(galat):
    data = {
        "meta": {
            "dokumen": "BAB III 3.1 Permasalahan & Alternatif Solusi",
            "versi": "1.0",
            "dibuat": datetime.now(ZoneInfo("Asia/Jakarta")).strftime("%Y-%m-%d %H:%M WIB"),
            "skrip": "scratch/ppt1/build_alternatif.py",
            "sumber_utama": [
                "docs/V7_R1_SOLUTIONS.md",
                "docs/V4_MAINTENANCE_ML_OPTIONS.md",
                "docs/V9_EVAL_B_LAYERB.md",
                "docs/V9_EVAL_C_LAYERC.md",
                "docs/V9_PM1_ARCHITECTURE.md",
                "docs/V9_PM2_VERDICT.md",
                "docs/V8_PM_VERDICT.md",
                "docs/V10_D1_BAB_DATA.md",
                "docs/V6_E1_ML_DESIGN.md",
                "docs/PPT1_LEDGER_ANGKA.md",
                "scratch/v9_i1/v9_i1_RESULTS.json",
            ],
            "bok_acuan": "Buku Pedoman PPT Tahap I Tabel 2.1 (14 IEBoK) = IISE ISEBoK 2021",
            "catatan_bok": "Pedoman mewajibkan minimal 3 BoK, diawali BoK 14 dan diakhiri BoK 3.",
            "periksa": "lolos" if not galat else galat,
        },
        "permasalahan": PROBLEMS,
        "bok": {str(k): v for k, v in BOK.items()},
        "alternatif": ALTS,
        "peta_sumber": {s: [a["id"] for a in ALTS if s in a["sumber"]][0] for s in WAJIB_SUMBER},
        "rekap": {
            "jumlah_alternatif": len(ALTS),
            "per_anggota": {str(i): sum(1 for a in ALTS if a["anggota"] == i) for i in (1, 2, 3)},
            "jumlah_sumber_terpakai": len(set(sum((a["sumber"] for a in ALTS), []))),
            "status": {
                s: [a["id"] for a in ALTS if a["status"] == s] for s in sorted(STATUS_SAH)
            },
            "bok_terpakai": sorted({b for a in ALTS for b in a["bok"]}),
            "bok_belum_terpakai": sorted(set(BOK) - {b for a in ALTS for b in a["bok"]}),
        },
    }
    path = os.path.join(ROOT, "scratch/ppt1/alternatif.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path


def md_tabel_problems():
    baris = [
        "| Kode | Permasalahan | Uraian ringkas dan angka | Jejak |",
        "|---|---|---|---|",
    ]
    for p in PROBLEMS:
        baris.append(
            f"| {p['id']} | {p['judul']} | {p['uraian']} | `{p['jejak']}` |"
        )
    return "\n".join(baris)


def md_tabel_rekap():
    eksekusi = {
        "A1": "V9, sebagian (stuck K-ii dan hyd K-ii)",
        "A2": "V9, akuisisi data (baris hasil parse)",
        "A3": "belum ada",
        "A4": "belum ada",
        "A5": "belum ada",
        "A6": "belum ada",
        "A7": "V9, domain bengkel (K-i)",
        "A8": "belum ada",
        "A9": "belum ada",
    }
    baris = [
        "| No | Anggota | Alternatif solusi | Kode sumber | BoK | Masalah yang dirujuk | Dieksekusi di kampanye | Status |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for a in ALTS:
        bok = ", ".join(f"{b}" for b in a["bok"])
        baris.append(
            f"| {a['id']} | Anggota {a['anggota']} | {a['nama']} | "
            f"{', '.join(a['sumber'])} | {bok} | {', '.join(a['masalah'])} | "
            f"{eksekusi[a['id']]} | {a['status']} |"
        )
    return "\n".join(baris)


def md_rincian(a):
    out = []
    out.append(f"#### 3.1.4.{ALTS.index(a) + 1} {a['id']} {a['nama']} (Anggota {a['anggota']})")
    out.append("")
    out.append(f"**Ringkasan.** {a['ringkas']}")
    out.append("")
    out.append(f"**Deskripsi teknis.** {a['deskripsi']}")
    out.append("")
    out.append(
        "**Permasalahan yang diselesaikan.** "
        + ", ".join(a["masalah"])
        + ". "
        + " ".join(
            next(p["uraian"] for p in PROBLEMS if p["id"] == pid) for pid in a["masalah"]
        )
    )
    out.append("")
    out.append(
        "**Keterkaitan BoK.** "
        + "; ".join(f"BoK {b} {BOK[b]}" for b in a["bok"])
        + ". "
        + a["bok_alasan"]
    )
    out.append("")
    out.append("**Bukti kelayakan dari proyek.**")
    out.append("")
    for b in a["bukti"]:
        out.append(f"- {b['klaim']} Jejak: `{b['jejak']}`.")
    out.append("")
    out.append(f"**Status pelaksanaan.** {a['status']}. {a['status_catatan']}")
    out.append("")
    out.append(f"**Asal usul.** {a['sumber_jenis'][0].upper() + a['sumber_jenis'][1:]}. Kode sumber: {', '.join(a['sumber'])}.")
    out.append("")
    return "\n".join(out)


def tulis_md():
    sekarang = datetime.now(ZoneInfo("Asia/Jakarta"))
    bulan_id = {
        1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei", 6: "Juni",
        7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 11: "November", 12: "Desember",
    }
    tanggal = f"{sekarang.day} {bulan_id[sekarang.month]} {sekarang.year}"
    L = []
    L.append("# BAB III ANALISIS ALTERNATIF SOLUSI")
    L.append("")
    L.append("## 3.1 Permasalahan & Alternatif Solusi")
    L.append("")
    L.append("| Kendali dokumen | Keterangan |")
    L.append("|---|---|")
    L.append("| Dokumen | Proposal Proyek Perancangan Terpadu I, BAB III subbab 3.1 |")
    L.append("| Mitra | PT Halliburton Indonesia, divisi Sperry Drilling |")
    L.append(f"| Versi | 1.0, {tanggal} |")
    L.append("| Status | Berjalan, subbab 3.2 sampai 3.4 belum disusun |")
    L.append("| Acuan format | Buku Pedoman PPT Tahap I, subbab 3.2 Format Proposal, halaman 33 sampai 36 |")
    L.append("| Acuan BoK | Buku Pedoman PPT Tahap I Tabel 2.1, empat belas IEBoK, selaras IISE ISEBoK 2021 |")
    L.append("| Identitas anggota | Diisi tim. Dokumen ini tidak mengarang nama maupun NIM. |")
    L.append("")
    L.append("### 3.1.1 Dasar penyusunan dan aturan bukti")
    L.append("")
    L.append(
        "Riset pendahuluan: `grounded-citations` - setiap angka pada subbab ini melekat pada sumber yang "
        "sudah diekstrak, dan blok bukti memuat kunci jejak berupa berkas dan nomor baris, bukan ingatan."
    )
    L.append("")
    L.append(
        "Riset pendahuluan: `formal-project-documents` - register formal baku tanpa penanda status dalam tanda "
        "kurung, tanpa emoji, dan setiap konsep teknis dituliskan sebagai definisi, tujuan, alasan pemilihan, "
        "serta batasnya."
    )
    L.append("")
    L.append(
        "Riset pendahuluan: `sequentialthinking` (sequ-mcp, empat pikiran) - inventaris dua puluh dua sumber, "
        "uji tiga skema pembagian anggota, verifikasi status eksekusi per solusi, lalu penetapan pembagian "
        "berbasis lapisan intervensi (data dan label, formulasi model, sinyal fisik dan operasi)."
    )
    L.append("")
    L.append(
        "Sembilan alternatif pada subbab ini disusun dari inventaris solusi yang sudah berkode di dalam proyek, "
        "yaitu tiga belas solusi S-A1 sampai S-D4 beserta empat solusi pendukung pada bagian kelas rapuh "
        "(S-E1, S-E2, S-F1, S-F2), tiga opsi peningkatan pada dokumen opsi ML, dan dua lever pasca-V9 "
        "(6a perbaikan label, 6b kalibrasi ambang per sumur). Seluruh dua puluh dua sumber dipetakan tepat satu "
        "kali ke sembilan alternatif, sehingga tidak ada alternatif yang menduplikasi mekanisme alternatif lain, "
        "dan tidak ada sumber yang hilang tanpa rumah."
    )
    L.append("")
    L.append("Aturan bukti yang dipakai pada seluruh subbab:")
    L.append("")
    L.append(
        "1. Setiap angka menyebut berkas dan nomor baris, kunci JSON, atau skrip yang dapat dijalankan ulang."
    )
    L.append(
        "2. Angka yang belum dihitung ditulis eksplisit sebagai asumsi atau perkiraan desain, dan tidak "
        "disamarkan sebagai hasil pengukuran."
    )
    L.append(
        "3. Status pelaksanaan hanya memakai tiga nilai baku: Selesai, Berjalan, dan Rencana (belum terealisasi)."
    )
    L.append("")
    L.append("### 3.1.2 Permasalahan yang dirujuk")
    L.append("")
    L.append(md_tabel_problems())
    L.append("")
    L.append("### 3.1.3 Tabel rekap sembilan alternatif")
    L.append("")
    L.append(md_tabel_rekap())
    L.append("")
    L.append("Tiga anggota membagi lapisan intervensi, bukan kelas disfungsi. Pembagian ini dipilih karena satu "
             "pekerjaan akuisisi data melayani beberapa kelas sekaligus, sehingga pembagian per kelas akan "
             "menduplikasi mekanisme yang sama pada dua alternatif berbeda.")
    L.append("")
    L.append("- Anggota 1 mengerjakan lapisan data dan label (A1 sampai A3).")
    L.append("- Anggota 2 mengerjakan lapisan formulasi model dan evaluasi (A4 sampai A6).")
    L.append("- Anggota 3 mengerjakan lapisan sinyal fisik, keausan, dan operasi (A7 sampai A9).")
    L.append("")
    L.append("### 3.1.4 Rincian setiap alternatif")
    L.append("")
    for a in ALTS:
        L.append(md_rincian(a))
    L.append("### 3.1.5 Peta sumber ke alternatif")
    L.append("")
    L.append("| Sumber | Berkas asal | Alternatif |")
    L.append("|---|---|---|")
    asal = {
        "S-A1": "docs/V7_R1_SOLUTIONS.md:72", "S-A2": "docs/V7_R1_SOLUTIONS.md:79",
        "S-A3": "docs/V7_R1_SOLUTIONS.md:85", "S-B1": "docs/V7_R1_SOLUTIONS.md:103",
        "S-B2": "docs/V7_R1_SOLUTIONS.md:109", "S-B3": "docs/V7_R1_SOLUTIONS.md:115",
        "S-C1": "docs/V7_R1_SOLUTIONS.md:133", "S-C2": "docs/V7_R1_SOLUTIONS.md:139",
        "S-C3": "docs/V7_R1_SOLUTIONS.md:148", "S-D1": "docs/V7_R1_SOLUTIONS.md:167",
        "S-D2": "docs/V7_R1_SOLUTIONS.md:173", "S-D3": "docs/V7_R1_SOLUTIONS.md:179",
        "S-D4": "docs/V7_R1_SOLUTIONS.md:185", "S-E1": "docs/V7_R1_SOLUTIONS.md:198",
        "S-E2": "docs/V7_R1_SOLUTIONS.md:199", "S-F1": "docs/V7_R1_SOLUTIONS.md:204",
        "S-F2": "docs/V7_R1_SOLUTIONS.md:205",
        "V4-Opsi1": "docs/V4_MAINTENANCE_ML_OPTIONS.md:88",
        "V4-Opsi2": "docs/V4_MAINTENANCE_ML_OPTIONS.md:96",
        "V4-Opsi3": "docs/V4_MAINTENANCE_ML_OPTIONS.md:103",
        "6a": "docs/V4_MAINTENANCE_ML_OPTIONS.md:145",
        "6b": "docs/V4_MAINTENANCE_ML_OPTIONS.md:157",
    }
    for s in WAJIB_SUMBER:
        tujuan = next(a["id"] for a in ALTS if s in a["sumber"])
        L.append(f"| {s} | `{asal[s]}` | {tujuan} |")
    L.append("")
    L.append("### 3.1.6 Rekapitulasi status pelaksanaan")
    L.append("")
    L.append("| Status | Alternatif | Keterangan |")
    L.append("|---|---|---|")
    L.append("| Selesai | tidak ada | Tidak ada alternatif yang seluruh mekanismenya selesai. |")
    L.append("| Berjalan | A1, A2, A7 | Mekanisme inti sudah dieksekusi dan berangka; bagian lain belum. |")
    L.append("| Rencana (belum terealisasi) | A3, A4, A5, A6, A8, A9 | Belum ada artefak eksekusi. |")
    L.append("")
    L.append("### 3.1.7 Keterkaitan dengan BoK dan kepatuhan pedoman")
    L.append("")
    L.append("| Alternatif | BoK 1 | BoK 2 | BoK 3 | BoK 5 | BoK 6 | BoK 7 | BoK 10 | BoK 11 | BoK 12 | BoK 14 |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|")
    kolom = [1, 2, 3, 5, 6, 7, 10, 11, 12, 14]
    for a in ALTS:
        sel = " | ".join("ya" if b in a["bok"] else "-" for b in kolom)
        L.append(f"| {a['id']} | {sel} |")
    L.append("")
    L.append(
        "Pedoman menetapkan bahwa pelaksanaan proyek diawali BoK 14 Sistem Design dan Engineering, "
        "melibatkan minimal tiga IEBoK, lalu diakhiri BoK 3 Engineering Economic Analysis. Rancangan sembilan "
        "alternatif mengikuti pola tersebut: A1 memuat BoK 14 dan A9 memuat BoK 3, sedangkan setiap alternatif "
        "memuat tepat tiga BoK sehingga syarat minimal tiga BoK terpenuhi pada tingkat alternatif, bukan hanya "
        "pada tingkat proyek."
    )
    L.append("")
    L.append(
        "Sepuluh dari empat belas BoK tersentuh oleh rancangan ini. Empat BoK yang belum tersentuh adalah BoK 4 "
        "Facilities Engineering and Energy Management, BoK 8 Supply Chain Management, BoK 9 Engineering "
        "Management, dan BoK 13 Product Design and Development. Keempatnya dicatat terbuka agar subbab 3.2 "
        "dapat menilai apakah pengaitan tambahan diperlukan atau justru dipaksakan."
    )
    L.append("")
    L.append("### 3.1.8 Hasil negatif dan batas yang harus dinyatakan")
    L.append("")
    L.append(
        "1. Formulasi onset untuk hyd sudah diuji dan gagal pada titik operasi saat ini: nol dari tiga onset "
        "terdeteksi dengan TLead nol (`docs/V9_EVAL_B_LAYERB.md:103`). Alternatif A1 karena itu tidak boleh "
        "diklaim berhasil untuk semua kelas."
    )
    L.append(
        "2. Dua angka pada subbab ini berstatus asumsi atau perkiraan desain, yaitu rentang prevalensi unit stand "
        "10 sampai 40 persen (`docs/V7_R1_SOLUTIONS.md:111`) dan hasil kalibrasi ambang per sumur yang belum "
        "diukur setelah kalibrasi. Satu angka lain berstatus turunan aritmetik, yaitu plafon lift 2,0 yang berasal "
        "dari satu dibagi prevalensi sekitar 0,5 (`docs/V7_R1_SOLUTIONS.md:164`). Tidak ada di antaranya yang "
        "merupakan hasil ukur."
    )
    L.append(
        "3. Dampak perluasan wellbore pada gate belum dapat diklaim karena re-run fold belum dijalankan, meskipun "
        "baris data hasil parse sudah terukur (`docs/V9_PM1_ARCHITECTURE.md:186`)."
    )
    L.append(
        "4. Fitur dekomposisi mode pada A7 baru berupa rencana pada rancangan, tanpa artefak eksekusi "
        "(`docs/V9_PM1_ARCHITECTURE.md:276`)."
    )
    L.append("")
    L.append("### 3.1.9 Manifes jejak angka (internal, bukan untuk sirkulasi eksternal)")
    L.append("")
    L.append("| Angka | Nilai | Berkas dan baris |")
    L.append("|---|---|---|")
    L.append("| Prevalensi stuck F-9_A | 66,9 persen | `docs/V7_R1_SOLUTIONS.md:66` |")
    L.append("| Persistence mengalahkan RF pada stuck | 0,787 berbanding 0,651 | `docs/V7_R1_SOLUTIONS.md:66` |")
    L.append("| Positif shk per fold | 760 / 259 / 240 / 267 / 41 / 45 / 30 | `docs/V7_R1_SOLUTIONS.md:97` |")
    L.append("| Gate shk | G1 3 dari 7, G2 6 dari 7 | `docs/V7_R1_SOLUTIONS.md:97` |")
    L.append("| Persistence hyd mengalahkan RF | 7 dari 7 fold | `docs/V7_R1_SOLUTIONS.md:127` |")
    L.append("| Gate hyd | G1 2 dari 7, G2 4 dari 7 | `docs/V7_R1_SOLUTIONS.md:127` |")
    L.append("| Gate tool_wear | G1 0 dari 4, G2 4 dari 4 | `docs/V7_R1_SOLUTIONS.md:160` |")
    L.append("| Gate bit_wear | G1 3 dari 4, G2 4 dari 4 | `docs/V7_R1_SOLUTIONS.md:203` |")
    L.append("| Gate ssi | G1 4 dari 5, G2 5 dari 5 | `docs/V7_R1_SOLUTIONS.md:197` |")
    L.append("| Kanal CRPM hasil parse | 281.030 / 42.010 / 178.430 / 57.846 baris | `docs/V9_PM1_ARCHITECTURE.md:186` |")
    L.append("| Syarat kanal per wellbore | 188 / 186 / 125 / 66 / 18 dan seterusnya | `docs/V7_R1_SOLUTIONS.md:43-48` |")
    L.append("| Stuck K-ii B1 dan TLead | B1 0,51 sampai 1,00; TLead 10 sampai 11,5 menit | `docs/V9_EVAL_B_LAYERB.md:101` |")
    L.append("| Persistence-EVENT stuck | TLead median 7,0 menit; B1 0 sampai 11,5 persen | `docs/V9_EVAL_B_LAYERB.md:101` |")
    L.append("| Hyd K-ii | 0 dari 3 onset; TLead nol | `docs/V9_EVAL_B_LAYERB.md:103` |")
    L.append("| tool_wear K-i | 4 dari 4 alat; TLead 20 sampai 36 detik; FP 1 sampai 3 | `docs/V9_EVAL_C_LAYERC.md:98` |")
    L.append("| tool_wear K-ii canary | AUPRC 0,516 sampai 0,612 (1,19 kali) | `docs/V9_EVAL_C_LAYERC.md:99` |")
    L.append("| Sebaran FAR vib | 4,15 sampai 496,09 per 24 jam, rasio 119,6 kali | `docs/V9_PM2_VERDICT.md:114` |")
    L.append("| Kontrol-positif stuck | 0 dari 10 | `docs/V8_PM_VERDICT.md:202` |")
    L.append("| Basis label kurasi | 884 kejadian, 50 relevan BHA, 1.225 jam | `docs/PPT1_LEDGER_ANGKA.md:145, 193` |")
    L.append("| Berkas bhaRun | 77 berkas, tanpa dullingInfo | `docs/V4_MAINTENANCE_ML_OPTIONS.md:62` |")
    L.append("| TSPP | 52.905 baris, 4 berkas, 10 kanal | `docs/V10_D1_BAB_DATA.md:86, 296` |")
    L.append("| Slot alarm otomatis | 0 dari 27 head | `scratch/v9_i1/v9_i1_RESULTS.json` |")
    L.append("")
    L.append("Reproduksi: `python3 scratch/ppt1/build_alternatif.py` menulis ulang `scratch/ppt1/alternatif.json` "
             "dan dokumen ini, lalu menjalankan pemeriksaan acceptance.")
    L.append("")
    L.append("---")
    L.append("")
    L.append("Catatan penyusunan: subbab 3.2 Analisis Alternatif Solusi, 3.3 Kriteria dan Batasan, serta 3.4 "
             "Pemilihan Alternatif Solusi belum termasuk dalam dokumen ini.")
    L.append("")
    md = "\n".join(L)
    path = os.path.join(ROOT, "docs/PPT1_BAB3_1.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)
    return path, md


if __name__ == "__main__":
    galat = periksa()
    jp = tulis_json(galat)
    mp, md = tulis_md()
    emdash = md.count(chr(0x2014))
    print("JSON :", jp)
    print("MD   :", mp)
    print("baris MD:", md.count("\n") + 1, "| karakter:", len(md))
    print("em-dash (U+2014):", emdash)
    print("jumlah alternatif:", len(ALTS))
    for i in (1, 2, 3):
        print(f"  anggota {i}: {sum(1 for a in ALTS if a['anggota'] == i)}")
    print("sumber terpakai unik:", len(set(sum((a['sumber'] for a in ALTS), []))), "dari", len(WAJIB_SUMBER))
    print("BoK terpakai:", sorted({b for a in ALTS for b in a["bok"]}))
    print("BoK belum terpakai:", sorted(set(BOK) - {b for a in ALTS for b in a["bok"]}))
    print("STATUS PERIKSA:", "LOLOS" if not galat else galat)
