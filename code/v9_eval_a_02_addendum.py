import json, os, statistics

BASE = "/mnt/d/Capstone 1(v2)"
RES = os.path.join(BASE, "scratch/v9_eval_a/v9_eval_a_RESULTS.json")
R = json.load(open(RES))

def load(p):
    return json.load(open(p))

ml = {e: load(os.path.join(BASE, "scratch/v9_e_ml", f"v9_e_ML_{e}_RESULTS.json"))
      for e in ["vib", "ssi", "shk", "stuck_k2"]}
rule1 = load(os.path.join(BASE, "scratch/v9_e_rule", "v9_e_RULE_01_status_results.json"))

def stats(vals):
    vals = [v for v in vals if v is not None]
    if not vals:
        return None
    return {"min": min(vals), "median": statistics.median(vals), "max": max(vals), "n": len(vals)}

def pos_count(vals):
    vals = [v for v in vals if v is not None]
    return {"pos": sum(1 for v in vals if v > 0), "n": len(vals),
            "frac": (sum(1 for v in vals if v > 0) / len(vals)) if vals else None}

# (a) delta B: ML RF auprc - rule_display auprc per fold (join by well)
join = {}
for eng in ["vib", "ssi", "shk"]:
    rule_by_well = {f["test_well"]: f for f in rule1["classes"][eng]["folds"]}
    rows = []
    for f in ml[eng]["folds"]:
        w = f["test_well"]
        rf = f["models"]["rf"]["auprc"]
        rb = rule_by_well.get(w, {}).get("rule_display_t0minus1", {}).get("auprc")
        pe = rule_by_well.get(w, {}).get("persistence", {}).get("auprc")
        hy = rule_by_well.get(w, {}).get("hybrid_rule_and_persistence", {}).get("auprc")
        rows.append({"well": w, "underpowered": f["underpowered"], "rf": rf,
                     "rule": rb, "persistence": pe, "hybrid": hy,
                     "dB_rf_vs_rule": (rf - rb) if rb is not None else None,
                     "dB_rf_vs_persistence": (rf - pe) if pe is not None else None})
    join[eng] = {"rows": rows,
                 "dB_rf_vs_rule_layak": pos_count([r["dB_rf_vs_rule"] for r in rows if not r["underpowered"]]),
                 "dB_rf_vs_persistence_layak": pos_count([r["dB_rf_vs_persistence"] for r in rows if not r["underpowered"]]),
                 "n_rows_matched": sum(1 for r in rows if r["rule"] is not None)}
R["ml_vs_rule_join"] = join

# stuck_k1 fold wells
R["stuck_k1_folds"] = rule1["classes"]["stuck_k1"]["folds"]

# (b) hybrid & rule FP totals per class (sum fp across folds), + ssi rule n_nodata
fp_tot = {}
for cls, cd in rule1["classes"].items():
    rec = {}
    for meth in ["rule_display_t0minus1", "hybrid_rule_and_persistence", "persistence",
                 "rule_E1_2of3", "hybrid_E1_and_persistence"]:
        rows = [f[meth] for f in cd["folds"] if meth in f and "fp" in f[meth]]
        if rows:
            rec[meth] = {"fp_total": sum(r["fp"] for r in rows),
                         "tp_total": sum(r["tp"] for r in rows),
                         "fn_total": sum(r["fn"] for r in rows),
                         "n_nodata_total": sum(r.get("n_nodata", 0) for r in rows)}
    fp_tot[cls] = rec
R["rule_counts_totals"] = fp_tot

# (c) hybrid AUPRC vs persistence per fold for hyd_ki (E_RULE claim: menang 9/9)
hyd = rule1["classes"]["hyd_ki"]["folds"]
hb = [{"well": f["test_well"], "hybrid": f["hybrid_rule_and_persistence"]["auprc"],
       "persistence": f["persistence"]["auprc"], "rule": f["rule_display_t0minus1"]["auprc"],
       "dB_hybrid_vs_persistence": f["hybrid_rule_and_persistence"]["auprc"] - f["persistence"]["auprc"],
       "fp_hybrid": f["hybrid_rule_and_persistence"]["fp"], "fp_persistence": f["persistence"]["fp"],
       "fp_rule": f["rule_display_t0minus1"]["fp"]} for f in hyd]
