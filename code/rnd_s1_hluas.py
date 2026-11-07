#!/usr/bin/env python3
"""RND-S1 eksploratif: apa yang terjadi bila grid ambang CUSUM diperluas.

Pertanyaan: pada grid sekarang (maks 30) anggaran 6/1440 tidak pernah terpenuhi,
sehingga h tersaturasi. Bila grid diperluas sampai 600, pilih_h akan memilih h yang
benar-benar memenuhi anggaran di well kalibrasi. Yang diukur di sini: h terpilih,
laju alarm kalibrasi, dan konsekuensinya pada presisi, recall, FAR, serta lead H1
di sembilan fold. Varian ini diberi nama H1_hluas dan BUKAN bagian protokol R8.
"""
import json
import os
import sys

sys.path.insert(0, "/mnt/d/Capstone 1(v2)/code")
import numpy as np

import rnd_hybrid_harness as H

OUT = f"{H.BASE}/scratch/rnd/s1/s1_hluas.json"
EXT = (0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10, 12, 15, 20, 30, 40, 60, 80,
       100, 150, 200, 300, 400, 600)

df = H.muat_dataset(f"{H.DSD}/hyd_ki.csv.gz")
folds = H.muat_fold(f"{H.LOWOD}/lowo_hyd_ki.json")
well_df = H.pecah_well(df)
assert len(folds) == 9

rows = []
for f in folds:
    w = f["test_well"]
    cal = f["train_wells"][0]
    d = well_df[w]
    y = d["y_hyd"].to_numpy(int)
    ts = d["ts_bin"].to_numpy(int)
    zc, _ = H.seri_z(cal, well_df[cal]["ts_bin"].to_numpy(int))
    h = H.pilih_h(zc, grid=EXT)
    laju_cal = float(H.cusum_alarm(zc, h).mean())
    zv, _ = H.seri_z(w, ts)
    stat = H.jendela_alarm(H.cusum_alarm(zv, h))
    rule = H.gerbang_rule(w, ts)
    pred = ((stat == 1) & (rule == 1)).astype(int)
    rec = H.evaluasi_fold(y, pred, ts)
    rec.update(dict(fold=w, model="H1_hluas", h_terpilih=h, cal_well=cal,
                    laju_alarm_kalibrasi=laju_cal,
                    lolos_anggaran=bool(laju_cal <= H.ALPHA_BUDGET)))
    rows.append(rec)
    print(f"{w:8} h={h:6.1f} laju_cal={laju_cal:.6f} lolos={rec['lolos_anggaran']} "
          f"fp={rec['rows']['fp']:4d} tp={rec['rows']['tp']:4d} "
          f"prec={rec['rows']['precision']} rec={rec['rows']['recall']} "
          f"far_kal={rec['far24_kalender']} far_baris={rec['far24_baris']} "
          f"lead={rec['lead']['lead_median_min']}")

ring = H.ringkas_records(rows, "H1_hluas")
d0 = json.load(open(f"{H.BASE}/scratch/rnd/s1/s1_hyd_seeds.json"))
banding = {}
for m in ("fp_total", "tp_total", "precision_median", "recall_median",
          "far24_kalender_median", "far24_baris_median", "lead_median_median",
          "n_diperingatkan", "fold_far_le6", "cakupan_median"):
    lama = d0["per_seed"]["42"]["ringkas"].get(m)
    baru = ring.get(m)
    banding[m] = dict(lama=lama, baru=baru,
                      delta=(None if (lama is None or baru is None) else round(baru - lama, 4)))

out = dict(
    kartu="t_6890a1c7", model="H1_hluas", sifat="EKSPLORATIF, bukan protokol R8",
    grid_lama=list(H.H_GRID), grid_luas=list(EXT), alpha_budget=H.ALPHA_BUDGET,
    n_fold=len(rows), n_lolos_anggaran=int(sum(1 for r in rows if r["lolos_anggaran"])),
    ringkas=ring, banding=banding, per_fold=rows,
)
H.tulis_json(OUT, out)
print()
print("ringkas H1_hluas:", json.dumps(ring, indent=1))
print("n fold lolos anggaran:", out["n_lolos_anggaran"], "dari", out["n_fold"])
print("banding:", json.dumps({k: v["delta"] for k, v in banding.items()}, indent=1))
print("tulis", OUT)
