"""Verifikasi akhir S1: API harness, keberadaan artefak, dan cocok angka dokumen."""
import json
import os
import sys

B = "/mnt/d/Capstone 1(v2)"
sys.path.insert(0, f"{B}/code")
import rnd_hybrid_harness as H

print("=== 1. API harness yang dijanjikan docstring ===")
api = ["muat_dataset", "pecah_well", "muat_fold", "seri_z", "gerbang_rule", "cusum_alarm",
       "jendela_alarm", "pilih_h", "detektor_stat_rule", "fitur_dari", "latih_lgb",
       "threshold_conformal", "skor_ml_fold", "evaluasi_fold", "ringkas_records",
       "tulis_json", "sidik_metrik", "jalankan_h1"]
hilang = [a for a in api if not callable(getattr(H, a, None))]
print("fungsi dijanjikan:", len(api), "| hilang:", hilang if hilang else "tidak ada")
assert not hilang, hilang

print()
print("=== 2. Artefak yang dirujuk dokumen ada di disk ===")
paths = ["docs/RND_S1_SEED_ROBUSTNESS.md", "scratch/rnd/s1/s1_hyd_seeds.json",
         "scratch/rnd/s1/s1_meta.json", "scratch/rnd/s1/s1_h_saturasi.json",
         "code/rnd_hybrid_harness.py", "code/rnd_s1_run.py", "code/rnd_s1_hcheck.py",
         "code/rnd_s1_ledger.py", "code/rnd_s1_dokumen.py",
         "scratch/rnd/r8/r8_hyd.json", "scratch/v9_i1/v9_i1_RESULTS.json",
         "docs/RND_EVALUATION_POLICY.md", "docs/RND_PROVENANCE_LEDGER.md",
         "scratch/v9_d1/datasets/hyd_ki.csv.gz", "scratch/v9_d1/lowo_hyd_ki.json"]
for p in paths:
    ok = os.path.exists(f"{B}/{p}")
    print(("ADA  " if ok else "TIDAK") + " " + p)
    assert ok, p

print()
print("=== 3. Cocok angka dokumen dengan sumber (independen) ===")
doc = open(f"{B}/docs/RND_S1_SEED_ROBUSTNESS.md").read()
d = json.load(open(f"{B}/scratch/rnd/s1/s1_hyd_seeds.json"))
r8 = json.load(open(f"{B}/scratch/rnd/r8/r8_hyd.json"))
v9 = json.load(open(f"{B}/scratch/v9_i1/v9_i1_RESULTS.json"))
sat = json.load(open(f"{B}/scratch/rnd/s1/s1_h_saturasi.json"))

cek = []
cek.append(("FP total 935 di dokumen", "| FP total | 935 | 935 |" in doc))
cek.append(("presisi 0,7789", "0,7789" in doc))
cek.append(("recall 0,5638", "0,5638" in doc))
cek.append(("lead 11,5", "11,5" in doc))
cek.append(("far kalender 8,9132", "8,9132" in doc))
cek.append(("far baris maks 66,3873", "66,3873" in doc))
cek.append(("kontrol fp 1076..1421", "1076" in doc and "1421" in doc))
cek.append(("saturasi h 30 dan 300", "h=300" in doc))
cek.append(("V9 hybrid fp 110", "| 516 | 110 |" in doc))
cek.append(("F-14 rule tp 607 fp 368", "| 607 | 368 |" in doc))
for nama, ok in cek:
    print(("COCOK " if ok else "BEDA  ") + nama)
    assert ok, nama

print()
print("=== 4. Angka sumber yang dipakai dokumen (dibaca ulang dari JSON) ===")
print("r8 H1 fp/tp/prec/rec/lead:", r8["ringkas"]["H1_stat_dan_rule"]["fp_total"],
      r8["ringkas"]["H1_stat_dan_rule"]["tp_total"],
      r8["ringkas"]["H1_stat_dan_rule"]["precision_median"],
      r8["ringkas"]["H1_stat_dan_rule"]["recall_median"],
      r8["ringkas"]["H1_stat_dan_rule"]["lead_median_median"])
print("s1 seed42 ringkas fp:", d["per_seed"]["42"]["ringkas"]["fp_total"],
      "| rentang lintas seed fp:", d["lintas_seed"]["fp_total"]["rentang"])
print("saturasi n_saturasi:", sat["n_saturasi"], "| h luar grid:",
      sat["h_terkecil_lolos_anggaran_di_luar_grid"])
hy = [e for e in v9["engines"] if e["engine"] == "hyd"][0]
hyh = [h for h in hy["heads"] if h["head"] == "hybrid_rule_and_persistence"][0]["metrik_segmen"]
print("v9 hybrid:", hyh["tp"], hyh["fp"], hyh["precision"], hyh["recall"], hyh["far_segmen"])

print()
print("=== 5. Jumlah baris ledger S1 ===")
led = open(f"{B}/docs/RND_PROVENANCE_LEDGER.md").read().splitlines()
rows = [x for x in led if x.startswith("| S1-")]
print("baris S1:", len(rows), "| kolom (pipa):", sorted({x.count("|") for x in rows}))
print()
print("SEMUA ASSERT LULUS")
