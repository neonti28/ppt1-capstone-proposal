import json, os, glob
base = '/mnt/d/Capstone 1(v2)'
# 1) forbidden phrase search across docs
import re
hits=[]
for p in glob.glob(base+'/docs/*.md')+[base+'/CHANGELOG.md']:
    try: t=open(p,encoding='utf-8').read()
    except: continue
    for i,l in enumerate(t.split('\n')):
        if 'lulus bersyarat' in l.lower() or 'bersyarat' in l.lower():
            hits.append((os.path.basename(p), i+1, l.strip()[:120]))
print('=== "bersyarat" hits:', len(hits))
for h in hits[:40]: print(h)

# 2) ipynb tail cells 24..36 sources
nb=json.load(open(base+'/docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.ipynb',encoding='utf-8'))
print('\n=== cell24 (arsip) ===')
print(''.join(nb['cells'][24]['source']))
print('\n=== code cell ids/heads ===')
for i in range(25,37):
    c=nb['cells'][i]
    s=''.join(c['source'])
    print(i, c['cell_type'], 'outputs=%d'%len(c.get('outputs',[])), 'exec=%s'%c.get('execution_count'), '|', s.split('\n')[0][:70])
