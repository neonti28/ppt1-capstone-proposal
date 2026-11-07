"""V9-E_RULE 05 — gerbang determinisme: rerun skrip 01-04, JSON fold wajib identik.

Bandingan menstrip field temporal (meta.generated_at) lalu deep-compare.
Exit code 1 bila ada selisih -> dokumen tidak boleh diterbitkan.
"""
import json
import subprocess
import sys
import time

BASE = "/mnt/d/Capstone 1(v2)"
OUT = f"{BASE}/scratch/v9_e_rule"
SCRIPTS = ["v9_e_RULE_01_status.py", "v9_e_RULE_02_stuck_onset.py",
           "v9_e_RULE_03_bitwear_toolwear.py", "v9_e_RULE_04_hyd_k2.py"]
JSONS = ["v9_e_RULE_01_status_results.json", "v9_e_RULE_02_stuck_onset_results.json",
         "v9_e_RULE_03_bitwear_toolwear_results.json",
         "v9_e_RULE_04_hyd_k2_results.json"]


def strip(o):
    if isinstance(o, dict):
        return {k: strip(v) for k, v in o.items()
                if k not in ("generated_at", "elapsed_s", "fit_time_s")}
    if isinstance(o, list):
        return [strip(x) for x in o]
    return o


before = {j: strip(json.load(open(f"{OUT}/{j}"))) for j in JSONS}
fail = []
for s in SCRIPTS:
    t0 = time.time()
    r = subprocess.run([sys.executable, f"{BASE}/code/{s}"],
                       capture_output=True, text=True)
    print(f"rerun {s}: rc={r.returncode} ({round(time.time()-t0,1)}s)")
    if r.returncode != 0:
        print(r.stderr[-2000:])
        fail.append(s)
after = {j: strip(json.load(open(f"{OUT}/{j}"))) for j in JSONS}
for j in JSONS:
    same = before[j] == after[j]
    print(f"{j}: identik={same}")
    if not same:
        fail.append(j)
print("DETERMINISM:", "PASS" if not fail else f"FAIL {fail}")
sys.exit(1 if fail else 0)
