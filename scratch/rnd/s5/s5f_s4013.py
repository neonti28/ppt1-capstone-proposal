import json, pathlib
p = pathlib.Path("/mnt/d/Capstone 1(v2)/scratch/rnd/s5/s5_resolve3.json")
d = json.loads(p.read_text(encoding="utf-8"))
print("S4 keys:", list(d["ledger"]["S4"].keys()))
txt = p.read_text(encoding="utf-8")
i = txt.find("S4-013")
print("konteks S4-013 di resolve3:", txt[max(0, i-400):i+300] if i >= 0 else "TIDAK ADA")
# cari kelas baris lewat daftar tidak_resolve
for k in ("S1", "S2", "S3", "S4"):
    tr = d["ledger"][k].get("tidak_resolve", [])
    hit = [x for x in tr if isinstance(x, dict) and x.get("kode") == "S4-013"]
    if hit:
        print("S4-013 ada di tidak_resolve:", json.dumps(hit[0], ensure_ascii=False)[:300])
