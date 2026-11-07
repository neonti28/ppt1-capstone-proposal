#!/usr/bin/env python3
"""R5 v2 — ukur perilaku detektor perubahan pada baseline NYATA (hyd K-i, 9 well).

Perbaikan atas percobaan pertama (scratch/rnd_r5/measure_drift.py):
`ts_bin` adalah INDEKS MENIT (epoch menit), bukan detik. Bukti: selisih antar
baris berturut-turut bernilai 1 pada 99,5% pasangan (grid_check.py), dan
span F-10 = 11249 menit = 187,5 jam. Percobaan pertama melangkah 60 pada grid
indeks menit sehingga setiap blok pecah menjadi 1 titik, lalu menyimpulkan
"tidak ada baseline 600 menit". Itu artefak satuan, bukan sifat data.

Pertanyaan yang dijawab (semua angka keluar ke JSON):
Q1 FAR episode/24 jam CUSUM dan Page-Hinkley pada baseline bersih nyata.
Q2 Transfer kalibrasi: h dikalibrasi di separuh awal, diuji di separuh akhir.
Q3 Autokorelasi lag-1 (asumsi iid gugur atau tidak).
Q4 Recall terhadap label hyd K-i, horizon 10 menit.
Q5 Uji KS antar well (drift distribusi) dan dalam well (separuh awal lawan akhir).

Jalankan: python3 scratch/rnd_r5/measure_drift_v2.py
"""
import gzip
import csv
import json
import math
import os
import statistics as st
from datetime import datetime

BASE = "/mnt/d/Capstone 1(v2)"
SRC = os.path.join(BASE, "scratch/v9_d1/datasets/hyd_ki.csv.gz")
OUTDIR = os.path.join(BASE, "scratch/rnd_r5")
OUT = os.path.join(OUTDIR, "drift_measured_v2.json")

CHANNEL = "TQA_mean"
MIN_BASE = 240          # menit kontigu bersih minimum agar well dipakai
MERGE_GAP = 30          # menit; episode alarm digabung bila jaraknya <= 30 menit
HORIZON = 10            # menit sebelum onset
K_SIGMA = 0.5
H_SIGMA = 5.0
PH_DELTA = 0.005
PH_LAMBDA = 50.0
MAX_KS = 6000           # batas ukuran sampel per sisi untuk uji KS (independensi parsial)


def load(path):
    data = {}
    with gzip.open(path, "rt", newline="", encoding="utf-8") as f:
        rd = csv.DictReader(f)
        need = {"well", "ts_bin", CHANNEL, "y_hyd"}
        if not need.issubset(set(rd.fieldnames)):
            raise SystemExit("kolom hilang: %s" % (need - set(rd.fieldnames)))
        for r in rd:
            w = r["well"]
            try:
                ts = int(round(float(r["ts_bin"])))
            except (TypeError, ValueError):
                continue
            try:
                x = float(r[CHANNEL])
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


def runs(ts):
    """Blok kontigu: indeks baris yang ts-nya berselisih tepat 1 menit."""
    blocks = []
    cur = [0]
    for i in range(1, len(ts)):
        if ts[i] - ts[i - 1] == 1:
            cur.append(i)
        else:
            blocks.append(cur)
            cur = [i]
    blocks.append(cur)
    return blocks


def cusum(z, k=K_SIGMA, h=H_SIGMA):
    sp = sn = 0.0
    out = []
    for v in z:
        sp = max(0.0, sp + v - k)
        sn = max(0.0, sn - v - k)
        out.append(sp > h or sn > h)
    return out


def page_hinkley(z, delta=PH_DELTA, lam=PH_LAMBDA):
    m = mt = 0.0
    out = []
    for v in z:
        m += v - delta
        mt = min(mt, m)
        a = (m - mt) > lam
        out.append(a)
        if a:
            m = mt = 0.0
    return out


def episodes(flags, gap=MERGE_GAP):
    t = [i for i, a in enumerate(flags) if a]
    if not t:
        return 0
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
    """h terkecil pada grid yang menghasilkan <= target_ep episode pada data acuan."""
    for h in (2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 15.0, 20.0, 30.0, 40.0, 60.0):
        if episodes(cusum(z_ref, h=h)) <= target_ep:
            return h, episodes(cusum(z_ref, h=h))
    return 60.0, episodes(cusum(z_ref, h=60.0))


