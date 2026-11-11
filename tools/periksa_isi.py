#!/usr/bin/env python3
"""Gerbang kepadatan isi. Menolak paragraf yang panjang tanpa satu pun muatan:

  - angka (0-9),
  - rujukan pustaka [n],
  - tabel (|),
  - definisi teknis (pola "adalah", "didefinisikan", "dihitung").

Alasannya: kalimat berguna membawa objek, metode, angka, atau sumber. Kalimat
sampah hampir selalu tidak membawa satu pun, dan panjangnya hanya menutupi itu.
Gerbang ini tidak peduli pilihan kata, jadi tidak bisa diakali dengan sinonim.

Pakai: python3 tools/periksa_isi.py [--detail] [--pasang]
Kode keluar 1 bila jumlah paragraf kosong melewati batas.
"""
import json
import pathlib
import re
import sys

MIN_PANJANG = 320
BASELINE = pathlib.Path(__file__).with_name("isi_baseline.json")
MUTAN = re.compile(r"\d|\[\d+\]|\||\badalah\b|\bdidefinisikan\b|\bdihitung\b|\bdiukur\b", re.I)


def paragraf(baris):
    buf, awal = [], 0
    for i, b in enumerate(baris, 1):
        if b.strip():
            if not buf:
                awal = i
            buf.append(b)
        else:
            if buf:
                yield awal, " ".join(x.strip() for x in buf)
            buf = []
    if buf:
        yield awal, " ".join(x.strip() for x in buf)


def main() -> int:
    detail = "--detail" in sys.argv
    pasang = "--pasang" in sys.argv
    path = pathlib.Path("docs/PPT1_PROPOSAL_FINAL_V2.md")
    baris = path.read_text(encoding="utf-8").split("\n")

    kosong = []
    for no, teks in paragraf(baris):
        if teks.startswith(("#", "```", "!", "---")):
            continue
        if len(teks) < MIN_PANJANG:
            continue
        if not MUTAN.search(teks):
            kosong.append((no, len(teks), teks))

    batas = json.loads(BASELINE.read_text()) if BASELINE.exists() else {}
    b = batas.get("kosong")
    tanda = "tanpa batas" if b is None else ("NAIK" if len(kosong) > b else "ok")
    print(f"paragraf >= {MIN_PANJANG} karakter tanpa angka/rujukan/tabel/definisi: {len(kosong)}  batas={b}  {tanda}")
    if detail:
        for no, n, teks in sorted(kosong, key=lambda x: -x[1])[:15]:
            print(f"  {no:5d} ({n:4d} kar) {teks[:180]}")
    if pasang:
        BASELINE.write_text(json.dumps({"kosong": len(kosong)}, indent=2) + "\n")
        print("batas diperbarui")
        return 0
    return 1 if b is not None and len(kosong) > b else 0


if __name__ == "__main__":
    sys.exit(main())
