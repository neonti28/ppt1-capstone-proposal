"""Cetak isi pilihan.json secara ringkas: kunci tingkat atas, lalu 15 baris tabel
dengan semua kolom metrik yang ada, dan kutipan kartu lain."""
import json

B = "/mnt/d/Capstone 1(v2)"
P = json.load(open(f"{B}/scratch/rnd/s6/pilihan.json"))
print("TOPBARIS:", list(P.keys()))
for k, v in P.items():
    if isinstance(v, list):
        print(f"{k}: list n={len(v)}")
    elif isinstance(v, dict):
        print(f"{k}: dict keys={list(v.keys())}")

print("\n=== SATU BARIS CONTOH ===")
t = P["tabel_perbandingan"][0]
print(json.dumps(t, indent=1, ensure_ascii=False)[:2500])
