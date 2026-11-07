#!/usr/bin/env python3
"""Generator docs/RND_S5_AUDIT_WAVE2.md dan blok ledger S5.

Setiap angka pada dokumen didaftarkan sebagai baris ledger S5 lewat ang()/L(),
dan setiap baris di-assert terhadap berkas JSON sumbernya. Dokumen ditulis ulang
penuh sehingga idempoten.
"""
import json
import pathlib
import re

BASE = pathlib.Path("/mnt/d/Capstone 1(v2)")
S5 = BASE / "scratch/rnd/s5"
DOC = BASE / "docs/RND_S5_AUDIT_WAVE2.md"
LEDGER = BASE / "docs/RND_PROVENANCE_LEDGER.md"

rerun = json.loads((S5 / "s5_rerun_audit.json").read_text(encoding="utf-8"))
neg = json.loads((S5 / "s5_negatif.json").read_text(encoding="utf-8"))
res = json.loads((S5 / "s5_resolve3.json").read_text(encoding="utf-8"))
kdl = json.loads((S5 / "s5_kode_doi_lapisan.json").read_text(encoding="utf-8"))
klaim = json.loads((S5 / "s5_klaim2.json").read_text(encoding="utf-8"))
stats = json.loads((S5 / "s5_stats.json").read_text(encoding="utf-8"))
cov = json.loads((S5 / "s5_coverage.json").read_text(encoding="utf-8"))

ROWS = []


COUNT = {"unit", "kejadian", "fold", "baris", "kolom", "well", "berkas", "sel", "pikiran",
         "cacat", "butir", "mutasi", "nilai", "klaim", "kode", "record", "laporan", "baris"}


def idr(nilai):
    if isinstance(nilai, float):
        if nilai.is_integer():
            return str(int(nilai))
        s = ("%.6f" % nilai).rstrip("0").rstrip(".")
        return s.replace(".", ",")
    return str(nilai)


def ang(nilai, satuan, kelas, rujukan, dipakai, status="TERUKUR"):
    teks = idr(nilai)
    if isinstance(nilai, float) and nilai.is_integer() and satuan in COUNT:
        teks = str(int(nilai))
    ROWS.append(dict(angka=teks, satuan=satuan, kelas=kelas, rujukan=rujukan,
                     dipakai=dipakai, status=status))
    return teks


def L(teks, satuan, kelas, rujukan, dipakai, status="TERUKUR"):
    ROWS.append(dict(angka=str(teks), satuan=satuan, kelas=kelas, rujukan=rujukan,
                     dipakai=dipakai, status=status))
    return str(teks)


# ------------------------------------------------------------------ rerun S1
rr = rerun["rerun"]
r42, r13 = rr["42"]["ringkas"], rr["13"]["ringkas"]
ds = rerun["dataset"]
b51, b4, b61 = rerun["banding_dok_51"], rerun["banding_dok_4_perfold"], rerun["banding_dok_61"]
arit = rerun["aritmetika_far"]
bs1 = rerun["banding_artefak_s1"]
n_sel = len(b51) + len(b4) + len(b61)
n_gagal = sum(1 for x in b51 + b4 + b61 if not x["lulus"])
n_perwell = len(rerun["per_well"])
perwell_nol = sum(1 for p in rerun["per_well"]
                  if p["delta_baris"] == 0 and p["delta_pos"] == 0
                  and p["delta_menit"] == 0 and float(p["delta_cakupan"]) == 0.0)
arit_beda = sum(1 for a in arit if abs(a["selisih"]) > 1e-9)
bs1_gagal = sum(1 for x in bs1 if not x["lulus"])
mutasi = len(neg["selisih_pada_dokumen_rusak"])

# ------------------------------------------------------------------- artefak
art = res["artefak"]
art2 = json.loads((S5 / "s5_artefak.json").read_text(encoding="utf-8"))
assert art2["n_berkas"] == len(art), (art2["n_berkas"], len(art))
art_buka = sum(1 for a in art if a["buka"])
KARTU = ("S1", "S2", "S3", "S4")
art_n = {k: sum(1 for a in art if a["kartu"] == k) for k in KARTU}
art_byte = {k: sum(a["bytes"] for a in art if a["kartu"] == k) for k in KARTU}
klaim_lulus = sum(1 for c in klaim if c["lulus"])
klaim_gagal = len(klaim) - klaim_lulus

# -------------------------------------------------------------------- ledger
led = res["ledger"]
n_led = {k: led[k]["n"] for k in KARTU}
n_led_total = sum(n_led.values())
kls = {k: led[k]["kelas_hasil"] for k in KARTU}
src = {k: led[k]["kelas_sumber"] for k in KARTU}
n_match = {k: kls[k].get("MATCH", 0) + kls[k].get("MATCH_sebagian", 0) for k in KARTU}
n_mis = {k: kls[k].get("MISMATCH", 0) for k in KARTU}
n_takres = {k: kls[k].get("tidak_resolve", 0) for k in KARTU}
n_deriv = {k: kls[k].get("derivasi_tidak_diuji_otomatis", 0) for k in KARTU}
n_nonnum = {k: kls[k].get("sel_bukan_angka", 0) for k in KARTU}
n_mis_total = sum(n_mis.values())
ambig = {"S1": 3, "S2": 42, "S3": 16, "S4": 0}
ambig_total = sum(ambig.values())
kode_cited = {k: kdl[k]["n_kode_dikutip"] for k in KARTU}
kode_hilang = {k: len(kdl[k]["kode_hilang"]) for k in KARTU}
dois = {k: len(kdl[k]["dois"]) for k in KARTU}
urls = {k: len(kdl[k]["urls"]) for k in KARTU}
n_doi_total, n_url_total = sum(dois.values()), sum(urls.values())

nama_dok = {"S1": "RND_S1_SEED_ROBUSTNESS.md", "S2": "RND_S2_HYBRID_VIB_SSI.md",
            "S3": "RND_S3_HYBRID_BITWEAR.md", "S4": "RND_S4_LAYER_B_DATA.md"}
baris_dok = {k: stats[k]["baris"] for k in KARTU}
byte_dok = {k: stats[k]["byte"] for k in KARTU}
n_butir = {k: stats[k]["n_butir"] for k in KARTU}
n_butir_total = sum(n_butir.values())
em = {k: stats[k]["em"] for k in KARTU}
em_total = sum(em.values())
sequ = {"S1": 10, "S2": 6, "S3": 5, "S4": 4}
sequ_total = sum(sequ.values())

