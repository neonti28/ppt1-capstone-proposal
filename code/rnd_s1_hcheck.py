#!/usr/bin/env python3
"""RND-S1 -- pemeriksaan saturasi ambang CUSUM (artefak mentah s1_h_saturasi.json).

Pertanyaan yang dijawab skrip ini, satu pertanyaan satu ukuran:

1. Apakah h=30 dipilih karena memenuhi anggaran FAR, atau karena grid habis?
   Ukur laju alarm CUSUM pada h=H_GRID[-1] di well kalibrasi tiap fold, bandingkan
   dengan anggaran ALPHA_BUDGET. Bila laju > anggaran, pilih_h jatuh ke fallback.
2. Berapa h terkecil yang benar-benar memenuhi anggaran bila grid diperluas?
   Pindai h di luar grid (40 sampai 600) pada well kalibrasi yang sama.
3. Well kalibrasi mana yang dipakai tiap fold? (train_wells[0])

Keluaran: scratch/rnd/s1/s1_h_saturasi.json
"""
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rnd_hybrid_harness as H

OUT = f"{H.BASE}/scratch/rnd/s1"
DS = f"{H.DSD}/hyd_ki.csv.gz"
LOWO = f"{H.LOWOD}/lowo_hyd_ki.json"
GRID_LUAR = (40, 50, 60, 80, 100, 120, 150, 200, 250, 300, 400, 500, 600)


def main():
    t0 = time.time()
    df = H.muat_dataset(DS)
    folds = H.muat_fold(LOWO)
    well_df = H.pecah_well(df)
    h_maks = float(H.H_GRID[-1])
    budget = float(H.ALPHA_BUDGET)

    zcache = {}

    def z(well):
        if well not in zcache:
            ts = well_df[well]["ts_bin"].to_numpy(int)
            zcache[well] = H.seri_z(well, ts)
        return zcache[well]

    per_fold = []
    for f in folds:
        w = f["test_well"]
        cal = f["train_wells"][0]
        zc, _ = z(cal)
        laju_maks = float(H.cusum_alarm(zc, h_maks).mean())
        h_dipilih = float(H.pilih_h(zc, budget=budget))
        per_fold.append(dict(
            fold=w, cal_well=cal, n_cal=int(len(zc)),
            h_grid_maks=h_maks, laju_alarm_h_maks=laju_maks,
            lolos_anggaran=laju_maks <= budget,
            h_dipilih=h_dipilih,
            saturasi=bool(h_dipilih >= h_maks and laju_maks > budget),
        ))

    # perluasan grid pada well kalibrasi pertama
    cal0 = folds[0]["train_wells"][0]
    z0, _ = z(cal0)
    pindai = []
    for h in GRID_LUAR:
        laju = float(H.cusum_alarm(z0, h).mean())
        pindai.append(dict(h=float(h), laju_alarm=laju, lolos_anggaran=laju <= budget))
    h_cukup = next((p["h"] for p in pindai if p["lolos_anggaran"]), None)

    n_saturasi = sum(1 for r in per_fold if r["saturasi"])
    hasil = dict(
        kartu="t_6890a1c7",
        tanggal=time.strftime("%Y-%m-%d %H:%M:%S"),
        pertanyaan="apakah h=30 terkalibrasi atau tersaturasi di batas grid",
        anggaran_alpha=budget,
        h_grid=list(H.H_GRID),
        h_grid_maks=h_maks,
        cusum_k=H.CUSUM_K,
        per_fold=per_fold,
        n_fold=len(per_fold),
        n_saturasi=n_saturasi,
        well_kalibrasi_unik=sorted({r["cal_well"] for r in per_fold}),
        pindai_h_luar_grid_well=cal0,
        pindai=pindai,
        h_terkecil_lolos_anggaran_di_luar_grid=h_cukup,
        kesimpulan=("saturasi" if n_saturasi == len(per_fold) else
                    ("sebagian" if n_saturasi else "tidak_saturasi")),
        elapsed_s=round(time.time() - t0, 1),
    )
    p = H.tulis_json(f"{OUT}/s1_h_saturasi.json", hasil)
    print(json.dumps(dict(status="OK", n_saturasi=n_saturasi, n_fold=len(per_fold),
                          anggaran=budget, h_maks=h_maks,
                          well_kalibrasi=hasil["well_kalibrasi_unik"],
                          h_cukup_di_luar_grid=h_cukup,
                          tulis=p), indent=1))
    for r in per_fold:
        print(f"  {r['fold']:8} cal={r['cal_well']:6} laju_h{h_maks:.0f}={r['laju_alarm_h_maks']:.6f} "
              f"lolos={r['lolos_anggaran']} saturasi={r['saturasi']}")


if __name__ == "__main__":
    main()
