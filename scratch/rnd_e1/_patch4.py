p = "/mnt/d/Capstone 1(v2)/scratch/rnd_e1/e1_build.py"
s = open(p).read()

anchor = '''# wakil terbaik per algoritma (hanya status ADA atau SEBAGIAN, skor sel > 0)
TERBAIK = {}
for r in PASANGAN:
    if r["status_data"] == "TIDAK" or r["skor_sel"] == 0 or r["skor_prioritas"] == 0:
        continue
    k = r["algoritma"]
    if k not in TERBAIK or r["skor_prioritas"] > TERBAIK[k]["skor_prioritas"]:
        TERBAIK[k] = r

PERINGKAT = sorted(TERBAIK.values(), key=lambda r: (-r["skor_prioritas"], r["algoritma"]))'''

new = '''# Engine sasaran per algoritma. Dipilih dari rekomendasi R1-R6, bukan dari skor tertinggi,
# supaya algoritma tidak diberi panggung pada engine yang jelas tidak butuh dia.
TARGET = {
    "A01": "vib", "A02": "hyd", "A03": "vib", "A04": "tool_wear", "A05": "vib",
    "A06": "shk", "A07": "tool_wear", "A08": "vib", "A09": "hyd", "A10": "hyd",
    "A11": "stuck", "A12": "tool_wear", "A13": "stuck", "A14": "hyd", "A15": "tool_wear",
    "A16": "tool_wear", "A17": "tool_wear", "A18": "bit_wear", "A19": "vib", "A20": "hyd",
    "A21": "hyd", "A22": "hyd", "A23": "hyd", "A24": "vib", "A25": "vib",
    "A26": "stuck", "A27": "vib", "A28": "vib",
}
assert set(TARGET) == {a["kode"] for a in A}, "TARGET harus mencakup semua algoritma"

TERBAIK = {}
for r in PASANGAN:
    if r["engine"] != TARGET[r["algoritma"]]:
        continue
    TERBAIK[r["algoritma"]] = r
PERINGKAT = sorted(TERBAIK.values(), key=lambda r: (-r["skor_prioritas"], r["algoritma"]))'''
assert anchor in s
s = s.replace(anchor, new)

# tambahkan target ke JSON peringkat
s = s.replace('''    "peringkat_algoritma": PERINGKAT,''',
'''    "target_engine": TARGET,
    "peringkat_algoritma": PERINGKAT,''')
open(p, "w").write(s)
print("ok")
