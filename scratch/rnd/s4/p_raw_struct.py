import json
d = json.load(open('/mnt/d/Capstone 1(v2)/scratch/rnd/s4/inventory_raw.json', encoding='utf-8'))
def walk(o, p="", depth=0):
    if depth > 3:
        return
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, (dict, list)):
                print(f"{p}.{k} <{type(v).__name__} len={len(v)}>")
                walk(v, f"{p}.{k}", depth + 1)
            else:
                print(f"{p}.{k} = {v}")
    elif isinstance(o, list) and o and isinstance(o[0], dict):
        print(f"{p}[0] keys = {list(o[0].keys())}")
walk(d)
