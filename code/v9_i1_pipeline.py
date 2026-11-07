#!/usr/bin/env python3
"""V9-I1 — PIPELINE ALAT PdM ADVISORY (prototipe integrasi 7 engine).

Task: t_34e9b879 [Integration Engineer] · Board: capstone-v9-build · 2026-10-12 (WIB)
Sumbu: docs/V9_PM1_ARCHITECTURE.md §1 (pipeline 5 lapis) + §2 (spesifikasi 7 engine);
       tier pemakaian = docs/V9_EVAL_{A,B,C} — I1 TIDAK boleh menaikkan tier sendiri.

Isi modul:
  1. REGISTRY — tier + lapisan + badge FAR + label keyakinan + batas pemakaian per
     engine/klaim/head, dengan jejak sumber dokumen (audit A1 bisa cek).
  2. 7 ENGINE — vib, ssi, shk, stuck (K-i+K-ii), hyd (K-i + K-ii-tidak-tersedia),
     bit_wear, tool_wear. Head dijalankan persis resep kampanye:
       · rule-display   = aturan kanal pada menit t0-1 (strict-past; E_RULE §2 —
                          membaca bin t0-1 = data masa lalu, anti-bocor S5)
       · persistence    = kolom y_prev_* (resep D1, jendela [t0-10, t0))
       · hybrid D-A3    = rule AND persistence
       · stuck E1       = 2-dari-3 z(TQA)/z(HKLD)/ROP-drop, z vs median+MAD 60 mnt
       · stuck E0b      = persistence-event (menit t-1 = menit onset)
       · ML             = RF kontrak (leaf 5, balanced_subsample, seed 42) dilatih
                          LOWO (latih well lain, uji segmen) → skor RANKING sahaja
       · tool_wear K-i  = kalibrasi within-tool (median+MAD 30% awal R01, alarm
                          bila >=5/27 fitur |z|>3) — resep identik E_STAT 03
  3. DECISION LAYER — L0 status otomatis / L1 peringatan human-in-loop / L2 tren /
     L3 keputusan manusia; ALARM OTOMATIS KRITIS = 0 slot.

Assertion keras (diverifikasi di kode, bukan hanya ditulis):
  * setiap head membawa tier REGISTRY; REGISTRY tidak memuat "ALARM-OTOMATIS";
  * head tier TREN TIDAK boleh jatuh ke L1 (engine tren tidak memunculkan alarm);
  * semua output L1 wajib human_review_required = True;
  * klaim BELUM tersedia ditulis eksplisit (hyd K-ii, bit_wear K-2, tool_wear K-ii RF).

Riset pendahuluan: scientific-critical-thinking — OBSERVED (angka replay segmen +
kutipan EVAL) dipisahkan dari DESAIN (registry/lapisan) dan BELUM-TERUKUR (klaim non-aktif).
Riset pendahuluan: verification-mandatory — badge membawa sumber dokumen; verifikasi
independen terpisah di code/v9_i1_verify.py (recompute dari dataset mentah).
Riset pendahuluan: statistical-analysis — FAR segmen memakai konvensi kampanye
FP/(n_neg/60)*24 (per 24 jam, skala jendela 60 dtk); AUPRC = average_precision;
metrik TIDAK dirata-ratakan antar kelas; fold UNDERPOWERED tidak dihitung mayoritas.
Riset pendahuluan: what-if-oracle — cabang Δ ("promosikan engine jadi alarm") ditolak
lewat assertion tier; robust action lintas cabang = registry tier-terkunci + badge FAR.
Riset pendahuluan: consciousness-council — 5 arketipe (Architect, Empiricist,
Minimalist, Pragmatist, Contrarian); ketegangan "cepat terlihat berguna" vs "jujur soal
bukti" diresolusi dengan memisahkan L1 (peringatan berpengawas) dari L2 (tren).
Riset pendahuluan: sequentialthinking — 4 pikiran: inventaris data → rancang 5 lapis →
audit risiko kejujuran (rule≡label, kenaikan tier, ML non-terpakai) → rencana uji integrasi.
"""
from __future__ import annotations

import importlib.util
import os

import numpy as np
import pandas as pd

BASE = "/mnt/d/Capstone 1(v2)"
DS = f"{BASE}/scratch/v9_d1/datasets"
BINS = f"{BASE}/scratch/v9_d1/bins"
USROP = f"{BASE}/data/USROP_labeled.csv"
TOOLWEAR = f"{BASE}/scratch/v6_e1/toolwear_windows.csv"
OUTDIR = f"{BASE}/scratch/v9_i1"

SEED = 42
META_COLS = ("well", "ts_bin", "feat_ts_max", "lab_ts", "lab_kind")
LABEL_PREFIXES = ("y_", "valid_", "obs_", "anom_")

T_TREN = "TREN"
T_SUPERV = "PERINGATAN-BERPENGAWAS"
T_NONE = "BELUM LAYAK PAKAI"
TIER_FORBIDDEN = "ALARM-OTOMATIS"  # dilarang di registry (EVAL_C §3: 0 engine)

