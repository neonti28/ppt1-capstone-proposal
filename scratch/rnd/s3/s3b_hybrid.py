#!/usr/bin/env python3
"""S3b: uji hybrid untuk bit_wear K-1 pada USROP, memakai harness S1.

Bentuk yang diuji
-----------------
H5  statistik DAN rule   : CUSUM residual SPP DAN gerbang |z| torsi (keduanya kausal)
H6  ML DAN statistik     : skor ML kanal fisik (conformal) DAN CUSUM residual SPP
Pembanding
rule_kanal               : gerbang |z| torsi saja
stat_cusum               : CUSUM residual SPP saja
rule_label               : label itu sendiri (batas atas sirkular, bukan model)
ml_dengan_MSE            : ML yang memakai MSE dan ROC_coef sebagai fitur (diagnostik
                           sirkularitas, bukan kandidat)

Aturan
------
1. Fitur kanal fisik tidak memuat MSE, D_exp, ROC_coef, karena ketiga kolom itu
   yang mendefinisikan label.
2. z dihitung kausal: median dan MAD dari jendela LALU (shift 1), bukan dari
   seluruh deret.
3. Ambang CUSUM h dan ambang conformal dipilih pada well kalibrasi di dalam
   train_wells, bukan pada well uji.
4. FAR dilaporkan pada dua satuan: menit kalender (dari est_timestamp, turunan
   interpolasi) dan per 1000 sampel kedalaman. Satuan baris mentah tidak dipakai
   sebagai FAR karena gridnya kedalaman (temuan E0 S-6).
"""
from __future__ import annotations

import json
import os
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, "/mnt/d/Capstone 1(v2)/code")
import rnd_hybrid_harness as H  # noqa: E402

BASE = "/mnt/d/Capstone 1(v2)"
USROP = f"{BASE}/data/USROP_labeled.csv"
TSUROP = f"{BASE}/data/volve/usrop_timestamped.csv"
OUTD = f"{BASE}/scratch/rnd/s3"
OUT = f"{OUTD}/s3b_hybrid.json"

PHYS = ["Weight on Bit kkgf", "Average Standpipe Pressure kPa",
        "Average Surface Torque kN.m", "Rate of Penetration m/h",
        "Average Rotary Speed rpm", "Mud Flow In L/min", "Average Hookload kkgf"]
TERLARANG = ["MSE", "D_exp", "ROC_coef"]
CHAN_RULE = "Average Surface Torque kN.m"
CHAN_STAT = "Average Standpipe Pressure kPa"
THR_RULE = 2.0
W_ALARM = 10          # sampel kedalaman
WIN_Z = 500           # sampel lookback untuk median/MAD
MIN_Z = 100
SEED = 42


def z_kausal(s, win=WIN_Z, minp=MIN_Z):
    """Robust z kausal: median/MAD dari jendela masa lalu, digeser satu sampel."""
    s = pd.Series(np.asarray(s, float))
    med = s.rolling(win, min_periods=minp).median().shift(1)
    mad = (s - med).abs().rolling(win, min_periods=minp).median().shift(1)
    z = (s - med) / (1.4826 * mad.replace(0, np.nan))
    return np.nan_to_num(z.to_numpy(float), nan=0.0)


def far_menit_kalender(ts_menit, y, pred):
    """FAR per 24 jam pada satuan menit kalender.

    Definisi yang dipakai: alarm palsu per 24 jam OPERASI, yaitu menit alarm
    yang tidak mengandung baris positif dibagi menit berdata.

    Alasan definisi ini, bukan menit negatif sebagai penyebut: label K-1 hanya
    25 persen baris dan tersebar, sehingga menit yang mengandung sedikitnya satu
    baris positif bisa hampir seluruh menit (pada satu well menyisakan satu
    menit negatif). Penyebut menit negatif karena itu runtuh dan menghasilkan
    angka ribuan yang bukan laju. Menit negatif tetap dilaporkan supaya
    pembaca bisa memeriksa.
    """
    ts_menit = np.asarray(ts_menit, float)
    y = np.asarray(y).astype(int)
    pred = np.asarray(pred).astype(int)
    ok = np.isfinite(ts_menit)
    menit = np.unique(np.floor(ts_menit[ok]).astype(np.int64))
    menit_pos = np.unique(np.floor(ts_menit[ok & (y == 1)]).astype(np.int64))
    menit_alarm = np.unique(np.floor(ts_menit[ok & (pred == 1)]).astype(np.int64))
    alarm_neg = np.setdiff1d(menit_alarm, menit_pos)
    menit_neg = np.setdiff1d(menit, menit_pos)
    span = float(menit.max() - menit.min() + 1) if len(menit) else 0.0
    jam_operasi = len(menit) / 60.0
    return dict(
        menit_berdata=int(len(menit)), menit_pos=int(len(menit_pos)),
        menit_neg=int(len(menit_neg)), menit_alarm=int(len(menit_alarm)),
        menit_alarm_neg=int(len(alarm_neg)),
        rentang_menit=round(span, 1),
        jam_operasi=round(jam_operasi, 3),
        cakupan_menit=round(len(menit) / span, 4) if span else None,
        far24_kalender=round(len(alarm_neg) / (jam_operasi / 24.0), 4) if jam_operasi else None,
    )


