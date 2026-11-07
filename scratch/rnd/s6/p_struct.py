import json

B = "/mnt/d/Capstone 1(v2)"
V = json.load(open(f"{B}/scratch/rnd/s6/s6_verifikasi.json"))
K = json.load(open(f"{B}/scratch/rnd/s6/s6_kandidat.json"))

print("== V keys:", list(V.keys()))
print("== K keys:", list(K.keys()))
print("== jumlah_cek", V.get("jumlah_cek"), V.get("jumlah_cek_lulus"))
print("== ringkas kelas:", list(V["ringkas"].keys()))
for kelas, d in V["ringkas"].items():
    print("  ", kelas, "model:", list(d.keys()))
    mo = list(d.keys())[0]
    print("    field contoh:", list(d[mo].keys()))
print("== turunan keys:", list(V["turunan"].keys()))
print("== meta:", V["turunan"].get("meta"))
print("== kontrol_ml:", V["turunan"].get("kontrol_ml"))
print("== galat_reproduksi_s2:", V["turunan"].get("galat_reproduksi_s2"))
print("== K meta:", K.get("meta"))
