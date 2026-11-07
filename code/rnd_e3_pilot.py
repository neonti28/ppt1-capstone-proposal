#!/usr/bin/env python3
"""RND-E3 — eksekusi pilot pada engine hyd K-i.

Dua finalis (protokol E2 §4.1 dan varian deteksi-perubahan E2 §4.2 yang dipindah ke hyd):
  A1  LightGBM + ambang conformal cross-conformal (CV+) di dalam fold.
  A2  CUSUM dua sisi pada residu SPPA terstandar (z label-forming), ambang dikalibrasi di dalam fold.

Split: LOWO 9 fold (scratch/v9_d1/lowo_hyd_ki.json), unit = well.
Anti-bocor: kolom turunan label (y_hyd, y_prev_hyd, valid_prev_hyd, obs_hyd, anom_hyd,
lab_ts, lab_kind) TIDAK dipakai sebagai fitur (E0 K-5 / E2 §2.3 L3).

Keluaran JSON: scratch/rnd/e3/
  e3_a_conformal_results.json, e3_b_cusum_results.json, e3_baseline_results.json,
  e3_pairing.csv, e3_cakupan.json, e3_run_summary.json
"""
import argparse, json, os, sys, time, warnings
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score

warnings.filterwarnings("ignore")

BASE = "/mnt/d/Capstone 1(v2)"
DS = f"{BASE}/scratch/v9_d1/datasets/hyd_ki.csv.gz"
LOWO = f"{BASE}/scratch/v9_d1/lowo_hyd_ki.json"
BINSD = f"{BASE}/scratch/v9_d1/bins"
OUT = f"{BASE}/scratch/rnd/e3"
os.makedirs(OUT, exist_ok=True)

W = 10                 # panjang jendela label (menit) dari resep V9-D1_03
H_DET = 10             # ambang delay deteksi (menit), sama dengan v9_e_STAT_01
LABEL_DERIVED = ("y_hyd", "y_prev_hyd", "valid_prev_hyd", "obs_hyd", "anom_hyd",
                 "lab_ts", "lab_kind", "feat_ts_max")
ALPHAS = [0.0005, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.10, 0.20, 0.30]
H_GRID = [1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0, 15.0, 20.0, 30.0]
CUSUM_K = 0.5          # referensi CUSUM dalam satuan sigma


# ---------------------------------------------------------------- utilitas
def log(msg, store=None):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    if store is not None:
        store.append(line)


def load_data():
    df = pd.read_csv(DS)
    feats = [c for c in df.columns if c not in LABEL_DERIVED]
    feats = [c for c in feats if pd.api.types.is_numeric_dtype(df[c])]
    return df, feats


def op_metrics(y, pred):
    """Resep v9_e_STAT_01: FAR_24 = FP / (n_neg/60) * 24, n_neg = jumlah jendela negatif."""
    y = np.asarray(y).astype(int)
    pred = np.asarray(pred).astype(int)
    tp = int(((pred == 1) & (y == 1)).sum())
    fp = int(((pred == 1) & (y == 0)).sum())
    fn = int(((pred == 0) & (y == 1)).sum())
    tn = int(((pred == 0) & (y == 0)).sum())
    n_neg = int((y == 0).sum())
    jam_neg = n_neg / 60.0
    return dict(
        tp=tp, fp=fp, fn=fn, tn=tn, n_neg=n_neg,
        precision=(tp / (tp + fp)) if (tp + fp) else None,
        recall=(tp / (tp + fn)) if (tp + fn) else None,
        far_per_24h=(fp / jam_neg * 24.0) if jam_neg else None,
        jam_neg=jam_neg,
    )


def garwood_upper(k, jam_neg, alpha=0.95):
    """Batas atas laju 95 persen dua sisi untuk k kejadian (Garwood / chi-square)."""
    from scipy.stats import chi2
    if jam_neg <= 0:
        return None
    hi = chi2.ppf(1 - (1 - alpha) / 2, 2 * (k + 1)) / 2.0
    return hi / jam_neg * 24.0


def detection_stats(y, alarm):
    """Delay deteksi per blok positif berurutan (menit-jendela), resep v9_e_STAT_01."""
    delays, onsets, detected_H = [], 0, 0
    n = len(y)
    i = 0
    while i < n:
        if y[i] == 1:
            j = i
            while j < n and y[j] == 1:
                j += 1
            onsets += 1
            nz = np.flatnonzero(np.asarray(alarm[i:j]))
            if len(nz):
                delays.append(int(nz[0]))
                if nz[0] <= H_DET:
                    detected_H += 1
            i = j
        else:
            i += 1
    return dict(onsets=onsets, detected_any=len(delays), detected_within_H10=detected_H,
                pct_detected=round(detected_H / onsets, 4) if onsets else None,
                delay_median_min=float(np.median(delays)) if delays else None)


