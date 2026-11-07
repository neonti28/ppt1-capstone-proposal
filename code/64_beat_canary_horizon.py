#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
code/64_beat_canary_horizon.py — Kampanye T2-f JALUR 2: horizon 6 jam
(anchors digeser ke act_start − 6h, ZONA DATA-MENGALIR → missingness tak bisa
jadi sinyal). Kanban task: t_66037ed6 [ML Engineer] — SATU kampanye, TANPA
tuning, seed 42; PRA-REGISTRASI = komentar kartu t_66037ed6 comment 33
(ditulis SEBELUM run pertama; bukti = timestamp komentar < generated_at ini).

PERTANYAAN (kriteria kartu T2-f, diuji apa adanya):
  Dari data sensor yang BERAKHIR 6 jam sebelum event, apakah ada varian fitur
  yang macro-LOWO AUPRC >= target DAN unggul >=5/7 fold vs canary-MD (varian
  G/log) pada unit & horizon yang SAMA (canary dihitung segar)?
  target = max(0,2465 ; canary + 0,02)  — lantai TIDAK boleh diubah pasca-hasil.

DESAIN (dibekukan di pra-registrasi comment 33; desain = poin 1–6 kartu):
  ANCHOR POSITIF : a = act_start − 6 jam (fitur T10 jalur kode identik, semua
                   sampel timestamp < a; jendela beku T10 w30m/w2h/w6h ->
                   cakupan efektif [act_start−12h, act_start−6h)).
                   (klarifikasi pra-registrasi: body kartu menulis −24h; jendela
                   T10 terlebar 6h sehingga tanpa fitur baru batasnya 12h)
  NEGATIF        : kontrol berdata desain T2-e DIPAKAI ULANG byte-identik
                   (data/predictive/features_timeseries_controls_berdata.npz +
                   shard) — aturan seleksinya identik bentuk dengan aturan
                   positif; tanpa rebuild/resample sehingga mustahil ada
                   pemilihan hasil pasca-hasil.
  KETERSEDIAAN   : aturan P4 T2-e, simetris — n_rows(w30m @ anchor kelas
                   masing-masing) >= 1, berlaku latih + evaluasi. Positif yang
                   gugur DIBUANG + dilaporkan per fold.
  JOIN FITUR LAMA: deviasi terdokumentasi — SEMUA kelas (pos & neg) join md =
                   md_last-at-anchor (positif T2-e memakai md label event; di
                   horizon md event = look-ahead 6h), tol 1,0 m.
  VARIAN         : G = 7 statistik MD w2h di anchor (canary, segar)
                   E = 480 fitur time-series T10 di anchor baru
                   F = E + 70 fitur lama (58 features_v2 + 12 last_*)
  PROTOKOL       : identik T2-d/T2-e — LOWO 7 fold, val 15% ekor temporal
                   (thr F1-maks), seed 42, RF/HGB/log params kampanye 40,
                   StandardScaler di latih, RF prediksi serial (fix P7),
                   TANPA tuning, output pertama = final.
  GATE           : identik T2-e — target = max(0,2465; canary+0,02), menang
                   >= 5/7 fold vs canary horizon-sama.
  DIAGNOSTIK     : D1 flag kosong @anchor per kelas; D2 missingness-only AUPRC
                   (terpisah, bukan gate); D3 tabel gugur ketersediaan per fold.
  STOP (exit 3)  : fold uji tanpa dua kelas; violations anti-leakage > 0;
                   unit kosong di dalam kampanye != 0; canary None; fold != 7.

Implementation notes:
  - code/46 & code/60 diimpor sebagai PUSTAKA (jalur kode fitur/protokol sama
    persis dengan T2-d/T2-e; tidak ada logika protokol yang disalin ulang).
  - Kontrol T2-e tidak disentuh; sha256 + mtime dicatat sbg bukti pemakaian ulang.

Output: docs/V2_ML_BEAT_CANARY_HORIZON.json + docs/V2_ML_BEAT_CANARY_HORIZON.md
        (ditulis skrip dari JSON, 0 angka manual) + RUN_LOG via tee.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
PARSED = BASE / "data" / "volve" / "witsml_parsed"
EVENTS_NPZ = BASE / "data" / "predictive" / "features_timeseries.npz"
# kontrol desain P4/T2-e — DIPAKAI ULANG, tidak dibangun ulang
CONTROLS_NPZ_B = BASE / "data" / "predictive" / "features_timeseries_controls_berdata.npz"
POS_SHARD_DIR = BASE / "data" / "predictive" / "horizon_pos_shards"
OUT_JSON = BASE / "docs" / "V2_ML_BEAT_CANARY_HORIZON.json"
OUT_MD = BASE / "docs" / "V2_ML_BEAT_CANARY_HORIZON.md"

PRA_KOMENTAR = "t_66037ed6 comment 33 (pra-registrasi, ditulis sebelum run pertama)"


