"""S4-C: sapuan bukti lapisan B pada seluruh kandidat file. READ-ONLY.

Langkah:
 1. Inventaris folder dokumen Well_technical_data (jumlah file, byte).
 2. Hitung dokumen DDR per format (HTML/XML/PDF).
 3. Pindai SEMUA XML DDR untuk token biaya / work order / inspeksi (bukti ada atau tidak).
 4. Pindai SEMUA HTML DDR untuk token yang sama.
 5. Hitung kategori katalog Volve (apa yang ada di sumber, apa yang lokal).
 6. Pindai header semua CSV di data/ untuk kolom bernuansa biaya/inspeksi/NPT.
Keluaran: scratch/rnd/s4/inventory_raw.json
"""
import os, json, csv, glob
from collections import Counter

ROOT = "/mnt/d/Capstone 1(v2)"
OUT = os.path.join(ROOT, "scratch/rnd/s4/inventory_raw.json")
WTD = os.path.join(ROOT, "data/volve/external/dbx_volume/Well_technical_data")

res = {}

# ---------- 1. inventaris folder ----------
folders = {}
for name in sorted(os.listdir(WTD)):
    p = os.path.join(WTD, name)
    if not os.path.isdir(p):
        continue
    n_files = 0
    n_bytes = 0
    for dirpath, _, files in os.walk(p):
        for f in files:
            fp = os.path.join(dirpath, f)
            try:
                n_files += 1
                n_bytes += os.path.getsize(fp)
            except OSError:
                pass
    folders[name] = {"n_files": n_files, "bytes": n_bytes}
res["folder_well_technical_data"] = folders
res["folder_total"] = {"n_files": sum(v["n_files"] for v in folders.values()),
                       "bytes": sum(v["bytes"] for v in folders.values())}

# ---------- 2. dokumen DDR per format ----------
fmt = {}
for name, sub in [("html", "Daily Drilling Report - HTML Version"),
                  ("xml", "Daily Drilling Report - XML Version"),
                  ("pdf", "Daily Drilling report - PDF Version")]:
    p = os.path.join(WTD, sub)
    files = sorted(glob.glob(os.path.join(p, "*")))
    fmt[name] = {"n_files": len(files), "bytes": sum(os.path.getsize(f) for f in files)}
res["ddr_dokumen_per_format"] = fmt

# ---------- 3. pindai XML DDR ----------
TOKENS = ["cost", "work order", "workorder", "inspection", "inspect", "maintain", "downtime", "npt"]
def scan(files, label):
    occ = Counter()
    files_hit = Counter()
    n_read = 0
    n_err = 0
    for fp in files:
        try:
            with open(fp, "r", encoding="latin-1", errors="replace") as f:
                txt = f.read().lower()
        except OSError:
            n_err += 1
            continue
        n_read += 1
        for t in TOKENS:
            c = txt.count(t)
            if c:
                occ[t] += c
                files_hit[t] += 1
    return {"label": label, "n_file_dibaca": n_read, "n_file_gagal": n_err,
            "kemunculan": dict(occ), "file_mengandung": dict(files_hit)}

xml_files = sorted(glob.glob(os.path.join(WTD, "Daily Drilling Report - XML Version", "*.xml")))
res["pindai_xml_ddr"] = scan(xml_files, "XML DDR")

html_files = sorted(glob.glob(os.path.join(WTD, "Daily Drilling Report - HTML Version", "*.html")))
res["pindai_html_ddr"] = scan(html_files, "HTML DDR")

# ---------- 5. katalog Volve ----------
cat_path = os.path.join(ROOT, "data/volve/external/volve_catalog_target_paths.csv")
cats = Counter()
exts = Counter()
n_rows = 0
with open(cat_path, "r", encoding="utf-8", errors="replace", newline="") as f:
    rdr = csv.DictReader(f)
    for row in rdr:
        n_rows += 1
        cats[row.get("category", "")] += 1
        exts[row.get("ext", "")] += 1
res["katalog_volve"] = {
    "path": cat_path,
    "bytes": os.path.getsize(cat_path),
    "n_baris": n_rows,
    "kolom": ["category", "well", "ext", "path"],
    "kategori": dict(cats.most_common()),
    "ekstensi": dict(exts.most_common(15)),
}

# ---------- 6. pindai header CSV di data/ ----------
csv_files = []
for dirpath, _, files in os.walk(os.path.join(ROOT, "data")):
    for f in files:
        if f.lower().endswith((".csv", ".tsv")):
            fp = os.path.join(dirpath, f)
            try:
                if os.path.getsize(fp) < 500 * 1024 * 1024:
                    csv_files.append(fp)
            except OSError:
                pass
csv_files.sort()
scan_csv = []
for fp in csv_files:
    try:
        with open(fp, "r", encoding="utf-8", errors="replace", newline="") as f:
            header = f.readline().strip()
    except OSError:
        continue
    low = header.lower()
    hit = [k for k in ["cost", "biaya", "inspection", "inspeksi", "work_order", "workorder",
                       "downtime", "npt", "durasi", "duration", "repair", "maintenance"]
           if k in low]
    scan_csv.append({"path": os.path.relpath(fp, ROOT), "bytes": os.path.getsize(fp),
                     "n_kolom": len(header.split(",")), "header": header[:400],
                     "kata_kunci_header": hit})
res["csv_di_data"] = {"n_file": len(scan_csv), "berkas": scan_csv}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
print("WROTE", OUT, os.path.getsize(OUT))
print("folder total:", res["folder_total"])
print("ddr format:", fmt)
print("xml scan:", res["pindai_xml_ddr"]["n_file_dibaca"], "file;", res["pindai_xml_ddr"]["kemunculan"])
print("html scan:", res["pindai_html_ddr"]["n_file_dibaca"], "file;", res["pindai_html_ddr"]["kemunculan"])
print("katalog kategori:", res["katalog_volve"]["kategori"])
print("csv dipindai:", len(scan_csv), "| yang punya kata kunci header:",
      [(r["path"], r["kata_kunci_header"]) for r in scan_csv if r["kata_kunci_header"]])
