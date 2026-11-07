"""RND-E2 probe: struktur JSON hasil, jumlah fold, positif per fold, versi pustaka.

Semua angka yang keluar dari sini berkelas RUN-KITA dan dipakai di
docs/RND_E2_PROTOKOL.md + docs/RND_PROVENANCE_LEDGER.md.
Output: scratch/rnd_e2/e2_probe.json
"""
from __future__ import annotations

import gzip
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path("/mnt/d/Capstone 1(v2)")
OUT = BASE / "scratch/rnd_e2"
OUT.mkdir(parents=True, exist_ok=True)

res: dict = {}

# ---------------------------------------------------------------- 1. JSON V9-I1
p_json = BASE / "scratch/v9_i1/v9_i1_RESULTS.json"
d = json.loads(p_json.read_text())
res["v9_i1_top_keys"] = sorted(d.keys())

elapsed = {}
def walk(node, path=""):
    if isinstance(node, dict):
        for k, v in node.items():
            if k in ("elapsed_s", "runtime_s", "seconds") and isinstance(v, (int, float)):
                elapsed[path + "/" + k] = v
            walk(v, path + "/" + str(k))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, path + f"[{i}]")
walk(d)
res["elapsed_s_found"] = dict(list(elapsed.items())[:40])
res["elapsed_s_count"] = len(elapsed)
res["elapsed_s_sum"] = round(sum(elapsed.values()), 3) if elapsed else None

# seed / versi yang ditulis di JSON
def find_keys(node, keys, path="", acc=None):
    if acc is None:
        acc = {}
    if isinstance(node, dict):
        for k, v in node.items():
            if k in keys:
                acc.setdefault(path + "/" + str(k), v)
            find_keys(v, keys, path + "/" + str(k), acc)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            find_keys(v, keys, path + f"[{i}]", acc)
    return acc

meta = find_keys(d, {"seed", "SEED", "sklearn", "package_versions", "versions", "n_fold",
                     "n_folds", "win_s", "window_s", "generated_at", "timestamp"})
res["meta_in_json"] = dict(list(meta.items())[:30])

# ---------------------------------------------------------------- 2. dataset jendela
DS = BASE / "scratch/v9_d1/datasets"
res["dataset_dir_exists"] = DS.exists()
per_engine = {}
if DS.exists():
    for f in sorted(DS.glob("*.csv.gz")):
        eng = f.name.replace(".csv.gz", "")
        with gzip.open(f, "rt") as fh:
            header = fh.readline().rstrip("\n").split(",")
            if "well" not in header:
                per_engine[eng] = {"error": "kolom well tidak ada", "n_cols": len(header)}
                continue
            iw = header.index("well")
            # cari kolom label: y_*
            ycols = [(i, c) for i, c in enumerate(header) if c.startswith("y_")]
            tot = Counter()
            pos = defaultdict(Counter)
            nrow = 0
            for line in fh:
                parts = line.rstrip("\n").split(",")
                nrow += 1
                w = parts[iw]
                tot[w] += 1
                for i, c in ycols:
                    v = parts[i]
                    if v not in ("", "0", "0.0", "False", "nan"):
                        pos[w][c] += 1
            per_engine[eng] = {
                "rows": nrow,
                "wells": sorted(tot),
                "n_wells": len(tot),
                "rows_per_well": dict(tot),
                "y_cols": [c for _, c in ycols],
                "pos_per_well_per_label": {w: dict(v) for w, v in pos.items()},
            }
res["per_engine"] = per_engine

# ---------------------------------------------------------------- 3. versi pustaka
vers = {}
for mod in ("numpy", "pandas", "sklearn", "scipy", "statsmodels", "lightgbm",
            "xgboost", "catboost", "pyarrow"):
    try:
        m = __import__(mod)
        vers[mod] = getattr(m, "__version__", "tanpa __version__")
    except Exception as e:
        vers[mod] = f"TIDAK TERPASANG ({type(e).__name__})"
vers["python"] = sys.version.split()[0]
res["lib_versions"] = vers

(OUT / "e2_probe.json").write_text(json.dumps(res, indent=2, ensure_ascii=False))
print(json.dumps({k: res[k] for k in ("v9_i1_top_keys", "elapsed_s_count", "elapsed_s_sum",
                                      "meta_in_json", "lib_versions")}, indent=2, ensure_ascii=False))
print("\n--- per engine ---")
for eng, info in per_engine.items():
    if "error" in info:
        print(eng, info)
        continue
    print(f"{eng}: rows={info['rows']} wells={info['n_wells']} labels={info['y_cols']}")
    for w, c in info["pos_per_well_per_label"].items():
        print(f"   {w}: {c}")
