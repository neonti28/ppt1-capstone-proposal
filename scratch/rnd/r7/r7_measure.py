import sys, json
sys.path.insert(0, "code")
import numpy as np, pandas as pd
import rnd_e3_pilot as P

BASE = "/mnt/d/Capstone 1(v2)"
df = pd.read_csv(f"{BASE}/scratch/v9_d1/datasets/hyd_ki.csv.gz")
lowo = json.load(open(f"{BASE}/scratch/v9_d1/lowo_hyd_ki.json"))
folds = lowo["folds"]
W = 10

# ---------- A) baseline jujur: rule t0-1 dari bins (anom di ts-1) ----------
def bin_anom(well):
    b = pd.read_csv(f"{BASE}/scratch/v9_d1/bins/{well}.csv.gz")
    d = b.dropna(subset=["SPPA_mean", "TFLO_mean"]).copy()
    d = d[d["TFLO_mean"] > 0]
    anom = pd.Series(False, index=b.index)
    if len(d) >= 50:
        try:
            d["qbin"] = pd.qcut(d["TFLO_mean"], 10, labels=False, duplicates="drop")
        except ValueError:
            d["qbin"] = 0
        med = d.groupby("qbin")["SPPA_mean"].transform("median")
        mad = d.groupby("qbin")["SPPA_mean"].transform(lambda s: (s - s.median()).abs().median())
        z = (d["SPPA_mean"] - med) / (1.4826 * mad.replace(0, np.nan))
        anom.loc[d.index] = (z.abs() > 2).fillna(False)
    B = pd.DataFrame({"ts_bin": b["ts_bin"], "obs": b["SPPA_mean"].notna() & b["TFLO_mean"].notna(),
                      "anom": anom.values})
    return B.set_index("ts_bin")

rows = []
tot = {"rule": 0, "pers": 0, "hyb": 0}
for f in folds:
    w = f["test_well"]
    d = df[df["well"] == w].sort_values("ts_bin").reset_index(drop=True)
    y = d["y_hyd"].to_numpy(int)
    ts = d["ts_bin"].to_numpy(int)
    Bs = bin_anom(w)
    prev = Bs.reindex(ts - 1)
    rule = (prev["anom"].fillna(False).to_numpy() & prev["obs"].fillna(False).to_numpy()).astype(int)
    pers = np.where(d["valid_prev_hyd"].to_numpy(int) == 1, d["y_prev_hyd"].to_numpy(int), 0)
    hyb = (rule & pers).astype(int)
    # proxy yang dipakai E3: label baris sebelumnya (jendela tumpang tindih ke masa depan)
    rule_lag = np.concatenate([[0], y[:-1]])
    hyb_px = (rule_lag & pers).astype(int)
    for nama, pred in (("rule_t0m1", rule), ("persistence", pers),
                       ("hybrid_jujur", hyb), ("hybrid_proxy_E3", hyb_px)):
        m = P.op_metrics(y, pred)
        rows.append(dict(well=w, model=nama, fp=m["fp"], tp=m["tp"], far24=m["far_per_24h"],
                         prec=m["precision"], rec=m["recall"], n_neg=m["n_neg"],
                         gateA=bool(m["far_per_24h"] is not None and m["far_per_24h"] <= 6)))
    for k, v in (("rule", rule), ("pers", pers), ("hyb", hyb)):
        tot[k] += int(((v == 1) & (y == 0)).sum())

t = pd.DataFrame(rows)
print("=== A. BASELINE: rule t0-1 jujur vs proksi E3 (FP per well) ===")
piv = t.pivot(index="well", columns="model", values=["fp", "far24", "prec", "rec", "gateA"])
print(piv.round(4).to_string())
print("\nTOTAL FP  rule_t0m1:", tot["rule"], " persistence:", tot["pers"], " hybrid_jujur:", tot["hyb"])
print("terbit (E2/E_RULE): rule 2091, hybrid 927")
print("hybrid_jujur FP:", t[t.model == 'hybrid_jujur'].fp.sum(),
      " hybrid_proxy_E3 FP:", t[t.model == 'hybrid_proxy_E3'].fp.sum())
print("gateA lolos: rule_t0m1", int(t[t.model == 'rule_t0m1'].gateA.sum()),
      "| hybrid_jujur", int(t[t.model == 'hybrid_jujur'].gateA.sum()),
      "| hybrid_proxy_E3", int(t[t.model == 'hybrid_proxy_E3'].gateA.sum()),
      "| persistence", int(t[t.model == 'persistence'].gateA.sum()))

# ---------- B) A2: penghitungan ganda alarm jendela 10 menit ----------
print("\n=== B. A2 CUSUM h=30 reset=True: baris FP vs episode alarm ===")
out = []
for f in folds:
    w = f["test_well"]
    d = df[df["well"] == w].sort_values("ts_bin").reset_index(drop=True)
    y = d["y_hyd"].to_numpy(int)
    zz = P.build_z(w)
    al = P.cusum_alarms(zz["z"].to_numpy(), 30.0, reset=True)
    zts = zz["ts_bin"].to_numpy()
    lab = d["lab_ts"].to_numpy()
    flagged = np.zeros(len(d), dtype=int)
    ep = np.zeros(len(d), dtype=int)   # episode: alarm pertama dalam jendela saja
    for i, t0 in enumerate(lab):
        lo = np.searchsorted(zts, t0 - W, side="left")
        hi = np.searchsorted(zts, t0, side="left")
        if hi > lo:
            seg = al[lo:hi]
            flagged[i] = int(seg.max())
            nz = np.flatnonzero(seg)
            if len(nz):
                ep[i] = 1 if nz[0] == 0 else int(seg[nz[0]] and (not seg[nz[0]-1]))
    m_row = P.op_metrics(y, flagged)
    m_ep = P.op_metrics(y, ep)
    n_alarm_min = int(al.sum())
    out.append(dict(well=w, alarm_menit=n_alarm_min, baris_menyala=int(flagged.sum()),
                    fp_baris=m_row["fp"], far24_baris=m_row["far_per_24h"],
                    fp_episode=m_ep["fp"], far24_episode=m_ep["far_per_24h"],
                    rasio=(m_row["far_per_24h"] / m_ep["far_per_24h"]) if m_ep["far_per_24h"] else None,
                    gateA_baris=m_row["far_per_24h"] <= 6, gateA_episode=m_ep["far_per_24h"] <= 6))
b = pd.DataFrame(out)
print(b.round(3).to_string())
print("\nmedian FAR24 baris:", round(float(b.far24_baris.median()), 3),
      "| median FAR24 episode:", round(float(b.far24_episode.median()), 3),
      "| median rasio:", round(float(b.rasio.median()), 3))
print("gateA lolos baris:", int(b.gateA_baris.sum()), "| episode:", int(b.gateA_episode.sum()))

json.dump(dict(baseline=t.to_dict("records"), total_fp=tot, cusum=b.to_dict("records")),
          open(f"{BASE}/scratch/rnd/r7/r7_measure.json", "w"), indent=2)
