#!/usr/bin/env python3
"""S3c: rekap per fold dari s3b_hybrid.json plus angka sirkularitas s3a.

Keluaran: scratch/rnd/s3/s3c_ringkas.json
Semua angka dokumen diambil dari berkas ini, bukan dari ingatan.
"""
import json
import statistics as st

BASE = "/mnt/d/Capstone 1(v2)"
D = f"{BASE}/scratch/rnd/s3"

with open(f"{D}/s3b_hybrid.json") as f:
    h = json.load(f)
with open(f"{D}/s3a_feasibility.json") as f:
    a = json.load(f)

MODELS = ["rule_label", "rule_kanal", "stat_cusum", "H5_stat_dan_rule",
          "ml_fisik", "H6_ml_dan_stat", "ml_dengan_MSE"]

tabel = []
for r in h["records"]:
    far = r["far24_kalender"]
    tabel.append(dict(
        fold=r["fold"], model=r["model"], n=r["n"], n_pos=r["n_pos"],
        tp=r["rows"]["tp"], fp=r["rows"]["fp"],
        precision=r["rows"]["precision"], recall=r["rows"]["recall"],
        menit_neg=r["far"]["menit_neg"], menit_alarm_neg=r["far"]["menit_alarm_neg"],
        far24=far, far_per_1000_sampel=r["far_per_1000_sampel"],
        lead_median_sampel=r["lead"]["lead_median_min"],
        n_onset=r["lead"]["n_onset"], n_diperingatkan=r["lead"]["n_diperingatkan"],
        h=r["h_terpilih"], amb=r["ambang_conformal"],
        gate_A_baru=r["gate_A_baru"],
    ))

# agregat hanya dari fold yang FAR-nya terdefinisi
agg = {}
for m in MODELS:
    sub = [t for t in tabel if t["model"] == m]
    valid = [t for t in sub if t["far24"] is not None]
    agg[m] = dict(
        n_fold=len(sub), n_fold_far_terdefinisi=len(valid),
        fp_total=int(sum(t["fp"] for t in sub)),
        tp_total=int(sum(t["tp"] for t in sub)),
        recall_median=round(st.median([t["recall"] for t in sub if t["recall"] is not None]), 4)
        if any(t["recall"] is not None for t in sub) else None,
        precision_median=round(st.median([t["precision"] for t in sub if t["precision"] is not None]), 4)
        if any(t["precision"] is not None for t in sub) else None,
        far24_median_valid=round(st.median([t["far24"] for t in valid]), 3) if valid else None,
        far24_min_valid=round(min(t["far24"] for t in valid), 3) if valid else None,
        far24_maks_valid=round(max(t["far24"] for t in valid), 3) if valid else None,
        fold_far_le6=int(sum(1 for t in valid if t["far24"] <= 6.0)),
        fold_gate_A=int(sum(1 for t in sub if t["gate_A_baru"])),
        lead_median_sampel=round(st.median([t["lead_median_sampel"] for t in sub
                                            if t["lead_median_sampel"] is not None]), 3)
        if any(t["lead_median_sampel"] is not None for t in sub) else None,
        n_onset=int(sum(t["n_onset"] for t in sub)),
        n_diperingatkan=int(sum(t["n_diperingatkan"] for t in sub)),
    )

far_takdef = sorted({t["fold"] for t in tabel if t["far24"] is None})
laju = {f["fold"]: f["laju_stat"] for f in h["folds"]}
amb = {f["fold"]: f["ambang_conformal"] for f in h["folds"]}

# baseline bengkel dari artefak, bukan dari dokumen
with open(f"{BASE}/scratch/v9_i1/v9_i1_RESULTS.json") as f:
    v9 = json.load(f)
tw = {e["engine"]: e for e in v9["engines"]}["tool_wear"]
head = [x for x in tw["heads"] if x.get("head") == "op_far_calibrated"][0]
bengkel = dict(
    fp_per_alat=[p["fp_R01"] for p in head["per_alat"]],
    tlead_detik=[p["TLead_s"] for p in head["per_alat"]],
    deteksi=[p["det_R02"] for p in head["per_alat"]],
    n_jendela=tw["heads"][0]["n_windows"], n_alat=tw["heads"][0]["n_alat"],
    presisi_run=tw["heads"][0]["metrik_segmen"]["precision"],
    recall_run=tw["heads"][0]["metrik_segmen"]["recall"],
    sumber="scratch/v9_i1/v9_i1_RESULTS.json engines[tool_wear].heads[op_far_calibrated]",
)

out = dict(
    sumber=dict(hybrid=f"{D}/s3b_hybrid.json", feasibility=f"{D}/s3a_feasibility.json"),
    kelayakan=dict(
        baris=a["inventaris"]["baris"], kolom=a["inventaris"]["kolom"],
        n_well=a["label"]["n_well"], n_pos=a["label"]["n_pos"],
        prevalensi=a["label"]["prevalensi"],
        well_tanpa_positif=a["label"]["well_tanpa_positif"],
        ada_kolom_identitas_bit=a["identitas"]["ada_kolom_identitas_bit"],
        ada_kolom_run=a["identitas"]["ada_kolom_run"],
        kolom_mengandung_bit=a["identitas"]["kolom_mengandung_bit"],
        n_diameter_unik=a["identitas"]["n_diameter_unik"],
        indeks_duplikat=a["identitas"]["indeks_duplikat"],
        sirkularitas=a["sirkularitas"],
        grid_kedalaman=a["grid_kedalaman"],
        waktu_kalender=a["waktu_kalender"],
        per_well=a["label"]["per_well"],
    ),
    tabel=tabel, agregat=agg,
    far_tak_terdefinisi=far_takdef,
    laju_stat=laju, ambang_conformal=amb,
    baseline_bengkel=bengkel,
    meta=h["meta"], well_info=h["well_info"],
)
with open(f"{D}/s3c_ringkas.json", "w") as f:
    json.dump(out, f, indent=1, default=float)

print("fold FAR tak terdefinisi:", far_takdef)
print("laju_stat:", json.dumps(laju, indent=1)[:600])
print("\nagregat:")
for m in MODELS:
    g = agg[m]
    print(f"  {m:18s} fold={g['n_fold']} far_def={g['n_fold_far_terdefinisi']} "
          f"tp={g['tp_total']:6d} fp={g['fp_total']:6d} "
          f"P={g['precision_median']} R={g['recall_median']} "
          f"far24_med={g['far24_median_valid']} far24_min={g['far24_min_valid']} "
          f"le6={g['fold_far_le6']} gateA={g['fold_gate_A']}")
print("\nbengkel:", bengkel["fp_per_alat"], bengkel["tlead_detik"], bengkel["presisi_run"])
print("wrote", f"{D}/s3c_ringkas.json")
