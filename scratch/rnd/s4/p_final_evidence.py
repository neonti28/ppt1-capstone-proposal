"""Bukti mentah akhir untuk laporan: blok kunci dari tiap JSON."""
import json, os
ROOT = "/mnt/d/Capstone 1(v2)"
S4 = os.path.join(ROOT, "scratch/rnd/s4")
def L(n): return json.load(open(os.path.join(S4, n), encoding="utf-8"))

dt = L("ddr_downtime_table.json")
print("== ddr_downtime_table ==")
print("tabel:", {k: dt["tabel"][k] for k in ("n_file_memuat_tabel", "persen_file_memuat_tabel")}, "| sumber:", dt["sumber"])
print("record:", dt["record"])
print("n_kelas_equipment_unik:", dt["n_kelas_equipment_unik"])

inv = L("inventory.json")
print("\n== metrik_lapisan_b (kunci) ==")
m = inv["metrik_lapisan_b"]
for k in sorted(m):
    v = m[k]
    if isinstance(v, dict):
        flat = {kk: v[kk] for kk in v if not isinstance(v[kk], (dict, list))}
        print(k, flat)
    else:
        print(k, v)

cc = L("crosscheck.json")
print("\n== crosscheck total ==")
print(cc["silang_total"])
print("pres_test_type:", cc["pres_test_type"]["n_laporan_dengan_uji"], cc["pres_test_type"]["distribusi"])
print("kode_activity_bernuansa:", cc["kode_activity_bernuansa"]["n_record"])

raw = L("inventory_raw.json")
print("\n== pindai token XML ==")
print({k: v for k, v in raw["pindai_xml_ddr"]["kemunculan"].items() if v})
print("== pindai token HTML ==")
print({k: v for k, v in raw["pindai_html_ddr"]["kemunculan"].items() if v})
print("berkas dipindai xml:", raw["pindai_xml_ddr"]["n_file"], "html:", raw["pindai_html_ddr"]["n_file"])
