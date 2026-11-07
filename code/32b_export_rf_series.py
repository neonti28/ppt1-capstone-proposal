#!/usr/bin/env python3
"""Add per-window series for the four Random Forest heads to head_pages.json.

Runs the same LOWO training the engine ran (same seed, same hyper-parameters,
same feature list) and keeps the result only if the recomputed active count and
segment metrics equal the published ones exactly.

Reads/writes : dashboard/data/head_pages.json
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path("/mnt/d/Capstone 1(v2)")
sys.path.insert(0, str(BASE / "code"))
import v9_i1_pipeline as P  # noqa: E402

RES = json.loads((BASE / "scratch" / "v9_i1" / "v9_i1_RESULTS.json").read_text())
OUT = BASE / "dashboard" / "data" / "head_pages.json"
PAGES = json.loads(OUT.read_text())
WELL = RES["meta"]["segmen_rig"]

JOBS = [("vib", "vib", "y_vib", 300), ("ssi", "ssi", "y_ssi", 300),
        ("shk", "shk", "y_shk", 300), ("stuck", "stuck_k2", "y_stuck_onset", 200)]

N_BINS, N_CUM = 120, 40


def bins(arr, y, n_bins=N_BINS):
    k = max(1, int(np.ceil(len(arr) / n_bins)))
    out = []
    for start in range(0, len(arr), k):
        chunk = arr[start:start + k]
        out.append({"i": start // k, "n": int(len(chunk)), "a": int(chunk.sum()),
                    "y": int(np.asarray(y)[start:start + k].sum())})
    return out


def cumulative(pred, y, steps=N_CUM):
    idx = np.unique(np.linspace(1, len(y), steps).astype(int))
    tp = np.cumsum((pred == 1) & (y == 1))
    fp = np.cumsum((pred == 1) & (y == 0))
    tot_pos, tot_neg = max(int((y == 1).sum()), 1), max(int((y == 0).sum()), 1)
    return [{"at": int(i), "frac": round(i / len(y), 4),
             "recall": round(float(tp[i - 1] / tot_pos), 4),
             "far_share": round(float(fp[i - 1] / tot_neg), 5)} for i in idx]


def main() -> int:
    ok = 0
    for engine, key, ycol, n_est in JOBS:
        t0 = time.time()
        df = pd.read_csv(f"{P.DS}/{key}.csv.gz").sort_values(["well", "ts_bin"]).reset_index(drop=True)
        res = P.train_lowo(df, ycol, WELL, n_estimators=n_est)
        pred = (res["score"] >= 0.5).astype(int)
        y = np.asarray(res["y"]).astype(int)
        hkey = f"{engine}/rf_lowo"
        rec = PAGES["heads"].get(hkey)
        if rec is None:
            print("skip, no head record:", hkey)
            continue
        met = rec["metrics"]
        got = P.seg_metrics(y, pred, win_s=60)
        count_ok = (rec["n_aktif"] is None) or int(pred.sum()) == int(rec["n_aktif"])
        metric_ok = all(got.get(k) == met.get(k) for k in
                        ("n", "pos", "neg", "tp", "fp", "fn", "precision", "recall", "far_segmen"))
        print(f"{hkey}: fit {time.time() - t0:.1f}s active {int(pred.sum())} vs {rec['n_aktif']} "
              f"count_ok={count_ok} metric_ok={metric_ok}")
        if count_ok and metric_ok:
            rec["series_ok"] = True
            rec["series_note"] = None
            rec["series"] = {"unit": "window index inside this segment", "n": int(len(pred)),
                             "active_total": int(pred.sum()), "bins": bins(pred, y),
                             "cumulative": cumulative(pred, y),
                             "refit_seconds": round(time.time() - t0, 1)}
            ok += 1
        else:
            rec["series_ok"] = False
            rec["series_note"] = ("refit does not reproduce the published count or metric, "
                                  "so the series is not drawn")
    PAGES["series_ok"] = sum(1 for r in PAGES["heads"].values() if r["series_ok"])
    OUT.write_text(json.dumps(PAGES, indent=1, ensure_ascii=False))
    print(f"rf series added: {ok} | series_ok total {PAGES['series_ok']} | {OUT.stat().st_size} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
