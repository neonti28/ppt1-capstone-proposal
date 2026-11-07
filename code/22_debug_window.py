"""Debug: kenapa cek jendela kampanye melaporkan semua baris di luar?"""
import importlib.util, os
import numpy as np, pandas as pd

ROOT = "/mnt/d/Capstone 1"
spec = importlib.util.spec_from_file_location("join20", os.path.join(ROOT, "code", "20_join_md_time.py"))
j20 = importlib.util.module_from_spec(spec); spec.loader.exec_module(j20)

out = pd.read_csv(os.path.join(ROOT, "data", "volve", "usrop_timestamped.csv"),
                  dtype={"est_timestamp": str, "join_status": str}, keep_default_na=False, na_values=[])
ts = pd.to_datetime(out["est_timestamp"].replace("", pd.NA), utc=True, errors="coerce", format="ISO8601")

ddr = pd.read_parquet(j20.DDR_PATH)
pairs, _, _, _ = j20.collect_pairs(ddr)

for well_name, wb in list(j20.WELL_MAP.items())[:3]:
    mds, tss = j20.build_anchor_curve(pairs[wb])
    lo, hi = float(np.min(tss)), float(np.max(tss))
    m = (out["well"] == well_name).to_numpy()
    t = ts[m].dropna()
    epoch = t.astype("int64").to_numpy(dtype="float64") / 1e9
    print(f"{well_name} -> {wb}")
    print(f"   anchor t  : {lo:.0f} .. {hi:.0f}  ({pd.Timestamp(lo, unit='s', tz='UTC')} .. {pd.Timestamp(hi, unit='s', tz='UTC')})")
    print(f"   est epoch : {epoch.min():.0f} .. {epoch.max():.0f}  ({pd.Timestamp(epoch.min(), unit='s', tz='UTC')} .. {pd.Timestamp(epoch.max(), unit='s', tz='UTC')})")
    print(f"   ts dtype  : {t.dtype}  sample: {t.iloc[0]}")
    print(f"   n di luar : {int(((epoch < lo) | (epoch > hi)).sum())} / {len(epoch)}")
