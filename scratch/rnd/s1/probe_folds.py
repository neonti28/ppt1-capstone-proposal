import json
p = "/mnt/d/Capstone 1(v2)/scratch/rnd/s1/s1_hyd_seeds.json"
d = json.load(open(p))
s42 = d["per_seed"]["42"]
print("=== RINGKAS SEED 42 ===")
print(json.dumps(s42["ringkas"], indent=1))
print()
print("=== PER FOLD H1 seed 42 ===")
hdr = f"{'fold':8} {'n':>6} {'npos':>5} {'tp':>5} {'fp':>5} {'prec':>7} {'rec':>7} {'far_kal':>8} {'far_baris':>9} {'cakupan':>7} {'lead':>6} {'h':>4}"
print(hdr)
for r in s42["folds"]:
    if r["model"] != "H1_stat_dan_rule":
        continue
    print(f"{r['fold']:8} {r['n']:6d} {r['n_pos']:5d} {r['rows']['tp']:5d} {r['rows']['fp']:5d} "
          f"{str(r['rows']['precision']):>7} {str(r['rows']['recall']):>7} {r['far24_kalender']:8} "
          f"{r['far24_baris']:9} {r['cakupan']:7} {str(r['lead']['lead_median_min']):>6} {r['h_terpilih']:>4}")
print()
print("=== MODEL LAIN seed 42 (ringkas) ===")
for m in ("rule_kanal", "stat_cusum", "H1_stat_dan_rule", "H1b_stat_atau_rule"):
    rr = [r for r in s42["folds"] if r["model"] == m]
    fp = sum(r["rows"]["fp"] for r in rr)
    tp = sum(r["rows"]["tp"] for r in rr)
    far_k = [r["far24_kalender"] for r in rr]
    far_b = [r["far24_baris"] for r in rr]
    pr = [r["rows"]["precision"] for r in rr if r["rows"]["precision"] is not None]
    rc = [r["rows"]["recall"] for r in rr if r["rows"]["recall"] is not None]
    import statistics as st
    print(f"{m:22} FP {fp:5d} TP {tp:5d} far_kal_med {st.median(far_k):8} far_baris_med {st.median(far_b):9} "
          f"prec_med {round(st.median(pr),4):7} rec_med {round(st.median(rc),4):7} "
          f"fold<=6 {sum(1 for x in far_k if x<=6)}/9")
print()
print("=== F-14 detail untuk banding V9 ===")
for r in s42["folds"]:
    if r["fold"] == "F-14":
        print(json.dumps({k: r[k] for k in ("model","n","n_pos","rows","far24_kalender","far24_baris",
                                            "cakupan","lead","h_terpilih","menit_kalender")}, indent=1))
