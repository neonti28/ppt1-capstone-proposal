import json
d=json.load(open("scratch/v9_i1/v9_i1_RESULTS.json"))
for i,e in enumerate(d["engines"]):
    print(f"=== [{i}] {e['engine']} | tugas={e.get('jenis_tugas')} | tier={e.get('sumber_tier')}")
    hd=e.get("heads")
    if isinstance(hd,dict):
        for name,h in hd.items():
            if isinstance(h,dict):
                keys=list(h.keys())
                print(f"    head={name} keys={keys}")
                print("      ", json.dumps(h)[:500])
