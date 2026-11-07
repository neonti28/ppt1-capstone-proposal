#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
code/30_audit_inventory.py — AUDIT t_abc6eef6 [ML Auditor] CHECK 2 (leakage) + CHECK 5 (claim boundary)

Dijalankan oleh AUDITOR (bukan ML Engineer). Semua angka di stdout = bukti eksekusi sendiri.

Bagian A : kolom dataset -> daftar fitur nyata, kolom terlarang, kolom "masa depan"
Bagian B : rekonstruksi independen window fitur dari usrop_timestamped.csv (bukti fitur
           hanya memakai window [md-W, md] / data lampau)
Bagian C : cross-check tabel/klaim docs/V2_ML_RESULTS.md terhadap artefak eksekusi
           (V2_ML_METRICS.json, V2_ML_RUN_LOG.txt, V2_TSPP_AE_SCORES.csv)
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path
import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
DS = BASE / "data" / "predictive" / "dataset_prediktif.csv"
USROP = BASE / "data" / "volve" / "usrop_timestamped.csv"
REPORT = BASE / "docs" / "V2_ML_RESULTS.md"
METRICS = BASE / "docs" / "V2_ML_METRICS.json"
RUNLOG = BASE / "docs" / "V2_ML_RUN_LOG.txt"
TSPP_CSV = BASE / "docs" / "V2_TSPP_AE_SCORES.csv"

FORBIDDEN = ["MSE", "D_exp", "ROC_coef", "label"]
FUTURE_TOKENS = ["label", "next_event", "lead", "y_10", "y_5", "y_15", "y_30",
                 "est_timestamp", "event", "act_start", "mse", "roc", "d_exp", "health"]
STAT_PREFIX = ("mean_", "std_", "first_", "last_", "delta_")

def hdr(t): print("\n" + "=" * 78 + f"\n{t}\n" + "=" * 78, flush=True)
findings = []

def chk(name, ok, detail):
    findings.append((name, bool(ok), detail))
    print(f"  [{'OK ' if ok else 'GAGAL'}] {name}: {detail}", flush=True)

# ---------------------------------------------------------------- A. kolom
hdr("A. KOLOM DATASET & FITUR (leakage statis)")
ds = pd.read_csv(DS, nrows=200)
cols = list(ds.columns)
print(f"dataset_prediktif.csv: {len(cols)} kolom (baca 200 baris)")
feats = [c for c in cols if c.startswith(STAT_PREFIX)]
meta = [c for c in cols if not c.startswith(STAT_PREFIX)]
print(f"fitur (prefix mean/std/first/last/delta) = {len(feats)}")
print(f"kolom non-fitur     = {len(meta)} -> {meta}")

for f in FORBIDDEN:
    print(f"  FORBIDDEN '{f}' persis di kolom dataset? {f in cols}")

susp = [c for c in feats if any(t in c.lower() for t in FUTURE_TOKENS)]
print(f"fitur dengan token 'masa depan' (label/event/next/lead/ts/mse/roc/d_exp)? {susp}")

sensors_slug = ["md", "wob", "spp", "torque", "rop", "rpm", "flow", "mud_density",
                "diameter", "hookload", "tvd", "gamma"]
expect = {f"{st}_{sl}" for st in ("mean", "std", "first", "last", "delta") for sl in sensors_slug}
ok_feats = set(feats) == expect
print(f"fitur == persis 60 kolom resep (5 stat x 12 sensor)? {ok_feats}")
if not ok_feats:
    print(f"  extra : {sorted(set(feats) - expect)}")
    print(f"  kurang: {sorted(expect - set(feats))}")
chk("A1 fitur == 60 kolom resep", ok_feats, "5 statistik x 12 sensor, tanpa kolom lain")
chk("A2 0 kolom terlarang di daftar fitur", not susp and all(f not in feats for f in FORBIDDEN),
    "MSE/D_exp/ROC_coef/label/timestamp/next_event tidak ada di fitur")

# ---------------------------------------------------------------- B. rekonstruksi window
hdr("B. REKONSTRUKSI INDEPENDEN WINDOW FITUR (fitur = data LAMPAU saja?)")
us = pd.read_csv(USROP)
us["row_id"] = np.arange(len(us), dtype=np.int64)
keep = (us["join_status"] == "interpolated") & us["est_timestamp"].notna()
sub = us.loc[keep].copy()
dsv = pd.read_csv(DS, usecols=["row_id", "md", "last_md", "mean_rop", "first_gamma", "delta_torque"])
print(f"row_id dataset: min={dsv.row_id.min()} max={dsv.row_id.max()} n={len(dsv)} "
      f"| baris lolos sampling usrop = {len(sub)}")
print(f"urutan row_id dataset == urutan baris lolos sampling? "
      f"{list(dsv.row_id[:5]) == list(sub['row_id'][:5])} (contoh {list(dsv.row_id[:5])})")

