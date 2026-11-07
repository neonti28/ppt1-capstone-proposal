import json, pathlib
B = pathlib.Path("/mnt/d/Capstone 1(v2)")
inv = json.loads((B / "scratch/rnd/s4/inventory.json").read_text(encoding="utf-8"))
mb = inv["metrik_lapisan_b"]
for k, v in mb.items():
    print(k, "->", json.dumps(v, ensure_ascii=False)[:220])
