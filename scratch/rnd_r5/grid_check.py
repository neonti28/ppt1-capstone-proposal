#!/usr/bin/env python3
"""R5 — cek struktur grid hyd_ki (apakah blok pendek artefak atau nyata).

Pertanyaan: apakah ts_bin benar-benar kelipatan 60 detik dan bersambung, atau
blok 6-28 menit pada percobaan sebelumnya adalah artefak persyaratan kontigu
yang terlalu ketat? Keluaran dipakai untuk memutuskan cara mengukur FAR.
"""
import gzip
import csv
import collections
import json
import os

BASE = "/mnt/d/Capstone 1(v2)"
SRC = os.path.join(BASE, "scratch/v9_d1/datasets/hyd_ki.csv.gz")
OUT = os.path.join(BASE, "scratch/rnd_r5/grid_structure.json")

def main():
    per_well = collections.defaultdict(list)
    cols = None
    n = 0
    with gzip.open(SRC, "rt", newline="", encoding="utf-8") as f:
        rd = csv.DictReader(f)
        cols = rd.fieldnames
        for r in rd:
            n += 1
            try:
                ts = float(r["ts_bin"])
            except (TypeError, ValueError):
                continue
            per_well[r["well"]].append(ts)
    out = {"meta": {"sumber": SRC, "n_rows": n, "n_cols": len(cols), "kolom": cols}, "per_well": {}}
    for w in sorted(per_well):
        v = sorted(per_well[w])
        d = [v[i + 1] - v[i] for i in range(len(v) - 1)]
        cnt = collections.Counter(int(round(x)) for x in d)
        # panjang run bila delta <= 90 s dianggap sambung
        best = cur = 1
        for x in d:
            if x <= 90:
                cur += 1
                best = max(best, cur)
            else:
                cur = 1
        # panjang run bila delta tepat 60
        best60 = cur60 = 1
        for x in d:
            if int(round(x)) == 60:
                cur60 += 1
                best60 = max(best60, cur60)
            else:
                cur60 = 1
        out["per_well"][w] = {
            "n": len(v),
            "ts_min": v[0],
            "ts_max": v[-1],
            "span_minutes": round((v[-1] - v[0]) / 60.0, 1),
            "delta_top5_seconds": [[k, c] for k, c in cnt.most_common(5)],
            "delta_mod60_nonzero": sum(c for k, c in cnt.items() if k % 60 != 0),
            "longest_run_minutes_delta_le_90": best,
            "longest_run_minutes_delta_eq_60": best60,
        }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    print(json.dumps(out["per_well"], indent=1, ensure_ascii=False))
    print("N_ROWS", n)

if __name__ == "__main__":
    main()
