"""R6: struktur per-fold metrik ML (AUPRC/CI) yang tersedia untuk uji berpasangan antar-well."""
import json
from pathlib import Path

BASE = Path("/mnt/d/Capstone 1(v2)/scratch")
for f in ["v9_e_ml/v9_e_ML_vib_RESULTS.json", "v9_e_ml/v9_e_ML_shk_RESULTS.json"]:
    d = json.loads((BASE / f).read_text(encoding="utf-8"))
    print(f"\n===== {f}")
    print("keys:", list(d.keys()))
    folds = d.get("folds", [])
    print("n_folds:", len(folds))
    if folds:
        print("fold[0] keys:", list(folds[0].keys()))
        print(json.dumps(folds[0], ensure_ascii=False)[:2500])
