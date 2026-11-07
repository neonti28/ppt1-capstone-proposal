#!/usr/bin/env python3
"""V9-EVAL_A: hitung metrik LAPISAN A (P, R, FAR, waktu deteksi) untuk 7 engine
dari JSON primer E_ML / E_STAT / E_RULE. Semua angka = turunan mekanis dari JSON.
Output: scratch/v9_eval_a/v9_eval_a_RESULTS.json
"""
import json, os, statistics, datetime

BASE = "/mnt/d/Capstone 1(v2)"
OUT_DIR = os.path.join(BASE, "scratch", "v9_eval_a")
os.makedirs(OUT_DIR, exist_ok=True)

def load(p):
    with open(p) as fh:
        return json.load(fh)

def stats(vals):
    vals = [v for v in vals if v is not None]
    if not vals:
        return None
    return {"min": min(vals), "median": statistics.median(vals),
            "max": max(vals), "n": len(vals)}

def pos_count(vals):
    vals = [v for v in vals if v is not None]
    return {"pos": sum(1 for v in vals if v > 0), "n": len(vals),
            "frac": (sum(1 for v in vals if v > 0) / len(vals)) if vals else None}

R = {}

# ---------------------------------------------------------------- meta
R["meta"] = {
    "task": "V9-EVAL_A",
    "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
    "framework": "Lapisan A operator: precision, recall, false alarm rate, waktu deteksi, "
                 "dibanding baseline RELEVAN per tugas; titik operasi praktis (grid), bukan satu ambang; "
                 "hasil = kemampuan+batas, bukan vonis biner",
    "far_convention_rig": "FAR_24jam = FP / (n_neg/60) * 24 = alarm palsu per 24 jam waktu operasi NEGATIF "
                          "(grid 60 detik; konvensi V8 claim1_eval + E_RULE meta)",
    "far_convention_bengkel": "tool_wear: alarm palsu per MENIT (domain bengkel 1 dtk; PM1 D-A7)",
    "fold_layak": "underpowered == False (positif < 30 per fold = UNDERPOWERED, dilabeli, tidak dihitung mayoritas)",
    "sources": [
        "scratch/v9_e_ml/v9_e_ML_{vib,ssi,shk,stuck_k2}_RESULTS.json",
        "scratch/v9_e_ml/v9_e_ML_stuck_k2_persistence_onset.json",
        "scratch/v9_e_stat/v9_e_stat_{01_hyd_ki,02_stuck_e2,03_tool_wear,04_fisher_pearson}_RESULTS.json",
        "scratch/v9_e_rule/v9_e_RULE_{01_status,02_stuck_onset,03_bitwear_toolwear,04_hyd_k2}_results.json",
        "docs/V9_PM1_ARCHITECTURE.md (spesifikasi + angka V8 OBSERVED sbg referensi)",
    ],
    "v8_reference_note": "Angka berlabel V8 = kutipan OBSERVED dari PM1 §2 (bukan eksekusi V9); "
                         "dipakai HANYA bila head tersebut tidak dijalankan ulang di V9.",
}

# ---------------------------------------------------------------- ML heads
ML_FILES = {"vib": "v9_e_ML_vib_RESULTS.json", "ssi": "v9_e_ML_ssi_RESULTS.json",
            "shk": "v9_e_ML_shk_RESULTS.json", "stuck_k2": "v9_e_ML_stuck_k2_RESULTS.json"}
BASELINES = ["persistence", "canary_depth", "prevalence_random"]
ml_all = {}
ml_point_total = {"grid_points": 0, "far6_recall_pos": 0, "far1_recall_pos": 0}

