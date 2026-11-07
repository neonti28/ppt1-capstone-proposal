#!/usr/bin/env python3
"""V9-E_STAT 02 — engine stuck-E2 (skor z TQA/HKLD/ROP-drop, ambang q95-TRAIN).

Spesifikasi: docs/V9_PM1_ARCHITECTURE.md §2.4 (E2_stats) + docs/V9_R1_JUSTIFICATION.md §3.4.
- Skor (resep literal V8-E_stuck eval_stuck.rule_and_score):
    med60  = rolling(60, min20).median().shift(1)            [TQA, HKLD, ROP]
    mad60  = |x - med60|.rolling(60, min20).median().shift(1) [TQA, HKLD]
    mean10 = rolling(10, min3).mean()
    z      = (mean10 - med60) / (1.4826*mad60 + 1e-9)
    rop_drop = ((med60_ROP - mean10_ROP) / |med60_ROP|.clip(1e-6)).clip(0)
    score  = z_tqa.fillna(0) + z_hkld.fillna(0) + rop_drop.fillna(0)
  per SEGMEN (gap > 30 mnt = segmen baru) pada grid 60 dtk dari bins/.
- Ambang operasi: q95 skor di TRAIN (pooled train-wells, mask ops & ~in-block) — anti-peeking.
- Split: LOWO 4 fold (scratch/v9_d1/lowo_stuck_k2.json), seed 42.
- BASELINE relevan (R1 §4.1): (a) E0 persistence literal (kolom y_prev_stuck_onset);
  (b) E0 persistence versi konstruksi V8 (alarm hanya di t_e -> recall@H 0 by construction);
  (c) prevalence-random (AUPRC = prev, analitik). Canary-depth = domain E_ML/E_RULE (S9).
- Anti-sirkular: STUCK_RT tidak dipakai apa pun selain mask in-block (bukan fitur skor).
- CI95: moving-block bootstrap blok 60, 1000, seed 42.

Output (S6): scratch/v9_e_stat/v9_e_stat_02_stuck_e2_RESULTS.json + run log.
"""
import json, os, time
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score

SEED = 42
Q95 = 0.95
H = 10            # menit horizon
GAP_SEG_MIN = 30  # menit pemisah segmen
BASE = "/mnt/d/Capstone 1(v2)"
DS = f"{BASE}/scratch/v9_d1/datasets/stuck_k2.csv.gz"
BINS = f"{BASE}/scratch/v9_d1/bins"
LOWO = f"{BASE}/scratch/v9_d1/lowo_stuck_k2.json"
OUT = f"{BASE}/scratch/v9_e_stat"
os.makedirs(OUT, exist_ok=True)
LOGP = f"{OUT}/v9_e_stat_02_run_log.txt"
log_lines = []
WELLS = None


def log(m):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {m}"
    print(line, flush=True)
    log_lines.append(line)


def block_bootstrap_ci(y, score, n_boot=1000, block=60, seed=SEED):
    rng = np.random.default_rng(seed)
    n = len(y)
    if n < 2 * block or y.sum() == 0 or y.sum() == n:
        return None
    nb = int(np.ceil(n / block)); vals = []
    for _ in range(n_boot):
        starts = rng.choice(np.arange(n), size=nb, replace=True)
        idx = ((starts[:, None] + np.arange(block)[None, :]).ravel() % n)[:n]
        yb, sb = y[idx], score[idx]
        if yb.min() == yb.max():
            continue
        vals.append(average_precision_score(yb, sb))
    if not vals:
        return None
    return [round(float(np.percentile(vals, 2.5)), 4),
            round(float(np.percentile(vals, 97.5)), 4)]


