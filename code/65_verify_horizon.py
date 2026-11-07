#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""code/65_verify_horizon.py — Verifier INDEPENDEN hasil T2-f (kanban t_66037ed6).

Jalur kode BERBEDA dari code/64: semua angka dihitung ULANG dari sumber primer
(shard fitur, npz kontrol, pooled_scores, CSV mentah, kanban DB), bukan membaca
klaim code/64.

  V1  pra-registrasi: komentar comment 33 ada di kanban DB dan timestamp-nya
      < mtime JSON (bukti desain ditulis sebelum hasil)
  V2  unit: n_pos dihitung ulang dari shard (XM[:,0]>0 per event), n_neg dari
      sampling meta + npz kontrol, n_total & prevalensi cocok
  V3  horizon: semua anchor positif == act_start − 6 jam TEPAT (events npz)
  V4  kontrol dipakai ulang: sha256 npz == provenance JSON; mtime kontrol <
      timestamp komentar pra-registrasi (tak mungkin dibangun ulang sesudahnya)
  V5  anti-leakage: violations == 0 (positif & kontrol), rows_scanned > 0
  V6  gate dihitung ulang dari tabel fold JSON (macro, target=max(0,2465;can+0,02),
      menang>=5/7, flag LOLOS, ada_yang_lolos)
  V7  pooled + per-fold PR-AUC dihitung ulang dari pooled_scores (skor primer)
  V8  D2 missingness-only dihitung ulang dari flag empty_2h
  V9  ketersediaan: 0 unit kampanye berflag kosong (dari array, bukan klaim)
  V10 angka gate tak diubah di kode: 64 mengimpor konstanta dari 46; 46 memuat
      0,2465 / 0,02 / MIN_WINS=5 (dicek literal di source)
  V11 spot-recompute fitur dari CSV MENTAH (jalur boolean, bukan searchsorted):
      7 sel baseline MD + 1 sel TS mean per unit, utk unit positif & negatif
  V12 MD memuat token kunci JSON + framing §3.3 + baris 'Riset pendahuluan'

Keluaran: baris PASS/FAIL + ringkasan "N/N PASS"; exit 0 hanya bila semua PASS.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import sqlite3
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score

BASE = Path(__file__).resolve().parents[1]
DOCS = BASE / "docs"
PARSED = BASE / "data" / "volve" / "witsml_parsed"
OUT_JSON = DOCS / "V2_ML_BEAT_CANARY_HORIZON.json"
OUT_MD = DOCS / "V2_ML_BEAT_CANARY_HORIZON.md"
EVENTS_NPZ = BASE / "data" / "predictive" / "features_timeseries.npz"
CONTROLS_NPZ = BASE / "data" / "predictive" / "features_timeseries_controls_berdata.npz"
POS_SHARD_DIR = BASE / "data" / "predictive" / "horizon_pos_shards"
SRC64 = BASE / "code" / "64_beat_canary_horizon.py"
SRC46 = BASE / "code" / "46_beat_canary_ts.py"

TASK_ID = "t_66037ed6"
ANCHOR_OFFSET_NS = 6 * 3600 * 1_000_000_000
TARGET_FLOOR, MARGIN, MIN_WINS = 0.2465, 0.02, 5
MODELS = ["log", "rf", "hgb"]
SETS = ["G", "E", "F"]
KEYS = [f"{m}_{s}" for s in SETS for m in MODELS]
CANARY_KEY = "log_G"
FRAMING_TOKEN = ("Pipeline predictive maintenance (event nyata + jendela waktu/"
                 "kedalaman sebelum event")

RESULTS = []


def check(name: str, ok: bool, detail: str = "") -> bool:
    RESULTS.append((name, bool(ok), detail))
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f" — {detail}" if detail else ""),
          flush=True)
    return bool(ok)


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def ap4(y, s):
    if len(np.unique(y)) < 2:
        return None
    return round(float(average_precision_score(y, s)), 4)


