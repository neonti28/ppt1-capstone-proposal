"""S4-I: pindai token biaya dan work order pada SELURUH 1.759 XML dan 1.759 HTML DDR.

Koreksi: inventory_raw.json hanya memindai 5 token (maintain, inspection, inspect,
downtime, npt). Klaim "cost 0 kemunculan" di dokumen sebelumnya mengambil nilai
default .get("cost", 0), bukan hasil pengukuran. Skrip ini mengukur sungguhan.
"""
import os, re, json

ROOT = "/mnt/d/Capstone 1(v2)"
BASE = os.path.join(ROOT, "data/volve/external/dbx_volume/Well_technical_data")
OUT = os.path.join(ROOT, "scratch/rnd/s4/token_scan.json")

LITERAL = ["cost", "work order", "workorder", "work-order", "daycost", "day cost",
           "invoice", "budget", "price", "tariff", "usd", "nok", "inspection",
           "inspect", "maintenance", "service order", "purchase order"]
REGEX = {
    "kata_berakar_cost": re.compile(r"\bcost\w*", re.I),
    "kata_berakar_invoice": re.compile(r"\binvoic\w*", re.I),
    "kata_berakar_budget": re.compile(r"\bbudget\w*", re.I),
    "kata_berakar_price": re.compile(r"\bpric\w*", re.I),
    "nomor_wo": re.compile(r"\bWO[-\s]?\d{2,}", re.I),
}

def scan_dir(d, exts):
    n_file = 0
    gagal = 0
    lit = {t: 0 for t in LITERAL}
    lit_files = {t: 0 for t in LITERAL}
    reg = {k: 0 for k in REGEX}
    reg_files = {k: 0 for k in REGEX}
    contoh = {}
    for name in sorted(os.listdir(d)):
        if not name.lower().endswith(exts):
            continue
        p = os.path.join(d, name)
        if not os.path.isfile(p):
            continue
        try:
            with open(p, "r", encoding="utf-8", errors="replace") as f:
                txt = f.read().lower()
        except Exception:
            gagal += 1
            continue
        n_file += 1
        for t in LITERAL:
            c = txt.count(t)
            if c:
                lit[t] += c
                lit_files[t] += 1
                if t not in contoh:
                    contoh[t] = name
        for k, rx in REGEX.items():
            m = rx.findall(txt)
            if m:
                reg[k] += len(m)
                reg_files[k] += 1
                if k not in contoh:
                    contoh[k] = (name, sorted(set(x.lower() for x in m))[:5])
    return {
        "n_file_dibaca": n_file,
        "n_file_gagal": gagal,
        "kemunculan_literal": lit,
        "file_mengandung_literal": lit_files,
        "kemunculan_regex": reg,
        "file_mengandung_regex": reg_files,
        "contoh_berkas": contoh,
    }

res = {
    "sumber": {
        "xml": os.path.join(BASE, "Daily Drilling Report - XML Version"),
        "html": os.path.join(BASE, "Daily Drilling Report - HTML Version"),
    },
    "catatan": "pemindaian penuh, bukan sampel; teks di-lowercase, hitungan substring literal dan regex kata berakar",
    "xml": scan_dir(os.path.join(BASE, "Daily Drilling Report - XML Version"), (".xml",)),
    "html": scan_dir(os.path.join(BASE, "Daily Drilling Report - HTML Version"), (".html", ".htm")),
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, indent=2, ensure_ascii=False)

for fmt in ("xml", "html"):
    r = res[fmt]
    print(f"== {fmt.upper()} == berkas dibaca {r['n_file_dibaca']}, gagal {r['n_file_gagal']}")
    print("  literal:", {k: v for k, v in r["kemunculan_literal"].items() if v})
    print("  regex  :", {k: v for k, v in r["kemunculan_regex"].items() if v})
    print("  contoh :", r["contoh_berkas"])
print("ditulis:", OUT)
