#!/usr/bin/env python3
"""R5 — uji anomali TANPA LABEL pada jendela hyd K-i (9 well), dilatih hanya
pada baseline bersih, lalu dievaluasi dengan label yang TIDAK dipakai saat latih.

Detektor: Isolation Forest, LOF (novelty), One-Class SVM, autoencoder (MLP),
matrix profile (1 kanal, z-normalisasi).
Metrik: (a) laju alarm pada baseline sendiri (kepatuhan contamination),
(b) episode alarm per 24 jam baseline, (c) transfer lintas well (fit di well A,
ukur laju alarm di baseline well B), (d) recall horizon 10 menit terhadap y_hyd
sebagai DIAGNOSIS, bukan dasar kalibrasi.

Jalankan: scratch/rnd_r5/.venv/bin/python scratch/rnd_r5/anomaly_unsup.py
"""
import gzip
import csv
import json
import os
import statistics as st
from datetime import datetime

import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.svm import OneClassSVM
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler

BASE = "/mnt/d/Capstone 1(v2)"
SRC = os.path.join(BASE, "scratch/v9_d1/datasets/hyd_ki.csv.gz")
OUT = os.path.join(BASE, "scratch/rnd_r5/anomaly_unsup.json")

CHANNELS = ["TQA", "RPM", "SWOB", "HKLD", "ROP", "BPOS", "depth", "dbtm"]
STATS = ["mean", "std", "slope", "last"]
FEATS = ["%s_%s" % (c, s) for c in CHANNELS for s in STATS]
MIN_BASE = 240
HORIZON = 10
CONTAM = 0.01
FIT_CAP = 1500
MP_WINDOW = 60
MP_CHANNEL = "TQA_mean"
SEED = 0


def load():
    data = {}
    with gzip.open(SRC, "rt", newline="", encoding="utf-8") as f:
        rd = csv.DictReader(f)
        rdr = rd
        for r in rdr:
            w = r["well"]
            try:
                ts = int(round(float(r["ts_bin"])))
            except (TypeError, ValueError):
                continue
            feats = []
            ok = True
            for k in FEATS:
                try:
                    v = float(r[k])
                except (TypeError, ValueError, KeyError):
                    ok = False
                    break
                if v != v:
                    ok = False
                    break
                feats.append(v)
            y = int(float(r["y_hyd"])) if r.get("y_hyd") not in (None, "") else 0
            e = data.setdefault(w, {"ts": [], "X": [], "y": [], "mp": []})
            e["ts"].append(ts)
            e["X"].append(feats if ok else None)
            e["y"].append(y)
            try:
                e["mp"].append(float(r[MP_CHANNEL]))
            except (TypeError, ValueError):
                e["mp"].append(None)
    for w in data:
        order = sorted(range(len(data[w]["ts"])), key=lambda i: data[w]["ts"][i])
        for k in ("ts", "X", "y", "mp"):
            data[w][k] = [data[w][k][i] for i in order]
    return data


def runs(ts):
    blocks, cur = [], [0]
    for i in range(1, len(ts)):
        if ts[i] - ts[i - 1] == 1:
            cur.append(i)
        else:
            blocks.append(cur)
            cur = [i]
    blocks.append(cur)
    return blocks


def episodes(flags, gap=30):
    t = [i for i, a in enumerate(flags) if a]
    if not t:
        return 0
    n, last = 1, t[0]
    for v in t[1:]:
        if v - last > gap:
            n += 1
        last = v
    return n


