#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""code/48_verify_t2e.py — Verifier INDEPENDEN hasil T2-e (kanban t_471b790f).

Jalur kode BERBEDA dari code/46 (menghitung ulang dari sumber primer, bukan
membaca klaim code/46). Verifikasi:

  V1  integritas arsip: sha256 JSON/MD arsip T2-d tidak berubah sejak salinan
  V2  P1: kekosongan jendela dihitung ulang langsung dari npz
      (X_window_meta events + controls) -> cocok kekosongan_jendela + koreksi P1
  V3  P2: subset evaluasi dihitung ulang dari pooled_scores arsip -> cocok koreksi P2
  V4  P3: counter anti-leakage dibaca dari meta T10 + arsip -> cocok koreksi P3
  V5  P7: isi docs/V2_P7_DETERMINISME.json (fit seri==paralel, pred seri==seri,
      paralel!=seri)
  V6  unit P4: n_pos = jumlah event XM[:,0]>0; n_neg = jumlah sampling n_neg;
      TIDAK ADA unit dgn jendela kosong di pooled_scores
  V7  gate dihitung ulang dari tabel fold p4 (canary/target/menang/flag LOLOS)
  V8  pooled PR-AUC dihitung ulang dari pooled_scores p4 per varian
  V9  S1 dihitung ulang dari pooled_scores + pooled_scores_extra (skor out-of-fold)
  V10 S2 missingness-only dihitung ulang dari flag kosong
  V11 MD memuat token kunci & TIDAK memuat string basi desain lama

Keluaran: baris PASS/FAIL + ringkasan "N/N PASS"; exit 0 hanya bila semua PASS.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
from sklearn.metrics import average_precision_score as ap

BASE = Path(__file__).resolve().parents[1]
DOCS = BASE / "docs"
OUT_JSON = DOCS / "V2_ML_BEAT_CANARY_TS.json"
OUT_MD = DOCS / "V2_ML_BEAT_CANARY_TS.md"
ARCH_JSON = DOCS / "V2_ML_BEAT_CANARY_TS_T2D_ARSIP.json"
ARCH_MD = DOCS / "V2_ML_BEAT_CANARY_TS_T2D_ARSIP.md"
P7_JSON = DOCS / "V2_P7_DETERMINISME.json"
EVENTS_NPZ = BASE / "data" / "predictive" / "features_timeseries.npz"
CONTROLS_NPZ = BASE / "data" / "predictive" / "features_timeseries_controls.npz"
META10 = BASE / "data" / "predictive" / "features_timeseries_meta.json"

# sha256 salinan arsip saat dibuat (dicatat dari cp -p + sha256sum, run awal T2-e)
ARCH_SHA256_JSON = "30c84dce7bb4496f7c76a41e6ddcaeba26fd0762a8b64a8b4ee749a91420de97"
ARCH_SHA256_MD = "6cf712775fbc59909bd29a01314e2ecda4ff97b9e6845c231dd96d33a8328d77"

TARGET_FLOOR, MARGIN, MIN_WINS = 0.2465, 0.02, 5
MODELS = ["log", "rf", "hgb"]
SETS = ["G", "E", "F"]
KEYS = [f"{m}_{s}" for s in SETS for m in MODELS]
CANARY_KEY = "log_G"

RESULTS = []


def check(name: str, ok: bool, detail: str = "") -> bool:
    RESULTS.append((name, bool(ok), detail))
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f" — {detail}" if detail else ""),
          flush=True)
    return bool(ok)


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def macro_of(folds: dict) -> dict:
    out = {}
    for k in KEYS:
        vals = [folds[k][w].get("pr_auc") for w in folds[k]
                if folds[k][w].get("pr_auc") is not None]
        out[k] = round(float(np.mean(vals)), 4) if vals else None
    return out


