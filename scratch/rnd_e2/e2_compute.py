"""RND-E2: hitung semua angka turunan protokol + ASSERT terhadap sumber primer.

Setiap angka yang ditulis di docs/RND_E2_PROTOKOL.md harus lahir di sini dan
di-assert terhadap JSON/dokumen sumbernya. Bila assert gagal, skrip berhenti:
tidak ada angka yang lolos tanpa bukti.

Output: scratch/rnd_e2/e2_final.json
"""
from __future__ import annotations

import json
from pathlib import Path

BASE = Path("/mnt/d/Capstone 1(v2)")
S = BASE / "scratch/rnd_e2"

probe = json.loads((S / "e2_probe.json").read_text())
stats = json.loads((S / "e2_stats.json").read_text())
tw = json.loads((BASE / "scratch/v9_e_stat/v9_e_stat_03_tool_wear_RESULTS.json").read_text())
twp = json.loads((S / "e2_toolwear.json").read_text())
v9i1 = json.loads((BASE / "scratch/v9_i1/v9_i1_RESULTS.json").read_text())

R: dict = {}
A = tw["part_A_change_point"]
B = tw["part_B_within_tool_calibration"]
C = tw["part_C_operating_far_calibrated"]

# ---------------------------------------------------------------- 1. bengkel: FAR per menit
n_eval = {p["tool"]: p["n_eval_R01"] for p in B["per_tool"]}
make = {}
for row in C:
    if abs(row["target_fp_per_min"] - 1.0) > 1e-9:
        continue
    tool = row["tool"]
    n = n_eval[tool]
    jam_eval = n / 3600.0
    far_per_min = row["fp_R01"] / (n / 60.0)
    make[tool] = {
        "fp_R01": row["fp_R01"],
        "n_eval_jendela_1s": n,
        "jam_eval": round(jam_eval, 4),
        "far_fp_per_menit_eval": round(far_per_min, 4),
        "TLead_s": row["TLead_s"],
        "det_R02": row["det_R02"],
        "pct_R02_alarmed": row["pct_R02_alarmed"],
    }
R["tool_wear_partC_target1"] = make

fp_vals = [v["fp_R01"] for v in make.values()]
lead_vals = sorted(v["TLead_s"] for v in make.values())
assert fp_vals == [1, 3, 1, 3], fp_vals                     # EVAL_C "FP 1-3/alat"
assert lead_vals == [20, 24, 25, 36], lead_vals             # EVAL_C "TLead 20-36"
assert sorted(round(v["far_fp_per_menit_eval"], 2) for v in make.values()) == [1.43, 1.43, 4.5, 5.14]
n_lolos_far1 = sum(1 for v in make.values() if v["far_fp_per_menit_eval"] <= 1.0)
R["tool_wear_ringkas"] = {
    "fp_per_alat": fp_vals,
    "TLead_s": lead_vals,
    "TLead_median": (lead_vals[1] + lead_vals[2]) / 2,
    "TLead_rasio_maks_min": round(max(lead_vals) / min(lead_vals), 4),
    "far_eval_per_menit": sorted(round(v["far_fp_per_menit_eval"], 4) for v in make.values()),
    "n_alat_lolos_far_1_per_menit": n_lolos_far1,
    "n_alat": len(make),
    "det_R02": f"{sum(1 for v in make.values() if v['det_R02'])}/4",
}
assert R["tool_wear_ringkas"]["TLead_median"] == 24.5
assert R["tool_wear_ringkas"]["TLead_rasio_maks_min"] == 1.8
assert n_lolos_far1 == 0, n_lolos_far1     # TEMUAN: 0 dari 4 alat lolos <=1 alarm/menit di segmen evaluasi

# target 0.2 FP/menit tidak menurunkan FP di T02/T04 (kuantisasi hitungan fitur)
C02 = {r["tool"]: r for r in C if abs(r["target_fp_per_min"] - 0.2) < 1e-9}
R["tool_wear_target02"] = {t: {"fp_R01": r["fp_R01"], "TLead_s": r["TLead_s"]} for t, r in C02.items()}
assert C02["T02"]["fp_R01"] == 3 and C02["T04"]["fp_R01"] == 3
assert C02["T01"]["fp_R01"] == 1 and C02["T03"]["fp_R01"] == 1

