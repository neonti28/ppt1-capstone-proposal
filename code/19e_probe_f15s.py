"""Probe 4: identify which DDR wellbore Norway '15/9-F-15S' really is.
Evidence gathered: (a) wellboreAlias strings, (b) statusInfo.diaHole per wellbore,
(c) USROP Diamated mm profile per well, (d) gamma correlation F-15 vs F-15S."""
import pandas as pd, numpy as np, json, re, collections

d = pd.read_parquet("data/volve/ddr.parquet")

print("== wellboreAlias unique per wellbore (F-15*/F-9*) ==")
al = collections.defaultdict(set)
for _, r in d.iterrows():
    wb = r["nameWellbore"]
    if "F-15" in wb or "F-9" in wb:
        al[wb].add(str(r["wellboreAlias"]))
for k in sorted(al):
    print(" ", k)
    for v in sorted(al[k])[:3]:
        print("     ", v[:200])

print("\n== statusInfo.diaHole per wellbore ==")
dh = collections.defaultdict(collections.Counter)
for _, r in d.iterrows():
    st = r["statusInfo"]
    if isinstance(st, np.ndarray) and len(st) and isinstance(st[0], dict):
        dh[r["nameWellbore"]][st[0].get("diaHole")] += 1
for k in sorted(dh):
    if "F-15" in k or "F-5" in k or "F-9" in k or "F-14" in k or "F-7" in k:
        print(" ", k, dict(dh[k]))

print("\n== activity proprietaryCode x md-range for F-15 family ==")
rows = []
for _, r in d.iterrows():
    wb = r["nameWellbore"]
    if "F-15" not in wb:
        continue
    for it in (r["activity"] if isinstance(r["activity"], np.ndarray) else []):
        if isinstance(it, dict):
            try:
                md = float(it.get("md"))
            except (TypeError, ValueError):
                continue
            if md > 0:
                rows.append((wb, it.get("proprietaryCode"), md))
adf = pd.DataFrame(rows, columns=["wb", "code", "md"])
print(adf.groupby(["wb", "code"])["md"].agg(["count", "min", "max"]).to_string())

print("\n== USROP 'Diameter mm' unique values per well ==")
u = pd.read_csv("data/USROP_labeled.csv", usecols=["well", "Measured Depth m", "Diameter mm", "USROP Gamma gAPI"])
for w, g in u.groupby("well"):
    print(" ", w, "diam:", sorted(g["Diameter mm"].dropna().round(2).unique())[:10],
          "| n=", len(g))

print("\n== gamma correlation F-15 vs F-15S on common md grid ==")
a = u[u["well"].str.contains("F-15d")]
b = u[u["well"].str.contains("F-15Sd")]
lo = max(a["Measured Depth m"].min(), b["Measured Depth m"].min())
hi = min(a["Measured Depth m"].max(), b["Measured Depth m"].max())
grid = np.arange(np.ceil(lo), np.floor(hi), 1.0)
ga = np.interp(grid, a.sort_values("Measured Depth m")["Measured Depth m"],
               a.sort_values("Measured Depth m")["USROP Gamma gAPI"])
gb = np.interp(grid, b.sort_values("Measured Depth m")["Measured Depth m"],
               b.sort_values("Measured Depth m")["USROP Gamma gAPI"])
m = np.isfinite(ga) & np.isfinite(gb)
print(f"  common md [{lo:.0f},{hi:.0f}], n={m.sum()}, Pearson r = {np.corrcoef(ga[m], gb[m])[0,1]:.4f}")

# same test as control: F-15 vs F-14 (different wells) should be ~0
c = u[u["well"].str.contains("F-14d")]
lo2 = max(a["Measured Depth m"].min(), c["Measured Depth m"].min())
hi2 = min(a["Measured Depth m"].max(), c["Measured Depth m"].max())
g2 = np.arange(np.ceil(lo2), np.floor(hi2), 1.0)
ga2 = np.interp(g2, a.sort_values("Measured Depth m")["Measured Depth m"], a.sort_values("Measured Depth m")["USROP Gamma gAPI"])
gc2 = np.interp(g2, c.sort_values("Measured Depth m")["Measured Depth m"], c.sort_values("Measured Depth m")["USROP Gamma gAPI"])
m2 = np.isfinite(ga2) & np.isfinite(gc2)
print(f"  CONTROL F-15 vs F-14: n={m2.sum()}, Pearson r = {np.corrcoef(ga2[m2], gc2[m2])[0,1]:.4f}")
