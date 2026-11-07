#!/usr/bin/env python3
"""Sumber tunggal angka S2 untuk generator dokumen dan generator ledger.

Dokumen dan ledger sama-sama membaca dari modul ini, sehingga angka di keduanya
tidak mungkin berbeda. Setiap entri ledger membawa path JSON persisnya dan
di-assert terhadap isi JSON saat dibangkitkan.
"""
from __future__ import annotations

import json

BASE = "/mnt/d/Capstone 1(v2)"
OUT = f"{BASE}/scratch/rnd/s2"
TANGGAL = "2026-10-28"

MODEL_SINGLE = ["persistence", "rule_kanal", "stat_cusum", "ML_conformal", "ML_kalender"]
MODEL_HYBRID = ["H1_stat_dan_rule", "H1b_stat_atau_rule", "H2_ML_kalender_dan_stat",
                "H2b_ML_kalender_atau_stat", "H3_ML_kalender_dan_rule"]
MODEL_SEMUA = MODEL_SINGLE + MODEL_HYBRID + ["ML_conformal_seed13"]
BUDGET = (12, 24, 48, 96, 192)

LABEL_MODEL = {
    "persistence": "Persistence (y_prev, baseline per tugas dari data)",
    "rule_kanal": "Rule kanal (gerbang nilai mutlak z kanal)",
    "stat_cusum": "Statistik CUSUM pada z kanal",
    "ML_conformal": "ML LightGBM, ambang conformal",
    "ML_kalender": "ML LightGBM, ambang anggaran kalender",
    "H1_stat_dan_rule": "H1 statistik DAN rule",
    "H1b_stat_atau_rule": "H1b statistik ATAU rule",
    "H2_ML_kalender_dan_stat": "H2 ML DAN statistik",
    "H2b_ML_kalender_atau_stat": "H2b ML ATAU statistik",
    "H3_ML_kalender_dan_rule": "H3 ML DAN rule",
    "ML_conformal_seed13": "ML conformal seed 13 (uji ketahanan)",
}


def muat():
    rec = {k: json.load(open(f"{OUT}/s2_records_{k}.json")) for k in ("vib", "ssi")}
    ring = json.load(open(f"{OUT}/s2_ringkas.json"))
    meta = json.load(open(f"{OUT}/s2_meta.json"))
    return rec, ring, meta


def fi(x):
    """Bilangan bulat dengan pemisah ribuan titik."""
    return f"{int(x):,}".replace(",", ".")


def fd(x, n=4):
    """Desimal dengan koma, n digit."""
    if x is None:
        return "tidak terukur"
    return f"{float(x):.{n}f}".replace(".", ",")


class Ledger:
    """Pembangun baris ledger dengan penomoran otomatis dan assert ke JSON."""

    def __init__(self):
        self.baris = []

    def tambah(self, angka, satuan, kelas, rujukan, dipakai, status="TERUKUR"):
        kode = f"S2-{len(self.baris) + 1:03d}"
        self.baris.append(dict(kode=kode, angka=str(angka), satuan=satuan, kelas=kelas,
                               rujukan=rujukan, dipakai=dipakai, status=status))
        return kode

    def angka_dari(self, nilai, jalur, satuan, kelas, dipakai, bulat=False, digit=4):
        """Ambil nilai dari jalur 'a.b.0.c' pada dict hasil muat, assert ada, lalu catat."""
        v = resolve(nilai, jalur)
        teks = fi(v) if bulat else fd(v, digit)
        return self.tambah(teks, satuan, kelas, f"`{jalur}`", dipakai)

    def markdown(self):
        out = ["| No | Angka | Satuan | Kelas sumber | Rujukan persis | Dipakai di | Status |",
               "|---|---|---|---|---|---|---|"]
        for b in self.baris:
            out.append(f"| {b['kode']} | {b['angka']} | {b['satuan']} | {b['kelas']} | "
                       f"{b['rujukan']} | {b['dipakai']} | {b['status']} |")
        return "\n".join(out)


def resolve(obj, jalur):
    """Resolusi jalur bertitik, mendukung indeks list dan kunci bertitik."""
    cur = obj
    for bagian in jalur.split("."):
        if isinstance(cur, list):
            cur = cur[int(bagian)]
        else:
            if bagian not in cur:
                raise KeyError(f"jalur tidak ada: {jalur} (gagal di '{bagian}')")
            cur = cur[bagian]
    if cur is None:
        raise ValueError(f"nilai None pada jalur {jalur}")
    return cur
