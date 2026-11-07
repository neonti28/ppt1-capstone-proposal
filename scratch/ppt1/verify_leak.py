import json
p = "/mnt/d/Capstone 1(v2)/scratch/v9_d1/v9_d1_05_leak_lowo.json"
d = json.load(open(p))
tot = 0
print("dataset            status  n_rows  leak_viol  folds")
for k, v in d.items():
    lv = v.get("leak_violations_feat_ge_lab")
    tot += (lv or 0)
    print("%-18s %-7s %-7s %-10s %s" % (k, v.get("status"), v.get("n_rows"), lv, v.get("n_folds")))
print("TOTAL leak violations:", tot, "| dataset:", len(d))
