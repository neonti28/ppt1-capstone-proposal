import numpy as np
import pandas as pd

d = pd.read_csv("/mnt/d/Capstone 1/scratch/v9_d1/datasets/stuck_k2.csv.gz")
print("rows", len(d))
for c in ["ts_bin", "feat_ts_max", "lab_ts", "lab_kind", "y_stuck_onset",
          "y_prev_stuck_onset"]:
    s = d[c]
    n_nan = s.isna().sum()
    print(f"{c}: dtype={s.dtype} nan={n_nan}")
    if n_nan:
        print(d.loc[s.isna(), ["well", "ts_bin", "feat_ts_max", "lab_ts",
                               "lab_kind", "y_stuck_onset"]].head(10).to_string())
print("\nlab_kind counts:")
print(d["lab_kind"].value_counts(dropna=False))
print("\nlab_ts nan by lab_kind:")
print(d.groupby(d["lab_kind"].fillna("NaN"))["lab_ts"].apply(lambda s: s.isna().sum()))
print("\nrows where lab_kind==onset_event & lab_ts nan:",
      ((d["lab_kind"] == "onset_event") & d["lab_ts"].isna()).sum())
print("rows where lab_kind==onset_event & ts_bin nan:",
      ((d["lab_kind"] == "onset_event") & d["ts_bin"].isna()).sum())
print("\nts_bin nan by well:")
print(d.groupby("well")["ts_bin"].apply(lambda s: s.isna().sum()))
