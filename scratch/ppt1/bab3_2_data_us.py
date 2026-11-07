"""User stories untuk BAB III subbab 3.3."""

CATATAN_PERAN = (
    "Enam peran di bawah ini adalah peran operasi yang lazim pada pengeboran dan pada pengelolaan alat. "
    "Dua peran memiliki rujukan langsung di dokumen proyek, yaitu insinyur dan driller. Empat peran lain "
    "belum memiliki rujukan dokumen dan belum diverifikasi melalui wawancara mitra. Dasar pernyataan itu: "
    "pencarian kata wawancara dan interview pada seluruh berkas docs/ hanya menemukan dokumen ini sendiri, "
    "dan tidak ada berkas bernama wawancara atau interview di dalam docs/. Status verifikasi peran ditulis "
    "pada setiap cerita, dan verifikasi wawancara dicatat sebagai pekerjaan terbuka."
)

USER_STORIES = [
    {
        "id": "U1",
        "peran": "Insinyur pengeboran Sperry Drilling",
        "peran_status": "Rujukan dokumen ada, wawancara belum dilakukan",
        "dasar": "`docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md:123-126`, yaitu empat skenario penggunaan: konfirmasi status otomatis, peringatan berpengawas manusia yang ditindaklanjuti insinyur, dasbor tren, dan keputusan manusia",
        "cerita": "Sebagai insinyur pengeboran, saya ingin menerima peringatan onset beberapa menit sebelum kondisi memburuk beserta waktu peringatan dan tingkat keyakinannya, agar saya punya waktu memilih tindakan sebelum kejadian berubah menjadi waktu rig yang hilang.",
        "alasan": "Ini pemilik masalah utama, karena seluruh keluaran alat berakhir pada keputusan insinyur dan bukan pada aktuasi otomatis.",
        "alternatif": ["A1", "A8", "A9"],
        "klaster": ["K1", "K4"],
        "kriteria": ["C1", "C2", "C3"],
        "acceptance": [
            {
                "teks": "Pada kelas stuck dengan horizon 10 menit dan titik operasi 0,05, peringatan memberi B1 minimal 0,50 dan TLead median minimal 5 menit.",
                "ambang": "B1 minimal 0,50 dan TLead median minimal 5 menit",
                "jejak": "docs/V9_EVAL_B_LAYERB.md:101",
                "status": "lulus pada kelas stuck, terukur B1 0,51 sampai 1,00 dan TLead 10 sampai 11,5 menit",
            },
            {
                "teks": "Setiap peringatan menampilkan tingkat keyakinan, tier, dan batas pemakaian head yang menghasilkannya.",
                "ambang": "27 dari 27 head memiliki isi pada kunci batas_pemakaian, dan 13 head wajib review manusia",
                "jejak": "scratch/v9_i1/v9_i1_RESULTS.json kunci engines, dalam daftar heads",
                "status": "lulus",
            },
            {
                "teks": "Untuk kelas hidrolik, sistem tidak menampilkan peringatan yang diklaim sebagai deteksi kick atau loss sampai label fisika tersedia.",
                "ambang": "nol klaim deteksi kick pada kelas hyd",
                "jejak": "docs/V9_EVAL_B_LAYERB.md:103",
                "status": "terbuka, menunggu label fisika pada A8, terukur 0 dari 3 onset dengan TLead nol",
            },
        ],
    },
    {
        "id": "U2",
        "peran": "Driller di lantai rig",
        "peran_status": "Rujukan dokumen ada, wawancara belum dilakukan",
        "dasar": "`docs/V8_E_shk_CAPABILITY.md:106` tentang menandai menit yang layak driller cek, dan `docs/V8_R1_ABC_SPEC.md:240` tentang satu pemeriksaan driller per empat jam",
        "cerita": "Sebagai driller, saya ingin menerima daftar menit yang layak diperiksa beserta alasannya, bukan alarm yang memaksa saya berhenti, agar saya tidak kehilangan waktu pada alarm yang salah.",
        "alasan": "Driller adalah penerima keluaran dengan beban kerja paling langsung, sehingga anggaran alarm harus diukur dari pemeriksaan yang ia harus lakukan.",
        "alternatif": ["A9", "A7"],
        "klaster": ["K4"],
        "kriteria": ["C3", "C4", "C8"],
        "acceptance": [
            {
                "teks": "False alarm rate pada titik operasi terpilih tidak lebih dari 6 per 24 jam untuk setiap sumur.",
                "ambang": "FAR maksimal 6 per 24 jam per sumur",
                "jejak": "docs/V8_R1_ABC_SPEC.md:240; docs/V8_E_shk_CAPABILITY.md:106",
                "status": "belum lulus pada shk, karena terukur 18 sampai 63 per 24 jam pada titik operasi 0,05 sampai 0,10",
            },
            {
                "teks": "Tidak ada slot alarm otomatis kritis pada alat.",
                "ambang": "auto_critical_alarm_slots sama dengan 0",
                "jejak": "scratch/v9_i1/v9_i1_RESULTS.json kunci auto_critical_alarm_slots",
                "status": "lulus",
            },
            {
                "teks": "Keluaran berupa satu baris peringatan dengan waktu, keyakinan, dan tindakan yang disarankan, sehingga tidak menuntut driller menafsirkan model.",
                "ambang": "rubrik beban kognitif tingkat 3 sesuai kriteria C8",
                "jejak": "docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md:123-126",
                "status": "terbuka, karena antarmuka belum dirancang",
            },
        ],
    },
    {
        "id": "U3",
        "peran": "Toolhand penanggung jawab bengkel alat",
        "peran_status": "Peran operasi, belum ada rujukan dokumen dan belum diverifikasi",
        "dasar": "Kebutuhan diturunkan dari domain data bengkel, yaitu 4 alat dan 2 run dengan 469 jendela (`docs/V9_PM1_ARCHITECTURE.md:276`); nama peran belum ada di dokumen proyek",
        "cerita": "Sebagai toolhand, saya ingin tahu alat mana yang sedang menuju akhir umur dan seberapa cepat, agar penggantian dilakukan sebelum kerusakan memaksa berhenti.",
        "alasan": "Satu-satunya domain pada proyek ini yang sudah memiliki ambang alarm terkalibrasi adalah domain bengkel, sehingga peran ini paling cepat menerima manfaat.",
        "alternatif": ["A7"],
        "klaster": ["K4"],
        "kriteria": ["C1", "C5"],
        "acceptance": [
            {
                "teks": "Titik perubahan terdeteksi pada setiap alat yang diuji.",
                "ambang": "4 dari 4 alat",
                "jejak": "docs/V9_EVAL_C_LAYERC.md:98",
                "status": "lulus",
            },
            {
                "teks": "Waktu ancang sebelum titik perubahan minimal 20 detik.",
                "ambang": "TLead 20 sampai 36 detik, yaitu 1,8 kali",
                "jejak": "docs/V9_EVAL_C_LAYERC.md:98",
                "status": "lulus",
            },
            {
                "teks": "Jumlah alarm palsu per alat tidak lebih dari 3 setelah kalibrasi, dan presisi per run dinyatakan terbuka.",
                "ambang": "false positive 1 sampai 3 per alat, presisi run 0,50 dilaporkan",
                "jejak": "docs/V9_EVAL_C_LAYERC.md:98",
                "status": "lulus dengan catatan, karena presisi run 0,50 berarti separuh titik ubah terjadi pada alat baru",
            },
        ],
    },
    {
        "id": "U4",
        "peran": "Manajer operasi Sperry Drilling",
        "peran_status": "Peran operasi, belum ada rujukan dokumen dan belum diverifikasi",
        "dasar": "Kebutuhan diturunkan dari struktur registry yang memberi tier dan batas pemakaian per head (`scratch/v9_i1/v9_i1_RESULTS.json`)",
        "cerita": "Sebagai manajer operasi, saya ingin setiap klaim alat membawa tingkat kesiapan dan batasnya, agar saya dapat memutuskan pemakaian tanpa menanggung klaim yang berlebih.",
        "alasan": "Keputusan memakai alat di lapangan adalah keputusan manajerial, dan risiko klaim berlebih bersifat organisasi, bukan teknis.",
        "alternatif": ["A3", "A5", "A9"],
        "klaster": ["K1", "K3", "K4"],
        "kriteria": ["C4", "C7"],
        "acceptance": [
            {
                "teks": "Setiap head membawa tier, batas pemakaian, dan lencana false alarm.",
                "ambang": "27 dari 27 head terisi ketiga kunci tersebut",
                "jejak": "scratch/v9_i1/v9_i1_RESULTS.json kunci engines, dalam daftar heads, kunci tier, batas_pemakaian, badge_far",
                "status": "lulus",
            },
            {
                "teks": "Head yang belum layak pakai tidak dipakai di tingkat mana pun.",
                "ambang": "2 head berstatus belum layak pakai dinyatakan terbuka",
                "jejak": "scratch/v9_i1/v9_i1_RESULTS.json, nilai tier BELUM LAYAK PAKAI pada engine hyd dan bit_wear",
                "status": "lulus",
            },
            {
                "teks": "Setiap angka pada laporan manajemen menunjuk berkas dan baris atau kunci JSON.",
                "ambang": "nol angka tanpa jejak pada pemeriksa",
                "jejak": "scratch/ppt1/check_bab3_2.py; docs/PPT1_LEDGER_ANGKA.md",
                "status": "lulus pada dokumen ini, diperiksa skrip",
            },
        ],
    },
    {
        "id": "U5",
        "peran": "Insinyur data dan kinerja",
        "peran_status": "Peran operasi, belum ada rujukan dokumen dan belum diverifikasi",
        "dasar": "Kebutuhan diturunkan dari adanya pipeline registry `code/v9_i1_pipeline.py` dan berkas hasil `scratch/v9_i1/v9_i1_RESULTS.json`",
        "cerita": "Sebagai insinyur data, saya ingin dapat menjalankan ulang pipeline dan evaluasi dari skrip yang tersimpan, agar angka pada proposal dapat diaudit oleh pihak lain.",
        "alasan": "Tanpa reproduksibilitas, seluruh klaim hanya dapat dipercaya atas dasar kepercayaan, dan itu tidak cukup untuk mitra industri.",
        "alternatif": ["A2", "A5"],
        "klaster": ["K2", "K3"],
        "kriteria": ["C2", "C7"],
        "acceptance": [
            {
                "teks": "Registry dapat dihitung ulang dari skrip yang tersimpan.",
                "ambang": "code/v9_i1_pipeline.py tersedia dan head terhitung 27 dari 7 engine",
                "jejak": "code/v9_i1_pipeline.py; docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md:57",
                "status": "sebagian, karena skrip tersedia dan jumlah head terverifikasi dari JSON, tetapi eksekusi ulang belum dijalankan pada kartu ini",
            },
            {
                "teks": "Setiap lapisan keputusan dapat ditelusuri ke head asalnya.",
                "ambang": "jumlah head pada empat lapisan sama dengan 27",
                "jejak": "scratch/v9_i1/v9_i1_RESULTS.json kunci decision_layer, lapisan L0 sampai L3",
                "status": "lulus",
            },
            {
                "teks": "Perubahan definisi label tercatat sebagai versi, bukan sebagai penimpaan.",
                "ambang": "satu varian onset dikunci dan varian lain dicatat",
                "jejak": "docs/V4_MAINTENANCE_ML_OPTIONS.md:145",
                "status": "terbuka, karena audit label belum dijalankan",
            },
        ],
    },
    {
        "id": "U6",
        "peran": "Pengawas well-control",
        "peran_status": "Peran operasi, belum ada rujukan dokumen dan belum diverifikasi",
        "dasar": "Kebutuhan diturunkan dari BoK 10 Safety dan dari status label hyd yang masih proksi (`docs/V8_PM_VERDICT.md:202`)",
        "cerita": "Sebagai pengawas well-control, saya ingin alat tidak pernah menyatakan kick atau kehilangan sirkulasi secara otomatis, agar tidak ada keputusan keselamatan yang bergantung pada label proksi.",
        "alasan": "Kick dan lost circulation adalah bahaya well-control. Klaim deteksi otomatis pada label proksi akan menjadi tanggung jawab keselamatan yang tidak dapat dipertanggungjawabkan.",
        "alternatif": ["A8"],
        "klaster": ["K1"],
        "kriteria": ["C4", "C7"],
        "acceptance": [
            {
                "teks": "Nol klaim deteksi kick atau loss secara otomatis pada seluruh keluaran alat.",
                "ambang": "auto_critical_alarm_slots sama dengan 0 dan nol head berlabel kick otomatis",
                "jejak": "scratch/v9_i1/v9_i1_RESULTS.json kunci auto_critical_alarm_slots, dan head hyd k2_tidak_tersedia pada tier BELUM LAYAK PAKAI",
                "status": "lulus",
            },
            {
                "teks": "Status label hidrolik dinyatakan sebagai proksi pada setiap dokumen yang memuatnya.",
                "ambang": "satu pernyataan proksi pada dokumen ini dan pada verdict",
                "jejak": "docs/V8_PM_VERDICT.md:202",
                "status": "lulus",
            },
            {
                "teks": "Label fisika, yaitu perubahan volume pit dan selisih laju alir, dicatat sebagai prasyarat sebelum klaim well-control apa pun dibuat.",
                "ambang": "kanal sumber label terdaftar dan terhitung",
                "jejak": "docs/V7_R1_SOLUTIONS.md:37-38",
                "status": "terbuka, karena label pit dan flow belum diparse menjadi deret label",
            },
        ],
    },
]

MATRIKS_US_KRITERIA = {
    "U1": ["C1", "C2", "C3"],
    "U2": ["C3", "C4", "C8"],
    "U3": ["C1", "C5"],
    "U4": ["C4", "C7"],
    "U5": ["C2", "C7"],
    "U6": ["C4", "C7"],
}