# ---------------------------------------------------------------------------
# 1. REGISTRY — tier/lapisan/badge/batas (sumber = dokumen V9_EVAL_A/B/C + E_*)
# ---------------------------------------------------------------------------
REGISTRY = {
    "vib": {
        "klaim_tugas": "deteksi kondisi getaran lateral (status VIBLAT_RT >= 32,17405 ft/s2)",
        "jenis_tugas": "deteksi kondisi (bukan prediksi onset — TLead tidak berlaku)",
        "sumber_tier": "docs/V9_EVAL_C_LAYERC.md §1 baris vib + §2.1",
        "heads": {
            "rule_display": {
                "tier": T_SUPERV, "layer": "L1",
                "badge_far": "FAR 10,0-49,9/24jam di 4 well (E_RULE §2.1); P 0,87-0,95",
                "keyakinan": "presisi rule stabil antar-well (1,1x); recall 0,28-0,60",
                "batas": "jangan klaim lead-time menit; ambang wajib kalibrasi per-well (D-A4) sebelum dipakai sbg alarm",
            },
            "persistence": {
                "tier": T_TREN, "layer": "L0",
                "badge_far": "persistence = baseline konfirmasi-status (AUPRC V8 0,517-0,796)",
                "keyakinan": "ΔB RF vs persistence hanya 2/4 fold — persistence setara ML di 2 fold",
                "batas": "konfirmasi-status saja; bukan prediksi kegagalan mendatang",
            },
            "hybrid_rule_and_persistence": {
                "tier": T_SUPERV, "layer": "L1",
                "badge_far": "hibrida ≡ rule utk kelas ini (E_RULE §2.1: FP = rule)",
                "keyakinan": "rule t0-1 ⊆ persistence utk kelas definisi-kanal",
                "batas": "sama dengan rule; keuntungan = konfirmasi dua langkah",
            },
            "rf_lowo": {
                "tier": T_TREN, "layer": "L2",
                "badge_far": "FAR τ0,5 menyebar 4,1-496 (119x) — TIDAK PORTABEL (EVAL_C C3)",
                "keyakinan": "CI95 memuat prevalensi 0/4; ΔB vs canary 4/4",
                "batas": "ranking/tren sahaja; JANGAN sbg ambang alarm global",
            },
        },
    },
    "ssi": {
        "klaim_tugas": "deteksi kondisi stick-slip torsional (SSI(CRPM_RT) >= 1)",
        "jenis_tugas": "deteksi kondisi",
        "sumber_tier": "docs/V9_EVAL_C_LAYERC.md §1 baris ssi + §2.2",
        "heads": {
            "rule_display": {
                "tier": T_SUPERV, "layer": "L1",
                "badge_far": "FP rule total 26 lintas fold (E_RULE §2.2)",
                "keyakinan": "rule single-bin ≈ random antar-menit (jarang persisten)",
                "batas": "nodata CRPM 62,3% baris — deteksi bergantung ketersediaan sensor",
            },
            "persistence": {
                "tier": T_TREN, "layer": "L0",
                "badge_far": "persistence kalah 0/5 vs RF (angka V8)",
                "keyakinan": "baseline lemah — jangan dibaca sbg detektor mandiri",
                "batas": "konfirmasi-status saja",
            },
            "hybrid_rule_and_persistence": {
                "tier": T_SUPERV, "layer": "L1",
                "badge_far": "FP 26 -> 7 (-73,1%) konsisten 7/7 well; FAR hybrid 0-3,7 (EVAL_C §2.2)",
                "keyakinan": "pemangkasan FP konsisten lintas 7 well",
                "batas": "hemat-pemeriksaan, bukan alarm; 2 fold UNDERPOWERED dilabeli",
            },
            "rf_lowo": {
                "tier": T_TREN, "layer": "L2",
                "badge_far": "τ0,3 FAR 0-15,6; well FAR<=6 hanya 2/7 (EVAL_C C3)",
                "keyakinan": "CI memuat prev 3/7 layak (5/9 all); AUPRC antar-well spread 30x",
                "batas": "ranking sahaja; nodata 62,3% = keterbatasan sensor, bukan murni model",
            },
        },
    },
    "shk": {
        "klaim_tugas": "deteksi anomali/dysfunction bit bounce (SHKRSK_RT >= 1)",
        "jenis_tugas": "deteksi anomali sedang berlangsung",
        "sumber_tier": "docs/V9_EVAL_C_LAYERC.md §1 baris shk + §2.3",
        "heads": {
            "rule_display": {
                "tier": T_SUPERV, "layer": "L1",
                "badge_far": "FAR 0,67-6,6/24jam; <=6 di 7/9 well (EVAL_C §2.3)",
                "keyakinan": "satu-satunya kelas rig dgn mayoritas fold lolos FAR<=6 tanpa kalibrasi",
                "batas": "badge FAR wajib tampil; B3 EVAL_B negatif → periksa dulu, jangan auto",
            },
            "persistence": {
                "tier": T_TREN, "layer": "L0",
                "badge_far": "persistence ≥ prevalence-random 7/9 (E_RULE §2.3)",
                "keyakinan": "recall display-rule 0-0,38",
                "batas": "konfirmasi-status saja",
            },
            "hybrid_rule_and_persistence": {
                "tier": T_SUPERV, "layer": "L1",
                "badge_far": "hibrida ≡ rule (E_RULE §2.3)",
                "keyakinan": "rule ⊆ persistence utk kelas definisi-kanal",
                "batas": "sama dengan rule",
            },
            "rf_lowo": {
                "tier": T_TREN, "layer": "L2",
                "badge_far": "τ0,3 FAR 0-96,5; well <=6 hanya 1/9 (EVAL_C C3)",
                "keyakinan": "CI95 memuat prevalensi 7/9 well = sinyal lokal-wellbore",
                "batas": "screening berbiaya-cek-tinggi (tau 0,05-0,10); JANGAN sbg alarm",
            },
        },
    },
    "stuck": {
        "klaim_tugas": "K-i: deteksi kondisi blok STUCK_RT; K-ii: prediksi onset 0→1 (H=10 mnt)",
        "jenis_tugas": "deteksi kondisi (K-i) + prediksi kejadian mendatang (K-ii)",
        "sumber_tier": "docs/V9_EVAL_C_LAYERC.md §1 baris stuck K-i/K-ii + §2.4",
        "heads": {
            "rule_display": {
                "klaim": "K-i", "tier": T_SUPERV, "layer": "L1",
                "badge_far": "rule P 0,92-0,97; FAR 8,3-61,0 (hanya 2 well: F-14, F-9_A)",
                "keyakinan": "cakupan 2/9 well → portabilitas BELUM TERUKUR",
                "batas": "hanya layak di well yang diuji; replikasi F-9/F-10/F-15 diperlukan",
            },
            "persistence": {
                "klaim": "K-i", "tier": T_TREN, "layer": "L0",
                "badge_far": "persistence 0,787 (F-9_A, kutipan V6)",
                "keyakinan": "konfirmasi-status, bukan prediksi onset",
                "batas": "K-i saja; tidak memberi peringatan dini",
            },
            "hybrid_rule_and_persistence": {
                "klaim": "K-i", "tier": T_SUPERV, "layer": "L1",
                "badge_far": "hibrida stuck_k1 = E_RULE §2.4 (2 fold)",
                "keyakinan": "rule-display ≥ persistence di 2/2 fold",
                "batas": "cakupan 2 well",
            },
            "e1_2of3": {
                "klaim": "K-ii", "tier": T_TREN, "layer": "L2",
                "badge_far": "E1 FAR 2,1-29,0 (13,9x); B1 0-0,066; FP 422 (EVAL_C §2.4)",
                "keyakinan": "rule mekanis mentah ≈ prevalence pada onset (E_RULE §4)",
                "batas": "TRIAGE/riset ranking — belum layak peringatan (B1 di bawah 0,5)",
            },
            "persistence_event": {
                "klaim": "K-ii", "tier": T_TREN, "layer": "L2",
                "badge_far": "FAR 0-2,9; FP alarm total 11 (EVAL_C §2.4)",
                "keyakinan": "TLead median 7,0 mnt (anchor 2,67-7,37); B1 0-0,115",
                "batas": "peringatan-dini berbeban-wajar utk tinjauan manusia; bukan alarm",
            },
            "rf_lowo": {
                "klaim": "K-ii", "tier": T_TREN, "layer": "L2",
                "badge_far": "RF τ0,5 B1 0-0,045; signifikan CI hanya 1/4 (EVAL_C §2.4)",
                "keyakinan": "canary depth ≥ RF (G2 gagal) — ranking lemah",
                "batas": "ranking sahaja",
            },
        },
    },
    "hyd": {
        "klaim_tugas": "K-i: deteksi kondisi residu SPPA |z|>2; K-ii: prediksi kick/loss proxy",
        "jenis_tugas": "deteksi kondisi (K-i) + prediksi kejadian mendatang (K-ii)",
        "sumber_tier": "docs/V9_EVAL_C_LAYERC.md §1 baris hyd K-i/K-ii + §2.5",
        "heads": {
            "rule_display": {
                "klaim": "K-i", "tier": T_SUPERV, "layer": "L1",
                "badge_far": "rule t0-1 FP total 2.091 lintas fold (E_RULE §2.5)",
                "keyakinan": "label = residu SPPA (PROXY — anotasi wajib)",
                "batas": "FAR skala jendela 38-132 = beban blok, bukan alarm",
            },
            "persistence": {
                "klaim": "K-i", "tier": T_SUPERV, "layer": "L0",
                "badge_far": "persistence P 0,615-0,793; FAR_t 32,2-109,7/24jam",
                "keyakinan": "CI95 memuat prevalensi 0/9 (satu-satunya kelas rig bersih)",
                "batas": "RF DILARANG di kelas ini (D-A5: ΔB negatif 7/7)",
            },
            "hybrid_rule_and_persistence": {
                "klaim": "K-i", "tier": T_SUPERV, "layer": "L1",
                "head_utama": True,
                "lead_menit": 8.0,
                "lead_sumber": "docs/RND_S6_PM_WAVE2.md §4.1 (H1p rule DAN persistence, 9 fold, 2 seed)",
                "badge_far": ("S6 lintas fold+seed (docs/RND_S6_PM_WAVE2.md §4.1): FP 927, presisi 0,8243, "
                              "recall 0,6519, FAR 4,10/24jam, lead 8,0 mnt; 7/9 fold lolos FAR<6 dan recall>=0,5"),
                "keyakinan": "menang atas H1 rule-dan-statistik (7/9 lawan 5/9 fold) pada penyebut 9 fold dan 390 onset",
                "batas": ("lapisan B belum terukur (0 kolom biaya, 0 jadwal inspeksi); cakupan di atas 50% hanya F-10 "
                          "(0,673); bukan alarm otomatis"),
            },
            "k2_tidak_tersedia": {
                "klaim": "K-ii", "tier": T_NONE, "layer": "L3",
                "badge_far": "q95: P=R=0 (0 TP, FP 177); fisher CI memuat prev (EVAL_C §2.5)",
                "keyakinan": "sign-flip 78,7% jendela; FlowOut absen = kendala sensor terukur",
                "batas": "TIDAK DIJALANKAN di prototipe (data pit/GAINLOSSTOT belum diparse) — bukan kegagalan metode; RF V8 = referensi",
            },
        },
    },
    "bit_wear": {
        "klaim_tugas": "K-1: deteksi status blok high_MSE; K-2: prediksi onset (pra-reg belum terbit)",
        "jenis_tugas": "deteksi kondisi (K-1); K-2 onset = BELUM DIJALANKAN",
        "sumber_tier": "docs/V9_EVAL_C_LAYERC.md §1 baris bit_wear + §2.6",
        "heads": {
            "persistence": {
                "klaim": "K-1", "tier": T_TREN, "layer": "L2",
                "badge_far": "P/R/FAR = BELUM TERUKUR (field tidak ada di JSON EVAL_A §2.6)",
                "keyakinan": "persistence AUPRC 0,119-0,984; ΔB vs canary 5/5 scorable",
                "batas": "ranking/tren saja; hibrida degradasi ke persistence (label Teale = kanal terlarang); dataset USROP ≠ rig Volve",
            },
            "k2_onset_belum": {
                "klaim": "K-2", "tier": T_NONE, "layer": "L3",
                "badge_far": "nol angka (kampanye belum jalan)",
                "keyakinan": "pra-reg K-2 belum terbit",
                "batas": "K-2 BELUM boleh dipakai di tingkat apa pun sebelum kampanye berangka",
            },
        },
    },
    "tool_wear": {
        "klaim_tugas": "K-i: deteksi perubahan-regime dalam-run (bengkel); K-ii: ranking lintas-alat",
        "jenis_tugas": "deteksi perubahan-regime (K-i); K-ii = ranking",
        "sumber_tier": "docs/V9_EVAL_C_LAYERC.md §1 baris tool_wear + §2.7",
        "domain": "BENGKEL — lead detik; TIDAK dijumlahkan dengan lead rig menit (D-A7)",
        "heads": {
            "calib_5of27": {
                "klaim": "K-i", "tier": T_TREN, "layer": "L2",
                "badge_far": "engine 5/27 (E_STAT §B): FP_R01 27-41 jendela (71-98% jendela evaluasi) — terlalu sensitif utk peringatan; deteksi R02 4/4 alat, TLead 20-36 dtk",
                "keyakinan": "deteksi konsisten 4/4 alat (tes artefak termal 0/8); namun FP tinggi pada alat BARU (R01)",
                "batas": "dipakai sbg GATING inspeksi + skor perubahan-regime sahaja; JANGAN jadi peringatan (FP besar); titik operasi layak = op_far_calibrated",
            },
            "op_far_calibrated": {
                "klaim": "K-i", "tier": T_SUPERV, "layer": "L1",
                "badge_far": "FAR-terkalibrasi target <=1 alarm/menit: FP_R01 1-3/alat; deteksi R02 4/4; TLead 20-36 dtk (E_STAT §C, EVAL_C §2.7)",
                "keyakinan": "TLead median 20-36 dtk (dispersi 1,8x — terkecil antar engine); kalibrasi dalam-run = sifat desain",
                "batas": "detektor PERUBAHAN-REGIME; precision run 0,50 → JANGAN dibaca sbg 'keausan spesifik'; domain bengkel, transfer ke rig TIDAK diklaim (D-A7)",
            },
            "canary_3rms": {
                "klaim": "K-ii", "tier": T_TREN, "layer": "L2",
                "badge_far": "canary 3-RMS AUPRC 0,516-0,612 (1,19x); identity-majority = prev (plafon lift 2,0)",
                "keyakinan": "RF K-ii V9 TIDAK dijalankan → angka V8 = referensi",
                "batas": "ranking lintas-alat saja; precision biner V8 0,50-0,56 ≈ peluang → jangan sbg alarm",
            },
        },
    },
}

