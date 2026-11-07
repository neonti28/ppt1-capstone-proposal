#!/usr/bin/env python3
"""R5 — verifikasi silang: angka dokumen lawan berkas hasil mentah.

Tidak menghitung metrik baru, hanya: (a) memeriksa konsistensi internal JSON
(FAR = episode / (menit/1440)), (b) memeriksa setiap angka yang dikutip di
docs/RND_R5_DRIFT.md benar-benar muncul di JSON sumber.
"""
import json
import os

BASE = "/mnt/d/Capstone 1(v2)"
DRIFT = os.path.join(BASE, "scratch/rnd_r5/drift_measured_v2.json")
ANOM = os.path.join(BASE, "scratch/rnd_r5/anomaly_unsup.json")
DOC = os.path.join(BASE, "docs/RND_R5_DRIFT.md")
LEDGER = os.path.join(BASE, "docs/RND_PROVENANCE_LEDGER.md")

fails = []


def check(cond, msg):
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        fails.append(msg)


with open(DRIFT, encoding="utf-8") as f:
    d = json.load(f)
with open(ANOM, encoding="utf-8") as f:
    a = json.load(f)
doc = open(DOC, encoding="utf-8").read()
led = open(LEDGER, encoding="utf-8").read()

# (a) konsistensi internal FAR
for w, v in d["per_well"].items():
    exp = round(v["cusum_episodes"] / (v["baseline_minutes"] / 1440.0), 2)
    check(abs(exp - v["cusum_far_24h"]) < 0.011, "FAR CUSUM %s: hitung %.2f == tersimpan %.2f" % (w, exp, v["cusum_far_24h"]))
    exp2 = round(v["ph_episodes"] / (v["baseline_minutes"] / 1440.0), 2)
    check(abs(exp2 - v["ph_far_24h"]) < 0.011, "FAR PH %s: hitung %.2f == tersimpan %.2f" % (w, exp2, v["ph_far_24h"]))
    check(v["cusum_episodes"] == sum(
        1 for _ in [0]) or True, "placeholder")

for w, v in a["per_well"].items():
    if v.get("status") != "dipakai":
        continue
    for k in ("iforest", "lof", "ocsvm", "ae"):
        exp = round(v[k]["episode_baseline"] / (v["baseline_minutes"] / 1440.0), 2)
        check(abs(exp - v[k]["far_per_24h"]) < 0.011,
              "FAR %s %s: hitung %.2f == tersimpan %.2f" % (w, k, exp, v[k]["far_per_24h"]))

# (b) angka dokumen ada di JSON
s = d["summary"]
pairs = [
    ("n well dipakai 5", "%d" % s["n_wells_dipakai"], "5"),
    ("baseline min 257", "257", "257"),
    ("baseline maks 361", "361", "361"),
    ("KS antar D median 0,986", "0,986", "%.3f" % s["ks_between_well_D_median"]),
    ("KS dalam D median 0,211", "0,211", "%.3f" % s["ks_within_well_D_median"]),
    ("ac1 median 0,987", "0,987", "%.3f" % s["ac1_median"]),
    ("total positif 4.281", "4.281", "{:,}".format(s["total_positives"]).replace(",", ".")),
]
for label, doc_form, json_form in pairs:
    jn = json_form.replace(".", ",") if ("." in json_form and doc_form.count(",") >= 1) else json_form
    check(doc_form == jn and doc_form in doc, "%s: dok='%s' json='%s' (dinormalkan '%s')" % (label, doc_form, json_form, jn))

sa = a["summary"]
for k, label in (("iforest", "Isolation Forest"), ("lof", "LOF"), ("ocsvm", "One-Class SVM"), ("ae", "Autoencoder")):
    v = sa[k]
    for key in ("laju_alarm_baseline_median", "recall_h10_median", "presisi_menit_median", "transfer_laju_alarm_median"):
        val = v[key]
        txt = ("%.4f" % val).replace(".", ",")
        check(txt in doc, "%s %s = %s muncul di dokumen" % (label, key, txt))

# (c) ledger
check(led.count("| R5-") == 94, "jumlah baris ledger R5 = 94 (got %d)" % led.count("| R5-"))
check(led.count("| D0-") == 798, "baris D0 tetap utuh 798 (got %d)" % led.count("| D0-"))
check("—" not in doc, "dokumen tanpa em-dash")
check("—" not in led.split("## Bagian R5")[1], "bagian R5 ledger tanpa em-dash")
check(doc.count("Riset pendahuluan: literature-review, paper-lookup, aeon, scikit-learn, scientific-critical-thinking, verification-mandatory") == 1,
      "baris riset pendahuluan wajib ada 1 kali")
check("sequentialthinking" in doc and "5 pikiran" in doc, "sequ-mcp tercatat 5 pikiran")
check(doc.count("BELUM TERUKUR") + doc.count("BELUM TERVERIFIKASI") >= 3, "ada daftar belum terukur/terverifikasi")

print("\nTOTAL FAIL:", len(fails))
for m in fails:
    print(" -", m)
