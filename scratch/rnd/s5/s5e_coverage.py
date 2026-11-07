#!/usr/bin/env python3
"""Uji klaim 'setiap angka punya baris ledger' secara terukur.

Metode: setiap sel numerik pada tabel dokumen diambil, lalu dicari padanannya di
blok ledger kartu itu. Pencocokan menerima titik atau koma desimal dan pembulatan
4 desimal. Hasilnya fraksi sel tabel yang punya padanan di ledger.
"""
import json
import pathlib
import re

B = pathlib.Path("/mnt/d/Capstone 1(v2)")
F = {"S1": "docs/RND_S1_SEED_ROBUSTNESS.md", "S2": "docs/RND_S2_HYBRID_VIB_SSI.md",
     "S3": "docs/RND_S3_HYBRID_BITWEAR.md", "S4": "docs/RND_S4_LAYER_B_DATA.md"}
LED = (B / "docs/RND_PROVENANCE_LEDGER.md").read_text(encoding="utf-8")


def blok(kartu):
    aktif, buf = False, []
    for l in LED.splitlines():
        if l.startswith("## Bagian"):
            aktif = bool(re.search(r"Bagian %s\b" % kartu, l))
            continue
        if aktif:
            buf.append(l)
    return "\n".join(buf)


def kandidat(tok):
    """Semua tafsir wajar satu token angka: titik bisa desimal atau pemisah ribuan."""
    tok = tok.rstrip(".,")
    out = set()
    try:
        if "," in tok and "." in tok:
            out.add(round(abs(float(tok.replace(".", "").replace(",", "."))), 4))
        elif "," in tok:
            out.add(round(abs(float(tok.replace(",", "."))), 4))
            out.add(round(abs(float(tok.replace(",", ""))), 4))
        elif re.fullmatch(r"\d{1,3}(?:\.\d{3})+", tok):
            out.add(round(abs(float(tok.replace(".", ""))), 4))
            out.add(round(abs(float(tok)), 4))
        else:
            out.add(round(abs(float(tok)), 4))
    except ValueError:
        pass
    return out


def angka_ledger(teks):
    out = set()
    for tok in re.findall(r"\d[\d.,]*", teks):
        out |= kandidat(tok)
    return out


def sel_tabel(teks):
    """Kembalikan daftar himpunan kandidat, satu himpunan per sel angka."""
    out = []
    for l in teks.splitlines():
        if not l.strip().startswith("|"):
            continue
        for c in l.strip().strip("|").split("|"):
            c = c.strip().strip("*` ")
            if re.fullmatch(r"-?\d+(?:[.,]\d+)?", c):
                k = kandidat(c)
                if k:
                    out.append((c, k))
    return out


hasil = {}
for k, rel in F.items():
    teks = (B / rel).read_text(encoding="utf-8")
    sel = sel_tabel(teks)
    led = angka_ledger(blok(k))
    ada = 0
    hilang_contoh = []
    for asli, kand in sel:
        cocok = any(any(abs(v - x) <= 0.5 * 10 ** (-4) + 1e-9 or abs(v - x) <= 0.5 * 10 ** (-2) + 1e-9
                        for x in led) for v in kand)
        if cocok:
            ada += 1
        elif len(hilang_contoh) < 8:
            hilang_contoh.append(asli)
    hasil[k] = dict(sel_tabel=len(sel), ada_di_ledger=ada,
                    fraksi=round(ada / len(sel), 4) if sel else None,
                    contoh_tanpa_padanan=hilang_contoh,
                    angka_unik_ledger=len(led))
    print(k, hasil[k])

(B / "scratch/rnd/s5/s5_coverage.json").write_text(json.dumps(hasil, indent=1, ensure_ascii=False),
                                                   encoding="utf-8")
print("WROTE scratch/rnd/s5/s5_coverage.json")
