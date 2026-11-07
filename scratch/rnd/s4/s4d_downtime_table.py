"""S4-D: ekstraksi tabel equipmentfailureInfoTable dari 1.759 DDR HTML. READ-ONLY.

Tabel ini berisi kolom: Start time | Depth mMD | Depth mTVD | Sub Equip - Syst Class |
Operation Downtime (min) | Equipment Repaired | Remark

Keluaran:
  scratch/rnd/s4/ddr_downtime_table.json      (agregat + contoh)
  scratch/rnd/s4/ddr_downtime_records.jsonl   (semua record mentah, satu baris per record)
"""
import os, re, json, glob
from collections import Counter, defaultdict
from bs4 import BeautifulSoup

ROOT = "/mnt/d/Capstone 1(v2)"
HTML_DIR = os.path.join(ROOT, "data/volve/external/dbx_volume/Well_technical_data/Daily Drilling Report - HTML Version")
OUT_AGG = os.path.join(ROOT, "scratch/rnd/s4/ddr_downtime_table.json")
OUT_REC = os.path.join(ROOT, "scratch/rnd/s4/ddr_downtime_records.jsonl")

files = sorted(glob.glob(os.path.join(HTML_DIR, "*.html")))
print("n_file:", len(files))

n_files_with_table = 0
n_files_no_table = 0
n_files_error = 0
records = []
per_file = {}

for fp in files:
    try:
        with open(fp, "r", encoding="utf-8", errors="replace") as f:
            txt = f.read()
    except OSError:
        n_files_error += 1
        continue
    if "equipmentfailureInfoTable" not in txt:
        n_files_no_table += 1
        continue
    soup = BeautifulSoup(txt, "lxml")
    tbl = soup.find("table", id="equipmentfailureInfoTable")
    if tbl is None:
        n_files_no_table += 1
        continue
    n_files_with_table += 1
    base = os.path.basename(fp)
    # wellbore & periode dari header laporan
    wb = ""
    m = re.search(r"Wellbore:\s*</b>\s*([^<]+)", txt)
    if m:
        wb = m.group(1).strip()
    period = ""
    m2 = re.search(r"Period:\s*</b>\s*([^<]+)", txt)
    if m2:
        period = m2.group(1).strip()
    heads = [th.get_text(" ", strip=True) for th in tbl.find_all("th")]
    rows = []
    for tr in tbl.find_all("tr"):
        tds = tr.find_all("td")
        if not tds:
            continue
        cells = [td.get_text(" ", strip=True) for td in tds]
        # pastikan 7 kolom; sel kosong self-closing tetap terhitung oleh bs4
        rows.append(cells)
    per_file[base] = {"wellbore": wb, "period": period, "n_baris": len(rows)}
    for cells in rows:
        rec = {
            "file": base,
            "wellbore": wb,
            "period": period,
            "n_kolom": len(cells),
            "start_time": cells[0] if len(cells) > 0 else "",
            "depth_mmd": cells[1] if len(cells) > 1 else "",
            "depth_mtvd": cells[2] if len(cells) > 2 else "",
            "sub_equip_syst_class": cells[3] if len(cells) > 3 else "",
            "downtime_min": cells[4] if len(cells) > 4 else "",
            "equipment_repaired": cells[5] if len(cells) > 5 else "",
            "remark": cells[6] if len(cells) > 6 else "",
        }
        records.append(rec)

print("file dengan tabel:", n_files_with_table, "| tanpa tabel:", n_files_no_table, "| error:", n_files_error)
print("n record:", len(records))

# ---------- agregat ----------
def to_num(s):
    s = (s or "").strip().replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None

dt_vals = []
n_dt_missing = 0
n_dt_zero = 0
n_dt_pos = 0
n_col_mismatch = Counter()
cls = Counter()
eq_rep = Counter()
per_well = defaultdict(lambda: {"n": 0, "jam": 0.0})
per_file_sum = defaultdict(float)

for r in records:
    n_col_mismatch[r["n_kolom"]] += 1
    v = to_num(r["downtime_min"])
    if v is None:
        n_dt_missing += 1
    else:
        dt_vals.append(v)
        if v == 0:
            n_dt_zero += 1
        else:
            n_dt_pos += 1
        per_well[r["wellbore"]]["n"] += 1
        per_well[r["wellbore"]]["jam"] += v / 60.0
        per_file_sum[r["file"]] += v / 60.0
    c = r["sub_equip_syst_class"].strip()
    if c:
        cls[c] += 1
    e = r["equipment_repaired"].strip()
    if e and e not in ("00:00",):
        eq_rep[e] += 1

import statistics
agg = {
    "sumber": {"dir": HTML_DIR, "n_file_html": len(files), "n_file_dibaca": n_files_with_table + n_files_no_table,
               "n_file_error": n_files_error},
    "tabel": {"id": "equipmentfailureInfoTable",
              "kolom": ["Start time", "Depth mMD", "Depth mTVD", "Sub Equip - Syst Class",
                        "Operation Downtime (min)", "Equipment Repaired", "Remark"],
              "n_file_memuat_tabel": n_files_with_table,
              "n_file_tanpa_tabel": n_files_no_table,
              "persen_file_memuat_tabel": round(100.0 * n_files_with_table / max(1, len(files)), 2)},
    "record": {
        "n_record": len(records),
        "n_kolom_distribusi": dict(n_col_mismatch),
        "n_downtime_numerik": len(dt_vals),
        "n_downtime_kosong_atau_teks": n_dt_missing,
        "n_downtime_nol": n_dt_zero,
        "n_downtime_positif": n_dt_pos,
        "total_menit": round(sum(dt_vals), 1),
        "total_jam": round(sum(dt_vals) / 60.0, 3),
        "median_menit": round(statistics.median(dt_vals), 2) if dt_vals else None,
        "max_menit": round(max(dt_vals), 1) if dt_vals else None,
        "mean_menit_positif": round(sum(v for v in dt_vals if v > 0) / max(1, n_dt_pos), 2) if n_dt_pos else None,
    },
    "kelas_equipment_teratas": dict(cls.most_common(30)),
    "n_kelas_equipment_unik": len(cls),
    "equipment_repaired_teratas": dict(eq_rep.most_common(15)),
    "per_wellbore": {k: {"n": v["n"], "jam": round(v["jam"], 3)} for k, v in sorted(per_well.items(), key=lambda kv: -kv[1]["jam"])},
    "per_file_jam": {k: round(v, 3) for k, v in sorted(per_file_sum.items(), key=lambda kv: -kv[1])[:20]},
    "contoh_5_record": records[:5],
}

with open(OUT_AGG, "w", encoding="utf-8") as f:
    json.dump(agg, f, ensure_ascii=False, indent=1)
with open(OUT_REC, "w", encoding="utf-8") as f:
    for r in records:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

print("WROTE", OUT_AGG, os.path.getsize(OUT_AGG), "|", OUT_REC, os.path.getsize(OUT_REC))
print("total jam downtime:", agg["record"]["total_jam"], "| record:", len(records), "| nol:", n_dt_zero, "| positif:", n_dt_pos)
print("n kelas unik:", len(cls))
print("kelas teratas:", dict(cls.most_common(8)))
print("per wellbore:", agg["per_wellbore"])
