#!/usr/bin/env python3
"""S5 probe: angka pasti untuk laporan (rekap rerun, hash dokumen, ukuran artefak)."""
import hashlib
import json
import os

BASE = "/mnt/d/Capstone 1(v2)"
r = json.load(open(f"{BASE}/scratch/rnd/s5/s5_rerun.json", encoding="utf-8"))
print("rekap:", json.dumps(r["rekap"], ensure_ascii=False))
for k in ("tabel_5_1", "tabel_5_2", "tabel_6_1", "tabel_4"):
    t = r[k]
    n_sel = sum(len(v.get("per_seed", {})) if isinstance(v, dict) else 0 for v in t.values()) if isinstance(t, dict) else 0
    gagal = r.get("rekap", {}).get(k.replace("tabel_", "t") .replace("_", "") + "_gagal")
    print(f" {k}: n_metrik={len(t)} n_sel_per_seed={n_sel} kunci_metrik={list(t)[:4]}")
print("selisih_rerun_vs_json:", json.dumps(r["selisih_rerun_vs_json"], ensure_ascii=False)[:200])
print("selisih_rerun_vs_dokumen:", json.dumps(r["selisih_rerun_vs_dokumen"], ensure_ascii=False)[:200])
print("rerun:", json.dumps(r["rerun"], ensure_ascii=False))

n = json.load(open(f"{BASE}/scratch/rnd/s5/s5_negative.json", encoding="utf-8"))
print("\nnegatif rekap:", json.dumps(n.get("rekap", {}), ensure_ascii=False))
print("negatif t61:", json.dumps(n.get("tabel_6_1", {}).get("F-10", {}), ensure_ascii=False)[:300])

print("\n== hash dokumen ==")
for f in ("docs/RND_S1_SEED_ROBUSTNESS.md", "docs/RND_S2_HYBRID_VIB_SSI.md",
          "docs/RND_S3_HYBRID_BITWEAR.md", "docs/RND_S4_LAYER_B_DATA.md",
          "docs/RND_PROVENANCE_LEDGER.md", "docs/RND_EVALUATION_POLICY.md",
          "code/rnd_hybrid_harness.py", "scratch/rnd/s1/s1_hyd_seeds.json"):
    p = f"{BASE}/{f}"
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
    print(f" {f} {os.path.getsize(p)}B {h}")

print("\n== artefak per kartu ==")
for kode in ("s1", "s2", "s3", "s4"):
    d = f"{BASE}/scratch/rnd/{kode}"
    for f in sorted(os.listdir(d)):
        p = os.path.join(d, f)
        if os.path.isfile(p) and f.endswith((".json", ".jsonl")):
            print(f" {kode}/{f} {os.path.getsize(p)}B")
print(" 645763 cek:", os.path.getsize(f"{BASE}/data/volve/external/volve_catalog_target_paths.csv"))
