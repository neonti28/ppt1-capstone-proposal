"""Pemeriksa independen untuk BAB III 3.4 (MCDM).

Jalankan dari akar repo:
    python3 scratch/ppt1/check_mcdm.py

Pemeriksa ini TIDAK mengimpor build_mcdm.py maupun build_doc_mcdm.py. ROC,
TOPSIS, dan SAW dihitung ulang dari data mentah pada mcdm.json, lalu dibandingkan
dengan hasil yang tertulis pada JSON. Angka pada dokumen diperiksa terhadap JSON.
Tujuan: bila mesin hitung salah, pemeriksa ini tetap menangkapnya.

Keluaran: baris LOLOS atau GAGAL, lalu ringkasan. Exit code 1 bila ada yang gagal.
Jalankan dengan argumen --negatif untuk menjalankan uji negatif.
"""
import json
import math
import os
import re
import shutil
import sys

AKAR = "/mnt/d/Capstone 1(v2)"
DOC = os.path.join(AKAR, "docs/PPT1_BAB3_4_MCDM.md")
JSONF = os.path.join(AKAR, "scratch/ppt1/mcdm.json")
NEG = os.path.join(AKAR, "scratch/ppt1/_negatif")
LAPORAN_NEG = os.path.join(AKAR, "scratch/ppt1/check_mcdm_negative_test.txt")

TOL = 1e-6

# fungsi nilai, ditulis ulang dari definisi pada subbab 3.4.3
def nilai(c, unit):
    if c == "C1":
        return {"L100": 100.0, "L75": 75.0, "L40": 40.0, "L20": 20.0}[unit]
    if c == "C2":
        return min(100.0, 100.0 * float(unit) / 18.0)
    if c == "C3":
        return {"L100": 100.0, "L60": 60.0, "L30": 30.0}[unit]
    if c == "C4":
        return 100.0 if int(unit) == 0 else 0.0
    if c == "C5":
        return 100.0 / (1.0 + float(unit))
    if c == "C6":
        return max(0.0, min(100.0, 100.0 * (9.0 - float(unit)) / 9.0))
    if c == "C7":
        return 100.0 * float(unit[0]) / float(unit[1])
    if c == "C8":
        return {3: 100.0, 2: 50.0, 1: 0.0}[int(unit)]
    raise ValueError(c)


def roc(peringkat, n):
    urut = sorted(peringkat, key=lambda c: peringkat[c])
    w = {}
    for pos, c in enumerate(urut, start=1):
        w[c] = sum(1.0 / k for k in range(pos, n + 1)) / n
    return w


def topsis_hitung(M, w, ALT, KRIT):
    bagi = {c: math.sqrt(sum(M[(a, c)] ** 2 for a in ALT)) for c in KRIT}
    V = {(a, c): w[c] * M[(a, c)] / bagi[c] for a in ALT for c in KRIT}
    ip = {c: max(V[(a, c)] for a in ALT) for c in KRIT}
    im = {c: min(V[(a, c)] for a in ALT) for c in KRIT}
    out = {}
    for a in ALT:
        dp = math.sqrt(sum((V[(a, c)] - ip[c]) ** 2 for c in KRIT))
        dm = math.sqrt(sum((V[(a, c)] - im[c]) ** 2 for c in KRIT))
        out[a] = {"D_plus": dp, "D_minus": dm,
                  "C": dm / (dp + dm) if (dp + dm) else 0.0}
    urut = sorted(ALT, key=lambda a: -out[a]["C"])
    for i, a in enumerate(urut, start=1):
        out[a]["peringkat"] = i
    return out, urut


def saw_hitung(M, w, ALT, KRIT):
    bagi = {c: math.sqrt(sum(M[(a, c)] ** 2 for a in ALT)) for c in KRIT}
    skor = {a: sum(w[c] * M[(a, c)] / bagi[c] for c in KRIT) for a in ALT}
    return skor, sorted(ALT, key=lambda a: -skor[a])