R["hyd_ki_hybrid_vs_persistence"] = {
    "rows": hb,
    "wins": sum(1 for r in hb if r["dB_hybrid_vs_persistence"] > 0), "n": len(hb),
    "fp_rule_total": sum(r["fp_rule"] for r in hb),
    "fp_hybrid_total": sum(r["fp_hybrid"] for r in hb),
    "fp_persistence_total": sum(r["fp_persistence"] for r in hb),
    "dB_stats": stats([r["dB_hybrid_vs_persistence"] for r in hb])}

# (d) ssi/shk rule n_nodata share (why recall rendah)
for cls in ["ssi", "shk", "vib"]:
    rec = fp_tot.get(cls, {}).get("rule_display_t0minus1")
    if rec:
        R["rule_counts_totals"][cls]["rule_display_t0minus1"]["n_nodata_total"] = rec["n_nodata_total"]

# (e) RF titik operasi "hemat-awas": list fold/tau dgn FAR<=6 & recall>0 + FAR<=1
practical = {}
for eng, d in ml.items():
    pts = []
    for m in ["rf", "gb", "lr"]:
        for f in d["folds"]:
            for t, tm in f["models"][m]["tau_metrics"].items():
                if t == "q95_train":
                    continue
                if tm["FAR_24jam"] <= 6 and tm["recall"] > 0:
                    ot = f["models"][m].get("onset_by_tau", {}).get(t, {})
                    pts.append({"model": m, "well": f["test_well"], "tau": t,
                                "P": tm["precision"], "R": tm["recall"], "FAR": tm["FAR_24jam"],
                                "B1": ot.get("B1_coverage"), "TLead": ot.get("TLead_median_mnt")})
    practical[eng] = {"points_FARle6_recall_pos": pts,
                      "n": len(pts),
                      "n_model_rf": sum(1 for p in pts if p["model"] == "rf"),
                      "points_FARle1": [p for p in pts if p["FAR"] <= 1]}
R["practical_operating_points"] = practical

# (f) rule FAR<=6 & recall>0 lists per class (untuk ringkasan)
rule_pts = {}
for cls, cd in rule1["classes"].items():
    pts = []
    for meth in ["rule_display_t0minus1", "hybrid_rule_and_persistence", "persistence"]:
        for f in cd["folds"]:
            if meth in f and "far_24h" in f[meth]:
                r = f[meth]
                if r["far_24h"] <= 6 and r.get("recall", 0) > 0:
                    pts.append({"meth": meth, "well": f["test_well"], "P": r["precision"],
                                "R": r["recall"], "FAR": r["far_24h"]})
    rule_pts[cls] = pts
R["rule_practical_points"] = rule_pts

with open(RES, "w") as fh:
    json.dump(R, fh, indent=1, ensure_ascii=False)

print("updated", RES)
print("\nml_vs_rule_join:")
for e, j in join.items():
    print(" ", e, "matched", j["n_rows_matched"],
          "dB_rf_vs_rule(layak)", j["dB_rf_vs_rule_layak"],
          "dB_rf_vs_pers(layak)", j["dB_rf_vs_persistence_layak"])
print("\nstuck_k1 folds:", [(f["test_well"], f["underpowered"], f["n"], f["pos"]) for f in R["stuck_k1_folds"]])
print("\nrule_counts_totals:")
for k, v in fp_tot.items():
    print(" ", k, v)
print("\nhyd hybrid vs persistence:", R["hyd_ki_hybrid_vs_persistence"]["wins"], "/",
      R["hyd_ki_hybrid_vs_persistence"]["n"],
      "fp rule", R["hyd_ki_hybrid_vs_persistence"]["fp_rule_total"],
      "fp hybrid", R["hyd_ki_hybrid_vs_persistence"]["fp_hybrid_total"],
      "fp persistence", R["hyd_ki_hybrid_vs_persistence"]["fp_persistence_total"],
      "dB", R["hyd_ki_hybrid_vs_persistence"]["dB_stats"])
print("\npractical points (FAR<=6 & R>0):")
for e, p in practical.items():
    print(" ", e, "n=", p["n"], "rf=", p["n_model_rf"], "le1=", len(p["points_FARle1"]))
    for pt in p["points_FARle6_recall_pos"]:
        print("    ", pt)
print("\nrule practical points:")
for e, p in rule_pts.items():
    print(" ", e, len(p))
    for pt in p[:6]:
        print("    ", pt)
