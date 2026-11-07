#!/usr/bin/env python3
"""S3a: pengukuran kelayakan bit_wear dari file, bukan dari ingatan.

Yang diukur:
 1. inventaris kolom dan pemindaian token (bit, run, time, cost, downtime, npt).
 2. jumlah record, well, sebaran label per well.
 3. spasi grid kedalaman (satuan baris, temuan E0 S-6).
 4. identitas bit dan run: dibuktikan ada atau tidak ada.
 5. sirkularitas label: rekonstruksi label dari MSE dan ROC_coef.
 6. ketersediaan waktu kalender dari data/volve/usrop_timestamped.csv.

Keluaran: scratch/rnd/s3/s3a_feasibility.json
"""
import json
import os

import numpy as np
import pandas as pd

BASE = "/mnt/d/Capstone 1(v2)"
USROP = f"{BASE}/data/USROP_labeled.csv"
TSUROP = f"{BASE}/data/volve/usrop_timestamped.csv"
OUT = f"{BASE}/scratch/rnd/s3/s3a_feasibility.json"

TOK_BIT = ("bitno", "bit_no", "bitrun", "bit_run", "bitid", "bit_id",
           "bit_number", "serial", "dull", "iaddc", "bha_no")
TOK_RUN = ("run", "runno", "run_no", "trip", "bha", "assembly")
TOK_TIME = ("time", "timestamp", "date", "hour", "minute", "second", "rul")
TOK_COST = ("cost", "downtime", "npt", "price", "usd", "opex", "rig_rate", "standby")


def norm(c):
    return "".join(ch.lower() if ch.isalnum() else "_" for ch in c)


def scan(cols, toks):
    """Cocokkan token identitas secara utuh, bukan substring bebas.

    Substring 'bit' akan menangkap 'Weight on Bit kkgf', sehingga pemindaian
    substring menghasilkan klaim identitas bit yang palsu. Karena itu token
    dicocokkan sebagai bagian nama yang dipisah garis bawah.
    """
    hit = {}
    for c in cols:
        parts = set(p for p in norm(c).split("_") if p)
        n = norm(c)
        for t in toks:
            if t in parts or t in n:
                hit.setdefault(t, []).append(c)
    return hit


def percentile_linear(vals, q):
    a = np.sort(np.asarray(vals, dtype=float))
    if len(a) == 0:
        return None
    pos = (len(a) - 1) * q / 100.0
    lo, hi = int(np.floor(pos)), int(np.ceil(pos))
    if lo == hi:
        return float(a[lo])
    return float(a[lo] + (a[hi] - a[lo]) * (pos - lo))


d = pd.read_csv(USROP)
cols = list(d.columns)

out = {"sumber": {"usrop": USROP, "timestamped": TSUROP}}

# 1. inventaris dan token scan
out["inventaris"] = {
    "baris": int(len(d)),
    "kolom": int(d.shape[1]),
    "nama_kolom": cols,
    "token_bit": scan(cols, TOK_BIT),
    "token_run": scan(cols, TOK_RUN),
    "token_waktu": scan(cols, TOK_TIME),
    "token_biaya": scan(cols, TOK_COST),
}

# 2. sebaran label per well
lab = d["label"].value_counts(dropna=False).to_dict()
per_well = []
for w, g in d.groupby("well"):
    c = g["label"].value_counts()
    n = len(g)
    pos = int(c.get("high_MSE_bit_wear", 0))
    per_well.append({
        "well": w, "baris": int(n),
        "high_MSE": pos, "low_ROP": int(c.get("low_ROP_efficiency", 0)),
        "normal": int(c.get("normal", 0)),
        "prevalensi_high_MSE": round(pos / n, 6),
        "well_positif": bool(pos > 0),
    })
out["label"] = {
    "total": lab,
    "per_well": sorted(per_well, key=lambda r: -r["baris"]),
    "n_well": int(d["well"].nunique()),
    "n_well_tanpa_positif": int(sum(1 for r in per_well if not r["well_positif"])),
    "well_tanpa_positif": [r["well"] for r in per_well if not r["well_positif"]],
    "n_pos": int((d["label"] == "high_MSE_bit_wear").sum()),
    "prevalensi": round(float((d["label"] == "high_MSE_bit_wear").mean()), 6),
}

# 3. spasi grid kedalaman per well
sp = []
for w, g in d.groupby("well"):
    md = g["Measured Depth m"].to_numpy(float)
    dd = np.diff(md)
    dd = dd[dd > 0]
    if len(dd) == 0:
        sp.append({"well": w, "n": 0})
        continue
    sp.append({
        "well": w, "n": int(len(dd)),
        "median_m": round(float(np.median(dd)), 6),
        "min_m": round(float(dd.min()), 6),
        "maks_m": round(float(dd.max()), 6),
        "fraksi_tepat_0_015": round(float((np.abs(dd - 0.015) < 1e-9).mean()), 4),
        "md_min": round(float(md.min()), 3), "md_max": round(float(md.max()), 3),
        "md_rentang_m": round(float(md.max() - md.min()), 3),
        "md_duplikat": int((np.diff(md) == 0).sum()),
    })
out["grid_kedalaman"] = sp

