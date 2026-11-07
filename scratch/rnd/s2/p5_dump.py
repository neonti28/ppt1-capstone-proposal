#!/usr/bin/env python3
"""Dump angka kunci S2 dalam bentuk ringkas untuk penulisan dokumen dan ledger."""
import json

BASE = "/mnt/d/Capstone 1(v2)"
OUT = f"{BASE}/scratch/rnd/s2"
r = json.load(open(f"{OUT}/s2_ringkas.json"))

for kelas in ("vib", "ssi"):
    d = r[kelas]
    print(f"===== {kelas} =====")
    print(f"baris={d['n_baris']} well={d['n_well']} fitur={d['n_fitur']} "
          f"fold_total={d['n_fold_total']} fold_uji={d['n_fold_dapat_diuji']} "
          f"fold_gugur={d['n_fold_tidak_dapat_diuji']} pos_uji={d['n_pos_total_dapat_diuji']}")
    print("gugur:", d["tak_dapat_diuji"])
    print("wells:")
    for w in d["wells"]:
        print("  ", json.dumps(w, ensure_ascii=False))
    print("single terbaik:", d["single_terbaik"], "| hybrid terbaik:", d["hybrid_terbaik"])
    print("banding:", json.dumps(d["banding_hybrid_lawan_single"], ensure_ascii=False))
    print("separuh:")
    for m, v in d["lapisan_c_separuh"].items():
        print(f"   {m:32s} {v}")
    print("variasi seed:", json.dumps(d["variasi_seed_ml"], ensure_ascii=False))
    print()

print("===== justifikasi ambang positif =====")
for x in r["justifikasi_ambang_positif"]:
    print(json.dumps(x, ensure_ascii=False))
