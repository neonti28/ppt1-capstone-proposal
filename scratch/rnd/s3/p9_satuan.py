import pandas as pd

t = pd.read_csv("/mnt/d/Capstone 1(v2)/data/volve/usrop_timestamped.csv")
ts = pd.to_datetime(t["est_timestamp"], errors="coerce", utc=True)
print("dtype", ts.dtype, "| unit", getattr(ts.dtype, "unit", "?"))
a = ts.astype("int64").iloc[0]
b = (ts - pd.Timestamp("1970-01-01", tz="UTC")).dt.total_seconds().iloc[0]
print("astype(int64)      ", a, "(satuan mengikuti dtype, yaitu mikrodetik)")
print("total_seconds      ", b)
print("rasio a/b          ", a / b if b else None)
g = t.assign(ts=ts)
for w, gg in g.groupby("well"):
    ok = gg["ts"].notna()
    m_ok = (gg.loc[ok, "ts"] - pd.Timestamp("1970-01-01", tz="UTC")).dt.total_seconds() / 60.0
    m_raw = gg.loc[ok, "ts"].astype("int64") / 1e9 / 60.0
    print(f"{w[:26]:28s} uniq_benar={m_ok.nunique():5d} uniq_raw={m_raw.nunique():5d} "
          f"span_jam_benar={(m_ok.max()-m_ok.min())/60.0:9.2f} span_jam_raw={(m_raw.max()-m_raw.min())/60.0:8.2f}")
