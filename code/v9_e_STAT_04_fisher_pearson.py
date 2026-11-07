#!/usr/bin/env python3
"""V9-E_STAT 04 — baseline hyd K-ii: Fisher/Pearson literal (R1 §3.5 butir 7 / §4.5 H1).

Status FlowOut (TES PEMBEDA, probe_03_flow.py, sesi ini):
  4 kolom flow di F-9A time.csv -> 'Flow Pumps' 345442 nn, 'Mud Flow In' 83565,
  'TFLO30s' 64757, 'FLOW-TRPM' 34115; korelasi PEARSON antar mereka r = 0.995-1.000
  -> SEMUA mewakili aliran MASUK; TIDAK ada kanal FlowOut di F-9A.
  => Fisher/Pearson literal dgn (FlowIn - FlowOut) TIDAK DAPAT dijalankan literal.
  VARIAN TERDOKUMENTASI (change-control, dijalankan + dilaporkan terpisah):
  imbalance_proxy = dV_active/dt dari 'Tank volume (active) m3' (neraca permukaan
  aktif: dV_active/dt = FlowIn - FlowOut bila tak ada gain/loss lain) ->
  r_t = Pearson(imbalance_proxy, dV_pit) per jendela 30 mnt.
  RISIKO SIRKULARITAS: tank aktif bisa diturunkan dari pit yang sama -> r bisa
  mekanis tinggi; DILAPORKAN eksplisit, bukan disembunyikan.

Label K-ii (resep literal V8-E_hyd claim2 pre-declarations):
  grid 1 mnt (median sampel/menit); V_pit = mean(13 kolom pit, sentinel di luar
  [-5,150] -> NaN); r10(t) = V_pit(t) - V_pit(t-10); z = (r10 - med)/(1.4826*MAD);
  episode |z|>2 berkelanjutan >=5 mnt (gain z>+2 / loss z<-2), merge onset <30 mnt,
  syarat sirkulasi Flow Pumps >= 500 L/min saat onset; jendela [t_e-10, t_e) = positif;
  jendela dalam episode (+30 mnt pasca-onset) Dibuang; split temporal 70/30.

Detector literal (R1): z' = atanh(r) Fisher; baseline rolling 60 mnt (med+MAD);
  skor = |z'_t - med_baseline| / (1.4826*MAD_baseline); alarm = skor >= q95 TRAIN
  ATAU pergantian tanda r vs baseline (dilaporkan terpisah). Ambang q95 TIDAK
  dioptimasi pasca-hasil.

Baseline relevan (R1 §4.1 K-ii): prevalence-random; rule z-pit (TLead=0, sistem
  hari-ini). Fisher/Pearson literal = ENGINE yang dinilai di sini.
Single wellbore F-9A -> 1 fold temporal (bukan LOWO; alasan: pit hanya F-9A).

Output (S6): scratch/v9_e_stat/v9_e_stat_04_fisher_pearson_RESULTS.json + log.
"""
import json, os, time
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score

SEED = 42
H = 10
Q95 = 0.95
EP_MIN = 5          # menit sustain |z|>2
MERGE_MIN = 30      # merge onset <30 mnt
CIRC_MIN = 500.0    # L/min syarat sirkulasi
WIN_R = 30          # jendela korelasi (menit)
BASE_R = 60         # jendela baseline Fisher-z (menit)
SENT_LO, SENT_HI = -5.0, 150.0
F = "/mnt/d/Capstone 1(v2)/data/witsml/Norway-NA-15_47_9-F-9 A time.csv"
OUT = "/mnt/d/Capstone 1(v2)/scratch/v9_e_stat"
os.makedirs(OUT, exist_ok=True)
LOGP = f"{OUT}/v9_e_stat_04_run_log.txt"
log_lines = []


def log(m):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {m}"
    print(line, flush=True)
    log_lines.append(line)


def block_bootstrap_ci(y, score, n_boot=1000, block=60, seed=SEED):
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
    return [round(float(np.percentile(vals, 2.5)), 4),
            round(float(np.percentile(vals, 97.5)), 4)]


