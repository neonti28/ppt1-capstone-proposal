#!/usr/bin/env python3
"""V9-EVAL_B 01 — ekstrak metrik LAPISAN B (B1/B2/B3 inputs) dari JSON primer engine.

Sumber (semua OBSERVED, tanpa komputasi ulang metrik A):
- scratch/v9_e_ml/v9_e_ML_*.json        (B1/TLead onset stuck_k2; window-FP RF per tau)
- scratch/v9_e_rule/v9_e_RULE_01_*.json  (FP rule/persistence/hybrid per kelas status)
- scratch/v9_e_rule/v9_e_RULE_02_*.json  (B1/TLead onset stuck_k2: persistence/event/horizon, E1)
- scratch/v9_e_rule/v9_e_RULE_04_*.json  (hyd_kii: rule z-pit load, B1=0)
- scratch/v9_e_stat/v9_e_stat_01_hyd_ki*.json   (delay konfirmasi hyd_ki)
- scratch/v9_e_stat/v9_e_stat_02_stuck_e2*.json (B1/TLead E2)
- scratch/v9_e_stat/v9_e_stat_03_tool_wear*.json (TLead bengkel, kurangi_ragu)
- scratch/v9_e_stat/v9_e_stat_04_fisher*.json    (B1/TLead hyd_kii varian)

Output: scratch/v9_eval_b/_A_json.json (+ log)
Definisi: V8_R1_ABC_SPEC.md §1.3 (B1..B4) + V9_PM1_ARCHITECTURE.md §4.7.
"""
import json, os, statistics as stat

S = "/mnt/d/Capstone 1(v2)/scratch"
OUT = f"{S}/v9_eval_b"
os.makedirs(OUT, exist_ok=True)


def num(vals):
    v = [x for x in vals if x is not None]
    if not v:
        return {"n": 0}
    return {"n": len(v), "min": min(v), "median": stat.median(v), "max": max(v),
            "values": v}


def load(p):
    with open(p) as f:
        return json.load(f)


A = {"meta": {
        "task": "V9-EVAL_B 01 — ekstrak B1/B2/B3 dari JSON primer",
        "defs": {
            "B1": "% onset terdeteksi alarm dalam [t_e - H, t_e), H=10 mnt (V8_R1 §1.3)",
            "B2": "TLead median/IQR vs anchor KELAS; kategorikal >=30 / 10-30 / <10 / nol mnt; anchor stuck=2.67-7.37 mnt (Crossformer Volve, R1-S1 §2.2) DILARANG dipinjam ke kelas lain",
            "B3": "kurangi_ragu = 1 - FP_engine / FP_baseline_rule (baseline = aturan status-quo; PM1 §4.7)",
            "B4": "median jendela (menit) antara alarm terdekat sebelum masuk blok status berkelanjutan (>=5 mnt) — dihitung di skrip 02",
        },
        "units": "FP = jendela (grid 1 mnt) kecuali dinyatakan lain; TLead = menit; tool_wear = detik bengkel",
     },
     "onset": {}, "B3": {}, "status_delay": {}, "belum": {}}

TAUS = ["0.05", "0.1", "0.2", "0.3", "0.5"]

# ---------------------------------------------------------------- stuck_k2 ML
ml = load(f"{S}/v9_e_ml/v9_e_ML_stuck_k2_RESULTS.json")
stuck_ml = {"jenis_task": ml["jenis_task"], "H_menit": 10, "anchor_kelas": [2.67, 7.37],
            "models": {}}
