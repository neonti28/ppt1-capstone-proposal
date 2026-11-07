import gzip, pandas as pd, json
BASE = "/mnt/d/Capstone 1(v2)"
b = pd.read_csv(f"{BASE}/scratch/v9_d1/bins/F-14.csv.gz", compression="gzip", usecols=["ts_bin"])
print("ts_bin min/max:", int(b.ts_bin.min()), int(b.ts_bin.max()))
print("as epoch:", pd.to_datetime(b.ts_bin.min(), unit="s"), pd.to_datetime(b.ts_bin.max(), unit="s"))
print("span days:", (b.ts_bin.max() - b.ts_bin.min()) / 86400)
# real timestamp range from parsed witsml (first column only, small read)
h = pd.read_csv(f"{BASE}/data/volve/witsml_parsed/F-14.csv", usecols=["timestamp"], nrows=3)
print("parsed first ts:", h["timestamp"].tolist())
t = pd.read_csv(f"{BASE}/data/volve/witsml_parsed/F-14.csv", usecols=["timestamp"], skiprows=range(1, 5000), nrows=3)
print("parsed ts at row 5000:", t["timestamp"].tolist())
