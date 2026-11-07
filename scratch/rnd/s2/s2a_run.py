#!/usr/bin/env python3
"""RND-S2 driver: hybrid statistik+rule dan ML+statistik untuk kelas vib dan ssi.

Modul ini TIDAK menulis harness kedua. Pemuatan data, gerbang rule, CUSUM,
pemilihan h, pelatihan LightGBM, ambang conformal, dan evaluasi fold semuanya
dipanggil dari `code/rnd_hybrid_harness.py` (kartu S1). Driver hanya merakit
komposisi dan menulis artefak.

Keputusan desain yang dikunci:
1. Kanal gerbang dan ambang rule dipilih HANYA dari well latih tiap fold.
2. Kanal pembangkit label (crpm untuk ssi) tidak boleh dipakai sebagai gerbang.
3. Baseline per tugas memakai y_prev_<kelas> dari data, bukan baseline hyd.
4. Fold dengan positif < 30 ditandai tidak dapat diuji dan tidak masuk agregat.
5. Ambang ML disiapkan dua versi: conformal (satuan baris, dari harness) dan
   anggaran kalender (satuan menit kalender well kalibrasi). Versi kalender
   dihitung dengan primitif harness yang sama, dan ambang conformalnya
   di-assert sama dengan keluaran H.skor_ml_fold sebagai bukti komposisi setia.

Keluaran: scratch/rnd/s2/s2_records_<kelas>.json, s2_meta.json
"""
from __future__ import annotations

import json
import os
import sys
import time

import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, roc_auc_score

BASE = "/mnt/d/Capstone 1(v2)"
sys.path.insert(0, f"{BASE}/code")
import rnd_hybrid_harness as H  # noqa: E402

OUT = f"{BASE}/scratch/rnd/s2"
DSD = f"{BASE}/scratch/v9_d1/datasets"
LOWOD = f"{BASE}/scratch/v9_d1"

KELAS = {
    "vib": dict(y="y_vib", prev="y_prev_vib", fold="lowo_vib.json"),
    "ssi": dict(y="y_ssi", prev="y_prev_ssi", fold="lowo_ssi.json"),
}

# Kanal fisik yang boleh jadi gerbang, memakai nama kolom bins (spm, depth, dbtm
# berhuruf kecil di bins). crpm sengaja TIDAK ada karena crpm adalah pembangkit
# label y_ssi (SSI = (maks-min)/(2 x rerata) pada kanal crpm).
KANAL = ["TQA", "SPPA", "TFLO", "RPM", "SWOB", "HKLD", "ROP", "BPOS", "spm", "depth", "dbtm"]
THR_GRID = (1.5, 2.0, 2.5, 3.0)
# Kurva sensitivitas anggaran FAR per 24 jam kalender, di luar anggaran gate 6.
BUDGET_GRID = (12, 24, 48, 96, 192)
MIN_POS_UJI = 30
SEED_UTAMA = 42
SEED_UJI = 13
FAR_MAKS = H.FAR_MAKS


class CacheSinyal:
    """Cache keluaran fungsi harness per (tag dataset, well, kanal[, ambang]).

    Isinya tetap hasil `H.seri_z` dan `H.gerbang_rule`, bukan implementasi tandingan.
    Tag dataset wajib ada di kunci: nama well sama muncul di beberapa dataset
    (F-14 ada di vib dan ssi) dengan jumlah baris berbeda, sehingga kunci tanpa tag
    akan memakai ulang z dari dataset lain dan panjang array tidak cocok.
    """

    def __init__(self, tag):
        self.tag = tag
        self.z = {}
        self.rule = {}
        self.n_panggil_harness = 0

    def seri(self, well, ts, chan):
        k = (self.tag, well, chan)
        if k not in self.z:
            self.z[k] = H.seri_z(well, ts, chan=chan)
            self.n_panggil_harness += 1
        return self.z[k]

    def gerbang(self, well, ts, chan, thr):
        k = (self.tag, well, chan, thr)
        if k not in self.rule:
            self.rule[k] = H.gerbang_rule(well, ts, chan=chan, thr=thr)
            self.n_panggil_harness += 1
        return self.rule[k]