def load_mod(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# pustaka: jalur kode protokol & fitur IDENTIK T2-d/T2-e
m46 = load_mod(BASE / "code" / "46_beat_canary_ts.py", "c46")
m60 = m46.load_t10()                       # code/60 (kanal/statistik/jendela)

log = m46.log
ap = m46.ap
nm = m46.nm

# ---- pra-registrasi (comment 33) — jangan diubah setelah hasil terlihat ----
ANCHOR_OFFSET_S = 6 * 3600          # anchor = act_start − 6 jam
HORIZON_LABEL_S = 7200              # definisi label negatif T2-e (dipakai ulang)
SEED = m46.SEED
TARGET_FLOOR = m46.TARGET_FLOOR     # 0,2465 — lantai T2, TIDAK boleh diubah
MARGIN = m46.MARGIN                 # 0,02
MIN_WINS = m46.MIN_WINS             # 5
RF_PARAMS = m46.RF_PARAMS
HGB_PARAMS = m46.HGB_PARAMS
MODELS = m46.MODELS
SETS = m46.SETS
KEYS = m46.KEYS
CANARY_KEY = m46.CANARY_KEY
FRAMING_33 = m46.FRAMING_33
SHORT = m46.SHORT

PRA_REGISTRASI = {
    "komentar_kartu": PRA_KOMENTAR,
    "keputusan": "anchor positif = act_start − 6 jam; kontrol desain T2-e dipakai "
                 "ulang byte-identik; syarat ketersediaan P4 simetris; join md "
                 "semua kelas = md_last-at-anchor; gate identik T2-e",
    "alasan": "zona [act_start−2h, act_start) = zona mati T2-e (191/661 positif "
              "jendela-2h kosong; missingness-only 0,398 > canary 0,1494); anchor "
              "−6h ada di zona data-mengalir sehingga missingness tak bisa jadi "
              "penanda kelas",
    "klarifikasi_horizon": "body kartu menulis [act_start−24h, act_start−6h]; "
                           "jendela T10 dibekukan (w30m/w2h/w6h) dan kartu melarang "
                           "fitur baru -> cakupan efektif [act_start−12h, "
                           "act_start−6h); dinyatakan di pra-registrasi sebelum hasil",
    "protokol": "LOWO 7 fold, val 15% ekor temporal, seed 42, RF/HGB params "
                "kampanye 40, RF predict serial, varian G/E/F, SATU kampanye "
                "tanpa tuning, output pertama = final",
    "gate": "canary = varian G (log) dihitung segar pada horizon ini; "
            "target = max(0,2465; canary+0,02); menang >= 5/7 fold",
    "negatif": "kontrol berdata T2-e dipakai ulang (aturan seleksi identik bentuk: "
               "anchor tenang + n_rows(w30m)>=1) — tanpa rebuild/resample",
    "diagnostik": "D1 flag kosong @anchor per kelas; D2 missingness-only (terpisah, "
                  "bukan gate); D3 gugur ketersediaan per fold",
    "aturan_klaim": "framing §3.3 verbatim; TIDAK ada klaim 'mengalahkan canary' "
                    "kecuali varian lolos gate; kalau GAGAL -> tulis GAGAL apa "
                    "adanya, jangan ganti desain lalu ulang",
}


# Riset pendahuluan (docs/PROTOCOL_RISET_TIM.md) — dievaluasi SEBELUM run final;
# tidak mengubah desain/gate, hanya dokumentasi kewajiban protocol.
RISET_PENDAHULUAN = {
    "protocol": "docs/PROTOCOL_RISET_TIM.md (operator 2026-10-06): riset dulu, "
                "baru eksekusi; sebutkan skill + poin dipakai di deliverable",
    "scikit-learn": "imputasi median + StandardScaler fit HANYA di latih, per fold "
                    "(anti leakage); random_state=42 semua model; metrik "
                    "ketidakseimbangan = AUPRC (gate); RF/HGB tanpa scaling, "
                    "logistik dengan scaling",
    "statistical-analysis": "tentukan rencana uji SEBELUM lihat data (pra-registrasi "
                            "= anti p-hacking); 1 kampanye tanpa shopping hasil; "
                            "pisahkan konfirmatif (gate) vs eksploratif (D1-D3); "
                            "hasil tak signifikan ≠ tidak ada efek -> catatan daya "
                            "wajib; laporkan efek (delta vs canary), bukan hanya "
                            "lulus/tidak",
    "experimental-design": "unit = event (anti pseudoreplication baris 4-detik); "
                           "LOWO = blocking pada sumur, val temporal = blok waktu; "
                           "canary = kontrol sejalan pada unit & fold sama; "
                           "syarat ketersediaan simetris = keseimbangan kondisi "
                           "antar kelas; desain + seed didokumentasikan pra-registrasi",
    "kesimpulan": "desain & gate T2-f konsisten dengan ketiga skill -> TIDAK ada "
                  "perubahan desain/gate; penambahan hanya dokumenter (baris riset "
                  "di MD + limitasi daya/multiplicitas di §8)",
}


def log2(m: str = "") -> None:
    print(m, flush=True)


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def iso_mtime(p: Path) -> str:
    return datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc).isoformat()


# =========================================================================
# PART A — fitur positif di anchor digeser (jalur kode identik T10)
# =========================================================================
def build_pos_features(mod, z) -> dict:
    """661 event -> fitur di a = act_start − 6h. Cache per fold (shard)."""
    verify = json.load(open(PARSED / "_verify.json"))
    ev_fold = np.array([str(f) for f in z["fold"]], dtype=object)
    ev_ts = np.array([pd.Timestamp(str(t)).value for t in z["act_start_utc"]],
                     dtype="int64")
    feat_names = [f"{w}__{ch}__{st}" for w, _ in mod.WINDOWS
                  for ch in mod.CHANNELS for st in mod.STATS]
    bnames = ["md_mean", "md_std", "md_min", "md_max", "md_slope_per_min", "md_last",
              "md_delta", "time_hour_sin", "time_hour_cos", "time_dow_sin", "time_dow_cos"]
    mnames = [f"{w}__{s}" for w, _ in mod.WINDOWS
              for s in ["n_rows", "gap_median_s", "gap_max_s", "full_window"]]
    POS_SHARD_DIR.mkdir(parents=True, exist_ok=True)

    Xs, XBs, XMs, anchors, folds, viol_tot, scan_tot = [], [], [], [], [], 0, 0
    for fold in sorted(set(ev_fold)):
        t0 = time.time()
        sel = np.flatnonzero(ev_fold == fold)
        cache = POS_SHARD_DIR / f"pos_{fold}.npz"
        if cache.exists():
            s = np.load(cache, allow_pickle=True)
            ok = (int(s["seed"]) == SEED
                  and int(s["anchor_offset_s"]) == ANCHOR_OFFSET_S
                  and int(s["n_feat"]) == len(feat_names)
                  and np.array_equal(s["event_idx"], sel)
                  and [str(x) for x in s["feature_names"]] == feat_names)
            if not ok:
                raise RuntimeError(f"{cache}: seed/offset/event_idx/features berbeda "
                                   "-> hapus shard manual")
            X, XB, XM = s["X"], s["XB"], s["XM"]
            anc = s["anchor_ts"]
            v, sc = int(s["violations"]), int(s["rows_scanned"])
            log2(f"  [{fold}] shard positif ada: {len(sel)} event (dipakai ulang)")
        else:
            resolution, usecols = m46.fold_resolution(mod, verify, fold)
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

            t_end_all = ev_ts[sel] - ANCHOR_OFFSET_S * 1_000_000_000
            X = np.full((len(sel), len(feat_names)), np.nan, dtype=np.float32)
            XB = np.full((len(sel), len(bnames)), np.nan, dtype=np.float32)
            XM = np.full((len(sel), len(mnames)), np.nan, dtype=np.float32)
            v = sc = 0
            for r, t_end in enumerate(t_end_all):
                vi, sci = m46.features_for_anchor(mod, ts_ns, cols, md_vals, int(t_end),
                                                  X[r], XB[r], XM[r])
                v += vi
                sc += sci
            anc = t_end_all.astype("int64")
            np.savez_compressed(cache, X=X, XB=XB, XM=XM, anchor_ts=anc,
                                event_idx=sel, feature_names=np.array(feat_names, dtype=object),
                                seed=np.array(SEED), anchor_offset_s=np.array(ANCHOR_OFFSET_S),
                                n_feat=np.array(len(feat_names)), violations=np.array(v),
                                rows_scanned=np.array(sc))
            del df, ts, cols
            log2(f"  [{fold}] fitur positif @−6h: {len(sel)} event "
                 f"(violations={v}, rows={nm(sc)}, {time.time()-t0:.0f}s)")
        viol_tot += v
        scan_tot += sc
        Xs.append(X)
        XBs.append(XB)
        XMs.append(XM)
        anchors.append(anc)
        folds.extend([fold] * len(sel))

    return {
        "X": np.vstack(Xs).astype(np.float64),
        "XB": np.vstack(XBs).astype(np.float64),
        "XM": np.vstack(XMs).astype(np.float64),
        "anchor_ts": np.concatenate(anchors),
        "fold": np.array(folds, dtype=object),
        "event_idx": np.concatenate([np.flatnonzero(ev_fold == f)
                                     for f in sorted(set(ev_fold))]),
        "feature_names": feat_names,
        "baseline_names": bnames,
        "window_meta_names": mnames,
        "anti_leakage": {"violations": int(viol_tot), "rows_scanned": int(scan_tot),
                         "scope": "661 event T2-f di anchor act_start−6h (part A "
                                  "code/64, jalur kode identik code/60)"},
    }