for model in ["rf", "gb", "lr"]:
    per_tau = {}
    for tau in TAUS + ["q95_train"]:
        b1s, tms, iqr_lo, iqr_hi, fpx, tpx, fars = [], [], [], [], [], [], []
        for f in ml["folds"]:
            ob = f["models"][model].get("onset_by_tau", {}).get(tau)
            if ob:
                b1s.append(ob["B1_coverage"])
                tms.append(ob["TLead_median_mnt"])
                if ob.get("TLead_iqr_mnt"):
                    iqr_lo.append(ob["TLead_iqr_mnt"][0])
                    iqr_hi.append(ob["TLead_iqr_mnt"][1])
            tm = f["models"][model]["tau_metrics"].get(tau)
            if tm:
                fp = tm.get("FP", tm.get("fp"))
                tp = tm.get("TP", tm.get("tp"))
                far = tm.get("FAR_24jam", tm.get("far_24h"))
                if fp is not None:
                    fpx.append(fp)
                if tp is not None:
                    tpx.append(tp)
                if far is not None:
                    fars.append(far)
        per_tau[tau] = {
            "B1_coverage": num(b1s), "TLead_median_mnt": num(tms),
            "TLead_iqr_lo": num(iqr_lo), "TLead_iqr_hi": num(iqr_hi),
            "FP_window_total": sum(fpx) if fpx else None,
            "TP_window_total": sum(tpx) if tpx else None,
            "FAR_24jam_range": [min(fars), max(fars)] if fars else None,
            "n_folds": len(b1s),
        }
    stuck_ml["models"][model] = per_tau
# q95 keys of first fold for audit
stuck_ml["_q95_keys"] = list(ml["folds"][0]["models"]["rf"]["tau_metrics"]["q95_train"].keys())
stuck_ml["_q95_threshold"] = ml["folds"][0]["models"]["rf"]["q95_train"]
stuck_ml["_folds"] = [{"fold": f["fold"], "test_well": f["test_well"],
                       "pos": f["pos_test"], "underpowered": f["underpowered"]}
                      for f in ml["folds"]]
A["onset"]["stuck_k2_ML"] = stuck_ml

# ------------------------------------------------------------- stuck_k2 E_RULE
r2 = load(f"{S}/v9_e_rule/v9_e_RULE_02_stuck_onset_results.json")
stuck_rule = {"anchor_kelas": [2.67, 7.37], "metode": {}}
for meth in ["persistence_horizon", "persistence_event", "rule_E1_2of3"]:
    b1s, tms, wfp, wfpr, afp = [], [], [], [], []
    for f in r2["folds"]:
        m = f[meth]
        o = m.get("onset", {})
        b1s.append(o.get("b1"))
        tms.append((o.get("tlead_min") or {}).get("median"))
        wfp.append(m.get("fp"))
        afp.append((o.get("fp_alarm")))
    stuck_rule["metode"][meth] = {
        "B1": num(b1s), "TLead_median_mnt": num(tms),
        "FP_window_total": sum(x for x in wfp if x is not None),
        "FP_alarm_total": sum(x for x in afp if x is not None),
        "n_onsets_per_fold": [f.get("n_onsets") for f in r2["folds"]],
        "hindsight": meth == "persistence_horizon",
        "catatan": ("label horizon kontigu [t_e-10,t_e) -> y(t-1) 'tahu' isi horizon = HINDSIGHT"
                    if meth == "persistence_horizon" else
                    ("alarm = status ONSET kemarin (deployable)" if meth == "persistence_event"
                     else "rule E1 2-dari-3 (TQA|HKLD|ROP-drop)")),
    }
stuck_rule["aggregate_json"] = r2.get("aggregate")
A["onset"]["stuck_k2_RULE"] = stuck_rule

# ------------------------------------------------------------- stuck_k2 E_STAT
s2 = load(f"{S}/v9_e_stat/v9_e_stat_02_stuck_e2_RESULTS.json")
e2 = {"anchor_kelas": [2.67, 7.37], "per_fold": []}
for f in s2["folds"]:
    on = f["engine_E2_stats"]["onset_level"]
    op = f["engine_E2_stats"]["op_q95"]
    e0 = f["baseline_E0_persistence_literal"]["onset_level"]
    e2["per_fold"].append({
        "test_well": f["test_well"], "n_onsets": on.get("onsets"),
        "B1_recall_at_H": on.get("recall_at_H"),
        "TLead_median_min": on.get("TLead_median_min"),
        "TLead_IQR_min": on.get("TLead_IQR_min"),
        "FP_window_q95": op.get("fp"), "FAR_q95_24h": op.get("far_per_24h_neg"),
        "E0_persistence_literal_B1": e0.get("recall_at_H"),
        "E0_TLead_median_min": e0.get("TLead_median_min"),
        "E0_catatan": e0.get("catatan"),
    })
