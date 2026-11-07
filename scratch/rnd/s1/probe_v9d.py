import json
p='/mnt/d/Capstone 1(v2)/scratch/v9_i1/v9_i1_RESULTS.json'
d=json.load(open(p))
h=[e for e in d['engines'] if e['engine']=='hyd'][0]
print("klaim:", h['klaim_tugas'])
print("jenis:", h['jenis_tugas'])
for hd in h['heads']:
    print("\n=== HEAD:", list(hd.keys()))
    print(json.dumps(hd, indent=1)[:4000])
