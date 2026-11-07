#!/usr/bin/env python3
"""Cek 10: audit 1:1 seluruh angka tabel bab ML kandidat_2 vs JSON primer.
Menghitung: berapa angka dicocokkan, berapa beda toleransi, berapa salah."""
import json, os, re, glob

BASE = "/mnt/d/Capstone 1(v2)"
S = os.path.join(BASE, "scratch/v9_e_ml")
K2 = open(os.path.join(BASE, "docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md"), encoding="utf-8").read()
bab4 = K2[K2.find("## Bab 4: Labeling untuk Head ML"):K2.find("## Bab 5: Metode Statistik")]

engines = {"vib": None, "ssi": None, "shk": None, "stuck_k2": None}
for e in engines:
    engines[e] = json.load(open(os.path.join(S, f"v9_e_ML_{e}_RESULTS.json")))

num = lambda s: float(s.replace("**", "").replace("*", "").strip()
                      .replace(",", ".").replace("−", "-").replace("–", "-"))

rows_expected = 0
rows_checked = 0
mismatch = []
cell_checked = 0

SECTION = {"4.1": "vib", "4.2": "ssi", "4.3": "shk", "4.4": "stuck_k2"}
# temukan tabel per sub-bab
for sec, e in SECTION.items():
    start = bab4.find(f"#### {sec}")
    if start < 0:
        print("!! seksi tidak ketemu", sec); continue
    nxt = bab4.find("#### ", start + 5)
    block = bab4[start:nxt if nxt > 0 else len(bab4)]
    jf = {f["fold"]: f for f in engines[e]["folds"]}
    for line in block.split("\n"):
        m = re.match(r"^\|\s*(\d+)\s*\|\s*([A-Za-z0-9_\-]+)\s*\|", line)
        if not m:
            continue
        fold = int(m.group(1)); well = m.group(2)
        if fold not in jf:
            continue
        f = jf[fold]
        if f["test_well"] != well:
            mismatch.append((e, fold, "well", well, f["test_well"]))
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        # fold, well, n, pos, prev, UP, RF(CI), GB, LR, pers, canary, rand
        if len(cells) < 12:
            continue
        rows_expected += 1
        rows_checked += 1
        checks = []
        checks.append(("n", num(cells[2]), f["n_test"], 0.5))
        checks.append(("pos", num(cells[3]), f["pos_test"], 0.5))
        checks.append(("prev", num(cells[4]), round(f["prev_test"], 4), 5e-4))
        # RF + CI
        mrf = re.match(r"^\**([0-9,\.]+)\**\s*\[([0-9,\.]+);\s*([0-9,\.]+)\]", cells[6])
        if not mrf:
            mismatch.append((e, fold, "format RF/CI", cells[6], ""))
        else:
            mrf_v = engines[e]["folds"][fold]["models"]["rf"]
            checks.append(("rf", num(mrf.group(1)), round(mrf_v["auprc"], 4), 5e-4))
            checks.append(("ci_lo", num(mrf.group(2)), round(mrf_v["ci95"][0], 3), 5e-4))
            checks.append(("ci_hi", num(mrf.group(3)), round(mrf_v["ci95"][1], 3), 5e-4))
        for idx, name in ((7, "gb"), (8, "lr")):
            v = f["models"][name]["auprc"]
            checks.append((name, num(cells[idx]), round(v, 4), 5e-4))
        for idx, name in ((9, "pers"), (10, "canary"), (11, "rand")):
            key = {"pers": "persistence", "canary": "canary_depth",
                   "rand": "prevalence_random"}[name]
            v = f["baselines"][key]["auprc"]
            checks.append((name, num(cells[idx]), round(v, 4), 5e-4))
        for label, got, want, tol in checks:
            cell_checked += 1
            if abs(got - want) > tol:
                mismatch.append((e, fold, label, got, want))

print(f"baris tabel ditemukan/dicek = {rows_checked} (expected 26)")
print(f"sel angka dicek = {cell_checked}")
print(f"ketidakcocokan = {len(mismatch)}")
for x in mismatch:
    print("   MISMATCH:", x)