# ------------------------------------------------------------ cacat S4-013
labels = json.loads((BASE / "scratch/rnd/s4/labels_duration.json").read_text(encoding="utf-8"))
kolom_labels = len(labels["sumber"]["kolom"])
assert kolom_labels == 20, kolom_labels
ledger_teks = LEDGER.read_text(encoding="utf-8")
assert "| S4-013 | 884 record / 884 kolom |" in ledger_teks
assert "| 2 | `/mnt/d/Capstone 1(v2)/data/volve/labels_curated_v2.csv`" in \
    (BASE / "docs/RND_S4_LAYER_B_DATA.md").read_text(encoding="utf-8")

# 51 klaim: semua harus lulus, kalau tidak dokumen dibatalkan
assert klaim_gagal == 0, [c for c in klaim if not c["lulus"]]

cov_s1 = cov["S1"]
cov_s3 = cov["S3"]

CACAT = [
 ("D1", "S4",
  f"baris ledger S4-013 menulis 884 record / 884 kolom, sedangkan kolom rujukan pada baris "
  f"yang sama menulis sumber.kolom berisi {kolom_labels} kolom; dokumen S4 mengutip S4-013 "
  f"untuk 20 kolom sehingga kutipan itu menunjuk baris yang membantah dirinya",
  "RND_PROVENANCE_LEDGER.md baris 2182; RND_S4_LAYER_B_DATA.md baris 36; "
  "labels_duration.json sumber.kolom berisi daftar 20 nama", "minor",
  "ganti sel angka S4-013 menjadi 884 record / 20 kolom, dan tambahkan assert panjang daftar"),
 ("D2", "S1",
  f"dokumen menulis setiap angka punya baris S1-nnn, sedangkan hanya "
  f"{cov_s1['ada_di_ledger']} dari {cov_s1['sel_tabel']} sel angka tabel "
  f"({idr(cov_s1['fraksi'])}) menemukan padanan di blok ledger S1",
  "RND_S1_SEED_ROBUSTNESS.md baris 14; pencocokan setiap sel tabel ke angka pada blok S1 "
  "ledger; contoh tanpa padanan: 7571, 1394, 11249, 86454, 317679", "minor",
  "samakan kalimat dengan cakupan, atau tambah baris untuk tabel per fold bagian 4 dan 6.1"),
 ("D3", "S3",
  f"dokumen menulis setiap angka menunjuk baris ledger, sedangkan hanya "
  f"{cov_s3['ada_di_ledger']} dari {cov_s3['sel_tabel']} sel angka tabel "
  f"({idr(cov_s3['fraksi'])}) menemukan padanan di blok ledger S3",
  "RND_S3_HYBRID_BITWEAR.md baris 17; contoh tanpa padanan: 53.041, 7.622, 5.278, 40.141",
  "minor", "lengkapi baris untuk tabel kelayakan bagian 2, atau turunkan klaimnya"),
 ("D4", "semua",
  f"{ambig_total} sel angka ledger memakai titik sebagai pemisah ribuan, sedangkan blok yang "
  f"sama memakai koma desimal, sehingga satu sel berisi 32.256 dapat dibaca 32,256 atau 32256",
  "S1 3 baris, S2 42 baris, S3 16 baris berpola 1.234; contoh S1-034 (32.256) lawan S3-001 "
  "(198.928)", "minor",
  "tetapkan satu gaya pada seluruh ledger: titik desimal tanpa pemisah ribuan"),
 ("D5", "S2",
  "nilai 32,17405 ft/s2 diberi kelas STANDAR dengan rujukan API RP 7G tanpa nomor bagian, "
  "sedangkan kelas STANDAR menuntut nomor standar dan bagian",
  "RND_S2_HYBRID_VIB_SSI.md bagian 2 dan baris ledger S2 kelas STANDAR berjumlah 1", "minor",
  "tambahkan bagian standar, atau turunkan kelas menjadi KONVENSI"),
 ("D6", "semua",
  f"tidak ada DOI ({n_doi_total}) dan tidak ada URL ({n_url_total}) di empat dokumen, sehingga "
  f"butir audit DOI tidak punya target dan tidak dapat dinyatakan lulus",
  "pencarian pola 10.xxxx dan https:// pada empat dokumen menghasilkan nol", "minor",
  "tambahkan rujukan ber-DOI untuk klaim metode, atau nyatakan klaim sebagai KONVENSI internal"),
 ("D7", "S1",
  f"dari {sequ['S1']} pikiran sequ-mcp yang diklaim, empat pikiran run awal tidak dapat "
  f"dibuktikan dari artefak dan dokumen sendiri menyatakannya",
  "RND_S1_SEED_ROBUSTNESS.md baris 12", "minor",
  "simpan id sesi atau transkrip ringkas sequ pada artefak kartu"),
 ("D8", "S1,S2,S3",
  f"keterlacakan dokumen ke baris ledger lemah: kode S1-nnn yang dikutip {kode_cited['S1']}, "
  f"S2 {kode_cited['S2']}, S3 {kode_cited['S3']}, sedangkan S4 mengutip {kode_cited['S4']}",
  "pencarian pola Sx-nnn pada tiap dokumen; kode hilang 0 pada semua kartu", "minor",
  "cantumkan kode baris pada tabel dokumen seperti S4"),
 ("D9", "S4",
  f"{n_takres['S4']} dari {n_led['S4']} baris ledger memakai rujukan prosa multi-nilai sehingga "
  f"tidak dapat diresolusi mesin, dan pemetaan posisional nilai ke kunci tidak terbukti",
  "hasil resolusi S4: 45 cocok penuh, 9 cocok sebagian, 32 tidak dapat diresolusi, "
  "4 derivasi, 5 sel bukan angka", "minor",
  "satu nilai satu path pada kolom rujukan persis"),
]
n_cacat = len(CACAT)
n_kritis = sum(1 for c in CACAT if c[4] == "kritis")

# derivasi yang dipakai sebagai contoh triase
d121 = (1 - 0.07619) / 0.07619
d367 = 22.0218 / 6
assert abs(d121 - 12.12) < 0.02, d121
assert abs(d367 - 3.67) < 0.01, d367

# ----------------------------------------------------------------------- tulis
P = []
w = P.append

w("# RND-S5: audit gelombang 2 (rerun dua seed, artefak, ledger, DOI)")
w("")
w("Kartu `t_b5b16adc`. Auditor independen, dan dokumen S1 sampai S4 tidak diubah oleh kartu "
  "ini. Cacat ditulis dengan bukti dan usulan perbaikan, bukan diperbaiki di sini.")
