"""R2: menambahkan baris ledger provenance untuk semua angka di docs/RND_R2_STOKASTIK.md."""
import io

LEDGER = "/mnt/d/Capstone 1(v2)/docs/RND_PROVENANCE_LEDGER.md"
TGL = "2026-10-27"
MC = "`scratch/rnd_r2/mc_result.json`; `python3 scratch/rnd_r2/mc_iterations.py` (run 2026-10-27 04:02 WIB, seed 11/22/33/44/55)"
DOC = "RND_R2_STOKASTIK.md"

rows = [
    ("R2-001", "95.925 baris / 40 FP / FAR 0,603", "jendela; FP/24 jam", "RUN-KITA",
     f"`scratch/v9_i1/v9_i1_RESULTS.json` head `stuck.rf_lowo` metrik_segmen (`fp`=40, `far_segmen`=0,603); populasi D0-600 (95.925) + D0-599 (389 positif)",
     TGL, f"{DOC} §4.2 kasus A; §7.2", "TERUKUR"),
    ("R2-002", "10.401 baris / 110 FP / FAR 16,611", "jendela; FP/24 jam", "RUN-KITA",
     "`scratch/v9_i1/v9_i1_RESULTS.json` head `hyd.hybrid_rule_and_persistence` metrik_segmen (`n`=10.401, `fp`=110, `far_segmen`=16,611)",
     TGL, f"{DOC} §4.2 kasus B", "TERUKUR"),
    ("R2-003", "0,005 FAR absolut; 1% lebar CI; N=2.000 default; N=10.000 utk FAR < 1/24 jam", "FP/24 jam; %; iterasi",
     "KONVENSI", f"kriteria berhenti ditetapkan sebelum run di `scratch/rnd_r2/mc_iterations.py` docstring; hasil uji di {DOC} §4.2", TGL,
     f"{DOC} §4.2", "BELUM"),
    ("R2-004", "SE(lo)=0,0176 SE(hi)=0,0113 lebar=0,3710 (N=200, stuck K-ii)", "FAR; FAR; FAR", "RUN-KITA", MC, TGL, f"{DOC} §4.2 tabel A", "TERUKUR"),
    ("R2-005", "SE(lo)=0,0095 SE(hi)=0,0074 lebar=0,3679 (N=500, stuck K-ii)", "FAR; FAR; FAR", "RUN-KITA", MC, TGL, f"{DOC} §4.2 tabel A", "TERUKUR"),
    ("R2-006", "SE(lo)=0,0060 SE(hi)=0,0060 lebar=0,3770 (N=1.000, stuck K-ii)", "FAR; FAR; FAR", "RUN-KITA", MC, TGL, f"{DOC} §4.2 tabel A", "TERUKUR"),
    ("R2-007", "SE(lo)=0,0060 SE(hi)=0,0000 lebar=0,3800 (N=2.000, stuck K-ii)", "FAR; FAR; FAR", "RUN-KITA", MC, TGL, f"{DOC} §4.2 tabel A", "TERUKUR"),
    ("R2-008", "SE(lo)=0,4125 SE(hi)=0,2169 lebar=6,2316 (N=200, hyd K-i)", "FAR; FAR; FAR", "RUN-KITA", MC, TGL, f"{DOC} §4.2 tabel B", "TERUKUR"),
    ("R2-009", "SE(lo)=0,1666 SE(hi)=0,1227 lebar=6,1713 (N=500, hyd K-i)", "FAR; FAR; FAR", "RUN-KITA", MC, TGL, f"{DOC} §4.2 tabel B", "TERUKUR"),
    ("R2-010", "SE(lo)=0,0608 SE(hi)=0,0614 lebar=6,2631 (N=1.000, hyd K-i)", "FAR; FAR; FAR", "RUN-KITA", MC, TGL, f"{DOC} §4.2 tabel B", "TERUKUR"),
    ("R2-011", "SE(lo)=0,0745 SE(hi)=0,0614 lebar=6,2935 (N=2.000, hyd K-i)", "FAR; FAR; FAR", "RUN-KITA", MC, TGL, f"{DOC} §4.2 tabel B", "TERUKUR"),
    ("R2-012", "galat baku relatif 4,82% (N=200) dan 2,02% (N=2.000) dan 0,14% (N=10.000) pada FAR 0,6/24 jam", "%", "RUN-KITA",
     f"{MC}; blok `threshold_sim` kunci `q=0.0035`", TGL, f"{DOC} §4.2 tabel C", "TERUKUR"),
    ("R2-013", "galat baku relatif 0,68% (N=200) dan 0,18% (N=2.000) pada FAR 16,6/24 jam", "%", "RUN-KITA",
     f"{MC}; blok `threshold_sim` kunci `q=0.0115`", TGL, f"{DOC} §4.2 tabel C", "TERUKUR"),
    ("R2-014", "galat baku relatif 1,89% (N=200) dan 0,50% (N=2.000) pada FAR 6,6/24 jam", "%", "RUN-KITA",
     f"{MC}; blok `threshold_sim` kunci `q=0.0416`", TGL, f"{DOC} §4.2 tabel C", "TERUKUR"),
    ("R2-015", "B1 0-0,115; TLead 4,5-8,5", "probabilitas Brier; menit", "RUN-KITA",
     "`docs/V9_EVAL_C_LAYERC.md` §1 baris stuck K-ii (turunan `scratch/v9_e_stat/*.json`)", TGL,
     f"{DOC} §7.2", "TERUKUR"),
    ("R2-016", "median episode 1,0", "menit", "RUN-KITA", "`docs/RND_D0_DATA_FEASIBILITY.md` §3 tabel state (kolom median episode); dihitung `scratch/rnd_d0/*`", TGL, f"{DOC} §2, §3, §11", "TERUKUR"),
    ("R2-017", "4 dari 9 well punya kanal STUCK", "well", "RUN-KITA", "`docs/RND_D0_DATA_FEASIBILITY.md` §3 kesimpulan; tabel per well", TGL, f"{DOC} §1, §2, §3, §11", "TERUKUR"),
    ("R2-018", "31 DOI terdaftar, HTTP 200", "entri DOI", "RUN-KITA",
     "`scratch/rnd_r2/doi_verified.json` (13 DOI kanonik) + `scratch/rnd_r2/doi_verified_apps.json` (18 DOI aplikasi); `python3 scratch/rnd_r2/doi_verify.py` dan `doi_verify_apps.py`", TGL,
     f"{DOC} §9", "TERUKUR"),
    ("R2-019", "vib FAR tau0,5 sebar 4,1-496; ssi AUPRC sebar 30x", "FP/24 jam; rasio", "RUN-KITA",
     "`docs/V9_EVAL_C_LAYERC.md` §2.1 (C3 vib) dan §2.2 (C1 ssi)", TGL, f"{DOC} §4.1, §5", "TERUKUR"),
    ("R2-020", "0 dari 8 metode memenuhi syarat naik tier tanpa asumsi baru; hanya MC skor 5", "penilaian", "KONVENSI",
     f"penilaian ahli kartu ini, dasar = tabel D0 §3/§4 + skor §8 {DOC}; bukan metrik, tidak boleh dibaca sebagai hasil eksperimen", TGL,
     f"{DOC} §8, §10 butir 7", "BELUM"),
]

HEADER_NOTE = """
## Bagian R2: stokastik + survival (kartu t_c24b3640)

Penomoran memakai awalan `R2-` agar tidak bertabrakan dengan `L-xx` (P0) dan `D0-xxx` (D0).
Angka D0 yang dipakai ulang di dokumen R2 tidak diduplikasi di sini: rujukannya id D0 yang sudah ada
(mis. 95.925 = D0-600, 389 positif = D0-599, 469 jendela = D0-766, onset 55 = D0-581). Jumlah baris R2 = {n}.
"""

lines = ["", HEADER_NOTE.format(n=len(rows)).strip(), "",
         "| No | Angka | Satuan | Kelas sumber | Rujukan persis | Tanggal akses | Dipakai di | Status |",
         "|---|---|---|---|---|---|---|---|"]
for r in rows:
    lines.append("| " + " | ".join(str(x) for x in r) + " |")

with io.open(LEDGER, "a", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print("appended", len(rows), "rows")
