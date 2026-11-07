#!/usr/bin/env python3
"""S5-A: rerun dua seed S1 (42, 13) dengan harness bersama, bandingkan per metrik
ke artefak JSON S1 dan ke tabel dokumen RND_S1_SEED_ROBUSTNESS.md.

Keluaran: scratch/rnd/s5/s5_rerun.json
"""
import json
import os
import re
import sys
import time

BASE = "/mnt/d/Capstone 1(v2)"
sys.path.insert(0, f"{BASE}/code")
import rnd_hybrid_harness as H  # noqa: E402

DOC = f"{BASE}/docs/RND_S1_SEED_ROBUSTNESS.md"
JSON_S1 = f"{BASE}/scratch/rnd/s1/s1_hyd_seeds.json"
OUT = f"{BASE}/scratch/rnd/s5/s5_rerun.json"
MODEL = "H1_stat_dan_rule"
SEEDS = [42, 13]


def num(s):
    s = s.strip().replace("\u00a0", " ")
    if s in ("", "-", "tidak", "ya"):
        return None
    s = s.replace(" ", "")
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def desimal(s):
    s = s.strip()
    m = re.search(r"[.,](\d+)$", s)
    return len(m.group(1)) if m else 0


def ambil_tabel(baris, awal):
    """Ambil baris tabel markdown mulai indeks awal sampai baris kosong.
    Baris pemisah header (---) dibuang."""
    out = []
    i = awal
    while i < len(baris) and baris[i].startswith("|"):
        sel = [c.strip() for c in baris[i].strip().strip("|").split("|")]
        if not all(re.fullmatch(r":?-{3,}:?", s or "-") for s in sel):
            out.append(sel)
        i += 1
    return out


teks = open(DOC, encoding="utf-8").read().splitlines()


def cari(pat):
    for i, ln in enumerate(teks):
        if re.search(pat, ln):
            return i
    return -1


# ------------------------------------------------------------------ tabel 5.1
i51 = cari(r"^### 5\.1")
t51 = ambil_tabel(teks, i51 + 2)
lintas_doc = {}
for row in t51[1:]:  # lewati header
    if len(row) < 10:
        continue
    met = row[0]
    vals = row[1:]
    lintas_doc[met] = dict(
        per_seed={str(s): num(vals[j]) for j, s in enumerate(["42", "7", "13", "21", "33"])},
        median=num(vals[5]), min=num(vals[6]), maks=num(vals[7]), rentang=num(vals[8]),
        desimal=dict(per_seed={str(s): desimal(vals[j]) for j, s in enumerate(["42", "7", "13", "21", "33"])},
                     median=desimal(vals[5]), min=desimal(vals[6]), maks=desimal(vals[7]),
                     rentang=desimal(vals[8])))

# ------------------------------------------------------------------ tabel 5.2
i52 = cari(r"^### 5\.2")
t52 = ambil_tabel(teks, i52 + 2)
kontrol_doc = {}
for row in t52[1:]:
    if len(row) < 8:
        continue
    seed = row[0]
    kontrol_doc[seed] = dict(
        fp_total=num(row[1]), tp_total=num(row[2]), precision_median=num(row[3]),
        recall_median=num(row[4]), far24_kalender_median=num(row[5]),
        lead_median=num(row[6]), n_diperingatkan=num(row[7]),
        desimal=dict(fp_total=desimal(row[1]), tp_total=desimal(row[2]),
                     precision_median=desimal(row[3]), recall_median=desimal(row[4]),
                     far24_kalender_median=desimal(row[5]), lead_median=desimal(row[6]),
                     n_diperingatkan=desimal(row[7])))

# ------------------------------------------------------------------ tabel 6.1
i61 = cari(r"^### 6\.1")
t61 = ambil_tabel(teks, i61 + 2)
urutan61 = ["TP", "FP", "Presisi", "Recall", "FAR24 kalender", "FAR24 baris",
            "Lead median", "Diperingatkan", "Cakupan", "h", "Gate A baru"]
fold_doc = {}
for row in t61[1:]:
    if not row or not row[0].startswith("F-"):
        continue
    d = {}
    for j, nama in enumerate(urutan61):
        sel = row[j + 1]
        d[nama] = dict(nilai=num(sel), teks=sel, desimal=desimal(sel))
    fold_doc[row[0]] = d

# ------------------------------------------------------------------ tabel 4
i4 = cari(r"^## 4\. Reproduksi")
t4 = ambil_tabel(teks, i4 + 2)
repro_doc = {}
for row in t4[1:]:
    if len(row) < 5:
        continue
    repro_doc[row[0]] = dict(terbit=num(row[1]), replikasi=num(row[2]), delta=num(row[3]),
                             lulus=row[4], desimal_replikasi=desimal(row[2]))

