#!/usr/bin/env python3
"""Verifikasi independen: baca JSON mentah, cetak angka yang dipakai dokumen PM.

Tidak menulis apa pun. Dipakai untuk membuktikan angka dokumen bukan hasil salin
dari dokumen lain, melainkan ada di berkas mentah.
"""
import json
from pathlib import Path

WS = Path("/mnt/d/Capstone 1(v2)")
S = WS / "scratch/rnd"

hyd = json.loads((S / "r8/r8_hyd.json").read_text())
shk = json.loads((S / "r8/r8_shk.json").read_text())
stuck = json.loads((S / "r8/r8_stuck.json").read_text())
tw = json.loads((S / "r8/r8_toolwear.json").read_text())
agg = json.loads((S / "r8/r8_agg.json").read_text())
e4 = json.loads((S / "e4/e4_summary.json").read_text())
e3 = json.loads((S / "e3/e3_verify.json").read_text())


def ambil(d, jalur, default="TIDAK ADA"):
    cur = d
    for k in jalur.split("."):
        if isinstance(cur, dict) and k in cur:
            cur = cur[k]
        elif isinstance(cur, list) and k.isdigit() and int(k) < len(cur):
            cur = cur[int(k)]
        else:
            return default
    return cur


print("=== r8_hyd ringkas ===")
r = ambil(hyd, "ringkas", {})
print("kunci:", list(r)[:12])
print("rule:", json.dumps(r.get("rule_kanal", {}), ensure_ascii=False)[:400])
print("H1:", json.dumps(r.get("H1_stat_dan_rule", {}), ensure_ascii=False)[:400])
print("agg hyd:", json.dumps(agg.get("turunan", {}).get("hyd", agg.get("hyd", {})),
                             ensure_ascii=False)[:400])
print("\n=== shk ===")
print(json.dumps({k: v for k, v in (shk.get("ringkas") or {}).items()}, ensure_ascii=False)[:600])
print("\n=== stuck ===")
print(json.dumps({k: v for k, v in (stuck.get("ringkas") or {}).items()}, ensure_ascii=False)[:600])
print("\n=== toolwear ===")
print(json.dumps({k: v for k, v in (tw.get("ringkas") or {}).items()}, ensure_ascii=False)[:600])
print("\n=== e4 cakupan/fitur ===")
for k in ("cakupan", "n_fitur", "gate"):
    if k in e4:
        print(k, json.dumps(e4[k], ensure_ascii=False)[:400])
print("kunci e4:", list(e4)[:15])
print("\n=== e3 gate ===")
for k in ("gate_A_fold", "models", "coverage"):
    if k in e3:
        print(k, json.dumps(e3[k], ensure_ascii=False)[:300])
print("kunci e3:", list(e3)[:15])
