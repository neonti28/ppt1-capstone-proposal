import sys, json
sys.path.insert(0, "code")
import numpy as np, pandas as pd
import rnd_e3_pilot as P

BASE = "/mnt/d/Capstone 1(v2)"
df = pd.read_csv(f"{BASE}/scratch/v9_d1/datasets/hyd_ki.csv.gz")
folds = json.load(open(f"{BASE}/scratch/v9_d1/lowo_hyd_ki.json"))["folds"]

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
    return pd.DataFrame({"ts_bin": b["ts_bin"], "obs": b["SPPA_mean"].notna() & b["TFLO_mean"].notna(),
                         "anom": anom.values}).set_index("ts_bin")

rows = []
for f in folds:
    w = f["test_well"]
    d = df[df["well"] == w].sort_values("ts_bin").reset_index(drop=True)
    y = d["y_hyd"].to_numpy(int); ts = d["ts_bin"].to_numpy(int)
    Bs = bin_anom(w); prev = Bs.reindex(ts - 1)
    rule = (prev["anom"].fillna(False).to_numpy() & prev["obs"].fillna(False).to_numpy()).astype(int)
    pers = np.where(d["valid_prev_hyd"].to_numpy(int) == 1, d["y_prev_hyd"].to_numpy(int), 0)
    hyb = (rule & pers).astype(int)
    det = P.detection_stats(y, hyb)
    rows.append(dict(well=w, delay_median=det["delay_median_min"], onsets=det["onsets"],
                     det_any=det["detected_any"], det_H10=det["detected_within_H10"],
                     pct_H10=det["pct_detected"]))
t = pd.DataFrame(rows)
print(t.to_string(index=False))
print("\nmedian delay antar well:", float(t.delay_median.median()),
      "| rentang:", float(t.delay_median.min()), "-", float(t.delay_median.max()))
json.dump(t.to_dict("records"), open(f"{BASE}/scratch/rnd/r7/r7_delay.json", "w"), indent=2)
