import json
B = "/mnt/d/Capstone 1(v2)"
d = json.load(open(f"{B}/scratch/v9_i1/v9_i1_RESULTS.json"))
for e in d["engines"]:
    if e["engine"] != "hyd_ki":
        continue
    print("ENGINE:", e["engine"], "| klaim:", e.get("klaim_tugas"))
    print("jenis:", e.get("jenis_tugas"), "| tier:", e.get("sumber_tier"))
    for h in e["heads"]:
        print(" --- HEAD", h["head"], "| tier", h.get("tier"), "| layer", h.get("layer"))
        print("     definisi:", h.get("definisi"))
        print("     metrik:", json.dumps(h.get("metrik_segmen")))
        print("     badge_far:", h.get("badge_far"))
        print("     keyakinan:", h.get("keyakinan"))
        print("     batas:", h.get("batas_pemakaian"))