for eng, fn in ML_FILES.items():
    d = load(os.path.join(BASE, "scratch", "v9_e_ml", fn))
    folds = d["folds"]
    models = ["rf", "gb", "lr"]
    taus = list(folds[0]["models"]["rf"]["tau_metrics"].keys())
    grid_taus = [t for t in taus if t != "q95_train"]
    out = {
        "jenis_task": d["jenis_task"], "klaim_tugas": d["klaim_tugas"],
        "n_folds": len(folds),
        "folds": [{"fold": f["fold"], "test_well": f["test_well"], "n_test": f["n_test"],
                   "pos_test": f["pos_test"], "prev_test": f["prev_test"],
                   "underpowered": f["underpowered"]} for f in folds],
        "underpowered_folds": [f["test_well"] for f in folds if f["underpowered"]],
        "dataset_sha256": d["dataset_sha256"], "models": {},
    }
    for m in models:
        mo = {}
        a = [f["models"][m]["auprc"] for f in folds]
        lo = [f["models"][m]["ci95"][0] for f in folds]
        hi = [f["models"][m]["ci95"][1] for f in folds]
        li = [f["models"][m]["lift"] for f in folds]
        pl = [f["models"][m]["plafon_lift"] for f in folds]
        mo["auprc"] = stats(a)
        mo["ci95_lo_min"] = min(lo); mo["ci95_hi_max"] = max(hi)
        mo["ci95_contains_prev_folds"] = sum(
            1 for f in folds if f["models"][m]["ci95"][0] <= f["prev_test"] <= f["models"][m]["ci95"][1])
        mo["lift"] = stats(li); mo["plafon_lift"] = stats(pl)
        mo["delta_b"] = {}
        for b in BASELINES:
            key = f"{m}_vs_{b}"
            vals = [f["delta_B"].get(key) for f in folds]
            vals_layak = [f["delta_B"].get(key) for f in folds if not f["underpowered"]]
            mo["delta_b"]["vs_" + b] = {
                "all": pos_count(vals), "layak": pos_count(vals_layak),
                "stats": stats(vals),
                "values": [{"well": f["test_well"], "v": f["delta_B"].get(key),
                            "underpowered": f["underpowered"]} for f in folds]}
        ops = {}
        for t in taus:
            rows = [(f, f["models"][m]["tau_metrics"][t]) for f in folds]
            lay = [(f, r) for f, r in rows if not f["underpowered"]]
            o = {
                "n_folds": len(rows), "n_layak": len(lay),
                "P": stats([r["precision"] for _, r in rows]),
                "R": stats([r["recall"] for _, r in rows]),
                "FAR_24jam": stats([r["FAR_24jam"] for _, r in rows]),
                "P_layak": stats([r["precision"] for _, r in lay]),
                "R_layak": stats([r["recall"] for _, r in lay]),
                "FAR_layak": stats([r["FAR_24jam"] for _, r in lay]),
                "n_FARle6_recall_pos": sum(1 for _, r in rows if r["FAR_24jam"] <= 6 and r["recall"] > 0),
                "n_FARle1_recall_pos": sum(1 for _, r in rows if r["FAR_24jam"] <= 1 and r["recall"] > 0),
                "per_fold": [{"well": f["test_well"], "underpowered": f["underpowered"],
                              "P": r["precision"], "R": r["recall"], "FAR": r["FAR_24jam"]}
                             for f, r in rows],
            }
            ot0 = folds[0]["models"][m].get("onset_by_tau", {}).get(t)
            if ot0:
                o["onset"] = {
                    "B1": stats([fl["models"][m]["onset_by_tau"][t]["B1_coverage"] for fl in folds]),
                    "TLead_median_mnt": stats([fl["models"][m]["onset_by_tau"][t]["TLead_median_mnt"] for fl in folds]),
                    "n_events_per_fold": ot0["n_events"],
                }
            ops[t] = o
            if t in grid_taus:
                ml_all_point_total_key = None
        mo["operating_points"] = ops
        mo["far_grid_counts"] = {
            "definition": "point = (fold, model, tau) pada 5 tau grid pra-reg, semua fold",
            "n_points": len(folds) * len(grid_taus),
            "FARle6_recall_pos": sum(
                1 for f in folds for t in grid_taus
                if f["models"][m]["tau_metrics"][t]["FAR_24jam"] <= 6
                and f["models"][m]["tau_metrics"][t]["recall"] > 0),
            "FARle1_recall_pos": sum(
                1 for f in folds for t in grid_taus
                if f["models"][m]["tau_metrics"][t]["FAR_24jam"] <= 1
                and f["models"][m]["tau_metrics"][t]["recall"] > 0),
        }
        ml_point_total["grid_points"] += mo["far_grid_counts"]["n_points"]
        ml_point_total["far6_recall_pos"] += mo["far_grid_counts"]["FARle6_recall_pos"]
        ml_point_total["far1_recall_pos"] += mo["far_grid_counts"]["FARle1_recall_pos"]
        out["models"][m] = mo
    ml_all[eng] = out

R["ml_heads"] = ml_all
R["ml_far_grid_total"] = ml_point_total

# persistence-onset horizon variant (stuck_k2)
R["ml_persistence_onset_horizon"] = load(
    os.path.join(BASE, "scratch/v9_e_ml/v9_e_ML_stuck_k2_persistence_onset.json"))

# ---------------------------------------------------------------- RULE 01 status
rule1 = load(os.path.join(BASE, "scratch/v9_e_rule", "v9_e_RULE_01_status_results.json"))
r1 = {"meta": rule1["meta"], "classes": {}}
METHODS = ["persistence", "rule_display_t0minus1", "hybrid_rule_and_persistence",
           "canary_depth", "rule_E1_2of3", "hybrid_E1_and_persistence"]
