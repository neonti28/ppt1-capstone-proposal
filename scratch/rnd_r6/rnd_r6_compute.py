"""R6 — METRIK, UJI STATISTIK, DAN DESAIN EKSPERIMEN (hitung dari JSON primer nyata).

Semua angka yang dicetak skrip ini masuk ke docs/RND_R6_METRIK.md dan ke
docs/RND_PROVENANCE_LEDGER.md. Tidak ada angka literatur di sini; hanya
(a) rekalkulasi identitas dari JSON primer, (b) uji statistik atas angka tersimpan,
(c) validasi implementasi uji pada data sintetis berbenih (bukan angka proyek).

Jalankan: .venv/bin/python rnd_r6_compute.py
Keluaran: rnd_r6_RESULTS.json (mesin) + ringkasan stdout.
"""

from __future__ import annotations

import json
import math
from itertools import combinations
from pathlib import Path

import numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.proportion import proportion_confint

BASE = Path("/mnt/d/Capstone 1(v2)")
SCR = BASE / "scratch"
OUT = SCR / "rnd_r6" / "rnd_r6_RESULTS.json"
RNG = np.random.default_rng(42)

R = {}  # hasil


def jp(x):
    """Bulatkan aman untuk JSON (None tetap None)."""
    if x is None:
        return None
    if isinstance(x, float) and (math.isnan(x) or math.isinf(x)):
        return None
    return x


# =====================================================================
# 1. IDENTITAS DEFINISI: FAR, lift, plafon lift  (rekalkulasi dari JSON)
# =====================================================================
def sec1_definisi():
    i1 = json.loads((SCR / "v9_i1" / "v9_i1_RESULTS.json").read_text(encoding="utf-8"))
    rows = []
    for e in i1["engines"]:
        for h in e["heads"]:
            m = h.get("metrik_segmen")
            if not m:
                continue
            fp, neg, far = m.get("fp"), m.get("neg"), m.get("far_segmen")
            if fp is None or not neg or far is None:
                continue
            unit = m.get("far_unit") or ""
            # Satuan tersimpan menentukan pengali: rig = jendela 60 dtk (1440/hari);
            # bengkel = jendela 1 dtk tetapi far_segmen dilaporkan PER MENIT (60).
            if "jendela 60" in unit:
                per_day, satuan_uji = 1440.0, "FP/24 jam-negatif"
            elif "jendela 1 dtk" in unit:
                per_day, satuan_uji = 60.0, "FP/menit-negatif"
            else:
                continue
            calc = fp / neg * per_day
            rows.append({
                "engine": e["engine"], "head": h["head"], "fp": fp, "neg": neg,
                "far_stored": far, "far_recalc": round(calc, 6),
                "abs_diff": round(abs(calc - far), 9),
                "far_unit": unit, "satuan_uji": satuan_uji, "pengali": per_day,
            })
    max_diff = max((r["abs_diff"] for r in rows), default=None)
    R["s1_far_identity"] = {
        "n_rows": len(rows),
        "max_abs_diff": max_diff,
        # angka tersimpan dibulatkan 3 desimal, jadi kesamaan diuji pada toleransi 5e-4
        "identik_sampai_pembulatan_3_desimal": (max_diff is not None and max_diff <= 5e-4),
        "n_baris_selisih_gt_5e-4": sum(1 for r in rows if r["abs_diff"] > 5e-4),
        "contoh": rows[:4],
        "contoh_bengkel": [r for r in rows if r["pengali"] == 60.0][:2],
    }

    # lift = AUPRC / prev ; plafon = 1/prev
    ml_files = ["v9_e_ml/v9_e_ML_vib_RESULTS.json", "v9_e_ml/v9_e_ML_ssi_RESULTS.json",
                "v9_e_ml/v9_e_ML_shk_RESULTS.json", "v9_e_ml/v9_e_ML_stuck_k2_RESULTS.json"]
    lift_rows = []
    for f in ml_files:
        d = json.loads((SCR / f).read_text(encoding="utf-8"))
        for fold in d["folds"]:
            prev = fold["prev_test"]
            for mname, mv in fold["models"].items():
                if not isinstance(mv, dict):
                    continue
                au, lf, pf = mv.get("auprc"), mv.get("lift"), mv.get("plafon_lift")
                if au is None or lf is None:
                    continue
                lift_rows.append({
                    "file": f.split("/")[-1], "well": fold["test_well"], "model": mname,
                    "auprc": au, "prev": prev, "lift_stored": lf,
                    "lift_calc": au / prev, "plafon_stored": pf, "plafon_calc": 1.0 / prev,
                    "d_lift": abs(lf - au / prev),
                    "d_plafon": abs((pf or 0) - 1.0 / prev),
                })
    R["s1_lift_identity"] = {
        "n_rows": len(lift_rows),
        "max_abs_diff_lift": round(max((r["d_lift"] for r in lift_rows), default=0.0), 12),
        "max_abs_diff_plafon": round(max((r["d_plafon"] for r in lift_rows), default=0.0), 12),
        "contoh": [{k: v for k, v in r.items() if not k.startswith("d_")} for r in lift_rows[:3]],
    }
    return i1