def e2_score(g):
    """Skor E2 per menit (resep V8 eval_stuck.rule_and_score) — tanpa melihat label."""
    dt = g.index.to_series().diff()
    seg = (dt.isna() | (dt > pd.Timedelta(minutes=GAP_SEG_MIN))).cumsum()
    score = pd.Series(np.nan, index=g.index)
    cols = ["TQA_mean", "HKLD_mean", "ROP_mean"]
    rename = {"TQA_mean": "TQA", "HKLD_mean": "HKLD", "ROP_mean": "ROP"}
    for _, sub in g.groupby(seg.values, sort=True):
        x = sub[cols].rename(columns=rename)
        if len(x) < 3:
            continue
        med60 = x[["TQA", "HKLD", "ROP"]].rolling(60, min_periods=20).median().shift(1)
        mad60 = (x[["TQA", "HKLD"]] - med60[["TQA", "HKLD"]]).abs() \
            .rolling(60, min_periods=20).median().shift(1)
        mean10 = x[["TQA", "HKLD", "ROP"]].rolling(10, min_periods=3).mean()
        z_tqa = (mean10["TQA"] - med60["TQA"]) / (1.4826 * mad60["TQA"] + 1e-9)
        z_hkld = (mean10["HKLD"] - med60["HKLD"]) / (1.4826 * mad60["HKLD"] + 1e-9)
        rop_drop = ((med60["ROP"] - mean10["ROP"]) /
                    med60["ROP"].abs().clip(lower=1e-6)).clip(lower=0)
        score.loc[sub.index] = (z_tqa.fillna(0) + z_hkld.fillna(0)
                                + rop_drop.fillna(0))
    return score


def load_wells():
    data = {}
    for w in WELLS:
        b = pd.read_csv(f"{BINS}/{w}.csv.gz")
        b = b.set_index("ts_bin").sort_index()
        b.index = pd.to_datetime(b.index, unit="m", utc=True)
        ops = b[["TQA_mean", "HKLD_mean", "SWOB_mean", "RPM_mean"]].notna().any(axis=1)
        inb = (b["stuck_max"].fillna(0) >= 1) if "stuck_max" in b.columns else \
            pd.Series(False, index=b.index)
        sc = e2_score(b)
        data[w] = dict(score=sc, ops=ops, inb=inb)
        log(f"  [load {w}] grid={len(b)} ops={int(ops.sum())} inblock={int(inb.sum())} "
            f"score_finite={int(np.isfinite(sc).sum())}")
    return data


def positive_runs(te):
    """Kelompok baris positif = satu onset (menit berurutan dlm horizon H)."""
    pos = te[te.y == 1].sort_values("m")
    runs = []
    cur = []
    for _, r in pos.iterrows():
        if cur and (r["m"] - cur[-1]) > 1:
            runs.append(cur); cur = []
        cur.append(r["m"])
    if cur:
        runs.append(cur)
    return runs


