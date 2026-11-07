#!/usr/bin/env python3
"""J2 ekstraksi baris jendela berlabel STUCK_RT dari WITSML terparse.

Streaming satu baris per iterasi (hemat memori WSL). Menyimpan baris dalam
span berlabel [first_labeled - margin, last_labeled + margin] per burst,
dengan kolom fitur + STUCK_RT ke CSV ringkas per wellbore.
"""
import csv
import sys
from datetime import datetime, timedelta

BASE = "/mnt/d/Capstone 1/data/volve/witsml_parsed"
OUT = "/mnt/d/Capstone 1/data/predictive/j2_stuck"
MARGIN = timedelta(minutes=15)

WELLS = {
    "F-9_A": ["SPPA", "TQA", "TFLO", "HKLD", "SWOB", "RPM", "ROP", "BPOS", "DEPT"],
    "F-9":   ["SPPA", "TQA", "TFLO", "HKLD", "SWOB", "NRPM_RT", "ROP", "BPOS", "DEPT"],
    "F-14":  ["SPPA", "TQA", "TFLO", "HKLD", "SWOB", "RPM", "ROP", "BPOS", "DEPT"],
}


def parse_ts(s):
    s = s.strip().replace("Z", "")
    for fmt in ("%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            pass
    return None


def main():
    import os
    os.makedirs(OUT, exist_ok=True)
    for well, cols in WELLS.items():
        src = f"{BASE}/{well}.csv"
        # pass 1: burst spans dari baris berlabel
        spans = []
        cur = None
        n_labeled = 0
        with open(src, newline="") as fh:
            r = csv.reader(fh)
            header = [c.strip() for c in next(r)]
            si = header.index("STUCK_RT")
            ti = header.index("timestamp")
            for row in r:
                if row[si] == "":
                    continue
                t = parse_ts(row[ti])
                if t is None:
                    continue
                n_labeled += 1
                if cur is None:
                    cur = [t, t]
                elif t - cur[1] <= timedelta(hours=6):
                    cur[1] = t
                else:
                    spans.append(tuple(cur))
                    cur = [t, t]
        if cur is not None:
            spans.append(tuple(cur))
        spans = [(a - MARGIN, b + MARGIN) for a, b in spans]
        print(f"{well}: labeled={n_labeled} bursts={len(spans)} "
              f"span={[ (str(a), str(b)) for a,b in spans ]}", flush=True)

        # pass 2: ekstrak baris dalam span
        out_path = f"{OUT}/{well}_window.csv"
        kept = 0
        with open(src, newline="") as fh, open(out_path, "w", newline="") as out:
            r = csv.reader(fh)
            header = [c.strip() for c in next(r)]
            ti = header.index("timestamp")
            si = header.index("STUCK_RT")
            idx = {c: header.index(c) for c in cols}
            w = csv.writer(out)
            w.writerow(["timestamp", "STUCK_RT"] + cols)
            for row in r:
                t = parse_ts(row[ti])
                if t is None:
                    continue
                if not any(a <= t <= b for a, b in spans):
                    continue
                rec = [row[ti], row[si]]
                for c in cols:
                    rec.append(row[idx[c]] if idx[c] < len(row) else "")
                w.writerow(rec)
                kept += 1
        print(f"{well}: kept={kept} -> {out_path}", flush=True)


if __name__ == "__main__":
    sys.exit(main())
