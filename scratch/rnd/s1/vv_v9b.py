import json
d=json.load(open("scratch/v9_i1/v9_i1_RESULTS.json"))
print("=== segmen_info/hyd_ki ===")
print(json.dumps(d["segmen_info"]["hyd_ki"], indent=1)[:1500])
e=d["engines"]
print("\n=== engines type ===", type(e).__name__, list(e.keys())[:30] if isinstance(e,dict) else len(e))
def show(o,dep=0):
    if dep>2: return
    if isinstance(o,dict):
        for k,v in o.items():
            if "hyd" in str(k).lower() or "rule" in str(k).lower() or "persist" in str(k).lower():
                print("  "*dep, k, type(v).__name__, (list(v.keys())[:12] if isinstance(v,dict) else (len(v) if hasattr(v,'__len__') else v)))
            show(v,dep+1)
    elif isinstance(o,list):
        for i,v in enumerate(o[:3]): show(v,dep+1)
show(e)
