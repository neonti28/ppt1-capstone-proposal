import json
d=json.load(open("scratch/v9_i1/v9_i1_RESULTS.json"))
print("TYPE",type(d).__name__)
if isinstance(d,dict): print("KEYS",list(d.keys()))
def find(o,path="",hits=None,dep=0):
    if hits is None: hits=[]
    if dep>4: return hits
    if isinstance(o,dict):
        for k,v in o.items():
            if "hyd" in str(k).lower(): hits.append((path+"/"+str(k), type(v).__name__))
            find(v,path+"/"+str(k),hits,dep+1)
    elif isinstance(o,list):
        for i,v in enumerate(o[:5]): find(v,path+f"[{i}]",hits,dep+1)
    return hits
h=find(d)
print("HYD PATHS:")
for x in h[:25]: print("  ",x)
