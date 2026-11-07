#!/usr/bin/env python3
"""RND-S6 driver: uji kandidat pra-riset (D-A3: rule DAN persistence) lawan
kandidat pasca-riset (H1: statistik DAN rule, H2: ML dan statistik) memakai
harness bersama S1, pada kelas status hyd, vib, dan ssi.

Prinsip:
1. Tidak ada harness kedua. Semua sinyal, evaluasi, dan ringkasan dari
   code/rnd_hybrid_harness.py. Kanal gerbang vib/ssi dipilih oleh fungsi yang
   sudah dipakai S2 (pilih_kanal_rule) supaya perbandingan setara.
2. Reproduksi dulu: H1 hyd wajib sama persis dengan S1/R8, dan rule serta H1
   vib/ssi wajib sama persis dengan artefak S2. Bila meleset, skrip berhenti.
3. H1p = rule(t-1) DAN persistence(t) dibangun dari primitif harness dan kolom
   y_prev_<kelas> yang sudah ada di dataset V9. Tidak ada implementasi baru
   untuk komponen mana pun.
4. Seed hanya boleh menyentuh jalur acak. H1p deterministik, jadi dua seed wajib
   identik; kontrol ML dua fold dipakai untuk membuktikan seed benar tersambung.
"""
from __future__ import annotations

import json
import os
import sys
import time

import numpy as np
import pandas as pd

BASE = "/mnt/d/Capstone 1(v2)"
sys.path.insert(0, f"{BASE}/code")
sys.path.insert(0, f"{BASE}/scratch/rnd/s2")
import rnd_hybrid_harness as H  # noqa: E402
import s2a_run as S2  # noqa: E402

OUT = f"{BASE}/scratch/rnd/s6"
DSD = f"{BASE}/scratch/v9_d1/datasets"
LOWOD = f"{BASE}/scratch/v9_d1"
S2OUT = f"{BASE}/scratch/rnd/s2"
TOL = 5e-5

KELAS = {
    "hyd": dict(y="y_hyd", prev="y_prev_hyd", fold="lowo_hyd_ki.json"),
    "vib": dict(y="y_vib", prev="y_prev_vib", fold="lowo_vib.json"),
    "ssi": dict(y="y_ssi", prev="y_prev_ssi", fold="lowo_ssi.json"),
}


def evaluasi(nama, pred, y, ts, kelas, fold, seed, extra=None):
    rec = H.evaluasi_fold(y, pred, ts)
    rec.update(dict(kelas=kelas, model=nama, fold=fold, seed=int(seed),
                    n=len(y), n_pos=int(np.asarray(y).sum())))
    if extra:
        rec.update(extra)
    return rec


def jalankan_hyd(seed):
    cfg = KELAS["hyd"]
    df = H.muat_dataset(f"{DSD}/hyd_ki.csv.gz")
    well_df = H.pecah_well(df)
    folds = H.muat_fold(f"{LOWOD}/{cfg['fold']}")
    recs = []
    for f in folds:
        w = f["test_well"]
        d = well_df[w]
        y = d[cfg["y"]].to_numpy(int)
        ts = d["ts_bin"].to_numpy(int)
        cal = f["train_wells"][0]
        ts_cal = well_df[cal]["ts_bin"].to_numpy(int)
        sig = H.detektor_stat_rule(w, ts, cal, ts_cal, chan="SPPA")
        pers = d[cfg["prev"]].fillna(0).to_numpy(int)
        pred = {
            "rule_kanal": sig["rule"],
            "persistence": pers,
            "H1p_rule_dan_persist": ((sig["rule"] == 1) & (pers == 1)).astype(int),
            "H1_stat_dan_rule": sig["h1"],
            "H1b_stat_atau_rule": sig["h1b"],
            "H1p3_rule_persist_stat": ((sig["rule"] == 1) & (pers == 1) & (sig["stat"] == 1)).astype(int),
            "stat_cusum": sig["stat"],
        }
        for nama, p in pred.items():
            recs.append(evaluasi(nama, p, y, ts, "hyd", w, seed,
                                 extra=dict(h_terpilih=sig["h"], cal_well=cal)))
    return recs


