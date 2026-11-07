import pandas as pd, numpy as np
b = pd.read_csv("scratch/v9_d1/bins/F-14.csv.gz", usecols=["ts_bin", "stuck_max", "stuck_n"])
t = b["ts_bin"].to_numpy()
print("bins:", len(b), "min:", t.min(), "->", pd.to_datetime(t.min(), unit="m", utc=True),
      "max:", t.max(), "->", pd.to_datetime(t.max(), unit="m", utc=True))
span_min = t.max() - t.min() + 1
print("span_minutes:", span_min, "observed:", len(b), "density:", round(len(b)/span_min, 4))
d = np.diff(np.sort(t))
print("gap>30min segments:", int((d > 30).sum()), "max_gap_min:", int(d.max()))
# onsets invariant test dari bins: ffill stuck_max -> edge 0->1
s = b.set_index(pd.to_datetime(b["ts_bin"], unit="m", utc=True))["stuck_max"].sort_index()
prev, on = None, 0
for v in s.to_numpy():
    if np.isnan(v):
        continue
    if prev is not None and prev < 1 and v >= 1:
        on += 1
    prev = v
print("onsets_ffill_from_bins:", on, "(REF F-14 = 61)")
