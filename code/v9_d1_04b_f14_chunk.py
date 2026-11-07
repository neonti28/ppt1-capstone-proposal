import os
import numpy as np
import pandas as pd

P = "data/volve/witsml_parsed/F-14.csv"
SURF = ["TQA", "SPPA", "TFLO", "RPM", "SWOB", "HKLD", "ROP", "BPOS"]
SPMC = ["SPM1", "SPM2", "SPM3"]
STUCK = "STUCK_RT"
DMEA, DBTM = "DMEA", "DBTM"
CHUNK = 200_000

out_dir = "scratch/v9_d1/tmp_F14_1min"
os.makedirs(out_dir, exist_ok=True)

parts = []
for i, chunk in enumerate(pd.read_csv(P, chunksize=CHUNK, low_memory=False)):
    ts = pd.to_datetime(chunk["timestamp"], format="ISO8601", utc=True, errors="coerce")
    m = ts.notna()
    ts = ts[m]
    c = chunk[m]
    use = [x for x in SURF + SPMC + [STUCK, DMEA, DBTM] if x in c.columns]
    sub = c[use].apply(pd.to_numeric, errors="coerce").copy()
    sub.index = ts
    sub = sub.sort_index()
    sub = sub.resample("60s").mean()
    f = os.path.join(out_dir, f"part_{i:04d}.parquet")
    sub.to_parquet(f)
    parts.append(f)
    print(f"part {i}: rows={len(sub)} -> {f}", flush=True)

# merge: reindex union lalu mean per menit
idx = None
acc = None
cnt = None
for f in parts:
    s = pd.read_parquet(f)
    if idx is None:
        idx = s.index
        acc = s.copy()
        cnt = pd.Series(1.0, index=s.index)
    else:
        new = idx.union(s.index)
        a = acc.reindex(new)
        b = s.reindex(new)
        acc = a.add(b, fill_value=0.0)
        cnt = cnt.reindex(new).add(pd.Series(1.0, index=s.index).reindex(new), fill_value=0.0)
        idx = new
g = acc.div(cnt, axis=0)
g.to_parquet("scratch/v9_d1/F-14_1min.parquet")
print("FINAL minutes:", len(g), flush=True)
print("STUCK_rt nonnull:", int(g[STUCK].notna().sum()) if STUCK in g else None, flush=True)
for f in parts:
    os.remove(f)