for cls, cd in rule1["classes"].items():
    folds = cd["folds"]
    c = {"n_folds": len(folds),
         "folds": [{"fold": f["fold"], "test_well": f["test_well"], "n": f["n"],
                    "pos": f["pos"], "prev": f["prev"], "underpowered": f["underpowered"]}
                   for f in folds],
         "underpowered_folds": [f["test_well"] for f in folds if f["underpowered"]],
         "identity_rule_window_vs_label": cd.get("identity_rule_window_vs_label"),
         "methods": {}, "aggregate": cd.get("aggregate", {})}
    for meth in METHODS:
        present = [f[meth] for f in folds if meth in f]
        if not present:
            continue
        mrec = {
            "n_folds": len(present),
            "P": stats([x.get("precision") for x in present]),
            "R": stats([x.get("recall") for x in present]),
            "FAR_24jam": stats([x.get("far_24h") for x in present]),
            "auprc": stats([x.get("auprc") for x in present]),
            "lift": stats([x.get("lift") for x in present]),
            "n_FARle6_recall_pos": sum(1 for x in present if x.get("far_24h") is not None
                                       and x["far_24h"] <= 6 and x.get("recall", 0) > 0),
            "n_FARle1_recall_pos": sum(1 for x in present if x.get("far_24h") is not None
                                       and x["far_24h"] <= 1 and x.get("recall", 0) > 0),
            "per_fold": [{"well": f["test_well"], "underpowered": f["underpowered"],
                          "P": f[meth].get("precision"), "R": f[meth].get("recall"),
                          "FAR": f[meth].get("far_24h"), "auprc": f[meth].get("auprc")}
                         for f in folds if meth in f],
        }
        # dB vs persistence & vs prevalence (derived from JSON auprc)
        if meth != "persistence":
            dp, dv = [], []
            for f in folds:
                if meth in f and "persistence" in f and f[meth].get("auprc") is not None:
                    dp.append(f[meth]["auprc"] - f["persistence"].get("auprc"))
                if meth in f and f[meth].get("auprc") is not None and f.get("prev"):
                    dv.append(f[meth]["auprc"] - f["prev"])
            mrec["dB_vs_persistence"] = pos_count(dp)
            mrec["dB_vs_persistence_values"] = dp
            mrec["dB_vs_prevalence"] = pos_count(dv)
        c["methods"][meth] = mrec
    # prevalence baseline
    pr = [f.get("prevalence_random", {}) for f in folds]
    c["prevalence_random"] = {"auprc_emp": stats([x.get("auprc_emp") for x in pr]),
                              "prev": stats([f.get("prev") for f in folds])}
    r1["classes"][cls] = c
r1["rule_fp_total"] = {k: v["aggregate"].get("rule_display_total_fp")
                       for k, v in r1["classes"].items()}
R["rule_status"] = r1

# ---------------------------------------------------------------- RULE 02 stuck onset
rule2 = load(os.path.join(BASE, "scratch/v9_e_rule", "v9_e_RULE_02_stuck_onset_results.json"))
r2 = {"meta": rule2["meta"], "folds": [], "aggregate": rule2["aggregate"]}
for f in rule2["folds"]:
    fr = {"fold": f["fold"], "test_well": f["test_well"], "n": f["n"], "pos": f["pos"],
          "prev": f["prev"], "underpowered": f["underpowered"], "n_onsets": f["n_onsets"],
          "methods": {}}
    for meth in ["persistence_horizon", "persistence_event", "rule_E1_2of3",
                 "canary_depth", "prevalence_random"]:
        if meth not in f:
            continue
        mm = f[meth]
        rec = {"auprc": mm.get("auprc"), "lift": mm.get("lift")}
        if "precision" in mm:
            rec.update({"P": mm.get("precision"), "R": mm.get("recall"),
                        "FAR": mm.get("far_24h"), "tp": mm.get("tp"), "fp": mm.get("fp"),
                        "fn": mm.get("fn"), "n_neg": mm.get("n_neg")})
        if "onset" in mm:
            rec["onset"] = mm["onset"]
        if "auprc_emp" in mm:
            rec["auprc_emp"] = mm["auprc_emp"]
            rec["prev_analytic"] = mm.get("prev_analytic")
        fr["methods"][meth] = rec
    r2["folds"].append(fr)
# aggregate P/R/FAR + fp_alarm untuk E1 & persistence_event (cross-check B3)
for meth in ["persistence_horizon", "persistence_event", "rule_E1_2of3"]:
    rows = [f["methods"][meth] for f in r2["folds"] if meth in f["methods"] and "P" in f["methods"][meth]]
    r2.setdefault("op_aggregate", {})[meth] = {
        "P": stats([x["P"] for x in rows]), "R": stats([x["R"] for x in rows]),
        "FAR": stats([x["FAR"] for x in rows]),
        "n_FARle6_recall_pos": sum(1 for x in rows if x["FAR"] <= 6 and x["R"] > 0),
        "n_FARle1_recall_pos": sum(1 for x in rows if x["FAR"] <= 1 and x["R"] > 0),
        "fp_alarm_total": sum(x.get("onset", {}).get("fp_alarm", 0) for x in rows),
        "B1": stats([x.get("onset", {}).get("b1") for x in rows]),
        "TLead_median": stats([x.get("onset", {}).get("tlead_min", {}).get("median")
                               for x in rows]),
    }
R["rule_stuck_onset"] = r2

