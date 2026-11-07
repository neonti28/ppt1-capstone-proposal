#!/usr/bin/env python3
"""RND-R8 -- uji hybrid nyata per tugas (kebijakan A/B/C, RND_EVALUATION_POLICY.md).

Empat tugas, satu skrip, satu perintah per tugas:
  hyd      Lapisan A hyd K-i   : stat (CUSUM z SPPA) + rule kanal (anom t-1)
  shk      Lapisan A shk K-i   : ML LightGBM + stat CUSUM residu
  toolwear Lapisan A tool_wear : ML logistik + metaheuristik GWO (ambang dan C)
  stuck    Lapisan A stuck K-ii: rule + stat + ML tiga komponen (onset)

Aturan yang dipegang:
  - LOWO per well / per tool dari scratch/v9_d1/lowo_*.json
  - kolom turunan label, ts_bin, feat_ts_max, lab_ts, lab_kind TIDAK menjadi fitur
  - ambang dipilih DI DALAM fold (satu well kalibrasi dari daftar train_wells),
    bukan dari well uji
  - FAR dilaporkan pada satuan kalender (fp / menit_neg_kalender * 1440)
  - setiap angka disimpan ke JSON supaya bisa di-assert skrip ledger

Keluaran: /mnt/d/Capstone 1(v2)/scratch/rnd/r8/
"""
import argparse, json, os, time, warnings
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, average_precision_score

warnings.filterwarnings("ignore")
BASE = "/mnt/d/Capstone 1(v2)"
DSD = f"{BASE}/scratch/v9_d1/datasets"
BINSD = f"{BASE}/scratch/v9_d1/bins"
LOWOD = f"{BASE}/scratch/v9_d1"
OUT = f"{BASE}/scratch/rnd/r8"
os.makedirs(OUT, exist_ok=True)

SEED = 42
ALPHA_BUDGET = 6.0 / 1440.0   # FAR 6 per 24 jam kalender, dalam fraksi menit negatif
LEAD_HORIZON = 60             # menit, jendela "peringatan sebelum memburuk"
LABEL_COLS = ("y_", "valid_prev_", "obs_", "anom_", "lab_")
META_COLS = ("well", "ts_bin", "feat_ts_max", "lab_ts", "lab_kind", "tool", "run",
             "file", "start_sample")


def log(msg, store=None):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    if store is not None:
        store.append(line)


# --------------------------------------------------------------- metrik
def rows_metrics(y, pred):
    y = np.asarray(y).astype(int); pred = np.asarray(pred).astype(int)
    tp = int(((pred == 1) & (y == 1)).sum()); fp = int(((pred == 1) & (y == 0)).sum())
    fn = int(((pred == 0) & (y == 1)).sum()); tn = int(((pred == 0) & (y == 0)).sum())
    return dict(tp=tp, fp=fp, fn=fn, tn=tn,
                precision=(tp / (tp + fp)) if (tp + fp) else None,
                recall=(tp / (tp + fn)) if (tp + fn) else None,
                menit_alarm=int(pred.sum()), n_pos=int(y.sum()), n_neg=int((y == 0).sum()))


def event_metrics(y, pred):
    y = np.asarray(y).astype(int); pred = np.asarray(pred).astype(int)
    runs, i, n = [], 0, len(pred)
    while i < n:
        if pred[i] == 1:
            j = i
            while j < n and pred[j] == 1:
                j += 1
            runs.append((i, j)); i = j
        else:
            i += 1
    tp_ev = sum(1 for a, b in runs if y[a:b].sum() > 0)
    fp_ev = sum(1 for a, b in runs if y[a:b].sum() == 0)
    return dict(tp_kejadian=int(tp_ev), fp_kejadian=int(fp_ev), n_kejadian=len(runs))


