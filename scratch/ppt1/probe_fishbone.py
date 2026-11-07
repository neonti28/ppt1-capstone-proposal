"""Ekstrak bukti mentah untuk fishbone 6M (kartu t_39eac1b2).

Semua angka yang dicetak di sini berasal dari berkas nyata dan dipakai
sebagai jejak di docs/PPT1_BAB1_2.md + scratch/ppt1/fishbone.json.
"""
import csv
import json
import os
from collections import Counter
from datetime import datetime

BASE = "/mnt/d/Capstone 1(v2)"
OUT = {}


def p(*a):
    print(*a)


# ---------------------------------------------------------------- 1. label
lab_path = os.path.join(BASE, "data/volve/labels_curated_v2.csv")
rows = list(csv.DictReader(open(lab_path, encoding="utf-8", errors="replace")))
p("== labels_curated_v2.csv ==")
p("baris_terbaca:", len(rows))
p("kolom:", len(rows[0]))

cat = Counter(r["category"] for r in rows)
bha = Counter((r["bha_relevant"] or "KOSONG").strip().lower() for r in rows)
outcome = Counter((r["outcome"] or "").strip() for r in rows)
wells = Counter((r["wellbore"] or "").strip() for r in rows)
p("kategori:", cat.most_common())
p("bha_relevant:", bha.most_common())
p("outcome kosong:", outcome.get("", 0), "dari", len(rows))
p("wellbore:", len(wells), wells.most_common())

# durasi
durs = []
bad = 0
for r in rows:
    try:
        s = datetime.fromisoformat(r["act_start"])
        e = datetime.fromisoformat(r["act_end"])
        d = (e - s).total_seconds() / 60.0
        if d >= 0:
            durs.append(d)
        else:
            bad += 1
    except Exception:
        bad += 1
durs.sort()
p("durasi_valid:", len(durs), "gagal_parse/negatif:", bad)
if durs:
    p("total_menit:", round(sum(durs), 1), "jam:", round(sum(durs) / 60, 1))
    p("median:", durs[len(durs) // 2], "p90:", durs[int(len(durs) * 0.9)])

# sebaran durasi per kategori
per_cat = {}
for r in rows:
    try:
        s = datetime.fromisoformat(r["act_start"])
        e = datetime.fromisoformat(r["act_end"])
        d = (e - s).total_seconds() / 60.0
        per_cat.setdefault(r["category"], []).append(d)
    except Exception:
        pass
p("kategori -> n, total_jam:")
for k, v in sorted(per_cat.items(), key=lambda kv: -sum(kv[1])):
    p("   ", k, len(v), round(sum(v) / 60, 1))

OUT["labels"] = {
    "file": "data/volve/labels_curated_v2.csv",
    "baris": len(rows),
    "kolom": len(rows[0]),
    "kategori": dict(cat),
    "bha_relevant": dict(bha),
    "outcome_kosong": outcome.get("", 0),
    "wellbore_n": len(wells),
    "wellbore": dict(wells),
    "durasi": {
        "valid": len(durs),
        "gagal": bad,
        "total_menit": round(sum(durs), 1),
        "total_jam": round(sum(durs) / 60, 1),
        "median_menit": durs[len(durs) // 2] if durs else None,
        "p90_menit": durs[int(len(durs) * 0.9)] if durs else None,
        "per_kategori": {k: {"n": len(v), "jam": round(sum(v) / 60, 1)}
                         for k, v in per_cat.items()},
    },
}

# ------------------------------------------------------------ 2. registry 27
i1_path = os.path.join(BASE, "scratch/v9_i1/v9_i1_RESULTS.json")
i1 = json.load(open(i1_path))
p("\n== v9_i1_RESULTS.json ==")
p("top keys:", list(i1.keys()))


def walk(o, depth=0, path=""):
    if depth > 2:
        return
    if isinstance(o, dict):
        for k, v in list(o.items())[:40]:
            if isinstance(v, (dict, list)):
                p("  " * depth, path + "/" + str(k), type(v).__name__, len(v))
                walk(v, depth + 1, path + "/" + str(k))
            else:
                p("  " * depth, path + "/" + str(k), "=", repr(v)[:100])
    elif isinstance(o, list) and o:
        p("  " * depth, path, "[0] ->", repr(o[0])[:200])


walk(i1)

# ------------------------------------------------------------ 3. vib FAR
vib_path = os.path.join(BASE, "scratch/v9_e_ml/v9_e_ML_vib_RESULTS.json")
if os.path.exists(vib_path):
    vib = json.load(open(vib_path))
    p("\n== v9_e_ML_vib_RESULTS.json ==")
    walk(vib)
    tex = json.dumps(vib, ensure_ascii=False)
    p("ada substring 496.09?", "496.09" in tex or "496,09" in tex)
    p("ada 4.149/4.15?", "4.149" in tex or "4.15" in tex)

json.dump(OUT, open(os.path.join(BASE, "scratch/ppt1/_probe_fishbone.json"), "w"),
          ensure_ascii=False, indent=2)
p("\nOK -> scratch/ppt1/_probe_fishbone.json")