# ---------------------------------------------------------------- RULE 03 bit_wear / tool_wear baselines
rule3 = load(os.path.join(BASE, "scratch/v9_e_rule", "v9_e_RULE_03_bitwear_toolwear_results.json"))
bw = rule3["bitwear_k1"]
r3 = {"bitwear_k1": {"meta": bw["meta"], "n_folds": len(bw["folds"]), "folds": [], "aggregate": bw["aggregate"]}}
for f in bw["folds"]:
    fr = {"fold": f["fold"], "test_well": f["test_well"], "n": f["n"], "pos": f["pos"],
          "prev": f["prev"], "underpowered": f["underpowered"], "crosscheck_v6": f.get("crosscheck_v6")}
    for meth in ["persistence", "persistence_allrows", "canary_depth",
                 "prevalence_random", "hybrid_rule_and_persistence"]:
        if meth in f:
            mm = f[meth]
            rec = {k: mm.get(k) for k in ["auprc", "lift", "plafon", "prev", "n", "pos",
                                          "auprc_emp", "prev_analytic"]}
            rec = {k: v for k, v in rec.items() if v is not None}
            fr[meth] = rec
    if "persistence" in f and f.get("prev"):
        fr["dB_persistence_vs_prevalence"] = f["persistence"]["auprc"] - f["prev"]
        fr["dB_canary_vs_prevalence"] = f.get("canary_depth", {}).get("auprc", 0) - f["prev"]
    r3["bitwear_k1"]["folds"].append(fr)
tw = rule3["toolwear_kii"]
r3["toolwear_kii"] = {"meta": tw["meta"], "folds": []}
for f in tw["folds"]:
    fr = {"fold": f["fold"], "test_tool": f["test_tool"], "n": f["n"], "pos": f["pos"],
          "prev": f["prev"], "underpowered": f["underpowered"]}
    for meth in ["canary_3rms", "identity_run_majority", "persistence_diagnostic",
                 "prevalence_random"]:
        if meth in f:
            mm = f[meth]
            rec = {k: mm.get(k) for k in ["auprc", "lift", "plafon", "prev", "auprc_emp",
                                          "prev_analytic", "declared", "note"]}
            fr[meth] = {k: v for k, v in rec.items() if v is not None}
    r3["toolwear_kii"]["folds"].append(fr)
R["rule_bitwear_toolwear"] = r3

# ---------------------------------------------------------------- RULE 04 hyd K-ii
rule4 = load(os.path.join(BASE, "scratch/v9_e_rule", "v9_e_RULE_04_hyd_k2_results.json"))
R["rule_hyd_k2"] = rule4

# ---------------------------------------------------------------- STAT 01 hyd K-i
s1 = load(os.path.join(BASE, "scratch/v9_e_stat", "v9_e_stat_01_hyd_ki_RESULTS.json"))
st1 = {"engine": s1["engine"], "claim_task": s1["claim_task"], "jenis_engine": s1["jenis_engine"],
       "label_crosscheck": s1["label_crosscheck"], "n_folds": len(s1["folds"]),
       "folds": [], "summary": s1["summary"], "baselines": {}}
for f in s1["folds"]:
    e = f["engine_persistence"]
    st1["folds"].append({
        "fold": f["fold"], "test_well": f["test_well"], "n_test": f["n_test"],
        "n_pos": f["n_pos"], "prev": f["prev"], "underpowered": f["underpowered"],
        "n_prev_valid": f["n_prev_valid"],
        "auprc": e["auprc"], "ci95": e["ci95_auprc"], "lift": e["lift"],
        "lift_ceiling": e["lift_ceiling_1_over_prev"],
        "dB_vs_prev": e["dB_vs_prevalence_random"],
        "op": e["op"], "det": e.get("det"),
        "rule_z_manual": f.get("baseline_rule_z_manual")})
for key in ["P", "R", "FAR"]:
    fmap = {"P": "precision", "R": "recall", "FAR": "far_per_24h_neg"}
    st1["baselines"][key] = stats([f["op"][fmap[key]] for f in st1["folds"]])
st1["baselines"]["auprc"] = stats([f["auprc"] for f in st1["folds"]])
st1["baselines"]["ci95_lo_min"] = min(f["ci95"][0] for f in st1["folds"])
st1["baselines"]["ci95_hi_max"] = max(f["ci95"][1] for f in st1["folds"])
st1["baselines"]["dB_pos_folds"] = sum(1 for f in st1["folds"] if f["dB_vs_prev"] > 0)
st1["baselines"]["delay_median_min"] = stats([f["det"]["delay_median_min"] for f in st1["folds"] if f.get("det")])
st1["baselines"]["pct_detected_within_H10"] = stats([f["det"]["pct_detected_within_H10"] for f in st1["folds"] if f.get("det")])
st1["baselines"]["n_FARle6_recall_pos"] = sum(1 for f in st1["folds"] if f["op"]["far_per_24h_neg"] <= 6 and f["op"]["recall"] > 0)
st1["baselines"]["n_FARle1_recall_pos"] = sum(1 for f in st1["folds"] if f["op"]["far_per_24h_neg"] <= 1 and f["op"]["recall"] > 0)
st1["rule_z_tautology"] = s1["folds"][0].get("baseline_rule_z_manual")
R["stat_hyd_ki"] = st1

# ---------------------------------------------------------------- STAT 02 stuck E2
s2 = load(os.path.join(BASE, "scratch/v9_e_stat", "v9_e_stat_02_stuck_e2_RESULTS.json"))
st2 = {"engine": s2["engine"], "claim_task": s2["claim_task"], "jenis_engine": s2["jenis_engine"],
       "n_folds": len(s2["folds"]), "folds": [], "summary": s2["summary"]}
