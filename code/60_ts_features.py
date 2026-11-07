#!/usr/bin/env python3
"""T10 — Fitur time-series WITSML (window pra-event) anti-leakage.

Sumber :
  - data/volve/labels_curated_v2.csv        (884 event, kolom act_start = anchor)
  - data/volve/witsml_parsed/*.csv          (hasil T9, 7 fold; VAR_F-5_alt TIDAK dipakai)
  - data/volve/witsml_parsed/_verify.json   (fill-rate per channel per fold, threshold 50%)

Pemetaan label wellbore -> fold CSV (dipakai ulang dari code/51 FOLD2LABEL, rantai bukti):
  USROP_A N (nama file mentah) == nama folder WITSML  ->  fold CSV (lihat _parse_summary.json)
  USROP_A N -> label wellbore (V2_DATA_JOIN_REPORT, join 99,998% utk A4)
    A0 F-9 A -> F-9_A.csv   A1 F-7 -> F-7.csv     A2 F-14 -> F-14.csv
    A3 F-15  -> F-15A.csv   A4 F-15S -> F-15_S.csv A5 F-5 -> F-5.csv
    A6 F-9   -> F-9.csv
  Label F-15 B/C/D (213 event) = TIDAK punya CSV WITSML -> dikecualikan, dicatat.

Anti-leakage: SEMUA sampel fitur diambil dari timestamp < act_start (window [t-W, t)).
Cek otomatis dihitung per baris yang dipakai; violations WAJIB 0.

Output:
  data/predictive/features_timeseries.npz
  data/predictive/features_timeseries_meta.json
  data/predictive/features_timeseries_events.csv   (audit per event)
"""
from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timezone

import numpy as np
import pandas as pd

BASE = "/mnt/d/Capstone 1"
PARSED = os.path.join(BASE, "data/volve/witsml_parsed")
LABELS = os.path.join(BASE, "data/volve/labels_curated_v2.csv")
OUT_NPZ = os.path.join(BASE, "data/predictive/features_timeseries.npz")
OUT_META = os.path.join(BASE, "data/predictive/features_timeseries_meta.json")
OUT_EVENTS = os.path.join(BASE, "data/predictive/features_timeseries_events.csv")

# --- fold CSV -> label wellbore (code/51 FOLD2LABEL; rantai bukti di docstring) ---
FOLD2LABEL = {
    "F-9_A":  "NO 15/9-F-9 A",
    "F-7":    "NO 15/9-F-7",
    "F-14":   "NO 15/9-F-14",
    "F-15A":  "NO 15/9-F-15 A",
    "F-15_S": "NO 15/9-F-15",
    "F-5":    "NO 15/9-F-5",
    "F-9":    "NO 15/9-F-9",
}
LABEL2FOLD = {v: k for k, v in FOLD2LABEL.items()}

# --- channel kanonik (fisik, bukan alias) -------------------------------------
# Ketersediaan (>=50% fill, kolom base ATAU varian GS_) di 7 fold:
#   7/7 : DMEA DBTM DVER BPOS SWOB HKLD TQA SPPA TFLO MWTI ROP GASA CHKP SPM1
#   6/7 : RPM (absen di F-9)   5/7 : MDOA (absen di F-15_S, F-9)
# ACTC (rig mode, diskret) sengaja TIDAK dimasukkan: mean tidak bermakna.
CHANNELS = ["DMEA", "DBTM", "DVER", "BPOS", "SWOB", "HKLD", "TQA", "RPM",
            "SPPA", "TFLO", "MWTI", "MDOA", "ROP", "GASA", "CHKP", "SPM1"]

STATS = ["mean", "std", "min", "max", "slope_per_min", "trend_rho",
         "delta_mean", "delta_absmean", "burstiness", "missing_rate"]

# Jendela: 30m (pendahulu segera), 2h (siklus stand/koneksi), 6h (konteks shift)
WINDOWS = [("w30m", 30 * 60), ("w2h", 2 * 3600), ("w6h", 6 * 3600)]
PRIMARY = "w2h"