def load_controls() -> dict:
    """Kontrol desain T2-e — DIPAKAI ULANG byte-identik (pembuktian: sha256)."""
    if not CONTROLS_NPZ_B.exists():
        raise RuntimeError(f"kontrol T2-e tidak ada: {CONTROLS_NPZ_B}")
    c = np.load(CONTROLS_NPZ_B, allow_pickle=True)
    return {
        "X": c["X"].astype(np.float64),
        "XB": c["X_baseline"].astype(np.float64),
        "XM": c["X_window_meta"].astype(np.float64),
        "fold": np.array([str(f) for f in c["fold"]], dtype=object),
        "anchor_ts": c["anchor_ts"].astype("int64"),
        "y": c["y"].astype(np.int64),
        "sampling_meta": json.loads(str(c["sampling_meta"])),
        "anti_leakage": {"violations": int(c["anti_violations"]),
                         "rows_scanned": int(c["anti_rows_scanned"]),
                         "scope": f"kontrol T2-e dipakai ulang ({len(c['anchor_ts'])} "
                                  "anchor, counter dari npz T2-e)"},
        "provenance": {"path": str(CONTROLS_NPZ_B),
                       "sha256": sha256(CONTROLS_NPZ_B),
                       "mtime_utc": iso_mtime(CONTROLS_NPZ_B),
                       "size_bytes": CONTROLS_NPZ_B.stat().st_size,
                       "reused_not_rebuilt": True},
    }


