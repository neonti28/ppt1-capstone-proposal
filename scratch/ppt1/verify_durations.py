import csv, json, datetime as dt
from collections import Counter, defaultdict

base = "/mnt/d/Capstone 1(v2)"
rows = list(csv.DictReader(open(base + "/data/volve/labels_curated_v2.csv", newline="", encoding="utf-8")))

def p(ts):
    ts = (ts or "").strip()
    if not ts:
        return None
    try:
        return dt.datetime.fromisoformat(ts)
    except Exception:
        return None

durs = []
per_cat = defaultdict(float)
per_well = Counter()
bad = 0
for r in rows:
    a, b = p(r["act_start"]), p(r["act_end"])
    if a and b and b >= a:
        m = (b - a).total_seconds() / 60.0
        durs.append(m)
        per_cat[r["category"]] += m
        per_well[r["wellbore"]] += 1
    else:
        bad += 1

durs.sort()
out = {
    "n_rows": len(rows),
    "dur_ok": len(durs),
    "dur_bad": bad,
    "total_minutes": round(sum(durs), 1),
    "total_hours": round(sum(durs) / 60.0, 1),
    "median_min": round(durs[len(durs) // 2], 1),
    "p90_min": round(durs[int(len(durs) * 0.9)], 1),
    "max_min": round(durs[-1], 1),
    "wells": len(per_well),
    "per_well_top": per_well.most_common(12),
    "hours_per_category": {k: round(v / 60.0, 1) for k, v in sorted(per_cat.items(), key=lambda x: -x[1])},
}
print(json.dumps(out, indent=1))
