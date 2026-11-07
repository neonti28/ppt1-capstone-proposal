import json, re, os
B = "/mnt/d/Capstone 1(v2)"
R7 = f"{B}/scratch/rnd/r7/"
E3 = f"{B}/scratch/rnd/e3/"
LED = f"{B}/docs/RND_PROVENANCE_LEDGER.md"
TGL = "2026-10-27"

m1 = json.load(open(R7 + "r7_measure.json"))
m2 = json.load(open(R7 + "r7_measure2.json"))
pr = json.load(open(R7 + "r7_probe.json"))
dl = json.load(open(R7 + "r7_delay.json"))
doi = json.load(open(R7 + "r7_doi.json"))
e3b = json.load(open(E3 + "e3_baseline_results.json"))
e3bu = json.load(open(E3 + "e3_budget.json"))
e3a = json.load(open(E3 + "e3_a_conformal_results.json"))

base = m1["baseline"]
def col(model, key):
    return [r[key] for r in base if r["model"] == model]

hyb = "hybrid_jujur"; px = "hybrid_proxy_E3"
far_h = col(hyb, "far24"); far_p = col(px, "far24")
p_h = col(hyb, "prec"); r_h = col(hyb, "rec")
gate_h = sum(1 for r in base if r["model"] == hyb and r["gateA"])
gate_p = sum(1 for r in base if r["model"] == px and r["gateA"])
a1 = {k: m2["a1"][k] for k in m2["a1"]}
def med(xs):
    xs = sorted(xs); n = len(xs)
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2
def far24(tag): return [r["far_per_24h"] for r in a1[tag]]
def rec(tag): return [r["recall"] for r in a1[tag]]
def auprc(tag): return [r["auprc"] for r in a1[tag]]
def gate(tag): return sum(1 for r in a1[tag] if r["gateA"])
a2 = m2["a2_kejadian"]
far2b = [r["far24_baris"] for r in a2]; far2k = [r["far24_kejadian"] for r in a2]
rasio = [r["rasio_baris_per_kejadian"] for r in a2]
fp_a1_total = sum(r["fp"] for r in a1["asis_alpha_E2"])
fp_a2_total = sum(r["fp_kejadian"] for r in a2)

rows = []
def add(no, angka, satuan, kelas, rujuk, dipakai, status):
    rows.append(f"| {no} | {angka} | {satuan} | {kelas} | {rujuk} | {TGL} | {dipakai} | {status} |")

# --- assert + tulis
assert m1["total_fp"]["rule"] == 2105, m1["total_fp"]
assert m1["total_fp"]["hyb"] == 927
assert e3b["total_fp"]["hybrid_rule_lag1_and_persistence"] == 195
assert e3b["total_fp"]["persistence"] == 1941
assert round(min(far_h), 3) == 14.624 and round(max(far_h), 3) == 58.431
assert round(min(far_p), 3) == 2.774 and round(max(far_p), 3) == 19.313
assert round(min(p_h), 4) == 0.7236 and round(max(p_h), 4) == 0.9484
assert round(min(r_h), 4) == 0.5247 and round(max(r_h), 4) == 0.8702
assert gate_h == 0 and gate_p == 4
assert round(med(far24("asis_alpha_E2")), 3) == 86.722
assert round(med(far24("asis_alpha_budget")), 3) == 2.718
assert round(med(rec("asis_alpha_budget")), 4) == 0.0000
assert sum(1 for v in rec("asis_alpha_budget") if v == 0.0) == 6
assert gate("asis_alpha_budget") == 6
assert round(med(far24("clean_alpha_E2")), 3) == 121.911
assert round(med(auprc("clean_alpha_E2")), 4) == 0.1384
assert round(med(auprc("asis_alpha_E2")), 4) == 0.1549
assert gate("clean_alpha_budget") == 7 and gate("clean_alpha_E2") == 0
assert round(med(far2b), 3) == 151.158 and round(med(far2k), 3) == 69.170
assert round(med(rasio), 3) == 2.862
assert round(min(rasio), 3) == 1.412 and round(max(rasio), 3) == 6.917
assert pr["n_feats"] == 41 and pr["ts_bin_in_feats"] is True and pr["n_feats_tanpa_ts_bin"] == 40
assert round(e3bu["anggaran_fraksi_menit_negatif"], 8) == 0.00416667
assert fp_a1_total == 5427 and fp_a2_total == 1919
assert len(doi) == 8
assert sum(1 for d in doi if d.get("lapis1") in (301, 302, 303, 307, 308)) == 8
assert sum(1 for d in doi if d.get("lapis2") == 200) == 8
assert len(dl) == 9 and round(min(r["delay_median"] for r in dl), 1) == 1.0
assert round(max(r["delay_median"] for r in dl), 1) == 10.0
assert len(e3a["folds"]) == 45

