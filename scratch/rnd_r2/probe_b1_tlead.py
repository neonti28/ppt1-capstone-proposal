import json

p = "/mnt/d/Capstone 1(v2)/scratch/v9_i1/v9_i1_RESULTS.json"
d = json.load(open(p))


def walk(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk(v, f"{path}.{k}" if path else k)
    else:
        yield path, obj


KEYS = ("b1", "tlead", "t_lead", "lead", "auprc", "far", "precision", "recall")

for e in d["engines"]:
    print("=" * 70)
    print("ENGINE:", e["engine"])
    for h in e["heads"]:
        print(f"  HEAD {h.get('head')} | klaim={h.get('klaim')} | tier={h.get('tier')}")
        for k, v in h.items():
            if k in ("head", "klaim", "tier", "layer", "badge_far", "keyakinan",
                     "batas_pemakaian", "human_review_required", "n_windows",
                     "n_aktif", "frac_aktif", "contoh_idx_aktif", "n_nodata"):
                continue
            s = json.dumps(v, ensure_ascii=False)
            print(f"    .{k} = {s[:400]}")
