import sys, json, time
sys.path.insert(0, "code")
import numpy as np, pandas as pd
import rnd_e3_pilot as P
from sklearn.metrics import average_precision_score

BASE = "/mnt/d/Capstone 1(v2)"
W = 10
df = pd.read_csv(f"{BASE}/scratch/v9_d1/datasets/hyd_ki.csv.gz")
lowo = json.load(open(f"{BASE}/scratch/v9_d1/lowo_hyd_ki.json"))
folds = lowo["folds"]

# ---------- B2) A2: laju alarm per KEJADIAN (alarm-minute), bukan per baris ----------
print("=== B2. A2 CUSUM h=30 reset=True: satuan kejadian alarm ===")
out = []
for f in folds:
    w = f["test_well"]
    d = df[df["well"] == w].sort_values("ts_bin").reset_index(drop=True)
    y = d["y_hyd"].to_numpy(int)
    lab = d["lab_ts"].to_numpy()
    zz = P.build_z(w)
    zts = zz["ts_bin"].to_numpy()
    al = P.cusum_alarms(zz["z"].to_numpy(), 30.0, reset=True)
    am = zts[al == 1]                      # menit alarm (kejadian)
    # tutup positif: menit alarm t dianggap TP bila ada baris positif dengan lab_ts-10 <= t < lab_ts
    pos = lab[y == 1]
    tp_ev = 0
    for t in am:
        if np.any((pos - W <= t) & (t < pos)):
            tp_ev += 1
    fp_ev = len(am) - tp_ev
    n_neg = int((y == 0).sum()); jam_neg = n_neg / 60.0
    far_ev = fp_ev / jam_neg * 24.0
    # baris (metode E3)
    flagged = np.zeros(len(d), dtype=int)
    for i, t0 in enumerate(lab):
        lo = np.searchsorted(zts, t0 - W, side="left"); hi = np.searchsorted(zts, t0, side="left")
        if hi > lo: flagged[i] = int(al[lo:hi].max())
    m_row = P.op_metrics(y, flagged)
    out.append(dict(well=w, alarm_menit=len(am), tp_kejadian=tp_ev, fp_kejadian=fp_ev,
                    far24_kejadian=round(far_ev, 3), far24_baris=round(m_row["far_per_24h"], 3),
                    rasio_baris_per_kejadian=round(m_row["far_per_24h"] / far_ev, 3) if far_ev else None,
                    fp_baris=m_row["fp"], gateA_kejadian=far_ev <= 6))
b = pd.DataFrame(out)
print(b.to_string())
print("\nmedian FAR24 baris:", round(float(b.far24_baris.median()), 3),
      "| median FAR24 kejadian:", round(float(b.far24_kejadian.median()), 3),
      "| median rasio:", round(float(b.rasio_baris_per_kejadian.median()), 3))
print("gateA lolos (kejadian):", int(b.gateA_kejadian.sum()), "dari 9")

# ---------- C) A1: titik operasi pada anggaran gate A, dan tanpa fitur ts_bin ----------
print("\n=== C. A1 seed 42: titik operasi anggaran 1/240 dan fitur tanpa ts_bin ===")
LABEL_DERIVED = P.LABEL_DERIVED
feats_asis = [c for c in df.columns if c not in LABEL_DERIVED]
feats_asis = [c for c in feats_asis if pd.api.types.is_numeric_dtype(df[c])]
feats_clean = [c for c in feats_asis if c != "ts_bin"]
print("n_fitur as-is:", len(feats_asis), "| tanpa ts_bin:", len(feats_clean))

def fit_lgb(Xtr, ytr, seed):
    import lightgbm as lgb
    m = lgb.LGBMClassifier(
        n_estimators=100, num_leaves=15, learning_rate=0.1,
        min_child_samples=50, subsample=0.8, subsample_freq=1,
        colsample_bytree=0.8, reg_lambda=1.0, random_state=seed,
        n_jobs=4, verbose=-1,
    )
    m.fit(Xtr, ytr)
    return m


def run(seed, feats, mode, alpha_fix=None):
    rows = []
    for f in folds:
        w = f["test_well"]; inner = f["train_wells"]
        dtr_all = df[df["well"].isin(inner)]
        dte = df[df["well"] == w].sort_values("ts_bin").reset_index(drop=True)
        oof_s, oof_y, oof_w = [], [], []
        for j in inner:
            tr = dtr_all[dtr_all["well"] != j]; ca = dtr_all[dtr_all["well"] == j]
            m = fit_lgb(tr[feats], tr["y_hyd"].to_numpy(int), seed)
            oof_s.append(m.predict_proba(ca[feats])[:, 1])
            oof_y.append(ca["y_hyd"].to_numpy(int)); oof_w.append(np.array([j] * len(ca)))
        s_oof = np.concatenate(oof_s); y_oof = np.concatenate(oof_y); w_oof = np.concatenate(oof_w)
        m_final = fit_lgb(dtr_all[feats], dtr_all["y_hyd"].to_numpy(int), seed)
        s_te = m_final.predict_proba(dte[feats])[:, 1]
        y_te = dte["y_hyd"].to_numpy(int)
        neg = s_oof[y_oof == 0]
        if alpha_fix is not None:
            alpha = alpha_fix
        else:
            alpha = None
            for a in P.ALPHAS:
                thr = float(np.quantile(neg, 1 - a))
                if all(int(((s_oof[w_oof == j] >= thr) & (y_oof[w_oof == j] == 1)).sum()) >= 1 for j in inner):
                    alpha = a; break
            if alpha is None: alpha = P.ALPHAS[-1]
        thr = float(np.quantile(neg, 1 - alpha))
        pred = (s_te >= thr).astype(int)
        m = P.op_metrics(y_te, pred)
        m.update(dict(well=w, alpha=alpha, auprc=round(float(average_precision_score(y_te, s_te)), 4),
                      prev=round(float(y_te.mean()), 4), n_pos=int(y_te.sum())))
        m["gateA"] = bool(m["far_per_24h"] is not None and m["far_per_24h"] <= 6)
        rows.append(m)
    return pd.DataFrame(rows)

t0 = time.time()
res = {}
for tag, feats, afix in (("asis_alpha_E2", feats_asis, None),
                         ("asis_alpha_budget", feats_asis, 1/240),
                         ("clean_alpha_E2", feats_clean, None),
                         ("clean_alpha_budget", feats_clean, 1/240)):
    r = run(42, feats, tag, afix)
    res[tag] = r
    print(f"\n-- {tag}: median FAR24={r.far_per_24h.median():.3f} rentang=({r.far_per_24h.min():.3f},{r.far_per_24h.max():.3f}) "
          f"recall_median={r.recall.median():.4f} auprc_median={r.auprc.median():.4f} gateA={int(r.gateA.sum())}/9")
    print(r[["well", "alpha", "far_per_24h", "precision", "recall", "auprc", "prev", "gateA"]].round(4).to_string(index=False))
print("\nelapsed:", round(time.time() - t0, 1), "s")

json.dump(dict(a2_kejadian=b.to_dict("records"),
               a1={k: v.to_dict("records") for k, v in res.items()}),
          open(f"{BASE}/scratch/rnd/r7/r7_measure2.json", "w"), indent=2)
