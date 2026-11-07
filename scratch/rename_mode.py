"""Ganti istilah 'engine' (yang menunjuk mode kegagalan) menjadi 'mode kegagalan'/'mode <kode>'.

Yang DIPERTAHANKAN sebagai 'engine':
- 'engine pencarian otomatis', 'engine pencarian hyperparameter otomatis' (AutoML, makna algoritma)
- 'engine ML', 'ML engine', 'rule engine', 'persistence/rule engine'
- 'adalah engine itu', 'dipakai sebagai engine', 'engine kebal' (makna pelaksana metode)

Semua kemunculan lain dianggap mode kegagalan dan diganti.
Jalankan: python rename_mode.py --cek (dry run) | --tulis
"""
import argparse
import glob
import pathlib
import re

D = pathlib.Path("/mnt/d/ARCT-9F2/docs")
TARGET = [f for f in sorted(glob.glob(str(D / "PPT1_*.md"))) + sorted(glob.glob(str(D / "RND_*.md")))
          if "PROPOSAL_FINAL" not in f]

JAGA = [
    r"engine pencarian otomatis",
    r"engine pencarian hyperparameter otomatis",
    r"engine ML\b",
    r"\bML engine\b",
    r"rule engine",
    r"persistence/rule engine",
    r"adalah engine itu",
    r"dipakai sebagai engine",
    r"engine kebal",
]
JAGA_RE = re.compile("|".join(JAGA), re.I)

# (pola, pengganti) dijalankan berurutan; hanya pada teks yang tidak masuk JAGA
ATURAN = [
    (re.compile(r"\bEngine sasaran\b"), "Mode sasaran"),
    (re.compile(r"\bengine sasaran\b"), "mode sasaran"),
    (re.compile(r"\bEngine / klaim\b"), "Mode / klaim"),
    (re.compile(r"\bengine (vib|ssi|shk|stuck|hyd|bit_wear|tool_wear)\b", re.I),
     lambda m: "mode " + m.group(1).lower()),
    (re.compile(r"\bengine (hidraulik|getaran|stick-slip|keausan|tren|status)\b", re.I),
     lambda m: "mode " + m.group(1).lower()),
    (re.compile(r"\bper engine\b"), "per mode"),
    (re.compile(r"\bantar engine\b"), "antar mode"),
    (re.compile(r"\btiap engine\b", re.I), "tiap mode"),
    (re.compile(r"\bsatu engine\b", re.I), "satu mode"),
    (re.compile(r"\b(\d+)\s*(?:x|×)\s*engine\b", re.I), r"\1 mode"),
    (re.compile(r"\b(\d+)\s+engine\b", re.I), r"\1 mode"),
    (re.compile(r"\bEngine\b"), "Mode"),
    (re.compile(r"\bengine\b"), "mode"),
]
# baris khusus yang maknanya 'detektor/modul', bukan mode
KHUSUS = [
    (re.compile(r"Engine boleh rule based, statistical, persistence"), "Detektor boleh rule based, statistical, persistence"),
    (re.compile(r"engine masih berguna untuk onset"), "detektor masih berguna untuk onset"),
    (re.compile(r"B1 engine pada data ini"), "B1 detektor pada data ini"),
]


def ganti_teks(teks):
    """Ganti satu baris; kembalikan (baris_baru, jumlah)."""
    if JAGA_RE.search(teks):
        # baris masih mungkin memuat 'engine' bermakna mode di bagian lain;
        # aman: hanya ganti frasa yang eksplisit menyebut kode mode
        baru = teks
        n = 0
        for pola, ganti in ATURAN[:5]:
            baru, k = pola.subn(ganti, baru)
            n += k
        return baru, n
    baru, n = teks, 0
    for pola, ganti in KHUSUS + ATURAN:
        baru, k = pola.subn(ganti, baru)
        n += k
    return baru, n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tulis", action="store_true")
    a = ap.parse_args()
    total = 0
    for f in TARGET:
        p = pathlib.Path(f)
        lama = p.read_text()
        baris = lama.split("\n")
        baru, log, n = [], [], 0
        for i, b in enumerate(baris, 1):
            nb, k = ganti_teks(b)
            if k and nb != b:
                log.append((i, b, nb))
                n += k
            baru.append(nb)
        if n:
            total += n
            print(f"\n=== {p.name}  ({n} penggantian)")
            for i, b, nb in log[:6]:
                print(f"  {i}: {b.strip()[:120]}")
                print(f"     -> {nb.strip()[:120]}")
            if len(log) > 6:
                print(f"  ... {len(log)-6} baris lain")
            if a.tulis:
                p.write_text("\n".join(baru))
    print(f"\nTOTAL penggantian: {total} | mode tulis: {a.tulis}")


if __name__ == "__main__":
    main()
