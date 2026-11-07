"""RND-E4 — agregasi sebelum vs sesudah, tiga definisi gate, dua satuan.

Semua angka dibaca dari JSON hasil run, tidak ada yang diketik manual.
"""
import json, os
import numpy as np

BASE = "/mnt/d/Capstone 1(v2)"
E4 = f"{BASE}/scratch/rnd/e4"
E3 = f"{BASE}/scratch/rnd/e3"


def jload(p):
    with open(p) as f:
        return json.load(f)


def med(v):
    v = [x for x in v if x is not None]
    return round(float(np.median(v)), 4) if v else None


a1 = jload(f"{E4}/e4_a1.json")
hyb = jload(f"{E4}/e4_hybrid.json")
base = jload(f"{E4}/e4_baseline.json")
a2 = jload(f"{E4}/e4_a2.json")
e3a = jload(f"{E3}/e3_a_conformal_results.json")
e3b = jload(f"{E3}/e3_baseline_results.json")
e3c = jload(f"{E3}/e3_cakupan.json")

assert a1["n_fitur"] == 40 and "ts_bin" not in a1["fitur"], "R7-2 tidak terbukti"

# ---------------- tabel per fold: semua model ------------------------------
def row_from_penuh(r, model):
    return dict(model=model, fold=r.get("fold", r.get("test_well")), seed=r.get("seed"),
                fp_baris=r["rows"]["fp"], fp_kejadian=r["events"]["fp_kejadian"],
                far24_baris=r["rows"]["far_per_24h"],
                far24_kejadian=r["events"]["far24_kejadian"],
                far24_kalender=r["far24_kalender"],
                recall=r["rows"]["recall"], precision=r["rows"]["precision"],
                cakupan=r["cakupan"]["fraksi"], gate_A_lama=r["gate_A_lama"],
                gate_A_lama_penuh=r["gate_A_lama_penuh"], gate_A_baru=r["gate_A_baru"])


tabel = []
for r in base["folds"]:
    tabel.append(row_from_penuh(r, r["model"]))
for r in a1["folds"]:
    tabel.append(row_from_penuh(r, "A1_" + r["varian"]))
for r in hyb["folds"]:
    tabel.append(row_from_penuh(r, r["model"]))
for r in a2["folds"]:
    tabel.append(dict(model="A2_cusum_h30", fold=r["test_well"], seed=None,
                      fp_baris=r["rows"]["fp"], fp_kejadian=r["fp_kejadian"],
                      far24_baris=r["rows"]["far_per_24h"],
                      far24_kejadian=r["far24_kejadian_episode"],
                      far24_kalender=r["far24_kalender"],
                      recall=r["rows"]["recall"], precision=r["rows"]["precision"],
                      cakupan=r["cakupan"]["fraksi"], gate_A_lama=r["gate_A_lama"],
                      gate_A_lama_penuh=r["gate_A_lama_penuh"], gate_A_baru=r["gate_A_baru"]))

# ---------------- tiga definisi gate ---------------------------------------
def gate_counts(sel):
    """G1 = FAR baris <= 6 (definisi E3 lama). G2 = FAR kejadian <= 6 dan recall >= 0.5.
    G3 = G2 ditambah cakupan >= 0.5 dan FAR kalender <= 6 (usulan R7-6). G4 = G3 tanpa syarat cakupan."""
    g1 = sum(1 for r in sel if r["gate_A_lama"])
    g2 = sum(1 for r in sel if (r["far24_kejadian"] is not None and r["far24_kejadian"] <= 6
                                and (r["recall"] or 0) >= 0.5))
    g3 = sum(1 for r in sel if r["gate_A_baru"])
    g4 = sum(1 for r in sel if (r["far24_kejadian"] is not None and r["far24_kejadian"] <= 6
                                and (r["recall"] or 0) >= 0.5
                                and r["far24_kalender"] <= 6))
    return dict(n=len(sel), G1_far_baris=g1, G2_far_kejadian_recall=g2,
                G3_baru_plus_cakupan=g3, G4_tanpa_syarat_cakupan=g4)


