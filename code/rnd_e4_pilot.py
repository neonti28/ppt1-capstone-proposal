#!/usr/bin/env python3
"""RND-E4 — pilot ulang hyd K-i SETELAH perbaikan temuan R7.

Perbaikan yang diterapkan (nomor mengikuti docs/RND_R7_REVIEW.md):
  R7-1  baseline rule memakai anom bin (t-1) dari bins lewat code/rnd_rule_baseline.py
        (proksi `rule_lag = y[t-1]` dibuang). Assert FP rule 2.091 +-5% dan hybrid 927 +-5%.
  R7-2  ts_bin masuk daftar kolom terlarang sebagai fitur. Assert len(feats) == 40.
  R7-3  setiap detektor dilaporkan pada DUA satuan: FP baris dan FP kejadian,
        dengan kolom "satuan_dipakai_gate".
  R7-4  gate_A wajib memuat syarat recall >= 0.5.
  R7-5  titik operasi diambil dari anggaran alarm (alpha = 1/240), tanpa syarat TP minimum;
        varian aturan lama tetap dijalankan hanya sebagai pembanding sebelum/sesudah.
  R7-6  gate A versi baru: FAR per 24 jam KALENDER + syarat cakupan >= 0.50 + recall.

Keluaran: scratch/rnd/e4/*.json
"""
import argparse, json, os, sys, time, warnings
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score

warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rnd_rule_baseline as RB

BASE = "/mnt/d/Capstone 1(v2)"
DS = f"{BASE}/scratch/v9_d1/datasets/hyd_ki.csv.gz"
LOWO = f"{BASE}/scratch/v9_d1/lowo_hyd_ki.json"
OUT = f"{BASE}/scratch/rnd/e4"
E3 = f"{BASE}/scratch/rnd/e3"
os.makedirs(OUT, exist_ok=True)

W = 10
H_DET = 10
LABEL_DERIVED = ("y_hyd", "y_prev_hyd", "valid_prev_hyd", "obs_hyd", "anom_hyd",
                 "lab_ts", "lab_kind", "feat_ts_max")
KOLOM_TERLARANG_FITUR = set(LABEL_DERIVED) | {"ts_bin"}
ALPHAS = [0.0005, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.10, 0.20, 0.30]
ALPHA_ANGGARAN = 1.0 / 240.0     # R7-5: FAR<=6/24 jam setara alpha<=1/240
H_GRID = [1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0, 15.0, 20.0, 30.0]
CUSUM_K = 0.5
CAKUPAN_MIN = 0.50
RECALL_MIN = 0.50
FAR_MAKS = 6.0

RUNLOG = []


def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    RUNLOG.append(line)


# ------------------------------------------------------------------ metrik
def op_metrics(y, pred):
    y = np.asarray(y).astype(int); pred = np.asarray(pred).astype(int)
    tp = int(((pred == 1) & (y == 1)).sum()); fp = int(((pred == 1) & (y == 0)).sum())
    fn = int(((pred == 0) & (y == 1)).sum()); tn = int(((pred == 0) & (y == 0)).sum())
    n_neg = int((y == 0).sum()); jam_neg = n_neg / 60.0
    return dict(tp=tp, fp=fp, fn=fn, tn=tn, n_neg=n_neg,
                precision=(tp / (tp + fp)) if (tp + fp) else None,
                recall=(tp / (tp + fn)) if (tp + fn) else None,
                far_per_24h=(fp / jam_neg * 24.0) if jam_neg else None,
                jam_neg=jam_neg)


def event_metrics(y, pred):
    """Satuan kejadian (R7-3). Satu deret pred==1 berurutan = satu kejadian.
    Kejadian dihitung FP bila tidak menempel pada satu baris positif pun."""
    y = np.asarray(y).astype(int); pred = np.asarray(pred).astype(int)
    runs, n, i = [], len(pred), 0
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
    n_neg = int((y == 0).sum()); jam_neg = n_neg / 60.0
    return dict(tp_kejadian=int(tp_ev), fp_kejadian=int(fp_ev),
                n_kejadian=len(runs),
                far24_kejadian=(fp_ev / jam_neg * 24.0) if jam_neg else None,
                menit_alarm=int(pred.sum()))


