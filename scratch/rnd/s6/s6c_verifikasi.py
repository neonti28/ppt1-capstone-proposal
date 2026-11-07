"""RND-S6: verifikasi independen dan turunan angka dari s6_kandidat.json.

Prinsip:
1. Tidak memakai H.ringkas_records. Semua median, hitungan fold, dan turunan
   dihitung ulang di sini dengan statistics.median, supaya kesalahan di harness
   peringkas tidak otomatis lolos.
2. Setiap angka kunci di-assert terhadap nilai terbit: H1 hyd terhadap R8/S1,
   rule dan hybrid rule+persistence pada F-14 terhadap V9 pra-riset, dan
   vib/ssi terhadap S2.
3. Yang tidak dapat dihitung ditulis sebagai None dengan sebab, bukan dikira.
"""
import json
import statistics as st

B = "/mnt/d/Capstone 1(v2)"
KAND = f"{B}/scratch/rnd/s6/s6_kandidat.json"
OUT = f"{B}/scratch/rnd/s6/s6_verifikasi.json"
TOL = 5e-5

d = json.load(open(KAND))
recs = d["records"]["seed42"]

KELAS = ("hyd", "vib", "ssi")
MODEL = {
    "hyd": ("persistence", "rule_kanal", "stat_cusum", "H1p_rule_dan_persist",
            "H1p3_rule_persist_stat", "H1_stat_dan_rule", "H1b_stat_atau_rule"),
    "vib": ("persistence", "rule_kanal", "stat_cusum", "H1p_rule_dan_persist",
            "H1_stat_dan_rule", "H1b_stat_atau_rule"),
    "ssi": ("persistence", "rule_kanal", "stat_cusum", "H1p_rule_dan_persist",
            "H1_stat_dan_rule", "H1b_stat_atau_rule"),
}


def med(xs):
    v = [x for x in xs if x is not None]
    return round(float(st.median(v)), 6) if v else None


def mn(xs):
    v = [x for x in xs if x is not None]
    return round(float(min(v)), 6) if v else None


def mx(xs):
    v = [x for x in xs if x is not None]
    return round(float(max(v)), 6) if v else None


def ringkas(kelas, model):
    sub = [r for r in recs[kelas] if r["model"] == model]
    if not sub:
        return None
    far = [r["far24_kalender"] for r in sub]
    paruh_ok = 0
    for r in sub:
        s = r["separuh"]
        if len(s) == 2 and all((s[k]["recall"] or 0) > 0 for k in ("awal", "akhir")):
            paruh_ok += 1
    return dict(
        kelas=kelas, model=model, n_fold=len(sub),
        fp_total=sum(int(r["rows"]["fp"]) for r in sub),
        tp_total=sum(int(r["rows"]["tp"]) for r in sub),
        tp_kejadian=sum(int(r["events"]["tp_kejadian"]) for r in sub),
        fp_kejadian=sum(int(r["events"]["fp_kejadian"]) for r in sub),
        presisi_median=med([r["rows"]["precision"] for r in sub]),
        recall_median=med([r["rows"]["recall"] for r in sub]),
        presisi_min=mn([r["rows"]["precision"] for r in sub]),
        presisi_maks=mx([r["rows"]["precision"] for r in sub]),
        recall_min=mn([r["rows"]["recall"] for r in sub]),
        recall_maks=mx([r["rows"]["recall"] for r in sub]),
        far24_kalender_median=med(far), far24_kalender_min=mn(far), far24_kalender_maks=mx(far),
        far24_baris_median=med([r["far24_baris"] for r in sub]),
        cakupan_median=med([r["cakupan"] for r in sub]),
        lead_median=med([r["lead"]["lead_median_min"] for r in sub]),
        lead_median_maks=mx([r["lead"]["lead_median_min"] for r in sub]),
        n_onset=sum(int(r["lead"]["n_onset"]) for r in sub),
        n_diperingatkan=sum(int(r["lead"]["n_diperingatkan"]) for r in sub),
        fold_far_le6=sum(1 for x in far if x <= 6.0),
        fold_recall_ge05=sum(1 for r in sub if (r["rows"]["recall"] or 0) >= 0.5),
        fold_gate_A=sum(1 for r in sub if r["gate_A_baru"]),
        fold_recall_positive=sum(1 for r in sub if (r["rows"]["recall"] or 0) > 0),
        fold_paruh_dua_positif=paruh_ok,
        rasio_far_maks_min=round(mx(far) / mn(far), 4) if mn(far) else None,
    )


R = {}
for k in KELAS:
    R[k] = {}
    for m in MODEL[k]:
        r = ringkas(k, m)
        if r:
            R[k][m] = r

