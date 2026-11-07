#!/usr/bin/env python3
"""Cek 6: jendela ketat-lalu + eligibility di kode builder; run-length onset; output v9_d1_04;
mtime file (klaim kolom kosong); nama 7 engine; md=ipynb tingkat bab-ML."""
import os, re, glob, json, gzip, csv, collections, statistics, datetime

BASE = "/mnt/d/Capstone 1(v2)"

print("=== A. jendela ketat-lalu & eligibility (klaim k2 §1.2/§2.1) ===")
for f in ["code/v9_d1_02_rig_windows.py", "code/v9_d1_03_rig_datasets.py",
          "code/v9_d1_04_stuck_k2.py"]:
    p = os.path.join(BASE, f)
    if not os.path.exists(p):
        print("  MISSING", f); continue
    for i, l in enumerate(open(p, encoding="utf-8", errors="replace").read().splitlines(), 1):
        if any(k in l for k in ("t0 - 10", "t0-10", "W = 10", "shift(-", "drill_bins",
                                "drill_rows", "feat_valid", "strict", "lab_ts", "feat_ts_max")):
            if len(l.strip()) < 190:
                print(f"  {f}:{i}: {l.strip()}")

print("\n=== B. run-length label positif stuck_k2 (klaim k2: median run 10 menit) ===")
p = os.path.join(BASE, "scratch/v9_d1/datasets/stuck_k2.csv.gz")
runs = []
with gzip.open(p, "rt", newline="") as fh:
    r = csv.DictReader(fh)
    cur = collections.Counter()
    prev_w = None
    cur_len = 0
    for row in r:
        w = row["well"]
        y = int(float(row["y_stuck_onset"]))
        if w != prev_w:
            if cur_len:
                runs.append((prev_w, cur_len))
            cur_len = 0
            prev_w = w
        if y == 1:
            cur_len += 1
        else:
            if cur_len:
                runs.append((prev_w, cur_len))
            cur_len = 0
    if cur_len:
        runs.append((prev_w, cur_len))
lens = [l for _, l in runs]
print("n run positif =", len(lens), "| median =", statistics.median(lens),
      "| mean =", round(statistics.mean(lens), 2), "| distribusi:",
      dict(collections.Counter(lens).most_common(12)))
per_w = collections.defaultdict(list)
for w, l in runs:
    per_w[w].append(l)
for w, ls in per_w.items():
    print(f"  {w}: n_run={len(ls)} median={statistics.median(ls)}")

print("\n=== C. output v9_d1_04 (invarian onsets per well; klaim F-9=55) ===")
cands = glob.glob(os.path.join(BASE, "scratch/v9_d1/*")) 
for p in sorted(cands):
    if os.path.isdir(p):
        continue
    if "stuck" in os.path.basename(p).lower() or "d1_04" in os.path.basename(p).lower():
        print("  file:", os.path.basename(p))
        if p.endswith(".json"):
            j = json.load(open(p))
            s = json.dumps(j, ensure_ascii=False)
            print("   ", s[:900])
# fallback: cari 55 di semua json v9_d1
for p in sorted(glob.glob(os.path.join(BASE, "scratch/v9_d1/*.json"))):
    txt = open(p, encoding="utf-8", errors="replace").read()
    if "onsets" in txt and "F-9" in txt:
        print("  kandidat sumber onsets:", os.path.basename(p))
        for m in re.finditer(r".{0,90}(onset|onsets|positives).{0,90}", txt):
            seg = m.group(0)
            if "F-9" in seg or "55" in seg:
                print("     ", seg.replace("\n", " ")[:200])

print("\n=== D. mtime (jejak regenerate dataset stuck_k2) ===")
files = [
    "scratch/v9_d1/datasets/stuck_k2.csv.gz",
    "scratch/v9_e_ml/v9_e_ML_stuck_k2_RESULTS.json",
    "scratch/v9_e_ml/v9_e_ML_stuck_k2_RUN_LOG.txt",
    "scratch/v9_d1/v9_d1_05_leak_lowo.json",
    "docs/V9_E_ML_ENGINE.md",
    "docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md",
    "docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.v3_arsip.md",
    "code/v9_e_ML_01_train.py",
    "code/v9_d1_04_stuck_k2.py",
]
for f in files:
    p = os.path.join(BASE, f)
    if os.path.exists(p):
        st = os.stat(p)
        print(f"  {datetime.datetime.fromtimestamp(st.st_mtime)}  {st.st_size:>9}  {f}")
    else:
        print("  MISSING", f)

print("\n=== E. nama 7 engine / 27 head di protokol V11 (primer kosakata) ===")
p = os.path.join(BASE, "docs/V11_PROTOCOL.md")
if os.path.exists(p):
    txt = open(p, encoding="utf-8").read().splitlines()
    for i, l in enumerate(txt, 1):
        if any(k in l for k in ("7 engine", "27 head", "11 klaim", "hyd", "tool_wear", "bit_wear")) and i < 90:
            print(f"  :{i}: {l.strip()[:190]}")

print("\n=== F. md=ipynb tingkat BAB ML (potong bab per kandidat) ===")
DOCS = os.path.join(BASE, "docs")


def nb_text(path):
    nb = json.load(open(path, encoding="utf-8"))
    return "\n".join("".join(c.get("source", [])) for c in nb["cells"])


# kandidat 2: Bab 4 -> Bab 5
md = open(os.path.join(DOCS, "ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md"), encoding="utf-8").read()
ip = nb_text(os.path.join(DOCS, "ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.ipynb"))
def slice_between(t, a, b):
    i = t.find(a); j = t.find(b, i + 1)
    return t[i:j] if i >= 0 and j > 0 else ""
m4 = slice_between(md, "## Bab 4: Labeling untuk Head ML", "## Bab 5: Metode Statistik")
i4 = slice_between(ip, "## Bab 4: Labeling untuk Head ML", "## Bab 5: Metode Statistik")
print(f"  K2 bab4 md chars={len(m4)} ipynb chars={len(i4)}")
ml = [l.strip() for l in m4.split("\n") if l.strip()]
miss = [l for l in ml if l.replace(" ", "") not in i4.replace("\n", "")]
miss2 = [l for l in ml if l not in i4]
print(f"  baris md bab4 hilang persis di ipynb: {len(miss2)}/{len(ml)}")
for l in miss2:
    print("     -", l[:150])

# kandidat 1: ## 8. Data -> ## 14. Arsitektur
md1 = open(os.path.join(DOCS, "ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.v3_arsip.md"), encoding="utf-8").read()
ip1 = nb_text(os.path.join(DOCS, "ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.v3_arsip.ipynb"))
m1 = slice_between(md1, "## 8. Data", "## 14. Arsitektur")
print(f"  K1 §8-13 md chars={len(m1)}")
ml1 = [l.strip() for l in m1.split("\n") if l.strip()]
miss1 = [l for l in ml1 if l not in ip1]
print(f"  baris K1 §8-13 hilang di ipynb: {len(miss1)}/{len(ml1)}")
for l in miss1:
    print("     -", l[:150])
print("  ipynb K1 memuat '## 8. Data'?", "## 8. Data" in ip1, "| '## 13. Metrik Evaluasi'?",
      "## 13. Metrik Evaluasi" in ip1)