def garwood_upper(k, jam_neg, alpha=0.95):
    from scipy.stats import chi2
    if jam_neg <= 0:
        return None
    hi = chi2.ppf(1 - (1 - alpha) / 2, 2 * (k + 1)) / 2.0
    return hi / jam_neg * 24.0


def detection_stats(y, alarm):
    delays, onsets, detected_H = [], 0, 0
    n, i = len(y), 0
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


def cakupan_stats(ts):
    menit_kal = float(ts.max() - ts.min() + 1)
    return dict(n=len(ts), menit_kalender=menit_kal,
                fraksi=round(len(ts) / menit_kal, 4) if menit_kal else None)


def lengkapi(y, pred, ts):
    """Rekap satu fold pada dua satuan + FAR kalender + gerbang versi lama dan baru."""
    rows = op_metrics(y, pred)
    ev = event_metrics(y, pred)
    cak = cakupan_stats(ts)
    n_pos = int(np.asarray(y).sum())
    menit_neg_kal = max(cak["menit_kalender"] - n_pos, 1.0)
    out = dict(rows=rows, events=ev, cakupan=cak,
               far24_kalender=(rows["fp"] / (menit_neg_kal / 1440.0)),
               far24_kalender_kejadian=(ev["fp_kejadian"] / (menit_neg_kal / 1440.0)))
    out["gate_A_lama"] = bool(rows["far_per_24h"] is not None and rows["far_per_24h"] <= FAR_MAKS)
    out["gate_A_lama_penuh"] = bool(rows["far_per_24h"] is not None and rows["far_per_24h"] <= FAR_MAKS
                                    and (rows["recall"] or 0) >= 0.5)
    out["gate_A_baru"] = bool(out["far24_kalender"] <= FAR_MAKS
                              and (cak["fraksi"] or 0) >= CAKUPAN_MIN
                              and (rows["recall"] or 0) >= RECALL_MIN)
    out["gate_A_baru_kejadian"] = bool(out["far24_kalender_kejadian"] <= FAR_MAKS
                                       and (cak["fraksi"] or 0) >= CAKUPAN_MIN
                                       and (rows["recall"] or 0) >= RECALL_MIN)
    out["satuan_dipakai_gate"] = "baris (far24_kalender); kejadian dilaporkan berdampingan"
    return out


def block_bootstrap_ci(y, score, n_boot=300, block=60, seed=42):
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
    return [round(float(np.percentile(vals, 2.5)), 4), round(float(np.percentile(vals, 97.5)), 4)]


# ------------------------------------------------------------------ CUSUM
def build_z(well):
    b = pd.read_csv(f"{BASE}/scratch/v9_d1/bins/{well}.csv.gz")
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


