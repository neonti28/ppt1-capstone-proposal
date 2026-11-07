#!/usr/bin/env python3
"""V9-EVAL_B 03 — gabung A+B: hitung B3, tabel joint B3xB4, VERIFIKASI mandiri.

Input : scratch/v9_eval_b/_A_json.json (B1/B2/B3 inputs, skrip 01)
        scratch/v9_eval_b/_B_b4.json    (B4 + identitas RF, skrip 02)
Output: scratch/v9_eval_b/v9_eval_b_RESULTS.json (PRIMER) + v9_eval_b_SUMMARY.txt
        + v9_eval_b_VERIFY.txt

Verifikasi (verification-mandatory):
  V1  B3 dihitung ULANG dari FP sumber E_RULE (re-sum mentah) == tersimpan
  V2  B1 stuck RF diekstrak ULANG dari JSON E_ML == tersimpan skrip 01
  V3  B4 persistence vib dihitung ulang dgn implementasi BERBEDA (pandas shift)
      == hasil skrip 02 (margin list + coverage)
  V4  identitas retrain RF (AUPRC + TP/FP per tau) dari skrip 02
  V5  crosscheck FP prediksi ulang skrip 02 vs E_RULE fold == semua match
  V6  formula B3 direcompute dari FP tersimpan (self-consistency)
"""
import json, os, statistics as stat

S = "/mnt/d/Capstone 1(v2)/scratch"
OUT = f"{S}/v9_eval_b"
SEED42_SOURCES = f"{S}/v9_e_rule/v9_e_RULE_01_status_results.json"

A = json.load(open(f"{OUT}/_A_json.json"))
B = json.load(open(f"{OUT}/_B_b4.json"))

R = {"meta": {
        "task": "V9-EVAL_B — metrik LAPISAN B (B1/B2/B3/B4) 7 engine",
        "kerangka": "operator (Evaluasi User.txt) via V9_PM1_ARCHITECTURE §4.7 + V8_R1_ABC_SPEC §1.3",
        "primer": ["scratch/v9_eval_b/_A_json.json", "scratch/v9_eval_b/_B_b4.json"],
        "units": "FP = jendela 1 menit (rig) kecuali dinyatakan; tool_wear = detik bengkel; TLead = menit",
        "larangan": ["vonis biner LULUS/GAGAL", "anchor dipinjam antar kelas",
                     "B1>=80% dituntut dari kelas status", "menghitung ulang metrik A"],
     },
     "B1_B2_onset": A["onset"],
     "B3": {},
     "B4_status": B["classes"],
     "joint_B3_B4": {},
     "belum_terukur": A["belum"],
     "status_delay_konfirmasi": A["status_delay"],
     "verify": {}}

STATUS = ["vib", "ssi", "shk", "stuck_k1", "hyd_ki"]
TAUS = ["0.05", "0.1", "0.2", "0.3", "0.5"]


def b3(fp_eng, fp_base):
    if not fp_base:
        return None
    return 1.0 - fp_eng / fp_base


def f4(x):
    return None if x is None else round(float(x), 4)


# =============================================================== B3 kelas status
status_fp = A["B3"]["kelas_status_FP"]
ml_fp = A["B3"]["ML_FP_window"]
for cls in STATUS:
    fp_rule = status_fp[cls]["FP_totals"].get("rule_display_t0minus1")
    engs = {}
    for meth, fp in status_fp[cls]["FP_totals"].items():
        engs[meth] = {"FP": fp, "B3_kurangi_ragu_vs_rule": f4(b3(fp, fp_rule))}
    if cls in ml_fp:
        for model in ["rf", "gb", "lr"]:
            for tau in TAUS:
                v = ml_fp[cls][model][tau]
                engs[f"{model}_tau{tau}"] = {
                    "FP": v["FP"], "TP": v["TP"],
                    "B3_kurangi_ragu_vs_rule": f4(b3(v["FP"], fp_rule))}
    note = {
        "vib": "baseline = rule VIBLAT>=32,17405 (status-quo)",
        "ssi": "baseline = rule SSI(CRPM)>=1 (status-quo); n_nodata rule "
               f"{status_fp[cls]['n_nodata_rule_total']} baris",
        "shk": "baseline = rule SHKRSK display (status-quo)",
        "stuck_k1": "baseline = rule display STUCK (status-quo); cakupan E_RULE "
                    f"hanya {status_fp[cls]['n_folds_E_RULE']} fold ({', '.join(status_fp[cls]['test_wells'])})",
        "hyd_ki": "baseline = rule |z|>2 = PEMBENTUK LABEL (tautologi) -> B3 = "
                  "pengurangan BEBAN ALARM relatif tampilan hari-ini, BUKAN keunggulan skill",
    }[cls]
    R["B3"][cls] = {"FP_rule_status_quo": fp_rule, "engines": engs, "catatan": note}