MIN_VALID = 5          # minimal sampel valid utk statistik selain missing_rate
EPS = 1e-12

CH_STATS = [s for s in STATS if s != "missing_rate"]  # selalu bisa dihitung (missing_rate)


def log(msg: str) -> None:
    print(f"[{datetime.now(timezone.utc).strftime('%H:%M:%S')}] {msg}", flush=True)


def ols_slope(y: np.ndarray, t_min: np.ndarray) -> float:
    """Slope OLS y ~ t (per menit). y & t_min sudah difilter finite."""
    if y.size < 2:
        return np.nan
    tc = t_min - t_min.mean()
    den = float((tc * tc).sum())
    if den <= 0:
        return np.nan
    yc = y - y.mean()
    return float((tc * yc).sum() / den)


def spearman_rho(y: np.ndarray, t: np.ndarray) -> float:
    """Spearman rho tanpa scipy.stats (rankdata via pandas, tie = average rank)."""
    if y.size < 3:
        return np.nan
    ry = pd.Series(y).rank().to_numpy()
    rt = pd.Series(t).rank().to_numpy()
    sy, st = ry.std(), rt.std()
    if sy <= 0 or st <= 0:
        return np.nan
    return float(np.corrcoef(ry, rt)[0, 1])


def channel_stats(x: np.ndarray, t_sec: np.ndarray) -> dict:
    """Statistik 1 channel di dalam 1 jendela.
    x: nilai (float, boleh NaN), t_sec: detik sejak awal jendela (per baris).
    TANPA interpolasi: gap antar-sampel dicatat terpisah oleh pemanggil.
    """
    out = {}
    n_rows = x.size
    if n_rows == 0:
        out["missing_rate"] = np.nan
        for s in CH_STATS:
            out[s] = np.nan
        return out
    valid = np.isfinite(x)
    n_valid = int(valid.sum())
    out["missing_rate"] = 1.0 - n_valid / n_rows
    if n_valid < MIN_VALID:
        for s in CH_STATS:
            out[s] = np.nan
        return out
    xv = x[valid]
    tv = t_sec[valid]
    out["mean"] = float(xv.mean())
    out["std"] = float(xv.std(ddof=1)) if n_valid >= 2 else np.nan
    out["min"] = float(xv.min())
    out["max"] = float(xv.max())
    out["slope_per_min"] = ols_slope(xv, tv / 60.0)
    out["trend_rho"] = spearman_rho(xv, tv)
    if n_valid >= 3:
        d = np.diff(xv)
        out["delta_mean"] = float(d.mean())
        out["delta_absmean"] = float(np.abs(d).mean())
        sd_level = float(xv.std(ddof=1))
        out["burstiness"] = float(d.std(ddof=1) / sd_level) if sd_level > EPS else np.nan
    else:
        out["delta_mean"] = np.nan
        out["delta_absmean"] = np.nan
        out["burstiness"] = np.nan
    return out


