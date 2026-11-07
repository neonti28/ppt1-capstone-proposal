#!/usr/bin/env python3
"""
Eksplorasi awal dataset Petrobras 3W — verifikasi struktur & isi.
Jalankan: python 01_explore_3w.py  (pakai venv dengan pandas/pyarrow)
"""
from pathlib import Path
import sys

import pandas as pd

DATASET_ROOT = Path(__file__).resolve().parent.parent / "data" / "3W" / "dataset"


def main():
    print("3W dataset path:", DATASET_ROOT)
    print("exists:", DATASET_ROOT.exists())
    if not DATASET_ROOT.exists():
        sys.exit("Dataset belum ada — clone dulu (data/3W)")

    class_dirs = sorted(
        [p for p in DATASET_ROOT.iterdir() if p.is_dir() and p.name.isdigit()]
    )
    print(f"\nFolder kelas ditemukan: {len(class_dirs)}")
    for d in class_dirs:
        n = len(list(d.glob("*.parquet")))
        print(f"  class {d.name}: {n} file")

    # Ambil contoh file class 4 (Flow Instability) & class 0 (Normal)
    for cls in ["4", "0"]:
        files = sorted((DATASET_ROOT / cls).glob("*.parquet"))
        if not files:
            continue
        f = files[0]
        df = pd.read_parquet(f)
        print(f"\n--- {f.name} (class {cls}) ---")
        print("shape:", df.shape)
        print("columns:", list(df.columns))
        print("dtypes:")
        print(df.dtypes.to_string())
        print("index:", type(df.index).__name__, "first:", df.index[0])
        print("class unique:", df["class"].unique())


if __name__ == "__main__":
    main()