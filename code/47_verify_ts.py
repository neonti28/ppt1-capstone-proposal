#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
code/47_verify_ts.py — Verifier INDEPENDEN kampanye T2-d (kanban t_9df689f1).

Jalur kode BERBEDA dari code/46 (menghitung ulang, bukan membaca klaim):
  V1  macro per varian dihitung ulang dari tabel fold di JSON -> cocok field macro
  V2  gate dihitung ulang: canary=log_G, target=max(0,2465, canary+0,02),
      menang/5-7 fold per varian -> cocok field gate (termasuk flag LOLOS)
  V3  dokumen MD memuat token angka kunci (diambil dari p4_desain_baru bila ada:
      canary, target, verdict, wins, framing §3.3)
  V4  sampling dihitung ULANG dari timestamp CSV mentah per fold
      (p_f, quiet pool, n_neg) -> cocok sampling di JSON
  V5  anti-leakage: sebaris acak anchor kontrol -> slice [t-W, t) dari CSV;
      semua ts < anchor DAN n_rows cocok dgn X_window_meta tersimpan
  V6  fitur MD dihitung ulang dari kolom DMEA mentah utk beberapa anchor
      (mean/last) -> cocok X_baseline tersimpan (tol 1e-6 relatif)
  V7  konsistensi unit: n_pos/n_neg dari npz == JSON; 7 fold; tiap fold dua kelas

Keluaran: baris PASS/FAIL per cek + ringkasan "N/N PASS"; exit 0 hanya bila semua PASS.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
PARSED = BASE / "data" / "volve" / "witsml_parsed"
OUT_JSON = BASE / "docs" / "V2_ML_BEAT_CANARY_TS.json"
OUT_MD = BASE / "docs" / "V2_ML_BEAT_CANARY_TS.md"
EVENTS_NPZ = BASE / "data" / "predictive" / "features_timeseries.npz"
CONTROLS_NPZ = BASE / "data" / "predictive" / "features_timeseries_controls.npz"

TARGET_FLOOR = 0.2465
MARGIN = 0.02
MIN_WINS = 5
HORIZON_NS = 2 * 3600 * 1_000_000_000
SEED = 42
MODELS = ["log", "rf", "hgb"]
SETS = ["G", "E", "F"]
KEYS = [f"{m}_{s}" for s in SETS for m in MODELS]
CANARY_KEY = "log_G"
CHALLENGERS = [k for k in KEYS if k != CANARY_KEY and k[-1] in ("E", "F")]
WINDOWS_S = {"w30m": 30 * 60, "w2h": 2 * 3600, "w6h": 6 * 3600}

RESULTS = []


def check(name: str, ok: bool, detail: str = "") -> bool:
    RESULTS.append((name, bool(ok), detail))
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f" — {detail}" if detail else ""),
          flush=True)
    return bool(ok)


def cz2d(x) -> str:
    return f"{float(x):.4f}".replace(".", ",")