def lengkap(y, pred, ts):
    r = rows_metrics(y, pred); ev = event_metrics(y, pred)
    menit_kal = float(ts.max() - ts.min() + 1)
    menit_neg_kal = max(menit_kal - r["n_pos"], 1.0)
    return dict(rows=r, events=ev,
                cakupan=round(len(ts) / menit_kal, 4) if menit_kal else None,
                menit_kalender=menit_kal,
                far24_kalender=round(r["fp"] / (menit_neg_kal / 1440.0), 4),
                far24_kalender_kejadian=round(ev["fp_kejadian"] / (menit_neg_kal / 1440.0), 4),
                garwood_atas_fp=garwood(r["fp"], menit_neg_kal))


def garwood(k, menit_neg_kal, alpha=0.95):
    from scipy.stats import chi2
    hi = chi2.ppf(1 - (1 - alpha) / 2, 2 * (k + 1)) / 2.0
    return round(hi / (menit_neg_kal / 1440.0), 4)


def lead_time(y, alarm, horizon=LEAD_HORIZON):
    """Untuk setiap onset (0->1), cari alarm terakhir dalam [onset-horizon, onset)."""
    y = np.asarray(y).astype(int); alarm = np.asarray(alarm).astype(int)
    onset_idx = np.flatnonzero((y[1:] == 1) & (y[:-1] == 0)) + 1
    if len(y) and y[0] == 1:
        onset_idx = np.concatenate([[0], onset_idx])
    leads, warned = [], 0
    for o in onset_idx:
        lo = max(0, o - horizon)
        seg = np.flatnonzero(alarm[lo:o])
        if len(seg):
            warned += 1
            leads.append(int(o - (lo + seg[-1])))
    return dict(n_onset=int(len(onset_idx)), n_diperingatkan=int(warned),
                lead_median_min=float(np.median(leads)) if leads else None,
                lead_min_min=int(min(leads)) if leads else None,
                lead_maks_min=int(max(leads)) if leads else None)


def separuh(ts, y, pred):
    """Lapisan C: kestabilan dalam dua paruh waktu well yang sama."""
    med = float(np.median(ts)); out = {}
    for nama, m in (("awal", ts <= med), ("akhir", ts > med)):
        if m.sum() == 0:
            continue
        r = rows_metrics(y[m], pred[m])
        out[nama] = dict(precision=r["precision"], recall=r["recall"],
                         fp=r["fp"], n_pos=r["n_pos"])
    return out


# ------------------------------------------------------- komponen statistik
def zresid(well, chan="SPPA", flow="TFLO"):
    """z residual kanal per bin aliran (resep label), per well. Tanpa label."""
    b = pd.read_csv(f"{BINSD}/{well}.csv.gz")
    d = b.dropna(subset=[f"{chan}_mean", f"{flow}_mean"]).copy()
    d = d[d[f"{flow}_mean"] > 0]
    if len(d) < 50:
        return None
    try:
        d["qbin"] = pd.qcut(d[f"{flow}_mean"], 10, labels=False, duplicates="drop")
    except ValueError:
        d["qbin"] = 0
    med = d.groupby("qbin")[f"{chan}_mean"].transform("median")
    mad = d.groupby("qbin")[f"{chan}_mean"].transform(lambda s: (s - s.median()).abs().median())
    d["z"] = (d[f"{chan}_mean"] - med) / (1.4826 * mad.replace(0, np.nan))
    d = d.dropna(subset=["z"]).sort_values("ts_bin")
    return d[["ts_bin", "z"]].reset_index(drop=True)


def cusum(z, h, k=0.5, reset=True):
    z = np.asarray(z, float); n = len(z)
    cp = np.zeros(n); cn = np.zeros(n); a = np.zeros(n, int)
    for i, v in enumerate(z):
        pp = cp[i - 1] if i else 0.0; pn = cn[i - 1] if i else 0.0
        cp[i] = max(0.0, pp + (v - k)); cn[i] = max(0.0, pn + (-v - k))
        if cp[i] > h or cn[i] > h:
            a[i] = 1
            if reset:
                cp[i] = 0.0; cn[i] = 0.0
    return a


