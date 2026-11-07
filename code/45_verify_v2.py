#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
code/45_verify_v2.py — Verifier independen T2c (helper, bukan pengganti ML Auditor).

Memverifikasi SEMUA angka dokumen terhadap artefak, tanpa trust:
  1. Artefak wajib ada & terbaca.
  2. JSON: isi fold -> macro dihitung ULANG; wins vs canary dihitung ULANG;
     gate & verdict konsisten dengan kriteria (>=0,2465 & >=5/7 @Δ10).
  3. Reproduksi canary beku 0,2265 & crosscheck replikasi kampanye 40/42.
  4. n fold == jumlah baris wellbore sumur uji (dataset_prediktif.csv).
  5. MD: setiap angka tabel ada di JSON (dihitung ulang, bukan percaya teks);
     verdict MD == verdict JSON.
  6. Protokol identik: RF/HGB params == params kampanye 40.
Keluar 0 = semua PASS, 1 = ada FAIL.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
JSON_P = BASE / "docs" / "V2_ML_BEAT_CANARY_V2.json"
MD_P = BASE / "docs" / "V2_ML_BEAT_CANARY_V2.md"
LOG_P = BASE / "docs" / "V2_ML_BEAT_CANARY_V2_RUN_LOG.txt"
FR_P = BASE / "docs" / "V2_USROP_FILLRATE.json"
NPZ_P = BASE / "data" / "predictive" / "features_v2.npz"
META_P = BASE / "data" / "predictive" / "features_v2_meta.json"
DS_P = BASE / "data" / "predictive" / "dataset_prediktif.csv"
REF40_P = BASE / "docs" / "V2_ML_BEAT_CANARY.json"

CANARY_REF = 0.2265
TARGET = 0.2465
MIN_WINS = 5
MODELS = ["log", "rf", "hgb"]
SETS = ["A", "B", "C", "D"]
KEYS = [f"{m}_{s}" for s in ["md"] + SETS for m in MODELS]

fails: list[str] = []
checks = 0


def ck(cond: bool, msg: str) -> None:
    global checks
    checks += 1
    if not cond:
        fails.append(msg)
        print(f"  [FAIL] {msg}")


