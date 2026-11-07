#!/usr/bin/env python3
"""V9-D1 04 — dataset `stuck_k2` (prediksi onset stuck pipe, H=10 menit).

Resep label = V8-E_stuck (extract_folds2.py + eval_stage.py) — DIADOPSI PENUH:
- grid 60 detik ALL-rows (resample mean; bukan drilling-only — mask = ops =
  TQA/HKLD/SWOB/RPM tidak-NaN per menit; saat stuck RPM/SWOB sering 0)
- STUCK_RT ffill (PRIMER, dikunci pra-reg) -> resample max per menit
- onset = edge 0->1 (NaN dilewati / strict=False)
- inblock = menit dengan STUCK_ffill>=1 (jendela onset ikut inblock -> Dibuang)
- positif = [t_e-10, t_e) dgn aturan skorable V8: horizon len==10, same segment,
  tidak seluruhnya inblock; negatif = baris ops & ~inb lainnya
DEVIASI YANG DIPUTUSKAN D1 (kontrak S1, terdokumentasi):
- fitur = CHAN11 x mean/std/slope/last/frac (PM §2.4 'E3 55 fitur') dgn jendela
  KETAT-LALU [t0-10, t0) — bukan rolling t-9..t ala V8 — agar stempel anti-bocor
  (feat_ts_max < lab_ts) berlaku utk baris negatif (lab_ts=t0) maupun positif (t_e).
- eligibility: ops(t0) & ~inb(t0) & >=1 menit data dalam jendela fitur.
Wells: F-9, F-9_A, F-10, F-14 (satu-satunya parsed CSV dgn STUCK_RT).
MODE: `python3 v9_d1_04_stuck_k2.py <WELL>` = proses 1 well (RAM per-subprocess);
tanpa argumen = menjalankan 4 well berurutan via subprocess lalu merge.
Invarian validasi: onsets_ffill wajib = V8 (F-9_A 72, F-14 61, F-10 93).
Output: scratch/v9_d1/datasets/stuck_k2.csv.gz + v9_d1_04_qc.json + log.
"""
import gc
import json
import os
import subprocess
import sys
import time
import numpy as np
import pandas as pd

SEED = 42
np.random.seed(SEED)

BASE = "/mnt/d/Capstone 1/data/volve/witsml_parsed"
OUT = "/mnt/d/Capstone 1/scratch/v9_e_rule/repair"
QC_DIR = "/mnt/d/Capstone 1/scratch/v9_e_rule/repair"
os.makedirs(OUT, exist_ok=True)
WELLS = ["F-9", "F-9_A", "F-10", "F-14"]
REF_ONSETS = {"F-9_A": 72, "F-14": 61, "F-10": 93}
H = 10
GAP_SEG_MIN = 30
STATS = ["mean", "std", "slope", "last", "frac"]
CHAN = ["TQA", "SPPA", "TFLO", "RPM", "SWOB", "HKLD", "ROP", "BPOS", "SPM",
        "depth", "dbtm"]
FEAT55 = [f"{c}_{s}" for c in CHAN for s in STATS]
SURF = ["TQA", "SPPA", "TFLO", "RPM", "SWOB", "HKLD", "ROP", "BPOS"]
SPMC = ["SPM1", "SPM2", "SPM3"]

t_start = time.time()
log_lines = []


def log(msg):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line, flush=True)
    log_lines.append(line)


def onsets_ffill(s):
    """Edge 0->1; NaN dilewati (prev bertahan) — resep eval_stage."""
    out, prev = [], None
    for t, v in s.items():
        if np.isnan(v):
            continue
        if prev is not None and prev < 1 and v >= 1:
            out.append(t)
        prev = v
    return out


