import json
import pandas as pd
BASE = "/mnt/d/Capstone 1(v2)"
d = json.load(open(f"{BASE}/scratch/rnd/r8/r8_toolwear.json"))
for r in d["rows"]:
    print(r["fold"], r["model"], "n_uji", r["n_uji"], "tp", r["tp"], "fp", r["fp"],
          "fn", r["fn"], "bacc", r["bacc"], "prev", r["prev"], "thr", r["thr"], "C", r["C"])
tw = pd.read_csv(f"{BASE}/scratch/v6_e1/toolwear_windows.csv")
print(tw.groupby("tool")["y"].agg(["count", "mean"]))
print("total", len(tw))
