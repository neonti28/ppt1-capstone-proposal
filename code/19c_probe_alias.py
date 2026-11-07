"""Probe 2: wellbore aliases, per-wellbore md ranges, USROP->Norway file mapping."""
import pandas as pd, numpy as np, json, collections, re

d = pd.read_parquet("data/volve/ddr.parquet")

print("== wellboreAlias / wellAlias samples for F-15* and F-9* ==")
for _, r in d.iterrows():
    wb = r["nameWellbore"]
    if wb in ("NO 15/9-F-15", "NO 15/9-F-15 A", "NO 15/9-F-15 B", "NO 15/9-F-15 C",
              "NO 15/9-F-15 D", "NO 15/9-F-9", "NO 15/9-F-9 A"):
        print(wb, "| wellboreAlias:", json.dumps(r["wellboreAlias"], default=str),
              "| wellAlias:", json.dumps(r["wellAlias"], default=str))
        break
al = collections.defaultdict(set)
for _, r in d.iterrows():
    wa = r["wellboreAlias"]
    if isinstance(wa, dict):
        al[r["nameWellbore"]].add(wa.get("name"))
for k in sorted(al):
    if "F-15" in k or "F-9" in k:
        print("ALIAS", k, "->", al[k])

print("\n== per-wellbore md range from activity + surveyStation + statusInfo ==")
rows = []
for _, r in d.iterrows():
    wb = r["nameWellbore"]
    md_a, t_a = [], []
    for it in (r["activity"] if isinstance(r["activity"], np.ndarray) else []):
        if isinstance(it, dict):
            try:
                md = float(it.get("md"))
            except (TypeError, ValueError):
                md = np.nan
            ts = it.get("dTimStart")
            if not np.isnan(md) and md > 0 and ts:
                md_a.append(md)
                t_a.append(str(ts))
    md_s = []
    for it in (r["surveyStation"] if isinstance(r["surveyStation"], np.ndarray) else []):
        if isinstance(it, dict):
            try:
                md = float(it.get("md"))
            except (TypeError, ValueError):
                md = np.nan
            if not np.isnan(md) and md > 0 and it.get("dTim"):
                md_s.append(md)
    st = r["statusInfo"]
    md_st, ts_st = np.nan, None
    if isinstance(st, np.ndarray) and len(st) and isinstance(st[0], dict):
        try:
            md_st = float(st[0].get("md"))
        except (TypeError, ValueError):
            md_st = np.nan
        ts_st = st[0].get("dTim")
        if md_st is not None and md_st <= 0:
            md_st = np.nan
    rows.append(dict(wb=wb,
                     n_act=len(md_a),
                     act_min=min(md_a) if md_a else np.nan,
                     act_max=max(md_a) if md_a else np.nan,
                     t_min=min(t_a) if t_a else None, t_max=max(t_a) if t_a else None,
                     n_surv=len(md_s),
                     status_md=md_st, status_ts=ts_st))
df = pd.DataFrame(rows)
agg = df.groupby("wb").agg(n_rows=("wb", "size"), n_act=("n_act", "sum"),
                           act_min=("act_min", "min"), act_max=("act_max", "max"),
                           t_min=("t_min", "min"), t_max=("t_max", "max"),
                           n_surv=("n_surv", "sum")).reset_index()
agg = agg[agg["wb"].str.contains(r"F-5|F-7|F-9|F-14|F-15", regex=True)]
pd.set_option("display.width", 250)
pd.set_option("display.max_rows", 100)
print(agg.to_string(index=False))

print("\n== statusInfo md==nan count / sentinel check ==")
st_md = df["status_md"]
print("status md valid (>0):", st_md.notna().sum(), "of", len(df))
print("status ts samples:", df["status_ts"].dropna().unique()[:5])

print("\n== making_USROP.py mapping ==")
txt = open("data/USROP/Code/making_USROP.py", encoding="utf-8", errors="replace").read()
print(txt[:3000])
