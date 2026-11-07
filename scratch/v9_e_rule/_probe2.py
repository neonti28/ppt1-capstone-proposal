import pandas as pd
import glob

print("=== USROP_labeled label counts ===")
d = pd.read_csv("/mnt/d/Capstone 1/data/USROP_labeled.csv", usecols=["well", "label"])
print(d["label"].value_counts())
print(d["well"].nunique(), "unique well-files")
print(d["well"].value_counts())

print("\n=== toolwear_windows label ===")
t = pd.read_csv("/mnt/d/Capstone 1/scratch/v6_e1/toolwear_windows.csv")
print(t[["tool", "run", "y"]].drop_duplicates().to_string())
print("rows:", len(t))

print("\n=== cari time.csv / F-9A ===")
hits = glob.glob("/mnt/d/Capstone 1/**/time*.csv", recursive=True)
print(hits[:20])
hits2 = glob.glob("/mnt/d/Capstone 1/**/*F-9*", recursive=True)
print(hits2[:30])