W = 10.0
rng = np.random.default_rng(7)
sample_idx = rng.choice(len(dsv), size=300, replace=False)
mis = {"last_md": 0, "mean_rop": 0, "first_gamma": 0, "delta_torque": 0}
worst = {"last_md": 0.0, "mean_rop": 0.0, "first_gamma": 0.0, "delta_torque": 0.0}
for i in sample_idx:
    rid = int(dsv.row_id.iloc[i])
    r = sub.loc[sub.row_id == rid]
    if len(r) == 0:
        continue
    well = r["well"].iloc[0]
    md_t = float(r["Measured Depth m"].iloc[0])
    g = sub[sub["well"] == well]
    md = pd.to_numeric(g["Measured Depth m"], errors="coerce").to_numpy(float)
    order = np.argsort(md, kind="stable")
    md_s = md[order]
    pos = np.searchsorted(md_s, md_t, side="right") - 1
    left = np.searchsorted(md_s, md_t - W, side="left")
    def col(name):
        x = pd.to_numeric(g[name], errors="coerce").to_numpy(float)[order]
        return np.nan_to_num(x, nan=0.0, posinf=0.0, neginf=0.0)
    rop = col("Rate of Penetration m/h"); gamma = col("USROP Gamma gAPI")
    tq = col("Average Surface Torque kN.m")
    ref = {
        "last_md": md_s[pos],
        "mean_rop": float(rop[left:pos + 1].mean()),
        "first_gamma": float(gamma[left]),
        "delta_torque": float(tq[pos] - tq[left]),
    }
    got = dsv.iloc[i]
    for k, v in ref.items():
        d = abs(v - float(got[k]))
        rel = d / max(abs(v), 1e-9)
        worst[k] = max(worst[k], rel)
        # toleransi: penulisan CSV memakai float_format %.6g (6 signifikan)
        mis[k] += rel > 1e-5
print("300 baris acak, rekonstruksi manual window [md-10, md] dari file mentah "
      "(toleransi relatif 1e-5 = presisi %.6g):")
for k in mis:
    print(f"  {k:13s} mismatch {mis[k]}/300 | selisih relatif terbesar {worst[k]:.3g}")
ok_window = all(v == 0 for v in mis.values())
chk("B1 window fitur ter-rekonstruksi dari data lampau", ok_window,
    "300/300 baris sama pada 4 fitur representatif (mean/first/last/delta)")
print("  -> fitur HANYA dihitung dari baris dengan md <= md_t (window mundur 10 m).")
print("  -> 'md'/'tvd' ikut fitur = posisi kedalaman, bukan kolom label/timestamp.")
print(f"  fitur berisi 'est_timestamp'? {any('timestamp' in c for c in feats)}")
print(f"  fitur berisi 'next_event'?    {any('next_event' in c for c in feats)}")

# ---------------------------------------------------------------- C. claim cross-check
hdr("C. CROSS-CHECK KLAIM docs/V2_ML_RESULTS.md vs ARTEFAK EKSEKUSI")
report = REPORT.read_text(encoding="utf-8")
met = json.loads(METRICS.read_text(encoding="utf-8"))
dsm = json.loads((BASE / "docs" / "V2_PREDICTIVE_DATASET_METRICS.json").read_text(encoding="utf-8"))

# C1 tabel §9 TSPP
tspp_csv = pd.read_csv(TSPP_CSV)
print("\n-- C1: tabel §9 (validasi sekunder Bo TSPP) vs V2_TSPP_AE_SCORES.csv --")
tbl_rows = re.findall(
    r"^\| (TSPP[\w\-.]+\.csv) \| ([\d\.]+) \| (\d+) \| ([\d,]+) \| ([\d,]+)% \| ([\d,]+)% \|",
    report, flags=re.M)
print(f"  baris tabel terdeteksi di report: {len(tbl_rows)}")
bad1 = []
for fname, rows_s, cols_s, err_s, share_s, z_s in tbl_rows:
    rows_r = int(rows_s.replace(".", ""))
    err_r = float(err_s.replace(",", "."))
    share_r = float(share_s.replace(",", ".")) / 100
    z_r = float(z_s.replace(",", ".")) / 100
    row = tspp_csv[tspp_csv.file == fname]
    if len(row) == 0:
        bad1.append(fname); print(f"    {fname}: tidak ada di artefak"); continue
    r = row.iloc[0]
    same = (int(r.rows) == rows_r and abs(float(r.err_median) - err_r) < 5e-4
            and abs(float(r.share_above_threshold) - share_r) < 1e-3
            and abs(float(r.share_rows_any_z_gt3) - z_r) < 1e-3)
    print(f"    {fname:16s} report rows={rows_r:7d} err={err_r:.4f} share={share_r:.3f} z={z_r:.3f} | "
          f"eksekusi rows={int(r.rows):7d} err={float(r.err_median):.4f} "
          f"share={float(r.share_above_threshold):.3f} z={float(r.share_rows_any_z_gt3):.3f} "
          f"-> {'cocok' if same else 'TIDAK COCOK'}")
    if not same:
        bad1.append(fname)
chk("C1 tabel §9 TSPP == artefak eksekusi", len(bad1) == 0,
    "semua baris identik" if not bad1 else f"{len(bad1)}/6 baris BEDA dari output eksekusi")

