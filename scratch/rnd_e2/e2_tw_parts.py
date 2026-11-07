"""RND-E2: baca part_B dan part_C tool_wear apa adanya (untuk merekonsiliasi TLead)."""
from __future__ import annotations

import json
from pathlib import Path

BASE = Path("/mnt/d/Capstone 1(v2)")
d = json.loads((BASE / "scratch/v9_e_stat/v9_e_stat_03_tool_wear_RESULTS.json").read_text())
for k in ("part_B_within_tool_calibration", "part_C_operating_far_calibrated"):
    print("=" * 30, k)
    print(json.dumps(d[k], indent=2, ensure_ascii=False)[:4200])