def auc_aman(y, x):
    y = np.asarray(y, int)
    x = np.asarray(x, float)
    m = np.isfinite(x)
    if m.sum() < 50 or len(np.unique(y[m])) < 2:
        return None
    try:
        return float(roc_auc_score(y[m], x[m]))
    except Exception:
        return None


def pilih_kanal_rule(well_df, fold, y_col, cache):
    """Pilih (kanal, ambang) gerbang dari well latih saja.

    Kanal dipilih lewat AUC |z| terhadap label pada baris latih, lalu ambang
    dipilih pada grid dengan F1 baris latih. Well uji tidak pernah dilihat.
    """
    ytr = pd.concat([well_df[w][y_col] for w in fold["train_wells"]]).to_numpy(int)
    skor_kanal = {}
    for ch in KANAL:
        bagian = []
        for w in fold["train_wells"]:
            zv, _ = cache.seri(w, well_df[w]["ts_bin"].to_numpy(int), ch)
            bagian.append(np.abs(zv))
        a = auc_aman(ytr, np.concatenate(bagian))
        if a is not None:
            skor_kanal[ch] = a
    if not skor_kanal:
        return dict(kanal=None, auc=None, thr=None, f1=None,
                    alasan="tidak ada kanal dengan AUC terdefinisi")
    ch = max(skor_kanal, key=skor_kanal.get)
    best = dict(thr=None, f1=-1.0)
    for thr in THR_GRID:
        bag = [cache.gerbang(w, well_df[w]["ts_bin"].to_numpy(int), ch, thr)
               for w in fold["train_wells"]]
        pred = np.concatenate(bag).astype(int)
        tp = int(((pred == 1) & (ytr == 1)).sum())
        fp = int(((pred == 1) & (ytr == 0)).sum())
        fn = int(((pred == 0) & (ytr == 1)).sum())
        f1 = (2 * tp / (2 * tp + fp + fn)) if (2 * tp + fp + fn) else 0.0
        if f1 > best["f1"]:
            best = dict(thr=thr, f1=round(float(f1), 6), tp=tp, fp=fp, fn=fn)
    return dict(kanal=ch, auc=round(float(skor_kanal[ch]), 6), thr=best["thr"],
                f1=best["f1"], tp=best.get("tp"), fp=best.get("fp"), fn=best.get("fn"),
                auc_semua={k: round(v, 6) for k, v in
                           sorted(skor_kanal.items(), key=lambda kv: -kv[1])})


def ambang_kalender(skor_cal, y_cal, ts_cal, budget=H.ALPHA_BUDGET):
    """Ambang skor ML dari anggaran FAR menit kalender well kalibrasi.

    k_maks = lantai(budget x menit_neg_kalender). Ambang diambil pada skor negatif
    ke-k_maks (terurut turun), sehingga laju alarm kalender <= budget.
    """
    y_cal = np.asarray(y_cal, int)
    skor_cal = np.asarray(skor_cal, float)
    ts_cal = np.asarray(ts_cal, int)
    menit_kal = float(ts_cal.max() - ts_cal.min() + 1)
    menit_neg = max(menit_kal - float(y_cal.sum()), 1.0)
    k_maks = int(np.floor(budget * menit_neg))
    neg = np.sort(skor_cal[y_cal == 0])[::-1]
    if len(neg) == 0:
        return dict(ambang=float(np.max(skor_cal)), k_maks=0,
                    menit_neg_kalender=round(menit_neg, 1), neg_baris=0)
    if k_maks >= len(neg):
        amb = float(np.nextafter(neg[-1], -np.inf))
    else:
        amb = float(neg[k_maks])
    return dict(ambang=amb, k_maks=k_maks, menit_neg_kalender=round(menit_neg, 1),
                neg_baris=int(len(neg)))