# =============================================================== B3 stuck_k2 onset
r2m = A["onset"]["stuck_k2_RULE"]["metode"]
fp_e1 = r2m["rule_E1_2of3"]["FP_window_total"]
stuck = {"FP_rule_E1_status_quo": fp_e1,
         "satuan": "FP jendela 1 menit (grid onset stuck_k2)",
         "engines": {}}
for meth in ["persistence_horizon", "persistence_event", "rule_E1_2of3"]:
    m = r2m[meth]
    stuck["engines"][meth] = {
        "FP_window": m["FP_window_total"], "FP_alarm": m["FP_alarm_total"],
        "B3_kurangi_ragu_vs_E1": f4(b3(m["FP_window_total"], fp_e1)),
        "hindsight": m.get("hindsight", False)}
e2fp = sum(x["FP_window_q95"] or 0 for x in A["onset"]["stuck_k2_STAT_E2"]["per_fold"])
stuck["engines"]["E2_stats_q95"] = {"FP_window": e2fp,
                                    "B3_kurangi_ragu_vs_E1": f4(b3(e2fp, fp_e1))}
for model in ["rf", "gb", "lr"]:
    for tau in TAUS + ["q95_train"]:
        v = ml_fp["stuck_k2"][model].get(tau)
        if v:
            stuck["engines"][f"{model}_tau{tau}"] = {
                "FP": v["FP"], "TP": v["TP"],
                "B3_kurangi_ragu_vs_E1": f4(b3(v["FP"], fp_e1))}
stuck["catatan"] = ("baseline E1 = aturan fisika 2-dari-3 (pemicu pemeriksaan terdekat utk "
                    "kelas onset; display status-quo TIDAK memprediksi onset -> FP_display onset=0)")
R["B3"]["stuck_k2_onset"] = stuck

# =============================================================== B3 hyd_kii
h4 = A["onset"]["hyd_kii"]
R["B3"]["hyd_kii"] = {
    "B3_kurangi_ragu_vs_rule": None,
    "alasan": "FP rule z-pit pada baris evaluasi = 0 BY CONSTRUCTION (blok episode +30 mnt "
              "dibuang) -> pembagi nol; B3 tidak terdefinisi utk kelas ini",
    "beban_inspeksi": {
        "rule_zpit_episode_minutes_total": h4["rule_zpit_status_quo"]["inspection_load"]["episode_minutes_total"],
        "rule_zpit_episode_minutes_test": h4["rule_zpit_status_quo"]["inspection_load"]["episode_minutes_test"],
        "varian_fisher_FP_window_q95": h4["varian_fisher_pearson_proxy"]["FP_window_q95"],
        "always_negative_FP": h4["always_negative"]["fp"]},
    "catatan": "FAR varian q95 = 31,6/24jam (EVAL_A); pembanding beban = beban rule vs "
               "jumlah alarm varian, bukan rasio B3"}

# =============================================================== B3 tool_wear
tw = A["onset"]["tool_wear"]
R["B3"]["tool_wear"] = {
    "K_i_kalibrasi_mentah_5of27": {
        "kurangi_ragu_vs_rule3RMS_range": tw["K_i"]["kalibrasi5of27_kurangi_ragu_vs_rule3RMS_range"],
        "FAR_range_per_min": tw["K_i"]["kalibrasi5of27_FAR_range_per_min"]},
    "K_i_FAR_terkalibrasi": tw["K_i"]["B3_FAR_terkalibrasi_per_tool"],
    "K_ii": "V9 tanpa head RF/FP engine (ranking only; RF = angka V8 ref) -> B3 K-ii belum terukur V9",
    "satuan": "FP = alarm per run bengkel (detik 1 Hz)"}

# =============================================================== B3 bit_wear
R["B3"]["bit_wear"] = {
    "K_1": "BELUM TERUKUR — E_RULE/E_STAT tidak menghitung TP/FP utk kelas ini (EVAL_A §2.6)",
    "K_2": "BELUM TERUKUR — pra-reg K-2 belum terbit (E_RULE DoD-d); bukan gagal"}

