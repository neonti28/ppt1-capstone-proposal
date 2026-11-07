import pandas as pd
df = pd.read_csv("scratch/v9_d1/bins/F-14.csv.gz", nrows=3)
print(df.columns.tolist())
print("rows(total):")
import gzip
print(sum(1 for _ in gzip.open("scratch/v9_d1/bins/F-14.csv.gz", "rt")) - 1)
