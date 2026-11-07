#!/usr/bin/env python3
"""RND-E4b — audit label hyd pada beberapa ambang z.

Menjawab permintaan R7 §9.3 dan instruksi kerja butir 4/5:
berapa banyak positif yang bertahan bila ambang digeser dari |z|>2 ke 2,5 dan 3,
dan apakah onset (rising edge) masih muncul.

Resep identik dengan code/rnd_rule_baseline.py dan code/v9_d1_03_rig_datasets.py:55-75
(qcut TFLO 10 bin, median/MAD per bin, z = (SPPA - med) / (1.4826 * MAD)).
"""
import json
import numpy as np
import pandas as pd

BINSD = "/mnt/d/Capstone 1(v2)/scratch/v9_d1/bins"
OUT = "/mnt/d/Capstone 1(v2)/scratch/rnd/e4/e4_audit_label.json"
WELLS = ["F-10", "F-12", "F-14", "F-15A", "F-15_S", "F-5", "F-7", "F-9", "F-9_A"]
THRESH = [2.0, 2.5, 3.0]


def z_series(well):
    b = pd.read_csv(f"{BINSD}/{well}.csv.gz")
    d = b.dropna(subset=["SPPA_mean", "TFLO_mean"]).copy()
    d = d[d["TFLO_mean"] > 0]
    if len(d) < 50:
        return None
    try:
        d["qbin"] = pd.qcut(d["TFLO_mean"], 10, labels=False, duplicates="drop")
    except ValueError:
        d["qbin"] = 0
    med = d.groupby("qbin")["SPPA_mean"].transform("median")
    mad = d.groupby("qbin")["SPPA_mean"].transform(lambda s: (s - s.median()).abs().median())
    z = (d["SPPA_mean"] - med) / (1.4826 * mad.replace(0, np.nan))
    return z.dropna()


def edges(flags):
    """Rising edge: kejadian 0 -> 1. Ini definisi onset yang dipakai konsisten."""
    a = np.asarray(flags, dtype=int)
    if len(a) == 0:
        return 0
    return int(((a[1:] == 1) & (a[:-1] == 0)).sum() + (1 if a[0] == 1 else 0))


rows = []
for w in WELLS:
    z = z_series(w)
    if z is None:
        rows.append(dict(well=w, status="n_terlalu_kecil"))
        continue
    rec = dict(well=w, n_obs=int(len(z)),
               z_abs_p50=round(float(z.abs().median()), 4),
               z_abs_p99=round(float(z.abs().quantile(0.99)), 4))
    n2 = int((z.abs() > 2.0).sum())
    for t in THRESH:
        m = (z.abs() > t)
        n = int(m.sum())
        rec[f"n_pos_{t}"] = n
        rec[f"laju_{t}"] = round(n / len(z), 6)
        rec[f"onset_{t}"] = edges(m.to_numpy())
        rec[f"retensi_{t}"] = round(n / n2, 4) if n2 else None
    rows.append(rec)

ok = [r for r in rows if "n_pos_2.0" in r]
agg = {}
for t in THRESH:
    tot = sum(r[f"n_pos_{t}"] for r in ok)
    tobs = sum(r["n_obs"] for r in ok)
    agg[f"thr_{t}"] = dict(
        total_pos=tot, total_obs=tobs,
        laju=round(tot / tobs, 6),
        onset_total=sum(r[f"onset_{t}"] for r in ok),
        retensi_vs_2=round(tot / sum(r["n_pos_2.0"] for r in ok), 4),
    )

res = dict(
    deskripsi="Audit label hyd pada ambang |z| 2 / 2,5 / 3, resep sama dengan bins",
    well=WELLS, threshold=THRESH, per_well=rows, agregat=agg,
    catatan=("z ini juga dipakai CUSUM A2 sehingga label dan detektor berbagi sumber; "
             "hasil audit tidak bisa dipakai sebagai bukti kemampuan deteksi independen"),
)
json.dump(res, open(OUT, "w"), indent=2)

print("%-7s %8s %9s %9s %9s %9s" % ("well", "n_obs", "pos z2", "pos z2.5", "pos z3", "onset z2"))
for r in rows:
    if "n_pos_2.0" not in r:
        print(r["well"], r.get("status"))
        continue
    print("%-7s %8d %9d %9d %9d %9d" % (r["well"], r["n_obs"], r["n_pos_2.0"],
                                        r["n_pos_2.5"], r["n_pos_3.0"], r["onset_2.0"]))
print()
for t in THRESH:
    a = agg[f"thr_{t}"]
    print(f"thr {t}: total_pos={a['total_pos']} laju={a['laju']} onset={a['onset_total']} retensi={a['retensi_vs_2']}")
print("OUT", OUT)