def features_strict_past(g, chan_cols, seg, store):
    """Fitur [t0-10, t0) per menit, segment-aware; HANYA baris `store` disimpan.

    Statistik = definisi jendela rig S1: mean, std (ddof=1), slope OLS per menit
    (cnt>=3 & den>1e-9 selain itu NaN), last = nilai t0-1, frac = hitung non-null/10.
    """
    n_all = len(g)
    colnames = [f"{c}_{s}" for c in chan_cols for s in STATS]
    store_pos = np.flatnonzero(store)
    slot_of = np.full(n_all, -1, np.int64)
    slot_of[store_pos] = np.arange(len(store_pos), dtype=np.int64)
    out = np.full((len(store_pos), len(chan_cols) * 5), np.nan, np.float64)
    seg_v = seg.to_numpy()
    for _, idx in pd.Series(seg_v).groupby(seg_v, sort=True).groups.items():
        idx = np.asarray(idx)
        if len(idx) == 0:
            continue
        p = pd.Series(np.arange(len(idx), dtype=np.float64))
        pv = p.to_numpy()
        for j, c in enumerate(chan_cols):
            y = g[c].to_numpy(dtype=np.float64)[idx]
            ys = pd.Series(y)
            m = ys.notna().astype(np.float64)
            ym = ys.fillna(0.0)
            n = m.shift(1).rolling(10, min_periods=1).sum().to_numpy()
            Sp = (p * m).shift(1).rolling(10, min_periods=1).sum().to_numpy()
            Spp = (p * p * m).shift(1).rolling(10, min_periods=1).sum().to_numpy()
            Sy = ym.shift(1).rolling(10, min_periods=1).sum().to_numpy()
            Spy = (p * ym).shift(1).rolling(10, min_periods=1).sum().to_numpy()
            mean = ys.shift(1).rolling(10, min_periods=1).mean().to_numpy()
            std = ys.shift(1).rolling(10, min_periods=1).std().to_numpy()
            last = ys.shift(1).to_numpy()
            with np.errstate(invalid="ignore", divide="ignore"):
                Sx = Sp - pv * n
                Sxx = Spp - 2 * pv * Sp + pv * pv * n
                Sxy = Spy - pv * Sy
                den = n * Sxx - Sx * Sx
                slope = np.where((n >= 3) & (den > 1e-9),
                                 (n * Sxy - Sx * Sy) /
                                 np.where(den > 1e-9, den, 1.0), np.nan)
            frac = n / 10.0
            base = j * 5
            slots = slot_of[idx]
            keep = slots >= 0
            if keep.any():
                ks = slots[keep]
                for b, arr in enumerate((mean, std, slope, last, frac)):
                    out[ks, base + b] = arr[keep]
    return pd.DataFrame(out, index=store_pos, columns=colnames)


