#!/usr/bin/env python3
"""V9-EVAL_B 02 — B4 (margin status-awal) untuk kelas status + verifikasi retrain RF.

Definisi (V8_R1_ABC_SPEC §1.3, PM1 §4.7):
  B4 = median jendela (menit) antara alarm dan masuknya blok label-status
       berkelanjutan (>= K_SUSTAIN menit). Alarm terdekat SEBELUM entry dalam
       lookback L (menit) -> margin = t_entry - t_alarm (>0 = peringatan awal).
  B-positif referensi: B4 median >= 1 jendela (status) — dilaporkan sebagai
  angka + konteks, BUKAN vonis biner (aturan operator).

Resep (dinyatakan, anti pilih-pilih):
  - blok = run baris y=1 per well, DIPUTUS bila jeda ts_bin > 2 menit
    (merge gap <= 2 menit, resep V8-E_shk); durasi = ts(e)-ts(s).
  - berkelanjutan = durasi >= 5 menit (K_SUSTAIN V8-E_shk pra-reg);
    run pendek dilaporkan terpisah (bukan dicampur).
  - alarm = transisi pred 0->1 per well (resep V8 alarm_events).
  - L utama = 10 menit; sensitivitas L = 30 menit.
  - konfirmasi-delay = alarm PERTAMA pada/ setelah entry (untuk persistence/rule
    yang by-construction menyusul blok) — dipisahkan dari margin.
  - grid = 1 menit (menit-integer ts_bin; konvensi E_ML/S7).

Engine deterministic: persistence (y_prev), rule_display t0-1, hybrid = rule AND
persistence, E1 (stuck_k1) — semuanya resep identik E_RULE (impor modul).
Engine RF: retrain deterministik (seed 42, resep E_ML identik) + VERIFIKASI
identitas: AUPRC fold & TP/FP per tau WAJIB sama dgn JSON E_ML (toleransi
AUPRC 1e-6, FP/TP eksak) sebelum angka B4 dipakai.

Output: scratch/v9_eval_b/_B_b4.json
"""
import json, os, sys, statistics as stat
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import average_precision_score

sys.path.insert(0, "/mnt/d/Capstone 1(v2)/code")
import v9_e_RULE_01_status as R01
import v9_e_ML_01_train as ML01

S = "/mnt/d/Capstone 1(v2)/scratch"
OUT = f"{S}/v9_eval_b"
os.makedirs(OUT, exist_ok=True)

L_PRIMARY = 10      # menit lookback margin utama
L_SENS = 30         # menit sensitivitas
K_SUSTAIN = 5       # menit "blok berkelanjutan" (V8-E_shk pra-reg)
GAP_MERGE = 2       # menit — run positif digabung bila jeda <= 2 menit
TAUS = ["0.05", "0.1", "0.2", "0.3", "0.5"]
SEED = 42
AUPRC_TOL = 1e-6

STATUS_CLASSES = ["vib", "ssi", "shk", "stuck_k1", "hyd_ki"]
RF_CLASSES = ["vib", "ssi", "shk"]          # E_ML ALLOWED; hyd_ki D-A5; stuck_k1 tanpa head ML
E_RULE_EVAL_WELLS = {                       # well yang dievaluasi E_RULE (untuk konsistensi cakupan)
    "vib": None, "ssi": None, "shk": None, "stuck_k1": None, "hyd_ki": None,
}


def med(v):
    return float(np.median(v)) if len(v) else None


def q(v, p):
    return float(np.percentile(v, p)) if len(v) else None


def find_blocks(ts, y):
    """Run baris y=1 per urutan, diputus bila jeda ts > GAP_MERGE menit."""
    blocks = []
    n = len(y)
    i = 0
    while i < n:
        if y[i] == 1:
            s = i
            j = i
            while j + 1 < n and y[j + 1] == 1 and (ts[j + 1] - ts[j]) <= GAP_MERGE:
                j += 1
            blocks.append({"s": s, "e": j, "t0": int(ts[s]), "t1": int(ts[j]),
                           "dur_mnt": int(ts[j] - ts[s])})
            i = j + 1
        else:
            i += 1
    return blocks


def alarm_times(ts, pred):
    """Transisi 0->1 pred (per urutan)."""
    pred = np.asarray(pred).astype(int)
    idx = np.flatnonzero((pred == 1) & (np.r_[0, pred[:-1]] == 0))
    return np.asarray(ts)[idx], idx


