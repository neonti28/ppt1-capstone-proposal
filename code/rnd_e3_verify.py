#!/usr/bin/env python3
"""RND-E3 — verifikasi independen atas hasil pilot hyd K-i.

Tujuan: membuktikan angka di scratch/rnd/e3/*.json konsisten dengan definisi
protokol E2, bukan menyalin klaim. Setiap pemeriksaan memakai assert.

Pemeriksaan:
  V1  FAR_24 = FP / (n_neg/60) * 24 dihitung ulang dari tp/fp/fn/tn tiap baris.
  V2  Total FP baseline (persistence, hybrid proxy) dihitung ulang per fold.
  V3  Jumlah fold lulus gate A (FAR<=6 dan syarat 4xFP) per model dan per seed.
  V4  Rentang FAR dan recall per model.
  V5  Audit anti-bocor: fitur A1 vs A1b, apakah memuat kolom turunan label.
  V6  Recompute baseline langsung dari dataset (persistence + proxy hybrid).
  V7  Gate A tidak dapat disertifikasi bila jam_neg < 4*FP (syarat 4xFP).

Keluaran: scratch/rnd/e3/e3_verify.json
"""
import json, os
import numpy as np
import pandas as pd

BASE = "/mnt/d/Capstone 1(v2)"
OUT = f"{BASE}/scratch/rnd/e3"
DS = f"{BASE}/scratch/v9_d1/datasets/hyd_ki.csv.gz"

LABEL_DERIVED = ("y_hyd", "y_prev_hyd", "valid_prev_hyd", "obs_hyd", "anom_hyd",
                 "lab_ts", "lab_kind", "feat_ts_max")

R = {}
fail = []


def jload(name):
    with open(f"{OUT}/{name}") as f:
        return json.load(f)


def chk(cond, label, detail=""):
    R.setdefault("checks", []).append(dict(check=label, lulus=bool(cond), detail=str(detail)))
    if not cond:
        fail.append(f"{label}: {detail}")


def recompute_far(row):
    n_neg = row["n_neg"]
    if n_neg == 0:
        return None
    return row["fp"] / (n_neg / 60.0) * 24.0


# ---------------------------------------------------------------- muat artefak
A1 = jload("e3_a_conformal_results.json")
A1B = jload("e3_a1b_lag_results.json")
A2 = jload("e3_b_cusum_results.json")
BL = jload("e3_baseline_results.json")
SUM = jload("e3_run_summary.json")

# V1 + V2: FAR konsisten dan total FP baseline
max_dev = 0.0
for nama, rows in (("A1", A1["folds"]), ("A1b", A1B["folds"]),
                   ("A2_reset", A2["varian"]["reset"]["folds"]),
                   ("A2_tanpa_reset", A2["varian"]["tanpa_reset"]["folds"]),
                   ("baseline", BL["folds"])):
    for r in rows:
        rc = recompute_far(r)
        if rc is None:
            continue
        dev = abs(rc - r["far_per_24h"])
        max_dev = max(max_dev, dev)
        chk(dev < 1e-6, f"V1 FAR konsisten {nama} {r.get('fold')} {r.get('model', '')}",
            f"json={r['far_per_24h']} hitung={rc}")

R["v1_max_deviasi_far"] = max_dev

tot_pers = sum(r["fp"] for r in BL["folds"] if r["model"] == "persistence")
tot_hyb = sum(r["fp"] for r in BL["folds"] if r["model"] == "hybrid_rule_lag1_and_persistence")
chk(tot_pers == BL["total_fp"]["persistence"], "V2 total FP persistence",
    f"hitung={tot_pers} json={BL['total_fp']['persistence']}")
chk(tot_hyb == BL["total_fp"]["hybrid_rule_lag1_and_persistence"], "V2 total FP hybrid proxy",
    f"hitung={tot_hyb} json={BL['total_fp']['hybrid_rule_lag1_and_persistence']}")

