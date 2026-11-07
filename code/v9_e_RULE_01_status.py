#!/usr/bin/env python3
"""V9-E_RULE 01 — baseline S9 + rule + hibrida D-A3 untuk 5 kelas STATUS rig.

Kelas: vib, ssi, shk, stuck_k1, hyd_ki  (dataset D1 scratch/v9_d1/datasets/*.csv.gz,
fold LOWO identik dari scratch/v9_d1/lowo_<engine>.json — S9: fold IDENTIK dgn
engine utama, dihitung deterministik sebelum melihat hasil engine lain).

Baseline per fold (S9):
  1. persistence       = kolom y_prev_<cls> (resep D1, jendela [t0-10,t0)).
                         Dihitung pada (a) semua baris test, (b) subset
                         valid_prev=1 (konvensi V8 claim1) — keduanya dicetak.
  2. prevalence-random = skor acak default_rng(42) per fold + prev analitik;
                         plafon lift = 1/prev.
  3. canary-depth      = RF kontrak (300, leaf5, balanced_subsample, seed42)
                         HANYA fitur depth_*+dbtm_* (10), imputer median
                         fold-safe. Baseline AUPRC (kontrol memorisasi posisi).
Rule (PM1 §4.5 — dijalankan pada data nyata, FP tercetak):
  - display/kanal per kelas pada menit t0-1 (STRICT PAST, konsisten invariant
    anti-bocor S5: bin t0 bagian jendela label -> membaca bin t0 = membaca label).
  - stuck_k1: E1 2-dari-3 (z TQA>2, z HKLD>2, ROP-drop>=30%, z vs median+MAD
    jendela 60 menit strict-past dari bins) — detektor independen asli.
Cek identitas sirkular (rule pada jendela LABEL [t0,t0+10) vs y) = recompute
independen dari bins; dilaporkan sbg sifat konstruksi BUKAN skor kemenangan.
Hibrida D-A3: h(t) = rule(t0-1) AND persistence(t)  [konfirmasi-status].

Metrik per fold: n/pos/prev/underpowered, AUPRC, lift (=AUPRC/prev), plafon
1/prev, P/R/TP/FP/FN/TN, FAR_24h = FP/(n_neg/60)*24 (konvensi V8 claim1_eval).
SEMUA angka dari eksekusi; seed 42; output JSON primer di scratch DULU (S6).
"""
import json
import os
import time
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import average_precision_score

SEED = 42
np.random.seed(SEED)

BASE = "/mnt/d/Capstone 1(v2)"
DS = f"{BASE}/scratch/v9_d1/datasets"
BINS = f"{BASE}/scratch/v9_d1/bins"
LOWO = f"{BASE}/scratch/v9_d1"
OUT = f"{BASE}/scratch/v9_e_rule"
os.makedirs(OUT, exist_ok=True)

VIB_THRESH = 32.17405
SSI_MIN_SAMPLES = 10
W = 10
E1_WIN = 60          # menit jendela median/MAD stuck-E1
E1_MIN_OBS = 10      # min observasi agar z terdefinisi
Z_SCALE = 0.6745     # MAD -> skala normal (NIST, R1 [7][8])
ROP_DROP = 0.30      # ROP-drop >= 30%

CLS = {
    "vib":     dict(y="y_vib",      prev="y_prev_vib",      rp="vib"),
    "ssi":     dict(y="y_ssi",      prev="y_prev_ssi",      rp="ssi"),
    "shk":     dict(y="y_shk",      prev="y_prev_shk",      rp="shk"),
    "stuck_k1": dict(y="y_stuck",   prev="y_prev_stuck",    rp="stuck"),
    "hyd_ki":  dict(y="y_hyd",      prev="y_prev_hyd",      rp="hyd"),
}
META = ["well", "ts_bin", "feat_ts_max", "lab_ts", "lab_kind"]

log_lines = []


def log(m):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {m}"
    print(line, flush=True)
    log_lines.append(line)


# ---------------- metrik ----------------
def auprc(y, s):
    if len(y) == 0 or y.sum() == 0:
        return None
    return float(average_precision_score(y, s))


