import json, pathlib
B = pathlib.Path("/mnt/d/Capstone 1(v2)/scratch/rnd")

def g(f, path):
    d = json.loads((B / f).read_text(encoding="utf-8"))
    cur = d
    for k in path.split("."):
        cur = cur[int(k)] if isinstance(cur, list) else cur[k]
    return cur

uji = [
    ("s2", "s2_ringkas.json", "ssi.sensitivitas.ML_kalender_b24.precision_median"),
    ("s2", "s2_ringkas.json", "vib.agregat.persistence.far24_kalender_median"),
    ("s3", "s3c_ringkas.json", "agregat.ml_fisik.far24_median_valid"),
    ("s4", "labels_duration.json", "n_baris"),
    ("s4", "labels_duration.json", "sumber.kolom"),
]
for kartu, f, p in uji:
    try:
        v = g(f, p)
        print(kartu, f, p, "->", (len(v) if isinstance(v, (list, dict)) else v),
              ("(list)" if isinstance(v, list) else ""))
    except Exception as e:
        print(kartu, f, p, "-> ERROR", type(e).__name__, e)

# cari kunci yang mengandung potongan nama untuk S2-448/449 dan S3-085
print("\n--- s2_ringkas keys ---")
d = json.loads((B / "s2/s2_ringkas.json").read_text(encoding="utf-8"))
print("top:", list(d.keys()))
print("ssi keys:", list(d["ssi"].keys()))
print("ssi.sensitivitas keys:", list(d["ssi"].get("sensitivitas", {}).keys())[:15])
for k in list(d["ssi"].get("sensitivitas", {}))[:3]:
    print("  ", k, d["ssi"]["sensitivitas"][k])
print("vib.agregat keys:", list(d["vib"].get("agregat", {}).keys()))
print("vib.agregat.persistence:", d["vib"].get("agregat", {}).get("persistence"))

print("\n--- s3c agregat.ml_fisik ---")
d3 = json.loads((B / "s3/s3c_ringkas.json").read_text(encoding="utf-8"))
print(json.dumps(d3.get("agregat", {}).get("ml_fisik", {}), indent=1)[:900])

print("\n--- s4 labels_duration n_baris + kolom ---")
d4 = json.loads((B / "s4/labels_duration.json").read_text(encoding="utf-8"))
print("n_baris", d4.get("n_baris"), "| n kolom", len(d4.get("sumber", {}).get("kolom", [])))