def main():
    global WELLS
    t0 = time.time()
    df = pd.read_csv(DS)
    lowo = json.load(open(LOWO))
    WELLS = [f["test_well"] for f in lowo["folds"]]
    df["y"] = df["y_stuck_onset"].astype(int)
    log(f"dataset stuck_k2 rows={len(df)} test_wells={WELLS}")

    log("loading bins + computing E2 score per well (label-blind)...")
    DATA = load_wells()

    # anchor baris dataset: m = menit fitur terakhir (feat_ts_max)
    df["m"] = df["feat_ts_max"]
    df["dtm"] = pd.to_datetime(df["m"], unit="m", utc=True)
    score_all = {}
    miss_join = {}
    for w, d in DATA.items():
        s = d["score"].reindex(df.loc[df.well == w, "dtm"]).to_numpy()
        nmis = int(np.isnan(s).sum())
        miss_join[w] = nmis
        score_all[w] = np.nan_to_num(s, nan=0.0)
    df["score_e2"] = 0.0
    for w in WELLS:
        mask = (df.well == w).to_numpy()
        df.loc[mask, "score_e2"] = score_all[w]
    log(f"join score->rows missing (fill 0): {miss_join}")

    folds = []
    for f in lowo["folds"]:
        w_te = f["test_well"]
        # ---- ambang q95 dari TRAIN pooled (ops & ~inblock) ----
        tr_scores = []
        for w_tr in f["train_wells"]:
            d = DATA[w_tr]
            m = d["ops"] & ~d["inb"]
            tr_scores.append(d["score"][m].dropna().to_numpy())
        thr = float(np.quantile(np.concatenate(tr_scores), Q95))

        te = df[df.well == w_te].sort_values("m").reset_index(drop=True)
        y = te["y"].to_numpy()
        s = te["score_e2"].to_numpy()
        prev = float(y.mean())
        pred = (s >= thr).astype(int)
        tp = int(((pred == 1) & (y == 1)).sum()); fp = int(((pred == 1) & (y == 0)).sum())
        fn = int(((pred == 0) & (y == 1)).sum()); tn = int(((pred == 0) & (y == 0)).sum())
        P = tp / (tp + fp) if (tp + fp) else None
        R = tp / (tp + fn) if (tp + fn) else None
        jam_neg = int((y == 0).sum()) / 60.0
        far24 = (fp / jam_neg * 24) if jam_neg else None
        auprc = (float(average_precision_score(y, s)) if y.sum() > 0 else None)
        ci = block_bootstrap_ci(y, s) if auprc else None

        # ---- onset-level dari run positif ----
        runs = positive_runs(te)
        det, leads = 0, []
        for r in runs:
            t_e = r[-1] + 1
            sub = te[te.m.isin(r)]
            al = sub.loc[sub.score_e2 >= thr, "m"]
            if len(al):
                det += 1
                leads.append(float(t_e - al.min()))
        # persistence literal (y_prev) — onset-level
        pv = te["y_prev_stuck_onset"].fillna(0).to_numpy().astype(int)
        det_p, leads_p = 0, []
        for r in runs:
            t_e = r[-1] + 1
            sub = te[te.m.isin(r)]
            al = sub.loc[sub.y_prev_stuck_onset.fillna(0) >= 1, "m"]
            if len(al):
                det_p += 1
                leads_p.append(float(t_e - al.min()))

        auprc_p = (float(average_precision_score(y, pv.astype(float)))
                   if len(np.unique(y)) > 1 else None)
        res = {
            "fold": f"LOWO_test_{w_te}", "test_well": w_te,
            "train_wells": f["train_wells"],
            "task": "prediksi onset (H=10 menit)",
            "engine": "E2_stats (z TQA + z HKLD + ROP-drop), ambang q95-TRAIN",
            "thr_q95_train": round(thr, 6),
            "n_test": int(len(te)), "n_pos": int(y.sum()),
            "prev": round(prev, 6), "underpowered": bool(y.sum() < 30),
            "n_onsets_from_runs": len(runs),
            "engine_E2_stats": {
                "auprc": round(auprc, 4) if auprc is not None else None,
                "ci95_auprc": ci,
                "lift": round(auprc / prev, 3) if (auprc and prev) else None,
                "lift_ceiling_1_over_prev": round(1 / prev, 3) if prev else None,
                "dB_vs_prevalence_random": (round(auprc - prev, 4)
                                            if auprc is not None else None),
                "op_q95": dict(tp=tp, fp=fp, fn=fn, tn=tn, precision=P, recall=R,
                               far_per_neg_hour=(fp / jam_neg if jam_neg else None),
                               far_per_24h_neg=far24),
                "onset_level": {
                    "onsets": len(runs), "detected_at_H": det,
                    "recall_at_H": (det / len(runs) if runs else None),
                    "TLead_median_min": float(np.median(leads)) if leads else None,
                    "TLead_IQR_min": ([float(np.percentile(leads, 25)),
                                       float(np.percentile(leads, 75))] if leads else None),
                },
            },
            "baseline_prevalence_random": {
                "auprc_equals_prev": round(prev, 6), "lift_by_definition": 1.0,
                "type": "analitik",
            },
            "baseline_E0_persistence_literal": {
                "definition": "y_hat(t) = y(t-1) literal (kolom y_prev_stuck_onset)",
                "auprc": round(auprc_p, 4) if auprc_p is not None else None,
                "lift": (round(auprc_p / prev, 3)
                         if (auprc_p and prev) else None),
                "onset_level": {
                    "onsets": len(runs), "detected_at_H": det_p,
                    "recall_at_H": (det_p / len(runs) if runs else None),
                    "TLead_median_min": float(np.median(leads_p)) if leads_p else None,
                    "catatan": "persistence menyala di menit horizon ke-2..H "
                               "(label persisten) — angka ini LITERAL, bukan "
                               "konstruksi V8",
                },
            },
            "baseline_E0_persistence_v8_construction": {
                "definition": "alarm HANYA tepat di t_e (resep V8 eval_stuck E0)",
                "recall_at_H": 0.0,
                "note": "by construction alarm jatuh DI LUAR horizon [t_e-H, t_e) "
                        "-> recall 0; dilaporkan untuk kontinuitas angka V8",
            },
            "score_join_missing_fill0": miss_join.get(w_te, 0),
        }
        folds.append(res)
        e = res["engine_E2_stats"]
        log(f"  [{w_te}] n={res['n_test']} pos={res['n_pos']} prev={res['prev']} "
            f"thr={res['thr_q95_train']} AUPRC={e['auprc']} CI={e['ci95_auprc']} "
            f"lift={e['lift']} P={e['op_q95']['precision']} R={e['op_q95']['recall']} "
            f"FAR24={e['op_q95']['far_per_24h_neg']} "
            f"onsets={e['onset_level']['onsets']} R@H={e['onset_level']['recall_at_H']} "
            f"persist_R@H={res['baseline_E0_persistence_literal']['onset_level']['recall_at_H']} "
            f"up={res['underpowered']}")

    layak = [f for f in folds if not f["underpowered"]]
    auprcs = [f["engine_E2_stats"]["auprc"] for f in layak
              if f["engine_E2_stats"]["auprc"] is not None]
    lifts = [f["engine_E2_stats"]["lift"] for f in layak
             if f["engine_E2_stats"]["lift"] is not None]
    ci_contains_prev = sum(
        1 for f in layak
        if f["engine_E2_stats"]["ci95_auprc"] and
        f["engine_E2_stats"]["ci95_auprc"][0] <= f["prev"] <=
        f["engine_E2_stats"]["ci95_auprc"][1])
    summary = {
        "n_folds": len(folds), "n_layak": len(layak),
        "n_underpowered": len(folds) - len(layak),
        "auprc_range_layak": [min(auprcs), max(auprcs)] if auprcs else None,
        "lift_range_layak": [min(lifts), max(lifts)] if lifts else None,
        "lift_gt1_folds": sum(1 for x in lifts if x > 1),
        "ci95_contains_prev_folds": ci_contains_prev,
        "onset_runs_total": int(sum(f["n_onsets_from_runs"] for f in folds)),
        "elapsed_s": round(time.time() - t0, 1),
    }
    out = {"engine": "stuck_E2", "claim_task": "prediksi onset stuck (H=10 mnt)",
           "jenis_engine": "statistical (z-score + q95-train)",
           "seed": SEED, "split": "LOWO", "folds": folds, "summary": summary}
    json.dump(out, open(f"{OUT}/v9_e_stat_02_stuck_e2_RESULTS.json", "w"),
              indent=1, default=str)
    open(LOGP, "w").write("\n".join(log_lines) + "\n")
    log("SUMMARY: " + json.dumps(summary, default=str))
    log(f"DONE -> {OUT}/v9_e_stat_02_stuck_e2_RESULTS.json")


if __name__ == "__main__":
    main()
