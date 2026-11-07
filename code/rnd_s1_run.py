#!/usr/bin/env python3
"""RND-S1 — uji lintas seed H1 hyd memakai harness bersama.

Alur yang dijalankan skrip ini, berurutan dan gagal-keras:

1. Reproduksi seed 42 terhadap angka terbit R8 (FP 935, presisi median 0,7789,
   recall median 0,5638, lead median 11,5 menit). Bila selisih di luar toleransi,
   skrip menulis artefak kegagalan lalu berhenti sebelum menjalankan seed lain.
2. Jalankan H1 untuk daftar seed (default 42,7,13,21,33), sembilan fold LOWO
   per seed, lalu hitung delta tiap metrik terhadap seed 42.
3. Kontrol stokastik: komponen ML (LightGBM, random_state=seed) pada data hyd
   yang sama untuk daftar seed yang sama. Kontrol ini ada supaya klaim
   "varians H1 nol karena deterministik" bisa diuji: kalau kontrol juga nol,
   plambing seed di harness yang salah, bukan H1-nya yang deterministik.

Keluaran: scratch/rnd/s1/s1_hyd_seeds.json dan s1_meta.json
"""
import argparse
import hashlib
import json
import os
import platform
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rnd_hybrid_harness as H

OUT = f"{H.BASE}/scratch/rnd/s1"
DS = f"{H.DSD}/hyd_ki.csv.gz"
LOWO = f"{H.LOWOD}/lowo_hyd_ki.json"
R8 = f"{H.BASE}/scratch/rnd/r8/r8_hyd.json"

# Angka terbit R8 (bagian 4.1 dan 4.2) yang wajib direproduksi. Nilai ini hanya
# dipakai sebagai pengunci silang: pembanding sesungguhnya dibaca dari r8_hyd.json
# pada main(), lalu di-assert sama dengan konstanta di bawah. Dengan begitu tes
# reproduksi bisa GAGAL bila artefak R8 berubah, bukan hanya bila run kita meleset.
R8_TERBIT_SEHARUSNYA = dict(fp_total=935, precision_median=0.7789, recall_median=0.5638,
                            lead_median=11.5, tp_total=3804, n_onset=390,
                            n_diperingatkan=219)
TOL = dict(fp_total=0, precision_median=0.0001, recall_median=0.0001,
           lead_median=0.0001, tp_total=0, n_onset=0, n_diperingatkan=0)

MODEL = "H1_stat_dan_rule"
MODEL_ML = "ML_saja_kontrol"


