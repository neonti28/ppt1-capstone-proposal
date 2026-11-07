#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
code/46_beat_canary_ts.py — Kampanye T2-d: "beat-the-canary FINAL, resolusi time-based"
Kanban task: t_9df689f1 [ML Engineer] — SATU kampanye, TANPA tuning, seed tetap.

PERTANYAAN (kriteria PM, diuji apa adanya):
  Apakah ada varian fitur time-based yang macro-LOWO AUPRC >= target
  DAN unggul >=5/7 fold vs canary-MD time-based (varian G/log) ?
  target = max(0,2465 ; canary_time_based + 0,02)
  (kartu T2-d: "kalau canary time-based lebih tinggi dari 0,2465 maka target ikut naik,
   JANGAN pakai canary lama 0,2265 yang tidak sebanding")

DESAIN (di-pra-registrasi sebelum hasil dilihat — dokumentasi §3 dokumen keluaran):
  UNIT ANALISIS = EVENT, bukan baris 4-detik (menghindari pseudo-replication
  "multiple rows per event"):
    - positif  = 661 event dari T10 (data/predictive/features_timeseries.npz), 1 baris/event
    - negatif  = kontrol anchors: sampel baris WITSML yang TENANG (tidak ada event
                 start dalam horizon H=2 jam ke depan), tanam per fold
    - H = 2 jam = jendela utama T10 (w2h); horizon "event start within next 2h"
    - prevalensi per fold DIPERTAHANKAN sama dengan laju alamiah p_f =
      fraksi baris fold yang punya event start dalam 2h ke depan (case-control
      yang mempertahankan odds alamiah -> AUPRC gate tetap sebanding dgn dunia md)
      n_neg_f = round(n_pos_f * (1-p_f)/p_f), sampel uniform tanpa penggantian, seed 42
    - anchor negatif WAJIB tenang: pencarian ts < anchor ketat (anti-leakage sama dgn T10)

VARIAN (sekali jalan, tanpa seleksi fitur berbasis label):
  G : baseline MD saja, 7 fitur statistik DMEA jendela 2h dari X_baseline
      (canary time-based — dihitung DULU; dasar gate)
  E : fitur time-series saja (480 = 3 jendela x 16 channel x 10 statistik, T10)
  F : E + fitur lama (12 kolom last_* kampanye 40 + 58 kolom features_v2 kampanye 44),
      join per unit: wellbore + md terdekat (tol 1,0 m), tanpa look-ahead

PROTOKOL = identik kampanye 40/42/44 (wajib agar sebanding):
  LOWO 7 fold; uji = 1 sumur penuh; latih = 6 sumur lain; val = 15% ekor temporal latih
  (threshold F1-maks dari skor val); seed 42; StandardScaler logistik fit di latih;
  RF_PARAMS & HGB_PARAMS persis kampanye 40. Satu kampanye, output pertama = final.
  DEVIASI terdokumentasi (bukan pilihan model):
    (a) set md kini bisa punya NaN (window kosong T10) -> imputasi median LATIH
        dipakai seragam untuk semua varian (kampanye 44 md bebas NaN);
    (b) tidak ada lengan Δ (tak ada md-delta di resolusi waktu) -> 1 lengan, H=2h;
    (c) canary beku 0,2265 TIDAK bisa direproduksi (unit berbeda) -> canary G dihitung
        segar; verifikasi independen code/47.

Output: docs/V2_ML_BEAT_CANARY_TS.json + docs/V2_ML_BEAT_CANARY_TS.md
        (ditulis skrip dari JSON, 0 angka manual) + data/predictive/*controls*.npz
STOP (exit 3) bila asumsi protokol/pokok terpenuhi tapi hasil tidak sah
(shape fold != 7, fold tanpa dua kelas, anti-leakage violations > 0, canary None).
"""
from __future__ import annotations

import importlib.util
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (average_precision_score, confusion_matrix, f1_score,
                             precision_recall_curve, precision_score, recall_score,
                             roc_auc_score)
from sklearn.preprocessing import StandardScaler

BASE = Path(__file__).resolve().parents[1]
PARSED = BASE / "data" / "volve" / "witsml_parsed"
EVENTS_NPZ = BASE / "data" / "predictive" / "features_timeseries.npz"
LABELS = BASE / "data" / "volve" / "labels_curated_v2.csv"
V2_NPZ = BASE / "data" / "predictive" / "features_v2.npz"
DS_PATH = BASE / "data" / "predictive" / "dataset_prediktif.csv"
SHARD_DIR = BASE / "data" / "predictive" / "controls_shards"
CONTROLS_NPZ = BASE / "data" / "predictive" / "features_timeseries_controls.npz"
# T2-e (P4): desain BARU (syarat ketersediaan simetris) memakai artefak terpisah
# supaya artefak T2-d yang dikutip PM/ML Auditor tidak ditimpa.
SHARD_DIR_B = BASE / "data" / "predictive" / "controls_shards_berdata"
CONTROLS_NPZ_B = BASE / "data" / "predictive" / "features_timeseries_controls_berdata.npz"
# Arsip JSON kampanye T2-d (salinan persis sebelum T2-e) -> blok desain asli
# dibaca ulang tiap run sehingga rerun tetap mereproduksi dokumen penuh.
ARCHIVE_JSON = BASE / "docs" / "V2_ML_BEAT_CANARY_TS_T2D_ARSIP.json"
# Hasil probe determinisme (code/49_p7_determinisme.py) — dibaca utk laporan P7.
P7_JSON = BASE / "docs" / "V2_P7_DETERMINISME.json"

# Pra-registrasi P4 (diambil dari komentar kartu t_471b790f sebelum hasil dilihat).
PRA_REGISTRASI_P4 = {
    "komentar_kartu": "t_471b790f comment 24 (timestamp komentar < generated_at kampanye)",
    "keputusan": "(ii) simetrisasi syarat ketersediaan data — jendela kosong "
                 "DILARANG sama untuk positif dan negatif",
    "alasan": "flag kosong hampir penanda kelas (191 pos vs 1 neg) dan "
              "missingness-only 0,3747 > canary 0,3606 -> artefak harus dihilangkan "
              "secara struktural, bukan sekadar dikecualikan dari skor",
    "syarat": "n_rows(w30m) >= 1 (jendela bersarang: 30m < 2h < 6h -> setara ketiga "
              "jendela non-kosong); berlaku identik utk kelas negatif dan dipakai pada "
              "LATIHAN + EVALUASI",
    "protokol": "LOWO 7 fold, val 15% ekor temporal, seed 42, RF/HGB params kampanye 40, "
                "varian G/E/F identik, SATU kampanye tanpa tuning, output pertama = final",
    "gate": "canary = varian G (log) desain baru; target = max(0,2465; canary+0,02); "
            "menang >= 5/7 fold",
    "sampling": "p_f dihitung dari seluruh baris (tidak berubah); "
                "n_neg_f = round(n_pos_f*(1-p_f)/p_f) dgn n_pos_f = event lolos syarat; "
                "pool tenang difilter syarat yg sama; uniform tanpa penggantian, seed 42",
    "sensitivitas": {
        "S1": "evaluasi longgar: semua 661 event + kontrol desain baru, skor out-of-fold "
              "model yang sama (tanpa training ulang)",
        "S2": "baseline hanya-flag-kosong pada set S1, dilaporkan terpisah dari skor sensor",
    },
    "aturan_klaim": "framing §3.3 verbatim; TIDAK ada klaim 'mengalahkan canary' kecuali "
                    "varian lolos gate pada desain baru ini; jika gagal -> tulis GAGAL",
    "fakta_struktur_data_sebelum_kampanye": "positif 467/661 lolos (194 gugur: 191 "
                                            "kosong-2h + 3 kosong-30m); kontrol 6617/6618",
}
OUT_JSON = BASE / "docs" / "V2_ML_BEAT_CANARY_TS.json"
OUT_MD = BASE / "docs" / "V2_ML_BEAT_CANARY_TS.md"

# ---- pra-registrasi (dibaca sebelum hasil; jangan diubah setelah hasil terlihat) ----
HORIZON_S = 2 * 3600          # H = 2 jam (= jendela utama T10 w2h)
HORIZON_NS = HORIZON_S * 1_000_000_000
JUNK_CUTOFF = np.datetime64("2010-01-01T00:00:00")   # 2 baris/fold th 2015 = artefak parse
JUNK_CUTOFF_NS = int(pd.Timestamp("2010-01-01", tz="UTC").value)   # ns sejak epoch
SEED = 42
MD_TOL = 1.0                  # meter, join fitur lama (konsisten TOL_BACK 44a)
TARGET_FLOOR = 0.2465         # syarat mutlak T2 dari PM
MARGIN = 0.02                 # margin canary -> target (aturan kartu T2-d)
MIN_WINS = 5                  # syarat fold wins (R7)

# ---- T2-e / P4: syarat ketersediaan (pra-registrasi, komentar kartu t_471b790f) ----
# Jendela bersarang: w30m < w2h < w6h -> syarat "ketiga jendela non-kosong"
# identik dengan n_rows(w30m) >= 1. Berlaku SAMA utk positif & negatif dan
# dipakai pada LATIHAN + EVALUASI (satu himpunan unit).
W30M_S = 30 * 60
W2H_S = 2 * 3600
W6H_S = 6 * 3600

RF_PARAMS = dict(n_estimators=300, class_weight="balanced", min_samples_leaf=2,
                 n_jobs=-1, random_state=42)
HGB_PARAMS = dict(max_iter=300, class_weight="balanced", random_state=42)

MODELS = ["log", "rf", "hgb"]
SETS = ["G", "E", "F"]
KEYS = [f"{m}_{s}" for s in SETS for m in MODELS]
CANARY_KEY = "log_G"

SHORT = {"F-9_A": "F-9A", "F-7": "F-7", "F-14": "F-14", "F-15A": "F-15A",
         "F-15_S": "F-15 (S)", "F-5": "F-5", "F-9": "F-9"}

FRAMING_33 = (
    '"Pipeline predictive maintenance (event nyata + jendela waktu/kedalaman sebelum event + '
    "model tervalidasi temporal dan leave-one-well-out) sudah terbangun dan bebas leakage. "
    "Keterampilan prediktifnya saat ini masih di bawah baseline posisi-kedalaman, sehingga klaim "
    "'prediksi dini berbasis sensor' belum boleh dinaikkan sebelum model mengalahkan baseline tersebut.\\\""
)

OLD_LAST_COLS = ["last_md", "last_wob", "last_spp", "last_torque", "last_rop", "last_rpm",
                 "last_flow", "last_mud_density", "last_diameter", "last_hookload",
                 "last_tvd", "last_gamma"]


def log(m: str = "") -> None:
    print(m, flush=True)


def nm(v) -> str:
    """Pemisah ribuan gaya ID utk MD: 4274005 -> '4.274.005' (int/str numerik)."""
    if v is None:
        return ""
    if isinstance(v, str):
        try:
            v = int(v.replace(".", "").replace(",", ""))
        except ValueError:
            return v
    return f"{int(v):,}".replace(",", ".")


def load_t10():
    """Muat modul code/60_ts_features.py sebagai pustaka (jalur kode fitur IDENTIK T10)."""
    path = BASE / "code" / "60_ts_features.py"
    spec = importlib.util.spec_from_file_location("ts60", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def ap(yt, st):
    if len(np.unique(yt)) < 2:
        return None
    return round(float(average_precision_score(yt, st)), 4)


def prf(yt, pred) -> dict:
    tn, fp, fn, tp = confusion_matrix(yt, pred, labels=[0, 1]).ravel()
    return {"precision": round(float(precision_score(yt, pred, zero_division=0)), 4),
            "recall": round(float(recall_score(yt, pred, zero_division=0)), 4),
            "f1": round(float(f1_score(yt, pred, zero_division=0)), 4),
            "tp": int(tp), "fp": int(fp), "fn": int(fn), "tn": int(tn)}


def tune_thr(yv, sv) -> float:
    p, r, t = precision_recall_curve(yv, sv)
    f1 = np.where((p[:-1] + r[:-1]) > 0,
                  2 * p[:-1] * r[:-1] / np.maximum(p[:-1] + r[:-1], 1e-12), 0.0)
    if f1.size == 0:
        return float(np.quantile(sv, 0.95))
    return float(t[f1 >= f1.max() - 1e-12].max())


def r_at_p(yt, st, pmin: float) -> float:
    p, r, _ = precision_recall_curve(yt, st)
    m = p >= pmin
    return round(float(r[m].max()), 4) if m.any() else 0.0


def brier(yt, st) -> float:
    return round(float(np.mean((np.asarray(st, float) - np.asarray(yt, float)) ** 2)), 4)


def reliability(yt, st, n_bins: int = 10):
    idx = np.argsort(st, kind="stable")
    bins = []
    for b in np.array_split(idx, n_bins):
        if b.size == 0:
            continue
        bins.append({"n": int(b.size), "mean_pred": round(float(st[b].mean()), 4),
                     "frac_pos": round(float(yt[b].mean()), 4)})
    n = float(len(yt))
    ece = round(sum(x["n"] / n * abs(x["mean_pred"] - x["frac_pos"]) for x in bins), 4)
    maxgap = round(max(abs(x["mean_pred"] - x["frac_pos"]) for x in bins), 4)
    return bins, ece, maxgap


def impute_fit(Xtr: np.ndarray) -> np.ndarray:
    with np.errstate(all="ignore"):
        med = np.nanmedian(np.where(np.isfinite(Xtr), Xtr, np.nan), axis=0)
    med = np.where(np.isfinite(med), med, 0.0)
    return med


def impute_apply(X: np.ndarray, med: np.ndarray) -> np.ndarray:
    out = np.where(np.isfinite(X), X, med[None, :])
    return out.astype(np.float64, copy=False)


# =========================================================================
# PART A — kontrol anchors (negatif) + fiturnya, jalur kode identik T10
# =========================================================================
def fold_resolution(mod, verify, fold: str):
    fmeta = verify[fold]
    fill = fmeta["fill_rate_ge_50pct"]
    resolution, usecols = {}, ["timestamp"]
    for ch in mod.CHANNELS:
        if ch in fill:
            resolution[ch] = {"column": ch, "variant": "base"}
            usecols.append(ch)
        elif f"GS_{ch}" in fill:
            resolution[ch] = {"column": f"GS_{ch}", "variant": "GS_"}
            usecols.append(f"GS_{ch}")
        else:
            resolution[ch] = {"column": None, "variant": None}
    return resolution, usecols


def features_for_anchor(mod, ts_ns, cols, md_vals, t_end, X_row, XB_row, XM_row):
    """Fitur 1 anchor persis loop T10 (code/60) — window [t-W, t) ketat."""
    violations = 0
    rows_scanned = 0
    for wi, (wname, wsec) in enumerate(mod.WINDOWS):
        w_start = t_end - wsec * 1_000_000_000
        i0 = int(np.searchsorted(ts_ns, w_start, side="left"))
        i1 = int(np.searchsorted(ts_ns, t_end, side="left"))
        seg = ts_ns[i0:i1]
        rows_scanned += seg.size
        if seg.size and (seg >= t_end).any():
            violations += int((seg >= t_end).sum())
        n_rows = seg.size
        full = bool(w_start >= ts_ns[0])
        if n_rows >= 2:
            dt = np.diff(seg) / 1e9
            gap_med, gap_max = float(np.median(dt)), float(np.max(dt))
        else:
            gap_med, gap_max = (np.nan, np.nan)
        base_i = wi * len(mod.CHANNELS) * len(mod.STATS)
        t_sec = (seg - w_start) / 1e9 if n_rows else np.array([])
        for ci, ch in enumerate(mod.CHANNELS):
            v = cols[ch]
            x = v[i0:i1] if v is not None else np.array([])
            st = mod.channel_stats(x, t_sec)
            for si, s in enumerate(mod.STATS):
                X_row[base_i + ci * len(mod.STATS) + si] = st.get(s, np.nan)
        mbase = wi * 4
        XM_row[mbase + 0] = n_rows
        XM_row[mbase + 1] = gap_med
        XM_row[mbase + 2] = gap_max
        XM_row[mbase + 3] = 1.0 if full else 0.0
    # baseline md (jendela 2h) + konteks waktu anchor
    if md_vals is not None:
        wname, wsec = mod.WINDOWS[1]
        w_start = t_end - wsec * 1_000_000_000
        i0 = int(np.searchsorted(ts_ns, w_start, side="left"))
        i1 = int(np.searchsorted(ts_ns, t_end, side="left"))
        x = md_vals[i0:i1]
        t_sec = (ts_ns[i0:i1] - w_start) / 1e9
        v = np.isfinite(x)
        if int(v.sum()) >= mod.MIN_VALID:
            xv, tv = x[v], t_sec[v]
            XB_row[0] = xv.mean()
            XB_row[1] = xv.std(ddof=1)
            XB_row[2] = xv.min()
            XB_row[3] = xv.max()
            XB_row[4] = mod.ols_slope(xv, tv / 60.0)
            XB_row[5] = xv[-1]
            XB_row[6] = xv[-1] - xv[0]
    t_anchor = pd.Timestamp(t_end).tz_localize("UTC").to_pydatetime()
    h = t_anchor.hour + t_anchor.minute / 60.0
    dow = t_anchor.weekday() + (t_anchor.hour / 24.0)
    XB_row[7] = np.sin(2 * np.pi * h / 24.0)
    XB_row[8] = np.cos(2 * np.pi * h / 24.0)
    XB_row[9] = np.sin(2 * np.pi * dow / 7.0)
    XB_row[10] = np.cos(2 * np.pi * dow / 7.0)
    return violations, rows_scanned


def build_controls(mod, events_npz, avail_map=None, shard_dir=None,
                   controls_npz=None, design_tag="asli") -> dict:
    """Bangun kontrol anchors per fold (cache per shard; deterministik seed 42).

    avail_map (opsional, desain P4): dict fold -> bool[] sepanjang unit positif fold
    itu; pool tenang lalu DIFILTER dgn syarat ketersediaan yg sama dgn positif.
    """
    shard_dir = Path(shard_dir) if shard_dir else SHARD_DIR
    controls_npz = Path(controls_npz) if controls_npz else CONTROLS_NPZ
    shard_dir.mkdir(parents=True, exist_ok=True)
    verify = json.load(open(PARSED / "_verify.json"))
    # event start per fold (dari npz T10 — unit positif yang dipakai kampanye ini)
    ev_by_fold = {}
    for f, t in zip(events_npz["fold"], events_npz["act_start_utc"]):
        ev_by_fold.setdefault(str(f), []).append(pd.Timestamp(str(t)))
    feat_names = [f"{w}__{ch}__{st}" for w, _ in mod.WINDOWS
                  for ch in mod.CHANNELS for st in mod.STATS]
    n_feat = len(feat_names)
    bnames = ["md_mean", "md_std", "md_min", "md_max", "md_slope_per_min", "md_last",
              "md_delta", "time_hour_sin", "time_hour_cos", "time_dow_sin", "time_dow_cos"]
    mnames = [f"{w}__{s}" for w, _ in mod.WINDOWS
              for s in ["n_rows", "gap_median_s", "gap_max_s", "full_window"]]

    rng = np.random.default_rng(SEED)
    out = {"fold": [], "anchor_ts": [], "X": [], "XB": [], "XM": []}
    samp_meta = {}
    viol_total = 0
    scanned_total = 0

    for fold in sorted(ev_by_fold):
        t0 = time.time()
        shard = shard_dir / f"controls_{fold}.npz"
        n_pos_all = len(ev_by_fold[fold])
        n_pos_f = (int(np.asarray(avail_map[fold]).sum()) if avail_map is not None
                   else n_pos_all)
        events_ns = np.sort(np.array([pd.Timestamp(t).value for t in ev_by_fold[fold]],
                                     dtype="int64"))
        if shard.exists():
            s = np.load(shard, allow_pickle=True)
            ok = (int(s["seed"]) == SEED and int(s["n_pos"]) == n_pos_f
                  and int(s["horizon_s"]) == HORIZON_S
                  and (str(s["design_tag"]) if "design_tag" in s.files else "asli")
                     == design_tag)
            if not ok:
                raise RuntimeError(f"{shard}: seed/n_pos/horizon/design berbeda -> hapus shard manual")
            idx = s["anchor_idx"]
            samp_meta[fold] = json.loads(str(s["sampling_meta"]))
            log(f"  [{fold}] shard ada: {len(idx)} kontrol (dipakai ulang)")
        else:
            resolution, usecols = fold_resolution(mod, verify, fold)
            df = pd.read_csv(PARSED / f"{fold}.csv", usecols=usecols)
            ts = pd.to_datetime(df["timestamp"], format="ISO8601", utc=True)
            if not ts.is_monotonic_increasing:
                order = np.argsort(ts.to_numpy(), kind="stable")
                ts = ts.iloc[order]
                df = df.iloc[order]
            ts_ns = ts.dt.tz_convert("UTC").dt.tz_localize(None).to_numpy().astype(np.int64)
            junk = ts_ns > JUNK_CUTOFF_NS
            pool = np.flatnonzero(~junk)
            # laju alamiah p_f: fraksi baris pool dgn event start dalam (t, t+H]
            j = np.searchsorted(events_ns, ts_ns[pool], side="right")
            has = j < len(events_ns)
            nxt = np.full(len(pool), np.iinfo("int64").max, dtype="int64")
            nxt[has] = events_ns[j[has]]
            in_horizon = (nxt - ts_ns[pool]) < HORIZON_NS
            p_f = float(in_horizon.mean())
            quiet = pool[~in_horizon]
            quiet_all = int(len(quiet))
            if avail_map is not None:
                # syarat ketersediaan P4 (simetris): anchor kontrol harus punya
                # >= 1 baris dalam [anchor-30m, anchor) — sama dgn syarat positif,
                # dan dihitung persis seperti jalur fitur (searchsorted left/left).
                ts_q = ts_ns[quiet]
                i0 = np.searchsorted(ts_ns, ts_q - W30M_S * 1_000_000_000, side="left")
                i1 = np.searchsorted(ts_ns, ts_q, side="left")
                quiet = quiet[i0 < i1]
            n_neg = int(round(n_pos_f * (1.0 - p_f) / max(p_f, 1e-9)))
            if n_neg > len(quiet):
                raise RuntimeError(f"{fold}: quiet pool {len(quiet)} < n_neg {n_neg}")
            idx = np.sort(rng.choice(quiet, size=n_neg, replace=False))
            samp_meta[fold] = {
                "n_pool_rows": int(len(pool)),
                "junk_rows_dropped": int(junk.sum()),
                "p_natural_2h": round(p_f, 4),
                "n_pos": int(n_pos_f),
                "n_pos_semua_event": int(n_pos_all),
                "n_neg": int(n_neg),
                "quiet_pool": quiet_all,
                "quiet_pool_berdata": int(len(quiet)),
                "prevalence_fold": round(n_pos_f / (n_pos_f + n_neg), 4),
                "seed": SEED,
                "horizon_s": HORIZON_S,
                "design_tag": design_tag,
            }
            np.savez_compressed(shard, anchor_idx=idx, seed=SEED, n_pos=n_pos_f,
                                horizon_s=HORIZON_S, design_tag=design_tag,
                                sampling_meta=json.dumps(samp_meta[fold]))
            del df, ts
            log(f"  [{fold}] kontrol dibangun: pool={len(pool)} p_f={p_f:.4f} "
                f"n_neg={n_neg} ({time.time()-t0:.0f}s)")

        # fitur kontrol — jalur identik T10
        shard_cache = shard_dir / f"ctrlfeat_{fold}.npz"
        if shard_cache.exists():
            c = np.load(shard_cache, allow_pickle=True)
            Xc, XBc, XMc = c["X"], c["XB"], c["XM"]
            anchors = c["anchor_ts"]
            viol_total += int(c["violations"])
            scanned_total += int(c["rows_scanned"])
        else:
            resolution, usecols = fold_resolution(mod, verify, fold)
            df = pd.read_csv(PARSED / f"{fold}.csv", usecols=usecols)
            ts = pd.to_datetime(df["timestamp"], format="ISO8601", utc=True)
            if not ts.is_monotonic_increasing:
                order = np.argsort(ts.to_numpy(), kind="stable")
                ts = ts.iloc[order]
                df = df.iloc[order]
            ts_ns = ts.dt.tz_convert("UTC").dt.tz_localize(None).to_numpy().astype(np.int64)
            cols = {}
            for ch in mod.CHANNELS:
                c_ = resolution[ch]["column"]
                cols[ch] = df[c_].to_numpy(dtype=np.float64) if c_ else None
            md_col = resolution["DMEA"]["column"]
            md_vals = df[md_col].to_numpy(dtype=np.float64) if md_col else None
            n = len(idx)
            v0, s0 = viol_total, scanned_total
            Xc = np.full((n, n_feat), np.nan, dtype=np.float32)
            XBc = np.full((n, len(bnames)), np.nan, dtype=np.float32)
            XMc = np.full((n, len(mnames)), np.nan, dtype=np.float32)
            anchors = ts_ns[idx]
            for r, i in enumerate(idx):
                v, sc = features_for_anchor(mod, ts_ns, cols, md_vals, int(ts_ns[i]),
                                            Xc[r], XBc[r], XMc[r])
                viol_total += v
                scanned_total += sc
            np.savez_compressed(shard_cache, X=Xc, XB=XBc, XM=XMc, anchor_ts=anchors,
                                violations=int(viol_total - v0),
                                rows_scanned=int(scanned_total - s0))
            del df, ts, cols
            log(f"  [{fold}] fitur kontrol: {n} anchor ({time.time()-t0:.0f}s)")
        out["fold"].extend([fold] * len(idx))
        out["anchor_ts"].extend(anchors.tolist())
        out["X"].append(Xc)
        out["XB"].append(XBc)
        out["XM"].append(XMc)

    res = {
        "fold": np.array(out["fold"], dtype=object),
        "anchor_ts": np.array(out["anchor_ts"], dtype="int64"),
        "X": np.vstack(out["X"]),
        "XB": np.vstack(out["XB"]),
        "XM": np.vstack(out["XM"]),
        "feature_names": np.array(feat_names, dtype=object),
        "baseline_names": np.array(bnames, dtype=object),
        "window_meta_names": np.array(mnames, dtype=object),
        "y": np.zeros(len(out["fold"]), dtype=np.int64),
    }
    np.savez_compressed(controls_npz,
                        X=res["X"], X_baseline=res["XB"], X_window_meta=res["XM"],
                        feature_names=res["feature_names"],
                        baseline_names=res["baseline_names"],
                        window_meta_names=res["window_meta_names"],
                        fold=res["fold"], anchor_ts=res["anchor_ts"], y=res["y"],
                        seed=np.array(SEED), horizon_s=np.array(HORIZON_S),
                        design_tag=design_tag,
                        anti_violations=np.array(int(viol_total)),
                        anti_rows_scanned=np.array(int(scanned_total)),
                        sampling_meta=json.dumps(samp_meta))
    return {**res, "sampling_meta": samp_meta, "npz_path": str(controls_npz),
            "shard_dir": str(shard_dir),
            "anti_leakage": {"violations": int(viol_total),
                             "rows_scanned": int(scanned_total),
                             "scope": f"kontrol ({len(out['fold'])} anchor, jalur kode ini)"}}


# =========================================================================
# PART B — fitur lama (12 last_* + 58 features_v2) via join wellbore+md
# =========================================================================
def join_old_features(units_wb: np.ndarray, units_md: np.ndarray):
    v2 = np.load(V2_NPZ, allow_pickle=True)
    md_v2 = v2["md"].astype(np.float64)
    wb_v2 = np.array([str(x) for x in v2["wellbore"]])
    X_new = v2["X_new"].astype(np.float64)
    v2_cols = [str(c) for c in v2["cols"]]
    row_id_v2 = v2["row_id"].astype(np.int64)

    ds = pd.read_csv(DS_PATH, usecols=["row_id"] + OLD_LAST_COLS)
    ds = ds.set_index("row_id")
    missing = int((~np.isin(row_id_v2, ds.index)).sum())
    last_all = ds.reindex(row_id_v2)[OLD_LAST_COLS].to_numpy(dtype=np.float64)

    # urutkan indeks v2 per wellbore (untuk searchsorted md)
    order_by_wb = {}
    for w in sorted(set(wb_v2)):
        ii = np.flatnonzero(wb_v2 == w)
        order_by_wb[w] = ii[np.argsort(md_v2[ii], kind="stable")]

    n = len(units_wb)
    old = np.full((n, X_new.shape[1] + len(OLD_LAST_COLS)), np.nan, dtype=np.float64)
    matched = 0
    matched_mask = np.zeros(n, dtype=bool)
    for i in range(n):
        w = units_wb[i]
        m = units_md[i]
        ii = order_by_wb.get(w)
        if ii is None or ii.size == 0 or not np.isfinite(m):
            continue
        mm = md_v2[ii]
        k = int(np.searchsorted(mm, m))
        best = None
        for cand in (k - 1, k):
            if 0 <= cand < ii.size and abs(mm[cand] - m) <= MD_TOL:
                if best is None or abs(mm[cand] - m) < abs(mm[best] - m):
                    best = cand
        if best is None:
            continue
        j = ii[best]
        old[i, :X_new.shape[1]] = X_new[j]
        old[i, X_new.shape[1]:] = last_all[j]
        matched += 1
        matched_mask[i] = True
    names = [f"v2__{c}" for c in v2_cols] + [f"old__{c}" for c in OLD_LAST_COLS]
    meta = {"tol_m": MD_TOL, "n_units": int(n), "matched": int(matched),
            "match_rate": round(matched / max(n, 1), 4),
            "matched_mask": matched_mask,
            "v2_row_id_missing_in_dataset": missing,
            "columns": names}
    return old, names, meta


# =========================================================================
# PART C — kampanye LOWO (protokol identik 40/42/44)
# =========================================================================
def run_arm(sets, y, ts_np, wells, _keys, label="main", extra=None):
    """extra (opsional, P4-S1): {"sets": {G/E/F: matriks unit tambahan},
    "wells": wellbore per unit} -> skor out-of-fold utk unit di luar himpunan
    pelatihan, TANPA training tambahan (dipakai sensitivitas evaluasi longgar)."""
    folds = {k: {} for k in KEYS}
    pool = {k: {"y": [], "score": [], "pred": []} for k in KEYS}
    imp_acc = {f"rf_{s}": [] for s in SETS}
    split_info = {}
    score_full = {k: np.full(len(y), np.nan) for k in KEYS}
    pred_full = {k: np.full(len(y), -1, dtype=int) for k in KEYS}
    n_extra = 0 if extra is None else len(extra["wells"])
    score_extra = {k: np.full(n_extra, np.nan) for k in KEYS}

    for w in sorted(set(wells)):
        te = np.flatnonzero(wells == w)
        rest = np.flatnonzero(wells != w)
        rest = rest[np.argsort(ts_np[rest], kind="stable")]
        n_va = int(0.15 * len(rest))
        va, tr = rest[-n_va:], rest[:-n_va]
        split_info[w] = {"n_test": int(len(te)), "n_train": int(len(tr)),
                         "n_val": int(len(va)),
                         "prev_test": round(float(y[te].mean()), 4)}
        yw = y[te]
        two = len(np.unique(yw)) > 1
        if not two:
            raise RuntimeError(f"fold {w} test tanpa dua kelas")

        cand = {}
        fitted = {}
        for s in SETS:
            Xs = sets[s]
            med = impute_fit(Xs[tr])
            Xtr = impute_apply(Xs[tr], med)
            Xva = impute_apply(Xs[va], med)
            Xte = impute_apply(Xs[te], med)

            sc = StandardScaler().fit(Xtr)
            lrm = LogisticRegression(max_iter=1000, class_weight="balanced", C=1.0)
            lrm.fit(sc.transform(Xtr), y[tr])
            s_va = lrm.predict_proba(sc.transform(Xva))[:, 1]
            s_te = lrm.predict_proba(sc.transform(Xte))[:, 1]
            cand[f"log_{s}"] = (s_te, tune_thr(y[va], s_va))

            rfm = RandomForestClassifier(**RF_PARAMS)
            rfm.fit(Xtr, y[tr])
            # P7 (determinisme): fit n_jobs=-1 bitwise identik dgn n_jobs=1, TETAPI
            # predict_proba dgn n_jobs=-1 mengakumulasi proba per-pohon dgn urutan
            # joblib tidak tetap -> selisih last-bit (probe code/49: 11/2048 skor
            # beda utk n_jobs -1 vs +1, maks 1,11e-16; repeat mode lama 246/2048
            # beda) -> skor bisa beda antar run. Prediksi serial => byte-identik.
            rfm.n_jobs = 1
            cand[f"rf_{s}"] = (rfm.predict_proba(Xte)[:, 1],
                               tune_thr(y[va], rfm.predict_proba(Xva)[:, 1]))
            imp_acc[f"rf_{s}"].append(rfm.feature_importances_.copy())

            hgm = HistGradientBoostingClassifier(**HGB_PARAMS)
            hgm.fit(Xtr, y[tr])
            cand[f"hgb_{s}"] = (hgm.predict_proba(Xte)[:, 1],
                                tune_thr(y[va], hgm.predict_proba(Xva)[:, 1]))
            fitted[s] = (med, sc, lrm, rfm, hgm)

        # skor out-of-fold utk unit tambahan (P4-S1) — model & imputasi YANG SAMA
        if extra is not None:
            ex_sel = np.flatnonzero(extra["wells"] == w)
            if ex_sel.size:
                for s in SETS:
                    med, sc, lrm, rfm, hgm = fitted[s]
                    Xex = impute_apply(extra["sets"][s][ex_sel], med)
                    score_extra[f"log_{s}"][ex_sel] = \
                        lrm.predict_proba(sc.transform(Xex))[:, 1]
                    score_extra[f"rf_{s}"][ex_sel] = rfm.predict_proba(Xex)[:, 1]
                    score_extra[f"hgb_{s}"][ex_sel] = hgm.predict_proba(Xex)[:, 1]

        row = {}
        for k in KEYS:
            s_te, thr = cand[k]
            pred = (s_te >= thr).astype(int)
            d = {"n": int(len(te)), "n_pos": int(yw.sum()),
                 "prev": round(float(yw.mean()), 4),
                 "pr_auc": ap(yw, s_te),
                 "roc_auc": round(float(roc_auc_score(yw, s_te)), 4),
                 "brier": brier(yw, s_te)}
            d.update(prf(yw, pred))
            d["thr"] = round(float(thr), 5)
            folds[k][w] = d
            pool[k]["y"].append(yw)
            pool[k]["score"].append(s_te)
            pool[k]["pred"].append(pred)
            score_full[k][te] = s_te
            pred_full[k][te] = pred
            row[k] = d["pr_auc"]
        log(f"  [{label}] {SHORT.get(w, w):10s} " +
            " ".join(f"{k}={row.get(k)}" for k in KEYS))

    pooled = {}
    for k in KEYS:
        yP = np.concatenate(pool[k]["y"])
        sP = np.concatenate(pool[k]["score"])
        pP = np.concatenate(pool[k]["pred"])
        bins, ece, maxgap = reliability(yP, sP)
        d = {"n": int(len(yP)), "prev": round(float(yP.mean()), 4),
             "pr_auc": ap(yP, sP),
             "roc_auc": round(float(roc_auc_score(yP, sP)), 4),
             "brier": brier(yP, sP), "ece": ece, "reliability_max_gap": maxgap,
             "reliability_bins": bins}
        d.update(prf(yP, pP))
        d["r_at_p20"] = r_at_p(yP, sP, 0.20)
        d["r_at_p50"] = r_at_p(yP, sP, 0.50)
        d["macro_pr_auc"] = round(float(np.mean(
            [folds[k][w]["pr_auc"] for w in folds[k] if folds[k][w].get("pr_auc") is not None])), 4)
        d["lift"] = round(float(d["pr_auc"] / max(float(yP.mean()), 1e-9)), 3)
        pooled[k] = d
        log(f"  [{label}] POOLED {k:6s} PR-AUC={d['pr_auc']} macro={d['macro_pr_auc']} "
            f"R@P20={d['r_at_p20']} Brier={d['brier']} ECE={d['ece']}")
    return folds, pooled, imp_acc, split_info, score_full, pred_full, score_extra


def macro_table(folds) -> dict:
    out = {}
    for k in KEYS:
        vals = [folds[k][w]["pr_auc"] for w in folds[k]
                if folds[k][w].get("pr_auc") is not None]
        out[k] = round(float(np.mean(vals)), 4) if vals else None
    return out


def gate_eval(folds, macro) -> dict:
    can = folds[CANARY_KEY]
    can_macro = macro[CANARY_KEY]
    target = round(max(TARGET_FLOOR, (can_macro or 0.0) + MARGIN), 4)
    out = {"canary_key": CANARY_KEY, "canary_macro": can_macro,
           "target_formula": f"max({TARGET_FLOOR}, canary + {MARGIN})",
           "target_macro": target, "floor": TARGET_FLOOR, "min_wins": MIN_WINS,
           "canary_exceeds_floor": bool(can_macro is not None and can_macro > TARGET_FLOOR),
           "per_variant": {}}
    for s in ("E", "F"):
        for m in MODELS:
            k = f"{m}_{s}"
            wins, valid, per = 0, 0, {}
            for w in sorted(can):
                a = can[w].get("pr_auc")
                b = folds[k][w].get("pr_auc")
                if a is None or b is None:
                    per[w] = None
                    continue
                valid += 1
                per[w] = round(b - a, 4)
                if b > a:
                    wins += 1
            mac = macro.get(k)
            ok_floor = mac is not None and mac >= TARGET_FLOOR
            ok_target = mac is not None and mac >= target
            ok_wins = valid > 0 and wins >= MIN_WINS
            out["per_variant"][k] = {
                "macro": mac, "wins_vs_canary": f"{wins}/{valid}", "wins_num": wins,
                "n_valid": valid, "delta_per_fold": per,
                "pass_floor_02465": bool(ok_floor), "pass_target": bool(ok_target),
                "pass_wins": bool(ok_wins), "LOLOS": bool(ok_target and ok_wins)}
    out["ada_yang_lolos"] = any(v["LOLOS"] for v in out["per_variant"].values())
    out["verdict_t2d"] = ("LOLOS GATE (subjek re-audit ML Auditor; bukan klaim LULUS penuh)"
                          if out["ada_yang_lolos"] else "GAGAL GATE")
    return out


def importance_groups(imp_mean, names, v2_group_map=None):
    """Agregasi importance RF (train-side, diagnostik) per window & per kelompok."""
    v2_group_map = v2_group_map or {}
    per_window, per_group = {}, {}
    for name, v in zip(names, imp_mean):
        name = str(name)
        if name.startswith("v2__"):
            g = "old:" + v2_group_map.get(name[4:], "v2_other")
        elif name.startswith("old__"):
            g = "old:last_*"
        else:
            parts = name.split("__")
            if len(parts) == 3:
                per_window[parts[0]] = per_window.get(parts[0], 0.0) + float(v)
                g = "ch:" + parts[1]
            else:
                g = "other"
        per_group[g] = per_group.get(g, 0.0) + float(v)
    return {k: round(v, 5) for k, v in sorted(per_window.items(), key=lambda x: -x[1])}, \
        {k: round(v, 5) for k, v in sorted(per_group.items(), key=lambda x: -x[1])}


# =========================================================================
# PART D — dokumen (ditulis dari JSON, 0 angka manual)
# =========================================================================
def write_md(res: dict) -> None:
    L = []
    A = L.append
    # Hasil kampanye T2-e (desain P4) utk seksi hasil; arsip T2-d utk seksi koreksi.
    R = res["p4_desain_baru"]
    K = res.get("koreksi_t2e", {})
    Q = res.get("kekosongan_jendela", {})
    D = res.get("determinisme_p7", {})
    PR = res.get("pra_registrasi_p4", {})
    G = R["gate"]
    S = R.get("sensitivity")

    def cz(v, n=4):
        if v is None:
            return "NA"
        return f"{float(v):.{n}f}".replace(".", ",")

    A("# V2 — BEAT-THE-CANARY: DESAIN P4 SIMETRIS + KOREKSI P1/P2/P3/P7 (T2-e)")
    A("")
    A("Task kanban: `t_471b790f` [ML Engineer] — perbaikan P1/P2/P3/P7 dan desain P4 "
      "pasca audit `t_bdf55b10`; verdict akhir = hak PM/ML Auditor, bukan skrip ini. "
      "Blok hasil desain asli T2-d (task `t_9df689f1`) tetap tersimpan di JSON "
      "top-level dari arsip agar sitasi PM/audit tetap terverifikasi.")
    A("Status: semua angka berasal dari eksekusi `code/46_beat_canary_ts.py`; log: "
      "`docs/V2_ML_BEAT_CANARY_TS_RUN_LOG.txt`; JSON: `docs/V2_ML_BEAT_CANARY_TS.json`.")
    A("")
    A("Framing mengikat (PM audit §3.3, dipakai apa adanya — keputusan PM, tidak diubah):")
    A("> " + FRAMING_33)
    A("")
    A("---")
    A("")
    A("## 0. Koreksi P1/P2/P3, pra-registrasi P4, determinisme P7 (T2-e)")
    A("")
    A(f"- **P1 — SATU definisi + SATU angka** (semua dihitung dari npz, bukan dikutip): "
      f"definisi deviasi protokol (a) = `{Q.get('definisi_jendela_2h_kosong')}` → "
      f"**{Q.get('total_jendela_2h_kosong')} unit** "
      f"({Q.get('positif', {}).get('jendela_2h_kosong')} positif + "
      f"{Q.get('negatif_kontrol_kampanye_asli', {}).get('jendela_2h_kosong')} negatif).")
    A(f"  - Unit NaN varian G = {Q.get('total_unit_NaN_varian_G')} — "
      f"ekivalen dengan jendela 2h kosong: {Q.get('equivalensi_2h_kosong_dgn_NaN_G')} "
      "(dibuktikan per-unit, bukan asumsi).")
    A(f"  - Nilai lama yang dikoreksi: `{(K.get('P1') or {}).get('lama')}`")
    A(f"- **P2 — subset evaluasi sensitivitas**: lama n_eval_neg = "
      f"{(K.get('P2') or {}).get('lama_n_eval_neg')}, benar = "
      f"{(K.get('P2') or {}).get('baru_n_eval_neg')} negatif "
      f"+ {(K.get('P2') or {}).get('n_eval_pos')} positif "
      f"= {(K.get('P2') or {}).get('n_eval_total')} unit "
      f"(dari total {(K.get('P2') or {}).get('n_neg_total', 0)} negatif; "
      f"{(K.get('P2') or {}).get('n_neg_empty_terbuang')} negatif window-kosong ikut "
      f"terbuang oleh mask yang sama). Definisi: {(K.get('P2') or {}).get('definisi')}.")
    _ak = (K.get("P3") or {}).get("kontrol", {})
    _ae = (K.get("P3") or {}).get("event", {})
    A(f"- **P3 — counter anti-leakage per cakupan**: kontrol "
      f"rows_scanned = {nm(_ak.get('rows_scanned'))} "
      f"(violations {_ak.get('violations')}) — {_ak.get('scope')}; "
      f"event T10 rows_scanned = {nm(_ae.get('rows_scanned'))} "
      f"(violations {_ae.get('violations')}) — {_ae.get('scope')}. "
      f"Klaim lama yang dikoreksi: `{(K.get('P3') or {}).get('lama_klaim')}`")
    A(f"- **P4 — pra-registrasi** (komentar {PR.get('komentar_kartu')}): keputusan "
      f"**{PR.get('keputusan')}**; syarat = {PR.get('syarat')}; "
      f"fakta struktur data sebelum kampanye: {PR.get('fakta_struktur_data_sebelum_kampanye')}.")
    A(f"- **P7 — determinisme RF**: status = {D.get('status')}; "
      f"{D.get('kesimpulan', D.get('catatan', ''))} Fix yang diterapkan: "
      f"{D.get('fix', 'rfm.n_jobs = 1 setelah fit (prediksi serial)')}.")
    A("")
    A("---")
    A("")
    A("## 1. Kriteria T2 (dari kartu T2-d) + verdict jujur — desain P4")
    A("")
    A(f"- Syarat: macro-LOWO AUPRC varian ≥ target **{cz(G['target_macro'])}** "
      f"(rumus: {G['target_formula']}; canary time-based = {cz(G['canary_macro'])}; "
      f"lantai {cz(G['floor'])}) **DAN** unggul ≥ **{G['min_wins']}/7** fold vs canary "
      f"varian G (log_MD) pada unit event.")
    A(f"- Canary time-based (G/log) = **{cz(G['canary_macro'])}** "
      f"{'> lantai 0,2465 → target ikut naik' if G['canary_exceeds_floor'] else '≤ lantai 0,2465 → target = lantai'}"
      " (canary lama 0,2265 TIDAK dipakai: unit & resolusi berbeda → tidak sebanding).")
    A(f"- **VERDICT T2-e (desain P4): {G['verdict_t2d']}**")
    if S:
        _ls = ", ".join(k for k, v in S["per_variant"].items() if v["LOLOS"]) or "-"
        A(f"- Sensitivitas PRA-REGISTRASI S1 (§7b): gate dihitung ulang pada set longgar "
          f"({S.get('n_unit_set_panjang')} unit = {S.get('n_pos_set_panjang')} positif + "
          f"{S.get('n_neg_set_panjang')} negatif, termasuk "
          f"{S.get('n_unit_extra_out_of_fold')} positif gugur ketersediaan) → "
          + (f"varian lolos-sens: {_ls}" if S["ada_yang_lolos"]
             else "**TIDAK ADA varian lolos-sens**")
          + " — gate §1 TIDAK berubah; angka ini konsumsi ML Auditor.")
    A("")
    A("| Varian | Model | macro-LOWO | menang vs canary | ≥target | ≥5/7 | LULUS |")
    A("|---|---|---|---|---|---|---|")
    for s in ("E", "F"):
        for m in MODELS:
            k = f"{m}_{s}"
            v = G["per_variant"][k]
            A(f"| {s} | {m} | {cz(v['macro'])} | {v['wins_vs_canary']} | "
              f"{'ya' if v['pass_target'] else 'tidak'} | "
              f"{'ya' if v['pass_wins'] else 'tidak'} | {'✅' if v['LOLOS'] else '❌'} |")
    A("")
    A("## 2. Desain P4 (pra-registrasi — komentar kartu ditulis SEBELUM hasil dilihat)")
    A("")
    A("- **Syarat ketersediaan simetris (P4-ii)**: unit hanya dipakai bila "
      f"`{Q.get('definisi_syarat_ketersediaan_P4')}` — identik untuk kelas positif "
      "dan negatif, dan dipakai pada LATIHAN maupun EVALUASI (satu himpunan unit, "
      "bukan dua). Unit dengan jendela kosong TIDAK MASUK kampanye ini "
      f"({Q.get('positif', {}).get('jendela_2h_kosong')} positif + "
      f"{Q.get('negatif_kontrol_kampanye_asli', {}).get('jendela_2h_kosong')} negatif "
      "gugur).")
    A("- **Unit analisis = event, bukan baris 4-detik** (menghindari pseudo-replication "
      "multiple-rows-per-event): positif = event T10 lolos syarat "
      f"({R['units']['n_pos']} event, dari {R['units']['n_pos_semua_event']}); "
      f"negatif = kontrol anchor WITSML tenang berdata ({R['units']['n_neg']}, "
      f"dari {Q.get('negatif_kontrol_kampanye_asli', {}).get('n_unit')}); "
      "tanpa event start dalam horizon **H = 2 jam** ke depan.")
    A("- **Prevalensi per fold dipertahankan = laju alamiah p_f** (case-control odds-preserving): "
      "`n_neg = round(n_pos·(1−p)/p)` dgn n_pos = event lolos syarat; "
      "sampel uniform tanpa penggantian, **seed 42**; pool tenang = baris tanpa event "
      "di [t, t+H) **dan** lolos syarat ketersediaan.")
    A(f"- **Anti-leakage**: semua sampel fitur `timestamp < anchor` — kontrol "
      f"rows_scanned = {nm(R['anti_leakage']['rows_scanned'])} "
      f"(violations {R['anti_leakage']['violations']}); event T10 "
      f"rows_scanned = {nm(R['anti_leakage_event']['rows_scanned'])} "
      f"(violations {R['anti_leakage_event']['violations']}). Counter dipisah per "
      "cakupan (P3).")
    A("- Fitur lama (F) di-join per unit: wellbore + md terdekat tol **1,0 m** "
      "(tanpa look-ahead); jendela/kanal/statistik = definisi T10 (`code/60`, diimpor langsung).")
    A("")
    A("| Fold | n_pos berdata | n_neg berdata | p alamiah (event dlm 2h) | prevalensi fold | pool tenang | baris sampah th-2015 |")
    A("|---|---|---|---|---|---|---|")
    for f in sorted(R["sampling"]):
        s = R["sampling"][f]
        A(f"| {SHORT.get(f, f)} | {s['n_pos']} | {s['n_neg']} | {cz(s['p_natural_2h'])} | "
          f"{cz(s['prevalence_fold'])} | {s['quiet_pool']} | {s['junk_rows_dropped']} |")
    A("")
    A("## 3. Protokol (identik kampanye 40/42/44)")
    A("")
    A("- LOWO 7 fold; uji = 1 sumur penuh; latih = 6 sumur lain; val = 15% ekor temporal latih "
      "(threshold F1-maks dari skor val); seed 42; StandardScaler logistik fit di latih; "
      "RF/HGB params persis kampanye 40. Satu kampanye, tanpa tuning, output pertama = final.")
    A("- Varian: **G** = 7 statistik MD jendela 2h (canary time-based) · **E** = 480 fitur "
      "time-series (3 jendela × 16 kanal × 10 statistik) · **F** = E + 70 fitur lama "
      "(58 features_v2 + 12 last_*).")
    A("- Deviasi terdokumentasi (desain P4):")
    for dev in R["protocol"]["deviasi_terdokumentasi"]:
        A(f"  - {dev}")
    A(f"- **Determinisme P7**: RF fit parallel tetap (dibuktikan bitwise identik); "
      f"prediksi `predict_proba` dijalankan serial (`rfm.n_jobs = 1`) — status probe: "
      f"{D.get('status')}.")
    A("")
    A("## 4. Hasil per fold (PR-AUC, unit desain P4)")
    A("")
    A("| Fold | n | prev | " + " | ".join(KEYS) + " |")
    A("|---|" + "---|" * (len(KEYS) + 2))
    for w in R["folds"][CANARY_KEY]:
        ref = R["folds"][CANARY_KEY][w]
        cells = []
        for k in KEYS:
            d = R["folds"][k][w]
            cells.append(cz(d.get("pr_auc")) if d.get("pr_auc") is not None else "NA")
        A(f"| {SHORT.get(w, w)} | {ref['n']} | {cz(ref['prev'])} | " + " | ".join(cells) + " |")
    A("")
    A("## 5. Pooled + kalibrasi + recall@P≥0,20")
    A("")
    A("| Model | pooled PR-AUC | macro | prev | lift | R@P≥0,20 | R@P≥0,50 | Brier | ECE 10 bin | F1 @thr-val |")
    A("|---|---|---|---|---|---|---|---|---|---|")
    for k in KEYS:
        d = R["pooled"][k]
        A(f"| {k} | {cz(d['pr_auc'])} | {cz(d['macro_pr_auc'])} | {cz(d['prev'])} | "
          f"{cz(d['lift'], 3)} | {cz(d['r_at_p20'])} | {cz(d['r_at_p50'])} | "
          f"{cz(d['brier'])} | {cz(d['ece'])} | {cz(d['f1'])} |")
    A("")
    A("## 6. Analisis channel/jendela — mana yang menambah? (diagnostik train-side)")
    A("")
    A("- Importance RF rata-rata 7 fold, **hanya dari data latih fold** → petunjuk, BUKAN "
      "pemilihan fitur (seleksi fitur dibekukan pra-registrasi tanpa label).")
    A("")
    for key in ("rf_E", "rf_F"):
        g = R["importances"].get(key, {})
        A(f"**{key}** — top jendela: " + ", ".join(f"{k}={v}" for k, v in
                                                    list(g["per_window"].items())[:3]))
        A("")
        top = [f"{k}={v}" for k, v in list(g["per_group"].items())[:14]]
        A("top kelompok: " + " · ".join(top))
        A("")
    A("- Delta per fold vs canary (varian E): " +
      " · ".join(f"{k}: " + ", ".join(f"{SHORT.get(w, w)}={cz(v)}"
                                      for w, v in G["per_variant"][k]["delta_per_fold"].items())
                 for k in ("log_E", "rf_E", "hgb_E")))
    A("")
    A("## 7. Diagnostik kejujuran")
    A("")
    dgn = R["diagnostics"]
    A(f"- Join fitur lama: matched **{R['join_old']['matched']}/{R['join_old']['n_units']}** "
      f"unit ({R['join_old']['match_rate']}) — sisa NaN diimputasi median latih; "
      "cakupan join per kelas di bawah (confound bila beda jauh):")
    A(f"  - positif (event) match-rate = {dgn['join_match_rate_pos']} · "
      f"negatif (kontrol) match-rate = {dgn['join_match_rate_neg']}")
    A(f"- **Unit dgn jendela kosong TIDAK ADA di kampanye P4** (syarat ketersediaan "
      f"simetris, verifikasi keras di kode — run berhenti bila ≠ 0): "
      f"jendela-2h kosong = {dgn['n_unit_kampanye_jendela_2h_kosong']}, "
      f"jendela-30m kosong = {dgn['n_unit_kampanye_jendela_30m_kosong']}.")
    A("- Fraksi sel NaN (missingness) per kelas — pemeriksaan apakah sisa artefak "
      "missingness masih beda antar kelas:")
    A(f"  - varian G: pos {cz(dgn['frac_nan_sel_G_pos'], 6)} vs neg "
      f"{cz(dgn['frac_nan_sel_G_neg'], 6)}")
    A(f"  - varian E: pos {cz(dgn['frac_nan_sel_E_pos'], 6)} vs neg "
      f"{cz(dgn['frac_nan_sel_E_neg'], 6)}")
    A(f"  - varian F: pos {cz(dgn['frac_nan_sel_F_pos'], 6)} vs neg "
      f"{cz(dgn['frac_nan_sel_F_neg'], 6)}")
    _gk = dgn.get("gugur_ketersediaan", {})
    A(f"- Unit gugur syarat ketersediaan: {_gk.get('positif_dibuang')} positif + "
      f"{_gk.get('negatif_dibuang')} negatif (syarat: {_gk.get('syarat')}).")
    A(f"- Prevalensi pooled unit = {cz(R['units']['prevalence'])} "
      f"({R['units']['n_pos']} positif / {R['units']['n_total']} unit; "
      "odds-preserving per fold, lihat §2).")
    if S:
        A("")
        A("## 7b. Sensitivitas PRA-REGISTRASI S1/S2 (BUKAN bagian gate)")
        A("")
        A(f"- Konteks: pada desain asli, flag jendela kosong hampir penanda kelas "
          f"({Q.get('positif', {}).get('jendela_2h_kosong')} positif vs "
          f"{Q.get('negatif_kontrol_kampanye_asli', {}).get('jendela_2h_kosong')} negatif) "
          "dan missingness-only sempat mengalahkan canary — itulah alasan desain P4. "
          "S1/S2 mengukur ketergantungan kesimpulan pada syarat ketersediaan, memakai "
          "skor out-of-fold model YANG SAMA (tanpa training ulang).")
        A(f"- **S1 set longgar**: {S.get('n_unit_set_panjang')} unit = "
          f"{S.get('n_pos_set_panjang')} positif + {S.get('n_neg_set_panjang')} negatif "
          f"(termasuk {S.get('n_unit_extra_out_of_fold')} positif gugur ketersediaan "
          f"dengan skor out-of-fold).")
        A("- Skor out-of-fold S1 tersimpan di JSON "
          "`p4_desain_baru.pooled_scores_extra` — silakan recompute mandiri "
          "(macro per fold dari gabungan `pooled_scores` + `pooled_scores_extra`).")
        A(f"- **S2 missingness-only** (skor = flag jendela 2h kosong, TANPA sensor; "
          f"dilaporkan TERPISAH): macro AUPRC = "
          f"{cz(S['missingness_only_macro_pr_auc'])}, "
          f"pooled = {cz(S['missingness_only_pooled_pr_auc'])}; "
          f"flag pos {S.get('n_flag_kosong_pos')} vs neg {S.get('n_flag_kosong_neg')}.")
        A(f"- **Limitasi S2 (wajib baca)**: {S.get('catatan_S2')}")
        A(f"- Canary-sens = {cz(S['canary'])} → target-sens = {cz(S['target'])} "
          "(formula sama: max(0,2465, canary+0,02)).")
        A("")
        A("| Varian | Model | macro sens | menang vs canary-sens | ≥target-sens | ≥5/7 | LULUS-sens |")
        A("|---|---|---|---|---|---|---|")
        for s in ("E", "F"):
            for m in MODELS:
                k = f"{m}_{s}"
                v = S["per_variant"][k]
                A(f"| {s} | {m} | {cz(v['macro'])} | {v['wins_vs_canary']} | "
                  f"{'ya' if v['pass_target'] else 'tidak'} | "
                  f"{'ya' if v['pass_wins'] else 'tidak'} | "
                  f"{'✅' if v['LOLOS'] else '❌'} |")
        A("")
        A(f"- **VERDICT S1 (set longgar): "
          + ("ada varian lolos — gate desain P4 tidak bergantung pada syarat "
             "ketersediaan." if S["ada_yang_lolos"] else
             "TIDAK ADA varian lolos pada set longgar — simpulan gate memang "
             "bergantung pada syarat ketersediaan; ML Auditor harus menilai apakah "
             "syarat itu sah (definisi data, bukan seleksi hasil).")
          + "**")
    A("")
    A("## 8. Limitasi (wajib baca sebelum kutip angka)")
    A("")
    A("- Klaim 'prediksi dini berbasis sensor' TIDAK boleh dinaikkan selama framing §3.3 "
      "belum terpenuhi — keputusan PM, tidak diubah oleh kampanye ini.")
    A("- Unit = event dengan kontrol tenang: AUPRC di sini BUKAN angka yang boleh dibandingkan "
      "angka-ke-angka dengan AUPRC dunia baris-md (0,2265); yang sebanding adalah posisi "
      "terhadap canary time-based pada unit yang sama (itu guna varian G).")
    A("- Pemetaan F-15/F-15S ke wellbore = asumsi terkuat, belum tervalidasi independen (T7).")
    A("- VAR_F-5_alt tidak dipakai (keputusan T2-d): konsistensi 7 fold T10 dipertahankan.")
    A(f"- {dgn.get('gugur_ketersediaan', {}).get('positif_dibuang')} positif gugur syarat "
      "ketersediaan TIDAK ikut gate §1 — ketergantungannya diukur di §7b (S1, skor "
      "out-of-fold pada set longgar).")
    A("- Syarat ketersediaan adalah definisi data (unit tanpa sensor di jendela = bukan "
      "observasi), BUKAN penyaringan hasil; tetapi keputusan ini memang mengubah populasi "
      "evaluasi — karenanya S1 wajib dibaca bersama gate.")
    A("- **Ledger eksekusi (bukan tuning)**: kampanye T2-e dijalankan berulang HANYA utk "
      "verifikasi determinisme P7 / perbaikan bug flag S2 — protokol, seed 42, parameter "
      "model, dan himpunan unit TIDAK pernah diubah antar-run (param dibekukan pra-"
      "registrasi; tidak ada loop tuning). Pembanding determinisme: `code/50_cmp_t2e_runs.py`.")
    A("")
    A("## 9. Reproduksi + artefak")
    A("")
    A("```bash")
    A('cd "/mnt/d/Capstone 1"')
    A("python3 code/49_p7_determinisme.py      # probe P7 -> docs/V2_P7_DETERMINISME.json")
    A("python3 code/46_beat_canary_ts.py 2>&1 | tee docs/V2_ML_BEAT_CANARY_TS_RUN_LOG_T2E.txt")
    A("python3 code/47_verify_ts.py            # verifier desain asli (blok arsip)")
    A("python3 code/48_verify_t2e.py           # verifier T2-e (P1-P3/P7/P4/S1/S2)")
    A("python3 code/50_cmp_t2e_runs.py         # determinisme P7: run-1 vs run-2 identik")
    A("python3 code/57_verify_md_json_t2e.py   # helper: angka MD == JSON (6 blok tabel + headline)")
    A("```")
    A("")
    A(f"Runtime terukur desain P4: {R['runtime_seconds']} s "
      f"(arsip T2-d: {res.get('runtime_seconds')} s) — deterministik: "
      "random_state=42, seed 42, RF prediksi serial.")
    A("")
    A("Artefak:")
    A("")
    A("- `code/46_beat_canary_ts.py` (kampanye desain P4 + koreksi P1-P3, rerunnable, exit 0)")
    A("- `code/47_verify_ts.py` (verifier independen: recompute gate/fold wins + sampling + fitur)")
    A("- `code/48_verify_t2e.py` (verifier independen T2-e: P1-P3, P7, unit/gate/S1/S2)")
    A("- `code/49_p7_determinisme.py` (probe determinisme RF -> `docs/V2_P7_DETERMINISME.json`)")
    A("- `code/57_verify_md_json_t2e.py` (helper verifikasi: semua angka MD == JSON)")
    A("- `code/50_cmp_t2e_runs.py` (perbandingan run determinisme P7 — blok inti wajib identik)")
    A("- `data/predictive/features_timeseries_controls_berdata.npz` (kontrol P4 + meta/sampling)")
    A("- `data/predictive/controls_shards_berdata/` (shard per fold desain P4, cache deterministik)")
    A("- `docs/V2_ML_BEAT_CANARY_TS_T2D_ARSIP.json` (arsip byte-identik JSON T2-d)")
    A("- `docs/V2_ML_BEAT_CANARY_TS.json` (semua angka primer: arsip top-level + p4_desain_baru)")
    A("- `docs/V2_ML_BEAT_CANARY_TS.md` (dokumen ini — ditulis skrip dari JSON, 0 angka manual)")
    A("- `docs/V2_ML_BEAT_CANARY_TS_RUN_LOG.txt` (log eksekusi)")
    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")


def hitung_kekosongan(XM_pos, XB_pos) -> dict:
    """Fakta P1 — SEMUA definisi kekosongan dihitung dari npz (0 angka manual).

    Definisi resmi utk deviasi protokol (a) = "jendela 2h kosong"
    (0 baris WITSML dalam [anchor-2h, anchor)) karena H=2h dan varian G memakai w2h.
    Angka lain (30m/6h) hanya dipakai bila definisinya ikut ditulis.
    """
    def cnt(XM, XB):
        d = {"n_unit": int(len(XM)),
             "jendela_30m_kosong": int((XM[:, 0] == 0).sum()),
             "jendela_2h_kosong": int((XM[:, 4] == 0).sum()),
             "jendela_6h_kosong": int((XM[:, 8] == 0).sum()),
             "ketiga_jendela_kosong": int(((XM[:, 0] == 0) & (XM[:, 4] == 0)
                                           & (XM[:, 8] == 0)).sum()),
             "non_kosong_semua": int(((XM[:, 0] > 0) & (XM[:, 4] > 0)
                                      & (XM[:, 8] > 0)).sum()),
             "unit_NaN_varian_G": int((~np.isfinite(XB[:, 0:7])).any(axis=1).sum())}
        return d

    p = cnt(XM_pos, XB_pos)
    n = None
    if CONTROLS_NPZ.exists():
        c = np.load(CONTROLS_NPZ, allow_pickle=True)
        n = cnt(c["X_window_meta"].astype(np.float64),
                c["X_baseline"].astype(np.float64))
    tot_2h = p["jendela_2h_kosong"] + (n["jendela_2h_kosong"] if n else 0)
    tot_g = p["unit_NaN_varian_G"] + (n["unit_NaN_varian_G"] if n else 0)
    return {
        "definisi_jendela_2h_kosong": "unit tanpa satu pun baris WITSML dalam "
                                      "[anchor-2h, anchor) — definisi resmi utk "
                                      "deviasi protokol (a) 'set md bisa NaN'",
        "definisi_ketiga_jendela_kosong": "n_rows(w30m)=n_rows(w2h)=n_rows(w6h)=0 "
                                          "(jendela bersarang: 30m < 2h < 6h)",
        "definisi_syarat_ketersediaan_P4": "n_rows(w30m) >= 1 (≡ ketiga jendela non-kosong)",
        "positif": p,
        "negatif_kontrol_kampanye_asli": n,
        "total_jendela_2h_kosong": tot_2h,
        "total_unit_NaN_varian_G": tot_g,
        "equivalensi_2h_kosong_dgn_NaN_G": bool(tot_2h == tot_g),
        "angka_lain": ["194 = jendela 30m kosong (positif)",
                       "191 = jendela 2h kosong (positif)",
                       "185 = jendela 6h kosong / ketiga jendela kosong (positif)"],
    }


def determinisme_p7() -> dict:
    """Baca hasil probe determinisme (code/49_p7_determinisme.py) utk laporan P7."""
    if not P7_JSON.exists():
        return {"status": "belum_diukur",
                "catatan": "jalankan: python3 code/49_p7_determinisme.py"}
    d = json.load(open(P7_JSON))
    d.setdefault("status", "diukur")
    return d


def muat_arsip_t2d(kekosongan: dict) -> dict:
    """Baca arsip JSON kampanye T2-d + terapkan koreksi P1/P2/P3.

    Semua angka koreksi dihitung ulang dari data tersimpan (pooled_scores arsip,
    npz, meta T10) — 0 angka manual. Blok asli dipertahankan di JSON top-level
    agar sitasi PM (V2_PM_VERDICT_FINAL.md) dan recompute tetap terverifikasi.
    """
    if not ARCHIVE_JSON.exists():
        raise RuntimeError(f"arsip T2-d tidak ada: {ARCHIVE_JSON}")
    a = json.load(open(ARCHIVE_JSON))
    corr = {}

    # ---- P1: SATU definisi + SATU angka untuk deviasi protokol (a) ----
    d2h = kekosongan["definisi_jendela_2h_kosong"]
    p2h = kekosongan["positif"]["jendela_2h_kosong"]
    n2h = kekosongan["negatif_kontrol_kampanye_asli"]["jendela_2h_kosong"]
    tot = kekosongan["total_jendela_2h_kosong"]
    corr["P1"] = {"lama": a["protocol"]["deviasi_terdokumentasi"][0],
                  "baru": None,
                  "fakta": {"jendela_2h_kosong_pos": p2h, "jendela_2h_kosong_neg": n2h,
                            "total": tot,
                            "unit_NaN_varian_G": kekosongan["total_unit_NaN_varian_G"],
                            "ekivalen": kekosongan["equivalensi_2h_kosong_dgn_NaN_G"]}}
    corr["P1"]["baru"] = (
        f"set md bisa NaN: {d2h} -> {tot} unit ({p2h} positif + {n2h} negatif); "
        f"unit NaN pada varian G = {kekosongan['total_unit_NaN_varian_G']} "
        f"(ekivalen, dibuktikan); imputasi median LATIH seragam semua varian")
    a["protocol"]["deviasi_terdokumentasi"][0] = corr["P1"]["baru"]

    # ---- P2: subset evaluasi sensitivitas = yang benar-benar dieksekusi ----
    ps = a["pooled_scores"]
    y = np.asarray(ps["y"], dtype=int)
    emp = np.asarray(ps["empty_window_pos"], dtype=bool)
    ev_pos = int(((y == 1) & ~emp).sum())
    ev_neg = int(((y == 0) & ~emp).sum())
    corr["P2"] = {"lama_n_eval_neg": a["sensitivity"].get("n_eval_neg"),
                  "baru_n_eval_neg": ev_neg, "n_eval_pos": ev_pos,
                  "n_eval_total": ev_pos + ev_neg,
                  "n_neg_total": int((y == 0).sum()),
                  "n_neg_empty_terbuang": int(((y == 0) & emp).sum()),
                  "definisi": "mask ~empty (jendela 2h tidak kosong) pada unit "
                              "desain asli — 1 negatif window-kosong ikut terbuang"}
    a["sensitivity"]["n_eval_pos"] = ev_pos
    a["sensitivity"]["n_eval_neg"] = ev_neg
    a["sensitivity"]["n_eval_total"] = ev_pos + ev_neg
    a["sensitivity"]["n_neg_total"] = corr["P2"]["n_neg_total"]
    a["sensitivity"]["n_neg_empty_excluded"] = corr["P2"]["n_neg_empty_terbuang"]
    a["sensitivity"]["subset_eval_definisi"] = corr["P2"]["definisi"]

    # ---- P3: counter anti-leakage dipisah per cakupan ----
    meta10 = json.load(open(BASE / "data" / "predictive" / "features_timeseries_meta.json"))
    n_ctrl_units = int(kekosongan["negatif_kontrol_kampanye_asli"]["n_unit"])
    a["anti_leakage"] = {
        "violations": int(a["anti_leakage"]["violations"]),
        "rows_scanned": int(a["anti_leakage"]["rows_scanned"]),
        "scope": f"kontrol ({n_ctrl_units} anchor) saja — part A code/46; "
                 "bukan cakupan unit event"}
    a["anti_leakage_event"] = {
        "violations": int(meta10["anti_leakage"]["violations"]),
        "rows_scanned": int(meta10["anti_leakage"]["rows_scanned"]),
        "scope": "661 event T10 (part A code/60), counter terpisah",
        "source": "data/predictive/features_timeseries_meta.json"}
    corr["P3"] = {"lama_klaim": "MD §2: 'semua sampel ... rows_scanned = 67.731.473'",
                  "kontrol": a["anti_leakage"], "event": a["anti_leakage_event"]}
    a["koreksi_t2e"] = corr
    return a


def main() -> int:
    t_start = time.time()
    mod = load_t10()

    # ---------- A. unit positif (T10) ----------
    z = np.load(EVENTS_NPZ, allow_pickle=True)
    X_pos_all = z["X"].astype(np.float64)
    XB_pos_all = z["X_baseline"].astype(np.float64)
    XM_pos_all = z["X_window_meta"].astype(np.float64)
    ev_fold_all = np.array([str(f) for f in z["fold"]], dtype=object)
    ev_wb_all = np.array([str(w) for w in z["wellbore"]], dtype=object)
    ev_ts_all = np.array([pd.Timestamp(str(t)).value for t in z["act_start_utc"]],
                         dtype="int64")
    ev_id_all = z["event_id"].astype(np.int64)

    # ---------- A2. fakta kekosongan (P1) + syarat ketersediaan (P4) ----------
    # Syarat pra-registrasi P4: ketiga jendela non-kosong (bersarang => cukup
    # n_rows(w30m) >= 1). Berlaku sama utk positif & negatif, latih + evaluasi.
    avail_all = XM_pos_all[:, 0] > 0
    kekosongan = hitung_kekosongan(XM_pos_all, XB_pos_all)
    avail_by_fold = {f: avail_all[ev_fold_all == f] for f in sorted(set(ev_fold_all))}
    sel = np.flatnonzero(avail_all)          # positif lolos syarat (467)
    exc = np.flatnonzero(~avail_all)         # positif dibuang (194) -> sensitivitas S1
    log(f"positif: {len(sel)}/{len(avail_all)} lolos syarat ketersediaan "
        f"(dibuang {len(exc)}); fakta kekosongan: {json.dumps(kekosongan)}")
    # preflight: arsip T2-d + koreksi P1-P3 harus bisa dimuat SEBELUM kampanye panjang
    arsip = muat_arsip_t2d(kekosongan)
    _p2 = arsip["koreksi_t2e"]["P2"]
    log(f"preflight arsip OK: {ARCHIVE_JSON.name} | P1 baru "
        f"{arsip['koreksi_t2e']['P1']['fakta']['total']} unit | P2 n_eval_neg "
        f"{_p2['lama_n_eval_neg']} -> {_p2['baru_n_eval_neg']} | P3 kontrol rows "
        f"{arsip['anti_leakage']['rows_scanned']} / event "
        f"{arsip['anti_leakage_event']['rows_scanned']} | P7 "
        f"{determinisme_p7().get('status')}")

    X_pos, XB_pos, XM_pos = X_pos_all[sel], XB_pos_all[sel], XM_pos_all[sel]
    ev_fold, ev_wb, ev_ts, ev_id = (ev_fold_all[sel], ev_wb_all[sel],
                                    ev_ts_all[sel], ev_id_all[sel])
    y_pos = np.ones(len(ev_ts), dtype=np.int64)

    # ---------- A. unit negatif (kontrol, desain P4: syarat ketersediaan sama) ----------
    if CONTROLS_NPZ_B.exists():
        c = np.load(CONTROLS_NPZ_B, allow_pickle=True)
        sampling = json.loads(str(c["sampling_meta"]))
        controls = {"X": c["X"].astype(np.float64), "XB": c["X_baseline"].astype(np.float64),
                    "XM": c["X_window_meta"].astype(np.float64),
                    "fold": np.array([str(f) for f in c["fold"]], dtype=object),
                    "anchor_ts": c["anchor_ts"].astype("int64"),
                    "y": c["y"].astype(np.int64),
                    "sampling_meta": sampling, "npz_path": str(CONTROLS_NPZ_B),
                    "shard_dir": str(SHARD_DIR_B),
                    "anti_leakage": {"violations": int(c["anti_violations"]),
                                     "rows_scanned": int(c["anti_rows_scanned"]),
                                     "scope": f"kontrol ({len(c['anchor_ts'])} anchor, "
                                              "jalur kode ini)"}}
        log(f"kontrol: npz berdata ada ({len(controls['fold'])} anchor) — dipakai ulang")
    else:
        controls = build_controls(mod, z, avail_map=avail_by_fold, shard_dir=SHARD_DIR_B,
                                  controls_npz=CONTROLS_NPZ_B, design_tag="berdata")
    log(f"negatif: {len(controls['fold'])} kontrol | sampling: "
        + json.dumps(controls["sampling_meta"]))

    if int(controls["anti_leakage"]["violations"]) > 0:
        log("LEAKAGE pada kontrol > 0 — STOP")
        return 3

    # ---------- B. susun matriks ----------
    n_pos, n_neg = len(ev_ts), len(controls["anchor_ts"])
    y = np.concatenate([y_pos, controls["y"].astype(np.int64)])
    wells = np.concatenate([ev_wb, np.array([mod.FOLD2LABEL[f] for f in controls["fold"]],
                                            dtype=object)])
    folds_all = np.concatenate([ev_fold, controls["fold"]])
    ts_all = np.concatenate([ev_ts, controls["anchor_ts"]])
    order = np.argsort(ts_all, kind="stable")
    y, wells, folds_all, ts_all = y[order], wells[order], folds_all[order], ts_all[order]

    X_ts = np.vstack([X_pos, controls["X"]]).astype(np.float64)[order]
    XB = np.vstack([XB_pos, controls["XB"]]).astype(np.float64)[order]
    X_wm = np.vstack([XM_pos, controls["XM"]]).astype(np.float64)[order]

    # fitur lama (join wellbore + md terdekat) — utk unit kampanye + unit extra (S1)
    lab = pd.read_csv(LABELS, usecols=["event_id", "md"])
    md_pos = lab.set_index("event_id")["md"].reindex(ev_id).to_numpy(dtype=np.float64)
    md_ctrl = controls["XB"][:, 5]           # md_last (DMEA terakhir di jendela 2h)
    md_all = np.concatenate([md_pos, md_ctrl])[order]
    wb_all = wells
    # unit EXTRA = positif yg gugur syarat ketersediaan (hanya utk sensitivitas S1)
    wb_ex = ev_wb_all[exc]
    md_ex = lab.set_index("event_id")["md"].reindex(ev_id_all[exc]).to_numpy(dtype=np.float64)
    old_full, old_names, meta_full = join_old_features(np.concatenate([wb_all, wb_ex]),
                                                       np.concatenate([md_all, md_ex]))
    n_p4 = len(wb_all)
    old_all, old_ex = old_full[:n_p4], old_full[n_p4:]
    mmask_full = meta_full.pop("matched_mask")
    join_meta = {**meta_full, "matched": int(mmask_full[:n_p4].sum()),
                 "n_units": int(n_p4),
                 "match_rate": round(float(mmask_full[:n_p4].mean()), 4),
                 "matched_mask": mmask_full[:n_p4],
                 "unit_extra_sensitivitas": {"n_units": int(len(wb_ex)),
                                             "matched": int(mmask_full[n_p4:].sum()),
                                             "match_rate": round(
                                                 float(mmask_full[n_p4:].mean()), 4)}}
    log(f"join fitur lama: {join_meta['matched']}/{join_meta['n_units']} "
        f"({join_meta['match_rate']}), kolom={len(old_names)}; "
        f"unit extra {join_meta['unit_extra_sensitivitas']}")

    sets = {
        "G": XB[:, 0:7],                                   # canary: MD saja (7)
        "E": X_ts,                                         # time-series 480
        "F": np.hstack([X_ts, old_all]),                   # TS + fitur lama
    }
    # matriks unit extra (positif gugur ketersediaan) utk skor out-of-fold S1
    XB_ex = XB_pos_all[exc]
    X_ts_ex = X_pos_all[exc]
    sets_ex = {"G": XB_ex[:, 0:7], "E": X_ts_ex,
               "F": np.hstack([X_ts_ex, old_ex])}
    # P7-S2: flag kekosongan unit extra dihitung dari npz (kolom 4 = n_rows w2h),
    # BUKAN dihardcode. 194 gugur = 191 kosong-2h + 3 hanya kosong-30m, jadi flag
    # "jendela 2h kosong" utk unit extra = 191 (yg 3 unit: 2h terisi, 30m kosong).
    empty_2h_ex = XM_pos_all[exc][:, 4] == 0
    if int(empty_2h_ex.sum()) != int(kekosongan["positif"]["jendela_2h_kosong"]):
        log(f"STOP: flag 2h unit extra {int(empty_2h_ex.sum())} != total positif "
            f"kosong-2h {kekosongan['positif']['jendela_2h_kosong']} "
            "(kampanye P4 harusnya 0 unit kosong)")
        return 4
    extra = {"sets": sets_ex, "wells": wb_ex, "y": np.ones(len(wb_ex), dtype=np.int64),
             "empty_2h": empty_2h_ex}
    set_meta = {"G": {"cols": 7, "desc": "baseline MD jendela 2h (canary time-based)"},
                "E": {"cols": int(X_ts.shape[1]), "desc": "fitur time-series T10 (3 jendela)"},
                "F": {"cols": int(sets["F"].shape[1]),
                      "desc": "E + 58 features_v2 + 12 last_* (join md tol 1 m)"}}
    log(f"unit total: {len(y)} (pos {int(y.sum())}, prev {y.mean():.4f}); "
        f"unit extra S1: {len(wb_ex)} (semua positif gugur ketersediaan)")

    if sorted(set(folds_all)) != sorted(mod.FOLD2LABEL):
        log(f"fold tidak persis 7: {sorted(set(folds_all))} — STOP")
        return 3

    # ---------- C. kampanye ----------
    folds_res, pooled, imp_acc, split_info, score_full, pred_full, score_extra = run_arm(
        sets, y, ts_all, wells, KEYS, "main", extra=extra)
    macro = macro_table(folds_res)
    gate = gate_eval(folds_res, macro)
    log(f"GATE: canary={gate['canary_macro']} target={gate['target_macro']} "
        f"verdict={gate['verdict_t2d']}")

    # ---------- diagnostik importance (train-side) ----------
    v2meta = json.load(open(BASE / "data" / "predictive" / "features_v2_meta.json"))
    v2_group_map = {}
    for gname, cols in v2meta.get("groups", {}).items():
        for c in cols:
            v2_group_map[c] = gname
    imps = {}
    for key, names in (("rf_E", list(z["feature_names"])),
                       ("rf_F", list(z["feature_names"]) + old_names)):
        arr = np.vstack(imp_acc[key])
        pw, pg = importance_groups(arr.mean(axis=0), names, v2_group_map)
        imps[key] = {"per_window": pw, "per_group": pg}

    # ---------- diagnostik kejujuran desain P4 ----------
    pos_mask = (y == 1)
    # verifikasi keras: TIDAK ADA unit kampanye dgn jendela kosong (syarat P4)
    empty2h_ord = np.concatenate([XM_pos[:, 4] == 0, controls["XM"][:, 4] == 0])[order]
    empty30m_ord = np.concatenate([XM_pos[:, 0] == 0, controls["XM"][:, 0] == 0])[order]
    if empty2h_ord.any() or empty30m_ord.any():
        log(f"SYARAT KETERSEDIAAN P4 dilanggar: kosong-2h={int(empty2h_ord.sum())} "
            f"kosong-30m={int(empty30m_ord.sum())} — STOP")
        return 3
    mmask = join_meta.pop("matched_mask")
    klog = "log_E"

    def frac_nan(X, m):
        return round(float((~np.isfinite(X[m])).mean()), 6) if m.any() else None

    n_neg = int(n_neg)
    dgn = {
        "join_match_rate_pos": round(float(mmask[pos_mask].mean()), 4),
        "join_match_rate_neg": round(float(mmask[~pos_mask].mean()), 4),
        "n_unit_kampanye_jendela_2h_kosong": int(empty2h_ord.sum()),
        "n_unit_kampanye_jendela_30m_kosong": int(empty30m_ord.sum()),
        "frac_nan_sel_G_pos": frac_nan(sets["G"], pos_mask),
        "frac_nan_sel_G_neg": frac_nan(sets["G"], ~pos_mask),
        "frac_nan_sel_E_pos": frac_nan(sets["E"], pos_mask),
        "frac_nan_sel_E_neg": frac_nan(sets["E"], ~pos_mask),
        "frac_nan_sel_F_pos": frac_nan(sets["F"], pos_mask),
        "frac_nan_sel_F_neg": frac_nan(sets["F"], ~pos_mask),
        "score_diagnostics_key": klog,
        "gugur_ketersediaan": {
            "positif_dibuang": int(len(exc)),
            "negatif_dibuang": int(kekosongan["negatif_kontrol_kampanye_asli"]["n_unit"]
                                   - n_neg),
            "syarat": kekosongan["definisi_syarat_ketersediaan_P4"],
        },
    }

    # ---------- sensitivitas PRA-REGISTRASI desain P4 (BUKAN bagian gate) ----------
    # S1 "evaluasi longgar": semua 661 event (tanpa syarat ketersediaan) + kontrol
    #     desain baru, memakai skor out-of-fold dari model YANG SAMA (tanpa training
    #     ulang) -> mengukur ketergantungan kesimpulan pada syarat ketersediaan.
    # S2 "flag terpisah": baseline hanya-flag-kosong pada set S1 (TANPA sensor),
    #     dilaporkan TERPISAH dari skor sensor.
    y_long = np.concatenate([y, extra["y"]])
    wells_long = np.concatenate([wells, extra["wells"]])
    empty_long = np.concatenate([empty2h_ord, extra["empty_2h"]])
    score_long = {k: np.concatenate([score_full[k], score_extra[k]]) for k in KEYS}
    if np.isnan(np.concatenate(list(score_long.values()))).any():
        log("skor S1 belum lengkap (NaN out-of-fold) — STOP")
        return 3
    sens_folds = {k: {} for k in KEYS}
    for w in sorted(set(wells_long)):
        m = wells_long == w
        yw = y_long[m]
        for k in KEYS:
            v = ap(yw, score_long[k][m])
            sens_folds[k][w] = {"n": int(m.sum()), "n_pos": int(yw.sum()), "pr_auc": v}
    sens_macro = {}
    for k in KEYS:
        vals = [sens_folds[k][w]["pr_auc"] for w in sens_folds[k]
                if sens_folds[k][w]["pr_auc"] is not None]
        sens_macro[k] = round(float(np.mean(vals)), 4) if vals else None
    can_s = sens_macro[CANARY_KEY]
    target_s = round(max(TARGET_FLOOR, (can_s or 0.0) + MARGIN), 4)
    sens_per = {}
    for k in [x for x in KEYS if x != CANARY_KEY and x[-1] in ("E", "F")]:
        wins, valid = 0, 0
        for w in sens_folds[k]:
            a = sens_folds[CANARY_KEY][w].get("pr_auc")
            b = sens_folds[k][w].get("pr_auc")
            if a is None or b is None:
                continue
            valid += 1
            wins += b > a
        mac = sens_macro[k]
        ok = mac is not None and mac >= target_s and wins >= MIN_WINS
        sens_per[k] = {"macro": mac, "wins_vs_canary": f"{wins}/{valid}", "wins_num": wins,
                       "n_valid": valid, "pass_target": bool(mac is not None and mac >= target_s),
                       "pass_wins": bool(valid > 0 and wins >= MIN_WINS),
                       "LOLOS": bool(ok)}
    mscore = empty_long.astype(np.float64)
    sens = {
        "pra_registrasi": True,
        "komentar_kartu": "kanban t_471b790f comment 24 (ditulis sebelum hasil dilihat)",
        "desc": "S1 evaluasi longgar: gate dihitung ulang pada set SEMUA 661 event "
                "(tanpa syarat ketersediaan) + kontrol desain baru, memakai skor "
                "out-of-fold model desain baru (tanpa training ulang) — BUKAN bagian gate",
        "n_unit_set_panjang": int(len(y_long)),
        "n_pos_set_panjang": int(y_long.sum()),
        "n_neg_set_panjang": int((y_long == 0).sum()),
        "n_unit_extra_out_of_fold": int(len(extra["wells"])),
        "folds": sens_folds, "macro": sens_macro,
        "canary": can_s, "target_formula": f"max({TARGET_FLOOR}, canary + {MARGIN})",
        "target": target_s, "per_variant": sens_per,
        "ada_yang_lolos": any(v["LOLOS"] for v in sens_per.values()),
        "verdict": ("S1: ADA varian lolos pada set longgar" if any(
            v["LOLOS"] for v in sens_per.values())
            else "S1: TIDAK ADA varian lolos pada set longgar"),
        "missingness_only_desc": "S2: skor = flag jendela 2h kosong (1/0), TANPA sensor; "
                                 "dilaporkan terpisah dari skor sensor",
        "missingness_only_pooled_pr_auc": ap(y_long, mscore),
        "missingness_only_macro_pr_auc": round(float(np.nanmean(
            [ap(y_long[wells_long == w], mscore[wells_long == w])
             for w in sorted(set(wells_long))])), 4),
        "n_flag_kosong_pos": int(((y_long == 1) & empty_long).sum()),
        "n_flag_kosong_neg": int(((y_long == 0) & empty_long).sum()),
        "catatan_S2": (
            "Pada set longgar, negatif = kontrol desain baru (semua lolos syarat "
            "ketersediaan, pool difilter dgn syarat identik) sehingga flag=1 hanya "
            "mungkin pada positif (flag⇒positif per konstruksi sampling). S2 karena "
            "itu = batas-atas artifaktual dari sinyal kekosongan pada desain ini, "
            "bukan perbandingan adil kelas; angka dilaporkan terpisah dari skor "
            "sensor dan TIDAK dipakai utk klaim mengalahkan canary."),
    }
    log(f"SENS S1 (evaluasi longgar): canary={can_s} target={target_s} "
        f"lolos={sens['ada_yang_lolos']} | S2 missingness-only macro="
        f"{sens['missingness_only_macro_pr_auc']} "
        f"(flag pos {sens['n_flag_kosong_pos']} vs neg {sens['n_flag_kosong_neg']})")

    # ---------- susun JSON: top-level = desain asli T2-d (arsip, P1-P3 dikoreksi);
    #            p4_desain_baru = kampanye T2-e ---------- (arsip sudah dimuat preflight)
    res = dict(arsip)
    res["task"] = ("t_471b790f [ML Engineer] T2-e — perbaikan P1/P2/P3/P7 + desain P4; "
                   "blok top-level = kampanye T2-d asli dari arsip (P1-P3 dikoreksi), "
                   "hasil kampanye T2-e ada di p4_desain_baru")
    res["task_asli"] = arsip.get("task")
    res["generated_at_utc"] = datetime.now(timezone.utc).isoformat()
    res["arsip_provenance"] = {
        "file": str(ARCHIVE_JSON),
        "isi": "salinan byte-identik JSON kampanye T2-d (t_9df689f1) sebelum T2-e",
        "catatan": "blok top-level TIDAK dihitung ulang; angkanya berasal dari "
                   "eksekusi T2-d yang diverifikasi ML Auditor (recompute fold-AP "
                   "63/63, MD==JSON byte-identik)",
    }
    res["kekosongan_jendela"] = kekosongan
    res["koreksi_t2e"] = arsip["koreksi_t2e"]
    res["determinisme_p7"] = determinisme_p7()
    res["pra_registrasi_p4"] = PRA_REGISTRASI_P4

    p4 = {
        "pra_registrasi": PRA_REGISTRASI_P4,
        "protocol": {
            "lowo_folds": sorted(mod.FOLD2LABEL),
            "val": "15% ekor temporal latih; threshold F1-maks dari skor val",
            "seed": SEED, "models": MODELS,
            "rf_params": {**RF_PARAMS, "predict_n_jobs": 1},
            "hgb_params": HGB_PARAMS,
            "scaler": "StandardScaler fit di latih (logistik)",
            "identik_kampanye": ["40_beat_canary.py", "42_sensor_increment.py",
                                 "44_beat_canary_v2.py"],
            "deviasi_terdokumentasi": [
                f"syarat ketersediaan P4 ({kekosongan['definisi_syarat_ketersediaan_P4']}) "
                f"membuang {len(exc)} positif + "
                f"{kekosongan['negatif_kontrol_kampanye_asli']['n_unit'] - n_neg} negatif "
                "-> TIDAK ADA unit dgn jendela kosong di kampanye ini",
                "sisa NaN (kanal tanpa data dalam jendela + join fitur lama) tetap "
                "diimputasi median LATIH seragam semua varian",
                "tanpa lengan delta (resolusi waktu); horizon H=2h mendefinisikan label",
                "canary G dihitung segar pada desain baru (canary beku 0,2265 tidak sebanding)"],
        },
        "design": {
            "unit": "event berdata (1 baris/event, syarat ketersediaan) + kontrol "
                    "anchors berdata (negatif)",
            "syarat_ketersediaan": kekosongan["definisi_syarat_ketersediaan_P4"],
            "simetris": "syarat identik utk positif & negatif, berlaku pd latih + evaluasi",
            "horizon_h": HORIZON_S / 3600,
            "sampling": "odds-preserving case-control per fold: n_neg=round(n_pos*(1-p)/p), "
                        "pool tenang difilter syarat ketersediaan, uniform tanpa "
                        "penggantian",
            "seed": SEED, "md_tol_m": MD_TOL,
            "anti_leakage": "semua sampel fitur: timestamp < anchor (jalur kode identik T10)",
            "variants": set_meta,
            "time_features_used": False,
            "var_f5_alt_used": False,
        },
        "anti_leakage": controls["anti_leakage"],
        "anti_leakage_event": dict(arsip["anti_leakage_event"],
                                   scope="661 event T10 (part A code/60) — dipakai "
                                         "juga utk unit extra S1"),
        "sampling": controls["sampling_meta"],
        "units": {"n_pos": int(n_pos), "n_neg": int(n_neg),
                  "n_total": int(len(y)), "prevalence": round(float(y.mean()), 4),
                  "n_pos_semua_event": int(len(avail_all)),
                  "n_pos_gugur_ketersediaan": int(len(exc))},
        "join_old": join_meta,
        "folds": folds_res, "pooled": pooled, "macro": macro,
        "split_info": split_info,
        "gate": gate, "importances": imps, "diagnostics": dgn,
        "sensitivity": sens,
        "pooled_scores": {"y": y.astype(int).tolist(),
                          "empty_window_pos": empty2h_ord.astype(bool).tolist(),
                          "wells": wells.astype(str).tolist(),
                          "keys": {k: {"score": [float(v) for v in score_full[k]],
                                       "pred": pred_full[k].astype(int).tolist()}
                                   for k in KEYS}},
        "pooled_scores_extra": {
            "desc": "unit positif yg gugur syarat ketersediaan, skor out-of-fold "
                    "dari model desain P4 (tanpa training ulang) — bahan verifikasi S1",
            "y": extra["y"].astype(int).tolist(),
            "wells": extra["wells"].astype(str).tolist(),
            "empty_window_2h": extra["empty_2h"].astype(bool).tolist(),
            "keys": {k: {"score": [float(v) for v in score_extra[k]]} for k in KEYS},
            "n_nan_per_key": {k: int(np.isnan(score_extra[k]).sum()) for k in KEYS},
        },
        "runtime_seconds": round(time.time() - t_start, 1),
    }
    res["p4_desain_baru"] = p4
    res["runtime_seconds_p4"] = p4["runtime_seconds"]
    json.dump(res, open(OUT_JSON, "w"), indent=1, ensure_ascii=False, default=str)
    write_md(res)
    log(f"JSON ditulis: {OUT_JSON}")
    log(f"MD ditulis: {OUT_MD}")
    log(f"VERIFIED P4: folds={len(mod.FOLD2LABEL)}, units={len(y)} "
        f"(pos {int(y.sum())}), extra_S1={len(extra['wells'])}, "
        f"canary={gate['canary_macro']}, target={gate['target_macro']}, "
        f"lolos={gate['ada_yang_lolos']} | S1 lolos={sens['ada_yang_lolos']} | "
        f"violations kontrol={p4['anti_leakage']['violations']} "
        f"event={p4['anti_leakage_event']['violations']} | "
        f"unit_kosong_dlm_kampanye={dgn['n_unit_kampanye_jendela_2h_kosong']} | "
        f"runtime P4={p4['runtime_seconds']}s (arsip T2-d {res['runtime_seconds']}s)")
    print("DONE", flush=True)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        import traceback
        traceback.print_exc()
        sys.exit(1)
