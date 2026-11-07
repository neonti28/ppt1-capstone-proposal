#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
code/20_predictive_dataset.py — Bangun dataset PREDIKTIF t+Delta (Capstone V2)

Task kanban : t_e7e9bd6d [ML Engineer] Dataset prediktif t+Delta + baseline RF & autoencoder
Prinsip      : fitur = data SEBELUMNYA (window [md-W, md], 12 sensor asli saja),
               label = apakah event terjadi dalam [md, md+Delta] ke depan.

Sumber (read-only):
  data/volve/usrop_timestamped.csv   198.928 baris = 12 sensor + well + kolom lama + est_timestamp
  data/volve/labels_curated.csv      884 event terkurasi (md + act_start + wellbore)

Output:
  data/predictive/dataset_prediktif.csv                (artefak wajib)
  docs/V2_PREDICTIVE_DATASET_METRICS.json              (metrik mentah)
  stdout ringkasan -> log eksekusi

Desain (mengikuti docs/V2_RND_METHODS.md §3.1-3.2):
  * Delta utama = 10 m; sensitivitas Delta = {5, 15, 30} m.
  * Label  y_Delta = 1  bila ada event dengan md in [md_t, md_t + Delta]  (event = next event di atas md_t)
  * Fitur  = window [md_t - W, md_t], W = 10 m, statistik mean/std/first/last/delta
             dari 12 parameter sensor ASLI. TIDAK memakai MSE / D_exp / ROC_coef / label lama
             (anti-leakage, F4 di 11_PLAN).
  * Sampling = baris dengan est_timestamp valid (join_status == 'interpolated').
  * Timestamp dipakai untuk: (a) filter sampling, (b) split temporal nanti,
    (c) cross-check depth-vs-waktu untuk baris positif (dilaporkan apa adanya).

Anti-halusinasi: semua angka dihitung di sini dari file, tidak ada estimasi manual.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
USROP_PATH = BASE / "data" / "volve" / "usrop_timestamped.csv"
LABELS_PATH = BASE / "data" / "volve" / "labels_curated.csv"
OUT_DIR = BASE / "data" / "predictive"
OUT_CSV = OUT_DIR / "dataset_prediktif.csv"
METRICS_JSON = BASE / "docs" / "V2_PREDICTIVE_DATASET_METRICS.json"

# --- Pemetaan well USROP -> wellbore DDR (SAMA PERSIS dengan code/20_join_md_time.py) ---
WELL_MAP = {
    "USROP_A 0 N-NA_F-9_Ad.csv": "NO 15/9-F-9 A",
    "USROP_A 1 N-S_F-7d.csv": "NO 15/9-F-7",
    "USROP_A 2 N-SH_F-14d.csv": "NO 15/9-F-14",
    "USROP_A 3 N-SH-F-15d.csv": "NO 15/9-F-15 A",
    "USROP_A 4 N-SH_F-15Sd.csv": "NO 15/9-F-15",
    "USROP_A 5 N-SH-F-5d.csv": "NO 15/9-F-5",
    "USROP_A 6 N-SH_F-9d.csv": "NO 15/9-F-9",
}

# --- 12 parameter sensor ASLI (satu-satunya sumber fitur) ---
SENSORS = [
    "Measured Depth m",
    "Weight on Bit kkgf",
    "Average Standpipe Pressure kPa",
    "Average Surface Torque kN.m",
    "Rate of Penetration m/h",
    "Average Rotary Speed rpm",
    "Mud Flow In L/min",
    "Mud Density In g/cm3",
    "Diameter mm",
    "Average Hookload kkgf",
    "Hole Depth (TVD) m",
    "USROP Gamma gAPI",
]
FORBIDDEN = ["MSE", "D_exp", "ROC_coef", "label"]  # dilarang jadi fitur (leakage)

W_LOOKBACK_M = 10.0           # W = 10 m (RND §3.2)
DELTA_MAIN = 10.0             # Delta utama (RND §3.1)
DELTAS = [5.0, 10.0, 15.0, 30.0]
STATS = ["mean", "std", "first", "last", "delta"]


