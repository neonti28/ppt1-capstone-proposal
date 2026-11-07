#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Probe P7: sumber nondeterminisme skor RF (paralelisme n_jobs).

Dilaporkan pada audit t_bdf55b10 sebagai "random forest tanpa random_state"
(padahal random_state=42 sudah di set). Probe ini membedakan 3 hipotesis
dgn pemisahan variabel (semua mode pakai RF params & seed yang sama):

  mode A : fit n_jobs=-1, predict n_jobs=-1   (kondisi kode lama)
  mode B : fit n_jobs=-1, predict n_jobs=+1
  mode C : fit n_jobs=+1, predict n_jobs=+1

Diskriminasi:
  B vs C  -> determinisme FIT paralel vs seri (forest identik? skor identik?)
  B1 vs B2 -> determinisme prediksi SERI (repeat, forest beda proses)
  A1 vs B1 -> efek akumulasi predict_proba PARALEL pada forest yang sama
              (karena fit paralel dibuktikan deterministik lewat B vs C)

Parent mode (tanpa argumen) menjalankan 5 subprocess, membandingkan skor,
lalu menulis docs/V2_P7_DETERMINISME.json (dibaca code/46 utk laporan P7).

Penggunaan:
  python3 code/49_p7_determinisme.py           # probe penuh -> JSON
  python3 code/49_p7_determinisme.py --mode A --rep 1 --npy /tmp/x.npy
