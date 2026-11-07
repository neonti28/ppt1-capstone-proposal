"""RND-E2: verifikasi statistik protokol, implementasi sendiri (stdlib saja).

Tujuan: bukan meminjam angka R6, tetapi menghitung ulang secara independen
supaya angka protokol punya dua jalur (R6 dan skrip ini).

Output: scratch/rnd_e2/e2_stats.json
"""
from __future__ import annotations

import json
import math
from pathlib import Path

OUT = Path("/mnt/d/Capstone 1(v2)/scratch/rnd_e2")
OUT.mkdir(parents=True, exist_ok=True)
R: dict = {}

# ---------------------------------------------------------------- 1. uji tanda eksak
def sign_p_two_sided(k: int, n: int) -> float:
    """p dua sisi eksak: 2 * P(X >= k) dengan X~Bin(n, 0.5), dipotong 1."""
    tail = sum(math.comb(n, i) for i in range(k, n + 1)) / 2 ** n
    return min(1.0, 2.0 * tail)

def sign_krit(n: int, alpha: float = 0.05) -> int | None:
    for k in range(0, n + 1):
        if sign_p_two_sided(k, n) <= alpha:
            return k
    return None

def sign_power(n: int, concord: float, alpha: float = 0.05) -> float:
    k = sign_krit(n, alpha)
    if k is None:
        return 0.0
    return sum(math.comb(n, i) * concord ** i * (1 - concord) ** (n - i)
               for i in range(k, n + 1))

tbl = {}
for n in (4, 7, 9):
    k = sign_krit(n)
    tbl[str(n)] = {
        "k_minimum_sepakat": k,
        "p_pada_k": None if k is None else round(sign_p_two_sided(k, n), 6),
        "p_minimum_mungkin": round(sign_p_two_sided(n, n), 6),
        "daya_konkordansi": {str(c): round(sign_power(n, c), 4)
                              for c in (0.7, 0.8, 0.9, 1.0)},
    }
R["sign_test"] = tbl

# ---------------------------------------------------------------- 2. Wilson untuk B1
def wilson(k: float, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    """Wilson score interval. k boleh pecahan supaya lebar pada p=0,5 dihitung tepat
    untuk n ganjil; memakai round(k) akan menggeser p dari 0,5 (bug yang ditemukan
    pada draf pertama skrip ini)."""
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    den = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, centre - half), min(1.0, centre + half))

wil = {}
for n in (3, 12, 20, 29, 30, 50, 100, 281):
    lo, hi = wilson(0.5 * n, n)
    wil[str(n)] = {"p": 0.5, "lo": round(lo, 4), "hi": round(hi, 4),
                   "lebar": round(hi - lo, 4), "setengah_lebar": round((hi - lo) / 2, 4)}
R["wilson_p05"] = wil

def n_untuk_setengah_lebar(target: float, p: float = 0.5) -> int:
    for n in range(2, 100000):
        lo, hi = wilson(p * n, n)
        if (hi - lo) / 2 <= target:
            return n
    return -1

R["wilson_n_untuk"] = {
    "setengah_lebar_0.05": n_untuk_setengah_lebar(0.05),
    "setengah_lebar_0.10": n_untuk_setengah_lebar(0.10),
    "setengah_lebar_0.168": n_untuk_setengah_lebar(0.168),
}

# B1 gabungan 0,1281 pada 281 onset (R6 2.4) dicek ulang
lo, hi = wilson(36, 281)
R["wilson_b1_281_cek"] = {"k": 36, "n": 281, "p": round(36 / 281, 4),
                          "lo": round(lo, 4), "hi": round(hi, 4)}
lo2, hi2 = wilson(245, 281)
R["wilson_b1_persist_cek"] = {"k": 245, "n": 281, "p": round(245 / 281, 4),
                              "lo": round(lo2, 4), "hi": round(hi2, 4)}

