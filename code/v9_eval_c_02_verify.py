#!/usr/bin/env python3
"""
V9-EVAL_C — 02: verifikasi independen hasil 01.
(a) recompute terpisah (path kode berbeda) utk metrik kunci per kelas;
(b) rekonsiliasi vs EVAL_A (angka yang sama harus cocok);
(c) cek selisih & laporkan.
"""
import json, os, math

BASE = '/mnt/d/Capstone 1(v2)/scratch'
def load(p):
    with open(os.path.join(BASE, p)) as f:
        return json.load(f)

R1 = load('v9_eval_c/v9_eval_c_RESULTS.json')
fails, checks = [], 0

def chk(name, cond, detail=''):
    global checks
    checks += 1
    if not cond:
        fails.append(f'{name}: {detail}')
    print(('PASS ' if cond else 'FAIL ') + name + (' | ' + detail if detail else ''))

# ---- V1: recompute FAR dispersion vib RF tau0,5 manual ----
ml = load('v9_e_ml/v9_e_ML_vib_RESULTS.json')
fars = sorted(f['models']['rf']['tau_metrics']['0.5']['FAR_24jam'] for f in ml['folds'] if not f['underpowered'])
d = R1['C_ml']['vib']['rf']['far_by_tau']['0.5']['FAR_disp']
chk('V1 vib FAR tau0.5 min==min', abs(d['min']-fars[0]) < 1e-9, f"{d['min']} vs {fars[0]}")
chk('V1b vib FAR tau0.5 max==max', abs(d['max']-fars[-1]) < 1e-9, f"{d['max']} vs {fars[-1]}")

# ---- V2: recompute CI-contains-prev shk RF dari mentah ----
ml = load('v9_e_ml/v9_e_ML_shk_RESULTS.json')
layak = [f for f in ml['folds'] if not f['underpowered']]
cnt_layak = sum(1 for f in layak if f['models']['rf']['ci95'][0] <= f['prev_test'] <= f['models']['rf']['ci95'][1])
cnt_all = sum(1 for f in ml['folds'] if f['models']['rf']['ci95'][0] <= f['prev_test'] <= f['models']['rf']['ci95'][1])
chk('V2 shk CIprev layak 7/9', cnt_layak == 7 and len(layak) == 9, f'{cnt_layak}/{len(layak)}; all={cnt_all}/9 (EVAL_A: 7/9)')

# ---- V3: rekonsiliasi ssi CIprev (EVAL_A 5/9 all-fold; evaluator 3/7 layak) ----
ml = load('v9_e_ml/v9_e_ML_ssi_RESULTS.json')
layak = [f for f in ml['folds'] if not f['underpowered']]
up = [f for f in ml['folds'] if f['underpowered']]
c_layak = sum(1 for f in layak if f['models']['rf']['ci95'][0] <= f['prev_test'] <= f['models']['rf']['ci95'][1])
c_up = sum(1 for f in up if f['models']['rf']['ci95'][0] <= f['prev_test'] <= f['models']['rf']['ci95'][1])
chk('V3 ssi CIprev rekonsiliasi 3/7 layak + 2 UP = 5/9 all',
    c_layak == 3 and c_up == 2 and (c_layak + c_up) == 5,
    f'layak={c_layak}/7, UP={c_up}/2, all={c_layak+c_up}/9 == EVAL_A 5/9')

# ---- V4: recompute Wilson CI utk shk rule fold F-10 ----
def wilson(k, n, z=1.959963985):
    p = k/n; dd = 1+z*z/n; c = p+z*z/(2*n); r = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))
    return [round((c-r)/dd, 4), round((c+r)/dd, 4)]
rs = load('v9_e_rule/v9_e_RULE_01_status_results.json')
f10 = [f for f in rs['classes']['shk']['folds'] if f['test_well'] == 'F-10'][0]
e = f10['rule_display_t0minus1']
mine = wilson(e['tp'], e['tp']+e['fp'])
stored = [x for x in R1['C_rule_status']['shk']['rule_display_t0minus1']['wilson_ci95_precision'] if x['well'] == 'F-10'][0]
chk('V4 Wilson shk F-10 presisi', mine == stored['ci'], f'{mine} vs {stored["ci"]}; TP={e["tp"]} FP={e["fp"]}')

# ---- V5: recompute hybrid FP cut hyd_ki ----
layak = [f for f in rs['classes']['hyd_ki']['folds'] if not f['underpowered']]
fr = sum(f['rule_display_t0minus1']['fp'] for f in layak)
fh = sum(f['hybrid_rule_and_persistence']['fp'] for f in layak)
stored = R1['C_rule_status']['hyd_ki']['hybrid_fp_cut']
chk('V5 hyd_ki hybrid FP 2091->927', fr == 2091 and fh == 927 and stored['rule_FP'] == fr and stored['hybrid_FP'] == fh,
    f'{fr}->{fh} stored {stored["rule_FP"]}->{stored["hybrid_FP"]} (EVAL_A: 2091->927)')

