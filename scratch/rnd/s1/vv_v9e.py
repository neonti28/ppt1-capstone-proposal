import json
d=json.load(open("scratch/v9_i1/v9_i1_RESULTS.json"))
h=d["engines"][4]
print("engine:",h["engine"],"| heads type:",type(h["heads"]).__name__,"n:",len(h["heads"]))
print(json.dumps(h["heads"], indent=1)[:4000])
