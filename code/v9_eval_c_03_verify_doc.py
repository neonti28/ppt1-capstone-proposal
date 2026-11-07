#!/usr/bin/env python3
"""V9-EVAL_C — 03: verifikasi dokumen vs acceptance criteria task."""
import json, os, re, time

DOC = '/mnt/d/Capstone 1(v2)/docs/V9_EVAL_C_LAYERC.md'
JSN = '/mnt/d/Capstone 1(v2)/scratch/v9_eval_c/v9_eval_c_RESULTS.json'
txt = open(DOC).read()
fails = []

def chk(name, cond, detail=''):
    print(('PASS ' if cond else 'FAIL ') + name + (' | ' + detail if detail else ''))
    if not cond:
        fails.append(name)

# (a) 7 engine dinilai
for e in ['vib', 'ssi', 'shk', 'stuck', 'hyd', 'bit_wear', 'tool_wear']:
    chk(f'(a) engine {e} ada', e in txt)
claims = ['stuck K-i', 'stuck K-ii', 'hyd K-i', 'hyd K-ii', 'bit_wear K-1', 'tool_wear K-i', 'tool_wear K-ii']
for c in claims:
    chk(f'(a) klaim {c}', c in txt)

# (b) metrik dari eksekusi nyata
chk('(b) RESULTS.json ada', os.path.exists(JSN))
chk('(b) skrip compute ada', os.path.exists('/mnt/d/Capstone 1(v2)/code/v9_eval_c_01_compute.py'))
chk('(b) verify 13/13', '13/13 PASS' in txt or '13/13' in txt)
chk('(b) json mtime < doc mtime', os.path.getmtime(JSN) < os.path.getmtime(DOC),
    f"{time.ctime(os.path.getmtime(JSN))} < {time.ctime(os.path.getmtime(DOC))}")

# (c) baseline relevan
chk('(c) baseline canary', 'canary' in txt)
chk('(c) baseline persistence', 'persistence' in txt)
chk('(c) baseline rule status-quo', 'status-quo' in txt or 'rule' in txt)
chk('(c) far<=6 gerbang', 'FAR≤6' in txt)

# (d) tidak ada vonis biner — regex uppercase LULUS/GAGAL di luar konteks negasi
hits = []
for m in re.finditer(r'\b(LULUS|GAGAL)\b', txt):
    ctx = txt[max(0, m.start()-60):m.end()+60]
    if any(k in ctx for k in ['BUKAN', 'bukan', 'tanpa vonis', 'TIDAK', 'tidak']):
        continue
    hits.append(ctx.replace('\n', ' '))
chk('(d) tanpa vonis biner', len(hits) == 0, f'{len(hits)} hit')
# tiap klaim punya 'belum' + 'memenuhi'
chk('(d) memenuhi+belum per dokumen', txt.count('Memenuhi') + txt.count('memenuhi') >= 7
    and txt.count('belum') + txt.count('Belum') >= 10)

# riset pendahuluan
for s in ['scientific-critical-thinking', 'verification-mandatory', 'statistical-analysis',
          'what-if-oracle', 'consciousness-council', 'sequentialthinking']:
    chk(f'riset {s}', f'Riset pendahuluan: {s}' in txt)

# tier ditetapkan per engine
for e in ['TREN', 'PERINGATAN-BERPENGAWAS', 'ALARM-OTOMATIS']:
    chk(f'tier {e} disebut', e in txt)

# RESULT json lengkap 11 klaim
d = json.load(open(JSN))
keys_ok = (len(d['C_ml']) == 4 and len(d['C_rule_status']) == 5 and 'hyd_ki_persistence' in d['C_stat']
           and 'stuck_E2' in d['C_stat'] and 'hyd_kii_fisher_variant' in d['C_stat']
           and 'stuck_k2' in d['C_onset'] and 'K1' in d['C_bitwear']
           and 'K_i' in d['C_toolwear'] and 'K_ii' in d['C_toolwear'])
chk('JSON 11-klaim lengkap', keys_ok)

print(f'\nTOTAL fails={len(fails)}')
for f in fails:
    print(' FAIL:', f)
with open('/mnt/d/Capstone 1(v2)/scratch/v9_eval_c/v9_eval_c_VERIFY_DOC.txt', 'w') as f:
    f.write(f'fails={len(fails)}\n' + '\n'.join(fails))
