"""R6: apakah delta_B dan baselines per fold tersimpan? (untuk bootstrap berpasangan)."""
import json
from pathlib import Path

BASE = Path("/mnt/d/Capstone 1(v2)/scratch")
for f in ["v9_e_ml/v9_e_ML_shk_RESULTS.json", "v9_e_ml/v9_e_ML_vib_RESULTS.json",
          "v9_e_ml/v9_e_ML_ssi_RESULTS.json", "v9_e_ml/v9_e_ML_stuck_k2_RESULTS.json"]:
    d = json.loads((BASE / f).read_text(encoding="utf-8"))
    folds = d["folds"]
    print(f"\n=== {f} folds={len(folds)} ci95_method={d.get('ci95_method')}")
    print("  test_wells:", [x["test_well"] for x in folds])
    print("  underpowered:", [x["underpowered"] for x in folds])
    print("  delta_B keys:", json.dumps(folds[0].get("delta_B"), ensure_ascii=False)[:400])
    print("  baselines keys:", list((folds[0].get("baselines") or {}).keys()))
    b = folds[0].get("baselines") or {}
    for k, v in list(b.items())[:3]:
        print("   ", k, "->", json.dumps(v, ensure_ascii=False)[:220])
    print("  agregat:", json.dumps(d.get("agregat"), ensure_ascii=False)[:600])