def main():
    t0 = time.time()
    cols = pd.read_csv(F, nrows=0).columns.tolist()
    pit = [c for c in cols if "MudPit Volume Average" in c]
    use = (["Time s", "Tank volume (active) m3", "Flow Pumps L/min"] + pit)
    pieces = []
    for ch in pd.read_csv(F, usecols=use, chunksize=50_000):
        pieces.append(ch.astype({c: "float32" for c in use if c != "Time s"}))
    d = pd.concat(pieces, ignore_index=True); del pieces
    t = pd.to_datetime(d["Time s"], utc=True, errors="coerce")
    d = d[t.notna()].copy(); t = t[t.notna()]
    d = d.assign(_t=t).set_index("_t").sort_index()
    d = d.drop(columns=["Time s"])  # kolom teks datetime, bukan numerik
    log(f"raw rows={len(d)} pit_cols={len(pit)}")

    # sentinel pit (mentah, level baris — resep V8)
    P = d[pit].apply(pd.to_numeric, errors="coerce")
    P = P.where((P >= -5) & (P <= 150))
    d["_pit_total"] = P.mean(axis=1)
    v_act = d["Tank volume (active) m3"].where(
        d["Tank volume (active) m3"].between(-10, 250))
    flowr = d["Flow Pumps L/min"].where(d["Flow Pumps L/min"].abs() < 1e5)

    # grid 1 menit median
    g = pd.DataFrame({
        "_pit_total": d["_pit_total"].resample("1min").median(),
        "_v_act": v_act.resample("1min").median(),
        "_flow": flowr.resample("1min").median(),
    })
    v_pit = g["_pit_total"]
    v_act = g["_v_act"]
    flow = g["_flow"]
    log(f"grid={len(g)} v_pit nonnull={int(v_pit.notna().sum())} "
        f"v_act={int(v_act.notna().sum())} flow={int(flow.notna().sum())}")

    # ---- LABEL K-ii (resep LITERAL V8-E_hyd claim2) ----
    r10 = v_pit - v_pit.shift(10)
    med = r10.median(); mad = (r10 - med).abs().median()
    scale = 1.4826 * mad if mad > 0 else r10.std()
    z = (r10 - med) / scale
    circ = flow.fillna(0) >= 500.0
    z_c = z.where(circ)                       # sirkulasi WAJIB di tiap menit run

    def runs_of(mask):
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
        for a, b in runs_of(m):
            if b - a + 1 >= 5:
                onsets.append((a, nm))
    onsets.sort()
    merged = []                               # merge: drop onset <30 mnt dr sebelumnya
    for a, nm in onsets:
        if merged and a - merged[-1][0] < 30:
            continue
        merged.append((a, nm))
    log(f"LABEL: episodes={len(merged)} "
        f"kick={sum(1 for _, n in merged if n == 'kick')} "
        f"loss={sum(1 for _, n in merged if n == 'loss')}")

    N = len(g)
    y = np.zeros(N, int)
    in_ep = np.zeros(N, bool)
    for a, nm in merged:
        y[max(a - 10, 0):a] = 1
        in_ep[a:min(a + 30, N)] = True
    evaluable = ~in_ep
    scorable = [g.index[a] for a, _ in merged]
    log(f"pos_windows={int(y.sum())} evaluable={int(evaluable.sum())}")

    # ---- DETECTOR Fisher/Pearson literal (variance imbalance_proxy) ----
    dv_pit = v_pit - v_pit.shift(1)
    dv_act = v_act - v_act.shift(1)
    r_t = dv_pit.rolling(WIN_R).corr(dv_act)      # Pearson per jendela 30 mnt
    zprime = np.arctanh(r_t.clip(-0.999999, 0.999999))
    b_med = zprime.rolling(BASE_R, min_periods=20).median().shift(1)
    b_mad = (zprime - b_med).abs().rolling(BASE_R, min_periods=20).median().shift(1)
    score = ((zprime - b_med) / (1.4826 * b_mad + 1e-12)).abs()
    sign_flip = ((np.sign(r_t) != np.sign(r_t.rolling(BASE_R, min_periods=20)
                                            .median().shift(1))) &
                 r_t.notna() & b_med.notna())
    log(f"score finite={int(np.isfinite(score).sum())} "
        f"sign_flip={int(sign_flip.sum())}")

    # ---- split temporal 70/30 (index, resep V8) + ambang q95 train ----
    split = int(N * 0.7)
    split_time = g.index[split]
    pos = np.arange(N)
    sc_finite = np.isfinite(score.to_numpy())
    tr_m = (pos < split) & evaluable & sc_finite
    te_m = (pos >= split) & evaluable
    thr = float(pd.Series(score.to_numpy()[tr_m]).quantile(Q95))
    log(f"split_idx={split} time={split_time} thr_q95={thr:.4f} "
        f"train_n={int(tr_m.sum())} test_n={int(te_m.sum())} "
        f"pos_test={int(y[te_m].sum())}")

    yt = y[te_m].astype(int)
    st = np.nan_to_num(score.to_numpy()[te_m], nan=0.0)
    prev = float(yt.mean()) if len(yt) else None
    auprc = (float(average_precision_score(yt, st)) if (yt.sum() > 0 and
             (yt == 0).sum() > 0) else None)
    ci = block_bootstrap_ci(yt, st) if auprc else None
    pred = np.nan_to_num(score.to_numpy()[te_m], nan=-np.inf) >= thr
    tp = int((pred & (yt == 1)).sum()); fp = int((pred & (yt == 0)).sum())
    fn = int((~pred & (yt == 1)).sum())
    P = tp / (tp + fp) if (tp + fp) else None
    R = tp / (tp + fn) if (tp + fn) else None
    jam_neg = int((yt == 0).sum()) / 60.0
    far24 = (fp / jam_neg * 24) if jam_neg else None

    # onset-level (B1/TLead): onset uji = posisi a pada [split, N)
    scv = score.to_numpy()
    alarm_all = np.nan_to_num(scv, nan=-np.inf) >= thr
    eps_test = [a for a, _ in merged if split <= a < N]
    det, leads = 0, []
    for a in eps_test:
        seg = np.zeros(N, bool)
        seg[max(a - H, 0):a] = True
        seg &= evaluable
        nz = np.flatnonzero(alarm_all & seg)
        if len(nz):
            det += 1
            leads.append(float(a - nz[0]))

    # baseline rule z-pit: alarm HANYA di menit onset a (DI LUAR horizon [a-10,a))
    # -> det_rule = 0 by construction (TLead=0 = deteksi simultan, bukan prediksi-dini)
    det_rule = 0
    out = {
        "engine": "hyd_Kii_fisher_pearson_literal",
        "claim_task": "baseline prediksi kegagalan hidrolik (kick/loss proxy, H=10 mnt)",
        "jenis_engine": "statistical (korelasi Pearson + Fisher z-transform)",
        "seed": SEED,
        "flowout_status": {
            "verdict": "FlowOut TIDAK TERSEDIA di F-9A — literal (FlowIn-FlowOut) "
                       "TIDAK DIJALANKAN",
            "evidence": "probe_03_flow.py: korelasi 4 kolom flow satu sama lain "
                        "r=0.995-1.000 (semua aliran masuk); kolom out-flow tidak ada",
            "variant_run": "imbalance_proxy = dV_active/dt (neraca tank aktif), "
                           "dijalankan & dilaporkan terpisah",
            "circularity_risk": "tank aktif bisa diturunkan dari pit sama -> r bisa "
                                "mekanis tinggi; angka variant BUKAN bukti keunggulan "
                                "metode literal penuh",
        },
        "label_Kii": {
            "recipe": "V8-E_hyd claim2 pre-declarations (median 1-menit, 13 pit cols, "
                      "sentinel[-5,150], r10, z=0.6745-scaled, |z|>2 sustain>=5, "
                      "merge<30, FlowPumps>=500)",
            "n_pit_cols": len(pit),
            "n_episodes": len(merged),
            "n_kick": sum(1 for _, n in merged if n == "kick"),
            "n_loss": sum(1 for _, n in merged if n == "loss"),
            "n_onsets_total": len(merged),
            "pos_windows": int(y.sum()),
            "evaluable_windows": int(evaluable.sum()),
            "n_grid": len(g),
        },
        "split": {"type": "temporal 70/30 index (single wellbore F-9A, resep V8)",
                  "split_time": str(split_time), "thr_q95_train": round(thr, 5),
                  "train_n": int(tr_m.sum()), "test_n": int(te_m.sum())},
        "engine_fisher_pearson_variant": {
            "r_definition": f"Pearson(dV_active/dt, dV_pit) jendela {WIN_R} mnt; "
                            f"skor = |z'_t - med_base|/(1.4826*MAD_base), "
                            f"z'=atanh(r), baseline {BASE_R} mnt shift(1)",
            "n_test": int(len(yt)), "n_pos": int(yt.sum()),
            "prev": round(prev, 6) if prev is not None else None,
            "underpowered": bool((yt.sum() if len(yt) else 0) < 30),
            "auprc": round(auprc, 4) if auprc is not None else None,
            "ci95_auprc": ci,
            "lift": (round(auprc / prev, 3) if (auprc and prev) else None),
            "lift_ceiling_1_over_prev": (round(1 / prev, 3) if prev else None),
            "dB_vs_prevalence_random": (round(auprc - prev, 4)
                                        if (auprc is not None and prev) else None),
            "op_q95": dict(tp=tp, fp=fp, fn=fn, precision=P, recall=R,
                           far_per_neg_hour=(fp / jam_neg if jam_neg else None),
                           far_per_24h_neg=far24),
            "onset_level": {"onsets_test": len(eps_test), "detected_at_H": det,
                            "B1_recall_at_H": (det / len(eps_test)
                                               if eps_test else None),
                            "TLead_median_min": (float(np.median(leads))
                                                 if leads else None),
                            "TLead_IQR_min": ([float(np.percentile(leads, 25)),
                                               float(np.percentile(leads, 75))]
                                              if leads else None)},
            "sign_flip_windows": int(sign_flip.sum()),
        },
        "baseline_prevalence_random": {
            "auprc_equals_prev": round(prev, 6) if prev is not None else None,
            "lift_by_definition": 1.0, "type": "analitik"},
        "baseline_rule_zpit": {
            "definition": "alarm pada menit pertama episode z-pit (sistem hari-ini)",
            "onsets_test": len(eps_test), "detected_at_H": det_rule,
            "note": "TLead=0 by construction: alarm DI t_e, di luar horizon "
                    "[t_e-10, t_e) -> B1 harapan 0 untuk klaim prediksi-dini",
        },
        "meta": {"elapsed_s": round(time.time() - t0, 1), "H_min": H, "q95": Q95,
                 "win_corr_min": WIN_R, "win_base_min": BASE_R},
    }
    json.dump(out, open(f"{OUT}/v9_e_stat_04_fisher_pearson_RESULTS.json", "w"),
              indent=1, default=str)
    open(LOGP, "w").write("\n".join(log_lines) + "\n")
    log("LABEL: " + json.dumps(out["label_Kii"], default=str))
    e = out["engine_fisher_pearson_variant"]
    log(f"ENGINE: auprc={e['auprc']} prev={e['prev']} lift={e['lift']} "
        f"P={e['op_q95']['precision']} R={e['op_q95']['recall']} "
        f"FAR24={e['op_q95']['far_per_24h_neg']} B1={e['onset_level']['B1_recall_at_H']} "
        f"TLead={e['onset_level']['TLead_median_min']}")
    log(f"DONE -> {OUT}/v9_e_stat_04_fisher_pearson_RESULTS.json")


if __name__ == "__main__":
    main()
