import json

a = json.load(open("/mnt/d/Capstone 1(v2)/scratch/rnd/s3/s3a_feasibility.json"))
for r in a["waktu_kalender"]["per_well"]:
    print(r["well"][:28], "|", r.get("rentang_jam"), "|", r.get("ts_min"), "|", r.get("ts_maks"))
