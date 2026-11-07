#!/usr/bin/env python3
"""RND-E3 — generator baris ledger provenance untuk dokumen hasil pilot.

Setiap baris WAJIB lolos assert terhadap path JSON sebelum ditulis. Kalau assert
gagal, tidak ada satu baris pun yang ditulis. Format mengikuti bagian E2 (8 kolom).

Idempoten: blok "## Bagian E3" lama dibuang lebih dulu.

Keluaran: docs/RND_PROVENANCE_LEDGER.md (bagian E3), scratch/rnd/e3/e3_ledger.json
"""
import json, os, sys

BASE = "/mnt/d/Capstone 1(v2)"
E3 = f"{BASE}/scratch/rnd/e3"
LEDGER = f"{BASE}/docs/RND_PROVENANCE_LEDGER.md"
TGL = "2026-10-27"
HEAD = "## Bagian E3: eksekusi pilot pada hyd K-i (kartu `t_13309129`)"


def L(n):
    return json.load(open(f"{E3}/{n}"))


A1, A1B, A2, BL = L("e3_a_conformal_results.json"), L("e3_a1b_lag_results.json"), \
    L("e3_b_cusum_results.json"), L("e3_baseline_results.json")
SUM, CAK, VER, BUD, DOI = L("e3_run_summary.json"), L("e3_cakupan.json"), \
    L("e3_verify.json"), L("e3_budget.json"), L("e3_doi.json")

rows = []
err = []


def add(no, angka, satuan, kelas, rujukan, dipakai, status, cek):
    try:
        ok = cek()
    except Exception as e:                       # noqa: BLE001
        ok = False
        rujukan = f"{rujukan} [assert error: {e}]"
    if not ok:
        err.append(no)
        return
    rows.append((no, angka, satuan, kelas, rujukan, TGL, dipakai, status))


def between(vals, lo, hi, nd=4):
    return lambda: all(round(lo, nd) <= round(float(v), nd) <= round(hi, nd) for v in vals)


fw = lambda name, sub=None: f"`scratch/rnd/e3/{name}`" + (f" `{sub}`" if sub else "")

a1_s42 = [r for r in A1["folds"] if r["seed"] == 42]
far_a1 = [r["far_per_24h"] for r in a1_s42]
b_pers = [r for r in BL["folds"] if r["model"] == "persistence"]
b_hyb = [r for r in BL["folds"] if r["model"] == "hybrid_rule_lag1_and_persistence"]
a2r = A2["varian"]["reset"]["folds"]
a2n = A2["varian"]["tanpa_reset"]["folds"]
cak_fr = [c["fraksi"] for c in CAK["per_fold"]]

add("E3-001", 52509, "baris", "RUN-KITA", fw("e3_verify.json", "`v6_total.n_baris`"),
    "bagian 2", "TERUKUR", lambda: VER["v6_total"]["n_baris"] == 52509)
add("E3-002", 9, "well/fold", "RUN-KITA", fw("e3_run_summary.json", "`n_folds`"),
    "bagian 2, 4", "TERUKUR", lambda: SUM["n_folds"] == 9)
add("E3-003", 41, "fitur A1", "RUN-KITA", fw("e3_verify.json", "`v5_audit_fitur.n_fitur_A1`"),
    "bagian 3.1", "TERUKUR", lambda: VER["v5_audit_fitur"]["n_fitur_A1"] == 41)
add("E3-004", 43, "fitur A1b", "RUN-KITA", fw("e3_verify.json", "`v5_audit_fitur.n_fitur_A1b`"),
    "bagian 3.2", "TERUKUR", lambda: VER["v5_audit_fitur"]["n_fitur_A1b"] == 43)
add("E3-005", 233.7, "detik", "RUN-KITA", fw("e3_run_summary.json", "`elapsed_s`"),
    "bagian 2, 6", "TERUKUR", lambda: SUM["elapsed_s"] == 233.7)

