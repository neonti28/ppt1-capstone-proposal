#!/usr/bin/env python3
# Build docs/PPT1_LEDGER_ANGKA.md + scratch/ppt1/ledger.json dari SATU sumber data
# supaya tabel markdown dan JSON tidak mungkin berbeda isi.
import json, os, collections

BASE = "/mnt/d/Capstone 1(v2)"
DOCX = "Proposal_PPT_I_SperryDrilling_ML_NPT.docx (13 Agu 2026)"
MD = "docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md"
SESS = "@session:default/20260813_185624_605c0c pesan 10791"

# status kanonik: TERUKUR | ASUMSI | WARISAN-DRAFT
# sub: kualifikasi bukti (TARGET = angka sasaran, EKSTERNAL = angka pihak ketiga terverifikasi,
#      LITERAL-GENERATOR = ditulis literal di skrip generator, DIHITUNG-ULANG = saya jalankan sendiri)
R = []

def row(gid, angka, konteks, sumber, status, sub, verifikasi, temuan=""):
    R.append(dict(id=gid, grup=gid[0], angka=angka, konteks=konteks, sumber=sumber,
                  status=status, sub=sub, verifikasi=verifikasi, temuan=temuan))

# ============ GRUP A: DRAFT DOCX 13 AGU 2026 ============
src = DOCX + " baris ekstraksi teks (read_file), "
row("A01", "3 mahasiswa", "Ukuran tim proyek (mono-discipline)", src + "l.19",
    "WARISAN-DRAFT", "LITERAL-GENERATOR", "Cocokkan dengan daftar anggota resmi kelompok di SIMAK/berita acara",
    "Angka administratif, bukan hasil ukur; tidak perlu diganti kecuali jumlah anggota berubah")
row("A02", "2 SKS", "Bobot mata kuliah PPT I", src + "l.25",
    "WARISAN-DRAFT", "LITERAL-GENERATOR", "Cek Buku Pedoman PPT h.1-5 (beban SKS) dan KRS semester 7",
    "Administratif; verifikasi ke pedoman, bukan ke data")
row("A03", "Semester 7", "Semester pelaksanaan", src + "l.25",
    "WARISAN-DRAFT", "LITERAL-GENERATOR", "Cek KRS/transkrip anggota", "Administratif")
row("A04", "2026/2027", "Tahun akademik", src + "l.27",
    "WARISAN-DRAFT", "LITERAL-GENERATOR", "Cek kalender akademik UNS", "Administratif")
row("A05", "pekan ke-10", "Batas penetapan mentor dosen (pedoman 2.7)", src + "l.29",
    "WARISAN-DRAFT", "LITERAL-GENERATOR", "Baca pedoman PPT bagian 2.7 (penetapan mentor)",
    "Rujukan prosedural, bukan angka hasil")
row("A06", "9 Juli 2026", "Tanggal deployment closed-loop rig automation Eni+Halliburton deepwater Indonesia", src + "l.57 dan l.328",
    "TERUKUR", "EKSTERNAL",
    "Buka https://www.halliburton.com/en/about-us/press-release/eni-halliburton-achieve-industry-first-closed-loop-rig-automation-indonesia (terverifikasi 25 Okt 2026, juga di ir.halliburton.com)",
    "Sumber primer ada dan bertanggal HOUSTON, July 9, 2026")
row("A07", "efisiensi >15%", "Klaim vendor: LOGIX Orchestration + MPD menaikkan efisiensi pengeboran", src + "l.57",
    "TERUKUR", "EKSTERNAL",
    "Sumber sama A06: kalimat 'improved efficiency by more than 15%' ada di press release; cross-check worldoil.com 2026/7/9",
    "BUKAN hasil proyek kita. Wajib dikutip dengan atribusi vendor; dilarang menjadi janji luaran proposal")
row("A08", "10-30 menit (lead time)", "Target sistem mendeteksi dysfunction sebelum kejadian (1.1.5)", src + "l.80",
    "ASUMSI", "TARGET", "Tidak ada run yang mencapainya: MD §1.1 baris 63-67 menyatakan 0 engine memenuhi syarat alarm; MD baris 3431 mensyaratkan FAR<=6/24jam dulu",
    "Harus ditulis sebagai target, bukan hasil")
row("A09", "S=9, O=7, D=6, RPN=378", "FMEA mode 'Excessive vibration'", src + "l.137-140; literal di " + SESS,
    "WARISAN-DRAFT", "LITERAL-GENERATOR",
    "python3 scratch/ppt1/arith_audit.py (RPN cocok 5/5) + telusur literal ke " + SESS,
    "Aritmetika RPN benar, tetapi S/O/D tidak punya tabel justifikasi skala. Menunggu kartu R1/B2")
row("A10", "S=8, O=7, D=5, RPN=280", "FMEA mode 'Stick-slip'", src + "l.144-147; literal di " + SESS,
    "WARISAN-DRAFT", "LITERAL-GENERATOR", "python3 scratch/ppt1/arith_audit.py",
    "Sama seperti A09")
row("A11", "S=9, O=6, D=6, RPN=324", "FMEA mode 'Pressure anomaly'", src + "l.150-154; literal di " + SESS,
    "WARISAN-DRAFT", "LITERAL-GENERATOR", "python3 scratch/ppt1/arith_audit.py",
    "Sama seperti A09")
row("A12", "S=7, O=5, D=7, RPN=245", "FMEA mode 'Telemetry failure'", src + "l.157-161; literal di " + SESS,
    "WARISAN-DRAFT", "LITERAL-GENERATOR", "python3 scratch/ppt1/arith_audit.py",
    "Sama seperti A09")
row("A13", "S=8, O=6, D=5, RPN=240", "FMEA mode 'Bit/BHA dysfunction'", src + "l.164-168; literal di " + SESS,
    "WARISAN-DRAFT", "LITERAL-GENERATOR", "python3 scratch/ppt1/arith_audit.py",
    "Sama seperti A09")
row("A14", "~1 Hz", "Asumsi laju stream telemetri masukan", src + "l.224",
    "ASUMSI", "DESAIN", "Pipeline V9 memakai grid 60 detik (docs/V9_D1_DATA_PIPELINE.md), bukan 1 Hz",
    "Tidak didukung data yang benar-benar dipakai; turunkan ke 1/60 Hz atau hapus")
row("A15", "window=30, step=5", "Rolling window preprocessing", src + "l.225",
    "ASUMSI", "DESAIN", "Cek kontrak grid di docs/V9_D1_DATA_PIPELINE.md dan 6 dataset latih scratch/v9_d1/datasets",
    "Hyperparameter usulan, belum diuji sensitivitasnya di dokumen ini")
row("A16", "n_estimators=300", "Hyperparameter Random Forest", src + "l.229",
    "ASUMSI", "DESAIN", "Cek kontrak model di MD §3 (Bab 4) dan skrip RF di code/",
    "Hyperparameter, bukan hasil")
row("A17", "recall >=0,70-0,80", "Target KPI deteksi", src + "l.233",
    "ASUMSI", "TARGET", "Bandingkan dengan hasil terukur MD baris 2972-2982: recall rule 0,276-0,595 (vib), 0,000-0,032 (ssi), 0,449-0,599 (stuck K-i); FAR 14,62-58,43 (hyd)",
    "Target lebih tinggi dari hampir semua hasil terukur. Wajib dilabeli target")