models = sorted(set(r["model"] for r in tabel))
ringkas = {}
for m in models:
    sel = [r for r in tabel if r["model"] == m]
    ringkas[m] = dict(
        far24_baris_median=med([r["far24_baris"] for r in sel]),
        far24_kejadian_median=med([r["far24_kejadian"] for r in sel]),
        far24_kalender_median=med([r["far24_kalender"] for r in sel]),
        recall_median=med([r["recall"] for r in sel]),
        precision_median=med([r["precision"] for r in sel]),
        fp_baris_total=int(sum(r["fp_baris"] for r in sel)),
        fp_kejadian_total=int(sum(r["fp_kejadian"] for r in sel)),
        fold_recall_nol=sum(1 for r in sel if (r["recall"] or 0) == 0),
        **gate_counts(sel))

# ---------------- SEBELUM (E3, seed 42, fitur 41 termasuk ts_bin) ----------
def dari_e3():
    f = [r for r in e3a["folds"] if r["seed"] == 42]
    return dict(model="A1_E3_sebelum",
                n=len(f), n_fitur=41, ts_bin_dipakai=True,
                far24_baris_median=med([r["far_per_24h"] for r in f]),
                recall_median=med([r["recall"] for r in f]),
                precision_median=med([r["precision"] for r in f]),
                auprc_median=med([r["auprc"] for r in f]),
                fp_baris_total=int(sum(r["fp"] for r in f)),
                fold_gate_A_E3=sum(1 for r in f if r["gate_A_lulus"]),
                fold_gate_A_dengan_recall=sum(1 for r in f if r["gate_A_lulus"] and (r["recall"] or 0) >= 0.5))


sebelum = dari_e3()
sebelum["baseline_proxy_total_fp"] = e3b["total_fp"]
sesudah = dict(
    model="A1_E4_sesudah",
    n_fitur=40, ts_bin_dipakai=False,
    varian_alpha=ringkas["A1_alpha_E2_lama"],
    varian_anggaran=ringkas["A1_alpha_anggaran"],
    baseline_total_fp=base["total_fp"],
    assert_r7_1=base["assert_r7_1"])

# ---------------- cakupan per fold -----------------------------------------
cak = [dict(fold=r["fold"], well=r["test_well"], n_jendela=r["n_jendela"],
            menit_kalender=r["menit_kalender"], fraksi=r["fraksi"],
            lulus_cakupan_min_050=bool((r["fraksi"] or 0) >= 0.5)) for r in e3c["per_fold"]]

out = dict(deskripsi="Agregasi E4: sebelum (E3, fitur 41 termasuk ts_bin, aturan alpha E2) "
                     "lawan sesudah (E4, fitur 40, alpha anggaran 1/240, baseline rule t0-1).",
           assert_r7_1=base["assert_r7_1"], assert_r7_2=dict(n_fitur=a1["n_fitur"],
                                                            ts_bin_dipakai="ts_bin" in a1["fitur"]),
           cakupan=cak, n_fold_cakupan_lulus=sum(1 for r in cak if r["lulus_cakupan_min_050"]),
           ringkas=ringkas, sebelum=sebelum, sesudah=sesudah, tabel=tabel)
json.dump(out, open(f"{E4}/e4_compare.json", "w"), indent=2)

print("=== RINGKAS PER MODEL (median; gate G1/G2/G3/G4) ===")
for m in models:
    r = ringkas[m]
    print(f"{m:26s} n={r['n']:2d} FARbaris={str(r['far24_baris_median']):>8s} "
          f"FARkej={str(r['far24_kejadian_median']):>8s} FARkal={str(r['far24_kalender_median']):>8s} "
          f"R={str(r['recall_median']):>8s} P={str(r['precision_median']):>8s} "
          f"G1={r['G1_far_baris']} G2={r['G2_far_kejadian_recall']} "
          f"G3={r['G3_baru_plus_cakupan']} G4={r['G4_tanpa_syarat_cakupan']}")
print("\n=== SEBELUM vs SESUDAH (A1, seed 42) ===")
print(json.dumps(sebelum, indent=1))
print("\ncakupan lulus >=0.50:", out["n_fold_cakupan_lulus"], "dari", len(cak))
