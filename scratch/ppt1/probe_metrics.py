"""Rincian FAR per fold (tau 0,5) + tabel klaim-tidak-terukur."""
import json
import os

BASE = "/mnt/d/Capstone 1(v2)"


def load(p):
    return json.load(open(os.path.join(BASE, p)))


print("== vib: FAR_24jam @ tau0.5 per fold (model rf) ==")
vib = load("scratch/v9_e_ml/v9_e_ML_vib_RESULTS.json")
rows = []
for f in vib["folds"]:
    rf = f["models"]["rf"]["tau_metrics"]["0.5"]
    rows.append((f["test_well"], rf["precision"], rf["recall"], rf["FAR_24jam"]))
for w, p, r, far in rows:
    print(f"  {w:8s} P={p:.4f} R={r:.4f} FAR_24jam={far:.2f}")
if rows:
    fars = [x[3] for x in rows]
    print("  min/max/rasio:", min(fars), max(fars), round(max(fars) / min(fars), 2))

print("\n== vib agregat ==")
print(json.dumps(vib.get("agregat", {}), ensure_ascii=False)[:1500])

print("\n== engine lain: cari FAR di RESULT json masing-masing ==")
for f in ["ssi", "stuck_k2", "shk"]:
    p = f"scratch/v9_e_ml/v9_e_ML_{f}_RESULTS.json"
    try:
        d = load(p)
    except Exception as e:
        print(p, "ERROR", e)
        continue
    print(f"\n-- {f}: keys {list(d.keys())}")
    print("  agregat:", json.dumps(d.get("agregat", {}), ensure_ascii=False)[:800])
    folds = d.get("folds", [])
    for fo in folds[:12]:
        ms = fo.get("models", {})
        for mname, m in ms.items():
            tm = (m or {}).get("tau_metrics", {})
            if "0.5" in tm:
                t = tm["0.5"]
                print(f"   fold{fo.get('fold')} {fo.get('test_well')} {mname} "
                      f"P={t.get('precision'):.4f} R={t.get('recall'):.4f} FAR={t.get('FAR_24jam')}")

print("\n== registry tier ==")
i1 = load("scratch/v9_i1/v9_i1_RESULTS.json")
print("n_engine:", i1["meta"]["n_engine"], "auto_alarm_slots:", i1["auto_critical_alarm_slots"])
print("lapisan:", i1["decision_layer"]["ringkasan"])
heads = []
for e in i1["engines"]:
    for h in e["heads"]:
        heads.append((e["engine"], h["head"], h["tier"], h["layer"]))
print("n_head:", len(heads))
from collections import Counter
print("tier:", Counter(h[2] for h in heads))
print("layer:", Counter(h[3] for h in heads))
for h in heads:
    print("  ", h)