row("A18", "lead time 10-30 menit", "Target KPI (3.1.1.E)", src + "l.233",
    "ASUMSI", "TARGET", "Hasil terukur MD baris 2976: TLead stuck K-ii 4,5-8,5 menit (median 7,0); tool_wear 20-36 detik (domain bengkel, D-A7)",
    "Target belum tercapai di domain rig; lihat juga V8_PM_VERDICT baris 199 (G4)")
row("A19", "bobot K1=0,25", "MCDM/TOPSIS bobot kriteria 'Recall/efektivitas'", src + "l.262",
    "WARISAN-DRAFT", "LITERAL-GENERATOR", "Tidak ada berita acara pembobotan stakeholder; " + SESS + " memuatnya literal",
    "Bobot tidak punya jejak elisitasi. Harus ditulis 'bobot usulan penulis'")
row("A20", "bobot K2=0,20", "MCDM/TOPSIS bobot 'Lead time'", src + "l.263",
    "WARISAN-DRAFT", "LITERAL-GENERATOR", "Sama A19", "")
row("A21", "bobot K3=0,15", "MCDM/TOPSIS bobot 'Explainability'", src + "l.264",
    "WARISAN-DRAFT", "LITERAL-GENERATOR", "Sama A19", "")
row("A22", "bobot K4=0,10", "MCDM/TOPSIS bobot 'Biaya implementasi'", src + "l.265",
    "WARISAN-DRAFT", "LITERAL-GENERATOR", "Sama A19", "")
row("A23", "bobot K5=0,15", "MCDM/TOPSIS bobot 'Kemudahan integrasi'", src + "l.266",
    "WARISAN-DRAFT", "LITERAL-GENERATOR", "Sama A19", "")
row("A24", "bobot K6=0,15", "MCDM/TOPSIS bobot 'ROI'", src + "l.267",
    "WARISAN-DRAFT", "LITERAL-GENERATOR", "Sama A19; total bobot = 1,00 (dicek arith_audit.py)", "")
row("A25", "skala 1-5", "Skala penilaian kriteria", src + "l.260",
    "WARISAN-DRAFT", "LITERAL-GENERATOR", "grep -rl 'skala 1-5\\|rubrik skala' docs/*.md | grep -v PPT1_LEDGER_ANGKA | wc -l -> 0 (tidak ada rubrik skala di dokumen tim mana pun)",
    "Perlu rubrik eksplisit agar skor bisa diaudit")
row("A26", "skor A1 = 4,35", "Skor akhir alternatif ML Classifier", src + "l.276",
    "WARISAN-DRAFT", "LITERAL-GENERATOR", "python3 scratch/ppt1/arith_audit.py: weighted-sum = 4,35 (COCOK); TOPSIS closeness = 0,8306",
    "Satu-satunya baris yang bisa direproduksi dengan bobot tertulis")
row("A27", "skor A2 = 3,40", "Skor akhir IsoForest", src + "l.284",
    "WARISAN-DRAFT", "LITERAL-GENERATOR", "python3 scratch/ppt1/arith_audit.py: weighted-sum = 3,35 (selisih +0,05, TIDAK cocok); TOPSIS CC = 0,5213",
    "TEMUAN: skor tidak reproducible. Di TOPSIS sejati A2 mengalahkan A3, sedangkan draft menaruh A3 (3,55) di atas A2 (3,40)")
row("A28", "skor A3 = 3,55", "Skor akhir SHAP Dashboard", src + "l.292",
    "WARISAN-DRAFT", "LITERAL-GENERATOR", "python3 scratch/ppt1/arith_audit.py: weighted-sum = 3,50 (selisih +0,05)",
    "TEMUAN: urutan A3 di atas A2 tidak bertahan pada TOPSIS sejati (A3 0,4255 < A2 0,5213)")
row("A29", "skor A4 = 2,95", "Skor akhir Rule-based", src + "l.300",
    "WARISAN-DRAFT", "LITERAL-GENERATOR", "python3 scratch/ppt1/arith_audit.py: weighted-sum = 3,00 (selisih -0,05)", "")
row("A30", "skor A6 = 2,45", "Skor akhir Integrasi LOGIX", src + "l.308",
    "WARISAN-DRAFT", "LITERAL-GENERATOR", "python3 scratch/ppt1/arith_audit.py: weighted-sum = 2,40 (selisih +0,05)", "")
row("A31", "9 alternatif (3 anggota x 3)", "Struktur Bab III 3.1", src + "l.180",
    "WARISAN-DRAFT", "LITERAL-GENERATOR", "Hitung baris tabel A1-A9 pada l.185-220 = 9 baris",
    "Aman dipakai; hanya perlu memastikan tiap anggota benar menyumbang 3")
row("A32", "5 BOK terlibat", "Kedalaman BOK Bab III", src + "l.251",
    "WARISAN-DRAFT", "LITERAL-GENERATOR", "Hitung baris tabel BOK l.241-250 = 5 BOK (14, 11, 5, 3, 6)",
    "Sesuai, tetapi BOK harus dipetakan ke isi bab, bukan hanya didaftar")
row("A33", "6 kriteria (K1-K6)", "Kriteria MCDM", src + "l.258",
    "WARISAN-DRAFT", "LITERAL-GENERATOR", "Hitung K1..K6 di l.258 dan header tabel l.262-267", "")
row("A34", "14 BOK TI", "Jumlah BOK dalam body of knowledge IISE", src + "l.238",
    "WARISAN-DRAFT", "LITERAL", "Cek IISE ISE BoK (https://www.iise.org/Details.aspx?id=43631) sebelum final",
    "Perlu verifikasi eksternal sekali, lalu dikutip dengan sitasi")
row("A35", "4 cabang FTA", "TOP event NPT dengan 4 anak OR", src + "l.173",
    "WARISAN-DRAFT", "LITERAL-GENERATOR", "Hitung cabang pada l.173: vibration, stick-slip, pressure-anomaly, telemetry-loss",
    "Konsisten dengan 5 mode FMEA minus bit/BHA, perlu dirapikan")
row("A36", "6M fishbone", "Kategori cause fishbone", src + "l.171",
    "WARISAN-DRAFT", "LITERAL-GENERATOR", "Hitung kategori l.83: Man, Method, Machine, Material, Measurement, Environment = 6", "")
row("A37", "10 pertanyaan ke supervisor", "Rencana pengumpulan data", src + "l.318",
    "WARISAN-DRAFT", "LITERAL-GENERATOR", "Cari daftar 10 pertanyaan; tidak ada lampirannya di docx",
    "Rujukan menggantung: daftar 10 pertanyaan tidak dilampirkan")
row("A38", "1 kanal publikasi", "Luaran wajib (2.9)", src + "l.320",
    "WARISAN-DRAFT", "LITERAL", "Cek pedoman 2.9 untuk syarat luaran", "Prosedural")

# ============ GRUP B: MD TECHNICAL DESIGN ============
m = MD + " baris "
row("B01", "7 engine", "Jumlah kelas kegagalan yang dideteksi", m + "57 (dan 55)",
    "TERUKUR", "DIHITUNG-ULANG", "python3 scratch/ppt1/verify_numbers.py -> registry_heads_per_engine (7 kunci engine)",
    "Cocok dengan registry yang dieksekusi")
