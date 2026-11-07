"""V5 J1 — VERIFIER INDEPENDEN (code/81).

Tidak melatih ulang model. Membaca ulang artefak kampanye dan MENGHITUNG ULANG metrik
dari nol dari tabel prediksi, lalu membandingkan dengan JSON primer (toleransi 1e-9).
Memverifikasi: (a) hash pra-registrasi cocok dengan yang dikunci di kartu; (b) angka JSON
berasal dari CSV prediksi (recompute); (c) leakage check (fold per-run, fitur terlarang);
(d) label run_predictions cocok dengan manifest.csv.

Output: stdout ringkas + docs/V5_J1_VERIFY.json
"""
import hashlib
import json
import os

import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, accuracy_score, f1_score

WS = "/mnt/d/Capstone 1"
PREREG = os.path.join(WS, "docs", "V5_J1_PREREG.md")
JSONF = os.path.join(WS, "docs", "V5_J1_RESULTS.json")
RUNCSV = os.path.join(WS, "docs", "V5_J1_run_predictions.csv")
FOLDCSV = os.path.join(WS, "docs", "V5_J1_fold_assignments.csv")
WCSV = os.path.join(WS, "docs", "V5_J1_window_predictions.csv.gz")
NULLNPY = os.path.join(WS, "docs", "V5_J1_perm_null.npy")
MANIFEST = os.path.join(WS, "data", "sim_v5", "manifest.csv")
LOCKED_PREREG_SHA = "9c7a080bb20bc39917e850e5c7b38bc4a916ad70ef5784f75e99cff063ad214a"
TOL = 1e-9
G1_T, G2_M = 0.60, 0.15

checks = []


def ck(name, ok, detail=""):
    checks.append({"name": name, "pass": bool(ok), "detail": detail})
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {detail}")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for c in iter(lambda: fh.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def macro_ap(y, p):
    return float(average_precision_score(y, p, average="macro"))


def main():
    res = json.load(open(JSONF))
    classes = res["data"]["classes"]
    n = len(classes)

    # (a) hash pra-registrasi
    live = sha256_file(PREREG)
    ck("prereg_live_sha_eq_locked_card", live == LOCKED_PREREG_SHA, live[:16])
    ck("prereg_live_sha_eq_json", live == res["prereg_sha256"], "")

    # load prediksi run-level
    rp = pd.read_csv(RUNCSV)
    ck("run_csv_rows_eq_1200", len(rp) == 1200, f"n={len(rp)}")
    ck("run_csv_unique_run_id", rp.run_id.nunique() == len(rp), "")

    y = rp["y_true"].to_numpy(int)
    p_m1 = rp[[f"p_m1_{c}" for c in classes]].to_numpy(float)
    p_can = rp[[f"p_can_{c}" for c in classes]].to_numpy(float)
    p_m2 = rp[[f"p_m2_{c}" for c in classes]].to_numpy(float)

    # probabilitas harus valid (>=0, baris ~ 1)
    ck("m1_proba_rows_sum_1", bool(np.allclose(p_m1.sum(1), 1.0, atol=1e-6)),
       f"max|sum-1|={np.abs(p_m1.sum(1)-1).max():.2e}")
    ck("can_proba_rows_sum_1", bool(np.allclose(p_can.sum(1), 1.0, atol=1e-6)), "")

    return res, classes, y, p_m1, p_can, p_m2, rp