# ------------------------------------------------------------------ cek terbit
cek = []


def assert_eq(label, got, want, tol=TOL):
    ok = abs(float(got) - float(want)) < tol
    cek.append(dict(label=label, got=got, want=want, lulus=bool(ok)))
    assert ok, (label, got, want)


assert_eq("hyd H1 fp_total = R8-001", R["hyd"]["H1_stat_dan_rule"]["fp_total"], 935)
assert_eq("hyd H1 tp_total = R8-006", R["hyd"]["H1_stat_dan_rule"]["tp_total"], 3804)
assert_eq("hyd H1 presisi median = R8-010", R["hyd"]["H1_stat_dan_rule"]["presisi_median"], 0.7789)
assert_eq("hyd H1 recall median = R8-011", R["hyd"]["H1_stat_dan_rule"]["recall_median"], 0.5638)
assert_eq("hyd H1 FAR median = R8-012", R["hyd"]["H1_stat_dan_rule"]["far24_kalender_median"], 3.5302)
assert_eq("hyd H1 lead median = R8-016", R["hyd"]["H1_stat_dan_rule"]["lead_median"], 11.5)
assert_eq("hyd H1 diperingatkan = R8-018", R["hyd"]["H1_stat_dan_rule"]["n_diperingatkan"], 219)
assert_eq("hyd rule fp_total = R8-002", R["hyd"]["rule_kanal"]["fp_total"], 2105)
assert_eq("hyd rule tp_total = R8-007", R["hyd"]["rule_kanal"]["tp_total"], 5579)
assert_eq("hyd rule presisi = R8-009", R["hyd"]["rule_kanal"]["presisi_median"], 0.6835)
assert_eq("hyd rule recall = R8 bagian 4.1", R["hyd"]["rule_kanal"]["recall_median"], 0.7507)
assert_eq("hyd rule diperingatkan = R8-019", R["hyd"]["rule_kanal"]["n_diperingatkan"], 307)

# F-14: V9 pra-riset (S1-054..S1-069)
idx = {(r["model"], r["fold"]): r for r in recs["hyd"]}
f14 = "F-14"
assert_eq("F-14 rule TP = V9/S1-054", idx[("rule_kanal", f14)]["rows"]["tp"], 607)
assert_eq("F-14 rule FP = V9/S1-056", idx[("rule_kanal", f14)]["rows"]["fp"], 368)
assert_eq("F-14 rule presisi = S1-058", idx[("rule_kanal", f14)]["rows"]["precision"], 0.622564)
assert_eq("F-14 rule recall = S1-059", idx[("rule_kanal", f14)]["rows"]["recall"], 0.701734)
assert_eq("F-14 rule FAR baris = V9", idx[("rule_kanal", f14)]["far24_baris"], 55.57, tol=5e-3)
assert_eq("F-14 H1p TP = V9/S1-061", idx[("H1p_rule_dan_persist", f14)]["rows"]["tp"], 516)
assert_eq("F-14 H1p FP = V9/S1-062", idx[("H1p_rule_dan_persist", f14)]["rows"]["fp"], 110)
assert_eq("F-14 H1p presisi = S1-063", idx[("H1p_rule_dan_persist", f14)]["rows"]["precision"], 0.8243, tol=5e-4)
assert_eq("F-14 H1p recall = S1-064", idx[("H1p_rule_dan_persist", f14)]["rows"]["recall"], 0.5965, tol=5e-4)
assert_eq("F-14 H1p FAR baris = S1-065", idx[("H1p_rule_dan_persist", f14)]["far24_baris"], 16.611, tol=5e-3)
assert_eq("F-14 H1 TP = S1-066", idx[("H1_stat_dan_rule", f14)]["rows"]["tp"], 443)
assert_eq("F-14 H1 FP = S1-067", idx[("H1_stat_dan_rule", f14)]["rows"]["fp"], 215)

# vib/ssi terhadap S2
assert_eq("vib persistence FP = S2", R["vib"]["persistence"]["fp_total"], 1456)
assert_eq("vib persistence recall = S2", R["vib"]["persistence"]["recall_median"], 0.7405)
assert_eq("vib persistence FAR = S2", R["vib"]["persistence"]["far24_kalender_median"], 22.0218)
assert_eq("vib H1 recall = S2", R["vib"]["H1_stat_dan_rule"]["recall_median"], 0.1426)

# ssi: S2 hanya memakai 7 fold yang dapat diuji (n_pos >= 30). Batasi dulu.
ssi_uji = [r for r in recs["ssi"]
           if r["model"] == "persistence" and int(r["n_pos"]) >= 30]