# ---------------------------------------------------------------- 3. batas resolusi FAR
# Garwood: batas atas eksak untuk 0 kejadian = chi2(1-alpha/2, 2)/2 per satuan paparan.
# KOREKSI yang dicatat: draf pertama skrip ini memakai chi2(0.95,2)/2 = 2,9957 dan
# MELABELI-nya "95% satu sisi". Nilai yang dipakai R6 (3,6889) adalah batas dua sisi
# 95% = chi2(0.975,2)/2. Untuk klaim sertifikasi FAR dipakai yang LEBIH KONSERVATIF
# (3,6889); nilai satu sisi dilaporkan sebagai bandingan, bukan dasar.
CHI2_95_2 = 5.991464547107979   # chi2.ppf(0.95, 2) -> batas satu sisi 95%
CHI2_975_2 = 7.377758908227872  # chi2.ppf(0.975, 2) -> batas dua sisi 95%
upper0_1sided = CHI2_95_2 / 2          # 2,9957
upper0_2sided = CHI2_975_2 / 2         # 3,6889 (dipakai, konservatif)
R["garwood"] = {
    "chi2_95_2": CHI2_95_2,
    "chi2_975_2": CHI2_975_2,
    "batas_atas_0_fp_1sisi": round(upper0_1sided, 4),
    "batas_atas_0_fp_2sisi": round(upper0_2sided, 4),
    "dipakai": round(upper0_2sided, 4),
    "jam_neg_min_untuk_far6_dengan_0fp_konservatif": round(upper0_2sided * 24 / 6, 4),
    "jam_neg_min_untuk_far6_dengan_0fp_satusisi": round(upper0_1sided * 24 / 6, 4),
}
# FP <= jam_neg/24*6  <=>  jam_neg >= 4*FP
R["jam_neg_min_per_fp"] = {str(fp): round(4.0 * fp, 2) for fp in (0, 1, 2, 3, 6, 12, 30)}
# cek ssi F-9_A: n_neg 786 jendela 60 dtk = 13,1 jam
jam = 786 * 60 / 3600
R["ssi_F9A"] = {"n_neg": 786, "jam_neg": round(jam, 4),
                "batas_atas_far_0fp_2sisi": round(upper0_2sided * 24 / jam, 4),
                "batas_atas_far_0fp_1sisi": round(upper0_1sided * 24 / jam, 4),
                "sertifikasi_far6_mungkin": bool(upper0_2sided * 24 / jam <= 6)}
# konvensi bengkel: FAR <= 1 alarm/menit, jendela 1 dtk (window 1)
R["bengkel_far_konvensi"] = {"batas_alarm_per_menit": 1.0,
                             "ekuivalen_alarm_per_60_detik": 1.0}

# ---------------------------------------------------------------- 4. fold underpowered
probe = json.loads((OUT / "e2_probe.json").read_text())
und = {}
THRESH = 30
for eng, info in probe["per_engine"].items():
    if "error" in info:
        continue
    ycol = [c for c in info["y_cols"] if not c.startswith("y_prev")][0]
    pos = {w: v.get(ycol, 0) for w, v in info["pos_per_well_per_label"].items()}
    small = {w: n for w, n in pos.items() if n < THRESH}
    und[eng] = {
        "label": ycol,
        "n_folds": len(pos),
        "positif_per_fold": pos,
        "fold_di_bawah_30": small,
        "n_fold_di_bawah_30": len(small),
        "n_fold_layak": len(pos) - len(small),
        "min_positif": min(pos.values()) if pos else None,
        "max_positif": max(pos.values()) if pos else None,
    }
R["underpowered"] = und
R["ambang_underpowered"] = THRESH

# ---------------------------------------------------------------- 5. skenario naik tier: FAR target
# untuk tiap engine: berapa FP yang boleh terjadi agar FAR<=6 pada paparan tertentu
R["fp_budget_far6"] = {f"{jam}jam": math.floor(jam / 24 * 6) for jam in (8, 12, 24, 48, 120)}

(OUT / "e2_stats.json").write_text(json.dumps(R, indent=2, ensure_ascii=False))
print(json.dumps({k: R[k] for k in ("sign_test", "wilson_p05", "garwood", "ssi_F9A",
                                    "ambang_underpowered")}, indent=2, ensure_ascii=False))
print("\n--- underpowered ---")
for eng, v in und.items():
    print(f"{eng}: folds={v['n_folds']} <30 = {v['n_fold_di_bawah_30']} {v['fold_di_bawah_30']}"
          f" min={v['min_positif']} max={v['max_positif']}")
print("\n--- fp budget ---")
print(R["fp_budget_far6"])
