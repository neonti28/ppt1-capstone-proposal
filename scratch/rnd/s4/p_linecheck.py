"""Verifikasi klaim baris: apakah baris yang dikutip benar memuat klaim 'jam henti tidak ada'."""
import os, re
ROOT = "/mnt/d/Capstone 1(v2)"
targets = {
    "docs/RND_E3_HASIL.md": [217, 300],
    "docs/RND_E4_PERBAIKAN.md": [256, 343],
    "docs/RND_R7_REVIEW.md": [359],
    "docs/RND_R8_EVALUASI_BERLAPIS.md": [148, 234],
    "docs/RND_S1_SEED_ROBUSTNESS.md": [170, 255],
    "docs/RND_PM_VERDICT.md": [182, 263, 292],
}
for rel, lines in targets.items():
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p):
        print(rel, "TIDAK ADA")
        continue
    txt = open(p, encoding="utf-8").read().splitlines()
    print("=" * 70)
    print(rel, "total baris:", len(txt))
    for n in lines:
        if n > len(txt):
            print(f"  {n}: DI LUAR BERKAS")
            continue
        s = txt[n - 1].strip()
        print(f"  {n}: {s[:220]}")
