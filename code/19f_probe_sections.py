"""Probe 5: section structure - USROP md ranges per Diameter, DDR statusInfo (md, diaHole, time)
maps per F-15 family wellbore, and drill-activity depth progression."""
import pandas as pd, numpy as np, collections

u = pd.read_csv("data/USROP_labeled.csv", usecols=["well", "Measured Depth m", "Diameter mm"])
print("== USROP md range per (well, Diameter mm) ==")
g = u.groupby([u["well"].str.extract(r'(F-\d+A?S?)')[0], "Diameter mm"])["Measured Depth m"]
print(g.agg(["min", "max", "count"]).to_string())

d = pd.read_parquet("data/volve/ddr.parquet")
print("\n== DDR statusInfo (dTim, md, diaHole) for F-15 family ==")
rows = []
for _, r in d.iterrows():
    wb = r["nameWellbore"]
    if "F-15" not in wb:
        continue
    st = r["statusInfo"]
    if isinstance(st, np.ndarray) and len(st) and isinstance(st[0], dict):
        s = st[0]
        try:
            md = float(s.get("md"))
        except (TypeError, ValueError):
            md = np.nan
        rows.append(dict(wb=wb, dTim=s.get("dTim"), md=md, diaHole=s.get("diaHole")))
sdf = pd.DataFrame(rows)
for wb, gg in sdf.groupby("wb"):
    gg = gg.sort_values("dTim")
    print(f"\n--- {wb}")
    print(gg[["dTim", "md", "diaHole"]].to_string(index=False, max_rows=40))

print("\n== drill-activity first-reach depth progression (F-15 family) ==")
rows = []
for _, r in d.iterrows():
    wb = r["nameWellbore"]
    if "F-15" not in wb:
        continue
    for it in (r["activity"] if isinstance(r["activity"], np.ndarray) else []):
        if isinstance(it, dict) and it.get("proprietaryCode") == "drilling -- drill":
            try:
                md = float(it.get("md"))
            except (TypeError, ValueError):
                continue
            if md > 0 and it.get("dTimStart"):
                rows.append(dict(wb=wb, t=it["dTimStart"], md=md))
dd = pd.DataFrame(rows)
dd["t"] = pd.to_datetime(dd["t"], utc=True)
for wb, gg in dd.groupby("wb"):
    gg = gg.sort_values("t")
    mx = gg["md"].cummax()
    print(f"  {wb}: n={len(gg)} span {gg['t'].min().date()}..{gg['t'].max().date()} "
          f"md_max_progress {mx.iloc[0]:.0f}->{mx.iloc[-1]:.0f} "
          f"| monotone-in-time reach of 1400m at {gg.loc[mx>=1400,'t'].min() if (mx>=1400).any() else 'never'} "
          f"| 4000m at {gg.loc[mx>=4000,'t'].min() if (mx>=4000).any() else 'never'}")
