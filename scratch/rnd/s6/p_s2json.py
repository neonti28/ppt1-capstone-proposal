import json

BASE = "/mnt/d/Capstone 1(v2)"
for k in ("vib", "ssi"):
    d = json.load(open(f"{BASE}/scratch/rnd/s2/s2_records_{k}.json"))
    print("=" * 50, k, type(d).__name__)
    if isinstance(d, dict):
        print(" keys:", list(d.keys())[:12])
        for kk, vv in list(d.items())[:6]:
            print("  ", kk, type(vv).__name__, len(vv) if isinstance(vv, (list, dict)) else vv)
        # cari list of records
        for kk, vv in d.items():
            if isinstance(vv, list) and vv and isinstance(vv[0], dict):
                print("   list rec di", kk, "n", len(vv), "keys contoh", list(vv[0].keys())[:12])
                print("   contoh:", {x: vv[0][x] for x in list(vv[0])[:8] if not isinstance(vv[0][x], (list, dict))})
                break