def main() -> int:
    res = json.load(open(OUT_JSON))
    arch = json.load(open(ARCH_JSON))
    md = OUT_MD.read_text(encoding="utf-8")
    p4 = res["p4_desain_baru"]

    # ---------- V1 integritas arsip ----------
    check("V1a sha256 arsip JSON == salinan awal",
          sha256(ARCH_JSON) == ARCH_SHA256_JSON, sha256(ARCH_JSON)[:16])
    check("V1b sha256 arsip MD == salinan awal",
          sha256(ARCH_MD) == ARCH_SHA256_MD, sha256(ARCH_MD)[:16])
    # V1c: blok top-level JSON T2-e = salinan arsip T2-d KECUALI field yang memang
    # dikoreksi P1/P2/P3 (satu angka utk satu pernyataan) + field meta hasil T2-e.
    # Daftar ini tertutup: beda lain = FAIL.
    KOREKSI_IZIN = {
        ("protocol", "deviasi_terdokumentasi"),          # P1: 191 -> 192 + definisi
        ("anti_leakage", "scope"),                       # P3: counter = kontrol saja
        ("sensitivity", "n_eval_neg"),                   # P2: 6618 -> 6617
        ("sensitivity", "n_eval_total"),                 # P2: 7087 (470+6617)
        ("sensitivity", "n_neg_total"),                  # P2: 6618 total negatif
        ("sensitivity", "n_neg_empty_excluded"),         # P2: 1 negatif kosong terbuang
        ("sensitivity", "subset_eval_definisi"),         # P2: definisi subset eksekusi
    }
    bad_v1c = []
    for k, v in arch.items():
        if k in ("generated_at_utc", "task"):
            continue
        if res.get(k) == v:
            continue
        if isinstance(v, dict) and isinstance(res.get(k), dict):
            for kk, vv in v.items():
                if res[k].get(kk) != vv and (k, kk) not in KOREKSI_IZIN:
                    bad_v1c.append(f"{k}.{kk}")
        else:
            bad_v1c.append(k)
    check("V1c blok top-level == arsip T2-d, kecuali koreksi P1/P2/P3 terdaftar",
          not bad_v1c,
          ("beda di luar daftar: " + ", ".join(bad_v1c[:5])) if bad_v1c
          else f"{len(KOREKSI_IZIN)} field koreksi terdaftar, sisanya identik")

    # ---------- V2 P1: kekosongan dihitung ulang dari npz ----------
    z = np.load(EVENTS_NPZ, allow_pickle=True)
    XM = z["X_window_meta"].astype(np.float64)
    XB = z["X_baseline"].astype(np.float64)
    c = np.load(CONTROLS_NPZ, allow_pickle=True)
    XMc = c["X_window_meta"].astype(np.float64)
    XBc = c["X_baseline"].astype(np.float64)
    q = res["kekosongan_jendela"]
    pos2h = int((XM[:, 4] == 0).sum())
    neg2h = int((XMc[:, 4] == 0).sum())
    posG = int((~np.isfinite(XB[:, 0:7])).any(axis=1).sum())
    negG = int((~np.isfinite(XBc[:, 0:7])).any(axis=1).sum())
    check("V2a P1 jumlah jendela-2h kosong (positif)",
          pos2h == q["positif"]["jendela_2h_kosong"] == 191, f"{pos2h}")
    check("V2b P1 jumlah jendela-2h kosong (negatif)",
          neg2h == q["negatif_kontrol_kampanye_asli"]["jendela_2h_kosong"] == 1,
          f"{neg2h}")
    check("V2c P1 total 2h-kosong == total unit NaN varian G",
          pos2h + neg2h == posG + negG == 192, f"{pos2h+neg2h} vs {posG+negG}")
    check("V2d koreksi P1 memuat SATU angka 192 + definisi",
          "192" in res["koreksi_t2e"]["P1"]["baru"]
          and "anchor-2h" in res["koreksi_t2e"]["P1"]["baru"],
          res["koreksi_t2e"]["P1"]["baru"][:90])

    # ---------- V3 P2: subset evaluasi dari pooled_scores arsip ----------
    ps = arch["pooled_scores"]
    y = np.asarray(ps["y"], dtype=int)
    emp = np.asarray(ps["empty_window_pos"], dtype=bool)
    ev_pos, ev_neg = int(((y == 1) & ~emp).sum()), int(((y == 0) & ~emp).sum())
    k2 = res["koreksi_t2e"]["P2"]
    check("V3a P2 n_eval_pos recompute", ev_pos == k2["n_eval_pos"] == 470, f"{ev_pos}")
    check("V3b P2 n_eval_neg recompute (bukan 6618)",
          ev_neg == k2["baru_n_eval_neg"] == 6617, f"{ev_neg}")
    check("V3c P2 n_eval_total + n_neg_total",
          k2["n_eval_total"] == 470 + 6617 and k2["n_neg_total"] == 6618,
          f"{k2['n_eval_total']}/{k2['n_neg_total']}")

    # ---------- V4 P3: counter per cakupan ----------
    meta = json.load(open(META10))
    k3 = res["koreksi_t2e"]["P3"]
    check("V4a P3 counter kontrol == arsip (67.731.473)",
          k3["kontrol"]["rows_scanned"] == arch["anti_leakage"]["rows_scanned"] == 67731473,
          str(k3["kontrol"]["rows_scanned"]))
    check("V4b P3 counter event == meta T10 (bukan 67.731.473)",
          k3["event"]["rows_scanned"] == meta["anti_leakage"]["rows_scanned"] == 4274005
          and k3["event"]["rows_scanned"] != k3["kontrol"]["rows_scanned"],
          str(k3["event"]["rows_scanned"]))
    check("V4c P3 kedua counter violations = 0",
          k3["kontrol"]["violations"] == k3["event"]["violations"] == 0)

    # ---------- V5 P7 ----------
    p7 = json.load(open(P7_JSON))
    h = p7["hasil"]
    check("V5a P7 fit paralel == seri (bitwise)",
          h["B1_vs_C1_fit_paralel_vs_seri"]["identik_bitwise"] is True)
    check("V5b P7 prediksi seri repeat (bitwise)",
          h["B1_vs_B2_prediksi_seri_repeat"]["identik_bitwise"] is True)
    check("V5c P7 prediksi paralel != seri (akar penyebab)",
          h["A1_vs_B1_predict_paralel_vs_seri"]["identik_bitwise"] is False
          and h["A1_vs_B1_predict_paralel_vs_seri"]["n_skor_bedanya"] > 0
          and h["A1_vs_A2_repeat_mode_A_lama"]["n_skor_bedanya"] > 0,
          f"n_bedanya={h['A1_vs_B1_predict_paralel_vs_seri']['n_skor_bedanya']}, "
          f"repeat lama={h['A1_vs_A2_repeat_mode_A_lama']['n_skor_bedanya']}")
    check("V5d kode 46 memakai prediksi serial (rfm.n_jobs=1 setelah fit)",
          "rfm.n_jobs = 1" in (BASE / "code" / "46_beat_canary_ts.py").read_text())

    # ---------- V6 unit P4 ----------
    u = p4["units"]
    avail_pos = int((XM[:, 0] > 0).sum())
    n_neg_json = sum(p4["sampling"][f]["n_neg"] for f in p4["sampling"])
    check("V6a n_pos P4 == jumlah event lolos syarat",
          u["n_pos"] == avail_pos == 467, f"{u['n_pos']} vs {avail_pos}")
    check("V6b n_neg P4 == jumlah sampling n_neg",
          u["n_neg"] == n_neg_json == 3958, f"{u['n_neg']} vs {n_neg_json}")
    check("V6c n_total & prevalensi konsisten",
          u["n_total"] == u["n_pos"] + u["n_neg"]
          and abs(u["prevalence"] - round(u["n_pos"] / u["n_total"], 4)) < 1e-9,
          f"{u['n_total']} prev={u['prevalence']}")
    ps4 = p4["pooled_scores"]
    check("V6d TIDAK ADA unit jendela kosong di pooled_scores P4",
          not any(ps4["empty_window_pos"])
          and p4["diagnostics"]["n_unit_kampanye_jendela_2h_kosong"] == 0
          and p4["diagnostics"]["n_unit_kampanye_jendela_30m_kosong"] == 0)
    ex = p4["pooled_scores_extra"]
    check("V6e extra S1: 194 unit, semua NaN skor == 0",
          len(ex["y"]) == 194 and all(v == 0 for v in ex["n_nan_per_key"].values())
          and all(int(v) == 1 for v in ex["y"]),
          f"n_nan={ex['n_nan_per_key']}")

    # ---------- V7 gate recompute ----------
    g = p4["gate"]
    m = macro_of(p4["folds"])
    ok_m = all(abs((m[k] or 0) - (p4["macro"][k] or 0)) < 1e-9 for k in KEYS)
    check("V7a macro recompute == field macro", ok_m)
    can = m[CANARY_KEY]
    target = round(max(TARGET_FLOOR, (can or 0) + MARGIN), 4)
    check("V7b canary + target recompute",
          abs(can - g["canary_macro"]) < 1e-9 and abs(target - g["target_macro"]) < 1e-9,
          f"canary={can} target={target}")
    wins_ok, flags_ok = True, True
    for k, v in g["per_variant"].items():
        w = sum(1 for x in p4["folds"][CANARY_KEY]
                if p4["folds"][k][x]["pr_auc"] is not None
                and p4["folds"][k][x]["pr_auc"] > p4["folds"][CANARY_KEY][x]["pr_auc"])
        n_valid = sum(1 for x in p4["folds"][CANARY_KEY]
                      if p4["folds"][k][x]["pr_auc"] is not None)
        if w != v["wins_num"] or n_valid != v["n_valid"]:
            wins_ok = False
        if (bool(m[k] is not None and m[k] >= target and w >= MIN_WINS)) != v["LOLOS"]:
            flags_ok = False
    check("V7c menang per varian recompute", wins_ok)
    check("V7d flag LOLOS per varian recompute", flags_ok)

    # ---------- V8 pooled AP recompute ----------
    bad = []
    for k in KEYS:
        yy = np.asarray(ps4["y"], dtype=int)
        ss = np.asarray(ps4["keys"][k]["score"], dtype=float)
        if not np.isfinite(ss).all():
            bad.append(f"{k}:NaN")
            continue
        v = float(ap(yy, ss))
        if abs(v - p4["pooled"][k]["pr_auc"]) > 5e-5:
            bad.append(f"{k}:{v:.4f}!={p4['pooled'][k]['pr_auc']}")
    check("V8 pooled PR-AUC recompute per varian (9/9)", not bad, "; ".join(bad) or "9/9")

    # ---------- V9 S1 recompute dari skor out-of-fold ----------
    sens = p4["sensitivity"]
    yL = np.concatenate([np.asarray(ps4["y"], dtype=int), np.asarray(ex["y"], dtype=int)])
    wL = np.concatenate([np.asarray(ps4["wells"], dtype=object),
                         np.asarray(ex["wells"], dtype=object)])
    bad = []
    for k in KEYS:
        sL = np.concatenate([np.asarray(ps4["keys"][k]["score"], dtype=float),
                             np.asarray(ex["keys"][k]["score"], dtype=float)])
        vals = [float(ap(yL[wL == w], sL[wL == w])) for w in sorted(set(wL))]
        mac = round(float(np.mean(vals)), 4)
        if abs(mac - sens["macro"][k]) > 5e-5:
            bad.append(f"{k}:{mac}!={sens['macro'][k]}")
    check("V9a S1 macro recompute per varian (9/9)", not bad, "; ".join(bad) or "9/9")
    canL = sens["macro"][CANARY_KEY]
    tgtL = round(max(TARGET_FLOOR, (canL or 0) + MARGIN), 4)
    check("V9b S1 canary/target recompute",
          abs(canL - sens["canary"]) < 1e-9 and abs(tgtL - sens["target"]) < 1e-9,
          f"{canL}/{tgtL}")
    flag = any(v["macro"] is not None and v["macro"] >= tgtL and v["wins_num"] >= MIN_WINS
               for v in sens["per_variant"].values())
    check("V9c S1 flag ada_yang_lolos recompute", flag == sens["ada_yang_lolos"],
          str(flag))
    check("V9d S1 set longgar = 661 positif + kontrol P4",
          sens["n_pos_set_panjang"] == 661
          and sens["n_unit_set_panjang"] == 661 + u["n_neg"],
          f"{sens['n_unit_set_panjang']}")

    # ---------- V10 S2 recompute ----------
    emptyL = np.concatenate([np.asarray(ps4["empty_window_pos"], dtype=bool),
                             np.asarray(ex["empty_window_2h"], dtype=bool)])
    mscore = emptyL.astype(float)
    pooled_ms = float(ap(yL, mscore))
    check("V10a S2 pooled missingness-only recompute",
          abs(pooled_ms - sens["missingness_only_pooled_pr_auc"]) < 5e-5,
          f"{pooled_ms:.4f}")
    # flag S2 = jendela 2h kosong; hitung ulang dari array (bukan dari JSON):
    # long set = unit P4 (yg syarat ketersediaan -> 0 kosong) + unit extra (yg
    # gugur; di antaranya 191 kosong-2h, 3 hanya kosong-30m). Negatif long set =
    # kontrol desain baru (semua berdata) -> 0.
    n_flag_pos = int(((yL == 1) & emptyL).sum())
    n_flag_neg = int(((yL == 0) & emptyL).sum())
    check("V10b S2 flag kelas dihitung ulang (pos 191 / neg 0)",
          n_flag_pos == 191 and n_flag_neg == 0
          and sens["n_flag_kosong_pos"] == n_flag_pos
          and sens["n_flag_kosong_neg"] == n_flag_neg,
          f"recompute pos={n_flag_pos} neg={n_flag_neg} | "
          f"JSON pos={sens['n_flag_kosong_pos']} neg={sens['n_flag_kosong_neg']}")

    # ---------- V11 MD ----------
    need = ["T2-e", "DESAIN P4", "192", "6617", "4.274.005", "pra-registrasi",
            "P7", "S1", "pooled_scores_extra", "467", "3958"]
    miss = [t for t in need if t not in md]
    check("V11a MD memuat token kunci T2-e", not miss, f"hilang: {miss}")
    stale = ["185 window kosong T10", "T2-d LOLOS GATE", "n_pos_empty_window",
             "score_pos_empty_window", "Sensitivitas POST-HOC"]
    ada = [t for t in stale if t in md]
    check("V11b MD bebas string basi desain lama", not ada, f"ada: {ada}")
    gtxt = f"{g['canary_macro']:.4f}".replace(".", ",")
    check("V11c MD memuat nilai canary desain P4", gtxt in md, gtxt)

    n_pass = sum(1 for _, ok, _ in RESULTS if ok)
    print(f"\n{n_pass}/{len(RESULTS)} PASS")
    return 0 if n_pass == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