def z_on_ts(well, ts, chan="SPPA"):
    """Selaraskan z ke grid ts_bin dataset (join kiri pada ts_bin)."""
    z = zresid(well, chan=chan)
    if z is None:
        return np.zeros(len(ts)), np.zeros(len(ts), bool)
    m = pd.Series(z["z"].to_numpy(), index=z["ts_bin"].to_numpy()).reindex(ts)
    return np.nan_to_num(m.to_numpy(dtype=float), nan=0.0), m.notna().to_numpy()


def rule_anom_prev(well, ts, chan="SPPA", thr=2.0):
    """Rule kanal kausal: |z| kanal pada bin t-1 melewati ambang."""
    zv, ok = z_on_ts(well, ts - 1, chan=chan)
    return ((np.abs(zv) > thr) & ok).astype(int)


def any_alarm_window(alarm, w=10):
    """Alarm dipertahankan w menit (zona peringatan)."""
    a = np.asarray(alarm, int)
    if w <= 1:
        return a
    out = np.zeros_like(a)
    idx = np.flatnonzero(a)
    for i in idx:
        out[i:i + w] = 1
    return out


def pilih_h(z, budget=ALPHA_BUDGET, grid=(0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10, 12, 15, 20, 30)):
    """Ambang CUSUM terbesar yang masih memenuhi anggaran alarm pada kalibrasi."""
    best = grid[-1]
    for h in grid:
        a = cusum(z, h)
        if a.mean() <= budget:
            best = h
            break
    return best


# ---------------------------------------------------------------- ML
def fit_lgb(X, y, seed=SEED):
    import lightgbm as lgb
    m = lgb.LGBMClassifier(n_estimators=150, learning_rate=0.08, num_leaves=31,
                           min_child_samples=40, subsample=0.9, subsample_freq=1,
                           colsample_bytree=0.9, random_state=seed, n_jobs=2,
                           verbose=-1)
    m.fit(X, y)
    return m


def ambil_ambigu(y, score, alpha=ALPHA_BUDGET):
    """Ambang conformal sederhana: kuantil (1-alpha) skor negatif set kalibrasi."""
    neg = score[np.asarray(y) == 0]
    if len(neg) == 0:
        return float(np.max(score))
    return float(np.quantile(neg, 1.0 - alpha))


def fitur_dari(df):
    drop = [c for c in df.columns if c.startswith(LABEL_COLS) or c in META_COLS]
    feats = [c for c in df.columns if c not in drop and pd.api.types.is_numeric_dtype(df[c])]
    assert "ts_bin" not in feats and "feat_ts_max" not in feats, "kolom bocor masuk fitur"
    return feats


# ---------------------------------------------------------------- tugas
def task_hyd():
    """Statistik + rule pada hyd K-i. Satu-satunya tugas tanpa ML."""
    df = pd.read_csv(f"{DSD}/hyd_ki.csv.gz")
    folds = json.load(open(f"{LOWOD}/lowo_hyd_ki.json"))["folds"]
    well_df = {w: df[df["well"] == w].sort_values("ts_bin").reset_index(drop=True)
               for w in df["well"].unique()}
    rows = []
    for f in folds:
        w = f["test_well"]; d = well_df[w]
        y = d["y_hyd"].to_numpy(int); ts = d["ts_bin"].to_numpy(int)
        zv, ok = z_on_ts(w, ts)
        rule = rule_anom_prev(w, ts)
        cal = f["train_wells"][0]
        dc = well_df[cal]
        zc, _ = z_on_ts(cal, dc["ts_bin"].to_numpy(int))
        h = pilih_h(zc)
        stat = cusum(zv, h)
        stat_w = any_alarm_window(stat, 10)
        for nama, pred in (
            ("rule_kanal", rule),
            ("stat_cusum", stat_w),
            ("H1_stat_dan_rule", ((stat_w == 1) & (rule == 1)).astype(int)),
            ("H1b_stat_atau_rule", ((stat_w == 1) | (rule == 1)).astype(int)),
        ):
            rec = lengkap(y, pred, ts)
            rec.update(dict(fold=w, model=nama, h_terpilih=h,
                            lead=lead_time(y, pred), separuh=separuh(ts, y, pred),
                            prev=round(float(y.mean()), 6)))
            rows.append(rec)
        log(f"hyd {w}: h={h} rule FP={int(((rule==1)&(y==0)).sum())} "
            f"stat FP={int(((stat_w==1)&(y==0)).sum())}")
    return rows