"""
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
OUT_JSON = BASE / "docs" / "V2_P7_DETERMINISME.json"
SCRATCH = Path("/home/neonti/.hermes/cache/scratch")

RF_PARAMS = dict(n_estimators=300, class_weight="balanced", min_samples_leaf=2,
                 n_jobs=-1, random_state=42)

MODE_DESC = {
    "A": "fit n_jobs=-1, predict n_jobs=-1 (kondisi kode lama)",
    "B": "fit n_jobs=-1, predict n_jobs=+1 (prediksi serial)",
    "C": "fit n_jobs=+1, predict n_jobs=+1 (prediksi serial + fit serial)",
}


def build_matrix():
    """Unit + split fold persis run_arm (urutan ts; varian G = 7 statistik MD)."""
    from importlib.util import module_from_spec, spec_from_file_location
    z = np.load(BASE / "data/predictive/features_timeseries.npz", allow_pickle=True)
    c = np.load(BASE / "data/predictive/features_timeseries_controls.npz",
                allow_pickle=True)
    spec = spec_from_file_location("ts60", BASE / "code/60_ts_features.py")
    mod = module_from_spec(spec)
    spec.loader.exec_module(mod)

    XB_pos = z["X_baseline"].astype(np.float64)
    XB_neg = c["X_baseline"].astype(np.float64)
    ev_ts = np.array([pd.Timestamp(str(t)).value for t in z["act_start_utc"]],
                     dtype="int64")
    ev_wb = np.array([str(w) for w in z["wellbore"]], dtype=object)
    ctrl_wb = np.array([mod.FOLD2LABEL[str(f)] for f in c["fold"]], dtype=object)
    y = np.concatenate([np.ones(len(ev_ts), dtype=int), c["y"].astype(int)])
    wells = np.concatenate([ev_wb, ctrl_wb])
    ts = np.concatenate([ev_ts, c["anchor_ts"].astype("int64")])
    XG = np.vstack([XB_pos[:, 0:7], XB_neg[:, 0:7]])
    order = np.argsort(ts, kind="stable")
    return XG[order], y[order], wells[order]


def one_run(mode: str, rep: int, npy: str) -> None:
    from sklearn.ensemble import RandomForestClassifier
    X, y, wells = build_matrix()
    # fold uji = fold dgn unit terbanyak (sama utk semua mode -> perbandingan adil)
    w = max(sorted(set(wells)), key=lambda ww: int((wells == ww).sum()))
    te = np.flatnonzero(wells == w)
    rest = np.flatnonzero(wells != w)
    n_va = int(0.15 * len(rest))
    va, tr = rest[-n_va:], rest[:-n_va]
    with np.errstate(all="ignore"):
        med = np.nanmedian(np.where(np.isfinite(X[tr]), X[tr], np.nan), axis=0)
        Xv = np.where(np.isfinite(X), X, med)
    fit_n = 1 if mode == "C" else -1
    rf = RandomForestClassifier(**{**RF_PARAMS, "n_jobs": fit_n})
    rf.fit(Xv[tr], y[tr])
    rf.n_jobs = -1 if mode == "A" else 1    # A: prediksi paralel (kondisi lama)
                                             # B/C: prediksi serial (fix P7)
    proba = rf.predict_proba(Xv[te])[:, 1]
    np.save(npy, proba)
    print(f"MODE {mode} rep {rep} n={len(proba)} -> {npy}", flush=True)


def stats(a: np.ndarray, b: np.ndarray) -> dict:
    d = np.abs(a - b)
    return {"n_skor": int(a.size),
            "n_skor_bedanya": int((d > 0).sum()),
            "max_abs_diff": float(d.max()),
            "identik_bitwise": bool((d == 0).all()),
            "n_flip_di_ambang_05": int(((a >= 0.5) != (b >= 0.5)).sum())}


def parent() -> int:
    SCRATCH.mkdir(parents=True, exist_ok=True)
    X0, y0, wells0 = build_matrix()
    runs = [("A", 1), ("A", 2), ("B", 1), ("B", 2), ("C", 1)]
    npys = {}
    t0 = time.time()
    for mode, rep in runs:
        npy = SCRATCH / f"p7_49_{mode}{rep}.npy"
        cmd = [sys.executable, str(Path(__file__).resolve()),
               "--mode", mode, "--rep", str(rep), "--npy", str(npy)]
        r = subprocess.run(cmd, capture_output=True, text=True)
        print(r.stdout.strip())
        if r.returncode != 0:
            print(r.stderr[-2000:])
            print(f"GAGAL: mode {mode} rep {rep}")
            return 1
        npys[(mode, rep)] = npy
    load = {k: np.load(v) for k, v in npys.items()}

    fit_par = stats(load[("B", 1)], load[("C", 1)])        # fit paralel vs seri
    seri_rep = stats(load[("B", 1)], load[("B", 2)])       # prediksi serial repeat
    pred_par = stats(load[("A", 1)], load[("B", 1)])       # prediksi paralel vs seri
    pred_par2 = stats(load[("A", 1)], load[("A", 2)])      # repeat mode A (kondisi lama)

    all_identik = fit_par["identik_bitwise"] and seri_rep["identik_bitwise"]
    if all_identik and not pred_par["identik_bitwise"]:
        kesimpulan = (
            f"AKAR PENYEBAB = akumulasi predict_proba PARALEL (urutan joblib), "
            f"bukan fit dan bukan random_state: fit paralel==seri bitwise "
            f"({fit_par['n_skor_bedanya']} skor beda), prediksi seri repeat bitwise "
            f"identik ({seri_rep['n_skor_bedanya']} skor beda), sedangkan "
            f"predict n_jobs=-1 vs +1 beda pada {pred_par['n_skor_bedanya']}/"
            f"{pred_par['n_skor']} skor dgn max abs diff {pred_par['max_abs_diff']:.3e} "
            f"(selisih last-bit) → {pred_par['n_flip_di_ambang_05']} skor lewat "
            f"ambang 0,5 saat di-threshold ulang.")
    elif all_identik and pred_par["identik_bitwise"]:
        kesimpulan = ("Semua mode bitwise identik pada probe ini — tidak ada "
                      "nondeterminisme yang teramati pada kondisi ini.")
    else:
        kesimpulan = ("Teramati perbedaan pada kondisi yang seharusnya deterministik "
                      f"(fit_par={fit_par['identik_bitwise']}, "
                      f"seri_repeat={seri_rep['identik_bitwise']}) — selidiki lebih lanjut.")

    out = {
        "probe": "code/49_p7_determinisme.py",
        "verified_at_utc": datetime.now(timezone.utc).isoformat(),
        "runtime_seconds": round(time.time() - t0, 1),
        "rf_params": RF_PARAMS,
        "data": {"sumber": ["data/predictive/features_timeseries.npz",
                            "data/predictive/features_timeseries_controls.npz"],
                 "varian": "G (7 statistik MD jendela 2h)",
                 "n_unit": int(len(y0)),
                 "n_unit_latih": "85% fold bukan uji; val = 15% ekor",
                 "n_fitur": 7},
        "modes": MODE_DESC,
        "hasil": {
            "B1_vs_C1_fit_paralel_vs_seri": fit_par,
            "B1_vs_B2_prediksi_seri_repeat": seri_rep,
            "A1_vs_B1_predict_paralel_vs_seri": pred_par,
            "A1_vs_A2_repeat_mode_A_lama": pred_par2,
        },
        "kesimpulan": kesimpulan,
        "fix": ("code/46: rfm.n_jobs = 1 setelah fit (prediksi serial) — fit tetap "
                "paralel karena dibuktikan deterministik; prediksi 1× per fold tidak "
                "menambah beban berarti"),
        "status": "diukur",
    }
    OUT_JSON.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"JSON ditulis: {OUT_JSON}")
    print("KESIMPULAN:", kesimpulan)
    return 0


if __name__ == "__main__":
    if "--mode" in sys.argv:
        i = sys.argv.index("--mode")
        one_run(sys.argv[i + 1], int(sys.argv[sys.argv.index("--rep") + 1]),
                sys.argv[sys.argv.index("--npy") + 1])
    else:
        sys.exit(parent())
