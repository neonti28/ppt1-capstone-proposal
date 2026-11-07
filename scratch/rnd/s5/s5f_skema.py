import json, pathlib
S5 = pathlib.Path("/mnt/d/Capstone 1(v2)/scratch/rnd/s5")
for n in ["s5_rerun_audit", "s5_negatif", "s5_resolve3", "s5_kode_doi_lapisan", "s5_klaim", "a1_struktur"]:
    p = S5 / (n + ".json")
    print("=" * 20, n, p.exists())
    if not p.exists():
        continue
    d = json.loads(p.read_text(encoding="utf-8"))
    if isinstance(d, dict):
        print("  top:", list(d.keys()))
        for k, v in d.items():
            if isinstance(v, dict):
                print("   ", k, "-> dict keys", list(v.keys())[:12])
            elif isinstance(v, list):
                print("   ", k, "-> list len", len(v), "first:", json.dumps(v[0], ensure_ascii=False)[:220] if v else None)
            else:
                print("   ", k, "=", v)
    else:
        print("  list len", len(d), "first:", json.dumps(d[0], ensure_ascii=False)[:300])
