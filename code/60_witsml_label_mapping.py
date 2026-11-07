#!/usr/bin/env python3
"""T10 — Diskriminasi pemetaan label wellbore -> file WITSML (bukti, bukan tebakan).

Tes: untuk tiap event label (act_start + md valid), cari baris CSV pada jendela
+-DELTa jam di sekitar act_start, lalu ukur selisih depth minimum |depth - md|.
Kandidat mapping yang BENAR harus menunjukkan banyak event dengan depth-match
kecil; mapping yang salah menunjukkan match sedikit/tidak ada.

Output: scratch/t10/mapping_matrix.json + tabel stdout.
"""
import pandas as pd, numpy as np, glob, os, json, itertools

LAB = 'data/volve/labels_curated_v2.csv'
PARSED = 'data/volve/witsml_parsed'
DELTA_H = 6.0
DEPTH_TOL = 30.0  # meter

lab = pd.read_csv(LAB)
lab['t'] = pd.to_datetime(lab['act_start'], utc=True, errors='coerce')
lab = lab[lab['t'].notna() & lab['md_valid'] & lab['md'].notna()].copy()
print(f'events usable (act_start + md valid): {len(lab)}')

DEP = ['DMEA', 'DEPT', 'DBTM']
res = {}
for f in sorted(glob.glob(PARSED + '/*.csv')):
    name = os.path.basename(f)[:-4]
    cols = list(pd.read_csv(f, nrows=0).columns)
    use = [c for c in DEP if c in cols]
    if 'timestamp' not in cols or not use:
        print(name, 'SKIP', use)
        continue
    df = pd.read_csv(f, usecols=['timestamp'] + use)
    t = pd.to_datetime(df['timestamp'], utc=True, errors='coerce')
    valid = t.notna().values
    tvals = t[valid].astype('int64').values
    order = np.argsort(tvals, kind='mergesort')
    tvals = tvals[order]
    depth = {}
    for c in use:
        d = pd.to_numeric(df.loc[valid, c], errors='coerce').values[order]
        depth[c] = d
    del df, t

    per_wb = {}
    for wb, sub in lab.groupby('wellbore'):
        tsec = (sub['t'].astype('int64') / 1e9).values
        md = sub['md'].values
        hit = 0
        mindiffs = []
        for ts, m in zip(tsec, md):
            lo = np.searchsorted(tvals, (ts - DELTA_H * 3600) * 1e9)
            hi = np.searchsorted(tvals, (ts + DELTA_H * 3600) * 1e9)
            if hi <= lo:
                continue
            best = np.inf
            for c in use:
                d = depth[c][lo:hi]
                d = d[(d > 0) & (d < 8000)]
                if d.size:
                    best = min(best, float(np.min(np.abs(d - m))))
            if np.isfinite(best):
                mindiffs.append(best)
                if best <= DEPTH_TOL:
                    hit += 1
        mdn = len(sub)
        med = float(np.median(mindiffs)) if mindiffs else None
        per_wb[wb] = {'n_lab': mdn, 'n_with_rows': len(mindiffs), 'n_depth_hit': hit,
                      'frac_hit': round(hit / mdn, 3), 'median_abs_dmd': med}
    res[name] = per_wb
    print(f'--- {name} ---')
    for wb, v in sorted(per_wb.items(), key=lambda kv: -kv[1]['frac_hit']):
        print(f"   {wb:16s} n={v['n_lab']:3d} rows={v['n_with_rows']:3d} "
              f"hit={v['n_depth_hit']:3d} frac={v['frac_hit']:.3f} med|dmd|={v['median_abs_dmd']}")

os.makedirs('scratch/t10', exist_ok=True)
json.dump(res, open('scratch/t10/mapping_matrix.json', 'w'), indent=1)
print('wrote scratch/t10/mapping_matrix.json')