def matrix_profile_flags(x, m=MP_WINDOW, cap_frac=0.01):
    """Matrix profile 1 kanal (z-normalisasi) dengan diskord sebagai anomali.

    Kembalikan (mp_array, flag_array) pada panjang n-m+1 subsequence.
    """
    n = len(x)
    if n < 3 * m:
        return None, None
    N = n - m + 1
    sub = np.lib.stride_tricks.sliding_window_view(x, m)
    mu = sub.mean(axis=1, keepdims=True)
    sd = sub.std(axis=1, keepdims=True)
    sd[sd == 0] = 1e-9
    zs = (sub - mu) / sd
    mp = np.full(N, np.inf)
    step = 512
    for s in range(0, N, step):
        e = min(N, s + step)
        d = np.sqrt(np.maximum(0.0, 2 * m - 2 * (zs[s:e] @ zs.T)))
        for r in range(s, e):
            d[r - s, max(0, r - m + 1):min(N, r + m)] = np.inf  # trivial match
        mp[s:e] = d.min(axis=1)
    thr = np.quantile(mp, 1.0 - cap_frac)
    return mp, mp >= thr


def fit_detectors(Xb):
    sc = StandardScaler().fit(Xb)
    Zb = sc.transform(Xb)
    n_fit = min(FIT_CAP, len(Zb))
    idx = np.linspace(0, len(Zb) - 1, n_fit).astype(int)
    Zf = Zb[idx]
    det = {}
    det["iforest"] = IsolationForest(n_estimators=200, contamination=CONTAM,
                                    random_state=SEED).fit(Zf)
    det["lof"] = LocalOutlierFactor(n_neighbors=20, novelty=True,
                                   contamination=CONTAM).fit(Zf)
    det["ocsvm"] = OneClassSVM(kernel="rbf", nu=CONTAM, gamma="scale").fit(Zf)
    ae = MLPRegressor(hidden_layer_sizes=(16,), max_iter=300, random_state=SEED,
                      early_stopping=False)
    ae.fit(Zf, Zf)
    rec = ((ae.predict(Zf) - Zf) ** 2).sum(axis=1)
    det["ae"] = (ae, float(np.quantile(rec, 1.0 - CONTAM)))
    return sc, det


def score(sc, det, X):
    Z = sc.transform(X)
    out = {}
    out["iforest"] = det["iforest"].predict(Z) == -1
    out["lof"] = det["lof"].predict(Z) == -1
    out["ocsvm"] = det["ocsvm"].predict(Z) == -1
    ae, thr = det["ae"]
    out["ae"] = ((ae.predict(Z) - Z) ** 2).sum(axis=1) >= thr
    return out