for f in s2["folds"]:
    e = f["engine_E2_stats"]
    st2["folds"].append({
        "fold": f["fold"], "test_well": f["test_well"], "n_test": f["n_test"],
        "n_pos": f["n_pos"], "prev": f["prev"], "underpowered": f["underpowered"],
        "n_onsets": f["n_onsets_from_runs"], "thr_q95_train": f["thr_q95_train"],
        "auprc": e["auprc"], "ci95": e["ci95_auprc"], "lift": e["lift"],
        "dB_vs_prev": e["dB_vs_prevalence_random"], "op_q95": e["op_q95"],
        "onset_level": e["onset_level"],
        "e0_literal": f["baseline_E0_persistence_literal"],
        "e0_v8": f["baseline_E0_persistence_v8_construction"]})
st2["op_aggregate"] = {
    "P": stats([f["op_q95"]["precision"] for f in st2["folds"]]),
    "R": stats([f["op_q95"]["recall"] for f in st2["folds"]]),
    "FAR": stats([f["op_q95"]["far_per_24h_neg"] for f in st2["folds"]]),
    "n_FARle6_recall_pos": sum(1 for f in st2["folds"] if f["op_q95"]["far_per_24h_neg"] <= 6 and f["op_q95"]["recall"] > 0),
    "n_FARle1_recall_pos": sum(1 for f in st2["folds"] if f["op_q95"]["far_per_24h_neg"] <= 1 and f["op_q95"]["recall"] > 0),
    "auprc": stats([f["auprc"] for f in st2["folds"]]),
    "ci95_contains_prev": sum(1 for f in st2["folds"] if f["ci95"][0] <= f["prev"] <= f["ci95"][1]),
    "recall_at_H": stats([f["onset_level"]["recall_at_H"] for f in st2["folds"]]),
    "TLead_median": stats([f["onset_level"]["TLead_median_min"] for f in st2["folds"]]),
    "e0_literal_recall_H": stats([f["e0_literal"]["onset_level"]["recall_at_H"] for f in st2["folds"]]),
    "e0_literal_TLead": stats([f["e0_literal"]["onset_level"]["TLead_median_min"] for f in st2["folds"]]),
}
R["stat_stuck_e2"] = st2

# ---------------------------------------------------------------- STAT 03 tool_wear K-i
s3 = load(os.path.join(BASE, "scratch/v9_e_stat", "v9_e_stat_03_tool_wear_RESULTS.json"))
st3 = {"engine": s3["engine"], "claim_task": s3["claim_task"], "jenis_engine": s3["jenis_engine"],
       "n_perm": s3["n_perm"], "part_A": s3["part_A_change_point"],
       "part_B": s3["part_B_within_tool_calibration"],
       "part_C": s3["part_C_operating_far_calibrated"],
       "part_D": s3["part_D_ranking_auprc"], "summary": s3["summary"]}
# agregat FAR-terkalibrasi per target
byt = {}
for row in st3["part_C"]:
    byt.setdefault(str(row["target_fp_per_min"]), []).append(row)
st3["part_C_by_target"] = {
    k: {"n_tools": len(v), "n_detected_R02": sum(1 for x in v if x["det_R02"]),
        "fp_R01": stats([x["fp_R01"] for x in v]),
        "TLead_s": stats([x["TLead_s"] for x in v]),
        "pct_R02_alarmed": stats([x["pct_R02_alarmed"] for x in v])}
    for k, v in byt.items()}
R["stat_tool_wear_ki"] = st3

# ---------------------------------------------------------------- STAT 04 hyd K-ii
s4 = load(os.path.join(BASE, "scratch/v9_e_stat", "v9_e_stat_04_fisher_pearson_RESULTS.json"))
R["stat_hyd_kii"] = s4

# ================================================================ RECOMPUTE CHECKS
chk = []
def add_check(kelas, sumber, metric, stored, recomputed, note="", tol=1e-9):
    ok = stored is not None and recomputed is not None and abs(stored - recomputed) <= tol
    chk.append({"kelas": kelas, "sumber": sumber, "metric": metric, "stored": stored,
                "recomputed": recomputed, "abs_diff": (abs(stored - recomputed)
                                                       if stored is not None and recomputed is not None else None),
                "ok": bool(ok), "note": note, "tol": tol})

# vib: ML RF tau 0.2 fold 0
f = ml_all["vib"]["models"]["rf"]["operating_points"]["0.2"]["per_fold"][0]
d = load(os.path.join(BASE, "scratch/v9_e_ml", ML_FILES["vib"]))
ff = d["folds"][0]["models"]["rf"]["tau_metrics"]["0.2"]
add_check("vib", "E_ML vib RF tau=0.2 fold0 F-14", "precision", ff["precision"],
          ff["TP"] / (ff["TP"] + ff["FP"]), "TP/(TP+FP)")
add_check("vib", "E_ML vib RF tau=0.2 fold0 F-14", "FAR_24jam", ff["FAR_24jam"],
          ff["FP"] / (ff["n_neg"] / 60) * 24, "FP/(n_neg/60)*24")
