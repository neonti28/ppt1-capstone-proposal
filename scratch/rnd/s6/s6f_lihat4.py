"""Cetak meta pilihan.json (harness, seed, kebijakan) dan tabel cacat S5 bagian 7."""
import json
import re

B = "/mnt/d/Capstone 1(v2)"
P = json.load(open(f"{B}/scratch/rnd/s6/pilihan.json"))
print("=== META S6 ===")
print(json.dumps(P["meta"], indent=1, ensure_ascii=False))

print("\n=== CACAT S5 (baris tabel dokumen S5) ===")
txt = open(f"{B}/docs/RND_S5_AUDIT_WAVE2.md", encoding="utf-8").read().splitlines()
mulai = None
for i, l in enumerate(txt):
    if re.match(r"^#+\s*7\.", l):
        mulai = i
        break
assert mulai is not None, "bagian 7 tidak ditemukan"
for i in range(mulai, min(mulai + 30, len(txt))):
    print(f"{i+1}: {txt[i]}")