def jalankan_vib_ssi(kelas, seed):
    cfg = KELAS[kelas]
    df = H.muat_dataset(f"{DSD}/{kelas}.csv.gz")
    well_df = H.pecah_well(df)
    folds = H.muat_fold(f"{LOWOD}/{cfg['fold']}")
    cache = S2.CacheSinyal(f"s6_{kelas}")
    recs = []
    for f in folds:
        w = f["test_well"]
        d = well_df[w]
        y = d[cfg["y"]].to_numpy(int)
        ts = d["ts_bin"].to_numpy(int)
        n_pos = int(y.sum())
        sel = S2.pilih_kanal_rule(well_df, f, cfg["y"], cache)
        chan, thr = sel["kanal"], sel["thr"]
        pers = d[cfg["prev"]].fillna(0).to_numpy(int)
        if chan is None:
            continue
        cal = f["train_wells"][0]
        sig = H.detektor_stat_rule(w, ts, cal, well_df[cal]["ts_bin"].to_numpy(int),
                                  chan=chan, alpha=H.ALPHA_BUDGET)
        rule = cache.gerbang(w, ts, chan, thr)
        pred = {
            "rule_kanal": rule,
            "persistence": pers,
            "H1p_rule_dan_persist": ((rule == 1) & (pers == 1)).astype(int),
            "H1_stat_dan_rule": ((sig["stat"] == 1) & (rule == 1)).astype(int),
            "H1b_stat_atau_rule": ((sig["stat"] == 1) | (rule == 1)).astype(int),
            "stat_cusum": sig["stat"],
        }
        for nama, p in pred.items():
            recs.append(evaluasi(nama, p, y, ts, kelas, w, seed,
                                 extra=dict(h_terpilih=sig["h"], kanal=chan,
                                            thr=thr, n_pos=n_pos,
                                            dapat_diuji=bool(n_pos >= S2.MIN_POS_UJI))))
    return recs


def kontrol_ml_seed(seed, folds_ambil=("F-14", "F-5")):
    """Bukti seed tersambung: skor ML pada fold sama harus berbeda antar seed."""
    df = H.muat_dataset(f"{DSD}/hyd_ki.csv.gz")
    well_df = H.pecah_well(df)
    folds = [f for f in H.muat_fold(f"{LOWOD}/lowo_hyd_ki.json")
             if f["test_well"] in folds_ambil]
    feats = H.fitur_dari(df)
    out = []
    for f in folds:
        info = H.skor_ml_fold(well_df, f, "y_hyd", feats, seed=seed, alpha=H.ALPHA_BUDGET)
        y = well_df[f["test_well"]]["y_hyd"].to_numpy(int)
        pred = (info["skor"] >= info["ambang"]).astype(int)
        out.append(dict(seed=int(seed), fold=f["test_well"], ambang=float(info["ambang"]),
                        fp=int(((pred == 1) & (y == 0)).sum()),
                        tp=int(((pred == 1) & (y == 1)).sum()),
                        ck_pertama=round(float(np.round(info["skor"], 6).sum()), 6)))
    return out


def sidik(recs, kelas, model):
    sub = [r for r in recs if r["kelas"] == kelas and r["model"] == model]
    return {
        "fp": [int(r["rows"]["fp"]) for r in sub],
        "tp": [int(r["rows"]["tp"]) for r in sub],
        "far24_kalender": [r["far24_kalender"] for r in sub],
        "recall": [r["rows"]["recall"] for r in sub],
        "presisi": [r["rows"]["precision"] for r in sub],
    }


