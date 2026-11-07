import pandas as pd
p = "/mnt/d/Capstone 1(v2)/data/volve/ddr.parquet"
df = pd.read_parquet(p)
print("shape:", df.shape)
print("\ncolumns:")
for c in df.columns:
    print(" -", c, "|", str(df[c].dtype), "| nunique=", df[c].nunique(dropna=True))
print("\nhead:")
print(df.head(3).to_string()[:3000])
