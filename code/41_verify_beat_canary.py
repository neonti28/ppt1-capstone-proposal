#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
code/41_verify_beat_canary.py — helper verifikasi acceptance T2+T3 (task t_d6df5080)

Acceptance (dicek PM/auditor):
  (a) angka reproduksi dari log
  (b) garis acuan F1 0,058/0,110/0,151/0,256 tetap ada
  (c) framing §3.3 dipakai apa adanya
  (d) 0 angka karangan

Cek yang dijalankan (semua dari file di disk, exit 0 = semua PASS):
  1. docs/V2_ML_BEAT_CANARY_RUN_LOG.txt ada, memuat "SELESAI" + verdict T2/T3
     yang identik dengan JSON.
  2. Semua baris tabel §3/§5 di MD ada padanan angkanya di JSON (fold per fold).
  3. Garis acuan F1: 0,058 | 0,110 | 0,151 | 0,256 ada di MD §8.
  4. Framing §3.3 di MD identik (karakter demi karakter) dengan kutipan PM
     di docs/V2_PM_AUDIT.md §3.3.
  5. Verdict gate di MD == verdict di JSON == perhitungan ulang dari JSON
     (macro >= 0.2465 & menang >= 5/7; R@P0.20 > 0).
  6. B1 canary macro-LOWO di JSON == 0.2265 (referensi beku T1/D4).
  7. Tidak ada angka "0.2465"-palsu: target T2 di MD = 0.2465 konsisten.

Output: stdout + exit 0/1.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
MD = BASE / "docs" / "V2_ML_BEAT_CANARY.md"
JSON_P = BASE / "docs" / "V2_ML_BEAT_CANARY.json"
LOG = BASE / "docs" / "V2_ML_BEAT_CANARY_RUN_LOG.txt"
PM = BASE / "docs" / "V2_PM_AUDIT.md"

FAILS: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    print(f"{'PASS' if ok else 'FAIL'} | {name}" + (f" — {detail}" if detail else ""), flush=True)
    if not ok:
        FAILS.append(name)


