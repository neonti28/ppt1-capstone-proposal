#!/usr/bin/env python3
"""V9-E_RULE 02b — PERBAIKAN dataset stuck_k2 (kolom meta ts_bin/lab_ts NaN).

BUG (direproduksi, scratch/v9_e_rule/_repro_insert_bug.py):
  code/v9_d1_04_stuck_k2.py baris 227/229 memakai
    sub.insert(1, "ts_bin", lab_ts_all[mask].astype(np.int64))
    sub.insert(3, "lab_ts", lab_ts_out[mask])
  keduanya Series ber-index DatetimeIndex; DataFrame.insert ME-ALIGN-kan Series
  ke index integer sub -> SEMUA nilai NaN (numpy array tidak terpengaruh).
Dampak: ts_bin & lab_ts kosong di 118.567/118.567 baris; checker anti-bocor
  v9_d1_05 (mask both=notna) menguji 0 baris -> "0 pelanggaran" VAKUUM.

REPAIR: salinan resep v9_d1_04 VERBATIM + fix .to_numpy() pada 2 insert.
Output: scratch/v9_e_rule/repair/stuck_k2.csv.gz (+ per-well + QC).
Verifikasi (script 02c): baris/positif/y identik dgn file asli; ts_bin/lab_ts
  non-null; invarian onset V8 cocok; anti-bocor NYATA (feat_ts_max < lab_ts).
"""
import json
import os
import subprocess
import sys
import time
import numpy as np
import pandas as pd

SEED = 42
np.random.seed(SEED)

BASE = "/mnt/d/Capstone 1(v2)"
SRC = f"{BASE}/code/v9_d1_04_stuck_k2.py"          # sumber resep (VERBATIM)
OUT = f"{BASE}/scratch/v9_e_rule/repair"
QC_DIR = OUT
os.makedirs(OUT, exist_ok=True)

WELLS = ["F-9", "F-9_A", "F-10", "F-14"]
REF_ONSETS = {"F-9_A": 72, "F-14": 61, "F-10": 93}
log_lines = []


def log(m):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {m}"
    print(line, flush=True)
    log_lines.append(line)


def main():
    t0 = time.time()
    src = open(SRC).read()
    # FIX 1+2: Series -> numpy sebelum insert (alignment bug)
    a_old = 'sub.insert(1, "ts_bin", lab_ts_all[mask].astype(np.int64))'
    a_new = ('sub.insert(1, "ts_bin",\n'
             '                lab_ts_all[mask].to_numpy().astype(np.int64))')
    b_old = 'sub.insert(3, "lab_ts", lab_ts_out[mask])'
    b_new = 'sub.insert(3, "lab_ts", lab_ts_out[mask].to_numpy())'
    assert a_old in src and b_old in src, "pola insert tidak cocok — resep berubah?"
    src = src.replace(a_old, a_new).replace(b_old, b_new)
    # arahkan output ke direktori repair
    src = src.replace(f'OUT = "{BASE}/scratch/v9_d1/datasets"',
                      f'OUT = "{OUT}"')
    src = src.replace(f'QC_DIR = "{BASE}/scratch/v9_d1"',
                      f'QC_DIR = "{QC_DIR}"')
    assert f'OUT = "{OUT}"' in src and f'QC_DIR = "{QC_DIR}"' in src, \
        "gagal mengarahkan OUT/QC_DIR"
    patched = f"{BASE}/code/_repair_k2_patched.py"
    open(patched, "w").write(src)

    # jalankan 4 well (resume bila artefak per-well sudah ada) + merge
    r = subprocess.run([sys.executable, patched], capture_output=True, text=True)
    log(r.stdout[-6000:])
    if r.returncode != 0:
        log(r.stderr[-4000:])
        raise SystemExit(f"gagal rc={r.returncode}")
    log(f"-> selesai {round(time.time() - t0, 1)} s")


if __name__ == "__main__":
    main()