row("B02", "11 klaim", "Sub-tugas terpisah (3x1 + 4x2)", m + "57",
    "TERUKUR", "DIHITUNG-ULANG", "python3 scratch/ppt1/verify_numbers.py -> registry_heads_per_engine: engine dengan 6 head (stuck) = 2 tugas; 3 engine tugas tunggal",
    "3x1+4x2 = 11 konsisten")
row("B03", "27 head (4+4+4+6+4+2+3)", "Varian metode yang benar-benar dievaluasi", m + "57 dan docs/V10_PM2_VERDICT.md baris 39-41",
    "TERUKUR", "DIHITUNG-ULANG", "python3 scratch/ppt1/verify_numbers.py -> registry_heads_n = 27; registry_heads_per_engine = vib 4, ssi 4, shk 4, stuck 6, hyd 4, bit_wear 2, tool_wear 3",
    "Sebaran identik dengan verdict V10")
row("B04", "tier 0/3/2/2 dan 7 dari 7", "Status kemampuan 7 engine (alarm, peringatan, bersyarat, tren)", m + "63-67",
    "TERUKUR", "DIHITUNG-ULANG", "python3 scratch/ppt1/verify_numbers.py -> registry_tier_counts = PERINGATAN-BERPENGAWAS 12, TREN 13, BELUM LAYAK PAKAI 2 (head); rekap engine 0+3+2+2=7 di docs/V10_PM2_VERDICT.md baris 13",
    "Level engine (7) dan level head (27) beda; jangan dijumlah")
row("B05", "884 kejadian", "Populasi kejadian di label terkurasi", m + "1405 dan 1435",
    "TERUKUR", "DIHITUNG-ULANG", "python3 scratch/ppt1/verify_numbers.py -> labels_v2_n = 884 (csv.DictReader, bukan wc -l)",
    "COCOK PERSIS")
row("B06", "496/216/47/38/28/25/21/12/1", "Distribusi 884 kejadian per kategori", m + "1405",
    "TERUKUR", "DIHITUNG-ULANG", "python3 scratch/ppt1/verify_numbers.py -> category_counts_desc",
    "COCOK PERSIS; 496 = routine_no_failure_evidence (56,1%) sehingga klaim '884 kejadian kerusakan' harus dikoreksi")
row("B07", "bha_relevant yes 50 / no 263 / uncertain 571", "Relevansi BHA dari 884 kejadian", m + "1405",
    "TERUKUR", "DIHITUNG-ULANG", "python3 scratch/ppt1/verify_numbers.py -> bha_relevant",
    "COCOK PERSIS. Hanya 50 kejadian (5,7%) benar-benar relevan BHA: penting untuk latar belakang")
row("B08", "198.928 baris", "Data baris USROP_labeled.csv", m + "1387-1391 dan 1434",
    "TERUKUR", "DIHITUNG-ULANG", "wc -l data/USROP_labeled.csv -> 198.929 baris termasuk header; 198.928 data",
    "Cocok setelah koreksi header")
row("B09", "18 kolom", "Jumlah kolom USROP_labeled.csv", m + "1387-1391",
    "TERUKUR", "DIHITUNG-ULANG", "head -1 data/USROP_labeled.csv | tr ',' '\\n' | wc -l -> 18",
    "MD mengoreksi klaim kartu '115 kolom' (itu depth.csv F-9A). Koreksi TERBUKTI")
row("B10", "239 kolom (time.csv F-9A)", "Total kolom WITSML time.csv", m + "1393-1401",
    "TERUKUR", "DILAPORKAN", "head -1 'data/witsml/Norway-NA-15_47_9-F-9 A time.csv' | tr ',' '\\n' | wc -l",
    "Belum saya hitung ulang sesi ini")
row("B11", "13 kolom pit", "Kolom MudPit Volume Average", m + "1393-1401",
    "TERUKUR", "DILAPORKAN", "grep -o 'MudPit Volume Average[0-9 ]*' header time.csv | sort -u | wc -l",
    "MD menjelaskan akar selisih 12 vs 13 (kolom 3 dan 13 tanpa spasi)")
row("B12", "7.080.457 baris / 8 CSV", "Baris WITSML hasil parse V3", m + "1403",
    "TERUKUR", "DIHITUNG-ULANG-SEBAGIAN", "ls data/volve/witsml_parsed/*.csv | wc -l -> 10 berkas; python3 scratch/ppt1/verify_numbers.py -> total baris mentah 9.935.708",
    "9.935.708 - 10 header = 9.935.698 = angka MD baris 1433. Selisih 10 dijelaskan header, bukan kontradiksi")
row("B13", "9.935.698 baris / 10 CSV", "Baris dan berkas WITSML di folder v2", m + "1403 dan 1433",
    "TERUKUR", "DIHITUNG-ULANG", "python3 scratch/ppt1/verify_numbers.py -> witsml_parsed_total_lines = 9.935.708 (mentah)",
    "Cocok bila header 10 baris dikurangkan")
row("B14", "192 XML tubular / 1.392 komponen", "Inventaris tubular", m + "1406",
    "TERUKUR", "DIHITUNG-ULANG", "find data/volve/witsml_raw -path '*tubular*' -name '*.xml' | wc -l -> 192",
    "192 COCOK; 1.392 komponen belum saya hitung")
row("B15", "161 bhaRun / 154 cocok uidRef", "Keterkaitan bhaRun ke tubular", m + "1407",
    "TERUKUR", "DIHITUNG-ULANG-SEBAGIAN", "find data/volve/witsml_raw -path '*bhaRun*' -name '*.xml' | wc -l -> 161",
    "161 COCOK; rasio 154/161 dilaporkan di V7_A1_AUDIT D5")
row("B16", "63 trajectory / 5.561 stasiun", "Inventaris trajectory", m + "1408",
    "TERUKUR", "DIHITUNG-ULANG-SEBAGIAN", "find data/volve/witsml_raw -path '*trajectory*' -name '*.xml' | wc -l -> 63",
    "63 COCOK; 5.561 stasiun belum dihitung ulang")
row("B17", "27 wbGeometry / 109 section", "Inventaris geometri sumur", m + "1408",
    "TERUKUR", "DIHITUNG-ULANG-SEBAGIAN", "find data/volve/witsml_raw -path '*wbGeometry*' -name '*.xml' | wc -l -> 27",
    "27 COCOK")
row("B18", "8 mudLog / 2.882 interval", "Inventaris mud log", m + "1408",
    "TERUKUR", "DIHITUNG-ULANG-SEBAGIAN", "find data/volve/witsml_raw -path '*mudLog*' -name '*.xml' | wc -l -> 8",
    "8 COCOK")
row("B19", "21 CSV / 309.644 baris (DLIS/PETRO)", "Data petrofisika", m + "1409",
    "TERUKUR", "DIHITUNG-ULANG", "ls '/mnt/d/Capstone 1/scratch/v6_d1f/csv/' | wc -l -> 21; wc -l csv/*.csv -> 309.665 (kurang 21 header = 309.644)",
    "COCOK; berkas ada di arsip, bukan v2")
row("B20", "469 jendela / 27 fitur (toolwear)", "Dataset keausan alat", m + "1409",
    "TERUKUR", "DIHITUNG-ULANG", "python3 scratch/ppt1/verify_numbers.py -> toolwear_windows_rows = 469 (32 kolom termasuk id+label)",
    "469 COCOK")
