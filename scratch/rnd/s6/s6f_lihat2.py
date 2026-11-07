"""Ringkas 15 baris tabel ke satu baris teks per kandidat, plus pilihan_per_kelas."""
import json

B = "/mnt/d/Capstone 1(v2)"
P = json.load(open(f"{B}/scratch/rnd/s6/pilihan.json"))

print("=== 15 BARIS TABEL ===")
hdr = ("kelas", "kandidat", "asal", "pres", "rec", "recmin", "far24", "farmax", "f_far6", "f_gateA", "lead", "diper")
print(" | ".join(hdr))
for t in P["tabel_perbandingan"]:
    A, Bb, C = t["lapisan_A"], t["lapisan_B"], t["lapisan_C"]
    print(" | ".join(str(x) for x in (
        t["kelas"], t["kandidat"], t["asal"],
        A.get("presisi_median"), A.get("recall_median"), A.get("recall_min_fold"),
        A.get("far24_kalender_median"), A.get("far24_kalender_maks"),
        f"{A.get('fold_far_le6')}/{A.get('n_fold')}", A.get("fold_gate_A"),
        Bb.get("lead_median_menit"), Bb.get("n_diperingatkan"),
    )))

print("\n=== PILIHAN PER KELAS ===")
print(json.dumps(P["pilihan_per_kelas"], indent=1, ensure_ascii=False))
