#!/usr/bin/env python3
"""Export per-head detail data for the dashboard head pages.

Reads  : scratch/v9_i1/v9_i1_RESULTS.json  (numbers already published)
         scratch/v9_d1/datasets/*.csv.gz   (per-window features + labels)
         data/USROP_labeled.csv, scratch/v6_e1/toolwear_windows.csv
         code/v9_e1_RULE_*.py via code/v9_i1_pipeline.py (same engine code)
Writes : dashboard/data/head_pages.json

Every per-window series is RECOMPUTED with the engine's own functions and then
cross-checked against the published n_aktif and metrik_segmen. A head whose
recomputation does not match exactly is exported with series_ok=false and no
series, so the page can say "series not exported" instead of drawing a picture
that disagrees with the table.

Monte Carlo blocks are simulations drawn from the measured confusion counts
(Beta posterior for precision / recall, Poisson for alarms per 8 h shift).
They are labelled as simulations in the JSON; they are not field data.
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

RES_PATH = BASE / "scratch" / "v9_i1" / "v9_i1_RESULTS.json"
OUT = BASE / "dashboard" / "data" / "head_pages.json"

SEED = 20261029
N_DRAW = 20000
N_BINS = 120
N_CUM = 40

RES = json.loads(RES_PATH.read_text())
WELL = RES["meta"]["segmen_rig"]

r01, r02 = P.rule_modules()


# ---------------------------------------------------------------- datasets
def dataset(key: str) -> pd.DataFrame:
    return pd.read_csv(f"{P.DS}/{key}.csv.gz")


def segment(key: str) -> pd.DataFrame:
    df = dataset(key)
    return (df[df["well"] == WELL].sort_values("ts_bin").reset_index(drop=True))


def usrop_segment() -> pd.DataFrame:
    usrop = pd.read_csv(P.USROP)
    seg = usrop[usrop["well"].str.contains(WELL.replace("-", ""), regex=False)
                | (usrop["well"] == f"USROP_A 2 N-SH_{WELL}d.csv")]
    if len(seg) == 0:
        seg = usrop[usrop["well"].str.contains("_F-14", regex=False)]
    return seg


# ---------------------------------------------------------------- series
def status_series(cls_key, df, ycol, prevcol):
    y = df[ycol].to_numpy().astype(int)
    rp, _ = r01.rule_display(cls_key, df)
    rp = np.asarray(rp).astype(int)
    pers = df[prevcol].to_numpy().astype(int)
    hyb = ((rp == 1) & (pers == 1)).astype(int)
    return y, {
        "rule_display": rp,
        "persistence": pers,
        "hybrid_rule_and_persistence": hyb,
    }


def stuck_series(df_k1, df_k2):
    y1, s1 = status_series("stuck_k1", df_k1, "y_stuck", "y_prev_stuck")
    y2 = df_k2["y_stuck_onset"].to_numpy().astype(int)
    e1, _ = r01.rule_e1(df_k2)
    pev = np.asarray(r02.event_persistence(df_k2)).astype(int)
    s1["e1_2of3"] = None  # different window grid, filled by caller
    return (y1, s1), (y2, {"e1_2of3": np.asarray(e1).astype(int),
                           "persistence_event": pev})


def bitwear_series(df):
    df = df.sort_values("Measured Depth m").reset_index(drop=True)
    is_mse = (df["label"] == "high_MSE_bit_wear").to_numpy().astype(int)
    pers = np.concatenate([[0], is_mse[:-1]])
    return is_mse, {"persistence": pers}


def toolwear_series(tw: pd.DataFrame) -> tuple[np.ndarray, dict]:
    """Exact replay of P.run_tool_wear alarm construction (no shortcuts)."""
    feats = [c for c in tw.columns
             if c.endswith(("_mean", "_std", "_rms", "_kurt", "_skew", "_p2p",
                            "_crest", "_zcr", "_fdom"))]
    if len(feats) != 27:
        raise SystemExit(f"tool wear feature count {len(feats)} != 27")
    n = len(tw)
    y = tw["y"].to_numpy().astype(int)
    alarm_b = np.zeros(n, dtype=int)
    alarm_op = np.zeros(n, dtype=int)
    rms_rank = np.zeros(n, dtype=float)
    for _tool, g in tw.groupby("tool"):
        r01r = g[g["run"] == "R01"].sort_values("start_sample")
        r02r = g[g["run"] == "R02"].sort_values("start_sample")
        ncal = max(5, int(np.ceil(0.30 * len(r01r))))
        cal, ev1 = r01r.iloc[:ncal], r01r.iloc[ncal:]
        med = cal[feats].median()
        mad = (cal[feats] - med).abs().median() * 1.4826
        mad = mad.replace(0, np.nan)

        def sc(ev):
            z = ((ev[feats] - med) / mad).abs()
            return (z > 3.0).sum(axis=1).to_numpy()

        s1, s2 = sc(ev1), sc(r02r)
        alarm_b[ev1.index.to_numpy()] = (s1 >= 5).astype(int)
        alarm_b[r02r.index.to_numpy()] = (s2 >= 5).astype(int)
        q = 1.0 - 1.0 * (len(ev1) / 60.0) / max(len(ev1), 1)
        q = min(max(q, 0.5), 1.0)
        thr = float(np.quantile(s1, q)) if len(s1) else None
        if thr is not None:
            alarm_op[ev1.index.to_numpy()] = (s1 >= thr).astype(int)
            alarm_op[r02r.index.to_numpy()] = (s2 >= thr).astype(int)
        rms3 = [c for c in feats if c.endswith("_rms")]
        zrms = ((g[rms3] - med[rms3]) / mad[rms3]).abs().mean(axis=1)
        rms_rank[g.index.to_numpy()] = zrms.to_numpy()
    return y, {"calib_5of27": alarm_b, "op_far_calibrated": alarm_op,
               "canary_3rms": (rms_rank >= 3.0).astype(int)}


# ---------------------------------------------------------------- helpers
def bins(arr: np.ndarray, lab: np.ndarray | None, n_bins: int = N_BINS) -> list:
    k = max(1, int(np.ceil(len(arr) / n_bins)))
    out = []
    for start in range(0, len(arr), k):
        chunk = arr[start:start + k]
        row = {"i": start // k, "n": int(len(chunk)), "a": int(chunk.sum())}
        if lab is not None:
            row["y"] = int(np.asarray(lab)[start:start + k].sum())
        out.append(row)
    return out


def cumulative(pred: np.ndarray, y: np.ndarray, steps: int = N_CUM) -> list:
    idx = np.unique(np.linspace(1, len(y), steps).astype(int))
    tp = np.cumsum((pred == 1) & (y == 1))
    fp = np.cumsum((pred == 1) & (y == 0))
    tot_pos = max(int((y == 1).sum()), 1)
    tot_neg = max(int((y == 0).sum()), 1)
    return [{"at": int(i), "frac": round(i / len(y), 4),
             "recall": round(float(tp[i - 1] / tot_pos), 4),
             "far_share": round(float(fp[i - 1] / tot_neg), 5)} for i in idx]


def hist(values: np.ndarray, edges: np.ndarray) -> list:
    counts, _ = np.histogram(values, bins=edges)
    total = max(int(counts.sum()), 1)
    return [{"lo": round(float(edges[i]), 4), "hi": round(float(edges[i + 1]), 4),
             "share": round(float(counts[i] / total), 4)} for i in range(len(counts))]


def monte_carlo(met: dict, rng) -> dict:
    tp, fp, fn = int(met["tp"]), int(met["fp"]), int(met["fn"])
    far = met.get("far")
    out = {"n_draw": N_DRAW, "seed": SEED,
           "basis": "Beta(tp+1, fp+1) and Beta(tp+1, fn+1); Poisson(FAR/3) for one 8 hour shift"}
    if tp + fp > 0:
        p = rng.beta(tp + 1, fp + 1, N_DRAW)
        out["precision"] = {"p05": round(float(np.percentile(p, 5)), 4),
                            "p50": round(float(np.percentile(p, 50)), 4),
                            "p95": round(float(np.percentile(p, 95)), 4),
                            "hist": hist(p, np.linspace(0, 1, 21))}
    if tp + fn > 0:
        r = rng.beta(tp + 1, fn + 1, N_DRAW)
        out["recall"] = {"p05": round(float(np.percentile(r, 5)), 4),
                         "p50": round(float(np.percentile(r, 50)), 4),
                         "p95": round(float(np.percentile(r, 95)), 4),
                         "hist": hist(r, np.linspace(0, 1, 21))}
    if far is not None:
        per_minute = str(met.get("far_unit", "")).find("menit") >= 0
        lam = float(far) * 8.0 * 60.0 if per_minute else float(far) / 3.0
        d = rng.poisson(lam, N_DRAW)
        hi = int(max(np.percentile(d, 99), 1))
        nb = int(min(30, max(hi + 1, 5)))
        edges = np.linspace(-0.5, hi + 0.5, nb + 1)
        out["alarms_per_shift"] = {"lambda": round(lam, 3),
                                   "p05": round(float(np.percentile(d, 5)), 2),
                                   "p50": round(float(np.percentile(d, 50)), 2),
                                   "p95": round(float(np.percentile(d, 95)), 2),
                                   "hist": hist(d, edges),
                                   "unit": "alarms per 8 h of event free operation",
                                   "per_minute_source": per_minute}
    return out


# ---------------------------------------------------------------- main
def main() -> int:
    rng = np.random.default_rng(SEED)
    t0 = time.time()

    seg = {k: segment(k) for k in ["vib", "ssi", "shk", "stuck_k1", "stuck_k2", "hyd_ki"]}
    usrop = usrop_segment()
    tw = pd.read_csv(P.TOOLWEAR)

    # per-window predictions, recomputed with the engine's own code
    preds: dict[str, tuple[np.ndarray, np.ndarray]] = {}
    for eng, key in [("vib", "vib"), ("ssi", "ssi"), ("shk", "shk"), ("hyd", "hyd_ki")]:
        y, s = status_series(key, seg[key], f"y_{'hyd' if eng == 'hyd' else eng}",
                             f"y_prev_{'hyd' if eng == 'hyd' else eng}")
        for head, arr in s.items():
            preds[f"{eng}/{head}"] = (arr, y)
    (y1, s1), (y2, s2) = stuck_series(seg["stuck_k1"], seg["stuck_k2"])
    for head, arr in s1.items():
        if arr is not None:
            preds[f"stuck/{head}"] = (arr, y1)
    for head, arr in s2.items():
        preds[f"stuck/{head}"] = (arr, y2)
    by, bp = bitwear_series(usrop)
    for head, arr in bp.items():
        preds[f"bit_wear/{head}"] = (arr, by)
    ty, tp = toolwear_series(tw)
    for head, arr in tp.items():
        preds[f"tool_wear/{head}"] = (arr, ty)

    heads_out: dict[str, dict] = {}
    checks = []
    for eng in RES["engines"]:
        ekey = eng["engine"]
        for h in eng["heads"]:
            key = f"{ekey}/{h['head']}"
            met = h.get("metrik_segmen")
            rec = {
                "engine": ekey,
                "head": h["head"],
                "layer": h["layer"],
                "tier": h["tier"],
                "klaim": h.get("klaim"),
                "human_review": h.get("human_review_required"),
                "definisi": h.get("definisi"),
                "definisi_kode": P.registry_head(ekey, h["head"]).get("definisi"),
                "badge_far": h.get("badge_far"),
                "keyakinan": h.get("keyakinan"),
                "batas": h.get("batas_pemakaian"),
                "n_windows": h.get("n_windows"),
                "n_aktif": h.get("n_aktif"),
                "frac_aktif": h.get("frac_aktif"),
                "status": h.get("status"),
                "alasan": h.get("alasan"),
                "metrics": None,
                "series_ok": False,
                "series_note": None,
            }
            if met:
                # the published block names the rate far_segmen; keep one name
                met = dict(met)
                met["far"] = met.get("far_segmen")
                rec["metrics"] = met
                rec["montecarlo"] = monte_carlo(met, rng)
            if key in preds:
                arr, y = preds[key]
                arr = np.asarray(arr).astype(int)
                y = np.asarray(y).astype(int)
                ok_count = (rec["n_aktif"] is None) or int(arr.sum()) == int(rec["n_aktif"])
                ok_metric = True
                if met:
                    recomputed = P.seg_metrics(y, arr, win_s=1 if ekey == "tool_wear" else 60)
                    ok_metric = all(recomputed.get(k) == met.get(k)
                                    for k in ("n", "pos", "neg", "tp", "fp", "fn",
                                              "precision", "recall", "far_segmen"))
                    if not ok_metric:
                        checks.append({"key": key, "metric_mismatch": {
                            k: [recomputed.get(k), met.get(k)] for k in met if recomputed.get(k) != met.get(k)}})
                if ok_count and ok_metric:
                    rec["series_ok"] = True
                    rec["series"] = {
                        "unit": "window index inside this segment",
                        "n": int(len(arr)),
                        "active_total": int(arr.sum()),
                        "bins": bins(arr, y),
                        "cumulative": cumulative(arr, y),
                    }
                else:
                    rec["series_note"] = ("recomputed series does not match the published "
                                          "count or metric, so it is not drawn")
            else:
                rec["series_note"] = ("per-window predictions for this head are produced by "
                                      "the Random Forest training step, which is not re-run by "
                                      "this export")
            heads_out[key] = rec

    payload = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "source_results": str(RES_PATH.relative_to(BASE)),
        "segment": WELL,
        "model": RES["meta"],
        "heads": heads_out,
        "series_checked": len(preds),
        "series_ok": sum(1 for r in heads_out.values() if r["series_ok"]),
        "mismatches": checks,
    }
    OUT.write_text(json.dumps(payload, indent=1, ensure_ascii=False))
    print(f"written {OUT} ({OUT.stat().st_size} bytes) in {time.time() - t0:.1f}s")
    print(f"heads={len(heads_out)} series_ok={payload['series_ok']} mismatches={len(checks)}")
    for c in checks[:5]:
        print("MISMATCH", c)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