# =========================================================================
# PART D — dokumen (ditulis dari JSON, 0 angka manual)
# =========================================================================
def write_md(res: dict) -> None:
    L = []
    A = L.append
    G = res["gate"]
    U = res["units"]
    D = res["diagnostics"]
    PR = res["pra_registrasi"]

    def cz(v, n=4):
        if v is None:
            return "NA"
        return f"{float(v):.{n}f}".replace(".", ",")

    A("# V2 — BEAT-THE-CANARY HORIZON 6 JAM: JALUR 2 MISSINGNESS-PROOF (T2-f)")
    A("")
    A("Task kanban: `t_66037ed6` [ML Engineer] — anchors digeser ke "
      "`act_start − 6 jam` (zona data-mengalir); verdict akhir = hak PM/ML "
      "Auditor, bukan skrip ini. Pra-registrasi = komentar kartu "
      f"{PR['komentar_kartu']}.")
    A("Status: semua angka berasal dari eksekusi `code/64_beat_canary_horizon.py`; "
      "log: `docs/V2_ML_BEAT_CANARY_HORIZON_RUN_LOG.txt`; JSON: "
      "`docs/V2_ML_BEAT_CANARY_HORIZON.json`; verifier independen: "
      "`code/65_verify_horizon.py`.")
    A("")
    A("Riset pendahuluan (PROTOCOL_RISET_TIM): **scikit-learn** — imputasi/skaler fit "
      "di latih per fold, random_state=42, metrik imbalance = AUPRC · "
      "**statistical-analysis** — pra-registrasi sebelum hasil dilihat (anti "
      "p-hacking), 1 kampanye tanpa shopping hasil, konfirmatif vs eksploratif "
      "dipisah, wajib catatan daya · **experimental-design** — unit=event "
      "(anti-pseudoreplication), LOWO=blocking sumur, canary=kontrol sejalan pada "
      "unit/fold sama, desain+seed dipra-registrasi. Kesimpulan: desain & gate "
      "konsisten → tanpa perubahan (detail di JSON `riset_pendahuluan`).")
    A("")
    A("Framing mengikat (PM audit §3.3, dipakai apa adanya — keputusan PM, tidak diubah):")
    A("> " + FRAMING_33)
    A("")
    A("---")
    A("")
    A("## 0. Pra-registrasi (sebelum hasil) + klarifikasi horizon")
    A("")
    A(f"- Komentar pra-registrasi: `{PR['komentar_kartu']}` — timestamp komentar "
      "< generated_at JSON ini (dicek verifier).")
    A(f"- Keputusan: **{PR['keputusan']}**")
    A(f"- Alasan (bukan hasil): {PR['alasan']}")
    A(f"- Klarifikasi horizon: {PR['klarifikasi_horizon']}")
    A(f"- Aturan klaim: {PR['aturan_klaim']}")
    A("")
    A("---")
    A("")
    A("## 1. Kriteria T2-f (dari kartu) + verdict jujur")
    A("")
    A(f"- Syarat: macro-LOWO AUPRC varian ≥ target **{cz(G['target_macro'])}** "
      f"(rumus: {G['target_formula']}; canary horizon-sama = {cz(G['canary_macro'])}; "
      f"lantai {cz(G['floor'])}) **DAN** unggul ≥ **{G['min_wins']}/7** fold vs "
      "canary varian G (log_MD) pada horizon & unit yang sama (canary dihitung segar).")
    A(f"- **VERDICT T2-f: {G['verdict_t2f']}**")
    A("")
    A("| Varian | Model | macro-LOWO | menang vs canary | ≥target | ≥5/7 | LULUS |")
    A("|---|---|---|---|---|---|---|")
    for s in ("E", "F"):
        for m in MODELS:
            k = f"{m}_{s}"
            v = G["per_variant"][k]
            A(f"| {s} | {m} | {cz(v['macro'])} | {v['wins_vs_canary']} | "
              f"{'ya' if v['pass_target'] else 'tidak'} | "
              f"{'ya' if v['pass_wins'] else 'tidak'} | "
              f"{'✅' if v['LOLOS'] else '❌'} |")
    A("")
    A("## 2. Desain horizon (pra-registrasi comment 33)")
    A("")
    A(f"- **Anchor positif**: `a = act_start − {ANCHOR_OFFSET_S//3600} jam`; fitur "
      "dihitung ulang di anchor baru dengan jalur kode identik T10 "
      "(`features_for_anchor` code/46 → code/60). Semua sampel `timestamp < a` "
      "(anti-leakage).")
    A(f"- **Cakupan fitur efektif**: [act_start−12h, act_start−6h) karena jendela "
      "T10 dibekukan (w30m/w2h/w6h) — lihat klarifikasi §0.")
    A(f"- **Negatif**: kontrol desain T2-e **dipakai ulang byte-identik** "
      f"(sha256 `{res['controls_provenance']['sha256'][:16]}…`, mtime "
      f"{res['controls_provenance']['mtime_utc']} — sebelum pra-registrasi); "
      "aturan seleksinya identik bentuk dengan aturan positif (anchor tenang + "
      "`n_rows(w30m)≥1`), tanpa rebuild/resample.")
    A(f"- **Syarat ketersediaan simetris (P4)**: `{res['design']['syarat_ketersediaan']}` "
      "— identik utk positif (di anchor geser) & negatif, latih + evaluasi; "
      f"positif gugur = **{D['gugur']['positif_dibuang']}** (dilaporkan per fold, §7 D3).")
    A(f"- **Join fitur lama (deviasi terdokumentasi)**: {res['design']['join_md_deviasi']}")
    A(f"- Varian: G = 7 statistik MD w2h di anchor (canary segar) · E = 480 fitur "
      f"TS di anchor baru · F = E + 70 fitur lama (join tol "
      f"{res['design']['md_tol_m']} m).")
    A(f"- Unit: **{U['n_pos']}** positif lolos ketersediaan (dari {U['n_pos_semua_event']} "
      f"event) + **{U['n_neg']}** negatif kontrol dipakai ulang = {U['n_total']} unit "
      f"(prevalensi {cz(U['prevalence'])}).")
    A("")
    A("| Fold | n_pos @−6h | n_neg (dipakai ulang) | prev fold | flag kosong-2h pos (dari semua event) |")
    A("|---|---|---|---|---|")
    for f in sorted(D["gugur"]["per_fold"]):
        gp = D["gugur"]["per_fold"][f]
        A(f"| {SHORT.get(f, f)} | {gp['n_lolos']} | {gp['n_neg']} | "
          f"{cz(gp['prevalence_fold'])} | {gp['n_kosong_2h_semua_event']} |")
    A("")
    A("## 3. Protokol (identik T2-d/T2-e)")
    A("")
    A("- LOWO 7 fold; uji = 1 sumur penuh; latih = 6 sumur lain; val = 15% ekor "
      "temporal latih (threshold F1-maks dari skor val); seed 42; StandardScaler "
      "logistik fit di latih; RF/HGB params persis kampanye 40; RF prediksi serial "
      "(fix P7). Satu kampanye, tanpa tuning, output pertama = final.")
    for dev in res["protocol"]["deviasi_terdokumentasi"]:
        A(f"- Deviasi terdokumentasi: {dev}")
    A(f"- Anti-leakage: positif @−6h rows_scanned = "
      f"{nm(res['anti_leakage_pos']['rows_scanned'])} "
      f"(violations {res['anti_leakage_pos']['violations']}); kontrol T2-e rows_scanned = "
      f"{nm(res['anti_leakage']['rows_scanned'])} "
      f"(violations {res['anti_leakage']['violations']}).")
    A("")
    A("## 4. Hasil per fold (PR-AUC)")
    A("")
    A("| Fold | n | prev | " + " | ".join(KEYS) + " |")
    A("|---|" + "---|" * (len(KEYS) + 2))
    for w in res["folds"][CANARY_KEY]:
        ref = res["folds"][CANARY_KEY][w]
        cells = []
        for k in KEYS:
            d = res["folds"][k][w]
            cells.append(cz(d.get("pr_auc")) if d.get("pr_auc") is not None else "NA")
        A(f"| {SHORT.get(w, w)} | {ref['n']} | {cz(ref['prev'])} | " + " | ".join(cells) + " |")
    A("")
    A("## 5. Pooled + kalibrasi + recall@P≥0,20")
    A("")
    A("| Model | pooled PR-AUC | macro | prev | lift | R@P≥0,20 | R@P≥0,50 | Brier | ECE 10 bin | F1 @thr-val |")
    A("|---|---|---|---|---|---|---|---|---|---|")
    for k in KEYS:
        d = res["pooled"][k]
        A(f"| {k} | {cz(d['pr_auc'])} | {cz(d['macro_pr_auc'])} | {cz(d['prev'])} | "
          f"{cz(d['lift'], 3)} | {cz(d['r_at_p20'])} | {cz(d['r_at_p50'])} | "
          f"{cz(d['brier'])} | {cz(d['ece'])} | {cz(d['f1'])} |")
    A("")
    A("## 6. Diagnostik channel/jendela (train-side, bukan seleksi fitur)")
    A("")
    for key in ("rf_E", "rf_F"):
        g = res["importances"].get(key, {})
        A(f"**{key}** — top jendela: " + ", ".join(f"{k}={v}" for k, v in
                                                    list(g.get("per_window", {}).items())[:3]))
        A("")
        A("top kelompok: " + " · ".join(f"{k}={v}" for k, v in
                                        list(g.get("per_group", {}).items())[:14]))
        A("")
    A("## 7. Diagnostik kejujuran (D1–D3, BUKAN bagian gate)")
    A("")
    A(f"- **D1 flag kosong @anchor** — positif (semua {D['flag_kosong']['pos']['n_unit']} "
      f"event, pra-filter): kosong-30m {D['flag_kosong']['pos']['empty_30m']}, "
      f"kosong-2h {D['flag_kosong']['pos']['empty_2h']}, "
      f"kosong-6h {D['flag_kosong']['pos']['empty_6h']}.")
    A(f"  - negatif kontrol ({D['flag_kosong']['neg']['n_unit']} anchor): "
      f"kosong-30m {D['flag_kosong']['neg']['empty_30m']}, "
      f"kosong-2h {D['flag_kosong']['neg']['empty_2h']}, "
      f"kosong-6h {D['flag_kosong']['neg']['empty_6h']}.")
    A(f"- **D1b unit kampanye dgn jendela kosong = "
      f"{D['n_unit_kampanye_kosong']}** (verifikasi keras; >0 → run berhenti).")
    A(f"- **D2 missingness-only** (skor = flag kosong-2h @anchor, TANPA sensor; "
      f"dilaporkan TERPISAH): macro AUPRC = {cz(D['missingness_only']['macro'])}, "
      f"pooled = {cz(D['missingness_only']['pooled'])}; flag pos "
      f"{D['missingness_only']['n_flag_pos']} / neg "
      f"{D['missingness_only']['n_flag_neg']}.")
    A(f"- **Limitasi D2 (wajib baca)**: {D['missingness_only']['catatan']}")
    A(f"- **D3 gugur ketersediaan @−6h**: {D['gugur']['positif_dibuang']} positif "
      f"gugur dari {U['n_pos_semua_event']} (per fold di §2); gugur TIDAK ikut "
      "latih/evaluasi — bukan S1 (tidak ada sensitivitas keluar pra-registrasi).")
    A(f"- Join fitur lama: matched **{res['join_old']['matched']}/"
      f"{res['join_old']['n_units']}** unit ({res['join_old']['match_rate']}); "
      f"match-rate pos {D['join_match_rate_pos']} vs neg {D['join_match_rate_neg']}.")
    A("")
    A("## 8. Limitasi (wajib baca sebelum kutip angka)")
    A("")
    nps = [d.get("n_pos") for d in res["folds"][CANARY_KEY].values()
           if d.get("n_pos") is not None]
    A(f"- **Daya & unit inferensi**: makro = rata-rata PR-AUC 7 fold (7 sumur, "
      f"n_pos/fold {min(nps)}–{max(nps)}) → ketidakpastian per-fold lebar; gate "
      "adalah syarat pra-registrasi (lantai + margin + menang ≥5/7), **bukan** uji "
      "signifikansi formal — 'LOLOS/GAGAL' = keputusan desain, bukan klaim "
      "probabilitas. GAGAL ≠ membuktikan tidak ada sinyal (statistical-analysis: "
      "hasil tak signifikan ≠ tidak ada efek; desain ini mungkin kurang daya).")
    A(f"- **Multiplicitas**: 6 varian (E/F × log/rf/hgb) diuji dalam satu kampanye → "
      "klaim sah HANYA untuk varian yang lolos KEDUA syarat gate; tidak ada klaim "
      "per-varian lain, dan tidak ada uji susulan yang dipilih setelah hasil.")
    A("- **Konfirmatif vs eksploratif**: gate §1 = konfirmatif; D1–D3 §7 = "
      "diagnostik/eksploratif, dilabeli begitu dan tidak boleh dipakai utk klaim "
      "lolos/tidaknya gate.")
    A("- **Ledger eksekusi (bug display-only, tanpa perubahan angka/desain)**: "
      "run 1 menulis JSON primer LALU crash `KeyError 'prevalence'` saat render MD "
      "(setelah semua perhitungan selesai) → key diperbaiki jadi `prevalence_fold` "
      "saja + mode `--md-only` ditambah; MD run 1 dirender ulang utk verifikasi "
      "awal; run 2 (kode final; desain, gate, dan seluruh konstanta identik) "
      "dijalankan penuh dan JSON run 2 dibandingkan identik dengan run 1 "
      "(determinisme, cek V13 di verifier) sebelum artefak final disahkan. "
      "Tidak ada angka yang disentuh; fix murni penamaan key dict.")
    A("- Klaim 'prediksi dini berbasis sensor' TIDAK boleh dinaikkan selama framing "
      "§3.3 belum terpenuhi — keputusan PM, tidak diubah oleh kampanye ini.")
    A("- Cakupan fitur efektif [act_start−12h, act_start−6h) (klarifikasi §0) — "
      "angka ini sebanding HANYA untuk posisi relatif terhadap canary horizon-sama, "
      "bukan angka AUPRC dunia baris-md.")
    A("- Negatif = kontrol desain T2-e (jaminan tenang 2 jam ke depan, aturan T2-e) "
      "→ anchor negatif bisa berjarak 2–6 jam dari event lain; ini label-noise yang "
      "konservatif (menekan skor semua varian secara merata, termasuk canary).")
    A("- n_neg per fold mengikuti desain T2-e (dipakai ulang); bila n_pos @−6h "
      "berbeda dari T2-e, prevalensi fold sedikit bergeser dari odds-persis — "
      "angka aktual per fold di §2.")
    A("- Pemetaan F-15/F-15S ke wellbore = asumsi terkuat, belum tervalidasi (T7).")
    A("- VAR_F-5_alt tidak dipakai (keputusan T2-d): konsistensi 7 fold T10 dipertahankan.")
    A("- Tidak ada sensitivitas S1/S2 desain lama di kampanye ini (di luar pra-"
      "registrasi comment 33); diagnostik D1–D3 menggantikan peran kejujuran.")
    A("")
    A("## 9. Reproduksi + artefak")
    A("")
    A("```bash")
    A('cd "/mnt/d/Capstone 1"')
    A("python3 code/64_beat_canary_horizon.py 2>&1 | tee "
      "docs/V2_ML_BEAT_CANARY_HORIZON_RUN_LOG.txt")
    A("python3 code/65_verify_horizon.py   # verifier independen")
    A("```")
    A("")
    A(f"Runtime terukur: {res['runtime_seconds']} s (deterministik: random_state=42, "
      "seed 42, RF prediksi serial; shard positif cache per fold).")
    A("")
    A("Artefak:")
    A("")
    for a in res["artifacts"]:
        A(f"- `{a}`")
    A("")
    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")