def kendall(p, q):
    n = len(p)
    pq = {a: i for i, a in enumerate(q)}
    c = d = 0
    for i in range(n):
        for j in range(i + 1, n):
            s = pq[p[i]] - pq[p[j]]
            if s < 0:
                c += 1
            elif s > 0:
                d += 1
    return (c - d) / (c + d) if (c + d) else 0.0


def fmt(x, d=4):
    return f"{float(x):.{d}f}".replace(".", ",")


def angka(sel):
    sel = sel.strip().replace("+", "")
    if re.fullmatch(r"-?\d+(,\d+)?", sel):
        return float(sel.replace(",", "."))
    return None


def ambil_tabel(teks, penanda):
    """Ambil baris tabel pertama yang muncul setelah baris yang memuat penanda."""
    baris = teks.splitlines()
    for i, b in enumerate(baris):
        if penanda in b:
            keluar = []
            mulai = False
            for b2 in baris[i + 1:]:
                if b2.strip().startswith("|"):
                    mulai = True
                    sel = [x.strip() for x in b2.strip().strip("|").split("|")]
                    if all(re.fullmatch(r"-{2,}", x) for x in sel if x):
                        continue
                    keluar.append(sel)
                elif mulai:
                    break
            return keluar
    return []


def baca(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def kunci_ada(obj, kunci):
    for bagian in kunci.split("."):
        if isinstance(obj, dict) and bagian in obj:
            obj = obj[bagian]
        elif isinstance(obj, list) and bagian.isdigit() and int(bagian) < len(obj):
            obj = obj[int(bagian)]
        else:
            return False
    return True


TOKEN = [
    ("docs/V9_PM2_VERDICT.md", 114, "119,6"),
    ("docs/V9_PM2_VERDICT.md", 114, "496,09"),
    ("docs/V9_EVAL_B_LAYERB.md", 101, "B1 0,51"),
    ("docs/V9_EVAL_B_LAYERB.md", 101, "TLead"),
    ("docs/V9_EVAL_B_LAYERB.md", 103, "0/3 onset"),
    ("docs/V9_EVAL_C_LAYERC.md", 98, "TLead 20"),
    ("docs/V9_EVAL_C_LAYERC.md", 98, "precision run 0,50"),
    ("docs/V7_R1_SOLUTIONS.md", 66, "G1 1/2"),
    ("docs/V7_R1_SOLUTIONS.md", 97, "G1 3/7"),
    ("docs/V7_R1_SOLUTIONS.md", 127, "G1 2/7"),
    ("docs/V7_R1_SOLUTIONS.md", 160, "G1 0/4"),
    ("docs/V7_R1_SOLUTIONS.md", 197, "G1 4/5"),
    ("docs/V7_R1_SOLUTIONS.md", 203, "G1 3/4"),
    ("docs/V8_PM_VERDICT.md", 202, "0/10"),
    ("docs/V8_PM_VERDICT.md", 155, "LULUS penuh"),
    ("docs/V6_PM_VERDICT.md", 131, "LULUS penuh"),
    ("docs/PPT1_BAB3_2.md", 665, "Antarmuka peringatan belum dirancang"),
    ("docs/PPT1_BAB3_2.md", 659, "Tarif rig per jam tidak tersedia"),
    ("scratch/ppt1/docx_draft_text.txt", 279, "Random Forest"),
    ("scratch/ppt1/docx_draft_text.txt", 229, "TOPSIS"),
]


def periksa(doc_path, json_path):
    """Kembalikan daftar (nama, lolos, bukti)."""
    hasil = []
    teks = baca(doc_path)
    J = json.loads(baca(json_path))

    KRIT = [k["id"] for k in J["kriteria"]]
    ALT = [a for a, _ in J["alternatif"]] if "alternatif" in J else list(J["matriks_nilai"].keys())
    ALT = list(J["matriks_nilai"].keys())
    NAMA = {a: "" for a in ALT}

    # ---- 1. kelengkapan matriks
    jml_sel = len(J["sel"])
    hasil.append(("jumlah sel 9 kali 8", jml_sel == 72, f"{jml_sel} sel"))
    hasil.append(("jumlah alternatif", len(ALT) == 9, f"{len(ALT)} alternatif"))
    hasil.append(("jumlah kriteria", len(KRIT) == 8, f"{len(KRIT)} kriteria"))

    # ---- 2. fungsi nilai dihitung ulang
    salah_nilai = []
    for s in J["sel"]:
        harap = nilai(s["c"], s["unit"])
        if abs(harap - s["nilai"]) > TOL:
            salah_nilai.append(f"{s['alt']}/{s['c']} harap {harap:.6f} tertulis {s['nilai']:.6f}")
    hasil.append(("fungsi nilai konsisten dengan unit mentah", not salah_nilai,
                  "72 sel" if not salah_nilai else "; ".join(salah_nilai[:3])))
    salah_m = []
    for s in J["sel"]:
        if abs(J["matriks_nilai"][s["alt"]][s["c"]] - s["nilai"]) > TOL:
            salah_m.append(f"{s['alt']}/{s['c']}")
    hasil.append(("matriks nilai sama dengan sel", not salah_m,
                  "72 sel" if not salah_m else ", ".join(salah_m[:3])))

    # ---- 3. bobot ROC dihitung ulang
    peringkat = {k["id"]: k["peringkat"] for k in J["kriteria"]}
    w = roc(peringkat, len(KRIT))
    beda_w = [f"{c}: harap {w[c]:.6f} tertulis {J['bobot']['nilai'][c]:.6f}"
              for c in KRIT if abs(w[c] - J["bobot"]["nilai"][c]) > TOL]
    hasil.append(("bobot ROC dapat dihitung ulang", not beda_w,
                  f"jumlah {sum(w.values()):.12f}" if not beda_w else "; ".join(beda_w)))
    hasil.append(("jumlah bobot = 1", abs(sum(w.values()) - 1) < 1e-9, f"{sum(w.values()):.12f}"))

    # ---- 4. TOPSIS dihitung ulang
    M = {(a, c): J["matriks_nilai"][a][c] for a in ALT for c in KRIT}
    t2, urut2 = topsis_hitung(M, w, ALT, KRIT)
    beda_t = [f"{a}: harap {t2[a]['C']:.6f} tertulis {J['topsis']['sel'][a]['C']:.6f}"
              for a in ALT if abs(t2[a]["C"] - J["topsis"]["sel"][a]["C"]) > TOL]
    hasil.append(("koefisien TOPSIS dapat dihitung ulang", not beda_t,
                  f"juara {urut2[0]}" if not beda_t else "; ".join(beda_t[:3])))
    hasil.append(("urutan TOPSIS dapat dihitung ulang", urut2 == J["topsis"]["peringkat"],
                  f"{', '.join(urut2)}"))
    beda_d = [a for a in ALT
              if abs(t2[a]["D_plus"] - J["topsis"]["sel"][a]["D_plus"]) > TOL
              or abs(t2[a]["D_minus"] - J["topsis"]["sel"][a]["D_minus"]) > TOL]
    hasil.append(("jarak D plus dan D minus dapat dihitung ulang", not beda_d,
                  "18 nilai" if not beda_d else ", ".join(beda_d[:3])))

    # ---- 5. SAW dihitung ulang dan pembanding
    skor2, urut_s = saw_hitung(M, w, ALT, KRIT)
    beda_s = [a for a in ALT if abs(skor2[a] - J["saw"]["skor"][a]) > TOL]
    hasil.append(("skor SAW dapat dihitung ulang", not beda_s,
                  "9 nilai" if not beda_s else ", ".join(beda_s[:3])))
    hasil.append(("SAW memberi urutan sama dengan JSON", urut_s == J["saw"]["peringkat"],
                  ", ".join(urut_s)))
    tau = kendall(urut2, urut_s)
    hasil.append(("juara TOPSIS dan SAW sama", urut2[0] == urut_s[0], f"{urut2[0]} dan {urut_s[0]}"))
    hasil.append(("Kendall tau JSON sama dengan hitungan ulang",
                  abs(tau - J["kendall_topsis_saw"]) < 1e-6, f"{tau:.6f}"))

    # ---- 6. sensitivitas
    sken = J["sensitivitas"]["skenario"]
    hasil.append(("jumlah skenario minimal delapan", len(sken) >= 8, f"{len(sken)} skenario"))
    hasil.append(("jumlah skenario minimal tiga (syarat kartu)", len(sken) >= 3, f"{len(sken)} skenario"))
    juara_sken = sorted({s["juara"] for s in sken})
    hasil.append(("juara pada seluruh skenario konsisten", len(juara_sken) <= 1,
                  f"juara {', '.join(juara_sken)}"))
    hasil.append(("jumlah uji satu per satu enam belas",
                  len(J["sensitivitas"]["oat"]) == 16, f"{len(J['sensitivitas']['oat'])} uji"))
    hasil.append(("sapuan C1 punya titik balik",
                  J["sensitivitas"].get("titik_balik_C1") is not None,
                  str(J["sensitivitas"]["juara_unik_sapuan"])))

    # ---- 7. draft lama
    dl = J["draft_lama"]
    hasil.append(("lima baris draft dihitung ulang", len(dl["baris"]) == 5, f"{len(dl['baris'])} baris"))
    hasil.append(("jumlah baris tidak reproducible dilaporkan",
                  dl["jumlah_tidak_reproduksi"] == len(dl["baris_tidak_reproduksi"]) == 4,
                  f"{dl['jumlah_tidak_reproduksi']} dari 5"))
    hasil.append(("TOPSIS draft memberi juara A1 ML Classifier",
                  dl["topsis_sejati"][0]["nama"].startswith("A1"),
                  f"{dl['topsis_sejati'][0]['nama']} C {dl['topsis_sejati'][0]['C']:.6f}"))

    # ---- 8. angka pada dokumen
    hilang = []
    for a in ALT:
        r = J["topsis"]["sel"][a]
        pola = f"| {r['peringkat']} | {a} |"
        if pola not in teks:
            hilang.append(f"baris TOPSIS {a}")
        if fmt(r["C"]) not in teks:
            hilang.append(f"C {a} {fmt(r['C'])}")
    for c in KRIT:
        if fmt(w[c]) not in teks:
            hilang.append(f"bobot {c} {fmt(w[c])}")
    hasil.append(("angka TOPSIS dan bobot muncul pada dokumen", not hilang,
                  "9 baris dan 8 bobot" if not hilang else "; ".join(hilang[:4])))

    # ---- 8b. tabel hasil TOPSIS dibaca ulang dan dicocokkan persis
    tabel_t = [r for r in ambil_tabel(teks, "Tabel 3.4.4 Hasil TOPSIS") if angka(r[0]) is not None]
    cek_t = []
    if len(tabel_t) != len(ALT):
        cek_t.append(f"jumlah baris {len(tabel_t)}, seharusnya {len(ALT)}")
    for row in tabel_t:
        if len(row) < 6:
            cek_t.append(f"kolom kurang: {row}")
            continue
        per, a, dpl, dmi, cc = row[0], row[1], row[3], row[4], row[5]
        if a not in ALT:
            cek_t.append(f"alternatif asing {a}")
            continue
        r = J["topsis"]["sel"][a]
        if angka(per) != r["peringkat"]:
            cek_t.append(f"{a} peringkat {per} tidak sama dengan {r['peringkat']}")
        for label, sel, harap in (("D+", dpl, r["D_plus"]), ("D-", dmi, r["D_minus"]), ("C", cc, r["C"])):
            x = angka(sel)
            if x is None or abs(x - round(harap, 4)) > 1e-6:
                cek_t.append(f"{a} {label} tertulis {sel}, seharusnya {fmt(harap)}")
    hasil.append(("tabel hasil TOPSIS cocok persis dengan JSON", not cek_t,
                  f"{len(tabel_t)} baris dibaca" if not cek_t else "; ".join(cek_t[:4])))

    tabel_w = [r for r in ambil_tabel(teks, "| Peringkat | Kriteria | Aturan | Bobot ROC | Alasan ringkas |") if angka(r[0]) is not None]
    cek_w = []
    if len(tabel_w) != len(KRIT):
        cek_w.append(f"jumlah baris {len(tabel_w)}, seharusnya {len(KRIT)}")
    for row in tabel_w:
        if len(row) < 4:
            cek_w.append(f"kolom kurang: {row}")
            continue
        c = row[1].split()[0]
        if c not in KRIT:
            cek_w.append(f"kriteria asing {c}")
            continue
        x = angka(row[3])
        if x is None or abs(x - round(w[c], 4)) > 1e-6:
            cek_w.append(f"{c} bobot tertulis {row[3]}, seharusnya {fmt(w[c])}")
    hasil.append(("tabel bobot cocok persis dengan hitungan ulang", not cek_w,
                  f"{len(tabel_w)} baris dibaca" if not cek_w else "; ".join(cek_w[:4])))

    # ---- 8c. koefisien yang disebut pada narasi harus salah satu nilai JSON
    nilai_C = {fmt(J["topsis"]["sel"][a]["C"], 4) for a in ALT}
    narasi = re.findall(r"koefisien kedekatan ([\d,]+)", teks)
    asing = [x for x in narasi if x not in nilai_C]
    hasil.append(("koefisien pada narasi sama dengan nilai JSON", not asing,
                  f"{len(narasi)} sebutan" if not asing else f"tidak dikenal: {', '.join(sorted(set(asing)))}"))

    hilang2 = []
    for s in sken:
        if f"| {s['id']} |" not in teks:
            hilang2.append(s["id"])
        if f"| {s['juara']} | {', '.join(s['tiga_besar'])} |" not in teks:
            hilang2.append(f"juara {s['id']}")
    hasil.append(("seluruh skenario muncul pada dokumen", not hilang2,
                  f"{len(sken)} skenario" if not hilang2 else "; ".join(hilang2[:4])))

    hilang3 = []
    for a in ALT:
        if f"| {a} |" not in teks:
            hilang3.append(a)
    hasil.append(("seluruh alternatif muncul pada tabel dokumen", not hilang3,
                  "9 alternatif" if not hilang3 else ", ".join(hilang3)))

    # ---- 9. rujukan berkas dan baris
    pola_ref = re.compile(r"(?P<path>(?:docs|scratch|code)/[A-Za-z0-9_\-./()]+\.(?:md|json|csv|py|txt))"
                          r"(?P<tail>(?::\s?\d+(?:\s?[-,]\s?\d+)*)?)")
    rusak = []
    n_ref = 0
    for m in pola_ref.finditer(teks):
        path = m.group("path")
        tail = m.group("tail") or ""
        penuh = os.path.join(AKAR, path)
        if not os.path.exists(penuh):
            rusak.append(f"berkas tidak ada {path}")
            continue
        if not tail:
            continue
        with open(penuh, encoding="utf-8", errors="replace") as f:
            jml = sum(1 for _ in f)
        for nomor in re.findall(r"\d+", tail):
            n_ref += 1
            if not (1 <= int(nomor) <= jml):
                rusak.append(f"{path}:{nomor} di luar rentang (berkas {jml} baris)")
    hasil.append(("seluruh rujukan berkas dan baris sah", not rusak,
                  f"{n_ref} nomor baris diperiksa" if not rusak else "; ".join(rusak[:4])))

    # ---- 10. rujukan kunci JSON
    pola_kunci = re.compile(r"(?P<path>(?:docs|scratch)/[A-Za-z0-9_\-./()]+\.json)\s+kunci\s+"
                            r"(?P<key>[A-Za-z0-9_.]+)")
    rusak_k = []
    n_k = 0
    for m in pola_kunci.finditer(teks):
        path, key = m.group("path"), m.group("key").rstrip(".")
        penuh = os.path.join(AKAR, path)
        if not os.path.exists(penuh):
            rusak_k.append(f"berkas tidak ada {path}")
            continue
        try:
            isi = json.loads(baca(penuh))
        except Exception as e:
            rusak_k.append(f"{path} gagal dibaca: {e}")
            continue
        n_k += 1
        if not kunci_ada(isi, key):
            rusak_k.append(f"{path} tidak punya kunci {key}")
    hasil.append(("seluruh rujukan kunci JSON sah", not rusak_k,
                  f"{n_k} kunci diperiksa" if not rusak_k else "; ".join(rusak_k[:4])))

    # ---- 11. token penanda
    rusak_t = []
    for path, nomor, token in TOKEN:
        penuh = os.path.join(AKAR, path)
        if not os.path.exists(penuh):
            rusak_t.append(f"{path} tidak ada")
            continue
        baris = baca(penuh).splitlines()
        if nomor > len(baris):
            rusak_t.append(f"{path}:{nomor} di luar rentang")
            continue
        if token not in baris[nomor - 1]:
            rusak_t.append(f"{path}:{nomor} tidak memuat '{token}'")
    hasil.append(("token penanda ada pada baris yang dikutip", not rusak_t,
                  f"{len(TOKEN)} token" if not rusak_t else "; ".join(rusak_t[:4])))

    # ---- 12. jumlah bukti per alternatif sama dengan C7
    alt_json = os.path.join(AKAR, "scratch/ppt1/alternatif.json")
    beda_b = []
    if os.path.exists(alt_json):
        aj = json.loads(baca(alt_json))
        peta = {it["id"]: len(it.get("bukti", [])) for it in aj["alternatif"]}
        for s in J["sel"]:
            if s["c"] != "C7":
                continue
            if peta.get(s["alt"]) != s["unit"][0]:
                beda_b.append(f"{s['alt']} bukti {peta.get(s['alt'])} unit {s['unit']}")
    hasil.append(("jumlah bukti per alternatif sama dengan unit C7", not beda_b,
                  "9 alternatif" if not beda_b else "; ".join(beda_b)))

    # ---- 13. gaya penulisan
    hasil.append(("nol em-dash dan en-dash", ("\u2014" not in teks) and ("\u2013" not in teks),
                  f"em {teks.count(chr(8212))}, en {teks.count(chr(8211))}"))
    han = len(re.findall(r"[\u4e00-\u9fff]", teks))
    hasil.append(("nol aksara Han", han == 0, f"{han} aksara"))
    hasil.append(("tidak memakai kata fiktif", "fiktif" not in teks.lower(),
                  "kata fiktif tidak ditemukan"))
    hasil.append(("skala 1 sampai 5 tidak dipakai untuk kriteria terukur",
                  "1 sampai 5 tanpa rubrik" in teks.lower() and "skala 1 sampai 5" in teks.lower(),
                  "larangan disebut dan dipatuhi"))

    # ---- 14. acceptance kartu
    hasil.append(("dokumen menjelaskan pemilihan metode", "### 3.4.2" in teks, "subbab 3.4.2 ada"))
    hasil.append(("dokumen memuat matriks keputusan", "Tabel 3.4.2" in teks and "Tabel 3.4.3" in teks,
                  "dua matriks ada"))
    hasil.append(("dokumen memuat uji sensitivitas", "Tabel 3.4.6" in teks and "Tabel 3.4.9" in teks,
                  "empat tabel uji ada"))
    hasil.append(("dokumen membandingkan draft lama",
                  "Tabel 3.4.10" in teks and "Tabel 3.4.11" in teks, "dua tabel draft ada"))
    hasil.append(("dokumen memuat perintah reproduksi",
                  "build_mcdm.py" in teks and "check_mcdm.py" in teks, "blok perintah ada"))

    # ---- 15. integritas tabel markdown
    baris_tabel = [b for b in teks.splitlines() if b.strip().startswith("|")]
    cacat = 0
    for b in baris_tabel:
        if b.count("|") < 2:
            cacat += 1
    hasil.append(("integritas tabel markdown", cacat == 0,
                  f"{len(baris_tabel)} baris tabel, {cacat} cacat"))

    return hasil


def jalankan(doc_path, json_path, label):
    try:
        hasil = periksa(doc_path, json_path)
    except Exception as e:
        print(f"[GAGAL] {label}: pemeriksa gagal menjalankan: {e}")
        return 1, 1, [f"exception: {e}"]
    gagal = [h for h in hasil if not h[1]]
    for nama, lolos, bukti in hasil:
        print(f"  [{'LOLOS' if lolos else 'GAGAL'}] {label} {nama}: {bukti}")
    print(f"{label}: {len(hasil) - len(gagal)} lolos, {len(gagal)} gagal")
    return len(hasil) - len(gagal), len(gagal), [h[0] for h in gagal]


def negatif():
    os.makedirs(NEG, exist_ok=True)
    asli = baca(DOC)
    dasar = os.path.join(NEG, "dasar.md")
    with open(dasar, "w", encoding="utf-8") as f:
        f.write(asli)
    lolos, gagal, _ = jalankan(dasar, JSONF, "salinan-asli")

    kasus = [
        ("angka koefisien diubah", lambda t: t.replace("0,8465", "0,8565", 1)),
        ("rujukan baris di luar rentang", lambda t: t.replace("docs/V9_PM2_VERDICT.md:114",
                                                              "docs/V9_PM2_VERDICT.md:9114")),
        ("em-dash disisipkan", lambda t: t.replace("3.4.5 Matriks keputusan",
                                                   "3.4.5 Matriks keputusan \u2014 tambahan", 1)),
        ("tabel draft dihapus", lambda t: t.replace("Tabel 3.4.11", "Tabel tanpa nomor")),
        ("kata fiktif disisipkan", lambda t: t.replace("Perbedaan angka draft lama",
                                                       "Perbedaan angka draft lama yang fiktif", 1)),
        ("kunci JSON salah", lambda t: t.replace("kunci auto_critical_alarm_slots",
                                                 "kunci auto_critical_alarm_slots_salah", 1)),
    ]
    keluaran = [f"dasar salinan asli: {lolos} lolos, {gagal} gagal"]
    semua_benar = (gagal == 0)
    for i, (nama, ubah) in enumerate(kasus, start=1):
        teks = ubah(asli)
        p = os.path.join(NEG, f"kasus{i}.md")
        with open(p, "w", encoding="utf-8") as f:
            f.write(teks)
        l, g, _ = jalankan(p, JSONF, f"kasus{i}")
        ditolak = g > 0
        semua_benar = semua_benar and ditolak
        keluaran.append(f"kasus{i} ({nama}): {l} lolos, {g} gagal, ditolak={'ya' if ditolak else 'TIDAK'}")
        print()
    keluaran.append(f"hasil uji negatif: {'semua kasus sesuai harapan' if semua_benar else 'ADA KASUS TIDAK SESUAI'}")
    with open(LAPORAN_NEG, "w", encoding="utf-8") as f:
        f.write("\n".join(keluaran) + "\n")
    print()
    for b in keluaran:
        print(b)
    return 0 if semua_benar else 1


def main():
    if "--negatif" in sys.argv:
        return negatif()
    lolos, gagal, daftar = jalankan(DOC, JSONF, "dokumen")
    if gagal:
        print("GAGAL:", daftar)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
