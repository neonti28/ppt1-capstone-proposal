import json

P = "/mnt/d/Capstone 1(v2)/scratch/v9_i1/v9_i1_RESULTS.json"
d = json.load(open(P))
print("META:", json.dumps(d["meta"], ensure_ascii=False))
print("SEGMEN:", json.dumps(d["segmen_info"], ensure_ascii=False)[:600])
print()
for e in d["engines"]:
    print("=" * 78)
    print(e["engine"], "| heads:", len(e["heads"]))
    for h in e["heads"]:
        m = h.get("metrik_segmen")
        print(f"  {h['head']:<28} tier={h['tier']:<24} layer={h['layer']} "
              f"klaim={h.get('klaim')} n={h['n_windows']} aktif={h.get('n_aktif')}")
        if m:
            print(f"      metrik: n={m['n']} pos={m['pos']} neg={m['neg']} tp={m['tp']} fp={m['fp']} "
                  f"fn={m['fn']} P={m['precision']} R={m['recall']} FAR={m['far_segmen']} [{m['far_unit']}]")
        if h.get("auprc_segmen") is not None:
            print(f"      auprc_segmen={h['auprc_segmen']}  n_fitur={h.get('n_fitur')}")
print()
tot = sum(len(e["heads"]) for e in d["engines"])
print("TOTAL HEAD:", tot, "| n_engine:", len(d["engines"]))
print("DECISION:", json.dumps(d["decision_layer"]["ringkasan"], ensure_ascii=False),
      "L1:", d["decision_layer"]["nperingatan_l1"])