def slug(col: str) -> str:
    """Nama kolom fitur yang aman: 'Average Surface Torque kN.m' -> 'surface_torque_knm'."""
    s = col.lower()
    for a, b in [("measured depth m", "md"), ("weight on bit kkgf", "wob"),
                 ("average standpipe pressure kpa", "spp"),
                 ("average surface torque kn.m", "torque"),
                 ("rate of penetration m/h", "rop"),
                 ("average rotary speed rpm", "rpm"),
                 ("mud flow in l/min", "flow"),
                 ("mud density in g/cm3", "mud_density"),
                 ("diameter mm", "diameter"),
                 ("average hookload kkgf", "hookload"),
                 ("hole depth (tvd) m", "tvd"),
                 ("usrop gamma gapi", "gamma")]:
        if s == a:
            return b
    return "".join(ch if ch.isalnum() else "_" for ch in s)


def fail(msg: str) -> None:
    print(f"FATAL: {msg}", flush=True)
    sys.exit(1)


def window_stats(md_sorted: np.ndarray, x_sorted: np.ndarray, W: float):
    """Statistik window [md-W, md] per baris (md_sorted naik). O(N) via cumsum."""
    n = md_sorted.size
    c1 = np.concatenate(([0.0], np.cumsum(x_sorted, dtype=np.float64)))
    c2 = np.concatenate(([0.0], np.cumsum(x_sorted * x_sorted, dtype=np.float64)))
    left = np.searchsorted(md_sorted, md_sorted - W, side="left")
    idx = np.arange(n)
    cnt = (idx - left + 1).astype(np.float64)
    s1 = c1[idx + 1] - c1[left]
    s2 = c2[idx + 1] - c2[left]
    mean = s1 / cnt
    var = np.maximum(s2 / cnt - mean * mean, 0.0)
    std = np.sqrt(var)
    first = x_sorted[left]
    last = x_sorted[idx]
    delta = last - first
    return mean, std, first, last, delta


