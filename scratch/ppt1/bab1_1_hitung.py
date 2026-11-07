"""Hitung ulang SEMUA angka kuantitatif pada subbab 1.1 langsung dari data di disk.

Instrumen sengaja dibuat BERBEDA dari scratch/ppt1/verify_durations.py:
stempel waktu diparse dengan regex sendiri lalu dikonversi ke epoch detik
(bukan datetime.fromisoformat), sehingga kalau dua skrip sepakat, hasilnya
tidak menumpang pada satu parser saja.

Jalankan: python3 scratch/ppt1/bab1_1_hitung.py
Keluaran: scratch/ppt1/bab1_1_angka.json + ringkasan ke stdout.
"""
import csv
import gzip
import pathlib
import json
import os
import re
import statistics
from collections import Counter, defaultdict

BASE = str(pathlib.Path(__file__).resolve().parents[2])
OUT = BASE + "/scratch/ppt1/bab1_1_angka.json"

TS_RE = re.compile(
    r"^(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2})(?::(\d{2}))?"
    r"(Z|[+-]\d{2}:?\d{2})?$"
)


def epoch(ts):
    """Parse ISO-8601 dengan offset menjadi detik epoch (UTC). None bila gagal."""
    ts = (ts or "").strip()
    if not ts:
        return None
    m = TS_RE.match(ts)
    if not m:
        return None
    y, mo, d, hh, mm, ss, off = m.groups()
    days = 0
    # hari sejak epoch: algoritma sipil -> hari (Howard Hinnant), tanpa pustaka datetime
    yy = int(y) - (1 if int(mo) <= 2 else 0)
    era = (yy if yy >= 0 else yy - 399) // 400
    yoe = yy - era * 400
    mp = (int(mo) + 9) % 12
    doy = (153 * mp + 2) // 5 + int(d) - 1
    doe = yoe * 365 + yoe // 4 - yoe // 100 + doy
    days = era * 146097 + doe - 719468
    secs = days * 86400 + int(hh) * 3600 + int(mm) * 60 + int(ss or 0)
    if off and off != "Z":
        sign = 1 if off[0] == "+" else -1
        body = off[1:].replace(":", "")
        secs -= sign * (int(body[:2]) * 3600 + int(body[2:]) * 60)
    return secs


def pct_index(sorted_vals, q):
    """Kuantil cara-1: ambil elemen ke-int(n*q), tanpa interpolasi."""
    n = len(sorted_vals)
    if not n:
        return None
    return sorted_vals[min(int(n * q), n - 1)]


R = {"meta": {"skrip": "scratch/ppt1/bab1_1_hitung.py", "basis": BASE}}

# ---------------------------------------------------------------- 1. label kejadian
lab_path = BASE + "/data/volve/labels_curated_v2.csv"
rows = list(csv.DictReader(open(lab_path, newline="", encoding="utf-8")))
R["labels"] = {
    "berkas": "data/volve/labels_curated_v2.csv",
    "baris": len(rows),
    "kolom": len(rows[0].keys()) if rows else 0,
    "kolom_nama": list(rows[0].keys()) if rows else [],
}
cat = Counter(r["category"] for r in rows)
R["labels"]["kategori_n"] = len(cat)
R["labels"]["kategori"] = dict(cat.most_common())
R["labels"]["bha_relevant"] = dict(Counter((r["bha_relevant"] or "").strip() for r in rows))

durs_min, per_cat_min, per_well = [], defaultdict(float), Counter()
bad, neg, overflow = 0, 0, 0
for r in rows:
    a, b = epoch(r["act_start"]), epoch(r["act_end"])
    if a is None or b is None:
        bad += 1
        continue
    d = (b - a) / 60.0
    if d < 0:
        neg += 1
        continue
    if d > 720 * 60:  # > 720 jam dibuang sesuai instruksi kartu D1
        overflow += 1
        continue
    durs_min.append(d)
    per_cat_min[r["category"]] += d
    per_well[r["wellbore"]] += 1

sd = sorted(durs_min)
n = len(sd)
R["durasi"] = {
    "n_terpakai": n,
    "dibuang_timestamp_gagal": bad,
    "dibuang_negatif": neg,
    "dibuang_lebih_720_jam": overflow,
    "total_menit": round(sum(sd), 1),
    "total_jam": round(sum(sd) / 60.0, 1),
    "mean_menit": round(statistics.fmean(sd), 2) if sd else None,
    "median_menit": round(statistics.median(sd), 1) if sd else None,
    "p90_menit_cara1": round(pct_index(sd, 0.90), 1),
    "p90_menit_interpolasi": round(statistics.quantiles(sd, n=10)[8], 1) if n > 10 else None,
    "max_menit": round(sd[-1], 1),
    "min_menit": round(sd[0], 1),
}
R["durasi"]["jam_per_kategori"] = {
    k: {"n": cat[k], "jam": round(v / 60.0, 1)}
    for k, v in sorted(per_cat_min.items(), key=lambda x: -x[1])
}
R["durasi"]["wellbore_n"] = len(per_well)
R["durasi"]["kejadian_per_wellbore"] = dict(per_well.most_common())

# ------------------------------------------------- rentang tahun kejadian (klaim "2007 sampai 2015")
thn = [r["event_date"][:4] for r in rows if r.get("event_date")]
R["tahun"] = {
    "dari": min(thn) if thn else None,
    "sampai": max(thn) if thn else None,
    "per_tahun": dict(sorted(Counter(thn).items())),
    "kolom": "event_date",
}

