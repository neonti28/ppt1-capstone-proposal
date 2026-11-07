import json
d=json.load(open("scratch/rnd/s1/s1_hyd_seeds.json"))
for r in d["per_seed"]["42"]["folds"]:
    if r["model"]=="rule_kanal":
        print(r["fold"], "tp",r["rows"]["tp"],"fp",r["rows"]["fp"],"prec",round(r["rows"]["precision"],4),
              "rec",round(r["rows"]["recall"],4),"far_baris",r["far24_baris"])
