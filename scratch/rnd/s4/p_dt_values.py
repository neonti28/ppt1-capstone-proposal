"""Probe: nilai mentah kolom tabel downtime (kenapa semua 0)."""
import json, os, re
from collections import Counter
ROOT = "/mnt/d/Capstone 1(v2)"
P = os.path.join(ROOT, "scratch/rnd/s4/ddr_downtime_records.jsonl")
recs = [json.loads(l) for l in open(P, encoding="utf-8")]
print("n:", len(recs))
print("--- nilai downtime_min mentah (top) ---")
print(Counter(r["downtime_min"] for r in recs).most_common(10))
print("--- nilai equipment_repaired mentah (top) ---")
print(Counter(r["equipment_repaired"] for r in recs).most_common(10))
print("--- n_kolom ---")
print(Counter(r["n_kolom"] for r in recs).most_common())
print("--- 8 record contoh (semua kolom) ---")
for r in recs[:8]:
    print({k: (v[:70] if isinstance(v, str) else v) for k, v in r.items()})
print("--- remark yang memuat angka jam/menit ---")
pat = re.compile(r"(\d+[.,]?\d*)\s*(hrs?|hours?|h\b|min)", re.I)
hit = [r for r in recs if pat.search(r["remark"])]
print("n remark berangka durasi:", len(hit), "dari", len(recs))
for r in hit[:5]:
    print("  ", r["file"], "|", r["remark"][:120])
