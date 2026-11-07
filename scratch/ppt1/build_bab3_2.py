"""Bangun docs/PPT1_BAB3_2.md dan scratch/ppt1/affinity.json, lalu periksa acceptance."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)

from bab3_2_data import (  # noqa: E402
    META, RISET, ATURAN_BUKTI, METODE_AFINITAS, KLASTER, RELASI_KLASTER,
    MATRIKS_KLASTER_BOK, MATRIKS_KLASTER_MASALAH, OVERLAY_LAPISAN, G1,
)
from bab3_2_data_bok import BOK_DIDALAMI, BOK_TERBUKA, KRITERIA, BATASAN  # noqa: E402
from bab3_2_data_us import CATATAN_PERAN, USER_STORIES, MATRIKS_US_KRITERIA  # noqa: E402

ALT_PATH = os.path.join(ROOT, "scratch", "ppt1", "alternatif.json")
OUT_MD = os.path.join(ROOT, "docs", "PPT1_BAB3_2.md")
OUT_JSON = os.path.join(ROOT, "scratch", "ppt1", "affinity.json")

ALT = json.load(open(ALT_PATH, encoding="utf-8"))
ALT_BY_ID = {a["id"]: a for a in ALT["alternatif"]}
BOK_NAMA = ALT["bok"]


def row(cells):
    return "| " + " | ".join(str(c) for c in cells) + " |"


def header(cells):
    return row(cells) + "\n" + "|" + "|".join(["---"] * len(cells)) + "|"


def alt_name(aid):
    return ALT_BY_ID[aid]["nama"]


def alt_status(aid):
    return ALT_BY_ID[aid]["status"]


def render():
    L = []
    W = L.append

    W("# BAB III ANALISIS ALTERNATIF SOLUSI")
    W("")
    W("## Subbab 3.2 Analisis Alternatif Solusi dan Subbab 3.3 Kriteria dan Batasan")
    W("")
    W(header(["Kendali dokumen", "Keterangan"]))
    W(row(["Dokumen", META["dokumen"]]))
    W(row(["Mitra", META["mitra"]]))
    W(row(["Versi", META["versi"] + ", 25 Oktober 2026"]))
    W(row(["Status", "Berjalan. Subbab 3.1 sudah selesai, subbab 3.4 belum disusun."]))
    W(row(["Acuan format", META["acuan_format"]]))
    W(row(["Acuan rubrik", META["acuan_rubrik"]]))
    W(row(["Acuan BoK", META["acuan_bok"]]))
    W(row(["Identitas anggota", "Diisi tim. Dokumen ini tidak mengarang nama maupun NIM."]))
    W("")

    # ---------------- 3.2.1 ----------------
    W("### 3.2.1 Dasar analisis dan aturan bukti")
    W("")
    for r in RISET:
        W(r)
        W("")
    W("Pedoman menuntut tiga hal pada subbab 3.2, yaitu ruang brainstorming yang tidak menilai ide pada tahap awal, "
      "analisis sembilan alternatif dengan kedalaman minimal tiga BoK dari empat belas BoK, dan peta afinitas untuk "
      "mengelompokkan ide yang mirip ke kategori yang logis (Buku Pedoman PPT Tahap I subbab 3.2, halaman 35). "
      "Dokumen ini menjawab ketiganya dengan urutan: himpunan ide tetap sembilan alternatif dari subbab 3.1, "
      "pengelompokan dilakukan pada 3.2.2 sampai 3.2.6, dan pendalaman BoK dilakukan pada 3.2.7 sampai 3.2.9.")
    W("")
    W("Aturan bukti yang dipakai:")
    W("")
    for i, a in enumerate(ATURAN_BUKTI, 1):
        W(f"{i}. {a}")
    W("")

    # ---------------- 3.2.2 ----------------
    W("### 3.2.2 Metode peta afinitas")
    W("")
    for i, m in enumerate(METODE_AFINITAS, 1):
        W(f"{i}. {m}")
    W("")
    W("Hasil akhirnya empat klaster, dengan sebaran tiga, dua, dua, dan dua alternatif. Dua klaster melintasi batas "
      "anggota, yaitu K1 yang memuat alternatif milik anggota 1 dan anggota 3, serta K2 yang memuat alternatif milik "
      "anggota 1 dan anggota 2. Karena itu peta ini bukan salinan pembagian tugas pada subbab 3.1, melainkan "
      "pengelompokan berdasarkan mekanisme.")
    W("")

    # ---------------- 3.2.3 ----------------
    W("### 3.2.3 Peta afinitas empat klaster")
    W("")
    W(header(["Klaster", "Nama klaster", "Prinsip pengelompokan", "Anggota", "Masalah", "BoK", "Status"]))
    for k in KLASTER:
        W(row([
            k["id"], k["nama"], k["prinsip"],
            ", ".join(k["anggota"]),
            ", ".join(k["masalah"]),
            ", ".join(str(b) for b in k["bok"]),
            k["status"],
        ]))
    W("")
    W("Tabel di atas memuat seluruh sembilan alternatif tepat satu kali. Pemeriksaan otomatis pada "
      "`scratch/ppt1/check_bab3_2.py` menolak dokumen ini bila ada alternatif yang tidak masuk klaster atau masuk "
      "lebih dari satu klaster.")
    W("")

    # ---------------- 3.2.4 ----------------
    W("### 3.2.4 Rincian setiap klaster")
    W("")
    for idx, k in enumerate(KLASTER, 1):
        W(f"#### 3.2.4.{idx} {k['id']} {k['nama']}")
        W("")
        W(f"**Prinsip pengelompokan.** {k['prinsip']}")
        W("")
        W("**Anggota dan mekanisme.**")
        W("")
        for aid, mech in k["mekanisme"]:
            W(f"- {aid} {alt_name(aid)}. {mech}")
        W("")
        W(f"**Yang menyatukan.** {k['kesamaan']}")
        W("")
        W(f"**Yang membedakan.** {k['pembeda']}")
        W("")
        W("**Angka penentu.**")
        W("")
        W(header(["Keterangan", "Nilai", "Jejak"]))
        for klaim, nilai, jejak in k["angka"]:
            W(row([klaim, nilai, f"`{jejak}`"]))
        W("")
        if k.get("kasus_batas"):
            W(f"**Kasus batas.** {k['kasus_batas']}")
            W("")
        W("**Relasi dengan klaster lain.**")
        W("")
        rel_out = [r for r in RELASI_KLASTER if r["dari"] == k["id"]]
        rel_in = [r for r in RELASI_KLASTER if r["ke"] == k["id"]]
        if rel_out:
            for r in rel_out:
                W(f"- Keluar ke {r['ke']} dengan jenis {r['jenis']}. {r['alasan']} Jejak: `{r['jejak']}`.")
        if rel_in:
            for r in rel_in:
                W(f"- Masuk dari {r['dari']}. {r['alasan']} Jejak: `{r['jejak']}`.")
        if not rel_out and not rel_in:
            W("- Tidak ada relasi prasyarat maupun penyuplai yang tercatat untuk klaster ini.")
        W("")
        W(f"**Risiko bila klaster dipilih sendirian.** {k['risiko']}")
        W("")
        W(f"**Status agregat.** {k['status']}.")
        W("")

    # ---------------- 3.2.5 ----------------
    W("### 3.2.5 Silang klaster dengan masalah, BoK, dan lapisan intervensi")
    W("")
    W("**Cakupan masalah.**")
    W("")
    all_p = sorted({p for ps in MATRIKS_KLASTER_MASALAH.values() for p in ps})
    W(header(["Masalah"] + [k["id"] for k in KLASTER] + ["Jumlah klaster"]))
    for p in all_p:
        cells = ["ya" if p in MATRIKS_KLASTER_MASALAH[k["id"]] else "-" for k in KLASTER]
        W(row([p] + cells + [sum(1 for c in cells if c == "ya")]))
    W("")
    W(f"Sembilan masalah P1 sampai P9 seluruhnya tercakup oleh empat klaster, yaitu {len(all_p)} masalah. "
      "Tidak ada masalah pada subbab 3.1 yang kehilangan rumah, dan tidak ada klaster yang tidak menyentuh masalah.")
    W("")
    W("**Cakupan BoK per klaster.**")
    W("")
    W(header(["Klaster"] + [f"BoK {b}" for b in range(1, 15)]))
    for k in KLASTER:
        cells = ["ya" if b in MATRIKS_KLASTER_BOK[k["id"]] else "-" for b in range(1, 15)]
        W(row([k["id"]] + cells))
    W("")
    jumlah_bok = len({b for bs in MATRIKS_KLASTER_BOK.values() for b in bs})
    W(f"Sepuluh dari empat belas BoK tersentuh, yaitu {jumlah_bok} BoK. Empat BoK yang belum tersentuh dibahas pada 3.2.9.")
    W("")
    W("**Lapisan intervensi.** Lapisan memakai pembagian yang sama dengan subbab 3.1, supaya pembacaan tetap konsisten.")
    W("")
    W(header(["Lapisan", "Nama lapisan", "Klaster", "Anggota lapisan"]))
    for lid, lname in OVERLAY_LAPISAN.items():
        ks = [k["id"] for k in KLASTER if lid in k["lapisan"]]
        alts = [a for k in KLASTER if lid in k["lapisan"] for a in k["anggota"]]
        W(row([lid, lname, ", ".join(ks) if ks else "-", ", ".join(alts) if alts else "-"]))
    W("")
    W("K1 seluruhnya berada pada lapisan data dan label. K3 seluruhnya berada pada lapisan formulasi model. K2 "
      "menyentuh dua lapisan, yaitu data dan formulasi, karena basis bukti memengaruhi himpunan sumur sekaligus "
      "agregasi fitur. K4 berada pada lapisan sinyal fisik dan operasi. Lapisan bukan sumbu pengelompokan, sehingga "
      "dua klaster boleh berada pada lapisan yang sama. Yang membedakan klaster adalah objek yang diubah, bukan "
      "lapisannya. Karena itu peta afinitas ini tidak dapat disamakan dengan pembagian anggota pada subbab 3.1.")
    W("")

    # ---------------- 3.2.6 ----------------
    W("### 3.2.6 Struktur klaster untuk diagram G1")
    W("")
    W("Bagian ini adalah serahan untuk kartu diagram, supaya gambar tidak mengarang isi. Seluruh nilainya juga "
      "tersedia sebagai JSON pada `scratch/ppt1/affinity.json` dengan kunci `g1`.")
    W("")
    W(f"Kanvas: A4 landscape, {G1['kanvas']['lebar_in']:.2f} kali {G1['kanvas']['tinggi_in']:.2f} inci, "
      f"{G1['kanvas']['dpi']} dpi.".replace(".", ",", 2))
    W("")
    W("**Node klaster.**")
    W("")
    W(header(["Id", "Label", "Warna", "Anggota", "Teks ringkas", "Posisi x", "Posisi y"]))
    for n in G1["node_klaster"]:
        W(row([n["id"], n["label"], n["warna"], ", ".join(n["anggota"]), n["ringkas"], n["x"], n["y"]]))
    W("")
    W("**Node alternatif.**")
    W("")
    W(header(["Id", "Label pendek", "Klaster", "Status"]))
    for n in G1["node_alternatif"]:
        W(row([n["id"], n["label"], n["klaster"], n["status"]]))
    W("")
    W("**Edge antar klaster.**")
    W("")
    W(header(["Dari", "Ke", "Label", "Gaya garis"]))
    for e in G1["edge"]:
        W(row([e["dari"], e["ke"], e["label"], e["gaya"]]))
    W("")
    W("**Legenda.**")
    W("")
    for lg in G1["legenda"]:
        W(f"- {lg['simbol']}: {lg['arti']}")
    W("")
    pk = G1["penanda_kasus_batas"]
    W(f"**Penanda kasus batas.** {pk['alternatif']} {pk['teks']}. Penanda ditulis sebagai catatan kecil pada kotak "
      f"{pk['alternatif']}, bukan sebagai klaster kelima.")
    W("")
    W(f"**Catatan desain.** {G1['catatan_desain']}")
    W("")

    # ---------------- 3.2.7 ----------------
    W("### 3.2.7 Pendalaman BoK")
    W("")
    W("Empat BoK didalami, bukan sepuluh. Alasannya: BoK 14 dan BoK 3 wajib muncul karena pedoman menetapkan rantai "
      "BoK dimulai dari BoK 14 dan berakhir pada BoK 3, sedangkan BoK 5 dan BoK 11 dipilih karena frekuensi "
      "pemakaiannya paling tinggi pada sembilan alternatif. Empat BoK yang didalami ini masing-masing membawa peran, "
      "keputusan, standar, angka, dan batas. BoK lain yang hanya muncul sekali dicatat pada 3.2.8 dan tidak dipaksakan "
      "menjadi pendalaman semu.")
    W("")
    W(header(["BoK", "Nama", "Peran satu baris", "Jumlah alternatif", "Status pendalaman"]))
    for b in BOK_DIDALAMI:
        n_alt = sum(1 for a in ALT["alternatif"] if b["no"] in a["bok"])
        W(row([b["no"], b["nama"], b["peran"].split(". ")[0].rstrip(".") + ".", n_alt, "didalami"]))
    W("")

    for idx, b in enumerate(BOK_DIDALAMI, 1):
        W(f"#### 3.2.7.{idx} BoK {b['no']} {b['nama']}")
        W("")
        W(f"**Peran konkret dalam solusi.** {b['peran']}")
        W("")
        W("**Keputusan yang diambil melalui BoK ini.**")
        W("")
        for k in b["keputusan"]:
            W(f"- {k}")
        W("")
        W("**Standar dan metrik acuan.**")
        W("")
        for s in b["standar"]:
            W(f"- {s}")
        W("")
        W("**Angka penentu.**")
        W("")
        W(header(["Keterangan", "Nilai", "Jejak"]))
        for klaim, nilai, jejak in b["angka"]:
            W(row([klaim, nilai, f"`{jejak}`"]))
        W("")
        W(f"**Alternatif yang memakai BoK ini.** {b['alternatif']}")
        W("")
        W(f"**Kegagalan yang terjadi bila BoK ini diabaikan.** {b['gagal']}")
        W("")
        W(f"**Batas pendalaman.** {b['batas']}")
        W("")

    # ---------------- 3.2.8 ----------------
    W("### 3.2.8 Cakupan BoK terhadap alternatif")
    W("")
    W(header(["BoK", "Nama", "Jumlah alternatif", "Alternatif"]))
    for no in sorted(BOK_NAMA, key=lambda x: int(x)):
        alts = [a["id"] for a in ALT["alternatif"] if int(no) in a["bok"]]
        W(row([no, BOK_NAMA[no], len(alts), ", ".join(alts)]))
    W("")
    W("Rubrik penilaian memuat frasa bahwa alternatif solusi minimal tiga per BoK yang berbeda. Bila frasa itu "
      "ditafsirkan sebagai tiga alternatif untuk setiap BoK yang disebut, maka BoK 1, BoK 6, BoK 7, BoK 10, dan BoK 12 "
      "belum memenuhi, karena masing-masing hanya dimuat oleh satu alternatif. Dua jalan keluar yang tersedia: "
      "pertama, mempersempit daftar BoK yang diklaim sehingga setiap BoK yang diklaim memuat minimal tiga alternatif; "
      "kedua, menambah mekanisme pada alternatif yang sudah ada, bukan menciptakan alternatif baru yang tidak berasal "
      "dari inventaris solusi subbab 3.1. Keputusan ini diserahkan kepada pembimbing, dan dicatat sebagai risiko "
      "penilaian pada 3.3.6.")
    W("")

    # ---------------- 3.2.9 ----------------
    W("### 3.2.9 BoK yang belum disentuh dan alasan tidak dipaksakan")
    W("")
    W(header(["BoK", "Nama", "Alasan belum disentuh", "Kandidat pengaitan", "Rekomendasi"]))
    for t in BOK_TERBUKA:
        W(row([t["no"], t["nama"], t["alasan"], t["kandidat"], t["rekomendasi"]]))
    W("")
    W("Empat BoK di atas dibiarkan terbuka dengan sadar. Memaksakan BoK tanpa data akan menghasilkan kalimat yang "
      "terdengar dalam tetapi tidak mengubah satu pun keputusan pada sembilan alternatif. Rubrik menilai kedalaman "
      "penggunaan standar BoK, bukan jumlah BoK yang disebut.")
    W("")

    # ---------------- 3.3 ----------------
    W("## 3.3 Kriteria dan Batasan Pemilihan Alternatif Solusi")
    W("")
    W("Subbab ini menyiapkan bahan untuk subbab 3.4, dan sengaja tidak menetapkan bobot. Bobot adalah keputusan "
      "stakeholder dan dihitung pada subbab 3.4 beserta uji sensitivitasnya.")
    W("")
    W("### 3.3.1 Kriteria pemilihan")
    W("")
    W(header(["Kode", "Kriteria", "Arah", "Satuan", "Status angka"]))
    for c in KRITERIA:
        W(row([c["id"], c["nama"], c["arah"], c["satuan"], c["status"]]))
    W("")
    W("Rincian cara ukur dan sumber setiap kriteria:")
    W("")
    for c in KRITERIA:
        W(f"- **{c['id']} {c['nama']}.** Cara ukur: {c['cara']} Sumber: `{c['sumber']}`.")
    W("")
    W("Kriteria C8 adalah satu-satunya kriteria kualitatif, sehingga rubriknya ditulis terbuka pada tabel kriteria di "
      "atas dan diulang di sini: tingkat 3 bila keluaran satu baris peringatan dengan waktu, keyakinan, dan tindakan "
      "yang disarankan, serta frekuensi pemeriksaan satu kali per empat jam atau lebih jarang; tingkat 2 bila keluaran "
      "berupa daftar kandidat tanpa urutan prioritas, atau frekuensi lebih dari 6 per 24 jam; tingkat 1 bila keluaran "
      "berupa alarm biner tanpa konteks atau menuntut pengguna menafsirkan model. Rubrik ini berstatus asumsi sampai "
      "divalidasi mitra.")
    W("")
    W("Tujuh dari delapan kriteria memiliki angka terukur atau baku, dan hanya C8 yang kualitatif. Ini disengaja, "
      "supaya subbab 3.4 tidak perlu memakai skala 1 sampai 5 untuk hal yang sudah dapat diukur, misalnya false alarm "
      "rate atau jumlah fold.")
    W("")

    W("### 3.3.2 Batasan pemilihan")
    W("")
    W(header(["Kode", "Batasan", "Kategori", "Bukti", "Konsekuensi desain"]))
    for b in BATASAN:
        W(row([b["id"], b["nama"], b["kategori"], f"`{b['bukti']}`", b["konsekuensi"]]))
    W("")
    W("Rincian setiap batasan:")
    W("")
    for b in BATASAN:
        W(f"- **{b['id']} {b['nama']} (kategori {b['kategori']}).** {b['isi']}")
    W("")
    kategori = sorted({b["kategori"] for b in BATASAN})
    W(f"Enam batasan di atas menutup {len(kategori)} kategori, yaitu " + ", ".join(kategori) +
      ". Rubrik menuntut minimal tiga batasan, sehingga syarat itu terpenuhi.")
    W("")

    # ---------------- user stories ----------------
    W("### 3.3.3 User stories")
    W("")
    W(CATATAN_PERAN)
    W("")
    W("Format yang dipakai adalah kalimat peran, kebutuhan, dan manfaat, lalu dilengkapi kriteria penerimaan yang dapat "
      "diukur beserta jejaknya.")
    W("")
    for idx, u in enumerate(USER_STORIES, 1):
        W(f"#### 3.3.3.{idx} {u['id']} {u['peran']}")
        W("")
        W(f"**Cerita.** {u['cerita']}")
        W("")
        W(f"**Mengapa peran ini pemilik masalah.** {u['alasan']}")
        W("")
        W(f"**Status peran.** {u['peran_status']}. Dasar: {u['dasar']}.")
        W("")
        W(f"**Alternatif yang melayani.** {', '.join(u['alternatif'])}. Klaster: {', '.join(u['klaster'])}. "
          f"Kriteria utama: {', '.join(u['kriteria'])}.")
        W("")
        W("**Kriteria penerimaan.**")
        W("")
        W(header(["Kriteria penerimaan", "Ambang", "Jejak", "Status"]))
        for ac in u["acceptance"]:
            W(row([ac["teks"], ac["ambang"], f"`{ac['jejak']}`", ac["status"]]))
        W("")

    W("### 3.3.4 Silang user story, kriteria, dan alternatif")
    W("")
    W(header(["User story", "Peran", "Kriteria", "Alternatif", "Jumlah kriteria terpenuhi"]))
    for u in USER_STORIES:
        lulus = sum(1 for ac in u["acceptance"] if ac["status"].startswith("lulus"))
        total = len(u["acceptance"])
        W(row([u["id"], u["peran"], ", ".join(u["kriteria"]), ", ".join(u["alternatif"]), f"{lulus} dari {total}"]))
    W("")
    W("Kolom terakhir menghitung kriteria penerimaan yang berstatus lulus, bukan yang berstatus terbuka. Ini sengaja "
      "dibuat ketat, supaya kemajuan tidak dilaporkan dari kriteria yang belum diuji.")
    W("")

    W("### 3.3.5 Serahan untuk subbab 3.4")
    W("")
    W("Subbab 3.4 menerima bahan berikut, dan tidak perlu menghitung ulang dari awal:")
    W("")
    W("1. Delapan kriteria dengan arah, satuan, cara ukur, dan sumber angka, pada 3.3.1.")
    W("2. Enam batasan dengan kategori dan konsekuensi desain, pada 3.3.2.")
    W("3. Enam user story dengan kriteria penerimaan terukur, pada 3.3.3.")
    W("4. Empat klaster beserta relasi prasyarat, pada 3.2.3 sampai 3.2.5, sebagai dasar membaca mengapa dua alternatif "
      "tidak boleh dibandingkan sendirian tanpa prasyaratnya.")
    W("")
    W("Yang belum tersedia dan menjadi tugas subbab 3.4:")
    W("")
    W("1. Bobot kriteria. Belum ada wawancara mitra, sehingga bobot wajib ditetapkan sebagai asumsi dengan minimal tiga "
      "skenario sensitivitas, bukan satu angka tunggal.")
    W("2. Skor kriteria kualitatif C8 untuk setiap alternatif. Rubriknya sudah tersedia di 3.3.1.")
    W("3. Perbandingan dengan pilihan draft lama, yang memilih pengklasifikasi pembelajaran mesin tanpa prosedur MCDM.")
    W("")
    W("Larangan yang perlu dipegang subbab 3.4: jangan memakai skala 1 sampai 5 untuk kriteria yang sudah memiliki angka "
      "terukur, misalnya C1, C2, C3, C4, dan C5. Untuk kriteria itu, angka asli dipakai langsung setelah dinormalisasi.")
    W("")

    W("### 3.3.6 Hasil negatif dan batas yang harus dinyatakan")
    W("")
    W("1. Peran pemilik masalah belum diverifikasi melalui wawancara. Pencarian kata wawancara dan interview pada "
      "seluruh berkas `docs/` tidak menemukan berkas lain selain dokumen ini, sehingga empat dari enam peran pada "
      "3.3.3 berstatus peran operasi yang belum dikonfirmasi mitra.")
    W("2. Tarif rig per jam tidak tersedia, sehingga nilai rupiah apa pun pada subbab 3.4 berstatus asumsi.")
    W("3. Portabilitas antar sumur sesudah kalibrasi belum terukur. Yang terukur baru sebaran sebelum kalibrasi, yaitu "
      "4,15 sampai 496,09 per 24 jam (`docs/V9_PM2_VERDICT.md:114`).")
    W("4. Prevalensi unit stand 10 sampai 40 persen pada A4 masih perkiraan desain (`docs/V7_R1_SOLUTIONS.md:111`).")
    W("5. Presisi titik ubah pada alat bengkel hanya 0,50, sehingga klaim keausan progresif belum sah untuk alat baru "
      "(`docs/V9_EVAL_C_LAYERC.md:98`).")
    W("6. Rubrik yang menuntut tiga alternatif per BoK belum terpenuhi untuk BoK 1, 6, 7, 10, dan 12. Risiko penilaian "
      "ini dicatat pada 3.2.8, beserta dua jalan keluarnya.")
    W("7. System response time dan downtime belum diukur, sehingga standar BoK 11 yang berkaitan dengannya tidak dapat "
      "diklaim terpenuhi.")
    W("8. Antarmuka peringatan belum dirancang, sehingga kriteria C8 belum dapat dinilai untuk alternatif mana pun.")
    W("")

    # ---------------- manifest ----------------
    W("### 3.3.7 Manifes jejak angka (internal, bukan untuk sirkulasi eksternal)")
    W("")
    W(header(["Angka", "Nilai", "Berkas dan baris"]))
    manifest = [
        ("FAR vib antar sumur", "4,15 sampai 496,09 per 24 jam, rasio 119,6 kali", "docs/V9_PM2_VERDICT.md:114"),
        ("Kontrol-positif stuck", "0 dari 10", "docs/V8_PM_VERDICT.md:202"),
        ("Stuck K-ii", "B1 0,51 sampai 1,00, TLead 10 sampai 11,5 menit", "docs/V9_EVAL_B_LAYERB.md:101"),
        ("Hyd K-ii", "0 dari 3 onset, TLead nol", "docs/V9_EVAL_B_LAYERB.md:103"),
        ("Tool_wear K-i", "4 dari 4 alat, TLead 20 sampai 36 detik, FP 1 sampai 3, presisi run 0,50", "docs/V9_EVAL_C_LAYERC.md:98"),
        ("Tool_wear K-ii canary", "AUPRC 0,516 sampai 0,612 atau 1,19 kali", "docs/V9_EVAL_C_LAYERC.md:99"),
        ("Gate shk", "G1 3 dari 7, G2 6 dari 7", "docs/V7_R1_SOLUTIONS.md:97"),
        ("Gate hyd", "G1 2 dari 7, G2 4 dari 7", "docs/V7_R1_SOLUTIONS.md:127"),
        ("Gate tool_wear", "G1 0 dari 4, G2 4 dari 4", "docs/V7_R1_SOLUTIONS.md:160"),
        ("Gate ssi", "G1 4 dari 5, G2 5 dari 5, F-7 tiga positif, F-9 dua belas positif", "docs/V7_R1_SOLUTIONS.md:197"),
        ("Gate bit_wear", "G1 3 dari 4, G2 4 dari 4, persistence menang 4 dari 4", "docs/V7_R1_SOLUTIONS.md:203"),
        ("Kanal disfungsi empat wellbore", "188/186/66/18, 135/135/135/86, 91/90/52/6, 77/76/76/76", "docs/V7_R1_SOLUTIONS.md:45-48"),
        ("Kanal label fisika", "GAINLOSSTOT 575 dan 517, PITTOT 565 dan 506, FLOWOUT 688, FLOWOUTPC 949", "docs/V7_R1_SOLUTIONS.md:37-38"),
        ("Baris CRPM hasil parse", "281.030 / 42.010 / 178.430 / 57.846", "docs/V9_PM1_ARCHITECTURE.md:186"),
        ("TSPP", "52.905 baris, empat berkas", "docs/V10_D1_BAB_DATA.md:86, 296"),
        ("Basis label kurasi", "884 kejadian, 50 relevan BHA, 73.500 menit atau 1.225 jam", "docs/PPT1_LEDGER_ANGKA.md:145, 193"),
        ("Berkas bhaRun tanpa label keausan", "77 berkas", "docs/V4_MAINTENANCE_ML_OPTIONS.md:62"),
        ("Prevalensi unit stand", "10 sampai 40 persen, berstatus asumsi", "docs/V7_R1_SOLUTIONS.md:111"),
        ("Ambang kelayakan pemantauan", "FAR maksimal 6 per 24 jam", "docs/V8_R1_ABC_SPEC.md:240"),
        ("Keluaran screening shk", "FAR 18 sampai 63 per 24 jam, presisi 0,00 sampai 0,12", "docs/V8_E_shk_CAPABILITY.md:106"),
        ("Tiga angka pengikat", "7 engine, 11 klaim, 27 head", "docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md:57"),
        ("Lapisan keputusan", "5 / 11 / 9 / 2 sama dengan 27", "docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md:3142"),
        ("Sumber data", "Volve terbuka dan empat set data eksternal", "docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md:12"),
        ("Batas muktamad cakupan", "satu lapangan, bengkel berbeda dari rig, hyd proksi", "docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md:327"),
        ("Slot alarm otomatis", "0 pada 27 head", "scratch/v9_i1/v9_i1_RESULTS.json kunci auto_critical_alarm_slots"),
    ]
    for a, b, c in manifest:
        W(row([a, b, f"`{c}`"]))
    W("")
    W("Reproduksi: `python3 scratch/ppt1/build_bab3_2.py` menulis ulang dokumen ini dan `scratch/ppt1/affinity.json`, "
      "lalu `python3 scratch/ppt1/check_bab3_2.py` memeriksa acceptance dan keberadaan setiap jejak. Pemeriksa itu "
      "sendiri sudah diuji negatif, yaitu menolak rujukan baris di luar berkas, menolak em-dash, menolak klaster yang "
      "kehilangan satu alternatif, dan menolak user story tanpa kriteria penerimaan. Keluaran uji negatif tersimpan di "
      "`scratch/ppt1/check_bab3_2_negative_test.txt`, dengan hasil lima dari lima kasus sesuai harapan.")
    W("")
    return "\n".join(L)


def build_json():
    alt_ids = [a["id"] for a in ALT["alternatif"]]
    data = {
        "meta": {
            "dokumen": "BAB III 3.2 Analisis Alternatif Solusi dan 3.3 Kriteria dan Batasan",
            "versi": "1.0",
            "dibuat": "2026-10-25 WIB",
            "skrip": "scratch/ppt1/build_bab3_2.py",
            "data": ["scratch/ppt1/bab3_2_data.py", "scratch/ppt1/bab3_2_data_bok.py", "scratch/ppt1/bab3_2_data_us.py"],
            "sumber_utama": META["sumber_utama"],
            "sumber_alternatif": "scratch/ppt1/alternatif.json",
            "metode_afinitas": METODE_AFINITAS,
            "periksa": "dijalankan oleh scratch/ppt1/check_bab3_2.py",
        },
        "klaster": KLASTER,
        "relasi_klaster": RELASI_KLASTER,
        "matriks_klaster_bok": MATRIKS_KLASTER_BOK,
        "matriks_klaster_masalah": MATRIKS_KLASTER_MASALAH,
        "overlay_lapisan": OVERLAY_LAPISAN,
        "rekap": {
            "jumlah_klaster": len(KLASTER),
            "jumlah_alternatif_terkelompok": sum(len(k["anggota"]) for k in KLASTER),
            "alternatif_dikenal": alt_ids,
            "masalah_tercakup": sorted({p for ps in MATRIKS_KLASTER_MASALAH.values() for p in ps}),
            "bok_tersentuh": sorted({b for bs in MATRIKS_KLASTER_BOK.values() for b in bs}),
            "bok_didalami": [b["no"] for b in BOK_DIDALAMI],
            "jumlah_kriteria": len(KRITERIA),
            "jumlah_batasan": len(BATASAN),
            "jumlah_user_story": len(USER_STORIES),
            "jumlah_kriteria_penerimaan": sum(len(u["acceptance"]) for u in USER_STORIES),
        },
        "g1": G1,
        "bok_didalami": BOK_DIDALAMI,
        "bok_terbuka": BOK_TERBUKA,
        "kriteria": KRITERIA,
        "batasan": BATASAN,
        "user_stories": USER_STORIES,
        "matriks_us_kriteria": MATRIKS_US_KRITERIA,
        "catatan_peran": CATATAN_PERAN,
    }
    return data


def acceptance(data):
    errs = []
    alt_ids = [a["id"] for a in ALT["alternatif"]]
    seen = []
    for k in data["klaster"]:
        seen.extend(k["anggota"])
    if sorted(seen) != sorted(alt_ids):
        errs.append(f"klaster tidak menutup 9 alternatif tepat sekali: {sorted(seen)} vs {sorted(alt_ids)}")
    if len(seen) != len(set(seen)):
        errs.append("ada alternatif yang masuk lebih dari satu klaster")
    if len(data["bok_didalami"]) < 3:
        errs.append("BoK didalami kurang dari 3")
    if len(data["user_stories"]) < 4:
        errs.append("user story kurang dari 4")
    for u in data["user_stories"]:
        if len(u["acceptance"]) < 1:
            errs.append(f"{u['id']} tidak punya kriteria penerimaan")
        for ac in u["acceptance"]:
            if not ac.get("jejak"):
                errs.append(f"{u['id']} punya kriteria penerimaan tanpa jejak")
    if len(data["kriteria"]) < 5:
        errs.append("kriteria kurang dari 5")
    if len(data["batasan"]) < 3:
        errs.append("batasan kurang dari 3")
    if len({b["kategori"] for b in data["batasan"]}) < 3:
        errs.append("kategori batasan kurang dari 3")
    for n in data["g1"]["node_alternatif"]:
        if n["id"] not in alt_ids:
            errs.append(f"node G1 memuat alternatif tidak dikenal: {n['id']}")
    if len(data["g1"]["node_alternatif"]) != len(alt_ids):
        errs.append("node G1 tidak memuat 9 alternatif")
    return errs


def main():
    md = render()
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write(md)
    data = build_json()
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    errs = acceptance(data)
    print(f"MD   : {OUT_MD} ({len(md.splitlines())} baris)")
    print(f"JSON : {OUT_JSON}")
    print(f"klaster={len(data['klaster'])} alternatif={data['rekap']['jumlah_alternatif_terkelompok']} "
          f"bok_didalami={len(data['bok_didalami'])} kriteria={len(data['kriteria'])} "
          f"batasan={len(data['batasan'])} user_story={len(data['user_stories'])} "
          f"acceptance={data['rekap']['jumlah_kriteria_penerimaan']}")
    if errs:
        print("GAGAL:")
        for e in errs:
            print(" -", e)
        return 1
    print("ACCEPTANCE INTERNAL: LOLOS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