def binary_metrics(y, pred):
    y = np.asarray(y).astype(int)
    pred = np.asarray(pred).astype(int)
    tp = int(((pred == 1) & (y == 1)).sum())
    fp = int(((pred == 1) & (y == 0)).sum())
    fn = int(((pred == 0) & (y == 1)).sum())
    tn = int(((pred == 0) & (y == 0)).sum())
    n_neg = fp + tn
    jam_neg = n_neg / 60.0
    P = tp / (tp + fp) if (tp + fp) else None
    R = tp / (tp + fn) if (tp + fn) else None
    far = (fp / jam_neg * 24.0) if jam_neg else None
    return dict(tp=tp, fp=fp, fn=fn, tn=tn, precision=P, recall=R,
                n_neg=n_neg, far_24h=far)


def fold_stats(y):
    y = np.asarray(y).astype(int)
    n, pos = int(len(y)), int(y.sum())
    prev = (pos / n) if n else None
    return n, pos, prev, bool(pos < 30)


def detector_block(y, pred, score=None):
    b = binary_metrics(y, pred)
    a = auprc(y, pred)           # AUPRC detektor biner = P/R tradeoff pada skor biner
    prev = float(np.mean(y)) if len(y) else None
    b["auprc"] = a
    b["lift"] = (a / prev) if (a is not None and prev) else None
    b["plafon_1_over_prev"] = (1.0 / prev) if prev else None
    return b


def prevalence_block(y, rng_seed=SEED):
    y = np.asarray(y).astype(int)
    n, pos, prev, _ = fold_stats(y)
    if n == 0 or pos == 0 or pos == n:
        return dict(auprc_emp=None, prev_analytic=prev, plafon=None)
    rng = np.random.default_rng(rng_seed)
    s = rng.uniform(0, 1, n)
    return dict(auprc_emp=float(average_precision_score(y, s)),
                prev_analytic=prev, plafon=1.0 / prev)


def canary_depth(train_df, test_df, feat_cols, ycol):
    """RF kontrak seragam, HANYA fitur depth/dbtm. Imputer fold-safe."""
    Xtr = train_df[feat_cols]
    Xte = test_df[feat_cols]
    ytr = train_df[ycol].to_numpy().astype(int)
    yte = test_df[ycol].to_numpy().astype(int)
    if len(np.unique(ytr)) < 2:
        return dict(auprc=None, lift=None, plafon=None,
                    note="train hanya 1 kelas — RF tak terdefinisi")
    imp = SimpleImputer(strategy="median")
    Xtr_i = imp.fit_transform(Xtr)
    Xte_i = imp.transform(Xte)
    rf = RandomForestClassifier(n_estimators=300, min_samples_leaf=5,
                                class_weight="balanced_subsample",
                                random_state=SEED, n_jobs=-1)
    rf.fit(Xtr_i, ytr)
    s = rf.predict_proba(Xte_i)[:, 1]
    a = auprc(yte, s)
    prev = float(np.mean(yte)) if len(yte) else None
    return dict(auprc=a, lift=(a / prev) if (a is not None and prev) else None,
                plafon=(1.0 / prev) if prev else None)


# ---------------- bins: aturan t0-1 + cek identitas ----------------
_bins_cache = {}


def get_bins(well):
    if well not in _bins_cache:
        b = pd.read_csv(f"{BINS}/{well}.csv.gz")
        b["ts_bin"] = b["ts_bin"].astype("int64")
        b = b.sort_values("ts_bin").set_index("ts_bin")
        _bins_cache[well] = b
    return _bins_cache[well]


