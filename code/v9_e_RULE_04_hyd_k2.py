#!/usr/bin/env python3
"""V9-E_RULE 04 — baseline S9 kelas hyd-K-ii (prediksi kick/loss proxy, H=10).

Data & label VERBATIM resep V8-E_hyd claim2 (f9a_time.csv, satu wellbore F-9 A):
  V_pit = mean(13 kolom pit, sentinel [-5,150]->NaN); r10 = V_pit(t)-V_pit(t-10);
  z = (r10-med)/(1.4826*MAD); kick z>+2 sustain>=5mnt; loss z<-2; merge <30mnt;
  syarat sirkulasi Flow Pumps>=500; positif = [t_e-10,t_e); jendela dalam blok
  (+30 mnt pasca-onset) DibuANG; split temporal 70/30 (identik V8).
Baseline (S9):
  - prevalence-random (seed42) + prev_test analitik + plafon 1/prev.
  - selalu-negatif ("onset persistence" istilah V8): recall=0; AUPRC=prev.
  - rule z-pit (sistem hari-ini): alarm = menit run |z|>2 (≥5 mnt, syarat
    sirkulasi). Pada baris evaluasi (blok dibuang) alarm=0 BY CONSTRUCTION;
    TLead terukur = 0 (alarm tepat DI onset) -> relevan utk B3, bukan TLead.
Catatan: Fisher/Pearson literal = milik E_STAT (PM1 §4.4); RF K-ii = E_ML.
"""
import json
import os
import time
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score

import sys
sys.path.insert(0, "/mnt/d/Capstone 1(v2)/code")
from v9_e_RULE_01_status import SEED, OUT, binary_metrics, fold_stats, log, log_lines  # noqa: E402

F = "/home/neonti/.hermes/cache/scratch/f9a_time.csv"
REF = "/mnt/d/Capstone 1(v2)/scratch/v8_e_hyd/claim2_results.json"
H = 10
EPISODE_GAP = 30
SUSTAIN = 5
QMIN = 500.0


