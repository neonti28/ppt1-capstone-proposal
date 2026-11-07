#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RND-E1: menulis docs/RND_E1_MATRIKS.md dan bagian ledger E1 dari e1_scores.json.
Satu sumber untuk tabel dan JSON supaya keduanya tidak mungkin berbeda.
"""
import json, os, re, datetime

BASE = "/mnt/d/Capstone 1(v2)"
OUT = os.path.join(BASE, "scratch", "rnd_e1")
DOC = os.path.join(BASE, "docs", "RND_E1_MATRIKS.md")
LEDGER = os.path.join(BASE, "docs", "RND_PROVENANCE_LEDGER.md")
TANGGAL = "2026-10-27"
D = json.load(open(os.path.join(OUT, "e1_scores.json")))
M = D["matriks"]
ENG = ["vib", "ssi", "shk", "stuck", "hyd", "bit_wear", "tool_wear"]
SING = {"ADA": "A", "SEBAGIAN": "S", "TIDAK": "T"}

# --- finalis dan shortlist (keputusan manusia yang di-hardcode, bukan hasil hitung) ---
SHORTLIST = ["A10", "A19", "A16", "A06", "A04", "A07"]
FINALIS = [
    ("A10", "hyd", "Kalibrasi ambang per well secara prospektif (conformal V3)"),
    ("A16", "tool_wear", "Page-Hinkley dan CUSUM dengan reset, terkalibrasi per alat"),
    ("A06", "shk", "Boosting terkalibrasi (LightGBM atau XGBoost) pada kelas bervolume besar"),
]
JALUR_GATE = {
 "A10": {
  "C": "hyd sudah memenuhi C paling lengkap di antara kelas status: CI persistence tidak memuat prevalensi di "
       "0 dari 9 well (ledger R1-032). Klaim pilot tidak boleh melemahkan itu, jadi hasil per well dilaporkan "
       "utuh dan uji tanda dipakai dengan syarat 8 dari 9 well sepakat pada tingkat 0,05 (R6 bagian 3.1).",
  "A": "satu-satunya gerbang yang kini gagal adalah FAR hybrid 14,6 sampai 58,4 per 24 jam terhadap gerbang 6. "
       "Alpha conformal dipilih supaya laju alarm yang dijanjikan berada di bawah 6, lalu FAR dilaporkan sebagai "
       "laju kalender dengan cakupan waktu (menjawab temuan Kritis E0 K-4).",
  "B": "hybrid sudah memangkas FP dari 2.091 ke 927 (55,7 persen) secara konsisten di 9 dari 9 well. Target "
       "pilot adalah mempertahankan pemangkasan itu sambil menurunkan jumlah alarm yang harus diperiksa manusia "
       "per shift, bukan per menit.",
  "stop": "alpha yang dibutuhkan untuk mencapai FAR 6 ternyata menghasilkan nol alarm pada baseline, sehingga "
          "detektor tidak lagi berguna. Pada kondisi itu statusnya bukan gagal, melainkan bukti bahwa ambang "
          "tunggal tidak bisa melayani 9 well sekaligus, dan hasilnya dilaporkan sebagai temuan.",
 },
 "A16": {
  "C": "hanya ada 4 alat, dan uji tanda dengan 4 unit berdaya 0 pada semua tingkat konkordansi (R6 bagian 3.1). "
       "Karena itu klaim C untuk tool_wear tidak boleh memakai uji tanda: yang sah adalah LOTO 4 fold yang "
       "dilaporkan per alat, dan klaim lintas alat hanya dibuat bila keempatnya searah, bukan dari rata-rata.",
  "A": "gate A relatif sudah terpenuhi: FP 1 sampai 3 per alat dengan ambang terkalibrasi (ledger L-33). "
       "Target pilot adalah menjaga FAR itu ketika ambang dipindah ke alat baru, yaitu menguji apakah kalibrasi "
       "bertahan di luar alat yang dipakai untuk mengalibrasi.",
  "B": "masalah utama kelas ini bukan FAR melainkan beban pemeriksaan: presisi run 0,50 dengan 4 FP pada alat "
       "baru. Target pilot adalah menurunkan FP per shift tanpa mengorbankan TLead 1,8 kali yang sudah terukur.",
  "stop": "bila FP pada alat baru tidak turun setelah reset diaktifkan, kesimpulannya metode ini menangkap "
          "perubahan regime yang bukan keausan, dan itu dilaporkan sebagai batas klaim, bukan sebagai kegagalan alat.",
 },
 "A06": {
  "C": "shk punya 9 well, tetapi CI RF memuat prevalensi di 7 dari 9 fold (ledger R1-030). Target pilot adalah "
       "menutup CI itu, dan itu hanya bisa diklaim bila boosting menang di hampir semua well, karena uji tanda "
       "butuh 8 dari 9 sepakat dan daya baru 0,775 pada konkordansi 0,90 (R6 bagian 3.1).",
  "A": "rule di kelas ini sudah lolos FAR 0,67 sampai 6,6 per 24 jam di 7 dari 9 fold (ledger R3-51). "
       "Karena itu kriteria gate A bersifat mempertahankan, bukan memperbaiki: boosting yang AUPRC-nya naik "
       "tetapi FAR-nya melewati 6 di lebih banyak fold dinyatakan gagal, walau AUPRC lebih tinggi.",
  "B": "prevalensi 0,0355 (ledger R4-29) berarti pada 24 jam jumlah alarm yang bisa diterima manusia jauh lebih "
       "kecil dari jumlah jendela positif. Beban dilaporkan sebagai pemeriksaan per shift pada titik operasi "
       "yang dipatok, bukan sebagai presisi di titik operasi terbaik.",
  "stop": "bila biaya latih terukur melebihi anggaran run sehingga hanya satu fold yang bisa diselesaikan, "
          "hasilnya tidak boleh dilaporkan sebagai perbandingan, dan statusnya kembali BELUM TERUKUR.",
 },
}

ALASAN_BUKAN_FINALIS = {
    "A19": "skor 2,50 tetapi perannya gerbang diagnosis sebelum meminjam ambang, bukan detektor; gerbang tidak dipilotkan sebagai model",
    "A04": "skor 2,25 tetapi R3 menyebutnya pembanding murah, bukan pengganti rule; menaikkan tier tidak berasal dari SVM",
    "A07": "skor 2,00 dan bersaing langsung dengan A06 pada tujuan yang sama; dua finalis tidak boleh menguji hal yang sama",
    "A15": "skor 2,20 dan satu paket dengan A16; CUSUM tanpa reset sudah terbukti menyala 52,293 sampai 60,000 menit tiap jam (ledger R5-032)",
    "A17": "skor 2,35 tetapi belum dijalankan sama sekali pada data kita; masuk shortlist sebagai pembanding A16, bukan finalis",
    "A01": "skor 2,00; R1 sendiri menyatakan pembatas sebenarnya adalah portabilitas ambang, bukan dimensi fitur",
}

def cell_txt(kode, e):
    c = M[kode]["sel"][e]
    return f'{c["skor"]}/{SING[c["status"]]}'

def fmt(x):
    return f"{x:.2f}".replace(".", ",")

L = []
w = L.append

w("# RND-E1: MATRIKS KELAYAKAN ALGORITMA x ENGINE DAN SHORTLIST")
w("")
w(f"Kartu: `t_9abcb3b3` · Board: `rnd-algo-2026` · Tanggal: {TANGGAL} (WIB)")
w("Workspace: `/mnt/d/Capstone 1(v2)` · Arsip `/mnt/d/Capstone 1` tidak disentuh")
w("Masukan: R1, R2, R3, R4, R5, R6, D0, P0, E0, dan tabel tier `docs/V9_EVAL_C_LAYERC.md`.")
w("Keluaran: matriks 28 algoritma x 7 engine (196 sel), skor prioritas berbobot, 6 kandidat, 3 finalis.")
w("")
w("## Riset pendahuluan")
w("")
w("Riset pendahuluan: what-if-oracle, statistical-analysis, verification-mandatory, scientific-critical-thinking")
w("")
w("- `what-if-oracle` dipakai untuk memetakan empat cabang hasil pilot (finalis berhasil menurunkan FAR, "
  "finalis berhasil tetapi biayanya tidak terbayar, finalis gagal karena label, dan cabang liar berupa "
  "perubahan definisi label), lalu memilih tindakan tanpa penyesalan yang berlaku di semua cabang.")
w("- `statistical-analysis` dipakai untuk menolak membandingkan angka antar kelas yang desainnya berbeda: "
  "uji yang sah ditentukan per pertanyaan (Wilson untuk presisi, Poisson eksak Garwood untuk rasio FAR, "
  "uji tanda untuk arah per well), dan efek minimum yang dapat dideteksi dipakai sebagai syarat sebelum "
  "menjanjikan kenaikan tier, bukan sesudahnya.")
w("- `verification-mandatory` dipakai sebagai gerbang tulis: setiap angka di dokumen ini menunjuk baris "
  "ledger, skor yang merupakan penilaian diberi kelas KONVENSI, dan angka yang tidak terukur ditulis "
  "BELUM TERUKUR tanpa dibulatkan menjadi tebakan.")
w("- `scientific-critical-thinking` dipakai untuk memisahkan \"metode ini bagus di literatur\" dari "
  "\"metode ini bisa menyerang gate C, A, atau B pada data ini\", dan untuk menandai tiga sumber bias "
  "yang nyata di proyek ini: sirkularitas label, pemilihan titik operasi setelah melihat hasil, serta "
  "penyebut FAR yang bukan kalender.")
w("")
w("Riset pendahuluan: sequentialthinking, 6 pikiran (`mcp__sequentialthinking__sequentialthinking`, "
  "thoughtNumber 1..6, thoughtHistoryLength 6). Ringkas: (1) tiga skala skor R1-R6 tidak boleh dijahit "
  "tanpa rubrik, (2) skor kesesuaian dan status data wajib dipisah, (3) bobot diturunkan dari plan bagian 6 "
  "dan temuan D0 serta E0, bukan dari hasil yang diinginkan, (4) uji balik bobot: menurunkan bobot risiko "
  "akan menaikkan metode yang menang karena artefak, (5) pemilihan tiga finalis dari kegagalan gate yang "
  "paling umum, (6) pemisahan tegas antara ditolak dan ditunda.")
w("")
w("---")
w("")
w("## 0. Ringkasan keputusan")
w("")
w("| Butir | Keputusan |")
w("|---|---|")
w("| Algoritma yang masuk matriks | 28 baris, 196 sel, 7 engine |")
w("| Algoritma dengan skor prioritas di atas 2,0 | {{N_GT2}} dari {{N_ALG}} |")
w("| Shortlist | 6 kandidat |")
w("| Finalis pilot | 3 kandidat |")
w("| Ditolak permanen | {{N_TOLAK}} algoritma atau keluarga algoritma |")
w("| Ditunda | {{N_TUNDA}} algoritma atau keluarga algoritma |")
w("| Temuan terpenting | pembatas utama bukan pilihan algoritma, melainkan portabilitas ambang antar unit "
  "(sebar FAR 119 kali pada vib, ledger R5-072) dan kualitas label (bit_wear, ledger R5-068) |")
w("")
w("---")
w("")
w("## 1. Cara membaca matriks")
w("")
w("### 1.1 Rubrik skor kesesuaian sel (0 sampai 3)")
w("")
w("| Skor | Arti |")
w("|---|---|")
w("| 0 | Tidak ada peran pada engine itu: metode tidak menyentuh gate C, A, atau B di kelas tersebut |")
w("| 1 | Peran pinggiran atau pembanding: bisa dipakai, tetapi tidak mengubah keputusan tier |")
w("| 2 | Menyerang satu syarat gate pada engine itu |")
w("| 3 | Menyerang syarat gate yang justru menjadi kegagalan utama engine itu |")
w("")
w("Rubrik ini keputusan dokumen (KONVENSI, ledger E1-006). Ia tidak boleh dibaca sebagai hasil ukur.")
w("")
w("### 1.2 Status data (dari D0, bukan taksiran)")
w("")
w("| Status | Arti |")
w("|---|---|")
w("| `A` | ADA: kanal dan label tersedia, jumlah jendela terukur |")
w("| `S` | SEBAGIAN: kanal atau label hanya ada di sebagian well, atau kanal penentu absen |")
w("| `T` | TIDAK: prasyarat fisik tidak terpenuhi, misalnya laju sampel di bawah pita diagnostik |")
w("")
w("### 1.3 Aturan angka")
w("")
w("Setiap angka di tabel alasan menunjuk baris ledger. Angka yang tidak punya baris ledger tidak ditulis. "
  "Daftar baris baru untuk kartu ini ada di `docs/RND_PROVENANCE_LEDGER.md` bagian E1.")
w("")
w("---")
w("")
w("## 2. MATRIKS A: algoritma x 7 engine")
w("")
w("Format sel: `skor/status`, contoh `2/A` berarti skor kesesuaian 2 dan data ADA.")
w("Baris diurutkan menurut skor prioritas tertinggi algoritma tersebut (lihat bagian 5).")
w("")
hdr = "| Kode | Algoritma | Sumber | " + " | ".join(ENG) + " |"
w(hdr)
w("|" + "---|" * (3 + len(ENG)))
rank = {r["algoritma"]: i for i, r in enumerate(D["peringkat_algoritma"])}
order = sorted(M.keys(), key=lambda k: (rank.get(k, 999), k))
for k in order:
    a = M[k]
    w(f'| {k} | {a["nama"]} | {a["sumber"]} | ' + " | ".join(cell_txt(k, e) for e in ENG) + " |")
w("")
w("Bacaan cepat: sel `0/T` menandai prasyarat fisik yang tidak terpenuhi, misalnya laju sampel di bawah "
  "pita diagnostik, bukan penilaian bahwa metodenya jelek.")
w("")
w("---")
w("")
w("## 3. Alasan satu baris untuk tiap sel")
w("")
w("Sel dengan skor 0 yang bukan karena prasyarat fisik dikelompokkan di akhir tiap engine, karena alasannya "
  "sama dan menuliskannya 12 kali tidak menambah informasi.")
w("")
for e in ENG:
    w(f"### 3.{ENG.index(e)+1} Engine `{e}`")
    w("")
    w("| Kode | Algoritma | Skor | Data | Alasan satu baris |")
    w("|---|---|---|---|---|")
    nonzero = [k for k in order if M[k]["sel"][e]["skor"] > 0]
    zero = [k for k in order if M[k]["sel"][e]["skor"] == 0]
    for k in nonzero:
        c = M[k]["sel"][e]
        w(f'| {k} | {M[k]["nama"]} | {c["skor"]} | {c["status"]} | {c["alasan"]} |')
    w(f'| lainnya | {len(zero)} algoritma | 0 | campuran | tidak ada peran pada engine ini; alasan per algoritma ada di bagian 8 dan di sel engine lain |')
    w("")
w("---")
w("")
w("## 4. MATRIKS B: lapisan evaluasi (R6) dan gate")
w("")
w("R6 tidak memberi skor per engine, karena isinya metode evaluasi, bukan model prediksi. Karena itu R6 "
  "tidak dipaksa masuk sebagai baris matriks A: memasukkannya akan membuat kolom engine berisi angka yang "
  "tidak bermakna. R6 dilaporkan sebagai matriks B dengan kolom gate.")
w("")
w("| Metode | Gate C | Gate A | Gate B | Status pada data kita | Rujukan |")
w("|---|---|---|---|---|---|")
w("| Wilson (presisi) | ya, lebar CI | tidak | tidak | TERUKUR | R6 bagian 2.9 |")
w("| Poisson eksak Garwood (rasio FAR) | tidak | ya | tidak | TERUKUR | R6 bagian 2.9 |")
w("| Fisher eksak (dua well berbeda) | ya | tidak | tidak | TERUKUR | R6 bagian 2.9 |")
w("| Uji tanda (arah per well) | ya | tidak | tidak | TERUKUR, n = 4, 7, 9 | R6 bagian 3.1 |")
w("| Bootstrap blok per well | ya | ya | tidak | TERUKUR pada simulasi, data nyata butuh skor per jendela | R6 bagian 2.9 |")
w("| DeLong | ya | tidak | tidak | BELUM TERUKUR, skor per jendela tidak disimpan | R6 bagian 2.9 |")
w("| McNemar | tidak | tidak | ya | BELUM TERUKUR, hitungan berpasangan tidak ada | R6 bagian 2.9 |")
w("| Holm dan BH | ya | ya | ya | TERUKUR | R6 bagian 2.9 |")
w("| MDE rasio laju FAR | tidak | ya | tidak | TERUKUR, MDE pada rasio 1,40 | R6 bagian 3.2 |")
w("")
w("Konsekuensi yang harus dibaca sebelum memilih finalis: dua uji yang paling sering diminta untuk klaim "
  "\"algoritma X lebih baik\", yaitu DeLong dan McNemar, tidak dapat dijalankan pada artefak yang ada. "
  "Artinya setiap klaim perbandingan antar model pada gelombang ini harus disandarkan pada uji tanda, "
  "Fisher, dan bootstrap, atau harus lebih dulu menyimpan skor per jendela.")
w("")
w("---")
w("")
w("## 5. Skor prioritas, bobot, dan alasan bobot")
w("")
w("### 5.1 Bobot")
w("")
w("| Komponen | Bobot | Alasan bobot |")
w("|---|---|---|")
w("| Potensi naik tier (0-3) | 0,50 | Plan bagian 6 menyatakan tier hanya naik bila C stabil, A FAR memadai, "
  "dan B beban wajar terpenuhi bersamaan. Metode yang tidak menyentuh salah satu syarat itu tidak punya "
  "nilai proyek, seberapa pun bagusnya di literatur. Bobot terbesar karena alasan ini, bukan karena selera. |")
w("| Kelayakan data (0,25) | 0,25 | D0 menunjukkan blokir data bersifat mutlak dan tidak dapat diperbaiki "
  "algoritma apa pun: Nyquist 0,1667 Hz (ledger R3-02), STUCK_RT hanya di 4 dari 9 well, FlowOut absen. "
  "Blokir seperti ini membunuh kandidat lebih cepat daripada kelemahan metode. |")
w("| Risiko (0,15, terbalik) | 0,15 | E0 menemukan 5 temuan Kritis di mana angka terlihat bagus padahal "
  "artefak: presisi rule yang tidak pernah menyala saat status belum aktif (K-1), lead time yang dikreditkan "
  "ke kejadian salah (K-2), dan kriteria \"pernah menyala sekali\" (K-3). Bobot ini menahan kandidat yang "
  "menang karena artefak. |")
w("| Biaya (0,10, terbalik) | 0,10 | Biaya membatasi berapa varian yang bisa dicoba, bukan apakah metodenya "
  "sah. Pembatas biaya yang ekstrem sudah tertangkap di sel skor, misalnya kNN-DTW 137.374,35 jam "
  "(ledger R3-40). Memberi bobot besar akan menghukum dua kali. |")
w("")
w("Rumus: skor = 0,50 x tier + 0,25 x data + 0,15 x risiko + 0,10 x biaya, dengan skala 0 sampai 3.")
w("Gerbang: bila potensi tier pada engine itu 0, skor dipaksa 0. Tanpa gerbang ini, metode pendukung "
  "seperti Monte Carlo menang karena dua komponen terbalik memberi lantai nilai, padahal kontribusinya ke "
  "tier nol. Gerbang dan koreksinya dicatat terbuka di ledger E1-005 dan E1-017.")
w("")
w("Tiga hal yang perlu dinyatakan jujur:")
w("")
w("1. Bobot dan skor komponen adalah KONVENSI rekayasa, bukan hasil ukur. Yang terukur adalah angka di "
  "kolom alasan; bobot hanya cara mengurutkan. Dokumen ini menyebutnya terbuka supaya bisa dibantah "
  "dengan argumen, bukan disembunyikan di balik angka desimal.")
w("2. Skor komponen biaya untuk LightGBM dan XGBoost (1) adalah batas bawah, karena biaya latihnya BELUM "
  "TERUKUR (ledger E1-018). Kalau nanti biaya terukur murah, skornya naik dan peringkatnya berubah. Itu "
  "dinyatakan sekarang supaya tidak dibaca sebagai penilaian final.")
w("3. Memilih enam kandidat lalu tiga finalis dari satu tabel berbobot adalah bentuk pemilihan setelah "
  "melihat hasil. Mitigasinya: kriteria finalis dikunci sebelum tabel dihitung, yaitu data ADA atau "
  "SEBAGIAN dan jalur eksplisit ke gate C, A, B. Semua finalis di bagian 7 memenuhi kriteria itu, dan "
  "kandidat yang skornya lebih tinggi tetapi tidak memenuhi kriteria dicatat sebagai bukan finalis "
  "beserta alasannya.")
w("")
w("### 5.2 Peringkat per engine sasaran")
w("")
w("| # | Kode | Algoritma | Engine sasaran | Tier | Data | Risiko | Biaya | Skor |")
w("|---|---|---|---|---|---|---|---|---|")
for i, r in enumerate(D["peringkat_algoritma"], 1):
    k = r["komponen"]
    w(f'| {i} | {r["algoritma"]} | {r["nama"]} | {r["engine"]} | {k["tier"]} | {k["data"]} | '
      f'{k["risiko"]} | {k["biaya"]} | **{fmt(r["skor_prioritas"])}** |')
w("")
w("Engine sasaran adalah engine tempat algoritma itu direkomendasikan R1 sampai R6, bukan engine dengan "
  "skor tertinggi. Aturan ini dipakai supaya algoritma tidak diberi panggung pada engine yang jelas tidak "
  "membutuhkannya: tanpa aturan ini, Isolation Forest akan dinilai pada shk yang sudah berlabel dan "
  "tampak lebih baik daripada perannya yang sebenarnya, yaitu triase pada kelas tanpa label. Pemetaan "
  "engine sasaran ada di `scratch/rnd_e1/e1_build.py` konstanta `TARGET`.")
w("")
w("Kolom tier, data, risiko, biaya adalah skor komponen 0 sampai 3. Kolom Skor adalah hasil rumus 5.1. "
  "Algoritma dengan skor 0 tidak muncul karena gerbang tier memaksanya ke 0.")
w("")
w("---")
w("")
w("## 6. SHORTLIST: 6 kandidat")
w("")
w("Enam kandidat dipilih dari peringkat 5.2 dengan satu syarat tambahan: tiap kandidat harus punya engine "
  "dengan data ADA atau SEBAGIAN dan satu jalur gate yang bisa ditunjuk. Nomor urut adalah peringkat skor.")
w("")
w("| # | Kode | Kandidat | Engine target | Skor | Kenapa masuk shortlist |")
w("|---|---|---|---|---|---|")
SL_WHY = {
 "A10": "satu-satunya metode yang menyerang kegagalan C paling umum, yaitu portabilitas ambang; pada hyd satu-satunya gerbang tersisa adalah FAR",
 "A19": "gerbang diagnosis sebelum meminjam ambang antar well; R5 menempatkannya sebagai prioritas kedua setelah CUSUM dan PH",
 "A16": "detektor perubahan level yang biayanya rendah dan interpretasinya bisa diaudit; satu paket dengan CUSUM",
 "A06": "satu-satunya jalur yang bisa menaikkan daya deteksi pada kelas bervolume besar, dan biayanya belum pernah diukur",
 "A04": "pembanding murah yang bisa menandingi rule pada fitur tabular, khususnya pada tool_wear yang 27 fitur",
 "A07": "keunggulan kategorikal alat pada LOTO, satu-satunya kelas dengan identitas alat eksplisit",
}
for i, k in enumerate(SHORTLIST, 1):
    r = next(x for x in D["peringkat_algoritma"] if x["algoritma"] == k)
    w(f'| {i} | {k} | {r["nama"]} | {r["engine"]} | **{fmt(r["skor_prioritas"])}** | {SL_WHY[k]} |')
w("")
w("---")
w("")
w("## 7. FINALIS: 3 kandidat pilot")
w("")
w("Kriteria finalis dikunci sebelum tabel 5.2 dihitung: (a) data ADA atau SEBAGIAN, (b) ada jalur eksplisit "
  "ke gate C, A, dan B, (c) tiga finalis tidak menguji hal yang sama.")
w("")
w("Tiga syarat yang berlaku untuk KETIGA finalis sebelum run dijalankan:")
w("")
w("1. Pra-registrasi titik operasi ditulis lebih dulu, termasuk alpha, ambang, dan aturan penolakan. "
  "Tanpa ini, memilih titik operasi setelah melihat hasil adalah p-hacking yang tidak bisa dibedakan dari temuan.")
w("2. Skor per jendela disimpan per fold per model. Saat ini skor itu tidak disimpan, sehingga DeLong dan "
  "McNemar tidak dapat dijalankan (R6 bagian 2.9), dan setiap klaim perbandingan antar model akan tetap "
  "berstatus hipotesis tanpa artefak ini.")
w("3. FAR dilaporkan sebagai laju kalender beserta cakupan waktu teramati, bukan laju per menit teramati. "
  "Temuan Kritis E0 K-4 menunjukkan cakupan menit teramati hanya 1,46 sampai 71,7 persen, sehingga FAR "
  "yang dilaporkan tanpa cakupan menyesatkan ke arah optimistis.")
w("")
for i, (k, e, peran) in enumerate(FINALIS, 1):
    r = next(x for x in D["peringkat_algoritma"] if x["algoritma"] == k)
    c = M[k]["sel"][e]
    g = JALUR_GATE[k]
    w(f"### 7.{i} Finalis {i}: {M[k]['nama']} pada `{e}`")
    w("")
    w(f"Peran pilot: {peran}.")
    w("")
    w(f"- Skor prioritas {fmt(r['skor_prioritas'])} (tier {r['komponen']['tier']}, data "
      f"{r['komponen']['data']}, risiko {r['komponen']['risiko']}, biaya {r['komponen']['biaya']}).")
    w(f"- Status data: {c['status']}. Alasan sel: {c['alasan']}.")
    w(f"- Jalur ke gate C: {g['C']}")
    w(f"- Jalur ke gate A: {g['A']}")
    w(f"- Jalur ke gate B: {g['B']}")
    w(f"- Kriteria berhenti: {g['stop']}")
    w("")
w("### 7.4 Kandidat yang skornya lebih tinggi atau setara tetapi bukan finalis")
w("")
w("| Kode | Skor | Alasan bukan finalis |")
w("|---|---|---|")
for k, alasan in ALASAN_BUKAN_FINALIS.items():
    r = next(x for x in D["peringkat_algoritma"] if x["algoritma"] == k)
    w(f'| {k} | {fmt(r["skor_prioritas"])} | {alasan} |')
w("")
w("---")
w("")
w("## 8. Ditolak, ditunda, dan alasannya")
w("")
w("### 8.1 Ditolak permanen (alasan fisik atau biaya, bukan selera)")
w("")
w("| Algoritma | Alasan penolakan | Bukti |")
w("|---|---|---|")
w("| VMD, EMD, wavelet | laju sampel tertinggi 0,3333 Hz memberi Nyquist 0,1667 Hz, sementara pita diagnostik "
  "bantalan berada pada orde ratusan Hz; 105 percobaan VMD dijalankan dan 75 gagal | ledger R3-02, R3-29, R3-30 |")
w("| kNN-DTW | biaya 134,01 sampai 137.374,35 jam per klasifikasi penuh | ledger R3-40 |")
w("| EO dan Horse Herd | nol bukti domain fault diagnosis, getaran, pengeboran, atau PdM setelah pencarian khusus | R1 bagian 4.3 |")
w("| HBO (Heap-Based) | bukti diagnosis hanya tersedia dalam bentuk hibrida dengan GWO sehingga tidak bisa dipisahkan | R1 bagian 4.3 |")
w("| HHO | risiko implementasi tertinggi, tujuh fase, tanpa keunggulan yang bisa dibuktikan pada ruang 4 sampai 6 dimensi | R1 bagian 4.3 |")
w("| EPO dan SSA-Salp | hanya mendukung peran seleksi fitur, dan peran itu sudah ditempati BGWO dengan bukti lebih kuat | R1 bagian 4.3 |")
w("| SSA-Sparrow | bukti berpusat pada jaringan mendalam dan VMD, sedangkan VMD sudah ditolak | R1 bagian 4.3 |")
w("| Honey Badger | peran identik GWO dan WOA tanpa keunggulan terukur | R1 bagian 4.3 |")
w("| Autoencoder | dijalankan sebagai pembanding, hasilnya jenuh: recall 1,0 dengan 96 persen menit menyala | ledger R5-067 |")
w("| One-Class SVM | laju alarm 6,65 kali parameter, tidak layak dipakai menetapkan laju alarm | ledger R5-045 |")
w("| LOF | dijalankan sebagai pembanding, jenuh menyala seperti autoencoder | ledger R5-067 |")
w("| MCMC dan Bayesian network | prior dan DAG belum ada, sehingga model menjelaskan prior kita, bukan data | R2 bagian 10 |")
w("| RSF dan DeepHit | event per well kecil dan horizon hanya 10 menit | ledger L-28 |")
w("")
w("### 8.2 Ditunda (alasan keadaan, bisa berubah)")
w("")
w("| Algoritma | Alasan penundaan | Syarat pencairan |")
w("|---|---|---|")
w("| BOCPD | butuh baseline kontinu yang jauh lebih panjang dari yang tersedia | baseline kontigu memadai per well (R5 bagian 6) |")
w("| ADWIN | belum dijalankan sama sekali pada data kita | satu run pembanding pada tool_wear dengan laju alarm terukur |")
w("| Cox | relevan hanya untuk K-ii, dan survival tidak otomatis memperbaiki lead time | pra-registrasi TLead dan uji asumsi proportional hazards |")
w("| Markov chain dan HMM | median episode 1,0 menit membuat memori hampir nol; state fisik tidak ada | uji orde Markov dijalankan dan label state fisik tersedia |")
w("| Monte Carlo | perannya pelaporan selang, bukan menaikkan deteksi | dipakai bersama finalis, bukan sebagai finalis |")
w("")
w("### 8.3 Yang ditolak sebagai rujukan, bukan sebagai algoritma")
w("")
w("DOI `10.1214/18-AOS1801` yang lazim dipakai untuk conformalized quantile regression diperiksa pada "
  "run ini dan ternyata menunjuk Chen 2020 tentang inferensi parameter pada stochastic gradient descent, "
  "bukan Romano dan rekan. Karena itu DOI tersebut tidak dipakai. Yang dipakai untuk conformal adalah "
  "Vovk 2005 (DOI 10.1007/b106715, terverifikasi dua lapis) dan arXiv 1905.03222 yang judulnya cocok.")
w("")
w("---")
w("")
w("## 9. Yang belum terukur dan belum terverifikasi")
w("")
w("Daftar ini bagian dari hasil, bukan lampiran. Semua butir di bawah tidak dipakai sebagai dasar "
  "rekomendasi di bagian 6 dan 7.")
w("")
w("1. BELUM TERUKUR: biaya latih dan AUPRC LightGBM, XGBoost, CatBoost pada data kita. Run pembanding R4 "
  "tidak selesai dalam anggaran waktu (ledger E1-018).")
w("2. BELUM TERUKUR: jumlah sampel kalibrasi minimum yang memadai. Yang ada hanya ukuran himpunan "
  "(1.989 sampai 10.903 baris per well pada kelas vib, ledger R4-01), bukan hasil uji kelayakan.")
w("3. BELUM TERUKUR: tiga varian ambang conformal (V1 kuantil-hindsight, V2 lintas-well, V3 dalam-well "
  "prospektif) dan selisih FAR empiris terhadap alpha. Belum ada satu pun baris yang dieksekusi.")
w("4. BELUM TERUKUR: DeLong dan McNemar pada data nyata, karena skor per jendela dan hitungan berpasangan "
  "tidak disimpan.")
w("5. BELUM TERUKUR: manfaat matrix profile pada kanal VIBLAT. Biaya per query terukur, manfaatnya tidak.")
w("6. BELUM TERVERIFIKASI: teks penuh 10 dari 11 rujukan R5 tidak terbaca dari host ini karena blokir "
  "penerbit (403 dan 202). Rekaman Crossref cocok, isi tidak dibaca.")
w("7. BELUM TERVERIFIKASI: label bit_wear K-2. Pra-registrasinya belum terbit, sehingga status datanya "
  "SEBAGIAN dan finalis tidak dibangun di atasnya.")
w("8. BELUM TERVERIFIKASI: FAR bit_wear dalam satuan 24 jam, karena barisnya grid kedalaman 0,015 m "
  "(temuan E0 S-6). Angka FAR kelas ini tidak dipakai di dokumen ini.")
w("9. BELUM TERUKUR: kestabilan lintas seed. Seluruh run memakai SEED = 42.")
w("10. Penilaian skor komponen (tier, risiko, biaya) adalah KONVENSI, bukan pengukuran. Yang terukur "
  "hanya angka di kolom alasan.")
w("")
w("---")
w("")
w("## 10. Rujukan")
w("")
w("Semua DOI diperiksa pada 2026-10-27 dengan dua lapis: resolusi `https://doi.org/<doi>` tanpa mengikuti "
  "redirect, dan metadata `https://api.crossref.org/works/<doi>`. Berkas hasil: "
  "`scratch/rnd_e1/doi_check.json`, perintah `python3 scratch/rnd_e1/doi_check.py`.")
w("")
w("| # | Penulis pertama | Tahun | Judul | DOI atau URL | doi.org | Crossref | Dipakai untuk |")
w("|---|---|---|---|---|---|---|---|")
REF = [
 ("Vovk", 2005, "Algorithmic Learning in a Random World", "10.1007/b106715", 302, 200, "dasar conformal prediction (finalis 1)"),
 ("Niculescu-Mizil", 2005, "Predicting good probabilities with supervised learning", "10.1145/1102351.1102430", 302, 200, "dasar kalibrasi, bukan dasar angka"),
 ("Chen", 2016, "XGBoost: A Scalable Tree Boosting System", "10.1145/2939672.2939785", 302, 200, "keluarga boosting (finalis 3)"),
 ("Liu", 2008, "Isolation Forest", "10.1109/ICDM.2008.17", 302, 200, "detektor tanpa label pada kelas tanpa anotasi"),
 ("Page", 1954, "Continuous Inspection Schemes", "10.1093/biomet/41.1-2.100", 302, 200, "dasar CUSUM (finalis 2)"),
 ("DeLong", 1988, "Comparing the Areas under Two or More Correlated ROC Curves", "10.2307/2531595", 302, 200, "uji pembanding AUC, belum dapat dijalankan"),
 ("Teale", 1965, "The concept of specific energy in rock drilling", "10.1016/0148-9062(65)90022-7", 302, 200, "konteks kanal mekanis, bukan dasar skor"),
 ("Ke", 2017, "LightGBM: A Highly Efficient Gradient Boosting Decision Tree", "https://papers.nips.cc/paper_files/paper/2017/hash/6449f44a102fde848669bdd9eb6b76fa-Abstract.html", "URL", 200, "keluarga boosting (finalis 3)"),
 ("Romano", 2019, "Conformalized Quantile Regression", "https://arxiv.org/abs/1905.03222", "URL", 200, "varian conformal untuk regresi kuantil"),
 ("Prokhorenkova", 2017, "CatBoost: unbiased boosting with categorical features", "https://arxiv.org/abs/1706.09516", "URL", 200, "LOTO pada tool_wear"),
 ("Angelopoulos", 2021, "A Gentle Introduction to Conformal Prediction", "https://arxiv.org/abs/2107.07511", "URL", 200, "definisi cakupan conformal"),
]
for i, (a1, y, t, doi, l1, l2, use) in enumerate(REF, 1):
    w(f"| {i} | {a1} | {y} | {t} | {doi} | {l1} | {l2} | {use} |")
w("")
w("Catatan kejujuran atas tabel ini: tujuh rujukan pertama terverifikasi pada lapis registrasi (doi.org) "
  "dan lapis metadata (Crossref), masing-masing 302 dan 200. Empat rujukan terakhir adalah arXiv dan "
  "halaman prosiding, jadi tidak punya DOI; yang diverifikasi adalah URL terbuka dengan judul halaman yang "
  "cocok, bukan DOI. Isi penuh sebagian rujukan tidak dibaca karena blokir penerbit, dan itu tidak "
  "dipakai sebagai dasar angka.")
w("")
w("---")
w("")
w("## Ringkasan 5 baris")
w("")
w("1. Matriks {{N_ALG}} algoritma x 7 engine berisi 196 sel, dan {{N_GT2}} algoritma punya skor prioritas di "
  "atas 2,0 dari skala 3.")
w("2. Peringkat teratas bukan model yang lebih canggih, melainkan metode yang menyerang portabilitas "
  "ambang: conformal per well pada hyd dengan skor 2,85, disusul uji KS dan Page-Hinkley.")
w("3. Tiga finalis pilot adalah kalibrasi ambang prospektif (hyd), Page-Hinkley dan CUSUM dengan reset "
  "(tool_wear), serta boosting terkalibrasi (shk, ssi, stuck K-ii); ketiganya punya data ADA atau "
  "SEBAGIAN dan jalur gate C, A, B yang bisa ditunjuk.")
w("4. Sebanyak {{N_TOLAK}} algoritma atau keluarga algoritma ditolak permanen dengan alasan fisik atau biaya, "
  "{{N_TUNDA}} ditunda karena keadaan, dan satu DOI conformal populer ditolak karena menunjuk makalah lain.")
w("5. Yang paling menghambat bukan pilihan algoritma: FAR belum dilaporkan sebagai laju kalender (temuan "
  "E0 K-4) dan skor per jendela tidak disimpan, sehingga DeLong dan McNemar belum bisa dijalankan.")
w("")
w("### Daftar yang belum terverifikasi")
w("")
w("- Biaya latih dan AUPRC LightGBM, XGBoost, CatBoost pada data kita.")
w("- Jumlah sampel kalibrasi minimum yang memadai.")
w("- FAR empiris tiga varian conformal.")
w("- DeLong dan McNemar pada data nyata.")
w("- Manfaat matrix profile pada kanal VIBLAT.")
w("- Teks penuh 10 dari 11 rujukan R5 (blokir penerbit).")
w("- Label bit_wear K-2 (pra-registrasi belum terbit).")
w("- FAR bit_wear dalam satuan 24 jam.")
w("- Kestabilan lintas seed selain 42.")
w("")

doc = "\n".join(L)

# hitung jumlah baris nyata tiap tabel keputusan, lalu subsitusi placeholder
def rows_of(sec_start, sec_end):
    txt = doc.split(sec_start)[1].split(sec_end)[0]
    return [ln for ln in txt.splitlines() if ln.startswith("| ") and not ln.startswith("| Algoritma |")]

n_tolak = len(rows_of("### 8.1 Ditolak permanen", "### 8.2 Ditunda"))
n_tunda = len(rows_of("### 8.2 Ditunda", "### 8.3 Yang ditolak sebagai rujukan"))
n_gt2 = sum(1 for r in D["peringkat_algoritma"] if r["skor_prioritas"] > 2.0)
n_alg = len(D["matriks"])
assert n_tolak > 0 and n_tunda > 0, (n_tolak, n_tunda)
doc = (doc.replace("{{N_TOLAK}}", str(n_tolak))
          .replace("{{N_TUNDA}}", str(n_tunda))
          .replace("{{N_GT2}}", str(n_gt2))
          .replace("{{N_ALG}}", str(n_alg)))
assert "{{" not in doc, "placeholder tersisa"
open(DOC, "w", encoding="utf-8").write(doc)
print("wrote", DOC, len(doc), "chars", doc.count("\n") + 1, "lines")

# ---------------------------------------------------------------------------
# Ledger bagian E1 (idempoten: hapus blok lama, tulis ulang, assert dulu)
# ---------------------------------------------------------------------------
BOBOT = D["meta"]["bobot"]
assert abs(BOBOT["tier"] - 0.50) < 1e-9 and abs(BOBOT["data"] - 0.25) < 1e-9
assert abs(BOBOT["risiko"] - 0.15) < 1e-9 and abs(BOBOT["biaya"] - 0.10) < 1e-9
assert abs(sum(BOBOT.values()) - 1.0) < 1e-12

per = {r["algoritma"]: r for r in D["peringkat_algoritma"]}
def cek(kode, eng, harap):
    r = per[kode]
    assert r["engine"] == eng, (kode, "engine", r["engine"], eng)
    k = r["komponen"]
    hit = (BOBOT["tier"]*k["tier"] + BOBOT["data"]*k["data"]
           + BOBOT["risiko"]*k["risiko"] + BOBOT["biaya"]*k["biaya"])
    assert abs(hit - r["skor_prioritas"]) < 5e-5, (kode, hit, r["skor_prioritas"])
    assert abs(hit - harap) < 5e-5, (kode, "harapan", harap, hit)
    return k, r["skor_prioritas"]

k10, s10 = cek("A10", "hyd", 2.85)
k16, s16 = cek("A16", "tool_wear", 2.35)
k06, s06 = cek("A06", "shk", 2.15)
assert len(D["pasangan"]) == 196
assert len(D["matriks"]) == 28
assert max(r["skor_prioritas"] for r in D["pasangan"] if r["algoritma"] == "A14") == 0.0, \
    "gerbang tier=0 harus memaksa Monte Carlo ke 0"

def f2(x): return f"{x:.2f}".replace(".", ",")

rows = []
def R(no, angka, satuan, kelas, rujuk, dipakai, status):
    rows.append(f"| {no} | {angka} | {satuan} | {kelas} | {rujuk} | {TANGGAL} | {dipakai} | {status} |")

# --- verifikasi angka yang dikutip di bagian 7 tetapi belum punya baris ledger sendiri ---
# Tiap butir di-assert ada di dokumen sumbernya sebelum baris ledger ditulis.
_baca = lambda rel: open(os.path.join(BASE, rel), encoding="utf-8").read()
_evc = _baca("docs/V9_EVAL_C_LAYERC.md")
_r6 = _baca("docs/RND_R6_METRIK.md")
_e0 = _baca("docs/RND_E0_AUDIT_ENGINE.md")
_r5 = _baca("docs/RND_R5_DRIFT.md")
SRC = [
    ("E1-021", "14,6 sampai 58,4", "FAR per 24 jam, hybrid hyd K-i", _evc, "14,6\u201358,4",
     "docs/V9_EVAL_C_LAYERC.md bagian 1 baris hyd K-i", "bagian 7.1"),
    ("E1-022", "0,50", "presisi run tool_wear", _evc, "precision run 0,50",
     "docs/V9_EVAL_C_LAYERC.md bagian 1 baris tool_wear K-i", "bagian 7.2"),
    ("E1-023", "1,8", "rasio TLead tool_wear", _evc, "TLead 1,8",
     "docs/V9_EVAL_C_LAYERC.md bagian 1 baris tool_wear K-i", "bagian 7.2"),
    ("E1-024", "0,775", "daya uji tanda 9 well", _r6, "0,775",
     "docs/RND_R6_METRIK.md bagian 3.1", "bagian 7.1, 7.3"),
    ("E1-025", "1,46 sampai 71,7", "cakupan waktu teramati per well (persen)", _e0, "1,46% sampai 71,7",
     "docs/RND_E0_AUDIT_ENGINE.md temuan Kritis K-4", "bagian 7, 9"),
    ("E1-026", "6,65", "rasio laju alarm One-Class SVM terhadap parameter nu", _r5, "6,65",
     "docs/RND_R5_DRIFT.md bagian 5 tabel skor (baris One-Class SVM)", "bagian 3.5 A23"),
]
for _no, _ang, _sat, _doc, _needle, _src, _dipakai in SRC:
    assert _needle in _doc, (_no, _needle, "tidak ditemukan di sumber")
    R(_no, _ang, _sat, "RUN-KITA", _src, _dipakai, "TERUKUR (kutipan diverifikasi ada di sumber)")


R("E1-001", "0,50", "bobot", "KONVENSI", "keputusan dokumen ini; diturunkan dari `docs/RND_ALGO_RESEARCH_PLAN.md` bagian 6 (tier hanya naik bila C, A, B terpenuhi bersamaan)", "bagian 5.1", "TERVERIFIKASI sebagai aritmetik (jumlah bobot 1,000)")
R("E1-002", "0,25", "bobot", "KONVENSI", "keputusan dokumen ini; alasan di `docs/RND_D0_DATA_FEASIBILITY.md` bagian 2 tentang blokir laju sampel", "bagian 5.1", "TERVERIFIKASI sebagai aritmetik")
R("E1-003", "0,15", "bobot", "KONVENSI", "keputusan dokumen ini; alasan di `docs/RND_E0_AUDIT_ENGINE.md` bagian 6 (5 temuan Kritis)", "bagian 5.1", "TERVERIFIKASI sebagai aritmetik")
R("E1-004", "0,10", "bobot", "KONVENSI", "keputusan dokumen ini; biaya ekstrem sudah tertangkap di sel (ledger R3-40)", "bagian 5.1", "TERVERIFIKASI sebagai aritmetik")
R("E1-005", "0,50*tier + 0,25*data + 0,15*risiko + 0,10*biaya", "rumus skor 0-3", "DERIVASI", "`scratch/rnd_e1/e1_build.py` fungsi `skor_prioritas`, dengan gerbang skor 0 bila tier 0", "bagian 5.1, 5.2", "TERVERIFIKASI (rumus dijalankan skrip, hasil di `e1_scores.json`)")
R("E1-006", "0 sampai 3", "rubrik", "KONVENSI", "rubrik kesesuaian sel di `docs/RND_E1_MATRIKS.md` bagian 1.1", "bagian 1.1, 2, 3", "BELUM (definisi dokumen, bukan temuan)")
R("E1-007", "3 / 1 / 0", "skor data", "KONVENSI", "pemetaan ADA ke 3, SEBAGIAN ke 1, TIDAK ke 0 di `e1_build.py` `DATA_SCORE`", "bagian 5.1", "BELUM (keputusan dokumen)")
R("E1-008", "196", "sel", "DERIVASI", "28 algoritma x 7 engine; assert `len(D['pasangan']) == 196` di `e1_doc.py`", "bagian 0, 2", "TERVERIFIKASI (assert lolos)")
R("E1-009", "28", "algoritma", "DERIVASI", "`len(D['matriks']) == 28`; daftar di `docs/RND_E1_MATRIKS.md` bagian 2", "bagian 0, 2", "TERVERIFIKASI (assert lolos)")
R("E1-010", "6", "pikiran", "RUN-KITA", "`mcp__sequentialthinking__sequentialthinking` thoughtNumber 1..6, thoughtHistoryLength 6", "bagian Riset pendahuluan", "TERUKUR")
R("E1-011", f2(s10), "skor prioritas", "DERIVASI", f"A10 conformal pada hyd: 0,50*{k10['tier']} + 0,25*{k10['data']} + 0,15*{k10['risiko']} + 0,10*{k10['biaya']} = {f2(s10)}", "bagian 5.2, 6, 7.1", "TERVERIFIKASI (assert aritmetik)")
R("E1-012", f2(s16), "skor prioritas", "DERIVASI", f"A16 Page-Hinkley pada tool_wear: 0,50*{k16['tier']} + 0,25*{k16['data']} + 0,15*{k16['risiko']} + 0,10*{k16['biaya']} = {f2(s16)}", "bagian 5.2, 6, 7.2", "TERVERIFIKASI (assert aritmetik)")
R("E1-013", f2(s06), "skor prioritas", "DERIVASI", f"A06 LightGBM atau XGBoost pada shk: 0,50*{k06['tier']} + 0,25*{k06['data']} + 0,15*{k06['risiko']} + 0,10*{k06['biaya']} = {f2(s06)}", "bagian 5.2, 6, 7.3", "TERVERIFIKASI (assert aritmetik)")
R("E1-014", "0,00", "skor prioritas Monte Carlo", "DERIVASI", "gerbang tier=0 memaksa A14 ke 0; assert atas D['pasangan'] untuk A14 di `e1_doc.py`", "bagian 5.1", "TERVERIFIKASI (assert lolos)")
R("E1-015", str(n_gt2), "algoritma", "DERIVASI", "hitung dari `e1_scores.json` peringkat_algoritma dengan ambang skor > 2,0", "bagian 0", "TERVERIFIKASI (hitung ulang di `e1_doc.py`)")
R("E1-016", f"{n_tolak} / {n_tunda}", "algoritma ditolak / ditunda", "KONVENSI", "hitungan baris tabel `docs/RND_E1_MATRIKS.md` bagian 8.1 dan 8.2, dihitung ulang oleh `rows_of()` di `e1_doc.py`", "bagian 0, 8", "TERVERIFIKASI (hitung baris tabel)")
R("E1-017", "10.1214/18-AOS1801", "DOI", "JURNAL", "Crossref 200 mengembalikan Chen 2020 tentang inferensi SGD, bukan Romano 2019; lihat `scratch/rnd_e1/doi_check.json`", "bagian 8.3, 10", "DITOLAK (tidak dipakai)")
R("E1-018", "BELUM TERUKUR", "detik biaya latih", "BELUM-TERUKUR", "run pembanding R4 tidak selesai; sebelum diberi angka, tidak ada nilai yang boleh ditulis", "bagian 5.1 butir 2, 9 butir 1", "BELUM")
R("E1-019", "302 / 200", "status HTTP", "RUN-KITA", "tujuh DOI di `scratch/rnd_e1/doi_check.py`: doi.org 302 tanpa mengikuti redirect, Crossref 200 dengan penulis dan tahun cocok", "bagian 10", "TERUKUR")
R("E1-020", "200", "status HTTP", "RUN-KITA", "empat URL arXiv dan prosiding di `scratch/rnd_e1/` diperiksa dengan `curl -L`, judul halaman cocok", "bagian 10", "TERUKUR")

ledger_new = []
ledger_new.append("")
rows.sort(key=lambda r: int(r.split("|")[1].strip().split("-")[1]))
ledger_new.append("---")
ledger_new.append("")
ledger_new.append("## Bagian E1: matriks kelayakan algoritma x engine dan shortlist (kartu `t_9abcb3b3`)")
ledger_new.append("")
ledger_new.append("Dokumen pendamping: `docs/RND_E1_MATRIKS.md`. Sumber angka: `scratch/rnd_e1/e1_scores.json` "
                  "(dibuat " + D["meta"]["dibuat"] + " oleh `scratch/rnd_e1/e1_build.py`), "
                  "`scratch/rnd_e1/doi_check.json`, dan baris ledger R1, R3, R4, R5, D0 yang dirujuk ulang.")
ledger_new.append("")
ledger_new.append("Baris E1 tidak menduplikasi angka hasil ukur yang sudah punya baris sendiri. Yang ditulis "
                  "di sini adalah bobot, rubrik, rumus, hasil derivasi skor, dan status verifikasi baru.")
ledger_new.append("")
ledger_new.append("| No | Angka | Satuan | Kelas sumber | Rujukan persis | Tanggal akses | Dipakai di | Status |")
ledger_new.append("|---|---|---|---|---|---|---|---|")
ledger_new.extend(rows)
ledger_new.append("")
ledger_new.append(f"Rekap kelas: 7 KONVENSI (E1-001..E1-004, E1-006, E1-007, E1-016), 8 DERIVASI (E1-005, E1-008, "
                  f"E1-009, E1-011..E1-015), 9 RUN-KITA (E1-010, E1-019, E1-020, E1-021..E1-026), "
                  f"1 JURNAL ditolak (E1-017), 1 BELUM (E1-018).")
ledger_new.append("")
ledger_new.append("Catatan koreksi yang ditemukan pada run ini: DOI `10.1214/18-AOS1801` tidak menunjuk "
                  "Romano 2019 (conformalized quantile regression) melainkan Chen 2020. DOI itu dibuang, "
                  "dan conformal disandarkan pada Vovk 2005 serta arXiv 1905.03222.")
ledger_new.append("")

txt = open(LEDGER, encoding="utf-8").read()
marker = "## Bagian E1: matriks kelayakan algoritma x engine dan shortlist"
if marker in txt:
    head = txt.split("---\n\n" + marker)[0]
    txt = head.rstrip() + "\n"
open(LEDGER, "w", encoding="utf-8").write(txt + "\n".join(ledger_new) + "\n")
print("ledger rows:", len(rows), "| ledger bytes:", len(txt) + len("\n".join(ledger_new)))