def rule_display(cls, df):
    """Rule per kanal pada menit t0-1 (strict past). Returns (pred, n_nodata)."""
    ts = df["ts_bin"].to_numpy().astype("int64")
    wells = df["well"].to_numpy()
    pred = np.zeros(len(df), np.int8)
    nodata = np.zeros(len(df), bool)
    if cls == "hyd_ki":
        # anom per-menit: kalibrasi qcut(TFLO,10)+median/MAD per well = resep label V6-31
        for w in np.unique(wells):
            m = wells == w
            b = get_bins(w)
            anom = hyd_bin_anom(b)
            key = pd.Index(ts[m] - 1)
            vals = anom.reindex(key)
            pred[m] = (vals.fillna(-1).to_numpy() > 0).astype(np.int8)
            nodata[m] = vals.isna().to_numpy()
        return pred, nodata
    rp = CLS[cls]["rp"]
    colmap = {"vib": ("vib_max", VIB_THRESH), "shk": ("shk_max", 1.0),
              "stuck": ("stuck_max", 1.0)}
    for w in np.unique(wells):
        m = wells == w
        b = get_bins(w)
        key = pd.Index(ts[m] - 1)
        if rp in colmap:
            col, thr = colmap[rp]
            if col in b.columns:
                v = b[col].reindex(key)
                pred[m] = (v.fillna(-np.inf).to_numpy() >= thr).astype(np.int8)
                nodata[m] = v.isna().to_numpy()
            else:
                nodata[m] = True
        elif rp == "ssi":
            need = ["crpm_min", "crpm_max", "crpm_mean", "crpm_n"]
            if all(c in b.columns for c in need):
                mn = b["crpm_min"].reindex(key)
                mx = b["crpm_max"].reindex(key)
                me = b["crpm_mean"].reindex(key)
                nn = b["crpm_n"].reindex(key)
                ok = (nn.fillna(0) >= SSI_MIN_SAMPLES) & (me.fillna(0) > 0)
                ssi = (mx - mn) / (2.0 * me.where(me > 0))
                pred[m] = np.where(ok, (ssi >= 1.0), False).astype(np.int8)
                nodata[m] = (~ok).to_numpy()
            else:
                nodata[m] = True
    return pred, nodata


def hyd_bin_anom(b):
    """Label anom per menit (resep V9_D1_03 hyd_bin_labels — identik)."""
    d = b.dropna(subset=["SPPA_mean", "TFLO_mean"]).copy()
    d = d[d["TFLO_mean"] > 0]
    anom = pd.Series(0, index=b.index, dtype=np.int8)
    if len(d) >= 50:
        try:
            d["qbin"] = pd.qcut(d["TFLO_mean"], 10, labels=False,
                                duplicates="drop")
        except ValueError:
            d["qbin"] = 0
        med = d.groupby("qbin")["SPPA_mean"].transform("median")
        mad = d.groupby("qbin")["SPPA_mean"].transform(
            lambda s: (s - s.median()).abs().median())
        z = (d["SPPA_mean"] - med) / (1.4826 * mad.replace(0, np.nan))
        anom.loc[d.index] = (z.abs() > 2).fillna(False).astype(np.int8)
    return anom