add("E3-006", 1941, "FP", "RUN-KITA", fw("e3_baseline_results.json", "`total_fp.persistence`"),
    "bagian 4.1", "TERUKUR", lambda: BL["total_fp"]["persistence"] == 1941)
add("E3-007", 195, "FP", "RUN-KITA",
    fw("e3_baseline_results.json", "`total_fp.hybrid_rule_lag1_and_persistence`"),
    "bagian 4.1", "TERUKUR", lambda: BL["total_fp"]["hybrid_rule_lag1_and_persistence"] == 195)
add("E3-008", "32,17 sampai 109,69", "FP per 24 jam", "DERIVASI",
    fw("e3_baseline_results.json", "`folds[].far_per_24h` model persistence") +
    " ; FAR = FP/(n_neg/60)*24", "bagian 4.1", "TERVERIFIKASI (assert V1, deviasi 0,0)",
    between([r["far_per_24h"] for r in b_pers], 32.1710, 109.6943))
add("E3-009", "2,77 sampai 19,31", "FP per 24 jam", "DERIVASI",
    fw("e3_baseline_results.json", "`folds[].far_per_24h` model hybrid proxy") +
    " ; FAR = FP/(n_neg/60)*24", "bagian 4.1", "TERVERIFIKASI (assert V1)",
    between([r["far_per_24h"] for r in b_hyb], 2.7736, 19.3127))
add("E3-010", "0 dari 9", "fold lulus gate A", "DERIVASI",
    "hitung ulang `e3_rnd_e3_verify` kunci `v3b_gate_A_baseline_hitung_manual.persistence`"
    if False else fw("e3_verify.json", "`v3b_gate_A_baseline_hitung_manual.persistence`"),
    "bagian 4.1, 5", "TERVERIFIKASI",
    lambda: VER["v3b_gate_A_baseline_hitung_manual"]["persistence"] == [])
add("E3-011", "4 dari 9", "fold lulus gate A", "DERIVASI",
    fw("e3_verify.json", "`v3b_gate_A_baseline_hitung_manual.hybrid_proxy`") +
    " = F-10, F-14, F-15A, F-5", "bagian 4.1, 5", "TERVERIFIKASI",
    lambda: sorted(VER["v3b_gate_A_baseline_hitung_manual"]["hybrid_proxy"]) ==
    sorted(["F-10", "F-14", "F-15A", "F-5"]))

add("E3-012", "0,00 sampai 543,50", "FP per 24 jam", "DERIVASI",
    fw("e3_a_conformal_results.json", "`folds[]` seed 42 `far_per_24h`") +
    " ; median 86,72", "bagian 4.2, 5", "TERVERIFIKASI (assert V1)",
    between(far_a1, 0.0, 543.4958))
add("E3-013", "63,29", "FP per 24 jam median 45 fold-run", "DERIVASI",
    fw("e3_verify.json", "`v4_rentang.A1_semua_seed_far.median`"),
    "bagian 4.2", "TERVERIFIKASI", lambda: round(VER["v4_rentang"]["A1_semua_seed_far"]["median"], 2) == 63.29)
add("E3-014", "0,0010 sampai 0,5057", "recall", "DERIVASI",
    fw("e3_verify.json", "`v4_rentang.A1_seed42_recall`") + " ; median 0,0740",
    "bagian 4.2", "TERVERIFIKASI",
    between([VER["v4_rentang"]["A1_seed42_recall"][k] for k in ("min", "max")], 0.0010, 0.5057))
add("E3-015", "2 dari 9", "fold lulus gate A seed 42", "DERIVASI",
    fw("e3_run_summary.json", "`fold_gate_A_A1_seed42`"), "bagian 4.2, 5", "TERVERIFIKASI",
    lambda: SUM["fold_gate_A_A1_seed42"] == 2)
