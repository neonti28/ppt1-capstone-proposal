"""RND-D0 measurement 2: native cadence + gaps per key channel from parsed WITSML CSV."""
import json, os, sys
import numpy as np
import pandas as pd

BASE = "/mnt/d/Capstone 1(v2)"
PARSED = f"{BASE}/data/volve/witsml_parsed"
OUT = os.path.dirname(os.path.abspath(__file__))
WELLS = sys.argv[1:] or ["F-9_A", "F-14"]
CH = ["VIBLAT_RT", "SHKRSK_RT", "STUCK_RT", "CRPM_RT", "SPPA", "TQA", "HKLD", "ROP", "TFLO"]
_env = os.environ.get("RND_CH")
if _env:
    CH = [c.strip() for c in _env.split(",") if c.strip()]

res = {}
_jp = f"{OUT}/meas2_native_cadence.json"
if os.path.exists(_jp):
    try:
        res = json.load(open(_jp))
    except Exception:
        res = {}
for w in WELLS:
    p = f"{PARSED}/{w}.csv"
    if not os.path.exists(p):
        print("MISSING", p); continue
    print("reading", p, os.path.getsize(p) // 1_000_000, "MB")
    usecols = ["timestamp"] + CH
    # find which key channels exist
    hdr = pd.read_csv(p, nrows=0).columns.tolist()
    usecols = [c for c in usecols if c in hdr]
    missing_ch = [c for c in CH if c not in hdr]
    store = {}
    for chunk in pd.read_csv(p, usecols=usecols, chunksize=200000, low_memory=False):
        tser = pd.to_datetime(chunk.pop("timestamp"), errors="coerce", utc=True)
        t = tser.to_numpy(dtype="datetime64[ns]").astype("int64").astype("float64") / 1e9
        t = np.where(np.isnat(tser.to_numpy(dtype="datetime64[ns]")), np.nan, t)
        for c in chunk.columns:
            v = chunk[c].to_numpy(dtype="float64", copy=False)
            ok = ~np.isnan(v) & ~np.isnan(t)
            if not ok.any():
                continue
            store.setdefault(c, []).append(t[ok])
    wres = {"file": f"data/volve/witsml_parsed/{w}.csv", "channels_missing": missing_ch}
    for c, parts in store.items():
        tt = np.unique(np.concatenate(parts))
        tt.sort()
        d = np.diff(tt)
        # longest continuous run at native cadence (<= 2x median gap)
        med = float(np.median(d)) if len(d) else None
        tol = (2.0 * med) if med else None
        best = cur = 1
        if len(d):
            for x in d:
                if x <= tol:
                    cur += 1
                    best = max(best, cur)
                else:
                    cur = 1
        wres[c] = {
            "n_samples": int(len(tt)),
            "span_hours": float((tt[-1] - tt[0]) / 3600.0),
            "median_dt_s": med,
            "p05_dt_s": float(np.percentile(d, 5)) if len(d) else None,
            "p95_dt_s": float(np.percentile(d, 95)) if len(d) else None,
            "max_gap_s": float(d.max()) if len(d) else None,
            "gaps_gt_60s": int((d > 60).sum()),
            "gaps_gt_300s": int((d > 300).sum()),
            "longest_contiguous_samples": int(best),
            "longest_contiguous_hours": float(best * med / 3600.0) if med else None,
            "nominal_hz": float(1.0 / med) if med else None,
        }
        print(f"  {w} {c}: n={len(tt)} med_dt={med}s hz={1/med if med else None} gaps>60s={int((d>60).sum())} longest={best}")
    res[w] = wres

with open(f"{OUT}/meas2_native_cadence.json", "w") as fh:
    json.dump(res, fh, indent=1)
print("WROTE", f"{OUT}/meas2_native_cadence.json")
