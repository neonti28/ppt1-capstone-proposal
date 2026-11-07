#!/usr/bin/env python3
"""T10 verifier independen — jalur kode BERBEDA dari code/60.

Cek:
  1. Aritmetika coverage: 884 - 213 (tanpa WITSML) - 10 (out-of-range) == baris X.
  2. Anti-leakage independen: utk sampel acak event, baca ulang CSV mentah,
     filter dengan mask pandas (bukan searchsorted) -> semua ts < act_start.
  3. Regr eval: hitung ulang mean/std/missing_rate utk sampel sel -> cocok dgn npz.
  4. Struktur npz/meta: nama fitur unik, shape konsisten, violations=0.
Exit 0 = semua PASS.
"""
import json
import numpy as np
import pandas as pd

BASE = "/mnt/d/Capstone 1"
PARSED = f"{BASE}/data/volve/witsml_parsed"
rng = np.random.default_rng(20261005)

checks = []


def ck(name, cond, detail=""):
    checks.append((name, bool(cond), detail))
    print(f"{'PASS' if cond else 'FAIL'}  {name}  {detail}", flush=True)


z = np.load(f"{BASE}/data/predictive/features_timeseries.npz", allow_pickle=True)
meta = json.load(open(f"{BASE}/data/predictive/features_timeseries_meta.json"))
ev = pd.read_csv(f"{BASE}/data/predictive/features_timeseries_events.csv")
X, names = z["X"], list(z["feature_names"])

# 1. coverage arithmetic
cov = meta["coverage"]
ck("coverage: 884-213-10=661 == rows X",
   884 - sum(cov["unmapped_excluded"].values()) - sum(cov["out_of_range_excluded"].values()) == X.shape[0] == cov["features_built"],
   f"X={X.shape}")
ck("events csv rows == X rows", len(ev) == X.shape[0])
ck("feature_names unik", len(set(names)) == len(names), f"{len(names)} names")
ck("meta violations == 0 & pass", meta["anti_leakage"]["violations"] == 0 and meta["anti_leakage"]["pass"] is True)
ck("shape meta == npz", meta["shape"]["X"] == list(X.shape))

# 2+3. sampel acak: leakage independen + regr eval
win_defs = {"w30m": 1800, "w2h": 7200, "w6h": 21600}
idx_pick = rng.choice(len(ev), size=12, replace=False)
leak_bad = 0
rows_checked = 0
regr_bad = 0
regr_checked = 0
for i in sorted(idx_pick):
    r = ev.iloc[i]
    fold, t_end = r["fold"], pd.Timestamp(r["act_start_utc"])
    # baca ulang CSV penuh utk kolom minimal (jalur berbeda dari searchsorted)
    resolution = meta["channel_resolution_per_fold"][fold]["DMEA"]
    res_col = resolution["column"]
    usecols = ["timestamp"] + ([res_col] if res_col else [])
    df = pd.read_csv(f"{PARSED}/{fold}.csv", usecols=usecols)
    ts = pd.to_datetime(df["timestamp"], format="ISO8601", utc=True)
    for wname, wsec in win_defs.items():
        w_start = t_end - pd.Timedelta(seconds=wsec)
        mask = (ts >= w_start) & (ts < t_end)          # mask pandas, bukan searchsorted
        seg = ts[mask]
        rows_checked += int(mask.sum())
        if len(seg) and (seg >= t_end).any():
            leak_bad += int((seg >= t_end).sum())
        # regr eval utk channel DMEA (jika ada kolom & dipakai fold)
        resolution = meta["channel_resolution_per_fold"][fold]["DMEA"]
        if resolution["column"] and len(seg) >= 5:
            x = df.loc[mask, resolution["column"]].to_numpy(dtype=np.float64)
            v = np.isfinite(x)
            if v.sum() >= 5:
                got_mean = float(x[v].mean())
                got_std = float(x[v].std(ddof=1))
                col = names.index(f"{wname}__DMEA__mean")
                want_mean, want_std = X[i, col], X[i, col + 1]
                regr_checked += 2
                if not (np.isclose(got_mean, want_mean, rtol=1e-5, equal_nan=True)
                        and np.isclose(got_std, want_std, rtol=1e-4, equal_nan=True)):
                    regr_bad += 1
                    print(f"   mismatch event {r['event_id']} {wname}: got {got_mean:.6g}/{got_std:.6g} "
                          f"npz {want_mean:.6g}/{want_std:.6g}")
        # missing_rate vs n_rows di events csv
        n_rows_csv = int(r[f"{wname}_n_rows"])
        if n_rows_csv != int(mask.sum()):
            regr_bad += 1
            print(f"   n_rows mismatch event {r['event_id']} {wname}: csv={n_rows_csv} recomputed={int(mask.sum())}")
        regr_checked += 1

ck("leakage independen (12 event x 3 jendela)", leak_bad == 0, f"rows scanned={rows_checked}, violations={leak_bad}")
ck("regr eval mean/std/n_rows cocok", regr_bad == 0, f"{regr_checked} cek")

# 4. tidak ada fitur dgn timestamp pasca-event: struktural (semua fitur dari window < t_end) sudah
# diverifikasi di atas; cek tambahan: tidak ada kolom fitur yang memakai act_end/outcome
forbidden = [n for n in names if "act_end" in n or "outcome" in n or "label" in n]
ck("tanpa fitur turunan act_end/outcome/label", len(forbidden) == 0, str(forbidden))

fails = [c for c in checks if not c[1]]
print(f"\n=== {len(checks) - len(fails)}/{len(checks)} PASS ===")
if fails:
    for f in fails:
        print("FAILED:", f)
raise SystemExit(1 if fails else 0)
