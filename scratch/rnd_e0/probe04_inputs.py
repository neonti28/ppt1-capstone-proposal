import pandas as pd

TW = "/mnt/d/Capstone 1(v2)/scratch/v6_e1/toolwear_windows.csv"
tw = pd.read_csv(TW)
print("toolwear:", tw.shape)
print("kolom:", list(tw.columns))
print(tw[["tool", "run"]].value_counts())
print("start_sample range:", tw["start_sample"].min(), tw["start_sample"].max())
print("y mean:", tw["y"].mean())

feats = [c for c in tw.columns
         if c.endswith(("_mean", "_std", "_rms", "_kurt", "_skew", "_p2p",
                        "_crest", "_zcr", "_fdom"))]
print("n fitur (resep pipeline):", len(feats))

for w in ["F-14", "F-9_A", "F-10"]:
    b = pd.read_csv(f"/mnt/d/Capstone 1(v2)/scratch/v9_d1/bins/{w}.csv.gz")
    print(w, "bins:", b.shape, "ts range:", b["ts_bin"].min(), b["ts_bin"].max())
