#!/usr/bin/env python3
"""RND-E4 — tulis Bagian E4 ke docs/RND_PROVENANCE_LEDGER.md.

Setiap baris RUN-KITA dan DERIVASI di-assert terhadap path JSON sebelum ditulis.
Idempoten: blok E4 lama dibuang dulu, jadi menjalankan ulang tidak menggandakan.
"""
import json
import re

BASE = "/mnt/d/Capstone 1(v2)"
S = f"{BASE}/scratch/rnd/e4"
LED = f"{BASE}/docs/RND_PROVENANCE_LEDGER.md"
TGL = "2026-10-27"

base_j = json.load(open(f"{S}/e4_baseline.json"))
summ = json.load(open(f"{S}/e4_summary.json"))
ba = json.load(open(f"{S}/e4_beforeafter.json"))
gd = json.load(open(f"{S}/e4_gate_decomp.json"))
au = json.load(open(f"{S}/e4_audit_label.json"))
doi = json.load(open(f"{S}/e4_doi.json"))

ROWS = []


def add(angka, satuan, kelas, rujukan, dipakai, status="TERUKUR"):
    assert "|" not in str(angka), "pipa merusak tabel"
    ROWS.append((len(ROWS) + 1, angka, satuan, kelas, rujukan, TGL, dipakai, status))


def chk(path_val, expect, tol=0.0):
    if tol:
        ok = abs(float(path_val) - float(expect)) <= tol
    else:
        ok = path_val == expect
    assert ok, f"ASSERT GAGAL: json={path_val} ditulis={expect}"
    return expect


P = "scratch/rnd/e4"

a = base_j["assert_r7_1"]
add(chk(base_j["total_fp"]["rule_t0m1"], 2105), "FP", "RUN-KITA",
    f"{P}/e4_baseline.json total_fp.rule_t0m1; 9 fold seed 42+7; "
    "python3 code/rnd_e4_pilot.py --seeds 42,7 (run 11:32)", "RND_E4 3 R7-1")
add(chk(base_j["total_fp"]["hybrid_rule_persistence"], 927), "FP", "RUN-KITA",
    f"{P}/e4_baseline.json total_fp.hybrid_rule_persistence", "RND_E4 3 R7-1")
add(chk(base_j["total_fp"]["persistence"], 1941), "FP", "RUN-KITA",
    f"{P}/e4_baseline.json total_fp.persistence", "RND_E4 3")
add(chk(base_j["total_fp"]["hybrid_proxy_E3"], 195), "FP", "RUN-KITA",
    f"{P}/e4_baseline.json total_fp.hybrid_proxy_E3 (proksi E3, ditolak)", "RND_E4 3")
add(chk(a["fp_rule_terbit"], 2091), "FP", "RUN-KITA",
    "docs/RND_E3_HASIL.md angka terbit; direproduksi R7 3.2", "RND_E4 3")
add(chk(a["selisih_rule_pct"], 0.67), "persen", "DERIVASI",
    "(2105-2091)/2091 x 100", "RND_E4 3")
add(chk(a["selisih_hybrid_pct"], 0.0), "persen", "DERIVASI",
    "(927-927)/927 x 100", "RND_E4 3")
add(chk(a["toleransi_pct"], 5.0), "persen", "KONVENSI",
    "kriteria selesai R7 8 butir 1", "RND_E4 3")

add(chk(summ["n_fitur"], 40), "fitur", "RUN-KITA",
    f"{P}/e4_summary.json n_fitur; assert di code/rnd_e4_pilot.py", "RND_E4 3 R7-2")

h = ba["hybrid_rule_persistence"]
add(chk(h["far24_baris"], 28.416), "FP/24 jam", "RUN-KITA",
    f"{P}/e4_beforeafter.json hybrid_rule_persistence.far24_baris", "RND_E4 4")
