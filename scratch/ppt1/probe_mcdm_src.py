"""Probe sumber untuk BAB III 3.4: registry V9, affinity, alternatif."""
import json

AKAR = "/mnt/d/Capstone 1(v2)/"

with open(AKAR + "scratch/v9_i1/v9_i1_RESULTS.json", encoding="utf-8") as f:
    r = json.load(f)
print("=== v9_i1_RESULTS.json kunci atas ===")
print(list(r.keys()))
for k in r:
    v = r[k]
    if isinstance(v, (int, float, str)):
        print(f"  {k} = {v}")
    elif isinstance(v, list):
        print(f"  {k} = list len {len(v)}; contoh {v[:1]}")
    elif isinstance(v, dict):
        print(f"  {k} = dict keys {list(v.keys())[:12]}")

print()
print("=== affinity.json kunci atas ===")
with open(AKAR + "scratch/ppt1/affinity.json", encoding="utf-8") as f:
    a = json.load(f)
print(list(a.keys()))
if "kriteria" in a:
    print("kriteria:", [(k.get("id"), k.get("nama", "")[:40]) for k in a["kriteria"]])
print("matriks_us_kriteria:", json.dumps(a.get("matriks_us_kriteria"))[:1500])
print("batasan:", [(b.get("id"), b.get("kategori")) for b in a.get("batasan", [])])

print()
print("=== alternatif.json bukti per alternatif ===")
with open(AKAR + "scratch/ppt1/alternatif.json", encoding="utf-8") as f:
    alt = json.load(f)
print("kunci atas:", list(alt.keys()))
items = alt.get("alternatif", alt)
if isinstance(items, list):
    for it in items:
        b = it.get("bukti", [])
        print(it.get("id"), it.get("nama", "")[:45], "| bukti:", len(b))