def task_shk():
    """ML + statistik pada shk K-i."""
    df = pd.read_csv(f"{DSD}/shk.csv.gz")
    folds = json.load(open(f"{LOWOD}/lowo_shk.json"))["folds"]
    feats = fitur_dari(df)
    well_df = {w: df[df["well"] == w].sort_values("ts_bin").reset_index(drop=True)
               for w in df["well"].unique()}
    rows = []
    for f in folds:
        w = f["test_well"]; d = well_df[w]
        y = d["y_shk"].to_numpy(int); ts = d["ts_bin"].to_numpy(int)
        cal = f["train_wells"][0]
        tr_wells = [t for t in f["train_wells"] if t != cal]
        Xtr = pd.concat([well_df[t][feats] for t in tr_wells]); ytr = pd.concat(
            [well_df[t]["y_shk"] for t in tr_wells]).to_numpy(int)
        m = fit_lgb(Xtr, ytr)
        cal_score = m.predict_proba(well_df[cal][feats])[:, 1]
        cal_y = well_df[cal]["y_shk"].to_numpy(int)
        thr = ambil_ambigu(cal_y, cal_score)
        score = m.predict_proba(d[feats])[:, 1]
        ml = (score >= thr).astype(int)
        zv, ok = z_on_ts(w, ts)
        zc, _ = z_on_ts(cal, well_df[cal]["ts_bin"].to_numpy(int))
        h = pilih_h(zc)
        stat_w = any_alarm_window(cusum(zv, h), 10)
        rule = rule_anom_prev(w, ts)
        for nama, pred in (
            ("ML_saja", ml),
            ("stat_cusum", stat_w),
            ("rule_kanal", rule),
            ("H2_ML_dan_stat", ((ml == 1) & (stat_w == 1)).astype(int)),
            ("H2b_ML_dan_stat_atau_rule", ((ml == 1) & ((stat_w == 1) | (rule == 1))).astype(int)),
        ):
            rec = lengkap(y, pred, ts)
            rec.update(dict(fold=w, model=nama, thr_kalibrasi=round(thr, 6), h_terpilih=h,
                            lead=lead_time(y, pred), separuh=separuh(ts, y, pred),
                            auprc=round(float(average_precision_score(y, score)), 4),
                            auc=round(float(roc_auc_score(y, score)), 4) if 0 < y.sum() < len(y) else None,
                            prev=round(float(y.mean()), 6)))
            rows.append(rec)
        log(f"shk {w}: thr={thr:.4f} ML FP={int(((ml==1)&(y==0)).sum())} "
            f"H2 FP={int(((ml==1)&(stat_w==1)&(y==0)).sum())} prev={y.mean():.4f}")
    return rows