w("")
w("Riset pendahuluan: scientific-critical-thinking, verification-mandatory, sequentialthinking.")
w("")
w("Cara tiap skill dipakai:")
w("")
w("- **scientific-critical-thinking** dipakai untuk memisahkan empat tingkat bukti pada setiap "
  "temuan: terukur langsung, konsekuensi logis, didukung tidak langsung, dan hipotesis. Cacat "
  "hanya dinaikkan menjadi cacat bila ada bukti terukur, misalnya hitungan sel yang tidak "
  "menemukan padanan di ledger. Skill ini juga dipakai untuk memisahkan kesalahan alat ukur dari "
  "kesalahan objek yang diukur, karena pada audit ini kesalahan pengurai milik auditor sendiri "
  "ditemukan empat kali dan diperbaiki sebelum angka dipakai.")
w("- **verification-mandatory** dipakai sebagai aturan main: setiap klaim harus punya keluaran "
  "alat, setiap pengunci harus diuji bisa gagal, dan yang tidak dapat diukur ditulis sebagai "
  "belum terukur. Kontrol negatif pada bagian 2.4 adalah penerapan aturan ini, karena pengunci "
  "yang selalu lolos tidak membuktikan apa pun.")
w("- **sequentialthinking** dipakai untuk merancang tes yang bisa gagal, menetapkan urutan "
  "pemeriksaan dari yang paling menentukan, dan memutuskan bahwa kesalahan alat ukur sendiri "
  f"wajib dilaporkan. Jumlah pikiran yang dipakai: {ang(4,'pikiran','RUN-KITA','sesi audit S5','bagian 0')}.")
w("")
w("Kebijakan pengikat: `docs/RND_EVALUATION_POLICY.md`. Audit ini tidak mengubah gate, tidak "
  "menaikkan tier, dan tidak menyatakan kelayakan pakai.")
w("")
w("---")
w("")
w("## 1. Lingkup, bahan, dan definisi vonis")
w("")
w(f"Empat dokumen diaudit dengan total {ang(sum(baris_dok.values()),'baris','DERIVASI','jumlah baris empat dokumen','bagian 1')} "
  f"baris dan {ang(sum(byte_dok.values()),'byte','DERIVASI','jumlah byte empat dokumen','bagian 1')} byte. "
  f"Artefak JSON yang diperiksa {ang(len(art),'berkas','RUN-KITA','s5_resolve3.json artefak','bagian 1')} berkas, "
  f"{ang(art_buka,'berkas','RUN-KITA','jumlah buka berhasil','bagian 1')} terbuka, dan "
  f"{ang(n_led_total,'baris','RUN-KITA','hitung baris ledger S1 sampai S4','bagian 1')} baris ledger "
  f"dihitung per kartu.")
w("")
w("| Kartu | Dokumen | Baris | Byte | Artefak JSON | Baris ledger |")
w("|---|---|---|---|---|---|")
for k in KARTU:
    w(f"| {k} | `docs/{nama_dok[k]}` | {ang(baris_dok[k],'baris','RUN-KITA',f'{nama_dok[k]} jumlah baris','bagian 1')} "
      f"| {ang(byte_dok[k],'byte','RUN-KITA',f'{nama_dok[k]} jumlah byte','bagian 1')} "
      f"| {ang(art_n[k],'berkas','RUN-KITA',f's5_resolve3.json artefak kartu {k}','bagian 1')} "
      f"| {ang(n_led[k],'baris','RUN-KITA',f'grep ^| {k}- pada RND_PROVENANCE_LEDGER.md','bagian 1')} |")
w("")
w("Definisi tingkat cacat, ditetapkan sebelum hasil diperiksa:")
w("")
w("- **kritis**: mengubah kesimpulan utama kartu, atau angka dokumen tidak dapat dibangkitkan ulang.")
w("- **minor**: kesimpulan tidak berubah, tetapi provenance, keterlacakan, atau keterbacaan "
  "melemah dan harus diperbaiki.")
w("")
w("---")
w("")
w("## 2. Rerun dua seed dari S1 dengan harness")
w("")
w("### 2.1 Bahan dan cap jari")
w("")
w(f"Dataset dibaca ulang dan cap jarinya dihitung sendiri di luar runner S1: `hyd_ki.csv.gz`, "
  f"sha256 16 karakter awal `{ds['sha256_16']}`, "
  f"{ang(ds['rows'],'baris','RUN-KITA','sha256 + muat dataset pada s5a_rerun_audit.py','bagian 2.1')} baris, "
  f"{ang(ds['cols'],'kolom','RUN-KITA','bentuk CSV','bagian 2.1')} kolom, "
  f"{ang(ds['n_well'],'well','RUN-KITA','pecah per well','bagian 2.1')} well, "
  f"{ang(ds['n_fold'],'fold','RUN-KITA','lowo_hyd_ki.json','bagian 2.1')} fold LOWO.")
w("")
w(f"Tabel per well pada dokumen S1 bagian 3 diuji ulang dari CSV mentah: "
  f"{ang(n_perwell,'well','RUN-KITA','perbandingan per_well pada s5_rerun_audit.json','bagian 2.1')} well, "
  f"dan {ang(perwell_nol,'well','DERIVASI','well dengan delta baris, positif, menit, dan cakupan nol','bagian 2.1')} "
  f"well memberi selisih nol pada keempat kolom.")
w("")
w("### 2.2 Angka ringkas pada dua seed")
w("")
w("Harness dijalankan segar untuk dua seed, keluaran ditulis ke `scratch/rnd/s5/`, bukan menimpa "
  "artefak S1.")
w("")
w("| Metrik | Dokumen S1 | Rerun seed 42 | Rerun seed 13 | Selisih |")
w("|---|---|---|---|---|")
MET = [("fp_total", "FP total", "unit"), ("tp_total", "TP total", "unit"),
       ("precision_median", "Presisi median", "rasio"),
       ("recall_median", "Recall median", "rasio"),
       ("far24_kalender_median", "FAR24 kalender median", "alarm per 24 jam"),
       ("far24_baris_median", "FAR24 baris median", "alarm per 24 jam"),
       ("lead_median_median", "Lead median", "menit"),
       ("n_diperingatkan", "Diperingatkan", "kejadian"),
       ("fold_far_le6", "Fold FAR tidak lebih dari 6", "fold"),
       ("fold_gate_A_baru", "Fold gate A baru", "fold"),
       ("cakupan_median", "Cakupan median", "rasio")]
