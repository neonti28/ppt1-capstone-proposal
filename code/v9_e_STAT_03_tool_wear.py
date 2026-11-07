#!/usr/bin/env python3
"""V9-E_STAT 03 — engine tool_wear-K-i (change-point SSE+permutation + kalibrasi within-tool).

Spesifikasi: docs/V9_PM1_ARCHITECTURE.md §2.7 (K-i) + docs/V9_R1_JUSTIFICATION.md §3.7.
Data: Mendeley th4yv974r2 -> scratch/v6_e1/toolwear_windows.csv (469 jendela 1 dtk,
27 fitur getaran; resep fitur = v6_e1_50_toolwear.py; label = identitas run, desain dataset).

BAGIAN A — change-point 1-split SSE + permutation 500x (seed 42):
  SSE(tau) = sum_{t<=tau}(x_t-mu1)^2 + sum_{t>tau}(x_t-mu2)^2 ; tau* = argmin
  p = (1 + #{SSE_perm >= SSE_obs-drop}) / (1+500)   [arah = V8 v8e_cp_validity.py:
  drop besar = signifikan]. CATATAN: teks R1 §3.7 menulis "# {SSE_perm <= SSE_obs}"
  (arah terbalik) dan "ambang p=0,002" — keduanya dilaporkan sebagai temuan
  change-control; EKSEKUSI memakai arah benar (>=) dan DUA ambang:
  p<=0.05 (resep V8) DAN p<=0.002 (literal spek; = p minimal yang tercapai dgn
  500 permutasi, 1/501=0.001996). Keduanya dilaporkan — tidak pilih hasil.
  Tes pembeda t_cp: cp di jendela awal (<5 dtk) di >50% run = artefak termal
  -> sub-klaim gugur. Juga: spesifisitas = cp signifikan di alat BARU (R01).

BAGIAN B — kalibrasi within-tool (median+MAD 30% awal R01, alarm >=5/27 fitur |z|>3)
  + baseline rule 3-RMS (>=1 kanal RMS |z|>3, kalibrasi sama) -> kurangi_ragu B3.

C) titik operasi FAR-terkalibrasi (threshold = kuantile skor R01; target 1.0 & 0.2 alarm/menit).
D) AUPRC ranking jendela (skor = jumlah fitur |z|>3, label = identitas run) vs
   baseline identity-run majority (prev; plafon 1/prev). persistence N/A (label konstan
   dlm run — DINYATAKAN, resep R1 §3.7).

Output (S6): scratch/v9_e_stat/v9_e_stat_03_tool_wear_RESULTS.json + run log.
"""
import json, os, time
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score

CSV = "/mnt/d/Capstone 1(v2)/scratch/v6_e1/toolwear_windows.csv"
OUT = "/mnt/d/Capstone 1(v2)/scratch/v9_e_stat"
os.makedirs(OUT, exist_ok=True)
LOGP = f"{OUT}/v9_e_stat_03_run_log.txt"
SEED, N_PERM, MIN_SEG, EARLY_W = 42, 500, 5, 5
P_V8, P_LIT = 0.05, 0.002
CAL_FRAC, Z_THR, N_FEAT_ALARM = 0.30, 3.0, 5
META = ["tool", "run", "file", "start_sample", "y"]
FAMS = {"kurt": ["X_kurt", "Y_kurt", "Z_kurt"],
        "crest": ["X_crest", "Y_crest", "Z_crest"],
        "fdom": ["X_fdom", "Y_fdom", "Z_fdom"],
        "rms": ["X_rms", "Y_rms", "Z_rms"]}
ALLF = [c for v in FAMS.values() for c in v]
log_lines = []


def log(m):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {m}"
    print(line, flush=True)
    log_lines.append(line)


def sse_split(Z):
    n = Z.shape[0]
    csum = np.cumsum(Z, axis=0)
    csum2 = np.cumsum(Z ** 2, axis=0)
    tot_sse = float(csum2[-1].sum() - (csum[-1] ** 2).sum() / n)
    best_i, best_drop = None, -np.inf
    for i in range(MIN_SEG, n - MIN_SEG + 1):
        s1, s2 = csum[i - 1], csum[-1] - csum[i - 1]
        q1, q2 = csum2[i - 1], csum2[-1] - csum2[i - 1]
        m1, m2 = i, n - i
        sse = float(q1.sum() - (s1 ** 2).sum() / m1) + \
            float(q2.sum() - (s2 ** 2).sum() / m2)
        drop = tot_sse - sse
        if np.isfinite(drop) and drop > best_drop:
            best_drop, best_i = drop, i
    if best_i is None:
        raise RuntimeError(f"sse_split: no valid split (n={n})")
    return best_i, float(best_drop)