def process_well(well):
    p = os.path.join(BASE, f"{well}.csv")
    hdr = pd.read_csv(p, nrows=0).columns.tolist()
    use = set(SURF + SPMC + ["STUCK_RT", "DMEA", "DBTM", "timestamp"]) & set(hdr)
    # Chunked read (chunksize=250rb = resep v9_d1_01): read_csv single-shot pada F-14
    # (813MB) gagal OSError Errno 12 (ENOMEM di parser C) — chunked terbukti jalan.
    dtypes = {c: np.float32 for c in sorted(use) if c != "timestamp"}
    parts = []
    for ch in pd.read_csv(p, usecols=sorted(use), chunksize=250_000,
                          low_memory=False, dtype=dtypes):
        parts.append(ch)
    df = pd.concat(parts, ignore_index=True)
    del parts
    gc.collect()
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="ISO8601",
                                     utc=True, errors="coerce")
    df = df[df["timestamp"].notna()].sort_values("timestamp")
    df = df.drop_duplicates("timestamp", keep="last").set_index("timestamp")
    for c in df.columns:
        if df[c].dtype == object:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    num = df
    wq = {
        "stuck_nonnull_raw": int(num["STUCK_RT"].notna().sum()) if "STUCK_RT" in num else None,
        "stuck_valcounts_raw": ({str(k): int(v) for k, v in
                                 num["STUCK_RT"].value_counts().items()}
                                if "STUCK_RT" in num else None),
    }

    # grid 60s: index dari resample (bin tepat :00) — PENTING, jangan date_range
    base_idx = num.iloc[:, 0].resample("60s").mean().index
    g = pd.DataFrame(index=base_idx)
    for c in SURF:
        if c in num:
            g[c] = num[c].resample("60s").mean().to_numpy()
    spm_cols = [c for c in SPMC if c in num]
    if spm_cols:
        g["SPM"] = num[spm_cols].sum(axis=1, min_count=1).resample("60s").mean().to_numpy()
    g["depth"] = num["DMEA"].resample("60s").mean().to_numpy() if "DMEA" in num else np.nan
    g["dbtm"] = num["DBTM"].resample("60s").mean().to_numpy() if "DBTM" in num else np.nan
    if "STUCK_RT" in num:
        g["STUCK_raw"] = num["STUCK_RT"].resample("60s").max().reindex(base_idx).to_numpy()
        ff = num["STUCK_RT"].ffill(limit=None)
        g["STUCK_ffill"] = ff.resample("60s").max().reindex(base_idx).to_numpy()
    else:
        g["STUCK_raw"] = np.nan
        g["STUCK_ffill"] = np.nan
    del num, df
    gc.collect()

    dt = g.index.to_series().diff()
    seg = (dt.isna() | (dt > pd.Timedelta(minutes=GAP_SEG_MIN))).cumsum()
    stuckf = (g["STUCK_ffill"] >= 1).fillna(False)
    ops = g[[c for c in ["TQA", "HKLD", "SWOB", "RPM"] if c in g]].notna().any(axis=1)
    on_f = onsets_ffill(g["STUCK_ffill"])
    on_s = onsets_ffill(g["STUCK_raw"])

    y = pd.Series(0, index=g.index, dtype=np.int8)
    reasons = {"no_prior_windows": 0, "all_horizon_inblock_or_gap": 0}
    scorable = []
    for t_e in on_f:
        if t_e not in g.index:
            k = g.index.get_indexer([t_e], method="nearest")[0]
            t_e = g.index[k]
        hor = g.index[(g.index >= t_e - pd.Timedelta(minutes=H)) & (g.index < t_e)]
        if len(hor) < H or not (seg.loc[hor] == seg.loc[t_e]).all():
            reasons["no_prior_windows"] += 1
            continue
        elig = hor[~stuckf.loc[hor].to_numpy()]
        if len(elig) == 0:
            reasons["all_horizon_inblock_or_gap"] += 1
            continue
        y.loc[elig] = 1
        scorable.append(t_e)
    scorable = pd.DatetimeIndex(scorable)

    chan_cols = [c for c in CHAN if c in g.columns]
    any_present = g[chan_cols].notna().any(axis=1)
    win_present = (any_present.shift(1).rolling(10, min_periods=1).sum()
                   .fillna(0).to_numpy() > 0)
    mask = ops.to_numpy() & (~stuckf.to_numpy()) & win_present

    F = features_strict_past(g, chan_cols, seg, mask)
    gc.collect()

    ts_series = pd.Series(g.index, index=g.index)
    last_present = ts_series.where(any_present).ffill().shift(1)
    feat_ts_max_all = (last_present.astype("int64") // 10**9 // 60).astype(np.float64)
    feat_ts_max_all = feat_ts_max_all.where(last_present.notna(), np.nan)

    y_prev = y.shift(1)
    lab_ts_all = pd.Series((g.index.astype("int64") // 10**9 // 60).astype(np.float64),
                           index=g.index)
    lab_kind_all = np.where(mask, "onset_horizon_neg", "")
    lab_ts_out = lab_ts_all.copy()
    for t_e in scorable:
        minute = t_e.value // 10**9 // 60
        sel = (mask & (y.to_numpy() == 1) &
               (lab_ts_all >= minute - H) & (lab_ts_all < minute))
        lab_ts_out[sel] = float(minute)
        lab_kind_all[sel] = "onset_event"

    sub = F.copy()
    sub.insert(0, "well", well)
    sub.insert(1, "ts_bin",
                lab_ts_all[mask].to_numpy().astype(np.int64))
    sub.insert(2, "feat_ts_max", feat_ts_max_all.to_numpy()[mask])
    sub.insert(3, "lab_ts", lab_ts_out[mask].to_numpy())
    sub.insert(4, "lab_kind", lab_kind_all[mask])
    sub["y_stuck_onset"] = y.to_numpy()[mask]
    sub["y_prev_stuck_onset"] = y_prev.to_numpy()[mask]
    sub = sub.reset_index(drop=True)

    wq.update({
        "grid_minutes": int(len(g)),
        "ops_rows": int(ops.sum()),
        "inblock_rows": int(stuckf.sum()),
        "onsets_ffill": len(on_f),
        "onsets_strict": len(on_s),
        "onsets_scorable": len(scorable),
        "onset_skipped": reasons,
        "eligible_rows": int(mask.sum()),
        "positives": int(y.to_numpy()[mask].sum()),
        "v8_onsets_match": (len(on_f) == REF_ONSETS[well]) if well in REF_ONSETS else None,
    })
    out_ds = os.path.join(OUT, f"_stuck_k2_{well}.csv.gz")
    sub.to_csv(out_ds, index=False, compression={"method": "gzip", "mtime": 0})
    json.dump(wq, open(os.path.join(QC_DIR, f"_stuck_k2_{well}.json"), "w"), indent=1)
    log(f"== {well}: grid={wq['grid_minutes']} ops={wq['ops_rows']} "
        f"inb={wq['inblock_rows']} onsets ffill/strict={len(on_f)}/{len(on_s)} "
        f"scorable={len(scorable)} eligible={wq['eligible_rows']} "
        f"pos={wq['positives']} v8_match={wq['v8_onsets_match']}")
    return wq


def main():
    if len(sys.argv) > 1:
        process_well(sys.argv[1])
        return
    # jalankan tiap well di subprocess terpisah (kembalikan RAM penuh);
    # resume: lewati well yang artefaknya sudah ada
    for w in WELLS:
        if (os.path.exists(os.path.join(OUT, f"_stuck_k2_{w}.csv.gz")) and
                os.path.exists(os.path.join(QC_DIR, f"_stuck_k2_{w}.json"))):
            print(f"skip {w} (artefak sudah ada)", flush=True)
            continue
        r = subprocess.run([sys.executable, os.path.abspath(__file__), w],
                           capture_output=True, text=True)
        print(r.stdout, end="")
        log_lines.append(r.stdout.rstrip("\n"))
        if r.returncode != 0:
            print(r.stderr[-3000:])
            raise SystemExit(f"well {w} gagal (rc={r.returncode})")
    # merge
    parts, qc = [], {"seed": SEED, "H_min": H, "gap_seg_min": GAP_SEG_MIN,
                     "recipe": "V8 extract_folds2 label + S1 strict-past features (55)",
                     "reference_onsets_v8": REF_ONSETS, "wells": {}}
    for w in WELLS:
        parts.append(pd.read_csv(os.path.join(OUT, f"_stuck_k2_{w}.csv.gz")))
        qc["wells"][w] = json.load(open(os.path.join(QC_DIR, f"_stuck_k2_{w}.json")))
        os.remove(os.path.join(OUT, f"_stuck_k2_{w}.csv.gz"))
        os.remove(os.path.join(QC_DIR, f"_stuck_k2_{w}.json"))
    df_all = pd.concat(parts, ignore_index=True)
    df_all = df_all.sort_values(["well", "ts_bin"]).reset_index(drop=True)
    path = os.path.join(OUT, "stuck_k2.csv.gz")
    df_all.to_csv(path, index=False, compression={"method": "gzip", "mtime": 0})
    qc["dataset"] = {"file": path, "n_rows": int(len(df_all)),
                     "n_features": len(FEAT55),
                     "positives": int(df_all["y_stuck_onset"].sum()),
                     "per_well": {w: {"n": int((df_all["well"] == w).sum()),
                                      "pos": int(df_all.loc[df_all["well"] == w,
                                                            "y_stuck_onset"].sum())}
                                  for w in WELLS}}
    qc["elapsed_s"] = round(time.time() - t_start, 1)
    json.dump(qc, open(os.path.join(QC_DIR, "v9_d1_04_qc.json"), "w"), indent=1)
    open(os.path.join(QC_DIR, "v9_d1_04_run_log.txt"), "w").write(
        "\n".join(log_lines) + "\n")
    print("merged rows =", qc["dataset"]["n_rows"],
          "pos =", qc["dataset"]["positives"])


if __name__ == "__main__":
    main()