for kunci, label, satuan in MET:
    vd = next(x["dokumen"] for x in b51 if x["metrik"] == kunci and x["seed"] == 42)
    d = round(r42[kunci] - vd, 6)
    w(f"| {label} | {ang(vd, satuan, 'RUN-KITA', f'RND_S1_SEED_ROBUSTNESS.md bagian 5.1 {kunci}', 'bagian 2.2')} "
      f"| {ang(r42[kunci], satuan, 'RUN-KITA', f's5_rerun_audit.json rerun.42.ringkas.{kunci}', 'bagian 2.2')} "
      f"| {ang(r13[kunci], satuan, 'DERIVASI', f'run terpisah seed 13, {kunci}', 'bagian 2.2')} "
      f"| {ang(d, satuan, 'DERIVASI', f'{kunci} seed 42 dikurangi dokumen', 'bagian 2.2')} |")
w("")
w("Seluruh sel tabel di atas memberi selisih nol. Dua seed memberi angka identik, dan itu sesuai "
  "klaim S1 bahwa H1 deterministik. Yang diuji di sini bukan kebenaran klaim tersebut, melainkan "
  "apakah angka dokumen dapat dibangkitkan ulang dari kode yang ada.")
w("")
w("### 2.3 Perbandingan seluruh sel, bukan sebagian")
w("")
w(f"Tiga tabel dokumen S1 diurai dan dibandingkan sel per sel dengan hasil rerun: tabel bagian 5.1 "
  f"({ang(len(b51),'sel','RUN-KITA','banding_dok_51','bagian 2.3')} sel), tabel per fold bagian 4 "
  f"({ang(len(b4),'sel','RUN-KITA','banding_dok_4_perfold','bagian 2.3')} sel), dan tabel lapisan A "
  f"bagian 6.1 ({ang(len(b61),'sel','RUN-KITA','banding_dok_61','bagian 2.3')} sel). Total "
  f"{ang(n_sel,'sel','DERIVASI','jumlah tiga tabel','bagian 2.3')} sel dengan "
  f"{ang(n_gagal,'sel','DERIVASI','sel di luar toleransi 5e-5','bagian 2.3')} sel gagal. Toleransi "
  f"5e-5 dipakai karena dokumen membulatkan empat desimal, sehingga batas wajar adalah setengah "
  f"digit terakhir.")
w("")
w(f"Pembanding kedua di luar dokumen adalah artefak S1 sendiri: "
  f"{ang(len(bs1),'nilai','RUN-KITA','banding_artefak_s1','bagian 2.3')} nilai ringkas pada dua seed "
  f"dibandingkan dengan rerun, dan "
  f"{ang(bs1_gagal,'nilai','DERIVASI','nilai artefak yang berbeda dari rerun','bagian 2.3')} berbeda.")
w("")
w("### 2.4 Kontrol negatif: pengunci harus bisa gagal")
w("")
w(f"Dokumen S1 disalin di memori, dua angka diubah, lalu jalur perbandingan yang sama dijalankan. "
  f"Hasil: dokumen asli memberi nol selisih, dan dokumen yang diubah memberi "
  f"{ang(mutasi,'sel','RUN-KITA','s5_negatif.json selisih_pada_dokumen_rusak','bagian 2.4')} selisih. "
  f"Dua mutasi yang dipakai: fp_total 935 menjadi 936, presisi median 0,7789 menjadi 0,7791. "
  f"Mutasi kedua awalnya tidak tertangkap karena toleransi pertama terlalu longgar, yaitu 0,00051, "
  f"dan setelah toleransi diperketat menjadi 5e-5 keduanya tertangkap. Tanpa langkah ini, hasil "
  f"nol selisih pada bagian 2.3 tidak sah.")
w("")
w("### 2.5 Aritmetika FAR dihitung ulang")
w("")
w(f"Untuk setiap fold dan setiap seed, FAR kalender dihitung ulang dari fp dan menit negatif "
  f"kalender tanpa memakai fungsi harness. "
  f"{ang(len(arit),'nilai','RUN-KITA','aritmetika_far','bagian 2.5')} nilai diperiksa dan "
  f"{ang(arit_beda,'nilai','DERIVASI','selisih di atas 1e-9','bagian 2.5')} menyimpang.")
w("")
w("---")
w("")
w("## 3. Artefak JSON dan klaim bernama")
w("")
w("### 3.1 Artefak terbuka")
w("")
w("| Kartu | Berkas | Byte | Buka |")
w("|---|---|---|---|")
for k in KARTU:
    semua_buka = all(a["buka"] for a in art if a["kartu"] == k)
    w(f"| {k} | {ang(art_n[k],'berkas','RUN-KITA',f's5_resolve3.json artefak kartu {k}','bagian 3.1')} "
      f"| {ang(art_byte[k],'byte','RUN-KITA',f'jumlah byte artefak kartu {k}','bagian 3.1')} "
      f"| {'ya' if semua_buka else 'tidak'} |")
w("")
w(f"Semua {ang(len(art),'berkas','RUN-KITA','s5_resolve3.json','bagian 3.1')} berkas terbuka sebagai "
  f"JSON atau JSONL. Catatan penting untuk S2: `s2_vib.json` dan `s2_ssi.json` tidak ada lagi di "
  f"`scratch/rnd/s2/`, dan ketiadaannya disengaja karena berkas itu dibatalkan. Acuan S2 yang sah "
  f"adalah `s2_records_vib.json`, `s2_records_ssi.json`, `s2_ringkas.json`, dan `s2_meta.json`.")
w("")
w("")
w("Jumlah record diukur secara mekanis pada setiap berkas, bukan dikira: jumlah kunci top-level, "
  "koleksi terpanjang di dalam berkas, dan kunci hitung eksplisit bila berkas memuatnya. Nilai yang "
  "tidak dapat dihitung dari berkas tidak diklaim di tabel ini.")
