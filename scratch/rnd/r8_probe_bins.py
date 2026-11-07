import pandas as pd
b = pd.read_csv("/mnt/d/Capstone 1(v2)/scratch/v9_d1/bins/F-10.csv.gz", nrows=3)
print("bins cols:", list(b.columns))
print(b.head(2).to_string())
w = pd.read_csv("/mnt/d/Capstone 1(v2)/scratch/v9_d1/windows/F-10.csv.gz", nrows=3)
print("win cols:", list(w.columns))
