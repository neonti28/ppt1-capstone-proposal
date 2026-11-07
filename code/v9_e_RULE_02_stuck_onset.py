#!/usr/bin/env python3
"""V9-E_RULE 02 — baseline + rule E1 pada kelas ONSET stuck_k2 (H=10 menit).

Engines/baselines per fold LOWO (lowo_stuck_k2.json, fold identik D1):
  E0a persistence_horizon = y_prev_stuck_onset (resep D1: y(t-1) pada label
     horizon) — TES PEMBEDA utama. CATATAN: label horizon mensyaratkan
     pengetahuan t_e di masa lalu -> baseline IN-DEPLOYMENT tidak mungkin;
     dipakai sebagai upper-bound/tes formulasi, bukan pembanding adil harian.
  E0b persistence_event    = 1[peristiwa onset tepat di menit t-1] — literal
     R1 E0 "pada deret onset" (diharapkan recall ~0 per konstruksi).
  E1 rule 2-dari-3         = z(TQA)>2 + z(HKLD)>2 + ROP-drop>=30% >= 2,
     z vs median+MAD jendela 60 menit strict-past dari bins (resep PM1 §2.4/R1).
  prevalence-random        = default_rng(42); plafon 1/prev.
  canary-depth             = RF kontrak, fitur depth/dbtm saja.
Metrik: AUPRC/lift/plafon, P/R/FP/FAR_24h (konvensi V8), B1 (% onset tercakup
alarm di [t_e-10,t_e)), TLead median/IQR (menit) per fold.
"""
import json
import os
import sys
import time
import numpy as np
import pandas as pd

sys.path.insert(0, "/mnt/d/Capstone 1(v2)/code")
from v9_e_RULE_01_status import (  # noqa: E402
    SEED, DS, LOWO, OUT, detector_block, binary_metrics, auprc,
    fold_stats, prevalence_block, canary_depth, e1_alarm_series, log,
    log_lines)

H = 10
CLS_RP = "stuck"


def onset_events(test_df):
    """Menit peristiwa t_e unik per well (dari lab_kind='onset_event', lab_ts=t_e)."""
    ev = test_df.loc[test_df["lab_kind"] == "onset_event", "lab_ts"]
    return sorted(set(ev.astype("int64")))


def event_persistence(df):
    """ŷ(t) = 1[menit t-1 adalah menit peristiwa onset] — PER WELL (hindari
    silang-wellbore F-9/F-9_A yang rentangnya berimpit)."""
    out = np.zeros(len(df), np.int8)
    for _, g in df.groupby("well"):
        ev = g.loc[g["lab_kind"] == "onset_event", "lab_ts"].astype("int64")
        evset = set(ev.unique())
        ts = g["ts_bin"].to_numpy().astype("int64")
        out[g.index.to_numpy()] = (np.isin(ts - 1, list(evset)).astype(np.int8)
                                   if evset else 0)
    return out


def alarm_onset_stats(df, pred, events):
    """B1 + TLead per onset: onset dikenali dari baris onset_event (lab_ts=t_e)."""
    sub = df.loc[pred == 1, ["ts_bin", "lab_kind", "lab_ts", "well"]]
    ev_rows = df[df["lab_kind"] == "onset_event"]
    alarms, leads = {}, []
    for _, r in sub.iterrows():
        if r["lab_kind"] == "onset_event":
            te = int(r["lab_ts"])
            lead = te - int(r["ts_bin"])
            alarms.setdefault(te, []).append(lead)
    covered, lead_all = 0, []
    for te in events:
        if te in alarms:
            covered += 1
            lead_all.append(min(alarms[te]))
    b1 = (covered / len(events)) if events else None
    if lead_all:
        q = np.percentile(lead_all, [25, 50, 75])
        tlead = dict(n=len(lead_all), median=float(q[1]), iqr=[float(q[0]), float(q[2])],
                     min=int(np.min(lead_all)), max=int(np.max(lead_all)))
    else:
        tlead = dict(n=0, median=None, iqr=None, min=None, max=None)
    fp = int(((pred == 1) & (df["y_stuck_onset"].to_numpy() == 0)).sum())
    return dict(n_onsets=len(events), b1_covered=covered, b1=b1,
                tlead_min=tlead, fp_alarm=fp)