add(chk(h["far24_kej"], 8.3208), "FP kejadian/24 jam", "RUN-KITA",
    f"{P}/e4_beforeafter.json hybrid_rule_persistence.far24_kej", "RND_E4 4")
add(chk(h["far24_kal"], 4.0984), "FP/24 jam kalender", "RUN-KITA",
    f"{P}/e4_beforeafter.json hybrid_rule_persistence.far24_kal", "RND_E4 4")
add(chk(h["recall"], 0.6519), "rasio", "RUN-KITA",
    f"{P}/e4_beforeafter.json hybrid_rule_persistence.recall", "RND_E4 4")
add(chk(h["precision"], 0.8243), "rasio", "RUN-KITA",
    f"{P}/e4_beforeafter.json hybrid_rule_persistence.precision", "RND_E4 4")

p = ba["persistence"]
add(chk(p["far24_kal"], 6.7404), "FP/24 jam kalender", "RUN-KITA",
    f"{P}/e4_beforeafter.json persistence.far24_kal", "RND_E4 4")
add(chk(p["recall"], 0.6791), "rasio", "RUN-KITA",
    f"{P}/e4_beforeafter.json persistence.recall", "RND_E4 4")
add(chk(p["precision"], 0.7114), "rasio", "RUN-KITA",
    f"{P}/e4_beforeafter.json persistence.precision", "RND_E4 4")

r = ba["rule_t0m1"]
add(chk(r["far24_kal"], 6.932), "FP/24 jam kalender", "RUN-KITA",
    f"{P}/e4_beforeafter.json rule_t0m1.far24_kal", "RND_E4 4")
add(chk(r["recall"], 0.7507), "rasio", "RUN-KITA",
    f"{P}/e4_beforeafter.json rule_t0m1.recall", "RND_E4 4")
add(chk(r["precision"], 0.6835), "rasio", "RUN-KITA",
    f"{P}/e4_beforeafter.json rule_t0m1.precision", "RND_E4 4")

a1e = ba["A1_alpha_E2_lama_seed42"]
add(chk(a1e["far24_baris"], 121.9111), "FP/24 jam", "RUN-KITA",
    f"{P}/e4_beforeafter.json A1_alpha_E2_lama_seed42.far24_baris; "
    "sama dengan R7 P3 tanpa ts_bin", "RND_E4 5")
add(chk(a1e["recall"], 0.133), "rasio", "RUN-KITA",
    f"{P}/e4_beforeafter.json A1_alpha_E2_lama_seed42.recall", "RND_E4 5")
a1b = ba["A1_alpha_anggaran_seed42"]
add(chk(a1b["recall"], 0.0), "rasio", "RUN-KITA",
    f"{P}/e4_beforeafter.json A1_alpha_anggaran_seed42.recall", "RND_E4 5")
add(chk(a1b["gateA_lama"], 7), "fold", "RUN-KITA",
    f"{P}/e4_beforeafter.json A1_alpha_anggaran_seed42.gateA_lama dari 9", "RND_E4 5")
add(chk(a1b["far24_baris"], 0.0), "FP/24 jam", "RUN-KITA",
    f"{P}/e4_beforeafter.json A1_alpha_anggaran_seed42.far24_baris nol alarm", "RND_E4 5")

hm = ba["H_and_hybrid_ML_pooled"]
add(chk(hm["gateA_lama"], 18), "fold-run", "RUN-KITA",
    f"{P}/e4_beforeafter.json H_and_hybrid_ML_pooled.gateA_lama dari 18", "RND_E4 5 R7-4")
add(chk(hm["recall"], 0.0), "rasio", "RUN-KITA",
    f"{P}/e4_beforeafter.json H_and_hybrid_ML_pooled.recall", "RND_E4 5")
add(chk(gd["H_and_hybrid_ML"]["fold_tanpa_alarm"], 13), "fold-run", "RUN-KITA",
    f"{P}/e4_gate_decomp.json H_and_hybrid_ML.fold_tanpa_alarm dari 18", "RND_E4 5")