def rule_window_identity(cls, df):
    """Recompute rule pada jendela LABEL [t0,t0+10) dari bins; bandingkan dgn y.

    Untuk kelas definisi-kanal hasilnya diharap identik (sirkular-per-konstruksi).
    """
    ycol = CLS[cls]["y"]
    y = df[ycol].to_numpy().astype(int)
    ts = df["ts_bin"].to_numpy().astype("int64")
    wells = df["well"].to_numpy()
    pred = np.zeros(len(df), np.int8)
    for w in np.unique(wells):
        m = wells == w
        b = get_bins(w)
        if cls == "ssi":
            # SSI jendela 10 menit, min 10 sampel total (resep v9_d1_02.build)
            keys = (ts[m][:, None] + np.arange(W)[None, :]).ravel()
            idx = pd.Index(b.index)
            def col(c):
                return b[c].reindex(pd.Index(keys)).to_numpy(np.float64)
            Cn = np.nan_to_num(col("crpm_n"), nan=0.0).reshape(-1, W)
            Cmean = col("crpm_mean").reshape(-1, W)
            Cmin = col("crpm_min").reshape(-1, W)
            Cmax = col("crpm_max").reshape(-1, W)
            n_tot = Cn.sum(axis=1)
            num = np.where(Cn > 0, np.nan_to_num(Cmean, nan=0.0) * Cn, 0.0).sum(axis=1)
            wmean = num / np.where(n_tot > 0, n_tot, np.nan)
            wmin = np.where(np.isnan(Cmin) | (Cn == 0), np.inf, Cmin).min(axis=1)
            wmax = np.where(np.isnan(Cmax) | (Cn == 0), -np.inf, Cmax).max(axis=1)
            with np.errstate(invalid="ignore", divide="ignore"):
                ssi = (wmax - wmin) / (2.0 * wmean)
            ok = (n_tot >= SSI_MIN_SAMPLES) & (wmean > 0) & np.isfinite(ssi)
            pred[m] = (ok & (ssi >= 1.0)).astype(np.int8)
        elif cls == "hyd_ki":
            # valid & anom/obs >= 0.5 dgn MIN_OBS=5 (resep v9_d1_03)
            obs_c = b["SPPA_mean"].notna() & b["TFLO_mean"].notna()
            anom = hyd_bin_anom(b)
            keys = (ts[m][:, None] + np.arange(W)[None, :]).ravel()
            o = obs_c.reindex(pd.Index(keys)).fillna(False).to_numpy().reshape(-1, W)
            a = anom.reindex(pd.Index(keys)).fillna(0).to_numpy().reshape(-1, W)
            n_obs = o.sum(axis=1)
            n_anom = (o & (a > 0)).sum(axis=1)
            valid = n_obs >= 5
            pred[m] = (valid & (n_anom / np.maximum(n_obs, 1) >= 0.5)).astype(np.int8)
        else:
            col, thr = {"vib": ("vib_max", VIB_THRESH),
                        "shk": ("shk_max", 1.0),
                        "stuck": ("stuck_max", 1.0)}[CLS[cls]["rp"]]
            if col not in b.columns:
                pred[m] = -1  # kanal absen — tandai tak-terhitung
                continue
            keys = (ts[m][:, None] + np.arange(W)[None, :]).ravel()
            v = b[col].reindex(pd.Index(keys)).to_numpy(np.float64).reshape(-1, W)
            n = (b[f'{col.replace("_max","")}_n'].reindex(pd.Index(keys))
                 .to_numpy(np.float64).reshape(-1, W)
                 if f'{col.replace("_max","")}_n' in b.columns
                 else np.ones_like(v))
            n = np.nan_to_num(n, nan=0.0)
            valid = n.sum(axis=1) >= 1
            mx = np.where(np.isnan(v) | (n == 0), -np.inf, v).max(axis=1)
            pred[m] = (valid & (mx >= thr)).astype(np.int8)
    scorable = pred >= 0
    mismatch = int((pred[scorable] != y[scorable]).sum()) if scorable.any() else None
    return dict(n_checked=int(scorable.sum()), n_mismatch=mismatch,
                identity=(mismatch == 0) if mismatch is not None else None,
                note="rule jendela LABEL = pembentuk label (sirkular per konstruksi)")


# ---------------- stuck-E1 (2-dari-3) ----------------
_e1_cache = {}


