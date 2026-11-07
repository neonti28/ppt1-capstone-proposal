import json

d = json.load(open("/mnt/d/Capstone 1(v2)/scratch/rnd/s1/s1_hyd_seeds.json"))
r = d["reproduksi"]
print("=== ARITMETIKA YANG DIPAKAI DI DOKUMEN ===")

print("1. FP cut H1 vs rule  : (2105-935)/2105*100 =", round((2105 - 935) / 2105 * 100, 4))
print("2. rasio FAR kalender maks/min : 8.9132/0.4059 =", round(8.9132 / 0.4059, 4))
print("3. rasio FAR baris / FAR kalender median : 32.256/3.5302 =", round(32.256 / 3.5302, 4))
print("4. 1/cakupan_median : 1/0.0903 =", round(1 / 0.0903, 4))
print("5. FP H1 F-14 vs V9 hybrid : 215/110 =", round(215 / 110, 4),
      "-> lebih tinggi", round((215 / 110 - 1) * 100, 4), "persen")
print("6. TP H1 F-14 vs V9 hybrid : (516-443)/516*100 =", round((516 - 443) / 516 * 100, 4), "persen lebih rendah")
print("7. presisi F-14 selisih : 0.8243-0.6733 =", round(0.8243 - 0.6733, 4))
print("8. recall F-14 selisih : 0.5965-0.5121 =", round(0.5965 - 0.5121, 4))
print("9. FAR baris F-14 H1 vs V9 hybrid : 32.4664/16.611 =", round(32.4664 / 16.611, 4),
      "-> lebih tinggi", round((32.4664 / 16.611 - 1) * 100, 4), "persen")
print("10. laju h=30 F-12 / anggaran : 0.044114/0.0041666667 =", round(0.044114 / (6 / 1440), 4), "kali")
print("11. laju h=30 F-10 / anggaran : 0.017567/0.0041666667 =", round(0.017567 / (6 / 1440), 4), "kali")
print("12. h=300 / h=30 =", round(300 / 30, 4), "kali")
print("13. cakupan F-10 vs F-5 : 0.673/0.0171 =", round(0.673 / 0.0171, 4), "kali")
print("14. FP kontrol ML rentang relatif : 345/1076*100 =", round(345 / 1076 * 100, 4), "persen dari nilai minimum")
print("15. jumlah fold H1 =", len([x for x in d["per_seed"]["42"]["folds"] if x["model"] == "H1_stat_dan_rule"]))

print()
print("=== TABEL LINTAS SEED (untuk dokumen) ===")
metrik = ["fp_total", "tp_total", "precision_median", "recall_median",
          "far24_kalender_median", "far24_baris_median", "lead_median_median",
          "n_diperingatkan", "fold_far_le6", "fold_gate_A_baru", "cakupan_median"]
for m in metrik:
    v = d["lintas_seed"][m]
    ps = v["per_seed"]
    print(f"{m:26} per_seed={[ps[str(s)] for s in d['seed_list']]} median={v['median']} "
          f"min={v['min']} maks={v['maks']} rentang={v['rentang']}")
