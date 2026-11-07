import re, os
base = '/mnt/d/Capstone 1(v2)/docs'
files = ['V10_D1_BAB_DATA.md','V10_R1_ALASAN.md','V10_E_ML_BAB.md','V10_E_STAT_BAB.md','V10_E_RULE_BAB.md','V10_EVAL_BAB.md']
for f in files:
    p = os.path.join(base,f)
    txt = open(p, encoding='utf-8').read()
    lines = txt.split('\n')
    # find first '---' separator (standalone)
    seps = [i for i,l in enumerate(lines) if l.strip()=='---']
    first_h2 = next((i for i,l in enumerate(lines) if l.startswith('## ')), None)
    print('='*70)
    print(f)
    print('  first --- at line', [s+1 for s in seps[:4]])
    print('  first "## " at line', first_h2+1 if first_h2 is not None else None)
    print('  last 3 lines:', repr(lines[-3:]))
    # count of task-card tokens
    for tok in ['Task:', 'Papan:', 'Peran', 't_', 'Riset pendahuluan', 'lulus bersyarat', 'v3_arsip', 'board', 'capstone-v9']:
        c = txt.count(tok)
        if c: print('   token %-20s x%d' % (tok, c))