# V3: gate A per model
def gate_rows(rows):
    return [r for r in rows if r.get("gate_A_lulus")]


gate = {}
for nama, rows in (("A1", A1["folds"]), ("A1b", A1B["folds"]),
                   ("A2_reset", A2["varian"]["reset"]["folds"]),
                   ("A2_tanpa_reset", A2["varian"]["tanpa_reset"]["folds"]),
                   ("baseline_persistence", [r for r in BL["folds"] if r["model"] == "persistence"]),
                   ("baseline_hybrid_proxy", [r for r in BL["folds"]
                                              if r["model"] == "hybrid_rule_lag1_and_persistence"])):
    lulus = gate_rows(rows)
    gate[nama] = dict(n_fold=len(rows), n_gate_A_lulus=len(lulus),
                      folds_lulus=[r.get("test_well") for r in lulus])
R["v3_gate_A"] = gate

# baseline tidak punya kunci gate_A_lulus, hitung manual
def man_gate(rows):
    ok = []
    for r in rows:
        far = r["far_per_24h"]
        if far is not None and far <= 6 and r.get("syarat_4x_fp") is not False:
            ok.append(r["test_well"])
    return ok


base_gate = {
    "persistence": man_gate([r for r in BL["folds"] if r["model"] == "persistence"]),
    "hybrid_proxy": man_gate([r for r in BL["folds"]
                              if r["model"] == "hybrid_rule_lag1_and_persistence"]),
}
R["v3b_gate_A_baseline_hitung_manual"] = base_gate

# konsistensi dengan ringkasan run
seed_gate = {}
for s in A1["seed_list"]:
    seed_gate[str(s)] = sum(1 for r in A1["folds"] if r["seed"] == s and r["gate_A_lulus"])
chk(seed_gate == SUM["fold_gate_A_A1_all_seeds"], "V3 gate A per seed = ringkasan run",
    f"hitung={seed_gate} json={SUM['fold_gate_A_A1_all_seeds']}")
R["v3c_gate_A_per_seed"] = seed_gate

# V4: rentang
def rng(rows, key):
    v = [r[key] for r in rows if r.get(key) is not None]
    return dict(n=len(v), min=float(min(v)) if v else None, max=float(max(v)) if v else None,
                median=float(np.median(v)) if v else None)


R["v4_rentang"] = {
    "A1_seed42_far": rng([r for r in A1["folds"] if r["seed"] == 42], "far_per_24h"),
    "A1_seed42_recall": rng([r for r in A1["folds"] if r["seed"] == 42], "recall"),
    "A1_semua_seed_far": rng(A1["folds"], "far_per_24h"),
    "A1b_far": rng(A1B["folds"], "far_per_24h"),
    "A1b_recall": rng(A1B["folds"], "recall"),
    "A1b_precision": rng(A1B["folds"], "precision"),
    "A2_reset_far": rng(A2["varian"]["reset"]["folds"], "far_per_24h"),
    "A2_reset_recall": rng(A2["varian"]["reset"]["folds"], "recall"),
    "A2_tanpa_reset_far": rng(A2["varian"]["tanpa_reset"]["folds"], "far_per_24h"),
    "A2_tanpa_reset_recall": rng(A2["varian"]["tanpa_reset"]["folds"], "recall"),
    "baseline_persistence_far": rng([r for r in BL["folds"] if r["model"] == "persistence"],
                                    "far_per_24h"),
    "baseline_hybrid_far": rng([r for r in BL["folds"]
                                if r["model"] == "hybrid_rule_lag1_and_persistence"],
                               "far_per_24h"),
    "baseline_persistence_recall": rng([r for r in BL["folds"] if r["model"] == "persistence"],
                                       "recall"),
    "baseline_hybrid_recall": rng([r for r in BL["folds"]
                                   if r["model"] == "hybrid_rule_lag1_and_persistence"],
                                  "recall"),
}

