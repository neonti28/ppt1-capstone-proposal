import json
B = "/mnt/d/Capstone 1(v2)"
r8 = json.load(open(f"{B}/scratch/rnd/r8/r8_hyd.json"))
for m in r8["ringkas"]:
    print(m, json.dumps(r8["ringkas"][m]))