def main():
    t0 = time.time()
    cols = pd.read_csv(F, nrows=0).columns.tolist()
    pit_cols = [c for c in cols if "MudPit Volume Average" in c]
    base = ["Time s", "Tank volume (active) m3", "Flow Pumps L/min",
            "Mud Flow In L/min"]
    use = list(dict.fromkeys(pit_cols + base))
    pieces = []
    for ch in pd.read_csv(F, usecols=use, chunksize=50_000):
        pieces.append(ch.astype({c: "float32" for c in use if c != "Time s"}))
    d = pd.concat(pieces, ignore_index=True)
    del pieces
    t = pd.to_datetime(d["Time s"], utc=True, errors="coerce")
    d = d[t.notna()].copy()
    t = t[t.notna()]
    d = d.assign(_t=t).set_index("_t").sort_index()
    P = d[pit_cols].apply(pd.to_numeric, errors="coerce")
    P = P.where((P >= -5) & (P <= 150))
    d["_pit_total"] = P.mean(axis=1)
    num = d[base[1:]].copy()
    for c in base[1:]:
        num[c] = pd.to_numeric(num[c], errors="coerce")
    num["Tank volume (active) m3"] = num["Tank volume (active) m3"].where(
        num["Tank volume (active) m3"].between(-10, 250))
    g = num.resample("1min").median()
    g["_pit_total"] = d["_pit_total"].resample("1min").median()

    r10 = g["_pit_total"] - g["_pit_total"].shift(10)
    med = r10.median()
    mad = (r10 - med).abs().median()
    scale = 1.4826 * mad if mad > 0 else r10.std()
    z = (r10 - med) / scale
    circ = g["Flow Pumps L/min"].fillna(0) >= QMIN
    z_c = z.where(circ)

    def runs(mask):
        idx = np.flatnonzero(mask.to_numpy())
        out = []
        if len(idx):
            s = p = idx[0]
            for i in idx[1:]:
                if i == p + 1:
                    p = i
                else:
                    out.append((s, p)); s = p = i
            out.append((s, p))
        return out

    onsets = []
    for sign, nm in ((+1, "kick"), (-1, "loss")):
        m = (z_c * sign) > 2
        for a, b in runs(m):
            if b - a + 1 >= SUSTAIN:
                onsets.append((a, nm, b))
    onsets.sort()
    merged = []
    for a, nm, b in onsets:
        if merged and a - merged[-1][0] < EPISODE_GAP:
            continue
        merged.append((a, nm, b))

    N = len(g)
    y = np.zeros(N, int)
    inblock = np.zeros(N, bool)
    for a, nm, b in merged:
        y[max(a - H, 0):a] = 1
        inblock[a:min(a + EPISODE_GAP, N)] = True
    evaluable = ~inblock

    # split temporal 70/30 identik V8
    split = int(N * 0.7)
    res = {"meta": {"task": "V9-E_RULE 04 hyd-K-ii baselines",
                    "seed": SEED, "recipe": "VERBATIM V8-E_hyd claim2",
                    "n_grid": int(N), "split": split,
                    "n_episodes": len(merged),
                    "generated_at": time.strftime("%Y-%m-%d %H:%M:%S")},
           "test": {}}

    yte = y[split:]
    ev_te = evaluable[split:]
    n, pos, prev, underp = fold_stats(yte[ev_te])
    res["test"]["fold"] = dict(test_well="F-9_A(temporal-30%akhir)", n=n,
                               pos=pos, prev=prev, underpowered=underp)

    # prevalence-random
    rng = np.random.default_rng(SEED)
    s_rand = rng.uniform(0, 1, n)
    res["test"]["prevalence_random"] = dict(
        auprc_emp=float(average_precision_score(yte[ev_te], s_rand)),
        prev_analytic=prev, plafon=(1.0 / prev) if prev else None)

    # selalu-negatif ("onset persistence" V8): skor konstan 0 -> AUPRC=prev
    pred0 = np.zeros(n, int)
    bn = binary_metrics(yte[ev_te], pred0)
    bn["auprc"] = float(average_precision_score(yte[ev_te], pred0))
    bn["note"] = "recall=0 BY CONSTRUCTION (V8: 'onset persistence' = selalu-negatif)"
    res["test"]["always_negative"] = bn

    # rule z-pit: alarm = menit run |z|>2 bersyarat-sirkulasi (>= SUSTAIN)
    alarm_all = np.zeros(N, bool)
    lag = []
    for a, nm, b in merged:
        alarm_all[a:b + 1] = True
        lag.append(0)  # alarm PERTAMA tepat di menit onset a (konstruksi rule)
    alarm_eval = alarm_all[split:][ev_te]
    res["test"]["rule_zpit"] = dict(
        n_alarm_in_evalrows=int(alarm_eval.sum()),
        fp_in_evalrows=int(alarm_eval.sum()),  # semua alarm di baris eval = FP(y=0)
        note="blok episode +30 mnt Dibuang dari baris evaluasi -> alarm rule=0 "
             "pada baris eval BY CONSTRUCTION; TLead=0 (deteksi saat-kejadian)",
        tlead_minutes=lag[:10], tlead_all_zero=bool(all(l == 0 for l in lag)),
        n_episode_minutes=int(alarm_all.sum()),
        b1_horizon_pct=0.0,  # alarm mulai DI t_e; horizon [t_e-10,t_e) tanpa alarm
        inspection_load=dict(
            episode_minutes_total=int(alarm_all.sum()),
            episode_minutes_test=int(alarm_all[split:].sum())))

    # cross-check prev_test vs V8
    try:
        v8 = json.load(open(REF))
        res["crosscheck_v8"] = dict(
            n_episodes_match=len(merged) == v8["label"]["n_episodes"],
            v8_n_episodes=v8["label"]["n_episodes"],
            v8_prev_test_cons=v8["conservative"]["prev_test"],
            v8_prev_test_flow=v8["with_flow_in"]["prev_test"],
            my_prev_test=prev)
    except Exception as e:
        res["crosscheck_v8"] = f"ERR {e}"

    log(f"hyd_k2: grid={N} episodes={len(merged)} prev_test={prev} "
        f"rand={res['test']['prevalence_random']['auprc_emp']} "
        f"zpit_alarms_eval={res['test']['rule_zpit']['n_alarm_in_evalrows']} "
        f"xcheck={res.get('crosscheck_v8')}")
    path = f"{OUT}/v9_e_RULE_04_hyd_k2_results.json"
    json.dump(res, open(path, "w"), indent=1, allow_nan=False)
    open(f"{OUT}/v9_e_RULE_04_run_log.txt", "w").write(
        "\n".join(log_lines) + "\n")
    log(f"-> {path} ({round(time.time() - t0, 1)} s)")


if __name__ == "__main__":
    main()