def cusum_alarms(z, h, k=CUSUM_K, reset=True):
    z = np.asarray(z, dtype=float)
    cp = np.zeros(len(z)); cn = np.zeros(len(z)); al = np.zeros(len(z), dtype=int)
    for i, v in enumerate(z):
        prev_p = cp[i - 1] if i else 0.0
        prev_n = cn[i - 1] if i else 0.0
        cp[i] = max(0.0, prev_p + (v - k))
        cn[i] = max(0.0, prev_n + (-v - k))
        if cp[i] > h or cn[i] > h:
            al[i] = 1
            if reset:
                cp[i] = 0.0; cn[i] = 0.0
    return al


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", default="42,7")
    ap.add_argument("--skip-cusum", action="store_true")
    args = ap.parse_args()
    seeds = [int(s) for s in args.seeds.split(",")]
    t0 = time.time()

    df = pd.read_csv(DS)
    feats = [c for c in df.columns if c not in KOLOM_TERLARANG_FITUR
             and pd.api.types.is_numeric_dtype(df[c])]
    assert "ts_bin" not in feats, "R7-2 gagal: ts_bin masih dipakai sebagai fitur"
    assert len(feats) == 40, f"R7-2: jumlah fitur {len(feats)}, harap 40"
    lowo = json.load(open(LOWO)); folds = lowo["folds"]
    log(f"data {df.shape} fitur {len(feats)} (ts_bin dibuang) fold {len(folds)} seed {seeds}")

    well_df = {w: df[df["well"] == w].sort_values("ts_bin").reset_index(drop=True)
               for w in sorted(df["well"].unique())}

    # ---------------- baseline jujur + proksi lama sebagai pembanding ----------
    base_rows = []
    for f in folds:
        w = f["test_well"]
        d = well_df[w]
        y = d["y_hyd"].to_numpy(int)
        ts = d["ts_bin"].to_numpy(int)
        hyb, rule, pers = RB.hybrid_rule_persistence(
            w, ts, d["y_prev_hyd"].to_numpy(int), d["valid_prev_hyd"].to_numpy(int))
        proxy = (np.concatenate([[0], y[:-1]]) & pers).astype(int)
        for nama, pred, status in (("rule_t0m1", rule, "sah"),
                                   ("persistence", pers, "sah"),
                                   ("hybrid_rule_persistence", hyb, "sah"),
                                   ("hybrid_proxy_E3", proxy, "TIDAK SAH: proksi label bocor")):
            rec = lengkapi(y, pred, ts)
            rec.update(dict(fold=f"LOWO_test_{w}", test_well=w, model=nama, status_kesahan=status,
                            prev=round(float(y.mean()), 6)))
            base_rows.append(rec)
        log(f"baseline {w}: rule FP={int(((rule==1)&(y==0)).sum())} "
            f"hyb FP={int(((hyb==1)&(y==0)).sum())} proxy FP={int(((proxy==1)&(y==0)).sum())}")

    tot_rule = sum(r["rows"]["fp"] for r in base_rows if r["model"] == "rule_t0m1")
    tot_hyb = sum(r["rows"]["fp"] for r in base_rows if r["model"] == "hybrid_rule_persistence")
    assert_info = RB.assert_published(tot_rule, tot_hyb)
    log(f"ASSERT R7-1 lulus: FP rule {tot_rule} (terbit 2091), FP hybrid {tot_hyb} (terbit 927)")
    json.dump(dict(deskripsi="Baseline dihitung pada 9 fold LOWO memakai rule t0-1 dari bins "
                             "(code/rnd_rule_baseline.py). Proksi E3 ikut dicatat hanya "
                             "sebagai pembanding sebelum/sesudah.",
                   assert_r7_1=assert_info, folds=base_rows,
                   total_fp={"rule_t0m1": tot_rule, "hybrid_rule_persistence": tot_hyb,
                             "persistence": int(sum(r["rows"]["fp"] for r in base_rows
                                                    if r["model"] == "persistence")),
                             "hybrid_proxy_E3": int(sum(r["rows"]["fp"] for r in base_rows
                                                        if r["model"] == "hybrid_proxy_E3"))}),
              open(f"{OUT}/e4_baseline.json", "w"), indent=2)

    # ---------------- A1 LightGBM + conformal ---------------------------------
    import lightgbm as lgb

    def fit_lgb(Xtr, ytr, seed):
        m = lgb.LGBMClassifier(n_estimators=100, num_leaves=15, learning_rate=0.1,
                               min_child_samples=50, subsample=0.8, subsample_freq=1,
                               colsample_bytree=0.8, reg_lambda=1.0, random_state=seed,
                               n_jobs=4, verbose=-1)
        m.fit(Xtr, ytr)
        return m

    a_recs, a_thr, hyb_recs = [], [], []
    for seed in seeds:
        for f in folds:
            w = f["test_well"]; inner = f["train_wells"]
            dtr = df[df["well"].isin(inner)]
            d = well_df[w]
            y = d["y_hyd"].to_numpy(int); ts = d["ts_bin"].to_numpy(int)
            s_oof, y_oof, w_oof = [], [], []
            for j in inner:
                tr = dtr[dtr["well"] != j]; ca = dtr[dtr["well"] == j]
                m = fit_lgb(tr[feats], tr["y_hyd"].to_numpy(int), seed)
                s_oof.append(m.predict_proba(ca[feats])[:, 1])
                y_oof.append(ca["y_hyd"].to_numpy(int))
                w_oof.append(np.array([j] * len(ca)))
            s_oof = np.concatenate(s_oof); y_oof = np.concatenate(y_oof); w_oof = np.concatenate(w_oof)
            m_final = fit_lgb(dtr[feats], dtr["y_hyd"].to_numpy(int), seed)
            s_te = m_final.predict_proba(d[feats])[:, 1]
            neg = s_oof[y_oof == 0]

            # (a) aturan lama E2: alpha terkecil yang masih memberi >=1 TP di tiap fold dalam
            pilih_lama, kandidat = None, []
            for a in ALPHAS:
                thr = float(np.quantile(neg, 1 - a))
                tp_per = [int(((s_oof[w_oof == j] >= thr) & (y_oof[w_oof == j] == 1)).sum())
                          for j in inner]
                ok = all(t >= 1 for t in tp_per)
                kandidat.append(dict(alpha=a, threshold=thr, tp_inner=tp_per, ok=ok))
                if ok and pilih_lama is None:
                    pilih_lama = dict(alpha=a, threshold=thr, tp_inner=tp_per); break
            fallback = pilih_lama is None
            if fallback:
                best = max(kandidat, key=lambda r: (sum(t >= 1 for t in r["tp_inner"]), -r["alpha"]))
                pilih_lama = dict(alpha=best["alpha"], threshold=best["threshold"],
                                  tp_inner=best["tp_inner"])

            # (b) aturan baru R7-5: alpha dari anggaran alarm, tanpa syarat TP
            thr_budget = float(np.quantile(neg, 1 - ALPHA_ANGGARAN))
            pilih_baru = dict(alpha=ALPHA_ANGGARAN, threshold=thr_budget,
                              n_oof_neg=int(len(neg)))

            auprc = round(float(average_precision_score(y, s_te)), 4)
            for label, pilih in (("alpha_E2_lama", pilih_lama), ("alpha_anggaran", pilih_baru)):
                pred = (s_te >= pilih["threshold"]).astype(int)
                rec = lengkapi(y, pred, ts)
                rec.update(dict(fold=f"LOWO_test_{w}", test_well=w, seed=seed, varian=label,
                                alpha=pilih["alpha"], threshold=round(float(pilih["threshold"]), 8),
                                fallback=bool(fallback) if label == "alpha_E2_lama" else False,
                                tp_inner=pilih.get("tp_inner"), n=len(y), prev=round(float(y.mean()), 6),
                                auprc=auprc, det=detection_stats(y, pred)))
                rec["garwood_upper_95"] = garwood_upper(rec["rows"]["fp"], rec["rows"]["jam_neg"])
                if seed == seeds[0] and label == "alpha_anggaran":
                    rec["ci95_auprc"] = block_bootstrap_ci(y, s_te, seed=seed)
                    rec["ci_memuat_prev"] = (rec["ci95_auprc"] is not None and
                                             rec["ci95_auprc"][0] <= rec["prev"] <= rec["ci95_auprc"][1])
                a_recs.append(rec)
                log(f"A1 {label} seed{seed} {w}: FAR24baris={rec['rows']['far_per_24h']:.2f} "
                    f"FAR24kej={rec['events']['far24_kejadian']:.2f} P={rec['rows']['precision']} "
                    f"R={rec['rows']['recall']} alpha={pilih['alpha']:.6f}")

            # hybrid (kebijakan evaluasi §4): ML sebagai pemeringkat di belakang gerbang rule
            hyb, rule, pers = RB.hybrid_rule_persistence(
                w, ts, d["y_prev_hyd"].to_numpy(int), d["valid_prev_hyd"].to_numpy(int))
            ml = (s_te >= thr_budget).astype(int)
            for nama, pred in (("H_and_hybrid_ML", (hyb & ml).astype(int)),
                               ("H_or_hybrid_ML", (hyb | ml).astype(int))):
                rec = lengkapi(y, pred, ts)
                rec.update(dict(fold=f"LOWO_test_{w}", test_well=w, seed=seed, model=nama,
                                alpha=ALPHA_ANGGARAN, threshold=round(thr_budget, 8),
                                n=len(y), prev=round(float(y.mean()), 6), auprc=auprc,
                                det=detection_stats(y, pred)))
                hyb_recs.append(rec)
                log(f"{nama} seed{seed} {w}: FAR24kej={rec['events']['far24_kejadian']:.2f} "
                    f"P={rec['rows']['precision']} R={rec['rows']['recall']}")
            a_thr.append(dict(seed=seed, fold=f"LOWO_test_{w}", pilih_lama=pilih_lama,
                              pilih_baru=pilih_baru, n_kandidat=len(kandidat),
                              alpha_lama_di_luar_anggaran=bool(pilih_lama["alpha"] > ALPHA_ANGGARAN)))

    json.dump(dict(finalis="A1 LightGBM + conformal CV+, fitur 40 (tanpa ts_bin)",
                   fitur=list(feats), n_fitur=len(feats), seed_list=seeds,
                   alpha_anggaran=ALPHA_ANGGARAN, folds=a_recs, titik_operasi=a_thr,
                   catatan=("Dua aturan titik operasi dijalankan pada skor yang sama: "
                            "alpha_E2_lama (aturan E2, >=1 TP tiap fold dalam) hanya untuk "
                            "pembanding sebelum/sesudah; alpha_anggaran (R7-5) adalah aturan "
                            "yang berlaku. Gate dilaporkan pada dua satuan (R7-3), dan gate_A "
                            "memuat syarat recall >= 0.5 (R7-4) serta cakupan >= 0.5 (R7-6).")),
              open(f"{OUT}/e4_a1.json", "w"), indent=2)
    json.dump(dict(model="H1 = hybrid rule & persistence & ML; H2 = union",
                   folds=hyb_recs,
                   catatan="ML dilatih identik dengan A1; gerbang rule memakai rule t0-1 dari bins."),
              open(f"{OUT}/e4_hybrid.json", "w"), indent=2)

    # ---------------- A2 CUSUM: dua satuan ------------------------------------
    if not args.skip_cusum:
        zmap = {w: build_z(w) for w in well_df}
        c_rows = []
        for w, d in well_df.items():
            zz = zmap[w]
            if zz is None:
                continue
            y = d["y_hyd"].to_numpy(int); ts = d["ts_bin"].to_numpy(int)
            al = cusum_alarms(zz["z"].to_numpy(), 30.0, reset=True)
            zts = zz["ts_bin"].to_numpy()
            row_flag = np.zeros(len(d), dtype=int)
            for i, t in enumerate(ts):
                lo = np.searchsorted(zts, t - W, side="left")
                hi = np.searchsorted(zts, t, side="left")
                if hi > lo:
                    row_flag[i] = int(al[lo:hi].max())
            # satuan kejadian (definisi R7): satu MENIT alarm = satu kejadian.
            # TP bila menit alarm t jatuh di dalam jendela [lab_ts-10, lab_ts) sebuah baris positif.
            am = zts[al == 1]
            pos = ts[y == 1]
            tp_ev = int(sum(1 for t in am if np.any((pos - W <= t) & (t < pos))))
            fp_ev = int(len(am) - tp_ev)
            n_neg = int((y == 0).sum()); jam_neg = n_neg / 60.0
            far_ev = (fp_ev / jam_neg * 24.0) if jam_neg else None
            rec = lengkapi(y, row_flag, ts)
            rec.update(dict(test_well=w, h=30.0, reset=True, alarm_menit=int(len(am)),
                            tp_kejadian=tp_ev, fp_kejadian=fp_ev,
                            far24_kejadian_episode=round(far_ev, 4) if far_ev is not None else None,
                            gate_A_baru_kejadian=bool(far_ev is not None and far_ev <= FAR_MAKS
                                                      and (rec["cakupan"]["fraksi"] or 0) >= CAKUPAN_MIN),
                            catatan="SIRKULAR: z pembentuk label, bukan bukti independen"))
            c_rows.append(rec)
            log(f"A2 {w}: FP baris {rec['rows']['fp']} | FP kejadian {fp_ev} "
                f"| FAR24 baris {rec['rows']['far_per_24h']:.2f} | FAR24 kejadian {far_ev if far_ev is None else round(far_ev,2)}")
        json.dump(dict(finalis="A2 CUSUM dua sisi pada z SPPA", h=30.0, reset=True,
                       folds=c_rows), open(f"{OUT}/e4_a2.json", "w"), indent=2)

    # ---------------- ringkasan ----------------------------------------------
    def med(vals):
        v = [x for x in vals if x is not None]
        return round(float(np.median(v)), 4) if v else None

    summ = dict(seeds=seeds, n_folds=len(folds), elapsed_s=round(time.time() - t0, 1),
                assert_r7_1=assert_info, n_fitur=len(feats),
                ringkas={})
    for var in ("alpha_E2_lama", "alpha_anggaran"):
        sel = [r for r in a_recs if r["varian"] == var]
        summ["ringkas"][var] = dict(
            n=len(sel),
            far24_baris_median=med([r["rows"]["far_per_24h"] for r in sel]),
            far24_kejadian_median=med([r["events"]["far24_kejadian"] for r in sel]),
            far24_kalender_median=med([r["far24_kalender"] for r in sel]),
            recall_median=med([r["rows"]["recall"] for r in sel]),
            precision_median=med([r["rows"]["precision"] for r in sel]),
            fold_gate_A_lama=sum(1 for r in sel if r["gate_A_lama"]),
            fold_gate_A_lama_penuh=sum(1 for r in sel if r["gate_A_lama_penuh"]),
            fold_gate_A_baru=sum(1 for r in sel if r["gate_A_baru"]),
            fold_recall_nol=sum(1 for r in sel if (r["rows"]["recall"] or 0) == 0),
            recall_min=min([r["rows"]["recall"] for r in sel if r["rows"]["recall"] is not None] or [None]),
            recall_maks=max([r["rows"]["recall"] for r in sel if r["rows"]["recall"] is not None] or [None]),
            auprc_median=med([r["auprc"] for r in sel]),
        )
    for nm in ("persistence", "rule_t0m1", "hybrid_rule_persistence", "hybrid_proxy_E3"):
        sel = [r for r in base_rows if r["model"] == nm]
        summ["ringkas"][nm] = dict(
            n=len(sel),
            far24_baris_median=med([r["rows"]["far_per_24h"] for r in sel]),
            far24_kejadian_median=med([r["events"]["far24_kejadian"] for r in sel]),
            far24_kalender_median=med([r["far24_kalender"] for r in sel]),
            recall_median=med([r["rows"]["recall"] for r in sel]),
            precision_median=med([r["rows"]["precision"] for r in sel]),
            fold_gate_A_lama=sum(1 for r in sel if r["gate_A_lama"]),
            fold_gate_A_lama_penuh=sum(1 for r in sel if r["gate_A_lama_penuh"]),
            fold_gate_A_baru=sum(1 for r in sel if r["gate_A_baru"]))
    for nm in ("H_and_hybrid_ML", "H_or_hybrid_ML"):
        sel = [r for r in hyb_recs if r["model"] == nm]
        summ["ringkas"][nm] = dict(
            n=len(sel),
            far24_baris_median=med([r["rows"]["far_per_24h"] for r in sel]),
            far24_kejadian_median=med([r["events"]["far24_kejadian"] for r in sel]),
            far24_kalender_median=med([r["far24_kalender"] for r in sel]),
            recall_median=med([r["rows"]["recall"] for r in sel]),
            precision_median=med([r["rows"]["precision"] for r in sel]),
            fold_gate_A_baru=sum(1 for r in sel if r["gate_A_baru"]))
    summ["log"] = RUNLOG
    json.dump(summ, open(f"{OUT}/e4_summary.json", "w"), indent=2)
    log(f"SELESAI {summ['elapsed_s']}s")


if __name__ == "__main__":
    main()
