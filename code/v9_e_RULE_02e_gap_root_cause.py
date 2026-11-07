"""V9-E_RULE 02e-v2 — klasifikasi DEFINITIF 13 onset tanpa-anchor (koreksi 02e).

Koreksi: tes absorpsi memakai MENIT ELIG (non-inblock) BUKAN hor penuh.
Bukti smoking-gun per onset hilang: baris dataset dgn ts_bin di [t_e-10,t_e)
+ lab_kind mereka (onset_event dgn lab_ts siapa / horizon_neg / tak ada baris).
Klasifikasi:
  ABSORBED : semua baris y=1 di jendela punya lab_ts onset LAIN (t_eB>t_e).
  MASK-FAIL: tak ada baris ekspor sama sekali di jendela (mask gugur semua).
  PARTIAL  : sebagian baris punya anchor sendiri, sebagian pindah.
"""
import json
import numpy as np
import pandas as pd

BASE = "/mnt/d/Capstone 1(v2)"
WELLS = ["F-9", "F-9_A", "F-10", "F-14"]
H = 10
GAP_SEG = 30
SURF = ["TQA", "SPPA", "TFLO", "RPM", "SWOB", "HKLD", "ROP", "BPOS"]
SPMC = ["SPM1", "SPM2", "SPM3"]


def onsets_ffill(idx, vals):
    out, prev = [], None
    for t, v in zip(idx, vals):
        if np.isnan(v):
            continue
        if prev is not None and prev < 1 and v >= 1:
            out.append(t)
        prev = v
    return out


ds_all = pd.read_csv(f"{BASE}/scratch/v9_e_rule/repair/stuck_k2.csv.gz")
res = {}
for w in WELLS:
    p = f"{BASE}/data/volve/witsml_parsed/{w}.csv"
    hdr = pd.read_csv(p, nrows=0).columns.tolist()
    use = sorted(set(SURF + SPMC + ["STUCK_RT", "timestamp"]) & set(hdr))
    dtypes = {c: np.float32 for c in use if c != "timestamp"}
    parts = []
    for ch in pd.read_csv(p, usecols=use, chunksize=250_000,
                          low_memory=False, dtype=dtypes):
        parts.append(ch)
    df = pd.concat(parts, ignore_index=True)
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="ISO8601",
                                     utc=True, errors="coerce")
    df = df[df["timestamp"].notna()].sort_values("timestamp")
    df = df.drop_duplicates("timestamp", keep="last").set_index("timestamp")
    for c in df.columns:
        if df[c].dtype == object:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    base_idx = df.iloc[:, 0].resample("60s").mean().index
    g = pd.DataFrame(index=base_idx)
    for c in SURF:
        if c in df:
            g[c] = df[c].resample("60s").mean().to_numpy()
    if any(c in df for c in SPMC):
        g["SPM"] = df[[c for c in SPMC if c in df]].sum(
            axis=1, min_count=1).resample("60s").mean().to_numpy()
    ff = df["STUCK_RT"].ffill(limit=None)
    g["STUCK_ffill"] = ff.resample("60s").max().reindex(base_idx).to_numpy()
    del df, parts

    stuckf = (g["STUCK_ffill"] >= 1).fillna(False)
    on_f = onsets_ffill(g.index, g["STUCK_ffill"].to_numpy())
    on_minutes = [int(t.value // 10**9 // 60) for t in on_f]

    dsw = ds_all[ds_all["well"] == w]
    anchors = set(dsw.loc[dsw["lab_kind"] == "onset_event", "lab_ts"]
                  .astype("int64").unique().tolist())
    ev = dsw[dsw["lab_kind"] == "onset_event"]

    missing = []
    for t_e, m_e in zip(on_f, on_minutes):
        if m_e in anchors:
            continue
        hor = g.index[(g.index >= t_e - pd.Timedelta(minutes=H)) &
                      (g.index < t_e)]
        elig = hor[~stuckf.loc[hor].to_numpy()]
        elig_min = (elig.astype("int64") // 10**9 // 60).tolist()
        win = dsw[(dsw["ts_bin"] >= m_e - H) & (dsw["ts_bin"] < m_e)]
        ev_win = win[win["lab_kind"] == "onset_event"]
        lab_ts_win = sorted(set(ev_win["lab_ts"].astype("int64").tolist()))
        n_hor_exported = len(win)
        # klasifikasi
        if n_hor_exported == 0:
            kelas = "MASK-FAIL"
        elif len(ev_win) == 0:
            kelas = "NO-POSITIVE-ROW"
        elif all(lt != m_e for lt in lab_ts_win):
            kelas = "ABSORBED"
        else:
            kelas = "PARTIAL"
        # onset penyerap (semua lab_ts selain t_e sendiri)
        absorbers = [int(lt) for lt in lab_ts_win if lt != m_e]
        missing.append(dict(t_e=m_e, kelas=kelas, n_elig=len(elig),
                            elig_min=elig_min, n_rows_window=n_hor_exported,
                            n_pos_rows=len(ev_win),
                            lab_ts_in_window=lab_ts_win,
                            absorbers=absorbers,
                            absorber_delta_min=[lt - m_e for lt in absorbers]))
    res[w] = dict(n_onsets=len(on_f), n_anchors=len(anchors),
                  n_missing=len(missing), missing=missing)
    print(f"{w}: onsets={len(on_f)} anchors={len(anchors)} missing={len(missing)}")
    for m in missing:
        print("   ", m)

json.dump(res, open(f"{BASE}/scratch/v9_e_rule/v9_e_RULE_02e_gap_root_cause.json",
                    "w"), indent=1, default=str)
cls = {}
for r in res.values():
    for m in r["missing"]:
        cls[m["kelas"]] = cls.get(m["kelas"], 0) + 1
print("TOTAL missing:", sum(r["n_missing"] for r in res.values()), "|", cls)