add("E3-016", "3 dari 45", "fold-run lulus gate A semua seed", "DERIVASI",
    fw("e3_verify.json", "`v3_gate_A.A1.n_gate_A_lulus` = 3 dari `n_fold` = 45"),
    "bagian 4.2, 5", "TERVERIFIKASI",
    lambda: VER["v3_gate_A"]["A1"]["n_gate_A_lulus"] == 3 and VER["v3_gate_A"]["A1"]["n_fold"] == 45)
add("E3-017", "0,05 sampai 0,20", "alpha conformal terpilih", "DERIVASI",
    fw("e3_budget.json", "`A1_alpha_vs_anggaran_seed42[].alpha_dipilih`"),
    "bagian 4.2, 6.2", "TERVERIFIKASI",
    lambda: sorted({r["alpha"] for r in a1_s42}) == [0.05, 0.1, 0.2])

add("E3-018", "127,49 sampai 232,66", "FP per 24 jam A2 reset", "DERIVASI",
    fw("e3_b_cusum_results.json", "`varian.reset.folds[].far_per_24h`"),
    "bagian 4.3, 5", "TERVERIFIKASI (assert V1)", between([r["far_per_24h"] for r in a2r], 127.4880, 232.6638))
add("E3-019", "0,3871 sampai 0,8038", "recall A2 reset", "DERIVASI",
    fw("e3_verify.json", "`v4_rentang.A2_reset_recall`"), "bagian 4.3", "TERVERIFIKASI",
    between([VER["v4_rentang"]["A2_reset_recall"][k] for k in ("min", "max")], 0.3871, 0.8038))
add("E3-020", "1330,94 sampai 1440,00", "FP per 24 jam A2 tanpa reset", "DERIVASI",
    fw("e3_b_cusum_results.json", "`varian.tanpa_reset.folds[].far_per_24h`"),
    "bagian 4.3, 5", "TERVERIFIKASI (assert V1)",
    between([r["far_per_24h"] for r in a2n], 1330.9440, 1440.0))
add("E3-021", "0,8882 sampai 1,0000", "recall A2 tanpa reset", "DERIVASI",
    fw("e3_verify.json", "`v4_rentang.A2_tanpa_reset_recall`"), "bagian 4.3", "TERVERIFIKASI",
    between([VER["v4_rentang"]["A2_tanpa_reset_recall"][k] for k in ("min", "max")], 0.8882, 1.0))
add("E3-022", "0 dari 9", "fold lulus gate A A2 (kedua varian)", "DERIVASI",
    fw("e3_verify.json", "`v3_gate_A.A2_reset` dan `A2_tanpa_reset`"),
    "bagian 4.3, 5", "TERVERIFIKASI",
    lambda: VER["v3_gate_A"]["A2_reset"]["n_gate_A_lulus"] == 0
    and VER["v3_gate_A"]["A2_tanpa_reset"]["n_gate_A_lulus"] == 0)

add("E3-023", "0,00 sampai 24,14", "FP per 24 jam A1b", "DERIVASI",
    fw("e3_a1b_lag_results.json", "`folds[].far_per_24h`"), "bagian 4.4", "TERVERIFIKASI",
    between([r["far_per_24h"] for r in A1B["folds"]], 0.0, 24.1449))
add("E3-024", "0,4737 sampai 0,9645", "presisi A1b (8 fold berpresisi terdefinisi)", "DERIVASI",
    fw("e3_verify.json", "`v4_rentang.A1b_precision`") + " ; F-9_A presisi tidak terdefinisi (0 alarm)",
    "bagian 4.4", "TERVERIFIKASI",
    between([VER["v4_rentang"]["A1b_precision"][k] for k in ("min", "max")], 0.4737, 0.9645))
add("E3-025", 2, "kolom turunan label dipakai A1b", "RUN-KITA",
    fw("e3_verify.json", "`v5_audit_fitur.kolom_turunan_label_dipakai_A1b`") +
    " = y_prev_hyd, valid_prev_hyd ; melanggar E2 §2.3 L3",
    "bagian 4.4, 5", "TERVERIFIKASI",
    lambda: sorted(VER["v5_audit_fitur"]["kolom_turunan_label_dipakai_A1b"]) ==
    sorted(["y_prev_hyd", "valid_prev_hyd"]))