def main() -> int:
    t_start = time.time()
    violations = 0          # anti-leakage: jumlah sampel dengan ts >= act_start yang terpakai
    rows_scanned = 0        # jumlah sampel (event x jendela) yang diperiksa utk leakage

    # ---------- 1. labels ----------
    lab = pd.read_csv(LABELS)
    lab["act_start_utc"] = pd.to_datetime(lab["act_start"], format="ISO8601", utc=True)
    n_total = len(lab)
    log(f"labels: {n_total} baris, act_start NaT={int(lab['act_start_utc'].isna().sum())}")

    lab["fold"] = lab["wellbore"].map(LABEL2FOLD)
    unmapped = lab[lab["fold"].isna()]
    excl_unmapped = unmapped["wellbore"].value_counts().to_dict()
    lab = lab[lab["fold"].notna()].copy()
    log(f"mapped: {len(lab)} | unmapped (tanpa WITSML): {len(unmapped)} -> {excl_unmapped}")

    verify = json.load(open(os.path.join(PARSED, "_verify.json")))

    # range per fold (pakai _verify.json, sumber yg sama dgn T9)
    fold_range = {}
    for f in FOLD2LABEL:
        tmin = pd.Timestamp(verify[f]["t_min_utc"])
        tmax = pd.Timestamp(verify[f]["t_max_utc"])
        fold_range[f] = (tmin, tmax)

    in_mask = []
    for _, r in lab.iterrows():
        tmin, tmax = fold_range[r["fold"]]
        in_mask.append(bool(tmin <= r["act_start_utc"] <= tmax))
    lab["in_range"] = in_mask
    out_of_range = lab[~lab["in_range"]]
    excl_oor = out_of_range.groupby("fold").size().to_dict()
    lab = lab[lab["in_range"]].copy()
    log(f"in-range (act_start dalam rentang CSV): {len(lab)} | out-of-range: {len(out_of_range)} -> {excl_oor}")

    # ---------- 2. susun matriks fitur ----------
    feat_names = [f"{w}__{ch}__{st}" for w, _ in WINDOWS for ch in CHANNELS for st in STATS]
    n_feat = len(feat_names)
    baseline_names = (["md_mean", "md_std", "md_min", "md_max", "md_slope_per_min",
                       "md_last", "md_delta"]
                      + ["time_hour_sin", "time_hour_cos", "time_dow_sin", "time_dow_cos"])
    winmeta_names = [f"{w}__{s}" for w, _ in WINDOWS
                     for s in ["n_rows", "gap_median_s", "gap_max_s", "full_window"]]
    n = len(lab)
    X = np.full((n, n_feat), np.nan, dtype=np.float32)
    XB = np.full((n, len(baseline_names)), np.nan, dtype=np.float32)
    XM = np.full((n, len(winmeta_names)), np.nan, dtype=np.float32)

    ch_resolution = {}   # fold -> {channel: {"column": str|None, "file_fill": float|None}}
    fill_agg = {}        # fold -> {channel: mean missing_rate across events (w6h)}
    zero_row_windows = 0
    partial_windows = 0

    lab = lab.sort_values(["fold", "act_start_utc"]).reset_index(drop=True)
    lab["row"] = np.arange(len(lab))

    for fold, g in lab.groupby("fold"):
        t0 = time.time()
        fmeta = verify[fold]
        fill = fmeta["fill_rate_ge_50pct"]
        # resolusi channel: kolom base jika >=50%, else varian GS_, else tidak eligible
        resolution = {}
        usecols = ["timestamp"]
        for ch in CHANNELS:
            if ch in fill:
                resolution[ch] = {"column": ch, "file_fill": fill[ch], "variant": "base"}
                usecols.append(ch)
            elif f"GS_{ch}" in fill:
                resolution[ch] = {"column": f"GS_{ch}", "file_fill": fill[f"GS_{ch}"], "variant": "GS_"}
                usecols.append(f"GS_{ch}")
            else:
                resolution[ch] = {"column": None, "file_fill": None, "variant": None}
        # baseline md pakai DMEA (resolusi sama)
        ch_resolution[fold] = resolution

        csv_path = os.path.join(PARSED, f"{fold}.csv")
        df = pd.read_csv(csv_path, usecols=usecols)
        ts = pd.to_datetime(df["timestamp"], format="ISO8601", utc=True)
        if ts.isna().any():
            raise RuntimeError(f"{fold}: timestamp NaT")
        if not ts.is_monotonic_increasing:
            log(f"{fold}: timestamp TIDAK monotonic -> sort")
            order = np.argsort(ts.to_numpy(), kind="stable")
            ts = ts.iloc[order]
            df = df.iloc[order]
        ts_ns = ts.dt.tz_convert("UTC").dt.tz_localize(None).to_numpy().astype(np.int64)
        log(f"{fold}: {len(df)} baris, {len(usecols)-1} kolom dibaca, {time.time()-t0:.1f}s")

        cols = {}
        for ch in CHANNELS:
            c = resolution[ch]["column"]
            cols[ch] = df[c].to_numpy(dtype=np.float64) if c else None
        md_col = resolution["DMEA"]["column"]
        md_vals = df[md_col].to_numpy(dtype=np.float64) if md_col else None

        for _, r in g.iterrows():
            i = int(r["row"])
            t_end = r["act_start_utc"].value            # int64 ns, STRICT upper bound
            for wi, (wname, wsec) in enumerate(WINDOWS):
                w_start = t_end - wsec * 1_000_000_000
                i0 = int(np.searchsorted(ts_ns, w_start, side="left"))
                i1 = int(np.searchsorted(ts_ns, t_end, side="left"))  # ts[i1] >= t_end
                # ---- anti-leakage check (otomatis) ----
                seg = ts_ns[i0:i1]
                rows_scanned += seg.size
                if seg.size and (seg >= t_end).any():
                    violations += int((seg >= t_end).sum())
                n_rows = seg.size
                if n_rows == 0:
                    zero_row_windows += 1
                full = bool(w_start >= ts_ns[0])
                if not full:
                    partial_windows += 1
                # gap antar-sampel (dicatat, tidak diinterpolasi)
                if n_rows >= 2:
                    dt = np.diff(seg) / 1e9
                    gap_med, gap_max = float(np.median(dt)), float(np.max(dt))
                else:
                    gap_med, gap_max = (np.nan, np.nan)
                base_i = wi * len(CHANNELS) * len(STATS)
                t_sec = (seg - w_start) / 1e9 if n_rows else np.array([])
                for ci, ch in enumerate(CHANNELS):
                    v = cols[ch]
                    x = v[i0:i1] if v is not None else np.array([])
                    st = channel_stats(x, t_sec)
                    for si, s in enumerate(STATS):
                        X[i, base_i + ci * len(STATS) + si] = st.get(s, np.nan)
                    if wname == "w6h":
                        fill_agg.setdefault(fold, {}).setdefault(ch, []).append(st.get("missing_rate", np.nan))
                mbase = wi * 4
                XM[i, mbase + 0] = n_rows
                XM[i, mbase + 1] = gap_med
                XM[i, mbase + 2] = gap_max
                XM[i, mbase + 3] = 1.0 if full else 0.0
            # ---- baseline: kedalaman (DMEA) + waktu jam/dow event ----
            if md_vals is not None:
                wname, wsec = WINDOWS[1]  # baseline ikut jendela utama (2h)
                w_start = t_end - wsec * 1_000_000_000
                i0 = int(np.searchsorted(ts_ns, w_start, side="left"))
                i1 = int(np.searchsorted(ts_ns, t_end, side="left"))
                x = md_vals[i0:i1]
                t_sec = (ts_ns[i0:i1] - w_start) / 1e9
                v = np.isfinite(x)
                if int(v.sum()) >= MIN_VALID:
                    xv, tv = x[v], t_sec[v]
                    XB[i, 0] = xv.mean()
                    XB[i, 1] = xv.std(ddof=1)
                    XB[i, 2] = xv.min()
                    XB[i, 3] = xv.max()
                    XB[i, 4] = ols_slope(xv, tv / 60.0)
                    XB[i, 5] = xv[-1]
                    XB[i, 6] = xv[-1] - xv[0]
            dt_ev = r["act_start_utc"].to_pydatetime()
            h = dt_ev.hour + dt_ev.minute / 60.0
            dow = dt_ev.weekday() + (dt_ev.hour / 24.0)
            XB[i, 7] = np.sin(2 * np.pi * h / 24.0)
            XB[i, 8] = np.cos(2 * np.pi * h / 24.0)
            XB[i, 9] = np.sin(2 * np.pi * dow / 7.0)
            XB[i, 10] = np.cos(2 * np.pi * dow / 7.0)

        log(f"{fold}: {len(g)} event diproses ({time.time()-t0:.1f}s)")

    # ---------- 3. simpan ----------
    os.makedirs(os.path.dirname(OUT_NPZ), exist_ok=True)
    np.savez_compressed(
        OUT_NPZ,
        X=X, feature_names=np.array(feat_names, dtype=object),
        X_baseline=XB, baseline_names=np.array(baseline_names, dtype=object),
        X_window_meta=XM, window_meta_names=np.array(winmeta_names, dtype=object),
        event_id=lab["event_id"].to_numpy(dtype=np.int64),
        fold=lab["fold"].to_numpy(dtype=object),
        wellbore=lab["wellbore"].to_numpy(dtype=object),
        act_start_utc=lab["act_start_utc"].astype(str).to_numpy(dtype=object),
        category=lab["category"].to_numpy(dtype=object),
        outcome=lab["outcome"].fillna("").to_numpy(dtype=object),
        channels=np.array(CHANNELS, dtype=object),
        windows=np.array([f"{w}:{s}" for w, s in WINDOWS], dtype=object),
        primary_window=np.array(PRIMARY, dtype=object),
    )
    log(f"npz ditulis: {OUT_NPZ} ({os.path.getsize(OUT_NPZ)/1e6:.1f} MB)")

    # audit per event
    ev = lab.copy()
    for wi, (wname, _) in enumerate(WINDOWS):
        ev[f"{wname}_n_rows"] = XM[:, wi * 4 + 0]
        ev[f"{wname}_gap_median_s"] = XM[:, wi * 4 + 1]
        ev[f"{wname}_gap_max_s"] = XM[:, wi * 4 + 2]
        ev[f"{wname}_full_window"] = XM[:, wi * 4 + 3]
    ev[["event_id", "fold", "wellbore", "act_start", "act_start_utc",
        *[f"{w}_{s}" for w, _ in WINDOWS for s in ["n_rows", "gap_median_s", "gap_max_s", "full_window"]]]].to_csv(
        OUT_EVENTS, index=False)
    log(f"events csv ditulis: {OUT_EVENTS}")

    # meta json
    fill_summary = {}
    for fold, chans in fill_agg.items():
        fill_summary[fold] = {}
        for ch, vals in chans.items():
            arr = np.asarray(vals, dtype=float)
            fill_summary[fold][ch] = {
                "mean_missing_rate_w6h": None if np.isnan(arr).mean() == 1 else float(np.nanmean(arr)),
                "n_nan_windows": int(np.isnan(arr).sum()),
            }
    meta = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "task": "T10 fitur time-series WITSML (window pra-event) anti-leakage",
        "sources": {
            "labels": LABELS,
            "witsml_csv_dir": PARSED,
            "verify": os.path.join(PARSED, "_verify.json"),
            "folds_used": sorted(FOLD2LABEL.keys()),
            "excluded_variant": "VAR_F-5_alt (keputusan pemakaian varian -> T2-d, lihat V3_WITSML_PARSE_REPORT §5)",
        },
        "label_mapping": FOLD2LABEL,
        "mapping_evidence": "code/51 FOLD2LABEL; USROP_A N -> nama folder WITSML; V2_DATA_JOIN_REPORT (A4 join 99,998%)",
        "coverage": {
            "labels_total": int(n_total),
            "mapped_to_fold": int(n_total - len(unmapped)),
            "unmapped_excluded": {str(k): int(v) for k, v in excl_unmapped.items()},
            "out_of_range_excluded": {str(k): int(v) for k, v in excl_oor.items()},
            "features_built": int(n),
            "zero_row_windows": int(zero_row_windows),
            "partial_windows": int(partial_windows),
        },
        "windows": [{"name": w, "seconds": s, "primary": w == PRIMARY} for w, s in WINDOWS],
        "window_rationale": {
            "w30m": "pendahulu segera (gejala operasional menit-jam sebelum kejadian)",
            "w2h": "jendela utama — ~1 stand/siklus koneksi, sinyal mekanis + hidrolik lengkap",
            "w6h": "konteks shift/operasi lebih luas (trend lambat, persiapan trip)",
        },
        "channels": CHANNELS,
        "channel_resolution_per_fold": ch_resolution,
        "channel_eligibility_rule": "channel dipakai utk 1 fold jika fill file >=50% (_verify.json) pada kolom base ATAU varian GS_; jika tidak -> semua statistik channel itu NaN utk fold itu (tanpa interpolasi)",
        "stats_definitions": {
            "mean/std(min,max)": "statistik basis atas sampel valid di jendela (ddof=1 utk std)",
            "slope_per_min": "slope OLS nilai ~ waktu (per menit)",
            "trend_rho": "Spearman rho antara nilai dan waktu (trend monotonik, -1..1)",
            "delta_mean": "rata-rata selisih bertanda antar sampel valid berurutan",
            "delta_absmean": "rata-rata |selisih| antar sampel valid berurutan",
            "burstiness": "std(diff) / std(level): variasi cepat relatif terhadap variasi total",
            "missing_rate": "fraksi baris jendela dengan nilai NaN (1 - valid/n_rows); NaN jika n_rows=0",
            "min_valid_samples": MIN_VALID,
        },
        "anti_leakage": {
            "rule": "semua sampel fitur: timestamp < act_start (window [t-W, t) ketat)",
            "rows_scanned": int(rows_scanned),
            "violations": int(violations),
            "required": 0,
            "pass": int(violations) == 0,
        },
        "gap_handling": "gap antar-sampel dicatat per event (gap_median_s, gap_max_s, n_rows); TANPA interpolasi",
        "baseline": {
            "names": baseline_names,
            "window": "w2h (jendela utama)",
            "md_features": "statistik DMEA (hole depth MD) — posisi saja, tanpa sensor",
            "time_features": "hour-of-day + day-of-week (sin/cos) dari act_start UTC — konteks waktu yang diketahui saat scoring (bukan info pasca-event)",
        },
        "window_meta": {
            "names": winmeta_names,
            "definitions": {"n_rows": "jumlah baris CSV dalam jendela",
                            "gap_median_s": "median gap antar sampel (detik)",
                            "gap_max_s": "gap maksimum antar sampel (detik)",
                            "full_window": "1 jika awal jendela >= awal data fold (window penuh), 0 jika terpotong"},
        },
        "shape": {"X": list(X.shape), "X_baseline": list(XB.shape), "X_window_meta": list(XM.shape),
                  "n_features": n_feat},
        "feature_name_pattern": "<window>__<channel>__<stat> (urutan npz feature_names)",
        "feature_names": feat_names,
        "fill_rate_summary": fill_summary,
        "runtime_seconds": round(time.time() - t_start, 1),
        "known_limitations": [
            "Label F-15 B/C/D (213 event) tanpa CSV WITSML -> tidak ada fitur time-series (folder F-15A/F-15B/NO-F-15 TIDAK diparse T9, di luar cakupan T10).",
            "Aktivasi channel per fold mengikuti fill file-level >=50% (T9); fill dalam jendela bisa lebih rendah (missing_rate per baris).",
            "Timezone: act_start sudah dikonversi ke UTC dari offset label (+01/+02); jam operasi lokal CET tidak disilang (catatan T9 §5).",
            "VAR_F-5_alt sengaja tidak digabung (keputusan -> T2-d).",
        ],
    }
    with open(OUT_META, "w") as f:
        json.dump(meta, f, indent=1, ensure_ascii=False)
    log(f"meta ditulis: {OUT_META}")

    # ---------- 4. verifikasi ulang (reload) ----------
    z = np.load(OUT_NPZ, allow_pickle=True)
    assert z["X"].shape == (n, n_feat), z["X"].shape
    assert z["X_baseline"].shape == (n, len(baseline_names))
    assert z["X_window_meta"].shape == (n, len(winmeta_names))
    assert int(meta["anti_leakage"]["violations"]) == 0, "LEAKAGE!"
    m2 = json.load(open(OUT_META))
    assert m2["anti_leakage"]["pass"] is True
    n_nan_primary = float(np.isnan(z["X"][:, :len(CHANNELS) * len(STATS)]).mean())
    log(f"VERIFIED: X={z['X'].shape}, violations=0, rows_scanned={rows_scanned}, "
        f"NaN frac (w30m block)={n_nan_primary:.3f}, runtime={meta['runtime_seconds']}s")
    print("DONE", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
