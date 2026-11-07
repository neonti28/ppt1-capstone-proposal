import json, statistics
d = json.load(open("scratch/rnd/r8/r8_hyd.json"))
print("KEYS:", list(d.keys()))
def walk(o, pre="", depth=0):
    if depth>2: return
    if isinstance(o, dict):
        for k,v in list(o.items())[:14]:
            print("  "*depth, pre+str(k), type(v).__name__, (len(v) if hasattr(v,"__len__") else v))
            walk(v, "", depth+1)
print("--- struktur ---")
walk(d)