def main():
    data = load()
    per_well = {}
    models = {}
    baselines = {}
    for w in sorted(data):
        e = data[w]
        ts, X, y = e["ts"], e["X"], e["y"]
        blocks = runs(ts)
        cand = [b for b in blocks
                if len(b) >= MIN_BASE and all(X[i] is not None and y[i] == 0 for i in b)]
        if not cand:
            per_well[w] = {"status": "tidak dipakai", "blok_maks_menit":
                           max((len(b) for b in blocks), default=0),
                           "n_rows": len(ts)}
            continue
        b = max(cand, key=len)
        Xb = np.array([X[i] for i in b], dtype=float)
        sc, det = fit_detectors(Xb)
        models[w] = (sc, det)
        baselines[w] = Xb
        flags_b = score(sc, det, Xb)

        # skor seluruh deret (baris dengan fitur lengkap)
        rows_ok = [i for i in range(len(ts)) if X[i] is not None]
        Xall = np.array([X[i] for i in rows_ok], dtype=float)
        flags_all = score(sc, det, Xall)
        pos_rel = [k for k, i in enumerate(rows_ok) if y[i] == 1]

        res = {"status": "dipakai", "n_rows": len(ts), "baseline_minutes": len(b),
               "fitur": len(FEATS), "baris_dinilai": len(rows_ok), "positif": len(pos_rel)}
        for k in flags_b:
            fb, fa = flags_b[k], flags_all[k]
            rate = float(fb.mean())
            ep = episodes(list(fb))
            recall = None
            if pos_rel:
                hit = 0
                for p in pos_rel:
                    lo = max(0, p - HORIZON)
                    if fa[lo:p + 1].any():
                        hit += 1
                recall = round(hit / len(pos_rel), 4)
            # presisi alarm-menit: fraksi menit alarm yang berada <=10 mnt sebelum positif
            posmask = np.zeros(len(rows_ok), dtype=bool)
            posmask[pos_rel] = True
            near = np.convolve(posmask.astype(int), np.ones(HORIZON + 1, dtype=int), "same") > 0
            prec = float((fa & near).sum() / fa.sum()) if fa.sum() else None
            res[k] = {
                "laju_alarm_baseline": round(rate, 4),
                "episode_baseline": ep,
                "far_per_24h": round(ep / (len(b) / 1440.0), 2),
                "recall_h10": recall,
                "presisi_menit_alarm": round(prec, 4) if prec is not None else None,
                "alarm_menit_total": int(fa.sum()),
            }

        # matrix profile pada kanal TQA
        xm = [e["mp"][i] for i in b]
        if all(v is not None for v in xm):
            arr = np.array(xm, dtype=float)
            mp, flag = matrix_profile_flags(arr)
            if mp is not None:
                res["matrix_profile"] = {
                    "window_menit": MP_WINDOW,
                    "titik_diskord": int(flag.sum()),
                    "fraksi_diskord": round(float(flag.mean()), 4),
                    "episode_baseline": episodes(list(flag)),
                    "panjang_seri": int(len(arr)),
                }
        per_well[w] = res

    # transfer lintas well: fit di A, ukur laju alarm pada baseline B
    wells = sorted(models)
    transfer = []
    for a in wells:
        sc_a, det_a = models[a]
        for bb in wells:
            if a == bb:
                continue
            Xb = baselines[bb]
            fl = score(sc_a, det_a, Xb)
            row = {"fit_di": a, "diuji_di": bb,
                   "baseline_menit_uji": len(Xb)}
            for k, v in fl.items():
                row[k] = round(float(v.mean()), 4)
            transfer.append(row)

    # ringkasan
    used = [w for w in per_well if per_well[w].get("status") == "dipakai"]
    summary = {"n_well_dipakai": len(used), "wells": used}
    for k in ("iforest", "lof", "ocsvm", "ae"):
        vals = [per_well[w][k]["laju_alarm_baseline"] for w in used if k in per_well[w]]
        recs = [per_well[w][k]["recall_h10"] for w in used
                if k in per_well[w] and per_well[w][k]["recall_h10"] is not None]
        precs = [per_well[w][k]["presisi_menit_alarm"] for w in used
                 if k in per_well[w] and per_well[w][k]["presisi_menit_alarm"] is not None]
        tr = [r[k] for r in transfer if r.get(k) is not None]
        summary[k] = {
            "laju_alarm_baseline_median": round(st.median(vals), 4) if vals else None,
            "laju_alarm_baseline_min": min(vals) if vals else None,
            "laju_alarm_baseline_max": max(vals) if vals else None,
            "recall_h10_median": round(st.median(recs), 4) if recs else None,
            "presisi_menit_median": round(st.median(precs), 4) if precs else None,
            "transfer_laju_alarm_median": round(st.median(tr), 4) if tr else None,
            "transfer_laju_alarm_max": max(tr) if tr else None,
            "transfer_pasangan": len(tr),
        }

    out = {"meta": {"kartu": "t_56d8d11d RND-R5",
                    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "sumber": SRC,
                    "perintah": "scratch/rnd_r5/.venv/bin/python scratch/rnd_r5/anomaly_unsup.py",
                    "sklearn": __import__("sklearn").__version__,
                    "fitur": FEATS, "n_fitur": len(FEATS),
                    "contamination": CONTAM, "fit_cap": FIT_CAP,
                    "catatan": "Detektor dilatih HANYA pada baseline bersih (label tidak dipakai saat latih). "
                               "Label y_hyd dipakai hanya untuk diagnosis recall/presisi setelah skor keluar."},
           "summary": summary, "per_well": per_well, "transfer": transfer}
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    print(json.dumps(summary, indent=1, ensure_ascii=False))
    print(json.dumps(per_well, indent=1, ensure_ascii=False)[:6000])


if __name__ == "__main__":
    main()