# ------------------------------------------------- persentase turunan (dihitung, bukan dikira)
_n = R["labels"]["baris"]
_tot_jam = R["durasi"]["total_jam"]
R["persen"] = {
    "routine_no_failure_evidence": round(496 / _n * 100, 1),
    "bha_relevant_yes": round(50 / _n * 100, 1),
    "bha_relevant_uncertain": round(571 / _n * 100, 1),
    "wellbore_F14": round(182 / _n * 100, 1),
    "jam_bha_stuck_fishing": round(47.3 / _tot_jam * 100, 1),
    "jam_routine": round(601.1 / _tot_jam * 100, 1),
    "jam_surface_rig": round(343.5 / _tot_jam * 100, 1),
    "jam_kejadian_relevan_bha": round((47.3 + 14.0) / _tot_jam * 100, 1),
}

# ---------------------------------------------------------------- 2. WITSML terparse
wp = sorted(f for f in os.listdir(BASE + "/data/volve/witsml_parsed") if f.endswith(".csv"))
lines, data_rows = {}, {}
for f in wp:
    with open(BASE + "/data/volve/witsml_parsed/" + f, "rb") as fh:
        c = sum(1 for _ in fh)
    lines[f] = c
    data_rows[f] = c - 1
R["witsml_parsed"] = {
    "folder": "data/volve/witsml_parsed",
    "csv_n": len(wp),
    "baris_mentah_total": sum(lines.values()),
    "baris_data_total": sum(data_rows.values()),
    "per_berkas_baris_mentah": lines,
}

# ---------------------------------------------------------------- 3. dataset latih + fold
ds = sorted(f for f in os.listdir(BASE + "/scratch/v9_d1/datasets") if f.endswith(".csv.gz"))
rows_ds, fold_ds = {}, {}
for f in ds:
    with gzip.open(BASE + "/scratch/v9_d1/datasets/" + f, "rt") as fh:
        rows_ds[f] = sum(1 for _ in fh) - 1
leak = json.load(open(BASE + "/scratch/v9_d1/v9_d1_05_leak_lowo.json", encoding="utf-8"))
for k, v in leak.items():
    fold_ds[k] = v.get("n_folds")
R["dataset_latih"] = {
    "berkas_n": len(ds),
    "baris_per_berkas": rows_ds,
    "baris_total": sum(rows_ds.values()),
    "fold_per_dataset": fold_ds,
    "fold_total": sum(x for x in fold_ds.values() if x),
    "pelanggaran_bocor_total": sum(v.get("leak_violations_feat_ge_lab") or 0 for v in leak.values()),
    "dataset_status": {k: v.get("status") for k, v in leak.items()},
}

# ---------------------------------------------------------------- 4. registry head
reg = json.load(open(BASE + "/scratch/v9_i1/v9_i1_RESULTS.json", encoding="utf-8"))
heads = []
for e in reg["engines"]:
    for h in e.get("heads", []):
        heads.append((e["engine"], h.get("head"), h.get("tier"), h.get("layer")))
R["registry"] = {
    "berkas": "scratch/v9_i1/v9_i1_RESULTS.json",
    "engine_n": len(reg["engines"]),
    "head_n": len(heads),
    "head_per_engine": {e["engine"]: len(e.get("heads", [])) for e in reg["engines"]},
    "tier": dict(Counter(h[2] for h in heads)),
    "layer": dict(Counter(h[3] for h in heads)),
}

# ---------------------------------------------------------------- 5. inventaris di disk
akar = os.path.join(BASE, "data/volve")
n_berkas, total_byte, per_entri = 0, 0, {}
for entri in sorted(os.listdir(akar)):
    jalur = os.path.join(akar, entri)
    if os.path.isdir(jalur):
        n_f, n_b = 0, 0
        for d, _, fs in os.walk(jalur):
            for f in fs:
                try:
                    n_b += os.path.getsize(os.path.join(d, f))
                except OSError:
                    pass
                n_f += 1
    else:
        n_f, n_b = 1, os.path.getsize(jalur)
    per_entri[entri] = {"berkas": n_f, "byte": n_b}
    n_berkas += n_f
    total_byte += n_b
R["inventaris_disk"] = {
    "akar": "data/volve",
    "entri_puncak": len(per_entri),
    "berkas_total": n_berkas,
    "total_byte": total_byte,
    "total_gb": round(total_byte / 1e9, 2),
    "per_entri": per_entri,
}

json.dump(R, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

print(json.dumps({
    "n_kejadian": R["labels"]["baris"],
    "kategori_n": R["labels"]["kategori_n"],
    "durasi": {k: R["durasi"][k] for k in
               ("n_terpakai", "dibuang_timestamp_gagal", "dibuang_negatif",
                "dibuang_lebih_720_jam", "total_menit", "total_jam",
                "median_menit", "p90_menit_cara1", "p90_menit_interpolasi",
                "max_menit", "wellbore_n")},
    "jam_per_kategori": R["durasi"]["jam_per_kategori"],
    "witsml_csv": R["witsml_parsed"]["csv_n"],
    "witsml_baris_mentah": R["witsml_parsed"]["baris_mentah_total"],
    "dataset_n": R["dataset_latih"]["berkas_n"],
    "dataset_baris": R["dataset_latih"]["baris_total"],
    "fold_total": R["dataset_latih"]["fold_total"],
    "bocor": R["dataset_latih"]["pelanggaran_bocor_total"],
    "head_n": R["registry"]["head_n"],
    "tier": R["registry"]["tier"],
    "layer": R["registry"]["layer"],
    "inventaris_berkas": R["inventaris_disk"]["berkas_total"],
    "inventaris_gb": R["inventaris_disk"]["total_gb"],
}, indent=1, ensure_ascii=False))
print("\nJSON ->", OUT)
