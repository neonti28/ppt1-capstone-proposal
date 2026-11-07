#!/usr/bin/env python3
"""
Fault Injection untuk Drilling Telemetry Simulator.

Membuat beberapa skenario dengan 'fault' yang dimodelkan lewat perubahan
parameter fisik scenario:
  - FK1 (Hard Formation / Bit Wear): UCS dinaikkan 10x → ROP turun, torque/WOB naik
  - FK2 (BHA Drag / Friction): friction naik → hookload/torque naik
  - FK3 (Motor/PDM wear): drivetrain PDM efficiency turun → DIFP naik
  - FK0 (Normal): kondisi baseline

Output: surface_telemetry.csv + label kondisi per baris.
"""
import json
import os
import shutil
import sys
from pathlib import Path

RIG_SIM = "/tmp/capstone-venv/.venv/bin"

BASE_EXAMPLE = None
for p in [
    Path("/tmp/capstone-venv/.venv/lib/python3.12/site-packages/rig_telemetry_sim/data/examples"),
    Path("/tmp/capstone-venv/.venv/lib/python3.12/site-packages/rig_telemetry_sim/data/examples"),
]:
    if (p / "precision_st1200_rig_first_example.json").exists():
        BASE_EXAMPLE = p / "precision_st1200_rig_first_example.json"
        break

if BASE_EXAMPLE is None:
    sys.exit("Contoh scenario tidak ditemukan")

OUT_ROOT = Path("/mnt/d/Capstone 1/data/sim-fault")
OUT_ROOT.mkdir(parents=True, exist_ok=True)

scenarios = {
    "FK0_normal": {"label": "normal", "changes": {}},
    "FK1_hard_formation": {
        "label": "hard_formation_bit_wear",
        "changes": {"formation_intervals_ucs_pa": 30_000_000},  # 10x UCS (keras)
    },
    "FK2_high_friction": {
        "label": "high_friction_bha_drag",
        "changes": {"string_friction_factor": 0.15},  # friction string naik
    },
    "FK3_bit_cutting_efficiency_low": {
        "label": "bit_wear_low_cutting",
        "changes": {"bit_cutting_efficiency": 0.2},  # bit aus, efisiensi potong turun
    },
}

for name, spec in scenarios.items():
    scenario = json.load(open(BASE_EXAMPLE))
    label = spec["label"]
    changes = spec["changes"]

    # apply changes
    if "formation_intervals_ucs_pa" in changes:
        for iv in scenario["formation"]["intervals"]:
            iv["ucs_pa"] = changes["formation_intervals_ucs_pa"]
    if "string_friction_factor" in changes:
        if "hydraulics" not in scenario:
            scenario["hydraulics"] = {}
        scenario["hydraulics"]["string_friction_factor"] = changes["string_friction_factor"]
    if "bit_cutting_efficiency" in changes:
        if "bit" not in scenario:
            scenario["bit"] = {}
        scenario["bit"]["cutting_efficiency"] = changes["bit_cutting_efficiency"]

    scenario["name"] = f"fault-{label}"

    # tulis scenario sementara
    scen_path = OUT_ROOT / f"{name}.json"
    json.dump(scenario, open(scen_path, "w"), indent=2)

    out_dir = OUT_ROOT / name
    if out_dir.exists():
        shutil.rmtree(out_dir)

    os.system(
        f'{RIG_SIM}/rig-telemetry-sim generate "{scen_path}" --output "{out_dir}" > /tmp/fault_{name}.log 2>&1'
    )

    csv_path = out_dir / "surface_telemetry.csv"
    if csv_path.exists():
        import pandas as pd
        df = pd.read_csv(csv_path)
        print(f"{name}: OK — {len(df)} baris, kolom={df.shape[1]}")
    else:
        print(f"{name}: GAGAL — log:")
        print(open(f"/tmp/fault_{name}.log").read()[-500:])

print("\nSelesai. Output di:", OUT_ROOT)