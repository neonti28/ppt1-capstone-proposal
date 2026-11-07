import json, os
B="/mnt/d/Capstone 1(v2)/scratch/v9_e_stat"
for f in ["v9_e_stat_01_hyd_ki_RESULTS.json","v9_e_stat_02_stuck_e2_RESULTS.json","v9_e_stat_03_tool_wear_RESULTS.json","v9_e_stat_04_fisher_pearson_RESULTS.json"]:
    d=json.load(open(os.path.join(B,f)))
    print("="*70); print(f); print("engine:",d.get("engine"))
    print("summary:",json.dumps(d.get("summary",{}),ensure_ascii=False))
    if "label_crosscheck" in d:
        cc=d["label_crosscheck"]; print("crosscheck:",cc["verdict"],"mismatch:",cc["total_y_mismatch"],"rows:",cc["total_rows"])
    if "flowout_status" in d:
        print("flowout:",d["flowout_status"]["verdict"])
        print("label_Kii:",json.dumps(d["label_Kii"],ensure_ascii=False))
        e=d["engine_fisher_pearson_variant"]; print("fisher auprc:",e["auprc"],"prev:",e["prev"],"op:",json.dumps(e["op_q95"]))
