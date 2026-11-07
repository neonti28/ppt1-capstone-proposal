"""Probe 8: provenance of 'Diameter mm' - inspect raw Norway file columns for name/Diameter/bit."""
import pandas as pd, glob

for f in sorted(glob.glob('data/USROP/Code/Norway*.csv'))[:3] + [
        'data/USROP/Code/Norway-StatoilHydro-15_$47$_9-F-15 depth .csv',
        'data/USROP/Code/Norway-StatoilHydro-15_$47$_9-F-15S depth.csv']:
    df = pd.read_csv(f, nrows=3000, low_memory=False)
    hits = [c for c in df.columns if 'name' in c.lower() or 'diam' in c.lower() or 'bit' in c.lower()]
    print('===', f.split('/')[-1])
    print('   matching cols:', hits)
    for c in hits:
        vals = df[c].dropna().unique()[:6]
        print(f'   {c!r} sample: {list(vals)}')

print('\n=== intermediate data/USROP/USROP_A * files (pipeline output) ===')
for f in sorted(glob.glob('data/USROP/USROP_A*.csv'))[3:5]:
    df = pd.read_csv(f, nrows=2000)
    print('===', f.split('/')[-1], list(df.columns))
    print('   Diameter mm uniques:', sorted(df['Diameter mm'].dropna().unique())[:8])