def e1_alarm_series(well):
    """Alarm E1 per menit m: z(m) vs median+MAD [m-60, m] strict-past<=m.

    z = 0.6745*(x-median)/MAD; syarat: z(TQA)>2, z(HKLD)>2, ROP-drop>=30%
    (ROP <= 0.7*median60). Alarm butuh >=E1_MIN_OBS observasi per kanal.
    """
    if well in _e1_cache:
        return _e1_cache[well]
    b = get_bins(well)
    out = pd.Series(0, index=b.index, dtype=np.int8)
    if not all(c in b.columns for c in ("TQA_mean", "HKLD_mean", "ROP_mean")):
        _e1_cache[well] = out
        return out
    df = b[["TQA_mean", "HKLD_mean", "ROP_mean"]].sort_index().copy()
    roll = df.rolling(E1_WIN, min_periods=E1_MIN_OBS)
    med = roll.median()
    mad = roll.apply(lambda x: np.median(np.abs(x - np.median(x))),
                     raw=True)
    with np.errstate(invalid="ignore", divide="ignore"):
        zt = Z_SCALE * (df["TQA_mean"] - med["TQA_mean"]) / mad["TQA_mean"]
        zh = Z_SCALE * (df["HKLD_mean"] - med["HKLD_mean"]) / mad["HKLD_mean"]
        medr = med["ROP_mean"]
        drop = (medr - df["ROP_mean"]) / medr
    # guard MAD==0: sinyal datar -> z tak-terdefinisi -> perlakukan TIDAK-anomali
    # (konservatif; dicatat di dokumen agar FAR tidak meledak oleh 0/0)
    zt = zt.where(mad["TQA_mean"] > 0, 0.0)
    zh = zh.where(mad["HKLD_mean"] > 0, 0.0)
    cond = ((zt > 2).astype(np.int8) + (zh > 2).astype(np.int8) +
            ((drop >= ROP_DROP) & (medr > 0)).astype(np.int8))
    out = (cond >= 2).astype(np.int8)
    # MAD==0 -> z NaN/inf: jadikan 0 (tak-terukur, konservatif) kecuali drop terpenuhi
    out = out.astype(np.int8)
    _e1_cache[well] = out
    return out


def rule_e1(df):
    ts = df["ts_bin"].to_numpy().astype("int64")
    wells = df["well"].to_numpy()
    pred = np.zeros(len(df), np.int8)
    nodata = np.zeros(len(df), bool)
    for w in np.unique(wells):
        m = wells == w
        s = e1_alarm_series(w)
        v = s.reindex(pd.Index(ts[m] - 1))
        pred[m] = v.fillna(0).to_numpy().astype(np.int8)
        nodata[m] = v.isna().to_numpy()
    return pred, nodata


