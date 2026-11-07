#!/usr/bin/env python3
"""V9-E_RULE 03 — baseline S9 kelas bit_wear K-1 + tool_wear K-ii.

bit_wear K-1 (data: scratch/v6_e1/usrop_windows.csv, resep V6-E1d VERBATIM):
  - split LOWO 7 well (identik E1d_LOWO_RESULTS.json; fold dibangun ulang dari
    unique(well) sorted — cross-check n_test/n_pos per fold vs JSON V6).
  - persistence      = y_bitwear shift(1) per well (resep V6: subset y_prev
    non-null = n_persistence; dicetak pula versi fill-0 semua baris).
  - canary-depth     = RF kontrak HANYA MD_*+TVD_* (10 fitur) — diharapkan
    mereproduksi auprc_depth V6 (cross-check independen).
  - prevalence-random= default_rng(42) + prev + plafon 1/prev.
  - hibrida          = rule layer = LABEL ITU SENDIRI (Teale high_MSE, kanal
    terlarang) -> DEGRADASI ke persistence (dinyatakan, bukan disembunyikan).
  - K-2 onset: TIDAK DIJALANKAN — kampanye pra-reg K-2 belum terbit (R1 §3.3);
    syarat DoD (d) "bila pra-reg terbit" tidak terpenuhi -> 'belum terukur'.

tool_wear K-ii (data: scratch/v6_e1/toolwear_windows.csv, resep V8-E_A_loto):
  - split Leave-One-Tool-Out (4 fold).
  - canary 3-RMS     = RF kontrak HANYA X_rms/Y_rms/Z_rms (resep V8).
  - identity-run majority = prev (AUPRC konstan = prev; plafon lift 2,0).
  - persistence      = DIAGNOSTIK + DINYATAKAN N/A per PM1 §2.7 (label konstan
    dalam run -> y(t-1) identik dgn label run; bukan pembanding adil lintas-alat).
"""
import json
import os
import sys
import time
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import average_precision_score

sys.path.insert(0, "/mnt/d/Capstone 1(v2)/code")
from v9_e_RULE_01_status import (SEED, OUT, detector_block, fold_stats,
                                 prevalence_block, log, log_lines)  # noqa: E402

BW_CSV = "/mnt/d/Capstone 1(v2)/scratch/v6_e1/usrop_windows.csv"
BW_REF = "/mnt/d/Capstone 1(v2)/scratch/v6_e1/E1d_LOWO_RESULTS.json"
TW_CSV = "/mnt/d/Capstone 1(v2)/scratch/v6_e1/toolwear_windows.csv"
STATS = ["mean", "std", "slope", "last", "frac"]
BW_FEATS = [f"{c}_{s}" for c in ["SPP", "FLOW", "MUD", "GAM", "MD", "TVD"]
            for s in STATS]
BW_DEPTH = [f"{c}_{s}" for c in ["MD", "TVD"] for s in STATS]


def rf_fit(Xtr, ytr, Xte):
    imp = SimpleImputer(strategy="median")
    Xi = imp.fit_transform(Xtr)
    rf = RandomForestClassifier(n_estimators=300, min_samples_leaf=5,
                                class_weight="balanced_subsample",
                                random_state=SEED, n_jobs=-1)
    rf.fit(Xi, ytr)
    return rf.predict_proba(imp.transform(Xte))[:, 1]


def auprc(y, s):
    if len(y) == 0 or np.sum(y) == 0:
        return None
    return float(average_precision_score(y, s))


def rank_block(y, s):
    a = auprc(y, s)
    prev = float(np.mean(y)) if len(y) else None
    return dict(auprc=a, lift=(a / prev) if (a is not None and prev) else None,
                plafon=(1.0 / prev) if prev else None,
                prev=prev, n=int(len(y)), pos=int(np.sum(y)))


