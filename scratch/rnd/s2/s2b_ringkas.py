#!/usr/bin/env python3
"""Agregasi S2: ringkasan per model per kelas, perbandingan hybrid lawan single engine.

Aturan agregasi yang dikunci sebelum melihat hasil:
1. Hanya fold dengan dapat_diuji = True yang masuk agregat.
2. "Single engine" = persistence, rule_kanal, stat_cusum, ML_conformal, ML_kalender.
   "Hybrid" = H1_stat_dan_rule, H1b_stat_atau_rule, H2_ML_kalender_dan_stat,
   H2b_ML_kalender_atau_stat, H3_ML_kalender_dan_rule.
3. Single engine terbaik dipilih dengan urutan: (a) jumlah fold yang lolos
   FAR <= 6 per 24 jam kalender DAN recall >= 0,50, (b) recall median lebih besar,
   (c) FAR median lebih kecil, (d) presisi median lebih besar.
   Urutan ini ditetapkan di kode, bukan dipilih setelah melihat angka.
"""
import json
import re
import statistics as st

BASE = "/mnt/d/Capstone 1(v2)"
OUT = f"{BASE}/scratch/rnd/s2"

SINGLE = ["persistence", "rule_kanal", "stat_cusum", "ML_conformal", "ML_kalender"]
HYBRID = ["H1_stat_dan_rule", "H1b_stat_atau_rule", "H2_ML_kalender_dan_stat",
          "H2b_ML_kalender_atau_stat", "H3_ML_kalender_dan_rule"]
FAR_MAKS = 6.0
RECALL_MIN = 0.50


def med(xs):
    v = [x for x in xs if x is not None]
    return round(float(st.median(v)), 6) if v else None


def mn(xs):
    v = [x for x in xs if x is not None]
    return round(float(min(v)), 6) if v else None


def mx(xs):
    v = [x for x in xs if x is not None]
    return round(float(max(v)), 6) if v else None


def agregat(folds, model):
    recs = [f["models"][model] for f in folds if model in f["models"]]
    if not recs:
        return dict(n_fold=0)
    prec = [r["rows"]["precision"] for r in recs]
    recl = [r["rows"]["recall"] for r in recs]
    far = [r["far24_kalender"] for r in recs]
    far_b = [r["far24_baris"] for r in recs]
    return dict(
        n_fold=len(recs),
        fp_total=int(sum(r["rows"]["fp"] for r in recs)),
        tp_total=int(sum(r["rows"]["tp"] for r in recs)),
        fn_total=int(sum(r["rows"]["fn"] for r in recs)),
        n_pos_total=int(sum(r["rows"]["n_pos"] for r in recs)),
        precision_median=med(prec), precision_min=mn(prec), precision_maks=mx(prec),
        recall_median=med(recl), recall_min=mn(recl), recall_maks=mx(recl),
        recall_gabungan=round(sum(r["rows"]["tp"] for r in recs) /
                              max(1, sum(r["rows"]["n_pos"] for r in recs)), 6),
        far24_kalender_median=med(far), far24_kalender_min=mn(far), far24_kalender_maks=mx(far),
        far24_baris_median=med(far_b), far24_baris_min=mn(far_b), far24_baris_maks=mx(far_b),
        cakupan_median=med([r["cakupan"] for r in recs]),
        lead_median=med([r["lead"]["lead_median_min"] for r in recs]),
        n_onset=int(sum(r["lead"]["n_onset"] for r in recs)),
        n_diperingatkan=int(sum(r["lead"]["n_diperingatkan"] for r in recs)),
        fold_far_le6=int(sum(1 for v in far if v is not None and v <= FAR_MAKS)),
        fold_recall_ge50=int(sum(1 for v in recl if v is not None and v >= RECALL_MIN)),
        fold_gate_A_baru=int(sum(1 for r in recs if r["gate_A_baru"])),
        fold_lolos_far_recall=int(sum(1 for r in recs if r["lolos_far_recall"])),
    )


def urut_single(agg):
    """Kunci peringkat single engine, sesuai aturan yang dideklarasikan di docstring."""
    return (
        -agg.get("fold_lolos_far_recall", 0),
        -(agg.get("recall_median") or 0.0),
        (agg.get("far24_kalender_median") if agg.get("far24_kalender_median") is not None else 1e18),
        -(agg.get("precision_median") or 0.0),
    )


def lapisan_c(folds, model):
    """Ketahanan: separuh waktu dan variasi seed."""
    awal, akhir = [], []
    for f in folds:
        r = f["models"].get(model, {}).get("separuh", {})
        if "awal" in r and r["awal"]["recall"] is not None:
            awal.append(r["awal"]["recall"])
        if "akhir" in r and r["akhir"]["recall"] is not None:
            akhir.append(r["akhir"]["recall"])
    turun = sum(1 for a, b in zip(awal, akhir) if b < a)
    return dict(recall_awal_median=med(awal), recall_akhir_median=med(akhir),
                n_fold_banding=min(len(awal), len(akhir)), n_fold_menurun=turun)


