#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
code/44a_build_new_features.py — Tahap WAJIB sebelum kampanye T2c (kanban t_33cc76d7):
(a) VERIFIKASI berkas sumber (sha256, jumlah baris, pemetaan wellbore, konsistensi md)
(b) AUDIT FILL-RATE kolom raw USROP (data/USROP/Code/Norway*.csv) — aturan task:
    kolom fill-rate <50% JANGAN dipakai kecuali dijustifikasi; keputusan dicatat.
    Definisi fill (diukur, ditemukan dari struktur file): tiap kolom punya grid sampel
    sendiri (dekadium 0,15–1,0 m) sementara grid dataset 0,05 m — karena itu fill =
    fraksi baris dataset yang punya sampel non-null TERAKHIR sebelum md dalam 1,0 m
    (backward/tanpa look-ahead, konsisten dgn fitur lama `last_*`).
(c) BUILD matriks fitur BARU -> data/predictive/features_v2.npz + features_v2_meta.json

Mode:
  --audit   : hanya (a)+(b) -> docs/V2_USROP_FILLRATE.json (TANPA menulis npz)
  default   : (a)+(b)+(c)

Sumber fitur baru (semua diverifikasi ada di disk oleh skrip ini):
  1. Norway*.csv (7 file)      -> fitur raw/prekursor, join md terdekat tol 0,1 m
  2. Well_picks_Volve_v1.dat   -> fitur "formasi/zone pada md ini" (tops per wellbore)
  3. DLIS/LIS log petrofisik   -> kurva geologi per md (gamma/rhob/nphi/res/pef/drho)
  4. LAS 2.0 F-15 D            -> diverifikasi & DILAPORKAN (wellbore tidak ada di dataset)

SELEKSI FITUR = label-free (fill-rate + blocklist struktural) — TIDAK memakai y_10/y_30.
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import re
import sys
import time
import traceback
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
DS_PATH = BASE / "data" / "predictive" / "dataset_prediktif.csv"
RAW_DIR = BASE / "data" / "USROP" / "Code"
PICKS = BASE / "data" / "volve" / "external" / "spwla_volve_logs" / "Well_picks_Volve_v1.dat"
LOG_DIR = BASE / "data" / "volve" / "external" / "spwla_volve_logs"
OUT_JSON = BASE / "docs" / "V2_USROP_FILLRATE.json"
OUT_NPZ = BASE / "data" / "predictive" / "features_v2.npz"
OUT_META = BASE / "data" / "predictive" / "features_v2_meta.json"

MD_TOL_RAW = 0.1      # meter; jarak md terdekat terukur maks 0.067 m (probe join)
MD_TOL_LOG = 1.0      # meter; sampling log 0,1524 m (0,5 ft)
# Fill/nilai raw memakai sampel non-null TERAKHIR sebelum md (backward) — TANPA look-ahead,
# konsisten dengan fitur lama `last_*` (jendela ke belakang). Toleransi 1,0 m:
#   ~1/10 dari jendela utama Δ=10 m, menutup dekadium sampling mentah (median gap 0,15–1,0 m).
TOL_BACK = 1.0
# Filter korupsi penyimpanan (ditemukan di file F-15: 120 sel SPP dgn nilai s/d 1,3e32 kPa —
# tidak fisika). Ambang 1e12 jauh di atas semua kanal di file ini (termasuk kumulatif:
# Total Bit Revolutions maks terukur 2,5e6; Total Strokes 1,07e6) -> aman untuk semua kolom.
HARD_CAP = 1e12

# Pemetaan well dataset (kolom `well`) -> file Norway. Diverifikasi lewat rentang md + kolom nameWellbore.
WELL2FILE = {
    "USROP_A 0 N-NA_F-9_Ad.csv": "Norway-NA-15_$47$_9-F-9 A depth.csv",
    "USROP_A 1 N-S_F-7d.csv": "Norway-Statoil-15_$47$_9-F-7 depth.csv",
    "USROP_A 2 N-SH_F-14d.csv": "Norway-StatoilHydro-15_$47$_9-F-14 depth.csv",
    "USROP_A 3 N-SH-F-15d.csv": "Norway-StatoilHydro-15_$47$_9-F-15 depth .csv",
    "USROP_A 4 N-SH_F-15Sd.csv": "Norway-StatoilHydro-15_$47$_9-F-15S depth.csv",
    "USROP_A 5 N-SH-F-5d.csv": "Norway-StatoilHydro-15_$47$_9-F-5 depth.csv",
    "USROP_A 6 N-SH_F-9d.csv": "Norway-StatoilHydro-15_$47$_9-F-9 depth.csv",
}
# wellbore (kolom dataset) yang diharapkan per well — untuk cek silang file
WELL2EXPECTED_WELLBORE = {
    "USROP_A 0 N-NA_F-9_Ad.csv": "NO 15/9-F-9 A",
    "USROP_A 1 N-S_F-7d.csv": "NO 15/9-F-7",
    "USROP_A 2 N-SH_F-14d.csv": "NO 15/9-F-14",
    "USROP_A 3 N-SH-F-15d.csv": "NO 15/9-F-15 A",
    "USROP_A 4 N-SH_F-15Sd.csv": "NO 15/9-F-15",
    "USROP_A 5 N-SH-F-5d.csv": "NO 15/9-F-5",
    "USROP_A 6 N-SH_F-9d.csv": "NO 15/9-F-9",
}

