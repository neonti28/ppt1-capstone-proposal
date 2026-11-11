#!/usr/bin/env python3
"""Gerbang gaya naskah. Menolak tiga jenis kalimat yang tidak menambah isi:

1. meta   : kalimat yang mengatur cara menulis atau menilai kalimat lain
            (kalimat yang sah, tidak boleh ditulis, dapat diklaim, keabsahan).
2. diri   : kata ganti penulis dan jejak proses kerja (saya, kami, penulis,
            sudah saya, pada revisi ini, versi ini, dokumen ini).
3. retorik: perbandingan yang menghias, bukan membandingkan data
            (bukan X melainkan Y, justru, padahal, sebaliknya, alih-alih).

Baris tabel dan butir bukti tidak diperiksa untuk pola retorik, karena di sana
kontras sering menyatakan keadaan data yang sebenarnya.

Pakai: python3 tools/periksa_gaya.py [--detail=meta|diri|retorik] [--pasang]
  --pasang : tulis hitungan sekarang sebagai batas. Commit ditolak bila salah
             satu kelas bertambah di atas batas.
Kode keluar 1 bila melewati batas.
"""
import json
import pathlib
import re
import sys

KELAS = {
    "meta": r"kalimat yang sah|kalimat yang boleh|tidak boleh ditulis|dapat diklaim|"
            r"tidak dapat diklaim|dapat dipertanggungjawabkan|dinyatakan terbuka|"
            r"secara akademik|keabsahan|\bklaim yang sah\b",
    "diri": r"\b(saya|kami|penulis)\b|sudah saya|pada revisi ini|di revisi ini|"
            r"\bversi ini\b|\bdraft ini\b|\bdraf ini\b|\bsebelumnya saya\b|"
            r"\bdokumen ini\b|\bnaskah ini\b|\bproposal ini\b",
    "retorik": r"\bbukan [^.\n]{2,60}? melainkan\b|\balih-alih\b|\bjustru\b|"
               r"\bpadahal\b|\bsebaliknya\b|\bnyatanya\b|\btetap saja\b",
}

BASELINE = pathlib.Path(__file__).with_name("gaya_baseline.json")


def hitung(baris):
    hasil = {}
    for nama, pola in KELAS.items():
        kena = []
        for i, b in enumerate(baris):
            if nama == "retorik" and b.lstrip().startswith(("|", "- ", "1.", "2.", "3.")):
                continue
            if re.search(pola, b, flags=re.I):
                kena.append((i + 1, b.strip()))
        hasil[nama] = kena
    return hasil


def main() -> int:
    detail = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--detail=")), None)
    pasang = "--pasang" in sys.argv
    path = pathlib.Path("docs/PPT1_PROPOSAL_FINAL_V2.md")
    baris = path.read_text(encoding="utf-8").split("\n")
    hasil = hitung(baris)
    sekarang = {k: len(v) for k, v in hasil.items()}
    batas = json.loads(BASELINE.read_text()) if BASELINE.exists() else {}

    kode = 0
    for nama in KELAS:
        n = sekarang[nama]
        b = batas.get(nama)
        tanda = "tanpa batas" if b is None else ("NAIK" if n > b else "ok")
        if b is not None and n > b:
            kode = 1
        print(f"{nama:8s} {n:4d}  batas={b}  {tanda}")
        if detail == nama:
            for no, isi in hasil[nama]:
                print(f"  {no:5d}| {isi[:200]}")
    print(f"{'TOTAL':8s} {sum(sekarang.values()):4d} dari {len(baris)} baris")

    if pasang:
        BASELINE.write_text(json.dumps(sekarang, indent=2) + "\n")
        print("batas diperbarui:", sekarang)
        kode = 0
    return kode


if __name__ == "__main__":
    sys.exit(main())
