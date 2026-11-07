"""Probe 7: calibrate USROP 'Diameter mm' boundaries against DDR diaHole section transitions
for ALL wellbores, to judge whether hole-size signature is a reliable discriminator."""
import pandas as pd, numpy as np

d = pd.read_parquet("data/volve/ddr.parquet")

print("== DDR statusInfo diaHole transitions per USROP-relevant wellbore ==")
for wb in sorted(d["nameWellbore"].unique()):
    if not any(k in wb for k in ("F-5", "F-7", "F-9", "F-14", "F-15")):
        continue
    tr = []
    prev = None
    mdmin, mdmax = {}, {}
    for _, r in d[d["nameWellbore"] == wb].iterrows():
        st = r["statusInfo"]
        if not (isinstance(st, np.ndarray) and len(st) and isinstance(st[0], dict)):
            continue
        s = st[0]
        try:
            md = float(s.get("md"))
        except (TypeError, ValueError):
            md = np.nan
        dh = s.get("diaHole")
        if md == md and md > 0:
            mdmin[dh] = min(mdmin.get(dh, md), md)
            mdmax[dh] = max(mdmax.get(dh, md), md)
        if dh != prev:
            tr.append(f"{str(s.get('dTim'))[:10]}:{md:.0f}m:{dh}")
            prev = dh
    print(f"  {wb:>16} | " + " -> ".join(tr))
    print(f"  {'':>16} | md per diaHole: " +
          ", ".join(f"{k}=[{mdmin[k]:.0f},{mdmax[k]:.0f}]" for k in mdmin if k is not None))

print("\n== USROP diameter boundaries per file ==")
u = pd.read_csv("data/USROP_labeled.csv", usecols=["well", "Measured Depth m", "Diameter mm"])
for w, g in u.groupby("well"):
    g = g.sort_values("Measured Depth m")
    b = []
    prev = None
    for _, row in g.iterrows():
        if row["Diameter mm"] != prev:
            b.append(f"{row['Diameter mm']}@{row['Measured Depth m']:.1f}")
            prev = row["Diameter mm"]
    print(f"  {w:<28} start={g['Measured Depth m'].min():.1f} end={g['Measured Depth m'].max():.1f} | " +
          " -> ".join(b))

print("\n== DDR wellbore TD (max valid activity md) ==")
td = {}
for _, r in d.iterrows():
    wb = r["nameWellbore"]
    for it in (r["activity"] if isinstance(r["activity"], np.ndarray) else []):
        if isinstance(it, dict):
            try:
                md = float(it.get("md"))
            except (TypeError, ValueError):
                continue
            if md > 0:
                td[wb] = max(td.get(wb, 0), md)
for k in sorted(td):
    if any(x in k for x in ("F-5", "F-7", "F-9", "F-14", "F-15")):
        print(f"  {k:>16} TD(activity md max)={td[k]:.1f}")