row("B21", "4 CSV utama / 52.905 baris (TSPP)", "Kanal permukaan frekuensi tinggi", m + "1410 dan 1440",
    "TERUKUR", "DIHITUNG-ULANG-SEBAGIAN", "ls data/bo_tspp/TSPP*.csv -> 7 berkas (TSPP1-4 + varian 15s/long + AE_SCORES); 4 utama = TSPP1..4",
    "4 utama konsisten; 3 berkas turunan harus disebut agar tidak dianggap hilang")
row("B22", "10.650 CD_ASSEMBLY_COMP / 632 CD_BHA_COMP_BIT (EDM)", "Data keausan alat dari EDM", m + "1410",
    "TERUKUR", "DILAPORKAN", "Hitung ulang dari sumber EDM di data/ (lihat V6_D1g_EDM.md)", "Belum saya hitung ulang")
row("B23", "6 dataset latih / 292.954 baris", "Dataset siap latih", m + "1411-1413",
    "TERUKUR", "DIHITUNG-ULANG", "python3 scratch/ppt1/verify_numbers.py -> train_datasets_n = 6, train_datasets_rows_sum = 292.954; python3 scratch/ppt1/verify_leak.py -> 6 dataset per nama",
    "COCOK PERSIS dengan kontrol aritmetika MD baris 1413")
row("B24", "23.922+35.906+56.495+5.555+52.509+118.567 = 292.954", "Kontrol aritmetika dataset", m + "1413",
    "TERUKUR", "DIHITUNG-ULANG", "python3 scratch/ppt1/verify_leak.py -> n_rows vib 23922, ssi 35906, shk 56495, stuck_k1 5555, hyd_ki 52509, stuck_k2 118567",
    "Keenam suku cocok satu per satu, jumlah cocok")
row("B25", "37 fold LOWO (4+9+9+2+9+4)", "Skema validasi leave-one-well-out", m + "1411 dan 1414",
    "TERUKUR", "DIHITUNG-ULANG", "python3 scratch/ppt1/verify_leak.py -> n_folds 4, 9, 9, 2, 9, 4 sehingga total 37",
    "COCOK PERSIS dengan kontrol aritmetika MD baris 1414")
row("B26", "0 pelanggaran anti-bocor 6/6", "Uji kebocoran fitur", m + "1411",
    "TERUKUR", "DIHITUNG-ULANG", "python3 scratch/ppt1/verify_leak.py -> TOTAL leak violations: 0, status OK untuk 6/6 dataset",
    "COCOK; seluruh dataset berstatus OK")
row("B27", "vib 4 fold, AUPRC 0,4405-0,9117", "Hasil RF engine vib", m + "1718",
    "TERUKUR", "DIHITUNG-ULANG-SEBAGIAN", "Cek agregat di scratch/v9_e_ml/*vib*.json; nilai fold F-14 verifikasi baris 1727",
    "Rentang konsisten dengan baris fold 1727-1730")
row("B28", "ssi 9 fold (2 underpowered), 0,0151-0,4589", "Hasil RF engine ssi", m + "1719",
    "TERUKUR", "DIHITUNG-ULANG-SEBAGIAN", "Cek agregat scratch/v9_e_ml/*ssi*.json; baris fold 1743-1751",
    "2 fold UP = F-7 dan F-9 (n=982, n=1126)")
row("B29", "shk 9 fold, 0,0069-0,1929", "Hasil RF engine shk", m + "1720",
    "TERUKUR", "DIHITUNG-ULANG-SEBAGIAN", "Cek agregat scratch/v9_e_ml/*shk*.json; baris fold 1763-1771",
    "Rentang cocok dengan baris fold")
row("B30", "stuck K-ii 4 fold, 0,0697-0,4443", "Hasil RF onset stuck", m + "1721",
    "TERUKUR", "DIHITUNG-ULANG-SEBAGIAN", "Cek agregat scratch/v9_e_ml/*stuck*.json",
    "ΔB vs persistence 0/4: persistence menang, dilaporkan jujur")
row("B31", "F-14 vib: n=1989, pos=1124, prev 0,5651, AUPRC 0,9117", "Baris fold pertama vib", m + "1727",
    "TERUKUR", "DIHITUNG-ULANG", "python3 scratch/ppt1/verify_numbers.py -> segmen_info vib n = 1989 (registry)",
    "n COCOK dengan registry; AUPRC per fold dari JSON")
row("B32", "rule vib P 0,868-0,952", "Presisi rule ambang vib", m + "2972",
    "TERUKUR", "DIHITUNG-ULANG-SEBAGIAN", "Cek scratch/v9_e_rule/*vib*.json field precision", "Angka tabel 11 klaim")
row("B33", "vib FAR 9,99-49,94 dan τ0,5 FAR 4,15-496,09 (119,57x)", "Alarm palsu per 24 jam vib", m + "2972",
    "TERUKUR", "DIHITUNG-ULANG-SEBAGIAN", "496,09/4,15 = 119,54 dari endpoint yang dibulatkan; dokumen menulis 119,57 karena memakai nilai penuh sebelum pembulatan. Cek JSON FAR per fold",
    "Selisih 0,03 murni pembulatan endpoint, arah kesimpulan sama (FAR menyebar sekitar 120x antar sumur)")
row("B34", "ssi nodata CRPM 22.385/35.906 = 62,34%", "Keterbatasan sensor stick-slip", m + "2973",
    "TERUKUR", "DIHITUNG-ULANG-SEBAGIAN", "22.385/35.906 = 0,6234; n 35.906 cocok dengan dataset ssi",
    "n dataset cocok; pembilang belum saya hitung ulang")
row("B35", "stuck K-i FAR 8,32-61,0, <=6 di 0/2, 2 fold", "Cakupan engine stuck", m + "2975",
    "TERUKUR", "DIHITUNG-ULANG-SEBAGIAN", "Cek scratch/v9_e_rule/*stuck_k1*.json", "Cakupan 2/9 well dilaporkan terbuka")
row("B36", "stuck K-ii TLead 4,5-8,5 menit (median 7,0)", "Lead time terukur engine stuck", m + "2976",
    "TERUKUR", "DIHITUNG-ULANG-SEBAGIAN", "Cek scratch/v9_e_rule/*stuck_k2*.json field TLead",
    "SATU-SATUNYA lead time menit terukur; di bawah target 10-30 menit")
row("B37", "hyd K-i hybrid P 0,724-0,948, R 0,52-0,87, FAR 14,62-58,43, FP 2091->927 (-55,7%)", "Kandidat terkuat engine hyd", m + "2977",
    "TERUKUR", "DIHITUNG-ULANG-SEBAGIAN", "Cek scratch/v9_e_rule/*hyd*.json; 927/2091 = 0,4434 sehingga penurunan 55,66%",
    "Aritmetika pengurangan FP bisa direproduksi dari dua angka yang dilaporkan")
row("B38", "hyd K-ii fisher AUPRC 0,022 CI [0,0025;0,0684], sign-flip 78,66% (6.377/8.107)", "Baseline statistik hyd K-ii", m + "2978",
    "TERUKUR", "DIHITUNG-ULANG-SEBAGIAN", "6.377/8.107 = 0,7866; cek scratch/v9_e_stat/*hyd*.json",
    "78,66% COCOK dengan pembagian dua angka yang dilaporkan")