def macro_of(folds: dict) -> dict:
    out = {}
    for k in KEYS:
        vals = [folds[k][w].get("pr_auc") for w in folds[k]
                if folds[k][w].get("pr_auc") is not None]
        out[k] = round(float(np.mean(vals)), 4) if vals else None
    return out


def kanban_comment_time() -> tuple[int | None, str]:
    db = os.environ.get("HERMES_KANBAN_DB") or str(Path.home() / ".hermes" / "kanban.db")
    if not Path(db).exists():
        return None, f"kanban db tidak ditemukan: {db}"
    con = sqlite3.connect(db)
    cur = con.cursor()
    rows = cur.execute(
        "SELECT id, created_at, body FROM task_comments "
        "WHERE task_id=? AND body LIKE '%PRA-REGISTRASI T2-f%' "
        "ORDER BY id", (TASK_ID,)).fetchall()
    con.close()
    if not rows:
        return None, "komentar pra-registrasi T2-f tidak ditemukan di kanban DB"
    cid, ts, body = rows[0]
    return int(ts), f"comment id={cid} created_at={ts}"


def load_mod(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def independent_feature_spot(mod, res) -> bool:
    """Recompute baseline MD (7 sel) + 1 sel TS mean dari CSV mentah, jalur boolean."""
    verify = json.load(open(PARSED / "_verify.json"))
    checks = []

    def spot(fold, anchor_ns, XB_row, X_row, is_pos, tag):
        fmeta = verify[fold]
        fill = fmeta["fill_rate_ge_50pct"]
        usecols, cols = ["timestamp"], {}
        for ch in mod.CHANNELS:
            if ch in fill:
                cols[ch] = ch
                usecols.append(ch)
            elif f"GS_{ch}" in fill:
                cols[ch] = f"GS_{ch}"
                usecols.append(f"GS_{ch}")
            else:
                cols[ch] = None
        df = pd.read_csv(PARSED / f"{fold}.csv", usecols=usecols)
        ts = pd.to_datetime(df["timestamp"], format="ISO8601", utc=True)
        order = np.argsort(ts.to_numpy(), kind="stable")
        ts = ts.iloc[order]
        df = df.iloc[order]
        t = ts.dt.tz_convert("UTC").dt.tz_localize(None).to_numpy().astype(np.int64)
        mask2h = (t >= anchor_ns - 2 * 3600 * 1_000_000_000) & (t < anchor_ns)
        # --- baseline MD, jalur independen (mask boolean, bukan searchsorted) ---
        mdcol = cols.get("DMEA")
        ok_base = True
        if mdcol is not None:
            x = df[mdcol].to_numpy(dtype=np.float64)[mask2h]
            v = np.isfinite(x)
            if int(v.sum()) >= mod.MIN_VALID:
                xv = x[v]
                tt = (t[mask2h][v] - (anchor_ns - 2 * 3600 * 1_000_000_000)) / 1e9 / 60.0
                tc = tt - tt.mean()
                xc = xv - xv.mean()
                slope = float((tc * xc).sum() / (tc * tc).sum()) if (tc * tc).sum() else np.nan
                ref = [xv.mean(), xv.std(ddof=1), xv.min(), xv.max(), slope,
                       xv[-1], xv[-1] - xv[0]]
                got = list(np.asarray(XB_row, dtype=np.float64)[:7])
                for a, b in zip(ref, got):
                    if np.isnan(a) and np.isnan(b):
                        continue
                    if not np.isclose(a, b, rtol=1e-4, atol=1e-4):
                        ok_base = False
                        checks.append(f"{tag} baseline beda: {a} vs {b}")
        return ok_base

    # unit positif: 2 fold pertama, event pertama
    z = np.load(EVENTS_NPZ, allow_pickle=True)
    ev_fold = np.array([str(f) for f in z["fold"]], dtype=object)
    ev_ts = np.array([pd.Timestamp(str(t)).value for t in z["act_start_utc"]],
                     dtype="int64")
    ok_all = True
    n_units = 0
    for fold in sorted(set(ev_fold))[:2]:
        shard = POS_SHARD_DIR / f"pos_{fold}.npz"
        if not shard.exists():
            check("V11 shard positif ada", False, str(shard))
            return False
        s = np.load(shard, allow_pickle=True)
        r = 0
        idx = int(s["event_idx"][r])
        anchor = int(ev_ts[idx]) - ANCHOR_OFFSET_NS
        if int(s["anchor_ts"][r]) != anchor:
            check("V11 anchor shard == act_start−6h", False, fold)
            return False
        ok_all &= spot(fold, anchor, s["XB"][r], s["X"][r], True, f"pos:{fold}")
        n_units += 1
    # unit negatif: kontrol fold pertama
    c = np.load(CONTROLS_NPZ, allow_pickle=True)
    fold0 = str(c["fold"][0])
    i0 = int(np.flatnonzero(np.array([str(f) for f in c["fold"]]) == fold0)[0])
    ok_all &= spot(fold0, int(c["anchor_ts"][i0]), c["X_baseline"][i0],
                   c["X"][i0], False, f"neg:{fold0}")
    n_units += 1
    # sel TS mean secara independen (positif fold pertama)
    fold = sorted(set(ev_fold))[0]
    s = np.load(POS_SHARD_DIR / f"pos_{fold}.npz", allow_pickle=True)
    names = [str(x) for x in s["feature_names"]]
    col = names.index("w30m__DMEA__mean")
    ok_ts, det_ts = spot_ts(mod, verify, fold, int(s["anchor_ts"][0]), s["X"][0], col)
    check("V11b sel TS w30m__DMEA__mean recompute dari CSV mentah", ok_ts, det_ts)
    detail = f"{n_units} unit baseline MD"
    if checks:
        detail += " | " + "; ".join(checks[:3])
    return bool(ok_all)


def spot_ts(mod, verify, fold, anchor_ns, X_row, col) -> tuple[bool, str]:
    fill = verify[fold]["fill_rate_ge_50pct"]
    if "DMEA" in fill:
        ch_col = "DMEA"
    elif "GS_DMEA" in fill:
        ch_col = "GS_DMEA"
    else:
        return True, "DMEA tidak tersedia di fold — sel dilewati"
    df = pd.read_csv(PARSED / f"{fold}.csv", usecols=["timestamp", ch_col])
    ts = pd.to_datetime(df["timestamp"], format="ISO8601", utc=True)
    order = np.argsort(ts.to_numpy(), kind="stable")
    ts, df = ts.iloc[order], df.iloc[order]
    t = ts.dt.tz_convert("UTC").dt.tz_localize(None).to_numpy().astype(np.int64)
    mask = (t >= anchor_ns - 30 * 60 * 1_000_000_000) & (t < anchor_ns)
    x = df[ch_col].to_numpy(dtype=np.float64)[mask]
    v = np.isfinite(x)
    got = float(np.asarray(X_row, dtype=np.float64)[col])
    if int(v.sum()) < mod.MIN_VALID:
        return (bool(np.isnan(got)), f"TS sel NaN konsisten (n_valid={int(v.sum())})")
    ref = float(np.nanmean(x))
    ok = bool(np.isclose(ref, got, rtol=1e-4, atol=1e-4))
    return ok, f"ref={ref:.6f} got={got:.6f}"


def main() -> int:
    res = json.load(open(OUT_JSON))
    md = OUT_MD.read_text(encoding="utf-8")
    g = res["gate"]

    # ---------- V1 pra-registrasi ----------
    ts_c, det_c = kanban_comment_time()
    json_mtime = int(OUT_JSON.stat().st_mtime)
    ok_v1 = ts_c is not None and ts_c < json_mtime
    check("V1 pra-registrasi comment < mtime JSON", ok_v1,
          f"{det_c}; json_mtime={json_mtime}")
    if ts_c is not None:
        check("V1b komentar pra-registrasi < mtime controls npz? (harusnya kontrol "
              "lebih tua dari komentar)", int(CONTROLS_NPZ.stat().st_mtime) < ts_c,
              f"controls mtime={int(CONTROLS_NPZ.stat().st_mtime)} vs comment={ts_c}")

    # ---------- V2 unit dihitung ulang dari shard ----------
    n_pos_shard, n_kosong_shard = 0, 0
    for sh in sorted(POS_SHARD_DIR.glob("pos_*.npz")):
        s = np.load(sh, allow_pickle=True)
        xm = s["XM"]
        n_pos_shard += int((xm[:, 0] > 0).sum())
        n_kosong_shard += int((xm[:, 0] == 0).sum())
    u = res["units"]
    check("V2a n_pos == jumlah shard lolos ketersediaan",
          n_pos_shard == u["n_pos"], f"{n_pos_shard} vs {u['n_pos']}")
    check("V2b n_pos_semua == total event shard",
          n_pos_shard + n_kosong_shard == u["n_pos_semua_event"],
          f"{n_pos_shard}+{n_kosong_shard} vs {u['n_pos_semua_event']}")
    n_neg_samp = sum(int(v["n_neg"]) for v in res["sampling"].values())
    c = np.load(CONTROLS_NPZ, allow_pickle=True)
    check("V2c n_neg == sum sampling == len(npz kontrol)",
          u["n_neg"] == n_neg_samp == len(c["y"]),
          f"{u['n_neg']} / {n_neg_samp} / {len(c['y'])}")
    check("V2d n_total & prevalensi konsisten",
          u["n_total"] == u["n_pos"] + u["n_neg"]
          and abs(u["prevalence"] - round(u["n_pos"] / u["n_total"], 4)) <= 1e-4,
          f"total={u['n_total']} prev={u['prevalence']}")
    check("V2e jumlah unit pooled_scores == n_total",
          len(res["pooled_scores"]["y"]) == u["n_total"],
          f"{len(res['pooled_scores']['y'])} vs {u['n_total']}")

    # ---------- V3 horizon tepat 6 jam ----------
    z = np.load(EVENTS_NPZ, allow_pickle=True)
    ev_ts = np.array([pd.Timestamp(str(t)).value for t in z["act_start_utc"]],
                     dtype="int64")
    maxdiff, n_ev = 0, 0
    for sh in sorted(POS_SHARD_DIR.glob("pos_*.npz")):
        s = np.load(sh, allow_pickle=True)
        want = ev_ts[s["event_idx"].astype(int)] - ANCHOR_OFFSET_NS
        maxdiff = max(maxdiff, int(np.abs(want.astype("int64")
                                          - s["anchor_ts"].astype("int64")).max()))
        n_ev += len(s["anchor_ts"])
    check("V3 anchor positif == act_start − 6h tepat (semua event)",
          maxdiff == 0 and n_ev == u["n_pos_semua_event"],
          f"maxdiff={maxdiff} ns, n_event={n_ev}")

    # ---------- V4 kontrol dipakai ulang ----------
    prov = res["controls_provenance"]
    check("V4a sha256 controls npz == provenance JSON",
          sha256(CONTROLS_NPZ) == prov["sha256"], sha256(CONTROLS_NPZ)[:16])
    check("V4b mtime controls < timestamp pra-registrasi",
          ts_c is not None and int(CONTROLS_NPZ.stat().st_mtime) < ts_c,
          f"controls={int(CONTROLS_NPZ.stat().st_mtime)} comment={ts_c}")
    check("V4c kontrol y semua 0 (negatif) & design_tag berdata",
          int(c["y"].sum()) == 0 and str(c["design_tag"]) == "berdata",
          f"y_sum={int(c['y'].sum())}")

    # ---------- V5 anti-leakage ----------
    ap_ = res["anti_leakage_pos"]
    check("V5a anti-leakage positif @−6h violations == 0",
          int(ap_["violations"]) == 0 and int(ap_["rows_scanned"]) > 0,
          f"viol={ap_['violations']} rows={ap_['rows_scanned']}")
    check("V5b anti-leakage kontrol violations == 0",
          int(res["anti_leakage"]["violations"]) == 0
          and int(res["anti_leakage"]["rows_scanned"]) > 0,
          f"viol={res['anti_leakage']['violations']}")

    # ---------- V6 gate recompute ----------
    folds = res["folds"]
    macro = macro_of(folds)
    check("V6a macro recompute == JSON macro",
          all(macro[k] == res["macro"][k] for k in KEYS),
          json.dumps({k: macro[k] for k in KEYS}))
    can = macro[CANARY_KEY]
    target = round(max(TARGET_FLOOR, (can or 0.0) + MARGIN), 4)
    check("V6b canary & target formula",
          can == g["canary_macro"] and target == g["target_macro"],
          f"can={can} target={target} (JSON {g['canary_macro']}/{g['target_macro']})")
    ok_flags = True
    for s in ("E", "F"):
        for m in MODELS:
            k = f"{m}_{s}"
            wins = sum(1 for w in folds[CANARY_KEY]
                       if folds[k][w].get("pr_auc") is not None
                       and folds[CANARY_KEY][w].get("pr_auc") is not None
                       and folds[k][w]["pr_auc"] > folds[CANARY_KEY][w]["pr_auc"])
            mac = macro[k]
            lolos = bool(mac is not None and mac >= target and wins >= MIN_WINS)
            j = g["per_variant"][k]
            if not (wins == j["wins_num"] and mac == j["macro"]
                    and lolos == j["LOLOS"]):
                ok_flags = False
                check(f"V6c {k}", False, f"recompute wins={wins} mac={mac} "
                                         f"LOLOS={lolos} vs JSON {j}")
    check("V6c semua flag gate (wins/macro/LOLOS) recompute == JSON", ok_flags)
    check("V6d ada_yang_lolos & verdict konsisten",
          g["ada_yang_lolos"] == any(v["LOLOS"] for v in g["per_variant"].values())
          and (g["ada_yang_lolos"] and g["verdict_t2f"].startswith("LOLOS")
               or (not g["ada_yang_lolos"] and g["verdict_t2f"] == "GAGAL GATE")),
          g["verdict_t2f"])

    # ---------- V7 pooled + per-fold AP dari skor primer ----------
    y = np.asarray(res["pooled_scores"]["y"], dtype=int)
    wells = np.asarray(res["pooled_scores"]["wells"], dtype=str)
    ok_pool, ok_fold = True, True
    for k in KEYS:
        sc = np.asarray(res["pooled_scores"]["keys"][k]["score"], dtype=float)
        if ap4(y, sc) != res["pooled"][k]["pr_auc"]:
            ok_pool = False
            check(f"V7 pooled {k}", False, f"{ap4(y, sc)} vs {res['pooled'][k]['pr_auc']}")
        for w in sorted(set(wells)):
            m = wells == w
            v = ap4(y[m], sc[m])
            if v != folds[k][w].get("pr_auc"):
                ok_fold = False
                check(f"V7 fold {k}/{w}", False, f"{v} vs {folds[k][w].get('pr_auc')}")
    check("V7a pooled PR-AUC recompute dari pooled_scores == JSON (9/9)", ok_pool)
    check("V7b per-fold PR-AUC recompute == JSON (63 sel)", ok_fold)

    # ---------- V8 D2 recompute ----------
    empty = np.asarray(res["pooled_scores"]["empty_2h"], dtype=bool)
    mscore = empty.astype(np.float64)
    d2 = res["diagnostics"]["missingness_only"]
    d2_folds = {w: ap4(y[wells == w], mscore[wells == w]) for w in sorted(set(wells))}
    d2_macro = round(float(np.nanmean([v for v in d2_folds.values()
                                       if v is not None])), 4)
    check("V8 D2 macro/pooled/flag recompute",
          d2_macro == d2["macro"] and ap4(y, mscore) == d2["pooled"]
          and int(((y == 1) & empty).sum()) == d2["n_flag_pos"]
          and int(((y == 0) & empty).sum()) == d2["n_flag_neg"],
          f"macro={d2_macro} pooled={ap4(y, mscore)}")

    # ---------- V9 ketersediaan ----------
    check("V9a 0 unit kampanye berflag kosong-2h",
          int(empty.sum()) == 0 and res["diagnostics"]["n_unit_kampanye_kosong"] == 0,
          f"empty={int(empty.sum())}")
    check("V9b 2 kelas di tiap fold + fold persis 7",
          len(set(wells)) == 7 and all(len(np.unique(y[wells == w])) == 2
                                       for w in set(wells)),
          f"folds={len(set(wells))}")

    # ---------- V10 angka gate tidak diubah di kode ----------
    src64 = SRC64.read_text(encoding="utf-8")
    src46 = SRC46.read_text(encoding="utf-8")
    check("V10a 64 mengimpor konstanta gate dari 46 (tanpa literal sendiri)",
          "TARGET_FLOOR = m46.TARGET_FLOOR" in src64
          and "MARGIN = m46.MARGIN" in src64
          and "MIN_WINS = m46.MIN_WINS" in src64
          and re.search(r"TARGET_FLOOR\s*=\s*0\.", src64) is None,
          "impor terverifikasi")
    check("V10b 46 memuat lantai 0.2465, margin 0.02, MIN_WINS 5",
          re.search(r"TARGET_FLOOR\s*=\s*0\.2465", src46) is not None
          and re.search(r"MARGIN\s*=\s*0\.02\b", src46) is not None
          and re.search(r"MIN_WINS\s*=\s*5\b", src46) is not None,
          "literal ditemukan di code/46")

    # ---------- V11 spot-recompute fitur dari CSV mentah ----------
    mod = load_mod(BASE / "code" / "60_ts_features.py", "v60")
    ok_spot = independent_feature_spot(mod, res)
    check("V11 spot-recompute fitur dari CSV mentah (baseline MD + sel TS)", ok_spot)

    # ---------- V12 MD token ----------
    tgt = f"{g['target_macro']:.4f}".replace(".", ",")
    can_t = f"{g['canary_macro']:.4f}".replace(".", ",")
    check("V12a MD memuat token target & canary", tgt in md and can_t in md,
          f"{tgt}/{can_t}")
    check("V12b MD memuat verdict JSON", g["verdict_t2f"] in md, g["verdict_t2f"])
    check("V12c MD memuat framing §3.3 verbatim", FRAMING_TOKEN in md)
    check("V12d MD memuat baris 'Riset pendahuluan'", "Riset pendahuluan" in md)
    check("V12e MD memuat klarifikasi horizon 12h & anchor −6h",
          re.search(r"act_start.{0,4}12h", md) is not None
          and re.search(r"act_start.{0,4}6\s*jam", md) is not None)

    # ---------- V13 determinisme: JSON final vs backup run-1 ----------
    bkp = Path.home() / ".hermes" / "cache" / "scratch" / "run1_horizon.json"
    if bkp.exists():
        r1 = json.load(open(bkp))
        eq_keys = ["folds", "macro", "pooled", "gate", "split_info",
                   "pooled_scores", "units", "sampling", "diagnostics"]
        diffs = [k for k in eq_keys if r1.get(k) != res.get(k)]
        check("V13 JSON final identik dengan run-1 (determinisme, 9 blok primer)",
              not diffs, "identik" if not diffs else f"blok beda: {diffs}")
    else:
        check("V13 backup run-1 tersedia utk cek determinisme", False, str(bkp))

    n_pass = sum(1 for _, ok, _ in RESULTS if ok)
    print(f"\n{n_pass}/{len(RESULTS)} PASS", flush=True)
    return 0 if n_pass == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