# --- Blocklist struktural (ALASAN dicatat; tanpa label) --------------------
BLOCKLIST_EXACT = {"Unnamed: 0", "Measured Depth m", "name", "nameWellbore",
                   "Pass Name unitless", "Bit run number unitless"}
BLOCKLIST_SUBSTR = ["depth", "tvd"]   # md/tvd/bit-depth = posisi murni (baseline sudah `md`)
# Kandidat prekursor fisik yang DISEBUT task (dilaporkan fill-rate-nya terpisah,
# terlepas dari lolos/tidak seleksi)
CANDIDATE_PATTERNS = {
    "stuck_rt": r"STUCK_RT",
    "mwd_total_shocks": r"MWD Total Shocks",
    "shock_rate": r"Shock Rate",
    "mwd_turbine_rpm": r"Turbine RPM",
    "mudpit_tank_volume": r"Pit|Tank Volume",
    "spp_standpipe": r"Standpipe",
    "flow": r"Flow",
    "gas_chromatography": r"butane|Butane|Pentane|Pent|C1\b|C3\b|C4\b|C5\b|Gas",
    "bit_drill_time": r"Bit Drill Time",
    "total_bit_revolutions": r"Total Bit Revolutions",
}
FILL_MIN = 0.50
MIN_WELLS_AT_FILL = 5   # >=50% fill di >=5/7 wellbore

# --- Geologi --------------------------------------------------------------
CURVE_CANDIDATES = {
    "log_gamma": ["GR", "GR_ARC", "GR_ARC_FILT", "GRM1"],
    "log_rhob": ["RHOB"],
    "log_nphi": ["NPHI", "TNPH", "BPHI"],
    "log_res_deep": ["RT", "RD", "A40H", "P40H"],
    "log_pef": ["PEF"],
    "log_drho": ["DRHO"],
}
# file log per wellbore dataset (diverifikasi terhadap kolom `wellbore`)
WELLBORE2LOG = {
    "NO 15/9-F-5": ["15_9-F-5__WLC_PETROPHYSICAL_COMPOSITE_1.DLIS"],
    "NO 15/9-F-9": ["15_9-F-9__WLC_PETROPHYSICAL_COMPOSITE_1.DLIS"],
    "NO 15/9-F-9 A": ["15_9-F-9A__WLC_PETROPHYSICAL_COMPOSITE_1.DLIS"],
    "NO 15/9-F-14": ["15_9-F14__WLC_PETRO_COMPUTED_INPUT_1.DLIS"],
    "NO 15/9-F-15 A": ["15_9-F15A__WLC_PETROPHYSICAL_COMPOSITE_2.DLIS"],
    "NO 15/9-F-15": ["15_9-F15__WLC_PETROPHYSICAL_COMPOSITE_2.DLIS"],
    "NO 15/9-F-7": ["15_9-F-7__WLC_PETROPHYSICAL_COMPOSITE_1.LIS"],  # diperkirakan gagal load
}
LAS_FILE = "15_9-F15D__WLC_PETRO_COMPUTED_INPUT_1.LAS"

NO_PICK = "__UNASSIGNED__"


