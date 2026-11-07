import json
B = "/mnt/d/Capstone 1(v2)"
d = json.load(open(f"{B}/scratch/rnd/s1/s1_hyd_seeds.json"))
folds = d["per_seed"]["42"]["folds"]
print("model tersedia:", sorted({r["model"] for r in folds}))
print()
hdr = f"{'model':20}{'fold':8}{'tp':>6}{'fp':>6}{'prec':>8}{'rec':>8}{'far24_row':>11}{'far24_kal':>11}{'lead':>7}{'cak':>8}"
print(hdr)
for r in folds:
    if r["fold"] in ("F-14",):
        print(f"{r['model']:20}{r['fold']:8}{r['rows']['tp']:6d}{r['rows']['fp']:6d}"
              f"{str(round(r['rows']['precision'],4)):>8}{str(round(r['rows']['recall'],4)):>8}"
              f"{r['far24_baris']:11.4f}{r['far24_kalender']:11.4f}"
              f"{str(r['lead']['lead_median_min']):>7}{r['cakupan']:8.4f}")
print()
print("=== semua fold H1: far24_baris ===")
for r in folds:
    if r["model"] == "H1_stat_dan_rule":
        print(f"  {r['fold']:8} n={r['n']:6d} pos={r['n_pos']:5d} fp={r['rows']['fp']:4d} "
              f"far24_baris={r['far24_baris']:8.3f} far24_kal={r['far24_kalender']:7.4f} h={r['h_terpilih']}")