e2["B1"] = num([x["B1_recall_at_H"] for x in e2["per_fold"]])
e2["TLead_median_min"] = num([x["TLead_median_min"] for x in e2["per_fold"]])
e2["summary_json"] = s2.get("summary")
A["onset"]["stuck_k2_STAT_E2"] = e2

# ----------------------------------------------------------------- hyd_kii
s4 = load(f"{S}/v9_e_stat/v9_e_stat_04_fisher_pearson_RESULTS.json")
r4 = load(f"{S}/v9_e_rule/v9_e_RULE_04_hyd_k2_results.json")
fv = s4["engine_fisher_pearson_variant"]
hyd2 = {
    "anchor_kelas": None,  # dilarang meminjam anchor stuck
    "varian_fisher_pearson_proxy": {
        "B1_recall_at_H": fv["onset_level"].get("B1_recall_at_H"),
        "onsets_test": fv["onset_level"].get("onsets_test"),
        "detected_at_H": fv["onset_level"].get("detected_at_H"),
        "TLead_median_min": fv["onset_level"].get("TLead_median_min"),
        "FP_window_q95": fv["op_q95"].get("fp"),
        "FAR_q95_24h": fv["op_q95"].get("far_per_24h_neg"),
        "catatan": "FlowOut absen -> literal TIDAK DIJALANKAN; varian pakai dV_active/dt (proxy, risiko sirkularitas dinyatakan E_STAT)",
    },
    "rule_zpit_status_quo": {
        "B1_horizon_pct": r4["test"]["rule_zpit"].get("b1_horizon_pct"),
        "TLead_minutes": r4["test"]["rule_zpit"].get("tlead_minutes"),
        "tlead_all_zero": r4["test"]["rule_zpit"].get("tlead_all_zero"),
        "inspection_load": r4["test"]["rule_zpit"].get("inspection_load"),
        "FP_window_eval": r4["test"]["rule_zpit"].get("fp_in_evalrows"),
        "catatan": "TLead=0 BY CONSTRUCTION (alarm di menit pertama episode); blok episode +30 mnt dibuang dari baris eval",
    },
    "always_negative": r4["test"]["always_negative"],
    "RF_V8_referensi": {
        "B1": 0.667, "B1_note": "66,7% (2/3 onset), 1 wellbore, 3 onset = UNDERPOWERED",
        "TLead_median_min": 7.0, "FAR_24h": 5.9,
        "sumber": "PM1 §2.5 kutipan OBSERVED V8-E_hyd — TIDAK dijalankan ulang di V9 (EA-7)",
    },
}
A["onset"]["hyd_kii"] = hyd2