LAYERS = {
    "L0": "status otomatis (rule/persistence = sistem hari-ini, tanpa notifikasi)",
    "L1": "peringatan human-in-loop (wajib konfirmasi operator; badge FAR tampil)",
    "L2": "tren/skor (dasbor, tanpa notifikasi)",
    "L3": "keputusan manusia (klaim yang belum layak peringatan / belum tersedia)",
}
AUTO_CRITICAL_SLOTS = 0  # desain EVAL_C §3: 0/7 engine layak alarm otomatis

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def feature_cols(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns
            if c not in META_COLS and not c.startswith(LABEL_PREFIXES)]


def seg_metrics(y, pred, win_s: int = 60) -> dict:
    """Metrik segmen; FAR pada SKALA JENDELA ASLI.
    win_s=60 (rig): FP per 24 jam operasi negatif = FP/(n_neg/60)*24 (konvensi
    kampanye V8/V9). win_s=1 (bengkel): FP per menit operasi negatif."""
    y = np.asarray(y).astype(int)
    pred = np.asarray(pred).astype(int)
    tp = int(((pred == 1) & (y == 1)).sum())
    fp = int(((pred == 1) & (y == 0)).sum())
    fn = int(((pred == 0) & (y == 1)).sum())
    n_neg = int((y == 0).sum())
    n_pos = int((y == 1).sum())
    p = tp / (tp + fp) if (tp + fp) else None
    r = tp / (tp + fn) if (tp + fn) else None
    neg_min = n_neg * win_s / 60.0
    neg_h = n_neg * win_s / 3600.0
    if win_s == 60:
        # konvensi kampanye: FAR_24h = FP / (n_neg/60) * 24  → FP per 24 jam
        far = (fp / neg_h * 24.0) if neg_h else None
        unit = "FP/24jam-negatif (jendela 60 dtk)"
    else:
        far = (fp / neg_min) if neg_min else None
        unit = f"FP/menit-negatif (jendela {win_s} dtk)"
    return dict(n=int(len(y)), pos=n_pos, neg=n_neg, tp=tp, fp=fp, fn=fn,
                precision=None if p is None else round(p, 4),
                recall=None if r is None else round(r, 4),
                far_segmen=None if far is None else round(far, 3),
                far_unit=unit)


