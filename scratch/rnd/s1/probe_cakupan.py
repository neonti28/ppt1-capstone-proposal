import json
d = json.load(open('/mnt/d/Capstone 1(v2)/scratch/rnd/r8/r8_hyd.json'))
print("cakupan per fold (H1):")
for r in d["rows"]:
    if r["model"] == "H1_stat_dan_rule":
        print(f"  {r['fold']:8s} cakupan={r['cakupan']} menit_kal={r['menit_kalender']} n={r['rows']['n_pos']+r['rows']['n_neg']}")
