"""RND-E2: kutip angka bengkel (tool_wear) langsung dari JSON primer."""
from __future__ import annotations

import json
from pathlib import Path

BASE = Path("/mnt/d/Capstone 1(v2)")
OUT = BASE / "scratch/rnd_e2"
p = BASE / "scratch/v9_e_stat/v9_e_stat_03_tool_wear_RESULTS.json"
d = json.loads(p.read_text())
keep = {}
for k in ("claim_task", "seed", "n_perm", "summary"):
    keep[k] = d.get(k)
for k in ("part_A_change_point", "part_B_within_tool_calibration",
          "part_C_operating_far_calibrated", "part_D_ranking_auprc"):
    v = d.get(k)
    keep[k] = v if not isinstance(v, dict) else {kk: v[kk] for kk in list(v)[:12]}
(OUT / "e2_toolwear_stats.json").write_text(json.dumps(keep, indent=2, ensure_ascii=False))
print(json.dumps(keep, indent=2, ensure_ascii=False)[:5000])