# ================================================= joint B3 x B4 (kelas status)
for cls in STATUS:
    rows = []
    b4c = B["classes"][cls]
    fp_rule = R["B3"][cls]["FP_rule_status_quo"]
    for eng in ["persistence", "rule_display_t0minus1", "hybrid_rule_and_persistence",
                "rule_E1_2of3"]:
        if eng in b4c["engines"]:
            e = b4c["engines"][eng]["L10"]
            fp = status_fp[cls]["FP_totals"].get(eng)
            rows.append({
                "engine": eng, "FP": fp,
                "B3_vs_rule": f4(b3(fp, fp_rule)),
                "B4_median_margin_mnt": e["B4_median_margin_mnt"],
                "B4_IQR": e["B4_IQR_margin_mnt"],
                "B4_coverage": f4(e["B4_coverage"]),
                "konfirmasi_delay_median_mnt": e["konfirmasi_delay_median_mnt"],
                "n_blocks_sustained": e["n_blocks_sustained_ge5mnt"],
                "n_alarms": e["n_alarms"],
            })
    if b4c.get("rf_retrain"):
        pooled = b4c["rf_retrain"]["b4_pooled_per_tau"]
        for tau in TAUS:
            e = pooled[tau]["L10"]
            fp = ml_fp[cls]["rf"][tau]["FP"]
            rows.append({
                "engine": f"rf_tau{tau}", "FP": fp,
                "B3_vs_rule": f4(b3(fp, fp_rule)),
                "B4_median_margin_mnt": e["B4_median_margin_mnt"],
                "B4_IQR": e["B4_IQR_margin_mnt"],
                "B4_coverage": f4(e["B4_coverage"]),
                "konfirmasi_delay_median_mnt": None,
                "n_blocks_sustained": e["n_blocks_sustained_ge5mnt"],
                "n_alarms": e["n_alarms"],
            })
    R["joint_B3_B4"][cls] = {
        "FP_rule_status_quo": fp_rule,
        "blocks": b4c["blocks"],
        "rows": rows,
        "catatan": "margin = menit alarm terdekat SEBELUM entry blok (L=10); "
                   "coverage = fraksi blok berkelanjutan dgn alarm di lookback"}

# =================================================================== VERIFIKASI
V = []

# V1 — re-sum FP langsung dari JSON sumber E_RULE, banding dg B3 tersimpan
r1 = json.load(open(SEED42_SOURCES))
v1_ok, v1_n = 0, 0
for cls in STATUS:
    folds = r1["classes"][cls]["folds"]
    for meth in ["persistence", "rule_display_t0minus1", "hybrid_rule_and_persistence",
                 "rule_E1_2of3", "hybrid_E1_and_persistence"]:
        vals = [f.get(meth, {}).get("fp") for f in folds if meth in f]
        if not vals:
            continue
        fp_src = sum(vals)
        stored = R["B3"][cls]["engines"].get(meth, {}).get("FP")
        v1_n += 1
        v1_ok += int(stored == fp_src)
        if stored != fp_src:
            V.append(f"V1 MISMATCH {cls}.{meth}: stored={stored} source={fp_src}")
V.append(f"V1 FP E_RULE re-sum == tersimpan: {v1_ok}/{v1_n}")

# V1b — B3 stuck_k2 FP E1 re-sum
fp_e1_src = 0
r2 = json.load(open(f"{S}/v9_e_rule/v9_e_RULE_02_stuck_onset_results.json"))
for f in r2["folds"]:
    fp_e1_src += f["rule_E1_2of3"]["fp"]
v1b = fp_e1_src == stuck["FP_rule_E1_status_quo"]
V.append(f"V1b FP E1 onset re-sum ({fp_e1_src}) == tersimpan ({stuck['FP_rule_E1_status_quo']}): {v1b}")

# V2 — B1 stuck RF tau0.05 diekstrak ulang dari JSON E_ML
ml = json.load(open(f"{S}/v9_e_ml/v9_e_ML_stuck_k2_RESULTS.json"))
b1_src = [f["models"]["rf"]["onset_by_tau"]["0.05"]["B1_coverage"] for f in ml["folds"]]
b1_stored = A["onset"]["stuck_k2_ML"]["models"]["rf"]["0.05"]["B1_coverage"]["values"]
v2 = b1_src == b1_stored
V.append(f"V2 B1 stuck RF tau0.05 re-extract == tersimpan: {v2} ({b1_stored} vs {b1_src})")

# V3 — B4 persistence vib, implementasi BERBEDA (index-based, spesifikasi sama:
#      blok diputus bila jeda ts > 2 mnt; alarm = transisi y_prev 0->1 per well;
#      margin = entry - alarm terdekat dalam [te-10, te))
import numpy as np
import pandas as pd
df = pd.read_csv(f"{S}/v9_d1/datasets/vib.csv.gz").sort_values(["well", "ts_bin"])
margins_ref = B["classes"]["vib"]["engines"]["persistence"]["L10"]["margins_mnt"]
margins_alt, blocks_alt = [], 0
for w, sub in df.groupby("well", sort=False):
    ts = sub["ts_bin"].to_numpy().astype("int64")
    y = sub["y_vib"].to_numpy().astype(int)
    yp = sub["y_prev_vib"].fillna(0).to_numpy().astype(int)
    # alarm: transisi 0->1 y_prev (skip indeks 0 tiap well)
    a_idx = [i for i in range(1, len(yp)) if yp[i] == 1 and yp[i - 1] == 0]
    a_ts = ts[a_idx]
    # blok: mulai y=1 setelah y=0 / gap > 2 mnt; berakhir saat y=0 / gap > 2 mnt
    n = len(y)
    i = 0
    while i < n:
        if y[i] == 1:
            s = i
            j = i
            while (j + 1 < n and y[j + 1] == 1 and (ts[j + 1] - ts[j]) <= 2):
                j += 1
            if ts[j] - ts[s] >= 5:
                blocks_alt += 1
                pre = [t for t in a_ts if ts[s] - 10 <= t < ts[s]]
                if pre:
                    margins_alt.append(int(ts[s] - max(pre)))
            i = j + 1
        else:
            i += 1
