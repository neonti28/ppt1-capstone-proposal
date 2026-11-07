"""RND-E2: profil dataset bengkel (tool wear) dari file nyata.

Output: scratch/rnd_e2/e2_toolwear.json
"""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

BASE = Path("/mnt/d/Capstone 1(v2)")
OUT = BASE / "scratch/rnd_e2"
R: dict = {}

p = BASE / "scratch/v6_e1/toolwear_windows.csv"
R["path"] = str(p)
R["exists"] = p.exists()
with p.open(newline="") as fh:
    rd = csv.DictReader(fh)
    header = rd.fieldnames or []
    rows = list(rd)
R["n_cols"] = len(header)
R["n_rows"] = len(rows)
R["cols"] = header
unit_col = next((c for c in header if c.lower() in ("alat", "tool", "unit", "well", "tool_id")), None)
R["unit_col"] = unit_col
if unit_col:
    c = Counter(r[unit_col] for r in rows)
    R["per_unit"] = dict(c)
    R["n_units"] = len(c)
lab_cols = [c for c in header if c.lower().startswith(("y_", "label", "target"))]
R["label_cols"] = lab_cols
for lc in lab_cols:
    ones = sum(1 for r in rows if r[lc] not in ("", "0", "0.0", "False", "nan"))
    R.setdefault("label_counts", {})[lc] = ones

# JSON statistik tool wear yang sudah ada (untuk angka TLead/FP per alat)
for name in ("v9_e_stat_03_tool_wear_RESULTS.json", "v9_e_RULE_03_bitwear_toolwear_results.json"):
    q = BASE / "scratch/v9_e_stat" / name
    if not q.exists():
        q = BASE / "scratch/v9_e_rule" / name
    if q.exists():
        d = json.loads(q.read_text())
        R.setdefault("json_sources", {})[name] = {
            "keys": sorted(d.keys())[:25],
            "size": q.stat().st_size,
        }

(OUT / "e2_toolwear.json").write_text(json.dumps(R, indent=2, ensure_ascii=False))
print(json.dumps({k: R[k] for k in ("exists", "n_rows", "n_cols", "unit_col", "n_units",
                                    "per_unit", "label_cols", "label_counts")},
                 indent=2, ensure_ascii=False))
print("\njson sources:", json.dumps(R.get("json_sources", {}), indent=2)[:1200])
