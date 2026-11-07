import json
import numpy as np

base = "/mnt/d/Capstone 1(v2)/scratch/rnd/e4"
a1 = json.load(open(f"{base}/e4_a1.json"))
base_j = json.load(open(f"{base}/e4_baseline.json"))
hyb = json.load(open(f"{base}/e4_hybrid.json"))


def med(v):
    v = [x for x in v if x is not None]
    return round(float(np.median(v)), 4) if v else None


def summarize(rows, seed=None):
    sel = rows if seed is None else [r for r in rows if r.get("seed") == seed]
    if not sel:
        return None
    return dict(
        n=len(sel),
        far24_baris=med([r["rows"]["far_per_24h"] for r in sel]),
        far24_kej=med([r["events"]["far24_kejadian"] for r in sel]),
        far24_kal=med([r.get("far24_kalender") for r in sel]),
        recall=med([r["rows"]["recall"] for r in sel]),
        precision=med([r["rows"]["precision"] for r in sel]),
        gateA_lama=sum(1 for r in sel if r.get("gate_A_lama")),
        gateA_lama_penuh=sum(1 for r in sel if r.get("gate_A_lama_penuh")),
        gateA_baru=sum(1 for r in sel if r.get("gate_A_baru")),
        recall_nol=sum(1 for r in sel if (r["rows"]["recall"] or 0) == 0),
    )


out = {}
for var in ("alpha_E2_lama", "alpha_anggaran"):
    rows = [r for r in a1["folds"] if r.get("varian") == var]
    out[f"A1_{var}_seed42"] = summarize(rows, 42)
    out[f"A1_{var}_pooled"] = summarize(rows)

for nm in ("persistence", "rule_t0m1", "hybrid_rule_persistence", "hybrid_proxy_E3"):
    rows = [r for r in base_j["folds"] if r.get("model") == nm]
    out[nm] = summarize(rows)

for nm in ("H_and_hybrid_ML", "H_or_hybrid_ML"):
    rows = [r for r in hyb["folds"] if r.get("model") == nm]
    out[f"{nm}_seed42"] = summarize(rows, 42)
    out[f"{nm}_pooled"] = summarize(rows)

json.dump(out, open(f"{base}/e4_beforeafter.json", "w"), indent=2)

hdr = "%-30s %3s %9s %9s %9s %8s %8s %6s %6s %6s" % (
    "variant", "n", "FAR_bar", "FAR_kej", "FAR_kal", "R", "P", "gA_l", "gA_lp", "gA_b")
print(hdr)
for k, v in out.items():
    if not v:
        continue
    print("%-30s %3d %9s %9s %9s %8s %8s %6d %6d %6d" % (
        k, v["n"], v["far24_baris"], v["far24_kej"], v["far24_kal"],
        v["recall"], v["precision"], v["gateA_lama"], v["gateA_lama_penuh"], v["gateA_baru"]))
