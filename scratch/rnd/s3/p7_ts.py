import pandas as pd

P = "/mnt/d/Capstone 1(v2)/data/volve/usrop_timestamped.csv"
t = pd.read_csv(P)
print(t.shape, list(t.columns))
ts = pd.to_datetime(t["est_timestamp"], errors="coerce", utc=True)
print("nat", int(ts.isna().sum()))
for w, g in t.groupby("well"):
    tt = pd.to_datetime(g["est_timestamp"], errors="coerce", utc=True)
    ok = tt.notna()
    m = (tt[ok].astype("int64") // 10**9 // 60)
    print(f"{w[:28]:30s} n={len(g):6d} finite={int(ok.sum()):6d} uniq_menit={m.nunique():6d} "
          f"span_jam={(m.max()-m.min())/60.0:10.3f} uniq_ts={tt[ok].nunique():6d}")
print(t["est_timestamp"].head(3).tolist())
print(t.loc[t["well"].str.contains("F-9_A", na=False), "est_timestamp"].head(5).tolist())
