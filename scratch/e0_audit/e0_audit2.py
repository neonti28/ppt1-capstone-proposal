#!/usr/bin/env python3
"""E0 audit bagian 2: provenance alarm, tool_wear kebetulan, registry, arsip."""
import importlib.util
import json
import os

import numpy as np
import pandas as pd

BASE = "/mnt/d/Capstone 1(v2)"
DS = f"{BASE}/scratch/v9_d1/datasets"
OUTDIR = "/home/neonti/.hermes/kanban/boards/rnd-algo-2026/workspaces/t_57e7d52b"
res = {}


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# ----------------------------------------------------- A. stuck_k2 provenance
print("== A. provenance alarm persistence_event (stuck_k2)")
d = pd.read_csv(f"{DS}/stuck_k2.csv.gz",
                usecols=["well", "ts_bin", "lab_ts", "lab_kind", "y_stuck_onset"])
pev = np.zeros(len(d), np.int8)
for w, g in d.groupby("well"):
    ev = set(g.loc[g["lab_kind"] == "onset_event", "lab_ts"].astype("int64").unique())
    ts = g["ts_bin"].to_numpy().astype("int64")
    pev[g.index.to_numpy()] = np.isin(ts - 1, list(ev)).astype(np.int8)
d["pev"] = pev
al = d[d["pev"] == 1]
A = {"n_rows": int(len(d)), "n_alarm_rows": int(len(al)),
     "n_events": int(d.loc[d["lab_kind"] == "onset_event", "lab_ts"].nunique()),
     "n_rows_lab_kind_onset": int((d["lab_kind"] == "onset_event").sum()),
     "alarm_lab_kind_counts": {str(k): int(v) for k, v in
                               al["lab_kind"].fillna("").value_counts().items()},
     "alarm_lead_dist": (None if al.empty else
                         {str(int(k)): int(v) for k, v in
                          (al["lab_ts"] - al["ts_bin"]).value_counts().sort_index().items()}),
     "alarm_pos_rate": round(float(al["y_stuck_onset"].mean()), 4) if len(al) else None,
     "rows_onset_with_ts_ge_lab_ts": int(((d["lab_kind"] == "onset_event") &
                                          (d["ts_bin"] >= d["lab_ts"])).sum())}
# apakah alarm menutup event yang sama sekali berbeda dari penyebabnya?
ev_by_well = {w: set(g.loc[g["lab_kind"] == "onset_event", "lab_ts"].astype("int64").unique())
              for w, g in d.groupby("well")}
same_event = 0
other_event = 0
for _, r in al.iterrows():
    trig = int(r["ts_bin"]) - 1          # event yang memicu alarm
    target = int(r["lab_ts"])            # event yang dihitung terbantu
    if trig == target:
        same_event += 1
    elif target in ev_by_well[r["well"]]:
        other_event += 1
A["alarm_trigger_sama_dgn_event_dihitung"] = same_event
A["alarm_trigger_event_berbeda"] = other_event
res["stuck_k2_alarm_provenance"] = A
print(json.dumps(A, indent=1)[:1200])

# ------------------------------------------------ B. tool_wear: nilai kebetulan
print("== B. tool_wear: peluang alarm acak pada jendela R02")
tw = pd.read_csv(f"{BASE}/scratch/v6_e1/toolwear_windows.csv")
rows = []
for (tool, run), g in tw.groupby(["tool", "run"]):
    rows.append({"alat": tool, "run": run, "n": int(len(g)),
                 "y": int(g["y"].iloc[0])})
