#!/usr/bin/env python3
"""V9-E_STAT 01 — engine hyd-K-i (deteksi kondisi residu SPPA).

Spesifikasi: docs/V9_PM1_ARCHITECTURE.md §2.5 (K-i) + docs/V9_R1_JUSTIFICATION.md §3.5.
- Label-forming statistic: bin qcut(TFLO,10); z = (SPPA - median_bin)/(1.4826*MAD_bin);
  anom = |z|>2 per menit; window y = valid(n_obs>=5) & (n_anom/n_obs >= 0.5), W=10 menit.
- ENGINE: persistence ŷ(t) = y(t-W) (kolom y_prev_hyd, valid_prev_hyd) — D-A5: RF DILARANG.
- BASELINE (R1 §4.1): (a) prevalence-random (AUPRC = prev, analitik);
  (b) rule |z| manual = PEMBENTUK LABEL (sirkular-by-definisi — dilaporkan sbg tautologi,
      perannya B3 beban-kerja, bukan pembanding keunggulan).
- Split: LOWO 9 fold (scratch/v9_d1/lowo_hyd_ki.json), seed 42.
- CI95: moving-block bootstrap, blok 60, 1000 resample, seed 42 (resep V8-E_hyd claim1).
- VERIFIKASI (verification-mandatory #2): recompute label dari bins/ secara independen,
  bandingkan row-level dengan label dataset.

Output (S6): scratch/v9_e_stat/v9_e_stat_01_hyd_ki_RESULTS.json + run log bertimestamp.
"""
import json, os, time
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score

SEED = 42
W, NQ, MIN_OBS = 10, 10, 5
H_DET = 10
BASE = "/mnt/d/Capstone 1(v2)"
DS = f"{BASE}/scratch/v9_d1/datasets/hyd_ki.csv.gz"
BINS = f"{BASE}/scratch/v9_d1/bins"
LOWO = f"{BASE}/scratch/v9_d1/lowo_hyd_ki.json"
OUT = f"{BASE}/scratch/v9_e_stat"
os.makedirs(OUT, exist_ok=True)
LOGP = f"{OUT}/v9_e_stat_01_run_log.txt"
log_lines = []


def log(m):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {m}"
    print(line, flush=True)
    log_lines.append(line)


def block_bootstrap_ci(y, score, n_boot=1000, block=60, seed=SEED):
    rng = np.random.default_rng(seed)
    n = len(y)
    if n < 2 * block or y.sum() == 0 or y.sum() == n:
        return None
    nb = int(np.ceil(n / block))
    vals = []
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


def operating_metrics(y, pred):
    tp = int(((pred == 1) & (y == 1)).sum())
    fp = int(((pred == 1) & (y == 0)).sum())
    fn = int(((pred == 0) & (y == 1)).sum())
    tn = int(((pred == 0) & (y == 0)).sum())
    P = tp / (tp + fp) if (tp + fp) else None
    R = tp / (tp + fn) if (tp + fn) else None
    jam_neg = (y == 0).sum() / 60.0
    far_24 = (fp / jam_neg * 24) if jam_neg else None
    return dict(tp=tp, fp=fp, fn=fn, tn=tn, precision=P, recall=R,
                far_per_neg_hour=(fp / jam_neg if jam_neg else None),
                far_per_24h_neg=far_24)


def detection_stats(y, alarm):
    """Blok positif pada deret eligible; delay = jendela pertama alarm - awal blok (menit)."""
    delays, onsets, detected_H = [], 0, 0
    n = len(y); i = 0
    while i < n:
        if y[i] == 1:
            j = i
            while j < n and y[j] == 1:
                j += 1
            onsets += 1
            nz = np.flatnonzero(alarm[i:j])
            if len(nz):
                delays.append(int(nz[0]))
                if nz[0] <= H_DET:
                    detected_H += 1
            i = j
        else:
            i += 1
    d = np.array(delays)
    return dict(onsets=onsets, detected_any=int(len(d)),
                detected_within_H10=detected_H,
                pct_detected_within_H10=(detected_H / onsets if onsets else None),
                delay_median_min=(float(np.median(d)) if len(d) else None),
                delay_p25_p75=([float(np.percentile(d, 25)), float(np.percentile(d, 75))]
                               if len(d) else None))


