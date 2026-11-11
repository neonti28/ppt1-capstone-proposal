# CATATAN INTERNAL PENULIS: JEJAK BERKAS DAN PERINTAH

Berkas ini bukan bagian proposal dan tidak diserahkan sebagai lampiran. Isinya jejak kerja penulis: nama berkas, lokasi penyimpanan, dan perintah yang dipakai untuk memperoleh angka pada proposal. Proposal hanya memuat rumus, bahan hitung, dan status, sesuai aturan bahwa dokumen formal tidak memuat rujukan ke tata letak penyimpanan penulis.

## 1. Artefak bukti

| Berkas | Isi | Angka yang ditopang |
|---|---|---|
| `data/volve/labels_curated_v2.csv` | tabel label 884 kejadian, 10 wellbore, kolom waktu mulai, waktu selesai, kategori, relevansi BHA | A-07, A-08, A-17, 884, 10 wellbore, 73.500 menit, median 45, p90 180, maksimum 780, 50/571/263 |
| `data/volve/witsml_parsed/*.qc.json` | ringkasan mutu kanal per sumur, memuat medan `n_channels_ge_50pct` | A-19, 28 sampai 48 kanal |
| `data/predictive/features_timeseries_controls_berdata.npz` | matriks fitur latih, 3.958 baris kali 480 kolom | A-20, 480 fitur |
| `dashboard/data/engine_v9_i1.json` | registry 27 head beserta metrik, tier, penanda `human_review` | A-09, A-11, A-13, A-22, 27 head, 13 head wajib tinjauan |
| `docs/V9_EVAL_C_LAYERC.md` | tabel evaluasi lapisan keputusan per klaim | A-18, 6 dari 7 mode, 0 alarm otomatis, lead 4,5 sampai 8,5 menit |
| `docs/evidence/folds_per_dataset.json` | rekap cacah sumur tiap dataset latih, total 37 | A-21 |
| `docs/evidence/simv5_baseline.json` | keluaran simulator internal 1.200 run | A-01 sampai A-06 |
| `docs/evidence/h2o_kontrol.json`, `docs/evidence/dl_klipp99.json` | keluaran ablasi pemilihan otomatis dan uji klip | A-10 |
| `scratch/ppt1/ledger.json` | buku besar angka evaluasi, lift per fold | A-12 |
| `scratch/ppt1/v9_engine_heads_flat.json` | tabel datar 27 head | A-13 |
| `scratch/ppt1/mcdm.json` | keluaran TOPSIS, koefisien kedekatan tiap alternatif | A-14 |
| `docs/PPT1_LEDGER_ANGKA.md` | buku besar angka Bab I, cacah berkas log | A-15 |
| `scratch/v9_d1/datasets/*.csv.gz` | enam dataset latih per sumur, 292.954 baris, 66 MB | A-21, 292.954 baris |

Dataset latih dan data mentah WITSML tidak disertakan pada repositori karena ukuran dan lisensi. Angka lipatan dibuktikan lewat `docs/evidence/folds_per_dataset.json` yang disertakan.

## 2. Perintah pengulang

Dijalankan dari akar folder proyek. Semua perintah memakai pustaka standar Python 3.

```bash
# 884 kejadian, 73.500 menit, median 45, p90 180, maksimum 780
python3 - <<'AKHIR'
import csv, statistics, math
from datetime import datetime
r=list(csv.DictReader(open('data/volve/labels_curated_v2.csv',encoding='utf-8')))
f='%Y-%m-%dT%H:%M:%S%z'
d=sorted((datetime.strptime(x['act_end'],f)-datetime.strptime(x['act_start'],f)).total_seconds()/60 for x in r)
n=len(d)
print(n, round(sum(d),1), statistics.median(d), d[math.ceil(0.9*n)-1], d[-1])
AKHIR

# kanal terisi sedikitnya 50 persen per sumur
python3 - <<'AKHIR'
import json, glob
for f in sorted(glob.glob('data/volve/witsml_parsed/*.qc.json')):
    q=json.load(open(f,encoding='utf-8'))
    print(f.split('/')[-1].replace('.qc.json',''), q['n_channels_ge_50pct'])
AKHIR

# 37 lipatan, dibaca dari manifest
python3 - <<'AKHIR'
import json
d=json.load(open('docs/evidence/folds_per_dataset.json',encoding='utf-8'))
for k,v in d['per_dataset'].items(): print(k, v['n_well'])
print('total', d['total_lipatan'])
AKHIR

# 27 head dan 13 head wajib tinjauan
python3 - <<'AKHIR'
import json
d=json.load(open('dashboard/data/engine_v9_i1.json',encoding='utf-8'))
print(len(d['heads']), sum(1 for h in d['heads'] if h['human_review']))
AKHIR

# 480 fitur
python3 - <<'AKHIR'
import zipfile, ast
b=zipfile.ZipFile('data/predictive/features_timeseries_controls_berdata.npz').read('X.npy')
off = 10 if b[6]==1 else 12
hlen = int.from_bytes(b[8:off],'little')
h=ast.literal_eval(b[off:off+hlen].decode('latin1'))
print(h['shape'], '-> fitur', h['shape'][1])
AKHIR
```

## 3. Perintah lain yang dipakai pada pengujian sebelumnya

```bash
python3 scratch/ppt1/verify_durations.py            # A-07, A-08
python3 scratch/ppt1/riset_klasifikasi_simv5.py     # A-01 sampai A-06
python3 scratch/ppt1/verifikasi_bab1_2.py           # A-16
python3 scratch/ppt1/check_mcdm.py                  # A-14
python3 scratch/ppt1/inspect_v9_engines.py          # A-13
```

## 4. Aturan pemakaian

Nama berkas dan perintah tidak dipindahkan kembali ke proposal. Bila angka berubah, yang diperbarui lebih dulu adalah berkas bukti pada tabel bagian 1, lalu proposal, lalu catatan ini.
