import csv, json, sys

base = "/mnt/d/Capstone 1(v2)"
out = {}

# 1) label count
p = base + "/data/volve/labels_curated_v2.csv"
rows = list(csv.DictReader(open(p, newline="", encoding="utf-8")))
out["labels_curated_v2_rows"] = len(rows)
out["labels_curated_v2_cols"] = list(rows[0].keys())

# 2) registry heads
q = base + "/scratch/v9_i1/v9_i1_RESULTS.json"
d = json.load(open(q, encoding="utf-8"))
if isinstance(d, dict):
    out["v9_i1_top_keys"] = list(d.keys())[:20]
    for k, v in d.items():
        if isinstance(v, list):
            out["v9_i1_len_" + k] = len(v)
print(json.dumps(out, indent=1)[:4000])