def gwo(obj, dim, lo, hi, n_wolf=12, n_iter=18, seed=SEED):
    """Grey Wolf Optimizer sederhana dan deterministik."""
    rng = np.random.default_rng(seed)
    X = rng.uniform(lo, hi, size=(n_wolf, dim))
    fit = np.array([obj(x) for x in X])
    order = np.argsort(fit)
    alpha, beta, delta = X[order[0]].copy(), X[order[1]].copy(), X[order[2]].copy()
    fa = fit[order[0]]
    for it in range(n_iter):
        a = 2.0 - 2.0 * it / max(n_iter - 1, 1)
        for i in range(n_wolf):
            for j in range(dim):
                r1, r2 = rng.random(), rng.random()
                A1 = 2 * a * r1 - a; C1 = 2 * r2
                D = abs(C1 * alpha[j] - X[i, j]); x1 = alpha[j] - A1 * D
                r1, r2 = rng.random(), rng.random()
                A2 = 2 * a * r1 - a; C2 = 2 * r2
                D = abs(C2 * beta[j] - X[i, j]); x2 = beta[j] - A2 * D
                r1, r2 = rng.random(), rng.random()
                A3 = 2 * a * r1 - a; C3 = 2 * r2
                D = abs(C3 * delta[j] - X[i, j]); x3 = delta[j] - A3 * D
                X[i, j] = np.clip((x1 + x2 + x3) / 3.0, lo[j], hi[j])
            fit[i] = obj(X[i])
        order = np.argsort(fit)
        if fit[order[0]] < fa:
            fa = float(fit[order[0]]); alpha = X[order[0]].copy()
        beta, delta = X[order[1]].copy(), X[order[2]].copy()
    return alpha, float(fa)


def task_toolwear():
    """Metaheuristik + ML pada tool_wear (469 jendela, LOWO per tool)."""
    from sklearn.metrics import balanced_accuracy_score, f1_score
    tw = pd.read_csv(f"{BASE}/scratch/v6_e1/toolwear_windows.csv")
    feats = [c for c in tw.columns if c.startswith(("X_", "Y_", "Z_"))]
    tools = sorted(tw["tool"].unique())
    rows = []
    for t in tools:
        tr = tw[tw["tool"] != t]; te = tw[tw["tool"] == t].sort_values(["run", "start_sample"])
        if te["y"].nunique() < 2 or tr["y"].nunique() < 2:
            log(f"toolwear {t}: dilewati, label tidak bervariasi"); continue
        Xtr = tr[feats].to_numpy(float); ytr = tr["y"].to_numpy(int)
        Xte = te[feats].to_numpy(float); yte = te["y"].to_numpy(int)
        scaler = StandardScaler().fit(Xtr)
        Xtr_s, Xte_s = scaler.transform(Xtr), scaler.transform(Xte)

        def skor(C, thr):
            clf = LogisticRegression(C=C, max_iter=2000, random_state=SEED)
            clf.fit(Xtr_s, ytr)
            p = clf.predict_proba(Xte_s)[:, 1]
            pred = (p >= thr).astype(int)
            bacc = balanced_accuracy_score(yte, pred)
            f1 = f1_score(yte, pred, zero_division=0)
            pr = rows_metrics(yte, pred)
            return dict(bacc=round(float(bacc), 4), f1=round(float(f1), 4),
                        precision=pr["precision"], recall=pr["recall"],
                        tp=pr["tp"], fp=pr["fp"], fn=pr["fn"], thr=float(thr), C=float(C))

        default = skor(1.0, 0.5)

        # GWO hanya melihat data latih (inner LOWO per tool latih), bukan tool uji
        inner = []
        for t2 in sorted(tr["tool"].unique()):
            a = tr[tr["tool"] != t2]; b = tr[tr["tool"] == t2]
            if b["y"].nunique() < 2 or a["y"].nunique() < 2:
                continue
            inner.append((a[feats].to_numpy(float), a["y"].to_numpy(int),
                          b[feats].to_numpy(float), b["y"].to_numpy(int)))

        def buat_obj(kriteria):
            def obj(v):
                C = float(np.clip(v[0], 0.01, 30.0)); thr = float(np.clip(v[1], 0.05, 0.95))
                vals = []
                for Xa, ya, Xb, yb in inner:
                    sc = StandardScaler().fit(Xa)
                    clf = LogisticRegression(C=C, max_iter=2000, random_state=SEED)
                    clf.fit(sc.transform(Xa), ya)
                    p = clf.predict_proba(sc.transform(Xb))[:, 1]
                    pred = (p >= thr).astype(int)
                    if kriteria == "f1":
                        vals.append(f1_score(yb, pred, zero_division=0))
                    else:
                        vals.append(balanced_accuracy_score(yb, pred))
                return float(-(np.mean(vals) - 0.25 * np.std(vals)))
            return obj

        hasil_gwo = {}
        for kriteria in ("f1", "bacc"):
            best, fbest = gwo(buat_obj(kriteria), 2, np.array([-2.0, 0.05]), np.array([3.4, 0.95]))
            C_b = float(np.clip(10 ** best[0], 0.01, 30.0)); thr_b = float(np.clip(best[1], 0.05, 0.95))
            hasil_gwo[kriteria] = (C_b, thr_b, skor(C_b, thr_b), round(float(-fbest), 4))

        for nama, res in (("ML_default", default),
                          ("H3a_GWO_objF1", hasil_gwo["f1"][2]),
                          ("H3b_GWO_objBacc", hasil_gwo["bacc"][2])):
            rec = dict(fold=t, model=nama, n_uji=int(len(te)),
                       prev=round(float(yte.mean()), 4), **res)
            rec["delta_bacc"] = round(res["bacc"] - default["bacc"], 4)
            rows.append(rec)
        log(f"toolwear {t}: default bacc={default['bacc']} "
            f"GWO-F1 bacc={hasil_gwo['f1'][2]['bacc']} (C={hasil_gwo['f1'][0]:.3f}, thr={hasil_gwo['f1'][1]:.3f}) "
            f"GWO-Bacc bacc={hasil_gwo['bacc'][2]['bacc']} (C={hasil_gwo['bacc'][0]:.3f}, thr={hasil_gwo['bacc'][1]:.3f})")
    return rows


