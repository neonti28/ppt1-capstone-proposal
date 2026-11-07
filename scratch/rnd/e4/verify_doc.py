import json
import re

base = "/mnt/d/Capstone 1(v2)"
S = f"{base}/scratch/rnd/e4"
DOC = f"{base}/docs/RND_E4_PERBAIKAN.md"
doc = open(DOC).read()

a = json.load(open(f"{S}/e4_summary_run1.json"))
b = json.load(open(f"{S}/e4_summary.json"))
ba = json.load(open(f"{S}/e4_beforeafter.json"))
gd = json.load(open(f"{S}/e4_gate_decomp.json"))
au = json.load(open(f"{S}/e4_audit_label.json"))
bj = json.load(open(f"{S}/e4_baseline.json"))

# hitung jumlah field ringkas yang benar-benar dibandingkan
n_field = 0
for k in a["ringkas"]:
    if k in b["ringkas"]:
        n_field += len(set(a["ringkas"][k]) & set(b["ringkas"][k]))
print("JUMLAH FIELD RINGKASAN DIBANDINGKAN =", n_field)
print("doc menyebut '96 angka ringkasan':", "96 angka ringkasan" in doc)
if n_field != 96 and "96 angka ringkasan" in doc:
    print("!! DOKUMEN HARUS DIPERBAIKI: 96 ->", n_field)

# cek setiap angka kunci muncul di dokumen dalam format koma desimal Indonesia
def id_fmt(x, dec=4):
    return f"{x:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")

checks = []
def want(val, dec=4, label=""):
    s = id_fmt(float(val), dec)
    checks.append((label, s, s in doc))

h = ba["hybrid_rule_persistence"]
want(h["far24_baris"], 3, "hybrid FAR baris")
want(h["far24_kej"], 4, "hybrid FAR kejadian")
want(h["far24_kal"], 4, "hybrid FAR kalender")
want(h["recall"], 4, "hybrid recall")
want(h["precision"], 4, "hybrid presisi")
p = ba["persistence"]
want(p["far24_baris"], 3, "pers FAR baris"); want(p["far24_kej"], 4, "pers FAR kej")
want(p["far24_kal"], 4, "pers FAR kal"); want(p["recall"], 4, "pers R"); want(p["precision"], 4, "pers P")
r = ba["rule_t0m1"]
want(r["far24_baris"], 3, "rule FAR baris"); want(r["far24_kej"], 4, "rule FAR kej")
want(r["far24_kal"], 4, "rule FAR kal"); want(r["recall"], 4, "rule R"); want(r["precision"], 4, "rule P")
a1e = ba["A1_alpha_E2_lama_seed42"]
want(a1e["far24_baris"], 4, "A1 E2 FAR baris"); want(a1e["far24_kej"], 4, "A1 E2 FAR kej")
want(a1e["far24_kal"], 4, "A1 E2 FAR kal"); want(a1e["recall"], 4, "A1 E2 R"); want(a1e["precision"], 4, "A1 E2 P")
a1b = ba["A1_alpha_anggaran_seed42"]
want(a1b["precision"], 4, "A1 anggaran P")
ho = ba["H_or_hybrid_ML_seed42"]
want(ho["far24_baris"], 4, "H_or FAR baris"); want(ho["far24_kej"], 4, "H_or FAR kej")
want(ho["far24_kal"], 4, "H_or FAR kal"); want(ho["precision"], 4, "H_or P")
hm = ba["H_and_hybrid_ML_seed42"]
want(hm["precision"], 4, "H_and P")
px = ba["hybrid_proxy_E3"]
want(px["far24_baris"], 3, "proxy FAR baris"); want(px["far24_kej"], 4, "proxy FAR kej")
want(px["far24_kal"], 4, "proxy FAR kal"); want(px["precision"], 4, "proxy P")

for thr in ("2.0", "2.5", "3.0"):
    x = au["agregat"][f"thr_{thr}"]
    want(x["laju"], 6, f"laju z{thr}")
    want(x["retensi_vs_2"], 4, f"retensi z{thr}")
    s = id_fmt(float(x["onset_total"]), 0)
    checks.append((f"onset z{thr}", s, s in doc))
s = id_fmt(float(au["agregat"]["thr_2.0"]["total_pos"]), 0)
checks.append(("total_pos z2", s, s in doc))
s = id_fmt(float(au["agregat"]["thr_2.0"]["total_obs"]), 0)
checks.append(("total_obs", s, s in doc))
s = id_fmt(float(au["agregat"]["thr_2.5"]["total_pos"]), 0)
checks.append(("total_pos z2.5", s, s in doc))
s = id_fmt(float(au["agregat"]["thr_3.0"]["total_pos"]), 0)
checks.append(("total_pos z3", s, s in doc))

cak = {x["test_well"]: x["cakupan"]["fraksi"] for x in bj["folds"] if x.get("model") == "hybrid_rule_persistence"}
checks.append(("cakupan min", id_fmt(min(cak.values()), 4), id_fmt(min(cak.values()), 4) in doc))
checks.append(("cakupan max", id_fmt(max(cak.values()), 4), id_fmt(max(cak.values()), 4) in doc))
checks.append(("rasio 39,36", "39,36", "39,36" in doc))

bad = [c for c in checks if not c[2]]
print(f"\nCEK ANGKA: {len(checks)-len(bad)}/{len(checks)} cocok")
for label, s, ok in bad:
    print("  TIDAK ADA DI DOKUMEN:", label, "=", s)

# konsistensi klaim hitungan fold
print("\nCEK KLAIM FOLD:")
g = gd["hybrid_rule_persistence"]
pairs = [
    ("hybrid FAR<=6 kejadian 9 dari 9", g["far_ok_kejadian"] == 9 and "9 dari 9 fold" in doc),
    ("hybrid recall 9 dari 9", g["recall_ok"] == 9),
    ("hybrid cakupan 1 dari 9", g["cakupan_ok"] == 1),
    ("H_and gate lama 18 dari 18", ba["H_and_hybrid_ML_pooled"]["gateA_lama"] == 18),
    ("H_and tanpa alarm 13 dari 18", gd["H_and_hybrid_ML"]["fold_tanpa_alarm"] == 13),
    ("A1 anggaran tanpa alarm 12 dari 18", gd["A1_alpha_anggaran"]["fold_tanpa_alarm"] == 12),
]
for label, ok in pairs:
    print(f"  {'OK ' if ok else 'SALAH'} {label}")
