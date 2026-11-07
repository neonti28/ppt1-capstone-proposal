import json, pathlib
d = json.loads(pathlib.Path("/mnt/d/Capstone 1(v2)/scratch/rnd/s5/s5_resolve3.json").read_text(encoding="utf-8"))
for a in d["artefak"]:
    print(a["kartu"], a["berkas"], a["bytes"], a["top"], a["n_top"], a.get("catatan", ""))
