"""Probe 3: do raw Norway files carry any date/time column? identity columns?"""
import pandas as pd, glob

for f in sorted(glob.glob('data/USROP/Code/Norway*.csv')):
    df = pd.read_csv(f, nrows=5000, low_memory=False)
    cols = list(df.columns)
    timecols = [c for c in cols if any(k in c.lower() for k in
                ['date', 'time', 'tim', 'day', 'year', 'clock'])]
    ident = [c for c in cols if c in ('name', 'nameWellbore', 'nameWell', 'dTim', 'Pass Name unitless')]
    print('===', f, '| ncols=', len(cols))
    print('   time-like:', timecols[:20])
    for c in ident:
        print('   ', c, '->', list(df[c].dropna().unique()[:5]))