def perm_p(Z, rng):
    _, obs = sse_split(Z)
    cnt = 0
    for _ in range(N_PERM):
        Zp = Z[rng.permutation(Z.shape[0])]
        _, d = sse_split(Zp)
        if d >= obs:            # arah benar (V8): drop perm >= drop obs
            cnt += 1
    return (cnt + 1) / (N_PERM + 1), obs


def main():
    t0 = time.time()
    df = pd.read_csv(CSV)
    feats = [c for c in df.columns if c not in META]
    rms3 = ["X_rms", "Y_rms", "Z_rms"]
    rng = np.random.default_rng(SEED)
    log(f"toolwear_windows rows={len(df)} feats={len(feats)} "
        f"tools={sorted(df.tool.unique())}")

    # ---------- BAGIAN A: change-point + permutation ----------
    cp_rows = []
    for (tool, run), g in df.groupby(["tool", "run"]):
        g = g.sort_values("start_sample").reset_index(drop=True)
        n = len(g)
        Z_all = ((g[ALLF] - g[ALLF].mean()) /
                 g[ALLF].std(ddof=0).replace(0, np.nan)).fillna(0.0).to_numpy()
        p_all, drop_all = perm_p(Z_all, rng)
        i_all, _ = sse_split(Z_all)
        rec = {"tool": tool, "run": run, "n_windows": n,
               "y_progression": 1 if run == "R02" else 0,
               "t_cp_s": int(i_all), "t_cp_frac": round(i_all / n, 3),
               "sse_drop": round(drop_all, 2), "perm_p": round(p_all, 4),
               "sig_p05_v8": bool(p_all <= P_V8),
               "sig_p002_literal": bool(p_all <= P_LIT),
               "early_5s": bool(i_all < EARLY_W),
               "early_10pct": bool(i_all < max(1, int(np.ceil(0.10 * n))))}
        for fam, cols in FAMS.items():
            Zf = ((g[cols] - g[cols].mean()) /
                  g[cols].std(ddof=0).replace(0, np.nan)).fillna(0.0).to_numpy()
            i_f, _ = sse_split(Zf)
            p_f = perm_p(Zf, rng)[0]
            rho = float(pd.Series(g[cols].mean(axis=1)).corr(
                pd.Series(np.arange(n)), method="spearman"))
            rec[f"t_cp_{fam}"] = int(i_f)
            rec[f"perm_p_{fam}"] = round(p_f, 4)
            rec[f"rho_time_{fam}"] = round(rho, 3)
        cp_rows.append(rec)
        log(f"  [cp {tool} {run}] n={n} t_cp={i_all}s p={p_all:.4f} "
            f"sig05={rec['sig_p05_v8']} sig002={rec['sig_p002_literal']} "
            f"early5={rec['early_5s']}")

    r = pd.DataFrame(cp_rows)
    fam_cols = [f"t_cp_{f}" for f in FAMS]
    r["fam_spread_s"] = r[fam_cols].max(axis=1) - r[fam_cols].min(axis=1)
    r01, r02 = r[r.run == "R01"], r[r.run == "R02"]
    n_runs = len(r)
    n_early = int(r["early_5s"].sum())

    def run_level(sig_col):
        tp = int(((r.y_progression == 1) & r[sig_col]).sum())
        fp = int(((r.y_progression == 0) & r[sig_col]).sum())
        fn = int(((r.y_progression == 1) & ~r[sig_col]).sum())
        tn = int(((r.y_progression == 0) & ~r[sig_col]).sum())
        return dict(tp=tp, fp=fp, fn=fn, tn=tn,
                    precision=(tp / (tp + fp) if (tp + fp) else None),
                    recall=(tp / (tp + fn) if (tp + fn) else None))

    lead = r.n_windows - r.t_cp_s
    r = r.assign(t_lead_s=lead)
    part_a = {
        "method": "SSE 1-split + permutation 500x seed42; fitur progresi 12-dim "
                  "(kurt/crest/fdom/rms x XYZ), standardisasi in-run",
        "formula_note_change_control": (
            "R1 §3.7 menulis p=(1+#{SSE_perm <= SSE_obs})/501 — arah terbalik; "
            "implementasi memakai >= (arah benar, sama dgn V8 v8e_cp_validity.py). "
            "Ambang p=0.002 literal spek = p minimal attainable (1/501=0.001996); "
            "dilaporkan DUA ambang: p<=0.05 (V8) dan p<=0.002 (literal)."),
        "validity_test_t_cp": {
            "rule_prereg": "t_cp di detik awal (<5 jendela) di >50% run = artefak "
                           "termal -> sub-klaim gugur",
            "n_runs": n_runs, "n_early_5s": n_early,
            "frac_early": round(n_early / n_runs, 3),
            "frac_early_R01": round(float(r01.early_5s.mean()), 3),
            "frac_early_R02": round(float(r02.early_5s.mean()), 3),
            "verdict": ("SUB-KLAIM GUGUR (artefak termal)" if n_early / n_runs > 0.5
                        else "t_cp TIDAK dominan awal -> lanjut dinilai"),
        },
        "run_level_sig_p05_v8": {
            **run_level("sig_p05_v8"),
            "frac_sig_R01": round(float(r01.sig_p05_v8.mean()), 3),
            "frac_sig_R02": round(float(r02.sig_p05_v8.mean()), 3),
            "interpretasi": "precision run-level = spesifisitas keausan; R01 = alat "
                            "BARU (negatif) -> FP di R01 = alarm pada alat baru",
        },
        "run_level_sig_p002_literal": {
            **run_level("sig_p002_literal"),
            "frac_sig_R01": round(float(r01.sig_p002_literal.mean()), 3),
            "frac_sig_R02": round(float(r02.sig_p002_literal.mean()), 3),
        },
        "TLead_to_end_R02_s": {
            "values": [int(x) for x in r.loc[r.run == "R02", "t_lead_s"]],
            "median": float(r.loc[r.run == "R02", "t_lead_s"].median()),
            "min": int(r.loc[r.run == "R02", "t_lead_s"].min()),
            "anchor": "alat TUMPUL di akhir R02 (deskripsi Mendeley)",
        },
        "cross_family_spread_s": {
            "median": float(r.fam_spread_s.median()),
            "range": [int(r.fam_spread_s.min()), int(r.fam_spread_s.max())],
        },
        "underpowered": n_runs < 30,
        "runs": r.to_dict(orient="records"),
    }

    # ---------- BAGIAN B: kalibrasi within-tool ----------
    cal_rows = []
    for tool, g in df.groupby("tool"):
        r01 = g[g.run == "R01"].sort_values("start_sample").reset_index(drop=True)
        r02 = g[g.run == "R02"].sort_values("start_sample").reset_index(drop=True)
        ncal = max(5, int(np.ceil(CAL_FRAC * len(r01))))
        cal, ev1 = r01.iloc[:ncal], r01.iloc[ncal:]
        med = cal[feats].median()
        mad = (cal[feats] - med).abs().median() * 1.4826
        mad = mad.replace(0, np.nan)

        def n_over(ev):
            Z = ((ev[feats] - med) / mad).abs()
            return (Z > Z_THR).sum(axis=1).to_numpy()

        n1, n2 = n_over(ev1), n_over(r02)
        a1, a2 = n1 >= N_FEAT_ALARM, n2 >= N_FEAT_ALARM
        # baseline rule 3-RMS, kalibrasi sama
        Zr1 = ((ev1[rms3] - med[rms3]) / mad[rms3]).abs()
        Zr2 = ((r02[rms3] - med[rms3]) / mad[rms3]).abs()
        rule1 = (Zr1 > Z_THR).any(axis=1).to_numpy()
        rule2 = (Zr2 > Z_THR).any(axis=1).to_numpy()
        fp = int(a1.sum()); neg_min = len(ev1) / 60.0
        first = int(np.argmax(a2)) if a2.any() else None
        t_lead = float(len(r02) - first) if first is not None else None
        rule_fp = int(rule1.sum())
        cal_rows.append({
            "tool": tool, "n_cal": int(ncal), "n_eval_R01": int(len(ev1)),
            "n_R02": int(len(r02)),
            "engine_5of27": {
                "fp_R01": fp,
                "far_fp_per_min_R01": round(fp / neg_min, 3) if neg_min else None,
                "pct_R01_alarmed": round(100 * fp / max(len(ev1), 1), 1),
                "detected_R02": bool(a2.any()),
                "pct_R02_alarmed": round(100 * float(a2.mean()), 1),
                "first_alarm_s_in_R02": first,
                "TLead_to_end_R02_s": t_lead,
            },
            "baseline_rule_3RMS": {
                "fp_R01": rule_fp,
                "detected_R02": bool(rule2.any()),
                "pct_R02_alarmed": round(100 * float(rule2.mean()), 1),
            },
            "kurangi_ragu_vs_rule": (round(1 - fp / rule_fp, 3)
                                      if rule_fp else None),
            "frac_feat_over3sig": {
                "R01_eval_mean": round(float(n1.mean() / len(feats)), 3),
                "R02_mean": round(float(n2.mean() / len(feats)), 3)},
        })
        e = cal_rows[-1]
        log(f"  [cal {tool}] FP_R01={fp}/{len(ev1)} detR02={e['engine_5of27']['detected_R02']} "
            f"TLead={t_lead}s ruleFP={rule_fp} kurangi_ragu={e['kurangi_ragu_vs_rule']}")

    # ---------- C) titik operasi FAR-terkalibrasi (E1 statistik) ----------
    op_rows = []
    for target in (1.0, 0.2):
        for tool, g in df.groupby("tool"):
            r01 = g[g.run == "R01"].sort_values("start_sample").reset_index(drop=True)
            r02 = g[g.run == "R02"].sort_values("start_sample").reset_index(drop=True)
            ncal = max(5, int(np.ceil(CAL_FRAC * len(r01))))
            cal = r01.iloc[:ncal]
            med = cal[feats].median()
            mad = (cal[feats] - med).abs().median() * 1.4826
            mad = mad.replace(0, np.nan)

            def sc(ev):
                Z = ((ev[feats] - med) / mad).abs()
                return (Z > Z_THR).sum(axis=1).to_numpy()

            ev1 = r01.iloc[ncal:]
            s1, s2 = sc(ev1), sc(r02)
            q = 1.0 - target * (len(ev1) / 60.0) / max(len(ev1), 1)
            q = min(max(q, 0.5), 1.0)
            thr = float(np.quantile(s1, q)) if len(s1) else None
            z1 = (s1 >= thr) if thr is not None else np.zeros(0, bool)
            z2 = (s2 >= thr) if thr is not None else np.zeros(0, bool)
            first = int(np.argmax(z2)) if z2.any() else None
            op_rows.append({
                "target_fp_per_min": target, "tool": tool,
                "thr_featcount": thr, "fp_R01": int(z1.sum()),
                "det_R02": bool(z2.any()),
                "first_alarm_s": first,
                "TLead_s": (float(len(r02) - first) if first is not None else None),
                "pct_R02_alarmed": round(100 * float(z2.mean()), 1) if len(z2) else None,
            })
            rr = op_rows[-1]
            log(f"  [op t={target} {tool}] thr={thr} fpR01={rr['fp_R01']} "
                f"det={rr['det_R02']} TLead={rr['TLead_s']}s")

    # ---------- D) AUPRC ranking jendela vs identity-majority ----------
    sc_all, y_all = [], []
    for tool, g in df.groupby("tool"):
        r01 = g[g.run == "R01"].sort_values("start_sample").reset_index(drop=True)
        r02 = g[g.run == "R02"].sort_values("start_sample").reset_index(drop=True)
        ncal = max(5, int(np.ceil(CAL_FRAC * len(r01))))
        cal = r01.iloc[:ncal]
        med = cal[feats].median()
        mad = (cal[feats] - med).abs().median() * 1.4826
        mad = mad.replace(0, np.nan)
        for ev in (r01, r02):
            Z = ((ev[feats] - med) / mad).abs()
            sc_all.append((Z > Z_THR).sum(axis=1).to_numpy().astype(float))
            y_all.append(ev["y"].to_numpy().astype(int))
    s_pool = np.concatenate(sc_all)
    y_pool = np.concatenate(y_all)
    prev = float(y_pool.mean())
    auprc = float(average_precision_score(y_pool, s_pool))
    # baseline identity-majority: skor konstan = prev -> AUPRC = prev
    part_d = {
        "auprc_engine_5of27_score": round(auprc, 4),
        "prev_identity_run": round(prev, 4),
        "lift": round(auprc / prev, 3) if prev else None,
        "lift_ceiling_1_over_prev": round(1 / prev, 3) if prev else None,
        "dB_vs_identity_majority": round(auprc - prev, 4),
        "baseline_identity_majority": "skor konstan -> AUPRC = prev (analitik)",
        "baseline_persistence": "N/A — label konstan dalam run; DINYATAKAN "
                                "(R1 §3.7), bukan dihilangkan diam-diam",
        "n_windows": int(len(y_pool)), "n_pos": int(y_pool.sum()),
        "underpowered": bool(y_pool.sum() < 30 or (len(y_pool) - y_pool.sum()) < 30),
    }

    det_b = [c["engine_5of27"]["detected_R02"] for c in cal_rows]
    leads_b = [c["engine_5of27"]["TLead_to_end_R02_s"] for c in cal_rows
               if c["engine_5of27"]["TLead_to_end_R02_s"] is not None]
    summary = {
        "n_runs": n_runs, "cp_sig_p05": int(r.sig_p05_v8.sum()),
        "cp_sig_p002": int(r.sig_p002_literal.sum()),
        "calibration_det_R02": f"{sum(det_b)}/{len(det_b)}",
        "TLead_median_s_cal": float(np.median(leads_b)) if leads_b else None,
        "auprc_engine": part_d["auprc_engine_5of27_score"],
        "lift": part_d["lift"], "lift_ceiling": part_d["lift_ceiling_1_over_prev"],
        "elapsed_s": round(time.time() - t0, 1),
    }
    out = {"engine": "tool_wear_Ki",
           "claim_task": "deteksi perubahan-regime dalam-run (bengkel, detik)",
           "jenis_engine": "statistical (change-point SSE+permutation; "
                           "kalibrasi median/MAD within-tool)",
           "seed": SEED, "n_perm": N_PERM,
           "part_A_change_point": part_a,
           "part_B_within_tool_calibration": {
               "ambang": "alarm jika >=5/27 fitur |z|>3 (median+MAD 30% awal R01)",
               "per_tool": cal_rows,
               "aggregate": {
                   "n_tools": len(cal_rows),
                   "n_detected_R02": int(sum(det_b)),
                   "B1_pct_detected_before_end_R02": round(
                       100 * sum(det_b) / len(cal_rows), 1),
                   "TLead_median_s": float(np.median(leads_b)) if leads_b else None,
                   "TLead_range_s": [min(leads_b), max(leads_b)] if leads_b else None,
                   "far_fp_per_min_R01_range": [
                       min(c["engine_5of27"]["far_fp_per_min_R01"] for c in cal_rows),
                       max(c["engine_5of27"]["far_fp_per_min_R01"] for c in cal_rows)],
                   "rule_detected_all_R02": all(
                       c["baseline_rule_3RMS"]["detected_R02"] for c in cal_rows),
                   "kurangi_ragu_range": [
                       min(c["kurangi_ragu_vs_rule"] for c in cal_rows
                           if c["kurangi_ragu_vs_rule"] is not None),
                       max(c["kurangi_ragu_vs_rule"] for c in cal_rows
                           if c["kurangi_ragu_vs_rule"] is not None)],
               },
           },
           "part_C_operating_far_calibrated": op_rows,
           "part_D_ranking_auprc": part_d,
           "summary": summary}
    json.dump(out, open(f"{OUT}/v9_e_stat_03_tool_wear_RESULTS.json", "w"),
              indent=1, default=str)
    open(LOGP, "w").write("\n".join(log_lines) + "\n")
    log("SUMMARY: " + json.dumps(summary, default=str))
    log(f"DONE -> {OUT}/v9_e_stat_03_tool_wear_RESULTS.json")


if __name__ == "__main__":
    main()