def auprc(y, score) -> float | None:
    y = np.asarray(y).astype(int)
    if len(np.unique(y)) < 2:
        return None
    from sklearn.metrics import average_precision_score
    return round(float(average_precision_score(y, score)), 4)


def registry_head(engine: str, name: str) -> dict:
    return REGISTRY[engine]["heads"][name]


def make_head(engine: str, name: str, active=None, n_windows: int = 0,
              extra: dict | None = None, y=None, win_s: int = 60) -> dict:
    """Bangun entri head lengkap + asersi tier/lapisan yang sah."""
    reg = registry_head(engine, name)
    assert reg["tier"] != TIER_FORBIDDEN, f"tier terlarang utk {engine}/{name}"
    assert reg["layer"] in LAYERS, f"layer tak dikenal: {reg['layer']}"
    if reg["tier"] in (T_TREN, T_NONE):
        assert reg["layer"] != "L1", (
            f"PELANGGARAN: head {engine}/{name} bertier {reg['tier']} tidak boleh L1 "
            "(engine tren/tidak-layak tidak boleh memunculkan peringatan)")
    if reg["layer"] == "L1":
        assert reg["tier"] == T_SUPERV, "L1 hanya untuk tier PERINGATAN-BERPENGAWAS"
    out = {
        "head": name,
        "klaim": reg.get("klaim"),
        "tier": reg["tier"],
        "layer": reg["layer"],
        "badge_far": reg["badge_far"],
        "keyakinan": reg["keyakinan"],
        "batas_pemakaian": reg["batas"],
        "human_review_required": reg["layer"] in ("L1", "L3"),
        "n_windows": int(n_windows),
    }
    for k in ("lead_menit", "lead_sumber", "head_utama", "definisi"):
        if k in reg:
            out[k] = reg[k]
    if active is not None:
        active = np.asarray(active).astype(bool)
        out["n_aktif"] = int(active.sum())
        out["frac_aktif"] = round(float(active.mean()), 4)
        idx = np.where(active)[0]
        out["contoh_idx_aktif"] = [int(i) for i in idx[:5]]
        if y is not None:
            assert len(y) == len(active) == n_windows, (
                f"ketidakselarasan panjang pada {engine}/{name}: "
                f"y={len(y)} active={len(active)} n={n_windows}")
            out["metrik_segmen"] = seg_metrics(y, active.astype(int), win_s=win_s)
    if extra:
        out.update(extra)
    return out