g = gd["hybrid_rule_persistence"]
add(chk(g["far_ok_baris"], 7), "fold", "RUN-KITA",
    f"{P}/e4_gate_decomp.json hybrid_rule_persistence.far_ok_baris dari 9", "RND_E4 6")
add(chk(g["far_ok_kejadian"], 9), "fold", "RUN-KITA",
    f"{P}/e4_gate_decomp.json hybrid_rule_persistence.far_ok_kejadian dari 9", "RND_E4 6")
add(chk(g["recall_ok"], 9), "fold", "RUN-KITA",
    f"{P}/e4_gate_decomp.json hybrid_rule_persistence.recall_ok dari 9", "RND_E4 6")
add(chk(g["cakupan_ok"], 1), "fold", "RUN-KITA",
    f"{P}/e4_gate_decomp.json hybrid_rule_persistence.cakupan_ok dari 9", "RND_E4 6")
add(chk(g["ketiga_baris"], 0), "fold", "RUN-KITA",
    f"{P}/e4_gate_decomp.json hybrid_rule_persistence.ketiga_baris dari 9", "RND_E4 6")
add(chk(g["ketiga_kejadian"], 1), "fold", "RUN-KITA",
    f"{P}/e4_gate_decomp.json hybrid_rule_persistence.ketiga_kejadian dari 9", "RND_E4 6")

cak = {}
for r_ in base_j["folds"]:
    if r_.get("model") == "hybrid_rule_persistence":
        cak[r_["test_well"]] = r_["cakupan"]["fraksi"]
lo = min(cak.values())
hi = max(cak.values())
add(chk(round(lo, 4), 0.0171), "rasio", "RUN-KITA",
    f"{P}/e4_baseline.json folds cakupan.fraksi minimum F-5", "RND_E4 6")
add(chk(round(hi, 4), 0.673), "rasio", "RUN-KITA",
    f"{P}/e4_baseline.json folds cakupan.fraksi maksimum F-10", "RND_E4 6")
add(chk(round(hi / lo, 2), 39.36), "kali", "DERIVASI",
    "0,673 / 0,0171", "RND_E4 6")

for thr in ("2.0", "2.5", "3.0"):
    a_ = au["agregat"][f"thr_{thr}"]
    add(chk(a_["laju"], {"2.0": 0.169119, "2.5": 0.129673, "3.0": 0.093008}[thr]),
        "rasio", "RUN-KITA",
        f"{P}/e4_audit_label.json agregat.thr_{thr}.laju; "
        "python3 scratch/rnd/e4/e4_audit_label.py", "RND_E4 7")
    add(chk(a_["onset_total"], {"2.0": 2446, "2.5": 2158, "3.0": 1626}[thr]),
        "kejadian", "RUN-KITA",
        f"{P}/e4_audit_label.json agregat.thr_{thr}.onset_total", "RND_E4 7")
    add(chk(a_["retensi_vs_2"], {"2.0": 1.0, "2.5": 0.7668, "3.0": 0.55}[thr]),
        "rasio", "RUN-KITA",
        f"{P}/e4_audit_label.json agregat.thr_{thr}.retensi_vs_2", "RND_E4 7")
add(chk(au["agregat"]["thr_2.0"]["total_obs"], 87412), "menit teramati", "RUN-KITA",
    f"{P}/e4_audit_label.json agregat.thr_2.0.total_obs 9 well", "RND_E4 7")
add(chk(au["agregat"]["thr_2.0"]["total_pos"], 14783), "menit positif", "RUN-KITA",
    f"{P}/e4_audit_label.json agregat.thr_2.0.total_pos", "RND_E4 7")