# 4. identitas bit dan run: nilai unik kolom kandidat
out["identitas"] = {
    "kolom_bit": out["inventaris"]["token_bit"],
    "kolom_run": out["inventaris"]["token_run"],
    "kolom_mengandung_bit": [c for c in cols if "bit" in norm(c)],
    "ada_kolom_identitas_bit": bool(out["inventaris"]["token_bit"]),
    "ada_kolom_run": bool(out["inventaris"]["token_run"]),
    "diameter_unik": sorted([float(x) for x in d["Diameter mm"].dropna().unique()]),
    "n_diameter_unik": int(d["Diameter mm"].nunique()),
    "indeks_unik": int(d["Unnamed: 0"].nunique()),
    "indeks_duplikat": int(len(d) - d["Unnamed: 0"].nunique()),
}

# 5. sirkularitas label: rekonstruksi dari MSE dan ROC_coef
mse_pos = d.loc[d["MSE"] > 0, "MSE"].to_numpy(float)
roc_pos = d.loc[d["ROC_coef"] > 0, "ROC_coef"].to_numpy(float)
mse_p75 = percentile_linear(mse_pos, 75)
roc_p25 = percentile_linear(roc_pos, 25)
mse = d["MSE"].to_numpy(float)
roc = d["ROC_coef"].to_numpy(float)
rekon = np.where(mse > mse_p75, "high_MSE_bit_wear",
                 np.where(roc < roc_p25, "low_ROP_efficiency", "normal"))
obs = d["label"].to_numpy()
match = (rekon == obs)
out["sirkularitas"] = {
    "mse_p75_positif": round(float(mse_p75), 6),
    "roc_p25_positif": round(float(roc_p25), 9),
    "baris": int(len(d)),
    "cocok": int(match.sum()),
    "tidak_cocok": int((~match).sum()),
    "akurasi_rekonstruksi": round(float(match.mean()), 6),
    "catatan": "label = fungsi deterministik MSE>P75 lalu ROC<P25, bukan hasil observasi keausan",
}

# rekonstruksi per well (uji apakah ambang global atau per well)
per_well_rekon = []
for w, idx in d.groupby("well").groups.items():
    g = d.loc[idx]
    m = percentile_linear(g.loc[g["MSE"] > 0, "MSE"].to_numpy(float), 75)
    r = percentile_linear(g.loc[g["ROC_coef"] > 0, "ROC_coef"].to_numpy(float), 25)
    rk = np.where(g["MSE"].to_numpy(float) > m, "high_MSE_bit_wear",
                  np.where(g["ROC_coef"].to_numpy(float) < r, "low_ROP_efficiency", "normal"))
    per_well_rekon.append({
        "well": w, "mse_p75": round(float(m), 6), "roc_p25": round(float(r), 9),
        "cocok": int((rk == g["label"].to_numpy()).sum()), "baris": int(len(g)),
        "akurasi": round(float((rk == g["label"].to_numpy()).mean()), 6),
    })
out["sirkularitas"]["per_well_ambang_sendiri"] = per_well_rekon

# 6. waktu kalender hasil interpolasi
if os.path.exists(TSUROP):
    t = pd.read_csv(TSUROP, usecols=["well", "est_timestamp", "join_status"])
    t["ts"] = pd.to_datetime(t["est_timestamp"], errors="coerce", utc=True)
    js = t["join_status"].value_counts(dropna=False).to_dict()
    tw = []
    for w, g in t.groupby("well"):
        ok = g["ts"].notna()
        if ok.sum() == 0:
            tw.append({"well": w, "baris": int(len(g)), "terisi": 0})
            continue
        span_h = (g.loc[ok, "ts"].max() - g.loc[ok, "ts"].min()).total_seconds() / 3600.0
        tw.append({
            "well": w, "baris": int(len(g)), "terisi": int(ok.sum()),
            "fraksi_terisi": round(float(ok.mean()), 4),
            "rentang_jam": round(float(span_h), 3),
            "baris_per_jam": round(float(ok.sum() / span_h), 2) if span_h > 0 else None,
            "ts_min": str(g.loc[ok, "ts"].min()), "ts_maks": str(g.loc[ok, "ts"].max()),
        })
    out["waktu_kalender"] = {
        "berkas": TSUROP,
        "baris": int(len(t)),
        "join_status": js,
        "per_well": sorted(tw, key=lambda r: -r["baris"]),
        "catatan": "est_timestamp adalah interpolasi md ke waktu dari DDR, bukan waktu terukur per baris",
    }
else:
    out["waktu_kalender"] = {"berkas": TSUROP, "ada": False}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w") as f:
    json.dump(out, f, indent=1, default=float)

print("baris", out["inventaris"]["baris"], "kolom", out["inventaris"]["kolom"])
print("kolom_identitas_bit", out["identitas"]["ada_kolom_identitas_bit"],
      "kolom_run", out["identitas"]["ada_kolom_run"],
      "mengandung_bit", out["identitas"]["kolom_mengandung_bit"])
print("n_well", out["label"]["n_well"], "tanpa_positif", out["label"]["well_tanpa_positif"])
print("akurasi_rekonstruksi", out["sirkularitas"]["akurasi_rekonstruksi"],
      "tidak_cocok", out["sirkularitas"]["tidak_cocok"])
print("mse_p75", out["sirkularitas"]["mse_p75_positif"], "roc_p25", out["sirkularitas"]["roc_p25_positif"])
print("diameter_unik", out["identitas"]["n_diameter_unik"], "indeks_duplikat", out["identitas"]["indeks_duplikat"])
print("join_status", out.get("waktu_kalender", {}).get("join_status"))
for r in out.get("waktu_kalender", {}).get("per_well", []):
    print("  ", r["well"], r["baris"], r["terisi"], r.get("fraksi_terisi"), r.get("rentang_jam"))
print("wrote", OUT)