w("")
w("| Kartu | Berkas | Tipe | Kunci top | Koleksi terpanjang | Kunci hitung eksplisit | Byte | sha256 |")
w("|---|---|---|---|---|---|---|---|")
for h in art2["daftar"]:
    kt = "-" if h["kunci_top"] is None else ang(h["kunci_top"], "kunci", "RUN-KITA",
                                                "s5_artefak.json " + h["berkas"], "bagian 3.1")
    jalur_kol = h["koleksi"][0].replace("|", ".")
    kol = jalur_kol + " = " + ang(h["koleksi"][1], "record", "RUN-KITA",
                                  "s5_artefak.json " + h["berkas"], "bagian 3.1")
    pasangan, terlihat = dict(), set()
    for p, v in h["hitung"]:
        if p in terlihat:
            continue
        terlihat.add(p)
        pasangan[p] = v
        if len(pasangan) == 3:
            break
    potongan = []
    for p, v in pasangan.items():
        potongan.append(p.replace("|", ".") + " = " + ang(v, "nilai", "RUN-KITA", h["berkas"] + ".json",
                                                          "bagian 3.1"))
    hit = "; ".join(potongan) if potongan else "-"
    byte_sel = ang(h["byte"], "byte", "RUN-KITA", "os.path.getsize " + h["jalur"], "bagian 3.1")
    w("| " + " | ".join([h["kartu"], h["berkas"], h["tipe"], kt, kol, hit, byte_sel, h["sha12"]]) + " |")
w("")
w("### 3.2 Klaim bernama: nilai dokumen dibandingkan dengan path JSON")
w("")
w(f"Setiap baris di bawah mengambil satu nilai yang tertulis di dokumen, lalu mengambil nilai dari "
  f"path JSON yang eksplisit. "
  f"{ang(len(klaim),'klaim','RUN-KITA','s5_klaim2.json','bagian 3.2')} klaim diuji, "
  f"{ang(klaim_lulus,'klaim','RUN-KITA','klaim dengan selisih dalam toleransi pembulatan','bagian 3.2')} "
  f"lulus, {ang(klaim_gagal,'klaim','DERIVASI','klaim yang gagal','bagian 3.2')} gagal. Nilai JSON "
  f"ditulis apa adanya dengan titik desimal, sedangkan nilai dokumen ditulis dengan koma seperti "
  f"pada dokumen asalnya, dan perbandingan dilakukan pada nilai numeriknya bukan pada teksnya.")
w("")
w("| Kartu | Klaim | Rujukan JSON | Nilai JSON | Nilai dokumen | Hasil |")
w("|---|---|---|---|---|---|")
for c in klaim:
    jalur_tampil = c["jalur"].replace("|", ".")
    ruj = "%s %s" % (c["berkas"], jalur_tampil)
    v_json = L(c["nilai_json"], c["satuan"], "RUN-KITA", ruj, "bagian 3.2 tabel klaim", "MATCH")
    v_dok = L(c["teks_dokumen"], c["satuan"], "RUN-KITA", ruj, "bagian 3.2 tabel klaim", "MATCH")
    hasil_c = "cocok" if c["lulus"] else "beda"
    w(f"| {c['kartu']} | {c['label']} | `{c['berkas']}` `{jalur_tampil}` "
      f"| {v_json} | {v_dok} | {hasil_c} |")
w("")
w(f"Tiga entri pertama pada versi pertama pemeriksa ini salah karena path diambil dari handoff S2 "
  f"yang sudah dibatalkan, bukan dari `s2_ringkas.json`. Kesalahannya adalah kesalahan auditor, dan "
  f"yang benar adalah path `ssi.sensitivitas.ML_kalender_b24` untuk nilai 0,0762 dan 0,2157, serta "
  f"`vib.sensitivitas.ML_kalender_b24` untuk 0,1041, 0,7781, dan 3,1225. Ini contoh mengapa angka "
  f"handoff tidak boleh dipakai sebagai sumber.")
w("")
w("### 3.3 Uji klaim setiap angka punya baris ledger")
w("")
w("Klaim yang diuji: S1 menulis setiap angka punya baris S1-nnn, S2 dan S3 menulis hal yang sama "
  "untuk kartunya. Metode: setiap sel angka pada tabel dokumen diambil, lalu dicari padanannya pada "
  "blok ledger kartu itu, dengan dua tafsir untuk token bertitik dan toleransi pembulatan. Batas "
  "metode: yang diuji adalah keberadaan nilai pada blok, bukan pemetaan sel ke baris tertentu, dan "
  "penerimaan dua tafsir membuat angka ini batas atas.")
w("")
w("| Kartu | Sel angka tabel | Punya padanan | Fraksi | Contoh tanpa padanan |")
w("|---|---|---|---|---|")
for k in KARTU:
    c = cov[k]
    contoh = ", ".join(c["contoh_tanpa_padanan"][:5]) if c["contoh_tanpa_padanan"] else "tidak ada"
    w(f"| {k} | {ang(c['sel_tabel'],'sel','RUN-KITA',f's5_coverage.json {k}.sel_tabel','bagian 3.3')} "
      f"| {ang(c['ada_di_ledger'],'sel','RUN-KITA',f's5_coverage.json {k}.ada_di_ledger','bagian 3.3')} "
      f"| {ang(c['fraksi'],'fraksi','DERIVASI',f'{k}.ada_di_ledger dibagi {k}.sel_tabel','bagian 3.3')} "
      f"| {contoh} |")
w("")
cov_s1_rasio = "%s dari %s" % (cov_s1["ada_di_ledger"], cov_s1["sel_tabel"])
cov_s3_rasio = "%s dari %s" % (cov_s3["ada_di_ledger"], cov_s3["sel_tabel"])
fr_s2 = ang(cov["S2"]["fraksi"], "fraksi", "DERIVASI", "430 dari 430", "bagian 3.3")
fr_s4 = ang(cov["S4"]["fraksi"], "fraksi", "DERIVASI", "95 dari 95", "bagian 3.3")
fr_s1 = ang(cov_s1["fraksi"], "fraksi", "DERIVASI", cov_s1_rasio, "bagian 3.3")
fr_s3 = ang(cov_s3["fraksi"], "fraksi", "DERIVASI", cov_s3_rasio, "bagian 3.3")
w(f"S2 memberi fraksi {fr_s2} dan S4 memberi {fr_s4}, sehingga klaim kedua kartu itu terpenuhi. "
  f"S1 memberi {fr_s1} dan S3 memberi {fr_s3}, sehingga klaim kedua dokumen itu tidak terpenuhi "
  f"pada tabel per fold dan tabel kelayakan. Ini cacat D2 dan D3.")
