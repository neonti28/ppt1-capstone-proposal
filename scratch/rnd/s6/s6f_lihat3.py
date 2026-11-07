"""Cetak sisa bagian pilihan.json: kelas tool_wear/bit_wear, kutipan, tier,
kandidat baru, tidak boleh diklaim, belum terukur, roadmap."""
import json

B = "/mnt/d/Capstone 1(v2)"
P = json.load(open(f"{B}/scratch/rnd/s6/pilihan.json"))
for k in ("tool_wear", "bit_wear"):
    print(f"=== {k} ===")
    print(json.dumps(P["pilihan_per_kelas"][k], indent=1, ensure_ascii=False))
for k in ("kutipan_kartu_lain", "usulan_tier", "kandidat_baru", "tidak_boleh_diklaim",
          "belum_terukur", "roadmap_gelombang_3"):
    print(f"\n=== {k} ===")
    print(json.dumps(P[k], indent=1, ensure_ascii=False)[:4200])