assert len(ssi_uji) == 7, len(ssi_uji)
ssi_fp = sum(int(r["rows"]["fp"]) for r in ssi_uji)
ssi_rec = med([r["rows"]["recall"] for r in ssi_uji])
assert_eq("ssi persistence FP 7 fold uji = S2", ssi_fp, 255)
assert_eq("ssi persistence recall median 7 fold = S2", ssi_rec, 0.0361)

# ------------------------------------------------------------- turunan lapisan
DER = {}
hyd = R["hyd"]
DER["delta_tp_H1p_lawan_H1"] = hyd["H1p_rule_dan_persist"]["tp_total"] - hyd["H1_stat_dan_rule"]["tp_total"]
DER["delta_tp_H1p_persen"] = round(100.0 * DER["delta_tp_H1p_lawan_H1"] / hyd["H1_stat_dan_rule"]["tp_total"], 4)
DER["delta_fp_H1p_lawan_H1"] = hyd["H1p_rule_dan_persist"]["fp_total"] - hyd["H1_stat_dan_rule"]["fp_total"]
DER["delta_recall_H1p_lawan_H1"] = round(hyd["H1p_rule_dan_persist"]["recall_median"] - hyd["H1_stat_dan_rule"]["recall_median"], 4)
DER["delta_presisi_H1p_lawan_H1"] = round(hyd["H1p_rule_dan_persist"]["presisi_median"] - hyd["H1_stat_dan_rule"]["presisi_median"], 4)
DER["delta_far_H1p_lawan_H1"] = round(hyd["H1p_rule_dan_persist"]["far24_kalender_median"] - hyd["H1_stat_dan_rule"]["far24_kalender_median"], 4)
DER["delta_tp_H1p3_lawan_H1"] = hyd["H1p3_rule_persist_stat"]["tp_total"] - hyd["H1_stat_dan_rule"]["tp_total"]
DER["delta_fp_H1p3_lawan_H1"] = hyd["H1p3_rule_persist_stat"]["fp_total"] - hyd["H1_stat_dan_rule"]["fp_total"]
DER["fold_far_le6_H1p3_vs_H1"] = [hyd["H1p3_rule_persist_stat"]["fold_far_le6"], hyd["H1_stat_dan_rule"]["fold_far_le6"]]
DER["alarm_per_onset"] = {k: round(R["hyd"][k]["fp_total"] / R["hyd"][k]["n_onset"], 4)
                          for k in ("rule_kanal", "H1_stat_dan_rule", "H1p_rule_dan_persist",
                                    "H1p3_rule_persist_stat")}
DER["lead_persen_henti_median_60mnt"] = {
    k: round(100.0 * R["hyd"][k]["lead_median"] / 60.0, 2)
    for k in ("rule_kanal", "H1_stat_dan_rule", "H1p_rule_dan_persist", "H1p3_rule_persist_stat")
}
DER["kontrol_ml"] = d["kontrol_ml"]
DER["seed_cek"] = d["seed_cek"]
DER["reproduksi_s2"] = d["reproduksi_s2"]
DER["galat_reproduksi_s2"] = len(d["galat_reproduksi_s2"])
DER["meta"] = d["meta"]

tulis = dict(kartu="RND-S6", waktu=d["meta"]["waktu"], kelas=list(KELAS), ringkas=R,
             cek_terbit=cek, turunan=DER,
             jumlah_cek=len(cek), jumlah_cek_lulus=sum(1 for c in cek if c["lulus"]),
             catatan=("Median dihitung ulang dengan statistics.median, bukan H.ringkas_records. "
                      "Kelas ssi pada S6 memakai 9 fold termasuk dua fold UNDERPOWERED dari S2, "
                      "sehingga angka ssi di sini bukan angka S2 yang sama penyebutnya."))
json.dump(tulis, open(OUT, "w"), indent=1)
print("cek lulus", tulis["jumlah_cek_lulus"], "dari", tulis["jumlah_cek"])
for k in KELAS:
    for m, r in R[k].items():
        print(f"{k:4s} {m:24s} FP {r['fp_total']:5d} TP {r['tp_total']:5d} P {r['presisi_median']} "
              f"R {r['recall_median']} FARmed {r['far24_kalender_median']} le6 {r['fold_far_le6']} "
              f"lead {r['lead_median']} dip {r['n_diperingatkan']}/{r['n_onset']} paruh2 {r['fold_paruh_dua_positif']}")
print(json.dumps(DER, indent=1)[:1600])
print("tulis", OUT)
