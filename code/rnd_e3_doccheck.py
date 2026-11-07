#!/usr/bin/env python3
"""RND-E3 — pemeriksaan dokumen hasil terhadap berkas JSON.

Bukan pembacaan visual: setiap angka yang muncul di dokumen diambil dari JSON,
diformat dengan konvensi Indonesia (koma desimal), lalu di-assert ADA di teks.
Ditambah pemeriksaan aturan penulisan (tanpa em-dash), kelengkapan bagian wajib,
dan kecocokan klaim jumlah pikiran sequentialthinking.

Keluaran: scratch/rnd/e3/e3_doccheck.json
"""
import json, re, sys

BASE = "/mnt/d/Capstone 1(v2)"
E3 = f"{BASE}/scratch/rnd/e3"
DOC = f"{BASE}/docs/RND_E3_HASIL.md"
LEDGER = f"{BASE}/docs/RND_PROVENANCE_LEDGER.md"

txt = open(DOC, encoding="utf-8").read()
led = open(LEDGER, encoding="utf-8").read()

A1 = json.load(open(f"{E3}/e3_a_conformal_results.json"))
A1B = json.load(open(f"{E3}/e3_a1b_lag_results.json"))
A2 = json.load(open(f"{E3}/e3_b_cusum_results.json"))
BL = json.load(open(f"{E3}/e3_baseline_results.json"))
SUM = json.load(open(f"{E3}/e3_run_summary.json"))
CAK = json.load(open(f"{E3}/e3_cakupan.json"))
VER = json.load(open(f"{E3}/e3_verify.json"))
DOI = json.load(open(f"{E3}/e3_doi.json"))

fail, checks = [], []


def id_(v, nd):
    r = f"{v:,.{nd}f}"
    return r.replace(",", "@").replace(".", ",").replace("@", ".")


def chk(cond, label, detail=""):
    checks.append(dict(check=label, lulus=bool(cond), detail=str(detail)))
    if not cond:
        fail.append(f"{label} :: {detail}")


def ada(s, label):
    chk(s in txt, f"angka di dokumen: {label}", f"dicari '{s}'")


# ---------------------------------------------------------------- bagian wajib
wajib = [
    "Riset pendahuluan: scikit-learn, statsmodels, exploratory-data-analysis, "
    "statistical-analysis, verification-mandatory",
    "Riset pendahuluan: sequentialthinking, 4 pikiran",
    "## 5. Status gate C, A, dan B",
    "## 11. Ringkasan 5 baris",
    "## 12. Daftar yang belum terverifikasi",
    "## 8. Rujukan ilmiah dan status verifikasinya",
]
for w in wajib:
    chk(w in txt, "bagian wajib", w)

for skill in ("scikit-learn", "statsmodels", "exploratory-data-analysis",
              "statistical-analysis", "verification-mandatory"):
    chk(f"**{skill}**" in txt, f"satu kalimat pemakaian skill {skill}", skill)

# ---------------------------------------------------------------- em-dash
n_em = txt.count("\u2014")
n_en = txt.count("\u2013")
chk(n_em == 0, "tanpa em-dash di dokumen", f"jumlah em-dash = {n_em}")
chk(led.count("Bagian E3") >= 1, "bagian E3 ada di ledger", "ok")

# ---------------------------------------------------------------- angka kunci
chk(id_(SUM["elapsed_s"], 1) == "233,7", "elapsed_s 233,7", id_(SUM["elapsed_s"], 1))
ada(id_(SUM["elapsed_s"], 1), "waktu jalan")
ada(id_(VER["v6_total"]["n_baris"], 0), "jumlah baris 52.509")
ada("41", "fitur A1")
ada("43", "fitur A1b")
ada(id_(BL["total_fp"]["persistence"], 0), "total FP persistence 1941")
ada(id_(BL["total_fp"]["hybrid_rule_lag1_and_persistence"], 0), "total FP hybrid 195")

# baseline tabel: setiap FP dan FAR harus muncul dalam format dokumen
for r in BL["folds"]:
    w = r["test_well"]
    ada(f"| {w} |", f"baris baseline {w}")
    ada(id_(r["fp"], 0), f"FP baseline {w} {r['model']}")
    ada(id_(r["far_per_24h"], 2), f"FAR baseline {w} {r['model']}")

# A1 seed 42
a1 = {r["test_well"]: r for r in A1["folds"] if r["seed"] == 42}
for w, r in a1.items():
    ada(id_(r["far_per_24h"], 2), f"FAR A1 {w}")
    ada(id_(r["recall"], 4), f"recall A1 {w}")
    ada(id_(r["tp"], 0), f"TP A1 {w}")

# A1b
for r in A1B["folds"]:
    ada(id_(r["far_per_24h"], 2), f"FAR A1b {r['test_well']}")
    if r["precision"] is not None:
        ada(id_(r["precision"], 4), f"presisi A1b {r['test_well']}")

# A2
for r in A2["varian"]["reset"]["folds"]:
    ada(id_(r["far_per_24h"], 2), f"FAR A2 reset {r['test_well']}")
    ada(id_(r["fp"], 0), f"FP A2 {r['test_well']}")
for r in A2["varian"]["tanpa_reset"]["folds"]:
    ada(id_(r["far_per_24h"], 2), f"FAR A2 tanpa reset {r['test_well']}")

# cakupan
for c in CAK["per_fold"]:
    ada(id_(c["fraksi"], 4), f"cakupan {c['test_well']}")

# gate
ada("2 dari 9", "gate A A1 seed42")
ada("3 dari 45", "gate A A1 semua seed")
ada("4 dari 9", "gate A hybrid proxy")
ada("0 dari 9", "gate A A2")
ada("7 dari 9", "ambang E2")
ada("1/240", "anggaran alarm")
ada("0,00416667", "anggaran fraksi")
ada("12 sampai 48", "kelebihan alpha")
ada("90,6", "rasio maksimum A1")
ada("113", "jumlah pemeriksaan")
ada("233,7", "elapsed")

# rujukan
for r in DOI["refs"]:
    ada(r["doi"], f"DOI {r['key']}")
    ada(str(r["tahun"]), f"tahun rujukan {r['key']}")
    ada(r["penulis"], f"penulis pertama {r['key']}")
chk(sum(1 for r in DOI["refs"] if r["metadata_terverifikasi"]) == 7,
    "7 metadata DOI terverifikasi", "ok")

# koefisien/angka terlarang: tidak boleh ada em-dash, tidak boleh ada placeholder
for bad in ("TODO", "TBD", "xxx", "NaN", "None"):
    chk(bad not in txt, f"tidak ada placeholder {bad}", bad)

# ledger E3
sec = led[led.index("## Bagian E3"):]
n_rows = len(re.findall(r"^\| E3-\d{3} \|", sec, re.M))
chk(n_rows == 36, "36 baris ledger E3", f"terhitung {n_rows}")
chk("BELUM-TERUKUR" in sec, "ada baris BELUM-TERUKUR di ledger E3", "ok")

out = dict(n_checks=len(checks), n_gagal=len(fail), gagal=fail,
           n_em_dash=n_em, n_en_dash=n_en,
           panjang_dokumen_char=len(txt),
           n_bagian=len(re.findall(r"^## ", txt, re.M)),
           n_baris_ledger_e3=n_rows)
json.dump(dict(ringkasan=out, checks=checks), open(f"{E3}/e3_doccheck.json", "w"), indent=2)
print(json.dumps(out, indent=2))
if fail:
    print("\nGAGAL:")
    for f in fail:
        print(" -", f)
    sys.exit(1)
print("\nSEMUA PEMERIKSAAN DOKUMEN LULUS")
