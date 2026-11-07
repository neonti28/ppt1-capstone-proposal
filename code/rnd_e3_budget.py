#!/usr/bin/env python3
"""RND-E3 — anggaran laju alarm: mengapa gate A gagal secara mekanis.

Untuk FAR kalender <= 6 per 24 jam, fraksi menit negatif yang boleh menyala
adalah 6/1440 = 1/240 = 0,00416667. Skrip ini menghitung fraksi menyala
(fp / n_neg) per fold untuk tiap model, lalu rasionya terhadap anggaran itu.

Keluaran: scratch/rnd/e3/e3_budget.json
"""
import json

BASE = "/mnt/d/Capstone 1(v2)"
OUT = f"{BASE}/scratch/rnd/e3"
BUDGET = 6.0 / 1440.0          # 0,00416667 fraksi menit negatif
FAR_MAX = 6.0


def load(n):
    return json.load(open(f"{OUT}/{n}"))


def rows_prov(name, rows):
    out = []
    for r in rows:
        n_neg = r["n_neg"]
        frac = r["fp"] / n_neg if n_neg else None
        out.append(dict(
            fold=r.get("fold"), well=r.get("test_well"),
            alpha=r.get("alpha"), h=r.get("h"),
            fp=r["fp"], tp=r["tp"], n_neg=n_neg,
            fraksi_menit_menyala=round(frac, 6) if frac is not None else None,
            far_per_24h=round(r["far_per_24h"], 4) if r.get("far_per_24h") is not None else None,
            rasio_vs_anggaran=round(frac / BUDGET, 3) if frac is not None else None,
            lulus_gate_A_6=r.get("gate_A_lulus"),
        ))
    return out


A1 = load("e3_a_conformal_results.json")
A1B = load("e3_a1b_lag_results.json")
A2 = load("e3_b_cusum_results.json")
BL = load("e3_baseline_results.json")

park = {
    "anggaran_fraksi_menit_negatif": BUDGET,
    "far_maks_per_24h": FAR_MAX,
    "rumus": "FAR_24 = fp / (n_neg/60) * 24 ; anggaran fp <= n_neg/240",
    "A1_seed42": rows_prov("A1", [r for r in A1["folds"] if r["seed"] == 42]),
    "A1_semua_seed": rows_prov("A1", A1["folds"]),
    "A1b": rows_prov("A1b", A1B["folds"]),
    "A2_reset": rows_prov("A2", A2["varian"]["reset"]["folds"]),
    "A2_tanpa_reset": rows_prov("A2", A2["varian"]["tanpa_reset"]["folds"]),
    "baseline_persistence": rows_prov("pers", [r for r in BL["folds"] if r["model"] == "persistence"]),
    "baseline_hybrid_proxy": rows_prov("hyb", [r for r in BL["folds"]
                                               if r["model"] == "hybrid_rule_lag1_and_persistence"]),
}

# alpha yang dipilih A1 vs alpha yang dibutuhkan untuk lulus gate A
alfa = []
for r in A1["folds"]:
    if r["seed"] != 42:
        continue
    alfa.append(dict(well=r["test_well"], alpha_dipilih=r["alpha"],
                     alpha_dibutuhkan_agar_lulus=BUDGET,
                     kelebihan_kali=round(r["alpha"] / BUDGET, 2)))
park["A1_alpha_vs_anggaran_seed42"] = alfa

json.dump(park, open(f"{OUT}/e3_budget.json", "w"), indent=2)

print("anggaran fraksi menit negatif:", round(BUDGET, 8), "= 1/240")
for name in ("A1_seed42", "A1b", "A2_reset", "A2_tanpa_reset",
             "baseline_persistence", "baseline_hybrid_proxy"):
    v = [r["fraksi_menit_menyala"] for r in park[name] if r["fraksi_menit_menyala"] is not None]
    rr = [r["rasio_vs_anggaran"] for r in park[name] if r["rasio_vs_anggaran"] is not None]
    print(f"{name:24s} n={len(v):3d} fraksi min={min(v):.6f} maks={max(v):.6f} "
          f"rasio min={min(rr):.1f}x maks={max(rr):.1f}x")
print("alpha A1 seed42 vs anggaran:")
for r in alfa:
    print(f"  {r['well']:7s} alpha={r['alpha_dipilih']:<6} kelebihan={r['kelebihan_kali']}x")
