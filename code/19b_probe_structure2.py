"""Probe deeper: activity items, statusInfo, surveyStation, wellbore name matching."""
import pandas as pd, numpy as np, json, collections

d = pd.read_parquet("data/volve/ddr.parquet")
print("activity dtype per row sample:")
act_col = d["activity"]
print(type(act_col.iloc[0]), act_col.notna().sum(), "non-null")

keys = collections.Counter()
n_items = n_md = 0
md_ts_pairs = 0
sample_items = []
for v in act_col:
    if v is None or (isinstance(v, float) and np.isnan(v)):
        continue
    if isinstance(v, np.ndarray):
        items = v
    elif isinstance(v, list):
        items = v
    else:
        continue
    for it in items:
        n_items += 1
        if isinstance(it, dict):
            keys.update(it.keys())
            if len(sample_items) < 3:
                sample_items.append(it)
print("activity items:", n_items, "keys:", keys.most_common(30))
for s in sample_items:
    print(json.dumps(s, default=str)[:600])

print("=" * 70)
for c in ["statusInfo", "surveyStation", "wellboreInfo", "fluid", "porePressure", "lithShowInfo"]:
    col = d[c]
    nn = col.dropna()
    print(f"--- {c}: non-null={len(nn)}")
    if len(nn):
        v = nn.iloc[0]
        print("   type:", type(v).__name__)
        if isinstance(v, np.ndarray):
            print("   len:", len(v))
            if len(v):
                print("   first elem type:", type(v[0]).__name__)
                print("   first elem:", json.dumps(v[0], default=str)[:700])
        else:
            print("   ", json.dumps(v, default=str)[:700])

print("=" * 70)
# Does surveyStation/statusInfo carry md + time?
for c in ["statusInfo", "surveyStation"]:
    cnt_md = cnt_ts = 0
    keys_c = collections.Counter()
    for v in d[c]:
        if not isinstance(v, np.ndarray):
            continue
        for it in v:
            if isinstance(it, dict):
                keys_c.update(it.keys())
                if "md" in it:
                    cnt_md += 1
                if any(k.startswith("dTim") for k in it):
                    cnt_ts += 1
    print(c, "items with md:", cnt_md, "with dTim*:", cnt_ts, "keys:", keys_c.most_common(20))
