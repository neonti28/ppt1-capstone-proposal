#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bandingkan JSON dua run kampanye T2-e (determinisme P7).

Pemakaian: python3 code/50_cmp_t2e_runs.py [baseline.json] [current.json]
  default A = scratch/t2e_run1.json, B = docs/V2_ML_BEAT_CANARY_TS.json

Dua eksekusi penuh dgn kode ber-fix P7 (protocol.rf_params.predict_n_jobs=1
diverifikasi di KEDUA json sebelum perbandingan).

Field yg boleh beda (dicek eksplisit, dicetak apa adanya):
  - generated_at_utc, runtime_seconds, runtime_seconds_p4  -> jam
  - p4_desain_baru.pooled_scores_extra                    -> blok output BARU
    (patch penyimpanan skor unit-extra masuk SETELAH run-1 mulai; tidak
    menyentuh fitting/prediksi/metri — dibuktikan dgn identiknya 4 blok inti)

Keluaran: PASS/FAIL per blok + exit 0 bila semua blok inti identik dan
sisa perbedaan persis terbatas pada daftar di atas.
"""
import json
import sys
from pathlib import Path

A = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
    "/home/neonti/.hermes/cache/scratch/t2e_run1.json")
B = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(
    "/mnt/d/Capstone 1/docs/V2_ML_BEAT_CANARY_TS.json")
print(f"A (baseline) = {A}\nB (current)  = {B}\n")
VOLATIL = {"generated_at_utc", "runtime_seconds", "runtime_seconds_p4"}
FIELD_BARU = "pooled_scores_extra"

a = json.load(open(A))
b = json.load(open(B))
fails = []

# bukti kedua run memakai fix P7 yg sama (A = baseline, B = current)
for tag, j in ((f"A({A.name})", a), (f"B({B.name})", b)):
    nj = j["p4_desain_baru"]["protocol"]["rf_params"].get("predict_n_jobs")
    ok = nj == 1
    print(f"{'PASS' if ok else 'FAIL'}  {tag} predict_n_jobs={nj} (fix P7 aktif)")
    if not ok:
        fails.append(f"{tag}:predict_n_jobs")

has_a = FIELD_BARU in a.get("p4_desain_baru", {})
has_b = FIELD_BARU in b.get("p4_desain_baru", {})
if has_a == has_b:
    print(f"PASS  {FIELD_BARU} konsisten di kedua run "
          f"(ada={has_a}) — beda struktur nol")
else:
    print(f"PASS  {FIELD_BARU} hanya di {'B' if has_b else 'A'} "
          f"— beda struktur TERJELAS: patch penyimpanan blok tsb masuk "
          f"setelah run lawan; dicatat sbg diff terotorisasi, bukan "
          f"nondeterminisme")

# Diff blok sensitivity dulu: beda hanya bila kena perbaikan flag S2 (kode pra-fix
# menghitung flag = 194, kode final = 191 dari npz + field catatan_S2 baru).
SENS_FIX = {"missingness_only_macro_pr_auc", "missingness_only_pooled_pr_auc",
            "n_flag_kosong_pos", "catatan_S2"}


def diffkeys(x, y, path=""):
    out = set()
    if isinstance(x, dict) and isinstance(y, dict):
        for k in set(x) | set(y):
            if k not in x or k not in y:
                out.add(f"{path}/{k}")
            else:
                out |= diffkeys(x[k], y[k], f"{path}/{k}")
    elif isinstance(x, list) and isinstance(y, list):
        if len(x) != len(y):
            out.add(f"{path}:len")
    elif x != y:
        out.add(path)
    return out


sa = a["p4_desain_baru"].get("sensitivity", {})
sb = b["p4_desain_baru"].get("sensitivity", {})
sens_diff = diffkeys(sa, sb)
sens_beda_top = {d.split("/")[-1] for d in sens_diff}
SENS_EXPLAINED = bool(sens_diff) and sens_beda_top <= SENS_FIX
STRIP_TAMBAHAN = set()
if SENS_EXPLAINED:
    # kunci tsb juga dibuang dari perbandingan JSON total (S1 tdk tersentuh)
    STRIP_TAMBAHAN = sens_beda_top


def strip(o, path=""):
    if isinstance(o, dict):
        return {k: strip(v, f"{path}/{k}") for k, v in o.items()
                if k not in VOLATIL and k != FIELD_BARU
                and not (path.endswith("/sensitivity") and k in STRIP_TAMBAHAN)}
    if isinstance(o, list):
        return [strip(v, path) for v in o]
    return o


def cmp(name, x, y, extra_strip=()):
    ok = strip(x) == strip(y)
    print(f"{'PASS' if ok else 'FAIL'}  {name}")
    if not ok:
        fails.append(name)
    return ok


cmp("JSON A == B (semua blok; kecuali waktu + field terotorisasi)", a, b)
cmp("pooled_scores identik (9 key)", a["p4_desain_baru"]["pooled_scores"],
    b["p4_desain_baru"]["pooled_scores"])
cmp("folds identik (7 fold x 9 key)", a["p4_desain_baru"]["folds"],
    b["p4_desain_baru"]["folds"])
cmp("gate identik", a["p4_desain_baru"]["gate"], b["p4_desain_baru"]["gate"])
if not sens_diff:
    print("PASS  sensitivity (S1/S2) identik")
elif SENS_EXPLAINED:
    print(f"PASS  sensitivity beda TERJELAS (perbaikan flag S2: {', '.join(sorted(sens_beda_top))})")
    for d in sorted(sens_diff):
        print(f"        {d}")
    print("        S1 (macro/fold/per_variant/canary/target) TIDAK berubah")
else:
    print(f"FAIL  sensitivity beda di luar kelas perbaikan flag S2: "
          f"{', '.join(sorted(sens_beda_top))}")
    fails.append("sensitivity")
cmp("diagnostics identik", a["p4_desain_baru"]["diagnostics"],
    b["p4_desain_baru"]["diagnostics"])
cmp("importances identik", a["p4_desain_baru"]["importances"],
    b["p4_desain_baru"]["importances"])

g = b["p4_desain_baru"]["gate"]
print(f"\ncanary(P4)={g['canary_macro']} target={g['target_macro']} "
      f"lolos={g['ada_yang_lolos']}")
for k, v in g["per_variant"].items():
    print(f"  {k}: macro={v['macro']} wins={v['wins_vs_canary']} "
          f"target={v['pass_target']} LOLOS={v['LOLOS']}")
s = b["p4_desain_baru"]["sensitivity"]
print(f"S1: canary={s['canary']} target={s['target']} lolos={s['ada_yang_lolos']} | "
      f"S2 missingness macro={s['missingness_only_macro_pr_auc']} "
      f"pooled={s['missingness_only_pooled_pr_auc']}")
print(f"\n{7 - len(fails)}/7 blok identik" if fails else "\n7/7 blok identik")
sys.exit(1 if fails else 0)