def _load_module(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def rule_modules():
    """Impor ulang engine kampanye E_RULE (resep identik — integrasi, bukan salinan)."""
    r01 = _load_module(f"{BASE}/code/v9_e_RULE_01_status.py", "v9_e_rule01")
    r02 = _load_module(f"{BASE}/code/v9_e_RULE_02_stuck_onset.py", "v9_e_rule02")
    return r01, r02


def train_lowo(df: pd.DataFrame, ycol: str, test_well: str,
               n_estimators: int = 300) -> dict:
    """RF kontrak (seed 42, leaf 5, balanced_subsample, imputer median fold-safe).

    Split LOWO: latih SEMUA well selain `test_well`, uji di `test_well` (segmen).
    Tidak ada grid search, tidak ada ambang dioptimasi pasca-hasil (pra-reg S3).
    `df` HARUS berisi SEMUA well (data latih tidak mungkin dari satu well saja);
    baris uji diurutkan ts_bin agar selaras dengan segmen replay.
    """
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.impute import SimpleImputer

    feats = feature_cols(df)
    tr = df[df["well"] != test_well]
    te = df[df["well"] == test_well].sort_values("ts_bin")
    assert len(tr) > 0, f"set latih kosong (df tidak berisi well selain {test_well})"
    assert len(te) > 0, f"set uji kosong (well {test_well} tidak ada di df)"
    imp = SimpleImputer(strategy="median")
    Xtr = imp.fit_transform(tr[feats])
    Xte = imp.transform(te[feats])
    ytr = tr[ycol].to_numpy().astype(int)
    yte = te[ycol].to_numpy().astype(int)
    clf = RandomForestClassifier(
        n_estimators=n_estimators, min_samples_leaf=5,
        class_weight="balanced_subsample", random_state=SEED, n_jobs=-1)
    clf.fit(Xtr, ytr)
    score = clf.predict_proba(Xte)[:, 1]
    return dict(score=score, y=yte, n_train=len(tr), n_test=len(te),
                n_features=len(feats), n_estimators=n_estimators,
                train_wells=sorted(tr["well"].unique().tolist()),
                test_well=test_well)


# ---------------------------------------------------------------------------
# 2. ENGENE — 7 engine prototipe
# ---------------------------------------------------------------------------


def _status_heads(engine: str, cls_key: str, df: pd.DataFrame, ycol: str,
                  prevcol: str, r01) -> list[dict]:
    """rule-display (t0-1) + persistence + hybrid D-A3 untuk kelas status.

    `engine`  = kunci REGISTRY (vib/ssi/shk/stuck/hyd);
    `cls_key` = kelas di skrip E_RULE ("stuck_k1", "hyd_ki", ...).
    """
    y = df[ycol].to_numpy().astype(int)
    n = len(df)
    rp, nodata = r01.rule_display(cls_key, df)
    pers = df[prevcol].to_numpy().astype(int)
    valid = df[prevcol.replace("y_prev", "valid_prev")].to_numpy().astype(int) \
        if prevcol.replace("y_prev", "valid_prev") in df.columns else np.ones(n, int)
    hyb = ((rp == 1) & (pers == 1)).astype(int)
    heads = [
        make_head(engine, "rule_display", rp, n, y=y,
                  extra={"n_nodata": int(nodata.sum()),
                         "definisi": "aturan kanal pada menit t0-1 (strict-past)"}),
        make_head(engine, "persistence", pers, n, y=y,
                  extra={"n_valid_prev": int(valid.sum()),
                         "definisi": "y_prev (jendela [t0-10,t0))"}),
        make_head(engine, "hybrid_rule_and_persistence", hyb, n, y=y,
                  extra={"definisi": "rule(t0-1) AND persistence(t) [D-A3]"}),
    ]
    return heads


def run_vib(df: pd.DataFrame, df_full: pd.DataFrame, r01, ml: bool) -> dict:
    heads = _status_heads("vib", "vib", df, "y_vib", "y_prev_vib", r01)
    if ml:
        res = train_lowo(df_full, "y_vib", str(df["well"].iloc[0]), n_estimators=300)
        heads.append(make_head(
            "vib", "rf_lowo", (res["score"] >= 0.5).astype(int), len(df),
            y=res["y"], extra={
                "auprc_segmen": auprc(res["y"], res["score"]),
                "skor_ringkas": {"min": round(float(res["score"].min()), 4),
                                 "median": round(float(np.median(res["score"])), 4),
                                 "max": round(float(res["score"].max()), 4)},
                "latih_well": res["train_wells"], "n_fitur": res["n_features"],
                "catatan": "skor = RANKING tren (L2); ambang 0,5 hanya utk cetak metrik segmen, BUKAN alarm",
                "ambang_operasi": "TIDAK ditetapkan di prototipe (pra-reg S3) — pakai AUPRC/rank, bukan angka biner ambang 0,5"}))
    else:
        heads.append(make_head("vib", "rf_lowo", None, len(df),
                               extra={"status": "TIDAK DIJALANKAN (flag --ml mati)"}))
    return _engine_block("vib", heads)


def run_ssi(df: pd.DataFrame, df_full: pd.DataFrame, r01, ml: bool) -> dict:
    heads = _status_heads("ssi", "ssi", df, "y_ssi", "y_prev_ssi", r01)
    if ml:
        res = train_lowo(df_full, "y_ssi", str(df["well"].iloc[0]), n_estimators=300)
        heads.append(make_head(
            "ssi", "rf_lowo", (res["score"] >= 0.5).astype(int), len(df),
            y=res["y"], extra={
                "auprc_segmen": auprc(res["y"], res["score"]),
                "latih_well": res["train_wells"], "n_fitur": res["n_features"],
                "catatan": "ranking tren (L2); nodata CRPM 62,3% lintas fold",
                "ambang_operasi": "TIDAK ditetapkan di prototipe (pra-reg S3) — metrik biner ambang 0,5 = ilustrasi; pakai AUPRC/rank"}))
    else:
        heads.append(make_head("ssi", "rf_lowo", None, len(df),
                               extra={"status": "TIDAK DIJALANKAN (flag --ml mati)"}))
    return _engine_block("ssi", heads)


def run_shk(df: pd.DataFrame, df_full: pd.DataFrame, r01, ml: bool) -> dict:
    heads = _status_heads("shk", "shk", df, "y_shk", "y_prev_shk", r01)
    if ml:
        res = train_lowo(df_full, "y_shk", str(df["well"].iloc[0]), n_estimators=300)
        heads.append(make_head(
            "shk", "rf_lowo", (res["score"] >= 0.5).astype(int), len(df),
            y=res["y"], extra={
                "auprc_segmen": auprc(res["y"], res["score"]),
                "latih_well": res["train_wells"], "n_fitur": res["n_features"],
                "catatan": "screening tren (L2); badge FAR kampanye wajib tampil; B3 negatif",
                "ambang_operasi": "TIDAK ditetapkan di prototipe (pra-reg S3) — metrik biner ambang 0,5 = ilustrasi; pakai AUPRC/rank"}))
    else:
        heads.append(make_head("shk", "rf_lowo", None, len(df),
                               extra={"status": "TIDAK DIJALANKAN (flag --ml mati)"}))
    return _engine_block("shk", heads)


def run_stuck(df_k1: pd.DataFrame, df_k2: pd.DataFrame,
              df_k2_full: pd.DataFrame, r01, r02, ml: bool) -> dict:
    # --- K-i (status) ---
    heads = _status_heads("stuck", "stuck_k1", df_k1, "y_stuck", "y_prev_stuck", r01)
    # --- K-ii (onset) ---
    y2 = df_k2["y_stuck_onset"].to_numpy().astype(int)
    e1, e1_nd = r01.rule_e1(df_k2)
    pev = r02.event_persistence(df_k2).astype(int)
    phor = df_k2["y_prev_stuck_onset"].to_numpy().astype(int)
    heads += [
        make_head("stuck", "e1_2of3", e1, len(df_k2), y=y2,
                  extra={"n_nodata": int(e1_nd.sum()),
                         "definisi": "2-dari-3 z(TQA)>2, z(HKLD)>2, ROP-drop>=30% (MEDIAN+MAD 60 mnt strict-past)",
                         "klaim": "K-ii"}),
        make_head("stuck", "persistence_event", pev, len(df_k2), y=y2,
                  extra={"definisi": "ŷ(t)=1[bila menit t-1 = menit peristiwa onset] (E0b)",
                         "persistence_horizon_ref": {
                             "n_aktif": int(phor.sum()),
                             "auprc_segmen": auprc(y2, phor),
                             "catatan": "E0a = HINDSIGHT (label horizon) — batas-atas teori, bukan pemakaian"}},
                  ),
    ]
    if ml:
        res = train_lowo(df_k2_full, "y_stuck_onset", str(df_k2["well"].iloc[0]),
                         n_estimators=200)
        heads.append(make_head(
            "stuck", "rf_lowo", (res["score"] >= 0.5).astype(int), len(df_k2),
            y=res["y"], extra={
                "auprc_segmen": auprc(res["y"], res["score"]),
                "latih_well": res["train_wells"], "n_fitur": res["n_features"],
                "n_estimators": 200,
                "catatan": "skor ranking triage (L2); ambang q95 pra-reg tidak dioptimasi di sini",
                "ambang_operasi": "TIDAK ditetapkan di prototipe (pra-reg S3) — metrik biner ambang 0,5 = ilustrasi; pakai AUPRC/rank"}))
    else:
        heads.append(make_head("stuck", "rf_lowo", None, len(df_k2),
                               extra={"status": "TIDAK DIJALANKAN (flag --ml mati)"}))
    blk = _engine_block("stuck", heads)
    blk["catatan_klaim"] = ("K-i dan K-ii = klaim TERPISAH; metrik segmen dicetak "
                            "terpisah (n windows berbeda: K-i %d, K-ii %d)"
                            % (len(df_k1), len(df_k2)))
    return blk


def run_hyd(df: pd.DataFrame, r01) -> dict:
    heads = _status_heads("hyd", "hyd_ki", df, "y_hyd", "y_prev_hyd", r01)
    heads.append(make_head(
        "hyd", "k2_tidak_tersedia", None, 0,
        extra={"status": "BELUM TERSEDIA DI PROTOTIPE",
               "alasan": "data 12 kolom pit / GAINLOSSTOT F-1C/F-11 belum diparse; FlowOut absen",
               "tindakan": "status eksplisit — BUKAN skor 0; jangan dibaca sbg 'engine gagal'"}))
    blk = _engine_block("hyd", heads)
    blk["catatan_klaim"] = ("RF pada hyd-K-i DILARANG (D-A5, ΔB negatif 7/7) — "
                            "tidak ada head RF di engine ini, by design")
    return blk


def run_bit_wear(df: pd.DataFrame) -> dict:
    # grid = urutan Kedalaman (USROP), label K-1 = blok high_MSE (Teale)
    df = df.sort_values("Measured Depth m").reset_index(drop=True)
    is_mse = (df["label"] == "high_MSE_bit_wear").to_numpy().astype(int)
    pers = np.concatenate([[0], is_mse[:-1]])  # persistence y(t-1) pada grid depth
    heads = [
        make_head("bit_wear", "persistence", pers, len(df), y=is_mse,
                  extra={"definisi": "ŷ(t)=y(t-1) pada grid Kedalaman (USROP)",
                         "label_pos": int(is_mse.sum()),
                         "label_komposisi": df["label"].value_counts().to_dict()}),
        make_head("bit_wear", "k2_onset_belum", None, 0,
                  extra={"status": "BELUM DIJALANKAN",
                         "alasan": "pra-reg K-2 belum terbit (kampanye onset belum berangka)",
                         "tindakan": "jangan pakai K-2 di tingkat apa pun"}),
    ]
    return _engine_block("bit_wear", heads)


def run_tool_wear(tw: pd.DataFrame) -> dict:
    """K-i dua titik operasi (resep identik v9_e_STAT_03, CAL_FRAC=0.30,
    Z_THR=3.0, N_FEAT_ALARM=5):
      · calib_5of27        = engine §B (ambang tetap 5/27) — gating/skor,
                             FP tinggi pada alat baru → L2, bukan peringatan;
      · op_far_calibrated  = titik operasi §C (kuantile skor R01, target
                             <=1 alarm/menit) — inilah bukti EVAL_C §2.7 → L1.
    Jendela 1 detik → FAR dilaporkan per MENIT (bukan per 24 jam)."""
    feats = [c for c in tw.columns
             if c.endswith(("_mean", "_std", "_rms", "_kurt", "_skew", "_p2p",
                            "_crest", "_zcr", "_fdom"))]
    assert len(feats) == 27, f"fitur getaran = {len(feats)}, diharapkan 27"
    n = len(tw)
    y = tw["y"].to_numpy().astype(int)
    alarm_b = np.zeros(n, dtype=int)
    alarm_op = np.zeros(n, dtype=int)
    rms_rank = np.zeros(n, dtype=float)
    per_tool = []
    TARGET_FP_PER_MIN = 1.0
    for tool, g in tw.groupby("tool"):
        r01 = g[g["run"] == "R01"].sort_values("start_sample")
        r02 = g[g["run"] == "R02"].sort_values("start_sample")
        ncal = max(5, int(np.ceil(0.30 * len(r01))))
        cal, ev1 = r01.iloc[:ncal], r01.iloc[ncal:]
        med = cal[feats].median()
        mad = (cal[feats] - med).abs().median() * 1.4826
        mad = mad.replace(0, np.nan)

        def sc(ev):
            Z = ((ev[feats] - med) / mad).abs()
            return (Z > 3.0).sum(axis=1).to_numpy()

        s1, s2 = sc(ev1), sc(r02)
        a1, a2 = s1 >= 5, s2 >= 5
        alarm_b[ev1.index.to_numpy()] = a1.astype(int)
        alarm_b[r02.index.to_numpy()] = a2.astype(int)
        # titik operasi FAR-terkalibrasi (resep E_STAT §C, target 1,0 alarm/menit)
        q = 1.0 - TARGET_FP_PER_MIN * (len(ev1) / 60.0) / max(len(ev1), 1)
        q = min(max(q, 0.5), 1.0)
        thr = float(np.quantile(s1, q)) if len(s1) else None
        o1 = (s1 >= thr) if thr is not None else np.zeros(0, bool)
        o2 = (s2 >= thr) if thr is not None else np.zeros(0, bool)
        alarm_op[ev1.index.to_numpy()] = o1.astype(int)
        alarm_op[r02.index.to_numpy()] = o2.astype(int)
        # K-ii: ranking 3-RMS (canary) terhadap kalibrasi alat itu
        rms3 = [c for c in feats if c.endswith("_rms")]
        zrms = ((g[rms3] - med[rms3]) / mad[rms3]).abs().mean(axis=1)
        rms_rank[g.index.to_numpy()] = zrms.to_numpy()
        # statistik engine §B
        first_b = int(np.argmax(a2)) if a2.any() else None
        # statistik titik operasi §C
        first_c = int(np.argmax(o2)) if o2.any() else None
        per_tool.append({
            "alat": tool,
            "n_R01": int(len(r01)), "n_kalibrasi": int(ncal),
            "n_eval_R01": int(len(ev1)), "n_R02": int(len(r02)),
            "engine_5of27": {
                "fp_R01": int(a1.sum()),
                "pct_R01_alarmed": round(100 * float(a1.mean()), 1) if len(a1) else None,
                "det_R02": bool(a2.any()),
                "first_alarm_s": first_b,
                "TLead_s": (float(len(r02) - first_b) if first_b is not None else None),
            },
            "op_far_calibrated": {
                "target_fp_per_min": TARGET_FP_PER_MIN, "thr_featcount": thr,
                "fp_R01": int(o1.sum()),
                "det_R02": bool(o2.any()),
                "first_alarm_s": first_c,
                "TLead_s": (float(len(r02) - first_c) if first_c is not None else None),
                "pct_R02_alarmed": round(100 * float(o2.mean()), 1) if len(o2) else None,
            },
        })
    heads = [
        make_head("tool_wear", "calib_5of27", alarm_b, n, y=y, win_s=1,
                  extra={"definisi": "median+MAD 30% awal R01; alarm bila >=5/27 fitur |z|>3 "
                                     "(jendela evaluasi = R01 setelah kalibrasi + R02)",
                         "per_alat": per_tool,
                         "n_alat": int(tw["tool"].nunique()),
                         "n_jendela_kalibrasi_tidak_dinilai": int(sum(
                             t["n_kalibrasi"] for t in per_tool))}),
        make_head("tool_wear", "op_far_calibrated", alarm_op, n, y=y, win_s=1,
                  extra={"definisi": "kuantile skor R01 (target 1,0 alarm/menit) per alat "
                                     "— titik operasi FAR-terkalibrasi E_STAT §C",
                         "per_alat": [t["op_far_calibrated"] | {"alat": t["alat"]}
                                      for t in per_tool]}),
        make_head("tool_wear", "canary_3rms", (rms_rank >= 3.0).astype(int), n,
                  extra={"definisi": "skor ranking |z| rata-rata 3-RMS (baseline canary) — L2",
                         "skor_ringkas": {"median": round(float(np.median(rms_rank)), 4),
                                          "max": round(float(np.max(rms_rank)), 4)}}),
    ]
    blk = _engine_block("tool_wear", heads)
    blk["domain"] = REGISTRY["tool_wear"]["domain"]
    blk["catatan_klaim"] = ("label = identitas run (desain dataset); K-i detektor "
                            "PERUBAHAN-REGIME — bukan klaim 'keausan spesifik' "
                            "(precision run 0,50); lead DETIK bengkel, tidak dijumlah "
                            "dengan lead menit rig (D-A7)")
    return blk


def _engine_block(engine: str, heads: list[dict]) -> dict:
    return {
        "engine": engine,
        "klaim_tugas": REGISTRY[engine]["klaim_tugas"],
        "jenis_tugas": REGISTRY[engine]["jenis_tugas"],
        "sumber_tier": REGISTRY[engine]["sumber_tier"],
        "heads": heads,
    }


# ---------------------------------------------------------------------------
# 3. DECISION LAYER
# ---------------------------------------------------------------------------


def decision_layer(engines: list[dict]) -> dict:
    """Petakan head → L0/L1/L2/L3 dengan assertion keras (tanpa alarm otomatis)."""
    out = {k: [] for k in LAYERS}
    n_l1 = 0
    for e in engines:
        for h in e["heads"]:
            assert h["tier"] != TIER_FORBIDDEN, f"tier alarm-otomatis ditemukan: {h}"
            assert h["layer"] in LAYERS
            if h["layer"] == "L1":
                n_l1 += 1
                assert h["tier"] == T_SUPERV, "L1 hanya utk PERINGATAN-BERPENGAWAS"
                assert h["human_review_required"] is True, \
                    "setiap peringatan L1 wajib human_review_required"
            if h["tier"] in (T_TREN, T_NONE):
                assert h["layer"] != "L1", \
                    f"{e['engine']}/{h['head']} tier {h['tier']} tidak boleh L1"
            out[h["layer"]].append({
                "engine": e["engine"], "head": h["head"], "klaim": h.get("klaim"),
                "tier": h["tier"], "status": h.get("status"),
                "n_aktif": h.get("n_aktif"),
                "human_review_required": h["human_review_required"],
            })
    assert AUTO_CRITICAL_SLOTS == 0, "slot alarm otomatis kritis harus 0"
    return {
        "layers": out,
        "ringkasan": {k: len(v) for k, v in out.items()},
        "nperingatan_l1": n_l1,
        "auto_critical_alarm_slots": AUTO_CRITICAL_SLOTS,
        "keputusan_akhir": "MANUSIA (insinyur pengeboran) — tidak ada output otomatis "
                           "yang memicu tindakan tanpa konfirmasi",
    }

# ---------------------------------------------------------------------------
# 4. PROFIL KAPABILITAS (bukan bit lulus/gagal, lihat ml-system-evaluation)
# ---------------------------------------------------------------------------


def profil_kapabilitas(engines: list[dict]) -> list[dict]:
    """Satu profil per engine: jenis tugas, lapisan A/B/C, layak-untuk, belum-untuk.

    Lapisan B hanya ditandai TERUKUR bila head membawa angka lead atau jam henti.
    Selain itu ditulis BELUM TERUKUR, tanpa angka karangan.
    """
    out = []
    for e in engines:
        reg = REGISTRY.get(e["engine"], {})
        heads = e.get("heads", [])
        metrik = [h["metrik_segmen"] for h in heads if isinstance(h.get("metrik_segmen"), dict)]
        ada_lead = [h["head"] for h in heads if h.get("lead_menit") is not None]
        tier_l1 = [h["head"] for h in heads if h.get("layer") == "L1"]
        out.append({
            "engine": e["engine"],
            "jenis_tugas": reg.get("jenis_tugas"),
            "klaim_tugas": reg.get("klaim_tugas"),
            "lapisan_A_deteksi": {
                "head_dengan_metrik": len(metrik),
                "presisi_maks": max((m.get("precision") or 0 for m in metrik), default=None),
                "recall_maks": max((m.get("recall") or 0 for m in metrik), default=None),
                "far_min": min((m.get("far_segmen") for m in metrik if m.get("far_segmen") is not None), default=None),
            },
            "lapisan_B_nilai_maintenance": {
                "status": "TERUKUR" if ada_lead else "BELUM TERUKUR",
                "head_dengan_lead": ada_lead,
                "lead_menit": {h["head"]: h["lead_menit"] for h in heads if h.get("lead_menit") is not None},
                "alasan": None if ada_lead else "tidak ada angka lead/jam henti yang menempel pada head",
            },
            "lapisan_C_ketepatan": {
                "head_peringatan_L1": tier_l1,
                "keyakinan": [h.get("keyakinan") for h in heads if h.get("keyakinan")],
            },
            "layak_untuk": [h["batas_pemakaian"] for h in heads if h.get("layer") == "L1"] or ["pemantauan tren"],
            "belum_untuk": [h.get("status") for h in heads if h.get("tier") == T_NONE] or [],
            "kekuatan_bukti": ("SEDANG" if len(metrik) >= 2 else "LEMAH"),
        })
    return out


# ---------------------------------------------------------------------------
# 5. NILAI MAINTENANCE DARI DATA AKTIVITAS (DDR), BUKAN ASUMSI
# ---------------------------------------------------------------------------


def nilai_maintenance(engines: list[dict]) -> dict:
    """Jam henti nyata dari DDR Volve + beban tinjauan per shift tiap head L1.

    Sumber: data/volve/ddr.parquet kolom activity (23.447 record, 1.750 laporan).
    Beban tinjauan = FAR per 24 jam dibagi 3 shift (8 jam), pembulatan ke atas.
    """
    import math
    path = f"{BASE}/data/volve/ddr.parquet"
    total_h = 0.0
    per_code: dict[str, float] = {}
    per_detail: dict[str, float] = {}
    n_rec = 0
    try:
        ddr = pd.read_parquet(path, columns=["activity"])
        for arr in ddr["activity"]:
            if arr is None or not hasattr(arr, "__len__"):
                continue
            for a in arr:
                if not isinstance(a, dict):
                    continue
                s, t = a.get("dTimStart"), a.get("dTimEnd")
                if not s or not t:
                    continue
                try:
                    ts, te = pd.Timestamp(s), pd.Timestamp(t)
                except Exception:
                    continue
                h = (te - ts).total_seconds() / 3600.0
                if h <= 0 or h > 24 * 7:
                    continue
                n_rec += 1
                total_h += h
                code = str(a.get("proprietaryCode") or "lain")
                per_code[code] = per_code.get(code, 0.0) + h
                det = str(a.get("stateDetailActivity") or "-")
                if code.startswith("interruption"):
                    per_detail[det] = per_detail.get(det, 0.0) + h
    except Exception as exc:  # jalur data hilang harus terbaca, bukan diam
        return {"status": f"GAGAL BACA: {type(exc).__name__}: {exc}", "path": path}

    beban = []
    for e in engines:
        for h in e.get("heads", []):
            m = h.get("metrik_segmen")
            if not isinstance(m, dict) or m.get("far_segmen") is None:
                continue
            if h.get("layer") != "L1":
                continue
            beban.append({
                "engine": e["engine"], "head": h["head"],
                "far_per_24jam": round(float(m["far_segmen"]), 3),
                "tinjauan_per_shift_8jam": int(math.ceil(float(m["far_segmen"]) / 3.0)),
            })
    inter = {k: round(v, 3) for k, v in sorted(per_code.items(), key=lambda kv: -kv[1])[:8]}
    return {
        "sumber": path,
        "n_record_aktivitas": n_rec,
        "total_jam_tercatat": round(total_h, 3),
        "jam_per_kode": inter,
        "jam_henti_per_sebab": {k: round(v, 3) for k, v in sorted(per_detail.items(), key=lambda kv: -kv[1])[:6]},
        "beban_tinjauan_L1": beban,
        "batas": ("jam henti tidak dapat dipetakan ke satu alarm tertentu: tidak ada kunci bit atau work order "
                  "yang menghubungkan alarm ke record DDR"),
    }