v3 = (sorted(margins_alt) == sorted(margins_ref))
V.append(f"V3 B4(vib persistence) recompute alternatif (index-based, spesifikasi sama) "
         f"== skrip02: {v3} (n_alt={len(margins_alt)} n_ref={len(margins_ref)}; "
         f"blocks_alt={blocks_alt})")

# V4 — identitas retrain RF
v4_lines = []
v4_all = True
for cls in ["vib", "ssi", "shk"]:
    rf = B["classes"][cls]["rf_retrain"]["verifikasi"]
    v4_lines.append(f"V4 {cls}: AUPRC {rf['auprc_match']}, TP/FP {rf['tau_fp_tp_match']}")
    v4_all &= rf["auprc_match"].split("/")[0] == rf["auprc_match"].split("/")[1]
    v4_all &= rf["tau_fp_tp_match"].split("/")[0] == rf["tau_fp_tp_match"].split("/")[1]
V += v4_lines
V.append(f"V4 identitas RF keseluruhan: {'SEMUA MATCH' if v4_all else 'ADA MISMATCH'}")

# V5 — crosscheck FP prediksi ulang (skrip 02) vs fold E_RULE
v5_n = v5_ok = 0
for cls in STATUS:
    for k, x in B["classes"][cls]["crosscheck_fp_vs_E_RULE"].items():
        v5_n += 1
        v5_ok += int(x["match"])
        if not x["match"]:
            V.append(f"V5 MISMATCH {cls}.{k}: {x}")
V.append(f"V5 FP(prediksi ulang) == FP fold E_RULE: {v5_ok}/{v5_n}")

# V6 — recompute formula B3 dari FP tersimpan
v6_n = v6_ok = 0
for cls in STATUS:
    fp_rule = R["B3"][cls]["FP_rule_status_quo"]
    for eng, d in R["B3"][cls]["engines"].items():
        want = f4(b3(d["FP"], fp_rule))
        v6_n += 1
        v6_ok += int(want == d["B3_kurangi_ragu_vs_rule"])
V.append(f"V6 formula B3 self-consistency: {v6_ok}/{v6_n}")

R["verify"] = {"checks": V, "V1": f"{v1_ok}/{v1_n}", "V1b": v1b, "V2": v2,
               "V3": v3, "V4": v4_all, "V5": f"{v5_ok}/{v5_n}", "V6": f"{v6_ok}/{v6_n}"}

json.dump(R, open(f"{OUT}/v9_eval_b_RESULTS.json", "w"), indent=1, allow_nan=False)
open(f"{OUT}/v9_eval_b_VERIFY.txt", "w").write("\n".join(V) + "\n")

# -------------------------------------------------------------------- SUMMARY
L = []
L.append("=== V9-EVAL_B SUMMARY ===")
L.append("\n-- B3 kelas status (vs FP rule status-quo) --")
for cls in STATUS:
    e = R["B3"][cls]
    L.append(f"{cls} (FP_rule={e['FP_rule_status_quo']}):")
    for k, d in e["engines"].items():
        L.append(f"   {k}: FP={d['FP']} B3={d['B3_kurangi_ragu_vs_rule']}")
L.append("\n-- B3 stuck_k2 onset (vs E1 FP=%d) --" % fp_e1)
for k, d in stuck["engines"].items():
    L.append(f"   {k}: FP={d.get('FP', d.get('FP_window'))} B3={d['B3_kurangi_ragu_vs_E1']}")
L.append("\n-- joint B3 x B4 (L10) --")
for cls in STATUS:
    L.append(f"{cls}: blocks={B['classes'][cls]['blocks']}")
    for r in R["joint_B3_B4"][cls]["rows"]:
        L.append(f"   {r['engine']}: FP={r['FP']} B3={r['B3_vs_rule']} "
                 f"B4med={r['B4_median_margin_mnt']} cov={r['B4_coverage']} "
                 f"konf={r['konfirmasi_delay_median_mnt']} nblk={r['n_blocks_sustained']}")
L.append("\n-- verify --")
L += V
open(f"{OUT}/v9_eval_b_SUMMARY.txt", "w").write("\n".join(L) + "\n")
print("\n".join(L))