# =====================================================================
# 2. WILSON CI untuk presisi & recall tiap head (dari TP/FP/FN mentah)
# =====================================================================
def sec2_wilson(i1):
    rows = []
    for e in i1["engines"]:
        for h in e["heads"]:
            m = h.get("metrik_segmen")
            if not m or m.get("tp") is None:
                continue
            tp, fp, fn = m["tp"], m["fp"], m["fn"]
            lo_p, hi_p = proportion_confint(tp, tp + fp, alpha=0.05, method="wilson") \
                if (tp + fp) > 0 else (None, None)
            lo_r, hi_r = proportion_confint(tp, tp + fn, alpha=0.05, method="wilson") \
                if (tp + fn) > 0 else (None, None)
            rows.append({
                "engine": e["engine"], "head": h["head"], "klaim": h.get("klaim"),
                "tp": tp, "fp": fp, "fn": fn, "pos": m.get("pos"), "neg": m.get("neg"),
                "precision": m.get("precision"), "recall": m.get("recall"),
                "wilson_prec_lo": jp(lo_p), "wilson_prec_hi": jp(hi_p),
                "wilson_rec_lo": jp(lo_r), "wilson_rec_hi": jp(hi_r),
                "wilson_prec_width": (hi_p - lo_p) if lo_p is not None else None,
                "wilson_rec_width": (hi_r - lo_r) if lo_r is not None else None,
            })
    R["s2_wilson_heads"] = rows
    widths = [r["wilson_prec_width"] for r in rows if r["wilson_prec_width"] is not None]
    R["s2_ringkas"] = {
        "n_head": len(rows),
        "n_dgn_precision_terdefinisi": len(widths),
        "lebar_ci_presisi_min": round(min(widths), 4) if widths else None,
        "lebar_ci_presisi_max": round(max(widths), 4) if widths else None,
        "n_head_lebar_gt_0_10": sum(1 for w in widths if w > 0.10),
    }
    return rows


# =====================================================================
# 3. UJI BERPASANGAN: ΔB per well -> bootstrap berpasangan + uji tanda
# =====================================================================
def sec3_deltaB_paired():
    plan = [("v9_e_ml/v9_e_ML_shk_RESULTS.json", "shk"),
            ("v9_e_ml/v9_e_ML_ssi_RESULTS.json", "ssi"),
            ("v9_e_ml/v9_e_ML_vib_RESULTS.json", "vib"),
            ("v9_e_ml/v9_e_ML_stuck_k2_RESULTS.json", "stuck_k2")]
    out = []
    for f, eng in plan:
        d = json.loads((SCR / f).read_text(encoding="utf-8"))
        folds = [x for x in d["folds"] if not x.get("underpowered")]
        vals, wells = [], []
        for fold in folds:
            db = (fold.get("delta_B") or {}).get("rf_vs_persistence")
            if db is None:
                continue
            vals.append(db)
            wells.append(fold["test_well"])
        v = np.asarray(vals, dtype=float)
        n = len(v)
        if n == 0:
            continue
        # bootstrap berpasangan atas well (resample well, bukan jendela)
        nb = 5000
        idx = RNG.integers(0, n, size=(nb, n))
        boot = v[idx].mean(axis=1)
        lo, hi = np.percentile(boot, [2.5, 97.5])
        n_pos = int((v > 0).sum())
        # uji tanda dua sisi eksak (H0: p=0,5)
        p_sign = stats.binomtest(n_pos, n, 0.5, alternative="two-sided").pvalue
        # Wilcoxon signed-rank (exact bila n<=25)
        try:
            p_w = stats.wilcoxon(v, zero_method="wilcox", alternative="two-sided",
                                 method="exact").pvalue
        except Exception:  # noqa: BLE001
            p_w = None
        out.append({
            "engine": eng, "n_well": n, "wells": wells,
            "mean_deltaB": float(v.mean()), "median_deltaB": float(np.median(v)),
            "min": float(v.min()), "max": float(v.max()),
            "boot_ci95": [float(lo), float(hi)],
            "boot_includes_zero": bool(lo <= 0 <= hi),
            "n_pos": n_pos, "n_neg": int((v < 0).sum()), "n_tie": int((v == 0).sum()),
            "p_sign": float(p_sign), "p_wilcoxon": (float(p_w) if p_w is not None else None),
        })
    R["s3_deltaB_paired"] = out
    return out


