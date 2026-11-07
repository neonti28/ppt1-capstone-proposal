import json
p = "/mnt/d/Capstone 1(v2)/scratch/v9_i1/v9_i1_RESULTS.json"
d = json.load(open(p))

out = []
for e in d["engines"]:
    print("=" * 100)
    print("ENGINE:", e["engine"], "|", e.get("klaim_tugas"))
    print("jenis:", e.get("jenis_tugas"))
    for h in e.get("heads", []):
        m = h.get("metrik_segmen") or {}
        print(f"  - {h['head']:32s} tier={h['tier']:24s} layer={h['layer']} "
              f"n={m.get('n')} tp={m.get('tp')} fp={m.get('fp')} fn={m.get('fn')} "
              f"P={m.get('precision')} R={m.get('recall')} FAR={m.get('far_segmen')}")
        print(f"      badge_far: {str(h.get('badge_far'))[:150]}")
        print(f"      keyakinan: {str(h.get('keyakinan'))[:200]}")
        print(f"      batas: {str(h.get('batas_pemakaian'))[:200]}")
        out.append(dict(engine=e["engine"], head=h["head"], tier=h["tier"], layer=h["layer"],
                        metrik=m, badge_far=h.get("badge_far"), keyakinan=h.get("keyakinan"),
                        batas=h.get("batas_pemakaian")))

json.dump(out, open("/mnt/d/Capstone 1(v2)/scratch/ppt1/v9_engine_heads_flat.json", "w"), indent=1, ensure_ascii=False)
print("\nsaved", len(out), "heads")