def task_stuck():
    """Tiga komponen pada stuck K-ii (onset): rule + stat + ML."""
    df = pd.read_csv(f"{DSD}/stuck_k2.csv.gz")
    folds = json.load(open(f"{LOWOD}/lowo_stuck_k2.json"))["folds"]
    feats = fitur_dari(df)
    well_df = {w: df[df["well"] == w].sort_values("ts_bin").reset_index(drop=True)
               for w in df["well"].unique()}
    rows = []
    for f in folds:
        w = f["test_well"]; d = well_df[w]
        y = d["y_stuck_onset"].to_numpy(int); ts = d["ts_bin"].to_numpy(int)
        cal = f["train_wells"][0]
        tr_wells = [t for t in f["train_wells"] if t != cal]
        Xtr = pd.concat([well_df[t][feats] for t in tr_wells])
        ytr = pd.concat([well_df[t]["y_stuck_onset"] for t in tr_wells]).to_numpy(int)
        if ytr.sum() == 0:
            log(f"stuck {w}: train tanpa positif, dilewati"); continue
        m = fit_lgb(Xtr, ytr)
        cal_score = m.predict_proba(well_df[cal][feats])[:, 1]
        cal_y = well_df[cal]["y_stuck_onset"].to_numpy(int)
        thr = ambil_ambigu(cal_y, cal_score) if cal_y.sum() > 0 else float(np.quantile(cal_score, 0.99))
        score = m.predict_proba(d[feats])[:, 1]
        ml = (score >= thr).astype(int)
        zv, _ = z_on_ts(w, ts, chan="TQA")
        zc, _ = z_on_ts(cal, well_df[cal]["ts_bin"].to_numpy(int), chan="TQA")
        h = pilih_h(zc)
        stat_w = any_alarm_window(cusum(zv, h), 10)
        rule = rule_anom_prev(w, ts, chan="TQA")
        for nama, pred in (
            ("ML_saja", ml),
            ("stat_cusum", stat_w),
            ("rule_kanal", rule),
            ("H4_tiga_komponen", ((ml == 1) & ((stat_w == 1) | (rule == 1))).astype(int)),
            ("H4b_strict_ML_dan_stat_dan_rule", ((ml == 1) & (stat_w == 1) & (rule == 1)).astype(int)),
        ):
            rec = lengkap(y, pred, ts)
            rec.update(dict(fold=w, model=nama, thr_kalibrasi=round(thr, 6), h_terpilih=h,
                            lead=lead_time(y, pred), separuh=separuh(ts, y, pred),
                            auprc=round(float(average_precision_score(y, score)), 4) if y.sum() else None,
                            prev=round(float(y.mean()), 6)))
            rows.append(rec)
        log(f"stuck {w}: thr={thr:.4f} ML FP={int(((ml==1)&(y==0)).sum())} "
            f"H4 FP={int(((ml==1)&((stat_w==1)|(rule==1))&(y==0)).sum())} prev={y.mean():.4f}")
    return rows


