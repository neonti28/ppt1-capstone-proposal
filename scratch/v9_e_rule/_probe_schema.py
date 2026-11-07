import pandas as pd

print("=== BINS F-14 columns ===")
b = pd.read_csv("/mnt/d/Capstone 1/scratch/v9_d1/bins/F-14.csv.gz", nrows=3)
print(len(b.columns), list(b.columns))

print("\n=== DATASET schemas ===")
for ds in ["vib", "ssi", "shk", "stuck_k1", "hyd_ki", "stuck_k2"]:
    p = f"/mnt/d/Capstone 1/scratch/v9_d1/datasets/{ds}.csv.gz"
    d = pd.read_csv(p, nrows=3)
    print("-" * 10, ds, "ncols=", len(d.columns))
    print(list(d.columns))