# ---------------- driver ----------------
def main():
    t0 = time.time()
    results = {"meta": {
        "task": "V9-E_RULE 01 status baselines",
        "seed": SEED,
        "far_convention": "FAR_24h = FP / (n_neg/60) * 24  (konvensi V8 claim1_eval)",
        "persistence_recipe": "D1 y_prev_* (jendela [t0-10,t0)); subset valid_prev dicetak terpisah",
        "rule_time_basis": "menit t0-1 strict-past (invariant S5)",
        "canary": "RF 300/leaf5/balanced_subsample/seed42, fitur depth_*+dbtm_* saja",
        "prevalence_random": "default_rng(42).uniform per fold; plafon = 1/prev",
        "underpowered": "positif < 30 per fold",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }, "classes": {}}

    for cls, cfg in CLS.items():
        path = f"{DS}/{cls}.csv.gz"
        df = pd.read_csv(path)
        ycol, pcol = cfg["y"], cfg["prev"]
        lowo = json.load(open(f"{LOWO}/lowo_{cls}.json"))
        feat_cols = [c for c in df.columns if c not in META
                     and not c.startswith(("y_", "valid_", "obs_", "anom_"))]
        depth_cols = [c for c in feat_cols
                      if c.startswith("depth_") or c.startswith("dbtm_")]
        log(f"== {cls}: rows={len(df)} folds={lowo['n_folds']} "
            f"feats={len(feat_cols)} depth_feats={len(depth_cols)}")

        # cek identitas sirkular (recompute dari bins) — SEKALI per kelas
        ident = rule_window_identity(cls, df)

        # rule display t0-1 + E1 (stuck_k1)
        r_pred, r_nodata = rule_display(cls, df)
        extra = {}
        if cls == "stuck_k1":
            e1_pred, e1_nodata = rule_e1(df)
            extra["e1"] = (e1_pred, e1_nodata)

        cls_out = {"identity_rule_window_vs_label": ident, "folds": []}
        for i, fold in enumerate(lowo["folds"]):
            te = fold["test_well"]
            tr_wells = fold["train_wells"]
            mte = df["well"] == te
            mtr = df["well"].isin(tr_wells)
            test_df = df[mte].reset_index(drop=True)
            train_df = df[mtr].reset_index(drop=True)
            y = test_df[ycol].to_numpy().astype(int)
            n, pos, prev, underp = fold_stats(y)
            fb = {"fold": i, "test_well": te, "n": n, "pos": pos,
                  "prev": prev, "underpowered": underp}

            # 1. persistence
            yp = test_df[pcol].to_numpy().astype(int)
            vp = test_df[f"valid_prev_{cfg['rp']}"].to_numpy().astype(int) \
                if f"valid_prev_{cfg['rp']}" in test_df.columns else None
            fb["persistence"] = detector_block(y, yp)
            fb["persistence"]["auprc_validprev"] = (
                auprc(y[vp == 1], yp[vp == 1]) if vp is not None and (vp == 1).any()
                else None)
            fb["persistence"]["n_validprev"] = int((vp == 1).sum()) if vp is not None else None

            # 2. prevalence-random
            fb["prevalence_random"] = prevalence_block(y)

            # 3. canary-depth
            fb["canary_depth"] = canary_depth(train_df, test_df, depth_cols, ycol)

            # 4. rule display t0-1
            rp = r_pred[mte.to_numpy()]
            fb["rule_display_t0minus1"] = detector_block(y, rp)
            fb["rule_display_t0minus1"]["n_nodata"] = int(
                r_nodata[mte.to_numpy()].sum())

            # 4b. E1 (stuck_k1)
            if cls == "stuck_k1":
                ep = extra["e1"][0][mte.to_numpy()]
                fb["rule_E1_2of3"] = detector_block(y, ep)
                fb["rule_E1_2of3"]["n_nodata"] = int(
                    extra["e1"][1][mte.to_numpy()].sum())

            # 5. hibrida D-A3: rule AND persistence (konfirmasi-status)
            fb["hybrid_rule_and_persistence"] = detector_block(
                y, ((rp == 1) & (yp == 1)).astype(np.int8))
            if cls == "stuck_k1":
                ep = extra["e1"][0][mte.to_numpy()]
                fb["hybrid_E1_and_persistence"] = detector_block(
                    y, ((ep == 1) & (yp == 1)).astype(np.int8))

            cls_out["folds"].append(fb)
            log(f"   {te}: n={n} pos={pos} prev={None if prev is None else round(prev,4)} "
                f"pers.auprc={_r(fb['persistence']['auprc'])} "
                f"rule.FP={fb['rule_display_t0minus1']['fp']} "
                f"rule.P={_r(fb['rule_display_t0minus1']['precision'])} "
                f"hybrid.FP={fb['hybrid_rule_and_persistence']['fp']} "
                f"canary={_r(fb['canary_depth']['auprc'])}")

        # agregat fold
        cls_out["aggregate"] = aggregate(cls_out["folds"])
        results["classes"][cls] = cls_out

    outp = f"{OUT}/v9_e_RULE_01_status_results.json"
    json.dump(results, open(outp, "w"), indent=1, allow_nan=False)
    open(f"{OUT}/v9_e_RULE_01_run_log.txt", "w").write("\n".join(log_lines) + "\n")
    log(f"-> {outp} ({round(time.time() - t0, 1)} s)")


def _r(x, nd=4):
    return None if x is None else round(float(x), nd)


def aggregate(folds):
    keys = ["persistence", "rule_display_t0minus1",
            "hybrid_rule_and_persistence", "canary_depth",
            "prevalence_random", "rule_E1_2of3", "hybrid_E1_and_persistence"]
    agg = {}
    for k in keys:
        vals = [f[k]["auprc"] for f in folds if k in f and f[k].get("auprc") is not None]
        if vals:
            agg[k] = dict(auprc_mean=float(np.mean(vals)),
                          auprc_median=float(np.median(vals)),
                          n_folds_scorable=len(vals))
        pref = [f[k].get("auprc_emp") for f in folds
                if k in f and f[k].get("auprc_emp") is not None]
        if pref:
            agg[k] = agg.get(k, {})
            agg[k]["auprc_emp_mean"] = float(np.mean(pref))
    # jumlah FP rule lintas fold (B3)
    fps = [f["rule_display_t0minus1"]["fp"] for f in folds]
    agg["rule_display_total_fp"] = int(sum(fps))
    return agg


if __name__ == "__main__":
    main()