def main():
    os.makedirs(OUT, exist_ok=True)
    t0 = time.time()
    log = []
    ringkasan = {}
    semua = {}

    for seed in (42, 13):
        print(f"== seed {seed}", flush=True)
        hyd = jalankan_hyd(seed)
        vib = jalankan_vib_ssi("vib", seed)
        ssi = jalankan_vib_ssi("ssi", seed)
        semua[seed] = dict(hyd=hyd, vib=vib, ssi=ssi)
        print(f"   hyd {len(hyd)} rec, vib {len(vib)} rec, ssi {len(ssi)} rec "
              f"({time.time() - t0:.1f} s)", flush=True)

    # ---- kontrol reproduksi R8/S1 pada hyd (seed 42 dan 13, keduanya wajib) ----
    reproduksi = []
    for seed in (42, 13):
        h1 = [r for r in semua[seed]["hyd"] if r["model"] == "H1_stat_dan_rule"]
        rule = [r for r in semua[seed]["hyd"] if r["model"] == "rule_kanal"]
        cek = dict(
            seed=int(seed),
            fp_total=int(sum(r["rows"]["fp"] for r in h1)),
            tp_total=int(sum(r["rows"]["tp"] for r in h1)),
            fp_rule_total=int(sum(r["rows"]["fp"] for r in rule)),
            tp_rule_total=int(sum(r["rows"]["tp"] for r in rule)),
            n_onset=int(sum(r["lead"]["n_onset"] for r in h1)),
            n_diperingatkan=int(sum(r["lead"]["n_diperingatkan"] for r in h1)),
            presisi_median=H.ringkas_records(h1)["precision_median"],
            recall_median=H.ringkas_records(h1)["recall_median"],
            lead_median=H.ringkas_records(h1)["lead_median_median"],
            h_per_fold=[r["h_terpilih"] for r in h1],
        )
        assert cek["fp_total"] == 935, cek
        assert cek["tp_total"] == 3804, cek
        assert cek["fp_rule_total"] == 2105, cek
        assert cek["tp_rule_total"] == 5579, cek
        assert abs(cek["presisi_median"] - 0.7789) < TOL, cek
        assert abs(cek["recall_median"] - 0.5638) < TOL, cek
        assert abs(cek["lead_median"] - 11.5) < TOL, cek
        assert cek["h_per_fold"] == [30.0] * 9, cek
        reproduksi.append(cek)
        log.append(f"reproduksi H1 hyd seed {seed}: FP 935 TP 3804 P 0,7789 R 0,5638 LULUS")

    # ---- reproduksi angka S2 untuk vib/ssi ----
    # Bentuk artefak S2: dokumen berisi folds[], lalu folds[i].models[model].rows.
    repro_s2 = []
    galat_s2 = []
    for kelas in ("vib", "ssi"):
        pub = json.load(open(f"{S2OUT}/s2_records_{kelas}.json"))
        pubfold = {f["fold"]: f for f in pub["folds"]}
        for model in ("persistence", "rule_kanal", "stat_cusum", "H1_stat_dan_rule"):
            mine = [r for r in semua[42][kelas] if r["model"] == model]
            assert mine, (kelas, model)
            n_cocok = 0
            for b in mine:
                pf = pubfold.get(b["fold"])
                if pf is None or model not in pf["models"]:
                    galat_s2.append(dict(kelas=kelas, model=model, fold=b["fold"], sebab="fold/model hilang"))
                    continue
                a = pf["models"][model]["rows"]
                for k in ("tp", "fp"):
                    if int(a[k]) != int(b["rows"][k]):
                        galat_s2.append(dict(kelas=kelas, model=model, fold=b["fold"], sel=k,
                                             s2=int(a[k]), s6=int(b["rows"][k])))
                for k in ("precision", "recall"):
                    va, vb = a.get(k), b["rows"].get(k)
                    if va is None or vb is None:
                        if not (va is None and vb is None):
                            galat_s2.append(dict(kelas=kelas, model=model, fold=b["fold"], sel=k,
                                                 s2=va, s6=vb))
                        continue
                    if abs(float(va) - float(vb)) >= TOL:
                        galat_s2.append(dict(kelas=kelas, model=model, fold=b["fold"], sel=k,
                                             s2=float(va), s6=float(vb)))
                n_cocok += 1
            log.append(f"reproduksi S2 {kelas}/{model}: {n_cocok} fold dibandingkan")
            repro_s2.append(dict(kelas=kelas, model=model, n_fold=n_cocok,
                                 status="COCOK" if not galat_s2 else "ADA_SELISIH"))

    # ---- seed tidak boleh mengubah H1p ----
    seed_cek = {}
    for kelas in ("hyd", "vib", "ssi"):
        for model in ("H1p_rule_dan_persist", "H1_stat_dan_rule", "rule_kanal"):
            a = sidik(semua[42][kelas], kelas, model)
            b = sidik(semua[13][kelas], kelas, model)
            beda = sum(1 for k in a for x, y in zip(a[k], b[k]) if x != y)
            seed_cek[f"{kelas}/{model}"] = dict(beda_sel=beda, n_sel=sum(len(v) for v in a.values()))
    assert all(v["beda_sel"] == 0 for v in seed_cek.values()), seed_cek
    log.append("H1p, H1, dan rule identik antara seed 42 dan 13 (0 sel berbeda)")

    # ---- kontrol ML: seed tersambung ----
    ml42 = kontrol_ml_seed(42)
    ml13 = kontrol_ml_seed(13)
    beda_ml = sum(1 for a, b in zip(ml42, ml13) if a["ck_pertama"] != b["ck_pertama"])
    assert beda_ml == len(ml42), (ml42, ml13)
    log.append(f"kontrol ML: {beda_ml} dari {len(ml42)} fold berubah antar seed")

    # ---- ringkasan per kelas dan model ----
    for kelas in ("hyd", "vib", "ssi"):
        ringkasan[kelas] = {}
        for model in ("persistence", "rule_kanal", "stat_cusum", "H1p_rule_dan_persist",
                      "H1p3_rule_persist_stat",
                      "H1_stat_dan_rule", "H1b_stat_atau_rule"):
            sub = [r for r in semua[42][kelas] if r["model"] == model]
            if sub:
                ringkasan[kelas][model] = H.ringkas_records(sub)

    tulis = dict(
        meta=dict(kartu="RND-S6", kelas=list(KELAS), seed=[42, 13],
                  alpha_budget=H.ALPHA_BUDGET, far_maks=H.FAR_MAKS,
                  recall_min=H.RECALL_MIN, grid_h=[float(min(H.H_GRID)), float(max(H.H_GRID))],
                  kanal_hyd="SPPA", durasi_detik=round(time.time() - t0, 1),
                  versi_harness=f"{BASE}/code/rnd_hybrid_harness.py",
                  python=__import__("sys").version.split()[0],
                  pandas=__import__("pandas").__version__,
                  numpy=__import__("numpy").__version__,
                  waktu=time.strftime("%Y-%m-%d %H:%M:%S")),
        reproduksi_r8=reproduksi,
        reproduksi_s2=repro_s2,
        galat_reproduksi_s2=galat_s2,
        seed_cek=seed_cek,
        kontrol_ml=dict(seed42=ml42, seed13=ml13, fold_berubah=beda_ml, n_fold=len(ml42)),
        ringkas=ringkasan,
        records=dict(seed42=semua[42], seed13=semua[13]),
        log=log,
    )
    with open(f"{OUT}/s6_kandidat.json", "w") as fh:
        json.dump(tulis, fh, indent=1)
    for l in log:
        print("  ", l)
    print(f"selesai {tulis['meta']['durasi_detik']} s -> {OUT}/s6_kandidat.json")
    if galat_s2:
        print(f"GALAT reproduksi S2: {len(galat_s2)} sel -> lihat galat_reproduksi_s2")
        raise SystemExit(3)


if __name__ == "__main__":
    main()