# ---------------------------------------------------------------- 2. bengkel: presisi run
rl = A["run_level_sig_p05_v8"]
R["tool_wear_run_level"] = {"tp": rl["tp"], "fp": rl["fp"], "fn": rl["fn"], "tn": rl["tn"],
                            "precision": rl["precision"], "recall": rl["recall"],
                            "frac_sig_R01": rl["frac_sig_R01"]}
assert rl["precision"] == 0.5 and rl["recall"] == 1.0

# ---------------------------------------------------------------- 3. jumlah fold dan positif
und = stats["underpowered"]
R["fold"] = {k: {"n_folds": v["n_folds"], "n_fold_di_bawah_30": v["n_fold_di_bawah_30"],
                 "min_positif": v["min_positif"], "max_positif": v["max_positif"],
                 "label": v["label"]} for k, v in und.items()}
assert R["fold"]["hyd_ki"]["n_folds"] == 9
assert R["fold"]["shk"]["n_folds"] == 9
assert R["fold"]["hyd_ki"]["n_fold_di_bawah_30"] == 0
assert R["fold"]["shk"]["n_fold_di_bawah_30"] == 0
assert R["fold"]["shk"]["min_positif"] == 30
assert R["fold"]["vib"]["n_folds"] == 4

# ---------------------------------------------------------------- 4. jumlah head / tier
eng = v9i1["engines"]
n_heads = sum(len(e["heads"]) for e in eng)
tiers = {}
for e in eng:
    for h in e["heads"]:
        tiers[h["tier"]] = tiers.get(h["tier"], 0) + 1
R["registry"] = {"n_engine": len(eng), "n_head": n_heads, "tier": tiers,
                 "auto_slots": v9i1.get("auto_critical_alarm_slots"),
                 "elapsed_s": v9i1["meta"]["elapsed_s"], "seed": v9i1["meta"]["seed"]}
assert n_heads == 27
assert tiers["PERINGATAN-BERPENGAWAS"] == 12
assert tiers["TREN"] == 13
assert tiers["BELUM LAYAK PAKAI"] == 2
assert "ALARM-OTOMATIS" not in tiers
assert R["registry"]["auto_slots"] == 0

# ---------------------------------------------------------------- 5. statistik protokol
R["sign_test"] = stats["sign_test"]
R["wilson_p05"] = stats["wilson_p05"]
R["wilson_n_untuk"] = stats["wilson_n_untuk"]
R["garwood"] = stats["garwood"]
R["jam_neg_min_per_fp"] = stats["jam_neg_min_per_fp"]
assert stats["sign_test"]["9"]["k_minimum_sepakat"] == 8
assert abs(stats["sign_test"]["9"]["daya_konkordansi"]["0.9"] - 0.7748) < 1e-9
assert stats["sign_test"]["4"]["k_minimum_sepakat"] is None
assert abs(stats["garwood"]["jam_neg_min_untuk_far6_dengan_0fp_konservatif"] - 14.7555) < 1e-6
assert stats["ssi_F9A"]["sertifikasi_far6_mungkin"] is False

# ---------------------------------------------------------------- 6. sensus seed / runtime
R["seed_rencana"] = [42, 43, 44, 45, 46]
R["seed_primer"] = 42
R["runtime_anchor_s"] = v9i1["meta"]["elapsed_s"]   # 1 lintasan 7 engine prototipe
R["budget"] = {
    "per_fold_menit": 12,
    "n_fold_hyd": 9, "n_fold_shk": 9, "n_fold_tw": 4,
    "n_seed": 5,
    "total_fold_run": (9 + 9 + 4) * 5,
    "catatan": "12 menit per fold x 22 fold x 5 seed = 110 fold-run; runtime maksimum pilot 1.320 menit",
}
R["budget"]["total_menit"] = R["budget"]["total_fold_run"] * R["budget"]["per_fold_menit"]
assert R["budget"]["total_menit"] == 1320

# ---------------------------------------------------------------- 7. dataset bengkel
R["tool_wear_data"] = {"n_rows": twp["n_rows"], "n_cols": twp["n_cols"],
                       "n_units": twp["n_units"], "per_unit": twp["per_unit"]}
assert twp["n_rows"] == 469 and twp["n_units"] == 4

(S / "e2_final.json").write_text(json.dumps(R, indent=2, ensure_ascii=False))
print("SEMUA ASSERT LOLOS")
print(json.dumps({k: R[k] for k in ("tool_wear_ringkas", "tool_wear_run_level", "registry",
                                    "budget", "wilson_n_untuk")}, indent=2, ensure_ascii=False))
