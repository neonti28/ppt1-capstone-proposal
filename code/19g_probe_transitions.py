"""Probe 6: settle F-15 / F-15S identity via section transitions + casing points."""
import pandas as pd, numpy as np

d = pd.read_parquet("data/volve/ddr.parquet")

def st_rows(wb):
    out = []
    for _, r in d[d["nameWellbore"] == wb].iterrows():
        st = r["statusInfo"]
        if isinstance(st, np.ndarray) and len(st) and isinstance(st[0], dict):
            s = st[0]
            try:
                md = float(s.get("md"))
            except (TypeError, ValueError):
                md = np.nan
            out.append((s.get("dTim", "")[:10], md, s.get("diaHole")))
    return sorted(out)

for wb in ["NO 15/9-F-15", "NO 15/9-F-15 A"]:
    rows = st_rows(wb)
    print(f"=== {wb}: {len(rows)} statusInfo rows; diaHole transition points ===")
    prev = None
    for t, md, dh in rows:
        if dh != prev:
            print(f"   {t}  md={md:>8}  diaHole={dh}")
            prev = dh
    print("   md by diaHole:", {k: (min(m for _, m, m2 in rows if m2 == k and m == m),
                                    max(m for _, m, m2 in rows if m2 == k and m == m))
                                for k in set(x[2] for x in rows)})

print("\n=== casing activities (F-15 main / F-15 A) ===")
for wb in ["NO 15/9-F-15", "NO 15/9-F-15 A"]:
    print("---", wb)
    for _, r in d[d["nameWellbore"] == wb].iterrows():
        for it in (r["activity"] if isinstance(r["activity"], np.ndarray) else []):
            if isinstance(it, dict) and it.get("proprietaryCode") == "drilling -- casing":
                try:
                    md = float(it.get("md"))
                except (TypeError, ValueError):
                    continue
                if md > 0:
                    print(f"   {str(it.get('dTimStart'))[:16]} md={md:>7} stateDetail={it.get('stateDetailActivity')} :: {str(it.get('comments'))[:90]}")

print("\n=== USROP exact section boundary rows ===")
u = pd.read_csv("data/USROP_labeled.csv", usecols=["well", "Measured Depth m", "Diameter mm"])
for w, g in u.groupby("well"):
    if "F-15" not in w:
        continue
    g = g.sort_values("Measured Depth m")
    print("---", w)
    prev = None
    for _, row in g.iterrows():
        if row["Diameter mm"] != prev:
            print(f"   md={row['Measured Depth m']:>9}  diam={row['Diameter mm']}")
            prev = row["Diameter mm"]
    print(f"   last md={g['Measured Depth m'].iloc[-1]}  last diam={g['Diameter mm'].iloc[-1]}")