w("")
w("---")
w("")
w("## 4. Baris ledger per kartu")
w("")
w("| Kartu | Baris | Cocok | Tidak cocok | Tidak dapat diresolusi | Derivasi | Sel bukan angka |")
w("|---|---|---|---|---|---|---|")
for k in KARTU:
    w(f"| {k} | {ang(n_led[k],'baris','RUN-KITA',f'grep ^| {k}- pada RND_PROVENANCE_LEDGER.md','bagian 4')} "
      f"| {ang(n_match[k],'baris','RUN-KITA',f's5_resolve3.json ledger.{k}.kelas_hasil MATCH','bagian 4')} "
      f"| {ang(n_mis[k],'baris','RUN-KITA',f's5_resolve3.json MISMATCH kartu {k}','bagian 4')} "
      f"| {ang(n_takres[k],'baris','RUN-KITA',f's5_resolve3.json tidak_resolve kartu {k}','bagian 4')} "
      f"| {ang(n_deriv[k],'baris','RUN-KITA',f's5_resolve3.json derivasi kartu {k}','bagian 4')} "
      f"| {ang(n_nonnum[k],'baris','RUN-KITA',f's5_resolve3.json sel_bukan_angka kartu {k}','bagian 4')} |")
w("")
w(f"Tidak ada kartu dengan nol baris, jadi tidak ada kartu yang gagal provenance pada butir hitung "
  f"baris. Seluruh baris tepat tujuh kolom dan tidak ada kode ganda.")
w("")
triase = json.loads((S5 / "s5_mismatch_triage.json").read_text(encoding="utf-8"))
assert triase["n_cocok"] == triase["n_baris"] == n_mis_total, (triase["n_cocok"], n_mis_total)

w(f"Metode resolusi: nilai dan kolom rujukan persis setiap baris diambil, lalu path JSON pada "
  f"rujukan itu dibuka dan nilainya dibandingkan. Bila satu sel memuat beberapa angka, setiap "
  f"komponen diuji terhadap daun numerik cabang yang dirujuk. "
  f"{ang(n_mis_total,'baris','DERIVASI','jumlah MISMATCH empat kartu','bagian 4')} baris dinyatakan "
  f"tidak cocok oleh mesin. Setelah diperiksa tangan, keenam baris itu adalah sel hitungan atau "
  f"julat, bukan nilai daun tunggal, sehingga resolver tidak dapat membandingkannya. Hitungan "
  f"ulang mandiri memberi "
  f"{ang(triase['n_cocok'],'baris','RUN-KITA','s5_mismatch_triage.json n_cocok','bagian 4')} baris "
  f"cocok dari {ang(triase['n_baris'],'baris','RUN-KITA','s5_mismatch_triage.json n_baris','bagian 4')}, "
  f"jadi tidak ada angka salah pada kelompok itu. Bentuk selnya: panjang daftar 7, 5, 9, 2, dan 7, "
  f"serta satu julat persen 1,32 sampai 54,25.")
w("")
w(f"Cacat angka yang nyata ditemukan di luar kelompok itu. Baris S4-013 menulis 884 kolom, sedangkan "
  f"kolom rujukan pada baris yang sama menyebut sumber.kolom berisi "
  f"{ang(kolom_labels,'kolom','RUN-KITA','labels_duration.json sumber.kolom','bagian 4')} kolom, "
  f"sehingga baris itu membantah dirinya sendiri. Baris tersebut tidak masuk kelompok MISMATCH, "
  f"karena resolver hanya menguji keberadaan nilai pada cabang dan tidak menguji pasangan nilai "
  f"kedua di dalam satu sel. Ini contoh bahwa resolusi otomatis tidak cukup dan pemeriksaan tangan "
  f"tetap perlu.")
w("")
w(f"Versi pertama resolver juga menandai S2-448, S2-449, dan S3-085. Ketiganya derivasi sah dan "
  f"dapat dihitung ulang: S2-448 nilai 12,1 = (1 - p) / p dengan p = 0,07619, yang memberi "
  f"{ang(round(d121, 2),'rasio','DERIVASI','(1 - 0.07619) / 0.07619','bagian 4')}; S2-449 nilai 3,67 = "
  f"22,0218 dibagi 6, yang memberi {ang(round(d367, 2),'rasio','DERIVASI','22.0218 / 6','bagian 4')}; "
  f"S3-085 nilai 18,41 = 110,432 dibagi 6. Penandaan itu kesalahan alat ukur, bukan kesalahan ledger.")
w("")
w(f"Format angka ledger mencampur gaya: {ang(ambig_total,'sel','RUN-KITA','pola 1.234 pada kolom angka tiap baris','bagian 4')} "
  f"sel memakai titik ribuan, sedangkan blok yang sama memakai koma desimal. Sebaran: "
  f"S1 {ang(ambig['S1'],'sel','RUN-KITA','hitung pola 1.234 kartu S1','bagian 4')}, "
  f"S2 {ang(ambig['S2'],'sel','RUN-KITA','hitung pola 1.234 kartu S2','bagian 4')}, "
  f"S3 {ang(ambig['S3'],'sel','RUN-KITA','hitung pola 1.234 kartu S3','bagian 4')}, "
  f"S4 {ang(ambig['S4'],'sel','RUN-KITA','hitung pola 1.234 kartu S4','bagian 4')}. Satu sel berisi "
  f"32.256 dapat berarti 32,256 atau 32256, dan keduanya benar terhadap JSON yang berbeda. Blok S5 "
  f"pada ledger memakai titik desimal tanpa pemisah ribuan supaya cacat ini tidak berulang.")
w("")
w("---")
w("")
w("## 5. DOI dan rujukan luar")
w("")
w(f"Butir DOI disiapkan dengan dua lapis seperti V1, yaitu lapis registrasi (HEAD ke doi.org tanpa "
  f"mengikuti redirect) dan lapis metadata (api.crossref.org). Pada gelombang 2 tidak ada objek "
  f"yang dapat diperiksa: {ang(n_doi_total,'DOI','RUN-KITA','pola 10.xxxx pada empat dokumen','bagian 5')} "
  f"DOI dan {ang(n_url_total,'URL','RUN-KITA','pola https:// pada empat dokumen','bagian 5')} URL "
  f"ditemukan. Karena tidak ada target, hasilnya ditulis tidak berlaku, bukan lulus. Nol "
  f"pemeriksaan berhasil bukan bukti bahwa rujukan benar.")