def log(m: str = "") -> None:
    print(m, flush=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def nearest_idx(sorted_md: np.ndarray, sorted_orig: np.ndarray, q: np.ndarray, tol: float):
    """Index baris TERDEKAT untuk tiap q, dikembalikan dalam INDEKS ORISINAL
    (indeks ke array sebelum diurutkan; sorted_orig = argsort). tol -> -1 bila tak ada."""
    out = np.full(len(q), -1, dtype=np.int64)
    if len(sorted_md) == 0:
        return out, np.full(len(q), np.inf)
    pos = np.searchsorted(sorted_md, q)
    pos = np.clip(pos, 1, len(sorted_md) - 1)
    lo = pos - 1
    hi = pos
    d_lo = np.abs(sorted_md[lo] - q)
    d_hi = np.abs(sorted_md[hi] - q)
    take_hi = d_hi < d_lo
    best_sorted = np.where(take_hi, hi, lo)
    dist = np.where(take_hi, d_hi, d_lo)
    # tie (jarak sama) -> pilih baris awal (orig lebih kecil)
    tie = (d_hi == d_lo) & (sorted_orig[lo] <= sorted_orig[hi])
    best_sorted = np.where(tie, lo, best_sorted)
    dist = np.where(tie, d_lo, dist)
    best = sorted_orig[best_sorted]
    out[dist <= tol] = best[dist <= tol]
    return out, dist


def backward_values(md_all: np.ndarray, val: np.ndarray, q: np.ndarray, tol: float):
    """Nilai terakhir yang diketahui SEBELUM md baris (backward, causal).
    md_all/val = seluruh baris file; q = md dataset. Return (values, gap).
    gap = q - md_sampel terakhir (inf bila tak ada sampel sebelum q).
    Sel: md valid, nilai finite, dan |nilai| <= HARD_CAP (filter korupsi)."""
    n = len(q)
    m = np.isfinite(md_all) & np.isfinite(val) & (np.abs(val) <= HARD_CAP)
    if not m.any():
        return np.full(n, np.nan), np.full(n, np.inf)
    md_c = md_all[m]
    v_c = val[m]
    o = np.argsort(md_c, kind="stable")
    s = md_c[o]
    vs = v_c[o]
    pos = np.searchsorted(s, q, side="right") - 1
    ok = pos >= 0
    gap = np.full(n, np.inf)
    gap[ok] = q[ok] - s[pos[ok]]
    vals = np.full(n, np.nan)
    hit = ok & (gap <= tol)
    p = np.clip(pos, 0, len(s) - 1)
    vals[hit] = vs[p[hit]]
    return vals, gap


def load_dataset() -> pd.DataFrame:
    ds = pd.read_csv(DS_PATH, low_memory=False)
    need = {"row_id", "well", "wellbore", "md", "est_timestamp", "y_10", "y_30"}
    miss = need - set(ds.columns)
    if miss:
        raise SystemExit(f"dataset_prediktif.csv kekurangan kolom: {sorted(miss)}")
    return ds


def verify_sources(ds: pd.DataFrame) -> dict:
    """(a) Verifikasi berkas: ada, sha256, jumlah baris, pemetaan wellbore, rentang md."""
    out = {"files": {}, "checks": []}
    ok = True
    for well, fname in WELL2FILE.items():
        p = RAW_DIR / fname
        if not p.exists():
            ok = False
            out["checks"].append({"check": f"file_ada:{fname}", "pass": False, "note": "TIDAK ADA"})
            continue
        log(f"  sha256 {fname[:48]:48s} ...")
        out["files"][fname] = {"bytes": p.stat().st_size, "sha256": sha256(p)}
    for extra in [PICKS, LOG_DIR / LAS_FILE]:
        if extra.exists():
            out["files"][extra.name] = {"bytes": extra.stat().st_size, "sha256": sha256(extra)}
        else:
            ok = False
            out["checks"].append({"check": f"file_ada:{extra.name}", "pass": False, "note": "TIDAK ADA"})
    # baris dataset per well + rentang md
    for well, sub in ds.groupby("well"):
        out["checks"].append({
            "check": f"dataset_rows:{well}", "pass": True,
            "n": int(len(sub)),
            "md_range": [round(float(sub["md"].min()), 3), round(float(sub["md"].max()), 3)],
            "wellbore": sorted(set(sub["wellbore"]))[0]})
    out["all_files_present"] = ok
    return out


def audit_raw_fillrate(ds: pd.DataFrame) -> dict:
    """(b) Fill-rate per kolom: pooled + per wellbore (join md terdekat). Tanpa label."""
    n_by_well = ds["well"].value_counts().to_dict()
    fill_num: dict[str, dict] = {}     # col -> {well: (nonnull, n)}
    meta: dict[str, dict] = {}         # col -> {well: {n_sampel, med_gap, md_range}}
    present_in: dict[str, set] = {}
    nonnum: dict[str, int] = {}
    cand_hits: dict[str, list] = {k: [] for k in CANDIDATE_PATTERNS}
    join_info = {}
    names_check = {}

    for well, fname in WELL2FILE.items():
        p = RAW_DIR / fname
        sub = ds[ds["well"] == well]
        md_q = sub["md"].to_numpy(float)
        df = pd.read_csv(p, low_memory=False)
        # verifikasi pemetaan file <-> wellbore lewat kolom identitas bila ada
        ident = {}
        for c in ("name", "nameWellbore"):
            if c in df.columns:
                vals = sorted({str(v) for v in df[c].dropna().unique()})[:5]
                ident[c] = vals
        names_check[well] = {"expected_wellbore": WELL2EXPECTED_WELLBORE[well],
                             "identitas_di_file": ident}
        if "Measured Depth m" not in df.columns:
            join_info[well] = {"error": "kolom 'Measured Depth m' tidak ada"}
            continue
        raw_md = pd.to_numeric(df["Measured Depth m"], errors="coerce").to_numpy(float)
        okm = np.isfinite(raw_md)
        md_full = raw_md                 # untuk backward join (pakai seluruh baris)
        raw_md_sorted_src = raw_md[okm]
        order = np.argsort(raw_md_sorted_src, kind="stable")
        sorted_md = raw_md_sorted_src[order]
        sorted_orig = order  # indeks relatif urut md; tie -> urutan awal stabil
        idx, dist = nearest_idx(sorted_md, sorted_orig, md_q, MD_TOL_RAW)
        matched = idx >= 0
        join_info[well] = {
            "n_rows_dataset": int(len(md_q)),
            "matched": int(matched.sum()),
            "match_rate": round(float(matched.mean()), 4),
            "dist_median": round(float(np.median(dist)), 5),
            "dist_max": round(float(dist.max()), 5),
            "dist_max_tertol": round(float(dist[matched].max()), 5) if matched.any() else None,
            "n_rows_file": int(len(df)),
            "n_unique_md_file": int(len(np.unique(raw_md_sorted_src))),
            "n_dup_md_file": int(len(raw_md_sorted_src) - len(np.unique(raw_md_sorted_src))),
            "md_file_range": [round(float(raw_md_sorted_src.min()), 3),
                              round(float(raw_md_sorted_src.max()), 3)],
            "catatan_join": "match_rate = penjajaran grid md file vs dataset (bukan fill fitur); "
                            "fill fitur = backward_values (sampel non-null terakhir sebelum md, "
                            f"tol {TOL_BACK} m)",
        }
        for c in df.columns:
            if c == "Measured Depth m":
                continue
            s = df[c]
            num = pd.to_numeric(s, errors="coerce")
            nnum_bad = int(s.notna().sum() - num.notna().sum())
            if num.notna().sum() == 0:
                # kolom non-numerik sepenuhnya (identitas/teks)
                nonnum[c] = nonnum.get(c, 0) + 1
                continue
            nv = num.to_numpy(float)
            vals, gap = backward_values(md_full, nv, md_q, TOL_BACK)
            nn = int(np.isfinite(vals).sum())
            samp_md = md_full[np.isfinite(md_full) & np.isfinite(nv)]
            gaps = np.diff(np.sort(samp_md))
            fill_num.setdefault(c, {})[well] = (nn, int(len(md_q)))
            meta.setdefault(c, {})[well] = {
                "n_sampel": int(len(samp_md)),
                "med_gap": round(float(np.median(gaps)), 3) if len(gaps) else None,
                "md_range": [round(float(samp_md.min()), 2), round(float(samp_md.max()), 2)]
                            if len(samp_md) else None,
            }
            present_in.setdefault(c, set()).add(well)
            if nnum_bad:
                nonnum[f"{c}::nonnum_cells"] = nonnum.get(f"{c}::nonnum_cells", 0) + nnum_bad
        del df
        log(f"  audited {fname[:46]:46s} matched={join_info[well]['match_rate']:.3f}")

    # pooled fill-rate = total sel terisi / SELURUH baris dataset (file tanpa kolom = 0,
    # sebelumnya salah pakai penyebut parsial -> fill ter-inflasi; diverifikasi ulang)
    n_total_ds = int(len(ds))
    table = {}
    for c, per in fill_num.items():
        nn = sum(v[0] for v in per.values())
        pooled = nn / n_total_ds if n_total_ds else 0.0
        wells_ok = [w for w, (a, b) in per.items() if b > 0 and a / b >= FILL_MIN]
        table[c] = {
            "fill_pooled": round(pooled, 4),
            "fill_per_well": {w: (round(per[w][0] / per[w][1], 4) if w in per and per[w][1] else 0.0)
                              for w in WELL2FILE},
            "n_wells_ge_50": len(wells_ok),
            "present_files": sorted(per.keys()),
        }
    # kandidat yang DISEBUT task
    task_candidates = {}
    for key, pat in CANDIDATE_PATTERNS.items():
        hits = {c: table[c] for c in table if re.search(pat, c)}
        task_candidates[key] = {c: {"fill_pooled": v["fill_pooled"],
                                    "n_wells_ge_50": v["n_wells_ge_50"]}
                                for c, v in hits.items()}
    return {"join": join_info, "fillrate": table, "task_candidates": task_candidates,
            "identity_check": names_check, "column_meta": meta,
            "non_numeric_columns": sorted(
                [c for c in table if False]) ,
            "columns_seen_non_numeric": sorted(set(nonnum)),
            "n_numeric_columns_audited": len(table)}


def select_columns(fillrate: dict) -> dict:
    """Seleksi label-free: blocklist -> fill>=50% pooled -> fill>=50% di >=5/7 well -> non-konstan."""
    kept, dropped = [], []
    for c, v in fillrate.items():
        reasons = []
        if c in BLOCKLIST_EXACT:
            reasons.append("blocklist:identitas/param-posisi")
        elif any(s in c.lower() for s in BLOCKLIST_SUBSTR):
            reasons.append("blocklist:kolom-kedalaman/posisi (baseline md sudah ada)")
        if not reasons:
            if v["fill_pooled"] < FILL_MIN:
                reasons.append(f"fill_pooled {v['fill_pooled']} < {FILL_MIN}")
            elif v["n_wells_ge_50"] < MIN_WELLS_AT_FILL:
                reasons.append(f"fill>=50% hanya di {v['n_wells_ge_50']}/{MIN_WELLS_AT_FILL} wellbore")
        if reasons:
            dropped.append({"column": c, "reason": "; ".join(reasons),
                            "fill_pooled": v["fill_pooled"],
                            "n_wells_ge_50": v["n_wells_ge_50"]})
        else:
            kept.append(c)
    return {"kept": sorted(kept), "dropped": dropped}


def build_raw_matrix(ds: pd.DataFrame, kept: list[str]) -> tuple[np.ndarray, list, dict]:
    """Pass 2: baca ulang file, isi matriks 198.927 x len(kept) (float32, NaN = tak terisi).
    Nilai = sampel non-null TERAKHIR sebelum md (backward, tol TOL_BACK) — sama dgn audit."""
    n = len(ds)
    X = np.full((n, len(kept)), np.nan, dtype=np.float32)
    col_index = {c: i for i, c in enumerate(kept)}
    stats = {}
    for well, fname in WELL2FILE.items():
        pos = np.flatnonzero(ds["well"].to_numpy() == well)
        md_q = ds["md"].to_numpy(float)[pos]
        df = pd.read_csv(RAW_DIR / fname, low_memory=False)
        md_full = pd.to_numeric(df["Measured Depth m"], errors="coerce").to_numpy(float)
        got = 0
        n_fill = 0
        for c in kept:
            if c not in df.columns:
                continue
            v = pd.to_numeric(df[c], errors="coerce").to_numpy(float)
            vals, gap = backward_values(md_full, v, md_q, TOL_BACK)
            X[pos, col_index[c]] = vals.astype(np.float32)
            got += 1
            n_fill += int(np.isfinite(vals).sum())
        stats[well] = {"columns_present": got,
                       "mean_fill_di_well": round(n_fill / max(got * len(pos), 1), 4),
                       "total_rows": int(len(pos))}
        del df
    return X, kept, stats


def load_picks() -> dict:
    """Parse formation tops per wellbore -> {wellbore: [(md, surface), ...]}."""
    wells: dict[str, list] = {}
    cur = None
    for line in open(PICKS, encoding="utf-8", errors="replace"):
        if line.startswith("Well "):
            cur = line[4:].strip()
            wells.setdefault(cur, [])
            continue
        if cur is None or not line.startswith("  ") or "----" in line or line.strip().startswith("Well name"):
            continue
        m = re.match(r"^\s{2}(.+?)\s{2,}(\S.*?)\s{2,}(\d+)\s+([A-Z]{2}\s+)?(-?\d+\.\d+)\s+(-?\d+\.\d+)?", line)
        if not m:
            continue
        wname, surface, obs, qlf, md, tvd = m.groups()
        wells[cur].append({"surface": surface.strip(), "md": float(md), "qlf": (qlf or "").strip()})
    return wells


def build_zone(ds: pd.DataFrame, picks: dict) -> tuple[np.ndarray, list, dict]:
    """Fitur zone = satu-hot 'formasi/zone pada md ini' (top terdalam yang md_top <= md)."""
    wb = ds["wellbore"].to_numpy()
    md = ds["md"].to_numpy(float)
    label = np.full(len(ds), NO_PICK, dtype=object)
    info = {}
    for w, plist in picks.items():
        sel = wb == w
        if not sel.any():
            continue
        if not plist:
            info[w] = {"n_picks": 0}
            continue
        tops = sorted([(p["md"], p["surface"]) for p in plist])
        top_md = np.array([t[0] for t in tops])
        top_nm = np.array([t[1] for t in tops], dtype=object)
        k = np.searchsorted(top_md, md[sel], side="right") - 1
        lab = np.where(k >= 0, top_nm[np.clip(k, 0, len(tops) - 1)], NO_PICK)
        label[sel] = lab
        info[w] = {"n_picks": len(tops),
                   "n_rows": int(sel.sum()),
                   "n_above_first_top": int((k < 0).sum()),
                   "tops": [f"{nm}@{m}" for m, nm in tops]}
    for w in sorted(set(wb)):
        if w not in info:
            info[w] = {"n_picks": 0, "note": "wellbore TIDAK punya picks di file"}
    cats = sorted(set(label.tolist()))
    Z = np.zeros((len(ds), len(cats)), dtype=np.float32)
    for j, c in enumerate(cats):
        Z[:, j] = (label == c).astype(np.float32)
    counts = {c: int((label == c).sum()) for c in cats}
    info["_category_counts"] = counts
    return Z, cats, info


def build_curves(ds: pd.DataFrame, report: dict) -> tuple[np.ndarray, list, dict]:
    """Kurva geologi per md dari DLIS (fallback LIS). units DEPTH DLIS = '0.1 in' -> x0.00254 m."""
    import dlisio  # dipasang di lingkungan ini; gagal = fitur geologi kurva kosong

    wb = ds["wellbore"].to_numpy()
    md = ds["md"].to_numpy(float)
    out = {k: np.full(len(ds), np.nan, dtype=np.float32) for k in CURVE_CANDIDATES}
    info = {}
    for w, files in WELLBORE2LOG.items():
        sel = wb == w
        entry = {"files": files, "n_rows": int(sel.sum())}
        if not sel.any():
            entry["note"] = "wellbore tidak ada di dataset"
            info[w] = entry
            continue
        got = {}
        for fname in files:
            p = LOG_DIR / fname
            if not p.exists():
                entry["load"] = f"MISSING {fname}"
                continue
            try:
                loader = dlisio.dlis.load if fname.endswith(".DLIS") else dlisio.lis.load
                pf = loader(str(p))
                lf = pf[0]
                if not hasattr(lf, "frames"):
                    entry["load"] = f"OK tapi tanpa frame API ({fname})"
                    continue
                frm = lf.frames[0]
                chs = {c.name: c for c in lf.channels}
                if "DEPTH" not in chs:
                    entry["load"] = "tanpa kanal DEPTH"
                    continue
                units = str(chs["DEPTH"].units).strip()
                conv = {"0.1 in": 0.00254, "in": 0.0254, "ft": 0.3048, "m": 1.0, "mm": 0.001}
                if units not in conv:
                    entry["load"] = f"units DEPTH tak dikenal: {units!r}"
                    continue
                arr = frm.curves() if callable(frm.curves) else frm.curves
                names = arr.dtype.names
                d = np.asarray(arr["DEPTH"], dtype=float).ravel() * conv[units]
                okd = np.isfinite(d)
                d = d[okd]
                order = np.argsort(d, kind="stable")
                d_s = d[order]
                avail = {}
                for feat, cands in CURVE_CANDIDATES.items():
                    mnem = next((c for c in cands if c in names), None)
                    if mnem is None:
                        continue
                    v = np.asarray(arr[mnem], dtype=float).ravel()[okd]
                    v = np.where(np.isfinite(v) & (v > -900), v, np.nan)  # null log
                    if feat == "log_res_deep":
                        with np.errstate(divide="ignore"):
                            v = np.where(v > 0, np.log10(v), np.nan)
                    v_s = v[order]
                    q = md[sel]
                    idx, dist = nearest_idx(d_s, order, q, MD_TOL_LOG)
                    vals = np.full(len(q), np.nan, dtype=np.float32)
                    hit = idx >= 0
                    vals[hit] = v[idx[hit]].astype(np.float32)   # idx = indeks orisinal v
                    # hanya isi bila sampel terdekat finite (lubang log = NaN)
                    out[feat][sel] = np.where(np.isfinite(vals), vals, np.nan)
                    avail[feat] = {"mnem": mnem,
                                   "fill_di_well": round(float(np.isfinite(vals).mean()), 4),
                                   "n_valid_sampel_file": int(np.isfinite(v_s).sum()),
                                   "md_range_sampel": [round(float(d_s.min()), 2),
                                                       round(float(d_s.max()), 2)]}
                entry.update({"load": f"OK {fname}", "units": units, "curves": avail,
                              "md_range_file": [round(float(d_s.min()), 2), round(float(d_s.max()), 2)]})
                if avail:
                    got = avail
                break
            except Exception as e:
                entry["load"] = f"GAGAL {fname}: {type(e).__name__} {str(e)[:120]}"
        entry["overlap_md_dataset"] = None
        if got:
            r = entry.get("md_range_file")
            if r:
                sub = md[sel]
                entry["overlap_md_dataset"] = round(float(np.mean((sub >= r[0]) & (sub <= r[1]))), 4)
        info[w] = entry
        log(f"  curves {w:16s} {entry.get('load', '')[:70]}")
    cols = list(CURVE_CANDIDATES.keys())
    M = np.column_stack([out[c] for c in cols]).astype(np.float32)
    return M, cols, info


def verify_las(report: dict) -> dict:
    """LAS 2.0 F-15 D: parse + laporkan cakupan (wellbore di luar 7 sumur dataset?)."""
    p = LOG_DIR / LAS_FILE
    res = {"file": LAS_FILE, "exists": p.exists()}
    if not p.exists():
        return res
    try:
        import lasio
        las = lasio.read(str(p))
        # nama wellbore: header LAS (lasio bisa tak mengisi WELL -> fallback regex teks)
        well_name = None
        try:
            if las.well.WELL is not None:
                well_name = str(las.well.WELL.value).strip() or None
        except Exception:
            well_name = None
        if not well_name:
            head = open(p, encoding="utf-8", errors="replace").read(4000)
            m = re.search(r"^WELL\.\s*(.+?)\s*:", head, re.M)
            well_name = m.group(1).strip() if m else None
        res.update({
            "well_header": well_name,
            "start": float(las.index.min()), "stop": float(las.index.max()),
            "step": float(np.median(np.diff(las.index))),
            "n_samples": int(len(las.index)),
            "curves": [c.mnemonic for c in las.curves],
        })
        wb_in_ds = sorted(set(pd.read_csv(DS_PATH, usecols=["wellbore"])["wellbore"]))
        res["dataset_wellbores"] = wb_in_ds
        res["wellbore_in_dataset"] = (f"NO {well_name}" in wb_in_ds) or (well_name in wb_in_ds) \
            if well_name else False
        res["keputusan"] = ("LAS hanya berisi wellbore F-15 D yang TIDAK ada di 7 wellbore dataset "
                            "-> TIDAK bisa menjadi fitur evaluasi; kurva geologi diambil dari "
                            "DLIS/LIS wellbore dataset (lihat build_curves).")
    except Exception as e:
        res["error"] = f"{type(e).__name__}: {e}"
    return res


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit", action="store_true", help="hanya audit fill-rate (tanpa npz)")
    args = ap.parse_args()
    t0 = time.time()
    log("=" * 78)
    log("44a_build_new_features.py — audit fill-rate + build fitur baru (T2c)")
    log("=" * 78)

    ds = load_dataset()
    log(f"dataset: {len(ds)} baris, {len(ds.columns)} kolom | y_10 prev={ds['y_10'].mean():.4f} "
        f"y_30 prev={ds['y_30'].mean():.4f}")
    last_feats = [c for c in ds.columns if c.startswith("last_")]
    nan_a = {c: int(ds[c].isna().sum()) for c in last_feats}
    log(f"fitur lama last_* ({len(last_feats)}) NaN per kolom: { {k: v for k, v in nan_a.items() if v} }")

    log("\n[1] VERIFIKASI berkas sumber (sha256 + pemetaan)")
    verif = verify_sources(ds)
    log(f"    semua file ada: {verif['all_files_present']} | "
        f"n file ter-hash: {len(verif['files'])}")

    log("\n[2] AUDIT FILL-RATE Norway*.csv (join md terdekat, tol 0,1 m; TANPA label)")
    audit = audit_raw_fillrate(ds)
    for w, j in audit["join"].items():
        log(f"    {WELL2FILE[w][:44]:44s} match={j.get('match_rate')} "
            f"dist_max={j.get('dist_max')} dup_md_file={j.get('n_dup_md_file')}")

    sel = select_columns(audit["fillrate"])
    # drop kolom konstan (variansi 0) setelah seleksi fill — dicek di pass 2
    log(f"\n    kolom numerik diaudit : {audit['n_numeric_columns_audited']}")
    log(f"    lolos seleksi         : {len(sel['kept'])}")
    log(f"    ditulis drop reason   : {len(sel['dropped'])}")

    log("\n[3] GELOGI — formation picks + kurva log + LAS")
    picks = load_picks()
    Z, zone_cols, zone_info = build_zone(ds, picks)
    log(f"    zone one-hot: {len(zone_cols)} kategori | counts={zone_info['_category_counts']}")
    try:
        M, curve_cols, curve_info = build_curves(ds, audit)
        curve_fill = {c: round(float(np.isfinite(M[:, j]).mean()), 4)
                      for j, c in enumerate(curve_cols)}
        log(f"    kurva fill-rate pooled: {curve_fill}")
    except Exception:
        traceback.print_exc(limit=2)
        M = np.zeros((len(ds), 0), dtype=np.float32)
        curve_cols, curve_info, curve_fill = [], {}, {}
    las_res = verify_las(audit)
    log(f"    LAS {las_res.get('well_header')}: di dataset? {las_res.get('wellbore_in_dataset')}")

    result = {
        "task": "t_33cc76d7",
        "script": "code/44a_build_new_features.py",
        "runtime_s": round(time.time() - t0, 1),
        "rules": {
            "fill_min": FILL_MIN,
            "min_wells_at_fill": MIN_WELLS_AT_FILL,
            "blocklist_exact": sorted(BLOCKLIST_EXACT),
            "blocklist_substr": BLOCKLIST_SUBSTR,
            "md_tol_raw_m": MD_TOL_RAW,
            "md_tol_log_m": MD_TOL_LOG,
            "tol_backward_m": TOL_BACK,
            "join_nilai": "backward: sampel non-null TERAKHIR sebelum md (tanpa look-ahead); "
                          "sama untuk audit dan build",
            "label_free": "seleksi TIDAK memakai y_10/y_30 (hanya fill-rate + blocklist struktural)",
        },
        "verification": verif,
        "audit": audit,
        "selection": sel,
        "zone": {"columns": zone_cols, "info": zone_info},
        "curves": {"columns": curve_cols, "fill_pooled": curve_fill, "info": curve_info},
        "las": las_res,
        "last_feats_nan": {k: v for k, v in nan_a.items() if v},
        "mode": "audit_only" if args.audit else "full_build",
    }
    OUT_JSON.write_text(json.dumps(result, indent=1, ensure_ascii=False, default=str),
                        encoding="utf-8")
    log(f"\nJSON audit -> {OUT_JSON}")

    if args.audit:
        log("mode --audit: npz TIDAK ditulis.")
        log(f"SELESAI {result['runtime_s']}s")
        return

    # ---- build npz (tanpa kolom konstan) ----
    log("\n[4] BUILD matriks fitur baru")
    X_raw, raw_cols, build_stats = build_raw_matrix(ds, sel["kept"])
    var = np.nanvar(X_raw, axis=0)
    konstan = [raw_cols[j] for j in range(len(raw_cols)) if not np.isfinite(var[j]) or var[j] == 0]
    keep_mask = np.array([np.isfinite(var[j]) and var[j] > 0 for j in range(len(raw_cols))])
    X_raw = X_raw[:, keep_mask]
    raw_cols = [c for c, k in zip(raw_cols, keep_mask) if k]
    log(f"    raw: {X_raw.shape} | drop konstan/all-NaN: {konstan}")

    cols = list(raw_cols) + list(zone_cols) + list(curve_cols)
    group = (["raw"] * len(raw_cols)) + (["zone"] * len(zone_cols)) + (["curve"] * len(curve_cols))
    # indikator keberadaan kurva (2/7 wellbore tanpa log berguna -> NaN; imputasi median
    # membuatnya tak terbedakan dari nilai nyata, jadi keberadaan dikasih eksplisit)
    ind_cols = [f"present::{c}" for c in curve_cols]
    IND = np.isfinite(M).astype(np.float32)
    cols = cols + ind_cols
    group = group + (["curve_present"] * len(ind_cols))
    X_new = np.hstack([X_raw, Z, M, IND]).astype(np.float32)
    log(f"    X_new: {X_new.shape} (raw {X_raw.shape[1]} + zone {Z.shape[1]} + "
        f"curve {M.shape[1]} + indikator {IND.shape[1]})")

    fill_final = {c: round(float(np.isfinite(X_new[:, j]).mean()), 4)
                  for j, c in enumerate(cols)}
    np.savez_compressed(
        OUT_NPZ,
        X_new=X_new,
        cols=np.array(cols, dtype=object),
        group=np.array(group, dtype=object),
        row_id=ds["row_id"].to_numpy(),
        md=ds["md"].to_numpy(float),
        well=ds["well"].to_numpy(dtype=object),
        wellbore=ds["wellbore"].to_numpy(dtype=object),
    )
    meta = {
        "task": "t_33cc76d7",
        "source_script": "code/44a_build_new_features.py",
        "created_unix": int(time.time()),
        "shape": [int(X_new.shape[0]), int(X_new.shape[1])],
        "columns": cols,
        "groups": {g: [c for c, gg in zip(cols, group) if gg == g]
                   for g in ("raw", "zone", "curve", "curve_present")},
        "fill_pooled": fill_final,
        "raw_build_stats": build_stats,
        "raw_columns_dropped_konstan": konstan,
        "fillrate_json": "docs/V2_USROP_FILLRATE.json",
        "justifikasi_fill_kurva": {
            "aturan": "task: kolom fill<50% tidak dipakai KECUALI dijustifikasi",
            "dipertahankan": [c for c in curve_cols if fill_final.get(c, 0) < FILL_MIN],
            "alasan": ("Kurva log bersifat interval (hanya bagian yang di-log) dan 2/7 wellbore "
                       "tak punya log berguna (F-7 file LIS korup, F-9 log lebih dalam dari "
                       "jendela USROP) -> fill pooled turun. Kurva tetap dipertahankan karena "
                       "inilah satu-satunya sinyal geologi terukur yang diminta task (variant C); "
                       "baris tanpa log diimputasi median train-fold + indikator present::*."),
        },
        "source_sha256": {k: v.get("sha256") for k, v in verif["files"].items()},
        "selection_rules": result["rules"],
        "curve_fill_pooled": curve_fill,
        "las": las_res,
        "runtime_s": round(time.time() - t0, 1),
    }
    OUT_META.write_text(json.dumps(meta, indent=1, ensure_ascii=False, default=str),
                        encoding="utf-8")
    log(f"NPZ  -> {OUT_NPZ}")
    log(f"META -> {OUT_META}")
    below = {c: f for c, f in fill_final.items() if f < FILL_MIN}
    log(f"kolom dgn fill<50% di npz (butuh justifikasi di doc): {len(below)}")
    for c, f in sorted(below.items(), key=lambda kv: kv[1])[:25]:
        log(f"    {c[:70]:70s} {f}")
    log(f"SELESAI {result['runtime_s']}s")
    log("EXIT 0")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        traceback.print_exc()
        sys.exit(1)
