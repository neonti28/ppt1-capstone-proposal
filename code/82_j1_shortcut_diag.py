"""J1 shortcut diagnostic (EKSPLORATIF — tidak mengubah gate).

Pertanyaan: apakah skor tinggi J1 berasal dari pembacaan ulang setpoint/parameter injeksi
(low_rpm -> surface_rpm, low_pump -> pump_spm, high_friction -> SPP, hard_formation -> ROP)
bukan dari "kerusakan"? Uji: model hanya pada fitur SETPOINT-derived (rpm, spm, flow) vs
hanya fitur NON-setpoint (mekanik/hidrolik: wob, hookload, torque, spp, difp, rop).
"""
import json
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import average_precision_score
from sklearn.model_selection import StratifiedGroupKFold

WS = "/mnt/d/Capstone 1"
CLASSES = ["bit_wear", "hard_formation", "high_friction", "low_pump", "low_rpm", "normal_soft"]
SENSORS = ["rop_m_per_hr", "wob_n", "hookload_n", "surface_rpm", "surface_torque_nm",
           "pump_spm", "flow_rate_m3_per_min", "spp_kpa", "difp_kpa", "block_position_m",
           "hole_depth_m", "bit_depth_m"]
STATS = ["mean", "std", "min", "max", "slope"]
SETPOINT_SENSORS = {"surface_rpm", "pump_spm", "flow_rate_m3_per_min"}
MECH_SENSORS = {"wob_n", "hookload_n", "surface_torque_nm", "spp_kpa", "difp_kpa"}

FEAT = [f"{c}__{s}" for s in STATS for c in SENSORS]
idx = {f: i for i, f in enumerate(FEAT)}
SETPOINT_IDX = [idx[f"{c}__{s}"] for s in STATS for c in SENSORS if c in SETPOINT_SENSORS]
MECH_IDX = [idx[f"{c}__{s}"] for s in STATS for c in SENSORS if c in MECH_SENSORS]
print(f"setpoint feats={len(SETPOINT_IDX)} mech feats={len(MECH_IDX)}")

wf = pd.read_csv(f"{WS}/docs/V5_J1_window_predictions.csv.gz")
print("windows:", len(wf), "runs:", wf.run_id.nunique())

# rebuild feature matrix from disk (independent from training script)
import os, csv
def slope_of(v):
    x = np.arange(len(v), dtype=float); x -= x.mean(); y = v - v.mean()
    d = (x*x).sum()
    return 0.0 if d == 0 else float((x*y).sum()/d)

rows = []
for cls in CLASSES:
    for run in sorted(os.listdir(f"{WS}/data/sim_v5/{cls}")):
        tel = f"{WS}/data/sim_v5/{cls}/{run}/surface_telemetry.csv"
        df = pd.read_csv(tel)
        d = df[df.activity == "drilling"]
        n = len(d)
        blocks = [d.iloc[s:s+100] for s in range(0, max(n-100+1,1), 50)] if n >= 100 else [d]
        for wi, b in enumerate(blocks):
            fr = {}
            for c in SENSORS:
                v = b[c].to_numpy(float)
                fr[f"{c}__mean"]=v.mean(); fr[f"{c}__std"]=v.std()
                fr[f"{c}__min"]=v.min(); fr[f"{c}__max"]=v.max(); fr[f"{c}__slope"]=slope_of(v)
            fr["run_id"]=run; fr["window_idx"]=wi; fr["y"]=CLASSES.index(cls)
            rows.append(fr)
Xdf = pd.DataFrame(rows)
print("rebuilt windows:", len(Xdf))
assert len(Xdf) == len(wf), (len(Xdf), len(wf))
Xdf.to_parquet("/home/neonti/.hermes/cache/scratch/j1_Xdf.parquet")

X = Xdf[FEAT].to_numpy(float)
y = Xdf["y"].to_numpy(int)
g = Xdf["run_id"].to_numpy()

def run_subset(name, cols):
    oof = np.zeros((len(Xdf), 6))
    for tr, te in StratifiedGroupKFold(5, shuffle=True, random_state=42).split(X, y, g):
        m = RandomForestClassifier(n_estimators=200, min_samples_leaf=2,
                                   random_state=42, n_jobs=-1)
        m.fit(X[tr][:, cols], y[tr])
        oof[te] = m.predict_proba(X[te][:, cols])
    # agregat run-level
    tmp = pd.DataFrame({f"p_{i}": oof[:, i] for i in range(6)})
    tmp["run_id"] = g; tmp["y"] = y
    agg = tmp.groupby("run_id").mean(numeric_only=True)
    yr = agg["y"].round().astype(int).to_numpy()
    pr = agg[[f"p_{i}" for i in range(6)]].to_numpy()
    ap = average_precision_score(yr, pr, average="macro")
    print(f"  {name:28s} macro-AUPRC(run) = {ap:.4f}")
    return ap

print("=== Shortcut diagnostic (eksploratif, gate TIDAK berubah) ===")
ap_all = run_subset("ALL 60 feats", list(range(60)))
ap_sp = run_subset("SETPOINT only (rpm/spm/flow)", SETPOINT_IDX)
ap_me = run_subset("MECH only (wob/hl/tq/spp/difp)", MECH_IDX)

json.dump({"ap_all": ap_all, "ap_setpoint_only": ap_sp, "ap_mech_only": ap_me,
           "note": "eksploratif; gate J1 tidak berubah"},
          open(f"{WS}/docs/V5_J1_shortcut_diag.json", "w"), indent=2)
print("saved ->", f"{WS}/docs/V5_J1_shortcut_diag.json")
