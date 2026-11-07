#!/usr/bin/env python3
"""Probe kedua: cakupan E4 dan gate A E3."""
import json
from pathlib import Path

W = Path("/mnt/d/Capstone 1(v2)")
e4 = json.loads((W / "scratch/rnd/e4/e4_summary.json").read_text())
print("e4 kunci:", list(e4))
print("e4 ringkas kunci:", list(e4.get("ringkas", {})))
print(json.dumps(e4.get("ringkas", {}), ensure_ascii=False)[:1400])
e3 = json.loads((W / "scratch/rnd/e3/e3_verify.json").read_text())
print("\ne3 v3_gate_A:", json.dumps(e3.get("v3_gate_A"), ensure_ascii=False)[:400])
print("e3 ringkasan:", json.dumps(e3.get("ringkasan"), ensure_ascii=False)[:700])