# =====================================================================
# 4. FISHER (independen) vs McNEMAR (berpasangan) + koreksi multiplisitas
# =====================================================================
def sec4_fisher_mcnemar(i1):
    # 4a. Fisher: FAR dua well berbeda (independen) memakai FP/neg per well ML vib tau0,5
    d = json.loads((SCR / "v9_e_ml" / "v9_e_ML_vib_RESULTS.json").read_text(encoding="utf-8"))
    cells, wells = [], []
    for fold in d["folds"]:
        tm = fold["models"]["rf"]["tau_metrics"]["0.5"]
        fp, neg = tm["FP"], tm["n_neg"]
        cells.append((fp, neg - fp))
        wells.append(fold["test_well"])
    pairs = []
    for (i, j) in combinations(range(len(cells)), 2):
        (a, b), (c, dd) = cells[i], cells[j]
        odds, p = stats.fisher_exact([[a, b], [c, dd]])
        pairs.append({"well_a": wells[i], "well_b": wells[j],
                      "fp_a": a, "neg_a": b, "fp_b": c, "neg_b": dd,
                      "odds_ratio": (float(odds) if odds == odds else None), "p_fisher": float(p)})
    if pairs:
        praw = [x["p_fisher"] for x in pairs]
        holm = multipletests(praw, alpha=0.05, method="holm")[1]
        bh = multipletests(praw, alpha=0.05, method="fdr_bh")[1]
        for k, x in enumerate(pairs):
            x["p_holm"] = float(holm[k])
            x["p_bh"] = float(bh[k])
            x["sig_raw"] = bool(x["p_fisher"] < 0.05)
            x["sig_holm"] = bool(holm[k] < 0.05)
    R["s4a_fisher_far_antarwell_vib"] = {
        "n_uji": len(pairs), "uji": pairs,
        "n_sig_raw": sum(1 for x in pairs if x["sig_raw"]),
        "n_sig_holm": sum(1 for x in pairs if x["sig_holm"]),
    }

    # 4b. McNemar: perbandingan berpasangan rule vs persistence pada jendela yang sama
    #     Hanya selisih total alarm (b-c) yang dapat dipulihkan dari agregat JSON.
    mcn = []
    for e in i1["engines"]:
        hmap = {h["head"]: h for h in e["heads"] if h.get("metrik_segmen")}
        for hname, other in (("rule_display", "persistence"),
                             ("hybrid_rule_and_persistence", "rule_display")):
            if hname not in hmap or other not in hmap:
                continue
            A, B = hmap[hname]["metrik_segmen"], hmap[other]["metrik_segmen"]
            alarm_a = (A["tp"] or 0) + (A["fp"] or 0)
            alarm_b = (B["tp"] or 0) + (B["fp"] or 0)
            diff = alarm_a - alarm_b
            # batas bawah p eksak McNemar: b minimal = |diff|, c = 0 (atau sebaliknya)
            k = abs(diff)
            p_min = 2.0 * (0.5 ** k) if k > 0 else 1.0
            p_min = min(1.0, p_min)
            mcn.append({
                "engine": e["engine"], "head": hname, "pembanding": other,
                "alarm_head": alarm_a, "alarm_pembanding": alarm_b,
                "b_minus_c": diff,
                "p_mcnemar_batas_bawah": float(p_min),
                "catatan": "tabel diskordan b/c per jendela TIDAK tersimpan; hanya b-c total",
            })
    R["s4b_mcnemar_bound"] = mcn

    # 4c. Koreksi multiplisitas pada keluarga uji tanda ΔB (4 engine)
    fam = [(x["engine"], x["p_sign"]) for x in R["s3_deltaB_paired"]]
    if fam:
        praw = [p for _, p in fam]
        holm = multipletests(praw, alpha=0.05, method="holm")[1]
        bh = multipletests(praw, alpha=0.05, method="fdr_bh")[1]
        R["s4c_koreksi_keluarga_deltaB"] = [
            {"engine": fam[i][0], "p_raw": float(praw[i]),
             "p_holm": float(holm[i]), "p_bh": float(bh[i])}
            for i in range(len(fam))
        ]
        # ilustrasi efek koreksi pada 27 head (family-wise 11 klaim x 3 head)
        R["s4c_ilustrasi_alpha"] = {
            "n_keluarga": 4, "alpha_raw": 0.05,
            "alpha_holm_terkecil": float(0.05 / 4),
        }
    return mcn