# ---- V6: recompute anchor gap stuck ----
gap = load('v9_e_rule/v9_e_RULE_02e_gap_root_cause.json')
tot_o = sum(g['n_onsets'] for g in gap.values()); tot_m = sum(g['n_missing'] for g in gap.values())
a = R1['C_onset']['stuck_k2']['anchor_gap']
chk('V6 anchor gap 13/281', tot_o == 281 and tot_m == 13 and a['n_onsets_total'] == 281 and a['n_missing_anchors'] == 13,
    f'{tot_m}/{tot_o} frac={a["frac"]}')

# ---- V7: recompute tool_wear partC TLead disp ----
tw = load('v9_e_stat/v9_e_stat_03_tool_wear_RESULTS.json')
t1 = [x['TLead_s'] for x in tw['part_C_operating_far_calibrated'] if x['target_fp_per_min'] == 1.0]
d = R1['C_toolwear']['K_i']['partC_TLead_disp']
chk('V7 tool_wear TLead disp', d['min'] == min(t1) and d['max'] == max(t1) and d['n'] == 4, f'{d} vs {sorted(t1)}')

# ---- V8: recompute fisher sign-flip frac ----
fp = load('v9_e_stat/v9_e_stat_04_fisher_pearson_RESULTS.json')
v = fp['engine_fisher_pearson_variant']
frac = round(v['sign_flip_windows']/v['n_test'], 4)
chk('V8 fisher sign-flip 0.7866', frac == R1['C_stat']['hyd_kii_fisher_variant']['sign_flip_frac'] == 0.7866,
    f'{v["sign_flip_windows"]}/{v["n_test"]}={frac}')

# ---- V9: recompute bitwear scorable & dB ----
bwh = load('v9_e_rule/v9_e_RULE_03_bitwear_toolwear_results.json')['bitwear_k1']
sc = [f for f in bwh['folds'] if f['persistence']['auprc'] is not None]
pos = sum(1 for f in sc if f['persistence']['auprc'] > f['canary_depth']['auprc'])
chk('V9 bitwear 5/5 scorable & pers>canary', len(sc) == 5 and pos == 5
    and R1['C_bitwear']['K1']['n_scorable'] == 5 and R1['C_bitwear']['K1']['dB_pers_vs_canary_pos'] == '5/5',
    f'scorable={len(sc)} pos={pos}')

# ---- V10: determinisme E_STAT hash (independen) ----
import hashlib
def hsh(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()
ok_files = 0
for name in ['v9_e_stat_01_hyd_ki_RESULTS.json', 'v9_e_stat_02_stuck_e2_RESULTS.json',
             'v9_e_stat_03_tool_wear_RESULTS.json', 'v9_e_stat_04_fisher_pearson_RESULTS.json']:
    a = json.load(open(os.path.join(BASE, 'v9_e_stat', name)))
    b = json.load(open(os.path.join(BASE, 'v9_e_stat', '_det_a', name)))
    # buang elapsed lalu compare
    for obj in (a, b):
        obj.get('summary', {}).pop('elapsed_s', None)
        obj.get('meta', {}).pop('elapsed_s', None)
    if a == b:
        ok_files += 1
chk('V10 E_STAT rerun identik kecuali elapsed_s', ok_files == 4, f'{ok_files}/4 file (semantic-equal)')

# ---- V11: recompute E2 CIprev 4/4 ----
e2 = load('v9_e_stat/v9_e_stat_02_stuck_e2_RESULTS.json')
c = sum(1 for f in e2['folds'] if f['engine_E2_stats']['ci95_auprc'][0] <= f['prev'] <= f['engine_E2_stats']['ci95_auprc'][1])
chk('V11 E2 CIprev 4/4', c == 4 and R1['C_stat']['stuck_E2']['ci95_contains_prev_folds']['n'] == '4/4', f'{c}/4')

# ---- V12: recompute hyd_ki STAT CIprev 0/9 ----
st = load('v9_e_stat/v9_e_stat_01_hyd_ki_RESULTS.json')
c = sum(1 for f in st['folds'] if f['engine_persistence']['ci95_auprc'][0] <= f['prev'] <= f['engine_persistence']['ci95_auprc'][1])
chk('V12 hyd_ki STAT CIprev 0/9', c == 0 and R1['C_stat']['hyd_ki_persistence']['ci95_contains_prev_folds']['n'] == '0/9', f'{c}/9')

print(f'\nTOTAL {checks} checks, {len(fails)} FAIL')
for x in fails:
    print('  FAIL:', x)
with open(os.path.join(BASE, 'v9_eval_c', 'v9_eval_c_VERIFY.txt'), 'w') as f:
    f.write(f'{checks} checks, {len(fails)} FAIL\n')
    for x in fails:
        f.write('FAIL: ' + x + '\n')
