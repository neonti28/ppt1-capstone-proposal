#!/usr/bin/env python3
"""V9-EVAL_B 04 — verifikasi dokumen vs JSON primer (verification-mandatory #1/#2)."""
import json, os, re, time

OUT = "/mnt/d/Capstone 1(v2)/scratch/v9_eval_b"
DOC = "/mnt/d/Capstone 1(v2)/docs/V9_EVAL_B_LAYERB.md"
R = json.load(open(f"{OUT}/v9_eval_b_RESULTS.json"))
txt = open(DOC).read()
norm = txt.replace("−", "-").replace("–", "-").replace("…", "...")
ok = fail = 0
lines = []


def chk(name, cond, detail=""):
    global ok, fail
    if cond:
        ok += 1
        lines.append(f"PASS {name}")
    else:
        fail += 1
        lines.append(f"FAIL {name} {detail}")


def idp(x, nd=2):
    """format Indo: 0,55 + tanda."""
    s = f"{x:+.{nd}f}" if x is not None else ""
    return s.replace(".", ",")


# --- (a) 7 engine / 11 klaim
for eng in ["vib", "ssi", "shk", "stuck K-i", "stuck K-ii", "hyd K-i", "hyd K-ii",
            "bit_wear K-1", "bit_wear K-2", "tool_wear K-i", "tool_wear K-ii"]:
    chk(f"klaim {eng} ada", eng in txt)

# --- (b) angka dari JSON primer
B3 = R["B3"]
chk("B3 vib persistence", f"{B3['vib']['engines']['persistence']['B3_kurangi_ragu_vs_rule']:.2f}".replace(".", ",") in norm,
    f"got {B3['vib']['engines']['persistence']['B3_kurangi_ragu_vs_rule']}")
chk("B3 ssi hybrid +0,73", "0,731" in norm or "+0,73" in norm)
chk("B3 hyd hybrid", f"{B3['hyd_ki']['engines']['hybrid_rule_and_persistence']['B3_kurangi_ragu_vs_rule']:.3f}".replace(".", ",") in norm)
chk("B3 stuck RF tau0.5", f"{B3['stuck_k2_onset']['engines']['rf_tau0.5']['B3_kurangi_ragu_vs_E1']:.3f}".replace(".", ",") in norm)
chk("B3 stuck pers-event", f"{B3['stuck_k2_onset']['engines']['persistence_event']['B3_kurangi_ragu_vs_E1']:.3f}".replace(".", ",") in norm)
chk("B3 stuck E2 negatif", f"{B3['stuck_k2_onset']['engines']['E2_stats_q95']['B3_kurangi_ragu_vs_E1']:.3f}".replace(".", ",") in norm)
chk("B3 tool_wear terkalibrasi 0,909", "+0,909" in norm and "+0,976" in norm)
chk("B3 shk RF tau0.5", f"{B3['shk']['engines']['rf_tau0.5']['B3_kurangi_ragu_vs_rule']:.3f}".replace(".", ",") in norm)
chk("FP stuck RF tau0.05 = 32938 (32.938)", "32.938" in norm)
chk("FP E1 onset 422", "422" in norm)
chk("FP pers-event 11", B3['stuck_k2_onset']['engines']['persistence_event']['FP_window'] == 11 and "FP 11" in norm)

# B4 dari RESULTS
J = R["joint_B3_B4"]
def row(cls, eng):
    for r in J[cls]["rows"]:
        if r["engine"] == eng:
            return r
    return None

r = row("vib", "rule_display_t0minus1")
chk("B4 vib rule cov 26,4%", f"{r['B4_coverage']*100:.1f}".replace(".", ",") + "%" in norm, f"cov={r['B4_coverage']}")
chk("B4 vib rule margin 5,0", f"{r['B4_median_margin_mnt']:.1f}".replace(".", ",") in norm)
r = row("shk", "rule_display_t0minus1")
chk("B4 shk rule cov 13,4%", f"{r['B4_coverage']*100:.1f}".replace(".", ",") + "%" in norm)
chk("B4 shk rule margin 4,5", f"{r['B4_median_margin_mnt']:.1f}".replace(".", ",") in norm)
r = row("ssi", "rf_tau0.05")
chk("B4 ssi RF0.05 cov 27,5%", f"{r['B4_coverage']*100:.1f}".replace(".", ",") + "%" in norm)
r = row("hyd_ki", "hybrid_rule_and_persistence")
chk("B4 hyd hybrid cov 13,0%", f"{r['B4_coverage']*100:.1f}".replace(".", ",") + "%" in norm)
chk("B4 hyd hybrid margin 4,5", f"{r['B4_median_margin_mnt']:.1f}".replace(".", ",") in norm)
r = row("hyd_ki", "persistence")
chk("B4 hyd pers margin 7,0", f"{r['B4_median_margin_mnt']:.1f}".replace(".", ",") in norm)
r = row("stuck_k1", "rule_display_t0minus1")
chk("B4 stuck_k1 rule cov 11,8%", f"{r['B4_coverage']*100:.1f}".replace(".", ",") + "%" in norm)

