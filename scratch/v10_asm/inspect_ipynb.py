import json, sys
from collections import Counter

path = '/mnt/d/Capstone 1(v2)/docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.ipynb'
nb = json.load(open(path, encoding='utf-8'))
cells = nb['cells']
print('total cells:', len(cells))
print(Counter(c['cell_type'] for c in cells))
for i, c in enumerate(cells):
    src = ''.join(c['source'])
    first = src.strip().split('\n')[0][:100] if src.strip() else '<empty>'
    nlines = src.count('\n') + 1
    print(i, c['cell_type'], 'lines=%d' % nlines, '|', first)
print('--- meta ---')
print(json.dumps(nb.get('metadata', {}), indent=1)[:800])