def wilson(k, n, z=1.959964):
    """Selang Wilson 95 persen untuk proporsi k/n."""
    if n is None or n <= 0:
        return dict(p=None, lo=None, hi=None, n=int(n or 0))
    k = float(k)
    p = k / n
    d = 1 + z * z / n
    pusat = (p + z * z / (2 * n)) / d
    setengah = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return dict(p=round(float(p), 6), lo=round(float(max(0.0, pusat - setengah)), 6),
                hi=round(float(min(1.0, pusat + setengah)), 6), n=int(n))


def evaluasi(nama, pred, y, ts):
    rec = H.evaluasi_fold(y, pred, ts)
    r = rec["rows"]
    rec["model"] = nama
    rec["lolos_far_recall"] = bool(rec["far24_kalender"] <= FAR_MAKS
                                   and (r["recall"] or 0) >= H.RECALL_MIN)
    rec["wilson_recall"] = wilson(r["tp"], r["n_pos"])
    rec["wilson_precision"] = wilson(r["tp"], r["tp"] + r["fp"])
    return rec


def latih_ulang_untuk_kalibrasi(well_df, fold, y_col, feats, seed):
    """Komposisi ulang pemisahan latih/kalibrasi memakai primitif harness.

    Dipakai HANYA untuk mendapat skor well kalibrasi, karena H.skor_ml_fold tidak
    mengembalikan skor kalibrasi. Kesetiaan komposisi dibuktikan dengan assert
    bahwa ambang conformal hasil komposisi ini sama dengan ambang dari harness.
    """
    cal = fold["train_wells"][0]
    tr = [t for t in fold["train_wells"] if t != cal]
    Xtr = pd.concat([well_df[t][feats] for t in tr])
    ytr = pd.concat([well_df[t][y_col] for t in tr]).to_numpy(int)
    m = H.latih_lgb(Xtr, ytr, seed=seed)
    skor_cal = m.predict_proba(well_df[cal][feats])[:, 1]
    y_cal = well_df[cal][y_col].to_numpy(int)
    amb_conformal = H.threshold_conformal(y_cal, skor_cal, H.ALPHA_BUDGET)
    return dict(skor_cal=skor_cal, y_cal=y_cal, cal_well=cal,
                ambang_conformal_komposisi=amb_conformal)