# blocks
for cls, n in [("vib", 216), ("shk", 164), ("hyd_ki", 277), ("stuck_k1", 76)]:
    b = R["B4_status"][cls]["blocks"]["n_sustained_ge5mnt"]
    chk(f"blocks {cls}={b}", b == n and str(n) in norm)
ssi_b = R["B4_status"]["ssi"]["blocks"]
chk("ssi blocks 40/137", ssi_b["n_sustained_ge5mnt"] == 40 and ssi_b["n_runs_total"] == 137
    and "40/137" in norm)

# B1/B2 stuck
sm = R["B1_B2_onset"]["stuck_k2_ML"]["models"]["rf"]["0.05"]
chk("stuck RF0.05 B1 min 0,51", f"{sm['B1_coverage']['min']:.2f}".replace(".", ",") in norm)
chk("stuck RF0.05 TLead 10-11,5", "10-11,5" in norm or "10–11,5" in txt)
hor = R["B1_B2_onset"]["stuck_k2_RULE"]["metode"]["persistence_horizon"]["B1"]
chk("horizon B1 0,93-0,97", f"{hor['min']:.2f}".replace(".", ",") in norm and f"{hor['max']:.2f}".replace(".", ",") in norm)
chk("anchor 2,67-7,37", "2,67-7,37" in norm or "2,67–7,37" in txt)

# hyd_ki det
d = R["status_delay_konfirmasi"]["hyd_ki"]
chk("hyd delay 0-3,5", "0-3,5" in norm or "0–3,5" in txt)
w = d["pct_within_H10_range"]
chk("hyd withinH10 31,6-65,4", f"{w['min']*100:.1f}".replace(".", ",") in norm and f"{w['max']*100:.1f}".replace(".", ",") in norm)

# tool_wear
tw = R["B1_B2_onset"]["tool_wear"]["K_i"]
chk("tool cp TLead 35 dtk", tw["change_point_TLead_to_end_R02_s"]["median"] == 35 and "35 dtk" in norm)
chk("tool kalibrasi 59 dtk", tw["kalibrasi5of27_TLead_median_s"] == 59 and "59 dtk" in norm)
chk("tool FAR-cal TLead 20-36", "20-36" in norm or "20–36" in txt)

# --- (c) baseline relevan dinyatakan
for s in ["rule status-quo", "rule E1", "rule z-pit", "rule 3-RMS", "anchor kelas",
          "dilarang dipinjam"]:
    chk(f"baseline/anchor: '{s}'", s in txt)

# --- (d) tanpa vonis biner (hanya uppercase LULUS/GAGAL dgn konteks negasi)
bad = [l for l in txt.splitlines()
       if re.search(r"\bLULUS\b|\bGAGAL\b", l) and "BUKAN" not in l and "bukan" not in l]
chk("tanpa vonis biner LULUS/GAGAL", len(bad) == 0, f"pelanggar: {bad[:3]}")
chk("negasi eksplisit ada", "BUKAN vonis" in txt)

# --- struktur riset pendahuluan
skills = ["scientific-critical-thinking", "verification-mandatory", "statistical-analysis",
          "what-if-oracle", "consciousness-council", "sequentialthinking"]
for s in skills:
    chk(f"baris riset pendahuluan: {s}", f"Riset pendahuluan: {s}" in txt)
chk("minimal 6 baris riset pendahuluan", txt.count("Riset pendahuluan:") >= 6,
    f"count={txt.count('Riset pendahuluan:')}")

# --- JSON dulu baru dokumen
tj = os.path.getmtime(f"{OUT}/v9_eval_b_RESULTS.json")
td = os.path.getmtime(DOC)
chk("JSON primer lebih dulu dari dokumen", tj < td,
    f"json={time.ctime(tj)} doc={time.ctime(td)}")

# --- verifikasi V1..V6 ikut terekam di dokumen
for v in ["17/17", "22/22", "110/110", "16/16", "62/62", "27=27"]:
    chk(f"angka verifikasi '{v}' di dokumen", v in norm)

# --- belum terukur dipisah
chk("bagian belum terukur ada", "BELUM TERUKUR" in txt.upper() and "bukan gagal" in txt)

lines.append(f"\n=== verify_doc: {ok} PASS, {fail} FAIL ===")
out = "\n".join(lines)
open(f"{OUT}/v9_eval_b_VERIFY_DOC.txt", "w").write(out + "\n")
print(out)
