import json

# TOPSIS/WSM arithmetic audit against docx Table 3.4 (Proposal_PPT_I, lines 261-308)
K = ["K1", "K2", "K3", "K4", "K5", "K6"]
w = [0.25, 0.20, 0.15, 0.10, 0.15, 0.15]
rows = {
    "A1": ([5, 5, 4, 3, 4, 4], 4.35),
    "A2": ([4, 3, 3, 4, 3, 3], 3.40),
    "A3": ([3, 2, 5, 4, 5, 3], 3.55),
    "A4": ([3, 2, 2, 5, 5, 2], 2.95),
    "A6": ([2, 1, 3, 2, 5, 2], 2.45),
}
fmea = [
    ("Excessive vibration", 9, 7, 6, 378),
    ("Stick-slip", 8, 7, 5, 280),
    ("Pressure anomaly", 9, 6, 6, 324),
    ("Telemetry failure", 7, 5, 7, 245),
    ("Bit/BHA dysfunction", 8, 6, 5, 240),
]

out = {"weights_sum": round(sum(w), 4), "scores": {}, "fmea": []}
print("sum w =", sum(w))
for k, (v, claimed) in rows.items():
    wsm = round(sum(a * b for a, b in zip(v, w)), 4)
    # TOPSIS step: normalised decision matrix r_ij = x_ij/sqrt(sum x_ij^2) over alternatives
    out["scores"][k] = {"nilai": v, "skor_docx": claimed, "wsm_hitung": wsm,
                        "selisih": round(claimed - wsm, 4)}
    print(k, "WSM=", wsm, "docx=", claimed, "delta=", round(claimed - wsm, 4))

# real TOPSIS (vector normalisation + ideal/anti-ideal distance) with same weights
import math
alts = list(rows.keys())
vals = {k: rows[k][0] for k in alts}
norm = {}
for j in range(6):
    denom = math.sqrt(sum(vals[k][j] ** 2 for k in alts))
    for k in alts:
        norm.setdefault(k, []).append(vals[k][j] / denom)
weighted = {k: [norm[k][j] * w[j] for j in range(6)] for k in alts}
ideal = [max(weighted[k][j] for k in alts) for j in range(6)]
anti = [min(weighted[k][j] for k in alts) for j in range(6)]
topsis = {}
for k in alts:
    dp = math.sqrt(sum((weighted[k][j] - ideal[j]) ** 2 for j in range(6)))
    dn = math.sqrt(sum((weighted[k][j] - anti[j]) ** 2 for j in range(6)))
    topsis[k] = round(dn / (dp + dn), 4)
out["topsis_cc"] = topsis
print("TOPSIS closeness coeff:", topsis)
print("rank TOPSIS:", sorted(topsis, key=lambda x: -topsis[x]))

for name, S, O, D, rpn in fmea:
    calc = S * O * D
    out["fmea"].append({"mode": name, "S": S, "O": O, "D": D, "rpn_docx": rpn,
                        "rpn_hitung": calc, "cocok": calc == rpn})
    print(name, S, O, D, "->", calc, "docx", rpn, "OK" if calc == rpn else "MISMATCH")

json.dump(out, open("/mnt/d/Capstone 1(v2)/scratch/ppt1/arith_audit.json", "w"), indent=1)
print("saved arith_audit.json")