# ssi: RULE persistence fold 0
c = r1["classes"]["ssi"]
f0 = [x for x in c["folds"] if x["fold"] == 0][0]
mm = json.load(os.path.join(open(os.devnull, "w")) if False else open(
    os.path.join(BASE, "scratch/v9_e_rule", "v9_e_RULE_01_status_results.json")))["classes"]["ssi"]["folds"][0]["persistence"]
add_check("ssi", "E_RULE ssi persistence fold0 F-10", "precision", mm["precision"],
          mm["tp"] / (mm["tp"] + mm["fp"]), "TP/(TP+FP)")
add_check("ssi", "E_RULE ssi persistence fold0 F-10", "far_24h", mm["far_24h"],
          mm["fp"] / (mm["n_neg"] / 60) * 24, "FP/(n_neg/60)*24")
# shk: RULE rule_display fold0 + ML RF tau0.05 fold0
shk_raw = json.load(open(os.path.join(BASE, "scratch/v9_e_rule", "v9_e_RULE_01_status_results.json")))["classes"]["shk"]["folds"][0]["rule_display_t0minus1"]
add_check("shk", "E_RULE shk rule_display fold0 F-10", "precision", shk_raw["precision"],
          shk_raw["tp"] / (shk_raw["tp"] + shk_raw["fp"]), "TP/(TP+FP)")
add_check("shk", "E_RULE shk rule_display fold0 F-10", "far_24h", shk_raw["far_24h"],
          shk_raw["fp"] / (shk_raw["n_neg"] / 60) * 24, "FP/(n_neg/60)*24")
# stuck_k1: RULE rule_display fold0
sk1 = json.load(open(os.path.join(BASE, "scratch/v9_e_rule", "v9_e_RULE_01_status_results.json")))["classes"]["stuck_k1"]["folds"][0]["rule_display_t0minus1"]
add_check("stuck_k1", "E_RULE stuck_k1 rule_display fold0 F-14", "recall", sk1["recall"],
          sk1["tp"] / (sk1["tp"] + sk1["fn"]), "TP/(TP+FN)")
# stuck_k2: ML RF tau0.3 fold0 + STAT E2 op fold0
ff = load(os.path.join(BASE, "scratch/v9_e_ml", ML_FILES["stuck_k2"]))["folds"][0]["models"]["rf"]["tau_metrics"]["0.3"]
add_check("stuck_k2", "E_ML stuck_k2 RF tau=0.3 fold0 F-10", "precision", ff["precision"],
          ff["TP"] / (ff["TP"] + ff["FP"]), "TP/(TP+FP)")
add_check("stuck_k2", "E_ML stuck_k2 RF tau=0.3 fold0 F-10", "FAR_24jam", ff["FAR_24jam"],
          ff["FP"] / (ff["n_neg"] / 60) * 24, "FP/(n_neg/60)*24")
e2 = st2["folds"][0]["op_q95"]
add_check("stuck_k2", "E_STAT stuck_E2 op_q95 fold0 F-10", "far_per_24h_neg", e2["far_per_24h_neg"],
          e2["fp"] / (((e2["tp"] + e2["fp"] + e2["fn"] + e2["tn"]) - (e2["tp"] + e2["fn"])) / 60) * 24,
          "FP/(n_neg_eval/60)*24")
# hyd_ki: STAT fold0 op + RULE hybrid fold0
op = st1["folds"][0]["op"]
add_check("hyd_ki", "E_STAT hyd_ki persistence fold0 F-10", "precision", op["precision"],
          op["tp"] / (op["tp"] + op["fp"]), "TP/(TP+FP)")
add_check("hyd_ki", "E_STAT hyd_ki persistence fold0 F-10", "far_per_24h_neg", op["far_per_24h_neg"],
          op["fp"] / ((op["tp"] + op["fp"] + op["fn"] + op["tn"] - op["tp"] - op["fn"]) / 60) * 24,
          "FP/(n_neg_eval/60)*24")
hyb = json.load(open(os.path.join(BASE, "scratch/v9_e_rule", "v9_e_RULE_01_status_results.json")))["classes"]["hyd_ki"]["folds"][0]["hybrid_rule_and_persistence"]
add_check("hyd_ki", "E_RULE hyd_ki hybrid fold0 F-10", "far_24h", hyb["far_24h"],
          hyb["fp"] / (hyb["n_neg"] / 60) * 24, "FP/(n_neg/60)*24")
# hyd_kii: STAT fisher op
fop = s4["engine_fisher_pearson_variant"]["op_q95"]
add_check("hyd_kii", "E_STAT fisher-pearson varian op_q95", "far_per_24h_neg", fop["far_per_24h_neg"],
          fop["fp"] / (s4["engine_fisher_pearson_variant"]["n_test"] - s4["label_Kii"]["pos_windows"] * 0 + 8077) / 60 * 24
          if False else fop["fp"] / (8077 / 60) * 24, "FP/(n_neg/60)*24; n_neg=n_test-n_pos=8107-30=8077")
# bit_wear: lift = auprc/prev
b0 = r3["bitwear_k1"]["folds"][0]["persistence"]
add_check("bit_wear", "E_RULE bitwear persistence fold0", "lift", b0["lift"],
          b0["auprc"] / b0["prev"], "auprc/prev")