add("E3-026", "0,00416667", "fraksi menit negatif yang boleh menyala", "KONVENSI",
    "6 alarm / 1440 menit ; ambang gate A dari docs/RND_ALGO_RESEARCH_PLAN.md §6 dan "
    "docs/RND_E2_PROTOKOL.md §5.2 ; dihitung ulang di `code/rnd_e3_budget.py`",
    "bagian 6.1", "TERVERIFIKASI",
    lambda: abs(BUD["anggaran_fraksi_menit_negatif"] - 6 / 1440) < 1e-12)
add("E3-027", "12 sampai 48", "kali lipat di atas anggaran (alpha A1)", "DERIVASI",
    fw("e3_budget.json", "`A1_alpha_vs_anggaran_seed42[].kelebihan_kali`") + " = 12, 12, 12, 48, 12, 48, 12, 12, 24",
    "bagian 6.1", "TERVERIFIKASI",
    lambda: max(r["kelebihan_kali"] for r in BUD["A1_alpha_vs_anggaran_seed42"]) == 48.0)
add("E3-028", "0,377428", "fraksi menit negatif menyala tertinggi A1", "DERIVASI",
    fw("e3_budget.json", "`A1_seed42[].fraksi_menit_menyala` maks") + " ; 90,6 kali anggaran",
    "bagian 6.1", "TERVERIFIKASI",
    lambda: max(r["fraksi_menit_menyala"] for r in BUD["A1_seed42"]) == 0.377428)
add("E3-029", "0,0885 sampai 0,1616", "fraksi menit negatif menyala A2 reset", "DERIVASI",
    fw("e3_budget.json", "`A2_reset[].fraksi_menit_menyala`") + " ; 21,2 sampai 38,8 kali anggaran",
    "bagian 6.1", "TERVERIFIKASI",
    between([BUD["A2_reset"][0]["fraksi_menit_menyala"],
             max(r["fraksi_menit_menyala"] for r in BUD["A2_reset"])], 0.088533, 0.161572, 6))
add("E3-030", "0,9243 sampai 1,0000", "fraksi menit negatif menyala A2 tanpa reset", "DERIVASI",
    fw("e3_budget.json", "`A2_tanpa_reset[].fraksi_menit_menyala`") + " ; 221,8 sampai 240,0 kali anggaran",
    "bagian 6.1", "TERVERIFIKASI",
    lambda: min(r["fraksi_menit_menyala"] for r in BUD["A2_tanpa_reset"]) > 0.92)

add("E3-031", "0,0171 sampai 0,6730", "cakupan waktu teramati per fold", "DERIVASI",
    fw("e3_cakupan.json", "`per_fold[].fraksi`"), "bagian 3, 5.1", "TERUKUR",
    between(cak_fr, 0.0171, 0.6730))
add("E3-032", "1 dari 9", "fold dengan cakupan >= 50 persen", "DERIVASI",
    fw("e3_cakupan.json", "`per_fold[].fraksi` ; hanya F-10 = 0,6730") +
    " ; E2 §4.1 butir (d) melarang sertifikasi fold dengan cakupan < 50 persen",
    "bagian 5.1", "TERVERIFIKASI", lambda: sum(1 for f in cak_fr if f >= 0.5) == 1)
add("E3-033", 113, "pemeriksaan verifikasi", "RUN-KITA",
    fw("e3_verify.json", "`checks` panjang ; 0 gagal") + " ; `code/rnd_e3_verify.py`",
    "bagian 3, 7", "TERUKUR",
    lambda: len(VER["checks"]) == 113 and VER["ringkasan"]["n_gagal"] == 0)
