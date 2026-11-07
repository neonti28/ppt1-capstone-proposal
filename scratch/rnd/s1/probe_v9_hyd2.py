import json
B = "/mnt/d/Capstone 1(v2)"
d = json.load(open(f"{B}/scratch/v9_i1/v9_i1_RESULTS.json"))
e = [x for x in d["engines"] if x["engine"] == "hyd"][0]
print("n heads:", len(e["heads"]))
for h in e["heads"]:
    m = h.get("metrik_segmen") or {}
    print(f"{h['head']:34} klaim={h.get('klaim')} tier={h.get('tier')} layer={h.get('layer')} "
          f"n={m.get('n')} tp={m.get('tp')} fp={m.get('fp')} prec={m.get('precision')} "
          f"rec={m.get('recall')} far={m.get('far_segmen')}")
print()
print("segmen_info hyd_ki:", json.dumps(d["segmen_info"]["hyd_ki"]))
print()
print("keputusan_akhir:", d.get("keputusan_akhir"))
