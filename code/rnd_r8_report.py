import json
import numpy as np
BASE = "/mnt/d/Capstone 1(v2)"
agg = json.load(open(f"{BASE}/scratch/rnd/r8/r8_agg.json"))

def med(xs):
    v = [x for x in xs if x is not None]
    return round(float(np.median(v)), 4) if v else None

for task in ["hyd", "shk", "stuck"]:
    print("=" * 70)
    print("TASK", task)
    for mdl, m in agg["task"][task]["model"].items():
        pf = m["per_fold"]
        rec = [v["recall"] for v in pf.values()]
        pre = [v["precision"] for v in pf.values()]
        far = [v["far24"] for v in pf.values()]
        lead = [v["lead"]["lead_median_min"] for v in pf.values()]
        n_ons = sum(v["lead"]["n_onset"] for v in pf.values())
        n_warn = sum(v["lead"]["n_diperingatkan"] for v in pf.values())
        both = sum(1 for v in pf.values()
                   if v["separuh"].get("awal", {}).get("recall") and v["separuh"].get("akhir", {}).get("recall"))
        sep_awal = med([v["separuh"].get("awal", {}).get("recall") for v in pf.values()])
        sep_akhir = med([v["separuh"].get("akhir", {}).get("recall") for v in pf.values()])
        print(f"{mdl:34s} FP={m['fp_total']:6d} TP={m['tp_total']:5d} "
              f"P={med(pre)} R={med(rec)} Rmin={min([x for x in rec if x is not None] or [0])} "
              f"FAR24med={med(far)} far[{min(far)},{max(far)}] foldFAR6={m['fold_far_le6']}/{m['n_fold']} "
              f"leadMed={med(lead)} warn={n_warn}/{n_ons} halvesBoth={both}/{len(pf)} "
              f"R_awal={sep_awal} R_akhir={sep_akhir}")
    print()
    # table bahan dokumen (per fold, model utama)
    for mdl in agg["task"][task]["model"]:
        if mdl.startswith(("H1_", "H2_", "H4_")):
            print("---", mdl)
            for w, v in agg["task"][task]["model"][mdl]["per_fold"].items():
                print(f"  {w:8s} P={v['precision']} R={v['recall']} FP={v['fp']} "
                      f"TP={v['tp']} npos={v['n_pos']} FAR24={v['far24']} "
                      f"lead={v['lead']['lead_median_min']} thr={v.get('thr')} h={v.get('h')} "
                      f"auprc={v.get('auprc')} prev={v['prev']}")
print()
print("anggota toolwear n_window 469 (T01 120 T02 112 T03 121 T04 116)")