# =====================================================================
# 5. DELONG: implementasi + validasi pada data sintetis berbenih
# =====================================================================
def _midrank(x):
    J = np.argsort(x)
    Z = x[J]
    N = len(x)
    T = np.zeros(N, dtype=float)
    i = 0
    while i < N:
        j = i
        while j < N and Z[j] == Z[i]:
            j += 1
        T[i:j] = 0.5 * (i + j - 1) + 1
        i = j
    T2 = np.empty(N, dtype=float)
    T2[J] = T
    return T2


def delong_components(scores, labels):
    """V10/V01 struktural DeLong. labels: 1 positif, 0 negatif."""
    scores = np.asarray(scores, dtype=float)
    labels = np.asarray(labels, dtype=int)
    pos = scores[labels == 1]
    neg = scores[labels == 0]
    m, n = len(pos), len(neg)
    tx = _midrank(pos)
    ty = _midrank(neg)
    tz = _midrank(np.concatenate([pos, neg]))
    tz_pos, tz_neg = tz[:m], tz[m:]
    auc = (tz_pos.sum() - m * (m + 1) / 2.0) / (m * n)
    v10 = (tz_pos - tx) / n
    v01 = 1.0 - (tz_neg - ty) / m
    return auc, v10, v01, m, n


def delong_test(scores_a, scores_b, labels):
    auc_a, v10a, v01a, m, n = delong_components(scores_a, labels)
    auc_b, v10b, v01b, _, _ = delong_components(scores_b, labels)
    s10 = np.cov(np.vstack([v10a, v10b]))
    s01 = np.cov(np.vstack([v01a, v01b]))
    S = s10 / m + s01 / n
    var = S[0, 0] + S[1, 1] - 2 * S[0, 1]
    if var <= 0:
        z, p = 0.0, 1.0
    else:
        z = (auc_a - auc_b) / math.sqrt(var)
        p = 2 * (1 - stats.norm.cdf(abs(z)))
    return {"auc_a": auc_a, "auc_b": auc_b, "delta": auc_a - auc_b,
            "se": math.sqrt(max(var, 0.0)), "z": z, "p": p}


def hanley_mcneil_var(auc, m, n):
    q1 = auc / (2 - auc)
    q2 = 2 * auc * auc / (1 + auc)
    return (auc * (1 - auc) + (m - 1) * (q1 - auc * auc) + (n - 1) * (q2 - auc * auc)) / (m * n)


