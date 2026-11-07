import json, pathlib, re
d = json.loads(pathlib.Path("/mnt/d/Capstone 1(v2)/scratch/rnd/s5/s5_klaim.json").read_text(encoding="utf-8"))
for i, x in enumerate(d, 1):
    print(i, x["kartu"], "|", x["klaim"], "|", x["berkas"], "|", x["jalur"], "|", x.get("nilai_json"))
