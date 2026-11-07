"""S4-A: statistik record activity DDR (durasi, kode, state). READ-ONLY.

Keluaran: scratch/rnd/s4/ddr_activity_stats.json
Sumber: data/volve/ddr.parquet (1.759 laporan harian, kolom activity).
"""
import os, json
from collections import Counter, defaultdict
from datetime import datetime
import numpy as np
import pandas as pd

ROOT = "/mnt/d/Capstone 1(v2)"
SRC = os.path.join(ROOT, "data/volve/ddr.parquet")
OUT = os.path.join(ROOT, "scratch/rnd/s4/ddr_activity_stats.json")

df = pd.read_parquet(SRC)

def as_list(obj):
    if obj is None:
        return []
    if isinstance(obj, np.ndarray):
        return list(obj)
    if isinstance(obj, (list, tuple)):
        return list(obj)
    if isinstance(obj, dict):
        return [obj]
    return []

def parse_dt(s):
    if not isinstance(s, str) or not s.strip():
        return None
    try:
        return datetime.fromisoformat(s)
    except Exception:
        return None

res = {
    "sumber": {"path": SRC, "bytes": os.path.getsize(SRC), "baris": int(len(df)), "kolom": list(df.columns)},
    "laporan": {},
    "activity": {},
}

res["laporan"]["n_baris"] = int(len(df))
res["laporan"]["n_kolom"] = int(len(df.columns))
res["laporan"]["n_wellbore_unik"] = int(df["nameWellbore"].nunique())
res["laporan"]["wellbore_daftar"] = sorted(df["nameWellbore"].unique().tolist())
res["laporan"]["laporan_per_wellbore"] = {k: int(v) for k, v in df["nameWellbore"].value_counts().items()}
res["laporan"]["dTimStart_min"] = str(df["dTimStart"].min())
res["laporan"]["dTimStart_max"] = str(df["dTimStart"].max())

# --- activity ---
codes = Counter()
states = Counter()
details = Counter()
dur_by_code = defaultdict(list)
n_rec = 0
n_rows_with_act = 0
n_missing_time = 0
n_neg_dur = 0
n_zero_dur = 0
dur_all = []
comments_len = 0
n_comments = 0
kw = {
    "repair": 0, "replace": 0, "replac": 0, "change": 0, "inspect": 0,
    "function_test": 0, "pressure_test": 0, "service": 0, "failed": 0,
    "leak": 0, "trip_for": 0,
}
per_well = Counter()
act_per_report = []

for idx, row in df.iterrows():
    items = as_list(row["activity"])
    act_per_report.append(len(items))
    if items:
        n_rows_with_act += 1
    wb = row["nameWellbore"]
    for a in items:
        if not isinstance(a, dict):
            continue
        n_rec += 1
        per_well[wb] += 1
        code = (a.get("proprietaryCode") or "").strip()
        state = (a.get("state") or "").strip()
        det = (a.get("stateDetailActivity") or "").strip()
        codes[code] += 1
        states[state] += 1
        details[det] += 1
        c = a.get("comments")
        if isinstance(c, str) and c.strip():
            n_comments += 1
            comments_len += len(c)
            low = c.lower()
            for k in kw:
                if k in low:
                    kw[k] += 1
        t0 = parse_dt(a.get("dTimStart"))
        t1 = parse_dt(a.get("dTimEnd"))
        if t0 is None or t1 is None:
            n_missing_time += 1
            continue
        d = (t1 - t0).total_seconds() / 3600.0
        if d < 0:
            n_neg_dur += 1
            continue
        if d == 0:
            n_zero_dur += 1
        dur_all.append(d)
        dur_by_code[code].append(d)

def stats(v):
    if not v:
        return None
    s = pd.Series(v)
    return {
        "n": int(len(v)),
        "sum_jam": round(float(s.sum()), 3),
        "mean_jam": round(float(s.mean()), 4),
        "median_jam": round(float(s.median()), 4),
        "p90_jam": round(float(s.quantile(0.90)), 4),
        "max_jam": round(float(s.max()), 4),
        "min_jam": round(float(s.min()), 4),
    }

