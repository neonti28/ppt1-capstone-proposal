"""Cross-check P1: bins V9 (7 well bersama) vs bins V6 — max abs diff per kolom."""
import json
import numpy as np
import pandas as pd

V6 = "/mnt/d/Capstone 1(v2)/scratch/v6_e1/bins"
V9 = "/mnt/d/Capstone 1(v2)/scratch/v9_d1/bins"
WELLS = ["F-14", "F-15A", "F-15_S", "F-5", "F-7", "F-9", "F-9_A"]

res = {}
for w in WELLS:
    a = pd.read_csv(f"{V6}/{w}.csv.gz").set_index("ts_bin").sort_index()
    b = pd.read_csv(f"{V9}/{w}.csv.gz").set_index("ts_bin").sort_index()
    r = {"rows_v6": int(len(a)), "rows_v9": int(len(b)),
         "ts_index_identical": bool(a.index.equals(b.index))}
    common = [c for c in a.columns if c in b.columns]
    only_v6 = sorted(set(a.columns) - set(b.columns))
    only_v9 = sorted(set(b.columns) - set(a.columns))
    r["cols_only_v6"] = only_v6
    r["cols_only_v9"] = only_v9
    if r["ts_index_identical"]:
        diffs = {}
        for c in common:
            x = pd.to_numeric(a[c], errors="coerce").to_numpy(dtype=float)
            y = pd.to_numeric(b[c], errors="coerce").to_numpy(dtype=float)
            same_nan = np.isnan(x) == np.isnan(y)
            both = ~np.isnan(x) & ~np.isnan(y)
            d = float(np.max(np.abs(x[both] - y[both]))) if both.any() else 0.0
            mism = int((~same_nan).sum()) + int((~both & same_nan & False).sum())
            nan_mism = int((np.isnan(x) != np.isnan(y)).sum())
            if d > 0 or nan_mism:
                diffs[c] = {"max_abs_diff": d, "nan_mismatch": nan_mism}
        r["col_diffs"] = diffs
        r["n_cols_checked"] = len(common)
        r["identical"] = len(diffs) == 0
    else:
        r["identical"] = False
    res[w] = r
    print(f"== {w}: rows {r['rows_v6']}/{r['rows_v9']} idx_identical={r['ts_index_identical']} "
          f"identical={r['identical']} diffs={list(diffs)[:5] if r['ts_index_identical'] else 'N/A'}")

out = "/mnt/d/Capstone 1(v2)/scratch/v9_d1/v9_d1_01_crosscheck_v6.json"
json.dump(res, open(out, "w"), indent=1)
n_ident = sum(1 for r in res.values() if r.get("identical"))
print(f"IDENTICAL: {n_ident}/{len(WELLS)} wells -> {out}")
