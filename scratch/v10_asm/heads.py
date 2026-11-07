import re, os, glob
base = '/mnt/d/Capstone 1(v2)/docs'
files = ['V10_D1_BAB_DATA.md','V10_R1_ALASAN.md','V10_E_ML_BAB.md','V10_E_STAT_BAB.md','V10_E_RULE_BAB.md','V10_EVAL_BAB.md']
for f in files:
    p = os.path.join(base,f)
    txt = open(p, encoding='utf-8').read()
    lines = txt.split('\n')
    print('='*80)
    print(f, '|', len(lines), 'lines |', len(txt), 'chars')
    print('='*80)
    for i,l in enumerate(lines):
        if re.match(r'^#{1,4}\s', l):
            print('  L%d: %s' % (i+1, l[:120]))
    print()
