import csv, json, glob, gzip, os
from collections import Counter

base = "/mnt/d/Capstone 1(v2)"
R = {}

# --- 1. labels_curated_v2.csv ---
p = base + "/data/volve/labels_curated_v2.csv"
rows = list(csv.DictReader(open(p, newline="", encoding="utf-8")))
R["labels_v2_n"] = len(rows)
R["category_counts"] = dict(Counter(r["category"] for r in rows))
R["category_counts_desc"] = sorted(Counter(r["category"] for r in rows).values(), reverse=True)
R["bha_relevant"] = dict(Counter((r["bha_relevant"] or "").strip() for r in rows))

# durations
def parse(ts):
    ts = (ts or "").strip()
    for f in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            import datetime as dt
            return dt.datetime.strptime(ts, f)
        except Exception:
            pass
    return None

durs = []
bad = 0
for r in rows:
    a, b = parse(r["act_start"]), parse(r["act_end"])
    if a and b and b >= a:
        durs.append((b - a).total_seconds() / 60.0)
    else:
        bad += 1
durs.sort()
R["dur_ok"] = len(durs)
R["dur_unparsed"] = bad
if durs:
    R["dur_min_sum_hours"] = round(sum(durs) / 60.0, 1)
    R["dur_median_min"] = round(durs[len(durs)//2], 1)
    R["dur_max_min"] = round(durs[-1], 1)

# --- 2. witsml_parsed CSV count / lines ---
wp = sorted(glob.glob(base + "/data/volve/witsml_parsed/*.csv"))
R["witsml_parsed_csv_n"] = len(wp)
tot = 0
for f in wp:
    with open(f, "rb") as fh:
        tot += sum(1 for _ in fh)
R["witsml_parsed_total_lines"] = tot

# --- 3. datasets latih ---
ds = sorted(glob.glob(base + "/scratch/v9_d1/datasets/*.csv.gz"))
R["train_datasets_n"] = len(ds)
dsz = {}
for f in ds:
    with gzip.open(f, "rt") as fh:
        dsz[os.path.basename(f)] = sum(1 for _ in fh) - 1
R["train_datasets_rows"] = dsz
R["train_datasets_rows_sum"] = sum(dsz.values())

# --- 4. lowo folds ---
lw = sorted(glob.glob(base + "/scratch/v9_d1/lowo_*.json"))
R["lowo_json_n"] = len(lw)
R["lowo_json_names"] = [os.path.basename(x) for x in lw]

# --- 5. toolwear windows ---
tw = base + "/scratch/v6_e1/toolwear_windows.csv"
if os.path.exists(tw):
    with open(tw, newline="", encoding="utf-8") as fh:
        rd = csv.reader(fh)
        hdr = next(rd)
        R["toolwear_windows_rows"] = sum(1 for _ in rd)
        R["toolwear_windows_cols"] = len(hdr)

# --- 6. REGISTRY heads/tier ---
d = json.load(open(base + "/scratch/v9_i1/v9_i1_RESULTS.json", encoding="utf-8"))
heads = []
for e in d["engines"]:
    for h in e.get("heads", []):
        heads.append((e["engine"], h.get("head"), h.get("tier"), h.get("layer")))
R["registry_heads_n"] = len(heads)
R["registry_heads_per_engine"] = {e["engine"]: len(e.get("heads", [])) for e in d["engines"]}
R["registry_tier_counts"] = dict(Counter(h[2] for h in heads))
R["registry_layer_counts"] = dict(Counter(h[3] for h in heads))
R["registry_head_names"] = [h[0] + "/" + str(h[1]) for h in heads]

print(json.dumps(R, indent=1, ensure_ascii=False))
