import json, pathlib
d = json.loads(pathlib.Path("/mnt/d/Capstone 1(v2)/scratch/rnd/s5/s5_resolve3.json").read_text(encoding="utf-8"))
for k in ("S1", "S2", "S3", "S4"):
    v = d["ledger"][k]
    print("==", k, "MISMATCH:", v["kelas_hasil"].get("MISMATCH", 0))
    for m in v.get("mismatch", []):
        print("   ", json.dumps(m, ensure_ascii=False)[:400])
