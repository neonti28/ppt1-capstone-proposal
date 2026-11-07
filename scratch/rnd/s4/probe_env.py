import sys, os, json, hashlib
print("python", sys.version.split()[0])
for m in ["pandas", "pyarrow", "numpy"]:
    try:
        mod = __import__(m)
        print("LIB", m, getattr(mod, "__version__", "?"))
    except Exception as e:
        print("LIB", m, "MISSING", type(e).__name__)

ROOT = "/mnt/d/Capstone 1(v2)"
p = os.path.join(ROOT, "data/volve/ddr.parquet")
print("SIZE", p, os.path.getsize(p))
import pandas as pd
df = pd.read_parquet(p)
print("SHAPE", df.shape)
print("COLS", list(df.columns))
print("DTYPES")
print(df.dtypes.to_string())
