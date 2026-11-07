#!/usr/bin/env python3
"""RND-E4 — definisi TUNGGAL baseline rule t0-1 (perbaikan R7-1).

Dipakai bersama oleh E0, E4, dan skrip review supaya tidak ada lagi proksi
"label baris sebelumnya" yang menintip masa depan.

Resep label diambil apa adanya dari code/v9_d1_03_rig_datasets.py:55-75:
  qcut(TFLO_mean, 10) -> median/MAD per bin -> |z| > 2  => anom per menit.
Sinyal rule pada titik keputusan t HANYA memakai anom di bin (t-1), seluruhnya
masa lalu. Tidak ada nilai pada t atau setelah t yang dipakai.
"""
import numpy as np
import pandas as pd

BINSD = "/mnt/d/Capstone 1(v2)/scratch/v9_d1/bins"
W = 10  # panjang jendela label (menit)


def bin_table(well, binsd=BINSD):
    """Tabel per menit: ts_bin, obs (kanal teramati), anom (|z| > 2)."""
    b = pd.read_csv(f"{binsd}/{well}.csv.gz")
    d = b.dropna(subset=["SPPA_mean", "TFLO_mean"]).copy()
    d = d[d["TFLO_mean"] > 0]
    anom = pd.Series(False, index=b.index)
    if len(d) >= 50:
        try:
            d["qbin"] = pd.qcut(d["TFLO_mean"], 10, labels=False, duplicates="drop")
        except ValueError:
            d["qbin"] = 0
        med = d.groupby("qbin")["SPPA_mean"].transform("median")
        mad = d.groupby("qbin")["SPPA_mean"].transform(lambda s: (s - s.median()).abs().median())
        z = (d["SPPA_mean"] - med) / (1.4826 * mad.replace(0, np.nan))
        anom.loc[d.index] = (z.abs() > 2).fillna(False)
    out = pd.DataFrame({
        "ts_bin": b["ts_bin"],
        "obs": b["SPPA_mean"].notna() & b["TFLO_mean"].notna(),
        "anom": anom.values,
    })
    return out.set_index("ts_bin")


def rule_t0m1(well, ts, binsd=BINSD):
    """Sinyal rule kausal: anom pada bin (t-1) dari tabel bins well yang sama."""
    B = bin_table(well, binsd=binsd)
    prev = B.reindex(np.asarray(ts, dtype=int) - 1)
    a = prev["anom"].fillna(False).to_numpy().astype(bool)
    o = prev["obs"].fillna(False).to_numpy().astype(bool)
    return (a & o).astype(int)


def hybrid_rule_persistence(well, ts, y_prev, valid_prev, binsd=BINSD):
    """Baseline hybrid terbit: rule t0-1 DAN persistence (y_prev jendela [t-10, t))."""
    rule = rule_t0m1(well, ts, binsd=binsd)
    pers = np.where(np.asarray(valid_prev).astype(int) == 1,
                    np.asarray(y_prev).astype(int), 0)
    return (rule & pers).astype(int), rule, pers


def assert_published(total_rule_fp, total_hybrid_fp, tol=0.05):
    """R7-1 kriteria selesai: FP rule 2.091 dan FP hybrid 927, toleransi 5 persen."""
    ok_rule = abs(total_rule_fp - 2091) <= tol * 2091
    ok_hyb = abs(total_hybrid_fp - 927) <= tol * 927
    assert ok_rule, f"FP rule {total_rule_fp} di luar 2091 +-5%"
    assert ok_hyb, f"FP hybrid {total_hybrid_fp} di luar 927 +-5%"
    return dict(fp_rule=total_rule_fp, fp_hybrid=total_hybrid_fp,
                fp_rule_terbit=2091, fp_hybrid_terbit=927,
                selisih_rule_pct=round(100 * (total_rule_fp - 2091) / 2091, 3),
                selisih_hybrid_pct=round(100 * (total_hybrid_fp - 927) / 927, 3),
                toleransi_pct=100 * tol, lulus=True)