def sec5_delong_validation():
    rng = np.random.default_rng(7)
    # 5a. Kecocokan AUC DeLong vs U Mann-Whitney (definisi langsung)
    auc_diffs = []
    for _ in range(200):
        n1, n0 = 40, 120
        s = np.concatenate([rng.normal(1.0, 1.0, n1), rng.normal(0.0, 1.0, n0)])
        y = np.concatenate([np.ones(n1, int), np.zeros(n0, int)])
        auc_dl, *_ = delong_components(s, y)
        u = stats.mannwhitneyu(s[y == 1], s[y == 0], alternative="two-sided").statistic
        auc_mw = u / (n1 * n0)
        auc_diffs.append(abs(auc_dl - auc_mw))
    # 5b. Varians DeLong vs aproksimasi Hanley-McNeil
    var_rel = []
    for _ in range(200):
        n1, n0 = 40, 120
        s = np.concatenate([rng.normal(1.2, 1.0, n1), rng.normal(0.0, 1.0, n0)])
        y = np.concatenate([np.ones(n1, int), np.zeros(n0, int)])
        auc, v10, v01, m, n = delong_components(s, y)
        var_dl = np.var(v10, ddof=1) / m + np.var(v01, ddof=1) / n
        var_hm = hanley_mcneil_var(auc, m, n)
        var_rel.append(var_dl / var_hm)
    # 5c. Type-I error di bawah H0 (dua skor dari distribusi sama)
    rej0 = 0
    NT = 2000
    for _ in range(NT):
        y = np.concatenate([np.ones(60, int), np.zeros(180, int)])
        sa = rng.normal(0, 1, 240)
        sb = rng.normal(0, 1, 240)
        if delong_test(sa, sb, y)["p"] < 0.05:
            rej0 += 1
    # 5d. Power di bawah H1 (delta AUC diketahui lewat konstruksi)
    rej1 = 0
    for _ in range(NT):
        y = np.concatenate([np.ones(60, int), np.zeros(180, int)])
        sa = np.where(y == 1, rng.normal(1.2, 1, 240), rng.normal(0, 1, 240))
        sb = rng.normal(0, 1, 240)
        if delong_test(sa, sb, y)["p"] < 0.05:
            rej1 += 1
    # 5e. AUPRC: apakah DeLong berlaku? Bandingkan batas CI DeLong-style vs bootstrap
    R["s5_delong_validasi"] = {
        "n_rep_auc_vs_mw": 200,
        "max_abs_diff_auc_delong_vs_mannwhitney": float(max(auc_diffs)),
        "median_rasio_var_delong_vs_hanleymcneil": float(np.median(var_rel)),
        "iqr_rasio_var": [float(np.percentile(var_rel, 25)), float(np.percentile(var_rel, 75))],
        "type_I_error": rej0 / NT, "n_sim_type_I": NT,
        "power_alt_delta_konstruksi": rej1 / NT,
        "catatan_auprc": "DeLong adalah uji dua-sampel U-statistik untuk AUROC; AUPRC bukan "
                         "U-statistik sehingga tidak memakai rumus DeLong.",
    }

    # 5f. Bootstrap stratifikasi untuk AUPRC: cakupan CI diukur terhadap "kebenaran"
    #     yang diestimasi dari replika besar independen (bukan terhadap titik sendiri).
    def auprc(y, s):
        order = np.argsort(-s, kind="mergesort")
        y = y[order]
        tp = np.cumsum(y)
        fp = np.cumsum(1 - y)
        prec = tp / np.maximum(tp + fp, 1)
        return float(prec[y == 1].mean())

    cov, widths = 0, []
    NS, NTRUTH = 300, 200_000
    for _ in range(NS):
        y = (rng.random(800) < 0.10).astype(int)
        s = np.where(y == 1, rng.normal(1.0, 1, 800), rng.normal(0, 1, 800))
        # kebenaran: AUPRC pada sampel besar dari DGP yang sama
        yt = (rng.random(NTRUTH) < 0.10).astype(int)
        st = np.where(yt == 1, rng.normal(1.0, 1, NTRUTH), rng.normal(0, 1, NTRUTH))
        truth = auprc(yt, st)
        bs = []
        for _ in range(400):
            ip = rng.integers(0, int(y.sum()), int(y.sum()))
            inn = rng.integers(0, int((1 - y).sum()), int((1 - y).sum()))
            yb = np.concatenate([np.ones(len(ip), int), np.zeros(len(inn), int)])
            sb = np.concatenate([s[y == 1][ip], s[y == 0][inn]])
            bs.append(auprc(yb, sb))
        lo, hi = np.percentile(bs, [2.5, 97.5])
        widths.append(hi - lo)
        if lo <= truth <= hi:
            cov += 1
    R["s5f_bootstrap_auprc"] = {
        "n_sim": NS, "n_boot": 400, "n_truth_sample": NTRUTH,
        "cakupan_ci95_pct": 100.0 * cov / NS,
        "lebar_ci_median": float(np.median(widths)),
        "sampel_per_replikasi": 800, "prevalensi_dgp": 0.10,
        "catatan": "kebenaran = AUPRC pada 200.000 sampel dari DGP sama; cakupan nominal 95%.",
    }


