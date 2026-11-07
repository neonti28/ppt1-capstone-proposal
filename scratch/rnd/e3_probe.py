#!/usr/bin/env python3
"""RND-E3 probe: verifikasi lingkungan + struktur dataset hyd K-i sebelum run pilot."""
import json, sys, os, hashlib, subprocess, datetime
import numpy as np
import pandas as pd

BASE = "/mnt/d/Capstone 1(v2)"
DS = f"{BASE}/scratch/v9_d1/datasets/hyd_ki.csv.gz"
OUT = f"{BASE}/scratch/rnd/e3"
os.makedirs(OUT, exist_ok=True)

rep = {}
rep["python"] = sys.version.split()[0]
for mod in ("numpy", "pandas", "sklearn", "scipy", "statsmodels", "lightgbm"):
    try:
        m = __import__(mod)
        rep[mod] = getattr(m, "__version__", "unknown")
    except Exception as e:
        rep[mod] = f"MISSING: {type(e).__name__}: {e}"

df = pd.read_csv(DS)
rep["dataset_path"] = DS
rep["dataset_sha256"] = hashlib.sha256(open(DS, "rb").read()).hexdigest()
rep["shape"] = list(df.shape)
rep["columns"] = list(df.columns)
rep["dtypes"] = {c: str(t) for c, t in df.dtypes.items()}
wellcol = "well" if "well" in df.columns else ("well_id" if "well_id" in df.columns else None)
rep["well_col"] = wellcol
if wellcol:
    rep["n_wells"] = int(df[wellcol].nunique())
    rep["per_well"] = {str(k): int(v) for k, v in df.groupby(wellcol).size().items()}
if "y_hyd" in df.columns:
    rep["y_overall_mean"] = float(df["y_hyd"].mean())
    rep["y_per_well"] = {str(k): float(v) for k, v in df.groupby(wellcol)["y_hyd"].mean().items()}
    rep["pos_per_well"] = {str(k): int(v) for k, v in df.groupby(wellcol)["y_hyd"].sum().items()}
rep["n_dupe_rows"] = int(df.duplicated().sum())
rep["nan_counts"] = {c: int(v) for c, v in df.isna().sum().items() if v > 0}
rep["head3"] = df.head(3).to_dict(orient="records")
rep["timestamp"] = datetime.datetime.now().isoformat(timespec="seconds")

with open(f"{OUT}/e3_probe.json", "w") as f:
    json.dump(rep, f, indent=2, default=str)

freeze = subprocess.run([sys.executable, "-m", "pip", "freeze"],
                        capture_output=True, text=True)
with open(f"{OUT}/pip_freeze.txt", "w") as f:
    f.write(freeze.stdout)
env = {
    "python": sys.version,
    "pip_freeze_sha256": hashlib.sha256(freeze.stdout.encode()).hexdigest(),
    "pip_freeze_returncode": freeze.returncode,
    "pip_freeze_stderr": freeze.stderr[-2000:],
    "captured_at": datetime.datetime.now().isoformat(timespec="seconds"),
    "command": "python3 -m pip freeze",
}
with open(f"{OUT}/e3_env.json", "w") as f:
    json.dump(env, f, indent=2)

print(json.dumps(rep, indent=2, default=str)[:4000])
print("---FREEZE RC---", freeze.returncode, "lines", len(freeze.stdout.splitlines()))
print("---STDERR---", freeze.stderr[-800:])