# =========================================================================
# main
# =========================================================================
def main() -> int:
    t_start = time.time()
    mod = m60
    log(f"T2-f horizon 6h | pra-registrasi: {PRA_KOMENTAR}")
    log(f"windows T10 beku: {mod.WINDOWS}")

    # ---------- A. positif: fitur segar di anchor digeser ----------
    z = np.load(EVENTS_NPZ, allow_pickle=True)
    pos = build_pos_features(mod, z)
    ev_fold_all = np.array([str(f) for f in z["fold"]], dtype=object)
    ev_wb_all = np.array([str(w) for w in z["wellbore"]], dtype=object)
    ev_id_all = z["event_id"].astype(np.int64)
    # build per fold -> urutan gabungan; SELARAS-kan ke urutan global event dulu
    n_ev = len(ev_fold_all)
    covered = np.zeros(n_ev, dtype=bool)
    covered[pos["event_idx"]] = True
    if not covered.all():
        log(f"event tanpa fitur horizon: {int((~covered).sum())} — STOP")
        return 3
    XG = np.full((n_ev, pos["X"].shape[1]), np.nan, dtype=np.float64)
    XBG = np.full((n_ev, pos["XB"].shape[1]), np.nan, dtype=np.float64)
    XMG = np.full((n_ev, pos["XM"].shape[1]), np.nan, dtype=np.float64)
    XG[pos["event_idx"]] = pos["X"]
    XBG[pos["event_idx"]] = pos["XB"]
    XMG[pos["event_idx"]] = pos["XM"]
    ancG = np.zeros(n_ev, dtype="int64")
    ancG[pos["event_idx"]] = pos["anchor_ts"]

    avail = XMG[:, 0] > 0                 # syarat P4 @anchor geser (simetris)
    sel = np.flatnonzero(avail)
    exc = np.flatnonzero(~avail)
    log(f"positif @−6h: {len(sel)}/{len(avail)} lolos syarat ketersediaan "
        f"(gugur {len(exc)})")

    X_pos, XB_pos, XM_pos = XG[sel], XBG[sel], XMG[sel]
    anc_pos = ancG[sel]
    ev_fold, ev_wb = ev_fold_all[sel], ev_wb_all[sel]
    ev_id = ev_id_all[sel]
    y_pos = np.ones(len(sel), dtype=np.int64)

    # ---------- B. negatif: kontrol T2-e dipakai ulang ----------
    controls = load_controls()
    log(f"negatif: {len(controls['fold'])} kontrol T2-e DIPAKAI ULANG "
        f"(sha256 {controls['provenance']['sha256'][:16]}…, mtime "
        f"{controls['provenance']['mtime_utc']})")
    log(f"sampling meta T2-e: {json.dumps(controls['sampling_meta'])}")
    if int(controls["anti_leakage"]["violations"]) > 0:
        log("LEAKAGE pada kontrol > 0 — STOP")
        return 3
    if int(pos["anti_leakage"]["violations"]) > 0:
        log(f"LEAKAGE pada positif @−6h > 0 ({pos['anti_leakage']['violations']}) — STOP")
        return 3

    # ---------- C. susun matriks (urut temporal, identik T2-e) ----------
    y = np.concatenate([y_pos, controls["y"]])
    wells = np.concatenate([ev_wb,
                            np.array([mod.FOLD2LABEL[f] for f in controls["fold"]],
                                     dtype=object)])
    folds_all = np.concatenate([ev_fold, controls["fold"]])
    ts_all = np.concatenate([anc_pos, controls["anchor_ts"]])
    order = np.argsort(ts_all, kind="stable")
    y, wells, folds_all, ts_all = y[order], wells[order], folds_all[order], ts_all[order]
    X_ts = np.vstack([X_pos, controls["X"]])[order]
    XB = np.vstack([XB_pos, controls["XB"]])[order]
    X_wm = np.vstack([XM_pos, controls["XM"]])[order]

    # join fitur lama — md = md_last-at-anchor untuk SEMUA kelas (deviasi terdokumentasi)
    md_all = np.concatenate([XB_pos[:, 5], controls["XB"][:, 5]])[order]
    old_all, old_names, meta_full = m46.join_old_features(wells, md_all)
    join_meta = dict(meta_full)
    mmask = join_meta.pop("matched_mask")
    log(f"join fitur lama: {join_meta['matched']}/{join_meta['n_units']} "
        f"({join_meta['match_rate']}), kolom={len(old_names)}")

    sets = {
        "G": XB[:, 0:7],
        "E": X_ts,
        "F": np.hstack([X_ts, old_all]),
    }
    log(f"unit total: {len(y)} (pos {int(y.sum())}, prev {y.mean():.4f})")

    if sorted(set(folds_all)) != sorted(mod.FOLD2LABEL):
        log(f"fold tidak persis 7: {sorted(set(folds_all))} — STOP")
        return 3

    # verifikasi keras: TIDAK ADA unit kampanye dgn jendela kosong (P4 simetris)
    e30 = X_wm[:, 0] == 0
    e2h = X_wm[:, 4] == 0
    e6h = X_wm[:, 8] == 0
    if e30.any() or e2h.any() or e6h.any():
        log(f"SYARAT KETERSEDIAAN dilanggar di kampanye: 30m={int(e30.sum())} "
            f"2h={int(e2h.sum())} 6h={int(e6h.sum())} — STOP")
        return 3

    # ---------- D. kampanye (protokol identik 40/42/44/46) ----------
    try:
        folds_res, pooled, imp_acc, split_info, score_full, pred_full, _ = \
            m46.run_arm(sets, y, ts_all, wells, KEYS, "main", extra=None)
    except RuntimeError as e:
        log(f"STOP (inconclusive): {e}")
        return 3
    macro = m46.macro_table(folds_res)
    gate = m46.gate_eval(folds_res, macro)
    gate["verdict_t2f"] = gate.pop("verdict_t2d")
    if gate["canary_macro"] is None:
        log("canary None — STOP")
        return 3
    log(f"GATE: canary={gate['canary_macro']} target={gate['target_macro']} "
        f"verdict={gate['verdict_t2f']}")

    # ---------- E. diagnostik importance (train-side) ----------
    v2meta = json.load(open(BASE / "data" / "predictive" / "features_v2_meta.json"))
    v2_group_map = {}
    for gname, cols in v2meta.get("groups", {}).items():
        for c in cols:
            v2_group_map[c] = gname
    imps = {}
    for key, names in (("rf_E", list(z["feature_names"])),
                       ("rf_F", list(z["feature_names"]) + old_names)):
        arr = np.vstack(imp_acc[key])
        pw, pg = m46.importance_groups(arr.mean(axis=0), names, v2_group_map)
        imps[key] = {"per_window": pw, "per_group": pg}

    # ---------- F. diagnostik D1–D3 ----------
    def flagcnt(XM):
        return {"n_unit": int(len(XM)),
                "empty_30m": int((XM[:, 0] == 0).sum()),
                "empty_2h": int((XM[:, 4] == 0).sum()),
                "empty_6h": int((XM[:, 8] == 0).sum())}

    pos_flags = flagcnt(XMG)                   # semua 661 event @−6h (urutan global)
    neg_flags = flagcnt(controls["XM"])         # kontrol T2-e
    n_kam_kosong = int(e30.sum() + e2h.sum() + e6h.sum())

    # D2 missingness-only: skor = flag kosong-2h @anchor pada unit kampanye
    mscore = e2h.astype(np.float64)
    d2_folds = {}
    for w in sorted(set(wells)):
        m = wells == w
        d2_folds[w] = {"n": int(m.sum()), "n_pos": int(y[m].sum()),
                       "pr_auc": ap(y[m], mscore[m])}
    d2_macro = round(float(np.nanmean([d2_folds[w]["pr_auc"] for w in d2_folds
                                       if d2_folds[w]["pr_auc"] is not None])), 4)
    d2 = {"macro": d2_macro, "pooled": ap(y, mscore),
          "n_flag_pos": int(((y == 1) & e2h).sum()),
          "n_flag_neg": int(((y == 0) & e2h).sum()),
          "folds": d2_folds,
          "catatan": "flag kosong-2h @anchor seragam 0 di seluruh unit kampanye "
                     "(syarat ketersediaan simetris; dijaga guard STOP) -> skor "
                     "konstan, AUPRC = prevalensi, TIDAK informatif. Angka ini "
                     "justru bukti missingness tak bisa jadi penanda kelas pada "
                     "desain horizon; dilaporkan terpisah dari skor sensor dan "
                     "tidak dipakai utk klaim mengalahkan canary."}

    # per-fold gugur/prevalensi — dihitung langsung dari array kampanye (urutan global)
    gugur_per_fold = {}
    pos_mask_ord = np.concatenate([np.ones(len(sel), dtype=bool),
                                   np.zeros(len(controls['fold']), dtype=bool)])[order]
    for f in sorted(set(folds_all)):
        m = folds_all == f
        n_pos_f = int((m & pos_mask_ord).sum())
        n_neg_f = int((m & ~pos_mask_ord).sum())
        m_all = ev_fold_all == f
        n_kosong_2h = int((XMG[m_all][:, 4] == 0).sum())
        gugur_per_fold[f] = {
            "n_semua_event": int(m_all.sum()),
            "n_lolos": n_pos_f,
            "n_gugur": int(m_all.sum()) - n_pos_f,
            "n_neg": n_neg_f,
            "prevalence_fold": round(n_pos_f / max(n_pos_f + n_neg_f, 1), 4),
            "n_kosong_2h_semua_event": n_kosong_2h,
        }

    diagnostics = {
        "flag_kosong": {"pos": pos_flags, "neg": neg_flags,
                        "definisi": "n_rows(w30m/w2h/w6h) == 0 pada anchor kelas "
                                    "masing-masing (positif @−6h, kontrol @anchor)"},
        "n_unit_kampanye_kosong": n_kam_kosong,
        "missingness_only": d2,
        "gugur": {"positif_dibuang": int(len(exc)),
                  "positif_lolos": int(len(sel)),
                  "per_fold": gugur_per_fold,
                  "syarat": "n_rows(w30m @ anchor) >= 1 (simetris P4)"},
        "join_match_rate_pos": round(float(mmask[pos_mask_ord].mean()), 4),
        "join_match_rate_neg": round(float(mmask[~pos_mask_ord].mean()), 4),
    }

    res = {
        "task": "t_66037ed6 [ML Engineer] T2-f JALUR 2 — horizon 6 jam "
                "(missingness-proof), pra-registrasi comment 33",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "pra_registrasi": PRA_REGISTRASI,
        "riset_pendahuluan": RISET_PENDAHULUAN,
        "design": {
            "anchor_positif": "act_start − 6 jam (fitur dihitung ulang, jalur kode "
                              "identik T10; semua sampel timestamp < anchor)",
            "cakupan_fitur_efektif": "[act_start−12h, act_start−6h) — jendela T10 "
                                     "dibekukan (w30m/w2h/w6h); klarifikasi "
                                     "pra-registrasi vs teks kartu −24h",
            "syarat_ketersediaan": "n_rows(w30m @ anchor) >= 1 (simetris P4: pos "
                                   "@anchor geser, negatif @anchor-nya; latih+evaluasi)",
            "negatif": "kontrol berdata desain T2-e dipakai ulang byte-identik "
                       "(tanpa rebuild/resample)",
            "join_md_deviasi": "SEMUA kelas join md = md_last-at-anchor (T2-e positif "
                               "pakai md label event; di horizon md event = look-ahead "
                               "6h); md_last negatif identik dgn T2-e",
            "md_tol_m": m46.MD_TOL,
            "horizon_label_negatif": "aturan T2-e dipakai ulang: anchor tenang = tanpa "
                                     "event start dalam 2 jam ke depan + lolos syarat",
            "variants": {"G": "7 statistik MD w2h di anchor (canary, segar)",
                         "E": f"{int(X_ts.shape[1])} fitur time-series T10 di anchor baru",
                         "F": f"E + {len(old_names)} fitur lama (join md tol "
                              f"{m46.MD_TOL} m)"},
            "seed": SEED,
            "anti_leakage": "semua sampel fitur: timestamp < anchor (jalur kode identik "
                            "T10)",
        },
        "protocol": {
            "lowo_folds": sorted(mod.FOLD2LABEL),
            "val": "15% ekor temporal latih; threshold F1-maks dari skor val",
            "seed": SEED, "models": MODELS,
            "rf_params": {**RF_PARAMS, "predict_n_jobs": 1},
            "hgb_params": HGB_PARAMS,
            "scaler": "StandardScaler fit di latih (logistik)",
            "identik_kampanye": ["40_beat_canary.py", "42_sensor_increment.py",
                                 "44_beat_canary_v2.py", "46_beat_canary_ts.py"],
            "deviasi_terdokumentasi": [
                "anchor positif digeser ke act_start−6h (itulah desain jalur 2); "
                "fitur dihitung ulang, bukan dipotong dari X T10",
                "negatif = kontrol T2-e dipakai ulang (aturan seleksi identik bentuk) "
                "— tanpa rebuild/resample",
                "join md semua kelas = md_last-at-anchor (deviasi dari T2-e yg "
                "memakai md label event utk positif)",
                "sisa NaN (kanal tanpa data dalam jendela + join fitur lama) "
                "diimputasi median LATIH seragam semua varian",
                "canary G dihitung segar pada horizon & unit ini (canary lama tidak "
                "sebanding)",
            ],
        },
        "controls_provenance": controls["provenance"],
        "anti_leakage": controls["anti_leakage"],
        "anti_leakage_pos": pos["anti_leakage"],
        "sampling": controls["sampling_meta"],
        "units": {"n_pos": int(len(sel)), "n_neg": int(len(controls['fold'])),
                  "n_total": int(len(y)), "prevalence": round(float(y.mean()), 4),
                  "n_pos_semua_event": int(len(avail)),
                  "n_pos_gugur_ketersediaan": int(len(exc))},
        "join_old": {**join_meta,
                     "unit_extra": "tidak ada (positif gugur tidak dihitung ulang; "
                                   "bukan desain S1)"},
        "folds": folds_res, "pooled": pooled, "macro": macro,
        "split_info": split_info,
        "gate": gate, "importances": imps, "diagnostics": diagnostics,
        "pooled_scores": {"y": y.astype(int).tolist(),
                          "wells": wells.astype(str).tolist(),
                          "empty_2h": e2h.astype(bool).tolist(),
                          "keys": {k: {"score": [float(v) for v in score_full[k]],
                                       "pred": pred_full[k].astype(int).tolist()}
                                   for k in KEYS}},
        "artifacts": [
            "code/64_beat_canary_horizon.py (kampanye, rerunnable, exit 0)",
            "code/65_verify_horizon.py (verifier independen)",
            "docs/V2_ML_BEAT_CANARY_HORIZON.md (dokumen ini — ditulis skrip dari JSON)",
            "docs/V2_ML_BEAT_CANARY_HORIZON.json (semua angka primer)",
            "docs/V2_ML_BEAT_CANARY_HORIZON_RUN_LOG.txt (log eksekusi)",
            "data/predictive/horizon_pos_shards/ (fitur positif @−6h, cache per fold)",
            "data/predictive/features_timeseries_controls_berdata.npz (kontrol T2-e, "
            "dipakai ulang — sha256 di provenance)",
        ],
        "runtime_seconds": round(time.time() - t_start, 1),
    }
    json.dump(res, open(OUT_JSON, "w"), indent=1, ensure_ascii=False, default=str)
    write_md(res)
    log(f"JSON ditulis: {OUT_JSON}")
    log(f"MD ditulis: {OUT_MD}")
    log(f"VERIFIED T2-f: folds={len(mod.FOLD2LABEL)}, units={len(y)} "
        f"(pos {int(y.sum())}), gugur_pos={len(exc)}, canary={gate['canary_macro']}, "
        f"target={gate['target_macro']}, lolos={gate['ada_yang_lolos']} | "
        f"violations pos={pos['anti_leakage']['violations']} "
        f"neg={controls['anti_leakage']['violations']} | "
        f"unit_kosong_dlm_kampanye={n_kam_kosong} | D2 macro={d2['macro']} | "
        f"runtime={res['runtime_seconds']}s")
    print("DONE", flush=True)
    return 0


if __name__ == "__main__":
    if "--md-only" in sys.argv:
        # Render MD dari JSON primer yang SUDAH ada (dipakai setelah crash run-1 di
        # write_md; tidak menghitung ulang apa pun — lihat ledger §8).
        try:
            res = json.load(open(OUT_JSON))
            write_md(res)
            print(f"md-only OK -> {OUT_MD}", flush=True)
            sys.exit(0)
        except Exception:
            import traceback
            traceback.print_exc()
            sys.exit(1)
    try:
        sys.exit(main())
    except Exception:
        import traceback
        traceback.print_exc()
        sys.exit(1)
