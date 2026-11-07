#!/usr/bin/env python3
"""Probe ketiga: cek PM-065 (fold tanpa alarm) pada dua berkas E4."""
import json
from pathlib import Path

W = Path("/mnt/d/Capstone 1(v2)")
d = json.loads((W / "scratch/rnd/e4/e4_gate_decomp.json").read_text())
print("kunci gate_decomp:", list(d))
a = d.get("A1_alpha_anggaran", {})
print("A1_alpha_anggaran:", json.dumps(a, ensure_ascii=False)[:600])
s = json.loads((W / "scratch/rnd/e4/e4_summary.json").read_text())
aa = s["ringkas"]["alpha_anggaran"]
print("summary alpha_anggaran:", json.dumps(aa, ensure_ascii=False)[:600])
print("fold_tanpa_alarm =", a.get("fold_tanpa_alarm"), "fold_recall_nol =", aa.get("fold_recall_nol"))
