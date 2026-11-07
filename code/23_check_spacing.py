"""Cek jarak sampling md USROP (untuk klaim di laporan)."""
import pandas as pd, numpy as np

u = pd.read_csv('data/USROP_labeled.csv', usecols=['well', 'Measured Depth m'])
parts = []
for _, g in u.groupby('well'):
    parts.append(np.diff(np.sort(g['Measured Depth m'].to_numpy())))
a = np.concatenate(parts)
print('spacing m: min=%.4f median=%.4f p99=%.4f max=%.4f' %
      (a.min(), np.median(a), np.percentile(a, 99), a.max()))
print('n negatif:', int((a < 0).sum()))
print('n baris per well (sorted?):')
for w, g in u.groupby('well'):
    s = g['Measured Depth m'].to_numpy()
    print('  %-28s terurut=%s  n=%d' % (w, bool((np.diff(s) >= 0).all()), len(s)))