# ------------------------------------------------- tool_wear (bengkel, detik)
s3 = load(f"{S}/v9_e_stat/v9_e_stat_03_tool_wear_RESULTS.json")
pa = s3["part_A_change_point"]
pb = s3["part_B_within_tool_calibration"]
pc = s3["part_C_operating_far_calibrated"]
tw = {
    "anchor_kelas": "RUL bengkel (akhir run R02 = alat tumpul); anchor numerik formal TIDAK didefinisikan di PM1/R1 -> dilaporkan absolut (detik) + kategorikal <10 mnt",
    "K_i": {
        "change_point_TLead_to_end_R02_s": pa.get("TLead_to_end_R02_s"),
        "cross_family_spread_s": pa.get("cross_family_spread_s"),
        "kalibrasi5of27_TLead_median_s": pb["aggregate"].get("TLead_median_s"),
        "kalibrasi5of27_TLead_range_s": pb["aggregate"].get("TLead_range_s"),
        "kalibrasi5of27_B1_pct": pb["aggregate"].get("B1_pct_detected_before_end_R02"),
        "kalibrasi5of27_FAR_range_per_min": pb["aggregate"].get("far_fp_per_min_R01_range"),
        "kalibrasi5of27_kurangi_ragu_vs_rule3RMS_range": pb["aggregate"].get("kurangi_ragu_range"),
        "FAR_terkalibrasi_per_tool": [
            {"target_fp_per_min": c["target_fp_per_min"], "tool": c["tool"],
             "fp_R01": c["fp_R01"], "det_R02": c["det_R02"],
             "first_alarm_s": c["first_alarm_s"], "TLead_s": c["TLead_s"],
             "pct_R02_alarmed": c["pct_R02_alarmed"]} for c in pc],
        "B3_FAR_terkalibrasi_per_tool": [],  # dihitung di bawah
    },
    "K_ii": {
        "V9_baseline": "canary 3-RMS + identity-majority (AUPRC; tanpa TLead)",
        "RF_V8_referensi_TLead_median_s": 47.5,
        "RF_V8_referensi_TLead_range_s": [35, 59],
        "RF_V8_referensi_note": "FAR-terkalibrasi <=1/menit, deteksi 4/4, FP 1-3 (V8, EA-7)",
    },
}
# baseline rule 3RMS FP R01 per tool dari part B
rule_fp = {t["tool"]: t["baseline_rule_3RMS"]["fp_R01"] for t in pb["per_tool"]}
tw["K_i"]["baseline_rule_3RMS_fp_R01"] = rule_fp
for c in pc:
    b = 1 - c["fp_R01"] / rule_fp[c["tool"]]
    tw["K_i"]["B3_FAR_terkalibrasi_per_tool"].append(
        {"tool": c["tool"], "target_fp_per_min": c["target_fp_per_min"],
         "FP_engine": c["fp_R01"], "FP_rule3RMS": rule_fp[c["tool"]],
         "kurangi_ragu": b})
A["onset"]["tool_wear"] = tw

# --------------------------------------------------- B3 kelas status (FP totals)
r1 = load(f"{S}/v9_e_rule/v9_e_RULE_01_status_results.json")
A["B3"]["kelas_status_FP"] = {}
for cls, c in r1["classes"].items():
    folds = c["folds"]
    ent = {"n_folds_E_RULE": len(folds),
           "test_wells": [f["test_well"] for f in folds],
           "FP_totals": {}}
    for meth in ["persistence", "rule_display_t0minus1", "hybrid_rule_and_persistence",
                 "rule_E1_2of3", "hybrid_E1_and_persistence"]:
        fps = [f.get(meth, {}).get("fp") for f in folds if meth in f]
        if fps and any(x is not None for x in fps):
            ent["FP_totals"][meth] = sum(x for x in fps if x is not None)
    ent["rule_display_total_fp_json"] = c["aggregate"].get("rule_display_total_fp")
    ent["n_nodata_rule_total"] = sum(f.get("rule_display_t0minus1", {}).get("n_nodata", 0)
                                     for f in folds)
    A["B3"]["kelas_status_FP"][cls] = ent

# FP RF/GB/LR per tau (window) dari E_ML utk kelas dengan head ML
A["B3"]["ML_FP_window"] = {}
for eng in ["vib", "ssi", "shk", "stuck_k2"]:
    m = load(f"{S}/v9_e_ml/v9_e_ML_{eng}_RESULTS.json")
    ent = {}
    for model in ["rf", "gb", "lr"]:
        ent[model] = {}
        for tau in TAUS:
            fp = sum(f["models"][model]["tau_metrics"][tau]["FP"] for f in m["folds"])
            tp = sum(f["models"][model]["tau_metrics"][tau]["TP"] for f in m["folds"])
            ent[model][tau] = {"FP": fp, "TP": tp}
        # q95 utk stuck_k2
        if eng == "stuck_k2":
            q = [f["models"][model]["tau_metrics"].get("q95_train") for f in m["folds"]]
            if q and all(q):
                ent[model]["q95_train"] = {
                    "FP": sum(x.get("FP", x.get("fp", 0)) for x in q),
                    "TP": sum(x.get("TP", x.get("tp", 0)) for x in q),
                    "keys": list(q[0].keys())}
    A["B3"]["ML_FP_window"][eng] = ent

