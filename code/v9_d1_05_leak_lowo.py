import os, json
import pandas as pd

DS = "scratch/v9_d1/datasets"
OUT = "scratch/v9_d1"
engines = {
    "vib": f"{DS}/vib.csv.gz", "ssi": f"{DS}/ssi.csv.gz", "shk": f"{DS}/shk.csv.gz",
    "stuck_k1": f"{DS}/stuck_k1.csv.gz", "hyd_ki": f"{DS}/hyd_ki.csv.gz",
    "stuck_k2": f"{DS}/stuck_k2.csv.gz",
}
report = {}
for eng, path in engines.items():
    if not os.path.exists(path):
        report[eng] = {"status": "MISSING (merge berjalan)"}
        continue
    df = pd.read_csv(path, usecols=["well", "ts_bin", "feat_ts_max", "lab_ts"])
    n = len(df)
    both = df["feat_ts_max"].notna() & df["lab_ts"].notna()
    viol = int((df.loc[both, "feat_ts_max"] >= df.loc[both, "lab_ts"]).sum())
    nan_feat = int(df["feat_ts_max"].isna().sum())
    wells = sorted(df["well"].dropna().unique().tolist())
    folds = [{"test_well": w, "train_wells": [x for x in wells if x != w]} for w in wells]
    json.dump({"engine": eng, "n_rows": n, "wells": wells, "n_folds": len(folds), "folds": folds},
              open(f"{OUT}/lowo_{eng}.json", "w"), indent=1)
    report[eng] = {"status": "OK", "n_rows": n, "leak_violations_feat_ge_lab": viol,
                   "rows_with_nan_feat_ts": nan_feat, "wells": wells, "n_folds": len(folds)}
json.dump(report, open(f"{OUT}/v9_d1_05_leak_lowo.json", "w"), indent=1)
print(json.dumps(report, indent=1))