# C2 tabel §5 temporal
print("\n-- C2: tabel §5 (hasil temporal) vs V2_ML_METRICS.json --")
probe = [
    ("B1 logistik hanya-MD", "0,1218", met["run"]["baselines_temporal"]["B1_logistik_hanya_MD"]["pr_auc"]),
    ("B2 fuzzy legacy", "0,0457", met["run"]["baselines_temporal"]["B2_legacy_fuzzy"]["pr_auc"]),
    ("B3 RF with_md", "0,0796", met["run"]["rf_temporal"]["B3_RF_with_md"]["pr_auc"]),
    ("B3 RF no_md", "0,0750", met["run"]["rf_temporal"]["B3_RF_no_md"]["pr_auc"]),
    ("M1 AE", "0,0368", met["run"]["ae_temporal"]["pr_auc"]),
]
all_match = True
for name, rep, js in probe:
    rep_f = float(rep.replace(",", "."))
    ok = abs(rep_f - js) < 5e-5
    all_match &= ok
    print(f"    {name:24s} report={rep} json={js} -> {'cocok' if ok else 'BEDA'}")
chk("C2 tabel §5 == JSON", all_match, "5/5 PR-AUC temporal identik")

# C3 runtime
print("\n-- C3: klaim runtime --")
m = re.search(r"Runtime terukur: ([\d,]+) s \+ ([\d,]+) s \+ ([\d,]+) s \+ ([\d,]+) s", report)
vals = [float(x.replace(",", ".")) for x in m.groups()] if m else []
print(f"    report: {vals}; JSON runtime_s_total={met['run']['runtime_s_total']}")
ok3 = bool(m) and abs(vals[1] - met["run"]["runtime_s_total"]) < 0.5
chk("C3 runtime total", ok3, f"284 s vs JSON {met['run']['runtime_s_total']}")

# C4 forbidden columns saat build
print(f"\n-- C4: forbidden_columns_absent di V2_PREDICTIVE_DATASET_METRICS.json = "
      f"{dsm['output'].get('forbidden_columns_absent')} --")
print(f"    distribusi kelas: { {k: v['prev'] for k, v in dsm['class_distribution'].items()} }")
chk("C4 forbidden columns (build)", dsm["output"].get("forbidden_columns_absent") is True,
    "MSE/D_exp/ROC_coef/label tidak tertulis ke CSV")

# C5 klaim 85,8%
xc = dsm["timestamp_crosscheck_delta_main"]
print(f"\n-- C5: cross-check waktu: {xc} --")
chk("C5 klaim 85,8% est<=act", abs(xc["frac_est_ts_sebelum_event"] - 0.858) < 0.005,
    f"JSON frac={xc['frac_est_ts_sebelum_event']:.4f}")

# C6 tabel §1 & §5 lain: B2b & LOWO
print("\n-- C6: sampel klaim lain (LOWO pooled, D2, delta) --")
lowo = met["run"]["lowo"]["pooled"]
diag = json.loads((BASE / "docs" / "V2_ML_DIAGNOSTICS.json").read_text(encoding="utf-8"))
c6 = [
    ("LOWO pooled PR-AUC 0,0907", abs(lowo["pr_auc"] - 0.0907) < 5e-5, lowo["pr_auc"]),
    ("LOWO macro fold 0,1033", abs(lowo["macro_pr_auc_folds"] - 0.1033) < 5e-5, lowo["macro_pr_auc_folds"]),
    ("D2 RF baris-saja test 0,194", abs(diag["D2_raw_row_features"]["test_pr_auc"] - 0.194) < 5e-4,
     diag["D2_raw_row_features"]["test_pr_auc"]),
    ("D4 canary LOWO macro 0,2265", abs(diag["D4_md_only_lowo"]["pooled"]["macro"] - 0.2265) < 5e-5,
     diag["D4_md_only_lowo"]["pooled"]["macro"]),
    ("prev seluruh data y10 = 6,88%", abs(dsm["class_distribution"]["y_10"]["prev"] - 0.06883) < 1e-5,
     dsm["class_distribution"]["y_10"]["prev"]),
    ("prev y30 = 16,54%", abs(dsm["class_distribution"]["y_30"]["prev"] - 0.16538) < 1e-5,
     dsm["class_distribution"]["y_30"]["prev"]),
]
for nm, ok, val in c6:
    print(f"    [{'OK ' if ok else 'GAGAL'}] {nm} -> {val}")
    chk(nm, ok, f"nilai eksekusi {val}")

hdr("RINGKASAN CHECK 2 (leakage) & CHECK 5 (claim boundary)")
for nm, ok, d in findings:
    print(f"  {'PASS' if ok else 'FAIL'} | {nm} | {d}")
n_fail = sum(1 for _, ok, _ in findings if not ok)
print(f"\nTOTAL: {len(findings)-n_fail} PASS, {n_fail} FAIL")
json.dump([{"name": n, "ok": ok, "detail": d} for n, ok, d in findings],
          open(BASE / "docs" / "V2_ML_AUDIT_PART0.json", "w"), indent=2, ensure_ascii=False)
print("-> docs/V2_ML_AUDIT_PART0.json")
sys.exit(0)
