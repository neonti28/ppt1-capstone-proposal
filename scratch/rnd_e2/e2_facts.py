"""RND-E2: fakta pendukung protokol (runtime, jumlah head, dataset bengkel).

Output: scratch/rnd_e2/e2_facts.json
"""
from __future__ import annotations

import json
from pathlib import Path

BASE = Path("/mnt/d/Capstone 1(v2)")
OUT = BASE / "scratch/rnd_e2"
R: dict = {}

# 1. runtime + jumlah head dari JSON V9-I1
d = json.loads((BASE / "scratch/v9_i1/v9_i1_RESULTS.json").read_text())
R["meta"] = d.get("meta", {})
heads = []
for eng in d.get("engines", []):
    for h in eng.get("heads", []):
        heads.append({"engine": eng.get("engine"), "head": h.get("head"),
                      "tier": h.get("tier"), "layer": h.get("layer")})
R["n_engines"] = len(d.get("engines", []))
R["n_heads"] = len(heads)
R["daftar_engine"] = [e.get("engine") for e in d.get("engines", [])]
R["heads_per_engine"] = {e.get("engine"): len(e.get("heads", [])) for e in d.get("engines", [])}
R["tier_count"] = {}
for h in heads:
    R["tier_count"][h["tier"]] = R["tier_count"].get(h["tier"], 0) + 1
R["layer_count"] = {}
for h in heads:
    R["layer_count"][h["layer"]] = R["layer_count"].get(h["layer"], 0) + 1
R["auto_critical_alarm_slots"] = d.get("auto_critical_alarm_slots")
R["keputusan_akhir"] = d.get("keputusan_akhir")

# 2. dataset bengkel tool_wear
tw = BASE / "scratch/v9_d1/datasets"
cands = sorted(tw.glob("*tool*")) if tw.exists() else []
R["tool_wear_files"] = [p.name for p in cands]
for p in cands:
    if p.suffix == ".gz":
        import gzip
        with gzip.open(p, "rt") as fh:
            header = fh.readline().rstrip("\n").split(",")
            n = 0
            tools = {}
            iw = header.index("well") if "well" in header else (header.index("alat") if "alat" in header else None)
            for line in fh:
                n += 1
                if iw is not None:
                    w = line.split(",")[iw]
                    tools[w] = tools.get(w, 0) + 1
        R.setdefault("tool_wear_detail", {})[p.name] = {
            "rows": n, "n_cols": len(header), "unit_counts": tools,
            "cols_sample": header[:12],
        }

(OUT / "e2_facts.json").write_text(json.dumps(R, indent=2, ensure_ascii=False))
print(json.dumps(R, indent=2, ensure_ascii=False)[:2500])
