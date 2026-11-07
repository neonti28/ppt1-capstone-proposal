import json
P = '/mnt/d/Capstone 1(v2)/scratch/rnd/s1/'
d = json.load(open(P + 's1_hyd_seeds.json'))
m = json.load(open(P + 's1_meta.json'))
print("STATUS", d["status"], "seeds", d["seed_list"])
print("reproduksi semua_lulus:", d["reproduksi"]["semua_lulus"])
print("delta:", json.dumps(d["reproduksi"]["delta"]))
print("per_fold delta fp:", [x["fp_delta"] for x in d["reproduksi"]["per_fold"]])
print("per_fold delta tp:", [x["tp_delta"] for x in d["reproduksi"]["per_fold"]])
print("\n== H1 per fold seed 42 ==")
for r in d["per_seed"]["42"]["folds"]:
    if r["model"] == "H1_stat_dan_rule":
        print(f"{r['fold']:8s} fp={r['rows']['fp']:5d} tp={r['rows']['tp']:5d} "
              f"P={r['rows']['precision']:.4f} R={r['rows']['recall']:.4f} "
              f"farK={r['far24_kalender']:8.4f} farB={r['far24_baris']:8.4f} "
              f"lead={r['lead']['lead_median_min']} warn={r['lead']['n_diperingatkan']}/{r['lead']['n_onset']} "
              f"cak={r['cakupan']} h={r['h_terpilih']} gate={r['gate_A_baru']}")
print("\n== ringkas per seed H1 ==")
for s in d["seed_list"]:
    r = d["per_seed"][str(s)]["ringkas"]
    print(s, {k: r[k] for k in ("fp_total","tp_total","precision_median","recall_median",
                                "far24_kalender_median","far24_baris_median","lead_median_median",
                                "n_diperingatkan","fold_far_le6","cakupan_median")})
print("\n== kontrol per seed ==")
for s in d["seed_list"]:
    k = d["kontrol_stokastik"]["per_seed"][str(s)]["ringkas"]
    print(s, {kk: k[kk] for kk in ("fp_total","tp_total","precision_median","recall_median",
                                   "far24_kalender_median","lead_median_median","n_diperingatkan")})
print("\n== kontrol sebaran ==", json.dumps(d["kontrol_stokastik"]["sebaran"]))
print("\n== lintas seed (median/min/maks/rentang) ==")
for k, v in d["lintas_seed"].items():
    print(f"{k:28s} median={v['median']} min={v['min']} maks={v['maks']} rentang={v['rentang']}")
print("\n== meta ==")
for k in ("elapsed_s","python","pandas","numpy","dataset_shape","dataset_sha256","n_fold","harness_sha256"):
    print(k, m.get(k))
print("wells", json.dumps(m["wells"]))
print("pos", json.dumps(m["per_well_pos"]))
print("kal", json.dumps(m["per_well_menit_kalender"]))
print("n_fold_berbeda_maks", d["n_fold_berbeda_maks"])