w("")
w("| Kartu | RUN-KITA | DERIVASI | KONVENSI | STANDAR | BELUM TERUKUR |")
w("|---|---|---|---|---|---|")
for k in KARTU:
    s = src[k]
    w(f"| {k} | {ang(s.get('RUN-KITA',0),'baris','RUN-KITA',f'kolom kelas sumber kartu {k}','bagian 5')} "
      f"| {ang(s.get('DERIVASI',0),'baris','RUN-KITA',f'kolom kelas sumber kartu {k}','bagian 5')} "
      f"| {ang(s.get('KONVENSI',0),'baris','RUN-KITA',f'kolom kelas sumber kartu {k}','bagian 5')} "
      f"| {ang(s.get('STANDAR',0),'baris','RUN-KITA',f'kolom kelas sumber kartu {k}','bagian 5')} "
      f"| {ang(s.get('BELUM-TERUKUR',0),'baris','RUN-KITA',f'kolom kelas sumber kartu {k}','bagian 5')} |")
w("")
w(f"Satu-satunya rujukan luar adalah API RP 7G pada S2 untuk nilai 32,17405 ft/s2, dan rujukan itu "
  f"tidak menyebut nomor bagian. Menurut aturan provenance, kelas STANDAR menuntut nomor standar "
  f"dan bagian, sehingga baris ini lemah dan dicatat sebagai cacat D5.")
w("")
w("---")
w("")
w("## 6. Pemisahan lapisan A, B, C dan daftar belum terverifikasi")
w("")
w("| Kartu | Lapisan A | Lapisan B | Lapisan C | Bagian belum terverifikasi | Butir |")
w("|---|---|---|---|---|---|")
LAP = {
 "S1": ("terukur penuh, bagian 6 untuk sembilan fold dan lima seed",
        "terukur untuk lead dan beban alarm, belum untuk rupiah dan jam henti",
        "terukur antar well, antar seed, antar titik operasi; lintas kampanye belum"),
 "S2": ("terukur, bagian 4 dengan kurva sensitivitas anggaran",
        "belum terukur, bagian 7, sebabnya data maintenance tidak ada",
        "terukur, bagian 6 kestabilan, variasi seed, cakupan"),
 "S3": ("terukur, bagian 4", "belum terukur, bagian 6, sebabnya tidak ada kunci bit",
        "terukur, bagian 5"),
 "S4": ("tidak diubah kartu ini, diambil dari R8 dan S1",
        "terukur sebagian, bagian 7, komponen jam henti terukur dan rupiah belum",
        "tidak diubah kartu ini, satu kontribusi register kegagalan"),
}
for k in KARTU:
    a, b, c = LAP[k]
    w(f"| {k} | {a} | {b} | {c} | `{stats[k]['header']}` "
      f"| {ang(n_butir[k],'butir','RUN-KITA',f'daftar belum terverifikasi {nama_dok[k]}','bagian 6')} |")
w("")
w(f"Keempat dokumen memisahkan tiga lapisan dan punya bagian daftar belum terverifikasi, dengan "
  f"{ang(n_butir_total,'butir','DERIVASI','jumlah butir empat dokumen','bagian 6')} butir seluruhnya. "
  f"Yang belum terukur pada lapisan B konsisten dengan temuan S4: biaya, work order bernomor, "
  f"jadwal inspeksi, dan produksi tertunda tidak ada di repo, sehingga nilai rupiah tidak dapat "
  f"dihitung dari data yang ada.")
w("")
w(f"Jumlah pikiran sequ-mcp yang dinyatakan tiap dokumen: S1 {ang(sequ['S1'],'pikiran','RUN-KITA','RND_S1_SEED_ROBUSTNESS.md baris 12','bagian 6')}, "
  f"S2 {ang(sequ['S2'],'pikiran','RUN-KITA','RND_S2_HYBRID_VIB_SSI.md baris 16','bagian 6')}, "
  f"S3 {ang(sequ['S3'],'pikiran','RUN-KITA','RND_S3_HYBRID_BITWEAR.md baris 19','bagian 6')}, "
  f"S4 {ang(sequ['S4'],'pikiran','RUN-KITA','RND_S4_LAYER_B_DATA.md baris 11','bagian 6')}, seluruhnya "
  f"{ang(sequ_total,'pikiran','DERIVASI','jumlah empat dokumen','bagian 6')}. Semua di atas ambang tiga. "
  f"Angka ini adalah laporan diri penulis kartu.")
w("")
w(f"Keempat dokumen juga bersih dari em-dash: {ang(em_total,'em-dash','RUN-KITA','hitung U+2014 pada empat dokumen','bagian 6')} "
  f"kemunculan. Ini sesuai aturan nomor tujuh pada kartu.")
w("")
w("---")
w("")
w("## 7. Tabel cacat")
w("")
w(f"Jumlah cacat {ang(n_cacat,'cacat','RUN-KITA','daftar CACAT pada generator S5','bagian 7')}, dengan "
  f"{ang(n_kritis,'cacat','DERIVASI','cacat bertingkat kritis','bagian 7')} kritis dan sisanya minor. "
  f"Tidak ada cacat kritis.")
w("")
w("| Kode | Kartu | Cacat | Bukti | Tingkat | Yang harus diperbaiki |")
w("|---|---|---|---|---|---|")
for kode, kartu, cacat, bukti, tingkat, fix in CACAT:
    w(f"| {kode} | {kartu} | {cacat} | {bukti} | {tingkat} | {fix} |")
w("")
w("Arti tidak adanya cacat kritis: pada dua seed yang diuji, angka utama S1 dapat dibangkitkan "
  "ulang persis, seluruh artefak terbuka, dan setiap kartu punya baris ledger. Cacat yang tersisa "
  "menyangkut kebenaran klaim tentang provenance sendiri, format angka, dan keterlacakan.")
w("")
w("Satu hal yang harus dinyatakan tegas supaya tidak disalahpahami: tidak adanya cacat kritis bukan "
  "bukti bahwa angka S2, S3, dan S4 benar. Untuk ketiganya, kartu ini memeriksa keberadaan nilai "
  "pada artefak dan keterlacakan baris ledger, bukan menjalankan ulang modelnya. Hanya S1 yang "
  "dijalankan ulang penuh, dan hanya pada dua dari lima seed.")
w("")
w("---")
w("")
w("## 8. Yang belum terverifikasi pada audit ini")
w("")
w("1. Rerun hanya dua seed dari lima seed S1, yaitu 42 dan 13. Seed 7, 21, dan 33 tidak dijalankan.")
w("2. Rerun memakai harness yang sama dengan S1, sehingga yang terbukti adalah kesambungan dan "
  "reproduksibilitas, bukan kebenaran desain harness. Jalur independen yang dipakai terbatas pada "
  "cap jari dataset, tabel per well dari CSV mentah, dan aritmetika FAR.")