row("B39", "bit_wear AUPRC 0,119-0,984, ΔB vs canary 5/5", "Engine bit_wear K-1", m + "2979",
    "TERUKUR", "DIHITUNG-ULANG-SEBAGIAN", "Cek scratch/v9_e_ml/*bit_wear*.json", "P/R/FAR dilaporkan belum terukur (field tidak ada)")
row("B40", "tool_wear cp signifikan 8/8, precision 0,50, TLead 20-36 detik", "Engine keausan alat domain bengkel", m + "2981",
    "TERUKUR", "DIHITUNG-ULANG-SEBAGIAN", "Cek scratch/v9_e_stat/*tool_wear*.json; 4/8 = 0,50 cocok",
    "Lead detik TIDAK boleh dijumlah dengan lead menit rig (D-A7)")
row("B41", "tool_wear K-ii canary AUPRC 0,516-0,612", "Baseline ranking lintas alat", m + "2982",
    "TERUKUR", "DILAPORKAN", "Cek scratch/v9_e_ml/*tool_wear*.json", "RF V9 belum dijalankan, bukti masih referensi V8")
row("B42", "0 dari 7 engine memenuhi syarat alarm otomatis", "Rekap tier alat", m + "3378 dan docs/V8_PM_VERDICT.md baris 30",
    "TERUKUR", "DIHITUNG-ULANG", "python3 scratch/ppt1/verify_numbers.py -> registry_layer_counts L3 = 2, tier BELUM LAYAK 2; tidak ada head tier alarm",
    "Konsisten: tidak ada head berlabel alarm otomatis")
row("B43", "135 titik shk, 53 dengan FAR<=60, 1 titik FAR<=6 dengan recall>0", "Audit ambang engine shk", m + "1776-1777",
    "TERUKUR", "DIHITUNG-ULANG-SEBAGIAN", "Cek grid tau di scratch/v9_e_ml/*shk*.json (9 fold x 3 model x 5 tau = 135)",
    "135 = 9x3x5 konsisten secara aritmetika")
row("B44", "10 dari 402 titik uji (<1%) dengan FAR<=6 dan recall>0", "Sapuan ambang seluruh engine", m + "1861",
    "TERUKUR", "DILAPORKAN", "Hitung ulang grid ambang dari JSON per engine", "Belum saya hitung ulang; klaim '<1%' konsisten dengan 10/402")
row("B45", "B3: vib 0,00; ssi +0,73; shk 0,00; stuck +0,16; hyd +0,56; tool_wear +0,91..+0,98", "Nilai pemeliharaan lapisan B", m + "3000-3006",
    "TERUKUR", "DILAPORKAN", "Cek scratch/v9_eval_b/*.json field B3 per kelas", "Belum dihitung ulang; arah (positif = hemat inspeksi) konsisten")
row("B46", "ambang FAR<=1/24jam (alarm) dan FAR<=6/24jam (L1)", "Syarat naik tier", m + "3431-3433",
    "ASUMSI", "KEPUTUSAN-DESAIN", "Tidak ada preseden vendor yang dikutip untuk angka 1 dan 6; cek protokol prareg V6_E1_PREREG.md",
    "Ambang keputusan, bukan hasil ukur. Wajib disebut sebagai kriteria yang ditetapkan penulis")
row("B47", "syarat B1>=80% dan C2 drop<20%", "Syarat alarm otomatis", m + "3433",
    "ASUMSI", "KEPUTUSAN-DESAIN", "Cek docs/V8_R1_ABC_SPEC.md", "Kriteria desain")
row("B48", "55 fitur (11 kanal x 5 statistik)", "Ruang fitur model", m + "1641 dan docs/V10_PM2_VERDICT.md baris 27",
    "TERUKUR", "DILAPORKAN", "11x5 = 55 (kontrol aritmetika); cek scratch/v9_d1 dataset header",
    "55 COCOK secara aritmetika")
row("B49", "seed 42", "Seed eksperimen", m + "docs/V10_PM2_VERDICT.md baris 27",
    "TERUKUR", "DIHITUNG-ULANG", "python3 -c tidak dipakai; baca scratch/v9_i1/v9_i1_RESULTS.json key meta/seed",
    "Tersimpan di registry JSON")
row("B50", "26 fold ML", "Jumlah fold untuk head ML", m + "docs/V10_PM2_VERDICT.md baris 27",
    "TERUKUR", "DILAPORKAN", "Hitung fold pada 4 engine ML di MD baris 1718-1721: 4+9+9+4 = 26",
    "26 COCOK dari penjumlahan fold yang dilaporkan")

# ============ GRUP C: VERDICT V6-V11 ============
v = "docs/"
row("C01", "0+3+2+2 = 7", "Rekap tier tingkat engine (verdict V10)", v + "V10_PM2_VERDICT.md baris 13",
    "TERUKUR", "DIHITUNG-ULANG", "python3 scratch/ppt1/verify_numbers.py -> 7 engine; jumlah tier 0+3+2+2 = 7",
    "Cocok")
row("C02", "rekap head 12/13/2", "Rekap tier tingkat head (verdict V10)", v + "V10_PM2_VERDICT.md baris 41",
    "TERUKUR", "DIHITUNG-ULANG", "python3 scratch/ppt1/verify_numbers.py -> registry_tier_counts",
    "COCOK PERSIS")
row("C03", "lapisan 5/11/9/2", "Rekap lapisan L0-L3 (verdict V10)", v + "V10_PM2_VERDICT.md baris 13",
    "TERUKUR", "DIHITUNG-ULANG", "python3 scratch/ppt1/verify_numbers.py -> registry_layer_counts",
    "COCOK PERSIS, jumlah 27")
row("C04", "28 angka kunci ditelusuri", "Cakupan audit A1 (verdict V10)", v + "V10_PM2_VERDICT.md baris 85",
    "TERUKUR", "DILAPORKAN", "Cek docs/V10_A1_AUDIT.md tabel audit", "Jumlah angka yang diaudit, bukan hasil ukur")
row("C05", "23/27 klaim eksak, 3 temuan nyata", "Hasil audit V9 (verdict V9)", v + "V9_PM2_VERDICT.md baris 217",
    "TERUKUR", "DIHITUNG-ULANG-SEBAGIAN", "23+3 = 26; 1 klaim sisanya = k2_tidak_tersedia (lihat registry head hyd/k2_tidak_tersedia)",
    "23+3+1 = 27 konsisten dengan registry")
row("C06", "kandidat 2 = 95..96 vs kandidat 1 = 46,2..48,2; selisih 49,8; ambang selisih tipis 5 poin", "Skor keputusan akhir (verdict V11)", v + "V11_PM_FINAL.md baris 64-69, 123",
    "TERUKUR", "DIHITUNG-ULANG", "96-46,2 = 49,8 (cocok dengan baris 123); 95-48,2 = 46,8 (batas bawah)",
    "Skor adalah rubrik penilaian internal, bukan metrik model")
row("C07", "α Likely 55%, Δ Worst 15%", "Probabilitas skenario verdict V11", v + "V11_PM_FINAL.md baris 203-204",
    "ASUMSI", "JUDGEMENT", "Tidak ada dasar frekuentis; angka penilaian ahli (expert elicitation) internal",
    "Wajib disebut penilaian, dilarang disebut probabilitas terukur")