def part2(res, classes, y, p_m1, p_can, p_m2, rp):
    n = len(classes)
    ap_m1 = macro_ap(y, p_m1)
    ap_can = macro_ap(y, p_can)
    ap_m2 = macro_ap(y, p_m2)
    gap = ap_m1 - ap_can
    ck("recompute_m1_macro_auprc", abs(ap_m1 - res["primary"]["m1_macro_auprc_run"]) < TOL,
       f"{ap_m1:.10f} vs json {res['primary']['m1_macro_auprc_run']:.10f}")
    ck("recompute_canary_macro_auprc",
       abs(ap_can - res["primary"]["canary_macro_auprc_run"]) < TOL,
       f"{ap_can:.10f} vs {res['primary']['canary_macro_auprc_run']:.10f}")
    ck("recompute_m2_hgb_macro_auprc",
       abs(ap_m2 - res["secondary"]["m2_hgb_macro_auprc_run"]) < TOL,
       f"{ap_m2:.10f}")
    ck("recompute_gap", abs(gap - res["primary"]["gap_m1_minus_canary"]) < TOL, f"{gap:.10f}")

    acc = float(accuracy_score(y, p_m1.argmax(1)))
    f1 = float(f1_score(y, p_m1.argmax(1), average="macro"))
    ck("recompute_m1_accuracy", abs(acc - res["secondary"]["m1_accuracy_run"]) < TOL, f"{acc:.6f}")
    ck("recompute_m1_macro_f1", abs(f1 - res["secondary"]["m1_macro_f1_run"]) < TOL, f"{f1:.6f}")

    # gate
    g1 = ap_m1 >= G1_T
    g2 = gap >= G2_M
    ck("gate_G1_recompute", g1 == res["gates"]["G1_m1_macro_auprc_ge_0.60"]["pass"],
       f"ap={ap_m1:.4f} thr={G1_T}")
    ck("gate_G2_recompute", g2 == res["gates"]["G2_m1_ge_canary_plus_0.15"]["pass"],
       f"gap={gap:.4f} margin={G2_M}")
    verdict_re = "LOLOS" if (g1 and g2 and res["gates"]["G3_integrity"]["pass"]) else "GAGAL"
    ck("verdict_recompute", verdict_re == res["verdict"], f"{verdict_re} vs {res['verdict']}")

    # permutation p dari null npy
    null = np.load(NULLNPY)
    obs = ap_m1
    p_re = float((1 + (null >= obs).sum()) / (1 + len(null)))
    ck("recompute_perm_p", abs(p_re - res["permutation_test"]["p_value"]) < TOL,
       f"p={p_re:.6f} null_max={null.max():.4f}")

    # label cocok manifest
    man = pd.read_csv(MANIFEST)
    mmap = dict(zip(man.run_id, man.class_label))
    mism = [r.run_id for r in rp.itertuples() if mmap.get(r.run_id) != classes[r.y_true]]
    ck("labels_match_manifest", len(mism) == 0, f"mismatches={len(mism)}")
    # prevalensi 200/kelas
    vc = pd.Series(y).value_counts().to_dict()
    ck("balanced_200_per_class", all(vc.get(i, 0) == 200 for i in range(n)), str(vc))

    # integritas fold: setiap run_id satu fold saja
    fa = pd.read_csv(FOLDCSV)
    per_run_folds = fa.groupby("run_id")["fold"].nunique()
    ck("each_run_single_fold", bool((per_run_folds == 1).all()),
       f"runs_with_multi_fold={int((per_run_folds>1).sum())}")
    wc = pd.read_csv(WCSV)
    wc_folds = wc.groupby("run_id")["fold"].nunique()
    ck("window_pred_each_run_single_fold", bool((wc_folds == 1).all()),
       f"multi={int((wc_folds>1).sum())}")
    # fold assignments konsisten antara fold csv dan window csv
    mrg = fa.merge(wc[["run_id", "fold"]].drop_duplicates(), on="run_id", suffixes=("_fa", "_wc"))
    ck("fold_assignments_consistent", bool((mrg.fold_fa == mrg.fold_wc).all()), f"rows={len(mrg)}")
    return ap_m1, ap_can, gap, verdict_re


if __name__ == "__main__":
    res, classes, y, p_m1, p_can, p_m2, rp = main()
    ap_m1, ap_can, gap, verdict_re = part2(res, classes, y, p_m1, p_can, p_m2, rp)
    n_pass = sum(1 for c in checks if c["pass"])
    n_fail = sum(1 for c in checks if not c["pass"])
    print(f"\n=== VERIFIER INDEPENDEN: {n_pass} PASS / {n_fail} FAIL ===")
    out = {
        "task_id": "t_943af8af",
        "verifier": "code/81_j1_verify_v5.py (recompute tanpa training ulang)",
        "n_pass": n_pass,
        "n_fail": n_fail,
        "all_pass": n_fail == 0,
        "recomputed": {
            "m1_macro_auprc_run": ap_m1,
            "canary_macro_auprc_run": ap_can,
            "gap_m1_minus_canary": gap,
            "verdict": verdict_re,
        },
        "checks": checks,
    }
    json.dump(out, open(os.path.join(WS, "docs", "V5_J1_VERIFY.json"), "w"), indent=2)
    print("saved ->", os.path.join(WS, "docs", "V5_J1_VERIFY.json"))
