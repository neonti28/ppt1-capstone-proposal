"""Verifikasi jumlah record (bukan jumlah baris teks) untuk tiga CSV yang dikutip."""
import os
import pandas as pd
ROOT = "/mnt/d/Capstone 1(v2)"
for rel in ["data/volve/usrop_wellbores_events.csv",
            "data/predictive/features_timeseries_events.csv",
            "data/USROP_health.csv"]:
    p = os.path.join(ROOT, rel)
    df = pd.read_csv(p, low_memory=False)
    with open(p, "rb") as f:
        n_lines = sum(1 for _ in f)
    print(f"{rel}: baris_teks={n_lines} record_pandas={len(df)} kolom={df.shape[1]}")