def jalankan_kelas(kelas, cache):
    cfg = KELAS[kelas]
    y_col, prev_col = cfg["y"], cfg["prev"]
    df = H.muat_dataset(f"{DSD}/{kelas}.csv.gz")
    well_df = H.pecah_well(df)
    folds = H.muat_fold(f"{LOWOD}/{cfg['fold']}")
    feats = H.fitur_dari(df)

    out_folds, tak_uji = [], []
    for f in folds:
        w = f["test_well"]
        d = well_df[w]
        y = d[y_col].to_numpy(int)
        ts = d["ts_bin"].to_numpy(int)
        n_pos = int(y.sum())
        dapat = bool(n_pos >= MIN_POS_UJI)
        sel = pilih_kanal_rule(well_df, f, y_col, cache)
        chan, thr = sel["kanal"], sel["thr"]

        models = {}
        # baseline per tugas dari data: persistence y_prev
        models["persistence"] = evaluasi("persistence", d[prev_col].fillna(0).to_numpy(int), y, ts)

        cal0 = f["train_wells"][0]
        # (a) statistik + rule
        if chan is not None:
            sig = H.detektor_stat_rule(w, ts, cal0, well_df[cal0]["ts_bin"].to_numpy(int),
                                       chan=chan, alpha=H.ALPHA_BUDGET)
            rule = cache.gerbang(w, ts, chan, thr)
            models["rule_kanal"] = evaluasi("rule_kanal", rule, y, ts)
            models["stat_cusum"] = evaluasi("stat_cusum", sig["stat"], y, ts)
            models["H1_stat_dan_rule"] = evaluasi("H1_stat_dan_rule",
                                                  ((sig["stat"] == 1) & (rule == 1)).astype(int), y, ts)
            models["H1b_stat_atau_rule"] = evaluasi("H1b_stat_atau_rule",
                                                    ((sig["stat"] == 1) | (rule == 1)).astype(int), y, ts)
            h_terpilih = sig["h"]
        else:
            h_terpilih = None

        # (b) ML + statistik dengan kalibrasi
        ml_meta = []
        for seed, label in ((SEED_UTAMA, "42"), (SEED_UJI, "13")):
            info = H.skor_ml_fold(well_df, f, y_col, feats, seed=seed, alpha=H.ALPHA_BUDGET)
            kk = latih_ulang_untuk_kalibrasi(well_df, f, y_col, feats, seed)
            assert abs(kk["ambang_conformal_komposisi"] - info["ambang"]) < 1e-12, (
                f"komposisi kalibrasi tidak setia pada {kelas}/{w}/seed {seed}: "
                f"{kk['ambang_conformal_komposisi']} lawan {info['ambang']}")
            ak = ambang_kalender(kk["skor_cal"], kk["y_cal"],
                                 well_df[kk["cal_well"]]["ts_bin"].to_numpy(int))
            skor = info["skor"]
            ml_c = (skor >= info["ambang"]).astype(int)
            ml_k = (skor >= ak["ambang"]).astype(int)
            auprc = float(average_precision_score(y, skor)) if len(np.unique(y)) > 1 else None
            auc = auc_aman(y, skor)
            ml_meta.append(dict(seed=seed, ambang_conformal=info["ambang"],
                                ambang_kalender=ak["ambang"], k_maks_kalender=ak["k_maks"],
                                menit_neg_kalender=ak["menit_neg_kalender"],
                                cal_well=info["cal_well"], n_latih=info["n_latih"],
                                n_pos_latih=info["n_pos_latih"],
                                auprc=round(auprc, 6) if auprc is not None else None,
                                auc=round(auc, 6) if auc is not None else None,
                                n_alarm_conformal=int(ml_c.sum()),
                                n_alarm_kalender=int(ml_k.sum())))
            if seed == SEED_UTAMA:
                models["ML_conformal"] = evaluasi("ML_conformal", ml_c, y, ts)
                models["ML_kalender"] = evaluasi("ML_kalender", ml_k, y, ts)
                if chan is not None:
                    models["H2_ML_kalender_dan_stat"] = evaluasi(
                        "H2_ML_kalender_dan_stat", ((ml_k == 1) & (sig["stat"] == 1)).astype(int), y, ts)
                    models["H2b_ML_kalender_atau_stat"] = evaluasi(
                        "H2b_ML_kalender_atau_stat", ((ml_k == 1) | (sig["stat"] == 1)).astype(int), y, ts)
                    models["H3_ML_kalender_dan_rule"] = evaluasi(
                        "H3_ML_kalender_dan_rule", ((ml_k == 1) & (rule == 1)).astype(int), y, ts)
                # kurva sensitivitas anggaran: ambang ML dan h CUSUM diambil ulang
                # pada anggaran lebih longgar, semuanya dari well kalibrasi
                sens = []
                for b in BUDGET_GRID:
                    akb = ambang_kalender(kk["skor_cal"], kk["y_cal"],
                                          well_df[kk["cal_well"]]["ts_bin"].to_numpy(int),
                                          budget=b / 1440.0)
                    mlb = (skor >= akb["ambang"]).astype(int)
                    models[f"ML_kalender_b{b}"] = evaluasi(f"ML_kalender_b{b}", mlb, y, ts)
                    entri = dict(budget=b, ambang_ml=akb["ambang"], n_alarm_ml=int(mlb.sum()),
                                 k_maks=akb["k_maks"])
                    if chan is not None:
                        sigb = H.detektor_stat_rule(w, ts, cal0,
                                                    well_df[cal0]["ts_bin"].to_numpy(int),
                                                    chan=chan, alpha=b / 1440.0)
                        models[f"stat_cusum_b{b}"] = evaluasi(f"stat_cusum_b{b}", sigb["stat"], y, ts)
                        models[f"H1_stat_dan_rule_b{b}"] = evaluasi(
                            f"H1_stat_dan_rule_b{b}",
                            ((sigb["stat"] == 1) & (rule == 1)).astype(int), y, ts)
                        entri["h_cusum"] = sigb["h"]
                        if b == 24:
                            models["H2_ML_kalender_dan_stat_b24"] = evaluasi(
                                "H2_ML_kalender_dan_stat_b24",
                                ((mlb == 1) & (sigb["stat"] == 1)).astype(int), y, ts)
                    sens.append(entri)
                ml_meta[-1]["sensitivitas_anggaran"] = sens
            else:
                models["ML_conformal_seed13"] = evaluasi("ML_conformal_seed13", ml_c, y, ts)

        rec = dict(fold=w, n=int(len(y)), n_pos=n_pos,
                   n_neg=int((y == 0).sum()), prev=round(float(y.mean()), 6),
                   menit_kalender=int(ts.max() - ts.min() + 1),
                   n_well_latih=len(f["train_wells"]), train_wells=f["train_wells"],
                   dapat_diuji=dapat, seleksi=sel, h_terpilih=h_terpilih,
                   ml=ml_meta, models=models)
        out_folds.append(rec)
        if not dapat:
            tak_uji.append(dict(fold=w, n=int(len(y)), n_pos=n_pos, n_neg=int((y == 0).sum()),
                                alasan=f"positif {n_pos} kurang dari {MIN_POS_UJI}"))
        print(f"  [{kelas}] {w}: n={len(y)} pos={n_pos} dapat={dapat} "
              f"kanal={chan} thr={thr} h={h_terpilih}", flush=True)

    hasil = dict(
        kelas=kelas, y_col=y_col, prev_col=prev_col,
        path_dataset=f"{DSD}/{kelas}.csv.gz", path_fold=f"{LOWOD}/{cfg['fold']}",
        n_baris=int(len(df)), n_well=int(df["well"].nunique()),
        wells=sorted(df["well"].unique().tolist()),
        n_fitur=len(feats), fitur=feats,
        min_pos_uji=MIN_POS_UJI, n_fold=len(folds),
        folds=out_folds, tak_dapat_diuji=tak_uji,
        n_fold_dapat_diuji=int(sum(1 for r in out_folds if r["dapat_diuji"])),
    )
    with open(f"{OUT}/s2_records_{kelas}.json", "w") as fh:
        json.dump(hasil, fh, indent=1, default=float)
    print(f"  ditulis {OUT}/s2_records_{kelas}.json", flush=True)
    return hasil


