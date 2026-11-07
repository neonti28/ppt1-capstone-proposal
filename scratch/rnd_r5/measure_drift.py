#!/usr/bin/env python3
"""R5 — ukur beban alarm palsu detektor drift tanpa label pada baseline nyata.

Implementasi pustaka-standar saja (tanpa numpy/pandas), supaya bisa dijalankan
ulang di host dengan memori terbatas dan tanpa lingkungan venv.

Q1. Berapa episode alarm palsu per 24 jam CUSUM dan Page-Hinkley pada baseline
    bersih nyata (bukan simulasi Gaussian iid)?
Q2. Apakah ambang yang dikalibrasi di separuh awal baseline tetap bersih di
    separuh akhir (uji transfer kalibrasi)?
Q3. Berapa autokorelasi lag-1 sehingga asumsi iid gugur?
Q4. Berapa recall detektor itu terhadap label hyd K-i (horizon 10 menit) saat
    kanal yang dipakai TQA, bukan kanal pembentuk label?

Sumber: scratch/v9_d1/datasets/hyd_ki.csv.gz (jendela 1 menit V9, 9 well).
Perintah: python3 scratch/rnd_r5/measure_drift.py
"""
import csv
import gzip
import json
import os
import statistics as st
from datetime import datetime

BASE = "/mnt/d/Capstone 1(v2)"
SRC = os.path.join(BASE, "scratch/v9_d1/datasets/hyd_ki.csv.gz")
OUTDIR = os.path.join(BASE, "scratch/rnd_r5")
OUT = os.path.join(OUTDIR, "drift_far_measured.json")

CHANNEL = "TQA_mean"
MIN_BASE = 600
MERGE_GAP = 30
HORIZON = 10
K_SIGMA = 0.5
H_SIGMA = 5.0
PH_DELTA = 0.005
PH_LAMBDA = 50.0


def load(path):
    """Baca kolom yang perlu; kembalikan dict well -> (ts, x, y)."""
    data = {}
    with gzip.open(path, "rt", newline="", encoding="utf-8") as f:
        rd = csv.DictReader(f)
        need = {"well", "ts_bin", CHANNEL, "y_hyd"}
        if not need.issubset(set(rd.fieldnames)):
            raise SystemExit("kolom hilang: %s" % (need - set(rd.fieldnames)))
        for r in rd:
            w = r["well"]
            try:
                ts = int(float(r["ts_bin"]))
            except (TypeError, ValueError):
                continue
            v = r[CHANNEL]
            try:
                x = float(v)
            except (TypeError, ValueError):
                x = None
            try:
                y = int(float(r["y_hyd"]))
            except (TypeError, ValueError):
                y = None
            e = data.setdefault(w, {"ts": [], "x": [], "y": []})
            e["ts"].append(ts)
            e["x"].append(x)
            e["y"].append(y)
    for w in data:
        order = sorted(range(len(data[w]["ts"])), key=lambda i: data[w]["ts"][i])
        for k in ("ts", "x", "y"):
            data[w][k] = [data[w][k][i] for i in order]
    return data


def grid_runs(ts, x, y):
    """Peta ke grid 1 menit, lalu bagi jadi blok kontigu tanpa menit bolong.

    Kembalikan daftar blok: (list_index_grid_awal, list_posisi_baris).
    Blok hanya berisi menit yang benar-benar ada barisnya dan bersambung 60 dtk.
    """
    pos = {t: i for i, t in enumerate(ts)}
    if not ts:
        return []
    step = 60
    blocks = []
    cur = []
    t = ts[0]
    t_end = ts[-1]
    while t <= t_end:
        i = pos.get(t)
        if i is None:
            if cur:
                blocks.append(cur)
            cur = []
        else:
            cur.append(i)
        t += step
    if cur:
        blocks.append(cur)
    return blocks


def cusum(alarm_out, z, k=K_SIGMA, h=H_SIGMA):
    sp = 0.0
    sn = 0.0
    out = []
    for v in z:
        sp = max(0.0, sp + v - k)
        sn = max(0.0, sn - v - k)
        a = sp > h or sn > h
        out.append(a)
        alarm_out.append(a)
    return out


def page_hinkley(z, delta=PH_DELTA, lam=PH_LAMBDA):
    m = 0.0
    mt = 0.0
    out = []
    for v in z:
        m += v - delta
        mt = min(mt, m)
        a = (m - mt) > lam
        out.append(a)
        if a:
            m, mt = 0.0, 0.0
    return out


def episodes(idxs, gap=MERGE_GAP):
    if not idxs:
        return 0
    t = sorted(idxs)
    n, last = 1, t[0]
    for v in t[1:]:
        if v - last > gap:
            n += 1
        last = v
    return n


def mad_sigma(vals):
    med = st.median(vals)
    mad = st.median([abs(v - med) for v in vals])
    return med, 1.4826 * mad


def lag1(vals):
    if len(vals) < 11:
        return None
    m = st.fmean(vals)
    num = sum((vals[i] - m) * (vals[i + 1] - m) for i in range(len(vals) - 1))
    den = sum((v - m) ** 2 for v in vals)
    return round(num / den, 4) if den > 0 else None


def calib_h(z_ref, target_ep=0):
    for h in (2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 15.0, 20.0, 30.0):
        sink = []
        al = cusum(sink, z_ref, h=h)
        if episodes([i for i, a in enumerate(al) if a]) <= target_ep:
            return h
    return 30.0


