"""Pemeriksaan klaim data yang dipakai dokumen S2: kolom dataset dan konstanta 1 g."""
import glob
import json
import os

BASE = "/mnt/d/Capstone 1(v2)"
print("1 g dalam ft/s2 =", round(9.80665 / 0.3048, 5))

meta = json.load(open(f"{BASE}/scratch/rnd/s2/s2_meta.json"))
print("kanal gerbang yang tersedia di meta:", meta["kanal"])

# cari dataset yang dipakai harness
kandidat = sorted(glob.glob(f"{BASE}/scratch/v9_d1/datasets/*.parquet")) or \
           sorted(glob.glob(f"{BASE}/scratch/**/*.parquet", recursive=True))
print("jumlah parquet:", len(kandidat))
for p in kandidat[:6]:
    print(" -", os.path.relpath(p, BASE), round(os.path.getsize(p) / 1e6, 1), "MB")

if kandidat:
    import pandas as pd
    p = kandidat[0]
    kol = pd.read_parquet(p).columns.tolist()
    print("\nberkas:", os.path.relpath(p, BASE))
    print("jumlah kolom:", len(kol))
    for nama in ("vib", "vib_max", "crpm", "TQA", "SPPA", "TFLO", "RPM", "SWOB", "HKLD",
                 "ROP", "BPOS", "spm", "depth", "dbtm"):
        print(f"  {nama}: {'ADA' if nama in kol else 'tidak ada'}")
    print("kolom lengkap:", kol)
