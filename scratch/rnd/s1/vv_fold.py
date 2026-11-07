import json
d=json.load(open("scratch/rnd/s1/s1_hyd_seeds.json"))
f42={r["fold"]:r for r in d["per_seed"]["42"]["folds"] if r["model"]=="H1_stat_dan_rule"}
print("=== H1 seed 42 per fold: tp fp prec recall far24kal far24baris lead n_dip cakupan h ===")
tot_fp=tot_tp=0
for f in sorted(f42):
    r=f42[f]; tot_fp+=r["rows"]["fp"]; tot_tp+=r["rows"]["tp"]
    print(f"{f:7s} tp={r['rows']['tp']:5d} fp={r['rows']['fp']:4d} prec={r['rows']['precision']} rec={r['rows']['recall']} "
          f"fark={r['far24_kalender']} farb={r['far24_baris']} lead={r['lead']['lead_median_min']} "
          f"dip={r['lead']['n_diperingatkan']}/{r['lead']['n_onset']} cak={r['cakupan']} h={r['h_terpilih']}")
print("TOTAL fp",tot_fp,"tp",tot_tp)
print()
r8=json.load(open("scratch/rnd/r8/r8_hyd.json"))
print("=== R8 rows aggregated ===")
for mdl in ("H1_stat_dan_rule","rule_kanal","H1b_stat_atau_rule","stat_cusum"):
    rs=[r for r in r8["rows"] if r["model"]==mdl]
    if not rs: continue
    dip=sum(r["lead"]["n_diperingatkan"] for r in rs); ons=sum(r["lead"]["n_onset"] for r in rs)
    print(f"{mdl:22s} n={len(rs)} fp={sum(r['rows']['fp'] for r in rs)} tp={sum(r['rows']['tp'] for r in rs)} dip={dip}/{ons}")
print()
print("=== R8 H1 per fold (cek tabel bagian 4) ===")
for r in sorted([x for x in r8["rows"] if x["model"]=="H1_stat_dan_rule"], key=lambda x:x["fold"]):
    print(f"{r['fold']:7s} fp={r['rows']['fp']:4d} tp={r['rows']['tp']:5d} h={r['h_terpilih']}")