def main():
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    meta = dict(mulai=time.strftime("%Y-%m-%d %H:%M:%S"), kanal=KANAL, thr_grid=list(THR_GRID),
                budget_grid=list(BUDGET_GRID),
                min_pos_uji=MIN_POS_UJI, seed_utama=SEED_UTAMA, seed_uji=SEED_UJI,
                alpha_budget=H.ALPHA_BUDGET, far_maks=FAR_MAKS,
                versi_harness=f"{BASE}/code/rnd_hybrid_harness.py")
    total_panggil = 0
    for kelas in ("vib", "ssi"):
        print(f"== kelas {kelas}", flush=True)
        cache = CacheSinyal(kelas)
        jalankan_kelas(kelas, cache)
        total_panggil += cache.n_panggil_harness
        print(f"   panggilan sinyal harness untuk {kelas}: {cache.n_panggil_harness}", flush=True)
    meta["panggil_harness_sinyal"] = total_panggil
    meta["durasi_detik"] = round(time.time() - t0, 1)
    meta["selesai"] = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(f"{OUT}/s2_meta.json", "w") as fh:
        json.dump(meta, fh, indent=1)
    print(f"selesai dalam {meta['durasi_detik']} s, "
          f"{total_panggil} panggilan sinyal harness", flush=True)


if __name__ == "__main__":
    main()
