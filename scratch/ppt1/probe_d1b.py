import pandas as pd, os, json

base = "/mnt/d/Capstone 1(v2)/data/volve"

print("=== ddr.parquet ===")
d = pd.read_parquet(base + "/ddr.parquet")
print("shape", d.shape)
print("cols", list(d.columns)[:40])
print(d.head(3).to_string()[:2000])

print("\n=== usrop_wellbores_events.csv ===")
u = pd.read_csv(base + "/usrop_wellbores_events.csv")
print("shape", u.shape)
print("cols", list(u.columns))
print(u.head(5).to_string()[:2500])

print("\n=== usrop_timestamped.csv head ===")
with open(base + "/usrop_timestamped.csv", encoding="utf-8") as f:
    for i, line in enumerate(f):
        print(line.rstrip()[:300])
        if i > 3:
            break

print("\n=== witsml_parsed ===")
wd = base + "/witsml_parsed"
for root, dirs, files in os.walk(wd):
    print(root, "dirs:", dirs[:5], "nfiles:", len(files), "sample:", files[:4])
    if root.count(os.sep) - wd.count(os.sep) > 1:
        dirs[:] = []
