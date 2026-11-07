"""V9-E_RULE 02c — verifikasi hasil repair stuck_k2 + audit meta dataset lain."""
import json
import numpy as np
import pandas as pd

BASE = "/mnt/d/Capstone 1"
orig = pd.read_csv(f"{BASE}/scratch/v9_d1/datasets/stuck_k2.csv.gz")
fix = pd.read_csv(f"{BASE}/scratch/v9_e_rule/repair/stuck_k2.csv.gz")

print("== IDENTITAS STRUKTUR ==")
print("rows orig/fix:", len(orig), len(fix), "same:", len(orig) == len(fix))
print("cols same:", list(orig.columns) == list(fix.columns))
# urutan baris BEDA antar file (original: sort ts_bin NaN -> urutan concat;
# repaired: sort ts_bin valid -> kronologis). Bandingkan PER WELL dlm urutan file.
per_well_identical = {}
for w in sorted(set(orig["well"])):
    a = orig[orig["well"] == w].reset_index(drop=True)
    b = fix[fix["well"] == w].reset_index(drop=True)
    ok_n = len(a) == len(b)
    ok_y = ok_n and np.array_equal(a["y_stuck_onset"].to_numpy(),
                                   b["y_stuck_onset"].to_numpy())
    ok_yp = ok_n and np.array_equal(a["y_prev_stuck_onset"].to_numpy(),
                                    b["y_prev_stuck_onset"].to_numpy())
    ok_f = ok_n and np.allclose(a["TQA_mean"].fillna(-9e9).to_numpy(),
                                b["TQA_mean"].fillna(-9e9).to_numpy(),
                                equal_nan=True)
    ok_fk = ok_n and np.allclose(a["feat_ts_max"].fillna(-9e9).to_numpy(),
                                 b["feat_ts_max"].fillna(-9e9).to_numpy())
    per_well_identical[w] = dict(n=ok_n, y=ok_y, y_prev=ok_yp,
                                 TQA_mean=ok_f, feat_ts_max=ok_fk)
    print(" ", w, per_well_identical[w])
all_same = all(all(v.values()) for v in per_well_identical.values())
same_y = all(v["y"] for v in per_well_identical.values())
print("SEMUA IDENTIK per well:", all_same, "| y identik:", same_y)

print("\n== META DIPERBAIKI ==")
for c in ["ts_bin", "lab_ts", "feat_ts_max"]:
    print(f"{c}: orig_nan={orig[c].isna().sum()} fix_nan={fix[c].isna().sum()}")
print("lab_kind counts fix:")
print(fix["lab_kind"].value_counts())

print("\n== ANTI-BOCOR NYATA (bukan vakuum) ==")
both = fix["feat_ts_max"].notna() & fix["lab_ts"].notna()
n_both = int(both.sum())
viol = int((fix.loc[both, "feat_ts_max"] >= fix.loc[both, "lab_ts"]).sum())
strict_lt = int((fix.loc[both, "feat_ts_max"] < fix.loc[both, "lab_ts"]).sum())
print(f"rows with both non-null: {n_both}/{len(fix)}")
print(f"feat_ts_max >= lab_ts: {viol} | feat_ts_max < lab_ts: {strict_lt}")

print("\n== INVARIAN ONSET ==")
ev = fix.loc[fix["lab_kind"] == "onset_event"].groupby("well")["lab_ts"].nunique()
print(ev.to_dict(), "(REF: F-9_A=72 F-10=93 F-14=61; F-9=55 tanpa REF)")
neg_lab_ts_eq_ts = (fix.loc[fix["lab_kind"] == "onset_horizon_neg", "lab_ts"]
                    == fix.loc[fix["lab_kind"] == "onset_horizon_neg", "ts_bin"]).all()
print("negatif: lab_ts == ts_bin seluruhnya:", bool(neg_lab_ts_eq_ts))
lead = (fix.loc[fix["lab_kind"] == "onset_event", "lab_ts"]
        - fix.loc[fix["lab_kind"] == "onset_event", "ts_bin"])
print("lead menit (positif): min/max:", int(lead.min()), int(lead.max()),
      "| semua < H=10:", bool((lead < 10).all()), "| >=0:", bool((lead >= 0).all()))
# baris per onset harus <=10 (horizon H=10)
per_ev = fix.loc[fix["lab_kind"] == "onset_event"].groupby(["well", "lab_ts"]).size()
print("baris horizon per onset: max =", int(per_ev.max()), "(<=10:", bool(per_ev.max() <= 10), ")")

print("\n== AUDIT META 5 DATASET LAIN (risiko vakuum checker) ==")
report = {}
for eng in ["vib", "ssi", "shk", "stuck_k1", "hyd_ki"]:
    d = pd.read_csv(f"{BASE}/scratch/v9_d1/datasets/{eng}.csv.gz",
                    usecols=["ts_bin", "feat_ts_max", "lab_ts"])
    n = len(d)
    nan_ts, nan_lab = int(d["ts_bin"].isna().sum()), int(d["lab_ts"].isna().sum())
    both = d["feat_ts_max"].notna() & d["lab_ts"].notna()
    viol = int((d.loc[both, "feat_ts_max"] >= d.loc[both, "lab_ts"]).sum())
    report[eng] = dict(n=n, nan_ts_bin=nan_ts, nan_lab_ts=nan_lab,
                       both_nonnull=int(both.sum()), leak_violations=viol)
    print(eng, report[eng])

report["stuck_k2_repair"] = dict(n=len(fix), nan_ts_bin=0, nan_lab_ts=0,
                                 leak_violations=int(
                                     (fix["feat_ts_max"] >= fix["lab_ts"]).sum()))
json.dump({"stuck_k2_repair": {"rows": len(fix), "y_identical": bool(same_y),
                               "leak_violations": viol, "both_nonnull": n_both},
           "other_datasets": report},
          open(f"{BASE}/scratch/v9_e_rule/v9_e_RULE_02c_verify.json", "w"), indent=1)
print("\n-> verify json written")