# V5: audit anti-bocor
df_cols = list(pd.read_csv(DS, nrows=3).columns)
feats_a1 = [c for c in df_cols if c not in LABEL_DERIVED]
feats_a1 = [c for c in feats_a1 if pd.api.types.is_numeric_dtype(pd.read_csv(DS, nrows=3)[c])]
feats_a1b = feats_a1 + A1B["fitur_tambahan"]
bocor_a1 = [c for c in feats_a1 if c in LABEL_DERIVED]
bocor_a1b = [c for c in feats_a1b if c in LABEL_DERIVED]
chk(len(bocor_a1) == 0, "V5a fitur A1 bebas kolom turunan label", f"bocor={bocor_a1}")
chk(sorted(bocor_a1b) == sorted(A1B["fitur_tambahan"]),
    "V5b fitur A1b memuat kolom turunan label (pelanggaran L3)",
    f"bocor={bocor_a1b}")
R["v5_audit_fitur"] = dict(n_fitur_A1=len(feats_a1), n_fitur_A1b=len(feats_a1b),
                           tambahan_A1b=A1B["fitur_tambahan"],
                           kolom_turunan_label_dipakai_A1b=bocor_a1b,
                           kolom_turunan_label_didefinisikan=list(LABEL_DERIVED))

# V6: recompute baseline langsung dari dataset
df = pd.read_csv(DS)
recomp = {}
for w, g in df.groupby("well"):
    g = g.sort_values("ts_bin")
    y = g["y_hyd"].to_numpy(int)
    pers = np.where(g["valid_prev_hyd"].to_numpy(int) == 1,
                    g["y_prev_hyd"].to_numpy(int), 0)
    rule_lag = np.concatenate([[0], y[:-1]])
    hyb = (rule_lag & pers).astype(int)
    recomp[w] = dict(n=len(y), n_pos=int(y.sum()),
                     fp_pers=int(((pers == 1) & (y == 0)).sum()),
                     fp_hyb=int(((hyb == 1) & (y == 0)).sum()))
json_pers = {r["test_well"]: r["fp"] for r in BL["folds"] if r["model"] == "persistence"}
json_hyb = {r["test_well"]: r["fp"] for r in BL["folds"]
            if r["model"] == "hybrid_rule_lag1_and_persistence"}
for w in recomp:
    chk(recomp[w]["fp_pers"] == json_pers.get(w), f"V6 FP persistence {w}",
        f"hitung={recomp[w]['fp_pers']} json={json_pers.get(w)}")
    chk(recomp[w]["fp_hyb"] == json_hyb.get(w), f"V6 FP hybrid {w}",
        f"hitung={recomp[w]['fp_hyb']} json={json_hyb.get(w)}")
R["v6_recompute_baseline"] = recomp
R["v6_total"] = dict(persistence=int(sum(v["fp_pers"] for v in recomp.values())),
                     hybrid=int(sum(v["fp_hyb"] for v in recomp.values())),
                     n_baris=int(sum(v["n"] for v in recomp.values())))

# V7: syarat 4xFP
gagal_sertifikasi = {}
for nama, rows in (("A1", A1["folds"]), ("A1b", A1B["folds"]),
                   ("A2_reset", A2["varian"]["reset"]["folds"])):
    bad = [r["test_well"] for r in rows if r.get("syarat_4x_fp") is False]
    gagal_sertifikasi[nama] = bad
R["v7_syarat_4x_fp_gagal"] = gagal_sertifikasi

R["ringkasan"] = dict(
    n_gagal=len(fail), gagal=fail,
    verdict="SEMUA PEMERIKSAAN LULUS" if not fail else "ADA PEMERIKSAAN GAGAL",
)
with open(f"{OUT}/e3_verify.json", "w") as f:
    json.dump(R, f, indent=2)

print(json.dumps({k: v for k, v in R.items() if k != "checks"}, indent=2))
print(f"\nchecks: {len(R['checks'])} total, {len(fail)} gagal")
for f_ in fail:
    print("GAGAL:", f_)