# hyd_ki persistence/hybrid FP dari E_STAT (op) -> cross-check E_RULE
s1 = load(f"{S}/v9_e_stat/v9_e_stat_01_hyd_ki_RESULTS.json")
A["status_delay"]["hyd_ki"] = {
    "persistence_det_per_fold": [
        {"test_well": f["test_well"], **f["engine_persistence"].get("det", {}),
         "FP": f["engine_persistence"]["op"].get("fp")} for f in s1["folds"]],
    "rule_z_manual": {
        "n_label_rule_alarms_fold0": s1["folds"][0]["baseline_rule_z_manual"].get("n_label_rule_alarms"),
        "note": s1["folds"][0]["baseline_rule_z_manual"].get("note")},
}
A["status_delay"]["hyd_ki"]["persistence_FP_total_STAT"] = sum(
    x["FP"] for x in A["status_delay"]["hyd_ki"]["persistence_det_per_fold"])
A["status_delay"]["hyd_ki"]["delay_median_range_min"] = num(
    [x["delay_median_min"] for x in A["status_delay"]["hyd_ki"]["persistence_det_per_fold"]])
A["status_delay"]["hyd_ki"]["pct_within_H10_range"] = num(
    [x["pct_detected_within_H10"] for x in A["status_delay"]["hyd_ki"]["persistence_det_per_fold"]])

# ------------------------------------------------------------- belum terukur
A["belum"] = {
    "bit_wear_K1": "FP/TP tidak dihitung E_RULE utk kelas ini (EVAL_A §2.6) -> B3 belum terukur; B4 per-baris = dataset USROP di luar pipeline D1 (6 dataset) -> lihat skrip 02 utk status konstruksi",
    "bit_wear_K2": "pra-reg K-2 belum terbit (E_RULE DoD-d) -> B1/B2/B3/B4 belum terukur, bukan gagal",
    "kontrol_positif_stuck": "labels_curated_v2 (884 event) BELUM tersinkron zona-waktu dgn ts_bin (tripwire terbuka PM1 §5.1) -> validasi kejadian kurasi belum dilakukan di V9; angka V8 = kontrol-positif 0/10 (F-14) sbg referensi",
    "RF_hyd_kii_bitwear_toolwear_Kii_V9": "tidak dijalankan di V9 (EA-7) -> TLead/B1 V9 untuk head tsb = referensi V8",
}

outp = f"{OUT}/_A_json.json"
json.dump(A, open(outp, "w"), indent=1, allow_nan=False)
print("saved", outp)

# ------------------------------------------------------------------ ringkasan
print("\n--- B1/B2 onset ringkas ---")
for tau in TAUS + ["q95_train"]:
    r = stuck_ml["models"]["rf"][tau]
    print(f"stuck RF tau={tau}: B1 {r['B1_coverage']} TLead {r['TLead_median_mnt']} FP={r['FP_window_total']}")
print("E2:", e2["B1"], e2["TLead_median_min"])
for meth, v in stuck_rule["metode"].items():
    print(f"RULE {meth}: B1 {v['B1']} TLead {v['TLead_median_mnt']} FPwin={v['FP_window_total']} FPalarm={v['FP_alarm_total']}")
print("\n--- B3 FP totals kelas status ---")
for cls, ent in A["B3"]["kelas_status_FP"].items():
    print(cls, ent["FP_totals"], "nodata", ent["n_nodata_rule_total"])
print("\nhyd_ki STAT FP total:", A["status_delay"]["hyd_ki"]["persistence_FP_total_STAT"])
print("tool_wear B3 FAR-cal:", tw["K_i"]["B3_FAR_terkalibrasi_per_tool"])
