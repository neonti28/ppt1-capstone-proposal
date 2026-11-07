"""Rapikan istilah: mode kegagalan vs detektor vs engine.

Tiga makna yang dipisahkan:
1. MODE KEGAGALAN (vib, ssi, shk, stuck, hyd, bit_wear, tool_wear, dan hitungannya)
   -> 'mode ...'
2. PELAKSANA DETEKSI (implementasi rule/persistence/model yang menjalankan satu mode,
   misalnya 'engine lama', 'engine utama', 'engine layak pakai', 'engine ini')
   -> 'detektor ...'
3. ALGORITMA / MESIN (AutoML, rule engine, engine ML, engine Random Forest)
   -> tetap 'engine'

Jalankan: python3 rename_tiga_arah.py          (dry run, tampilkan perubahan)
          python3 rename_tiga_arah.py --tulis  (terapkan)
"""
import argparse
import glob
import pathlib
import re

D = pathlib.Path("/mnt/d/ARCT-9F2/docs")
TARGET = [f for f in sorted(glob.glob(str(D / "PPT1_*.md"))) + sorted(glob.glob(str(D / "RND_*.md")))
          if "PROPOSAL_FINAL" not in f]

# --- makna 3: tetap engine (algoritma / mesin) -------------------------------
TETAP = [
    r"engines? pencarian otomatis", r"pencarian hyperparameter otomatis",
    r"engine ML\b", r"\bML engine", r"rule engine", r"persistence/rule engine",
    r"engine (?:Random Forest|XGBoost|LightGBM|CatBoost|boosting|SVM|H2O)\b",
    r"adalah engine itu", r"dipakai sebagai engine", r"engine kebal", r"bukan pada engine",
]
TETAP_RE = re.compile("|".join(TETAP), re.I)

# --- makna 1: mode kegagalan -------------------------------------------------
MODE = [
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
    (re.compile(r"\b(\d+)\s+dari\s+(\d+)\s+engine\b", re.I), r"\1 dari \2 mode"),
    (re.compile(r"^\| *Engine *\|"), "| Mode |"),
    (re.compile(r"\| Engine \|"), "| Mode |"),
]
# --- makna 2: pelaksana deteksi ---------------------------------------------
DETEKTOR = [
    (re.compile(r"\bEngine lama\b"), "Detektor lama"),
    (re.compile(r"\bengine lama\b"), "detektor lama"),
    (re.compile(r"\bEngine\b"), "Detektor"),
    (re.compile(r"\bengine\b"), "detektor"),
]
KHUSUS = [
    (re.compile(r"Engine boleh rule based, statistical, persistence"),
     "Detektor boleh rule based, statistical, persistence"),
    (re.compile(r"RF tuned sebagai engine utama"), "Random Forest sebagai detektor utama"),
    (re.compile(r"engine yang labelnya tersedia"), "detektor yang labelnya tersedia"),
]


def ganti_baris(baris):
    if not re.search(r"engine", baris, re.I):
        return baris, 0
    baru, n = baris, 0
    for pola, g in KHUSUS + MODE:
        baru, k = pola.subn(g, baru)
        n += k
    # sisa 'engine' yang bukan makna algoritma -> detektor
    def _sub(m):
        nonlocal n
        potong = baru[max(0, m.start() - 30):m.end() + 30]
        if TETAP_RE.search(potong):
            return m.group(0)
        n += 1
        return "Detektor" if m.group(0)[0].isupper() else "detektor"

    baru = re.sub(r"\bengine\b", _sub, baru, flags=re.I)
    return baru, n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tulis", action="store_true")
    a = ap.parse_args()
    total = 0
    for f in TARGET:
        p = pathlib.Path(f)
        baris = p.read_text().split("\n")
        baru, log, n = [], [], 0
        for i, b in enumerate(baris, 1):
            nb, k = ganti_baris(b)
            if k and nb != b:
                log.append((i, b, nb)); n += k
            baru.append(nb)
        if n:
            total += n
            print(f"\n=== {p.name} ({n})")
            for i, b, nb in log:
                print(f"  {i}: {b.strip()[:150]}\n   -> {nb.strip()[:150]}")
        if n and a.tulis:
            p.write_text("\n".join(baru))
    print(f"\nTOTAL: {total} | tulis: {a.tulis}")


if __name__ == "__main__":
    main()
