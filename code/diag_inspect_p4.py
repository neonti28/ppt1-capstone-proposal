#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inspect struktur JSON p4 utk menulis helper MD==JSON."""
import json

R = "/mnt/d/Capstone 1/docs/V2_ML_BEAT_CANARY_TS.json"
r = json.load(open(R))
p4 = r["p4_desain_baru"]
k0 = list(p4["folds"].keys())[0]
f0 = list(p4["folds"][k0].keys())[0]
print("folds[key][fold] =", json.dumps(p4["folds"][k0][f0], indent=1)[:700])
print("pooled[log_G]    =", json.dumps(p4["pooled"]["log_G"], indent=1)[:700])
print("macro            =", json.dumps(p4["macro"])[:300])
print("split_info keys  =", list(p4["split_info"].keys())[:8])
si = p4["split_info"]
first = list(si.values())[0] if isinstance(si, dict) else si
print("split_info[0]    =", json.dumps(first)[:500])
print("units            =", json.dumps(p4["units"]))
print("gate keys        =", list(p4["gate"].keys()))
print("diagnostics keys =", list(p4["diagnostics"].keys()))
