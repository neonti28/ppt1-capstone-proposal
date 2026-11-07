import json
import numpy as np
import pandas as pd

DS = "/mnt/d/Capstone 1(v2)/scratch/v9_d1/datasets"
OUT = "/home/neonti/.hermes/kanban/boards/rnd-algo-2026/workspaces/t_57e7d52b/e0v_onset.json"

res = {}
for cls, ycol in (("vib", "y_vib"), ("shk", "y_shk"), ("stuck_k1", "y_stuck"),
                  ("ssi", "y_ssi"), ("hyd_ki", "y_hyd")):
    d = pd.read_csv(f"{DS}/{cls}.csv.gz")
    prev = [c for c in d.columns if c.startswith("y_prev")]
    y = d[ycol].to_numpy().astype(int)
    p = d[prev[0]].to_numpy() if prev else None
    pos = y == 1
    res[cls] = {
        "kolom_prev": prev[0] if prev else None,
        "n": int(len(d)),
        "n_pos": int(pos.sum()),
        "n_pos_prev1": int((pos & (p == 1)).sum()) if p is not None else None,
        "n_pos_prev0": int((pos & (p == 0)).sum()) if p is not None else None,
        "fraksi_pos_onset_baru": round(float((pos & (p == 0)).sum() / pos.sum()), 4) if p is not None else None,
        "n_prev_nan": int(np.isnan(p.astype(float)).sum()) if p is not None else None,
    }
json.dump(res, open(OUT, "w"), indent=1)
print(json.dumps(res, indent=1))
