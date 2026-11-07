import json

B = "/mnt/d/Capstone 1(v2)"
V = json.load(open(f"{B}/scratch/rnd/s6/s6_verifikasi.json"))
R = V["ringkas"]
F = ["n_fold", "fp_total", "tp_total", "presisi_median", "recall_median", "recall_min",
     "far24_kalender_median", "far24_kalender_maks", "cakupan_median", "lead_median",
     "n_onset", "n_diperingatkan", "fold_far_le6", "fold_recall_ge05", "fold_gate_A",
     "fold_recall_positive", "fold_paruh_dua_positif", "rasio_far_maks_min"]
for kelas in ("hyd", "vib", "ssi"):
    print("=" * 30, kelas)
    print("model".ljust(24) + "".join(f.ljust(14) for f in F))
    for mo, d in R[kelas].items():
        print(mo.ljust(24) + "".join(str(d[f])[:13].ljust(14) for f in F))
print("=" * 30, "turunan")
for k, v in V["turunan"].items():
    if isinstance(v, dict) and not k.startswith("meta"):
        print(k, json.dumps(v)[:400])
    elif not isinstance(v, dict):
        print(k, v)