def ks_two_sample(a, b):
    """Statistik KS dua sampel + p asimtotik (Kolmogorov)."""
    a = sorted(a)
    b = sorted(b)
    na, nb = len(a), len(b)
    if na == 0 or nb == 0:
        return None
    i = j = 0
    d = 0.0
    while i < na and j < nb:
        if a[i] <= b[j]:
            i += 1
        else:
            j += 1
        d = max(d, abs(i / na - j / nb))
    lam = math.sqrt(na * nb / (na + nb)) * d
    if lam == 0:
        p = 1.0
    else:
        p = 2.0 * sum((-1) ** (k - 1) * math.exp(-2.0 * k * k * lam * lam) for k in range(1, 101))
        p = min(1.0, max(0.0, p))
    return {"D": round(d, 4), "p_approx": round(p, 6), "n_a": na, "n_b": nb}


def thin(vals, cap=MAX_KS):
    if len(vals) <= cap:
        return vals
    step = len(vals) / cap
    return [vals[int(i * step)] for i in range(cap)]


def main():
    data = load(SRC)
    per_well = {}
    skipped = {}
    clean_series = {}
    for w in sorted(data):
        e = data[w]
        ts, x, y = e["ts"], e["x"], e["y"]
        blocks = runs(ts)
        clean = [b for b in blocks
                 if len(b) >= MIN_BASE and all(x[i] is not None and y[i] == 0 for i in b)]
        if not clean:
            skipped[w] = {
                "n_rows": len(ts),
                "block_max_minutes": max((len(b) for b in blocks), default=0),
                "alasan": "tidak ada blok kontigu >= %d menit yang seluruh labelnya 0" % MIN_BASE,
            }
            continue
        b = max(clean, key=len)
        xb = [x[i] for i in b]
        nb = len(b)
        med, sig = mad_sigma(xb)
        z = [(v - med) / sig for v in xb] if sig > 0 else [0.0] * nb

        al_c = cusum(z)
        al_p = page_hinkley(z)
        ep_c = episodes(al_c)
        ep_p = episodes(al_p)

        half = nb // 2
        h_cal, ep_cal = calib_h(z[:half])
        al2 = cusum(z[half:], h=h_cal)
        ep2 = episodes(al2)

        # --- evaluasi pada SELURUH seri (bukan hanya dalam baseline) ---
        # Parameter (median, sigma MAD, h) diambil dari baseline, lalu detektor
        # dijalankan pada tiap segmen nilai tak-null. Ini yang membuat recall
        # bermakna: alarm di luar baseline ikut dihitung.
        full_c = [False] * len(x)
        full_p = [False] * len(x)
        zf = [((v - med) / sig) if (v is not None and sig > 0) else None for v in x]
        i = 0
        n_seg = 0
        while i < len(zf):
            if zf[i] is None:
                i += 1
                continue
            j = i
            while j < len(zf) and zf[j] is not None:
                j += 1
            seg = zf[i:j]
            if len(seg) >= 10:
                n_seg += 1
                for k, a in enumerate(cusum(seg)):
                    full_c[i + k] = a
                for k, a in enumerate(page_hinkley(seg)):
                    full_p[i + k] = a
            i = j

        pos = [i for i, v in enumerate(y) if v == 1]
        alarm_base = [False] * len(x)
        for j, ii in enumerate(b):
            alarm_base[ii] = al_c[j]
        hit_in_base = sum(1 for p in pos if any(alarm_base[max(0, p - HORIZON):p + 1]))

        def recall_at(flags, horizon=HORIZON):
            hit = 0
            for p in pos:
                lo = max(0, p - horizon)
                if any(flags[lo:p + 1]):
                    hit += 1
            return round(hit / len(pos), 4) if pos else None

        hit_full = sum(1 for p in pos if any(full_c[max(0, p - HORIZON):p + 1]))
        bl = set(b)
        alarms_outside = sum(1 for idx, a in enumerate(full_c) if a and idx not in bl)
        # alarm per jam pada menit yang BUKAN baseline (positif atau tidak)
        outside_minutes = len(x) - nb

        clean_series[w] = thin(xb)
        per_well[w] = {
            "n_rows": len(ts),
            "n_blocks": len(blocks),
            "n_segmen_deret": n_seg,
            "baseline_minutes": nb,
            "baseline_hours": round(nb / 60.0, 2),
            "baseline_start_ts": ts[b[0]],
            "median": round(med, 6),
            "sigma_mad": round(sig, 6),
            "cv_percent": round(100.0 * sig / abs(med), 2) if med else None,
            "ac1": lag1(z),
            "cusum_episodes": ep_c,
            "cusum_far_24h": round(ep_c / (nb / 1440.0), 2),
            "ph_episodes": ep_p,
            "ph_far_24h": round(ep_p / (nb / 1440.0), 2),
            "half1_h_calibrated": h_cal,
            "half1_episodes_at_cal_h": ep_cal,
            "half2_episodes_at_cal_h": ep2,
            "half2_far_24h_at_cal_h": round(ep2 / ((nb - half) / 1440.0), 2),
            "positives": len(pos),
            "cusum_recall_h10_baseline_only": round(hit_in_base / len(pos), 4) if pos else None,
            "cusum_recall_h10_full_series": recall_at(full_c),
            "ph_recall_h10_full_series": recall_at(full_p),
            "cusum_alarm_minutes_outside_baseline": alarms_outside,
            "minutes_outside_baseline": outside_minutes,
            "cusum_alarm_rate_outside_per_hour": round(alarms_outside / (outside_minutes / 60.0), 3)
            if outside_minutes else None,
        }

    # KS dalam well: separuh awal lawan separuh akhir baseline
    within = {}
    for w, vals in clean_series.items():
        h = len(vals) // 2
        within[w] = ks_two_sample(vals[:h], vals[h:])

    # KS antar well (matriks)
    wells = sorted(clean_series)
    between = []
    for i in range(len(wells)):
        for j in range(i + 1, len(wells)):
            r = ks_two_sample(clean_series[wells[i]], clean_series[wells[j]])
            if r:
                r.update({"a": wells[i], "b": wells[j]})
                between.append(r)
    ds = [r["D"] for r in between]
    ps = [r["p_approx"] for r in between]

    def col(k):
        return [v[k] for v in per_well.values() if isinstance(v.get(k), (int, float))]

    summary = {
        "channel": CHANNEL,
        "n_wells_total": len(data),
        "n_wells_dipakai": len(per_well),
        "baseline_minutes_min": min(col("baseline_minutes")) if per_well else None,
        "baseline_minutes_median": round(st.median(col("baseline_minutes")), 1) if per_well else None,
        "baseline_minutes_max": max(col("baseline_minutes")) if per_well else None,
        "cusum_far24_median": round(st.median(col("cusum_far_24h")), 2) if per_well else None,
        "cusum_far24_min": min(col("cusum_far_24h")) if per_well else None,
        "cusum_far24_max": max(col("cusum_far_24h")) if per_well else None,
        "ph_far24_median": round(st.median(col("ph_far_24h")), 2) if per_well else None,
        "ph_far24_min": min(col("ph_far_24h")) if per_well else None,
        "ph_far24_max": max(col("ph_far_24h")) if per_well else None,
        "ac1_median": round(st.median(col("ac1")), 3) if col("ac1") else None,
        "ac1_min": min(col("ac1")) if col("ac1") else None,
        "ac1_max": max(col("ac1")) if col("ac1") else None,
        "wells_half2_bersih_pada_h_kalibrasi": sum(1 for v in per_well.values()
                                                   if v["half2_episodes_at_cal_h"] == 0),
        "ks_between_well_D_median": round(st.median(ds), 3) if ds else None,
        "ks_between_well_D_max": max(ds) if ds else None,
        "ks_between_well_D_min": min(ds) if ds else None,
        "ks_between_well_p_lt_0_05": sum(1 for p in ps if p < 0.05),
        "ks_between_well_pairs": len(between),
        "ks_within_well_D_median": round(st.median([v["D"] for v in within.values() if v]), 3) if within else None,
        "ks_within_well_p_lt_0_05": sum(1 for v in within.values() if v and v["p_approx"] < 0.05),
        "total_positives": sum(v["positives"] for v in per_well.values()),
    }

    out = {
        "meta": {
            "kartu": "t_56d8d11d RND-R5",
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sumber": SRC,
            "perintah": "python3 scratch/rnd_r5/measure_drift_v2.py",
            "parameter": {
                "cusum_k_sigma": K_SIGMA, "cusum_h_sigma": H_SIGMA,
                "ph_delta_sigma": PH_DELTA, "ph_lambda_sigma": PH_LAMBDA,
                "min_baseline_minutes": MIN_BASE, "merge_gap_minutes": MERGE_GAP,
                "horizon_minutes": HORIZON, "max_ks_sampel": MAX_KS,
            },
            "catatan_satuan": "ts_bin = indeks menit (epoch menit); selisih 1 = 1 menit. "
                             "Bukti: scratch/rnd_r5/grid_structure.json.",
            "catatan_far": "FAR = episode alarm pada baseline bersih nyata per 24 jam baseline, "
                           "bukan ARL Gaussian iid. Episode digabung bila jarak <= 30 menit.",
        },
        "summary": summary,
        "per_well": per_well,
        "ks_within_well": within,
        "ks_between_well": between,
        "skipped": skipped,
    }
    os.makedirs(OUTDIR, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    print(json.dumps(summary, indent=1, ensure_ascii=False))
    print(json.dumps(per_well, indent=1, ensure_ascii=False))
    print("KS within", json.dumps(within, ensure_ascii=False))
    print("KS between D:", [round(r["D"], 3) for r in between])
    print("SKIPPED", json.dumps(skipped, ensure_ascii=False))


if __name__ == "__main__":
    main()
