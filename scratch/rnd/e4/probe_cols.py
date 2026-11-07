import pandas as pd, json
BASE = "/mnt/d/Capstone 1(v2)"
df = pd.read_csv(f"{BASE}/scratch/v9_d1/datasets/hyd_ki.csv.gz", nrows=5)
print("dataset cols", len(df.columns))
print(list(df.columns))
LD = ("y_hyd","y_prev_hyd","valid_prev_hyd","obs_hyd","anom_hyd","lab_ts","lab_kind","feat_ts_max")
feats = [c for c in df.columns if c not in LD and pd.api.types.is_numeric_dtype(df[c])]
print("feats_with_tsbin", len(feats))
feats2 = [c for c in feats if c != "ts_bin"]
print("feats_no_tsbin", len(feats2))
b = pd.read_csv(f"{BASE}/scratch/v9_d1/bins/F-12.csv.gz", nrows=3)
print("bins cols", list(b.columns))
print(b.head(3).to_string())
lowo = json.load(open(f"{BASE}/scratch/v9_d1/lowo_hyd_ki.json"))
print("folds", [f["test_well"] for f in lowo["folds"]])
print("inner keys", list(lowo["folds"][0].keys()))
print("sizes", {f["test_well"]: f.get("n_test") for f in lowo["folds"]})