# tool_wear: precision cp + lift part D + FAR part C
a = st3["part_A"]["run_level_sig_p05_v8"]
add_check("tool_wear", "E_STAT tool_wear cp run-level p<=0.05", "precision", a["precision"],
          a["tp"] / (a["tp"] + a["fp"]), "TP/(TP+FP)")
d3 = st3["part_D"]
add_check("tool_wear", "E_STAT tool_wear part_D ranking", "lift", d3["lift"],
          d3["auprc_engine_5of27_score"] / d3["prev_identity_run"],
          "stored+input dibulatkan -> tol 1e-3", tol=1e-3)
c0 = st3["part_C"][0]
add_check("tool_wear", "E_STAT tool_wear part_C row0", "fp_R01_ge_target",
          1.0 if c0["fp_R01"] <= c0["target_fp_per_min"] * 60 else 0.0, 1.0,
          "ceklis: fp_R01=1 <= target 1/menit x 60 dtk? (target_fp_per_min=1.0)")
R["recompute_checks"] = chk

# ================================================================ CROSS-TEAM CHECKS
xchk = []
def add_x(name, a_label, a, b_label, b, tol=1e-6):
    ok = abs(a - b) <= tol
    xchk.append({"check": name, "a_label": a_label, "a": a, "b_label": b_label, "b": b,
                 "abs_diff": abs(a - b), "ok": bool(ok)})

# vib persistence auprc: ML (validprev) vs RULE (auprc_validprev)
mlv = load(os.path.join(BASE, "scratch/v9_e_ml", ML_FILES["vib"]))["folds"][0]["baselines"]["persistence"]["auprc"]
ruv = json.load(open(os.path.join(BASE, "scratch/v9_e_rule", "v9_e_RULE_01_status_results.json")))["classes"]["vib"]["folds"][0]["persistence"]["auprc_validprev"]
add_x("vib persistence AUPRC fold0 F-14 (ML validprev vs RULE validprev)", "E_ML", mlv, "E_RULE", ruv)
# hyd_ki persistence TP/FP: STAT vs RULE fold0
add_x("hyd_ki persistence TP fold0 F-10 (STAT vs RULE)", "E_STAT", st1["folds"][0]["op"]["tp"],
      "E_RULE", hyb["tp"] if False else json.load(open(os.path.join(BASE, "scratch/v9_e_rule", "v9_e_RULE_01_status_results.json")))["classes"]["hyd_ki"]["folds"][0]["persistence"]["tp"])
add_x("hyd_ki persistence FP fold0 F-10 (STAT vs RULE)", "E_STAT", st1["folds"][0]["op"]["fp"],
      "E_RULE", json.load(open(os.path.join(BASE, "scratch/v9_e_rule", "v9_e_RULE_01_status_results.json")))["classes"]["hyd_ki"]["folds"][0]["persistence"]["fp"])
# stuck_k2 persistence AUPRC: ML baseline vs RULE persistence_horizon fold0
mlp = load(os.path.join(BASE, "scratch/v9_e_ml", ML_FILES["stuck_k2"]))["folds"][0]["baselines"]["persistence"]["auprc"]
r2h = rule2["folds"][0]["persistence_horizon"]["auprc"]
add_x("stuck_k2 persistence-horizon AUPRC fold0 F-10 (ML vs RULE)", "E_ML", mlp, "E_RULE", r2h)
# hyd_kii label episodes: STAT vs RULE crosscheck_v8
add_x("hyd_K-ii n_episodes (E_STAT label vs E_RULE crosscheck)", "E_STAT", s4["label_Kii"]["n_episodes"],
      "E_RULE", rule4["crosscheck_v8"]["v8_n_episodes"])
# hyd_kii prev_test
add_x("hyd_K-ii prev_test (E_STAT vs E_RULE)", "E_STAT",
      s4["engine_fisher_pearson_variant"]["prev"], "E_RULE", rule4["test"]["prevalence_random"]["prev_analytic"])
R["cross_team_checks"] = xchk