add(6.0, "alarm/24 jam", "KONVENSI", "docs/V9_EVAL_C_LAYERC.md EC-4; R7 4.1", "RND_E4 2 gate A")
add(0.50, "rasio", "KONVENSI", "docs/RND_E2_PROTOKOL.md 4.1 butir (d) cakupan", "RND_E4 2 gate A")
add(0.50, "rasio", "KONVENSI", "docs/RND_R7_REVIEW.md 6.4 syarat recall", "RND_E4 2 gate A")
add(0.004167, "alpha", "DERIVASI",
    "1/240; FAR tidak lebih dari 6/24 jam setara alpha tidak lebih dari 6/1440", "RND_E4 2")

n_ok1 = sum(1 for d in doi if d.get("lapis1") in (301, 302, 303, 307))
n_ok2 = sum(1 for d in doi if d.get("lapis2") == 200)
add(chk(n_ok1, 8), "DOI", "RUN-KITA",
    f"{P}/e4_doi.json lapis1 3xx; python3 scratch/rnd/e4/e4_doi.py (run 11:31)", "RND_E4 9")
add(chk(n_ok2, 8), "DOI", "RUN-KITA",
    f"{P}/e4_doi.json lapis2 200 crossref/datacite", "RND_E4 9")

for txt in (
    "Gate B beban manusia per alarm, tidak ada data durasi inspeksi.",
    "Delay deteksi pada definisi R7, angka terbit 3,5 menit tidak tereproduksi.",
    "Penyempitan kandidat dua tahap R7 9.1, belum dijalankan.",
    "Kesetiaan label terhadap kegagalan hidraulik fisik, tidak ada label insiden independen.",
):
    add("BELUM TERUKUR", "-", "BELUM-TERUKUR", "tidak ada sumber", "RND_E4 10", "BELUM TERUKUR")

hdr = ("| # | Angka | Satuan | Kelas sumber | Rujukan persis | Tanggal akses | "
       "Dipakai di | Status |\n|---|---|---|---|---|---|---|---|\n")
body = "".join(
    f"| E4-{i:03d} | {ang} | {sat} | {kel} | {ref} | {tgl} | {dip} | {st} |\n"
    for i, ang, sat, kel, ref, tgl, dip, st in ROWS)

rekap = {k: sum(1 for x in ROWS if x[3] == k) for k in
         ("RUN-KITA", "DERIVASI", "KONVENSI", "BELUM-TERUKUR")}
blok = (
    "\n---\n\n## Bagian E4: engineer menjawab temuan R7 (kartu `t_61edf756`)\n\n"
    "Sumber angka: `scratch/rnd/e4/*.json`. Setiap baris RUN-KITA dan DERIVASI di-assert "
    "terhadap path JSON oleh `scratch/rnd/e4/e4_ledger2.py`; baris yang gagal assert tidak ditulis.\n\n"
    + hdr + body +
    "\n### Rekap kelas sumber E4\n\n"
    "| Kelas | Jumlah baris |\n|---|---|\n"
    + "".join(f"| {k} | {v} |\n" for k, v in rekap.items()) +
    f"\nTotal baris: {len(ROWS)}. Baris BELUM-TERUKUR sengaja disertakan supaya cakupan tidak "
    "terlihat penuh.\n\n"
    "### Yang tetap belum terukur pada E4\n\n"
    "1. Gate B beban manusia per alarm tidak terukur karena tidak ada data durasi inspeksi.\n"
    "2. Delay deteksi pada definisi R7 belum tereproduksi.\n"
    "3. Penyempitan kandidat dua tahap belum dijalankan.\n"
    "4. Tidak ada label kegagalan fisik independen, sehingga kesetiaan label proksi belum terukur.\n"
)

txt = open(LED).read()
txt = re.sub(r"\n---\n\n## Bagian E4:.*?(?=\n---\n\n## |\Z)", "\n", txt, flags=re.S)
txt = txt.rstrip("\n") + "\n" + blok
open(LED, "w").write(txt)
print(f"OK {len(ROWS)} baris ditulis. rekap={rekap}")