def sha256(path, blok=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(blok)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", default="42,7,13,21,33")
    ap.add_argument("--kontrol", action="store_true",
                    help="jalankan kontrol stokastik ML pada seed yang sama")
    ap.add_argument("--tanpa-tulis", action="store_true")
    args = ap.parse_args()
    seeds = [int(s) for s in args.seeds.split(",")]
    t0 = time.time()
    log = []

    os.makedirs(OUT, exist_ok=True)
    H.log(f"muat data {DS}", log)
    df = H.muat_dataset(DS)
    folds = H.muat_fold(LOWO)
    well_df = H.pecah_well(df)
    H.log(f"data {df.shape} well {len(well_df)} fold {len(folds)} seed {seeds}", log)
    assert len(folds) == 9, f"fold bukan 9: {len(folds)}"

    r8 = json.load(open(R8))
    r8_ring = r8["ringkas"][MODEL]
    r8_rows_h1 = [r for r in r8["rows"] if r["model"] == MODEL]
    # Pembanding dibaca dari artefak R8, bukan dari konstanta skrip ini.
    R8_TERBIT = dict(
        fp_total=int(r8_ring["fp_total"]),
        precision_median=float(r8_ring["precision_median"]),
        recall_median=float(r8_ring["recall_median"]),
        lead_median=float(r8_ring["lead_median_median"]),
        tp_total=int(r8_ring["tp_total"]),
        n_onset=int(sum(r["lead"]["n_onset"] for r in r8_rows_h1)),
        n_diperingatkan=int(sum(r["lead"]["n_diperingatkan"] for r in r8_rows_h1)),
    )
    for k, v in R8_TERBIT_SEHARUSNYA.items():
        assert abs(float(R8_TERBIT[k]) - float(v)) <= 1e-9, (
            f"angka terbit kartu {k}={v} beda dari r8_hyd.json {R8_TERBIT[k]}")

    # ---------------------------------------------------------- 1. reproduksi
    H.log("reproduksi seed 42 ...", log)
    rec42 = H.jalankan_h1(seed=42, well_df=well_df, folds=folds)
    ring42 = H.ringkas_records(rec42, MODEL)
    aktual = dict(fp_total=ring42["fp_total"], precision_median=ring42["precision_median"],
                  recall_median=ring42["recall_median"],
                  lead_median=ring42["lead_median_median"],
                  tp_total=ring42["tp_total"], n_onset=ring42["n_onset"],
                  n_diperingatkan=ring42["n_diperingatkan"])
    delta = {k: (None if aktual[k] is None else round(aktual[k] - R8_TERBIT[k], 6))
             for k in R8_TERBIT}
    lulus = {k: (delta[k] is not None and abs(delta[k]) <= TOL[k]) for k in R8_TERBIT}
    per_fold_r8 = {}
    for r in r8["rows"]:
        if r["model"] == MODEL:
            per_fold_r8[r["fold"]] = dict(fp=int(r["rows"]["fp"]), tp=int(r["rows"]["tp"]),
                                          far24_kalender=r["far24_kalender"],
                                          precision=r["rows"]["precision"],
                                          recall=r["rows"]["recall"],
                                          lead=r["lead"]["lead_median_min"],
                                          h=r["h_terpilih"])
    per_fold_kini = {}
    for r in rec42:
        if r["model"] == MODEL:
            per_fold_kini[r["fold"]] = dict(fp=int(r["rows"]["fp"]), tp=int(r["rows"]["tp"]),
                                            far24_kalender=r["far24_kalender"],
                                            precision=r["rows"]["precision"],
                                            recall=r["rows"]["recall"],
                                            lead=r["lead"]["lead_median_min"],
                                            h=r["h_terpilih"])
    per_fold = []
    for f in sorted(per_fold_r8):
        a, b = per_fold_r8[f], per_fold_kini.get(f, {})
        per_fold.append(dict(fold=f, fp_r8=a["fp"], fp_kini=b.get("fp"),
                             fp_delta=None if b.get("fp") is None else b["fp"] - a["fp"],
                             tp_r8=a["tp"], tp_kini=b.get("tp"),
                             tp_delta=None if b.get("tp") is None else b["tp"] - a["tp"],
                             far24_r8=a["far24_kalender"], far24_kini=b.get("far24_kalender"),
                             h_r8=a["h"], h_kini=b.get("h")))
    reproduksi = dict(model=MODEL, terbit_r8=R8_TERBIT, terbit_sumber=R8,
                      terbit_pengunci_skrip=R8_TERBIT_SEHARUSNYA, aktual=aktual, delta=delta,
                      toleransi=TOL, lulus=lulus,
                      semua_lulus=bool(all(lulus.values())), per_fold=per_fold,
                      ringkas_r8=r8_ring, ringkas_kini=ring42)
    H.log(f"reproduksi: {json.dumps(aktual)} lulus={reproduksi['semua_lulus']}", log)

    if not reproduksi["semua_lulus"]:
        H.log("REPRODUKSI GAGAL, berhenti sebelum seed lain", log)
        if not args.tanpa_tulis:
            H.tulis_json(f"{OUT}/s1_hyd_seeds.json",
                         dict(kartu="t_6890a1c7", status="GAGAL_REPRODUKSI",
                              reproduksi=reproduksi, log=log))
        sys.exit(2)

    # ------------------------------------------------------ 2. lintas seed H1
    per_seed = {}
    for s in seeds:
        H.log(f"H1 seed {s} ...", log)
        rec = rec42 if s == 42 else H.jalankan_h1(seed=s, well_df=well_df, folds=folds)
        ring = H.ringkas_records(rec, MODEL)
        per_seed[str(s)] = dict(seed=s, ringkas=ring, folds=rec,
                                sidik=H.sidik_metrik(rec, MODEL))

    metrik = ("fp_total", "tp_total", "precision_median", "recall_median",
              "far24_kalender_median", "far24_kalender_min", "far24_kalender_maks",
              "far24_baris_median", "lead_median_median", "n_diperingatkan",
              "fold_far_le6", "fold_gate_A_baru", "cakupan_median")
    lintas = {}
    for m in metrik:
        vals = [per_seed[str(s)]["ringkas"].get(m) for s in seeds]
        v = [x for x in vals if x is not None]
        lintas[m] = dict(
            per_seed={str(s): per_seed[str(s)]["ringkas"].get(m) for s in seeds},
            median=round(float(np.median(v)), 4) if v else None,
            min=round(float(min(v)), 4) if v else None,
            maks=round(float(max(v)), 4) if v else None,
            rentang=round(float(max(v) - min(v)), 4) if v else None,
        )
    delta_seed = {}
    base = per_seed[str(seeds[0])]["sidik"]
    for s in seeds:
        sid = per_seed[str(s)]["sidik"]
        delta_seed[str(s)] = {k: (0 if sid[k] == base[k] else
                                  sum(1 for x, y in zip(sid[k], base[k]) if x != y))
                              for k in base}
    n_fold_berbeda = max(max(v.values()) for v in delta_seed.values())
    H.log(f"H1 lintas seed: fold berbeda maksimum {n_fold_berbeda}", log)

    # ------------------------------------------------ 3. kontrol stokastik ML
    kontrol = None
    if args.kontrol:
        feats = H.fitur_dari(df)
        H.log(f"kontrol stokastik ML, fitur {len(feats)} ...", log)
        kontrol = dict(model=MODEL_ML, n_fitur=len(feats), per_seed={})
        for s in seeds:
            recs = []
            for f in folds:
                w = f["test_well"]
                d = well_df[w]
                y = d["y_hyd"].to_numpy(int)
                ts = d["ts_bin"].to_numpy(int)
                ml = H.skor_ml_fold(well_df, f, "y_hyd", feats, seed=s)
                pred = (ml["skor"] >= ml["ambang"]).astype(int)
                rec = H.evaluasi_fold(y, pred, ts)
                rec.update(dict(fold=w, model=MODEL_ML, seed=s, ambang=round(ml["ambang"], 8),
                                cal_well=ml["cal_well"], n=len(y), n_pos=int(y.sum())))
                recs.append(rec)
            ring = H.ringkas_records(recs, MODEL_ML)
            kontrol["per_seed"][str(s)] = dict(seed=s, ringkas=ring, folds=recs)
            H.log(f"kontrol seed {s}: FP {ring['fp_total']} presisi {ring['precision_median']} "
                  f"recall {ring['recall_median']}", log)
        fps = [kontrol["per_seed"][str(s)]["ringkas"]["fp_total"] for s in seeds]
        prs = [kontrol["per_seed"][str(s)]["ringkas"]["precision_median"] for s in seeds]
        rcs = [kontrol["per_seed"][str(s)]["ringkas"]["recall_median"] for s in seeds]
        kontrol["sebaran"] = dict(
            fp_min=int(min(fps)), fp_maks=int(max(fps)), fp_rentang=int(max(fps) - min(fps)),
            precision_rentang=round(float(max(prs) - min(prs)), 4),
            recall_rentang=round(float(max(rcs) - min(rcs)), 4),
            ada_varians=bool(len(set(fps)) > 1 or len(set(prs)) > 1 or len(set(rcs)) > 1),
        )
        H.log(f"kontrol sebaran: {json.dumps(kontrol['sebaran'])}", log)

    # -------------------------------------------------------------- 4. keluaran
    hasil = dict(
        kartu="t_6890a1c7", status="OK",
        tanggal=time.strftime("%Y-%m-%d %H:%M:%S"),
        seed_list=seeds, model=MODEL,
        konstanta=dict(alpha_budget=H.ALPHA_BUDGET, lead_horizon=H.LEAD_HORIZON,
                       w_jendela=H.W_JENDELA, cusum_k=H.CUSUM_K,
                       h_grid=list(H.H_GRID), far_maks=H.FAR_MAKS,
                       recall_min=H.RECALL_MIN, cakupan_min=H.CAKUPAN_MIN),
        reproduksi=reproduksi,
        per_seed={k: dict(seed=v["seed"], ringkas=v["ringkas"], sidik=v["sidik"],
                          folds=v["folds"]) for k, v in per_seed.items()},
        lintas_seed=lintas,
        delta_fold_terhadap_seed_pertama=delta_seed,
        n_fold_berbeda_maks=n_fold_berbeda,
        kontrol_stokastik=kontrol,
        log=log,
    )
    meta = dict(
        kartu="t_6890a1c7", tanggal=hasil["tanggal"],
        elapsed_s=round(time.time() - t0, 1),
        python=platform.python_version(), executable=sys.executable,
        pandas=pd.__version__, numpy=np.__version__,
        dataset=DS, dataset_shape=list(df.shape),
        dataset_sha256=sha256(DS),
        fold_file=LOWO, n_fold=len(folds),
        wells={w: int(len(well_df[w])) for w in well_df},
        per_well_pos={w: int(well_df[w]["y_hyd"].sum()) for w in well_df},
        per_well_menit_kalender={w: int(well_df[w]["ts_bin"].max() - well_df[w]["ts_bin"].min() + 1)
                                 for w in well_df},
        r8_artefak=R8, r8_sha256=sha256(R8),
        skrip=os.path.abspath(__file__), harness=os.path.abspath(H.__file__),
        harness_sha256=sha256(os.path.abspath(H.__file__)),
        perintah=" ".join([sys.executable] + sys.argv),
    )
    if not args.tanpa_tulis:
        p1 = H.tulis_json(f"{OUT}/s1_hyd_seeds.json", hasil)
        p2 = H.tulis_json(f"{OUT}/s1_meta.json", meta)
        H.log(f"tulis {p1}", log)
        H.log(f"tulis {p2}", log)
    print(json.dumps(dict(status="OK", n_fold_berbeda=n_fold_berbeda,
                          lintas_seed={k: {kk: vv for kk, vv in v.items() if kk != "per_seed"}
                                       for k, v in lintas.items()},
                          kontrol=(kontrol or {}).get("sebaran")), indent=1))


if __name__ == "__main__":
    main()