def main():
    t0 = time.time()
    log = []
    H.log("muat USROP", log)
    d = pd.read_csv(USROP)
    d["y"] = (d["label"] == "high_MSE_bit_wear").astype(int)

    t = pd.read_csv(TSUROP)
    assert len(t) == len(d), f"panjang beda {len(t)} vs {len(d)}"
    if "well" in t.columns:
        assert (t["well"].to_numpy() == d["well"].to_numpy()).all(), "urutan well tidak sejajar"
    d["ts"] = pd.to_datetime(t["est_timestamp"], errors="coerce", utc=True)
    # PENTING: pandas 3 menyimpan datetime pada resolusi mikrodetik
    # (dtype datetime64[us, UTC]), sehingga astype("int64") memberi mikrodetik
    # dan astype("datetime64[ns]") pada seri bertz melempar TypeError. Konversi
    # lewat total_seconds supaya satuan menit benar, bukan terkompresi 1000 kali.
    d["ts_menit"] = (
        d["ts"] - pd.Timestamp("1970-01-01", tz="UTC")
    ).dt.total_seconds() / 60.0
    d.loc[d["ts"].isna(), "ts_menit"] = np.nan
    H.log(f"sejajar: {len(d)} baris, ts kosong {int(d['ts_menit'].isna().sum())}", log)

    wells = sorted(d["well"].unique())
    per_well = {}
    for w in wells:
        g = d[d["well"] == w].sort_values("Measured Depth m").reset_index(drop=True)
        per_well[w] = g

    # statistik per well untuk laporan
    well_info = {}
    for w, g in per_well.items():
        jam = (np.nanmax(g["ts_menit"]) - np.nanmin(g["ts_menit"])) / 60.0
        well_info[w] = dict(
            baris=int(len(g)), pos=int(g["y"].sum()),
            prevalensi=round(float(g["y"].mean()), 6),
            rentang_jam=round(float(jam), 3),
            baris_per_jam=round(float(len(g) / jam), 2) if jam > 0 else None,
            md_min=round(float(g["Measured Depth m"].min()), 3),
            md_maks=round(float(g["Measured Depth m"].max()), 3),
        )

    # fold LOWO: well uji = w, kalibrasi = train_wells[0]
    folds = []
    for i, w in enumerate(wells):
        train = [x for x in wells if x != w]
        folds.append({"test_well": w, "train_wells": train})

    # pra-hitung z kausal per well
    zc = {}
    for w, g in per_well.items():
        zc[w] = {c: z_kausal(g[c].to_numpy(float)) for c in PHYS}

    records = []
    fold_meta = []
    for fold in folds:
        w = fold["test_well"]
        cal = fold["train_wells"][0]
        g = per_well[w]
        y = g["y"].to_numpy(int)
        ts = g["ts_menit"].to_numpy(float)

        # --- sinyal rule dan statistik
        zr = zc[w][CHAN_RULE]
        rule = ((np.abs(np.concatenate([[0.0], zr[:-1]])) > THR_RULE)).astype(int)
        h = H.pilih_h(zc[cal][CHAN_STAT], budget=H.ALPHA_BUDGET)
        stat_raw = H.cusum_alarm(zc[w][CHAN_STAT], h)
        stat = H.jendela_alarm(stat_raw, W_ALARM)
        h5 = ((stat == 1) & (rule == 1)).astype(int)
        laju_stat = dict(
            h=h, saturasi=bool(h >= H.H_GRID[-1]),
            frac_raw=round(float(stat_raw.mean()), 6),
            frac_jendela=round(float(stat.mean()), 6),
            anggaran=round(float(H.ALPHA_BUDGET), 6),
        )

        # --- ML kanal fisik (tanpa MSE/ROC) dan ML dengan MSE (diagnostik)
        feats = PHYS
        feats_mse = PHYS + TERLARANG
        tr = [x for x in fold["train_wells"] if x != cal]
        Xtr = pd.concat([per_well[x][feats] for x in tr])
        ytr = pd.concat([per_well[x]["y"] for x in tr]).to_numpy(int)
        m = H.latih_lgb(Xtr, ytr, seed=SEED)
        skor_cal = m.predict_proba(per_well[cal][feats])[:, 1]
        amb = H.threshold_conformal(per_well[cal]["y"].to_numpy(int), skor_cal, H.ALPHA_BUDGET)
        skor = m.predict_proba(g[feats])[:, 1]
        ml = (skor >= amb).astype(int)
        h6 = ((ml == 1) & (stat == 1)).astype(int)

        Xtr2 = pd.concat([per_well[x][feats_mse] for x in tr])
        m2 = H.latih_lgb(Xtr2, ytr, seed=SEED)
        skor_cal2 = m2.predict_proba(per_well[cal][feats_mse])[:, 1]
        amb2 = H.threshold_conformal(per_well[cal]["y"].to_numpy(int), skor_cal2, H.ALPHA_BUDGET)
        ml_mse = (m2.predict_proba(g[feats_mse])[:, 1] >= amb2).astype(int)

        for nama, pred in (("rule_label", y.copy()), ("rule_kanal", rule),
                           ("stat_cusum", stat), ("H5_stat_dan_rule", h5),
                           ("ml_fisik", ml), ("H6_ml_dan_stat", h6),
                           ("ml_dengan_MSE", ml_mse)):
            r = H.rows_metrics(y, pred)
            ev = H.event_metrics(y, pred)
            far = far_menit_kalender(ts, y, pred)
            lead = H.lead_time(y, pred, horizon=60)
            rec = dict(
                fold=w, model=nama, n=len(y), n_pos=int(y.sum()),
                rows=r, events=ev, far=far,
                far24_kalender=far["far24_kalender"],
                far24_baris=None,
                far_per_1000_sampel=round(r["fp"] / max(len(y) - r["n_pos"], 1) * 1000.0, 3),
                garwood_atas_fp=H.garwood_atas(r["fp"], max(far["menit_neg"], 1)),
                lead=lead, separuh=H.separuh(np.arange(len(y)), y, pred),
                h_terpilih=h, ambang_conformal=round(float(amb), 6),
                cakupan=far["cakupan_menit"],
                gate_A_baru=bool(
                    far["far24_kalender"] is not None
                    and far["far24_kalender"] <= H.FAR_MAKS
                    and (far["cakupan_menit"] or 0) >= H.CAKUPAN_MIN
                    and (r["recall"] or 0) >= H.RECALL_MIN
                ),
            )
            records.append(rec)

        fold_meta.append(dict(
            fold=w, cal_well=cal, h=h, ambang_conformal=round(float(amb), 6),
            n_latih=int(len(Xtr)), n_pos_latih=int(ytr.sum()),
            prevalensi_uji=round(float(y.mean()), 6),
            laju_stat=laju_stat,
            recall_rule=records[-6]["rows"]["recall"],
            recall_ml=records[-3]["rows"]["recall"],
            recall_ml_mse=records[-1]["rows"]["recall"],
        ))
        H.log(f"fold {w} selesai h={h} amb={amb:.4f}", log)

    # ringkas_records dari harness tidak menerima FAR tak terdefinisi (menit_neg = 0).
    # Salinan untuk harness mengisi FAR tak terdefinisi dengan 1e9 supaya dihitung
    # GAGAL gate, bukan lolos diam-diam. Nilai asli tetap None di records.
    import copy
    rec_h = copy.deepcopy(records)
    n_takdef = 0
    for r in rec_h:
        if r["far24_kalender"] is None:
            r["far24_kalender"] = 1e9
            n_takdef += 1
    ringkas = {m: H.ringkas_records(rec_h, m) for m in
               ("rule_label", "rule_kanal", "stat_cusum", "H5_stat_dan_rule",
                "ml_fisik", "H6_ml_dan_stat", "ml_dengan_MSE")}
    takdef_per_model = {}
    for m in ringkas:
        takdef_per_model[m] = int(sum(1 for r in records
                                      if r["model"] == m and r["far24_kalender"] is None))

    out = dict(
        meta=dict(
            sumber=USROP, waktu=TSUROP, seed=SEED, durasi_detik=round(time.time() - t0, 1),
            kanal_rule=CHAN_RULE, kanal_stat=CHAN_STAT, thr_rule=THR_RULE,
            w_alarm=W_ALARM, win_z=WIN_Z, alpha=H.ALPHA_BUDGET,
            fitur_fisik=PHYS, fitur_terlarang=TERLARANG,
            catatan=("ambang h dan conformal dipilih pada well kalibrasi; label tidak "
                     "dipakai untuk membentuk z, rule, atau statistik"),
        ),
        well_info=well_info, folds=fold_meta, records=records, ringkas=ringkas,
        far_tak_terdefinisi=dict(n_rekaman=n_takdef, per_model=takdef_per_model,
                                 arti="menit_neg = 0 sehingga penyebut FAR tidak ada; dihitung gagal gate"),
        log=log,
    )
    H.tulis_json(OUT, out)

    print(json.dumps(ringkas, indent=1))
    print("durasi", out["meta"]["durasi_detik"], "s")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
