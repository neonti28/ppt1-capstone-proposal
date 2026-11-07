"""Probe structures: USROP well labels, DDR parquet nested fields, Norway file mapping."""
import pandas as pd, json, collections

pd.set_option("display.width", 200)

print("=" * 60)
print("USROP_labeled.csv well values")
u = pd.read_csv("data/USROP_labeled.csv", usecols=["well", "Measured Depth m"])
print(u["well"].value_counts())
print("md range per well:")
print(u.groupby("well")["Measured Depth m"].agg(["min", "max", "count"]))

print("=" * 60)
print("DDR parquet top-level schema")
d = pd.read_parquet("data/volve/ddr.parquet")
print(d.shape)
print(list(d.columns))
print(d[["nameWellbore", "dTimStart"]].head(3))
print("nameWellbore value_counts:")
print(d["nameWellbore"].value_counts(dropna=False))

print("=" * 60)
print("activity structure (first non-null)")
act = d.loc[d["activity"].notna(), "activity"].iloc[0]
print(type(act))
print(json.dumps(act[:2] if isinstance(act, list) else act, indent=1, default=str)[:2000])

print("=" * 60)
print("keys inside activity dicts across ALL rows")
keys = collections.Counter()
n_md = 0
n_total = 0
samples = []
for a in d["activity"].dropna():
    if isinstance(a, list):
        for it in a:
            n_total += 1
            if isinstance(it, dict):
                keys.update(it.keys())
                md = it.get("md")
                if isinstance(md, dict):
                    samples.append(("dict_md", md))
                elif isinstance(md, (int, float)) and md and md > 0:
                    n_md += 1
print("n activity items:", n_total, "with numeric md>0:", n_md)
print("key freq:", keys.most_common(40))
print("md dict samples:", samples[:3])

print("=" * 60)
print("statusInfo / surveyStation presence")
for c in d.columns:
    if d[c].notna().any() and d[c].iloc[0] is not None:
        first = d.loc[d[c].notna(), c].iloc[0]
        if isinstance(first, (list, dict)):
            print(f"--- {c}: type={type(first).__name__}")
            s = json.dumps(first, default=str, indent=1)
            print(s[:800])
