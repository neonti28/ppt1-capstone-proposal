import json, re, sys

BASE = "/mnt/d/Capstone 1(v2)"
p_md = BASE + "/docs/PPT1_LEDGER_ANGKA.md"
p_js = BASE + "/scratch/ppt1/ledger.json"

d = json.load(open(p_js, encoding="utf-8"))
rows = d["baris"]
ALLOWED = {"TERUKUR", "ASUMSI", "WARISAN-DRAFT"}
bad_status = [r["id"] for r in rows if r.get("status") not in ALLOWED]
bad_verif = [r["id"] for r in rows if not (r.get("verifikasi") or "").strip()]
bad_src = [r["id"] for r in rows if not (r.get("sumber") or "").strip()]
ids = [r["id"] for r in rows]
dup = [i for i in set(ids) if ids.count(i) > 1]

md = open(p_md, encoding="utf-8").read()
lines = md.splitlines()
# hitung baris tabel data (mulai | A01 / B01 ...)
data_rows = [l for l in lines if re.match(r"^\| [ABCD]\d\d \|", l)]
# cek tiap baris tabel punya 8 kolom (pipe tak ter-escape)
bad_cols = []
for l in data_rows:
    # hitung pipe yang tidak didahului backslash
    n = len(re.findall(r"(?<!\\)\|", l))
    if n != 9:
        bad_cols.append((l[:40], n))

em = md.count("\u2014")
print("rows_json:", len(rows))
print("rows_md_tabel:", len(data_rows))
print("status_ilegal:", bad_status)
print("verifikasi_kosong:", bad_verif)
print("sumber_kosong:", bad_src)
print("id_duplikat:", dup)
print("baris_tabel_kolom_salah:", bad_cols[:5], "n_bad:", len(bad_cols))
print("em_dash_count:", em)
print("section_h3:", [l for l in lines if l.startswith("### ")])
print("h2:", [l for l in lines if l.startswith("## ")])
# cek angka kunci muncul di md
for k in ["884", "27 head", "4,35", "0,5213", "1.225", ">15%", "0,8306"]:
    print("ada", repr(k), ":", k in md)
print("SIZE_MD", len(md))
