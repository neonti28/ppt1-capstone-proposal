"""S4-B: durasi kejadian (jam henti) dari labels_curated_v2.csv. READ-ONLY.

Keluaran: scratch/rnd/s4/labels_duration.json
"""
import os, json
from datetime import datetime
from collections import Counter, defaultdict
import pandas as pd

ROOT = "/mnt/d/Capstone 1(v2)"
SRC = os.path.join(ROOT, "data/volve/labels_curated_v2.csv")
OUT = os.path.join(ROOT, "scratch/rnd/s4/labels_duration.json")

df = pd.read_csv(SRC, low_memory=False)
res = {
    "sumber": {"path": SRC, "bytes": os.path.getsize(SRC), "baris": int(len(df)), "kolom": list(df.columns)},
}

t0 = pd.to_datetime(df["act_start"], errors="coerce", format="ISO8601", utc=True)
t1 = pd.to_datetime(df["act_end"], errors="coerce", format="ISO8601", utc=True)
ok = t0.notna() & t1.notna()
dur_h = (t1 - t0).dt.total_seconds() / 3600.0

res["n_baris"] = int(len(df))
res["n_durasi_valid"] = int(ok.sum())
res["n_tanpa_waktu"] = int((~ok).sum())
neg = ok & (dur_h < 0)
zero = ok & (dur_h == 0)
res["n_durasi_negatif"] = int(neg.sum())
res["n_durasi_nol"] = int(zero.sum())

d = dur_h[ok & (dur_h >= 0)]
res["durasi_jam"] = {
    "n": int(len(d)),
    "sum": round(float(d.sum()), 3),
    "mean": round(float(d.mean()), 4),
    "median": round(float(d.median()), 4),
    "p25": round(float(d.quantile(0.25)), 4),
    "p75": round(float(d.quantile(0.75)), 4),
    "p90": round(float(d.quantile(0.90)), 4),
    "max": round(float(d.max()), 4),
    "min": round(float(d.min()), 4),
}
# distribusi per kelas durasi
bins = [0, 0.25, 0.5, 1, 2, 4, 8, 24, 1e9]
labels = ["0-15m", "15-30m", "30-60m", "1-2j", "2-4j", "4-8j", "8-24j", ">24j"]
cats = pd.cut(d, bins=bins, labels=labels, right=False)
res["distribusi_durasi"] = {str(k): int(v) for k, v in cats.value_counts().reindex(labels).items()}

def agg_by(col):
    out = {}
    for key, g in df[ok & (dur_h >= 0)].assign(_d=d).groupby(col):
        v = g["_d"]
        out[str(key)] = {"n": int(len(v)), "sum_jam": round(float(v.sum()), 3),
                         "median_jam": round(float(v.median()), 4),
                         "p90_jam": round(float(v.quantile(0.90)), 4)}
    return dict(sorted(out.items(), key=lambda kv: -kv[1]["sum_jam"]))

for col in ["category", "state_detail", "source_code", "wellbore", "outcome", "component"]:
    if col in df.columns:
        res["per_" + col] = agg_by(col)

# wellbore dengan n kecil tetap dilaporkan apa adanya
res["n_wellbore"] = int(df["wellbore"].nunique())

# cakupan 7 fold yang dipakai engine
FOLD2LABEL = {
    "F-14": "NO 15/9-F-14", "F-7": "NO 15/9-F-7", "F-14b": "NO 15/9-F-14",
    "F-15A": "NO 15/9-F-15 A", "F-15_S": "NO 15/9-F-15", "F-5": "NO 15/9-F-5",
    "F-9": "NO 15/9-F-9", "F-9_A": "NO 15/9-F-9 A",
}
fold_wells = ["NO 15/9-F-14", "NO 15/9-F-15 A", "NO 15/9-F-15", "NO 15/9-F-5", "NO 15/9-F-7", "NO 15/9-F-9", "NO 15/9-F-9 A"]
sub = df[ok & (dur_h >= 0) & df["wellbore"].isin(fold_wells)].assign(_d=d)
res["tujuh_well_engine"] = {
    "well": fold_wells,
    "n_kejadian": int(len(sub)),
    "sum_jam": round(float(sub["_d"].sum()), 3),
    "median_jam": round(float(sub["_d"].median()), 4),
    "p90_jam": round(float(sub["_d"].quantile(0.90)), 4),
}

# kategori kegagalan peralatan saja.
# CATATAN BUG (diuji, bukan diduga): pada pandas 3.1, `.assign()` pada DataFrame hasil
# filter kosong MELEBARKAN baris menjadi sepanjang Series yang di-assign, sehingga
# hasilnya 884 baris NaN. Karena itu di sini dipakai mask eksplisit + .loc + .copy().
m_eq = ok & (dur_h >= 0) & (df["state_detail"] == "equipment failure")
eq = df.loc[m_eq].copy()
eq["_d"] = dur_h[m_eq]
res["equipment_failure_state_detail"] = {
    "definisi": "state_detail == 'equipment failure' (bukan kolom category)",
    "n": int(len(eq)),
    "sum_jam": round(float(eq["_d"].sum()), 3),
    "median_jam": round(float(eq["_d"].median()), 4) if len(eq) else None,
    "p90_jam": round(float(eq["_d"].quantile(0.90)), 4) if len(eq) else None,
    "max_jam": round(float(eq["_d"].max()), 4) if len(eq) else None,
    "per_wellbore": {str(k): {"n": int(len(v)), "sum_jam": round(float(v["_d"].sum()), 3)}
                     for k, v in eq.groupby("wellbore")} if len(eq) else {},
}

# subset "kegagalan beralasan" = kategori selain routine_no_failure_evidence
m_fail = ok & (dur_h >= 0) & (df["category"] != "routine_no_failure_evidence")
fa = df.loc[m_fail].copy()
fa["_d"] = dur_h[m_fail]
res["kegagalan_beralasan"] = {
    "definisi": "category != routine_no_failure_evidence",
    "n": int(len(fa)),
    "sum_jam": round(float(fa["_d"].sum()), 3),
    "median_jam": round(float(fa["_d"].median()), 4),
    "p90_jam": round(float(fa["_d"].quantile(0.90)), 4),
    "per_kategori": {str(k): {"n": int(len(v)), "sum_jam": round(float(v["_d"].sum()), 3),
                              "median_jam": round(float(v["_d"].median()), 4)}
                     for k, v in fa.groupby("category")},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
print("WROTE", OUT, os.path.getsize(OUT))
print("baris", res["n_baris"], "valid", res["n_durasi_valid"], "nol", res["n_durasi_nol"], "neg", res["n_durasi_negatif"])
print("durasi:", res["durasi_jam"])
print("distribusi:", res["distribusi_durasi"])
print("kategori teratas:", list(res["per_category"].items())[:6])
print("equipment_failure(state_detail):", res["equipment_failure_state_detail"]["n"], res["equipment_failure_state_detail"]["sum_jam"])
print("kegagalan_beralasan:", res["kegagalan_beralasan"]["n"], res["kegagalan_beralasan"]["sum_jam"])
print("tujuh well:", res["tujuh_well_engine"])