TASKS = dict(hyd=task_hyd, shk=task_shk, toolwear=task_toolwear, stuck=task_stuck)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True, choices=sorted(TASKS))
    args = ap.parse_args()
    t0 = time.time()
    rows = TASKS[args.task]()
    ringkas = {}
    for mdl in sorted({r["model"] for r in rows}):
        sub = [r for r in rows if r["model"] == mdl]
        if "far24_kalender" in sub[0]:
            ringkas[mdl] = dict(
                n_fold=len(sub),
                fp_total=int(sum(r["rows"]["fp"] for r in sub)),
                tp_total=int(sum(r["rows"]["tp"] for r in sub)),
                recall_median=_med([r["rows"]["recall"] for r in sub]),
                recall_min=_min([r["rows"]["recall"] for r in sub]),
                recall_maks=_maks([r["rows"]["recall"] for r in sub]),
                precision_median=_med([r["rows"]["precision"] for r in sub]),
                far24_median=_med([r["far24_kalender"] for r in sub]),
                far24_min=_min([r["far24_kalender"] for r in sub]),
                far24_maks=_maks([r["far24_kalender"] for r in sub]),
                fold_far_le6=int(sum(1 for r in sub if r["far24_kalender"] <= 6.0)),
                fold_recall_gt0=int(sum(1 for r in sub if (r["rows"]["recall"] or 0) > 0)),
                fp_kejadian_total=int(sum(r["events"]["fp_kejadian"] for r in sub)),
                lead_median_median=_med([r["lead"]["lead_median_min"] for r in sub]),
                n_onset=int(sum(r["lead"]["n_onset"] for r in sub)),
                n_diperingatkan=int(sum(r["lead"]["n_diperingatkan"] for r in sub)),
            )
        else:
            ringkas[mdl] = dict(
                n_fold=len(sub),
                bacc_median=_med([r["bacc"] for r in sub]),
                bacc_min=_min([r["bacc"] for r in sub]),
                bacc_maks=_maks([r["bacc"] for r in sub]),
                f1_median=_med([r["f1"] for r in sub]),
                tp_total=int(sum(r["tp"] for r in sub)),
                fp_total=int(sum(r["fp"] for r in sub)),
                fn_total=int(sum(r["fn"] for r in sub)),
            )
    out = dict(task=args.task, seed=SEED, alpha_budget=ALPHA_BUDGET,
               elapsed_s=round(time.time() - t0, 1), rows=rows, ringkas=ringkas)
    p = f"{OUT}/r8_{args.task}.json"
    json.dump(out, open(p, "w"), indent=1)
    log(f"{args.task} selesai {out['elapsed_s']}s -> {p}")
    print(json.dumps(ringkas, indent=1))


def _vals(xs):
    return [x for x in xs if x is not None]


def _med(xs):
    v = _vals(xs)
    return round(float(np.median(v)), 4) if v else None


def _min(xs):
    v = _vals(xs)
    return round(float(min(v)), 4) if v else None


def _maks(xs):
    v = _vals(xs)
    return round(float(max(v)), 4) if v else None


if __name__ == "__main__":
    main()