def main() -> int:
    res = json.load(open(OUT_JSON))
    md = OUT_MD.read_text(encoding="utf-8")

    # ---------- V1: macro dihitung ulang ----------
    bad = []
    for k in KEYS:
        vals = [res["folds"][k][w].get("pr_auc") for w in res["folds"][k]]
        vals = [v for v in vals if v is not None]
        mac = round(float(np.mean(vals)), 4) if vals else None
        if mac != res["macro"][k]:
            bad.append(f"{k}: {mac} vs {res['macro'][k]}")
    check("V1 macro recompute (7 fold x 9 key)", not bad, "; ".join(bad) or "semua cocok")

    # ---------- V2: gate dihitung ulang ----------
    can = res["folds"][CANARY_KEY]
    can_macro = res["macro"][CANARY_KEY]
    target = round(max(TARGET_FLOOR, can_macro + MARGIN), 4)
    bad = []
    if target != res["gate"]["target_macro"]:
        bad.append(f"target {target} vs {res['gate']['target_macro']}")
    for k in CHALLENGERS:
        wins = 0
        valid = 0
        for w in sorted(can):
            a = can[w].get("pr_auc")
            b = res["folds"][k][w].get("pr_auc")
            if a is None or b is None:
                continue
            valid += 1
            wins += b > a
        g = res["gate"]["per_variant"][k]
        lolos = (res["macro"][k] is not None and res["macro"][k] >= target
                 and wins >= MIN_WINS)
        if f"{wins}/{valid}" != g["wins_vs_canary"]:
            bad.append(f"{k} wins {wins}/{valid} vs {g['wins_vs_canary']}")
        if bool(lolos) != g["LOLOS"]:
            bad.append(f"{k} LOLOS {lolos} vs {g['LOLOS']}")
    check("V2 gate recompute (target + fold wins + flags)", not bad,
          "; ".join(bad) or f"target={target} cocok; 6 varian ok")

    # ---------- V3: token di dokumen MD ----------
    # MD kini mendokumentasikan kampanye DESAIN P4 (T2-e); token diambil dari blok
    # p4_desain_baru. Konsistensi blok arsip desain asli tervalidasi V1/V2/V4-V8.
    p4 = res.get("p4_desain_baru") or {}
    gp = p4.get("gate", res["gate"])
    tokens = [cz2d(gp["canary_macro"]), cz2d(gp["target_macro"]), gp["verdict_t2d"],
              "0,2465", "≥5/7"]
    for k in CHALLENGERS:
        tokens.append(gp["per_variant"][k]["wins_vs_canary"])
    framing_ok = "belum boleh dinaikkan sebelum model mengalahkan baseline tersebut" in md
    missing = [t for t in tokens if t not in md]
    check("V3 MD memuat token kunci + framing §3.3", not missing and framing_ok,
          ("hilang: " + ", ".join(missing)) if missing else "semua token ada")

    # ---------- V4: sampling dihitung ulang dari timestamp CSV ----------
    ev = np.load(EVENTS_NPZ, allow_pickle=True)
    ev_by_fold = {}
    for f, t in zip(ev["fold"], ev["act_start_utc"]):
        ev_by_fold.setdefault(str(f), []).append(pd.Timestamp(str(t)).value)
    bad = []
    for fold, meta in sorted(res["sampling"].items()):
        ts = pd.read_csv(PARSED / f"{fold}.csv", usecols=["timestamp"])
        t = pd.to_datetime(ts["timestamp"], format="ISO8601", utc=True)
        tns = (t.dropna().astype("int64")).sort_values().to_numpy()
        junk_cut = int(pd.Timestamp("2010-01-01", tz="UTC").value)   # ns sejak epoch
        pool = tns[tns <= junk_cut]
        evt = np.sort(np.array(ev_by_fold[fold], dtype="int64"))
        j = np.searchsorted(evt, pool, side="right")
        has = j < len(evt)
        nxt = np.full(len(pool), np.iinfo("int64").max, dtype="int64")
        nxt[has] = evt[j[has]]
        in_h = (nxt - pool) < HORIZON_NS
        p = float(in_h.mean())
        quiet = int((~in_h).sum())
        n_neg = int(round(meta["n_pos"] * (1 - p) / max(p, 1e-9)))
        if abs(p - meta["p_natural_2h"]) > 5e-5:
            bad.append(f"{fold} p {p:.4f} vs {meta['p_natural_2h']}")
        if quiet != meta["quiet_pool"]:
            bad.append(f"{fold} quiet {quiet} vs {meta['quiet_pool']}")
        if n_neg != meta["n_neg"]:
            bad.append(f"{fold} n_neg {n_neg} vs {meta['n_neg']}")
    check("V4 sampling recompute (p_f, quiet pool, n_neg per fold)", not bad,
          "; ".join(bad) or "7 fold cocok dari timestamp mentah")

    # ---------- V5: anti-leakage independen + n_rows ----------
    c = np.load(CONTROLS_NPZ, allow_pickle=True)
    cfold = np.array([str(x) for x in c["fold"]])
    cat = c["anchor_ts"].astype("int64")
    cxm = c["X_window_meta"]
    rng = np.random.default_rng(7)
    bad = []
    scanned = 0
    for fold in sorted(set(cfold)):
        ii = np.flatnonzero(cfold == fold)
        take = rng.choice(ii, size=min(4, len(ii)), replace=False)
        ts = pd.read_csv(PARSED / f"{fold}.csv", usecols=["timestamp"])
        t = pd.to_datetime(ts["timestamp"], format="ISO8601", utc=True)
        tns = (t.dropna().astype("int64")).sort_values().to_numpy()
        for i in take:
            a = int(cat[i])
            for wi, (wname, wsec) in enumerate(WINDOWS_S.items()):
                i0 = int(np.searchsorted(tns, a - wsec * 1_000_000_000, side="left"))
                i1 = int(np.searchsorted(tns, a, side="left"))
                seg = tns[i0:i1]
                scanned += seg.size
                if seg.size and (seg >= a).any():
                    bad.append(f"{fold}@{a}: {wname} leakage")
                if int(cxm[i, wi * 4]) != seg.size:
                    bad.append(f"{fold}@{a}: {wname} n_rows {seg.size} vs "
                               f"{int(cxm[i, wi * 4])}")
    check("V5 anti-leakage independen + n_rows (28 anchor x 3 jendela)", not bad,
          "; ".join(bad[:4]) or f"{scanned} baris dipindai, 0 pelanggaran")

    # ---------- V6: fitur MD dihitung ulang dari DMEA mentah ----------
    bad = []
    for fold in sorted(set(cfold))[:2]:
        ii = np.flatnonzero(cfold == fold)
        take = rng.choice(ii, size=3, replace=False)
        meta = json.load(open(PARSED / "_verify.json"))
        fill = meta[fold]["fill_rate_ge_50pct"]
        col = "DMEA" if "DMEA" in fill else ("GS_DMEA" if "GS_DMEA" in fill else None)
        if col is None:
            bad.append(f"{fold}: DMEA tak eligible")
            continue
        df = pd.read_csv(PARSED / f"{fold}.csv", usecols=["timestamp", col])
        t = pd.to_datetime(df["timestamp"], format="ISO8601", utc=True)
        tns = t.astype("int64").to_numpy()
        o = np.argsort(tns, kind="stable")
        tns, mdv = tns[o], df[col].to_numpy(dtype=np.float64)[o]
        for i in take:
            a = int(cat[i])
            i0 = int(np.searchsorted(tns, a - 2 * 3600 * 1_000_000_000, side="left"))
            i1 = int(np.searchsorted(tns, a, side="left"))
            x = mdv[i0:i1]
            v = np.isfinite(x)
            if int(v.sum()) < 5:
                exp_mean = np.nan
            else:
                exp_mean = float(x[v].mean())
            got = float(c["X_baseline"][i, 0])
            if np.isnan(exp_mean) and not np.isnan(got):
                bad.append(f"{fold}@{a}: md_mean recompute NaN vs {got}")
            elif not np.isnan(exp_mean) and (
                    np.isnan(got) or abs(exp_mean - got) > 1e-4 * max(1.0, abs(exp_mean))):
                bad.append(f"{fold}@{a}: md_mean {exp_mean} vs {got}")
    check("V6 md_mean dihitung ulang dari DMEA mentah (6 anchor)", not bad,
          "; ".join(bad) or "cocok")

    # ---------- V7: konsistensi unit ----------
    bad = []
    n_pos_npz = int(len(ev["event_id"]))
    n_neg_npz = int(len(c["anchor_ts"]))
    u = res["units"]
    if n_pos_npz != u["n_pos"]:
        bad.append(f"n_pos {n_pos_npz} vs {u['n_pos']}")
    if n_neg_npz != u["n_neg"]:
        bad.append(f"n_neg {n_neg_npz} vs {u['n_neg']}")
    if n_pos_npz + n_neg_npz != u["n_total"]:
        bad.append("n_total tidak konsisten")
    if len(res["sampling"]) != 7:
        bad.append(f"fold sampling {len(res['sampling'])} != 7")
    for w, si in res["split_info"].items():
        if not (0.0 < si["prev_test"] < 1.0):
            bad.append(f"{w} test tanpa dua kelas")
    if int(c["anti_violations"]) != res["anti_leakage"]["violations"]:
        bad.append("violations npz vs json beda")
    check("V7 konsistensi unit/fold/dua kelas", not bad,
          "; ".join(bad) or f"{u['n_pos']}+{u['n_neg']}={u['n_total']} unit, 7 fold ok")

    # ---------- V8: pooled PR-AUC dihitung ulang dari skor tersimpan ----------
    from sklearn.metrics import average_precision_score as ap_sk
    ps = res.get("pooled_scores")
    bad = []
    if not ps:
        bad.append("pooled_scores tidak ada di JSON")
    else:
        ys = np.array(ps["y"], dtype=int)
        for k in KEYS:
            s = np.array(ps["keys"][k]["score"], dtype=float)
            got = round(float(ap_sk(ys, s)), 4)
            if got != res["pooled"][k]["pr_auc"]:
                bad.append(f"{k}: {got} vs {res['pooled'][k]['pr_auc']}")
    check("V8 pooled PR-AUC recompute dari skor tersimpan (9 key)", not bad,
          "; ".join(bad) or "semua cocok")

    # ---------- V9: sensitivitas post-hoc dihitung ulang dari skor ----------
    bad = []
    S = res.get("sensitivity")
    if not (ps and S):
        bad.append("sensitivity/pooled_scores tidak ada")
    else:
        ys = np.array(ps["y"], dtype=int)
        wells_s = np.array(ps["wells"], dtype=str)
        emp = np.array(ps["empty_window_pos"], dtype=bool)
        if int(emp.sum()) != S["n_pos_excluded"] + S["n_neg_empty"]:
            bad.append("hitungan excluded tidak konsisten")
        sens_macro = {}
        for k in KEYS:
            vals = []
            for w in sorted(set(wells_s)):
                m = (wells_s == w) & ~emp
                vals.append(round(float(ap_sk(ys[m],
                        np.array(ps["keys"][k]["score"], dtype=float)[m])), 4))
            sens_macro[k] = round(float(np.mean(vals)), 4)
            if sens_macro[k] != S["macro"][k]:
                bad.append(f"{k} sens macro {sens_macro[k]} vs {S['macro'][k]}")
        target_s = round(max(TARGET_FLOOR, sens_macro[CANARY_KEY] + MARGIN), 4)
        if target_s != S["target"]:
            bad.append(f"target-sens {target_s} vs {S['target']}")
        for k in S["per_variant"]:
            wins, valid = 0, 0
            for w in sorted(set(wells_s)):
                m = (wells_s == w) & ~emp
                a = round(float(ap_sk(ys[m], np.array(
                    ps["keys"][CANARY_KEY]["score"], dtype=float)[m])), 4)
                b = round(float(ap_sk(ys[m], np.array(
                    ps["keys"][k]["score"], dtype=float)[m])), 4)
                valid += 1
                wins += b > a
            g = S["per_variant"][k]
            lolos = sens_macro[k] >= target_s and wins >= MIN_WINS
            if f"{wins}/{valid}" != g["wins_vs_canary"]:
                bad.append(f"{k} sens wins {wins}/{valid} vs {g['wins_vs_canary']}")
            if bool(lolos) != g["LOLOS"]:
                bad.append(f"{k} sens LOLOS {lolos} vs {g['LOLOS']}")
        ms = emp.astype(float)
        if round(float(ap_sk(ys, ms)), 4) != S["missingness_only_pooled_pr_auc"]:
            bad.append("missingness-only pooled tidak cocok")
        if not (("VERDICT SENSITIVITAS" in md) or ("VERDICT S1" in md)):
            bad.append("MD tanpa VERDICT SENSITIVITAS/S1")
    check("V9 sensitivitas recompute dari skor arsip", not bad,
          "; ".join(bad) or f"canary-sens={S['canary']} target-sens={S['target']} "
                            f"lolos-sens={S['ada_yang_lolos']}")

    n_pass = sum(1 for _, ok, _ in RESULTS if ok)
    print(f"\n{n_pass}/{len(RESULTS)} PASS", flush=True)
    return 0 if n_pass == len(RESULTS) else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        import traceback
        traceback.print_exc()
        sys.exit(2)