def block_bootstrap_ci(y, score, n_boot=400, block=60, seed=42):
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
    return [round(float(np.percentile(vals, 2.5)), 4), round(float(np.percentile(vals, 97.5)), 4)]


# ---------------------------------------------------------------- CUSUM series
def cusum_series(z, k=CUSUM_K, reset=True):
    """CUSUM dua sisi kausal. reset=True: kembali 0 setelah alarm (Page-Hinkley reset)."""
    z = np.asarray(z, dtype=float)
    cp = np.zeros(len(z)); cn = np.zeros(len(z)); al = np.zeros(len(z), dtype=int)
    thr = np.inf
    for i, v in enumerate(z):
        prev_p = cp[i - 1] if i else 0.0
        prev_n = cn[i - 1] if i else 0.0
        cp[i] = max(0.0, prev_p + (v - k))
        cn[i] = max(0.0, prev_n + (-v - k))
        if thr < np.inf and (cp[i] > thr or cn[i] > thr):
            al[i] = 1
            if reset:
                cp[i] = 0.0; cn[i] = 0.0
    return cp, cn, al


def cusum_alarms(z, h, reset=True):
    """Alarm per menit untuk ambang h."""
    z = np.asarray(z, dtype=float)
    cp = np.zeros(len(z)); cn = np.zeros(len(z)); al = np.zeros(len(z), dtype=int)
    for i, v in enumerate(z):
        prev_p = cp[i - 1] if i else 0.0
        prev_n = cn[i - 1] if i else 0.0
        cp[i] = max(0.0, prev_p + (v - k_glob))
        cn[i] = max(0.0, prev_n + (-v - k_glob))
        if cp[i] > h or cn[i] > h:
            al[i] = 1
            if reset:
                cp[i] = 0.0; cn[i] = 0.0
    return al


k_glob = CUSUM_K