# ================================================================ FP UNTUK B3 (EVAL_B)
R["fp_rule_for_B3"] = {
    "vib": {"fp_rule_display_total": r1["rule_fp_total"].get("vib"), "unit": "fold LOWO gabungan, t0-1 strict-past"},
    "ssi": {"fp_rule_display_total": r1["rule_fp_total"].get("ssi")},
    "shk": {"fp_rule_display_total": r1["rule_fp_total"].get("shk")},
    "stuck_k1": {"fp_rule_display_total": r1["rule_fp_total"].get("stuck_k1")},
    "hyd_ki": {"fp_rule_display_total": r1["rule_fp_total"].get("hyd_ki"),
               "note": "rule = PEMBENTUK LABEL (tautologi) -> FP = beban alarm sistem hari-ini"},
    "stuck_k2": {"fp_E1_alarm_total": r2.get("op_aggregate", {}).get("rule_E1_2of3", {}).get("fp_alarm_total"),
                 "fp_persistence_event_total": r2.get("op_aggregate", {}).get("persistence_event", {}).get("fp_alarm_total"),
                 "fp_persistence_horizon_total": r2.get("op_aggregate", {}).get("persistence_horizon", {}).get("fp_alarm_total")},
    "hyd_kii": {"fp_rule_zpit_evalrows": rule4["test"]["rule_zpit"]["fp_in_evalrows"],
                "note": "alarm dlm blok episode Dibuang dari baris eval -> FP eval=0 BY CONSTRUCTION; "
                        "TLead=0 (deteksi saat-kejadian); n_episode_minutes=" + str(rule4["test"]["rule_zpit"]["n_episode_minutes"])},
    "tool_wear": {"fp_R01_partB_range": st3["part_B"]["aggregate"].get("far_fp_per_min_R01_range"),
                  "fp_R01_partC": {k: v["fp_R01"] for k, v in st3["part_C_by_target"].items()},
                  "note": "part B kalibrasi 5/27 |z|>3 = FP/alat R01; part C = titik FAR-terkalibrasi per target"},
    "bit_wear": {"fp": None, "note": "P/R/FAR tidak dihitung E_RULE/E_STAT (field tidak ada) -> LAPISAN A P/R/FAR = BELUM TERUKUR"},
}

with open(os.path.join(OUT_DIR, "v9_eval_a_RESULTS.json"), "w") as fh:
    json.dump(R, fh, indent=1, ensure_ascii=False)

# ---------------------------------------------------------------- console summary
print("WROTE", os.path.join(OUT_DIR, "v9_eval_a_RESULTS.json"))
print("\n== recompute checks:", sum(1 for c in chk if c["ok"]), "/", len(chk), "OK")
for c in chk:
    if not c["ok"]:
        print("  FAIL:", c)
print("== cross-team checks:", sum(1 for c in xchk if c["ok"]), "/", len(xchk), "OK")
for c in xchk:
    if not c["ok"]:
        print("  DIFF:", c)
print("\n== ML far grid total:", ml_point_total)
for eng, o in ml_all.items():
    print(f"-- {eng}: folds={o['n_folds']} underpowered={o['underpowered_folds']}")
    for m in ["rf", "gb", "lr"]:
        mo = o["models"][m]
        print(f"   {m}: auprc {mo['auprc']['min']:.3f}-{mo['auprc']['max']:.3f} "
              f"CIprev={mo['ci95_contains_prev_folds']}/{o['n_folds']} "
              f"dBcanary={mo['delta_b']['vs_canary_depth']['all']['pos']}/{mo['delta_b']['vs_canary_depth']['all']['n']} "
              f"dBpersistence={mo['delta_b']['vs_persistence']['all']['pos']}/{mo['delta_b']['vs_persistence']['all']['n']} "
              f"far-grid={mo['far_grid_counts']}")
        for t, op in mo["operating_points"].items():
            far = op["FAR_24jam"]; P = op["P"]; Rc = op["R"]
            print(f"     tau={t}: P {P['min']:.2f}-{P['max']:.2f} R {Rc['min']:.2f}-{Rc['max']:.2f} "
                  f"FAR {far['min']:.1f}-{far['max']:.1f} | le6+R>0 {op['n_FARle6_recall_pos']}/{op['n_folds']} "
                  f"le1+R>0 {op['n_FARle1_recall_pos']}/{op['n_folds']}")
print("\n== RULE01 per class")
for cls, c in r1["classes"].items():
    print(f"-- {cls}: folds={c['n_folds']} up={c['underpowered_folds']} fp_rule={c['aggregate'].get('rule_display_total_fp')}")
    for meth, mrec in c["methods"].items():
        if mrec["P"]:
            print(f"     {meth}: P {mrec['P']['min']:.2f}-{mrec['P']['max']:.2f} "
                  f"R {mrec['R']['min']:.2f}-{mrec['R']['max']:.2f} "
                  f"FAR {mrec['FAR_24jam']['min']:.1f}-{mrec['FAR_24jam']['max']:.1f} "
                  f"le6 {mrec['n_FARle6_recall_pos']}/{mrec['n_folds']} le1 {mrec['n_FARle1_recall_pos']}/{mrec['n_folds']} "
                  f"auprc {mrec['auprc']['min']:.3f}-{mrec['auprc']['max']:.3f}")
        else:
            print(f"     {meth}: (tanpa P/R/FAR) auprc {mrec['auprc']['min']:.3f}-{mrec['auprc']['max']:.3f}")
print("\n== RULE02 stuck onset op aggregate")
for meth, agg in r2.get("op_aggregate", {}).items():
    print("  ", meth, json.dumps(agg, ensure_ascii=False))
print("\n== STAT hyd_ki:", json.dumps(st1["baselines"], ensure_ascii=False, default=str)[:600])
print("\n== STAT stuck_E2:", json.dumps(st2["op_aggregate"], ensure_ascii=False, default=str)[:600])
print("\n== STAT tool_wear part_C by target:", json.dumps(st3["part_C_by_target"], ensure_ascii=False))
print("\n== FP for B3:", json.dumps(R["fp_rule_for_B3"], ensure_ascii=False, default=str))