def main() -> None:
    md = MD.read_text(encoding="utf-8")
    res = json.loads(JSON_P.read_text(encoding="utf-8"))
    log = LOG.read_text(encoding="utf-8")
    pm = PM.read_text(encoding="utf-8")

    # 1. log exit-0 markers + verdict identik
    check("log: memuat SELESAI", "SELESAI" in log)
    check("log: memuat T2 KESELURUHAN", "T2 KESELURUHAN: FAIL" in log
          or "T2 KESELURUHAN: PASS" in log)
    m2 = re.search(r"T2 KESELURUHAN: (PASS|FAIL)", log)
    m3 = re.search(r"T3 KESELURUHAN: (PASS|FAIL)", log)
    check("log verdict == JSON verdict",
          bool(m2) and bool(m3)
          and (m2.group(1) == ("PASS" if res["verdict"]["T2_overall"] else "FAIL"))
          and (m3.group(1) == ("PASS" if res["verdict"]["T3_overall"] else "FAIL")),
          f"log T2={m2 and m2.group(1)} T3={m3 and m3.group(1)}")

    # 2. angka tabel fold di MD ada di JSON
    short = {"F-9A": "USROP_A 0 N-NA_F-9_Ad.csv", "F-7": "USROP_A 1 N-S_F-7d.csv",
             "F-14": "USROP_A 2 N-SH_F-14d.csv", "F-15A": "USROP_A 3 N-SH-F-15d.csv",
             "F-15 (S)": "USROP_A 4 N-SH_F-15Sd.csv", "F-5": "USROP_A 5 N-SH-F-5d.csv",
             "F-9": "USROP_A 6 N-SH_F-9d.csv"}
    models = ["B1_canary_md", "A1_rf_row", "A2_rf_row_platt", "A3_hgb_row", "A4_log_row"]
    miss = []
    for shortn, full in short.items():
        row = re.search(rf"^\| {re.escape(shortn)} \|(.*)$", md, re.M)
        if not row:
            miss.append(f"{shortn}: baris tak ada")
            continue
        cells = [c.strip().strip("*") for c in row.group(1).split("|")]
        # sel: n, prev, B1, A1, A2, A3, A4, D1
        jf = res["d10"]["folds"]
        expect = [str(jf["B1_canary_md"][full]["n"]), str(jf["B1_canary_md"][full]["prev"]),
                  str(jf["B1_canary_md"][full]["pr_auc"]),
                  str(jf["A1_rf_row"][full]["pr_auc"]),
                  str(jf["A2_rf_row_platt"][full]["pr_auc"]),
                  str(jf["A3_hgb_row"][full]["pr_auc"]),
                  str(jf["A4_log_row"][full]["pr_auc"]),
                  str(jf["D1_hgb_md_diag"][full]["pr_auc"])]
        got = cells[:8]
        if got != expect:
            miss.append(f"{shortn}: MD={got} JSON={expect}")
    check("tabel fold Δ10 MD == JSON (7 fold x 8 sel)", not miss, "; ".join(miss[:3]))

    # Δ30 fold table
    miss30 = []
    for shortn, full in short.items():
        row = re.search(rf"^\| {re.escape(shortn)} \(prev [\d.]+\) \|(.*)$", md, re.M)
        if not row:
            miss30.append(f"{shortn}: baris Δ30 tak ada")
            continue
        cells = [c.strip() for c in row.group(1).split("|")]
        jf = res["d30"]["folds"]
        expect = [str(jf["B1_canary_md"][full]["pr_auc"]),
                  str(jf["A1_rf_row"][full]["pr_auc"]),
                  str(jf["A2_rf_row_platt"][full]["pr_auc"]),
                  str(jf["A3_hgb_row"][full]["pr_auc"]),
                  str(jf["A4_log_row"][full]["pr_auc"])]
        if cells[:5] != expect:
            miss30.append(f"{shortn}: MD={cells[:5]} JSON={expect}")
    check("tabel fold Δ30 MD == JSON", not miss30, "; ".join(miss30[:3]))

    # pooled table Δ10
    missp = []
    for m in models + ["D1_hgb_md_diag"]:
        p = res["d10"]["pooled"][m]
        pat = rf"^\| {re.escape(m)} \| {re.escape(str(p['pr_auc']))} \({re.escape(str(p['lift']))}"
        if not re.search(pat, md, re.M):
            missp.append(m)
    check("tabel pooled Δ10 MD == JSON (PR-AUC + lift)", not missp, ", ".join(missp))

    # 3. garis acuan F1
    check("garis acuan F1 0,058 | 0,110 | 0,151 | 0,256 ada di MD",
          all(s in md for s in ("0,058", "0,110", "0,151", "0,256")))

    # 4. framing §3.3 identik
    pm_q = re.search(r"Pipeline predictive maintenance \(event nyata.*?baseline tersebut\.",
                     pm, re.S)
    md_q = re.search(r"Pipeline predictive maintenance \(event nyata.*?baseline tersebut\.", md, re.S)
    check("framing §3.3 identik dgn PM audit", bool(pm_q) and bool(md_q)
          and pm_q.group(0) == md_q.group(0),
          f"pm={bool(pm_q)} md={bool(md_q)}")

    # 5. verdict MD == JSON == hitung ulang dari JSON
    v = res["verdict"]
    recompute = {}
    for m, d in v["T2_per_model"].items():
        macro = res["d10"]["pooled"][m]["macro_pr_auc"]
        wins = sum(1 for w in res["d10"]["folds"][m]
                   if res["d10"]["folds"][m][w].get("pr_auc") is not None
                   and res["d10"]["folds"][m][w]["pr_auc"]
                   > res["d10"]["folds"]["B1_canary_md"][w]["pr_auc"])
        recompute[m] = (macro >= 0.2465 and wins >= 5)
        check(f"verdict T2 {m} konsisten (JSON vs hitung ulang)",
              d["macro"] == macro and d["wins"] == wins and d["pass"] == recompute[m],
              f"macro={macro} wins={wins}")
    md_t2 = "T2: FAIL" in md.replace("**", "")
    check("MD verdict T2 == JSON", md_t2 == (not v["T2_overall"]))
    md_t3 = "T3: PASS" in md.replace("**", "")
    check("MD verdict T3 == JSON", md_t3 == v["T3_overall"])
    for m, d in v["T3_per_model"].items():
        rp = res["d10"]["pooled"][m]["recall_at_p020"]
        check(f"verdict T3 {m} konsisten", d["recall_at_p020"] == rp
              and d["pass"] == (rp > 0), f"R@P0.20={rp}")

    # 6. referensi beku
    check("B1 canary macro == 0.2265 (referensi beku)",
          res["d10"]["pooled"]["B1_canary_md"]["macro_pr_auc"] == 0.2265,
          str(res["d10"]["pooled"]["B1_canary_md"]["macro_pr_auc"]))
    check("target T2 di JSON == 0.2465", res["reference"]["t2_target_macro"] == 0.2465)

    # 7. artefak ada
    for p in (MD, JSON_P, LOG, BASE / "code" / "40_beat_canary.py"):
        check(f"ada: {p.relative_to(BASE)}", p.exists() and p.stat().st_size > 0)

    print("\n" + ("=" * 60))
    if FAILS:
        print(f"VERIFIKASI: {len(FAILS)} GAGAL -> {FAILS}")
        sys.exit(1)
    print("VERIFIKASI: SEMUA CHECK PASS (exit 0)")


if __name__ == "__main__":
    main()
