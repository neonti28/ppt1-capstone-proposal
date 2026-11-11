#!/usr/bin/env python3
"""Entitas yang tidak boleh muncul di badan naskah, tanpa kecuali.

Hanya empat pola, karena hanya empat ini yang tidak punya pemakaian sah di
dalam naskah akademik:

  1. rujukan ke buku pedoman internal (pedoman, Buku Pedoman),
  2. perintah shell (python3, bash, git),
  3. path berkas di dalam tanda kutip terbalik,
  4. nama penulis sebagai kata ganti orang pertama.

Kata "rubrik", "asumsi", dan "saya" TIDAK dimasukkan, meskipun muncul pada
audit. Alasannya terukur, bukan selera: "rubrik" dipakai sebagai instrumen
penilaian kriteria C1 sampai C9, dan "saya" muncul di dalam user story yang
justru diwajibkan. Melarangnya akan menghapus isi yang harus ada.

Pakai: python3 tools/periksa_entitas.py [--detail]
Kode keluar 1 bila ada temuan.
"""
import pathlib
import re
import sys

POLA = {
    "pedoman": r"\bpedoman\b|buku pedoman",
    "perintah": r"\bpython3\b|\bbash\b|\bgit (add|commit|push)\b",
    "path": r"`[^`]*(/|\.(py|json|csv|md|xlsx|sh))\b[^`]*`",
    "kata-ganti": r"\b(saya|kami)\b",
}


def main() -> int:
    detail = "--detail" in sys.argv
    path = pathlib.Path("docs/PPT1_PROPOSAL_FINAL_V2.md")
    baris = path.read_text(encoding="utf-8").split("\n")
    total = 0
    for nama, pola in POLA.items():
        kena = [(i + 1, b.strip()) for i, b in enumerate(baris) if re.search(pola, b, flags=re.I)]
        total += len(kena)
        print(f"{nama:12s} {len(kena):4d}")
        if detail:
            for no, isi in kena:
                print(f"  {no:5d}| {isi[:160]}")
    print(f"{'TOTAL':12s} {total:4d} dari {len(baris)} baris")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