def b4_metrics(df, y, pred, L):
    """B4 pooled per kelas (alarm/blok per well, margin dipool)."""
    ts_all = df["ts_bin"].to_numpy().astype("int64")
    wells = df["well"].to_numpy()
    margins, konf, reactive = [], [], 0
    n_blocks = n_short = n_alarms = 0
    per_well = {}
    for w in pd.unique(wells):
        m = wells == w
        ts, yw, pw = ts_all[m], y[m], np.asarray(pred)[m]
        blocks = find_blocks(ts, yw)
        sus = [b for b in blocks if b["dur_mnt"] >= K_SUSTAIN]
        short = [b for b in blocks if b["dur_mnt"] < K_SUSTAIN]
        ats, _ = alarm_times(ts, pw)
        n_alarms += len(ats)
        wm, wk, wrea = [], [], 0
        for b in sus:
            pre = ats[(ats >= b["t0"] - L) & (ats < b["t0"])]
            if len(pre):
                wm.append(int(b["t0"] - pre.max()))          # alarm terdekat sebelum entry
            post = ats[(ats >= b["t0"])]
            if len(post) and post.min() <= b["t1"] + 30:
                wk.append(int(post.min() - b["t0"]))          # konfirmasi-delay (bisa <=0)
            wrea += int(((ats >= b["t0"]) & (ats <= b["t1"])).sum())
        margins += wm
        konf += wk
        reactive += wrea
        n_blocks += len(sus)
        n_short += len(short)
        per_well[w] = {"n_sustained": len(sus), "n_short": len(short),
                       "n_alarms": int(len(ats)),
                       "n_covered": len(wm), "margins": wm,
                       "konfirmasi_delays": wk, "n_reactive": wrea}
    out = {
        "n_blocks_sustained_ge5mnt": n_blocks,
        "n_runs_short": n_short,
        "n_alarms": n_alarms,
        "B4_coverage": (len(margins) / n_blocks) if n_blocks else None,
        "B4_median_margin_mnt": med(margins),
        "B4_IQR_margin_mnt": [q(margins, 25), q(margins, 75)] if margins else None,
        "margins_mnt": margins,
        "konfirmasi_delay_median_mnt": med(konf),
        "konfirmasi_delays_mnt": konf,
        "n_alarms_reaktif_dalam_blok": reactive,
        "per_well": per_well,
    }
    return out


def compute_blocks_summary(df, ycol):
    y = df[ycol].to_numpy().astype(int)
    ts = df["ts_bin"].to_numpy().astype("int64")
    wells = df["well"].to_numpy()
    n_short = n_sus = 0
    lens = []
    for w in pd.unique(wells):
        m = wells == w
        for b in find_blocks(ts[m], y[m]):
            lens.append(b["dur_mnt"])
            if b["dur_mnt"] >= K_SUSTAIN:
                n_sus += 1
            else:
                n_short += 1
    return {"n_runs_total": len(lens), "n_sustained_ge5mnt": n_sus,
            "n_short": n_short, "runlen_mnt_median": med(lens),
            "runlen_mnt_max": max(lens) if lens else None}


def rf_train_scores(df, feats, tr_mask, te_mask, y_tr, engine):
    imp = SimpleImputer(strategy="median")
    X_tr = imp.fit_transform(df.loc[tr_mask, feats])
    X_te = imp.transform(df.loc[te_mask, feats])
    rf = RandomForestClassifier(
        n_estimators=ML01.RF_N_EST.get(engine, 300), min_samples_leaf=5,
        class_weight="balanced_subsample", random_state=SEED, n_jobs=-1)
    rf.fit(X_tr, y_tr)
    return rf.predict_proba(X_te)[:, 1]


