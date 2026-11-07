import json, pathlib
p = pathlib.Path("/mnt/d/Capstone 1(v2)/scratch/rnd/s5/s5_ledger_resolve2.json")
d = json.loads(p.read_text(encoding="utf-8"))
for k in ("S1", "S2", "S3", "S4"):
    print("=" * 60)
    print(k, d[k]["kelas"], "n_baris", d[k]["n_baris"])
    print(" mismatch:", len(d[k]["mismatch"]))
    for m in d[k]["mismatch"][:12]:
        print("   ", m.get("kode"), "|", m.get("sel") or ("ledger=%s disk=%s" % (m.get("ledger"), m.get("disk"))),
              "|", m.get("berkas"), m.get("jalur"), "| cocok", m.get("cocok"))
    print(" tak-resolve contoh:")
    for t in d[k]["tidak_resolve"][:12]:
        print("   ", t)
