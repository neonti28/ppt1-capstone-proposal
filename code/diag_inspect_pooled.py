#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inspect pooled[key] keys utk helper MD==JSON."""
import json

r = json.load(open("/mnt/d/Capstone 1/docs/V2_ML_BEAT_CANARY_TS.json"))
p4 = r["p4_desain_baru"]
g = p4["pooled"]["log_G"]
print("pooled[log_G] keys:", list(g.keys()))
for k in ("lift", "r_at_p20", "r_at_p50", "recall_at_p20", "recall_at_p50",
          "f1_thr", "f1", "ece"):
    print(f"  {k} = {g.get(k)}")
print("gate:", json.dumps({k: v for k, v in p4["gate"].items()
                           if k != "per_variant"})[:400])
print("diagnostics:", json.dumps(p4["diagnostics"])[:600])