def hyd_bin_labels(b):
    """Label per menit — resep identik v9_d1_03.hyd_bin_labels (recompute independen)."""
    d = b.dropna(subset=["SPPA_mean", "TFLO_mean"]).copy()
    d = d[d["TFLO_mean"] > 0]
    anom = pd.Series(False, index=b.index)
    n_label_bins = 0
    if len(d) >= 50:
        try:
            d["qbin"] = pd.qcut(d["TFLO_mean"], NQ, labels=False, duplicates="drop")
        except ValueError:
            d["qbin"] = 0
        med = d.groupby("qbin")["SPPA_mean"].transform("median")
        mad = d.groupby("qbin")["SPPA_mean"].transform(
            lambda s: (s - s.median()).abs().median())
        z = (d["SPPA_mean"] - med) / (1.4826 * mad.replace(0, np.nan))
        anom.loc[d.index] = (z.abs() > 2).fillna(False)
        n_label_bins = len(d)
    B = pd.DataFrame({"ts_bin": b["ts_bin"],
                      "obs": b["SPPA_mean"].notna() & b["TFLO_mean"].notna(),
                      "anom": anom.values})
    return B, n_label_bins


def main():
    t0 = time.time()
    df = pd.read_csv(DS)
    lowo = json.load(open(LOWO))
    log(f"dataset hyd_ki rows={len(df)} wells={sorted(df.well.unique())} "
        f"folds={lowo['n_folds']}")

    # ---- (1) VERIFIKASI independen: recompute label dari bins ----
    crosscheck = {"method": "recompute hyd_bin_labels dari bins/ lalu agregasi jendela "
                            "W=10 identik v9_d1_03 (NQ=10, MIN_OBS=5)", "per_well": {}}
    df["y_recomp"] = -1
    for well, g in df.groupby("well"):
        b = pd.read_csv(f"{BINS}/{well}.csv.gz")
        B, n_bins = hyd_bin_labels(b)
        Bs = B.set_index("ts_bin")
        ts = g["ts_bin"].to_numpy()
        n_obs = np.zeros(len(ts)); n_anom = np.zeros(len(ts))
        for k in range(0, W):
            sub = Bs.reindex(ts + k)
            o = sub["obs"].fillna(False).to_numpy() & sub["anom"].notna().to_numpy()
            a = np.nan_to_num(sub["anom"].to_numpy(dtype=float), nan=0.0)
            n_obs += o.astype(float)
            n_anom += (o & (a > 0)).astype(float)
        valid = n_obs >= MIN_OBS
        y_rc = (valid & (n_anom / np.maximum(n_obs, 1) >= 0.5)).astype(int)
        idx = g.index
        df.loc[idx, "y_recomp"] = y_rc
        match = int((y_rc == g["y_hyd"].to_numpy()).sum())
        # y_prev: cek HANYA baris yang jendela sebelumnya (ts-W) ADA di dataset ini
        # (window ts-W yang terekspor pasti punya label di subset ini; di luar itu
        #  dataset dihitung dari master windows penuh — di luar jangkauan recompute ini)
        y_at = dict(zip(ts.tolist(), y_rc.tolist()))
        prev_pairs = [(y_at[int(t) - W], pv)
                      for t, pv in zip(ts, g["y_prev_hyd"].to_numpy())
                      if int(t) - W in y_at]
        prev_match = sum(1 for a, b in prev_pairs if a == b)
        crosscheck["per_well"][well] = {
            "rows": int(len(g)), "label_bins": int(n_bins),
            "y_match": match, "y_mismatch": int(len(g)) - match,
            "y_match_pct": round(100 * match / len(g), 4),
            "y_prev_pairs_in_dataset": int(len(prev_pairs)),
            "y_prev_match": prev_match,
            "y_prev_mismatch_in_dataset": int(len(prev_pairs)) - prev_match}
        log(f"  [crosscheck {well}] y_match={match}/{len(g)} "
            f"prev_match={prev_match}/{len(prev_pairs)} (pasangan dalam dataset)")
    n_mis = int((df["y_recomp"] != df["y_hyd"]).sum())
    crosscheck["total_rows"] = int(len(df))
    crosscheck["total_y_mismatch"] = n_mis
    crosscheck["verdict"] = ("LABEL TERDUPLIKASI PERSIS (0 mismatch)" if n_mis == 0
                             else f"ADA MISMATCH: {n_mis} baris — SELIDIKI sebelum pakai")
    log(f"CROSSCHECK label: mismatch={n_mis}/{len(df)} -> {crosscheck['verdict']}")

    # ---- (2) ENGINE persistence + baselines per fold LOWO ----
    folds = []
    for f in lowo["folds"]:
        w_te = f["test_well"]
        te = df[df.well == w_te].sort_values("ts_bin").reset_index(drop=True)
        y = te["y_hyd"].to_numpy().astype(int)
        prev = float(y.mean())
        pv = te["valid_prev_hyd"].to_numpy() > 0
        y_p, s_p = y[pv], te["y_prev_hyd"].to_numpy()[pv].astype(int)
        auprc = (float(average_precision_score(y_p, s_p))
                 if len(np.unique(y_p)) > 1 else None)
        ci = block_bootstrap_ci(y_p, s_p.astype(float)) if auprc else None
        lift = (auprc / prev if (auprc and prev) else None)
        res = {
            "fold": f"LOWO_test_{w_te}", "test_well": w_te,
            "train_wells": f["train_wells"],
            "task": "deteksi kondisi (bukan onset)",
            "engine": "persistence y_hat(t)=y(t-W)",
            "n_test": int(len(te)), "n_pos": int(y.sum()), "prev": round(prev, 6),
            "underpowered": bool(y.sum() < 30),
            "n_prev_valid": int(pv.sum()),
            "engine_persistence": {
                "auprc": round(auprc, 4) if auprc is not None else None,
                "ci95_auprc": ci,
                "lift": round(lift, 3) if lift else None,
                "lift_ceiling_1_over_prev": round(1 / prev, 3) if prev else None,
                "dB_vs_prevalence_random": (round(auprc - prev, 4)
                                            if auprc is not None else None),
                "op": operating_metrics(y_p, s_p),
                "det": detection_stats(y_p, s_p),
            },
            "baseline_prevalence_random": {
                "auprc_equals_prev": round(prev, 6),
                "type": "analitik (AUPRC acak = prevalensi)",
                "lift_by_definition": 1.0,
            },
            "baseline_rule_z_manual": {
                "definition": "rule |z|>2 per qcut(TFLO,10) = PEMBENTUK LABEL",
                "note": "TAUTOLOGI: rule == definisi label -> P=R=1.0 by construction; "
                        "bukan pembanding keunggulan. Nilai B3 = menghitung beban alarm.",
                "n_label_rule_alarms": int(y.sum()),
                "rule_far_per_24h_neg_definitional": (
                    float((y == 0).sum() and y.sum() / ((y == 0).sum() / 60.0) * 24)
                    if (y == 0).sum() else None),
            },
        }
        folds.append(res)
        e = res["engine_persistence"]
        log(f"  [{w_te}] n={res['n_test']} pos={res['n_pos']} prev={res['prev']} "
            f"AUPRC={e['auprc']} CI={e['ci95_auprc']} lift={e['lift']} "
            f"P={e['op']['precision']} R={e['op']['recall']} "
            f"FAR24={e['op']['far_per_24h_neg']} up={res['underpowered']}")

    layak = [f for f in folds if not f["underpowered"]]
    auprcs = [f["engine_persistence"]["auprc"] for f in layak
              if f["engine_persistence"]["auprc"] is not None]
    lifts = [f["engine_persistence"]["lift"] for f in layak
             if f["engine_persistence"]["lift"] is not None]
    summary = {
        "n_folds": len(folds), "n_layak": len(layak),
        "n_underpowered": len(folds) - len(layak),
        "auprc_range_layak": [min(auprcs), max(auprcs)] if auprcs else None,
        "lift_range_layak": [min(lifts), max(lifts)] if lifts else None,
        "lift_gt1_folds": sum(1 for x in lifts if x > 1),
        "dB_pos_folds": sum(1 for f in layak if (f["engine_persistence"]
                             ["dB_vs_prevalence_random"] or 0) > 0),
        "p_range": [min((f["engine_persistence"]["op"]["precision"] for f in layak
                         if f["engine_persistence"]["op"]["precision"] is not None),
                        default=None),
                    max((f["engine_persistence"]["op"]["precision"] for f in layak
                         if f["engine_persistence"]["op"]["precision"] is not None),
                        default=None)],
        "elapsed_s": round(time.time() - t0, 1),
    }
    out = {"engine": "hyd_ki", "claim_task": "deteksi kondisi |z|>2 residu SPPA",
           "jenis_engine": "statistical (persistence) + label-forming median/MAD",
           "seed": SEED, "split": "LOWO", "label_crosscheck": crosscheck,
           "folds": folds, "summary": summary}
    json.dump(out, open(f"{OUT}/v9_e_stat_01_hyd_ki_RESULTS.json", "w"),
              indent=1, default=str)
    open(LOGP, "w").write("\n".join(log_lines) + "\n")
    log("SUMMARY: " + json.dumps(summary, default=str))
    log(f"DONE -> {OUT}/v9_e_stat_01_hyd_ki_RESULTS.json")


if __name__ == "__main__":
    main()
