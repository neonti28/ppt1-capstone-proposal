import json, pathlib
B = pathlib.Path("/mnt/d/Capstone 1(v2)/scratch/rnd")
s1 = json.loads((B / "s1/s1_hyd_seeds.json").read_text(encoding="utf-8"))
print("sebaran:", json.dumps(s1["kontrol_stokastik"]["sebaran"], ensure_ascii=False))
print("kontrol per_seed keys:", list(s1["kontrol_stokastik"]["per_seed"].keys()))
sat = json.loads((B / "s1/s1_h_saturasi.json").read_text(encoding="utf-8"))
print("n_saturasi:", sat["n_saturasi"], "n_fold:", sat["n_fold"], "h_grid_maks:", sat["h_grid_maks"],
      "well_kalibrasi_unik:", sat["well_kalibrasi_unik"])
print("h_terkecil_lolos:", sat["h_terkecil_lolos_anggaran_di_luar_grid"])