def main():
    t0 = time.time()
    df = pd.read_csv(f"{DS}/stuck_k2.csv.gz")
    lowo = json.load(open(f"{LOWO}/lowo_stuck_k2.json"))
    ycol = "y_stuck_onset"
    meta = ["well", "ts_bin", "feat_ts_max", "lab_ts", "lab_kind"]
    feat_cols = [c for c in df.columns if c not in meta
                 and not c.startswith(("y_", "valid_", "obs_", "anom_"))]
    depth_cols = [c for c in feat_cols
                  if c.startswith("depth_") or c.startswith("dbtm_")]
    df["_e1"] = 0
    for w in df["well"].unique():
        m = df["well"] == w
        s = e1_alarm_series(w)
        ts = df.loc[m, "ts_bin"].to_numpy().astype("int64")
        df.loc[m, "_e1"] = s.reindex(pd.Index(ts - 1)).fillna(0).to_numpy().astype(np.int8)
    df["_pev"] = event_persistence(df)
    log(f"== stuck_k2: rows={len(df)} pos={int(df[ycol].sum())} "
        f"folds={lowo['n_folds']} e1_alarm_total={int(df['_e1'].sum())} "
        f"event_persist_pos={int(df['_pev'].sum())}")

    out = {"meta": {"task": "V9-E_RULE 02 stuck onset baselines",
                    "seed": SEED, "H_min": H,
                    "far_convention": "FAR_24h = FP/(n_neg/60)*24 (V8 claim1)",
                    "E0a_caveat": "persistence_horizon = y(t-1) pada label horizon — "
                                  "butuh pengetahuan t_e lampau (hindsight); dipakai sbg "
                                  "tes formulasi/upper-bound, bukan detektor deployable",
                    "E0b": "persistence_event literal R1 E0 (deret peristiwa)",
                    "E1": "2-dari-3 z(TQA)>2 z(HKLD)>2 ROP-drop>=30%, MAD 60mnt strict-past",
                    "generated_at": time.strftime("%Y-%m-%d %H:%M:%S")},
           "folds": []}

    for i, fold in enumerate(lowo["folds"]):
        te = fold["test_well"]
        mte = df["well"] == te
        mtr = df["well"].isin(fold["train_wells"])
        test_df = df[mte].reset_index(drop=True)
        y = test_df[ycol].to_numpy().astype(int)
        n, pos, prev, underp = fold_stats(y)
        events = onset_events(test_df)
        fb = {"fold": i, "test_well": te, "n": n, "pos": pos, "prev": prev,
              "underpowered": underp, "n_onsets": len(events)}

        # E0a persistence horizon
        pa = test_df["y_prev_stuck_onset"].to_numpy().astype(int)
        fb["persistence_horizon"] = detector_block(y, pa)
        fb["persistence_horizon"]["onset"] = alarm_onset_stats(test_df, pa, events)

        # E0b persistence event
        pb = test_df["_pev"].to_numpy().astype(int)
        fb["persistence_event"] = detector_block(y, pb)
        fb["persistence_event"]["onset"] = alarm_onset_stats(test_df, pb, events)

        # E1 rule
        e1 = test_df["_e1"].to_numpy().astype(np.int8)
        fb["rule_E1_2of3"] = detector_block(y, e1)
        fb["rule_E1_2of3"]["onset"] = alarm_onset_stats(test_df, e1, events)

        # prevalence-random
        fb["prevalence_random"] = prevalence_block(y)

        # canary-depth
        fb["canary_depth"] = canary_depth(df[mtr], test_df, depth_cols, ycol)

        log(f"   {te}: n={n} pos={pos} prev={prev:.4f} onsets={len(events)} "
            f"persH.auprc={fb['persistence_horizon']['auprc']} "
            f"B1={fb['persistence_horizon']['onset']['b1']} "
            f"persE.auprc={fb['persistence_event']['auprc']} "
            f"FP={fb['persistence_event']['fp']} "
            f"E1.auprc={fb['rule_E1_2of3']['auprc']} "
            f"E1.B1={fb['rule_E1_2of3']['onset']['b1']} "
            f"canary={fb['canary_depth']['auprc']}")
        out["folds"].append(fb)

    agg = {}
    for k in ["persistence_horizon", "persistence_event", "rule_E1_2of3",
              "canary_depth", "prevalence_random"]:
        vals = [f[k]["auprc"] for f in out["folds"] if f[k].get("auprc") is not None]
        agg[k] = dict(auprc_mean=float(np.mean(vals)) if vals else None,
                      n_folds=len(vals))
        if k in ("persistence_horizon", "persistence_event", "rule_E1_2of3"):
            b1s = [f[k]["onset"]["b1"] for f in out["folds"]
                   if f[k]["onset"]["b1"] is not None]
            leads = [f[k]["onset"]["tlead_min"]["median"] for f in out["folds"]
                     if f[k]["onset"]["tlead_min"]["median"] is not None]
            agg[k]["b1_mean"] = float(np.mean(b1s)) if b1s else None
            agg[k]["tlead_median_of_foldmedians"] = float(np.median(leads)) if leads else None
    out["aggregate"] = agg

    path = f"{OUT}/v9_e_RULE_02_stuck_onset_results.json"
    json.dump(out, open(path, "w"), indent=1, allow_nan=False)
    open(f"{OUT}/v9_e_RULE_02_run_log.txt", "w").write(
        "\n".join(log_lines) + "\n")
    log(f"-> {path} ({round(time.time() - t0, 1)} s)")


if __name__ == "__main__":
    main()