add("E3-034", "7 dari 7", "rujukan dengan metadata terverifikasi", "RUN-KITA",
    fw("e3_doi.json", "`refs[].metadata_terverifikasi`") + " ; `code/rnd_e3_doi.py`",
    "bagian 8", "TERUKUR", lambda: sum(1 for r in DOI["refs"] if r["metadata_terverifikasi"]) == 7)
add("E3-035", 4, "penerbit membalas 403 (blokir bot)", "RUN-KITA",
    fw("e3_doi.json", "`refs[].lapis3_akses` = 403") + " ; Lei, Page, Garwood, Siffer",
    "bagian 8", "TERUKUR",
    lambda: sum(1 for r in DOI["refs"] if r["lapis3_akses"] == 403) == 4)
add("E3-036", "BELUM TERUKUR", "jam orang gate B", "BELUM-TERUKUR",
    "tidak ada data durasi pemeriksaan manusia per alarm pada repo; gate B tidak dapat dihitung",
    "bagian 5.3", "BELUM TERUKUR", lambda: True)

if err:
    print("ASSERT GAGAL, tidak ada baris ditulis:", err)
    sys.exit(1)

tabel = ["| No | Angka | Satuan | Kelas sumber | Rujukan persis | Tanggal akses | Dipakai di | Status |",
         "|---|---|---|---|---|---|---|---|"]
for r in rows:
    tabel.append("| " + " | ".join(str(x).replace("|", "/") for x in r) + " |")

blok = "\n".join([
    HEAD, "",
    "Dokumen pendamping: `docs/RND_E3_HASIL.md`. Sumber: `scratch/rnd/e3/e3_a_conformal_results.json`, "
    "`e3_a1b_lag_results.json`, `e3_b_cusum_results.json`, `e3_baseline_results.json`, "
    "`e3_budget.json`, `e3_cakupan.json`, `e3_verify.json`, `e3_doi.json`, `e3_run_summary.json`. "
    "Setiap baris di-assert terhadap path JSON oleh `code/rnd_e3_ledger.py`; assert yang gagal "
    "membatalkan seluruh penulisan.", "",
    *tabel, "",
    f"Jumlah baris: {len(rows)}. Baris BELUM-TERUKUR: 1 (E3-036, gate B).", "",
    "### Rekap kelas sumber E3", "",
    f"- RUN-KITA: {sum(1 for r in rows if r[3] == 'RUN-KITA')} baris",
    f"- DERIVASI: {sum(1 for r in rows if r[3] == 'DERIVASI')} baris",
    f"- KONVENSI: {sum(1 for r in rows if r[3] == 'KONVENSI')} baris",
    f"- BELUM-TERUKUR: {sum(1 for r in rows if r[3] == 'BELUM-TERUKUR')} baris", "",
    "### Yang tetap belum terukur pada E3", "",
    "- Jam orang dan beban pemeriksaan manusia (gate B), karena tidak ada data durasi inspeksi "
    "per alarm di repo ini.",
    "- FAR pada satuan bengkel untuk hyd, karena hyd adalah engine rig dan konvensinya per 24 jam.",
    "- Kestabilan gate C antar seed untuk A2, karena ambang CUSUM dikalibrasi deterministik "
    "sehingga seed tidak berlaku.",
    "",
])

txt = open(LEDGER, encoding="utf-8").read()
if HEAD in txt:
    txt = txt[:txt.index(HEAD)].rstrip() + "\n\n"
open(LEDGER, "w", encoding="utf-8").write(txt.rstrip() + "\n\n" + blok)
json.dump([dict(zip(("no", "angka", "satuan", "kelas", "rujukan", "tanggal", "dipakai", "status"), r))
           for r in rows], open(f"{E3}/e3_ledger.json", "w"), indent=2, ensure_ascii=False)

print(f"OK: {len(rows)} baris E3 ditulis, 0 assert gagal")
print(f"ledger total baris file: {sum(1 for _ in open(LEDGER, encoding='utf-8'))}")