res["activity"]["n_record"] = n_rec
res["activity"]["n_laporan_punya_activity"] = n_rows_with_act
res["activity"]["n_laporan_tanpa_activity"] = int(len(df)) - n_rows_with_act
res["activity"]["n_record_tanpa_waktu"] = n_missing_time
res["activity"]["n_record_durasi_negatif"] = n_neg_dur
res["activity"]["n_record_durasi_nol"] = n_zero_dur
res["activity"]["n_record_durasi_valid"] = len(dur_all)
res["activity"]["total_jam_semua_activity"] = round(float(sum(dur_all)), 3)
res["activity"]["durasi_semua"] = stats(dur_all)
res["activity"]["n_comments_terisi"] = n_comments
res["activity"]["rata_panjang_comment_char"] = round(comments_len / n_comments, 1) if n_comments else 0
res["activity"]["kata_kunci_comment"] = kw

# pengelompokan kode: prefix sebelum " -- "
prefix = Counter()
for c, n in codes.items():
    p = c.split("--")[0].strip() if "--" in c else c
    prefix[p] += n
res["activity"]["kode_prefix"] = dict(prefix.most_common())
res["activity"]["kode_teratas"] = dict(codes.most_common(40))
res["activity"]["n_kode_unik"] = len(codes)
res["activity"]["state"] = dict(states.most_common())
res["activity"]["state_detail"] = dict(details.most_common(25))

# durasi per kode (semua kode dengan >=1 record valid)
res["activity"]["durasi_per_kode"] = {c: stats(v) for c, v in sorted(dur_by_code.items(), key=lambda kv: -sum(kv[1]))}

# khusus kode interruption (henti) dan kode maintain
inter = {c: v for c, v in dur_by_code.items() if c.startswith("interruption")}
res["activity"]["interruption"] = {
    "n_kode": len(inter),
    "total_record": int(sum(len(v) for v in inter.values())),
    "total_jam": round(float(sum(sum(v) for v in inter.values())), 3),
    "per_kode": {c: stats(v) for c, v in sorted(inter.items(), key=lambda kv: -sum(kv[1]))},
}

maint = {c: v for c, v in dur_by_code.items() if "maintain" in c or "repair" in c}
res["activity"]["maintenance_terkait"] = {
    "n_kode": len(maint),
    "total_record": int(sum(len(v) for v in maint.values())),
    "total_jam": round(float(sum(sum(v) for v in maint.values())), 3),
    "per_kode": {c: stats(v) for c, v in maint.items()},
}

# state=fail dengan durasi (proxy kegagalan peralatan)
fail_dur = []
for idx, row in df.iterrows():
    for a in as_list(row["activity"]):
        if not isinstance(a, dict):
            continue
        if (a.get("state") or "").strip() != "fail":
            continue
        t0 = parse_dt(a.get("dTimStart")); t1 = parse_dt(a.get("dTimEnd"))
        if t0 is None or t1 is None:
            continue
        d = (t1 - t0).total_seconds() / 3600.0
        if d >= 0:
            fail_dur.append(d)
res["activity"]["state_fail_durasi"] = stats(fail_dur)

res["activity"]["record_per_wellbore"] = dict(per_well.most_common())
apr = pd.Series(act_per_report)
res["activity"]["activity_per_laporan"] = {
    "mean": round(float(apr.mean()), 3),
    "median": round(float(apr.median()), 3),
    "max": int(apr.max()),
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
print("WROTE", OUT, os.path.getsize(OUT), "bytes")
print("ringkas: laporan", res["laporan"]["n_baris"], "| activity", n_rec, "| kode unik", res["activity"]["n_kode_unik"],
      "| total jam", res["activity"]["total_jam_semua_activity"], "| interruption jam", res["activity"]["interruption"]["total_jam"])
print("prefix:", res["activity"]["kode_prefix"])
print("state:", res["activity"]["state"])
print("maintenance:", res["activity"]["maintenance_terkait"]["total_record"], "record,", res["activity"]["maintenance_terkait"]["total_jam"], "jam")
print("kata kunci comment:", kw)
print("state_fail:", res["activity"]["state_fail_durasi"])
