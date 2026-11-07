import json, pathlib
d = json.loads(pathlib.Path("/mnt/d/Capstone 1(v2)/scratch/rnd/s5/s5_rerun_audit.json").read_text(encoding="utf-8"))
seen = []
for x in d["banding_dok_51"]:
    print(x["metrik"], x["seed"], x["dokumen"], x["ukur_ulang"], x["lulus"])
