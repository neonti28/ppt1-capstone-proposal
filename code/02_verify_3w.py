#!/usr/bin/env python3
"""
Verifikasi dataset 3W setelah diekstrak.
Menampilkan struktur folder kelas & sampel file parquet.
"""
from pathlib import Path
import sys

import pandas as pd

DATASET_ROOT = Path(__file__).resolve().parent.parent / "data" / "3W-main" / "dataset"
if not DATASET_ROOT.exists():
    DATASET_ROOT = Path(__file__).resolve().parent.parent / "data" / "3W" / "dataset"


def main():
    print("Dataset root:", DATASET_ROOT)
    if not DATASET_ROOT.exists():
        sys.exit("Dataset belum ada. Ekstrak dulu 3W.zip ke data/")

    class_dirs = sorted(
        [p for p in DATASET_ROOT.iterdir() if p.is_dir() and p.name.isdigit()]
    )
    print(f"\nKelas ditemukan: {len(class_dirs)}")
    total_files = 0
    for d in class_dirs:
        n = len(list(d.glob("*.parquet")))
        total_files += n
        print(f"  class {d.name}: {n} file")
    print(f"\nTotal file parquet: {total_files}")

    # Sampel class 4
    for cls in ["4", "0"]:
        files = sorted((DATASET_ROOT / cls).glob("*.parquet"))
        if not files:
            print(f"\n(class {cls} kosong)")
            continue
        f = files[0]
        df = pd.read_parquet(f)
        print(f"\n--- {f.name} (class {cls}) ---")
        print("shape:", df.shape)
        print("columns:", list(df.columns))
        print("class unique:", df["class"].unique())
        print("index type:", type(df.index).__name__)


if __name__ == "__main__":
    main()