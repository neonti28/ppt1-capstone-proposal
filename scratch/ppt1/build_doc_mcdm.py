"""Perender dokumen BAB III 3.4 dari mesin hitung yang sama dengan mcdm.json.

Jalankan dari akar repo:
    python3 scratch/ppt1/build_doc_mcdm.py

Masukan : scratch/ppt1/mcdm_data.py dan fungsi pada scratch/ppt1/build_mcdm.py
Keluaran: docs/PPT1_BAB3_4_MCDM.md
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mcdm_data as D
import build_mcdm as B

AKAR = "/mnt/d/Capstone 1(v2)"
KRIT = B.KRIT
ALT = B.ALT
NAMA = B.NAMA_ALT


def n(x, d=4):
    """Angka desimal dengan koma Indonesia."""
    return f"{float(x):.{d}f}".replace(".", ",")


def unit_teks(u):
    if isinstance(u, (list, tuple)):
        return f"{u[0]}/{u[1]}"
    if isinstance(u, str):
        return u
    if isinstance(u, float) and abs(u - round(u)) < 1e-9:
        return str(int(round(u)))
    return str(u)


def main():
    sel = B.hitung_sel()
    M = B.matriks_nilai(sel)
    t = B.topsis(M, B.BOBOT_DASAR)
    s = B.saw(M, B.BOBOT_DASAR)
    tau_metode = B.kendall_tau(t["peringkat"], s["peringkat"])
    sens = B.sensitivitas(M, sel)
    disk = B.diskriminasi(M, B.BOBOT_DASAR)
    lama = B.hitung_draft_lama()

    with open(os.path.join(AKAR, D.JSON_OUT), encoding="utf-8") as f:
        J = json.load(f)
    assert J["topsis"]["peringkat"] == t["peringkat"], "JSON tidak segar, jalankan build_mcdm.py"
    assert len(J["sensitivitas"]["skenario"]) == len(sens["skenario"])

    juara = t["peringkat"][0]
    kedua = t["peringkat"][1]
    ketiga = t["peringkat"][2]
    c_juara = t["sel"][juara]["C"]
    c_kedua = t["sel"][kedua]["C"]
    c_ketiga = t["sel"][ketiga]["C"]
    selisih_12 = c_juara - c_kedua
    selisih_23 = c_kedua - c_ketiga
    n_kasus = len(sens["skenario"]) + len(sens["oat"])
    juara_set = sorted({sk["juara"] for sk in sens["skenario"]})
    oat_berubah = sum(1 for o in sens["oat"] if o["berubah"])
    segmen = sens["titik_balik_C1"]["segmen"]
    ambang_balik = None
    for i in range(1, len(segmen)):
        if segmen[i - 1]["juara"] != segmen[i]["juara"]:
            ambang_balik = segmen[i]["bobot_C1_dari"]

    # kontribusi per kriteria (V = bobot x nilai ternormalisasi)
    def kontrib(a, c):
        return t["sel"][a]["V"][c]

    beda = {c: kontrib(juara, c) - kontrib(kedua, c) for c in KRIT}
    unggul = sorted([c for c in KRIT if beda[c] > 0], key=lambda c: -beda[c])
    kalah = sorted([c for c in KRIT if beda[c] < 0], key=lambda c: beda[c])
    penentu = [c for c in KRIT if abs(beda[c]) > 1e-12]
    pemegang_tiga = [a for a in ALT if sens["stabilitas"][a]["tiga_besar"] > 0]
    belum_eksekusi = [a for a in ALT if sel[(a, "C1")]["unit"] == "L20"]
    n_belum = len(belum_eksekusi)

    L = []
    A = L.append

    A("# BAB III ANALISIS ALTERNATIF SOLUSI")
    A("")
    A("## Subbab 3.4 Pemilihan Alternatif Solusi dengan MCDM")
    A("")
    A("| Kendali dokumen | Keterangan |")
    A("|---|---|")
    A("| Dokumen | Proposal Proyek Perancangan Terpadu I, BAB III subbab 3.4 |")
    A("| Mitra | PT Halliburton Indonesia, divisi Sperry Drilling |")
    A("| Versi | 1.0, 25 Oktober 2026 |")
    A("| Status | Berjalan. Subbab 3.1, 3.2, dan 3.3 sudah selesai, subbab ini menutup BAB III. |")
    A("| Acuan format | Buku Pedoman PPT Tahap I subbab 3.2 Format Proposal, halaman 33 sampai 36 |")
    A("| Acuan rubrik | Rubrik Penilaian PPT oleh Dosen, halaman 38 dan berikutnya, butir 2.2, 3.2, dan 3.3 |")
    A("| Metode | TOPSIS dengan bobot Rank-Order Centroid, pembanding SAW |")
    A(f"| Hasil | {juara} ({NAMA[juara]}) dengan koefisien kedekatan {n(c_juara)} |")
    A("| Identitas anggota | Diisi tim. Dokumen ini tidak mengarang nama maupun NIM. |")
    A("")

    # ------------------------------------------------------------------ 3.4.1
    A("### 3.4.1 Dasar perhitungan dan aturan bukti")
    A("")
    A("Riset pendahuluan: `statistical-analysis` - disiplin uji sensitivitas dan larangan menyajikan angka tanpa ketidakpastian. Poin yang dipakai: analisis sensitivitas dipakai untuk menguji apakah kesimpulan bergantung pada asumsi bobot, dan seluruh hitungan disimpan pada skrip yang dapat dijalankan ulang. Dua butir panduan yang relevan adalah \"A non-significant result is not evidence of no effect\" dan \"Make it reproducible\"; keduanya diterapkan sebagai kewajiban sembilan skenario dan skrip reproduksi.")
    A("")
    A("Riset pendahuluan: `grounded-citations` - setiap klaim dari sumber luar memakai penanda dan daftar sumber yang dihasilkan mesin, bukan diketik dari ingatan. Poin yang dipakai: DOI ketiga sumber metode diperiksa lewat pencarian web pada 25 Oktober 2026 sebelum ditulis, sedangkan rujukan internal tetap memakai bentuk berkas dan nomor baris.")
    A("")
    A("Riset pendahuluan: `sequentialthinking` (sequ-mcp, enam pikiran) - menetapkan urutan kerja: verifikasi sumber sebelum memakai hasil lama, penolakan AHP karena tidak ada pakar, pemilihan TOPSIS dengan SAW sebagai pembanding, penanganan dua kolom tanpa variasi, penyelesaian pertentangan C8 terhadap subbab 3.3.6 butir 8, dan penetapan batas klaim sebelum menulis.")
    A("")
    A("Aturan bukti yang dipakai pada subbab ini:")
    A("")
    A("1. Setiap angka pada matriks keputusan menunjuk berkas dan nomor baris, kunci JSON, atau skrip yang dapat dijalankan ulang. Kolom jejak pada tabel 3.4.1 memuat rujukan itu.")
    A("2. Angka yang belum terukur ditulis sebagai asumsi dan diberi penanda yang sama pada tabel, bukan disamarkan sebagai hasil pengukuran.")
    A("3. Skala 1 sampai 5 tidak dipakai untuk kriteria yang sudah punya angka terukur, sesuai larangan pada subbab 3.3.5. Angka asli dipakai langsung, lalu dipetakan ke skala 0 sampai 100 memakai fungsi nilai yang ditulis terbuka pada subbab 3.4.3.")
    A("4. Dokumen tim tidak disebut dengan kata yang menyiratkan tuduhan. Perbedaan angka draft lama diperiksa dengan hitung ulang, dan hasilnya ditulis sebagai temuan yang dapat diperiksa sendiri.")
    A("")

    # ------------------------------------------------------------------ 3.4.2
    A("### 3.4.2 Pemilihan metode MCDM")
    A("")
    A("Tiga metode dipertimbangkan. Yang menentukan bukan popularitas, melainkan apakah masukannya tersedia tanpa mengarang angka.")
    A("")
    A("| Metode | Kebutuhan masukan | Kesesuaian dengan bukti yang ada | Keputusan | Alasan |")
    A("|---|---|---|---|---|")
    for m in D.METODE_KANDIDAT:
        A(f"| {m['nama']} | {m['kebutuhan']} | {m['kesesuaian']} | {m['keputusan']} | {m['alasan']} |")
    A("")
    A(f"TOPSIS dipakai sebagai metode utama dan SAW sebagai pembanding bebas. Keduanya memakai matriks keputusan yang sama, sehingga perbedaan hasil hanya berasal dari cara mengukur jarak. Hasilnya: juara kedua metode sama, yaitu {juara}, dengan Kendall tau {n(tau_metode)}. Perbedaan hanya menyangkut posisi A9, yang naik dari peringkat sembilan ke peringkat tujuh pada SAW, dan itu tidak menyentuh keputusan.")
    A("")
    A("AHP ditolak dengan alasan yang perlu dinyatakan tegas: AHP menuntut perbandingan berpasangan oleh pakar, dan pada proyek ini belum ada wawancara mitra. Mengisi matriks perbandingan tanpa pakar berarti menulis angka yang tidak punya jejak, sekaligus membuat rasio konsistensi tidak bermakna. Penolakan ini soal ketersediaan bukti, bukan penilaian bahwa AHP lemah. Bila wawancara tersedia pada tahap berikutnya, AHP dapat dijalankan dan dibandingkan dengan hasil subbab ini.")
    A("")
    A("Sumber metode, dengan DOI yang sudah diperiksa:")
    A("")
    A("| Sumber | Dipakai untuk | DOI | Cara verifikasi |")
    A("|---|---|---|---|")
    for st in D.SITASI:
        A(f"| {st['teks']} | {st['dipakai_untuk']} | `{st['doi']}` | {st['verifikasi']} |")
    A("")
    A("Satu batas pemakaian dinyatakan di depan. Kunsch dan Ishizaka menunjukkan bahwa keunggulan bobot Rank-Order Centroid bergantung pada cara bobot seharusnya diperoleh. Karena itu bobot ROC pada subbab ini bukan bobot final mitra, melainkan bobot terbaik yang dapat dipertanggungjawabkan dari bahan yang ada, dan wajib disertai uji sensitivitas pada 3.4.8.")
    A("")

    # ------------------------------------------------------------------ 3.4.3
    A("### 3.4.3 Kriteria, arah, dan fungsi nilai")
    A("")
    A("Delapan kriteria diambil tanpa perubahan definisi dari subbab 3.3.1. Yang ditambahkan di sini hanya fungsi nilai, yaitu aturan yang mengubah satuan mentah menjadi skala 0 sampai 100 supaya dapat dibandingkan dan diukur jaraknya.")
    A("")
    A("| Kode | Kriteria | Arah | Satuan mentah | Fungsi nilai ke 0 sampai 100 | Status angka |")
    A("|---|---|---|---|---|---|")
    for k in sorted(D.KRITERIA, key=lambda x: x["peringkat"]):
        A(f"| {k['id']} | {k['nama']} | {k['arah']} | {k['satuan']} | {k['fungsi_nilai']} | {k['status']} |")
    A("")
    A("Empat hal perlu dijelaskan tentang tabel di atas.")
    A("")
    A("Pertama, kriteria terukur tidak diskalakan ulang menjadi 1 sampai 5. C2 memakai jumlah fold layak dibagi 18, yaitu jumlah fold terbesar yang dimiliki satu alternatif, sehingga 18 fold layak bernilai 100 dan 9 fold bernilai 50. C5 memakai bentuk 100 dibagi (1 ditambah jumlah wellbore tersisa), sehingga nol wellbore bernilai 100. C7 memakai persentase klaim yang berjejak, dan nilainya 100 untuk seluruh alternatif karena setiap butir bukti pada subbab 3.1 membawa rujukan.")
    A("")
    A("Kedua, C1 dan C3 berbentuk rubrik berjangkar karena pertanyaannya bukan besaran, melainkan keadaan pelaksanaan. C1 memakai empat tingkat: 100 bila gate G1 dan G2 lolos, 75 bila mekanisme sudah dieksekusi dan delta terukur positif, 40 bila sudah dieksekusi tanpa delta positif, dan 20 bila belum dieksekusi. C3 memakai tiga tingkat: 100 bila kalibrasi per sumur sudah diuji pada dua sumur atau lebih, 60 bila menambah sumur uji atau memuat rancangan kalibrasi yang belum diuji, dan 30 bila tidak menyentuh portabilitas. Setiap tingkat menunjuk keadaan yang dapat diperiksa pada dokumen proyek, bukan kesan penilai.")
    A("")
    A("Ketiga, C8 tetap berstatus asumsi dan ini dinyatakan terbuka. Subbab 3.3.6 butir 8 menyatakan antarmuka peringatan belum dirancang sehingga C8 belum dapat dinilai untuk alternatif mana pun (`docs/PPT1_BAB3_2.md:665`). Pada subbab ini C8 tetap diisi dengan tingkat yang dibaca dari niat desain: tingkat 3 untuk alternatif yang rancangan keluarannya berupa satu baris peringatan dengan waktu, keyakinan, dan tindakan, dan tingkat 2 untuk alternatif yang keluarannya masih berupa label, daftar kandidat, atau angka yang perlu ditafsirkan. Konsekuensinya, skenario P7 pada 3.4.8 menolkan bobot C8, sehingga dapat diperiksa apakah keputusan berubah bila kriteria yang belum divalidasi itu dibuang sama sekali.")
    A("")
    A("Keempat, tidak ada angka rupiah pada subbab ini. Batasan B6 mengingatkan bahwa tarif rig per jam tidak tersedia pada seluruh 13 dataset (`docs/PPT1_BAB3_2.md:659`). Karena itu biaya diukur sebagai jumlah wellbore yang harus diproses dan jumlah minggu kerja, bukan rupiah. Dengan begitu tidak ada satu pun nilai pada matriks keputusan yang bersandar pada tarif yang tidak diketahui.")
    A("")
    A("Tabel 3.4.1 Jejak setiap sel matriks keputusan")
    A("")
    A("| Alternatif | Kriteria | Satuan mentah | Status | Dasar | Jejak |")
    A("|---|---|---|---|---|---|")
    for a in ALT:
        for c in KRIT:
            s_ = sel[(a, c)]
            A(f"| {a} | {c} | {unit_teks(s_['unit'])} | {s_['status']} | {s_['dasar']} | {s_['jejak']} |")
    A("")

    # ------------------------------------------------------------------ 3.4.4
    A("### 3.4.4 Bobot kriteria")
    A("")
    A("Bobot tidak ditetapkan sebagai angka bulat. Yang tersedia pada proyek ini adalah urutan prioritas, bukan rasio antar kriteria, sehingga urutan itu diturunkan menjadi bobot kardinal dengan Rank-Order Centroid. Aturan penyusunan urutan ditulis lebih dahulu, supaya urutan itu dapat dibantah.")
    A("")
    A("| Kode | Aturan pengurutan | Kriteria | Dasar |")
    A("|---|---|---|---|")
    for r in D.ATURAN_DEF:
        A(f"| {r['kode']} | {r['aturan']} | {r['kriteria']} | {r['dasar']} |")
    A("")
    A("Aturan dibaca berurutan dari R1 sampai R8: kriteria yang memenuhi aturan lebih awal mendapat peringkat lebih tinggi. Di dalam kelompok batasan keras, dua hal menentukan urutan, yaitu sifat menggugurkan atau tidaknya pelanggaran lebih dahulu, lalu jumlah user story yang bergantung pada kriteria itu menurut `scratch/ppt1/affinity.json` kunci `matriks_us_kriteria`.")
    A("")
    A("| Peringkat | Kriteria | Aturan | Bobot ROC | Alasan ringkas |")
    A("|---|---|---|---|---|")
    for k in sorted(D.KRITERIA, key=lambda x: x["peringkat"]):
        A(f"| {k['peringkat']} | {k['id']} {k['nama']} | {D.ATURAN_URUT[k['id']]} | {n(B.BOBOT_DASAR[k['id']])} | {k['alasan_peringkat']} |")
    A("")
    A(f"Rumus yang dipakai: untuk n kriteria dan peringkat i, bobot sama dengan satu per n dikali jumlah satu per k untuk k dari i sampai n. Untuk delapan kriteria, peringkat satu menghasilkan {n(B.BOBOT_DASAR['C1'])} dan peringkat delapan menghasilkan {n(B.BOBOT_DASAR['C8'])}. Pemeriksaan jumlah:")
    A("")
    A(f"- Jumlah delapan bobot = {n(sum(B.BOBOT_DASAR.values()), 12)}")
    A(f"- Bobot terbesar {n(max(B.BOBOT_DASAR.values()))} pada kriteria yang memenuhi R1, bobot terkecil {n(min(B.BOBOT_DASAR.values()))} pada kriteria yang memenuhi R8")
    A(f"- Rasio bobot terbesar terhadap terkecil = {n(max(B.BOBOT_DASAR.values()) / min(B.BOBOT_DASAR.values()), 2)}")
    A("")
    A("Status bobot ini adalah ASUMSI, dengan dua alasan yang ditulis apa adanya: belum ada wawancara mitra yang menetapkan prioritas, dan ROC adalah pendekatan, bukan elisitasi langsung. Satu kelemahan perlu disebut di sini, bukan hanya di bagian hasil: karena C4 menempati peringkat dua, kriteria yang pada matriks ternyata tidak membedakan justru menerima bobot terbesar kedua. Hal itu tidak diubah tanpa pemberitahuan, sebab menurunkan peringkat C4 akan berarti mengubah penilaian tentang kekerasan batasan B2. Yang dilakukan adalah menguji akibatnya lewat skenario P6, yang menolkan bobot C4 dan C7. Karena status bobotnya asumsi, subbab ini tidak berhenti pada satu vektor bobot, melainkan menguji sembilan skenario, enam belas uji satu per satu, dan satu sapuan penuh pada kriteria terpenting. Yang menentukan adalah apakah juara berubah, bukan apakah angkanya bergeser.")
    A("")

    # ------------------------------------------------------------------ 3.4.5
    A("### 3.4.5 Matriks keputusan")
    A("")
    A("Matriks berukuran sembilan alternatif kali delapan kriteria, seluruhnya 72 sel terisi. Tabel 3.4.2 memuat satuan mentah supaya dapat dicocokkan dengan berkas sumber, sedangkan tabel 3.4.3 memuat nilai baku yang masuk hitungan.")
    A("")
    A("Tabel 3.4.2 Matriks keputusan dalam satuan mentah")
    A("")
    A("| Alternatif | " + " | ".join(KRIT) + " |")
    A("|---|" + "---|" * len(KRIT))
    for a in ALT:
        A(f"| {a} | " + " | ".join(unit_teks(sel[(a, c)]["unit"]) for c in KRIT) + " |")
    A("")
    A("Keterangan satuan: C1 dan C3 memakai kode tingkat rubrik, yaitu L100, L75, L60, L40, L30, dan L20. C2 memakai jumlah fold layak, C4 jumlah slot alarm otomatis, C5 jumlah wellbore atau berkas yang harus diproses, C6 jumlah minggu kerja, C7 jumlah klaim berjejak dibagi jumlah klaim, dan C8 tingkat rubrik beban kognitif.")
    A("")
    A("Tabel 3.4.3 Matriks nilai baku 0 sampai 100")
    A("")
    A("| Alternatif | " + " | ".join(KRIT) + " |")
    A("|---|" + "---|" * len(KRIT))
    for a in ALT:
        A(f"| {a} | " + " | ".join(n(M[(a, c)], 2) for c in KRIT) + " |")
    A("")
    A(f"Daya beda kolom diperiksa sebelum bobot dipakai. Kolom tanpa variasi: {', '.join(disk['tanpa_variasi'])}. Keduanya bernilai sama untuk sembilan alternatif, yaitu nol slot alarm otomatis untuk C4 dan 100 untuk C7, sehingga tidak mungkin mengubah urutan. Massa bobot yang benar-benar membedakan hanya {n(disk['massa_bobot_efektif'])}, sedangkan {n(disk['massa_bobot_tanpa_variasi'])} berada pada dua kolom yang tidak membedakan. Ini bukan cacat hitungan, melainkan fakta tentang alternatifnya: pada tahap ini tidak ada alternatif yang mengusulkan alarm otomatis, dan semua alternatif membawa jejak bukti. Konsekuensinya diuji lewat skenario P6 yang menolkan bobot kedua kolom tersebut.")
    A("")

    # ------------------------------------------------------------------ 3.4.6
    A("### 3.4.6 Perhitungan TOPSIS")
    A("")
    A("Lima langkah, seluruhnya dijalankan oleh `scratch/ppt1/build_mcdm.py`.")
    A("")
    A("1. Normalisasi vektor per kolom: setiap nilai dibagi akar jumlah kuadrat kolomnya.")
    A("2. Pembobotan: nilai ternormalisasi dikali bobot kriteria.")
    A("3. Solusi ideal positif dan negatif: nilai terbesar dan terkecil per kolom pada matriks berbobot.")
    A("4. Jarak Euclidean setiap alternatif ke kedua solusi ideal, yaitu D plus dan D minus.")
    A("5. Koefisien kedekatan C sama dengan D minus dibagi (D plus ditambah D minus). Nilai satu berarti paling dekat ke ideal.")
    A("")
    A("| Kriteria | Pembagi normalisasi | Ideal positif | Ideal negatif | Bobot |")
    A("|---|---|---|---|---|")
    for c in KRIT:
        A(f"| {c} | {n(t['bagi'][c], 4)} | {n(t['ideal_plus'][c], 4)} | {n(t['ideal_min'][c], 4)} | {n(B.BOBOT_DASAR[c])} |")
    A("")
    A("Tabel 3.4.4 Hasil TOPSIS")
    A("")
    A("| Peringkat | Alternatif | Nama | D plus | D minus | Koefisien kedekatan C |")
    A("|---|---|---|---|---|---|")
    for a in t["peringkat"]:
        r = t["sel"][a]
        A(f"| {r['peringkat']} | {a} | {NAMA[a]} | {n(r['D_plus'], 4)} | {n(r['D_minus'], 4)} | {n(r['C'], 4)} |")
    A("")
    A(f"Selisih koefisien antara peringkat satu dan dua adalah {n(selisih_12)}, sedangkan antara peringkat dua dan tiga adalah {n(selisih_23)}. Lompatan terbesar karena itu berada di antara peringkat dua dan tiga, bukan di puncak. Artinya dua alternatif teratas membentuk kelompok tersendiri, dan jaraknya ke kelompok berikutnya jauh lebih lebar daripada jarak antar keduanya. Alasannya terbaca pada tabel kontribusi berikut, yang memecah koefisien menjadi sumbangan tiap kriteria.")
    A("")
    A("Tabel 3.4.5 Kontribusi tiap kriteria pada tiga besar (nilai V sama dengan bobot kali nilai ternormalisasi)")
    A("")
    A("| Kriteria | Bobot | " + " | ".join([juara, kedua, ketiga]) + " | Selisih " + juara + " dikurangi " + kedua + " |")
    A("|---|---|" + "---|" * 3 + "---|")
    for c in KRIT:
        A(f"| {c} | {n(B.BOBOT_DASAR[c])} | " +
          " | ".join(n(kontrib(a, c), 5) for a in (juara, kedua, ketiga)) +
          f" | {'+' if beda[c] >= 0 else ''}{n(beda[c], 5)} |")
    A("")
    A(f"Kontribusi yang menentukan kemenangan {juara} adalah " +
      ", ".join(f"{c} sebesar +{n(beda[c], 5)}" for c in unggul[:3]) +
      (f", sedangkan {kedua} hanya unggul pada " +
       ", ".join(f"{c} sebesar {n(beda[c], 5)}" for c in kalah)
       if kalah else
       f", sedangkan pada kriteria lain selisihnya nol sehingga {kedua} tidak unggul pada satu kriteria pun") +
      ". Dengan kata lain, kemenangan itu berasal dari selisih pada kriteria yang berbobot besar, bukan dari keunggulan menyeluruh.")
    A("")
    A(f"Perlu dicatat bahwa {juara} dan {kedua} sama-sama bernilai 75 pada C1, karena keduanya sudah dieksekusi dan memberi delta terukur positif, yaitu stuck dengan B1 0,51 sampai 1,00 pada `docs/V9_EVAL_B_LAYERB.md:101` dan alat bengkel dengan lead time 20 sampai 36 detik pada `docs/V9_EVAL_C_LAYERC.md:98`. Yang memisahkan keduanya adalah kriteria lain, terutama jumlah fold layak, beban kognitif, dan waktu kerja. Penilaian C1 untuk {juara} juga tidak seragam antar kelas: pada kelas hyd hasilnya negatif, yaitu nol dari tiga onset menurut `docs/V9_EVAL_B_LAYERB.md:103`, dan itu dicatat terbuka, bukan dirata-ratakan menjadi kemenangan.")
    A("")

    # ------------------------------------------------------------------ 3.4.7
    A("### 3.4.7 Pembanding SAW")
    A("")
    A("SAW memakai normalisasi vektor dan bobot yang sama, lalu menjumlahkan hasil kali bobot dengan nilai ternormalisasi. Karena tidak memakai titik ideal, hasilnya dapat berbeda bila ada alternatif yang menonjol pada satu kriteria tetapi lemah pada kriteria lain.")
    A("")
    A("| Peringkat | Alternatif | Skor SAW | Peringkat TOPSIS |")
    A("|---|---|---|---|")
    for i, a in enumerate(s["peringkat"], start=1):
        A(f"| {i} | {a} | {n(s['skor'][a], 4)} | {t['sel'][a]['peringkat']} |")
    A("")
    tau_skor = B.kendall_tau(s["peringkat"], t["peringkat"])
    sepakat = int(round((tau_skor + 1) / 2 * 36))
    pos_t = {a: i for i, a in enumerate(t["peringkat"])}
    pos_s = {a: i for i, a in enumerate(s["peringkat"])}
    pasangan_beda = [(x, y) for i, x in enumerate(ALT) for y in ALT[i + 1:]
                     if (pos_t[x] - pos_t[y]) * (pos_s[x] - pos_s[y]) < 0]
    A(f"Kendall tau antara peringkat TOPSIS dan SAW adalah {n(tau_skor)}. Dengan sembilan alternatif, jumlah pasangan adalah 36, sehingga nilai itu berarti {sepakat} pasangan sepakat dan {36 - sepakat} pasangan berbeda. Pasangan yang berbeda adalah " +
      ", ".join(f"{x} terhadap {y}" for x, y in pasangan_beda) +
      f". Keduanya melibatkan posisi peringkat tujuh sampai sembilan, jauh di bawah dua besar. Juara kedua metode sama, yaitu {juara}, sehingga keputusan tidak bergantung pada pilihan metode.")
    A("")

    # ------------------------------------------------------------------ 3.4.8
    A("### 3.4.8 Uji sensitivitas")
    A("")
    A("Uji dilakukan pada tiga tingkat. Pertama, sembilan skenario vektor bobot yang mewakili pembacaan berbeda atas prioritas. Kedua, enam belas uji satu per satu, yaitu setiap bobot dikali 1,5 lalu 0,5 dan dinormalkan ulang. Ketiga, satu sapuan penuh bobot C1 dari nol sampai 0,90 untuk mencari titik balik juara.")
    A("")
    A("Tabel 3.4.6 Sembilan skenario bobot")
    A("")
    A("| Skenario | Nama | Jenis | " + " | ".join(KRIT) + " | Juara | Tiga besar | Tau terhadap P0 |")
    A("|---|---|---|" + "---|" * len(KRIT) + "---|---|---|")
    for sk in sens["skenario"]:
        A(f"| {sk['id']} | {sk['nama']} | {sk['jenis']} | " +
          " | ".join(n(sk["bobot"][c], 3) for c in KRIT) +
          f" | {sk['juara']} | {', '.join(sk['tiga_besar'])} | {n(sk['tau_vs_dasar'])} |")
    A("")
    for sk in sens["skenario"]:
        A(f"- {sk['id']} {sk['nama']}: {sk['catatan']}")
    A("")
    A(f"Hasil sembilan skenario: juara yang muncul hanya {', '.join(juara_set)}, dan {sum(1 for sk in sens['skenario'] if sk['juara'] == juara)} dari {len(sens['skenario'])} skenario memilih {juara}.")
    A("")
    A("Tabel 3.4.7 Enam belas uji satu per satu")
    A("")
    A("| Kriteria | Arah | Bobot baru | Juara | Juara berubah |")
    A("|---|---|---|---|---|")
    for o in sens["oat"]:
        A(f"| {o['kriteria']} | {o['arah']} | {n(o['bobot_baru'])} | {o['juara']} | {'ya' if o['berubah'] else 'tidak'} |")
    A("")
    A(f"Dari {len(sens['oat'])} uji satu per satu, tidak satu pun mengubah juara, dengan hitungan {oat_berubah} dari {len(sens['oat'])}. Artinya juara tidak bergantung pada satu bobot saja, termasuk pada kriteria yang bobotnya paling besar.")
    A("")
    A("Tabel 3.4.8 Sapuan bobot C1")
    A("")
    A("| Juara | Bobot C1 dari | Bobot C1 sampai |")
    A("|---|---|---|")
    for sg in segmen:
        A(f"| {sg['juara']} | {n(sg['bobot_C1_dari'])} | {n(sg['bobot_C1_sampai'])} |")
    A("")
    if ambang_balik is not None:
        A(f"Titik balik juara berada pada bobot C1 = {n(ambang_balik)}. Di bawah nilai itu {segmen[0]['juara']} menang, di atasnya {juara} menang. Bobot C1 pada skenario dasar adalah {n(B.BOBOT_DASAR['C1'])}, dan skenario bobot sama memberi C1 = 0,1250. Keduanya berada di atas titik balik, sehingga hasil tidak bergantung pada penurunan ROC yang memberi C1 bobot besar.")
    A("")
    A("Tabel 3.4.9 Stabilitas peringkat pada seluruh uji")
    A("")
    A("| Alternatif | Menjadi juara | Masuk tiga besar | Peringkat terburuk | Jumlah kasus |")
    A("|---|---|---|---|---|")
    for a in ALT:
        st = sens["stabilitas"][a]
        A(f"| {a} | {st['juara']} | {st['tiga_besar']} | {st['peringkat_terburuk']} | {st['jumlah_kasus']} |")
    A("")
    A(f"Jumlah kasus adalah {n_kasus}, yaitu {len(sens['skenario'])} skenario ditambah {len(sens['oat'])} uji satu per satu. {juara} menjadi juara pada seluruh {n_kasus} kasus dan tidak pernah turun dari peringkat satu. Posisi tiga besar dihuni {', '.join(pemegang_tiga)}, dengan {kedua} masuk {sens['stabilitas'][kedua]['tiga_besar']} kali dan {ketiga} masuk {sens['stabilitas'][ketiga]['tiga_besar']} kali dari {n_kasus} kasus. Selain itu hanya A4 yang menyentuh tiga besar sebanyak {sens['stabilitas']['A4']['tiga_besar']} kali dan A5 sebanyak {sens['stabilitas']['A5']['tiga_besar']} kali, dan itu terjadi ketika bobot kriteria yang menjadi kekuatannya dinaikkan, bukan ketika bobot diturunkan.")
    A("")

    # ------------------------------------------------------------------ 3.4.9
    A("### 3.4.9 Perbandingan dengan draft lama")
    A("")
    A("Draft 13 Agustus 2026 memilih A1 ML Classifier dipadukan A3 SHAP dashboard, memakai enam kriteria berskala 1 sampai 5 tanpa rubrik dan bobot 0,25, 0,20, 0,15, 0,10, 0,15, 0,15 (`scratch/ppt1/docx_draft_text.txt:228-279`). Dua pemeriksaan dilakukan: menghitung ulang jumlah berbobot setiap baris, dan menjalankan TOPSIS sejati pada matriks draft itu sendiri.")
    A("")
    A("Tabel 3.4.10 Hitung ulang jumlah berbobot draft lama")
    A("")
    A("| Alternatif draft | Skor K1 sampai K6 | Total tertulis | Total hitung ulang | Selisih | Dapat direproduksi |")
    A("|---|---|---|---|---|---|")
    for r in lama["baris"]:
        A(f"| {r['nama']} | {', '.join(str(int(x)) for x in r['skor'])} | {n(r['total_tertulis'], 2)} | {n(r['jumlah_berbobot_hitung'], 2)} | {n(r['selisih'], 2)} | {'ya' if r['reproduksi'] else 'tidak'} |")
    A("")
    A(f"Dari lima baris, {5 - lama['jumlah_tidak_reproduksi']} dapat direproduksi dan {lama['jumlah_tidak_reproduksi']} tidak. Selisihnya 0,05 pada empat baris. Temuan ini bukan tuduhan, melainkan akibat langsung dari skala 1 sampai 5 tanpa rubrik: karena tidak ada aturan resmi yang menghubungkan angka 5 pada K1 dengan keadaan tertentu, selisih sekecil itu tidak dapat diketahui pembaca. Pada subbab ini hal yang sama dicegah dengan fungsi nilai yang ditulis terbuka pada 3.4.3 dan pemeriksa otomatis.")
    A("")
    A("Peta kriteria draft ke kriteria subbab 3.3:")
    A("")
    A("| Kriteria draft | Kriteria subbab 3.3 | Status | Catatan |")
    A("|---|---|---|---|")
    for p in D.PETA_DRAFT:
        A(f"| {p['draft']} | {p['kita']} | {p['status']} | {p['catatan']} |")
    A("")
    A("Dua dari enam kriteria draft, yaitu K5 kemudahan integrasi dan K6 ROI, tidak dapat dipertahankan karena tidak ada berkas proyek yang mengukurnya. Karena itu perbandingan angka mentah antara TOPSIS subbab ini dan skor draft tidak bermakna. Yang dibandingkan adalah keputusan dan alasannya.")
    A("")
    A("Tabel 3.4.11 TOPSIS sejati pada matriks draft lama")
    A("")
    A("| Peringkat | Alternatif draft | D plus | D minus | C |")
    A("|---|---|---|---|---|")
    for x in lama["topsis_sejati"]:
        A(f"| {x['peringkat']} | {x['nama']} | {n(x['D_plus'], 4)} | {n(x['D_minus'], 4)} | {n(x['C'], 4)} |")
    A("")
    A("Tiga kesimpulan perbandingan, ditulis apa adanya.")
    A("")
    A("Pertama, label juara sama tetapi isinya berbeda, dan ini harus dinyatakan terbuka. Draft memilih A1 yang berarti pengklasifikasi pembelajaran mesin. Pada subbab 3.1, A1 berarti relabeling onset peristiwa, yaitu memindahkan definisi target dari status ke titik masuk peristiwa, dan justru mekanisme itulah yang membuat pengklasifikasi dapat bekerja. Jadi kesamaan huruf A1 bukan kesamaan objek pemilihan. Yang benar-benar sejalan adalah arah: pembelajaran terbimbing di atas label onset dengan keluaran berpengawas manusia.")
    A("")
    urut_tertulis = sorted(lama["baris"], key=lambda r: -r["total_tertulis"])
    pos_w = {r["nama"]: i for i, r in enumerate(urut_tertulis)}
    pos_t2 = {x["nama"]: i for i, x in enumerate(lama["topsis_sejati"])}
    nama_draft = [r["nama"] for r in urut_tertulis]
    tukar = [(x, y) for i, x in enumerate(nama_draft) for y in nama_draft[i + 1:]
             if (pos_w[x] - pos_w[y]) * (pos_t2[x] - pos_t2[y]) < 0]
    A("Kedua, draft menyebut metodenya TOPSIS (`scratch/ppt1/docx_draft_text.txt:229`), tetapi angka yang ditulis pada tabel draft adalah jumlah berbobot, yaitu skor dikali bobot lalu dijumlahkan. Hitungan itu adalah SAW, bukan TOPSIS. Ketika TOPSIS sejati dijalankan pada matriks yang sama, urutannya berubah: " +
      ", ".join(f"{x} dan {y} bertukar posisi" for x, y in tukar) +
      ". Juara tidak berubah, tetapi peringkat kedua dan ketiga pada draft bergantung pada metode yang dipakai, dan hal itu tidak terlihat karena draft tidak menulis langkah perhitungannya. Pada subbab ini kedua metode dihitung dan dibandingkan secara terbuka pada 3.4.6 dan 3.4.7.")
    A("")
    A(f"Ketiga, draft tidak memisahkan alternatif yang sudah dieksekusi dari yang belum. Akibatnya alternatif yang belum dijalankan dapat memperoleh skor 5 pada K1 karena tampak menjanjikan. Pada subbab ini pemisahan itu dilakukan lewat rubrik C1, dan skenario P5 menguji apa yang terjadi bila penalti bukti dihapus: juara tetap {juara}. Artinya kemenangan {juara} bukan akibat pembatasan metode, melainkan bertahan bahkan ketika alternatif yang belum dieksekusi diberi nilai lebih murah hati.")
    A("")

    # ------------------------------------------------------------------ 3.4.10
    A("### 3.4.10 Keputusan dan tindak lanjut")
    A("")
    A(f"Alternatif terpilih: {juara} ({NAMA[juara]}), dengan koefisien kedekatan {n(c_juara)} pada skenario dasar, menjadi juara pada {sens['stabilitas'][juara]['juara']} dari {n_kasus} kasus uji, dan tidak pernah turun dari peringkat satu.")
    A("")
    peran = {
        juara: "sumbu utama rancangan solusi",
        kedua: "jalur kedua pada domain berbeda, dijalankan bila jadwal memungkinkan",
        ketiga: "pendukung akuisisi bukti, dijalankan bersamaan dengan sumbu utama",
    }
    alasan_peran = {
        juara: "Mekanismenya sudah dieksekusi, memberi delta terukur positif pada kelas stuck, dan tidak menuntut parse baru sehingga C5 bernilai 100.",
        kedua: "Bukti terkuat pada domain bengkel dengan lead time 20 sampai 36 detik, tetapi domainnya berbeda dari rig sehingga tidak boleh menjadi klaim utama.",
        ketiga: "Menambah wellbore dan fold layak paling banyak, sehingga memperkuat alternatif lain tanpa menjadi bentuk keluaran tersendiri.",
        "A4": "Nilai C1 masih 20 karena belum dieksekusi, dan C2 hanya 12 fold, sehingga kalah dari A2 yang menyentuh empat kelas; unit stand tetap menarik karena tidak menuntut data baru.",
        "A8": "Nilai C1 masih 20 karena belum dieksekusi, dan C5 bernilai 33,33 karena dua sumur masih perlu parse kanal pit dan flow.",
        "A6": "Nilai C1 masih 20 karena belum dieksekusi, dan hasil negatif hyd yaitu nol dari tiga onset membuat formulasi survival belum punya sinyal pendukung pada kelas itu.",
        "A5": "Nilai C1 masih 20 karena belum dieksekusi, dan dua kelas sasarannya hanya memberi 9 fold layak sehingga C2 bernilai 50.",
        "A3": "Nilai C1 masih 20 dan C2 hanya 9 fold, sehingga kalah sebagai alternatif tunggal, walaupun pekerjaannya tetap dituntut oleh batasan B4 sebagai prasyarat.",
        "A9": "Nilai C1 masih 20 dan C3 baru tingkat 60 karena rancangan kalibrasi belum diuji, walaupun A9 satu-satunya yang menyentuh langsung gejala 119,6 kali.",
    }
    A("| Peringkat | Alternatif | Peran yang diusulkan | Dasar |")
    A("|---|---|---|---|")
    for a in t["peringkat"]:
        A(f"| {t['sel'][a]['peringkat']} | {a} {NAMA[a]} | {peran.get(a, 'tidak dipilih sebagai sumbu PPT I')} | {alasan_peran.get(a, 'Kalah bersaing pada seluruh skenario uji.')} |")
    A("")
    A("Satu hal perlu dinyatakan supaya tabel di atas tidak dibaca keliru: A3 berada di peringkat delapan, tetapi batasan B4 menuntut audit mutu label dikerjakan lebih dahulu sebelum kalibrasi dan pelatihan. Karena itu peringkat delapan bukan izin melewati A3. Yang dikatakan MCDM adalah bahwa A3 tidak cukup kuat sebagai sumbu utama bila dibandingkan sebagai alternatif tunggal, bukan bahwa pekerjaannya boleh dilewati.")
    A("")
    A("Satu catatan metodologis perlu disampaikan karena berkaitan dengan batas MCDM itu sendiri: matriks pada subbab ini memeringkat alternatif secara terpisah, sehingga kombinasi antaralternatif tidak dihitung. Kenyataan bahwa A1 dan A2 dapat dijalankan bersamaan, seperti terlihat pada klaster dan relasi prasyarat subbab 3.2, tidak diwakili oleh satu sel pun pada matriks. Karena itu keputusan di atas dibaca sebagai urutan prioritas, bukan sebagai larangan menjalankan alternatif lain secara paralel.")
    A("")

    # ------------------------------------------------------------------ 3.4.11
    A("### 3.4.11 Hasil negatif dan batas yang harus dinyatakan")
    A("")
    A("1. Bobot berstatus asumsi karena belum ada wawancara mitra. Yang dapat diklaim bukan bahwa bobot ini benar, melainkan bahwa keputusan tidak berubah pada sembilan skenario, enam belas uji satu per satu, dan satu sapuan penuh.")
    A("2. C8 belum tervalidasi, dan subbab 3.3.6 butir 8 menyatakan antarmuka peringatan belum dirancang. Tingkat C8 pada subbab ini adalah niat desain. Skenario P7 menolkan bobotnya dan juara tidak berubah, tetapi kriteria ini tetap tidak boleh dipakai sebagai bukti kualitas antarmuka.")
    A(f"3. Dua kolom tidak membedakan sama sekali, yaitu C4 dan C7, sehingga {n(disk['massa_bobot_tanpa_variasi'])} massa bobot tidak berperan dalam pengurutan. Keduanya tetap dipertahankan karena berfungsi sebagai saringan lulus atau gagal, dan skenario P6 membuktikan penolakan bobotnya tidak mengubah juara.")
    A(f"4. {n_belum} dari {len(ALT)} alternatif belum dieksekusi, sehingga nilai C1 mereka berasal dari rubrik tingkat 20, bukan dari hasil pengukuran. Bila salah satu alternatif itu dieksekusi dan gate-nya lolos, urutan dapat berubah. Ini pekerjaan terbuka yang dicatat, bukan risiko yang bisa diabaikan.")
    A("5. Jumlah minggu kerja pada C6 berstatus asumsi untuk setiap alternatif. Yang baku hanya tenggat sembilan minggu menurut Buku Pedoman PPT Tahap I Tabel 3.1 halaman 32.")
    A("6. Tidak ada angka rupiah pada perhitungan ini karena tarif rig tidak tersedia. Konsekuensinya keputusan tidak dapat dinyatakan sebagai penghematan biaya, dan klaim ROI tidak dibuat.")
    A("7. ROC adalah pendekatan bobot, bukan elisitasi. Menurut Kunsch dan Ishizaka, keunggulan ROC bergantung pada cara bobot seharusnya diperoleh, sehingga bila wawancara mitra menghasilkan rasio yang berbeda jauh, perhitungan wajib diulang dengan bobot hasil wawancara itu.")
    A("8. Portabilitas antar sumur belum terukur sesudah kalibrasi. Yang terukur baru sebaran sebelum kalibrasi, yaitu 4,15 sampai 496,09 per 24 jam (`docs/V9_PM2_VERDICT.md:114`), sehingga nilai C3 untuk A2, A8, dan A9 berstatus rubrik tingkat 60, bukan hasil uji.")
    A("9. A7 berada pada peringkat dua dengan koefisien 0,6993, tetapi berada pada domain bengkel, dengan presisi run 0,50 (`docs/V9_EVAL_C_LAYERC.md:98`) dan gate G1 nol dari empat alat (`docs/V7_R1_SOLUTIONS.md:160`). Peringkat dua itu tidak boleh dibaca sebagai kesiapan penerapan di rig.")
    A("10. Perbandingan dengan draft lama terbatas pada lima alternatif yang ada pada draft, dan dua kriteria draft tidak dapat dipetakan. Perbandingan angka mentah antara kedua dokumen tidak sah.")
    A("")

    # ------------------------------------------------------------------ 3.4.12
    A("### 3.4.12 Manifes jejak angka (internal, bukan untuk sirkulasi eksternal)")
    A("")
    A("| Angka | Nilai | Berkas, baris, atau kunci |")
    A("|---|---|---|")
    A(f"| Bobot ROC kriteria peringkat 1 | {n(B.BOBOT_DASAR['C1'])} | dihitung `scratch/ppt1/build_mcdm.py` fungsi roc_weights |")
    A(f"| Bobot ROC kriteria peringkat 8 | {n(B.BOBOT_DASAR['C8'])} | dihitung `scratch/ppt1/build_mcdm.py` fungsi roc_weights |")
    A(f"| Jumlah bobot | {n(sum(B.BOBOT_DASAR.values()), 12)} | `scratch/ppt1/mcdm.json` kunci bobot.jumlah |")
    A(f"| Koefisien kedekatan {juara} | {n(c_juara)} | `scratch/ppt1/mcdm.json` kunci topsis.sel.{juara}.C |")
    A(f"| Koefisien kedekatan {kedua} | {n(c_kedua)} | `scratch/ppt1/mcdm.json` kunci topsis.sel.{kedua}.C |")
    A(f"| Jumlah skenario | {len(sens['skenario'])} | `scratch/ppt1/mcdm.json` kunci sensitivitas.skenario |")
    A(f"| Jumlah uji satu per satu | {len(sens['oat'])} | `scratch/ppt1/mcdm.json` kunci sensitivitas.oat |")
    A(f"| Titik balik bobot C1 | {n(ambang_balik)} | `scratch/ppt1/mcdm.json` kunci sensitivitas.titik_balik_C1 |")
    A(f"| Kendall tau TOPSIS dan SAW | {n(tau_skor)} | `scratch/ppt1/mcdm.json` kunci kendall_topsis_saw |")
    A(f"| Massa bobot efektif | {n(disk['massa_bobot_efektif'])} | `scratch/ppt1/mcdm.json` kunci diskriminasi.massa_bobot_efektif |")
    A("| Baris draft lama yang tidak dapat direproduksi | 4 dari 5 | `scratch/ppt1/mcdm.json` kunci draft_lama.baris_tidak_reproduksi |")
    A("| Bobot draft lama | 0,25 / 0,20 / 0,15 / 0,10 / 0,15 / 0,15 | `scratch/ppt1/docx_draft_text.txt:232-237` |")
    A("| Pilihan draft lama | A1 ML Classifier dipadukan A3 SHAP | `scratch/ppt1/docx_draft_text.txt:279` |")
    A("| Slot alarm otomatis | 0 | `scratch/v9_i1/v9_i1_RESULTS.json` kunci auto_critical_alarm_slots |")
    A("| FAR vib antar sumur | 4,15 sampai 496,09 per 24 jam, rasio 119,6 kali | `docs/V9_PM2_VERDICT.md:114` |")
    A("| Stuck K-ii | B1 0,51 sampai 1,00, TLead 10 sampai 11,5 menit | `docs/V9_EVAL_B_LAYERB.md:101` |")
    A("| Hyd K-ii | 0 dari 3 onset | `docs/V9_EVAL_B_LAYERB.md:103` |")
    A("| Tool_wear K-i | TLead 20 sampai 36 detik, FP 1 sampai 3 per alat, presisi run 0,50 | `docs/V9_EVAL_C_LAYERC.md:98` |")
    A("| Gate shk, hyd, tool_wear, ssi, bit_wear, stuck | 3/7, 2/7, 0/4, 4/5, 3/4, 1/2 | `docs/V7_R1_SOLUTIONS.md:97, 127, 160, 197, 203, 66` |")
    A("| Jumlah bukti per alternatif | 3, 3, 3, 3, 3, 3, 4, 3, 4 | `scratch/ppt1/alternatif.json` kunci alternatif |")
    A("| Antarmuka peringatan belum dirancang | pernyataan 3.3.6 butir 8 | `docs/PPT1_BAB3_2.md:665` |")
    A("| Tarif rig tidak tersedia | pernyataan 3.3.6 butir 2 | `docs/PPT1_BAB3_2.md:659` |")
    A("")

    A("### 3.4.13 Lampiran bukti kelas sasaran")
    A("")
    A(f"Tabel berikut memuat angka yang menjadi jangkar rubrik C1 dan C3. Tujuannya supaya pembaca dapat memeriksa sendiri apakah tingkat 75 pada C1 memang layak, tanpa harus membuka dokumen V7 dan V9 satu per satu. {len(D.BUKTI_KELAS)} kelas sasaran tercatat, dan setiap baris menunjuk berkas dan nomor baris.")
    A("")
    A("Tabel 3.4.12 Bukti terukur per kelas sasaran")
    A("")
    A("| Kelas sasaran | Alternatif yang memakai | Lift terukur | Gate G1 dan G2 | Catatan | Jejak |")
    A("|---|---|---|---|---|---|")
    for b in D.BUKTI_KELAS:
        A(f"| {b['kelas']} | {', '.join(b['alternatif'])} | {b['lift']} | {b['gate']} | {b['catatan']} | {b['jejak']} |")
    A("")
    A("Dua hal perlu dibaca dari tabel itu. Pertama, menurut `docs/V8_PM_VERDICT.md:155` yang mengutip `docs/V6_PM_VERDICT.md:131`, hanya dua kelas yang berstatus LULUS penuh pada baseline, yaitu vib dan ssi. Meski begitu, tingkat 100 pada C1 belum diberikan kepada alternatif mana pun, karena rubrik C1 menuntut gate lolos untuk mekanisme alternatif itu sendiri: A1 memberi delta terukur positif pada kelas stuck tetapi negatif pada kelas hyd, sedangkan A2 dan A9 yang menyentuh vib, serta A2, A4, dan A5 yang menyentuh ssi, belum menjalankan evaluasi ulang pada kelas-kelas itu. Kedua, jumlah fold berbeda jauh antar kelas, dari dua fold pada stuck sampai tujuh fold pada shk, sehingga C2 terikat pada kelas mana yang disentuh sebuah alternatif.")
    A("")
    A("Reproduksi:")
    A("")
    A("```bash")
    A("cd \"/mnt/d/Capstone 1(v2)\"")
    A("python3 scratch/ppt1/build_mcdm.py        # menulis scratch/ppt1/mcdm.json")
    A("python3 scratch/ppt1/build_doc_mcdm.py    # menulis dokumen ini dari mesin yang sama")
    A("python3 scratch/ppt1/check_mcdm.py        # memeriksa acceptance dan setiap jejak")
    A("```")
    A("")
    A("Pemeriksa `check_mcdm.py` menolak dokumen bila ada angka yang berbeda dari JSON, bila rujukan berkas dan baris tidak ada atau di luar rentang, bila token penanda tidak ditemukan pada baris yang dikutip, bila jumlah skenario kurang dari delapan, dan bila terdapat em-dash atau en-dash. Pemeriksa itu sendiri diuji negatif memakai dokumen yang sengaja dirusak.")
    A("")

    teks = "\n".join(L) + "\n"
    jalur = os.path.join(AKAR, D.DOK)
    with open(jalur, "w", encoding="utf-8") as f:
        f.write(teks)

    print("dokumen:", jalur)
    print("baris:", len(L) + 1)
    print("juara:", juara, n(c_juara), "| kedua:", kedua, n(c_kedua), "| ketiga:", ketiga, n(c_ketiga))
    print("tau TOPSIS vs SAW:", tau_skor)
    print("titik balik C1:", ambang_balik)
    print("kasus uji:", n_kasus, "juara unik:", juara_set)
    print("pemegang tiga besar:", pemegang_tiga)
    print("penentu selisih:", penentu)


if __name__ == "__main__":
    main()