def bitwear():
    df = pd.read_csv(BW_CSV)
    assert all(c in df.columns for c in BW_FEATS), "fitur V6 tidak lengkap"
    for banned in ("MSE", "WOB", "TQ", "RPM", "ROP", "HKLD", "D_exp", "ROC"):
        assert not any(banned in c for c in BW_FEATS), banned
    ycol = "y_bitwear" if "y_bitwear" in df.columns else "y_bw"
    sortc = [c for c in ["well", "anchor_depth"] if c in df.columns]
    if len(sortc) == 2:
        df = df.sort_values(sortc).reset_index(drop=True)  # urut depth per well (resep V6)
    df["y_prev"] = df.groupby("well")[ycol].shift(1)
    ref = json.load(open(BW_REF))
    refmap = {f["well"]: f for f in ref["folds"]}
    wells = sorted(df["well"].unique())
    assert wells == sorted(refmap), (wells, sorted(refmap))
    out = {"meta": {"task": "V9-E_RULE 03a bit_wear K-1 baselines",
                    "seed": SEED, "split": "LOWO 7 well (identik E1d)",
                    "persistence": "y_bitwear shift(1) per well — subset non-null "
                                   "(konvensi V6 n_persistence) + versi fill-0",
                    "canary": "RF kontrak, fitur MD_*+TVD_* saja",
                    "hybrid": "rule layer = label (Teale high_MSE, kanal terlarang) "
                              "-> degradasi ke persistence (dinyatakan)",
                    "K2_onset": "BELUM DIJALANKAN — pra-reg K-2 belum terbit "
                                "(R1 §3.3); DoD (d) 'bila pra-reg terbit' tak terpenuhi",
                    "generated_at": time.strftime("%Y-%m-%d %H:%M:%S")},
           "folds": []}
    for i, w in enumerate(wells):
        te = df["well"] == w
        tr = ~te
        test_df, train_df = df[te], df[tr]
        y = test_df[ycol].to_numpy().astype(int)
        n, pos, prev, underp = fold_stats(y)
        r = refmap[w]
        fb = {"fold": i, "test_well": w, "n": n, "pos": pos, "prev": prev,
              "underpowered": underp,
              "crosscheck_v6": {"n_test_match": n == r["n_test"],
                                "pos_match": pos == r["n_pos"]}}
        # persistence — subset non-null (resep V6)
        yp = test_df["y_prev"]
        mnn = yp.notna().to_numpy()
        fb["persistence"] = rank_block(y[mnn], yp[mnn].to_numpy().astype(int))
        fb["persistence"]["n_persistence"] = int(mnn.sum())
        fb["persistence"]["crosscheck_v6_auprc"] = r.get("auprc_persistence")
        # persistence fill-0 semua baris (sekunder)
        ypf = yp.fillna(0).to_numpy().astype(int)
        fb["persistence_allrows"] = rank_block(y, ypf)
        # canary-depth
        s = rf_fit(train_df[BW_FEATS].loc[:, BW_DEPTH],
                   train_df[ycol].to_numpy().astype(int),
                   test_df[BW_DEPTH])
        fb["canary_depth"] = rank_block(y, s)
        fb["canary_depth"]["crosscheck_v6_auprc_depth"] = r.get("auprc_depth")
        # prevalence-random
        fb["prevalence_random"] = prevalence_block(y)
        # hybrid = persistence (rule layer degenerate — dinyatakan)
        fb["hybrid_rule_and_persistence"] = fb["persistence"]
        log(f"   BW {w}: n={n} pos={pos} pers={fb['persistence']['auprc']} "
            f"(v6={r.get('auprc_persistence')}) "
            f"canary={fb['canary_depth']['auprc']} (v6={r.get('auprc_depth')}) "
            f"nmatch={fb['crosscheck_v6']}")
        out["folds"].append(fb)
    out["aggregate"] = {
        k: {"auprc_mean": float(np.mean(v))} for k, v in {
            "persistence": [f["persistence"]["auprc"] for f in out["folds"]
                            if f["persistence"]["auprc"] is not None],
            "canary_depth": [f["canary_depth"]["auprc"] for f in out["folds"]
                             if f["canary_depth"]["auprc"] is not None],
        }.items() if v}
    return out


def toolwear():
    df = pd.read_csv(TW_CSV)
    feats = [c for c in df.columns if c not in
             ["tool", "run", "file", "start_sample", "y"]]
    assert len(feats) == 27, feats
    df["_ord"] = np.arange(len(df))
    df["y_prev"] = df.groupby("tool")["y"].shift(1)  # urutan CSV = urutan run
    tools = sorted(df["tool"].unique())
    out = {"meta": {"task": "V9-E_RULE 03b tool_wear K-ii baselines",
                    "seed": SEED, "split": "Leave-One-Tool-Out (4 fold)",
                    "canary": "RF kontrak, fitur X_rms/Y_rms/Z_rms (resep V8-E_A)",
                    "identity_majority": "AUPRC skor konstan = prev (plafon 2,0)",
                    "persistence": "DIAGNOSTIK + DINYATAKAN N/A per PM1 §2.7 "
                                   "(label konstan dalam run -> y(t-1)≡identitas-run)",
                    "generated_at": time.strftime("%Y-%m-%d %H:%M:%S")},
           "folds": []}
    for i, w in enumerate(tools):
        tr, te = df["tool"] != w, df["tool"] == w
        test_df = df[te]
        y = test_df["y"].to_numpy().astype(int)
        n, pos, prev, underp = fold_stats(y)
        fb = {"fold": i, "test_tool": w, "n": n, "pos": pos, "prev": prev,
              "underpowered": underp}
        # canary 3-RMS
        s = rf_fit(df.loc[tr, ["X_rms", "Y_rms", "Z_rms"]],
                   df.loc[tr, "y"].to_numpy().astype(int),
                   test_df[["X_rms", "Y_rms", "Z_rms"]])
        fb["canary_3rms"] = rank_block(y, s)
        # identity-run majority = prev
        fb["identity_run_majority"] = dict(auprc=(prev if prev else None),
                                           note="AUPRC skor konstan = prev")
        # persistence diagnostik (N/A-declaration)
        yp = test_df["y_prev"]
        mnn = yp.notna().to_numpy()
        fb["persistence_diagnostic"] = rank_block(
            y[mnn], yp[mnn].to_numpy().astype(int))
        fb["persistence_diagnostic"]["declared"] = (
            "N/A per PM1 §2.7: label konstan dalam run — persistence ≡ "
            "identitas-run yang sedang berjalan; bukan pembanding adil")
        fb["prevalence_random"] = prevalence_block(y)
        log(f"   TW {w}: n={n} pos={pos} canary3rms={fb['canary_3rms']['auprc']} "
            f"prev={prev} persDiag={fb['persistence_diagnostic']['auprc']}")
        out["folds"].append(fb)
    return out


def main():
    t0 = time.time()
    res = {"meta": {"seed": SEED,
                    "generated_at": time.strftime("%Y-%m-%d %H:%M:%S")},
           "bitwear_k1": bitwear(), "toolwear_kii": toolwear()}
    path = f"{OUT}/v9_e_RULE_03_bitwear_toolwear_results.json"
    json.dump(res, open(path, "w"), indent=1, allow_nan=False)
    open(f"{OUT}/v9_e_RULE_03_run_log.txt", "w").write(
        "\n".join(log_lines) + "\n")
    log(f"-> {path} ({round(time.time() - t0, 1)} s)")


if __name__ == "__main__":
    main()
