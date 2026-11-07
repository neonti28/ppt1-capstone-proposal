"""Verifikasi klaim bagian 2.4: isi fitur, keberadaan vib dan crpm."""
import sys

import pandas as pd

BASE = "/mnt/d/Capstone 1(v2)"
sys.path.insert(0, f"{BASE}/code")
import rnd_hybrid_harness as H  # noqa: E402

b = pd.read_csv(f"{H.BINSD}/F-14.csv.gz")
print("kolom bins F-14:", list(b.columns))
for nama in ("vib", "vib_max", "crpm", "TQA", "SPPA", "TFLO", "RPM", "SWOB", "HKLD", "ROP",
             "BPOS", "spm", "depth", "dbtm"):
    print(f"  bins {nama}: {'ADA' if nama in b.columns else 'tidak ada'}")

for kelas in ("vib", "ssi"):
    df = H.muat_dataset(f"{H.DSD}/{kelas}.csv.gz")
    feats = H.fitur_dari(df)
    print(f"\nkelas {kelas}: {len(feats)} fitur, {len(df.columns)} kolom")
    print("  vib di fitur:", "vib" in feats, "| vib_max di fitur:", "vib_max" in feats,
          "| crpm di fitur:", "crpm" in feats)
    print("  daftar fitur:", feats)
