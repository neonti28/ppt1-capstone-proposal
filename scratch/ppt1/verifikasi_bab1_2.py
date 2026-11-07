#!/usr/bin/env python3
"""Hitung ulang angka BAB I 1.2 Proposal PPT I (Volve/ARCT-9F2) dari data primer.

Langkah per angka tertulis di sini, bukan di dokumen. Setiap angka dicetak
dengan nilai yang dihitung ulang supaya dapat diperiksa siapa pun.

Pemakaian: python3 scratch/ppt1/verifikasi_bab1_2.py
"""
import csv, json, statistics, pathlib, collections

R = pathlib.Path(__file__).resolve().parents[2]

# ---------- 1. Tabel label kejadian terkurasi ----------
with (R / 'data/volve/labels_curated_v2.csv').open(encoding='utf-8') as f:
    rows = list(csv.DictReader(f))


n = len(rows)
duras = []
for r in rows:
    if r['act_start'] and r['act_end']:
        from datetime import datetime
        a = datetime.fromisoformat(r['act_start'].replace('Z', '+00:00'))
        b = datetime.fromisoformat(r['act_end'].replace('Z', '+00:00'))
        duras.append((b - a).total_seconds() / 60)

kategori = collections.Counter(r['category'] for r in rows)
bha = collections.Counter(r['bha_relevant'] for r in rows)
sumur = {r['wellbore'] for r in rows}

hasil = [
    ('Jumlah baris tabel label', n, 884),
    ('Total durasi (menit)', round(sum(duras)), 73500),
    ('Median durasi (menit)', statistics.median(duras), 45),
    ('Persentil 90 durasi (menit)', statistics.quantiles(duras, n=100)[89], 180),
    ('Durasi maksimum (menit)', max(duras), 780),
    ('Jumlah sumur', len(sumur), 10),
    ('Kejadian tanpa bukti kegagalan', kategori.get('routine_no_failure_evidence', 0), 496),
    ('Kejadian relevan BHA ya', bha.get('yes', 0), 50),
    ('Kejadian relevansi belum pasti', bha.get('uncertain', 0), 571),
]

# ---------- 2. Ringkasan hasil eksekusi model (lapis keputusan, head, slot) ----------
i1 = json.loads((R / 'scratch/v9_i1/v9_i1_RESULTS.json').read_text())
engines = i1['engines']
heads = [h for e in engines for h in e['heads']]
ring = i1['decision_layer']['ringkasan']
hasil += [
    ('Jumlah detektor (engine)', len(engines), 7),
    ('Jumlah head', len(heads), 27),
    ('Sebaran head per detektor', tuple(len(e['heads']) for e in engines), (4, 4, 4, 6, 4, 2, 3)),
    ('L0', ring['L0'], 5),
    ('L1', ring['L1'], 11),
    ('L2', ring['L2'], 9),
    ('L3', ring['L3'], 2),
    ('Tier TREN', sum(1 for h in heads if h['tier'] == 'TREN'), 13),
    ('Tier PERINGATAN-BERPENGAWAS', sum(1 for h in heads if h['tier'] == 'PERINGATAN-BERPENGAWAS'), 12),
    ('Tier BELUM LAYAK PAKAI', sum(1 for h in heads if h['tier'] == 'BELUM LAYAK PAKAI'), 2),
    ('Slot alarm otomatis kritis', i1['decision_layer']['auto_critical_alarm_slots'], 0),
    ('Peringatan L1 (manusia)', i1['decision_layer']['nperingatan_l1'], 11),
]

# ---------- 3. Nodata CRPM agregat dan per sumur ----------
evc = json.loads((R / 'scratch/v9_eval_c/v9_eval_c_RESULTS.json').read_text())
nodata = evc['C_rule_status']['ssi']['sensor_nodata_rule']
hasil += [
    ('Jendela tanpa data CRPM', nodata['n_nodata'], 22385),
    ('Jendela uji ssi total', nodata['n_total'], 35906),
    ('Frasa nodata agregat (persen)', round(100 * nodata['frac'], 2), 62.34),
]

d1 = json.loads((R / 'scratch/v9_d1/v9_d1_01_summary.json').read_text())['wells']
f14 = d1['F-14']
hasil += [
    ('F-14 bin dengan observasi CRPM', f14['bins_with_crpm_obs'], 11794),
    ('F-14 seluruh bin', f14['n_bins'], 96698),
    ('F-14 bin pengeboran', f14['n_bins_drill'], 12635),
    ('F-14 nodata atas seluruh bin (persen)', round(100 * (1 - f14['bins_with_crpm_obs'] / f14['n_bins']), 2), 87.80),
    ('F-14 bin pengeboran tanpa CRPM', f14['n_bins_drill'] - f14['bins_with_crpm_obs'], 841),
    ('F-14 nodata atas bin pengeboran (persen)', round(100 * (f14['n_bins_drill'] - f14['bins_with_crpm_obs']) / f14['n_bins_drill'], 2), 6.66),
    ('F-10 bin pengeboran', d1['F-10']['n_bins_drill'], 13781),
    ('F-10 seluruh bin', d1['F-10']['n_bins'], 41446),
    ('F-12 bin pengeboran', d1['F-12']['n_bins_drill'], 23931),
    ('F-12 seluruh bin', d1['F-12']['n_bins'], 180958),
    ('F-10 bin dengan observasi getaran', d1['F-10']['bins_with_vib_obs'], 0),
]

# ---------- 4. Laju alarm palsu dan recall per sumur pada ambang 0,5 ----------
vib = json.loads((R / 'scratch/v9_e_ml/v9_e_ML_vib_RESULTS.json').read_text())
far, rec = {}, {}
for fold in vib['folds']:
    tm = fold['models']['rf']['tau_metrics']['0.5']
    for k, v in tm.items():
        if k.startswith('FAR_24jam'):
            far[fold['test_well']] = v
        if k.startswith('recall'):
            rec[fold['test_well']] = v
hasil += [
    ('FAR 24 jam terbesar', round(max(far.values()), 5), 496.09249),
    ('FAR 24 jam terkecil', round(min(far.values()), 5), 4.14897),
    ('Rasio FAR terbesar/terkecil', round(max(far.values()) / min(far.values()), 2), 119.57),
    ('Recall F-14', round(rec['F-14'], 4), 0.8657),
    ('Recall F-15_S', round(rec['F-15_S'], 4), 0.1018),
]

# ---------- 5. Prevalensi kelas ssi per sumur ----------
eva = json.loads((R / 'scratch/v9_eval_a/v9_eval_a_RESULTS.json').read_text())
prev = {}
for f in eva['rule_status']['classes']['ssi']['folds']:
    prev[f['test_well']] = (f['pos'], f['n'], round(100 * f['pos'] / f['n'], 2))
hasil += [
    ('ssi F-15A', prev['F-15A'][:2], (31, 6020)),
    ('ssi F-7', prev['F-7'][:2], (3, 982)),
    ('ssi F-9_A', prev['F-9_A'][:2], (55, 841)),
]

print('=' * 78)
lulus = 0
for nama, dihitung, diharapkan in hasil:
    ok = dihitung == diharapkan
    lulus += ok
    print(f"{'LULUS' if ok else 'BEDA '} | {nama:<42} | {dihitung} (diharapkan {diharapkan})")
print('=' * 78)
print(f'{lulus}/{len(hasil)} angka cocok')
print()
print('Kunci JSON yang dipakai: C_rule_status.ssi.sensor_nodata_rule; wells.F-14.*;')
print('engines[].heads[].tier; decision_layer.ringkasan; models.rf.tau_metrics["0.5"]')
