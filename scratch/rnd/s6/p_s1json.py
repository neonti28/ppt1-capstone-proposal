import json, os, glob

BASE = "/mnt/d/Capstone 1(v2)"
d = json.load(open(f"{BASE}/scratch/rnd/s1/s1_hyd_seeds.json"))
print("S1 keys:", list(d.keys()))
for k, v in d.items():
    print(" ", k, type(v).__name__, (len(v) if isinstance(v, (list, dict)) else v))

# cari record H1 seed 42 per fold
def cari(o, path="root"):
    if isinstance(o, dict):
        for k, v in o.items():
            cari(v, f"{path}.{k}")
    elif isinstance(o, list):
        if o and isinstance(o[0], dict) and "model" in o[0]:
            print("LIST of records di", path, "n=", len(o))
            for r in o:
                if r.get("model") == "H1_stat_dan_rule" and r.get("seed") == 42:
                    print("   ", r.get("fold"), "fp", r["rows"]["fp"], "tp", r["rows"]["tp"], "h", r.get("h_terpilih"))
        else:
            for i, v in enumerate(o[:3]):
                cari(v, f"{path}[{i}]")

cari(d)

print("\nBINS mtimes:")
for f in sorted(glob.glob(f"{BASE}/scratch/v9_d1/bins/*.csv.gz")):
    print(" ", os.path.basename(f), os.path.getmtime(f))