row("C08", "192 XML tubular, 198.928 baris USROP, label 134.013/49.732/15.183", "Hitung ulang mandiri PM V6", v + "V6_PM_VERDICT.md baris 15-17",
    "TERUKUR", "DIHITUNG-ULANG-SEBAGIAN", "192 dan 198.928 COCOK dengan verifikasi saya; 134.013+49.732+15.183 = 198.928 (kontrol aritmetika)",
    "Tiga label menjumlah tepat ke total baris")
row("C09", "3 kelas lolos gate G1+G2, taksonomi 7 kelas", "Vonis V6", v + "V6_PM_VERDICT.md baris 26-27",
    "TERUKUR", "DILAPORKAN", "Lihat gate G1/G2 di docs/V6_E1_PREREG.md", "Vonis berbasis gate prareg, bukan angka baru")
row("C10", "7 kelas dalam vonis V7", "Jumlah kelas yang dinilai (verdict V7)", v + "V7_PM_VERDICT.md baris 161",
    "TERUKUR", "DIHITUNG-ULANG", "python3 scratch/ppt1/verify_numbers.py -> 7 engine", "Cocok")
row("C11", "0 dari 7 engine layak alarm otomatis (V8)", "Vonis V8", v + "V8_PM_VERDICT.md baris 30",
    "TERUKUR", "DIHITUNG-ULANG", "Sama seperti B42", "Konsisten lintas verdict")
row("C12", "G4: peringatan >10-30 menit belum terlayani (semua horizon <=10 menit)", "Keterbatasan lead time (V8)", v + "V8_PM_VERDICT.md baris 40 dan 199",
    "TERUKUR", "DIHITUNG-ULANG-SEBAGIAN", "MD baris 2976: TLead 4,5-8,5 menit; horizon onset H=10 menit di docs/V6_E1_PREREG.md",
    "Menegaskan target 10-30 menit (A08/A18) BELUM tercapai")
row("C13", "7 engine / 11 klaim / 27 head (re-verifikasi registry)", "Audit klaim angka (V11_AUD_CLAIM)", v + "V11_AUD_CLAIM.md baris 30 dan 67",
    "TERUKUR", "DIHITUNG-ULANG", "python3 scratch/ppt1/verify_numbers.py -> semua tiga angka cocok",
    "Independen dari verdict, tetap cocok")

# ============ GRUP D: HITUNG SENDIRI SESI INI ============
row("D01", "73.500 menit (1.225 jam)", "Total durasi 884 kejadian (act_end - act_start)", "data/volve/labels_curated_v2.csv kolom act_start/act_end; python3 scratch/ppt1/verify_durations.py",
    "TERUKUR", "DIHITUNG-ULANG", "python3 scratch/ppt1/verify_durations.py -> total_minutes 73500.0, total_hours 1225.0",
    "ANGKA BARU: dasar kuantitatif untuk klaim dampak NPT, menggantikan klaim tanpa angka")
row("D02", "median 45 menit, p90 180 menit, maksimum 780 menit", "Sebaran durasi kejadian", "idem D01 (verify_durations.py)",
    "TERUKUR", "DIHITUNG-ULANG", "python3 scratch/ppt1/verify_durations.py -> median_min 45.0, p90_min 180.0, max_min 780.0",
    "Bisa dipakai untuk memilih horizon prediksi 10-30 menit secara empiris")
row("D03", "10 wellbore, F-14 182 kejadian", "Sebaran kejadian per sumur", "idem D01 (verify_durations.py)",
    "TERUKUR", "DIHITUNG-ULANG", "python3 scratch/ppt1/verify_durations.py -> wells 10, per_well_top",
    "F-14 = 182/884 (20,6%): sumur terpadat, konsisten dengan fokus kalibrasi per-well di MD")
row("D04", "0 dari 884 durasi tidak bisa diparse", "Kualitas timestamp label", "idem D01",
    "TERUKUR", "DIHITUNG-ULANG", "python3 scratch/ppt1/verify_durations.py -> dur_bad 0",
    "Timestamp ISO lengkap dengan offset, aman dipakai")
row("D05", "9.935.708 baris mentah WITSML (10 CSV)", "Baris mentah folder witsml_parsed", "python3 scratch/ppt1/verify_numbers.py",
    "TERUKUR", "DIHITUNG-ULANG", "python3 scratch/ppt1/verify_numbers.py -> witsml_parsed_total_lines",
    "Beda 10 dari MD baris 1433 = jumlah header; dua definisi, bukan kontradiksi")
row("D06", "27 head: 5 L0, 11 L1, 9 L2, 2 L3", "Rekap lapisan registry (hitung sendiri)", "scratch/v9_i1/v9_i1_RESULTS.json engines[].heads[].layer; python3 scratch/ppt1/verify_numbers.py",
    "TERUKUR", "DIHITUNG-ULANG", "python3 scratch/ppt1/verify_numbers.py -> registry_layer_counts",
    "COCOK dengan dokumen dan verdict")
row("D07", "tier head 12 peringatan / 13 tren / 2 belum layak", "Rekap tier registry (hitung sendiri)", "scratch/v9_i1/v9_i1_RESULTS.json engines[].heads[].tier",
    "TERUKUR", "DIHITUNG-ULANG", "python3 scratch/ppt1/verify_numbers.py -> registry_tier_counts",
    "COCOK dengan V10_PM2 baris 41")
row("D08", "weighted-sum 4,35 / 3,35 / 3,50 / 3,00 / 2,40", "Reproduksi skor MCDM dengan bobot tertulis", "python3 scratch/ppt1/arith_audit.py",
    "TERUKUR", "DIHITUNG-ULANG", "python3 scratch/ppt1/arith_audit.py -> scores[*].wsm_hitung",
    "TEMUAN: 4 dari 5 skor draft menyimpang 0,05 dari perhitungan bobot tertulis")
row("D09", "TOPSIS closeness 0,8306 / 0,5213 / 0,4255 / 0,3251 / 0,1731", "TOPSIS sejati dengan bobot dan nilai yang sama", "python3 scratch/ppt1/arith_audit.py",
    "TERUKUR", "DIHITUNG-ULANG", "python3 scratch/ppt1/arith_audit.py -> topsis_cc",
    "TEMUAN: peringkat A2 (0,52) di atas A3 (0,43), sedangkan draft menaruh A3 lebih tinggi. Pemenang A1 tetap")
row("D10", "RPN 378/280/324/245/240 cocok 5/5", "Uji aritmetika SxOxD", "python3 scratch/ppt1/arith_audit.py",
    "TERUKUR", "DIHITUNG-ULANG", "python3 scratch/ppt1/arith_audit.py -> fmea[*].cocok",
    "Aritmetika FMEA benar; yang belum terjustifikasi adalah skala S/O/D")

