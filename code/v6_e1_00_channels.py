#!/usr/bin/env python3
"""V6-E1 step 0: eksplorasi kanal label per sumur di data NYATA.

Tujuan: sebelum merancang kelas, hitung ketersediaan & populasi kanal label
instrumen (STUCK_RT, STKSLP, STICK_RT, VIBLAT_RT, SHKRSK_RT, CRPM_RT) per file.
Output: JSON ringkas di scratch/v6_e1/ + stdout.
"""
import csv
import json
import os
import sys

PARSED = "/mnt/d/Capstone 1/data/volve/witsml_parsed"
TIME_CSV = "/mnt/d/Capstone 1/data/witsml/Norway-NA-15_47_9-F-9 A time.csv"
OUT = "/mnt/d/Capstone 1/scratch/v6_e1/ch00_channels.json"

CANDIDATES = ["STUCK_RT", "STKSLP", "STICK_RT", "VIBLAT_RT", "SHKRSK_RT",
              "WHIRL_RT", "BOUNCE_RT", "CRPM_RT", "DTOR_RT", "DWOB_RT",
              "TQA", "SPPA", "TFLO", "RPM", "SWOB", "ROKE", "MSE"]


def scan(path, candidates, max_rows=None):
    res = {"path": path, "exists": os.path.exists(path)}
    if not res["exists"]:
        return res
    with open(path, newline="") as fh:
        rd = csv.reader(fh)
        try:
            hdr = next(rd)
        except StopIteration:
            res["error"] = "empty"
            return res
        res["n_cols"] = len(hdr)
        res["columns"] = hdr
        idx = {}
        for c in candidates:
            if c in hdr:
                idx[c] = hdr.index(c)
        res["candidates_present"] = sorted(idx)
        counts = {c: 0 for c in idx}
        nonzero = {c: 0 for c in idx}
        total = 0
        for i, row in enumerate(rd):
            total += 1
            for c, j in idx.items():
                if j < len(row):
                    v = row[j].strip()
                    if v not in ("", "NaN", "nan", "--", "None"):
                        counts[c] += 1
                        try:
                            if float(v) != 0.0:
                                nonzero[c] += 1
                        except ValueError:
                            nonzero[c] += 1
            if max_rows and total >= max_rows:
                res["truncated"] = True
                break
    res["rows"] = total
    res["nonnull"] = counts
    res["nonzero"] = nonzero
    return res


def main():
    out = {"parsed_witsml": {}, "f9a_time": None}
    for f in sorted(os.listdir(PARSED)):
        if not f.endswith(".csv"):
            continue
        out["parsed_witsml"][f] = scan(os.path.join(PARSED, f), CANDIDATES)
    # time.csv F-9 A sangat besar (427 MB) -> hitung penuh tapi hemat memori
    out["f9a_time"] = scan(TIME_CSV, CANDIDATES)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1)
    # ringkas
    for f, r in out["parsed_witsml"].items():
        print(f"== {f}: rows={r.get('rows')} cols={r.get('n_cols')}")
        print("   present:", r.get("candidates_present"))
        print("   nonzero:", {k: v for k, v in (r.get("nonzero") or {}).items()})
    t = out["f9a_time"]
    print(f"== F-9 A time.csv: rows={t.get('rows')} cols={t.get('n_cols')}")
    print("   present:", t.get("candidates_present"))
    print("   nonzero:", t.get("nonzero"))
    print("saved:", OUT)


if __name__ == "__main__":
    sys.exit(main())
