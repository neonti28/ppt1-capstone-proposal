#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
code/33_audit_claims.py — AUDIT t_abc6eef6 [ML Auditor] CHECK 5 (lanutan): verifikasi klaim
numerik spesifik docs/V2_ML_RESULTS.md yang belum dicek di 30_audit_inventory.py.
Semua dihitung ulang dari file mentah.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path
import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
DS = BASE / "data" / "predictive" / "dataset_prediktif.csv"
REPORT = (BASE / "docs" / "V2_ML_RESULTS.md").read_text(encoding="utf-8")

print("=" * 78, "\nCLAIM 1: '79 event menjadi next_event_id pada >=1 baris positif (76 distinct next_event_md)'\n" + "=" * 78)
ds = pd.read_csv(DS, low_memory=False)
pos = ds[ds["y_10"] == 1]
n_nid = pos["next_event_id"].nunique()
n_nmd = pos["next_event_md"].nunique()
print(f"  distinct next_event_id  pada baris y_10=1 : {n_nid}  (laporan: 79)")
print(f"  distinct next_event_md  pada baris y_10=1 : {n_nmd}  (laporan: 76)")
c1 = (n_nid == 79) and (n_nmd == 76)
print(f"  -> {'PASS' if c1 else 'GAGAL'}")

print("\n" + "=" * 78, "\nCLAIM 2: '27,7% baris positif Delta=10 punya |act-est| > 30 hari'\n" + "=" * 78)
lab = pd.read_csv(BASE / "data" / "volve" / "labels_curated.csv",
                  usecols=["event_id", "act_start"])
pos2 = pos.merge(lab, left_on="next_event_id", right_on="event_id", how="left")
est = pd.to_datetime(pos2["est_timestamp"], utc=True, errors="coerce")
act = pd.to_datetime(pos2["act_start"], utc=True, errors="coerce")
diff = (act - est).dt.total_seconds().abs() / 86400.0
frac = float((diff > 30).mean())
print(f"  n baris positif = {len(pos2)}; act_start ter-parse = {int(act.notna().sum())}")
print(f"  fraksi |act-est| > 30 hari = {frac*100:.2f}%  (laporan: 27,7%)")
c2 = abs(frac * 100 - 27.7) < 0.5
print(f"  -> {'PASS' if c2 else 'GAGAL'}")

print("\n" + "=" * 78, "\nCLAIM 3: '170 event jatuh dalam rentang md USROP (potensi menandai)'\n" + "=" * 78)
dm = json.loads((BASE / "docs" / "V2_PREDICTIVE_DATASET_METRICS.json").read_text(encoding="utf-8"))
pw = dm["events"]["per_wellbore"]
s_in = sum(v["n_md_dalam_rentang_usrop"] for v in pw.values())
s_pot = sum(v["n_event_potensi_menandai"] for v in pw.values())
print(f"  Sigma n_md_dalam_rentang_usrop = {s_in}  (defisi: benar-benar di dalam rentang md)")
print(f"  Sigma n_event_potensi_menandai = {s_pot}  (defisi: rentang +/- Delta max)")
print(f"  laporan §3 menulis: '170 event jatuh dalam rentang md USROP (potensi menandai)'")
c3 = (s_pot == 170)
print(f"  -> 170 == potensi_menandai? {c3} | 170 == dalam_rentang? {s_in == 170}")
if c3 and s_in != 170:
    print("  -> PARTIAL: angka 170 benar utk 'potensi menandai', tapi KALIMAT menyebut")
    print("     'dalam rentang md USROP' yang nilainya 157 -> wording menyesatkan.")

print("\n" + "=" * 78, "\nCLAIM 4: 'akun event: 884 -> 671 -> 506 dipakai'\n" + "=" * 78)
ev = dm["events"]
print(f"  total={ev['total']} (laporan 884) | wellbore_mapped={ev['wellbore_mapped']} (671) | "
      f"usable_md_valid={ev['usable_md_valid']} (506)")
c4 = ev["total"] == 884 and ev["wellbore_mapped"] == 671 and ev["usable_md_valid"] == 506
print(f"  -> {'PASS' if c4 else 'GAGAL'}")

print("\n" + "=" * 78, "\nCLAIM 5: 'window 10 m ~ 192 baris' + artefak §14 ada di disk\n" + "=" * 78)
log = (BASE / "docs" / "V2_PREDICTIVE_DATASET_RUN_LOG.txt").read_text(encoding="utf-8")
n192 = log.count("window 10 m ~ 192 baris")
print(f"  baris log build yang menyebut 'window 10 m ~ 192 baris': {n192}/7 wellbore")
artefak = re.findall(r"^\| `([^`]+)` \|", REPORT, flags=re.M)
missing = [a for a in artefak if not (BASE / a).exists()]
print(f"  artefak §14 terdaftar: {len(artefak)} | hilang di disk: {missing if missing else 'tidak ada'}")
c5 = (n192 == 7) and not missing
print(f"  -> {'PASS' if c5 else 'GAGAL'}")

print("\n" + "=" * 78)
print(f"RINGKASAN CLAIM LANJUTAN: claim1={'PASS' if c1 else 'GAGAL'}, "
      f"claim2={'PASS' if c2 else 'GAGAL'}, claim3={'PARTIAL' if (c3 and s_in != 170) else ('PASS' if c3 else 'GAGAL')}, "
      f"claim4={'PASS' if c4 else 'GAGAL'}, claim5={'PASS' if c5 else 'GAGAL'}")
json.dump({"claim1_distinct_event": [n_nid, n_nmd], "claim2_frac_gt30d": round(frac, 4),
           "claim3_sum_dalam_rentang": int(s_in), "claim3_sum_potensi": int(s_pot),
           "claim4_ok": bool(c4), "claim5_n192": n192, "claim5_missing_artifacts": missing},
          open(BASE / "docs" / "V2_ML_AUDIT_PART3.json", "w"), indent=2, ensure_ascii=False)
print("-> docs/V2_ML_AUDIT_PART3.json")
sys.exit(0)
