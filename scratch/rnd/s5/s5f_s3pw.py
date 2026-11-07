import json, pathlib
B = pathlib.Path("/mnt/d/Capstone 1(v2)")
d = json.loads((B / "scratch/rnd/s3/s3a_feasibility.json").read_text(encoding="utf-8"))
pw = d["label"]["per_well"]
print(type(pw))
if isinstance(pw, dict):
    for k, v in pw.items():
        print(" ", k, v if not isinstance(v, dict) else {kk: v[kk] for kk in v if "preval" in kk or kk in ("n_pos", "n_baris", "n_well")})
else:
    for v in pw:
        print(" ", {kk: v[kk] for kk in v if "preval" in kk or kk in ("well", "n_pos", "n_baris")})