# ------------------------------------------------------------------- JSON S1
j = json.load(open(JSON_S1))

# Mode uji negatif: rusak satu sel dokumen di memori untuk membuktikan
# pembanding bisa GAGAL. Tidak menulis ke berkas dokumen.
NEGATIF = "--negatif" in sys.argv
if NEGATIF:
    lintas_doc["fp_total"]["per_seed"]["42"] = 936.0
    fold_doc["F-10"]["FP"]["nilai"] = 62.0
    out_path = OUT.replace("s5_rerun.json", "s5_negative.json")
else:
    out_path = OUT


def fold_map(recs, model=MODEL):
    return {r["fold"]: r for r in recs if r["model"] == model}


hasil = dict(
    kartu="t_b5b16adc", langkah="S5-A rerun seed 42 dan 13",
    tanggal=time.strftime("%Y-%m-%d %H:%M:%S"),
    sumber=dict(dokumen=DOC, json_s1=JSON_S1),
    tabel_5_1={}, tabel_5_2={}, tabel_6_1={}, tabel_4={},
    rerun={}, selisih_rerun_vs_json={}, selisih_rerun_vs_dokumen={},
)

# ------------------------------------------- 1. dokumen 5.1 vs JSON lintas
for met, dd in lintas_doc.items():
    jj = j["lintas_seed"].get(met)
    if jj is None:
        hasil["tabel_5_1"][met] = dict(status="METRIK_TIDAK_ADA_DI_JSON")
        continue
    baris = {}
    for s in ["42", "7", "13", "21", "33"]:
        a = jj["per_seed"].get(s)
        d = dd["per_seed"][s]
        tol = 0.5 * 10 ** (-dd["desimal"]["per_seed"][s]) + 1e-12
        ok = (a is not None and d is not None and abs(float(a) - d) <= tol)
        baris[s] = dict(json=a, dok=d, delta=None if (a is None or d is None) else round(float(a) - d, 8), cocok=bool(ok))
    for k in ("median", "min", "maks", "rentang"):
        a = jj.get(k)
        d = dd[k]
        tol = 0.5 * 10 ** (-dd["desimal"][k]) + 1e-12
        ok = (a is not None and d is not None and abs(float(a) - d) <= tol)
        baris[k] = dict(json=a, dok=d, delta=None if (a is None or d is None) else round(float(a) - d, 8), cocok=bool(ok))
    hasil["tabel_5_1"][met] = dict(sel=baris, semua_cocok=all(v["cocok"] for v in baris.values()))

# ------------------------------------------- 2. dokumen 5.2 vs JSON kontrol
kontrol_json = (j.get("kontrol_stokastik") or {}).get("per_seed", {})
for seed, dd in kontrol_doc.items():
    jj = (kontrol_json.get(seed) or {}).get("ringkas", {})
    baris = {}
    for nama, nilai_doc in dd.items():
        if nama == "desimal":
            continue
        a = jj.get(nama)
        tol = 0.5 * 10 ** (-dd["desimal"][nama]) + 1e-12
        ok = (a is not None and nilai_doc is not None and abs(float(a) - nilai_doc) <= tol)
        baris[nama] = dict(json=a, dok=nilai_doc, delta=None if (a is None or nilai_doc is None) else round(float(a) - nilai_doc, 8), cocok=bool(ok))
    hasil["tabel_5_2"][seed] = dict(sel=baris, semua_cocok=all(v["cocok"] for v in baris.values()))

# ------------------------------------------- 3. dokumen 6.1 vs JSON per fold
folds42 = fold_map(j["per_seed"]["42"]["folds"])


def nilai_fold(r, nama):
    return {
        "TP": r["rows"]["tp"], "FP": r["rows"]["fp"], "Presisi": r["rows"]["precision"],
        "Recall": r["rows"]["recall"], "FAR24 kalender": r["far24_kalender"],
        "FAR24 baris": r["far24_baris"], "Lead median": r["lead"]["lead_median_min"],
        "Diperingatkan": r["lead"]["n_diperingatkan"], "Cakupan": r["cakupan"],
        "h": r["h_terpilih"], "Gate A baru": r["gate_A_baru"],
    }[nama]


