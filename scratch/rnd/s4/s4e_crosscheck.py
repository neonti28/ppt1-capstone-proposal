"""S4-E: uji silang dan register inspeksi/uji dari DDR. READ-ONLY.

(a) distribusi presTestType (jenis uji integritas sumur) dari statusInfo
(b) jumlah activity dengan kode mengandung 'test'/'inspect'/'maintain'
(c) uji silang: jam interruption per wellbore (DDR activity) lawan jam kejadian (labels)
Keluaran: scratch/rnd/s4/crosscheck.json
"""
import os, json
from collections import Counter, defaultdict
from datetime import datetime
import numpy as np
import pandas as pd

ROOT = "/mnt/d/Capstone 1(v2)"
OUT = os.path.join(ROOT, "scratch/rnd/s4/crosscheck.json")
df = pd.read_parquet(os.path.join(ROOT, "data/volve/ddr.parquet"))

def as_list(o):
    if o is None:
        return []
    if isinstance(o, np.ndarray):
        return list(o)
    if isinstance(o, (list, tuple)):
        return list(o)
    if isinstance(o, dict):
        return [o]
    return []

def pdt(s):
    if not isinstance(s, str) or not s:
        return None
    try:
        return datetime.fromisoformat(s)
    except Exception:
        return None

res = {}

# (a) presTestType
ptt = Counter()
ptt_well = defaultdict(Counter)
for _, r in df.iterrows():
    for si in as_list(r["statusInfo"]):
        v = (si.get("presTestType") or "").strip() if isinstance(si, dict) else ""
        if v and v.lower() != "none":
            ptt[v] += 1
            ptt_well[r["nameWellbore"]][v] += 1
res["pres_test_type"] = {
    "definisi": "statusInfo.presTestType pada laporan DDR (jenis uji tekanan/integritas)",
    "n_laporan_dengan_uji": int(sum(ptt.values())),
    "n_laporan_total": int(len(df)),
    "distribusi": dict(ptt.most_common()),
    "per_wellbore": {k: dict(v) for k, v in ptt_well.items()},
}

# (b) kode activity bernuansa uji/inspeksi/maintenance
kw = {"test": 0, "inspect": 0, "maintain": 0, "repair": 0, "service": 0}
kw_dur = defaultdict(float)
n = 0
for _, r in df.iterrows():
    for a in as_list(r["activity"]):
        if not isinstance(a, dict):
            continue
        code = (a.get("proprietaryCode") or "").lower()
        t0 = pdt(a.get("dTimStart")); t1 = pdt(a.get("dTimEnd"))
        d = ((t1 - t0).total_seconds() / 3600.0) if (t0 and t1) else 0.0
        if d < 0:
            d = 0.0
        n += 1
        for k in kw:
            if k in code:
                kw[k] += 1
                kw_dur[k] += d
res["kode_activity_bernuansa"] = {
    "definisi": "jumlah record activity yang proprietaryCode-nya mengandung kata kunci",
    "n_record_total": n,
    "n_record": kw,
    "jam": {k: round(v, 3) for k, v in kw_dur.items()},
}

# (c) uji silang jam per wellbore: DDR interruption vs labels
inter_jam = defaultdict(float)
inter_n = defaultdict(int)
for _, r in df.iterrows():
    for a in as_list(r["activity"]):
        if not isinstance(a, dict):
            continue
        code = (a.get("proprietaryCode") or "")
        if not code.startswith("interruption"):
            continue
        t0 = pdt(a.get("dTimStart")); t1 = pdt(a.get("dTimEnd"))
        if not (t0 and t1):
            continue
        d = (t1 - t0).total_seconds() / 3600.0
        if d < 0:
            continue
        inter_jam[r["nameWellbore"]] += d
        inter_n[r["nameWellbore"]] += 1

lab = pd.read_csv(os.path.join(ROOT, "data/volve/labels_curated_v2.csv"), low_memory=False)
t0 = pd.to_datetime(lab["act_start"], errors="coerce", format="ISO8601", utc=True)
t1 = pd.to_datetime(lab["act_end"], errors="coerce", format="ISO8601", utc=True)
lab["_d"] = (t1 - t0).dt.total_seconds() / 3600.0
lab = lab[lab["_d"].notna() & (lab["_d"] >= 0)]
lab_jam = lab.groupby("wellbore")["_d"].sum().to_dict()
lab_n = lab.groupby("wellbore")["_d"].count().to_dict()

rows = []
for wb in sorted(set(list(inter_jam.keys()) + list(lab_jam.keys()))):
    rows.append({
        "wellbore": wb,
        "ddr_interruption_n": int(inter_n.get(wb, 0)),
        "ddr_interruption_jam": round(float(inter_jam.get(wb, 0.0)), 3),
        "labels_n": int(lab_n.get(wb, 0)),
        "labels_jam": round(float(lab_jam.get(wb, 0.0)), 3),
        "rasio_labels_terhadap_ddr": round(float(lab_jam.get(wb, 0.0)) / float(inter_jam[wb]), 4) if inter_jam.get(wb) else None,
    })
res["silang_per_wellbore"] = rows
res["silang_total"] = {
    "ddr_interruption_jam": round(float(sum(inter_jam.values())), 3),
    "ddr_interruption_n": int(sum(inter_n.values())),
    "labels_jam": round(float(lab["_d"].sum()), 3),
    "labels_n": int(len(lab)),
    "rasio_jam": round(float(lab["_d"].sum()) / sum(inter_jam.values()), 4),
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
print("WROTE", OUT, os.path.getsize(OUT))
print("presTestType:", res["pres_test_type"]["n_laporan_dengan_uji"], "laporan;", res["pres_test_type"]["distribusi"])
print("kode bernuansa:", res["kode_activity_bernuansa"]["n_record"])
print("silang total:", res["silang_total"])
print("7 well (F-14,F-15A,F-15,F-5,F-7,F-9,F-9A):")
for r in rows:
    if r["wellbore"] in ("NO 15/9-F-14", "NO 15/9-F-15 A", "NO 15/9-F-15", "NO 15/9-F-5", "NO 15/9-F-7", "NO 15/9-F-9", "NO 15/9-F-9 A"):
        print("  ", r)
