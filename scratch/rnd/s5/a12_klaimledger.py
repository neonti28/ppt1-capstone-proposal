import json, pathlib, re
B = pathlib.Path("/mnt/d/Capstone 1(v2)")
LED = (B / "docs/RND_PROVENANCE_LEDGER.md").read_text(encoding="utf-8").splitlines()

DOC = {"S1": "docs/RND_S1_SEED_ROBUSTNESS.md", "S2": "docs/RND_S2_HYBRID_VIB_SSI.md",
       "S3": "docs/RND_S3_HYBRID_BITWEAR.md", "S4": "docs/RND_S4_LAYER_B_DATA.md"}
for k, rel in DOC.items():
    t = (B / rel).read_text(encoding="utf-8")
    for l in t.splitlines():
        if re.search(r"setiap angka|seluruh angka|semua angka", l, re.I):
            print(f"{k}: {l.strip()[:220]}")

print("\n--- sel angka ambigu titik-ribuan per kartu ---")
for k in DOC:
    rows = [l for l in LED if l.startswith("| %s-" % k)]
    amb = 0
    for l in rows:
        sel = [c.strip() for c in l.strip().strip("|").split("|")]
        if len(sel) == 7 and re.match(r"^\d{1,3}(?:\.\d{3})+$", sel[1]):
            amb += 1
    print(f"  {k}: {amb} dari {len(rows)} baris")

print("\n--- kode S4-N (BELUM) dan jumlah baris BELUM per kartu ---")
for k in DOC:
    rows = [l for l in LED if l.startswith("| %s-" % k)]
    belum = sum(1 for l in rows if "BELUM" in l.split("|")[-2] or "BELUM" in l)
    print(f"  {k}: baris menyebut BELUM = {belum}")