def main():
    ringkas = {}
    for kelas in ("vib", "ssi"):
        d = json.load(open(f"{OUT}/s2_records_{kelas}.json"))
        folds = [f for f in d["folds"] if f["dapat_diuji"]]
        semua_model = sorted({m for f in folds for m in f["models"]})
        agg = {m: agregat(folds, m) for m in semua_model}
        urut = sorted(SINGLE, key=lambda m: urut_single(agg[m]))
        terbaik = urut[0] if urut else None
        hybrid_ada = [m for m in HYBRID if agg.get(m, {}).get("n_fold", 0) > 0]
        urut_h = sorted(hybrid_ada, key=lambda m: urut_single(agg[m]))
        terbaik_h = urut_h[0] if urut_h else None

        banding = None
        if terbaik and terbaik_h:
            a, b = agg[terbaik], agg[terbaik_h]
            banding = dict(
                single=terbaik, hybrid=terbaik_h,
                delta_recall_median=round((b["recall_median"] or 0) - (a["recall_median"] or 0), 6),
                delta_precision_median=round((b["precision_median"] or 0) - (a["precision_median"] or 0), 6),
                rasio_far_median=(round(b["far24_kalender_median"] / a["far24_kalender_median"], 6)
                                  if a["far24_kalender_median"] else None),
                delta_fold_lolos=b["fold_lolos_far_recall"] - a["fold_lolos_far_recall"],
            )

        # variasi seed pada komponen ML
        seed_banding = []
        for f in folds:
            m42 = f["models"].get("ML_conformal")
            m13 = f["models"].get("ML_conformal_seed13")
            if m42 and m13:
                seed_banding.append(dict(
                    fold=f["fold"],
                    delta_fp=int(m13["rows"]["fp"] - m42["rows"]["fp"]),
                    delta_tp=int(m13["rows"]["tp"] - m42["rows"]["tp"]),
                    delta_recall=round((m13["rows"]["recall"] or 0) - (m42["rows"]["recall"] or 0), 6),
                ))

        ringkas[kelas] = dict(
            n_fold_total=d["n_fold"], n_fold_dapat_diuji=len(folds),
            n_fold_tidak_dapat_diuji=len(d["tak_dapat_diuji"]),
            tak_dapat_diuji=d["tak_dapat_diuji"],
            n_baris=d["n_baris"], n_well=d["n_well"], n_fitur=d["n_fitur"],
            n_pos_total_dapat_diuji=int(sum(f["n_pos"] for f in folds)),
            sensitivitas={m: agregat(folds, m) for m in semua_model
                          if re.search(r"_b\d+$", m)},
            wells=[dict(fold=f["fold"], n=f["n"], n_pos=f["n_pos"], n_neg=f["n_neg"],
                        menit_kalender=f["menit_kalender"],
                        n_well_latih=f["n_well_latih"],
                        kanal=f["seleksi"]["kanal"], auc_kanal=f["seleksi"]["auc"],
                        thr_rule=f["seleksi"]["thr"], f1_latih=f["seleksi"]["f1"],
                        h_cusum=f["h_terpilih"],
                        auprc_ml=f["ml"][0]["auprc"], auc_ml=f["ml"][0]["auc"],
                        ambang_conformal=f["ml"][0]["ambang_conformal"],
                        ambang_kalender=f["ml"][0]["ambang_kalender"],
                        n_alarm_ml_conformal=f["ml"][0]["n_alarm_conformal"],
                        n_alarm_ml_kalender=f["ml"][0]["n_alarm_kalender"],
                        dapat_diuji=f["dapat_diuji"]) for f in d["folds"]],
            agregat=agg, peringkat_single=urut, single_terbaik=terbaik,
            peringkat_hybrid=urut_h, hybrid_terbaik=terbaik_h,
            banding_hybrid_lawan_single=banding,
            lapisan_c_separuh={m: lapisan_c(folds, m) for m in semua_model},
            variasi_seed_ml=seed_banding,
        )
        print(f"== {kelas}: fold uji {len(folds)}/{d['n_fold']}, "
              f"single terbaik {terbaik}, hybrid terbaik {terbaik_h}", flush=True)
        for m in semua_model:
            a = agg[m]
            print(f"   {m:32s} rec_med={a['recall_median']} prec_med={a['precision_median']} "
                  f"far_med={a['far24_kalender_median']} lolos={a['fold_lolos_far_recall']}/{a['n_fold']}",
                  flush=True)

    # justifikasi ambang 30 positif dengan lebar selang Wilson
    from_uji = []
    for n_pos in (3, 12, 30, 31, 55, 75, 83, 102, 161):
        from_uji.append(dict(n_pos=n_pos, wilson_recall_0=wilson(0, n_pos),
                             wilson_recall_penuh=wilson(n_pos, n_pos),
                             lebar_penuh=round(wilson(n_pos, n_pos)["hi"] - wilson(n_pos, n_pos)["lo"], 6)))
    ringkas["justifikasi_ambang_positif"] = from_uji
    with open(f"{OUT}/s2_ringkas.json", "w") as fh:
        json.dump(ringkas, fh, indent=1, default=float)
    print("ditulis:", f"{OUT}/s2_ringkas.json", flush=True)


def wilson(k, n, z=1.959964):
    if n <= 0:
        return dict(p=None, lo=None, hi=None, n=n)
    p = k / n
    d = 1 + z * z / n
    pusat = (p + z * z / (2 * n)) / d
    setengah = z * (p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5 / d
    return dict(p=round(float(p), 6), lo=round(float(max(0.0, pusat - setengah)), 6),
                hi=round(float(min(1.0, pusat + setengah)), 6), n=int(n))


if __name__ == "__main__":
    main()