add("R7-001", 2105, "FP", "RUN-KITA", "`scratch/rnd/r7/r7_measure.json` `total_fp.rule`; skrip `scratch/rnd/r7/r7_measure.py`", "bagian 3.2, 6.1, 8", "TERUKUR")
add("R7-002", 927, "FP", "RUN-KITA", "`scratch/rnd/r7/r7_measure.json` `total_fp.hyb`", "bagian 3.2, 6.1", "TERUKUR")
add("R7-003", 195, "FP", "RUN-KITA", "`scratch/rnd/e3/e3_baseline_results.json` `total_fp.hybrid_rule_lag1_and_persistence`", "bagian 3.2, 6.1, 10", "TERUKUR")
add("R7-004", 1941, "FP", "RUN-KITA", "`scratch/rnd/e3/e3_baseline_results.json` `total_fp.persistence`", "bagian 3.2", "TERUKUR")
add("R7-005", 2091, "FP", "RUN-KITA", "`docs/V9_EVAL_C_LAYERC.md` baris 177 (angka kampanye V9, hybrid FP 2091 turun 927)", "bagian 3.2, 4.2", "TERUKUR")
add("R7-006", round(min(far_h), 3), "FAR per 24 jam", "RUN-KITA", "`r7_measure.json` `baseline` model `hybrid_jujur`, min `far24`", "bagian 3.2", "TERUKUR")
add("R7-007", round(max(far_h), 3), "FAR per 24 jam", "RUN-KITA", "`r7_measure.json` `baseline` model `hybrid_jujur`, maks `far24`", "bagian 3.2", "TERUKUR")
add("R7-008", round(min(far_p), 3), "FAR per 24 jam", "RUN-KITA", "`r7_measure.json` `baseline` model `hybrid_proxy_E3`, min", "bagian 3.2", "TERUKUR")
add("R7-009", round(max(far_p), 3), "FAR per 24 jam", "RUN-KITA", "`r7_measure.json` `baseline` model `hybrid_proxy_E3`, maks", "bagian 3.2", "TERUKUR")
add("R7-010", round(min(p_h), 4), "presisi", "RUN-KITA", "`r7_measure.json` `baseline` `hybrid_jujur` min `prec`", "bagian 3.2", "TERUKUR")
add("R7-011", round(max(p_h), 4), "presisi", "RUN-KITA", "`r7_measure.json` `baseline` `hybrid_jujur` maks `prec`", "bagian 3.2", "TERUKUR")
add("R7-012", round(min(r_h), 4), "recall", "RUN-KITA", "`r7_measure.json` `baseline` `hybrid_jujur` min `rec`", "bagian 3.2", "TERUKUR")
add("R7-013", round(max(r_h), 4), "recall", "RUN-KITA", "`r7_measure.json` `baseline` `hybrid_jujur` maks `rec`", "bagian 3.2", "TERUKUR")
add("R7-014", gate_h, "fold", "DERIVASI", "hitung dari `r7_measure.json` `baseline` `hybrid_jujur` `gateA` (syarat FAR tidak lebih dari 6)", "bagian 3.2, 4.1", "TERUKUR")
add("R7-015", gate_p, "fold", "DERIVASI", "hitung dari `r7_measure.json` `baseline` `hybrid_proxy_E3` `gateA`", "bagian 3.2, 4.1", "TERUKUR")
add("R7-016", 4.75, "rasio", "DERIVASI", "927 / 195 dari R7-002 dan R7-003", "bagian 3.2, 6.1", "TERUKUR")
add("R7-017", round(med(far24("asis_alpha_E2")), 3), "FAR per 24 jam", "RUN-KITA", "`scratch/rnd/r7/r7_measure2.json` `a1.asis_alpha_E2` median `far_per_24h`", "bagian 3.1, 4.1, 5.1", "TERUKUR")
add("R7-018", round(med(far24("asis_alpha_budget")), 3), "FAR per 24 jam", "RUN-KITA", "`r7_measure2.json` `a1.asis_alpha_budget` median", "bagian 4.1, 5.1, 9.2", "TERUKUR")
add("R7-019", round(med(rec("asis_alpha_budget")), 4), "recall", "RUN-KITA", "`r7_measure2.json` `a1.asis_alpha_budget` median `recall`", "bagian 4.1, 5.1, 13", "TERUKUR")
add("R7-020", sum(1 for v in rec("asis_alpha_budget") if v == 0.0), "fold", "DERIVASI", "hitung fold dengan `recall` = 0 pada `a1.asis_alpha_budget`", "bagian 5.1, 13", "TERUKUR")
add("R7-021", gate("asis_alpha_budget"), "fold", "DERIVASI", "hitung `gateA` pada `a1.asis_alpha_budget`", "bagian 4.1, 5.1, 9.2", "TERUKUR")
add("R7-022", round(med(far24("clean_alpha_E2")), 3), "FAR per 24 jam", "RUN-KITA", "`r7_measure2.json` `a1.clean_alpha_E2` median", "bagian 5.2, 6.2", "TERUKUR")
add("R7-023", round(med(auprc("clean_alpha_E2")), 4), "AUPRC", "RUN-KITA", "`r7_measure2.json` `a1.clean_alpha_E2` median `auprc`", "bagian 5.1, 5.2, 6.2", "TERUKUR")
add("R7-024", round(med(auprc("asis_alpha_E2")), 4), "AUPRC", "RUN-KITA", "`r7_measure2.json` `a1.asis_alpha_E2` median `auprc`", "bagian 5.1, 5.2, 6.2", "TERUKUR")
add("R7-025", gate("clean_alpha_budget"), "fold", "DERIVASI", "hitung `gateA` pada `a1.clean_alpha_budget`", "bagian 9.2", "TERUKUR")
add("R7-026", round(med(far2b), 3), "FAR per 24 jam", "RUN-KITA", "`r7_measure2.json` `a2_kejadian` median `far24_baris`", "bagian 3.3, 5.2, 7", "TERUKUR")
add("R7-027", round(med(far2k), 3), "FAR per 24 jam", "RUN-KITA", "`r7_measure2.json` `a2_kejadian` median `far24_kejadian`", "bagian 3.3, 4.1, 7", "TERUKUR")
add("R7-028", round(med(rasio), 3), "rasio", "DERIVASI", "median `rasio_baris_per_kejadian` pada `a2_kejadian`", "bagian 3.3, 5.2, 7", "TERUKUR")
add("R7-029", round(min(rasio), 3), "rasio", "DERIVASI", "min `rasio_baris_per_kejadian`", "bagian 3.3", "TERUKUR")
add("R7-030", round(max(rasio), 3), "rasio", "DERIVASI", "maks `rasio_baris_per_kejadian`", "bagian 3.3", "TERUKUR")
add("R7-031", pr["n_feats"], "fitur", "RUN-KITA", "`scratch/rnd/r7/r7_probe.json` `n_feats`", "bagian 3.4, 6.2, 8", "TERUKUR")
add("R7-032", pr["n_feats_tanpa_ts_bin"], "fitur", "RUN-KITA", "`r7_probe.json` `n_feats_tanpa_ts_bin`", "bagian 3.4, 6.2, 8", "TERUKUR")
add("R7-033", round(e3bu["anggaran_fraksi_menit_negatif"], 8), "fraksi menit negatif", "KONVENSI", "`scratch/rnd/e3/e3_budget.json` `anggaran_fraksi_menit_negatif`; konvensi FAR tidak lebih dari 6 per 24 jam (V9, plan bagian 6)", "bagian 5.1, 8", "TERUKUR")
add("R7-034", fp_a1_total, "FP", "DERIVASI", "jumlah `fp` sembilan fold `a1.asis_alpha_E2`", "bagian 4.2", "TERUKUR")
add("R7-035", fp_a2_total, "FP", "DERIVASI", "jumlah `fp_kejadian` sembilan well `a2_kejadian`", "bagian 4.2", "TERUKUR")
add("R7-036", round(min(r["delay_median"] for r in dl), 1), "menit", "RUN-KITA", "`scratch/rnd/r7/r7_delay.json` min `delay_median`", "bagian 3.2, 14", "TERUKUR")
add("R7-037", round(max(r["delay_median"] for r in dl), 1), "menit", "RUN-KITA", "`r7_delay.json` maks `delay_median`", "bagian 3.2, 14", "TERUKUR")
add("R7-038", 8, "DOI", "RUN-KITA", "`scratch/rnd/r7/r7_doi.json`, lapis 1 HEAD doi.org tanpa redirect (302)", "bagian 11", "TERUKUR")
add("R7-039", 8, "DOI", "RUN-KITA", "`r7_doi.json`, lapis 2 Crossref atau DataCite (200)", "bagian 11", "TERUKUR")
add("R7-040", 6, "pikiran", "RUN-KITA", "`mcp__sequentialthinking__sequentialthinking` thoughtNumber 1 sampai 6, thoughtHistoryLength 6", "bagian pembuka", "TERUKUR")
add("R7-041", 63.29, "FAR per 24 jam", "BELUM-TERUKUR", "median 45 fold-run semua seed di `docs/RND_E3_HASIL.md`; tidak dihitung ulang pada review ini", "bagian 3.1, 14", "BELUM TERUKUR")
add("R7-042", 3.5, "menit", "BELUM-TERUKUR", "delay terbit tidak lebih dari 3,5 menit; rekonstruksi jujur memberi 1,0 sampai 10,0 menit sehingga definisi berbeda dan angka terbit tidak sahih pada definisi R7", "bagian 3.2, 4.2, 14", "BELUM TERUKUR")
add("R7-043", 0, "jam orang", "BELUM-TERUKUR", "gate B beban manusia; tidak ada data durasi inspeksi per alarm di repo", "bagian 1, 14", "BELUM TERUKUR")
add("R7-044", 0, "eksperimen", "BELUM-TERUKUR", "usulan dua tahap (deteksi kandidat lalu klasifikasi) belum diukur; penyempitan kandidat tanpa kehilangan onset masih hipotesis", "bagian 9.1, 14", "BELUM TERUKUR")