def main():
    res = {"meta": {
        "task": "V9-EVAL_B 02 — B4 margin status-awal",
        "defs": {"B4": "median menit antara alarm terdekat sebelum entry blok berkelanjutan >=5 mnt",
                 "L_primary_mnt": L_PRIMARY, "L_sensitivitas_mnt": L_SENS,
                 "K_SUSTAIN_mnt": K_SUSTAIN, "GAP_MERGE_mnt": GAP_MERGE,
                 "grid": "1 menit (ts_bin integer)"},
        "resep": "persistence=y_prev; rule=rule_display t0-1 (impor R01); hybrid=rule AND "
                 "persistence; RF=retrain seed42 resep E_ML + verifikasi identitas",
    }, "classes": {}}

    for cls in STATUS_CLASSES:
        cfg = R01.CLS[cls]
        ycol, pcol = cfg["y"], cfg["prev"]
        df = pd.read_csv(f"{S}/v9_d1/datasets/{cls}.csv.gz")
        df = df.sort_values(["well", "ts_bin"]).reset_index(drop=True)
        y = df[ycol].to_numpy().astype(int)
        print(f"== {cls}: rows={len(df)} pos={int(y.sum())}", flush=True)

        blk = compute_blocks_summary(df, ycol)
        engines = {}

        # persistence
        pred_pers = df[pcol].fillna(0).to_numpy().astype(int)
        engines["persistence"] = {
            "L10": b4_metrics(df, y, pred_pers, L_PRIMARY),
            "L30": b4_metrics(df, y, pred_pers, L_SENS)}

        # rule display t0-1 (resep E_RULE)
        r_pred, r_nodata = R01.rule_display(cls, df)
        engines["rule_display_t0minus1"] = {
            "n_nodata": int(r_nodata.sum()),
            "L10": b4_metrics(df, y, r_pred, L_PRIMARY),
            "L30": b4_metrics(df, y, r_pred, L_SENS)}

        # hybrid = rule AND persistence
        hyb = ((r_pred == 1) & (pred_pers == 1)).astype(np.int8)
        engines["hybrid_rule_and_persistence"] = {
            "L10": b4_metrics(df, y, hyb, L_PRIMARY),
            "L30": b4_metrics(df, y, hyb, L_SENS)}

        # E1 (stuck_k1 saja)
        if cls == "stuck_k1":
            e1_pred, e1_nodata = R01.rule_e1(df)
            engines["rule_E1_2of3"] = {
                "n_nodata": int(e1_nodata.sum()),
                "L10": b4_metrics(df, y, e1_pred, L_PRIMARY),
                "L30": b4_metrics(df, y, e1_pred, L_SENS)}

        # cross-check FP vs E_RULE JSON (fold wells)
        r1 = json.load(open(f"{S}/v9_e_rule/v9_e_RULE_01_status_results.json"))
        folds_wells = [f["test_well"] for f in r1["classes"][cls]["folds"]]
        json_fp = {m: r1["classes"][cls]["aggregate"].get(m, {}) for m in []}
        fold_fp = {}
        for m in r1["classes"][cls]["folds"]:
            for k in ["persistence", "rule_display_t0minus1",
                      "hybrid_rule_and_persistence", "rule_E1_2of3"]:
                if k in m:
                    fold_fp[k] = fold_fp.get(k, 0) + m[k]["fp"]
        mask_eval = df["well"].isin(folds_wells)
        my_fp = {}
        for name, pred in [("persistence", pred_pers),
                           ("rule_display_t0minus1", r_pred),
                           ("hybrid_rule_and_persistence", hyb)]:
            if name == "persistence":
                p = pred
            else:
                p = pred
            my_fp[name] = int(((p == 1) & (y == 0) & mask_eval.to_numpy()).sum())
        if cls == "stuck_k1":
            my_fp["rule_E1_2of3"] = int(((e1_pred == 1) & (y == 0)
                                          & mask_eval.to_numpy()).sum())
        xcheck = {k: {"mine": my_fp.get(k), "E_RULE": fold_fp.get(k),
                      "match": my_fp.get(k) == fold_fp.get(k)}
                  for k in sorted(set(my_fp) | set(fold_fp))}

        # --- RF (retrain + verifikasi identitas) ---
        rf_part = None
        if cls in RF_CLASSES:
            mlj = json.load(open(f"{S}/v9_e_ml/v9_e_ML_{cls}_RESULTS.json"))
            feats = mlj["feature_cols"]
            lowo = json.load(open(f"{S}/v9_d1/lowo_{cls}.json"))
            folds_out = []
            auprc_ok = tau_ok = n_checks = 0
            for i, fold in enumerate(lowo["folds"]):
                tw = fold["test_well"]
                tr_mask = df["well"].isin(fold["train_wells"])
                te_mask = df["well"] == tw
                y_tr = df.loc[tr_mask, ycol].to_numpy().astype(int)
                scores = rf_train_scores(df, feats, tr_mask, te_mask, y_tr, cls)
                y_te = df.loc[te_mask, ycol].to_numpy().astype(int)
                mine_ap = float(average_precision_score(y_te, scores))
                json_fold = mlj["folds"][i]
                assert json_fold["test_well"] == tw, f"fold mismatch {cls} {i}"
                ref_ap = json_fold["models"]["rf"]["auprc"]
                ap_match = abs(mine_ap - ref_ap) <= AUPRC_TOL
                auprc_ok += int(ap_match)
                n_checks += 1
                tau_chk = {}
                for tau in TAUS:
                    pred = (scores >= float(tau)).astype(int)
                    fp = int(((pred == 1) & (y_te == 0)).sum())
                    tp = int(((pred == 1) & (y_te == 1)).sum())
                    ref = json_fold["models"]["rf"]["tau_metrics"][tau]
                    ok = (fp == ref["FP"] and tp == ref["TP"])
                    tau_ok += int(ok)
                    tau_chk[tau] = {"FP_mine": fp, "TP_mine": tp,
                                    "FP_json": ref["FP"], "TP_json": ref["TP"],
                                    "match": ok}
                # B4 per fold (test well) per tau, L10 + L30
                sub = df.loc[te_mask].reset_index(drop=True)
                ysub = df.loc[te_mask, ycol].to_numpy().astype(int)
                b4t = {}
                for tau in TAUS:
                    pred = (scores >= float(tau)).astype(int)
                    b4t[tau] = {"L10": b4_metrics(sub, ysub, pred, L_PRIMARY),
                                "L30": b4_metrics(sub, ysub, pred, L_SENS)}
                folds_out.append({"fold": i, "test_well": tw,
                                  "auprc_mine": mine_ap, "auprc_json": ref_ap,
                                  "auprc_absdiff": abs(mine_ap - ref_ap),
                                  "auprc_match": ap_match,
                                  "tau_check": tau_chk, "b4_per_fold": b4t})
                print(f"   fold {i} {tw}: ap diff={abs(mine_ap-ref_ap):.2e} "
                      f"ap_match={ap_match} tau_ok={sum(int(v['match']) for v in tau_chk.values())}/5",
                      flush=True)
            # pooled B4 per tau (semua fold = semua well)
            pooled = {}
            for tau in TAUS:
                for Lv in ("L10", "L30"):
                    margins, konf = [], []
                    nb = ns = na = nr = 0
                    for fo in folds_out:
                        b = fo["b4_per_fold"][tau][Lv]
                        margins += b["margins_mnt"]
                        konf += b["konfirmasi_delays_mnt"]
                        nb += b["n_blocks_sustained_ge5mnt"]
                        ns += b["n_runs_short"]
                        na += b["n_alarms"]
                        nr += b["n_alarms_reaktif_dalam_blok"]
                    pooled.setdefault(tau, {})[Lv] = {
                        "n_blocks_sustained_ge5mnt": nb, "n_runs_short": ns,
                        "n_alarms": na,
                        "B4_coverage": (len(margins) / nb) if nb else None,
                        "B4_median_margin_mnt": med(margins),
                        "B4_IQR_margin_mnt": [q(margins, 25), q(margins, 75)] if margins else None,
                        "n_alarms_reaktif_dalam_blok": nr,
                    }
            rf_part = {"folds": folds_out,
                       "verifikasi": {"auprc_match": f"{auprc_ok}/{n_checks}",
                                      "tau_fp_tp_match": f"{tau_ok}/{n_checks * len(TAUS)}",
                                      "toleransi_auprc": AUPRC_TOL},
                       "b4_pooled_per_tau": pooled}

        res["classes"][cls] = {
            "dataset_rows": int(len(df)), "pos": int(y.sum()),
            "folds_E_RULE_wells": folds_wells,
            "blocks": blk, "engines": engines,
            "crosscheck_fp_vs_E_RULE": xcheck,
            "rf_retrain": rf_part,
        }
        # ringkas
        for nm, e in engines.items():
            b = e["L10"]
            print(f"   {nm}: cov={b['B4_coverage']} B4med={b['B4_median_margin_mnt']} "
                  f"konf_med={b['konfirmasi_delay_median_mnt']} nblk={b['n_blocks_sustained_ge5mnt']} "
                  f"alarms={b['n_alarms']}", flush=True)
        for k, v in xcheck.items():
            if not v["match"]:
                print(f"   XCHECK MISMATCH {cls} {k}: {v}", flush=True)

    outp = f"{OUT}/_B_b4.json"
    json.dump(res, open(outp, "w"), indent=1, allow_nan=False)
    print("saved", outp)


if __name__ == "__main__":
    main()
