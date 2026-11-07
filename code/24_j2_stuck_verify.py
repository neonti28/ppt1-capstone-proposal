#!/usr/bin/env python3
"""Verifier independen J2 — menghitung ulang klaim kunci dari primer + prediksi tersimpan.

Periksa:
 (a) label counts & prevalence dari CSV window (primer)
 (b) PR-AUC/prev dari file prediksi JSON (bukan dari JSON hasil kampanye)
 (c) tidak ada fitur masa depan: rolling hanya memakai 10 bin terakhir (inspeksi kode
     diverifikasi struktural: add_features pakai .rolling tanpa shift negatif — di sini
     diuji numerik: feature baris i harus identik saat data sesudah i dipotong)
 (d) determinisme: re-fit logreg E1 F-9_A -> prob identik dgn prediksi tersimpan
"""
import json
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score

SEED = 20261010
DATA = "/mnt/d/Capstone 1/data/predictive/j2_stuck"
CH_MAIN = ["SPPA", "TQA", "TFLO", "HKLD", "SWOB", "RPM", "ROP", "BPOS"]  # = CH9 kampanye
CHECKS = []


def check(name, ok, detail):
    CHECKS.append({"check": name, "pass": bool(ok), "detail": detail})
    print(("PASS " if ok else "FAIL ") + name + " :: " + str(detail))


def load_bins(well, channels):
    df = pd.read_csv(f"{DATA}/{well}_window.csv", dtype={"STUCK_RT": "float64"})
    df["ts"] = pd.to_datetime(df["timestamp"], format="ISO8601", utc=True)
    if "RPM" not in df.columns and "NRPM_RT" in df.columns:
        df = df.rename(columns={"NRPM_RT": "RPM"})
    for c in channels:
        df[c] = pd.to_numeric(df[c], errors="coerce") if c in df.columns else np.nan
    df = df.sort_values("ts").set_index("ts")
    bins = df[channels].resample("30s").median()
    lab = df["STUCK_RT"].dropna().resample("30s").agg(
        lambda s: s.mode().iloc[0] if len(s.mode()) else np.nan)
    cnt = df["STUCK_RT"].dropna().resample("30s").count()
    bins["code"] = lab
    bins["n_labeled"] = cnt
    for c in channels:
        bins[f"{c}_m"] = bins[c].rolling(10, min_periods=3).mean()
        bins[f"{c}_s"] = bins[c].rolling(10, min_periods=3).std()
    return bins.reset_index()