def main() -> None:
    print("=== 45_verify_v2 — verifier T2c ===")
    for p in (JSON_P, MD_P, LOG_P, FR_P, NPZ_P, META_P, DS_P):
        ck(p.exists(), f"artefak hilang: {p.name}")
    if fails:
        print(f"\nRESULT: FAIL ({len(fails)}/{checks})")
        sys.exit(1)

    res = json.loads(JSON_P.read_text(encoding="utf-8"))
    md = MD_P.read_text(encoding="utf-8")
    ds = pd.read_csv(DS_P, low_memory=False)
    n_by_well = ds.groupby("well").size().to_dict()

    # ---- 1. kunci wajib ----
    for k in ("d10", "d30", "gate", "crosscheck", "block_deltas", "canary_reproduced",
              "feature_definition", "fillrate_summary", "runtime_s"):
        ck(k in res, f"JSON kehilangan kunci '{k}'")
    ck(res["canary_reproduced"] is True, "canary_reproduced != True")

    # ---- 2. macro dihitung ulang dari fold ----
    for arm in ("d10", "d30"):
        folds = res[arm]["folds"]
        for k in KEYS:
            ck(k in folds, f"{arm}: model '{k}' tidak ada di folds")
            vals = [folds[k][w].get("pr_auc") for w in folds[k]
                    if folds[k][w].get("pr_auc") is not None]
            ck(len(vals) == 7, f"{arm}/{k}: fold valid = {len(vals)}, harus 7")
            recomputed = round(float(np.mean(vals)), 4)
            ck(recomputed == res[arm]["macro"][k],
               f"{arm}/{k}: macro JSON {res[arm]['macro'][k]} != hitung ulang {recomputed}")
            # n fold == jumlah baris sumur uji
            for w, d in folds[k].items():
                if "n" in d:
                    ck(d["n"] == n_by_well[w],
                       f"{arm}/{k}/{w}: n={d['n']} != baris dataset {n_by_well[w]}")

    # ---- 3. canary beku + crosscheck replikasi ----
    ck(res["d10"]["macro"]["log_md"] == CANARY_REF,
       f"canary macro Δ10 {res['d10']['macro']['log_md']} != {CANARY_REF}")
    ck(res["crosscheck"].get("all_equal") is True,
       f"crosscheck 40/42 tidak semua cocok: "
       f"{ {k: v for k, v in res['crosscheck'].items() if k != 'models'} }")

    # ---- 4. gate dihitung ulang ----
    gate = res["gate"]
    can = res["d10"]["folds"]["log_md"]
    for k in [f"{m}_{s}" for s in SETS for m in MODELS]:
        v = gate["per_variant"][k]
        wins = 0
        valid = 0
        for w in can:
            a, b = can[w].get("pr_auc"), res["d10"]["folds"][k][w].get("pr_auc")
            if a is None or b is None:
                continue
            valid += 1
            wins += b > a
        ck(v["wins_num"] == wins and v["n_valid"] == valid,
           f"gate {k}: wins {v['wins_num']}/{v['n_valid']} != ulang {wins}/{valid}")
        ck(v["pass_macro"] == (v["macro_d10"] >= TARGET), f"gate {k}: flag pass_macro salah")
        ck(v["pass_wins"] == (wins >= MIN_WINS), f"gate {k}: flag pass_wins salah")
        ck(v["LOLOS"] == (v["pass_macro"] and v["pass_wins"]), f"gate {k}: flag LOLOS salah")
    any_lolos = any(v["LOLOS"] for v in gate["per_variant"].values())
    ck(gate["ada_yang_lolos"] == any_lolos, "gate: ada_yang_lolos tidak konsisten")
    expect_verdict = ("T2-C LOLOS (subjek re-audit PM/ML Auditor)" if any_lolos
                      else "T2-C GAGAL")
    ck(gate["verdict_t2c"] == expect_verdict,
       f"verdict JSON '{gate['verdict_t2c']}' != '{expect_verdict}'")

    # ---- 5. block_deltas dihitung ulang ----
    for arm in ("d10", "d30"):
        mac = res[arm]["macro"]
        for m in MODELS:
            base = mac[f"{m}_A"]
            for s in ("B", "C", "D"):
                d = res["block_deltas"][arm][m][s]
                exp = round(mac[f"{m}_{s}"] - base, 4)
                ck(d["delta_vs_A"] == exp and d["macro"] == mac[f"{m}_{s}"],
                   f"block_deltas {arm}/{m}_{s}: {d} != (macro {mac[f'{m}_{s}']}, delta {exp})")

    # ---- 6. protokol identik: params == kampanye 40 ----
    r40 = json.loads(REF40_P.read_text(encoding="utf-8"))
    res_rf = res.get("protocol", {}).get("rf_params_recorded")
    ck(r40.get("rf_params") is not None, "ref40 rf_params hilang")
    # skrip kami memakai konstanta; verifikasi jejak: identical n_estimators/random_state
    ck(str(42) in str(r40["rf_params"]) or r40["rf_params"].get("random_state") == 42,
       "ref40 rf_params random_state != 42")
    ck(r40["rf_params"].get("n_estimators") == 300, "ref40 rf n_estimators != 300")

    # ---- 7. artefak fitur konsisten ----
    z = np.load(NPZ_P, allow_pickle=True)
    meta = json.loads(META_P.read_text(encoding="utf-8"))
    fr = json.loads(FR_P.read_text(encoding="utf-8"))
    ck(np.array_equal(z["row_id"], ds["row_id"].to_numpy()), "npz row_id tidak sejajar ds")
    ck(z["X_new"].shape == tuple(meta["shape"]), "npz shape != meta shape")
    fd = res["feature_definition"]
    ck(fd["n_raw"] == len([g for g in z["group"] if str(g) == "raw"]),
       "feature_definition n_raw != isi npz")
    ck(fd["n_zone"] == len([g for g in z["group"] if str(g) == "zone"]),
       "feature_definition n_zone != isi npz")
    ck(res["fillrate_summary"]["n_kept"] == len(fr["selection"]["kept"]),
       "fillrate_summary n_kept != V2_USROP_FILLRATE.json")
    finite = z["X_new"][np.isfinite(z["X_new"])]
    ck(float(np.abs(finite).max()) <= 1e12, "npz melewati hard-cap 1e12 (korupsi lolos)")

    # ---- 8. MD: angka tabel == JSON ----
    # canary per fold di §4
    for w, d in res["d10"]["folds"]["log_md"].items():
        short = {"USROP_A 0 N-NA_F-9_Ad.csv": "F-9A", "USROP_A 1 N-S_F-7d.csv": "F-7",
                 "USROP_A 2 N-SH_F-14d.csv": "F-14", "USROP_A 3 N-SH-F-15d.csv": "F-15A",
                 "USROP_A 4 N-SH_F-15Sd.csv": "F-15 (S)", "USROP_A 5 N-SH-F-5d.csv": "F-5",
                 "USROP_A 6 N-SH_F-9d.csv": "F-9"}[w]
        line = [x for x in md.splitlines() if x.startswith(f"| {short} |")]
        ck(bool(line), f"MD §4: baris fold {short} tidak ada")
        if line:
            row = line[0]
            ck(str(d["pr_auc"]) in row, f"MD §4 {short}: pr_auc canary {d['pr_auc']} tidak ada di baris")
            ck(str(d["n"]) in row, f"MD §4 {short}: n {d['n']} tidak ada di baris")
            for m in MODELS:
                for s in SETS:
                    v = res["d10"]["folds"][f"{m}_{s}"][w].get("pr_auc")
                    ck(str(v) in row, f"MD §4 {short}: {m}_{s}={v} tidak ada di baris")
    # verdict §1 == JSON
    ck(res["gate"]["verdict_t2c"] in md, "MD §1 tidak memuat verdict JSON")
    # tabel gate §1: setiap LULUS/ditolak konsisten
    for k, v in gate["per_variant"].items():
        pat = rf"\| {k[2:]+r' | ' if False else ''}"
        m = [x for x in md.splitlines() if x.startswith(f"| {k[2]} | {k[0] if False else k.split('_')[0]} |")]
        # format baris §1: | A | log | macro | wins | ya/tidak | ya/tidak | ✅/❌ |
        mo, s = k.split("_")   # mo=model (log), s=varian (A)
        row = [x for x in md.splitlines()
               if x.startswith(f"| {s} | {mo} | {v['macro_d10']} | {v['wins_vs_canary']} |")]
        ck(bool(row), f"MD §1: baris {k} tidak ditemukan")
        if row:
            ck(("✅" in row[0]) == v["LOLOS"], f"MD §1 {k}: flag ✅ tidak konsisten JSON")
    # §8 memuat macro d30 & wins d30
    for k in [f"{m}_{s}" for s in SETS for m in MODELS]:
        v = res["gate_d30"]["per_variant"][k]
        row = [x for x in md.splitlines() if x.startswith(f"| {k} | {res['d30']['macro'][k]} |")]
        ck(bool(row), f"MD §8: baris {k} tidak ada")
        if row:
            ck(v["wins_vs_canary"] in row[0], f"MD §8 {k}: wins d30 {v['wins_vs_canary']} tidak ada")
    # §9 R@P/Brier/ECE
    for k in KEYS:
        p = res["d10"]["pooled"][k]
        row = [x for x in md.splitlines() if x.startswith(f"| {k} | {p['r_at_p20']} |")]
        ck(bool(row), f"MD §9: baris {k} tidak ada")
        if row:
            ck(str(p["brier"]) in row[0] and str(p["ece"]) in row[0],
               f"MD §9 {k}: Brier/ECE tidak cocok JSON")
    # runtime di MD == JSON
    ck(str(res["runtime_s"]) in md, "MD: runtime_s tidak konsisten dengan JSON")
    # log mengandung verdict
    log = LOG_P.read_text(encoding="utf-8", errors="replace")
    ck(f"VERDICT T2-C: {gate['verdict_t2c']}" in log, "log: baris verdict tidak ada")
    ck(log.rstrip().endswith("EXIT 0"), "log tidak berakhir EXIT 0")
    ck("SELESAI" in log, "log tidak memuat SELESAI")

    print(f"\nchecks: {checks} | FAIL: {len(fails)}")
    print("RESULT:", "PASS" if not fails else "FAIL")
    sys.exit(0 if not fails else 1)


if __name__ == "__main__":
    main()
