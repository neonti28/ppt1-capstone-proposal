import json

r = json.load(open("s2_ringkas.json"))
for k in ("vib", "ssi"):
    d = r[k]
    print("==", k, "single_terbaik:", d["single_terbaik"], "hybrid_terbaik:", d["hybrid_terbaik"])
    print("   peringkat_single:", d["peringkat_single"][:3])
    print("   peringkat_hybrid:", d["peringkat_hybrid"][:3])
    a = d["agregat"]
    print("   max recall_median:", max(a[m]["recall_median"] for m in a),
          "min recall_median:", min(a[m]["recall_median"] for m in a))
    print("   max precision_median:", max(a[m]["precision_median"] for m in a))
    print("   H2_ML_kalender_dan_stat:", {x: a["H2_ML_kalender_dan_stat"][x] for x in
          ("recall_median", "precision_median", "far24_kalender_median")})
    print("   H1b:", {x: a["H1b_stat_atau_rule"][x] for x in
          ("recall_median", "precision_median", "far24_kalender_median")})
    print("   ML_kalender:", {x: a["ML_kalender"][x] for x in
          ("recall_median", "precision_median", "far24_kalender_median", "fold_lolos_far_recall")})
    print("   sens max recall:", max((v["recall_median"], m) for m, v in d["sensitivitas"].items()))
    print("   sens ML192:", d["sensitivitas"]["ML_kalender_b192"])
    print("   sens ML24:", d["sensitivitas"]["ML_kalender_b24"])
    print("   banding:", d["banding_hybrid_lawan_single"])
    print("   separuh H1b/H2b:", d["lapisan_c_separuh"]["H1b_stat_atau_rule"],
          d["lapisan_c_separuh"]["H2b_ML_kalender_atau_stat"])
    print("   auc_ml range:", min(w["auc_ml"] for w in d["wells"]), max(w["auc_ml"] for w in d["wells"]))
    print("   kanal per fold:", [(w["fold"], w["kanal"]) for w in d["wells"]])
    print("   cakupan:", a["persistence"]["cakupan_median"], "n_pos_total:", d["n_pos_total_dapat_diuji"])
print("justifikasi:", [(j["n_pos"], j["lebar_penuh"], j["wilson_recall_penuh"]["lo"]) for j in r["justifikasi_ambang_positif"]])
