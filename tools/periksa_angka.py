import csv, glob, json, math, statistics, zipfile, ast, re, pathlib, sys
from datetime import datetime

ROOT = pathlib.Path('/mnt/d/ARCT-9F2')
hasil = {}

# 1) label kejadian
lab = list(csv.DictReader(open(ROOT/'data/volve/labels_curated_v2.csv', encoding='utf-8')))
f = '%Y-%m-%dT%H:%M:%S%z'
dur = sorted((datetime.strptime(x['act_end'], f) - datetime.strptime(x['act_start'], f)).total_seconds()/60 for x in lab)
n = len(dur)
hasil['kejadian'] = n
hasil['wellbore'] = len({x['wellbore'] for x in lab})
hasil['total_menit'] = round(sum(dur))
hasil['median_menit'] = statistics.median(dur)
hasil['p90_menit'] = dur[math.ceil(0.9*n)-1]
hasil['maks_menit'] = dur[-1]
selaras = [x for x in dur if 0 <= x <= 720]
hasil['kejadian_720'] = len(selaras)
hasil['menit_720'] = round(sum(selaras))
kat = {}
for x in lab:
    kat[x['category']] = kat.get(x['category'], 0) + 1
hasil['kategori'] = sorted(kat.values(), reverse=True)
bha = {}
for x in lab:
    bha[x['bha_relevant']] = bha.get(x['bha_relevant'], 0) + 1
hasil['bha_relevan'] = bha

# 2) mutu kanal per sumur
kanal = {}
for fn in sorted(glob.glob(str(ROOT/'data/volve/witsml_parsed/*.qc.json'))):
    q = json.load(open(fn, encoding='utf-8'))
    kanal[pathlib.Path(fn).name.replace('.qc.json', '')] = q['n_channels_ge_50pct']
hasil['kanal'] = kanal
hasil['kanal_min'] = min(kanal.values())
hasil['kanal_max'] = max(kanal.values())

# 3) matriks fitur
b = zipfile.ZipFile(ROOT/'data/predictive/features_timeseries_controls_berdata.npz').read('X.npy')
off = 10 if b[6] == 1 else 12
hlen = int.from_bytes(b[8:off], 'little')
h = ast.literal_eval(b[off:off+hlen].decode('latin1'))
hasil['fitur_baris'], hasil['fitur_kolom'] = h['shape']

# 4) registry head
d = json.load(open(ROOT/'dashboard/data/engine_v9_i1.json', encoding='utf-8'))
heads = d['heads']
hasil['head'] = len(heads)
hasil['human_review'] = sum(1 for x in heads if x.get('human_review'))
tier = {}
lap = {}
for x in heads:
    tier[x.get('tier')] = tier.get(x.get('tier'), 0) + 1
    lap[x.get('layer')] = lap.get(x.get('layer'), 0) + 1
hasil['tier'] = tier
hasil['lapisan'] = lap
hasil['auto_alarm'] = d.get('kpi', {}).get('auto_alarm_slots', sum(1 for x in heads if x.get('tier') == 'ALARM-OTOMATIS'))

# 5) lipatan
man = json.load(open(ROOT/'docs/evidence/folds_per_dataset.json', encoding='utf-8'))
hasil['lipatan'] = man['total_lipatan']

# 6) baris dataset latih
tot = 0
for fn in glob.glob(str(ROOT/'scratch/v9_d1/datasets/*.csv.gz')):
    import gzip
    with gzip.open(fn, 'rt', encoding='utf-8') as fh:
        tot += max(sum(1 for _ in fh) - 1, 0)
hasil['dataset_baris'] = tot

# 7) tier per mode dari dokumen evaluasi
teks = (ROOT/'docs/V9_EVAL_C_LAYERC.md').read_text(encoding='utf-8').split('\n')
mulai = next(i for i, l in enumerate(teks) if l.startswith('## 1. TABEL RINGKAS'))
tier_baris = []
for l in teks[mulai:mulai+40]:
    if not l.startswith('|'):
        continue
    sel = [c.strip() for c in l.strip('|').split('|')]
    if len(sel) < 6 or 'TIER' in sel[0] or set(sel[0]) <= set('-: '):
        continue
    tier_baris.append((sel[0], sel[5]))
peringatan = set()
for nama, t in tier_baris:
    if 'PERINGATAN' in t.upper():
        bersih = re.sub(r'[*`]', '', nama).split()[0]
        peringatan.add(bersih)
hasil['klaim_terbaca'] = len(tier_baris)
hasil['mode_peringatan'] = len(peringatan)
hasil['mode_peringatan_daftar'] = sorted(peringatan)

pathlib.Path('/home/neonti/.hermes/cache/scratch/angka_terhitung.json').write_text(json.dumps(hasil, indent=1, ensure_ascii=False), encoding='utf-8')

# pembanding terhadap nilai yang tertulis di naskah
harap = {
    'kejadian': 884, 'wellbore': 10, 'total_menit': 73500, 'median_menit': 45,
    'p90_menit': 180, 'maks_menit': 780, 'kanal_min': 28, 'kanal_max': 48,
    'fitur_kolom': 480, 'head': 27, 'human_review': 13, 'lipatan': 37,
    'dataset_baris': 292954, 'mode_peringatan': 6, 'auto_alarm': 0,
    'kejadian_720': 883, 'menit_720': 72720,
}
gagal = 0
for k, v in harap.items():
    ada = hasil.get(k)
    ok = (ada == v)
    gagal += 0 if ok else 1
    print(f"{'COCOK ' if ok else 'BEDA  '} {k:16} naskah {v:>8} | hitung {ada}")

print('tier head      :', hasil['tier'])
print('lapisan head   :', hasil['lapisan'])
print('kategori       :', hasil['kategori'])
print('bha_relevan    :', hasil['bha_relevan'])
print('kanal per sumur:', hasil['kanal'])
print('klaim terbaca  :', hasil['klaim_terbaca'], '| mode peringatan:', hasil['mode_peringatan_daftar'])
print('SELISIH:', gagal)
sys.exit(1 if gagal else 0)
