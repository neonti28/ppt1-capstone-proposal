#!/usr/bin/env python3
"""
21_validate_join.py — Validasi independen hasil code/20_join_md_time.py.

A. Baca ulang data/volve/usrop_timestamped.csv: struktur, jumlah baris, format ISO,
   distribusi join_status, apakah semua est_timestamp berada di dalam jendela kampanye
   wellbore bersangkutan.
B. Cross-check PEMETAAN + interpolasi memakai 884 event kegagalan DDR
   (data/volve/usrop_wellbores_events.csv) yang punya timestamp ASLI:
   untuk tiap event (wellbore, md, act_start) yang md-nya berada dalam jangkauan USROP,
   bandingkan est_timestamp hasil join pada md itu dengan act_start.
   Selisih kecil => pemetaan wellbore + interpolasi konsisten dengan kenyataan.
   Event di luar jendela kampanye (dilaporkan terpisah) memang tidak harus cocok
   karena kurva join merepresentasikan first-reach saat drilling.
"""
import importlib.util
import json
import os

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

spec = importlib.util.spec_from_file_location("join20", os.path.join(ROOT, "code", "20_join_md_time.py"))
join20 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(join20)

OUT_CSV = os.path.join(ROOT, "data", "volve", "usrop_timestamped.csv")
EVT_CSV = os.path.join(ROOT, "data", "volve", "usrop_wellbores_events.csv")


def main():
    print("=" * 70)
    print("A. STRUKTUR & KONSISTENSI OUTPUT")
    src = pd.read_csv(join20.USROP_PATH)
    out = pd.read_csv(OUT_CSV, dtype={"est_timestamp": str, "join_status": str},
                      keep_default_na=False, na_values=[])
    print(f"  baris input : {len(src)}")
    print(f"  baris output: {len(out)}  (match: {len(src) == len(out)})")
    print(f"  kolom output: {list(out.columns)}")
    print(f"  kolom baru ada: {'est_timestamp' in out.columns and 'join_status' in out.columns}")
    print(f"  kolom lama identik: {list(out.columns[:-2]) == list(src.columns)}")

    ts = pd.to_datetime(out["est_timestamp"].replace("", pd.NA), utc=True,
                        errors="coerce", format="ISO8601")
    empty = (out["est_timestamp"] == "").sum()
    bad = int(ts.isna().sum()) - int(empty)
    print(f"  est_timestamp kosong={empty}, tidak bisa diparse={bad}, terparse={int(ts.notna().sum())}")
    print(f"  distribusi join_status:\n{out['join_status'].value_counts().to_string()}")
    samp = out.loc[out["est_timestamp"] != "", "est_timestamp"].head(3).tolist()
    samp += out.loc[out["est_timestamp"] != "", "est_timestamp"].tail(2).tolist()
    print(f"  contoh nilai est_timestamp: {samp}")

    # semua est_timestamp harus berada di jendela kampanye wellbore masing-masing
    ddr = pd.read_parquet(join20.DDR_PATH)
    pairs, _, _, _ = join20.collect_pairs(ddr)
    win = {}
    for wb, prs in pairs.items():
        mds, tss = join20.build_anchor_curve(prs)
        if mds is not None:
            win[wb] = (float(np.min(tss)), float(np.max(tss)))
    viol = 0
    for well_name, wb in join20.WELL_MAP.items():
        if wb not in win:
            continue
        m = (out["well"] == well_name).to_numpy()
        t = ts[m].dropna()
        lo, hi = win[wb]
        # datetime bisa berunit s/ms/us/ns -> bagi faktor konversi ke epoch detik
        scale = {"s": 1.0, "ms": 1e3, "us": 1e6, "ns": 1e9}[t.dtype.unit]
        epoch = t.astype("int64").to_numpy(dtype="float64") / scale
        v = int(((epoch < lo) | (epoch > hi)).sum())
        viol += v
        print(f"  {well_name:<28} -> {wb:<16} di luar jendela kampanye: {v}")
    print(f"  TOTAL est_timestamp di luar jendela kampanye: {viol}")

    print("=" * 70)
    print("B. CROSS-CHECK DENGAN EVENT DDR BER-TIMESTAMP ASLI")
    ev = pd.read_csv(EVT_CSV)
    print(f"  total event: {len(ev)}; kolom: {list(ev.columns)}")
    ev["md"] = pd.to_numeric(ev["md"], errors="coerce")
    ev["act_start"] = pd.to_datetime(ev["act_start"], utc=True, errors="coerce")
    wb2usrop = {v: k for k, v in join20.WELL_MAP.items()}

    curves = {}
    for wb in wb2usrop:
        mds, tss = join20.build_anchor_curve(pairs[wb])
        curves[wb] = (mds, tss, win[wb])

    rows = []
    for _, r in ev.iterrows():
        wb = r["wellbore"]
        if wb not in wb2usrop or wb not in curves or pd.isna(r["md"]) or pd.isna(r["act_start"]):
            continue
        mds, tss, (lo, hi) = curves[wb]
        x = float(r["md"])
        if x < mds[0] or x > mds[-1]:
            continue
        est = float(np.interp(x, mds, tss))
        diff_d = (est - r["act_start"].timestamp()) / 86400.0
        in_window = lo <= r["act_start"].timestamp() <= hi
        rows.append(dict(wellbore=wb, usrop=wb2usrop[wb], md=x,
                         t_event=r["act_start"].isoformat(),
                         diff_days=diff_d, in_window=in_window))

    df = pd.DataFrame(rows)
    print(f"  event teruji (md dalam jangkauan USROP): {len(df)}")
    agg = df.groupby("wellbore").agg(
        n=("diff_days", "size"),
        n_in_window=("in_window", "sum"),
        med_abs=("diff_days", lambda s: round(float(np.median(np.abs(s))), 3)),
        p90_abs=("diff_days", lambda s: round(float(np.percentile(np.abs(s), 90)), 3)),
        max_abs=("diff_days", lambda s: round(float(np.max(np.abs(s))), 3)),
        signed_med=("diff_days", lambda s: round(float(np.median(s)), 3)),
    )
    print(agg.to_string())
    if len(w := df[df["in_window"]]):
        agg_w = w.groupby("wellbore").agg(
            n=("diff_days", "size"),
            med_abs=("diff_days", lambda s: round(float(np.median(np.abs(s))), 3)),
            p90_abs=("diff_days", lambda s: round(float(np.percentile(np.abs(s), 90)), 3)),
            max_abs=("diff_days", lambda s: round(float(np.max(np.abs(s))), 3)),
            signed_med=("diff_days", lambda s: round(float(np.median(s)), 3)),
        )
        print("\n  --- hanya event di dalam jendela kampanye drilling ---")
        print(agg_w.to_string())
        a = np.abs(w["diff_days"].to_numpy())
        print(f"\n  HANYA event di dalam jendela kampanye (n={len(w)}): "
              f"median|diff|={np.median(a):.3f} hari, p90={np.percentile(a, 90):.3f}, "
              f"max={a.max():.3f}, signed median={np.median(w['diff_days']):.3f} hari")
        print(f"  (signed median mendekati 0 => timeline join tidak meleset sistematis)")
    df.to_csv(os.path.join(ROOT, "docs", "V2_EVENT_CROSSCHECK.csv"), index=False)
    print("  detail -> docs/V2_EVENT_CROSSCHECK.csv")


if __name__ == "__main__":
    main()