def main() -> None:
    t0 = time.time()
    print("=" * 78)
    print("20_predictive_dataset.py — bangun dataset prediktif t+Delta")
    print("=" * 78)

    # ---------------- 1. muat & bersihkan ----------------
    usrop = pd.read_csv(USROP_PATH)
    n_raw = len(usrop)
    print(f"[1] usrop_timestamped.csv dimuat: {n_raw} baris, {usrop.shape[1]} kolom")
    if n_raw != 198_928:
        fail(f"jumlah baris USROP {n_raw} != 198928 (data berubah?)")

    missing = [c for c in SENSORS + FORBIDDEN + ["well", "est_timestamp", "join_status",
                                                  "Measured Depth m"] if c not in usrop.columns]
    if missing:
        fail(f"kolom hilang: {missing}")

    # sampling: est_timestamp valid
    usrop["row_id"] = np.arange(n_raw, dtype=np.int64)
    keep = (usrop["join_status"] == "interpolated") & usrop["est_timestamp"].notna()
    n_drop_status = int((~(usrop["join_status"] == "interpolated")).sum())
    n_drop_ts = int(usrop["est_timestamp"].isna().sum())
    df = usrop.loc[keep].copy()
    print(f"[1] sampling: {len(df)} baris est_timestamp valid "
          f"(buang join_status!=interpolated: {n_drop_status}; est_timestamp kosong: {n_drop_ts})")

    unknown_wells = sorted(set(df["well"].dropna().unique()) - set(WELL_MAP))
    if unknown_wells:
        fail(f"nilai 'well' tanpa pemetaan: {unknown_wells}")
    df["wellbore"] = df["well"].map(WELL_MAP)

    # cek NaN/inf sensor
    nan_report = {}
    for c in SENSORS:
        s = pd.to_numeric(df[c], errors="coerce")
        n_nan = int(s.isna().sum())
        n_inf = int(np.isinf(s.to_numpy(dtype=float, na_value=np.nan)).sum())
        if n_nan or n_inf:
            nan_report[c] = {"nan": n_nan, "inf": n_inf}
    if nan_report:
        print(f"[1] PERINGATAN sensor NaN/inf: {nan_report}")
        for c in SENSORS:
            df[c] = pd.to_numeric(df[c], errors="coerce").ffill().bfill()
    else:
        print("[1] 12 sensor: 0 NaN, 0 inf (setelah filter sampling)")

    # ---------------- 2. event terkurasi ----------------
    ev_all = pd.read_csv(LABELS_PATH)
    mapped_wbs = sorted(set(WELL_MAP.values()))
    ev = ev_all[ev_all["wellbore"].isin(mapped_wbs)].copy()
    n_ev_mapped_wb = len(ev)
    ev = ev[ev["md_valid"] == True].copy()  # noqa: E712
    ev["md"] = pd.to_numeric(ev["md"], errors="coerce")
    ev = ev[ev["md"].notna() & (ev["md"] > 0)].copy()
    ev["act_start_dt"] = pd.to_datetime(ev["act_start"], errors="coerce", utc=True)
    ev = ev[ev["act_start_dt"].notna()].copy()
    n_ev_usable = len(ev)
    print(f"[2] event: total {len(ev_all)} -> wellbore terpetakan {n_ev_mapped_wb} "
          f"-> md_valid & md>0 & act_start valid = {n_ev_usable} dipakai")

    # ---------------- 3. window fitur per well ----------------
    feat_cols = [f"{st}_{slug(c)}" for c in SENSORS for st in STATS]
    out = pd.DataFrame(index=df.index)
    out["row_id"] = df["row_id"].to_numpy()
    out["well"] = df["well"].to_numpy()
    out["wellbore"] = df["wellbore"].to_numpy()
    out["md"] = pd.to_numeric(df["Measured Depth m"], errors="coerce").to_numpy(dtype=float)
    out["est_timestamp"] = df["est_timestamp"].to_numpy()

    n_rows_win = 0
    for well, g in df.groupby("well", sort=False):
        idx = g.index.to_numpy()
        md = out.loc[idx, "md"].to_numpy(dtype=float)
        order = np.argsort(md, kind="stable")
        idx_s = idx[order]
        md_s = md[order]
        if not np.all(np.isfinite(md_s)):
            fail(f"md non-finite di well {well}")
        for c in SENSORS:
            x = pd.to_numeric(g[c], errors="coerce").to_numpy(dtype=float)[order]
            x = np.nan_to_num(x, nan=0.0, posinf=0.0, neginf=0.0)
            mean, std, first, last, delta = window_stats(md_s, x, W_LOOKBACK_M)
            base = slug(c)
            out.loc[idx_s, f"mean_{base}"] = mean
            out.loc[idx_s, f"std_{base}"] = std
            out.loc[idx_s, f"first_{base}"] = first
            out.loc[idx_s, f"last_{base}"] = last
            out.loc[idx_s, f"delta_{base}"] = delta
        n_rows_win += md_s.size
        # lebar window aktual per well (diagnosis: 10 m kira-kira berapa baris)
        sp = np.diff(md_s)
        rows_per_10m = W_LOOKBACK_M * (md_s.size - 1) / (md_s.max() - md_s.min())
        print(f"    {well}: {md_s.size} baris, md {md_s.min():.1f}-{md_s.max():.1f} m, "
              f"spasi median {np.median(sp):.4f} m -> window 10 m ~ {rows_per_10m:.0f} baris (rata-rata)")
    if n_rows_win != len(out):
        fail("jumlah baris window != jumlah baris sampling")

    # ---------------- 4. label t+Delta + lead distance ----------------
    n_marked = {}
    ev_range = {}
    for D in DELTAS:
        out[f"y_{int(D)}"] = np.int8(0)
    out["lead_m"] = np.nan            # jarak md ke event terdekat BERIKUTNYA (md_e - md_t)
    out["next_event_id"] = -1
    out["next_event_md"] = np.nan
    out["next_event_ts"] = ""

    for wb, g in out.groupby("wellbore", sort=False):
        ev_w = ev[ev["wellbore"] == wb].sort_values("md")
        idx = g.index.to_numpy()
        md_t = g["md"].to_numpy(dtype=float)
        if len(ev_w) == 0:
            continue
        ev_md = ev_w["md"].to_numpy(dtype=float)
        ev_id = ev_w["event_id"].to_numpy()
        ev_ts = ev_w["act_start"].astype(str).to_numpy()
        # event pertama dengan md >= md_t
        j = np.searchsorted(ev_md, md_t, side="left")
        has_next = j < len(ev_md)
        lead = np.full(md_t.shape, np.nan)
        nid = np.full(md_t.shape, -1, dtype=np.int64)
        nmd = np.full(md_t.shape, np.nan)
        nts = np.array([""] * md_t.shape[0], dtype=object)
        jj = np.clip(j, 0, len(ev_md) - 1)
        lead[has_next] = ev_md[jj[has_next]] - md_t[has_next]
        nid[has_next] = ev_id[jj[has_next]]
        nmd[has_next] = ev_md[jj[has_next]]
        nts[has_next] = ev_ts[jj[has_next]]
        out.loc[idx, "lead_m"] = lead
        out.loc[idx, "next_event_id"] = nid
        out.loc[idx, "next_event_md"] = nmd
        out.loc[idx, "next_event_ts"] = nts
        for D in DELTAS:
            pos = has_next & (lead <= D)
            out.loc[idx, f"y_{int(D)}"] = pos.astype(np.int8)
        # event yang benar-benar punya peluang menandai baris (rentang USROP +/- Delta max)
        md_lo, md_hi = md_t.min(), md_t.max()
        dmax = float(max(DELTAS))
        marked = int(((ev_md >= md_lo - dmax) & (ev_md <= md_hi + dmax)).sum())
        ev_range[wb] = {
            "n_event_md_valid": int(len(ev_md)),
            "n_md_dalam_rentang_usrop": int(((ev_md >= md_lo) & (ev_md <= md_hi)).sum()),
            "n_event_diatas_td_usrop": int((ev_md > md_hi).sum()),
            "n_event_di_bawah_shoe_usrop": int((ev_md < md_lo).sum()),
            "n_event_potensi_menandai": marked,
            "usrop_md_range": [float(md_lo), float(md_hi)],
        }
    for D in DELTAS:
        n_marked[int(D)] = int(out[f"y_{int(D)}"].sum())
    # event yang benar-benar menandai >=1 baris positif (Delta utama)
    n_event_marked_main = int(out.loc[out[f"y_{int(DELTA_MAIN)}"] == 1, "next_event_id"].nunique())

    # ---------------- 5. cross-check depth vs waktu (baris positif Delta utama) ----------------
    ycol = f"y_{int(DELTA_MAIN)}"
    pos = out[out[ycol] == 1].copy()
    if len(pos):
        pos_dt = pd.to_datetime(pos["est_timestamp"], errors="coerce", utc=True)
        ev_dt = pd.to_datetime(pos["next_event_ts"], errors="coerce", utc=True)
        diff_days = (ev_dt - pos_dt).dt.total_seconds() / 86400.0
        xcheck = {
            "n_positif_delta_main": int(len(pos)),
            "frac_est_ts_sebelum_event": float((diff_days >= 0).mean()),
            "frac_est_ts_dalam_3_hari_setelah_event": float(((diff_days >= -3) & (diff_days < 0)).mean()),
            "median_diff_hari": float(diff_days.median()),
            "p10_diff_hari": float(diff_days.quantile(0.10)),
            "p90_diff_hari": float(diff_days.quantile(0.90)),
        }
    else:
        xcheck = {"n_positif_delta_main": 0}
    print(f"[4] label: " + ", ".join(f"Delta {D}m -> {n_marked[int(D)]} positif "
                                     f"({n_marked[int(D)]/len(out)*100:.2f}%)"
                                     for D in DELTAS))
    if xcheck.get("n_positif_delta_main"):
        print(f"[5] cross-check waktu (Delta {DELTA_MAIN}m): "
              f"est_timestamp <= act_start event = {xcheck['frac_est_ts_sebelum_event']*100:.1f}% "
              f"baris; median selisih {xcheck['median_diff_hari']:.3f} hari "
              f"(p10 {xcheck['p10_diff_hari']:.3f}, p90 {xcheck['p90_diff_hari']:.3f})")

    # ---------------- 6. tulis artefak ----------------
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ordered = (["row_id", "well", "wellbore", "md", "est_timestamp",
                "lead_m", "next_event_id", "next_event_md", "next_event_ts"]
               + [f"y_{int(D)}" for D in DELTAS]
               + feat_cols)
    out = out[ordered]
    out.to_csv(OUT_CSV, index=False, float_format="%.6g")
    n_col_csv = len(ordered)
    size = OUT_CSV.stat().st_size
    print(f"[6] tulis {OUT_CSV} = {len(out)} baris x {n_col_csv} kolom, {size} byte")

    # verifikasi baca ulang
    chk = pd.read_csv(OUT_CSV, nrows=5)
    if list(chk.columns) != ordered:
        fail("kolom hasil baca ulang != kolom yang ditulis")
    forbidden_in_csv = [c for c in chk.columns if c in FORBIDDEN]
    if forbidden_in_csv:
        fail(f"kolom terlarang ikut tertulis: {forbidden_in_csv}")

    # distribusi kelas per well
    dist_per_well = {}
    for well, g in out.groupby("well", sort=False):
        dist_per_well[well] = {f"y_{int(D)}": {"pos": int(g[f'y_{int(D)}'].sum()),
                                               "n": int(len(g)),
                                               "prev": round(float(g[f'y_{int(D)}'].mean()), 5)}
                               for D in DELTAS}

    metrics = {
        "script": "code/20_predictive_dataset.py",
        "runtime_s": round(time.time() - t0, 1),
        "inputs": {
            "usrop_timestamped_rows": n_raw,
            "labels_curated_rows": int(len(ev_all)),
        },
        "sampling": {
            "rows_valid_timestamp": int(len(out)),
            "dropped_join_status": n_drop_status,
            "dropped_null_timestamp": n_drop_ts,
        },
        "events": {
            "total": int(len(ev_all)),
            "wellbore_mapped": n_ev_mapped_wb,
            "usable_md_valid": n_ev_usable,
            "excluded_wellbore_no_usrop": int(len(ev_all) - n_ev_mapped_wb),
            "events_marking_positive_rows_delta_main": n_event_marked_main,
            "per_wellbore": ev_range,
        },
        "params": {"W_lookback_m": W_LOOKBACK_M, "delta_main_m": DELTA_MAIN,
                   "deltas_m": DELTAS, "stats": STATS, "n_sensors": len(SENSORS),
                   "n_features": len(feat_cols)},
        "class_distribution": {f"y_{int(D)}": {"pos": n_marked[int(D)],
                                               "n": int(len(out)),
                                               "prev": round(n_marked[int(D)] / len(out), 5)}
                               for D in DELTAS},
        "class_distribution_per_well": dist_per_well,
        "timestamp_crosscheck_delta_main": xcheck,
        "sensor_nan_report": nan_report,
        "output": {"path": str(OUT_CSV), "rows": int(len(out)),
                   "cols": n_col_csv, "bytes": size,
                   "forbidden_columns_absent": forbidden_in_csv == []},
    }
    METRICS_JSON.write_text(json.dumps(metrics, indent=2, ensure_ascii=False))
    print(f"[7] metrics -> {METRICS_JSON}")
    print(f"SELESAI dalam {time.time()-t0:.1f}s")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:  # error handling: gagal keras = exit 1 + traceback
        import traceback
        traceback.print_exc()
        sys.exit(1)