for f, dd in fold_doc.items():
    r = folds42.get(f)
    if r is None:
        hasil["tabel_6_1"][f] = dict(status="FOLD_TIDAK_ADA_DI_JSON")
        continue
    baris = {}
    for nama in urutan61:
        a = nilai_fold(r, nama)
        d = dd[nama]["nilai"]
        if nama == "Gate A baru":
            ok = (str(a).lower() == ("ya" if dd[nama]["teks"] == "ya" else "false")) or (dd[nama]["teks"] == "ya") == bool(a)
            baris[nama] = dict(json=bool(a), dok=dd[nama]["teks"], cocok=bool(ok))
            continue
        tol = 0.5 * 10 ** (-dd[nama]["desimal"]) + 1e-12
        ok = (d is not None and abs(float(a) - d) <= tol)
        baris[nama] = dict(json=a, dok=d, delta=None if d is None else round(float(a) - d, 8), cocok=bool(ok))
    hasil["tabel_6_1"][f] = dict(sel=baris, semua_cocok=all(v["cocok"] for v in baris.values()))

# ------------------------------------------- 4. tabel 4 vs JSON reproduksi
rep = j["reproduksi"]
peta4 = {"FP total": ("fp_total", "fp_total"), "TP total": ("tp_total", "tp_total"),
         "Presisi median": ("precision_median", "precision_median"),
         "Recall median": ("recall_median", "recall_median"),
         "Lead median": ("lead_median", "lead_median"),
         "Onset": ("n_onset", "n_onset"), "Diperingatkan": ("n_diperingatkan", "n_diperingatkan")}
for nama, dd in repro_doc.items():
    pasangan = peta4.get(nama)
    if pasangan is None:
        hasil["tabel_4"][nama] = dict(status="TIDAK_DIPETAKAN")
        continue
    k_rep, k_akt = pasangan
    a_terbit = rep["terbit_r8"][k_rep]
    a_aktual = rep["aktual"][k_akt]
    tol = 0.5 * 10 ** (-dd["desimal_replikasi"]) + 1e-12
    cocok = (abs(float(a_terbit) - dd["terbit"]) <= max(tol, 1e-9) and
             abs(float(a_aktual) - dd["replikasi"]) <= tol)
    hasil["tabel_4"][nama] = dict(terbit_json=a_terbit, terbit_dok=dd["terbit"],
                                  replikasi_json=a_aktual, replikasi_dok=dd["replikasi"],
                                  delta_dok=dd["delta"], lulus_dok=dd["lulus"], cocok=bool(cocok))

# ------------------------------------------------------------- 5. RERUN nyata
t0 = time.time()
df = H.muat_dataset(f"{H.DSD}/hyd_ki.csv.gz")
folds_in = H.muat_fold(f"{H.LOWOD}/lowo_hyd_ki.json")
well_df = H.pecah_well(df)
ringkas_ulang, folds_ulang = {}, {}
for s in SEEDS:
    rec = H.jalankan_h1(seed=s, well_df=well_df, folds=folds_in)
    ringkas_ulang[str(s)] = H.ringkas_records(rec, MODEL)
    folds_ulang[str(s)] = fold_map(rec)
hasil["rerun"]["elapsed_s"] = round(time.time() - t0, 1)
hasil["rerun"]["shape"] = list(df.shape)
hasil["rerun"]["n_fold"] = len(folds_in)
hasil["rerun"]["ringkas"] = ringkas_ulang

