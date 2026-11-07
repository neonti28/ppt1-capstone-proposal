import json, pathlib, re

B = pathlib.Path("/mnt/d/Capstone 1(v2)")
d = json.loads((B / "scratch/rnd/s1/s1_hyd_seeds.json").read_text(encoding="utf-8"))
print("kontrol keys:", list(d["kontrol_stokastik"].keys()))
print("sebaran:", json.dumps(d["kontrol_stokastik"]["sebaran"], ensure_ascii=False)[:400])

print("\n--- S4 baris yang tidak diresolusi otomatis (contoh) ---")
r3 = json.loads((B / "scratch/rnd/s5/s5_resolve3.json").read_text(encoding="utf-8"))
for t in r3["ledger"]["S4"]["tidak_resolve"][:10]:
    print("  ", t)

print("\n--- jumlah butir daftar belum terverifikasi per dokumen ---")
for nama, rel in [("S1", "docs/RND_S1_SEED_ROBUSTNESS.md"), ("S2", "docs/RND_S2_HYBRID_VIB_SSI.md"),
                  ("S3", "docs/RND_S3_HYBRID_BITWEAR.md"), ("S4", "docs/RND_S4_LAYER_B_DATA.md")]:
    t = (B / rel).read_text(encoding="utf-8").splitlines()
    mulai = None
    for i, l in enumerate(t):
        if re.match(r"^#+ .*(BELUM TERVERIFIKASI|belum terverifikasi|Yang belum terverifikasi)", l):
            mulai = i
    if mulai is None:
        print(nama, "TIDAK ADA bagian belum terverifikasi")
        continue
    butir = [l for l in t[mulai + 1:] if l.strip().startswith(("-", "*", "1", "2", "3", "4", "5", "6", "7", "8", "9"))]
    print(nama, "bagian di baris", mulai + 1, "| butir:", len(butir))

print("\n--- kalimat BELUM per lapisan ---")
for nama, rel in [("S1", "docs/RND_S1_SEED_ROBUSTNESS.md"), ("S2", "docs/RND_S2_HYBRID_VIB_SSI.md"),
                  ("S3", "docs/RND_S3_HYBRID_BITWEAR.md"), ("S4", "docs/RND_S4_LAYER_B_DATA.md")]:
    t = (B / rel).read_text(encoding="utf-8")
    hits = re.findall(r"[^.\n]{0,160}BELUM TERUKUR[^.\n]{0,160}", t)
    print(f"{nama}: {len(hits)} kalimat BELUM TERUKUR")
    for h in hits[:3]:
        print("   ", h.strip()[:200])