def main():
    data = load(SRC)
    rows = []
    skipped = {}
    for w in sorted(data):
        e = data[w]
        ts, x, y = e["ts"], e["x"], e["y"]
        blocks = grid_runs(ts, x, y)
        clean = []
        for b in blocks:
            if len(b) < MIN_BASE:
                continue
            if all(x[i] is not None and (y[i] == 0) for i in b):
                clean.append(b)
        if not clean:
            skipped[w] = {
                "n_rows": len(ts),
                "block_max_minutes": max((len(b) for b in blocks), default=0),
                "alasan": "tidak ada blok kontigu >= %d menit tanpa label positif" % MIN_BASE,
            }
            continue
        b = max(clean, key=len)
        xb = [x[i] for i in b]
        nb = len(b)
        med, sig = mad_sigma(xb)
        z = [(v - med) / sig for v in xb] if sig > 0 else [0.0] * nb

        al_c = cusum([], z)
        al_p = page_hinkley(z)
        ep_c = episodes([i for i, a in enumerate(al_c) if a])
        ep_p = episodes([i for i, a in enumerate(al_p) if a])

        half = nb // 2
        h_cal = calib_h(z[:half])
        al2 = cusum([], z[half:], h=h_cal)
        ep2 = episodes([i for i, a in enumerate(al2) if a])

        # recall label hyd K-i pada horizon HORIZON di seluruh seri well ini
        alarm_full = [False] * len(ts)
        for j, i in enumerate(b):
            alarm_full[i] = al_c[j]
        pos = [i for i, v in enumerate(y) if v == 1]
        hit = 0
        for p in pos:
            lo = max(0, p - HORIZON)
            if any(alarm_full[lo:p + 1]):
                hit += 1

        rows.append({
            "well": w,
            "baseline_minutes": nb,
            "median": round(med, 6),
            "sigma_mad": round(sig, 6),
            "ac1": lag1(z),
            "cusum_episodes": ep_c,
            "cusum_far_24h": round(ep_c / (nb / 1440.0), 2),
            "ph_episodes": ep_p,
            "ph_far_24h": round(ep_p / (nb / 1440.0), 2),
            "half1_h_calibrated": h_cal,
            "half2_episodes_at_h": ep2,
            "positives": len(pos),
            "cusum_recall_h10": round(hit / len(pos), 4) if pos else None,
        })

    def col(k):
        return [r[k] for r in rows if isinstance(r.get(k), (int, float))]

    summary = {
        "channel": CHANNEL,
        "n_wells_total": len(data),
        "n_wells_dipakai": len(rows),
        "baseline_minutes_min": min(col("baseline_minutes")) if rows else None,
        "baseline_minutes_max": max(col("baseline_minutes")) if rows else None,
        "cusum_far_24h_median": round(st.median(col("cusum_far_24h")), 2) if rows else None,
        "cusum_far_24h_min": min(col("cusum_far_24h")) if rows else None,
        "cusum_far_24h_max": max(col("cusum_far_24h")) if rows else None,
        "ph_far_24h_median": round(st.median(col("ph_far_24h")), 2) if rows else None,
        "ph_far_24h_min": min(col("ph_far_24h")) if rows else None,
        "ph_far_24h_max": max(col("ph_far_24h")) if rows else None,
        "ac1_median": round(st.median(col("ac1")), 4) if col("ac1") else None,
        "wells_clean_half2_at_calibrated_h": sum(1 for r in rows if r["half2_episodes_at_h"] == 0),
        "total_positives": sum(r["positives"] for r in rows),
        "recall_h10_pooled": (
            round(sum(r["cusum_recall_h10"] * r["positives"] for r in rows if r["positives"]) /
                  sum(r["positives"] for r in rows if r["positives"]), 4)
            if sum(r["positives"] for r in rows if r["positives"]) else None
        ),
    }
    os.makedirs(OUTDIR, exist_ok=True)
    payload = {
        "meta": {
            "kartu": "t_56d8d11d RND-R5",
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sumber": SRC,
            "perintah": "python3 scratch/rnd_r5/measure_drift.py",
            "parameter": {
                "cusum_k_sigma": K_SIGMA, "cusum_h_sigma": H_SIGMA,
                "ph_delta_sigma": PH_DELTA, "ph_lambda_sigma": PH_LAMBDA,
                "min_baseline_minutes": MIN_BASE, "merge_gap_minutes": MERGE_GAP,
                "horizon_minutes": HORIZON, "step_grid_seconds": 60,
            },
            "catatan": ("FAR dihitung dari episode alarm pada baseline bersih nyata, "
                        "bukan dari ARL Gaussian iid. Baseline = blok kontigu pada grid "
                        "1 menit tanpa menit bolong dan tanpa label positif."),
        },
        "summary": summary,
        "per_well": rows,
        "skipped": skipped,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=1, ensure_ascii=False)
    print(json.dumps(summary, indent=1, ensure_ascii=False))
    for r in rows:
        print(r["well"], r["baseline_minutes"], "CUSUM", r["cusum_episodes"], "/24j", r["cusum_far_24h"],
              "PH", r["ph_episodes"], "/24j", r["ph_far_24h"], "ac1", r["ac1"],
              "h_cal", r["half1_h_calibrated"], "half2_ep", r["half2_episodes_at_h"],
              "recall", r["cusum_recall_h10"])
    print("skipped:", json.dumps(skipped, ensure_ascii=False))
    print("out:", OUT)


if __name__ == "__main__":
    main()