# ============ tulis JSON ============
os.makedirs(BASE + "/scratch/ppt1", exist_ok=True)
cnt = collections.Counter(r["status"] for r in R)
sub = collections.Counter(r["sub"] for r in R)
grup = collections.Counter(r["grup"] for r in R)
payload = {
    "meta": {
        "dibuat": "2026-10-25",
        "kartu": "t_0eb03f13",
        "sumber": [DOCX, MD, "docs/V6_PM_VERDICT.md .. docs/V11_PM_FINAL.md",
                   "data/volve/labels_curated_v2.csv", "scratch/v9_i1/v9_i1_RESULTS.json"],
        "skrip_verifikasi": ["scratch/ppt1/verify_numbers.py", "scratch/ppt1/verify_durations.py",
                             "scratch/ppt1/arith_audit.py"],
        "status_kanonik": ["TERUKUR", "ASUMSI", "WARISAN-DRAFT"],
        "jumlah_baris": len(R),
        "rekap_status": dict(cnt),
        "rekap_sub": dict(sub),
        "rekap_grup": dict(grup),
    },
    "baris": R,
}
json.dump(payload, open(BASE + "/scratch/ppt1/ledger.json", "w"), indent=1, ensure_ascii=False)

# ============ tulis MARKDOWN ============
L = []
A = L.append
A("# LEDGER ANGKA PROPOSAL PPT I DAN DESAIN TEKNIS")
A("")
A("Kartu: `t_0eb03f13` (PM/Protokol). Tanggal: 25 Oktober 2026. Ruang kerja: `/mnt/d/Capstone 1(v2)`.")
A("")
A("Dokumen ini menginventaris **" + str(len(R)) + " angka** dari tiga sumber: draft `Proposal_PPT_I_SperryDrilling_ML_NPT.docx` (13 Agu 2026), `docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md`, dan verdict V6 sampai V11, ditambah angka hasil hitung ulang sesi ini.")
A("")
A("Riset pendahuluan: `verification-mandatory` - setiap angka dipisah menjadi bukti mentah dan kesimpulan, angka yang tidak bisa direproduksi dilarang ditulis sebagai hasil ukur, dan laporan ditutup dengan daftar yang belum dicek.")
A("Riset pendahuluan: `sequentialthinking` (sequ-mcp, 3 pikiran) - urutan: definisi status, uji provenance per klaster, lalu cek konsistensi lintas dokumen sebelum menyimpulkan.")
A("Riset pendahuluan: `grounded-citations` - klaim eksternal (efisiensi >15%) wajib menempel ke sumber primer, bukan ke ingatan.")
A("")
A("## 1. Ringkasan status")
A("")
A("| Status | Jumlah | Arti |")
A("|---|---|---|")
A("| TERUKUR | " + str(cnt.get("TERUKUR", 0)) + " | punya jejak berkas/JSON/perintah yang bisa dijalankan ulang |")
A("| ASUMSI | " + str(cnt.get("ASUMSI", 0)) + " | parameter, target, atau ambang keputusan yang belum diukur |")
A("| WARISAN-DRAFT | " + str(cnt.get("WARISAN-DRAFT", 0)) + " | lahir literal di generator draft, tidak punya jejak hitung |")
A("")
A("Rekap per grup: A (draft docx) " + str(grup.get("A", 0)) + " angka, B (desain teknis) " + str(grup.get("B", 0)) + " angka, C (verdict V6-V11) " + str(grup.get("C", 0)) + " angka, D (hitung ulang sesi ini) " + str(grup.get("D", 0)) + " angka.")
A("")
A("Rekap sub-status: " + ", ".join(k + "=" + str(vv) for k, vv in sorted(sub.items())) + ".")
A("")
A("## 2. Tabel ledger")
A("")
hdr = "| ID | Angka | Konteks | Sumber | Status | Sub | Cara verifikasi | Temuan |"
sep = "|---|---|---|---|---|---|---|---|"
judul = {
    "A": "### 2.A Draft `Proposal_PPT_I_SperryDrilling_ML_NPT.docx` (13 Agu 2026)",
    "B": "### 2.B `docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md` (255/3557?) lihat baris per baris",
    "C": "### 2.C Verdict V6 sampai V11",
    "D": "### 2.D Angka hasil hitung ulang sesi ini (25 Okt 2026)",
}
judul["B"] = "### 2.B `docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md`"
for g in ("A", "B", "C", "D"):
    A(judul[g])
    A("")
    A(hdr)
    A(sep)
    for r in R:
        if r["grup"] != g:
            continue
        tm = r["temuan"].replace("|", "\\|")
        cells = [r["id"], r["angka"], r["konteks"], r["sumber"], r["status"], r["sub"], r["verifikasi"], tm]
        cells = [c.replace("|", "\\|") for c in cells]
        A("| " + " | ".join(cells) + " |")
    A("")