B = {"per_run": rows}
try:
    R = json.load(open(f"{BASE}/scratch/v9_i1/v9_i1_RESULTS.json"))
    twblk = R["engines"]["tool_wear"]["heads"]
    hmap = {h["head"]: h for h in twblk}
    op = hmap.get("op_far_calibrated", {})
    B["op_far_calibrated_metrik"] = op.get("metrik_segmen")
    per = op.get("per_alat", [])
    lam = []
    for t in per:
        n_eval = t.get("n_eval_R01")
        n_r02 = t.get("n_R02")
        fp = t.get("fp_R01")
        if n_eval and n_r02 is not None and fp is not None:
            rate = fp / n_eval                     # alarm per jendela (1 dtk)
            lam.append({"alat": t["alat"], "fp_R01": fp, "n_eval_R01": n_eval,
                        "laju_alarm_per_jendela": round(rate, 5),
                        "n_R02": n_r02,
                        "harapan_alarm_acak_R02": round(rate * n_r02, 3),
                        "P_minimal_1_alarm_acak": round(1 - np.exp(-rate * n_r02), 4),
                        "det_benar": t.get("det_R02"),
                        "TLead_s": t.get("TLead_s")})
    B["harapan_kebetulan"] = lam
    B["n_eval_R01_contoh"] = per[0] if per else None
except Exception as e:
    B["error"] = repr(e)
res["tool_wear_kebetulan"] = B
print(json.dumps(B.get("harapan_kebetulan", B), indent=1)[:1600])

# --------------------------------------------------------- C. bit_wear label
print("== C. bit_wear: sirkularitas persistence")
u = pd.read_csv(f"{BASE}/data/USROP_labeled.csv", usecols=["label"])
is_mse = (u["label"] == "high_MSE_bit_wear").to_numpy().astype(int)
nxt = np.concatenate([is_mse[1:], [0]])
res["bit_wear"] = {
    "n_rows": int(len(is_mse)), "n_pos": int(is_mse.sum()),
    "prev": round(float(is_mse.mean()), 4),
    "P_y(t+1)=1_given_y(t)=1": round(float(nxt[is_mse == 1].mean()), 4),
    "P_y(t+1)=1_given_y(t)=0": round(float(nxt[is_mse == 0].mean()), 4),
    "komposisi_label": {str(k): int(v) for k, v in u["label"].value_counts().items()},
}
print(json.dumps(res["bit_wear"], indent=1))

# ------------------------------------------------------------ D. REGISTRY
print("== D. REGISTRY: jumlah head, tier, lapisan")
p = load(f"{BASE}/code/v9_i1_pipeline.py", "v9_i1")
heads = []
for eng, blk in p.REGISTRY.items():
    for hname, h in blk["heads"].items():
        heads.append({"engine": eng, "head": hname, "tier": h["tier"],
                      "layer": h["layer"], "klaim": h.get("klaim")})
tiers = {}
layers = {}
for h in heads:
    tiers[h["tier"]] = tiers.get(h["tier"], 0) + 1
    layers[h["layer"]] = layers.get(h["layer"], 0) + 1
res["registry"] = {"n_head": len(heads), "per_engine": {e: sum(1 for h in heads if h["engine"] == e)
                                                        for e in p.REGISTRY},
                   "tier_counts": tiers, "layer_counts": layers,
                   "heads": heads,
                   "heads_superv_layer_l0": [h for h in heads
                                             if h["tier"] == "PERINGATAN-BERPENGAWAS"
                                             and h["layer"] == "L0"]}
print(json.dumps({k: v for k, v in res["registry"].items() if k != "heads"}, indent=1))

# --------------------------------------------------- E. path arsip di kode v2
print("== E. rujukan folder arsip")
import subprocess
r = subprocess.run(["grep", "-rn", "/mnt/d/Capstone 1/", f"{BASE}/code/",
                    "--include=*.py"], capture_output=True, text=True)
hits = [ln for ln in r.stdout.splitlines() if "/mnt/d/Capstone 1(v2)" not in ln]
res["arsip_refs"] = {"n": len(hits), "contoh": hits[:25]}
print("jumlah rujukan arsip:", len(hits))
for h in hits[:15]:
    print("   ", h.replace(BASE, "."))

with open(f"{OUTDIR}/e0_audit_results2.json", "w") as f:
    json.dump(res, f, indent=1, default=str)
print("SELESAI -> e0_audit_results2.json")
