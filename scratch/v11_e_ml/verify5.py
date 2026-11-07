#!/usr/bin/env python3
"""Cek 5: (1) ts_bin/lab_ts stuck_k2 pakai csv parser resmi; (2) USROP label vs P75 MSE;
(3) NQ/W pada label hyd; (4) cross-tab label USROP."""
import csv, gzip, os, statistics, collections, json

BASE = "/mnt/d/Capstone 1(v2)"

print("=== 1. stuck_k2 ts_bin/lab_ts (parser csv resmi, bukan split) ===")
p = os.path.join(BASE, "scratch/v9_d1/datasets/stuck_k2.csv.gz")
with gzip.open(p, "rt", newline="") as fh:
    r = csv.DictReader(fh)
    n = 0
    vals_t = collections.Counter()
    vals_l = collections.Counter()
    nan_like = 0
    for row in r:
        n += 1
        t = (row.get("ts_bin") or "").strip()
        l = (row.get("lab_ts") or "").strip()
        if n <= 3:
            print("  contoh baris:", {"well": row["well"], "ts_bin": repr(t),
                                      "lab_ts": repr(l), "feat_ts_max": repr(row["feat_ts_max"]),
                                      "lab_kind": repr(row.get("lab_kind"))})
        vals_t[t if len(t) < 25 else t[:25]] += 1
        vals_l[l if len(l) < 25 else l[:25]] += 1
    print("rows =", n)
    print("nilai ts_bin (top10):", vals_t.most_common(10))
    print("nilai lab_ts (top10):", vals_l.most_common(10))
    def is_empty(k):
        kl = k.lower()
        return kl in ("", "nan", "none", "null", "na")
    e_t = sum(v for k, v in vals_t.items() if is_empty(k))
    e_l = sum(v for k, v in vals_l.items() if is_empty(k))
    print(f"ts_bin kosong/NaN = {e_t}/{n} ; lab_ts kosong/NaN = {e_l}/{n}")

print("\n=== 2. USROP_labeled: label vs MSE > P75 ===")
import csv as _csv
p = os.path.join(BASE, "data/USROP_labeled.csv")
with open(p, newline="", encoding="utf-8", errors="replace") as fh:
    rows = list(_csv.DictReader(fh))
mse = [float(x["MSE"]) for x in rows if x["MSE"] not in ("", None)]
mse_sorted = sorted(mse)
def pct(data, q):
    k = (len(data) - 1) * q
    f = int(k)
    c = min(f + 1, len(data) - 1)
    return data[f] + (data[c] - data[f]) * (k - f)
p75 = pct(mse_sorted, 0.75)
print("n MSE =", len(mse), "| P75 =", round(p75, 3), "| min/max =", round(min(mse), 2), round(max(mse), 2))
lab = collections.Counter(x["label"] for x in rows)
print("distribusi label:", dict(lab))
# cross-tab label vs MSE>P75
ct = collections.Counter()
for x in rows:
    if x["MSE"] in ("", None):
        continue
    hi = float(x["MSE"]) > p75
    ct[(x["label"], "MSE>P75" if hi else "MSE<=P75")] += 1
print("cross-tab (label, posisi vs P75):")
for k in sorted(ct):
    print("   ", k, ct[k])
# alternatif: cari nilai ambang yang memisahkan label persis
labs_hi = sorted({x["label"] for x in rows})
print("label unik:", labs_hi)
for cand_label in labs_hi:
    v = sorted(float(x["MSE"]) for x in rows if x["label"] == cand_label)
    if v and cand_label != "normal":
        print(f"  label '{cand_label}': n={len(v)} MSE min={v[0]:.3f} max={v[-1]:.3f} median={statistics.median(v):.3f}")
v_norm = sorted(float(x["MSE"]) for x in rows if x["label"] == "normal")
if v_norm:
    print(f"  label 'normal': n={len(v_norm)} MSE min={v_norm[0]:.3f} max={v_norm[-1]:.3f} "
          f"P25={pct(v_norm,0.25):.3f} P75={pct(v_norm,0.75):.3f}")

print("\n=== 3. NQ & jendela agregasi hyd (v9_d1_03) ===")
p = os.path.join(BASE, "code/v9_d1_03_rig_datasets.py")
for i, l in enumerate(open(p, encoding="utf-8", errors="replace").read().splitlines(), 1):
    if any(k in l for k in ("NQ =", "NQ=", "W =", "W=", "MINW", "frac", "0.5", "50")) and i < 130:
        print(f"  :{i}: {l.strip()[:170]}")

print("\n=== 4. grep ipynb md-diff kandidat 2 (v8_e_shk_02b) ===")
p = os.path.join(BASE, "docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.ipynb")
raw = open(p, encoding="utf-8").read()
i = raw.find("v8_e_shk_02b")
print(repr(raw[i - 300:i + 300]) if i >= 0 else "tidak ditemukan di ipynb")