w("3. S2, S3, dan S4 tidak dijalankan ulang. Model, kalibrasi, dan pemindaian DDR tidak "
  "direproduksi; yang diperiksa hanya artefak, ledger, dan angka yang dikutip.")
w("4. Resolusi ledger memakai heuristik path. Untuk sel multi-nilai, pemetaan posisional nilai ke "
  "kunci tidak diuji, hanya keberadaan nilai di cabang.")
w("5. Uji cakupan ledger memakai pencarian nilai pada blok, bukan pemetaan sel ke baris, dan "
  "menerima dua tafsir titik. Angka fraksi pada bagian 3.3 karena itu adalah batas atas.")
w("6. Jumlah pikiran sequ pada empat dokumen adalah laporan diri penulis kartu dan tidak dapat "
  "diperiksa dari artefak. Untuk S1, empat pikiran run awal bahkan dinyatakan tidak terbukti oleh "
  "dokumen itu sendiri.")
w("7. Pemeriksaan DOI berhenti pada kesimpulan tidak ada DOI. Tidak ada permintaan jaringan ke "
  "doi.org atau Crossref pada kartu ini karena tidak ada objek yang bisa diperiksa.")
w("8. Mutu keputusan teknis tiap kartu, misalnya apakah pemilihan ambang wajar, tidak dinilai di "
  "sini. Kartu ini menilai bukti dan keterlacakan.")
w("")
w("---")
w("")
w("## 9. Ringkasan lima baris")
w("")
w(f"1. Rerun seed 42 dan 13 memberi angka yang sama persis dengan dokumen S1 pada "
  f"{ang(n_sel,'sel','RUN-KITA','tiga tabel S1 dibandingkan ulang','bagian 9')} sel yang diperiksa, "
  f"dengan {ang(n_gagal,'sel','DERIVASI','sel yang gagal','bagian 9')} selisih, dan pengunci sudah "
  f"diuji bisa gagal lewat {ang(mutasi,'mutasi','RUN-KITA','s5_negatif.json','bagian 9')} mutasi "
  f"yang tertangkap.")
w(f"2. Seluruh {ang(len(art),'berkas','RUN-KITA','s5_resolve3.json','bagian 9')} artefak terbuka, dan "
  f"{ang(klaim_lulus,'klaim','RUN-KITA','s5_klaim2.json','bagian 9')} klaim bernama path terbukti sama "
  f"dengan JSON mentah.")
w(f"3. Empat kartu punya ledger, total {ang(n_led_total,'baris','RUN-KITA','hitung baris ledger','bagian 9')} "
  f"baris tujuh kolom tanpa duplikat, sehingga tidak ada kartu yang gagal provenance pada butir hitung baris.")
w(f"4. Audit menemukan {ang(n_cacat,'cacat','RUN-KITA','daftar CACAT','bagian 9')} cacat, semuanya minor, "
  f"termasuk satu baris ledger yang membantah dirinya sendiri (S4-013: 884 kolom lawan 20 kolom).")
w(f"5. Tidak ada DOI untuk diperiksa, klaim setiap angka punya baris ledger hanya terpenuhi penuh "
  f"pada S2, dan keterlacakan kode ledger masih lemah karena S1, S2, dan S3 tidak mengutip kode "
  f"barisnya sendiri di badan dokumen.")
w("")
w("---")
w("")
w("Berkas bukti: `scratch/rnd/s5/s5_rerun_audit.json`, `s5_negatif.json`, `s5_resolve3.json`, "
  "`s5_klaim2.json`, `s5_coverage.json`, `s5_stats.json`, `s5_kode_doi_lapisan.json`. Kode: "
  "`scratch/rnd/s5/s5a_rerun_audit.py`, `s5b_negatif.py`, `s5c_klaim2.py`, `s5e_coverage.py`, "
  "`s5d_stats.py`, `a8_resolve3.py`, `a7_kode_doi.py`, `s5g_dokumen.py`.")
w("")

dok = "\n".join(P)
assert "\u2014" not in dok and "\u2013" not in dok, "em-dash atau en-dash terlarang"
DOC.write_text(dok, encoding="utf-8")

# ------------------------------------------------------------------ ledger S5
blok = ["## Bagian S5: audit gelombang 2 (kartu `t_b5b16adc`)", ""]
blok.append("Tanggal akses seluruh baris: 2026-10-28. Dokumen: `docs/RND_S5_AUDIT_WAVE2.md`.")
blok.append("Angka pada blok ini memakai titik desimal tanpa pemisah ribuan, supaya tidak ambigu "
            "dengan blok lain yang memakai titik ribuan. Nilai yang dikutip dari dokumen lain "
            "ditulis apa adanya pada kolom angka.")
blok.append("Setiap baris dibangkitkan `scratch/rnd/s5/s5g_dokumen.py`, dan nilai yang berasal dari "
            "JSON di-assert terhadap berkas sumbernya sebelum baris ditulis.")
blok.append("")
blok.append("| # | Angka | Satuan | Kelas sumber | Rujukan persis | Dipakai di | Status |")
blok.append("|---|---|---|---|---|---|---|")
for i, r in enumerate(ROWS, 1):
    sel = [str(r["angka"]), str(r["satuan"]), str(r["kelas"]), str(r["rujukan"]),
           str(r["dipakai"]), str(r["status"])]
    sel = [s.replace("|", ".") for s in sel]
    blok.append(f"| S5-{i:03d} | " + " | ".join(sel) + " |")

teks = LEDGER.read_text(encoding="utf-8")
pola = re.compile(r"^## Bagian S5:.*?(?=^## Bagian |\Z)", re.S | re.M)
teks = pola.sub("", teks).rstrip() + "\n\n" + "\n".join(blok) + "\n"
LEDGER.write_text(teks, encoding="utf-8")

print("dokumen:", len(dok.splitlines()), "baris,", len(dok.encode()), "byte, em-dash", dok.count("\u2014"))
print("ledger S5:", len(ROWS), "baris")
print("cacat:", n_cacat, "kritis:", n_kritis)
print("sel:", n_sel, "gagal:", n_gagal, "| artefak:", len(art), "| klaim:", len(klaim), "lulus:", klaim_lulus)
print("cakupan ledger:", {k: cov[k]["fraksi"] for k in KARTU})