def build_z(well):
    """z SPPA per menit, resep label V9-D1_03: qcut(TFLO,10), median/MAD per bin."""
    b = pd.read_csv(f"{BINSD}/{well}.csv.gz")
    b = b.dropna(subset=["SPPA_mean", "TFLO_mean"]).copy()
    if len(b) < 50:
        return None
    try:
        b["qbin"] = pd.qcut(b["TFLO_mean"], 10, labels=False, duplicates="drop")
    except Exception:
        return None
    med = b.groupby("qbin")["SPPA_mean"].transform("median")
    mad = (b["SPPA_mean"] - med).abs().groupby(b["qbin"]).transform("median")
    mad = mad.replace(0, np.nan)
    b["z"] = (b["SPPA_mean"] - med) / (1.4826 * mad)
    b = b.dropna(subset=["z"]).sort_values("ts_bin")
    return b[["ts_bin", "z"]].reset_index(drop=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", default="42")
    ap.add_argument("--skip-cusum", action="store_true")
    args = ap.parse_args()
    seeds = [int(s) for s in args.seeds.split(",")]

    t_start = time.time()
    runlog = []
    df, feats = load_data()
    lowo = json.load(open(LOWO))
    folds = lowo["folds"]
    log(f"data {df.shape} featur {len(feats)} fold {len(folds)} seed {seeds}", runlog)

    # --- baseline yang dihitung ulang pada fold yang sama -------------------
    base_rows = []
    for f in folds:
        w = f["test_well"]
        d = df[df["well"] == w].sort_values("ts_bin").reset_index(drop=True)
        y = d["y_hyd"].to_numpy(int)
        pers = np.where(d["valid_prev_hyd"].to_numpy(int) == 1,
                        d["y_prev_hyd"].to_numpy(int), 0)
        # proxy rule t0-1: label satu baris (1 menit) sebelumnya di dalam well yang sama
        rule_lag = np.concatenate([[0], y[:-1]])
        hyb = (rule_lag & pers).astype(int)
        for nama, pred in (("persistence", pers), ("hybrid_rule_lag1_and_persistence", hyb)):
            m = op_metrics(y, pred)
            m.update(dict(fold=f"LOWO_test_{f['test_well']}", test_well=w, model=nama,
                          prev=float(y.mean()), n=len(y), n_pos=int(y.sum())))
            m["garwood_upper_95"] = garwood_upper(m["fp"], m["jam_neg"])
            m["syarat_4x_fp"] = bool(m["jam_neg"] >= 4 * m["fp"]) if m["fp"] else None
            base_rows.append(m)
        log(f"baseline {w}: pers FP={op_metrics(y, pers)['fp']} "
            f"hyb FP={op_metrics(y, hyb)['fp']}", runlog)

    json.dump(dict(
        deskripsi="Baseline dihitung ulang pada 9 fold LOWO yang sama dengan finalis. "
                  "rule t0-1 didekati dengan label satu menit sebelumnya di dalam well yang sama "
                  "(proxy; total FP dibandingkan dengan angka terbit E_RULE 2.091 / hybrid 927).",
        folds=base_rows,
        total_fp={"persistence": int(sum(r["fp"] for r in base_rows if r["model"] == "persistence")),
                  "hybrid_rule_lag1_and_persistence": int(sum(r["fp"] for r in base_rows
                                                              if r["model"] == "hybrid_rule_lag1_and_persistence"))},
    ), open(f"{OUT}/e3_baseline_results.json", "w"), indent=2)

    # --- A1: LightGBM + conformal -------------------------------------------
    import lightgbm as lgb

    def fit_lgb(Xtr, ytr, seed):
        m = lgb.LGBMClassifier(
            n_estimators=100, num_leaves=15, learning_rate=0.1,
            min_child_samples=50, subsample=0.8, subsample_freq=1,
            colsample_bytree=0.8, reg_lambda=1.0, random_state=seed,
            n_jobs=4, verbose=-1,
        )
        m.fit(Xtr, ytr)
        return m

    a_folds, a_thr = [], []
    for seed in seeds:
        for f in folds:
            w = f["test_well"]; inner = f["train_wells"]
            dtr_all = df[df["well"].isin(inner)]
            dte = df[df["well"] == w].sort_values("ts_bin").reset_index(drop=True)
            # out-of-fold calibration scores di 8 fold dalam (CV+)
            oof_score, oof_y, oof_well = [], [], []
            for j in inner:
                tr = dtr_all[dtr_all["well"] != j]
                ca = dtr_all[dtr_all["well"] == j]
                m = fit_lgb(tr[feats], tr["y_hyd"].to_numpy(int), seed)
                oof_score.append(m.predict_proba(ca[feats])[:, 1])
                oof_y.append(ca["y_hyd"].to_numpy(int))
                oof_well.append(np.array([j] * len(ca)))
            s_oof = np.concatenate(oof_score); y_oof = np.concatenate(oof_y)
            w_oof = np.concatenate(oof_well)
            # model final pada 8 well dalam
            m_final = fit_lgb(dtr_all[feats], dtr_all["y_hyd"].to_numpy(int), seed)
            s_te = m_final.predict_proba(dte[feats])[:, 1]
            y_te = dte["y_hyd"].to_numpy(int)

            # titik operasi: alpha terkecil (paling konservatif) yang masih memberi
            # minimal 1 alarm benar di SETIAP 8 fold dalam
            pilih, kandidat = None, []
            for a in ALPHAS:
                neg = s_oof[y_oof == 0]
                thr = float(np.quantile(neg, 1 - a))
                tp_per = []
                for j in inner:
                    mj = w_oof == j
                    tp_per.append(int(((s_oof[mj] >= thr) & (y_oof[mj] == 1)).sum()))
                ok = all(t >= 1 for t in tp_per)
                kandidat.append(dict(alpha=a, threshold=thr, tp_inner=tp_per, ok=ok))
                if ok and pilih is None:
                    pilih = dict(alpha=a, threshold=thr, tp_inner=tp_per)
                    break
            fallback = pilih is None
            if fallback:
                best = max(kandidat, key=lambda r: (sum(t >= 1 for t in r["tp_inner"]), -r["alpha"]))
                pilih = dict(alpha=best["alpha"], threshold=best["threshold"],
                             tp_inner=best["tp_inner"])

            pred = (s_te >= pilih["threshold"]).astype(int)
            m = op_metrics(y_te, pred)
            m.update(dict(
                fold=f"LOWO_test_{f['test_well']}", test_well=w, seed=seed, alpha=pilih["alpha"],
                threshold=round(pilih["threshold"], 6), fallback=fallback,
                tp_inner=pilih["tp_inner"], n=len(y_te), n_pos=int(y_te.sum()),
                prev=round(float(y_te.mean()), 6),
                auprc=round(float(average_precision_score(y_te, s_te)), 4),
            ))
            m["garwood_upper_95"] = garwood_upper(m["fp"], m["jam_neg"])
            m["syarat_4x_fp"] = bool(m["jam_neg"] >= 4 * m["fp"]) if m["fp"] else None
            m["alarm_per_shift"] = round((m["far_per_24h"] or 0) / 24 * 8, 3)
            m["det"] = detection_stats(y_te, pred)
            m["gate_A_lulus"] = bool(m["far_per_24h"] is not None and m["far_per_24h"] <= 6
                                     and m["syarat_4x_fp"] is not False)
            a_folds.append(m)
            if seed == seeds[0]:
                m["ci95_auprc"] = block_bootstrap_ci(y_te, s_te, seed=seed)
                m["ci_memuat_prev"] = (m["ci95_auprc"] is not None and
                                       m["ci95_auprc"][0] <= m["prev"] <= m["ci95_auprc"][1])
            a_thr.append(dict(seed=seed, fold=f"LOWO_test_{f['test_well']}", alpha=pilih["alpha"],
                              threshold=pilih["threshold"], fallback=fallback,
                              kandidat=kandidat))
            log(f"A1 seed{seed} {w}: FAR24={m['far_per_24h']:.2f} P={m['precision']} "
                f"R={m['recall']} alpha={pilih['alpha']} auprc={m['auprc']}", runlog)
        # skor per jendela untuk artefak (seed pertama saja, hemat ruang)
        if seed == seeds[0]:
            pass

    json.dump(dict(
        finalis="A1 LightGBM + conformal cross-conformal (CV+)",
        seed_list=seeds, folds=a_folds, titik_operasi=a_thr,
        catatan=("Ambang = kuantil (1-alpha) skor negatif out-of-fold 8 well dalam; "
                 "model uji dilatih pada 8 well dalam penuh. alpha dipilih paling kecil "
                 "yang masih memberi minimal 1 TP di setiap fold dalam (E2 §4.1)."),
    ), open(f"{OUT}/e3_a_conformal_results.json", "w"), indent=2)

    # --- A1b: varian dengan fitur lag label (y_prev, sah dipakai online) ----
    feats_b = feats + ["y_prev_hyd", "valid_prev_hyd"]
    b1_folds = []
    for f in folds:
        w = f["test_well"]; inner = f["train_wells"]
        dtr_all = df[df["well"].isin(inner)]
        dte = df[df["well"] == w].sort_values("ts_bin").reset_index(drop=True)
        oof_s, oof_y, oof_w = [], [], []
        for j in inner:
            tr = dtr_all[dtr_all["well"] != j]
            ca = dtr_all[dtr_all["well"] == j]
            m = fit_lgb(tr[feats_b], tr["y_hyd"].to_numpy(int), 42)
            oof_s.append(m.predict_proba(ca[feats_b])[:, 1])
            oof_y.append(ca["y_hyd"].to_numpy(int))
            oof_w.append(np.array([j] * len(ca)))
        s_oof = np.concatenate(oof_s); y_oof = np.concatenate(oof_y); w_oof = np.concatenate(oof_w)
        m_final = fit_lgb(dtr_all[feats_b], dtr_all["y_hyd"].to_numpy(int), 42)
        s_te = m_final.predict_proba(dte[feats_b])[:, 1]
        y_te = dte["y_hyd"].to_numpy(int)
        pilih = None
        for a in ALPHAS:
            neg = s_oof[y_oof == 0]
            thr = float(np.quantile(neg, 1 - a))
            tp_per = [int(((s_oof[w_oof == j] >= thr) & (y_oof[w_oof == j] == 1)).sum())
                      for j in inner]
            if all(t >= 1 for t in tp_per):
                pilih = dict(alpha=a, threshold=thr, tp_inner=tp_per); break
        if pilih is None:
            pilih = dict(alpha=ALPHAS[-1], threshold=float(np.quantile(s_oof[y_oof == 0],
                                                                      1 - ALPHAS[-1])),
                         tp_inner=[0])
            fallback = True
        else:
            fallback = False
        pred = (s_te >= pilih["threshold"]).astype(int)
        m = op_metrics(y_te, pred)
        m.update(dict(fold=f"LOWO_test_{w}", test_well=w, seed=42, alpha=pilih["alpha"],
                      threshold=round(pilih["threshold"], 6), fallback=fallback,
                      tp_inner=pilih["tp_inner"], n=len(y_te), n_pos=int(y_te.sum()),
                      prev=round(float(y_te.mean()), 6),
                      auprc=round(float(average_precision_score(y_te, s_te)), 4)))
        m["garwood_upper_95"] = garwood_upper(m["fp"], m["jam_neg"])
        m["syarat_4x_fp"] = bool(m["jam_neg"] >= 4 * m["fp"]) if m["fp"] else None
        m["alarm_per_shift"] = round((m["far_per_24h"] or 0) / 24 * 8, 3)
        m["det"] = detection_stats(y_te, pred)
        m["gate_A_lulus"] = bool(m["far_per_24h"] is not None and m["far_per_24h"] <= 6
                                 and m["syarat_4x_fp"] is not False)
        b1_folds.append(m)
        log(f"A1b {w}: FAR24={m['far_per_24h']:.2f} P={m['precision']} R={m['recall']} "
            f"auprc={m['auprc']}", runlog)
    json.dump(dict(finalis="A1b LightGBM + conformal, fitur lag label y_prev diizinkan",
                   seed_list=[42], folds=b1_folds, fitur_tambahan=["y_prev_hyd", "valid_prev_hyd"]),
              open(f"{OUT}/e3_a1b_lag_results.json", "w"), indent=2)

    # --- A2: CUSUM pada residu SPPA ----------------------------------------
    if not args.skip_cusum:
        zmap = {}
        for w in sorted(df["well"].unique()):
            zz = build_z(w)
            if zz is None:
                log(f"A2 z {w}: gagal dibangun", runlog)
            else:
                zmap[w] = zz
                log(f"A2 z {w}: n={len(zz)}", runlog)

        def alarm_for_well(well, h, d, reset=True):
            """Alarm per baris dataset (strict past: menit < lab_ts)."""
            zz = zmap.get(well)
            if zz is None:
                return np.zeros(len(d), dtype=int)
            al = cusum_alarms(zz["z"].to_numpy(), h, reset=reset)
            ts = zz["ts_bin"].to_numpy()
            lab = d["lab_ts"].to_numpy()
            out = np.zeros(len(d), dtype=int)
            for i, t0 in enumerate(lab):
                lo = np.searchsorted(ts, t0 - W, side="left")
                hi = np.searchsorted(ts, t0, side="left")   # eksklusif: menit < t0
                if hi > lo:
                    out[i] = int(al[lo:hi].max())
            return out

        well_df = {w: df[df["well"] == w].sort_values("ts_bin").reset_index(drop=True)
                   for w in df["well"].unique()}
        acache = {}

        def alarm_cached(well, h, reset=True):
            key = (well, h, reset)
            if key not in acache:
                acache[key] = alarm_for_well(well, h, well_df[well], reset=reset)
            return acache[key]

        b_all = {}
        for reset in (True, False):
          b_folds, b_thr = [], []
          for f in folds:
            w = f["test_well"]; inner = f["train_wells"]
            dte = well_df[w]
            y_te = dte["y_hyd"].to_numpy(int)
            # kalibrasi: h paling konservatif (terbesar) yang FAR<=6 dan >=1 TP di tiap fold dalam
            pilih, kandidat = None, []
            for h in H_GRID:
                per = []
                for j in inner:
                    dj = well_df[j]
                    aj = alarm_cached(j, h, reset)
                    mm = op_metrics(dj["y_hyd"].to_numpy(int), aj)
                    per.append(dict(well=j, far=mm["far_per_24h"], tp=mm["tp"], fp=mm["fp"]))
                ok = all((p["far"] is not None and p["far"] <= 6 and p["tp"] >= 1) for p in per)
                kandidat.append(dict(h=h, per_fold=per, ok=ok))
                if ok:
                    pilih = dict(h=h, per_fold=per)
            fallback = pilih is None
            if fallback:
                best = max(kandidat, key=lambda r: (sum(1 for p in r["per_fold"]
                                                        if p["far"] is not None and p["far"] <= 6),
                                                    r["h"]))
                pilih = dict(h=best["h"], per_fold=best["per_fold"])
            pred = alarm_cached(w, pilih["h"], reset)
            m = op_metrics(y_te, pred)
            m.update(dict(fold=f"LOWO_test_{f['test_well']}", test_well=w, h=pilih["h"], fallback=fallback,
                          reset=reset, n=len(y_te), n_pos=int(y_te.sum()),
                          prev=round(float(y_te.mean()), 6), auprc=None))
            m["garwood_upper_95"] = garwood_upper(m["fp"], m["jam_neg"])
            m["syarat_4x_fp"] = bool(m["jam_neg"] >= 4 * m["fp"]) if m["fp"] else None
            m["alarm_per_shift"] = round((m["far_per_24h"] or 0) / 24 * 8, 3)
            m["det"] = detection_stats(y_te, pred)
            m["gate_A_lulus"] = bool(m["far_per_24h"] is not None and m["far_per_24h"] <= 6
                                     and m["syarat_4x_fp"] is not False)
            b_folds.append(m)
            b_thr.append(dict(fold=f"LOWO_test_{f['test_well']}", h=pilih["h"], fallback=fallback,
                              kandidat_ok=[k["h"] for k in kandidat if k["ok"]]))
            log(f"A2 reset={reset} {w}: h={pilih['h']} FAR24={m['far_per_24h']:.2f} "
                f"P={m['precision']} R={m['recall']}", runlog)
          b_all["reset" if reset else "tanpa_reset"] = dict(folds=b_folds, titik_operasi=b_thr)

        json.dump(dict(
            finalis="A2 CUSUM dua sisi pada residu SPPA terstandar",
            k=CUSUM_K, h_grid=H_GRID, varian=b_all,
            catatan=("z dibangun per well dengan resep label (qcut TFLO 10, median/MAD per bin). "
                     "Alarm jendela = ada alarm CUSUM pada menit [lab_ts-W, lab_ts). "
                     "SIRKULAR: statistik z adalah pembentuk label, jadi A2 bersaing dengan rule, "
                     "bukan pengganti independen."),
        ), open(f"{OUT}/e3_b_cusum_results.json", "w"), indent=2)

    # --- cakupan waktu ------------------------------------------------------
    cak = []
    for f in folds:
        d = df[df["well"] == f["test_well"]]
        menit_kal = float(d["ts_bin"].max() - d["ts_bin"].min() + 1)
        cak.append(dict(fold=f"LOWO_test_{f['test_well']}", test_well=f["test_well"], n_jendela=len(d),
                        menit_teramati=float(len(d)), menit_kalender=menit_kal,
                        fraksi=round(len(d) / menit_kal, 4) if menit_kal else None,
                        well_start=int(d["ts_bin"].min()), well_end=int(d["ts_bin"].max())))
    json.dump(dict(deskripsi="Cakupan = jumlah jendela teramati / rentang menit kalender well.",
                   per_fold=cak), open(f"{OUT}/e3_cakupan.json", "w"), indent=2)

    # --- tabel berpasangan --------------------------------------------------
    pair = []
    base_p = {(r["test_well"]): r for r in base_rows if r["model"] == "persistence"}
    base_h = {(r["test_well"]): r for r in base_rows if r["model"] == "hybrid_rule_lag1_and_persistence"}
    for r in a_folds:
        if r["seed"] != seeds[0]:
            continue
        for nm, b in (("vs_persistence", base_p[r["test_well"]]),
                      ("vs_hybrid", base_h[r["test_well"]])):
            pair.append(dict(fold=r["fold"], model="A1", seed=r["seed"], pembanding=nm,
                             tp=r["tp"], fp=r["fp"], base_tp=b["tp"], base_fp=b["fp"],
                             delta_fp=r["fp"] - b["fp"],
                             far24=r["far_per_24h"], base_far24=b["far_per_24h"],
                             recall=r["recall"], base_recall=b["recall"]))
    pd.DataFrame(pair).to_csv(f"{OUT}/e3_pairing.csv", index=False)

    summ = dict(
        seeds=seeds, n_folds=len(folds),
        elapsed_s=round(time.time() - t_start, 1),
        fold_gate_A_A1_seed42=sum(1 for r in a_folds if r["seed"] == seeds[0] and r["gate_A_lulus"]),
        fold_gate_A_A1_all_seeds={str(s): sum(1 for r in a_folds if r["seed"] == s and r["gate_A_lulus"])
                                  for s in seeds},
        n_alphas_fallback={str(s): sum(1 for r in a_thr if r["seed"] == s and r["fallback"]) for s in seeds},
        log=runlog,
    )
    json.dump(summ, open(f"{OUT}/e3_run_summary.json", "w"), indent=2)
    log(f"SELESAI {summ['elapsed_s']}s gateA_A1(seed42)={summ['fold_gate_A_A1_seed42']}/9", runlog)


if __name__ == "__main__":
    main()
