#!/usr/bin/env python3
"""Pemeriksa independen untuk docs/RND_S2_HYBRID_VIB_SSI.md.

Pemeriksa ini sengaja TIDAK mengimpor s2_common. Ia membaca dokumen sebagai
teks, mengambil sel tabel, lalu menghitung ulang nilainya dari artefak JSON
dengan formatter sendiri. Dengan begitu dokumen tidak bisa lolos hanya karena
generator dan pemeriksa memakai kode yang sama.

Pemeriksa juga menguji dirinya sendiri: satu sel pada salinan dokumen dirusak,
dan pemeriksa wajib melaporkan ketidakcocokan. Bila salinan rusak itu tetap
lolos, hasil pemeriksaan dianggap tidak sah.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile

BASE = "/mnt/d/Capstone 1(v2)"
OUT = f"{BASE}/scratch/rnd/s2"
DOK = f"{BASE}/docs/RND_S2_HYBRID_VIB_SSI.md"
LEDGER = f"{BASE}/docs/RND_PROVENANCE_LEDGER.md"
BUDGET = [12, 24, 48, 96, 192]


def fi(x):
    return f"{int(x):,}".replace(",", ".")


def fd(x, n=4):
    return f"{x:.{n}f}".replace(".", ",")


def baca_tabel(teks):
    """Daftar (header, baris, nomor_baris_awal) untuk semua tabel markdown."""
    out = []
    baris = teks.split("\n")
    i = 0
    while i < len(baris):
        if (baris[i].startswith("| ") and i + 1 < len(baris)
                and re.match(r"^\|[-|]+\|$", baris[i + 1])):
            header = tuple(c.strip() for c in baris[i].strip().strip("|").split(" | "))
            isi = []
            j = i + 2
            while j < len(baris) and baris[j].startswith("|"):
                isi.append([c.strip() for c in baris[j].strip().strip("|").split(" | ")])
                j += 1
            out.append((header, isi, i))
            i = j
        else:
            i += 1
    return out


def kelas_sebelum(teks, idx):
    """Kelas yang disebut paling akhir sebelum baris idx."""
    sebelum = "\n".join(teks.split("\n")[:idx])
    pos_vib = sebelum.rfind("Kelas vib")
    pos_ssi = sebelum.rfind("Kelas ssi")
    if pos_vib < 0 and pos_ssi < 0:
        return None
    return "vib" if pos_vib > pos_ssi else "ssi"


def periksa(path):
    ring = json.load(open(f"{OUT}/s2_ringkas.json"))
    meta = json.load(open(f"{OUT}/s2_meta.json"))
    rec = {k: json.load(open(f"{OUT}/s2_records_{k}.json")) for k in ("vib", "ssi")}
    teks = open(path, encoding="utf-8").read()
    tab = baca_tabel(teks)
    masalah = []
    n = 0

    # 1. bentuk tabel: jumlah sel wajib sama dengan header
    for header, isi, _ in tab:
        for r in isi:
            if len(r) != len(header):
                masalah.append(f"tabel '{header[0]}': baris punya {len(r)} sel, header {len(header)}")

    # 2. tabel jumlah per kelas
    for header, isi, idx in tab:
        if header[0] != "Kelas" or "Baris" not in header or "Fold gugur" not in header:
            continue
        for r in isi:
            k = r[0]
            d = ring[k]
            harap = [k, fi(d["n_baris"]), fi(d["n_well"]), fi(d["n_fitur"]), fi(d["n_fold_total"]),
                     fi(d["n_fold_dapat_diuji"]), fi(d["n_fold_tidak_dapat_diuji"]),
                     fi(d["n_pos_total_dapat_diuji"])]
            for got, exp in zip(r, harap):
                n += 1
                if got != exp:
                    masalah.append(f"tabel 2.1 {k}: '{got}' != '{exp}'")

    # 3. tabel per fold
    peta = {(k, w["fold"]): w for k in ("vib", "ssi") for w in ring[k]["wells"]}
    for header, isi, idx in tab:
        if header[0] != "Fold" or "Kanal gerbang" not in header:
            continue
        kelas = kelas_sebelum(teks, idx)
        for r in isi:
            w = peta.get((kelas, r[0]))
            if w is None:
                masalah.append(f"tabel 2.2: fold {r[0]} tidak ada di JSON kelas {kelas}")
                continue
            harap = [w["fold"], fi(w["n"]), fi(w["n_pos"]), fi(w["menit_kalender"]), w["kanal"],
                     fd(w["auc_kanal"]), fd(w["h_cusum"], 1), fd(w["auprc_ml"]), fd(w["auc_ml"]),
                     "ya" if w["dapat_diuji"] else "tidak"]
            for got, exp in zip(r, harap):
                n += 1
                if got != exp:
                    masalah.append(f"tabel 2.2 {r[0]}: '{got}' != '{exp}'")

    # 4. tabel lapisan A per model
    for header, isi, idx in tab:
        if header[0] != "Model" or "Recall median" not in header:
            continue
        kelas = kelas_sebelum(teks, idx)
        d = ring[kelas]["agregat"]
        for r in isi:
            g = d[r[0]]
            harap = [r[0], fi(g["n_fold"]), fd(g["recall_median"]), fd(g["precision_median"]),
                     fd(g["far24_kalender_median"]), fd(g["far24_baris_median"]),
                     fi(g["fp_total"]), fd(g["cakupan_median"]),
                     f"{g['fold_lolos_far_recall']}/{g['n_fold']}"]
            for got, exp in zip(r, harap):
                n += 1
                if got != exp:
                    masalah.append(f"tabel 4 {kelas}/{r[0]}: '{got}' != '{exp}'")

    # 5. tabel sensitivitas anggaran
    for header, isi, idx in tab:
        if header[0] != "Anggaran":
            continue
        kelas = kelas_sebelum(teks, idx)
        sens = ring[kelas]["sensitivitas"]
        for r in isi:
            b = int(r[0].replace(".", ""))
            ml = sens[f"ML_kalender_b{b}"]
            st_ = sens[f"stat_cusum_b{b}"]
            harap = [fi(b), fd(ml["recall_median"]), fd(ml["precision_median"]),
                     fd(ml["far24_kalender_median"]), fd(st_["recall_median"]),
                     fd(st_["precision_median"]), fd(st_["far24_kalender_median"])]
            for got, exp in zip(r, harap):
                n += 1
                if got != exp:
                    masalah.append(f"tabel 4.3 {kelas} b{b}: '{got}' != '{exp}'")

    # 6. tabel perbandingan hybrid lawan single
    for header, isi, idx in tab:
        if "Single terbaik" not in header:
            continue
        for r in isi:
            b = ring[r[0]]["banding_hybrid_lawan_single"]
            harap = [r[0], b["single"], b["hybrid"], fd(b["delta_recall_median"]),
                     fd(b["delta_precision_median"]), fd(b["rasio_far_median"]),
                     fi(b["delta_fold_lolos"])]
            for got, exp in zip(r, harap):
                n += 1
                if got != exp:
                    masalah.append(f"tabel 5 {r[0]}: '{got}' != '{exp}'")

    # 7. tabel separuh waktu
    for header, isi, idx in tab:
        if "Recall paruh awal" not in header:
            continue
        kelas = kelas_sebelum(teks, idx)
        d = ring[kelas]["lapisan_c_separuh"]
        for r in isi:
            s = d[r[0]]
            harap = [r[0], fd(s["recall_awal_median"]), fd(s["recall_akhir_median"]),
                     f"{s['n_fold_menurun']}/{s['n_fold_banding']}"]
            for got, exp in zip(r, harap):
                n += 1
                if got != exp:
                    masalah.append(f"tabel 6.1 {kelas}/{r[0]}: '{got}' != '{exp}'")

    # 8. tabel variasi seed
    peta_seed = {(k, s["fold"]): s for k in ("vib", "ssi") for s in ring[k]["variasi_seed_ml"]}
    for header, isi, idx in tab:
        if "Selisih FP" not in header:
            continue
        for r in isi:
            s = peta_seed[(r[0], r[1])]
            harap = [r[0], r[1], fi(s["delta_fp"]), fi(s["delta_tp"]), fd(s["delta_recall"])]
            for got, exp in zip(r, harap):
                n += 1
                if got != exp:
                    masalah.append(f"tabel 6.2 {r[0]}/{r[1]}: '{got}' != '{exp}'")

    # 9. klaim narasi yang punya konsekuensi
    n30 = sum(1 for k in ("vib", "ssi") for f in rec[k]["folds"] if f["h_terpilih"] == 30.0)
    n15 = sum(1 for k in ("vib", "ssi") for f in rec[k]["folds"] if f["h_terpilih"] == 15.0)
    total = ring["vib"]["n_fold_total"] + ring["ssi"]["n_fold_total"]
    rasio = ring["vib"]["agregat"]["persistence"]["far24_kalender_median"] / meta["far_maks"]
    for teks_harap, label in [
        (f"{n30} dari {total} fold", "fold tersaturasi h=30"),
        (f"pada 15 di {n15} fold", "fold h=15"),
        (f"{fd(rasio, 2)} kali", "rasio FAR persistence vib terhadap gate"),
    ]:
        n += 1
        if teks_harap not in teks:
            masalah.append(f"narasi: '{teks_harap}' ({label}) tidak ada di dokumen")

    # 10. larangan em-dash dan en-dash
    for ch, nama in (("\u2014", "em-dash"), ("\u2013", "en-dash")):
        n += 1
        if ch in teks:
            masalah.append(f"dokumen memuat {nama} sebanyak {teks.count(ch)}")

    return masalah, n, len(tab)


def periksa_ledger(teks_dok):
    baris = [l for l in open(LEDGER, encoding="utf-8").read().split("\n") if l.startswith("| S2-")]
    masalah = []
    if not baris:
        return ["ledger S2 kosong"], 0
    kode = []
    for l in baris:
        sel = [c.strip() for c in l.strip().strip("|").split(" | ")]
        if len(sel) != 7:
            masalah.append(f"baris {sel[0]} punya {len(sel)} kolom, wajib 7")
            continue
        kode.append(sel[0])
        if sel[1] not in teks_dok:
            masalah.append(f"angka {sel[1]} pada {sel[0]} tidak muncul di dokumen")
    if len(set(kode)) != len(kode):
        masalah.append("ada kode ledger duplikat")
    if kode != [f"S2-{i:03d}" for i in range(1, len(kode) + 1)]:
        masalah.append("penomoran kode ledger tidak berurutan 1..N")

    # arah sebaliknya: token desimal di dokumen wajib punya baris ledger
    angka_ledger = set()
    for l in baris:
        sel = [c.strip() for c in l.strip().strip("|").split(" | ")]
        if len(sel) == 7:
            angka_ledger.add(sel[1])
            angka_ledger.add(sel[1].lstrip("-"))
    token = set(re.findall(r"\d+,\d{2,}", teks_dok)) | set(re.findall(r"\d{1,3}\.\d{3}(?!\d)", teks_dok))
    tanpa_baris = sorted(t for t in token if t not in angka_ledger)
    if tanpa_baris:
        masalah.append(f"token desimal dokumen tanpa baris ledger: {tanpa_baris[:12]}")
    return masalah, len(kode)


def uji_idempoten():
    sha = []
    for _ in range(2):
        subprocess.run([sys.executable, f"{OUT}/s2d_dokumen.py"], check=True,
                       capture_output=True, cwd=OUT)
        sha.append(hashlib.sha256(open(DOK, "rb").read()).hexdigest())
    return sha[0] == sha[1], sha[0]


def uji_bisa_gagal():
    """Rusak satu sel pada salinan dokumen, pemeriksa wajib menangkapnya."""
    tmp = tempfile.mkdtemp()
    salin = f"{tmp}/uji.md"
    teks = open(DOK, encoding="utf-8").read()
    target = "| persistence | 4 | 0,7405 |"
    if target not in teks:
        shutil.rmtree(tmp)
        return False, "sel target tidak ditemukan"
    open(salin, "w", encoding="utf-8").write(teks.replace(target, "| persistence | 4 | 0,7406 |", 1))
    masalah, _, _ = periksa(salin)
    shutil.rmtree(tmp)
    tertangkap = any("persistence" in m and "0,7406" in m for m in masalah)
    return tertangkap, f"{len(masalah)} masalah pada salinan rusak"


def main():
    masalah, n, ntab = periksa(DOK)
    ml, nled = periksa_ledger(open(DOK, encoding="utf-8").read())
    masalah += ml
    print(f"tabel diperiksa: {ntab}, sel dan klaim diperiksa: {n}")
    print(f"baris ledger S2: {nled}")
    ok_idem, sha = uji_idempoten()
    print(f"idempoten: {ok_idem} sha256={sha[:16]}")
    ok_gagal, ket = uji_bisa_gagal()
    print(f"pemeriksa bisa gagal: {ok_gagal} ({ket})")
    if not ok_idem:
        masalah.append("generator dokumen tidak idempoten")
    if not ok_gagal:
        masalah.append("pemeriksa tidak bisa gagal, hasil pemeriksaan tidak sah")
    if masalah:
        print(f"\nGAGAL, {len(masalah)} masalah:")
        for m in masalah[:40]:
            print(" -", m)
        return 1
    print("\nLULUS: seluruh sel tabel cocok dengan JSON, ledger 7 kolom dan tersitir, "
          "idempoten, dan pemeriksa terbukti bisa gagal.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