A("## 3. Fokus khusus yang diminta kartu")
A("")
A("### 3.1 FMEA S/O/D/RPN")
A("")
A("Status: **WARISAN-DRAFT**. RPN benar secara aritmetika (5 dari 5 cocok, `scratch/ppt1/arith_audit.py`), tetapi skala S, O, dan D tidak punya tabel justifikasi di dokumen mana pun. Jejak literalnya ada di " + SESS + " yang menulis tabel itu langsung ke generator docx. Tindakan: kartu R1 memberi justifikasi skala AIAG-VDA, kartu D1 memasok O dari frekuensi 884 kejadian, kartu B2 merakit ulang tabel.")
A("")
A("### 3.2 MCDM (draft menyebutnya TOPSIS)")
A("")
A("Status: **WARISAN-DRAFT** untuk bobot dan skor. Tiga temuan yang bisa direproduksi:")
A("")
A("1. Bobot tertulis berjumlah tepat 1,00 (0,25+0,20+0,15+0,10+0,15+0,15), jadi bobotnya konsisten sebagai himpunan, tetapi tidak ada berita acara elisitasi stakeholder.")
A("2. Skor draft hanya bisa direproduksi untuk A1 (weighted-sum 4,35). Empat baris lain menyimpang 0,05: A2 3,35 vs 3,40, A3 3,50 vs 3,55, A4 3,00 vs 2,95, A6 2,40 vs 2,45.")
A("3. TOPSIS sejati dengan normalisasi vektor dan jarak ideal memberi closeness 0,8306 / 0,5213 / 0,4255 / 0,3251 / 0,1731 untuk A1, A2, A3, A4, A6. Artinya **A2 mengalahkan A3**, sedangkan draft menaruh A3 (3,55) di atas A2 (3,40). Pemenang A1 tetap A1, jadi kesimpulan tidak berubah, tetapi tabel wajib diperbaiki atau dilabeli ulang sebagai weighted-sum, bukan TOPSIS.")
A("")
A("### 3.3 KPI target (recall 0,70-0,80 dan lead 10-30 menit)")
A("")
A("Status: **ASUMSI, kategori target**. Tidak ada satu pun run yang mencapainya:")
A("")
A("- Alarm otomatis: 0 dari 7 engine (MD baris 3378, V8_PM_VERDICT baris 30).")
A("- Recall terukur: vib 0,276-0,595; ssi 0,000-0,032; stuck K-i 0,449-0,599 (MD baris 2972-2975).")
A("- Lead time menit yang benar-benar terukur hanya stuck K-ii: 4,5-8,5 menit, median 7,0 (MD baris 2976). Ini di bawah target 10-30 menit.")
A("- Lead 20-36 detik pada tool_wear adalah domain bengkel dan dilarang dijumlahkan dengan lead rig (D-A7).")
A("")
A("Kalimat yang boleh masuk proposal: \"target recall 0,70-0,80 dan lead 10-30 menit ditetapkan sebagai sasaran desain, sementara hasil terukur saat ini baru mencapai recall 0,28-0,60 (rule vib) dan lead 4,5-8,5 menit (stuck K-ii)\".")
A("")
A("### 3.4 Klaim \"efisiensi >15%\"")
A("")
A("Status: **TERUKUR, kategori eksternal**. Terverifikasi di press release Halliburton 9 Juli 2026 (kalimat \"improved efficiency by more than 15%\") dan di salinan relasi investor serta worldoil.com. Angka ini milik vendor untuk operasi closed-loop MPD Eni, **bukan hasil proyek kita**. Boleh dikutip dengan atribusi, dilarang menjadi janji luaran proposal.")
A("")
A("### 3.5 Klaim \"884 kejadian\"")
A("")
A("Status: **TERUKUR**. `python3 scratch/ppt1/verify_numbers.py` memberi 884 baris. Tetapi distribusinya penting dan harus disebut agar tidak menyesatkan:")
A("")
A("- 496 dari 884 (56,1%) berkategori `routine_no_failure_evidence`, artinya bukan kegagalan.")
A("- `bha_relevant`: yes 50, no 263, uncertain 571. Hanya **50 kejadian (5,7%)** yang benar-benar relevan BHA.")
A("- Total durasi 884 kejadian = 73.500 menit = **1.225 jam**, median 45 menit, p90 180 menit, maksimum 780 menit.")
A("")
A("Kalimat yang benar: \"basis label memuat 884 kejadian operasi, 50 di antaranya terverifikasi relevan BHA, dengan total durasi 1.225 jam\". Bukan \"884 kejadian kerusakan\".")
A("")
A("### 3.6 Klaim \"27 head\"")
A("")
A("Status: **TERUKUR**. Registry yang dieksekusi memberi 27 head dengan sebaran 4+4+4+6+4+2+3, lapisan 5/11/9/2 (jumlah 27), tier 12 peringatan / 13 tren / 2 belum layak. Tiga angka 7 engine, 11 klaim, 27 head adalah tiga tingkat objek yang sama (kelas, tugas, varian metode) dan **tidak boleh dijumlahkan**.")
A("")
A("## 4. Definisi operasional")
A("")
A("Aturan yang mengikat setiap penulisan angka di proposal PPT I:")
A("")
A("1. **TERUKUR** hanya untuk angka yang bisa direproduksi: sebut berkas + baris, atau JSON key, atau perintah yang bisa dijalankan ulang. Contoh sah: 884 (labels_curated_v2.csv), 27 (registry), 292.954 (scratch/v9_d1/datasets).")
A("2. **ASUMSI** wajib ditulis dengan kata \"asumsi\" atau \"target\" di kalimat yang sama. Dilarang berdiri sendiri seolah hasil. Contoh: target recall 0,70-0,80; bobot MCDM; ambang FAR<=1/24jam; laju stream 1 Hz; window 30 dan step 5.")
A("3. **WARISAN-DRAFT** wajib diberi label \"(asumsi draft)\" sampai ada hitung ulang. Contoh: S/O/D FMEA dan seluruh skor MCDM.")
A("4. **Angka pihak ketiga** wajib menempel ke sumber primer dan disebut sebagai milik pihak lain (contoh: efisiensi >15% milik Halliburton untuk operasi Eni).")
A("5. **Angka hasil hitung sendiri** wajib menyebut skrip dan tanggalnya, supaya bisa diulang dosen (contoh: 1.225 jam dari `verify_durations.py`).")
A("6. **Tingkat objek tidak boleh dicampur**: 7 engine, 11 klaim, dan 27 head tidak dijumlahkan; lead detik bengkel tidak dijumlahkan dengan lead menit rig.")
A("7. **Angka yang belum dihitung ulang** wajib ditandai \"dilaporkan, belum dihitung ulang\" dan tidak boleh dipakai sebagai dasar klaim baru.")
A("")
A("## 5. Temuan yang mengubah naskah (bukan sekadar status)")
A("")
A("1. **884 tidak sama dengan 884 kerusakan.** 56,1% kejadian tidak berisi bukti kegagalan dan hanya 5,7% relevan BHA. Latar belakang proposal harus menyebut komposisi ini.")
A("2. **Skor MCDM di draft tidak reproducible dan bukan TOPSIS.** Perbaiki di kartu C3, sertakan tabel closeness coefficient dan uji sensitivitas bobot.")
A("3. **Asumsi 1 Hz bertabrakan dengan pipeline 60 detik.** Turunkan ke 1/60 Hz atau hapus dari §3.1.1.A.")
A("4. **Target KPI tidak tercapai oleh hasil terukur.** Tulis target dan hasil dalam satu kalimat berpasangan, jangan hanya target.")
A("5. **Kontrol aritmetika lintas dokumen lulus:** 6 dataset = 292.954 baris, 37 fold = 4+9+9+2+9+4, WITSML 59.489+547.500+1.883.062+1.286.967+457.545+1.648.026+778.162+419.706 = 7.080.457, label USROP 134.013+49.732+15.183 = 198.928, dan 9.935.708 baris mentah minus 10 header = 9.935.698 seperti ditulis MD.")
A("")
A("## 6. Belum diverifikasi (jujur)")
A("")
A("- 239 kolom dan 13 kolom pit pada `time.csv` F-9A: dilaporkan MD §3.7, belum saya hitung ulang.")
A("- 1.392 komponen tubular, 5.561 stasiun trajectory, 109 section wbGeometry, 2.882 interval mudLog: jumlah berkas induknya cocok, isi komponen belum dihitung.")
A("- EDM 10.650 `CD_ASSEMBLY_COMP` dan 632 `CD_BHA_COMP_BIT`: belum dihitung ulang.")
A("- Himpunan angka B3 (lapisan B) dan 402 titik uji: dilaporkan MD, belum saya reproduksi dari JSON.")
A("- Angka verdict berupa penilaian skenario (55%, 15%) adalah judgement internal, bukan probabilitas terukur.")
A("")
A("## 7. Berkas bukti")
A("")
A("- `scratch/ppt1/ledger.json` (versi mesin dari tabel ini, " + str(len(R)) + " baris).")
A("- `scratch/ppt1/verify_numbers.py` (884 kejadian, distribusi kategori, bha_relevant, dataset latih, toolwear, registry 27 head, tier, lapisan).")
A("- `scratch/ppt1/verify_durations.py` (durasi 884 kejadian: 73.500 menit, median, p90, maksimum, sebaran per sumur).")
A("- `scratch/ppt1/arith_audit.py` (RPN 5/5 cocok, weighted-sum vs skor draft, TOPSIS closeness coefficient).")
A("- `scratch/ppt1/verify_leak.py` (6 dataset latih, 292.954 baris, 37 fold LOWO, 0 pelanggaran anti-bocor).")
A("- `scratch/ppt1/verify_out.json` dan `scratch/ppt1/arith_audit.json` (keluaran mentah).")
A("")

open(BASE + "/docs/PPT1_LEDGER_ANGKA.md", "w").write("\n".join(L))
print("baris:", len(R))
print("status:", dict(cnt))
print("grup:", dict(grup))
print("MD bytes:", os.path.getsize(BASE + "/docs/PPT1_LEDGER_ANGKA.md"))
