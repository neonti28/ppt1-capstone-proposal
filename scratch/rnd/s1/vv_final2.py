import json
d=json.load(open("scratch/rnd/s1/s1_hluas.json"))
print("per_fold[0] keys:", list(d["per_fold"][0].keys()))
print(json.dumps(d["per_fold"][0], indent=1)[:700])