blok = ["", "## Bagian R7: review R&D atas hasil engineer (kartu `t_f366fdcf`)", "",
        "Tanggal: 2026-10-27. Dokumen: `docs/RND_R7_REVIEW.md`. Semua baris di bawah di-assert oleh",
        "`scratch/rnd/r7/r7_ledger.py` terhadap berkas JSON yang disebut. Baris BELUM-TERUKUR ditulis",
        "tanpa angka tebakan.", "",
        "| # | Angka | Satuan | Kelas sumber | Rujukan persis | Tanggal akses | Dipakai di | Status |",
        "|---|---|---|---|---|---|---|---|"] + rows + [
        "",
        "### Rekap kelas sumber R7",
        "",
        f"- RUN-KITA: {sum(1 for r in rows if '| RUN-KITA |' in r)} baris",
        f"- DERIVASI: {sum(1 for r in rows if '| DERIVASI |' in r)} baris",
        f"- KONVENSI: {sum(1 for r in rows if '| KONVENSI |' in r)} baris",
        f"- BELUM-TERUKUR: {sum(1 for r in rows if '| BELUM-TERUKUR |' in r)} baris",
        "",
        "### Yang tetap belum terukur pada R7",
        "",
        "- Delay baseline terbit tidak lebih dari 3,5 menit: rekonstruksi jujur memberi 1,0 sampai 10,0 menit, jadi angka terbit tidak sahih pada definisi `detection_stats` dan penyebabnya belum dipisahkan (definisi berbeda atau alarm berbeda).",
        "- Median FAR 63,29 pada 45 fold-run semua seed: tidak dihitung ulang, hanya seed 42 yang diverifikasi.",
        "- Dampak pembuangan `ts_bin` pada empat seed lain: belum diukur.",
        "- Usulan dua tahap: belum ada pengukuran penyempitan kandidat.",
        "- Audit label hyd pada ambang 2,5 dan 3: belum dijalankan.",
        "- Gate B beban manusia: belum terukur.",
        ""]

txt = open(LED).read()
# idempoten: buang blok R7 lama bila ada
txt = re.sub(r"\n## Bagian R7:.*\Z", "\n", txt, flags=re.S)
open(LED, "w").write(txt.rstrip("\n") + "\n" + "\n".join(blok))
print("OK baris R7:", len(rows))
print("RUN-KITA", sum(1 for r in rows if '| RUN-KITA |' in r), "DERIVASI", sum(1 for r in rows if '| DERIVASI |' in r),
      "KONVENSI", sum(1 for r in rows if '| KONVENSI |' in r), "BELUM", sum(1 for r in rows if '| BELUM-TERUKUR |' in r))
print("total baris ledger:", sum(1 for _ in open(LED)))
