import json
d = json.load(open("/mnt/d/Capstone 1(v2)/scratch/rnd_e0/probe01_kolom.json"))
for k in ["vib", "ssi", "hyd_ki"]:
    v = d[k]
    print("=" * 70)
    print(k, "| semua kolom:")
    print(v["kolom"])
    print("| fitur:")
    print(v["fitur"])