def main():
    res = json.load(open("/mnt/d/Capstone 1/docs/V5_J2_STUCK.json"))
    preds = json.load(open(f"{DATA}/j2_predictions.json"))

    # (a) label counts primer
    for well, exp in [("F-9_A", 45712), ("F-9", 5728), ("F-14", 5147)]:
        df = pd.read_csv(f"{DATA}/{well}_window.csv", usecols=["STUCK_RT"])
        n = int(df["STUCK_RT"].notna().sum())
        check(f"label_count_{well}", n == exp, f"n_labeled={n} expected={exp}")

    # (b) recompute PR-AUC dari prediksi tersimpan
    for key, entry in [("E1_F-9_A_logreg", res["E1"]["A"]["F-9_A"]["logreg"]),
                       ("E1_F-14_logreg", res["E1"]["A"]["F-14"]["logreg"]),
                       ("E1B_F-9_A_logreg", res["E1"]["B"]["F-9_A"]["logreg"])]:
        if key not in preds:
            check(f"pred_store_{key}", False, "missing")
            continue
        y = np.array(preds[key]["y"]); p = np.array(preds[key]["p"])
        ap = float(average_precision_score(y, p))
        ok = abs(ap - entry["pr_auc"]) < 1e-9
        check(f"prauc_recompute_{key}", ok, f"recomputed={ap:.9f} reported={entry['pr_auc']:.9f}")

    # G1 pooled recompute
    py, pp = [], []
    for w in ["F-9_A", "F-9", "F-14"]:
        k = f"E1_{w}_logreg"
        if k in preds:
            py.extend(preds[k]["y"]); pp.extend(preds[k]["p"])
    ap_pool = float(average_precision_score(np.array(py), np.array(pp)))
    g1 = res["GATES"]["G1"]
    ok = abs(ap_pool - g1["pooled_logreg_pr_auc"]) < 1e-9
    check("g1_pooled_recompute", ok,
          f"recomputed={ap_pool:.9f} reported={g1['pooled_logreg_pr_auc']:.9f}")
    prev = float(np.mean(py))
    g1_logic = (ap_pool >= prev + 0.15) and (g1["bootstrap_ci"]["ci_lo"] > prev)
    check("g1_gate_logic", g1_logic == g1["pass"],
          f"ap={ap_pool:.4f} prev={prev:.4f} ci_lo={g1['bootstrap_ci']['ci_lo']:.4f} pass={g1_logic}")

    # (c) no-future-feature test numerik: potong pada BATAS BIN (30s) agar tidak
    # ada bin yang setengah terisi; bandingkan fitur semua bin sebelum potongan.
    bins_full = load_bins("F-9_A", CH_MAIN)
    cols = [f"{c}_m" for c in CH_MAIN] + [f"{c}_s" for c in CH_MAIN]  # urutan sama dgn kampanye
    df = pd.read_csv(f"{DATA}/F-9_A_window.csv", dtype={"STUCK_RT": "float64"})
    df["ts"] = pd.to_datetime(df["timestamp"], format="ISO8601", utc=True)
    df = df.sort_values("ts")
    # batas potong = awal bin, 300 bin dari akhir
    t_cut = bins_full["ts"].iloc[-300]
    df_trunc = df[df["ts"] < t_cut]
    import tempfile
    tmpd = tempfile.mkdtemp()
    df_trunc.to_csv(f"{tmpd}/trunc.csv", index=False)
    dft = pd.read_csv(f"{tmpd}/trunc.csv", dtype={"STUCK_RT": "float64"})
    dft["ts"] = pd.to_datetime(dft["timestamp"], format="ISO8601", utc=True)
    dft = dft.sort_values("ts").set_index("ts")
    bins_trunc = dft[CH_MAIN].resample("30s").median()
    for c in CH_MAIN:
        bins_trunc[f"{c}_m"] = bins_trunc[c].rolling(10, min_periods=3).mean()
        bins_trunc[f"{c}_s"] = bins_trunc[c].rolling(10, min_periods=3).std()
    common = bins_full.set_index("ts").index.intersection(bins_trunc.index)
    a = bins_full.set_index("ts").loc[common, cols]
    b = bins_trunc.loc[common, cols]
    both_nan = a.isna() & b.isna()
    delta = (a - b).abs()
    delta[both_nan] = 0.0
    diff = np.nanmax(delta.values)
    check("no_future_features", diff < 1e-9,
          f"max|diff| pada {len(common)} bin sebelum potongan bin di -300 = {diff}")

    # (d) determinisme: re-fit logreg E1 F-9_A
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LogisticRegression
    b = load_bins("F-9_A", CH_MAIN)
    b = b[b["n_labeled"] > 0].copy()
    b["y"] = (b["code"] > 0).astype(int)
    b = b.dropna(subset=cols).reset_index(drop=True)
    split = int(len(b) * 0.7)
    tr, te = b.iloc[:split], b.iloc[split:]
    mdl = Pipeline([("sc", StandardScaler()),
                    ("clf", LogisticRegression(max_iter=2000, C=1.0,
                                               class_weight="balanced",
                                               random_state=SEED))])
    mdl.fit(tr[cols], tr["y"])
    p_refit = mdl.predict_proba(te[cols])[:, 1]
    p_saved = np.array(preds["E1_F-9_A_logreg"]["p"])
    same_len = len(p_refit) == len(p_saved)
    identical = same_len and np.array_equal(p_refit, p_saved)
    check("determinism_refit", identical,
          f"len refit/saved={len(p_refit)}/{len(p_saved)} identical={identical}")

    n_pass = sum(1 for c in CHECKS if c["pass"])
    verdict = "ALL PASS" if n_pass == len(CHECKS) else "ADA GAGAL"
    out = {"n_checks": len(CHECKS), "n_pass": n_pass, "verdict": verdict, "checks": CHECKS}
    with open("/mnt/d/Capstone 1/docs/V5_J2_VERIFY.json", "w") as fh:
        json.dump(out, fh, indent=1)
    print(f"\n{verdict}: {n_pass}/{len(CHECKS)}")


if __name__ == "__main__":
    main()
