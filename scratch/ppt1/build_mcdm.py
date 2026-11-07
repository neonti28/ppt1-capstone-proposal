"""Mesin perhitungan BAB III 3.4: TOPSIS, SAW, sensitivitas, dan hitung ulang draft lama.

Jalankan dari akar repo:
    python3 scratch/ppt1/build_mcdm.py

Masukan : scratch/ppt1/mcdm_data.py
Keluaran: scratch/ppt1/mcdm.json
"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mcdm_data as D

AKAR = "/mnt/d/Capstone 1(v2)"
KRIT = [k["id"] for k in D.KRITERIA]
BY_ID = {k["id"]: k for k in D.KRITERIA}
ALT = [a for a, _ in D.ALTERNATIF]
NAMA_ALT = dict(D.ALTERNATIF)


# ---------------------------------------------------------------------------
# Bobot Rank-Order Centroid
# ---------------------------------------------------------------------------
def roc_weights(peringkat):
    """ROC: w_i = (1/n) * sum_{k=i..n} 1/k untuk peringkat i (1 = paling penting)."""
    n = len(peringkat)
    urut = sorted(peringkat, key=lambda c: peringkat[c])
    w = {}
    for pos, c in enumerate(urut, start=1):
        w[c] = sum(1.0 / k for k in range(pos, n + 1)) / n
    return w


PERINGKAT = {k["id"]: k["peringkat"] for k in D.KRITERIA}
BOBOT_DASAR = roc_weights(PERINGKAT)


def norm(w):
    s = sum(w.values())
    return {k: v / s for k, v in w.items()}


# ---------------------------------------------------------------------------
# Fungsi nilai: unit mentah menjadi skala 0 sampai 100
# ---------------------------------------------------------------------------
def nilai_c1(unit):
    return D.RUBRIK_C1[unit]


def nilai_c2(unit):
    return min(100.0, 100.0 * float(unit) / D.AMBANG_FOLD)


def nilai_c3(unit):
    return D.RUBRIK_C3[unit]


def nilai_c4(unit):
    return 100.0 if int(unit) == 0 else 0.0


def nilai_c5(unit):
    return 100.0 / (1.0 + float(unit))


def nilai_c6(unit):
    v = 100.0 * (D.MINGGU_TERSEDIA - float(unit)) / D.MINGGU_TERSEDIA
    return max(0.0, min(100.0, v))


def nilai_c7(unit):
    berjejak, total = unit
    return 100.0 * float(berjejak) / float(total)


def nilai_c8(unit):
    return D.RUBRIK_C8[int(unit)]


FUNGSI = {
    "C1": nilai_c1, "C2": nilai_c2, "C3": nilai_c3, "C4": nilai_c4,
    "C5": nilai_c5, "C6": nilai_c6, "C7": nilai_c7, "C8": nilai_c8,
}


def hitung_sel():
    sel = {}
    for s in D.SEL:
        kunci = (s["alt"], s["c"])
        assert kunci not in sel, f"sel ganda {kunci}"
        sel[kunci] = dict(s)
        sel[kunci]["nilai"] = round(FUNGSI[s["c"]](s["unit"]), 6)
    # kelengkapan 9 x 8
    kurang = [f"{a}/{c}" for a in ALT for c in KRIT if (a, c) not in sel]
    assert not kurang, f"sel belum lengkap: {kurang}"
    return sel


# ---------------------------------------------------------------------------
# TOPSIS dan SAW
# ---------------------------------------------------------------------------
def matriks_nilai(sel, ubah=None):
    M = {}
    for a in ALT:
        for c in KRIT:
            v = sel[(a, c)]["nilai"]
            if ubah and (a, c) in ubah:
                v = ubah[(a, c)]
            M[(a, c)] = v
    return M


def topsis(M, bobot):
    # normalisasi vektor
    bagi = {}
    for c in KRIT:
        bagi[c] = math.sqrt(sum(M[(a, c)] ** 2 for a in ALT))
    V = {}
    for a in ALT:
        for c in KRIT:
            V[(a, c)] = bobot[c] * (M[(a, c)] / bagi[c])
    ideal_plus = {c: max(V[(a, c)] for a in ALT) for c in KRIT}
    ideal_min = {c: min(V[(a, c)] for a in ALT) for c in KRIT}
    hasil = {}
    for a in ALT:
        dp = math.sqrt(sum((V[(a, c)] - ideal_plus[c]) ** 2 for c in KRIT))
        dm = math.sqrt(sum((V[(a, c)] - ideal_min[c]) ** 2 for c in KRIT))
        ccoef = dm / (dp + dm) if (dp + dm) > 0 else 0.0
        hasil[a] = {"D_plus": round(dp, 6), "D_minus": round(dm, 6),
                    "C": round(ccoef, 6), "V": {c: round(V[(a, c)], 6) for c in KRIT}}
    peringkat = sorted(ALT, key=lambda a: -hasil[a]["C"])
    for i, a in enumerate(peringkat, start=1):
        hasil[a]["peringkat"] = i
    return {"sel": hasil, "peringkat": peringkat,
            "ideal_plus": {c: round(ideal_plus[c], 6) for c in KRIT},
            "ideal_min": {c: round(ideal_min[c], 6) for c in KRIT},
            "bagi": {c: round(bagi[c], 6) for c in KRIT}}


def saw(M, bobot):
    bagi = {c: math.sqrt(sum(M[(a, c)] ** 2 for a in ALT)) for c in KRIT}
    skor = {}
    for a in ALT:
        skor[a] = round(sum(bobot[c] * M[(a, c)] / bagi[c] for c in KRIT), 6)
    peringkat = sorted(ALT, key=lambda a: -skor[a])
    return {"skor": skor, "peringkat": peringkat}


def kendall_tau(p, q):
    """Kendall tau untuk dua urutan tanpa nilai seri (seluruh C berbeda)."""
    n = len(p)
    pos_q = {a: i for i, a in enumerate(q)}
    konkordan = diskordan = 0
    for i in range(n):
        for j in range(i + 1, n):
            selisih = pos_q[p[i]] - pos_q[p[j]]
            if selisih < 0:
                konkordan += 1
            elif selisih > 0:
                diskordan += 1
    total = konkordan + diskordan
    return round((konkordan - diskordan) / total, 6) if total else 0.0


# ---------------------------------------------------------------------------
# Skenario bobot
# ---------------------------------------------------------------------------
def bobot_skenario(sk, sel):
    """Kembalikan (bobot, ubah_skor)."""
    ubah = None
    if sk["id"] == "P0":
        w = dict(BOBOT_DASAR)
    elif sk["id"] == "P1":
        w = {c: 1.0 / len(KRIT) for c in KRIT}
    elif sk["id"] == "P2":
        w = _kunci({"C1": 0.55})
    elif sk["id"] == "P3":
        w = _kunci({"C2": 0.35, "C7": 0.25})
    elif sk["id"] == "P4":
        w = _kunci({"C5": 0.30, "C6": 0.30})
    elif sk["id"] == "P5":
        w = dict(BOBOT_DASAR)
        ubah = {}
        for a in ALT:
            if sel[(a, "C1")]["unit"] == "L20":
                ubah[(a, "C1")] = 50.0
        ubah[("A7", "C1")] = 60.0
    elif sk["id"] == "P6":
        # C4 dan C7 adalah kolom tanpa variasi, sehingga diperlakukan sebagai
        # saringan lulus atau gagal, bukan sebagai bobot.
        penyaring = {"C4", "C7"}
        w = {c: (0.0 if c in penyaring else BOBOT_DASAR[c]) for c in KRIT}
    elif sk["id"] == "P7":
        # C8 belum tervalidasi (3.3.6 butir 8: antarmuka belum dirancang).
        w = _kunci({"C8": 0.0})
    elif sk["id"] == "P8":
        w = _kunci({"C3": 0.30})
    else:
        raise ValueError(sk["id"])
    return norm(w), ubah


def _kunci(terkunci):
    """Kunci beberapa bobot, sisa dibagi proporsional dari bobot dasar."""
    sisa = 1.0 - sum(terkunci.values())
    lain = [c for c in KRIT if c not in terkunci]
    dasar_lain = sum(BOBOT_DASAR[c] for c in lain)
    w = dict(terkunci)
    for c in lain:
        w[c] = sisa * BOBOT_DASAR[c] / dasar_lain
    return w


# ---------------------------------------------------------------------------
# Hitung ulang draft lama
# ---------------------------------------------------------------------------
def hitung_draft_lama():
    b = D.DRAFT_LAMA["bobot"]
    baris = []
    for al in D.DRAFT_LAMA["alternatif"]:
        ws = sum(w * s for w, s in zip(b, al["skor"]))
        baris.append({
            "nama": al["nama"], "skor": al["skor"],
            "total_tertulis": al["total_tertulis"],
            "jumlah_berbobot_hitung": round(ws, 6),
            "selisih": round(ws - al["total_tertulis"], 6),
            "reproduksi": abs(ws - al["total_tertulis"]) < 0.005,
        })
    # TOPSIS sejati pada matriks draft lama (enam kriteria, semua benefit karena
    # skor biaya sudah dibalik pada draft: biaya murah dinilai tinggi)
    M = {}
    for al in D.DRAFT_LAMA["alternatif"]:
        for i, s in enumerate(al["skor"]):
            M[(al["nama"], f"K{i+1}")] = float(s)
    kk = [f"K{i+1}" for i in range(len(b))]
    bagi = {c: math.sqrt(sum(M[(al["nama"], c)] ** 2 for al in D.DRAFT_LAMA["alternatif"])) for c in kk}
    V = {(al["nama"], c): b[i] * M[(al["nama"], c)] / bagi[c]
         for al in D.DRAFT_LAMA["alternatif"] for i, c in enumerate(kk)}
    ip = {c: max(V[(al["nama"], c)] for al in D.DRAFT_LAMA["alternatif"]) for c in kk}
    im = {c: min(V[(al["nama"], c)] for al in D.DRAFT_LAMA["alternatif"]) for c in kk}
    tops = []
    for al in D.DRAFT_LAMA["alternatif"]:
        dp = math.sqrt(sum((V[(al["nama"], c)] - ip[c]) ** 2 for c in kk))
        dm = math.sqrt(sum((V[(al["nama"], c)] - im[c]) ** 2 for c in kk))
        tops.append({"nama": al["nama"], "D_plus": round(dp, 6), "D_minus": round(dm, 6),
                     "C": round(dm / (dp + dm), 6)})
    tops.sort(key=lambda x: -x["C"])
    for i, t in enumerate(tops, start=1):
        t["peringkat"] = i
    gagal = [r["nama"] for r in baris if not r["reproduksi"]]
    return {"bobot": b, "jumlah_kriteria": len(b), "baris": baris,
            "baris_tidak_reproduksi": gagal,
            "jumlah_tidak_reproduksi": len(gagal),
            "topsis_sejati": tops,
            "catatan_skala": D.DRAFT_LAMA["skala"]}


# ---------------------------------------------------------------------------
# Sensitivitas
# ---------------------------------------------------------------------------
def sensitivitas(M, sel):
    skenario = []
    for sk in D.SKENARIO:
        w, ubah = bobot_skenario(sk, sel)
        Mt = matriks_nilai(sel, ubah)
        t = topsis(Mt, w)
        skenario.append({
            "id": sk["id"], "nama": sk["nama"], "jenis": sk["jenis"],
            "catatan": sk["catatan"],
            "bobot": {c: round(w[c], 6) for c in KRIT},
            "peringkat": t["peringkat"],
            "juara": t["peringkat"][0],
            "tiga_besar": t["peringkat"][:3],
            "C": {a: t["sel"][a]["C"] for a in ALT},
        })

    # korelasi peringkat tiap skenario terhadap skenario dasar
    dasar_peringkat = skenario[0]["peringkat"]
    for sk in skenario:
        sk["tau_vs_dasar"] = kendall_tau(sk["peringkat"], dasar_peringkat)

    # one-at-a-time: tiap bobot dikali 1,5 dan 0,5 lalu dinormalkan
    oat = []
    dasar_juara = skenario[0]["juara"]
    for c in KRIT:
        for f, label in ((1.5, "naik 50 persen"), (0.5, "turun 50 persen")):
            w = dict(BOBOT_DASAR)
            w[c] = w[c] * f
            w = norm(w)
            t = topsis(M, w)
            oat.append({
                "kriteria": c, "arah": label, "aturan": "bobot dasar dikali 1,5 atau 0,5 lalu dinormalkan",
                "bobot_baru": round(w[c], 6),
                "juara": t["peringkat"][0],
                "berubah": t["peringkat"][0] != dasar_juara,
                "peringkat": t["peringkat"],
            })

    # titik balik: sapu bobot C1 dari 0 sampai 0,90 pada dua arah
    sapu = []
    for i in range(0, 181):
        wc1 = round(i * 0.005, 6)
        w = norm(_kunci({"C1": wc1}))
        t = topsis(M, w)
        sapu.append({"bobot_C1_diminta": wc1, "bobot_C1": round(w["C1"], 6),
                     "juara": t["peringkat"][0]})
    # rapatkan menjadi segmen
    segmen = []
    for titik in sapu:
        if not segmen or segmen[-1]["juara"] != titik["juara"]:
            segmen.append({"juara": titik["juara"],
                           "bobot_C1_dari": titik["bobot_C1"],
                           "bobot_C1_sampai": titik["bobot_C1"]})
        else:
            segmen[-1]["bobot_C1_sampai"] = titik["bobot_C1"]
    juara_unik = sorted({s["juara"] for s in sapu})
    titik_balik = None
    if len(segmen) > 1:
        titik_balik = {"segmen": segmen, "juara_unik": juara_unik}

    # stabilitas peringkat pada 6 skenario + 16 uji OAT
    semua = [s["peringkat"] for s in skenario] + [o["peringkat"] for o in oat]
    stab = {}
    for a in ALT:
        stab[a] = {
            "juara": sum(1 for p in semua if p[0] == a),
            "tiga_besar": sum(1 for p in semua if a in p[:3]),
            "peringkat_terburuk": max(p.index(a) + 1 for p in semua),
            "jumlah_kasus": len(semua),
        }
    return {"skenario": skenario, "oat": oat, "sapuan_C1": sapu,
            "titik_balik_C1": titik_balik, "juara_unik_sapuan": juara_unik,
            "stabilitas": stab}


# ---------------------------------------------------------------------------
# Diskriminasi kolom
# ---------------------------------------------------------------------------
def diskriminasi(M, bobot):
    kolom = {}
    for c in KRIT:
        vals = [M[(a, c)] for a in ALT]
        kolom[c] = {
            "min": round(min(vals), 6), "max": round(max(vals), 6),
            "rentang": round(max(vals) - min(vals), 6),
            "membedakan": (max(vals) - min(vals)) > 1e-9,
            "bobot": round(bobot[c], 6),
        }
    tanpa = [c for c in KRIT if not kolom[c]["membedakan"]]
    massa = sum(bobot[c] for c in KRIT if kolom[c]["membedakan"])
    return {"kolom": kolom, "tanpa_variasi": tanpa,
            "massa_bobot_efektif": round(massa, 6),
            "massa_bobot_tanpa_variasi": round(1.0 - massa, 6)}


# ---------------------------------------------------------------------------
def main():
    sel = hitung_sel()
    M = matriks_nilai(sel)
    t = topsis(M, BOBOT_DASAR)
    s = saw(M, BOBOT_DASAR)
    tau_metode = kendall_tau(t["peringkat"], s["peringkat"])
    sens = sensitivitas(M, sel)
    disk = diskriminasi(M, BOBOT_DASAR)
    lama = hitung_draft_lama()

    # pemeriksaan internal
    cek = []
    cek.append(("jumlah sel 9 x 8", len(sel) == 72, f"{len(sel)} sel"))
    cek.append(("jumlah bobot = 1", abs(sum(BOBOT_DASAR.values()) - 1) < 1e-9,
                f"{sum(BOBOT_DASAR.values()):.12f}"))
    cek.append(("jumlah skenario bobot >= 8", len(sens["skenario"]) >= 8,
                f"{len(sens['skenario'])} skenario"))
    cek.append(("jumlah uji OAT = 16", len(sens["oat"]) == 16, f"{len(sens['oat'])} uji"))
    cek.append(("semua C dalam (0,1)", all(0 < t["sel"][a]["C"] < 1 for a in ALT), "ya"))
    cek.append(("TOPSIS dan SAW memberi juara sama", t["peringkat"][0] == s["peringkat"][0],
                f"TOPSIS {t['peringkat'][0]}, SAW {s['peringkat'][0]}"))
    cek.append(("tau metode TOPSIS dan SAW", -1 <= tau_metode <= 1, f"{tau_metode}"))
    cek.append(("seluruh tau skenario dalam rentang", all(-1 <= sk["tau_vs_dasar"] <= 1 for sk in sens["skenario"]),
                f"{len(sens['skenario'])} nilai"))
    cek.append(("aturan urut menutup delapan kriteria",
                sorted(D.ATURAN_URUT.keys()) == sorted(KRIT) and len(D.ATURAN_DEF) == 8,
                f"{len(D.ATURAN_DEF)} aturan, {len(D.ATURAN_URUT)} kriteria"))
    cek.append(("aturan urut konsisten dengan peringkat",
                all(D.ATURAN_URUT[c] == f"R{PERINGKAT[c]}" for c in KRIT),
                "kode aturan sama dengan peringkat"))
    # monotonisitas fungsi nilai
    cek.append(("C2 naik saat fold bertambah", nilai_c2(10) < nilai_c2(20), "ya"))
    cek.append(("C5 turun saat wellbore bertambah", nilai_c5(0) > nilai_c5(2) > nilai_c5(4), "ya"))
    cek.append(("C6 turun saat minggu bertambah", nilai_c6(2) > nilai_c6(5), "ya"))
    gagal = [c[0] for c in cek if not c[1]]

    keluar = {
        "meta": {
            "dokumen": D.DOK, "json": D.JSON_OUT,
            "skrip": "scratch/ppt1/build_mcdm.py",
            "data": "scratch/ppt1/mcdm_data.py",
            "skrip_dokumen": "scratch/ppt1/build_doc_mcdm.py",
            "skrip_pemeriksa": "scratch/ppt1/check_mcdm.py",
            "perintah": "python3 scratch/ppt1/build_mcdm.py",
            "perintah_lengkap": [
                "python3 scratch/ppt1/build_mcdm.py",
                "python3 scratch/ppt1/build_doc_mcdm.py",
                "python3 scratch/ppt1/check_mcdm.py",
                "python3 scratch/ppt1/check_mcdm.py --negatif",
            ],
            "metode_utama": "TOPSIS",
            "metode_pembanding": "SAW",
            "metode_bobot": D.BOBOT_METODE,
            "jumlah_alternatif": len(ALT), "jumlah_kriteria": len(KRIT),
            "jumlah_sel": len(sel),
        },
        "kriteria": D.KRITERIA,
        "bobot": {
            "metode": D.BOBOT_METODE,
            "peringkat": PERINGKAT,
            "nilai": {c: round(BOBOT_DASAR[c], 6) for c in KRIT},
            "jumlah": round(sum(BOBOT_DASAR.values()), 12),
            "rumus": "w_i = (1/n) x jumlah 1/k untuk k = peringkat sampai n",
        },
        "sel": [sel[(a, c)] for a in ALT for c in KRIT],
        "matriks_nilai": {a: {c: sel[(a, c)]["nilai"] for c in KRIT} for a in ALT},
        "topsis": t,
        "saw": s,
        "kendall_topsis_saw": tau_metode,
        "metode_kandidat": D.METODE_KANDIDAT,
        "sitasi": D.SITASI,
        "aturan_urut": D.ATURAN_URUT,
        "aturan_def": D.ATURAN_DEF,
        "peta_draft": D.PETA_DRAFT,
        "diskriminasi": disk,
        "sensitivitas": sens,
        "bukti_kelas": D.BUKTI_KELAS,
        "draft_lama": lama,
        "triangulasi_v7": D.URUTAN_V7,
        "pemeriksaan": [{"butir": c[0], "lolos": c[1], "bukti": c[2]} for c in cek],
        "pemeriksaan_gagal": gagal,
    }
    os.makedirs(os.path.join(AKAR, "scratch/ppt1"), exist_ok=True)
    with open(os.path.join(AKAR, D.JSON_OUT), "w", encoding="utf-8") as f:
        json.dump(keluar, f, ensure_ascii=False, indent=1)

    print("=== BOBOT ROC ===")
    for c in KRIT:
        print(f"  {c} peringkat {PERINGKAT[c]}: {BOBOT_DASAR[c]:.6f}")
    print("  jumlah:", round(sum(BOBOT_DASAR.values()), 12))
    print("\n=== MATRIKS NILAI (0-100) ===")
    print("alt  " + "".join(f"{c:>9}" for c in KRIT))
    for a in ALT:
        print(f"{a:4} " + "".join(f"{M[(a, c)]:9.2f}" for c in KRIT))
    print("\n=== TOPSIS ===")
    for a in t["peringkat"]:
        r = t["sel"][a]
        print(f"  {r['peringkat']}. {a} C={r['C']:.6f} D+={r['D_plus']:.6f} D-={r['D_minus']:.6f}")
    print("\n=== SAW (pembanding) ===")
    for i, a in enumerate(s["peringkat"], 1):
        print(f"  {i}. {a} skor={s['skor'][a]:.6f}")
    print("\n=== DISKRIMINASI ===")
    print("  kolom tanpa variasi:", disk["tanpa_variasi"],
          "massa bobot efektif:", disk["massa_bobot_efektif"])
    print("\n=== SKENARIO ===")
    for sk in sens["skenario"]:
        print(f"  {sk['id']} {sk['nama']:28} juara={sk['juara']} tiga besar={sk['tiga_besar']}")
    print("\n  OAT berubah juara:", sum(1 for o in sens["oat"] if o["berubah"]), "dari", len(sens["oat"]))
    print("  segmen juara pada sapuan C1:", sens["titik_balik_C1"])
    print("  juara pada sapuan C1:", sens["juara_unik_sapuan"])
    print("\n=== STABILITAS (%d kasus) ===" % (len(sens["skenario"]) + len(sens["oat"])))
    for a in ALT:
        st = sens["stabilitas"][a]
        print(f"  {a} juara={st['juara']} top3={st['tiga_besar']} peringkat terburuk={st['peringkat_terburuk']}")
    print("\n=== DRAFT LAMA ===")
    for r in lama["baris"]:
        print(f"  {r['nama']:16} tertulis={r['total_tertulis']:.2f} hitung={r['jumlah_berbobot_hitung']:.2f} "
              f"selisih={r['selisih']:+.2f} reproduksi={r['reproduksi']}")
    print("  TOPSIS sejati draft:", [(x['nama'], x['C'], x['peringkat']) for x in lama["topsis_sejati"]])
    print("\n=== PEMERIKSAAN ===")
    for c in cek:
        print(f"  [{'OK' if c[1] else 'GAGAL'}] {c[0]}: {c[2]}")
    print("\nJSON:", os.path.join(AKAR, D.JSON_OUT))
    if gagal:
        print("GAGAL:", gagal)
        sys.exit(1)


if __name__ == "__main__":
    main()
