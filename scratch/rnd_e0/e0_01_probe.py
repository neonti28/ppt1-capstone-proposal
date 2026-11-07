#!/usr/bin/env python3
"""RND-E0 probe 01 — struktur dataset audit: jendela tool_wear (hop detik), rentang rig."""
import json
import pandas as pd

BASE = "/mnt/d/Capstone 1(v2)"
tw = pd.read_csv(f"{BASE}/scratch/v6_e1/toolwear_windows.csv")
print("toolwear shape:", tw.shape)
print("kolom (8 pertama):", tw.columns.tolist()[:8])
print(tw[["tool", "run", "start_sample"]].head(3).to_string())
out = {}
for (t, r), g in tw.groupby(["tool", "run"]):
    s = g["start_sample"].sort_values().to_numpy()
    d = pd.Series(s).diff().dropna()
    rec = dict(n=int(len(g)), dmin=None if not len(d) else int(d.min()),
               dmed=None if not len(d) else float(d.median()),
               dmax=None if not len(d) else int(d.max()),
               span_s=int(s.max() - s.min()) if len(s) else None,
               y_mean=None)
    out[f"{t}|{r}"] = rec
    print(f"{t:>8} {r} n={rec['n']:>4} dmin={rec['dmin']} dmed={rec['dmed']} "
          f"dmax={rec['dmax']} span_s={rec['span_s']}")
json.dump(out, open(f"{BASE}/scratch/rnd_e0/e0_01_toolwear_hop.json", "w"), indent=1)

usrop = pd.read_csv(f"{BASE}/data/USROP_labeled.csv", low_memory=False)
print("\nUSROP shape:", usrop.shape)
print("kolom:", usrop.columns.tolist()[:12])
print("wells:", sorted(usrop["well"].unique().tolist()))
print("label counts:", usrop["label"].value_counts().to_dict())
md = usrop["Measured Depth m"]
print("MD monotone per file?", bool(md.is_monotonic_increasing))
