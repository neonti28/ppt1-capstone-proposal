import json

B = "/mnt/d/Capstone 1(v2)"
d = json.load(open(f"{B}/scratch/rnd/s6/s6_kandidat.json"))
print("meta", {k: v for k, v in d["meta"].items() if k in ("kelas", "seed", "alpha_budget", "far_maks", "recall_min", "durasi_detik", "waktu", "pandas", "numpy")})
print("repro S2:", d["reproduksi_s2"])
print("galat S2:", len(d["galat_reproduksi_s2"]))
print("seed_cek:", d["seed_cek"])
print("kontrol_ml:", {k: d["kontrol_ml"][k] for k in ("fold_berubah", "n_fold")})
for kelas in ("hyd", "vib", "ssi"):
    print(f"\n=== {kelas}")
    hdr = ("model", "nf", "FP", "TP", "Pmed", "Rmed", "FARmed", "FARmin", "FARmax", "lead", "onset", "dip", "le6", "gateA")
    print(" | ".join(hdr))
    for m, r in d["ringkas"][kelas].items():
        print(" | ".join(str(x) for x in (m, r["n_fold"], r["fp_total"], r["tp_total"],
                                          r["precision_median"], r["recall_median"],
                                          r["far24_kalender_median"], r["far24_kalender_min"],
                                          r["far24_kalender_maks"], r["lead_median_median"],
                                          r["n_onset"], r["n_diperingatkan"], r["fold_far_le6"],
                                          r["fold_gate_A_baru"])))

print("\n=== hyd per fold: rule / H1p(rule&persist) / H1(rule&stat) / H1p3")
recs = d["records"]["seed42"]["hyd"]
fold_set = []
for r in recs:
    if r["fold"] not in fold_set:
        fold_set.append(r["fold"])
idx = {(r["model"], r["fold"]): r for r in recs}
print("fold | model | TP | FP | P | R | FARkal | lead | dip")
for f in fold_set:
    for m in ("rule_kanal", "H1p_rule_dan_persist", "H1_stat_dan_rule", "H1p3_rule_persist_stat"):
        r = idx[(m, f)]
        print(f"{f} | {m} | {r['rows']['tp']} | {r['rows']['fp']} | {r['rows']['precision']} | "
              f"{r['rows']['recall']} | {r['far24_kalender']} | {r['lead']['lead_median_min']} | "
              f"{r['lead']['n_diperingatkan']}/{r['lead']['n_onset']}")
