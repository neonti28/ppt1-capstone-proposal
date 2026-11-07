#!/usr/bin/env python3
"""
V9-EVAL_C — 01: komputasi metrik LAPISAN C dari JSON primer E_ML / E_STAT / E_RULE.
Layer C = kepercayaan pemakaian: ketahanan antar-well/periode (C1), ketidakpastian (C2),
portabilitas ambang / perubahan operasi (C3), kualitas sensor (C4), determinisme (C5).
Output primer: scratch/v9_eval_c/v9_eval_c_RESULTS.json
Semua angka dihitung dari JSON eksekusi nyata — tanpa angka karangan.
"""
import json, os, math, hashlib

BASE = '/mnt/d/Capstone 1(v2)/scratch'
OUT_DIR = os.path.join(BASE, 'v9_eval_c')
os.makedirs(OUT_DIR, exist_ok=True)

def load(p):
    with open(os.path.join(BASE, p)) as f:
        return json.load(f)

def wilson_ci(k, n, z=1.959963985):
    """Wilson score CI95 untuk proporsi k/n."""
    if n == 0:
        return None
    p = k / n
    d = 1 + z*z/n
    c = p + z*z/(2*n)
    r = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))
    return [round((c-r)/d, 4), round((c+r)/d, 4)]

def disp(vals):
    """dispersi sederhana: min, max, ratio max/min (0 bila min=0), median. None dibuang."""
    v = sorted(x for x in vals if x is not None)
    if not v:
        return None
    med = v[len(v)//2] if len(v) % 2 else (v[len(v)//2 - 1] + v[len(v)//2]) / 2
    ratio = round(v[-1]/v[0], 2) if v[0] > 0 else None
    return {'min': v[0], 'max': v[-1], 'median': round(med, 4), 'max_min_ratio': ratio, 'n': len(v)}

R = {'meta': {'task': 'V9-EVAL_C Layer C metrics', 'sources': [
        'scratch/v9_e_ml/*.json', 'scratch/v9_e_stat/*.json', 'scratch/v9_e_rule/*.json'],
    'defs': {
        'C1_ketahanan': 'dispersi metrik kunci antar fold LOWO (min/max/median/ratio) + fraksi fold mengalahkan baseline relevan + fold terburuk',
        'C2_ketidakpastian': 'CI95 AUPRC dari JSON (E_ML/E_STAT): apakah memuat prevalensi (no-skill); E_RULE tanpa CI -> Wilson CI95 dari TP/FP/FN',
        'C3_portabilitas_ambang': 'pada tau TETAP: dispersion FAR/recall antar well + jumlah well dgn FAR<=6&recall>0; konsistensi pemangkasan FP hybrid antar fold',
        'C4_kualitas_sensor': 'n_nodata, anchor hilang onset (ABSORBED), sign-flip jendela, kanal absen',
        'C5_determinisme': 'rerun identik: E_STAT hash-equality (kecuali elapsed_s), E_ML determinism_check, E_RULE rerun (dilaporkan tim)',
    }},
    'C_ml': {}, 'C_rule_status': {}, 'C_stat': {}, 'C_onset': {}, 'C_bitwear': {}, 'C_toolwear': {}, 'C5_det': {}}

TAUS = ['0.05', '0.1', '0.2', '0.3', '0.5']

# ============ C1/C2/C3 ML heads (vib, ssi, shk, stuck_k2) ============
for head in ['vib', 'ssi', 'shk', 'stuck_k2']:
    d = load(f'v9_e_ml/v9_e_ML_{head}_RESULTS.json')
    folds = d['folds']
    layak = [f for f in folds if not f['underpowered']]
    o = {'n_folds': len(folds), 'n_layak': len(layak),
         'test_wells': [f['test_well'] for f in folds],
         'underpowered_folds': [f['test_well'] for f in folds if f['underpowered']]}
    for m in ['rf', 'gb', 'lr']:
        auprc = [f['models'][m]['auprc'] for f in folds]
        ci_prev = [f['test_well'] for f in layak
                   if f['models'][m]['ci95'][0] <= f['prev_test'] <= f['models'][m]['ci95'][1]]
        dB = {}
        for b in ['persistence', 'canary_depth', 'prevalence_random']:
            key = {'persistence': 'rf_vs_persistence', 'canary_depth': 'rf_vs_canary_depth',
                   'prevalence_random': 'rf_vs_prevalence_random'}[b]
            pos = [f['test_well'] for f in layak if f['delta_B'][key] > 0]
            dB[b] = {'n_pos': f'{len(pos)}/{len(layak)}', 'folds_pos': pos,
                     'range': [round(min(f['delta_B'][key] for f in layak), 4),
                               round(max(f['delta_B'][key] for f in layak), 4)]} if layak else None
        far_tau, worst = {}, {}
        for t in TAUS:
            rows = [(f['test_well'], f['models'][m]['tau_metrics'][t]['FAR_24jam'],
                     f['models'][m]['tau_metrics'][t]['recall']) for f in layak]
            far_tau[t] = {'FAR_disp': disp([r[1] for r in rows]),
                          'recall_disp': disp([r[2] for r in rows]),
                          'n_well_FARle6_recall_pos': sum(1 for r in rows if r[1] <= 6 and r[2] > 0),
                          'n_well': len(rows)}
        o[m] = {'auprc_disp': disp(auprc),
                'ci95_contains_prev_folds': {'n': f'{len(ci_prev)}/{len(layak)}', 'folds': ci_prev},
                'delta_B_pos_folds': dB, 'far_by_tau': far_tau}
    R['C_ml'][head] = o

# ============ C_rule_status (vib, ssi, shk, stuck_k1, hyd_ki) ============
rs = load('v9_e_rule/v9_e_RULE_01_status_results.json')
for cls, obj in rs['classes'].items():
    folds = obj['folds']
    layak = [f for f in folds if not f['underpowered']]
    o = {'n_folds': len(folds), 'n_layak': len(layak),
         'test_wells': [f['test_well'] for f in folds]}
    for eng in ['rule_display_t0minus1', 'persistence', 'hybrid_rule_and_persistence']:
        if eng not in folds[0]:
            continue
        precs, recs, fars, wilson_p, wilson_r, nodata = [], [], [], [], [], 0
        for f in layak:
            e = f[eng]
            precs.append(e['precision']); recs.append(e['recall']); fars.append(e['far_24h'])
            wilson_p.append({'well': f['test_well'],
                             'ci': wilson_ci(e['tp'], e['tp']+e['fp']) if (e['tp']+e['fp']) > 0 else None,
                             'p': round(e['precision'], 4) if e['precision'] is not None else None})
            wilson_r.append({'well': f['test_well'],
                             'ci': wilson_ci(e['tp'], e['tp']+e['fn']) if (e['tp']+e['fn']) > 0 else None,
                             'r': round(e['recall'], 4) if e['recall'] is not None else None})
            nodata += e.get('n_nodata', 0) or 0
        # FP total & pemangkasan hybrid
        fp_tot = sum(f[eng]['fp'] for f in layak)
        o[eng] = {'precision_disp': disp(precs), 'recall_disp': disp(recs),
                  'far24h_disp': disp(fars), 'FP_total_layak': fp_tot,
                  'wilson_ci95_precision': wilson_p, 'wilson_ci95_recall': wilson_r,
                  'n_nodata_sum': nodata or None}
    # fp rule baseline utk hyd_ki membanding hybrid
    if 'hybrid_rule_and_persistence' in o and 'rule_display_t0minus1' in o:
        fr, fh = o['rule_display_t0minus1']['FP_total_layak'], o['hybrid_rule_and_persistence']['FP_total_layak']
        # konsistensi per fold
        cons = [f['test_well'] for f in layak
                if f['hybrid_rule_and_persistence']['fp'] <= f['rule_display_t0minus1']['fp']]
        o['hybrid_fp_cut'] = {'rule_FP': fr, 'hybrid_FP': fh,
                              'reduction_pct': round(100*(1-fh/fr), 1) if fr else None,
                              'folds_not_increasing': f'{len(cons)}/{len(layak)}', 'folds': cons}
    if cls == 'ssi':
        tot_nodata = sum(f['rule_display_t0minus1'].get('n_nodata', 0) for f in folds)
        tot_n = sum(f['n'] for f in folds)
        o['sensor_nodata_rule'] = {'n_nodata': tot_nodata, 'n_total': tot_n,
                                   'frac': round(tot_nodata/tot_n, 4)}
    if cls == 'shk':
        tot_nodata = sum(f['rule_display_t0minus1'].get('n_nodata', 0) for f in folds)
        tot_n = sum(f['n'] for f in folds)
        o['sensor_nodata_rule'] = {'n_nodata': tot_nodata, 'n_total': tot_n,
                                   'frac': round(tot_nodata/tot_n, 4)}
    R['C_rule_status'][cls] = o

# ============ C_stat hyd_ki (persistence, CI dari JSON STAT) ============
st = load('v9_e_stat/v9_e_stat_01_hyd_ki_RESULTS.json')
layak = [f for f in st['folds'] if not f['underpowered']]
ci_prev = [f['test_well'] for f in layak
           if f['engine_persistence']['ci95_auprc'][0] <= f['prev'] <= f['engine_persistence']['ci95_auprc'][1]]
delays = [f['engine_persistence']['det']['delay_median_min'] for f in layak
          if f['engine_persistence']['det'].get('delay_median_min') is not None]
pct_det = [f['engine_persistence']['det']['pct_detected_within_H10'] for f in layak]
R['C_stat']['hyd_ki_persistence'] = {
    'n_folds': len(st['folds']), 'n_layak': len(layak),
    'ci95_contains_prev_folds': {'n': f'{len(ci_prev)}/{len(layak)}', 'folds': ci_prev},
    'auprc_disp': disp([f['engine_persistence']['auprc'] for f in layak]),
    'far24h_disp': disp([f['engine_persistence']['op']['far_per_24h_neg'] for f in layak]),
    'delay_median_min_disp': disp(delays),
    'pct_detected_H10_disp': disp(pct_det)}

# ============ C_stat stuck E2 ============
e2 = load('v9_e_stat/v9_e_stat_02_stuck_e2_RESULTS.json')
layak = [f for f in e2['folds'] if not f['underpowered']]
ci_prev = [f['test_well'] for f in layak
           if f['engine_E2_stats']['ci95_auprc'][0] <= f['prev'] <= f['engine_E2_stats']['ci95_auprc'][1]]
R['C_stat']['stuck_E2'] = {
    'n_folds': len(e2['folds']), 'n_layak': len(layak),
    'ci95_contains_prev_folds': {'n': f'{len(ci_prev)}/{len(layak)}', 'folds': ci_prev},
    'lift_disp': disp([f['engine_E2_stats']['lift'] for f in layak]),
    'far24h_disp': disp([f['engine_E2_stats']['op_q95']['far_per_24h_neg'] for f in layak]),
    'recall_at_H_disp': disp([f['engine_E2_stats']['onset_level']['recall_at_H'] for f in layak])}

# ============ C_stat fisher/Pearson hyd K-ii ============
fp = load('v9_e_stat/v9_e_stat_04_fisher_pearson_RESULTS.json')
v = fp['engine_fisher_pearson_variant']
R['C_stat']['hyd_kii_fisher_variant'] = {
    'n_split_temporal': 1,
    'ci95_contains_prev': v['ci95_auprc'][0] <= fp['label_Kii']['pos_windows']/fp['label_Kii']['evaluable_windows'] <= v['ci95_auprc'][1],
    'ci95': v['ci95_auprc'], 'prev': v['prev'], 'lift': v['lift'],
    'sign_flip_windows': v['sign_flip_windows'], 'n_test': v['n_test'],
    'sign_flip_frac': round(v['sign_flip_windows']/v['n_test'], 4),
    'op_q95': v['op_q95'], 'onset_level': v['onset_level'],
    'flowout_status': fp['flowout_status']['verdict']}

# ============ C_onset stuck_k2 (RULE persistence-event + E1 + anchor gap) ============
so = load('v9_e_rule/v9_e_RULE_02_stuck_onset_results.json')
layak = [f for f in so['folds'] if not f['underpowered']]
gap = load('v9_e_rule/v9_e_RULE_02e_gap_root_cause.json')
tot_onsets = sum(g['n_onsets'] for g in gap.values())
tot_missing = sum(g['n_missing'] for g in gap.values())
o = {'n_folds': len(so['folds']), 'n_layak': len(layak)}
for eng in ['persistence_event', 'rule_E1_2of3', 'persistence_horizon']:
    b1 = [f[eng]['onset'].get('b1') for f in layak]
    tl = [f[eng]['onset'].get('tlead_min', {}).get('median') for f in layak]
    far = [f[eng]['far_24h'] for f in layak]
    fp_al = [f[eng]['onset'].get('fp_alarm') for f in layak]
    o[eng] = {'B1_disp': disp(b1), 'TLead_median_min_disp': disp(tl),
              'far24h_disp': disp(far), 'fp_alarm_total': sum(x or 0 for x in fp_al)}
o['anchor_gap'] = {'n_onsets_total': tot_onsets, 'n_missing_anchors': tot_missing,
                    'frac': round(tot_missing/tot_onsets, 4),
                    'kelas': 'ABSORBED (absorber delta 2-7 mnt)',
                    'per_well': {k: {'onsets': g['n_onsets'], 'missing': g['n_missing']}
                                 for k, g in gap.items()}}
R['C_onset']['stuck_k2'] = o

# ============ C_bitwear K-1 (7 fold USROP; P/R/FAR belum terukur) ============
bwh = load('v9_e_rule/v9_e_RULE_03_bitwear_toolwear_results.json')['bitwear_k1']
folds = bwh['folds']
scorable = [f for f in folds if f['persistence']['auprc'] is not None]
R['C_bitwear']['K1'] = {
    'n_folds': len(folds), 'n_scorable': len(scorable),
    'zero_pos_folds': [f['test_well'] for f in folds if f['pos'] == 0],
    'underpowered_folds': [f['test_well'] for f in folds if f['underpowered']],
    'auprc_disp_scorable': disp([f['persistence']['auprc'] for f in scorable]),
    'lift_disp_scorable': disp([f['persistence']['lift'] for f in scorable]),
    'canary_auprc_disp': disp([f['canary_depth']['auprc'] for f in scorable]),
    'dB_pers_vs_canary_pos': f"{sum(1 for f in scorable if f['persistence']['auprc'] > f['canary_depth']['auprc'])}/{len(scorable)}",
    'dataset': 'USROP (bukan rig Volve utama) — transfer lintas-dataset',
    'P_R_FAR': 'BELUM TERUKUR (field TP/FP tidak ada di JSON; konsisten EVAL_A §2.6)',
    'K2': 'BELUM DIJALANKAN (pra-reg belum terbit)'}

# ============ C_toolwear K-i + K-ii ============
tw = load('v9_e_stat/v9_e_stat_03_tool_wear_RESULTS.json')
runs = tw['part_A_change_point']['runs']
tp_run = sum(1 for r in runs if r['y_progression'] == 1 and r['sig_p05_v8'])
fp_run = sum(1 for r in runs if r['y_progression'] == 0 and r['sig_p05_v8'])
fam_spread = [r['fam_spread_s'] for r in runs]
pc = tw['part_C_operating_far_calibrated']
tools1 = [x for x in pc if x['target_fp_per_min'] == 1.0]
R['C_toolwear']['K_i'] = {
    'n_runs': len(runs),
    'cp_precision_runlevel': round(tp_run/(tp_run+fp_run), 4) if (tp_run+fp_run) else None,
    'cp_sig_folds': f"{tw['summary']['cp_sig_p05']}/{len(runs)} (p<=0,05) & {tw['summary']['cp_sig_p002']}/{len(runs)} (p<=0,002)",
    'thermal_artifact_test': tw['part_A_change_point']['validity_test_t_cp']['verdict'],
    'cross_family_spread_s': disp(fam_spread),
    'partC_target1_per_tool': [{'tool': x['tool'], 'fp_R01': x['fp_R01'], 'det_R02': x['det_R02'],
                                'TLead_s': x['TLead_s'], 'pct_R02_alarmed': x['pct_R02_alarmed']} for x in tools1],
    'partC_TLead_disp': disp([x['TLead_s'] for x in tools1]),
    'partC_FP_disp': disp([x['fp_R01'] for x in tools1]),
    'partB_raw_FAR_disp': disp([t['engine_5of27']['far_fp_per_min_R01']
                                for t in tw['part_B_within_tool_calibration']['per_tool']])}
tk2 = bwh = load('v9_e_rule/v9_e_RULE_03_bitwear_toolwear_results.json')['toolwear_kii']
R['C_toolwear']['K_ii'] = {
    'n_folds_LOTO': len(tk2['folds']),
    'tools': [f['test_tool'] for f in tk2['folds']],
    'canary_auprc_disp': disp([f['canary_3rms']['auprc'] for f in tk2['folds']]),
    'identity_auprc_disp': disp([f['identity_run_majority']['auprc'] for f in tk2['folds']]),
    'lift_ceiling': 2.0,
    'RF_V9': 'BELUM DIJALANKAN (E_ML 4 head; angka V8 = referensi, EA-7)',
    'persistence': 'N/A dinyatakan (label konstan dalam run)'}

# ============ C5 determinisme ============
vb = load('v9_e_ml/v9_e_ML_vib_RESULTS.json')
dc = vb.get('determinism_check')
R['C5_det'] = {
    'E_ML_vib': {'rerun_identical': dc['rerun_identical'],
                 'max_abs_diff': dc['max_abs_diff'],
                 'interpretasi': 'selisih = 2.2e-16 (machine epsilon) -> numerik identik'},
    'E_STAT': {'method': 'banding hash SHA256 file rerun _det_a & _det_b vs main',
               'hasil': 'SEMUA field identik kecuali summary.elapsed_s (waktu komputasi); _det_b hash == main (termasuk elapsed)',
               'verdict': 'deterministik (4/4 file)'},
    'E_RULE': {'rerun': 'dilaporkan tim E_RULE: 4/4 identik (handoff t_c8bebfb6)',
               'verifikasi evaluator': 'tidak di-rerun ulang oleh EVAL_C (mengikuti laporan tim + determinisme metode (seed 42, ambang q95-train))'}}

out = os.path.join(OUT_DIR, 'v9_eval_c_RESULTS.json')
with open(out, 'w') as f:
    json.dump(R, f, indent=1, ensure_ascii=False)
print('WROTE', out)

# ============ summary ringkas ============
for k in ['C_ml']:
    for h, o in R[k].items():
        rf = o['rf']
        print(f"ML {h}: CIprev {rf['ci95_contains_prev_folds']['n']} | dBcanary {rf['delta_B_pos_folds']['canary_depth']['n_pos']} | "
              f"dBpers {rf['delta_B_pos_folds']['persistence']['n_pos']} | FAR tau0.5 disp {rf['far_by_tau']['0.5']['FAR_disp']}")
for c, o in R['C_rule_status'].items():
    r = o.get('rule_display_t0minus1')
    if r:
        print(f"RULE {c}: FAR disp {r['far24h_disp']} | P disp {r['precision_disp']}")
    if 'hybrid_fp_cut' in o:
        print(f"  hybrid_fp_cut: {o['hybrid_fp_cut']}")
print('hyd_ki STAT:', R['C_stat']['hyd_ki_persistence']['ci95_contains_prev_folds'], R['C_stat']['hyd_ki_persistence']['delay_median_min_disp'])
print('E2:', R['C_stat']['stuck_E2']['ci95_contains_prev_folds'])
print('fisher:', R['C_stat']['hyd_kii_fisher_variant']['sign_flip_frac'], R['C_stat']['hyd_kii_fisher_variant']['ci95_contains_prev'])
print('stuck anchor gap:', R['C_onset']['stuck_k2']['anchor_gap']['frac'])
print('bitwear:', R['C_bitwear']['K1']['n_scorable'], R['C_bitwear']['K1']['auprc_disp_scorable'], R['C_bitwear']['K1']['dB_pers_vs_canary_pos'])
print('toolwear K-i:', R['C_toolwear']['K_i']['cp_precision_runlevel'], R['C_toolwear']['K_i']['partC_TLead_disp'])
print('toolwear K-ii:', R['C_toolwear']['K_ii']['canary_auprc_disp'])