# ------------------------------- 6. selisih rerun vs JSON S1 dan vs dokumen
for s in SEEDS:
    k = str(s)
    d_json = j["per_seed"][k]["ringkas"]
    d_rr = ringkas_ulang[k]
    baris = {}
    for met in ("fp_total", "tp_total", "fp_kejadian_total", "precision_median", "recall_median",
                "far24_kalender_median", "far24_kalender_min", "far24_kalender_maks",
                "far24_baris_median", "lead_median_median", "n_onset", "n_diperingatkan",
                "fold_far_le6", "fold_gate_A_baru", "cakupan_median"):
        a, b = d_rr.get(met), d_json.get(met)
        baris[met] = dict(rerun=a, json_s1=b,
                          delta=None if (a is None or b is None) else round(float(a) - float(b), 9),
                          cocok=(a is not None and b is not None and abs(float(a) - float(b)) <= 1e-9))
    # per fold
    fbaris = {}
    for f, r_json in fold_map(j["per_seed"][k]["folds"]).items():
        r_rr = folds_ulang[k].get(f)
        if r_rr is None:
            fbaris[f] = dict(status="HILANG_DI_RERUN")
            continue
        fmet = {}
        for nama in urutan61:
            a = nilai_fold(r_rr, nama)
            b = nilai_fold(r_json, nama)
            if isinstance(a, bool) or isinstance(b, bool):
                fmet[nama] = dict(rerun=bool(a), json_s1=bool(b), cocok=bool(a) == bool(b))
            else:
                fmet[nama] = dict(rerun=a, json_s1=b,
                                  delta=None if (a is None or b is None) else round(float(a) - float(b), 9),
                                  cocok=(a is not None and b is not None and abs(float(a) - float(b)) <= 1e-9))
        fmet["h_terpilih"] = dict(rerun=r_rr["h_terpilih"], json_s1=r_json["h_terpilih"],
                                  cocok=r_rr["h_terpilih"] == r_json["h_terpilih"])
        fbaris[f] = dict(sel=fmet, semua_cocok=all(v["cocok"] for v in fmet.values()))
    hasil["selisih_rerun_vs_json"][k] = dict(ringkas=baris,
                                             semua_cocok_ringkas=all(v["cocok"] for v in baris.values()),
                                             per_fold=fbaris,
                                             semua_cocok_fold=all(v["semua_cocok"] for v in fbaris.values()))

    # rerun vs dokumen 5.1 (kolom seed s) dan 6.1
    dbaris = {}
    for met, dd in lintas_doc.items():
        d_doc = dd["per_seed"].get(k)
        a = d_rr.get(met)
        if d_doc is None or a is None:
            continue
        tol = 0.5 * 10 ** (-dd["desimal"]["per_seed"][k]) + 1e-12
        dbaris[met] = dict(rerun=a, dok=d_doc, delta=round(float(a) - d_doc, 8),
                           cocok=bool(abs(float(a) - d_doc) <= tol))
    dfold = {}
    for f, dd in fold_doc.items():
        r_rr = folds_ulang[k].get(f)
        if r_rr is None:
            continue
        sel = {}
        for nama in urutan61:
            a = nilai_fold(r_rr, nama)
            d = dd[nama]["nilai"]
            if nama == "Gate A baru":
                sel[nama] = dict(rerun=bool(a), dok=dd[nama]["teks"],
                                 cocok=(dd[nama]["teks"] == "ya") == bool(a))
                continue
            tol = 0.5 * 10 ** (-dd[nama]["desimal"]) + 1e-12
            sel[nama] = dict(rerun=a, dok=d, delta=None if d is None else round(float(a) - d, 8),
                             cocok=(d is not None and abs(float(a) - d) <= tol))
        dfold[f] = dict(sel=sel, semua_cocok=all(v["cocok"] for v in sel.values()))
    hasil["selisih_rerun_vs_dokumen"][k] = dict(tabel_5_1=dbaris,
                                                semua_cocok_51=all(v["cocok"] for v in dbaris.values()),
                                                tabel_6_1=dfold,
                                                semua_cocok_61=all(v["semua_cocok"] for v in dfold.values()))

# -------------------------------------------------------------- 7. rekap
def hitung_rekap():
    r = dict(t51_metrik=len(hasil["tabel_5_1"]),
             t51_gagal=sorted([m for m, v in hasil["tabel_5_1"].items() if not v.get("semua_cocok")]),
             t52_gagal=sorted([s for s, v in hasil["tabel_5_2"].items() if not v.get("semua_cocok")]),
             t61_gagal=sorted([f for f, v in hasil["tabel_6_1"].items() if not v.get("semua_cocok")]),
             t4_gagal=sorted([m for m, v in hasil["tabel_4"].items() if not v.get("cocok")]))
    for s in SEEDS:
        k = str(s)
        v = hasil["selisih_rerun_vs_json"][k]
        w = hasil["selisih_rerun_vs_dokumen"][k]
        r[f"rerun{k}_ringkas_beda"] = sorted([m for m, x in v["ringkas"].items() if not x["cocok"]])
        r[f"rerun{k}_fold_beda"] = sorted([f for f, x in v["per_fold"].items() if not x["semua_cocok"]])
        r[f"rerun{k}_dok51_beda"] = sorted([m for m, x in w["tabel_5_1"].items() if not x["cocok"]])
        r[f"rerun{k}_dok61_beda"] = sorted([f for f, x in w["tabel_6_1"].items() if not x["semua_cocok"]])
    return r


hasil["rekap"] = hitung_rekap()
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(hasil, f, indent=1, ensure_ascii=False)

print(json.dumps(hasil["rekap"], indent=1, ensure_ascii=False))
print("elapsed rerun:", hasil["rerun"]["elapsed_s"])
print("tulis:", out_path, "mode_negatif:", NEGATIF)
if NEGATIF:
    gagal = (hasil["rekap"]["t51_gagal"] == ["fp_total"] and hasil["rekap"]["t61_gagal"] == ["F-10"])
    print("UJI_NEGATIF_TERDETEKSI:", gagal)
    sys.exit(0 if gagal else 3)