# =====================================================================
# 6. KEKUATAN UJI & EFEK MINIMUM TERDETEKSI (MDE)
# =====================================================================
def sec6_power():
    out = {}
    # 6a. Level well, n=9: uji tanda eksak dua sisi
    n = 9
    alpha = 0.05

    def p_two_sided(k, nn):
        return float(stats.binomtest(k, nn, 0.5, alternative="two-sided").pvalue)

    def k_upper(nn):
        """k TERKECIL di ekor atas sehingga dua-sisi p < alpha."""
        for k in range(nn // 2 + 1, nn + 1):
            if p_two_sided(k, nn) < alpha:
                return k
        return None

    crit_up = k_upper(n)
    crit_lo = (n - crit_up) if crit_up is not None else None

    def power_sign(q, nn, thresh):
        return sum(math.comb(nn, k) * q ** k * (1 - q) ** (nn - k)
                   for k in range(thresh, nn + 1))

    # MDE: q terkecil yang memberi power >= 0.80 pada ambang k_upper
    qs = np.linspace(0.5, 1.0, 5001)
    pw = np.array([power_sign(q, n, crit_up) for q in qs])
    idx = int(np.argmax(pw >= 0.80))
    mde_q = float(qs[idx]) if pw[idx] >= 0.80 else None
    out["s6a_uji_tanda_n9"] = {
        "n_well": n, "alpha": alpha,
        "k_kritis_ekor_atas": crit_up,
        "k_kritis_ekor_bawah": crit_lo,
        "p_pada_k_8": p_two_sided(8, n),
        "p_pada_k_9": p_two_sided(9, n),
        "power_pada_q_0_80": power_sign(0.80, n, crit_up),
        "power_pada_q_0_90": power_sign(0.90, n, crit_up),
        "power_pada_q_0_95": power_sign(0.95, n, crit_up),
        "power_pada_q_1_00": power_sign(1.00, n, crit_up),
        "MDE_q_untuk_power_0_80": mde_q,
        "n_minimal_agar_bisa_signifikan": next(
            (nn for nn in range(2, 41) if k_upper(nn) is not None), None),
        "tafsir": "q = fraksi well yang benar-benar membaik; dengan n=9 hanya 8/9 atau 9/9 "
                  "yang mencapai alpha 0,05",
    }
    # 6b. Wilcoxon signed-rank eksak, n=9
    try:
        cw = stats.wilcoxon(np.arange(1, n + 1, dtype=float), method="exact",
                            alternative="two-sided")
        p_all_same_sign = float(cw.pvalue)
    except Exception:  # noqa: BLE001
        p_all_same_sign = None
    # cari nilai kritis W (jumlah rank terkecil) pada alpha 0.05 dua sisi, n=9
    ncomb = 2 ** n
    dist = []
    for mask in range(ncomb):
        w = sum((i + 1) for i in range(n) if mask >> i & 1)
        dist.append(w)
    dist = np.array(sorted(dist))
    alpha_cum = 0.0
    w_crit = None
    for w in range(0, int(dist.max()) + 1):
        cnt = int((dist <= w).sum())
        if 2 * cnt / ncomb <= 0.05:
            w_crit = w
            alpha_cum = 2 * cnt / ncomb
    out["s6b_wilcoxon_n9"] = {
        "n": n, "nilai_kritis_W_dua_sisi": w_crit,
        "alpha_tercapai": float(alpha_cum),
        "p_semua_searah": p_all_same_sign,
        "tafsir": "dengan n=9 hanya semua tanda searah (atau 1 menyimpang) yang bisa signifikan",
    }
    # 6c. Level jendela: MDE AUROC via Hanley-McNeil pada hitungan nyata
    real = []
    for f, eng in [("v9_e_ml/v9_e_ML_shk_RESULTS.json", "shk"),
                   ("v9_e_ml/v9_e_ML_ssi_RESULTS.json", "ssi"),
                   ("v9_e_ml/v9_e_ML_vib_RESULTS.json", "vib"),
                   ("v9_e_ml/v9_e_ML_stuck_k2_RESULTS.json", "stuck_k2")]:
        d = json.loads((SCR / f).read_text(encoding="utf-8"))
        for fold in d["folds"]:
            npos = fold["pos_test"]
            nneg = fold["n_test"] - npos
            if npos < 5 or nneg < 5:
                real.append({"engine": eng, "well": fold["test_well"], "pos": npos,
                             "neg": nneg, "mde_auroc": None, "catatan": "pos<5"})
                continue
            # MDE dua sisi 80% power untuk AUROC=0,5 (konservatif): delta = (z.975+z.8)*SE
            se = math.sqrt(hanley_mcneil_var(0.5, npos, nneg))
            mde = (stats.norm.ppf(0.975) + stats.norm.ppf(0.80)) * se
            real.append({"engine": eng, "well": fold["test_well"], "pos": npos,
                         "neg": nneg, "prev": npos / fold["n_test"],
                         "se_auroc_null": se, "mde_auroc_delta": mde})
    R["s6c_mde_auroc_jendela"] = real
    ok = [x for x in real if x.get("mde_auroc_delta")]
    out["s6c_ringkas_mde_auroc"] = {
        "n_fold": len(real), "n_terhitung": len(ok),
        "mde_min": round(min(x["mde_auroc_delta"] for x in ok), 4) if ok else None,
        "mde_max": round(max(x["mde_auroc_delta"] for x in ok), 4) if ok else None,
        "mde_median": round(float(np.median([x["mde_auroc_delta"] for x in ok])), 4) if ok else None,
    }
    # 6d. MDE AUPRC dari lebar CI tersimpan (SE = lebar/3,92)
    apr = []
    for f, eng in [("v9_e_ml/v9_e_ML_shk_RESULTS.json", "shk"),
                   ("v9_e_ml/v9_e_ML_vib_RESULTS.json", "vib")]:
        d = json.loads((SCR / f).read_text(encoding="utf-8"))
        for fold in d["folds"]:
            for mname, mv in fold["models"].items():
                ci = (mv or {}).get("ci95")
                if not ci:
                    continue
                se = (ci[1] - ci[0]) / 3.92
                apr.append({"engine": eng, "well": fold["test_well"], "model": mname,
                            "auprc": mv["auprc"], "ci95": ci,
                            "se_turunan": se,
                            "mde_delta_auprc_80pct": (stats.norm.ppf(0.975) + stats.norm.ppf(0.80)) * se})
    R["s6d_mde_auprc_dari_ci"] = apr
    if apr:
        out["s6d_ringkas"] = {
            "n": len(apr),
            "mde_min": round(min(x["mde_delta_auprc_80pct"] for x in apr), 4),
            "mde_max": round(max(x["mde_delta_auprc_80pct"] for x in apr), 4),
            "mde_median": round(float(np.median([x["mde_delta_auprc_80pct"] for x in apr])), 4),
        }
    # 6e. Berapa well dibutuhkan untuk mendeteksi efek yang lebih kecil
    #     Memakai uji tanda eksak dengan ambang kritis yang SAH pada alpha=0,05.
    need = {}
    for q in (0.60, 0.70, 0.80, 0.90):
        for nn in range(2, 61):
            ku = k_upper(nn)
            if ku is None:
                continue
            p = power_sign(q, nn, ku)
            if p >= 0.80:
                need[f"q={q}"] = {"n_well": nn, "power": float(p),
                                  "ambang_k": ku, "alpha_uji": p_two_sided(ku, nn)}
                break
        else:
            need[f"q={q}"] = {"n_well": None, "catatan": "tidak tercapai sampai n=60"}
    out["s6e_well_dibutuhkan"] = need
    R["s6_power"] = out


# =====================================================================
# 7. ATURAN BERHENTI: batas "tidak ada bukti" yang bisa dihitung
# =====================================================================
def sec7_stopping():
    n = 9
    # daerah "tidak ada bukti" untuk uji tanda n=9
    zone = [k for k in range(n + 1)
            if stats.binomtest(k, n, 0.5, alternative="two-sided").pvalue >= 0.05]
    # batas futility: bila setelah n well hasilnya di zona ini, hentikan (bukan tunggu waktu)
    # hitung juga posterior Beta(1,1) P(q>0.5 | k dari n)
    post = []
    for k in range(n + 1):
        # Beta(1+k, 1+n-k)
        p_gt = 1 - stats.beta.cdf(0.5, 1 + k, 1 + n - k)
        post.append({"k": k, "P_q_gt_0_5": float(p_gt),
                     "p_sign": float(stats.binomtest(k, n, 0.5, alternative="two-sided").pvalue)})
    R["s7_stopping"] = {
        "n_well": n,
        "zona_tidak_ada_bukti_k": zone,
        "n_zona": len(zone),
        "posterior": post,
        "ambang_berhenti_tidak_ada_bukti": "hentikan bila k berada di zona dan tidak ada "
                                           "well tersisa; jangan perpanjang waktu untuk "
                                           "mengejar k di luar zona",
    }


# =====================================================================
# 8. RINGKASAN
# =====================================================================
def main():
    i1 = sec1_definisi()
    sec2_wilson(i1)
    sec3_deltaB_paired()
    sec4_fisher_mcnemar(i1)
    sec5_delong_validation()
    sec6_power()
    sec7_stopping()

    R["meta"] = {
        "task": "t_5ffc95c0 RND-R6",
        "generated_at": __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "seed": 42,
        "sumber_primer": [
            "scratch/v9_i1/v9_i1_RESULTS.json",
            "scratch/v9_e_ml/v9_e_ML_vib_RESULTS.json",
            "scratch/v9_e_ml/v9_e_ML_ssi_RESULTS.json",
            "scratch/v9_e_ml/v9_e_ML_shk_RESULTS.json",
            "scratch/v9_e_ml/v9_e_ML_stuck_k2_RESULTS.json",
        ],
        "versi_pustaka": {
            "numpy": np.__version__,
            "scipy": __import__("scipy").__version__,
            "statsmodels": __import__("statsmodels").__version__,
        },
    }
    OUT.write_text(json.dumps(R, indent=1, ensure_ascii=False), encoding="utf-8")
    print("=== RINGKASAN HITUNG R6 ===")
    print("1) FAR identik:", R["s1_far_identity"]["identik"],
          "| n baris:", R["s1_far_identity"]["n_rows"],
          "| max selisih:", R["s1_far_identity"]["max_abs_diff"])
    print("2) lift identik: max |d| =", R["s1_lift_identity"]["max_abs_diff_lift"],
          "| plafon max |d| =", R["s1_lift_identity"]["max_abs_diff_plafon"])
    print("3) Wilson head:", R["s2_ringkas"])
    print("4) DeltaB berpasangan:")
    for x in R["s3_deltaB_paired"]:
        print(f"   {x['engine']:9s} n={x['n_well']} mean={x['mean_deltaB']:+.4f} "
              f"CI95=[{x['boot_ci95'][0]:+.4f},{x['boot_ci95'][1]:+.4f}] "
              f"pos={x['n_pos']}/{x['n_well']} p_sign={x['p_sign']:.4f} "
              f"p_wilcox={x['p_wilcoxon']}")
    print("5) Fisher FAR vib: n_uji=", R["s4a_fisher_far_antarwell_vib"]["n_uji"],
          "sig_raw=", R["s4a_fisher_far_antarwell_vib"]["n_sig_raw"],
          "sig_holm=", R["s4a_fisher_far_antarwell_vib"]["n_sig_holm"])
    for x in R["s4a_fisher_far_antarwell_vib"]["uji"]:
        print(f"   {x['well_a']} vs {x['well_b']}: p={x['p_fisher']:.3g} "
              f"holm={x['p_holm']:.3g} bh={x['p_bh']:.3g} OR={x['odds_ratio']}")
    print("6) McNemar batas bawah:")
    for x in R["s4b_mcnemar_bound"]:
        print(f"   {x['engine']:8s} {x['head']:30s} b-c={x['b_minus_c']:+6d} "
              f"p_min={x['p_mcnemar_batas_bawah']:.3g}")
    print("7) DeLong validasi:", json.dumps(R["s5_delong_validasi"], ensure_ascii=False))
    print("8) Bootstrap AUPRC:", json.dumps(R["s5f_bootstrap_auprc"], ensure_ascii=False))
    print("9) Power:", json.dumps(R["s6_power"], ensure_ascii=False, indent=1)[:2200])
    print("10) Stopping zona:", R["s7_stopping"]["zona_tidak_ada_bukti_k"])
    print("\n-> ditulis:", OUT)


if __name__ == "__main__":
    main()
