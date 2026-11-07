"""Cek berkas mana saja yang ikut dipindai header (termasuk witsml_parsed)."""
import json, os
ROOT = "/mnt/d/Capstone 1(v2)"
d = json.load(open(os.path.join(ROOT, "scratch/rnd/s4/inventory_raw.json"), encoding="utf-8"))
files = d["csv_di_data"]["berkas"]
print("total:", len(files))
wp = [f for f in files if "witsml_parsed" in f["path"]]
print("dari witsml_parsed:", len(wp))
for f in wp:
    print("  ", f["path"], f["bytes"], "kata_kunci:", f["kata_kunci_header"])
print("--- semua yang punya kata kunci header ---")
for f in files:
    if f["kata_kunci_header"]:
        print("  ", f["path"], f["kata_kunci_header"])
print("--- path unik per folder ---")
import collections
c = collections.Counter(p["path"].rsplit("/", 1)[0] for p in files)
for k, v in c.most_common():
    print("  ", k, v)