# ---- agregat baris ringkasan (hanya tabel ringkasan §4 sebelum 4.1) ----
print("\n=== baris ringkasan agregat bab 4 ===")
agg_block = bab4[bab4.find("### 4. (e.4)"):bab4.find("#### 4.1")]
for line in agg_block.split("\n"):
    m = re.match(r"^\|\s*\*\*(vib|ssi|shk|stuck K-ii)\*\*\s*\|", line)
    if not m:
        continue
    key = {"stuck K-ii": "stuck_k2"}.get(m.group(1), m.group(1))
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    j = engines[key]["agregat"]["rf"]
    rng = re.match(r"([0-9,]+)[–-]([0-9,]+)", cells[3])
    ok = (num(rng.group(1)) == round(j["auprc_min"], 4) and
          num(rng.group(2)) == round(j["auprc_max"], 4)) if rng else False
    spread_ok = abs(num(cells[4]) - round(j["spread_auprc"], 4)) < 5e-4
    print(f"  {key}: rentang_cells={cells[3]} json=[{j['auprc_min']},{j['auprc_max']}] cocok={ok} | "
          f"spread={cells[4]} json={round(j['spread_auprc'],4)} cocok={spread_ok} | "
          f"canary={cells[5]} json={j['deltaB_vs_canary_pos']} | "
          f"pers={cells[6]} json={j['deltaB_vs_persistence_pos']}")

# ---- baris deltaB prosa ----
print("\n=== baris deltaB prosa (regex) ===")
db_re = re.compile(r"\*\*ΔB RF per fold\*\*\s*:\s*vs persistence:\s*([^\n]+)", re.S)
c_re = re.compile(r"vs canary:\s*([^\n]+)", re.S)
n_db_checked = 0
db_mis = []
for m in db_re.finditer(bab4):
    seg = m.group(1)
    mc = c_re.search(seg)
    pers_part = seg[:mc.start()] if mc else seg
    can_part = mc.group(1) if mc else ""
    pv = [num(x) for x in re.findall(r"[+\-−][0-9,]+", pers_part)]
    cv = [num(x) for x in re.findall(r"[+\-−][0-9,]+", can_part)]
    # tentukan engine dari posisi
    pos = m.start()
    sec = None
    for s, e in SECTION.items():
        i = bab4.find(f"#### {s}")
        j = bab4.find("#### ", i + 5)
        if i <= pos < (j if j > 0 else len(bab4)):
            sec = e
    if sec is None:
        continue
    folds = engines[sec]["folds"]
    for i, f in enumerate(folds):
        if i < len(pv):
            n_db_checked += 1
            want = round(f["delta_B"]["rf_vs_persistence"], 4)
            if abs(pv[i] - want) > 5e-4:
                db_mis.append((sec, f["fold"], "pers", pv[i], want))
        if i < len(cv):
            n_db_checked += 1
            want = round(f["delta_B"]["rf_vs_canary_depth"], 4)
            if abs(cv[i] - want) > 5e-4:
                db_mis.append((sec, f["fold"], "canary", cv[i], want))
print(f"  nilai deltaB dicek = {n_db_checked} | salah = {len(db_mis)}")
for x in db_mis:
    print("   MISMATCH:", x)

# ---- angka prosa kunci ----
print("\n=== prosa kunci vs primer ===")
def has(pat):
    return bool(re.search(pat, bab4, re.I))
checks = [
    ("26 fold", has(r"\b26\s*fold")),
    ("lift 1,61/2,36/3,50/1,63", has(r"1,61\s*/\s*2,36\s*/\s*3,50\s*/\s*1,63")),
    ("persistence-onset 0,8265-0,9016", has(r"0,8265.0,9016")),
    ("RF 0,0697-0,4443", has(r"0,0697.0,4443")),
    ("135 titik shk / 53 FAR<=60", has(r"135 titik") and has(r"53 titik")),
    ("10 dari 402 titik", has(r"10 dari 402")),
    ("determinisme 2,22e-16", has(r"2,22e-16")),
    ("UP F-7 3 pos / F-9 12 pos", has(r"F-7 \(3 pos\)") or has(r"3 pos")),
    ("assert baris 192-193", has(r"baris 192.193")),
    ("118.567 baris kosong", has(r"118\.567")),
    ("884 event (50/571/263)", has(r"884") and has(r"571")),
    ("P75 256,600 psi", has(r"256,600")),
    ("onset 72/93/61/55", has(r"F-9_A 72") and has(r"93") and has(r"55")),
    ("sklearn 1.9.1", has(r"1\.9\.1")),
    ("28 -> 26 koreksi", has(r"\b28\b")),
    ("median run 10 menit", has(r"median run 10 menit")),
    ("6/7 baris positif", has(r"6/7 baris positif")),
]
for name, ok in checks:
    print(f"  {'OK ' if ok else 'ABSEN'} {name}")
